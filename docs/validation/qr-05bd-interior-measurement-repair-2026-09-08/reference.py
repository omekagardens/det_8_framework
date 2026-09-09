"""Independent Bernoulli/beta-integral reference for the frozen QR-05BD study.

Own BC authoring patterns are carried statically. No other engine, artifact or
private target table is imported. Importing this module performs no study.
"""

from fractions import Fraction
from itertools import permutations, product
from math import factorial


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    pending = [(value, False)]
    active = set()
    while pending:
        item, leaving = pending.pop()
        kind = type(item)
        if kind not in (dict, list):
            _require(kind in (int, str, Fraction, type(None)), "non-native value")
            continue
        identity = id(item)
        if leaving:
            active.remove(identity)
            continue
        _require(identity not in active, "cyclic container")
        active.add(identity)
        pending.append((item, True))
        if kind is dict:
            _require(all(type(key) is str for key in item), "non-string key")
            pending.extend((child, False) for child in item.values())
        else:
            pending.extend((child, False) for child in item)


def _fraction(value):
    _require(type(value) in (str, int, Fraction), "invalid rational type")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational") from exc


def _record(value, fields, message):
    _require(type(value) is dict and set(value) == set(fields), message)


def _vector(value, length, message):
    _require(type(value) is list and len(value) == length, message)


def _dot(left, right):
    _require(len(left) == len(right), "vector width")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _multiply(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _matmul(left, right):
    columns = list(zip(*right))
    return [[_dot(row, column) for column in columns] for row in left]


def _beta(power, complement):
    """Integral x**power * (1-x)**complement over the unit interval."""
    _require(
        type(power) is int and type(complement) is int and power >= 0 and complement >= 0,
        "beta exponents",
    )
    return Fraction(factorial(power) * factorial(complement), factorial(power + complement + 1))


def _basis(u, v):
    return [(1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v]


def _bubble(u, v):
    return u * (1 - u) * v * (1 - v)


def _profile_value(corners, theta, point):
    u, v = point
    return _dot(corners, _basis(u, v)) + theta * _bubble(u, v)


def _coordinates(protocol):
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station order")
    _vector(protocol["coordinates"], 5, "five coordinates")
    points = []
    for point in protocol["coordinates"]:
        _vector(point, 2, "coordinate pair")
        points.append([_fraction(value) for value in point])
    expected = [
        [Fraction(int(symbol)) for symbol in station] for station in protocol["stations"][:4]
    ]
    _require(points[:4] == expected, "corner coordinates")
    _require(all(0 < value < 1 for value in points[4]), "interior fifth station")
    return points


def _geometry(protocol, points):
    supplied = protocol["geometry"]
    _record(supplied, ("u", "v", "measure_factor", "sigma_rule", "field_rule"), "geometry fields")
    _vector(supplied["u"], 2, "u bounds")
    _vector(supplied["v"], 2, "v bounds")
    u0, u1 = map(_fraction, supplied["u"])
    v0, v1 = map(_fraction, supplied["v"])
    measure = _fraction(supplied["measure_factor"])
    _require((u0, u1, v0, v1) == (0, 1, 0, 1), "unit null rectangle")
    _require(measure == Fraction(1, 2), "null-coordinate measure")
    _require(
        supplied["sigma_rule"] == "V^4" and supplied["field_rule"] == "F=V^2*f", "normalization"
    )
    volume = measure * (u1 - u0) * (v1 - v0)
    sigma = volume**4
    factor = volume**4 / sigma
    corner_weights = []
    for station in protocol["stations"][:4]:
        i, j = (int(symbol) for symbol in station)
        corner_weights.append(factor * _beta(i, 2 - i) * _beta(j, 2 - j))
    bubble_target = factor * _beta(1, 2) * _beta(1, 2)
    evaluation = [_basis(*point) + [_bubble(*point)] for point in points]
    center_basis = list(evaluation[4][:4])
    bubble_at_center = evaluation[4][4]
    _require(bubble_at_center > 0, "bubble must be visible at the interior station")
    # Direct coefficient recovery, without row reduction or a generic inverse.
    decoder = [[Fraction(int(i == j)) for j in range(5)] for i in range(4)]
    decoder.append([-value / bubble_at_center for value in center_basis] + [1 / bubble_at_center])
    identity = [[Fraction(int(i == j)) for j in range(5)] for i in range(5)]
    _require(_matmul(evaluation, decoder) == identity, "evaluation times decoder")
    _require(_matmul(decoder, evaluation) == identity, "decoder times evaluation")
    integral_row = corner_weights + [bubble_target]
    repaired = [_dot(integral_row, column) for column in zip(*decoder)]
    return {
        "volume": volume,
        "sigma": sigma,
        "corner_weights": corner_weights,
        "bubble_target": bubble_target,
        "bubble_at_center": bubble_at_center,
        "center_basis": center_basis,
        "evaluation_matrix": evaluation,
        "coefficient_decoder": decoder,
        "repair_weights": repaired,
        "weight_sum": sum(repaired, Fraction(0)),
    }


def _operator_diagonal(outcomes, basis, order):
    diagonal = []
    for bits in basis:
        entry = Fraction(1)
        for index in order:
            entry *= Fraction(int(outcomes[index] == 1 - 2 * bits[index]))
        diagonal.append(entry)
    return diagonal


def _operator_bank(factors):
    outcomes = list(product((-1, 1), repeat=factors))
    basis = list(product((0, 1), repeat=factors))
    rows = [
        {
            "outcomes": list(outcome),
            "kraus_diagonal": _operator_diagonal(outcome, basis, range(factors)),
        }
        for outcome in outcomes
    ]
    schedules = list(permutations(range(factors)))
    for schedule in schedules:
        for outcome, row in zip(outcomes, rows):
            _require(
                _operator_diagonal(outcome, basis, schedule) == row["kraus_diagonal"],
                "complete operator changed under a factor permutation",
            )
    return rows, len(schedules)


def _plan_specs(protocol, geometry):
    _require(type(protocol["plans"]) is list, "plan list")
    plans = []
    for supplied in protocol["plans"]:
        _record(supplied, ("id", "slots", "weights", "cost"), "plan fields")
        _require(type(supplied["id"]) is str and supplied["id"], "plan identifier")
        _require(type(supplied["slots"]) is list, "plan slots")
        slots = []
        for slot in supplied["slots"]:
            _vector(slot, 2, "event slot")
            station, shot = slot
            _require(type(station) is str and station in protocol["stations"], "event station")
            _require(type(shot) is int and shot > 0, "fresh-shot identifier")
            slots.append([station, shot])
        _require(len({tuple(slot) for slot in slots}) == len(slots), "distinct event slots")
        _require(type(supplied["cost"]) is int and supplied["cost"] == len(slots), "shot cost")
        _require(len(slots) in (4, 5), "bounded plan width")
        if supplied["weights"] == "corner":
            labels = protocol["stations"][:4]
            station_weights = dict(zip(labels, geometry["corner_weights"]))
        else:
            _require(supplied["weights"] == "repair", "weight rule")
            labels = protocol["stations"]
            station_weights = dict(zip(labels, geometry["repair_weights"]))
        counts = {station: sum(slot[0] == station for slot in slots) for station in labels}
        _require({slot[0] for slot in slots} == set(labels), "complete station coverage")
        plans.append(
            {
                "id": supplied["id"],
                "slots": slots,
                "cost": supplied["cost"],
                "event_weights": [
                    station_weights[station] / counts[station] for station, _ in slots
                ],
            }
        )
    _require([plan["id"] for plan in plans] == ["corner4", "repair5", "corner5"], "plan order")
    return plans


def _law(means, operators):
    _require(all(-1 <= mean <= 1 for mean in means), "nonpositive preparation")
    basis = list(product((0, 1), repeat=len(means)))
    density = [
        _multiply((1 + (1 - 2 * bit) * mean) / 2 for bit, mean in zip(bits, means))
        for bits in basis
    ]
    probabilities = []
    states = []
    for operator in operators:
        probability = _multiply(
            (1 + sign * mean) / 2 for sign, mean in zip(operator["outcomes"], means)
        )
        state = [rho * entry * entry for rho, entry in zip(density, operator["kraus_diagonal"])]
        _require(sum(state, Fraction(0)) == probability, "branch trace and Bernoulli law")
        probabilities.append(probability)
        states.append(state)
    _require(sum(probabilities, Fraction(0)) == 1, "record law normalization")
    return probabilities, states


def _plan_report(plan, sample_means, stations, target, operators):
    means_by_station = dict(zip(stations, sample_means))
    means = [means_by_station[station] for station, _ in plan["slots"]]
    event_weights = plan["event_weights"]
    probabilities, states = _law(means, operators)
    rows = [
        {
            "outcomes": list(operator["outcomes"]),
            "probability": probability,
            "state_diagonal": state,
            "estimate": _dot(event_weights, operator["outcomes"]),
        }
        for operator, probability, state in zip(operators, probabilities, states)
    ]
    mean = _dot(event_weights, means)
    variance = sum(
        (weight**2 * (1 - value**2) for weight, value in zip(event_weights, means)), Fraction(0)
    )
    bias = mean - target
    mse = variance + bias**2
    _require(
        sum((row["probability"] * row["estimate"] for row in rows), Fraction(0)) == mean,
        "enumerated mean",
    )
    _require(
        sum((row["probability"] * (row["estimate"] - mean) ** 2 for row in rows), Fraction(0))
        == variance,
        "enumerated variance",
    )
    _require(
        sum((row["probability"] * (row["estimate"] - target) ** 2 for row in rows), Fraction(0))
        == mse,
        "enumerated MSE",
    )
    return {"rows": rows, "mean": mean, "bias": bias, "variance": variance, "mse": mse}


def _coefficients(profile):
    _vector(profile["corners"], 4, "profile corners")
    corners = [_fraction(value) for value in profile["corners"]]
    theta = _fraction(profile["theta"])
    admission = max(abs(value) for value in corners) + abs(theta) * Fraction(1, 16)
    return corners, theta, admission


def _direct_target(corners, theta, geometry):
    integral = Fraction(0)
    for mean, (i, j) in zip(corners, ((0, 0), (1, 0), (0, 1), (1, 1))):
        integral += mean * _beta(i, 2 - i) * _beta(j, 2 - j)
    integral += theta * _beta(1, 2) * _beta(1, 2)
    return geometry["volume"] ** 4 / geometry["sigma"] * integral


def _decomposition(sample_means, geometry, repair_variance):
    base_weights = geometry["corner_weights"] + [Fraction(0)]
    theta_weights = geometry["coefficient_decoder"][4]
    individual_variances = [1 - mean**2 for mean in sample_means]
    base_variance = sum((w**2 * v for w, v in zip(base_weights, individual_variances)), Fraction(0))
    theta_variance = sum(
        (w**2 * v for w, v in zip(theta_weights, individual_variances)), Fraction(0)
    )
    covariance = sum(
        (a * b * v for a, b, v in zip(base_weights, theta_weights, individual_variances)),
        Fraction(0),
    )
    bubble_target = geometry["bubble_target"]
    shortcut = base_variance + bubble_target**2 * theta_variance
    corrected = shortcut + 2 * bubble_target * covariance
    _require(corrected == repair_variance, "shared-corner covariance identity")
    return {
        "base_variance": base_variance,
        "theta_variance": theta_variance,
        "base_theta_covariance": covariance,
        "independence_shortcut_variance": shortcut,
        "covariance_corrected_variance": corrected,
    }


def _profile_report(profile, protocol, points, geometry, plans, operators):
    _record(profile, ("id", "corners", "theta"), "profile fields")
    _require(type(profile["id"]) is str and profile["id"], "profile identifier")
    corners, theta, admission = _coefficients(profile)
    _require(admission <= 1, "outside sufficient admission domain")
    sample_means = [_profile_value(corners, theta, point) for point in points]
    recovered = [_dot(row, sample_means) for row in geometry["coefficient_decoder"]]
    _require(recovered == corners + [theta], "full coefficient recovery")
    target = _direct_target(corners, theta, geometry)
    corner_target = _direct_target(corners, Fraction(0), geometry)
    _require(_dot(geometry["repair_weights"], sample_means) == target, "repaired population target")
    plan_reports = {}
    for plan in plans:
        bank = operators["corner4" if len(plan["slots"]) == 4 else "five_factor"]
        plan_reports[plan["id"]] = _plan_report(
            plan, sample_means, protocol["stations"], target, bank
        )
    return {
        "id": profile["id"],
        "corners": corners,
        "theta": theta,
        "admission_bound": admission,
        "sample_means": sample_means,
        "recovered_coefficients": recovered,
        "target": target,
        "corner_target": corner_target,
        "plans": plan_reports,
        "repair_decomposition": _decomposition(
            sample_means, geometry, plan_reports["repair5"]["variance"]
        ),
        "mse_differences": {
            "repair_minus_corner4": plan_reports["repair5"]["mse"] - plan_reports["corner4"]["mse"],
            "repair_minus_corner5": plan_reports["repair5"]["mse"] - plan_reports["corner5"]["mse"],
        },
    }


def _off_model(protocol, points, geometry, repair_plan, operators):
    control = protocol["off_model"]
    _record(control, ("amplitude", "rule", "global_bound"), "off-model fields")
    _require(control["rule"] == "h=b*((u-1/2)^2+(v-1/2)^2)", "off-model rule")
    amplitude = _fraction(control["amplitude"])
    _require(0 < amplitude <= 1, "off-model amplitude")
    half = Fraction(1, 2)
    sample_means = [
        amplitude * _bubble(u, v) * ((u - half) ** 2 + (v - half) ** 2) for u, v in points
    ]
    # The response contributes x(1-x), and the kernel contributes another (1-x).
    # Integrate the squared-distance factor by its shifted beta moments.
    plain = _beta(1, 2)
    shifted_square = _beta(3, 2) - 2 * half * _beta(2, 2) + half**2 * _beta(1, 2)
    target = (
        amplitude
        * geometry["volume"] ** 4
        / geometry["sigma"]
        * (shifted_square * plain + plain * shifted_square)
    )
    bound = _fraction(control["global_bound"])
    sufficient_bound = amplitude * Fraction(1, 16) * (half**2 + half**2)
    _require(bound >= sufficient_bound and bound <= 1, "off-model global bound")
    plan_report = _plan_report(repair_plan, sample_means, protocol["stations"], target, operators)
    _require(all(value == 0 for value in sample_means), "declared five-site blind spot")
    return {
        "sample_means": sample_means,
        "global_bound": bound,
        "target": target,
        "probabilities": [row["probability"] for row in plan_report["rows"]],
        "state_diagonals": [row["state_diagonal"] for row in plan_report["rows"]],
        "estimator_mean": plan_report["mean"],
        "estimator_bias": plan_report["bias"],
        "estimator_variance": plan_report["variance"],
        "mse": plan_report["mse"],
    }


def _global_controls(protocol, points):
    _require(type(protocol["global_controls"]) is list, "global-control list")
    reports = []
    for control in protocol["global_controls"]:
        _record(
            control,
            ("id", "corners", "theta", "witness", "classification"),
            "global-control fields",
        )
        corners, theta, admission = _coefficients(control)
        _require(admission > 1, "global control must be outside sufficient domain")
        sample_means = [_profile_value(corners, theta, point) for point in points]
        _require(all(-1 <= value <= 1 for value in sample_means), "sample validity control")
        _vector(control["witness"], 2, "global-control witness")
        witness = [_fraction(value) for value in control["witness"]]
        _require(all(0 <= coordinate <= 1 for coordinate in witness), "witness in unit rectangle")
        value = _profile_value(corners, theta, witness)
        interval = [
            min(corners) + min(theta, Fraction(0)) / 16,
            max(corners) + max(theta, Fraction(0)) / 16,
        ]
        classification = control["classification"]
        if classification == "sample_valid_globally_invalid":
            _require(abs(value) > 1, "interior physical-invalidity witness")
        else:
            _require(classification == "globally_valid_outside_admission", "global classification")
            _require(-1 <= interval[0] <= interval[1] <= 1, "valid excluded profile certificate")
        # Formal diagnostic only: these controls never enter _law or a state simulator.
        reports.append(
            {
                "id": control["id"],
                "admission_bound": admission,
                "admission": "outside_sufficient_domain",
                "sample_means": sample_means,
                "witness": witness,
                "witness_value": value,
                "witness_min_eigenvalue": (1 - abs(value)) / 2,
                "global_interval": interval,
                "classification": classification,
            }
        )
    return reports


def analyze(protocol: dict) -> dict:
    """Compute the shared exact report; no private outputs are accepted as inputs."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    points = _coordinates(protocol)
    geometry = _geometry(protocol, points)
    four, four_schedules = _operator_bank(4)
    five, five_schedules = _operator_bank(5)
    operators = {"corner4": four, "five_factor": five}
    plans = _plan_specs(protocol, geometry)
    _require(type(protocol["profiles"]) is list, "profile list")
    profiles = [
        _profile_report(profile, protocol, points, geometry, plans, operators)
        for profile in protocol["profiles"]
    ]
    _require(
        len({profile["id"] for profile in profiles}) == len(profiles), "unique profile identifiers"
    )
    report = {
        "geometry": geometry,
        "operators": operators,
        "schedule_counts": {"corner4": four_schedules, "five_factor": five_schedules},
        "plans": plans,
        "profiles": profiles,
        "off_model": _off_model(protocol, points, geometry, plans[1], five),
        "global_controls": _global_controls(protocol, points),
    }
    _native(report)
    return report
