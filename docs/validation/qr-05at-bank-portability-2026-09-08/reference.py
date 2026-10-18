"""QR-05AT independent reference: frozen zero/unit pipelines identify the map.

Only supplied rectangles, matrices and raw values are consumed. No historical
executor, source fixture or hidden geometry is imported or read.
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
    """Reject active cycles without rejecting detached-compatible shared DAGs."""
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
    _need(all(type(row) is list and len(row) == columns for row in matrix), "matrix width")


def _pair_shapes(values):
    _need(all(type(x) is list and len(x) == 2 for x in values), "rational pair shapes")


def _matrix_pair_shapes(matrix):
    for row in matrix:
        _pair_shapes(row)


def _matrix(matrix):
    return [[_fraction(x) for x in row] for row in matrix]


def _dot(row, vector):
    return sum((a * b for a, b in zip(row, vector) if a and b), ZERO)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _multiply(left, right, columns):
    if not right:
        return [[ZERO] * columns for _ in left]
    transposed = list(zip(*right))
    _need(len(transposed) == columns, "internal product width")
    return [[_dot(row, col) for col in transposed] for row in left]


def produce(matrix, values):
    """Evaluate only a supplied raw matrix and vector, including empty widths."""
    _native(matrix)
    _native(values)
    _need(type(matrix) is list and len(matrix) <= 320, "producer row inventory")
    _need(type(values) is list and len(values) <= 1024, "producer value inventory")
    _dimensions(matrix, len(matrix), len(values))
    _matrix_pair_shapes(matrix)
    _pair_shapes(values)
    rows = _matrix(matrix)
    vector = [_fraction(x) for x in values]
    return _wire(_matvec(rows, vector))


def apply(intercept, matrix, observed):
    """Evaluate only the supplied frozen affine map and ordered values."""
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
    vector = [_fraction(x) for x in observed]
    return _wire([a + _dot(row, vector) for a, row in zip(offsets, rows)])


def _parse(problem):
    _native(problem)
    _keys(
        problem,
        (
            "family",
            "coarse_tiles",
            "bank_tiles",
            "target_labels",
            "observations",
            "bank",
            "targets",
            "geometric",
            "selected_rows",
            "filters",
            "intercept",
            "receiver",
        ),
    )
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    coarse, bank_tiles = problem["coarse_tiles"], problem["bank_tiles"]
    _need(type(coarse) is list and 1 <= len(coarse) <= 64, "coarse tile inventory")
    _need(type(bank_tiles) is list and 1 <= len(bank_tiles) <= 256, "bank tile inventory")
    c, b = len(coarse), len(bank_tiles)
    m, r = 4 * c, 4 * b
    _dimensions(coarse, c, 4)
    bank_bounds, parents = [], []
    for tile in bank_tiles:
        _keys(tile, ("bounds", "coarse_tile"))
        _need(type(tile["bounds"]) is list and len(tile["bounds"]) == 4, "bank bounds")
        parent = tile["coarse_tile"]
        _need(type(parent) is int and 0 <= parent < c, "bank parent index")
        bank_bounds.append(tile["bounds"])
        parents.append(parent)
    O, R, Q, G, F, a, L = (
        problem[key]
        for key in (
            "observations",
            "bank",
            "targets",
            "geometric",
            "filters",
            "intercept",
            "receiver",
        )
    )
    _need(type(Q) is list and 1 <= len(Q) <= 64 and type(Q[0]) is list, "target inventory")
    q, n = len(Q), len(Q[0])
    _need(1 <= n <= 576, "source inventory")
    selected = problem["selected_rows"]
    _need(type(selected) is list and len(selected) <= q, "selected row inventory")
    _need(all(type(i) is int and 0 <= i < q for i in selected), "selected row index")
    _need(selected == sorted(set(selected)), "selected rows ascending unique")
    k = len(selected)
    for matrix, rows, columns in (
        (O, m, n),
        (R, r, n),
        (Q, q, n),
        (G, q, r),
        (F, k, r),
        (L, q, m + k),
    ):
        _dimensions(matrix, rows, columns)
    _need(type(a) is list and len(a) == q, "intercept inventory")
    labels = problem["target_labels"]
    _need(type(labels) is list and len(labels) == q, "target label inventory")
    pairs = []
    for label in labels:
        _keys(label, ("first", "second"))
        _need(type(label["first"]) is int and type(label["second"]) is int, "signed target IDs")
        pairs.append((label["first"], label["second"]))
    _need(pairs == sorted(set(pairs)), "target label order")
    for matrix in (coarse, bank_bounds, O, R, Q, G, F, L):
        _matrix_pair_shapes(matrix)
    _pair_shapes(a)
    # All dimensions, indices and pair SHAPES are known before any Fraction.
    # Parse every scalar VALUE before partition arithmetic or matrix work.
    coarse, bank_bounds, O, R, Q, G, F, L = (
        _matrix(matrix) for matrix in (coarse, bank_bounds, O, R, Q, G, F, L)
    )
    a = [_fraction(x) for x in a]
    return coarse, bank_bounds, parents, O, R, Q, G, F, a, L, selected, n


def _overlap(left, right):
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


def _area(rectangle):
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])


def _partition(coarse, bank, parents):
    """Containment plus disjoint interiors and exact positive areas certify coverage."""
    for rectangle in coarse + bank:
        _need(rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3], "positive rectangle")
    for inventory in (coarse, bank):
        for i, left in enumerate(inventory):
            for right in inventory[i + 1 :]:
                _need(not _overlap(left, right), "disjoint rectangle interiors")
    children = [[] for _ in coarse]
    for j, (child, parent) in enumerate(zip(bank, parents)):
        rectangle = coarse[parent]
        _need(
            rectangle[0] <= child[0] < child[1] <= rectangle[1]
            and rectangle[2] <= child[2] < child[3] <= rectangle[3],
            "bank containment in named parent",
        )
        children[parent].append(j)
    for parent, child_indices in enumerate(children):
        _need(bool(child_indices), "every parent has children")
        _need(
            sum((_area(bank[j]) for j in child_indices), ZERO) == _area(coarse[parent]),
            "complete parent area coverage",
        )
    return children


def _difference(left, right):
    return [[a - b for a, b in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]


def _all_zero(matrix):
    return not any(value for row in matrix for value in row)


def build_family(problem):
    """Certify a frozen map on sources and diagnose its full affine bank defect."""
    coarse, bank_tiles, parents, O, R, Q, G, F, a, L, selected, n = _parse(problem)
    c, b, q, k = len(coarse), len(bank_tiles), len(Q), len(F)
    m, r = len(O), len(R)
    children = _partition(coarse, bank_tiles, parents)
    C = []
    for child_indices in children:
        for basis in range(4):
            row = [ZERO] * r
            for child in child_indices:
                row[4 * child + basis] = ONE
            C.append(row)
    coarse_predicted = _multiply(C, R, n)
    coarse_residuals = _difference(coarse_predicted, O)
    _need(_all_zero(coarse_residuals), "coarse source identity")
    _need(F == [G[i] for i in selected], "literal selected filters")
    H = _multiply(F, R, n)
    _need(H == [Q[i] for i in selected], "selected source identity")
    geometric_source = _multiply(G, R, n)
    geometric_residuals = _difference(geometric_source, Q)
    _need(_all_zero(geometric_residuals), "geometric source identity")
    receiver_source = _multiply(L, O + H, n)
    receiver_source = [[a[i] + value for value in row] for i, row in enumerate(receiver_source)]
    direct_residuals = _difference(receiver_source, Q)
    _need(_all_zero(direct_residuals), "frozen receiver source identity")

    # No Lc*C + Lh*F product is used to construct K. Each column is recovered
    # from actual restricted online evaluation, subtracting its zero-bank offset.
    C_wire = _wire(C)
    controls = []
    for control_index in range(r + 1):
        z = [ZERO] * r
        bank_index = None if control_index == 0 else control_index - 1
        if bank_index is not None:
            z[bank_index] = ONE
        z_wire = _wire(z)
        coarse_wire = produce(C_wire, z_wire)
        supplement_wire = produce(problem["filters"], z_wire)
        truth_wire = produce(problem["geometric"], z_wire)
        observed_wire = coarse_wire + supplement_wire
        predicted_wire = apply(problem["intercept"], problem["receiver"], observed_wire)
        coarse_values, supplement_values, observed, truth, predicted = (
            [_fraction(x) for x in values]
            for values in (coarse_wire, supplement_wire, observed_wire, truth_wire, predicted_wire)
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
                "residuals": [value - actual for value, actual in zip(predicted, truth)],
            }
        )
    origin = controls[0]
    _need(origin["predicted"] == a and origin["residuals"] == a, "zero-bank intercept")
    K = [
        [controls[j + 1]["predicted"][i] - origin["predicted"][i] for j in range(r)]
        for i in range(q)
    ]
    E = _difference(K, G)
    defect_on_sources = _multiply(E, R, n)
    source_residuals = [[a[i] + x for x in row] for i, row in enumerate(defect_on_sources)]
    _need(
        source_residuals == direct_residuals and _all_zero(source_residuals),
        "affine source identity",
    )
    first_failure = None
    for index, control in enumerate(controls):
        control["affine_defect"] = [
            a[i] + value for i, value in enumerate(_matvec(E, control["bank_values"]))
        ]
        _need(control["residuals"] == control["affine_defect"], "full affine probe identity")
        failed = next((i for i, value in enumerate(control["residuals"]) if value), None)
        if first_failure is None and failed is not None:
            first_failure = {"control_index": index, "target_row": failed}
    nonzero_intercept_rows = [i for i, value in enumerate(a) if value]
    nonzero_defect_rows = [i for i, row in enumerate(E) if any(row)]
    restricted_only = [i for i in range(q) if a[i] or any(E[i])]
    structural = [i for i in range(q) if i not in restricted_only]
    _need((first_failure is None) == (not restricted_only), "global structural classification")
    for i in range(q):
        _need(
            all(control["residuals"][i] == ZERO for control in controls) == (i in structural),
            "complete per-row structural classification",
        )
    result = {
        "problem": deepcopy(problem),
        "lineage": {
            "coarse_children": children,
            "coarse_map": C,
            "coarse_predicted": coarse_predicted,
            "coarse_residuals": coarse_residuals,
        },
        "composition": {
            "supplement_source": H,
            "geometric_source": geometric_source,
            "geometric_residuals": geometric_residuals,
            "receiver_source": receiver_source,
            "source_residuals": source_residuals,
            "effective_map": K,
            "coefficient_defect": E,
            "defect_on_sources": defect_on_sources,
        },
        "classification": {
            "structural_rows": structural,
            "restricted_only_rows": restricted_only,
            "nonzero_intercept_rows": nonzero_intercept_rows,
            "nonzero_defect_rows": nonzero_defect_rows,
            "unrestricted_exact": not restricted_only,
            "first_failure": first_failure,
        },
        "bank_controls": controls,
        "checks": dict.fromkeys(
            (
                "lineage_partition",
                "coarse_source_identity",
                "inherited_geometric_identity",
                "selected_filter_identity",
                "source_receiver_identity",
                "affine_probe_identity",
                "structural_classification",
            ),
            True,
        ),
        "counts": {
            "coarse_tiles": c,
            "bank_tiles": b,
            "source_columns": n,
            "coarse_values": m,
            "bank_values": r,
            "target_rows": q,
            "supplement_values": k,
            "receiver_values": m + k,
            "input_rational_entries": 4 * c
            + 4 * b
            + m * n
            + r * n
            + q * n
            + q * r
            + k * r
            + q
            + q * (m + k),
            "coarse_map_entries": m * r,
            "effective_map_entries": q * r,
            "defect_entries": q * r,
            "nonzero_defect_entries": sum(bool(value) for row in E for value in row),
            "nonzero_intercept_entries": len(nonzero_intercept_rows),
            "source_check_entries": 2 * m * n + k * n + 5 * q * n,
            "bank_controls": r + 1,
            "bank_control_entries": (r + 1) * (r + 2 * m + 2 * k + 4 * q),
            "structural_rows": len(structural),
            "restricted_only_rows": len(restricted_only),
        },
    }
    return _wire(result)
