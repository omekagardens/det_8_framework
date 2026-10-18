"""Independent exact convex-quadratic reference for QR-05AD.

Static own-lineage native guards. The optimizer certifies supplied polynomials,
not observation-law provenance. Critical-point evaluation and completion of
squares establish the entire optimizer set, including a flat interval.
"""

import hashlib
import json
from fractions import Fraction as F
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 65536
MAX_BYTES = 1048576
MAX_DECISIONS = 16
MAX_CRITICAL_POINTS = 48
MAX_VALUE_EVALUATIONS = 96
MAX_TOTAL_WORK = 320
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
RETAINED_WEIGHTS = (F(0), F(1, 2), F(1))
CHECKS = (
    "convexity",
    "critical_candidates_complete",
    "optimizer_set_complete",
    "global_kkt_certificate",
    "finite_menu_complete",
    "finite_menu_argmin_complete",
    "finite_menu_gap_nonnegative",
    "menu_grid_error_bound",
    "coarse_option_available",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _fields(obj, names, message):
    _require(
        type(obj) is dict and all(type(k) is str for k in obj) and set(obj) == set(names), message
    )


def _string_bytes(value):
    # Exact ensure_ascii=True JSON size without serializing an unbounded tree.
    _require(type(value) is str, "native object key or string")
    _require(len(value) <= MAX_BYTES, "string byte cap")
    count = 2
    for char in value:
        code = ord(char)
        if char in ('"', "\\", "\b", "\t", "\n", "\f", "\r"):
            count += 2
        elif code < 32 or code >= 127:
            count += 6 if code <= 65535 else 12
        else:
            count += 1
        _require(count <= MAX_BYTES, "escaped string byte cap")
    return count


def _native(value):
    # Nodes are JSON values, not object keys. A scalar/empty container has
    # height zero: root depth is zero and deepest scalar leaves count.
    pending, active, complete = [(value, False, 0)], set(), {}

    def scalar(v):
        if v is None:
            return (1, 0, 4)
        if type(v) is bool:
            return (1, 0, 4 if v else 5)
        if type(v) is str:
            return (1, 0, _string_bytes(v))
        if type(v) is int:
            _require(abs(v).bit_length() <= MAX_BITS, "native integer component bit cap")
            return (1, 0, len(str(v)))
        _require(type(v) in (list, dict), "non-native JSON value")
        return None

    while pending:
        current, leaving, depth = pending.pop()
        _require(depth <= MAX_DEPTH, "early native traversal depth cap")
        simple = scalar(current)
        if simple is not None:
            continue
        identity = id(current)
        if leaving:
            children = list(current.values()) if type(current) is dict else current
            nodes, height = 1, 0
            size = 2 + max(0, len(children) - 1)
            if type(current) is dict:
                for key in current:
                    size += _string_bytes(key) + 1
                    _require(size <= MAX_BYTES, "object-key expanded byte cap")
            for child in children:
                info = complete[id(child)] if type(child) in (list, dict) else scalar(child)
                nodes += info[0]
                height = max(height, info[1] + 1)
                size += info[2]
                _require(nodes <= MAX_NODES, "expanded value-node cap")
                _require(height <= MAX_DEPTH, "native depth cap")
                _require(size <= MAX_BYTES, "expanded canonical byte cap")
            _require(
                nodes <= MAX_NODES and height <= MAX_DEPTH and size <= MAX_BYTES,
                "native tree resource cap",
            )
            complete[identity] = (nodes, height, size)
            active.remove(identity)
            continue
        _require(identity not in active, "cyclic JSON container")
        if identity in complete:
            _require(depth + complete[identity][1] <= MAX_DEPTH, "cached subtree depth cap")
            continue
        _require(len(current) + 1 <= MAX_NODES, "container width value-node lower bound")
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native object key")
        active.add(identity)
        pending.append((current, True, depth))
        children = current.values() if type(current) is dict else current
        pending.extend((child, False, depth + 1) for child in children)
    info = complete[id(value)] if type(value) in (list, dict) else scalar(value)
    _require(
        info[0] <= MAX_NODES and info[1] <= MAX_DEPTH and info[2] + 1 <= MAX_BYTES,
        "complete expanded native wire cap",
    )


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, OverflowError, RecursionError, ValueError) as error:
        raise ValueError("canonical JSON serialization failed") from error


def _fraction(value, lower, upper):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    n, d = value
    _require(type(n) is int and type(d) is int, "native rational components")
    _require(d > 0 and lower * d <= n <= upper * d, "rational input interval")
    _require(gcd(n, d) == 1, "reduced rational input")
    _require(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "input component bit cap")
    return F(n, d)


def _wire(value, lower, upper):
    _require(type(value) is F and lower <= value <= upper, "retained exact rational interval")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained component bit cap",
    )
    return [value.numerator, value.denominator]


def _stationary(A, B):
    _require(type(A) is F and type(B) is F and 0 < B < A, "strict interior stationary division")
    result = B / A
    _wire(result, 0, 1)
    return result


def _coefficients(A, B):
    _require(type(A) is F and type(B) is F, "exact coefficient inputs")
    linear, curvature = -2 * B, 2 * A
    _wire(linear, -4, 4)
    _wire(curvature, 0, 4)
    return linear, curvature


def _gradient(A, B, weight):
    _require(all(type(v) is F for v in (A, B, weight)), "exact gradient inputs")
    result = 2 * A * weight - 2 * B
    _wire(result, -4, 8)
    return result


def _evaluate(A, B, weight):
    _require(all(type(v) is F for v in (A, B, weight)), "exact polynomial inputs")
    result = A * weight * weight - 2 * B * weight
    _wire(result, -4, 6)
    return result


def _gap(left, right):
    _require(type(left) is F and type(right) is F, "exact gap inputs")
    result = left - right
    _wire(result, 0, 6)
    return result


def _prepare(problem):
    _native(problem)
    _fields(
        problem,
        ("schema_version", "family", "levels", "retained_weights", "decisions"),
        "exact AD problem fields",
    )
    _require(problem["schema_version"] == "det8-qr05ad-problem-v1", "AD schema")
    _require(problem["family"] == "qr05ad_continuous_retention", "AD family")
    for key, expected in (("levels", LEVELS), ("retained_weights", RETAINED_WEIGHTS)):
        _require(
            type(problem[key]) is list and len(problem[key]) == len(expected), "fixed label count"
        )
        _require(tuple(_fraction(v, 0, 1) for v in problem[key]) == expected, "fixed labels")
    rows = problem["decisions"]
    _require(type(rows) is list and len(rows) == 16, "sixteen ordered quadratic decisions")
    parsed = []
    for index, row in enumerate(rows):
        _fields(
            row,
            ("assumed_index", "bound_index", "quadratic_coefficient", "half_linear_coefficient"),
            "exact quadratic decision",
        )
        _require(
            type(row["assumed_index"]) is int and row["assumed_index"] == index // 4,
            "native ordered assumed index",
        )
        _require(
            type(row["bound_index"]) is int and row["bound_index"] == index % 4,
            "native ordered bound index",
        )
        parsed.append(
            (
                _fraction(row["quadratic_coefficient"], 0, 2),
                _fraction(row["half_linear_coefficient"], -2, 2),
            )
        )
    interior = sum(0 < B < A for A, B in parsed)
    points = sum(A != 0 or B != 0 for A, B in parsed)
    critical = 32 + interior
    counts = {
        "decisions": 16,
        "critical_candidates": critical,
        "value_evaluations": critical + 48,
        "point_optimizers": points,
        "interval_optimizers": 16 - points,
        "interior_point_optimizers": interior,
        "optimizer_classifications": 16,
        "coefficient_visits": 16,
        "gradient_terms": points,
        "stationary_divisions": interior,
        "critical_value_terms": critical,
        "menu_value_terms": 48,
        "critical_selection_visits": critical,
        "menu_selection_visits": 48,
        "gap_terms": 64,
        "total_work_terms": 192 + points + interior + 2 * critical,
    }
    _require(16 <= MAX_DECISIONS, "planned decisions cap")
    _require(critical <= MAX_CRITICAL_POINTS, "planned critical point cap")
    _require(critical + 48 <= MAX_VALUE_EVALUATIONS, "planned value evaluation cap")
    _require(counts["total_work_terms"] <= MAX_TOTAL_WORK, "planned total work cap")
    return parsed, counts


def analyze(problem):
    """Certify every optimizer and finite-menu comparator on the closed interval."""
    rows, counts = _prepare(problem)
    visited = dict.fromkeys(
        (
            "optimizer_classifications",
            "coefficient_visits",
            "gradient_terms",
            "stationary_divisions",
            "critical_value_terms",
            "menu_value_terms",
            "critical_selection_visits",
            "menu_selection_visits",
            "gap_terms",
        ),
        0,
    )
    output = []
    lower_count = upper_count = menu_occurrences = 0
    for index, (A, B) in enumerate(rows):
        visited["optimizer_classifications"] += 1
        interval = A == 0 and B == 0
        interior = 0 < B < A
        linear, curvature = _coefficients(A, B)
        visited["coefficient_visits"] += 1
        weights = [F(0), F(1)]
        if interior:
            weights.insert(1, _stationary(A, B))
            visited["stationary_divisions"] += 1
        _require(
            weights == sorted(set(weights)) and weights[0] == 0 and weights[-1] == 1,
            "complete distinct critical candidates",
        )
        _require(len(weights) == 2 + int(interior), "complete strict interior stationary candidate")
        values = []
        minimum = None
        for weight in weights:
            value = _evaluate(A, B, weight)
            values.append(value)
            visited["critical_value_terms"] += 1
            if minimum is None or value < minimum:
                minimum = value
            visited["critical_selection_visits"] += 1
        _wire(minimum, -4, 0)
        minimizing_weights = [
            weight for weight, value in zip(weights, values, strict=True) if value == minimum
        ]
        _require(curvature >= 0, "convex quadratic")
        if interval:
            _require(
                A == B == minimum == 0 and minimizing_weights == weights,
                "complete zero polynomial optimizer interval",
            )
            optimizer = {"kind": "interval", "lower": [0, 1], "upper": [1, 1]}
            proof = {
                "kind": "zero_polynomial",
                "anchor": None,
                "gradient": None,
                "second_derivative": _wire(curvature, 0, 4),
            }
        else:
            _require(len(minimizing_weights) == 1, "unique nonflat optimizer")
            anchor = minimizing_weights[0]
            gradient = _gradient(A, B, anchor)
            visited["gradient_terms"] += 1
            if anchor == 0:
                _require(gradient >= 0, "lower endpoint KKT sign")
                lower_count += 1
            elif anchor == 1:
                _require(gradient <= 0, "upper endpoint KKT sign")
                upper_count += 1
            else:
                _require(gradient == 0 and A > 0, "interior stationary KKT")
            # Compare polynomial coefficients, not a sampled identity:
            # Q(a)-Q(anchor) = A(a-anchor)^2 + gradient*(a-anchor).
            _require(
                gradient - 2 * A * anchor == linear,
                "global completion-of-squares linear coefficient",
            )
            _require(
                A * anchor * anchor - gradient * anchor == -minimum,
                "global completion-of-squares constant coefficient",
            )
            _require(
                (A > 0) or (B != 0 and gradient != 0),
                "nonflat strict convexity or strict linear direction gives unique point",
            )
            optimizer = {"kind": "point", "weight": _wire(anchor, 0, 1)}
            proof = {
                "kind": "point_kkt",
                "anchor": _wire(anchor, 0, 1),
                "gradient": _wire(gradient, -4, 8),
                "second_derivative": _wire(curvature, 0, 4),
            }
        menu, menu_values = [], []
        best_menu = None
        for weight in RETAINED_WEIGHTS:
            value = _evaluate(A, B, weight)
            visited["menu_value_terms"] += 1
            gap = _gap(value, minimum)
            visited["gap_terms"] += 1
            menu_values.append(value)
            menu.append(
                {
                    "retained_weight": _wire(weight, 0, 1),
                    "value": _wire(value, -4, 6),
                    "excess_over_minimum": _wire(gap, 0, 6),
                }
            )
            if best_menu is None or value < best_menu:
                best_menu = value
            visited["menu_selection_visits"] += 1
        menu_minimizers = [i for i, value in enumerate(menu_values) if value == best_menu]
        menu_occurrences += len(menu_minimizers)
        _require(menu_values[0] == 0 and minimum <= best_menu <= 0, "coarse option available")
        _require(
            bool(menu_minimizers) and all(v >= best_menu for v in menu_values),
            "complete exact finite menu minimum",
        )
        grid_gap = _gap(best_menu, minimum)
        visited["gap_terms"] += 1
        _require(0 <= grid_gap <= F(1, 8) and 16 * grid_gap <= A, "exact menu grid error bound")
        if not interval:
            if anchor in (0, 1):
                _require(grid_gap == 0, "boundary optimizer lies in finite menu")
            else:
                _require(
                    min(abs(weight - anchor) for weight in RETAINED_WEIGHTS) <= F(1, 4),
                    "nearest menu grid weight",
                )
                _require(
                    all(
                        value - minimum == A * (weight - anchor) ** 2
                        for weight, value in zip(RETAINED_WEIGHTS, menu_values, strict=True)
                    ),
                    "stationary menu regret identity",
                )
        else:
            _require(grid_gap == 0 and menu_minimizers == [0, 1, 2], "flat menu ties complete")
        output.append(
            {
                "assumed_index": index // 4,
                "bound_index": index % 4,
                "quadratic_coefficient": _wire(A, 0, 2),
                "half_linear_coefficient": _wire(B, -2, 2),
                "linear_coefficient": _wire(linear, -4, 4),
                "critical_candidates": [
                    {"retained_weight": _wire(weight, 0, 1), "value": _wire(value, -4, 6)}
                    for weight, value in zip(weights, values, strict=True)
                ],
                "optimizer": optimizer,
                "minimum": _wire(minimum, -4, 0),
                "finite_menu": menu,
                "finite_menu_minimum": _wire(best_menu, -4, 0),
                "finite_menu_minimizer_indices": menu_minimizers,
                "finite_menu_minimizer_weights": [
                    _wire(RETAINED_WEIGHTS[i], 0, 1) for i in menu_minimizers
                ],
                "finite_menu_gap": _wire(grid_gap, 0, F(1, 8)),
                "proof": proof,
                "checks": dict.fromkeys(CHECKS, True),
            }
        )
    _require(all(visited[key] == counts[key] for key in visited), "planned and executed exact work")
    _require(sum(visited.values()) == counts["total_work_terms"], "complete declared work sum")
    counts.update(
        {
            "lower_endpoint_optimizers": lower_count,
            "upper_endpoint_optimizers": upper_count,
            "finite_menu_minimizer_occurrences": menu_occurrences,
        }
    )
    _require(
        lower_count + upper_count + counts["interior_point_optimizers"]
        == counts["point_optimizers"],
        "complete point classification",
    )
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "levels": [_wire(t, 0, 1) for t in LEVELS],
        "retained_weights": [_wire(a, 0, 1) for a in RETAINED_WEIGHTS],
        "decisions": output,
        "counts": counts,
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "complete detached output bytes")
    return json.loads(encoded)
