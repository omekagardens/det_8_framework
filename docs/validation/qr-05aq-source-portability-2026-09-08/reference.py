"""QR-05AQ reference: interpolated fields and direct Simpson integration.

No decoder fitting, external reads, historical executors or coefficient/moment
contraction is used to obtain the new measurements and true responses.
"""

from copy import deepcopy
from fractions import Fraction
from itertools import pairwise, product
from math import gcd

MAX_BITS = 4096
ZERO = Fraction(0)
ONE = Fraction(1)
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))


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


def _rectangle(value):
    _need(type(value) is list and len(value) == 4, "rectangle bounds")
    bounds = tuple(_fraction(x) for x in value)
    _need(bounds[0] < bounds[1] and bounds[2] < bounds[3], "positive rectangle")
    return bounds


def _area(bounds):
    if bounds is None:
        return ZERO
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _inside(inner, outer):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def _overlap(left, right):
    if left is None or right is None:
        return False
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


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
    return sum((a * b for a, b in zip(row, vector)), ZERO)


def apply(intercept, matrix, observed):
    """Apply only the supplied dense RAW affine map; raw rows are never null."""
    _native(intercept)
    _native(matrix)
    _native(observed)
    _need(type(intercept) is list and 1 <= len(intercept) <= 64, "output rows")
    _need(
        type(observed) is list and 4 <= len(observed) <= 256 and len(observed) % 4 == 0,
        "observation width",
    )
    _dimensions(matrix, len(intercept), len(observed))
    a, x, rows = (
        [_fraction(v) for v in intercept],
        [_fraction(v) for v in observed],
        _matrix(matrix),
    )
    return _wire([b + _dot(row, x) for b, row in zip(a, rows)])


def _cell_partition(rows, probe):
    cells = [(r["event"], None if r["bounds"] is None else _rectangle(r["bounds"])) for r in rows]
    ids = [event for event, _ in cells]
    _need(ids == sorted(set(ids)), "sorted unique cell IDs")
    for index, (_, bounds) in enumerate(cells):
        if bounds is not None:
            _need(_inside(bounds, probe), "cell inside probe")
            _need(
                all(not _overlap(bounds, other) for _, other in cells[index + 1 :]),
                "disjoint cell interiors",
            )
    _need(sum((_area(b) for _, b in cells), ZERO) == _area(probe), "cell coverage")
    return cells


def _tile_partition(rows, cells):
    cell_map = dict(cells)
    tiles = [(row["event"], _rectangle(row["bounds"])) for row in rows]
    keys = [(event, b[0], b[2], b[1], b[3]) for event, b in tiles]
    _need(keys == sorted(keys), "tile ordering")
    for index, (event, bounds) in enumerate(tiles):
        _need(event in cell_map and cell_map[event] is not None, "positive tile owner")
        _need(_inside(bounds, cell_map[event]), "tile within cell")
        _need(
            all(not _overlap(bounds, other) for _, other in tiles[index + 1 :]),
            "disjoint tile interiors",
        )
    for event, bounds in cells:
        _need(
            sum((_area(b) for owner, b in tiles if owner == event), ZERO) == _area(bounds),
            "tile coverage",
        )
    return tiles


def _parse(problem):
    _native(problem)
    _keys(
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
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    for key in ("coarse_cells", "fine_cells"):
        _need(type(problem[key]) is list and 1 <= len(problem[key]) <= 8, "cell inventory")
        for row in problem[key]:
            _keys(row, ("event", "bounds"))
            _need(type(row["event"]) is int, "cell event ID")
    for key in ("coarse_tiles", "fine_tiles"):
        _need(type(problem[key]) is list and 1 <= len(problem[key]) <= 64, "tile inventory")
        for row in problem[key]:
            _keys(
                row,
                ("event", "bounds")
                if key == "coarse_tiles"
                else ("event", "bounds", "coarse_tile"),
            )
            _need(type(row["event"]) is int, "tile event ID")
    c, t = len(problem["coarse_cells"]), len(problem["coarse_tiles"])
    m, q = 4 * t, c * c
    for row in problem["fine_tiles"]:
        _need(type(row["coarse_tile"]) is int and 0 <= row["coarse_tile"] < t, "coarse tile index")
    old_o = problem["old_observations"]
    _need(
        type(old_o) is list and len(old_o) == m and type(old_o[0]) is list, "old observation rows"
    )
    n = len(old_o[0])
    _need(1 <= n <= 64, "old generator count")
    _dimensions(old_o, m, n)
    _dimensions(problem["old_targets"], q, n)
    _dimensions(problem["geometric"], q, m)
    _keys(problem["canonical"], ("row_basis", "decoder"))
    basis = problem["canonical"]["row_basis"]
    _need(
        type(basis) is list and 1 <= len(basis) <= 64 and all(type(i) is int for i in basis),
        "basis types",
    )
    _need(basis == sorted(set(basis)) and basis[0] == 0 and basis[-1] <= m, "canonical basis")
    _dimensions(problem["canonical"]["decoder"], q, len(basis))
    # Every shape and public inventory cap is admitted before geometry/integration.
    probe = _rectangle(problem["probe"])
    coarse = _cell_partition(problem["coarse_cells"], probe)
    fine = _cell_partition(problem["fine_cells"], probe)
    parents = {}
    for event, bounds in fine:
        possible = [
            owner
            for owner, cb in coarse
            if cb is not None and bounds is not None and _inside(bounds, cb)
        ]
        _need(bounds is None or len(possible) == 1, "unique clipped fine parent")
        parents[event] = None if bounds is None else possible[0]
    for event, bounds in coarse:
        _need(
            sum((_area(b) for owner, b in fine if parents[owner] == event), ZERO) == _area(bounds),
            "fine cell parent coverage",
        )
    coarse_tiles = _tile_partition(problem["coarse_tiles"], coarse)
    fine_tiles = _tile_partition(problem["fine_tiles"], fine)
    ownership = [row["coarse_tile"] for row in problem["fine_tiles"]]
    for (event, bounds), index in zip(fine_tiles, ownership):
        owner, cb = coarse_tiles[index]
        _need(parents[event] == owner and _inside(bounds, cb), "fine tile coarse ownership")
    for index, (_, bounds) in enumerate(coarse_tiles):
        _need(
            sum((_area(b) for (_, b), owner in zip(fine_tiles, ownership) if owner == index), ZERO)
            == _area(bounds),
            "fine coverage of coarse tile",
        )
    old_o = _matrix(old_o)
    old_q = _matrix(problem["old_targets"])
    compact, geometric = _matrix(problem["canonical"]["decoder"]), _matrix(problem["geometric"])
    a, linear = [ZERO] * q, [[ZERO] * m for _ in range(q)]
    for row, entries in enumerate(compact):
        for index, entry in zip(basis, entries):
            if index == 0:
                a[row] = entry
            else:
                linear[row][index - 1] = entry
    for row, (first, second) in enumerate(product(coarse, repeat=2)):
        if first[1] is None or second[1] is None:
            _need(all(x == 0 for x in old_q[row]), "empty old response")
    for intercept, matrix in ((a, linear), ([ZERO] * q, geometric)):
        for row in range(q):
            for column in range(n):
                value = intercept[row] + sum(
                    (matrix[row][j] * old_o[j][column] for j in range(m)), ZERO
                )
                _need(value == old_q[row][column], "old response identity")
    return (
        probe,
        coarse,
        fine,
        coarse_tiles,
        fine_tiles,
        parents,
        ownership,
        old_o,
        a,
        linear,
        geometric,
    )


def _nodes(lo, hi, knots=()):
    cuts = sorted({lo, hi, *(x for x in knots if lo < x < hi)})
    result = {}
    for left, right in pairwise(cuts):
        width = (right - left) / 6
        for x, factor in ((left, 1), ((left + right) / 2, 4), (right, 1)):
            result[x] = result.get(x, ZERO) + factor * width
    return tuple(result.items())


def _integral(bounds, function, outgoing=None):
    """Exact on each cubic piece; evaluate the support polynomial at endpoints."""
    if bounds is None:
        return ZERO
    uk, vk = ((), ()) if outgoing is None else (outgoing[:2], outgoing[2:])
    un, vn = _nodes(bounds[0], bounds[1], uk), _nodes(bounds[2], bounds[3], vk)
    return sum((wu * wv * function(u, v) / 2 for u, wu in un for v, wv in vn), ZERO)


def _moments(bounds):
    return [
        _integral(bounds, lambda u, v, i=i, j=j: u**i * v**j) for i in range(4) for j in range(4)
    ]


def _tail(x, lo, hi):
    return max(ZERO, min(hi - lo, hi - x))


def _response(bounds, u, v):
    if bounds is None:
        return ZERO
    return _tail(u, bounds[0], bounds[1]) * _tail(v, bounds[2], bounds[3]) / 2


def _outgoing(tile, destination):
    if destination is None:
        return [ZERO] * 4
    if tile[0] >= destination[1] or tile[2] >= destination[3]:
        return [ZERO] * 4
    _need(
        all(not tile[0] < x < tile[1] for x in destination[:2])
        and all(not tile[2] < x < tile[3] for x in destination[2:]),
        "active outgoing knot inside coarse tile",
    )
    u0, u1, v0, v1 = tile
    f00, f10, f01, f11 = (
        _response(destination, u, v) for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))
    )
    cross = (f11 - f10 - f01 + f00) / ((u1 - u0) * (v1 - v0))
    cu = (f10 - f00) / (u1 - u0) - cross * v0
    cv = (f01 - f00) / (v1 - v0) - cross * u0
    coefficients = [f00 - cu * u0 - cv * v0 - cross * u0 * v0, cu, cv, cross]
    for u, v in product((u0, (u0 + u1) / 2, u1), (v0, (v0 + v1) / 2, v1)):
        _need(
            _dot(coefficients, [ONE, u, v, u * v]) == _response(destination, u, v),
            "outgoing corner interpolation",
        )
    return coefficients


def _bernstein(index, x):
    if index == 0:
        return (1 - x) ** 2
    if index == 1:
        return 2 * x * (1 - x)
    return x * x


def _source(bounds, i, j, amplitude, u, v):
    # Deliberately the polynomial extension, NOT a boundary-zeroed indicator.
    return (
        amplitude
        * _bernstein(i, (u - bounds[0]) / (bounds[1] - bounds[0]))
        * _bernstein(j, (v - bounds[2]) / (bounds[3] - bounds[2]))
    )


def _quadratic(nodes, values):
    x0, x1, x2 = nodes
    y0, y1, y2 = values
    first = (y1 - y0) / (x1 - x0)
    second = ((y2 - y1) / (x2 - x1) - first) / (x2 - x0)
    return [y0 - first * x0 + second * x0 * x1, first - second * (x0 + x1), second]


def _source_coefficients(bounds, i, j, amplitude):
    us = (bounds[0], (bounds[0] + bounds[1]) / 2, bounds[1])
    vs = (bounds[2], (bounds[2] + bounds[3]) / 2, bounds[3])
    along_u = [_quadratic(us, [_source(bounds, i, j, amplitude, u, v) for u in us]) for v in vs]
    coefficients = [x for p in range(3) for x in _quadratic(vs, [row[p] for row in along_u])]
    for u, v in product(us, vs):
        actual = sum(
            (coefficients[3 * p + q] * u**p * v**q for p in range(3) for q in range(3)), ZERO
        )
        _need(actual == _source(bounds, i, j, amplitude, u, v), "source interpolation")
    return coefficients


def _policy(name, intercept, matrix, observations, truth, scales):
    q, n = len(truth), len(truth[0])
    columns = list(zip(*observations))
    predicted = [[intercept[r] + _dot(matrix[r], column) for column in columns] for r in range(q)]
    residual = [[a - b for a, b in zip(row, target)] for row, target in zip(predicted, truth)]
    normalized = [
        None if scale == 0 else [x / scale for x in row] for row, scale in zip(residual, scales)
    ]
    failed_rows = [r for r, row in enumerate(residual) if any(x != 0 for x in row)]
    failed_generators = [g for g in range(n) if any(residual[r][g] != 0 for r in range(q))]
    bounds = []
    for row in normalized:
        if row is None:
            bounds.append(None)
            continue
        minimum, maximum, max_abs = min(row), max(row), max(abs(x) for x in row)
        bounds.append(
            {
                "minimum": minimum,
                "minimum_generators": [g for g, x in enumerate(row) if x == minimum],
                "maximum": maximum,
                "maximum_generators": [g for g, x in enumerate(row) if x == maximum],
                "max_abs": max_abs,
                "max_abs_generators": [g for g, x in enumerate(row) if abs(x) == max_abs],
            }
        )
    witness = None
    if failed_generators:
        generator = failed_generators[0]
        row = next(r for r in range(q) if residual[r][generator] != 0)
        weights = [ONE if j == generator else ZERO for j in range(n)]
        observed = [_dot(measurement, weights) for measurement in observations]
        actual_truth = [_dot(response, weights) for response in truth]
        actual_prediction = [a + _dot(linear, observed) for a, linear in zip(intercept, matrix)]
        actual_residual = [a - b for a, b in zip(actual_prediction, actual_truth)]
        actual_normalized = [
            None if scale == 0 else x / scale for x, scale in zip(actual_residual, scales)
        ]
        _need(sum(weights, ZERO) == 1 and all(x >= 0 for x in weights), "simplex witness")
        _need([j for j, x in enumerate(weights) if x != 0] == [generator], "unit witness support")
        _need(observed == list(columns[generator]), "witness observations")
        _need(actual_truth == [r[generator] for r in truth], "witness truth")
        _need(actual_prediction == [r[generator] for r in predicted], "witness prediction")
        _need(actual_residual == [r[generator] for r in residual], "witness residual")
        _need(
            actual_normalized == [None if r is None else r[generator] for r in normalized],
            "witness normalization",
        )
        _need(
            row == next(r for r, x in enumerate(actual_residual) if x != 0), "first detecting row"
        )
        witness = {
            "generator": generator,
            "separating_row": row,
            "weights": weights,
            "observed": observed,
            "truth": actual_truth,
            "predicted": actual_prediction,
            "residual": actual_residual,
            "normalized_residual": actual_normalized,
        }
    return {
        "name": name,
        "intercept": intercept,
        "matrix": matrix,
        "predicted": predicted,
        "residuals": residual,
        "normalized_residuals": normalized,
        "exact": not failed_rows,
        "nonzero_entries": sum(x != 0 for row in residual for x in row),
        "failed_rows": failed_rows,
        "failed_generators": failed_generators,
        "row_bounds": bounds,
        "witness": witness,
    }


def build_family(problem):
    """Build a complete certificate from supplied geometry and frozen maps."""
    probe, coarse, fine, ct, ft, parents, ownership, old_o, a, linear, geometric = _parse(problem)
    c, t, f = len(coarse), len(ct), len(ft)
    m, q, n = 4 * t, c * c, 9 * f
    volume, amplitude = _area(probe), _area(probe) ** 2
    cm, fm = [_moments(b) for _, b in ct], [_moments(b) for _, b in ft]
    outgoing = [[_outgoing(b, d) for _, d in coarse] for _, b in ct]
    for tile in range(t):
        for exponent in range(16):
            _need(
                cm[tile][exponent]
                == sum(
                    (fm[j][exponent] for j, owner in enumerate(ownership) if owner == tile), ZERO
                ),
                "moment additivity",
            )
    reconstructed = [[ZERO] * m for _ in range(q)]
    for r, ((first, _), _) in enumerate(product(coarse, repeat=2)):
        for tile, (owner, _) in enumerate(ct):
            if owner == first:
                reconstructed[r][4 * tile : 4 * tile + 4] = outgoing[tile][r % c]
    _need(reconstructed == geometric, "entire structural geometric policy")
    observations, targets = [[ZERO] * n for _ in range(m)], [[ZERO] * n for _ in range(q)]
    generators, integrals = [], []
    coarse_index = {event: index for index, (event, _) in enumerate(coarse)}
    for tile, (event, bounds) in enumerate(ft):
        owner_tile = ownership[tile]
        first = coarse_index[parents[event]]
        local_coefficients = []
        for i, j in product(range(3), repeat=2):
            column = len(generators)
            coefficients = _source_coefficients(bounds, i, j, amplitude)
            local_coefficients.append(coefficients)
            generators.append({"tile": tile, "i": i, "j": j, "coefficients": coefficients})

            def field(u, v, bounds=bounds, i=i, j=j):
                return _source(bounds, i, j, amplitude, u, v)

            for basis, (p, r) in enumerate(BASIS):
                observations[4 * owner_tile + basis][column] = _integral(
                    bounds, lambda u, v, p=p, r=r: field(u, v) * u**p * v**r
                )
            integral = _integral(bounds, field)
            _need(integral == amplitude * _area(bounds) / 9, "generator integral")
            integrals.append(integral)
            for second, (_, destination) in enumerate(coarse):
                targets[first * c + second][column] = _integral(
                    bounds,
                    lambda u, v, d=destination: field(u, v) * _response(d, u, v),
                    destination,
                )
        partition = [sum((row[k] for row in local_coefficients), ZERO) for k in range(9)]
        _need(partition == [amplitude] + [ZERO] * 8, "complete coefficient partition")
        for x in (ZERO, Fraction(1, 3), Fraction(1, 2), ONE):
            factors = [_bernstein(i, x) for i in range(3)]
            _need(
                all(value >= 0 for value in factors) and sum(factors, ZERO) == 1,
                "Bernstein factors",
            )
    constant_o = [
        amplitude * _integral(b, lambda u, v, p=p, r=r: u**p * v**r)
        for _, b in ct
        for p, r in BASIS
    ]
    constant_q = [
        amplitude * _integral(cb, lambda u, v, d=db: _response(d, u, v), db)
        for (_, cb), (_, db) in product(coarse, repeat=2)
    ]
    _need(constant_o == [sum(row, ZERO) for row in observations], "constant observations")
    _need(constant_q == [sum(row, ZERO) for row in targets], "constant responses")
    _need(sum(integrals, ZERO) == volume**3, "unweighted dictionary integral")
    scales = [amplitude * _area(cb) * _area(db) for (_, cb), (_, db) in product(coarse, repeat=2)]
    policies = [
        _policy("canonical", a, linear, observations, targets, scales),
        _policy("geometric", [ZERO] * q, geometric, observations, targets, scales),
    ]
    _need(policies[1]["exact"], "geometric portability")
    defined = sum(scale != 0 for scale in scales)
    witnesses = sum(policy["witness"] is not None for policy in policies)
    counts = {
        "coarse_cells": c,
        "fine_cells": len(fine),
        "positive_coarse_cells": sum(b is not None for _, b in coarse),
        "positive_fine_cells": sum(b is not None for _, b in fine),
        "coarse_tiles": t,
        "fine_tiles": f,
        "old_generators": len(old_o[0]),
        "new_generators": n,
        "observation_rows": m,
        "response_rows": q,
        "defined_response_rows": defined,
        "undefined_response_rows": q - defined,
        "coarse_moment_entries": 16 * t,
        "fine_moment_entries": 16 * f,
        "coarse_outgoing_entries": 4 * t * c,
        "source_coefficient_entries": 9 * n,
        "observation_entries": m * n,
        "target_entries": q * n,
        "generator_integral_entries": n,
        "constant_observation_entries": m,
        "constant_target_entries": q,
        "raw_decoder_entries": 2 * q * (m + 1),
        "prediction_entries": 2 * q * n,
        "residual_entries": 2 * q * n,
        "normalized_residual_entries": 2 * defined * n,
        "nonzero_residual_entries": sum(p["nonzero_entries"] for p in policies),
        "failed_rows": sum(len(p["failed_rows"]) for p in policies),
        "failed_generators": sum(len(p["failed_generators"]) for p in policies),
        "row_bound_entries": 6 * defined,
        "bound_attainer_indices": sum(
            len(row[key])
            for p in policies
            for row in p["row_bounds"]
            if row is not None
            for key in ("minimum_generators", "maximum_generators", "max_abs_generators")
        ),
        "witnesses": witnesses,
        "witness_entries": witnesses * (n + m + 3 * q + defined),
    }
    return _wire(
        {
            "problem": deepcopy(problem),
            "geometry": {
                "volume": volume,
                "coarse_cells": [
                    {"event": event, "bounds": b, "volume": _area(b)} for event, b in coarse
                ],
                "fine_cells": [
                    {"event": event, "bounds": b, "volume": _area(b)} for event, b in fine
                ],
                "parents": [{"event": event, "parent": parents[event]} for event, _ in fine],
                "coarse_tiles": [
                    {
                        "event": event,
                        "bounds": b,
                        "moments": cm[tile],
                        "outgoing": [
                            {"event": d, "coefficients": coef}
                            for (d, _), coef in zip(coarse, outgoing[tile])
                        ],
                    }
                    for tile, (event, b) in enumerate(ct)
                ],
                "fine_tiles": [
                    {
                        "event": event,
                        "bounds": b,
                        "coarse_tile": ownership[tile],
                        "moments": fm[tile],
                    }
                    for tile, (event, b) in enumerate(ft)
                ],
                "response_scales": scales,
            },
            "generators": generators,
            "matrices": {
                "observation_rows": [
                    {"tile": tile, "basis": basis} for tile in range(t) for basis in range(4)
                ],
                "response_rows": [
                    {"first": first, "second": second}
                    for (first, _), (second, _) in product(coarse, repeat=2)
                ],
                "observations": observations,
                "targets": targets,
                "generator_integrals": integrals,
                "constant_observations": constant_o,
                "constant_targets": constant_q,
            },
            "decoders": policies,
            "checks": {
                name: True
                for name in (
                    "old_response_identities",
                    "geometric_policy_authenticated",
                    "moment_additivity",
                    "bernstein_partition",
                    "generator_integrals",
                    "constant_field_observations",
                    "constant_field_responses",
                    "geometric_portability",
                    "witnesses_valid",
                )
            },
            "counts": counts,
        }
    )
