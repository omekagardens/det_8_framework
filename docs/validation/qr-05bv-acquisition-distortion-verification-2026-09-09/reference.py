"""Independent BV reference: tensor quadrature and shared-segment clipping.

No file access, historical mathematics, confidence-tail evaluation or quota loops.
Only analyze(protocol, baseline) constructs the fixed report.
"""

from fractions import Fraction as F
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _scan(value, active=None, depth=0, remaining=None):
    """Check complete native trees before constructing any new rational."""
    if active is None:
        active = set()
    if remaining is None:
        remaining = [16384]
    remaining[0] -= 1
    _require(remaining[0] >= 0 and depth <= 32, "native tree budget")
    kind = type(value)
    if kind in (dict, list):
        identity = id(value)
        _require(identity not in active, "cyclic native input")
        active.add(identity)
        if kind is dict:
            _require(all(type(k) is str and not k.startswith("$") for k in value), "native keys")
            children = value.values()
        else:
            children = value
        for child in children:
            _scan(child, active, depth + 1, remaining)
        active.remove(identity)
    else:
        _require(kind in (str, int, bool, F), "native leaf type")


def _exact(actual, expected):
    _require(type(actual) is type(expected), "exact native type")
    if type(expected) is dict:
        _require(set(actual) == set(expected), "exact native keys")
        for key in expected:
            _exact(actual[key], expected[key])
    elif type(expected) is list:
        _require(len(actual) == len(expected), "exact native length")
        for left, right in zip(actual, expected, strict=True):
            _exact(left, right)
    else:
        _require(actual == expected, "exact native value")


def _keys(value, names):
    _require(type(value) is dict and set(value) == set(names.split()), "baseline object keys")


def _fraction_fields(value, names):
    for name in names.split():
        _require(type(value[name]) is F, "baseline mathematical Fraction")


def _vector(value, size):
    _require(type(value) is list and len(value) == size, "baseline vector length")
    _require(all(type(entry) is F for entry in value), "baseline vector Fractions")


def _baseline_shape(baseline):
    _keys(baseline, "schema classes plans")
    _exact(baseline["schema"], "qr05bv-bt-baseline-v1")
    bounds = ["uniform", "half", "one", "two"]
    for name in ("classes", "plans"):
        _require(type(baseline[name]) is list and len(baseline[name]) == 4, "baseline census")
    for index, row in enumerate(baseline["classes"]):
        _keys(
            row,
            "bound upper segments kind deltas parameters points residual distance closed_form lower",
        )
        _exact(row["bound"], bounds[index])
        _exact(row["kind"], "ordered" if index < 2 else "collision")
        _fraction_fields(row, "upper distance closed_form")
        for name in ("deltas", "parameters", "residual"):
            _vector(row[name], 2)
        for name in ("segments", "points"):
            _require(type(row[name]) is list and len(row[name]) == 2, "baseline pair")
        for point in row["points"]:
            _vector(point, 2)
        for segment in row["segments"]:
            _keys(segment, "start end vector")
            for name in ("start", "end", "vector"):
                _vector(segment[name], 2)
        lower = row["lower"]
        _keys(lower, "normal coefficients corner_values norm value")
        _vector(lower["normal"], 2)
        _vector(lower["coefficients"], 3)
        _vector(lower["corner_values"], 4)
        _fraction_fields(lower, "norm value")
    for bound, row in zip(bounds, baseline["plans"], strict=True):
        _keys(
            row,
            "id kind source distance in_premise slack score grid_positive threshold_holds sufficient eligible status guarantees",
        )
        _exact(row["id"], "class/" + bound)
        _exact(row["kind"], "class")
        _exact(row["source"], bound)
        _fraction_fields(row, "distance slack score")
        for name in ("in_premise", "grid_positive", "threshold_holds", "sufficient", "eligible"):
            _require(type(row[name]) is bool, "baseline flag bool")
        _exact(row["in_premise"], True)
        _require(
            type(row["status"]) is str and row["status"] in ("certified", "not_certified"),
            "baseline plan status",
        )
        guarantees = row["guarantees"]
        _require(
            type(guarantees) is list and len(guarantees) in (0, 1), "baseline guarantee length"
        )
        for guarantee in guarantees:
            _keys(guarantee, "correct_singleton_at_least conditional_wrong_singleton_at_most")
            _fraction_fields(
                guarantee, "correct_singleton_at_least conditional_wrong_singleton_at_most"
            )


def _validate_inputs(protocol, baseline):
    _scan(protocol)
    _scan(baseline)
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
            {"id": "half/conformal", "bound": "half", "point": "conformal", "fraction": [1, 4]},
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
    _exact(protocol, expected)
    _baseline_shape(baseline)


def _fraction(pair):
    return F(pair[0], pair[1])


def _minus(left, right):
    return [x - y for x, y in zip(left, right, strict=True)]


def _dot(left, right):
    return sum((x * y for x, y in zip(left, right, strict=True)), F(0))


def _norm(vector):
    return max(abs(coordinate) for coordinate in vector)


def _nested(point):
    return F(0) <= point[0] <= point[1] <= F(1)


def _law(point):
    return [1 - point[1], point[1] - point[0], F(0), point[0]]


def _axis(lower, upper):
    weight = (upper - lower) / 6
    return [(lower, weight), ((lower + upper) / 2, 4 * weight), (upper, weight)]


def _integrate(rectangle, eta, scale, delta):
    """Tensor Simpson is exact for this polynomial of degree two per axis."""
    left, right, bottom, top = rectangle
    total = F(0)
    for u, weight_u in _axis(left, right):
        for v, weight_v in _axis(bottom, top):
            total += weight_u * weight_v * F(scale, 2) * (1 + eta * u * v) * (1 + delta * u * v)
    return total


def _masses(geometry, delta):
    return [constant + slope * delta for constant, slope in geometry["mass_coefficients"]]


def _point(geometry, delta):
    masses = _masses(geometry, delta)
    _require(masses[0] > 0, "positive mass denominator")
    return [mass / masses[0] for mass in masses[1:]]


def _line(first, second):
    vector = _minus(second, first)
    normal = [vector[1], -vector[0]]
    coefficients = normal + [_dot(normal, first)]
    denominator = 1
    for value in coefficients:
        denominator = denominator * value.denominator // gcd(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator) for value in coefficients]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    _require(common > 0 and integers[2] != 0, "nondegenerate normalized line")
    sign = 1 if integers[2] > 0 else -1
    return [F(sign * value // common) for value in integers]


def _geometry(description, rectangles):
    eta, scale = description["eta"], description["scale"]
    volumes = [_integrate(rectangle, eta, scale, F(0)) for rectangle in rectangles]
    masses_one = [_integrate(rectangle, eta, scale, F(1)) for rectangle in rectangles]
    coefficients = [
        [volume, mass - volume] for volume, mass in zip(volumes, masses_one, strict=True)
    ]
    constant, slope = coefficients[0]
    derivatives = [bi * constant - ai * slope for ai, bi in coefficients[1:]]
    positive = min(constant, constant + 2 * slope) > 0
    decreasing = all(derivative < 0 for derivative in derivatives)
    first = [ai / constant for ai, _ in coefficients[1:]]
    second = [(ai + 2 * bi) / (constant + 2 * slope) for ai, bi in coefficients[1:]]
    _require(positive and decreasing, "continuous ideal-family certificate")
    return {
        "id": description["id"],
        "eta": eta,
        "scale": scale,
        "volumes": volumes,
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "target": volumes[1] / volumes[0],
        "line": _line(first, second),
        "positive_normalizer": positive,
        "decreasing": decreasing,
    }


def _segment(geometry, upper):
    start, end = _point(geometry, F(0)), _point(geometry, upper)
    return {"start": start, "end": end, "vector": _minus(end, start)}


def _class(bound, geometries):
    upper = _fraction(bound["upper"])
    flat, conformal = geometries
    segments = [_segment(geometry, upper) for geometry in geometries]
    deltas = [upper if upper < 1 else F(1), F(0)]
    points = [_point(geometry, delta) for geometry, delta in zip(geometries, deltas, strict=True)]
    parameters = []
    for point, segment in zip(points, segments, strict=True):
        parameter = (point[0] - segment["start"][0]) / segment["vector"][0] if upper else F(0)
        _require(0 <= parameter <= 1, "ideal contact segment parameter")
        _require(
            point
            == [
                a + parameter * v for a, v in zip(segment["start"], segment["vector"], strict=True)
            ],
            "shared ideal contact parameter",
        )
        parameters.append(parameter)
    residual = _minus(points[0], points[1])
    distance = _norm(residual)
    normal = [F(0), F(1) if upper < 1 else F(0)]
    constant = _dot(normal, _minus(segments[0]["start"], segments[1]["start"]))
    slope_flat = _dot(normal, segments[0]["vector"])
    slope_conformal = -_dot(normal, segments[1]["vector"])
    corners = [
        constant,
        constant + slope_conformal,
        constant + slope_flat,
        constant + slope_flat + slope_conformal,
    ]
    lower = {
        "normal": normal,
        "coefficients": [constant, slope_flat, slope_conformal],
        "corner_values": corners,
        "norm": sum(map(abs, normal), F(0)),
        "value": min(corners),
    }
    closed = 3 * (1 - upper) / (16 * (4 + upper)) if upper < 1 else F(0)
    _require(
        lower["norm"] <= 1 and min(corners) == distance == closed,
        "global ideal class lower certificate",
    )
    _require(
        constant + slope_flat * parameters[0] + slope_conformal * parameters[1] == distance,
        "ideal class attainment",
    )
    _require(all(_nested(point) for point in points), "nested ideal class contacts")
    _require(flat["target"] != conformal["target"], "distinct ideal targets")
    return {
        "bound": bound["id"],
        "upper": upper,
        "segments": segments,
        "kind": "ordered" if upper < 1 else "collision",
        "deltas": deltas,
        "parameters": parameters,
        "points": points,
        "residual": residual,
        "distance": distance,
        "closed_form": closed,
        "lower": lower,
    }


def _case(description, ideal):
    fraction = _fraction(description["fraction"])
    distance = ideal["distance"]
    error = fraction * distance
    interpolation = min(error / distance, F(1, 2)) if distance else F(0)
    first, second = ideal["points"]
    movement = [interpolation * value for value in _minus(second, first)]
    actual = [
        [value + shift for value, shift in zip(first, movement, strict=True)],
        [value - shift for value, shift in zip(second, movement, strict=True)],
    ]
    offsets = [_minus(point, origin) for point, origin in zip(actual, ideal["points"], strict=True)]
    norms = [_norm(offset) for offset in offsets]
    signed = distance - 2 * error
    attained = _norm(_minus(actual[0], actual[1]))
    normal = list(ideal["lower"]["normal"])
    normal_norm = sum(map(abs, normal), F(0))
    penalty = 2 * error * normal_norm
    signed_lower = min(ideal["lower"]["corner_values"]) - penalty
    lower = {
        "normal": normal,
        "norm": normal_norm,
        "ideal_corner_values": list(ideal["lower"]["corner_values"]),
        "penalty": penalty,
        "signed_value": signed_lower,
        "value": max(F(0), signed_lower),
    }
    nested = [_nested(point) for point in actual]
    laws = [_law(point) for point in actual]
    _require(attained == max(F(0), signed) == lower["value"], "actual class lower and attainment")
    _require(all(nested) and all(value <= error for value in norms), "actual class membership")
    _require(
        all(min(law) >= 0 and sum(law, F(0)) == 1 and law[2] == 0 for law in laws),
        "actual nested probability laws",
    )
    return {
        "id": description["id"],
        "bound": description["bound"],
        "upper": ideal["upper"],
        "fraction": fraction,
        "error": error,
        "ideal_distance": distance,
        "signed_remaining": signed,
        "distance": attained,
        "ideal_deltas": list(ideal["deltas"]),
        "ideal_contacts": [list(point) for point in ideal["points"]],
        "actual_contacts": actual,
        "displacements": offsets,
        "distortion_norms": norms,
        "laws": laws,
        "nested": nested,
        "interpolation": interpolation,
        "kind": "inherited_collision"
        if distance == 0
        else "separated"
        if attained > 0
        else "new_collision",
        "lower": lower,
    }


def _guarantees(sufficient, alpha):
    return (
        [{"correct_singleton_at_least": 1 - alpha, "conditional_wrong_singleton_at_most": alpha}]
        if sufficient
        else []
    )


def _plan(case, protocol):
    step = F(1, protocol["grid_denominator"])
    slack = case["signed_remaining"] - 2 * step
    score = protocol["quota"] * slack * slack
    positive, threshold = slack > 0, score >= 10
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
        "guarantees": _guarantees(sufficient, _fraction(protocol["alpha"])),
    }


def _expanded(box, error):
    return [[max(F(0), lower - error), min(F(1), upper + error)] for lower, upper in box]


def _constraints(geometry, expanded):
    aq, bq = geometry["mass_coefficients"][0]
    result = []
    for (ai, bi), (lower, upper) in zip(geometry["mass_coefficients"][1:], expanded, strict=True):
        result.extend([[ai - lower * aq, bi - lower * bq], [upper * aq - ai, upper * bq - bi]])
    return result


def _endpoint(geometry, box, error, delta, constraints):
    point = _point(geometry, delta)
    lower = [max(interval[0], q - error) for interval, q in zip(box, point, strict=True)]
    upper = [min(interval[1], q + error) for interval, q in zip(box, point, strict=True)]
    witness = [lower[0], max(lower[1], lower[0])]
    offset = _minus(witness, point)
    values = [constant + slope * delta for constant, slope in constraints]
    nested = _nested(witness)
    inside = all(
        interval[0] <= value <= interval[1] for interval, value in zip(box, witness, strict=True)
    )
    within = _norm(offset) <= error
    _require(
        all(a <= b for a, b in zip(lower, upper, strict=True)),
        "feasible coordinate witness intervals",
    )
    _require(
        all(a <= r <= b for a, r, b in zip(lower, witness, upper, strict=True)),
        "nested witness in coordinate intersections",
    )
    _require(
        min(values) >= 0 and nested and inside and within,
        "original-ratio and latent witness certificate",
    )
    return {
        "delta": delta,
        "q": point,
        "constraint_values": values,
        "A": lower,
        "B": upper,
        "r": witness,
        "law": _law(witness),
        "offset": offset,
        "norm": _norm(offset),
        "nested": nested,
        "inside_box": inside,
        "within_error": within,
    }


def _inverse(geometry, box, error, upper):
    """Intersect one common probability-segment parameter, then recover delta."""
    _require(type(box) is list and len(box) == 2, "inverse box shape")
    for interval in box:
        _require(type(interval) is list and len(interval) == 2, "inverse interval shape")
        _require(all(type(value) is F for value in interval), "inverse interval rational type")
        _require(0 <= interval[0] <= interval[1] <= 1, "inverse interval range")
    _require(type(error) is F and error >= 0, "inverse nonnegative rational error")
    _require(type(upper) is F and 0 <= upper <= 2, "inverse rational density bound")
    if box[0][0] > box[1][1]:
        return {"delta_set": [], "constraints": [], "endpoints": []}
    expanded = _expanded(box, error)
    constraints = _constraints(geometry, expanded)
    segment = _segment(geometry, upper)
    low_t, high_t = F(0), F(1)
    empty = False
    for start, velocity, interval in zip(
        segment["start"], segment["vector"], expanded, strict=True
    ):
        if velocity == 0:
            if not interval[0] <= start <= interval[1]:
                empty = True
        else:
            first, second = (interval[0] - start) / velocity, (interval[1] - start) / velocity
            low_t, high_t = max(low_t, min(first, second)), min(high_t, max(first, second))
    if empty or low_t > high_t:
        return {"delta_set": [], "constraints": constraints, "endpoints": []}
    aq, bq = geometry["mass_coefficients"][0]
    # The endpoint-normalizer mixture, obtained independently of mass clipping.
    delta_set = [
        parameter * upper * aq / (aq + bq * upper * (1 - parameter))
        for parameter in (low_t, high_t)
    ]
    _require(0 <= delta_set[0] <= delta_set[1] <= upper, "closed shared-density interval")
    endpoints = [_endpoint(geometry, box, error, delta, constraints) for delta in delta_set]
    return {"delta_set": delta_set, "constraints": constraints, "endpoints": endpoints}


def _hypotheses(geometries, intervals, error, upper):
    return [
        {
            "id": geometry["id"],
            "eta": geometry["eta"],
            "scale": geometry["scale"],
            "target": geometry["target"],
            **_inverse(geometry, intervals, error, upper),
        }
        for geometry in geometries
    ]


def _target_result(hypotheses):
    targets = sorted({hypothesis["target"] for hypothesis in hypotheses if hypothesis["delta_set"]})
    return {
        "hypotheses": hypotheses,
        "targets": targets,
        "status": "empty" if not targets else "singleton" if len(targets) == 1 else "ambiguous",
    }


def _box(description, ideal, geometries):
    fraction = _fraction(description["fraction"])
    error = fraction * ideal["distance"]
    if description["point"] == "midpoint":
        point = [(left + right) / 2 for left, right in zip(*ideal["points"], strict=True)]
    else:
        point = list(ideal["points"][0 if description["point"] == "flat" else 1])
    intervals = [[coordinate, coordinate] for coordinate in point]
    nested_box = intervals[0][0] <= intervals[1][1]
    result = _target_result(_hypotheses(geometries, intervals, error, ideal["upper"]))
    unexpanded = _target_result(_hypotheses(geometries, intervals, F(0), ideal["upper"]))
    return {
        "id": description["id"],
        "bound": description["bound"],
        "upper": ideal["upper"],
        "fraction": fraction,
        "error": error,
        "point": point,
        "intervals": intervals,
        "nested_box": nested_box,
        "expanded": _expanded(intervals, error),
        **result,
        "unexpanded": unexpanded,
    }


def _negative(description, geometry, alpha):
    delta, movement = _fraction(description["delta"]), _fraction(description["lambda"])
    ideal = _point(geometry, delta)
    ideal_law = _law(ideal)
    actual = [
        value + sign * movement for value, sign in zip(ideal_law, [-1, 1, 1, -1], strict=True)
    ]
    marginals = [actual[2] + actual[3], actual[1] + actual[3]]
    error = F(0)
    return {
        "eta": description["eta"],
        "delta": delta,
        "error": error,
        "lambda": movement,
        "ideal_q": ideal,
        "ideal_law": ideal_law,
        "actual_law": actual,
        "actual_marginals": marginals,
        "marginals_equal": marginals == ideal,
        "within_error": _norm(_minus(marginals, ideal)) <= error,
        "population_in_S": _nested(marginals),
        "nonnegative": min(actual) >= 0,
        "normalized": sum(actual, F(0)) == 1,
        "nested_support": actual[2] == 0,
        "forbidden_mass": actual[2],
        "refusal_lower": actual[2],
        "alpha": alpha,
        "refusal_exceeds_alpha": actual[2] > alpha,
        "status": "outside_nested_law",
    }


def _invariant_inverse(hypothesis):
    return {
        "delta_set": hypothesis["delta_set"],
        "endpoints": [
            {key: value for key, value in endpoint.items() if key != "constraint_values"}
            for endpoint in hypothesis["endpoints"]
        ],
    }


def _scale_pairs(protocol, geometries, classes, cases, boxes):
    scaled_classes = [_class(bound, geometries[2:]) for bound in protocol["density_bounds"]]
    lookup = {row["bound"]: row for row in scaled_classes}
    scaled_cases = [
        _case(description, lookup[description["bound"]]) for description in protocol["cases"]
    ]
    result = []
    for index in (0, 1):
        base, scaled = geometries[index], geometries[index + 2]
        actual_scaling = (
            scaled["volumes"] == [4 * value for value in base["volumes"]]
            and scaled["mass_coefficients"]
            == [[4 * value for value in pair] for pair in base["mass_coefficients"]]
            and scaled["derivative_numerators"]
            == [16 * value for value in base["derivative_numerators"]]
        )
        inverse_equal = True
        constraint_scaled = True
        targets_equal = base["target"] == scaled["target"]
        for box in boxes:
            for hypotheses in (box["hypotheses"], box["unexpanded"]["hypotheses"]):
                first, second = hypotheses[index], hypotheses[index + 2]
                inverse_equal = inverse_equal and _invariant_inverse(first) == _invariant_inverse(
                    second
                )
                constraint_scaled = constraint_scaled and second["constraints"] == [
                    [4 * value for value in pair] for pair in first["constraints"]
                ]
                constraint_scaled = constraint_scaled and len(first["endpoints"]) == len(
                    second["endpoints"]
                )
                for endpoint, other in zip(first["endpoints"], second["endpoints"], strict=True):
                    constraint_scaled = constraint_scaled and other["constraint_values"] == [
                        4 * value for value in endpoint["constraint_values"]
                    ]
                targets_equal = targets_equal and first["target"] == second["target"]
        row = {
            "worlds": [base["id"], scaled["id"]],
            "volume_factor": F(4),
            "actual_scaling": actual_scaling,
            "classes_equal": classes == scaled_classes,
            "cases_equal": cases == scaled_cases,
            "inverses_equal": inverse_equal,
            "constraints_scaled": constraint_scaled,
            "targets_equal": targets_equal,
        }
        _require(
            all(row[key] for key in row if key not in ("worlds", "volume_factor")),
            "fixed same-input scale audit",
        )
        result.append(row)
    return result


def _legacy_plan(ideal, protocol):
    slack = ideal["distance"] - F(2, protocol["grid_denominator"])
    score = protocol["quota"] * slack * slack
    positive, threshold = slack > 0, score >= 10
    sufficient = positive and threshold
    return {
        "id": "class/" + ideal["bound"],
        "kind": "class",
        "source": ideal["bound"],
        "distance": ideal["distance"],
        "in_premise": True,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "eligible": sufficient,
        "status": "certified" if sufficient else "not_certified",
        "guarantees": _guarantees(sufficient, _fraction(protocol["alpha"])),
    }


def analyze(protocol, baseline):
    """Validate both full inputs, then independently derive the bounded report."""
    _validate_inputs(protocol, baseline)
    rectangles = [
        [_fraction(value) for value in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    geometries = [_geometry(description, rectangles) for description in protocol["geometries"]]
    classes = [_class(bound, geometries[:2]) for bound in protocol["density_bounds"]]
    by_bound = {row["bound"]: row for row in classes}
    cases = [
        _case(description, by_bound[description["bound"]]) for description in protocol["cases"]
    ]
    plans = [_plan(case, protocol) for case in cases]
    boxes = [
        _box(description, by_bound[description["bound"]], geometries)
        for description in protocol["boxes"]
    ]
    legacy = [_legacy_plan(ideal, protocol) for ideal in classes]
    _exact(classes, baseline["classes"])
    _exact(legacy, baseline["plans"])
    alpha = _fraction(protocol["alpha"])
    return {
        "schema": "qr05bv-report-v1",
        "planning": {
            "quota": protocol["quota"],
            "grid_denominator": protocol["grid_denominator"],
            "alpha": alpha,
            "tail_allocations": [_fraction(pair) for pair in protocol["tail_allocations"]],
            "threshold": F(10),
            "log_upper": F(5),
            "basis": "ln80_lt_5",
        },
        "geometries": geometries,
        "classes": classes,
        "cases": cases,
        "plans": plans,
        "boxes": boxes,
        "negative": _negative(protocol["negative"], geometries[0], alpha),
        "scale_pairs": _scale_pairs(protocol, geometries, classes, cases, boxes),
        "baseline": {
            "schema": "qr05bv-bt-comparison-v1",
            "zero_ids": [
                description["id"]
                for description in protocol["cases"]
                if description["fraction"][0] == 0
            ],
            "classes_equal": classes == baseline["classes"],
            "plans_equal": legacy == baseline["plans"],
            "plans": legacy,
        },
    }
