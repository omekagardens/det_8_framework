"""QR-05AZ independent reference: physical refinement and exact tile integrals.

The source producer and receiver evaluate only explicitly supplied raw values.
Geometry is supplied explicitly. No historical executor or stored answer is consumed.
"""

from copy import deepcopy
from fractions import Fraction
from math import gcd

MAX_BITS = 4096
ZERO = Fraction(0)
ONE = Fraction(1)


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Native containers may share children, but may not contain cycles."""
    pending = [(value, False)]
    active, done = set(), set()
    while pending:
        current, leaving = pending.pop()
        kind = type(current)
        if kind in (dict, list):
            identity = id(current)
            if leaving:
                active.remove(identity)
                done.add(identity)
                continue
            _need(identity not in active, "cyclic native input")
            if identity in done:
                continue
            active.add(identity)
            pending.append((current, True))
            if kind is dict:
                _need(all(type(k) is str for k in current), "native object keys")
                pending.extend((v, False) for v in current.values())
            else:
                pending.extend((v, False) for v in current)
        else:
            _need(kind in (str, int, type(None)), "non-native mathematical input")
            if kind is int:
                _need(abs(current).bit_length() <= MAX_BITS, "integer bits")


def _keys(value, expected):
    _need(type(value) is dict and set(value) == set(expected), "object fields")


def _fraction(value):
    _need(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    _need(type(n) is int and type(d) is int and d > 0, "fraction integers")
    _need(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "fraction bits")
    _need(gcd(n, d) == 1, "reduced fraction")
    return Fraction(n, d)


def _wire(value):
    if type(value) is Fraction:
        _need(
            max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
            "retained rational bits",
        )
        return [value.numerator, value.denominator]
    if type(value) in (list, tuple):
        return [_wire(x) for x in value]
    if type(value) is dict:
        return {k: _wire(v) for k, v in value.items()}
    if type(value) is int:
        _need(abs(value).bit_length() <= MAX_BITS, "retained integer bits")
    _need(type(value) in (str, int, bool, type(None)), "internal output type")
    return value


def _dimensions(matrix, rows, columns):
    _need(type(matrix) is list and len(matrix) == rows, "matrix rows")
    _need(
        all(type(row) is list and len(row) == columns for row in matrix),
        "matrix width",
    )


def _matrix(matrix):
    return [[_fraction(x) for x in row] for row in matrix]


def _dot(row, vector):
    return sum((a * b for a, b in zip(row, vector) if a and b), ZERO)


def _pair_shapes(values):
    _need(all(type(x) is list and len(x) == 2 for x in values), "rational pair shapes")


def _matrix_pair_shapes(matrix):
    for row in matrix:
        _pair_shapes(row)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _evaluate(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _need(type(matrix) is list and len(matrix) <= row_cap, "raw row inventory")
    _need(type(values) is list and len(values) <= width_cap, "raw width inventory")
    _dimensions(matrix, len(matrix), len(values))
    _matrix_pair_shapes(matrix)
    _pair_shapes(values)
    rows = _matrix(matrix)
    vector = [_fraction(x) for x in values]
    return _wire(_matvec(rows, vector))


def produce(matrix, values):
    return _evaluate(matrix, values, 1024, 1024)


def apply(matrix, observed):
    return _evaluate(matrix, observed, 64, 320)


def _rectangle_shape(rectangle):
    _need(type(rectangle) is list and len(rectangle) == 4, "rectangle shape")


def _parse_parent(problem, children):
    _native(problem)
    _keys(
        problem,
        (
            "family",
            "probe",
            "cells",
            "tiles",
            "bank_labels",
            "target_labels",
            "interface",
            "geometric",
            "decoder",
        ),
    )
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    probe, cells, tiles = (problem[key] for key in ("probe", "cells", "tiles"))
    _rectangle_shape(probe)
    _need(type(cells) is list and 1 <= len(cells) <= 8, "cell inventory")
    _need(type(tiles) is list and 1 <= len(tiles) <= 256, "tile inventory")
    ids = []
    rectangles = [probe]
    by_id = {}
    for cell in cells:
        _keys(cell, ("event", "bounds"))
        _need(type(cell["event"]) is int, "native cell ID")
        ids.append(cell["event"])
        by_id[cell["event"]] = cell["bounds"]
        if cell["bounds"] is not None:
            _rectangle_shape(cell["bounds"])
            rectangles.append(cell["bounds"])
    _need(ids == sorted(set(ids)), "sorted unique cell IDs")
    for tile in tiles:
        _keys(tile, ("event", "bounds"))
        _need(type(tile["event"]) is int and tile["event"] in by_id, "known tile owner")
        _need(by_id[tile["event"]] is not None, "tile owner is positive")
        _rectangle_shape(tile["bounds"])
        rectangles.append(tile["bounds"])
    t = len(tiles)
    r = 4 * t
    bank_labels = problem["bank_labels"]
    _need(type(bank_labels) is list and len(bank_labels) == r, "bank label inventory")
    for index, label in enumerate(bank_labels):
        _keys(label, ("tile", "basis"))
        _need(
            type(label["tile"]) is int
            and type(label["basis"]) is int
            and label["tile"] == index // 4
            and label["basis"] == index % 4,
            "actual tile-major bank label",
        )
    B, G, D = (problem[key] for key in ("interface", "geometric", "decoder"))
    _need(type(G) is list and 1 <= len(G) <= 64, "target inventory")
    q = len(G)
    _need(type(B) is list and len(B) <= 320, "receiver inventory")
    s = len(B)
    for matrix, rows, columns in ((B, s, r), (G, q, r), (D, q, s)):
        _dimensions(matrix, rows, columns)
    targets = problem["target_labels"]
    _need(type(targets) is list and len(targets) == q, "target label inventory")
    pairs = []
    for label in targets:
        _keys(label, ("first", "second"))
        _need(
            type(label["first"]) is int
            and type(label["second"]) is int
            and label["first"] in by_id
            and label["second"] in by_id,
            "known target cell IDs",
        )
        pairs.append((label["first"], label["second"]))
    _need(pairs == sorted(set(pairs)), "sorted unique target pairs")
    for rectangle in rectangles:
        _pair_shapes(rectangle)
    for matrix in (B, G, D):
        _matrix_pair_shapes(matrix)
    _need(type(children) is list and 1 <= len(children) <= 256, "child inventory")
    child_parents = []
    for child in children:
        _keys(child, ("parent", "bounds"))
        _need(type(child["parent"]) is int and 0 <= child["parent"] < t, "parent tile index")
        child_parents.append(child["parent"])
        _rectangle_shape(child["bounds"])
    for child in children:
        _pair_shapes(child["bounds"])
    # BOTH full shapes precede all Fractions; ALL values precede geometry.
    probe = [_fraction(x) for x in probe]
    cell_bounds = [
        None if cell["bounds"] is None else [_fraction(x) for x in cell["bounds"]] for cell in cells
    ]
    tile_bounds = [[_fraction(x) for x in tile["bounds"]] for tile in tiles]
    B, G, D = (_matrix(matrix) for matrix in (B, G, D))
    child_bounds = [[_fraction(x) for x in child["bounds"]] for child in children]
    return (
        probe,
        ids,
        cell_bounds,
        tile_bounds,
        [tile["event"] for tile in tiles],
        pairs,
        B,
        G,
        D,
        child_parents,
        child_bounds,
    )


def _volume(rectangle):
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _inside(inner, outer):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def _overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def _geometry(probe, ids, cells, tiles, owners, pairs):
    positive = [rectangle for rectangle in cells if rectangle is not None]
    for rectangle in [probe] + positive + tiles:
        _need(rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3], "positive rectangle")
    for inventory in (positive, tiles):
        for i, left in enumerate(inventory):
            for right in inventory[i + 1 :]:
                _need(not _overlap(left, right), "disjoint interiors")
    _need(all(_inside(rectangle, probe) for rectangle in positive), "cells inside probe")
    V = _volume(probe)
    cell_volumes = [ZERO if rectangle is None else _volume(rectangle) for rectangle in cells]
    _need(sum(cell_volumes, ZERO) == V, "cells cover probe")
    by_id = dict(zip(ids, cells))
    for rectangle, owner in zip(tiles, owners):
        _need(_inside(rectangle, by_id[owner]), "tile inside named cell")
    tile_volumes = [_volume(rectangle) for rectangle in tiles]
    for event, h in zip(ids, cell_volumes):
        _need(
            sum((v for v, owner in zip(tile_volumes, owners) if owner == event), ZERO) == h,
            "tiles cover each positive cell",
        )
    h_by_id = dict(zip(ids, cell_volumes))
    sigma = [V * V * h_by_id[first] * h_by_id[second] for first, second in pairs]
    defined = [i for i, value in enumerate(sigma) if value > ZERO]
    undefined = [i for i, value in enumerate(sigma) if value == ZERO]
    return V, cell_volumes, tile_volumes, sigma, defined, undefined


def _inverse(matrix):
    """Independent pivoted exact elimination; no triangular inverse formula."""
    width = len(matrix)
    augmented = [
        list(row) + [ONE if i == j else ZERO for j in range(width)] for i, row in enumerate(matrix)
    ]
    for column in range(width):
        pivot = next((i for i in range(column, width) if augmented[i][column]), None)
        _need(pivot is not None, "invertible coordinate block")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for i in range(width):
            if i == column:
                continue
            factor = augmented[i][column]
            augmented[i] = [a - factor * b for a, b in zip(augmented[i], augmented[column])]
    return [row[width:] for row in augmented]


def _values(vector):
    return [_fraction(value) for value in vector]


def _integration_geometry(probe, tiles):
    _need(probe[0] < probe[1] and probe[2] < probe[3], "positive probe")
    for i, tile in enumerate(tiles):
        _need(_inside(tile, probe), "positive tile inside probe")
        for earlier in tiles[:i]:
            _need(not _overlap(tile, earlier), "disjoint integration tile interiors")
    return _volume(probe)


def _corner_value(corners, x, y):
    weights = ((ONE - x) * (ONE - y), x * (ONE - y), (ONE - x) * y, x * y)
    return _dot(corners, weights)


def _integrals(V, tile, corners):
    """Integrate the actual field, not a previously synthesized moment vector."""
    a, end_u, b, end_v = tile
    du, dv = end_u - a, end_v - b
    amplitude, h = V * V, _volume(tile)
    c00, c10, c01, c11 = corners
    local_coeff = [
        amplitude * c00,
        amplitude * (c10 - c00),
        amplitude * (c01 - c00),
        amplitude * (c11 - c10 - c01 + c00),
    ]
    physical_corners = [(a, b), (end_u, b), (a, end_v), (end_u, end_v)]
    evaluation = [[ONE, u, v, u * v] for u, v in physical_corners]
    global_coeff = _matvec(_inverse(evaluation), [amplitude * c for c in corners])
    local_sums, raw_sums = [ZERO] * 4, [ZERO] * 4
    # Tensor Simpson integrates coordinatewise degree <= 3 exactly.
    # Here field times any requested monomial has degree <= 2 in each axis.
    nodes = ((ZERO, ONE / 6), (ONE / 2, 2 * ONE / 3), (ONE, ONE / 6))
    for x, wx in nodes:
        for y, wy in nodes:
            u, v = a + du * x, b + dv * y
            local_monomials = [ONE, x, y, x * y]
            global_monomials = [ONE, u, v, u * v]
            field = amplitude * _corner_value(corners, x, y)
            _need(
                field == _dot(local_coeff, local_monomials)
                and field == _dot(global_coeff, global_monomials),
                "actual local/global field reconstruction",
            )
            weighted = h * wx * wy * field
            for j in range(4):
                local_sums[j] += weighted * local_monomials[j]
                raw_sums[j] += weighted * global_monomials[j]
    return {
        "local_coefficients": local_coeff,
        "global_coefficients": global_coeff,
        "local_moments": [value / (amplitude * h) for value in local_sums],
        "raw_moments": raw_sums,
        "minima": [amplitude * min(corners)],
        "maxima": [amplitude * max(corners)],
    }


def integrate(probe, tiles, corners):
    """Actual signed bilinear fields; unrestricted corners and incomplete coverage."""
    for value in (probe, tiles, corners):
        _native(value)
    _rectangle_shape(probe)
    _need(type(tiles) is list and len(tiles) <= 256, "integration tile inventory")
    _need(type(corners) is list and len(corners) == 4 * len(tiles), "corner width")
    for tile in tiles:
        _rectangle_shape(tile)
    for rectangle in [probe] + tiles:
        _pair_shapes(rectangle)
    _pair_shapes(corners)
    parsed_probe = _values(probe)
    parsed_tiles = [_values(tile) for tile in tiles]
    values = _values(corners)
    V = _integration_geometry(parsed_probe, parsed_tiles)
    result = {
        key: []
        for key in (
            "local_coefficients",
            "global_coefficients",
            "local_moments",
            "raw_moments",
            "minima",
            "maxima",
        )
    }
    for index, tile in enumerate(parsed_tiles):
        part = _integrals(V, tile, values[4 * index : 4 * index + 4])
        for key, output in result.items():
            output.extend(part[key])
    return _wire(result)


def _kernel_tile(tile, coefficients):
    a, b, c, d = tile
    physical = ((a, c), (b, c), (a, d), (b, d))
    vertices = [_dot(coefficients, [ONE, u, v, u * v]) for u, v in physical]
    v00, v10, v01, v11 = vertices
    local = [v00, v10 - v00, v01 - v00, v11 - v10 - v01 + v00]
    total, bernstein = ZERO, [ZERO] * 4
    nodes = ((ZERO, ONE / 6), (ONE / 2, 2 * ONE / 3), (ONE, ONE / 6))
    h, lo, hi = _volume(tile), min(vertices), max(vertices)
    for x, wx in nodes:
        for y, wy in nodes:
            u, v = a + (b - a) * x, c + (d - c) * y
            kernel = _dot(local, [ONE, x, y, x * y])
            _need(kernel == _dot(coefficients, [ONE, u, v, u * v]), "physical kernel interpolation")
            _need(lo <= kernel <= hi, "interpolated kernel range")
            corner_basis = [(ONE - x) * (ONE - y), x * (ONE - y), (ONE - x) * y, x * y]
            _need(
                all(z >= ZERO for z in corner_basis) and sum(corner_basis, ZERO) == ONE,
                "nonnegative corner partition",
            )
            weighted = h * wx * wy * kernel
            total += weighted
            for j in range(4):
                bernstein[j] += weighted * corner_basis[j]
    _need(sum(bernstein, ZERO) == total, "corner integral partition")
    upper = h * max(abs(lo), abs(hi))
    _need(
        abs(total) <= upper and sum((abs(z) for z in bernstein), ZERO) <= upper,
        "finite corner envelope",
    )
    if lo == hi == ZERO:
        kind = "zero"
    elif lo >= ZERO:
        kind = "nonnegative"
    elif hi <= ZERO:
        kind = "nonpositive"
    else:
        kind = "mixed"
    return vertices, total, bernstein, upper, lo, hi, kind


def inspect_kernel(probe, tiles, coefficients):
    for value in (probe, tiles, coefficients):
        _native(value)
    _rectangle_shape(probe)
    _need(type(tiles) is list and len(tiles) <= 256, "kernel tile inventory")
    _need(type(coefficients) is list and len(coefficients) <= 64, "kernel row inventory")
    for tile in tiles:
        _rectangle_shape(tile)
    _dimensions(coefficients, len(coefficients), 4 * len(tiles))
    for rectangle in [probe] + tiles:
        _pair_shapes(rectangle)
    _matrix_pair_shapes(coefficients)
    parsed_probe, parsed_tiles, rows = (
        _values(probe),
        [_values(t) for t in tiles],
        _matrix(coefficients),
    )
    _integration_geometry(parsed_probe, parsed_tiles)
    out = {
        key: []
        for key in (
            "corner_values",
            "tile_integrals",
            "bernstein_integrals",
            "tile_abs_upper",
            "tile_minima",
            "tile_maxima",
            "tile_classes",
        )
    }
    for row in rows:
        values = [_kernel_tile(t, row[4 * i : 4 * i + 4]) for i, t in enumerate(parsed_tiles)]
        for key, index in (
            ("corner_values", 0),
            ("tile_integrals", 1),
            ("tile_abs_upper", 3),
            ("tile_minima", 4),
            ("tile_maxima", 5),
            ("tile_classes", 6),
        ):
            out[key].append([value[index] for value in values])
        out["bernstein_integrals"].append([z for value in values for z in value[2]])
    return _wire(out)


def _bank_probe(problem, G):
    q, r = len(G), len(G[0])
    K = [[ZERO] * r for _ in range(q)]
    for j in range(r):
        unit = [ZERO] * r
        unit[j] = ONE
        observed = produce(problem["interface"], _wire(unit))
        decoded = _values(apply(problem["decoder"], observed))
        for i, value in enumerate(decoded):
            K[i][j] = value
    residual = [[K[i][j] - G[i][j] for j in range(r)] for i in range(q)]
    _need(not any(z for row in residual for z in row), "complete frozen bank identity")
    return K, residual


def _sign(value):
    return int(value > ZERO) - int(value < ZERO)


def _radius(row):
    lower = sum((min(-z, z) for z in row), ZERO)
    upper = sum((max(-z, z) for z in row), ZERO)
    _need(lower == -upper, "symmetric interval")
    return upper


def _maximum(values):
    domain = [i for i, value in enumerate(values) if value is not None]
    if not domain:
        return {"gain": None, "rows": []}
    gain = max(values[i] for i in domain)
    return {"gain": gain, "rows": [i for i in domain if values[i] == gain]}


def _comparison(larger, smaller):
    gap = [None if lo is None or hi is None else hi - lo for hi, lo in zip(larger, smaller)]
    available = [i for i, x in enumerate(gap) if x is not None]
    unavailable = [i for i, x in enumerate(gap) if x is None]
    _need(all(gap[i] >= ZERO for i in available), "lower/upper order")
    strict = [i for i in available if gap[i] > ZERO]
    tied = [i for i in available if gap[i] == ZERO]
    _need(sorted(strict + tied + unavailable) == list(range(len(gap))), "comparison partition")
    maximum = _maximum(gap)
    return {
        "gain_gap": gap,
        "strict_rows": strict,
        "tied_rows": tied,
        "unavailable_rows": unavailable,
        "max_gap": maximum["gain"],
        "max_gap_rows": maximum["rows"],
    }


def _level(problem, V, sigma, defined, undefined):
    """New compact level calculation; no prior family executor or old witnesses."""
    G = _matrix(problem["geometric"])
    K, Rbank = _bank_probe(problem, G)
    kernel_wire = inspect_kernel(
        problem["probe"], [t["bounds"] for t in problem["tiles"]], problem["geometric"]
    )
    corners = [[_values(t) for t in row] for row in kernel_wire["corner_values"]]
    integrals = _matrix(kernel_wire["tile_integrals"])
    bernstein = _matrix(kernel_wire["bernstein_integrals"])
    upper = _matrix(kernel_wire["tile_abs_upper"])
    classes = kernel_wire["tile_classes"]
    q = len(G)
    J = [[V * V * z for z in row] for row in bernstein]
    A = [None if not scale else [z / scale for z in row] for scale, row in zip(sigma, J)]
    C = [
        None if not sigma[i] else V * V * sum((abs(z) for z in row), ZERO) / sigma[i]
        for i, row in enumerate(integrals)
    ]
    L = [None if row is None else _radius(row) for row in A]
    U = [None if not sigma[i] else V * V * sum(row, ZERO) / sigma[i] for i, row in enumerate(upper)]
    _need(all(ZERO <= C[i] <= L[i] <= U[i] for i in defined), "complete bound order")
    obstructions = []
    for row in corners:
        obs = []
        for j, values in enumerate(row):
            positive = next((a for a, v in enumerate(values) if v > ZERO), None)
            negative = next((a for a, v in enumerate(values) if v < ZERO), None)
            if positive is not None and negative is not None:
                obs.append({"tile": j, "positive_corner": positive, "negative_corner": negative})
        obstructions.append(obs)
    _need(
        all(
            [x["tile"] for x in obstructions[i]]
            == [j for j, kind in enumerate(row) if kind == "mixed"]
            for i, row in enumerate(classes)
        ),
        "complete mixed obstruction inventory",
    )
    _need(all(not obstructions[i] for i in undefined), "undefined zero kernel obstructions")
    certified = [i for i in defined if not obstructions[i]]
    uncertified = [i for i in defined if obstructions[i]]
    _need(
        sorted(certified + uncertified + undefined) == list(range(q)),
        "certificate domain partition",
    )
    exact = [L[i] if i in certified else None for i in range(q)]
    for i in certified:
        _need(C[i] == L[i], "sign-definite exact absolute integral")
        for kind, value, vertex in zip(classes[i], integrals[i], corners[i]):
            sign = _sign(value)
            _need(
                (kind == "zero" and sign == 0)
                or (kind == "nonnegative" and sign == 1)
                or (kind == "nonpositive" and sign == -1),
                "certified tile sign integral",
            )
            _need(all(sign * z >= ZERO for z in vertex), "pointwise sign alignment")
    point_nonneg = [i for i in defined if all(z >= ZERO for tile in corners[i] for z in tile)]
    point_nonpos = [i for i in defined if all(z <= ZERO for tile in corners[i] for z in tile)]
    point_zero = [i for i in defined if not any(z for tile in corners[i] for z in tile)]
    integrated_nonneg = [i for i in defined if all(z >= ZERO for z in A[i])]
    integrated_nonpos = [i for i in defined if all(z <= ZERO for z in A[i])]
    integrated_zero = [i for i in defined if not any(A[i])]
    _need(
        set(point_nonneg) & set(point_nonpos) == set(point_zero)
        and set(integrated_nonneg) & set(integrated_nonpos) == set(integrated_zero),
        "pointwise/integrated zero intersections",
    )
    _need(
        all(i in certified for i in point_nonneg + point_nonpos),
        "global sign implies tile certificate",
    )
    status = [
        "undefined" if i in undefined else "certified" if i in certified else "uncertified"
        for i in range(q)
    ]

    bounds = {"constant_lower": C, "bilinear_lower": L, "corner_upper": U, "certified_gain": exact}
    integrated_mixed = [i for i in uncertified if i in integrated_nonneg]
    return _wire(
        {
            "kernels": kernel_wire,
            "maps": {
                "decoder_bank": K,
                "bank_residual": Rbank,
                "raw_bilinear_target": J,
                "normalized_bilinear_target": A,
            },
            "bounds": {
                **bounds,
                "maxima": {key: _maximum(values) for key, values in bounds.items()},
            },
            "certification": {
                "status": status,
                "mixed_obstructions": obstructions,
                "certified_rows": certified,
                "uncertified_rows": uncertified,
                "undefined_rows": undefined,
                "nonnegative_rows": point_nonneg,
                "nonpositive_rows": point_nonpos,
                "zero_rows": point_zero,
                "integrated_nonnegative_rows": integrated_nonneg,
                "integrated_nonpositive_rows": integrated_nonpos,
                "integrated_zero_rows": integrated_zero,
                "integrated_nonnegative_mixed_rows": integrated_mixed,
            },
        }
    )


def _child_partition(parents, children, lineage):
    """Endpoint-grid multiplicity, independent of an area-only coverage test."""
    for parent_index, parent in enumerate(parents):
        pieces = [child for child, owner in zip(children, lineage) if owner == parent_index]
        _need(bool(pieces), "every parent is represented")
        for piece in pieces:
            _need(_inside(piece, parent), "positive child inside named parent")
        xs = sorted({parent[0], parent[1]} | {x for piece in pieces for x in piece[:2]})
        ys = sorted({parent[2], parent[3]} | {y for piece in pieces for y in piece[2:]})
        xi, yi = {x: i for i, x in enumerate(xs)}, {y: i for i, y in enumerate(ys)}
        difference = [[0] * len(ys) for _ in xs]
        for u0, u1, v0, v1 in pieces:
            a, b, c, d = xi[u0], xi[u1], yi[v0], yi[v1]
            difference[a][c] += 1
            difference[b][c] -= 1
            difference[a][d] -= 1
            difference[b][d] += 1
        for i in range(len(xs)):
            for j in range(len(ys)):
                if i:
                    difference[i][j] += difference[i - 1][j]
                if j:
                    difference[i][j] += difference[i][j - 1]
                if i and j:
                    difference[i][j] -= difference[i - 1][j - 1]
                if i < len(xs) - 1 and j < len(ys) - 1:
                    _need(difference[i][j] == 1, "endpoint-grid exact child coverage")
    return [_volume(child) for child in children]


def _physical_vertices(tile):
    a, b, c, d = tile
    return ((a, c), (b, c), (a, d), (b, d))


def _restrictions(parents, children, lineage):
    evaluations = [
        _inverse([[ONE, u, v, u * v] for u, v in _physical_vertices(parent)]) for parent in parents
    ]
    result = []
    for child, owner in zip(children, lineage):
        inverse = evaluations[owner]
        block = []
        for u, v in _physical_vertices(child):
            monomials = [ONE, u, v, u * v]
            block.append(
                [sum((monomials[j] * inverse[j][a] for j in range(4)), ZERO) for a in range(4)]
            )
        _need(
            all(z >= ZERO for row in block for z in row)
            and all(sum(row, ZERO) == ONE for row in block),
            "convex physical restriction",
        )
        result.append(block)
    return result


def _moment_blocks(V, tiles):
    blocks = []
    for tile in tiles:
        columns = []
        for a in range(4):
            basis = [ONE if j == a else ZERO for j in range(4)]
            columns.append(_integrals(V, tile, basis)["raw_moments"])
        blocks.append([[columns[a][j] for a in range(4)] for j in range(4)])
    return blocks


def _matrix_product(left, right):
    return [
        [sum((row[k] * right[k][j] for k in range(len(right))), ZERO) for j in range(len(right[0]))]
        for row in left
    ]


def _difference(left, right):
    return [[a - b for a, b in zip(x, y)] for x, y in zip(left, right)]


def _zero_matrix(matrix, message):
    _need(not any(x for row in matrix for x in row), message)


def _aggregate_blocks(child_blocks, E, lineage, p):
    out = [[[ZERO] * 4 for _ in range(4)] for _ in range(p)]
    for child, block, owner in zip(child_blocks, E, lineage):
        product = _matrix_product(child, block)
        for i in range(4):
            for j in range(4):
                out[owner][i][j] += product[i][j]
    return out


def _restrict_rows(rows, E, lineage, p):
    out = []
    for row in rows:
        if row is None:
            out.append(None)
            continue
        target = [ZERO] * (4 * p)
        for index, (block, owner) in enumerate(zip(E, lineage)):
            source = row[4 * index : 4 * index + 4]
            for j in range(4):
                target[4 * owner + j] += sum((source[k] * block[k][j] for k in range(4)), ZERO)
        out.append(target)
    return out


def _sum_raw(vector, lineage, p):
    result = [ZERO] * (4 * p)
    for child, owner in enumerate(lineage):
        for j in range(4):
            result[4 * owner + j] += vector[4 * child + j]
    return result


def _restrict_corners(corners, E, lineage):
    return [
        value
        for block, owner in zip(E, lineage)
        for value in _matvec(block, corners[4 * owner : 4 * owner + 4])
    ]


def _nullable_matrix(rows):
    return [None if row is None else _values(row) for row in rows]


def _nullable_values(values):
    return [None if value is None else _fraction(value) for value in values]


def _nullable_residual(left, right):
    _need(
        all((x is None) == (y is None) for x, y in zip(left, right)),
        "identical normalization domain",
    )
    return [None if x is None else [a - b for a, b in zip(x, y)] for x, y in zip(left, right)]


def _child_problem(parent, children, lineage):
    result = deepcopy(parent)
    result["tiles"] = [
        {"event": parent["tiles"][owner]["event"], "bounds": deepcopy(child["bounds"])}
        for child, owner in zip(children, lineage)
    ]
    result["bank_labels"] = [
        {"tile": i, "basis": j} for i in range(len(children)) for j in range(4)
    ]
    for key in ("interface", "geometric"):
        result[key] = [
            [deepcopy(value) for owner in lineage for value in row[4 * owner : 4 * owner + 4]]
            for row in parent[key]
        ]
    return result


def _pipeline(problem, corners, V, sigma, level, defined, undefined):
    _need(all(-ONE <= x <= ONE for x in corners), "bounded field corner data")
    raw = integrate(problem["probe"], [t["bounds"] for t in problem["tiles"]], _wire(corners))
    field = {key: _values(value) for key, value in raw.items()}
    observed_wire = produce(problem["interface"], raw["raw_moments"])
    observed = _values(observed_wire)
    direct = _values(produce(problem["geometric"], raw["raw_moments"]))
    decoded = _values(apply(problem["decoder"], observed_wire))
    normalized = [x / scale if scale else None for x, scale in zip(decoded, sigma)]
    J = _matrix(level["maps"]["raw_bilinear_target"])
    A = _nullable_matrix(level["maps"]["normalized_bilinear_target"])
    L, U = (_nullable_values(level["bounds"][key]) for key in ("bilinear_lower", "corner_upper"))
    _need(direct == decoded == _matvec(J, corners), "full raw pipeline identity")
    _need(
        all(normalized[i] == _dot(A[i], corners) for i in defined)
        and all(normalized[i] is None for i in undefined),
        "normalized pipeline identity",
    )
    _need(
        all(-L[i] <= normalized[i] <= L[i] and -U[i] <= normalized[i] <= U[i] for i in defined),
        "all target field bounds",
    )
    _need(
        all(-V * V <= lo <= hi <= V * V for lo, hi in zip(field["minima"], field["maxima"])),
        "actual bounded field extrema",
    )
    return {
        "corners": corners,
        "global_coefficients": field["global_coefficients"],
        "bank_error": field["raw_moments"],
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "tile_minima": field["minima"],
        "tile_maxima": field["maxima"],
    }


def _pipeline_pair(parent, child, corners, E, lineage, V, sigma, levels, defined, undefined):
    parent_output = _pipeline(parent, corners, V, sigma, levels["parent"], defined, undefined)
    child_corners = _restrict_corners(corners, E, lineage)
    child_output = _pipeline(child, child_corners, V, sigma, levels["child"], defined, undefined)
    p = len(parent["tiles"])
    aggregate = _sum_raw(child_output["bank_error"], lineage, p)
    bank_residual = [a - b for a, b in zip(aggregate, parent_output["bank_error"])]
    residuals = {}
    for key in ("observed", "direct", "decoded", "normalized"):
        left, right = child_output[key + "_error"], parent_output[key + "_error"]
        _need(
            all((a is None) == (b is None) for a, b in zip(left, right)),
            "paired normalization domain",
        )
        residuals[key + "_residual"] = [None if a is None else a - b for a, b in zip(left, right)]
    coefficients = []
    for index, owner in enumerate(lineage):
        coefficients.extend(
            a - b
            for a, b in zip(
                child_output["global_coefficients"][4 * index : 4 * index + 4],
                parent_output["global_coefficients"][4 * owner : 4 * owner + 4],
            )
        )
    _need(
        not any(bank_residual)
        and not any(coefficients)
        and all(all(value is None or value == ZERO for value in row) for row in residuals.values()),
        "same physical field paired responses and global moment additivity",
    )
    return {
        "parent": parent_output,
        "child": child_output,
        "aggregated_bank_error": aggregate,
        "bank_residual": bank_residual,
        **residuals,
        "field_coefficient_residual": coefficients,
    }


def build_family(supplied):
    _native(supplied)
    _keys(supplied, ("parent", "children"))
    parent, children = supplied["parent"], supplied["children"]
    (probe, ids, cells, parent_tiles, owners, pairs, B, G, _D, lineage, child_tiles) = (
        _parse_parent(parent, children)
    )
    V, cell_volumes, parent_volumes, sigma, defined, undefined = _geometry(
        probe,
        ids,
        cells,
        parent_tiles,
        owners,
        pairs,
    )
    for i in undefined:
        _need(not any(G[i]), "undefined raw target kernel")
    child_volumes = _child_partition(parent_tiles, child_tiles, lineage)
    p, m, q, s = len(parent_tiles), len(child_tiles), len(G), len(B)
    rp, rc = 4 * p, 4 * m
    child = _child_problem(parent, children, lineage)
    E = _restrictions(parent_tiles, child_tiles, lineage)
    Pp, Pc = _moment_blocks(V, parent_tiles), _moment_blocks(V, child_tiles)
    aggregate_P = _aggregate_blocks(Pc, E, lineage, p)
    residual_P = [_difference(a, b) for a, b in zip(aggregate_P, Pp)]
    for block in residual_P:
        _zero_matrix(block, "independent parent/child raw moment blocks")
    _wire(E)
    _wire(Pp)
    _wire(Pc)
    levels = {
        "parent": _level(parent, V, sigma, defined, undefined),
        "child": _level(child, V, sigma, defined, undefined),
    }
    pk, ck = levels["parent"]["kernels"], levels["child"]["kernels"]
    parent_corners = [[_values(tile) for tile in row] for row in pk["corner_values"]]
    child_corners = [[_values(tile) for tile in row] for row in ck["corner_values"]]
    for i in range(q):
        for j, owner in enumerate(lineage):
            _need(
                child_corners[i][j] == _matvec(E[j], parent_corners[i][owner]),
                "independent physical kernel restriction",
            )
            _need(
                child["geometric"][i][4 * j : 4 * j + 4]
                == parent["geometric"][i][4 * owner : 4 * owner + 4],
                "same global kernel coefficients",
            )
    parent_integrals, child_integrals = _matrix(pk["tile_integrals"]), _matrix(ck["tile_integrals"])
    aggregate_integrals = [[ZERO] * p for _ in range(q)]
    for i, row in enumerate(child_integrals):
        for value, owner in zip(row, lineage):
            aggregate_integrals[i][owner] += value
    kernel_residual = _difference(aggregate_integrals, parent_integrals)
    _zero_matrix(kernel_residual, "kernel integral additivity")
    aggregate_bernstein = _restrict_rows(_matrix(ck["bernstein_integrals"]), E, lineage, p)
    bernstein_residual = _difference(aggregate_bernstein, _matrix(pk["bernstein_integrals"]))
    _zero_matrix(bernstein_residual, "independent Bernstein transport")
    restricted_raw = _restrict_rows(
        _matrix(levels["child"]["maps"]["raw_bilinear_target"]), E, lineage, p
    )
    raw_residual = _difference(
        restricted_raw, _matrix(levels["parent"]["maps"]["raw_bilinear_target"])
    )
    _zero_matrix(raw_residual, "independent raw response transport")
    restricted_normalized = _restrict_rows(
        _nullable_matrix(levels["child"]["maps"]["normalized_bilinear_target"]), E, lineage, p
    )
    normalized_residual = _nullable_residual(
        restricted_normalized,
        _nullable_matrix(levels["parent"]["maps"]["normalized_bilinear_target"]),
    )
    for row in normalized_residual:
        _need(row is None or not any(row), "normalized response transport")
    pb, cb = levels["parent"]["bounds"], levels["child"]["bounds"]
    comparisons = {}
    for name, level_big, level_small, key in (
        ("constant_increase", cb, pb, "constant_lower"),
        ("bilinear_increase", cb, pb, "bilinear_lower"),
        ("upper_decrease", pb, cb, "corner_upper"),
    ):
        comparisons[name] = _comparison(
            _nullable_values(level_big[key]), _nullable_values(level_small[key])
        )
    pc, cc = levels["parent"]["certification"], levels["child"]["certification"]
    inherited = list(pc["certified_rows"])
    _need(set(inherited) <= set(cc["certified_rows"]), "certification cannot be lost")
    newly = [i for i in cc["certified_rows"] if i not in inherited]
    still = list(cc["uncertified_rows"])
    _need(
        sorted(inherited + newly + still + undefined) == list(range(q)),
        "certification bridge partition",
    )
    inherited_residual = [None] * q
    for i in inherited:
        inherited_residual[i] = _fraction(cb["certified_gain"][i]) - _fraction(
            pb["certified_gain"][i]
        )
        _need(inherited_residual[i] == ZERO, "same exact bounded-field functional gain")

    def pair(corners):
        return _pipeline_pair(
            parent, child, corners, E, lineage, V, sigma, levels, defined, undefined
        )

    def child_pipeline(corners):
        return _pipeline(child, corners, V, sigma, levels["child"], defined, undefined)

    witnesses = {}
    for name, values in (
        ("parent_pattern", [F for _ in range(p) for F in (-ONE, ZERO, ONE, ONE / 2)]),
        ("parent_constant", [ONE] * rp),
    ):
        witnesses[name] = {"positive": pair(values), "negative": pair([-x for x in values])}
    for name, level, tile_count, is_parent, gain_key in (
        ("parent_constant_maximizer", levels["parent"], p, True, "constant_lower"),
        ("parent_bilinear_maximizer", levels["parent"], p, True, "bilinear_lower"),
        ("child_constant_maximizer", levels["child"], m, False, "constant_lower"),
        ("child_bilinear_maximizer", levels["child"], m, False, "bilinear_lower"),
    ):
        if not defined:
            witnesses[name] = None
            continue
        maximum = level["bounds"]["maxima"][gain_key]
        target = maximum["rows"][0]
        _need(target in defined and len(maximum["rows"]) > 0, "first defined maximizing target")
        if gain_key == "constant_lower":
            signs = [_sign(x) for x in _values(level["kernels"]["tile_integrals"][target])]
            values = [ONE * x for x in signs for _ in range(4)]
            _need(len(signs) == tile_count, "constant sign inventory")
        else:
            signs = [_sign(x) for x in _values(level["maps"]["normalized_bilinear_target"][target])]
            values = [ONE * x for x in signs]
            _need(len(signs) == 4 * tile_count, "bilinear sign inventory")
        output = []
        for direction in (ONE, -ONE):
            endpoint = (
                pair([direction * x for x in values])
                if is_parent
                else child_pipeline([direction * x for x in values])
            )
            actual = endpoint["parent"] if is_parent else endpoint
            _need(
                actual["normalized_error"][target] == direction * _fraction(maximum["gain"]),
                "actual designated maximum lower attainment",
            )
            output.append(endpoint)
        witnesses[name] = {
            "target_row": target,
            "signs": signs,
            "positive": output[0],
            "negative": output[1],
        }
    for side, direction in (("positive", ONE), ("negative", -ONE)):
        for level in ("parent", "child"):
            actual = witnesses["parent_constant"][side][level]
            _need(
                all(x == direction * V * V for x in actual["tile_minima"] + actual["tile_maxima"]),
                "constant physical field preserved",
            )
    d, zp, zc = len(defined), len(pc["certified_rows"]), len(cc["certified_rows"])
    n, a = len(cells), sum(tile is not None for tile in cells)
    paired, child_witnesses = (8, 4) if d else (4, 0)
    Ep, Ec = 3 * rp + s + 2 * q + d + 2 * p, 3 * rc + s + 2 * q + d + 2 * m
    Epair = Ep + Ec + 2 * rp + s + 2 * q + d + rc
    return _wire(
        {
            "input": deepcopy(supplied),
            "child_problem": child,
            "geometry": {
                "volume": V,
                "cell_volumes": cell_volumes,
                "target_scales": sigma,
                "defined_rows": defined,
                "undefined_rows": undefined,
                "parent_tile_volumes": parent_volumes,
                "child_tile_volumes": child_volumes,
                "child_parents": lineage,
            },
            "restriction": {
                "blocks": E,
                "parent_moment_blocks": Pp,
                "child_moment_blocks": Pc,
                "aggregated_moment_blocks": aggregate_P,
                "moment_residuals": residual_P,
                "row_sums": [[sum(row, ZERO) for row in block] for block in E],
                "min_weights": [min(x for row in block for x in row) for block in E],
                "max_weights": [max(x for row in block for x in row) for block in E],
            },
            "levels": levels,
            "transport": {
                "aggregate_kernel_integrals": aggregate_integrals,
                "aggregate_bernstein_integrals": aggregate_bernstein,
                "kernel_integral_residuals": kernel_residual,
                "bernstein_residuals": bernstein_residual,
                "restricted_raw_target": restricted_raw,
                "raw_target_residuals": raw_residual,
                "restricted_normalized_target": restricted_normalized,
                "normalized_target_residuals": normalized_residual,
            },
            "comparison": comparisons,
            "certification_bridge": {
                "inherited_rows": inherited,
                "newly_certified_rows": newly,
                "still_uncertified_rows": still,
                "undefined_rows": undefined,
                "inherited_gain_residuals": inherited_residual,
            },
            "witnesses": witnesses,
            "checks": dict.fromkeys(
                (
                    "parent_geometry",
                    "child_partition",
                    "lineage_identity",
                    "frozen_bank_identity",
                    "restriction_convexity",
                    "raw_moment_additivity",
                    "kernel_restriction",
                    "kernel_integral_additivity",
                    "bernstein_transport",
                    "response_transport",
                    "normalization_domain",
                    "bound_monotonicity",
                    "certification_inheritance",
                    "parent_field_pipelines",
                    "child_extremizer_pipelines",
                    "constant_controls",
                    "complete_comparisons",
                ),
                True,
            ),
            "counts": {
                "cells": n,
                "positive_cells": a,
                "parent_tiles": p,
                "child_tiles": m,
                "parent_bank_values": rp,
                "child_bank_values": rc,
                "receiver_values": s,
                "target_rows": q,
                "defined_rows": d,
                "undefined_rows": q - d,
                "input_geometry_entries": 4 + 4 * a + 4 * p + 4 * m,
                "input_matrix_entries": s * rp + q * rp + q * s,
                "child_problem_geometry_entries": 4 + 4 * a + 4 * m,
                "child_problem_matrix_entries": s * rc + q * rc + q * s,
                "geometry_entries": 1 + n + q + p + m,
                "restriction_entries": 38 * m + 48 * p,
                "parent_kernel_entries": 12 * q * p,
                "child_kernel_entries": 12 * q * m,
                "parent_map_entries": (3 * q + d) * rp,
                "child_map_entries": (3 * q + d) * rc,
                "bound_entries": 6 * d
                + zp
                + zc
                + 2 * (3 if d else 0)
                + (1 if zp else 0)
                + (1 if zc else 0),
                "certification_bridge_entries": zp,
                "transport_entries": 2 * q * p + 4 * q * rp + 2 * d * rp,
                "comparison_entries": 3 * d + (3 if d else 0),
                "parent_paired_witnesses": paired,
                "child_witnesses": child_witnesses,
                "sign_entries": p + rp + m + rc if d else 0,
                "witness_entries": paired * Epair + child_witnesses * Ec,
                "constant_strict": len(comparisons["constant_increase"]["strict_rows"]),
                "bilinear_strict": len(comparisons["bilinear_increase"]["strict_rows"]),
                "upper_strict": len(comparisons["upper_decrease"]["strict_rows"]),
                "inherited_rows": len(inherited),
                "newly_certified_rows": len(newly),
                "still_uncertified_rows": len(still),
            },
        }
    )
