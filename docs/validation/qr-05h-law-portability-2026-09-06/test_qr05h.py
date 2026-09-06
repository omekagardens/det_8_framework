"""Independent exact menu-law and transport tests, without prior executors.

Observed chains, marked orders, predictions, and transports are cached per S.
No test constructs the unnecessary (S,T,U) product.
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
TARGETS = (
    "iid_half_means",
    "iid_half_counts",
    "iid_color_means",
    "iid_color_counts",
    "block_coin_means",
    "block_coin_counts",
    "menu_means",
    "menu_counts",
)
STATE_KEYS = {
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
    "color_graded",
    "block_order",
    "color_order",
    "observations",
    "predictions",
    "transports",
}


def problem():
    return {"schema_version": "det8-qr05h-problem-v1", "family": "qr05g_menu3"}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module name already occupied")
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
        private_module("_qr05h_test_direct", "portability.py"),
        private_module("_qr05h_test_reference", "reference_qr05h.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def aggregate_suite():
    return private_module("_qr05h_test_aggregate", "study.py").run_suite()


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
    graded = [[0] * 4 for _ in range(4)]
    colored = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    families = []
    for q in range(4):
        family = []
        for vertices in combinations([v for v in kept if 0 < v < 7], q):
            if all(local[a] in past[local[b]] for a, b in pairwise([0, *vertices, 7])):
                support = [v for v in vertices if v in eligible]
                odd = sum(v % 2 for v in support)
                even = len(support) - odd
                graded[q][len(support)] += 1
                colored[q][odd][even] += 1
                family.append(tuple(vertices))
        families.append(family)
    return (
        {
            "mask": mask,
            "kept": kept,
            "past": past,
            "chain_counts": [len(family) for family in families],
        },
        graded,
        colored,
    )


@cache
def canonical_orders(profile, mask):
    observation = observed(profile, mask)[0]
    kept, past = observation["kept"], observation["past"]
    fixed = population(profile)[1]
    local = {v: i for i, v in enumerate(kept)}
    n = len(kept)
    result = {}
    for kind, anchors in (("unmarked_order", [0, 7]), ("marked_order", fixed)):
        others = [v for v in kept if v not in anchors]
        codes, color_codes, block_codes = [], [], []
        for perm in permutations(others):
            arranged = anchors + list(perm)
            relation = sum(
                1 << (i * n + j)
                for i, a in enumerate(arranged)
                for j, b in enumerate(arranged)
                if local[a] in past[local[b]]
            )
            codes.append(relation)
            if kind == "marked_order":
                color = sum(1 << i for i, v in enumerate(arranged) if v not in fixed and v % 2)
                block = sum(
                    1 << (i * n + j)
                    for i, a in enumerate(arranged)
                    for j, b in enumerate(arranged)
                    if i < j and a not in fixed and b not in fixed and a % 2 == b % 2
                )
                color_codes.append((relation, color))
                block_codes.append((relation, block))
        result[kind] = [n, min(codes)]
        if kind == "marked_order":
            result["color_order"] = [n, *min(color_codes)]
            result["block_order"] = [n, *min(block_codes)]
    return result


def current_rate(design, s):
    if design == "parity_adaptive":
        return F(1 if s.bit_count() % 2 == 0 else 2, 3)
    if design == "parity_hole":
        return F(int(s.bit_count() % 2 == 0))
    return F(1, 2)


def current_kernel(design, s, t):
    if s & t != t:
        return F(0)
    if design == "common_coin":
        return F(1) if s == 0 else F(1, 2) if t in (0, s) else F(0)
    r = current_rate(design, s)
    return r ** t.bit_count() * (1 - r) ** (s.bit_count() - t.bit_count())


@cache
def first_law(case_index):
    profile, design = CASES[case_index]
    m = len(population(profile)[2])
    p1 = (
        [F(1, comb(m, 2)) if s.bit_count() == 2 else F(0) for s in range(1 << m)]
        if design == "first_pair"
        else [F(1, 1 << m)] * (1 << m)
    )
    inclusions = [
        sum((p for s, p in enumerate(p1) if s & a == a), start=F(0)) for a in range(1 << m)
    ]
    return p1, inclusions


@cache
def submasks(s):
    return [u for u in range(s + 1) if s & u == u]


@cache
def policy_law(profile, s, policy):
    eligible = population(profile)[2]
    blocks = [
        sum(1 << j for j, v in enumerate(eligible) if s & (1 << j) and v % 2 == parity)
        for parity in (0, 1)
    ]
    blocks = [block for block in blocks if block]
    probabilities = []
    for u in submasks(s):
        if policy == "block_coin":
            p = F(1, 2 ** len(blocks)) if all(u & b in (0, b) for b in blocks) else F(0)
        else:
            p = F(1)
            for j, v in enumerate(eligible):
                if s & (1 << j):
                    r = F(1, 2) if policy == "iid_half" else F(1 if v % 2 else 2, 3)
                    p *= r if u & (1 << j) else 1 - r
        probabilities.append(p)
    return probabilities


def pmf_wire(atoms):
    return [{"counts": list(z), "probability": str(p)} for z, p in sorted(atoms.items()) if p]


@cache
def prediction(profile, s, policy):
    probabilities = policy_law(profile, s, policy)
    assert sum(probabilities) == 1
    atoms = {}
    for u, p in zip(submasks(s), probabilities):
        z = tuple(observed(profile, u)[0]["chain_counts"])
        atoms[z] = atoms.get(z, F(0)) + p
    mean = [sum(p * z[q] for z, p in atoms.items()) for q in range(4)]
    return {
        "probabilities": list(map(str, probabilities)),
        "count_law": pmf_wire(atoms),
        "count_mean": list(map(str, mean)),
        "coefficient_mean": [str(F((-1) ** q, 2 ** (q + 1) * 12**q) * mean[q]) for q in range(4)],
    }


@cache
def transport(profile, s, source, target):
    masks = submasks(s)
    q, p = policy_law(profile, s, source), policy_law(profile, s, target)
    weights = [b / a if a else None for a, b in zip(q, p)]
    missing = [u for u, a, b in zip(masks, q, p) if b and not a]
    fine_missing = sum((b for a, b in zip(q, p) if not a), start=F(0))
    grouped = {}
    first, collision = {}, None
    for u, a, b, w in zip(masks, q, p, weights):
        z = tuple(observed(profile, u)[0]["chain_counts"])
        values = grouped.setdefault(z, [F(0), F(0), F(0)])
        values[0] += a
        values[1] += b
        values[2] += b if a else 0
        if a and collision is None:
            if z not in first:
                first[z] = (u, w)
            elif first[z][1] != w:
                collision = {"left_mask": first[z][0], "right_mask": u}
    coarse = []
    for z, (source_mass, target_mass, accessible) in sorted(grouped.items()):
        coarse.append(
            {
                "counts": list(z),
                "source_probability": str(source_mass),
                "target_probability": str(target_mass),
                "fine_supported_target_probability": str(accessible),
                "missing_fine_probability": str(target_mass - accessible),
                "weight": str(target_mass / source_mass) if source_mass else None,
                "conditional_fine_weight": str(accessible / source_mass) if source_mass else None,
                "weighted_probability": str(target_mass if source_mass else F(0)),
            }
        )
    coarse_missing = sum((b for a, b, _ in grouped.values() if not a), start=F(0))
    return {
        "source": source,
        "target": target,
        "fine_weights": [str(w) if w is not None else None for w in weights],
        "missing_masks": missing,
        "fine_missing_mass": str(fine_missing),
        "fine_supported": not bool(fine_missing),
        "weighted_count_law": pmf_wire({z: c for z, (_, _, c) in grouped.items()}),
        "coarse_rows": coarse,
        "coarse_missing_mass": str(coarse_missing),
        "coarse_supported": not bool(coarse_missing),
        "coarse_weighted_count_law": pmf_wire(
            {z: b if a else F(0) for z, (a, b, _) in grouped.items()}
        ),
        "fine_weight_count_measurable": collision is None,
        "first_weight_collision": collision,
    }


def test_complete_outputs_are_identical_native_exact_trees(analyses):
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
def test_source_states_observed_chains_color_grading_and_canonical_orders(analyses, case_index):
    profile, design = CASES[case_index]
    source, fixed, eligible = population(profile)
    p1, inclusions = first_law(case_index)
    for analysis in analyses:
        case = analysis["cases"][case_index]
        assert set(case) == {
            "case_index",
            "profile",
            "design",
            "density",
            "past",
            "fixed",
            "eligible",
            "stage1_inclusions",
            "states",
        }
        assert wire({k: v for k, v in case.items() if k != "states"}) == wire(
            {
                "case_index": case_index,
                "profile": profile,
                "design": design,
                "density": "12",
                "past": source,
                "fixed": fixed,
                "eligible": eligible,
                "stage1_inclusions": list(map(str, inclusions)),
            }
        )
        assert [state["mask"] for state in case["states"]] == list(range(len(p1)))
        for s, state in enumerate(case["states"]):
            assert set(state) == STATE_KEYS
            obs, graded, colored = observed(profile, s)
            expected = {
                **obs,
                "probability": str(p1[s]),
                "policy_token": str(current_rate(design, s)),
                "tagged_present": bool(s & 1),
                "graded_counts": graded,
                "color_graded": colored,
                **canonical_orders(profile, s),
            }
            assert wire({k: state[k] for k in expected}) == wire(expected)
            assert wire(state["observations"]) == wire(
                [observed(profile, u)[0] for u in submasks(s)]
            )
            assert sum(graded[0]) == 1
            for q in range(4):
                for k in range(4):
                    assert graded[q][k] == sum(
                        colored[q][o][e] for o in range(4) for e in range(4) if o + e == k
                    )
                assert all(colored[q][o][e] == 0 for o in range(4) for e in range(4) if o + e > q)


@pytest.mark.parametrize("case_index", range(10))
def test_policy_laws_pushforwards_all_means_and_block_law_from_color_grading(analyses, case_index):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            expected = {policy: prediction(profile, s, policy) for policy in POLICIES}
            assert wire(state["predictions"]) == wire(expected)
            colored = observed(profile, s)[2]
            for policy in POLICIES:
                means = []
                for q in range(4):
                    value = F(0)
                    for o in range(4):
                        for e in range(4):
                            inclusion = (
                                F(1, 2 ** (o + e))
                                if policy == "iid_half"
                                else F(1, 3) ** o * F(2, 3) ** e
                                if policy == "iid_color"
                                else F(1, 2 ** (int(o > 0) + int(e > 0)))
                            )
                            value += colored[q][o][e] * inclusion
                    means.append(str(value))
                assert means == state["predictions"][policy]["count_mean"]
            # Four coin assignments coalesce correctly even for absent parity blocks.
            coin_atoms = {}
            for odd_kept, even_kept in ((False, False), (True, False), (False, True), (True, True)):
                z = tuple(
                    sum(
                        colored[q][o][e]
                        for o in range(4)
                        for e in range(4)
                        if (o == 0 or odd_kept) and (e == 0 or even_kept)
                    )
                    for q in range(4)
                )
                coin_atoms[z] = coin_atoms.get(z, F(0)) + F(1, 4)
            assert wire(pmf_wire(coin_atoms)) == wire(
                state["predictions"]["block_coin"]["count_law"]
            )


@pytest.mark.parametrize("case_index", range(10))
def test_all_directed_transports_fine_coarse_residuals_and_first_weight_collisions(
    analyses, case_index
):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            assert wire(state["transports"]) == wire(
                [
                    transport(profile, s, source, target)
                    for source in POLICIES
                    for target in POLICIES
                ]
            )
            for item in state["transports"]:
                fine_missing, coarse_missing = (
                    F(item["fine_missing_mass"]),
                    F(item["coarse_missing_mass"]),
                )
                assert 0 <= coarse_missing <= fine_missing <= 1
                assert (
                    sum(F(row["probability"]) for row in item["weighted_count_law"])
                    == 1 - fine_missing
                )
                assert (
                    sum(F(row["probability"]) for row in item["coarse_weighted_count_law"])
                    == 1 - coarse_missing
                )
                residual = F(0)
                for row in item["coarse_rows"]:
                    q = F(row["source_probability"])
                    missing = F(row["missing_fine_probability"])
                    if q:
                        difference = F(row["weight"]) - F(row["conditional_fine_weight"])
                        assert difference == missing / q
                        residual += q * difference
                        if item["fine_supported"]:
                            assert difference == 0
                    else:
                        assert row["weight"] is row["conditional_fine_weight"] is None
                assert residual == fine_missing - coarse_missing
                if item["fine_supported"]:
                    assert item["coarse_supported"] is True
                if item["source"] == item["target"]:
                    assert fine_missing == coarse_missing == 0
                    assert item["fine_weight_count_measurable"] is True
                    assert all(w in (None, "1") for w in item["fine_weights"])


@cache
def expected_history_rows():
    rows = []
    for case_index, (profile, design) in enumerate(CASES):
        p1 = first_law(case_index)[0]
        for s in range(len(p1)):
            for t in submasks(s):
                conditional = current_kernel(design, s, t)
                rows.append(
                    {
                        "history_id": len(rows),
                        "case_index": case_index,
                        "stage1_mask": s,
                        "final_mask": t,
                        "conditional_probability": str(conditional),
                        "joint_probability": str(p1[s] * conditional),
                    }
                )
    return rows


def test_unchanged_current_history_laws_global_ids_and_all_inventory_counts(analyses):
    rows = expected_history_rows()
    totals = {"states": 0, "positive_states": 0, "observations": 0, "coarse_weight_cells": 0}
    for case_index, (profile, _) in enumerate(CASES):
        p1 = first_law(case_index)[0]
        totals["states"] += len(p1)
        totals["positive_states"] += sum(p > 0 for p in p1)
        for s in range(len(p1)):
            totals["observations"] += len(submasks(s))
            totals["coarse_weight_cells"] += 9 * len(
                {tuple(observed(profile, u)[0]["chain_counts"]) for u in submasks(s)}
            )
    totals.update(
        {
            "cases": 10,
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
    )
    assert (
        totals["states"] == 608
        and totals["positive_states"] == 510
        and totals["observations"] == 6804
    )
    for analysis in analyses:
        assert wire(analysis["counts"]) == wire(totals)
        assert len(rows) == len(analysis["histories"]) == 6804
        positive = 0
        for actual, expected in zip(analysis["histories"], rows):
            assert set(actual) == set(expected) | {"candidate_classes", "target_classes"}
            assert wire({k: actual[k] for k in expected}) == wire(expected)
            assert set(actual["candidate_classes"]) == set(CANDIDATES)
            assert set(actual["target_classes"]) == set(TARGETS)
            supported = F(expected["joint_probability"]) > 0
            positive += supported
            for field in ("candidate_classes", "target_classes"):
                assert all(
                    type(v) is int if supported else v is None for v in actual[field].values()
                )
        assert positive == 3534


@cache
def state_additions(profile, design, s):
    observation, graded, colored = observed(profile, s)
    orders = canonical_orders(profile, s)
    token, tag = str(current_rate(design, s)), bool(s & 1)
    return {
        "final_only": [],
        "policy_token": [token],
        "tagged_policy": [token, tag],
        "counts_policy": [token, observation["chain_counts"]],
        "graded_policy": [token, graded],
        "tagged_graded": [token, graded, tag],
        "unmarked_order": [token, orders["unmarked_order"]],
        "marked_order": [token, orders["marked_order"]],
        "full_record": [observation["kept"], observation["past"]],
        "color_graded": [token, colored],
        "block_order": [token, orders["block_order"]],
        "color_order": [token, orders["color_order"]],
    }


@cache
def target_signatures(profile, s):
    predictions = {policy: prediction(profile, s, policy) for policy in POLICIES}
    return {
        **{
            policy + "_" + kind: predictions[policy][field]
            for policy in POLICIES
            for kind, field in (("means", "count_mean"), ("counts", "count_law"))
        },
        "menu_means": [predictions[p]["count_mean"] for p in POLICIES],
        "menu_counts": [predictions[p]["count_law"] for p in POLICIES],
    }


@pytest.fixture(scope="session")
def partitions():
    candidates = {name: [] for name in CANDIDATES}
    targets = {name: [] for name in TARGETS}
    clookup, tlookup = {name: {} for name in CANDIDATES}, {name: {} for name in TARGETS}
    cids, tids = [], []
    for history in expected_history_rows():
        mass = F(history["joint_probability"])
        if not mass:
            cids.append({name: None for name in CANDIDATES})
            tids.append({name: None for name in TARGETS})
            continue
        profile, design = CASES[history["case_index"]]
        _, fixed, eligible = population(profile)
        s, t = history["stage1_mask"], history["final_mask"]
        final = observed(profile, t)[0]
        base = [[design, "12", fixed, eligible], final["kept"], final["past"]]
        additions, signatures = state_additions(profile, design, s), target_signatures(profile, s)
        c, d = {}, {}
        for name in CANDIDATES:
            key = [*base, *additions[name]]
            encoded = wire(key)
            if encoded not in clookup[name]:
                index = len(candidates[name])
                clookup[name][encoded] = index
                candidates[name].append(
                    {"class_id": index, "members": [], "joint_mass": F(0), "key": key}
                )
            index = clookup[name][encoded]
            candidates[name][index]["members"].append(history["history_id"])
            candidates[name][index]["joint_mass"] += mass
            c[name] = index
        for name in TARGETS:
            signature = signatures[name]
            encoded = wire([base, signature])
            if encoded not in tlookup[name]:
                index = len(targets[name])
                tlookup[name][encoded] = index
                targets[name].append(
                    {
                        "class_id": index,
                        "members": [],
                        "joint_mass": F(0),
                        "base": base,
                        "signature": signature,
                    }
                )
            index = tlookup[name][encoded]
            targets[name][index]["members"].append(history["history_id"])
            targets[name][index]["joint_mass"] += mass
            d[name] = index
        cids.append(c)
        tids.append(d)
    for collection in (candidates, targets):
        for classes in collection.values():
            for group in classes:
                group["joint_mass"] = str(group["joint_mass"])
    return candidates, targets, cids, tids


def test_all_pooled_partitions_first_appearance_members_and_mass(partitions, analyses):
    candidates, targets, cids, tids = partitions
    supported = [h["history_id"] for h in expected_history_rows() if F(h["joint_probability"]) > 0]
    for analysis in analyses:
        assert wire(analysis["candidate_partitions"]) == wire(candidates)
        assert wire(analysis["target_partitions"]) == wire(targets)
        for history, c, t in zip(analysis["histories"], cids, tids):
            assert wire(history["candidate_classes"]) == wire(c)
            assert wire(history["target_classes"]) == wire(t)
        for collection in (analysis["candidate_partitions"], analysis["target_partitions"]):
            for classes in collection.values():
                assert sum(F(c["joint_mass"]) for c in classes) == 10
                assert sorted(i for c in classes for i in c["members"]) == supported
                assert all(c["members"] == sorted(set(c["members"])) for c in classes)


def refines(left, right, supported):
    images = {}
    for i in supported:
        images.setdefault(left[i], set()).add(right[i])
    return all(len(values) == 1 for values in images.values())


def test_refinement_fiber_sufficiency_first_collisions_and_menu_intersections(partitions, analyses):
    candidates, _, cids, tids = partitions
    supported = [i for i, row in enumerate(cids) if row["final_only"] is not None]
    cmatrix = [
        [refines([x[a] for x in cids], [x[b] for x in cids], supported) for b in CANDIDATES]
        for a in CANDIDATES
    ]
    tmatrix = [
        [refines([x[a] for x in tids], [x[b] for x in tids], supported) for b in TARGETS]
        for a in TARGETS
    ]
    assessments = {}
    for candidate in CANDIDATES:
        assessments[candidate] = {}
        for target in TARGETS:
            first, collision = {}, None
            for i in supported:
                key = cids[i][candidate]
                if key not in first:
                    first[key] = i
                elif tids[first[key]][target] != tids[i][target]:
                    collision = {"left_history": first[key], "right_history": i}
                    break
            common = len({(cids[i][candidate], tids[i][target]) for i in supported})
            assessments[candidate][target] = {
                "sufficient": collision is None,
                "first_collision": collision,
                "common_refinement_classes": common,
            }
            assert (common == len(candidates[candidate])) is (collision is None)
            assert refines([x[candidate] for x in cids], [x[target] for x in tids], supported) is (
                collision is None
            )
    for kind in ("means", "counts"):
        tuples = [tuple(row[p + "_" + kind] for p in POLICIES) for row in tids]
        menu = [row["menu_" + kind] for row in tids]
        assert refines(tuples, menu, supported) and refines(menu, tuples, supported)
    for policy in POLICIES:
        assert tmatrix[TARGETS.index(policy + "_counts")][TARGETS.index(policy + "_means")]
    assert tmatrix[7][6] and not tmatrix[6][7]
    for analysis in analyses:
        assert wire(analysis["candidate_refinement"]) == wire(cmatrix)
        assert wire(analysis["target_refinement"]) == wire(tmatrix)
        assert wire(analysis["assessments"]) == wire(assessments)
        assert all(
            assessments[c][t]["sufficient"] for c in ("full_record", "color_order") for t in TARGETS
        )
        assert assessments["color_graded"]["menu_means"]["sufficient"] is True
        assert assessments["color_graded"]["menu_counts"]["sufficient"] is False
        assert assessments["color_graded"]["block_coin_counts"]["sufficient"] is True
        assert assessments["block_order"]["iid_half_counts"]["sufficient"] is True
        assert assessments["block_order"]["block_coin_counts"]["sufficient"] is True
        assert assessments["block_order"]["iid_color_means"]["sufficient"] is False


def history(analysis, s, case_index=0, t=0):
    return next(
        h
        for h in analysis["histories"]
        if (h["case_index"], h["stage1_mask"], h["final_mask"]) == (case_index, s, t)
    )


def get_transport(state, source, target):
    return next(
        row for row in state["transports"] if row["source"] == source and row["target"] == target
    )


def atom(state, policy, counts):
    return sum(
        (
            F(row["probability"])
            for row in state["predictions"][policy]["count_law"]
            if row["counts"] == counts
        ),
        start=F(0),
    )


def variance(state, policy, component):
    law = state["predictions"][policy]["count_law"]
    mean = sum(F(row["probability"]) * row["counts"][component] for row in law)
    return sum(F(row["probability"]) * (row["counts"][component] - mean) ** 2 for row in law)


def test_singleton_color_and_block_correlation_portability_controls(analyses):
    for analysis in analyses:
        states = analysis["cases"][0]["states"]
        odd, even = states[1], states[2]
        assert (
            odd["marked_order"] == even["marked_order"]
            and odd["block_order"] == even["block_order"]
        )
        assert odd["color_order"] != even["color_order"]
        assert [F(s["predictions"]["iid_color"]["count_mean"][1]) for s in (odd, even)] == [
            F(1, 3),
            F(2, 3),
        ]
        same_color, two_colors = states[5], states[3]
        assert same_color["marked_order"] == two_colors["marked_order"]
        assert (
            same_color["predictions"]["iid_half"]["count_law"]
            == two_colors["predictions"]["iid_half"]["count_law"]
        )
        assert atom(same_color, "block_coin", [1, 1, 0, 0]) == 0
        assert atom(two_colors, "block_coin", [1, 1, 0, 0]) == F(1, 2)
        for state in (same_color, two_colors):
            probabilities = map(F, state["predictions"]["block_coin"]["probabilities"])
            rows = list(zip(state["observations"], probabilities))
            for v in state["kept"][1:-1]:
                assert sum(p for row, p in rows if v in row["kept"]) == F(1, 2)
        for s in (1, 2, 3, 5):
            assert F(history(analysis, s)["joint_probability"]) > 0


def test_star_path_color_grading_preserves_menu_means_not_iid_laws(analyses):
    for analysis in analyses:
        star, path = (analysis["cases"][0]["states"][s] for s in (57, 27))
        assert star["color_graded"] == path["color_graded"]
        for policy in POLICIES:
            assert (
                star["predictions"][policy]["count_mean"]
                == path["predictions"][policy]["count_mean"]
            )
        assert [variance(s, "iid_half", 2) for s in (star, path)] == [F(15, 16), F(13, 16)]
        assert [variance(s, "iid_color", 2) for s in (star, path)] == [F(68, 81), F(52, 81)]
        assert list(map(F, star["predictions"]["iid_color"]["count_mean"])) == [
            F(1),
            F(2),
            F(5, 9),
            F(0),
        ]
        assert (
            star["predictions"]["block_coin"]["count_law"]
            == path["predictions"]["block_coin"]["count_law"]
        )
        h, k = history(analysis, 57), history(analysis, 27)
        assert h["candidate_classes"]["color_graded"] == k["candidate_classes"]["color_graded"]
        assert h["target_classes"]["menu_means"] == k["target_classes"]["menu_means"]
        assert h["target_classes"]["menu_counts"] != k["target_classes"]["menu_counts"]


def test_full_support_does_not_make_fine_weights_count_measurable(analyses):
    for analysis in analyses:
        tr = get_transport(analysis["cases"][0]["states"][3], "iid_half", "iid_color")
        assert tr["fine_supported"] is tr["coarse_supported"] is True
        assert tr["fine_weight_count_measurable"] is False
        assert tr["first_weight_collision"] == {"left_mask": 1, "right_mask": 2}
        assert [F(tr["fine_weights"][i]) for i in (1, 2)] == [F(4, 9), F(16, 9)]
        singleton = next(row for row in tr["coarse_rows"] if row["counts"] == [1, 1, 0, 0])
        assert F(singleton["weight"]) == F(singleton["conditional_fine_weight"]) == F(10, 9)


def test_support_loss_retains_unrenormalized_half_mass(analyses):
    for analysis in analyses:
        state = analysis["cases"][0]["states"][5]
        forward = get_transport(state, "iid_half", "block_coin")
        assert forward["fine_weights"] == ["2", "0", "0", "2"]
        assert forward["fine_supported"] is True
        reverse = get_transport(state, "block_coin", "iid_half")
        assert reverse["missing_masks"] == [1, 4]
        assert reverse["fine_missing_mass"] == reverse["coarse_missing_mass"] == "1/2"
        assert reverse["fine_supported"] is reverse["coarse_supported"] is False
        assert sum(F(row["probability"]) for row in reverse["weighted_count_law"]) == F(1, 2)
        assert sum(F(row["probability"]) for row in reverse["coarse_weighted_count_law"]) == F(1, 2)


def test_coarse_transport_can_work_without_fine_support_or_conditional_identity(analyses):
    for analysis in analyses:
        state = analysis["cases"][0]["states"][7]
        probabilities = list(map(F, state["predictions"]["block_coin"]["probabilities"]))
        assert [row["mask"] for row, p in zip(state["observations"], probabilities) if p] == [
            0,
            2,
            5,
            7,
        ]
        assert {p for p in probabilities if p} == {F(1, 4)}
        tr = get_transport(state, "block_coin", "iid_half")
        assert tr["missing_masks"] == [1, 3, 4, 6] and tr["fine_missing_mass"] == "1/2"
        assert tr["fine_supported"] is False and tr["coarse_supported"] is True
        assert tr["fine_weight_count_measurable"] is True
        assert [row["weight"] for row in tr["coarse_rows"]] == ["1/2", "3/2", "3/2", "1/2"]
        assert [row["conditional_fine_weight"] for row in tr["coarse_rows"]] == ["1/2"] * 4
        assert {w for w in tr["fine_weights"] if w is not None} == {"1/2"}
        assert sum(F(row["probability"]) for row in tr["weighted_count_law"]) == F(1, 2)
        assert sum(F(row["probability"]) for row in tr["coarse_weighted_count_law"]) == 1


def test_fixed_interior_is_never_randomly_colored_or_penalized(analyses):
    for analysis in analyses:
        states = analysis["cases"][9]["states"]
        empty = states[0]
        assert (
            empty["kept"] == [0, 3, 7] and empty["color_order"][2] == empty["block_order"][2] == 0
        )
        assert empty["color_graded"][1][0][0] == 1
        for policy in POLICIES:
            assert empty["predictions"][policy]["probabilities"] == ["1"]
            assert empty["predictions"][policy]["count_mean"] == ["1", "1", "0", "0"]
        eligible_edge, fixed_edge = states[10], states[20]
        assert eligible_edge["unmarked_order"] == fixed_edge["unmarked_order"]
        assert eligible_edge["marked_order"] != fixed_edge["marked_order"]
        assert [
            s["predictions"]["iid_half"]["count_mean"][2] for s in (eligible_edge, fixed_edge)
        ] == ["1/4", "1/2"]
        assert all(3 in row["kept"] for state in states for row in state["observations"])


def test_hidden_profile_pooling_and_menu_not_a_random_policy_context(analyses):
    for analysis in analyses:
        h, k = history(analysis, 63, 0), history(analysis, 63, 5)
        assert h["candidate_classes"]["final_only"] == k["candidate_classes"]["final_only"]
        assert h["candidate_classes"]["graded_policy"] == k["candidate_classes"]["graded_policy"]
        assert h["target_classes"]["iid_half_means"] == k["target_classes"]["iid_half_means"]
        assert h["target_classes"]["iid_half_counts"] != k["target_classes"]["iid_half_counts"]
        assert h["target_classes"]["menu_counts"] != k["target_classes"]["menu_counts"]
        assert len(analysis["histories"]) == 6804
        for groups in analysis["target_partitions"].values():
            assert all(len(group["base"]) == 3 and len(group["base"][0]) == 4 for group in groups)


def test_whole_aggregate_is_a_native_type_exact_json_round_trip(aggregate_suite):
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
        {"family": base["family"]},
        {**base, "profile": "ferrers6"},
        {**base, "extra": 1},
        Mapping(base),
        Sequence(),
        {**base, "schema_version": Text(base["schema_version"])},
        {**base, "family": Text(base["family"])},
        {Text("schema_version"): base["schema_version"], "family": base["family"]},
        {"schema_version": base["schema_version"], Text("family"): base["family"]},
        *({**base, "schema_version": value} for value in (None, True, False, 1, [], "wrong")),
        *(
            {**base, "family": value}
            for value in (None, True, False, 1, [], {}, "unknown", "qr05f_ten")
        ),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_fixed_input_schema_rejects_coercions_and_subclasses(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_execution_and_assertion_free_schema_guards(tmp_path):
    script = r"""
import hashlib, importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05h-problem-v1", "family":"qr05g_menu3"}
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
def native(value):
    if value is None or type(value) in (bool, int, str):
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
for number, filename in enumerate(("portability.py", "reference_qr05h.py")):
    name = "_qr05h_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    native(result)
    if result["counts"]["transports"] != 5472 or result["counts"]["positive_histories"] != 3534:
        raise RuntimeError("optimized integrated universe differs")
    digests.append(hashlib.sha256(json.dumps(result,sort_keys=True,allow_nan=False,separators=(",", ":")).encode()).hexdigest())
    del result
    for bad in invalid:
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized schema accepted invalid input")
if digests[0] != digests[1]:
    raise RuntimeError("optimized exact integrated outputs differ")
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
