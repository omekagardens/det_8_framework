"""Exact known-placement access certificates with sparse quantum branches.

Only definitions are evaluated at import.  Local helpers are statically adapted
from the preceding primary; no old executor or stored result is imported.
"""

from fractions import Fraction as F
from itertools import product


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
            "retained_indices",
            "omitted_index",
            "outcomes",
            "placements",
            "profile_rule",
            "admission_rule",
            "profiles",
            "collision",
            "stale_weights",
            "candidate_rule",
            "residual_orientation",
            "marginalization",
            "comparison",
            "third_oracle",
            "public_boundary",
            "no_claims",
        ),
    )
    _require(protocol["study"] == "QR-05BF" and protocol["version"] == 1, "protocol version")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometric conventions",
    )
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station order")
    _require(
        protocol["corners"] == [["0", "0"], ["1", "0"], ["0", "1"], ["1", "1"]],
        "fixed corner positions",
    )
    _require(
        protocol["retained_indices"] == [0, 1, 2, 4] and protocol["omitted_index"] == 3,
        "retained and omitted factors",
    )
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    placements = protocol["placements"]
    _require(type(placements) is list and len(placements) == 6, "six known placements")
    names = []
    for placement in placements:
        _fields(placement, ("id", "position"))
        _require(type(placement["id"]) is str and placement["id"], "placement identifier")
        _require(
            type(placement["position"]) is list and len(placement["position"]) == 2,
            "two coordinates",
        )
        _require(
            all(0 < _fraction(x) < 1 for x in placement["position"]),
            "strictly interior invertible placement",
        )
        names.append(placement["id"])
    _require(len(set(names)) == len(names), "unique placement identifiers")
    profiles = protocol["profiles"]
    _require(type(profiles) is list and len(profiles) == 4, "four base profiles")
    names = []
    for profile in profiles:
        _fields(profile, ("id", "corners", "theta"))
        corners, theta = _parameters(profile)
        _require(_admission(corners, theta) <= 1, "outside sufficient profile domain")
        names.append(profile["id"])
    _require(len(set(names)) == len(names), "unique base profile identifiers")
    collision = protocol["collision"]
    _fields(collision, ("ids", "rule"))
    _require(
        collision["ids"] == ["collision_minus", "collision_plus"]
        and not any(name in names for name in collision["ids"]),
        "ordered collision identifiers",
    )
    _require(
        type(protocol["stale_weights"]) is list and len(protocol["stale_weights"]) == 4,
        "four supplied stale weights",
    )
    for value in protocol["stale_weights"]:
        _fraction(value)


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


def _rank(matrix):
    rows = [list(row) for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0]) if rows else 0):
        candidates = [i for i in range(pivot_row, len(rows)) if rows[i][column]]
        if not candidates:
            continue
        chosen = candidates[0]
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [entry / divisor for entry in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row:
                scale = rows[i][column]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def _compile_geometry(protocol):
    bounds, measure, basis, kernel, corners, normalization, summary = _base_geometry(protocol)
    bubble = _poly_multiply(basis[0], basis[3])
    integrals = [
        normalization * _integral(_poly_multiply(function, kernel), bounds, measure)
        for function in [*basis, bubble]
    ]
    _require(integrals[:4] == summary["weights"], "independent coefficient integrals")
    _require(integrals[3] > 0 and integrals[4] > 0, "positive locus denominator and numerator")
    result = {
        "volume": summary["volume"],
        "sigma": summary["sigma"],
        "coefficient_integrals": integrals,
        "stale_weights": [_fraction(value) for value in protocol["stale_weights"]],
        "equality_threshold": integrals[4] / integrals[3],
        "retained_indices": list(protocol["retained_indices"]),
        "omitted_index": protocol["omitted_index"],
    }
    return result, bounds, measure, basis, bubble, kernel, corners, normalization


def _placement_certificate(supplied, geometry, basis, bubble, corners):
    position = [_fraction(value) for value in supplied["position"]]
    sites = [*corners, position]
    functions = [*basis, bubble]
    evaluation = [[_poly_value(function, *site) for function in functions] for site in sites]
    decoder = _inverse(evaluation)
    left, right = _dense_product(decoder, evaluation), _dense_product(evaluation, decoder)
    identity = _dense_identity(5)
    _require(left == identity and right == identity, "both population inverse identities")
    q = geometry["coefficient_integrals"]
    full_weights = _dense_product([q], decoder)[0]
    full_residual = [
        a - b for a, b in zip(_dense_product([full_weights], evaluation)[0], q, strict=True)
    ]
    _require(all(value == 0 for value in full_residual), "restored full target response")
    retained, omitted = geometry["retained_indices"], geometry["omitted_index"]
    reduced = [list(evaluation[i]) for i in retained]
    rank = _rank(reduced)
    direction = [row[omitted] for row in decoder]
    null_image = [_dot(row, direction) for row in reduced]
    target_image = _dot(q, direction)
    _require(
        rank == 4 and all(value == 0 for value in null_image), "one omitted coefficient direction"
    )
    _require(direction[:4] == [F(0), F(0), F(0), F(1)], "corner part of omitted direction")
    _require(direction[4] == -evaluation[4][3] / evaluation[4][4], "independent block direction")
    candidate = [full_weights[i] for i in retained]
    stale_residual = [
        a - b
        for a, b in zip(_dense_product([geometry["stale_weights"]], reduced)[0], q, strict=True)
    ]
    candidate_residual = [
        a - b for a, b in zip(_dense_product([candidate], reduced)[0], q, strict=True)
    ]
    expected_residual = [F(0)] * 5
    expected_residual[omitted] = -full_weights[omitted]
    _require(
        candidate_residual == expected_residual and full_weights[omitted] == target_image,
        "complete candidate residual and target-null identity",
    )
    denominator = (1 - position[0]) * (1 - position[1])
    locus_residual = denominator - geometry["equality_threshold"]
    _require(target_image == q[3] - q[4] / denominator, "independent target equality locus")
    identified = target_image == 0
    _require(
        identified == all(value == 0 for value in candidate_residual)
        and identified == (locus_residual == 0),
        "equivalent target-identification certificates",
    )
    delta = 1 / (2 * (1 + abs(direction[4]) / 16))
    _require(
        delta > 0
        and _admission([delta * x for x in direction[:4]], delta * direction[4]) == F(1, 2),
        "conservative physical collision scale",
    )
    result = {
        "id": supplied["id"],
        "position": position,
        "basis": list(evaluation[4]),
        "evaluation_matrix": evaluation,
        "coefficient_decoder": decoder,
        "left_inverse": left,
        "right_inverse": right,
        "full_weights": full_weights,
        "full_residual": full_residual,
        "retained_evaluation_matrix": reduced,
        "retained_rank": rank,
        "omission_direction": direction,
        "retained_null_image": null_image,
        "target_null_image": target_image,
        "locus_residual": locus_residual,
        "stale_residual": stale_residual,
        "candidate_weights": candidate,
        "candidate_residual": candidate_residual,
        "recovery_status": "identified" if identified else "not_identified",
        "collision_scale": delta,
    }
    return result, sites


def _score(probabilities, estimates, target):
    mean, variance = _moments(probabilities, estimates)
    bias = mean - target
    return {"mean": mean, "bias": bias, "variance": variance, "mse": variance + bias**2}


def _check_population_score(score, weights, means):
    _require(score["mean"] == _dot(weights, means), "linear score mean")
    independent_variance = sum(
        (weight**2 * (1 - mean**2) for weight, mean in zip(weights, means, strict=True)), F(0)
    )
    _require(score["variance"] == independent_variance, "fresh-copy variance")


def _partial_trace(matrix, count, omitted):
    full_basis = list(product((0, 1), repeat=count))
    remaining = list(product((0, 1), repeat=count - 1))
    indices = {bits: i for i, bits in enumerate(remaining)}
    _require(type(omitted) is int and 0 <= omitted < count, "partial-trace factor")
    answer = {}
    for (i, j), value in matrix.items():
        _require(0 <= i < len(full_basis) and 0 <= j < len(full_basis), "trace matrix index")
        first, second = full_basis[i], full_basis[j]
        if first[omitted] == second[omitted]:
            row = indices[first[:omitted] + first[omitted + 1 :]]
            column = indices[second[:omitted] + second[omitted + 1 :]]
            key = (row, column)
            answer[key] = answer.get(key, F(0)) + value
    return {key: value for key, value in answer.items() if value}


def _marginalize(reduced, full, reduced_branches, full_branches, geometry, placement):
    retained, omitted = geometry["retained_indices"], geometry["omitted_index"]
    rows, nonzero = [], 0
    for j, direct in enumerate(reduced["rows"]):
        indices = [
            i
            for i, row in enumerate(full["rows"])
            if [row["outcomes"][k] for k in retained] == direct["outcomes"]
        ]
        _require(len(indices) == 2, "complete omitted-outcome fiber")
        summed = {}
        probability, differences = F(0), []
        for i in indices:
            row = full["rows"][i]
            probability += row["probability"]
            summed = _matrix_add(summed, full_branches[i])
            difference = row["estimate"] - direct["candidate_estimate"]
            _require(
                difference == placement["full_weights"][omitted] * row["outcomes"][omitted],
                "pathwise missing-weight diagnostic",
            )
            differences.append(difference)
            if difference != 0:
                nonzero += 1
        trace = _partial_trace(summed, 5, omitted)
        _require(trace == reduced_branches[j], "exact sparse subsystem marginal")
        _require(
            probability == direct["probability"] == _trace(summed, 32) == _trace(trace, 16),
            "direct versus marginal probability and trace",
        )
        diagonal = _diagonal(trace, 16)
        _require(diagonal == direct["state_diagonal"], "retained subsystem basis order")
        rows.append(
            {
                "outcomes": list(direct["outcomes"]),
                "full_indices": indices,
                "probability": probability,
                "summed_full_state": _diagonal(summed, 32),
                "reduced_state": diagonal,
                "full_minus_candidate": differences,
            }
        )
    if placement["recovery_status"] == "identified":
        _require(nonzero == 0, "identified target has pathwise estimator preservation")
    return {"rows": rows, "pathwise_nonzero_count": nonzero}


def _profile(name, coefficients, sites, geometry, placement, polynomial_data, instruments):
    bounds, measure, basis, bubble, kernel, normalization = polynomial_data
    corners, theta = coefficients[:4], coefficients[4]
    admission = _admission(corners, theta)
    _require(admission <= 1, "sufficient global physical domain")
    profile = _model_polynomial(corners, theta, basis, bubble)
    means = [_poly_value(profile, *site) for site in sites]
    _require(all(-1 <= mean <= 1 for mean in means), "physical sampled states")
    _require(
        [_dot(row, coefficients) for row in placement["evaluation_matrix"]] == means,
        "polynomial and population evaluation agree",
    )
    recovered = [_dot(row, means) for row in placement["coefficient_decoder"]]
    _require(recovered == coefficients, "full-access population coefficient recovery")
    target = normalization * _integral(_poly_multiply(profile, kernel), bounds, measure)
    _require(
        target == _dot(geometry["coefficient_integrals"], coefficients), "integrated target row"
    )
    retained_means = [means[i] for i in geometry["retained_indices"]]
    probabilities, states, reduced_branches = _branches(retained_means, instruments[4])
    reduced_rows, stale_values, candidate_values = [], [], []
    for outcomes, probability, state in zip(
        product((-1, 1), repeat=4), probabilities, states, strict=True
    ):
        stale = _dot(geometry["stale_weights"], outcomes)
        candidate = _dot(placement["candidate_weights"], outcomes)
        stale_values.append(stale)
        candidate_values.append(candidate)
        reduced_rows.append(
            {
                "outcomes": list(outcomes),
                "probability": probability,
                "state_diagonal": list(state),
                "stale_estimate": stale,
                "candidate_estimate": candidate,
            }
        )
    reduced = {
        "rows": reduced_rows,
        "stale": _score(probabilities, stale_values, target),
        "candidate": _score(probabilities, candidate_values, target),
    }
    for key, weights in (
        ("stale", geometry["stale_weights"]),
        ("candidate", placement["candidate_weights"]),
    ):
        _check_population_score(reduced[key], weights, retained_means)
        residual = placement[key + "_residual"]
        _require(reduced[key]["bias"] == _dot(residual, coefficients), "complete row-residual bias")
    full_probabilities, full_states, full_branches = _branches(means, instruments[5])
    full_rows, values = [], []
    for outcomes, probability, state in zip(
        product((-1, 1), repeat=5), full_probabilities, full_states, strict=True
    ):
        estimate = _dot(placement["full_weights"], outcomes)
        values.append(estimate)
        full_rows.append(
            {
                "outcomes": list(outcomes),
                "probability": probability,
                "state_diagonal": list(state),
                "estimate": estimate,
            }
        )
    full = {"rows": full_rows, **_score(full_probabilities, values, target)}
    _check_population_score(full, placement["full_weights"], means)
    _require(full["mean"] == target and full["bias"] == 0, "restored full target identification")
    report = {
        "id": name,
        "coefficients": list(coefficients),
        "admission_bound": admission,
        "sample_means": means,
        "recovered_coefficients": recovered,
        "target": target,
        "reduced": reduced,
        "full": full,
        "marginalization": _marginalize(
            reduced, full, reduced_branches, full_branches, geometry, placement
        ),
    }
    return report, full_branches


def _tv(first, second):
    return (
        sum(
            (
                abs(a["probability"] - b["probability"])
                for a, b in zip(first["rows"], second["rows"], strict=True)
            ),
            F(0),
        )
        / 2
    )


def _collision(names, profiles, branch_sets, geometry, placement):
    indexed = {profile["id"]: profile for profile in profiles}
    first, second = (indexed[name] for name in names)
    difference = [b - a for a, b in zip(first["coefficients"], second["coefficients"], strict=True)]
    means_difference = [
        b - a for a, b in zip(first["sample_means"], second["sample_means"], strict=True)
    ]
    target_difference = second["target"] - first["target"]
    predicted = 2 * placement["collision_scale"] * placement["target_null_image"]
    _require(target_difference == predicted, "signed physical target collision")
    _require(
        difference
        == [2 * placement["collision_scale"] * x for x in placement["omission_direction"]],
        "complete signed coefficient collision",
    )
    omitted = geometry["omitted_index"]
    omitted_states = [_diagonal(_state(row["sample_means"][omitted]), 2) for row in (first, second)]
    averaged = []
    for name, report in zip(names, (first, second), strict=True):
        total = {}
        for branch in branch_sets[name]:
            total = _matrix_add(total, branch)
        preparation, size = _tensor_state(report["sample_means"])
        _require(total == preparation and size == 32, "outcome-averaged full state")
        averaged.append(_diagonal(total, size))
    full_tv, reduced_tv = (
        _tv(first["full"], second["full"]),
        _tv(first["reduced"], second["reduced"]),
    )
    _require(
        all(
            first["sample_means"][i] == second["sample_means"][i] == 0
            for i in geometry["retained_indices"]
        ),
        "null-direction retained means",
    )
    _require(
        first["reduced"]["rows"] == second["reduced"]["rows"] and reduced_tv == 0,
        "complete retained collision law and branch state",
    )
    _require(
        omitted_states[0] != omitted_states[1] and averaged[0] != averaged[1] and full_tv > 0,
        "distinct omitted and full information",
    )
    _require(
        (target_difference == 0) == (placement["recovery_status"] == "identified"),
        "profile collision versus target ambiguity",
    )
    return {
        "profiles": list(names),
        "coefficients_difference": difference,
        "full_means_difference": means_difference,
        "target_difference": target_difference,
        "predicted_target_difference": predicted,
        "omitted_states": omitted_states,
        "full_averaged_states": averaged,
        "full_law_total_variation": full_tv,
        "retained_law_total_variation": reduced_tv,
    }


def analyze(protocol):
    """Return exact access certificates; no fixed evaluation occurs on import."""
    _validate(protocol)
    geometry, bounds, measure, basis, bubble, kernel, corners, normalization = _compile_geometry(
        protocol
    )
    instruments = {count: _instrument(count) for count in (4, 5)}
    polynomial_data = bounds, measure, basis, bubble, kernel, normalization
    placements = []
    for supplied in protocol["placements"]:
        placement, sites = _placement_certificate(supplied, geometry, basis, bubble, corners)
        requested = []
        for profile in protocol["profiles"]:
            coefficients, theta = _parameters(profile)
            requested.append((profile["id"], [*coefficients, theta]))
        for name, sign in zip(protocol["collision"]["ids"], (-1, 1), strict=True):
            coefficients = [
                sign * placement["collision_scale"] * x for x in placement["omission_direction"]
            ]
            _require(
                _admission(coefficients[:4], coefficients[4]) == F(1, 2), "collision admission"
            )
            requested.append((name, coefficients))
        reports, branches = [], {}
        for name, coefficients in requested:
            report, full_branches = _profile(
                name, coefficients, sites, geometry, placement, polynomial_data, instruments
            )
            reports.append(report)
            branches[name] = full_branches
        placement["profiles"] = reports
        placement["collision"] = _collision(
            protocol["collision"]["ids"], reports, branches, geometry, placement
        )
        placements.append(placement)
    return {"geometry": geometry, "placements": placements}
