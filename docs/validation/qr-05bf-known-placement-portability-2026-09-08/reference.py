"""Independent exact QR-05BF Bernoulli/beta-integral reference.

Own earlier reference helpers are carried statically. No primary engine,
historical numerical executor, stored answer or public observer is imported.
"""

from fractions import Fraction
from itertools import product
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


def _direct_target(corners, theta, geometry):
    integral = Fraction(0)
    for mean, (i, j) in zip(corners, ((0, 0), (1, 0), (0, 1), (1, 1))):
        integral += mean * _beta(i, 2 - i) * _beta(j, 2 - j)
    integral += theta * _beta(1, 2) * _beta(1, 2)
    return geometry["volume"] ** 4 / geometry["sigma"] * integral


def _geometry(protocol):
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station order")
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    _require(protocol["retained_indices"] == [0, 1, 2, 4], "retained factor order")
    _require(protocol["omitted_index"] == 3, "omitted factor index")
    _vector(protocol["corners"], 4, "four corner coordinates")
    corners = []
    for point in protocol["corners"]:
        _vector(point, 2, "coordinate pair")
        corners.append([_fraction(value) for value in point])
    expected = [[Fraction(int(symbol)) for symbol in name] for name in protocol["stations"][:4]]
    _require(corners == expected, "supplied corner coordinates")
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
    integrals = []
    for station in protocol["stations"][:4]:
        i, j = (int(symbol) for symbol in station)
        integrals.append(factor * _beta(i, 2 - i) * _beta(j, 2 - j))
    integrals.append(factor * _beta(1, 2) * _beta(1, 2))
    _require(integrals[3] != 0, "nonzero omitted coefficient integral")
    _vector(protocol["stale_weights"], 4, "four frozen weights")
    return {
        "volume": volume,
        "sigma": sigma,
        "coefficient_integrals": integrals,
        "stale_weights": [_fraction(value) for value in protocol["stale_weights"]],
        "equality_threshold": integrals[4] / integrals[3],
        "retained_indices": list(protocol["retained_indices"]),
        "omitted_index": protocol["omitted_index"],
    }, corners


def _placement_certificate(supplied, geometry):
    _record(supplied, ("id", "position"), "placement fields")
    _require(type(supplied["id"]) is str and supplied["id"], "placement identifier")
    _vector(supplied["position"], 2, "placement position")
    position = [_fraction(value) for value in supplied["position"]]
    _require(all(0 < coordinate < 1 for coordinate in position), "strictly interior placement")
    u, v = position
    basis = _basis(u, v) + [_bubble(u, v)]
    evaluation = [[Fraction(int(i == j)) for j in range(5)] for i in range(4)]
    evaluation.append(list(basis))
    decoder = [[Fraction(int(i == j)) for j in range(5)] for i in range(4)]
    decoder.append([-value / basis[4] for value in basis[:4]] + [1 / basis[4]])
    left_inverse = _matmul(decoder, evaluation)
    right_inverse = _matmul(evaluation, decoder)
    identity = [[Fraction(int(i == j)) for j in range(5)] for i in range(5)]
    _require(left_inverse == identity and right_inverse == identity, "two-sided inverse")
    q = geometry["coefficient_integrals"]
    full_weights = [_dot(q, column) for column in zip(*decoder)]
    full_residual = [
        _dot(full_weights, column) - target for column, target in zip(zip(*evaluation), q)
    ]
    retained = [list(evaluation[index]) for index in geometry["retained_indices"]]
    unit_rows = [[Fraction(int(i == j)) for j in range(5)] for i in range(3)]
    _require(retained[:3] == unit_rows and retained[3][4] != 0, "retained matrix structure")
    rank = len(unit_rows) + int(retained[3][4] != 0)
    omitted = geometry["omitted_index"]
    direction = [row[omitted] for row in decoder]
    null_image = [_dot(row, direction) for row in retained]
    target_null = _dot(q, direction)
    locus = (1 - u) * (1 - v) - geometry["equality_threshold"]
    candidate = [full_weights[index] for index in geometry["retained_indices"]]
    stale_residual = [
        _dot(geometry["stale_weights"], column) - target
        for column, target in zip(zip(*retained), q)
    ]
    candidate_residual = [
        _dot(candidate, column) - target for column, target in zip(zip(*retained), q)
    ]
    expected_candidate_residual = [Fraction(0) for _ in q]
    expected_candidate_residual[omitted] = -full_weights[omitted]
    _require(all(value == 0 for value in full_residual), "full target row")
    _require(all(value == 0 for value in null_image), "retained null direction")
    _require(target_null == full_weights[omitted], "omission target coefficient")
    _require(target_null == q[3] - q[4] / ((1 - u) * (1 - v)), "independent equality locus")
    _require(candidate_residual == expected_candidate_residual, "truncation residual")
    _require((target_null == 0) == (locus == 0), "locus equivalence")
    _require(
        (target_null == 0) == all(value == 0 for value in candidate_residual),
        "identifiability equivalence",
    )
    scale = 1 / (2 * (1 + abs(direction[4]) / 16))
    return {
        "id": supplied["id"],
        "position": position,
        "basis": basis,
        "evaluation_matrix": evaluation,
        "coefficient_decoder": decoder,
        "left_inverse": left_inverse,
        "right_inverse": right_inverse,
        "full_weights": full_weights,
        "full_residual": full_residual,
        "retained_evaluation_matrix": retained,
        "retained_rank": rank,
        "omission_direction": direction,
        "retained_null_image": null_image,
        "target_null_image": target_null,
        "locus_residual": locus,
        "stale_residual": stale_residual,
        "candidate_weights": candidate,
        "candidate_residual": candidate_residual,
        "recovery_status": "identified" if target_null == 0 else "not_identified",
        "collision_scale": scale,
    }


def _law(means):
    _require(all(-1 <= mean <= 1 for mean in means), "positive local preparations")
    basis = list(product((0, 1), repeat=len(means)))
    density = [
        _multiply((1 + (1 - 2 * bit) * mean) / 2 for bit, mean in zip(bits, means))
        for bits in basis
    ]
    rows = []
    for outcomes in product((-1, 1), repeat=len(means)):
        probability = _multiply((1 + sign * mean) / 2 for sign, mean in zip(outcomes, means))
        diagonal = []
        for bits, entry in zip(basis, density):
            projected = entry
            for bit, outcome in zip(bits, outcomes):
                projected *= Fraction(int(1 - 2 * bit == outcome))
            diagonal.append(projected)
        _require(sum(diagonal, Fraction(0)) == probability, "instrument trace/Bernoulli product")
        rows.append(
            {
                "outcomes": list(outcomes),
                "probability": probability,
                "state_diagonal": diagonal,
            }
        )
    _require(sum((row["probability"] for row in rows), Fraction(0)) == 1, "law normalization")
    return rows


def _score(rows, means, weights, key, target):
    mean = _dot(weights, means)
    variance = sum(
        (weight**2 * (1 - value**2) for weight, value in zip(weights, means)), Fraction(0)
    )
    bias = mean - target
    mse = variance + bias**2
    _require(
        sum((row["probability"] * row[key] for row in rows), Fraction(0)) == mean, "enumerated mean"
    )
    _require(
        sum((row["probability"] * (row[key] - mean) ** 2 for row in rows), Fraction(0)) == variance,
        "enumerated variance",
    )
    _require(
        sum((row["probability"] * (row[key] - target) ** 2 for row in rows), Fraction(0)) == mse,
        "enumerated MSE",
    )
    return {"mean": mean, "bias": bias, "variance": variance, "mse": mse}


def _partial_trace(diagonal, omitted):
    _require(len(diagonal) == 32 and omitted == 3, "original omitted factor")
    reduced = [Fraction(0) for _ in range(16)]
    for full_index, entry in enumerate(diagonal):
        reduced_index = 0
        for position in range(5):
            if position != omitted:
                bit = (full_index >> (4 - position)) & 1
                reduced_index = 2 * reduced_index + bit
        reduced[reduced_index] += entry
    return reduced


def _marginalization(full, reduced, geometry):
    rows = []
    nonzero = 0
    for direct in reduced["rows"]:
        outcome = direct["outcomes"]
        indices = [
            index
            for index, row in enumerate(full["rows"])
            if [row["outcomes"][j] for j in geometry["retained_indices"]] == outcome
        ]
        _require(len(indices) == 2, "two omitted-outcome branches")
        probability = sum((full["rows"][index]["probability"] for index in indices), Fraction(0))
        summed = [
            sum((full["rows"][index]["state_diagonal"][j] for index in indices), Fraction(0))
            for j in range(32)
        ]
        traced = _partial_trace(summed, geometry["omitted_index"])
        differences = [
            full["rows"][index]["estimate"] - direct["candidate_estimate"] for index in indices
        ]
        nonzero += sum(value != 0 for value in differences)
        _require(traced == direct["state_diagonal"], "full/reduced state marginalization")
        _require(probability == direct["probability"], "full/reduced record marginalization")
        _require(sum(traced, Fraction(0)) == probability, "partial-trace probability")
        rows.append(
            {
                "outcomes": list(outcome),
                "full_indices": indices,
                "probability": probability,
                "summed_full_state": summed,
                "reduced_state": traced,
                "full_minus_candidate": differences,
            }
        )
    return {"rows": rows, "pathwise_nonzero_count": nonzero}


def _profile_report(identifier, coefficients, geometry, placement, corner_points):
    _require(type(identifier) is str and identifier, "profile identifier")
    _require(len(coefficients) == 5, "coefficient count")
    admission = max(abs(value) for value in coefficients[:4]) + abs(coefficients[4]) / 16
    _require(admission <= 1, "outside sufficient profile domain")
    points = corner_points + [placement["position"]]
    means = [_profile_value(coefficients[:4], coefficients[4], point) for point in points]
    _require(
        [_dot(row, coefficients) for row in placement["evaluation_matrix"]] == means,
        "basis evaluation",
    )
    recovered = [_dot(row, means) for row in placement["coefficient_decoder"]]
    _require(recovered == coefficients, "full coefficient recovery")
    target = _direct_target(coefficients[:4], coefficients[4], geometry)
    _require(
        target == _dot(geometry["coefficient_integrals"], coefficients), "direct target integral"
    )
    full_rows = _law(means)
    for row in full_rows:
        row["estimate"] = _dot(placement["full_weights"], row["outcomes"])
    full_score = _score(full_rows, means, placement["full_weights"], "estimate", target)
    _require(full_score["bias"] == 0, "full-access target restoration")
    full = {"rows": full_rows, **full_score}
    retained_means = [means[index] for index in geometry["retained_indices"]]
    reduced_rows = _law(retained_means)
    for row in reduced_rows:
        row["stale_estimate"] = _dot(geometry["stale_weights"], row["outcomes"])
        row["candidate_estimate"] = _dot(placement["candidate_weights"], row["outcomes"])
    reduced = {
        "rows": reduced_rows,
        "stale": _score(
            reduced_rows, retained_means, geometry["stale_weights"], "stale_estimate", target
        ),
        "candidate": _score(
            reduced_rows,
            retained_means,
            placement["candidate_weights"],
            "candidate_estimate",
            target,
        ),
    }
    _require(
        reduced["stale"]["bias"] == _dot(placement["stale_residual"], coefficients),
        "stale residual bias",
    )
    _require(
        reduced["candidate"]["bias"] == _dot(placement["candidate_residual"], coefficients),
        "candidate residual bias",
    )
    return {
        "id": identifier,
        "coefficients": list(coefficients),
        "admission_bound": admission,
        "sample_means": means,
        "recovered_coefficients": recovered,
        "target": target,
        "reduced": reduced,
        "full": full,
        "marginalization": _marginalization(full, reduced, geometry),
    }


def _collision(profiles, names, geometry, placement):
    by_name = {profile["id"]: profile for profile in profiles}
    first, second = [by_name[name] for name in names]
    difference = [b - a for a, b in zip(first["coefficients"], second["coefficients"])]
    means_difference = [b - a for a, b in zip(first["sample_means"], second["sample_means"])]
    target_difference = second["target"] - first["target"]
    predicted = 2 * placement["collision_scale"] * placement["target_null_image"]
    omitted_states = []
    averaged_states = []
    for profile in (first, second):
        mean = profile["sample_means"][geometry["omitted_index"]]
        omitted_states.append([(1 + mean) / 2, (1 - mean) / 2])
        full_rows = profile["full"]["rows"]
        averaged_states.append(
            [
                sum((row["state_diagonal"][index] for row in full_rows), Fraction(0))
                for index in range(32)
            ]
        )
        _require(profile["admission_bound"] == Fraction(1, 2), "prespecified collision scaling")
        _require(
            all(profile["sample_means"][index] == 0 for index in geometry["retained_indices"]),
            "null retained responses",
        )
    variations = {}
    for key in ("full", "reduced"):
        left, right = first[key]["rows"], second[key]["rows"]
        _require(
            [row["outcomes"] for row in left] == [row["outcomes"] for row in right],
            "collision outcome labels",
        )
        variations[key] = (
            sum(
                (abs(b["probability"] - a["probability"]) for a, b in zip(left, right)), Fraction(0)
            )
            / 2
        )
    _require(
        [row["state_diagonal"] for row in first["reduced"]["rows"]]
        == [row["state_diagonal"] for row in second["reduced"]["rows"]],
        "complete retained quantum branch collision",
    )
    _require(target_difference == predicted, "signed target collision")
    _require(
        (target_difference == 0) == (placement["recovery_status"] == "identified"),
        "collision/access distinction",
    )
    _require(variations["reduced"] == 0 and variations["full"] > 0, "full/retained collision laws")
    _require(omitted_states[0] != omitted_states[1], "different omitted states")
    return {
        "profiles": list(names),
        "coefficients_difference": difference,
        "full_means_difference": means_difference,
        "target_difference": target_difference,
        "predicted_target_difference": predicted,
        "omitted_states": omitted_states,
        "full_averaged_states": averaged_states,
        "full_law_total_variation": variations["full"],
        "retained_law_total_variation": variations["reduced"],
    }


def analyze(protocol: dict) -> dict:
    """Return the full exact mathematical certificate without import-time work."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    geometry, corner_points = _geometry(protocol)
    _require(type(protocol["profiles"]) is list, "base-profile list")
    base_profiles = []
    for supplied in protocol["profiles"]:
        _record(supplied, ("id", "corners", "theta"), "base-profile fields")
        _require(type(supplied["id"]) is str and supplied["id"], "base-profile identifier")
        _vector(supplied["corners"], 4, "base-profile corners")
        coefficients = [_fraction(value) for value in supplied["corners"]]
        coefficients.append(_fraction(supplied["theta"]))
        base_profiles.append((supplied["id"], coefficients))
    collision = protocol["collision"]
    _record(collision, ("ids", "rule"), "collision fields")
    _vector(collision["ids"], 2, "collision names")
    _require(all(type(name) is str and name for name in collision["ids"]), "collision identifiers")
    all_names = [identifier for identifier, _ in base_profiles] + list(collision["ids"])
    _require(len(set(all_names)) == len(all_names), "distinct profile identifiers")
    _require(type(protocol["placements"]) is list, "placement list")
    placements = []
    for supplied in protocol["placements"]:
        placement = _placement_certificate(supplied, geometry)
        scale = placement["collision_scale"]
        direction = placement["omission_direction"]
        cases = list(base_profiles) + [
            (collision["ids"][0], [-scale * value for value in direction]),
            (collision["ids"][1], [scale * value for value in direction]),
        ]
        profiles = [
            _profile_report(identifier, coefficients, geometry, placement, corner_points)
            for identifier, coefficients in cases
        ]
        placement["profiles"] = profiles
        placement["collision"] = _collision(profiles, collision["ids"], geometry, placement)
        placements.append(placement)
    _require(
        len({placement["id"] for placement in placements}) == len(placements), "distinct placements"
    )
    report = {"geometry": geometry, "placements": placements}
    _native(report)
    return report
