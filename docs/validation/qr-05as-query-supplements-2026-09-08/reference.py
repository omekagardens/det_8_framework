"""QR-05AS independent reference: forward bases and canonical right inverses.

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


def _reduce(row, echelon):
    """Forward reduction plus its expression in the original accepted rows."""
    remainder = list(row)
    expression = {}
    for pivot in sorted(echelon):
        factor = remainder[pivot]
        if not factor:
            continue
        basis, combination = echelon[pivot]
        for index in range(pivot, len(row)):
            remainder[index] -= factor * basis[index]
        for original, value in combination.items():
            expression[original] = expression.get(original, ZERO) + factor * value
    return remainder, expression


def _echelon(rows):
    """Greedy original-row admission, with pivot-sorted forward rows."""
    accepted = []
    echelon = {}
    for index, row in enumerate(rows):
        remainder, expression = _reduce(row, echelon)
        pivot = next((j for j, x in enumerate(remainder) if x), None)
        if pivot is None:
            continue
        factor = remainder[pivot]
        combination = {j: -x / factor for j, x in expression.items() if x}
        combination[index] = ONE / factor
        echelon[pivot] = ([x / factor for x in remainder], combination)
        accepted.append(index)
    return accepted, echelon


def _pair_shapes(values):
    _need(all(type(value) is list and len(value) == 2 for value in values), "rational pair shapes")


def _matrix_pair_shapes(matrix):
    for row in matrix:
        _pair_shapes(row)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _multiply(left, right, columns):
    if not right:
        return [[ZERO] * columns for _ in left]
    transposed = list(zip(*right))
    _need(len(transposed) == columns, "internal product width")
    return [[_dot(row, col) for col in transposed] for row in left]


def produce(filters, bank_values):
    """Emit only the supplied raw bank filters; zero filters/bank are valid."""
    _native(filters)
    _native(bank_values)
    _need(type(filters) is list and len(filters) <= 64, "producer row inventory")
    _need(type(bank_values) is list and len(bank_values) <= 1024, "bank value inventory")
    _dimensions(filters, len(filters), len(bank_values))
    _matrix_pair_shapes(filters)
    _pair_shapes(bank_values)
    rows = _matrix(filters)
    values = [_fraction(x) for x in bank_values]
    return _wire(_matvec(rows, values))


def apply(intercept, matrix, observed):
    """Receive only an affine map and its raw ordered input, including width0."""
    _native(intercept)
    _native(matrix)
    _native(observed)
    _need(type(intercept) is list and 1 <= len(intercept) <= 64, "receiver row inventory")
    _need(type(observed) is list and len(observed) <= 320, "receiver value inventory")
    _dimensions(matrix, len(intercept), len(observed))
    _pair_shapes(intercept)
    _matrix_pair_shapes(matrix)
    _pair_shapes(observed)
    offsets = [_fraction(x) for x in intercept]
    rows = _matrix(matrix)
    values = [_fraction(x) for x in observed]
    return _wire([a + _dot(row, values) for a, row in zip(offsets, rows)])


def _parse(problem):
    _native(problem)
    _keys(problem, ("family", "target_labels", "observations", "bank", "targets", "filters"))
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    O, R, Q, G = (problem[k] for k in ("observations", "bank", "targets", "filters"))
    _need(type(Q) is list and 1 <= len(Q) <= 64 and type(Q[0]) is list, "target row inventory")
    q, n = len(Q), len(Q[0])
    _need(1 <= n <= 576, "source inventory")
    _need(type(O) is list and len(O) <= 256, "coarse inventory")
    _need(type(R) is list and len(R) <= 1024, "bank inventory")
    _dimensions(Q, q, n)
    _dimensions(O, len(O), n)
    _dimensions(R, len(R), n)
    _dimensions(G, q, len(R))
    labels = problem["target_labels"]
    _need(type(labels) is list and len(labels) == q, "target label inventory")
    pairs = []
    for label in labels:
        _keys(label, ("first", "second"))
        _need(type(label["first"]) is int and type(label["second"]) is int, "signed target IDs")
        pairs.append((label["first"], label["second"]))
    _need(pairs == sorted(set(pairs)), "sorted unique target labels")
    for matrix in (O, R, Q, G):
        _matrix_pair_shapes(matrix)
    # All inventories, dimensions and PAIR SHAPES precede Fraction operations;
    # all scalar values are parsed before products or elimination.
    O, R, Q, G = (_matrix(matrix) for matrix in (O, R, Q, G))
    _need(_multiply(G, R, n) == Q, "complete inherited filter identity")
    return O, R, Q, G, n


def _extend(row, original_index, echelon):
    """Admit an unchanged original row, retaining its forward combination."""
    remainder, expression = _reduce(row, echelon)
    pivot = next((j for j, x in enumerate(remainder) if x), None)
    if pivot is None:
        return False, expression
    scale = remainder[pivot]
    combination = {j: -value / scale for j, value in expression.items() if value}
    combination[original_index] = ONE / scale
    echelon[pivot] = ([x / scale for x in remainder], combination)
    return True, None


def _expansion(row, echelon, indices, basis):
    remainder, expression = _reduce(row, echelon)
    _need(not any(remainder), "target outside supplemented span")
    coefficients = [expression.get(j, ZERO) for j in indices]
    n = len(row)
    _need(
        [sum((d * b[k] for d, b in zip(coefficients, basis) if d and b[k]), ZERO) for k in range(n)]
        == row,
        "complete original-basis expansion",
    )
    return coefficients


def _right_inverse_direction(echelon, row_basis, coordinate, n):
    """Solve B[:,P] w[P]=e_coordinate by transformed RHS and back substitution."""
    original = row_basis[coordinate]
    vector = [ZERO] * n
    for pivot in sorted(echelon, reverse=True):
        row, combination = echelon[pivot]
        rhs = combination.get(original, ZERO)
        vector[pivot] = rhs - _dot(row[pivot + 1 :], vector[pivot + 1 :])
    return vector


def _witness(j, target_row, base_rank, row_basis, basis, echelon, O, R, Q, filters, H, a, L):
    n, m, q = len(Q[0]), len(O), len(Q)
    delta = len(H)
    width = m + delta
    vector = _right_inverse_direction(echelon, row_basis, base_rank + j, n)
    desired = [ONE if k == base_rank + j else ZERO for k in range(len(basis))]
    _need(_matvec(basis, vector) == desired, "canonical square right inverse")
    _need(all(vector[k] == 0 for k in range(n) if k not in echelon), "nonpivot zeros")
    _need(sum(vector, ZERO) == 0 and not any(_matvec(O, vector)), "base-null direction")
    _need(
        _matvec(H, vector) == [ONE if k == j else ZERO for k in range(delta)],
        "unit omitted readout",
    )
    mass = sum((x for x in vector if x > 0), ZERO)
    _need(mass > 0 and mass == -sum((x for x in vector if x < 0), ZERO), "equal positive mass")
    plus = [max(x, ZERO) / mass for x in vector]
    minus = [max(-x, ZERO) / mass for x in vector]
    _need(sum(plus, ZERO) == 1 and sum(minus, ZERO) == 1, "normalized mixtures")
    _need(
        all(x >= 0 and y >= 0 and x * y == 0 for x, y in zip(plus, minus)),
        "disjoint positive mixtures",
    )
    bp, bm = _matvec(R, plus), _matvec(R, minus)
    cp, cm = _matvec(O, plus), _matvec(O, minus)
    tp, tm = _matvec(Q, plus), _matvec(Q, minus)
    # Exercise the restricted online APIs, never substitute H*lambda for emit.
    sp = [_fraction(x) for x in produce(_wire(filters), _wire(bp))]
    sm = [_fraction(x) for x in produce(_wire(filters), _wire(bm))]
    _need(sp == _matvec(H, plus) and sm == _matvec(H, minus), "actual producer outputs")
    fullp, fullm = cp + sp, cm + sm
    available_rows = [k for k in range(width) if k != m + j]
    ap, am = [fullp[k] for k in available_rows], [fullm[k] for k in available_rows]
    _need(ap == am, "omitted interface collision")
    difference = [x - y for x, y in zip(tp, tm)]
    _need(
        difference == [x / mass for x in _matvec(Q, vector)], "normalized complete truth difference"
    )
    _need(
        fullp[m + j] - fullm[m + j] == ONE / mass and difference[target_row] == ONE / mass,
        "positive named target difference",
    )
    pp = [_fraction(x) for x in apply(_wire(a), _wire(L), _wire(fullp))]
    pm = [_fraction(x) for x in apply(_wire(a), _wire(L), _wire(fullm))]
    rp, rm = [x - y for x, y in zip(pp, tp)], [x - y for x, y in zip(pm, tm)]
    _need(not any(rp) and not any(rm), "both complete online recoveries")
    _need(len(tp) == q and len(pp) == q, "complete witness target inventory")
    return {
        "omitted_index": j,
        "target_row": target_row,
        "available_rows": available_rows,
        "null_vector": vector,
        "positive_mass": mass,
        "weights_plus": plus,
        "weights_minus": minus,
        "bank_plus": bp,
        "bank_minus": bm,
        "coarse_plus": cp,
        "coarse_minus": cm,
        "supplement_plus": sp,
        "supplement_minus": sm,
        "available_plus": ap,
        "available_minus": am,
        "truth_plus": tp,
        "truth_minus": tm,
        "truth_difference": difference,
        "predicted_plus": pp,
        "predicted_minus": pm,
        "residual_plus": rp,
        "residual_minus": rm,
    }


def build_family(problem):
    O, R, Q, G, n = _parse(problem)
    m, r, q = len(O), len(R), len(Q)
    A = [[ONE] * n] + O
    base_indices, base_echelon = _echelon(A)
    base_rank = len(base_indices)
    target_rank = len(_echelon(Q)[0])
    joint_rank = len(_echelon(A + Q)[0])
    delta = joint_rank - base_rank
    _need(0 <= delta <= q, "quotient rank bounds")
    recoverable, failed = [], []
    for j, row in enumerate(Q):
        remainder, _ = _reduce(row, base_echelon)
        (failed if any(remainder) else recoverable).append(j)
    _need((delta == 0) == (not failed), "base membership classification")
    base = {
        "observation_rank": base_rank,
        "target_rank": target_rank,
        "joint_rank": joint_rank,
        "delta": delta,
        "row_basis": base_indices,
        "pivot_columns": sorted(base_echelon),
        "free_columns": [j for j in range(n) if j not in base_echelon],
        "recoverable_rows": recoverable,
        "failed_rows": failed,
    }
    greedy = dict(base_echelon)
    original_indices = list(base_indices)
    original_basis = [A[j] for j in base_indices]
    decisions, selected = [], []
    for target, row in enumerate(Q):
        before = len(original_indices)
        origin = len(A) + target
        admitted, expression = _extend(row, origin, greedy)
        if admitted:
            selected.append(target)
            original_indices.append(origin)
            original_basis.append(row)
            coefficients = None
        else:
            coefficients = [expression.get(j, ZERO) for j in original_indices]
            _need(
                [
                    sum(
                        (d * b[k] for d, b in zip(coefficients, original_basis) if d and b[k]), ZERO
                    )
                    for k in range(n)
                ]
                == row,
                "skipped row prefix identity",
            )
        decisions.append(
            {
                "target_row": target,
                "rank_before": before,
                "rank_after": len(original_indices),
                "selected": admitted,
                "coefficients": coefficients,
            }
        )
    _need(
        len(selected) == delta and len(original_indices) == joint_rank, "greedy quotient completion"
    )
    filters = [list(G[j]) for j in selected]
    H = _multiply(filters, R, n)
    _need(H == [Q[j] for j in selected], "literal selected target filters")
    support = [[k for k, x in enumerate(row) if x] for row in filters]
    selection = {
        "target_rows": selected,
        "target_labels": [deepcopy(problem["target_labels"][j]) for j in selected],
        "decisions": decisions,
        "filters": filters,
        "bank_support": support,
        "values": H,
    }
    X = O + H
    M = [[ONE] * n] + X
    row_basis, echelon = _echelon(M)
    _need(
        row_basis == base_indices + [1 + m + j for j in range(delta)],
        "supplemented original row basis",
    )
    basis = [M[j] for j in row_basis]
    _need(len(basis) == joint_rank, "supplemented rank")
    D = [_expansion(row, echelon, row_basis, basis) for row in Q]
    a = [ZERO] * q
    L = [[ZERO] * (m + delta) for _ in range(q)]
    for target, row in enumerate(D):
        for index, coefficient in zip(row_basis, row):
            if index == 0:
                a[target] = coefficient
            else:
                L[target][index - 1] = coefficient
    predicted = [[a[i] + value for value in row] for i, row in enumerate(_multiply(L, X, n))]
    residuals = [[x - y for x, y in zip(row, target)] for row, target in zip(predicted, Q)]
    _need(all(x == 0 for row in residuals for x in row), "complete receiver identity")
    decoder = {
        "row_basis": row_basis,
        "pivot_columns": sorted(echelon),
        "free_columns": [j for j in range(n) if j not in echelon],
        "coefficients": D,
        "intercept": a,
        "matrix": L,
        "predicted": predicted,
        "residuals": residuals,
        "exact": True,
    }
    witnesses = [
        _witness(j, target, base_rank, row_basis, basis, echelon, O, R, Q, filters, H, a, L)
        for j, target in enumerate(selected)
    ]
    _need(
        len(witnesses) == delta and joint_rank == base_rank + len(filters), "minimality dimensions"
    )
    counts = {
        "source_columns": n,
        "coarse_values": m,
        "bank_values": r,
        "target_rows": q,
        "supplement_values": delta,
        "receiver_values": m + delta,
        "input_matrix_entries": m * n + r * n + q * n + q * r,
        "selected_filter_entries": delta * r,
        "selected_filter_nonzero": sum(bool(x) for row in filters for x in row),
        "selected_bank_rows": len({k for row in support for k in row}),
        "supplement_entries": delta * n,
        "decision_coefficient_entries": sum(
            len(row["coefficients"]) for row in decisions if row["coefficients"] is not None
        ),
        "decoder_compact_entries": q * joint_rank,
        "decoder_raw_entries": q * (1 + m + delta),
        "prediction_entries": q * n,
        "residual_entries": q * n,
        "witnesses": delta,
        "witness_entries": 0
        if delta == 0
        else delta * (3 * n + 2 * r + 2 * m + 2 * delta + 2 * (m + delta - 1) + 7 * q + 1),
    }
    return _wire(
        {
            "problem": deepcopy(problem),
            "base": base,
            "selection": selection,
            "decoder": decoder,
            "witnesses": witnesses,
            "checks": {
                name: True
                for name in (
                    "inherited_filter_identity",
                    "base_certificate",
                    "greedy_selection",
                    "selected_filter_identity",
                    "receiver_identity",
                    "witness_constraints",
                    "online_witness_recovery",
                    "minimality_certificate",
                )
            },
            "counts": counts,
        }
    )
