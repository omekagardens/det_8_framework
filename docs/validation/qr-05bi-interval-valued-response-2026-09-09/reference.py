"""Independent QR-05BI exact interval and coupled-law reference.

Owned beta/Bernoulli and interpolation/de Casteljau helpers are carried
statically. No historical executor, primary helper or retained answer is used.
"""

from fractions import Fraction
from itertools import pairwise, product
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


def _interval(value):
    """Validate/copy one nonempty closed interval, or its empty null."""
    if value is None:
        return None
    _vector(value, 2, "two interval endpoints")
    lower, upper = [None if endpoint is None else _fraction(endpoint) for endpoint in value]
    _require(lower is None or upper is None or lower <= upper, "ordered interval")
    return [lower, upper]


def _solve_constraints(pairs):
    """Collect exact threshold extrema; no sequential clipping or sampling."""
    _require(type(pairs) is list, "affine constraint list")
    parsed = []
    lowers, uppers = [], []
    impossible = False
    for pair in pairs:
        _vector(pair, 2, "affine intercept/slope")
        intercept, slope = [_fraction(value) for value in pair]
        parsed.append([intercept, slope])
        if slope == 0:
            impossible = impossible or abs(intercept) > 1
        else:
            thresholds = [(-1 - intercept) / slope, (1 - intercept) / slope]
            lowers.append(min(thresholds))
            uppers.append(max(thresholds))
    if impossible:
        return None
    lower = max(lowers) if lowers else None
    upper = min(uppers) if uppers else None
    if lower is not None and upper is not None and lower > upper:
        return None
    for endpoint in (lower, upper):
        if endpoint is not None:
            _require(
                all(abs(intercept + slope * endpoint) <= 1 for intercept, slope in parsed),
                "extremal threshold satisfies every constraint",
            )
    return [lower, upper]


def _merge_intervals(intervals):
    """Canonical closed union; null intervals are empty, null endpoints infinite."""
    _require(type(intervals) is list, "interval list")
    copied = []
    for interval in intervals:
        parsed = _interval(interval)
        if parsed is not None:
            copied.append(parsed)
    copied.sort(
        key=lambda item: (item[0] is not None, item[0] if item[0] is not None else Fraction(0))
    )
    merged = []
    for lower, upper in copied:
        if not merged:
            merged.append([lower, upper])
            continue
        last = merged[-1]
        touching = last[1] is None or lower is None or lower <= last[1]
        if not touching:
            merged.append([lower, upper])
        elif last[1] is None or upper is None:
            last[1] = None
        else:
            last[1] = max(last[1], upper)
    return merged


def _intersect_unions(left, right):
    first = _merge_intervals(left)
    second = _merge_intervals(right)
    intersections = []
    for a, b in first:
        for c, d in second:
            lowers = [value for value in (a, c) if value is not None]
            uppers = [value for value in (b, d) if value is not None]
            lower = max(lowers) if lowers else None
            upper = min(uppers) if uppers else None
            if lower is None or upper is None or lower <= upper:
                intersections.append([lower, upper])
    return _merge_intervals(intersections)


def _project_union(union, offset, slope):
    source = _merge_intervals(union)
    offset, slope = _fraction(offset), _fraction(slope)
    if not source:
        return []
    if slope == 0:
        return [[offset, offset]]
    images = []
    for lower, upper in source:
        pair = [
            None if endpoint is None else offset + slope * endpoint for endpoint in (lower, upper)
        ]
        images.append(pair if slope > 0 else list(reversed(pair)))
    return _merge_intervals(images)


def _is_subset(left, right):
    return _intersect_unions(left, right) == _merge_intervals(left)


def _contains(union, point):
    return any(
        (lower is None or lower <= point) and (upper is None or point <= upper)
        for lower, upper in union
    )


def _finite(union):
    _require(
        all(endpoint is not None for interval in union for endpoint in interval),
        "finite data/target union",
    )
    return union


def _affine_value(pair, parameter):
    return pair[0] + pair[1] * parameter


def _affine_patch(corners, zero_net, one_net, descriptor, nodes):
    coefficients = [
        [[zero_net[i][j], one_net[i][j] - zero_net[i][j]] for j in range(3)] for i in range(3)
    ]
    slope_net = [[pair[1] for pair in row] for row in coefficients]
    (u0, u1), (v0, v1) = descriptor["bounds"]
    residual = []
    for u in nodes:
        row = []
        for v in nodes:
            physical = [u0 + (u1 - u0) * u, v0 + (v1 - v0) * v]
            original_zero = _profile_value(corners, Fraction(0), physical)
            original_slope = _profile_value(corners, Fraction(1), physical) - original_zero
            row.append(
                [
                    original_zero - _net_value(zero_net, u, v),
                    original_slope - _net_value(slope_net, u, v),
                ]
            )
        residual.append(row)
    _require(
        all(component == 0 for row in residual for pair in row for component in pair),
        "all-parameter Bernstein reconstruction",
    )
    allowed = [[_solve_constraints([pair]) for pair in row] for row in coefficients]
    return {
        "id": descriptor["id"],
        "bounds": [list(interval) for interval in descriptor["bounds"]],
        "coefficients": coefficients,
        "reconstruction_residual": residual,
        "allowed": allowed,
        "theta_interval": _solve_constraints([pair for row in coefficients for pair in row]),
    }


def _constraints(corners, certificate):
    root_descriptor, leaf_descriptors, nodes, points = _certificate_config(certificate)
    root_zero = _root_net(corners + [Fraction(0)], nodes)
    root_one = _root_net(corners + [Fraction(1)], nodes)
    zero_nets = [root_zero] + _leaf_nets(root_zero)
    one_nets = [root_one] + _leaf_nets(root_one)
    patches = [
        _affine_patch(corners, zero, one, descriptor, nodes)
        for zero, one, descriptor in zip(zero_nets, one_nets, [root_descriptor] + leaf_descriptors)
    ]
    witnesses = []
    for point in points:
        intercept = _profile_value(corners, Fraction(0), point)
        slope = _profile_value(corners, Fraction(1), point) - intercept
        pair = [intercept, slope]
        witnesses.append(
            {"position": list(point), "value": pair, "allowed": _solve_constraints([pair])}
        )
    radius = 16 * (1 - max(abs(value) for value in corners))
    _require(radius >= 0, "bounded exact corner means")
    old = [-radius, radius]
    bernstein = _solve_constraints(
        [pair for patch in patches[1:] for row in patch["coefficients"] for pair in row]
    )
    witness = _solve_constraints([item["value"] for item in witnesses])
    _require(
        bernstein is not None and _contains([bernstein], Fraction(0)),
        "zero belongs to Bernstein route",
    )
    _require(_contains([old], Fraction(0)), "zero belongs to old route")
    inner = _merge_intervals([old, bernstein])
    outer = _merge_intervals([witness])
    _require(len(inner) == 1, "alternative sufficient intervals form a connected union")
    _require(_is_subset(inner, outer), "sufficient intervals satisfy actual-point constraints")
    _require(
        _is_subset(_merge_intervals([patches[0]["theta_interval"]]), [bernstein]),
        "root success cannot be lost after subdivision",
    )
    return {
        "old_theta": old,
        "patches": patches,
        "witnesses": witnesses,
        "bernstein_theta": bernstein,
        "witness_theta": witness,
        "inner_theta": inner,
        "outer_theta": outer,
    }


def _law_family(corners):
    """One shared-mean Bernoulli family with independent bit-projector states."""
    _require(
        len(corners) == 4 and all(abs(value) <= 1 for value in corners),
        "four valid corner preparations",
    )
    bits = list(product((0, 1), repeat=5))
    density = []
    for basis in bits:
        prefix = _multiply((1 + (1 - 2 * bit) * mean) / 2 for bit, mean in zip(basis[:4], corners))
        density.append([prefix / 2, (1 - 2 * basis[4]) * prefix / 2])
    rows = []
    for outcomes in product((-1, 1), repeat=5):
        prefix = _multiply((1 + sign * mean) / 2 for sign, mean in zip(outcomes[:4], corners))
        probability = [prefix / 2, outcomes[4] * prefix / 2]
        state = []
        for basis, pair in zip(bits, density):
            indicator = _multiply(
                Fraction(int(1 - 2 * bit == outcome)) for bit, outcome in zip(basis, outcomes)
            )
            state.append([component * indicator for component in pair])
        _require(
            [sum((pair[k] for pair in state), Fraction(0)) for k in range(2)] == probability,
            "affine projector traces equal Bernoulli coefficients",
        )
        rows.append(
            {"outcomes": list(outcomes), "probability": probability, "state_diagonal": state}
        )
    _require(
        [sum((row["probability"][k] for row in rows), Fraction(0)) for k in range(2)]
        == [Fraction(1), Fraction(0)],
        "affine probability normalization",
    )
    averaged = [
        [sum((row["state_diagonal"][i][k] for row in rows), Fraction(0)) for k in range(2)]
        for i in range(32)
    ]
    _require(averaged == density, "complete averaged affine preparation")
    return {"rows": rows, "averaged_state": averaged}


def _endpoint_check(law, mean):
    probabilities = [_affine_value(row["probability"], mean) for row in law["rows"]]
    states = [[_affine_value(pair, mean) for pair in row["state_diagonal"]] for row in law["rows"]]
    averaged = [_affine_value(pair, mean) for pair in law["averaged_state"]]
    probability_sum = sum(probabilities, Fraction(0))
    averaged_trace = sum(averaged, Fraction(0))
    minimum_probability = min(probabilities)
    minimum_entry = min(value for state in states for value in state)
    maximum_residual = max(
        abs(sum(state, Fraction(0)) - probability)
        for state, probability in zip(states, probabilities)
    )
    _require(minimum_probability >= 0 and minimum_entry >= 0, "endpoint positivity")
    _require(probability_sum == averaged_trace == 1, "endpoint normalization")
    _require(maximum_residual == 0, "endpoint branch traces")
    _require(
        [sum((state[i] for state in states), Fraction(0)) for i in range(32)] == averaged,
        "endpoint state averaging",
    )
    return {
        "mean": mean,
        "probability_sum": probability_sum,
        "averaged_trace": averaged_trace,
        "minimum_probability": minimum_probability,
        "minimum_state_entry": minimum_entry,
        "maximum_trace_residual": maximum_residual,
    }


def _position_report(position, corners, response, constraints, geometry, corner_points):
    intercept = _dot(position["basis"][:4], corners)
    slope = position["basis"][4]
    _require(slope > 0, "positive interior response slope")
    data = [(mean - intercept) / slope for mean in response]
    _require(data[0] <= data[1], "ordered response inversion")
    target_offset = _dot(geometry["coefficient_integrals"][:4], corners)
    target_slope = geometry["coefficient_integrals"][4]
    projected = _finite(_project_union([data], target_offset, target_slope))
    _require(len(projected) == 1, "one data target interval")
    residuals = []
    for theta, mean in zip(data, response):
        coefficients = corners + [theta]
        reconstructed = [
            _profile_value(corners, theta, point)
            for point in corner_points + [position["position"]]
        ]
        expected = corners + [mean]
        residual = [
            actual - expected_value for actual, expected_value in zip(reconstructed, expected)
        ]
        _require(all(value == 0 for value in residual), "endpoint response reconstruction")
        _require(
            [_dot(row, expected) for row in position["coefficient_decoder"]] == coefficients,
            "endpoint inverse coefficients",
        )
        _require(
            _direct_target(corners, theta, geometry) == target_offset + target_slope * theta,
            "independent endpoint target integral",
        )
        residuals.append(residual)
    sources = {
        "old": _merge_intervals([constraints["old_theta"]]),
        "bernstein": _merge_intervals([constraints["bernstein_theta"]]),
        "inner": constraints["inner_theta"],
        "outer": constraints["outer_theta"],
    }
    theta_sets = {
        name: _finite(_intersect_unions([data], source)) for name, source in sources.items()
    }
    targets = {
        name: _finite(_project_union(union, target_offset, target_slope))
        for name, union in theta_sets.items()
    }
    _require(
        _is_subset(theta_sets["old"], theta_sets["inner"])
        and _is_subset(theta_sets["bernstein"], theta_sets["inner"])
        and _is_subset(theta_sets["inner"], theta_sets["outer"]),
        "data-intersected route inclusions",
    )
    _require(
        _merge_intervals(theta_sets["old"] + theta_sets["bernstein"]) == theta_sets["inner"],
        "alternative routes remain a union after data intersection",
    )
    classification = None
    if response[0] == response[1]:
        if theta_sets["inner"]:
            classification = "certified"
        elif not theta_sets["outer"]:
            classification = "refuted"
        else:
            classification = "unresolved"
    result = {
        "position_id": position["id"],
        "response_intercept": intercept,
        "response_slope": slope,
        "data_theta": list(data),
        "data_target": projected[0],
        "reconstruction_residual": residuals,
        "point_classification": classification,
    }
    for name in ("old", "bernstein", "inner", "outer"):
        result[name + "_theta"] = theta_sets[name]
        result[name + "_targets"] = targets[name]
    return result


def _set_summary(union):
    merged = _finite(_merge_intervals(union))
    hull = [merged[0][0], merged[-1][1]] if merged else None
    gaps = [[left[1], right[0]] for left, right in pairwise(merged)]
    probes = [(lower + upper) / 2 for lower, upper in gaps]
    _require(
        all(
            lower < probe < upper and not _contains(merged, probe)
            for (lower, upper), probe in zip(gaps, probes)
        ),
        "genuine open union gaps",
    )
    return {"intervals": merged, "hull": hull, "gaps": gaps, "gap_probes": probes}


def _menus(menus, position_reports):
    _require(type(menus) is list and type(position_reports) is list, "menu/position lists")
    by_position = {report["position_id"]: report for report in position_reports}
    _require(len(by_position) == len(position_reports), "unique position reports")
    result = []
    for menu in menus:
        _record(menu, ("id", "position_ids"), "menu fields")
        _require(type(menu["id"]) is str and menu["id"], "menu identifier")
        names = menu["position_ids"]
        _require(type(names) is list, "menu position list")
        _require(
            all(type(name) is str and name in by_position for name in names), "known menu positions"
        )
        _require(len(set(names)) == len(names), "unique menu position names")
        layers = {"old": [], "inner": [], "outer": []}
        for name in names:
            report = by_position[name]
            for layer, entries in layers.items():
                theta = _finite(_merge_intervals(report[layer + "_theta"]))
                targets = _finite(_merge_intervals(report[layer + "_targets"]))
                _require(bool(theta) == bool(targets), "theta/target emptiness agrees")
                if theta:
                    entries.append({"position_id": name, "theta": theta, "targets": targets})
            _require(
                _is_subset(report["old_theta"], report["inner_theta"])
                and _is_subset(report["inner_theta"], report["outer_theta"]),
                "menu hypothesis nesting",
            )
        summaries = {
            layer: _set_summary([interval for entry in entries for interval in entry["targets"]])
            for layer, entries in layers.items()
        }
        old_targets = summaries["old"]["intervals"]
        inner_targets = summaries["inner"]["intervals"]
        outer_targets = summaries["outer"]["intervals"]
        _require(
            _is_subset(old_targets, inner_targets) and _is_subset(inner_targets, outer_targets),
            "menu target union nesting",
        )
        if not layers["outer"]:
            existence, target_status = "infeasible", "infeasible"
        else:
            existence = "feasible" if layers["inner"] else "unresolved"
            if (
                layers["inner"]
                and len(outer_targets) == 1
                and outer_targets[0][0] == outer_targets[0][1]
            ):
                target_status = "identified"
            elif len(inner_targets) >= 2 or any(lower < upper for lower, upper in inner_targets):
                target_status = "ambiguous"
            else:
                target_status = "unresolved"
        result.append(
            {
                "id": menu["id"],
                "position_ids": list(names),
                **layers,
                "target_sets": summaries,
                "existence_status": existence,
                "target_status": target_status,
                "hypothesis_set_status": "exact"
                if layers["inner"] == layers["outer"]
                else "bounded",
                "target_set_status": "exact" if inner_targets == outer_targets else "bounded",
            }
        )
    _require(len({menu["id"] for menu in result}) == len(result), "unique menu identifiers")
    all_menus = [menu for menu in result if menu["id"] == "all"]
    if all_menus:
        for layer in ("old", "inner", "outer"):
            entries = {entry["position_id"]: entry for entry in all_menus[0][layer]}
            for menu in result:
                filtered = [entries[name] for name in menu["position_ids"] if name in entries]
                _require(filtered == menu[layer], "menu is an exact positional restriction")
    return result


def _budget_nesting(previous, current):
    _require(
        _is_subset([previous["response_interval"]], [current["response_interval"]]),
        "response budgets are nested",
    )
    _require(len(previous["positions"]) == len(current["positions"]), "matching budget positions")
    for first, second in zip(previous["positions"], current["positions"]):
        _require(first["position_id"] == second["position_id"], "budget position order")
        for key in ("data_theta", "data_target"):
            _require(_is_subset([first[key]], [second[key]]), "data inversion/projection nesting")
        for route in ("old", "bernstein", "inner", "outer"):
            for suffix in ("_theta", "_targets"):
                _require(
                    _is_subset(first[route + suffix], second[route + suffix]),
                    "route budget nesting",
                )
    _require(len(previous["menus"]) == len(current["menus"]), "matching budget menus")
    for first, second in zip(previous["menus"], current["menus"]):
        _require(first["id"] == second["id"], "budget menu order")
        for route in ("old", "inner", "outer"):
            _require(
                _is_subset(
                    first["target_sets"][route]["intervals"],
                    second["target_sets"][route]["intervals"],
                ),
                "menu target budget nesting",
            )


def _case_report(supplied, budget_inputs, geometry, positions, model, certificate, corner_points):
    _record(supplied, ("id", "population_means"), "case fields")
    _require(type(supplied["id"]) is str and supplied["id"], "case identifier")
    _vector(supplied["population_means"], 5, "five population centers")
    means = [_fraction(value) for value in supplied["population_means"]]
    _require(all(abs(value) <= 1 for value in means), "valid population centers")
    corners, center = means[:4], means[4]
    target_offset = _dot(geometry["coefficient_integrals"][:4], corners)
    target_slope = geometry["coefficient_integrals"][4]
    constraints = _constraints(corners, certificate)
    law = _law_family(corners)
    budgets = []
    previous_radius = None
    for supplied_budget in budget_inputs:
        _record(supplied_budget, ("id", "radius"), "budget fields")
        _require(type(supplied_budget["id"]) is str and supplied_budget["id"], "budget identifier")
        radius = _fraction(supplied_budget["radius"])
        _require(radius >= 0, "nonnegative supplied response radius")
        _require(previous_radius is None or previous_radius <= radius, "nested budget radii")
        previous_radius = radius
        response = [max(Fraction(-1), center - radius), min(Fraction(1), center + radius)]
        _require(response[0] <= center <= response[1], "clipped interval contains its center")
        position_reports = [
            _position_report(position, corners, response, constraints, geometry, corner_points)
            for position in positions
        ]
        budget = {
            "id": supplied_budget["id"],
            "response_interval": response,
            "endpoint_checks": [_endpoint_check(law, endpoint) for endpoint in response],
            "positions": position_reports,
            "menus": _menus(model["menus"], position_reports),
        }
        if budgets:
            _budget_nesting(budgets[-1], budget)
        budgets.append(budget)
    _require(len({budget["id"] for budget in budgets}) == len(budgets), "unique budget identifiers")
    return {
        "id": supplied["id"],
        "corners": list(corners),
        "center_mean": center,
        "target_offset": target_offset,
        "target_slope": target_slope,
        "constraints": constraints,
        "law_family": law,
        "budgets": budgets,
    }


def analyze(protocol: dict) -> dict:
    """Compile the exact coupled law and interval certificate; no import-time work."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    inherited = protocol["model"]
    model = inherited["model"]
    geometry, corner_points = _geometry(model)
    _require(geometry["coefficient_integrals"][4] > 0, "positive target bubble slope")
    _require(type(model["positions"]) is list, "supplied position list")
    positions = [_position(item, geometry) for item in model["positions"]]
    _require(len({position["id"] for position in positions}) == len(positions), "unique positions")
    _require(type(model["cases"]) is list, "supplied case list")
    _require(type(protocol["interval_budgets"]) is list, "supplied budget list")
    cases = [
        _case_report(
            item,
            protocol["interval_budgets"],
            geometry,
            positions,
            model,
            inherited["certificate"],
            corner_points,
        )
        for item in model["cases"]
    ]
    _require(len({case["id"] for case in cases}) == len(cases), "unique case identifiers")
    report = {"geometry": geometry, "positions": positions, "cases": cases}
    _native(report)
    return report
