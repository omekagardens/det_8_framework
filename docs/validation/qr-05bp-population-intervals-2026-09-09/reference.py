"""Independent BP quadrature and attained-range-first continuous inverse.

Importing this module performs no fixed mathematical evaluation. The module
has no file access, historical executor imports or shared mathematical code.
"""

from fractions import Fraction
from itertools import pairwise


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _validate_protocol(protocol):
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
    pending = [(protocol, expected)]
    while pending:
        actual, wanted = pending.pop()
        _require(type(actual) is type(wanted), "fixed protocol native type")
        if type(wanted) is dict:
            _require(
                all(type(key) is str for key in actual) and set(actual) == set(wanted),
                "fixed protocol fields",
            )
            pending.extend((actual[key], value) for key, value in wanted.items())
        elif type(wanted) is list:
            _require(len(actual) == len(wanted), "fixed protocol list length")
            pending.extend(zip(actual, wanted))
        else:
            _require(actual == wanted, "fixed protocol value")


def _fraction(pair):
    return Fraction(pair[0], pair[1])


def _axis(lower, upper):
    _require(
        type(lower) is Fraction and type(upper) is Fraction and lower < upper, "positive interval"
    )
    return ((lower, 1), ((lower + upper) / 2, 4), (upper, 1))


def _integrate(function, rectangle):
    left, right, bottom, top = rectangle
    total = Fraction(0)
    for u, wu in _axis(left, right):
        for v, wv in _axis(bottom, top):
            value = function(u, v)
            _require(type(value) is Fraction, "exact integrand")
            total += wu * wv * value
    return total * (right - left) * (top - bottom) / 36


def _proper(geometry, u, v):
    return Fraction(geometry["scale"], 2) * (1 + geometry["eta"] * u * v)


def _weighted(geometry, delta, u, v):
    return _proper(geometry, u, v) * (1 + delta * u * v)


def _mass(geometry, delta, regions):
    return [
        _integrate(lambda u, v: _weighted(geometry, delta, u, v), rectangle)
        for rectangle in regions
    ]


def _value(coefficients, delta):
    return coefficients[0] + coefficients[1] * delta


def _ratio(numerator, denominator, delta):
    bottom = _value(denominator, delta)
    _require(bottom > 0, "positive ratio denominator")
    return _value(numerator, delta) / bottom


def _interval(interval, allow_empty=False):
    _require(type(interval) is list, "native interval list")
    if allow_empty and not interval:
        return
    _require(
        len(interval) == 2
        and all(type(value) is Fraction for value in interval)
        and interval[0] <= interval[1],
        "closed rational interval",
    )


def _intersection(left, right):
    _interval(left, True)
    _interval(right, True)
    if not left or not right:
        return []
    lower, upper = max(left[0], right[0]), min(left[1], right[1])
    return [lower, upper] if lower <= upper else []


def _subset(left, right):
    if not left:
        return True
    return bool(right) and right[0] <= left[0] <= left[1] <= right[1]


def _contains(interval, value):
    return bool(interval) and interval[0] <= value <= interval[1]


def _range_inverse(numerator, denominator, probability_interval, density_interval):
    """Invert only the intersection with the ratio's attained closed range."""
    for coefficients in (numerator, denominator):
        _require(
            type(coefficients) is list
            and len(coefficients) == 2
            and all(type(value) is Fraction for value in coefficients),
            "affine rational coefficient pair",
        )
    _interval(probability_interval)
    _interval(density_interval)
    images = [_ratio(numerator, denominator, delta) for delta in density_interval]
    reachable = _intersection(probability_interval, [min(images), max(images)])
    if not reachable:
        return []
    a, b = numerator
    c, d = denominator
    derivative = b * c - a * d
    if derivative == 0:
        _require(images[0] == images[1], "constant ratio")
        return list(density_interval)
    recovered = []
    for q in reachable:
        divisor = d * q - b
        _require(divisor != 0, "a reachable nonconstant ratio cannot be an inverse pole")
        delta = (a - c * q) / divisor
        _require(
            _contains(density_interval, delta) and _ratio(numerator, denominator, delta) == q,
            "reachable endpoint inverse and forward certificate",
        )
        recovered.append(delta)
    result = recovered if derivative > 0 else list(reversed(recovered))
    _interval(result)
    return result


def _geometry(raw, regions):
    volumes = [_integrate(lambda u, v: _proper(raw, u, v), rectangle) for rectangle in regions]
    zero, one = _mass(raw, Fraction(0), regions), _mass(raw, Fraction(1), regions)
    coefficients = [[a, b - a] for a, b in zip(zero, one)]
    denominator, first, second = coefficients
    categories = [
        [a - b for a, b in zip(denominator, second)],
        [a - b for a, b in zip(second, first)],
        list(first),
    ]
    strict_support = True
    for delta in (Fraction(0), Fraction(2)):
        direct = _mass(raw, delta, regions)
        _require(direct == [_value(row, delta) for row in coefficients], "direct affine masses")
        _require(direct[0] > 0, "continuous normalization denominator")
        strict_support = strict_support and all(_value(row, delta) > 0 for row in categories)
    # Category masses are affine in delta, so endpoint positivity proves
    # positivity on the whole domain, not only at the selected cases.
    _require(strict_support, "strict continuous category support")
    derivatives = [row[1] * denominator[0] - row[0] * denominator[1] for row in (first, second)]
    full_ranges = [
        sorted(_ratio(row, denominator, delta) for delta in (Fraction(0), Fraction(2)))
        for row in (first, second)
    ]
    return {
        "id": raw["id"],
        "eta": raw["eta"],
        "scale": raw["scale"],
        "volumes": volumes,
        "target": volumes[1] / volumes[0],
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "full_q_ranges": full_ranges,
        "category_coefficients": categories,
        "strict_support": strict_support,
    }


def _data(protocol):
    points = {row["id"]: [_fraction(pair) for pair in row["q"]] for row in protocol["points"]}
    result = []
    for row in protocol["points"]:
        result.append(
            {"id": row["id"], "intervals": [[value, value] for value in points[row["id"]]]}
        )
    for row in protocol["boxes"]:
        if "center" in row:
            radius = _fraction(row["radius"])
            intervals = [[value - radius, value + radius] for value in points[row["center"]]]
        else:
            intervals = [[_fraction(pair) for pair in interval] for interval in row["intervals"]]
        result.append({"id": row["id"], "intervals": intervals})
    for datum in result:
        for interval in datum["intervals"]:
            _interval(interval)
            _require(0 <= interval[0] <= interval[1] <= 1, "supplied probability box")
        datum["nested_nonempty"] = datum["intervals"][0][0] <= datum["intervals"][1][1]
    return result


def _inequality(constant, slope):
    if slope == 0:
        kind, boundary = ("all" if constant >= 0 else "none"), []
    else:
        kind, boundary = ("lower" if slope > 0 else "upper"), [-constant / slope]
    return {"constant": constant, "slope": slope, "kind": kind, "boundary": boundary}


def _diagnostics(numerator, denominator, probability_interval):
    lower, upper = probability_interval
    return [
        _inequality(numerator[0] - lower * denominator[0], numerator[1] - lower * denominator[1]),
        _inequality(upper * denominator[0] - numerator[0], upper * denominator[1] - numerator[1]),
    ]


def _one_point(q):
    first, second = q
    _require(0 <= first <= second <= 1, "nested forward probabilities")
    result = [1 - second, second - first, Fraction(0), first]
    _require(sum(result, Fraction(0)) == 1, "same-point law normalization")
    return result


def _curve(geometry, interval, probability_box, regions):
    denominator, first, second = geometry["mass_coefficients"]
    categories = geometry["category_coefficients"]
    law_rows = [
        list(categories[0]),
        list(categories[1]),
        [Fraction(0), Fraction(0)],
        list(categories[2]),
    ]
    endpoints = []
    for delta in interval:
        mass = _mass(geometry, delta, regions)
        _require(
            mass == [_value(row, delta) for row in geometry["mass_coefficients"]],
            "endpoint direct masses",
        )
        q = [mass[1] / mass[0], mass[2] / mass[0]]
        _require(
            all(_contains(bounds, value) for bounds, value in zip(probability_box, q)),
            "same-delta endpoint box membership",
        )
        one_point = _one_point(q)
        _require(
            one_point == [_value(row, delta) / mass[0] for row in law_rows],
            "direct endpoint coupled law",
        )
        endpoints.append({"delta": delta, "q": q, "one_point": one_point})
    return {
        "domain": list(interval),
        "numerators": [list(first), list(second)],
        "denominator": list(denominator),
        "one_point_numerators": law_rows,
        "endpoints": endpoints,
        "q_ranges": [sorted(row["q"][i] for row in endpoints) for i in range(2)],
    }


def _hypothesis(geometry, datum, bound, regions):
    denominator, *numerators = geometry["mass_coefficients"]
    # These independently computed inverses, not the halfspace diagnostics,
    # determine the admitted continuous set.
    query_sets = [
        _range_inverse(numerator, denominator, probability_interval, bound["interval"])
        for numerator, probability_interval in zip(numerators, datum["intervals"])
    ]
    delta_set = _intersection(query_sets[0], query_sets[1])
    inequalities = []
    for numerator, probability_interval, query_set in zip(
        numerators, datum["intervals"], query_sets
    ):
        rows = _diagnostics(numerator, denominator, probability_interval)
        for delta in query_set:
            _require(
                all(row["constant"] + row["slope"] * delta >= 0 for row in rows),
                "diagnostic endpoint agreement",
            )
        inequalities.extend(rows)
    if delta_set:
        _require(datum["nested_nonempty"], "coupled model cannot fit an empty nested cone")
    return {
        "id": geometry["id"],
        "inequalities": inequalities,
        "query_sets": query_sets,
        "delta_set": delta_set,
        "status": "feasible" if delta_set else "infeasible",
        "curve": _curve(geometry, delta_set, datum["intervals"], regions) if delta_set else {},
    }


def _case(bound, datum, geometries, regions):
    hypotheses = [_hypothesis(geometry, datum, bound, regions) for geometry in geometries]
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({geometry["target"] for geometry in geometries if geometry["id"] in worlds})
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
        if not targets
        else "identified"
        if len(targets) == 1
        else "ambiguous",
    }


def _inclusion(tight, broad):
    worlds = set(tight["worlds"]) <= set(broad["worlds"])
    targets = set(tight["targets"]) <= set(broad["targets"])
    broader = {row["id"]: row["delta_set"] for row in broad["hypotheses"]}
    nuisance = all(_subset(row["delta_set"], broader[row["id"]]) for row in tight["hypotheses"])
    _require(worlds and targets and nuisance, "complete labeled set inclusion")
    return {"world_subset": worlds, "target_subset": targets, "nuisance_subset": nuisance}


def _density_monotonicity(bounds, data, cases):
    index = {case["id"]: case for case in cases}
    result = []
    for tight, broad in pairwise(bounds):
        _require(_subset(tight["interval"], broad["interval"]), "nested density bounds")
        for datum in data:
            result.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    **_inclusion(
                        index[tight["id"] + "/" + datum["id"]],
                        index[broad["id"] + "/" + datum["id"]],
                    ),
                }
            )
    return result


def _box_monotonicity(inclusions, bounds, data, cases):
    index = {case["id"]: case for case in cases}
    boxes = {datum["id"]: datum["intervals"] for datum in data}
    result = []
    for tight, broad in inclusions:
        _require(
            all(_subset(a, b) for a, b in zip(boxes[tight], boxes[broad])), "declared box inclusion"
        )
        for bound in bounds:
            result.append(
                {
                    "tight": tight,
                    "broad": broad,
                    "bound": bound["id"],
                    **_inclusion(
                        index[bound["id"] + "/" + tight], index[bound["id"] + "/" + broad]
                    ),
                }
            )
    return result


def _scaled_rows(left, right, factor):
    return right == [[factor * value for value in row] for row in left]


def _scale_pairs(geometries, cases):
    index = {geometry["id"]: geometry for geometry in geometries}
    result = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        left, right = index[first], index[second]
        factor = Fraction(right["scale"], left["scale"])
        _require(
            right["volumes"] == [factor * value for value in left["volumes"]],
            "all region volumes scale",
        )
        _require(
            _scaled_rows(left["mass_coefficients"], right["mass_coefficients"], factor),
            "mass coefficients scale",
        )
        _require(
            _scaled_rows(left["category_coefficients"], right["category_coefficients"], factor),
            "category coefficients scale",
        )
        target_equal = left["target"] == right["target"]
        nuisance_equal, laws_equal = True, True
        for case in cases:
            hypotheses = {row["id"]: row for row in case["hypotheses"]}
            a, b = hypotheses[first], hypotheses[second]
            nuisance_equal = (
                nuisance_equal
                and a["delta_set"] == b["delta_set"]
                and a["query_sets"] == b["query_sets"]
            )
            if not a["delta_set"] or not b["delta_set"]:
                laws_equal = laws_equal and a["curve"] == b["curve"] == {}
                continue
            ac, bc = a["curve"], b["curve"]
            laws_equal = (
                laws_equal
                and ac["domain"] == bc["domain"]
                and ac["endpoints"] == bc["endpoints"]
                and ac["q_ranges"] == bc["q_ranges"]
            )
            laws_equal = laws_equal and _scaled_rows(ac["numerators"], bc["numerators"], factor)
            laws_equal = laws_equal and bc["denominator"] == [
                factor * value for value in ac["denominator"]
            ]
            laws_equal = laws_equal and _scaled_rows(
                ac["one_point_numerators"], bc["one_point_numerators"], factor
            )
        _require(target_equal and nuisance_equal and laws_equal, "complete scale obstruction")
        result.append(
            {
                "worlds": [first, second],
                "volume_factor": factor,
                "target_equal": target_equal,
                "nuisance_sets_equal": nuisance_equal,
                "curve_laws_equal": laws_equal,
            }
        )
    return result


def _obstruction(geometries, regions, cases):
    index = {geometry["id"]: geometry for geometry in geometries}
    left, right = index["flat"], index["conformal"]
    left_delta, right_delta = Fraction(1), Fraction(0)
    left_mass, right_mass = _mass(left, left_delta, regions), _mass(right, right_delta, regions)
    q = [left_mass[1] / left_mass[0], left_mass[2] / left_mass[0]]
    _require(
        q == [right_mass[1] / right_mass[0], right_mass[2] / right_mass[0]],
        "same paired collision probabilities",
    )
    # Both specified normalized point densities are at most biquadratic.
    # Equality on this complete tensor interpolation grid proves equality
    # as polynomials, rather than inferring it from the two probabilities.
    point_equal = all(
        _weighted(left, left_delta, u, v) / left_mass[0]
        == _weighted(right, right_delta, u, v) / right_mass[0]
        for u, _ in _axis(regions[0][0], regions[0][1])
        for v, _ in _axis(regions[0][2], regions[0][3])
    )
    _require(point_equal, "whole-point compensation persists")
    rows = []
    for case in cases:
        hypotheses = {row["id"]: row for row in case["hypotheses"]}
        flat = _contains(hypotheses["flat"]["delta_set"], left_delta)
        conformal = _contains(hypotheses["conformal"]["delta_set"], right_delta)
        both, ambiguous = flat and conformal, case["status"] == "ambiguous"
        _require(not both or ambiguous, "admitted collision implies target ambiguity")
        rows.append(
            {
                "case": case["id"],
                "flat_present": flat,
                "conformal_present": conformal,
                "both": both,
                "target_ambiguous": ambiguous,
            }
        )
    return {
        "worlds": ["flat", "conformal"],
        "deltas": [left_delta, right_delta],
        "q": q,
        "point_equal": point_equal,
        "target_gap": left["target"] - right["target"],
        "cases": rows,
    }


def _support(geometries, quota):
    certificate = all(geometry["strict_support"] for geometry in geometries)
    _require(certificate, "continuous whole-family support certificate")
    allowed = [[0, 0], [0, 1], [1, 1]]
    symbols = [[0, 0], [0, 1], [1, 0], [1, 1]]
    possible = len(allowed) ** quota
    return {
        "quota": quota,
        "symbols": symbols,
        "allowed": allowed,
        "possible_words": possible,
        "zero_words": len(symbols) ** quota - possible,
        "continuous_certificate": certificate,
    }


def _native_report(report):
    pending = [report]
    while pending:
        value = pending.pop()
        if type(value) is dict:
            _require(all(type(key) is str for key in value), "native report keys")
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
        else:
            _require(type(value) in (Fraction, int, bool, str), "native report scalar")


def analyze(protocol: dict) -> dict:
    _validate_protocol(protocol)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    geometries = [_geometry(row, regions) for row in protocol["geometries"]]
    data = _data(protocol)
    cases = [_case(bound, datum, geometries, regions) for bound in bounds for datum in data]
    density_monotonicity = _density_monotonicity(bounds, data, cases)
    box_monotonicity = _box_monotonicity(protocol["box_inclusions"], bounds, data, cases)
    scale_pairs = _scale_pairs(geometries, cases)
    obstruction = _obstruction(geometries, regions, cases)
    support = _support(geometries, protocol["quota"])
    point_ids = {row["id"] for row in protocol["points"]}
    # This counts the new point projections only. Historical agreement is
    # checked by the driver against separately pinned bytes, never here.
    coverage = {
        "geometries": len(geometries),
        "data": len(data),
        "cases": len(cases),
        "hypotheses": sum(len(case["hypotheses"]) for case in cases),
        "density_monotonicity": len(density_monotonicity),
        "box_monotonicity": len(box_monotonicity),
        "scale_pairs": len(scale_pairs),
        "obstruction_cases": len(obstruction["cases"]),
        "point_recovery": sum(case["data"] in point_ids for case in cases),
    }
    _require(coverage == protocol["coverage"], "fixed report coverage")
    report = {
        "schema": "qr05bp-report-v1",
        "geometries": geometries,
        "data": data,
        "cases": cases,
        "density_monotonicity": density_monotonicity,
        "box_monotonicity": box_monotonicity,
        "scale_pairs": scale_pairs,
        "obstruction": obstruction,
        "support": support,
    }
    _native_report(report)
    return report
