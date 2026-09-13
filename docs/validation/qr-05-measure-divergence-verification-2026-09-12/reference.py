"""Independent exact neighbor-exchange reference for supplied graph measures."""

from fractions import Fraction


def _zero_vector(size):
    return [Fraction(0) for _ in range(size)]


def _zero_matrix(size):
    return [_zero_vector(size) for _ in range(size)]


def _diagonal(values):
    return [
        [values[i] if i == j else Fraction(0) for j in range(len(values))]
        for i in range(len(values))
    ]


def _sum(values):
    return sum(values, Fraction(0))


def _action(matrix, vector):
    return [_sum(entry * value for entry, value in zip(row, vector)) for row in matrix]


def _copy_world(world):
    return {
        "mu": world["mu"][:],
        "edges": [edge[:] for edge in world["edges"]],
        "k": world["k"][:],
        "x": world["x"][:],
        "mode": world["mode"],
        "I": world["I"][:],
        "D": world["D"][:],
        "f": world["f"][:],
        "g": world["g"][:],
        "q": world["q"][:],
    }


def _fraction_vector(value, length):
    if type(value) is not list or len(value) != length:
        raise ValueError("rational vector must be a plain list of the required length")
    for entry in value:
        if type(entry) is not Fraction:
            raise ValueError("rational entries must be plain Fractions")
        if abs(entry.numerator).bit_length() > 128 or entry.denominator.bit_length() > 128:
            raise ValueError("input rational exceeds the inclusive 128-bit bound")


def _labels(value, n):
    if type(value) is not list or len(value) > n:
        raise ValueError("node lists must be bounded plain lists")
    if any(type(label) is not int or not 0 <= label < n for label in value):
        raise ValueError("node labels must be plain ints in range")
    if len(set(value)) != len(value):
        raise ValueError("node lists cannot repeat labels")


def _validated_copy(world):
    keys = {"mu", "edges", "k", "x", "mode", "I", "D", "f", "g", "q"}
    if type(world) is not dict:
        raise ValueError("world must be a plain dict")
    if len(world) != len(keys) or any(type(key) is not str for key in world) or set(world) != keys:
        raise ValueError("world keys must match the declared schema exactly")
    if type(world["mu"]) is not list or not 1 <= len(world["mu"]) <= 3:
        raise ValueError("mu must describe one to three nodes")
    n = len(world["mu"])
    _fraction_vector(world["mu"], n)
    if any(value <= 0 for value in world["mu"]):
        raise ValueError("node measures must be positive")
    edges = world["edges"]
    if type(edges) is not list or len(edges) > n * (n - 1) // 2:
        raise ValueError("edges must be a bounded plain list")
    undirected = set()
    for edge in edges:
        if type(edge) is not list or len(edge) != 2:
            raise ValueError("an edge must be a plain two-element list")
        if any(type(node) is not int or not 0 <= node < n for node in edge):
            raise ValueError("edge labels must be plain ints in range")
        tail, head = edge
        if tail == head:
            raise ValueError("self-loops are forbidden")
        pair = (min(tail, head), max(tail, head))
        if pair in undirected:
            raise ValueError("undirected edges cannot be repeated")
        undirected.add(pair)
    _fraction_vector(world["k"], len(edges))
    if any(value < 0 for value in world["k"]):
        raise ValueError("edge conductances cannot be negative")
    _fraction_vector(world["x"], n)
    _fraction_vector(world["q"], n)
    if type(world["mode"]) is not str or world["mode"] not in (
        "closed",
        "flux",
        "dirichlet",
    ):
        raise ValueError("mode must be a declared plain string")
    _labels(world["I"], n)
    _labels(world["D"], n)
    if set(world["I"]) & set(world["D"]) or set(world["I"] + world["D"]) != set(range(n)):
        raise ValueError("I and D must partition all nodes")
    _fraction_vector(world["f"], len(world["I"]))
    _fraction_vector(world["g"], len(world["D"]))
    if world["mode"] == "dirichlet":
        if not world["I"] or not world["D"]:
            raise ValueError("Dirichlet mode needs dynamic and held nodes")
        if any(world["q"]):
            raise ValueError("Dirichlet mode cannot add prescribed exterior flux")
    else:
        if world["I"] != list(range(n)) or world["D"] or world["g"]:
            raise ValueError("closed and flux modes require canonical full-node I")
        if world["mode"] == "closed" and any(world["q"]):
            raise ValueError("closed mode requires zero exterior flux")
    return _copy_world(world)


def _exchange_matrices(world):
    """Build each neighbor's gain and loss directly; incidence is only reported."""
    mu = world["mu"]
    n = len(mu)
    laplacian, operator = _zero_matrix(n), _zero_matrix(n)
    incidence = []
    for (tail, head), conductance in zip(world["edges"], world["k"]):
        row = _zero_vector(n)
        row[tail], row[head] = Fraction(-1), Fraction(1)
        incidence.append(row)
        for receiving, neighbor in ((tail, head), (head, tail)):
            laplacian[receiving][receiving] += conductance
            laplacian[receiving][neighbor] -= conductance
            rate = conductance / mu[receiving]
            operator[receiving][neighbor] += rate
            operator[receiving][receiving] -= rate
    return incidence, laplacian, operator


def _moments(operator, coordinates):
    m0, m1, m2 = [], [], []
    for i, row in enumerate(operator):
        m0.append(_sum(row))
        m1.append(_sum(value * (coordinates[j] - coordinates[i]) for j, value in enumerate(row)))
        m2.append(
            _sum(value * (coordinates[j] - coordinates[i]) ** 2 for j, value in enumerate(row)) / 2
        )
    return {
        "m0": m0,
        "m1": m1,
        "m2": m2,
        "Q1": _action(operator, [Fraction(1) for _ in coordinates]),
        "Qx": _action(operator, coordinates),
        "Qx2": _action(operator, [value**2 for value in coordinates]),
    }


def _adjoint_residual(operator, measures):
    return [
        [measures[i] * operator[i][j] - measures[j] * operator[j][i] for j in range(len(measures))]
        for i in range(len(measures))
    ]


def _components(operator, nodes):
    """Connected sets from positive operator entries, independent of coordinates."""
    ordered = sorted(nodes)
    unseen = set(ordered)
    components = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        found = [seed]
        pending = [seed]
        while pending:
            current = pending.pop()
            for neighbor in ordered:
                if neighbor in unseen and operator[current][neighbor] > 0:
                    unseen.remove(neighbor)
                    pending.append(neighbor)
                    found.append(neighbor)
        components.append(sorted(found))
    return components


def _indicators(components, coordinates):
    return [[Fraction(int(node in component)) for node in coordinates] for component in components]


def _reconstruction(operator, components, world):
    """First reconstruct using Q alone, then compare against supplied inputs."""
    n = len(operator)
    normalized = _zero_vector(n)
    anchor_of = [0 for _ in range(n)]
    for component in components:
        anchor = component[0]
        normalized[anchor] = Fraction(1)
        known = {anchor}
        pending = [anchor]
        while pending:
            current = pending.pop()
            for neighbor in component:
                if neighbor not in known and operator[current][neighbor] > 0:
                    normalized[neighbor] = (
                        normalized[current]
                        * operator[current][neighbor]
                        / operator[neighbor][current]
                    )
                    known.add(neighbor)
                    pending.append(neighbor)
        for node in component:
            anchor_of[node] = anchor
    conductances = [normalized[tail] * operator[tail][head] for tail, head in world["edges"]]
    detailed = [
        [normalized[i] * operator[i][j] - normalized[j] * operator[j][i] for j in range(n)]
        for i in range(n)
    ]
    measures = world["mu"]
    return {
        "mu_normalized": normalized,
        "k_normalized": conductances,
        "detailed_balance": detailed,
        "mu_residual": [normalized[i] - measures[i] / measures[anchor_of[i]] for i in range(n)],
        "k_residual": [
            conductances[index] - world["k"][index] / measures[anchor_of[tail]]
            for index, (tail, _) in enumerate(world["edges"])
        ],
    }


def _field_and_flux(world, operator):
    field = _zero_vector(len(world["mu"]))
    for node, value in zip(world["I"], world["f"]):
        field[node] = value
    for node, value in zip(world["D"], world["g"]):
        field[node] = value
    gradient, edge_flux = [], []
    influx = _zero_vector(len(field))
    outward = _zero_vector(len(world["I"]))
    active = {node: index for index, node in enumerate(world["I"])}
    held = set(world["D"])
    for (tail, head), conductance in zip(world["edges"], world["k"]):
        difference = field[head] - field[tail]
        current = -conductance * difference
        gradient.append(difference)
        edge_flux.append(current)
        influx[tail] -= current
        influx[head] += current
        if tail in active and head in held:
            outward[active[tail]] += conductance * (field[tail] - field[head])
        if head in active and tail in held:
            outward[active[head]] += conductance * (field[head] - field[tail])
    return {
        "field": field,
        "gradient": gradient,
        "J": edge_flux,
        "influx": influx,
        "Qf": _action(operator, field),
        "dirichlet_outward": outward,
    }


def _reduced(world, operator, flux):
    nodes = world["I"]
    measures = [world["mu"][node] for node in nodes]
    block = [[operator[i][j] for j in nodes] for i in nodes]
    source = [-world["q"][node] / world["mu"][node] for node in nodes]
    active = {node: index for index, node in enumerate(nodes)}
    held = set(world["D"])
    for (tail, head), conductance in zip(world["edges"], world["k"]):
        if tail in active and head in held:
            source[active[tail]] += conductance * flux["field"][head] / world["mu"][tail]
        if head in active and tail in held:
            source[active[head]] += conductance * flux["field"][tail] / world["mu"][head]
    components = _components(operator, nodes)
    anchored = [
        any(operator[node][boundary] > 0 for node in component for boundary in world["D"])
        for component in components
    ]
    kernel = _indicators(
        [component for component, attached in zip(components, anchored) if not attached], nodes
    )
    report = _moments(block, [world["x"][node] for node in nodes])
    report.update(
        {
            "nodes": nodes[:],
            "W": _diagonal(measures),
            "Q": block,
            "adjoint_residual": _adjoint_residual(block, measures),
            "source": source,
            "fdot": [
                (flux["influx"][node] - world["q"][node]) / world["mu"][node] for node in nodes
            ],
            "constant_balance": [
                _sum(operator[node][j] for j in nodes)
                + _sum(operator[node][a] for a in world["D"])
                - world["q"][node] / world["mu"][node]
                for node in nodes
            ],
            "components": components,
            "anchored": anchored,
            "kernel_basis": kernel,
            "kernel_images": [_action(block, vector) for vector in kernel],
            "invertible": all(anchored),
        }
    )
    return report


def _balances(world, flux, reduced):
    nodes = world["I"]
    dynamic = set(nodes)
    measures = world["mu"]
    field = flux["field"]
    derivative = reduced["fdot"]
    internal = _sum(
        conductance * (field[tail] - field[head]) ** 2
        for (tail, head), conductance in zip(world["edges"], world["k"])
        if tail in dynamic and head in dynamic
    )
    external = _sum(field[node] * world["q"][node] for node in nodes)
    reservoir = _sum(
        field[node] * outward for node, outward in zip(nodes, flux["dirichlet_outward"])
    )
    return {
        "mass": _sum(measures[node] * field[node] for node in nodes),
        "energy": _sum(measures[node] * field[node] ** 2 for node in nodes) / 2,
        "mass_rate": _sum(measures[node] * rate for node, rate in zip(nodes, derivative)),
        "energy_rate": _sum(
            measures[node] * field[node] * rate for node, rate in zip(nodes, derivative)
        ),
        "mass_rhs": -_sum(world["q"][node] for node in nodes) - _sum(flux["dirichlet_outward"]),
        "energy_rhs": -internal - external - reservoir,
        "internal_dissipation": internal,
        "external_work": external,
        "reservoir_work": reservoir,
        "ordinary_rate": _sum(derivative),
    }


def evaluate(world):
    """Validate one finite world and return all exact native report objects."""
    copied = _validated_copy(world)
    incidence, laplacian, operator = _exchange_matrices(copied)
    measures = copied["mu"]
    n = len(measures)
    full = _moments(operator, copied["x"])
    full.update(
        {
            "counting_columns": [_sum(operator[i][j] for i in range(n)) for j in range(n)],
            "weighted_columns": [
                _sum(measures[i] * operator[i][j] for i in range(n)) for j in range(n)
            ],
            "adjoint_residual": _adjoint_residual(operator, measures),
            "energy_form": [[-measures[i] * operator[i][j] for j in range(n)] for i in range(n)],
        }
    )
    components = _components(operator, list(range(n)))
    kernel = _indicators(components, list(range(n)))
    flux = _field_and_flux(copied, operator)
    reduced = _reduced(copied, operator, flux)
    return {
        "world": copied,
        "B": incidence,
        "W": _diagonal(measures),
        "K": _diagonal(copied["k"]),
        "L": laplacian,
        "Q": operator,
        "full": full,
        "flux": flux,
        "components": components,
        "kernel_basis": kernel,
        "kernel_images": [_action(operator, vector) for vector in kernel],
        "reconstruction": _reconstruction(operator, components, copied),
        "reduced": reduced,
        "balances": _balances(copied, flux, reduced),
    }


def _base_worlds():
    """Independent literal fixture construction; these are not API coercions."""
    specifications = (
        ("singleton_closed", (1,), (), (), (0,), "closed", (0,), (), (2,), (), (0,)),
        (
            "unequal_closed",
            (1, 2),
            ((0, 1),),
            (1,),
            (0, 1),
            "closed",
            (0, 1),
            (),
            (0, 1),
            (),
            (0, 0),
        ),
        (
            "zero_edge_closed",
            (1, 2, 1),
            ((0, 1), (1, 2)),
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
            ((0, 1), (1, 2)),
            (Fraction(3, 2), 1),
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
            (Fraction(1, 2), 1, 1),
            ((0, 1), (1, 2)),
            (1, 1),
            (-1, 0, 1),
            "closed",
            (0, 1, 2),
            (),
            (0, 1, 0),
            (),
            (0, 0, 0),
        ),
        (
            "prescribed_flux",
            (1, 2),
            ((0, 1),),
            (1,),
            (0, 1),
            "flux",
            (0, 1),
            (),
            (1, 2),
            (),
            (2, -2),
        ),
        (
            "dirichlet_grounded",
            (1, 1, 1),
            ((0, 1), (1, 2)),
            (Fraction(3, 2), 1),
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
            ((0, 1), (1, 2)),
            (Fraction(3, 2), 1),
            (-1, 0, 1),
            "dirichlet",
            (1,),
            (0, 2),
            (Fraction(1, 2),),
            (1, 1),
            (0, 0, 0),
        ),
        (
            "dirichlet_unanchored",
            (1, 2, 1),
            ((0, 1), (1, 2)),
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
    worlds = []
    for name, mu, edges, k, x, mode, active, held, f, g, q in specifications:
        world = {
            "mu": [Fraction(value) for value in mu],
            "edges": [list(edge) for edge in edges],
            "k": [Fraction(value) for value in k],
            "x": [Fraction(value) for value in x],
            "mode": mode,
            "I": list(active),
            "D": list(held),
            "f": [Fraction(value) for value in f],
            "g": [Fraction(value) for value in g],
            "q": [Fraction(value) for value in q],
        }
        worlds.append((name, world))
    return worlds


def _transform(world, variant):
    transformed = _copy_world(world)
    if variant == "identity":
        return transformed
    if variant == "reversal":
        transformed["edges"] = [[head, tail] for tail, head in world["edges"]]
        return transformed
    if variant == "rescale":
        for key in ("mu", "k", "q"):
            transformed[key] = [Fraction(3, 2) * value for value in world[key]]
        return transformed
    if variant == "cyclic":
        n = len(world["mu"])
        for key in ("mu", "x", "q"):
            transformed[key] = _zero_vector(n)
            for old, value in enumerate(world[key]):
                transformed[key][(old + 1) % n] = value
        transformed["edges"] = [[(tail + 1) % n, (head + 1) % n] for tail, head in world["edges"]]
        if world["mode"] == "dirichlet":
            transformed["I"] = [(node + 1) % n for node in world["I"]]
            transformed["D"] = [(node + 1) % n for node in world["D"]]
        else:
            transformed["f"] = _zero_vector(n)
            for old, value in enumerate(world["f"]):
                transformed["f"][(old + 1) % n] = value
        return transformed
    raise ValueError("unknown fixed variant")


def analyze():
    """Construct just the fixed 36 rows and nine same-operator scale witnesses."""
    variants = ("identity", "cyclic", "reversal", "rescale")
    rows, witnesses = [], []
    for base, world in _base_worlds():
        base_rows = {}
        for variant in variants:
            row = evaluate(_transform(world, variant))
            row.update({"id": base + ":" + variant, "base": base, "variant": variant})
            rows.append(row)
            base_rows[variant] = row
        original, scaled = base_rows["identity"], base_rows["rescale"]
        if original["Q"] != scaled["Q"]:
            raise ValueError("declared scale witness has unequal operators")
        if original["world"]["mu"] == scaled["world"]["mu"]:
            raise ValueError("declared scale witness has equal measures")
        witnesses.append(
            {
                "base": base,
                "rows": [base + ":identity", base + ":rescale"],
                "Q": [row[:] for row in original["Q"]],
                "measures": [original["world"]["mu"][:], scaled["world"]["mu"][:]],
                "conductances": [original["world"]["k"][:], scaled["world"]["k"][:]],
            }
        )
    return {"schema": "qr05-measure-divergence-report-v1", "rows": rows, "witnesses": witnesses}
