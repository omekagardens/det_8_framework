"""Exact local Z-record calculation using sparse tensor quantum operations.

Importing this module defines functions only.  Geometry is compiled before any
profile is analyzed; no prior executor, stored answer or record decoder is read.
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
            "outcomes",
            "shots_per_station",
            "profiles",
            "bubble",
            "repeat_control",
            "calibrations",
            "error_control",
            "label_swap",
            "schedule_control",
            "public_context",
            "record_keys",
            "public_estimator_input",
            "quadrature_control",
            "comparison",
            "no_claims",
        ),
    )
    _require(protocol["study"] == "QR-05BC" and protocol["version"] == 1, "protocol version")
    _require(protocol["stations"] == ["00", "10", "01", "11"], "station order")
    _require(protocol["outcomes"] == [-1, 1], "binary outcome order")
    _require(protocol["shots_per_station"] == 1, "one-shot family only")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometry normalization convention",
    )
    profiles = protocol["profiles"]
    _require(type(profiles) is list and len(profiles) == 6, "six profile records required")
    names = []
    for profile in profiles:
        _fields(profile, ("id", "corners"))
        _require(type(profile["id"]) is str and profile["id"], "profile ID")
        _require(type(profile["corners"]) is list and len(profile["corners"]) == 4, "four means")
        for value in profile["corners"]:
            _polarization(value)
        names.append(profile["id"])
    _require(len(set(names)) == len(names), "unique profile IDs")
    bubble = protocol["bubble"]
    _fields(bubble, ("amplitude", "polynomial"))
    _require(0 < _fraction(bubble["amplitude"]) <= 1, "bubble amplitude domain")
    _require(type(bubble["polynomial"]) is list, "bubble polynomial terms")
    powers = []
    for term in bubble["polynomial"]:
        _require(type(term) is list and len(term) == 3, "polynomial term shape")
        i, j, coefficient = term
        _require(type(i) is int and type(j) is int and i >= 0 and j >= 0, "monomial powers")
        _fraction(coefficient)
        powers.append((i, j))
    _require(len(set(powers)) == len(powers), "duplicate monomial term")
    repeat = protocol["repeat_control"]
    _fields(repeat, ("station", "polarization", "shots", "modes"))
    _require(
        repeat["station"] == "00"
        and repeat["shots"] == 2
        and repeat["modes"] == ["fresh", "unreset"],
        "declared two-shot control",
    )
    _polarization(repeat["polarization"])
    calibrations = protocol["calibrations"]
    _require(type(calibrations) is list and len(calibrations) == 4, "four calibration records")
    names = []
    for row in calibrations:
        _fields(row, ("id", "polarization", "alpha", "beta"))
        _require(type(row["id"]) is str and row["id"], "calibration ID")
        _polarization(row["polarization"])
        _require(0 <= _fraction(row["alpha"]) <= 1, "alpha probability")
        _require(0 <= _fraction(row["beta"]) <= 1, "beta probability")
        names.append(row["id"])
    _require(len(set(names)) == len(names), "unique calibration IDs")
    error = protocol["error_control"]
    _fields(error, ("epsilon", "corner_errors", "profile_error"))
    _require(
        _fraction(error["epsilon"]) >= 0 and error["profile_error"] == "bubble", "error domain"
    )
    _require(
        type(error["corner_errors"]) is list and len(error["corner_errors"]) == 4, "four errors"
    )
    for value in error["corner_errors"]:
        _fraction(value)
    _require(protocol["label_swap"] == ["00", "11"], "declared label swap")


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


def _compile_geometry(protocol):
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


def _repeat(control):
    mean = _polarization(control["polarization"])
    single = _state(mean)
    fresh, size = _tensor(single, 2, single, 2)
    rows, estimates, fresh_probabilities, unreset_probabilities = [], [], [], []
    for x, y in product((-1, 1), repeat=2):
        first, second = _projector(x), _projector(y)
        independent, _ = _tensor(first, 2, second, 2)
        sequential = _matrix_multiply(second, first)
        fresh_branch = _matrix_multiply(_matrix_multiply(independent, fresh), _adjoint(independent))
        repeated_branch = _matrix_multiply(
            _matrix_multiply(sequential, single), _adjoint(sequential)
        )
        _diagonal(fresh_branch, size)
        _diagonal(repeated_branch, 2)
        pf, pu = _trace(fresh_branch, size), _trace(repeated_branch, 2)
        rows.append({"outcomes": [x, y], "fresh_probability": pf, "unreset_probability": pu})
        fresh_probabilities.append(pf)
        unreset_probabilities.append(pu)
        estimates.append(F(x + y, 2))
    _require(
        sum(fresh_probabilities, F(0)) == sum(unreset_probabilities, F(0)) == 1, "two-shot laws"
    )
    mf, vf = _moments(fresh_probabilities, estimates)
    mu, vu = _moments(unreset_probabilities, estimates)
    _require(mf == mu == mean, "two-shot estimator mean")
    return {
        "rows": rows,
        "fresh_mean": mf,
        "unreset_mean": mu,
        "fresh_variance": vf,
        "unreset_variance": vu,
    }


def _calibration(row):
    mean = _polarization(row["polarization"])
    alpha, beta = _fraction(row["alpha"]), _fraction(row["beta"])
    state = _state(mean)
    assignments, observed = [], [F(0), F(0)]
    for true, registered in product((-1, 1), repeat=2):
        projector = _projector(true)
        branch = _matrix_multiply(_matrix_multiply(projector, state), _adjoint(projector))
        true_probability = _trace(branch, 2)
        conditional = (
            (alpha if registered == -1 else 1 - alpha)
            if true == 1
            else (beta if registered == 1 else 1 - beta)
        )
        probability = true_probability * conditional
        assignments.append({"true": true, "registered": registered, "probability": probability})
        observed[(registered + 1) // 2] += probability
    offset, contrast = beta - alpha, 1 - alpha - beta
    observed_mean = observed[1] - observed[0]
    _require(
        sum(observed, F(0)) == 1 and all(p >= 0 for p in observed), "registered assignment law"
    )
    _require(observed_mean == offset + contrast * mean, "assignment-affine identity")
    corrected = None if contrast == 0 else (observed_mean - offset) / contrast
    _require(corrected is None or corrected == mean, "known-calibration inversion")
    return {
        "id": row["id"],
        "true_mean": mean,
        "alpha": alpha,
        "beta": beta,
        "offset": offset,
        "contrast": contrast,
        "assignments": assignments,
        "observed_law": observed,
        "observed_mean": observed_mean,
        "corrected_mean": corrected,
    }


def analyze(protocol):
    """Return the complete exact report for the declared finite BC protocol."""
    _validate(protocol)
    bounds, measure, basis, kernel, coordinates, normalization, geometry = _compile_geometry(
        protocol
    )
    weights = geometry["weights"]
    outcomes = list(product((-1, 1), repeat=4))
    matrices, operators, schedule_count = _operators(4, outcomes)
    swap = list(range(4))
    a, b = (protocol["stations"].index(name) for name in protocol["label_swap"])
    swap[a], swap[b] = swap[b], swap[a]
    relabeled_weights = [weights[j] for j in swap]
    profiles = []
    for supplied in protocol["profiles"]:
        corners = [_polarization(x) for x in supplied["corners"]]
        poly = {}
        for value, function in zip(corners, basis, strict=True):
            poly = _poly_add(poly, _poly_scale(function, value))
        integrand = _poly_multiply(poly, kernel)
        target = normalization * _integral(integrand, bounds, measure)
        naive = (
            normalization
            * measure
            * (bounds[1] - bounds[0])
            * (bounds[3] - bounds[2])
            * sum(
                (_poly_value(integrand, u, v) for u, v in coordinates),
                F(0),
            )
            / 4
        )
        _require(
            target == _dot(weights, corners),
            "independent profile integration and corner functional",
        )
        probabilities, states = _branches(corners, matrices)
        rows, estimates, wrong, histogram = [], [], [], [F(0)] * 5
        for record, probability, state in zip(outcomes, probabilities, states, strict=True):
            estimate = _dot(weights, record)
            swapped = [record[j] for j in swap]
            swapped_estimate = _dot(weights, swapped)
            relabeled = _dot(relabeled_weights, swapped)
            _require(relabeled == estimate, "joint outcome/weight relabeling")
            rows.append(
                {
                    "outcomes": list(record),
                    "probability": probability,
                    "state_diagonal": list(state),
                    "estimate": estimate,
                    "swapped_estimate": swapped_estimate,
                    "relabeled_estimate": relabeled,
                }
            )
            estimates.append(estimate)
            wrong.append(swapped_estimate)
            histogram[sum(x == 1 for x in record)] += probability
        reconstructed = [
            sum((p * record[j] for p, record in zip(probabilities, outcomes, strict=True)), F(0))
            for j in range(4)
        ]
        mean, variance = _moments(probabilities, estimates)
        _require(
            reconstructed == corners and mean == target,
            "physical corner means and unbiased estimator",
        )
        _require(
            variance
            == sum((w * w * (1 - f * f) for w, f in zip(weights, corners, strict=True)), F(0)),
            "independent-shot variance identity",
        )
        profiles.append(
            {
                "id": supplied["id"],
                "corners": corners,
                "target": target,
                "naive_target": naive,
                "rows": rows,
                "mean": mean,
                "variance": variance,
                "swapped_mean": _dot(probabilities, wrong),
                "histogram_law": histogram,
                "reconstructed_corner_means": reconstructed,
            }
        )
    bubble_input = protocol["bubble"]
    amplitude = _fraction(bubble_input["amplitude"])
    bubble_poly = {
        (i, j): _fraction(coefficient) for i, j, coefficient in bubble_input["polynomial"]
    }
    expected_bubble = _poly_multiply(_poly_multiply(basis[0], basis[3]), {(0, 0): F(1)})
    _require(bubble_poly == expected_bubble, "declared unit-rectangle bubble polynomial")
    bubble_poly = _poly_scale(bubble_poly, amplitude)
    bubble_corners = [_poly_value(bubble_poly, u, v) for u, v in coordinates]
    _require(all(f == 0 for f in bubble_corners), "bubble vanishes at all observed stations")
    bubble_target = normalization * _integral(_poly_multiply(bubble_poly, kernel), bounds, measure)
    _require(bubble_target > 0, "interior bubble changes the target")
    bubble_probabilities, bubble_states = _branches(bubble_corners, matrices)
    error_input = protocol["error_control"]
    epsilon = _fraction(error_input["epsilon"])
    errors = [_fraction(x) for x in error_input["corner_errors"]]
    _require(epsilon >= amplitude / 16, "declared elementary bubble error bound")
    reconstruction = _dot(weights, errors)
    field_envelope = epsilon * geometry["weight_sum"]
    readout_envelope = sum((abs(w) * abs(e) for w, e in zip(weights, errors, strict=True)), F(0))
    signed_error = reconstruction - bubble_target
    bound = field_envelope + readout_envelope
    _require(abs(signed_error) <= bound, "conditional error-composition envelope")
    return {
        "geometry": geometry,
        "operators": operators,
        "schedule_count": schedule_count,
        "schedule_discrepancies": [],
        "profiles": profiles,
        "bubble": {
            "corners": bubble_corners,
            "target": bubble_target,
            "probabilities": bubble_probabilities,
            "state_diagonals": bubble_states,
        },
        "repeat": _repeat(protocol["repeat_control"]),
        "calibrations": [_calibration(row) for row in protocol["calibrations"]],
        "error": {
            "epsilon": epsilon,
            "corner_errors": errors,
            "field_target": bubble_target,
            "bound": bound,
            "signed_error": signed_error,
            "reconstruction_term": reconstruction,
            "field_envelope": field_envelope,
            "readout_envelope": readout_envelope,
        },
    }
