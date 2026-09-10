"""Exact BV monomial integration and affine mass-inequality inversion.

Import defines functions only. The bounded analyze interface is pure: it
does not read files, import historical engines, or construct record laws
over words/counts. All execution belongs after the prospective freeze.
"""

from fractions import Fraction as F
from math import gcd, lcm


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, baseline=False, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (int, str) or baseline and kind in (bool, F):
        return
    _require(kind in (dict, list), "plain native input containers and scalars")
    identity = id(value)
    _require(identity not in active, "cyclic native input")
    if kind is dict:
        _require(
            all(type(key) is str and not key.startswith("$") for key in value),
            "plain nonreserved input keys",
        )
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native(child, baseline, active)
    finally:
        active.remove(identity)


def _fields(value, names, label):
    _require(type(value) is dict and set(value) == set(names.split()), label)


def _rationals(value, count, label):
    _require(
        type(value) is list and len(value) == count and all(type(x) is F for x in value),
        label,
    )


def _baseline_shape(baseline):
    _fields(baseline, "schema classes plans", "complete baseline fields")
    _require(baseline["schema"] == "qr05bv-bt-baseline-v1", "baseline schema")
    _require(
        type(baseline["classes"]) is list and len(baseline["classes"]) == 4,
        "four complete baseline classes",
    )
    _require(
        type(baseline["plans"]) is list and len(baseline["plans"]) == 4,
        "four complete baseline plans",
    )
    for name, row in zip(("uniform", "half", "one", "two"), baseline["classes"], strict=True):
        _fields(
            row,
            "bound upper segments kind deltas parameters points residual distance closed_form lower",
            "complete baseline class fields",
        )
        _require(row["bound"] == name, "baseline bound order")
        _require(
            row["kind"] == ("ordered" if name in ("uniform", "half") else "collision"),
            "baseline class kind metadata",
        )
        _require(
            all(type(row[key]) is F for key in ("upper", "distance", "closed_form")),
            "baseline class rational scalars",
        )
        for key in ("deltas", "parameters", "residual"):
            _rationals(row[key], 2, "baseline class rational pair")
        for key in ("segments", "points"):
            _require(type(row[key]) is list and len(row[key]) == 2, "baseline paired classes")
        for segment in row["segments"]:
            _fields(segment, "start end vector", "complete baseline segment")
            for key in ("start", "end", "vector"):
                _rationals(segment[key], 2, "baseline segment coordinates")
        for point in row["points"]:
            _rationals(point, 2, "baseline class point")
        lower = row["lower"]
        _fields(lower, "normal coefficients corner_values norm value", "complete baseline lower")
        for key, count in (("normal", 2), ("coefficients", 3), ("corner_values", 4)):
            _rationals(lower[key], count, "baseline lower rational vector")
        _require(
            type(lower["norm"]) is F and type(lower["value"]) is F,
            "baseline lower rational scalars",
        )
    for name, row in zip(("uniform", "half", "one", "two"), baseline["plans"], strict=True):
        _fields(
            row,
            "id kind source distance in_premise slack score grid_positive threshold_holds "
            "sufficient eligible status guarantees",
            "complete baseline plan fields",
        )
        _require(
            row["id"] == "class/" + name and row["kind"] == "class" and row["source"] == name,
            "baseline plan metadata",
        )
        _require(
            all(type(row[key]) is F for key in ("distance", "slack", "score")),
            "baseline plan rational scalars",
        )
        _require(
            all(
                type(row[key]) is bool
                for key in (
                    "in_premise",
                    "grid_positive",
                    "threshold_holds",
                    "sufficient",
                    "eligible",
                )
            )
            and row["in_premise"] is True,
            "baseline plan exact flags and premise",
        )
        _require(row["status"] in ("certified", "not_certified"), "baseline plan status")
        _require(
            type(row["guarantees"]) is list and len(row["guarantees"]) in (0, 1),
            "baseline guarantee list",
        )
        for guarantee in row["guarantees"]:
            _fields(
                guarantee,
                "correct_singleton_at_least conditional_wrong_singleton_at_most",
                "complete baseline guarantee",
            )
            _require(all(type(x) is F for x in guarantee.values()), "rational guarantees")


def _validate(protocol, baseline):
    # Check both entire native trees before constructing a fresh Fraction
    # or performing any of the model's mathematics.
    _native(protocol)
    _native(baseline, True)
    expected = {
        "schema": "qr05bv-protocol-v1",
        "quota": 65536,
        "grid_denominator": 256,
        "alpha": [1, 20],
        "tail_allocations": [[1, 80], [1, 80], [1, 80], [1, 80]],
        "regions": {
            "Q": [[0, 1], [1, 1], [0, 1], [1, 1]],
            "I1": [[0, 1], [1, 2], [0, 1], [1, 2]],
            "I2": [[0, 1], [3, 4], [0, 1], [1, 2]],
        },
        "geometries": [
            {"id": "flat", "eta": 0, "scale": 1},
            {"id": "conformal", "eta": 1, "scale": 1},
            {"id": "flat_x4", "eta": 0, "scale": 4},
            {"id": "conformal_x4", "eta": 1, "scale": 4},
        ],
        "density_bounds": [
            {"id": "uniform", "upper": [0, 1]},
            {"id": "half", "upper": [1, 2]},
            {"id": "one", "upper": [1, 1]},
            {"id": "two", "upper": [2, 1]},
        ],
        "cases": [
            {"id": "uniform/zero", "bound": "uniform", "fraction": [0, 1]},
            {"id": "uniform/quarter", "bound": "uniform", "fraction": [1, 4]},
            {"id": "uniform/contact", "bound": "uniform", "fraction": [1, 2]},
            {"id": "half/zero", "bound": "half", "fraction": [0, 1]},
            {"id": "half/quarter", "bound": "half", "fraction": [1, 4]},
            {"id": "half/contact", "bound": "half", "fraction": [1, 2]},
            {"id": "one/zero", "bound": "one", "fraction": [0, 1]},
            {"id": "two/zero", "bound": "two", "fraction": [0, 1]},
        ],
        "boxes": [
            {"id": "uniform/flat", "bound": "uniform", "point": "flat", "fraction": [1, 4]},
            {
                "id": "uniform/conformal",
                "bound": "uniform",
                "point": "conformal",
                "fraction": [1, 4],
            },
            {
                "id": "uniform/midpoint_quarter",
                "bound": "uniform",
                "point": "midpoint",
                "fraction": [1, 4],
            },
            {
                "id": "uniform/midpoint_contact",
                "bound": "uniform",
                "point": "midpoint",
                "fraction": [1, 2],
            },
            {"id": "half/flat", "bound": "half", "point": "flat", "fraction": [1, 4]},
            {
                "id": "half/conformal",
                "bound": "half",
                "point": "conformal",
                "fraction": [1, 4],
            },
            {
                "id": "half/midpoint_quarter",
                "bound": "half",
                "point": "midpoint",
                "fraction": [1, 4],
            },
            {
                "id": "half/midpoint_contact",
                "bound": "half",
                "point": "midpoint",
                "fraction": [1, 2],
            },
            {"id": "one/collision", "bound": "one", "point": "midpoint", "fraction": [0, 1]},
            {"id": "two/collision", "bound": "two", "point": "midpoint", "fraction": [0, 1]},
        ],
        "negative": {"eta": 0, "delta": [0, 1], "lambda": [1, 16]},
        "baseline": {
            "schema": "qr05bv-bt-baseline-v1",
            "sha256": "6beb088e27e0ec0c843b9be1c0794add02d8418a2fcbce9d4ade95ca685a9adb",
        },
        "coverage": {
            "geometries": 4,
            "classes": 4,
            "cases": 8,
            "plans": 8,
            "boxes": 10,
            "hypotheses": 40,
            "unexpanded_hypotheses": 40,
            "negative_controls": 1,
            "scale_pairs": 2,
            "baseline_classes": 4,
            "baseline_plans": 4,
        },
        "limits": {
            "source_bytes": 262144,
            "artifact_bytes": 16777216,
            "analysis_seconds": 30,
            "suite_seconds": 120,
            "alternate_reference_runs": 1,
        },
    }
    _require(type(protocol) is dict and protocol == expected, "complete fixed BV protocol")
    _baseline_shape(baseline)


def _fraction(pair):
    _require(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "plain rational pair",
    )
    numerator, denominator = pair
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "reduced rational pair")
    return F(numerator, denominator)


def _integrate(poly, rectangle):
    u0, u1, v0, v1 = rectangle
    _require(u0 < u1 and v0 < v1, "positive integration rectangle")
    return sum(
        (
            value
            * (u1 ** (i + 1) - u0 ** (i + 1))
            * (v1 ** (j + 1) - v0 ** (j + 1))
            / ((i + 1) * (j + 1))
            for (i, j), value in poly.items()
        ),
        F(0),
    )


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def _subtract(left, right):
    return [a - b for a, b in zip(left, right, strict=True)]


def _norm(vector):
    return max(abs(value) for value in vector)


def _affine(coefficients, delta):
    return coefficients[0] + coefficients[1] * delta


def _nested(point):
    return F(0) <= point[0] <= point[1] <= F(1)


def _law(point):
    _require(_nested(point), "actual population belongs to the closed nested triangle")
    law = [1 - point[1], point[1] - point[0], F(0), point[0]]
    _require(all(value >= 0 for value in law) and sum(law, F(0)) == 1, "nested symbol law")
    return law


def _primitive_line(coefficients):
    (a_q, b_q), (a_1, b_1), (a_2, b_2) = coefficients
    raw = [a_2 * b_q - a_q * b_2, a_q * b_1 - a_1 * b_q, a_2 * b_1 - a_1 * b_2]
    common = lcm(*(value.denominator for value in raw))
    integers = [(common * value).numerator for value in raw]
    divisor = gcd(*(abs(value) for value in integers))
    _require(divisor > 0 and integers[2] != 0, "nondegenerate normalized family line")
    orientation = 1 if integers[2] > 0 else -1
    result = [F(orientation * value // divisor) for value in integers]
    _require(
        all(
            result[0] * coefficients[1][j] + result[1] * coefficients[2][j]
            == result[2] * coefficients[0][j]
            for j in (0, 1)
        ),
        "complete affine mass supporting-line identity",
    )
    return result


def _geometry(raw, regions):
    proper = {(0, 0): F(raw["scale"], 2), (1, 1): F(raw["scale"] * raw["eta"], 2)}
    slope = {(i + 1, j + 1): value for (i, j), value in proper.items()}
    volumes = [_integrate(proper, rectangle) for rectangle in regions]
    coefficients = [
        [_integrate(poly, rectangle) for poly in (proper, slope)] for rectangle in regions
    ]
    a_q, b_q = coefficients[0]
    positive = all(a_q + b_q * endpoint > 0 for endpoint in (F(0), F(2)))
    derivatives = [b * a_q - a * b_q for a, b in coefficients[1:]]
    decreasing = all(value < 0 for value in derivatives)
    _require(positive and decreasing, "continuous positive normalization and decreasing ratios")
    return {
        "id": raw["id"],
        "eta": raw["eta"],
        "scale": raw["scale"],
        "volumes": volumes,
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "target": volumes[1] / volumes[0],
        "line": _primitive_line(coefficients),
        "positive_normalizer": positive,
        "decreasing": decreasing,
    }


def _forward(geometry, delta):
    masses = [_affine(pair, delta) for pair in geometry["mass_coefficients"]]
    _require(0 < masses[1] < masses[2] < masses[0], "strict ideal nested categories")
    return [masses[1] / masses[0], masses[2] / masses[0]]


def _segment(geometry, upper):
    start, end = _forward(geometry, F(0)), _forward(geometry, upper)
    vector = _subtract(end, start)
    if upper == 0:
        _require(all(value == 0 for value in vector), "point segment")
    else:
        _require(all(value < 0 for value in vector), "strict segment directions")
        a_q, b_q = geometry["mass_coefficients"][0]
        for i, (a, b) in enumerate(geometry["mass_coefficients"][1:]):
            _require(
                a == start[i] * a_q
                and b == start[i] * b_q + (a_q + b_q * upper) * vector[i] / upper,
                "whole continuous family has the retained segment parametrization",
            )
    return {"start": start, "end": end, "vector": vector}


def _parameter(geometry, upper, delta):
    _require(0 <= delta <= upper <= 2, "contact density in bounded family")
    if upper == 0:
        return F(0)
    a_q, b_q = geometry["mass_coefficients"][0]
    result = delta * (a_q + b_q * upper) / (upper * (a_q + b_q * delta))
    _require(0 <= result <= 1, "contact segment parameter")
    return result


def _class(bound, geometries):
    upper = bound["upper"]
    segments = [_segment(geometry, upper) for geometry in geometries]
    ordered = upper < 1
    deltas = [upper if ordered else F(1), F(0)]
    parameters = [
        _parameter(geometry, upper, delta)
        for geometry, delta in zip(geometries, deltas, strict=True)
    ]
    points = [_forward(geometry, delta) for geometry, delta in zip(geometries, deltas, strict=True)]
    for segment, point, parameter in zip(segments, points, parameters, strict=True):
        _require(
            point
            == [
                a + parameter * v for a, v in zip(segment["start"], segment["vector"], strict=True)
            ],
            "ideal class contact lies in its complete segment",
        )
    residual = _subtract(points[0], points[1])
    distance = _norm(residual)
    normal = [F(0), F(1)] if ordered else [F(0), F(0)]
    constant = _dot(normal, _subtract(segments[0]["start"], segments[1]["start"]))
    first = _dot(normal, segments[0]["vector"])
    second = -_dot(normal, segments[1]["vector"])
    corners = [constant, constant + second, constant + first, constant + first + second]
    norm = sum((abs(value) for value in normal), F(0))
    value = min(corners)
    closed = 3 * (1 - upper) / (16 * (4 + upper)) if ordered else F(0)
    _require(
        norm <= 1
        and value == distance == closed
        and constant + first * parameters[0] + second * parameters[1] == distance
        and _dot(normal, residual) == distance,
        "affine corner lower bound attains the complete ideal class distance",
    )
    return {
        "bound": bound["id"],
        "upper": upper,
        "segments": segments,
        "kind": "ordered" if ordered else "collision",
        "deltas": deltas,
        "parameters": parameters,
        "points": points,
        "residual": residual,
        "distance": distance,
        "closed_form": closed,
        "lower": {
            "normal": normal,
            "coefficients": [constant, first, second],
            "corner_values": corners,
            "norm": norm,
            "value": value,
        },
    }


def _case(raw, ideal):
    fraction = _fraction(raw["fraction"])
    distance = ideal["distance"]
    error = fraction * distance
    interpolation = min(error / distance, F(1, 2)) if distance > 0 else F(0)
    p0, p1 = ideal["points"]
    actual = [
        [(1 - interpolation) * x + interpolation * y for x, y in zip(p0, p1, strict=True)],
        [interpolation * x + (1 - interpolation) * y for x, y in zip(p0, p1, strict=True)],
    ]
    offsets = [_subtract(r, q) for r, q in zip(actual, ideal["points"], strict=True)]
    norms = [_norm(offset) for offset in offsets]
    remainder = distance - 2 * error
    attained = _norm(_subtract(actual[0], actual[1]))
    lower = ideal["lower"]
    penalty = 2 * error * lower["norm"]
    signed_value = min(lower["corner_values"]) - penalty
    value = max(F(0), signed_value)
    nested = [_nested(point) for point in actual]
    _require(
        all(nested)
        and all(norm <= error for norm in norms)
        and attained == max(F(0), remainder) == value,
        "actual interpolation attains global lower bound inside the nested triangle",
    )
    return {
        "id": raw["id"],
        "bound": raw["bound"],
        "upper": ideal["upper"],
        "fraction": fraction,
        "error": error,
        "ideal_distance": distance,
        "signed_remaining": remainder,
        "distance": attained,
        "ideal_deltas": list(ideal["deltas"]),
        "ideal_contacts": [list(point) for point in ideal["points"]],
        "actual_contacts": actual,
        "displacements": offsets,
        "distortion_norms": norms,
        "laws": [_law(point) for point in actual],
        "nested": nested,
        "interpolation": interpolation,
        "kind": "separated"
        if attained > 0
        else "new_collision"
        if distance > 0
        else "inherited_collision",
        "lower": {
            "normal": list(lower["normal"]),
            "norm": lower["norm"],
            "ideal_corner_values": list(lower["corner_values"]),
            "penalty": penalty,
            "signed_value": signed_value,
            "value": value,
        },
    }


def _guarantees(sufficient, alpha):
    return (
        [{"correct_singleton_at_least": 1 - alpha, "conditional_wrong_singleton_at_most": alpha}]
        if sufficient
        else []
    )


def _plan(case, planning):
    step = F(1, planning["grid_denominator"])
    slack = case["signed_remaining"] - 2 * step
    score = planning["quota"] * slack**2
    positive, threshold = slack > 0, score >= planning["threshold"]
    sufficient = positive and threshold
    return {
        "id": case["id"],
        "ideal_distance": case["ideal_distance"],
        "error": case["error"],
        "signed_remaining": case["signed_remaining"],
        "distance": case["distance"],
        "step": step,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "status": "certified" if sufficient else "not_certified",
        "guarantees": _guarantees(sufficient, planning["alpha"]),
    }


def _expanded(box, error):
    return [[max(F(0), lower - error), min(F(1), upper + error)] for lower, upper in box]


def _inverse(geometry, box, error, upper):
    _require(type(error) is F and error >= 0, "nonnegative rational error")
    _require(type(upper) is F and 0 <= upper <= 2, "rational density bound")
    _require(type(box) is list and len(box) == 2, "two original coordinate intervals")
    for interval in box:
        _rationals(interval, 2, "rational original interval")
        _require(0 <= interval[0] <= interval[1] <= 1, "ordered probability interval")
    if box[0][0] > box[1][1]:
        return {"delta_set": [], "constraints": [], "endpoints": []}
    expanded = _expanded(box, error)
    a_q, b_q = geometry["mass_coefficients"][0]
    constraints = []
    for (a, b), (lower, high) in zip(geometry["mass_coefficients"][1:], expanded, strict=True):
        constraints.extend([[a - lower * a_q, b - lower * b_q], [high * a_q - a, high * b_q - b]])
    lo, hi = F(0), upper
    feasible = True
    for constant, slope in constraints:
        if slope > 0:
            lo = max(lo, -constant / slope)
        elif slope < 0:
            hi = min(hi, -constant / slope)
        elif constant < 0:
            feasible = False
    if not feasible or lo > hi:
        return {"delta_set": [], "constraints": constraints, "endpoints": []}
    endpoints = []
    for delta in (lo, hi):
        q = _forward(geometry, delta)
        values = [_affine(pair, delta) for pair in constraints]
        low = [max(interval[0], point - error) for interval, point in zip(box, q, strict=True)]
        high = [min(interval[1], point + error) for interval, point in zip(box, q, strict=True)]
        r = [low[0], max(low[1], low[0])]
        offset = _subtract(r, q)
        norm = _norm(offset)
        nested = _nested(r)
        inside = all(
            interval[0] <= point <= interval[1] for interval, point in zip(box, r, strict=True)
        )
        within = norm <= error
        _require(
            0 <= delta <= upper
            and all(value >= 0 for value in values)
            and all(a <= b for a, b in zip(low, high, strict=True))
            and all(a <= point <= b for a, point, b in zip(low, r, high, strict=True))
            and nested
            and inside
            and within,
            "shared-density endpoint and explicit original-box nested witness",
        )
        endpoints.append(
            {
                "delta": delta,
                "q": q,
                "constraint_values": values,
                "A": low,
                "B": high,
                "r": r,
                "law": _law(r),
                "offset": offset,
                "norm": norm,
                "nested": nested,
                "inside_box": inside,
                "within_error": within,
            }
        )
    return {"delta_set": [lo, hi], "constraints": constraints, "endpoints": endpoints}


def _hypothesis(geometry, box, error, upper):
    inverse = _inverse(geometry, box, error, upper)
    return {
        "id": geometry["id"],
        "eta": geometry["eta"],
        "scale": geometry["scale"],
        "target": geometry["target"],
        "delta_set": inverse["delta_set"],
        "constraints": inverse["constraints"],
        "endpoints": inverse["endpoints"],
    }


def _target_result(hypotheses):
    targets = sorted({row["target"] for row in hypotheses if row["delta_set"]})
    status = "empty" if not targets else "singleton" if len(targets) == 1 else "ambiguous"
    return {"hypotheses": hypotheses, "targets": targets, "status": status}


def _box(raw, ideal, geometries):
    fraction = _fraction(raw["fraction"])
    error = fraction * ideal["distance"]
    p0, p1 = ideal["points"]
    point = (
        list(p0)
        if raw["point"] == "flat"
        else list(p1)
        if raw["point"] == "conformal"
        else [(x + y) / 2 for x, y in zip(p0, p1, strict=True)]
    )
    intervals = [[value, value] for value in point]
    upper = ideal["upper"]
    expanded = _target_result([_hypothesis(g, intervals, error, upper) for g in geometries])
    unexpanded = _target_result([_hypothesis(g, intervals, F(0), upper) for g in geometries])
    return {
        "id": raw["id"],
        "bound": raw["bound"],
        "upper": upper,
        "fraction": fraction,
        "error": error,
        "point": point,
        "intervals": intervals,
        "nested_box": intervals[0][0] <= intervals[1][1],
        "expanded": _expanded(intervals, error),
        "hypotheses": expanded["hypotheses"],
        "targets": expanded["targets"],
        "status": expanded["status"],
        "unexpanded": unexpanded,
    }


def _negative(raw, geometry, alpha):
    delta, lam = _fraction(raw["delta"]), _fraction(raw["lambda"])
    q = _forward(geometry, delta)
    ideal = _law(q)
    actual = [ideal[0] - lam, ideal[1] + lam, ideal[2] + lam, ideal[3] - lam]
    marginals = [actual[2] + actual[3], actual[1] + actual[3]]
    error = F(0)
    equal = marginals == q
    within = _norm(_subtract(marginals, q)) <= error
    nonnegative = all(value >= 0 for value in actual)
    normalized = sum(actual, F(0)) == 1
    nested_support = actual[2] == 0
    forbidden = actual[2]
    refusal = forbidden
    _require(
        equal
        and within
        and _nested(marginals)
        and nonnegative
        and normalized
        and not nested_support
        and forbidden == lam
        and refusal > alpha,
        "unchanged marginals do not establish nested symbol support",
    )
    return {
        "eta": raw["eta"],
        "delta": delta,
        "error": error,
        "lambda": lam,
        "ideal_q": q,
        "ideal_law": ideal,
        "actual_law": actual,
        "actual_marginals": marginals,
        "marginals_equal": equal,
        "within_error": within,
        "population_in_S": _nested(marginals),
        "nonnegative": nonnegative,
        "normalized": normalized,
        "nested_support": nested_support,
        "forbidden_mass": forbidden,
        "refusal_lower": refusal,
        "alpha": alpha,
        "refusal_exceeds_alpha": refusal > alpha,
        "status": "outside_nested_law",
    }


def _normalized_inverse(inverse):
    return {
        "delta_set": list(inverse["delta_set"]),
        "endpoints": [
            {key: value for key, value in endpoint.items() if key != "constraint_values"}
            for endpoint in inverse["endpoints"]
        ],
    }


def _scale_pairs(geometries, bounds, raw_cases, classes, cases, boxes):
    scaled = [geometries[2], geometries[3]]
    scaled_classes = [_class(bound, scaled) for bound in bounds]
    by_bound = {row["bound"]: row for row in scaled_classes}
    scaled_cases = [_case(raw, by_bound[raw["bound"]]) for raw in raw_cases]
    classes_equal = scaled_classes == classes
    cases_equal = scaled_cases == cases
    result = []
    for eta in (0, 1):
        unit, other = geometries[eta], geometries[eta + 2]
        factor = F(other["scale"], unit["scale"])
        actual = (
            other["volumes"] == [factor * value for value in unit["volumes"]]
            and other["mass_coefficients"]
            == [[factor * value for value in row] for row in unit["mass_coefficients"]]
            and other["derivative_numerators"]
            == [factor**2 * value for value in unit["derivative_numerators"]]
        )
        targets_equal = unit["target"] == other["target"]
        inverses_equal = True
        constraints_scaled = True
        for box in boxes:
            for error, stored in (
                (box["error"], box["hypotheses"]),
                (F(0), box["unexpanded"]["hypotheses"]),
            ):
                left = _inverse(unit, box["intervals"], error, box["upper"])
                right = _inverse(other, box["intervals"], error, box["upper"])
                inverses_equal = (
                    inverses_equal
                    and _normalized_inverse(left) == _normalized_inverse(right)
                    and _normalized_inverse(left) == _normalized_inverse(stored[eta])
                    and _normalized_inverse(right) == _normalized_inverse(stored[eta + 2])
                )
                constraints_scaled = (
                    constraints_scaled
                    and right["constraints"]
                    == [[factor * value for value in pair] for pair in left["constraints"]]
                    and len(left["endpoints"]) == len(right["endpoints"])
                    and all(
                        endpoint_right["constraint_values"]
                        == [factor * value for value in endpoint_left["constraint_values"]]
                        for endpoint_left, endpoint_right in zip(
                            left["endpoints"], right["endpoints"], strict=True
                        )
                    )
                )
                targets_equal = targets_equal and stored[eta]["target"] == stored[eta + 2]["target"]
        _require(
            actual
            and classes_equal
            and cases_equal
            and inverses_equal
            and constraints_scaled
            and targets_equal,
            "same-input scale comparison preserves normalized classes and latent inverses",
        )
        result.append(
            {
                "worlds": [unit["id"], other["id"]],
                "volume_factor": factor,
                "actual_scaling": actual,
                "classes_equal": classes_equal,
                "cases_equal": cases_equal,
                "inverses_equal": inverses_equal,
                "constraints_scaled": constraints_scaled,
                "targets_equal": targets_equal,
            }
        )
    return result


def _legacy_plan(ideal, planning):
    distance = ideal["distance"]
    slack = distance - F(2, planning["grid_denominator"])
    score = planning["quota"] * slack**2
    positive, threshold = slack > 0, score >= planning["threshold"]
    sufficient = positive and threshold
    return {
        "id": "class/" + ideal["bound"],
        "kind": "class",
        "source": ideal["bound"],
        "distance": distance,
        "in_premise": True,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "eligible": sufficient,
        "status": "certified" if sufficient else "not_certified",
        "guarantees": _guarantees(sufficient, planning["alpha"]),
    }


def analyze(protocol, baseline):
    """Return the exact fixed report from fully validated fresh native inputs."""
    _validate(protocol, baseline)
    planning = {
        "quota": protocol["quota"],
        "grid_denominator": protocol["grid_denominator"],
        "alpha": _fraction(protocol["alpha"]),
        "tail_allocations": [_fraction(pair) for pair in protocol["tail_allocations"]],
        "threshold": F(10),
        "log_upper": F(5),
        "basis": "ln80_lt_5",
    }
    _require(
        sum(planning["tail_allocations"], F(0)) == planning["alpha"],
        "fixed four-tail allocation",
    )
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    geometries = [_geometry(raw, regions) for raw in protocol["geometries"]]
    bounds = [
        {"id": raw["id"], "upper": _fraction(raw["upper"])} for raw in protocol["density_bounds"]
    ]
    classes = [_class(bound, geometries[:2]) for bound in bounds]
    class_by_bound = {row["bound"]: row for row in classes}
    cases = [_case(raw, class_by_bound[raw["bound"]]) for raw in protocol["cases"]]
    plans = [_plan(case, planning) for case in cases]
    boxes = [_box(raw, class_by_bound[raw["bound"]], geometries) for raw in protocol["boxes"]]
    legacy_plans = [_legacy_plan(ideal, planning) for ideal in classes]
    classes_equal = classes == baseline["classes"]
    plans_equal = legacy_plans == baseline["plans"]
    _require(
        classes_equal and plans_equal, "complete newly derived zero-error BT baseline equality"
    )
    comparison = {
        "schema": "qr05bv-bt-comparison-v1",
        "zero_ids": [row["id"] for row in cases if row["fraction"] == 0],
        "classes_equal": classes_equal,
        "plans_equal": plans_equal,
        "plans": legacy_plans,
    }
    return {
        "schema": "qr05bv-report-v1",
        "planning": planning,
        "geometries": geometries,
        "classes": classes,
        "cases": cases,
        "plans": plans,
        "boxes": boxes,
        "negative": _negative(protocol["negative"], geometries[0], planning["alpha"]),
        "scale_pairs": _scale_pairs(geometries, bounds, protocol["cases"], classes, cases, boxes),
        "baseline": comparison,
    }
