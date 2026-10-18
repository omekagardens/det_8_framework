"""Exact source-portability diagnostic for two inherited coarse-response maps.

New Bernstein fields are integrated from their supporting geometry. The raw
policies are authenticated and applied unchanged, never selected or fitted.
"""

import json
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd

LINEAR = ((0, 0), (1, 0), (0, 1), (1, 1))
QUADRATIC = tuple(product(range(3), repeat=2))
MOMENT_POWERS = tuple(product(range(4), repeat=2))


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


def _area(bounds):
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _contains(a, b):
    return a[0] <= b[0] and b[1] <= a[1] and a[2] <= b[2] and b[3] <= a[3]


def _overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def _cell_shapes(value):
    _require(type(value) is list and 1 <= len(value) <= 8, "bounded cell inventory required")
    for row in value:
        _fields(row, ("event", "bounds"))
        _require(type(row["event"]) is int, "native cell ID required")
        if row["bounds"] is not None:
            _rectangle_shape(row["bounds"])
    ids = [row["event"] for row in value]
    _require(ids == sorted(set(ids)), "sorted unique cell IDs required")


def _tile_shapes(value, fine, coarse_count):
    _require(type(value) is list and 1 <= len(value) <= 64, "bounded tile inventory required")
    for row in value:
        _fields(row, ("event", "bounds", "coarse_tile") if fine else ("event", "bounds"))
        _require(type(row["event"]) is int, "native tile owner required")
        _rectangle_shape(row["bounds"])
        if fine:
            _require(
                type(row["coarse_tile"]) is int and 0 <= row["coarse_tile"] < coarse_count,
                "global coarse-tile index invalid",
            )


def _preflight(problem):
    """Admit every container and matrix dimension before geometric arithmetic."""
    _native(problem)
    _fields(
        problem,
        (
            "family",
            "probe",
            "coarse_cells",
            "fine_cells",
            "coarse_tiles",
            "fine_tiles",
            "old_observations",
            "old_targets",
            "canonical",
            "geometric",
        ),
    )
    _require(type(problem["family"]) is str and problem["family"], "nonempty family required")
    _rectangle_shape(problem["probe"])
    _cell_shapes(problem["coarse_cells"])
    _cell_shapes(problem["fine_cells"])
    _tile_shapes(problem["coarse_tiles"], False, 0)
    _tile_shapes(problem["fine_tiles"], True, len(problem["coarse_tiles"]))
    m, q = 4 * len(problem["coarse_tiles"]), len(problem["coarse_cells"]) ** 2
    old = problem["old_observations"]
    _require(type(old) is list and len(old) == m and type(old[0]) is list, "old observation rows")
    n = len(old[0])
    _require(1 <= n <= 64, "bounded old generator count required")
    _matrix_shape(old, m, n)
    _matrix_shape(problem["old_targets"], q, n)
    _fields(problem["canonical"], ("row_basis", "decoder"))
    basis = problem["canonical"]["row_basis"]
    _require(
        type(basis) is list and 1 <= len(basis) <= 64 and all(type(i) is int for i in basis),
        "bounded native decoder basis required",
    )
    _require(
        basis == sorted(set(basis)) and basis[0] == 0 and basis[-1] <= m,
        "normalization-first in-range decoder basis required",
    )
    _matrix_shape(problem["canonical"]["decoder"], q, len(basis))
    _matrix_shape(problem["geometric"], q, m)
    return m, n, q


def _cells(rows):
    return [
        (row["event"], _rectangle(row["bounds"]) if row["bounds"] is not None else None)
        for row in rows
    ]


def _partition(cells, probe):
    positive = [b for _, b in cells if b is not None]
    _require(all(_contains(probe, b) for b in positive), "cell outside clipped probe")
    _require(all(not _overlap(a, b) for a, b in combinations(positive, 2)), "cells overlap")
    _require(sum((_area(b) for b in positive), F(0)) == _area(probe), "cells do not cover probe")


def _tile_partition(tiles, cells):
    by_id = dict(cells)
    keys = [(e, b[0], b[2], b[1], b[3]) for e, b in tiles]
    _require(keys == sorted(keys), "tile order differs")
    _require(
        all(e in by_id and by_id[e] is not None and _contains(by_id[e], b) for e, b in tiles),
        "tile lacks positive containing owner",
    )
    _require(all(not _overlap(a[1], b[1]) for a, b in combinations(tiles, 2)), "tiles overlap")
    for event, bounds in cells:
        volume = _area(bounds) if bounds is not None else F(0)
        _require(
            sum((_area(b) for e, b in tiles if e == event), F(0)) == volume,
            "tiles do not cover their cell",
        )


def _parse(problem):
    m, n, q = _preflight(problem)
    probe = _rectangle(problem["probe"])
    coarse, fine = _cells(problem["coarse_cells"]), _cells(problem["fine_cells"])
    ct = [(row["event"], _rectangle(row["bounds"])) for row in problem["coarse_tiles"]]
    ft = [(row["event"], _rectangle(row["bounds"])) for row in problem["fine_tiles"]]
    links = [row["coarse_tile"] for row in problem["fine_tiles"]]
    old_o, old_q = _matrix(problem["old_observations"]), _matrix(problem["old_targets"])
    compact, geometric = _matrix(problem["canonical"]["decoder"]), _matrix(problem["geometric"])
    _partition(coarse, probe)
    _partition(fine, probe)
    parents = {}
    for event, bounds in fine:
        if bounds is None:
            parents[event] = None
            continue
        matches = [e for e, b in coarse if b is not None and _contains(b, bounds)]
        _require(len(matches) == 1, "positive fine cell lacks unique containing coarse cell")
        parents[event] = matches[0]
    for event, bounds in coarse:
        expected = _area(bounds) if bounds is not None else F(0)
        _require(
            sum((_area(b) for e, b in fine if b is not None and parents[e] == event), F(0))
            == expected,
            "fine cells do not cover each coarse cell",
        )
    _tile_partition(ct, coarse)
    _tile_partition(ft, fine)
    for (event, bounds), index in zip(ft, links, strict=True):
        _require(
            ct[index][0] == parents[event] and _contains(ct[index][1], bounds),
            "fine tile disagrees with coarse-tile ownership",
        )
    for index, (_, bounds) in enumerate(ct):
        _require(
            sum((_area(b) for (_, b), link in zip(ft, links, strict=True) if link == index), F(0))
            == _area(bounds),
            "fine tiles do not cover each coarse tile",
        )
    a = [F(0)] * q
    linear = [[F(0)] * m for _ in range(q)]
    for j, row in enumerate(compact):
        for index, coefficient in zip(problem["canonical"]["row_basis"], row, strict=True):
            if index:
                linear[j][index - 1] = coefficient
            else:
                a[j] = coefficient
    raw = [("canonical", a, linear), ("geometric", [F(0)] * q, geometric)]
    for _, intercept, matrix in raw:
        values = _mm(matrix, old_o)
        _require(
            all([intercept[j] + x for x in row] == old_q[j] for j, row in enumerate(values)),
            "inherited old response identity failed",
        )
    volume = _area(probe)
    cv = [_area(b) if b is not None else F(0) for _, b in coarse]
    scales = [volume**2 * c * d for c, d in product(cv, repeat=2)]
    _require(
        all(s != 0 or all(x == 0 for x in row) for s, row in zip(scales, old_q, strict=True)),
        "empty response label has nonzero old target",
    )
    return probe, coarse, fine, ct, ft, links, parents, raw, volume, scales, n


def _moments(bounds):
    u, U, v, V = bounds
    left = [(U ** (p + 1) - u ** (p + 1)) / (p + 1) for p in range(4)]
    right = [(V ** (p + 1) - v ** (p + 1)) / (p + 1) for p in range(4)]
    return [a * b / 2 for a, b in product(left, right)]


def _tail(a, b, lo, hi):
    if hi <= a:
        return [b - a, F(0)]
    if lo >= b:
        return [F(0), F(0)]
    _require(not lo < a < hi and not lo < b < hi, "active outgoing knot lies inside tile")
    _require(a <= lo and hi <= b, "outgoing branch not resolved")
    return [b, F(-1)]


def _outgoing(endpoint, tile):
    if endpoint is None or tile[0] >= endpoint[1] or tile[2] >= endpoint[3]:
        return [F(0)] * 4
    u = _tail(endpoint[0], endpoint[1], tile[0], tile[1])
    v = _tail(endpoint[2], endpoint[3], tile[2], tile[3])
    return [u[i] * v[j] / 2 for i, j in LINEAR]


def _bernstein(a, b):
    denominator = (b - a) ** 2
    return [
        [b**2 / denominator, -2 * b / denominator, 1 / denominator],
        [-2 * a * b / denominator, 2 * (a + b) / denominator, -2 / denominator],
        [a**2 / denominator, -2 * a / denominator, 1 / denominator],
    ]


def _weighted(coefficients, power, moments):
    r, s = power
    return sum(
        (
            a * moments[4 * (p + r) + q + s]
            for a, (p, q) in zip(coefficients, QUADRATIC, strict=True)
            if a
        ),
        F(0),
    )


def _response(coefficients, outgoing, moments):
    return sum(
        (
            a * b * moments[4 * (p + r) + q + s]
            for a, (p, q) in zip(coefficients, QUADRATIC, strict=True)
            for b, (r, s) in zip(outgoing, LINEAR, strict=True)
            if a and b
        ),
        F(0),
    )


def _row_bounds(values):
    lo, hi = min(values), max(values)
    magnitude = max(map(abs, values))
    return {
        "minimum": lo,
        "minimum_generators": [i for i, x in enumerate(values) if x == lo],
        "maximum": hi,
        "maximum_generators": [i for i, x in enumerate(values) if x == hi],
        "max_abs": magnitude,
        "max_abs_generators": [i for i, x in enumerate(values) if abs(x) == magnitude],
    }


def _policy(name, intercept, matrix, observations, targets, scales):
    predicted = [[intercept[j] + x for x in row] for j, row in enumerate(_mm(matrix, observations))]
    residuals = [
        [x - y for x, y in zip(a, b, strict=True)] for a, b in zip(predicted, targets, strict=True)
    ]
    normalized = [
        [x / s for x in row] if s else None for row, s in zip(residuals, scales, strict=True)
    ]
    n = len(observations[0])
    failed_rows = [j for j, row in enumerate(residuals) if any(row)]
    failed_generators = [g for g in range(n) if any(row[g] for row in residuals)]
    nonzero = sum(x != 0 for row in residuals for x in row)
    bounds = [_row_bounds(row) if row is not None else None for row in normalized]
    witness = None
    if failed_generators:
        g = failed_generators[0]
        j = next(i for i, row in enumerate(residuals) if row[g])
        weights = [F(i == g) for i in range(n)]
        observed = [row[g] for row in observations]
        truth = [row[g] for row in targets]
        forecast = [row[g] for row in predicted]
        errors = [row[g] for row in residuals]
        normalized_errors = [None if row is None else row[g] for row in normalized]
        _require(all(x >= 0 for x in weights) and sum(weights, F(0)) == 1, "witness not simplex")
        _require([i for i, x in enumerate(weights) if x] == [g], "witness support differs")
        _require(
            observed == [_dot(row, weights) for row in observations], "witness observations differ"
        )
        _require(truth == [_dot(row, weights) for row in targets], "witness truth differs")
        _require(
            forecast == [a + _dot(row, observed) for a, row in zip(intercept, matrix, strict=True)],
            "witness frozen prediction differs",
        )
        _require(
            errors == [x - y for x, y in zip(forecast, truth, strict=True)] and errors[j] != 0,
            "witness residual differs",
        )
        _require(
            normalized_errors
            == [x / s if s else None for x, s in zip(errors, scales, strict=True)],
            "witness normalization differs",
        )
        witness = {
            "generator": g,
            "separating_row": j,
            "weights": weights,
            "observed": observed,
            "truth": truth,
            "predicted": forecast,
            "residual": errors,
            "normalized_residual": normalized_errors,
        }
    return {
        "name": name,
        "intercept": list(intercept),
        "matrix": [list(row) for row in matrix],
        "predicted": predicted,
        "residuals": residuals,
        "normalized_residuals": normalized,
        "exact": not failed_rows,
        "nonzero_entries": nonzero,
        "failed_rows": failed_rows,
        "failed_generators": failed_generators,
        "row_bounds": bounds,
        "witness": witness,
    }


def apply(intercept, matrix, observed):
    """Apply only the supplied dense raw affine map; no null or hidden model rows."""
    _native([intercept, matrix, observed])
    _require(type(intercept) is list and 1 <= len(intercept) <= 64, "bounded output rows required")
    _require(
        type(observed) is list and 0 < len(observed) <= 256 and len(observed) % 4 == 0,
        "bounded four-moment observation blocks required",
    )
    _matrix_shape(matrix, len(intercept), len(observed))
    a, linear, x = list(map(_fraction, intercept)), _matrix(matrix), list(map(_fraction, observed))
    return _detach([b + _dot(row, x) for b, row in zip(a, linear, strict=True)])


def build_family(problem):
    """Integrate a larger nonnegative dictionary and test unchanged response maps."""
    _, coarse, fine, ct, ft, links, parents, raw, volume, scales, old_n = _parse(problem)
    cm, fm = [_moments(b) for _, b in ct], [_moments(b) for _, b in ft]
    outgoing = [[_outgoing(b, tile) for _, b in coarse] for _, tile in ct]
    cids = [e for e, _ in coarse]
    response_rows = [{"first": c, "second": d} for c, d in product(cids, repeat=2)]
    derived_geometric = [
        [
            x
            for t, (owner, _) in enumerate(ct)
            for x in (outgoing[t][j] if owner == c else [F(0)] * 4)
        ]
        for c in cids
        for j in range(len(coarse))
    ]
    _require(derived_geometric == raw[1][2], "inherited geometric policy differs from geometry")
    for t, expected in enumerate(cm):
        summed = [
            sum((row[p] for row, link in zip(fm, links, strict=True) if link == t), F(0))
            for p in range(16)
        ]
        _require(summed == expected, "coarse/fine moment additivity failed")
    n, m, q = 9 * len(ft), 4 * len(ct), len(coarse) ** 2
    observations = [[F(0)] * n for _ in range(m)]
    targets = [[F(0)] * n for _ in range(q)]
    generators, integrals = [], []
    for t, ((_, bounds), moments, link) in enumerate(zip(ft, fm, links, strict=True)):
        bu, bv = _bernstein(bounds[0], bounds[1]), _bernstein(bounds[2], bounds[3])
        direct_outgoing = [_outgoing(b, bounds) for _, b in coarse]
        coefficients_for_tile = []
        for i, j in product(range(3), repeat=2):
            coefficients = [volume**2 * bu[i][p] * bv[j][r] for p, r in QUADRATIC]
            coefficients_for_tile.append(coefficients)
            g = len(generators)
            generators.append({"tile": t, "i": i, "j": j, "coefficients": coefficients})
            local_observations = [_weighted(coefficients, power, moments) for power in LINEAR]
            integrals.append(local_observations[0])
            _require(
                local_observations[0] == volume**2 * _area(bounds) / 9,
                "Bernstein generator integral differs",
            )
            for basis, value in enumerate(local_observations):
                observations[4 * link + basis][g] = value
            owner = ct[link][0]
            for row, labels in enumerate(response_rows):
                if labels["first"] == owner:
                    targets[row][g] = _response(
                        coefficients, direct_outgoing[row % len(coarse)], moments
                    )
        coefficient_sum = [sum((row[p] for row in coefficients_for_tile), F(0)) for p in range(9)]
        _require(
            coefficient_sum == [volume**2] + [F(0)] * 8, "Bernstein polynomial partition failed"
        )
    constant_observations = [volume**2 * row[4 * p + r] for row in cm for p, r in LINEAR]
    constant_targets = [
        volume**2
        * sum(
            (
                _dot(outgoing[t][j], [cm[t][4 * p + r] for p, r in LINEAR])
                for t, (owner, _) in enumerate(ct)
                if owner == c
            ),
            F(0),
        )
        for c in cids
        for j in range(len(coarse))
    ]
    _require(
        [sum(row, F(0)) for row in observations] == constant_observations,
        "constant-field observations differ",
    )
    _require(
        [sum(row, F(0)) for row in targets] == constant_targets, "constant-field responses differ"
    )
    _require(sum(integrals, F(0)) == volume**3, "constant source total integral differs")
    decoders = [_policy(name, a, linear, observations, targets, scales) for name, a, linear in raw]
    _require(decoders[1]["exact"], "structural geometric portability failed")
    d = sum(s > 0 for s in scales)
    witness_count = sum(row["witness"] is not None for row in decoders)
    bound_indices = sum(
        len(bound[key])
        for decoder in decoders
        for bound in decoder["row_bounds"]
        if bound is not None
        for key in ("minimum_generators", "maximum_generators", "max_abs_generators")
    )
    counts = {
        "coarse_cells": len(coarse),
        "fine_cells": len(fine),
        "positive_coarse_cells": sum(b is not None for _, b in coarse),
        "positive_fine_cells": sum(b is not None for _, b in fine),
        "coarse_tiles": len(ct),
        "fine_tiles": len(ft),
        "old_generators": old_n,
        "new_generators": n,
        "observation_rows": m,
        "response_rows": q,
        "defined_response_rows": d,
        "undefined_response_rows": q - d,
        "coarse_moment_entries": 16 * len(ct),
        "fine_moment_entries": 16 * len(ft),
        "coarse_outgoing_entries": 4 * len(ct) * len(coarse),
        "source_coefficient_entries": 9 * n,
        "observation_entries": m * n,
        "target_entries": q * n,
        "generator_integral_entries": n,
        "constant_observation_entries": m,
        "constant_target_entries": q,
        "raw_decoder_entries": 2 * q * (m + 1),
        "prediction_entries": 2 * q * n,
        "residual_entries": 2 * q * n,
        "normalized_residual_entries": 2 * d * n,
        "nonzero_residual_entries": sum(row["nonzero_entries"] for row in decoders),
        "failed_rows": sum(len(row["failed_rows"]) for row in decoders),
        "failed_generators": sum(len(row["failed_generators"]) for row in decoders),
        "row_bound_entries": 6 * d,
        "bound_attainer_indices": bound_indices,
        "witnesses": witness_count,
        "witness_entries": witness_count * (n + m + 3 * q + d),
    }
    return _detach(
        {
            "problem": problem,
            "geometry": {
                "volume": volume,
                "coarse_cells": [
                    {
                        "event": e,
                        "bounds": list(b) if b is not None else None,
                        "volume": _area(b) if b is not None else F(0),
                    }
                    for e, b in coarse
                ],
                "fine_cells": [
                    {
                        "event": e,
                        "bounds": list(b) if b is not None else None,
                        "volume": _area(b) if b is not None else F(0),
                    }
                    for e, b in fine
                ],
                "parents": [{"event": e, "parent": parents[e]} for e, _ in fine],
                "coarse_tiles": [
                    {
                        "event": e,
                        "bounds": list(b),
                        "moments": moments,
                        "outgoing": [
                            {"event": d, "coefficients": coefficients}
                            for (d, _), coefficients in zip(coarse, outs, strict=True)
                        ],
                    }
                    for (e, b), moments, outs in zip(ct, cm, outgoing, strict=True)
                ],
                "fine_tiles": [
                    {"event": e, "bounds": list(b), "coarse_tile": link, "moments": moments}
                    for (e, b), link, moments in zip(ft, links, fm, strict=True)
                ],
                "response_scales": scales,
            },
            "generators": generators,
            "matrices": {
                "observation_rows": [
                    {"tile": t, "basis": j} for t in range(len(ct)) for j in range(4)
                ],
                "response_rows": response_rows,
                "observations": observations,
                "targets": targets,
                "generator_integrals": integrals,
                "constant_observations": constant_observations,
                "constant_targets": constant_targets,
            },
            "decoders": decoders,
            "checks": dict.fromkeys(
                (
                    "old_response_identities",
                    "geometric_policy_authenticated",
                    "moment_additivity",
                    "bernstein_partition",
                    "generator_integrals",
                    "constant_field_observations",
                    "constant_field_responses",
                    "geometric_portability",
                    "witnesses_valid",
                ),
                True,
            ),
            "counts": counts,
        }
    )
