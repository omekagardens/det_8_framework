"""Independent Bernoulli/beta-integral reference for QR-05BE.

Own BD authoring patterns are carried statically. No old engine, artifact,
cross-engine helper or private target table is imported or executed.
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


def _plan_specs(protocol, geometry, reduction):
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
            coefficients = geometry["corner_weights"]
        elif supplied["weights"] == "repair":
            labels = protocol["stations"]
            coefficients = geometry["repair_weights"]
        else:
            _require(supplied["weights"] == "reduced", "weight rule")
            labels = protocol["reduction"]["retained_stations"]
            coefficients = reduction["target_weights"]
        station_weights = dict(zip(labels, coefficients))
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
    _require(
        [plan["id"] for plan in plans] == ["corner4", "repair5", "corner5", "target4", "repeatcc5"],
        "plan order",
    )
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


def _reduction(protocol, geometry):
    supplied = protocol["reduction"]
    _record(supplied, ("omitted_station", "retained_stations", "rule"), "reduction fields")
    stations = protocol["stations"]
    _require(supplied["omitted_station"] in stations, "omitted station")
    omitted = stations.index(supplied["omitted_station"])
    _vector(supplied["retained_stations"], 4, "four retained stations")
    retained = [stations.index(station) for station in supplied["retained_stations"]]
    _require(omitted == 3 and retained == [0, 1, 2, 4], "declared reduction order")
    evaluation = geometry["evaluation_matrix"]
    matrix = [list(evaluation[index]) for index in retained]
    # Three retained corner rows are independent coordinate vectors. The
    # remaining row has a nonzero bubble coordinate, so adds exactly one rank.
    units = [[Fraction(int(i == j)) for j in range(5)] for i in range(3)]
    _require(matrix[:3] == units, "retained corner-row structure")
    _require(matrix[3][4] != 0, "independent interior row")
    rank = len(units) + int(matrix[3][4] != 0)
    direction = [row[omitted] for row in geometry["coefficient_decoder"]]
    null_image = [_dot(row, direction) for row in matrix]
    integral_row = geometry["corner_weights"] + [geometry["bubble_target"]]
    target_null_image = _dot(integral_row, direction)
    target_weights = [geometry["repair_weights"][index] for index in retained]
    _require(all(value == 0 for value in null_image), "retained null certificate")
    _require(target_null_image == 0, "target null certificate")
    _require(geometry["repair_weights"][omitted] == 0, "omitted target coefficient")
    _require(
        [_dot(geometry["repair_weights"], column) for column in zip(*evaluation)] == integral_row,
        "full target row certificate",
    )
    _require(
        [_dot(target_weights, column) for column in zip(*matrix)] == integral_row,
        "reduced target row certificate",
    )
    return {
        "retained_indices": retained,
        "omitted_index": omitted,
        "retained_evaluation_matrix": matrix,
        "retained_rank": rank,
        "omission_direction": direction,
        "retained_null_image": null_image,
        "target_null_image": target_null_image,
        "target_weights": target_weights,
    }


def _partial_trace_diagonal(diagonal, factors, omitted):
    _require(len(diagonal) == 1 << factors, "full diagonal size")
    _require(0 <= omitted < factors, "trace index")
    reduced = [Fraction(0) for _ in range(1 << (factors - 1))]
    for full_index, entry in enumerate(diagonal):
        reduced_index = 0
        for position in range(factors):
            if position != omitted:
                bit = (full_index >> (factors - position - 1)) & 1
                reduced_index = 2 * reduced_index + bit
        reduced[reduced_index] += entry
    return reduced


def _marginalization(plans, reduction):
    full = plans["repair5"]
    direct = plans["target4"]
    retained = reduction["retained_indices"]
    omitted = reduction["omitted_index"]
    rows = []
    pathwise_checks = 0
    wrong_disagreements = 0
    for target_row in direct["rows"]:
        outcome = target_row["outcomes"]
        indices = [
            index
            for index, row in enumerate(full["rows"])
            if [row["outcomes"][position] for position in retained] == outcome
        ]
        _require(len(indices) == 2, "two omitted-outcome branches")
        full_estimates = [full["rows"][index]["estimate"] for index in indices]
        for estimate in full_estimates:
            _require(estimate == target_row["estimate"], "pathwise reduction")
            pathwise_checks += 1
        probability = sum((full["rows"][index]["probability"] for index in indices), Fraction(0))
        summed = [
            sum(
                (full["rows"][index]["state_diagonal"][coordinate] for index in indices),
                Fraction(0),
            )
            for coordinate in range(32)
        ]
        reduced = _partial_trace_diagonal(summed, 5, omitted)
        wrong = _partial_trace_diagonal(summed, 5, 4)
        _require(reduced == target_row["state_diagonal"], "direct reduced branch state")
        _require(probability == target_row["probability"], "direct marginal probability")
        _require(sum(reduced, Fraction(0)) == probability, "reduced trace")
        wrong_disagreements += int(wrong != target_row["state_diagonal"])
        rows.append(
            {
                "outcomes": list(outcome),
                "full_indices": indices,
                "full_estimates": full_estimates,
                "probability": probability,
                "summed_full_state": summed,
                "reduced_state": reduced,
                "wrong_trace_state": wrong,
                "estimate": target_row["estimate"],
            }
        )
    differences = {key: direct[key] - full[key] for key in ("mean", "variance", "mse")}
    _require(all(value == 0 for value in differences.values()), "reduction moment equality")
    return {
        "rows": rows,
        "pathwise_checks": pathwise_checks,
        "wrong_trace_disagreements": wrong_disagreements,
        "moment_differences": differences,
    }


def _reallocation(protocol, sample_means, geometry, plans):
    _require(protocol["reallocation"]["station"] == "cc", "declared repeat station")
    index = protocol["stations"].index(protocol["reallocation"]["station"])
    weight = geometry["repair_weights"][index]
    predicted = weight**2 * (1 - sample_means[index] ** 2) / 2
    direct = plans["target4"]["variance"] - plans["repeatcc5"]["variance"]
    mse_difference = plans["target4"]["mse"] - plans["repeatcc5"]["mse"]
    _require(plans["target4"]["mean"] == plans["repeatcc5"]["mean"], "replication mean")
    _require(direct == predicted == mse_difference and predicted >= 0, "fresh-copy replication")
    return {
        "direct_variance_reduction": direct,
        "predicted_variance_reduction": predicted,
        "direct_mse_reduction": mse_difference,
    }


def _profile_report(profile, protocol, points, geometry, reduction, plans, operators):
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
        "marginalization": _marginalization(plan_reports, reduction),
        "reallocation": _reallocation(protocol, sample_means, geometry, plan_reports),
        "mse_differences": {
            "target4_minus_corner4": plan_reports["target4"]["mse"]
            - plan_reports["corner4"]["mse"],
            "repeatcc5_minus_corner5": plan_reports["repeatcc5"]["mse"]
            - plan_reports["corner5"]["mse"],
            "repeatcc5_minus_repair5": plan_reports["repeatcc5"]["mse"]
            - plan_reports["repair5"]["mse"],
        },
    }


def _off_model(protocol, points, geometry, reduction, plans, operators):
    control = protocol["off_model"]
    _record(control, ("id", "amplitude", "rule", "global_bound", "plans"), "off-model fields")
    _require(type(control["id"]) is str and control["id"], "off-model identifier")
    _require(control["rule"] == "h=b*((u-1/2)^2+(v-1/2)^2)", "off-model rule")
    _require(control["plans"] == ["repair5", "target4", "repeatcc5"], "off-model plans")
    amplitude = _fraction(control["amplitude"])
    _require(0 < amplitude <= 1, "off-model amplitude")
    half = Fraction(1, 2)
    sample_means = [
        amplitude * _bubble(u, v) * ((u - half) ** 2 + (v - half) ** 2) for u, v in points
    ]
    # Shifted beta moments, independent of a monomial integration engine.
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
    _require(all(value == 0 for value in sample_means), "declared five-site blind spot")
    selected = {plan["id"]: plan for plan in plans}
    plan_reports = {}
    for name in control["plans"]:
        plan = selected[name]
        bank = operators["corner4" if len(plan["slots"]) == 4 else "five_factor"]
        plan_reports[name] = _plan_report(plan, sample_means, protocol["stations"], target, bank)
    return {
        "id": control["id"],
        "sample_means": sample_means,
        "global_bound": bound,
        "target": target,
        "plans": plan_reports,
        "marginalization": _marginalization(plan_reports, reduction),
    }


def _collision(protocol, profiles, reduction):
    supplied = protocol["collision"]
    _record(supplied, ("profiles", "rule"), "collision fields")
    _vector(supplied["profiles"], 2, "collision pair")
    by_name = {profile["id"]: profile for profile in profiles}
    first, second = [by_name[name] for name in supplied["profiles"]]
    first_coefficients = first["corners"] + [first["theta"]]
    second_coefficients = second["corners"] + [second["theta"]]
    coefficient_difference = [b - a for a, b in zip(first_coefficients, second_coefficients)]
    means_difference = [b - a for a, b in zip(first["sample_means"], second["sample_means"])]
    target_difference = second["target"] - first["target"]
    omitted_states = []
    averaged_states = []
    for profile in (first, second):
        mean = profile["sample_means"][reduction["omitted_index"]]
        omitted_states.append([(1 + mean) / 2, (1 - mean) / 2])
        rows = profile["plans"]["repair5"]["rows"]
        averaged_states.append(
            [
                sum((row["state_diagonal"][index] for row in rows), Fraction(0))
                for index in range(32)
            ]
        )
    total_variations = {}
    for plan in ("repair5", "target4"):
        left_rows = first["plans"][plan]["rows"]
        right_rows = second["plans"][plan]["rows"]
        _require(
            [row["outcomes"] for row in left_rows] == [row["outcomes"] for row in right_rows],
            "collision outcome labels",
        )
        total_variations[plan] = (
            sum(
                (abs(b["probability"] - a["probability"]) for a, b in zip(left_rows, right_rows)),
                Fraction(0),
            )
            / 2
        )
    _require(any(value != 0 for value in coefficient_difference), "different full coefficients")
    _require(omitted_states[0] != omitted_states[1], "different omitted-site states")
    _require(target_difference == 0 and total_variations["target4"] == 0, "target collision")
    _require(total_variations["repair5"] > 0, "visible difference with omitted site restored")
    return {
        "profiles": list(supplied["profiles"]),
        "coefficients_difference": coefficient_difference,
        "full_means_difference": means_difference,
        "target_difference": target_difference,
        "omitted_states": omitted_states,
        "full_averaged_states": averaged_states,
        "full_law_total_variation": total_variations["repair5"],
        "retained_law_total_variation": total_variations["target4"],
    }


def analyze(protocol: dict) -> dict:
    """Compute the frozen target-specific report without historical outputs."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    points = _coordinates(protocol)
    geometry = _geometry(protocol, points)
    reduction = _reduction(protocol, geometry)
    four, four_schedules = _operator_bank(4)
    five, five_schedules = _operator_bank(5)
    operators = {"corner4": four, "five_factor": five}
    plans = _plan_specs(protocol, geometry, reduction)
    _require(type(protocol["profiles"]) is list, "profile list")
    profiles = [
        _profile_report(profile, protocol, points, geometry, reduction, plans, operators)
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
        "reduction": reduction,
        "profiles": profiles,
        "collision": _collision(protocol, profiles, reduction),
        "off_model": _off_model(protocol, points, geometry, reduction, plans, operators),
    }
    _native(report)
    return report
