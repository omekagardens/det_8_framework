"""Exact global-admission refinement with a self-contained BG model.

Only definitions are evaluated at import.  Local helpers are statically adapted
from the preceding primary; no old executor or stored result is imported.
"""

from fractions import Fraction as F
from itertools import product
from math import comb


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if value is None or kind in (int, str):
        return
    _require(kind in (dict, list), "native protocol containers and scalars required")
    identity = id(value)
    _require(identity not in active, "cyclic protocol")
    if kind is dict:
        _require(all(type(k) is str for k in value), "native protocol keys required")
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native(child, active)
    finally:
        active.remove(identity)


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected protocol fields")


def _fraction(value):
    _require(type(value) is str, "protocol rational must be a string")
    try:
        answer = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid protocol rational") from exc
    _require(str(answer) == value, "canonical protocol rational required")
    return answer


def _polarization(value):
    answer = _fraction(value)
    _require(-1 <= answer <= 1, "polarization outside physical state domain")
    return answer


def _poly_add(left, right):
    answer = dict(left)
    for powers, value in right.items():
        answer[powers] = answer.get(powers, F(0)) + value
    return {powers: value for powers, value in answer.items() if value}


def _poly_scale(poly, scale):
    return {powers: scale * value for powers, value in poly.items() if scale * value}


def _poly_multiply(left, right):
    answer = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            powers = (i + k, j + ell)
            answer[powers] = answer.get(powers, F(0)) + a * b
    return {powers: value for powers, value in answer.items() if value}


def _poly_value(poly, u, v):
    return sum((coefficient * u**i * v**j for (i, j), coefficient in poly.items()), F(0))


def _integral(poly, bounds, measure):
    u0, u1, v0, v1 = bounds
    return measure * sum(
        (
            coefficient
            * (u1 ** (i + 1) - u0 ** (i + 1))
            / (i + 1)
            * (v1 ** (j + 1) - v0 ** (j + 1))
            / (j + 1)
            for (i, j), coefficient in poly.items()
        ),
        F(0),
    )


def _base_geometry(protocol):
    supplied = protocol["geometry"]
    bounds = [*map(_fraction, supplied["u"]), *map(_fraction, supplied["v"])]
    measure = _fraction(supplied["measure_factor"])
    u0, u1, v0, v1 = bounds
    one = {(0, 0): F(1)}
    u, v = {(1, 0): F(1)}, {(0, 1): F(1)}
    xi = _poly_scale(_poly_add(u, {(0, 0): -u0}), 1 / (u1 - u0))
    zeta = _poly_scale(_poly_add(v, {(0, 0): -v0}), 1 / (v1 - v0))
    xbar, zbar = _poly_add(one, _poly_scale(xi, -1)), _poly_add(one, _poly_scale(zeta, -1))
    basis = [
        _poly_multiply(xbar, zbar),
        _poly_multiply(xi, zbar),
        _poly_multiply(xbar, zeta),
        _poly_multiply(xi, zeta),
    ]
    kernel = _poly_scale(
        _poly_multiply(
            _poly_add({(0, 0): u1}, _poly_scale(u, -1)), _poly_add({(0, 0): v1}, _poly_scale(v, -1))
        ),
        measure,
    )
    volume = _integral(one, bounds, measure)
    sigma = volume**4
    normalization = volume**2 / sigma
    weights = [normalization * _integral(_poly_multiply(b, kernel), bounds, measure) for b in basis]
    coordinates = [(u0, v0), (u1, v0), (u0, v1), (u1, v1)]
    _require(all(w >= 0 for w in weights), "nonnegative geometric basis weights")
    _require(
        sum(weights, F(0)) == normalization * _integral(kernel, bounds, measure), "weight partition"
    )
    return (
        bounds,
        measure,
        basis,
        kernel,
        coordinates,
        normalization,
        {
            "volume": volume,
            "sigma": sigma,
            "weights": weights,
            "weight_sum": sum(weights, F(0)),
        },
    )


def _identity(size):
    return {(i, i): F(1) for i in range(size)}


def _matrix_scale(matrix, scale):
    return {position: scale * value for position, value in matrix.items() if scale * value}


def _matrix_add(left, right):
    result = dict(left)
    for position, value in right.items():
        result[position] = result.get(position, F(0)) + value
    return {position: value for position, value in result.items() if value}


def _adjoint(matrix):
    # All declared matrices are real rational; transpose is the full adjoint.
    return {(j, i): value for (i, j), value in matrix.items()}


def _matrix_multiply(left, right):
    by_row = {}
    for (i, j), value in right.items():
        by_row.setdefault(i, []).append((j, value))
    result = {}
    for (i, k), a in left.items():
        for j, b in by_row.get(k, ()):
            position = (i, j)
            result[position] = result.get(position, F(0)) + a * b
    return {position: value for position, value in result.items() if value}


def _tensor(left, left_size, right, right_size):
    return {
        (i * right_size + k, j * right_size + ell): a * b
        for (i, j), a in left.items()
        for (k, ell), b in right.items()
        if a * b
    }, left_size * right_size


def _diagonal(matrix, size):
    _require(
        all(
            0 <= i < size and 0 <= j < size and (i == j or not value)
            for (i, j), value in matrix.items()
        ),
        "unexpected off-diagonal entry or matrix index",
    )
    return [matrix.get((i, i), F(0)) for i in range(size)]


def _trace(matrix, size):
    return sum((matrix.get((i, i), F(0)) for i in range(size)), F(0))


def _state(mean):
    _require(-1 <= mean <= 1, "physical qubit polarization")
    z = {(0, 0): F(1), (1, 1): F(-1)}
    state = _matrix_add(_matrix_scale(_identity(2), F(1, 2)), _matrix_scale(z, mean / 2))
    _require(all(x >= 0 for x in _diagonal(state, 2)) and _trace(state, 2) == 1, "density state")
    return state


def _projector(outcome):
    _require(type(outcome) is int and outcome in (-1, 1), "projector outcome")
    z = {(0, 0): F(1), (1, 1): F(-1)}
    projector = _matrix_add(_matrix_scale(_identity(2), F(1, 2)), _matrix_scale(z, F(outcome, 2)))
    _require(_matrix_multiply(projector, projector) == projector, "projector idempotence")
    return projector


def _tensor_state(means):
    result, size = _identity(1), 1
    for mean in means:
        result, size = _tensor(result, size, _state(mean), 2)
    _require(
        _trace(result, size) == 1 and all(x >= 0 for x in _diagonal(result, size)), "tensor density"
    )
    return result, size


def _local_operator(station, outcome, count):
    result, size = _identity(1), 1
    for index in range(count):
        result, size = _tensor(
            result, size, _projector(outcome) if index == station else _identity(2), 2
        )
    return result


def _instrument(count):
    """Construct only the canonical complete local instrument for this gate."""
    size = 2**count
    local = {(i, x): _local_operator(i, x, count) for i in range(count) for x in (-1, 1)}
    matrices, completeness = [], {}
    for record in product((-1, 1), repeat=count):
        operator = _identity(size)
        for station in range(count):
            operator = _matrix_multiply(local[(station, record[station])], operator)
        _diagonal(operator, size)
        matrices.append(operator)
        completeness = _matrix_add(completeness, _matrix_multiply(_adjoint(operator), operator))
    _require(completeness == _identity(size), "complete outcome instrument")
    return matrices


def _branches(means, matrices):
    state, size = _tensor_state(means)
    probabilities, diagonals, branches = [], [], []
    for operator in matrices:
        branch = _matrix_multiply(_matrix_multiply(operator, state), _adjoint(operator))
        diagonal = _diagonal(branch, size)
        probability = _trace(branch, size)
        _require(probability >= 0 and all(x >= 0 for x in diagonal), "positive unnormalized branch")
        _require(sum(diagonal, F(0)) == probability, "branch trace")
        probabilities.append(probability)
        diagonals.append(diagonal)
        branches.append(branch)
    _require(sum(probabilities, F(0)) == 1, "normalized complete record law")
    return probabilities, diagonals, branches


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def _moments(probabilities, values):
    mean = _dot(probabilities, values)
    return mean, sum(
        (p * (x - mean) ** 2 for p, x in zip(probabilities, values, strict=True)), F(0)
    )


def _validate(protocol):
    _native(protocol)
    _fields(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "geometry",
            "stations",
            "corners",
            "outcomes",
            "positions",
            "menus",
            "cases",
            "profile_rule",
            "admission_rule",
            "inverse_rule",
            "position_rule",
            "set_rule",
            "hull_rule",
            "gap_probe_rule",
            "disclosure_rule",
            "witnesses",
            "domain_control",
            "third_oracle",
            "public_boundary",
            "comparison",
            "no_claims",
        ),
    )
    _require(protocol["study"] == "QR-05BG" and protocol["version"] == 1, "protocol version")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometric conventions",
    )
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station roles")
    _require(
        protocol["corners"] == [["0", "0"], ["1", "0"], ["0", "1"], ["1", "1"]],
        "fixed corner positions",
    )
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    positions = protocol["positions"]
    _require(type(positions) is list and len(positions) == 6, "six candidate positions")
    position_ids = []
    for position in positions:
        _fields(position, ("id", "position"))
        _require(type(position["id"]) is str and position["id"], "position identifier")
        _require(
            type(position["position"]) is list and len(position["position"]) == 2,
            "two position coordinates",
        )
        _require(
            all(0 < _fraction(x) < 1 for x in position["position"]), "strictly interior position"
        )
        position_ids.append(position["id"])
    _require(len(set(position_ids)) == len(position_ids), "unique position identifiers")
    menus = protocol["menus"]
    _require(type(menus) is list and len(menus) == 5, "five finite menus")
    menu_ids = []
    for menu in menus:
        _fields(menu, ("id", "position_ids"))
        _require(type(menu["id"]) is str and menu["id"], "menu identifier")
        names = menu["position_ids"]
        _require(
            type(names) is list and names and all(type(name) is str for name in names),
            "nonempty ordered position menu",
        )
        _require(
            len(set(names)) == len(names) and all(name in position_ids for name in names),
            "distinct known menu positions",
        )
        menu_ids.append(menu["id"])
    _require(len(set(menu_ids)) == len(menu_ids), "unique menu identifiers")
    _require(
        menus[0]["id"] == "all" and menus[0]["position_ids"] == position_ids,
        "first menu exhausts all declared positions",
    )
    cases = protocol["cases"]
    _require(type(cases) is list and len(cases) == 7, "seven population cases")
    case_ids = []
    for case in cases:
        _fields(case, ("id", "population_means"))
        _require(type(case["id"]) is str and case["id"], "case identifier")
        _require(
            type(case["population_means"]) is list and len(case["population_means"]) == 5,
            "five role-labeled population means",
        )
        for mean in case["population_means"]:
            _polarization(mean)
        case_ids.append(case["id"])
    _require(len(set(case_ids)) == len(case_ids), "unique public case identifiers")
    witnesses = protocol["witnesses"]
    _require(type(witnesses) is list and len(witnesses) == 2, "two declared witnesses")
    witness_ids = []
    for witness in witnesses:
        _fields(witness, ("id", "case_id", "position_ids"))
        _require(type(witness["id"]) is str and witness["id"], "witness identifier")
        _require(witness["case_id"] in case_ids, "witness public case")
        names = witness["position_ids"]
        _require(
            type(names) is list
            and len(names) == 2
            and all(type(x) is str for x in names)
            and names[0] != names[1]
            and all(x in position_ids for x in names),
            "witness positions",
        )
        witness_ids.append(witness["id"])
    _require(witness_ids == ["target_ambiguity", "harmless_position_ambiguity"], "witness order")
    control = protocol["domain_control"]
    _fields(control, ("case_id", "position_id", "rule"))
    _require(
        control["case_id"] in case_ids and control["position_id"] in position_ids,
        "domain-control references",
    )


def _admission(corners, theta):
    return max(map(abs, corners)) + abs(theta) / 16


def _dense_product(left, right):
    columns = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in columns] for row in left]


def _dense_identity(size):
    return [[F(i == j) for j in range(size)] for i in range(size)]


def _inverse(matrix):
    size = len(matrix)
    identity = _dense_identity(size)
    rows = [list(row) + list(identity[i]) for i, row in enumerate(matrix)]
    for column in range(size):
        pivots = [i for i in range(column, size) if rows[i][column]]
        _require(bool(pivots), "population evaluation map is singular")
        pivot = pivots[0]
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [entry / scale for entry in rows[column]]
        for i in range(size):
            if i != column:
                multiplier = rows[i][column]
                rows[i] = [a - multiplier * b for a, b in zip(rows[i], rows[column], strict=True)]
    answer = [row[size:] for row in rows]
    _require([row[:size] for row in rows] == identity, "complete rational elimination")
    _require(_dense_product(matrix, answer) == identity, "evaluation times decoder identity")
    _require(_dense_product(answer, matrix) == identity, "decoder times evaluation identity")
    return answer


def _model_polynomial(corners, theta, basis, bubble):
    profile = _poly_scale(bubble, theta)
    for coefficient, phi in zip(corners, basis, strict=True):
        profile = _poly_add(profile, _poly_scale(phi, coefficient))
    return profile


def _compile_geometry(protocol):
    bounds, measure, basis, kernel, corners, normalization, old = _base_geometry(protocol)
    bubble = _poly_multiply(basis[0], basis[3])
    q = [
        normalization * _integral(_poly_multiply(function, kernel), bounds, measure)
        for function in [*basis, bubble]
    ]
    _require(q[:4] == old["weights"], "complete geometric coefficient integrals")
    _require(q[4] > 0, "target is injective in the remaining bubble coefficient")
    return (
        {
            "volume": old["volume"],
            "sigma": old["sigma"],
            "coefficient_integrals": q,
        },
        bounds,
        measure,
        basis,
        bubble,
        kernel,
        corners,
        normalization,
    )


def _position(supplied, q, basis, bubble, corners):
    position = [_fraction(value) for value in supplied["position"]]
    sites = [*corners, position]
    a = [[_poly_value(function, *site) for function in [*basis, bubble]] for site in sites]
    decoder = _inverse(a)
    left, right = _dense_product(decoder, a), _dense_product(a, decoder)
    _require(left == right == _dense_identity(5), "two-sided population inverse")
    weights = _dense_product([q], decoder)[0]
    residual = [x - y for x, y in zip(_dense_product([weights], a)[0], q, strict=True)]
    _require(all(value == 0 for value in residual), "full target compilation")
    _require(a[4][4] > 0, "strict interior basis response")
    return {
        "id": supplied["id"],
        "position": position,
        "basis": list(a[4]),
        "evaluation_matrix": a,
        "coefficient_decoder": decoder,
        "left_inverse": left,
        "right_inverse": right,
        "full_weights": weights,
        "full_residual": residual,
    }, sites


def _law(means, instrument):
    probabilities, diagonals, branches = _branches(means, instrument)
    rows = [
        {
            "outcomes": list(outcome),
            "probability": probability,
            "state_diagonal": list(diagonal),
        }
        for outcome, probability, diagonal in zip(
            product((-1, 1), repeat=5), probabilities, diagonals, strict=True
        )
    ]
    averaged = {}
    for branch in branches:
        averaged = _matrix_add(averaged, branch)
    original, size = _tensor_state(means)
    _require(size == 32 and averaged == original, "complete outcome-averaged internal state")
    return {"rows": rows, "averaged_state": _diagonal(averaged, size)}


def _candidate(means, position, sites, q, polynomial_data, instrument):
    bounds, measure, basis, bubble, kernel, normalization = polynomial_data
    coefficients = [_dot(row, means) for row in position["coefficient_decoder"]]
    corners, theta = coefficients[:4], coefficients[4]
    independent_theta = (means[4] - _dot(position["basis"][:4], means[:4])) / position["basis"][4]
    _require(corners == means[:4] and theta == independent_theta, "independent block inversion")
    profile = _model_polynomial(corners, theta, basis, bubble)
    reconstructed = [_poly_value(profile, *site) for site in sites]
    residual = [a - b for a, b in zip(reconstructed, means, strict=True)]
    _require(all(value == 0 for value in residual), "polynomial reconstruction of public means")
    _require(
        [_dot(row, coefficients) for row in position["evaluation_matrix"]] == reconstructed,
        "polynomial versus population response",
    )
    target = normalization * _integral(_poly_multiply(profile, kernel), bounds, measure)
    _require(
        target == _dot(q, coefficients) == _dot(position["full_weights"], means),
        "integrated candidate target and compiled response",
    )
    bound = _admission(corners, theta)
    admitted = bound <= 1
    # Even a rejected global hypothesis can have valid local means. Reconstruct
    # those means first, then execute the physical local instrument independently.
    law = _law(reconstructed, instrument)
    return {
        "position_id": position["id"],
        "coefficients": coefficients,
        "admission_bound": bound,
        "admission_status": "admitted" if admitted else "outside_sufficient_class",
        "reconstructed_means": reconstructed,
        "reconstruction_residual": residual,
        "target": target,
        "law": law,
        "disclosure": {
            "status": "identified" if admitted else "infeasible",
            "target": target if admitted else None,
        },
    }


def _menu(supplied, candidates):
    lookup = {candidate["position_id"]: candidate for candidate in candidates}
    feasible = []
    for name in supplied["position_ids"]:
        candidate = lookup[name]
        admitted = candidate["admission_bound"] <= 1
        _require(
            admitted == (candidate["admission_status"] == "admitted"),
            "admission is the only filter",
        )
        if admitted:
            feasible.append(
                {
                    "position_id": name,
                    "coefficients": list(candidate["coefficients"]),
                    "target": candidate["target"],
                }
            )
    targets = sorted({row["target"] for row in feasible})
    if not targets:
        status, target_range, gap = "infeasible", None, None
    else:
        status = "identified" if len(targets) == 1 else "ambiguous"
        if status == "identified":
            _require(
                all(row["coefficients"] == feasible[0]["coefficients"] for row in feasible),
                "identified target and fixed corners also identify coefficients",
            )
        target_range = {
            "minimum": targets[0],
            "maximum": targets[-1],
            "width": targets[-1] - targets[0],
        }
        gap = None if len(targets) == 1 else (targets[0] + targets[1]) / 2
        if gap is not None:
            _require(
                targets[0] < gap < targets[1] and gap not in targets,
                "fixed gap probe is outside the exact target set",
            )
    return {
        "id": supplied["id"],
        "position_ids": list(supplied["position_ids"]),
        "feasible": feasible,
        "distinct_targets": targets,
        "target_range": target_range,
        "gap_probe": gap,
        "status": status,
    }


def _menus(supplied, candidates):
    reports = [_menu(menu, candidates) for menu in supplied]
    complete = {row["position_id"]: row for row in reports[0]["feasible"]}
    all_targets = set(reports[0]["distinct_targets"])
    for report in reports:
        filtered = [complete[name] for name in report["position_ids"] if name in complete]
        _require(report["feasible"] == filtered, "menu restriction equals exhaustive filtering")
        _require(
            set(report["distinct_targets"]).issubset(all_targets),
            "menu restriction cannot add targets",
        )
        for feasible in report["feasible"]:
            candidate = next(
                row for row in candidates if row["position_id"] == feasible["position_id"]
            )
            _require(
                candidate["disclosure"] == {"status": "identified", "target": feasible["target"]},
                "exact-position disclosure and feasible entry",
            )
    return reports


def _witness(supplied, cases):
    case = next(row for row in cases if row["id"] == supplied["case_id"])
    lookup = {row["position_id"]: row for row in case["candidates"]}
    first, second = (lookup[name] for name in supplied["position_ids"])
    _require(
        first["admission_status"] == second["admission_status"] == "admitted",
        "ambiguity witnesses must be globally admitted",
    )
    coefficient_difference = [
        b - a for a, b in zip(first["coefficients"], second["coefficients"], strict=True)
    ]
    means_difference = [
        b - a
        for a, b in zip(first["reconstructed_means"], second["reconstructed_means"], strict=True)
    ]
    target_difference = second["target"] - first["target"]
    law_tv = (
        sum(
            (
                abs(b["probability"] - a["probability"])
                for a, b in zip(first["law"]["rows"], second["law"]["rows"], strict=True)
            ),
            F(0),
        )
        / 2
    )
    disagreements = sum(
        a["state_diagonal"] != b["state_diagonal"]
        for a, b in zip(first["law"]["rows"], second["law"]["rows"], strict=True)
    )
    state_difference = [
        b - a
        for a, b in zip(
            first["law"]["averaged_state"], second["law"]["averaged_state"], strict=True
        )
    ]
    _require(
        all(value == 0 for value in means_difference)
        and law_tv == 0
        and disagreements == 0
        and all(value == 0 for value in state_difference),
        "complete role-labeled observational collision",
    )
    if supplied["id"] == "target_ambiguity":
        _require(
            target_difference != 0 and any(value != 0 for value in coefficient_difference),
            "position/profile collision changes the target",
        )
    else:
        _require(target_difference == 0, "harmless position ambiguity preserves target")
    _require(
        all(row["disclosure"]["status"] == "identified" for row in (first, second)),
        "disclosed witness hypotheses remain admitted",
    )
    return {
        "id": supplied["id"],
        "case_id": supplied["case_id"],
        "position_ids": list(supplied["position_ids"]),
        "admission_bounds": [first["admission_bound"], second["admission_bound"]],
        "coefficients_difference": coefficient_difference,
        "means_difference": means_difference,
        "target_difference": target_difference,
        "law_total_variation": law_tv,
        "branch_state_disagreements": disagreements,
        "averaged_state_difference": state_difference,
        "disclosed_targets": [first["disclosure"]["target"], second["disclosure"]["target"]],
    }


def _domain_control(supplied, cases, positions, polynomial_data):
    bounds, _measure, basis, bubble, _kernel, _normalization = polynomial_data
    case = next(row for row in cases if row["id"] == supplied["case_id"])
    candidate = next(
        row for row in case["candidates"] if row["position_id"] == supplied["position_id"]
    )
    position = next(row for row in positions if row["id"] == supplied["position_id"])
    coefficients = candidate["coefficients"]
    _require(
        coefficients[:4] == [F(1)] * 4 and coefficients[4] == -16,
        "specific valid-but-excluded polynomial",
    )
    u0, u1, v0, v1 = bounds
    minimum_position = [(u0 + u1) / 2, (v0 + v1) / 2]
    maximum_position = [u0, v0]
    _require(position["position"] == minimum_position, "declared center domain-control hypothesis")
    one = {(0, 0): F(1)}
    u, v = {(1, 0): F(1)}, {(0, 1): F(1)}
    u_factor = _poly_multiply(u, _poly_add(one, _poly_scale(u, -1)))
    v_factor = _poly_multiply(v, _poly_add(one, _poly_scale(v, -1)))
    u_center = _poly_add(u, {(0, 0): -minimum_position[0]})
    v_center = _poly_add(v, {(0, 0): -minimum_position[1]})
    quarter = minimum_position[0] * (1 - minimum_position[0])
    # On [0,1], each x(1-x) is nonnegative and equals 1/4-(x-1/2)^2.
    # Multiplication gives the global bubble enclosure; center/corner attain it.
    _require(
        _poly_add(u_factor, _poly_multiply(u_center, u_center)) == {(0, 0): quarter},
        "u-factor exact maximum identity",
    )
    _require(
        _poly_add(v_factor, _poly_multiply(v_center, v_center)) == {(0, 0): quarter},
        "v-factor exact maximum identity",
    )
    _require(_poly_multiply(u_factor, v_factor) == bubble, "factorized nonnegative bubble")
    bubble_range = [F(0), quarter**2]
    _require(
        _poly_value(bubble, *maximum_position) == bubble_range[0]
        and _poly_value(bubble, *minimum_position) == bubble_range[1],
        "attained bubble range",
    )
    profile = _model_polynomial(coefficients[:4], coefficients[4], basis, bubble)
    _require(profile == _poly_add(one, _poly_scale(bubble, coefficients[4])), "exact 1-16b control")
    profile_range = [
        F(1) + coefficients[4] * bubble_range[1],
        F(1) + coefficients[4] * bubble_range[0],
    ]
    _require(-1 <= profile_range[0] <= profile_range[1] <= 1, "globally physical excluded profile")
    _require(
        _poly_value(profile, *minimum_position) == profile_range[0]
        and _poly_value(profile, *maximum_position) == profile_range[1],
        "attained profile range",
    )
    _require(
        candidate["admission_bound"] > 1
        and candidate["admission_status"] == "outside_sufficient_class"
        and candidate["disclosure"] == {"status": "infeasible", "target": None},
        "conservative admission is not physical invalidity",
    )
    return {
        "case_id": supplied["case_id"],
        "position_id": supplied["position_id"],
        "coefficients": list(coefficients),
        "admission_bound": candidate["admission_bound"],
        "admission_status": candidate["admission_status"],
        "bubble_range": bubble_range,
        "profile_range": profile_range,
        "minimum_position": minimum_position,
        "maximum_position": maximum_position,
    }


def _analyze_bg(protocol):
    """Return the exhaustive finite population certificate; no work on import."""
    _validate(protocol)
    geometry, bounds, measure, basis, bubble, kernel, corners, normalization = _compile_geometry(
        protocol
    )
    polynomial_data = bounds, measure, basis, bubble, kernel, normalization
    positions, sites = [], {}
    for supplied in protocol["positions"]:
        report, coordinates = _position(
            supplied, geometry["coefficient_integrals"], basis, bubble, corners
        )
        positions.append(report)
        sites[report["id"]] = coordinates
    instrument = _instrument(5)
    cases = []
    for supplied in protocol["cases"]:
        means = [_polarization(value) for value in supplied["population_means"]]
        public_law = _law(means, instrument)
        candidates = []
        for position in positions:
            candidate = _candidate(
                means,
                position,
                sites[position["id"]],
                geometry["coefficient_integrals"],
                polynomial_data,
                instrument,
            )
            _require(
                candidate["law"] == public_law, "independently reconstructed complete local law"
            )
            candidates.append(candidate)
        cases.append(
            {
                "id": supplied["id"],
                "population_means": means,
                "law": public_law,
                "candidates": candidates,
                "menus": _menus(protocol["menus"], candidates),
            }
        )
    return {
        "geometry": geometry,
        "positions": positions,
        "cases": cases,
        "witnesses": [_witness(witness, cases) for witness in protocol["witnesses"]],
        "domain_control": _domain_control(
            protocol["domain_control"], cases, positions, polynomial_data
        ),
    }


def _validate_refinement(protocol):
    _native(protocol)
    _fields(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "model",
            "certificate",
            "set_rule",
            "existence_rule",
            "target_rule",
            "exactness_rule",
            "comparison",
            "no_claims",
        ),
    )
    _require(
        protocol["study"] == "QR-05BH" and protocol["version"] == 1, "refinement protocol version"
    )
    _validate(protocol["model"])
    certificate = protocol["certificate"]
    _fields(
        certificate,
        (
            "degree",
            "local_nodes",
            "root",
            "leaves",
            "witness_points",
            "coefficient_order",
            "reconstruction_rule",
            "classification_rule",
            "root_rule",
            "witness_rule",
        ),
    )
    _require(certificate["degree"] == [2, 2], "fixed tensor polynomial degree")
    _require(certificate["local_nodes"] == ["0", "1/2", "1"], "fixed unisolvent nodes")
    expected = [
        ("root", [["0", "1"], ["0", "1"]]),
        ("ll", [["0", "1/2"], ["0", "1/2"]]),
        ("lh", [["0", "1/2"], ["1/2", "1"]]),
        ("hl", [["1/2", "1"], ["0", "1/2"]]),
        ("hh", [["1/2", "1"], ["1/2", "1"]]),
    ]
    _require(
        type(certificate["leaves"]) is list and len(certificate["leaves"]) == 4,
        "four covering fixed leaves",
    )
    for patch, (name, bounds) in zip(
        [certificate["root"], *certificate["leaves"]], expected, strict=True
    ):
        _fields(patch, ("id", "bounds"))
        _require(patch["id"] == name and patch["bounds"] == bounds, "fixed covering partition")
    nodes = certificate["local_nodes"]
    _require(
        certificate["witness_points"] == [[u, v] for u in nodes for v in nodes],
        "fixed physical witness grid",
    )


def _refinement_polynomial(coefficients):
    _require(len(coefficients) == 5, "five profile coefficients")
    one = {(0, 0): F(1)}
    u, v = {(1, 0): F(1)}, {(0, 1): F(1)}
    ubar = _poly_add(one, _poly_scale(u, -1))
    vbar = _poly_add(one, _poly_scale(v, -1))
    basis = [
        _poly_multiply(ubar, vbar),
        _poly_multiply(u, vbar),
        _poly_multiply(ubar, v),
        _poly_multiply(u, v),
    ]
    bubble = _poly_multiply(basis[0], basis[3])
    result = _model_polynomial(coefficients[:4], coefficients[4], basis, bubble)
    _require(all(0 <= i <= 2 and 0 <= j <= 2 for i, j in result), "declared bidegree bound")
    return result


def _affine_power(poly, bounds):
    """Coefficients of f(a+(b-a)s,c+(d-c)t), from binomial substitution."""
    (a, b), (c, d) = bounds
    width, height = b - a, d - c
    _require(width > 0 and height > 0, "positive patch rectangle")
    local = {}
    for (i, j), coefficient in poly.items():
        for p in range(i + 1):
            for q in range(j + 1):
                value = (
                    coefficient
                    * comb(i, p)
                    * a ** (i - p)
                    * width**p
                    * comb(j, q)
                    * c ** (j - q)
                    * height**q
                )
                local[p, q] = local.get((p, q), F(0)) + value
    return {powers: value for powers, value in local.items() if value}


def _power_to_bernstein(local):
    # s^p = sum_{i>=p} binom(i,p)/binom(2,p) B_i(s), independently per axis.
    return [
        [
            sum(
                (
                    coefficient * F(comb(i, p), comb(2, p)) * F(comb(j, q), comb(2, q))
                    for (p, q), coefficient in local.items()
                    if p <= i and q <= j
                ),
                F(0),
            )
            for j in range(3)
        ]
        for i in range(3)
    ]


def _bernstein_values(x):
    return [F(comb(2, i)) * x**i * (1 - x) ** (2 - i) for i in range(3)]


def _patch(supplied, poly, nodes):
    bounds = [[_fraction(value) for value in axis] for axis in supplied["bounds"]]
    local = _affine_power(poly, bounds)
    coefficients = _power_to_bernstein(local)
    (a, b), (c, d) = bounds
    residual = []
    for s in nodes:
        row = []
        bu = _bernstein_values(s)
        for t in nodes:
            bv = _bernstein_values(t)
            represented = sum(
                (coefficients[i][j] * bu[i] * bv[j] for i in range(3) for j in range(3)), F(0)
            )
            original = _poly_value(poly, a + (b - a) * s, c + (d - c) * t)
            _require(original == _poly_value(local, s, t), "exact affine monomial substitution")
            row.append(original - represented)
        residual.append(row)
    _require(
        all(value == 0 for row in residual for value in row),
        "complete unisolvent Bernstein reconstruction",
    )
    flat = [value for row in coefficients for value in row]
    bound = [min(flat), max(flat)]
    within = -1 <= bound[0] and bound[1] <= 1
    return {
        "id": supplied["id"],
        "bounds": bounds,
        "coefficients": coefficients,
        "reconstruction_residual": residual,
        "range_bound": bound,
        "bound_status": "within" if within else "outside",
    }


def _classification(old_admitted, subdivision_within, violating_indices):
    """Internal semantic helper; its tuple is unpacked before report retention."""
    _require(
        type(old_admitted) is bool and type(subdivision_within) is bool,
        "internal certification flags",
    )
    _require(
        type(violating_indices) is list
        and all(type(index) is int and index >= 0 for index in violating_indices),
        "internal violation indices",
    )
    routes = []
    if old_admitted:
        routes.append("old_bound")
    if subdivision_within:
        routes.append("subdivision_bernstein")
    _require(
        not (routes and violating_indices), "global certification conflicts with actual violation"
    )
    if routes:
        classification = "certified"
    elif violating_indices:
        classification = "refuted"
    else:
        classification = "unresolved"
    return classification, routes


def _refinement_candidate(candidate, certificate):
    coefficients = candidate["coefficients"]
    poly = _refinement_polynomial(coefficients)
    nodes = [_fraction(value) for value in certificate["local_nodes"]]
    root = _patch(certificate["root"], poly, nodes)
    leaves = [_patch(leaf, poly, nodes) for leaf in certificate["leaves"]]
    leaf_values = [value for leaf in leaves for row in leaf["coefficients"] for value in row]
    _require(
        all(root["range_bound"][0] <= value <= root["range_bound"][1] for value in leaf_values),
        "root net encloses every subdivided coefficient",
    )
    subdivision_bound = [min(leaf_values), max(leaf_values)]
    within = all(leaf["bound_status"] == "within" for leaf in leaves)
    _require(
        within == (-1 <= subdivision_bound[0] and subdivision_bound[1] <= 1),
        "covering leaf classification and enclosure",
    )
    _require(root["bound_status"] != "within" or within, "root success implies leaf success")
    witnesses, violating = [], []
    for index, supplied in enumerate(certificate["witness_points"]):
        point = [_fraction(value) for value in supplied]
        value = _poly_value(poly, *point)
        violation = abs(value) > 1
        if violation:
            violating.append(index)
        witnesses.append(
            {"position": point, "value": value, "status": "violation" if violation else "within"}
        )
    old_admitted = candidate["admission_bound"] <= 1
    _require(
        old_admitted == (candidate["admission_status"] == "admitted")
        and candidate["admission_bound"] == _admission(coefficients[:4], coefficients[4]),
        "preserved old sufficient admission",
    )
    classification, routes = _classification(old_admitted, within, violating)
    return {
        "position_id": candidate["position_id"],
        "coefficients": list(coefficients),
        "target": candidate["target"],
        "old_admission_status": candidate["admission_status"],
        "root": root,
        "leaves": leaves,
        "subdivision_range_bound": subdivision_bound,
        "subdivision_status": "within" if within else "outside",
        "witnesses": witnesses,
        "violating_indices": violating,
        "certificate_routes": routes,
        "classification": classification,
    }


def _target_range(targets):
    if not targets:
        return None
    return {"minimum": targets[0], "maximum": targets[-1], "width": targets[-1] - targets[0]}


def _refinement_menus(menus, candidates):
    """Generic finite set semantics; only minimal candidate fields are consumed."""
    lookup = {}
    for candidate in candidates:
        name = candidate["position_id"]
        _require(type(name) is str and name and name not in lookup, "distinct candidate labels")
        _require(
            candidate["old_admission_status"] in ("admitted", "outside_sufficient_class"),
            "old admission classification",
        )
        _require(
            candidate["classification"] in ("certified", "refuted", "unresolved"),
            "three-way refinement classification",
        )
        _require(
            candidate["old_admission_status"] != "admitted"
            or candidate["classification"] == "certified",
            "preserved old certificate",
        )
        lookup[name] = candidate
    reports, names = [], set()
    for menu in menus:
        _require(
            type(menu["id"]) is str and menu["id"] and menu["id"] not in names,
            "distinct menu labels",
        )
        names.add(menu["id"])
        position_ids = menu["position_ids"]
        _require(
            type(position_ids) is list
            and all(type(name) is str and name in lookup for name in position_ids)
            and len(set(position_ids)) == len(position_ids),
            "finite known menu hypotheses",
        )
        layers = {"old": [], "inner": [], "outer": []}
        for name in position_ids:
            candidate = lookup[name]
            for layer, include in (
                ("old", candidate["old_admission_status"] == "admitted"),
                ("inner", candidate["classification"] == "certified"),
                ("outer", candidate["classification"] != "refuted"),
            ):
                if include:
                    layers[layer].append(
                        {
                            "position_id": name,
                            "coefficients": list(candidate["coefficients"]),
                            "target": candidate["target"],
                        }
                    )
        old_ids, inner_ids, outer_ids = (
            {row["position_id"] for row in layers[key]} for key in ("old", "inner", "outer")
        )
        _require(
            old_ids.issubset(inner_ids) and inner_ids.issubset(outer_ids),
            "nested hypothesis bounds",
        )
        targets = {key: sorted({row["target"] for row in rows}) for key, rows in layers.items()}
        if not layers["outer"]:
            existence = target_status = "infeasible"
        else:
            existence = "feasible" if layers["inner"] else "unresolved"
            if layers["inner"] and len(targets["outer"]) == 1:
                target_status = "identified"
            elif len(targets["inner"]) >= 2:
                target_status = "ambiguous"
            else:
                target_status = "unresolved"
        reports.append(
            {
                "id": menu["id"],
                "position_ids": list(position_ids),
                "old": layers["old"],
                "inner": layers["inner"],
                "outer": layers["outer"],
                "old_targets": targets["old"],
                "inner_targets": targets["inner"],
                "outer_targets": targets["outer"],
                "inner_range": _target_range(targets["inner"]),
                "outer_range": _target_range(targets["outer"]),
                "existence_status": existence,
                "target_status": target_status,
                "hypothesis_set_status": "exact"
                if layers["inner"] == layers["outer"]
                else "bounded",
                "target_set_status": "exact" if targets["inner"] == targets["outer"] else "bounded",
            }
        )
    for smaller in reports:
        for larger in reports:
            if set(smaller["position_ids"]).issubset(larger["position_ids"]):
                for layer in ("old", "inner", "outer"):
                    pool = {row["position_id"]: row for row in larger[layer]}
                    filtered = [pool[name] for name in smaller["position_ids"] if name in pool]
                    _require(
                        smaller[layer] == filtered, "every menu restriction is exact filtering"
                    )
                    _require(
                        set(smaller[layer + "_targets"]).issubset(larger[layer + "_targets"]),
                        "menu restriction cannot enlarge target bounds",
                    )
    return reports


def analyze(protocol):
    """Recompute the complete BG model, then apply the fixed global certificates."""
    _validate_refinement(protocol)
    bg_model = _analyze_bg(protocol["model"])
    refinement = []
    for case in bg_model["cases"]:
        candidates = [
            _refinement_candidate(candidate, protocol["certificate"])
            for candidate in case["candidates"]
        ]
        menus = _refinement_menus(protocol["model"]["menus"], candidates)
        for old_menu, refined_menu in zip(case["menus"], menus, strict=True):
            _require(
                old_menu["id"] == refined_menu["id"]
                and old_menu["feasible"] == refined_menu["old"]
                and old_menu["distinct_targets"] == refined_menu["old_targets"],
                "original BG finite-class answers preserved",
            )
        refinement.append({"id": case["id"], "candidates": candidates, "menus": menus})
    return {"bg_model": bg_model, "refinement": refinement}
