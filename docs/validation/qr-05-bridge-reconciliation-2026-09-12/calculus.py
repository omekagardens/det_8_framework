"""Bounded exact channel quotients on one declared finite world class.

The packet is a mathematical table, not acquired apparatus data. All target
coordinates refer to the same rows. Identification means that the complete
target vector is constant on each observation fiber; separate familywise
identification is never substituted for this joint condition.

Only plain dictionaries, lists, strings and integers are accepted. Booleans
are not integers for this interface. Invalid inputs raise ValueError. The
functions do not mutate the packet and perform no I/O.
"""

from itertools import combinations

MAX_CHANNELS = 8
MAX_WORLDS = 64
MAX_TARGET_COORDINATES = 8


def _validate_packet(packet):
    if type(packet) is not dict or set(packet) != {"channels", "rows"}:
        raise ValueError("packet must be a plain dictionary with channels and rows")
    channels = packet["channels"]
    if type(channels) is not list or len(channels) > MAX_CHANNELS:
        raise ValueError("channels must be a plain list of at most eight names")
    if any(type(channel) is not str for channel in channels):
        raise ValueError("channel names must be plain strings")
    if len(set(channels)) != len(channels):
        raise ValueError("channel names must be unique")
    rows = packet["rows"]
    if type(rows) is not list or not 1 <= len(rows) <= MAX_WORLDS:
        raise ValueError("rows must be a nonempty plain list of at most 64 worlds")
    seen_ids = set()
    target_width = None
    for row in rows:
        if type(row) is not dict or set(row) != {"id", "observations", "target"}:
            raise ValueError("each row must have exactly id, observations and target")
        world_id = row["id"]
        if type(world_id) is not str or world_id in seen_ids:
            raise ValueError("world identifiers must be unique plain strings")
        seen_ids.add(world_id)
        observations = row["observations"]
        if type(observations) is not list or len(observations) != len(channels):
            raise ValueError("each observations list must have the channel width")
        if any(type(value) is not int for value in observations):
            raise ValueError("observations must contain only plain integers")
        target = row["target"]
        if type(target) is not list or not 1 <= len(target) <= MAX_TARGET_COORDINATES:
            raise ValueError("target must be a plain list of one to eight coordinates")
        if any(type(value) is not int for value in target):
            raise ValueError("target coordinates must be plain integers")
        if target_width is None:
            target_width = len(target)
        elif len(target) != target_width:
            raise ValueError("all rows must have the same target width")


def _selected_indices(packet, selected):
    if type(selected) is not list or len(selected) > MAX_CHANNELS:
        raise ValueError("selected must be a plain list of at most eight names")
    if any(type(channel) is not str for channel in selected):
        raise ValueError("selected names must be plain strings")
    if len(set(selected)) != len(selected):
        raise ValueError("selected names must be unique")
    by_name = {name: index for index, name in enumerate(packet["channels"])}
    if any(name not in by_name for name in selected):
        raise ValueError("selected names must belong to the packet's channel universe")
    return [by_name[name] for name in selected]


def _blocks(packet, indices):
    """Observation fibers, preserving first occurrence and within-fiber row order."""
    grouped = {}
    for row in packet["rows"]:
        signature = tuple(row["observations"][index] for index in indices)
        grouped.setdefault(signature, []).append(row["id"])
    return list(grouped.values())


def _constant_on_blocks(packet, blocks):
    targets = {row["id"]: row["target"] for row in packet["rows"]}
    return all(
        all(targets[world_id] == targets[block[0]] for world_id in block[1:]) for block in blocks
    )


def partition(packet, selected):
    """Return world-ID fibers of the selected channels in input row order."""
    _validate_packet(packet)
    indices = _selected_indices(packet, selected)
    return _blocks(packet, indices)


def identifying(packet, selected):
    """Whether the joint target vector is constant on every observation fiber."""
    _validate_packet(packet)
    indices = _selected_indices(packet, selected)
    return _constant_on_blocks(packet, _blocks(packet, indices))


def analyze(packet):
    """Enumerate the exact finite identification lattice and pair obstructions.

    Subsets are ordered by cardinality, then by input channel indices. The
    inclusion-minimal identifying sets need not all have minimum cardinality.
    An empty minimum_size means that no channel set identifies the target;
    [0] means that the empty channel set already identifies it.

    An obstruction lists every pair of different target vectors and all
    channels that distinguish that pair. In particular an empty separator
    list is retained: no subset can identify the target on that pair.
    """
    _validate_packet(packet)
    channels = packet["channels"]
    rows = packet["rows"]
    partitions = []
    identifying_indices = []
    for size in range(len(channels) + 1):
        for indices in combinations(range(len(channels)), size):
            blocks = _blocks(packet, indices)
            identifies = _constant_on_blocks(packet, blocks)
            partitions.append(
                {
                    "selected": [channels[index] for index in indices],
                    "blocks": blocks,
                    "identifying": identifies,
                }
            )
            if identifies:
                identifying_indices.append(indices)

    minimal_indices = [
        candidate
        for candidate in identifying_indices
        if not any(set(other) < set(candidate) for other in identifying_indices)
    ]
    if identifying_indices:
        least = len(identifying_indices[0])
        minimum_size = [least]
        minimum_indices = [indices for indices in identifying_indices if len(indices) == least]
    else:
        minimum_size = []
        minimum_indices = []

    obstructions = []
    for first, second in combinations(range(len(rows)), 2):
        left, right = rows[first], rows[second]
        if left["target"] != right["target"]:
            obstructions.append(
                {
                    "worlds": [left["id"], right["id"]],
                    "separators": [
                        channel
                        for index, channel in enumerate(channels)
                        if left["observations"][index] != right["observations"][index]
                    ],
                }
            )

    return {
        "channels": list(channels),
        "partitions": partitions,
        "minimal_identifying_sets": [
            [channels[index] for index in indices] for indices in minimal_indices
        ],
        "minimum_size": minimum_size,
        "minimum_identifying_sets": [
            [channels[index] for index in indices] for indices in minimum_indices
        ],
        "obstructions": obstructions,
    }
