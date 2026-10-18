"""Source-independent exact linear receiver and raw bank countercontrols."""

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
    if rank == 0:
        return [], [], []
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


def _raw_shapes(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _require(type(values) is list and len(values) <= width_cap, "bounded raw input width")
    _require(type(matrix) is list and len(matrix) <= row_cap, "bounded raw output inventory")
    _vector_shape(values, len(values))
    _matrix_shape(matrix, len(matrix), len(values))


def produce(matrix, bank_values):
    _raw_shapes(matrix, bank_values, 320, 1024)
    rows, values = _matrix(matrix), list(map(_fraction, bank_values))
    return _detach([_dot(row, values) for row in rows])


def apply(matrix, observed):
    _raw_shapes(matrix, observed, 64, 320)
    rows, values = _matrix(matrix), list(map(_fraction, observed))
    return _detach([_dot(row, values) for row in rows])


def _certificate_shapes(interface, geometric):
    _native(interface)
    _native(geometric)
    _require(
        type(geometric) is list and 1 <= len(geometric) <= 64 and type(geometric[0]) is list,
        "bounded target inventory",
    )
    q, r = len(geometric), len(geometric[0])
    _require(1 <= r <= 1024, "bounded raw bank inventory")
    _require(type(interface) is list and len(interface) <= 320, "bounded interface inventory")
    _matrix_shape(interface, len(interface), r)
    _matrix_shape(geometric, q, r)
    return len(interface), q, r


def _representation(target, reduced, transform, pivots):
    coordinates = [target[p] for p in pivots]
    if _mm([coordinates], reduced, columns=len(target))[0] != target:
        return None
    return _mm([coordinates], transform, columns=len(pivots))[0]


def certify(interface, geometric):
    s, q, r = _certificate_shapes(interface, geometric)
    B, G = _matrix(interface), _matrix(geometric)
    indices = _row_basis(B)
    basis = [B[i] for i in indices]
    reduced, transform, pivots = _rref_with_transform(basis)
    _require(_mm(transform, basis, columns=r) == reduced, "original basis transform fails")
    free = [j for j in range(r) if j not in pivots]
    coefficients = [_representation(row, reduced, transform, pivots) for row in G]
    recovered = [i for i, row in enumerate(coefficients) if row is not None]
    failed = [i for i, row in enumerate(coefficients) if row is None]
    for i in recovered:
        _require(
            _mm([coefficients[i]], basis, columns=r)[0] == G[i], "complete target expansion fails"
        )
    rank = len(indices)
    target_rank, joint_rank = len(_row_basis(G)), len(_row_basis(B + G))
    _require((joint_rank == rank) == (not failed), "joint rank and membership disagree")
    collision = None
    if failed:
        for j in free:
            vector = [F(0)] * r
            vector[j] = F(1)
            for i, pivot in enumerate(pivots):
                vector[pivot] = -reduced[i][j]
            difference = [_dot(row, vector) for row in G]
            detecting = next((i for i, x in enumerate(difference) if x), None)
            if detecting is None:
                continue
            _require(detecting in failed, "recovered row detects a null direction")
            _require(
                [vector[t] for t in free] == [F(t == j) for t in free],
                "canonical free coordinate rule fails",
            )
            _require(
                [vector[p] for p in pivots] == [-row[j] for row in reduced],
                "canonical pivot coordinate rule fails",
            )
            _require(not any(_dot(row, vector) for row in B), "interface null identity fails")
            zero = [F(0)] * r
            observed_a = list(map(_fraction, produce(interface, _encode(zero))))
            observed_b = list(map(_fraction, produce(interface, _encode(vector))))
            truth_a = list(map(_fraction, produce(geometric, _encode(zero))))
            truth_b = list(map(_fraction, produce(geometric, _encode(vector))))
            truth_difference = [y - x for x, y in zip(truth_a, truth_b, strict=True)]
            _require(observed_a == observed_b == [F(0)] * s, "raw collision observations differ")
            _require(
                truth_a == [F(0)] * q
                and truth_difference == truth_b == difference
                and difference[detecting] != 0,
                "raw collision truths fail",
            )
            _require(
                all(difference[i] == 0 for i in recovered),
                "null direction changes recovered response",
            )
            collision = {
                "free_column": j,
                "separating_row": detecting,
                "null_vector": vector,
                "bank_a": zero,
                "bank_b": vector,
                "observed_a": observed_a,
                "observed_b": observed_b,
                "truth_a": truth_a,
                "truth_b": truth_b,
                "truth_difference": truth_difference,
            }
            break
        _require(collision is not None, "failed target lacks null witness")
    return _detach(
        {
            "interface_rank": rank,
            "target_rank": target_rank,
            "joint_rank": joint_rank,
            "row_basis": indices,
            "pivot_columns": pivots,
            "free_columns": free,
            "recoverable_rows": recovered,
            "failed_rows": failed,
            "row_coefficients": coefficients,
            "recoverable": not failed,
            "collision": collision,
        }
    )


def _preflight(problem):
    _native(problem)
    _fields(
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
    _require(type(problem["family"]) is str and problem["family"], "nonempty family required")
    G, Q = problem["geometric"], problem["targets"]
    _require(
        type(G) is list and 1 <= len(G) <= 64 and type(G[0]) is list,
        "bounded geometric target inventory",
    )
    q, r = len(G), len(G[0])
    _require(1 <= r <= 1024, "bounded raw bank inventory")
    _require(
        type(Q) is list and len(Q) == q and type(Q[0]) is list, "complete source target inventory"
    )
    n = len(Q[0])
    _require(1 <= n <= 576, "bounded source inventory")
    labels = problem["target_labels"]
    _require(type(labels) is list and len(labels) == q, "complete target labels required")
    pairs = []
    for label in labels:
        _fields(label, ("first", "second"))
        _require(
            type(label["first"]) is int and type(label["second"]) is int,
            "native signed target labels required",
        )
        pairs.append((label["first"], label["second"]))
    _require(pairs == sorted(set(pairs)), "target labels must be sorted unique")
    C, filters = problem["coarse_map"], problem["filters"]
    _require(type(C) is list and len(C) <= 256, "bounded coarse row inventory")
    _require(type(filters) is list and len(filters) <= q, "bounded filter inventory")
    m, k = len(C), len(filters)
    selected = problem["selected_rows"]
    _require(type(selected) is list and len(selected) == k, "selection inventory differs")
    _require(
        all(type(i) is int and 0 <= i < q for i in selected),
        "native target selection index required",
    )
    _require(selected == sorted(set(selected)), "target selection must be sorted unique")
    for key, rows, width in (
        ("coarse_map", m, r),
        ("filters", k, r),
        ("geometric", q, r),
        ("bank", r, n),
        ("observations", m, n),
        ("targets", q, n),
    ):
        _matrix_shape(problem[key], rows, width)
    return m, k, q, r, n


def _subtract(left, right):
    return [
        [x - y for x, y in zip(row, other, strict=True)]
        for row, other in zip(left, right, strict=True)
    ]


def _zero(rows):
    return not any(value for row in rows for value in row)


def build_family(problem):
    m, k, q, r, n = _preflight(problem)
    C, filters, G, R, O, Q = (
        _matrix(problem[key])
        for key in ("coarse_map", "filters", "geometric", "bank", "observations", "targets")
    )
    selected = problem["selected_rows"]
    _require(filters == [G[i] for i in selected], "filters differ from selected G rows")
    B = C + filters
    s = m + k
    B_wire, G_wire = _encode(B), _encode(G)
    certificate = certify(B_wire, G_wire)
    interface_values, geometric_values = _mm(B, R), _mm(G, R)
    coarse_residuals = _subtract(interface_values[:m], O)
    target_residuals = _subtract(geometric_values, Q)
    _require(
        _zero(coarse_residuals)
        and _zero(target_residuals)
        and interface_values[m:] == [Q[i] for i in selected],
        "source inputs inconsistent",
    )
    recovered, failed = certificate["recoverable_rows"], certificate["failed_rows"]
    _require(sorted(recovered + failed) == list(range(q)), "incomplete row classification")
    indices = certificate["row_basis"]
    D = []
    for i in recovered:
        compact = list(map(_fraction, certificate["row_coefficients"][i]))
        _require(len(compact) == len(indices), "compact decoder shape differs")
        row = [F(0)] * s
        for index, value in zip(indices, compact, strict=True):
            row[index] = value
        D.append(row)
    _require(
        all(certificate["row_coefficients"][i] is None for i in failed),
        "failed target has fabricated coefficients",
    )
    bank_predicted = _mm(D, B, columns=r)
    bank_residuals = _subtract(bank_predicted, [G[i] for i in recovered])
    source_predicted = _mm(D, interface_values, columns=n)
    source_residuals = _subtract(source_predicted, [Q[i] for i in recovered])
    _require(_zero(bank_residuals), "decoder bank identity fails")
    _require(_zero(source_residuals), "decoder source identity fails")
    complete = not failed
    _require(
        certificate["recoverable"] == complete
        and (certificate["collision"] is None) == complete
        and complete == (len(recovered) == q),
        "complete classification differs",
    )
    v = len(recovered)
    G_recovered = [G[i] for i in recovered]
    C_wire, F_wire, Gr_wire, D_wire = _encode(C), _encode(filters), _encode(G_recovered), _encode(D)
    controls = []
    for control_index in range(r + 1):
        bank_index = None if control_index == 0 else control_index - 1
        z = [F(j == bank_index) for j in range(r)]
        z_wire = _encode(z)
        coarse_values = list(map(_fraction, produce(C_wire, z_wire)))
        supplement_values = list(map(_fraction, produce(F_wire, z_wire)))
        observed = coarse_values + supplement_values
        truth = list(map(_fraction, produce(Gr_wire, z_wire)))
        predicted = list(map(_fraction, apply(D_wire, _encode(observed))))
        residuals = [x - y for x, y in zip(predicted, truth, strict=True)]
        _require(
            coarse_values == [_dot(row, z) for row in C]
            and supplement_values == [_dot(row, z) for row in filters]
            and observed == [_dot(row, z) for row in B],
            "actual interface application differs",
        )
        _require(
            truth == [_dot(row, z) for row in G_recovered]
            and predicted == [_dot(row, observed) for row in D]
            and predicted == truth
            and not any(residuals),
            "actual indexed receiver application differs",
        )
        controls.append(
            {
                "bank_index": bank_index,
                "bank_values": z,
                "coarse_values": coarse_values,
                "supplement_values": supplement_values,
                "observed": observed,
                "truth": truth,
                "predicted": predicted,
                "residuals": residuals,
            }
        )
    checks = dict.fromkeys(
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
    )
    collisions = int(not complete)
    counts = {
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
        "failed_rows": len(failed),
    }
    return _detach(
        {
            "problem": problem,
            "interface": B,
            "source": {
                "interface_values": interface_values,
                "geometric_values": geometric_values,
                "coarse_residuals": coarse_residuals,
                "target_residuals": target_residuals,
            },
            "certificate": certificate,
            "decoder": {
                "target_rows": recovered,
                "matrix": D,
                "bank_predicted": bank_predicted,
                "bank_residuals": bank_residuals,
                "source_predicted": source_predicted,
                "source_residuals": source_residuals,
                "complete": complete,
            },
            "bank_controls": controls,
            "checks": checks,
            "counts": counts,
        }
    )
