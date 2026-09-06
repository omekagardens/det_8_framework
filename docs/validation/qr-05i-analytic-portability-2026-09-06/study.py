"""QR-05I exact finite sampling capture and read-only replay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05i-results-v1"
BASE_COMMIT = "0f8d3ec4023cea5aac840cf19be692f0f2bbf5e8"
SOURCES = (
    "README.md",
    "analytic.py",
    "reference_qr05i.py",
    "study.py",
    "test_qr05i.py",
    "test_capture.py",
)
PRIORS = {
    "qr-05h-law-portability-2026-09-06/results.json": "e6d5f06d765ccca7a1da1cef15d12bc15a3287463ec3cce3732aab75af613b3a",
    "qr-05g-predictive-compression-2026-09-06/results.json": "62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74",
    "qr-01-quantum-records-2026-09-05/results.json": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05/results.json": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05/results.json": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05/results.json": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05/results.json": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05/results.json": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05/results.json": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05/results.json": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    "qr-05d-geometric-correspondence-2026-09-05/results-v2.json": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
    "qr-05f-two-stage-2026-09-06/results.json": "0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917",
    "qr-05e-sampling-aware-2026-09-06/results.json": "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def plain_bytes(path):
    require(path.is_file() and not path.is_symlink(), "input must be a plain file")
    return path.read_bytes()


def ledger():
    result = {}
    for name in SOURCES:
        raw = plain_bytes(HERE / name)
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def priors():
    result = {}
    for name, sha in PRIORS.items():
        raw = plain_bytes(HERE.parent / name)
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name)
    require(digest(raw) == PRIORS[name], "prior artifact changed")
    return json.loads(raw)


def load(name, filename):
    require(name not in sys.modules, "private study module collision")
    path = HERE / filename
    raw = plain_bytes(path)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


POLICIES = ("iid_half", "iid_color", "block_coin")
CANDIDATES = (
    "final_only",
    "policy_token",
    "tagged_policy",
    "counts_policy",
    "graded_policy",
    "tagged_graded",
    "unmarked_order",
    "marked_order",
    "full_record",
    "color_graded",
    "block_order",
    "color_order",
)
TARGETS = ("analytic_means", "analytic_counts")
H_TARGETS = tuple(p + "_" + q for p in POLICIES for q in ("means", "counts")) + (
    "menu_means",
    "menu_counts",
)
PAIRS = tuple(
    ("ferrers6", d)
    for d in ("independent", "parity_adaptive", "common_coin", "parity_hole", "first_pair")
) + (
    ("standard_example3", "independent"),
    ("chain6", "parity_adaptive"),
    ("chain6", "parity_hole"),
    ("chain6", "first_pair"),
    ("ferrers6_fixed", "independent"),
)
PREDICTIVE_PRIOR = "qr-05g-predictive-compression-2026-09-06/results.json"


def fixtures():
    return [{"schema_version": "det8-qr05i-problem-v1", "family": "qr05h_two_color"}]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"family": base["family"]},
        {"schema_version": base["schema_version"]},
        {**base, "extra": 1},
        *({**base, "family": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "schema_version": v} for v in (True, None, 1, [], "other")),
        {**base, "profile": "ferrers6"},
        {**base, "design": "independent"},
    ]


def current_kernel(design, s, u):
    if s & u != u:
        return F(0)
    if design == "common_coin":
        return F(1) if s == 0 else F(1, 2) if u in (0, s) else F(0)
    rate = (
        F(1 if s.bit_count() % 2 == 0 else 2, 3)
        if design == "parity_adaptive"
        else F(int(s.bit_count() % 2 == 0))
        if design == "parity_hole"
        else F(1, 2)
    )
    return rate ** u.bit_count() * (1 - rate) ** (s.bit_count() - u.bit_count())


def pushforward(observations, probabilities):
    atoms = {}
    for obs, p in zip(observations, probabilities, strict=True):
        if p:
            z = tuple(obs["chain_counts"])
            atoms[z] = atoms.get(z, F(0)) + p
    return [{"counts": list(z), "probability": str(atoms[z])} for z in sorted(atoms)]


def mean_from_law(law):
    return [
        str(sum((F(atom["probability"]) * atom["counts"][q] for atom in law), F(0)))
        for q in range(4)
    ]


def key_and_signatures(case, state, history):
    final = case["states"][history["final_mask"]]
    base = [
        [case["design"], case["density"], case["fixed"], case["eligible"]],
        final["kept"],
        final["past"],
    ]
    token, tag = state["policy_token"], state["tagged_present"]
    extra = [
        [],
        [token],
        [token, tag],
        [token, state["chain_counts"]],
        [token, state["graded_counts"]],
        [token, state["graded_counts"], tag],
        [token, state["unmarked_order"]],
        [token, state["marked_order"]],
        [state["kept"], state["past"]],
        [token, state["color_graded"]],
        [token, state["block_order"]],
        [token, state["color_order"]],
    ]
    keys = {n: base + tail for n, tail in zip(CANDIDATES, extra, strict=True)}
    signatures = {
        "analytic_means": state["mean_polynomials"],
        "analytic_counts": state["count_polynomials"],
    }
    return base, keys, signatures


def refines(rows, left, right):
    seen = {}
    for row in rows:
        a, b = row[left], row[right]
        if a in seen and seen[a] != b:
            return False
        seen[a] = b
    return True


GRID = (F(0), F(1, 3), F(2, 3), F(1))
AUDIT_POINTS = tuple(
    dict.fromkeys(
        [(x, y) for x in GRID for y in GRID]
        + [
            (F(1, 2), F(1, 2)),
            (F(1, 3), F(2, 3)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        ]
    )
)


def evaluate(table, x, y):
    return sum((F(c) * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row)), F(0))


def law_at(state, x, y):
    result = []
    for atom in state["count_polynomials"]:
        probability = evaluate(atom["coefficients"], x, y)
        require(probability >= 0, "negative evaluated probability")
        if probability:
            result.append({"counts": atom["counts"], "probability": str(probability)})
    require(sum((F(r["probability"]) for r in result), F(0)) == 1, "evaluated law normalization")
    return result


def block_law(state):
    atoms = {}
    for x, y in ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1))):
        corner = law_at(state, x, y)
        require(
            len(corner) == 1 and corner[0]["probability"] == "1", "corner law must be deterministic"
        )
        atom = tuple(corner[0]["counts"])
        atoms[atom] = atoms.get(atom, F(0)) + F(1, 4)
    return [{"counts": list(z), "probability": str(atoms[z])} for z in sorted(atoms)]


def subset_vector(case, state, x, y):
    result = []
    for observation in state["observations"]:
        probability = F(1)
        for bit, vertex in enumerate(case["eligible"]):
            if state["mask"] & (1 << bit):
                rate = x if vertex % 2 else y
                probability *= rate if observation["mask"] & (1 << bit) else 1 - rate
        result.append(probability)
    return result


def check_table(table):
    require(
        type(table) is list
        and len(table) == 4
        and all(type(row) is list and len(row) == 4 for row in table),
        "polynomial padding",
    )
    require(
        all(type(c) is int for row in table for c in row),
        "polynomial coefficients must be native integers",
    )


def check_analysis(a):
    require_same_wire(
        sorted(a),
        sorted(
            [
                "cases",
                "histories",
                "candidate_partitions",
                "target_partitions",
                "assessments",
                "candidate_refinement",
                "target_refinement",
                "counts",
            ]
        ),
        "analysis fields",
    )
    require(len(AUDIT_POINTS) == 22, "unique audit-point count")
    totals = {
        "cases": len(a["cases"]),
        "states": 0,
        "positive_states": 0,
        "observations": 0,
        "histories": len(a["histories"]),
        "positive_histories": 0,
        "zero_histories": 0,
        "candidates": len(CANDIDATES),
        "targets": len(TARGETS),
        "polynomial_atoms": 0,
        "polynomial_coefficient_cells": 0,
        "mean_coefficient_cells": 0,
    }
    expected_histories = []
    for ci, case in enumerate(a["cases"]):
        require((case["profile"], case["design"]) == PAIRS[ci], "case order")
        width = len(case["eligible"])
        require(len(case["states"]) == 1 << width, "state enumeration")
        require(
            sum((F(s["probability"]) for s in case["states"]), F(0)) == 1,
            "first-stage normalization",
        )
        for si, state in enumerate(case["states"]):
            require(state["mask"] == si, "state mask order")
            vertices = [v for j, v in enumerate(case["eligible"]) if si & (1 << j)]
            color_sizes = [sum(v % 2 == 1 for v in vertices), sum(v % 2 == 0 for v in vertices)]
            require_same_wire(state["color_sizes"], color_sizes, "eligible-only color sizes")
            omax, emax = color_sizes
            require(max(color_sizes) <= 3, "color degree frame")
            observations = state["observations"]
            require(
                [r["mask"] for r in observations] == [u for u in range(1 << width) if u & ~si == 0],
                "all nested masks",
            )
            require(all(r["chain_counts"][0] == 1 for r in observations), "N0")
            atoms = state["count_polynomials"]
            require(
                [r["counts"] for r in atoms]
                == [list(z) for z in sorted({tuple(r["chain_counts"]) for r in observations})],
                "attainable atom inventory",
            )
            for atom in atoms:
                require_same_wire(sorted(atom), ["coefficients", "counts"], "atom fields")
                table = atom["coefficients"]
                check_table(table)
                require(any(c for row in table for c in row), "identically zero atom")
                require(
                    all(
                        c == 0
                        for i, row in enumerate(table)
                        for j, c in enumerate(row)
                        if i > omax or j > emax
                    ),
                    "state color degree bound",
                )
            require(len(state["mean_polynomials"]) == 4, "mean table count")
            for table in state["mean_polynomials"]:
                check_table(table)
            for i in range(4):
                for j in range(4):
                    require(
                        sum(atom["coefficients"][i][j] for atom in atoms) == int(i == j == 0),
                        "coefficientwise probability normalization",
                    )
                    for q in range(4):
                        require(
                            sum(atom["counts"][q] * atom["coefficients"][i][j] for atom in atoms)
                            == state["mean_polynomials"][q][i][j],
                            "law-to-mean coefficient identity",
                        )
            require_same_wire(state["mean_polynomials"], state["color_graded"], "mean equals D")
            for q in range(4):
                require(
                    sum(sum(row) for row in state["color_graded"][q]) == state["chain_counts"][q],
                    "D row count",
                )
                for k in range(4):
                    require(
                        sum(
                            state["color_graded"][q][i][j]
                            for i in range(4)
                            for j in range(4)
                            if i + j == k
                        )
                        == state["graded_counts"][q][k],
                        "D-to-C grading",
                    )
            for x, y in AUDIT_POINTS:
                probabilities = subset_vector(case, state, x, y)
                require(sum(probabilities, F(0)) == 1, "subset-law normalization")
                law = law_at(state, x, y)
                require_same_wire(
                    law, pushforward(observations, probabilities), "independent subset evaluation"
                )
                require_same_wire(
                    mean_from_law(law),
                    [str(evaluate(t, x, y)) for t in state["mean_polynomials"]],
                    "evaluated mean identity",
                )
                if 0 < x < 1 and 0 < y < 1:
                    require(len(law) == len(atoms), "interior support must include every atom")
            block_law(state)
            totals["states"] += 1
            totals["positive_states"] += int(F(state["probability"]) > 0)
            totals["observations"] += len(observations)
            totals["polynomial_atoms"] += len(atoms)
            totals["polynomial_coefficient_cells"] += 16 * len(atoms)
            totals["mean_coefficient_cells"] += 64
            current_total = F(0)
            for obs in observations:
                conditional = current_kernel(case["design"], si, obs["mask"])
                current_total += conditional
                mass = conditional * F(state["probability"])
                h = a["histories"][len(expected_histories)]
                require_same_wire(
                    {
                        k: h[k]
                        for k in (
                            "history_id",
                            "case_index",
                            "stage1_mask",
                            "final_mask",
                            "conditional_probability",
                            "joint_probability",
                        )
                    },
                    {
                        "history_id": len(expected_histories),
                        "case_index": ci,
                        "stage1_mask": si,
                        "final_mask": obs["mask"],
                        "conditional_probability": str(conditional),
                        "joint_probability": str(mass),
                    },
                    "history identity and current kernel",
                )
                expected_histories.append(h)
                totals["positive_histories" if mass else "zero_histories"] += 1
                if not mass:
                    require_same_wire(
                        h["candidate_classes"],
                        {n: None for n in CANDIDATES},
                        "zero-history candidate exclusion",
                    )
                    require_same_wire(
                        h["target_classes"],
                        {n: None for n in TARGETS},
                        "zero-history target exclusion",
                    )
            require(current_total == 1, "current kernel normalization")
    require_same_wire(a["counts"], totals, "complete measured counts")
    require_same_wire(
        {
            k: totals[k]
            for k in (
                "cases",
                "states",
                "positive_states",
                "observations",
                "histories",
                "positive_histories",
                "zero_histories",
                "candidates",
                "targets",
            )
        },
        {
            "cases": 10,
            "states": 608,
            "positive_states": 510,
            "observations": 6804,
            "histories": 6804,
            "positive_histories": 3534,
            "zero_histories": 3270,
            "candidates": 12,
            "targets": 2,
        },
        "frozen universe",
    )
    require_same_wire(sorted(a["candidate_partitions"]), sorted(CANDIDATES), "candidate names")
    require_same_wire(sorted(a["target_partitions"]), sorted(TARGETS), "target names")
    audit_partitions(a, [h for h in a["histories"] if F(h["joint_probability"])])
    return {
        "distinct_points_per_state": len(AUDIT_POINTS),
        "state_point_checks": len(AUDIT_POINTS) * totals["states"],
        "coefficient_normalization_cells": 16 * totals["states"],
        "coefficient_mean_cells": 64 * totals["states"],
        "block_corner_checks": 4 * totals["states"],
    }


def audit_partitions(a, positive):
    expected = {name: [] for name in CANDIDATES + TARGETS}
    indices = {name: {} for name in expected}
    expected_rows = []
    # Cache the state-dependent strong signatures; histories are not expanded into triples.
    signature_cache = {}
    for history in positive:
        case = a["cases"][history["case_index"]]
        state = case["states"][history["stage1_mask"]]
        base, keys, sigs = key_and_signatures(case, state, history)
        cache_key = (history["case_index"], history["stage1_mask"])
        if cache_key not in signature_cache:
            signature_cache[cache_key] = {t: canonical(sigs[t]) for t in TARGETS}
        sigbytes = signature_cache[cache_key]
        row = {}
        for name in CANDIDATES + TARGETS:
            is_candidate = name in CANDIDATES
            key = canonical(keys[name]) if is_candidate else canonical(base) + sigbytes[name]
            if key not in indices[name]:
                cid = len(expected[name])
                indices[name][key] = cid
                entry = {"class_id": cid, "members": [], "joint_mass": F(0)}
                entry.update(
                    {"key": keys[name]} if is_candidate else {"base": base, "signature": sigs[name]}
                )
                expected[name].append(entry)
            cid = indices[name][key]
            entry = expected[name][cid]
            entry["members"].append(history["history_id"])
            entry["joint_mass"] += F(history["joint_probability"])
            row[name] = cid
        require_same_wire(
            history["candidate_classes"], {n: row[n] for n in CANDIDATES}, "candidate assignment"
        )
        require_same_wire(
            history["target_classes"], {n: row[n] for n in TARGETS}, "target assignment"
        )
        expected_rows.append(row)
    for name, entries in expected.items():
        require(sum(e["joint_mass"] for e in entries) == 10, "pooled mass is bookkeeping10")
        for entry in entries:
            entry["joint_mass"] = str(entry["joint_mass"])
        actual = a["candidate_partitions" if name in CANDIDATES else "target_partitions"][name]
        require_same_wire(actual, entries, "exact partition differs: " + name)
    require_same_wire(
        a["candidate_refinement"],
        [[refines(expected_rows, left, right) for right in CANDIDATES] for left in CANDIDATES],
        "candidate refinement",
    )
    require_same_wire(
        a["target_refinement"],
        [[refines(expected_rows, left, right) for right in TARGETS] for left in TARGETS],
        "target refinement",
    )
    for name in CANDIDATES:
        for target in TARGETS:
            representatives, first, joint_classes = {}, None, set()
            for history, row in zip(positive, expected_rows, strict=True):
                c, t = row[name], row[target]
                joint_classes.add((c, t))
                if c not in representatives:
                    representatives[c] = (t, history["history_id"])
                elif representatives[c][0] != t and first is None:
                    first = {
                        "left_history": representatives[c][1],
                        "right_history": history["history_id"],
                    }
            sufficient = refines(expected_rows, name, target)
            require(
                sufficient == (first is None) == (len(joint_classes) == len(expected[name])),
                "factorization/minimality",
            )
            require_same_wire(
                a["assessments"][name][target],
                {
                    "sufficient": sufficient,
                    "first_collision": first,
                    "common_refinement_classes": len(joint_classes),
                },
                "assessment witness/refinement",
            )


def comparison(rows, left, right):
    representatives, collision, common = {}, None, set()
    for h, a, b in rows:
        c, t = a[left], b[right]
        common.add((c, t))
        if c not in representatives:
            representatives[c] = (h, t)
        elif representatives[c][1] != t and collision is None:
            collision = {"left_history": representatives[c][0], "right_history": h}
    return {
        "refines": collision is None,
        "first_collision": collision,
        "common_refinement_classes": len(common),
    }


def prior_bridge(a):
    old_suite = prior_json("qr-05h-law-portability-2026-09-06/results.json")["suite"]
    old = old_suite["analysis"]
    require_same_wire(
        a["candidate_partitions"],
        old["candidate_partitions"],
        "all H candidate keys/members/masses",
    )
    require_same_wire(a["candidate_refinement"], old["candidate_refinement"], "H refinement")
    predictions_checked = 0
    for case, previous in zip(a["cases"], old["cases"], strict=True):
        require_same_wire(
            {k: v for k, v in case.items() if k != "states"},
            {k: v for k, v in previous.items() if k != "states"},
            "H source/frame",
        )
        for state, prior in zip(case["states"], previous["states"], strict=True):
            require_same_wire(
                {
                    k: v
                    for k, v in state.items()
                    if k not in ("color_sizes", "count_polynomials", "mean_polynomials")
                },
                {k: v for k, v in prior.items() if k not in ("predictions", "transports")},
                "H state/order/count/observation identity",
            )
            laws = {
                "iid_half": law_at(state, F(1, 2), F(1, 2)),
                "iid_color": law_at(state, F(1, 3), F(2, 3)),
                "block_coin": block_law(state),
            }
            for policy, law in laws.items():
                # Labeled probabilities are reconstructed from the supplied policy,
                # not recovered from the coarse count polynomials.
                if policy == "block_coin":
                    blocks = [
                        sum(
                            1 << bit
                            for bit, vertex in enumerate(case["eligible"])
                            if state["mask"] & (1 << bit) and vertex % 2 == parity
                        )
                        for parity in (1, 0)
                    ]
                    probabilities = [
                        F(
                            sum(
                                ((blocks[0] if coin & 1 else 0) | (blocks[1] if coin & 2 else 0))
                                == obs["mask"]
                                for coin in range(4)
                            ),
                            4,
                        )
                        for obs in state["observations"]
                    ]
                else:
                    rates = (F(1, 2), F(1, 2)) if policy == "iid_half" else (F(1, 3), F(2, 3))
                    probabilities = subset_vector(case, state, *rates)
                require_same_wire(
                    list(map(str, probabilities)),
                    prior["predictions"][policy]["probabilities"],
                    "supplied policy-to-H labeled probability vector",
                )
                require_same_wire(
                    pushforward(state["observations"], probabilities),
                    law,
                    "labeled policy and polynomial pushforward agree",
                )
                means = mean_from_law(law)
                require_same_wire(
                    law, prior["predictions"][policy]["count_law"], "polynomial-to-H count law"
                )
                require_same_wire(
                    means, prior["predictions"][policy]["count_mean"], "polynomial-to-H means"
                )
                coefficients = [
                    str(F((-1) ** q, 2 ** (q + 1) * 12**q) * F(means[q])) for q in range(4)
                ]
                require_same_wire(
                    coefficients,
                    prior["predictions"][policy]["coefficient_mean"],
                    "polynomial-to-H fixed coefficient means",
                )
                predictions_checked += 1
    rows, reverse = [], []
    for h, previous in zip(a["histories"], old["histories"], strict=True):
        require_same_wire(
            {k: v for k, v in h.items() if k != "target_classes"},
            {k: v for k, v in previous.items() if k != "target_classes"},
            "H complete history identity",
        )
        if F(h["joint_probability"]):
            rows.append((h["history_id"], h["target_classes"], previous["target_classes"]))
            reverse.append((h["history_id"], previous["target_classes"], h["target_classes"]))
    comparisons = {}
    for name in TARGETS:
        comparisons[name] = {}
        for prior in H_TARGETS:
            forward = comparison(rows, name, prior)
            backward = comparison(reverse, prior, name)
            comparisons[name][prior] = {
                "analytic_refines_prior": forward,
                "prior_refines_analytic": backward,
                "same_partition": forward["refines"] and backward["refines"],
            }
    mean_rows = [
        (h["history_id"], h["target_classes"], h["candidate_classes"])
        for h in a["histories"]
        if F(h["joint_probability"])
    ]
    mean_reverse = [(h, b, c) for h, c, b in mean_rows]
    require(
        comparison(mean_rows, "analytic_means", "color_graded")["refines"]
        and comparison(mean_reverse, "color_graded", "analytic_means")["refines"],
        "mean-polynomial iff color-graded membership",
    )
    require(
        all(
            comparisons["analytic_counts"][prior]["analytic_refines_prior"]["refines"]
            for prior in H_TARGETS
        ),
        "universal count laws refine every H question",
    )
    require(
        all(
            comparisons["analytic_means"][prior]["analytic_refines_prior"]["refines"]
            for prior in (
                "iid_half_means",
                "iid_color_means",
                "block_coin_means",
                "block_coin_counts",
                "menu_means",
            )
        ),
        "mean polynomials determine IID means and deterministic-corner mixture",
    )
    return {
        "H_artifact": "qr-05h-law-portability-2026-09-06/results.json",
        "H_predictions_reconstructed": predictions_checked,
        "H_labeled_vectors_checked_from_supplied_policy": predictions_checked,
        "H_states_matched": 608,
        "H_histories_matched": 6804,
        "H_candidate_partitions_matched": len(CANDIDATES),
        "analytic_mean_equals_color_graded_partition": True,
        "target_comparisons": comparisons,
        "prior_executors_imported": False,
        "prior_transports_recomputed": False,
        "prior_geometric_and_quantum_bridge": old_suite["prior_bridge"][
            "prior_geometric_and_quantum_bridge"
        ],
        "scope": "Pinned source/history identity and analytic specialization to H; no new quantum/geometric validation.",
    }


def find_history(a, case_index, mask):
    return next(
        h
        for h in a["histories"]
        if h["case_index"] == case_index and h["stage1_mask"] == mask and h["final_mask"] == 0
    )


def probability(law, counts):
    return sum((F(r["probability"]) for r in law if r["counts"] == counts), F(0))


def variance(law, q):
    mean = F(mean_from_law(law)[q])
    return str(sum((F(r["probability"]) * (r["counts"][q] - mean) ** 2 for r in law), F(0)))


def algebraic_controls():
    h = [[0] * 4 for _ in range(4)]
    h[1][:3] = [2, -7, 6]
    h[2][:3] = [-2, 7, -6]
    baseline = [["1/2" if i == j == 0 else "0" for j in range(4)] for i in range(4)]
    perturbed = []
    for sign in (1, -1):
        perturbed.append(
            [[str(F(baseline[i][j]) + sign * F(h[i][j], 4)) for j in range(4)] for i in range(4)]
        )
    coincidence_points = [
        (F(1, 2), F(1, 2)),
        (F(1, 3), F(2, 3)),
        (F(0), F(0)),
        (F(1), F(0)),
        (F(0), F(1)),
        (F(1), F(1)),
    ]
    for x, y in coincidence_points:
        require(evaluate(h, x, y) == 0, "selected-rate alias")
        require(
            all(evaluate(table, x, y) == F(1, 2) for table in perturbed),
            "selected-rate probabilities",
        )
    for x, y in AUDIT_POINTS:
        values = [evaluate(table, x, y) for table in perturbed]
        require(
            sum(values) == 1 and min(values) >= F(3, 8) and max(values) <= F(5, 8),
            "bounded abstract PMF diagnostic",
        )
    witness = [evaluate(table, F(1, 2), F(1, 3)) for table in perturbed]
    require(witness == [F(25, 48), F(23, 48)], "off-menu abstract-law distinction")
    g = [F(0), F(-2, 9), F(11, 9), F(-2), F(1)]
    g_eval = lambda x: sum((c * x**i for i, c in enumerate(g)), F(0))
    require(
        all(g_eval(x) == 0 for x in GRID) and g_eval(F(1, 2)) == F(1, 144),
        "out-of-degree grid alias",
    )
    return {
        "selected_rate_alias": {
            "scope": "Abstract two-atom polynomial PMFs, not claimed realizable as this gate's induced-order count laws.",
            "h_coefficients": h,
            "baseline_atom_coefficients": [baseline, baseline],
            "perturbed_atom_coefficients": perturbed,
            "bidegree": [2, 2],
            "global_component_bounds": ["3/8", "5/8"],
            "bound_argument": "|x(1-x)|<=1/4, |2y-1|<=1, |3y-2|<=2, so |h/4|<=1/8.",
            "coincidence_points": [[str(x), str(y)] for x, y in coincidence_points],
            "witness_point": ["1/2", "1/3"],
            "witness_baseline": ["1/2", "1/2"],
            "witness_perturbed": list(map(str, witness)),
            "first_atom_difference": "1/48",
        },
        "out_of_degree_grid_alias": {
            "scope": "Degree-four polynomial diagnostic, deliberately outside the bidegree contract; not a poset law.",
            "x_coefficients": list(map(str, g)),
            "degree_x": 4,
            "grid_values": ["0"] * 4,
            "witness_x": "1/2",
            "witness_value": "1/144",
        },
    }


def controls(a):
    states = a["cases"][0]["states"]
    odd, even = states[1], states[2]
    require_same_wire(odd["marked_order"], even["marked_order"], "singleton marked iso")
    singleton_means = [
        str(evaluate(s["mean_polynomials"][1], F(1, 3), F(2, 3))) for s in (odd, even)
    ]
    require(singleton_means == ["1/3", "2/3"], "singleton coloring matters")
    a5, a3 = states[5], states[3]
    require_same_wire(
        law_at(a5, F(1, 2), F(1, 2)), law_at(a3, F(1, 2), F(1, 2)), "antichain half laws"
    )
    block_atoms = [str(probability(block_law(s), [1, 1, 0, 0])) for s in (a5, a3)]
    require(block_atoms == ["0", "1/2"], "correlation changes law")
    star, path = states[57], states[27]
    require_same_wire(star["mean_polynomials"], path["mean_polynomials"], "star/path equal means")
    require(
        canonical(star["count_polynomials"]) != canonical(path["count_polynomials"]),
        "star/path unequal complete polynomials",
    )
    require_same_wire(block_law(star), block_law(path), "star/path equal corner mixture")
    variances = {}
    for label, x, y, expected in (
        ("iid_half", F(1, 2), F(1, 2), ["15/16", "13/16"]),
        ("iid_color", F(1, 3), F(2, 3), ["68/81", "52/81"]),
    ):
        values = [variance(law_at(s, x, y), 2) for s in (star, path)]
        require(values == expected, "star/path retained variance witness")
        variances[label] = values
    boundary = [
        str(probability(law_at(a5, x, F(2, 5)), [1, 1, 0, 0])) for x in (F(0), F(1, 2), F(1))
    ]
    require(boundary == ["0", "1/2", "0"], "boundary atom disappears")
    require(a5["color_sizes"] == [2, 0], "absent even color")
    require(
        all(
            c == 0
            for atom in a5["count_polynomials"]
            for row in atom["coefficients"]
            for c in row[1:]
        ),
        "absent color has no polynomial dependence",
    )
    fixed = a["cases"][9]["states"][0]
    require(
        fixed["color_sizes"] == [0, 0]
        and fixed["mean_polynomials"][1][0][0] == 1
        and fixed["chain_counts"] == [1, 1, 0, 0],
        "fixed interior not sampled",
    )
    for candidate in ("full_record", "color_order"):
        require(
            all(a["assessments"][candidate][t]["sufficient"] for t in TARGETS),
            "analytic sufficient order control",
        )
    require(
        a["assessments"]["color_graded"]["analytic_means"]["sufficient"] is True
        and a["assessments"]["color_graded"]["analytic_counts"]["sufficient"] is False,
        "mean/full-law sufficiency separation",
    )
    ids = {}
    for label, masks in (("singleton", (1, 2)), ("antichain", (5, 3)), ("star_path", (57, 27))):
        hs = [find_history(a, 0, mask) for mask in masks]
        require(all(F(h["joint_probability"]) > 0 for h in hs), "supported control histories")
        ids[label] = [h["history_id"] for h in hs]
    return {
        "singleton_color_failure": {
            "history_ids": ids["singleton"],
            "color_mean_N1": singleton_means,
        },
        "correlation_failure": {
            "history_ids": ids["antichain"],
            "block_P_N1_equals1": block_atoms,
            "equal_iid_half_laws": True,
        },
        "star_path": {
            "history_ids": ids["star_path"],
            "equal_mean_polynomials": True,
            "equal_count_polynomials": False,
            "equal_block_count_laws": True,
            "variance_N2": variances,
        },
        "boundary_and_absent_color": {
            "case_index": 0,
            "stage1_mask": 5,
            "color_sizes": [2, 0],
            "x": ["0", "1/2", "1"],
            "y": "2/5",
            "P_N1_equals1": boundary,
            "block_P_N1_equals1": "0",
            "fine_support_at_boundary_is_not_assumed": True,
        },
        "fixed_interior": {
            "case_index": 9,
            "stage1_mask": 0,
            "fixed": [0, 3, 7],
            "color_sizes": [0, 0],
            "deterministic_counts": [1, 1, 0, 0],
        },
        **algebraic_controls(),
    }


def run_suite():
    direct = load("qr05i_capture_direct", "analytic.py")
    oracle = load("qr05i_capture_reference", "reference_qr05i.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), oracle.analyze(problem)
    require_same_wire(a, b, "independent complete I outputs differ")
    audit = check_analysis(a)
    rejections = []
    for i, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (
            ("observed_order_expansion", direct),
            ("source_chain_interpolation", oracle),
        ):
            try:
                module.analyze(invalid)
            except (ValueError, TypeError):
                rejected.append(name)
            else:
                raise ValueError("malformed I problem accepted")
        rejections.append({"fixture_index": i, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "controls": controls(a),
        "prior_bridge": prior_bridge(a),
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "Exact finite polynomial-law portability over the full two-color IID rate square, with a degree-bounded interpolation cross-check.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "bidegree_max": [3, 3],
            "exact_component_bits": 4096,
        },
        "parameter_domain": "[0,1]^2",
        "interpolation_nodes": list(map(str, GRID)),
        "audit_points": [[str(x), str(y)] for x, y in AUDIT_POINTS],
        "coefficient_index_order": "x power, then y power; all16 integer cells retained",
        "general_contract_basis": "Explicit finite-sum and polynomial arguments in README; finite executors are not a machine-checked universal proof.",
        "block_coin_is_corner_mixture": True,
        "block_coin_is_interior_iid_evaluation": False,
        "selected_rate_equality_is_general_certificate": False,
        "pooled_class_mass_interpretation": "sum of ten design masses, total10; no source or policy prior",
        "boundary_support_assumed": False,
        "arbitrary_correlated_laws_covered": False,
        "unknown_laws_inferred": False,
        "dynamic_closure_established": False,
        "minimal_bit_cost_claimed": False,
        "quantum_channel_constructed": False,
        "gravity_derived": False,
        "continuum_limit_established": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "lean_proof_completed": False,
    }
    bits = retained_bits(suite)
    require(bits <= 4096, "exact component cap")
    suite["totals"] = {
        **a["counts"],
        **audit,
        "rejected_fixtures": len(rejections),
        "candidate_classes": {n: len(a["candidate_partitions"][n]) for n in CANDIDATES},
        "target_classes": {n: len(a["target_partitions"][n]) for n in TARGETS},
        "H_predictions_reconstructed": suite["prior_bridge"]["H_predictions_reconstructed"],
        "prior_target_comparisons": len(TARGETS) * len(H_TARGETS),
        "max_absolute_atom_coefficient": max(
            abs(c)
            for case in a["cases"]
            for state in case["states"]
            for atom in state["count_polynomials"]
            for row in atom["coefficients"]
            for c in row
        ),
        "max_retained_component_bits": bits,
    }
    require_same_wire(suite, json.loads(canonical(suite)), "native aggregate round trip")
    return suite


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is int:
        return abs(value).bit_length()
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        v = F(value)
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return 0


def require_wire(value):
    """Reject implicit JSON coercions in the mathematical evidence tree."""
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            require_wire(item)
        return
    if type(value) is dict:
        require(all(type(key) is str for key in value), "wire keys must be strings")
        for item in value.values():
            require_wire(item)
        return
    raise ValueError("mathematical suite must use native exact JSON types")


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def require_same_wire(left, right, message):
    require_wire(left)
    require_wire(right)
    require(canonical(left) == canonical(right), message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(
        sys.flags.isolated and sys.pycache_prefix, "run isolated with an external bytecode cache"
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "invalid bytecode cache boundary",
    )
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("result exists; use --verify, never overwrite")
    frozen, previous = ledger(), priors()
    if args.verify:
        before = plain_bytes(RESULT)
        existing = json.loads(before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == before, "result is not canonical")
        require_same_wire(existing["source_ledger"], frozen, "source identity changed")
        require_same_wire(existing["prior_artifacts"], previous, "prior identity changed")
    started = time.perf_counter()
    suite = run_suite()
    require_wire(suite)
    require_same_wire(suite, json.loads(canonical(suite)), "aggregate wire round trip differs")
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require_same_wire(existing["suite"], suite, "exact replay differs")
        require(plain_bytes(RESULT) == before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "sha256": digest(before),
                    "seconds": elapsed,
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": SCHEMA,
        "source_ledger": frozen,
        "prior_artifacts": previous,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "scope": "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    with RESULT.open("xb") as output:
        output.write(raw)
    require(plain_bytes(RESULT) == raw, "capture readback differs")
    print(
        json.dumps(
            {
                "status": "CREATED_EXACT_FINITE_RESULT",
                "path": str(RESULT),
                "bytes": len(raw),
                "sha256": digest(raw),
                "seconds": elapsed,
                "totals": suite["totals"],
            }
        )
    )


if __name__ == "__main__":
    main()
