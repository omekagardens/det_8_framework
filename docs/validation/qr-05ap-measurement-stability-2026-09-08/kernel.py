"""Private sharp box-error certificates for two inherited affine decoders.

No field integrations, rank selections or decoder fits occur here. Raw maps
are transported into declared dimensionless coordinates before comparison.
"""

import json
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "integer exceeds retained component bound")
    elif value is None or kind in (str, bool):
        return
    elif kind is list:
        for child in value:
            _native(child)
    elif kind is dict:
        _require(all(type(key) is str for key in value), "native string keys required")
        for child in value.values():
            _native(child)
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


def _rectangle_shape(value):
    _require(type(value) is list and len(value) == 4, "four rectangle coordinates required")


def _rectangle(value):
    _rectangle_shape(value)
    b = tuple(map(_fraction, value))
    _require(b[0] < b[1] and b[2] < b[3], "positive rectangle required")
    return b


def _matrix_shape(value, rows, columns):
    _require(type(value) is list and len(value) == rows, "matrix row count differs")
    _require(
        all(type(row) is list and len(row) == columns for row in value),
        "matrix column count differs",
    )


def _matrix(value):
    return [list(map(_fraction, row)) for row in value]


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F(0))


def _mm(left, right):
    columns = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in columns] for row in left]


def _area(b):
    return (b[1] - b[0]) * (b[3] - b[2]) / 2


def _contains(a, b):
    return a[0] <= b[0] and b[1] <= a[1] and a[2] <= b[2] and b[3] <= a[3]


def _overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def _preflight(problem):
    """All container/dimension admission precedes geometry and matrix loops."""
    _native(problem)
    _fields(
        problem,
        ("family", "probe", "cells", "tiles", "observations", "targets", "canonical", "geometric"),
    )
    _require(
        type(problem["family"]) is str and problem["family"], "nonempty native family required"
    )
    _rectangle_shape(problem["probe"])
    cells, tiles = problem["cells"], problem["tiles"]
    _require(
        type(cells) is list and 1 <= len(cells) <= 8, "bounded nonempty cell inventory required"
    )
    _require(
        type(tiles) is list and 1 <= len(tiles) <= 64, "bounded nonempty tile inventory required"
    )
    for cell in cells:
        _fields(cell, ("event", "bounds"))
        _require(type(cell["event"]) is int, "native cell ID required")
        if cell["bounds"] is not None:
            _rectangle_shape(cell["bounds"])
    ids = [cell["event"] for cell in cells]
    _require(ids == sorted(set(ids)), "sorted unique cell IDs required")
    for tile in tiles:
        _fields(tile, ("event", "bounds"))
        _require(type(tile["event"]) is int, "native tile owner required")
        _rectangle_shape(tile["bounds"])
    m, q = 4 * len(tiles), len(cells) ** 2
    observations = problem["observations"]
    _require(
        type(observations) is list and len(observations) == m and type(observations[0]) is list,
        "weighted observation row inventory differs",
    )
    n = len(observations[0])
    _require(1 <= n <= 64, "bounded generator dimension required")
    _matrix_shape(observations, m, n)
    _matrix_shape(problem["targets"], q, n)
    _fields(problem["canonical"], ("row_basis", "decoder"))
    basis = problem["canonical"]["row_basis"]
    _require(
        type(basis) is list and 1 <= len(basis) <= 64 and all(type(i) is int for i in basis),
        "bounded native decoder basis required",
    )
    _require(
        basis == sorted(set(basis)) and basis[0] == 0 and basis[-1] <= m,
        "normalization-first in-range basis required",
    )
    _matrix_shape(problem["canonical"]["decoder"], q, len(basis))
    _matrix_shape(problem["geometric"], q, m)
    return m, n, q


def _parse(problem):
    m, n, q = _preflight(problem)
    probe = _rectangle(problem["probe"])
    cells = [
        (row["event"], _rectangle(row["bounds"]) if row["bounds"] is not None else None)
        for row in problem["cells"]
    ]
    tiles = [(row["event"], _rectangle(row["bounds"])) for row in problem["tiles"]]
    observations, targets = _matrix(problem["observations"]), _matrix(problem["targets"])
    compact, geometric = _matrix(problem["canonical"]["decoder"]), _matrix(problem["geometric"])
    volume = _area(probe)
    positive = [b for _, b in cells if b is not None]
    _require(all(_contains(probe, b) for b in positive), "cell lies outside probe")
    _require(
        all(not _overlap(a, b) for a, b in combinations(positive, 2)), "cell interiors overlap"
    )
    _require(sum((_area(b) for b in positive), F(0)) == volume, "cells do not cover probe")
    by_id = dict(cells)
    _require(
        all(e in by_id and by_id[e] is not None and _contains(by_id[e], b) for e, b in tiles),
        "tile lacks its named nonempty containing cell",
    )
    keys = [(e, b[0], b[2], b[1], b[3]) for e, b in tiles]
    _require(keys == sorted(keys), "tile ordering differs")
    _require(
        all(not _overlap(a[1], b[1]) for a, b in combinations(tiles, 2)), "tile interiors overlap"
    )
    for event, bounds in cells:
        expected = _area(bounds) if bounds is not None else F(0)
        _require(
            sum((_area(b) for e, b in tiles if e == event), F(0)) == expected,
            "tiles do not cover each cell",
        )
    intercept = [F(0)] * q
    dense = [[F(0)] * m for _ in range(q)]
    for i, row in enumerate(compact):
        for index, coefficient in zip(problem["canonical"]["row_basis"], row, strict=True):
            if index == 0:
                intercept[i] = coefficient
            else:
                dense[i][index - 1] = coefficient
    raw = [("canonical", intercept, dense), ("geometric", [F(0)] * q, geometric)]
    for _, a, linear in raw:
        applied = _mm(linear, observations)
        _require(
            all([a[j] + x for x in row] == targets[j] for j, row in enumerate(applied)),
            "inherited raw response identity failed",
        )
    cell_volumes = [_area(b) if b is not None else F(0) for _, b in cells]
    scales = [volume**2 * a * b for a, b in product(cell_volumes, repeat=2)]
    for scale, target in zip(scales, targets, strict=True):
        _require(
            scale != 0 or all(x == 0 for x in target), "empty response label has nonzero target"
        )
    return cells, tiles, observations, targets, raw, volume, cell_volumes, scales, n


def _transforms(bounds, volume):
    u, u1, v, v1 = bounds
    du, dv = u1 - u, v1 - v
    scale = volume**2 * _area(bounds)
    forward = [
        [F(1), F(0), F(0), F(0)],
        [u, du, F(0), F(0)],
        [v, F(0), dv, F(0)],
        [u * v, du * v, u * dv, du * dv],
    ]
    inverse = [
        [F(1), F(0), F(0), F(0)],
        [-u / du, 1 / du, F(0), F(0)],
        [-v / dv, F(0), 1 / dv, F(0)],
        [u * v / (du * dv), -v / (du * dv), -u / (du * dv), 1 / (du * dv)],
    ]
    forward = [[x * scale for x in row] for row in forward]
    inverse = [[x / scale for x in row] for row in inverse]
    identity = [[F(i == j) for j in range(4)] for i in range(4)]
    _require(
        _mm(forward, inverse) == _mm(inverse, forward) == identity,
        "local/raw coordinate matrices are not mutual inverses",
    )
    return forward, inverse


def _decoder(name, raw_intercept, raw_matrix, transforms, scales, observations, targets):
    intercept, matrix = [], []
    for a, row, scale in zip(raw_intercept, raw_matrix, scales, strict=True):
        if scale == 0:
            intercept.append(None)
            matrix.append(None)
            continue
        intercept.append(a / scale)
        matrix.append(
            [
                sum((row[4 * t + i] * transform[i][j] for i in range(4)), F(0)) / scale
                for t, transform in enumerate(transforms)
                for j in range(4)
            ]
        )
    for a, row, target in zip(intercept, matrix, targets, strict=True):
        if row is None:
            _require(a is None and target is None, "normalized null rows differ")
        else:
            _require(
                [a + x for x in _mm([row], observations)[0]] == target,
                "normalized response identity failed",
            )
    gains = [sum(map(abs, row), F(0)) if row is not None else None for row in matrix]
    witnesses = []
    for j, row in enumerate(matrix):
        if row is None:
            witnesses.append(None)
            continue
        signs = [1 if x > 0 else -1 if x < 0 else 0 for x in row]
        _require(all(abs(x) <= 1 for x in signs), "witness leaves declared error box")
        output = [_dot(other, signs) if other is not None else None for other in matrix]
        _require(output[j] == gains[j], "witness does not attain row absolute bound")
        witnesses.append({"signs": signs, "output": output, "attained": output[j]})
    defined = [g for g in gains if g is not None]
    maximum = max(defined) if defined else None
    maximum_rows = [i for i, g in enumerate(gains) if g is not None and g == maximum]
    return {
        "name": name,
        "raw_intercept": list(raw_intercept),
        "raw_matrix": [list(row) for row in raw_matrix],
        "intercept": intercept,
        "matrix": matrix,
        "row_gains": gains,
        "witnesses": witnesses,
        "max_gain": maximum,
        "max_rows": maximum_rows,
    }


def apply(intercept, matrix, z):
    """Apply only the supplied affine map; no model or hidden-field access."""
    _native([intercept, matrix, z])
    _require(
        type(intercept) is list and 1 <= len(intercept) <= 64, "bounded paired output rows required"
    )
    _require(
        type(matrix) is list and len(matrix) == len(intercept), "paired output inventory differs"
    )
    _require(
        type(z) is list and 0 < len(z) <= 256 and len(z) % 4 == 0,
        "positive four-coordinate observation blocks required",
    )
    for a, row in zip(intercept, matrix, strict=True):
        _require((a is None) == (row is None), "intercept and matrix nulls must be paired")
        if row is not None:
            _require(type(row) is list and len(row) == len(z), "affine row width differs")
    coordinates = list(map(_fraction, z))
    parsed = [
        (None, None) if row is None else (_fraction(a), list(map(_fraction, row)))
        for a, row in zip(intercept, matrix, strict=True)
    ]
    return _detach([a + _dot(row, coordinates) if row is not None else None for a, row in parsed])


def build_family(problem):
    """Transport inherited maps and certify their exact rowwise box gains."""
    cells, tiles, observations, targets, raw, volume, cell_volumes, scales, n = _parse(problem)
    transform_pairs = [_transforms(bounds, volume) for _, bounds in tiles]
    forward = [pair[0] for pair in transform_pairs]
    inverse = [pair[1] for pair in transform_pairs]
    local_observations = [
        row
        for t, block in enumerate(inverse)
        for row in _mm(block, observations[4 * t : 4 * t + 4])
    ]
    local_targets = [
        [x / scale for x in row] if scale else None
        for row, scale in zip(targets, scales, strict=True)
    ]
    decoders = [
        _decoder(name, a, linear, forward, scales, local_observations, local_targets)
        for name, a, linear in raw
    ]
    comparison = {
        "gain_difference": [],
        "canonical_lower_rows": [],
        "geometric_lower_rows": [],
        "tied_rows": [],
        "undefined_rows": [],
    }
    for i, (a, b) in enumerate(
        zip(decoders[0]["row_gains"], decoders[1]["row_gains"], strict=True)
    ):
        _require((a is None) == (b is None), "gain supports differ")
        if a is None:
            comparison["gain_difference"].append(None)
            comparison["undefined_rows"].append(i)
        else:
            difference = a - b
            comparison["gain_difference"].append(difference)
            name = (
                "canonical_lower_rows"
                if difference < 0
                else "geometric_lower_rows"
                if difference > 0
                else "tied_rows"
            )
            comparison[name].append(i)
    lists = [
        comparison[k]
        for k in ("canonical_lower_rows", "geometric_lower_rows", "tied_rows", "undefined_rows")
    ]
    q, m = len(scales), len(observations)
    _require(
        sorted(i for rows in lists for i in rows) == list(range(q)),
        "gain comparison does not partition every response",
    )
    d = sum(scale > 0 for scale in scales)
    counts = {
        "cells": len(cells),
        "positive_cells": sum(b is not None for _, b in cells),
        "tiles": len(tiles),
        "generators": n,
        "observations": m,
        "responses": q,
        "defined_responses": d,
        "undefined_responses": q - d,
        "transform_entries": 32 * len(tiles),
        "dimensionless_observation_entries": m * n,
        "dimensionless_target_entries": d * n,
        "raw_decoder_entries": 2 * q * (m + 1),
        "normalized_decoder_entries": 2 * d * (m + 1),
        "gain_entries": 2 * d,
        "witnesses": 2 * d,
        "witness_sign_entries": 2 * d * m,
        "witness_output_entries": 2 * d * d,
        "maximizing_rows": sum(len(decoder["max_rows"]) for decoder in decoders),
        "canonical_lower_rows": len(comparison["canonical_lower_rows"]),
        "geometric_lower_rows": len(comparison["geometric_lower_rows"]),
        "tied_rows": len(comparison["tied_rows"]),
    }
    return _detach(
        {
            "problem": problem,
            "geometry": {
                "volume": volume,
                "cell_volumes": cell_volumes,
                "tile_volumes": [_area(b) for _, b in tiles],
                "response_rows": [
                    {"first": a, "second": b} for (a, _), (b, _) in product(cells, repeat=2)
                ],
                "response_scales": scales,
            },
            "coordinates": {
                "raw_from_local": forward,
                "local_from_raw": inverse,
                "observations": local_observations,
                "targets": local_targets,
            },
            "decoders": decoders,
            "comparison": comparison,
            "checks": dict.fromkeys(
                (
                    "raw_response_identity",
                    "coordinate_inverse",
                    "normalized_response_identity",
                    "witness_box",
                    "witness_attainment",
                    "complete_gain_partition",
                ),
                True,
            ),
            "counts": counts,
        }
    )
