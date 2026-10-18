"""Independent Bernstein-inventory tests of analytic two-color portability.

Only the pinned H JSON is read; no earlier executor is imported. Per-state
calculations are cached, and histories never expand into (S,T,U) triples.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, product
from math import comb
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
H_SHA = "e6d5f06d765ccca7a1da1cef15d12bc15a3287463ec3cce3732aab75af613b3a"
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
)
TARGETS = ("analytic_means", "analytic_counts")
H_TARGETS = (
    "iid_half_means",
    "iid_half_counts",
    "iid_color_means",
    "iid_color_counts",
    "block_coin_means",
    "block_coin_counts",
    "menu_means",
    "menu_counts",
)
GRID = tuple(product((F(0), F(1, 3), F(2, 3), F(1)), repeat=2))
AUDIT_POINTS = tuple(
    dict.fromkeys(
        (
            *GRID,
            (F(1, 2), F(1, 2)),
            (F(1, 3), F(2, 3)),
            (F(2, 5), F(3, 7)),
            (F(1, 5), F(4, 5)),
            (F(1, 2), F(1, 3)),
            (F(0), F(2, 5)),
            (F(3, 7), F(1)),
        )
    )
)


def problem():
    return {"schema_version": "det8-qr05i-problem-v1", "family": "qr05h_two_color"}


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
        private_module("_qr05i_test_direct", "analytic.py"),
        private_module("_qr05i_test_reference", "reference_qr05i.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors):
    return tuple(module.analyze(problem()) for module in executors)


@pytest.fixture(scope="session")
def pinned_h():
    path = HERE.parent / "qr-05h-law-portability-2026-09-06" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == H_SHA
    artifact = json.loads(raw)
    # Runtime metadata may contain descriptive floats; the exact-math suite may not.
    assert (
        json.dumps(artifact, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(artifact["suite"])
    return artifact["suite"]["analysis"]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05i_test_aggregate", "study.py")
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
    d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    counts = []
    for q in range(4):
        number = 0
        for vertices in combinations([v for v in kept if 0 < v < 7], q):
            if all(local[a] in past[local[b]] for a, b in pairwise([0, *vertices, 7])):
                support = [v for v in vertices if v in eligible]
                o = sum(v % 2 for v in support)
                d[q][o][len(support) - o] += 1
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
def bernstein_inventory(profile, s):
    atoms = {}
    for u in submasks(s):
        observation, _, (o, e) = observed(profile, u)
        z = tuple(observation["chain_counts"])
        multiplicities = atoms.setdefault(z, [[0] * 4 for _ in range(4)])
        multiplicities[o][e] += 1
    return atoms


@cache
def power_polynomials(profile, s):
    odd, even = observed(profile, s)[2]
    result = []
    for z, multiplicities in sorted(bernstein_inventory(profile, s).items()):
        coefficients = [[0] * 4 for _ in range(4)]
        for a in range(odd + 1):
            for b in range(even + 1):
                coefficients[a][b] = sum(
                    multiplicities[o][e]
                    * (-1) ** (a - o + b - e)
                    * comb(odd - o, a - o)
                    * comb(even - e, b - e)
                    for o in range(a + 1)
                    for e in range(b + 1)
                )
        result.append({"counts": list(z), "coefficients": coefficients})
    return result


@cache
def evaluate_immutable(coefficients, x, y):
    return sum(
        (F(c) * x**a * y**b for a, row in enumerate(coefficients) for b, c in enumerate(row)),
        start=F(0),
    )


def evaluate(coefficients, x, y):
    return evaluate_immutable(tuple(tuple(row) for row in coefficients), x, y)


@cache
def direct_law(profile, s, x, y):
    odd, even = observed(profile, s)[2]
    return {
        z: sum(
            (
                F(multiplicities[o][e]) * x**o * (1 - x) ** (odd - o) * y**e * (1 - y) ** (even - e)
                for o in range(odd + 1)
                for e in range(even + 1)
            ),
            start=F(0),
        )
        for z, multiplicities in bernstein_inventory(profile, s).items()
    }


def law_wire(atoms):
    return [{"counts": list(z), "probability": str(p)} for z, p in sorted(atoms.items()) if p]


def polynomial_law(state, x, y):
    return {
        tuple(atom["counts"]): evaluate(atom["coefficients"], x, y)
        for atom in state["count_polynomials"]
    }


def test_exact_native_complete_outputs_agree(analyses):
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
def test_state_metadata_and_observed_orders_preserve_pinned_h(analyses, pinned_h, case_index):
    prior = pinned_h["cases"][case_index]
    profile, design = CASES[case_index]
    source, fixed, eligible = population(profile)
    for analysis in analyses:
        case = analysis["cases"][case_index]
        assert set(case) == set(prior)
        assert wire({k: v for k, v in case.items() if k != "states"}) == wire(
            {k: v for k, v in prior.items() if k != "states"}
        )
        assert case["profile"] == profile and case["design"] == design
        assert case["past"] == source and case["fixed"] == fixed and case["eligible"] == eligible
        assert len(case["states"]) == len(prior["states"]) == 1 << len(eligible)
        for s, (state, old) in enumerate(zip(case["states"], prior["states"])):
            assert set(state) == (set(old) - {"predictions", "transports"}) | {
                "color_sizes",
                "count_polynomials",
                "mean_polynomials",
            }
            old_fields = set(old) - {"predictions", "transports"}
            assert wire({k: state[k] for k in old_fields}) == wire({k: old[k] for k in old_fields})
            observation, d, sizes = observed(profile, s)
            assert wire({k: state[k] for k in observation}) == wire(observation)
            assert wire(state["color_sizes"]) == wire(list(sizes))
            assert wire(state["color_graded"]) == wire(d)
            assert wire(state["observations"]) == wire(
                [observed(profile, u)[0] for u in submasks(s)]
            )


@pytest.mark.parametrize("case_index", range(10))
def test_bernstein_inventory_integer_coefficients_degree_normalization_and_means(
    analyses, case_index
):
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            inventory = bernstein_inventory(profile, s)
            odd, even = observed(profile, s)[2]
            assert sum(sum(sum(row) for row in m) for m in inventory.values()) == 2 ** (odd + even)
            for o in range(4):
                for e in range(4):
                    assert all(type(m[o][e]) is int and m[o][e] >= 0 for m in inventory.values())
                    assert sum(m[o][e] for m in inventory.values()) == (
                        comb(odd, o) * comb(even, e) if o <= odd and e <= even else 0
                    )
            expected = power_polynomials(profile, s)
            assert wire(state["count_polynomials"]) == wire(expected)
            assert wire(state["mean_polynomials"]) == wire(observed(profile, s)[1])
            for atom in state["count_polynomials"]:
                coefficients = atom["coefficients"]
                assert len(coefficients) == 4 and all(len(row) == 4 for row in coefficients)
                assert any(c != 0 for row in coefficients for c in row)
                assert all(
                    type(c) is int and abs(c).bit_length() <= 4096
                    for row in coefficients
                    for c in row
                )
                assert all(
                    coefficients[a][b] == 0
                    for a in range(4)
                    for b in range(4)
                    if a > odd or b > even
                )
            for a in range(4):
                for b in range(4):
                    assert sum(atom["coefficients"][a][b] for atom in expected) == int(a == b == 0)
                    for q in range(4):
                        assert (
                            sum(atom["counts"][q] * atom["coefficients"][a][b] for atom in expected)
                            == state["mean_polynomials"][q][a][b]
                        )
                        assert state["graded_counts"][q][a] == sum(
                            state["color_graded"][q][o][e]
                            for o in range(4)
                            for e in range(4)
                            if o + e == a
                        )


@pytest.mark.parametrize("case_index", range(10))
def test_full_grid_held_out_values_and_positive_open_square(analyses, case_index):
    assert len(GRID) == 16 and len(AUDIT_POINTS) == 22
    profile = CASES[case_index][0]
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            for x, y in (*AUDIT_POINTS, (F(2, 7), F(3, 5))):
                actual = polynomial_law(state, x, y)
                expected = direct_law(profile, state["mask"], x, y)
                assert actual == expected
                assert sum(actual.values()) == 1 and all(p >= 0 for p in actual.values())
                if 0 < x < 1 and 0 < y < 1:
                    assert all(p > 0 for p in actual.values())
                for q in range(4):
                    assert sum(z[q] * p for z, p in actual.items()) == evaluate(
                        state["mean_polynomials"][q], x, y
                    )


@pytest.mark.parametrize("case_index", range(10))
def test_all_nine_support_strata_from_compatible_labeled_masks(analyses, case_index):
    profile = CASES[case_index][0]
    eligible = population(profile)[2]
    strata = ((F(0),), (F(1, 4), F(2, 3)), (F(1),))
    for analysis in analyses:
        for state in analysis["cases"][case_index]["states"]:
            s = state["mask"]
            odd_mask = sum(1 << j for j, v in enumerate(eligible) if s & (1 << j) and v % 2)
            even_mask = s ^ odd_mask
            for odd_rates, even_rates in product(strata, repeat=2):
                support = None
                for x, y in product(odd_rates, even_rates):
                    compatible = []
                    for u in submasks(s):
                        if (x == 0 and u & odd_mask) or (x == 1 and u & odd_mask != odd_mask):
                            continue
                        if (y == 0 and u & even_mask) or (y == 1 and u & even_mask != even_mask):
                            continue
                        compatible.append(u)
                    expected = {tuple(observed(profile, u)[0]["chain_counts"]) for u in compatible}
                    positive = {z for z, p in polynomial_law(state, x, y).items() if p > 0}
                    assert positive == expected
                    if support is not None:
                        assert positive == support
                    support = positive
                    if x in (0, 1) and y in (0, 1):
                        assert len(compatible) == len(positive) == 1


@cache
def block_law(profile, s):
    corners = [direct_law(profile, s, F(x), F(y)) for x, y in product((0, 1), repeat=2)]
    return {
        z: sum(law.get(z, F(0)) for law in corners) / 4 for z in bernstein_inventory(profile, s)
    }


@pytest.mark.parametrize("case_index", range(10))
def test_pinned_h_iid_and_block_predictions_recovered_with_coefficient_means(
    analyses, pinned_h, case_index
):
    for analysis in analyses:
        case = analysis["cases"][case_index]
        for state, old in zip(case["states"], pinned_h["cases"][case_index]["states"]):
            laws = {
                "iid_half": polynomial_law(state, F(1, 2), F(1, 2)),
                "iid_color": polynomial_law(state, F(1, 3), F(2, 3)),
                "block_coin": block_law(case["profile"], state["mask"]),
            }
            d_corner_atoms = {}
            for x, y in product((F(0), F(1)), repeat=2):
                z = tuple(int(evaluate(table, x, y)) for table in state["mean_polynomials"])
                d_corner_atoms[z] = d_corner_atoms.get(z, F(0)) + F(1, 4)
            assert law_wire(d_corner_atoms) == law_wire(laws["block_coin"])
            for policy, law in laws.items():
                prior = old["predictions"][policy]
                assert wire(law_wire(law)) == wire(prior["count_law"])
                means = [sum(z[q] * p for z, p in law.items()) for q in range(4)]
                assert prior["count_mean"] == list(map(str, means))
                assert prior["coefficient_mean"] == [
                    str(F((-1) ** q, 2 ** (q + 1) * 12**q) * means[q]) for q in range(4)
                ]


def test_history_candidate_identities_and_inventory(analyses, pinned_h):
    for analysis in analyses:
        assert wire(analysis["candidate_partitions"]) == wire(pinned_h["candidate_partitions"])
        assert wire(analysis["candidate_refinement"]) == wire(pinned_h["candidate_refinement"])
        assert len(analysis["histories"]) == len(pinned_h["histories"]) == 6804
        for actual, old in zip(analysis["histories"], pinned_h["histories"]):
            assert set(actual) == set(old)
            assert wire({k: v for k, v in actual.items() if k != "target_classes"}) == wire(
                {k: v for k, v in old.items() if k != "target_classes"}
            )
            assert set(actual["target_classes"]) == set(TARGETS)
            positive = F(actual["joint_probability"]) > 0
            assert all(
                type(v) is int if positive else v is None for v in actual["target_classes"].values()
            )
        atoms = sum(
            len(bernstein_inventory(case["profile"], state["mask"]))
            for case in analysis["cases"]
            for state in case["states"]
        )
        assert wire(analysis["counts"]) == wire(
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
                "polynomial_atoms": atoms,
                "polynomial_coefficient_cells": 16 * atoms,
                "mean_coefficient_cells": 608 * 64,
            }
        )


@pytest.fixture(scope="session")
def partitions(pinned_h):
    groups, lookups = {t: [] for t in TARGETS}, {t: {} for t in TARGETS}
    ids = []
    for history in pinned_h["histories"]:
        mass = F(history["joint_probability"])
        if not mass:
            ids.append({target: None for target in TARGETS})
            continue
        case = pinned_h["cases"][history["case_index"]]
        profile, s, t = case["profile"], history["stage1_mask"], history["final_mask"]
        final = observed(profile, t)[0]
        base = [
            [case["design"], "12", case["fixed"], case["eligible"]],
            final["kept"],
            final["past"],
        ]
        signatures = {
            "analytic_means": observed(profile, s)[1],
            "analytic_counts": power_polynomials(profile, s),
        }
        row = {}
        for target, signature in signatures.items():
            key = wire([base, signature])
            if key not in lookups[target]:
                index = len(groups[target])
                lookups[target][key] = index
                groups[target].append(
                    {
                        "class_id": index,
                        "members": [],
                        "joint_mass": F(0),
                        "base": base,
                        "signature": signature,
                    }
                )
            index = lookups[target][key]
            groups[target][index]["members"].append(history["history_id"])
            groups[target][index]["joint_mass"] += mass
            row[target] = index
        ids.append(row)
    for collection in groups.values():
        for group in collection:
            group["joint_mass"] = str(group["joint_mass"])
    return groups, ids


def fiber_check(left, right, supported):
    first, collision = {}, None
    for i in supported:
        if left[i] not in first:
            first[left[i]] = i
        elif right[first[left[i]]] != right[i] and collision is None:
            collision = {"left_history": first[left[i]], "right_history": i}
    return collision is None, collision, len({(left[i], right[i]) for i in supported})


def test_partitions_mean_equivalence_refinement_and_first_collisions(
    analyses, pinned_h, partitions
):
    groups, ids = partitions
    histories = pinned_h["histories"]
    supported = [i for i, h in enumerate(histories) if F(h["joint_probability"]) > 0]
    target_matrix = [
        [
            fiber_check([row[a] for row in ids], [row[b] for row in ids], supported)[0]
            for b in TARGETS
        ]
        for a in TARGETS
    ]
    assert target_matrix == [[True, False], [True, True]]
    assessments = {}
    for candidate in CANDIDATES:
        assessments[candidate] = {}
        left = [h["candidate_classes"][candidate] for h in histories]
        for target in TARGETS:
            sufficient, collision, common = fiber_check(
                left, [row[target] for row in ids], supported
            )
            assert sufficient is (common == len(pinned_h["candidate_partitions"][candidate]))
            assessments[candidate][target] = {
                "sufficient": sufficient,
                "first_collision": collision,
                "common_refinement_classes": common,
            }
    d_ids = [h["candidate_classes"]["color_graded"] for h in histories]
    mean_ids = [row["analytic_means"] for row in ids]
    assert fiber_check(d_ids, mean_ids, supported)[0] and fiber_check(mean_ids, d_ids, supported)[0]
    assert assessments["color_graded"]["analytic_means"]["sufficient"] is True
    assert assessments["color_graded"]["analytic_counts"]["sufficient"] is False
    assert all(
        assessments[c][t]["sufficient"] for c in ("full_record", "color_order") for t in TARGETS
    )
    for analysis in analyses:
        assert wire(analysis["target_partitions"]) == wire(groups)
        assert wire(analysis["target_refinement"]) == wire(target_matrix)
        assert wire(analysis["assessments"]) == wire(assessments)
        for history, expected in zip(analysis["histories"], ids):
            assert wire(history["target_classes"]) == wire(expected)
        for classes in analysis["target_partitions"].values():
            assert sorted(i for group in classes for i in group["members"]) == supported
            assert all(group["members"] == sorted(set(group["members"])) for group in classes)
            assert sum(F(group["joint_mass"]) for group in classes) == 10


def test_h_point_menu_signatures_and_analytic_comparisons_use_actual_fibers(pinned_h, partitions):
    _, ids = partitions
    supported = [i for i, h in enumerate(pinned_h["histories"]) if F(h["joint_probability"]) > 0]
    # Every analytic law yields each H menu law, while pointwise converse
    # comparisons are measured as actual fibers, not inferred from counts.
    for target in H_TARGETS:
        coarse = [h["target_classes"][target] for h in pinned_h["histories"]]
        assert fiber_check([row["analytic_counts"] for row in ids], coarse, supported)[0]
        for analytic in TARGETS:
            left = [row[analytic] for row in ids]
            forward = fiber_check(left, coarse, supported)
            backward = fiber_check(coarse, left, supported)
            assert forward[2] == backward[2]
            for result, source, destination in ((forward, left, coarse), (backward, coarse, left)):
                assert result[0] is (result[1] is None)
                if result[1]:
                    a, b = result[1]["left_history"], result[1]["right_history"]
                    assert source[a] == source[b] and destination[a] != destination[b]
    # A fixture-specific coincidence, independently verified across the full
    # supported history universe; the synthetic control below forbids a
    # general finite-point conclusion from this observed equality.
    full = [row["analytic_counts"] for row in ids]
    menu = [h["target_classes"]["menu_counts"] for h in pinned_h["histories"]]
    assert fiber_check(full, menu, supported)[0] and fiber_check(menu, full, supported)[0]


def test_preserved_singleton_correlation_and_star_path_controls(analyses):
    for analysis in analyses:
        states = analysis["cases"][0]["states"]
        odd, even = states[1], states[2]
        assert odd["marked_order"] == even["marked_order"]
        assert odd["mean_polynomials"][1][1][0] == even["mean_polynomials"][1][0][1] == 1
        assert evaluate(odd["mean_polynomials"][1], F(1, 3), F(2, 3)) == F(1, 3)
        assert evaluate(even["mean_polynomials"][1], F(1, 3), F(2, 3)) == F(2, 3)
        assert law_wire(polynomial_law(states[5], F(1, 2), F(1, 2))) == law_wire(
            polynomial_law(states[3], F(1, 2), F(1, 2))
        )
        assert law_wire(block_law("ferrers6", 5)) != law_wire(block_law("ferrers6", 3))
        star, path = states[57], states[27]
        assert star["mean_polynomials"] == path["mean_polynomials"]
        assert star["count_polynomials"] != path["count_polynomials"]
        assert law_wire(block_law("ferrers6", 57)) == law_wire(block_law("ferrers6", 27))
        for policy_point, variances in (
            ((F(1, 2), F(1, 2)), (F(15, 16), F(13, 16))),
            ((F(1, 3), F(2, 3)), (F(68, 81), F(52, 81))),
        ):
            actual = []
            for state in (star, path):
                law = polynomial_law(state, *policy_point)
                mean = sum(z[2] * p for z, p in law.items())
                actual.append(sum((z[2] - mean) ** 2 * p for z, p in law.items()))
            assert tuple(actual) == variances


def test_fixed_and_absent_colors_and_boundary_atom_is_retained(analyses):
    for analysis in analyses:
        empty = analysis["cases"][9]["states"][0]
        assert empty["kept"] == [0, 3, 7] and empty["color_sizes"] == [0, 0]
        assert empty["mean_polynomials"][1][0][0] == 1
        assert empty["count_polynomials"] == [
            {
                "counts": [1, 1, 0, 0],
                "coefficients": [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            }
        ]
        state = analysis["cases"][0]["states"][5]
        assert state["color_sizes"] == [2, 0]
        singleton = next(a for a in state["count_polynomials"] if a["counts"] == [1, 1, 0, 0])
        assert singleton["coefficients"] == [
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [-2, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        for y in (F(0), F(1, 7), F(1)):
            assert evaluate(singleton["coefficients"], F(0), y) == 0
            assert evaluate(singleton["coefficients"], F(1), y) == 0
            assert evaluate(singleton["coefficients"], F(1, 2), y) == F(1, 2)
        assert block_law("ferrers6", 5)[(1, 1, 0, 0)] == 0
        assert all(
            3 in observation["kept"]
            for state in analysis["cases"][9]["states"]
            for observation in state["observations"]
        )


def h_diagnostic(x, y):
    return x * (1 - x) * (2 * y - 1) * (3 * y - 2)


def test_synthetic_selected_point_alias_is_valid_and_not_a_poset_law():
    h_coefficients = [[F(0)] * 4, [F(2), F(-7), F(6), F(0)], [F(-2), F(7), F(-6), F(0)], [F(0)] * 4]
    for x, y in AUDIT_POINTS:
        assert evaluate(h_coefficients, x, y) == h_diagnostic(x, y)
        law = (F(1, 2) + h_diagnostic(x, y) / 4, F(1, 2) - h_diagnostic(x, y) / 4)
        assert sum(law) == 1 and all(F(3, 8) <= p <= F(5, 8) for p in law)
    selected = ((F(1, 2), F(1, 2)), (F(1, 3), F(2, 3)), *product((F(0), F(1)), repeat=2))
    assert all(h_diagnostic(x, y) == 0 for x, y in selected)
    assert h_diagnostic(F(1, 2), F(1, 3)) / 4 == F(1, 48)
    assert F(1, 2) + h_diagnostic(F(1, 2), F(1, 3)) / 4 == F(25, 48)
    # Global bound: |x(1-x)|<=1/4, |2y-1|<=1, |3y-2|<=2.
    assert F(1, 4) * 1 * 2 / 4 == F(1, 8)
    assert any(h_diagnostic(x, y) != 0 for x, y in GRID)


def test_interpolation_certificate_requires_its_declared_degree_bound():
    def outside_degree(x):
        return x * (x - F(1, 3)) * (x - F(2, 3)) * (x - 1)

    assert all(outside_degree(x) == 0 for x, _ in GRID)
    assert outside_degree(F(1, 2)) == F(1, 144)
    # Rational Vandermonde elimination verifies rank four without tolerances.
    vandermonde = [[x**a for a in range(4)] for x in (F(0), F(1, 3), F(2, 3), F(1))]
    for k in range(4):
        pivot = vandermonde[k][k]
        assert pivot != 0
        for j in range(k, 4):
            vandermonde[k][j] /= pivot
        for i in range(k + 1, 4):
            multiplier = vandermonde[i][k]
            for j in range(k, 4):
                vandermonde[i][j] -= multiplier * vandermonde[k][j]


def test_whole_aggregate_native_round_trip(aggregate):
    _, suite = aggregate
    assert wire(json.loads(wire(suite))) == wire(suite)


def test_aggregate_retains_exact_algebraic_diagnostics(aggregate):
    _, suite = aggregate
    controls = suite["controls"]
    alias = controls["selected_rate_alias"]
    h = [[0] * 4, [2, -7, 6, 0], [-2, 7, -6, 0], [0] * 4]
    assert wire(alias["h_coefficients"]) == wire(h)
    assert alias["bidegree"] == [2, 2]
    assert alias["global_component_bounds"] == ["3/8", "5/8"]
    assert "not claimed realizable" in alias["scope"]
    baseline = [["1/2" if a == b == 0 else "0" for b in range(4)] for a in range(4)]
    assert alias["baseline_atom_coefficients"] == [baseline, baseline]
    expected = [
        [[str(F(baseline[a][b]) + sign * F(h[a][b], 4)) for b in range(4)] for a in range(4)]
        for sign in (1, -1)
    ]
    assert alias["perturbed_atom_coefficients"] == expected
    assert alias["witness_point"] == ["1/2", "1/3"]
    assert alias["witness_baseline"] == ["1/2", "1/2"]
    assert alias["witness_perturbed"] == ["25/48", "23/48"]
    assert alias["first_atom_difference"] == "1/48"
    for x, y in alias["coincidence_points"]:
        assert h_diagnostic(F(x), F(y)) == 0
        assert all(evaluate(table, F(x), F(y)) == F(1, 2) for table in expected)
    degree = controls["out_of_degree_grid_alias"]
    assert degree["x_coefficients"] == ["0", "-2/9", "11/9", "-2", "1"]
    assert degree["degree_x"] == 4 and degree["grid_values"] == ["0"] * 4
    assert degree["witness_x"] == "1/2" and degree["witness_value"] == "1/144"
    assert "outside" in degree["scope"] and "not a poset law" in degree["scope"]


def test_aggregate_h_bridge_comparisons_match_independent_all_history_fibers(
    aggregate, pinned_h, partitions
):
    _, suite = aggregate
    bridge = suite["prior_bridge"]
    _, ids = partitions
    supported = [i for i, h in enumerate(pinned_h["histories"]) if F(h["joint_probability"]) > 0]
    expected = {}
    for analytic in TARGETS:
        expected[analytic] = {}
        left = [row[analytic] for row in ids]
        for target in H_TARGETS:
            right = [h["target_classes"][target] for h in pinned_h["histories"]]
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
            expected[analytic][target] = {
                "analytic_refines_prior": directions[0],
                "prior_refines_analytic": directions[1],
                "same_partition": directions[0]["refines"] and directions[1]["refines"],
            }
    assert wire(bridge["target_comparisons"]) == wire(expected)
    assert bridge["H_predictions_reconstructed"] == 1824
    assert bridge["H_labeled_vectors_checked_from_supplied_policy"] == 1824
    assert bridge["H_states_matched"] == 608 and bridge["H_histories_matched"] == 6804
    assert bridge["H_candidate_partitions_matched"] == 12
    assert bridge["analytic_mean_equals_color_graded_partition"] is True
    assert bridge["prior_executors_imported"] is bridge["prior_transports_recomputed"] is False


@pytest.mark.parametrize(
    "mutation",
    (
        "coefficient_type",
        "coefficient_value",
        "degree",
        "padding",
        "mean",
        "grading",
        "atom_fields",
        "atom_missing",
        "observation",
    ),
)
def test_runner_audit_rejects_early_polynomial_and_boundary_inventory_tampering(
    aggregate, analyses, mutation
):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["cases"] = list(changed["cases"])
    changed["cases"][0] = dict(changed["cases"][0])
    changed["cases"][0]["states"] = list(changed["cases"][0]["states"])
    first = json.loads(wire(changed["cases"][0]["states"][0]))
    changed["cases"][0]["states"][0] = first
    if mutation == "coefficient_type":
        first["count_polynomials"][0]["coefficients"][0][0] = True
    elif mutation == "coefficient_value":
        first["count_polynomials"][0]["coefficients"][0][0] = 2
    elif mutation == "degree":
        first["count_polynomials"][0]["coefficients"][0][1] = 1
    elif mutation == "padding":
        first["count_polynomials"][0]["coefficients"].pop()
    elif mutation == "mean":
        first["mean_polynomials"][0][0][0] = 2
    elif mutation == "grading":
        first["graded_counts"][0][0] = 2
    elif mutation == "atom_fields":
        first["count_polynomials"][0]["extra"] = 1
    elif mutation == "atom_missing":
        first["count_polynomials"] = []
    else:
        first["observations"][0]["chain_counts"][0] = 0
    with pytest.raises(ValueError):
        runner.check_analysis(changed)


def test_prior_bridge_rejects_changed_candidate_membership_before_recomputation(
    aggregate, analyses
):
    runner, _ = aggregate
    changed = dict(analyses[0])
    changed["candidate_partitions"] = dict(changed["candidate_partitions"])
    changed["candidate_partitions"]["final_only"] = []
    with pytest.raises(ValueError):
        runner.prior_bridge(changed)


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
            for value in (None, True, False, 1, [], {}, "unknown", "qr05g_menu3")
        ),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_input_rejects_types_values_and_subclasses(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_execution_and_assertion_free_rejections(tmp_path):
    script = r"""
import hashlib, importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05i-problem-v1", "family":"qr05h_two_color"}
class Text(str):
    pass
class Mapping(dict):
    pass
class Sequence(list):
    pass
invalid = (
    True, {**valid,"extra":1}, {**valid,"family":False},
    {**valid,"family":"unknown"}, {**valid,"schema_version":1}, Mapping(valid), Sequence(),
    {**valid,"schema_version":Text(valid["schema_version"])},
    {**valid,"family":Text(valid["family"])},
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
    raise RuntimeError("non-native output")
digests = []
for number, filename in enumerate(("analytic.py", "reference_qr05i.py")):
    name = "_qr05i_optimized_test_" + str(number)
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
    digests.append(hashlib.sha256(json.dumps(result,sort_keys=True,allow_nan=False,separators=(",", ":")).encode()).hexdigest())
    del result
    for bad in invalid:
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized invalid input accepted")
if digests[0] != digests[1]:
    raise RuntimeError("optimized exact routes differ")
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
