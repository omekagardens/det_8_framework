"""Exact interval minimization for supplied convex quadratics.

The native guard is statically carried from this primary's own lineage.
No prior or alternative executor is imported; physical origins are not
inferred from the supplied polynomial coefficients.
"""

import hashlib
import json
from fractions import Fraction
from itertools import pairwise
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 65536
MAX_BYTES = 1048576
MAX_DECISIONS = 16
MAX_CRITICAL_POINTS = 48
MAX_VALUE_EVALUATIONS = 96
MAX_TOTAL_WORK = 320

LEVELS = (Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1))
RETAINED_WEIGHTS = (Fraction(0), Fraction(1, 2), Fraction(1))


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _string_size(value):
    _require(len(value) <= MAX_BYTES, "native string exceeds its byte cap")
    size = 2
    _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    for character in value:
        code = ord(character)
        if character in ('"', "\\") or code in (8, 9, 10, 12, 13):
            size += 2
        elif 32 <= code <= 126:
            size += 1
        elif code <= 65535:
            size += 6
        else:
            size += 12
        _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    return size


def _scalar_info(value):
    kind = type(value)
    if value is None:
        return 1, 0, 4
    if kind is bool:
        return 1, 0, 4 if value else 5
    if kind is str:
        return 1, 0, _string_size(value)
    if kind is int:
        _require(value.bit_length() <= MAX_BITS, "native integer exceeds its bit cap")
        return 1, 0, len(str(value))
    raise ValueError("expected exact native JSON value")


def _native(value):
    """Preflight expanded JSON value nodes, root-zero depth and exact bytes."""
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        _require(depth <= MAX_DEPTH, "native value exceeds depth cap")
        kind = type(item)
        if kind not in (list, dict):
            nodes, height, size = _scalar_info(item)
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native scalar exceeds cap")
            continue
        if leaving:
            active.remove(id(item))
            nodes, height, size = 1, 0, 2 + max(0, len(item) - 1)
            values = item if kind is list else item.values()
            if kind is dict:
                size += sum(_string_size(key) + 1 for key in item)
            for child in values:
                info = completed[id(child)] if type(child) in (list, dict) else _scalar_info(child)
                child_nodes, child_height, child_size = info
                nodes += child_nodes
                height = max(height, child_height + 1)
                size += child_size
                _require(nodes <= MAX_NODES, "expanded native node cap exceeded")
                _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native container exceeds cap")
            completed[id(item)] = nodes, height, size
            continue
        _require(id(item) not in active, "cyclic native JSON is invalid")
        if id(item) in completed:
            nodes, height, size = completed[id(item)]
            _require(depth + height <= MAX_DEPTH, "shared subtree exceeds depth cap")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "shared subtree exceeds cap")
            continue
        if kind is dict:
            _require(all(type(key) is str for key in item), "object keys must be native strings")
        _require(1 + len(item) <= MAX_NODES, "expanded native node cap exceeded")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if kind is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))
    if type(value) in (list, dict):
        nodes, height, size = completed[id(value)]
    else:
        nodes, height, size = _scalar_info(value)
    _require(height <= MAX_DEPTH and nodes <= MAX_NODES, "expanded native tree cap exceeded")
    _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
    return size + 1


def canonical(value):
    expected_bytes = _native(value)
    data = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    _require(len(data) == expected_bytes, "canonical size preflight disagrees with serialization")
    _require(len(data) <= MAX_BYTES, "canonical byte cap exceeded")
    return data


def _fields(value, names):
    _require(type(value) is dict and set(value) == set(names), "unexpected object fields")


def _integer(value, minimum, maximum):
    _require(
        type(value) is int and minimum <= value <= maximum and value.bit_length() <= MAX_BITS,
        "native integer outside declared bounds",
    )


def _fraction(value, lower, upper):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0
        and max(numerator.bit_length(), denominator.bit_length()) <= MAX_BITS,
        "invalid native fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must already be reduced")
    result = Fraction(numerator, denominator)
    _require(lower <= result <= upper, "fraction outside declared coefficient range")
    return result


def _retained(value, lower, upper):
    _require(
        type(value) is Fraction
        and lower <= value <= upper
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational outside range or bit bounds",
    )
    return value


def _pair(value, lower, upper):
    _retained(value, lower, upper)
    return [value.numerator, value.denominator]


def _stationary(A, B):
    _require(A > 0 and 0 < B < A, "only strict interior stationary division is allowed")
    return _retained(B / A, 0, 1)


def _coefficients(A, B):
    return _retained(-2 * B, -4, 4), _retained(2 * A, 0, 4)


def _gradient(A, B, a):
    return _retained(2 * A * a - 2 * B, -4, 8)


def _evaluate(A, B, a):
    return _retained(A * a * a - 2 * B * a, -4, 6)


def _gap(left, right):
    return _retained(left - right, 0, 6)


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "levels", "retained_weights", "decisions"))
    _require(
        problem["schema_version"] == "det8-qr05ad-problem-v1"
        and problem["family"] == "qr05ad_continuous_retention",
        "unknown continuous-retention schema",
    )
    for name, expected in (("levels", LEVELS), ("retained_weights", RETAINED_WEIGHTS)):
        values = problem[name]
        _require(type(values) is list and len(values) == len(expected), "fixed menu size differs")
        _require(
            tuple(_fraction(value, 0, 1) for value in values) == expected,
            "fixed menu order differs",
        )
    supplied = problem["decisions"]
    _require(
        type(supplied) is list and len(supplied) == 16 and len(supplied) <= MAX_DECISIONS,
        "exactly sixteen decisions within the live cap are required",
    )
    rows = []
    for index, row in enumerate(supplied):
        _fields(
            row,
            ("assumed_index", "bound_index", "quadratic_coefficient", "half_linear_coefficient"),
        )
        _integer(row["assumed_index"], index // 4, index // 4)
        _integer(row["bound_index"], index % 4, index % 4)
        A = _fraction(row["quadratic_coefficient"], 0, 2)
        B = _fraction(row["half_linear_coefficient"], -2, 2)
        rows.append((A, B))
    # Only comparisons are used to reserve conditional work; no division or
    # optimizer/value/coefficient arithmetic is performed during planning.
    interior = sum(1 for A, B in rows if A > 0 and 0 < B < A)
    points = sum(1 for A, B in rows if A != 0 or B != 0)
    critical = 2 * len(rows) + interior
    planned = {
        "decisions": len(rows),
        "critical_candidates": critical,
        "value_evaluations": critical + 3 * len(rows),
        "point_optimizers": points,
        "interval_optimizers": len(rows) - points,
        "interior_point_optimizers": interior,
        "optimizer_classifications": len(rows),
        "coefficient_visits": len(rows),
        "gradient_terms": points,
        "stationary_divisions": interior,
        "critical_value_terms": critical,
        "menu_value_terms": 3 * len(rows),
        "critical_selection_visits": critical,
        "menu_selection_visits": 3 * len(rows),
        "gap_terms": 4 * len(rows),
        "total_work_terms": 12 * len(rows) + points + interior + 2 * critical,
    }
    _require(critical <= MAX_CRITICAL_POINTS, "critical candidate cap exceeded")
    _require(planned["value_evaluations"] <= MAX_VALUE_EVALUATIONS, "value evaluation cap exceeded")
    _require(planned["total_work_terms"] <= MAX_TOTAL_WORK, "optimizer work cap exceeded")
    return rows, planned


def analyze(problem):
    """Return complete optimizer sets and exact convex/KKT certificates."""
    rows, planned = _prepare(problem)
    input_sha256 = hashlib.sha256(canonical(problem)).hexdigest()
    decisions = []
    optimizer_classifications = coefficient_visits = gradient_terms = stationary_divisions = 0
    critical_value_terms = menu_value_terms = critical_selection_visits = menu_selection_visits = 0
    gap_terms = lower_endpoints = upper_endpoints = point_optimizers = interval_optimizers = 0
    interior_optimizers = menu_occurrences = 0
    for index, (A, B) in enumerate(rows):
        optimizer_classifications += 1
        anchor = None
        isolated = None
        if A == 0:
            if B == 0:
                interval_optimizers += 1
            elif B > 0:
                anchor = Fraction(1)
                upper_endpoints += 1
            else:
                anchor = Fraction(0)
                lower_endpoints += 1
        elif B <= 0:
            anchor = Fraction(0)
            lower_endpoints += 1
        elif B >= A:
            anchor = Fraction(1)
            upper_endpoints += 1
        else:
            anchor = _stationary(A, B)
            stationary_divisions += 1
            isolated = anchor
            interior_optimizers += 1
        if anchor is not None:
            point_optimizers += 1

        linear, curvature = _coefficients(A, B)
        coefficient_visits += 1
        weights = [Fraction(0)]
        if isolated is not None:
            weights.append(isolated)
        weights.append(Fraction(1))
        critical, critical_values = [], []
        for weight in weights:
            value = _evaluate(A, B, weight)
            critical_value_terms += 1
            critical_values.append(value)
            critical.append({"retained_weight": _pair(weight, 0, 1), "value": _pair(value, -4, 6)})
        minimum, minimizing_critical = None, []
        for weight, value in zip(weights, critical_values):
            critical_selection_visits += 1
            if minimum is None or value < minimum:
                minimum, minimizing_critical = value, [weight]
            elif value == minimum:
                minimizing_critical.append(weight)
        _retained(minimum, -4, 0)

        if anchor is None:
            optimizer = {"kind": "interval", "lower": [0, 1], "upper": [1, 1]}
            proof = {
                "kind": "zero_polynomial",
                "anchor": None,
                "gradient": None,
                "second_derivative": _pair(curvature, 0, 4),
            }
            optimizer_complete = (
                A == B == linear == curvature == minimum == 0
                and minimizing_critical == [Fraction(0), Fraction(1)]
            )
            kkt_valid = A == 0 and B == 0 and linear == 0 and curvature == 0
        else:
            gradient = _gradient(A, B, anchor)
            gradient_terms += 1
            optimizer = {"kind": "point", "weight": _pair(anchor, 0, 1)}
            proof = {
                "kind": "point_kkt",
                "anchor": _pair(anchor, 0, 1),
                "gradient": _pair(gradient, -4, 8),
                "second_derivative": _pair(curvature, 0, 4),
            }
            optimizer_complete = (
                minimizing_critical == [anchor]
                and (A > 0 or (A == 0 and B != 0))
                and minimum == A * anchor * anchor + linear * anchor
            )
            sign = gradient >= 0 if anchor == 0 else gradient <= 0 if anchor == 1 else gradient == 0
            # Polynomial-coefficient equality verifies the global identity,
            # not merely agreement at sampled weights.
            kkt_valid = (
                curvature == 2 * A
                and curvature >= 0
                and 0 <= anchor <= 1
                and sign
                and gradient - 2 * A * anchor == linear
                and A * anchor * anchor - gradient * anchor == -minimum
            )

        menu, menu_values = [], []
        for weight in RETAINED_WEIGHTS:
            value = _evaluate(A, B, weight)
            menu_value_terms += 1
            excess = _gap(value, minimum)
            gap_terms += 1
            menu_values.append(value)
            menu.append(
                {
                    "retained_weight": _pair(weight, 0, 1),
                    "value": _pair(value, -4, 6),
                    "excess_over_minimum": _pair(excess, 0, 6),
                }
            )
        menu_minimum, menu_indices = None, []
        for rule, value in enumerate(menu_values):
            menu_selection_visits += 1
            if menu_minimum is None or value < menu_minimum:
                menu_minimum, menu_indices = value, [rule]
            elif value == menu_minimum:
                menu_indices.append(rule)
        _retained(menu_minimum, -4, 0)
        menu_gap = _gap(menu_minimum, minimum)
        gap_terms += 1
        _retained(menu_gap, 0, Fraction(1, 8))
        menu_occurrences += len(menu_indices)

        expected_interior = A > 0 and 0 < B < A
        critical_complete = (
            weights[0] == 0
            and weights[-1] == 1
            and all(left < right for left, right in pairwise(weights))
            and (
                len(weights) == 3
                and isolated is not None
                and 0 < isolated < 1
                and A * isolated == B
                if expected_interior
                else len(weights) == 2 and isolated is None
            )
        )
        checks = {
            "convexity": A >= 0 and curvature == 2 * A and curvature >= 0,
            "critical_candidates_complete": critical_complete,
            "optimizer_set_complete": optimizer_complete,
            "global_kkt_certificate": kkt_valid,
            "finite_menu_complete": len(menu) == 3
            and [entry["retained_weight"] for entry in menu]
            == [_pair(weight, 0, 1) for weight in RETAINED_WEIGHTS]
            and all(
                Fraction(*entry["excess_over_minimum"]) + minimum == value
                for entry, value in zip(menu, menu_values)
            ),
            "finite_menu_argmin_complete": menu_indices
            == [rule for rule, value in enumerate(menu_values) if value == menu_minimum]
            and all(value >= menu_minimum for value in menu_values),
            "finite_menu_gap_nonnegative": menu_gap >= 0 and menu_gap + minimum == menu_minimum,
            "menu_grid_error_bound": menu_gap <= Fraction(1, 8) and 16 * menu_gap <= A,
            "coarse_option_available": menu[0]["retained_weight"] == [0, 1]
            and menu_values[0] == 0
            and minimum <= menu_minimum <= 0,
        }
        _require(
            all(value is True for value in checks.values()), "quadratic certificate identity failed"
        )
        decisions.append(
            {
                "assumed_index": index // 4,
                "bound_index": index % 4,
                "quadratic_coefficient": _pair(A, 0, 2),
                "half_linear_coefficient": _pair(B, -2, 2),
                "linear_coefficient": _pair(linear, -4, 4),
                "critical_candidates": critical,
                "optimizer": optimizer,
                "minimum": _pair(minimum, -4, 0),
                "finite_menu": menu,
                "finite_menu_minimum": _pair(menu_minimum, -4, 0),
                "finite_menu_minimizer_indices": menu_indices,
                "finite_menu_minimizer_weights": [
                    _pair(RETAINED_WEIGHTS[rule], 0, 1) for rule in menu_indices
                ],
                "finite_menu_gap": _pair(menu_gap, 0, Fraction(1, 8)),
                "proof": proof,
                "checks": checks,
            }
        )

    counts = {
        "decisions": len(decisions),
        "critical_candidates": sum(len(row["critical_candidates"]) for row in decisions),
        "value_evaluations": critical_value_terms + menu_value_terms,
        "point_optimizers": point_optimizers,
        "interval_optimizers": interval_optimizers,
        "interior_point_optimizers": interior_optimizers,
        "lower_endpoint_optimizers": lower_endpoints,
        "upper_endpoint_optimizers": upper_endpoints,
        "finite_menu_minimizer_occurrences": menu_occurrences,
        "optimizer_classifications": optimizer_classifications,
        "coefficient_visits": coefficient_visits,
        "gradient_terms": gradient_terms,
        "stationary_divisions": stationary_divisions,
        "critical_value_terms": critical_value_terms,
        "menu_value_terms": menu_value_terms,
        "critical_selection_visits": critical_selection_visits,
        "menu_selection_visits": menu_selection_visits,
        "gap_terms": gap_terms,
        "total_work_terms": optimizer_classifications
        + coefficient_visits
        + gradient_terms
        + stationary_divisions
        + critical_value_terms
        + menu_value_terms
        + critical_selection_visits
        + menu_selection_visits
        + gap_terms,
    }
    computed_names = (
        "lower_endpoint_optimizers",
        "upper_endpoint_optimizers",
        "finite_menu_minimizer_occurrences",
    )
    _require(
        {name: value for name, value in counts.items() if name not in computed_names} == planned,
        "executed optimizer work differs from its preflight plan",
    )
    _require(
        lower_endpoints + upper_endpoints + interior_optimizers == point_optimizers
        and menu_occurrences == sum(len(row["finite_menu_minimizer_indices"]) for row in decisions),
        "optimizer/menu inventory differs",
    )
    result = {
        "input_sha256": input_sha256,
        "levels": [_pair(level, 0, 1) for level in LEVELS],
        "retained_weights": [_pair(weight, 0, 1) for weight in RETAINED_WEIGHTS],
        "decisions": decisions,
        "counts": counts,
    }
    return json.loads(canonical(result))
