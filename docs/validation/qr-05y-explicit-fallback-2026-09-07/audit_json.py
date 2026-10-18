"""Independent stdlib JSON-only QR-05Y raw-fallback-policy audit.

Static own-lineage raw helpers; no current/prior executor, runner or test
imports. Source bytes are consulted only for identity hashes. This audit
reconstructs W conditional laws, not prior operator/minimality certificates.
"""

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
XDIR = ROOT / "docs/validation/qr-05x-noise-misspecification-2026-09-07"
X_PRIOR = "qr-05x-noise-misspecification-2026-09-07/results.json"
X_ID = {
    "bytes": 8842933,
    "sha256": "1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4",
}
WDIR = ROOT / "docs/validation/qr-05w-noisy-readouts-2026-09-07"
W_PRIOR = "qr-05w-noisy-readouts-2026-09-07/results.json"
W_ID = {
    "bytes": 6756094,
    "sha256": "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a",
}
SDIR = ROOT / "docs/validation/qr-05s-local-deletion-2026-09-06"
LEVELS = [F(0), F(1, 2), F(3, 4), F(1)]
GARB = [F(1, 2), F(1, 2), F(1)]
COUNTS = defaultdict(int)
START = time.monotonic()


def check(condition, message):
    COUNTS["checks"] += 1
    if not condition:
        raise RuntimeError(message)


def eq(left, right, message):
    check(left == right, message)


def native_tree(value, depth=0):
    """Mathematical wire validation, separate from runtime float metadata."""
    check(depth <= 128, "strict native wire depth")
    kind = type(value)
    if value is None or kind in (str, bool):
        return
    if kind is int:
        check(abs(value).bit_length() <= 4096, "strict native integer bits")
        return
    check(kind in (list, dict), "strict mathematical native JSON type")
    if kind is dict:
        check(all(type(key) is str for key in value), "strict native dictionary keys")
        children = value.values()
    else:
        children = value
    for child in children:
        native_tree(child, depth + 1)


def native_eq(left, right, message):
    # Canonical bytes distinguish bool/int, preserve every key, and reject
    # numeric coercion that Python's container equality would permit.
    check(canon(left) == canon(right), message)


def canon(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()


def ident(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def rat(pair):
    check(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "fraction native pair",
    )
    n, d = pair
    check(0 <= n <= d and d > 0 and math.gcd(n, d) == 1, "fraction canonical range")
    check(max(n.bit_length(), d.bit_length()) <= 4096, "fraction bits")
    return F(n, d)


def wire(value, maximum=1):
    check(type(value) is F and 0 <= value <= maximum, "emitted fraction range")
    check(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "retained component bits",
    )
    return [value.numerator, value.denominator]


def add(target, key, value):
    if value:
        target[key] += value


def law_wire(law):
    return [{"value": list(q), "probability": wire(p)} for q, p in sorted(law.items()) if p]


def post_wire(law):
    return [{"class_id": h, "probability": wire(p)} for h, p in sorted(law.items()) if p]


def parse_law(rows, field="value"):
    out = {}
    last = None
    for row in rows:
        key = tuple(row[field]) if field == "value" else row[field]
        check(last is None or last < key, "wire support sorted unique")
        last = key
        p = rat(row["probability"])
        check(p > 0, "positive sparse support")
        out[key] = p
    eq(sum(out.values(), F(0)), F(1), "wire law mass")
    return out


def risk(law):
    # Independent replicas disagree with probability sum_q p(q)(1-p(q)).
    COUNTS["two_replica_terms"] += len(law)
    return sum((p * (1 - p) for p in law.values()), F(0))


def fields(obj, names, title):
    eq(set(obj), set(names.split()), title + " fields")


def all_true(obj, names, title):
    fields(obj, names, title)
    for name in names.split():
        eq(obj[name], True, title + " " + name)


def subset_ids(raw):
    states, frames = raw["states"], raw["frames"]
    relations, keys, ranks, internals, eligible = [], {}, [], [], []
    for sid, row in enumerate(states):
        eq(row["state_id"], sid, "raw contiguous state ID")
        kept = tuple(row["kept"])
        check(
            tuple(sorted(set(kept))) == kept and kept[0] == 0 and kept[-1] == 7, "raw kept labels"
        )
        frame = frames[row["frame_id"]]
        check(set(frame["fixed"]) <= set(kept), "raw frame fixed present")
        rel = {(kept[i], kept[j]) for j, past in enumerate(row["past"]) for i in past}
        check(all(a != b and (b, a) not in rel for a, b in rel), "raw strict relation")
        check(
            all((a, d) in rel for a, b in rel for c, d in rel if b == c), "raw transitive relation"
        )
        inside = tuple(x for x in kept if x not in (0, 7))
        check(
            all((0, x) in rel and (x, 7) in rel for x in inside) and (0, 7) in rel,
            "raw endpoint order",
        )
        live = tuple(x for x in kept if x in frame["eligible"])
        key = (row["frame_id"], kept, tuple(sorted(rel)))
        check(key not in keys, "unique raw induced state")
        keys[key] = sid
        relations.append(rel)
        ranks.append((sum(x % 2 for x in live), sum(x % 2 == 0 for x in live)))
        internals.append(inside)
        eligible.append(live)
    targets = []
    for sid, row in enumerate(states):
        fixed = set(frames[row["frame_id"]]["fixed"])
        table = []
        for mask in range(1 << len(eligible[sid])):
            kept = tuple(sorted(fixed | {v for j, v in enumerate(eligible[sid]) if mask >> j & 1}))
            rel = tuple(sorted((a, b) for a, b in relations[sid] if a in kept and b in kept))
            key = row["frame_id"], kept, rel
            check(key in keys, "raw closure under all eligible subsets")
            table.append(keys[key])
        targets.append(table)
    COUNTS["raw_states"] = len(states)
    COUNTS["raw_subset_atoms"] = sum(map(len, targets))
    return relations, ranks, internals, eligible, targets


def raw_features(raw, relation, ranks, internals, eligible, targets):
    chain = []
    for sid, inside in enumerate(internals):
        row = []
        for q in range(4):
            row.append(
                sum(
                    all(
                        (a, b) in relation[sid] or (b, a) in relation[sid]
                        for a, b in itertools.combinations(selected, 2)
                    )
                    for selected in itertools.combinations(inside, q)
                )
            )
        chain.append(row)
    features, classes, assignment, key_ids = [], [], [], {}
    for sid, live in enumerate(eligible):
        n = len(live)
        # Recover support coefficients by Boolean-lattice Mobius inversion
        # of induced chain counts and raw count products, not pair unions.
        polynomials = []
        for q in range(4):
            polynomials.append([chain[t][q] for t in targets[sid]])
        for q in range(4):
            for r in range(4):
                polynomials.append([chain[t][q] * chain[t][r] for t in targets[sid]])
        for column in polynomials:
            for bit in range(n):
                for mask in range(1 << n):
                    if mask >> bit & 1:
                        column[mask] -= column[mask ^ (1 << bit)]
                        COUNTS["mobius_subtractions"] += 1
        grades = [
            (
                sum(live[j] % 2 for j in range(n) if mask >> j & 1),
                sum(live[j] % 2 == 0 for j in range(n) if mask >> j & 1),
            )
            for mask in range(1 << n)
        ]
        tables = []
        for column in polynomials:
            table = [[0] * 4 for _ in range(4)]
            for value, (o, e) in zip(column, grades):
                check(value >= 0, "Mobius support coefficient nonnegative")
                table[o][e] += value
            tables.append(table)
        D = tables[:4]
        B = [tables[4 + 4 * q : 8 + 4 * q] for q in range(4)]
        motif, path = [], []
        odd, even = [v for v in live if v % 2], [v for v in live if v % 2 == 0]
        for left in itertools.combinations(odd, 2):
            for right in itertools.combinations(even, 2):
                rel = relation[sid]
                if any((a, b) in rel or (b, a) in rel for a, b in (left, right)):
                    continue
                forward = sum((a, b) in rel for a in left for b in right)
                backward = sum((b, a) in rel for a in left for b in right)
                support = sorted(left + right)
                if (forward, backward) in ((4, 0), (0, 4)):
                    motif.append(support)
                if (forward, backward) in ((3, 0), (0, 3)):
                    path.append(support)
        feature = {
            "state_id": sid,
            "color_sizes": list(ranks[sid]),
            "chain_counts": chain[sid],
            "mean_graded": D,
            "pair_graded": B,
            "motif_supports": sorted(motif),
            "motif_count": len(motif),
            "path_supports": sorted(path),
            "path_count": len(path),
        }
        features.append(feature)
        frame = raw["frames"][raw["states"][sid]["frame_id"]]
        key = [[frame["density"], frame["fixed"], frame["eligible"]], B, len(motif), len(path)]
        frozen = canon(key)
        if frozen not in key_ids:
            key_ids[frozen] = len(classes)
            classes.append({"class_id": len(classes), "key": key, "members": []})
        cid = key_ids[frozen]
        assignment.append(cid)
        classes[cid]["members"].append(sid)
    return features, {"classes": classes, "state_classes": assignment}


def build_model(raw, features, partition, ranks, eligible, targets):
    assignment = partition["state_classes"]
    classes, labels, profiles, raw_local = [], [], [], []
    for sid, row in enumerate(raw["states"]):
        n = len(eligible[sid])
        deleted = [defaultdict(int), defaultdict(int)]
        for bit, vertex in enumerate(eligible[sid]):
            target = targets[sid][((1 << n) - 1) ^ (1 << bit)]
            deleted[0 if vertex % 2 else 1][assignment[target]] += 1
        raw_local.append(
            {
                "state_id": sid,
                "frame_id": row["frame_id"],
                "parent_color_sizes": list(ranks[sid]),
                "odd": [
                    {"target_class": h, "multiplicity": x} for h, x in sorted(deleted[0].items())
                ],
                "even": [
                    {"target_class": h, "multiplicity": x} for h, x in sorted(deleted[1].items())
                ],
            }
        )
    for group in partition["classes"]:
        h, sid = group["class_id"], group["members"][0]
        row = {k: v for k, v in raw_local[sid].items() if k != "state_id"}
        row["class_id"] = h
        classes.append(row)
        label = [raw["states"][sid]["frame_id"]] + features[sid]["chain_counts"]
        labels.append(
            {
                "class_id": h,
                "observation": label,
                "question": label + [features[sid]["motif_count"], features[sid]["path_count"]],
            }
        )
        expected = None
        for member in group["members"]:
            local = {k: v for k, v in raw_local[member].items() if k != "state_id"}
            eq(local, {k: v for k, v in row.items() if k != "class_id"}, "all-member raw local row")
            counts = defaultdict(int)
            for target in targets[member]:
                counts[assignment[target]] += 1
            if expected is None:
                expected = dict(counts)
            eq(dict(counts), expected, "all-member full subset profile")
        profiles.append(
            {
                "class_id": h,
                "parent_color_sizes": list(ranks[sid]),
                "transitions": [
                    {
                        "target_class": k,
                        "retained_color_sizes": list(ranks[partition["classes"][k]["members"][0]]),
                        "multiplicity": count,
                    }
                    for k, count in sorted(expected.items())
                ],
            }
        )
    return {"classes": classes, "labels": labels}, profiles, raw_local


def raw_kernel(sid, rates, eligible, targets):
    out = defaultdict(F)
    for mask, target in enumerate(targets[sid]):
        p = F(1)
        for bit, vertex in enumerate(eligible[sid]):
            rate = rates[0 if vertex % 2 else 1]
            p *= rate if mask >> bit & 1 else 1 - rate
        add(out, target, p)
    eq(sum(out.values(), F(0)), F(1), "raw K3 row mass")
    return dict(out)


def kernel_audit(case_rates, model, profiles, partition, eligible, targets, labels):
    kernels, raw_kernels = {}, {}
    assignment = partition["state_classes"]
    for rates in sorted(set(case_rates)):
        raw_rows = [raw_kernel(sid, rates, eligible, targets) for sid in range(len(targets))]
        rows, qrows = [], []
        for group in partition["classes"]:
            expected = None
            for sid in group["members"]:
                pushed = defaultdict(F)
                for target, p in raw_rows[sid].items():
                    add(pushed, assignment[target], p)
                if expected is None:
                    expected = dict(pushed)
                eq(dict(pushed), expected, "all-member fixed K3 H law")
                COUNTS["raw_K3_rows"] += 1
            profile = profiles[group["class_id"]]
            O, E = profile["parent_color_sizes"]
            by_profile = {}
            for atom in profile["transitions"]:
                o, e = atom["retained_color_sizes"]
                p = (
                    atom["multiplicity"]
                    * rates[0] ** o
                    * (1 - rates[0]) ** (O - o)
                    * rates[1] ** e
                    * (1 - rates[1]) ** (E - e)
                )
                if p:
                    by_profile[atom["target_class"]] = p
            eq(expected, by_profile, "raw subset / class profile K3 law")
            rows.append(expected)
            q = defaultdict(F)
            for h, p in expected.items():
                add(q, tuple(model["labels"][h]["question"]), p)
            qrows.append(dict(q))
        kernels[rates] = (rows, qrows)
        raw_kernels[rates] = raw_rows
    return kernels, raw_kernels


def lifetime_histories(case, raw, features, partition, eligible, targets):
    rates = [[rat(x) for x in row] for row in case["rates"]]
    # L=0,1,2,3: first missing stage, with 3 meaning survives all stages.
    # One independent categorical draw per initial eligible vertex replaces
    # nested state transitions and independently generates S1,S2,S3 jointly.
    histories, first, after_first, after_second, after_third = (
        {},
        defaultdict(F),
        defaultdict(F),
        defaultdict(F),
        defaultdict(F),
    )
    for atom in case["raw_prior"]:
        initial, prior = atom["state_id"], rat(atom["probability"])
        probs = []
        for vertex in eligible[initial]:
            color = 0 if vertex % 2 else 1
            a, b, c = (row[color] for row in rates)
            probs.append((1 - a, a * (1 - b), a * b * (1 - c), a * b * c))
        for life in itertools.product(range(4), repeat=len(probs)):
            COUNTS["vertex_lifetime_assignments"] += 1
            p = prior * math.prod(probs[j][duration] for j, duration in enumerate(life))
            if not p:
                continue
            masks = [
                sum(1 << j for j, duration in enumerate(life) if duration >= stage)
                for stage in (1, 2, 3)
            ]
            s1, s2, s3 = [targets[initial][mask] for mask in masks]
            n1 = (raw["states"][s1]["frame_id"], *features[s1]["chain_counts"])
            n2 = (raw["states"][s2]["frame_id"], *features[s2]["chain_counts"])
            q3 = (
                raw["states"][s3]["frame_id"],
                *features[s3]["chain_counts"],
                features[s3]["motif_count"],
                features[s3]["path_count"],
            )
            joint = histories.setdefault((n1, n2), defaultdict(F))
            add(joint, (s2, q3), p)
            add(first, n1, p)
            add(after_first, partition["state_classes"][s1], p)
            add(after_second, partition["state_classes"][s2], p)
            add(after_third, partition["state_classes"][s3], p)
    eq(sum(first.values(), F(0)), F(1), "lifetime total mass")
    u = case["u_analysis"]
    eq(
        [tuple(map(tuple, x["observations"])) for x in u["histories"]],
        sorted(histories),
        "complete U history support/order",
    )
    normalized = []
    for row, (history, joint) in zip(u["histories"], sorted(histories.items())):
        weight = sum(joint.values(), F(0))
        normalized.append({key: value / weight for key, value in joint.items()})
        posterior, prediction = defaultdict(F), defaultdict(F)
        for (sid, q), p in joint.items():
            add(posterior, partition["state_classes"][sid], p / weight)
            add(prediction, q, p / weight)
        eq(row["likelihood"], wire(weight), "U history likelihood from lifetimes")
        eq(
            row["conditional_likelihood"],
            wire(weight / first[history[0]]),
            "U conditional history likelihood",
        )
        eq(row["posterior"], post_wire(posterior), "U current posterior from lifetimes")
        eq(row["prediction"], law_wire(prediction), "U future law from lifetimes")
    eq(u["unconditional"]["after_first"], post_wire(after_first), "U unconditional first law")
    eq(u["unconditional"]["after_second"], post_wire(after_second), "U unconditional current law")
    eq(u["unconditional"]["after_third"], post_wire(after_third), "U unconditional final law")
    return normalized


def make_cells(joint, observation, partition, channel=None):
    current, future = {}, {}
    for (sid, q), mass in joint.items():
        label = observation[sid]
        row = {label: F(1)} if channel is None else channel[label]
        for value, likelihood in row.items():
            add(
                current.setdefault(value, defaultdict(F)),
                partition["state_classes"][sid],
                mass * likelihood,
            )
            add(future.setdefault(value, defaultdict(F)), q, mass * likelihood)
    cells = {}
    for value in sorted(current):
        w = sum(current[value].values(), F(0))
        eq(sum(future[value].values(), F(0)), w, "raw noisy current/future joint row mass")
        post, pred = (
            {h: p / w for h, p in current[value].items()},
            {q: p / w for q, p in future[value].items()},
        )
        r = risk(pred)
        # Two replicas conditional on the SAME report, with denominator w^2.
        paired = sum((p * (w - p) / (w * w) for p in future[value].values()), F(0))
        eq(r, paired, "conditional two-replica normalization")
        cells[value] = {
            "value": list(value),
            "probability": wire(w),
            "posterior": post_wire(post),
            "prediction": law_wire(pred),
            "risk": wire(r),
        }
    eq(sum((rat(c["probability"]) for c in cells.values()), F(0)), F(1), "noisy cell masses")
    return cells


def expected_risk(cells):
    return sum((rat(c["probability"]) * rat(c["risk"]) for c in cells.values()), F(0))


def mixture(cells, weights, field):
    result = defaultdict(F)
    atom_field = "class_id" if field == "posterior" else "value"
    for value, weight in weights.items():
        for key, p in parse_law(cells[value][field], atom_field).items():
            add(result, key, weight * p)
    return post_wire(result) if field == "posterior" else law_wire(result)


def distance(left, right):
    return sum(
        ((left.get(q, F(0)) - right.get(q, F(0))) ** 2 for q in left.keys() | right.keys()), F(0)
    )


def family_from_model(model):
    alphabet = {}
    for row in model["labels"]:
        alphabet.setdefault(tuple(row["observation"]), set()).add(tuple(row["question"]))
    alphabet = {n: sorted(values) for n, values in sorted(alphabet.items())}
    channels = []
    for level in LEVELS:
        channel = {}
        for values in alphabet.values():
            for source in values:
                channel[source] = {
                    target: p
                    for target in values
                    if (p := (1 - level) * int(source == target) + level / len(values))
                }
                eq(sum(channel[source].values(), F(0)), F(1), "global report row mass")
        channels.append(channel)

    def rows_wire(rows):
        return [
            {
                "source": list(source),
                "transitions": [
                    {"value": list(target), "probability": wire(p)}
                    for target, p in sorted(row.items())
                ],
            }
            for source, row in sorted(rows.items())
        ]

    checks = []
    for i, d in enumerate((channels[1], channels[1], channels[3])):
        result, products = {}, 0
        for source, first in channels[i].items():
            final = defaultdict(F)
            for middle, p in first.items():
                for target, r in d[middle].items():
                    add(final, target, p * r)
                    products += 1
            result[source] = dict(final)
        eq(result, channels[i + 1], "full-model channel multiplication")
        checks.append(
            {
                "from_index": i,
                "to_index": i + 1,
                "garbling_level": wire(GARB[i]),
                "row_comparisons": len(result),
                "product_terms": products,
                "positive_composed_atoms": sum(map(len, result.values())),
                "composed_sha256": digest(rows_wire(result)),
                "exact": True,
            }
        )
    output = {
        "alphabet": [
            {"N": list(n), "values": [list(x) for x in values]} for n, values in alphabet.items()
        ],
        "channels": [
            {"level": wire(level), "rows": rows_wire(rows)} for level, rows in zip(LEVELS, channels)
        ],
        "composition_checks": checks,
    }
    return alphabet, channels, output


def score_fraction(pair):
    check(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "native score pair",
    )
    n, d = pair
    check(0 <= n <= 2 * d and d > 0 and math.gcd(n, d) == 1, "canonical score in [0,2]")
    check(max(n.bit_length(), d.bit_length()) <= 4096, "retained score bits")
    return F(n, d)


def explicit_scores(truth, forecast):
    """Literal outcome-by-coordinate loss, distinct from both linear cores."""
    alphabet = sorted(truth.keys() | forecast.keys())
    loss = F(0)
    for actual, mass in truth.items():
        conditional = F(0)
        for coordinate in alphabet:
            conditional += (forecast.get(coordinate, F(0)) - int(actual == coordinate)) ** 2
            COUNTS["explicit_outcome_loss_coordinates"] += 1
        loss += mass * conditional
    regret = sum(((truth.get(q, F(0)) - forecast.get(q, F(0))) ** 2 for q in alphabet), F(0))
    bayes = risk(truth)
    eq(loss, bayes + regret, "explicit outcome loss / independently squared regret")
    eq(regret == 0, truth == forecast, "complete future-law zero regret")
    check(0 <= loss <= 2 and 0 <= regret <= 2, "actual loss and regret bounds")
    return loss, regret


def score_pair(actual, assumed, i, j):
    cells = []
    bayes_total = coverage = supported_bayes = supported_loss = supported_regret = F(0)
    terms = 0
    equalities = []
    for value, source in sorted(actual.items()):
        mass = rat(source["probability"])
        truth = parse_law(source["prediction"])
        bayes = risk(truth)
        bayes_total += mass * bayes
        supported = value in assumed
        loss = regret = equal = forecast = None
        assumed_mass = F(0)
        if supported:
            target = assumed[value]
            forecast = parse_law(target["prediction"])
            assumed_mass = rat(target["probability"])
            loss, regret = explicit_scores(truth, forecast)
            equal = truth == forecast
            coverage += mass
            supported_bayes += mass * bayes
            supported_loss += mass * loss
            supported_regret += mass * regret
            terms += len(truth) + len(forecast)
            equalities.append(equal)
        cells.append(
            {
                "value": list(value),
                "actual_probability": wire(mass),
                "assumed_probability": wire(assumed_mass),
                "actual_prediction": law_wire(truth),
                "forecast": law_wire(forecast) if supported else None,
                "bayes_risk": wire(bayes),
                "forecast_risk": wire(loss, 2) if supported else None,
                "regret": wire(regret, 2) if supported else None,
                "supported": supported,
                "predictions_equal": equal,
            }
        )
    missing = sum(
        (rat(cell["probability"]) for value, cell in actual.items() if value not in assumed), F(0)
    )
    eq(coverage + missing, F(1), "actual support mass partition")
    eq(
        supported_loss,
        supported_bayes + supported_regret,
        "unnormalized supported loss decomposition",
    )
    eq(supported_regret == 0, all(equalities), "supported zero regret iff all defined laws equal")
    check(
        0 <= supported_bayes <= coverage
        and 0 <= supported_loss <= 2 * coverage
        and 0 <= supported_regret <= 2 * coverage,
        "coverage-scaled supported score bounds",
    )
    complete = missing == 0
    if complete:
        eq(supported_bayes, bayes_total, "complete Bayes contribution")
        eq(supported_loss, bayes_total + supported_regret, "complete loss decomposition")
    return {
        "actual_index": i,
        "assumed_index": j,
        "cells": cells,
        "bayes_risk": wire(bayes_total),
        "coverage": wire(coverage),
        "unsupported_mass": wire(missing),
        "supported_bayes_risk": wire(supported_bayes),
        "supported_forecast_risk": wire(supported_loss, 2),
        "supported_regret": wire(supported_regret, 2),
        "forecast_risk": wire(supported_loss, 2) if complete else None,
        "regret": wire(supported_regret, 2) if complete else None,
        "complete": complete,
        "checks": {
            "mass_partition": True,
            "supported_decomposition": True,
            "full_decomposition": True if complete else None,
            "zero_regret_iff_equal": True,
        },
    }, terms


def expected_x(problem):
    native_tree(problem)
    rows, terms = [], 0
    eq(sum((rat(b["weight"]) for b in problem["beliefs"]), F(0)), F(1), "X input history weights")
    for bid, belief in enumerate(problem["beliefs"]):
        eq(belief["belief_id"], bid, "X input belief order")
        check(rat(belief["weight"]) > 0, "X positive history weight")
        channels, marginals = [], []
        for index, channel in enumerate(belief["channels"]):
            native_eq(channel["level"], wire(LEVELS[index]), "X input fixed level")
            mapped = {tuple(cell["value"]): cell for cell in channel["cells"]}
            eq(len(mapped), len(channel["cells"]), "X distinct report cells")
            eq(list(mapped), sorted(mapped), "X sorted report cells")
            eq(sum((rat(c["probability"]) for c in mapped.values()), F(0)), F(1), "X report masses")
            marginal = defaultdict(F)
            for cell in mapped.values():
                check(rat(cell["probability"]) > 0, "X positive report cells")
                for q, p in parse_law(cell["prediction"]).items():
                    add(marginal, q, rat(cell["probability"]) * p)
            marginals.append(dict(marginal))
            channels.append(mapped)
        eq(len(channels), 4, "X four experiments")
        for marginal in marginals:
            eq(marginal, marginals[0], "X shared complete future marginal")
        pairs = []
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                pair, count = score_pair(actual, assumed, i, j)
                pairs.append(pair)
                terms += count
        rows.append({"belief_id": bid, "weight": belief["weight"], "pairs": pairs})
    aggregate = []
    fields_to_average = (
        "bayes_risk",
        "coverage",
        "unsupported_mass",
        "supported_bayes_risk",
        "supported_forecast_risk",
        "supported_regret",
    )
    for index in range(16):
        summed = {
            field: sum(
                (rat(row["weight"]) * score_fraction(row["pairs"][index][field]) for row in rows),
                F(0),
            )
            for field in fields_to_average
        }
        complete_count = sum(row["pairs"][index]["complete"] for row in rows)
        incomplete_count = len(rows) - complete_count
        complete = incomplete_count == 0
        eq(
            summed["coverage"] == 1,
            complete,
            "aggregate complete iff every positive history complete",
        )
        eq(summed["coverage"] + summed["unsupported_mass"], F(1), "aggregate coverage partition")
        eq(
            summed["supported_forecast_risk"],
            summed["supported_bayes_risk"] + summed["supported_regret"],
            "aggregate supported decomposition",
        )
        all_equal = all(
            cell["predictions_equal"]
            for row in rows
            for cell in row["pairs"][index]["cells"]
            if cell["supported"]
        )
        eq(
            summed["supported_regret"] == 0,
            all_equal,
            "aggregate zero supported regret iff all supported laws equal",
        )
        check(
            summed["supported_bayes_risk"] <= summed["coverage"]
            and summed["supported_forecast_risk"] <= 2 * summed["coverage"]
            and summed["supported_regret"] <= 2 * summed["coverage"],
            "aggregate coverage-scaled bounds",
        )
        if complete:
            eq(
                summed["supported_bayes_risk"],
                summed["bayes_risk"],
                "aggregate full Bayes contribution",
            )
            eq(
                summed["supported_forecast_risk"],
                summed["bayes_risk"] + summed["supported_regret"],
                "aggregate full decomposition",
            )
        aggregate.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                **{
                    field: wire(
                        value, 2 if field in ("supported_forecast_risk", "supported_regret") else 1
                    )
                    for field, value in summed.items()
                },
                "forecast_risk": wire(summed["supported_forecast_risk"], 2) if complete else None,
                "regret": wire(summed["supported_regret"], 2) if complete else None,
                "complete": complete,
                "checks": {
                    "mass_partition": True,
                    "supported_decomposition": True,
                    "full_decomposition": True if complete else None,
                    "zero_regret_iff_equal": True,
                },
                "complete_beliefs": complete_count,
                "incomplete_beliefs": incomplete_count,
            }
        )

    def first(index, predicate):
        return next((row["belief_id"] for row in rows if predicate(row["pairs"][index])), None)

    counts = {
        "beliefs": len(rows),
        "input_cells": sum(
            len(ch["cells"]) for belief in problem["beliefs"] for ch in belief["channels"]
        ),
        "input_prediction_atoms": sum(
            len(cell["prediction"])
            for belief in problem["beliefs"]
            for ch in belief["channels"]
            for cell in ch["cells"]
        ),
        "pair_cells": [sum(len(row["pairs"][i]["cells"]) for row in rows) for i in range(16)],
        "supported_pair_cells": [
            sum(cell["supported"] for row in rows for cell in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "unsupported_pair_cells": [
            sum(not cell["supported"] for row in rows for cell in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "scoring_terms": terms,
        "complete_beliefs": [row["complete_beliefs"] for row in aggregate],
        "incomplete_beliefs": [row["incomplete_beliefs"] for row in aggregate],
        "positive_supported_regret_beliefs": [
            sum(score_fraction(row["pairs"][i]["supported_regret"]) > 0 for row in rows)
            for i in range(16)
        ],
        "positive_full_regret_beliefs": [
            sum(
                row["pairs"][i]["complete"] and score_fraction(row["pairs"][i]["regret"]) > 0
                for row in rows
            )
            for i in range(16)
        ],
    }
    witnesses = {
        "first_incomplete": [first(i, lambda pair: not pair["complete"]) for i in range(16)],
        "first_positive_supported_regret": [
            first(i, lambda pair: score_fraction(pair["supported_regret"]) > 0) for i in range(16)
        ],
        "first_positive_full_regret": [
            first(i, lambda pair: pair["complete"] and score_fraction(pair["regret"]) > 0)
            for i in range(16)
        ],
    }
    COUNTS["X_scoring_support_terms"] += terms
    COUNTS["X_pair_cells"] += sum(counts["pair_cells"])
    return {
        "input_sha256": digest(problem),
        "levels": [wire(level) for level in LEVELS],
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": witnesses,
        "counts": counts,
    }


def raw_projection(case, raw, features, partition, eligible, targets, family):
    histories = lifetime_histories(case, raw, features, partition, eligible, targets)
    _, channels, channel_model = family
    N = [(raw["states"][sid]["frame_id"], *f["chain_counts"]) for sid, f in enumerate(features)]
    A = [(*N[sid], f["motif_count"], f["path_count"]) for sid, f in enumerate(features)]
    native_eq(
        channel_model["alphabet"],
        case["analysis"]["channel_model"]["alphabet"],
        "W whole-model distinct-label alphabet",
    )
    native_eq(
        channel_model["channels"],
        case["analysis"]["channel_model"]["channels"],
        "W fixed report channels",
    )
    beliefs, controls = [], []
    for bid, (joint, urow) in enumerate(zip(histories, case["u_analysis"]["histories"])):
        old = case["analysis"]["beliefs"][bid]
        native_eq(old["belief_id"], bid, "W received-history row order")
        native_eq(old["weight"], urow["likelihood"], "W received-history likelihood")
        n_cells = make_cells(joint, N, partition)
        noisy = [make_cells(joint, A, partition, channel) for channel in channels]
        for actual_index, actual_cells in enumerate(noisy):
            for assumed_index, assumed_cells in enumerate(noisy):
                for value, cell in actual_cells.items():
                    if value not in assumed_cells:
                        check(
                            actual_index > 0 and assumed_index == 0,
                            "W missing-label family premise",
                        )
                        parent = n_cells[value[:5]]
                        native_eq(
                            cell["posterior"],
                            parent["posterior"],
                            "unsupported W full current posterior equals N conditional",
                        )
                        native_eq(
                            cell["prediction"],
                            parent["prediction"],
                            "unsupported W full future law equals N conditional",
                        )
                        COUNTS["W_unsupported_posterior_and_future_checks"] += 1
        n_risk = expected_risk(n_cells)
        native_eq(
            list(n_cells.values()),
            old["controls"]["N"]["cells"],
            "W deterministic N cells from raw lifetimes",
        )
        native_eq(
            wire(n_risk), old["controls"]["N"]["expected_risk"], "W N risk from raw lifetimes"
        )
        projected, risks = [], []
        for index, cells in enumerate(noisy):
            native_eq(
                list(cells.values()),
                old["channels"][index]["cells"],
                "W full noisy cells from raw lifetimes",
            )
            native_eq(wire(LEVELS[index]), old["channels"][index]["level"], "W fixed level order")
            r = expected_risk(cells)
            risks.append(wire(r))
            native_eq(
                wire(r),
                old["channels"][index]["expected_risk"],
                "W noisy conditional expected risk",
            )
            projected.append(
                {
                    "level": wire(LEVELS[index]),
                    "cells": [
                        {
                            "value": cell["value"],
                            "probability": cell["probability"],
                            "prediction": cell["prediction"],
                        }
                        for cell in cells.values()
                    ],
                }
            )
        beliefs.append({"belief_id": bid, "weight": urow["likelihood"], "channels": projected})
        controls.append(
            {
                "weight": urow["likelihood"],
                "N_risk": wire(n_risk),
                "channel_risks": risks,
                "N_cells": list(n_cells.values()),
            }
        )
        COUNTS["raw_history_beliefs"] += 1
        COUNTS["raw_noisy_cells"] += sum(map(len, noisy))
    return {
        "schema_version": "det8-qr05x-problem-v1",
        "family": "qr05x_noise_misspecification",
        "beliefs": beliefs,
    }, controls


def producer_controls(analysis, raw_controls):
    for row, control in zip(analysis["beliefs"], raw_controls):
        native_eq(row["weight"], control["weight"], "X raw history weights")
        for i in range(4):
            diagonal = row["pairs"][5 * i]
            native_eq(diagonal["complete"], True, "X diagonal defined")
            native_eq(diagonal["regret"], [0, 1], "X diagonal zero regret")
            native_eq(
                diagonal["forecast_risk"],
                control["channel_risks"][i],
                "X diagonal equals raw W Bayes risk",
            )
            for j in (1, 2, 3):
                native_eq(
                    row["pairs"][4 * i + j]["complete"],
                    True,
                    "W positive assumed noise covers actual reports",
                )
            native_eq(
                row["pairs"][4 * i + 3]["forecast_risk"],
                control["N_risk"],
                "W full replacement forecast has raw N risk",
            )
    for i in range(4):
        weighted_diagonal = sum(
            (rat(c["weight"]) * rat(c["channel_risks"][i]) for c in raw_controls), F(0)
        )
        weighted_N = sum((rat(c["weight"]) * rat(c["N_risk"]) for c in raw_controls), F(0))
        native_eq(
            analysis["aggregate"]["pairs"][5 * i]["forecast_risk"],
            wire(weighted_diagonal),
            "case diagonal raw W risk",
        )
        native_eq(
            analysis["aggregate"]["pairs"][4 * i + 3]["forecast_risk"],
            wire(weighted_N),
            "case full replacement raw N risk",
        )
    # The last flag describes the separate capture runner, not this raw audit.
    return {
        "W_laws_are_declared_pinned_dependencies": True,
        "complete_projection_checked": True,
        "diagonal_W_risks_equal": True,
        "positive_assumed_noise_covers_actual_reports": True,
        "assumed_full_replacement_N_risk_equal": True,
        "W_channel_origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


X_FIELDS = (
    "coverage",
    "unsupported_mass",
    "bayes_risk",
    "supported_bayes_risk",
    "supported_forecast_risk",
    "supported_regret",
    "forecast_risk",
    "regret",
    "complete",
)
X_NUMERIC = X_FIELDS[:6]
Y_NUMERIC = (
    "fallback_bayes_risk",
    "fallback_forecast_risk",
    "fallback_regret",
    "completed_forecast_risk",
    "completed_regret",
    "coarse_forecast_risk",
    "coarse_regret",
    "gain_over_coarse",
)
Y_CHECKS = (
    "policy_total",
    "mass_partition",
    "split_decomposition",
    "completed_decomposition",
    "coarse_decomposition",
    "gain_identity",
    "supported_forecasts_preserved",
    "zero_regret_iff_equal",
)


def signed_wire(value):
    check(type(value) is F and -2 <= value <= 2, "signed gain range")
    check(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "signed retained component bits",
    )
    return [value.numerator, value.denominator]


def signed_fraction(pair):
    check(
        type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair),
        "signed native pair",
    )
    n, d = pair
    check(d > 0 and -2 * d <= n <= 2 * d and math.gcd(n, d) == 1, "signed reduced fraction")
    check(max(abs(n).bit_length(), d.bit_length()) <= 4096, "signed component bits")
    return F(n, d)


def y_identities(x, y, chosen_equal, coarse_equal, supported_gain):
    eq(x["coverage"] + x["unsupported_mass"], F(1), "Y support/fallback mass partition")
    eq(
        x["supported_forecast_risk"],
        x["supported_bayes_risk"] + x["supported_regret"],
        "Y unchanged supported decomposition",
    )
    eq(
        y["fallback_forecast_risk"],
        y["fallback_bayes_risk"] + y["fallback_regret"],
        "Y fallback decomposition",
    )
    eq(
        x["bayes_risk"],
        x["supported_bayes_risk"] + y["fallback_bayes_risk"],
        "Y Bayes contribution partition",
    )
    eq(
        y["completed_forecast_risk"],
        x["supported_forecast_risk"] + y["fallback_forecast_risk"],
        "Y completed branch losses",
    )
    eq(
        y["completed_regret"],
        x["supported_regret"] + y["fallback_regret"],
        "Y completed branch regrets",
    )
    eq(
        y["completed_forecast_risk"],
        x["bayes_risk"] + y["completed_regret"],
        "Y completed decomposition",
    )
    eq(y["coarse_forecast_risk"], x["bayes_risk"] + y["coarse_regret"], "Y coarse decomposition")
    eq(
        y["gain_over_coarse"],
        y["coarse_forecast_risk"] - y["completed_forecast_risk"],
        "Y risk gain",
    )
    eq(y["gain_over_coarse"], y["coarse_regret"] - y["completed_regret"], "Y regret gain")
    eq(y["gain_over_coarse"], supported_gain, "Y gain entirely from supported reports")
    check(abs(y["gain_over_coarse"]) <= 2 * x["coverage"], "Y coverage-scaled signed gain")
    eq(y["completed_regret"] == 0, chosen_equal, "Y completed zero regret iff full laws agree")
    eq(y["coarse_regret"] == 0, coarse_equal, "Y coarse zero regret iff full laws agree")
    for prefix, mass, table in (
        ("supported", x["coverage"], x),
        ("fallback", x["unsupported_mass"], y),
    ):
        check(
            0 <= table[prefix + "_bayes_risk"] <= mass
            and 0 <= table[prefix + "_forecast_risk"] <= 2 * mass
            and 0 <= table[prefix + "_regret"] <= 2 * mass,
            "Y unnormalized branch bounds",
        )


def y_x_wire(x):
    complete = x["coverage"] == 1
    return {
        **{
            key: wire(value, 2 if key in ("supported_forecast_risk", "supported_regret") else 1)
            for key, value in x.items()
        },
        "forecast_risk": wire(x["supported_forecast_risk"], 2) if complete else None,
        "regret": wire(x["supported_regret"], 2) if complete else None,
        "complete": complete,
    }


def y_numeric_wire(y):
    return {
        key: signed_wire(value)
        if key == "gain_over_coarse"
        else wire(value, 1 if key == "fallback_bayes_risk" else 2)
        for key, value in y.items()
    }


def score_y_pair(actual, assumed, fallbacks, i, j):
    x = {key: F(0) for key in X_NUMERIC}
    y = {key: F(0) for key in Y_NUMERIC}
    cells, chosen_flags, coarse_flags = [], [], []
    completed_terms = coarse_terms = 0
    supported_gain = F(0)
    for value, source in sorted(actual.items()):
        mass = rat(source["probability"])
        truth = parse_law(source["prediction"])
        coarse = fallbacks[value[:5]]
        supported = value in assumed
        forecast = parse_law(assumed[value]["prediction"]) if supported else coarse
        # Both policies are evaluated literally, even when they coincide.
        loss, regret = explicit_scores(truth, forecast)
        coarse_loss, coarse_regret = explicit_scores(truth, coarse)
        completed_terms += len(truth) + len(forecast)
        coarse_terms += len(truth) + len(coarse)
        bayes, gain = risk(truth), coarse_loss - loss
        eq(gain, coarse_regret - regret, "Y conditional gain identity")
        chosen_flags.append(truth == forecast)
        coarse_flags.append(truth == coarse)
        x["bayes_risk"] += mass * bayes
        if supported:
            x["coverage"] += mass
            x["supported_bayes_risk"] += mass * bayes
            x["supported_forecast_risk"] += mass * loss
            x["supported_regret"] += mass * regret
            supported_gain += mass * gain
        else:
            x["unsupported_mass"] += mass
            y["fallback_bayes_risk"] += mass * bayes
            y["fallback_forecast_risk"] += mass * loss
            y["fallback_regret"] += mass * regret
            eq(gain, F(0), "Y fallback branch cannot change coarse comparator")
        y["completed_forecast_risk"] += mass * loss
        y["completed_regret"] += mass * regret
        y["coarse_forecast_risk"] += mass * coarse_loss
        y["coarse_regret"] += mass * coarse_regret
        y["gain_over_coarse"] += mass * gain
        cells.append(
            {
                "value": list(value),
                "actual_probability": wire(mass),
                "assumed_probability": assumed[value]["probability"] if supported else [0, 1],
                "actual_prediction": law_wire(truth),
                "assumed_forecast": assumed[value]["prediction"] if supported else None,
                "coarse_forecast": law_wire(coarse),
                "forecast": law_wire(forecast),
                "supported": supported,
                "used_fallback": not supported,
                "bayes_risk": wire(bayes),
                "forecast_risk": wire(loss, 2),
                "regret": wire(regret, 2),
                "coarse_risk": wire(coarse_loss, 2),
                "coarse_regret": wire(coarse_regret, 2),
                "gain_over_coarse": signed_wire(gain),
                "predictions_equal": truth == forecast,
                "coarse_predictions_equal": truth == coarse,
            }
        )
    y_identities(x, y, all(chosen_flags), all(coarse_flags), supported_gain)
    return (
        {
            "actual_index": i,
            "assumed_index": j,
            "cells": cells,
            "x_scores": y_x_wire(x),
            **y_numeric_wire(y),
            "checks": dict.fromkeys(Y_CHECKS, True),
        },
        completed_terms,
        coarse_terms,
    )


def expected_y(problem, x_analysis):
    native_tree(problem)
    rows = []
    completed_terms = coarse_terms = 0
    for bid, belief in enumerate(problem["beliefs"]):
        channels = [
            {tuple(cell["value"]): cell for cell in channel["cells"]}
            for channel in belief["channels"]
        ]
        fallbacks = {
            tuple(row["value"]): parse_law(row["prediction"]) for row in belief["fallbacks"]
        }
        eq(len(fallbacks), len(belief["fallbacks"]), "Y distinct fallback keys")
        eq(list(fallbacks), sorted(fallbacks), "Y fallback key order")
        eq(
            set(fallbacks),
            {value[:5] for channel in channels for value in channel},
            "Y exact fallback prefix union",
        )
        pairs = []
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                pair, count_completed, count_coarse = score_y_pair(actual, assumed, fallbacks, i, j)
                completed_terms += count_completed
                coarse_terms += count_coarse
                native_eq(
                    pair["x_scores"],
                    {key: x_analysis["beliefs"][bid]["pairs"][4 * i + j][key] for key in X_FIELDS},
                    "Y independently preserves complete X score projection",
                )
                pairs.append(pair)
        rows.append({"belief_id": bid, "weight": belief["weight"], "pairs": pairs})
    aggregate = []
    for index in range(16):
        x = {
            key: sum(
                (
                    rat(row["weight"]) * score_fraction(row["pairs"][index]["x_scores"][key])
                    for row in rows
                ),
                F(0),
            )
            for key in X_NUMERIC
        }
        y = {
            key: sum(
                (
                    rat(row["weight"])
                    * (
                        signed_fraction(row["pairs"][index][key])
                        if key == "gain_over_coarse"
                        else score_fraction(row["pairs"][index][key])
                    )
                    for row in rows
                ),
                F(0),
            )
            for key in Y_NUMERIC
        }
        chosen_equal = all(
            cell["predictions_equal"] for row in rows for cell in row["pairs"][index]["cells"]
        )
        coarse_equal = all(
            cell["coarse_predictions_equal"]
            for row in rows
            for cell in row["pairs"][index]["cells"]
        )
        supported_gain = sum(
            (
                rat(row["weight"])
                * rat(cell["actual_probability"])
                * signed_fraction(cell["gain_over_coarse"])
                for row in rows
                for cell in row["pairs"][index]["cells"]
                if cell["supported"]
            ),
            F(0),
        )
        y_identities(x, y, chosen_equal, coarse_equal, supported_gain)
        complete = sum(row["pairs"][index]["x_scores"]["complete"] for row in rows)
        eq(x["coverage"] == 1, complete == len(rows), "Y original aggregate completeness")
        pair = {
            "actual_index": index // 4,
            "assumed_index": index % 4,
            "x_scores": y_x_wire(x),
            **y_numeric_wire(y),
            "checks": dict.fromkeys(Y_CHECKS, True),
            "complete_before_beliefs": complete,
            "incomplete_before_beliefs": len(rows) - complete,
        }
        native_eq(
            pair["x_scores"],
            {key: x_analysis["aggregate"]["pairs"][index][key] for key in X_FIELDS},
            "Y aggregate X score/null preservation",
        )
        aggregate.append(pair)

    def first(index, predicate):
        return next((row["belief_id"] for row in rows if predicate(row["pairs"][index])), None)

    witnesses = {
        "first_fallback": [
            first(i, lambda p: rat(p["x_scores"]["unsupported_mass"]) > 0) for i in range(16)
        ],
        "first_positive_fallback_regret": [
            first(i, lambda p: score_fraction(p["fallback_regret"]) > 0) for i in range(16)
        ],
        "first_positive_completed_regret": [
            first(i, lambda p: score_fraction(p["completed_regret"]) > 0) for i in range(16)
        ],
        "first_better_than_coarse": [
            first(i, lambda p: signed_fraction(p["gain_over_coarse"]) > 0) for i in range(16)
        ],
        "first_equal_to_coarse": [
            first(i, lambda p: signed_fraction(p["gain_over_coarse"]) == 0) for i in range(16)
        ],
        "first_worse_than_coarse": [
            first(i, lambda p: signed_fraction(p["gain_over_coarse"]) < 0) for i in range(16)
        ],
    }
    counts = {
        "beliefs": len(rows),
        "input_cells": sum(
            len(ch["cells"]) for belief in problem["beliefs"] for ch in belief["channels"]
        ),
        "input_prediction_atoms": sum(
            len(cell["prediction"])
            for belief in problem["beliefs"]
            for ch in belief["channels"]
            for cell in ch["cells"]
        ),
        "input_fallbacks": sum(len(b["fallbacks"]) for b in problem["beliefs"]),
        "input_fallback_atoms": sum(
            len(f["prediction"]) for b in problem["beliefs"] for f in b["fallbacks"]
        ),
        "pair_cells": [sum(len(row["pairs"][i]["cells"]) for row in rows) for i in range(16)],
        "supported_pair_cells": [
            sum(c["supported"] for row in rows for c in row["pairs"][i]["cells"]) for i in range(16)
        ],
        "fallback_pair_cells": [
            sum(c["used_fallback"] for row in rows for c in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "completed_scoring_terms": completed_terms,
        "coarse_scoring_terms": coarse_terms,
        "complete_before_beliefs": [p["complete_before_beliefs"] for p in aggregate],
        "incomplete_before_beliefs": [p["incomplete_before_beliefs"] for p in aggregate],
        "positive_fallback_regret_beliefs": [
            sum(score_fraction(row["pairs"][i]["fallback_regret"]) > 0 for row in rows)
            for i in range(16)
        ],
        "positive_completed_regret_beliefs": [
            sum(score_fraction(row["pairs"][i]["completed_regret"]) > 0 for row in rows)
            for i in range(16)
        ],
        "better_than_coarse_beliefs": [
            sum(signed_fraction(row["pairs"][i]["gain_over_coarse"]) > 0 for row in rows)
            for i in range(16)
        ],
        "equal_to_coarse_beliefs": [
            sum(signed_fraction(row["pairs"][i]["gain_over_coarse"]) == 0 for row in rows)
            for i in range(16)
        ],
        "worse_than_coarse_beliefs": [
            sum(signed_fraction(row["pairs"][i]["gain_over_coarse"]) < 0 for row in rows)
            for i in range(16)
        ],
    }
    COUNTS["Y_pair_cells"] += sum(counts["pair_cells"])
    COUNTS["Y_completed_support_terms"] += completed_terms
    COUNTS["Y_coarse_support_terms"] += coarse_terms
    return {
        "input_sha256": digest(problem),
        "levels": [wire(level) for level in LEVELS],
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": witnesses,
        "counts": counts,
    }


def y_producer_controls(analysis, x_analysis, raw_controls):
    for row, old, raw in zip(analysis["beliefs"], x_analysis["beliefs"], raw_controls):
        native_eq(row["belief_id"], old["belief_id"], "Y unchanged X belief ID")
        native_eq(row["weight"], old["weight"], "Y unchanged X history likelihood")
        n_cells = {tuple(c["value"]): c for c in raw["N_cells"]}
        for index, (pair, xp) in enumerate(zip(row["pairs"], old["pairs"])):
            native_eq(
                pair["x_scores"],
                {key: xp[key] for key in X_FIELDS},
                "Y original X scores/nulls unchanged",
            )
            native_eq(
                pair["coarse_forecast_risk"],
                raw["N_risk"],
                "Y coarse risk equals independently raw N risk",
            )
            native_eq(pair["fallback_regret"], [0, 1], "W family predicted zero fallback regret")
            native_eq(
                pair["completed_regret"],
                xp["supported_regret"],
                "W completion regret equals X supported regret",
            )
            eq(
                score_fraction(pair["completed_forecast_risk"]),
                score_fraction(xp["supported_forecast_risk"])
                + rat(xp["bayes_risk"])
                - rat(xp["supported_bayes_risk"]),
                "W completion loss identity",
            )
            eq(len(pair["cells"]), len(xp["cells"]), "Y all X actual cells retained")
            for cell, xcell in zip(pair["cells"], xp["cells"]):
                for key in (
                    "value",
                    "actual_probability",
                    "assumed_probability",
                    "actual_prediction",
                    "supported",
                ):
                    native_eq(cell[key], xcell[key], "Y X cell input retained " + key)
                native_eq(
                    cell["assumed_forecast"],
                    xcell["forecast"],
                    "Y original assumed forecast retained",
                )
                native_eq(
                    cell["coarse_forecast"],
                    n_cells[tuple(cell["value"][:5])]["prediction"],
                    "Y declared fallback derived from raw N law",
                )
                if cell["used_fallback"]:
                    native_eq(
                        cell["actual_prediction"],
                        cell["forecast"],
                        "W fallback full future law equals actual",
                    )
                    native_eq(cell["regret"], [0, 1], "W fallback regret identity")
                    native_eq(cell["gain_over_coarse"], [0, 1], "W fallback local gain identity")
                else:
                    native_eq(cell["forecast"], xcell["forecast"], "Y supported forecast unchanged")
                    native_eq(
                        cell["forecast_risk"], xcell["forecast_risk"], "Y supported risk unchanged"
                    )
                    native_eq(cell["regret"], xcell["regret"], "Y supported regret unchanged")
            if index // 4 == index % 4:
                native_eq(pair["completed_regret"], [0, 1], "Y Bayes-correct diagonal")
            if xp["complete"]:
                native_eq(
                    pair["completed_forecast_risk"],
                    xp["forecast_risk"],
                    "Y original complete risk unchanged",
                )
                native_eq(
                    pair["completed_regret"], xp["regret"], "Y original complete regret unchanged"
                )
    n_mean = sum((rat(row["weight"]) * rat(row["N_risk"]) for row in raw_controls), F(0))
    for pair, xp in zip(analysis["aggregate"]["pairs"], x_analysis["aggregate"]["pairs"]):
        native_eq(
            pair["x_scores"], {key: xp[key] for key in X_FIELDS}, "Y aggregate X preservation"
        )
        native_eq(pair["coarse_forecast_risk"], wire(n_mean), "Y aggregate raw N risk")
        native_eq(pair["fallback_regret"], [0, 1], "Y aggregate W zero fallback regret")
        native_eq(
            pair["completed_regret"], xp["supported_regret"], "Y aggregate W completion regret"
        )
    return {
        "X_laws_and_W_N_fallbacks_are_declared_dependencies": True,
        "complete_original_X_scores_and_nulls_preserved": True,
        "supported_forecasts_and_scores_preserved": True,
        "W_fallback_future_laws_equal_actual": True,
        "W_fallback_regret_zero": True,
        "W_completion_identity": True,
        "coarse_only_W_N_risk_equal": True,
        "channel_or_fallback_origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


def suite_totals(cases):
    totals = {
        "cases": len(cases),
        "analyze_calls": 2 * len(cases),
        "invalid_analyze_calls_rejected": 14,
    }
    for key, value in cases[0]["analysis"]["counts"].items():
        totals[key] = (
            [sum(case["analysis"]["counts"][key][i] for case in cases) for i in range(16)]
            if type(value) is list
            else sum(case["analysis"]["counts"][key] for case in cases)
        )
    return totals


def runtime_metadata(runtime):
    fields(
        runtime,
        "bytecode_cache executable isolated optimized platform python rss_high_water_at_suite_end rss_units scope suite_seconds",
        "runtime metadata",
    )
    native_eq(runtime["isolated"], True, "recorded isolated capture")
    check(
        type(runtime["optimized"]) is int and runtime["optimized"] in (0, 1),
        "recorded optimization metadata",
    )
    native_eq(runtime["executable"], str(ROOT / ".venv/bin/python"), "recorded executable")
    check(
        type(runtime["rss_units"]) is str and runtime["rss_units"] in ("bytes", "KiB"),
        "recorded RSS units",
    )
    native_eq(
        runtime["scope"],
        "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        "recorded runtime scope",
    )
    for key in ("bytecode_cache", "platform", "python"):
        check(type(runtime[key]) is str and bool(runtime[key]), "recorded runtime text " + key)
    cache = Path(runtime["bytecode_cache"])
    check(
        cache.is_absolute() and not cache.is_relative_to(ROOT), "recorded external bytecode cache"
    )
    check(
        type(runtime["rss_high_water_at_suite_end"]) is int
        and runtime["rss_high_water_at_suite_end"] >= 0,
        "recorded RSS metadata",
    )
    seconds = runtime["suite_seconds"]
    check(
        type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
        "recorded duration outside mathematical suite",
    )


def audit_capture(path=None):
    COUNTS.clear()
    started = time.monotonic()
    capture = Path(path) if path is not None else HERE / "results.json"
    check(capture.stat().st_size <= 64 * 1024 * 1024, "capture byte cap")
    before = ident(capture)
    data = capture.read_bytes()
    doc = json.loads(data)
    eq(canon(doc), data, "canonical Y envelope bytes")
    fields(doc, "schema_version runtime source_ledger prior_artifacts suite", "Y envelope")
    native_eq(doc["schema_version"], "det8-qr05y-results-v1", "Y schema")
    for key in ("suite", "source_ledger", "prior_artifacts"):
        native_tree(doc[key])
    names = [
        "README.md",
        "fallback.py",
        "reference_qr05y.py",
        "study.py",
        "test_qr05y.py",
        "test_capture.py",
        "audit_json.py",
    ]
    native_eq(sorted(doc["source_ledger"]), sorted(names), "seven exact Y source filenames")
    native_eq(ident(XDIR / "results.json"), X_ID, "prospectively pinned X artifact")
    native_eq(ident(WDIR / "results.json"), W_ID, "inherited pinned W artifact")
    xdata, wdata = (XDIR / "results.json").read_bytes(), (WDIR / "results.json").read_bytes()
    xdoc, wdoc = json.loads(xdata), json.loads(wdata)
    eq(canon(xdoc), xdata, "canonical inherited X envelope")
    eq(canon(wdoc), wdata, "canonical inherited W envelope")
    fields(xdoc, "schema_version runtime source_ledger prior_artifacts suite", "X envelope")
    native_eq(xdoc["schema_version"], "det8-qr05x-results-v1", "X producer schema")
    expected_priors = {**xdoc["prior_artifacts"], X_PRIOR: X_ID}
    native_eq(len(expected_priors), 29, "29-prior lineage size")
    native_eq(doc["prior_artifacts"], expected_priors, "exact Y inherited artifact lineage")
    native_eq(
        sorted(xdoc["source_ledger"]),
        sorted(
            [
                "README.md",
                "misspecification.py",
                "reference_qr05x.py",
                "study.py",
                "test_qr05x.py",
                "test_capture.py",
                "audit_json.py",
            ]
        ),
        "seven exact X producer source filenames",
    )
    native_eq(
        sorted(wdoc["source_ledger"]),
        sorted(
            [
                "README.md",
                "noisy_readout.py",
                "reference_qr05w.py",
                "study.py",
                "test_qr05w.py",
                "test_capture.py",
            ]
        ),
        "six exact W producer source filenames",
    )
    frozen = {HERE / name: record for name, record in doc["source_ledger"].items()}
    frozen.update({HERE.parent / name: record for name, record in expected_priors.items()})
    frozen.update({XDIR / name: record for name, record in xdoc["source_ledger"].items()})
    frozen.update({WDIR / name: record for name, record in wdoc["source_ledger"].items()})
    for source, record in frozen.items():
        native_eq(ident(source), record, "before source/prior identity " + str(source))
    xsuite, wsuite, suite = xdoc["suite"], wdoc["suite"], doc["suite"]
    raw = wsuite["raw_model"]
    rel, ranks, inside, eligible, targets = subset_ids(raw)
    features, partition = raw_features(raw, rel, ranks, inside, eligible, targets)
    sprior = json.loads((SDIR / "results.json").read_bytes())["suite"]["analysis"]
    native_eq(features, sprior["features"], "raw subset-Mobius feature reconstruction")
    native_eq(partition, sprior["partition"], "raw H fibers")
    model, profiles, local = build_model(raw, features, partition, ranks, eligible, targets)
    native_eq(model, wsuite["model"], "W model raw authentication")
    native_eq(local, sprior["local_rows"], "raw single-deletion class rows")
    kernel_audit(
        [tuple(rat(x) for x in case["rates"][2]) for case in wsuite["cases"]],
        model,
        profiles,
        partition,
        eligible,
        targets,
        features,
    )
    family = family_from_model(model)
    native_eq(
        [c["case_id"] for c in suite["cases"]],
        [c["case_id"] for c in xsuite["cases"]],
        "Y fixed experiment order from X",
    )
    native_eq(
        [c["case_id"] for c in xsuite["cases"]],
        [c["case_id"] for c in wsuite["cases"]],
        "X fixed experiment order from W",
    )
    expected_cases, expected_xcases = [], []
    for case, xcase, wcase in zip(suite["cases"], xsuite["cases"], wsuite["cases"]):
        xproblem, controls = raw_projection(
            wcase, raw, features, partition, eligible, targets, family
        )
        native_eq(xproblem, xcase["problem"], "full X projection from raw lifetime joints")
        xanalysis = expected_x(xproblem)
        native_eq(xanalysis, xcase["analysis"], "complete X scoring independently reconstructed")
        xcontrols = producer_controls(xanalysis, controls)
        native_eq(xcontrols, xcase["producer_controls"], "complete inherited X producer controls")
        expected_xcases.append(
            {
                "case_id": xcase["case_id"],
                "problem": xproblem,
                "analysis": xanalysis,
                "producer_controls": xcontrols,
            }
        )
        beliefs = []
        for xbelief, control in zip(xproblem["beliefs"], controls):
            fallbacks = [
                {"value": cell["value"], "prediction": cell["prediction"]}
                for cell in control["N_cells"]
            ]
            beliefs.append({**xbelief, "fallbacks": fallbacks})
        problem = {
            "schema_version": "det8-qr05y-problem-v1",
            "family": "qr05y_explicit_fallback",
            "beliefs": beliefs,
        }
        native_eq(problem, case["problem"], "entire Y input and raw N fallback table")
        analysis = expected_y(problem, xanalysis)
        native_eq(analysis, case["analysis"], "entire Y analysis from literal policy/coarse scores")
        ycontrols = y_producer_controls(analysis, xanalysis, controls)
        native_eq(ycontrols, case["producer_controls"], "entire Y producer controls")
        expected_cases.append(
            {
                "case_id": case["case_id"],
                "problem": problem,
                "analysis": analysis,
                "producer_controls": ycontrols,
            }
        )
    # Historical API counters are metadata, not APIs replayed by this audit.
    expected_xsuite = {
        "producer": {"artifact": W_PRIOR, **W_ID},
        "cases": expected_xcases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 14,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "noise_parameters_fitted": False,
            "fallback_forecasts_invented": False,
        },
        "totals": suite_totals(expected_xcases),
    }
    native_eq(xsuite, expected_xsuite, "complete X native canonical reporting closure")
    expected_suite = {
        "producer": {"artifact": X_PRIOR, **X_ID},
        "cases": expected_cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 14,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "fallback_rule_explicit": True,
            "fallback_optimized": False,
            "actual_level_used_to_select_forecast": False,
        },
        "totals": suite_totals(expected_cases),
    }
    native_eq(suite, expected_suite, "complete Y native canonical suite closure")
    runtime_metadata(doc["runtime"])
    runtime_metadata(xdoc["runtime"])
    for source, record in frozen.items():
        native_eq(ident(source), record, "after source/prior identity " + str(source))
    native_eq(ident(capture), before, "read-only Y artifact identity")
    analyses = [case["analysis"] for case in expected_cases]
    return {
        "status": "PASS",
        "artifact": before,
        "analysis_list": {"bytes": len(canon(analyses)), "sha256": digest(analyses)},
        "counts": dict(COUNTS),
        "seconds": time.monotonic() - started,
        "frozen_Y_sources": 7,
        "authenticated_X_sources": 7,
        "authenticated_W_sources": 6,
        "immutable_prior_artifacts": 29,
        "source_content_used_only_for_identity": True,
        "executor_runner_test_imports": False,
        "complete_native_canonical_X_and_Y_suites_checked": True,
        "unsupported_W_current_posteriors_and_future_laws_checked": True,
        "prior_public_APIs_and_broader_certificates_replayed": False,
        "inherited_fine_polynomial_digest": wsuite["raw_bridge"]["fine_sha256"],
        "fine_polynomial_digest_independently_rederived": False,
        "historical_API_and_runtime_counters_are_metadata_only": True,
        "route": "raw induction; subset-Mobius features/H; categorical vertex lifetimes; raw W N/noisy joint laws; unsupported full current/future equality; literal outcome-coordinate scores for both completed/coarse forecasts; complete X score/null preservation; full Y canonical reporting closure",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    print(json.dumps(audit_capture(args.artifact), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
