"""Independent exact two-stage observation-law tests, without prior executors.

The tests enumerate all transcripts and keep conditional kernels on null first
rows distinct from probability-conditioned states.  No CP-map assumption or
random simulation is used for these signed scalar coefficient questions.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise
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
METHODS = ("final_joint", "sequential_supported", "naive_quarter")


def problem(profile="ferrers6", design="independent"):
    return {"schema_version": "det8-qr05f-problem-v1", "profile": profile, "design": design}


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module name already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load research module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05f_test_direct", "sequential.py"),
        private_module("_qr05f_test_reference", "reference_qr05f.py"),
    )


@pytest.fixture(scope="session")
def results(executors):
    return {case: tuple(module.analyze(problem(*case)) for module in executors) for case in CASES}


@pytest.fixture(scope="session")
def aggregate_suite():
    return private_module("_qr05f_test_aggregate", "study.py").run_suite()


def require_native(value):
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            require_native(item)
        return
    if type(value) is dict:
        assert all(type(key) is str for key in value)
        for item in value.values():
            require_native(item)
        return
    raise AssertionError(f"non-native exact wire type {type(value)}")


def wire(value):
    require_native(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fs(values):
    assert all(type(value) is str and str(F(value)) == value for value in values)
    return list(map(F, values))


def matrix(values):
    return [fs(row) for row in values]


def source(profile):
    past = [[]]
    for j in range(6):
        if profile == "chain6":
            ancestors = list(range(1, j + 1))
        elif j < 3:
            ancestors = []
        else:
            ancestors = [
                i + 1
                for i in range(3)
                if (i != j - 3 if profile == "standard_example3" else i <= j - 3)
            ]
        past.append([0, *ancestors])
    past.append(list(range(7)))
    fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
    eligible = [i for i in range(8) if i not in fixed]
    return past, fixed, eligible


def token(design, first):
    if design == "parity_adaptive":
        return F(2 if first.bit_count() % 2 else 1, 3)
    if design == "parity_hole":
        return F(0 if first.bit_count() % 2 else 1)
    return F(1, 2)


def second_probability(design, first, final):
    if final & first != final:
        return F(0)
    if design == "common_coin":
        if first == 0:
            return F(int(final == 0))
        return F(1, 2) if final in (0, first) else F(0)
    r = token(design, first)
    return r ** final.bit_count() * (1 - r) ** (first.bit_count() - final.bit_count())


def second_inclusion(design, first, support):
    if support & first != support:
        return F(0)
    if support == 0:
        return F(1)
    return F(1, 2) if design == "common_coin" else token(design, first) ** support.bit_count()


@cache
def design_law(case):
    profile, design = case
    _, _, eligible = source(profile)
    m = len(eligible)
    first = (
        [F(1, comb(m, 2)) if s.bit_count() == 2 else F(0) for s in range(1 << m)]
        if design == "first_pair"
        else [F(1, 1 << m)] * (1 << m)
    )
    conditional = {
        (s, t): second_probability(design, s, t)
        for s in range(1 << m)
        for t in range(1 << m)
        if s & t == t
    }
    joint = {(s, t): first[s] * p for (s, t), p in conditional.items()}
    final = [
        sum((p for (s, t), p in joint.items() if t == target), start=F(0))
        for target in range(1 << m)
    ]
    first_inclusion = [
        sum((p for s, p in enumerate(first) if s & a == a), start=F(0)) for a in range(1 << m)
    ]
    final_inclusion = [
        sum((p for t, p in enumerate(final) if t & a == a), start=F(0)) for a in range(1 << m)
    ]
    return first, conditional, joint, final, first_inclusion, final_inclusion


def chain_families(kept, observed_past):
    local = {vertex: i for i, vertex in enumerate(kept)}
    families = []
    for degree in range(4):
        chains = []
        for vertices in combinations([v for v in kept if 0 < v < 7], degree):
            path = [0, *vertices, 7]
            if all(local[a] in observed_past[local[b]] for a, b in pairwise(path)):
                chains.append(list(vertices))
        families.append(chains)
    return families


@cache
def observation(profile, mask):
    past, fixed, eligible = source(profile)
    kept = sorted(fixed + [v for i, v in enumerate(eligible) if mask & (1 << i)])
    observed = [[i for i, a in enumerate(kept) if a in past[b]] for b in kept]
    return kept, observed, chain_families(kept, observed)


def support(vertices, eligible):
    return sum(1 << i for i, vertex in enumerate(eligible) if vertex in vertices)


@cache
def expected_estimates(case, first_mask, final_mask):
    profile, design = case
    _, _, eligible = source(profile)
    _, _, _, _, pi1, pif = design_law(case)
    _, _, families = observation(profile, final_mask)
    estimates = {name: [] for name in METHODS}
    omitted = {name: [] for name in METHODS[:2]}
    for family in families:
        totals = {name: F(0) for name in METHODS}
        missing = {name: 0 for name in METHODS[:2]}
        for vertices in family:
            a = support(vertices, eligible)
            pi2 = second_inclusion(design, first_mask, a)
            totals["naive_quarter"] += 4 ** a.bit_count()
            if pif[a] > 0:
                totals["final_joint"] += 1 / pif[a]
            else:
                missing["final_joint"] += 1
            if pi1[a] > 0 and pi2 > 0:
                totals["sequential_supported"] += 1 / (pi1[a] * pi2)
            else:
                missing["sequential_supported"] += 1
        for name in METHODS:
            estimates[name].append(totals[name])
        for name in METHODS[:2]:
            omitted[name].append(missing[name])
    return estimates, omitted


def moments(probabilities, vectors):
    assert sum(probabilities) == 1
    means = [sum(p * v[i] for p, v in zip(probabilities, vectors)) for i in range(4)]
    centered = [[v[i] - means[i] for i in range(4)] for v in vectors]
    covariance = [
        [sum(p * v[i] * v[j] for p, v in zip(probabilities, centered)) for j in range(4)]
        for i in range(4)
    ]
    return means, covariance


def assert_psd(covariance):
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


@pytest.mark.parametrize("case", CASES)
def test_complete_outputs_are_native_and_exactly_equal(results, case):
    direct, reference = results[case]
    assert wire(direct) == wire(reference)
    assert wire(json.loads(wire(direct))) == wire(direct)
    assert set(direct) == {
        "profile",
        "design",
        "density",
        "past",
        "fixed",
        "eligible",
        "stage1_probabilities",
        "final_probabilities",
        "stage1_inclusions",
        "final_inclusions",
        "questions",
        "first_rows",
        "transcripts",
        "final_rows",
        "moments",
        "variance_decomposition",
        "access",
        "counts",
    }


def test_prespecified_inventory_totals(results):
    analyses = [results[case][0] for case in CASES]
    assert sum(len(a["transcripts"]) for a in analyses) == 6804
    assert (
        sum(sum(F(t["joint_probability"]) > 0 for t in a["transcripts"]) for a in analyses) == 3534
    )
    assert sum(len(a["first_rows"]) for a in analyses) == 608
    assert sum(len(a["final_rows"]) for a in analyses) == 608
    assert sum(len(a["questions"]) for a in analyses) == 40
    assert sum(a["counts"]["estimator_cells"] for a in analyses) == 81648


@pytest.mark.parametrize("case", CASES)
def test_all_transcript_probabilities_compose_and_retain_null_rows(results, case):
    profile, design = case
    p1, conditional, joint, pf, pi1, pif = design_law(case)
    past, fixed, eligible = source(profile)
    for result in results[case]:
        assert (
            result["profile"] == profile
            and result["design"] == design
            and result["density"] == "12"
        )
        for key, expected in (("past", past), ("fixed", fixed), ("eligible", eligible)):
            assert wire(result[key]) == wire(expected)
        assert fs(result["stage1_probabilities"]) == p1
        assert fs(result["final_probabilities"]) == pf
        assert fs(result["stage1_inclusions"]) == pi1
        assert fs(result["final_inclusions"]) == pif
        assert pi1[0] == pif[0] == 1 and sum(p1) == sum(pf) == sum(joint.values()) == 1
        assert [(t["stage1_mask"], t["final_mask"]) for t in result["transcripts"]] == list(joint)
        for transcript in result["transcripts"]:
            s, t = transcript["stage1_mask"], transcript["final_mask"]
            assert type(s) is type(t) is int
            assert F(transcript["conditional_probability"]) == conditional[s, t]
            assert F(transcript["joint_probability"]) == joint[s, t]
        for s in range(len(p1)):
            assert sum(p for (first, _), p in conditional.items() if first == s) == 1
        for a in range(len(pi1)):
            assert pif[a] == sum(p * second_inclusion(design, s, a) for s, p in enumerate(p1))
        counts = result["counts"]
        assert counts["events"] == 8 and counts["eligible_events"] == len(eligible)
        assert counts["first_rows"] == counts["final_rows"] == 1 << len(eligible)
        assert counts["positive_first_rows"] == sum(p > 0 for p in p1)
        assert counts["positive_final_rows"] == sum(p > 0 for p in pf)
        assert counts["transcript_rows"] == 3 ** len(eligible)
        assert counts["positive_transcript_rows"] == sum(p > 0 for p in joint.values())
        assert counts["questions"] == 4
        assert counts["chain_terms"] == sum(len(q["chains"]) for q in result["questions"])
        assert counts["estimator_cells"] == 12 * len(joint)


@pytest.mark.parametrize("case", CASES)
def test_full_source_chain_coverage_and_positive_probability_holes(results, case):
    profile, design = case
    past, _, eligible = source(profile)
    families = chain_families(list(range(8)), past)
    p1, _, _, _, pi1, pif = design_law(case)
    for result in results[case]:
        assert [q["degree"] for q in result["questions"]] == [0, 1, 2, 3]
        for degree, (question, family) in enumerate(zip(result["questions"], families)):
            entries = []
            for vertices in family:
                a = support(vertices, eligible)
                holes = [
                    s
                    for s, p in enumerate(p1)
                    if p > 0 and s & a == a and second_inclusion(design, s, a) == 0
                ]
                gamma = (
                    sum(
                        (
                            p
                            for s, p in enumerate(p1)
                            if s & a == a and second_inclusion(design, s, a) > 0
                        ),
                        start=F(0),
                    )
                    / pi1[a]
                    if pi1[a] > 0
                    else F(0)
                )
                entries.append(
                    {
                        "vertices": vertices,
                        "eligible_mask": a,
                        "pi1": str(pi1[a]),
                        "pif": str(pif[a]),
                        "path_coverage": str(gamma),
                        "conditional_hole_masks": holes,
                    }
                )
            assert wire(question["chains"]) == wire(entries)
            assert type(question["degree"]) is type(question["target_count"]) is int
            assert question["target_count"] == len(family)
            alpha = F((-1) ** degree, 2 ** (degree + 1) * 12**degree)
            assert fs([question["scale"], question["target_coefficient"]]) == [
                alpha,
                alpha * len(family),
            ]
            first_count = sum(F(e["pi1"]) > 0 for e in entries)
            final_count = sum(F(e["pif"]) > 0 for e in entries)
            coverage = sum((F(e["path_coverage"]) for e in entries), start=F(0))
            assert question["first_supported_count"] == first_count
            assert question["final_supported_count"] == final_count
            assert F(question["sequential_coverage_target"]) == coverage
            assert question["full_final_support"] is (final_count == len(family))
            assert question["full_sequential_coverage"] is all(
                F(e["path_coverage"]) == 1 for e in entries
            )


@pytest.mark.parametrize("case", CASES)
def test_observed_orders_operational_estimates_and_conditional_defects(results, case):
    profile, design = case
    _, _, eligible = source(profile)
    p1, conditional, _, pf, pi1, _ = design_law(case)
    for result in results[case]:
        for rows, probabilities in ((result["first_rows"], p1), (result["final_rows"], pf)):
            assert [row["mask"] for row in rows] == list(range(len(probabilities)))
            for row, probability in zip(rows, probabilities):
                kept, past, _ = observation(profile, row["mask"])
                assert type(row["mask"]) is int and F(row["probability"]) == probability
                assert wire(row["kept"]) == wire(kept) and wire(row["past"]) == wire(past)
        for row in result["first_rows"]:
            s = row["mask"]
            assert row["policy_token"] == str(token(design, s))
            _, _, families = observation(profile, s)
            h1, supported, conditional_mean = [], [], []
            for q, family in enumerate(families):
                masks = [support(c, eligible) for c in family]
                h1.append(sum((1 / pi1[a] for a in masks if pi1[a] > 0), start=F(0)))
                supported.append(
                    all(not pi1[a] or second_inclusion(design, s, a) > 0 for a in masks)
                )
                conditional_mean.append(
                    sum(
                        (
                            p * expected_estimates(case, first, t)[0]["sequential_supported"][q]
                            for (first, t), p in conditional.items()
                            if first == s
                        ),
                        start=F(0),
                    )
                )
            assert fs(row["first_estimates"]) == h1
            assert fs(row["sequential_conditional_mean"]) == conditional_mean
            assert fs(row["conditional_defect"]) == [
                mean - initial for mean, initial in zip(conditional_mean, h1)
            ]
            assert all(mean <= initial for mean, initial in zip(conditional_mean, h1))
            assert wire(row["conditional_full_support"]) == wire(supported)
            assert F(row["repeat_probability"]) == second_inclusion(design, s, 1)
        for transcript in result["transcripts"]:
            expected, omitted = expected_estimates(
                case, transcript["stage1_mask"], transcript["final_mask"]
            )
            assert set(transcript["estimates"]) == set(METHODS)
            assert set(transcript["omitted_terms"]) == set(METHODS[:2])
            for method in METHODS:
                assert fs(transcript["estimates"][method]) == expected[method]
            assert wire(transcript["omitted_terms"]) == wire(omitted)
            if F(transcript["joint_probability"]) > 0:
                assert not any(omitted["final_joint"]) and not any(omitted["sequential_supported"])
        for row in result["final_rows"]:
            t = row["mask"]
            _, _, families = observation(profile, t)
            assert wire(row["chain_counts"]) == wire([len(f) for f in families])
            expected, _ = expected_estimates(case, t, t)
            assert fs(row["final_estimate"]) == expected["final_joint"]
            assert fs(row["naive_estimate"]) == expected["naive_quarter"]


@pytest.mark.parametrize("case", CASES)
def test_conditioning_on_final_records_moments_and_total_covariance(results, case):
    _, _, joint, pf, _, _ = design_law(case)
    for result in results[case]:
        grouped = {
            t: [row for row in result["transcripts"] if row["final_mask"] == t]
            for t in range(len(pf))
        }
        rb_probabilities, rb_vectors, conditional_covariances = [], [], []
        for final in result["final_rows"]:
            t = final["mask"]
            if pf[t] == 0:
                assert final["conditional_sequential_mean"] is None
                assert final["conditional_sequential_covariance"] is None
                continue
            probabilities = [F(row["joint_probability"]) / pf[t] for row in grouped[t]]
            vectors = [fs(row["estimates"]["sequential_supported"]) for row in grouped[t]]
            mean, covariance = moments(probabilities, vectors)
            assert fs(final["conditional_sequential_mean"]) == mean
            assert matrix(final["conditional_sequential_covariance"]) == covariance
            assert_psd(covariance)
            rb_probabilities.append(pf[t])
            rb_vectors.append(mean)
            conditional_covariances.append(covariance)
        assert set(result["moments"]) == set(METHODS) | {"rb_sequential"}
        targets = [q["target_count"] for q in result["questions"]]
        scales = fs([q["scale"] for q in result["questions"]])
        computed = {}
        for method in (*METHODS, "rb_sequential"):
            if method == "rb_sequential":
                probabilities, vectors = rb_probabilities, rb_vectors
            else:
                probabilities = list(joint.values())
                vectors = [fs(row["estimates"][method]) for row in result["transcripts"]]
            mean, covariance = moments(probabilities, vectors)
            computed[method] = mean, covariance
            report = result["moments"][method]
            assert fs(report["mean_counts"]) == mean
            assert fs(report["bias_counts"]) == [a - b for a, b in zip(mean, targets)]
            assert matrix(report["covariance_counts"]) == covariance
            assert fs(report["mean_coefficients"]) == [a * b for a, b in zip(mean, scales)]
            assert fs(report["bias_coefficients"]) == [
                (a - b) * c for a, b, c in zip(mean, targets, scales)
            ]
            transformed = [
                [covariance[i][j] * scales[i] * scales[j] for j in range(4)] for i in range(4)
            ]
            assert matrix(report["covariance_coefficients"]) == transformed
            assert_psd(covariance)
            assert_psd(transformed)
        assert computed["sequential_supported"][0] == computed["rb_sequential"][0]
        assert computed["sequential_supported"][0] == fs(
            [q["sequential_coverage_target"] for q in result["questions"]]
        )
        assert computed["final_joint"][0] == [
            q["final_supported_count"] for q in result["questions"]
        ]
        within = [
            [
                sum(p * cov[i][j] for p, cov in zip(rb_probabilities, conditional_covariances))
                for j in range(4)
            ]
            for i in range(4)
        ]
        sequential = computed["sequential_supported"][1]
        rb = computed["rb_sequential"][1]
        residual = [
            [sequential[i][j] - rb[i][j] - within[i][j] for j in range(4)] for i in range(4)
        ]
        assert residual == [[F(0)] * 4 for _ in range(4)]
        report = result["variance_decomposition"]
        assert matrix(report["sequential_covariance"]) == sequential
        assert matrix(report["rb_covariance"]) == rb
        assert matrix(report["mean_conditional_covariance"]) == within
        assert matrix(report["residual"]) == residual
        assert_psd(within)


def first_collision(result, key_name, target):
    representatives = {}
    for row in result["transcripts"]:
        if F(row["joint_probability"]) == 0:
            continue
        s, t = row["stage1_mask"], row["final_mask"]
        first = result["first_rows"][s]
        key = (
            (t,)
            if key_name == "final_only"
            else (t, first["policy_token"])
            if key_name == "policy_token"
            else (t, s)
        )
        values = (
            row["estimates"]["sequential_supported"]
            if target == "estimator"
            else [first["repeat_probability"]]
        )
        if key not in representatives:
            representatives[key] = (s, t, values)
            continue
        old_s, old_t, old_values = representatives[key]
        for index, (old, new) in enumerate(zip(old_values, values)):
            if F(old) != F(new):
                return {
                    "question_index": index,
                    "left": {"stage1_mask": old_s, "final_mask": old_t, "value": old},
                    "right": {"stage1_mask": s, "final_mask": t, "value": new},
                }
    return None


@pytest.mark.parametrize("case", CASES)
def test_access_measurability_and_first_collision_scan(results, case):
    for result in results[case]:
        assert set(result["access"]) == {"final_only", "policy_token", "full_stage1"}
        for key in ("final_only", "policy_token", "full_stage1"):
            for target in ("estimator", "repeat_prediction"):
                collision = first_collision(result, key, target)
                report = result["access"][key][target]
                assert report["measurable"] is (collision is None)
                assert wire(report["first_collision"]) == wire(collision)
        assert result["access"]["policy_token"]["estimator"]["measurable"] is True
        assert all(
            result["access"]["full_stage1"][target]["measurable"]
            for target in ("estimator", "repeat_prediction")
        )


@pytest.mark.parametrize("profile,variance", (("ferrers6", 138), ("standard_example3", 126)))
def test_independent_stages_compose_to_quarter_and_methods_agree(results, profile, variance):
    for result in results[(profile, "independent")]:
        for t, probability in enumerate(fs(result["final_probabilities"])):
            assert probability == F(1, 4) ** t.bit_count() * F(3, 4) ** (6 - t.bit_count())
        assert fs(result["final_inclusions"]) == [F(1, 4) ** a.bit_count() for a in range(64)]
        for row in result["transcripts"]:
            assert (
                row["estimates"]["final_joint"]
                == row["estimates"]["sequential_supported"]
                == row["estimates"]["naive_quarter"]
            )
        report = result["moments"]["final_joint"]
        assert fs(report["mean_counts"])[1:3] == [F(6), F(6)]
        covariance = matrix(report["covariance_counts"])
        assert covariance[1][1] == 18 and covariance[1][2] == 36 and covariance[2][2] == variance


def test_adaptive_inclusions_estimators_rb_and_variance_are_distinct(results):
    expected = [F(1), F(1, 4), F(5, 72), F(1, 48), F(17, 2592), F(11, 5184), F(1, 46656)]
    for result in results[("ferrers6", "parity_adaptive")]:
        assert fs(result["final_inclusions"]) == [expected[a.bit_count()] for a in range(64)]
        lookup = {(t["stage1_mask"], t["final_mask"]): t for t in result["transcripts"]}
        assert F(lookup[1, 1]["joint_probability"]) == F(1, 96)
        assert F(lookup[3, 1]["joint_probability"]) == F(1, 288)
        assert F(lookup[1, 1]["estimates"]["sequential_supported"][1]) == 3
        assert F(lookup[3, 1]["estimates"]["sequential_supported"][1]) == 6
        final = result["final_rows"][1]
        assert F(final["probability"]) == F(1309, 23328)
        assert F(final["conditional_sequential_mean"][1]) == F(570, 119)
        assert F(final["final_estimate"][1]) == 4
        assert F(result["moments"]["sequential_supported"]["covariance_counts"][1][1]) == 21
        assert F(result["moments"]["final_joint"]["covariance_counts"][1][1]) == F(64, 3) > 21
        assert result["access"]["final_only"]["estimator"]["measurable"] is False
        assert result["access"]["policy_token"]["repeat_prediction"]["measurable"] is False
        # This is the README's supported illustrative pair, not necessarily the first collision.
        assert (
            result["first_rows"][0]["policy_token"]
            == result["first_rows"][3]["policy_token"]
            == "1/3"
        )
        assert result["first_rows"][0]["repeat_probability"] == "0"
        assert result["first_rows"][3]["repeat_probability"] == "1/3"
        assert F(lookup[0, 0]["joint_probability"]) > 0 and F(lookup[3, 0]["joint_probability"]) > 0


def test_common_coin_has_correlated_inclusions_and_wrong_quarter_pair_mean(results):
    for result in results[("ferrers6", "common_coin")]:
        assert fs(result["final_inclusions"]) == [
            F(1) if a == 0 else F(1, 2 ** (a.bit_count() + 1)) for a in range(64)
        ]
        empty = result["transcripts"][0]
        assert empty["stage1_mask"] == empty["final_mask"] == 0
        assert empty["conditional_probability"] == "1"
        correct = result["moments"]["final_joint"]
        assert fs(correct["mean_counts"])[1:3] == [F(6), F(6)]
        assert fs(result["moments"]["naive_quarter"]["mean_counts"])[1:3] == [F(6), F(12)]
        covariance = matrix(correct["covariance_counts"])
        assert covariance[1][1] == 48 and covariance[1][2] == 60 and covariance[2][2] == 104


@pytest.mark.parametrize(
    "profile,sequence,final",
    (
        ("ferrers6", [1, 3, 3, 0], [1, 6, 6, 0]),
        ("chain6", [F(1), F(3), F(15, 2), F(10)], [1, 6, 15, 20]),
    ),
)
def test_conditional_holes_keep_fractional_coverage_and_biased_rb_mean(
    results, profile, sequence, final
):
    for result in results[(profile, "parity_hole")]:
        assert all(q["full_final_support"] for q in result["questions"])
        assert fs(result["moments"]["sequential_supported"]["mean_counts"]) == sequence
        assert fs(result["moments"]["rb_sequential"]["mean_counts"]) == sequence
        assert fs(result["moments"]["final_joint"]["mean_counts"]) == final
        for q in result["questions"][1:]:
            assert all(
                F(c["path_coverage"]) == F(1, 2) and c["conditional_hole_masks"]
                for c in q["chains"]
            )
        assert any(
            F(row["probability"]) > 0 and not all(row["conditional_full_support"])
            for row in result["first_rows"]
        )


def test_first_pair_preserves_null_rows_and_does_not_recover_unsupported_triples(results):
    for result in results[("chain6", "first_pair")]:
        question = result["questions"][3]
        assert question["target_count"] == 20
        assert question["first_supported_count"] == question["final_supported_count"] == 0
        assert question["sequential_coverage_target"] == "0"
        assert question["full_final_support"] is question["full_sequential_coverage"] is False
        assert any(row["probability"] == "0" for row in result["first_rows"])
        assert any(
            row["probability"] == "0" and row["chain_counts"][3] > 0 for row in result["final_rows"]
        )
        assert F(result["moments"]["final_joint"]["bias_counts"][3]) == -20


def test_fixed_interior_vertex_is_weighted_once_in_both_stages(results):
    for result in results[("ferrers6_fixed", "independent")]:
        assert result["final_rows"][0]["kept"] == [0, 3, 7]
        assert fs(result["final_rows"][0]["final_estimate"])[1] == 1
        assert fs(result["final_rows"][-1]["final_estimate"])[1:3] == [F(21), F(84)]
        for row in result["transcripts"]:
            assert (
                row["estimates"]["final_joint"]
                == row["estimates"]["sequential_supported"]
                == row["estimates"]["naive_quarter"]
            )
        assert F(result["moments"]["final_joint"]["mean_counts"][1]) == 6


def test_whole_aggregate_suite_is_native_and_round_trips(aggregate_suite):
    assert wire(json.loads(wire(aggregate_suite))) == wire(aggregate_suite)


def invalid_inputs():
    base = problem()
    return [
        None,
        [],
        True,
        {},
        {"profile": "ferrers6", "design": "independent"},
        {**base, "extra": 1},
        {**base, "density": "12"},
        *({**base, "schema_version": v} for v in (True, False, None, 1, "wrong")),
        *({**base, "profile": v} for v in (True, False, None, [], {}, 1, "unknown")),
        *({**base, "design": v} for v in (True, False, None, [], {}, 1, "unknown")),
        problem("chain6", "independent"),
        problem("standard_example3", "parity_adaptive"),
        problem("ferrers6_fixed", "parity_hole"),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_ten_fixture_schema(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_valid_execution_and_explicit_schema_rejections(tmp_path):
    script = r"""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05f-problem-v1", "profile":"ferrers6_fixed", "design":"independent"}
outputs = []
for number, filename in enumerate(("sequential.py", "reference_qr05f.py")):
    name = "_qr05f_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    if result["counts"]["transcript_rows"] != 243 or result["final_rows"][0]["final_estimate"][1] != "1":
        raise RuntimeError("valid optimized fixed-vertex calculation differs")
    outputs.append(result)
    for bad in (True, {**valid,"extra":1}, {**valid,"profile":False}, {**valid,"design":True},
                {**valid,"design":"parity_hole"}, {**valid,"schema_version":1}):
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized schema accepted invalid input")
if json.dumps(outputs[0],sort_keys=True,allow_nan=False) != json.dumps(outputs[1],sort_keys=True,allow_nan=False):
    raise RuntimeError("optimized outputs differ")
print(json.dumps({"valid_routes":2,"explicit_rejections":12}))
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
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 12}
