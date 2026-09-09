"""QR-05AW independent reference: corner coordinates and local column probes.

The source producer and receiver evaluate only explicitly supplied raw values.
No historical executor, geometry, stored answer or hidden file is consumed.
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


def _probe_maps(problem, B, G, D, blocks):
    q, r, s = len(G), len(G[0]), len(B)
    K = [[ZERO] * r for _ in range(q)]
    for j in range(r):
        basis = [ZERO] * r
        basis[j] = ONE
        observed = produce(problem["interface"], _wire(basis))
        decoded = _values(apply(problem["decoder"], observed))
        for i, value in enumerate(decoded):
            K[i][j] = value
    R_bank = [[K[i][j] - G[i][j] for j in range(r)] for i in range(q)]
    _need(not any(x for row in R_bank for x in row), "full frozen bank identity")
    H, J, L = (
        [[ZERO] * r for _ in range(s)],
        [[ZERO] * r for _ in range(q)],
        [[ZERO] * r for _ in range(q)],
    )
    for j in range(r):
        basis = [ZERO] * r
        basis[j] = ONE
        bank = synthesize(blocks, _wire(basis))
        observed = produce(problem["interface"], bank)
        direct = _values(produce(problem["geometric"], bank))
        decoded = _values(apply(problem["decoder"], observed))
        for i, value in enumerate(_values(observed)):
            H[i][j] = value
        for i in range(q):
            J[i][j], L[i][j] = direct[i], decoded[i]
    R_error = [[L[i][j] - J[i][j] for j in range(r)] for i in range(q)]
    _need(not any(x for row in R_error for x in row), "local error identity")
    return K, R_bank, H, J, L, R_error


def _radius(row):
    lower, upper = ZERO, ZERO
    for value in row:
        lower += min(-value, value)
        upper += max(-value, value)
    _need(lower == -upper and upper >= ZERO, "symmetric interval endpoints")
    return upper


def _sign(value):
    return int(value > ZERO) - int(value < ZERO)


def _normalized(raw, sigma):
    return [value / scale if scale else None for value, scale in zip(raw, sigma)]


def _maximum(values, defined):
    if not defined:
        return None, []
    value = max(values[i] for i in defined)
    return value, [i for i in defined if values[i] == value]


def build_family(problem):
    probe, ids, cells, tiles, owners, pairs, B, G, D = _parse(problem)
    V, cell_volumes, tile_volumes, sigma, defined, undefined = _geometry(
        probe, ids, cells, tiles, owners, pairs
    )
    for i in undefined:
        _need(not any(G[i]), "undefined target must have zero raw geometric map")
    scales, blocks, inverses = _coordinates(V, tiles, tile_volumes)
    raw_blocks, inverse_blocks = _wire(blocks), _wire(inverses)
    q, r, s = len(G), len(G[0]), len(B)
    K, R_bank, H, J, L, R_error = _probe_maps(problem, B, G, D, raw_blocks)
    beta = [_radius(row) for row in H]
    A = [None if not sigma[i] else [value / sigma[i] for value in row] for i, row in enumerate(J)]
    E = [
        None if not sigma[i] else [value * radius / sigma[i] for value, radius in zip(row, beta)]
        for i, row in enumerate(D)
    ]
    alpha = [None if row is None else _radius(row) for row in A]
    gamma = [None if row is None else _radius(row) for row in E]
    gap = [None if i in undefined else gamma[i] - alpha[i] for i in range(q)]
    _need(all(gap[i] >= ZERO for i in defined), "conservative enclosure")
    shared_witnesses, enclosure_witnesses = [None] * q, [None] * q
    for target in defined:
        signs = [_sign(value) for value in A[target]]
        endpoints = []
        for direction in (ONE, -ONE):
            primitive = [direction * value for value in signs]
            _need(all(-ONE <= value <= ONE for value in primitive), "local primitive box")
            bank_wire = synthesize(raw_blocks, _wire(primitive))
            roundtrip_wire = synthesize(inverse_blocks, bank_wire)
            observed_wire = produce(problem["interface"], bank_wire)
            direct_wire = produce(problem["geometric"], bank_wire)
            decoded_wire = apply(problem["decoder"], observed_wire)
            bank, roundtrip, observed, direct, decoded = (
                _values(values)
                for values in (bank_wire, roundtrip_wire, observed_wire, direct_wire, decoded_wire)
            )
            normalized = _normalized(decoded, sigma)
            _need(
                roundtrip == primitive and direct == decoded and observed == _matvec(H, primitive),
                "full local shared pipeline",
            )
            _need(
                all(normalized[i] == _dot(A[i], primitive) for i in defined)
                and all(normalized[i] is None for i in undefined),
                "normalization domain",
            )
            _need(
                all(-alpha[i] <= normalized[i] <= alpha[i] for i in defined)
                and all(-b <= value <= b for value, b in zip(observed, beta)),
                "complete shared bounds",
            )
            _need(normalized[target] == direction * alpha[target], "shared signed attainment")
            endpoints.append(
                {
                    "primitive": primitive,
                    "bank_error": bank,
                    "roundtrip_primitive": roundtrip,
                    "observed_error": observed,
                    "direct_error": direct,
                    "decoded_error": decoded,
                    "normalized_error": normalized,
                    "attained": normalized[target],
                }
            )
        shared_witnesses[target] = {
            "target_row": target,
            "signs": signs,
            "positive": endpoints[0],
            "negative": endpoints[1],
        }
        signs = [_sign(value) for value in E[target]]
        endpoints = []
        for direction in (ONE, -ONE):
            observed = [direction * b * value for b, value in zip(beta, signs)]
            _need(
                all(-b <= value <= b for b, value in zip(beta, observed)), "receiver enclosure box"
            )
            decoded = _values(apply(problem["decoder"], _wire(observed)))
            normalized = _normalized(decoded, sigma)
            _need(
                decoded == _matvec(D, observed)
                and all(-gamma[i] <= normalized[i] <= gamma[i] for i in defined)
                and all(normalized[i] is None for i in undefined),
                "full enclosure response",
            )
            _need(normalized[target] == direction * gamma[target], "enclosure signed attainment")
            endpoints.append(
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
            "positive": endpoints[0],
            "negative": endpoints[1],
        }
    shared_max, shared_rows = _maximum(alpha, defined)
    enclosure_max, enclosure_rows = _maximum(gamma, defined)
    max_gap, max_gap_rows = _maximum(gap, defined)
    strict = [i for i in defined if gap[i] > ZERO]
    tied = [i for i in defined if gap[i] == ZERO]
    _need(sorted(strict + tied + undefined) == list(range(q)), "complete gain/undefined partition")
    d, t, c = len(defined), len(tiles), len(cells)
    a = sum(rectangle is not None for rectangle in cells)
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
                "raw_from_local": blocks,
                "local_from_raw": inverses,
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
            "shared": {
                "row_gains": alpha,
                "witnesses": shared_witnesses,
                "max_gain": shared_max,
                "max_rows": shared_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": enclosure_witnesses,
                "max_gain": enclosure_max,
                "max_rows": enclosure_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": {
                "gain_gap": gap,
                "strict_rows": strict,
                "tied_rows": tied,
                "undefined_rows": undefined,
                "max_gap": max_gap,
                "max_gap_rows": max_gap_rows,
            },
            "checks": dict.fromkeys(
                (
                    "geometry_partitions",
                    "bank_label_identity",
                    "coordinate_inverse",
                    "frozen_bank_identity",
                    "error_map_identity",
                    "normalization_domain",
                    "primitive_box",
                    "shared_pipeline",
                    "shared_attainment",
                    "enclosure_box",
                    "enclosure_attainment",
                    "complete_gain_partition",
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
                "coordinate_entries": 33 * t,
                "map_entries": 5 * q * r + s * r + d * (r + s),
                "gain_entries": s + 3 * d + (3 if d else 0),
                "shared_witnesses": 2 * d,
                "shared_sign_entries": d * r,
                "shared_witness_entries": 2 * d * (3 * r + s + 2 * q + d + 1),
                "enclosure_witnesses": 2 * d,
                "enclosure_sign_entries": d * s,
                "enclosure_witness_entries": 2 * d * (s + q + d + 1),
                "shared_maximizers": len(shared_rows),
                "enclosure_maximizers": len(enclosure_rows),
                "gap_maximizers": len(max_gap_rows),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )
