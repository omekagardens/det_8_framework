"""QR-05AX independent reference: actual tensor-Simpson field integrals.

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


def synthesize(blocks, values):
    """Apply ONLY explicitly supplied four-coordinate blocks, including inverses."""
    _native(blocks)
    _native(values)
    _need(type(blocks) is list and len(blocks) <= 256, "block inventory")
    _need(type(values) is list and len(values) == 4 * len(blocks), "block value width")
    for block in blocks:
        _dimensions(block, 4, 4)
    for block in blocks:
        _matrix_pair_shapes(block)
    _pair_shapes(values)
    parsed = [_matrix(block) for block in blocks]
    vector = [_fraction(x) for x in values]
    result = []
    for i, block in enumerate(parsed):
        result.extend(_matvec(block, vector[4 * i : 4 * i + 4]))
    return _wire(result)


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


def _coordinates(V, tiles, volumes):
    blocks, inverses, scales = [], [], []
    for tile, h in zip(tiles, volumes):
        u0, u1, v0, v1 = tile
        corners = [(u0, v0), (u1, v0), (u0, v1), (u1, v1)]
        values = [[ONE, u, v, u * v] for u, v in corners]
        scale = V * V * h
        block = []
        for monomial in range(4):
            a, b, c, d = [corner[monomial] for corner in values]
            block.append([scale * a, scale * (b - a), scale * (c - a), scale * (d - b - c + a)])
        inverse = _inverse(block)
        for left, right in ((block, inverse), (inverse, block)):
            for i in range(4):
                for j in range(4):
                    _need(
                        sum((left[i][h] * right[h][j] for h in range(4)), ZERO)
                        == (ONE if i == j else ZERO),
                        "two-sided coordinate inverse",
                    )
        blocks.append(block)
        inverses.append(inverse)
        scales.append(scale)
    return scales, blocks, inverses


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


def _moments(V, tiles, blocks):
    unit_tile = [ZERO, ONE, ZERO, ONE]
    basis = [[ONE if i == j else ZERO for i in range(4)] for j in range(4)]
    columns = [_integrals(ONE, unit_tile, column)["local_moments"] for column in basis]
    Q = [[columns[j][i] for j in range(4)] for i in range(4)]
    U = _inverse(Q)
    for left, right in ((Q, U), (U, Q)):
        for i in range(4):
            for j in range(4):
                _need(
                    sum((left[i][k] * right[k][j] for k in range(4)), ZERO)
                    == (ONE if i == j else ZERO),
                    "two-sided corner-moment inverse",
                )
    rho = [sum(row, ZERO) for row in Q]
    _need(
        all(value >= ZERO for row in Q for value in row)
        and all(ZERO <= value <= ONE for value in rho),
        "corner moment box containment",
    )
    raw_from_corner = []
    for tile, W in zip(tiles, blocks):
        direct = [_integrals(V, tile, column) for column in basis]
        _need(
            all(direct[j]["local_moments"] == columns[j] for j in range(4)),
            "universal local moment integrals",
        )
        P = [[direct[j]["raw_moments"][i] for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                _need(
                    P[i][j] == sum((W[i][k] * Q[k][j] for k in range(4)), ZERO),
                    "direct field integrals equal coordinate contraction",
                )
        raw_from_corner.append(P)
    return Q, U, rho, raw_from_corner


def _probe_maps(problem, B, G, raw_blocks, corner_blocks):
    q, r, s = len(G), len(G[0]), len(B)
    K = [[ZERO] * r for _ in range(q)]
    for j in range(r):
        unit = [ZERO] * r
        unit[j] = ONE
        observed = produce(problem["interface"], _wire(unit))
        decoded = _values(apply(problem["decoder"], observed))
        for i, value in enumerate(decoded):
            K[i][j] = value
    residual = [[K[i][j] - G[i][j] for j in range(r)] for i in range(q)]
    _need(not any(value for row in residual for value in row), "full frozen bank identity")
    H0, J0 = [[ZERO] * r for _ in range(s)], [[ZERO] * r for _ in range(q)]
    H, J, L = (
        [[ZERO] * r for _ in range(s)],
        [[ZERO] * r for _ in range(q)],
        [[ZERO] * r for _ in range(q)],
    )
    for j in range(r):
        unit = [ZERO] * r
        unit[j] = ONE
        bank = synthesize(raw_blocks, _wire(unit))
        observed = _values(produce(problem["interface"], bank))
        direct = _values(produce(problem["geometric"], bank))
        for i, value in enumerate(observed):
            H0[i][j] = value
        for i, value in enumerate(direct):
            J0[i][j] = value
        bank = synthesize(corner_blocks, _wire(unit))
        observed_wire = produce(problem["interface"], bank)
        observed = _values(observed_wire)
        direct = _values(produce(problem["geometric"], bank))
        decoded = _values(apply(problem["decoder"], observed_wire))
        for i, value in enumerate(observed):
            H[i][j] = value
        for i in range(q):
            J[i][j], L[i][j] = direct[i], decoded[i]
    error_residual = [[L[i][j] - J[i][j] for j in range(r)] for i in range(q)]
    _need(not any(value for row in error_residual for value in row), "field error identity")
    return K, residual, H0, J0, H, J, L, error_residual


def _radius(row):
    lower = sum((min(-x, x) for x in row), ZERO)
    upper = sum((max(-x, x) for x in row), ZERO)
    _need(lower == -upper and upper >= ZERO, "symmetric interval endpoints")
    return upper


def _sign(value):
    return int(value > ZERO) - int(value < ZERO)


def _normalized(raw, sigma):
    return [value / scale if scale else None for value, scale in zip(raw, sigma)]


def _maximum(values, domain):
    if not domain:
        return None, []
    maximum = max(values[i] for i in domain)
    return maximum, [i for i in domain if values[i] == maximum]


def _comparison(larger, smaller, undefined=None):
    undefined = [] if undefined is None else undefined
    domain = [i for i in range(len(larger)) if i not in undefined]
    gaps = [None if i in undefined else larger[i] - smaller[i] for i in range(len(larger))]
    _need(all(gaps[i] >= ZERO for i in domain), "ordered error-body gains")
    strict = [i for i in domain if gaps[i] > ZERO]
    tied = [i for i in domain if gaps[i] == ZERO]
    _need(
        sorted(strict + tied + undefined) == list(range(len(larger))),
        "complete comparison partition",
    )
    maximum, indices = _maximum(gaps, domain)
    return {
        "gain_gap": gaps,
        "strict_rows": strict,
        "tied_rows": tied,
        "max_gap": maximum,
        "max_gap_rows": indices,
    }


def _field_endpoint(
    problem,
    corners,
    V,
    sigma,
    defined,
    undefined,
    Q_blocks,
    U_blocks,
    P_blocks,
    Z_blocks,
    H,
    A,
    alpha,
    beta,
):
    _need(all(-ONE <= c <= ONE for c in corners), "corner primitive box")
    tiles = [tile["bounds"] for tile in problem["tiles"]]
    corner_wire = _wire(corners)
    actual = integrate(problem["probe"], tiles, corner_wire)
    actual = {key: _values(value) for key, value in actual.items()}
    local = _values(synthesize(Q_blocks, corner_wire))
    bank_wire = synthesize(P_blocks, corner_wire)
    bank = _values(bank_wire)
    roundtrip_wire = synthesize(Z_blocks, bank_wire)
    roundtrip = _values(roundtrip_wire)
    recovered = _values(synthesize(U_blocks, roundtrip_wire))
    observed_wire = produce(problem["interface"], bank_wire)
    observed = _values(observed_wire)
    direct = _values(produce(problem["geometric"], bank_wire))
    decoded = _values(apply(problem["decoder"], observed_wire))
    normalized = _normalized(decoded, sigma)
    _need(
        local == actual["local_moments"]
        and bank == actual["raw_moments"]
        and roundtrip == local
        and recovered == corners,
        "complete integral and corner roundtrip",
    )
    _need(
        direct == decoded and observed == _matvec(H, corners),
        "complete actual field pipeline",
    )
    _need(
        all(normalized[i] == _dot(A[i], corners) for i in defined)
        and all(normalized[i] is None for i in undefined),
        "field normalization domain",
    )
    _need(
        all(-alpha[i] <= normalized[i] <= alpha[i] for i in defined)
        and all(-bound <= value <= bound for value, bound in zip(observed, beta)),
        "complete field response bounds",
    )
    _need(
        all(-V * V <= lo <= hi <= V * V for lo, hi in zip(actual["minima"], actual["maxima"])),
        "complete actual field extrema",
    )
    return {
        "corners": corners,
        "local_coefficients": actual["local_coefficients"],
        "global_coefficients": actual["global_coefficients"],
        "local_moments": local,
        "bank_error": bank,
        "integrated_bank_error": actual["raw_moments"],
        "roundtrip_local": roundtrip,
        "roundtrip_corners": recovered,
        "tile_minima": actual["minima"],
        "tile_maxima": actual["maxima"],
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
    }


def build_family(problem):
    probe, ids, cells, tiles, owners, pairs, B, G, D = _parse(problem)
    V, cell_volumes, tile_volumes, sigma, defined, undefined = _geometry(
        probe,
        ids,
        cells,
        tiles,
        owners,
        pairs,
    )
    for i in undefined:
        _need(not any(G[i]), "undefined target must have zero raw geometric map")
    scales, W, Z = _coordinates(V, tiles, tile_volumes)
    Q, U, rho, P = _moments(V, tiles, W)
    raw_W, raw_Z, raw_P = _wire(W), _wire(Z), _wire(P)
    t, q, r, s = len(tiles), len(G), len(G[0]), len(B)
    raw_Q, raw_U = [_wire(Q)] * t, [_wire(U)] * t
    K, R_bank, H0, J0, H, J, L, R_error = _probe_maps(problem, B, G, raw_W, raw_P)
    beta0, beta = [_radius(row) for row in H0], [_radius(row) for row in H]
    A0 = [None if not sigma[i] else [v / sigma[i] for v in row] for i, row in enumerate(J0)]
    A = [None if not sigma[i] else [v / sigma[i] for v in row] for i, row in enumerate(J)]
    E0 = [
        None if not sigma[i] else [v * b / sigma[i] for v, b in zip(row, beta0)]
        for i, row in enumerate(D)
    ]
    E = [
        None if not sigma[i] else [v * b / sigma[i] for v, b in zip(row, beta)]
        for i, row in enumerate(D)
    ]
    alpha0, alpha = (
        [None if row is None else _radius(row) for row in matrix] for matrix in (A0, A)
    )
    gamma0, gamma = (
        [None if row is None else _radius(row) for row in matrix] for matrix in (E0, E)
    )
    _need(
        all((alpha[i] == ZERO) == (alpha0[i] == ZERO) for i in defined), "invertible zero response"
    )
    comparisons = {}
    for name, larger, smaller in (
        ("field_vs_enclosure", gamma, alpha),
        ("field_vs_local", alpha0, alpha),
        ("enclosure_vs_local", gamma0, gamma),
    ):
        comparisons[name] = {
            **_comparison(larger, smaller, undefined),
            "undefined_rows": list(undefined),
        }
    comparisons["receiver_reduction"] = _comparison(beta0, beta)
    field_witnesses, enclosure_witnesses = [None] * q, [None] * q

    def endpoint(corners):
        return _field_endpoint(
            problem,
            corners,
            V,
            sigma,
            defined,
            undefined,
            raw_Q,
            raw_U,
            raw_P,
            raw_Z,
            H,
            A,
            alpha,
            beta,
        )

    for target in defined:
        signs = [_sign(value) for value in A[target]]
        ends = []
        for direction in (ONE, -ONE):
            actual = endpoint([direction * value for value in signs])
            actual["attained"] = actual["normalized_error"][target]
            _need(actual["attained"] == direction * alpha[target], "field signed attainment")
            ends.append(actual)
        field_witnesses[target] = {
            "target_row": target,
            "signs": signs,
            "positive": ends[0],
            "negative": ends[1],
        }
        signs = [_sign(value) for value in E[target]]
        ends = []
        for direction in (ONE, -ONE):
            observed = [direction * b * sign for b, sign in zip(beta, signs)]
            _need(all(-b <= value <= b for b, value in zip(beta, observed)), "enclosure box")
            decoded = _values(apply(problem["decoder"], _wire(observed)))
            normalized = _normalized(decoded, sigma)
            _need(
                decoded == _matvec(D, observed)
                and all(-gamma[i] <= normalized[i] <= gamma[i] for i in defined)
                and all(normalized[i] is None for i in undefined),
                "full enclosure bounds and normalization",
            )
            _need(normalized[target] == direction * gamma[target], "enclosure signed attainment")
            ends.append(
                {
                    "observed_error": observed,
                    "decoded_error": decoded,
                    "normalized_error": normalized,
                    "attained": normalized[target],
                }
            )
        enclosure_witnesses[target] = {
            "target_row": target,
            "signs": signs,
            "positive": ends[0],
            "negative": ends[1],
        }
    positive, negative = endpoint([ONE] * r), endpoint([-ONE] * r)
    nonnegative = [i for i in defined if all(v >= ZERO for v in A[i])]
    nonpositive = [i for i in defined if all(v <= ZERO for v in A[i])]
    mixed = [i for i in defined if any(v > ZERO for v in A[i]) and any(v < ZERO for v in A[i])]
    zeros = [i for i in defined if not any(A[i])]
    _need(
        set(nonnegative) & set(nonpositive) == set(zeros)
        and sorted(set(nonnegative) | set(nonpositive) | set(mixed)) == defined
        and not (set(mixed) & (set(nonnegative) | set(nonpositive))),
        "complete coefficient sign partition",
    )
    response = [None if i in undefined else sum(A[i], ZERO) for i in range(q)]
    _need(
        all(
            positive["normalized_error"][i] == response[i]
            and negative["normalized_error"][i] == -response[i]
            for i in defined
        )
        and all(
            positive["normalized_error"][i] is None and negative["normalized_error"][i] is None
            for i in undefined
        ),
        "constant field response",
    )
    _need(
        all(v == V * V for v in positive["tile_minima"] + positive["tile_maxima"])
        and all(v == -V * V for v in negative["tile_minima"] + negative["tile_maxima"]),
        "actual constant field extrema",
    )
    positive_attains = [i for i in defined if response[i] == alpha[i]]
    negative_attains = [i for i in defined if -response[i] == alpha[i]]
    _need(
        positive_attains == nonnegative and negative_attains == nonpositive,
        "constant attainment partition",
    )
    field_max, field_rows = _maximum(alpha, defined)
    enclosure_max, enclosure_rows = _maximum(gamma, defined)
    d, c, a = len(defined), len(cells), sum(rectangle is not None for rectangle in cells)
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
            "coordinates": {
                "bank_scales": scales,
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
                "bank_residual": R_bank,
                "interface_error": H,
                "target_error": J,
                "decoded_error": L,
                "error_residual": R_error,
                "normalized_target": A,
                "enclosure_target": E,
            },
            "field": {
                "row_gains": alpha,
                "witnesses": field_witnesses,
                "max_gain": field_max,
                "max_rows": field_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": enclosure_witnesses,
                "max_gain": enclosure_max,
                "max_rows": enclosure_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": comparisons,
            "positivity": {
                "nonnegative_rows": nonnegative,
                "nonpositive_rows": nonpositive,
                "mixed_rows": mixed,
                "zero_rows": zeros,
                "constant_response": response,
                "positive_constant_attains": positive_attains,
                "negative_constant_attains": negative_attains,
                "constant_positive": positive,
                "constant_negative": negative,
            },
            "checks": dict.fromkeys(
                (
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
                "zero_rows": len(zeros),
            },
        }
    )
