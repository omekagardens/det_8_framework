"""Pure exact incidence-matrix route for the supplied-measure fixed study.

The graph, weights, marks and boundary data are supplied inputs.  Nothing is
read from a file or another implementation, and no physical model is selected.
"""

from fractions import Fraction


def _fraction(value, name):
    if type(value) is not Fraction:
        raise ValueError(f"{name} must be a plain Fraction")
    if abs(value.numerator).bit_length() > 128 or value.denominator.bit_length() > 128:
        raise ValueError(f"{name} exceeds the 128-bit input bound")


def _vector(value, length, name):
    if type(value) is not list or len(value) != length:
        raise ValueError(f"{name} must be a matching plain list")
    for item in value:
        _fraction(item, name)


def _labels(value, size, name):
    if type(value) is not list or len(value) > size:
        raise ValueError(f"{name} must be a bounded plain label list")
    if any(type(label) is not int or not 0 <= label < size for label in value):
        raise ValueError(f"{name} contains an invalid node label")
    if len(set(value)) != len(value):
        raise ValueError(f"{name} contains duplicate labels")


def _validate(world):
    fields = {"mu", "edges", "k", "x", "mode", "I", "D", "f", "g", "q"}
    if type(world) is not dict:
        raise ValueError("world must be a plain dict")
    if (
        len(world) != len(fields)
        or any(type(key) is not str for key in world)
        or set(world) != fields
    ):
        raise ValueError("world fields must match the declared API")
    mu = world["mu"]
    if type(mu) is not list or not 1 <= len(mu) <= 3:
        raise ValueError("mu must be a plain list with 1 through 3 nodes")
    n = len(mu)
    _vector(mu, n, "mu")
    if any(value <= 0 for value in mu):
        raise ValueError("node measures must be positive")
    edges = world["edges"]
    if type(edges) is not list or len(edges) > n * (n - 1) // 2:
        raise ValueError("edges must be a simple-graph plain list")
    occupied = set()
    for edge in edges:
        if type(edge) is not list or len(edge) != 2:
            raise ValueError("each edge must be a plain two-label list")
        if any(type(label) is not int or not 0 <= label < n for label in edge):
            raise ValueError("invalid edge node label")
        tail, head = edge
        if tail == head:
            raise ValueError("self-loops are not admitted")
        pair = tuple(sorted(edge))
        if pair in occupied:
            raise ValueError("duplicate undirected edge")
        occupied.add(pair)
    _vector(world["k"], len(edges), "k")
    if any(value < 0 for value in world["k"]):
        raise ValueError("edge conductances must be nonnegative")
    _vector(world["x"], n, "x")
    _vector(world["q"], n, "q")
    mode = world["mode"]
    if type(mode) is not str or mode not in ("closed", "flux", "dirichlet"):
        raise ValueError("invalid boundary mode")
    active, held = world["I"], world["D"]
    _labels(active, n, "I")
    _labels(held, n, "D")
    if set(active) & set(held) or set(active) | set(held) != set(range(n)):
        raise ValueError("I and D must partition every node")
    _vector(world["f"], len(active), "f")
    _vector(world["g"], len(held), "g")
    if mode == "dirichlet":
        if not active or not held:
            raise ValueError("Dirichlet mode needs interior and held nodes")
    elif active != list(range(n)) or held:
        raise ValueError("closed and flux modes require canonical all-node I")
    if mode != "flux" and any(value != 0 for value in world["q"]):
        raise ValueError("only flux mode admits prescribed outward q")


def _world_copy(world):
    result = {key: value[:] for key, value in world.items() if type(value) is list}
    result["edges"] = [edge[:] for edge in world["edges"]]
    result["mode"] = world["mode"]
    return result


def _diag(values):
    return [
        [value if i == j else Fraction(0) for j in range(len(values))]
        for i, value in enumerate(values)
    ]


def _transpose(matrix, columns):
    """Explicit width preserves the transpose of a zero-edge incidence matrix."""
    return [[row[column] for row in matrix] for column in range(columns)]


def _multiply(left, right, columns):
    """Matrix multiplication with explicit output width, including inner size 0."""
    return [
        [
            sum((row[k] * right[k][j] for k in range(len(right))), Fraction(0))
            for j in range(columns)
        ]
        for row in left
    ]


def _act(matrix, vector):
    return [sum((value * vector[j] for j, value in enumerate(row)), Fraction(0)) for row in matrix]


def _dot(left, right):
    return sum((value * right[i] for i, value in enumerate(left)), Fraction(0))


def _difference(left, right):
    return [[value - right[i][j] for j, value in enumerate(row)] for i, row in enumerate(left)]


def _negative(matrix):
    return [[-value for value in row] for row in matrix]


def _block(matrix, rows, columns):
    return [[matrix[i][j] for j in columns] for i in rows]


def _adjoint_residual(measure, operator):
    n = len(operator)
    return _difference(
        _multiply(measure, operator, n),
        _multiply(_transpose(operator, n), measure, n),
    )


def _moments(operator, coordinates):
    n = len(coordinates)
    return {
        "m0": [sum(row, Fraction(0)) for row in operator],
        "m1": [
            sum((row[j] * (coordinates[j] - coordinates[i]) for j in range(n)), Fraction(0))
            for i, row in enumerate(operator)
        ],
        "m2": [
            sum(
                (row[j] * (coordinates[j] - coordinates[i]) ** 2 for j in range(n)),
                Fraction(0),
            )
            / 2
            for i, row in enumerate(operator)
        ],
        "Q1": _act(operator, [Fraction(1) for _ in range(n)]),
        "Qx": _act(operator, coordinates),
        "Qx2": _act(operator, [value**2 for value in coordinates]),
    }


def _components(operator, nodes):
    """Find positive-support components from the operator, not supplied measures."""
    remaining = set(nodes)
    components = []
    while remaining:
        anchor = min(remaining)
        discovered = {anchor}
        pending = [anchor]
        while pending:
            node = pending.pop()
            for other in sorted(remaining - discovered):
                if operator[node][other] > 0:
                    discovered.add(other)
                    pending.append(other)
        components.append(sorted(discovered))
        remaining -= discovered
    return components


def _indicators(components, nodes):
    return [[Fraction(1 if node in component else 0) for node in nodes] for component in components]


def _recover_ratios(operator, components):
    """Recover relative measures using only directed operator-entry ratios."""
    normalized = [Fraction(0) for _ in operator]
    anchors = [0 for _ in operator]
    for component in components:
        anchor = component[0]
        normalized[anchor] = Fraction(1)
        seen = {anchor}
        pending = [anchor]
        for node in component:
            anchors[node] = anchor
        while pending:
            node = pending.pop()
            for other in component:
                if operator[node][other] > 0:
                    if operator[other][node] <= 0:
                        raise ValueError("operator support is not reversible")
                    candidate = normalized[node] * operator[node][other] / operator[other][node]
                    if other in seen:
                        if normalized[other] != candidate:
                            raise ValueError("operator ratios are not path-independent")
                    else:
                        normalized[other] = candidate
                        seen.add(other)
                        pending.append(other)
    return normalized, anchors


def evaluate(world):
    """Evaluate the complete exact incidence, moment and boundary report."""
    _validate(world)
    mu, edges, conductance = world["mu"], world["edges"], world["k"]
    coordinates, active, held = world["x"], world["I"], world["D"]
    f, g, outward = world["f"], world["g"], world["q"]
    n, m = len(mu), len(edges)
    incidence = [[Fraction(0) for _ in range(n)] for _ in edges]
    for e, (tail, head) in enumerate(edges):
        incidence[e][tail] = Fraction(-1)
        incidence[e][head] = Fraction(1)
    transpose_b = _transpose(incidence, n)
    measure, edge_measure = _diag(mu), _diag(conductance)
    # This route uses the declared incidence products, not neighbor assembly.
    laplacian = _multiply(_multiply(transpose_b, edge_measure, m), incidence, n)
    operator = _negative(_multiply(_diag([1 / value for value in mu]), laplacian, n))
    weighted_operator = _multiply(measure, operator, n)
    full = {
        **_moments(operator, coordinates),
        "counting_columns": _act(_transpose(operator, n), [Fraction(1) for _ in range(n)]),
        "weighted_columns": _act(_transpose(weighted_operator, n), [Fraction(1) for _ in range(n)]),
        "adjoint_residual": _adjoint_residual(measure, operator),
        "energy_form": _negative(weighted_operator),
    }

    field = [Fraction(0) for _ in range(n)]
    for position, node in enumerate(active):
        field[node] = f[position]
    for position, node in enumerate(held):
        field[node] = g[position]
    gradient = _act(incidence, field)
    flux_j = [-value for value in _act(edge_measure, gradient)]
    influx = _act(transpose_b, flux_j)
    active_set = set(active)
    cut_flux = [
        flux_j[e] if (tail in active_set) != (head in active_set) else Fraction(0)
        for e, (tail, head) in enumerate(edges)
    ]
    cut_influx = _act(transpose_b, cut_flux)
    reservoir_outward = [-cut_influx[node] for node in active]
    flux = {
        "field": field,
        "gradient": gradient,
        "J": flux_j,
        "influx": influx,
        "Qf": _act(operator, field),
        "dirichlet_outward": reservoir_outward,
    }

    components = _components(operator, range(n))
    kernel_basis = _indicators(components, range(n))
    relative_mu, anchors = _recover_ratios(operator, components)
    relative_k = [relative_mu[tail] * operator[tail][head] for tail, head in edges]
    reconstruction = {
        "mu_normalized": relative_mu,
        "k_normalized": relative_k,
        "detailed_balance": [
            [relative_mu[i] * operator[i][j] - relative_mu[j] * operator[j][i] for j in range(n)]
            for i in range(n)
        ],
        "mu_residual": [relative_mu[i] - mu[i] / mu[anchors[i]] for i in range(n)],
        "k_residual": [
            relative_k[e] - conductance[e] / mu[anchors[tail]]
            for e, (tail, _head) in enumerate(edges)
        ],
    }

    reduced_measure = _block(measure, active, active)
    reduced_operator = _block(operator, active, active)
    boundary_operator = _block(operator, active, held)
    boundary_source = _act(boundary_operator, g)
    source = [boundary_source[i] - outward[node] / mu[node] for i, node in enumerate(active)]
    homogeneous = _act(reduced_operator, f)
    derivative = [homogeneous[i] + source[i] for i in range(len(active))]
    interior_constant = _act(reduced_operator, [Fraction(1) for _ in active])
    boundary_constant = _act(boundary_operator, [Fraction(1) for _ in held])
    interior_components = _components(operator, active)
    anchored = [
        any(operator[node][boundary] > 0 for node in component for boundary in held)
        for component in interior_components
    ]
    interior_basis = _indicators(
        [component for component, attached in zip(interior_components, anchored) if not attached],
        active,
    )
    reduced = {
        "nodes": active[:],
        "W": reduced_measure,
        "Q": reduced_operator,
        "adjoint_residual": _adjoint_residual(reduced_measure, reduced_operator),
        **_moments(reduced_operator, [coordinates[node] for node in active]),
        "source": source,
        "fdot": derivative,
        "constant_balance": [
            interior_constant[i] + boundary_constant[i] - outward[node] / mu[node]
            for i, node in enumerate(active)
        ],
        "components": interior_components,
        "anchored": anchored,
        "kernel_basis": interior_basis,
        "kernel_images": [_act(reduced_operator, vector) for vector in interior_basis],
        "invertible": all(anchored),
    }
    internal_dissipation = sum(
        (
            conductance[e] * gradient[e] ** 2
            for e, (tail, head) in enumerate(edges)
            if tail in active_set and head in active_set
        ),
        Fraction(0),
    )
    external_work = _dot(f, [outward[node] for node in active])
    reservoir_work = _dot(f, reservoir_outward)
    mass_weights = [mu[node] for node in active]
    energy_weights = [mu[node] * f[i] for i, node in enumerate(active)]
    balances = {
        "mass": _dot(mass_weights, f),
        "energy": _dot(energy_weights, f) / 2,
        "mass_rate": _dot(mass_weights, derivative),
        "energy_rate": _dot(energy_weights, derivative),
        "mass_rhs": -sum((outward[node] for node in active), Fraction(0))
        - sum(reservoir_outward, Fraction(0)),
        "energy_rhs": -internal_dissipation - external_work - reservoir_work,
        "internal_dissipation": internal_dissipation,
        "external_work": external_work,
        "reservoir_work": reservoir_work,
        "ordinary_rate": sum(derivative, Fraction(0)),
    }
    return {
        "world": _world_copy(world),
        "B": incidence,
        "W": measure,
        "K": edge_measure,
        "L": laplacian,
        "Q": operator,
        "full": full,
        "flux": flux,
        "components": components,
        "kernel_basis": kernel_basis,
        "kernel_images": [_act(operator, vector) for vector in kernel_basis],
        "reconstruction": reconstruction,
        "reduced": reduced,
        "balances": balances,
    }


def _rationals(values):
    """Convert only internal literal fixtures, never public evaluate inputs."""
    return [Fraction(*value) if type(value) is tuple else Fraction(value) for value in values]


def _cases():
    """Independent literal fixture bank; every three-node base is an open path."""
    specifications = (
        ("singleton_closed", (1,), (), (0,), "closed", (0,), (), (2,), (), (0,)),
        ("unequal_closed", (1, 2), (1,), (0, 1), "closed", (0, 1), (), (0, 1), (), (0, 0)),
        (
            "zero_edge_closed",
            (1, 2, 1),
            (1, 0),
            (0, 1, 2),
            "closed",
            (0, 1, 2),
            (),
            (0, 1, 2),
            (),
            (0, 0, 0),
        ),
        (
            "arithmetic_face_closed",
            (1, 1, 1),
            ((3, 2), 1),
            (-1, 0, 1),
            "closed",
            (0, 1, 2),
            (),
            (0, 1, 0),
            (),
            (0, 0, 0),
        ),
        (
            "pointwise_reweighted",
            ((1, 2), 1, 1),
            (1, 1),
            (-1, 0, 1),
            "closed",
            (0, 1, 2),
            (),
            (0, 1, 0),
            (),
            (0, 0, 0),
        ),
        ("prescribed_flux", (1, 2), (1,), (0, 1), "flux", (0, 1), (), (1, 2), (), (2, -2)),
        (
            "dirichlet_grounded",
            (1, 1, 1),
            ((3, 2), 1),
            (-1, 0, 1),
            "dirichlet",
            (1,),
            (0, 2),
            (1,),
            (0, 0),
            (0, 0, 0),
        ),
        (
            "dirichlet_driven",
            (1, 1, 1),
            ((3, 2), 1),
            (-1, 0, 1),
            "dirichlet",
            (1,),
            (0, 2),
            ((1, 2),),
            (1, 1),
            (0, 0, 0),
        ),
        (
            "dirichlet_unanchored",
            (1, 2, 1),
            (1, 0),
            (0, 1, 2),
            "dirichlet",
            (1, 2),
            (0,),
            (1, 2),
            (0,),
            (0, 0, 0),
        ),
    )
    cases = []
    for (
        name,
        mu,
        conductance,
        coordinates,
        mode,
        active,
        held,
        field,
        boundary,
        outward,
    ) in specifications:
        cases.append(
            (
                name,
                {
                    "mu": _rationals(mu),
                    "edges": [[node, node + 1] for node in range(len(mu) - 1)],
                    "k": _rationals(conductance),
                    "x": _rationals(coordinates),
                    "mode": mode,
                    "I": list(active),
                    "D": list(held),
                    "f": _rationals(field),
                    "g": _rationals(boundary),
                    "q": _rationals(outward),
                },
            )
        )
    return cases


def _variant(world, name):
    result = _world_copy(world)
    n = len(world["mu"])
    if name == "identity":
        return result
    if name == "cyclic":
        for key in ("mu", "x", "q"):
            result[key] = [world[key][(node - 1) % n] for node in range(n)]
        result["edges"] = [[(tail + 1) % n, (head + 1) % n] for tail, head in world["edges"]]
        if world["mode"] == "dirichlet":
            result["I"] = [(node + 1) % n for node in world["I"]]
            result["D"] = [(node + 1) % n for node in world["D"]]
        else:
            result["I"] = list(range(n))
            result["f"] = [world["f"][(node - 1) % n] for node in range(n)]
        return result
    if name == "reversal":
        result["edges"] = [[head, tail] for tail, head in world["edges"]]
        return result
    if name == "rescale":
        for key in ("mu", "k", "q"):
            result[key] = [value * Fraction(3, 2) for value in world[key]]
        return result
    raise ValueError("unknown fixed variant")


def analyze():
    """Return the fixed 36 labelled reports and nine same-Q scale witnesses."""
    rows = []
    cases = _cases()
    for base, world in cases:
        for variant in ("identity", "cyclic", "reversal", "rescale"):
            row = evaluate(_variant(world, variant))
            row.update({"id": base + ":" + variant, "base": base, "variant": variant})
            rows.append(row)
    by_id = {row["id"]: row for row in rows}
    witnesses = []
    for base, _world in cases:
        left_id, right_id = base + ":identity", base + ":rescale"
        left, right = by_id[left_id], by_id[right_id]
        if left["Q"] != right["Q"]:
            raise ValueError("fixed scale witness has different operators")
        if left["world"]["mu"] == right["world"]["mu"]:
            raise ValueError("fixed scale witness must have different measures")
        witnesses.append(
            {
                "base": base,
                "rows": [left_id, right_id],
                "Q": [row[:] for row in left["Q"]],
                "measures": [left["world"]["mu"][:], right["world"]["mu"][:]],
                "conductances": [left["world"]["k"][:], right["world"]["k"][:]],
            }
        )
    return {"schema": "qr05-measure-divergence-report-v1", "rows": rows, "witnesses": witnesses}
