"""Independent exact Bernoulli/beta-moment route for QR-05BC.

This module has no import-time execution or dependency on another study engine.
The geometry uses factorized beta integrals; instrument diagonals are built
from computational-basis indicators, independently of the probability route.
"""

from fractions import Fraction
from itertools import permutations, product
from math import factorial


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Reject non-native containers/scalars, floats, booleans and cycles."""
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
        raise ValueError("invalid rational value") from exc


def _mean(value):
    result = _fraction(value)
    _require(-1 <= result <= 1, "polarization outside [-1,1]")
    return result


def _probability(value):
    result = _fraction(value)
    _require(0 <= result <= 1, "probability outside [0,1]")
    return result


def _record(value, keys, name):
    _require(type(value) is dict and set(value) == set(keys), name)


def _vector(value, size, name):
    _require(type(value) is list and len(value) == size, name)


def _multiply(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _dot(left, right):
    _require(len(left) == len(right), "dot-product dimension")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _beta_moment(power, complement_power):
    """Integral of x**power * (1-x)**complement_power over [0,1]."""
    _require(
        type(power) is int
        and type(complement_power) is int
        and power >= 0
        and complement_power >= 0,
        "nonnegative integer exponents required",
    )
    return Fraction(
        factorial(power) * factorial(complement_power),
        factorial(power + complement_power + 1),
    )


def _compile_geometry(protocol):
    geometry = protocol["geometry"]
    _record(
        geometry,
        ("u", "v", "measure_factor", "sigma_rule", "field_rule"),
        "geometry fields",
    )
    _vector(geometry["u"], 2, "u bounds")
    _vector(geometry["v"], 2, "v bounds")
    u0, u1 = map(_fraction, geometry["u"])
    v0, v1 = map(_fraction, geometry["v"])
    measure = _fraction(geometry["measure_factor"])
    _require((u0, u1, v0, v1) == (0, 1, 0, 1), "unit rectangle required")
    _require(measure == Fraction(1, 2), "declared null-coordinate measure")
    _require(geometry["sigma_rule"] == "V^4", "sigma rule")
    _require(geometry["field_rule"] == "F=V^2*f", "field rule")
    stations = protocol["stations"]
    _require(stations == ["00", "10", "01", "11"], "station order")
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    _require(protocol["shots_per_station"] == 1, "one-shot protocol")
    volume = measure * (u1 - u0) * (v1 - v0)
    sigma = volume**4
    # R contributes V*(1-u)*(1-v), while dmu contributes V du dv.
    factor = volume**4 / sigma
    weights = []
    for station in stations:
        i, j = (int(symbol) for symbol in station)
        weights.append(factor * _beta_moment(i, 2 - i) * _beta_moment(j, 2 - j))
    return {
        "volume": volume,
        "sigma": sigma,
        "weights": weights,
        "weight_sum": sum(weights, Fraction(0)),
    }


def _probabilities(polarizations, outcomes):
    return [
        _multiply((1 + sign * mean) / 2 for sign, mean in zip(row, polarizations))
        for row in outcomes
    ]


def _density_diagonal(polarizations, basis):
    return [
        _multiply((1 + (1 - 2 * bit) * mean) / 2 for bit, mean in zip(bits, polarizations))
        for bits in basis
    ]


def _kraus_diagonal(outcomes, basis, order):
    diagonal = []
    for bits in basis:
        value = Fraction(1)
        for station in order:
            indicator = Fraction(int(outcomes[station] == 1 - 2 * bits[station]))
            value *= indicator
        diagonal.append(value)
    return diagonal


def _operators(outcomes, basis):
    operators = [
        {
            "outcomes": list(row),
            "kraus_diagonal": _kraus_diagonal(row, basis, range(4)),
        }
        for row in outcomes
    ]
    schedules = list(permutations(range(4)))
    for schedule in schedules:
        for row, operator in zip(outcomes, operators):
            _require(
                _kraus_diagonal(row, basis, schedule) == operator["kraus_diagonal"],
                "station order changes a full outcome operator",
            )
    return operators, len(schedules)


def _branch_states(polarizations, basis, operators):
    density = _density_diagonal(polarizations, basis)
    return [
        [rho * entry * entry for rho, entry in zip(density, operator["kraus_diagonal"])]
        for operator in operators
    ]


def _direct_bilinear_target(corners, stations, geometry):
    """Integrate the interpolated response afresh, without reading weights."""
    total = Fraction(0)
    for mean, station in zip(corners, stations):
        u_power, v_power = (int(symbol) for symbol in station)
        contribution = mean * _beta_moment(u_power, 2 - u_power)
        contribution *= _beta_moment(v_power, 2 - v_power)
        total += contribution
    return geometry["volume"] ** 4 * total / geometry["sigma"]


def _naive_target(corners, stations, geometry):
    nodal_sum = Fraction(0)
    for mean, station in zip(corners, stations):
        u, v = (int(symbol) for symbol in station)
        nodal_sum += mean * (1 - u) * (1 - v)
    return geometry["volume"] ** 4 * nodal_sum / (4 * geometry["sigma"])


def _profile_report(profile, protocol, geometry, outcomes, basis, operators):
    _record(profile, ("id", "corners"), "profile fields")
    _require(type(profile["id"]) is str and profile["id"], "profile identifier")
    _vector(profile["corners"], 4, "profile corner count")
    corners = [_mean(value) for value in profile["corners"]]
    probabilities = _probabilities(corners, outcomes)
    states = _branch_states(corners, basis, operators)
    weights = geometry["weights"]
    _vector(protocol["label_swap"], 2, "label swap")
    left, right = (protocol["stations"].index(label) for label in protocol["label_swap"])
    _require(left != right, "distinct swap stations")
    relabeled_weights = list(weights)
    relabeled_weights[left], relabeled_weights[right] = weights[right], weights[left]
    rows = []
    histogram_law = [Fraction(0) for _ in range(5)]
    for outcome, probability, state in zip(outcomes, probabilities, states):
        _require(sum(state, Fraction(0)) == probability, "branch trace/probability")
        swapped = list(outcome)
        swapped[left], swapped[right] = outcome[right], outcome[left]
        estimate = _dot(weights, outcome)
        relabeled_estimate = _dot(relabeled_weights, swapped)
        _require(relabeled_estimate == estimate, "joint relabeling")
        rows.append(
            {
                "outcomes": list(outcome),
                "probability": probability,
                "state_diagonal": state,
                "estimate": estimate,
                "swapped_estimate": _dot(weights, swapped),
                "relabeled_estimate": relabeled_estimate,
            }
        )
        histogram_law[sum(sign == 1 for sign in outcome)] += probability
    _require(sum(probabilities, Fraction(0)) == 1, "profile law normalization")
    mean = sum((row["probability"] * row["estimate"] for row in rows), Fraction(0))
    variance = sum(
        (row["probability"] * (row["estimate"] - mean) ** 2 for row in rows),
        Fraction(0),
    )
    target = _direct_bilinear_target(corners, protocol["stations"], geometry)
    _require(mean == target, "record mean/direct target")
    _require(
        variance == sum((w * w * (1 - f * f) for w, f in zip(weights, corners)), Fraction(0)),
        "independent-shot variance",
    )
    return {
        "id": profile["id"],
        "corners": corners,
        "target": target,
        "naive_target": _naive_target(corners, protocol["stations"], geometry),
        "rows": rows,
        "mean": mean,
        "variance": variance,
        "swapped_mean": sum(
            (row["probability"] * row["swapped_estimate"] for row in rows), Fraction(0)
        ),
        "histogram_law": histogram_law,
        "reconstructed_corner_means": [
            sum((p * row[station] for p, row in zip(probabilities, outcomes)), Fraction(0))
            for station in range(4)
        ],
    }


def _bubble_report(protocol, geometry, outcomes, basis, operators):
    bubble = protocol["bubble"]
    _record(bubble, ("amplitude", "polynomial"), "bubble fields")
    amplitude = _fraction(bubble["amplitude"])
    _require(0 < amplitude <= 1, "bubble amplitude")
    _require(type(bubble["polynomial"]) is list, "bubble polynomial")
    terms = []
    for term in bubble["polynomial"]:
        _vector(term, 3, "bubble term")
        i, j, coefficient = term
        _require(type(i) is int and type(j) is int and i >= 0 and j >= 0, "bubble exponent")
        terms.append((i, j, _fraction(coefficient)))
    corners = []
    for station in protocol["stations"]:
        u, v = (int(symbol) for symbol in station)
        corners.append(
            amplitude * sum((coefficient * u**i * v**j for i, j, coefficient in terms), Fraction(0))
        )
    target = (
        geometry["volume"] ** 4
        / geometry["sigma"]
        * amplitude
        * sum(
            (coefficient * _beta_moment(i, 1) * _beta_moment(j, 1) for i, j, coefficient in terms),
            Fraction(0),
        )
    )
    return {
        "corners": corners,
        "target": target,
        "probabilities": _probabilities(corners, outcomes),
        "state_diagonals": _branch_states(corners, basis, operators),
    }


def _repeat_report(protocol):
    control = protocol["repeat_control"]
    _record(control, ("station", "polarization", "shots", "modes"), "repeat fields")
    _require(control["station"] in protocol["stations"], "repeat station")
    _require(control["shots"] == 2 and control["modes"] == ["fresh", "unreset"], "repeat domain")
    polarization = _mean(control["polarization"])
    rows = []
    estimates = []
    for first, second in product((-1, 1), repeat=2):
        first_probability = (1 + first * polarization) / 2
        fresh = first_probability * (1 + second * polarization) / 2
        unreset = first_probability * int(first == second)
        rows.append(
            {
                "outcomes": [first, second],
                "fresh_probability": fresh,
                "unreset_probability": unreset,
            }
        )
        estimates.append(Fraction(first + second, 2))
    means = {}
    variances = {}
    for mode in ("fresh", "unreset"):
        probabilities = [row[mode + "_probability"] for row in rows]
        _require(sum(probabilities, Fraction(0)) == 1, "repeat normalization")
        means[mode] = _dot(probabilities, estimates)
        variances[mode] = sum(
            (p * (value - means[mode]) ** 2 for p, value in zip(probabilities, estimates)),
            Fraction(0),
        )
    return {
        "rows": rows,
        "fresh_mean": means["fresh"],
        "unreset_mean": means["unreset"],
        "fresh_variance": variances["fresh"],
        "unreset_variance": variances["unreset"],
    }


def _calibration_report(calibration):
    _record(calibration, ("id", "polarization", "alpha", "beta"), "calibration fields")
    _require(type(calibration["id"]) is str and calibration["id"], "calibration identifier")
    mean = _mean(calibration["polarization"])
    alpha = _probability(calibration["alpha"])
    beta = _probability(calibration["beta"])
    observed = [Fraction(0), Fraction(0)]
    assignments = []
    for true, registered in product((-1, 1), repeat=2):
        if true == 1:
            conditional = alpha if registered == -1 else 1 - alpha
        else:
            conditional = beta if registered == 1 else 1 - beta
        probability = (1 + true * mean) / 2 * conditional
        observed[(registered + 1) // 2] += probability
        assignments.append({"true": true, "registered": registered, "probability": probability})
    observed_mean = observed[1] - observed[0]
    offset = beta - alpha
    contrast = 1 - alpha - beta
    _require(sum(observed, Fraction(0)) == 1, "calibration normalization")
    _require(observed_mean == offset + contrast * mean, "assignment/affine mean")
    return {
        "id": calibration["id"],
        "true_mean": mean,
        "alpha": alpha,
        "beta": beta,
        "offset": offset,
        "contrast": contrast,
        "assignments": assignments,
        "observed_law": observed,
        "observed_mean": observed_mean,
        "corrected_mean": None if contrast == 0 else (observed_mean - offset) / contrast,
    }


def _error_report(protocol, geometry, bubble):
    control = protocol["error_control"]
    _record(control, ("epsilon", "corner_errors", "profile_error"), "error fields")
    _require(control["profile_error"] == "bubble", "declared field error")
    epsilon = _fraction(control["epsilon"])
    _require(epsilon >= 0, "nonnegative field radius")
    _vector(control["corner_errors"], 4, "corner errors")
    errors = [_fraction(value) for value in control["corner_errors"]]
    reconstruction = _dot(geometry["weights"], errors)
    field_envelope = epsilon * geometry["weight_sum"]
    readout_envelope = sum(
        (abs(w) * abs(error) for w, error in zip(geometry["weights"], errors)), Fraction(0)
    )
    signed_error = reconstruction - bubble["target"]
    bound = field_envelope + readout_envelope
    _require(abs(signed_error) <= bound, "supplied error envelope")
    return {
        "epsilon": epsilon,
        "corner_errors": errors,
        "field_target": bubble["target"],
        "bound": bound,
        "signed_error": signed_error,
        "reconstruction_term": reconstruction,
        "field_envelope": field_envelope,
        "readout_envelope": readout_envelope,
    }


def analyze(protocol: dict) -> dict:
    """Compute the complete frozen-study wire from explicit supplied data."""
    _native(protocol)
    _require(type(protocol) is dict, "protocol must be a native dictionary")
    geometry = _compile_geometry(protocol)
    outcomes = list(product((-1, 1), repeat=4))
    basis = list(product((0, 1), repeat=4))
    operators, schedule_count = _operators(outcomes, basis)
    _require(type(protocol["profiles"]) is list, "profiles must be a list")
    profiles = [
        _profile_report(profile, protocol, geometry, outcomes, basis, operators)
        for profile in protocol["profiles"]
    ]
    _require(len({profile["id"] for profile in profiles}) == len(profiles), "duplicate profile")
    bubble = _bubble_report(protocol, geometry, outcomes, basis, operators)
    _require(type(protocol["calibrations"]) is list, "calibrations must be a list")
    calibrations = [_calibration_report(row) for row in protocol["calibrations"]]
    report = {
        "geometry": geometry,
        "operators": operators,
        "schedule_count": schedule_count,
        "schedule_discrepancies": [],
        "profiles": profiles,
        "bubble": bubble,
        "repeat": _repeat_report(protocol),
        "calibrations": calibrations,
        "error": _error_report(protocol, geometry, bubble),
    }
    _native(report)
    return report
