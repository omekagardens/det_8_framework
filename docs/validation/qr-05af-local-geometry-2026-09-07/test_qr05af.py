"""Independent retained-order observer and exact local sampling diagnostics.

Generic controls do not load any producer artifacts. Fixed tests are separately
named and consume pinned JSON only after the coordinated release.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from fractions import Fraction as F
from itertools import combinations, pairwise
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
WEIGHTS = [[0, 1], [1, 2], [1, 1]]


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
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
    raise AssertionError(f"non-native mathematical wire type: {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def fraction(value):
    assert type(value) is list and len(value) == 2
    n, d = value
    assert type(n) is int and type(d) is int and d > 0
    result = F(n, d)
    assert [result.numerator, result.denominator] == value
    assert max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 4096
    return result


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("private test module name already in use")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("required module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")
SCOPE = dict.fromkeys(
    (
        "full_target_support_inferred",
        "source_moments_inferred",
        "geometry_inferred",
        "observation_origin_authenticated",
        "kernel_is_quantum_channel",
    ),
    False,
)
CAPS = (
    "MAX_BITS",
    "MAX_DEPTH",
    "MAX_NODES",
    "MAX_BYTES",
    "MAX_EVENTS",
    "MAX_ELIGIBLE",
    "MAX_PROBES",
    "MAX_INCLUSION_TERMS",
    "MAX_CHAIN_CANDIDATES",
    "MAX_ESTIMATOR_TERMS",
    "MAX_TOTAL_WORK",
)
HOOKS = ("_inclusions", "_chains", "_weight", "_scale")


def problem_of(mask=3, masses=None, rho=1, past=None, fixed=None, probes=None):
    if past is None:
        past = [list(range(i)) for i in range(4)]
    n = len(past)
    if fixed is None:
        fixed = [0, n - 1]
    eligible = [i for i in range(n) if i not in fixed]
    if masses is None:
        masses = [F(1, 1 << len(eligible))] * (1 << len(eligible))
    if probes is None:
        probes = [{"name": "whole", "source": 0, "target": n - 1}]
    kept = sorted(fixed + [v for i, v in enumerate(eligible) if mask & (1 << i)])
    return {
        "schema_version": "det8-qr05af-problem-v1",
        "family": "qr05af_local_geometry",
        "frame_size": n,
        "fixed": copy.deepcopy(fixed),
        "eligible": eligible,
        "probes": copy.deepcopy(probes),
        "density": fw(rho),
        "mask_probabilities": list(map(fw, masses)),
        "record": {
            "kept": kept,
            "past": [[j for j, p in enumerate(kept) if p in past[v]] for v in kept],
        },
    }


def fixed_internal_problem(mask=3):
    return problem_of(
        mask,
        [F(1, 2), 0, 0, F(1, 2)],
        past=[list(range(i)) for i in range(5)],
        fixed=[0, 2, 4],
        probes=[
            {"name": "whole", "source": 0, "target": 4},
            {"name": "left", "source": 0, "target": 2},
            {"name": "right", "source": 2, "target": 4},
        ],
    )


def independent_analysis(p):
    eligible, kept, past = p["eligible"], p["record"]["kept"], p["record"]["past"]
    m, k, probes = len(eligible), len(kept), len(p["probes"])
    masses = list(map(fraction, p["mask_probabilities"]))
    inclusions = [
        sum(probability for b, probability in enumerate(masses) if b & a == a)
        for a in range(1 << m)
    ]
    pbar = sum(inclusions[1 << i] for i in range(m)) / m
    rho = fraction(p["density"])
    mask = sum(1 << i for i, v in enumerate(eligible) if v in kept)
    original_past = {v: {kept[j] for j in past[i]} for i, v in enumerate(kept)}
    questions, total = [], 0
    for probe in p["probes"]:
        source, target = probe["source"], probe["target"]
        for degree in range(3):
            chains = []
            for vertices in combinations(kept, degree):
                path = (source, *vertices, target)
                if all(a in original_past[b] for a, b in pairwise(path)):
                    support = sum(1 << eligible.index(v) for v in vertices if v in eligible)
                    chains.append(
                        {
                            "vertices": list(vertices),
                            "eligible_mask": support,
                            "inclusion": fw(inclusions[support]),
                        }
                    )
            total += len(chains)
            estimates = dict.fromkeys(METHODS, F(0))
            for chain in chains:
                support = chain["eligible_mask"]
                marginal = F(1)
                for i in range(m):
                    if support & (1 << i):
                        marginal *= inclusions[1 << i]
                estimates["raw"] += 1
                estimates["marginal_product"] += 1 / marginal
                estimates["uniform_rate"] += 1 / pbar ** support.bit_count()
                if inclusions[support]:
                    estimates["joint_supported"] += 1 / inclusions[support]
            scale = F((-1) ** degree, 2 ** (degree + 1)) / rho**degree
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": fw(scale),
                    "observed_count": len(chains),
                    "observed_chains": chains,
                    "unsupported_observed_terms": sum(
                        fraction(c["inclusion"]) == 0 for c in chains
                    ),
                    "count_estimates": {name: fw(v) for name, v in estimates.items()},
                    "coefficient_estimates": {name: fw(scale * v) for name, v in estimates.items()},
                }
            )
    rows, inc, candidates, q = 1 << m, 3**m, probes * (1 + k + k * (k - 1) // 2), 3 * probes
    return {
        "input_sha256": digest(p),
        "mask": mask,
        "probability": fw(masses[mask]),
        "possible": masses[mask] > 0,
        "inclusion_probabilities": list(map(fw, inclusions)),
        "questions": questions,
        "counts": {
            "events": p["frame_size"],
            "eligible_events": m,
            "kept_events": k,
            "mask_rows": rows,
            "questions": q,
            "inclusion_terms": inc,
            "chain_candidates": candidates,
            "observed_chain_terms": total,
            "estimator_terms": 4 * total,
            "coefficient_evaluations": 4 * q,
            "reserved_estimator_terms": 4 * candidates,
            "reserved_total_work": rows + inc + 5 * candidates + 4 * q,
            "total_work": rows + inc + candidates + 4 * total + 4 * q,
        },
        "scope": copy.deepcopy(SCOPE),
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05af_test_primary", "geometry.py"),
        private_module("_qr05af_test_reference", "reference_qr05af.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05af_test_runner", "study.py")


@pytest.mark.parametrize("mask", range(4))
@pytest.mark.parametrize(
    "masses",
    [
        [F(1, 4)] * 4,
        [F(1, 2), 0, 0, F(1, 2)],
        [0, F(1, 2), F(1, 2), 0],
        [F(2, 9), F(1, 9), F(4, 9), F(2, 9)],
    ],
)
def test_generic_complete_wire_matches_original_ID_chain_and_joint_subset_oracle(
    executors, mask, masses
):
    p = problem_of(mask, masses)
    wanted = wire(independent_analysis(p))
    for module in executors:
        assert wire(module.analyze(p)) == wanted


def test_fixed_internal_probe_is_a_counted_unweighted_internal_vertex(executors):
    for module in executors:
        for mask in range(4):
            p = fixed_internal_problem(mask)
            a = module.analyze(p)
            assert wire(a) == wire(independent_analysis(p))
        empty = module.analyze(fixed_internal_problem(0))
        assert empty["questions"][1]["observed_chains"] == [
            {"vertices": [2], "eligible_mask": 0, "inclusion": [1, 1]}
        ]
        assert empty["questions"][1]["count_estimates"] == {m: [1, 1] for m in METHODS}
        full = module.analyze(fixed_internal_problem())
        pair = next(c for c in full["questions"][2]["observed_chains"] if c["vertices"] == [1, 2])
        assert pair["eligible_mask"] == 1 and pair["inclusion"] == [1, 2]
        assert full["questions"][2]["count_estimates"]["joint_supported"] == [6, 1]


def test_probability_zero_records_keep_explicit_unsupported_terms_without_becoming_evidence(
    executors,
):
    p = problem_of(3, [0, F(1, 2), F(1, 2), 0])
    for module in executors:
        a = module.analyze(p)
        assert a["probability"] == [0, 1] and a["possible"] is False
        assert a["questions"][2]["unsupported_observed_terms"] == 1
        assert a["questions"][2]["observed_chains"] == [
            {"vertices": [1, 2], "eligible_mask": 3, "inclusion": [0, 1]}
        ]
        assert a["questions"][2]["count_estimates"] == {
            "raw": [1, 1],
            "marginal_product": [4, 1],
            "uniform_rate": [4, 1],
            "joint_supported": [0, 1],
        }
        assert a["scope"] == SCOPE


def test_noncausal_probe_has_zero_chains_not_a_fabricated_positive_distance(executors):
    p = problem_of(
        past=[[], [0], [0], [0, 1, 2]],
        fixed=[0, 1, 2],
        probes=[{"name": "incomparable", "source": 1, "target": 2}],
        mask=1,
        masses=[F(1, 2), F(1, 2)],
    )
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independent_analysis(p))
        assert all(q["observed_chains"] == [] and q["observed_count"] == 0 for q in a["questions"])
        assert all(
            all(v == [0, 1] for v in q["coefficient_estimates"].values()) for q in a["questions"]
        )


def test_Hasse_channel_is_valid_but_not_authenticated_or_repaired(executors):
    induced = problem_of(mask=0)
    wrong = replaced(induced, ("record", "past"), [[], []])
    for module in executors:
        a, b = module.analyze(induced), module.analyze(wrong)
        assert a["questions"][0]["coefficient_estimates"]["raw"] == [1, 2]
        assert b["questions"][0]["coefficient_estimates"]["raw"] == [0, 1]
        assert b["scope"]["observation_origin_authenticated"] is False
        assert wire(b) == wire(independent_analysis(wrong))


def test_identical_observation_packets_cannot_read_hidden_order_targets_or_source_labels(
    executors, monkeypatch
):
    chain = [list(range(i)) for i in range(4)]
    diamond = [[], [0], [0], [0, 1, 2]]
    law = [0, F(1, 2), F(1, 2), 0]
    assert 1 in chain[2] and 1 not in diamond[2]
    pairs = [
        (problem_of(mask, law, past=chain), problem_of(mask, law, past=diamond)) for mask in (1, 2)
    ]

    def forbidden(*_args, **_kwargs):
        raise RuntimeError("observer attempted external source access")

    for module in executors:
        with monkeypatch.context() as m:
            m.setattr(builtins, "open", forbidden)
            m.setattr(os, "open", forbidden)
            m.setattr(Path, "open", forbidden)
            m.setattr(Path, "read_text", forbidden)
            m.setattr(Path, "read_bytes", forbidden)
            for left, right in pairs:
                assert wire(left) == wire(right)
                assert (
                    wire(module.analyze(left))
                    == wire(module.analyze(right))
                    == wire(independent_analysis(left))
                )


def moments(analyses, probabilities, method="joint_supported", key="count_estimates"):
    vectors = [[fraction(q[key][method]) for q in a["questions"]] for a in analyses]
    mean = [
        sum(p * v[i] for p, v in zip(probabilities, vectors, strict=True))
        for i in range(len(vectors[0]))
    ]
    covariance = [
        [
            sum(
                p * (v[i] - mean[i]) * (v[j] - mean[j])
                for p, v in zip(probabilities, vectors, strict=True)
            )
            for j in range(len(mean))
        ]
        for i in range(len(mean))
    ]
    return mean, covariance


def test_synthetic_design_moments_cross_signs_and_zero_union_cancellation_stay_outside_API(
    executors,
):
    for law, wanted in (
        ([F(1, 4)] * 4, [[0, 0, 0], [0, 2, 2], [0, 2, 3]]),
        ([F(1, 2), 0, 0, F(1, 2)], [[0, 0, 0], [0, 4, 2], [0, 2, 1]]),
    ):
        for module in executors:
            analyses = [module.analyze(problem_of(mask, law)) for mask in range(4)]
            mean, covariance = moments(analyses, law)
            assert mean == [1, 2, 1] and covariance == wanted
            coefficient_mean, coefficient_covariance = moments(
                analyses, law, key="coefficient_estimates"
            )
            scales = [F(1, 2), -F(1, 4), F(1, 8)]
            assert coefficient_mean == [v * s for v, s in zip(mean, scales, strict=True)]
            assert coefficient_covariance == [
                [scales[i] * scales[j] * covariance[i][j] for j in range(3)] for i in range(3)
            ]
            assert coefficient_covariance[1][2] == -F(1, 16)
            assert all(a["scope"]["source_moments_inferred"] is False for a in analyses)
    law = [0, F(1, 2), F(1, 2), 0]
    for module in executors:
        a = [module.analyze(problem_of(mask, law)) for mask in range(4)]
        mean, cov = moments(a, law)
        assert mean == [1, 2, 0] and cov == [[0] * 3 for _ in range(3)]
        assert 2 * (1 / F(1, 2) - 1) + 2 * (0 / (F(1, 2) * F(1, 2)) - 1) == 0


def test_cross_probe_covariance_and_density_scaling_use_the_same_law(executors):
    law = [F(1, 2), 0, 0, F(1, 2)]
    for module in executors:
        cases = [module.analyze(fixed_internal_problem(mask)) for mask in range(4)]
        mean, covariance = moments(cases, law)
        assert mean[1] == 3 and covariance[4][7] == 1
        assert covariance[1][4] == covariance[1][7] == 2
        for mask, old in enumerate(cases):
            p = fixed_internal_problem(mask)
            p["density"] = [1, 4]
            new = module.analyze(p)
            for left, right in zip(old["questions"], new["questions"], strict=True):
                assert left["count_estimates"] == right["count_estimates"]
                for method in METHODS:
                    assert fraction(right["coefficient_estimates"][method]) == 4 ** left[
                        "degree"
                    ] * fraction(left["coefficient_estimates"][method])


def test_retained_scale_overflow_rejects_but_large_internal_square_can_cancel(executors):
    good = problem_of(rho=F(1, 1 << 2048))
    assert ((1 << 2048) ** 2).bit_length() == 4097
    wanted = independent_analysis(good)
    native(wanted)
    for module in executors:
        assert wire(module.analyze(good)) == wire(wanted)
        for rho in (F(1, 1 << 2049), F(1 << 2048)):
            with pytest.raises(ValueError):
                module.analyze(problem_of(rho=rho))


def test_tiny_positive_joint_support_is_not_zero_and_retained_count_overflow_cannot_hide_in_density(
    executors,
):
    d = 1 << 4095
    p = problem_of(3, [F(d - 1, d), 0, 0, F(1, d)])
    # The single ordered pair has weight d (valid), but two observed vertices
    # produce count2d, a4097-bit retained scalar even if rho could cancel later.
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)
        small = problem_of(3, [F((1 << 128) - 1, 1 << 128), 0, 0, F(1, 1 << 128)])
        a = module.analyze(small)
        assert a["possible"] is True and a["questions"][2]["unsupported_observed_terms"] == 0
        assert a["questions"][2]["count_estimates"]["joint_supported"] == [1 << 128, 1]


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
    p = problem_of()
    bad = [None, [], (), DictChild(p), {**p, 1: 0}]
    bad += [
        {**p, key: []}
        for key in (
            "extra",
            "source",
            "coordinates",
            "population",
            "full_past",
            "targets",
            "fixture",
        )
    ]
    bad += [{k: v for k, v in p.items() if k != key} for key in p]
    for key in ("schema_version", "family"):
        bad += [replaced(p, (key,), v) for v in (None, "wrong", StrChild(p[key]), True)]
    bad += [replaced(p, ("frame_size",), v) for v in (True, 4.0, IntChild(4), "4", 1, 13)]
    for path in (("fixed",), ("eligible",), ("record", "kept")):
        row = p
        for key in path:
            row = row[key]
        for v in (
            None,
            tuple(row),
            ListChild(row),
            [],
            row[::-1],
            row + row[:1],
            [-1],
            [4],
            [False] + row[1:],
            [IntChild(row[0])] + row[1:],
        ):
            bad.append(replaced(p, path, v))
    bad += [
        replaced(p, ("fixed",), [0]),
        replaced(p, ("eligible",), [1]),
        replaced(p, ("eligible",), [0, 1, 2]),
        replaced(p, ("record", "kept"), [0, 1, 2]),
    ]
    bad += [
        replaced(p, ("probes",), v) for v in (None, (), ListChild(p["probes"]), [], p["probes"] * 2)
    ]
    row = p["probes"][0]
    bad += [
        replaced(p, ("probes", 0), v)
        for v in (None, [], DictChild(row), {**row, "coordinates": []})
    ]
    bad += [replaced(p, ("probes", 0), {k: v for k, v in row.items() if k != key}) for key in row]
    bad += [
        replaced(p, ("probes", 0, "name"), v)
        for v in (None, "", "A", "0whole", "a-b", "a b", "é", "a" * 41, StrChild("whole"))
    ]
    for key in ("source", "target"):
        bad += [
            replaced(p, ("probes", 0, key), v) for v in (False, 0.0, IntChild(0), "0", -1, 4, 1)
        ]
    bad += [
        replaced(p, ("probes", 0, "source"), 3),
        replaced(p, ("probes", 0, "target"), 0),
        replaced(p, ("probes",), [row, {**row, "name": "other"}]),
    ]
    for path in (("density",), ("mask_probabilities", 0)):
        bad += [
            replaced(p, path, v)
            for v in (
                None,
                (0, 1),
                ListChild([0, 1]),
                [],
                [1],
                [0, 1, 2],
                [False, 1],
                [0, True],
                [IntChild(0), 1],
                [0, IntChild(1)],
                [0.0, 1],
                [0, 1.0],
                ["0", 1],
                [0, 0],
                [0, -1],
                [0, 2],
                [2, 4],
                [1, 1 << 4096],
                [1 << 4096, 1],
            )
        ]
    bad += [replaced(p, ("density",), v) for v in ([0, 1], [-1, 1])]
    bad += [
        replaced(p, ("mask_probabilities",), v)
        for v in (
            None,
            (),
            ListChild(p["mask_probabilities"]),
            [],
            [[1, 1]],
            p["mask_probabilities"][:-1],
            p["mask_probabilities"] * 2,
        )
    ]
    bad += [replaced(p, ("mask_probabilities", 0), v) for v in ([-1, 1], [2, 1], [1, 3])]
    bad += [
        replaced(p, ("mask_probabilities",), v)
        for v in ([[1, 1], [0, 1], [0, 1], [0, 1]], [[0, 1], [1, 1], [0, 1], [0, 1]])
    ]
    bad += [
        replaced(p, ("record",), v)
        for v in (
            None,
            [],
            DictChild(p["record"]),
            {**p["record"], "source": "leak"},
            {"kept": p["record"]["kept"]},
            {"past": p["record"]["past"]},
        )
    ]
    bad += [
        replaced(p, ("record", "past"), v)
        for v in (
            None,
            (),
            ListChild(p["record"]["past"]),
            [],
            p["record"]["past"][:-1],
            p["record"]["past"] * 2,
        )
    ]
    bad += [
        replaced(p, ("record", "past", 3), v)
        for v in (
            None,
            (),
            ListChild([0, 1, 2]),
            [2, 1, 0],
            [0, 0, 1],
            [-1],
            [3],
            [False],
            [0.0],
            [IntChild(0)],
            [1, 2],
        )
    ]
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_schema_leakage_labels_normalization_and_transitivity_are_not_repaired(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def planned_caps(p):
    m, k, probes = len(p["eligible"]), len(p["record"]["kept"]), len(p["probes"])
    c, q = probes * (1 + k + k * (k - 1) // 2), 3 * probes
    return {
        "MAX_EVENTS": p["frame_size"],
        "MAX_ELIGIBLE": m,
        "MAX_PROBES": probes,
        "MAX_INCLUSION_TERMS": 3**m,
        "MAX_CHAIN_CANDIDATES": c,
        "MAX_ESTIMATOR_TERMS": 4 * c,
        "MAX_TOTAL_WORK": (1 << m) + 3**m + 5 * c + 4 * q,
    }


def test_complete_reservation_and_schema_precede_all_hooks_with_exact_call_inventory(
    executors, monkeypatch
):
    p = fixed_internal_problem()
    wanted = independent_analysis(p)
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as m:
            for name in HOOKS:
                original = getattr(module, name)

                def counted(*args, name=name, original=original, calls=calls):
                    calls[name] += 1
                    return original(*args)

                m.setattr(module, name, counted)
            assert wire(module.analyze(p)) == wire(wanted)
        assert calls == {
            "_inclusions": 1,
            "_chains": wanted["counts"]["questions"],
            "_weight": wanted["counts"]["estimator_terms"],
            "_scale": wanted["counts"]["questions"],
        }

        def forbidden(*_args):
            raise RuntimeError("work preceded complete reservation")

        for constant, limit in planned_caps(p).items():
            with monkeypatch.context() as m:
                m.setattr(module, constant, limit - 1)
                for name in HOOKS:
                    m.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        with monkeypatch.context() as m:
            for name in HOOKS:
                m.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(replaced(p, ("record", "past", 4), [2, 3]))
        with monkeypatch.context() as m:
            for name in ("_weight", "_scale"):
                m.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(
                    replaced(p, ("mask_probabilities",), [[1, 1], [0, 1], [0, 1], [0, 1]])
                )


@pytest.mark.parametrize("constant", CAPS)
def test_every_live_cap_restores_without_cached_admission(executors, monkeypatch, constant):
    p = fixed_internal_problem()
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as m:
            m.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def mutable_ids(value):
    if type(value) not in (dict, list):
        return set()
    answer = {id(value)}
    for child in value.values() if type(value) is dict else value:
        answer |= mutable_ids(child)
    return answer


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def test_native_exact_scalar_empty_shared_depth_ascii_nodes_and_output_bytes(
    executors, monkeypatch
):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    for module in executors:
        for v in (nested(0, 64), nested([], 64)):
            module._native(v)
        for v in (nested(0, 65), nested([], 65)):
            with pytest.raises(ValueError):
                module._native(v)
        shared = [0]
        module._native([shared, nested(shared, 62)])
        with pytest.raises(ValueError):
            module._native([shared, nested(shared, 63)])
        for constant, limit in (
            ("MAX_NODES", 8),
            ("MAX_DEPTH", 2),
            ("MAX_BYTES", len(wire(value))),
        ):
            with monkeypatch.context() as m:
                m.setattr(module, constant, limit)
                module._native(value)
                m.setattr(module, constant, limit - 1)
                with pytest.raises(ValueError):
                    module._native(value)
        p = shared_problem()
        nodes, depth = tree_resources(p)
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("unsafe tree serialized")

            with monkeypatch.context() as m:
                m.setattr(module, constant, limit)
                m.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        wanted = wire(module.analyze(p))
        assert len(wanted) > len(wire(p))
        with monkeypatch.context() as m:
            m.setattr(module, "MAX_BYTES", len(wanted) - 1)
            with pytest.raises(ValueError):
                module.analyze(p)
            m.setattr(module, "MAX_BYTES", len(wanted))
            assert wire(module.analyze(p)) == wanted


def shared_problem():
    p = problem_of()
    p["mask_probabilities"] = [[1, 4]] * 4
    return p


def test_outputs_are_detached_from_inputs_other_questions_and_calls(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        left, right = module.analyze(p), module.analyze(p)
        wanted = wire(right)
        assert not (mutable_ids(left) & (mutable_ids(p) | mutable_ids(right)))
        left["questions"][0]["count_estimates"]["raw"][0] = -1
        left["inclusion_probabilities"][0][0] = 2
        assert wire(p) == before and wire(right) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["density"] = [2, 1]
        assert wire(detached) == wanted and wire(module.analyze(changed)) != wanted


def graph_inputs(p):
    cycle = []
    cycle.append(cycle)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    dag = []
    for _ in range(40):
        dag = [dag, dag]
    for value in (cycle, cycle_dict, nested([], 1500), dag):
        yield {**p, "extra": value}
    for path in (
        ("fixed",),
        ("eligible",),
        ("probes",),
        ("probes", 0),
        ("probes", 0, "source"),
        ("density",),
        ("mask_probabilities",),
        ("mask_probabilities", 0, 1),
        ("record",),
        ("record", "kept"),
        ("record", "past"),
        ("record", "past", 3),
    ):
        yield replaced(p, path, dag)


def test_generic_auditor_complete_wire_includes_zero_rows_and_observer_scope():
    audit = private_module("_qr05af_test_generic_audit", "audit_json.py")
    for p in (problem_of(), fixed_internal_problem(0), problem_of(3, [0, F(1, 2), F(1, 2), 0])):
        assert wire(audit.expected_packet(p)) == wire(independent_analysis(p))


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05af_guards",Path(sys.argv[1]))
if spec is None or spec.loader is None:raise RuntimeError("missing helpers")
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
rejections=pre=0
def require(value,message):
    if not value:raise RuntimeError(message)
def reject(call,value):
    global rejections
    try:call(value)
    except ValueError:rejections+=1
    else:raise RuntimeError("invalid input accepted")
def before_dump(call,value):
    global pre
    original=json.dumps
    def forbidden(*args,**kwargs):raise RuntimeError("unsafe tree serialized")
    json.dumps=forbidden
    try:reject(call,value);pre+=1
    finally:json.dumps=original
valid=h.fixed_internal_problem();shared_valid=h.shared_problem();invalid=h.invalid_problems()
require(len(list(h.graph_inputs(valid)))==16,"graph fixture inventory")
for i,filename in enumerate(("geometry.py","reference_qr05af.py")):
    module=h.private_module("_qr05af_guard_core"+str(i),filename)
    for p in (valid,shared_valid,h.fixed_internal_problem(0),h.problem_of(3,[0,h.F(1,2),h.F(1,2),0])):
        require(h.wire(module.analyze(p))==h.wire(h.independent_analysis(p)),"complete generic packet wire")
    for bad in invalid:reject(module.analyze,bad)
    for bad in h.graph_inputs(valid):before_dump(module.analyze,bad)
    def forbidden(*args):raise RuntimeError("work preceded complete reservation")
    require(len(h.planned_caps(valid))==7 and len(h.CAPS)==11,"live-cap fixture inventory")
    for constant,limit in h.planned_caps(valid).items():
        old=getattr(module,constant);hooks={n:getattr(module,n) for n in h.HOOKS}
        setattr(module,constant,limit-1)
        for n in hooks:setattr(module,n,forbidden)
        try:reject(module.analyze,valid)
        finally:
            setattr(module,constant,old)
            for n,v in hooks.items():setattr(module,n,v)
    for constant in h.CAPS:
        old=getattr(module,constant);setattr(module,constant,1)
        try:reject(module.analyze,valid)
        finally:setattr(module,constant,old)
    hooks={n:getattr(module,n) for n in h.HOOKS}
    for n in hooks:setattr(module,n,forbidden)
    try:reject(module.analyze,h.replaced(valid,("record","past",4),[2,3]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    hooks={n:getattr(module,n) for n in ("_chains","_weight","_scale")}
    for n in hooks:setattr(module,n,forbidden)
    try:reject(module.analyze,h.problem_of(3,[1,0,0,0]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    for v in (h.nested(0,64),h.nested([],64)):module._native(v)
    for v in (h.nested(0,65),h.nested([],65)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,62)]);reject(module._native,[shared,h.nested(shared,63)])
    tiny=h.F(1,1<<3000)
    reject(module.analyze,h.problem_of(3,[1-tiny,0,0,tiny]))
    reject(module.analyze,h.problem_of(rho=tiny))
    old=module.MAX_BITS;module.MAX_BITS=2
    try:require(module._weight("marginal_product",3,[h.F(1),h.F(3,7),h.F(3,7),h.F(3,7)],h.F(3,7))==h.F(49,9),"unretained inverse must remain unbounded")
    finally:module.MAX_BITS=old
    scalar={'"\\\\\b\f\n\r\t\x00\x1f é 🐈 \ud800':["é","🐈","\udfff",-123,False,None]}
    for constant,limit in (("MAX_NODES",8),("MAX_DEPTH",2),("MAX_BYTES",len(h.wire(scalar)))):
        old=getattr(module,constant);setattr(module,constant,limit)
        try:
            module._native(scalar)
            setattr(module,constant,limit-1);reject(module._native,scalar)
        finally:setattr(module,constant,old)
    wanted=h.wire(module.analyze(shared_valid));old=module.MAX_BYTES
    require(len(wanted)>len(h.wire(shared_valid)),"output-byte fixture nonvacuous")
    module.MAX_BYTES=len(wanted)-1
    try:reject(module.analyze,shared_valid)
    finally:module.MAX_BYTES=old
    nodes,depth=h.tree_resources(shared_valid)
    for constant,limit in (("MAX_NODES",nodes-1),("MAX_DEPTH",depth-1),("MAX_BYTES",len(h.wire(shared_valid))-1)):
        old=getattr(module,constant);setattr(module,constant,limit)
        try:before_dump(module.analyze,shared_valid)
        finally:setattr(module,constant,old)
    result=module.analyze(shared_valid);result["questions"][0]["count_estimates"]["raw"][0]=-1
    result["inclusion_probabilities"][0][0]=2
    require(h.wire(module.analyze(shared_valid))==h.wire(h.independent_analysis(shared_valid)),"ownership and restored caps")
runner=h.private_module("_qr05af_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,128),h.nested([],128)):runner.require_wire(v)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==54,"pre-serialization rejection inventory")
require(rejections==2*(len(invalid)+48)+20,"explicit rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05af.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 48) + 20,
        "pre_serialization_rejections": 54,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2", "singleton")
SPECIFICATIONS = (
    [("mesh3", d) for d in DESIGNS]
    + [
        (name, d)
        for name in ("mesh3_boost", "mesh3_dilate", "mesh3_dilate_wrong_density", "mesh3_warp")
        for d in ("identity", "iid_half")
    ]
    + [(name, d) for name in ("ferrers6", "standard_example3") for d in ("identity", "iid_half")]
    + [("ferrers6", "singleton"), ("chain6", "singleton")]
)


def independent_source(name):
    coords = None
    if name.startswith("mesh3"):
        grid = [(i, j) for i in range(1, 4) for j in range(1, 4)]
        coords = [
            (F(0), F(0)),
            *((F(12 * i + j, 52), F(12 * j + i, 52)) for i, j in grid),
            (F(1), F(1)),
        ]
        past = (
            [[]]
            + [
                [0]
                + [k + 1 for k, (a, b) in enumerate(grid) if a <= i and b <= j and (a, b) != (i, j)]
                for i, j in grid
            ]
            + [list(range(10))]
        )
        rho, fixed = F(18), [0, 3, 5, 7, 10]
        if name == "mesh3_boost":
            coords = [(2 * u, v / 2) for u, v in coords]
        if name in ("mesh3_dilate", "mesh3_dilate_wrong_density"):
            coords = [(2 * u, 2 * v) for u, v in coords]
            if name == "mesh3_dilate":
                rho = F(9, 2)
        if name == "mesh3_warp":
            coords = [(u * u, v * v) for u, v in coords]
        triples = [
            ("whole", 0, 10),
            ("bottom_to_p5", 0, 5),
            ("p5_to_top", 5, 10),
            ("bottom_to_p3", 0, 3),
            ("p3_to_top", 3, 10),
            ("bottom_to_p7", 0, 7),
            ("p7_to_top", 7, 10),
        ]
    else:
        rho, fixed, triples = F(12), [0, 7], [("whole", 0, 7)]
        if name == "chain6":
            past = [list(range(i)) for i in range(8)]
        else:
            past = [[]] + [[0] for _ in range(3)]
            past += [
                [0] + [i + 1 for i in range(3) if (i <= j if name == "ferrers6" else i != j)]
                for j in range(3)
            ]
            past += [list(range(7))]
        if name == "ferrers6":
            coords = [
                (F(0), F(0)),
                *(
                    (F(u, 16), F(v, 16))
                    for u, v in ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
                ),
                (F(1), F(1)),
            ]
    if coords is not None:
        assert past == [
            [i for i, (u, v) in enumerate(coords) if u < uu and v < vv] for uu, vv in coords
        ]
    return {
        "name": name,
        "coordinates": None if coords is None else [[fw(u), fw(v)] for u, v in coords],
        "past": past,
        "fixed": fixed,
        "eligible": [i for i in range(len(past)) if i not in fixed],
        "probes": [{"name": n, "source": s, "target": t} for n, s, t in triples],
        "density": fw(rho),
        "density_kind": "intentionally_wrong"
        if name == "mesh3_dilate_wrong_density"
        else "algebraic_only"
        if coords is None
        else "whole_volume_calibrated",
    }


def independent_design(name, m=6):
    weights = []
    for mask in range(1 << m):
        size = mask.bit_count()
        if name == "identity":
            value = F(mask == (1 << m) - 1)
        elif name == "iid_half":
            value = F(1, 1 << m)
        elif name == "all_or_none":
            value = F(1, 2) if mask in (0, (1 << m) - 1) else F(0)
        elif name == "singleton":
            value = F(1, m) if size == 1 else F(0)
        elif name == "fixed_size2":
            value = F(1, len(list(combinations(range(m), 2)))) if size == 2 else F(0)
        else:
            assert name == "heterogeneous"
            value = F(1)
            for i in range(m):
                p = F(1 + (i % 2), 3)
                value *= p if mask & (1 << i) else 1 - p
        weights.append(value)
    assert sum(weights) == 1
    return {"name": name, "mask_probabilities": list(map(fw, weights))}


def make_packet(source, design, mask):
    return problem_of(
        mask,
        list(map(fraction, design["mask_probabilities"])),
        fraction(source["density"]),
        source["past"],
        source["fixed"],
        source["probes"],
    )


def independent_population(source, design):
    full = independent_analysis(make_packet(source, design, (1 << len(source["eligible"])) - 1))
    questions, geometry = [], None if source["coordinates"] is None else []
    rho = fraction(source["density"])
    for i, probe in enumerate(source["probes"]):
        tau = None
        if geometry is not None:
            u, v = map(fraction, source["coordinates"][probe["source"]])
            uu, vv = map(fraction, source["coordinates"][probe["target"]])
            assert uu > u and vv > v
            tau = (uu - u) * (vv - v)
        for degree, q in enumerate(full["questions"][3 * i : 3 * i + 3]):
            scale, count = fraction(q["scale"]), q["observed_count"]
            missing = [r["vertices"] for r in q["observed_chains"] if fraction(r["inclusion"]) == 0]
            continuum = None if tau is None else (F(1, 2), -tau / 8, tau * tau / 128)[degree]
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": fw(scale),
                    "chains": copy.deepcopy(q["observed_chains"]),
                    "target_count": count,
                    "target_coefficient": fw(count * scale),
                    "supported_count": count - len(missing),
                    "zero_inclusion_chains": missing,
                    "full_target_supported": not missing,
                    "continuum_coefficient": None if continuum is None else fw(continuum),
                    "finite_geometry_error": None
                    if continuum is None
                    else fw(count * scale - continuum),
                }
            )
        if geometry is not None:
            count_volume = F(full["questions"][3 * i + 1]["observed_count"]) / rho
            geometry.append(
                {
                    "probe": probe["name"],
                    "source": probe["source"],
                    "target": probe["target"],
                    "tau_squared": fw(tau),
                    "volume": fw(tau / 2),
                    "finite_count_volume": fw(count_volume),
                    "volume_error": fw(count_volume - tau / 2),
                }
            )
    return {"questions": questions, "interval_geometry": geometry}


def independent_moments(population, samples):
    probabilities = [fraction(s["analysis"]["probability"]) for s in samples]
    analyses = [s["analysis"] for s in samples]
    targets = [q["target_count"] for q in population["questions"]]
    scales = [fraction(q["scale"]) for q in population["questions"]]
    answer = {}
    for method in METHODS:
        mean, covariance = moments(analyses, probabilities, method)
        cm, cc = moments(analyses, probabilities, method, "coefficient_estimates")
        assert cm == [v * s for v, s in zip(mean, scales, strict=True)]
        assert cc == [
            [scales[i] * scales[j] * covariance[i][j] for j in range(len(scales))]
            for i in range(len(scales))
        ]
        comparisons = None
        if population["interval_geometry"] is not None:
            comparisons = []
            for i, q in enumerate(population["questions"]):
                continuum, finite = (
                    fraction(q["continuum_coefficient"]),
                    fraction(q["target_coefficient"]),
                )
                comparisons.append(
                    {
                        "probe": q["probe"],
                        "degree": q["degree"],
                        "continuum": fw(continuum),
                        "mean": fw(cm[i]),
                        "sampling_bias": fw(cm[i] - finite),
                        "finite_model_discrepancy": fw(finite - continuum),
                        "total_discrepancy": fw(cm[i] - continuum),
                    }
                )
        answer[method] = {
            "mean_counts": list(map(fw, mean)),
            "bias_counts": [fw(v - t) for v, t in zip(mean, targets, strict=True)],
            "covariance_counts": [list(map(fw, row)) for row in covariance],
            "mean_coefficients": list(map(fw, cm)),
            "bias_coefficients": [
                fw(s * (v - t)) for s, v, t in zip(scales, mean, targets, strict=True)
            ],
            "covariance_coefficients": [list(map(fw, row)) for row in cc],
            "geometry_comparisons": comparisons,
        }
    assert answer["joint_supported"]["mean_counts"] == [
        fw(q["supported_count"]) for q in population["questions"]
    ]
    return answer


def union_covariance(population, masses):
    inc = [
        sum(p for mask, p in enumerate(masses) if mask & subset == subset)
        for subset in range(len(masses))
    ]
    rows = [
        [r["eligible_mask"] for r in q["chains"] if fraction(r["inclusion"]) > 0]
        for q in population["questions"]
    ]
    return [
        [
            fw(sum((inc[a | b] / (inc[a] * inc[b]) - 1 for a in left for b in right), F(0)))
            for right in rows
        ]
        for left in rows
    ]


def wrong_past(full, kept):
    edges = {
        (a, b) for b, row in enumerate(full) for a in row if not any(a in full[c] for c in row)
    }
    relation = {(a, b) for a, b in edges if a in kept and b in kept}
    for middle in kept:
        relation |= {
            (a, b)
            for a in kept
            for b in kept
            if (a, middle) in relation and (middle, b) in relation
        }
    return [[i for i, a in enumerate(kept) if (a, b) in relation] for b in kept]


def independent_case(name, design_name):
    source, design = independent_source(name), independent_design(design_name)
    pop = independent_population(source, design)
    samples = []
    first, probability = None, F(0)
    for mask in range(64):
        p = make_packet(source, design, mask)
        a = independent_analysis(p)
        samples.append({"problem": p, "analysis": a})
        if not a["possible"]:
            continue
        kept = p["record"]["kept"]
        wrong = wrong_past(source["past"], kept)
        failed = [
            q["name"]
            for q in source["probes"]
            if (kept.index(q["source"]) in wrong[kept.index(q["target"])])
            != (kept.index(q["source"]) in p["record"]["past"][kept.index(q["target"])])
        ]
        if failed:
            probability += fraction(a["probability"])
            if first is None:
                bad = replaced(p, ("record", "past"), wrong)
                first = {
                    "mask": mask,
                    "kept": copy.deepcopy(kept),
                    "past": wrong,
                    "failed_probes": failed,
                    "analysis": independent_analysis(bad),
                }
    all_moments = independent_moments(pop, samples)
    formula = union_covariance(pop, list(map(fraction, design["mask_probabilities"])))
    assert formula == all_moments["joint_supported"]["covariance_counts"]
    return {
        "case_id": name + "__" + design_name,
        "source": source,
        "design": design,
        "population": pop,
        "samples": samples,
        "moments": all_moments,
        "joint_covariance_formula": formula,
        "hasse_control": {"mismatch_probability": fw(probability), "first_mismatch": first},
        "counts": {
            "events": len(source["past"]),
            "eligible_events": 6,
            "mask_rows": 64,
            "positive_rows": sum(s["analysis"]["possible"] for s in samples),
            "questions": len(pop["questions"]),
            "source_chain_terms": sum(q["target_count"] for q in pop["questions"]),
            "observed_chain_terms": sum(
                s["analysis"]["counts"]["observed_chain_terms"] for s in samples
            ),
            "packet_calls": 128,
        },
    }


@pytest.fixture(scope="session")
def expected_cases():
    return [independent_case(name, design) for name, design in SPECIFICATIONS]


@pytest.mark.parametrize("case_index", range(20))
def test_fixed_twenty_complete_source_packet_population_moment_and_wrong_channel_wires(
    executors, runner, expected_cases, case_index
):
    case = expected_cases[case_index]
    assert wire(runner.build_case(*SPECIFICATIONS[case_index])) == wire(case)
    for sample in case["samples"]:
        before = wire(sample["problem"])
        for module in executors:
            assert wire(module.analyze(sample["problem"])) == wire(sample["analysis"])
            assert wire(sample["problem"]) == before
    first = case["hasse_control"]["first_mismatch"]
    if first is not None:
        p = replaced(case["samples"][first["mask"]]["problem"], ("record", "past"), first["past"])
        for module in executors:
            assert wire(module.analyze(p)) == wire(first["analysis"])


def independent_controls(cases):
    lookup = {c["case_id"]: c for c in cases}
    result = {
        k: {"pairs": []} for k in ("boost", "correct_dilation", "wrong_density", "active_warp")
    }
    for design in ("identity", "iid_half"):
        base = lookup["mesh3__" + design]
        boost = lookup["mesh3_boost__" + design]
        assert wire(base["samples"]) == wire(boost["samples"])
        assert wire(base["population"]) == wire(boost["population"])
        assert wire(base["moments"]) == wire(boost["moments"])
        result["boost"]["pairs"].append(
            {
                "design": design,
                "public_samples_equal": True,
                "population_equal": True,
                "moments_equal": True,
            }
        )
        dilate = lookup["mesh3_dilate__" + design]
        assert fraction(dilate["source"]["density"]) == fraction(base["source"]["density"]) / 4
        for left, right in zip(base["samples"], dilate["samples"], strict=True):
            for a, b in zip(
                left["analysis"]["questions"], right["analysis"]["questions"], strict=True
            ):
                assert (
                    a["count_estimates"] == b["count_estimates"]
                    and a["observed_chains"] == b["observed_chains"]
                )
                assert fraction(b["scale"]) == 4 ** a["degree"] * fraction(a["scale"])
                assert b["coefficient_estimates"] == {
                    m: fw(fraction(v) * 4 ** a["degree"])
                    for m, v in a["coefficient_estimates"].items()
                }
        for a, b in zip(
            base["population"]["questions"], dilate["population"]["questions"], strict=True
        ):
            scaled = {
                **a,
                **{
                    k: fw(fraction(a[k]) * 4 ** a["degree"])
                    for k in (
                        "scale",
                        "target_coefficient",
                        "continuum_coefficient",
                        "finite_geometry_error",
                    )
                },
            }
            assert b == scaled
        for a, b in zip(
            base["population"]["interval_geometry"],
            dilate["population"]["interval_geometry"],
            strict=True,
        ):
            assert b == {
                **a,
                **{
                    k: fw(4 * fraction(a[k]))
                    for k in ("tau_squared", "volume", "finite_count_volume", "volume_error")
                },
            }
        for method in METHODS:
            a, b = base["moments"][method], dilate["moments"][method]
            for k in ("mean_counts", "bias_counts", "covariance_counts"):
                assert a[k] == b[k]
            for k in ("mean_coefficients", "bias_coefficients"):
                assert b[k] == [fw(fraction(v) * 4 ** (i % 3)) for i, v in enumerate(a[k])]
            assert b["covariance_coefficients"] == [
                [fw(fraction(v) * 4 ** (i % 3 + j % 3)) for j, v in enumerate(row)]
                for i, row in enumerate(a["covariance_coefficients"])
            ]
            for x, y in zip(a["geometry_comparisons"], b["geometry_comparisons"], strict=True):
                assert y == {
                    **x,
                    **{
                        k: fw(fraction(x[k]) * 4 ** x["degree"])
                        for k in (
                            "continuum",
                            "mean",
                            "sampling_bias",
                            "finite_model_discrepancy",
                            "total_discrepancy",
                        )
                    },
                }
        result["correct_dilation"]["pairs"].append(
            {
                "design": design,
                "count_estimates_equal": True,
                "population_scaling": True,
                "coefficient_packet_scaling": True,
                "complete_moment_congruence": True,
                "squared_length_factor": [4, 1],
            }
        )
        for key, name in (
            ("wrong_density", "mesh3_dilate_wrong_density"),
            ("active_warp", "mesh3_warp"),
        ):
            other = lookup[name + "__" + design]
            assert wire(base["samples"]) == wire(other["samples"])
            i, a, b = next(
                (i, a, b)
                for i, (a, b) in enumerate(
                    zip(
                        base["population"]["interval_geometry"],
                        other["population"]["interval_geometry"],
                        strict=True,
                    )
                )
                if a["volume"] != b["volume"] and (key != "active_warp" or i > 0)
            )
            result[key]["pairs"].append(
                {
                    "design": design,
                    "public_samples_equal": True,
                    "supplied_geometry_differs": True,
                    "witness": {
                        "probe": a["probe"],
                        "probe_index": i,
                        "base_volume": a["volume"],
                        "transformed_volume": b["volume"],
                        "base_error": a["volume_error"],
                        "transformed_error": b["volume_error"],
                    },
                }
            )
    f, s = lookup["ferrers6__identity"], lookup["standard_example3__identity"]
    finite = [q["target_coefficient"] for q in f["population"]["questions"]]
    assert finite == [q["target_coefficient"] for q in s["population"]["questions"]]
    fm, sm = [
        lookup[name + "__iid_half"]["moments"]["joint_supported"]
        for name in ("ferrers6", "standard_example3")
    ]
    assert (
        fm["mean_counts"] == sm["mean_counts"]
        and fm["covariance_counts"] != sm["covariance_counts"]
    )
    result["endpoint_collision"] = {
        "identity_cases": [f["case_id"], s["case_id"]],
        "finite_coefficients": finite,
        "iid_joint_mean_equal": True,
        "iid_joint_covariance_equal": False,
        "ferrers_iid_pair_variance": fm["covariance_counts"][2][2],
        "S3_iid_pair_variance": sm["covariance_counts"][2][2],
        "embedding_reassessed": False,
    }
    f, c = lookup["ferrers6__singleton"], lookup["chain6__singleton"]
    laws = [
        [
            {"problem": x["problem"], "probability": x["analysis"]["probability"]}
            for x in case["samples"]
            if x["analysis"]["possible"]
        ]
        for case in (f, c)
    ]
    assert wire(laws[0]) == wire(laws[1])
    ft, ct = (
        f["population"]["questions"][2]["target_count"],
        c["population"]["questions"][2]["target_count"],
    )
    assert ft != ct
    result["singleton_observation_collision"] = {
        "case_ids": [f["case_id"], c["case_id"]],
        "positive_packets_equal": True,
        "full_pair_targets": {"ferrers6": ft, "chain6": ct},
        "full_pair_targets_differ": True,
        "observation_law_sha256": digest(laws[0]),
    }
    return result


PINS = {
    "d1": (
        "qr-05d-geometric-correspondence-2026-09-05/results.json",
        "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    ),
    "d2": (
        "qr-05d-geometric-correspondence-2026-09-05/results-v2.json",
        "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
    ),
    "e": (
        "qr-05e-sampling-aware-2026-09-06/results.json",
        "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
    ),
}


@pytest.fixture(scope="session")
def pinned():
    answer = {}
    for name, (relative, sha) in PINS.items():
        path = HERE.parent / relative
        assert path.is_file() and not path.is_symlink()
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha
        answer[name] = json.loads(raw)["suite"]
        native(answer[name])
    return answer


def independent_prior_bridges(cases, pinned):
    assert wire(pinned["d1"]) == wire(pinned["d2"])
    ds = {row["analysis"]["case"]: row["analysis"] for row in pinned["d2"]["cases"]}
    es = {
        (row["analysis"]["order_name"], row["analysis"]["design"]): row["analysis"]
        for row in pinned["e"]["cases"]
    }
    lookup = {c["case_id"]: c for c in cases}
    base, d = lookup["mesh3__identity"], ds["mesh3"]
    assert base["source"]["coordinates"] == [[fw(F(x)) for x in row] for row in d["coordinates"]]
    assert [
        [int(i in row) for row in base["source"]["past"]]
        for i in range(len(base["source"]["past"]))
    ] == d["order"]["relation"]
    for i, probe in enumerate(base["source"]["probes"][:3]):
        for q in range(3):
            assert (
                fw(F(d["order"]["kernel_coefficients"][q][probe["source"]][probe["target"]]))
                == base["population"]["questions"][3 * i + q]["target_coefficient"]
            )
    for name in ("ferrers6", "standard_example3"):
        for q in range(3):
            assert lookup[name + "__identity"]["population"]["questions"][q][
                "target_coefficient"
            ] == fw(F(ds[name]["order"]["endpoint"]["coefficients"][q]))
        for design in ("identity", "iid_half"):
            for method in METHODS:
                new, old = (
                    lookup[name + "__" + design]["moments"][method],
                    es[name, design]["moments"][method],
                )
                for k in ("mean_counts", "bias_counts", "mean_coefficients", "bias_coefficients"):
                    assert new[k] == [fw(F(v)) for v in old[k][:3]]
                for k in ("covariance_counts", "covariance_coefficients"):
                    assert new[k] == [[fw(F(v)) for v in row[:3]] for row in old[k][:3]]
    for name in ("ferrers6", "chain6"):
        current, old = lookup[name + "__singleton"], es[name, "singleton"]
        law = [
            {**s["problem"]["record"], "probability": s["analysis"]["probability"]}
            for s in current["samples"]
            if s["analysis"]["possible"]
        ]
        assert law == [
            {**row, "probability": fw(F(row["probability"]))} for row in old["observation_law"]
        ]
        assert (
            current["population"]["questions"][2]["target_count"]
            == old["questions"][2]["target_count"]
        )
    return {
        "D_v1_v2_mathematical_suite_equal": True,
        "D_mesh3_order_coordinates_match": True,
        "D_shared_mesh3_probe_coefficients_checked": 9,
        "D_ferrers_S3_endpoint_coefficients_checked": 6,
        "E_matched_moment_cases": 4,
        "E_matched_q0_q1_q2_vectors_and_matrices": True,
        "E_singleton_observation_laws_preserved": True,
        "E_singleton_pair_targets_preserved": True,
        "E_other_controls_preserved_by_identity": True,
        "prior_forecasting_math_replayed": False,
    }


@pytest.fixture(scope="session")
def expected_suite(expected_cases, pinned):
    counts = {
        "cases": 20,
        **{k: sum(c["counts"][k] for c in expected_cases) for k in expected_cases[0]["counts"]},
    }
    return {
        "cases": expected_cases,
        "controls": independent_controls(expected_cases),
        "prior_bridges": independent_prior_bridges(expected_cases, pinned),
        "public_controls": {
            "ordinary_packet_calls": counts["packet_calls"],
            "wrong_channel_packet_calls": 2
            * sum(c["hasse_control"]["first_mismatch"] is not None for c in expected_cases),
            "independent_route_equal": True,
            "invalid_calls_rejected": 16,
        },
        "totals": counts,
        "scope": dict.fromkeys(
            (
                "unknown_geometry_reconstructed",
                "continuum_limit_established",
                "poisson_ensemble_validated",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
                "unknown_sampling_law_inferred",
            ),
            False,
        ),
    }


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_complete_suite_controls_geometric_decomposition_and_D_E_bridges(
    runner, aggregate, expected_suite
):
    assert wire(aggregate) == wire(expected_suite)
    assert wire(runner.assemble_suite(expected_suite["cases"])) == wire(expected_suite)


def assert_psd(matrix):
    a = [list(map(fraction, row)) for row in matrix]
    assert a == list(map(list, zip(*a, strict=True)))
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0
        if pivot == 0:
            assert all(a[k][j] == 0 for j in range(k + 1, len(a)))
            continue
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                a[i][j] -= a[i][k] * a[k][j] / pivot


def test_fixed_covariance_is_full_centered_PSD_with_cross_probe_signs_and_all_biases_retained(
    expected_cases,
):
    for case in expected_cases:
        for method in METHODS:
            m = case["moments"][method]
            assert_psd(m["covariance_counts"])
            assert_psd(m["covariance_coefficients"])
            for i in range(0, len(m["mean_counts"]), 3):
                assert all(v == [0, 1] for v in m["covariance_counts"][i])
            if m["geometry_comparisons"] is not None:
                for row in m["geometry_comparisons"]:
                    assert fraction(row["sampling_bias"]) + fraction(
                        row["finite_model_discrepancy"]
                    ) == fraction(row["total_discrepancy"])
        assert (
            case["joint_covariance_formula"]
            == case["moments"]["joint_supported"]["covariance_counts"]
        )
        for q, mean, bias in zip(
            case["population"]["questions"],
            case["moments"]["joint_supported"]["mean_counts"],
            case["moments"]["joint_supported"]["bias_counts"],
            strict=True,
        ):
            assert fraction(mean) == q["supported_count"]
            assert fraction(bias) == -len(q["zero_inclusion_chains"])


def test_extreme_admitted_frame_eligible_probe_and_candidate_boundaries(executors):
    past = [list(range(i)) for i in range(12)]
    first = problem_of(255, past=past, fixed=[0, 1, 2, 11])
    fixed = [0, 1, 2, 3, 11]
    probes = [
        {"name": "a" * 40 if i == 0 else f"p{i}", "source": a, "target": b}
        for i, (a, b) in enumerate(list(combinations(fixed, 2))[:8])
    ]
    second = problem_of(127, past=past, fixed=fixed, probes=probes)
    assert independent_analysis(first)["counts"]["inclusion_terms"] == 6561
    assert independent_analysis(second)["counts"]["chain_candidates"] == 632
    for p in (first, second):
        expected = independent_analysis(p)
        for engine in executors:
            assert wire(engine.analyze(p)) == wire(expected)


def test_ninth_eligible_event_rejects_before_inclusion_work(executors, monkeypatch):
    p = problem_of(511, past=[list(range(i)) for i in range(11)])
    assert len(p["eligible"]) == 9 and len(p["mask_probabilities"]) == 512

    def forbidden(*args):
        raise RuntimeError("oversized eligible frame reached arithmetic")

    for engine in executors:
        with monkeypatch.context() as patch:
            for name in HOOKS:
                patch.setattr(engine, name, forbidden)
            with pytest.raises(ValueError):
                engine.analyze(p)


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


def test_complete_packet_output_corruptions_are_nonvacuous_and_rejected(runner, expected_cases):
    # Every packet is independently checked above. Here the private checker is
    # deliberately given an independent expected case, not a self-derived oracle.
    original = expected_cases[5]
    sample = original["samples"][-1]
    p = sample["analysis"]
    changes = [
        replaced(p, ("input_sha256",), "0" * 64),
        replaced(p, ("mask",), p["mask"] + 1),
        add_fraction(p, ("probability",)),
        replaced(p, ("possible",), not p["possible"]),
        add_fraction(p, ("inclusion_probabilities", 0)),
        replaced(p, ("questions", 0, "probe"), "different_probe"),
        replaced(p, ("questions", 0, "degree"), 1),
        add_fraction(p, ("questions", 0, "scale")),
        replaced(p, ("questions", 0, "observed_count"), 2),
        replaced(p, ("questions", 0, "observed_chains", 0, "vertices"), [0]),
        replaced(
            p,
            ("questions", 1, "observed_chains", 0, "eligible_mask"),
            p["questions"][1]["observed_chains"][0]["eligible_mask"] + 1,
        ),
        add_fraction(p, ("questions", 1, "observed_chains", 0, "inclusion")),
        replaced(
            p,
            ("questions", 2, "unsupported_observed_terms"),
            p["questions"][2]["unsupported_observed_terms"] + 1,
        ),
        add_fraction(p, ("questions", 2, "count_estimates", "joint_supported")),
        add_fraction(p, ("questions", 2, "coefficient_estimates", "joint_supported")),
        replaced(p, ("counts", "total_work"), p["counts"]["total_work"] + 1),
        replaced(p, ("scope", "observation_origin_authenticated"), True),
    ]
    assert len(changes) == 17
    original_packet_wire, original_case_wire = wire(p), wire(original)
    for bad in changes:
        assert wire(bad) != original_packet_wire
        candidate = replaced(original, ("samples", 63, "analysis"), bad)
        assert wire(candidate) != original_case_wire
        with pytest.raises(ValueError):
            runner.check_case(candidate, original)
    assert wire(original) == original_case_wire


def test_complete_private_case_corruptions_cannot_hide_targets_covariances_or_geometry(
    runner, expected_cases
):
    original = expected_cases[5]
    q = original["population"]["questions"][2]
    changes = [
        replaced(original, ("case_id",), "unknown__singleton"),
        add_fraction(original, ("source", "coordinates", 1, 0)),
        replaced(original, ("source", "past", 10), original["source"]["past"][10][1:]),
        replaced(original, ("source", "fixed"), original["source"]["fixed"] + [1]),
        add_fraction(original, ("source", "density")),
        add_fraction(original, ("design", "mask_probabilities", 0)),
        replaced(original, ("population", "questions", 2, "target_count"), q["target_count"] + 1),
        replaced(
            original, ("population", "questions", 2, "supported_count"), q["supported_count"] + 1
        ),
        replaced(
            original,
            ("population", "questions", 2, "zero_inclusion_chains"),
            q["zero_inclusion_chains"] + [[]],
        ),
        add_fraction(original, ("population", "interval_geometry", 0, "volume")),
        add_fraction(original, ("moments", "joint_supported", "covariance_counts", 1, 2)),
        add_fraction(
            original,
            ("moments", "joint_supported", "geometry_comparisons", 1, "finite_model_discrepancy"),
        ),
        add_fraction(original, ("joint_covariance_formula", 1, 2)),
        add_fraction(original, ("hasse_control", "mismatch_probability")),
        replaced(original, ("counts", "packet_calls"), original["counts"]["packet_calls"] + 1),
    ]
    assert len(changes) == 15
    before = wire(original)
    for candidate in changes:
        assert wire(candidate) != before
        with pytest.raises(ValueError):
            runner.check_case(candidate, original)
    assert wire(original) == before


def test_complete_suite_corruptions_cannot_overstate_controls_lineage_or_scope(
    runner, expected_suite
):
    original = expected_suite
    changes = [
        replaced(original, ("controls", "endpoint_collision", "iid_joint_covariance_equal"), True),
        add_fraction(
            original, ("controls", "active_warp", "pairs", 0, "witness", "transformed_volume")
        ),
        replaced(original, ("prior_bridges", "D_shared_mesh3_probe_coefficients_checked"), 10),
        replaced(original, ("public_controls", "invalid_calls_rejected"), 17),
        replaced(original, ("totals", "cases"), 21),
        replaced(original, ("scope", "gravity_derived"), True),
        replaced(original, ("cases",), list(reversed(original["cases"]))),
        {**original, "selected_favorable_controls_only": True},
    ]
    assert len(changes) == 8
    before = wire(original)
    for candidate in changes:
        assert wire(candidate) != before
        with pytest.raises(ValueError):
            runner.check_suite(candidate, original)
    assert wire(original) == before
