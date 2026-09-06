"""QR-05G exact finite sampling capture and read-only replay."""

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
SCHEMA = "det8-qr05g-results-v1"
BASE_COMMIT = "490c443186dbe1b862d377e197f3281ee261ad56"
SOURCES = (
    "README.md",
    "compression.py",
    "reference_qr05g.py",
    "study.py",
    "test_qr05g.py",
    "test_capture.py",
)
PRIORS = {
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
)
TARGETS = ("current_estimate", "future_means", "future_counts", "future_records")
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
SEQUENTIAL_PRIOR = "qr-05f-two-stage-2026-09-06/results.json"
EXPECTED_COUNTS = {
    "cases": 10,
    "states": 608,
    "positive_states": 510,
    "repeat_rows": 6804,
    "positive_repeat_rows": 4872,
    "histories": 6804,
    "positive_histories": 3534,
    "zero_histories": 3270,
    "candidates": 9,
    "targets": 4,
    "current_estimator_cells": 27216,
}


def fixtures():
    return [{"schema_version": "det8-qr05g-problem-v1", "family": "qr05f_ten"}]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"family": "qr05f_ten"},
        {"schema_version": base["schema_version"]},
        {**base, "extra": 1},
        *({**base, "family": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "schema_version": v} for v in (True, None, 1, [], "other")),
        {**base, "profile": "ferrers6"},
        {**base, "design": "independent"},
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
    ]
    keys = {name: base + tail for name, tail in zip(CANDIDATES, extra, strict=True)}
    signatures = {
        "current_estimate": history["current_estimate"],
        "future_means": state["count_mean"],
        "future_counts": state["count_law"],
        "future_records": [
            {k: row[k] for k in ("kept", "past", "probability")}
            for row in state["repeat_rows"]
            if F(row["probability"]) > 0
        ],
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


def check_analysis(a):
    """Third-route wire, law, partition and factorization audit."""
    require_wire(a)
    require_same_wire(a["counts"], EXPECTED_COUNTS, "retained count contract")
    require(len(a["cases"]) == 10 and len(a["histories"]) == 6804, "universe size")
    expected_histories = []
    total_states = positive_states = repeat_rows = positive_repeat = 0
    for index, case in enumerate(a["cases"]):
        require(case["case_index"] == index, "case index")
        require((case["profile"], case["design"]) == PAIRS[index], "case order")
        states = case["states"]
        m = len(case["eligible"])
        require([s["mask"] for s in states] == list(range(1 << m)), "state masks")
        p1 = [F(s["probability"]) for s in states]
        require(min(p1) >= 0 and sum(p1) == 1, "first law")
        require_same_wire(
            case["stage1_inclusions"],
            [
                str(sum((p for mask, p in enumerate(p1) if mask & support == support), F(0)))
                for support in range(1 << m)
            ],
            "first inclusion law",
        )
        alpha = [F((-1) ** q, 2 ** (q + 1)) / F(case["density"]) ** q for q in range(4)]
        for state in states:
            s, rows = state["mask"], state["repeat_rows"]
            submasks = [t for t in range(1 << m) if s & t == t]
            require([r["mask"] for r in rows] == submasks, "repeat mask coverage")
            probs = [F(r["probability"]) for r in rows]
            require(min(probs) >= 0 and sum(probs) == 1, "repeat normalization")
            total_states += 1
            positive_states += int(p1[s] > 0)
            repeat_rows += len(rows)
            positive_repeat += sum(p > 0 for p in probs)
            law = {}
            for r, p in zip(rows, probs, strict=True):
                expected_histories.append((index, s, r["mask"], str(p), str(p1[s] * p)))
                require_same_wire(r["kept"], states[r["mask"]]["kept"], "repeat IDs")
                require_same_wire(r["past"], states[r["mask"]]["past"], "repeat order")
                require_same_wire(
                    r["chain_counts"], states[r["mask"]]["chain_counts"], "repeat counts"
                )
                if p:
                    vector = tuple(r["chain_counts"])
                    law[vector] = law.get(vector, F(0)) + p
            require_same_wire(
                state["count_law"],
                [{"counts": list(v), "probability": str(law[v])} for v in sorted(law)],
                "count pushforward",
            )
            mean = [
                sum((p * r["chain_counts"][q] for p, r in zip(probs, rows, strict=True)), F(0))
                for q in range(4)
            ]
            cov = [
                [
                    sum(
                        (
                            p * (r["chain_counts"][i] - mean[i]) * (r["chain_counts"][j] - mean[j])
                            for p, r in zip(probs, rows, strict=True)
                        ),
                        F(0),
                    )
                    for j in range(4)
                ]
                for i in range(4)
            ]
            require_same_wire(state["count_mean"], [str(x) for x in mean], "future mean")
            require_same_wire(
                state["count_covariance"],
                [[str(x) for x in row] for row in cov],
                "future covariance",
            )
            require_same_wire(
                state["coefficient_mean"],
                [str(alpha[q] * mean[q]) for q in range(4)],
                "coefficient mean",
            )
            require_same_wire(
                state["coefficient_covariance"],
                [[str(alpha[i] * alpha[j] * cov[i][j]) for j in range(4)] for i in range(4)],
                "coefficient covariance",
            )
            require_same_wire(
                state["chain_counts"],
                [sum(row) for row in state["graded_counts"]],
                "graded row sums",
            )
    require(
        (total_states, positive_states, repeat_rows, positive_repeat) == (608, 510, 6804, 4872),
        "actual retained totals",
    )
    positive = []
    for history, expected in zip(a["histories"], expected_histories, strict=True):
        actual = tuple(
            history[k]
            for k in (
                "case_index",
                "stage1_mask",
                "final_mask",
                "conditional_probability",
                "joint_probability",
            )
        )
        require(actual == expected, "history law/order")
        if F(history["joint_probability"]) > 0:
            positive.append(history)
            require(not any(history["omitted_terms"]), "positive history omitted support")
        else:
            require(
                all(v is None for v in history["candidate_classes"].values()),
                "zero candidate class",
            )
            require(all(v is None for v in history["target_classes"].values()), "zero target class")
    require([h["history_id"] for h in a["histories"]] == list(range(6804)), "global IDs")
    require(len(positive) == 3534, "positive history count")
    audit_partitions(a, positive)


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
            signature_cache[cache_key] = {t: canonical(sigs[t]) for t in TARGETS[1:]}
        sigbytes = {
            "current_estimate": canonical(sigs["current_estimate"]),
            **signature_cache[cache_key],
        }
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


def find_history(a, case, s, t):
    return next(
        h
        for h in a["histories"]
        if (h["case_index"], h["stage1_mask"], h["final_mask"]) == (case, s, t)
    )


def controls(a):
    result = {}
    for case_index, variances, atom, mass in (
        (0, ["15/16", "13/16"], "1/16", "1/1024"),
        (1, ["4/9", "32/81"], "2/81", "1/324"),
    ):
        case = a["cases"][case_index]
        star, path = [case["states"][s] for s in (57, 27)]
        hs = [find_history(a, case_index, s, 0) for s in (57, 27)]
        require_same_wire(star["count_mean"], path["count_mean"], "star/path means")
        for field in ("chain_counts", "graded_counts", "policy_token", "tagged_present"):
            require_same_wire(star[field], path[field], "star/path summary " + field)
        require(
            [s["count_covariance"][2][2] for s in (star, path)] == variances, "star/path variance"
        )
        atom_probs = [
            str(
                sum(
                    (F(r["probability"]) for r in s["count_law"] if r["counts"] == [1, 3, 0, 0]),
                    F(0),
                )
            )
            for s in (star, path)
        ]
        require(atom_probs == [atom, "0"], "star/path joint atom")
        require([h["joint_probability"] for h in hs] == [mass, mass], "star/path supported mass")
        result["star_path_" + case["design"]] = {
            "history_ids": [h["history_id"] for h in hs],
            "mean": star["count_mean"],
            "variance_R": variances,
            "joint_atom_N3_R0": atom_probs,
            "history_joint_mass": mass,
        }
    case = a["cases"][9]
    left, right = [case["states"][s] for s in (10, 20)]
    require_same_wire(left["chain_counts"], right["chain_counts"], "fixed counts")
    require_same_wire(left["unmarked_order"], right["unmarked_order"], "fixed unmarked iso")
    require(left["marked_order"] != right["marked_order"], "fixed marked distinction")
    require(left["graded_counts"] != right["graded_counts"], "fixed support grading")
    require(
        [left["count_mean"][2], right["count_mean"][2]] == ["1/4", "1/2"], "fixed relation means"
    )
    result["fixed_marking"] = {
        "history_ids": [find_history(a, 9, s, 0)["history_id"] for s in (10, 20)],
        "counts": left["chain_counts"],
        "unmarked_order": left["unmarked_order"],
        "mean_R": ["1/4", "1/2"],
    }
    case = a["cases"][0]
    up, down = [case["states"][s] for s in (57, 39)]
    require(up["marked_order"] != down["marked_order"], "up/down nonisomorphism")
    require_same_wire(up["count_law"], down["count_law"], "up/down equal count law")
    result["marked_order_not_necessary"] = {
        "history_ids": [find_history(a, 0, s, 0)["history_id"] for s in (57, 39)],
        "marked_orders": [up["marked_order"], down["marked_order"]],
        "equal_joint_count_laws": True,
    }
    edges = [case["states"][s] for s in (9, 18)]
    require_same_wire(edges[0]["marked_order"], edges[1]["marked_order"], "one-edge iso")
    require_same_wire(edges[0]["count_law"], edges[1]["count_law"], "one-edge count law")
    probabilities = [
        str(sum((F(r["probability"]) for r in s["repeat_rows"] if 1 in r["kept"]), F(0)))
        for s in edges
    ]
    require(probabilities == ["1/2", "0"], "labeled ID probability")
    result["marked_order_not_labeled_law"] = {
        "history_ids": [find_history(a, 0, s, 0)["history_id"] for s in (9, 18)],
        "ID1_repeat_probabilities": probabilities,
    }
    cross = [find_history(a, i, 63, 0) for i in (0, 5)]
    for candidate in ("final_only", "counts_policy", "graded_policy"):
        require(
            cross[0]["candidate_classes"][candidate] == cross[1]["candidate_classes"][candidate],
            "cross-source public pooling",
        )
    require(
        cross[0]["target_classes"]["future_means"] == cross[1]["target_classes"]["future_means"],
        "cross-source means",
    )
    require(
        cross[0]["target_classes"]["future_counts"] != cross[1]["target_classes"]["future_counts"],
        "cross-source count law",
    )
    result["cross_source"] = {
        "history_ids": [h["history_id"] for h in cross],
        "variance_R": [a["cases"][i]["states"][63]["count_covariance"][2][2] for i in (0, 5)],
        "profile_labels_excluded_from_keys": True,
    }
    holes = [
        h for h in a["histories"] if h["case_index"] in (3, 7) and F(h["joint_probability"]) > 0
    ]
    coins = [h for h in a["histories"] if h["case_index"] == 2 and F(h["joint_probability"]) > 0]
    require(
        refines(
            [dict(h["candidate_classes"], **h["target_classes"]) for h in holes],
            "final_only",
            "future_records",
        ),
        "parity hole final sufficiency",
    )
    require(
        refines(
            [dict(h["candidate_classes"], **h["target_classes"]) for h in coins],
            "counts_policy",
            "future_counts",
        ),
        "common coin count sufficiency",
    )
    empty, odd = [find_history(a, 3, s, 0) for s in (0, 1)]
    require(
        empty["target_classes"]["future_records"] == odd["target_classes"]["future_records"],
        "degenerate record quotient",
    )
    require(
        empty["candidate_classes"]["policy_token"] != odd["candidate_classes"]["policy_token"],
        "token unnecessary in degenerate context",
    )
    result["context_dependent_compression"] = {
        "parity_hole_final_record_sufficient_for_repeat_record": True,
        "common_coin_counts_sufficient_for_repeat_counts": True,
        "parity_hole_merged_history_ids": [empty["history_id"], odd["history_id"]],
        "global_counts_sufficiency": a["assessments"]["counts_policy"]["future_counts"][
            "sufficient"
        ],
    }
    for candidate, target in (
        ("policy_token", "current_estimate"),
        ("graded_policy", "future_means"),
        ("marked_order", "future_counts"),
        *(("full_record", t) for t in TARGETS),
    ):
        require(a["assessments"][candidate][target]["sufficient"], "positive sufficiency control")
    for candidate, target in (
        ("final_only", "current_estimate"),
        ("unmarked_order", "future_means"),
        ("counts_policy", "future_means"),
        ("tagged_graded", "future_counts"),
        ("marked_order", "future_records"),
    ):
        require(
            not a["assessments"][candidate][target]["sufficient"], "negative sufficiency control"
        )
    require(
        a["target_refinement"][3][2] and a["target_refinement"][2][1], "predictive target nesting"
    )
    return result


def prior_bridge(a):
    old_suite = prior_json(SEQUENTIAL_PRIOR)["suite"]
    previous = [c["analysis"] for c in old_suite["cases"]]
    require(len(previous) == len(a["cases"]), "prior case universe")
    states_checked = transcripts_checked = repeat_checked = 0
    for index, (case, old) in enumerate(zip(a["cases"], previous, strict=True)):
        for field in (
            "profile",
            "design",
            "density",
            "past",
            "fixed",
            "eligible",
            "stage1_inclusions",
        ):
            require_same_wire(case[field], old[field], "QR05F source/inclusion identity")
        paths = {(r["stage1_mask"], r["final_mask"]): r for r in old["transcripts"]}
        for state, earlier in zip(case["states"], old["first_rows"], strict=True):
            for field in ("mask", "probability", "kept", "past", "policy_token"):
                require_same_wire(state[field], earlier[field], "QR05F first row")
            require_same_wire(
                state["chain_counts"],
                old["final_rows"][state["mask"]]["chain_counts"],
                "QR05F observed counts",
            )
            states_checked += 1
            for repeat in state["repeat_rows"]:
                require_same_wire(
                    repeat["probability"],
                    paths[state["mask"], repeat["mask"]]["conditional_probability"],
                    "QR05F repeat kernel",
                )
                repeat_checked += 1
        current = [h for h in a["histories"] if h["case_index"] == index]
        require(len(current) == len(old["transcripts"]), "prior transcript coverage")
        for history, earlier in zip(current, old["transcripts"], strict=True):
            for field in (
                "stage1_mask",
                "final_mask",
                "conditional_probability",
                "joint_probability",
            ):
                require_same_wire(history[field], earlier[field], "QR05F history law")
            require_same_wire(
                history["current_estimate"],
                earlier["estimates"]["sequential_supported"],
                "QR05F current estimator",
            )
            require_same_wire(
                history["omitted_terms"],
                earlier["omitted_terms"]["sequential_supported"],
                "QR05F omitted support",
            )
            transcripts_checked += 1
    require(
        (states_checked, transcripts_checked, repeat_checked) == (608, 6804, 6804),
        "prior comparison totals",
    )
    return {
        "source_cases_checked": 10,
        "stage1_inclusion_tables_checked": 10,
        "first_rows_checked": states_checked,
        "transcripts_checked": transcripts_checked,
        "conditional_repeat_rows_checked": repeat_checked,
        "prior_executors_imported": False,
        "prior_geometric_and_quantum_bridge": old_suite["prior_bridge"][
            "prior_geometric_and_quantum_bridge"
        ],
        "scope": "Pinned JSON identities and exact finite sampling calculations; no new physical coupling.",
    }


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


def run_suite():
    direct = load("qr05g_capture_direct", "compression.py")
    reference = load("qr05g_capture_reference", "reference_qr05g.py")
    problem = fixtures()[0]
    a, oracle = direct.analyze(problem), reference.analyze(problem)
    require_same_wire(a, oracle, "independent integrated executors differ")
    check_analysis(a)
    rejected = []
    for index, invalid in enumerate(invalid_fixtures()):
        rejected_by = []
        for name, executor in (("observed_order", direct), ("full_source_oracle", reference)):
            try:
                executor.analyze(invalid)
            except (TypeError, ValueError):
                rejected_by.append(name)
            else:
                raise ValueError("malformed problem accepted")
        rejected.append({"fixture_index": index, "input": invalid, "rejected_by": rejected_by})
    suite = {
        "input": problem,
        "analysis": a,
        "rejections": rejected,
        "controls": controls(a),
        "prior_bridge": prior_bridge(a),
        "research_base_commit": BASE_COMMIT,
        "claim": "Exact question-relative factorization and finite coarsest partitions on the declared supported ten-case domain.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "exact_component_bits": 4096,
        },
        "pooled_class_mass_interpretation": "sum of ten per-case design masses, total10; no source prior or pooled posterior",
        "source_profile_is_public": False,
        "triple_history_expansion_used": False,
        "universal_minimal_history_claimed": False,
        "minimal_bit_cost_claimed": False,
        "dynamic_closure_established": False,
        "quantum_channel_constructed": False,
        "continuum_limit_established": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
    }
    bits = retained_bits(suite)
    require(bits <= 4096, "retained exact arithmetic cap")
    suite["totals"] = {
        **a["counts"],
        "rejected_fixtures": len(rejected),
        "candidate_classes": {n: len(a["candidate_partitions"][n]) for n in CANDIDATES},
        "target_classes": {n: len(a["target_partitions"][n]) for n in TARGETS},
        "max_retained_component_bits": bits,
    }
    require_same_wire(suite, json.loads(canonical(suite)), "native suite round trip")
    return suite


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
            "scope": "suite only; excludes serialization; no application performance claim",
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
