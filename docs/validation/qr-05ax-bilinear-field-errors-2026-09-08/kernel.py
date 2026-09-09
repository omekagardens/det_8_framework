"""Exact signed bilinear field-error realization and response certificates."""

import json
from fractions import Fraction as F
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "integer exceeds retained component bound")
    elif value is None or kind in (str, bool):
        return
    elif kind in (list, dict):
        identity = id(value)
        _require(identity not in active, "cyclic native containers are not supported")
        if kind is dict:
            _require(all(type(key) is str for key in value), "native string keys required")
        active.add(identity)
        try:
            for child in value if kind is list else value.values():
                _native(child, active)
        finally:
            active.remove(identity)
    else:
        raise ValueError("exact native mathematical wire required")


def _encode(value):
    if type(value) is F:
        _require(
            max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
            "retained fraction exceeds component bound",
        )
        return [value.numerator, value.denominator]
    if type(value) is list:
        return [_encode(x) for x in value]
    if type(value) is dict:
        return {key: _encode(child) for key, child in value.items()}
    return value


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _detach(value):
    return json.loads(canonical(_encode(value)))


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected fixture fields")


def _fraction(pair):
    _require(type(pair) is list and len(pair) == 2, "native fraction pair required")
    n, d = pair
    _require(
        type(n) is int
        and type(d) is int
        and d > 0
        and max(n.bit_length(), d.bit_length()) <= 4096
        and gcd(n, d) == 1,
        "reduced bounded fraction required",
    )
    return F(n, d)


def _pair_shape(value):
    _require(type(value) is list and len(value) == 2, "native rational-pair shape required")


def _vector_shape(value, width):
    _require(type(value) is list and len(value) == width, "vector width differs")
    for pair in value:
        _pair_shape(pair)


def _matrix_shape(value, rows, columns):
    _require(type(value) is list and len(value) == rows, "matrix row inventory differs")
    for row in value:
        _vector_shape(row, columns)


def _matrix(value):
    return [list(map(_fraction, row)) for row in value]


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F(0))


def _mm(left, right, columns=None):
    if not right:
        _require(columns is not None, "empty product requires its column dimension")
        return [[F(0)] * columns for _ in left]
    transposed = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in transposed] for row in left]


def _raw_product(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _require(type(matrix) is list and len(matrix) <= row_cap, "matrix row cap")
    _require(type(values) is list and len(values) <= width_cap, "raw width cap")
    _matrix_shape(matrix, len(matrix), len(values))
    _vector_shape(values, len(values))
    parsed = _matrix(matrix)
    vector = list(map(_fraction, values))
    return _detach([_dot(row, vector) for row in parsed])


def produce(matrix, values):
    """Evaluate a supplied raw matrix without source or geometry access."""
    return _raw_product(matrix, values, 1024, 1024)


def apply(matrix, observed):
    """Evaluate a supplied zero-intercept receiver."""
    return _raw_product(matrix, observed, 64, 320)


def synthesize(blocks, values):
    """Evaluate supplied four-by-four blocks, forward or inverse."""
    _native(blocks)
    _native(values)
    _require(type(blocks) is list and len(blocks) <= 256, "block inventory cap")
    for block in blocks:
        _matrix_shape(block, 4, 4)
    _vector_shape(values, 4 * len(blocks))
    parsed = [_matrix(block) for block in blocks]
    vector = list(map(_fraction, values))
    answer = []
    for index, block in enumerate(parsed):
        local = vector[4 * index : 4 * index + 4]
        answer.extend(_dot(row, local) for row in block)
    return _detach(answer)


def _rectangle_shape(value, nullable=False):
    if value is None and nullable:
        return
    _vector_shape(value, 4)


def _problem(problem):
    _native(problem)
    _fields(
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
    _require(type(problem["family"]) is str and problem["family"], "family label required")
    _rectangle_shape(problem["probe"])
    cells = problem["cells"]
    tiles = problem["tiles"]
    _require(type(cells) is list and 1 <= len(cells) <= 8, "cell inventory cap")
    _require(type(tiles) is list and 1 <= len(tiles) <= 256, "tile inventory cap")
    ids = []
    for cell in cells:
        _fields(cell, ("event", "bounds"))
        _require(type(cell["event"]) is int, "native cell ID required")
        ids.append(cell["event"])
        _rectangle_shape(cell["bounds"], True)
    _require(ids == sorted(set(ids)), "sorted unique cell IDs required")
    owners = set(ids)
    for tile in tiles:
        _fields(tile, ("event", "bounds"))
        _require(type(tile["event"]) is int and tile["event"] in owners, "unknown tile owner")
        _rectangle_shape(tile["bounds"])
    t = len(tiles)
    r = 4 * t
    labels = problem["bank_labels"]
    _require(type(labels) is list and len(labels) == r, "bank label inventory")
    for index, label in enumerate(labels):
        _fields(label, ("tile", "basis"))
        _require(
            type(label["tile"]) is int
            and type(label["basis"]) is int
            and label["tile"] == index // 4
            and label["basis"] == index % 4,
            "bank labels must follow the supplied tile order",
        )
    targets = problem["target_labels"]
    _require(type(targets) is list and 1 <= len(targets) <= 64, "target inventory cap")
    target_order = []
    for target in targets:
        _fields(target, ("first", "second"))
        _require(
            type(target["first"]) is int
            and type(target["second"]) is int
            and target["first"] in owners
            and target["second"] in owners,
            "target cell IDs required",
        )
        target_order.append((target["first"], target["second"]))
    _require(target_order == sorted(set(target_order)), "sorted unique targets required")
    q = len(targets)
    B = problem["interface"]
    _require(type(B) is list and len(B) <= 320, "receiver inventory cap")
    s = len(B)
    _matrix_shape(B, s, r)
    _matrix_shape(problem["geometric"], q, r)
    _matrix_shape(problem["decoder"], q, s)
    # Complete all structural inventories before constructing any Fraction.
    probe = list(map(_fraction, problem["probe"]))
    parsed_cells = [
        None if cell["bounds"] is None else list(map(_fraction, cell["bounds"])) for cell in cells
    ]
    parsed_tiles = [list(map(_fraction, tile["bounds"])) for tile in tiles]
    B = _matrix(B)
    G = _matrix(problem["geometric"])
    D = _matrix(problem["decoder"])
    # Every supplied scalar has been admitted before geometry or products.
    return probe, parsed_cells, parsed_tiles, B, G, D, target_order, q, r, s, t


def _inside(rectangle, outer):
    return (
        outer[0] <= rectangle[0] < rectangle[1] <= outer[1]
        and outer[2] <= rectangle[2] < rectangle[3] <= outer[3]
    )


def _positive(rectangle):
    return rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3]


def _area(rectangle):
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _overlap(left, right):
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


def _partition(rectangles, outer):
    _require(all(_inside(rectangle, outer) for rectangle in rectangles), "partition containment")
    for i, left in enumerate(rectangles):
        _require(
            all(not _overlap(left, right) for right in rectangles[i + 1 :]),
            "partition interiors overlap",
        )
    _require(
        sum((_area(rectangle) for rectangle in rectangles), F(0)) == _area(outer),
        "partition area differs",
    )


def _geometry(problem, probe, cells, tiles, target_order):
    _require(_positive(probe), "positive probe required")
    _require(
        all(cell is None or _positive(cell) for cell in cells), "positive or null cells required"
    )
    _require(all(_positive(tile) for tile in tiles), "positive bank tiles required")
    _partition([cell for cell in cells if cell is not None], probe)
    ids = [cell["event"] for cell in problem["cells"]]
    owned = {event: [] for event in ids}
    cell_by_id = dict(zip(ids, cells, strict=True))
    for tile, item in zip(tiles, problem["tiles"], strict=True):
        owner = item["event"]
        _require(cell_by_id[owner] is not None, "bank tile has a null owner")
        owned[owner].append(tile)
    for event, cell in cell_by_id.items():
        if cell is not None:
            _partition(owned[event], cell)
    V = _area(probe)
    cell_volumes = [F(0) if cell is None else _area(cell) for cell in cells]
    tile_volumes = list(map(_area, tiles))
    by_id = dict(zip(ids, cell_volumes, strict=True))
    scales = [V * V * by_id[first] * by_id[second] for first, second in target_order]
    defined = [i for i, scale in enumerate(scales) if scale > 0]
    undefined = [i for i, scale in enumerate(scales) if scale == 0]
    return V, cell_volumes, tile_volumes, scales, defined, undefined


def _blocks(tiles, weights):
    forward = []
    inverse = []
    identity = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    for rectangle, weight in zip(tiles, weights, strict=True):
        a, u1, b, v1 = rectangle
        du, dv = u1 - a, v1 - b
        W = [
            [weight * x for x in row]
            for row in [
                [1, 0, 0, 0],
                [a, du, 0, 0],
                [b, 0, dv, 0],
                [a * b, du * b, a * dv, du * dv],
            ]
        ]
        Z = [
            [F(x) / weight for x in row]
            for row in [
                [1, 0, 0, 0],
                [-a / du, 1 / du, 0, 0],
                [-b / dv, 0, 1 / dv, 0],
                [a * b / (du * dv), -b / (du * dv), -a / (du * dv), 1 / (du * dv)],
            ]
        ]
        _require(_mm(W, Z) == identity and _mm(Z, W) == identity, "two-sided block inverse")
        forward.append(W)
        inverse.append(Z)
    return forward, inverse


def _right_blocks(matrix, blocks):
    answer = []
    for row in matrix:
        result = []
        for tile, block in enumerate(blocks):
            local = row[4 * tile : 4 * tile + 4]
            result.extend(_dot(local, column) for column in zip(*block, strict=True))
        answer.append(result)
    return answer


def _subtract(left, right):
    return [[x - y for x, y in zip(a, b, strict=True)] for a, b in zip(left, right, strict=True)]


def _zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def _sign(value):
    return int(value > 0) - int(value < 0)


def _vector(value):
    return list(map(_fraction, value))


def _linear(matrix, values):
    return [_dot(row, values) for row in matrix]


def _normalized(values, scales):
    return [value / scale if scale else None for value, scale in zip(values, scales, strict=True)]


def _maximum(values, defined):
    if not defined:
        return None, []
    maximum = max(values[i] for i in defined)
    return maximum, [i for i in defined if values[i] == maximum]


def _power_integral(lower, upper, power):
    return (upper ** (power + 1) - lower ** (power + 1)) / (power + 1)


def _physical_integral(coefficients, rectangle, test_u, test_v):
    u0, u1, v0, v1 = rectangle
    powers = ((0, 0), (1, 0), (0, 1), (1, 1))
    terms = []
    for coefficient, (i, j) in zip(coefficients, powers, strict=True):
        for p, left in enumerate(test_u):
            for q, right in enumerate(test_v):
                terms.append(
                    coefficient
                    * left
                    * right
                    * _power_integral(u0, u1, i + p)
                    * _power_integral(v0, v1, j + q)
                    / 2
                )
    return sum(terms, F(0))


def integrate(probe, tiles, corners):
    """Integrate the actual signed bilinear field; standalone corners are unbounded."""
    _native(probe)
    _native(tiles)
    _native(corners)
    _rectangle_shape(probe)
    _require(type(tiles) is list and len(tiles) <= 256, "integration tile cap")
    for tile in tiles:
        _rectangle_shape(tile)
    _vector_shape(corners, 4 * len(tiles))
    rectangle = list(map(_fraction, probe))
    boxes = [list(map(_fraction, tile)) for tile in tiles]
    values = list(map(_fraction, corners))
    _require(_positive(rectangle), "positive integration probe")
    _require(all(_inside(box, rectangle) for box in boxes), "integration tile containment")
    for i, box in enumerate(boxes):
        _require(
            all(not _overlap(box, other) for other in boxes[i + 1 :]),
            "integration tiles overlap",
        )
    V = _area(rectangle)
    amplitude = V * V
    local_coefficients, global_coefficients = [], []
    local_moments, raw_moments, minima, maxima = [], [], [], []
    for t, box in enumerate(boxes):
        c00, c10, c01, c11 = values[4 * t : 4 * t + 4]
        local = [amplitude * c for c in [c00, c10 - c00, c01 - c00, c00 - c10 - c01 + c11]]
        a, u1, b, v1 = box
        du, dv = u1 - a, v1 - b
        g = [
            local[0] - a * local[1] / du - b * local[2] / dv + a * b * local[3] / (du * dv),
            local[1] / du - b * local[3] / (du * dv),
            local[2] / dv - a * local[3] / (du * dv),
            local[3] / (du * dv),
        ]
        local_coefficients.extend(local)
        global_coefficients.extend(g)
        weight = amplitude * _area(box)
        for pu, pv in ((0, 0), (1, 0), (0, 1), (1, 1)):
            raw_u = [F(1)] if pu == 0 else [F(0), F(1)]
            raw_v = [F(1)] if pv == 0 else [F(0), F(1)]
            local_u = [F(1)] if pu == 0 else [-a / du, 1 / du]
            local_v = [F(1)] if pv == 0 else [-b / dv, 1 / dv]
            raw_moments.append(_physical_integral(g, box, raw_u, raw_v))
            local_moments.append(_physical_integral(g, box, local_u, local_v) / weight)
        minima.append(amplitude * min(values[4 * t : 4 * t + 4]))
        maxima.append(amplitude * max(values[4 * t : 4 * t + 4]))
    return _detach(
        {
            "local_coefficients": local_coefficients,
            "global_coefficients": global_coefficients,
            "local_moments": local_moments,
            "raw_moments": raw_moments,
            "minima": minima,
            "maxima": maxima,
        }
    )


def _inverse(matrix):
    n = len(matrix)
    rows = [list(row) + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if rows[i][column]), None)
        _require(pivot is not None, "singular moment map")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [x / scale for x in rows[column]]
        for i in range(n):
            if i != column:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[column], strict=True)]
    return [row[n:] for row in rows]


def _corner_map():
    # Integrate the separate linear endpoint basis functions, not stored Q values.
    linear_basis = ((F(1), F(-1)), (F(0), F(1)))
    one_dimensional = [
        [
            sum((a / F(power + degree + 1) for power, a in enumerate(basis)), F(0))
            for basis in linear_basis
        ]
        for degree in (0, 1)
    ]
    pairs = ((0, 0), (1, 0), (0, 1), (1, 1))
    Q = [[one_dimensional[i][a] * one_dimensional[j][b] for a, b in pairs] for i, j in pairs]
    U = _inverse(Q)
    identity = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    _require(_mm(Q, U) == identity and _mm(U, Q) == identity, "two-sided corner inverse")
    rho = [sum(row, F(0)) for row in Q]
    _require(
        all(x >= 0 for row in Q for x in row) and all(x <= 1 for x in rho), "local cube containment"
    )
    return Q, U, rho


def _comparison(upper, lower, domain, undefined=None):
    gap = [None if i not in domain else upper[i] - lower[i] for i in range(len(upper))]
    _require(all(gap[i] >= 0 for i in domain), "baseline or enclosure domination failed")
    strict = [i for i in domain if gap[i] > 0]
    tied = [i for i in domain if gap[i] == 0]
    maximum, rows = _maximum(gap, domain)
    _require(sorted(strict + tied) == domain, "comparison partition")
    out = {
        "gain_gap": gap,
        "strict_rows": strict,
        "tied_rows": tied,
        "max_gap": maximum,
        "max_gap_rows": rows,
    }
    if undefined is not None:
        out["undefined_rows"] = undefined
        _require(
            sorted(strict + tied + undefined) == list(range(len(upper))),
            "target comparison partition",
        )
    return out


def _field_endpoint(index, direction, signs, wires, H, A, scales, alpha, beta, defined, amplitude):
    corners = [F(direction * sign) for sign in signs]
    _require(all(abs(x) <= 1 for x in corners), "corner outside unit box")
    integrated = integrate(wires["probe"], wires["tiles"], _encode(corners))
    local_wire = synthesize(wires["Q"], _encode(corners))
    bank_wire = synthesize(wires["P"], _encode(corners))
    roundtrip_local_wire = synthesize(wires["Z"], bank_wire)
    roundtrip_corners_wire = synthesize(wires["U"], roundtrip_local_wire)
    observed_wire = produce(wires["B"], bank_wire)
    direct_wire = produce(wires["G"], bank_wire)
    decoded_wire = apply(wires["D"], observed_wire)
    local, bank = _vector(local_wire), _vector(bank_wire)
    roundtrip_local, roundtrip_corners = (
        _vector(roundtrip_local_wire),
        _vector(roundtrip_corners_wire),
    )
    observed, direct, decoded = _vector(observed_wire), _vector(direct_wire), _vector(decoded_wire)
    local_integrals, raw_integrals = (
        _vector(integrated["local_moments"]),
        _vector(integrated["raw_moments"]),
    )
    minima, maxima = _vector(integrated["minima"]), _vector(integrated["maxima"])
    _require(
        local == local_integrals and bank == raw_integrals,
        "integrated field moments differ from synthesis",
    )
    _require(roundtrip_local == local and roundtrip_corners == corners, "field synthesis roundtrip")
    _require(direct == decoded, "full field response pipeline")
    _require(observed == _linear(H, corners), "field receiver map")
    _require(
        all(-amplitude <= lo <= hi <= amplitude for lo, hi in zip(minima, maxima, strict=True)),
        "actual field bound",
    )
    _require(
        all(abs(x) <= radius for x, radius in zip(observed, beta, strict=True)),
        "field receiver bound",
    )
    normalized = _normalized(decoded, scales)
    for i in defined:
        _require(normalized[i] == _dot(A[i], corners), "normalized field map")
        _require(abs(normalized[i]) <= alpha[i], "field response bound")
    out = {
        "corners": corners,
        "local_coefficients": _vector(integrated["local_coefficients"]),
        "global_coefficients": _vector(integrated["global_coefficients"]),
        "local_moments": local_integrals,
        "bank_error": bank,
        "integrated_bank_error": raw_integrals,
        "roundtrip_local": roundtrip_local,
        "roundtrip_corners": roundtrip_corners,
        "tile_minima": minima,
        "tile_maxima": maxima,
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
    }
    if index is not None:
        _require(normalized[index] == direction * alpha[index], "field endpoint fails attainment")
        out["attained"] = normalized[index]
    return out


def _enclosure_endpoint(index, direction, signs, decoder, E, scales, beta, gamma, defined):
    observed = [direction * radius * sign for radius, sign in zip(beta, signs, strict=True)]
    decoded = _vector(apply(decoder, _encode(observed)))
    normalized = _normalized(decoded, scales)
    primitive = [F(direction * sign) for sign in signs]
    for i in defined:
        _require(normalized[i] == _dot(E[i], primitive), "enclosure normalized map")
        _require(abs(normalized[i]) <= gamma[i], "enclosure response bound")
    _require(
        all(abs(x) <= radius for x, radius in zip(observed, beta, strict=True)), "enclosure box"
    )
    attained = normalized[index]
    _require(attained == direction * gamma[index], "enclosure endpoint attainment")
    return {
        "observed_error": observed,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "attained": attained,
    }


def build_family(problem):
    """Certify the declared bilinear field class through unchanged response maps."""
    probe, cells, tiles, B, G, D, targets, q, r, s, t = _problem(problem)
    V, cell_volumes, tile_volumes, scales, defined, undefined = _geometry(
        problem, probe, cells, tiles, targets
    )
    _require(all(all(x == 0 for x in G[i]) for i in undefined), "nonzero null-cell target")
    weights = [V * V * h for h in tile_volumes]
    W, Z = _blocks(tiles, weights)
    Q, U, rho = _corner_map()
    P = [_mm(block, Q) for block in W]
    K = _mm(D, B, r)
    Rbank = _subtract(K, G)
    _require(_zero(Rbank), "full frozen bank identity")
    H0 = _right_blocks(B, W)
    J0 = _right_blocks(G, W)
    A0 = [None if not scales[i] else [x / scales[i] for x in J0[i]] for i in range(q)]
    beta0 = [sum(map(abs, row), F(0)) for row in H0]
    alpha0 = [None if row is None else sum(map(abs, row), F(0)) for row in A0]
    gamma0 = [
        None
        if not scales[i]
        else sum((abs(D[i][j]) * beta0[j] / scales[i] for j in range(s)), F(0))
        for i in range(q)
    ]
    H = _right_blocks(B, P)
    J = _right_blocks(G, P)
    L = _mm(D, H, r)
    Rerror = _subtract(L, J)
    _require(_zero(Rerror), "field error identity")
    A = [None if not scales[i] else [x / scales[i] for x in J[i]] for i in range(q)]
    beta = [sum(map(abs, row), F(0)) for row in H]
    E = [
        None if not scales[i] else [D[i][j] * beta[j] / scales[i] for j in range(s)]
        for i in range(q)
    ]
    alpha = [None if row is None else sum(map(abs, row), F(0)) for row in A]
    gamma = [None if row is None else sum(map(abs, row), F(0)) for row in E]
    _require(
        all((alpha[i] == 0) == (alpha0[i] == 0) for i in defined),
        "zero field/local gain equivalence",
    )
    comparisons = {
        "field_vs_enclosure": _comparison(gamma, alpha, defined, undefined),
        "field_vs_local": _comparison(alpha0, alpha, defined, undefined),
        "enclosure_vs_local": _comparison(gamma0, gamma, defined, undefined),
        "receiver_reduction": _comparison(beta0, beta, list(range(s))),
    }
    field_max, field_rows = _maximum(alpha, defined)
    enclosure_max, enclosure_rows = _maximum(gamma, defined)
    wires = {
        "probe": problem["probe"],
        "tiles": [tile["bounds"] for tile in problem["tiles"]],
        "Q": _encode([Q for _ in tiles]),
        "U": _encode([U for _ in tiles]),
        "P": _encode(P),
        "Z": _encode(Z),
        "B": _encode(B),
        "G": _encode(G),
        "D": _encode(D),
    }
    fw, ew = [None] * q, [None] * q
    for i in defined:
        signs = list(map(_sign, A[i]))
        fw[i] = {
            "target_row": i,
            "signs": signs,
            "positive": _field_endpoint(
                i, 1, signs, wires, H, A, scales, alpha, beta, defined, V * V
            ),
            "negative": _field_endpoint(
                i, -1, signs, wires, H, A, scales, alpha, beta, defined, V * V
            ),
        }
        signs = list(map(_sign, E[i]))
        ew[i] = {
            "target_row": i,
            "signs": signs,
            "positive": _enclosure_endpoint(
                i, 1, signs, wires["D"], E, scales, beta, gamma, defined
            ),
            "negative": _enclosure_endpoint(
                i, -1, signs, wires["D"], E, scales, beta, gamma, defined
            ),
        }
    constants = [
        _field_endpoint(None, direction, [1] * r, wires, H, A, scales, alpha, beta, defined, V * V)
        for direction in (1, -1)
    ]
    nonnegative = [i for i in defined if all(x >= 0 for x in A[i])]
    nonpositive = [i for i in defined if all(x <= 0 for x in A[i])]
    mixed = [i for i in defined if any(x < 0 for x in A[i]) and any(x > 0 for x in A[i])]
    zero = [i for i in defined if all(x == 0 for x in A[i])]
    _require(set(zero) == set(nonnegative) & set(nonpositive), "zero sign intersection")
    _require(
        set(mixed) == set(defined) - (set(nonnegative) | set(nonpositive)), "mixed sign complement"
    )
    constant_response = [None if row is None else sum(row, F(0)) for row in A]
    for i in defined:
        _require(
            constants[0]["normalized_error"][i] == constant_response[i],
            "positive constant response",
        )
        _require(
            constants[1]["normalized_error"][i] == -constant_response[i],
            "negative constant response",
        )
    positive_attains = [i for i in defined if constant_response[i] == alpha[i]]
    negative_attains = [i for i in defined if -constant_response[i] == alpha[i]]
    d = len(defined)
    a = sum(cell is not None for cell in cells)
    return _detach(
        {
            "problem": problem,
            "geometry": {
                "volume": V,
                "cell_volumes": cell_volumes,
                "tile_volumes": tile_volumes,
                "target_scales": scales,
                "defined_rows": defined,
                "undefined_rows": undefined,
            },
            "coordinates": {
                "bank_scales": weights,
                "raw_from_local": W,
                "local_from_raw": Z,
                "local_from_corner": Q,
                "corner_from_local": U,
                "raw_from_corner": P,
                "corner_moment_row_sums": rho,
            },
            "baseline": {
                "interface_error": H0,
                "target_error": J0,
                "normalized_target": A0,
                "receiver_radii": beta0,
                "shared_gains": alpha0,
                "enclosure_gains": gamma0,
            },
            "maps": {
                "decoder_bank": K,
                "bank_residual": Rbank,
                "interface_error": H,
                "target_error": J,
                "decoded_error": L,
                "error_residual": Rerror,
                "normalized_target": A,
                "enclosure_target": E,
            },
            "field": {
                "row_gains": alpha,
                "witnesses": fw,
                "max_gain": field_max,
                "max_rows": field_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": ew,
                "max_gain": enclosure_max,
                "max_rows": enclosure_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": comparisons,
            "positivity": {
                "nonnegative_rows": nonnegative,
                "nonpositive_rows": nonpositive,
                "mixed_rows": mixed,
                "zero_rows": zero,
                "constant_response": constant_response,
                "positive_constant_attains": positive_attains,
                "negative_constant_attains": negative_attains,
                "constant_positive": constants[0],
                "constant_negative": constants[1],
            },
            "checks": {
                name: True
                for name in (
                    "geometry_partitions",
                    "bank_label_identity",
                    "coordinate_inverse",
                    "moment_integrals",
                    "moment_inverse",
                    "local_box_containment",
                    "frozen_bank_identity",
                    "error_map_identity",
                    "baseline_dominance",
                    "normalization_domain",
                    "field_bound",
                    "field_pipeline",
                    "field_attainment",
                    "enclosure_box",
                    "enclosure_attainment",
                    "constant_fields",
                    "coefficient_sign_partition",
                    "complete_gain_partitions",
                )
            },
            "counts": {
                "cells": len(cells),
                "positive_cells": a,
                "tiles": t,
                "bank_values": r,
                "receiver_values": s,
                "target_rows": q,
                "defined_rows": d,
                "undefined_rows": q - d,
                "geometry_input_entries": 4 + 4 * a + 4 * t,
                "input_matrix_entries": s * r + q * r + q * s,
                "geometry_entries": 1 + len(cells) + t + q,
                "coordinate_entries": 49 * t + 36,
                "baseline_entries": (s + q + d) * r + s + 2 * d,
                "map_entries": 5 * q * r + s * r + d * (r + s),
                "gain_entries": s + 2 * d + (2 if d else 0),
                "comparison_entries": 3 * d + s + (3 if d else 0) + (1 if s else 0),
                "positivity_entries": d,
                "field_witnesses": 2 * d,
                "field_sign_entries": d * r,
                "field_witness_entries": 2 * d * (8 * r + 2 * t + s + 2 * q + d + 1),
                "enclosure_witnesses": 2 * d,
                "enclosure_sign_entries": d * s,
                "enclosure_witness_entries": 2 * d * (s + q + d + 1),
                "constant_witnesses": 2,
                "constant_witness_entries": 2 * (8 * r + 2 * t + s + 2 * q + d),
                "field_maximizers": len(field_rows),
                "enclosure_maximizers": len(enclosure_rows),
                "field_enclosure_strict": len(comparisons["field_vs_enclosure"]["strict_rows"]),
                "field_local_strict": len(comparisons["field_vs_local"]["strict_rows"]),
                "enclosure_local_strict": len(comparisons["enclosure_vs_local"]["strict_rows"]),
                "receiver_strict": len(comparisons["receiver_reduction"]["strict_rows"]),
                "nonnegative_rows": len(nonnegative),
                "nonpositive_rows": len(nonpositive),
                "mixed_rows": len(mixed),
                "zero_rows": len(zero),
            },
        }
    )
