"""Independent exact BT reference: quadrature, breakpoints and dual witnesses.

No files, historical executors, logarithms, confidence tails or quota loops.
The only report entry point is analyze(protocol, baseline).
"""

from fractions import Fraction as F
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _scan(value, active=None, depth=0, budget=None):
    """Admit native trees, rejecting cycles while allowing harmless sharing."""
    if active is None:
        active = set()
    if budget is None:
        budget = [8192]
    budget[0] -= 1
    _require(budget[0] >= 0 and depth <= 32, "native tree budget")
    kind = type(value)
    if kind in (dict, list):
        ident = id(value)
        _require(ident not in active, "cyclic native tree")
        active.add(ident)
        if kind is dict:
            _require(all(type(k) is str and not k.startswith("$") for k in value), "native keys")
            children = value.values()
        else:
            children = value
        for child in children:
            _scan(child, active, depth + 1, budget)
        active.remove(ident)
    else:
        _require(kind in (str, int, bool, F), "native leaf type")


def _exact(value, expected):
    _require(type(value) is type(expected), "fixed input native type")
    if type(expected) is dict:
        _require(set(value) == set(expected), "fixed input keys")
        for key in expected:
            _exact(value[key], expected[key])
    elif type(expected) is list:
        _require(len(value) == len(expected), "fixed input list length")
        for actual, wanted in zip(value, expected, strict=True):
            _exact(actual, wanted)
    else:
        _require(value == expected, "fixed input value")


def _validate_inputs(protocol, baseline):
    # Both whole native trees are admitted before arithmetic or quadrature.
    _scan(protocol)
    _scan(baseline)
    expected = {
        "schema": "qr05bt-protocol-v1",
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
        "fixtures": [
            {"id": "flat_0", "eta": 0, "delta": [0, 1]},
            {"id": "flat_1", "eta": 0, "delta": [1, 1]},
            {"id": "flat_interior", "eta": 0, "delta": [16, 11]},
            {"id": "conformal_0", "eta": 1, "delta": [0, 1]},
            {"id": "conformal_1", "eta": 1, "delta": [1, 1]},
            {"id": "conformal_interior", "eta": 1, "delta": [45, 158]},
        ],
        "boxes": {
            "fixtures": ["flat_interior", "conformal_interior"],
            "bound": "two",
            "kinds": ["half_square", "touch_square", "contact_rectangle"],
        },
        "rational_control": {
            "quota": 40,
            "grid_denominator": 8,
            "radius": [1, 4],
            "distance": [3, 4],
        },
        "baseline": {
            "schema": "qr05bt-br-baseline-v1",
            "quota": 4,
            "grid_denominator": 256,
            "alpha": [1, 20],
            "sha256": "9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c",
        },
        "coverage": {
            "geometries": 4,
            "fixtures": 6,
            "distances": 24,
            "classes": 4,
            "plans": 28,
            "scale_pairs": 2,
            "baseline_intervals": 5,
            "baseline_comparisons": 28,
            "boxes": 6,
            "rational_controls": 1,
            "obstructions": 1,
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
    _require(type(baseline) is dict, "baseline dictionary")
    _require(
        set(baseline) == {"schema", "quota", "grid_denominator", "alpha", "intervals"},
        "baseline keys",
    )
    for key, wanted in (
        ("schema", "qr05bt-br-baseline-v1"),
        ("quota", 4),
        ("grid_denominator", 256),
    ):
        _exact(baseline[key], wanted)
    alpha = baseline["alpha"]
    _require(type(alpha) is F, "baseline alpha Fraction")
    _require(alpha.numerator == 1 and alpha.denominator == 20, "baseline alpha")
    rows = baseline["intervals"]
    _require(type(rows) is list and len(rows) == 5, "baseline interval rows")
    endpoints = [
        [(0, 1), (171, 256)],
        [(0, 1), (109, 128)],
        [(3, 64), (61, 64)],
        [(19, 128), (1, 1)],
        [(85, 256), (1, 1)],
    ]
    for k, row in enumerate(rows):
        _require(type(row) is dict and set(row) == {"k", "interval"}, "baseline row keys")
        _exact(row["k"], k)
        values = row["interval"]
        _require(type(values) is list and len(values) == 2, "baseline closed interval")
        for value, (numerator, denominator) in zip(values, endpoints[k], strict=True):
            _require(type(value) is F, "baseline endpoint Fraction")
            _require(
                value.numerator == numerator and value.denominator == denominator,
                "baseline endpoint value",
            )


def _fraction(pair):
    return F(pair[0], pair[1])


def _dot(left, right):
    return sum((x * y for x, y in zip(left, right, strict=True)), F(0))


def _difference(left, right):
    return [x - y for x, y in zip(left, right, strict=True)]


def _norm(vector):
    return max(abs(x) for x in vector)


def _sign(value):
    return F(1) if value > 0 else F(-1) if value < 0 else F(0)


def _axis(low, high):
    _require(low < high, "positive integration interval")
    unit = (high - low) / 6
    return [(low, unit), ((low + high) / 2, 4 * unit), (high, unit)]


def _integrate(bounds, eta, scale, delta=None):
    """Direct tensor Simpson of the actual proper/sampling density."""
    u0, u1, v0, v1 = bounds
    total = F(0)
    for u, wu in _axis(u0, u1):
        for v, wv in _axis(v0, v1):
            density = F(scale, 2) * (1 + eta * u * v)
            if delta is not None:
                density *= 1 + delta * u * v
            total += wu * wv * density
    return total


def _masses(geometry, delta):
    return [a + b * delta for a, b in geometry["mass_coefficients"]]


def _point(geometry, delta):
    masses = _masses(geometry, delta)
    _require(masses[0] > 0, "positive original mass normalizer")
    return [masses[1] / masses[0], masses[2] / masses[0]]


def _primitive_line(start, end):
    direction = _difference(end, start)
    normal = [direction[1], -direction[0]]
    values = normal + [_dot(normal, start)]
    _require(any(values), "nonconstant family line")
    denominator = 1
    for value in values:
        denominator = denominator * value.denominator // gcd(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator) for value in values]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    _require(divisor > 0 and integers[2] != 0, "nonzero primitive line")
    orientation = 1 if integers[2] > 0 else -1
    return [F(orientation * value // divisor) for value in integers]


def _geometry(description, regions):
    eta, scale = description["eta"], description["scale"]
    volumes = [_integrate(region, eta, scale) for region in regions]
    coefficients = []
    for region in regions:
        constant = _integrate(region, eta, scale, F(0))
        at_one = _integrate(region, eta, scale, F(1))
        coefficients.append([constant, at_one - constant])
    aq, bq = coefficients[0]
    derivatives = [bi * aq - ai * bq for ai, bi in coefficients[1:]]
    positive = min(aq, aq + 2 * bq) > 0
    decreasing = all(value < 0 for value in derivatives)
    _require(positive and decreasing, "continuous normalizer/monotonicity certificate")
    geometry = {
        "id": description["id"],
        "eta": eta,
        "scale": scale,
        "volumes": volumes,
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "target": volumes[1] / volumes[0],
        "line": _primitive_line(
            [coefficients[i][0] / aq for i in (1, 2)],
            [(coefficients[i][0] + 2 * coefficients[i][1]) / (aq + 2 * bq) for i in (1, 2)],
        ),
        "positive_normalizer": positive,
        "decreasing": decreasing,
    }
    line = geometry["line"]
    for column in (0, 1):
        _require(
            line[0] * coefficients[1][column] + line[1] * coefficients[2][column]
            == line[2] * coefficients[0][column],
            "whole affine-ratio family lies on derived line",
        )
    expected_line = [-20, 16, 1] if eta == 0 else [-9520, 7296, 371]
    _require(line == [F(x) for x in expected_line], "specified supporting line")
    _require(geometry["target"] == F(16 + eta, 16 * (4 + eta)), "proper-volume target")
    return geometry


def _segment(geometry, upper):
    start, end = _point(geometry, F(0)), _point(geometry, upper)
    vector = _difference(end, start)
    _require(
        (upper == 0 and vector == [F(0), F(0)])
        or (upper > 0 and all(value < 0 for value in vector)),
        "point or strictly decreasing complete segment",
    )
    return {"start": start, "end": end, "vector": vector}


def _on_segment(segment, parameter):
    return [a + parameter * v for a, v in zip(segment["start"], segment["vector"], strict=True)]


def _density_from_parameter(eta, upper, parameter):
    _require(0 <= parameter <= 1 and upper >= 0, "segment parameter domain")
    if upper == 0:
        return F(0)
    if eta == 0:
        numerator = 4 * upper * parameter
        denominator = 4 + upper * (1 - parameter)
    else:
        _require(eta == 1, "geometry eta")
        numerator = 45 * upper * parameter
        denominator = 45 + 13 * upper * (1 - parameter)
    _require(denominator > 0, "positive parameter-inversion denominator")
    result = numerator / denominator
    _require(0 <= result <= upper, "mapped density domain")
    return result


def _projection(p, segment, opposite_eta, upper):
    """Choose only among breakpoints of the four affine absolute-value pieces."""
    offset = _difference(p, segment["start"])
    vector = segment["vector"]
    if upper == 0:
        _require(vector == [F(0), F(0)], "degenerate point segment")
        parameter, raw, location = F(0), [], "point"
    else:
        _require(all(v < 0 for v in vector), "strictly decreasing segment")
        candidates = {F(0), F(1)}
        c1, c2 = offset
        m1, m2 = -vector[0], -vector[1]
        equations = [(c1, m1), (c2, m2), (c1 - c2, m1 - m2), (c1 + c2, m1 + m2)]
        for constant, slope in equations:
            if slope == 0:
                # A nonzero constant has no root; an identical zero adds no
                # isolated breakpoint. Endpoints already cover a linear piece.
                if constant == 0:
                    continue
                continue
            candidate = -constant / slope
            if 0 <= candidate <= 1:
                candidates.add(candidate)
        evaluated = [
            (_norm(_difference(p, _on_segment(segment, t))), t) for t in sorted(candidates)
        ]
        _, parameter = min(evaluated)
        # Diagnostic computed AFTER selection; it never supplies a candidate.
        balance = sum(offset, F(0)) / sum(vector, F(0))
        raw = [balance]
        if balance < 0:
            location = "before"
        elif balance == 0:
            location = "start"
        elif balance < 1:
            location = "interior"
        elif balance == 1:
            location = "end"
        else:
            location = "after"
        _require(parameter == min(F(1), max(F(0), balance)), "breakpoint/balance agreement")
    contact = _on_segment(segment, parameter)
    residual = _difference(p, contact)
    return {
        "raw": raw,
        "t": parameter,
        "location": location,
        "delta": _density_from_parameter(opposite_eta, upper, parameter),
        "q": contact,
        "residual": residual,
        "distance": _norm(residual),
    }


def _lower(p, segment, projection, upper):
    parameter, distance, residual = projection["t"], projection["distance"], projection["residual"]
    kind = (
        "point"
        if upper == 0
        else "start"
        if parameter == 0
        else "end"
        if parameter == 1
        else "interior"
    )
    normal = [F(0), F(0)]
    if distance == 0:
        pass
    elif kind == "point":
        coordinate = next(i for i in range(2) if abs(residual[i]) == distance)
        normal[coordinate] = _sign(residual[coordinate])
    elif kind == "start":
        available = [i for i in range(2) if residual[i] == distance]
        _require(bool(available), "start has a positive active residual")
        normal[available[0]] = F(1)
    elif kind == "end":
        available = [i for i in range(2) if residual[i] == -distance]
        _require(bool(available), "end has a negative active residual")
        normal[available[0]] = F(-1)
    else:
        vector = segment["vector"]
        total = abs(vector[0]) + abs(vector[1])
        _require(total > 0 and residual[0] == -residual[1], "interior opposite-face contact")
        normal = [
            _sign(residual[0]) * abs(vector[1]) / total,
            _sign(residual[1]) * abs(vector[0]) / total,
        ]
    constant = _dot(normal, _difference(p, segment["start"]))
    slope = -_dot(normal, segment["vector"])
    values = [constant, constant + slope]
    norm = sum((abs(x) for x in normal), F(0))
    _require(norm <= 1, "dual l1 norm")
    _require(min(values) == distance, "whole-segment lower bound attained")
    _require(constant + slope * parameter == distance, "contact dual equality")
    return {
        "kind": kind,
        "normal": normal,
        "coefficients": [constant, slope],
        "endpoint_values": values,
        "norm": norm,
        "value": min(values),
    }


def _fixture(description, geometry, regions):
    delta = _fraction(description["delta"])
    masses = [_integrate(region, description["eta"], 1, delta) for region in regions]
    _require(masses == _masses(geometry, delta), "direct fixture masses match affine coefficients")
    q = [masses[1] / masses[0], masses[2] / masses[0]]
    _require(0 < q[0] < q[1] < 1, "three positive allowed categories")
    return {
        "id": description["id"],
        "eta": description["eta"],
        "delta": delta,
        "target": geometry["target"],
        "masses": masses,
        "q": q,
        "one_point": [1 - q[1], q[1] - q[0], F(0), q[0]],
    }


def _distance(fixture, bound, geometry):
    upper = _fraction(bound["upper"])
    segment = _segment(geometry, upper)
    p = list(fixture["q"])
    projection = _projection(p, segment, geometry["eta"], upper)
    _require(_point(geometry, projection["delta"]) == projection["q"], "original ratio contact")
    return {
        "id": fixture["id"] + "/" + bound["id"],
        "fixture": fixture["id"],
        "bound": bound["id"],
        "in_premise": 0 <= fixture["delta"] <= upper,
        "opposite_eta": geometry["eta"],
        "p": p,
        "segment": segment,
        "projection": projection,
        "lower": _lower(p, segment, projection, upper),
    }


def _parameter_of_point(segment, point):
    vector = segment["vector"]
    if vector == [F(0), F(0)]:
        _require(point == segment["start"], "point segment contact")
        return F(0)
    parameter = (point[0] - segment["start"][0]) / vector[0]
    _require(
        0 <= parameter <= 1 and _on_segment(segment, parameter) == point, "complete segment contact"
    )
    return parameter


def _class_margin(bound, flat, conformal):
    upper = _fraction(bound["upper"])
    segments = [_segment(flat, upper), _segment(conformal, upper)]
    ordered = upper < 1
    deltas = [upper if ordered else F(1), F(0)]
    points = [_point(flat, deltas[0]), _point(conformal, deltas[1])]
    parameters = [_parameter_of_point(s, p) for s, p in zip(segments, points, strict=True)]
    residual = _difference(points[0], points[1])
    distance = _norm(residual)
    normal = [F(0), F(1) if ordered else F(0)]
    constant = _dot(normal, _difference(segments[0]["start"], segments[1]["start"]))
    mt = _dot(normal, segments[0]["vector"])
    ms = -_dot(normal, segments[1]["vector"])
    corners = [constant, constant + ms, constant + mt, constant + mt + ms]
    norm = sum((abs(x) for x in normal), F(0))
    _require(norm <= 1 and min(corners) == distance, "global affine-corner lower certificate")
    _require(
        constant + mt * parameters[0] + ms * parameters[1] == distance, "global attaining pair"
    )
    if ordered:
        _require(0 <= residual[0] <= residual[1], "ordered second-coordinate dominance")
        _require(mt <= 0 and ms >= 0, "ordered family monotonicity")
        closed_form = 3 * (1 - upper) / (16 * (4 + upper))
    else:
        _require(residual == [F(0), F(0)] and deltas[0] <= upper, "admitted collision")
        closed_form = F(0)
    _require(
        distance == closed_form, "analytical class margin agrees with contact and lower certificate"
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
        "closed_form": closed_form,
        "lower": {
            "normal": normal,
            "coefficients": [constant, mt, ms],
            "corner_values": corners,
            "norm": norm,
            "value": min(corners),
        },
    }


def _plan(identifier, kind, source, distance, in_premise, quota, grid_denominator):
    _require(type(distance) is F and distance >= 0, "planning distance")
    _require(type(in_premise) is bool, "planning premise flag")
    _require(type(quota) is int and quota > 0, "planning quota")
    _require(type(grid_denominator) is int and grid_denominator > 0, "planning grid")
    slack = distance - F(2, grid_denominator)
    score = quota * slack * slack
    grid_positive = slack > 0
    threshold_holds = score >= 10
    sufficient = grid_positive and threshold_holds
    eligible = in_premise and sufficient
    status = "out_of_premise" if not in_premise else "certified" if sufficient else "not_certified"
    guarantees = []
    if eligible:
        guarantees.append(
            {
                "correct_singleton_at_least": F(19, 20),
                "conditional_wrong_singleton_at_most": F(1, 20),
            }
        )
    return {
        "id": identifier,
        "kind": kind,
        "source": source,
        "distance": distance,
        "in_premise": in_premise,
        "slack": slack,
        "score": score,
        "grid_positive": grid_positive,
        "threshold_holds": threshold_holds,
        "sufficient": sufficient,
        "eligible": eligible,
        "status": status,
        "guarantees": guarantees,
    }


def _scale_pairs(geometries, fixtures, distances, classes, bounds):
    result = []
    fixture_by_id = {f["id"]: f for f in fixtures}
    bound_by_id = {b["id"]: _fraction(b["upper"]) for b in bounds}
    scaled_classes = [
        _class_margin(bound, geometries["flat_x4"], geometries["conformal_x4"]) for bound in bounds
    ]
    class_certificates_equal = scaled_classes == classes
    _require(class_certificates_equal, "scaled class contacts and complete lower certificates")
    for eta, unit_name, scaled_name in ((0, "flat", "flat_x4"), (1, "conformal", "conformal_x4")):
        unit, scaled = geometries[unit_name], geometries[scaled_name]
        actual_scaling = scaled["volumes"] == [4 * x for x in unit["volumes"]]
        actual_scaling = actual_scaling and scaled["mass_coefficients"] == [
            [4 * x for x in row] for row in unit["mass_coefficients"]
        ]
        _require(
            scaled["derivative_numerators"] == [16 * x for x in unit["derivative_numerators"]],
            "derivative scaling",
        )
        target_equal = unit["target"] == scaled["target"]
        _require(unit["line"] == scaled["line"], "scale-invariant line")
        segments_equal = all(_segment(unit, b) == _segment(scaled, b) for b in bound_by_id.values())
        distances_equal = class_certificates_equal
        for row in distances:
            fixture = fixture_by_id[row["fixture"]]
            upper = bound_by_id[row["bound"]]
            if fixture["eta"] == eta:
                p = _point(scaled, fixture["delta"])
                _require(
                    _masses(scaled, fixture["delta"]) == [4 * x for x in fixture["masses"]],
                    "scaled fixture masses",
                )
                segment = row["segment"]
            else:
                p = row["p"]
                segment = _segment(scaled, upper)
            projection = _projection(p, segment, row["opposite_eta"], upper)
            lower = _lower(p, segment, projection, upper)
            distances_equal = distances_equal and (
                p == row["p"]
                and segment == row["segment"]
                and projection == row["projection"]
                and lower == row["lower"]
            )
        _require(
            actual_scaling and target_equal and segments_equal and distances_equal,
            "full fixed scale comparison",
        )
        result.append(
            {
                "worlds": [unit_name, scaled_name],
                "volume_factor": F(4),
                "actual_scaling": actual_scaling,
                "target_equal": target_equal,
                "segments_equal": segments_equal,
                "distances_equal": distances_equal,
            }
        )
    return result


def _baseline_report(baseline, plans):
    intervals = []
    for row in baseline["intervals"]:
        low, high = row["interval"]
        intervals.append({"k": row["k"], "interval": [low, high], "width": high - low})
    maximum = max(row["width"] for row in intervals)
    return {
        "schema": baseline["schema"],
        "quota": baseline["quota"],
        "grid_denominator": baseline["grid_denominator"],
        "alpha": baseline["alpha"],
        "intervals": intervals,
        "max_width": maximum,
        "maximizers": [row["k"] for row in intervals if row["width"] == maximum],
        "comparisons": [
            {
                "id": row["id"],
                "distance": row["distance"],
                "strict_width_sufficient": maximum < row["distance"],
            }
            for row in plans
        ],
    }


def _box_delta_set(segment, opposite_eta, upper, intervals):
    """Clip one shared segment parameter, then map its complete interval."""
    low, high = F(0), F(1)
    for start, velocity, (left, right) in zip(
        segment["start"], segment["vector"], intervals, strict=True
    ):
        _require(left <= right, "ordered algebraic box")
        if velocity == 0:
            if not left <= start <= right:
                return []
            continue
        endpoints = sorted([(left - start) / velocity, (right - start) / velocity])
        low, high = max(low, endpoints[0]), min(high, endpoints[1])
        if low > high:
            return []
    for parameter in (low, high):
        point = _on_segment(segment, parameter)
        _require(
            all(
                left <= value <= right
                for value, (left, right) in zip(point, intervals, strict=True)
            ),
            "clipped segment endpoint",
        )
    result = [
        _density_from_parameter(opposite_eta, upper, low),
        _density_from_parameter(opposite_eta, upper, high),
    ]
    _require(result[0] <= result[1], "monotone density mapping")
    return result


def _box_row(distance_row, kind, opposite_geometry, upper):
    p = distance_row["p"]
    contact = distance_row["projection"]["q"]
    distance = distance_row["projection"]["distance"]
    _require(distance > 0, "prespecified positive-distance box controls")
    if kind == "half_square":
        radius = distance / 2
        intervals = [[value - radius, value + radius] for value in p]
    elif kind == "touch_square":
        intervals = [[value - distance, value + distance] for value in p]
    else:
        _require(kind == "contact_rectangle", "fixed box kind")
        intervals = [[min(a, b), max(a, b)] for a, b in zip(p, contact, strict=True)]
    widths = [high - low for low, high in intervals]
    maximum = max(widths)
    delta_set = _box_delta_set(
        distance_row["segment"], distance_row["opposite_eta"], upper, intervals
    )
    for delta in delta_set:
        q = _point(opposite_geometry, delta)
        _require(
            all(low <= value <= high for value, (low, high) in zip(q, intervals, strict=True)),
            "original ratio in algebraic box",
        )
    contains_true = all(
        low <= value <= high for value, (low, high) in zip(p, intervals, strict=True)
    )
    contains_contact = all(
        low <= value <= high for value, (low, high) in zip(contact, intervals, strict=True)
    )
    admits = bool(delta_set)
    _require(contains_true, "box retains its declared center")
    if kind == "half_square":
        _require(
            not admits and not contains_contact and maximum == distance,
            "strict full width is not necessary",
        )
    else:
        _require(admits and contains_contact, "closed contact must be admitted")
    if kind == "contact_rectangle":
        _require(
            maximum == distance and maximum / 2 < distance, "half-width/nonstrict counterexample"
        )
    return {
        "id": distance_row["fixture"] + "/" + kind,
        "distance_id": distance_row["id"],
        "kind": kind,
        "intervals": intervals,
        "widths": widths,
        "max_width": maximum,
        "half_width": maximum / 2,
        "contains_true": contains_true,
        "contains_contact": contains_contact,
        "opposite_delta_set": delta_set,
        "admits_opposite": admits,
        "strict_width_condition": maximum < distance,
        "half_width_condition": maximum / 2 < distance,
        "nonstrict_width_condition": maximum <= distance,
    }


def _rational_bound():
    terms = [F(1)]
    for degree in range(1, 6):
        terms.append(terms[-1] * 5 / degree)
    partial = sum(terms, F(0))
    strict = partial > 80
    _require(partial == F(1097, 12) and strict, "positive exponential-series lower certificate")
    return {
        "terms": terms,
        "partial_sum": partial,
        "threshold": F(80),
        "log_upper": F(5),
        "strict": strict,
    }


def _rational_control(description):
    quota, denominator = description["quota"], description["grid_denominator"]
    radius, distance = _fraction(description["radius"]), _fraction(description["distance"])
    step = F(1, denominator)
    square = 2 * quota * radius * radius
    width = 2 * radius + 2 * step
    slack = distance - 2 * step
    main_score = quota * slack * slack
    radius_test = radius >= 0 and square >= 5 and width <= distance
    direct_test = slack > 0 and main_score >= 10
    _require(radius_test and direct_test, "rational equality control")
    _require(
        square == 5 and width == distance and main_score == 10, "both rational equality boundaries"
    )
    return {
        "quota": quota,
        "grid_denominator": denominator,
        "radius": radius,
        "distance": distance,
        "step": step,
        "square_score": square,
        "width": width,
        "main_score": main_score,
        "radius_test": radius_test,
        "direct_test": direct_test,
        "strict_slack_basis": "ln80_lt_5",
    }


def _normalized_polynomial(geometry, delta):
    normalizer = _masses(geometry, delta)[0]
    _require(normalizer > 0, "whole-point normalization")
    values = []
    for z in (F(0), F(1, 2), F(1)):
        # Algebraic evaluation at uv=z; this is not a new observed record.
        values.append(
            F(geometry["scale"], 2) * (1 + geometry["eta"] * z) * (1 + delta * z) / normalizer
        )
    constant = values[0]
    quadratic = 2 * (values[2] - 2 * values[1] + values[0])
    linear = values[2] - constant - quadratic
    _require(constant + linear / 2 + quadratic / 4 == values[1], "interpolated normalized density")
    return [constant, linear, quadratic]


def _obstruction(flat, conformal):
    deltas = [F(1), F(0)]
    first, second = _point(flat, deltas[0]), _point(conformal, deltas[1])
    _require(first == second, "same complete membership-pair law")
    polynomials = [
        _normalized_polynomial(flat, deltas[0]),
        _normalized_polynomial(conformal, deltas[1]),
    ]
    point_equal = polynomials[0] == polynomials[1]
    targets = [flat["target"], conformal["target"]]
    _require(point_equal and targets[0] != targets[1], "whole-point target obstruction")
    return {
        "deltas": deltas,
        "q": first,
        "targets": targets,
        "target_gap": targets[0] - targets[1],
        "normalized_polynomials": polynomials,
        "point_equal": point_equal,
    }


def analyze(protocol, baseline):
    """Return the complete fixed BT report without reading either input from files."""
    _validate_inputs(protocol, baseline)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    geometries = [_geometry(row, regions) for row in protocol["geometries"]]
    geometry_by_id = {row["id"]: row for row in geometries}
    unit = {0: geometry_by_id["flat"], 1: geometry_by_id["conformal"]}
    fixtures = [_fixture(row, unit[row["eta"]], regions) for row in protocol["fixtures"]]
    bounds = protocol["density_bounds"]
    distances = [
        _distance(fixture, bound, unit[1 - fixture["eta"]])
        for fixture in fixtures
        for bound in bounds
    ]
    classes = [_class_margin(bound, unit[0], unit[1]) for bound in bounds]
    quota, denominator = protocol["quota"], protocol["grid_denominator"]
    plans = [
        _plan(
            "pointwise/" + row["id"],
            "pointwise",
            row["id"],
            row["projection"]["distance"],
            row["in_premise"],
            quota,
            denominator,
        )
        for row in distances
    ]
    plans.extend(
        _plan(
            "class/" + row["bound"],
            "class",
            row["bound"],
            row["distance"],
            True,
            quota,
            denominator,
        )
        for row in classes
    )
    distance_by_id = {row["id"]: row for row in distances}
    upper_by_id = {row["id"]: _fraction(row["upper"]) for row in bounds}
    boxes = []
    for fixture_id in protocol["boxes"]["fixtures"]:
        row = distance_by_id[fixture_id + "/" + protocol["boxes"]["bound"]]
        for kind in protocol["boxes"]["kinds"]:
            boxes.append(_box_row(row, kind, unit[row["opposite_eta"]], upper_by_id[row["bound"]]))
    report = {
        "schema": "qr05bt-report-v1",
        "geometries": geometries,
        "fixtures": fixtures,
        "distances": distances,
        "classes": classes,
        "plans": plans,
        "scale_pairs": _scale_pairs(geometry_by_id, fixtures, distances, classes, bounds),
        "baseline": _baseline_report(baseline, plans),
        "boxes": boxes,
        "rational_bound": _rational_bound(),
        "rational_controls": [_rational_control(protocol["rational_control"])],
        "obstruction": _obstruction(unit[0], unit[1]),
    }
    census = {
        "geometries": len(geometries),
        "fixtures": len(fixtures),
        "distances": len(distances),
        "classes": len(classes),
        "plans": len(plans),
        "scale_pairs": len(report["scale_pairs"]),
        "baseline_intervals": len(report["baseline"]["intervals"]),
        "baseline_comparisons": len(report["baseline"]["comparisons"]),
        "boxes": len(boxes),
        "rational_controls": len(report["rational_controls"]),
        "obstructions": 1,
    }
    _exact(census, protocol["coverage"])
    _scan(report, budget=[131072])
    return report
