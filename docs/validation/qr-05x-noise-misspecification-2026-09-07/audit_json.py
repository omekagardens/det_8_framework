"""Independent stdlib JSON-only QR-05X raw-projection/scoring audit.

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
            {"weight": urow["likelihood"], "N_risk": wire(n_risk), "channel_risks": risks}
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


def audit_capture(path=None):
    COUNTS.clear()
    started = time.monotonic()
    capture = Path(path) if path is not None else HERE / "results.json"
    check(capture.stat().st_size <= 64 * 1024 * 1024, "capture byte cap")
    capture_before = ident(capture)
    data = capture.read_bytes()
    doc = json.loads(data)
    eq(canon(doc), data, "canonical capture envelope bytes")
    fields(doc, "schema_version runtime source_ledger prior_artifacts suite", "capture envelope")
    native_eq(doc["schema_version"], "det8-qr05x-results-v1", "X capture schema")
    native_tree(doc["suite"])
    native_tree(doc["source_ledger"])
    native_tree(doc["prior_artifacts"])
    source_names = [
        "README.md",
        "misspecification.py",
        "reference_qr05x.py",
        "study.py",
        "test_qr05x.py",
        "test_capture.py",
        "audit_json.py",
    ]
    native_eq(sorted(doc["source_ledger"]), sorted(source_names), "seven exact X source filenames")
    native_eq(ident(WDIR / "results.json"), W_ID, "prospectively pinned W artifact")
    wdoc = json.loads((WDIR / "results.json").read_bytes())
    expected_priors = {**wdoc["prior_artifacts"], W_PRIOR: W_ID}
    native_eq(len(expected_priors), 28, "28-prior lineage size")
    native_eq(doc["prior_artifacts"], expected_priors, "exact X inherited artifact lineage")
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
        "six exact W source filenames",
    )
    frozen = {HERE / name: record for name, record in doc["source_ledger"].items()}
    frozen.update({HERE.parent / name: record for name, record in expected_priors.items()})
    frozen.update({WDIR / name: record for name, record in wdoc["source_ledger"].items()})
    for source, record in frozen.items():
        native_eq(ident(source), record, "before source/prior identity " + str(source))
    wsuite, suite = wdoc["suite"], doc["suite"]
    raw = wsuite["raw_model"]
    rel, ranks, inside, eligible, targets = subset_ids(raw)
    features, partition = raw_features(raw, rel, ranks, inside, eligible, targets)
    sprior = json.loads((SDIR / "results.json").read_bytes())["suite"]["analysis"]
    native_eq(features, sprior["features"], "raw subset-Mobius feature reconstruction")
    native_eq(partition, sprior["partition"], "raw H fibers")
    model, profiles, local = build_model(raw, features, partition, ranks, eligible, targets)
    native_eq(model, wsuite["model"], "W model raw authentication")
    native_eq(local, sprior["local_rows"], "raw local single-deletion rows")
    # Direct raw fixed-rate rows authenticate the law; no prior constructor
    # or commuting-operator/minimality certificate is imported or replayed.
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
        [c["case_id"] for c in wsuite["cases"]],
        "six fixed experiment order",
    )
    expected_cases = []
    for case, old in zip(suite["cases"], wsuite["cases"]):
        problem, controls = raw_projection(old, raw, features, partition, eligible, targets, family)
        native_eq(problem, case["problem"], "entire X producer projection from raw lifetimes")
        analysis = expected_x(problem)
        native_eq(analysis, case["analysis"], "entire X analysis from explicit outcome losses")
        checked_controls = producer_controls(analysis, controls)
        native_eq(
            checked_controls, case["producer_controls"], "entire producer control certificate"
        )
        expected_cases.append(
            {
                "case_id": old["case_id"],
                "problem": problem,
                "analysis": analysis,
                "producer_controls": checked_controls,
            }
        )
    # Historical capture-runner API counters are checked metadata only;
    # this independent JSON-only audit never calls those public APIs.
    totals = {
        "cases": len(expected_cases),
        "analyze_calls": 2 * len(expected_cases),
        "invalid_analyze_calls_rejected": 14,
    }
    scalar_counts = ("beliefs", "input_cells", "input_prediction_atoms", "scoring_terms")
    for key in scalar_counts:
        totals[key] = sum(case["analysis"]["counts"][key] for case in expected_cases)
    for key in expected_cases[0]["analysis"]["counts"]:
        if key not in scalar_counts:
            totals[key] = [
                sum(case["analysis"]["counts"][key][i] for case in expected_cases)
                for i in range(16)
            ]
    expected_suite = {
        "producer": {"artifact": W_PRIOR, **W_ID},
        "cases": expected_cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 14,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "noise_parameters_fitted": False,
            "fallback_forecasts_invented": False,
        },
        "totals": totals,
    }
    native_eq(suite, expected_suite, "complete X canonical native suite closure")
    runtime = doc["runtime"]
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
        runtime["rss_units"] in ("bytes", "KiB") and type(runtime["rss_units"]) is str,
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
        "recorded duration metadata outside mathematical suite",
    )
    for source, record in frozen.items():
        native_eq(ident(source), record, "after source/prior identity " + str(source))
    native_eq(ident(capture), capture_before, "read-only X artifact identity")
    analyses = [case["analysis"] for case in expected_cases]
    return {
        "status": "PASS",
        "artifact": capture_before,
        "analysis_list": {"bytes": len(canon(analyses)), "sha256": digest(analyses)},
        "counts": dict(COUNTS),
        "seconds": time.monotonic() - started,
        "frozen_X_sources": 7,
        "authenticated_W_sources": 6,
        "immutable_prior_artifacts": 28,
        "source_content_used_only_for_identity": True,
        "executor_runner_test_imports": False,
        "complete_native_canonical_suite_and_envelope_checked": True,
        "prior_public_APIs_and_broader_certificates_replayed": False,
        "inherited_fine_polynomial_digest": wsuite["raw_bridge"]["fine_sha256"],
        "fine_polynomial_digest_independently_rederived": False,
        "historical_API_and_runtime_counters_are_metadata_only": True,
        "route": "raw induction; subset-Mobius chain-count moments; categorical vertex lifetimes; raw current/report/future joints; explicit actual-outcome/forecast-coordinate Brier losses; independent squared-law regret; complete native X output/reporting closure",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    print(json.dumps(audit_capture(args.artifact), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
