"""Exact BP monomial masses and closed affine-halfspace clipping.

No mathematical work occurs on import. The explicit analyze(protocol) call
uses no files, historical execution, numerical captures or shared engines.
"""

from fractions import Fraction as F
from itertools import pairwise
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native_input(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (int, str):
        return
    _require(kind in (dict, list), "native protocol types")
    identity = id(value)
    _require(identity not in active, "cyclic protocol")
    if kind is dict:
        _require(all(type(key) is str for key in value), "native protocol keys")
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native_input(child, active)
    finally:
        active.remove(identity)


def _validate(protocol):
    _native_input(protocol)
    expected = {
        "schema": "qr05bp-protocol-v1",
        "quota": 4,
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
            {"id": "uniform", "interval": [[0, 1], [0, 1]]},
            {"id": "half", "interval": [[0, 1], [1, 2]]},
            {"id": "one", "interval": [[0, 1], [1, 1]]},
            {"id": "two", "interval": [[0, 1], [2, 1]]},
        ],
        "points": [
            {"id": "flat_0", "q": [[1, 4], [3, 8]]},
            {"id": "flat_1", "q": [[17, 80], [21, 64]]},
            {"id": "flat_2", "q": [[3, 16], [19, 64]]},
            {"id": "flat_interior", "q": [[1, 5], [5, 16]]},
            {"id": "conformal_0", "q": [[17, 80], [21, 64]]},
            {"id": "conformal_1", "q": [[163, 928], [2079, 7424]]},
            {"id": "conformal_2", "q": [[173, 1136], [567, 2272]]},
            {"id": "conformal_interior", "q": [[1, 5], [2275, 7296]]},
            {"id": "zero", "q": [[0, 1], [0, 1]]},
            {"id": "one", "q": [[1, 1], [1, 1]]},
            {"id": "equal", "q": [[1, 4], [1, 4]]},
            {"id": "zero_constant", "q": [[1, 16], [9, 64]]},
        ],
        "boxes": [
            {"id": "flat_small", "center": "flat_interior", "radius": [1, 65536]},
            {"id": "flat_wide", "center": "flat_interior", "radius": [1, 1024]},
            {"id": "conformal_small", "center": "conformal_interior", "radius": [1, 65536]},
            {"id": "conformal_wide", "center": "conformal_interior", "radius": [1, 1024]},
            {"id": "collision_small", "center": "flat_1", "radius": [1, 65536]},
            {"id": "full", "intervals": [[[0, 1], [1, 1]], [[0, 1], [1, 1]]]},
            {"id": "inconsistent", "intervals": [[[1, 4], [1, 4]], [[19, 64], [21, 64]]]},
            {"id": "touch", "intervals": [[[3, 16], [17, 80]], [[21, 64], [3, 8]]]},
            {"id": "crossing", "intervals": [[[1, 5], [2, 5]], [[3, 10], [1, 2]]]},
            {"id": "non_nested", "intervals": [[[3, 4], [1, 1]], [[0, 1], [1, 4]]]},
            {"id": "pole_band", "intervals": [[[1, 16], [1, 16]], [[0, 1], [1, 1]]]},
        ],
        "box_inclusions": [
            ["flat_interior", "flat_small"],
            ["flat_small", "flat_wide"],
            ["flat_wide", "full"],
            ["conformal_interior", "conformal_small"],
            ["conformal_small", "conformal_wide"],
            ["conformal_wide", "full"],
            ["flat_1", "collision_small"],
            ["collision_small", "full"],
            ["flat_1", "touch"],
            ["touch", "full"],
            ["inconsistent", "full"],
            ["crossing", "full"],
        ],
        "observer": {
            "schema": "qr05bp-query-v1",
            "data_kind": "population_intervals",
            "bound_basis": "external_assumption",
            "uncertainty_basis": "external_population_bounds",
            "integer_cap": 2147483647,
        },
        "coverage": {
            "geometries": 4,
            "data": 23,
            "cases": 92,
            "hypotheses": 368,
            "density_monotonicity": 69,
            "box_monotonicity": 48,
            "scale_pairs": 2,
            "obstruction_cases": 92,
            "point_recovery": 48,
        },
        "limits": {
            "source_bytes": 262144,
            "artifact_bytes": 16777216,
            "analysis_seconds": 30,
            "suite_seconds": 120,
            "alternate_reference_runs": 1,
        },
    }
    _require(type(protocol) is dict and protocol == expected, "complete fixed BP protocol")


def _fraction(pair):
    _require(
        type(pair) is list and len(pair) == 2 and all(type(value) is int for value in pair),
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


def _affine(coefficients, delta):
    return coefficients[0] + coefficients[1] * delta


def _subtract(left, right):
    return [a - b for a, b in zip(left, right, strict=True)]


def _forward(geometry, delta):
    masses = [_affine(row, delta) for row in geometry["mass_coefficients"]]
    _require(0 < masses[1] < masses[2] < masses[0], "positive nested category masses")
    return [masses[index] / masses[0] for index in (1, 2)]


def _geometry(supplied, regions):
    eta, scale = F(supplied["eta"]), F(supplied["scale"])
    proper = _clean({(0, 0): scale / 2, (1, 1): scale * eta / 2})
    slope = _multiply(proper, {(1, 1): F(1)})
    volumes = [_integrate(proper, rectangle) for rectangle in regions]
    coefficients = [
        [_integrate(poly, rectangle) for poly in (proper, slope)] for rectangle in regions
    ]
    category = [
        _subtract(coefficients[0], coefficients[2]),
        _subtract(coefficients[2], coefficients[1]),
        list(coefficients[1]),
    ]
    # These affine masses are positive on the whole delta >= 0 domain: each
    # intercept is positive and each slope nonnegative. No fixture extrapolation.
    strict_support = all(a > 0 and b >= 0 for a, b in category)
    _require(strict_support, "continuous three-category support certificate")
    a_q, b_q = coefficients[0]
    _require(a_q > 0 and b_q >= 0, "positive common normalizer on the density domain")
    derivatives = [b * a_q - a * b_q for a, b in coefficients[1:]]
    _require(all(value < 0 for value in derivatives), "both probability ratios strictly decrease")
    result = {
        "id": supplied["id"],
        "eta": supplied["eta"],
        "scale": supplied["scale"],
        "volumes": volumes,
        "target": volumes[1] / volumes[0],
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "full_q_ranges": [],
        "category_coefficients": category,
        "strict_support": strict_support,
    }
    left, right = _forward(result, F(0)), _forward(result, F(2))
    result["full_q_ranges"] = [[right[i], left[i]] for i in range(2)]
    return result, proper, slope


def _datum(identifier, intervals):
    _require(
        len(intervals) == 2
        and all(len(row) == 2 and 0 <= row[0] <= row[1] <= 1 for row in intervals),
        "well-shaped coordinate probability intervals",
    )
    return {
        "id": identifier,
        "intervals": [list(row) for row in intervals],
        "nested_nonempty": intervals[0][0] <= intervals[1][1],
    }


def _data(protocol):
    points = {row["id"]: [_fraction(pair) for pair in row["q"]] for row in protocol["points"]}
    result = [
        _datum(row["id"], [[value, value] for value in points[row["id"]]])
        for row in protocol["points"]
    ]
    for box in protocol["boxes"]:
        if "center" in box:
            radius = _fraction(box["radius"])
            _require(radius >= 0, "nonnegative stipulated radius")
            intervals = [[value - radius, value + radius] for value in points[box["center"]]]
        else:
            intervals = [[_fraction(pair) for pair in row] for row in box["intervals"]]
        result.append(_datum(box["id"], intervals))
    _require(
        len({row["id"] for row in result}) == len(result), "distinct supplied data identifiers"
    )
    return result


def _inequality(constant, slope):
    _require(type(constant) is F and type(slope) is F, "exact affine halfspace")
    if slope == 0:
        kind = "all" if constant >= 0 else "none"
        boundary = []
    else:
        kind = "lower" if slope > 0 else "upper"
        boundary = [-constant / slope]
    return {"constant": constant, "slope": slope, "kind": kind, "boundary": boundary}


def _clip(interval, inequality):
    if not interval or inequality["kind"] == "none":
        return []
    lower, upper = interval
    if inequality["kind"] == "lower":
        lower = max(lower, inequality["boundary"][0])
    elif inequality["kind"] == "upper":
        upper = min(upper, inequality["boundary"][0])
    else:
        _require(inequality["kind"] == "all", "known halfspace class")
    return [lower, upper] if lower <= upper else []


def _intersect(left, right):
    if not left or not right:
        return []
    lower, upper = max(left[0], right[0]), min(left[1], right[1])
    return [lower, upper] if lower <= upper else []


def _contains(interval, value):
    return bool(interval) and interval[0] <= value <= interval[1]


def _subset(left, right):
    return not left or bool(right) and right[0] <= left[0] <= left[1] <= right[1]


def _curve(geometry, interval, datum):
    endpoints = []
    coefficients = geometry["mass_coefficients"]
    one_point_numerators = [
        list(geometry["category_coefficients"][0]),
        list(geometry["category_coefficients"][1]),
        [F(0), F(0)],
        list(geometry["category_coefficients"][2]),
    ]
    for delta in interval:
        q = _forward(geometry, delta)
        denominator = _affine(coefficients[0], delta)
        one_point = [_affine(row, delta) / denominator for row in one_point_numerators]
        _require(one_point == [1 - q[1], q[1] - q[0], F(0), q[0]], "same-delta paired law")
        _require(sum(one_point, F(0)) == 1, "paired law normalization")
        _require(
            all(
                lower <= value <= upper
                for value, (lower, upper) in zip(q, datum["intervals"], strict=True)
            ),
            "paired endpoint lies in the supplied box",
        )
        endpoints.append({"delta": delta, "q": q, "one_point": one_point})
    _require(len(endpoints) == 2, "retain both endpoint rows even for a singleton")
    return {
        "domain": list(interval),
        "numerators": [list(row) for row in coefficients[1:]],
        "denominator": list(coefficients[0]),
        "one_point_numerators": one_point_numerators,
        "endpoints": endpoints,
        "q_ranges": [sorted([endpoints[0]["q"][i], endpoints[1]["q"][i]]) for i in range(2)],
    }


def _hypothesis(geometry, datum, bound):
    a_q, b_q = geometry["mass_coefficients"][0]
    inequalities = []
    for (a, b), (lower, upper) in zip(
        geometry["mass_coefficients"][1:], datum["intervals"], strict=True
    ):
        inequalities.append(_inequality(a - lower * a_q, b - lower * b_q))
        inequalities.append(_inequality(upper * a_q - a, upper * b_q - b))
    query_sets = []
    for offset in (0, 2):
        interval = list(bound)
        for row in inequalities[offset : offset + 2]:
            interval = _clip(interval, row)
        query_sets.append(interval)
    joint = _intersect(query_sets[0], query_sets[1])
    direct = list(bound)
    for row in inequalities:
        direct = _clip(direct, row)
    _require(joint == direct, "two-query intersection equals complete halfspace conjunction")
    if joint:
        _require(
            all(
                row["constant"] + row["slope"] * delta >= 0
                for row in inequalities
                for delta in joint
            ),
            "every closed endpoint satisfies all original inequalities",
        )
        _require(datum["nested_nonempty"], "admitted curve must meet the nested cone")
    return {
        "id": geometry["id"],
        "inequalities": inequalities,
        "query_sets": query_sets,
        "delta_set": joint,
        "status": "feasible" if joint else "infeasible",
        "curve": _curve(geometry, joint, datum) if joint else {},
    }


def _case(bound, datum, geometries):
    hypotheses = [_hypothesis(geometry, datum, bound["interval"]) for geometry in geometries]
    by_id = {geometry["id"]: geometry for geometry in geometries}
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({by_id[name]["target"] for name in worlds})
    return {
        "id": bound["id"] + "/" + datum["id"],
        "bound": bound["id"],
        "data": datum["id"],
        "intervals": [list(row) for row in datum["intervals"]],
        "nested_nonempty": datum["nested_nonempty"],
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": "infeasible"
        if not worlds
        else "identified"
        if len(targets) == 1
        else "ambiguous",
    }


def _inclusion(left, right):
    world_subset = set(left["worlds"]) <= set(right["worlds"])
    target_subset = set(left["targets"]) <= set(right["targets"])
    right_sets = {row["id"]: row["delta_set"] for row in right["hypotheses"]}
    nuisance_subset = all(
        _subset(row["delta_set"], right_sets[row["id"]]) for row in left["hypotheses"]
    )
    _require(
        world_subset and target_subset and nuisance_subset, "full labeled feasible-set inclusion"
    )
    return {
        "world_subset": world_subset,
        "target_subset": target_subset,
        "nuisance_subset": nuisance_subset,
    }


def _monotonicity(bounds, data, cases, inclusions):
    by_case = {row["id"]: row for row in cases}
    by_data = {row["id"]: row for row in data}
    density = []
    for tight, broad in pairwise(bounds):
        _require(_subset(tight["interval"], broad["interval"]), "nested density assumptions")
        for datum in data:
            left = by_case[tight["id"] + "/" + datum["id"]]
            right = by_case[broad["id"] + "/" + datum["id"]]
            density.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    **_inclusion(left, right),
                }
            )
    boxes = []
    for tight, broad in inclusions:
        _require(
            all(
                _subset(a, b)
                for a, b in zip(
                    by_data[tight]["intervals"], by_data[broad]["intervals"], strict=True
                )
            ),
            "declared box inclusion is coordinatewise valid",
        )
        for bound in bounds:
            left = by_case[bound["id"] + "/" + tight]
            right = by_case[bound["id"] + "/" + broad]
            boxes.append(
                {"tight": tight, "broad": broad, "bound": bound["id"], **_inclusion(left, right)}
            )
    return density, boxes


def _normalized_curve(curve):
    if not curve:
        return {}
    constant = curve["denominator"][0]
    _require(constant > 0, "positive coefficient gauge")
    return {
        "domain": list(curve["domain"]),
        "numerators": [[value / constant for value in row] for row in curve["numerators"]],
        "denominator": [value / constant for value in curve["denominator"]],
        "one_point_numerators": [
            [value / constant for value in row] for row in curve["one_point_numerators"]
        ],
        "endpoints": curve["endpoints"],
        "q_ranges": curve["q_ranges"],
    }


def _scale_pairs(geometries, cases):
    by_id = {row["id"]: row for row in geometries}
    result = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        left, right = by_id[first], by_id[second]
        factor = right["volumes"][0] / left["volumes"][0]
        _require(factor == F(right["scale"], left["scale"]), "metric scale versus volume factor")
        _require(
            right["volumes"] == [factor * value for value in left["volumes"]]
            and right["mass_coefficients"]
            == [[factor * value for value in row] for row in left["mass_coefficients"]]
            and right["category_coefficients"]
            == [[factor * value for value in row] for row in left["category_coefficients"]]
            and right["derivative_numerators"]
            == [factor**2 * value for value in left["derivative_numerators"]]
            and left["full_q_ranges"] == right["full_q_ranges"],
            "full region and affine coefficient scaling",
        )
        target_equal = left["target"] == right["target"]
        nuisance_equal = True
        curve_equal = True
        for case in cases:
            by_hypothesis = {row["id"]: row for row in case["hypotheses"]}
            a, b = by_hypothesis[first], by_hypothesis[second]
            nuisance_equal = nuisance_equal and a["delta_set"] == b["delta_set"]
            curve_equal = curve_equal and _normalized_curve(a["curve"]) == _normalized_curve(
                b["curve"]
            )
            _require(
                a["query_sets"] == b["query_sets"] and a["status"] == b["status"],
                "scale-invariant component feasibility",
            )
            for x, y in zip(a["inequalities"], b["inequalities"], strict=True):
                _require(
                    y["constant"] == factor * x["constant"]
                    and y["slope"] == factor * x["slope"]
                    and x["kind"] == y["kind"]
                    and x["boundary"] == y["boundary"],
                    "raw inequality scaling preserves exact boundaries",
                )
            if a["curve"]:
                for field in ("numerators", "one_point_numerators"):
                    _require(
                        b["curve"][field]
                        == [[factor * value for value in row] for row in a["curve"][field]],
                        "raw curve numerator scaling",
                    )
                _require(
                    b["curve"]["denominator"]
                    == [factor * value for value in a["curve"]["denominator"]],
                    "raw curve denominator scaling",
                )
        _require(target_equal and nuisance_equal and curve_equal, "all-case scale ambiguity")
        result.append(
            {
                "worlds": [first, second],
                "volume_factor": factor,
                "target_equal": target_equal,
                "nuisance_sets_equal": nuisance_equal,
                "curve_laws_equal": curve_equal,
            }
        )
    return result


def _obstruction(compiled, regions, data, bounds, cases):
    by_id = {row[0]["id"]: row for row in compiled}
    names, deltas = ["flat", "conformal"], [F(1), F(0)]
    polynomials, probabilities = [], []
    for name, delta in zip(names, deltas, strict=True):
        geometry, proper, slope = by_id[name]
        weighted = _add(proper, _scale(slope, delta))
        masses = [_integrate(weighted, rectangle) for rectangle in regions]
        _require(
            masses == [_affine(row, delta) for row in geometry["mass_coefficients"]],
            "obstruction monomial masses",
        )
        polynomials.append(_scale(weighted, F(1) / masses[0]))
        probabilities.append([masses[i] / masses[0] for i in (1, 2)])
    point_equal = polynomials[0] == polynomials[1]
    _require(
        point_equal and probabilities[0] == probabilities[1], "whole-point density compensation"
    )
    gap = by_id[names[0]][0]["target"] - by_id[names[1]][0]["target"]
    _require(gap != 0, "distinct geometric targets under whole-point equality")
    by_data = {row["id"]: row for row in data}
    by_bound = {row["id"]: row["interval"] for row in bounds}
    rows = []
    for case in cases:
        hypotheses = {row["id"]: row for row in case["hypotheses"]}
        present = [
            _contains(hypotheses[name]["delta_set"], delta)
            for name, delta in zip(names, deltas, strict=True)
        ]
        datum = by_data[case["data"]]
        pair_fits = all(
            _contains(interval, value)
            for interval, value in zip(datum["intervals"], probabilities[0], strict=True)
        )
        _require(
            present
            == [pair_fits and _contains(by_bound[case["bound"]], delta) for delta in deltas],
            "obstruction indicators agree with direct box and density membership",
        )
        both = all(present)
        ambiguous = case["status"] == "ambiguous"
        _require(not both or ambiguous, "both obstruction parameters imply target ambiguity")
        rows.append(
            {
                "case": case["id"],
                "flat_present": present[0],
                "conformal_present": present[1],
                "both": both,
                "target_ambiguous": ambiguous,
            }
        )
    return {
        "worlds": list(names),
        "deltas": list(deltas),
        "q": list(probabilities[0]),
        "point_equal": point_equal,
        "target_gap": gap,
        "cases": rows,
    }


def _support(geometries, bounds, quota):
    certificate = all(row["strict_support"] for row in geometries) and all(
        0 <= row["interval"][0] <= row["interval"][1] <= 2 for row in bounds
    )
    _require(certificate, "continuous support certificate and acquisition domain")
    symbols = [[0, 0], [0, 1], [1, 0], [1, 1]]
    allowed = [[0, 0], [0, 1], [1, 1]]
    possible = len(allowed) ** quota
    return {
        "quota": quota,
        "symbols": symbols,
        "allowed": allowed,
        "possible_words": possible,
        "zero_words": len(symbols) ** quota - possible,
        "continuous_certificate": certificate,
    }


def _native_report(value):
    if type(value) in (F, int, bool, str):
        return
    _require(type(value) in (dict, list), "unsupported native report type")
    if type(value) is dict:
        _require(all(type(key) is str for key in value), "native report keys")
    for child in value.values() if type(value) is dict else value:
        _native_report(child)


def analyze(protocol):
    """Compute only the declared interval report; prior point checks belong to the driver."""
    _validate(protocol)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    compiled = [_geometry(row, regions) for row in protocol["geometries"]]
    geometries = [row[0] for row in compiled]
    data = _data(protocol)
    cases = [_case(bound, datum, geometries) for bound in bounds for datum in data]
    density, boxes = _monotonicity(bounds, data, cases, protocol["box_inclusions"])
    scales = _scale_pairs(geometries, cases)
    obstruction = _obstruction(compiled, regions, data, bounds, cases)
    support = _support(geometries, bounds, protocol["quota"])
    point_ids = {row["id"] for row in protocol["points"]}
    coverage = {
        "geometries": len(geometries),
        "data": len(data),
        "cases": len(cases),
        "hypotheses": sum(len(row["hypotheses"]) for row in cases),
        "density_monotonicity": len(density),
        "box_monotonicity": len(boxes),
        "scale_pairs": len(scales),
        "obstruction_cases": len(obstruction["cases"]),
        "point_recovery": sum(row["data"] in point_ids for row in cases),
    }
    _require(coverage == protocol["coverage"], "complete fixed interval-domain census")
    report = {
        "schema": "qr05bp-report-v1",
        "geometries": geometries,
        "data": data,
        "cases": cases,
        "density_monotonicity": density,
        "box_monotonicity": boxes,
        "scale_pairs": scales,
        "obstruction": obstruction,
        "support": support,
    }
    _native_report(report)
    return report
