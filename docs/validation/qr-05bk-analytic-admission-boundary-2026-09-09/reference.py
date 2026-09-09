"""Independent QR-05BK stationary-resultant and Descartes certificate.

Owned BJ code is carried statically and recomputed. New algebra uses only
exact standard-library rationals; no historical engine or answer is imported.
"""

from fractions import Fraction
from functools import cmp_to_key
from itertools import pairwise, product
from math import comb, factorial, gcd, lcm


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


def _analyze_bi(protocol: dict) -> dict:
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


def _refinement_config(supplied):
    """Validate the complete, fixed Cartesian quarter partition and parent map."""
    _require(type(supplied) is dict, "native refinement descriptor")
    _require(supplied["degree"] == [2, 2], "unchanged degree-(2,2)")
    _vector(supplied["nodes"], 3, "three local reconstruction nodes")
    nodes = [_fraction(value) for value in supplied["nodes"]]
    _require(nodes == [Fraction(0), Fraction(1, 2), Fraction(1)], "fixed local nodes")
    _vector(supplied["leaves"], 16, "sixteen quarter leaves")
    names = ("ll", "lh", "hl", "hh")
    descriptors = []
    for leaf, (i, j) in zip(supplied["leaves"], product(range(4), repeat=2)):
        _record(leaf, ("id", "parent", "bounds"), "quarter leaf fields")
        _require(leaf["id"] == "q" + str(i) + str(j), "u-major quarter identifiers")
        parent = names[2 * (i // 2) + j // 2]
        _require(leaf["parent"] == parent, "quarter parent identity")
        bounds = _patch_bounds(leaf["bounds"])
        expected = [
            [Fraction(i, 4), Fraction(i + 1, 4)],
            [Fraction(j, 4), Fraction(j + 1, 4)],
        ]
        _require(bounds == expected, "complete covering quarter-grid bounds")
        descriptors.append({"id": leaf["id"], "parent": parent, "bounds": bounds})
    _vector(supplied["witness_nodes"], 5, "five physical witness coordinates")
    witness_nodes = [_fraction(value) for value in supplied["witness_nodes"]]
    _require(witness_nodes == [Fraction(i, 4) for i in range(5)], "fixed quarter witness grid")
    return descriptors, nodes, [[u, v] for u in witness_nodes for v in witness_nodes]


def _quarter_constraints(corners, baseline, config):
    descriptors, nodes, points = config
    parents = {patch["id"]: patch for patch in baseline["patches"]}
    _require(
        set(parents) == {"root", "ll", "lh", "hl", "hh"}, "complete inherited BI patch inventory"
    )
    child_nets = {}
    for name in ("ll", "lh", "hl", "hh"):
        parent = parents[name]
        zero = [[pair[0] for pair in row] for row in parent["coefficients"]]
        one = [[sum(pair, Fraction(0)) for pair in row] for row in parent["coefficients"]]
        child_nets[name] = (_leaf_nets(zero), _leaf_nets(one))
    patches = []
    for descriptor, (i, j) in zip(descriptors, product(range(4), repeat=2)):
        parent = parents[descriptor["parent"]]
        child_index = 2 * (i % 2) + (j % 2)
        local_indices = (i % 2, j % 2)
        expected_bounds = []
        for interval, local_index in zip(parent["bounds"], local_indices):
            midpoint = (interval[0] + interval[1]) / 2
            expected_bounds.append(
                [interval[0], midpoint] if local_index == 0 else [midpoint, interval[1]]
            )
        _require(
            descriptor["bounds"] == expected_bounds,
            "local half subdivision agrees with global child bounds",
        )
        zeros, ones = child_nets[descriptor["parent"]]
        patch = _affine_patch(corners, zeros[child_index], ones[child_index], descriptor, nodes)
        _require(
            _is_subset(
                _merge_intervals([parent["theta_interval"]]),
                _merge_intervals([patch["theta_interval"]]),
            ),
            "every child preserves its parent coefficient certificate",
        )
        patches.append(patch)
    witnesses = []
    for point in points:
        intercept = _profile_value(corners, Fraction(0), point)
        slope = _profile_value(corners, Fraction(1), point) - intercept
        pair = [intercept, slope]
        witnesses.append(
            {"position": list(point), "value": pair, "allowed": _solve_constraints([pair])}
        )
    by_point = {tuple(witness["position"]): witness for witness in witnesses}
    for old in baseline["witnesses"]:
        _require(
            by_point[tuple(old["position"])] == old, "every inherited actual witness is unchanged"
        )
    radius = 16 * (1 - max(abs(value) for value in corners))
    _require(radius >= 0, "valid fixed corners")
    old_theta = [-radius, radius]
    _require(old_theta == baseline["old_theta"], "old sufficient route unchanged")
    bernstein = _solve_constraints(
        [pair for patch in patches for row in patch["coefficients"] for pair in row]
    )
    witness = _solve_constraints([item["value"] for item in witnesses])
    _require(
        bernstein is not None and _contains([bernstein], Fraction(0)),
        "zero in refined Bernstein interval",
    )
    _require(_contains([old_theta], Fraction(0)), "zero in old sufficient interval")
    inner = _merge_intervals([old_theta, bernstein])
    outer = _merge_intervals([witness])
    _require(len(inner) == 1, "connected alternative sufficient routes")
    _require(
        _is_subset(_merge_intervals([baseline["bernstein_theta"]]), [bernstein]),
        "half-square Bernstein interval is included in quarter-square interval",
    )
    _require(
        _is_subset(baseline["inner_theta"], inner)
        and _is_subset(inner, outer)
        and _is_subset(outer, baseline["outer_theta"]),
        "global inner/outer refinement sandwich",
    )
    if baseline["inner_theta"] == baseline["outer_theta"]:
        _require(inner == outer == baseline["inner_theta"], "exact global set persists")
    return {
        "old_theta": old_theta,
        "patches": patches,
        "witnesses": witnesses,
        "bernstein_theta": bernstein,
        "witness_theta": witness,
        "inner_theta": inner,
        "outer_theta": outer,
    }


def _position_refinement(previous, current):
    for field in (
        "position_id",
        "response_intercept",
        "response_slope",
        "data_theta",
        "data_target",
        "reconstruction_residual",
        "old_theta",
        "old_targets",
    ):
        _require(previous[field] == current[field], "unchanged position data and old route")
    for suffix in ("_theta", "_targets"):
        _require(
            _is_subset(previous["bernstein" + suffix], current["bernstein" + suffix]),
            "position Bernstein route expands",
        )
        old_inner, old_outer = previous["inner" + suffix], previous["outer" + suffix]
        inner, outer = current["inner" + suffix], current["outer" + suffix]
        _require(
            _is_subset(old_inner, inner)
            and _is_subset(inner, outer)
            and _is_subset(outer, old_outer),
            "position hypothesis/target refinement sandwich",
        )
        if old_inner == old_outer:
            _require(inner == outer == old_inner, "exact position set persists")
    old_classification = previous["point_classification"]
    if old_classification in ("certified", "refuted"):
        _require(
            current["point_classification"] == old_classification, "decided point remains decided"
        )
    elif old_classification is None:
        _require(current["point_classification"] is None, "nonpoint classification stays undefined")


def _hypotheses_subset(left, right):
    right_by_position = {entry["position_id"]: entry for entry in right}
    return all(
        entry["position_id"] in right_by_position
        and _is_subset(entry["theta"], right_by_position[entry["position_id"]]["theta"])
        for entry in left
    )


def _menu_refinement(previous, current):
    for field in ("id", "position_ids", "old"):
        _require(previous[field] == current[field], "unchanged refinement menu and old route")
    _require(
        previous["target_sets"]["old"] == current["target_sets"]["old"],
        "unchanged old target summary",
    )
    _require(
        _hypotheses_subset(previous["inner"], current["inner"])
        and _hypotheses_subset(current["inner"], current["outer"])
        and _hypotheses_subset(current["outer"], previous["outer"]),
        "menu position/parameter refinement sandwich",
    )
    old_inner = previous["target_sets"]["inner"]["intervals"]
    old_outer = previous["target_sets"]["outer"]["intervals"]
    inner = current["target_sets"]["inner"]["intervals"]
    outer = current["target_sets"]["outer"]["intervals"]
    _require(
        _is_subset(old_inner, inner) and _is_subset(inner, outer) and _is_subset(outer, old_outer),
        "menu merged-target refinement sandwich",
    )
    if previous["hypothesis_set_status"] == "exact":
        _require(
            current["inner"] == current["outer"] == previous["inner"]
            and current["hypothesis_set_status"] == "exact",
            "exact menu hypothesis set persists",
        )
    if previous["target_set_status"] == "exact":
        _require(
            inner == outer == old_inner and current["target_set_status"] == "exact",
            "exact merged-target set persists",
        )
    if previous["target_status"] in ("ambiguous", "identified", "infeasible"):
        _require(
            current["target_status"] == previous["target_status"],
            "established target status persists",
        )
    if previous["existence_status"] in ("feasible", "infeasible"):
        _require(
            current["existence_status"] == previous["existence_status"],
            "established existence status persists",
        )


def _refinement_case(case, config, positions, geometry, model, corner_points):
    corners = list(case["corners"])
    constraints = _quarter_constraints(corners, case["constraints"], config)
    budgets = []
    for baseline in case["budgets"]:
        response = list(baseline["response_interval"])
        reports = [
            _position_report(position, corners, response, constraints, geometry, corner_points)
            for position in positions
        ]
        _require(len(reports) == len(baseline["positions"]), "matching position census")
        for old, new in zip(baseline["positions"], reports):
            _position_refinement(old, new)
        menus = _menus(model["menus"], reports)
        _require(len(menus) == len(baseline["menus"]), "matching menu census")
        for old, new in zip(baseline["menus"], menus):
            _menu_refinement(old, new)
        budget = {
            "id": baseline["id"],
            "response_interval": response,
            "positions": reports,
            "menus": menus,
        }
        if budgets:
            _budget_nesting(budgets[-1], budget)
        budgets.append(budget)
    return {"id": case["id"], "constraints": constraints, "budgets": budgets}


def _analyze_bj(protocol: dict) -> dict:
    """Recompute BI, then apply one prospectively fixed refinement budget."""
    _native(protocol)
    _require(type(protocol) is dict, "native protocol dictionary")
    config = _refinement_config(protocol["refinement"])
    bi_model = _analyze_bi(protocol["model"])
    model = protocol["model"]["model"]["model"]
    corner_points = [[_fraction(value) for value in point] for point in model["corners"]]
    refinement = [
        _refinement_case(
            case, config, bi_model["positions"], bi_model["geometry"], model, corner_points
        )
        for case in bi_model["cases"]
    ]
    report = {"bi_model": bi_model, "refinement": refinement}
    _native(report)
    return report


def _p_trim(poly):
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result or [Fraction(0)]


def _p_add(left, right):
    result = [Fraction(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        result[i] += value
    for i, value in enumerate(right):
        result[i] += value
    return _p_trim(result)


def _p_scale(poly, scalar):
    return _p_trim([value * scalar for value in poly])


def _p_sub(left, right):
    return _p_add(left, _p_scale(right, Fraction(-1)))


def _p_mul(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return _p_trim(result)


def _p_derivative(poly):
    return _p_trim([i * poly[i] for i in range(1, len(poly))])


def _p_at(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def _p_divmod(numerator, denominator):
    numerator, denominator = _p_trim(numerator), _p_trim(denominator)
    _require(denominator != [Fraction(0)], "nonzero polynomial divisor")
    quotient = [Fraction(0)] * max(1, len(numerator) - len(denominator) + 1)
    remainder = list(numerator)
    while remainder != [Fraction(0)] and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        scale = remainder[-1] / denominator[-1]
        quotient[shift] += scale
        for index, value in enumerate(denominator):
            remainder[index + shift] -= scale * value
        remainder = _p_trim(remainder)
    return _p_trim(quotient), remainder


def _p_exact_div(numerator, denominator):
    quotient, remainder = _p_divmod(numerator, denominator)
    _require(remainder == [Fraction(0)], "exact polynomial division")
    return quotient


def _p_gcd(left, right):
    left, right = _p_trim(left), _p_trim(right)
    while right != [Fraction(0)]:
        _, remainder = _p_divmod(left, right)
        left, right = right, remainder
    if left == [Fraction(0)]:
        return left
    return _p_scale(left, 1 / left[-1])


def _native_poly(poly):
    _require(type(poly) is list and bool(poly), "nonempty native polynomial list")
    _require(
        all(type(value) is Fraction for value in poly), "native Fraction polynomial coefficients"
    )
    _require(len(poly) <= 13, "polynomial degree budget")
    return _p_trim(poly)


def _primitive(poly):
    _require(poly != [Fraction(0)], "nonzero raw eliminant")
    _require(
        len(_p_gcd(poly, _p_derivative(poly))) == 1,
        "fixed eliminant must already be squarefree",
    )
    denominator = 1
    for coefficient in poly:
        denominator = lcm(denominator, coefficient.denominator)
    integers = [int(coefficient * denominator) for coefficient in poly]
    content = 0
    for coefficient in integers:
        content = gcd(content, abs(coefficient))
    direction = 1 if integers[-1] > 0 else -1
    primitive = [Fraction(direction * coefficient, content) for coefficient in integers]
    scalar = Fraction(direction * content, denominator)
    _require(_p_scale(primitive, scalar) == poly, "raw eliminant normalization relationship")
    return primitive, scalar


def _bernstein_variations(poly, left, right):
    """Descartes bound on the open interval from its Bernstein coefficient signs."""
    degree = len(poly) - 1
    width = right - left
    local = [
        width**j
        * sum(
            (poly[k] * comb(k, j) * left ** (k - j) for k in range(j, degree + 1)),
            Fraction(0),
        )
        for j in range(degree + 1)
    ]
    controls = [
        sum(
            (local[j] * Fraction(comb(i, j), comb(degree, j)) for j in range(i + 1)),
            Fraction(0),
        )
        for i in range(degree + 1)
    ]
    signs = [1 if value > 0 else -1 for value in controls if value != 0]
    return sum(first != second for first, second in pairwise(signs))


def _isolate_unit_roots(poly, depth, max_depth, max_nodes):
    """Canonical dyadic output; independent internal Descartes proof refinement."""
    poly = _native_poly(poly)
    _require(poly != [Fraction(0)], "zero polynomial has no finite root census")
    _require(
        type(depth) is int and type(max_depth) is int and type(max_nodes) is int,
        "native isolation budgets",
    )
    _require(0 <= depth <= max_depth <= 64, "isolation depth bounds")
    _require(1 <= max_nodes <= 4096, "isolation node bounds")
    if len(poly) == 1:
        return []
    _require(len(_p_gcd(poly, _p_derivative(poly))) == 1, "repeated polynomial roots")
    visited = set()
    counts = {}
    values = {}

    def value(point):
        if point not in values:
            values[point] = _p_at(poly, point)
        return values[point]

    def visit(left, right, level):
        _require(level <= max_depth, "root isolation depth exhausted")
        key = (left, right)
        if key not in visited:
            _require(len(visited) < max_nodes, "root isolation node budget exhausted")
            visited.add(key)
        return key

    def count(left, right, level):
        key = visit(left, right, level)
        if key in counts:
            return counts[key]
        variation = _bernstein_variations(poly, left, right)
        if variation <= 1:
            result = variation
        else:
            _require(level < max_depth, "Descartes count unresolved at depth cap")
            middle = (left + right) / 2
            result = (
                count(left, middle, level + 1)
                + int(value(middle) == 0)
                + count(middle, right, level + 1)
            )
        counts[key] = result
        return result

    roots = []

    def walk(left, right, level):
        census = count(left, right, level)
        if census == 0:
            return
        middle = (left + right) / 2
        if value(middle) == 0:
            if census == 1:
                roots.append([middle, middle])
                return
            _require(level < max_depth, "multiple roots at isolation depth cap")
            walk(left, middle, level + 1)
            roots.append([middle, middle])
            walk(middle, right, level + 1)
            return
        if census == 1 and level >= depth and value(left) != 0 and value(right) != 0:
            roots.append([left, right])
            return
        _require(level < max_depth, "canonical root cell unresolved")
        walk(left, middle, level + 1)
        walk(middle, right, level + 1)

    # Endpoint values are checked explicitly. Descartes sign variation excludes
    # endpoint roots because zero end controls contribute no sign changes.
    value(Fraction(0))
    value(Fraction(1))
    walk(Fraction(0), Fraction(1), 0)
    _require(len(roots) == count(Fraction(0), Fraction(1), 0), "complete unit root census")
    _require(
        all(
            0 <= lower <= upper <= 1 and (lower != upper or 0 < lower < 1) for lower, upper in roots
        ),
        "unit root cells and interior rational roots",
    )
    return roots


def _rational_interval(interval):
    _require(type(interval) is list and len(interval) == 2, "two rational interval endpoints")
    _require(
        all(type(value) is Fraction for value in interval), "finite Fraction interval endpoints"
    )
    _require(interval[0] <= interval[1], "ordered rational interval")
    return list(interval)


def _i_add(left, right):
    return [left[0] + right[0], left[1] + right[1]]


def _i_mul(left, right):
    products = [a * b for a in left for b in right]
    return [min(products), max(products)]


def _p_interval(poly, interval):
    result = [Fraction(0), Fraction(0)]
    for coefficient in reversed(poly):
        result = _i_add(_i_mul(result, interval), [coefficient, coefficient])
    return result


def _image_interval(numerator, denominator, interval):
    num = _p_interval(numerator, interval)
    den = _p_interval(denominator, interval)
    _require(den[0] > 0, "strictly positive image denominator")
    return _i_mul(num, [1 / den[1], 1 / den[0]]), den


def _rf(numerator, denominator=None):
    numerator = _p_trim(numerator)
    denominator = [Fraction(1)] if denominator is None else _p_trim(denominator)
    _require(denominator != [Fraction(0)], "nonzero rational-function denominator")
    if numerator == [Fraction(0)]:
        return [Fraction(0)], [Fraction(1)]
    common = _p_gcd(numerator, denominator)
    numerator = _p_exact_div(numerator, common)
    denominator = _p_exact_div(denominator, common)
    scale = 1 / denominator[-1]
    return _p_scale(numerator, scale), _p_scale(denominator, scale)


def _rf_add(left, right):
    return _rf(
        _p_add(_p_mul(left[0], right[1]), _p_mul(right[0], left[1])),
        _p_mul(left[1], right[1]),
    )


def _rf_scale(value, scalar):
    return _rf(_p_scale(value[0], scalar), value[1])


def _rf_sub(left, right):
    return _rf_add(left, _rf_scale(right, Fraction(-1)))


def _rf_mul(left, right):
    first = _p_gcd(left[0], right[1])
    second = _p_gcd(right[0], left[1])
    return _rf(
        _p_mul(_p_exact_div(left[0], first), _p_exact_div(right[0], second)),
        _p_mul(_p_exact_div(left[1], second), _p_exact_div(right[1], first)),
    )


def _rf_div(left, right):
    _require(right[0] != [Fraction(0)], "nonzero rational-function divisor")
    return _rf_mul(left, _rf(right[1], right[0]))


def _rf_remainder(value, defining):
    _require(
        len(_p_gcd(value[1], defining)) == 1,
        "rational identity denominator does not vanish at defining roots",
    )
    return _p_divmod(value[0], defining)[1]


def _boundary_certificate(boundary, case):
    _require(boundary["case_id"] == case["id"] == "asymmetric", "selected analytic corner case")
    corners = case["corners"]
    expected_corners = [Fraction(1, 2), Fraction(-1, 3), Fraction(2, 3), Fraction(-1, 2)]
    _require(corners == expected_corners, "fixed analytic corners")
    parsed = {}
    for name in ("A", "C", "D", "delta"):
        _require(type(boundary[name]) is list, "boundary polynomial list")
        parsed[name] = _native_poly([_fraction(value) for value in boundary[name]])
    a, c, d, delta = (parsed[name] for name in ("A", "C", "D", "delta"))
    expected_a = [6 * (1 - corners[0]), -6 * (corners[2] - corners[0])]
    expected_c = [
        -6 * (corners[1] - corners[0]),
        -6 * (corners[0] - corners[1] - corners[2] + corners[3]),
    ]
    _require(
        a == expected_a and c == expected_c, "stationarity coefficients derive from the profile"
    )
    _require(d == [Fraction(0), Fraction(1), Fraction(-1)], "positive open-square product")
    _require(delta == _p_scale(_p_derivative(d), Fraction(-1)), "delta is minus product derivative")
    _require(_p_add(_p_scale(a, Fraction(2)), c) == [Fraction(11)], "constant numerator identity")
    _require(
        _fraction(boundary["target_offset"]) == case["target_offset"]
        and _fraction(boundary["target_slope"]) == case["target_slope"],
        "target compiled from geometry",
    )
    p = _p_sub(_p_mul(_p_derivative(a), d), _p_mul(a, _p_derivative(d)))
    q = _p_sub(_p_mul(_p_derivative(c), d), _p_mul(c, _p_derivative(d)))
    raw = _p_sub(
        _p_sub(_p_mul(c, _p_mul(p, p)), _p_scale(_p_mul(a, _p_mul(p, q)), Fraction(2))),
        _p_mul(a, _p_mul(q, q)),
    )
    s = _p_mul(a, _p_add(a, c))
    k = _p_sub(_p_mul(c, d), _p_scale(_p_mul(s, delta), Fraction(2)))
    squared = _p_sub(_p_mul(k, k), _p_scale(_p_mul(_p_mul(delta, delta), s), Fraction(121)))
    _require(
        _p_add(_p_scale(p, Fraction(2)), q) == _p_scale(delta, Fraction(11)),
        "linear stationarity identity",
    )
    _require(
        k == _p_sub(_p_scale(p, Fraction(-11)), _p_mul(a, q)),
        "independent radical numerator identity",
    )
    _require(squared == _p_mul(c, raw), "independent resultant equals radical eliminant quotient")
    defining, normalization = _primitive(raw)
    config = boundary["isolation"]
    _record(config, ("depth", "max_depth", "max_nodes", "max_degree"), "isolation configuration")
    _require(type(config["max_degree"]) is int and config["max_degree"] == 12, "fixed degree cap")
    roots = _isolate_unit_roots(defining, config["depth"], config["max_depth"], config["max_nodes"])
    # Do not delete a possible delta-zero root. The midpoint rule must retain it.
    half = Fraction(1, 2)
    if _p_at(defining, half) == 0:
        _require([half, half] in roots, "explicit delta-zero root")
    root_records = []
    admitted = []
    for interval in roots:
        if interval[1] <= half:
            classification = "rejected_nonpositive_delta"
        else:
            _require(interval[0] > half, "canonical cell must separate delta sign")
            enclosure = _p_interval(k, interval)
            if enclosure[1] < 0:
                classification = "rejected_wrong_radical_sign"
            else:
                _require(enclosure[0] > 0, "radical sign unresolved on canonical root cell")
                classification = "admissible"
                admitted.append(interval)
        root_records.append({"interval": list(interval), "classification": classification})
    _require(len(admitted) == 1, "exactly one unsquared admissible stationary root")
    alpha = list(admitted[0])
    _require(0 < alpha[0] <= alpha[1] < 1, "strictly interior contact coordinate")
    k_interval = _p_interval(k, alpha)
    _require(_p_interval(s, alpha)[0] > 0, "positive radical square at contact")
    u_num = _p_scale(_p_mul(delta, a), Fraction(11))
    u_den = _p_add(u_num, k)
    beta_num = _p_add(_p_scale(delta, Fraction(121)), _p_scale(k, Fraction(2)))
    beta_den = _p_scale(_p_mul(delta, d), Fraction(66))
    u_interval, u_den_interval = _image_interval(u_num, u_den, alpha)
    beta_interval, beta_den_interval = _image_interval(beta_num, beta_den, alpha)
    _require(0 < u_interval[0] <= u_interval[1] < 1, "strictly interior u image")
    _require(beta_interval[0] > 0, "positive upper boundary")
    q_interval = _p_interval(q, alpha)
    _require(
        q_interval[1] < 0 or q_interval[0] > 0, "nonzero independent linear-equation denominator"
    )
    u = _rf(u_num, u_den)
    beta = _rf(beta_num, beta_den)
    independent_u = _rf(_p_scale(p, Fraction(-1)), q)
    _require(
        _rf_remainder(_rf_sub(u, independent_u), defining) == [Fraction(0)],
        "independent stationary u image",
    )
    one = _rf([Fraction(1)])
    v = _rf([Fraction(0), Fraction(1)])
    one_minus_u = _rf_sub(one, u)
    one_minus_v = _rf_sub(one, v)
    independent_beta = _rf_div(
        _rf_add(_rf(a), _rf_mul(_rf(c), independent_u)),
        _rf_scale(
            _rf_mul(_rf_mul(independent_u, _rf_sub(one, independent_u)), _rf(d)), Fraction(6)
        ),
    )
    _require(
        _rf_remainder(_rf_sub(beta, independent_beta), defining) == [Fraction(0)],
        "independent h-value image",
    )
    c0, cu, cv, cuv = (
        corners[0],
        corners[1] - corners[0],
        corners[2] - corners[0],
        corners[0] - corners[1] - corners[2] + corners[3],
    )
    r = _rf_add(
        _rf_add(_rf([c0]), _rf_scale(u, cu)),
        _rf_add(_rf_scale(v, cv), _rf_scale(_rf_mul(u, v), cuv)),
    )
    bubble = _rf_mul(_rf_mul(u, one_minus_u), _rf_mul(v, one_minus_v))
    field = _rf_add(r, _rf_mul(beta, bubble))
    derivative_u = _rf_add(
        _rf_add(_rf([cu]), _rf_scale(v, cuv)),
        _rf_mul(beta, _rf_mul(_rf_sub(one, _rf_scale(u, Fraction(2))), _rf_mul(v, one_minus_v))),
    )
    derivative_v = _rf_add(
        _rf_add(_rf([cv]), _rf_scale(u, cuv)),
        _rf_mul(beta, _rf_mul(_rf_mul(u, one_minus_u), _rf_sub(one, _rf_scale(v, Fraction(2))))),
    )
    remainders = {
        "value": _rf_remainder(_rf_sub(field, one), defining),
        "du": _rf_remainder(derivative_u, defining),
        "dv": _rf_remainder(derivative_v, defining),
    }
    _require(
        all(remainder == [Fraction(0)] for remainder in remainders.values()),
        "all three contact identities",
    )
    gaps = [1 - value for value in corners]
    _require(all(value > 0 for value in gaps), "strict positive reciprocal-product weights")
    minimum_gap = min(gaps)
    _require(minimum_gap > 0, "uniform boundary divergence numerator")
    # Each reflected 1/(xy) has Hessian determinant numerator 2*2-1=3.
    # Positive gap weights imply strict joint convexity; boundary divergence
    # and the verified interior contact establish the unique global minimum.
    convexity = {
        "corner_gaps": gaps,
        "hessian_determinant_numerator": 2 * 2 - 1,
        "minimum_corner_gap": minimum_gap,
    }
    return {
        "raw_eliminant": raw,
        "normalization_scalar": normalization,
        "defining_polynomial": defining,
        "roots": root_records,
        "alpha_interval": alpha,
        "k_interval": k_interval,
        "u_image": {"numerator": u_num, "denominator": u_den},
        "beta_image": {"numerator": beta_num, "denominator": beta_den},
        "u_interval": u_interval,
        "beta_interval": beta_interval,
        "denominator_intervals": {"u": u_den_interval, "beta": beta_den_interval},
        "contact_remainders": remainders,
        "convexity": convexity,
        "status": "exact_positive_boundary",
    }


def _beta_affine(offset, scale):
    _require(
        type(offset) is Fraction and type(scale) is Fraction, "native beta-affine coefficients"
    )
    if scale == 0:
        return offset
    return {"kind": "beta_affine", "offset": offset, "scale": scale}


def _endpoint_coefficients(value):
    if type(value) is Fraction:
        return value, Fraction(0)
    _record(value, ("kind", "offset", "scale"), "algebraic endpoint fields")
    _require(value["kind"] == "beta_affine", "known algebraic endpoint kind")
    _require(
        type(value["offset"]) is Fraction and type(value["scale"]) is Fraction,
        "native algebraic endpoint coefficients",
    )
    return value["offset"], value["scale"]


def _endpoint_normalize(value):
    return _beta_affine(*_endpoint_coefficients(value))


def _endpoint_compare(left, right, beta_interval):
    enclosure = _rational_interval(beta_interval)
    a, b = _endpoint_coefficients(left)
    c, d = _endpoint_coefficients(right)
    if (a, b) == (c, d):
        return 0
    offset, scale = a - c, b - d
    values = [offset + scale * bound for bound in enclosure]
    lower, upper = min(values), max(values)
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ValueError("unresolved algebraic endpoint order at the fixed enclosure")


def _merge_endpoint_intervals(intervals, beta_interval):
    beta_interval = _rational_interval(beta_interval)
    _require(type(intervals) is list, "algebraic interval list")
    copied = []
    for interval in intervals:
        _vector(interval, 2, "two algebraic interval endpoints")
        pair = [_endpoint_normalize(endpoint) for endpoint in interval]
        _require(
            _endpoint_compare(pair[0], pair[1], beta_interval) <= 0, "ordered algebraic interval"
        )
        copied.append(pair)
    copied.sort(
        key=cmp_to_key(lambda first, second: _endpoint_compare(first[0], second[0], beta_interval))
    )
    merged = []
    for lower, upper in copied:
        if not merged or _endpoint_compare(lower, merged[-1][1], beta_interval) > 0:
            merged.append([lower, upper])
        elif _endpoint_compare(upper, merged[-1][1], beta_interval) > 0:
            merged[-1][1] = upper
    return merged


def _intersect_endpoint_unions(left, right, beta_interval):
    first = _merge_endpoint_intervals(left, beta_interval)
    second = _merge_endpoint_intervals(right, beta_interval)
    pieces = []
    for a, b in first:
        for c, d in second:
            lower = a if _endpoint_compare(a, c, beta_interval) >= 0 else c
            upper = b if _endpoint_compare(b, d, beta_interval) <= 0 else d
            if _endpoint_compare(lower, upper, beta_interval) <= 0:
                pieces.append([lower, upper])
    return _merge_endpoint_intervals(pieces, beta_interval)


def _endpoint_subset(left, right, beta_interval):
    return _intersect_endpoint_unions(left, right, beta_interval) == _merge_endpoint_intervals(
        left, beta_interval
    )


def _project_endpoint_union(union, offset, scale, beta_interval):
    _require(type(offset) is Fraction and type(scale) is Fraction, "native target map")
    source = _merge_endpoint_intervals(union, beta_interval)
    images = []
    for interval in source:
        image = []
        for endpoint in interval:
            a, b = _endpoint_coefficients(endpoint)
            image.append(_beta_affine(offset + scale * a, scale * b))
        images.append(image if scale >= 0 else list(reversed(image)))
    return _merge_endpoint_intervals(images, beta_interval)


def _endpoint_set_summary(union, beta_interval):
    intervals = _merge_endpoint_intervals(union, beta_interval)
    hull = [intervals[0][0], intervals[-1][1]] if intervals else None
    gaps = [[first[1], second[0]] for first, second in pairwise(intervals)]
    _require(
        all(_endpoint_compare(lower, upper, beta_interval) < 0 for lower, upper in gaps),
        "genuine open algebraic union gaps",
    )
    return {"intervals": intervals, "hull": hull, "gaps": gaps}


def _resolved_position(previous, offset, scale, beta_interval):
    negative_inner = _intersect_unions(previous["inner_theta"], [[None, Fraction(0)]])
    negative_outer = _intersect_unions(previous["outer_theta"], [[None, Fraction(0)]])
    _require(
        negative_inner == negative_outer, "data-restricted negative admission must already be exact"
    )
    _finite(negative_inner)
    positive = _intersect_endpoint_unions(
        [previous["data_theta"]],
        [[Fraction(0), _beta_affine(Fraction(0), Fraction(1))]],
        beta_interval,
    )
    theta = _merge_endpoint_intervals(negative_inner + positive, beta_interval)
    targets = _project_endpoint_union(theta, offset, scale, beta_interval)
    for inner, exact, outer in (
        (previous["inner_theta"], theta, previous["outer_theta"]),
        (previous["inner_targets"], targets, previous["outer_targets"]),
    ):
        _require(
            _endpoint_subset(inner, exact, beta_interval)
            and _endpoint_subset(exact, outer, beta_interval),
            "resolved position remains in the BJ sandwich",
        )
        if inner == outer:
            _require(
                exact == _merge_endpoint_intervals(inner, beta_interval),
                "already exact position set unchanged",
            )
    return {
        "position_id": previous["position_id"],
        "data_theta": list(previous["data_theta"]),
        "negative_theta": [list(interval) for interval in negative_inner],
        "theta": theta,
        "targets": targets,
        "status": "exact",
    }


def _resolved_hypotheses_subset(left, right, left_field, right_field, beta_interval):
    right_index = {entry["position_id"]: entry for entry in right}
    return all(
        entry["position_id"] in right_index
        and _endpoint_subset(
            entry[left_field], right_index[entry["position_id"]][right_field], beta_interval
        )
        for entry in left
    )


def _resolved_menus(previous_menus, positions, beta_interval):
    by_position = {position["position_id"]: position for position in positions}
    _require(len(by_position) == len(positions), "unique resolved positions")
    result = []
    for previous in previous_menus:
        hypotheses = []
        for name in previous["position_ids"]:
            _require(name in by_position, "known resolved menu position")
            position = by_position[name]
            if position["theta"]:
                hypotheses.append(
                    {
                        "position_id": name,
                        "theta": _merge_endpoint_intervals(position["theta"], beta_interval),
                        "targets": _merge_endpoint_intervals(position["targets"], beta_interval),
                    }
                )
        summary = _endpoint_set_summary(
            [interval for entry in hypotheses for interval in entry["targets"]], beta_interval
        )
        targets = summary["intervals"]
        if not hypotheses:
            existence, target_status = "infeasible", "infeasible"
        else:
            existence = "feasible"
            target_status = (
                "identified"
                if len(targets) == 1
                and _endpoint_compare(targets[0][0], targets[0][1], beta_interval) == 0
                else "ambiguous"
            )
        _require(
            _resolved_hypotheses_subset(
                previous["inner"], hypotheses, "theta", "theta", beta_interval
            )
            and _resolved_hypotheses_subset(
                hypotheses, previous["outer"], "theta", "theta", beta_interval
            ),
            "resolved menu hypothesis sandwich",
        )
        old_inner = previous["target_sets"]["inner"]["intervals"]
        old_outer = previous["target_sets"]["outer"]["intervals"]
        _require(
            _endpoint_subset(old_inner, targets, beta_interval)
            and _endpoint_subset(targets, old_outer, beta_interval),
            "resolved menu target sandwich",
        )
        if previous["hypothesis_set_status"] == "exact":
            normalized = [
                {
                    "position_id": entry["position_id"],
                    "theta": _merge_endpoint_intervals(entry["theta"], beta_interval),
                    "targets": _merge_endpoint_intervals(entry["targets"], beta_interval),
                }
                for entry in previous["inner"]
            ]
            _require(hypotheses == normalized, "already exact menu hypotheses unchanged")
        if previous["target_set_status"] == "exact":
            _require(
                targets == _merge_endpoint_intervals(old_inner, beta_interval),
                "already exact menu targets unchanged",
            )
        if previous["existence_status"] in ("feasible", "infeasible"):
            _require(
                existence == previous["existence_status"], "settled existence status unchanged"
            )
        if previous["target_status"] in ("identified", "ambiguous", "infeasible"):
            _require(
                target_status == previous["target_status"],
                "settled target classification unchanged",
            )
        result.append(
            {
                "id": previous["id"],
                "position_ids": list(previous["position_ids"]),
                "hypotheses": hypotheses,
                "target_set": summary,
                "existence_status": existence,
                "target_status": target_status,
                "status": "exact",
            }
        )
    all_menus = [menu for menu in result if menu["id"] == "all"]
    _require(len(all_menus) == 1, "one resolved all-position menu")
    whole = {entry["position_id"]: entry for entry in all_menus[0]["hypotheses"]}
    for menu in result:
        _require(
            menu["hypotheses"] == [whole[name] for name in menu["position_ids"] if name in whole],
            "resolved menus filter the all-position hypotheses",
        )
    return result


def _resolution_nesting(previous, current, beta_interval):
    _require(
        _is_subset([previous["response_interval"]], [current["response_interval"]]),
        "resolved response budgets nested",
    )
    _require(len(previous["positions"]) == len(current["positions"]), "resolved position census")
    for old, new in zip(previous["positions"], current["positions"]):
        _require(old["position_id"] == new["position_id"], "resolved position order")
        _require(
            _is_subset([old["data_theta"]], [new["data_theta"]]), "resolved data inversion nesting"
        )
        _require(
            _is_subset(old["negative_theta"], new["negative_theta"]),
            "preserved negative budget nesting",
        )
        _require(
            _endpoint_subset(old["theta"], new["theta"], beta_interval)
            and _endpoint_subset(old["targets"], new["targets"], beta_interval),
            "exact position sets nested across budgets",
        )
    _require(len(previous["menus"]) == len(current["menus"]), "resolved menu census")
    for old, new in zip(previous["menus"], current["menus"]):
        _require(old["id"] == new["id"], "resolved menu order")
        _require(
            _endpoint_subset(
                old["target_set"]["intervals"], new["target_set"]["intervals"], beta_interval
            ),
            "exact menu target unions nested across budgets",
        )


def _resolve_collection(bj_model, selected_case, certificate):
    beta_interval = certificate["beta_interval"]
    cases = bj_model["refinement"]
    selected = [case for case in cases if case["id"] == selected_case["id"]]
    _require(len(selected) == 1, "unique selected quarter-refinement case")
    constraints = selected[0]["constraints"]
    global_negative_inner = _intersect_unions(constraints["inner_theta"], [[None, Fraction(0)]])
    global_negative_outer = _intersect_unions(constraints["outer_theta"], [[None, Fraction(0)]])
    remaining_negative_gap = global_negative_inner != global_negative_outer
    _require(remaining_negative_gap, "remaining global negative admission gap")
    budgets = []
    for old_budget in selected[0]["budgets"]:
        positions = [
            _resolved_position(
                position,
                selected_case["target_offset"],
                selected_case["target_slope"],
                beta_interval,
            )
            for position in old_budget["positions"]
        ]
        menus = _resolved_menus(old_budget["menus"], positions, beta_interval)
        budget = {
            "id": old_budget["id"],
            "response_interval": list(old_budget["response_interval"]),
            "positions": positions,
            "menus": menus,
        }
        if budgets:
            _resolution_nesting(budgets[-1], budget, beta_interval)
        budgets.append(budget)
    resolved_positions = sum(len(budget["positions"]) for budget in budgets)
    resolved_menus = sum(len(budget["menus"]) for budget in budgets)
    _require((resolved_positions, resolved_menus) == (18, 15), "fixed resolved schema census")
    complete_positions, complete_menus = resolved_positions, resolved_menus
    for case in cases:
        if case["id"] == selected_case["id"]:
            continue
        for budget in case["budgets"]:
            for position in budget["positions"]:
                if position["inner_theta"] == position["outer_theta"]:
                    _require(
                        position["inner_targets"] == position["outer_targets"],
                        "inherited exact hypothesis implies exact target",
                    )
                    complete_positions += 1
            for menu in budget["menus"]:
                if menu["hypothesis_set_status"] == "exact":
                    _require(menu["target_set_status"] == "exact", "inherited exact menu targets")
                    complete_menus += 1
    # This metadata flag records the actual remaining negative certificate gap.
    # It is deliberately the only boolean in the new report contract.
    return {
        "case_id": selected_case["id"],
        "positive_theta": [[Fraction(0), _beta_affine(Fraction(0), Fraction(1))]],
        "budgets": budgets,
        "summary": {
            "resolved_positions": resolved_positions,
            "resolved_menus": resolved_menus,
            "collection_exact_positions": complete_positions,
            "collection_exact_menus": complete_menus,
            "remaining_global_negative_gap": remaining_negative_gap,
        },
    }


def _validate_bk(protocol):
    _native(protocol)
    _record(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "model",
            "boundary",
            "comparison",
            "no_claims",
        ),
        "BK protocol fields",
    )
    _require(protocol["study"] == "QR-05BK", "BK study identifier")
    _require(type(protocol["version"]) is int and protocol["version"] == 1, "BK version")
    for key in ("base_commit", "classification", "comparison"):
        _require(type(protocol[key]) is str and protocol[key], "BK textual metadata")
    _require(type(protocol["model"]) is dict, "BJ model dictionary")
    _require(
        type(protocol["no_claims"]) is list
        and all(type(value) is str for value in protocol["no_claims"]),
        "BK no-claims list",
    )
    boundary = protocol["boundary"]
    _record(
        boundary,
        (
            "case_id",
            "A",
            "C",
            "D",
            "delta",
            "target_offset",
            "target_slope",
            "isolation",
            "polynomial_order",
            "root_filter",
            "endpoint_rule",
            "negative_rule",
        ),
        "BK boundary fields",
    )
    _require(boundary["case_id"] == "asymmetric", "fixed analytic case")
    for key in ("polynomial_order", "root_filter", "endpoint_rule", "negative_rule"):
        _require(type(boundary[key]) is str and boundary[key], "boundary textual rule")
    config = boundary["isolation"]
    expected_config = {"depth": 24, "max_depth": 64, "max_nodes": 4096, "max_degree": 12}
    _record(config, expected_config, "fixed isolation fields")
    for key, value in expected_config.items():
        _require(type(config[key]) is int and config[key] == value, "fixed isolation budget")
    for key, coefficients in (("A", (3, -1)), ("C", (5, 2)), ("D", (0, 1, -1)), ("delta", (-1, 2))):
        _vector(boundary[key], len(coefficients), "boundary polynomial shape")
        _require(
            [_fraction(value) for value in boundary[key]]
            == [Fraction(value) for value in coefficients],
            "fixed stationarity input coefficients",
        )
    _require(
        _fraction(boundary["target_offset"]) == Fraction(13, 216)
        and _fraction(boundary["target_slope"]) == Fraction(1, 144),
        "fixed analytic target input",
    )


def analyze(protocol: dict) -> dict:
    """Fresh BJ baseline and one exact positive analytic admission boundary."""
    _validate_bk(protocol)
    bj_model = _analyze_bj(protocol["model"])
    candidates = [
        case
        for case in bj_model["bi_model"]["cases"]
        if case["id"] == protocol["boundary"]["case_id"]
    ]
    _require(len(candidates) == 1, "unique analytic baseline case")
    selected = candidates[0]
    certificate = _boundary_certificate(protocol["boundary"], selected)
    resolution = _resolve_collection(bj_model, selected, certificate)
    flag = resolution["summary"]["remaining_global_negative_gap"]
    _require(type(flag) is bool and flag is True, "declared negative-boundary metadata flag")
    native_resolution = {
        **resolution,
        "summary": {
            key: value
            for key, value in resolution["summary"].items()
            if key != "remaining_global_negative_gap"
        },
    }
    _native({"bj_model": bj_model, "certificate": certificate, "resolution": native_resolution})
    return {"bj_model": bj_model, "certificate": certificate, "resolution": resolution}
