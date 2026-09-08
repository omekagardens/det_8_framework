"""Exact fine-response sufficiency and explicit measurement-repair diagnostic."""

import json
from fractions import Fraction as F
from itertools import combinations, pairwise, product
from math import gcd

LINEAR = ((0, 0), (1, 0), (0, 1), (1, 1))
QUADRATIC = tuple(product(range(3), repeat=2))


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
    _require(
        all(type(coordinate) is list and len(coordinate) == 2 for coordinate in value),
        "native rectangle rational-pair shapes required",
    )


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
    _native(problem)
    _fields(
        problem, ("family", "probe", "coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles")
    )
    _require(type(problem["family"]) is str and problem["family"], "nonempty family required")
    _rectangle_shape(problem["probe"])
    _cell_shapes(problem["coarse_cells"])
    _cell_shapes(problem["fine_cells"])
    _tile_shapes(problem["coarse_tiles"], False, 0)
    _tile_shapes(problem["fine_tiles"], True, len(problem["coarse_tiles"]))


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
    _preflight(problem)
    probe = _rectangle(problem["probe"])
    coarse, fine = _cells(problem["coarse_cells"]), _cells(problem["fine_cells"])
    ct = [(x["event"], _rectangle(x["bounds"])) for x in problem["coarse_tiles"]]
    ft = [(x["event"], _rectangle(x["bounds"])) for x in problem["fine_tiles"]]
    links = [x["coarse_tile"] for x in problem["fine_tiles"]]
    _partition(coarse, probe)
    _partition(fine, probe)
    parents = {}
    for event, bounds in fine:
        candidates = [
            e for e, b in coarse if b is not None and bounds is not None and _contains(b, bounds)
        ]
        _require(bounds is None or len(candidates) == 1, "fine cell lacks unique clipped parent")
        parents[event] = candidates[0] if bounds is not None else None
    for event, bounds in coarse:
        _require(
            sum((_area(b) for e, b in fine if b is not None and parents[e] == event), F(0))
            == (_area(bounds) if bounds is not None else F(0)),
            "fine cells do not cover coarse parent",
        )
    _tile_partition(ct, coarse)
    _tile_partition(ft, fine)
    for (event, bounds), index in zip(ft, links, strict=True):
        _require(
            ct[index][0] == parents[event] and _contains(ct[index][1], bounds),
            "fine tile parent index/geometry differs",
        )
    for index, (_, bounds) in enumerate(ct):
        _require(
            sum((_area(b) for (_, b), link in zip(ft, links, strict=True) if link == index), F(0))
            == _area(bounds),
            "fine tiles do not cover coarse tile",
        )
    # Reserve the entire deterministic overlay before moments, integrations or matrices.
    axes = []
    total = 0
    for _, bounds in ft:
        u = sorted(
            {
                bounds[0],
                bounds[1],
                *[x for _, b in fine if b is not None for x in b[:2] if bounds[0] < x < bounds[1]],
            }
        )
        v = sorted(
            {
                bounds[2],
                bounds[3],
                *[x for _, b in fine if b is not None for x in b[2:] if bounds[2] < x < bounds[3]],
            }
        )
        total += (len(u) - 1) * (len(v) - 1)
        _require(total <= 256, "repair-piece cap exceeded")
        axes.append((u, v))
    repair = []
    for t, ((event, _), (u, v), coarse_index) in enumerate(zip(ft, axes, links, strict=True)):
        for a, b in pairwise(u):
            for c, d in pairwise(v):
                repair.append((event, (a, b, c, d), t, coarse_index))
    _require(len(repair) == total and total >= len(ft), "repair inventory differs")
    return probe, coarse, fine, ct, ft, links, parents, repair


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


def _row_basis(rows):
    """Greedy ORIGINAL row admission; an internal forward basis is only a test."""
    echelon = []
    indices = []
    for index, row in enumerate(rows):
        candidate = list(row)
        for pivot, basis in echelon:
            coefficient = candidate[pivot]
            if coefficient:
                candidate = [a - coefficient * b for a, b in zip(candidate, basis, strict=True)]
        nonzero = next((j for j, x in enumerate(candidate) if x), None)
        if nonzero is None:
            continue
        divisor = candidate[nonzero]
        candidate = [x / divisor for x in candidate]
        echelon.append((nonzero, candidate))
        echelon.sort(key=lambda pair: pair[0])
        indices.append(index)
    return indices


def _rref_with_transform(basis):
    rank = len(basis)
    n = len(basis[0])
    rows = [list(row) + [F(i == j) for j in range(rank)] for i, row in enumerate(basis)]
    pivots = []
    pivot_row = 0
    for column in range(n):
        selected = next((i for i in range(pivot_row, rank) if rows[i][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [x / divisor for x in rows[pivot_row]]
        for i in range(rank):
            if i != pivot_row and rows[i][column]:
                coefficient = rows[i][column]
                rows[i] = [
                    x - coefficient * y for x, y in zip(rows[i], rows[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rank:
            break
    _require(pivot_row == rank, "selected basis is dependent")
    return [row[:n] for row in rows], [row[n:] for row in rows], pivots


def _certificate(observations, targets):
    n = len(targets[0])
    augmented = [[F(1)] * n] + observations
    indices = _row_basis(augmented)
    _require(indices and indices[0] == 0, "normalization row missing")
    basis = [augmented[i] for i in indices]
    reduced, transform, pivots = _rref_with_transform(basis)
    _require(_mm(transform, basis) == reduced, "row transform identity failed")
    free = [j for j in range(n) if j not in pivots]
    residuals = []
    decoders = []
    recovered = []
    failed = []
    for j, target in enumerate(targets):
        coordinates = [target[p] for p in pivots]
        approximation = _mm([coordinates], reduced)[0]
        residual = [a - b for a, b in zip(target, approximation, strict=True)]
        residuals.append(residual)
        if any(residual):
            decoders.append(None)
            failed.append(j)
        else:
            decoder = _mm([coordinates], transform)[0]
            _require(_mm([decoder], basis)[0] == target, "recovered row identity failed")
            decoders.append(decoder)
            recovered.append(j)
    target_rank = len(_row_basis(targets))
    joint_rank = len(indices) + len(_row_basis(residuals))
    _require(joint_rank == len(_row_basis(augmented + targets)), "joint rank inconsistency")
    _require((joint_rank == len(indices)) == (not failed), "membership/rank decisions differ")
    _require(
        sorted(recovered + failed) == list(range(len(targets))), "row membership inventory differs"
    )
    collision = None
    if failed:
        for free_column in free:
            vector = [F(0)] * n
            vector[free_column] = F(1)
            for pivot, row in zip(pivots, reduced, strict=True):
                vector[pivot] = -row[free_column]
            changes = [_dot(row, vector) for row in targets]
            if not any(changes):
                continue
            separating = next(j for j, x in enumerate(changes) if x)
            _require(all(_dot(row, vector) == 0 for row in augmented), "null vector failed")
            mass = sum((x for x in vector if x > 0), F(0))
            negative_mass = sum((-x for x in vector if x < 0), F(0))
            _require(mass == negative_mass and mass > 0, "null vector has invalid positive mass")
            plus = [max(x, F(0)) / mass for x in vector]
            minus = [max(-x, F(0)) / mass for x in vector]
            _require(sum(plus, F(0)) == sum(minus, F(0)) == 1, "collision weights do not normalize")
            _require(
                all(a >= 0 and b >= 0 and a * b == 0 for a, b in zip(plus, minus, strict=True)),
                "collision supports invalid",
            )
            observed_plus = [_dot(row, plus) for row in observations]
            observed_minus = [_dot(row, minus) for row in observations]
            truth_plus = [_dot(row, plus) for row in targets]
            truth_minus = [_dot(row, minus) for row in targets]
            difference = [a - b for a, b in zip(truth_plus, truth_minus, strict=True)]
            _require(observed_plus == observed_minus, "collision observations differ")
            _require(
                difference == [x / mass for x in changes] and difference[separating] != 0,
                "collision target difference invalid",
            )
            collision = {
                "free_column": free_column,
                "separating_row": separating,
                "null_vector": vector,
                "positive_mass": mass,
                "weights_plus": plus,
                "weights_minus": minus,
                "observed_plus": observed_plus,
                "observed_minus": observed_minus,
                "truth_plus": truth_plus,
                "truth_minus": truth_minus,
                "truth_difference": difference,
            }
            break
        _require(collision is not None, "failed target lacks canonical null witness")
    return {
        "observation_rank": len(indices),
        "target_rank": target_rank,
        "joint_rank": joint_rank,
        "row_basis": indices,
        "pivot_columns": pivots,
        "free_columns": free,
        "recoverable": not failed,
        "decoder": decoders if not failed else None,
        "recoverable_rows": recovered,
        "failed_rows": failed,
        "row_decoders": decoders,
        "collision": collision,
    }


def certify(observations, targets):
    """Exact finite-simplex recovery or a canonical normalized convex collision."""
    _native([observations, targets])
    _require(
        type(targets) is list and 1 <= len(targets) <= 64 and type(targets[0]) is list,
        "bounded target inventory required",
    )
    n = len(targets[0])
    _require(1 <= n <= 576, "bounded source columns required")
    _require(
        type(observations) is list and len(observations) <= 256,
        "bounded observation inventory required",
    )
    _matrix_shape(targets, len(targets), n)
    _matrix_shape(observations, len(observations), n)
    O, Q = _matrix(observations), _matrix(targets)
    return _detach(_certificate(O, Q))


def apply(intercept, matrix, observed):
    """Restricted dense affine application, without hidden field or geometry."""
    _native([intercept, matrix, observed])
    _require(type(intercept) is list and 1 <= len(intercept) <= 64, "bounded output rows required")
    _require(
        type(observed) is list and 0 < len(observed) <= 1024 and len(observed) % 4 == 0,
        "bounded four-moment observation blocks required",
    )
    _matrix_shape(matrix, len(intercept), len(observed))
    a, L, x = list(map(_fraction, intercept)), _matrix(matrix), list(map(_fraction, observed))
    return _detach([v + _dot(row, x) for v, row in zip(a, L, strict=True)])


def _sum_rows(matrix, children, parent_count):
    return [
        [
            sum((matrix[4 * i + j][g] for i, p in enumerate(children) if p == parent), F(0))
            for g in range(len(matrix[0]))
        ]
        for parent in range(parent_count)
        for j in range(4)
    ]


def _check_moments(parent, child, indices):
    for p, row in enumerate(parent):
        _require(
            row
            == [
                sum((r[j] for r, index in zip(child, indices, strict=True) if index == p), F(0))
                for j in range(16)
            ],
            "geometric moment additivity failed",
        )


def _geometric(owners, outgoing, ids):
    return [
        [
            x
            for t, owner in enumerate(owners)
            for x in (outgoing[t][j] if owner == c else [F(0)] * 4)
        ]
        for c in ids
        for j in range(len(ids))
    ]


def _constant_observations(moments, volume):
    return [volume**2 * row[4 * p + q] for row in moments for p, q in LINEAR]


def _constant_targets(owners, outgoing, moments, ids, volume):
    return [
        volume**2
        * sum(
            (
                _dot(outgoing[t][j], [moments[t][4 * p + q] for p, q in LINEAR])
                for t, owner in enumerate(owners)
                if owner == c
            ),
            F(0),
        )
        for c in ids
        for j in range(len(ids))
    ]


def _repair(matrix, observations, original_fine, targets, certificate, scales):
    predicted = _mm(matrix, observations)
    residuals = [
        [a - b for a, b in zip(row, target, strict=True)]
        for row, target in zip(predicted, targets, strict=True)
    ]
    _require(all(not any(row) for row in residuals), "geometric repair identity failed")
    collision = None
    if certificate["collision"] is not None:
        old = certificate["collision"]
        plus, minus = old["weights_plus"], old["weights_minus"]
        fp, fm = (
            [_dot(row, plus) for row in original_fine],
            [_dot(row, minus) for row in original_fine],
        )
        rp, rm = (
            [_dot(row, plus) for row in observations],
            [_dot(row, minus) for row in observations],
        )
        delta = [a - b for a, b in zip(rp, rm, strict=True)]
        _require(any(delta), "differing truths lack a repair measurement difference")
        pp, pm = [_dot(row, rp) for row in matrix], [_dot(row, rm) for row in matrix]
        ep = [a - b for a, b in zip(pp, old["truth_plus"], strict=True)]
        em = [a - b for a, b in zip(pm, old["truth_minus"], strict=True)]
        _require(not any(ep) and not any(em), "repair collision prediction invalid")
        normalized = [
            x / s if s else None for x, s in zip(old["truth_difference"], scales, strict=True)
        ]
        collision = {
            "fine_observed_plus": fp,
            "fine_observed_minus": fm,
            "observed_plus": rp,
            "observed_minus": rm,
            "difference": delta,
            "predicted_plus": pp,
            "predicted_minus": pm,
            "residual_plus": ep,
            "residual_minus": em,
            "normalized_truth_difference": normalized,
        }
    return {
        "intercept": [F(0)] * len(targets),
        "matrix": matrix,
        "predicted": predicted,
        "residuals": residuals,
        "exact": True,
        "collision": collision,
    }


def build_family(problem):
    """Determine fine-query sufficiency and expose explicit new measurement access."""
    probe, cc, fc, ct, ft, links, parents, rt = _parse(problem)
    volume = _area(probe)
    cids, fids = [e for e, _ in cc], [e for e, _ in fc]
    cm, fm, rm = (
        [_moments(b) for _, b in ct],
        [_moments(b) for _, b in ft],
        [_moments(b) for _, b, _, _ in rt],
    )
    co = [[_outgoing(b, tile) for _, b in cc] for _, tile in ct]
    ro = [[_outgoing(b, tile) for _, b in fc] for _, tile, _, _ in rt]
    repair_fine = [x[2] for x in rt]
    repair_coarse = [x[3] for x in rt]
    _check_moments(fm, rm, repair_fine)
    _check_moments(cm, fm, links)
    _check_moments(cm, rm, repair_coarse)
    n = 9 * len(ft)
    mc, mf, mr = 4 * len(ct), 4 * len(ft), 4 * len(rt)
    qc, qf = len(cc) ** 2, len(fc) ** 2
    Oc, Of, Or = (
        [[F(0)] * n for _ in range(mc)],
        [[F(0)] * n for _ in range(mf)],
        [[F(0)] * n for _ in range(mr)],
    )
    Qc, Qf = [[F(0)] * n for _ in range(qc)], [[F(0)] * n for _ in range(qf)]
    source_repair = [[i for i, x in enumerate(rt) if x[2] == t] for t in range(len(ft))]
    generators, integrals = [], []
    for t, ((event, bounds), moments, link) in enumerate(zip(ft, fm, links, strict=True)):
        u, v = _bernstein(bounds[0], bounds[1]), _bernstein(bounds[2], bounds[3])
        coarse_branches = [_outgoing(b, bounds) for _, b in cc]
        source_rows = []
        fine_first = fids.index(event)
        coarse_first = cids.index(ct[link][0])
        for i, j in product(range(3), repeat=2):
            coefficients = [volume**2 * u[i][p] * v[j][q] for p, q in QUADRATIC]
            source_rows.append(coefficients)
            g = len(generators)
            generators.append({"tile": t, "i": i, "j": j, "coefficients": coefficients})
            values = [_weighted(coefficients, power, moments) for power in LINEAR]
            integrals.append(values[0])
            _require(values[0] == volume**2 * _area(bounds) / 9, "generator integral invalid")
            for basis, value in enumerate(values):
                Of[4 * t + basis][g] = value
                Oc[4 * link + basis][g] = value
            for piece in source_repair[t]:
                for basis, power in enumerate(LINEAR):
                    Or[4 * piece + basis][g] = _weighted(coefficients, power, rm[piece])
            for d, branch in enumerate(coarse_branches):
                Qc[coarse_first * len(cc) + d][g] = _response(coefficients, branch, moments)
            for d in range(len(fc)):
                Qf[fine_first * len(fc) + d][g] = sum(
                    (
                        _response(coefficients, ro[piece][d], rm[piece])
                        for piece in source_repair[t]
                    ),
                    F(0),
                )
        _require(
            [sum((row[p] for row in source_rows), F(0)) for p in range(9)]
            == [volume**2] + [F(0)] * 8,
            "Bernstein source polynomial partition invalid",
        )
    _require(_sum_rows(Or, repair_fine, len(ft)) == Of, "repair-to-original observations differ")
    _require(_sum_rows(Of, links, len(ct)) == Oc, "original-to-coarse observations differ")
    _require(_sum_rows(Or, repair_coarse, len(ct)) == Oc, "repair-to-coarse observations differ")
    for a, c in enumerate(cids):
        for b, d in enumerate(cids):
            fine_rows = [
                i * len(fc) + j
                for i, (e, _) in enumerate(fc)
                if parents[e] == c
                for j, (f, _) in enumerate(fc)
                if parents[f] == d
            ]
            expected = [sum((Qf[row][g] for row in fine_rows), F(0)) for g in range(n)]
            _require(Qc[a * len(cc) + b] == expected, "two-parent response additivity failed")
    Gc = _geometric([e for e, _ in ct], co, cids)
    Gr = _geometric([e for e, _, _, _ in rt], ro, fids)
    _require(_mm(Gc, Oc) == Qc, "independent coarse geometric identity failed")
    _require(_mm(Gr, Or) == Qf, "independent fine geometric identity failed")
    constants = [_constant_observations(M, volume) for M in (cm, fm, rm)]
    constant_c = _constant_targets([e for e, _ in ct], co, cm, cids, volume)
    constant_f = _constant_targets([e for e, _, _, _ in rt], ro, rm, fids, volume)
    for matrix, constant in zip(
        (Oc, Of, Or, Qc, Qf), (*constants, constant_c, constant_f), strict=True
    ):
        _require(
            [sum(row, F(0)) for row in matrix] == constant, "constant field/source sum invalid"
        )
    _require(sum(integrals, F(0)) == volume**3, "unweighted source integral sum invalid")
    cv = [_area(b) if b is not None else F(0) for _, b in cc]
    fv = [_area(b) if b is not None else F(0) for _, b in fc]
    cs = [volume**2 * a * b for a, b in product(cv, repeat=2)]
    fs = [volume**2 * a * b for a, b in product(fv, repeat=2)]
    certificate = _certificate(Oc, Qf)
    repair = _repair(Gr, Or, Of, Qf, certificate, fs)
    defined = sum(s > 0 for s in fs)
    collision_count = int(certificate["collision"] is not None)
    decoder_entries = sum(len(row) for row in certificate["row_decoders"] if row is not None)
    if certificate["decoder"] is not None:
        decoder_entries += sum(len(row) for row in certificate["decoder"])
    counts = {
        "coarse_cells": len(cc),
        "fine_cells": len(fc),
        "positive_coarse_cells": sum(b is not None for _, b in cc),
        "positive_fine_cells": sum(b is not None for _, b in fc),
        "coarse_tiles": len(ct),
        "fine_tiles": len(ft),
        "repair_tiles": len(rt),
        "added_repair_tiles": len(rt) - len(ft),
        "generators": n,
        "coarse_observation_rows": mc,
        "fine_observation_rows": mf,
        "repair_observation_rows": mr,
        "coarse_response_rows": qc,
        "fine_response_rows": qf,
        "defined_fine_response_rows": defined,
        "undefined_fine_response_rows": qf - defined,
        "coarse_moment_entries": 16 * len(ct),
        "fine_moment_entries": 16 * len(ft),
        "repair_moment_entries": 16 * len(rt),
        "outgoing_entries": 4 * (len(ct) * len(cc) + len(rt) * len(fc)),
        "source_coefficient_entries": 9 * n,
        "observation_entries": (mc + mf + mr) * n,
        "target_entries": (qc + qf) * n,
        "constant_observation_entries": mc + mf + mr,
        "constant_target_entries": qc + qf,
        "generator_integral_entries": n,
        "raw_geometric_entries": qc * mc + qf * (1 + mr),
        "certificate_decoder_entries": decoder_entries,
        "recoverable_rows": len(certificate["recoverable_rows"]),
        "failed_rows": len(certificate["failed_rows"]),
        "collisions": collision_count,
        "collision_entries": collision_count * (3 * n + 2 * mc + 3 * qf + 1),
        "repair_prediction_entries": qf * n,
        "repair_residual_entries": qf * n,
        "repair_collision_entries": collision_count * (2 * mf + 3 * mr + 4 * qf + defined),
    }
    cell_rows = lambda cells: [
        {
            "event": e,
            "bounds": list(b) if b is not None else None,
            "volume": _area(b) if b is not None else F(0),
        }
        for e, b in cells
    ]
    observation_rows = lambda count: [
        {"tile": i, "basis": j} for i in range(count) for j in range(4)
    ]
    response_rows = lambda ids: [{"first": a, "second": b} for a, b in product(ids, repeat=2)]
    result = {
        "problem": problem,
        "geometry": {
            "volume": volume,
            "coarse_cells": cell_rows(cc),
            "fine_cells": cell_rows(fc),
            "parents": [{"event": e, "parent": parents[e]} for e, _ in fc],
            "coarse_tiles": [
                {
                    "event": e,
                    "bounds": list(b),
                    "moments": M,
                    "outgoing": [
                        {"event": d, "coefficients": row}
                        for (d, _), row in zip(cc, outs, strict=True)
                    ],
                }
                for (e, b), M, outs in zip(ct, cm, co, strict=True)
            ],
            "fine_tiles": [
                {"event": e, "bounds": list(b), "coarse_tile": link, "moments": M}
                for (e, b), link, M in zip(ft, links, fm, strict=True)
            ],
            "repair_tiles": [
                {
                    "event": e,
                    "bounds": list(b),
                    "fine_tile": t,
                    "coarse_tile": link,
                    "moments": M,
                    "outgoing": [
                        {"event": d, "coefficients": row}
                        for (d, _), row in zip(fc, outs, strict=True)
                    ],
                }
                for (e, b, t, link), M, outs in zip(rt, rm, ro, strict=True)
            ],
            "coarse_response_scales": cs,
            "fine_response_scales": fs,
        },
        "generators": generators,
        "matrices": {
            "coarse_observation_rows": observation_rows(len(ct)),
            "fine_observation_rows": observation_rows(len(ft)),
            "repair_observation_rows": observation_rows(len(rt)),
            "coarse_response_rows": response_rows(cids),
            "fine_response_rows": response_rows(fids),
            "coarse_observations": Oc,
            "fine_observations": Of,
            "repair_observations": Or,
            "coarse_targets": Qc,
            "fine_targets": Qf,
            "coarse_geometric": Gc,
            "generator_integrals": integrals,
            "constant_coarse_observations": constants[0],
            "constant_fine_observations": constants[1],
            "constant_repair_observations": constants[2],
            "constant_coarse_targets": constant_c,
            "constant_fine_targets": constant_f,
        },
        "certificate": certificate,
        "repair": repair,
        "checks": dict.fromkeys(
            (
                "geometry_partitions",
                "bernstein_partition",
                "generator_integrals",
                "moment_additivity",
                "observation_additivity",
                "response_additivity",
                "geometric_coarse_identity",
                "geometric_fine_identity",
                "coarse_certificate_valid",
                "collision_valid",
                "repair_collision_valid",
                "constant_field_sums",
            ),
            True,
        ),
        "counts": counts,
    }
    return _detach(result)
