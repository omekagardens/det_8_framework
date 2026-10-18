"""Exact BO monomial geometry, elimination and paired-population inversion.

All mathematical work is deferred to an explicit analyze(protocol) call.
No file access, previous executors or other mathematical routes are used.
"""

from fractions import Fraction as F
from itertools import pairwise, product
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, active=None):
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
            _native(child, active)
    finally:
        active.remove(identity)


def _validate(protocol):
    _native(protocol)
    fixtures = []
    for scale in (1, 4):
        for name, eta, delta in (
            ("flat_0", 0, [0, 1]),
            ("flat_1", 0, [1, 1]),
            ("flat_2", 0, [2, 1]),
            ("flat_interior", 0, [16, 11]),
            ("conformal_0", 1, [0, 1]),
            ("conformal_1", 1, [1, 1]),
            ("conformal_2", 1, [2, 1]),
            ("conformal_interior", 1, [45, 158]),
        ):
            fixtures.append(
                {
                    "id": name + ("_x4" if scale == 4 else ""),
                    "eta": eta,
                    "scale": scale,
                    "delta": delta,
                }
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
        "fixtures": fixtures,
        "fixture_data": [row["id"] for row in fixtures if row["scale"] == 1],
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
    _require(type(protocol) is dict and protocol == expected, "complete fixed BO protocol")


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


def _scale(poly, value):
    return _clean({powers: coefficient * value for powers, coefficient in poly.items()})


def _add(left, right):
    result = dict(left)
    for powers, coefficient in right.items():
        result[powers] = result.get(powers, F(0)) + coefficient
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
    _require(u0 < u1 and v0 < v1, "positive rectangle")
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


def _coefficients(poly):
    _require(all(i == j and 0 <= i <= 2 for i, j in poly), "declared polynomial span")
    return [poly.get((degree, degree), F(0)) for degree in range(3)]


def _dot(left, right):
    _require(len(left) == len(right), "dot-product dimensions")
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def _matmul(left, right):
    return [[_dot(row, list(column)) for column in zip(*right, strict=True)] for row in left]


def _inverse(matrix):
    size = len(matrix)
    _require(size > 0 and all(len(row) == size for row in matrix), "square moment matrix")
    rows = [list(row) + [F(i == j) for j in range(size)] for i, row in enumerate(matrix)]
    determinant = F(1)
    for column in range(size):
        pivot_rows = [i for i in range(column, size) if rows[i][column] != 0]
        _require(bool(pivot_rows), "nonsingular moment matrix")
        pivot_row = pivot_rows[0]
        if pivot_row != column:
            rows[column], rows[pivot_row] = rows[pivot_row], rows[column]
            determinant = -determinant
        pivot = rows[column][column]
        determinant *= pivot
        rows[column] = [value / pivot for value in rows[column]]
        for i in range(size):
            if i != column:
                multiplier = rows[i][column]
                rows[i] = [
                    value - multiplier * basis
                    for value, basis in zip(rows[i], rows[column], strict=True)
                ]
    identity = [[F(i == j) for j in range(size)] for i in range(size)]
    _require([row[:size] for row in rows] == identity, "complete rational elimination")
    return [row[size:] for row in rows], determinant


def _reconstruction(regions):
    moments = [
        [_integrate({(degree, degree): F(1)}, rectangle) for degree in range(3)]
        for rectangle in regions
    ]
    inverse, determinant = _inverse(moments)
    identity = [[F(i == j) for j in range(3)] for i in range(3)]
    left_equal = _matmul(inverse, moments) == identity
    right_equal = _matmul(moments, inverse) == identity
    _require(left_equal and right_equal, "both inverse identities")
    products = []
    for rectangle in regions:
        u0, u1, v0, v1 = rectangle
        _require(u0 == 0 and v0 == 0, "origin-anchored moment domain")
        products.append(u1 * v1)
    vandermonde = F(1, 36)
    for value in products:
        vandermonde *= value
    for i in range(3):
        for j in range(i + 1, 3):
            vandermonde *= products[j] - products[i]
    _require(determinant == vandermonde and determinant != 0, "scaled Vandermonde certificate")
    return {
        "moments": moments,
        "determinant": determinant,
        "inverse": inverse,
        "left_identity": left_equal,
        "right_identity": right_equal,
    }


def _geometry(supplied, regions):
    eta, scale = F(supplied["eta"]), F(supplied["scale"])
    proper = _clean({(0, 0): scale / 2, (1, 1): scale * eta / 2})
    slope = _multiply(proper, {(1, 1): F(1)})
    volumes = [_integrate(proper, rectangle) for rectangle in regions]
    coefficients = [
        [_integrate(poly, rectangle) for poly in (proper, slope)] for rectangle in regions
    ]
    _require(0 < volumes[1] < volumes[2] < volumes[0], "strict positive nested regions")
    # Positive affine coefficients certify these differences for every delta >= 0,
    # not only at the finite validation fixtures.
    for degree in (0, 1):
        _require(
            0 < coefficients[1][degree] < coefficients[2][degree] < coefficients[0][degree],
            "strict continuous support of all three nonzero categories",
        )
    a, b = coefficients[1]
    c, d = coefficients[0]
    _require(b * c - a * d < 0, "nonconstant strictly decreasing first probability")
    return {
        "id": supplied["id"],
        "eta": supplied["eta"],
        "scale": supplied["scale"],
        "proper": proper,
        "slope": slope,
        "volumes": volumes,
        "mass_coefficients": coefficients,
        "target": volumes[1] / volumes[0],
    }


def _weighted(geometry, delta, regions):
    poly = _add(geometry["proper"], _scale(geometry["slope"], delta))
    masses = [_integrate(poly, rectangle) for rectangle in regions]
    affine = [a + b * delta for a, b in geometry["mass_coefficients"]]
    _require(masses == affine, "direct polynomial and affine mass equality")
    _require(0 < masses[1] < masses[2] < masses[0], "admitted positive nested probability")
    normalized = _scale(poly, F(1) / masses[0])
    _require(_integrate(normalized, regions[0]) == 1, "point-law normalization")
    return masses, _coefficients(normalized)


def _one_point(q):
    first, second = q
    _require(
        all(type(value) is F for value in q) and 0 <= first <= second <= 1,
        "nested exact population pair",
    )
    probabilities = [1 - second, second - first, F(0), first]
    _require(sum(probabilities, F(0)) == 1, "complete paired one-point law")
    return probabilities


def _records(probabilities, quota):
    result = []
    symbols = ((0, 0), (0, 1), (1, 0), (1, 1))
    for word in product(symbols, repeat=quota):
        probability = F(1)
        for first, second in word:
            probability *= probabilities[2 * first + second]
        result.append({"y": [list(symbol) for symbol in word], "p": probability})
    _require(sum((row["p"] for row in result), F(0)) == 1, "complete four-attempt law")
    return result


def _marginal(records, first_probability, quota):
    buckets = {word: F(0) for word in product((0, 1), repeat=quota)}
    for row in records:
        key = tuple(pair[0] for pair in row["y"])
        buckets[key] += row["p"]
    marginal = [{"y": list(word), "p": probability} for word, probability in buckets.items()]
    direct = [
        {
            "y": list(word),
            "p": first_probability ** sum(word) * (1 - first_probability) ** (quota - sum(word)),
        }
        for word in product((0, 1), repeat=quota)
    ]
    equal = marginal == direct
    _require(equal, "complete first-query marginal law")
    return marginal, equal


def _world(fixture, geometry, regions, reconstruction, quota):
    delta = _fraction(fixture["delta"])
    _require(0 <= delta <= 2, "fixture density domain")
    masses, normalized = _weighted(geometry, delta, regions)
    q = [masses[index] / masses[0] for index in (1, 2)]
    probabilities = _one_point(q)
    records = _records(probabilities, quota)
    marginal, marginal_equal = _marginal(records, q[0], quota)
    recovered = [_dot(row, [F(1), *q]) for row in reconstruction["inverse"]]
    reconstruction_equal = recovered == normalized
    _require(reconstruction_equal, "moment recovery of the complete normalized polynomial")
    independent_10 = q[0] * (1 - q[1])
    _require(independent_10 > 0 and probabilities[2] == 0, "wrong independent-marginal channel")
    for row in records:
        _require(
            (row["p"] > 0) == all(pair != [1, 0] for pair in row["y"]),
            "full retained structural-zero branch inventory",
        )
    return {
        "id": fixture["id"],
        "eta": fixture["eta"],
        "scale": fixture["scale"],
        "delta": delta,
        "volumes": list(geometry["volumes"]),
        "target": geometry["target"],
        "mass_coefficients": [list(row) for row in geometry["mass_coefficients"]],
        "mass": masses,
        "normalized_coefficients": normalized,
        "q": q,
        "one_point": probabilities,
        "records": records,
        "marginal": marginal,
        "recovered": recovered,
        "reconstruction_equal": reconstruction_equal,
        "marginal_equal": marginal_equal,
        "independent_10": independent_10,
    }


def _datum(identifier, q, reconstruction):
    solution = [_dot(row, [F(1), *q]) for row in reconstruction["inverse"]]
    _require(
        [_dot(row, solution) for row in reconstruction["moments"]] == [F(1), *q],
        "full moment solution, without premature density admission",
    )
    return {"id": identifier, "q": list(q), "moment_solution": solution, "one_point": _one_point(q)}


def _factor_admission(geometry, datum, bound, regions, reconstruction):
    constant, linear, quadratic = datum["moment_solution"]
    if constant <= 0:
        return []
    alpha, beta = linear / constant, quadratic / constant
    delta = alpha - geometry["eta"]
    if beta != geometry["eta"] * delta or not bound[0] <= delta <= bound[1]:
        return []
    masses, coefficients = _weighted(geometry, delta, regions)
    _require(
        coefficients == datum["moment_solution"], "factorized normalization and positive constant"
    )
    _require(
        [masses[index] / masses[0] for index in (1, 2)] == datum["q"]
        and [_dot(row, coefficients) for row in reconstruction["moments"]] == [F(1), *datum["q"]],
        "both factorized forward probabilities",
    )
    return [delta]


def _hypothesis(geometry, datum, bound, regions, reconstruction):
    first, second = datum["q"]
    a, b = geometry["mass_coefficients"][1]
    c, d = geometry["mass_coefficients"][0]
    numerator, denominator = a - c * first, d * first - b
    candidate, delta_set, residual, normalized = [], [], [], []
    if denominator == 0:
        _require(numerator != 0, "constant-map inverse is outside this family")
    else:
        delta = numerator / denominator
        candidate = [delta]
        _require(denominator * delta == numerator, "raw first-query inverse")
        if bound[0] <= delta <= bound[1]:
            masses, coefficients = _weighted(geometry, delta, regions)
            _require(masses[1] == first * masses[0], "first-query forward substitution")
            residual = [masses[2] - second * masses[0]]
            if residual[0] == 0:
                delta_set = [delta]
                normalized = coefficients
                _require(
                    normalized == datum["moment_solution"],
                    "admitted full coefficient reconstruction",
                )
    factor_set = _factor_admission(geometry, datum, bound, regions, reconstruction)
    _require(delta_set == factor_set, "continuous inverse and moment factorization admission agree")
    return {
        "id": geometry["id"],
        "inverse_numerator": numerator,
        "inverse_denominator": denominator,
        "candidate": candidate,
        "delta_set": delta_set,
        "status": "feasible" if delta_set else "infeasible",
        "second_residual": residual,
        "normalized_coefficients": normalized,
    }


def _case(bound, datum, geometries, regions, reconstruction):
    hypotheses = [
        _hypothesis(geometry, datum, bound["interval"], regions, reconstruction)
        for geometry in geometries
    ]
    targets_by_id = {geometry["id"]: geometry["target"] for geometry in geometries}
    worlds = [row["id"] for row in hypotheses if row["delta_set"]]
    targets = sorted({targets_by_id[name] for name in worlds})
    return {
        "id": bound["id"] + "/" + datum["id"],
        "bound": bound["id"],
        "data": datum["id"],
        "q": list(datum["q"]),
        "hypotheses": hypotheses,
        "worlds": worlds,
        "targets": targets,
        "status": "infeasible"
        if not worlds
        else "identified"
        if len(targets) == 1
        else "ambiguous",
    }


def _classes(worlds, field):
    values, groups = [], []
    by_id = {world["id"]: world for world in worlds}
    for world in worlds:
        value = world[field]
        if value not in values:
            values.append(value)
            groups.append([])
        groups[values.index(value)].append(world["id"])
    result = []
    for group in groups:
        targets = sorted({by_id[name]["target"] for name in group})
        result.append({"worlds": list(group), "targets": targets, "identified": len(targets) == 1})
    return result


def _collisions(worlds):
    by_id = {world["id"]: world for world in worlds}
    result = []
    for name, ids in (
        ("inherited_whole_point", ["flat_1", "conformal_0"]),
        ("membership_only", ["flat_interior", "conformal_interior"]),
    ):
        left, right = [by_id[identifier] for identifier in ids]
        first_equal = left["marginal"] == right["marginal"]
        joint_equal = left["records"] == right["records"]
        point_equal = left["normalized_coefficients"] == right["normalized_coefficients"]
        gap = left["target"] - right["target"]
        _require(first_equal and gap != 0, "declared first-query target collision")
        if name == "inherited_whole_point":
            _require(
                point_equal and joint_equal, "whole-point equality survives the common channel"
            )
        result.append(
            {
                "id": name,
                "worlds": list(ids),
                "first_equal": first_equal,
                "joint_equal": joint_equal,
                "point_equal": point_equal,
                "q2_gap": left["q"][1] - right["q"][1],
                "target_gap": gap,
            }
        )
    return result


def _scale_pairs(worlds):
    by_id = {world["id"]: world for world in worlds}
    result = []
    for left in worlds:
        if left["scale"] != 1:
            continue
        right = by_id[left["id"] + "_x4"]
        factor = right["volumes"][0] / left["volumes"][0]
        _require(factor == F(right["scale"], left["scale"]), "declared metric scaling")
        for index in range(3):
            _require(
                right["volumes"][index] == factor * left["volumes"][index]
                and right["mass"][index] == factor * left["mass"][index]
                and right["mass_coefficients"][index]
                == [factor * value for value in left["mass_coefficients"][index]],
                "all regions retain proper-volume and sampling-mass scaling",
            )
        target_equal = left["target"] == right["target"]
        point_equal = left["normalized_coefficients"] == right["normalized_coefficients"]
        joint_equal = left["records"] == right["records"]
        _require(
            target_equal and point_equal and joint_equal and left["q"] == right["q"],
            "scale remains unobserved",
        )
        result.append(
            {
                "worlds": [left["id"], right["id"]],
                "volume_factor": factor,
                "target_equal": target_equal,
                "point_equal": point_equal,
                "joint_equal": joint_equal,
            }
        )
    return result


def _monotonicity(bounds, data, cases):
    by_id = {case["id"]: case for case in cases}
    result = []
    for tight, broad in pairwise(bounds):
        _require(
            broad["interval"][0]
            <= tight["interval"][0]
            <= tight["interval"][1]
            <= broad["interval"][1],
            "nested external acquisition bounds",
        )
        for datum in data:
            left = by_id[tight["id"] + "/" + datum["id"]]
            right = by_id[broad["id"] + "/" + datum["id"]]
            world_subset = set(left["worlds"]) <= set(right["worlds"])
            target_subset = set(left["targets"]) <= set(right["targets"])
            right_deltas = {row["id"]: row["delta_set"] for row in right["hypotheses"]}
            nuisance_preserved = all(
                row["delta_set"] == right_deltas[row["id"]]
                for row in left["hypotheses"]
                if row["delta_set"]
            )
            _require(
                world_subset and target_subset and nuisance_preserved,
                "bound inclusion preserves surviving nuisance",
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


def _support(geometries, bounds, quota):
    _require(
        all(0 <= row["interval"][0] <= row["interval"][1] <= 2 for row in bounds),
        "positive-density support domain",
    )
    # _geometry certified all three category masses positive for every delta >= 0.
    labels = [geometry["id"] for geometry in geometries]
    targets = sorted({geometry["target"] for geometry in geometries})
    result = []
    symbols = ((0, 0), (0, 1), (1, 0), (1, 1))
    for word in product(symbols, repeat=quota):
        possible = all(symbol != (1, 0) for symbol in word)
        result.append(
            {
                "y": [list(symbol) for symbol in word],
                "possible": possible,
                "worlds": list(labels) if possible else [],
                "targets": list(targets) if possible else [],
            }
        )
    _require(
        sum(row["possible"] for row in result) == 3**quota, "full continuous structural support"
    )
    return result


def _native_report(value):
    if type(value) in (str, int, bool, F):
        return
    _require(type(value) in (dict, list), "unsupported report type")
    if type(value) is dict:
        _require(all(type(key) is str for key in value), "native report keys")
    for child in value.values() if type(value) is dict else value:
        _native_report(child)


def analyze(protocol):
    """Produce the fixed report from public definitions, not prior numerical results."""
    _validate(protocol)
    regions = [
        [_fraction(pair) for pair in protocol["regions"][name]] for name in ("Q", "I1", "I2")
    ]
    bounds = [
        {"id": row["id"], "interval": [_fraction(pair) for pair in row["interval"]]}
        for row in protocol["density_bounds"]
    ]
    reconstruction = _reconstruction(regions)
    geometries = [_geometry(row, regions) for row in protocol["geometries"]]
    geometry_keys = {(row["eta"], row["scale"]): row for row in geometries}
    worlds = [
        _world(
            row,
            geometry_keys[(row["eta"], row["scale"])],
            regions,
            reconstruction,
            protocol["quota"],
        )
        for row in protocol["fixtures"]
    ]
    by_world = {row["id"]: row for row in worlds}
    data = [
        _datum(identifier, by_world[identifier]["q"], reconstruction)
        for identifier in protocol["fixture_data"]
    ]
    data.extend(
        _datum(row["id"], [_fraction(pair) for pair in row["q"]], reconstruction)
        for row in protocol["control_data"]
    )
    cases = [
        _case(bound, datum, geometries, regions, reconstruction)
        for bound in bounds
        for datum in data
    ]
    classes = {
        "first": _classes(worlds, "marginal"),
        "joint": _classes(worlds, "records"),
        "point": _classes(worlds, "normalized_coefficients"),
    }
    _require(
        classes["joint"] == classes["point"],
        "joint queries identify the normalized polynomial within the declared span",
    )
    collisions = _collisions(worlds)
    scales = _scale_pairs(worlds)
    monotonicity = _monotonicity(bounds, data, cases)
    support = _support(geometries, bounds, protocol["quota"])
    coverage = {
        "worlds": len(worlds),
        "records": sum(len(row["records"]) for row in worlds),
        "marginals": sum(len(row["marginal"]) for row in worlds),
        "data": len(data),
        "cases": len(cases),
        "hypotheses": sum(len(row["hypotheses"]) for row in cases),
        "monotonicity": len(monotonicity),
        "support": len(support),
        "collisions": len(collisions),
        "scale_pairs": len(scales),
    }
    _require(coverage == protocol["coverage"], "complete fixed verification inventory")
    report = {
        "schema": "qr05bo-report-v1",
        "reconstruction": reconstruction,
        "worlds": worlds,
        "data": data,
        "cases": cases,
        "classes": classes,
        "collisions": collisions,
        "scale_pairs": scales,
        "monotonicity": monotonicity,
        "support": support,
    }
    _native_report(report)
    return report
