"""Independent QR-05BH interpolation/de Casteljau admission certificates.

The owned BG Bernoulli/beta route is carried statically and recomputed.
No historical engine, primary helper or retained numerical answer is imported.
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
    _vector(protocol["corners"], 4, "four corner coordinates")
    points = []
    for point in protocol["corners"]:
        _vector(point, 2, "coordinate pair")
        points.append([_fraction(value) for value in point])
    expected = [[Fraction(int(symbol)) for symbol in name] for name in protocol["stations"][:4]]
    _require(points == expected, "supplied corner coordinates")
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
    return {"volume": volume, "sigma": sigma, "coefficient_integrals": integrals}, points


def _position(supplied, geometry):
    _record(supplied, ("id", "position"), "position fields")
    _require(type(supplied["id"]) is str and supplied["id"], "position identifier")
    _vector(supplied["position"], 2, "position coordinates")
    position = [_fraction(value) for value in supplied["position"]]
    _require(all(0 < value < 1 for value in position), "strictly interior position")
    basis = _basis(*position) + [_bubble(*position)]
    evaluation = [[Fraction(int(i == j)) for j in range(5)] for i in range(4)]
    evaluation.append(list(basis))
    decoder = [[Fraction(int(i == j)) for j in range(5)] for i in range(4)]
    decoder.append([-value / basis[4] for value in basis[:4]] + [1 / basis[4]])
    left = _matmul(decoder, evaluation)
    right = _matmul(evaluation, decoder)
    identity = [[Fraction(int(i == j)) for j in range(5)] for i in range(5)]
    _require(left == identity and right == identity, "two-sided position inverse")
    q = geometry["coefficient_integrals"]
    full_weights = [_dot(q, column) for column in zip(*decoder)]
    residual = [_dot(full_weights, column) - target for column, target in zip(zip(*evaluation), q)]
    _require(all(value == 0 for value in residual), "full target map")
    return {
        "id": supplied["id"],
        "position": position,
        "basis": basis,
        "evaluation_matrix": evaluation,
        "coefficient_decoder": decoder,
        "left_inverse": left,
        "right_inverse": right,
        "full_weights": full_weights,
        "full_residual": residual,
    }


def _law(means):
    _require(
        len(means) == 5 and all(-1 <= mean <= 1 for mean in means), "valid five local preparations"
    )
    computational_basis = list(product((0, 1), repeat=5))
    density = [
        _multiply((1 + (1 - 2 * bit) * mean) / 2 for bit, mean in zip(bits, means))
        for bits in computational_basis
    ]
    rows = []
    for outcomes in product((-1, 1), repeat=5):
        probability = _multiply((1 + sign * mean) / 2 for sign, mean in zip(outcomes, means))
        diagonal = []
        for bits, entry in zip(computational_basis, density):
            projected = entry
            for bit, outcome in zip(bits, outcomes):
                projected *= Fraction(int(1 - 2 * bit == outcome))
            diagonal.append(projected)
        _require(sum(diagonal, Fraction(0)) == probability, "projector trace/Bernoulli product")
        rows.append(
            {
                "outcomes": list(outcomes),
                "probability": probability,
                "state_diagonal": diagonal,
            }
        )
    _require(sum((row["probability"] for row in rows), Fraction(0)) == 1, "law normalization")
    averaged = [sum((row["state_diagonal"][i] for row in rows), Fraction(0)) for i in range(32)]
    _require(averaged == density, "outcome-averaged diagonal state")
    return {"rows": rows, "averaged_state": averaged}


def _candidate(means, public_law, position, geometry, corner_points):
    corners = list(means[:4])
    theta = (means[4] - _dot(position["basis"][:4], corners)) / position["basis"][4]
    coefficients = corners + [theta]
    _require(
        [_dot(row, means) for row in position["coefficient_decoder"]] == coefficients,
        "direct coefficient-recovery formula",
    )
    points = corner_points + [position["position"]]
    reconstructed = [_profile_value(corners, theta, point) for point in points]
    residual = [candidate - public for candidate, public in zip(reconstructed, means)]
    _require(all(value == 0 for value in residual), "candidate response reconstruction")
    admission = max(abs(value) for value in corners) + abs(theta) / 16
    admitted = admission <= 1
    target = _direct_target(corners, theta, geometry)
    _require(
        target == _dot(geometry["coefficient_integrals"], coefficients), "direct target integral"
    )
    # Crucial access check: compute a fresh candidate law from the reconstructed
    # polynomial values, not from the input means or a copy of the public law.
    law = _law(reconstructed)
    _require(law == public_law, "complete candidate/public local record law")
    return {
        "position_id": position["id"],
        "coefficients": coefficients,
        "admission_bound": admission,
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


def _menus(supplied_menus, candidates, position_ids):
    _require(type(supplied_menus) is list and supplied_menus, "nonempty menu list")
    by_position = {candidate["position_id"]: candidate for candidate in candidates}
    reports = []
    for menu in supplied_menus:
        _record(menu, ("id", "position_ids"), "menu fields")
        _require(type(menu["id"]) is str and menu["id"], "menu identifier")
        ids = menu["position_ids"]
        _require(type(ids) is list and ids, "nonempty menu")
        _require(
            all(type(name) is str and name in by_position for name in ids), "known menu positions"
        )
        _require(len(set(ids)) == len(ids), "distinct menu positions")
        feasible = []
        for name in ids:
            candidate = by_position[name]
            if candidate["admission_status"] == "admitted":
                feasible.append(
                    {
                        "position_id": name,
                        "coefficients": list(candidate["coefficients"]),
                        "target": candidate["target"],
                    }
                )
        targets = sorted({entry["target"] for entry in feasible})
        if len(targets) == 1:
            _require(
                all(entry["coefficients"] == feasible[0]["coefficients"] for entry in feasible),
                "fixed corner means and one target identify the coefficient vector",
            )
        if not targets:
            target_range = None
            gap = None
            status = "infeasible"
        else:
            target_range = {
                "minimum": targets[0],
                "maximum": targets[-1],
                "width": targets[-1] - targets[0],
            }
            status = "identified" if len(targets) == 1 else "ambiguous"
            gap = None if len(targets) == 1 else (targets[0] + targets[1]) / 2
            if gap is not None:
                _require(
                    targets[0] < gap < targets[1] and gap not in targets, "finite-set gap probe"
                )
        reports.append(
            {
                "id": menu["id"],
                "position_ids": list(ids),
                "feasible": feasible,
                "distinct_targets": targets,
                "target_range": target_range,
                "gap_probe": gap,
                "status": status,
            }
        )
    _require(len({menu["id"] for menu in reports}) == len(reports), "distinct menu identifiers")
    all_menus = [menu for menu in reports if menu["id"] == "all"]
    _require(
        len(all_menus) == 1 and all_menus[0]["position_ids"] == position_ids, "all-position menu"
    )
    all_report = all_menus[0]
    all_feasible = {entry["position_id"]: entry for entry in all_report["feasible"]}
    for menu in reports:
        filtered = [all_feasible[name] for name in menu["position_ids"] if name in all_feasible]
        _require(filtered == menu["feasible"], "menu is an exact restriction")
        _require(
            set(menu["distinct_targets"]) <= set(all_report["distinct_targets"]),
            "target-set restriction",
        )
    return reports


def _case(supplied, positions, geometry, corner_points, menus):
    _record(supplied, ("id", "population_means"), "public case fields")
    _require(type(supplied["id"]) is str and supplied["id"], "case identifier")
    _vector(supplied["population_means"], 5, "five population means")
    means = [_fraction(value) for value in supplied["population_means"]]
    _require(all(-1 <= value <= 1 for value in means), "local population bounds")
    law = _law(means)
    candidates = [
        _candidate(means, law, position, geometry, corner_points) for position in positions
    ]
    return {
        "id": supplied["id"],
        "population_means": means,
        "law": law,
        "candidates": candidates,
        "menus": _menus(menus, candidates, [position["id"] for position in positions]),
    }


def _witness(supplied, cases):
    _record(supplied, ("id", "case_id", "position_ids"), "witness fields")
    _require(type(supplied["id"]) is str and supplied["id"], "witness identifier")
    _vector(supplied["position_ids"], 2, "witness position pair")
    by_case = {case["id"]: case for case in cases}
    case = by_case[supplied["case_id"]]
    by_position = {candidate["position_id"]: candidate for candidate in case["candidates"]}
    first, second = [by_position[name] for name in supplied["position_ids"]]
    _require(first["position_id"] != second["position_id"], "distinct witness positions")
    _require(
        first["admission_status"] == second["admission_status"] == "admitted",
        "admitted witness hypotheses",
    )
    coefficient_difference = [b - a for a, b in zip(first["coefficients"], second["coefficients"])]
    means_difference = [
        b - a for a, b in zip(first["reconstructed_means"], second["reconstructed_means"])
    ]
    target_difference = second["target"] - first["target"]
    left_rows, right_rows = first["law"]["rows"], second["law"]["rows"]
    _require(
        [row["outcomes"] for row in left_rows] == [row["outcomes"] for row in right_rows],
        "witness outcome labels",
    )
    variation = (
        sum(
            (abs(b["probability"] - a["probability"]) for a, b in zip(left_rows, right_rows)),
            Fraction(0),
        )
        / 2
    )
    disagreements = sum(
        a["state_diagonal"] != b["state_diagonal"] for a, b in zip(left_rows, right_rows)
    )
    averaged_difference = [
        b - a for a, b in zip(first["law"]["averaged_state"], second["law"]["averaged_state"])
    ]
    _require(variation == 0 and disagreements == 0, "complete observable witness collision")
    _require(all(value == 0 for value in averaged_difference), "averaged witness states")
    if supplied["id"] == "target_ambiguity":
        _require(target_difference != 0, "unequal admitted targets")
    else:
        _require(supplied["id"] == "harmless_position_ambiguity", "declared witness kind")
        _require(target_difference == 0, "harmless target ambiguity")
    disclosures = [first["disclosure"], second["disclosure"]]
    _require(
        all(item["status"] == "identified" for item in disclosures), "exact position disclosures"
    )
    return {
        "id": supplied["id"],
        "case_id": supplied["case_id"],
        "position_ids": list(supplied["position_ids"]),
        "admission_bounds": [first["admission_bound"], second["admission_bound"]],
        "coefficients_difference": coefficient_difference,
        "means_difference": means_difference,
        "target_difference": target_difference,
        "law_total_variation": variation,
        "branch_state_disagreements": disagreements,
        "averaged_state_difference": averaged_difference,
        "disclosed_targets": [item["target"] for item in disclosures],
    }


def _domain_control(supplied, cases, positions):
    _record(supplied, ("case_id", "position_id", "rule"), "domain-control fields")
    by_case = {case["id"]: case for case in cases}
    case = by_case[supplied["case_id"]]
    by_candidate = {candidate["position_id"]: candidate for candidate in case["candidates"]}
    candidate = by_candidate[supplied["position_id"]]
    by_position = {position["id"]: position for position in positions}
    position = by_position[supplied["position_id"]]
    coefficients = candidate["coefficients"]
    constant = coefficients[0]
    theta = coefficients[4]
    _require(all(value == constant for value in coefficients[:4]), "constant-corner domain control")
    _require(theta < 0, "negative bubble control")
    _require(candidate["admission_status"] == "outside_sufficient_class", "domain-refusal control")
    minimum_position = [Fraction(1, 2), Fraction(1, 2)]
    maximum_position = [Fraction(0), Fraction(0)]
    _require(position["position"] == minimum_position, "center domain-control hypothesis")
    # x(1-x)=1/4-(x-1/2)^2 lies in [0,1/4] on the unit interval.
    # The product attains its upper bound at the center and zero at a corner.
    bubble_range = [Fraction(0), Fraction(1, 4) ** 2]
    _require(_bubble(*minimum_position) == bubble_range[1], "bubble maximum attained")
    _require(_bubble(*maximum_position) == bubble_range[0], "bubble minimum attained")
    profile_range = [constant + theta * bubble_range[1], constant + theta * bubble_range[0]]
    _require(profile_range == [Fraction(0), Fraction(1)], "globally valid excluded profile")
    _require(
        _profile_value(coefficients[:4], theta, minimum_position) == profile_range[0],
        "profile minimum attained",
    )
    _require(
        _profile_value(coefficients[:4], theta, maximum_position) == profile_range[1],
        "profile maximum attained",
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


def _analyze_bg(protocol: dict) -> dict:
    """Compute the finite-menu population certificate, without import-time work."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    geometry, corner_points = _geometry(protocol)
    _require(geometry["coefficient_integrals"][4] != 0, "target detects the bubble coefficient")
    _require(type(protocol["positions"]) is list, "position list")
    positions = [_position(supplied, geometry) for supplied in protocol["positions"]]
    _require(
        len({position["id"] for position in positions}) == len(positions), "distinct positions"
    )
    _require(type(protocol["cases"]) is list, "case list")
    cases = [
        _case(supplied, positions, geometry, corner_points, protocol["menus"])
        for supplied in protocol["cases"]
    ]
    _require(len({case["id"] for case in cases}) == len(cases), "distinct case identifiers")
    _require(type(protocol["witnesses"]) is list, "witness list")
    witnesses = [_witness(supplied, cases) for supplied in protocol["witnesses"]]
    report = {
        "geometry": geometry,
        "positions": positions,
        "cases": cases,
        "witnesses": witnesses,
        "domain_control": _domain_control(protocol["domain_control"], cases, positions),
    }
    _native(report)
    return report


def _interpolate_curve(values):
    """Recover quadratic Bernstein controls from endpoint/midpoint values."""
    first, middle, last = values
    return [first, 2 * middle - (first + last) / 2, last]


def _root_net(coefficients, nodes):
    """Tensor interpolation, first in u and then in v; no power coefficients."""
    samples = [
        [_profile_value(coefficients[:4], coefficients[4], [u, v]) for v in nodes] for u in nodes
    ]
    u_curves = [_interpolate_curve([samples[i][j] for i in range(3)]) for j in range(3)]
    return [_interpolate_curve([u_curves[j][i] for j in range(3)]) for i in range(3)]


def _halve_curve(values):
    """Two half-interval nets from the three exact de Casteljau levels."""
    first, middle, last = values
    left_middle = (first + middle) / 2
    right_middle = (middle + last) / 2
    shared = (left_middle + right_middle) / 2
    return [first, left_middle, shared], [shared, right_middle, last]


def _halve_net_u(net):
    low = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    high = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for j in range(3):
        left, right = _halve_curve([net[i][j] for i in range(3)])
        for i in range(3):
            low[i][j] = left[i]
            high[i][j] = right[i]
    return low, high


def _halve_net_v(net):
    low, high = [], []
    for row in net:
        first, second = _halve_curve(row)
        low.append(first)
        high.append(second)
    return low, high


def _leaf_nets(root_net):
    low_u, high_u = _halve_net_u(root_net)
    ll, lh = _halve_net_v(low_u)
    hl, hh = _halve_net_v(high_u)
    return [ll, lh, hl, hh]


def _bernstein_curve(point):
    return [(1 - point) ** 2, 2 * point * (1 - point), point**2]


def _net_value(net, u, v):
    return _dot(_bernstein_curve(u), [_dot(row, _bernstein_curve(v)) for row in net])


def _patch_bounds(value):
    _vector(value, 2, "two patch intervals")
    result = []
    for interval in value:
        _vector(interval, 2, "patch interval endpoints")
        pair = [_fraction(endpoint) for endpoint in interval]
        _require(pair[0] < pair[1], "positive patch interval")
        result.append(pair)
    return result


def _certificate_config(supplied):
    _require(type(supplied) is dict, "native certificate record")
    _require(supplied["degree"] == [2, 2], "degree-(2,2) certificate")
    _vector(supplied["local_nodes"], 3, "three local interpolation nodes")
    nodes = [_fraction(value) for value in supplied["local_nodes"]]
    _require(nodes == [Fraction(0), Fraction(1, 2), Fraction(1)], "fixed local nodes")
    _record(supplied["root"], ("id", "bounds"), "root patch fields")
    root = {"id": supplied["root"]["id"], "bounds": _patch_bounds(supplied["root"]["bounds"])}
    full = [[nodes[0], nodes[2]], [nodes[0], nodes[2]]]
    _require(root["id"] == "root" and root["bounds"] == full, "fixed full-square root")
    _vector(supplied["leaves"], 4, "four half-square leaves")
    leaves = []
    intervals = [[nodes[0], nodes[1]], [nodes[1], nodes[2]]]
    for supplied_leaf, (i, j), name in zip(
        supplied["leaves"], product(range(2), repeat=2), ("ll", "lh", "hl", "hh")
    ):
        _record(supplied_leaf, ("id", "bounds"), "leaf patch fields")
        bounds = _patch_bounds(supplied_leaf["bounds"])
        _require(supplied_leaf["id"] == name, "fixed leaf order")
        _require(bounds == [intervals[i], intervals[j]], "covering half-square partition")
        leaves.append({"id": name, "bounds": bounds})
    _vector(supplied["witness_points"], 9, "nine physical witness points")
    points = []
    for point in supplied["witness_points"]:
        _vector(point, 2, "physical witness coordinates")
        points.append([_fraction(value) for value in point])
    _require(points == [[u, v] for u in nodes for v in nodes], "u-major physical witness grid")
    return root, leaves, nodes, points


def _patch(coefficients, net, descriptor, nodes):
    (u0, u1), (v0, v1) = descriptor["bounds"]
    residual = []
    for u in nodes:
        row = []
        for v in nodes:
            physical = [u0 + (u1 - u0) * u, v0 + (v1 - v0) * v]
            original = _profile_value(coefficients[:4], coefficients[4], physical)
            row.append(original - _net_value(net, u, v))
        residual.append(row)
    _require(
        all(value == 0 for row in residual for value in row),
        "complete patch interpolation identity",
    )
    values = [value for row in net for value in row]
    lower, upper = min(values), max(values)
    return {
        "id": descriptor["id"],
        "bounds": [list(interval) for interval in descriptor["bounds"]],
        "coefficients": [list(row) for row in net],
        "reconstruction_residual": residual,
        "range_bound": [lower, upper],
        "bound_status": "within" if -1 <= lower <= upper <= 1 else "outside",
    }


def _classification(old_admitted, subdivision_within, violating_indices):
    """Three-way generic logic; actual witnesses cannot conflict with proof."""
    _require(
        type(old_admitted) is bool and type(subdivision_within) is bool, "classification flags"
    )
    _require(type(violating_indices) is list, "violation index list")
    _require(
        all(type(index) is int and index >= 0 for index in violating_indices),
        "native nonnegative violation indices",
    )
    _require(violating_indices == sorted(set(violating_indices)), "ordered unique violations")
    routes = []
    if old_admitted:
        routes.append("old_bound")
    if subdivision_within:
        routes.append("subdivision_bernstein")
    _require(not (routes and violating_indices), "certificate/refutation conflict")
    if routes:
        return "certified", routes
    if violating_indices:
        return "refuted", routes
    return "unresolved", routes


def _refinement_candidate(candidate, root_descriptor, leaf_descriptors, nodes, points):
    coefficients = list(candidate["coefficients"])
    root_net = _root_net(coefficients, nodes)
    root = _patch(coefficients, root_net, root_descriptor, nodes)
    leaves = [
        _patch(coefficients, net, descriptor, nodes)
        for net, descriptor in zip(_leaf_nets(root_net), leaf_descriptors)
    ]
    low, high = root["range_bound"]
    _require(
        all(
            low <= value <= high for leaf in leaves for row in leaf["coefficients"] for value in row
        ),
        "root enclosure contains every leaf coefficient",
    )
    subdivision = [
        min(leaf["range_bound"][0] for leaf in leaves),
        max(leaf["range_bound"][1] for leaf in leaves),
    ]
    within = all(leaf["bound_status"] == "within" for leaf in leaves)
    _require(
        root["bound_status"] != "within" or within, "root certificate persists under subdivision"
    )
    witnesses = []
    violations = []
    for index, point in enumerate(points):
        value = _profile_value(coefficients[:4], coefficients[4], point)
        violated = abs(value) > 1
        witnesses.append(
            {
                "position": list(point),
                "value": value,
                "status": "violation" if violated else "within",
            }
        )
        if violated:
            violations.append(index)
    old_status = candidate["admission_status"]
    _require(old_status in ("admitted", "outside_sufficient_class"), "old admission status")
    classification, routes = _classification(old_status == "admitted", within, violations)
    return {
        "position_id": candidate["position_id"],
        "coefficients": coefficients,
        "target": candidate["target"],
        "old_admission_status": old_status,
        "root": root,
        "leaves": leaves,
        "subdivision_range_bound": subdivision,
        "subdivision_status": "within" if within else "outside",
        "witnesses": witnesses,
        "violating_indices": violations,
        "certificate_routes": routes,
        "classification": classification,
    }


def _target_hull(targets):
    if not targets:
        return None
    return {"minimum": targets[0], "maximum": targets[-1], "width": targets[-1] - targets[0]}


def _refinement_menus(menus, candidates):
    """Bracket hypotheses and target images without assuming existence."""
    _require(type(menus) is list and type(candidates) is list, "menu/candidate lists")
    by_position = {candidate["position_id"]: candidate for candidate in candidates}
    _require(len(by_position) == len(candidates), "unique refined candidate positions")
    reports = []
    for menu in menus:
        _record(menu, ("id", "position_ids"), "refinement menu fields")
        _require(type(menu["id"]) is str and menu["id"], "refinement menu identifier")
        names = menu["position_ids"]
        _require(type(names) is list, "menu position list")
        _require(
            all(type(name) is str and name in by_position for name in names), "known menu positions"
        )
        _require(len(set(names)) == len(names), "unique menu positions")
        layers = {"old": [], "inner": [], "outer": []}
        for name in names:
            candidate = by_position[name]
            classification = candidate["classification"]
            old = candidate["old_admission_status"]
            _require(
                classification in ("certified", "refuted", "unresolved"),
                "refinement classification",
            )
            _require(
                old in ("admitted", "outside_sufficient_class"), "old sufficient classification"
            )
            _require(old != "admitted" or classification == "certified", "old admission retained")
            included = {
                "old": old == "admitted",
                "inner": classification == "certified",
                "outer": classification != "refuted",
            }
            for layer, include in included.items():
                if include:
                    layers[layer].append(
                        {
                            "position_id": name,
                            "coefficients": list(candidate["coefficients"]),
                            "target": candidate["target"],
                        }
                    )
        old_names = {entry["position_id"] for entry in layers["old"]}
        inner_names = {entry["position_id"] for entry in layers["inner"]}
        outer_names = {entry["position_id"] for entry in layers["outer"]}
        _require(old_names <= inner_names <= outer_names, "nested hypothesis certificates")
        targets = {
            layer: sorted({entry["target"] for entry in entries})
            for layer, entries in layers.items()
        }
        _require(
            set(targets["old"]) <= set(targets["inner"]) <= set(targets["outer"]),
            "nested finite target certificates",
        )
        if not layers["outer"]:
            existence = "infeasible"
            target_status = "infeasible"
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
                "position_ids": list(names),
                **layers,
                "old_targets": targets["old"],
                "inner_targets": targets["inner"],
                "outer_targets": targets["outer"],
                "inner_range": _target_hull(targets["inner"]),
                "outer_range": _target_hull(targets["outer"]),
                "existence_status": existence,
                "target_status": target_status,
                "hypothesis_set_status": "exact"
                if layers["inner"] == layers["outer"]
                else "bounded",
                "target_set_status": "exact" if targets["inner"] == targets["outer"] else "bounded",
            }
        )
    _require(
        len({report["id"] for report in reports}) == len(reports), "unique refinement menu names"
    )
    all_menus = [report for report in reports if report["id"] == "all"]
    if all_menus:
        _require(len(all_menus) == 1, "single all-position refinement menu")
        for layer in ("old", "inner", "outer"):
            whole = {entry["position_id"]: entry for entry in all_menus[0][layer]}
            for report in reports:
                expected = [whole[name] for name in report["position_ids"] if name in whole]
                _require(report[layer] == expected, "every layer restricts the all-menu hypotheses")
    return reports


def analyze(protocol: dict) -> dict:
    """Fresh model computation followed by the fixed global certificate budget."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    root, leaves, nodes, points = _certificate_config(protocol["certificate"])
    bg_model = _analyze_bg(protocol["model"])
    refinement = []
    for case in bg_model["cases"]:
        candidates = [
            _refinement_candidate(candidate, root, leaves, nodes, points)
            for candidate in case["candidates"]
        ]
        menus = _refinement_menus(protocol["model"]["menus"], candidates)
        old_menus = {menu["id"]: menu for menu in case["menus"]}
        for menu in menus:
            _require(
                menu["old"] == old_menus[menu["id"]]["feasible"],
                "complete old hypothesis set retained",
            )
            _require(
                menu["old_targets"] == old_menus[menu["id"]]["distinct_targets"],
                "old target image retained",
            )
        refinement.append({"id": case["id"], "candidates": candidates, "menus": menus})
    report = {"bg_model": bg_model, "refinement": refinement}
    _native(report)
    return report
