"""Independent exact geometry route: quadrature, quadratic cones, pair separators.

No source, protocol, primary engine or mathematical helper is imported. The
fixed census is generated here; public individual-world APIs additionally
admit bounded positive rational scales and density normalizations. Reference
channels are mathematical information, not acquired/calibrated instruments.
"""

from fractions import Fraction
from itertools import product

F = Fraction
INPUT_BITS = 128
CHANNEL_NAMES = ("O", "P", "T", "D", "R")
WORLD_KEYS = ("kappa", "orientation", "a", "b", "L", "r")


def _integer(value, choices, label):
    if type(value) is not int or value not in choices:
        raise ValueError(f"{label} must be a declared plain integer")


def _fraction(value, label, *, positive=False):
    if type(value) is not Fraction:
        raise ValueError(f"{label} must be a plain Fraction")
    if value.numerator.bit_length() > INPUT_BITS or value.denominator.bit_length() > INPUT_BITS:
        raise ValueError(f"{label} exceeds the rational bit bound")
    if positive and value <= 0:
        raise ValueError(f"{label} must be positive")


def _world(world):
    if (
        type(world) is not dict
        or any(type(key) is not str for key in world)
        or set(world) != set(WORLD_KEYS)
    ):
        raise ValueError("world must have exactly the six declared keys")
    _integer(world["kappa"], (1, 2), "kappa")
    _integer(world["orientation"], (-1, 1), "orientation")
    _integer(world["a"], (0, 1), "a")
    _integer(world["b"], (0, 1), "b")
    _fraction(world["L"], "L", positive=True)
    _fraction(world["r"], "r", positive=True)


def _channels(channels):
    if (
        type(channels) is not dict
        or any(type(key) is not str for key in channels)
        or set(channels) != set(CHANNEL_NAMES)
    ):
        raise ValueError("channels must have exactly O,P,T,D,R")
    order = channels["O"]
    if type(order) is not list or len(order) != 2:
        raise ValueError("O must be a two-entry plain list")
    if any(type(value) is not int for value in order):
        raise ValueError("O entries must be plain integers")
    if tuple(order) not in ((-1, -1), (-1, 0), (1, 1), (1, 0)):
        raise ValueError("O is outside the probe image")
    _fraction(channels["P"], "P")
    _fraction(channels["T"], "T", positive=True)
    _fraction(channels["R"], "R", positive=True)
    _integer(channels["D"], (0, 1), "D")
    if channels["P"] not in (F(1, 2), F(5, 12), F(19, 56)):
        raise ValueError("P is outside the normalized strip-probability image")


def _point(point):
    if type(point) is not list or len(point) != 2:
        raise ValueError("a point must be a two-coordinate plain list")
    for coordinate in point:
        _fraction(coordinate, "point coordinate")
        if not 0 <= coordinate <= 1:
            raise ValueError("point coordinates must lie in the closed unit square")


def chronological(kappa, orientation, left, right):
    """Strict chronology from the quadratic metric sign and time orientation."""
    _integer(kappa, (1, 2), "kappa")
    _integer(orientation, (-1, 1), "orientation")
    _point(left)
    _point(right)
    dt = right[0] - left[0]
    dx = right[1] - left[1]
    squared_interval = -dt * dt + kappa * kappa * dx * dx
    if squared_interval >= 0:
        return 0
    return orientation if dt > 0 else -orientation


def _simpson(function, left, right):
    """Exact on degree-two products; all nodes and weights are rational."""
    midpoint = (left + right) / 2
    return (right - left) * (function(left) + 4 * function(midpoint) + function(right)) / 6


def _trapezoid(function, left, right):
    """Exact on the affine proper-area density."""
    return (right - left) * (function(left) + function(right)) / 2


def _sampling(a, b):
    def density(x):
        return (1 + a * x) * (1 + b * x)

    zero, half, one = F(0), F(1, 2), F(1)
    total = _simpson(density, zero, one)
    strip = _simpson(density, zero, half)
    f0, fm, f1 = density(zero), density(half), density(one)
    # Recover the quadratic coefficients by interpolation, not integration
    # of the primary route's coefficient formula.
    quadratic = 2 * (f1 - 2 * fm + f0)
    linear = f1 - f0 - quadratic
    coefficients = [f0, linear, quadratic]
    return total, strip / total, coefficients


def _basic(world):
    """Forward model only: it never calls evaluate or recover."""
    kappa, orientation = world["kappa"], world["orientation"]
    a, b, scale, normalization = world["a"], world["b"], world["L"], world["r"]
    zero, half, one = F(0), F(1, 2), F(1)

    def proper_density(x):
        return kappa * scale * (1 + a * x)

    area = _trapezoid(proper_density, zero, one)
    left_area = _trapezoid(proper_density, zero, half)
    geometry = [proper_density(zero), proper_density(one) - proper_density(zero)]
    total, probability, product_coefficients = _sampling(a, b)
    amplitude = kappa * scale * normalization
    intensity = [amplitude * coefficient for coefficient in product_coefficients]
    point_density = [coefficient / total for coefficient in product_coefficients]
    mean_count = amplitude * total
    origin = [F(1, 8), F(1, 8)]
    vertical = [F(7, 8), F(1, 8)]
    diagonal = [F(7, 8), F(5, 8)]
    order = [
        chronological(kappa, orientation, origin, vertical),
        chronological(kappa, orientation, origin, diagonal),
    ]
    return {
        "channels": {"O": order, "P": probability, "T": mean_count, "D": b, "R": normalization},
        "target": {"O": list(order), "relative_volume": left_area / area, "volume": area},
        "geometry_coefficients": geometry,
        "intensity_coefficients": intensity,
        "point_density_coefficients": point_density,
        "Z": total,
        "fisher": [[mean_count, mean_count], [mean_count, mean_count]],
    }


def recover(channels):
    """Invert an admissible five-channel image, retaining the world bit bound."""
    _channels(channels)
    orientation = channels["O"][0]
    kappa = 2 if channels["O"][1] == 0 else 1
    b = channels["D"]
    possible = [a for a in (0, 1) if _sampling(a, b)[1] == channels["P"]]
    if len(possible) != 1:
        raise ValueError("P and D do not describe one admissible geometry shape")
    a = possible[0]
    total = _sampling(a, b)[0]
    world = {
        "kappa": kappa,
        "orientation": orientation,
        "a": a,
        "b": b,
        "L": channels["T"] / (kappa * channels["R"] * total),
        "r": channels["R"],
    }
    _world(world)
    if _basic(world)["channels"] != channels:
        raise ValueError("recovered world does not reproduce the channel image")
    return world


def evaluate(world):
    """Evaluate a world, refusing derived-channel overflow before recovery."""
    _world(world)
    result = _basic(world)
    _channels(result["channels"])
    result["world"] = {key: world[key] for key in WORLD_KEYS}
    result["recovered"] = recover(result["channels"])
    return result


def _target_copy(target):
    return {
        "O": list(target["O"]),
        "relative_volume": target["relative_volume"],
        "volume": target["volume"],
    }


def _fibers(worlds, selected):
    """Connected components of the exact observation-equivalence relation."""
    size = len(worlds)
    relation = [
        [
            all(left["channels"][key] == right["channels"][key] for key in selected)
            for right in worlds
        ]
        for left in worlds
    ]
    unseen = set(range(size))
    components = []
    while unseen:
        first = min(unseen)
        component = {first}
        pending = [first]
        while pending:
            current = pending.pop()
            for neighbor in sorted(unseen - component):
                if relation[current][neighbor]:
                    component.add(neighbor)
                    pending.append(neighbor)
        unseen -= component
        components.append(sorted(component))
    return components


def _menus():
    subsets = [
        [index for index in range(len(CHANNEL_NAMES)) if mask & (1 << index)]
        for mask in range(1 << len(CHANNEL_NAMES))
    ]
    subsets.sort(key=lambda subset: (len(subset), subset))
    return [[CHANNEL_NAMES[index] for index in subset] for subset in subsets]


def _world_tuple(world):
    return tuple(world[key] for key in WORLD_KEYS)


def _identifiers(worlds):
    return {_world_tuple(row["world"]): row["id"] for row in worlds}


def _omissions(worlds):
    lookup = _identifiers(worlds)
    one, large, inverse = F(1), F(3, 2), F(2, 3)
    base = (1, 1, 0, 0, one, one)
    pairs = [
        ("O", base, (1, -1, 0, 0, one, one)),
        ("P", (1, 1, 0, 0, large, one), (1, 1, 1, 0, one, one)),
        ("T", base, (1, 1, 0, 0, large, one)),
        ("D", (1, 1, 1, 0, one, one), (1, 1, 0, 1, one, one)),
        ("R", base, (1, 1, 0, 0, large, inverse)),
    ]
    by_id = {row["id"]: row for row in worlds}
    result = []
    for omitted, first, second in pairs:
        first_id, second_id = lookup[first], lookup[second]
        left, right = by_id[first_id], by_id[second_id]
        if left["target"] == right["target"]:
            raise ValueError("an omission witness has no geometric target difference")
        if any(
            left["channels"][key] != right["channels"][key]
            for key in CHANNEL_NAMES
            if key != omitted
        ):
            raise ValueError("an omission witness differs on a retained channel")
        result.append({"omitted": omitted, "worlds": [first_id, second_id]})
    return result


def _collisions(worlds):
    lookup = _identifiers(worlds)
    by_id = {row["id"]: row for row in worlds}
    groups = []
    for kappa, orientation in product((1, 2), (-1, 1)):
        identifiers = [
            lookup[(kappa, orientation, a, b, scale, normalization)]
            for a, b in ((1, 0), (0, 1))
            for scale, normalization in ((F(1), F(1)), (F(3, 2), F(2, 3)))
        ]
        members = [by_id[identifier] for identifier in identifiers]
        first = members[0]
        for member in members[1:]:
            for field in ("intensity_coefficients", "point_density_coefficients"):
                if member[field] != first[field]:
                    raise ValueError("a full-law collision has different density coefficients")
            if any(member["channels"][key] != first["channels"][key] for key in ("O", "P", "T")):
                raise ValueError("a full-law collision changes a retained record channel")
        if any(
            members[i]["target"] == members[j]["target"]
            for i in range(len(members))
            for j in range(i + 1, len(members))
        ):
            raise ValueError("a collision group repeats a geometric target")
        groups.append({"kappa": kappa, "orientation": orientation, "worlds": identifiers})
    return groups


def analyze():
    """Return the complete fixed census with pair-hitting identification logic."""
    worlds = []
    domain = product((1, 2), (-1, 1), (0, 1), (0, 1), (F(1), F(3, 2)), (F(1), F(2, 3)))
    for index, coordinates in enumerate(domain):
        row = evaluate(dict(zip(WORLD_KEYS, coordinates)))
        row["id"] = f"w{index:03d}"
        worlds.append(row)

    obstructions = []
    separator_sets = []
    for first in range(len(worlds)):
        for second in range(first + 1, len(worlds)):
            left, right = worlds[first], worlds[second]
            if left["target"] == right["target"]:
                continue
            separators = [
                key for key in CHANNEL_NAMES if left["channels"][key] != right["channels"][key]
            ]
            separator_sets.append(set(separators))
            obstructions.append({"worlds": [left["id"], right["id"]], "separators": separators})

    def hits(menu):
        selected = set(menu)
        return all(bool(selected & separators) for separators in separator_sets)

    menus = _menus()
    partitions = []
    for menu in menus:
        components = _fibers(worlds, menu)
        targets = []
        for component in components:
            distinct = []
            for index in component:
                target = worlds[index]["target"]
                if target not in distinct:
                    distinct.append(_target_copy(target))
            targets.append(distinct)
        identifies = hits(menu)
        if identifies != all(len(values) == 1 for values in targets):
            raise ValueError("pair separators and target-constant fibers disagree")
        partitions.append(
            {
                "selected": list(menu),
                "blocks": [
                    [worlds[index]["id"] for index in component] for component in components
                ],
                "targets": targets,
                "identifying": identifies,
            }
        )

    good = [menu for menu in menus if hits(menu)]
    minimal = [
        menu
        for menu in good
        if all(not hits([key for key in menu if key != removed]) for removed in menu)
    ]
    minimum_size = [len(good[0])] if good else []
    minimum = [list(menu) for menu in good if len(menu) == minimum_size[0]]
    return {
        "schema": "qr05-joint-geometry-report-v1",
        "channels": list(CHANNEL_NAMES),
        "worlds": worlds,
        "partitions": partitions,
        "minimal_identifying_sets": [list(menu) for menu in minimal],
        "minimum_size": minimum_size,
        "minimum_identifying_sets": minimum,
        "obstructions": obstructions,
        "omission_witnesses": _omissions(worlds),
        "collision_groups": _collisions(worlds),
    }
