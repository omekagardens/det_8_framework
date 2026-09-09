"""Exact target-specific acquisition reduction using sparse quantum operations.

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
            "coordinates",
            "outcomes",
            "profile_rule",
            "admission_rule",
            "profiles",
            "plans",
            "reduction",
            "reallocation",
            "collision",
            "off_model",
            "schedule_control",
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
    _require(protocol["study"] == "QR-05BE" and protocol["version"] == 1, "protocol version")
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station order")
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometric conventions",
    )
    _require(
        protocol["coordinates"] == [["0", "0"], ["1", "0"], ["0", "1"], ["1", "1"], ["1/2", "1/2"]],
        "five fixed sites",
    )
    profiles = protocol["profiles"]
    _require(type(profiles) is list and len(profiles) == 12, "twelve profiles")
    ids = []
    for profile in profiles:
        _fields(profile, ("id", "corners", "theta"))
        corners, theta = _parameters(profile)
        _require(_admission(corners, theta) <= 1, "outside sufficient profile domain")
        ids.append(profile["id"])
    _require(len(set(ids)) == len(ids), "unique profile identifiers")
    required_plans = [
        ("corner4", [["00", 1], ["10", 1], ["01", 1], ["11", 1]], "corner", 4),
        ("repair5", [["00", 1], ["10", 1], ["01", 1], ["11", 1], ["cc", 1]], "repair", 5),
        ("corner5", [["00", 1], ["00", 2], ["10", 1], ["01", 1], ["11", 1]], "corner", 5),
        ("target4", [["00", 1], ["10", 1], ["01", 1], ["cc", 1]], "reduced", 4),
        ("repeatcc5", [["00", 1], ["10", 1], ["01", 1], ["cc", 1], ["cc", 2]], "reduced", 5),
    ]
    _require(type(protocol["plans"]) is list and len(protocol["plans"]) == 5, "five plans")
    for plan, (name, slots, weights, cost) in zip(protocol["plans"], required_plans, strict=True):
        _fields(plan, ("id", "slots", "weights", "cost"))
        _require(
            plan["id"] == name
            and plan["slots"] == slots
            and plan["weights"] == weights
            and plan["cost"] == cost,
            "fixed acquisition plan",
        )
    reduction = protocol["reduction"]
    _fields(reduction, ("omitted_station", "retained_stations", "rule"))
    _require(
        reduction["omitted_station"] == "11"
        and reduction["retained_stations"] == ["00", "10", "01", "cc"],
        "declared target-specific reduction",
    )
    reallocation = protocol["reallocation"]
    _fields(reallocation, ("station", "rationale", "rule"))
    _require(reallocation["station"] == "cc", "fixed fresh-copy reallocation")
    collision = protocol["collision"]
    _fields(collision, ("profiles", "rule"))
    _require(
        collision["profiles"] == ["collision_minus", "collision_plus"]
        and all(name in ids for name in collision["profiles"]),
        "declared collision pair",
    )
    off = protocol["off_model"]
    _fields(off, ("id", "amplitude", "rule", "global_bound", "plans"))
    _require(type(off["id"]) is str and off["id"], "off-model identifier")
    _require(_fraction(off["amplitude"]) == 1, "fixed off-model amplitude")
    _require(0 < _fraction(off["global_bound"]) <= 1, "physical off-model bound")
    _require(
        off["rule"] == "h=b*((u-1/2)^2+(v-1/2)^2)"
        and off["plans"] == ["repair5", "target4", "repeatcc5"],
        "off-model contract",
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


def _rank(matrix):
    rows = [list(row) for row in matrix]
    width = len(rows[0]) if rows else 0
    pivot_row = 0
    for column in range(width):
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


def _reduction(protocol, geometry):
    stations = protocol["stations"]
    retained = [stations.index(name) for name in protocol["reduction"]["retained_stations"]]
    omitted = stations.index(protocol["reduction"]["omitted_station"])
    evaluation = geometry["evaluation_matrix"]
    reduced = [list(evaluation[i]) for i in retained]
    direction = [row[omitted] for row in geometry["coefficient_decoder"]]
    retained_image = [_dot(row, direction) for row in reduced]
    target_image = _dot([*geometry["corner_weights"], geometry["bubble_target"]], direction)
    rank = _rank(reduced)
    _require(
        rank == len(retained) and rank < len(evaluation), "reduced rank versus full coefficients"
    )
    _require(
        all(x == 0 for x in retained_image) and target_image == 0, "target-null omitted direction"
    )
    _require(geometry["repair_weights"][omitted] == 0, "omitted target coefficient must vanish")
    target_weights = [geometry["repair_weights"][i] for i in retained]
    _require(
        _dense_product([target_weights], reduced)[0]
        == [*geometry["corner_weights"], geometry["bubble_target"]],
        "reduced population target identity",
    )
    return {
        "retained_indices": retained,
        "omitted_index": omitted,
        "retained_evaluation_matrix": reduced,
        "retained_rank": rank,
        "omission_direction": direction,
        "retained_null_image": retained_image,
        "target_null_image": target_image,
        "target_weights": target_weights,
    }


def _compiled_plans(protocol, geometry, reduction):
    full_stations = protocol["stations"]
    choices = {
        "corner": (full_stations[:4], geometry["corner_weights"]),
        "repair": (full_stations, geometry["repair_weights"]),
        "reduced": (protocol["reduction"]["retained_stations"], reduction["target_weights"]),
    }
    result = []
    for supplied in protocol["plans"]:
        names, weights = choices[supplied["weights"]]
        station_weights = dict(zip(names, weights, strict=True))
        multiplicities = {
            name: sum(station == name for station, _ in supplied["slots"]) for name in names
        }
        _require(all(count > 0 for count in multiplicities.values()), "mandatory station shots")
        events = [station_weights[name] / multiplicities[name] for name, _ in supplied["slots"]]
        _require(sum(events, F(0)) == geometry["weight_sum"], "plan constant-profile response")
        result.append(
            {
                "id": supplied["id"],
                "slots": [[station, shot] for station, shot in supplied["slots"]],
                "cost": supplied["cost"],
                "event_weights": events,
            }
        )
    center = full_stations.index(protocol["reallocation"]["station"])
    _require(
        abs(geometry["repair_weights"][center]) == max(map(abs, geometry["repair_weights"])),
        "declared geometric reallocation rationale",
    )
    return result


def _score_plan(means, target, plan, matrices):
    outcomes = list(product((-1, 1), repeat=len(means)))
    probabilities, states, branches = _branches(means, matrices)
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
    independent = sum(
        (
            weight**2 * (1 - polarization**2)
            for weight, polarization in zip(plan["event_weights"], means, strict=True)
        ),
        F(0),
    )
    _require(variance == independent, "fresh independent-copy variance")
    bias = mean - target
    return {
        "rows": rows,
        "mean": mean,
        "bias": bias,
        "variance": variance,
        "mse": variance + bias**2,
    }, branches


def _partial_trace(matrix, count, omitted):
    """Trace one original tensor factor on the complete sparse matrix."""
    _require(type(omitted) is int and 0 <= omitted < count, "partial-trace factor")
    basis = list(product((0, 1), repeat=count))
    kept_basis = list(product((0, 1), repeat=count - 1))
    kept_indices = {bits: i for i, bits in enumerate(kept_basis)}
    answer = {}
    for (i, j), value in matrix.items():
        _require(0 <= i < len(basis) and 0 <= j < len(basis), "partial-trace basis index")
        row_bits, column_bits = basis[i], basis[j]
        if row_bits[omitted] == column_bits[omitted]:
            row = kept_indices[row_bits[:omitted] + row_bits[omitted + 1 :]]
            column = kept_indices[column_bits[:omitted] + column_bits[omitted + 1 :]]
            position = (row, column)
            answer[position] = answer.get(position, F(0)) + value
    return {position: value for position, value in answer.items() if value}


def _marginalization(reports, branches, reduction):
    full, direct = reports["repair5"], reports["target4"]
    retained, omitted = reduction["retained_indices"], reduction["omitted_index"]
    rows = []
    pathwise, wrong_disagreements = 0, 0
    for direct_index, direct_row in enumerate(direct["rows"]):
        outcome = direct_row["outcomes"]
        indices = [
            i
            for i, row in enumerate(full["rows"])
            if [row["outcomes"][j] for j in retained] == outcome
        ]
        _require(len(indices) == 2, "complete omitted-outcome fiber")
        summed = {}
        estimates = []
        probability = F(0)
        for i in indices:
            row = full["rows"][i]
            _require(row["estimate"] == direct_row["estimate"], "pathwise zero-weight omission")
            pathwise += 1
            estimates.append(row["estimate"])
            probability += row["probability"]
            summed = _matrix_add(summed, branches["repair5"][i])
        reduced = _partial_trace(summed, 5, omitted)
        wrong = _partial_trace(summed, 5, 4)
        _require(
            reduced == branches["target4"][direct_index],
            "sparse partial trace equals direct branch",
        )
        _require(
            probability == direct_row["probability"] == _trace(reduced, 16) == _trace(summed, 32),
            "complete marginal law and trace",
        )
        reduced_state, wrong_state = _diagonal(reduced, 16), _diagonal(wrong, 16)
        _require(reduced_state == direct_row["state_diagonal"], "retained subsystem basis")
        if wrong_state != reduced_state:
            wrong_disagreements += 1
        rows.append(
            {
                "outcomes": list(outcome),
                "full_indices": indices,
                "full_estimates": estimates,
                "probability": probability,
                "summed_full_state": _diagonal(summed, 32),
                "reduced_state": reduced_state,
                "wrong_trace_state": wrong_state,
                "estimate": direct_row["estimate"],
            }
        )
    differences = {name: direct[name] - full[name] for name in ("mean", "variance", "mse")}
    _require(all(value == 0 for value in differences.values()), "marginal target moments")
    _require(pathwise == len(full["rows"]), "each full branch checked once")
    return {
        "rows": rows,
        "pathwise_checks": pathwise,
        "wrong_trace_disagreements": wrong_disagreements,
        "moment_differences": differences,
    }


def _reallocation(reports, means, geometry):
    direct_variance = reports["target4"]["variance"] - reports["repeatcc5"]["variance"]
    predicted = geometry["repair_weights"][4] ** 2 * (1 - means[4] ** 2) / 2
    direct_mse = reports["target4"]["mse"] - reports["repeatcc5"]["mse"]
    _require(reports["target4"]["mean"] == reports["repeatcc5"]["mean"], "replication keeps mean")
    _require(
        direct_variance == predicted == direct_mse and predicted >= 0,
        "fixed fresh replication variance and MSE identity",
    )
    return {
        "direct_variance_reduction": direct_variance,
        "predicted_variance_reduction": predicted,
        "direct_mse_reduction": direct_mse,
    }


def _total_variation(left, right):
    return (
        sum(
            (
                abs(a["probability"] - b["probability"])
                for a, b in zip(left["rows"], right["rows"], strict=True)
            ),
            F(0),
        )
        / 2
    )


def _collision(names, profiles, all_branches, reduction):
    indexed = {row["id"]: row for row in profiles}
    first, second = (indexed[name] for name in names)
    coefficients_difference = [
        b - a
        for a, b in zip(
            [*first["corners"], first["theta"]], [*second["corners"], second["theta"]], strict=True
        )
    ]
    full_means_difference = [
        b - a for a, b in zip(first["sample_means"], second["sample_means"], strict=True)
    ]
    target_difference = second["target"] - first["target"]
    omitted = reduction["omitted_index"]
    omitted_states = [_diagonal(_state(row["sample_means"][omitted]), 2) for row in (first, second)]
    averaged = []
    for name, profile in zip(names, (first, second), strict=True):
        complete = {}
        for branch in all_branches[name]["repair5"]:
            complete = _matrix_add(complete, branch)
        prepared, size = _tensor_state(profile["sample_means"])
        _require(complete == prepared and size == 32, "full averaged projective state")
        averaged.append(_diagonal(complete, size))
    full_tv = _total_variation(first["plans"]["repair5"], second["plans"]["repair5"])
    retained_tv = _total_variation(first["plans"]["target4"], second["plans"]["target4"])
    _require(
        any(value != 0 for value in coefficients_difference)
        and omitted_states[0] != omitted_states[1]
        and averaged[0] != averaged[1],
        "omission loses profile and full-state information",
    )
    _require(
        target_difference == 0 and retained_tv == 0 and full_tv > 0,
        "target-specific observational collision",
    )
    _require(
        all(full_means_difference[i] == 0 for i in reduction["retained_indices"]),
        "retained population observations coincide",
    )
    _require(
        first["plans"]["target4"]["rows"] == second["plans"]["target4"]["rows"],
        "complete retained instrument laws coincide",
    )
    return {
        "profiles": list(names),
        "coefficients_difference": coefficients_difference,
        "full_means_difference": full_means_difference,
        "target_difference": target_difference,
        "omitted_states": omitted_states,
        "full_averaged_states": averaged,
        "full_law_total_variation": full_tv,
        "retained_law_total_variation": retained_tv,
    }


def analyze(protocol):
    """Compile geometry, then evaluate only the declared private fixed fixtures."""
    _validate(protocol)
    geometry, bounds, measure, basis, bubble, kernel, sites, normalization = _geometry(protocol)
    reduction = _reduction(protocol, geometry)
    plans = _compiled_plans(protocol, geometry, reduction)
    operators, sparse, schedule_counts = {}, {}, {}
    for name, count in (("corner4", 4), ("five_factor", 5)):
        matrices, rows, orders = _operators(count, list(product((-1, 1), repeat=count)))
        operators[name], sparse[count], schedule_counts[name] = rows, matrices, orders
    station_index = {station: i for i, station in enumerate(protocol["stations"])}
    profiles, all_branches = [], {}
    for supplied in protocol["profiles"]:
        corners, theta = _parameters(supplied)
        profile = _model_polynomial(corners, theta, basis, bubble)
        means = [_poly_value(profile, *site) for site in sites]
        _require(all(-1 <= mean <= 1 for mean in means), "physical sampled means")
        coefficients = [*corners, theta]
        _require(
            [_dot(row, coefficients) for row in geometry["evaluation_matrix"]] == means,
            "complete population evaluation",
        )
        recovered = [_dot(row, means) for row in geometry["coefficient_decoder"]]
        _require(recovered == coefficients, "complete five-site coefficient recovery")
        target = normalization * _integral(_poly_multiply(profile, kernel), bounds, measure)
        corner_poly = _model_polynomial(corners, F(0), basis, bubble)
        corner_target = normalization * _integral(
            _poly_multiply(corner_poly, kernel), bounds, measure
        )
        _require(
            target == _dot(geometry["repair_weights"], means), "integrated versus compiled target"
        )
        _require(corner_target == _dot(geometry["corner_weights"], corners), "corner target")
        reports, branches = {}, {}
        for plan in plans:
            plan_means = [means[station_index[station]] for station, _ in plan["slots"]]
            report, branch_matrices = _score_plan(plan_means, target, plan, sparse[plan["cost"]])
            expected = corner_target if plan["id"] in ("corner4", "corner5") else target
            _require(report["mean"] == expected, "plan population response")
            reports[plan["id"]], branches[plan["id"]] = report, branch_matrices
        all_branches[supplied["id"]] = branches
        profiles.append(
            {
                "id": supplied["id"],
                "corners": corners,
                "theta": theta,
                "admission_bound": _admission(corners, theta),
                "sample_means": means,
                "recovered_coefficients": recovered,
                "target": target,
                "corner_target": corner_target,
                "plans": reports,
                "marginalization": _marginalization(reports, branches, reduction),
                "reallocation": _reallocation(reports, means, geometry),
                "mse_differences": {
                    "target4_minus_corner4": reports["target4"]["mse"] - reports["corner4"]["mse"],
                    "repeatcc5_minus_corner5": reports["repeatcc5"]["mse"]
                    - reports["corner5"]["mse"],
                    "repeatcc5_minus_repair5": reports["repeatcc5"]["mse"]
                    - reports["repair5"]["mse"],
                },
            }
        )
    udelta = {(1, 0): F(1), (0, 0): -sites[4][0]}
    vdelta = {(0, 1): F(1), (0, 0): -sites[4][1]}
    distance = _poly_add(_poly_multiply(udelta, udelta), _poly_multiply(vdelta, vdelta))
    amplitude = _fraction(protocol["off_model"]["amplitude"])
    off_poly = _poly_scale(_poly_multiply(bubble, distance), amplitude)
    means = [_poly_value(off_poly, *site) for site in sites]
    _require(all(mean == 0 for mean in means), "further off-model sampling collision")
    bound = _fraction(protocol["off_model"]["global_bound"])
    distance_bound = max((bounds[0] - sites[4][0]) ** 2, (bounds[1] - sites[4][0]) ** 2) + max(
        (bounds[2] - sites[4][1]) ** 2, (bounds[3] - sites[4][1]) ** 2
    )
    _require(amplitude * distance_bound / 16 <= bound <= 1, "physical off-model enclosure")
    target = normalization * _integral(_poly_multiply(off_poly, kernel), bounds, measure)
    _require(target > 0, "positive blind-mode target")
    reports, branches = {}, {}
    zero = next(row for row in profiles if row["id"] == "zero")
    for plan in plans:
        if plan["id"] in protocol["off_model"]["plans"]:
            plan_means = [means[station_index[station]] for station, _ in plan["slots"]]
            report, branch_matrices = _score_plan(plan_means, target, plan, sparse[plan["cost"]])
            _require(
                report["mean"] == 0 and report["rows"] == zero["plans"][plan["id"]]["rows"],
                "all declared off-model records remain blind",
            )
            reports[plan["id"]], branches[plan["id"]] = report, branch_matrices
    return {
        "geometry": geometry,
        "operators": operators,
        "schedule_counts": schedule_counts,
        "plans": plans,
        "reduction": reduction,
        "profiles": profiles,
        "collision": _collision(
            protocol["collision"]["profiles"], profiles, all_branches, reduction
        ),
        "off_model": {
            "id": protocol["off_model"]["id"],
            "sample_means": means,
            "global_bound": bound,
            "target": target,
            "plans": reports,
            "marginalization": _marginalization(reports, branches, reduction),
        },
    }
