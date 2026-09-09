"""Independent BO direct quadrature, cofactor reconstruction and factorization.

No file access, historical executor import or fixed mathematical evaluation
occurs on import. The finite fixtures validate, but do not define, admission.
"""

from fractions import Fraction
from itertools import pairwise, product


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _validate_protocol(protocol):
    base_fixtures = (
        ("flat_0", 0, [0, 1]),
        ("flat_1", 0, [1, 1]),
        ("flat_2", 0, [2, 1]),
        ("flat_interior", 0, [16, 11]),
        ("conformal_0", 1, [0, 1]),
        ("conformal_1", 1, [1, 1]),
        ("conformal_2", 1, [2, 1]),
        ("conformal_interior", 1, [45, 158]),
    )
    expected = {
        "schema": "qr05bo-protocol-v1",
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
        "fixtures": [
            {
                "id": name + ("_x4" if scale == 4 else ""),
                "eta": eta,
                "scale": scale,
                "delta": list(delta),
            }
            for scale in (1, 4)
            for name, eta, delta in base_fixtures
        ],
        "fixture_data": [name for name, _, _ in base_fixtures],
        "control_data": [
            {"id": "zero", "q": [[0, 1], [0, 1]]},
            {"id": "one", "q": [[1, 1], [1, 1]]},
            {"id": "equal", "q": [[1, 4], [1, 4]]},
            {"id": "zero_constant", "q": [[1, 16], [9, 64]]},
        ],
        "density_bounds": [
            {"id": "uniform", "interval": [[0, 1], [0, 1]]},
            {"id": "half", "interval": [[0, 1], [1, 2]]},
            {"id": "one", "interval": [[0, 1], [1, 1]]},
            {"id": "two", "interval": [[0, 1], [2, 1]]},
        ],
        "observer": {
            "schema": "qr05bo-query-v1",
            "data_kind": "population_pair",
            "bound_basis": "external_assumption",
            "integer_cap": 2147483647,
        },
        "coverage": {
            "worlds": 16,
            "records": 4096,
            "marginals": 256,
            "data": 12,
            "cases": 48,
            "hypotheses": 192,
            "monotonicity": 36,
            "support": 256,
            "collisions": 2,
            "scale_pairs": 8,
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
        type(lower) is Fraction and type(upper) is Fraction and lower < upper,
        "exact positive interval",
    )
    return ((lower, 1), ((lower + upper) / 2, 4), (upper, 1))


def _integrate(function, rectangle):
    left, right, bottom, top = rectangle
    total = Fraction(0)
    for u, wu in _axis(left, right):
        for v, wv in _axis(bottom, top):
            value = function(u, v)
            _require(type(value) is Fraction, "rational quadrature integrand")
            total += wu * wv * value
    return total * (right - left) * (top - bottom) / 36


def _dot(left, right):
    _require(len(left) == len(right), "dot-product width")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _matmul(left, right):
    return [[_dot(row, column) for column in zip(*right)] for row in left]


def _cofactor_inverse(matrix):
    _require(
        len(matrix) == 3 and all(len(row) == 3 for row in matrix), "three-dimensional moment map"
    )
    cofactors = []
    for i in range(3):
        row = []
        for j in range(3):
            rows = [r for r in range(3) if r != i]
            columns = [c for c in range(3) if c != j]
            minor = (
                matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
                - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
            )
            row.append((-1) ** (i + j) * minor)
        cofactors.append(row)
    determinant = _dot(matrix[0], cofactors[0])
    _require(determinant != 0, "moment functionals must be independent")
    inverse = [[cofactors[j][i] / determinant for j in range(3)] for i in range(3)]
    return determinant, inverse


def _reconstruction(regions):
    moments = [
        [
            _integrate(lambda u, v, degree=degree: (u * v) ** degree, rectangle)
            for degree in range(3)
        ]
        for rectangle in regions
    ]
    determinant, inverse = _cofactor_inverse(moments)
    identity = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    left = _matmul(inverse, moments) == identity
    right = _matmul(moments, inverse) == identity
    _require(left and right, "both cofactor inverse identities")
    return {
        "moments": moments,
        "determinant": determinant,
        "inverse": inverse,
        "left_identity": left,
        "right_identity": right,
    }


def _proper(geometry, u, v):
    return Fraction(geometry["scale"], 2) * (1 + geometry["eta"] * u * v)


def _weighted(geometry, delta, u, v):
    return _proper(geometry, u, v) * (1 + delta * u * v)


def _mass(geometry, delta, regions):
    return [
        _integrate(lambda u, v: _weighted(geometry, delta, u, v), rectangle)
        for rectangle in regions
    ]


def _geometry(geometry, regions):
    volumes = [_integrate(lambda u, v: _proper(geometry, u, v), rectangle) for rectangle in regions]
    zero = _mass(geometry, Fraction(0), regions)
    one = _mass(geometry, Fraction(1), regions)
    coefficients = [[a, b - a] for a, b in zip(zero, one)]
    for delta in (Fraction(0), Fraction(2)):
        mass = _mass(geometry, delta, regions)
        _require(mass == [row[0] + delta * row[1] for row in coefficients], "affine direct masses")
        _require(0 < mass[1] < mass[2] < mass[0], "positive nested category masses")
    # Each category mass is affine in delta and positive at both endpoints;
    # this proves continuous-domain support, not just support on fixtures.
    a, b = coefficients[1]
    c, d = coefficients[0]
    _require(b * c - a * d < 0 and c > 0 and c + 2 * d > 0, "nonconstant first-query map")
    return {
        "id": geometry["id"],
        "eta": geometry["eta"],
        "scale": geometry["scale"],
        "volumes": volumes,
        "target": volumes[1] / volumes[0],
        "mass_coefficients": coefficients,
    }


def _quadratic(values):
    first, second, third = values
    square = (third - 2 * second + first) / 2
    return [first, second - first - square, square]


def _point_coefficients(geometry, delta, normalizer, region):
    def density(u, v):
        return _weighted(geometry, delta, u, v) / normalizer

    nodes = [Fraction(0), Fraction(1), Fraction(2)]
    first = [_quadratic([density(u, v) for u in nodes]) for v in nodes]
    coefficients = [Fraction(0), Fraction(0), Fraction(0)]
    for i in range(3):
        for j, value in enumerate(_quadratic([row[i] for row in first])):
            if i == j:
                coefficients[i] = value
            else:
                _require(value == 0, "point density lies in declared monomial span")
    for u, _ in _axis(region[0], region[1]):
        for v, _ in _axis(region[2], region[3]):
            _require(
                sum(
                    (value * (u * v) ** degree for degree, value in enumerate(coefficients)),
                    Fraction(0),
                )
                == density(u, v),
                "direct point-density interpolation",
            )
    _require(_integrate(density, region) == 1, "direct normalized point density")
    return coefficients


def _one_point(q):
    first, second = q
    _require(
        type(first) is Fraction and type(second) is Fraction and 0 <= first <= second <= 1,
        "nested population pair",
    )
    probabilities = [1 - second, second - first, Fraction(0), first]
    _require(sum(probabilities, Fraction(0)) == 1, "one-point normalization")
    return probabilities


def _word_product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _records(one_point, quota):
    symbols = ((0, 0), (0, 1), (1, 0), (1, 1))
    rows = []
    for word in product(range(4), repeat=quota):
        rows.append(
            {
                "y": [list(symbols[index]) for index in word],
                "p": _word_product(one_point[index] for index in word),
            }
        )
    _require(sum((row["p"] for row in rows), Fraction(0)) == 1, "full paired-record law")
    return rows


def _marginal(records, q1, quota):
    totals = {word: Fraction(0) for word in product((0, 1), repeat=quota)}
    for row in records:
        totals[tuple(pair[0] for pair in row["y"])] += row["p"]
    marginal = [{"y": list(word), "p": probability} for word, probability in totals.items()]
    independent = [
        {"y": list(word), "p": _word_product(q1 if bit else 1 - q1 for bit in word)}
        for word in product((0, 1), repeat=quota)
    ]
    return marginal, marginal == independent


def _world(fixture, geometry, regions, reconstruction, quota):
    delta = _fraction(fixture["delta"])
    _require(0 <= delta <= 2, "fixture belongs to continuous family")
    mass = _mass(geometry, delta, regions)
    _require(0 < mass[1] < mass[2] < mass[0], "positive proper nested probabilities")
    q = [mass[1] / mass[0], mass[2] / mass[0]]
    coefficients = _point_coefficients(geometry, delta, mass[0], regions[0])
    recovered = _matvec(reconstruction["inverse"], [Fraction(1), *q])
    reconstruction_equal = recovered == coefficients
    _require(reconstruction_equal, "moment reconstruction of full normalized density")
    one_point = _one_point(q)
    records = _records(one_point, quota)
    marginal, marginal_equal = _marginal(records, q[0], quota)
    _require(marginal_equal, "old membership law preserved by marginalization")
    independent_10 = q[0] * (1 - q[1])
    _require(independent_10 > 0 and one_point[2] == 0, "reject independent-question shortcut")
    return {
        "id": fixture["id"],
        "eta": fixture["eta"],
        "scale": fixture["scale"],
        "delta": delta,
        "volumes": list(geometry["volumes"]),
        "target": geometry["target"],
        "mass_coefficients": [list(row) for row in geometry["mass_coefficients"]],
        "mass": mass,
        "normalized_coefficients": coefficients,
        "q": q,
        "one_point": one_point,
        "records": records,
        "marginal": marginal,
        "recovered": recovered,
        "reconstruction_equal": reconstruction_equal,
        "marginal_equal": marginal_equal,
        "independent_10": independent_10,
    }


def _data(protocol, worlds, reconstruction, regions):
    index = {world["id"]: world for world in worlds}
    inputs = [(identifier, list(index[identifier]["q"])) for identifier in protocol["fixture_data"]]
    inputs.extend(
        (row["id"], [_fraction(value) for value in row["q"]]) for row in protocol["control_data"]
    )
    rows = []
    for identifier, q in inputs:
        solution = _matvec(reconstruction["inverse"], [Fraction(1), *q])
        _require(
            _matvec(reconstruction["moments"], solution) == [Fraction(1), *q],
            "moment solution does not assert geometric admission",
        )
        if identifier == "zero_constant":
            supplied_density = [
                _integrate(lambda u, v: 4 * u * v, rectangle) for rectangle in regions
            ]
            _require(
                supplied_density == [Fraction(1), *q] and solution[0] == 0,
                "declared nonfamily zero-constant control",
            )
        rows.append(
            {"id": identifier, "q": q, "moment_solution": solution, "one_point": _one_point(q)}
        )
    return rows


def _factorization(geometry, solution, q, bound, regions):
    """Admission uses only moment reconstruction and its geometric factorization."""
    admitted, normalized = [], []
    if solution[0] > 0:
        eta = Fraction(geometry["eta"])
        linear_ratio, square_ratio = solution[1] / solution[0], solution[2] / solution[0]
        delta = linear_ratio - eta
        lower, upper = bound["interval"]
        if lower <= delta <= upper and square_ratio == eta * delta:
            mass = _mass(geometry, delta, regions)
            _require(
                mass[0] > 0 and [mass[1] / mass[0], mass[2] / mass[0]] == q,
                "factorization must certify both original forwards",
            )
            normalized = _point_coefficients(geometry, delta, mass[0], regions[0])
            _require(normalized == solution, "factorization normalization and full coefficients")
            admitted = [delta]
    return admitted, normalized


def _hypothesis(geometry, datum, bound, regions):
    q1, q2 = datum["q"]
    admitted, normalized = _factorization(
        geometry, datum["moment_solution"], datum["q"], bound, regions
    )
    a, b = geometry["mass_coefficients"][1]
    c, d = geometry["mass_coefficients"][0]
    numerator, denominator = a - c * q1, d * q1 - b
    candidate, residual, diagnostic_admission = [], [], []
    if denominator == 0:
        _require(numerator != 0, "guard nonconstant inverse pole")
    else:
        delta = numerator / denominator
        candidate = [delta]
        _require(denominator * delta == numerator, "first-query inverse diagnostic")
        if bound["interval"][0] <= delta <= bound["interval"][1]:
            mass = _mass(geometry, delta, regions)
            _require(
                mass[0] > 0 and mass[1] == q1 * mass[0], "bound-admitted first-query diagnostic"
            )
            residual = [mass[2] - q2 * mass[0]]
            if residual[0] == 0:
                diagnostic_admission = [delta]
    _require(
        admitted == diagnostic_admission, "independent factorization/inverse admission agreement"
    )
    return {
        "id": geometry["id"],
        "inverse_numerator": numerator,
        "inverse_denominator": denominator,
        "candidate": candidate,
        "delta_set": admitted,
        "status": "feasible" if admitted else "infeasible",
        "second_residual": residual,
        "normalized_coefficients": normalized,
    }


def _case(bound, datum, geometries, regions):
    hypotheses = [_hypothesis(geometry, datum, bound, regions) for geometry in geometries]
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({geometry["target"] for geometry in geometries if geometry["id"] in worlds})
    status = "infeasible" if not targets else "identified" if len(targets) == 1 else "ambiguous"
    return {
        "id": bound["id"] + "/" + datum["id"],
        "bound": bound["id"],
        "data": datum["id"],
        "q": list(datum["q"]),
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": status,
    }


def _class_key(world, field):
    if field == "point":
        return world["normalized_coefficients"]
    return [row["p"] for row in world["marginal" if field == "first" else "records"]]


def _classes(worlds, field):
    representatives, classes = [], []
    for world in worlds:
        key = _class_key(world, field)
        destination = next((j for j, old in enumerate(representatives) if old == key), None)
        if destination is None:
            representatives.append(key)
            classes.append({"worlds": [], "targets": [], "identified": False})
            destination = len(classes) - 1
        group = classes[destination]
        group["worlds"].append(world["id"])
        if world["target"] not in group["targets"]:
            group["targets"].append(world["target"])
    for group in classes:
        group["targets"].sort()
        group["identified"] = len(group["targets"]) == 1
    return classes


def _collisions(worlds):
    index = {world["id"]: world for world in worlds}
    rows = []
    for identifier, pair in (
        ("inherited_whole_point", ("flat_1", "conformal_0")),
        ("membership_only", ("flat_interior", "conformal_interior")),
    ):
        left, right = (index[name] for name in pair)
        first_equal = _class_key(left, "first") == _class_key(right, "first")
        joint_equal = _class_key(left, "joint") == _class_key(right, "joint")
        point_equal = _class_key(left, "point") == _class_key(right, "point")
        q2_gap = left["q"][1] - right["q"][1]
        _require(
            first_equal and joint_equal == point_equal and joint_equal == (q2_gap == 0),
            "richer-channel collision comparison",
        )
        if identifier == "inherited_whole_point":
            _require(point_equal, "whole-point collision cannot be split by a common channel")
        rows.append(
            {
                "id": identifier,
                "worlds": list(pair),
                "first_equal": first_equal,
                "joint_equal": joint_equal,
                "point_equal": point_equal,
                "q2_gap": q2_gap,
                "target_gap": left["target"] - right["target"],
            }
        )
    return rows


def _scale_pairs(worlds, original_ids):
    index = {world["id"]: world for world in worlds}
    rows = []
    for identifier in original_ids:
        left, right = index[identifier], index[identifier + "_x4"]
        factor = right["volumes"][0] / left["volumes"][0]
        _require(
            factor == Fraction(right["scale"], left["scale"])
            and right["volumes"] == [factor * value for value in left["volumes"]],
            "consistent absolute-volume scale in all three regions",
        )
        target_equal = left["target"] == right["target"]
        point_equal = left["normalized_coefficients"] == right["normalized_coefficients"]
        joint_equal = left["records"] == right["records"]
        _require(target_equal and point_equal and joint_equal, "normalized scale obstruction")
        rows.append(
            {
                "worlds": [identifier, identifier + "_x4"],
                "volume_factor": factor,
                "target_equal": target_equal,
                "point_equal": point_equal,
                "joint_equal": joint_equal,
            }
        )
    return rows


def _monotonicity(bounds, data, cases):
    index = {case["id"]: case for case in cases}
    rows = []
    for tight, broad in pairwise(bounds):
        _require(
            broad["interval"][0] <= tight["interval"][0]
            and tight["interval"][1] <= broad["interval"][1],
            "nested external bounds",
        )
        for datum in data:
            first = index[tight["id"] + "/" + datum["id"]]
            second = index[broad["id"] + "/" + datum["id"]]
            world_subset = set(first["worlds"]) <= set(second["worlds"])
            target_subset = set(first["targets"]) <= set(second["targets"])
            broad_rows = {row["id"]: row for row in second["hypotheses"]}
            nuisance_preserved = all(
                row["delta_set"] == broad_rows[row["id"]]["delta_set"]
                for row in first["hypotheses"]
                if row["delta_set"]
            )
            _require(world_subset and target_subset and nuisance_preserved, "bound monotonicity")
            rows.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    "world_subset": world_subset,
                    "target_subset": target_subset,
                    "nuisance_preserved": nuisance_preserved,
                }
            )
    return rows


def _support(geometries, quota):
    labels = [geometry["id"] for geometry in geometries]
    targets = sorted({geometry["target"] for geometry in geometries})
    symbols = ((0, 0), (0, 1), (1, 0), (1, 1))
    rows = []
    for word in product(symbols, repeat=quota):
        possible = all(symbol != (1, 0) for symbol in word)
        rows.append(
            {
                "y": [list(symbol) for symbol in word],
                "possible": possible,
                "worlds": list(labels) if possible else [],
                "targets": list(targets) if possible else [],
            }
        )
    return rows


def _native_report(report):
    pending = [report]
    while pending:
        value = pending.pop()
        if type(value) is dict:
            _require(all(type(key) is str for key in value), "native report key")
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
        else:
            _require(type(value) in (Fraction, int, bool, str), "native report scalar")


def analyze(protocol: dict) -> dict:
    _validate_protocol(protocol)
    quota = protocol["quota"]
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    reconstruction = _reconstruction(regions)
    geometries = [_geometry(row, regions) for row in protocol["geometries"]]
    geometry_index = {(row["eta"], row["scale"]): row for row in geometries}
    worlds = [
        _world(
            fixture,
            geometry_index[(fixture["eta"], fixture["scale"])],
            regions,
            reconstruction,
            quota,
        )
        for fixture in protocol["fixtures"]
    ]
    data = _data(protocol, worlds, reconstruction, regions)
    cases = [_case(bound, datum, geometries, regions) for bound in bounds for datum in data]
    classes = {field: _classes(worlds, field) for field in ("first", "joint", "point")}
    _require(
        classes["joint"] == classes["point"],
        "joint moments identify the declared point-density span",
    )
    collisions = _collisions(worlds)
    scale_pairs = _scale_pairs(worlds, protocol["fixture_data"])
    monotonicity = _monotonicity(bounds, data, cases)
    support = _support(geometries, quota)
    coverage = {
        "worlds": len(worlds),
        "records": sum(len(world["records"]) for world in worlds),
        "marginals": sum(len(world["marginal"]) for world in worlds),
        "data": len(data),
        "cases": len(cases),
        "hypotheses": sum(len(case["hypotheses"]) for case in cases),
        "monotonicity": len(monotonicity),
        "support": len(support),
        "collisions": len(collisions),
        "scale_pairs": len(scale_pairs),
    }
    _require(coverage == protocol["coverage"], "fixed report coverage")
    report = {
        "schema": "qr05bo-report-v1",
        "reconstruction": reconstruction,
        "worlds": worlds,
        "data": data,
        "cases": cases,
        "classes": classes,
        "collisions": collisions,
        "scale_pairs": scale_pairs,
        "monotonicity": monotonicity,
        "support": support,
    }
    _native_report(report)
    return report
