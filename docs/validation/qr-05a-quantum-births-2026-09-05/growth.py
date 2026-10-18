"""Exact three-birth quantum/record research executor; fixed shared qubit.

Directly applies Kraus operators to matrix units, independently of the
superoperator reference. No mutable DET, T8, or RET implementation imports.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from functools import cache
from itertools import permutations, product
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
BASE_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _load_exact():
    require(
        BASE_PATH.is_file() and not BASE_PATH.is_symlink(), "pinned source must be a plain file"
    )
    raw = BASE_PATH.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BASE_SHA, "QR-01 source identity differs")
    name = "qr05a_direct_exact"
    require(name not in sys.modules, "private exact module name collision")
    spec = importlib.util.spec_from_file_location(name, BASE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load pinned source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(BASE_PATH), "exec"), module.__dict__)  # noqa: S102
    return module


ex = _load_exact()
F = Fraction
RULES = ("weak_phase", "weak_dephase", "parity_zx", "stage_zx")


def parse(wire):
    ex._keys(wire, ("schema_version", "births", "growth", "instrument"))
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05a-problem-v1",
        "unsupported schema",
    )
    n = wire["births"]
    require(type(n) is int and 1 <= n <= 3, "birth count must be 1, 2, or 3")
    rule = wire["instrument"]
    require(type(rule) is str and rule in RULES, "unknown instrument family")
    growth = wire["growth"]
    require(type(growth) is dict, "growth must be an object")
    kind = growth.get("kind")
    require(type(kind) is str, "growth kind must be a string")
    if kind == "percolation":
        ex._keys(growth, ("kind", "p"))
        p = ex._fraction(growth["p"])
        require(0 <= p <= 1, "growth probability must lie in [0,1]")
    elif kind == "uniform_ideals":
        ex._keys(growth, ("kind",))
        p = None
    else:
        raise ValueError("unknown growth law")
    return n, kind, p, rule


@cache
def ideals(order):
    n = len(order)
    candidates = (tuple(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n))
    return tuple(sorted(s for s in candidates if all(set(order[i]) <= set(s) for i in s)))


@cache
def orders(n):
    if n == 0:
        return ((),)
    return tuple(sorted((*c, s) for c in orders(n - 1) for s in ideals(c)))


def growth_weight(kind, p, order, precursor):
    if kind == "uniform_ideals":
        return F(1, len(ideals(order)))
    maximal = sum(not any(i in order[j] for j in precursor) for i in precursor)
    return p**maximal * (1 - p) ** (len(order) - len(precursor))


def scoped_outcomes(order, record, precursor):
    require(len(order) == len(record), "parent record dimension differs")
    require(all(type(x) is int and x in (0, 1) for x in record), "records must be binary")
    require(precursor in ideals(order), "read set must be a precursor ideal")
    return tuple(record[i] for i in precursor)


@cache
def instrument(rule, stage, context):
    """Intrinsic rules see only this scoped tuple; stage rule is a negative control."""
    parity = sum(context) % 2
    if rule in ("weak_phase", "weak_dephase"):
        a, b = ex.q(F(3, 5)), ex.q(F(4, 5))
        phase = ex.q(0, 1) if parity else ex.ONE
        first = ((a, ex.ZERO), (ex.ZERO, phase * b))
        second = ((b, ex.ZERO), (ex.ZERO, phase * a))
        if rule == "weak_phase":
            setting, ops = f"weak{parity}", ((first,), (second,))
        else:
            z = ((ex.ONE, ex.ZERO), (ex.ZERO, ex.q(-1)))
            setting = f"dephase{parity}"
            ops = tuple((ex.scale(d, a), ex.scale(ex.mul(z, d), b)) for d in (first, second))
    else:
        use_x = stage % 2 if rule == "stage_zx" else parity
        if use_x:
            half = ex.q(F(1, 2))
            minus = ex.q(F(-1, 2))
            ops = ((((half, half), (half, half)),), (((half, minus), (minus, half)),))
            setting = "X"
        else:
            ops = (
                (((ex.ONE, ex.ZERO), (ex.ZERO, ex.ZERO)),),
                (((ex.ZERO, ex.ZERO), (ex.ZERO, ex.ONE)),),
            )
            setting = "Z"
    complete = ex.zeros(2)
    for group in ops:
        for m in group:
            complete = ex.add(complete, ex.mul(ex.dagger(m), m))
    require(complete == ex.identity(2), "fixed instrument is not complete")
    return setting, ops


def event_instrument(rule, order, record, precursor):
    context = () if rule == "stage_zx" else scoped_outcomes(order, record, precursor)
    return instrument(rule, len(order), context)


def apply_kraus(operators, state):
    result = ex.zeros(2)
    for m in operators:
        result = ex.add(result, ex.mul(ex.mul(m, state), ex.dagger(m)))
    return result


def direct_map(groups):
    columns = []
    for k, l in product(range(2), repeat=2):
        state = tuple(
            tuple(ex.ONE if (i, j) == (k, l) else ex.ZERO for j in range(2)) for i in range(2)
        )
        for group in groups:
            state = apply_kraus(group, state)
        columns.append(tuple(value for row in state for value in row))
    return tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))


def trace_preserving(matrix):
    return all(
        matrix[0][j] + matrix[3][j] == (ex.ONE if j in (0, 3) else ex.ZERO) for j in range(4)
    )


def history_map(kind, p, rule, order, record):
    groups, settings = [], []
    weight = F(1)
    for j, precursor in enumerate(order):
        parent = order[:j]
        setting, ops = event_instrument(rule, parent, record[:j], precursor)
        settings.append(setting)
        groups.append(ops[record[j]])
        weight *= growth_weight(kind, p, parent, precursor)
    return tuple(settings), weight, ex.scale(direct_map(groups), ex.q(weight))


def transported(order, record, permutation):
    inverse = {old: new for new, old in enumerate(permutation)}
    return (
        tuple(tuple(sorted(inverse[i] for i in order[old])) for old in permutation),
        tuple(record[old] for old in permutation),
    )


def linear_extensions(order):
    for perm in permutations(range(len(order))):
        positions = {old: new for new, old in enumerate(perm)}
        if all(positions[i] < positions[j] for j, past in enumerate(order) for i in past):
            yield perm


def class_key(order, record, settings):
    def key(perm):
        relation = "".join("1" if a in order[b] else "0" for a in perm for b in perm)
        marks = tuple((settings[i], record[i]) for i in perm)
        return relation, marks

    return min(key(perm) for perm in permutations(range(len(order))))


def order_wire(order):
    return [list(past) for past in order]


def analyze(wire):
    births, kind, p, rule = parse(wire)
    levels, internal_levels = [], []
    normalization, diamonds = [], []
    for n in range(births + 1):
        internal, rows = [], []
        total = ex.zeros(4)
        for order in orders(n):
            for record in product((0, 1), repeat=n):
                settings, weight, superop = history_map(kind, p, rule, order, record)
                internal.append((order, record, settings, weight, superop))
                rows.append(
                    {
                        "order": order_wire(order),
                        "outcomes": list(record),
                        "settings": list(settings),
                        "weight": str(weight),
                        "superoperator": ex.matrix_wire(superop),
                    }
                )
                total = ex.add(total, superop)
                if n < births:
                    growth_sum, birth_sum = F(0), ex.zeros(4)
                    for s in ideals(order):
                        q = growth_weight(kind, p, order, s)
                        growth_sum += q
                        _, operations = event_instrument(rule, order, record, s)
                        for group in operations:
                            birth_sum = ex.add(birth_sum, ex.scale(direct_map((group,)), ex.q(q)))
                    normalization.append(
                        {
                            "order": order_wire(order),
                            "outcomes": list(record),
                            "growth_sum": str(growth_sum),
                            "instrument_complete": True,
                            "birth_sum_trace_preserving": trace_preserving(birth_sum),
                        }
                    )
                if n <= births - 2:
                    for s, t in product(ideals(order), repeat=2):
                        qf = growth_weight(kind, p, order, s) * growth_weight(
                            kind, p, (*order, s), t
                        )
                        qr = growth_weight(kind, p, order, t) * growth_weight(
                            kind, p, (*order, t), s
                        )
                        branches, equal, weighted_equal = [], True, True
                        for x, y in product((0, 1), repeat=2):
                            sa, oa = event_instrument(rule, order, record, s)
                            sb, ob = event_instrument(rule, (*order, s), (*record, x), t)
                            tb, rb = event_instrument(rule, order, record, t)
                            ta, ra = event_instrument(rule, (*order, t), (*record, y), s)
                            forward = direct_map((oa[x], ob[y]))
                            reverse = direct_map((rb[y], ra[x]))
                            wf, wr = ex.scale(forward, ex.q(qf)), ex.scale(reverse, ex.q(qr))
                            labels_equal = (sa, sb) == (ta, tb)
                            equal &= labels_equal and forward == reverse
                            weighted_equal &= labels_equal and wf == wr
                            branches.append(
                                {
                                    "outcomes": [x, y],
                                    "forward_settings": [sa, sb],
                                    "reverse_settings": [ta, tb],
                                    "forward": ex.matrix_wire(forward),
                                    "reverse": ex.matrix_wire(reverse),
                                    "weighted_forward": ex.matrix_wire(wf),
                                    "weighted_reverse": ex.matrix_wire(wr),
                                }
                            )
                        diamonds.append(
                            {
                                "order": order_wire(order),
                                "outcomes": list(record),
                                "left_ideal": list(s),
                                "right_ideal": list(t),
                                "forward_weight": str(qf),
                                "reverse_weight": str(qr),
                                "unweighted_equal": equal,
                                "weighted_equal": weighted_equal,
                                "branches": branches,
                            }
                        )
        internal_levels.append(internal)
        levels.append(
            {
                "births": n,
                "histories": rows,
                "total_map": ex.matrix_wire(total),
                "trace_preserving": trace_preserving(total),
            }
        )

    terminal = internal_levels[-1]
    lookup = {(c, r): i for i, (c, r, _, _, _) in enumerate(terminal)}
    relabelings, groups = [], {}
    for index, (order, record, settings, _, matrix) in enumerate(terminal):
        for perm in linear_extensions(order):
            target = lookup[transported(order, record, perm)]
            expected = tuple(settings[i] for i in perm)
            settings_equal = expected == terminal[target][2]
            map_equal = matrix == terminal[target][4]
            relabelings.append(
                {
                    "history": index,
                    "permutation": list(perm),
                    "target": target,
                    "settings_expected": list(expected),
                    "settings_equal": settings_equal,
                    "map_equal": map_equal,
                    "equal": settings_equal and map_equal,
                }
            )
        key = class_key(order, record, settings)
        members, total = groups.get(key, ([], ex.zeros(4)))
        groups[key] = ([*members, index], ex.add(total, matrix))
    classes = [
        {
            "key": {"relation": key[0], "record": [list(mark) for mark in key[1]]},
            "members": members,
            "superoperator": ex.matrix_wire(total),
        }
        for key, (members, total) in sorted(groups.items())
    ]
    return {
        "levels": levels,
        "normalization": normalization,
        "diamonds": diamonds,
        "relabelings": relabelings,
        "classes": classes,
        "flags": {
            "normalized": all(row["trace_preserving"] for row in levels)
            and all(
                row["growth_sum"] == "1"
                and row["birth_sum_trace_preserving"]
                and row["instrument_complete"]
                for row in normalization
            ),
            "unweighted_diamonds_equal": all(row["unweighted_equal"] for row in diamonds),
            "weighted_diamonds_equal": all(row["weighted_equal"] for row in diamonds),
            "terminal_relabeling_equal": all(row["equal"] for row in relabelings),
        },
        "counts": {
            "level_histories": [len(rows) for rows in internal_levels],
            "normalization_rows": len(normalization),
            "diamond_contexts": len(diamonds),
            "diamond_outcome_pairs": 4 * len(diamonds),
            "terminal_relabelings": len(relabelings),
            "nonidentity_relabelings": sum(
                row["permutation"] != list(range(births)) for row in relabelings
            ),
            "terminal_classes": len(classes),
            "zero_terminal_maps": sum(row[4] == ex.zeros(4) for row in terminal),
        },
    }
