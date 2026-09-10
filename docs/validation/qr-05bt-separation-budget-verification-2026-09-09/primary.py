"""Exact BT monomial masses, clipped balances and dual lower certificates.

Import defines functions only. analyze(protocol, baseline) has no file
access, historical runtime imports, tail tables or large-quota iteration.
"""

from fractions import Fraction as F
from math import factorial, gcd, lcm


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native_input(value, fractions=False, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (int, str) or fractions and kind is F:
        return
    _require(kind in (dict, list), "native input containers and scalars")
    identity = id(value)
    _require(identity not in active, "cyclic input")
    if kind is dict:
        _require(all(type(key) is str for key in value), "native input keys")
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native_input(child, fractions, active)
    finally:
        active.remove(identity)


def _validate(protocol, baseline):
    # Both complete native trees are checked before any rational construction.
    _native_input(protocol)
    _native_input(baseline, True)
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
    _require(type(protocol) is dict and protocol == expected, "complete fixed BT protocol")
    _require(
        type(baseline) is dict
        and set(baseline) == {"schema", "quota", "grid_denominator", "alpha", "intervals"},
        "complete baseline fields",
    )
    _require(
        type(baseline["schema"]) is str
        and baseline["schema"] == "qr05bt-br-baseline-v1"
        and type(baseline["quota"]) is int
        and baseline["quota"] == 4
        and type(baseline["grid_denominator"]) is int
        and baseline["grid_denominator"] == 256,
        "baseline native metadata",
    )
    _require(
        type(baseline["alpha"]) is F
        and baseline["alpha"].numerator == 1
        and baseline["alpha"].denominator == 20,
        "baseline exact alpha",
    )
    _require(
        type(baseline["intervals"]) is list and len(baseline["intervals"]) == 5,
        "five inherited interval rows",
    )
    expected_pairs = [
        ((0, 1), (171, 256)),
        ((0, 1), (109, 128)),
        ((3, 64), (61, 64)),
        ((19, 128), (1, 1)),
        ((85, 256), (1, 1)),
    ]
    for k, (row, pairs) in enumerate(zip(baseline["intervals"], expected_pairs, strict=True)):
        _require(type(row) is dict and set(row) == {"k", "interval"}, "baseline row fields")
        _require(type(row["k"]) is int and row["k"] == k, "baseline count metadata")
        _require(
            type(row["interval"]) is list and len(row["interval"]) == 2, "baseline endpoint shape"
        )
        for value, (numerator, denominator) in zip(row["interval"], pairs, strict=True):
            _require(
                type(value) is F
                and value.numerator == numerator
                and value.denominator == denominator,
                "unchanged exact baseline endpoint",
            )


def _fraction(pair):
    _require(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "native rational pair",
    )
    numerator, denominator = pair
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "reduced rational pair")
    return F(numerator, denominator)


def _clean(poly):
    return {powers: value for powers, value in poly.items() if value != 0}


def _scale(poly, scalar):
    return _clean({powers: scalar * value for powers, value in poly.items()})


def _add(left, right):
    result = dict(left)
    for powers, value in right.items():
        result[powers] = result.get(powers, F(0)) + value
    return _clean(result)


def _multiply(left, right):
    result = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            powers = (i + k, j + ell)
            result[powers] = result.get(powers, F(0)) + a * b
    return _clean(result)


def _integrate(poly, rectangle):
    u0, u1, v0, v1 = rectangle
    _require(u0 < u1 and v0 < v1, "positive integration rectangle")
    return sum(
        (
            coefficient
            * (u1 ** (i + 1) - u0 ** (i + 1))
            * (v1 ** (j + 1) - v0 ** (j + 1))
            / ((i + 1) * (j + 1))
            for (i, j), coefficient in poly.items()
        ),
        F(0),
    )


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def _subtract(left, right):
    return [a - b for a, b in zip(left, right, strict=True)]


def _norm(vector):
    return max(abs(value) for value in vector)


def _sign(value):
    return F(1) if value > 0 else F(-1) if value < 0 else F(0)


def _affine(coefficients, delta):
    return coefficients[0] + coefficients[1] * delta


def _primitive_line(coefficients):
    (a_q, b_q), (a_1, b_1), (a_2, b_2) = coefficients
    raw = [a_2 * b_q - a_q * b_2, a_q * b_1 - a_1 * b_q, a_2 * b_1 - a_1 * b_2]
    common = lcm(*(value.denominator for value in raw))
    integers = [(value * common).numerator for value in raw]
    divisor = gcd(*(abs(value) for value in integers))
    _require(divisor > 0 and integers[2] != 0, "nondegenerate primitive supporting line")
    orientation = 1 if integers[2] > 0 else -1
    line = [F(orientation * value // divisor) for value in integers]
    _require(
        all(
            line[0] * coefficients[1][j] + line[1] * coefficients[2][j]
            == line[2] * coefficients[0][j]
            for j in (0, 1)
        ),
        "supporting line is an affine-mass identity",
    )
    return line


def _geometry(raw, regions):
    scale, eta = F(raw["scale"]), F(raw["eta"])
    proper = _clean({(0, 0): scale / 2, (1, 1): scale * eta / 2})
    slope = _multiply(proper, {(1, 1): F(1)})
    volumes = [_integrate(proper, rectangle) for rectangle in regions]
    coefficients = [
        [_integrate(poly, rectangle) for poly in (proper, slope)] for rectangle in regions
    ]
    a_q, b_q = coefficients[0]
    normalizer = all(a_q + b_q * delta > 0 for delta in (F(0), F(2)))
    derivatives = [b * a_q - a * b_q for a, b in coefficients[1:]]
    decreasing = all(value < 0 for value in derivatives)
    _require(normalizer and decreasing, "continuous positive normalization and strict decrease")
    line = _primitive_line(coefficients)
    expected_line = [-20, 16, 1] if raw["eta"] == 0 else [-9520, 7296, 371]
    _require(line == [F(value) for value in expected_line], "derived exact family line")
    return (
        {
            "id": raw["id"],
            "eta": raw["eta"],
            "scale": raw["scale"],
            "volumes": volumes,
            "mass_coefficients": coefficients,
            "derivative_numerators": derivatives,
            "target": volumes[1] / volumes[0],
            "line": line,
            "positive_normalizer": normalizer,
            "decreasing": decreasing,
        },
        proper,
        slope,
    )


def _masses(geometry, delta):
    return [_affine(row, delta) for row in geometry["mass_coefficients"]]


def _forward(geometry, delta):
    masses = _masses(geometry, delta)
    _require(0 < masses[1] < masses[2] < masses[0], "positive normalized nested categories")
    return [masses[index] / masses[0] for index in (1, 2)]


def _fixture(raw, compiled, regions):
    geometry, proper, slope = compiled
    delta = _fraction(raw["delta"])
    weighted = _add(proper, _scale(slope, delta))
    masses = [_integrate(weighted, rectangle) for rectangle in regions]
    _require(masses == _masses(geometry, delta), "direct fixture integration and affine masses")
    q = _forward(geometry, delta)
    law = [1 - q[1], q[1] - q[0], F(0), q[0]]
    _require(sum(law, F(0)) == 1, "fixture paired one-point law")
    return {
        "id": raw["id"],
        "eta": raw["eta"],
        "delta": delta,
        "target": geometry["target"],
        "masses": masses,
        "q": q,
        "one_point": law,
    }


def _segment(geometry, upper):
    start, end = _forward(geometry, F(0)), _forward(geometry, upper)
    vector = _subtract(end, start)
    if upper == 0:
        _require(vector == [F(0), F(0)], "point segment")
    else:
        _require(all(value < 0 for value in vector), "strictly decreasing segment direction")
        a_q, b_q = geometry["mass_coefficients"][0]
        # This coefficient identity establishes the complete rational
        # reparametrization, not merely agreement at the two endpoints.
        for i, (a, b) in enumerate(geometry["mass_coefficients"][1:]):
            _require(
                a == start[i] * a_q
                and b == start[i] * b_q + (a_q + b_q * upper) * vector[i] / upper,
                "whole-family segment parameter identity",
            )
    return {"start": start, "end": end, "vector": vector}


def _density(eta, upper, parameter):
    _require(0 <= parameter <= 1 and 0 <= upper <= 2, "bounded segment parameter")
    a, b = (F(4), F(1)) if eta == 0 else (F(45), F(13))
    denominator = a + b * upper * (1 - parameter)
    _require(denominator > 0, "positive density recovery denominator")
    return a * upper * parameter / denominator


def _parameter(eta, upper, delta):
    _require(0 <= delta <= upper <= 2, "contact density in its declared segment")
    if upper == 0:
        return F(0)
    a, b = (F(4), F(1)) if eta == 0 else (F(45), F(13))
    parameter = delta * (a + b * upper) / (upper * (a + b * delta))
    _require(
        0 <= parameter <= 1 and _density(eta, upper, parameter) == delta,
        "exact contact parameter inverse",
    )
    return parameter


def _lower(p, segment, projection, kind):
    residual, distance = projection["residual"], projection["distance"]
    vector = segment["vector"]
    normal = [F(0), F(0)]
    if distance == 0:
        pass
    elif kind == "point":
        index = next(i for i, value in enumerate(residual) if abs(value) == distance)
        normal[index] = _sign(residual[index])
    elif kind == "start":
        index = next(i for i, value in enumerate(residual) if value == distance)
        normal[index] = F(1)
    elif kind == "end":
        index = next(i for i, value in enumerate(residual) if value == -distance)
        normal[index] = F(-1)
    else:
        _require(
            kind == "interior" and residual[0] == -residual[1], "interior opposite-face balance"
        )
        total = sum((abs(value) for value in vector), F(0))
        _require(total > 0, "nonzero interior segment")
        normal = [
            _sign(residual[0]) * abs(vector[1]) / total,
            _sign(residual[1]) * abs(vector[0]) / total,
        ]
    constant = _dot(normal, _subtract(p, segment["start"]))
    slope = -_dot(normal, vector)
    endpoints = [constant, constant + slope]
    norm = sum((abs(value) for value in normal), F(0))
    value = min(endpoints)
    _require(
        norm <= 1
        and value == distance
        and constant + slope * projection["t"] == distance
        and _dot(normal, residual) == distance,
        "global dual lower bound and contact equality",
    )
    return {
        "kind": kind,
        "normal": normal,
        "coefficients": [constant, slope],
        "endpoint_values": endpoints,
        "norm": norm,
        "value": value,
    }


def _distance(fixture, bound, opposite):
    upper, p = bound["upper"], list(fixture["q"])
    segment = _segment(opposite, upper)
    if upper == 0:
        raw, parameter, location = [], F(0), "point"
        kind = "point"
    else:
        denominator = sum(segment["vector"], F(0))
        _require(denominator < 0, "negative balance denominator")
        balance = sum(_subtract(p, segment["start"]), F(0)) / denominator
        raw = [balance]
        parameter = max(F(0), min(F(1), balance))
        location = (
            "before"
            if balance < 0
            else "start"
            if balance == 0
            else "interior"
            if balance < 1
            else "end"
            if balance == 1
            else "after"
        )
        kind = "start" if parameter == 0 else "end" if parameter == 1 else "interior"
    contact = [a + parameter * v for a, v in zip(segment["start"], segment["vector"], strict=True)]
    delta = _density(opposite["eta"], upper, parameter)
    _require(
        contact == _forward(opposite, delta)
        and _parameter(opposite["eta"], upper, delta) == parameter,
        "original forward law attains the retained closest contact",
    )
    residual = _subtract(p, contact)
    projection = {
        "raw": raw,
        "t": parameter,
        "location": location,
        "delta": delta,
        "q": contact,
        "residual": residual,
        "distance": _norm(residual),
    }
    lower = _lower(p, segment, projection, kind)
    return {
        "id": fixture["id"] + "/" + bound["id"],
        "fixture": fixture["id"],
        "bound": bound["id"],
        "in_premise": 0 <= fixture["delta"] <= upper,
        "opposite_eta": opposite["eta"],
        "p": p,
        "segment": segment,
        "projection": projection,
        "lower": lower,
    }


def _class(bound, geometries):
    upper = bound["upper"]
    segments = [_segment(geometries[eta], upper) for eta in (0, 1)]
    ordered = upper < 1
    deltas = [upper if ordered else F(1), F(0)]
    parameters = [_parameter(eta, upper, delta) for eta, delta in enumerate(deltas)]
    points = [_forward(geometries[eta], delta) for eta, delta in enumerate(deltas)]
    for parameter, point, segment in zip(parameters, points, segments, strict=True):
        _require(
            point
            == [
                a + parameter * v for a, v in zip(segment["start"], segment["vector"], strict=True)
            ],
            "class contact belongs to its complete segment",
        )
    residual = _subtract(points[0], points[1])
    distance = _norm(residual)
    closed = 3 * (1 - upper) / (16 * (4 + upper)) if ordered else F(0)
    normal = [F(0), F(1)] if ordered else [F(0), F(0)]
    constant = _dot(normal, _subtract(segments[0]["start"], segments[1]["start"]))
    first = _dot(normal, segments[0]["vector"])
    second = -_dot(normal, segments[1]["vector"])
    corners = [constant, constant + second, constant + first, constant + first + second]
    norm = sum((abs(value) for value in normal), F(0))
    value = min(corners)
    _require(
        distance == closed == value
        and norm <= 1
        and constant + first * parameters[0] + second * parameters[1] == distance
        and _dot(normal, residual) == distance,
        "whole-class corner lower bound and attained closed formula",
    )
    lower = {
        "normal": normal,
        "coefficients": [constant, first, second],
        "corner_values": corners,
        "norm": norm,
        "value": value,
    }
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
        "lower": lower,
    }


def _plan(kind, source, distance, in_premise, quota, step, alpha):
    slack = distance - 2 * step
    score = quota * slack**2
    positive, threshold = slack > 0, score >= 10
    sufficient = positive and threshold
    eligible = in_premise and sufficient
    return {
        "id": kind + "/" + source,
        "kind": kind,
        "source": source,
        "distance": distance,
        "in_premise": in_premise,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "eligible": eligible,
        "status": "out_of_premise"
        if not in_premise
        else "certified"
        if sufficient
        else "not_certified",
        "guarantees": [
            {"correct_singleton_at_least": 1 - alpha, "conditional_wrong_singleton_at_most": alpha}
        ]
        if eligible
        else [],
    }


def _plans(distances, classes, protocol):
    quota, step, alpha = (
        protocol["quota"],
        F(1, protocol["grid_denominator"]),
        _fraction(protocol["alpha"]),
    )
    allocations = [_fraction(pair) for pair in protocol["tail_allocations"]]
    _require(
        sum(allocations, F(0)) == alpha and all(value == F(1, 80) for value in allocations),
        "fixed separation-to-confidence error allocation",
    )
    points = [
        _plan(
            "pointwise",
            row["id"],
            row["projection"]["distance"],
            row["in_premise"],
            quota,
            step,
            alpha,
        )
        for row in distances
    ]
    whole = [
        _plan("class", row["bound"], row["distance"], True, quota, step, alpha) for row in classes
    ]
    return points + whole


def _scale_pairs(compiled, fixtures, raw_fixtures, bounds, distances, classes, regions):
    by_key = {(row[0]["eta"], row[0]["scale"]): row for row in compiled}
    by_fixture = {row["id"]: row for row in fixtures}
    by_distance = {row["id"]: row for row in distances}
    raw_by_id = {row["id"]: row for row in raw_fixtures}
    scaled_geometries = {eta: by_key[(eta, 4)][0] for eta in (0, 1)}
    result = []
    for eta in (0, 1):
        left, right = by_key[(eta, 1)][0], by_key[(eta, 4)][0]
        factor = F(right["scale"], left["scale"])
        actual = right["volumes"] == [factor * x for x in left["volumes"]] and right[
            "mass_coefficients"
        ] == [[factor * x for x in row] for row in left["mass_coefficients"]]
        _require(
            right["derivative_numerators"] == [factor**2 * x for x in left["derivative_numerators"]]
            and right["line"] == left["line"]
            and right["positive_normalizer"] == left["positive_normalizer"]
            and right["decreasing"] == left["decreasing"],
            "scaled derivative and line identities",
        )
        segments_equal = all(
            _segment(left, bound["upper"]) == _segment(right, bound["upper"]) for bound in bounds
        )
        distance_equal = True
        for identifier, fixture in by_fixture.items():
            if fixture["eta"] != eta:
                continue
            scaled = _fixture(raw_by_id[identifier], by_key[(eta, 4)], regions)
            actual = actual and scaled["masses"] == [factor * x for x in fixture["masses"]]
            _require(
                scaled["q"] == fixture["q"]
                and scaled["one_point"] == fixture["one_point"]
                and scaled["target"] == fixture["target"],
                "scaled fixture population and target",
            )
            for bound in bounds:
                transformed = _distance(scaled, bound, scaled_geometries[1 - eta])
                distance_equal = (
                    distance_equal and transformed == by_distance[identifier + "/" + bound["id"]]
                )
        for bound, original in zip(bounds, classes, strict=True):
            distance_equal = distance_equal and _class(bound, scaled_geometries) == original
        target_equal = left["target"] == right["target"]
        _require(
            actual and target_equal and segments_equal and distance_equal,
            "full actual-scale and normalized contact/certificate comparison",
        )
        result.append(
            {
                "worlds": [left["id"], right["id"]],
                "volume_factor": factor,
                "actual_scaling": actual,
                "target_equal": target_equal,
                "segments_equal": segments_equal,
                "distances_equal": distance_equal,
            }
        )
    return result


def _baseline(baseline, plans):
    intervals = [
        {
            "k": row["k"],
            "interval": list(row["interval"]),
            "width": row["interval"][1] - row["interval"][0],
        }
        for row in baseline["intervals"]
    ]
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


def _inside(point, box):
    return all(lower <= value <= upper for value, (lower, upper) in zip(point, box, strict=True))


def _opposite_interval(geometry, box, upper):
    a_q, b_q = geometry["mass_coefficients"][0]
    constraints = []
    for (a, b), (lower, high) in zip(geometry["mass_coefficients"][1:], box, strict=True):
        constraints.extend([(a - lower * a_q, b - lower * b_q), (high * a_q - a, high * b_q - b)])
    left, right = F(0), upper
    for constant, slope in constraints:
        if slope == 0:
            if constant < 0:
                return []
        elif slope > 0:
            left = max(left, -constant / slope)
        else:
            right = min(right, -constant / slope)
    if left > right:
        return []
    interval = [left, right]
    _require(
        all(_inside(_forward(geometry, delta), box) for delta in interval)
        and all(
            constant + slope * delta >= 0 for constant, slope in constraints for delta in interval
        ),
        "same-density box interval has exact closed forward endpoints",
    )
    return interval


def _boxes(protocol, distances, geometries, bounds):
    by_distance = {row["id"]: row for row in distances}
    by_bound = {row["id"]: row for row in bounds}
    result = []
    for identifier in protocol["boxes"]["fixtures"]:
        source = by_distance[identifier + "/" + protocol["boxes"]["bound"]]
        p, contact = source["p"], source["projection"]["q"]
        distance = source["projection"]["distance"]
        _require(
            distance > 0 and source["in_premise"] and source["lower"]["kind"] == "interior",
            "declared positive interior controls",
        )
        for kind in protocol["boxes"]["kinds"]:
            if kind == "contact_rectangle":
                box = [sorted([a, b]) for a, b in zip(p, contact, strict=True)]
            else:
                radius = distance / 2 if kind == "half_square" else distance
                box = [[value - radius, value + radius] for value in p]
            _require(
                all(0 <= lower <= upper <= 1 for lower, upper in box), "derived probability box"
            )
            widths = [upper - lower for lower, upper in box]
            maximum = max(widths)
            half = maximum / 2
            contains_true, contains_contact = _inside(p, box), _inside(contact, box)
            interval = _opposite_interval(
                geometries[source["opposite_eta"]], box, by_bound[source["bound"]]["upper"]
            )
            admits = bool(interval)
            _require(contains_true, "true-centered or contact-hull control retains the true point")
            if kind == "half_square":
                _require(
                    not contains_contact and not admits and maximum == distance,
                    "half-radius square excludes despite full-width equality",
                )
            else:
                _require(
                    contains_contact
                    and admits
                    and interval[0] <= source["projection"]["delta"] <= interval[1],
                    "closed contact is admitted by the coupled interval",
                )
            if kind == "contact_rectangle":
                _require(
                    maximum == distance and half < distance,
                    "contact rectangle refutes half-width and nonstrict-width exclusions",
                )
            result.append(
                {
                    "id": identifier + "/" + kind,
                    "distance_id": source["id"],
                    "kind": kind,
                    "intervals": box,
                    "widths": widths,
                    "max_width": maximum,
                    "half_width": half,
                    "contains_true": contains_true,
                    "contains_contact": contains_contact,
                    "opposite_delta_set": interval,
                    "admits_opposite": admits,
                    "strict_width_condition": maximum < distance,
                    "half_width_condition": half < distance,
                    "nonstrict_width_condition": maximum <= distance,
                }
            )
    return result


def _rational_bound():
    terms = [F(5**j, factorial(j)) for j in range(6)]
    total = sum(terms, F(0))
    strict = total > 80
    _require(
        all(term > 0 for term in terms) and total == F(1097, 12) and strict,
        "finite positive series certifies logarithmic strict slack",
    )
    return {
        "terms": terms,
        "partial_sum": total,
        "threshold": F(80),
        "log_upper": F(5),
        "strict": strict,
    }


def _rational_control(raw):
    quota, denominator = raw["quota"], raw["grid_denominator"]
    radius, distance = _fraction(raw["radius"]), _fraction(raw["distance"])
    step = F(1, denominator)
    square, width = 2 * quota * radius**2, 2 * radius + 2 * step
    slack = distance - 2 * step
    score = quota * slack**2
    radius_test = radius >= 0 and square >= 5 and width <= distance
    direct_test = slack > 0 and score >= 10
    _require(
        radius_test and direct_test and square == 5 and width == distance and score == 10,
        "both rational-equality boundary controls retain strict logarithmic slack",
    )
    return {
        "quota": quota,
        "grid_denominator": denominator,
        "radius": radius,
        "distance": distance,
        "step": step,
        "square_score": square,
        "width": width,
        "main_score": score,
        "radius_test": radius_test,
        "direct_test": direct_test,
        "strict_slack_basis": "ln80_lt_5",
    }


def _obstruction(unit, regions):
    deltas = [F(1), F(0)]
    probabilities, targets, coefficients = [], [], []
    for eta, delta in enumerate(deltas):
        geometry, proper, slope = unit[eta]
        poly = _add(proper, _scale(slope, delta))
        masses = [_integrate(poly, rectangle) for rectangle in regions]
        normalized = _scale(poly, F(1) / masses[0])
        powers = ((0, 0), (1, 1), (2, 2))
        _require(set(normalized) <= set(powers), "complete declared normalized polynomial basis")
        coefficients.append([normalized.get(power, F(0)) for power in powers])
        probabilities.append([masses[index] / masses[0] for index in (1, 2)])
        targets.append(geometry["target"])
    point_equal = coefficients[0] == coefficients[1]
    _require(
        point_equal and probabilities[0] == probabilities[1] and targets[0] != targets[1],
        "whole-point collision with distinct targets",
    )
    return {
        "deltas": deltas,
        "q": probabilities[0],
        "targets": targets,
        "target_gap": targets[0] - targets[1],
        "normalized_polynomials": coefficients,
        "point_equal": point_equal,
    }


def _native_report(value):
    if type(value) in (F, int, bool, str):
        return
    _require(type(value) in (dict, list), "native report container")
    if type(value) is dict:
        _require(
            all(type(key) is str and not key.startswith("$") for key in value),
            "native nonreserved report keys",
        )
    for child in value.values() if type(value) is dict else value:
        _native_report(child)


def analyze(protocol, baseline):
    """Compute only fixed small separation certificates, never a quota-sized law."""
    _validate(protocol, baseline)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "upper": _fraction(row["upper"])} for row in protocol["density_bounds"]
    ]
    compiled = [_geometry(row, regions) for row in protocol["geometries"]]
    geometries = [row[0] for row in compiled]
    unit = {row[0]["eta"]: row for row in compiled if row[0]["scale"] == 1}
    unit_geometries = {eta: row[0] for eta, row in unit.items()}
    fixtures = [_fixture(row, unit[row["eta"]], regions) for row in protocol["fixtures"]]
    distances = [
        _distance(fixture, bound, unit_geometries[1 - fixture["eta"]])
        for fixture in fixtures
        for bound in bounds
    ]
    classes = [_class(bound, unit_geometries) for bound in bounds]
    plans = _plans(distances, classes, protocol)
    scales = _scale_pairs(
        compiled, fixtures, protocol["fixtures"], bounds, distances, classes, regions
    )
    baseline_report = _baseline(baseline, plans)
    boxes = _boxes(protocol, distances, unit_geometries, bounds)
    rational_bound = _rational_bound()
    rational_controls = [_rational_control(protocol["rational_control"])]
    obstruction = _obstruction(unit, regions)
    census = {
        "geometries": len(geometries),
        "fixtures": len(fixtures),
        "distances": len(distances),
        "classes": len(classes),
        "plans": len(plans),
        "scale_pairs": len(scales),
        "baseline_intervals": len(baseline_report["intervals"]),
        "baseline_comparisons": len(baseline_report["comparisons"]),
        "boxes": len(boxes),
        "rational_controls": len(rational_controls),
        "obstructions": 1,
    }
    _require(census == protocol["coverage"], "complete fixed separation and planning inventory")
    report = {
        "schema": "qr05bt-report-v1",
        "geometries": geometries,
        "fixtures": fixtures,
        "distances": distances,
        "classes": classes,
        "plans": plans,
        "scale_pairs": scales,
        "baseline": baseline_report,
        "boxes": boxes,
        "rational_bound": rational_bound,
        "rational_controls": rational_controls,
        "obstruction": obstruction,
    }
    _native_report(report)
    return report
