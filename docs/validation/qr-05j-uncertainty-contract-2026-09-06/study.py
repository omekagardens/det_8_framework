"""QR-05J exact finite sampling capture and read-only replay."""

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
from functools import cache as memoize
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05j-results-v1"
BASE_COMMIT = "da75a0ea9cb7e61277004abf698b0d0eb82b3a92"
SOURCES = (
    "README.md",
    "uncertainty.py",
    "reference_qr05j.py",
    "study.py",
    "test_qr05j.py",
    "test_capture.py",
)
PRIORS = {
    "qr-05i-analytic-portability-2026-09-06/results.json": "9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798",
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
    "pair_graded",
)
TARGETS = ("analytic_means", "analytic_second")
I_CANDIDATES = CANDIDATES[:-1]
I_TARGETS = ("analytic_means", "analytic_counts")
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


def fixtures():
    return [{"schema_version": "det8-qr05j-problem-v1", "family": "qr05i_chain_pairs"}]


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
        [token, state["pair_graded"]],
    ]
    keys = {n: base + tail for n, tail in zip(CANDIDATES, extra, strict=True)}
    signatures = {
        "analytic_means": state["mean_polynomials"],
        "analytic_second": state["pair_graded"],
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
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        ]
    )
)


@memoize
def _evaluate(table, x, y):
    return sum(
        (c * x**i * y**j for i, row in enumerate(table) for j, c in enumerate(row) if c), F(0)
    )


def evaluate(table, x, y):
    return _evaluate(tuple(tuple(row) for row in table), x, y)


def check_tensor(value, shape, nonnegative=False):
    if not shape:
        require(
            type(value) is int and (not nonnegative or value >= 0), "native coefficient type/sign"
        )
        return
    require(type(value) is list and len(value) == shape[0], "tensor shape")
    for child in value:
        check_tensor(child, shape[1:], nonnegative)


def convolve(left, right):
    result = [[0] * 7 for _ in range(7)]
    for a, row in enumerate(left):
        for b, x in enumerate(row):
            for c, row2 in enumerate(right):
                for d, y in enumerate(row2):
                    result[a + c][b + d] += x * y
    return result


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


def policy_vector(case, state, policy):
    if policy != "block_coin":
        rates = (F(1, 2), F(1, 2)) if policy == "iid_half" else (F(1, 3), F(2, 3))
        return subset_vector(case, state, *rates)
    blocks = [
        sum(
            1 << bit
            for bit, vertex in enumerate(case["eligible"])
            if state["mask"] & (1 << bit) and vertex % 2 == parity
        )
        for parity in (1, 0)
    ]
    return [
        F(
            sum(
                ((blocks[0] if coin & 1 else 0) | (blocks[1] if coin & 2 else 0)) == obs["mask"]
                for coin in range(4)
            ),
            4,
        )
        for obs in state["observations"]
    ]


@memoize
def _direct_moments(counts, probabilities):
    require(sum(probabilities, F(0)) == 1 and min(probabilities) >= 0, "supplied probability law")
    mean = tuple(
        sum((p * z[q] for z, p in zip(counts, probabilities, strict=True)), F(0)) for q in range(4)
    )
    raw = tuple(
        tuple(
            sum((p * z[q] * z[r] for z, p in zip(counts, probabilities, strict=True)), F(0))
            for r in range(4)
        )
        for q in range(4)
    )
    # Center the outcomes independently instead of defining covariance by subtraction.
    cov = tuple(
        tuple(
            sum(
                (
                    p * (z[q] - mean[q]) * (z[r] - mean[r])
                    for z, p in zip(counts, probabilities, strict=True)
                ),
                F(0),
            )
            for r in range(4)
        )
        for q in range(4)
    )
    return mean, raw, cov


def direct_moments(state, probabilities):
    return _direct_moments(
        tuple(tuple(o["chain_counts"]) for o in state["observations"]), tuple(probabilities)
    )


def evaluated_moments(state, x, y):
    return (
        tuple(evaluate(t, x, y) for t in state["mean_polynomials"]),
        tuple(tuple(evaluate(t, x, y) for t in row) for row in state["pair_graded"]),
        tuple(tuple(evaluate(t, x, y) for t in row) for row in state["covariance_polynomials"]),
    )


def matrix_wire(matrix):
    return [[str(v) for v in row] for row in matrix]


def prediction_wire(mean, raw, covariance):
    alpha = [F((-1) ** q, 2 ** (q + 1) * 12**q) for q in range(4)]
    return {
        "count_mean": list(map(str, mean)),
        "count_second_moment": matrix_wire(raw),
        "count_covariance": matrix_wire(covariance),
        "coefficient_mean": [str(alpha[q] * mean[q]) for q in range(4)],
        "coefficient_covariance": [
            [str(alpha[q] * alpha[r] * covariance[q][r]) for r in range(4)] for q in range(4)
        ],
    }


@memoize
def principal_minors(matrix):
    values = []
    for mask in range(1, 8):
        ids = [i + 1 for i in range(3) if mask & (1 << i)]
        n = len(ids)
        total = F(0)
        for perm in permutations(range(n)):
            inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
            term = F((-1) ** inversions)
            for i, j in enumerate(perm):
                term *= matrix[ids[i]][ids[j]]
            total += term
        values.append(total)
    return tuple(values)


def check_covariance(matrix):
    require(len(matrix) == 4 and all(len(row) == 4 for row in matrix), "evaluated covariance shape")
    require(
        all(matrix[q][r] == matrix[r][q] for q in range(4) for r in range(4)), "covariance symmetry"
    )
    require(all(matrix[0][r] == matrix[r][0] == 0 for r in range(4)), "constant-count covariance")
    minors = principal_minors(tuple(tuple(row) for row in matrix))
    require(min(minors) >= 0, "evaluated covariance is not positive semidefinite")
    return minors


def block_from_corners(state):
    corners = [evaluated_moments(state, F(x), F(y)) for x, y in ((0, 0), (1, 0), (0, 1), (1, 1))]
    require(all(v == 0 for _, _, cov in corners for row in cov for v in row), "corner covariance")
    for mean, raw, _ in corners:
        require(all(v.denominator == 1 for v in mean), "deterministic corner counts")
        require(
            all(raw[q][r] == mean[q] * mean[r] for q in range(4) for r in range(4)),
            "deterministic corner raw moments",
        )
    mean = tuple(sum((m[q] for m, _, _ in corners), F(0)) / 4 for q in range(4))
    raw = tuple(
        tuple(sum((r[q][k] for _, r, _ in corners), F(0)) / 4 for k in range(4)) for q in range(4)
    )
    cov = tuple(tuple(raw[q][r] - mean[q] * mean[r] for r in range(4)) for q in range(4))
    centered = tuple(
        tuple(
            sum(((m[q] - mean[q]) * (m[r] - mean[r]) for m, _, _ in corners), F(0)) / 4
            for r in range(4)
        )
        for q in range(4)
    )
    require(cov == centered, "between-corner total covariance")
    return mean, raw, cov


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
    require(len(AUDIT_POINTS) == 22, "audit point count")
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
        "pair_instances": 0,
        "pair_coefficient_cells": 0,
        "covariance_coefficient_cells": 0,
        "mean_coefficient_cells": 0,
        "predictions": 0,
    }
    cursor = 0
    for ci, case in enumerate(a["cases"]):
        require((case["profile"], case["design"]) == PAIRS[ci], "case order")
        width = len(case["eligible"])
        require(len(case["states"]) == 1 << width, "state enumeration")
        require(
            sum((F(s["probability"]) for s in case["states"]), F(0)) == 1, "first law normalized"
        )
        for si, state in enumerate(case["states"]):
            require(state["mask"] == si, "state order")
            eligible = [v for j, v in enumerate(case["eligible"]) if si & (1 << j)]
            sizes = [sum(v % 2 == 1 for v in eligible), sum(v % 2 == 0 for v in eligible)]
            require_same_wire(state["color_sizes"], sizes, "eligible-only color sizes")
            require(max(sizes) <= 3, "frame degree bound")
            obs = state["observations"]
            require(
                [o["mask"] for o in obs] == [u for u in range(1 << width) if u & ~si == 0],
                "nested observation order",
            )
            d, b, k = (
                state["mean_polynomials"],
                state["pair_graded"],
                state["covariance_polynomials"],
            )
            check_tensor(d, (4, 4, 4), True)
            check_tensor(b, (4, 4, 4, 4), True)
            check_tensor(k, (4, 4, 7, 7))
            require_same_wire(d, state["color_graded"], "mean coefficients equal D")
            for q in range(4):
                require_same_wire(b[0][q], d[q], "B zero row recovers means")
                require(sum(sum(row) for row in d[q]) == state["chain_counts"][q], "mean total")
                for degree in range(4):
                    require(
                        sum(d[q][i][j] for i in range(4) for j in range(4) if i + j == degree)
                        == state["graded_counts"][q][degree],
                        "D-to-C grading",
                    )
                for r in range(4):
                    require_same_wire(b[q][r], b[r][q], "pair symmetry")
                    require_same_wire(k[q][r], k[r][q], "covariance coefficient symmetry")
                    require(
                        sum(sum(row) for row in b[q][r])
                        == state["chain_counts"][q] * state["chain_counts"][r],
                        "ordered pair multiplicity",
                    )
                    require(
                        all(
                            b[q][r][i][j] == 0
                            for i in range(4)
                            for j in range(4)
                            if i > sizes[0] or j > sizes[1] or i + j > q + r
                        ),
                        "pair union degree",
                    )
                    product = convolve(d[q], d[r])
                    for i in range(7):
                        for j in range(7):
                            raw = b[q][r][i][j] if i < 4 and j < 4 else 0
                            require(
                                k[q][r][i][j] == raw - product[i][j], "full covariance convolution"
                            )
                            if i + j > q + r or q == 0 or r == 0:
                                require(k[q][r][i][j] == 0, "covariance degree/constant boundary")
            for x, y in AUDIT_POINTS:
                actual = evaluated_moments(state, x, y)
                expected = direct_moments(state, subset_vector(case, state, x, y))
                require(actual == expected, "direct centered moment evaluation")
                check_covariance(actual[2])
                require(
                    all(v >= 0 for row in actual[2] for v in row),
                    "count-indicator covariance monotonicity",
                )
            block = block_from_corners(state)
            check_covariance(block[2])
            require_same_wire(sorted(state["predictions"]), sorted(POLICIES), "policy names")
            for policy in POLICIES:
                moments = (
                    evaluated_moments(state, F(1, 2), F(1, 2))
                    if policy == "iid_half"
                    else evaluated_moments(state, F(1, 3), F(2, 3))
                    if policy == "iid_color"
                    else block
                )
                direct = direct_moments(state, policy_vector(case, state, policy))
                require(moments == direct, "policy moments from labeled outcomes")
                require_same_wire(
                    state["predictions"][policy],
                    prediction_wire(*moments),
                    "all evaluated/scaled prediction fields",
                )
            current_total = F(0)
            for observation in obs:
                conditional = current_kernel(case["design"], si, observation["mask"])
                current_total += conditional
                mass = conditional * F(state["probability"])
                h = a["histories"][cursor]
                require_same_wire(
                    {
                        key: h[key]
                        for key in (
                            "history_id",
                            "case_index",
                            "stage1_mask",
                            "final_mask",
                            "conditional_probability",
                            "joint_probability",
                        )
                    },
                    {
                        "history_id": cursor,
                        "case_index": ci,
                        "stage1_mask": si,
                        "final_mask": observation["mask"],
                        "conditional_probability": str(conditional),
                        "joint_probability": str(mass),
                    },
                    "history identity",
                )
                cursor += 1
                totals["positive_histories" if mass else "zero_histories"] += 1
                if not mass:
                    require_same_wire(
                        h["candidate_classes"], {n: None for n in CANDIDATES}, "zero candidate"
                    )
                    require_same_wire(
                        h["target_classes"], {n: None for n in TARGETS}, "zero target"
                    )
            require(current_total == 1, "current law normalized")
            totals["states"] += 1
            totals["positive_states"] += int(F(state["probability"]) > 0)
            totals["observations"] += len(obs)
            totals["pair_instances"] += sum(state["chain_counts"]) ** 2
            totals["pair_coefficient_cells"] += 256
            totals["covariance_coefficient_cells"] += 784
            totals["mean_coefficient_cells"] += 64
            totals["predictions"] += 3
    require(cursor == len(a["histories"]), "history cover")
    require_same_wire(a["counts"], totals, "all measured counts")
    require_same_wire(
        {
            key: totals[key]
            for key in (
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
            "candidates": 13,
            "targets": 2,
        },
        "frozen universe",
    )
    require_same_wire(sorted(a["candidate_partitions"]), sorted(CANDIDATES), "candidate names")
    require_same_wire(sorted(a["target_partitions"]), sorted(TARGETS), "target names")
    positive = [h for h in a["histories"] if F(h["joint_probability"])]
    audit_partitions(a, positive)
    require(
        all(
            h["candidate_classes"]["pair_graded"] == h["target_classes"]["analytic_second"]
            for h in positive
        ),
        "pair-graded second-moment membership equivalence",
    )
    require(
        all(
            h["candidate_classes"]["color_graded"] == h["target_classes"]["analytic_means"]
            for h in positive
        ),
        "mean grading membership equivalence",
    )
    require(a["target_refinement"][1][0] is True, "raw second moments refine means")
    return {
        "distinct_points_per_state": 22,
        "state_point_checks": 608 * 22,
        "raw_coefficient_cells_checked": 608 * 256,
        "covariance_convolution_cells_checked": 608 * 784,
        "covariance_matrices_psd_checked": 608 * 23,
        "principal_minors_checked": 608 * 23 * 7,
        "deterministic_corner_checks": 608 * 4,
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
    old_suite = prior_json("qr-05i-analytic-portability-2026-09-06/results.json")["suite"]
    old = old_suite["analysis"]
    require_same_wire(
        {n: a["candidate_partitions"][n] for n in I_CANDIDATES},
        old["candidate_partitions"],
        "all twelve I candidate identities",
    )
    require_same_wire(
        [row[:12] for row in a["candidate_refinement"][:12]],
        old["candidate_refinement"],
        "I candidate refinement",
    )
    require_same_wire(
        a["target_partitions"]["analytic_means"],
        old["target_partitions"]["analytic_means"],
        "I complete mean partition",
    )
    coefficient_cells = 0
    for case, previous in zip(a["cases"], old["cases"], strict=True):
        require_same_wire(
            {k: v for k, v in case.items() if k != "states"},
            {k: v for k, v in previous.items() if k != "states"},
            "I source/frame identity",
        )
        for state, prior in zip(case["states"], previous["states"], strict=True):
            require_same_wire(
                {
                    k: v
                    for k, v in state.items()
                    if k not in ("pair_graded", "covariance_polynomials", "predictions")
                },
                {k: v for k, v in prior.items() if k != "count_polynomials"},
                "I complete state identity",
            )
            atoms = prior["count_polynomials"]
            for q in range(4):
                for r in range(4):
                    table = [
                        [
                            sum(
                                atom["counts"][q] * atom["counts"][r] * atom["coefficients"][i][j]
                                for atom in atoms
                            )
                            for j in range(4)
                        ]
                        for i in range(4)
                    ]
                    require_same_wire(
                        state["pair_graded"][q][r],
                        table,
                        "pair unions equal pinned full-law raw moments",
                    )
                    coefficient_cells += 16
    rows, reverse = [], []
    for h, previous in zip(a["histories"], old["histories"], strict=True):
        current = {k: v for k, v in h.items() if k != "target_classes"}
        current["candidate_classes"] = {n: h["candidate_classes"][n] for n in I_CANDIDATES}
        require_same_wire(
            current,
            {k: v for k, v in previous.items() if k != "target_classes"},
            "I complete current history",
        )
        if F(h["joint_probability"]):
            rows.append((h["history_id"], h["target_classes"], previous["target_classes"]))
            reverse.append((h["history_id"], previous["target_classes"], h["target_classes"]))
    comparisons = {}
    for name in TARGETS:
        comparisons[name] = {}
        for prior in I_TARGETS:
            forward, backward = comparison(rows, name, prior), comparison(reverse, prior, name)
            comparisons[name][prior] = {
                "current_refines_prior": forward,
                "prior_refines_current": backward,
                "same_partition": forward["refines"] and backward["refines"],
            }
    require(comparisons["analytic_means"]["analytic_means"]["same_partition"], "means unchanged")
    require(
        comparisons["analytic_second"]["analytic_means"]["current_refines_prior"]["refines"],
        "second moments include means",
    )
    require(
        comparisons["analytic_second"]["analytic_counts"]["prior_refines_current"]["refines"],
        "complete laws determine second moments",
    )
    return {
        "I_artifact": "qr-05i-analytic-portability-2026-09-06/results.json",
        "I_states_matched": 608,
        "I_histories_matched": 6804,
        "I_candidate_partitions_matched": 12,
        "I_raw_moment_coefficient_cells_matched": coefficient_cells,
        "target_comparisons": comparisons,
        "prior_executors_imported": False,
        "I_full_laws_retained_in_primary_output": False,
        "prior_transports_recomputed": False,
        "prior_geometric_and_quantum_bridge": old_suite["prior_bridge"][
            "prior_geometric_and_quantum_bridge"
        ],
        "scope": "Pinned I identities and raw moments of its full count polynomials; no new quantum/geometric validation.",
    }


def find_history(a, case_index, mask):
    return next(
        h
        for h in a["histories"]
        if h["case_index"] == case_index and h["stage1_mask"] == mask and h["final_mask"] == 0
    )


def sparse_table(terms, size):
    table = [[0] * size for _ in range(size)]
    for i, j, c in terms:
        table[i][j] = c
    return table


def abstract_moment_alias():
    laws = [
        [
            {"counts": [1, 0, 0, 0], "probability": "1/2"},
            {"counts": [1, 2, 0, 0], "probability": "1/2"},
        ],
        [
            {"counts": [1, 0, 0, 0], "probability": "1/3"},
            {"counts": [1, 1, 0, 0], "probability": "1/2"},
            {"counts": [1, 3, 0, 0], "probability": "1/6"},
        ],
    ]
    values = []
    thirds = []
    for law in laws:
        counts = tuple(tuple(z["counts"]) for z in law)
        probabilities = tuple(F(z["probability"]) for z in law)
        moments = _direct_moments(counts, probabilities)
        values.append(prediction_wire(*moments))
        thirds.append(
            str(sum((p * z[1] ** 3 for z, p in zip(counts, probabilities, strict=True)), F(0)))
        )
    require_same_wire(values[0], values[1], "abstract moments agree")
    require(
        values[0]["count_mean"] == ["1", "1", "0", "0"]
        and values[0]["count_second_moment"][1][1] == "2"
        and values[0]["count_covariance"][1][1] == "1"
        and thirds == ["4", "5"],
        "abstract same moments unequal third",
    )
    require(canonical(laws[0]) != canonical(laws[1]), "abstract laws differ")
    return {
        "scope": "Abstract probability distributions on four-count vectors, not claimed induced-order IID laws in this gate.",
        "laws": laws,
        "common_moments": values[0],
        "third_moment_N1": thirds,
        "equal_first_and_second_moments": True,
        "equal_laws": False,
    }


def controls(a):
    cases = a["cases"]
    states = cases[0]["states"]
    singleton, pair = states[1], states[5]
    require_same_wire(
        singleton["pair_graded"][1][1],
        sparse_table([(1, 0, 1)], 4),
        "self-pair union not independent product",
    )
    require_same_wire(
        singleton["covariance_polynomials"][1][1],
        sparse_table([(1, 0, 1), (2, 0, -1)], 7),
        "singleton variance",
    )
    require_same_wire(
        pair["pair_graded"][1][1],
        sparse_table([(1, 0, 2), (2, 0, 2)], 4),
        "both off-diagonal orientations",
    )
    require_same_wire(
        pair["covariance_polynomials"][1][1],
        sparse_table([(1, 0, 2), (2, 0, -2)], 7),
        "pair variance",
    )
    require(
        pair["predictions"]["iid_half"]["count_covariance"][1][1] == "1/2"
        and pair["predictions"]["block_coin"]["count_covariance"][1][1] == "1",
        "block mixture versus half variance",
    )
    star, path = states[57], states[27]
    require_same_wire(star["mean_polynomials"], path["mean_polynomials"], "star/path equal means")
    difference = [
        [
            star["covariance_polynomials"][2][2][i][j] - path["covariance_polynomials"][2][2][i][j]
            for j in range(7)
        ]
        for i in range(7)
    ]
    require_same_wire(
        difference, sparse_table([(1, 2, 2), (2, 2, -2)], 7), "star/path overlap difference"
    )
    require_same_wire(
        star["predictions"]["block_coin"],
        path["predictions"]["block_coin"],
        "star/path block uncertainty agrees",
    )
    variances = {
        p: [s["predictions"][p]["count_covariance"][2][2] for s in (star, path)]
        for p in ("iid_half", "iid_color")
    }
    require(
        variances == {"iid_half": ["15/16", "13/16"], "iid_color": ["68/81", "52/81"]},
        "retained star/path variances",
    )
    shared = states[41]
    require_same_wire(
        shared["pair_graded"][2][2],
        sparse_table([(1, 1, 2), (1, 2, 2)], 4),
        "shared root once and cross pairs twice",
    )
    require_same_wire(
        shared["covariance_polynomials"][2][2],
        sparse_table([(1, 1, 2), (1, 2, 2), (2, 2, -4)], 7),
        "shared-root variance",
    )
    submatrices = {}
    for p, expected in (
        ("iid_half", [["3/4", "1/2"], ["1/2", "1/2"]]),
        ("block_coin", [["5/4", "3/4"], ["3/4", "3/4"]]),
    ):
        actual = [
            [shared["predictions"][p]["count_covariance"][q][r] for r in (1, 2)] for q in (1, 2)
        ]
        require_same_wire(actual, expected, "shared-root evaluated covariance")
        submatrices[p] = actual
    edge = evaluated_moments(shared, F(0), F(1, 2))
    require(
        edge[2][1][1] == F(1, 2) and edge[2][2][2] == 0, "edge is not necessarily deterministic"
    )
    chain_odd, chain_even = cases[6]["states"][21], cases[6]["states"][42]
    for state, raw, cov in (
        (chain_odd, [(3, 0, 1)], [(3, 0, 1), (6, 0, -1)]),
        (chain_even, [(0, 3, 1)], [(0, 3, 1), (0, 6, -1)]),
    ):
        require_same_wire(state["pair_graded"][3][3], sparse_table(raw, 4), "triple raw moment")
        require_same_wire(
            state["covariance_polynomials"][3][3],
            sparse_table(cov, 7),
            "triple requires degree six",
        )
    fixed, fixed_random = cases[9]["states"][0], cases[9]["states"][16]
    require(
        fixed["color_sizes"] == [0, 0] and fixed["pair_graded"][1][1][0][0] == 1,
        "fixed-only chain deterministic second moment",
    )
    require_same_wire(
        fixed["covariance_polynomials"][1][1], sparse_table([], 7), "fixed variance zero"
    )
    require_same_wire(
        fixed_random["pair_graded"][1][2],
        sparse_table([(0, 1, 2)], 4),
        "fixed eligible overlap multiplicity",
    )
    require_same_wire(
        fixed_random["covariance_polynomials"][1][2],
        sparse_table([(0, 1, 1), (0, 2, -1)], 7),
        "fixed vertex not randomly weighted",
    )
    histories = {}
    for label, ci, masks in (
        ("singleton", 0, [1]),
        ("ordered_pair", 0, [5]),
        ("star_path", 0, [57, 27]),
        ("shared_root", 0, [41]),
        ("degree_six", 6, [21, 42]),
        ("fixed", 9, [0, 16]),
    ):
        hs = [find_history(a, ci, mask) for mask in masks]
        require(
            all(F(h["joint_probability"]) > 0 for h in hs), "controls must use supported histories"
        )
        histories[label] = [h["history_id"] for h in hs]
    for candidate in ("full_record", "color_order", "pair_graded"):
        require(
            all(a["assessments"][candidate][t]["sufficient"] for t in TARGETS),
            "constructive sufficient positive control",
        )
    require(
        a["assessments"]["color_graded"]["analytic_means"]["sufficient"] is True
        and a["assessments"]["color_graded"]["analytic_second"]["sufficient"] is False,
        "means insufficient for uncertainty",
    )
    return {
        "singleton_self_overlap": {
            "history_ids": histories["singleton"],
            "raw_N1_second": singleton["pair_graded"][1][1],
            "variance_N1": singleton["covariance_polynomials"][1][1],
        },
        "ordered_pair_and_mixture": {
            "history_ids": histories["ordered_pair"],
            "raw_N1_second": pair["pair_graded"][1][1],
            "iid_half_variance": "1/2",
            "block_variance": "1",
            "mean_corner_covariance": "0",
            "omitting_one_cross_orientation_raw_at_x1": "3",
            "correct_raw_at_x1": "4",
        },
        "star_path": {
            "history_ids": histories["star_path"],
            "equal_mean_polynomials": True,
            "equal_second_moment_polynomials": False,
            "variance_N2": variances,
            "variance_difference_polynomial": difference,
            "equal_block_moments": True,
        },
        "shared_root": {
            "history_ids": histories["shared_root"],
            "raw_N2_second": shared["pair_graded"][2][2],
            "variance_N2": shared["covariance_polynomials"][2][2],
            "covariance_N1_N2_submatrices": submatrices,
            "edge_point": ["0", "1/2"],
            "edge_variance_N1": "1/2",
            "edge_variance_N2": "0",
        },
        "degree_six": {
            "history_ids": histories["degree_six"],
            "odd_covariance_N3": chain_odd["covariance_polynomials"][3][3],
            "even_covariance_N3": chain_even["covariance_polynomials"][3][3],
        },
        "fixed_eligible": {
            "history_ids": histories["fixed"],
            "fixed_only_second_N1": "1",
            "fixed_only_variance_N1": "0",
            "fixed_random_raw_N1_N2": fixed_random["pair_graded"][1][2],
            "fixed_random_covariance_N1_N2": fixed_random["covariance_polynomials"][1][2],
        },
        "moment_law_alias": abstract_moment_alias(),
    }


def run_suite():
    direct = load("qr05j_capture_direct", "uncertainty.py")
    oracle = load("qr05j_capture_reference", "reference_qr05j.py")
    problem = fixtures()[0]
    a, b = direct.analyze(problem), oracle.analyze(problem)
    require_same_wire(a, b, "independent complete J outputs differ")
    audit = check_analysis(a)
    rejections = []
    for i, invalid in enumerate(invalid_fixtures()):
        rejected = []
        for name, module in (("observed_chain_pairs", direct), ("full_law_moments", oracle)):
            try:
                module.analyze(invalid)
            except (ValueError, TypeError):
                rejected.append(name)
            else:
                raise ValueError("malformed J problem accepted")
        rejections.append({"fixture_index": i, "input": invalid, "rejected_by": rejected})
    suite = {
        "input": problem,
        "analysis": a,
        "audit": audit,
        "controls": controls(a),
        "prior_bridge": prior_bridge(a),
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "Constructive exact mean/covariance sufficiency from eligible-union-graded ordered chain pairs, independently checked against full count laws.",
        "bounds": {
            "events_per_source": 8,
            "eligible_per_source_max": 6,
            "chain_order_max": 3,
            "raw_moment_bidegree_max": [3, 3],
            "covariance_bidegree_cap": [6, 6],
            "covariance_total_degree_max": 6,
            "exact_component_bits": 4096,
        },
        "parameter_domain": "[0,1]^2",
        "audit_points": [[str(x), str(y)] for x, y in AUDIT_POINTS],
        "primary_constructs_full_laws": False,
        "ordered_pair_multiplicity_retained": True,
        "self_pairs_retained": True,
        "fixed_vertices_randomized": False,
        "covariance_uses_complete_mean_convolution": True,
        "block_covariance_includes_between_corner_variation": True,
        "coefficient_matrices_assumed_psd": False,
        "positive_definiteness_required": False,
        "general_contract_basis": "Explicit finite-indicator and covariance arguments in README; executions are not machine-checked universal proofs.",
        "pooled_class_mass_interpretation": "sum of ten design masses, total10; no source or policy prior",
        "moment_equality_is_general_full_law_certificate": False,
        "minimal_bit_cost_claimed": False,
        "application_speedup_measured": False,
        "arbitrary_correlated_laws_covered": False,
        "unknown_acquisition_laws_inferred": False,
        "empirical_covariance_calibration_tested": False,
        "dynamic_closure_established": False,
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
        "prior_target_comparisons": len(TARGETS) * len(I_TARGETS),
        "max_pair_coefficient": max(
            v
            for c in a["cases"]
            for s in c["states"]
            for row in s["pair_graded"]
            for t in row
            for r in t
            for v in r
        ),
        "max_absolute_covariance_coefficient": max(
            abs(v)
            for c in a["cases"]
            for s in c["states"]
            for row in s["covariance_polynomials"]
            for t in row
            for r in t
            for v in r
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
