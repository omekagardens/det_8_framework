"""Exact geometry-local bank error domains for a frozen linear receiver."""

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


def _shared_endpoint(index, direction, signs, wires, H, A, scales, alpha, beta, defined):
    primitive = [F(direction * sign) for sign in signs]
    _require(all(abs(value) <= 1 for value in primitive), "primitive outside unit box")
    bank_wire = synthesize(wires["W"], _encode(primitive))
    roundtrip_wire = synthesize(wires["Z"], bank_wire)
    observed_wire = produce(wires["B"], bank_wire)
    direct_wire = produce(wires["G"], bank_wire)
    decoded_wire = apply(wires["D"], observed_wire)
    bank, roundtrip = _vector(bank_wire), _vector(roundtrip_wire)
    observed, direct, decoded = _vector(observed_wire), _vector(direct_wire), _vector(decoded_wire)
    normalized = _normalized(decoded, scales)
    _require(roundtrip == primitive, "local roundtrip differs")
    _require(direct == decoded, "shared full raw pipeline differs")
    _require(observed == _linear(H, primitive), "shared interface map differs")
    for i in defined:
        _require(normalized[i] == _dot(A[i], primitive), "normalized shared map differs")
        _require(abs(normalized[i]) <= alpha[i], "shared target bound exceeded")
    _require(
        all(abs(value) <= radius for value, radius in zip(observed, beta, strict=True)),
        "shared receiver radius exceeded",
    )
    attained = normalized[index]
    _require(attained == direction * alpha[index], "shared endpoint fails attainment")
    return {
        "primitive": primitive,
        "bank_error": bank,
        "roundtrip_primitive": roundtrip,
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "attained": attained,
    }


def _enclosure_endpoint(index, direction, signs, decoder, E, scales, beta, gamma, defined):
    observed = [direction * radius * sign for radius, sign in zip(beta, signs, strict=True)]
    decoded = _vector(apply(decoder, _encode(observed)))
    normalized = _normalized(decoded, scales)
    primitive = [F(direction * sign) for sign in signs]
    for i in defined:
        _require(normalized[i] == _dot(E[i], primitive), "normalized enclosure map differs")
        _require(abs(normalized[i]) <= gamma[i], "enclosure target bound exceeded")
    _require(
        all(abs(value) <= radius for value, radius in zip(observed, beta, strict=True)),
        "enclosure receiver radius exceeded",
    )
    attained = normalized[index]
    _require(attained == direction * gamma[index], "enclosure endpoint fails attainment")
    return {
        "observed_error": observed,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "attained": attained,
    }


def build_family(problem):
    """Certify a newly declared local moment-error box, not AV's raw box."""
    probe, cells, tiles, B, G, D, targets, q, r, s, t = _problem(problem)
    V, cell_volumes, tile_volumes, scales, defined, undefined = _geometry(
        problem, probe, cells, tiles, targets
    )
    _require(
        all(all(value == 0 for value in G[i]) for i in undefined), "null-cell target G row nonzero"
    )
    weights = [V * V * volume for volume in tile_volumes]
    W, Z = _blocks(tiles, weights)
    K = _mm(D, B, r)
    bank_residual = _subtract(K, G)
    _require(_zero(bank_residual), "frozen full-bank identity differs")
    H = _right_blocks(B, W)
    J = _right_blocks(G, W)
    L = _mm(D, H, r)
    error_residual = _subtract(L, J)
    _require(_zero(error_residual), "error map identity differs")
    A = [None if not scales[i] else [x / scales[i] for x in J[i]] for i in range(q)]
    beta = [sum(map(abs, row), F(0)) for row in H]
    E = [
        None if not scales[i] else [D[i][j] * beta[j] / scales[i] for j in range(s)]
        for i in range(q)
    ]
    alpha = [None if row is None else sum(map(abs, row), F(0)) for row in A]
    gamma = [None if row is None else sum(map(abs, row), F(0)) for row in E]
    gap = [None if not scales[i] else gamma[i] - alpha[i] for i in range(q)]
    _require(all(gap[i] >= 0 for i in defined), "enclosure fails to contain shared gain")
    strict = [i for i in defined if gap[i] > 0]
    tied = [i for i in defined if gap[i] == 0]
    _require(sorted(strict + tied + undefined) == list(range(q)), "gain partition incomplete")
    shared_max, shared_rows = _maximum(alpha, defined)
    enclosure_max, enclosure_rows = _maximum(gamma, defined)
    gap_max, gap_rows = _maximum(gap, defined)
    wires = {"W": _encode(W), "Z": _encode(Z), "B": _encode(B), "G": _encode(G), "D": _encode(D)}
    sw, ew = [None] * q, [None] * q
    for i in defined:
        signs = list(map(_sign, A[i]))
        sw[i] = {
            "target_row": i,
            "signs": signs,
            "positive": _shared_endpoint(i, 1, signs, wires, H, A, scales, alpha, beta, defined),
            "negative": _shared_endpoint(i, -1, signs, wires, H, A, scales, alpha, beta, defined),
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
            "coordinates": {"bank_scales": weights, "raw_from_local": W, "local_from_raw": Z},
            "maps": {
                "decoder_bank": K,
                "bank_residual": bank_residual,
                "interface_error": H,
                "target_error": J,
                "decoded_error": L,
                "error_residual": error_residual,
                "normalized_target": A,
                "enclosure_target": E,
            },
            "shared": {
                "row_gains": alpha,
                "witnesses": sw,
                "max_gain": shared_max,
                "max_rows": shared_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": ew,
                "max_gain": enclosure_max,
                "max_rows": enclosure_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": {
                "gain_gap": gap,
                "strict_rows": strict,
                "tied_rows": tied,
                "undefined_rows": undefined,
                "max_gap": gap_max,
                "max_gap_rows": gap_rows,
            },
            "checks": {
                "geometry_partitions": True,
                "bank_label_identity": True,
                "coordinate_inverse": True,
                "frozen_bank_identity": True,
                "error_map_identity": True,
                "normalization_domain": True,
                "primitive_box": True,
                "shared_pipeline": True,
                "shared_attainment": True,
                "enclosure_box": True,
                "enclosure_attainment": True,
                "complete_gain_partition": True,
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
                "gap_maximizers": len(gap_rows),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )
