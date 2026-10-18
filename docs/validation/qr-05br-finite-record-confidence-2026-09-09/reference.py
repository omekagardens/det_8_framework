"""Independent BR convolution, quadrature and count-space confidence route.

Only definitions occur on import. No file access, prior engine imports or
fixed mathematical evaluation is performed before analyze is called.
"""

from fractions import Fraction
from itertools import pairwise


def _validate_protocol(protocol):
    expected = {
        "schema": "qr05br-protocol-v1",
        "quota": 4,
        "alpha": [1, 20],
        "tail_allocations": [[1, 80], [1, 80], [1, 80], [1, 80]],
        "grid_denominator": 256,
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
        "fixtures": [
            {"id": "flat_0", "eta": 0, "delta": [0, 1]},
            {"id": "flat_1", "eta": 0, "delta": [1, 1]},
            {"id": "flat_interior", "eta": 0, "delta": [16, 11]},
            {"id": "conformal_0", "eta": 1, "delta": [0, 1]},
            {"id": "conformal_1", "eta": 1, "delta": [1, 1]},
            {"id": "conformal_interior", "eta": 1, "delta": [45, 158]},
        ],
        "ties": [
            {"id": "lower_tie", "side": "lower", "k": 4, "epsilon": [1, 16]},
            {"id": "upper_tie", "side": "upper", "k": 0, "epsilon": [1, 16]},
        ],
        "observer": {
            "schema": "qr05br-record-query-v1",
            "protocol_id": "qr05br-n4-g256-a20-v1",
            "data_kind": "paired_causal_records",
            "bound_basis": "external_assumption",
            "result_schema": "qr05br-record-result-v1",
            "confidence_basis": "fixed_iid_paired_binomial_union",
            "coverage_kind": "unconditional_model_relative",
        },
        "coverage": {
            "tail_rows": 1285,
            "tail_values": 2570,
            "intervals": 5,
            "counts": 15,
            "cases": 60,
            "hypotheses": 240,
            "fixtures": 6,
            "count_probabilities": 90,
            "summaries": 24,
            "scale_pairs": 2,
            "comparisons": 2,
            "ties": 2,
            "obstruction_cases": 60,
            "obstruction_coverage": 4,
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


def _require(condition, message):
    if not condition:
        raise ValueError(message)


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


def _point_obstruction(geometries, regions, cases):
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


def _bernoulli_law(quota, probability):
    _require(type(quota) is int and 0 <= quota <= 4, "bounded native quota")
    _require(type(probability) is Fraction and 0 <= probability <= 1, "exact unit probability")
    # This recurrence also handles p=0 and p=1 as degenerate laws, without
    # ambiguous powers or a separate approximation.
    law = [Fraction(1)]
    for _ in range(quota):
        updated = [Fraction(0) for _ in range(len(law) + 1)]
        for k, mass in enumerate(law):
            updated[k] += (1 - probability) * mass
            updated[k + 1] += probability * mass
        law = updated
    _require(sum(law, Fraction(0)) == 1, "convolved marginal normalization")
    return law


def _tail_table(quota, grid_denominator):
    _require(type(grid_denominator) is int and 1 <= grid_denominator <= 256, "bounded grid")
    columns = []
    for index in range(grid_denominator + 1):
        grid = Fraction(index, grid_denominator)
        law = _bernoulli_law(quota, grid)
        plus, minus = [Fraction(0)] * (quota + 1), [Fraction(0)] * (quota + 1)
        cumulative = Fraction(0)
        for k in range(quota + 1):
            cumulative += law[k]
            minus[k] = cumulative
        cumulative = Fraction(0)
        for k in range(quota, -1, -1):
            cumulative += law[k]
            plus[k] = cumulative
        _require(
            all(plus[k] + minus[k] == 1 + law[k] for k in range(quota + 1)),
            "inclusive cumulative-tail identity",
        )
        columns.append((grid, plus, minus))
    return [
        {"k": k, "grid": grid, "plus": plus[k], "minus": minus[k]}
        for k in range(quota + 1)
        for grid, plus, minus in columns
    ]


def _endpoint_certificate(k, side, epsilon, tails, quota, grid_denominator):
    _require(type(k) is int and 0 <= k <= quota, "native count")
    _require(type(side) is str and side in ("lower", "upper"), "endpoint side")
    _require(type(epsilon) is Fraction and 0 < epsilon < 1, "positive tail allocation")
    rows = [row for row in tails if row["k"] == k]
    _require(
        len(rows) == grid_denominator + 1
        and all(row["grid"] == Fraction(j, grid_denominator) for j, row in enumerate(rows)),
        "complete ordered grid slice",
    )
    key = "plus" if side == "lower" else "minus"
    default = (side == "lower" and k == 0) or (side == "upper" and k == quota)
    if default:
        row = rows[0 if side == "lower" else -1]
        _require(row[key] == 1, "default endpoint tail is one")
        return {"kind": "default", "grid": row["grid"], "tail": row[key], "neighbor": []}
    eligible = [j for j, row in enumerate(rows) if row[key] <= epsilon]
    _require(bool(eligible), "nondefault endpoint exists")
    selected = max(eligible) if side == "lower" else min(eligible)
    neighbor = selected + 1 if side == "lower" else selected - 1
    _require(0 <= neighbor <= grid_denominator, "inward neighbor exists")
    row, adjacent = rows[selected], rows[neighbor]
    _require(row[key] <= epsilon < adjacent[key], "selected and inward threshold certificate")
    return {
        "kind": "tail",
        "grid": row["grid"],
        "tail": row[key],
        "neighbor": [[adjacent["grid"], adjacent[key]]],
    }


def _interval_table(tails, quota, grid_denominator, epsilon):
    result = []
    for k in range(quota + 1):
        lower = _endpoint_certificate(k, "lower", epsilon, tails, quota, grid_denominator)
        upper = _endpoint_certificate(k, "upper", epsilon, tails, quota, grid_denominator)
        interval = [lower["grid"], upper["grid"]]
        _interval(interval)
        result.append({"k": k, "interval": interval, "lower": lower, "upper": upper})
    _require(
        all(
            a["interval"][0] <= b["interval"][0] and a["interval"][1] <= b["interval"][1]
            for a, b in pairwise(result)
        ),
        "count-monotone confidence endpoints",
    )
    return result


def _count_dp(quota, weights):
    _require(type(quota) is int and 0 <= quota <= 4, "bounded count-DP quota")
    _require(type(weights) is list and len(weights) == 3, "three allowed category weights")
    scalar = type(weights[0])
    _require(
        scalar in (int, Fraction) and all(type(value) is scalar for value in weights),
        "uniform exact DP scalars",
    )
    _require(all(value >= 0 for value in weights), "nonnegative category weights")
    zero, one = scalar(0), scalar(1)
    states = {(0, 0): one}
    for _ in range(quota):
        updated = {}
        for (k1, k2), mass in states.items():
            for (i, j), weight in zip(((0, 0), (0, 1), (1, 1)), weights):
                key = (k1 + i, k2 + j)
                updated[key] = updated.get(key, zero) + mass * weight
        states = updated
    return states


def _counts(quota, intervals):
    multiplicities = _count_dp(quota, [1, 1, 1])
    result = []
    for k1 in range(quota + 1):
        for k2 in range(k1, quota + 1):
            box = [list(intervals[k1]["interval"]), list(intervals[k2]["interval"])]
            result.append(
                {
                    "id": str(k1) + "/" + str(k2),
                    "k": [k1, k2],
                    "category_counts": [quota - k2, k2 - k1, k1],
                    "multiplicity": multiplicities[(k1, k2)],
                    "intervals": box,
                    "nested_nonempty": box[0][0] <= box[1][1],
                }
            )
    _require(len(result) == len(multiplicities), "complete reachable count states")
    _require(
        sum(row["multiplicity"] for row in result) == 3**quota, "unit-weight DP word accounting"
    )
    return result


def _case(bound, count, geometries, regions):
    hypotheses = [_hypothesis(geometry, count, bound, regions) for geometry in geometries]
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({geometry["target"] for geometry in geometries if geometry["id"] in worlds})
    return {
        "id": bound["id"] + "/" + count["id"],
        "bound": bound["id"],
        "count": count["id"],
        "intervals": [list(row) for row in count["intervals"]],
        "nested_nonempty": count["nested_nonempty"],
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": "infeasible"
        if not targets
        else "identified"
        if len(targets) == 1
        else "ambiguous",
    }


def _fixture(raw, geometry, regions, counts, quota):
    delta = _fraction(raw["delta"])
    _require(0 <= delta <= 2, "fixture in full continuous domain")
    mass = _mass(geometry, delta, regions)
    _require(0 < mass[1] < mass[2] < mass[0], "strict nested fixture masses")
    q = [mass[1] / mass[0], mass[2] / mass[0]]
    one_point = _one_point(q)
    probabilities = _count_dp(quota, [one_point[0], one_point[1], one_point[3]])
    rows = []
    marginal1 = [Fraction(0) for _ in range(quota + 1)]
    marginal2 = [Fraction(0) for _ in range(quota + 1)]
    mean1, mean2, cross = Fraction(0), Fraction(0), Fraction(0)
    for count in counts:
        k1, k2 = count["k"]
        probability = probabilities[(k1, k2)]
        _require(type(probability) is Fraction and probability > 0, "positive count probability")
        covered = all(_contains(interval, value) for interval, value in zip(count["intervals"], q))
        rows.append({"count": count["id"], "p": probability, "population_covered": covered})
        marginal1[k1] += probability
        marginal2[k2] += probability
        mean1 += k1 * probability
        mean2 += k2 * probability
        cross += k1 * k2 * probability
    _require(len(rows) == len(probabilities), "complete paired count law")
    _require(sum((row["p"] for row in rows), Fraction(0)) == 1, "paired count normalization")
    _require(marginal1 == _bernoulli_law(quota, q[0]), "first binomial marginal from paired law")
    _require(marginal2 == _bernoulli_law(quota, q[1]), "second binomial marginal from paired law")
    _require(mean1 == quota * q[0] and mean2 == quota * q[1], "marginal count means")
    covariance = cross - mean1 * mean2
    independent_10 = q[0] * (1 - q[1])
    _require(independent_10 > 0 and one_point[2] == 0, "independent-question negative control")
    _require(covariance == quota * independent_10, "shared-question count covariance")
    return {
        "id": raw["id"],
        "eta": raw["eta"],
        "delta": delta,
        "target": geometry["target"],
        "q": q,
        "one_point": one_point,
        "count_law": rows,
        "independent_10": independent_10,
        "count_covariance": covariance,
    }


def _summaries(fixtures, bounds, cases, alpha):
    index = {case["id"]: case for case in cases}
    result = []
    for fixture in fixtures:
        for bound in bounds:
            in_premise = _contains(bound["interval"], fixture["delta"])
            totals = {
                key: Fraction(0)
                for key in (
                    "population_noncoverage",
                    "target_noncoverage",
                    "empty",
                    "singleton",
                    "wrong_singleton",
                    "ambiguous",
                )
            }
            for row in fixture["count_law"]:
                case = index[bound["id"] + "/" + row["count"]]
                probability = row["p"]
                population_miss = not row["population_covered"]
                target_miss = fixture["target"] not in case["targets"]
                size = len(case["targets"])
                _require(size in (0, 1, 2), "discrete target domain")
                if population_miss:
                    totals["population_noncoverage"] += probability
                if target_miss:
                    totals["target_noncoverage"] += probability
                category = ("empty", "singleton", "ambiguous")[size]
                totals[category] += probability
                if size == 1 and target_miss:
                    totals["wrong_singleton"] += probability
                if in_premise:
                    _require(not target_miss or population_miss, "in-premise event containment")
            _require(
                totals["empty"] + totals["singleton"] + totals["ambiguous"] == 1,
                "complete outcome probabilities",
            )
            _require(
                totals["target_noncoverage"] == totals["empty"] + totals["wrong_singleton"],
                "empty plus wrong singleton identity",
            )
            population_bound = totals["population_noncoverage"] <= alpha
            target_bound = totals["target_noncoverage"] <= alpha
            _require(population_bound, "population coverage for every valid fixture")
            if in_premise:
                _require(
                    target_bound
                    and totals["target_noncoverage"] <= totals["population_noncoverage"],
                    "in-premise target coverage only",
                )
            conditional = (
                []
                if totals["singleton"] == 0
                else [totals["wrong_singleton"] / totals["singleton"]]
            )
            result.append(
                {
                    "id": fixture["id"] + "/" + bound["id"],
                    "fixture": fixture["id"],
                    "bound": bound["id"],
                    "in_premise": in_premise,
                    **totals,
                    "conditional_wrong_singleton": conditional,
                    "population_bound_holds": population_bound,
                    "target_bound_holds": target_bound,
                }
            )
    return result


def _comparisons(fixtures):
    index = {fixture["id"]: fixture for fixture in fixtures}
    result = []
    for identifier, pair in (
        ("whole_point", ("flat_1", "conformal_0")),
        ("membership_only", ("flat_interior", "conformal_interior")),
    ):
        first, second = (index[name] for name in pair)
        q1_equal, q2_equal = first["q"][0] == second["q"][0], first["q"][1] == second["q"][1]
        law_equal = [row["p"] for row in first["count_law"]] == [
            row["p"] for row in second["count_law"]
        ]
        _require(q1_equal and law_equal == q2_equal, "paired count-law comparison")
        if identifier == "whole_point":
            _require(q2_equal, "inherited whole-point pair")
        result.append(
            {
                "id": identifier,
                "fixtures": list(pair),
                "q1_equal": q1_equal,
                "q2_equal": q2_equal,
                "count_law_equal": law_equal,
                "target_gap": first["target"] - second["target"],
                "q2_gap": first["q"][1] - second["q"][1],
            }
        )
    return result


def _ties(protocol, tails):
    result = []
    for raw in protocol["ties"]:
        epsilon = _fraction(raw["epsilon"])
        certificate = _endpoint_certificate(
            raw["k"], raw["side"], epsilon, tails, protocol["quota"], protocol["grid_denominator"]
        )
        _require(
            certificate["grid"] == Fraction(1, 2) and certificate["tail"] == epsilon,
            "private equality endpoint control",
        )
        result.append(
            {
                "id": raw["id"],
                "side": raw["side"],
                "k": raw["k"],
                "epsilon": epsilon,
                "certificate": certificate,
            }
        )
    return result


def _obstruction(geometries, regions, cases, fixtures, bounds, alpha):
    result = _point_obstruction(geometries, regions, cases)
    fixture_index = {fixture["id"]: fixture for fixture in fixtures}
    common = fixture_index["flat_1"]["count_law"]
    other = fixture_index["conformal_0"]["count_law"]
    _require(
        [row["p"] for row in common] == [row["p"] for row in other]
        and fixture_index["flat_1"]["q"] == result["q"],
        "same full count law for the compensated pair",
    )
    case_index = {case["id"]: case for case in cases}
    witnesses = {row["case"]: row for row in result["cases"]}
    coverage = []
    for bound in bounds:
        both_in = all(_contains(bound["interval"], delta) for delta in result["deltas"])
        probability = Fraction(0)
        for row in common:
            identifier = bound["id"] + "/" + row["count"]
            case = case_index[identifier]
            if case["status"] == "ambiguous":
                probability += row["p"]
            if both_in and row["population_covered"]:
                _require(
                    witnesses[identifier]["both"], "common population event includes both witnesses"
                )
        bound_holds = probability >= 1 - alpha
        if both_in:
            _require(bound_holds, "common-box ambiguity coverage under admitted pair")
        coverage.append(
            {
                "bound": bound["id"],
                "both_in_premise": both_in,
                "both_target_probability": probability,
                "bound_holds": bound_holds,
            }
        )
    result["coverage"] = coverage
    return result


def _support(geometries, counts, quota):
    certificate = all(geometry["strict_support"] for geometry in geometries)
    _require(certificate, "continuous geometric support")
    symbols, allowed = [[0, 0], [0, 1], [1, 0], [1, 1]], [[0, 0], [0, 1], [1, 1]]
    possible = len(allowed) ** quota
    return {
        "symbols": symbols,
        "allowed": allowed,
        "count_states": len(counts),
        "possible_words": possible,
        "zero_words": len(symbols) ** quota - possible,
        "continuous_certificate": certificate,
    }


def analyze(protocol: dict) -> dict:
    _validate_protocol(protocol)
    quota, grid_denominator = protocol["quota"], protocol["grid_denominator"]
    alpha = _fraction(protocol["alpha"])
    allocations = [_fraction(pair) for pair in protocol["tail_allocations"]]
    _require(
        0 < alpha < 1
        and all(value > 0 for value in allocations)
        and sum(allocations, Fraction(0)) <= alpha,
        "simultaneous tail budget",
    )
    _require(all(value == allocations[0] for value in allocations), "shared fixed interval table")
    confidence = {
        "quota": quota,
        "alpha": alpha,
        "tail_allocations": allocations,
        "grid_denominator": grid_denominator,
        "confidence_basis": protocol["observer"]["confidence_basis"],
        "bound_basis": protocol["observer"]["bound_basis"],
        "coverage_kind": protocol["observer"]["coverage_kind"],
    }
    tails = _tail_table(quota, grid_denominator)
    intervals = _interval_table(tails, quota, grid_denominator, allocations[0])
    counts = _counts(quota, intervals)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    geometries = [_geometry(raw, regions) for raw in protocol["geometries"]]
    cases = [_case(bound, count, geometries, regions) for bound in bounds for count in counts]
    unit_geometries = {row["eta"]: row for row in geometries if row["scale"] == 1}
    fixtures = [
        _fixture(raw, unit_geometries[raw["eta"]], regions, counts, quota)
        for raw in protocol["fixtures"]
    ]
    summaries = _summaries(fixtures, bounds, cases, alpha)
    scale_pairs = _scale_pairs(geometries, cases)
    comparisons = _comparisons(fixtures)
    ties = _ties(protocol, tails)
    obstruction = _obstruction(geometries, regions, cases, fixtures, bounds, alpha)
    support = _support(geometries, counts, quota)
    coverage = {
        "tail_rows": len(tails),
        "tail_values": 2 * len(tails),
        "intervals": len(intervals),
        "counts": len(counts),
        "cases": len(cases),
        "hypotheses": sum(len(case["hypotheses"]) for case in cases),
        "fixtures": len(fixtures),
        "count_probabilities": sum(len(row["count_law"]) for row in fixtures),
        "summaries": len(summaries),
        "scale_pairs": len(scale_pairs),
        "comparisons": len(comparisons),
        "ties": len(ties),
        "obstruction_cases": len(obstruction["cases"]),
        "obstruction_coverage": len(obstruction["coverage"]),
    }
    _require(coverage == protocol["coverage"], "fixed report inventory")
    report = {
        "schema": "qr05br-report-v1",
        "confidence": confidence,
        "tails": tails,
        "intervals": intervals,
        "counts": counts,
        "geometries": geometries,
        "cases": cases,
        "fixtures": fixtures,
        "summaries": summaries,
        "scale_pairs": scale_pairs,
        "comparisons": comparisons,
        "ties": ties,
        "obstruction": obstruction,
        "support": support,
    }
    _native_report(report)
    return report
