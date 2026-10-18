"""Independent head-based renewal-port route; no external math imports."""

from fractions import Fraction


def validate(history):
    if type(history) not in (list, tuple) or len(history) > 4:
        raise ValueError("history must contain at most four births")
    seen = set()
    for item in history:
        if type(item) not in (list, tuple) or len(item) != 3:
            raise ValueError("a birth is (event id, action, bit)")
        event, action, bit = item
        if type(event) is not int or not 0 <= event < 1000 or event in seen:
            raise ValueError("event ids must be fresh bounded integers")
        if type(action) is not str or action not in ("a", "b", "ab"):
            raise ValueError("unknown action")
        if type(bit) is not int or bit not in (0, 1):
            raise ValueError("only positive binary branches may be committed")
        seen.add(event)


def permutation(action, setting):
    if type(action) is not str or action not in ("a", "b", "ab"):
        raise ValueError("unknown action")
    if type(setting) is not int or setting not in (0, 1):
        raise ValueError("setting is a bit")
    result = []
    for atom in range(9):
        i, j = divmod(atom, 3)
        if action == "a":
            i = i + 1 if setting == 0 else -i
        elif action == "b":
            j = j + 1 if setting == 0 else -j
        elif setting == 0:
            i, j = j, i
        else:
            j += i
        result.append(3 * (i % 3) + j % 3)
    return result


def _cells(perm):
    return [9 * perm[i] + perm[j] for i in range(9) for j in range(9)]


def evaluate(history):
    validate(history)
    heads = {}
    pasts = {}
    records = {}
    composed = list(range(9))
    for event, action, bit in history:
        past = set()
        for port in action:
            if port in heads:
                head = heads[port]
                past |= pasts[head] | {head}
        setting = bit ^ (sum(records[v][1] for v in past) % 2)
        perm = permutation(action, setting)
        composed = [perm[atom] for atom in composed]
        pasts[event] = past
        records[event] = (action, bit, setting)
        for port in action:
            heads[port] = event
    next_branches = []
    for action in ("a", "b", "ab"):
        past = set()
        for port in action:
            if port in heads:
                head = heads[port]
                past |= pasts[head] | {head}
        parity = sum(records[v][1] for v in past) % 2
        for bit in (0, 1, None):
            setting = None if bit is None else bit ^ parity
            next_branches.append(
                {
                    "action": action,
                    "outcome": bit,
                    "setting": setting,
                    "past": sorted(past),
                    "weight": Fraction(0 if bit is None else 1, 6),
                    "cell_map": [None] * 81
                    if bit is None
                    else _cells(permutation(action, setting)),
                    "committable": bit is not None,
                }
            )
    return {
        "events": sorted(records),
        "order": sorted([v, e] for e in records for v in pasts[e]),
        "records": [[e, *records[e]] for e in sorted(records)],
        "pasts": [[e, sorted(pasts[e])] for e in sorted(records)],
        "weight": Fraction(1, 6 ** len(history)),
        "cell_map": _cells(composed),
        "next": next_branches,
    }
