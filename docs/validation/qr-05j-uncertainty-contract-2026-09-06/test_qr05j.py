"""Independent subset-outcome uncertainty tests; no earlier executor imports."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, permutations, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
I_SHA = "9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798"
CASES = (
    ("ferrers6", "independent"),
    ("ferrers6", "parity_adaptive"),
    ("ferrers6", "common_coin"),
    ("ferrers6", "parity_hole"),
    ("ferrers6", "first_pair"),
    ("standard_example3", "independent"),
    ("chain6", "parity_adaptive"),
    ("chain6", "parity_hole"),
    ("chain6", "first_pair"),
    ("ferrers6_fixed", "independent"),
)
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
POLICIES = ("iid_half", "iid_color", "block_coin")
POINTS = tuple(
    dict.fromkeys(
        (
            *product((F(0), F(1, 3), F(2, 3), F(1)), repeat=2),
            (F(1, 2), F(1, 2)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        )
    )
)


def problem():
    return {"schema_version": "det8-qr05j-problem-v1", "family": "qr05i_chain_pairs"}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module name already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05j_test_direct", "uncertainty.py"),
        private_module("_qr05j_test_reference", "reference_qr05j.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def pinned_i():
    path = HERE.parent / "qr-05i-analytic-portability-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == I_SHA
    artifact = json.loads(raw)
    # Descriptive runtime floats belong to the envelope, never the exact suite.
    assert (
        json.dumps(artifact, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(artifact["suite"])
    return artifact["suite"]["analysis"]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05j_test_aggregate", "study.py")
    return runner, runner.run_suite()


def native(value):
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict:
        assert all(type(key) is str for key in value)
        for item in value.values():
            native(item)
        return
    raise AssertionError(f"non-native exact mathematical value {type(value)}")


def wire(value):
    native(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


@cache
def population(profile):
    past = [[]]
    for j in range(6):
        if profile == "chain6":
            before = list(range(1, j + 1))
        elif j < 3:
            before = []
        else:
            before = [
                i + 1
                for i in range(3)
                if (i != j - 3 if profile == "standard_example3" else i <= j - 3)
            ]
        past.append([0, *before])
    past.append(list(range(7)))
    fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
    eligible = [v for v in range(8) if v not in fixed]
    return past, fixed, eligible


@cache
def observed(profile, mask):
    source, fixed, eligible = population(profile)
    kept = sorted(fixed + [v for j, v in enumerate(eligible) if mask & (1 << j)])
    past = [[i for i, v in enumerate(kept) if v in source[target]] for target in kept]
    local = {v: i for i, v in enumerate(kept)}
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    counts = []
    for q in range(4):
        number = 0
        for vertices in combinations([v for v in kept if 0 < v < 7], q):
            if all(local[a] in past[local[b]] for a, b in pairwise([0, *vertices, 7])):
                support = [v for v in vertices if v in eligible]
                odd = sum(v % 2 for v in support)
                d[q][odd][len(support) - odd] += 1
                number += 1
        counts.append(number)
    odd = sum(v % 2 for v in kept if v in eligible)
    return (
        {"mask": mask, "kept": kept, "past": past, "chain_counts": counts},
        d,
        (odd, mask.bit_count() - odd),
    )


@cache
def submasks(s):
    return [u for u in range(s + 1) if u & s == u]


@cache
def raw_coefficients(profile, s):
    # This is a subset-outcome Bernstein inventory, not chain-pair enumeration.
    odd, even = observed(profile, s)[2]
    sums = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for u in submasks(s):
        observation, _, (o, e) = observed(profile, u)
        z = observation["chain_counts"]
        for q in range(4):
            for r in range(4):
                sums[q][r][o][e] += z[q] * z[r]
    result = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for r in range(4):
            for a in range(odd + 1):
                for b in range(even + 1):
                    result[q][r][a][b] = sum(
                        sums[q][r][o][e]
                        * (-1) ** (a - o + b - e)
                        * comb(odd - o, a - o)
                        * comb(even - e, b - e)
                        for o in range(a + 1)
                        for e in range(b + 1)
                    )
    return result


@cache
def covariance_coefficients(profile, s):
    means, raw = observed(profile, s)[1], raw_coefficients(profile, s)
    result = [[[[0] * 7 for _ in range(7)] for _ in range(4)] for _ in range(4)]
    for q in range(4):
        for r in range(4):
            for i in range(7):
                for j in range(7):
                    result[q][r][i][j] = (raw[q][r][i][j] if i < 4 and j < 4 else 0) - sum(
                        means[q][a][b] * means[r][i - a][j - b]
                        for a in range(4)
                        for b in range(4)
                        if 0 <= i - a < 4 and 0 <= j - b < 4
                    )
    return result


@cache
def evaluate_immutable(table, x, y):
    return sum(
        (F(c) * x**a * y**b for a, row in enumerate(table) for b, c in enumerate(row) if c),
        start=F(0),
    )


def evaluate(table, x, y):
    return evaluate_immutable(tuple(tuple(row) for row in table), x, y)


def numeric_moments(rows, probabilities):
    assert sum(probabilities) == 1 and all(p >= 0 for p in probabilities)
    mean = [sum(p * z[q] for z, p in zip(rows, probabilities)) for q in range(4)]
    second = [
        [sum(p * z[q] * z[r] for z, p in zip(rows, probabilities)) for r in range(4)]
        for q in range(4)
    ]
    covariance = [
        [
            sum(p * (z[q] - mean[q]) * (z[r] - mean[r]) for z, p in zip(rows, probabilities))
            for r in range(4)
        ]
        for q in range(4)
    ]
    return mean, second, covariance


@cache
def outcome_moments(profile, s, x, y, block=False):
    odd, even = observed(profile, s)[2]
    eligible = population(profile)[2]
    blocks = [
        sum(1 << j for j, v in enumerate(eligible) if s & (1 << j) and v % 2 == parity)
        for parity in (0, 1)
    ]
    blocks = [b for b in blocks if b]
    probabilities, rows = [], []
    for u in submasks(s):
        observation, _, (o, e) = observed(profile, u)
        p = (
            (F(1, 2 ** len(blocks)) if all(u & b in (0, b) for b in blocks) else F(0))
            if block
            else x**o * (1 - x) ** (odd - o) * y**e * (1 - y) ** (even - e)
        )
        probabilities.append(p)
        rows.append(observation["chain_counts"])
    return numeric_moments(rows, probabilities)


def determinant(matrix):
    total = F(0)
    n = len(matrix)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F((-1) ** inversions)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        total += term
    return total


def psd(matrix):
    assert len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    assert all(matrix[0][q] == matrix[q][0] == 0 for q in range(4))
    assert all(matrix[q][r] == matrix[r][q] for q in range(4) for r in range(4))
    minors = []
    for size in (1, 2, 3):
        for indices in combinations((1, 2, 3), size):
            minors.append(determinant([[matrix[q][r] for r in indices] for q in indices]))
    assert len(minors) == 7 and all(value >= 0 for value in minors)


def prediction(mean, second, covariance):
    alpha = [F((-1) ** q, 2 ** (q + 1) * 12**q) for q in range(4)]
    return {
        "count_mean": list(map(str, mean)),
        "count_second_moment": [list(map(str, row)) for row in second],
        "count_covariance": [list(map(str, row)) for row in covariance],
        "coefficient_mean": [str(alpha[q] * mean[q]) for q in range(4)],
        "coefficient_covariance": [
            [str(alpha[q] * alpha[r] * covariance[q][r]) for r in range(4)] for q in range(4)
        ],
    }


def test_complete_outputs_are_native_identical_and_round_trip(analyses):
    assert wire(analyses[0]) == wire(analyses[1])
    assert wire(json.loads(wire(analyses[0]))) == wire(analyses[0])
    assert set(analyses[0]) == {
        "cases",
        "histories",
        "candidate_partitions",
        "target_partitions",
        "assessments",
        "candidate_refinement",
        "target_refinement",
        "counts",
    }


@pytest.mark.parametrize("case_index", range(10))
def test_pinned_i_metadata_and_independent_observed_counts(analyses, pinned_i, case_index):
    prior = pinned_i["cases"][case_index]
    profile, design = CASES[case_index]
    for analysis in analyses:
        case = analysis["cases"][case_index]
        assert set(case) == set(prior)
        assert wire({k: v for k, v in case.items() if k != "states"}) == wire(
            {k: v for k, v in prior.items() if k != "states"}
        )
        assert case["profile"] == profile and case["design"] == design
        source, fixed, eligible = population(profile)
        assert case["past"] == source and case["fixed"] == fixed and case["eligible"] == eligible
        assert len(case["states"]) == len(prior["states"]) == 1 << len(eligible)
        for s, (state, old) in enumerate(zip(case["states"], prior["states"])):
            old_fields = set(old) - {"count_polynomials"}
            assert set(state) == old_fields | {
                "pair_graded",
                "covariance_polynomials",
                "predictions",
            }
            assert wire({k: state[k] for k in old_fields}) == wire({k: old[k] for k in old_fields})
            observation, d, sizes = observed(profile, s)
            assert wire({k: state[k] for k in observation}) == wire(observation)
            assert wire(state["color_sizes"]) == wire(list(sizes))
            assert wire(state["mean_polynomials"]) == wire(d)
            assert wire(state["observations"]) == wire(
                [observed(profile, u)[0] for u in submasks(s)]
            )


@pytest.mark.parametrize("case_index", range(10))
def test_raw_moments_from_bernstein_outcomes_and_pinned_full_law_coefficients(
    analyses, pinned_i, case_index
):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state, old in zip(
            analysis["cases"][case_index]["states"], pinned_i["cases"][case_index]["states"]
        ):
            raw, d = raw_coefficients(profile, state["mask"]), observed(profile, state["mask"])[1]
            odd, even = state["color_sizes"]
            assert wire(state["pair_graded"]) == wire(raw)
            assert raw[0] == d
            for q in range(4):
                for r in range(4):
                    assert raw[q][r] == raw[r][q]
                    assert (
                        sum(sum(row) for row in raw[q][r])
                        == state["chain_counts"][q] * state["chain_counts"][r]
                    )
                    for o in range(4):
                        for e in range(4):
                            value = raw[q][r][o][e]
                            assert type(value) is int and value >= 0
                            if o > odd or e > even or o + e > q + r:
                                assert value == 0
                            assert value == sum(
                                atom["counts"][q] * atom["counts"][r] * atom["coefficients"][o][e]
                                for atom in old["count_polynomials"]
                            )


@pytest.mark.parametrize("case_index", range(10))
def test_every_covariance_coefficient_is_full_mean_convolution(analyses, case_index):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            cov = state["covariance_polynomials"]
            assert wire(cov) == wire(covariance_coefficients(profile, state["mask"]))
            odd, even = state["color_sizes"]
            for q in range(4):
                for r in range(4):
                    assert cov[q][r] == cov[r][q]
                    assert len(cov[q][r]) == 7 and all(len(row) == 7 for row in cov[q][r])
                    for i in range(7):
                        for j in range(7):
                            c = cov[q][r][i][j]
                            assert type(c) is int and abs(c).bit_length() <= 4096
                            if q == 0 or r == 0 or i > 2 * odd or j > 2 * even or i + j > q + r:
                                assert c == 0


@pytest.mark.parametrize("case_index", range(10))
def test_exact_evaluations_centered_gram_psd_principal_minors_and_corners(analyses, case_index):
    assert len(POINTS) == 22
    profile = CASES[case_index][0]
    # Complete dual-route identity above makes one set of costly PSD minors enough.
    for state in analyses[0]["cases"][case_index]["states"]:
        for x, y in POINTS:
            mean, second, covariance = outcome_moments(profile, state["mask"], x, y)
            assert mean == [evaluate(table, x, y) for table in state["mean_polynomials"]]
            assert second == [
                [evaluate(table, x, y) for table in row] for row in state["pair_graded"]
            ]
            assert covariance == [
                [evaluate(table, x, y) for table in row] for row in state["covariance_polynomials"]
            ]
            assert all(c >= 0 for row in covariance for c in row)
            psd(covariance)
            if x in (0, 1) and y in (0, 1):
                assert all(c == 0 for row in covariance for c in row)
            vector = (0, 1, -1, 2)
            quadratic = sum(
                vector[q] * covariance[q][r] * vector[r] for q in range(4) for r in range(4)
            )
            assert quadratic >= 0
            assert quadratic == sum(
                vector[q] * vector[r] * (second[q][r] - mean[q] * mean[r])
                for q in range(4)
                for r in range(4)
            )


@pytest.mark.parametrize("case_index", range(10))
def test_three_supplied_laws_predictions_scaling_and_total_block_covariance(analyses, case_index):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            moments = {
                "iid_half": outcome_moments(profile, s, F(1, 2), F(1, 2)),
                "iid_color": outcome_moments(profile, s, F(1, 3), F(2, 3)),
                "block_coin": outcome_moments(profile, s, F(0), F(0), True),
            }
            assert wire(state["predictions"]) == wire(
                {policy: prediction(*values) for policy, values in moments.items()}
            )
            for values in moments.values():
                pred = prediction(*values)
                psd(values[2])
                psd([[F(c) for c in row] for row in pred["coefficient_covariance"]])
            corners = [
                outcome_moments(profile, s, F(x), F(y)) for x, y in product((0, 1), repeat=2)
            ]
            assert all(c == 0 for _, _, cov in corners for row in cov for c in row)
            mean, second, covariance = moments["block_coin"]
            assert mean == [sum(values[0][q] for values in corners) / 4 for q in range(4)]
            assert second == [
                [sum(values[1][q][r] for values in corners) / 4 for r in range(4)] for q in range(4)
            ]
            assert covariance == [
                [
                    sum((values[0][q] - mean[q]) * (values[0][r] - mean[r]) for values in corners)
                    / 4
                    for r in range(4)
                ]
                for q in range(4)
            ]


@pytest.fixture(scope="session")
def partitions(pinned_i):
    targets, lookups = {t: [] for t in TARGETS}, {t: {} for t in TARGETS}
    pairs, plookup, ids, pair_ids = [], {}, [], []
    for h in pinned_i["histories"]:
        mass = F(h["joint_probability"])
        if not mass:
            ids.append({target: None for target in TARGETS})
            pair_ids.append(None)
            continue
        case = pinned_i["cases"][h["case_index"]]
        profile, s = case["profile"], h["stage1_mask"]
        final = observed(profile, h["final_mask"])[0]
        state = case["states"][s]
        base = [
            [case["design"], "12", case["fixed"], case["eligible"]],
            final["kept"],
            final["past"],
        ]
        b = raw_coefficients(profile, s)
        key = [*base, state["policy_token"], b]
        encoded = wire(key)
        if encoded not in plookup:
            index = len(pairs)
            plookup[encoded] = index
            pairs.append({"class_id": index, "members": [], "joint_mass": F(0), "key": key})
        index = plookup[encoded]
        pairs[index]["members"].append(h["history_id"])
        pairs[index]["joint_mass"] += mass
        pair_ids.append(index)
        row = {}
        for target, signature in (
            ("analytic_means", observed(profile, s)[1]),
            ("analytic_second", b),
        ):
            encoded = wire([base, signature])
            if encoded not in lookups[target]:
                index = len(targets[target])
                lookups[target][encoded] = index
                targets[target].append(
                    {
                        "class_id": index,
                        "members": [],
                        "joint_mass": F(0),
                        "base": base,
                        "signature": signature,
                    }
                )
            index = lookups[target][encoded]
            targets[target][index]["members"].append(h["history_id"])
            targets[target][index]["joint_mass"] += mass
            row[target] = index
        ids.append(row)
    for collection in (pairs, *targets.values()):
        for group in collection:
            group["joint_mass"] = str(group["joint_mass"])
    return pairs, targets, pair_ids, ids


def fiber_check(left, right, supported):
    first, collision = {}, None
    for i in supported:
        if left[i] not in first:
            first[left[i]] = i
        elif right[first[left[i]]] != right[i] and collision is None:
            collision = {"left_history": first[left[i]], "right_history": i}
    return collision is None, collision, len({(left[i], right[i]) for i in supported})


def test_histories_old_candidates_pair_partition_and_prespecified_inventory(
    analyses, pinned_i, partitions
):
    pairs, targets, pair_ids, ids = partitions
    supported = [i for i, h in enumerate(pinned_i["histories"]) if F(h["joint_probability"]) > 0]
    pair_instances = sum(
        sum(observed(case["profile"], state["mask"])[0]["chain_counts"]) ** 2
        for case in pinned_i["cases"]
        for state in case["states"]
    )
    for analysis in analyses:
        assert wire(analysis["candidate_partitions"]) == wire(
            {**pinned_i["candidate_partitions"], "pair_graded": pairs}
        )
        assert wire(analysis["target_partitions"]) == wire(targets)
        assert len(analysis["histories"]) == len(pinned_i["histories"]) == 6804
        for h, old, pair_id, target_ids in zip(
            analysis["histories"], pinned_i["histories"], pair_ids, ids
        ):
            assert set(h) == set(old)
            assert wire(
                {k: v for k, v in h.items() if k not in ("candidate_classes", "target_classes")}
            ) == wire(
                {k: v for k, v in old.items() if k not in ("candidate_classes", "target_classes")}
            )
            assert wire(h["candidate_classes"]) == wire(
                {**old["candidate_classes"], "pair_graded": pair_id}
            )
            assert wire(h["target_classes"]) == wire(target_ids)
        for collection in (analysis["candidate_partitions"], analysis["target_partitions"]):
            for groups in collection.values():
                assert sorted(i for group in groups for i in group["members"]) == supported
                assert sum(F(group["joint_mass"]) for group in groups) == 10
                assert all(group["members"] == sorted(set(group["members"])) for group in groups)
        assert wire(analysis["counts"]) == wire(
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
                "pair_instances": pair_instances,
                "pair_coefficient_cells": 608 * 256,
                "covariance_coefficient_cells": 608 * 784,
                "mean_coefficient_cells": 608 * 64,
                "predictions": 608 * 3,
            }
        )


def test_fiber_sufficiency_refinements_first_witnesses_and_pair_equivalence(
    analyses, pinned_i, partitions
):
    pairs, _, pair_ids, ids = partitions
    supported = [i for i, h in enumerate(pinned_i["histories"]) if F(h["joint_probability"]) > 0]
    cids = [
        {**h["candidate_classes"], "pair_graded": p}
        for h, p in zip(pinned_i["histories"], pair_ids)
    ]
    cmatrix = [
        [
            fiber_check([row[a] for row in cids], [row[b] for row in cids], supported)[0]
            for b in CANDIDATES
        ]
        for a in CANDIDATES
    ]
    tmatrix = [
        [
            fiber_check([row[a] for row in ids], [row[b] for row in ids], supported)[0]
            for b in TARGETS
        ]
        for a in TARGETS
    ]
    assert tmatrix == [[True, False], [True, True]]
    second = [row["analytic_second"] for row in ids]
    assert (
        fiber_check(pair_ids, second, supported)[0] and fiber_check(second, pair_ids, supported)[0]
    )
    assessments = {}
    for candidate in CANDIDATES:
        assessments[candidate] = {}
        size = (
            len(pairs)
            if candidate == "pair_graded"
            else len(pinned_i["candidate_partitions"][candidate])
        )
        for target in TARGETS:
            sufficient, collision, common = fiber_check(
                [row[candidate] for row in cids], [row[target] for row in ids], supported
            )
            assert sufficient is (common == size)
            assessments[candidate][target] = {
                "sufficient": sufficient,
                "first_collision": collision,
                "common_refinement_classes": common,
            }
    assert all(
        assessments[c][t]["sufficient"]
        for c in ("pair_graded", "color_order", "full_record")
        for t in TARGETS
    )
    assert assessments["color_graded"]["analytic_second"]["sufficient"] is False
    for analysis in analyses:
        assert wire(analysis["candidate_refinement"]) == wire(cmatrix)
        assert wire(analysis["target_refinement"]) == wire(tmatrix)
        assert wire(analysis["assessments"]) == wire(assessments)


def test_analytic_second_is_compared_to_i_full_laws_by_actual_members(pinned_i, partitions):
    _, _, _, ids = partitions
    supported = [i for i, h in enumerate(pinned_i["histories"]) if F(h["joint_probability"]) > 0]
    full = [h["target_classes"]["analytic_counts"] for h in pinned_i["histories"]]
    second = [row["analytic_second"] for row in ids]
    assert fiber_check(full, second, supported)[0]
    for target in TARGETS:
        for prior in ("analytic_means", "analytic_counts"):
            left, right = (
                [row[target] for row in ids],
                [h["target_classes"][prior] for h in pinned_i["histories"]],
            )
            forward, reverse = (
                fiber_check(left, right, supported),
                fiber_check(right, left, supported),
            )
            assert forward[2] == reverse[2]
            for result, source, destination in ((forward, left, right), (reverse, right, left)):
                if result[1]:
                    a, b = result[1]["left_history"], result[1]["right_history"]
                    assert source[a] == source[b] and destination[a] != destination[b]


def test_self_pair_ordered_multiplicity_and_shared_eligible_root_controls(analyses):
    for analysis in analyses:
        states = analysis["cases"][0]["states"]
        singleton, antichain, star = states[1], states[5], states[41]
        assert singleton["pair_graded"][1][1][1][0] == 1
        assert singleton["covariance_polynomials"][1][1][1][0] == 1
        assert singleton["covariance_polynomials"][1][1][2][0] == -1
        assert antichain["pair_graded"][1][1][1][0] == 2
        assert antichain["pair_graded"][1][1][2][0] == 2
        assert sum(sum(row) for row in antichain["pair_graded"][1][1]) == 4
        assert star["pair_graded"][2][2][1][1] == 2
        assert star["pair_graded"][2][2][1][2] == 2
        assert star["pair_graded"][2][2][2][2] == 0
        cov = star["covariance_polynomials"][2][2]
        assert cov[1][1] == cov[1][2] == 2 and cov[2][2] == -4
        assert sum(abs(c) for row in cov for c in row) == 8
        for x, y in POINTS:
            assert evaluate(cov, x, y) == 2 * x * y + 2 * x * y * y - 4 * x * x * y * y


def test_fixed_support_is_not_random_and_degree_six_terms_are_not_truncated(analyses):
    for analysis in analyses:
        fixed, edge = (analysis["cases"][9]["states"][s] for s in (0, 16))
        assert fixed["chain_counts"] == [1, 1, 0, 0]
        assert fixed["pair_graded"][1][1][0][0] == 1
        assert all(
            c == 0
            for matrix in fixed["covariance_polynomials"]
            for table in matrix
            for row in table
            for c in row
        )
        assert edge["color_sizes"] == [0, 1]
        assert edge["pair_graded"][1][2][0][1] == 2
        assert edge["pair_graded"][1][1][0][0] == 1 and edge["pair_graded"][1][1][0][1] == 3
        for x, y in POINTS:
            assert evaluate(edge["covariance_polynomials"][1][2], x, y) == y - y * y
        for mask, axis in ((21, 0), (42, 1)):
            state = analysis["cases"][6]["states"][mask]
            raw, cov = state["pair_graded"][3][3], state["covariance_polynomials"][3][3]
            a, b = (3, 0) if axis == 0 else (0, 3)
            c, d = (6, 0) if axis == 0 else (0, 6)
            assert raw[a][b] == cov[a][b] == 1 and cov[c][d] == -1
            assert sum(abs(v) for row in cov for v in row) == 2
            for x, y in POINTS:
                rate = x if axis == 0 else y
                assert evaluate(cov, x, y) == rate**3 - rate**6


def test_mixture_requires_between_corner_covariance_and_edges_can_remain_random(analyses):
    for analysis in analyses:
        state = analysis["cases"][0]["states"][41]
        half = state["predictions"]["iid_half"]["count_covariance"]
        block = state["predictions"]["block_coin"]["count_covariance"]
        assert [[half[q][r] for r in (1, 2)] for q in (1, 2)] == [["3/4", "1/2"], ["1/2", "1/2"]]
        assert [[block[q][r] for r in (1, 2)] for q in (1, 2)] == [["5/4", "3/4"], ["3/4", "3/4"]]
        for x, y in product((F(0), F(1)), repeat=2):
            assert all(
                evaluate(table, x, y) == 0
                for matrix in state["covariance_polynomials"]
                for table in matrix
            )
        assert evaluate(state["covariance_polynomials"][1][1], F(0), F(1, 2)) == F(1, 2)
        assert evaluate(state["covariance_polynomials"][2][2], F(0), F(1, 2)) == 0
        # All full covariance matrices are singular due to constant N0.
        assert determinant([[F(c) for c in row] for row in block]) == 0


def test_star_path_equal_means_do_not_determine_uncertainty(analyses):
    for analysis in analyses:
        star, path = (analysis["cases"][0]["states"][s] for s in (57, 27))
        assert star["mean_polynomials"] == path["mean_polynomials"]
        assert star["pair_graded"] != path["pair_graded"]
        assert star["covariance_polynomials"] != path["covariance_polynomials"]
        assert [
            state["predictions"]["iid_half"]["count_covariance"][2][2] for state in (star, path)
        ] == ["15/16", "13/16"]
        assert [
            state["predictions"]["iid_color"]["count_covariance"][2][2] for state in (star, path)
        ] == ["68/81", "52/81"]
        assert star["predictions"]["block_coin"] == path["predictions"]["block_coin"]


def test_abstract_equal_first_second_moments_do_not_determine_a_law():
    laws = (([0, 2], [F(1, 2), F(1, 2)]), ([0, 1, 3], [F(1, 3), F(1, 2), F(1, 6)]))
    moments, third = [], []
    for counts, probabilities in laws:
        rows = [[1, n, 0, 0] for n in counts]
        moments.append(numeric_moments(rows, probabilities))
        third.append(sum(p * n**3 for n, p in zip(counts, probabilities)))
    assert moments[0] == moments[1]
    assert moments[0][0] == [1, 1, 0, 0]
    assert moments[0][1][1][1] == 2 and moments[0][2][1][1] == 1
    assert third == [4, 5] and laws[0] != laws[1]


def test_whole_aggregate_native_exact_round_trip(aggregate):
    _, suite = aggregate
    assert wire(json.loads(wire(suite))) == wire(suite)


def test_retained_abstract_moment_alias_and_realized_control_evidence(aggregate, analyses):
    _, suite = aggregate
    controls = suite["controls"]
    alias = controls["moment_law_alias"]
    assert "not claimed induced-order" in alias["scope"]
    expected_laws = [
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
    assert wire(alias["laws"]) == wire(expected_laws)
    for law in expected_laws:
        values = numeric_moments([r["counts"] for r in law], [F(r["probability"]) for r in law])
        assert wire(alias["common_moments"]) == wire(prediction(*values))
    assert alias["third_moment_N1"] == ["4", "5"]
    assert alias["equal_first_and_second_moments"] is True and alias["equal_laws"] is False
    analysis = analyses[0]
    for label, case_index, masks in (
        ("singleton_self_overlap", 0, [1]),
        ("ordered_pair_and_mixture", 0, [5]),
        ("star_path", 0, [57, 27]),
        ("shared_root", 0, [41]),
        ("degree_six", 6, [21, 42]),
        ("fixed_eligible", 9, [0, 16]),
    ):
        selected = [
            next(
                h
                for h in analysis["histories"]
                if (h["case_index"], h["stage1_mask"], h["final_mask"]) == (case_index, s, 0)
            )
            for s in masks
        ]
        assert controls[label]["history_ids"] == [h["history_id"] for h in selected]
        assert all(F(h["joint_probability"]) > 0 for h in selected)
    pair = controls["ordered_pair_and_mixture"]
    assert pair["iid_half_variance"] == "1/2" and pair["block_variance"] == "1"
    assert pair["mean_corner_covariance"] == "0"
    assert (
        pair["omitting_one_cross_orientation_raw_at_x1"] == "3" and pair["correct_raw_at_x1"] == "4"
    )
    shared = controls["shared_root"]
    assert shared["edge_point"] == ["0", "1/2"]
    assert shared["edge_variance_N1"] == "1/2" and shared["edge_variance_N2"] == "0"
    assert shared["raw_N2_second"] == analysis["cases"][0]["states"][41]["pair_graded"][2][2]
    assert (
        shared["variance_N2"] == analysis["cases"][0]["states"][41]["covariance_polynomials"][2][2]
    )
    assert controls["degree_six"]["odd_covariance_N3"][6][0] == -1
    assert controls["degree_six"]["even_covariance_N3"][0][6] == -1
    audit = suite["audit"]
    assert wire(audit) == wire(
        {
            "distinct_points_per_state": 22,
            "state_point_checks": 608 * 22,
            "raw_coefficient_cells_checked": 608 * 256,
            "covariance_convolution_cells_checked": 608 * 784,
            "covariance_matrices_psd_checked": 608 * 23,
            "principal_minors_checked": 608 * 23 * 7,
            "deterministic_corner_checks": 608 * 4,
        }
    )


def test_retained_i_bridge_four_pairs_eight_directions(aggregate, pinned_i, partitions):
    _, suite = aggregate
    bridge = suite["prior_bridge"]
    _, _, _, ids = partitions
    supported = [i for i, h in enumerate(pinned_i["histories"]) if F(h["joint_probability"]) > 0]
    expected = {}
    for target in TARGETS:
        expected[target] = {}
        for prior in ("analytic_means", "analytic_counts"):
            left = [row[target] for row in ids]
            right = [h["target_classes"][prior] for h in pinned_i["histories"]]
            directions = []
            for source, destination in ((left, right), (right, left)):
                refines, collision, common = fiber_check(source, destination, supported)
                directions.append(
                    {
                        "refines": refines,
                        "first_collision": collision,
                        "common_refinement_classes": common,
                    }
                )
            expected[target][prior] = {
                "current_refines_prior": directions[0],
                "prior_refines_current": directions[1],
                "same_partition": directions[0]["refines"] and directions[1]["refines"],
            }
    assert wire(bridge["target_comparisons"]) == wire(expected)
    assert bridge["I_states_matched"] == 608 and bridge["I_histories_matched"] == 6804
    assert bridge["I_candidate_partitions_matched"] == 12
    assert bridge["I_raw_moment_coefficient_cells_matched"] == 608 * 256
    assert bridge["prior_executors_imported"] is False
    assert bridge["I_full_laws_retained_in_primary_output"] is False
    assert bridge["prior_transports_recomputed"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "pair_type",
        "pair_negative",
        "pair_value",
        "pair_padding",
        "cov_type",
        "cov_value",
        "cov_padding",
        "mean",
        "color_sizes",
    ),
)
def test_runner_rejects_early_raw_covariance_and_mean_mutations(aggregate, analyses, kind):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["cases"] = list(changed["cases"])
    changed["cases"][0] = dict(changed["cases"][0])
    changed["cases"][0]["states"] = list(changed["cases"][0]["states"])
    first = json.loads(wire(changed["cases"][0]["states"][0]))
    changed["cases"][0]["states"][0] = first
    if kind == "pair_type":
        first["pair_graded"][0][0][0][0] = True
    elif kind == "pair_negative":
        first["pair_graded"][0][0][0][0] = -1
    elif kind == "pair_value":
        first["pair_graded"][0][0][0][0] = 2
    elif kind == "pair_padding":
        first["pair_graded"][0][0].pop()
    elif kind == "cov_type":
        first["covariance_polynomials"][0][0][0][0] = False
    elif kind == "cov_value":
        first["covariance_polynomials"][0][0][0][0] = 1
    elif kind == "cov_padding":
        first["covariance_polynomials"][0][0].pop()
    elif kind == "mean":
        first["mean_polynomials"][0][0][0] = 2
    else:
        first["color_sizes"][0] = True
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


def test_prior_bridge_rejects_changed_old_candidate_before_full_recompute(aggregate, analyses):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["candidate_partitions"] = dict(changed["candidate_partitions"])
    changed["candidate_partitions"]["final_only"] = []
    with pytest.raises(ValueError):
        runner.prior_bridge(changed)


@pytest.mark.parametrize(
    "kind", ("two_minor", "three_minor", "negative_diag", "asymmetric", "nonconstant_zero", "shape")
)
def test_exact_psd_guard_rejects_invalid_covariance_without_regularization(aggregate, kind):
    runner, _ = aggregate
    matrix = [[F(0)] * 4 for _ in range(4)]
    for q in (1, 2, 3):
        matrix[q][q] = F(1)
    if kind == "two_minor":
        matrix[1][2] = matrix[2][1] = F(2)
    elif kind == "three_minor":
        matrix[1][2] = matrix[2][1] = matrix[1][3] = matrix[3][1] = F(1)
        assert all(
            determinant([[matrix[q][r] for r in ids] for q in ids]) >= 0
            for ids in combinations((1, 2, 3), 2)
        )
        assert determinant([[matrix[q][r] for r in (1, 2, 3)] for q in (1, 2, 3)]) == -1
    elif kind == "negative_diag":
        matrix[1][1] = F(-1)
    elif kind == "asymmetric":
        matrix[1][2] = F(1)
    elif kind == "nonconstant_zero":
        matrix[0][0] = F(1)
    else:
        matrix.pop()
    with pytest.raises(ValueError):
        runner.check_covariance(matrix)


def test_exact_psd_guard_accepts_zero_and_singular_covariances(aggregate):
    runner, _ = aggregate
    zero = [[F(0)] * 4 for _ in range(4)]
    assert tuple(runner.check_covariance(zero)) == (F(0),) * 7
    rank_one = [[F(0)] * 4 for _ in range(4)]
    for q in (1, 2):
        for r in (1, 2):
            rank_one[q][r] = F(1)
    expected = []
    for mask in range(1, 8):
        ids = [q + 1 for q in range(3) if mask & (1 << q)]
        expected.append(determinant([[rank_one[q][r] for r in ids] for q in ids]))
    assert tuple(runner.check_covariance(rank_one)) == tuple(expected)
    assert tuple(runner.principal_minors(tuple(tuple(row) for row in rank_one))) == tuple(expected)
    assert determinant(rank_one) == 0


def invalid_inputs():
    class Text(str):
        pass

    class Mapping(dict):
        pass

    class Sequence(list):
        pass

    base = problem()
    return [
        None,
        [],
        True,
        False,
        {},
        {"schema_version": base["schema_version"]},
        {"family": base["family"]},
        {**base, "extra": 1},
        {**base, "profile": "ferrers6"},
        Mapping(base),
        Sequence(),
        {**base, "schema_version": Text(base["schema_version"])},
        {**base, "family": Text(base["family"])},
        {Text("schema_version"): base["schema_version"], "family": base["family"]},
        {"schema_version": base["schema_version"], Text("family"): base["family"]},
        *({**base, "schema_version": v} for v in (None, True, False, 1, [], "wrong")),
        *(
            {**base, "family": v}
            for v in (None, True, False, 1, [], {}, "unknown", "qr05h_two_color")
        ),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_input_rejects_wrong_types_values_and_subclasses(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_outputs_and_assertion_free_schema_guards(tmp_path):
    script = r"""
import hashlib, importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05j-problem-v1", "family":"qr05i_chain_pairs"}
class Text(str):
    pass
class Mapping(dict):
    pass
class Sequence(list):
    pass
invalid = (
    True, {**valid,"extra":1}, {**valid,"family":False}, {**valid,"family":"unknown"},
    {**valid,"schema_version":1}, Mapping(valid), Sequence(),
    {**valid,"schema_version":Text(valid["schema_version"])}, {**valid,"family":Text(valid["family"])},
    {Text("schema_version"):valid["schema_version"], "family":valid["family"]},
    {"schema_version":valid["schema_version"], Text("family"):valid["family"]},
)
def native(value):
    if value is None or type(value) in (bool,int,str):
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            native(item)
        return
    raise RuntimeError("non-native exact output")
digests = []
for number, filename in enumerate(("uncertainty.py", "reference_qr05j.py")):
    name = "_qr05j_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    native(result)
    if result["counts"]["states"] != 608 or result["counts"]["positive_histories"] != 3534:
        raise RuntimeError("optimized universe differs")
    digests.append(hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",", ":"),allow_nan=False).encode()).hexdigest())
    del result
    for bad in invalid:
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized malformed input accepted")
if digests[0] != digests[1]:
    raise RuntimeError("optimized exact outputs differ")
print(json.dumps({"valid_routes":2,"explicit_rejections":2*len(invalid)}))
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-X",
            f"pycache_prefix={tmp_path / 'bytecode'}",
            "-c",
            script,
            str(HERE),
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 22}
