"""Independent exact sampling-design and observation-channel checks for QR-05E.

All 17 finite laws are enumerated, including structural zero rows.  Covariance
is checked as a weighted centered Gram matrix; scalar coefficients are not CP
maps, conditional probabilities, or a recovered geometry.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from itertools import combinations, pairwise
from math import comb, prod
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
F = Fraction
DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2")
CASES = tuple(
    (order, design)
    for order in ("ferrers6", "standard_example3", "mesh3_center")
    for design in DESIGNS
) + (("ferrers6", "singleton"), ("chain6", "singleton"))
METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")


def problem(order="ferrers6", design="iid_half"):
    return {"schema_version": "det8-qr05e-problem-v1", "order": order, "design": design}


def load_private(name, filename):
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
        load_private("_qr05e_test_direct", "thinning.py"),
        load_private("_qr05e_test_reference", "reference_qr05e.py"),
    )


@pytest.fixture(scope="session")
def results(executors):
    return {case: tuple(module.analyze(problem(*case)) for module in executors) for case in CASES}


@pytest.fixture(scope="session")
def aggregate_suite():
    runner = load_private("_qr05e_test_aggregate_runner", "study.py")
    return runner.run_suite()


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
    raise AssertionError(f"non-native exact JSON type: {type(value)}")


def wire(value):
    require_native(value)
    return json.dumps(value, sort_keys=True, allow_nan=False, separators=(",", ":"))


def fractions(values):
    assert all(type(value) is str and str(F(value)) == value for value in values)
    return list(map(F, values))


def expected_pmf(design, m):
    probabilities = []
    for mask in range(1 << m):
        if design == "identity":
            value = F(int(mask == (1 << m) - 1))
        elif design == "iid_half":
            value = F(1, 1 << m)
        elif design == "heterogeneous":
            marginals = [F(1 if i % 2 == 0 else 2, 3) for i in range(m)]
            value = prod(
                (p if mask & (1 << i) else 1 - p for i, p in enumerate(marginals)), start=F(1)
            )
        elif design == "all_or_none":
            value = F(1, 2) if mask in (0, (1 << m) - 1) else F(0)
        elif design == "fixed_size2":
            value = F(1, comb(m, 2)) if mask.bit_count() == 2 else F(0)
        else:
            assert design == "singleton"
            value = F(1, m) if mask.bit_count() == 1 else F(0)
        probabilities.append(value)
    return probabilities


def expected_past(order):
    if order == "mesh3_center":
        interiors = [(i, j) for i in range(3) for j in range(3)]
        past = [[]]
        for index, (u, v) in enumerate(interiors):
            past.append(
                [0] + [j + 1 for j, (a, b) in enumerate(interiors[:index]) if a <= u and b <= v]
            )
        return past + [list(range(10))]
    past = [[]]
    for index in range(6):
        if order == "chain6":
            internal = list(range(1, index + 1))
        elif index < 3:
            internal = []
        else:
            internal = [
                i + 1
                for i in range(3)
                if (i <= index - 3 if order == "ferrers6" else i != index - 3)
            ]
        past.append([0, *internal])
    return past + [list(range(7))]


def observed_chains(kept, observed_past, source, target, degree):
    local = {original: index for index, original in enumerate(kept)}
    candidates = [vertex for vertex in kept if source < vertex < target]
    chains = []
    for vertices in combinations(candidates, degree):
        path = [source, *vertices, target]
        if all(local[left] in observed_past[local[right]] for left, right in pairwise(path)):
            chains.append(list(vertices))
    return chains


def eligible_mask(vertices, eligible):
    return sum(1 << index for index, vertex in enumerate(eligible) if vertex in vertices)


def question_index(result, probe, degree):
    return next(
        i
        for i, row in enumerate(result["questions"])
        if row["probe"] == probe and row["degree"] == degree
    )


def assert_psd(matrix):
    # Exact Schur-complement elimination accepts genuine semidefinite matrices.
    work = [row[:] for row in matrix]
    n = len(work)
    assert all(len(row) == n for row in work)
    assert all(work[i][j] == work[j][i] for i in range(n) for j in range(n))
    for k in range(n):
        pivot = work[k][k]
        assert pivot >= 0
        if pivot == 0:
            assert all(work[k][j] == work[j][k] == 0 for j in range(k + 1, n))
            continue
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                work[i][j] -= work[i][k] * work[k][j] / pivot


@pytest.mark.parametrize("case", CASES)
def test_complete_outputs_have_native_types_and_identical_wire(results, case):
    direct, reference = results[case]
    assert wire(direct) == wire(reference)
    assert wire(json.loads(wire(direct))) == wire(direct)


def test_prespecified_total_inventory(results):
    analyses = [results[case][0] for case in CASES]
    assert len(analyses) == 17
    assert sum(len(a["samples"]) for a in analyses) == 2048
    assert sum(sum(F(s["probability"]) > 0 for s in a["samples"]) for a in analyses) == 847
    assert sum(len(a["questions"]) for a in analyses) == 108
    assert sum(a["counts"]["estimator_cells"] for a in analyses) == 73728


@pytest.mark.parametrize("case", CASES)
def test_design_pmf_all_joint_inclusions_and_observer_access(results, case):
    order, design = case
    for result in results[case]:
        assert result["order_name"] == order and result["design"] == design
        past = expected_past(order)
        assert wire(result["past"]) == wire(past)
        fixed = [0, 5, 10] if order == "mesh3_center" else [0, 7]
        eligible = [i for i in range(len(past)) if i not in fixed]
        assert wire(result["fixed"]) == wire(fixed) and wire(result["eligible"]) == wire(eligible)
        probes = [{"name": "whole", "source": 0, "target": len(past) - 1}]
        if order == "mesh3_center":
            probes.extend(
                [
                    {"name": "bottom_to_middle", "source": 0, "target": 5},
                    {"name": "middle_to_top", "source": 5, "target": 10},
                ]
            )
        assert wire(result["probes"]) == wire(probes)
        assert F(result["density"]) == (18 if order == "mesh3_center" else 12)
        m = len(eligible)
        pmf = expected_pmf(design, m)
        assert sum(pmf) == 1
        assert [sample["mask"] for sample in result["samples"]] == list(range(1 << m))
        assert fractions([s["probability"] for s in result["samples"]]) == pmf
        inclusion = [
            sum(p for retained, p in enumerate(pmf) if retained & subset == subset)
            for subset in range(1 << m)
        ]
        assert fractions(result["inclusion_probabilities"]) == inclusion
        assert inclusion[0] == 1
        assert all(inclusion[1 << i] > 0 for i in range(m))
        observation_law = []
        for sample, probability in zip(result["samples"], pmf):
            assert type(sample["mask"]) is int
            kept = sorted(
                fixed + [vertex for i, vertex in enumerate(eligible) if sample["mask"] & (1 << i)]
            )
            observed = [
                [i for i, source in enumerate(kept) if source in past[target]] for target in kept
            ]
            assert sample["kept"] == kept and sample["observed_past"] == observed
            if probability > 0:
                observation_law.append(
                    {"kept": kept, "past": observed, "probability": str(probability)}
                )
        assert wire(result["observation_law"]) == wire(observation_law)
        counts = result["counts"]
        assert counts["events"] == len(past) and counts["eligible_events"] == m
        assert counts["mask_rows"] == 1 << m
        assert counts["positive_rows"] == sum(p > 0 for p in pmf)
        assert counts["questions"] == len(result["questions"])
        assert counts["chain_terms"] == sum(len(q["chains"]) for q in result["questions"])
        assert counts["estimator_cells"] == 4 * (1 << m) * len(result["questions"])


@pytest.mark.parametrize("case", CASES)
def test_source_questions_and_all_observed_chain_estimators(results, case):
    for result in results[case]:
        probes = {p["name"]: p for p in result["probes"]}
        assert [(q["probe"], q["degree"]) for q in result["questions"]] == [
            (p["name"], degree) for p in result["probes"] for degree in range(4)
        ]
        eligible = result["eligible"]
        inclusion = fractions(result["inclusion_probabilities"])
        marginals = [inclusion[1 << i] for i in range(len(eligible))]
        pbar = sum(marginals) / len(marginals)
        for qindex, question in enumerate(result["questions"]):
            probe, degree = probes[question["probe"]], question["degree"]
            assert type(degree) is int
            assert type(question["target_count"]) is type(question["supported_count"]) is int
            source_chains = observed_chains(
                list(range(len(result["past"]))),
                result["past"],
                probe["source"],
                probe["target"],
                degree,
            )
            masks = [eligible_mask(vertices, eligible) for vertices in source_chains]
            expected_chains = [
                {"vertices": vertices, "eligible_mask": mask, "inclusion": str(inclusion[mask])}
                for vertices, mask in zip(source_chains, masks)
            ]
            assert wire(question["chains"]) == wire(expected_chains)
            unsupported = [
                vertices for vertices, mask in zip(source_chains, masks) if inclusion[mask] == 0
            ]
            assert question["zero_inclusion_chains"] == unsupported
            assert question["target_count"] == len(source_chains)
            assert question["supported_count"] == len(source_chains) - len(unsupported)
            assert question["full_target_supported"] is (not unsupported)
            alpha = F((-1) ** degree, 2 ** (degree + 1)) / F(result["density"]) ** degree
            assert F(question["scale"]) == alpha
            assert F(question["target_coefficient"]) == alpha * len(source_chains)
            for sample in result["samples"]:
                chains = observed_chains(
                    sample["kept"],
                    sample["observed_past"],
                    probe["source"],
                    probe["target"],
                    degree,
                )
                assert sample["chain_counts"][qindex] == len(chains)
                assert type(sample["chain_counts"][qindex]) is int
                estimates = {method: F(0) for method in METHODS}
                omitted = 0
                for vertices in chains:
                    mask = eligible_mask(vertices, eligible)
                    estimates["raw"] += 1
                    estimates["marginal_product"] += 1 / prod(
                        (p for i, p in enumerate(marginals) if mask & (1 << i)), start=F(1)
                    )
                    estimates["uniform_rate"] += 1 / pbar ** mask.bit_count()
                    if inclusion[mask] == 0:
                        omitted += 1
                    else:
                        estimates["joint_supported"] += 1 / inclusion[mask]
                assert sample["unsupported_observed_terms"][qindex] == omitted
                assert type(sample["unsupported_observed_terms"][qindex]) is int
                assert not omitted or F(sample["probability"]) == 0
                assert set(sample["estimates"]) == set(METHODS)
                for method, expected in estimates.items():
                    token = sample["estimates"][method][qindex]
                    assert type(token) is str and str(F(token)) == token
                    assert F(token) == expected


@pytest.mark.parametrize("case", CASES)
def test_all_exact_moments_coefficient_transform_and_covariance_gram(results, case):
    for result in results[case]:
        targets = [q["target_count"] for q in result["questions"]]
        scales = fractions([q["scale"] for q in result["questions"]])
        probabilities = fractions([s["probability"] for s in result["samples"]])
        for method in METHODS:
            observations = [fractions(sample["estimates"][method]) for sample in result["samples"]]
            dimension = len(targets)
            means = [
                sum(p * row[i] for p, row in zip(probabilities, observations))
                for i in range(dimension)
            ]
            centered = [[value - mean for value, mean in zip(row, means)] for row in observations]
            covariance = [
                [
                    sum(p * row[i] * row[j] for p, row in zip(probabilities, centered))
                    for j in range(dimension)
                ]
                for i in range(dimension)
            ]
            reported = result["moments"][method]
            assert fractions(reported["mean_counts"]) == means
            assert fractions(reported["bias_counts"]) == [
                mean - target for mean, target in zip(means, targets)
            ]
            assert [fractions(row) for row in reported["covariance_counts"]] == covariance
            assert fractions(reported["mean_coefficients"]) == [
                a * mean for a, mean in zip(scales, means)
            ]
            assert fractions(reported["bias_coefficients"]) == [
                a * (mean - target) for a, mean, target in zip(scales, means, targets)
            ]
            coefficient_covariance = [
                [scales[i] * scales[j] * covariance[i][j] for j in range(dimension)]
                for i in range(dimension)
            ]
            assert [
                fractions(row) for row in reported["covariance_coefficients"]
            ] == coefficient_covariance
            exact = [
                sum(p for p, row in zip(probabilities, observations) if row[i] == targets[i])
                for i in range(dimension)
            ]
            assert fractions(reported["exact_target_probabilities"]) == exact
            assert F(reported["vector_exact_target_probability"]) == sum(
                p for p, row in zip(probabilities, observations) if row == targets
            )
            assert_psd(covariance)
            assert_psd(coefficient_covariance)
        assert fractions(result["moments"]["joint_supported"]["mean_counts"]) == [
            q["supported_count"] for q in result["questions"]
        ]


@pytest.mark.parametrize("case", CASES)
def test_joint_covariance_identity_includes_negative_zero_union_terms(results, case):
    for result in results[case]:
        inclusion = fractions(result["inclusion_probabilities"])
        supports = [
            [
                chain["eligible_mask"]
                for chain in question["chains"]
                if inclusion[chain["eligible_mask"]] > 0
            ]
            for question in result["questions"]
        ]
        expected = [
            [
                sum(
                    (
                        inclusion[a | b] / (inclusion[a] * inclusion[b]) - 1
                        for a in left
                        for b in right
                    ),
                    start=F(0),
                )
                for right in supports
            ]
            for left in supports
        ]
        assert [fractions(row) for row in result["joint_covariance_formula"]] == expected
        assert [
            fractions(row) for row in result["moments"]["joint_supported"]["covariance_counts"]
        ] == expected
        if case == ("ferrers6", "fixed_size2"):
            assert any(inclusion[a | b] == 0 for a in supports[2] for b in supports[2])
            assert expected[1][1] == expected[1][2] == 0
            assert expected[2][2] == 54


@pytest.mark.parametrize("order,variance", (("ferrers6", 34), ("standard_example3", 30)))
def test_iid_endpoint_collision_has_distinct_variance_and_never_exact_relation_estimate(
    results, order, variance
):
    for result in results[(order, "iid_half")]:
        moments = result["moments"]["joint_supported"]
        assert fractions(moments["mean_counts"])[1:3] == [F(6), F(6)]
        covariance = [fractions(row) for row in moments["covariance_counts"]]
        assert covariance[1][1] == 6 and covariance[1][2] == 12 and covariance[2][2] == variance
        assert F(moments["exact_target_probabilities"][2]) == 0
        assert all(
            F(sample["estimates"]["joint_supported"][2]) % 4 == 0 for sample in result["samples"]
        )
        assert F(moments["vector_exact_target_probability"]) == 0


@pytest.mark.parametrize("order", ("ferrers6", "standard_example3"))
def test_correlated_all_or_none_needs_joint_not_marginal_weights(results, order):
    for result in results[(order, "all_or_none")]:
        inclusion = fractions(result["inclusion_probabilities"])
        assert all(value == F(1, 2) for value in inclusion[1:])
        assert F(result["moments"]["joint_supported"]["mean_counts"][2]) == 6
        for wrong in ("marginal_product", "uniform_rate"):
            assert F(result["moments"][wrong]["mean_counts"][2]) == 12
            assert F(result["moments"][wrong]["mean_coefficients"][2]) == F(1, 96)
        assert F(result["questions"][2]["target_coefficient"]) == F(1, 192)


@pytest.mark.parametrize(
    "order,wrong_mean", (("ferrers6", F(52, 9)), ("standard_example3", F(56, 9)))
)
def test_heterogeneous_independence_does_not_justify_one_uniform_rate(results, order, wrong_mean):
    for result in results[(order, "heterogeneous")]:
        assert wire(result["moments"]["marginal_product"]) == wire(
            result["moments"]["joint_supported"]
        )
        assert F(result["moments"]["uniform_rate"]["mean_counts"][2]) == wrong_mean != 6


def test_fixed_center_receives_no_random_vertex_weight(results):
    for result in results[("mesh3_center", "iid_half")]:
        full, empty = result["samples"][-1], result["samples"][0]
        assert full["chain_counts"][1:3] == [9, 27]
        assert fractions(full["estimates"]["joint_supported"])[1:3] == [F(17), F(96)]
        assert empty["kept"] == [0, 5, 10]
        assert F(empty["estimates"]["joint_supported"][1]) == 1
        assert F(result["moments"]["joint_supported"]["mean_counts"][1]) == 9
        naive_density_rescaled_mean = sum(
            F(s["probability"]) * 2 * s["chain_counts"][1] for s in result["samples"]
        )
        assert naive_density_rescaled_mean == 10


def test_fixed_size_two_reports_supported_projection_and_vacuous_empty_targets(results):
    for result in results[("mesh3_center", "fixed_size2")]:
        q = question_index(result, "whole", 3)
        target = result["questions"][q]
        assert target["full_target_supported"] is False
        assert target["zero_inclusion_chains"]
        # Center may be first/last as well as the middle chain vertex:
        # two chains below it, nine crossing it, and two chains above it.
        assert target["supported_count"] == 2 + 9 + 2 == 13
        assert target["target_count"] == 37
        assert len(target["zero_inclusion_chains"]) == 24
        mean = F(result["moments"]["joint_supported"]["mean_counts"][q])
        assert mean == target["supported_count"]
        assert F(result["moments"]["joint_supported"]["bias_counts"][q]) < 0
        assert any(s["unsupported_observed_terms"][q] > 0 for s in result["samples"])
        assert all(
            not s["unsupported_observed_terms"][q]
            for s in result["samples"]
            if F(s["probability"]) > 0
        )
        for probe in ("bottom_to_middle", "middle_to_top"):
            empty = result["questions"][question_index(result, probe, 3)]
            assert empty["chains"] == [] and empty["target_count"] == 0
            assert empty["full_target_supported"] is True


def test_singleton_sampling_is_a_genuine_labeled_observation_law_collision(results):
    for ferrers, chain in zip(results[("ferrers6", "singleton")], results[("chain6", "singleton")]):
        assert wire(ferrers["observation_law"]) == wire(chain["observation_law"])
        assert len(ferrers["observation_law"]) == 6
        assert [q["target_count"] for q in ferrers["questions"]] == [1, 6, 6, 0]
        assert [q["target_count"] for q in chain["questions"]] == [1, 6, 15, 20]
        for row in ferrers["observation_law"]:
            assert row["past"] == [[], [0], [0, 1]] and F(row["probability"]) == F(1, 6)
        assert ferrers["questions"][3]["full_target_supported"] is True
        assert chain["questions"][3]["full_target_supported"] is False


@pytest.mark.parametrize("case", CASES)
def test_restricted_hasse_edges_are_a_different_observation_channel(results, case):
    for result in results[case]:
        past = result["past"]
        original_links = {
            (i, j)
            for j, ancestors in enumerate(past)
            for i in ancestors
            if not any(i in past[k] for k in ancestors)
        }
        mismatches = []
        for sample in result["samples"]:
            kept = set(sample["kept"])
            reachability = []
            for probe in result["probes"]:
                reached = {probe["source"]}
                for vertex in sample["kept"]:
                    if any((source, vertex) in original_links for source in reached):
                        reached.add(vertex)
                reachability.append(probe["target"] in reached)
                assert probe["source"] in kept and probe["target"] in kept
                local_source, local_target = (
                    sample["kept"].index(probe["source"]),
                    sample["kept"].index(probe["target"]),
                )
                assert local_source in sample["observed_past"][local_target]
            assert wire(sample["hasse_only_reachability"]) == wire(reachability)
            if not all(reachability) and F(sample["probability"]) > 0:
                mismatches.append(sample)
        probability = sum((F(s["probability"]) for s in mismatches), start=F(0))
        assert F(result["hasse_control"]["mismatch_probability"]) == probability
        first = result["hasse_control"]["first_mismatch"]
        if not mismatches:
            assert first is None
        else:
            sample = mismatches[0]
            assert first == {
                "mask": sample["mask"],
                "kept": sample["kept"],
                "probes": [
                    p["name"]
                    for p, flag in zip(result["probes"], sample["hasse_only_reachability"])
                    if not flag
                ],
            }
        if case[1] == "all_or_none":
            assert probability == F(1, 2)


def test_whole_aggregate_suite_is_native_and_round_trips_exactly(aggregate_suite):
    assert wire(json.loads(wire(aggregate_suite))) == wire(aggregate_suite)


def invalid_inputs():
    base = problem()
    return [
        None,
        [],
        True,
        {},
        {"order": "ferrers6", "design": "iid_half"},
        {**base, "extra": 1},
        {**base, "density": "12"},
        *({**base, "schema_version": v} for v in (True, None, 1, "wrong")),
        *({**base, "order": v} for v in (True, False, None, [], {}, 1, "unknown")),
        *({**base, "design": v} for v in (True, False, None, [], {}, 1, "unknown")),
        problem("chain6", "iid_half"),
        problem("standard_example3", "singleton"),
        problem("mesh3_center", "singleton"),
    ]


@pytest.mark.parametrize("value", invalid_inputs())
def test_strict_seventeen_fixture_schema(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(value)


def test_optimized_execution_and_explicit_schema_rejection(tmp_path):
    script = r"""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05e-problem-v1", "order":"ferrers6", "design":"singleton"}
outputs = []
for number, filename in enumerate(("thinning.py", "reference_qr05e.py")):
    name = "_qr05e_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    result = module.analyze(valid)
    if result["counts"]["mask_rows"] != 64 or result["counts"]["positive_rows"] != 6:
        raise RuntimeError("valid optimized enumeration differs")
    outputs.append(result)
    for bad in (True, {**valid,"extra":1}, {**valid,"order":True}, {**valid,"design":False},
                {**valid,"order":"standard_example3"}, {**valid,"schema_version":1}):
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
