"""Independent diagonal-coefficient reference; no direct-executor imports.

Continuation is derived analytically, witnesses use Bloch coefficients, and
partitions use pairwise equivalence rather than the primary's keyed grouping.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path

PRIOR = Path(__file__).resolve().parent.parent / "qr-05a-quantum-births-2026-09-05" / "results.json"
PRIOR_HASH = "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479"
CASE_NAMES = ("weak_phase", "grouped_dephase", "zero_link_boundary", "chain_boundary")
SUMMARY_NAMES = ("constant", "source_effect", "payload_map", "payload_counts", "decorated_order")
OUTPUTS = [(m, b, x) for m in range(4) for b in range(2) for x in range(2)]
PROBES = (("0", "0", "0"), ("1/2", "0", "0"), ("0", "1/2", "0"), ("0", "0", "1/2"))


def check(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    result = Fraction(value)
    check(
        max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 4096,
        "rational guard exceeded",
    )
    return result


Z = (Fraction(0), Fraction(0))
ZERO_DIAG = (Z, Z, Z, Z)


def plus(a, b):
    return rational(a[0] + b[0]), rational(a[1] + b[1])


def times(a, b):
    return rational(a[0] * b[0] - a[1] * b[1]), rational(a[0] * b[1] + a[1] * b[0])


def diag_sum(items):
    result = list(ZERO_DIAG)
    for item in items:
        for i in range(4):
            result[i] = plus(result[i], item[i])
    return tuple(result)


def diag_scale(item, factor):
    return tuple(times(value, (factor, Fraction(0))) for value in item)


def encode(diagonal):
    return [[str(a), str(b)] for a, b in diagonal]


def decode(matrix):
    check(len(matrix) == 4 and all(len(row) == 4 for row in matrix), "source dimension")
    values = [[tuple(rational(v) for v in cell) for cell in row] for row in matrix]
    check(
        all(values[i][j] == Z for i in range(4) for j in range(4) if i != j), "source not diagonal"
    )
    d = tuple(values[i][i] for i in range(4))
    check(
        d[0][1] == d[3][1] == 0 and d[1] == (d[2][0], -d[2][1]), "source not Hermiticity preserving"
    )
    return d


def load(wire):
    check(type(wire) is dict and set(wire) == {"schema_version", "case"}, "bad root fields")
    check(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05b-problem-v1",
        "wrong schema",
    )
    check(type(wire["case"]) is str and wire["case"] in CASE_NAMES, "unsupported fixed case")
    check(PRIOR.is_file() and not PRIOR.is_symlink(), "prior not plain file")
    data = PRIOR.read_bytes()
    check(hashlib.sha256(data).hexdigest() == PRIOR_HASH, "prior identity differs")
    artifact = json.loads(data)
    check(artifact["schema_version"] == "det8-qr05a-results-v1", "prior schema")
    matches = [c for c in artifact["suite"]["cases"] if c["id"] == wire["case"]]
    check(len(matches) == 1, "prior case inventory")
    case = matches[0]
    check(all(case["analysis"]["flags"].values()), "source not consistent")
    history = case["analysis"]["levels"][3]["histories"]
    check(len(history) == 56, "source history inventory")
    return case["input"], history


def relation(order):
    return [[i in order[j] for j in range(3)] for i in range(3)]


def order_counts(order):
    rel = relation(order)
    links = sum(
        rel[i][j] and not any(rel[i][k] and rel[k][j] for k in range(3))
        for i in range(3)
        for j in range(3)
    )
    related = sum(sum(row) for row in rel)
    minima = sum(not any(rel[i][j] for i in range(3)) for j in range(3))
    maxima = sum(not any(rel[i][j] for j in range(3)) for i in range(3))
    return (3, links, 3 - related, minima, maxima)


def isomorphism_key(row):
    rel = relation(row["order"])
    options = []
    for p in permutations(range(3)):
        options.append(
            (
                "".join(str(int(rel[p[i]][p[j]])) for i in range(3) for j in range(3)),
                tuple((row["settings"][p[i]], row["outcomes"][p[i]]) for i in range(3)),
            )
        )
    return min(options)


def growth_entries(order, record, p):
    rel = relation(order)
    entries = []
    for mask in range(8):
        s = [i for i in range(3) if mask & (1 << i)]
        if any(rel[i][j] and i not in s for j in s for i in range(3)):
            continue
        maxima = sum(not any(rel[i][j] for j in s) for i in s)
        q = rational(p**maxima * (1 - p) ** (3 - len(s)))
        entries.append((len(s), sum(record[i] for i in s) % 2, q))
    check(sum(e[2] for e in entries) == 1, "growth not normalized")
    return entries


def next_coefficients(source, entries, grouped):
    table = {(m, b): Fraction(0) for m in range(4) for b in range(2)}
    for m, b, q in entries:
        table[m, b] += q
    result = []
    for m, b, x in OUTPUTS:
        a = Fraction(3 if x == 0 else 4, 5)
        d = Fraction(4 if x == 0 else 3, 5)
        damp = Fraction(-7, 25) if grouped else Fraction(1)
        # V^b multiplies the lower amplitude: E01 gets conjugate i^b.
        coherence = (a * d * damp, Fraction(0)) if b == 0 else (Fraction(0), -a * d * damp)
        kernel = (
            (a * a, Fraction(0)),
            coherence,
            (coherence[0], -coherence[1]),
            (d * d, Fraction(0)),
        )
        result.append(diag_scale(tuple(times(source[i], kernel[i]) for i in range(4)), table[m, b]))
    total = diag_sum(result)
    check(total[0] == source[0] and total[3] == source[3], "trace effect changed")
    return tuple(result)


def equivalence_classes(values):
    remaining = set(range(len(values)))
    groups = []
    while remaining:
        representative = min(remaining)
        group = [i for i in sorted(remaining) if values[i] == values[representative]]
        groups.append(group)
        remaining.difference_update(group)
    return groups


def is_refinement(fine, coarse):
    return all(any(set(group) <= set(parent) for parent in coarse) for group in fine)


def probability_values(diagonal, vector):
    x, y, z = map(Fraction, vector)
    pop0 = rational(diagonal[0][0] * (1 + z) / 2)
    pop1 = rational(diagonal[3][0] * (1 - z) / 2)
    real = rational((diagonal[1][0] * x + diagonal[1][1] * y) / 2)
    imag = rational((diagonal[1][1] * x - diagonal[1][0] * y) / 2)
    total = rational(pop0 + pop1)
    effects = (pop0, pop1, rational(total / 2 + real), rational(total / 2 - imag))
    check(all(value >= 0 for value in effects), "negative physical witness")
    return total, effects


def first_witness(pair, signatures, size, keys):
    a, b = pair
    differing = next(i for i in range(size) if signatures[a][i] != signatures[b][i])
    if differing == 0:
        probe, outcome = "payload", None
    elif differing <= len(keys):
        probe, outcome = "order_counts", list(keys[differing - 1])
    else:
        probe, outcome = "next_birth", list(OUTPUTS[differing - 1 - len(keys)])
    for vector in PROBES:
        pa = probability_values(signatures[a][differing], vector)[1]
        pb = probability_values(signatures[b][differing], vector)[1]
        for i, label in enumerate(("P0", "P1", "P+X", "P+Y")):
            if pa[i] != pb[i]:
                return {
                    "histories": pair,
                    "probe": probe,
                    "outcome": outcome,
                    "input_bloch": list(vector),
                    "effect": label,
                    "source_probabilities": [
                        str(probability_values(signatures[h][0], vector)[0]) for h in pair
                    ],
                    "joint_probabilities": [str(pa[i]), str(pb[i])],
                }
    raise ValueError("no witness in complete bank")


def total_signature(items):
    items = list(items)
    check(bool(items), "empty signature inventory")
    return tuple(diag_sum(item[i] for item in items) for i in range(len(items[0])))


def encode_signature(value, keys):
    return {
        "source": encode(value[0]),
        "counts": [encode(value[i + 1]) for i in range(len(keys))],
        "birth": [encode(v) for v in value[1 + len(keys) :]],
    }


def aggregation(rows, signatures, classes, keys):
    by_class = [total_signature(signatures[i] for i in group) for group in classes]
    direct, staged, coarse_values = [], [], []
    for key in keys:
        members = [i for i, row in enumerate(rows) if tuple(row["counts"]) == key]
        indices = [j for j, group in enumerate(classes) if set(group) <= set(members)]
        check(sorted(i for j in indices for i in classes[j]) == members, "invalid coarse class")
        d = total_signature(signatures[i] for i in members)
        s = total_signature(by_class[j] for j in indices)
        coarse_values.append(d)
        direct.append(
            {"key": list(key), "members": members, "signature": encode_signature(d, keys)}
        )
        staged.append(
            {"key": list(key), "members": members, "signature": encode_signature(s, keys)}
        )
    whole = total_signature(signatures)
    from_counts, from_classes = total_signature(coarse_values), total_signature(by_class)
    average = diag_sum(
        diag_scale(by_class[j][0], Fraction(1, len(group))) for j, group in enumerate(classes)
    )
    correct = probability_values(whole[0], PROBES[0])[0]
    check(
        correct == 1 and whole[0][0] == whole[0][3] == (Fraction(1), Fraction(0)),
        "incorrect source total",
    )
    return {
        "direct_counts": direct,
        "via_decorated_counts": staged,
        "direct_total": encode_signature(whole, keys),
        "via_counts_total": encode_signature(from_counts, keys),
        "via_decorated_total": encode_signature(from_classes, keys),
        "counts_equal": direct == staged,
        "totals_equal": whole == from_counts == from_classes,
        "wrong_average_source": encode(average),
        "wrong_average_trace": str(probability_values(average, PROBES[0])[0]),
        "correct_trace": str(correct),
    }


def control_pair(rows, targets, p):
    indices = [
        next(i for i, row in enumerate(rows) if (row["order"], row["outcomes"]) == target)
        for target in targets
    ]
    a, b = (rows[i] for i in indices)
    distributions = []
    for row in (a, b):
        joint = [[Fraction(0), Fraction(0)] for _ in range(4)]
        for m, parity, q in growth_entries(row["order"], row["outcomes"], p):
            joint[m][parity] += q
        distributions.append(
            {
                "joint": [[str(v) for v in row] for row in joint],
                "size": [str(row[0] + row[1]) for row in joint],
                "parity": [str(sum(row[b] for row in joint)) for b in range(2)],
            }
        )
    return {
        "histories": indices,
        "source_live": [not row["zero_source"] for row in (a, b)],
        "source_equal": a["source"] == b["source"],
        "counts_equal": a["counts"] == b["counts"],
        "distributions": distributions,
    }


def analyze(wire):
    problem, prior_rows = load(wire)
    p = Fraction(problem["growth"]["p"])
    rows, maps, features, iso_keys, futures = [], [], [], [], []
    for prior in prior_rows:
        source = decode(prior["superoperator"])
        feature = order_counts(prior["order"])
        key = isomorphism_key(prior)
        future = next_coefficients(
            source,
            growth_entries(prior["order"], prior["outcomes"], p),
            problem["instrument"] == "weak_dephase",
        )
        maps.append(source)
        features.append(feature)
        iso_keys.append(key)
        futures.append(future)
        rows.append(
            {
                "order": prior["order"],
                "outcomes": prior["outcomes"],
                "settings": prior["settings"],
                "counts": list(feature),
                "decorated_key": {"relation": key[0], "record": [list(mark) for mark in key[1]]},
                "source": encode(source),
                "next_birth": [encode(m) for m in future],
                "zero_source": source == ZERO_DIAG,
            }
        )
    keys = sorted(set(features))
    signatures = [
        tuple(
            [maps[i]]
            + [maps[i] if features[i] == k else ZERO_DIAG for k in keys]
            + list(futures[i])
        )
        for i in range(56)
    ]
    summaries = (
        [None] * 56,
        [(s[0], s[3]) for s in maps],
        maps,
        list(zip(maps, features, strict=True)),
        iso_keys,
    )
    candidates = [
        {"name": name, "classes": equivalence_classes(summary)}
        for name, summary in zip(SUMMARY_NAMES, summaries, strict=True)
    ]
    families = []
    for number, size in enumerate((1, 1 + len(keys), len(signatures[0]))):
        signature_keys = [s[:size] for s in signatures]
        groups = equivalence_classes(signature_keys)
        checks = []
        for candidate in candidates:
            same_summary = {
                (a, b) for group in candidate["classes"] for a in group for b in group if a < b
            }
            conflicts = [
                [a, b]
                for a in range(56)
                for b in range(a + 1, 56)
                if (a, b) in same_summary and signature_keys[a] != signature_keys[b]
            ]
            checks.append(
                {
                    "name": candidate["name"],
                    "valid": len(conflicts) == 0,
                    "conflicts": conflicts,
                    "first_witness": first_witness(conflicts[0], signatures, size, keys)
                    if conflicts
                    else None,
                }
            )
        families.append(
            {
                "name": f"F{number}",
                "classes": groups,
                "refines_previous": is_refinement(groups, families[-1]["classes"])
                if families
                else None,
                "candidate_checks": checks,
            }
        )
    return {
        "case": wire["case"],
        "count_keys": [list(k) for k in keys],
        "birth_keys": [list(k) for k in OUTPUTS],
        "histories": rows,
        "candidates": candidates,
        "families": families,
        "aggregation": aggregation(rows, signatures, candidates[-1]["classes"], keys),
        "controls": {
            "fork_join": control_pair(
                rows, [([[], [0], [0]], [0, 0, 0]), ([[], [], [0, 1]], [0, 0, 0])], p
            ),
            "record_location": control_pair(
                rows, [([[], [], [0]], [0, 0, 1]), ([[], [], [0]], [0, 1, 0])], p
            ),
        },
        "counts": {
            "histories": 56,
            "zero_sources": sum(row["zero_source"] for row in rows),
            "continuation_blocks": 896,
            "decorated_classes": len(candidates[-1]["classes"]),
            "family_classes": [len(f["classes"]) for f in families],
            "candidate_checks": sum(len(f["candidate_checks"]) for f in families),
            "candidate_conflicts": sum(
                len(c["conflicts"]) for f in families for c in f["candidate_checks"]
            ),
        },
    }
