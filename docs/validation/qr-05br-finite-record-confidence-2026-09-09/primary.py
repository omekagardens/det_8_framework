"""BR exact integer tails, monomial masses and shared-density halfspaces.

Import defines functions only. The explicit analyzer has no file access,
historical engine imports, stored-answer lookup or floating arithmetic.
"""

from fractions import Fraction as F
from itertools import pairwise
from math import comb, factorial, gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native_input(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (int, str):
        return
    _require(kind in (dict, list), "native protocol containers/scalars")
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
    _require(type(protocol) is dict and protocol == expected, "complete fixed BR protocol")


def _fraction(pair):
    _require(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "native rational pair",
    )
    numerator, denominator = pair
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "reduced rational pair")
    return F(numerator, denominator)


def _tail_numerators(k, index, quota, denominator):
    """Inclusive tails over one common integer denominator, including edge laws."""
    total = denominator**quota
    if index == 0:
        masses = [total] + [0] * quota
    elif index == denominator:
        masses = [0] * quota + [total]
    else:
        masses = [
            comb(quota, r) * index**r * (denominator - index) ** (quota - r)
            for r in range(quota + 1)
        ]
    _require(sum(masses) == total, "integer binomial normalization")
    plus, minus = sum(masses[k:]), sum(masses[: k + 1])
    _require(plus + minus == total + masses[k], "inclusive tail overlap identity")
    return plus, minus


def _certificate(k, side, epsilon, quota, denominator, numerators):
    column = 0 if side == "lower" else 1
    common = denominator**quota
    values = [row[column] for row in numerators]
    eligible = [
        index
        for index, value in enumerate(values)
        if value * epsilon.denominator <= epsilon.numerator * common
    ]
    default = k == (0 if side == "lower" else quota)
    if default:
        index = 0 if side == "lower" else denominator
        _require(not eligible and values[index] == common, "default endpoint tail is one")
        neighbor = []
    else:
        _require(bool(eligible), "nondefault endpoint has eligible grid values")
        index = max(eligible) if side == "lower" else min(eligible)
        inward = index + 1 if side == "lower" else index - 1
        _require(0 <= inward <= denominator, "nondefault endpoint has inward neighbor")
        _require(
            values[index] * epsilon.denominator
            <= epsilon.numerator * common
            < values[inward] * epsilon.denominator,
            "closed selected tail and strict inward-neighbor certificate",
        )
        neighbor = [[F(inward, denominator), F(values[inward], common)]]
    return {
        "kind": "default" if default else "tail",
        "grid": F(index, denominator),
        "tail": F(values[index], common),
        "neighbor": neighbor,
    }


def _endpoint(k, side, epsilon, quota=4, grid_denominator=256):
    """Private exact endpoint helper, also used for the separate equality controls."""
    _require(
        type(k) is int and type(quota) is int and type(grid_denominator) is int,
        "native count/grid metadata",
    )
    _require(
        1 <= quota <= 4 and 0 <= k <= quota and 1 <= grid_denominator <= 256,
        "bounded private endpoint domain",
    )
    _require(type(side) is str and side in ("lower", "upper"), "endpoint side")
    _require(type(epsilon) is F and 0 < epsilon < 1, "exact private tail allocation")
    numerators = [
        _tail_numerators(k, j, quota, grid_denominator) for j in range(grid_denominator + 1)
    ]
    return _certificate(k, side, epsilon, quota, grid_denominator, numerators)


def _confidence_tables(protocol):
    quota, denominator = protocol["quota"], protocol["grid_denominator"]
    alpha = _fraction(protocol["alpha"])
    allocations = [_fraction(pair) for pair in protocol["tail_allocations"]]
    _require(
        0 < alpha < 1
        and all(0 < value < 1 for value in allocations)
        and sum(allocations, F(0)) <= alpha
        and len(set(allocations)) == 1,
        "fixed simultaneous error budget and shared count intervals",
    )
    tails, intervals = [], []
    common = denominator**quota
    for k in range(quota + 1):
        integers = [_tail_numerators(k, j, quota, denominator) for j in range(denominator + 1)]
        _require(
            all(a[0] <= b[0] and a[1] >= b[1] for a, b in pairwise(integers)),
            "tail monotonicity on the declared grid",
        )
        for j, (plus, minus) in enumerate(integers):
            tails.append(
                {
                    "k": k,
                    "grid": F(j, denominator),
                    "plus": F(plus, common),
                    "minus": F(minus, common),
                }
            )
            _require(
                all(
                    value * allocations[0].denominator != allocations[0].numerator * common
                    for value in (plus, minus)
                ),
                "main dyadic table has no allocation equality",
            )
        lower = _certificate(k, "lower", allocations[0], quota, denominator, integers)
        upper = _certificate(k, "upper", allocations[1], quota, denominator, integers)
        _require(lower["grid"] <= upper["grid"], "outward confidence interval does not reverse")
        intervals.append(
            {"k": k, "interval": [lower["grid"], upper["grid"]], "lower": lower, "upper": upper}
        )
    confidence = {
        "quota": quota,
        "alpha": alpha,
        "tail_allocations": allocations,
        "grid_denominator": denominator,
        "confidence_basis": protocol["observer"]["confidence_basis"],
        "bound_basis": protocol["observer"]["bound_basis"],
        "coverage_kind": protocol["observer"]["coverage_kind"],
    }
    ties = []
    for supplied in protocol["ties"]:
        epsilon = _fraction(supplied["epsilon"])
        certificate = _endpoint(supplied["k"], supplied["side"], epsilon, quota, denominator)
        _require(
            certificate["grid"] == F(1, 2) and certificate["tail"] == epsilon,
            "separate exact-equality endpoint control",
        )
        ties.append(
            {
                "id": supplied["id"],
                "side": supplied["side"],
                "k": supplied["k"],
                "epsilon": epsilon,
                "certificate": certificate,
            }
        )
    return confidence, tails, intervals, ties


def _counts(quota, intervals):
    rows = []
    for k1 in range(quota + 1):
        for k2 in range(k1, quota + 1):
            categories = [quota - k2, k2 - k1, k1]
            divisor = 1
            for count in categories:
                divisor *= factorial(count)
            multiplicity, remainder = divmod(factorial(quota), divisor)
            _require(remainder == 0 and multiplicity > 0, "integer multinomial multiplicity")
            box = [list(intervals[k]["interval"]) for k in (k1, k2)]
            rows.append(
                {
                    "id": f"{k1}/{k2}",
                    "k": [k1, k2],
                    "category_counts": categories,
                    "multiplicity": multiplicity,
                    "intervals": box,
                    "nested_nonempty": box[0][0] <= box[1][1],
                }
            )
    _require(
        sum(row["multiplicity"] for row in rows) == 3**quota,
        "count multiplicities cover the allowed ordered words",
    )
    return rows


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
    categories = [
        _subtract(coefficients[0], coefficients[2]),
        _subtract(coefficients[2], coefficients[1]),
        list(coefficients[1]),
    ]
    support = all(a > 0 and b >= 0 for a, b in categories)
    a_q, b_q = coefficients[0]
    _require(support and a_q > 0 and b_q >= 0, "continuous positive mass certificate")
    derivatives = [b * a_q - a * b_q for a, b in coefficients[1:]]
    _require(all(value < 0 for value in derivatives), "strictly decreasing sampling ratios")
    geometry = {
        "id": supplied["id"],
        "eta": supplied["eta"],
        "scale": supplied["scale"],
        "volumes": volumes,
        "target": volumes[1] / volumes[0],
        "mass_coefficients": coefficients,
        "derivative_numerators": derivatives,
        "full_q_ranges": [],
        "category_coefficients": categories,
        "strict_support": support,
    }
    left, right = _forward(geometry, F(0)), _forward(geometry, F(2))
    geometry["full_q_ranges"] = [sorted([left[i], right[i]]) for i in range(2)]
    return geometry, proper, slope


def _inequality(constant, slope):
    _require(type(constant) is F and type(slope) is F, "exact affine halfspace")
    if slope == 0:
        return {
            "constant": constant,
            "slope": slope,
            "kind": "all" if constant >= 0 else "none",
            "boundary": [],
        }
    return {
        "constant": constant,
        "slope": slope,
        "kind": "lower" if slope > 0 else "upper",
        "boundary": [-constant / slope],
    }


def _clip(interval, inequality):
    if not interval or inequality["kind"] == "none":
        return []
    lower, upper = interval
    if inequality["kind"] == "lower":
        lower = max(lower, inequality["boundary"][0])
    elif inequality["kind"] == "upper":
        upper = min(upper, inequality["boundary"][0])
    else:
        _require(inequality["kind"] == "all", "known zero-slope halfspace")
    return [lower, upper] if lower <= upper else []


def _intersect(left, right):
    if not left or not right:
        return []
    lower, upper = max(left[0], right[0]), min(left[1], right[1])
    return [lower, upper] if lower <= upper else []


def _contains(interval, value):
    return bool(interval) and interval[0] <= value <= interval[1]


def _curve(geometry, interval, count):
    coefficients = geometry["mass_coefficients"]
    numerators = [
        list(geometry["category_coefficients"][0]),
        list(geometry["category_coefficients"][1]),
        [F(0), F(0)],
        list(geometry["category_coefficients"][2]),
    ]
    endpoints = []
    for delta in interval:
        q = _forward(geometry, delta)
        normalizer = _affine(coefficients[0], delta)
        law = [_affine(row, delta) / normalizer for row in numerators]
        _require(
            law == [1 - q[1], q[1] - q[0], F(0), q[0]] and sum(law, F(0)) == 1,
            "same-density paired endpoint law",
        )
        _require(
            all(_contains(box, value) for box, value in zip(count["intervals"], q, strict=True)),
            "coupled endpoint lies in the constructed box",
        )
        endpoints.append({"delta": delta, "q": q, "one_point": law})
    _require(len(endpoints) == 2, "retain duplicate singleton endpoints")
    return {
        "domain": list(interval),
        "numerators": [list(row) for row in coefficients[1:]],
        "denominator": list(coefficients[0]),
        "one_point_numerators": numerators,
        "endpoints": endpoints,
        "q_ranges": [sorted([endpoints[0]["q"][i], endpoints[1]["q"][i]]) for i in range(2)],
    }


def _hypothesis(geometry, count, bound):
    a_q, b_q = geometry["mass_coefficients"][0]
    inequalities = []
    for (a, b), (lower, upper) in zip(
        geometry["mass_coefficients"][1:], count["intervals"], strict=True
    ):
        inequalities.append(_inequality(a - lower * a_q, b - lower * b_q))
        inequalities.append(_inequality(upper * a_q - a, upper * b_q - b))
    queries = []
    for start in (0, 2):
        interval = list(bound)
        for inequality in inequalities[start : start + 2]:
            interval = _clip(interval, inequality)
        queries.append(interval)
    joint = _intersect(queries[0], queries[1])
    direct = list(bound)
    for inequality in inequalities:
        direct = _clip(direct, inequality)
    _require(joint == direct, "per-query conjunction equals all-four halfspaces")
    if joint:
        _require(
            count["nested_nonempty"]
            and all(
                row["constant"] + row["slope"] * value >= 0
                for row in inequalities
                for value in joint
            ),
            "closed original-inequality endpoints",
        )
    return {
        "id": geometry["id"],
        "inequalities": inequalities,
        "query_sets": queries,
        "delta_set": joint,
        "status": "feasible" if joint else "infeasible",
        "curve": _curve(geometry, joint, count) if joint else {},
    }


def _case(bound, count, geometries):
    hypotheses = [_hypothesis(geometry, count, bound["interval"]) for geometry in geometries]
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
        if not worlds
        else "identified"
        if len(targets) == 1
        else "ambiguous",
    }


def _fixture(supplied, compiled, regions, counts, quota):
    geometry, proper, slope = next(
        row for row in compiled if row[0]["eta"] == supplied["eta"] and row[0]["scale"] == 1
    )
    delta = _fraction(supplied["delta"])
    _require(0 <= delta <= 2, "fixture density in the continuous model")
    weighted = _add(proper, _scale(slope, delta))
    masses = [_integrate(weighted, rectangle) for rectangle in regions]
    _require(
        masses == [_affine(row, delta) for row in geometry["mass_coefficients"]],
        "direct fixture monomials agree with affine mass compilation",
    )
    q = [masses[index] / masses[0] for index in (1, 2)]
    one_point = [1 - q[1], q[1] - q[0], F(0), q[0]]
    _require(
        sum(one_point, F(0)) == 1 and all(one_point[i] > 0 for i in (0, 1, 3)),
        "normalized positive allowed fixture categories",
    )
    rows = []
    for count in counts:
        probability = F(count["multiplicity"])
        for base, exponent in zip(
            (one_point[0], one_point[1], one_point[3]), count["category_counts"], strict=True
        ):
            probability *= base**exponent
        _require(probability > 0, "every valid count state has positive fixture mass")
        covered = all(
            _contains(interval, value)
            for interval, value in zip(count["intervals"], q, strict=True)
        )
        rows.append({"count": count["id"], "p": probability, "population_covered": covered})
    _require(sum(row["p"] for row in rows) == 1, "complete multinomial count-law normalization")
    for i in range(2):
        for k in range(quota + 1):
            marginal = sum(
                (row["p"] for count, row in zip(counts, rows, strict=True) if count["k"][i] == k),
                F(0),
            )
            expected = F(comb(quota, k)) * q[i] ** k * (1 - q[i]) ** (quota - k)
            _require(marginal == expected, "binomial count marginal, not independent joint counts")
    means = [
        sum((row["p"] * count["k"][i] for count, row in zip(counts, rows, strict=True)), F(0))
        for i in range(2)
    ]
    cross = sum(
        (row["p"] * count["k"][0] * count["k"][1] for count, row in zip(counts, rows, strict=True)),
        F(0),
    )
    covariance = cross - means[0] * means[1]
    independent_10 = q[0] * (1 - q[1])
    _require(
        means == [quota * value for value in q] and covariance == quota * independent_10 > 0,
        "enumerated shared-point covariance",
    )
    return {
        "id": supplied["id"],
        "eta": supplied["eta"],
        "delta": delta,
        "target": geometry["target"],
        "q": q,
        "one_point": one_point,
        "count_law": rows,
        "independent_10": independent_10,
        "count_covariance": covariance,
    }


def _summaries(fixtures, bounds, cases, alpha):
    by_case = {row["id"]: row for row in cases}
    result = []
    for fixture in fixtures:
        population = sum(
            (row["p"] for row in fixture["count_law"] if not row["population_covered"]), F(0)
        )
        _require(population <= alpha, "fixture simultaneous population-box coverage")
        for bound in bounds:
            in_premise = _contains(bound["interval"], fixture["delta"])
            sums = {
                key: F(0)
                for key in (
                    "target_noncoverage",
                    "empty",
                    "singleton",
                    "wrong_singleton",
                    "ambiguous",
                )
            }
            for row in fixture["count_law"]:
                case = by_case[bound["id"] + "/" + row["count"]]
                miss = fixture["target"] not in case["targets"]
                size = len(case["targets"])
                category = "empty" if size == 0 else "singleton" if size == 1 else "ambiguous"
                sums[category] += row["p"]
                if miss:
                    sums["target_noncoverage"] += row["p"]
                    if size == 1:
                        sums["wrong_singleton"] += row["p"]
                if in_premise:
                    _require(
                        not miss or not row["population_covered"],
                        "in-premise target-miss event containment",
                    )
            _require(
                sums["empty"] + sums["singleton"] + sums["ambiguous"] == 1
                and sums["target_noncoverage"] == sums["empty"] + sums["wrong_singleton"],
                "complete status partition and exact target-miss decomposition",
            )
            target_bound = sums["target_noncoverage"] <= alpha
            if in_premise:
                _require(
                    sums["target_noncoverage"] <= population <= alpha,
                    "in-premise confidence-to-target coverage transfer",
                )
            conditional = [sums["wrong_singleton"] / sums["singleton"]] if sums["singleton"] else []
            result.append(
                {
                    "id": fixture["id"] + "/" + bound["id"],
                    "fixture": fixture["id"],
                    "bound": bound["id"],
                    "in_premise": in_premise,
                    "population_noncoverage": population,
                    **sums,
                    "conditional_wrong_singleton": conditional,
                    "population_bound_holds": population <= alpha,
                    "target_bound_holds": target_bound,
                }
            )
    return result


def _normalized_curve(curve):
    if not curve:
        return {}
    constant = curve["denominator"][0]
    _require(constant > 0, "positive normalized coefficient gauge")
    return {
        "domain": list(curve["domain"]),
        "numerators": [[x / constant for x in row] for row in curve["numerators"]],
        "denominator": [x / constant for x in curve["denominator"]],
        "one_point_numerators": [
            [x / constant for x in row] for row in curve["one_point_numerators"]
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
        _require(factor == F(right["scale"], left["scale"]), "metric scale and volume factor")
        _require(
            right["volumes"] == [factor * x for x in left["volumes"]]
            and right["derivative_numerators"]
            == [factor**2 * x for x in left["derivative_numerators"]]
            and left["full_q_ranges"] == right["full_q_ranges"],
            "all-region and derivative scaling",
        )
        for field in ("mass_coefficients", "category_coefficients"):
            _require(
                right[field] == [[factor * x for x in row] for row in left[field]],
                "actual mass scaling",
            )
        nuisance_equal, curve_equal = True, True
        for case in cases:
            hypotheses = {row["id"]: row for row in case["hypotheses"]}
            a, b = hypotheses[first], hypotheses[second]
            nuisance_equal = nuisance_equal and a["delta_set"] == b["delta_set"]
            curve_equal = curve_equal and _normalized_curve(a["curve"]) == _normalized_curve(
                b["curve"]
            )
            _require(
                a["query_sets"] == b["query_sets"] and a["status"] == b["status"],
                "scale-invariant query feasibility",
            )
            for x, y in zip(a["inequalities"], b["inequalities"], strict=True):
                _require(
                    y["constant"] == factor * x["constant"]
                    and y["slope"] == factor * x["slope"]
                    and x["kind"] == y["kind"]
                    and x["boundary"] == y["boundary"],
                    "raw inequality scaling",
                )
            if a["curve"]:
                for field in ("numerators", "one_point_numerators"):
                    _require(
                        b["curve"][field]
                        == [[factor * x for x in row] for row in a["curve"][field]],
                        "raw curve numerator scaling",
                    )
                _require(
                    b["curve"]["denominator"] == [factor * x for x in a["curve"]["denominator"]],
                    "raw curve normalizer scaling",
                )
        target_equal = left["target"] == right["target"]
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


def _comparisons(fixtures):
    by_id = {row["id"]: row for row in fixtures}
    result = []
    for identifier, names in (
        ("whole_point", ["flat_1", "conformal_0"]),
        ("membership_only", ["flat_interior", "conformal_interior"]),
    ):
        left, right = [by_id[name] for name in names]
        equal1 = left["q"][0] == right["q"][0]
        equal2 = left["q"][1] == right["q"][1]
        laws_equal = [row["p"] for row in left["count_law"]] == [
            row["p"] for row in right["count_law"]
        ]
        _require(
            equal1 and equal2 == laws_equal and equal2 == (identifier == "whole_point"),
            "prespecified equal-first-query and distinct joint-law controls",
        )
        result.append(
            {
                "id": identifier,
                "fixtures": names,
                "q1_equal": equal1,
                "q2_equal": equal2,
                "count_law_equal": laws_equal,
                "target_gap": left["target"] - right["target"],
                "q2_gap": left["q"][1] - right["q"][1],
            }
        )
    return result


def _obstruction(compiled, regions, bounds, cases, fixtures, alpha):
    by_id = {row[0]["id"]: row for row in compiled}
    names, deltas = ["flat", "conformal"], [F(1), F(0)]
    polynomials, probabilities = [], []
    for name, delta in zip(names, deltas, strict=True):
        geometry, proper, slope = by_id[name]
        weighted = _add(proper, _scale(slope, delta))
        masses = [_integrate(weighted, rectangle) for rectangle in regions]
        polynomials.append(_scale(weighted, F(1) / masses[0]))
        probabilities.append([masses[i] / masses[0] for i in (1, 2)])
        _require(
            masses == [_affine(row, delta) for row in geometry["mass_coefficients"]],
            "compensated monomial mass identity",
        )
    point_equal = polynomials[0] == polynomials[1]
    _require(
        point_equal and probabilities[0] == probabilities[1], "whole-point density compensation"
    )
    gap = by_id[names[0]][0]["target"] - by_id[names[1]][0]["target"]
    _require(gap != 0, "unequal compensated geometric targets")
    by_bound = {row["id"]: row["interval"] for row in bounds}
    rows = []
    for case in cases:
        hypotheses = {row["id"]: row for row in case["hypotheses"]}
        present = [
            _contains(hypotheses[name]["delta_set"], delta)
            for name, delta in zip(names, deltas, strict=True)
        ]
        fits = all(
            _contains(interval, value)
            for interval, value in zip(case["intervals"], probabilities[0], strict=True)
        )
        _require(
            present == [fits and _contains(by_bound[case["bound"]], delta) for delta in deltas],
            "direct compensated-parameter membership",
        )
        both, ambiguous = all(present), case["status"] == "ambiguous"
        _require(not both or ambiguous, "compensated pair implies target ambiguity")
        rows.append(
            {
                "case": case["id"],
                "flat_present": present[0],
                "conformal_present": present[1],
                "both": both,
                "target_ambiguous": ambiguous,
            }
        )
    fixtures_by_id = {row["id"]: row for row in fixtures}
    common = fixtures_by_id["flat_1"]["count_law"]
    _require(
        probabilities[0] == fixtures_by_id["flat_1"]["q"] == fixtures_by_id["conformal_0"]["q"],
        "shared fixture and polynomial probability law",
    )
    by_case = {row["id"]: row for row in cases}
    coverage = []
    for bound in bounds:
        both_in = all(_contains(bound["interval"], delta) for delta in deltas)
        probability = sum(
            (
                row["p"]
                for row in common
                if len(by_case[bound["id"] + "/" + row["count"]]["targets"]) == 2
            ),
            F(0),
        )
        holds = probability >= 1 - alpha
        if both_in:
            _require(holds, "common-box ambiguity at least one minus alpha")
        coverage.append(
            {
                "bound": bound["id"],
                "both_in_premise": both_in,
                "both_target_probability": probability,
                "bound_holds": holds,
            }
        )
    return {
        "worlds": names,
        "deltas": deltas,
        "q": probabilities[0],
        "point_equal": point_equal,
        "target_gap": gap,
        "cases": rows,
        "coverage": coverage,
    }


def _support(geometries, counts, quota):
    certificate = all(row["strict_support"] for row in geometries)
    _require(
        certificate and len(counts) == comb(quota + 2, 2),
        "continuous category support and count inventory",
    )
    return {
        "symbols": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "allowed": [[0, 0], [0, 1], [1, 1]],
        "count_states": len(counts),
        "possible_words": 3**quota,
        "zero_words": 4**quota - 3**quota,
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
    """Evaluate only this frozen finite confidence domain, without external state."""
    _validate(protocol)
    confidence, tails, intervals, ties = _confidence_tables(protocol)
    quota, alpha = confidence["quota"], confidence["alpha"]
    counts = _counts(quota, intervals)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    compiled = [_geometry(row, regions) for row in protocol["geometries"]]
    geometries = [row[0] for row in compiled]
    cases = [_case(bound, count, geometries) for bound in bounds for count in counts]
    fixtures = [_fixture(row, compiled, regions, counts, quota) for row in protocol["fixtures"]]
    summaries = _summaries(fixtures, bounds, cases, alpha)
    scales = _scale_pairs(geometries, cases)
    comparisons = _comparisons(fixtures)
    obstruction = _obstruction(compiled, regions, bounds, cases, fixtures, alpha)
    support = _support(geometries, counts, quota)
    by_case = {row["id"]: row for row in cases}
    for bound in bounds:
        all_zero = by_case[bound["id"] + "/0/0"]
        all_one = by_case[bound["id"] + f"/{quota}/{quota}"]
        _require(
            all_zero["status"] == "ambiguous"
            and all(row["delta_set"] == bound["interval"] for row in all_zero["hypotheses"]),
            "all00 preserves every nuisance domain and both targets",
        )
        _require(
            all_one["status"] == "infeasible" and not all_one["targets"],
            "allowed all11 has empty inverse",
        )
    census = {
        "tail_rows": len(tails),
        "tail_values": 2 * len(tails),
        "intervals": len(intervals),
        "counts": len(counts),
        "cases": len(cases),
        "hypotheses": sum(len(row["hypotheses"]) for row in cases),
        "fixtures": len(fixtures),
        "count_probabilities": sum(len(row["count_law"]) for row in fixtures),
        "summaries": len(summaries),
        "scale_pairs": len(scales),
        "comparisons": len(comparisons),
        "ties": len(ties),
        "obstruction_cases": len(obstruction["cases"]),
        "obstruction_coverage": len(obstruction["coverage"]),
    }
    _require(census == protocol["coverage"], "full prespecified confidence-domain census")
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
        "scale_pairs": scales,
        "comparisons": comparisons,
        "ties": ties,
        "obstruction": obstruction,
        "support": support,
    }
    _native_report(report)
    return report
