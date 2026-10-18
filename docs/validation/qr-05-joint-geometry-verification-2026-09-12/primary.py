"""Exact primary route for the fixed joint-geometry verification contract.

Polynomial coefficients are integrated by their antiderivatives. Chronology
uses signed slope inequalities. Joint identification is decided by grouping
observations on one common world class, never by separate parameter slices.
The pure public API performs no I/O, sampling, imports of local helpers, or
cached computation. Invalid public inputs raise ValueError without coercion.
"""

from fractions import Fraction
from itertools import combinations, product

RATIONAL_BITS = 128
CHANNEL_NAMES = ("O", "P", "T", "D", "R")
WORLD_FIELDS = ("kappa", "orientation", "a", "b", "L", "r")
SCHEMA = "qr05-joint-geometry-report-v1"


def _fields(value, names, label):
    if (
        type(value) is not dict
        or any(type(key) is not str for key in value)
        or set(value) != set(names)
    ):
        raise ValueError(f"{label} must be a plain dictionary with exactly {names}")


def _choice(value, choices, label):
    if type(value) is not int or value not in choices:
        raise ValueError(f"{label} must be a plain integer in {choices}")


def _fraction(value, label, *, positive=False, unit=False):
    if type(value) is not Fraction:
        raise ValueError(f"{label} must be a plain Fraction")
    if (
        value.numerator.bit_length() > RATIONAL_BITS
        or value.denominator.bit_length() > RATIONAL_BITS
    ):
        raise ValueError(f"{label} exceeds the rational input bit bound")
    if positive and value <= 0:
        raise ValueError(f"{label} must be positive")
    if unit and not 0 <= value <= 1:
        raise ValueError(f"{label} must lie in the closed unit interval")


def _validate_world(world):
    _fields(world, WORLD_FIELDS, "world")
    _choice(world["kappa"], (1, 2), "kappa")
    _choice(world["orientation"], (-1, 1), "orientation")
    _choice(world["a"], (0, 1), "a")
    _choice(world["b"], (0, 1), "b")
    _fraction(world["L"], "L", positive=True)
    _fraction(world["r"], "r", positive=True)


def _validate_point(point, label):
    if type(point) is not list or len(point) != 2:
        raise ValueError(f"{label} must be a two-coordinate plain list")
    for value in point:
        _fraction(value, label, unit=True)


def chronological(kappa, orientation, left, right):
    """Signed strict chronology; equal, null and spacelike pairs return zero."""
    _choice(kappa, (1, 2), "kappa")
    _choice(orientation, (-1, 1), "orientation")
    _validate_point(left, "left point")
    _validate_point(right, "right point")
    directed_time = orientation * (right[0] - left[0])
    spatial_threshold = kappa * abs(right[1] - left[1])
    if directed_time > spatial_threshold:
        return 1
    if directed_time < -spatial_threshold:
        return -1
    return 0


def _integral(coefficients, lower, upper):
    """Integrate an increasing-degree coefficient polynomial exactly."""
    result = Fraction(0)
    for degree, coefficient in enumerate(coefficients):
        exponent = degree + 1
        result += coefficient * (upper**exponent - lower**exponent) / exponent
    return result


def _construct(world):
    """Construct the forward row, excluding recovery to prevent recursion."""
    kappa, orientation = world["kappa"], world["orientation"]
    a, b, length_squared, rate = world["a"], world["b"], world["L"], world["r"]
    geometry = [kappa * length_squared, kappa * length_squared * a]
    sampling = [rate, rate * b]
    intensity = [Fraction(0), Fraction(0), Fraction(0)]
    for first, geometric_coefficient in enumerate(geometry):
        for second, sampling_coefficient in enumerate(sampling):
            intensity[first + second] += geometric_coefficient * sampling_coefficient

    zero, one, half = Fraction(0), Fraction(1), Fraction(1, 2)
    shape = [Fraction(1), Fraction(a + b), Fraction(a * b)]
    normalizer = _integral(shape, zero, one)
    total = _integral(intensity, zero, one)
    volume = _integral(geometry, zero, one)
    probes = [
        [Fraction(1, 8), Fraction(1, 8)],
        [Fraction(7, 8), Fraction(1, 8)],
        [Fraction(7, 8), Fraction(5, 8)],
    ]
    order = [
        chronological(kappa, orientation, probes[0], probes[1]),
        chronological(kappa, orientation, probes[0], probes[2]),
    ]
    channels = {
        "O": order,
        "P": _integral(intensity, zero, half) / total,
        "T": total,
        "D": b,
        "R": rate,
    }
    return {
        "world": {name: world[name] for name in WORLD_FIELDS},
        "channels": channels,
        "target": {
            "O": list(order),
            "relative_volume": _integral(geometry, zero, half) / volume,
            "volume": volume,
        },
        "geometry_coefficients": geometry,
        "intensity_coefficients": intensity,
        "point_density_coefficients": [value / total for value in intensity],
        "Z": normalizer,
        "fisher": [[total, total], [total, total]],
    }


def _validate_channels(channels):
    _fields(channels, CHANNEL_NAMES, "channels")
    order = channels["O"]
    if type(order) is not list or len(order) != 2:
        raise ValueError("O must be a two-integer plain list")
    if any(type(value) is not int for value in order):
        raise ValueError("O must contain only plain integers")
    if order not in ([-1, -1], [-1, 0], [1, 1], [1, 0]):
        raise ValueError("O is not a valid signed probe output")
    _fraction(channels["P"], "P")
    _fraction(channels["T"], "T", positive=True)
    _fraction(channels["R"], "R", positive=True)
    _choice(channels["D"], (0, 1), "D")
    if channels["P"] not in (Fraction(1, 2), Fraction(5, 12), Fraction(19, 56)):
        raise ValueError("P is outside the binary shape model")


def recover(channels):
    """Invert a complete population/reference tuple, refusing non-model images."""
    _validate_channels(channels)
    orientation = channels["O"][0]
    kappa = 1 if channels["O"][1] == orientation else 2
    shape_sum = {
        Fraction(1, 2): 0,
        Fraction(5, 12): 1,
        Fraction(19, 56): 2,
    }[channels["P"]]
    b = channels["D"]
    a = shape_sum - b
    _choice(a, (0, 1), "recovered a")
    normalizer = _integral(
        [Fraction(1), Fraction(a + b), Fraction(a * b)], Fraction(0), Fraction(1)
    )
    world = {
        "kappa": kappa,
        "orientation": orientation,
        "a": a,
        "b": b,
        "L": channels["T"] / (kappa * channels["R"] * normalizer),
        "r": channels["R"],
    }
    _validate_world(world)
    if _construct(world)["channels"] != channels:
        raise ValueError("channels do not round-trip through the model")
    return world


def evaluate(world):
    """Forward evaluation, including independently bounded inverse recovery.

    Individually bounded inputs may yield channels outside the public bound;
    such a world is refused when its generated channel tuple is recovered.
    """
    _validate_world(world)
    row = _construct(world)
    row["recovered"] = recover(row["channels"])
    return row


def _channel_key(value):
    return tuple(value) if type(value) is list else value


def _target_key(target):
    return (tuple(target["O"]), target["relative_volume"], target["volume"])


def _copy_target(target):
    return {
        "O": list(target["O"]),
        "relative_volume": target["relative_volume"],
        "volume": target["volume"],
    }


def _partition_row(worlds, selected):
    groups = {}
    for row in worlds:
        signature = tuple(_channel_key(row["channels"][name]) for name in selected)
        groups.setdefault(signature, []).append(row)
    blocks, block_targets = [], []
    for members in groups.values():
        blocks.append([row["id"] for row in members])
        targets, seen = [], set()
        for row in members:
            key = _target_key(row["target"])
            if key not in seen:
                seen.add(key)
                targets.append(_copy_target(row["target"]))
        block_targets.append(targets)
    return {
        "selected": list(selected),
        "blocks": blocks,
        "targets": block_targets,
        "identifying": all(len(targets) == 1 for targets in block_targets),
    }


def analyze():
    """Compute the complete fixed-catalogue report without external inputs."""
    domains = (
        (1, 2),
        (-1, 1),
        (0, 1),
        (0, 1),
        (Fraction(1), Fraction(3, 2)),
        (Fraction(1), Fraction(2, 3)),
    )
    worlds = []
    ids_by_world = {}
    for index, coordinates in enumerate(product(*domains)):
        world = dict(zip(WORLD_FIELDS, coordinates, strict=True))
        row = evaluate(world)
        row["id"] = f"w{index:03d}"
        worlds.append(row)
        ids_by_world[coordinates] = row["id"]

    partitions = []
    for size in range(len(CHANNEL_NAMES) + 1):
        for selected in combinations(CHANNEL_NAMES, size):
            partitions.append(_partition_row(worlds, selected))
    identifying_sets = [row["selected"] for row in partitions if row["identifying"]]
    minimal_sets = [
        list(selected)
        for selected in identifying_sets
        if not any(set(other) < set(selected) for other in identifying_sets)
    ]
    if identifying_sets:
        least = len(identifying_sets[0])
        minimum_size = [least]
        minimum_sets = [list(selected) for selected in identifying_sets if len(selected) == least]
    else:
        minimum_size, minimum_sets = [], []

    obstructions = []
    for left, right in combinations(worlds, 2):
        if _target_key(left["target"]) != _target_key(right["target"]):
            obstructions.append(
                {
                    "worlds": [left["id"], right["id"]],
                    "separators": [
                        name
                        for name in CHANNEL_NAMES
                        if left["channels"][name] != right["channels"][name]
                    ],
                }
            )

    one, three_halves, two_thirds = Fraction(1), Fraction(3, 2), Fraction(2, 3)

    def world_id(a, b, length_squared, rate, *, kappa=1, orientation=1):
        return ids_by_world[(kappa, orientation, a, b, length_squared, rate)]

    omission_witnesses = [
        {
            "omitted": "O",
            "worlds": [
                world_id(0, 0, one, one),
                world_id(0, 0, one, one, orientation=-1),
            ],
        },
        {
            "omitted": "P",
            "worlds": [world_id(0, 0, three_halves, one), world_id(1, 0, one, one)],
        },
        {
            "omitted": "T",
            "worlds": [world_id(0, 0, one, one), world_id(0, 0, three_halves, one)],
        },
        {
            "omitted": "D",
            "worlds": [world_id(1, 0, one, one), world_id(0, 1, one, one)],
        },
        {
            "omitted": "R",
            "worlds": [world_id(0, 0, one, one), world_id(0, 0, three_halves, two_thirds)],
        },
    ]
    collision_groups = []
    for kappa, orientation in product((1, 2), (-1, 1)):
        members = []
        for a, b in ((1, 0), (0, 1)):
            for length_squared, rate in ((one, one), (three_halves, two_thirds)):
                members.append(
                    world_id(a, b, length_squared, rate, kappa=kappa, orientation=orientation)
                )
        collision_groups.append({"kappa": kappa, "orientation": orientation, "worlds": members})

    return {
        "schema": SCHEMA,
        "channels": list(CHANNEL_NAMES),
        "worlds": worlds,
        "partitions": partitions,
        "minimal_identifying_sets": minimal_sets,
        "minimum_size": minimum_size,
        "minimum_identifying_sets": minimum_sets,
        "obstructions": obstructions,
        "omission_witnesses": omission_witnesses,
        "collision_groups": collision_groups,
    }
