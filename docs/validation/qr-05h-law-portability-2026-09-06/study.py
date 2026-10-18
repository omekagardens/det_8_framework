"""QR-05H exact finite sampling capture and read-only replay."""

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
SCHEMA = "det8-qr05h-results-v1"
BASE_COMMIT = "cdfe6334ecf764a452c6d2dab0ed9970aef2e1e8"
SOURCES = (
    "README.md",
    "portability.py",
    "reference_qr05h.py",
    "study.py",
    "test_qr05h.py",
    "test_capture.py",
)
PRIORS = {
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
TARGETS = tuple(p + "_" + q for p in POLICIES for q in ("means", "counts")) + (
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
EXPECTED_COUNTS = {
    "cases": 10,
    "states": 608,
    "positive_states": 510,
    "observations": 6804,
    "policies": 3,
    "predictions": 1824,
    "probability_cells": 20412,
    "histories": 6804,
    "positive_histories": 3534,
    "zero_histories": 3270,
    "candidates": 12,
    "targets": 8,
    "transports": 5472,
    "fine_weight_cells": 61236,
}


def fixtures():
    return [{"schema_version": "det8-qr05h-problem-v1", "family": "qr05g_menu3"}]


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


def policy_vector(case, state, policy):
    s = state["mask"]
    vertices = [(i, v) for i, v in enumerate(case["eligible"]) if s & (1 << i)]
    blocks = [sum(1 << i for i, v in vertices if v % 2 == parity) for parity in (1, 0)]
    result = []
    for obs in state["observations"]:
        u = obs["mask"]
        if policy == "block_coin":
            probability = sum(
                (
                    F(1, 4)
                    for coin in range(4)
                    if ((blocks[0] if coin & 1 else 0) | (blocks[1] if coin & 2 else 0)) == u
                ),
                F(0),
            )
        else:
            probability = F(1)
            for i, v in vertices:
                rate = F(1, 2) if policy == "iid_half" else F(1 if v % 2 else 2, 3)
                probability *= rate if u & (1 << i) else 1 - rate
        result.append(probability)
    require(sum(result) == 1 and min(result) >= 0, "continuation probability normalization")
    return result


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
    signatures = {}
    for policy in POLICIES:
        signatures[policy + "_means"] = state["predictions"][policy]["count_mean"]
        signatures[policy + "_counts"] = state["predictions"][policy]["count_law"]
    for kind in ("means", "counts"):
        signatures["menu_" + kind] = [signatures[p + "_" + kind] for p in POLICIES]
    return base, keys, signatures


def refines(rows, left, right):
    seen = {}
    for row in rows:
        a, b = row[left], row[right]
        if a in seen and seen[a] != b:
            return False
        seen[a] = b
    return True


def check_transport(state, tr):
    """Independently reconstruct densities, missing mass and their count fibers."""
    obs = state["observations"]
    q = list(map(F, state["predictions"][tr["source"]]["probabilities"]))
    p = list(map(F, state["predictions"][tr["target"]]["probabilities"]))
    weights = [str(b / a) if a else None for a, b in zip(q, p, strict=True)]
    require_same_wire(tr["fine_weights"], weights, "fine density ratio")
    missing = [r["mask"] for r, a, b in zip(obs, q, p, strict=True) if not a and b]
    mass = sum((b for a, b in zip(q, p, strict=True) if not a), F(0))
    require_same_wire(tr["missing_masks"], missing, "missing fine masks")
    require_same_wire(tr["fine_missing_mass"], str(mass), "fine missing mass")
    require(tr["fine_supported"] is (mass == 0), "fine support")
    supported_p = [b if a else F(0) for a, b in zip(q, p, strict=True)]
    require_same_wire(
        tr["weighted_count_law"], pushforward(obs, supported_p), "fine weighted pushforward"
    )
    atoms = sorted({tuple(r["chain_counts"]) for r in obs})
    rows, coarse_probs = [], {}
    residual = F(0)
    for z in atoms:
        indices = [i for i, r in enumerate(obs) if tuple(r["chain_counts"]) == z]
        qs, ps, ss = (sum((v[i] for i in indices), F(0)) for v in (q, p, supported_p))
        w, conditional = (ps / qs, ss / qs) if qs else (None, None)
        if qs:
            require(w - conditional == (ps - ss) / qs, "coarsening residual identity")
            residual += qs * (w - conditional)
        if ps and qs:
            coarse_probs[z] = ps
        rows.append(
            {
                "counts": list(z),
                "source_probability": str(qs),
                "target_probability": str(ps),
                "fine_supported_target_probability": str(ss),
                "missing_fine_probability": str(ps - ss),
                "weight": str(w) if w is not None else None,
                "conditional_fine_weight": str(conditional) if conditional is not None else None,
                "weighted_probability": str(ps if qs else F(0)),
            }
        )
    require_same_wire(tr["coarse_rows"], rows, "coarse density/support rows")
    coarse_missing = sum(
        (F(r["target_probability"]) for r in rows if F(r["source_probability"]) == 0), F(0)
    )
    require_same_wire(tr["coarse_missing_mass"], str(coarse_missing), "coarse missing mass")
    require(tr["coarse_supported"] is (coarse_missing == 0), "coarse support")
    require(
        mass >= coarse_missing and residual == mass - coarse_missing, "integrated support residual"
    )
    require_same_wire(
        tr["coarse_weighted_count_law"],
        [{"counts": list(z), "probability": str(coarse_probs[z])} for z in sorted(coarse_probs)],
        "coarse weighted pushforward",
    )
    representative, collision = {}, None
    for r, prob, w in zip(obs, q, weights, strict=True):
        if not prob:
            continue
        z = tuple(r["chain_counts"])
        if z not in representative:
            representative[z] = (r["mask"], w)
        elif collision is None and representative[z][1] != w:
            collision = {"left_mask": representative[z][0], "right_mask": r["mask"]}
    require_same_wire(tr["first_weight_collision"], collision, "first fine-weight collision")
    require(tr["fine_weight_count_measurable"] is (collision is None), "fine weight measurability")


def check_analysis(a):
    require_wire(a)
    require(len(a["cases"]) == 10 and len(a["histories"]) == 6804, "universe size")
    histories = []
    ns = ps = no = prob_cells = nt = fw = cw = 0
    for index, case in enumerate(a["cases"]):
        require(
            case["case_index"] == index and (case["profile"], case["design"]) == PAIRS[index],
            "case order",
        )
        states = case["states"]
        require(
            [s["mask"] for s in states] == list(range(1 << len(case["eligible"]))), "state coverage"
        )
        p1 = list(map(F, (s["probability"] for s in states)))
        require(min(p1) >= 0 and sum(p1) == 1, "first law normalization")
        alpha = [F((-1) ** q, 2 ** (q + 1)) / F(case["density"]) ** q for q in range(4)]
        for state in states:
            ns += 1
            ps += int(F(state["probability"]) > 0)
            s = state["mask"]
            obs = state["observations"]
            require(
                [r["mask"] for r in obs]
                == [u for u in range(1 << len(case["eligible"])) if s & u == u],
                "observation coverage",
            )
            no += len(obs)
            for r in obs:
                reference = states[r["mask"]]
                for name in ("kept", "past", "chain_counts"):
                    require_same_wire(r[name], reference[name], "induced observation identity")
                k = current_kernel(case["design"], s, r["mask"])
                histories.append([index, s, r["mask"], str(k), str(p1[s] * k)])
            for policy in POLICIES:
                prediction = state["predictions"][policy]
                probabilities = policy_vector(case, state, policy)
                prob_cells += len(probabilities)
                require_same_wire(
                    prediction["probabilities"], [str(x) for x in probabilities], "continuation law"
                )
                law = pushforward(obs, probabilities)
                mean = mean_from_law(law)
                require_same_wire(prediction["count_law"], law, "joint count pushforward")
                require_same_wire(prediction["count_mean"], mean, "count mean")
                require_same_wire(
                    prediction["coefficient_mean"],
                    [str(alpha[q] * F(mean[q])) for q in range(4)],
                    "scaled coefficient mean",
                )
                graded_mean = []
                for row in state["color_graded"]:
                    total = F(0)
                    for odd in range(4):
                        for even in range(4):
                            factor = (
                                F(1, 2) ** (odd + even)
                                if policy == "iid_half"
                                else F(1, 3) ** odd * F(2, 3) ** even
                                if policy == "iid_color"
                                else F(1, 2) ** (int(odd > 0) + int(even > 0))
                            )
                            total += row[odd][even] * factor
                    graded_mean.append(str(total))
                require_same_wire(mean, graded_mean, "color-graded prediction")
            expected_pairs = [[source, target] for source in POLICIES for target in POLICIES]
            require_same_wire(
                [[t["source"], t["target"]] for t in state["transports"]],
                expected_pairs,
                "ordered transport pairs",
            )
            for tr in state["transports"]:
                check_transport(state, tr)
                nt += 1
                fw += len(tr["fine_weights"])
                cw += len(tr["coarse_rows"])
    fields = (
        "case_index",
        "stage1_mask",
        "final_mask",
        "conditional_probability",
        "joint_probability",
    )
    positive = []
    for i, (history, expected) in enumerate(zip(a["histories"], histories, strict=True)):
        require(history["history_id"] == i, "global history index")
        require_same_wire([history[k] for k in fields], expected, "current history law")
        if F(history["joint_probability"]) > 0:
            positive.append(history)
        else:
            require(
                all(
                    v is None
                    for v in [
                        *history["candidate_classes"].values(),
                        *history["target_classes"].values(),
                    ]
                ),
                "zero history classes",
            )
    require(
        (ns, ps, no, prob_cells, nt, fw, len(positive))
        == (608, 510, 6804, 20412, 5472, 61236, 3534),
        "retained actual totals",
    )
    require_same_wire(
        a["counts"], {**EXPECTED_COUNTS, "coarse_weight_cells": cw}, "retained count contract"
    )
    audit_partitions(a, positive)
    for kind in ("means", "counts"):
        groups, lookup = [], {}
        for history in positive:
            key = tuple(history["target_classes"][p + "_" + kind] for p in POLICIES)
            if key not in lookup:
                lookup[key] = len(groups)
                groups.append([])
            groups[lookup[key]].append(history["history_id"])
        require_same_wire(
            groups,
            [p["members"] for p in a["target_partitions"]["menu_" + kind]],
            "menu is same-domain common refinement",
        )


def find_history(a, case, s, t=0):
    return next(
        h
        for h in a["histories"]
        if (h["case_index"], h["stage1_mask"], h["final_mask"]) == (case, s, t)
    )


def transport(state, source, target):
    return next(t for t in state["transports"] if (t["source"], t["target"]) == (source, target))


def atom(state, policy, counts):
    return sum(
        (
            F(r["probability"])
            for r in state["predictions"][policy]["count_law"]
            if r["counts"] == counts
        ),
        F(0),
    )


def variance(state, policy, degree):
    law = state["predictions"][policy]["count_law"]
    mean = F(state["predictions"][policy]["count_mean"][degree])
    return str(sum((F(r["probability"]) * (r["counts"][degree] - mean) ** 2 for r in law), F(0)))


def controls(a):
    states = a["cases"][0]["states"]
    left, right = states[1], states[2]
    require_same_wire(left["marked_order"], right["marked_order"], "singleton marked iso")
    require_same_wire(left["block_order"], right["block_order"], "singleton anonymous block iso")
    require(
        [s["predictions"]["iid_color"]["count_mean"][1] for s in (left, right)] == ["1/3", "2/3"],
        "nonuniform singleton failure",
    )
    a5, a3 = states[5], states[3]
    require_same_wire(a5["marked_order"], a3["marked_order"], "antichain iso")
    require_same_wire(
        a5["predictions"]["iid_half"]["count_law"],
        a3["predictions"]["iid_half"]["count_law"],
        "antichain iid half",
    )
    require(
        [str(atom(s, "block_coin", [1, 1, 0, 0])) for s in (a5, a3)] == ["0", "1/2"],
        "correlation not marginal law",
    )
    star, path = states[57], states[27]
    require_same_wire(star["color_graded"], path["color_graded"], "color star/path grading")
    variances = {}
    for policy, expected in (("iid_half", ["15/16", "13/16"]), ("iid_color", ["68/81", "52/81"])):
        require_same_wire(
            star["predictions"][policy]["count_mean"],
            path["predictions"][policy]["count_mean"],
            "star/path means",
        )
        actual = [variance(s, policy, 2) for s in (star, path)]
        require_same_wire(actual, expected, "star/path variance")
        variances[policy] = actual
    require_same_wire(
        star["predictions"]["block_coin"]["count_law"],
        path["predictions"]["block_coin"]["count_law"],
        "graded block law control",
    )
    require(
        star["predictions"]["iid_color"]["count_mean"] == ["1", "2", "5/9", "0"],
        "color star/path mean",
    )
    varying = transport(states[3], "iid_half", "iid_color")
    require(
        varying["fine_supported"] is True and varying["fine_weight_count_measurable"] is False,
        "fine weights versus counts",
    )
    require_same_wire(
        varying["fine_weights"], ["8/9", "4/9", "16/9", "8/9"], "explicit unequal fine ratios"
    )
    middle = next(r for r in varying["coarse_rows"] if r["counts"] == [1, 1, 0, 0])
    require(
        middle["weight"] == middle["conditional_fine_weight"] == "10/9", "conditional coarse ratio"
    )
    forward = transport(states[5], "iid_half", "block_coin")
    reverse = transport(states[5], "block_coin", "iid_half")
    require_same_wire(forward["fine_weights"], ["2", "0", "0", "2"], "supported fine transport")
    require(
        reverse["missing_masks"] == [1, 4]
        and reverse["fine_missing_mass"] == reverse["coarse_missing_mass"] == "1/2",
        "unsupported reverse transport",
    )
    hole = transport(states[7], "block_coin", "iid_half")
    require(
        hole["fine_supported"] is False and hole["coarse_supported"] is True,
        "fine/coarse support separation",
    )
    require(
        hole["missing_masks"] == [1, 3, 4, 6]
        and hole["fine_missing_mass"] == "1/2"
        and hole["coarse_missing_mass"] == "0",
        "support hole mass",
    )
    require_same_wire(
        [r["weight"] for r in hole["coarse_rows"]],
        ["1/2", "3/2", "3/2", "1/2"],
        "coarse weights across support hole",
    )
    require_same_wire(
        [r["conditional_fine_weight"] for r in hole["coarse_rows"]],
        ["1/2"] * 4,
        "conditional supported weights across hole",
    )
    for candidate, targets in (
        ("full_record", TARGETS),
        ("color_order", TARGETS),
        (
            "color_graded",
            (
                "iid_half_means",
                "iid_color_means",
                "block_coin_means",
                "block_coin_counts",
                "menu_means",
            ),
        ),
        (
            "block_order",
            ("iid_half_means", "iid_half_counts", "block_coin_means", "block_coin_counts"),
        ),
        ("marked_order", ("iid_half_means", "iid_half_counts")),
    ):
        require(
            all(a["assessments"][candidate][t]["sufficient"] for t in targets),
            "portable positive control " + candidate,
        )
    for candidate, target in (
        ("marked_order", "iid_color_means"),
        ("marked_order", "block_coin_counts"),
        ("block_order", "iid_color_means"),
        ("color_graded", "iid_half_counts"),
        ("color_graded", "iid_color_counts"),
        ("color_graded", "menu_counts"),
    ):
        require(
            a["assessments"][candidate][target]["sufficient"] is False,
            "nonportable negative control",
        )
    for s in (1, 2, 3, 5, 7, 27, 57):
        require(F(find_history(a, 0, s)["joint_probability"]) > 0, "controls use supported history")
    return {
        "singleton_color_failure": {
            "history_ids": [find_history(a, 0, s)["history_id"] for s in (1, 2)],
            "mean_N1": ["1/3", "2/3"],
        },
        "correlation_failure": {
            "history_ids": [find_history(a, 0, s)["history_id"] for s in (5, 3)],
            "P_N1_equals1": ["0", "1/2"],
        },
        "star_path": {
            "history_ids": [find_history(a, 0, s)["history_id"] for s in (57, 27)],
            "variance_R": variances,
            "equal_block_count_laws": True,
        },
        "weight_not_count_measurable": {
            "case_index": 0,
            "stage1_mask": 3,
            "source": "iid_half",
            "target": "iid_color",
            "fine_weights": varying["fine_weights"],
            "coarse_N1_weight": "10/9",
        },
        "reverse_support_failure": {
            "case_index": 0,
            "stage1_mask": 5,
            "source": "block_coin",
            "target": "iid_half",
            "fine_missing_mass": "1/2",
            "coarse_missing_mass": "1/2",
        },
        "fine_coarse_support_separation": {
            "case_index": 0,
            "stage1_mask": 7,
            "source": "block_coin",
            "target": "iid_half",
            "missing_masks": hole["missing_masks"],
            "fine_missing_mass": "1/2",
            "coarse_missing_mass": "0",
            "coarse_weights": [r["weight"] for r in hole["coarse_rows"]],
            "conditional_fine_weights": [r["conditional_fine_weight"] for r in hole["coarse_rows"]],
        },
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


def prior_bridge(a):
    old_suite = prior_json(PREDICTIVE_PRIOR)["suite"]
    old = old_suite["analysis"]
    state_fields = (
        "mask",
        "probability",
        "kept",
        "past",
        "policy_token",
        "tagged_present",
        "chain_counts",
        "graded_counts",
        "unmarked_order",
        "marked_order",
    )
    states = observations = histories = baseline = 0
    for case, previous in zip(a["cases"], old["cases"], strict=True):
        for field in (
            "case_index",
            "profile",
            "design",
            "density",
            "past",
            "fixed",
            "eligible",
            "stage1_inclusions",
        ):
            require_same_wire(case[field], previous[field], "G source/current-law identity")
        for state, earlier in zip(case["states"], previous["states"], strict=True):
            for field in state_fields:
                require_same_wire(state[field], earlier[field], "G state identity")
            probabilities = []
            for row, old_row in zip(state["observations"], earlier["repeat_rows"], strict=True):
                for field in ("mask", "kept", "past", "chain_counts"):
                    require_same_wire(
                        row[field], old_row[field], "G induced continuation observation"
                    )
                k = current_kernel(case["design"], state["mask"], row["mask"])
                require_same_wire(str(k), old_row["probability"], "G current repeat kernel")
                probabilities.append(k)
                observations += 1
            law = pushforward(state["observations"], probabilities)
            mean = mean_from_law(law)
            require_same_wire(law, earlier["count_law"], "G baseline count law")
            require_same_wire(mean, earlier["count_mean"], "G baseline count means")
            require_same_wire(
                [
                    str(F(mean[q]) * F((-1) ** q, 2 ** (q + 1)) / F(case["density"]) ** q)
                    for q in range(4)
                ],
                earlier["coefficient_mean"],
                "G baseline coefficient means",
            )
            baseline += 1
            states += 1
    for h, g in zip(a["histories"], old["histories"], strict=True):
        for field in (
            "history_id",
            "case_index",
            "stage1_mask",
            "final_mask",
            "conditional_probability",
            "joint_probability",
        ):
            require_same_wire(h[field], g[field], "G history law")
        require_same_wire(
            {n: h["candidate_classes"][n] for n in CANDIDATES[:9]},
            g["candidate_classes"],
            "G candidate history class IDs",
        )
        histories += 1
    require_same_wire(
        {n: a["candidate_partitions"][n] for n in CANDIDATES[:9]},
        old["candidate_partitions"],
        "G full candidate partitions",
    )
    require_same_wire(
        [row[:9] for row in a["candidate_refinement"][:9]],
        old["candidate_refinement"],
        "G candidate refinement matrix",
    )
    require(
        (states, observations, histories, baseline) == (608, 6804, 6804, 608), "prior check totals"
    )
    return {
        "source_cases_checked": 10,
        "state_rows_checked": states,
        "observation_rows_checked": observations,
        "current_histories_checked": histories,
        "original_candidate_partitions_checked": 9,
        "original_candidate_history_assignments_checked": histories * 9,
        "baseline_repeat_predictions_checked": baseline,
        "prior_executors_imported": False,
        "prior_geometric_and_quantum_bridge": old_suite["prior_bridge"][
            "prior_geometric_and_quantum_bridge"
        ],
        "scope": "Pinned G identities and baseline finite predictions, not new quantum/geometric validation.",
    }


def run_suite():
    direct = load("qr05h_capture_direct", "portability.py")
    oracle = load("qr05h_capture_reference", "reference_qr05h.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), oracle.analyze(problem)
    require_same_wire(a, b, "independent complete H outputs differ")
    check_analysis(a)
    rejections = []
    for i, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (("observed_order", direct), ("full_source_oracle", oracle)):
            try:
                module.analyze(invalid)
            except (ValueError, TypeError):
                rejected.append(name)
            else:
                raise ValueError("malformed H problem accepted")
        rejections.append({"fixture_index": i, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "controls": controls(a),
        "prior_bridge": prior_bridge(a),
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "Exact finite predictive portability and distinct fine/coarse change-of-measure contracts for a fixed three-policy menu.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "exact_component_bits": 4096,
        },
        "policy_menu": list(POLICIES),
        "policy_menu_is_a_mixture": False,
        "pooled_class_mass_interpretation": "sum of ten design masses, total10; no source or policy prior",
        "transport_level": "labeled induced observations on each supplied S, then joint count pushforward",
        "unsupported_measures_renormalized": False,
        "unknown_laws_inferred": False,
        "dynamic_closure_established": False,
        "minimal_bit_cost_claimed": False,
        "quantum_channel_constructed": False,
        "gravity_derived": False,
        "continuum_limit_established": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
    }
    bits = retained_bits(suite)
    require(bits <= 4096, "exact component cap")
    tr = [t for c in a["cases"] for s in c["states"] for t in s["transports"]]
    positive_tr = [
        t
        for c in a["cases"]
        for s in c["states"]
        if F(s["probability"]) > 0
        for t in s["transports"]
    ]
    suite["totals"] = {
        **a["counts"],
        "rejected_fixtures": len(rejections),
        "candidate_classes": {n: len(a["candidate_partitions"][n]) for n in CANDIDATES},
        "target_classes": {n: len(a["target_partitions"][n]) for n in TARGETS},
        "transports_with_fine_support": sum(t["fine_supported"] for t in tr),
        "transports_with_coarse_support": sum(t["coarse_supported"] for t in tr),
        "coarse_supported_fine_unsupported": sum(
            t["coarse_supported"] and not t["fine_supported"] for t in tr
        ),
        "fine_weights_not_count_measurable": sum(not t["fine_weight_count_measurable"] for t in tr),
        "positive_state_transports": len(positive_tr),
        "positive_state_coarse_supported_fine_unsupported": sum(
            t["coarse_supported"] and not t["fine_supported"] for t in positive_tr
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
