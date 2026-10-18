"""QR-05BA independent reference: field and acquisition product domains.

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


def _parse_parent(problem, children, radii, budgets):
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
    _need(type(radii) is list and len(radii) == s, "receiver radius inventory")
    _pair_shapes(radii)
    _need(type(budgets) is list and 1 <= len(budgets) <= 8, "budget inventory")
    names = []
    for budget in budgets:
        _keys(budget, ("name", "field", "acquisition"))
        _need(type(budget["name"]) is str and bool(budget["name"]), "budget name")
        names.append(budget["name"])
        _pair_shapes([budget["field"], budget["acquisition"]])
    _need(len(set(names)) == len(names), "unique budget names")
    # ALL refinement/radius/budget shapes precede ALL Fractions.
    # ALL scalar values, including the last budget, precede geometry.
    probe = [_fraction(x) for x in probe]
    cell_bounds = [
        None if cell["bounds"] is None else [_fraction(x) for x in cell["bounds"]] for cell in cells
    ]
    tile_bounds = [[_fraction(x) for x in tile["bounds"]] for tile in tiles]
    B, G, D = (_matrix(matrix) for matrix in (B, G, D))
    child_bounds = [[_fraction(x) for x in child["bounds"]] for child in children]
    rho = [_fraction(x) for x in radii]
    budget_values = [(_fraction(b["field"]), _fraction(b["acquisition"])) for b in budgets]
    _need(all(x >= ZERO for x in rho), "nonnegative receiver radii")
    _need(all(e >= ZERO and a >= ZERO for e, a in budget_values), "nonnegative budgets")
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
        rho,
        budget_values,
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


def _difference(left, right):
    return [[a - b for a, b in zip(x, y)] for x, y in zip(left, right)]


def _zero_matrix(matrix, message):
    _need(not any(x for row in matrix for x in row), message)


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


def _field(parent, children, parsed):
    (
        probe,
        ids,
        cells,
        parent_tiles,
        owners,
        pairs,
        _B,
        G,
        _D,
        lineage,
        child_tiles,
        _rho,
        _budgets,
    ) = parsed
    V, cell_volumes, parent_volumes, sigma, defined, undefined = _geometry(
        probe, ids, cells, parent_tiles, owners, pairs
    )
    for i in undefined:
        _need(not any(G[i]), "undefined raw target kernel")
    child_volumes = _child_partition(parent_tiles, child_tiles, lineage)
    p, q = len(parent_tiles), len(G)
    child = _child_problem(parent, children, lineage)
    E = _restrictions(parent_tiles, child_tiles, lineage)
    _wire(E)
    levels = {
        "parent": _level(parent, V, sigma, defined, undefined),
        "child": _level(child, V, sigma, defined, undefined),
    }
    pk, ck = (levels[name]["kernels"] for name in ("parent", "child"))
    for i in range(q):
        for j, owner in enumerate(lineage):
            _need(
                _values(ck["corner_values"][i][j])
                == _matvec(E[j], _values(pk["corner_values"][i][owner])),
                "independent physical kernel restriction",
            )
    for key in ("raw_bilinear_target", "normalized_bilinear_target"):
        restricted = _restrict_rows(_nullable_matrix(levels["child"]["maps"][key]), E, lineage, p)
        residual = _nullable_residual(restricted, _nullable_matrix(levels["parent"]["maps"][key]))
        _need(
            all(row is None or not any(row) for row in residual), "independent response transport"
        )
    parent_integrals, child_integrals = _matrix(pk["tile_integrals"]), _matrix(ck["tile_integrals"])
    for i in range(q):
        aggregated = [ZERO] * p
        for value, owner in zip(child_integrals[i], lineage):
            aggregated[owner] += value
        _need(aggregated == parent_integrals[i], "independent kernel integral additivity")
    restricted_bernstein = _restrict_rows(_matrix(ck["bernstein_integrals"]), E, lineage, p)
    _zero_matrix(
        _difference(restricted_bernstein, _matrix(pk["bernstein_integrals"])),
        "independent Bernstein transport",
    )
    for key, bigger, smaller in (
        ("constant_lower", "child", "parent"),
        ("bilinear_lower", "child", "parent"),
        ("corner_upper", "parent", "child"),
    ):
        _comparison(
            _nullable_values(levels[bigger]["bounds"][key]),
            _nullable_values(levels[smaller]["bounds"][key]),
        )
    inherited = levels["parent"]["certification"]["certified_rows"]
    _need(
        set(inherited) <= set(levels["child"]["certification"]["certified_rows"]),
        "field certificate inheritance",
    )
    for i in inherited:
        _need(
            levels["parent"]["bounds"]["certified_gain"][i]
            == levels["child"]["bounds"]["certified_gain"][i],
            "same sharp field functional",
        )
    for key in ("family", "probe", "cells", "target_labels", "decoder"):
        _need(child[key] == parent[key], "unchanged receiver/target contract")
    for key in ("interface", "geometric"):
        _need(
            child[key]
            == [
                [x for owner in lineage for x in row[4 * owner : 4 * owner + 4]]
                for row in parent[key]
            ],
            "raw global column lineage",
        )
    geometry = {
        "volume": V,
        "cell_volumes": cell_volumes,
        "target_scales": sigma,
        "defined_rows": defined,
        "undefined_rows": undefined,
        "parent_tile_volumes": parent_volumes,
        "child_tile_volumes": child_volumes,
        "child_parents": lineage,
    }
    return (
        _wire(
            {
                "child_problem": child,
                "geometry": geometry,
                "restriction_blocks": E,
                "levels": levels,
            }
        ),
        V,
        sigma,
        defined,
        undefined,
        E,
    )


def _acquisition(parent, rho, sigma):
    """Independent actual receiver-column probes, not a dense D-times-diagonal."""
    q, s = len(parent["decoder"]), len(rho)
    K = [[ZERO] * s for _ in range(q)]
    for j in range(s):
        actual_noise = [ZERO] * s
        actual_noise[j] = rho[j]
        output = _values(apply(parent["decoder"], _wire(actual_noise)))
        for i, value in enumerate(output):
            K[i][j] = value
    H = [None if not sigma[i] else [x / sigma[i] for x in row] for i, row in enumerate(K)]
    gains = [None if row is None else _radius(row) for row in H]
    return _wire({"raw_map": K, "normalized_map": H, "gain": gains, "maxima": _maximum(gains)})


def _case_level(level, epsilon, eta, acquisition, defined, undefined):
    field_bounds = level["bounds"]
    gamma = _nullable_values(acquisition["gain"])
    q = len(gamma)
    bounds = {}
    for key in ("constant_lower", "bilinear_lower", "corner_upper"):
        values = _nullable_values(field_bounds[key])
        bounds[key] = [
            None if i in undefined else epsilon * values[i] + eta * gamma[i] for i in range(q)
        ]
    exact, reasons = [], []
    certified = level["certification"]["certified_rows"]
    for i in range(q):
        if i in undefined:
            exact.append(None)
            reasons.append("undefined")
        elif epsilon == ZERO:
            exact.append(eta * gamma[i])
            reasons.append("zero_field_budget")
        elif i in certified:
            exact.append(epsilon * _fraction(field_bounds["certified_gain"][i]) + eta * gamma[i])
            reasons.append("field_certified")
        else:
            exact.append(None)
            reasons.append("unavailable")
    available = [i for i in defined if exact[i] is not None]
    unavailable = [i for i in defined if exact[i] is None]
    _need(sorted(available + unavailable + undefined) == list(range(q)), "composed exact partition")
    bounds["exact_gain"] = exact
    for i in defined:
        _need(
            ZERO
            <= bounds["constant_lower"][i]
            <= bounds["bilinear_lower"][i]
            <= bounds["corner_upper"][i],
            "composed bound order",
        )
    for i in available:
        _need(
            bounds["constant_lower"][i] == bounds["bilinear_lower"][i] == exact[i],
            "certified composed lower equality",
        )
    return _wire(
        {
            "bounds": {**bounds, "maxima": {key: _maximum(v) for key, v in bounds.items()}},
            "exactness": {
                "reason": reasons,
                "available_rows": available,
                "unavailable_rows": unavailable,
                "undefined_rows": undefined,
            },
        }
    )


def _pipeline(
    problem,
    corners,
    coordinates,
    epsilon,
    eta,
    rho,
    V,
    sigma,
    field_level,
    acquisition,
    case_level,
    defined,
    undefined,
):
    _need(all(abs(x) <= epsilon for x in corners), "field corner budget")
    _need(all(abs(x) <= eta for x in coordinates), "acquisition coordinate budget")
    integrated = integrate(
        problem["probe"], [x["bounds"] for x in problem["tiles"]], _wire(corners)
    )
    bank = integrated["raw_moments"]
    field_observed = produce(problem["interface"], bank)
    field_direct = produce(problem["geometric"], bank)
    acquisition_direct = produce(acquisition["raw_map"], _wire(coordinates))
    noise = [radius * value for radius, value in zip(rho, coordinates)]
    _need(all(abs(x) <= eta * radius for x, radius in zip(noise, rho)), "physical acquisition box")
    acquisition_error = _wire(noise)
    total_observed = _wire([a + b for a, b in zip(_values(field_observed), noise)])
    field_decoded = apply(problem["decoder"], field_observed)
    acquisition_decoded = apply(problem["decoder"], acquisition_error)
    total_decoded = apply(problem["decoder"], total_observed)
    total_direct = _wire(
        [a + b for a, b in zip(_values(field_direct), _values(acquisition_direct))]
    )
    _need(
        field_direct == field_decoded
        and acquisition_direct == acquisition_decoded
        and total_direct == total_decoded,
        "actual component and joint decoder identities",
    )
    _need(
        _values(total_decoded)
        == [a + b for a, b in zip(_values(field_decoded), _values(acquisition_decoded))],
        "actual decoded component additivity",
    )
    raw = _values(total_direct)
    normalized = [None if not scale else raw[i] / scale for i, scale in enumerate(sigma)]
    A = _nullable_matrix(field_level["maps"]["normalized_bilinear_target"])
    H = _nullable_matrix(acquisition["normalized_map"])
    J = _matrix(field_level["maps"]["raw_bilinear_target"])
    _need(
        _matvec(J, corners) == _values(field_direct), "actual field moments vs integrated response"
    )
    for i in defined:
        _need(
            normalized[i] == _dot(A[i], corners) + _dot(H[i], coordinates),
            "actual normalized combined response",
        )
        for key in ("bilinear_lower", "corner_upper"):
            _need(
                abs(normalized[i]) <= _fraction(case_level["bounds"][key][i]),
                "all-target joint field/noise bound",
            )
    _need(all(normalized[i] is None for i in undefined), "raw versus normalized nulls")
    minima, maxima = _values(integrated["minima"]), _values(integrated["maxima"])
    _need(
        all(
            -epsilon * V * V <= low <= high <= epsilon * V * V for low, high in zip(minima, maxima)
        ),
        "actual scaled field extrema",
    )
    return _wire(
        {
            "corners": corners,
            "acquisition_coordinates": coordinates,
            "global_coefficients": integrated["global_coefficients"],
            "bank_error": bank,
            "field_observed_error": field_observed,
            "acquisition_error": acquisition_error,
            "total_observed_error": total_observed,
            "field_direct_error": field_direct,
            "field_decoded_error": field_decoded,
            "acquisition_direct_error": acquisition_direct,
            "acquisition_decoded_error": acquisition_decoded,
            "total_direct_error": total_direct,
            "total_decoded_error": total_decoded,
            "normalized_error": normalized,
            "tile_minima": minima,
            "tile_maxima": maxima,
        }
    )


def _pipeline_pair(
    parent,
    child,
    corners,
    coordinates,
    E,
    lineage,
    epsilon,
    eta,
    rho,
    V,
    sigma,
    field_levels,
    acquisition,
    case_levels,
    defined,
    undefined,
):
    pp = _pipeline(
        parent,
        corners,
        coordinates,
        epsilon,
        eta,
        rho,
        V,
        sigma,
        field_levels["parent"],
        acquisition,
        case_levels["parent"],
        defined,
        undefined,
    )
    cp = _pipeline(
        child,
        _restrict_corners(corners, E, lineage),
        coordinates,
        epsilon,
        eta,
        rho,
        V,
        sigma,
        field_levels["child"],
        acquisition,
        case_levels["child"],
        defined,
        undefined,
    )
    p = len(parent["tiles"])
    aggregate = _sum_raw(_values(cp["bank_error"]), lineage, p)
    bank_residual = [x - y for x, y in zip(aggregate, _values(pp["bank_error"]))]
    _need(not any(bank_residual), "actual global raw moment additivity")
    _need(
        pp["acquisition_coordinates"] == cp["acquisition_coordinates"]
        and pp["acquisition_error"] == cp["acquisition_error"],
        "same acquisition realization",
    )
    out = {
        "parent": pp,
        "child": cp,
        "aggregated_bank_error": aggregate,
        "bank_residual": bank_residual,
    }
    for source, target in (
        ("field_observed_error", "field_observed_residual"),
        ("acquisition_error", "acquisition_residual"),
        ("total_observed_error", "total_observed_residual"),
        ("field_direct_error", "field_direct_residual"),
        ("field_decoded_error", "field_decoded_residual"),
        ("acquisition_direct_error", "acquisition_direct_residual"),
        ("acquisition_decoded_error", "acquisition_decoded_residual"),
        ("total_direct_error", "total_direct_residual"),
        ("total_decoded_error", "total_decoded_residual"),
    ):
        residual = [x - y for x, y in zip(_values(cp[source]), _values(pp[source]))]
        _need(not any(residual), "same field/noise pipeline under refinement")
        out[target] = residual
    pn, cn = _nullable_values(pp["normalized_error"]), _nullable_values(cp["normalized_error"])
    normalized = [None if x is None else x - y for x, y in zip(cn, pn)]
    _need(all(x is None or x == ZERO for x in normalized), "same normalized joint response")
    out["normalized_residual"] = normalized
    parent_coefficients = _values(pp["global_coefficients"])
    duplicate = [x for owner in lineage for x in parent_coefficients[4 * owner : 4 * owner + 4]]
    coefficient_residual = [x - y for x, y in zip(_values(cp["global_coefficients"]), duplicate)]
    _need(not any(coefficient_residual), "same actual physical field polynomial")
    out["field_coefficient_residual"] = coefficient_residual
    return _wire(out)


def _case(
    parent,
    child,
    budget,
    epsilon,
    eta,
    rho,
    V,
    sigma,
    field_levels,
    acquisition,
    E,
    lineage,
    defined,
    undefined,
):
    levels = {
        name: _case_level(field_levels[name], epsilon, eta, acquisition, defined, undefined)
        for name in ("parent", "child")
    }
    comparisons = {}
    for name, key, bigger, smaller in (
        ("constant_increase", "constant_lower", "child", "parent"),
        ("bilinear_increase", "bilinear_lower", "child", "parent"),
        ("upper_decrease", "corner_upper", "parent", "child"),
    ):
        value = _comparison(
            _nullable_values(levels[bigger]["bounds"][key]),
            _nullable_values(levels[smaller]["bounds"][key]),
        )
        field_gap = _comparison(
            _nullable_values(field_levels[bigger]["bounds"][key]),
            _nullable_values(field_levels[smaller]["bounds"][key]),
        )
        _need(
            _nullable_values(_wire(value["gain_gap"]))
            == [None if x is None else epsilon * x for x in field_gap["gain_gap"]],
            "acquisition cancels in refinement gaps",
        )
        comparisons[name] = value
    inherited = levels["parent"]["exactness"]["available_rows"]
    child_available = levels["child"]["exactness"]["available_rows"]
    _need(set(inherited) <= set(child_available), "composed exact availability cannot be lost")
    newly = [i for i in child_available if i not in inherited]
    unavailable = levels["child"]["exactness"]["unavailable_rows"]
    _need(
        sorted(inherited + newly + unavailable + undefined) == list(range(len(sigma))),
        "complete exact bridge",
    )
    residuals = [None] * len(sigma)
    for i in inherited:
        residuals[i] = _fraction(levels["child"]["bounds"]["exact_gain"][i]) - _fraction(
            levels["parent"]["bounds"]["exact_gain"][i]
        )
        _need(residuals[i] == ZERO, "same inherited exact product-domain gain")
    bridge = {
        "inherited_rows": inherited,
        "newly_exact_rows": newly,
        "unavailable_rows": unavailable,
        "undefined_rows": undefined,
        "inherited_gain_residuals": residuals,
    }

    def pair(c, z):
        return _pipeline_pair(
            parent,
            child,
            c,
            z,
            E,
            lineage,
            epsilon,
            eta,
            rho,
            V,
            sigma,
            field_levels,
            acquisition,
            levels,
            defined,
            undefined,
        )

    def child_pipeline(c, z):
        return _pipeline(
            child,
            c,
            z,
            epsilon,
            eta,
            rho,
            V,
            sigma,
            field_levels["child"],
            acquisition,
            levels["child"],
            defined,
            undefined,
        )

    p, m, s = len(parent["tiles"]), len(child["tiles"]), len(rho)
    witnesses = {}
    pattern = (-ONE, ZERO, ONE, ONE / 2)
    for name, corners, coordinates in (
        (
            "parent_pattern",
            [epsilon * x for _ in range(p) for x in pattern],
            [eta * pattern[j % 4] for j in range(s)],
        ),
        ("parent_constant", [epsilon] * (4 * p), [eta] * s),
    ):
        witnesses[name] = {
            "positive": pair(corners, coordinates),
            "negative": pair([-x for x in corners], [-x for x in coordinates]),
        }
    K = _matrix(acquisition["raw_map"])
    for level_name, tiles, is_parent in (("parent", p, True), ("child", m, False)):
        for kind, key in (
            ("constant", "constant_lower"),
            ("bilinear", "bilinear_lower"),
            ("exact", "exact_gain"),
        ):
            name = level_name + "_" + kind + "_maximizer"
            maximum = levels[level_name]["bounds"]["maxima"][key]
            if maximum["gain"] is None:
                witnesses[name] = None
                continue
            i = maximum["rows"][0]
            if kind == "bilinear":
                source = _values(field_levels[level_name]["maps"]["normalized_bilinear_target"][i])
            else:
                source = _values(field_levels[level_name]["kernels"]["tile_integrals"][i])
            field_signs = [_sign(x) if epsilon else 0 for x in source]
            acquisition_signs = [_sign(x) if eta else 0 for x in K[i]]
            if kind == "exact" and epsilon:
                _need(
                    i in field_levels[level_name]["certification"]["certified_rows"],
                    "actual exact field witness is certified",
                )
            corners = [
                epsilon * x for x in field_signs for _ in range(1 if kind == "bilinear" else 4)
            ]
            coordinates = [eta * x for x in acquisition_signs]
            endpoint = pair if is_parent else child_pipeline
            positive, negative = (
                endpoint(corners, coordinates),
                endpoint([-x for x in corners], [-x for x in coordinates]),
            )
            ep, en = (positive["parent"], negative["parent"]) if is_parent else (positive, negative)
            gain = _fraction(maximum["gain"])
            _need(
                _fraction(ep["normalized_error"][i]) == gain
                and _fraction(en["normalized_error"][i]) == -gain,
                "actual signed joint attainment",
            )
            witnesses[name] = {
                "target_row": i,
                "field_signs": field_signs,
                "acquisition_signs": acquisition_signs,
                "positive": positive,
                "negative": negative,
            }
    return _wire(
        {
            "budget": deepcopy(budget),
            "levels": levels,
            "comparison": comparisons,
            "exact_bridge": bridge,
            "witnesses": witnesses,
        }
    )


def _counts(parent, child, cells, field, cases, defined, undefined):
    n, a = len(cells), sum(x is not None for x in cells)
    p, m = len(parent["tiles"]), len(child["tiles"])
    rp, rc, s, q, d, b = (
        4 * p,
        4 * m,
        len(parent["interface"]),
        len(parent["geometric"]),
        len(defined),
        len(cases),
    )
    zf = [
        len(field["levels"][name]["certification"]["certified_rows"])
        for name in ("parent", "child")
    ]
    exacts = [
        [len(case["levels"][name]["exactness"]["available_rows"]) for name in ("parent", "child")]
        for case in cases
    ]
    pairs = [4 + 4 * bool(d) + 2 * bool(zp) for zp, _zc in exacts]
    child_pipelines = [4 * bool(d) + 2 * bool(zc) for _zp, zc in exacts]
    ep, ec = 3 * rp + 4 * s + 6 * q + d + 2 * p, 3 * rc + 4 * s + 6 * q + d + 2 * m
    e_pair = ep + ec + 2 * rp + 3 * s + 6 * q + d + rc
    return {
        "cells": n,
        "positive_cells": a,
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": len(undefined),
        "budgets": b,
        "input_geometry_entries": 4 + 4 * a + 4 * p + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "input_budget_entries": s + 2 * b,
        "geometry_entries": 1 + n + q + p + m,
        "restriction_entries": 16 * m,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "field_bound_entries": sum(3 * d + z + 3 * bool(d) + bool(z) for z in zf),
        "acquisition_entries": q * s + d * s + d + bool(d),
        "case_bound_entries": sum(
            3 * d + z + 3 * bool(d) + bool(z) for pair in exacts for z in pair
        ),
        "case_exact_bridge_entries": sum(pair[0] for pair in exacts),
        "case_comparison_entries": b * (3 * d + 3 * bool(d)),
        "parent_paired_witnesses": sum(pairs),
        "child_witnesses": sum(child_pipelines),
        "sign_entries": sum(
            bool(d) * (p + rp + m + rc + 4 * s) + bool(zp) * (p + s) + bool(zc) * (m + s)
            for zp, zc in exacts
        ),
        "witness_entries": sum(pk * e_pair + ck * ec for pk, ck in zip(pairs, child_pipelines)),
        "constant_strict": sum(
            len(c["comparison"]["constant_increase"]["strict_rows"]) for c in cases
        ),
        "bilinear_strict": sum(
            len(c["comparison"]["bilinear_increase"]["strict_rows"]) for c in cases
        ),
        "upper_strict": sum(len(c["comparison"]["upper_decrease"]["strict_rows"]) for c in cases),
        "inherited_exact_rows": sum(len(c["exact_bridge"]["inherited_rows"]) for c in cases),
        "newly_exact_rows": sum(len(c["exact_bridge"]["newly_exact_rows"]) for c in cases),
        "unavailable_exact_rows": sum(len(c["exact_bridge"]["unavailable_rows"]) for c in cases),
    }


def build_family(supplied):
    _native(supplied)
    _keys(supplied, ("refinement", "receiver_radii", "budgets"))
    _keys(supplied["refinement"], ("parent", "children"))
    parent, children = (supplied["refinement"][key] for key in ("parent", "children"))
    parsed = _parse_parent(parent, children, supplied["receiver_radii"], supplied["budgets"])
    rho, budgets = parsed[-2:]
    field, V, sigma, defined, undefined, E = _field(parent, children, parsed)
    child, lineage = field["child_problem"], parsed[9]
    acquisition = _acquisition(parent, rho, sigma)
    cases = [
        _case(
            parent,
            child,
            budget,
            epsilon,
            eta,
            rho,
            V,
            sigma,
            field["levels"],
            acquisition,
            E,
            lineage,
            defined,
            undefined,
        )
        for budget, (epsilon, eta) in zip(supplied["budgets"], budgets)
    ]
    _need(
        len(cases) == len(supplied["budgets"])
        and [c["budget"] for c in cases] == supplied["budgets"],
        "complete ordered budget cases",
    )
    checks = dict.fromkeys(
        (
            "parent_geometry",
            "child_partition",
            "lineage_identity",
            "full_bank_identity",
            "same_receiver_contract",
            "restriction_convexity",
            "field_level_evidence",
            "response_transport",
            "acquisition_map",
            "normalization_domain",
            "composed_bounds",
            "exact_availability",
            "refinement_comparison",
            "paired_field_noise_pipelines",
            "joint_maximum_attainment",
            "complete_inventory",
        ),
        True,
    )
    return _wire(
        {
            "input": deepcopy(supplied),
            "field": field,
            "acquisition": acquisition,
            "cases": cases,
            "checks": checks,
            "counts": _counts(parent, child, parsed[2], field, cases, defined, undefined),
        }
    )
