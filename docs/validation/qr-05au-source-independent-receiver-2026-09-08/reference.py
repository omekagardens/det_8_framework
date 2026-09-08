"""QR-05AU independent reference: source-blind forward bases and raw nulls.

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


def _evaluate(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _need(type(matrix) is list and len(matrix) <= row_cap, "raw evaluator row inventory")
    _need(type(values) is list and len(values) <= width_cap, "raw evaluator width")
    _dimensions(matrix, len(matrix), len(values))
    _matrix_pair_shapes(matrix)
    _pair_shapes(values)
    rows = _matrix(matrix)
    vector = [_fraction(x) for x in values]
    return _wire(_matvec(rows, vector))


def produce(matrix, bank_values):
    """Evaluate only the supplied bank map; empty maps and banks are legal."""
    return _evaluate(matrix, bank_values, 320, 1024)


def apply(matrix, observed):
    """Evaluate only a zero-intercept recovered map; there is no offset input."""
    return _evaluate(matrix, observed, 64, 320)


def _null_direction(echelon, free_column, width):
    """Set one free variable to one and solve upper equations in reverse."""
    vector = [ZERO] * width
    vector[free_column] = ONE
    for pivot in sorted(echelon, reverse=True):
        row = echelon[pivot][0]
        vector[pivot] = -sum((row[j] * vector[j] for j in range(pivot + 1, width)), ZERO)
    return vector


def certify(interface, geometric):
    """Derive a certificate from these two raw matrices ONLY, without sources."""
    _native(interface)
    _native(geometric)
    _need(type(interface) is list and len(interface) <= 320, "interface inventory")
    _need(type(geometric) is list and 1 <= len(geometric) <= 64, "geometric inventory")
    _need(type(geometric[0]) is list and 1 <= len(geometric[0]) <= 1024, "bank width")
    width = len(geometric[0])
    _dimensions(interface, len(interface), width)
    _dimensions(geometric, len(geometric), width)
    _matrix_pair_shapes(interface)
    _matrix_pair_shapes(geometric)
    B, G = _matrix(interface), _matrix(geometric)
    accepted, echelon = _echelon(B)
    pivots = sorted(echelon)
    free = [j for j in range(width) if j not in echelon]
    recovered, failed, coefficients = [], [], []
    for index, row in enumerate(G):
        remainder, expansion = _reduce(row, echelon)
        if any(remainder):
            failed.append(index)
            coefficients.append(None)
        else:
            values = [expansion.get(j, ZERO) for j in accepted]
            _need(
                [
                    sum((values[h] * B[j][t] for h, j in enumerate(accepted)), ZERO)
                    for t in range(width)
                ]
                == row,
                "complete original-row expansion",
            )
            recovered.append(index)
            coefficients.append(values)
    target_basis, _ = _echelon(G)
    joint_basis, _ = _echelon(B + G)
    collision = None
    if failed:
        for free_column in free:
            vector = _null_direction(echelon, free_column, width)
            delta = _matvec(G, vector)
            separating = next((i for i, value in enumerate(delta) if value), None)
            if separating is None:
                continue
            _need(not any(_matvec(B, vector)), "complete null constraint")
            _need(
                all(vector[j] == (ONE if j == free_column else ZERO) for j in free),
                "canonical free coordinates",
            )
            zeros = [ZERO] * width
            observed_a = produce(interface, _wire(zeros))
            observed_b = produce(interface, _wire(vector))
            truth_a = produce(geometric, _wire(zeros))
            truth_b = produce(geometric, _wire(vector))
            observed_a, observed_b, truth_a, truth_b = (
                [_fraction(value) for value in values]
                for values in (observed_a, observed_b, truth_a, truth_b)
            )
            _need(
                observed_a == observed_b == [ZERO] * len(B)
                and truth_a == [ZERO] * len(G)
                and truth_b == delta,
                "actual raw zero/null evaluations",
            )
            collision = {
                "free_column": free_column,
                "separating_row": separating,
                "null_vector": vector,
                "bank_a": zeros,
                "bank_b": list(vector),
                "observed_a": observed_a,
                "observed_b": observed_b,
                "truth_a": truth_a,
                "truth_b": truth_b,
                "truth_difference": [b - a for a, b in zip(truth_a, truth_b)],
            }
            break
        _need(collision is not None, "failed membership must have a raw collision")
    _need((len(joint_basis) == len(accepted)) == (not failed), "rank/membership equivalence")
    return _wire(
        {
            "interface_rank": len(accepted),
            "target_rank": len(target_basis),
            "joint_rank": len(joint_basis),
            "row_basis": accepted,
            "pivot_columns": pivots,
            "free_columns": free,
            "recoverable_rows": recovered,
            "failed_rows": failed,
            "row_coefficients": coefficients,
            "recoverable": not failed,
            "collision": collision,
        }
    )


def _parse(problem):
    _native(problem)
    _keys(
        problem,
        (
            "family",
            "target_labels",
            "coarse_map",
            "filters",
            "geometric",
            "selected_rows",
            "bank",
            "observations",
            "targets",
        ),
    )
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    C, F, G, R, O, Q = (
        problem[key]
        for key in ("coarse_map", "filters", "geometric", "bank", "observations", "targets")
    )
    _need(type(G) is list and 1 <= len(G) <= 64, "target inventory")
    q = len(G)
    _need(type(G[0]) is list and 1 <= len(G[0]) <= 1024, "bank inventory")
    r = len(G[0])
    _need(type(Q) is list and len(Q) == q and type(Q[0]) is list, "source target inventory")
    n = len(Q[0])
    _need(1 <= n <= 576, "source column inventory")
    _need(type(C) is list and len(C) <= 256, "coarse inventory")
    m = len(C)
    selected = problem["selected_rows"]
    _need(type(selected) is list and len(selected) <= q, "selected row inventory")
    _need(all(type(i) is int and 0 <= i < q for i in selected), "selected target indices")
    _need(selected == sorted(set(selected)), "selected ascending unique")
    k = len(selected)
    for matrix, rows, columns in ((C, m, r), (F, k, r), (G, q, r), (R, r, n), (O, m, n), (Q, q, n)):
        _dimensions(matrix, rows, columns)
    labels = problem["target_labels"]
    _need(type(labels) is list and len(labels) == q, "target label inventory")
    pairs = []
    for label in labels:
        _keys(label, ("first", "second"))
        _need(type(label["first"]) is int and type(label["second"]) is int, "signed target IDs")
        pairs.append((label["first"], label["second"]))
    _need(pairs == sorted(set(pairs)), "target labels ascending unique")
    for matrix in (C, F, G, R, O, Q):
        _matrix_pair_shapes(matrix)
    # Every shape/label/index precedes every Fraction, and all values precede math.
    C, F, G, R, O, Q = (_matrix(matrix) for matrix in (C, F, G, R, O, Q))
    return C, F, G, R, O, Q, selected, n


def _difference(left, right):
    return [[a - b for a, b in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]


def _zero(matrix):
    return not any(value for row in matrix for value in row)


def build_family(problem):
    """Build an indexed recovered-only receiver, never fitted to source values."""
    C, F, G, R, O, Q, selected, n = _parse(problem)
    m, k, q, r = len(C), len(F), len(G), len(R)
    s = m + k
    _need(F == [G[i] for i in selected], "literal selected filters")
    B = C + F
    raw_interface = problem["coarse_map"] + problem["filters"]
    # This is deliberately the ACTUAL public two-matrix call, not a private
    # source-aware fit or an embedded older decoder.
    certificate = certify(raw_interface, problem["geometric"])
    BR, GR = _multiply(B, R, n), _multiply(G, R, n)
    coarse_residuals = _difference(BR[:m], O)
    target_residuals = _difference(GR, Q)
    _need(
        _zero(coarse_residuals) and _zero(target_residuals) and BR[m:] == [Q[i] for i in selected],
        "consistent selected source inputs",
    )
    recovered = certificate["recoverable_rows"]
    row_basis = certificate["row_basis"]
    v = len(recovered)
    D = []
    for index in recovered:
        row = [ZERO] * s
        compact = [_fraction(value) for value in certificate["row_coefficients"][index]]
        for original, value in zip(row_basis, compact):
            row[original] = value
        D.append(row)
    G_recovered = [G[i] for i in recovered]
    Q_recovered = [Q[i] for i in recovered]
    bank_predicted = _multiply(D, B, r)
    bank_residuals = _difference(bank_predicted, G_recovered)
    source_predicted = _multiply(D, BR, n)
    source_residuals = _difference(source_predicted, Q_recovered)
    _need(_zero(bank_residuals), "full recovered bank identity")
    _need(_zero(source_residuals), "full recovered source identity")
    D_wire, G_wire = _wire(D), _wire(G_recovered)
    controls = []
    for index in range(r + 1):
        z = [ZERO] * r
        bank_index = None if index == 0 else index - 1
        if bank_index is not None:
            z[bank_index] = ONE
        z_wire = _wire(z)
        cv = produce(problem["coarse_map"], z_wire)
        fv = produce(problem["filters"], z_wire)
        observed = cv + fv
        truth = produce(G_wire, z_wire)
        predicted = apply(D_wire, observed)
        cv, fv, observed, truth, predicted = (
            [_fraction(x) for x in values] for values in (cv, fv, observed, truth, predicted)
        )
        residuals = [a - b for a, b in zip(predicted, truth)]
        _need(
            cv == _matvec(C, z)
            and fv == _matvec(F, z)
            and observed == _matvec(B, z)
            and truth == _matvec(G_recovered, z)
            and predicted == _matvec(D, observed)
            and predicted == truth
            and not any(residuals),
            "complete restricted recovered application",
        )
        controls.append(
            {
                "bank_index": bank_index,
                "bank_values": z,
                "coarse_values": cv,
                "supplement_values": fv,
                "observed": observed,
                "truth": truth,
                "predicted": predicted,
                "residuals": residuals,
            }
        )
    complete = v == q
    _need(complete == certificate["recoverable"], "complete indexed recovery")
    collisions = int(certificate["collision"] is not None)
    return _wire(
        {
            "problem": deepcopy(problem),
            "interface": B,
            "source": {
                "interface_values": BR,
                "geometric_values": GR,
                "coarse_residuals": coarse_residuals,
                "target_residuals": target_residuals,
            },
            "certificate": certificate,
            "decoder": {
                "target_rows": list(recovered),
                "matrix": D,
                "bank_predicted": bank_predicted,
                "bank_residuals": bank_residuals,
                "source_predicted": source_predicted,
                "source_residuals": source_residuals,
                "complete": complete,
            },
            "bank_controls": controls,
            "checks": dict.fromkeys(
                (
                    "selected_filter_identity",
                    "source_inputs_consistent",
                    "source_independent_certificate",
                    "decoder_bank_identity",
                    "decoder_source_identity",
                    "restricted_application",
                    "collision_valid",
                    "complete_classification",
                ),
                True,
            ),
            "counts": {
                "coarse_values": m,
                "bank_values": r,
                "source_columns": n,
                "target_rows": q,
                "supplement_values": k,
                "receiver_values": s,
                "input_matrix_entries": m * r + k * r + q * r + r * n + m * n + q * n,
                "interface_entries": s * r,
                "source_check_entries": (s + m + 2 * q) * n,
                "compact_decoder_entries": v * certificate["interface_rank"],
                "raw_decoder_entries": v * s,
                "bank_prediction_entries": v * r,
                "bank_residual_entries": v * r,
                "source_prediction_entries": v * n,
                "source_residual_entries": v * n,
                "bank_controls": r + 1,
                "bank_control_entries": (r + 1) * (r + 2 * s + 3 * v),
                "collisions": collisions,
                "collision_entries": collisions * (3 * r + 2 * s + 3 * q),
                "recovered_rows": v,
                "failed_rows": q - v,
            },
        }
    )
