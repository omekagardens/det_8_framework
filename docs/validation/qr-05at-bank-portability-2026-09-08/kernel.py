"""Exact frozen receiver portability on supplied partitioned raw bank data."""

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
    _fields(
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
    _require(type(problem["family"]) is str and problem["family"], "nonempty family required")
    coarse, bank_tiles = problem["coarse_tiles"], problem["bank_tiles"]
    _require(type(coarse) is list and 1 <= len(coarse) <= 64, "bounded coarse inventory")
    _require(type(bank_tiles) is list and 1 <= len(bank_tiles) <= 256, "bounded bank inventory")
    c, b = len(coarse), len(bank_tiles)
    for rectangle in coarse:
        _vector_shape(rectangle, 4)
    parents = []
    for tile in bank_tiles:
        _fields(tile, ("bounds", "coarse_tile"))
        _vector_shape(tile["bounds"], 4)
        parent = tile["coarse_tile"]
        _require(type(parent) is int and 0 <= parent < c, "native coarse parent index required")
        parents.append(parent)
    Q = problem["targets"]
    _require(
        type(Q) is list and 1 <= len(Q) <= 64 and type(Q[0]) is list, "bounded target inventory"
    )
    q, n, m, r = len(Q), len(Q[0]), 4 * c, 4 * b
    _require(1 <= n <= 576, "bounded source inventory")
    labels = problem["target_labels"]
    _require(type(labels) is list and len(labels) == q, "complete target labels required")
    label_pairs = []
    for label in labels:
        _fields(label, ("first", "second"))
        _require(
            type(label["first"]) is int and type(label["second"]) is int,
            "native signed target labels required",
        )
        label_pairs.append((label["first"], label["second"]))
    _require(label_pairs == sorted(set(label_pairs)), "target labels must be sorted unique")
    selected = problem["selected_rows"]
    _require(type(selected) is list and len(selected) <= q, "bounded selection inventory")
    _require(
        all(type(i) is int and 0 <= i < q for i in selected),
        "native target selection index required",
    )
    _require(selected == sorted(set(selected)), "selection must be ascending unique")
    k = len(selected)
    for key, rows, width in (
        ("observations", m, n),
        ("bank", r, n),
        ("targets", q, n),
        ("geometric", q, r),
        ("filters", k, r),
        ("receiver", q, m + k),
    ):
        _matrix_shape(problem[key], rows, width)
    _vector_shape(problem["intercept"], q)
    return c, b, m, r, q, n, k, parents


def _overlap(left, right):
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


def _area(rectangle):
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2])


def _partition(coarse, bank, parents):
    for rectangle in coarse + bank:
        _require(
            rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3],
            "positive rectangles required",
        )
    for rectangles in (coarse, bank):
        for i, left in enumerate(rectangles):
            for right in rectangles[i + 1 :]:
                _require(not _overlap(left, right), "rectangle interiors overlap")
    children = [[] for _ in coarse]
    for j, (rectangle, parent) in enumerate(zip(bank, parents, strict=True)):
        outer = coarse[parent]
        _require(
            outer[0] <= rectangle[0] < rectangle[1] <= outer[1]
            and outer[2] <= rectangle[2] < rectangle[3] <= outer[3],
            "bank rectangle outside named parent",
        )
        children[parent].append(j)
    for i, indices in enumerate(children):
        _require(indices, "parent lacks children")
        _require(
            sum((_area(bank[j]) for j in indices), F(0)) == _area(coarse[i]),
            "children do not cover parent",
        )
    return children


def produce(matrix, values):
    _native(matrix)
    _native(values)
    _require(type(values) is list and len(values) <= 1024, "bounded raw value width")
    _require(type(matrix) is list and len(matrix) <= 320, "bounded producer row inventory")
    _vector_shape(values, len(values))
    _matrix_shape(matrix, len(matrix), len(values))
    rows, vector = _matrix(matrix), list(map(_fraction, values))
    return _detach([_dot(row, vector) for row in rows])


def apply(intercept, matrix, observed):
    _native(intercept)
    _native(matrix)
    _native(observed)
    _require(
        type(intercept) is list and 1 <= len(intercept) <= 64, "bounded receiver row inventory"
    )
    _require(type(observed) is list and len(observed) <= 320, "bounded receiver input width")
    _vector_shape(intercept, len(intercept))
    _vector_shape(observed, len(observed))
    _matrix_shape(matrix, len(intercept), len(observed))
    offsets, rows, vector = (
        list(map(_fraction, intercept)),
        _matrix(matrix),
        list(map(_fraction, observed)),
    )
    return _detach([offset + _dot(row, vector) for offset, row in zip(offsets, rows, strict=True)])


def _subtract(left, right):
    return [[x - y for x, y in zip(a, b, strict=True)] for a, b in zip(left, right, strict=True)]


def _zero(matrix):
    return not any(value for row in matrix for value in row)


def build_family(problem):
    c, b, m, r, q, n, k, parents = _preflight(problem)
    coarse = _matrix(problem["coarse_tiles"])
    bank_rectangles = _matrix([tile["bounds"] for tile in problem["bank_tiles"]])
    O, R, Q, G = (_matrix(problem[key]) for key in ("observations", "bank", "targets", "geometric"))
    filters, L = _matrix(problem["filters"]), _matrix(problem["receiver"])
    a = list(map(_fraction, problem["intercept"]))
    children = _partition(coarse, bank_rectangles, parents)
    selected = problem["selected_rows"]
    _require(filters == [G[i] for i in selected], "selected filters differ from supplied G")
    C = [[F(parents[j // 4] == i // 4 and j % 4 == i % 4) for j in range(r)] for i in range(m)]
    coarse_predicted = _mm(C, R)
    coarse_residuals = _subtract(coarse_predicted, O)
    _require(_zero(coarse_residuals), "coarse source identity fails")
    H = _mm(filters, R)
    _require(H == [Q[i] for i in selected], "supplement source identity fails")
    geometric_source = _mm(G, R)
    geometric_residuals = _subtract(geometric_source, Q)
    _require(_zero(geometric_residuals), "geometric source identity fails")
    receiver_linear = _mm(L, O + H)
    receiver_source = [
        [offset + x for x in row] for offset, row in zip(a, receiver_linear, strict=True)
    ]
    direct_residuals = _subtract(receiver_source, Q)
    _require(_zero(direct_residuals), "receiver source identity fails")
    coarse_effect = _mm([row[:m] for row in L], C)
    supplement_effect = _mm([row[m:] for row in L], filters, columns=r)
    K = [
        [x + y for x, y in zip(left, right, strict=True)]
        for left, right in zip(coarse_effect, supplement_effect, strict=True)
    ]
    E = _subtract(K, G)
    defect_on_sources = _mm(E, R)
    source_residuals = [
        [offset + x for x in row] for offset, row in zip(a, defect_on_sources, strict=True)
    ]
    _require(
        source_residuals == direct_residuals and _zero(source_residuals),
        "composed source residual identity fails",
    )
    nonzero_intercepts = [i for i, value in enumerate(a) if value]
    nonzero_defects = [i for i, row in enumerate(E) if any(row)]
    restricted = sorted(set(nonzero_intercepts) | set(nonzero_defects))
    structural = [i for i in range(q) if i not in restricted]
    controls = []
    first_failure = None
    C_wire, F_wire, G_wire = _encode(C), _encode(filters), _encode(G)
    a_wire, L_wire = _encode(a), _encode(L)
    for control_index in range(r + 1):
        bank_index = None if control_index == 0 else control_index - 1
        z = [F(j == bank_index) for j in range(r)]
        z_wire = _encode(z)
        coarse_values = list(map(_fraction, produce(C_wire, z_wire)))
        supplement_values = list(map(_fraction, produce(F_wire, z_wire)))
        observed = coarse_values + supplement_values
        truth = list(map(_fraction, produce(G_wire, z_wire)))
        predicted = list(map(_fraction, apply(a_wire, L_wire, _encode(observed))))
        residuals = [x - y for x, y in zip(predicted, truth, strict=True)]
        affine_defect = [offset + _dot(row, z) for offset, row in zip(a, E, strict=True)]
        _require(coarse_values == [_dot(row, z) for row in C], "coarse control identity fails")
        _require(
            supplement_values == [_dot(row, z) for row in filters],
            "supplement control identity fails",
        )
        _require(truth == [_dot(row, z) for row in G], "truth control identity fails")
        _require(
            predicted == [offset + _dot(row, observed) for offset, row in zip(a, L, strict=True)],
            "receiver control identity fails",
        )
        _require(residuals == affine_defect, "affine control identity fails")
        if first_failure is None:
            first = next((i for i, value in enumerate(residuals) if value), None)
            if first is not None:
                first_failure = {"control_index": control_index, "target_row": first}
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
                "affine_defect": affine_defect,
            }
        )
    for i in range(q):
        _require(
            (i in structural) == all(not row["residuals"][i] for row in controls),
            "per-row structural classification differs from controls",
        )
    _require((first_failure is None) == (not restricted), "global structural classification fails")
    checks = dict.fromkeys(
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
    )
    counts = {
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
        "nonzero_defect_entries": sum(bool(x) for row in E for x in row),
        "nonzero_intercept_entries": len(nonzero_intercepts),
        "source_check_entries": 2 * m * n + k * n + 5 * q * n,
        "bank_controls": r + 1,
        "bank_control_entries": (r + 1) * (r + 2 * m + 2 * k + 4 * q),
        "structural_rows": len(structural),
        "restricted_only_rows": len(restricted),
    }
    return _detach(
        {
            "problem": problem,
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
                "restricted_only_rows": restricted,
                "nonzero_intercept_rows": nonzero_intercepts,
                "nonzero_defect_rows": nonzero_defects,
                "unrestricted_exact": not restricted,
                "first_failure": first_failure,
            },
            "bank_controls": controls,
            "checks": checks,
            "counts": counts,
        }
    )
