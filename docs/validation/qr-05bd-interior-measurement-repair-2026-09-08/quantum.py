"""Exact five-station model repair using sparse quantum operations.

Only definitions are evaluated at import.  Local helpers are statically adapted
from the preceding primary; no old executor or stored result is imported.
"""

from fractions import Fraction as F
from itertools import permutations, product


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


def _operators(count, outcomes):
    size = 2**count
    local = {(i, x): _local_operator(i, x, count) for i in range(count) for x in (-1, 1)}
    orders = list(permutations(range(count)))
    rows, matrices = [], []
    completeness = {}
    for record in outcomes:
        canonical = None
        for order in orders:
            kraus = _identity(size)
            for station in order:
                kraus = _matrix_multiply(local[(station, record[station])], kraus)
            diagonal = _diagonal(kraus, size)
            if canonical is None:
                canonical = kraus
            _require(kraus == canonical, "station schedule changes the complete Kraus operator")
            _require(diagonal == _diagonal(canonical, size), "canonical basis action")
        matrices.append(canonical)
        rows.append({"outcomes": list(record), "kraus_diagonal": _diagonal(canonical, size)})
        completeness = _matrix_add(completeness, _matrix_multiply(_adjoint(canonical), canonical))
    _require(completeness == _identity(size), "complete outcome instrument")
    return matrices, rows, len(orders)


def _branches(means, matrices):
    state, size = _tensor_state(means)
    probabilities, diagonals = [], []
    for operator in matrices:
        branch = _matrix_multiply(_matrix_multiply(operator, state), _adjoint(operator))
        diagonal = _diagonal(branch, size)
        probability = _trace(branch, size)
        _require(probability >= 0 and all(x >= 0 for x in diagonal), "positive unnormalized branch")
        _require(sum(diagonal, F(0)) == probability, "branch trace")
        probabilities.append(probability)
        diagonals.append(diagonal)
    _require(sum(probabilities, F(0)) == 1, "normalized complete record law")
    return probabilities, diagonals


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
            "coordinates",
            "outcomes",
            "profile_rule",
            "admission_rule",
            "profiles",
            "plans",
            "off_model",
            "global_controls",
            "schedule_control",
            "decomposition_control",
            "score_rule",
            "third_oracle",
            "public_context",
            "record_keys",
            "observer_orders",
            "public_estimator_input",
            "zero_weight_policy",
            "comparison",
            "no_claims",
        ),
    )
    _require(protocol["study"] == "QR-05BD" and protocol["version"] == 1, "protocol version")
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station order")
    _require(protocol["outcomes"] == [-1, 1], "binary outcome order")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometry conventions",
    )
    sites = protocol["coordinates"]
    _require(type(sites) is list and len(sites) == 5, "five supplied sites")
    for site in sites:
        _require(type(site) is list and len(site) == 2, "site coordinates")
        for value in site:
            _fraction(value)
    _require(sites[:4] == [["0", "0"], ["1", "0"], ["0", "1"], ["1", "1"]], "corner locations")
    _require(sites[4] == ["1/2", "1/2"], "declared center station")
    profiles = protocol["profiles"]
    _require(type(profiles) is list and len(profiles) == 10, "ten admitted profiles")
    identifiers = []
    for profile in profiles:
        _fields(profile, ("id", "corners", "theta"))
        corners, theta = _parameters(profile)
        _require(_admission(corners, theta) <= 1, "outside the sufficient profile domain")
        identifiers.append(profile["id"])
    _require(len(set(identifiers)) == len(identifiers), "unique profile identifiers")
    plans = protocol["plans"]
    _require(type(plans) is list and len(plans) == 3, "three fixed plans")
    required = [
        ("corner4", [["00", 1], ["10", 1], ["01", 1], ["11", 1]], "corner", 4),
        ("repair5", [["00", 1], ["10", 1], ["01", 1], ["11", 1], ["cc", 1]], "repair", 5),
        ("corner5", [["00", 1], ["00", 2], ["10", 1], ["01", 1], ["11", 1]], "corner", 5),
    ]
    for plan, (name, slots, weights, cost) in zip(plans, required, strict=True):
        _fields(plan, ("id", "slots", "weights", "cost"))
        _require(
            plan["id"] == name
            and plan["slots"] == slots
            and plan["weights"] == weights
            and plan["cost"] == cost,
            "fixed acquisition plan",
        )
    off_model = protocol["off_model"]
    _fields(off_model, ("amplitude", "rule", "global_bound"))
    _require(0 < _fraction(off_model["amplitude"]) <= 1, "positive off-model amplitude")
    _require(0 < _fraction(off_model["global_bound"]) <= 1, "physical off-model bound")
    _require(off_model["rule"] == "h=b*((u-1/2)^2+(v-1/2)^2)", "off-model rule")
    controls = protocol["global_controls"]
    _require(type(controls) is list and len(controls) == 2, "two global-domain controls")
    for control in controls:
        _fields(control, ("id", "corners", "theta", "witness", "classification"))
        _parameters(control)
        _require(type(control["witness"]) is list and len(control["witness"]) == 2, "witness point")
        _require(
            all(0 <= _fraction(value) <= 1 for value in control["witness"]), "witness inside Q"
        )
        _require(
            control["classification"]
            in (
                "sample_valid_globally_invalid",
                "globally_valid_outside_admission",
            ),
            "declared global classification",
        )


def _parameters(profile):
    _require(type(profile["id"]) is str and profile["id"], "profile identifier")
    _require(
        type(profile["corners"]) is list and len(profile["corners"]) == 4,
        "four corner coefficients",
    )
    return [_polarization(value) for value in profile["corners"]], _fraction(profile["theta"])


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


def _geometry(protocol):
    bounds, measure, basis, kernel, _, normalization, old = _base_geometry(protocol)
    sites = [[_fraction(value) for value in row] for row in protocol["coordinates"]]
    bubble = _poly_multiply(basis[0], basis[3])
    functions = [*basis, bubble]
    evaluation = [[_poly_value(function, *site) for function in functions] for site in sites]
    coefficient_decoder = _inverse(evaluation)
    integrals = [
        normalization * _integral(_poly_multiply(function, kernel), bounds, measure)
        for function in functions
    ]
    _require(integrals[:4] == old["weights"], "independent corner integrals")
    repair_weights = _dense_product([integrals], coefficient_decoder)[0]
    _require(
        _dense_product([repair_weights], evaluation)[0] == integrals,
        "full population target identity",
    )
    _require(evaluation[4][4] > 0, "interior station detects the bubble basis")
    ratio = integrals[4] / evaluation[4][4]
    direct_weights = [integrals[a] - ratio * evaluation[4][a] for a in range(4)] + [ratio]
    _require(repair_weights == direct_weights, "target inverse and direct elimination agree")
    _require(sum(repair_weights, F(0)) == sum(integrals[:4], F(0)), "constant profile preservation")
    geometry = {
        "volume": old["volume"],
        "sigma": old["sigma"],
        "corner_weights": list(integrals[:4]),
        "bubble_target": integrals[4],
        "bubble_at_center": evaluation[4][4],
        "center_basis": list(evaluation[4][:4]),
        "evaluation_matrix": evaluation,
        "coefficient_decoder": coefficient_decoder,
        "repair_weights": repair_weights,
        "weight_sum": sum(repair_weights, F(0)),
    }
    return geometry, bounds, measure, basis, bubble, kernel, sites, normalization


def _compiled_plans(protocol, geometry):
    station_order = protocol["stations"]
    result = []
    for supplied in protocol["plans"]:
        raw = (
            geometry["repair_weights"]
            if supplied["weights"] == "repair"
            else geometry["corner_weights"]
        )
        station_weights = dict(zip(station_order[: len(raw)], raw, strict=True))
        multiplicities = {
            name: sum(station == name for station, _ in supplied["slots"])
            for name in station_weights
        }
        event_weights = [
            station_weights[station] / multiplicities[station] for station, _ in supplied["slots"]
        ]
        _require(
            sum(event_weights, F(0)) == geometry["weight_sum"], "plan constant-profile response"
        )
        result.append(
            {
                "id": supplied["id"],
                "slots": [[station, shot] for station, shot in supplied["slots"]],
                "cost": supplied["cost"],
                "event_weights": event_weights,
            }
        )
    return result


def _score_plan(means, target, plan, matrices):
    outcomes = list(product((-1, 1), repeat=len(means)))
    probabilities, states = _branches(means, matrices)
    rows, estimates = [], []
    for outcome, probability, state in zip(outcomes, probabilities, states, strict=True):
        estimate = _dot(plan["event_weights"], outcome)
        rows.append(
            {
                "outcomes": list(outcome),
                "probability": probability,
                "state_diagonal": list(state),
                "estimate": estimate,
            }
        )
        estimates.append(estimate)
    mean, variance = _moments(probabilities, estimates)
    independent_variance = sum(
        (
            weight**2 * (1 - polarization**2)
            for weight, polarization in zip(plan["event_weights"], means, strict=True)
        ),
        F(0),
    )
    _require(variance == independent_variance, "fresh-copy plan variance")
    bias = mean - target
    return {
        "rows": rows,
        "mean": mean,
        "bias": bias,
        "variance": variance,
        "mse": variance + bias**2,
    }


def _decomposition(repair, geometry, theta):
    rows = repair["rows"]
    probabilities = [row["probability"] for row in rows]
    base_values = [_dot(geometry["corner_weights"], row["outcomes"][:4]) for row in rows]
    theta_values = [_dot(geometry["coefficient_decoder"][4], row["outcomes"]) for row in rows]
    for row, base, estimate in zip(rows, base_values, theta_values, strict=True):
        _require(
            row["estimate"] == base + geometry["bubble_target"] * estimate,
            "pathwise repaired decomposition",
        )
    base_mean, base_variance = _moments(probabilities, base_values)
    theta_mean, theta_variance = _moments(probabilities, theta_values)
    _require(theta_mean == theta, "population theta recovery")
    covariance = sum(
        (
            p * (base - base_mean) * (estimate - theta_mean)
            for p, base, estimate in zip(probabilities, base_values, theta_values, strict=True)
        ),
        F(0),
    )
    naive = base_variance + geometry["bubble_target"] ** 2 * theta_variance
    corrected = naive + 2 * geometry["bubble_target"] * covariance
    _require(corrected == repair["variance"], "shared-corner covariance identity")
    return {
        "base_variance": base_variance,
        "theta_variance": theta_variance,
        "base_theta_covariance": covariance,
        "independence_shortcut_variance": naive,
        "covariance_corrected_variance": corrected,
    }


def _global_controls(controls, basis, bubble, sites):
    result = []
    for supplied in controls:
        corners, theta = _parameters(supplied)
        profile = _model_polynomial(corners, theta, basis, bubble)
        sample_means = [_poly_value(profile, *site) for site in sites]
        _require(all(-1 <= mean <= 1 for mean in sample_means), "global control sampled means")
        admission = _admission(corners, theta)
        _require(admission > 1, "global control must be outside sufficient admission")
        witness = [_fraction(value) for value in supplied["witness"]]
        value = _poly_value(profile, *witness)
        minimum_eigenvalue = (F(1) - abs(value)) / 2
        interval = [min(corners) + min(theta, F(0)) / 16, max(corners) + max(theta, F(0)) / 16]
        _require(interval[0] <= value <= interval[1], "global witness inside analytic enclosure")
        if supplied["classification"] == "sample_valid_globally_invalid":
            _require(abs(value) > 1 and minimum_eigenvalue < 0, "nonphysical interior witness")
        else:
            _require(-1 <= interval[0] <= interval[1] <= 1, "valid profile analytic interval")
            _require(minimum_eigenvalue >= 0, "physical witness for excluded profile")
        # No control witness is passed to _state or the positive branch simulator.
        result.append(
            {
                "id": supplied["id"],
                "admission_bound": admission,
                "admission": "outside_sufficient_domain",
                "sample_means": sample_means,
                "witness": witness,
                "witness_value": value,
                "witness_min_eigenvalue": minimum_eigenvalue,
                "global_interval": interval,
                "classification": supplied["classification"],
            }
        )
    return result


def analyze(protocol):
    """Return the complete fixed-domain report; no observer receives private profiles."""
    _validate(protocol)
    geometry, bounds, measure, basis, bubble, kernel, sites, normalization = _geometry(protocol)
    plans = _compiled_plans(protocol, geometry)
    operators, sparse, schedule_counts = {}, {}, {}
    for name, count in (("corner4", 4), ("five_factor", 5)):
        matrices, rows, orders = _operators(count, list(product((-1, 1), repeat=count)))
        operators[name], sparse[count], schedule_counts[name] = rows, matrices, orders
    station_index = {station: i for i, station in enumerate(protocol["stations"])}
    profiles = []
    for supplied in protocol["profiles"]:
        corners, theta = _parameters(supplied)
        profile = _model_polynomial(corners, theta, basis, bubble)
        sample_means = [_poly_value(profile, *site) for site in sites]
        _require(all(-1 <= mean <= 1 for mean in sample_means), "admitted physical sampled states")
        coefficients = [*corners, theta]
        _require(
            [_dot(row, coefficients) for row in geometry["evaluation_matrix"]] == sample_means,
            "profile evaluation versus complete linear map",
        )
        recovered = [_dot(row, sample_means) for row in geometry["coefficient_decoder"]]
        _require(recovered == coefficients, "all population coefficients recovered")
        target = normalization * _integral(_poly_multiply(profile, kernel), bounds, measure)
        corner_poly = _model_polynomial(corners, F(0), basis, bubble)
        corner_target = normalization * _integral(
            _poly_multiply(corner_poly, kernel), bounds, measure
        )
        _require(
            target == _dot(geometry["repair_weights"], sample_means),
            "geometric versus repaired target",
        )
        _require(
            corner_target == _dot(geometry["corner_weights"], corners), "original corner target"
        )
        plan_reports = {}
        for plan in plans:
            means = [sample_means[station_index[station]] for station, _ in plan["slots"]]
            scored = _score_plan(means, target, plan, sparse[plan["cost"]])
            expected_mean = target if plan["id"] == "repair5" else corner_target
            _require(scored["mean"] == expected_mean, "plan population target")
            plan_reports[plan["id"]] = scored
        repaired = plan_reports["repair5"]
        profiles.append(
            {
                "id": supplied["id"],
                "corners": corners,
                "theta": theta,
                "admission_bound": _admission(corners, theta),
                "sample_means": sample_means,
                "recovered_coefficients": recovered,
                "target": target,
                "corner_target": corner_target,
                "plans": plan_reports,
                "repair_decomposition": _decomposition(repaired, geometry, theta),
                "mse_differences": {
                    "repair_minus_corner4": repaired["mse"] - plan_reports["corner4"]["mse"],
                    "repair_minus_corner5": repaired["mse"] - plan_reports["corner5"]["mse"],
                },
            }
        )
    center = sites[4]
    udelta = {(1, 0): F(1), (0, 0): -center[0]}
    vdelta = {(0, 1): F(1), (0, 0): -center[1]}
    distance = _poly_add(_poly_multiply(udelta, udelta), _poly_multiply(vdelta, vdelta))
    amplitude = _fraction(protocol["off_model"]["amplitude"])
    off_poly = _poly_scale(_poly_multiply(bubble, distance), amplitude)
    sample_means = [_poly_value(off_poly, *site) for site in sites]
    _require(all(value == 0 for value in sample_means), "further off-model sampling collision")
    distance_bound = max((bounds[0] - center[0]) ** 2, (bounds[1] - center[0]) ** 2) + max(
        (bounds[2] - center[1]) ** 2,
        (bounds[3] - center[1]) ** 2,
    )
    global_bound = _fraction(protocol["off_model"]["global_bound"])
    _require(
        amplitude * distance_bound / 16 <= global_bound <= 1,
        "off-model nonnegative physical profile enclosure",
    )
    target = normalization * _integral(_poly_multiply(off_poly, kernel), bounds, measure)
    _require(target > 0, "further off-model true target")
    probabilities, states = _branches(sample_means, sparse[5])
    estimates = [_dot(geometry["repair_weights"], row) for row in product((-1, 1), repeat=5)]
    mean, variance = _moments(probabilities, estimates)
    _require(mean == 0, "five-site estimator remains blind outside its model")
    bias = mean - target
    return {
        "geometry": geometry,
        "operators": operators,
        "schedule_counts": schedule_counts,
        "plans": plans,
        "profiles": profiles,
        "off_model": {
            "sample_means": sample_means,
            "global_bound": global_bound,
            "target": target,
            "probabilities": probabilities,
            "state_diagonals": states,
            "estimator_mean": mean,
            "estimator_bias": bias,
            "estimator_variance": variance,
            "mse": variance + bias**2,
        },
        "global_controls": _global_controls(protocol["global_controls"], basis, bubble, sites),
    }
