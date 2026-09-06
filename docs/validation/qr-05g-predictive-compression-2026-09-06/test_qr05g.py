"""Independent finite predictive-compression tests with no prior executors.

Repeat laws are evaluated once per intermediate mask; histories reference them
without expanding (S,T,U).  Public keys never contain a hidden source label.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, permutations
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
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
)
TARGETS = ("current_estimate", "future_means", "future_counts", "future_records")


def problem():
    return {"schema_version": "det8-qr05g-problem-v1", "family": "qr05f_ten"}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("research module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05g_test_direct", "compression.py"),
        private_module("_qr05g_test_reference", "reference_qr05g.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def aggregate_suite():
    return private_module("_qr05g_test_aggregate", "study.py").run_suite()


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
    raise AssertionError(f"non-native exact wire type {type(value)}")


def wire(value):
    native(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fs(values):
    assert all(type(value) is str and str(F(value)) == value for value in values)
    return list(map(F, values))


def matrix(values):
    return [fs(row) for row in values]


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
    eligible = [i for i in range(8) if i not in fixed]
    return past, fixed, eligible


def rate(design, mask):
    if design == "parity_adaptive":
        return F(1 if mask.bit_count() % 2 == 0 else 2, 3)
    if design == "parity_hole":
        return F(int(mask.bit_count() % 2 == 0))
    return F(1, 2)


def kernel(design, first, final):
    if final & first != final:
        return F(0)
    if design == "common_coin":
        return F(1) if first == 0 else F(1, 2) if final in (0, first) else F(0)
    r = rate(design, first)
    return r ** final.bit_count() * (1 - r) ** (first.bit_count() - final.bit_count())


def conditional_inclusion(design, first, support):
    if first & support != support:
        return F(0)
    if support == 0:
        return F(1)
    return F(1, 2) if design == "common_coin" else rate(design, first) ** support.bit_count()


@cache
def first_law(case_index):
    profile, design = CASES[case_index]
    m = len(population(profile)[2])
    p = (
        [F(1, comb(m, 2)) if s.bit_count() == 2 else F(0) for s in range(1 << m)]
        if design == "first_pair"
        else [F(1, 1 << m)] * (1 << m)
    )
    inclusion = [sum((v for s, v in enumerate(p) if s & a == a), start=F(0)) for a in range(1 << m)]
    return p, inclusion


@cache
def observed(profile, mask):
    source, fixed, eligible = population(profile)
    kept = sorted(fixed + [v for i, v in enumerate(eligible) if mask & (1 << i)])
    past = [[i for i, v in enumerate(kept) if v in source[target]] for target in kept]
    local = {v: i for i, v in enumerate(kept)}
    families = []
    graded = [[0] * 4 for _ in range(4)]
    for q in range(4):
        chains = []
        for vertices in combinations([v for v in kept if 0 < v < 7], q):
            if all(local[a] in past[local[b]] for a, b in pairwise([0, *vertices, 7])):
                support = sum(1 << i for i, v in enumerate(eligible) if v in vertices)
                chains.append((vertices, support))
                graded[q][support.bit_count()] += 1
        families.append(chains)
    return kept, past, families, graded


@cache
def canonical_order(profile, mask, marked):
    kept, past, _, _ = observed(profile, mask)
    anchors = population(profile)[1] if marked else [0, 7]
    others = [v for v in kept if v not in anchors]
    original_position = {v: i for i, v in enumerate(kept)}
    n = len(kept)
    codes = []
    for perm in permutations(others):
        arranged = anchors + list(perm)
        codes.append(
            sum(
                1 << (i * n + j)
                for i, a in enumerate(arranged)
                for j, b in enumerate(arranged)
                if original_position[a] in past[original_position[b]]
            )
        )
    return [n, min(codes)]


def moments(probabilities, counts):
    assert sum(probabilities) == 1
    mean = [sum(p * row[i] for p, row in zip(probabilities, counts)) for i in range(4)]
    covariance = [
        [
            sum(
                p * (row[i] - mean[i]) * (row[j] - mean[j]) for p, row in zip(probabilities, counts)
            )
            for j in range(4)
        ]
        for i in range(4)
    ]
    return mean, covariance


def psd(covariance):
    work = [row[:] for row in covariance]
    assert len(work) == 4 and all(len(row) == 4 for row in work)
    assert all(work[i][j] == work[j][i] for i in range(4) for j in range(4))
    for k in range(4):
        pivot = work[k][k]
        assert pivot >= 0
        if pivot == 0:
            assert all(work[k][j] == work[j][k] == 0 for j in range(k + 1, 4))
        else:
            for i in range(k + 1, 4):
                for j in range(k + 1, 4):
                    work[i][j] -= work[i][k] * work[k][j] / pivot


def test_complete_universe_is_native_and_identical(analyses):
    first, second = analyses
    assert wire(first) == wire(second)
    assert wire(json.loads(wire(first))) == wire(first)
    assert set(first) == {
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
def test_observed_states_grading_and_anchored_order_canonicalization(analyses, case_index):
    for analysis in analyses:
        case = analysis["cases"][case_index]
        profile, design = CASES[case_index]
        source, fixed, eligible = population(profile)
        p1, inclusion = first_law(case_index)
        assert case["case_index"] == case_index and type(case["case_index"]) is int
        assert case["profile"] == profile and case["design"] == design and case["density"] == "12"
        for name, expected in (("past", source), ("fixed", fixed), ("eligible", eligible)):
            assert wire(case[name]) == wire(expected)
        assert fs(case["stage1_inclusions"]) == inclusion
        assert [row["mask"] for row in case["states"]] == list(range(len(p1)))
        for state in case["states"]:
            s = state["mask"]
            assert type(s) is int and F(state["probability"]) == p1[s]
            kept, past, families, graded = observed(profile, s)
            for name, expected in (
                ("kept", kept),
                ("past", past),
                ("graded_counts", graded),
                ("chain_counts", [len(f) for f in families]),
            ):
                assert wire(state[name]) == wire(expected)
            assert state["policy_token"] == str(rate(design, s))
            assert state["tagged_present"] is bool(s & 1)
            assert wire(state["unmarked_order"]) == wire(canonical_order(profile, s, False))
            assert wire(state["marked_order"]) == wire(canonical_order(profile, s, True))


@pytest.mark.parametrize("case_index", range(10))
def test_repeat_order_law_pushforward_moments_and_covariance(analyses, case_index):
    profile, design = CASES[case_index]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            expected_masks = [u for u in range(s + 1) if s & u == u]
            assert [row["mask"] for row in state["repeat_rows"]] == expected_masks
            probabilities, count_vectors, pmf = [], [], {}
            for row, u in zip(state["repeat_rows"], expected_masks):
                kept, past, family, _ = observed(profile, u)
                counts = [len(f) for f in family]
                p = kernel(design, s, u)
                assert wire(row) == wire(
                    {
                        "mask": u,
                        "probability": str(p),
                        "kept": kept,
                        "past": past,
                        "chain_counts": counts,
                    }
                )
                probabilities.append(p)
                count_vectors.append(counts)
                if p:
                    atom = tuple(counts)
                    pmf[atom] = pmf.get(atom, F(0)) + p
            expected_law = [
                {"counts": list(k), "probability": str(p)} for k, p in sorted(pmf.items())
            ]
            assert wire(state["count_law"]) == wire(expected_law)
            mean, covariance = moments(probabilities, count_vectors)
            assert fs(state["count_mean"]) == mean
            assert matrix(state["count_covariance"]) == covariance
            scales = [F((-1) ** q, 2 ** (q + 1) * 12**q) for q in range(4)]
            assert fs(state["coefficient_mean"]) == [a * b for a, b in zip(mean, scales)]
            transformed = [
                [covariance[i][j] * scales[i] * scales[j] for j in range(4)] for i in range(4)
            ]
            assert matrix(state["coefficient_covariance"]) == transformed
            psd(covariance)
            psd(transformed)
            # Mean identity from support grading is distinct from equality of PMFs.
            graded_mean = []
            for row in state["graded_counts"]:
                graded_mean.append(
                    sum(
                        F(number)
                        * (
                            1
                            if k == 0
                            else F(1, 2)
                            if design == "common_coin"
                            else rate(design, s) ** k
                        )
                        for k, number in enumerate(row)
                    )
                )
            assert graded_mean == mean


def test_histories_current_estimates_and_all_prespecified_counts(analyses):
    for analysis in analyses:
        expected = []
        positive = states = positive_states = repeat_rows = positive_repeat = 0
        for index, case in enumerate(analysis["cases"]):
            profile, design = CASES[index]
            p1, inclusion = first_law(index)
            states += len(case["states"])
            positive_states += sum(p > 0 for p in p1)
            for state in case["states"]:
                s = state["mask"]
                for repeated in state["repeat_rows"]:
                    repeat_rows += 1
                    positive_repeat += F(repeated["probability"]) > 0
                    t = repeated["mask"]
                    p = kernel(design, s, t)
                    _, _, families, _ = observed(profile, t)
                    values, omitted = [], []
                    for family in families:
                        value, missing = F(0), 0
                        for _, support in family:
                            pi2 = conditional_inclusion(design, s, support)
                            if inclusion[support] > 0 and pi2 > 0:
                                value += 1 / (inclusion[support] * pi2)
                            else:
                                missing += 1
                        values.append(str(value))
                        omitted.append(missing)
                    expected.append((index, s, t, p, p1[s] * p, values, omitted))
        assert len(expected) == len(analysis["histories"]) == 6804
        for number, (history, row) in enumerate(zip(analysis["histories"], expected)):
            index, s, t, conditional, joint, values, omitted = row
            assert type(history["history_id"]) is int and history["history_id"] == number
            assert wire(
                [history["case_index"], history["stage1_mask"], history["final_mask"]]
            ) == wire([index, s, t])
            assert fs([history["conditional_probability"], history["joint_probability"]]) == [
                conditional,
                joint,
            ]
            assert wire(history["current_estimate"]) == wire(values)
            assert wire(history["omitted_terms"]) == wire(omitted)
            assert set(history["candidate_classes"]) == set(CANDIDATES)
            assert set(history["target_classes"]) == set(TARGETS)
            if joint > 0:
                positive += 1
                assert all(type(v) is int for v in history["candidate_classes"].values())
                assert all(type(v) is int for v in history["target_classes"].values())
            else:
                assert all(v is None for v in history["candidate_classes"].values())
                assert all(v is None for v in history["target_classes"].values())
        assert wire(analysis["counts"]) == wire(
            {
                "cases": 10,
                "states": states,
                "positive_states": positive_states,
                "repeat_rows": repeat_rows,
                "positive_repeat_rows": positive_repeat,
                "histories": 6804,
                "positive_histories": positive,
                "zero_histories": 6804 - positive,
                "candidates": 9,
                "targets": 4,
                "current_estimator_cells": 27216,
            }
        )
        assert states == 608 and positive_states == 510
        assert repeat_rows == 6804 and positive_repeat == 4872
        assert positive == 3534


@pytest.fixture(scope="session")
def reconstructed_partitions(analyses):
    analysis = analyses[0]
    candidate_groups = {name: [] for name in CANDIDATES}
    target_groups = {name: [] for name in TARGETS}
    candidate_lookup = {name: {} for name in CANDIDATES}
    target_lookup = {name: {} for name in TARGETS}
    candidate_ids, target_ids = [], []
    record_laws = {}
    for case in analysis["cases"]:
        for state in case["states"]:
            record_laws[case["case_index"], state["mask"]] = [
                {"kept": row["kept"], "past": row["past"], "probability": row["probability"]}
                for row in state["repeat_rows"]
                if F(row["probability"]) > 0
            ]
    for history in analysis["histories"]:
        if F(history["joint_probability"]) == 0:
            candidate_ids.append({name: None for name in CANDIDATES})
            target_ids.append({name: None for name in TARGETS})
            continue
        case = analysis["cases"][history["case_index"]]
        state = case["states"][history["stage1_mask"]]
        final = observed(case["profile"], history["final_mask"])
        context = [case["design"], case["density"], case["fixed"], case["eligible"]]
        base = [context, final[0], final[1]]
        token, tag = state["policy_token"], state["tagged_present"]
        appended = {
            "final_only": [],
            "policy_token": [token],
            "tagged_policy": [token, tag],
            "counts_policy": [token, state["chain_counts"]],
            "graded_policy": [token, state["graded_counts"]],
            "tagged_graded": [token, state["graded_counts"], tag],
            "unmarked_order": [token, state["unmarked_order"]],
            "marked_order": [token, state["marked_order"]],
            "full_record": [state["kept"], state["past"]],
        }
        signatures = {
            "current_estimate": history["current_estimate"],
            "future_means": state["count_mean"],
            "future_counts": state["count_law"],
            "future_records": record_laws[case["case_index"], state["mask"]],
        }
        cids, tids = {}, {}
        for name in CANDIDATES:
            key = [*base, *appended[name]]
            encoded = wire(key)
            if encoded not in candidate_lookup[name]:
                index = len(candidate_groups[name])
                candidate_lookup[name][encoded] = index
                candidate_groups[name].append(
                    {"class_id": index, "members": [], "joint_mass": F(0), "key": key}
                )
            index = candidate_lookup[name][encoded]
            group = candidate_groups[name][index]
            group["members"].append(history["history_id"])
            group["joint_mass"] += F(history["joint_probability"])
            cids[name] = index
        for name in TARGETS:
            signature = signatures[name]
            encoded = wire([base, signature])
            if encoded not in target_lookup[name]:
                index = len(target_groups[name])
                target_lookup[name][encoded] = index
                target_groups[name].append(
                    {
                        "class_id": index,
                        "members": [],
                        "joint_mass": F(0),
                        "base": base,
                        "signature": signature,
                    }
                )
            index = target_lookup[name][encoded]
            group = target_groups[name][index]
            group["members"].append(history["history_id"])
            group["joint_mass"] += F(history["joint_probability"])
            tids[name] = index
        candidate_ids.append(cids)
        target_ids.append(tids)
    for collection in (candidate_groups, target_groups):
        for groups in collection.values():
            for group in groups:
                group["joint_mass"] = str(group["joint_mass"])
    return candidate_groups, target_groups, candidate_ids, target_ids


def test_all_partitions_are_reconstructed_without_hidden_source_names(
    analyses, reconstructed_partitions
):
    candidates, targets, cids, tids = reconstructed_partitions
    for analysis in analyses:
        assert wire(analysis["candidate_partitions"]) == wire(candidates)
        assert wire(analysis["target_partitions"]) == wire(targets)
        for h, c, t in zip(analysis["histories"], cids, tids):
            assert wire(h["candidate_classes"]) == wire(c)
            assert wire(h["target_classes"]) == wire(t)
        positive_ids = [
            h["history_id"] for h in analysis["histories"] if F(h["joint_probability"]) > 0
        ]
        for collection in (analysis["candidate_partitions"], analysis["target_partitions"]):
            for groups in collection.values():
                assert sorted(i for group in groups for i in group["members"]) == positive_ids
                assert sum(F(group["joint_mass"]) for group in groups) == 10
                assert all(group["members"] == sorted(set(group["members"])) for group in groups)


def refines(left, right, supported):
    images = {}
    for i in supported:
        images.setdefault(left[i], set()).add(right[i])
    return all(len(targets) == 1 for targets in images.values())


def test_refinement_matrices_minimality_and_first_collisions(analyses, reconstructed_partitions):
    candidates, _, cids, tids = reconstructed_partitions
    supported = [i for i, row in enumerate(cids) if row["final_only"] is not None]
    for analysis in analyses:
        cmatrix = [
            [refines([x[a] for x in cids], [x[b] for x in cids], supported) for b in CANDIDATES]
            for a in CANDIDATES
        ]
        tmatrix = [
            [refines([x[a] for x in tids], [x[b] for x in tids], supported) for b in TARGETS]
            for a in TARGETS
        ]
        assert wire(analysis["candidate_refinement"]) == wire(cmatrix)
        assert wire(analysis["target_refinement"]) == wire(tmatrix)
        assert tmatrix[3][2] and tmatrix[2][1]
        assert not tmatrix[2][3] and not tmatrix[1][2]
        for c in CANDIDATES:
            for target in TARGETS:
                first, collision = {}, None
                for i in supported:
                    key = cids[i][c]
                    if key not in first:
                        first[key] = i
                    elif tids[first[key]][target] != tids[i][target]:
                        collision = {"left_history": first[key], "right_history": i}
                        break
                common = len({(cids[i][c], tids[i][target]) for i in supported})
                expected = {
                    "sufficient": collision is None,
                    "first_collision": collision,
                    "common_refinement_classes": common,
                }
                assert wire(analysis["assessments"][c][target]) == wire(expected)
                assert (common == len(candidates[c])) is (collision is None)
                assert refines([x[c] for x in cids], [x[target] for x in tids], supported) is (
                    collision is None
                )
        assert all(analysis["assessments"]["full_record"][t]["sufficient"] for t in TARGETS)
        assert analysis["assessments"]["graded_policy"]["future_means"]["sufficient"] is True
        assert analysis["assessments"]["marked_order"]["future_counts"]["sufficient"] is True


def history(analysis, case_index, first, final=0):
    return next(
        h
        for h in analysis["histories"]
        if (h["case_index"], h["stage1_mask"], h["final_mask"]) == (case_index, first, final)
    )


def atom_probability(state, counts):
    return sum(
        (F(a["probability"]) for a in state["count_law"] if a["counts"] == counts), start=F(0)
    )


@pytest.mark.parametrize(
    "case_index,variances,atom,mass",
    (
        (0, (F(15, 16), F(13, 16)), F(1, 16), F(1, 1024)),
        (1, (F(4, 9), F(32, 81)), F(2, 81), F(1, 324)),
    ),
)
def test_equal_graded_counts_and_means_do_not_preserve_joint_future_law(
    analyses, case_index, variances, atom, mass
):
    for analysis in analyses:
        star, path = (analysis["cases"][case_index]["states"][s] for s in (57, 27))
        assert star["chain_counts"] == path["chain_counts"] == [1, 4, 3, 0]
        assert star["graded_counts"] == path["graded_counts"]
        assert star["count_mean"] == path["count_mean"]
        assert tuple(F(s["count_covariance"][2][2]) for s in (star, path)) == variances
        assert atom_probability(star, [1, 3, 0, 0]) == atom
        assert atom_probability(path, [1, 3, 0, 0]) == 0
        left, right = history(analysis, case_index, 57), history(analysis, case_index, 27)
        assert F(left["joint_probability"]) == F(right["joint_probability"]) == mass
        for c in ("counts_policy", "graded_policy", "tagged_graded"):
            assert left["candidate_classes"][c] == right["candidate_classes"][c]
        assert left["target_classes"]["future_means"] == right["target_classes"]["future_means"]
        assert left["target_classes"]["future_counts"] != right["target_classes"]["future_counts"]


def test_fixed_mark_cannot_be_forgotten_for_repeat_means(analyses):
    for analysis in analyses:
        left, right = (analysis["cases"][9]["states"][s] for s in (10, 20))
        assert left["chain_counts"] == right["chain_counts"] == [1, 3, 1, 0]
        assert left["unmarked_order"] == right["unmarked_order"]
        assert left["marked_order"] != right["marked_order"]
        assert left["graded_counts"] != right["graded_counts"]
        assert F(left["count_mean"][2]) == F(1, 4)
        assert F(right["count_mean"][2]) == F(1, 2)
        h, k = history(analysis, 9, 10), history(analysis, 9, 20)
        assert h["candidate_classes"]["unmarked_order"] == k["candidate_classes"]["unmarked_order"]
        assert h["target_classes"]["future_means"] != k["target_classes"]["future_means"]


def test_marked_isomorphism_is_sufficient_but_not_necessary_for_count_law(analyses):
    for analysis in analyses:
        up, down = (analysis["cases"][0]["states"][s] for s in (57, 39))
        assert up["marked_order"] != down["marked_order"]
        assert wire(up["count_law"]) == wire(down["count_law"])
        h, k = history(analysis, 0, 57), history(analysis, 0, 39)
        assert h["candidate_classes"]["marked_order"] != k["candidate_classes"]["marked_order"]
        assert h["target_classes"]["future_counts"] == k["target_classes"]["future_counts"]


def test_labeled_record_law_is_stronger_than_marked_order_count_law(analyses):
    for analysis in analyses:
        one, two = (analysis["cases"][0]["states"][s] for s in (9, 18))
        assert one["marked_order"] == two["marked_order"] and one["count_law"] == two["count_law"]
        assert sum(F(r["probability"]) for r in one["repeat_rows"] if 1 in r["kept"]) == F(1, 2)
        assert sum(F(r["probability"]) for r in two["repeat_rows"] if 1 in r["kept"]) == 0
        h, k = history(analysis, 0, 9), history(analysis, 0, 18)
        assert h["candidate_classes"]["marked_order"] == k["candidate_classes"]["marked_order"]
        assert h["target_classes"]["future_records"] != k["target_classes"]["future_records"]


def test_deterministic_hole_can_make_full_provenance_unnecessarily_detailed(analyses):
    for analysis in analyses:
        h, k = history(analysis, 3, 0), history(analysis, 3, 1)
        assert F(h["joint_probability"]) > 0 and F(k["joint_probability"]) > 0
        assert h["candidate_classes"]["full_record"] != k["candidate_classes"]["full_record"]
        assert h["candidate_classes"]["policy_token"] != k["candidate_classes"]["policy_token"]
        assert h["target_classes"]["future_records"] == k["target_classes"]["future_records"]


def test_common_coin_counts_sufficiency_remains_context_specific(analyses):
    for analysis in analyses:
        grouped = {}
        for h in analysis["histories"]:
            if h["case_index"] == 2 and F(h["joint_probability"]) > 0:
                grouped.setdefault(h["candidate_classes"]["counts_policy"], set()).add(
                    h["target_classes"]["future_counts"]
                )
        assert grouped and all(len(values) == 1 for values in grouped.values())
        assert analysis["assessments"]["counts_policy"]["future_counts"]["sufficient"] is False


def test_hidden_source_profiles_are_pooled_when_public_context_agrees(analyses):
    for analysis in analyses:
        ferrers, standard = (analysis["cases"][i]["states"][63] for i in (0, 5))
        assert ferrers["chain_counts"] == standard["chain_counts"] == [1, 6, 6, 0]
        assert ferrers["count_mean"] == standard["count_mean"]
        assert wire(ferrers["count_law"]) != wire(standard["count_law"])
        assert [[r["mask"], r["probability"]] for r in ferrers["repeat_rows"]] == [
            [r["mask"], r["probability"]] for r in standard["repeat_rows"]
        ]
        h, k = history(analysis, 0, 63), history(analysis, 5, 63)
        assert h["candidate_classes"]["final_only"] == k["candidate_classes"]["final_only"]
        assert h["candidate_classes"]["graded_policy"] == k["candidate_classes"]["graded_policy"]
        assert h["target_classes"]["future_means"] == k["target_classes"]["future_means"]
        assert h["target_classes"]["future_counts"] != k["target_classes"]["future_counts"]


def test_aggregate_suite_native_exact_round_trip(aggregate_suite):
    assert wire(json.loads(wire(aggregate_suite))) == wire(aggregate_suite)


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
        {"family": "qr05f_ten"},
        {**base, "profile": "ferrers6"},
        {**base, "extra": 1},
        Mapping(base),
        Sequence(),
        {**base, "schema_version": Text(base["schema_version"])},
        {**base, "family": Text(base["family"])},
        {Text("schema_version"): base["schema_version"], "family": base["family"]},
        {"schema_version": base["schema_version"], Text("family"): base["family"]},
        *({**base, "schema_version": v} for v in (None, True, False, 1, [], "wrong")),
        *({**base, "family": v} for v in (None, True, False, 1, [], {}, "unknown", "qr05f_nine")),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_integrated_fixed_schema(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_execution_and_explicit_rejections(tmp_path):
    script = r"""
import hashlib, importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05g-problem-v1", "family":"qr05f_ten"}
class Text(str):
    pass
class Mapping(dict):
    pass
class Sequence(list):
    pass
invalid = (
    True, {**valid,"extra":1}, {**valid,"family":False},
    {**valid,"family":"unknown"}, {**valid,"schema_version":1},
    Mapping(valid), Sequence(),
    {**valid,"schema_version":Text(valid["schema_version"])},
    {**valid,"family":Text(valid["family"])},
    {Text("schema_version"):valid["schema_version"], "family":valid["family"]},
    {"schema_version":valid["schema_version"], Text("family"):valid["family"]},
)
digests = []
for number, filename in enumerate(("compression.py", "reference_qr05g.py")):
    name = "_qr05g_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    if result["counts"]["histories"] != 6804 or result["counts"]["positive_histories"] != 3534:
        raise RuntimeError("valid optimized universe differs")
    digests.append(hashlib.sha256(json.dumps(result,sort_keys=True,allow_nan=False).encode()).hexdigest())
    del result
    for bad in invalid:
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized schema accepted invalid input")
if digests[0] != digests[1]:
    raise RuntimeError("optimized complete outputs differ")
print(json.dumps({"valid_routes":2,"explicit_rejections":2 * len(invalid)}))
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
