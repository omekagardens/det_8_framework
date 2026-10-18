"""Exact fixed-budget refinement with self-contained BI mathematical lineage.

Only definitions are evaluated at import.  Local helpers are statically adapted
from the preceding primary; no old executor or stored result is imported.
"""

from fractions import Fraction as F
from itertools import pairwise, product
from math import comb


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


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


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
            "outcomes",
            "positions",
            "menus",
            "cases",
            "profile_rule",
            "admission_rule",
            "inverse_rule",
            "position_rule",
            "set_rule",
            "hull_rule",
            "gap_probe_rule",
            "disclosure_rule",
            "witnesses",
            "domain_control",
            "third_oracle",
            "public_boundary",
            "comparison",
            "no_claims",
        ),
    )
    _require(protocol["study"] == "QR-05BG" and protocol["version"] == 1, "protocol version")
    geometry = protocol["geometry"]
    _fields(geometry, ("u", "v", "measure_factor", "sigma_rule", "field_rule"))
    _require(geometry["u"] == ["0", "1"] and geometry["v"] == ["0", "1"], "unit rectangle")
    _require(
        geometry["measure_factor"] == "1/2"
        and geometry["sigma_rule"] == "V^4"
        and geometry["field_rule"] == "F=V^2*f",
        "geometric conventions",
    )
    _require(protocol["stations"] == ["00", "10", "01", "11", "cc"], "station roles")
    _require(
        protocol["corners"] == [["0", "0"], ["1", "0"], ["0", "1"], ["1", "1"]],
        "fixed corner positions",
    )
    _require(protocol["outcomes"] == [-1, 1], "outcome order")
    positions = protocol["positions"]
    _require(type(positions) is list and len(positions) == 6, "six candidate positions")
    position_ids = []
    for position in positions:
        _fields(position, ("id", "position"))
        _require(type(position["id"]) is str and position["id"], "position identifier")
        _require(
            type(position["position"]) is list and len(position["position"]) == 2,
            "two position coordinates",
        )
        _require(
            all(0 < _fraction(x) < 1 for x in position["position"]), "strictly interior position"
        )
        position_ids.append(position["id"])
    _require(len(set(position_ids)) == len(position_ids), "unique position identifiers")
    menus = protocol["menus"]
    _require(type(menus) is list and len(menus) == 5, "five finite menus")
    menu_ids = []
    for menu in menus:
        _fields(menu, ("id", "position_ids"))
        _require(type(menu["id"]) is str and menu["id"], "menu identifier")
        names = menu["position_ids"]
        _require(
            type(names) is list and names and all(type(name) is str for name in names),
            "nonempty ordered position menu",
        )
        _require(
            len(set(names)) == len(names) and all(name in position_ids for name in names),
            "distinct known menu positions",
        )
        menu_ids.append(menu["id"])
    _require(len(set(menu_ids)) == len(menu_ids), "unique menu identifiers")
    _require(
        menus[0]["id"] == "all" and menus[0]["position_ids"] == position_ids,
        "first menu exhausts all declared positions",
    )
    cases = protocol["cases"]
    _require(type(cases) is list and len(cases) == 7, "seven population cases")
    case_ids = []
    for case in cases:
        _fields(case, ("id", "population_means"))
        _require(type(case["id"]) is str and case["id"], "case identifier")
        _require(
            type(case["population_means"]) is list and len(case["population_means"]) == 5,
            "five role-labeled population means",
        )
        for mean in case["population_means"]:
            _polarization(mean)
        case_ids.append(case["id"])
    _require(len(set(case_ids)) == len(case_ids), "unique public case identifiers")
    witnesses = protocol["witnesses"]
    _require(type(witnesses) is list and len(witnesses) == 2, "two declared witnesses")
    witness_ids = []
    for witness in witnesses:
        _fields(witness, ("id", "case_id", "position_ids"))
        _require(type(witness["id"]) is str and witness["id"], "witness identifier")
        _require(witness["case_id"] in case_ids, "witness public case")
        names = witness["position_ids"]
        _require(
            type(names) is list
            and len(names) == 2
            and all(type(x) is str for x in names)
            and names[0] != names[1]
            and all(x in position_ids for x in names),
            "witness positions",
        )
        witness_ids.append(witness["id"])
    _require(witness_ids == ["target_ambiguity", "harmless_position_ambiguity"], "witness order")
    control = protocol["domain_control"]
    _fields(control, ("case_id", "position_id", "rule"))
    _require(
        control["case_id"] in case_ids and control["position_id"] in position_ids,
        "domain-control references",
    )


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


def _compile_geometry(protocol):
    bounds, measure, basis, kernel, corners, normalization, old = _base_geometry(protocol)
    bubble = _poly_multiply(basis[0], basis[3])
    q = [
        normalization * _integral(_poly_multiply(function, kernel), bounds, measure)
        for function in [*basis, bubble]
    ]
    _require(q[:4] == old["weights"], "complete geometric coefficient integrals")
    _require(q[4] > 0, "target is injective in the remaining bubble coefficient")
    return (
        {
            "volume": old["volume"],
            "sigma": old["sigma"],
            "coefficient_integrals": q,
        },
        bounds,
        measure,
        basis,
        bubble,
        kernel,
        corners,
        normalization,
    )


def _position(supplied, q, basis, bubble, corners):
    position = [_fraction(value) for value in supplied["position"]]
    sites = [*corners, position]
    a = [[_poly_value(function, *site) for function in [*basis, bubble]] for site in sites]
    decoder = _inverse(a)
    left, right = _dense_product(decoder, a), _dense_product(a, decoder)
    _require(left == right == _dense_identity(5), "two-sided population inverse")
    weights = _dense_product([q], decoder)[0]
    residual = [x - y for x, y in zip(_dense_product([weights], a)[0], q, strict=True)]
    _require(all(value == 0 for value in residual), "full target compilation")
    _require(a[4][4] > 0, "strict interior basis response")
    return {
        "id": supplied["id"],
        "position": position,
        "basis": list(a[4]),
        "evaluation_matrix": a,
        "coefficient_decoder": decoder,
        "left_inverse": left,
        "right_inverse": right,
        "full_weights": weights,
        "full_residual": residual,
    }, sites


def _validate_refinement(protocol):
    _native(protocol)
    _fields(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "model",
            "certificate",
            "set_rule",
            "existence_rule",
            "target_rule",
            "exactness_rule",
            "comparison",
            "no_claims",
        ),
    )
    _require(
        protocol["study"] == "QR-05BH" and protocol["version"] == 1, "refinement protocol version"
    )
    _validate(protocol["model"])
    certificate = protocol["certificate"]
    _fields(
        certificate,
        (
            "degree",
            "local_nodes",
            "root",
            "leaves",
            "witness_points",
            "coefficient_order",
            "reconstruction_rule",
            "classification_rule",
            "root_rule",
            "witness_rule",
        ),
    )
    _require(certificate["degree"] == [2, 2], "fixed tensor polynomial degree")
    _require(certificate["local_nodes"] == ["0", "1/2", "1"], "fixed unisolvent nodes")
    expected = [
        ("root", [["0", "1"], ["0", "1"]]),
        ("ll", [["0", "1/2"], ["0", "1/2"]]),
        ("lh", [["0", "1/2"], ["1/2", "1"]]),
        ("hl", [["1/2", "1"], ["0", "1/2"]]),
        ("hh", [["1/2", "1"], ["1/2", "1"]]),
    ]
    _require(
        type(certificate["leaves"]) is list and len(certificate["leaves"]) == 4,
        "four covering fixed leaves",
    )
    for patch, (name, bounds) in zip(
        [certificate["root"], *certificate["leaves"]], expected, strict=True
    ):
        _fields(patch, ("id", "bounds"))
        _require(patch["id"] == name and patch["bounds"] == bounds, "fixed covering partition")
    nodes = certificate["local_nodes"]
    _require(
        certificate["witness_points"] == [[u, v] for u in nodes for v in nodes],
        "fixed physical witness grid",
    )


def _affine_power(poly, bounds):
    """Coefficients of f(a+(b-a)s,c+(d-c)t), from binomial substitution."""
    (a, b), (c, d) = bounds
    width, height = b - a, d - c
    _require(width > 0 and height > 0, "positive patch rectangle")
    local = {}
    for (i, j), coefficient in poly.items():
        for p in range(i + 1):
            for q in range(j + 1):
                value = (
                    coefficient
                    * comb(i, p)
                    * a ** (i - p)
                    * width**p
                    * comb(j, q)
                    * c ** (j - q)
                    * height**q
                )
                local[p, q] = local.get((p, q), F(0)) + value
    return {powers: value for powers, value in local.items() if value}


def _power_to_bernstein(local):
    # s^p = sum_{i>=p} binom(i,p)/binom(2,p) B_i(s), independently per axis.
    return [
        [
            sum(
                (
                    coefficient * F(comb(i, p), comb(2, p)) * F(comb(j, q), comb(2, q))
                    for (p, q), coefficient in local.items()
                    if p <= i and q <= j
                ),
                F(0),
            )
            for j in range(3)
        ]
        for i in range(3)
    ]


def _bernstein_values(x):
    return [F(comb(2, i)) * x**i * (1 - x) ** (2 - i) for i in range(3)]


def _validate_bi(protocol):
    _native(protocol)
    _fields(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "model",
            "interval_budgets",
            "response_rule",
            "constraint_rule",
            "inner_rule",
            "outer_rule",
            "interval_rule",
            "law_rule",
            "set_rule",
            "comparison",
            "no_claims",
        ),
    )
    _require(
        protocol["study"] == "QR-05BI" and protocol["version"] == 1, "interval protocol version"
    )
    _validate_refinement(protocol["model"])
    budgets = protocol["interval_budgets"]
    _require(type(budgets) is list and len(budgets) == 3, "three prospectively fixed budgets")
    for budget, name, radius in zip(
        budgets, ("point", "narrow", "wide"), ("0", "1/64", "1/8"), strict=True
    ):
        _fields(budget, ("id", "radius"))
        _require(budget["id"] == name and budget["radius"] == radius, "fixed response budgets")


def _exact(value):
    _require(type(value) in (F, int), "exact internal rational")
    return F(value)


def _copy_interval(interval):
    if interval is None:
        return None
    _require(type(interval) is list and len(interval) == 2, "closed interval shape")
    lower, upper = [None if x is None else _exact(x) for x in interval]
    _require(lower is None or upper is None or lower <= upper, "nonempty closed interval")
    return [lower, upper]


def _intersect_intervals(left, right):
    left, right = _copy_interval(left), _copy_interval(right)
    if left is None or right is None:
        return None
    lower = right[0] if left[0] is None else left[0]
    if right[0] is not None and lower is not None:
        lower = max(lower, right[0])
    upper = right[1] if left[1] is None else left[1]
    if right[1] is not None and upper is not None:
        upper = min(upper, right[1])
    if lower is not None and upper is not None and lower > upper:
        return None
    return [lower, upper]


def _solve_constraints(pairs):
    """Sequentially clip the real line by every exact |a+b*theta| <= 1."""
    _require(type(pairs) is list, "constraint list")
    parsed = []
    for pair in pairs:
        _require(type(pair) is list and len(pair) == 2, "affine constraint pair")
        parsed.append([_exact(x) for x in pair])
    result = [None, None]
    for intercept, slope in parsed:
        if slope == 0:
            permitted = [None, None] if abs(intercept) <= 1 else None
        else:
            endpoints = [(-1 - intercept) / slope, (1 - intercept) / slope]
            permitted = [min(endpoints), max(endpoints)]
        result = _intersect_intervals(result, permitted)
    return result


def _merge_intervals(intervals):
    """Canonical closed union; null entries are empty, null endpoints infinite."""
    _require(type(intervals) is list, "interval union list")
    copied = [_copy_interval(interval) for interval in intervals]
    ordered = sorted(
        [interval for interval in copied if interval is not None],
        key=lambda interval: (0, F(0)) if interval[0] is None else (1, interval[0]),
    )
    result = []
    for interval in ordered:
        if result and (
            result[-1][1] is None or interval[0] is None or interval[0] <= result[-1][1]
        ):
            if result[-1][1] is None or interval[1] is None:
                result[-1][1] = None
            else:
                result[-1][1] = max(result[-1][1], interval[1])
        else:
            result.append(list(interval))
    return result


def _intersect_unions(left, right):
    left, right = _merge_intervals(left), _merge_intervals(right)
    return _merge_intervals([_intersect_intervals(a, b) for a in left for b in right])


def _project_union(union, offset, slope):
    union = _merge_intervals(union)
    offset, slope = _exact(offset), _exact(slope)
    if not union:
        return []
    if slope == 0:
        return [[offset, offset]]
    result = []
    for lower, upper in union:
        first = None if lower is None else offset + slope * lower
        second = None if upper is None else offset + slope * upper
        result.append([first, second] if slope > 0 else [second, first])
    return _merge_intervals(result)


def _subset(left, right):
    return _intersect_unions(left, right) == _merge_intervals(left)


def _finite(union):
    result = _merge_intervals(union)
    _require(all(x is not None for interval in result for x in interval), "finite retained union")
    return result


def _contains(union, value):
    return any(
        (lower is None or lower <= value) and (upper is None or value <= upper)
        for lower, upper in _merge_intervals(union)
    )


def _affine_patch(supplied, poly_zero, poly_one, nodes):
    bounds = [[_fraction(value) for value in axis] for axis in supplied["bounds"]]
    power_zero, power_one = _affine_power(poly_zero, bounds), _affine_power(poly_one, bounds)
    net_zero, net_one = _power_to_bernstein(power_zero), _power_to_bernstein(power_one)
    coefficients = [
        [[net_zero[i][j], net_one[i][j] - net_zero[i][j]] for j in range(3)] for i in range(3)
    ]
    (a, b), (c, d) = bounds
    residual = []
    for s in nodes:
        row = []
        bu = _bernstein_values(s)
        for t in nodes:
            bv = _bernstein_values(t)
            original_zero = _poly_value(poly_zero, a + (b - a) * s, c + (d - c) * t)
            original_one = _poly_value(poly_one, a + (b - a) * s, c + (d - c) * t)
            _require(
                original_zero == _poly_value(power_zero, s, t)
                and original_one == _poly_value(power_one, s, t),
                "two affine polynomial substitutions",
            )
            represented = [
                sum(
                    (
                        coefficients[i][j][component] * bu[i] * bv[j]
                        for i in range(3)
                        for j in range(3)
                    ),
                    F(0),
                )
                for component in range(2)
            ]
            row.append(
                [
                    original_zero - represented[0],
                    original_one - original_zero - represented[1],
                ]
            )
        residual.append(row)
    _require(
        all(x == 0 for row in residual for pair in row for x in pair),
        "full affine Bernstein reconstruction",
    )
    pairs = [pair for row in coefficients for pair in row]
    return {
        "id": supplied["id"],
        "bounds": bounds,
        "coefficients": coefficients,
        "reconstruction_residual": residual,
        "allowed": [[_solve_constraints([pair]) for pair in row] for row in coefficients],
        "theta_interval": _solve_constraints(pairs),
    }


def _constraints(corners, basis, bubble, certificate):
    zero = _model_polynomial(corners, F(0), basis, bubble)
    one = _model_polynomial(corners, F(1), basis, bubble)
    _require(
        all(0 <= i <= 2 and 0 <= j <= 2 for poly in (zero, one) for i, j in poly),
        "declared polynomial degree",
    )
    nodes = [_fraction(x) for x in certificate["local_nodes"]]
    patches = [
        _affine_patch(patch, zero, one, nodes)
        for patch in [certificate["root"], *certificate["leaves"]]
    ]
    witnesses = []
    for supplied in certificate["witness_points"]:
        point = [_fraction(x) for x in supplied]
        intercept = _poly_value(zero, *point)
        pair = [intercept, _poly_value(one, *point) - intercept]
        witnesses.append({"position": point, "value": pair, "allowed": _solve_constraints([pair])})
    g = 16 * (1 - max(map(abs, corners)))
    old = [-g, g] if g >= 0 else None
    leaf_pairs = [pair for patch in patches[1:] for row in patch["coefficients"] for pair in row]
    bernstein = _solve_constraints(leaf_pairs)
    witness = _solve_constraints([item["value"] for item in witnesses])
    inner, outer = _merge_intervals([old, bernstein]), _merge_intervals([witness])
    _require(
        old is not None
        and bernstein is not None
        and _contains([old], F(0))
        and _contains([bernstein], F(0)),
        "valid exact corners admit theta zero through both sufficient routes",
    )
    _require(len(inner) == 1, "overlapping sufficient routes form one global interval")
    _require(_subset(inner, outer), "global certificates imply every witness inequality")
    root = patches[0]["theta_interval"]
    _require(
        _subset(_merge_intervals([root]), _merge_intervals([bernstein])),
        "root certification implies covering-leaf certification",
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


def _law_family(corners, instrument):
    corner_state, corner_size = _tensor_state(corners)
    constant = _matrix_scale(_identity(2), F(1, 2))
    derivative = {(0, 0): F(1, 2), (1, 1): F(-1, 2)}
    rho_zero, size = _tensor(corner_state, corner_size, constant, 2)
    rho_slope, slope_size = _tensor(corner_state, corner_size, derivative, 2)
    _require(size == slope_size == 32, "complete five-factor affine state")
    _require(
        _trace(rho_zero, size) == 1 and _trace(rho_slope, size) == 0, "affine input normalization"
    )
    rows, averaged_zero, averaged_slope = [], {}, {}
    for outcomes, operator in zip(product((-1, 1), repeat=5), instrument, strict=True):
        adjoint = _adjoint(operator)
        branch_zero = _matrix_multiply(_matrix_multiply(operator, rho_zero), adjoint)
        branch_slope = _matrix_multiply(_matrix_multiply(operator, rho_slope), adjoint)
        diag_zero, diag_slope = _diagonal(branch_zero, size), _diagonal(branch_slope, size)
        probability = [_trace(branch_zero, size), _trace(branch_slope, size)]
        diagonal = [[a, b] for a, b in zip(diag_zero, diag_slope, strict=True)]
        _require(
            [sum((pair[k] for pair in diagonal), F(0)) for k in range(2)] == probability,
            "both branch-trace coefficients",
        )
        rows.append(
            {"outcomes": list(outcomes), "probability": probability, "state_diagonal": diagonal}
        )
        averaged_zero = _matrix_add(averaged_zero, branch_zero)
        averaged_slope = _matrix_add(averaged_slope, branch_slope)
    _require(
        averaged_zero == rho_zero and averaged_slope == rho_slope,
        "complete affine nonselective instrument",
    )
    _require(
        [sum((row["probability"][k] for row in rows), F(0)) for k in range(2)] == [F(1), F(0)],
        "complete coupled law normalization",
    )
    return {
        "rows": rows,
        "averaged_state": [
            [a, b]
            for a, b in zip(
                _diagonal(averaged_zero, size), _diagonal(averaged_slope, size), strict=True
            )
        ],
    }


def _endpoint_check(family, corners, mean):
    _require(-1 <= mean <= 1, "physical response endpoint")
    probabilities, entries, trace_residuals = [], [], []
    summed_diagonal = [F(0)] * 32
    for row in family["rows"]:
        probability = row["probability"][0] + mean * row["probability"][1]
        diagonal = [pair[0] + mean * pair[1] for pair in row["state_diagonal"]]
        probabilities.append(probability)
        entries.extend(diagonal)
        trace_residuals.append(abs(sum(diagonal, F(0)) - probability))
        summed_diagonal = [a + b for a, b in zip(summed_diagonal, diagonal, strict=True)]
    averaged = [pair[0] + mean * pair[1] for pair in family["averaged_state"]]
    direct_state, size = _tensor_state([*corners, mean])
    _require(
        averaged == summed_diagonal == _diagonal(direct_state, size),
        "endpoint averaged-state reconstruction",
    )
    result = {
        "mean": mean,
        "probability_sum": sum(probabilities, F(0)),
        "averaged_trace": sum(averaged, F(0)),
        "minimum_probability": min(probabilities),
        "minimum_state_entry": min(entries),
        "maximum_trace_residual": max(trace_residuals),
    }
    _require(
        result["probability_sum"] == result["averaged_trace"] == 1
        and result["minimum_probability"] >= 0
        and result["minimum_state_entry"] >= 0
        and result["maximum_trace_residual"] == 0,
        "whole coupled affine law segment is physical",
    )
    return result


def _position_report(position, sites, corners, response, constraints, q, basis, bubble, point):
    intercept, slope = _dot(position["basis"][:4], corners), position["basis"][4]
    _require(slope > 0, "strictly interior response slope")
    theta = [(value - intercept) / slope for value in response]
    offset, target_slope = _dot(q[:4], corners), q[4]
    target = [offset + target_slope * value for value in theta]
    residual = []
    for mean, value in zip(response, theta, strict=True):
        coefficients = [*corners, value]
        poly = _model_polynomial(corners, value, basis, bubble)
        reconstructed = [_poly_value(poly, *site) for site in sites]
        means = [*corners, mean]
        row = [a - b for a, b in zip(reconstructed, means, strict=True)]
        _require(
            coefficients == [_dot(decoder, means) for decoder in position["coefficient_decoder"]]
            and reconstructed
            == [_dot(evaluation, coefficients) for evaluation in position["evaluation_matrix"]]
            and all(x == 0 for x in row),
            "both inverse-image endpoint profiles reconstruct all responses",
        )
        residual.append(row)
    global_routes = {
        "old": _merge_intervals([constraints["old_theta"]]),
        "bernstein": _merge_intervals([constraints["bernstein_theta"]]),
        "inner": constraints["inner_theta"],
        "outer": constraints["outer_theta"],
    }
    routes = {
        name: _finite(_intersect_unions(union, [theta])) for name, union in global_routes.items()
    }
    _require(
        _merge_intervals([*routes["old"], *routes["bernstein"]]) == routes["inner"],
        "alternative sufficient routes use union, not conjunction",
    )
    _require(
        _subset(routes["old"], routes["inner"]) and _subset(routes["inner"], routes["outer"]),
        "data-intersected hypothesis enclosure",
    )
    projected = {
        name: _finite(_project_union(union, offset, target_slope)) for name, union in routes.items()
    }
    classification = None
    if point:
        _require(response[0] == response[1], "zero-width point budget")
        classification = (
            "certified" if routes["inner"] else "refuted" if not routes["outer"] else "unresolved"
        )
    return {
        "position_id": position["id"],
        "response_intercept": intercept,
        "response_slope": slope,
        "data_theta": theta,
        "data_target": target,
        "reconstruction_residual": residual,
        **{name + "_theta": union for name, union in routes.items()},
        **{name + "_targets": union for name, union in projected.items()},
        "point_classification": classification,
    }


def _set_summary(union):
    intervals = _finite(union)
    if not intervals:
        return {"intervals": [], "hull": None, "gaps": [], "gap_probes": []}
    gaps = [[a[1], b[0]] for a, b in pairwise(intervals)]
    probes = [(a + b) / 2 for a, b in gaps]
    _require(
        all(a < b for a, b in gaps) and all(not _contains(intervals, p) for p in probes),
        "actual open gaps and unattainable probes",
    )
    return {
        "intervals": intervals,
        "hull": [intervals[0][0], intervals[-1][1]],
        "gaps": gaps,
        "gap_probes": probes,
    }


def _menus(menus, position_reports):
    lookup = {}
    for position in position_reports:
        name = position["position_id"]
        _require(type(name) is str and name and name not in lookup, "distinct position reports")
        lookup[name] = position
    results, names = [], set()
    for menu in menus:
        name, position_ids = menu["id"], menu["position_ids"]
        _require(type(name) is str and name and name not in names, "distinct menu names")
        names.add(name)
        _require(
            type(position_ids) is list
            and all(type(x) is str and x in lookup for x in position_ids)
            and len(set(position_ids)) == len(position_ids),
            "known distinct ordered menu positions",
        )
        layers = {layer: [] for layer in ("old", "inner", "outer")}
        for position_id in position_ids:
            supplied = lookup[position_id]
            normalized = {}
            for layer, entries in layers.items():
                theta = _finite(supplied[layer + "_theta"])
                targets = _finite(supplied[layer + "_targets"])
                _require(
                    bool(theta) == bool(targets), "nonempty target image iff nonempty hypothesis"
                )
                normalized[layer] = (theta, targets)
                if theta:
                    entries.append({"position_id": position_id, "theta": theta, "targets": targets})
            for left, right in (("old", "inner"), ("inner", "outer")):
                _require(
                    all(
                        _subset(a, b)
                        for a, b in zip(normalized[left], normalized[right], strict=True)
                    ),
                    "per-position nested hypotheses and targets",
                )
        summaries = {
            layer: _set_summary([interval for entry in entries for interval in entry["targets"]])
            for layer, entries in layers.items()
        }
        inner, outer = summaries["inner"]["intervals"], summaries["outer"]["intervals"]
        if not outer:
            existence = target_status = "infeasible"
        else:
            existence = "feasible" if inner else "unresolved"
            if inner and len(outer) == 1 and outer[0][0] == outer[0][1]:
                target_status = "identified"
            elif inner and (len(inner) > 1 or inner[0][0] < inner[0][1]):
                target_status = "ambiguous"
            else:
                target_status = "unresolved"
        results.append(
            {
                "id": name,
                "position_ids": list(position_ids),
                "old": layers["old"],
                "inner": layers["inner"],
                "outer": layers["outer"],
                "target_sets": summaries,
                "existence_status": existence,
                "target_status": target_status,
                "hypothesis_set_status": "exact"
                if layers["inner"] == layers["outer"]
                else "bounded",
                "target_set_status": "exact" if inner == outer else "bounded",
            }
        )
    for small in results:
        for large in results:
            if set(small["position_ids"]).issubset(large["position_ids"]):
                for layer in ("old", "inner", "outer"):
                    pool = {row["position_id"]: row for row in large[layer]}
                    _require(
                        small[layer]
                        == [pool[name] for name in small["position_ids"] if name in pool],
                        "menu restriction is exact filtering",
                    )
                    _require(
                        _subset(
                            small["target_sets"][layer]["intervals"],
                            large["target_sets"][layer]["intervals"],
                        ),
                        "menu restriction preserves target containment",
                    )
    return results


def _budget_monotonicity(budgets):
    for small, large in pairwise(budgets):
        _require(
            _subset([small["response_interval"]], [large["response_interval"]]),
            "nested response budgets",
        )
        for left, right in zip(small["positions"], large["positions"], strict=True):
            _require(left["position_id"] == right["position_id"], "unchanged position order")
            for key in ("data_theta", "data_target"):
                _require(
                    _subset([left[key]], [right[key]]), "data inversion/projection monotonicity"
                )
            for route in ("old", "bernstein", "inner", "outer"):
                for suffix in ("_theta", "_targets"):
                    _require(
                        _subset(left[route + suffix], right[route + suffix]),
                        "every certified/necessary route is monotone",
                    )
        for left, right in zip(small["menus"], large["menus"], strict=True):
            _require(left["id"] == right["id"], "unchanged menu order")
            for layer in ("old", "inner", "outer"):
                pool = {entry["position_id"]: entry for entry in right[layer]}
                for entry in left[layer]:
                    _require(entry["position_id"] in pool, "wider budget cannot lose a hypothesis")
                    for key in ("theta", "targets"):
                        _require(
                            _subset(entry[key], pool[entry["position_id"]][key]),
                            "position-specific menu monotonicity",
                        )
                _require(
                    _subset(
                        left["target_sets"][layer]["intervals"],
                        right["target_sets"][layer]["intervals"],
                    ),
                    "menu target-union monotonicity",
                )


def _analyze_bi(protocol):
    """Compute this compact gate directly; never replay or nest an old analyzer."""
    _validate_bi(protocol)
    model = protocol["model"]["model"]
    certificate = protocol["model"]["certificate"]
    geometry, _bounds, _measure, basis, bubble, _kernel, corners, _normalization = (
        _compile_geometry(model)
    )
    q = geometry["coefficient_integrals"]
    compiled = [_position(position, q, basis, bubble, corners) for position in model["positions"]]
    positions = [position for position, _sites in compiled]
    instrument = _instrument(5)
    cases = []
    for supplied in model["cases"]:
        means = [_polarization(value) for value in supplied["population_means"]]
        c, center = means[:4], means[4]
        offset = _dot(q[:4], c)
        constraints = _constraints(c, basis, bubble, certificate)
        family = _law_family(c, instrument)
        budgets = []
        for declared in protocol["interval_budgets"]:
            radius = _fraction(declared["radius"])
            response = [max(F(-1), center - radius), min(F(1), center + radius)]
            reports = [
                _position_report(
                    position,
                    sites,
                    c,
                    response,
                    constraints,
                    q,
                    basis,
                    bubble,
                    declared["id"] == "point",
                )
                for position, sites in compiled
            ]
            budgets.append(
                {
                    "id": declared["id"],
                    "response_interval": response,
                    "endpoint_checks": [_endpoint_check(family, c, value) for value in response],
                    "positions": reports,
                    "menus": _menus(model["menus"], reports),
                }
            )
        _budget_monotonicity(budgets)
        cases.append(
            {
                "id": supplied["id"],
                "corners": c,
                "center_mean": center,
                "target_offset": offset,
                "target_slope": q[4],
                "constraints": constraints,
                "law_family": family,
                "budgets": budgets,
            }
        )
    return {"geometry": geometry, "positions": positions, "cases": cases}


def _validate_bj(protocol):
    _native(protocol)
    _fields(
        protocol,
        (
            "study",
            "version",
            "base_commit",
            "classification",
            "model",
            "refinement",
            "comparison",
            "no_claims",
        ),
    )
    _require(
        protocol["study"] == "QR-05BJ" and protocol["version"] == 1,
        "fixed-refinement protocol version",
    )
    _validate_bi(protocol["model"])
    refinement = protocol["refinement"]
    _fields(
        refinement,
        ("degree", "nodes", "leaves", "witness_nodes", "certificate_rule", "witness_rule"),
    )
    _require(refinement["degree"] == [2, 2], "unchanged Bernstein degree")
    _require(refinement["nodes"] == ["0", "1/2", "1"], "unchanged local unisolvent grid")
    _require(
        refinement["witness_nodes"] == ["0", "1/4", "1/2", "3/4", "1"],
        "fixed five-node witness axes",
    )
    leaves = refinement["leaves"]
    _require(type(leaves) is list and len(leaves) == 16, "exactly sixteen quarter leaves")
    parents = {
        parent["id"]: [[_fraction(x) for x in axis] for axis in parent["bounds"]]
        for parent in protocol["model"]["model"]["certificate"]["leaves"]
    }
    grouped = {name: [] for name in parents}
    for leaf, (i, j) in zip(leaves, product(range(4), repeat=2), strict=True):
        _fields(leaf, ("id", "parent", "bounds"))
        expected = [[str(F(i, 4)), str(F(i + 1, 4))], [str(F(j, 4)), str(F(j + 1, 4))]]
        parent = ("l" if i < 2 else "h") + ("l" if j < 2 else "h")
        _require(
            leaf["id"] == f"q{i}{j}" and leaf["parent"] == parent and leaf["bounds"] == expected,
            "fixed quarter bounds, parentage and ordering",
        )
        bounds = [[_fraction(x) for x in axis] for axis in leaf["bounds"]]
        grouped[parent].append(bounds)
    for name, children in grouped.items():
        (a, b), (c, d) = parents[name]
        _require(len(children) == 4, "four quarter children of every half-square")
        _require(
            all(a <= u0 < u1 <= b and c <= v0 < v1 <= d for (u0, u1), (v0, v1) in children),
            "child containment",
        )
        area = sum(((u1 - u0) * (v1 - v0) for (u0, u1), (v0, v1) in children), F(0))
        _require(area == (b - a) * (d - c), "complete child area coverage")
        for first, left in enumerate(children):
            for right in children[first + 1 :]:
                _require(
                    not (
                        max(left[0][0], right[0][0]) < min(left[0][1], right[0][1])
                        and max(left[1][0], right[1][0]) < min(left[1][1], right[1][1])
                    ),
                    "disjoint child interiors",
                )


def _nested_bounds(old_inner, new_inner, new_outer, old_outer, message):
    """Certify all set inclusions and persistence whenever the old bounds agree."""
    unions = [_merge_intervals(union) for union in (old_inner, new_inner, new_outer, old_outer)]
    _require(all(_subset(left, right) for left, right in pairwise(unions)), message)
    if unions[0] == unions[-1]:
        _require(
            all(union == unions[0] for union in unions), "previous exact set must remain identical"
        )


def _quarter_constraints(corners, basis, bubble, refinement, baseline):
    zero = _model_polynomial(corners, F(0), basis, bubble)
    one = _model_polynomial(corners, F(1), basis, bubble)
    nodes = [_fraction(x) for x in refinement["nodes"]]
    patches = [_affine_patch(leaf, zero, one, nodes) for leaf in refinement["leaves"]]
    values = [_fraction(x) for x in refinement["witness_nodes"]]
    witnesses = []
    for u, v in product(values, repeat=2):
        intercept = _poly_value(zero, u, v)
        pair = [intercept, _poly_value(one, u, v) - intercept]
        witnesses.append({"position": [u, v], "value": pair, "allowed": _solve_constraints([pair])})
    lookup = {tuple(witness["position"]): witness for witness in witnesses}
    for old_witness in baseline["witnesses"]:
        _require(
            lookup[tuple(old_witness["position"])] == old_witness,
            "complete inherited witness value and preimage agreement",
        )
    g = 16 * (1 - max(map(abs, corners)))
    old = [-g, g] if g >= 0 else None
    _require(old == baseline["old_theta"], "old sufficient route unchanged")
    bernstein = _solve_constraints(
        [pair for patch in patches for row in patch["coefficients"] for pair in row]
    )
    witness = _solve_constraints([row["value"] for row in witnesses])
    inner, outer = _merge_intervals([old, bernstein]), _merge_intervals([witness])
    _require(
        old is not None
        and bernstein is not None
        and _contains([old], F(0))
        and _contains([bernstein], F(0))
        and len(inner) == 1,
        "overlapping sufficient routes and connected global union",
    )
    _require(
        _subset(_merge_intervals([baseline["bernstein_theta"]]), _merge_intervals([bernstein])),
        "half-square coefficient certificate implies quarter-square certificate",
    )
    _nested_bounds(
        baseline["inner_theta"],
        inner,
        outer,
        baseline["outer_theta"],
        "nested global certificate and witness bounds",
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


def _nested_position(old, new):
    for key in (
        "position_id",
        "response_intercept",
        "response_slope",
        "data_theta",
        "data_target",
        "reconstruction_residual",
        "old_theta",
        "old_targets",
    ):
        _require(old[key] == new[key], "unchanged position data, response and old route")
    for suffix in ("_theta", "_targets"):
        _require(
            _subset(old["bernstein" + suffix], new["bernstein" + suffix]),
            "refined Bernstein route cannot lose an accepted value",
        )
        _nested_bounds(
            old["inner" + suffix],
            new["inner" + suffix],
            new["outer" + suffix],
            old["outer" + suffix],
            "nested per-position hypothesis and target sets",
        )
    if old["point_classification"] in ("certified", "refuted"):
        _require(
            new["point_classification"] == old["point_classification"],
            "decided point classification is preserved",
        )
    if old["point_classification"] is None:
        _require(new["point_classification"] is None, "no nonpoint classification")


def _nested_menu(old, new):
    _require(
        old["id"] == new["id"] and old["position_ids"] == new["position_ids"],
        "unchanged menu metadata",
    )
    _require(
        old["old"] == new["old"] and old["target_sets"]["old"] == new["target_sets"]["old"],
        "menu old sufficient route unchanged",
    )
    lookup = {
        (version, layer): {entry["position_id"]: entry for entry in menu[layer]}
        for version, menu in (("old", old), ("new", new))
        for layer in ("inner", "outer")
    }
    for position_id in old["position_ids"]:
        entries = [
            lookup[version, layer].get(position_id)
            for version, layer in (
                ("old", "inner"),
                ("new", "inner"),
                ("new", "outer"),
                ("old", "outer"),
            )
        ]
        for key in ("theta", "targets"):
            _nested_bounds(
                *(entry[key] if entry is not None else [] for entry in entries),
                "nested menu position-specific hypotheses and targets",
            )
    _nested_bounds(
        old["target_sets"]["inner"]["intervals"],
        new["target_sets"]["inner"]["intervals"],
        new["target_sets"]["outer"]["intervals"],
        old["target_sets"]["outer"]["intervals"],
        "nested merged menu target unions",
    )
    if old["hypothesis_set_status"] == "exact":
        _require(
            new["hypothesis_set_status"] == "exact"
            and old["inner"] == new["inner"] == new["outer"] == old["outer"],
            "exact hypothesis set persists",
        )
    if old["target_set_status"] == "exact":
        _require(
            new["target_set_status"] == "exact"
            and old["target_sets"]["inner"]
            == new["target_sets"]["inner"]
            == new["target_sets"]["outer"]
            == old["target_sets"]["outer"],
            "exact target union, hull and gaps persist",
        )
    if old["target_status"] == "ambiguous":
        _require(new["target_status"] == "ambiguous", "certified ambiguity cannot disappear")
    if old["existence_status"] in ("feasible", "infeasible"):
        _require(
            new["existence_status"] == old["existence_status"], "settled existence status persists"
        )


def _nested_case(old_budgets, new_budgets):
    for old, new in zip(old_budgets, new_budgets, strict=True):
        _require(
            old["id"] == new["id"] and old["response_interval"] == new["response_interval"],
            "unchanged response budget",
        )
        for previous, refined in zip(old["positions"], new["positions"], strict=True):
            _nested_position(previous, refined)
        for previous, refined in zip(old["menus"], new["menus"], strict=True):
            _nested_menu(previous, refined)


def analyze(protocol):
    """Recompute BI locally once, then evaluate precisely the new checking budget."""
    _validate_bj(protocol)
    bi_model = _analyze_bi(protocol["model"])
    model = protocol["model"]["model"]["model"]
    geometry, _bounds, _measure, basis, bubble, _kernel, corners, _normalization = (
        _compile_geometry(model)
    )
    _require(geometry == bi_model["geometry"], "same directly compiled supplied geometry")
    q = geometry["coefficient_integrals"]
    refinement = []
    for baseline in bi_model["cases"]:
        constraints = _quarter_constraints(
            baseline["corners"], basis, bubble, protocol["refinement"], baseline["constraints"]
        )
        budgets = []
        for old_budget in baseline["budgets"]:
            response = list(old_budget["response_interval"])
            positions = [
                _position_report(
                    position,
                    [*corners, position["position"]],
                    baseline["corners"],
                    response,
                    constraints,
                    q,
                    basis,
                    bubble,
                    old_budget["id"] == "point",
                )
                for position in bi_model["positions"]
            ]
            budgets.append(
                {
                    "id": old_budget["id"],
                    "response_interval": response,
                    "positions": positions,
                    "menus": _menus(model["menus"], positions),
                }
            )
        _budget_monotonicity(budgets)
        _nested_case(baseline["budgets"], budgets)
        refinement.append({"id": baseline["id"], "constraints": constraints, "budgets": budgets})
    return {"bi_model": bi_model, "refinement": refinement}
