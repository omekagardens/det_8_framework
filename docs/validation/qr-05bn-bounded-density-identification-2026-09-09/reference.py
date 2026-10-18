"""Independent QR-05BN direct-quadrature and range-first inverse route.

Only standard-library exact arithmetic is used. No files, old engines,
computed answer tables or fixed evaluations are accessed on import.
"""

from fractions import Fraction
from itertools import pairwise, product


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _validate_protocol(protocol):
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
    pending = [(protocol, expected)]
    # The finite expected tree bounds traversal; aliases cannot enlarge the
    # accepted experiment or cause traversal around an input cycle forever.
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


def _rational(pair):
    return Fraction(pair[0], pair[1])


def _axis(lower, upper):
    _require(
        type(lower) is Fraction and type(upper) is Fraction and lower < upper,
        "exact positive quadrature interval",
    )
    return ((lower, 1), ((lower + upper) / 2, 4), (upper, 1))


def _integrate(function, rectangle):
    """Tensor Simpson integrates these coordinate-degree-two densities exactly."""
    left, right, bottom, top = rectangle
    total = Fraction(0)
    for u, wu in _axis(left, right):
        for v, wv in _axis(bottom, top):
            value = function(u, v)
            _require(type(value) is Fraction, "rational density value")
            total += wu * wv * value
    return total * (right - left) * (top - bottom) / 36


def _proper(geometry, u, v):
    return Fraction(geometry["scale"], 2) * (1 + geometry["eta"] * u * v)


def _weighted(geometry, delta, u, v):
    return _proper(geometry, u, v) * (1 + delta * u * v)


def _mass(geometry, delta, rectangle):
    return _integrate(lambda u, v: _weighted(geometry, delta, u, v), rectangle)


def _affine_mass(geometry, rectangle):
    zero = _mass(geometry, Fraction(0), rectangle)
    one = _mass(geometry, Fraction(1), rectangle)
    coefficients = [zero, one - zero]
    _require(
        _mass(geometry, Fraction(2), rectangle) == zero + 2 * coefficients[1],
        "affine mass dependence derived from direct integration",
    )
    return coefficients


def _forward(geometry, delta, regions):
    mass_q = _mass(geometry, delta, regions["Q"])
    mass_i = _mass(geometry, delta, regions["I"])
    _require(0 < mass_i < mass_q, "positive finite full-support point measure")
    return mass_i / mass_q, mass_q, mass_i


def _geometry(descriptor, bounds, regions):
    volume_q = _integrate(lambda u, v: _proper(descriptor, u, v), regions["Q"])
    volume_i = _integrate(lambda u, v: _proper(descriptor, u, v), regions["I"])
    numerator = _affine_mass(descriptor, regions["I"])
    denominator = _affine_mass(descriptor, regions["Q"])
    a, b = numerator
    c, d = denominator
    derivative_numerator = b * c - a * d
    _require(derivative_numerator < 0, "strictly decreasing nonconstant response")
    _require(c > 0 and c + 2 * d > 0, "positive affine mass throughout declared domain")
    ranges = []
    for bound in bounds:
        lower, upper = bound["interval"]
        _require(0 <= lower <= upper <= 2, "declared closed nuisance bound")
        minimum = _forward(descriptor, upper, regions)[0]
        maximum = _forward(descriptor, lower, regions)[0]
        _require(0 < minimum <= maximum < 1, "strict finite-record support over bound")
        for delta, q in ((lower, maximum), (upper, minimum)):
            _require(q * (c + d * delta) == a + b * delta, "direct range/affine map agreement")
        ranges.append({"bound": bound["id"], "delta": [lower, upper], "q": [minimum, maximum]})
    return {
        "id": descriptor["id"],
        "eta": descriptor["eta"],
        "scale": descriptor["scale"],
        "volume_Q": volume_q,
        "volume_I": volume_i,
        "target": volume_i / volume_q,
        "mass_I_coeffs": numerator,
        "mass_Q_coeffs": denominator,
        "derivative_numerator": derivative_numerator,
        "ranges": ranges,
    }


def _quadratic(values):
    first, second, third = values
    quadratic = (third - 2 * second + first) / 2
    return [first, second - first - quadratic, quadratic]


def _point_polynomial(geometry, delta, normalizer, rectangle):
    def density(u, v):
        return _weighted(geometry, delta, u, v) / normalizer

    nodes = [Fraction(0), Fraction(1), Fraction(2)]
    u_coefficients = [_quadratic([density(u, v) for u in nodes]) for v in nodes]
    polynomial = []
    for i in range(3):
        for j, coefficient in enumerate(_quadratic([row[i] for row in u_coefficients])):
            if coefficient:
                polynomial.append([i, j, coefficient])
    for u, _ in _axis(rectangle[0], rectangle[1]):
        for v, _ in _axis(rectangle[2], rectangle[3]):
            reconstructed = sum((value * u**i * v**j for i, j, value in polynomial), Fraction(0))
            _require(reconstructed == density(u, v), "point polynomial interpolation")
    _require(_integrate(density, rectangle) == 1, "point polynomial normalization")
    return polynomial


def _hypothesis(geometry, bound, q, regions):
    attainable = next(row for row in geometry["ranges"] if row["bound"] == bound["id"])
    in_range = attainable["q"][0] <= q <= attainable["q"][1]
    a, b = geometry["mass_I_coeffs"]
    c, d = geometry["mass_Q_coeffs"]
    inverse_numerator = a - q * c
    inverse_denominator = q * d - b
    candidate = []
    delta_set = []
    normalized = []
    mass_q_list = []
    mass_i_list = []
    if inverse_denominator == 0:
        _require(inverse_numerator != 0, "constant-map branch excluded by strict derivative")
        _require(not in_range, "inverse pole cannot lie in attainable range")
    else:
        delta = inverse_numerator / inverse_denominator
        candidate = [delta]
        _require(inverse_denominator * delta == inverse_numerator, "affine inverse certificate")
        lower, upper = bound["interval"]
        _require(in_range == (lower <= delta <= upper), "range-first and closed-bound equivalence")
        if in_range:
            actual_q, mass_q, mass_i = _forward(geometry, delta, regions)
            _require(actual_q == q, "original direct forward law of feasible candidate")
            _require(
                mass_q == c + d * delta and mass_i == a + b * delta,
                "candidate mass/affine consistency",
            )
            delta_set = [delta]
            mass_q_list, mass_i_list = [mass_q], [mass_i]
            normalized = _point_polynomial(geometry, delta, mass_q, regions["Q"])
    return {
        "id": geometry["id"],
        "q_range": list(attainable["q"]),
        "inverse_numerator": inverse_numerator,
        "inverse_denominator": inverse_denominator,
        "candidate": candidate,
        "delta_set": delta_set,
        "status": "feasible" if in_range else "infeasible",
        "normalized_point": normalized,
        "mass_Q": mass_q_list,
        "mass_I": mass_i_list,
    }


def _point_classes(hypotheses, geometries):
    index = {geometry["id"]: geometry for geometry in geometries}
    groups = []
    representatives = []
    feasible = [row for row in hypotheses if row["status"] == "feasible"]
    for row in feasible:
        polynomial = row["normalized_point"]
        destination = next((j for j, old in enumerate(representatives) if old == polynomial), None)
        if destination is None:
            representatives.append(polynomial)
            groups.append({"worlds": [], "targets": [], "identified": False})
            destination = len(groups) - 1
        group = groups[destination]
        group["worlds"].append(row["id"])
        target = index[row["id"]]["target"]
        if target not in group["targets"]:
            group["targets"].append(target)
    for group in groups:
        group["targets"].sort()
        group["identified"] = len(group["targets"]) == 1
    for left in feasible:
        eta_left = Fraction(index[left["id"]]["eta"])
        delta_left = left["delta_set"][0]
        for right in feasible:
            eta_right = Fraction(index[right["id"]]["eta"])
            delta_right = right["delta_set"][0]
            structural = (
                eta_left + delta_left == eta_right + delta_right
                and eta_left * delta_left == eta_right * delta_right
            )
            _require(
                (left["normalized_point"] == right["normalized_point"]) == structural,
                "full normalized point-law equivalence criterion",
            )
    return groups


def _case(bound, datum, geometries, regions):
    hypotheses = [_hypothesis(geometry, bound, datum["q"], regions) for geometry in geometries]
    worlds = [row["id"] for row in hypotheses if row["status"] == "feasible"]
    targets = sorted({geometry["target"] for geometry in geometries if geometry["id"] in worlds})
    status = "infeasible" if not targets else "identified" if len(targets) == 1 else "ambiguous"
    return {
        "id": bound["id"] + "/" + datum["id"],
        "bound": bound["id"],
        "data": datum["id"],
        "q": datum["q"],
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": status,
        "point_classes": _point_classes(hypotheses, geometries),
    }


def _word_rows(q, quota):
    _require(type(q) is Fraction and 0 <= q <= 1, "stipulated population probability")
    rows = []
    for word in product((0, 1), repeat=quota):
        probability = Fraction(1)
        for bit in word:
            probability *= q if bit else 1 - q
        rows.append({"y": list(word), "k": sum(word), "p": probability})
    _require(sum((row["p"] for row in rows), Fraction(0)) == 1, "complete data-law normalization")
    return rows


def _monotonicity(bounds, data, cases):
    index = {case["id"]: case for case in cases}
    rows = []
    for tight, broad in pairwise(bounds):
        _require(
            broad["interval"][0] <= tight["interval"][0]
            and tight["interval"][1] <= broad["interval"][1],
            "nested supplied bounds",
        )
        for datum in data:
            first = index[tight["id"] + "/" + datum["id"]]
            second = index[broad["id"] + "/" + datum["id"]]
            broad_hypotheses = {row["id"]: row for row in second["hypotheses"]}
            world_subset = set(first["worlds"]) <= set(second["worlds"])
            target_subset = set(first["targets"]) <= set(second["targets"])
            preserved = all(
                row["delta_set"] == broad_hypotheses[row["id"]]["delta_set"]
                for row in first["hypotheses"]
                if row["status"] == "feasible"
            )
            _require(
                world_subset and target_subset and preserved,
                "bound tightening preserves surviving solutions",
            )
            rows.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    "world_subset": world_subset,
                    "target_subset": target_subset,
                    "nuisance_preserved": preserved,
                }
            )
    return rows


def _finite_records(bounds, geometries, quota):
    groups = []
    targets = sorted({geometry["target"] for geometry in geometries})
    for bound in bounds:
        compatible = []
        for geometry in geometries:
            attainable = next(row for row in geometry["ranges"] if row["bound"] == bound["id"])
            if 0 < attainable["q"][0] <= attainable["q"][1] < 1:
                compatible.append(geometry["id"])
        strict_support = compatible == [geometry["id"] for geometry in geometries]
        _require(strict_support, "uniformly positive finite-word support for all nuisance values")
        rows = [
            {
                "y": list(word),
                "k": sum(word),
                "frequency": Fraction(sum(word), quota),
                "worlds": list(compatible),
                "targets": list(targets),
            }
            for word in product((0, 1), repeat=quota)
        ]
        groups.append({"bound": bound["id"], "strict_support": strict_support, "rows": rows})
    return groups


def _collisions(cases, geometries, regions, quota, widest):
    geometry_index = {row["id"]: row for row in geometries}
    case_index = {row["id"]: row for row in cases}
    rows = []
    for identifier, data_id, expected_point_equal in (
        ("inherited_whole_point", "overlap", True),
        ("membership_only", "interior", False),
    ):
        case_id = widest + "/" + data_id
        case = case_index[case_id]
        index = {row["id"]: row for row in case["hypotheses"]}
        first, second = index["flat"], index["conformal"]
        _require(
            first["status"] == second["status"] == "feasible", "prespecified collision candidates"
        )
        deltas = [first["delta_set"][0], second["delta_set"][0]]
        # Reintegrate each candidate independently; do not equate their
        # generated laws merely because they share an input data label.
        q_first = _forward(geometry_index["flat"], deltas[0], regions)[0]
        q_second = _forward(geometry_index["conformal"], deltas[1], regions)[0]
        membership_equal = _word_rows(q_first, quota) == _word_rows(q_second, quota)
        point_equal = first["normalized_point"] == second["normalized_point"]
        gap = geometry_index["flat"]["target"] - geometry_index["conformal"]["target"]
        _require(
            membership_equal and point_equal is expected_point_equal and gap != 0,
            "membership versus full-point collision distinction",
        )
        rows.append(
            {
                "id": identifier,
                "case": case_id,
                "worlds": ["flat", "conformal"],
                "deltas": deltas,
                "target_gap": gap,
                "membership_equal": membership_equal,
                "point_equal": point_equal,
            }
        )
    return rows


def _scale_pairs(geometries, cases):
    index = {row["id"]: row for row in geometries}
    rows = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        old, new = index[first], index[second]
        factor = new["volume_Q"] / old["volume_Q"]
        target_equal = old["target"] == new["target"]
        nuisance_equal = True
        points_equal = True
        for case in cases:
            hypotheses = {row["id"]: row for row in case["hypotheses"]}
            left, right = hypotheses[first], hypotheses[second]
            nuisance_equal = nuisance_equal and left["delta_set"] == right["delta_set"]
            points_equal = points_equal and left["normalized_point"] == right["normalized_point"]
        _require(
            factor == Fraction(new["scale"], old["scale"])
            and new["volume_I"] == factor * old["volume_I"],
            "absolute geometric scale factor",
        )
        for field in ("mass_I_coeffs", "mass_Q_coeffs"):
            _require(
                new[field] == [factor * value for value in old[field]],
                "affine mass scale covariance",
            )
        _require(
            target_equal and nuisance_equal and points_equal, "normalized inverse scale ambiguity"
        )
        rows.append(
            {
                "worlds": [first, second],
                "volume_factor": factor,
                "target_equal": target_equal,
                "nuisance_sets_equal": nuisance_equal,
                "point_laws_equal": points_equal,
            }
        )
    return rows


def _native_report(report):
    pending = [report]
    while pending:
        value = pending.pop()
        if type(value) is dict:
            _require(all(type(key) is str for key in value), "native output key")
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
        else:
            _require(type(value) in (Fraction, int, bool, str), "native output value")


def analyze(protocol: dict) -> dict:
    """Full fixed-domain report; no record frequency is promoted to population q."""
    _validate_protocol(protocol)
    regions = {
        key: [_rational(pair) for pair in value] for key, value in protocol["regions"].items()
    }
    bounds = [
        {"id": row["id"], "interval": [_rational(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    data = [{"id": row["id"], "q": _rational(row["q"])} for row in protocol["population_data"]]
    quota = protocol["quota"]
    geometries = [_geometry(row, bounds, regions) for row in protocol["geometries"]]
    cases = [_case(bound, datum, geometries, regions) for bound in bounds for datum in data]
    laws = [
        {"data": datum["id"], "q": datum["q"], "rows": _word_rows(datum["q"], quota)}
        for datum in data
    ]
    monotonicity = _monotonicity(bounds, data, cases)
    finite_records = _finite_records(bounds, geometries, quota)
    collisions = _collisions(cases, geometries, regions, quota, bounds[-1]["id"])
    scale_pairs = _scale_pairs(geometries, cases)
    actual_coverage = {
        "cases": len(cases),
        "hypotheses": sum(len(case["hypotheses"]) for case in cases),
        "laws": len(laws),
        "membership_rows": sum(len(law["rows"]) for law in laws),
        "monotonicity": len(monotonicity),
        "finite_records": sum(len(group["rows"]) for group in finite_records),
        "collisions": len(collisions),
    }
    _require(
        actual_coverage == protocol["coverage"] and len(scale_pairs) == 2, "fixed report coverage"
    )
    report = {
        "schema": "qr05bn-report-v1",
        "geometries": geometries,
        "cases": cases,
        "laws": laws,
        "monotonicity": monotonicity,
        "finite_records": finite_records,
        "collisions": collisions,
        "scale_pairs": scale_pairs,
    }
    _native_report(report)
    return report
