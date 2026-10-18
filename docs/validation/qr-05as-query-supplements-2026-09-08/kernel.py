"""Exact minimal supplemental scalar readouts on a supplied source simplex."""

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


def _preflight(problem):
    _native(problem)
    _fields(problem, ("family", "target_labels", "observations", "bank", "targets", "filters"))
    _require(type(problem["family"]) is str and problem["family"], "nonempty family required")
    Q = problem["targets"]
    _require(
        type(Q) is list and 1 <= len(Q) <= 64 and type(Q[0]) is list,
        "bounded target matrix required",
    )
    n, q = len(Q[0]), len(Q)
    _require(1 <= n <= 576, "bounded source columns required")
    O, R = problem["observations"], problem["bank"]
    _require(type(O) is list and len(O) <= 256, "bounded coarse row inventory required")
    _require(type(R) is list and len(R) <= 1024, "bounded bank row inventory required")
    labels = problem["target_labels"]
    _require(type(labels) is list and len(labels) == q, "complete target labels required")
    for row in labels:
        _fields(row, ("first", "second"))
        _require(
            type(row["first"]) is int and type(row["second"]) is int,
            "native signed label IDs required",
        )
    keys = [(x["first"], x["second"]) for x in labels]
    _require(keys == sorted(set(keys)), "target labels must be unique and ordered")
    _matrix_shape(Q, q, n)
    _matrix_shape(O, len(O), n)
    _matrix_shape(R, len(R), n)
    _matrix_shape(problem["filters"], q, len(R))
    return n, q, len(O), len(R)


def produce(filters, bank_values):
    """Only supplied raw bank values and linear filters enter this evaluator."""
    _native([filters, bank_values])
    _require(
        type(bank_values) is list and len(bank_values) <= 1024, "bounded raw bank values required"
    )
    _require(type(filters) is list and len(filters) <= 64, "bounded filter inventory required")
    _vector_shape(bank_values, len(bank_values))
    _matrix_shape(filters, len(filters), len(bank_values))
    G, x = _matrix(filters), list(map(_fraction, bank_values))
    return _detach([_dot(row, x) for row in G])


def apply(intercept, matrix, observed):
    """Only supplied affine coefficients and arbitrary-width raw values enter."""
    _native([intercept, matrix, observed])
    _require(
        type(intercept) is list and 1 <= len(intercept) <= 64, "bounded receiver outputs required"
    )
    _require(type(observed) is list and len(observed) <= 320, "bounded receiver values required")
    _vector_shape(intercept, len(intercept))
    _vector_shape(observed, len(observed))
    _matrix_shape(matrix, len(intercept), len(observed))
    a, L, x = list(map(_fraction, intercept)), _matrix(matrix), list(map(_fraction, observed))
    return _detach([v + _dot(row, x) for v, row in zip(a, L, strict=True)])


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


def _representation(target, reduced, transform, pivots):
    coordinates = [target[p] for p in pivots]
    if _mm([coordinates], reduced)[0] != target:
        return None
    return _mm([coordinates], transform)[0]


def _basis_data(basis):
    reduced, transform, pivots = _rref_with_transform(basis)
    _require(_mm(transform, basis) == reduced, "basis transform identity invalid")
    return reduced, transform, pivots


def _witness(
    j, target_row, base_rank, basis, pivots, transform, O, R, Q, H, filters, intercept, matrix
):
    n, m, k = len(Q[0]), len(O), len(H)
    vector = [F(0)] * n
    for i, pivot in enumerate(pivots):
        vector[pivot] = transform[i][base_rank + j]
    unit = [F(i == base_rank + j) for i in range(len(basis))]
    _require(
        [_dot(row, vector) for row in basis] == unit, "prescribed right-inverse direction invalid"
    )
    _require(
        all(vector[i] == 0 for i in range(n) if i not in pivots),
        "nonpivot source component nonzero",
    )
    _require(
        sum(vector, F(0)) == 0 and all(_dot(row, vector) == 0 for row in O),
        "base observations not null",
    )
    _require(
        [_dot(row, vector) for row in H] == [F(i == j) for i in range(k)],
        "supplement direction is not its coordinate unit",
    )
    mass = sum((max(x, F(0)) for x in vector), F(0))
    _require(
        mass > 0 and mass == sum((max(-x, F(0)) for x in vector), F(0)),
        "positive/negative witness masses differ",
    )
    plus = [max(x, F(0)) / mass for x in vector]
    minus = [max(-x, F(0)) / mass for x in vector]
    _require(sum(plus, F(0)) == sum(minus, F(0)) == 1, "witness weights not normalized")
    _require(
        all(a >= 0 and b >= 0 and a * b == 0 for a, b in zip(plus, minus, strict=True)),
        "witness supports invalid",
    )
    bank_plus = [_dot(row, plus) for row in R]
    bank_minus = [_dot(row, minus) for row in R]
    coarse_plus = [_dot(row, plus) for row in O]
    coarse_minus = [_dot(row, minus) for row in O]
    # Exercise the restricted public producer, not a hidden source-model evaluator.
    supplement_plus = list(map(_fraction, produce(_encode(filters), _encode(bank_plus))))
    supplement_minus = list(map(_fraction, produce(_encode(filters), _encode(bank_minus))))
    _require(
        supplement_plus == [_dot(row, plus) for row in H]
        and supplement_minus == [_dot(row, minus) for row in H],
        "producer outputs disagree with source-column values",
    )
    full_plus = coarse_plus + supplement_plus
    full_minus = coarse_minus + supplement_minus
    available_rows = [i for i in range(m + k) if i != m + j]
    available_plus = [full_plus[i] for i in available_rows]
    available_minus = [full_minus[i] for i in available_rows]
    _require(available_plus == available_minus, "deleted-readout observations differ")
    _require(
        supplement_plus[j] - supplement_minus[j] == 1 / mass, "omitted readout difference invalid"
    )
    truth_plus = [_dot(row, plus) for row in Q]
    truth_minus = [_dot(row, minus) for row in Q]
    truth_difference = [a - b for a, b in zip(truth_plus, truth_minus, strict=True)]
    _require(
        truth_difference == [_dot(row, vector) / mass for row in Q]
        and truth_difference[target_row] == 1 / mass,
        "true witness difference invalid",
    )
    # Exercise the restricted receiver on ALL coarse and supplement coordinates.
    predicted_plus = list(
        map(_fraction, apply(_encode(intercept), _encode(matrix), _encode(full_plus)))
    )
    predicted_minus = list(
        map(_fraction, apply(_encode(intercept), _encode(matrix), _encode(full_minus)))
    )
    residual_plus = [a - b for a, b in zip(predicted_plus, truth_plus, strict=True)]
    residual_minus = [a - b for a, b in zip(predicted_minus, truth_minus, strict=True)]
    _require(not any(residual_plus) and not any(residual_minus), "online witness recovery failed")
    return {
        "omitted_index": j,
        "target_row": target_row,
        "available_rows": available_rows,
        "null_vector": vector,
        "positive_mass": mass,
        "weights_plus": plus,
        "weights_minus": minus,
        "bank_plus": bank_plus,
        "bank_minus": bank_minus,
        "coarse_plus": coarse_plus,
        "coarse_minus": coarse_minus,
        "supplement_plus": supplement_plus,
        "supplement_minus": supplement_minus,
        "available_plus": available_plus,
        "available_minus": available_minus,
        "truth_plus": truth_plus,
        "truth_minus": truth_minus,
        "truth_difference": truth_difference,
        "predicted_plus": predicted_plus,
        "predicted_minus": predicted_minus,
        "residual_plus": residual_plus,
        "residual_minus": residual_minus,
    }


def build_family(problem):
    """Construct and certify minimal fixed scalar query supplements, not sensors."""
    n, q, m, r = _preflight(problem)
    O, R, Q, G = (_matrix(problem[key]) for key in ("observations", "bank", "targets", "filters"))
    _require(_mm(G, R, n) == Q, "inherited complete filter identity failed")
    A = [[F(1)] * n] + O
    base_rows = _row_basis(A)
    basis = [A[i] for i in base_rows]
    reduced, transform, pivots = _basis_data(basis)
    base_rank = len(basis)
    target_rank = len(_row_basis(Q))
    joint_rank = len(_row_basis(A + Q))
    delta = joint_rank - base_rank
    recovered = []
    failed = []
    for index, target in enumerate(Q):
        coefficients = _representation(target, reduced, transform, pivots)
        if coefficients is None:
            failed.append(index)
        else:
            _require(_mm([coefficients], basis)[0] == target, "base recoverable identity failed")
            recovered.append(index)
    _require((not failed) == (delta == 0), "base membership/rank disagreement")
    base = {
        "observation_rank": base_rank,
        "target_rank": target_rank,
        "joint_rank": joint_rank,
        "delta": delta,
        "row_basis": base_rows,
        "pivot_columns": list(pivots),
        "free_columns": [i for i in range(n) if i not in pivots],
        "recoverable_rows": recovered,
        "failed_rows": failed,
    }
    selected = []
    decisions = []
    for index, target in enumerate(Q):
        rank_before = len(basis)
        coefficients = _representation(target, reduced, transform, pivots)
        chosen = coefficients is None
        if chosen:
            basis.append(target)
            selected.append(index)
            reduced, transform, pivots = _basis_data(basis)
        else:
            _require(_mm([coefficients], basis)[0] == target, "skipped target expansion invalid")
        decisions.append(
            {
                "target_row": index,
                "rank_before": rank_before,
                "rank_after": len(basis),
                "selected": chosen,
                "coefficients": coefficients,
            }
        )
    _require(
        len(selected) == delta and len(basis) == joint_rank,
        "selection does not attain rank lower bound",
    )
    filters = [list(G[i]) for i in selected]
    H = _mm(filters, R, n)
    _require(H == [Q[i] for i in selected], "selected filters changed original target functionals")
    supports = [[j for j, x in enumerate(row) if x] for row in filters]
    selection = {
        "target_rows": selected,
        "target_labels": [dict(problem["target_labels"][i]) for i in selected],
        "decisions": decisions,
        "filters": filters,
        "bank_support": supports,
        "values": H,
    }
    X = O + H
    M = [[F(1)] * n] + X
    rows = _row_basis(M)
    _require(
        rows == base_rows + [1 + m + j for j in range(delta)],
        "supplemented canonical original-row basis differs",
    )
    _require([M[i] for i in rows] == basis, "full basis does not preserve original rows")
    coefficients = []
    for target in Q:
        row = _representation(target, reduced, transform, pivots)
        _require(
            row is not None and _mm([row], basis)[0] == target,
            "full receiver target identity failed",
        )
        coefficients.append(row)
    intercept = [F(0)] * q
    linear = [[F(0)] * (m + delta) for _ in range(q)]
    for j, row in enumerate(coefficients):
        for index, value in zip(rows, row, strict=True):
            if index:
                linear[j][index - 1] = value
            else:
                intercept[j] = value
    predicted = [[intercept[j] + x for x in row] for j, row in enumerate(_mm(linear, X, n))]
    residuals = [
        [a - b for a, b in zip(row, target, strict=True)]
        for row, target in zip(predicted, Q, strict=True)
    ]
    _require(all(not any(row) for row in residuals), "dense receiver residual nonzero")
    decoder = {
        "row_basis": rows,
        "pivot_columns": list(pivots),
        "free_columns": [i for i in range(n) if i not in pivots],
        "coefficients": coefficients,
        "intercept": intercept,
        "matrix": linear,
        "predicted": predicted,
        "residuals": residuals,
        "exact": True,
    }
    witnesses = [
        _witness(
            j, index, base_rank, basis, pivots, transform, O, R, Q, H, filters, intercept, linear
        )
        for j, index in enumerate(selected)
    ]
    counts = {
        "source_columns": n,
        "coarse_values": m,
        "bank_values": r,
        "target_rows": q,
        "supplement_values": delta,
        "receiver_values": m + delta,
        "input_matrix_entries": m * n + r * n + q * n + q * r,
        "selected_filter_entries": delta * r,
        "selected_filter_nonzero": sum(len(s) for s in supports),
        "selected_bank_rows": len({i for s in supports for i in s}),
        "supplement_entries": delta * n,
        "decision_coefficient_entries": sum(
            len(d["coefficients"]) for d in decisions if d["coefficients"] is not None
        ),
        "decoder_compact_entries": q * joint_rank,
        "decoder_raw_entries": q * (1 + m + delta),
        "prediction_entries": q * n,
        "residual_entries": q * n,
        "witnesses": delta,
        "witness_entries": delta
        * (3 * n + 2 * r + 2 * m + 2 * delta + 2 * (m + delta - 1) + 7 * q + 1)
        if delta
        else 0,
    }
    return _detach(
        {
            "problem": problem,
            "base": base,
            "selection": selection,
            "decoder": decoder,
            "witnesses": witnesses,
            "checks": dict.fromkeys(
                (
                    "inherited_filter_identity",
                    "base_certificate",
                    "greedy_selection",
                    "selected_filter_identity",
                    "receiver_identity",
                    "witness_constraints",
                    "online_witness_recovery",
                    "minimality_certificate",
                ),
                True,
            ),
            "counts": counts,
        }
    )
