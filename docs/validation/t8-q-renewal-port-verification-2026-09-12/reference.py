"""Independent full-history and inverse-pullback matrix-unit route."""

from fractions import Fraction


def inverse(action, setting):
    if type(action) is not str or action not in ("a", "b", "ab"):
        raise ValueError("unknown action")
    if type(setting) is not int or setting not in (0, 1):
        raise ValueError("setting is a bit")
    preimage = []
    for output in range(9):
        first = output // 3
        second = output % 3
        if action == "a" and setting == 0:
            first -= 1
        elif action == "a":
            first = -first
        elif action == "b" and setting == 0:
            second -= 1
        elif action == "b":
            second = -second
        elif setting == 0:
            first, second = second, first
        else:
            second -= first
        preimage.append((first % 3) * 3 + second % 3)
    return preimage


def matrix_units(action, setting):
    preimage = inverse(action, setting)
    destinations = []
    for source in range(81):
        source_row, source_col = divmod(source, 9)
        destinations.append(9 * preimage.index(source_row) + preimage.index(source_col))
    return destinations


def evaluate(history):
    if type(history) not in (tuple, list) or len(history) > 4:
        raise ValueError("finite history required")
    births = []
    ids = []
    for item in history:
        if type(item) not in (tuple, list) or len(item) != 3:
            raise ValueError("invalid birth shape")
        event, action, outcome = item
        if type(event) is not int or event < 0 or event >= 1000 or event in ids:
            raise ValueError("invalid or reused identity")
        if type(action) is not str or action not in ("a", "b", "ab"):
            raise ValueError("invalid port subset")
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("a zero branch is not a birth")
        ids.append(event)
        births.append((event, action, outcome))
    relation = set()
    for later in range(len(births)):
        for earlier in range(later):
            if any(port in births[later][1] for port in births[earlier][1]):
                relation.add((births[earlier][0], births[later][0]))
    for middle in ids:
        for first in ids:
            for last in ids:
                if (first, middle) in relation and (middle, last) in relation:
                    relation.add((first, last))
    raw_bits = {event: outcome for event, _, outcome in births}
    settings = {}
    cells = list(range(81))
    for event, action, outcome in births:
        ancestors = {u for u, v in relation if v == event}
        setting = (outcome + sum(raw_bits[u] for u in ancestors)) % 2
        settings[event] = setting
        step = matrix_units(action, setting)
        cells = [step[destination] for destination in cells]
    next_branches = []
    for action in ("a", "b", "ab"):
        affected = {
            event for event, old_action, _ in births if any(port in old_action for port in action)
        }
        ancestors = affected | {u for u, v in relation if v in affected}
        for outcome in (0, 1, None):
            setting = (
                None if outcome is None else (outcome + sum(raw_bits[u] for u in ancestors)) % 2
            )
            next_branches.append(
                {
                    "action": action,
                    "outcome": outcome,
                    "setting": setting,
                    "past": sorted(ancestors),
                    "weight": Fraction(0) if outcome is None else Fraction(1, 6),
                    "cell_map": [None for _ in range(81)]
                    if outcome is None
                    else matrix_units(action, setting),
                    "committable": outcome is not None,
                }
            )
    return {
        "events": sorted(ids),
        "order": [list(pair) for pair in sorted(relation)],
        "records": sorted(
            [event, action, outcome, settings[event]] for event, action, outcome in births
        ),
        "pasts": [[event, sorted(u for u, v in relation if v == event)] for event in sorted(ids)],
        "weight": Fraction(1, 6) ** len(births),
        "cell_map": cells,
        "next": next_branches,
    }
