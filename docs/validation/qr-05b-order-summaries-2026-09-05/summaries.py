"""Exact fixed-fixture summaries; direct Kraus continuation on operator units."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "qr-05a-quantum-births-2026-09-05" / "results.json"
SOURCE_SHA = "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479"
EXACT = HERE.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
EXACT_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"
CASES = ("weak_phase", "grouped_dephase", "zero_link_boundary", "chain_boundary")
CANDIDATES = ("constant", "source_effect", "payload_map", "payload_counts", "decorated_order")
FAMILIES = ("F0", "F1", "F2")
BIRTH_KEYS = tuple(product(range(4), range(2), range(2)))
BLOCH = ((0, 0, 0), (F(1, 2), 0, 0), (0, F(1, 2), 0), (0, 0, F(1, 2)))
EFFECT_NAMES = ("P0", "P1", "P+X", "P+Y")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_bytes(path, sha):
    require(path.is_file() and not path.is_symlink(), "pinned input must be a plain file")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == sha, "pinned input identity differs")
    return raw


def load_exact():
    raw = pinned_bytes(EXACT, EXACT_SHA)
    name = "qr05b_direct_exact"
    require(name not in sys.modules, "private arithmetic module collision")
    spec = importlib.util.spec_from_file_location(name, EXACT)
    require(spec is not None and spec.loader is not None, "cannot load arithmetic")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(EXACT), "exec"), module.__dict__)  # noqa: S102
    return module


ex = load_exact()
ZERO = (ex.ZERO,) * 4


def parse(wire):
    ex._keys(wire, ("schema_version", "case"))
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05b-problem-v1",
        "unsupported schema",
    )
    require(type(wire["case"]) is str and wire["case"] in CASES, "unknown fixed case")
    return wire["case"]


def source_case(name):
    report = json.loads(pinned_bytes(SOURCE, SOURCE_SHA))
    require(report["schema_version"] == "det8-qr05a-results-v1", "wrong prior schema")
    case = next(c for c in report["suite"]["cases"] if c["id"] == name)
    require(all(case["analysis"]["flags"].values()), "source is not a positive fixture")
    rows = case["analysis"]["levels"][-1]["histories"]
    require(len(rows) == 56, "prior inventory changed")
    return case["input"], rows


def decode_source(wire):
    matrix = ex.decode_matrix(wire, 4)
    require(
        all(matrix[i][j] == ex.ZERO for i in range(4) for j in range(4) if i != j),
        "source map not diagonal",
    )
    return tuple(matrix[i][i] for i in range(4))


def map_wire(diagonal):
    return [v.wire() for v in diagonal]


def add_maps(maps):
    result = ZERO
    for diagonal in maps:
        result = tuple(a + b for a, b in zip(result, diagonal, strict=True))
    return result


def scale_map(diagonal, weight):
    return tuple(ex.q(weight) * value for value in diagonal)


def ideals(order):
    return tuple(
        sorted(
            s
            for size in range(len(order) + 1)
            for s in combinations(range(len(order)), size)
            if all(set(order[j]) <= set(s) for j in s)
        )
    )


def maximal(order, subset):
    return sum(not any(i in order[j] for j in subset) for i in subset)


def counts(order):
    n = len(order)
    return (
        n,
        sum(maximal(order, past) for past in order),
        n * (n - 1) // 2 - sum(map(len, order)),
        sum(not past for past in order),
        maximal(order, tuple(range(n))),
    )


def decorated(order, record, settings):
    return min(
        (
            "".join("1" if a in order[b] else "0" for a in perm for b in perm),
            tuple((settings[i], record[i]) for i in perm),
        )
        for perm in permutations(range(len(order)))
    )


def weight(order, subset, p):
    return p ** maximal(order, subset) * (1 - p) ** (len(order) - len(subset))


def kraus(rule, parity, outcome):
    a, b = (F(3, 5), F(4, 5)) if outcome == 0 else (F(4, 5), F(3, 5))
    phase = ex.q(0, 1) if parity else ex.ONE
    d = ((ex.q(a), ex.ZERO), (ex.ZERO, phase * ex.q(b)))
    if rule == "weak_phase":
        return (d,)
    require(rule == "weak_dephase", "unexpected instrument")
    z = ((ex.ONE, ex.ZERO), (ex.ZERO, ex.q(-1)))
    return ex.scale(d, ex.q(F(3, 5))), ex.scale(ex.mul(z, d), ex.q(F(4, 5)))


def continue_map(source, operators):
    columns = []
    for index in range(4):
        state = tuple(
            tuple(source[index] if 2 * i + j == index else ex.ZERO for j in range(2))
            for i in range(2)
        )
        result = ex.zeros(2)
        for operator in operators:
            result = ex.add(result, ex.mul(ex.mul(operator, state), ex.dagger(operator)))
        columns.append(tuple(value for row in result for value in row))
    require(
        all(columns[j][i] == ex.ZERO for i in range(4) for j in range(4) if i != j),
        "continuation map not diagonal",
    )
    return tuple(columns[i][i] for i in range(4))


def births(order, record, source, p, rule):
    bank = {key: ZERO for key in BIRTH_KEYS}
    for subset in ideals(order):
        b = sum(record[i] for i in subset) % 2
        q = weight(order, subset, p)
        for x in range(2):
            key = (len(subset), b, x)
            branch = scale_map(continue_map(source, kraus(rule, b, x)), q)
            bank[key] = add_maps((bank[key], branch))
    result = tuple(bank[key] for key in BIRTH_KEYS)
    total = add_maps(result)
    require(
        (total[0], total[3]) == (source[0], source[3]), "future outcome sum changed source trace"
    )
    return result


def partition(keys):
    groups = {}
    for index, key in enumerate(keys):
        groups.setdefault(key, []).append(index)
    return sorted(groups.values(), key=lambda members: members[0])


def refines(fine, coarse):
    lookup = {h: i for i, group in enumerate(coarse) for h in group}
    return all(len({lookup[h] for h in group}) == 1 for group in fine)


def state(vector):
    x, y, z = map(F, vector)
    return ((ex.q((1 + z) / 2), ex.q(x / 2, -y / 2)), (ex.q(x / 2, y / 2), ex.q((1 - z) / 2)))


EFFECTS = (state((0, 0, 1)), state((0, 0, -1)), state((1, 0, 0)), state((0, 1, 0)))


def apply_map(diagonal, rho):
    return tuple(tuple(diagonal[2 * i + j] * rho[i][j] for j in range(2)) for i in range(2))


def probability(diagonal, rho, effect=None):
    output = apply_map(diagonal, rho)
    value = ex.trace(output if effect is None else ex.mul(effect, output))
    require(value.imag == 0 and value.real >= 0, "invalid physical probability")
    return value.real


def witness(pair, signatures, stop, count_keys):
    left, right = pair
    for index in range(stop):
        a, b = signatures[left][index], signatures[right][index]
        if a == b:
            continue
        if index == 0:
            probe, outcome = "payload", None
        elif index <= len(count_keys):
            probe, outcome = "order_counts", list(count_keys[index - 1])
        else:
            probe, outcome = "next_birth", list(BIRTH_KEYS[index - 1 - len(count_keys)])
        for bloch in BLOCH:
            rho = state(bloch)
            for effect_name, effect in zip(EFFECT_NAMES, EFFECTS, strict=True):
                values = [probability(m, rho, effect) for m in (a, b)]
                if values[0] != values[1]:
                    return {
                        "histories": list(pair),
                        "probe": probe,
                        "outcome": outcome,
                        "input_bloch": [str(v) for v in bloch],
                        "effect": effect_name,
                        "source_probabilities": [
                            str(probability(signatures[h][0], rho)) for h in pair
                        ],
                        "joint_probabilities": [str(v) for v in values],
                    }
        raise ValueError("complete physical witness bank missed a map discrepancy")
    raise ValueError("witness requested for equal signatures")


def sum_signatures(signatures):
    return tuple(add_maps(column) for column in zip(*signatures, strict=True))


def signature_wire(signature, count_keys):
    split = 1 + len(count_keys)
    return {
        "source": map_wire(signature[0]),
        "counts": [map_wire(m) for m in signature[1:split]],
        "birth": [map_wire(m) for m in signature[split:]],
    }


def aggregate(histories, signatures, decorated_classes, count_keys):
    direct_rows, staged_rows = [], []
    decorated_sums = [sum_signatures([signatures[h] for h in group]) for group in decorated_classes]
    for key in count_keys:
        members = [i for i, h in enumerate(histories) if tuple(h["counts"]) == key]
        class_ids = [
            i
            for i, group in enumerate(decorated_classes)
            if tuple(histories[group[0]]["counts"]) == key
        ]
        require(
            sorted(h for i in class_ids for h in decorated_classes[i]) == members,
            "coarsening changed membership",
        )
        direct = sum_signatures([signatures[h] for h in members])
        staged = sum_signatures([decorated_sums[i] for i in class_ids])
        direct_rows.append(
            {"key": list(key), "members": members, "signature": signature_wire(direct, count_keys)}
        )
        staged_rows.append(
            {"key": list(key), "members": members, "signature": signature_wire(staged, count_keys)}
        )
    total = sum_signatures(signatures)
    via_counts = sum_signatures(
        [
            sum_signatures(
                [signatures[i] for i, h in enumerate(histories) if tuple(h["counts"]) == key]
            )
            for key in count_keys
        ]
    )
    via_decorated = sum_signatures(decorated_sums)
    wrong = add_maps(
        scale_map(signature[0], F(1, len(group)))
        for signature, group in zip(decorated_sums, decorated_classes, strict=True)
    )
    correct_trace = probability(total[0], state((0, 0, 0)))
    require(
        correct_trace == 1 and total[0][0] == total[0][3] == ex.ONE,
        "source total not trace preserving",
    )
    return {
        "direct_counts": direct_rows,
        "via_decorated_counts": staged_rows,
        "direct_total": signature_wire(total, count_keys),
        "via_counts_total": signature_wire(via_counts, count_keys),
        "via_decorated_total": signature_wire(via_decorated, count_keys),
        "counts_equal": direct_rows == staged_rows,
        "totals_equal": total == via_counts == via_decorated,
        "wrong_average_source": map_wire(wrong),
        "wrong_average_trace": str(probability(wrong, state((0, 0, 0)))),
        "correct_trace": str(correct_trace),
    }


def growth_table(order, record, p):
    table = [[F(0), F(0)] for _ in range(4)]
    for subset in ideals(order):
        table[len(subset)][sum(record[i] for i in subset) % 2] += weight(order, subset, p)
    require(sum(map(sum, table)) == 1, "growth distribution not normalized")
    return {
        "joint": [[str(v) for v in row] for row in table],
        "size": [str(sum(row)) for row in table],
        "parity": [str(sum(row[b] for row in table)) for b in range(2)],
    }


def controls(histories, p):
    def get(order, record):
        return next(
            i for i, h in enumerate(histories) if h["order"] == order and h["outcomes"] == record
        )

    def pair_info(indices):
        rows = [histories[i] for i in indices]
        return {
            "histories": indices,
            "source_live": [not row["zero_source"] for row in rows],
            "source_equal": rows[0]["source"] == rows[1]["source"],
            "counts_equal": rows[0]["counts"] == rows[1]["counts"],
            "distributions": [growth_table(row["order"], row["outcomes"], p) for row in rows],
        }

    fork_join = pair_info([get([[], [0], [0]], [0, 0, 0]), get([[], [], [0, 1]], [0, 0, 0])])
    locations = pair_info([get([[], [], [0]], [0, 0, 1]), get([[], [], [0]], [0, 1, 0])])
    return {"fork_join": fork_join, "record_location": locations}


def analyze(wire):
    name = parse(wire)
    problem, source_rows = source_case(name)
    p, rule = F(problem["growth"]["p"]), problem["instrument"]
    histories, internal, decor_keys = [], [], []
    for row in source_rows:
        order, record, settings = (
            tuple(map(tuple, row["order"])),
            tuple(row["outcomes"]),
            tuple(row["settings"]),
        )
        source = decode_source(row["superoperator"])
        future = births(order, record, source, p, rule)
        key = decorated(order, record, settings)
        decor_keys.append(key)
        internal.append((source, counts(order), future))
        histories.append(
            {
                "order": row["order"],
                "outcomes": row["outcomes"],
                "settings": row["settings"],
                "counts": list(counts(order)),
                "decorated_key": {"relation": key[0], "record": [list(v) for v in key[1]]},
                "source": map_wire(source),
                "next_birth": [map_wire(m) for m in future],
                "zero_source": source == ZERO,
            }
        )
    count_keys = tuple(sorted({row[1] for row in internal}))
    signatures = [
        (source, *(source if count == key else ZERO for key in count_keys), *future)
        for source, count, future in internal
    ]
    candidate_keys = (
        [0] * len(histories),
        [(s[0], s[3]) for s, _, _ in internal],
        [s for s, _, _ in internal],
        [(s, c) for s, c, _ in internal],
        decor_keys,
    )
    candidates = [
        {"name": label, "classes": partition(keys)}
        for label, keys in zip(CANDIDATES, candidate_keys, strict=True)
    ]
    families, previous = [], None
    for family, stop in zip(FAMILIES, (1, 1 + len(count_keys), len(signatures[0])), strict=True):
        classes = partition(signature[:stop] for signature in signatures)
        checks = []
        for candidate in candidates:
            conflicts = sorted(
                [a, b]
                for group in candidate["classes"]
                for a, b in combinations(group, 2)
                if signatures[a][:stop] != signatures[b][:stop]
            )
            checks.append(
                {
                    "name": candidate["name"],
                    "valid": not conflicts,
                    "conflicts": conflicts,
                    "first_witness": witness(conflicts[0], signatures, stop, count_keys)
                    if conflicts
                    else None,
                }
            )
        families.append(
            {
                "name": family,
                "classes": classes,
                "refines_previous": None if previous is None else refines(classes, previous),
                "candidate_checks": checks,
            }
        )
        previous = classes
    return {
        "case": name,
        "count_keys": [list(key) for key in count_keys],
        "birth_keys": [list(key) for key in BIRTH_KEYS],
        "histories": histories,
        "candidates": candidates,
        "families": families,
        "aggregation": aggregate(histories, signatures, candidates[-1]["classes"], count_keys),
        "controls": controls(histories, p),
        "counts": {
            "histories": len(histories),
            "zero_sources": sum(h["zero_source"] for h in histories),
            "continuation_blocks": len(histories) * len(BIRTH_KEYS),
            "decorated_classes": len(candidates[-1]["classes"]),
            "family_classes": [len(f["classes"]) for f in families],
            "candidate_checks": len(FAMILIES) * len(CANDIDATES),
            "candidate_conflicts": sum(
                len(c["conflicts"]) for f in families for c in f["candidate_checks"]
            ),
        },
    }
