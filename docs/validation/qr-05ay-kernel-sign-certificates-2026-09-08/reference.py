"""QR-05AY independent reference: physical kernel interpolation and integrals.

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


def _parse(problem):
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
    # Complete shape/label inventories precede Fractions; every value precedes geometry.
    probe = [_fraction(x) for x in probe]
    cell_bounds = [
        None if cell["bounds"] is None else [_fraction(x) for x in cell["bounds"]] for cell in cells
    ]
    tile_bounds = [[_fraction(x) for x in tile["bounds"]] for tile in tiles]
    B, G, D = (_matrix(matrix) for matrix in (B, G, D))
    return probe, ids, cell_bounds, tile_bounds, [tile["event"] for tile in tiles], pairs, B, G, D


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


def _endpoint(problem, corners, V, sigma, A, L, U, defined, undefined):
    _need(all(-ONE <= z <= ONE for z in corners), "bounded field corners")
    raw = integrate(problem["probe"], [t["bounds"] for t in problem["tiles"]], _wire(corners))
    fields = {key: _values(value) for key, value in raw.items()}
    bank = fields["raw_moments"]
    observed_wire = produce(problem["interface"], raw["raw_moments"])
    observed = _values(observed_wire)
    direct = _values(produce(problem["geometric"], raw["raw_moments"]))
    decoded = _values(apply(problem["decoder"], observed_wire))
    normalized = [z / scale if scale else None for z, scale in zip(decoded, sigma)]
    _need(
        direct == decoded
        and all(normalized[i] == _dot(A[i], corners) for i in defined)
        and all(normalized[i] is None for i in undefined),
        "complete actual endpoint response",
    )
    _need(
        all(-L[i] <= normalized[i] <= L[i] and -U[i] <= normalized[i] <= U[i] for i in defined),
        "complete lower-class and envelope bounds",
    )
    _need(
        all(-V * V <= lo <= hi <= V * V for lo, hi in zip(fields["minima"], fields["maxima"])),
        "complete field extrema",
    )
    return {
        "corners": corners,
        "local_coefficients": fields["local_coefficients"],
        "global_coefficients": fields["global_coefficients"],
        "local_moments": fields["local_moments"],
        "bank_error": bank,
        "tile_minima": fields["minima"],
        "tile_maxima": fields["maxima"],
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
    }


def build_family(problem):
    probe, ids, cells, tiles, owners, pairs, B, G, _D = _parse(problem)
    V, cell_volumes, tile_volumes, sigma, defined, undefined = _geometry(
        probe,
        ids,
        cells,
        tiles,
        owners,
        pairs,
    )
    for i in undefined:
        _need(not any(G[i]), "undefined target raw kernel must be zero")
    K, Rbank = _bank_probe(problem, G)
    kernel_wire = inspect_kernel(
        problem["probe"], [t["bounds"] for t in problem["tiles"]], problem["geometric"]
    )
    corners = [[_values(t) for t in row] for row in kernel_wire["corner_values"]]
    integrals = _matrix(kernel_wire["tile_integrals"])
    bernstein = _matrix(kernel_wire["bernstein_integrals"])
    upper = _matrix(kernel_wire["tile_abs_upper"])
    classes = kernel_wire["tile_classes"]
    q, r, s, t = len(G), len(G[0]), len(B), len(tiles)
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
    tile_witnesses, bilinear_witnesses = [None] * q, [None] * q

    def endpoint(c):
        return _endpoint(problem, c, V, sigma, A, L, U, defined, undefined)

    for target in defined:
        tile_signs = [_sign(value) for value in integrals[target]]
        field_signs = [_sign(value) for value in A[target]]
        for signs, primitive, gain, destination in (
            (
                tile_signs,
                [value for value in tile_signs for _ in range(4)],
                C[target],
                tile_witnesses,
            ),
            (field_signs, field_signs, L[target], bilinear_witnesses),
        ):
            ends = []
            for direction in (ONE, -ONE):
                e = endpoint([direction * z for z in primitive])
                e["attained"] = e["normalized_error"][target]
                _need(e["attained"] == direction * gain, "actual lower signed attainment")
                ends.append(e)
            destination[target] = {
                "target_row": target,
                "signs": signs,
                "positive": ends[0],
                "negative": ends[1],
            }
    positive, negative = endpoint([ONE] * r), endpoint([-ONE] * r)
    _need(
        all(
            positive["normalized_error"][i] == sum(A[i], ZERO)
            and negative["normalized_error"][i] == -sum(A[i], ZERO)
            for i in defined
        ),
        "actual constant responses",
    )
    _need(
        all(z == V * V for z in positive["tile_minima"] + positive["tile_maxima"])
        and all(z == -V * V for z in negative["tile_minima"] + negative["tile_maxima"]),
        "actual global constant extrema",
    )
    bounds = {"constant_lower": C, "bilinear_lower": L, "corner_upper": U, "certified_gain": exact}
    maxima = {key: _maximum(values) for key, values in bounds.items()}
    comparisons = {
        "bilinear_minus_constant": _comparison(L, C),
        "upper_minus_bilinear": _comparison(U, L),
        "upper_minus_certified": _comparison(U, exact),
    }
    d, z, c, a = len(defined), len(certified), len(cells), sum(x is not None for x in cells)
    integrated_mixed = [i for i in uncertified if i in integrated_nonneg]
    return _wire(
        {
            "problem": deepcopy(problem),
            "geometry": {
                "volume": V,
                "cell_volumes": cell_volumes,
                "tile_volumes": tile_volumes,
                "target_scales": sigma,
                "defined_rows": defined,
                "undefined_rows": undefined,
            },
            "kernels": kernel_wire,
            "maps": {
                "decoder_bank": K,
                "bank_residual": Rbank,
                "raw_bilinear_target": J,
                "normalized_bilinear_target": A,
            },
            "bounds": {**bounds, "maxima": maxima},
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
            "witnesses": {
                "tile_constant": tile_witnesses,
                "bilinear": bilinear_witnesses,
                "constant_positive": positive,
                "constant_negative": negative,
            },
            "comparison": comparisons,
            "checks": dict.fromkeys(
                (
                    "geometry_partitions",
                    "bank_label_identity",
                    "frozen_bank_identity",
                    "kernel_corner_identity",
                    "kernel_integrals",
                    "bernstein_integrals",
                    "corner_envelope",
                    "normalization_domain",
                    "bound_order",
                    "sign_partition",
                    "obstruction_inventory",
                    "certified_exactness",
                    "endpoint_field_bound",
                    "endpoint_pipeline",
                    "lower_attainment",
                    "constant_controls",
                    "complete_comparisons",
                ),
                True,
            ),
            "counts": {
                "cells": c,
                "positive_cells": a,
                "tiles": t,
                "bank_values": r,
                "receiver_values": s,
                "target_rows": q,
                "defined_rows": d,
                "undefined_rows": q - d,
                "geometry_input_entries": 4 + 4 * a + 4 * t,
                "input_matrix_entries": s * r + q * r + q * s,
                "geometry_entries": 1 + c + t + q,
                "kernel_entries": 12 * q * t,
                "map_entries": (3 * q + d) * r,
                "bound_entries": 3 * d + z + (3 if d else 0) + (1 if z else 0),
                "comparison_entries": 2 * d + z + (2 if d else 0) + (1 if z else 0),
                "mixed_tiles": sum(len(row) for row in obstructions),
                "mixed_rows": len(uncertified),
                "certified_rows": z,
                "pointwise_nonnegative_rows": len(point_nonneg),
                "pointwise_nonpositive_rows": len(point_nonpos),
                "pointwise_zero_rows": len(point_zero),
                "integrated_nonnegative_rows": len(integrated_nonneg),
                "integrated_nonpositive_rows": len(integrated_nonpos),
                "integrated_zero_rows": len(integrated_zero),
                "integrated_nonnegative_mixed_rows": len(integrated_mixed),
                "tile_constant_witnesses": 2 * d,
                "bilinear_witnesses": 2 * d,
                "constant_witnesses": 2,
                "tile_sign_entries": d * t,
                "bilinear_sign_entries": d * r,
                "endpoint_entries": 4 * d * (5 * r + 2 * t + s + 2 * q + d + 1),
                "constant_endpoint_entries": 2 * (5 * r + 2 * t + s + 2 * q + d),
                "constant_gap_strict": len(comparisons["bilinear_minus_constant"]["strict_rows"]),
                "upper_gap_strict": len(comparisons["upper_minus_bilinear"]["strict_rows"]),
                "certified_upper_gap_strict": len(
                    comparisons["upper_minus_certified"]["strict_rows"]
                ),
                "constant_maximizers": len(maxima["constant_lower"]["rows"]),
                "bilinear_maximizers": len(maxima["bilinear_lower"]["rows"]),
                "upper_maximizers": len(maxima["corner_upper"]["rows"]),
                "certified_maximizers": len(maxima["certified_gain"]["rows"]),
            },
        }
    )
