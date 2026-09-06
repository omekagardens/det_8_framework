"""Finite CQ quotient dynamics, using direct exact Kraus action on matrix units."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as F
from functools import cache
from itertools import pairwise, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXACT = HERE.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
EXACT_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"
CASES = (
    "weak_phase",
    "grouped_dephase",
    "zero_link_boundary",
    "chain_boundary",
    "normalized_noncovariant_growth",
)
SUMMARIES = ("marked_order", "shape_ones", "link_counts_ones", "size_ones")
BLOCH = ((F(0), F(0), F(0)), (F(1, 2), F(0), F(0)), (F(0), F(1, 2), F(0)), (F(0), F(0), F(1, 2)))
EFFECT_NAMES = ("P0", "P1", "P+X", "P+Y")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_exact():
    require(EXACT.is_file() and not EXACT.is_symlink(), "arithmetic source must be a plain file")
    raw = EXACT.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXACT_SHA, "pinned arithmetic identity differs")
    name = "qr05c_direct_exact"
    require(name not in sys.modules, "private arithmetic module collision")
    spec = importlib.util.spec_from_file_location(name, EXACT)
    require(spec is not None and spec.loader is not None, "cannot load arithmetic")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(EXACT), "exec"), module.__dict__)  # noqa: S102
    return module


ex = load_exact()
ZERO = (ex.ZERO,) * 4
IDENTITY = (ex.ONE,) * 4


def parse(wire):
    ex._keys(wire, ("schema_version", "case"))
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05c-problem-v1",
        "unsupported schema",
    )
    require(type(wire["case"]) is str and wire["case"] in CASES, "unknown fixed case")
    name = wire["case"]
    rule = "weak_dephase" if name == "grouped_dephase" else "weak_phase"
    p = F(0) if name == "zero_link_boundary" else F(1) if name == "chain_boundary" else F(2, 5)
    return name, rule, p, name == "normalized_noncovariant_growth"


@cache
def ideals(order):
    n = len(order)
    subsets = (tuple(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n))
    return tuple(sorted(s for s in subsets if all(set(order[i]) <= set(s) for i in s)))


@cache
def orders(n):
    return ((),) if n == 0 else tuple(sorted((*c, s) for c in orders(n - 1) for s in ideals(c)))


def maximal(order, subset):
    return sum(not any(i in order[j] for j in subset) for i in subset)


def growth_weight(order, precursor, p, uniform):
    if uniform:
        return F(1, len(ideals(order)))
    return p ** maximal(order, precursor) * (1 - p) ** (len(order) - len(precursor))


def setting(rule, parity):
    return ("dephase" if rule == "weak_dephase" else "weak") + str(parity)


def settings(rule, order, record):
    return tuple(setting(rule, sum(record[i] for i in past) % 2) for past in order)


@cache
def kernel(rule, parity, outcome, weight):
    a, b = (F(3, 5), F(4, 5)) if outcome == 0 else (F(4, 5), F(3, 5))
    phase = ex.q(0, 1) if parity else ex.ONE
    d = ((ex.q(a), ex.ZERO), (ex.ZERO, ex.q(b) * phase))
    if rule == "weak_phase":
        operators = (d,)
    else:
        z = ((ex.ONE, ex.ZERO), (ex.ZERO, ex.q(-1)))
        operators = (ex.scale(d, ex.q(F(3, 5))), ex.scale(ex.mul(z, d), ex.q(F(4, 5))))
    columns = []
    for index in range(4):
        unit = tuple(
            tuple(ex.ONE if 2 * i + j == index else ex.ZERO for j in range(2)) for i in range(2)
        )
        result = ex.zeros(2)
        for operator in operators:
            result = ex.add(result, ex.mul(ex.mul(operator, unit), ex.dagger(operator)))
        columns.append(tuple(v for row in result for v in row))
    require(
        all(columns[j][i] == ex.ZERO for i in range(4) for j in range(4) if i != j),
        "kernel not diagonal",
    )
    return tuple(ex.q(weight) * columns[i][i] for i in range(4))


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def summed(maps):
    result = ZERO
    for item in maps:
        result = plus(result, item)
    return result


def compose(after, before):
    return tuple(a * b for a, b in zip(after, before, strict=True))


def trace_preserving(row):
    total = summed(row)
    return total[0] == total[3] == ex.ONE


def state(vector):
    x, y, z = map(F, vector)
    return ((ex.q((1 + z) / 2), ex.q(x / 2, -y / 2)), (ex.q(x / 2, y / 2), ex.q((1 - z) / 2)))


EFFECTS = (state((0, 0, 1)), state((0, 0, -1)), state((1, 0, 0)), state((0, 1, 0)))


def apply_map(diagonal, rho):
    return tuple(tuple(diagonal[2 * i + j] * rho[i][j] for j in range(2)) for i in range(2))


def probability(diagonal, rho, effect=None):
    result = apply_map(diagonal, rho)
    value = ex.trace(result if effect is None else ex.mul(effect, result))
    require(value.imag == 0 and value.real >= 0, "invalid physical probability")
    return value.real


class MapValue:
    def __init__(self, value):
        self.value = value


def pack(data):
    values = {ZERO}

    def visit(item):
        if isinstance(item, MapValue):
            values.add(item.value)
        elif isinstance(item, dict):
            for value in item.values():
                visit(value)
        elif isinstance(item, (list, tuple)):
            for value in item:
                visit(value)

    visit(data)
    bank = [
        ZERO,
        *sorted(values - {ZERO}, key=lambda d: tuple(token for v in d for token in v.wire())),
    ]
    lookup = {value: i for i, value in enumerate(bank)}

    def encode(item):
        if isinstance(item, MapValue):
            return lookup[item.value]
        if isinstance(item, dict):
            return {key: encode(value) for key, value in item.items()}
        if isinstance(item, (list, tuple)):
            return [encode(value) for value in item]
        return item

    result = encode(data)
    result["map_bank"] = [[v.wire() for v in diagonal] for diagonal in bank]
    result["counts"]["map_bank_entries"] = len(bank)
    return result


def build_fine(rule, p, uniform):
    levels, lookups, sources, steps = [], [], [], []
    for n in range(5):
        history = [
            (c, r, settings(rule, c, r)) for c in orders(n) for r in product((0, 1), repeat=n)
        ]
        levels.append(history)
        lookups.append({(c, r): i for i, (c, r, _) in enumerate(history)})
        sources.append([ZERO] * len(history))
    sources[0][0] = IDENTITY
    for n in range(4):
        rows, seen = [], set()
        for parent, (c, r, _) in enumerate(levels[n]):
            edges = []
            for s in ideals(c):
                q = growth_weight(c, s, p, uniform)
                b = sum(r[i] for i in s) % 2
                for x in range(2):
                    child = lookups[n + 1][((*c, s), (*r, x))]
                    require(child not in seen, "duplicate natural birth path")
                    seen.add(child)
                    k = kernel(rule, b, x, q)
                    sources[n + 1][child] = compose(k, sources[n][parent])
                    edges.append(
                        {
                            "target": child,
                            "precursor": list(s),
                            "growth_weight": str(q),
                            "setting": setting(rule, b),
                            "outcome": x,
                            "kernel": k,
                        }
                    )
            require(
                trace_preserving([edge["kernel"] for edge in edges]),
                "fine birth row not normalized",
            )
            rows.append(edges)
        require(len(seen) == len(levels[n + 1]), "missing natural history")
        steps.append(rows)
    return levels, sources, steps


def summary_key(name, history):
    c, r, marks = history
    n, ones = len(c), sum(r)
    if name in ("marked_order", "shape_ones"):
        options = [
            (
                "".join("1" if i in c[j] else "0" for i in perm for j in perm),
                tuple((marks[i], r[i]) for i in perm),
            )
            for perm in permutations(range(n))
        ]
        if name == "marked_order":
            rel, record = min(options)
            return {"relation": rel, "marks": [list(v) for v in record]}
        return {"relation": min(rel for rel, _ in options), "ones": ones}
    if name == "link_counts_ones":
        return {
            "n": n,
            "links": sum(maximal(c, past) for past in c),
            "incomparable": n * (n - 1) // 2 - sum(map(len, c)),
            "ones": ones,
        }
    return {"n": n, "ones": ones}


def partition(name, histories):
    table = {}
    for i, history in enumerate(histories):
        key = summary_key(name, history)
        encoded = json.dumps(key, sort_keys=True)
        if encoded not in table:
            table[encoded] = {"key": key, "members": []}
        table[encoded]["members"].append(i)
    return sorted(table.values(), key=lambda group: group["members"][0])


def class_lookup(groups):
    return {member: index for index, group in enumerate(groups) for member in group["members"]}


def physical_witness(conflict, actual, proposed):
    target = conflict["targets"][0]
    for bloch in BLOCH:
        rho = state(bloch)
        for label, effect in zip(EFFECT_NAMES, EFFECTS, strict=True):
            a, b = (
                probability(actual[target], rho, effect),
                probability(proposed[target], rho, effect),
            )
            if a != b:
                return {
                    "history": conflict["history"],
                    "representative": conflict["representative"],
                    "target": target,
                    "input_bloch": [str(v) for v in bloch],
                    "effect": label,
                    "actual_probability": str(a),
                    "proposed_probability": str(b),
                }
    raise ValueError("spanning physical witness bank missed discrepancy")


def compare(n, partitions, actual_rows, representative_rows, sources):
    lookup = class_lookup(partitions[n])
    conflicts, source_equal = [], True
    for h, actual in enumerate(actual_rows):
        g = lookup[h]
        proposed = representative_rows[g]
        targets = [i for i, (a, b) in enumerate(zip(actual, proposed, strict=True)) if a != b]
        if targets:
            conflicts.append(
                {"history": h, "representative": partitions[n][g]["members"][0], "targets": targets}
            )
        if any(
            compose(a, sources[n][h]) != compose(b, sources[n][h])
            for a, b in zip(actual, proposed, strict=True)
        ):
            source_equal = False
    first = conflicts[0] if conflicts else None
    witness = (
        physical_witness(
            first, actual_rows[first["history"]], representative_rows[lookup[first["history"]]]
        )
        if first
        else None
    )
    return {
        "births": n,
        "actual_rows": actual_rows,
        "representative_rows": representative_rows,
        "consistent": not conflicts,
        "all_fixed_source_branches_equal": source_equal,
        "conflicts": conflicts,
        "first_witness": witness,
    }


def quotient(name, levels, sources, fine_steps):
    partitions = [partition(name, histories) for histories in levels]
    steps, two = [], []
    for n in range(4):
        target_classes = class_lookup(partitions[n + 1])
        actual = []
        for edges in fine_steps[n]:
            row = [ZERO] * len(partitions[n + 1])
            for edge in edges:
                target = target_classes[edge["target"]]
                row[target] = plus(row[target], edge["kernel"])
            require(trace_preserving(row), "coarse actual row not normalized")
            actual.append(row)
        reps = [actual[group["members"][0]] for group in partitions[n]]
        steps.append(compare(n, partitions, actual, reps, sources))
    for n in range(3):
        target_classes = class_lookup(partitions[n + 2])
        actual = []
        for first_edges in fine_steps[n]:
            row = [ZERO] * len(partitions[n + 2])
            for first in first_edges:
                for second in fine_steps[n + 1][first["target"]]:
                    target = target_classes[second["target"]]
                    row[target] = plus(row[target], compose(second["kernel"], first["kernel"]))
            require(trace_preserving(row), "fine two-step row not normalized")
            actual.append(row)
        proposed = []
        for first_row in steps[n]["representative_rows"]:
            row = [ZERO] * len(partitions[n + 2])
            for middle, first in enumerate(first_row):
                if first == ZERO:
                    continue
                for target, second in enumerate(steps[n + 1]["representative_rows"][middle]):
                    if second != ZERO:
                        row[target] = plus(row[target], compose(second, first))
            require(trace_preserving(row), "trial coarse two-step row not normalized")
            proposed.append(row)
        two.append(compare(n, partitions, actual, proposed, sources))
    return {"name": name, "partitions": partitions, "steps": steps, "two_steps": two}


def refinements(quotients):
    result = []
    for fine, coarse in pairwise(quotients):
        levels = []
        for n in range(5):
            lookup = class_lookup(coarse["partitions"][n])
            sets = [{lookup[h] for h in group["members"]} for group in fine["partitions"][n]]
            valid = all(len(s) == 1 for s in sets)
            require(valid, "not a nested partition family")
            levels.append(
                {"births": n, "parent_classes": [next(iter(s)) for s in sets], "valid": valid}
            )
        result.append({"fine": fine["name"], "coarse": coarse["name"], "levels": levels})
    return result


def source_covariance(partitions, sources):
    result = []
    for n, groups in enumerate(partitions):
        conflicts = sorted(
            [group["members"][0], h]
            for group in groups
            for h in group["members"]
            if sources[n][h] != sources[n][group["members"][0]]
        )
        result.append({"births": n, "constant": not conflicts, "conflicts": conflicts})
    return result


def controls(levels, quotients):
    by_name = {q["name"]: q for q in quotients}

    def history(n, order, record):
        return next(
            i
            for i, (c, r, _) in enumerate(levels[n])
            if c == tuple(map(tuple, order)) and r == tuple(record)
        )

    def target(q, n, order, record):
        return class_lookup(q["partitions"][n])[history(n, order, record)]

    def observed(kernels):
        rho = state((1, 0, 0))
        return {
            "input_bloch": ["1", "0", "0"],
            "outputs": [ex.matrix_wire(apply_map(k, rho)) for k in kernels],
            "trace_probabilities": [str(probability(k, rho)) for k in kernels],
            "probabilities_Px": [str(probability(k, rho, EFFECTS[2])) for k in kernels],
        }

    shape = by_name["shape_ones"]
    pair = [history(2, [[], [0]], [0, 1]), history(2, [[], [0]], [1, 0])]
    t = target(shape, 3, [[], [0], [0]], [1, 0, 0])
    kernels = [shape["steps"][2]["actual_rows"][h][t] for h in pair]
    chain = {
        "births": 2,
        "quotient": "shape_ones",
        "histories": pair,
        "target": t,
        "kernels": [MapValue(k) for k in kernels],
        **observed(kernels),
    }
    h = history(1, [[]], [1])
    g = class_lookup(shape["partitions"][1])[h]
    actual = shape["two_steps"][1]["actual_rows"][h][t]
    proposed = shape["two_steps"][1]["representative_rows"][g][t]
    delayed = {
        "births": 1,
        "quotient": "shape_ones",
        "history": h,
        "representative": shape["partitions"][1][g]["members"][0],
        "target": t,
        "one_step_exact": shape["steps"][1]["actual_rows"][h]
        == shape["steps"][1]["representative_rows"][g],
        "actual": MapValue(actual),
        "proposed": MapValue(proposed),
        **observed((actual, proposed)),
    }
    reduced = by_name["link_counts_ones"]
    pair = [history(3, [[], [0], [0]], [0, 0, 0]), history(3, [[], [], [0, 1]], [0, 0, 0])]
    lookup = class_lookup(reduced["partitions"][3])
    row_a, row_b = (reduced["steps"][3]["actual_rows"][i] for i in pair)
    targets = [
        i for i, group in enumerate(reduced["partitions"][4]) if group["key"]["incomparable"] == 1
    ]
    fork_join = {
        "births": 3,
        "quotient": "link_counts_ones",
        "histories": pair,
        "parent_class_same": lookup[pair[0]] == lookup[pair[1]],
        "one_step_rows_equal": row_a == row_b,
        "counts_probe_incomparable": 1,
        "probabilities": [
            str(probability(summed(row[i] for i in targets), state((0, 0, 0))))
            for row in (row_a, row_b)
        ],
    }
    pair = [history(3, [[], [], [0]], [0, 0, 1]), history(3, [[], [], [0]], [0, 1, 0])]
    lookup = class_lookup(shape["partitions"][3])
    row_a, row_b = (shape["steps"][3]["actual_rows"][i] for i in pair)
    target_index = next(
        (i for i, (a, b) in enumerate(zip(row_a, row_b, strict=True)) if a != b), None
    )
    location = {
        "births": 3,
        "quotient": "shape_ones",
        "histories": pair,
        "parent_class_same": lookup[pair[0]] == lookup[pair[1]],
        "row_equal": row_a == row_b,
        "first_target": target_index,
        "kernels": []
        if target_index is None
        else [MapValue(row_a[target_index]), MapValue(row_b[target_index])],
    }
    marked = by_name["marked_order"]
    g = next(i for i, group in enumerate(marked["partitions"][2]) if len(group["members"]) > 1)
    members = marked["partitions"][2][g]["members"]
    correct = marked["steps"][2]["representative_rows"][g]
    wrong = [
        summed(marked["steps"][2]["actual_rows"][h][t] for h in members)
        for t in range(len(correct))
    ]
    wrong_sum = {
        "births": 2,
        "quotient": "marked_order",
        "parent_class": g,
        "members": members,
        "correct_row": [MapValue(m) for m in correct],
        "wrong_row": [MapValue(m) for m in wrong],
        "correct_trace": str(probability(summed(correct), state((0, 0, 0)))),
        "wrong_trace": str(probability(summed(wrong), state((0, 0, 0)))),
    }
    return {
        "chain_record": chain,
        "delayed": delayed,
        "fork_join": fork_join,
        "record_location": location,
        "wrong_parent_sum": wrong_sum,
    }


def analyze(wire):
    name, rule, p, uniform = parse(wire)
    levels, sources, fine_steps = build_fine(rule, p, uniform)
    quotients = [quotient(summary, levels, sources, fine_steps) for summary in SUMMARIES]
    data = {
        "case": name,
        "levels": [
            {
                "births": n,
                "histories": [
                    {
                        "order": [list(s) for s in c],
                        "outcomes": list(r),
                        "settings": list(marks),
                        "source": MapValue(sources[n][h]),
                    }
                    for h, (c, r, marks) in enumerate(histories)
                ],
            }
            for n, histories in enumerate(levels)
        ],
        "fine_steps": [
            {
                "births": n,
                "rows": [
                    [{**edge, "kernel": MapValue(edge["kernel"])} for edge in edges]
                    for edges in rows
                ],
            }
            for n, rows in enumerate(fine_steps)
        ],
        "quotients": [],
        "refinements": refinements(quotients),
        "source_covariance": source_covariance(quotients[0]["partitions"], sources),
        "controls": controls(levels, quotients),
        "counts": {
            "level_histories": list(map(len, levels)),
            "raw_birth_edges": sum(len(row) for step in fine_steps for row in step),
            "marked_classes": [len(groups) for groups in quotients[0]["partitions"]],
            "one_step_checks": sum(
                len(step["actual_rows"]) * len(step["actual_rows"][0])
                for q in quotients
                for step in q["steps"]
            ),
            "two_step_checks": sum(
                len(step["actual_rows"]) * len(step["actual_rows"][0])
                for q in quotients
                for step in q["two_steps"]
            ),
        },
    }
    for q in quotients:
        out = {"name": q["name"], "partitions": q["partitions"]}
        for kind in ("steps", "two_steps"):
            out[kind] = [
                {
                    **step,
                    "actual_rows": [[MapValue(m) for m in row] for row in step["actual_rows"]],
                    "representative_rows": [
                        [MapValue(m) for m in row] for row in step["representative_rows"]
                    ],
                }
                for step in q[kind]
            ]
        data["quotients"].append(out)
    return pack(data)
