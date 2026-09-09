"""Exact QR-05BN monomial mass integration and linear population inversion.

No files, historical executors or computed answer tables are accessed.
All numerical work occurs only when analyze(protocol) is explicitly called.
"""

from fractions import Fraction as F
from itertools import pairwise, product
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native_input(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (str, int):
        return
    _require(kind in (dict, list), "native protocol containers and scalars")
    identity = id(value)
    _require(identity not in active, "cyclic protocol")
    if kind is dict:
        _require(all(type(key) is str for key in value), "native string protocol keys")
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native_input(child, active)
    finally:
        active.remove(identity)


def _validate(protocol):
    _native_input(protocol)
    expected = {
        "schema": "qr05bn-protocol-v1",
        "quota": 4,
        "geometries": [
            {"id": "flat", "eta": 0, "scale": 1},
            {"id": "conformal", "eta": 1, "scale": 1},
            {"id": "flat_x4", "eta": 0, "scale": 4},
            {"id": "conformal_x4", "eta": 1, "scale": 4},
        ],
        "regions": {
            "Q": [[0, 1], [1, 1], [0, 1], [1, 1]],
            "I": [[0, 1], [1, 2], [0, 1], [1, 2]],
        },
        "density_bounds": [
            {"id": "uniform", "interval": [[0, 1], [0, 1]]},
            {"id": "half", "interval": [[0, 1], [1, 2]]},
            {"id": "one", "interval": [[0, 1], [1, 1]]},
            {"id": "two", "interval": [[0, 1], [2, 1]]},
        ],
        "population_data": [
            {"id": "zero", "q": [0, 1]},
            {"id": "conformal_pole", "q": [5, 104]},
            {"id": "flat_pole", "q": [1, 16]},
            {"id": "lower_edge", "q": [173, 1136]},
            {"id": "flat_edge", "q": [3, 16]},
            {"id": "interior", "q": [1, 5]},
            {"id": "overlap", "q": [17, 80]},
            {"id": "flat_uniform", "q": [1, 4]},
            {"id": "one", "q": [1, 1]},
        ],
        "observer": {
            "schema": "qr05bn-query-v1",
            "data_kind": "population_probability",
            "bound_basis": "external_assumption",
        },
        "coverage": {
            "cases": 36,
            "hypotheses": 144,
            "laws": 9,
            "membership_rows": 144,
            "monotonicity": 27,
            "finite_records": 64,
            "collisions": 2,
        },
        "limits": {
            "source_bytes": 262144,
            "artifact_bytes": 16777216,
            "analysis_seconds": 30,
            "suite_seconds": 120,
            "alternate_reference_runs": 1,
        },
    }
    _require(type(protocol) is dict and protocol == expected, "complete fixed BN protocol")


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


def _wire(poly):
    return [[i, j, coefficient] for (i, j), coefficient in sorted(poly.items()) if coefficient]


def _affine(coefficients, delta):
    return coefficients[0] + coefficients[1] * delta


def _forward(geometry, delta):
    mass_q = _affine(geometry["mass_Q_coeffs"], delta)
    _require(mass_q > 0, "positive affine sampling normalizer")
    return _affine(geometry["mass_I_coeffs"], delta) / mass_q


def _geometry(supplied, regions, bounds):
    eta, scale = F(supplied["eta"]), F(supplied["scale"])
    proper = _clean({(0, 0): scale / 2, (1, 1): scale * eta / 2})
    density_coefficient = _multiply(proper, {(1, 1): F(1)})
    volume_q, volume_i = [_integrate(proper, regions[name]) for name in ("Q", "I")]
    mass_i = [_integrate(poly, regions["I"]) for poly in (proper, density_coefficient)]
    mass_q = [_integrate(poly, regions["Q"]) for poly in (proper, density_coefficient)]
    a, b = mass_i
    c, d = mass_q
    derivative = b * c - a * d
    _require(0 < volume_i < volume_q and c > 0 and d > 0, "positive affine mass family")
    _require(derivative < 0, "strictly decreasing population probability")
    result = {
        "id": supplied["id"],
        "eta": supplied["eta"],
        "scale": supplied["scale"],
        "volume_Q": volume_q,
        "volume_I": volume_i,
        "target": volume_i / volume_q,
        "mass_I_coeffs": mass_i,
        "mass_Q_coeffs": mass_q,
        "derivative_numerator": derivative,
        "ranges": [],
    }
    for bound in bounds:
        lower, upper = bound["interval"]
        _require(0 <= lower <= upper <= 2, "externally stipulated positive-density domain")
        image = [_forward(result, upper), _forward(result, lower)]
        _require(0 < image[0] <= image[1] < 1, "closed attainable range and strict record support")
        result["ranges"].append(
            {"bound": bound["id"], "delta": list(bound["interval"]), "q": image}
        )
    return result, proper, density_coefficient


def _hypothesis(geometry, proper, density_coefficient, regions, bound, q):
    a, b = geometry["mass_I_coeffs"]
    c, d = geometry["mass_Q_coeffs"]
    numerator, denominator = a - q * c, q * d - b
    image_rows = [row for row in geometry["ranges"] if row["bound"] == bound["id"]]
    _require(len(image_rows) == 1, "unique supplied density range")
    q_range = list(image_rows[0]["q"])
    candidate = []
    delta_set = []
    normalized = []
    mass_q = []
    mass_i = []
    if denominator == 0:
        _require(numerator != 0, "constant-map all-delta solutions are outside this family")
    else:
        delta = numerator / denominator
        candidate = [delta]
        _require(denominator * delta == numerator, "exact raw linear inverse")
        if bound["interval"][0] <= delta <= bound["interval"][1]:
            delta_set = [delta]
            weighted = _add(proper, _scale(density_coefficient, delta))
            actual_q = _integrate(weighted, regions["Q"])
            actual_i = _integrate(weighted, regions["I"])
            _require(
                actual_q == _affine(geometry["mass_Q_coeffs"], delta)
                and actual_i == _affine(geometry["mass_I_coeffs"], delta),
                "direct monomial masses agree with the affine coefficient evaluation",
            )
            _require(
                0 < actual_i < actual_q and actual_i / actual_q == q,
                "physical forward reconstruction",
            )
            point = _scale(weighted, 1 / actual_q)
            _require(
                _integrate(point, regions["Q"]) == 1 and _integrate(point, regions["I"]) == q,
                "complete normalized point law and its membership probability",
            )
            normalized = _wire(point)
            mass_q, mass_i = [actual_q], [actual_i]
    feasible = len(delta_set) == 1
    _require(
        feasible == (q_range[0] <= q <= q_range[1]),
        "linear inverse intersection agrees with the complete closed attainable range",
    )
    return {
        "id": geometry["id"],
        "q_range": q_range,
        "inverse_numerator": numerator,
        "inverse_denominator": denominator,
        "candidate": candidate,
        "delta_set": delta_set,
        "status": "feasible" if feasible else "infeasible",
        "normalized_point": normalized,
        "mass_Q": mass_q,
        "mass_I": mass_i,
    }


def _point_classes(hypotheses, geometries):
    groups = []
    signatures = []
    feasible = [row for row in hypotheses if row["delta_set"]]
    for row in feasible:
        signature = tuple((i, j, coefficient) for i, j, coefficient in row["normalized_point"])
        if signature in signatures:
            groups[signatures.index(signature)].append(row["id"])
        else:
            signatures.append(signature)
            groups.append([row["id"]])
    # This checks the full point-law condition, not just the shared membership q.
    for i, left in enumerate(feasible):
        for right in feasible[i + 1 :]:
            eta_left, eta_right = geometries[left["id"]]["eta"], geometries[right["id"]]["eta"]
            delta_left, delta_right = left["delta_set"][0], right["delta_set"][0]
            symmetric_equal = (
                eta_left + delta_left == eta_right + delta_right
                and eta_left * delta_left == eta_right * delta_right
            )
            _require(
                (left["normalized_point"] == right["normalized_point"]) == symmetric_equal,
                "complete polynomial point-law equivalence criterion",
            )
    return [
        {
            "worlds": list(group),
            "targets": sorted({geometries[name]["target"] for name in group}),
            "identified": len({geometries[name]["target"] for name in group}) == 1,
        }
        for group in groups
    ]


def _case(bound, datum, compiled, regions):
    q = datum["q"]
    hypotheses = [
        _hypothesis(geometry, proper, density_coefficient, regions, bound, q)
        for geometry, proper, density_coefficient in compiled
    ]
    geometries = {geometry["id"]: geometry for geometry, _proper, _coefficient in compiled}
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({geometries[name]["target"] for name in worlds})
    status = "infeasible" if not targets else "identified" if len(targets) == 1 else "ambiguous"
    return {
        "id": bound["id"] + "/" + datum["id"],
        "bound": bound["id"],
        "data": datum["id"],
        "q": q,
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": status,
        "point_classes": _point_classes(hypotheses, geometries),
    }


def _word_rows(q, quota):
    _require(type(q) is F and 0 <= q <= 1, "exact population probability")
    rows = []
    for word in product((0, 1), repeat=quota):
        k = sum(word)
        probability = q**k * (1 - q) ** (quota - k)
        _require(probability >= 0, "nonnegative data-law probability")
        rows.append({"y": list(word), "k": k, "p": probability})
    _require(sum((row["p"] for row in rows), F(0)) == 1, "complete stipulated data law")
    return rows


def _monotonicity(bounds, data, cases):
    by_id = {case["id"]: case for case in cases}
    result = []
    for tight, broad in pairwise(bounds):
        _require(
            broad["interval"][0]
            <= tight["interval"][0]
            <= tight["interval"][1]
            <= broad["interval"][1],
            "external bounds are nested",
        )
        for datum in data:
            left = by_id[tight["id"] + "/" + datum["id"]]
            right = by_id[broad["id"] + "/" + datum["id"]]
            world_subset = set(left["worlds"]) <= set(right["worlds"])
            target_subset = set(left["targets"]) <= set(right["targets"])
            right_rows = {row["id"]: row for row in right["hypotheses"]}
            nuisance_preserved = all(
                row["delta_set"] == right_rows[row["id"]]["delta_set"]
                for row in left["hypotheses"]
                if row["delta_set"]
            )
            _require(
                world_subset and target_subset and nuisance_preserved, "bound-tightening controls"
            )
            for row in left["hypotheses"]:
                if row["delta_set"]:
                    for field in ("normalized_point", "mass_Q", "mass_I"):
                        _require(
                            row[field] == right_rows[row["id"]][field],
                            "surviving point law is unchanged",
                        )
            result.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    "world_subset": world_subset,
                    "target_subset": target_subset,
                    "nuisance_preserved": nuisance_preserved,
                }
            )
    return result


def _finite_records(bounds, geometries, quota):
    worlds = [geometry["id"] for geometry in geometries]
    targets = sorted({geometry["target"] for geometry in geometries})
    result = []
    for bound in bounds:
        ranges = [
            row["q"]
            for geometry in geometries
            for row in geometry["ranges"]
            if row["bound"] == bound["id"]
        ]
        strict = len(ranges) == len(worlds) and all(
            0 < lower <= upper < 1 for lower, upper in ranges
        )
        _require(strict, "strict support holds throughout each complete nuisance interval")
        rows = []
        for word in product((0, 1), repeat=quota):
            k = sum(word)
            _require(
                all(lower**k * (1 - upper) ** (quota - k) > 0 for lower, upper in ranges),
                "positive uniform bound for every realized word",
            )
            rows.append(
                {
                    "y": list(word),
                    "k": k,
                    "frequency": F(k, quota),
                    "worlds": list(worlds),
                    "targets": list(targets),
                }
            )
        result.append({"bound": bound["id"], "strict_support": strict, "rows": rows})
    return result


def _collisions(cases, geometries, widest, quota):
    by_id = {case["id"]: case for case in cases}
    result = []
    for name, datum, expected_point_equal in (
        ("inherited_whole_point", "overlap", True),
        ("membership_only", "interior", False),
    ):
        case_id = widest["id"] + "/" + datum
        case = by_id[case_id]
        by_world = {row["id"]: row for row in case["hypotheses"]}
        first, second = by_world["flat"], by_world["conformal"]
        _require(
            first["delta_set"] and second["delta_set"], "both collision witnesses are feasible"
        )
        first_q = first["mass_I"][0] / first["mass_Q"][0]
        second_q = second["mass_I"][0] / second["mass_Q"][0]
        # Recompute from each witness's own integrated mass, not from case.q.
        membership_equal = _word_rows(first_q, quota) == _word_rows(second_q, quota)
        point_equal = first["normalized_point"] == second["normalized_point"]
        target_gap = geometries["flat"]["target"] - geometries["conformal"]["target"]
        _require(
            membership_equal and point_equal == expected_point_equal and target_gap != 0,
            "prespecified distinct full-point and membership-only obstructions",
        )
        result.append(
            {
                "id": name,
                "case": case_id,
                "worlds": ["flat", "conformal"],
                "deltas": [first["delta_set"][0], second["delta_set"][0]],
                "target_gap": target_gap,
                "membership_equal": membership_equal,
                "point_equal": point_equal,
            }
        )
    return result


def _scale_pairs(cases, geometries):
    result = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        left, right = geometries[first], geometries[second]
        factor = right["volume_Q"] / left["volume_Q"]
        target_equal = left["target"] == right["target"]
        nuisance_equal = True
        point_equal = True
        _require(
            factor == F(right["scale"], left["scale"])
            and factor != 1
            and right["volume_I"] == factor * left["volume_I"],
            "absolute volume follows the declared metric scale",
        )
        for case in cases:
            rows = {row["id"]: row for row in case["hypotheses"]}
            a, b = rows[first], rows[second]
            nuisance_equal = nuisance_equal and a["delta_set"] == b["delta_set"]
            point_equal = point_equal and a["normalized_point"] == b["normalized_point"]
            _require(
                a["candidate"] == b["candidate"]
                and a["q_range"] == b["q_range"]
                and a["status"] == b["status"]
                and b["inverse_numerator"] == factor * a["inverse_numerator"]
                and b["inverse_denominator"] == factor * a["inverse_denominator"],
                "scale-invariant inverse with actual scaled mass coefficients",
            )
            if a["delta_set"]:
                _require(
                    b["mass_Q"][0] == factor * a["mass_Q"][0]
                    and b["mass_I"][0] == factor * a["mass_I"][0],
                    "feasible sampling masses retain scale",
                )
        _require(target_equal and nuisance_equal and point_equal, "all-case scale ambiguity")
        result.append(
            {
                "worlds": [first, second],
                "volume_factor": factor,
                "target_equal": target_equal,
                "nuisance_sets_equal": nuisance_equal,
                "point_laws_equal": point_equal,
            }
        )
    return result


def _native_report(value):
    if type(value) in (F, int, bool, str):
        return
    _require(type(value) in (dict, list), "unsupported report value")
    if type(value) is dict:
        _require(all(type(key) is str for key in value), "native report keys")
    for child in value.values() if type(value) is dict else value:
        _native_report(child)


def analyze(protocol):
    """Solve only the declared exact-population problems, without any file access."""
    _validate(protocol)
    regions = {
        name: [_fraction(pair) for pair in rectangle]
        for name, rectangle in protocol["regions"].items()
    }
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    data = [{"id": row["id"], "q": _fraction(row["q"])} for row in protocol["population_data"]]
    compiled = [_geometry(row, regions, bounds) for row in protocol["geometries"]]
    geometries = [geometry for geometry, _proper, _coefficient in compiled]
    by_geometry = {geometry["id"]: geometry for geometry in geometries}
    cases = [_case(bound, datum, compiled, regions) for bound in bounds for datum in data]
    laws = [
        {"data": datum["id"], "q": datum["q"], "rows": _word_rows(datum["q"], protocol["quota"])}
        for datum in data
    ]
    monotonicity = _monotonicity(bounds, data, cases)
    records = _finite_records(bounds, geometries, protocol["quota"])
    collisions = _collisions(cases, by_geometry, bounds[-1], protocol["quota"])
    scales = _scale_pairs(cases, by_geometry)
    actual = {
        "cases": len(cases),
        "hypotheses": sum(len(case["hypotheses"]) for case in cases),
        "laws": len(laws),
        "membership_rows": sum(len(law["rows"]) for law in laws),
        "monotonicity": len(monotonicity),
        "finite_records": sum(len(group["rows"]) for group in records),
        "collisions": len(collisions),
    }
    _require(actual == protocol["coverage"] and len(scales) == 2, "complete declared coverage")
    report = {
        "schema": "qr05bn-report-v1",
        "geometries": geometries,
        "cases": cases,
        "laws": laws,
        "monotonicity": monotonicity,
        "finite_records": records,
        "collisions": collisions,
        "scale_pairs": scales,
    }
    _native_report(report)
    return report
