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


METHODS = ("raw", "uniform_rate", "inclusion")
SCOPE = dict.fromkeys(
    (
        "missing_marks_inferred",
        "source_moments_inferred",
        "geometry_inferred",
        "mark_origin_authenticated",
        "observation_origin_authenticated",
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
    "MAX_MEMBER_CANDIDATES",
    "MAX_ESTIMATOR_TERMS",
    "MAX_TOTAL_WORK",
)
HOOKS = ("_marginals", "_members", "_weight")


def problem_of(mask=3, masses=None, marks=None, past=None, fixed=None, probes=None):
    past = [list(range(i)) for i in range(4)] if past is None else past
    n = len(past)
    fixed = [0, n - 1] if fixed is None else fixed
    eligible = [i for i in range(n) if i not in fixed]
    masses = [F(1, 1 << len(eligible))] * (1 << len(eligible)) if masses is None else masses
    marks = (
        [F(1), F(3)]
        if marks is None and len(eligible) == 2
        else ([F(i + 1) for i in range(len(eligible))] if marks is None else marks)
    )
    probes = [{"name": "whole", "source": 0, "target": n - 1}] if probes is None else probes
    kept = sorted(fixed + [v for j, v in enumerate(eligible) if mask & (1 << j)])
    return {
        "schema_version": "det8-qr05ag-problem-v1",
        "family": "qr05ag_local_volume",
        "frame_size": n,
        "fixed": copy.deepcopy(fixed),
        "eligible": eligible,
        "probes": copy.deepcopy(probes),
        "mask_probabilities": list(map(fw, masses)),
        "record": {
            "kept": kept,
            "past": [[j for j, v in enumerate(kept) if v in past[event]] for event in kept],
            "marks": [
                {"event": event, "volume": fw(marks[j])}
                for j, event in enumerate(eligible)
                if event in kept
            ],
        },
    }


def fixed_internal_problem(mask=3):
    return problem_of(
        mask,
        [F(1, 2), 0, 0, F(1, 2)],
        [2, 5],
        past=[list(range(i)) for i in range(5)],
        fixed=[0, 2, 4],
        probes=[
            {"name": "whole", "source": 0, "target": 4},
            {"name": "left", "source": 0, "target": 2},
            {"name": "right", "source": 2, "target": 4},
        ],
    )


def independent_analysis(p):
    eligible = p["eligible"]
    masses = list(map(fraction, p["mask_probabilities"]))
    pi = [
        sum((mass for mask, mass in enumerate(masses) if mask & (1 << j)), F())
        for j in range(len(eligible))
    ]
    pbar = sum(pi, F()) / len(pi)
    kept, past = p["record"]["kept"], p["record"]["past"]
    rows = dict(zip(kept, ({kept[j] for j in row} for row in past), strict=True))
    mark = {row["event"]: fraction(row["volume"]) for row in p["record"]["marks"]}
    inclusion = dict(zip(eligible, pi, strict=True))
    mask = sum(1 << j for j, v in enumerate(eligible) if v in kept)
    questions = []
    for probe in p["probes"]:
        a, b = probe["source"], probe["target"]
        members = [v for v in eligible if v in mark and a in rows[v] and v in rows[b]]
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": [
                    {"event": v, "volume": fw(mark[v]), "inclusion": fw(inclusion[v])}
                    for v in members
                ],
                "estimates": {
                    "raw": fw(sum((mark[v] for v in members), F())),
                    "uniform_rate": fw(sum((mark[v] / pbar for v in members), F())),
                    "inclusion": fw(sum((mark[v] / inclusion[v] for v in members), F())),
                },
            }
        )
    m, k, pn = len(eligible), len(mark), len(questions)
    l, i, c = 1 << m, m * (1 << (m - 1)), pn * k
    a = sum(len(q["observed_cells"]) for q in questions)
    return {
        "input_sha256": digest(p),
        "mask": mask,
        "probability": fw(masses[mask]),
        "possible": bool(masses[mask]),
        "marginals": list(map(fw, pi)),
        "questions": questions,
        "counts": {
            "events": p["frame_size"],
            "eligible_events": m,
            "kept_events": len(kept),
            "retained_cells": k,
            "mask_rows": l,
            "questions": pn,
            "inclusion_terms": i,
            "member_candidates": c,
            "observed_member_terms": a,
            "estimator_terms": 3 * a,
            "reserved_estimator_terms": 3 * c,
            "reserved_total_work": l + i + 4 * c + 3 * pn,
            "total_work": l + i + c + 3 * a + 3 * pn,
        },
        "scope": dict(SCOPE),
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ag_test_primary", "volume.py"),
        private_module("_qr05ag_test_reference", "reference_qr05ag.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ag_test_runner", "study.py")


GENERIC_LAWS = (
    [F(1, 4)] * 4,
    [F(1, 2), 0, 0, F(1, 2)],
    [0, F(1, 2), F(1, 2), 0],
    [F(2, 9), F(1, 9), F(4, 9), F(2, 9)],
)


@pytest.mark.parametrize("masses", GENERIC_LAWS)
@pytest.mark.parametrize("mask", range(4))
def test_generic_full_wire_original_ID_membership_mark_and_marginal_oracle(executors, masses, mask):
    p = problem_of(mask, masses)
    before = wire(p)
    for module in executors:
        assert wire(module.analyze(p)) == wire(independent_analysis(p))
        assert wire(p) == before


def test_empty_mark_rows_fixed_internal_markers_and_zero_probability_records(executors):
    for mask in range(4):
        p = fixed_internal_problem(mask)
        expected = independent_analysis(p)
        assert all(
            v["event"] not in p["fixed"] for q in expected["questions"] for v in q["observed_cells"]
        )
        if mask == 0:
            assert p["record"]["marks"] == []
            assert all(
                all(v == [0, 1] for v in q["estimates"].values()) for q in expected["questions"]
            )
        for module in executors:
            assert wire(module.analyze(p)) == wire(expected)
    impossible = problem_of(0, [0, 0, 0, 1])
    for module in executors:
        a = module.analyze(impossible)
        assert (
            not a["possible"] and a["probability"] == [0, 1] and a["counts"]["retained_cells"] == 0
        )


def test_noncausal_and_incomparable_boundaries_do_not_create_membership(executors):
    p = problem_of(past=[[], [], [], []])
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independent_analysis(p))
        assert a["questions"][0]["observed_cells"] == [] and a["questions"][0]["estimates"][
            "inclusion"
        ] == [0, 1]


def test_valid_stale_marks_and_wrong_origin_orders_are_not_repaired(executors):
    p = problem_of()
    stale = replaced(p, ("record", "marks", 0, "volume"), [7, 2])
    wrong = replaced(p, ("record", "past"), [[], [], [], []])
    for module in executors:
        for value in (p, stale, wrong):
            a = module.analyze(value)
            assert wire(a) == wire(independent_analysis(value)) and a["scope"] == SCOPE
        assert module.analyze(p)["questions"] != module.analyze(stale)["questions"]
        assert module.analyze(wrong)["questions"][0]["observed_cells"] == []


def test_missing_marks_are_not_available_via_hidden_files_or_mutable_context(
    executors, monkeypatch
):
    p = problem_of(1, marks=[1, 3])
    other_hidden_source = problem_of(1, marks=[1, 300])
    assert wire(p) == wire(other_hidden_source)
    expected = wire(independent_analysis(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("observer tried to read hidden source information")

    with monkeypatch.context() as patch:
        for host, name in (
            (builtins, "open"),
            (os, "open"),
            (Path, "open"),
            (Path, "read_bytes"),
            (Path, "read_text"),
        ):
            patch.setattr(host, name, forbidden)
        for module in executors:
            assert wire(module.analyze(p)) == expected
            assert wire(module.analyze(other_hidden_source)) == expected


def design_moments(analyses, masses, method):
    vectors = [[fraction(q["estimates"][method]) for q in a["questions"]] for a in analyses]
    qn = len(vectors[0])
    mean = [sum((p * v[i] for p, v in zip(masses, vectors, strict=True)), F()) for i in range(qn)]
    covariance = [
        [
            sum(
                (
                    p * (v[i] - mean[i]) * (v[j] - mean[j])
                    for p, v in zip(masses, vectors, strict=True)
                ),
                F(),
            )
            for j in range(qn)
        ]
        for i in range(qn)
    ]
    second = [
        [
            sum((p * v[i] * v[j] for p, v in zip(masses, vectors, strict=True)), F())
            - mean[i] * mean[j]
            for j in range(qn)
        ]
        for i in range(qn)
    ]
    assert covariance == second
    return mean, covariance


def test_singleton_correction_supports_linear_mean_despite_zero_pairs_and_signed_covariance(
    executors,
):
    masses = [F(0), F(1, 2), F(1, 2), F(0)]
    for marks, variance in (([1, 3], 4), ([2, 2], 0)):
        for module in executors:
            records = [module.analyze(problem_of(mask, masses, marks)) for mask in range(4)]
            mean, cov = design_moments(records, masses, "inclusion")
            assert mean == [sum(marks)] and cov == [[variance]]
    rich = [fixed_internal_problem(mask) for mask in range(4)]
    for p in rich:
        p["mask_probabilities"] = list(map(fw, masses))
    for module in executors:
        mean, cov = design_moments([module.analyze(p) for p in rich], masses, "inclusion")
        assert mean == [7, 2, 5]
        assert cov == [[9, -6, 15], [-6, 4, -10], [15, -10, 25]]
        # Zero joint inclusion, not its reciprocal, produces the -10 entry.
        assert F(2) * 5 * (F(0) / (F(1, 2) * F(1, 2)) - 1) == cov[1][2]


def test_correlated_and_uneven_designs_use_individual_not_joint_or_uniform_weights(executors):
    for masses in GENERIC_LAWS:
        for module in executors:
            analyses = [module.analyze(problem_of(mask, masses)) for mask in range(4)]
            mean, _ = design_moments(analyses, masses, "inclusion")
            assert mean == [4]
    masses = GENERIC_LAWS[-1]
    for module in executors:
        records = [module.analyze(problem_of(mask, masses)) for mask in range(4)]
        assert design_moments(records, masses, "uniform_rate")[0] == [F(14, 3)]


def test_unretained_inverse_and_products_can_cancel_but_retained_estimates_cannot_overflow(
    executors,
):
    tiny = F(1, 1 << 4095)
    cancelled = problem_of(3, [1 - 2 * tiny, 0, tiny, tiny], marks=[tiny, tiny])
    for module in executors:
        a = module.analyze(cancelled)
        assert wire(a) == wire(independent_analysis(cancelled))
        assert a["questions"][0]["estimates"]["inclusion"] == [3, 2]
        assert a["questions"][0]["estimates"]["uniform_rate"] == [4, 3]
        with pytest.raises(ValueError):
            module.analyze(problem_of(3, [1 - tiny, 0, 0, tiny], marks=[1, 1]))
        huge = F(1 << 4095)
        with pytest.raises(ValueError):
            module.analyze(problem_of(marks=[huge, huge]))


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
    bad += [replaced(p, ("frame_size",), v) for v in (True, 4.0, IntChild(4), "4", 2, 13)]
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
    for path in (("record", "marks", 0, "volume"), ("mask_probabilities", 0)):
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
    bad += [replaced(p, ("record", "marks", 0, "volume"), v) for v in ([0, 1], [-1, 1])]
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
    bad += [
        replaced(p, ("record", "marks"), v)
        for v in (
            None,
            (),
            ListChild(p["record"]["marks"]),
            [],
            p["record"]["marks"][::-1],
            p["record"]["marks"][:1],
            p["record"]["marks"] * 2,
        )
    ]
    first = p["record"]["marks"][0]
    bad += [
        replaced(p, ("record", "marks", 0), v)
        for v in (
            None,
            [],
            DictChild(first),
            {"event": 1},
            {"volume": [1, 1]},
            {**first, "geometry": [1, 1]},
            {**first, "true_volume": [1, 1]},
        )
    ]
    bad += [
        replaced(p, ("record", "marks", 0, "event"), v)
        for v in (None, False, 1.0, IntChild(1), "1", -1, 0, 2, 3, 4)
    ]
    bad += [
        {**p, key: []}
        for key in ("density", "missing_marks", "cell_bounds", "true_marks", "moments")
    ]
    partial = problem_of(1)
    bad.append(replaced(partial, ("record", "marks"), p["record"]["marks"]))
    bad.append(replaced(problem_of(0), ("record", "marks"), [first]))
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_schema_retained_mark_alignment_leakage_normalization_and_native_types(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def planned_caps(p):
    m, k, pn = len(p["eligible"]), len(p["record"]["marks"]), len(p["probes"])
    l, i, c = 1 << m, m * (1 << (m - 1)), pn * k
    return {
        "MAX_EVENTS": p["frame_size"],
        "MAX_ELIGIBLE": m,
        "MAX_PROBES": pn,
        "MAX_INCLUSION_TERMS": i,
        "MAX_MEMBER_CANDIDATES": c,
        "MAX_ESTIMATOR_TERMS": 3 * c,
        "MAX_TOTAL_WORK": l + i + 4 * c + 3 * pn,
    }


def test_complete_schema_reservation_and_positive_marginal_staging_precede_hooks(
    executors, monkeypatch
):
    p = fixed_internal_problem()
    expected = independent_analysis(p)
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as patch:
            for name in HOOKS:
                original = getattr(module, name)

                def counted(*args, _name=name, _original=original, _calls=calls):
                    _calls[_name] += 1
                    return _original(*args)

                patch.setattr(module, name, counted)
            assert wire(module.analyze(p)) == wire(expected)
        assert calls == {"_marginals": 1, "_members": 3, "_weight": 12}

        def forbidden(*args):
            raise RuntimeError("arithmetic reached before full validation and reservation")

        for constant, limit in planned_caps(p).items():
            with monkeypatch.context() as patch:
                for name in HOOKS:
                    patch.setattr(module, name, forbidden)
                patch.setattr(module, constant, limit - 1)
                with pytest.raises(ValueError):
                    module.analyze(p)
        late_bad = [
            replaced(p, ("record", "past", 4), [2, 3]),
            replaced(p, ("record", "marks", 1, "volume"), [0, 1]),
            replaced(p, ("record", "marks", 1, "event"), 4),
        ]
        for bad in late_bad:
            with monkeypatch.context() as patch:
                for name in HOOKS:
                    patch.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(bad)
        with monkeypatch.context() as patch:
            for name in ("_members", "_weight"):
                patch.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(problem_of(3, [1, 0, 0, 0]))


@pytest.mark.parametrize("constant", CAPS)
def test_all_eleven_live_caps_restore_without_cached_admission(executors, monkeypatch, constant):
    p = fixed_internal_problem()
    before = wire(independent_analysis(p))
    for module in executors:
        with monkeypatch.context() as patch:
            patch.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == before


def test_extreme_valid_eligible_and_probe_boundaries_and_preallocation_rejection(
    executors, monkeypatch
):
    past = [list(range(i)) for i in range(12)]
    p8 = problem_of(255, past=past, fixed=[0, 1, 2, 11])
    fixed = [0, 1, 2, 3, 11]
    probes = [
        {"name": "a" * 40 if i == 0 else f"p{i}", "source": a, "target": b}
        for i, (a, b) in enumerate(list(combinations(fixed, 2))[:8])
    ]
    q8 = problem_of(127, past=past, fixed=fixed, probes=probes)
    assert independent_analysis(p8)["counts"]["inclusion_terms"] == 1024
    assert independent_analysis(q8)["counts"]["member_candidates"] == 56
    for module in executors:
        for p in (p8, q8):
            assert wire(module.analyze(p)) == wire(independent_analysis(p))

        def forbidden(*args):
            raise RuntimeError("ninth eligible event reached hooks")

        with monkeypatch.context() as patch:
            for name in HOOKS:
                patch.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(problem_of(511, past=[list(range(i)) for i in range(11)]))


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
        left["questions"][0]["estimates"]["raw"][0] = -1
        left["marginals"][0][0] = 2
        assert wire(p) == before and wire(right) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["record"]["marks"][0]["volume"] = [2, 1]
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
        ("record", "marks"),
        ("mask_probabilities",),
        ("mask_probabilities", 0, 1),
        ("record",),
        ("record", "kept"),
        ("record", "past"),
        ("record", "past", 3),
        ("record", "marks", 0),
        ("record", "marks", 0, "volume"),
    ):
        yield replaced(p, path, dag)


def test_generic_auditor_complete_wire_preserves_observer_limits_and_zero_rows():
    audit = private_module("_qr05ag_test_generic_audit", "audit_json.py")
    for p in (
        problem_of(),
        fixed_internal_problem(0),
        problem_of(0, [0, 0, 0, 1]),
        problem_of(3, [0, F(1, 2), F(1, 2), 0]),
    ):
        assert wire(audit.expected_packet(p)) == wire(independent_analysis(p))


DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2", "singleton")
SPECIFICATIONS = [(name, design) for name in ("grid", "warp") for design in DESIGNS] + [
    (name, design)
    for name in ("warp_stale", "boost", "dilate")
    for design in ("identity", "iid_half")
]


def independent_source(name):
    markers = {
        "bottom": (F(0), F(0)),
        "aligned": (F(2, 3), F(1, 2)),
        "unaligned": (F(3, 5), F(2, 5)),
        "top": (F(1), F(1)),
    }
    rectangles = {
        f"c_{i}_{j}": (F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2))
        for i in range(3)
        for j in range(2)
    }
    base = dict(markers)
    for label, (ul, uh, vl, vh) in rectangles.items():
        base[label] = ((ul + uh) / 2, (vl + vh) / 2)
    labels = sorted(base, key=lambda label: (sum(base[label]), *base[label], label))
    ids = {label: i for i, label in enumerate(labels)}

    def transform(u, v):
        if name in ("warp", "warp_stale"):
            return u * u, v * v
        if name == "boost":
            return 2 * u, v / 2
        if name == "dilate":
            return 2 * u, 2 * v
        assert name == "grid"
        return u, v

    coords = [transform(*base[label]) for label in labels]
    past = [[i for i, (u, v) in enumerate(coords) if u < x and v < y] for x, y in coords]
    # IDs are assigned once before transforming, and a strict causal pair must
    # still have increasing original IDs; incomparable points are not relabelled.
    assert all(all(i < j for i in row) for j, row in enumerate(past))
    cells = []
    for label in sorted(rectangles, key=ids.__getitem__):
        ul, uh, vl, vh = rectangles[label]
        a, c = transform(ul, vl)
        b, d = transform(uh, vh)
        geometric = (b - a) * (d - c) / 2
        supplied = (uh - ul) * (vh - vl) / 2 if name == "warp_stale" else geometric
        cells.append(
            {
                "event": ids[label],
                "bounds": list(map(fw, (a, b, c, d))),
                "geometric_mark": fw(geometric),
                "supplied_mark": fw(supplied),
            }
        )
    probes = [
        {"name": q, "source": ids[a], "target": ids[b]}
        for q, a, b in (
            ("whole", "bottom", "top"),
            ("lower_aligned", "bottom", "aligned"),
            ("upper_aligned", "aligned", "top"),
            ("lower_unaligned", "bottom", "unaligned"),
            ("upper_unaligned", "unaligned", "top"),
        )
    ]
    return {
        "name": name,
        "coordinates": [list(map(fw, p)) for p in coords],
        "past": past,
        "fixed": sorted(ids[x] for x in markers),
        "eligible": [c["event"] for c in cells],
        "probes": probes,
        "cells": cells,
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def independent_design(name):
    masses = []
    for mask in range(64):
        if name == "identity":
            value = F(int(mask == 63))
        elif name == "iid_half":
            value = F(1, 64)
        elif name == "heterogeneous":
            value = F(1)
            for j in range(6):
                rate = F(1 + j % 2, 3)
                value *= rate if mask & (1 << j) else 1 - rate
        elif name == "all_or_none":
            value = F(1, 2) if mask in (0, 63) else F()
        elif name == "fixed_size2":
            value = F(1, 15) if mask.bit_count() == 2 else F()
        else:
            assert name == "singleton"
            value = F(1, 6) if mask.bit_count() == 1 else F()
        masses.append(value)
    assert sum(masses, F()) == 1
    return {"name": name, "mask_probabilities": list(map(fw, masses))}


def independent_packet(source, design, mask):
    return problem_of(
        mask,
        masses=list(map(fraction, design["mask_probabilities"])),
        marks=[fraction(c["supplied_mark"]) for c in source["cells"]],
        past=source["past"],
        fixed=source["fixed"],
        probes=source["probes"],
    )


def overlap_length(a, b, c, d):
    # Independent partition-by-endpoints route instead of directly clipping
    # a single interval with min/max endpoints.
    points = sorted({a, b, c, d})
    length = F()
    for left, right in pairwise(points):
        mid = (left + right) / 2
        if a < mid < b and c < mid < d:
            length += right - left
    return length


def independent_population(source):
    coords = [tuple(map(fraction, p)) for p in source["coordinates"]]
    result = []
    for probe in source["probes"]:
        a, b = probe["source"], probe["target"]
        au, av = coords[a]
        bu, bv = coords[b]
        members = [
            c["event"]
            for c in source["cells"]
            if au < coords[c["event"]][0] < bu and av < coords[c["event"]][1] < bv
        ]
        assert members == [
            i for i in source["eligible"] if a in source["past"][i] and i in source["past"][b]
        ]
        supplied = sum(
            (fraction(c["supplied_mark"]) for c in source["cells"] if c["event"] in members), F()
        )
        geometric = sum(
            (fraction(c["geometric_mark"]) for c in source["cells"] if c["event"] in members), F()
        )
        continuum = (bu - au) * (bv - av) / 2
        overlaps = []
        for c in source["cells"]:
            ul, uh, vl, vh = map(fraction, c["bounds"])
            value = overlap_length(ul, uh, au, bu) * overlap_length(vl, vh, av, bv) / 2
            overlaps.append({"event": c["event"], "volume": fw(value)})
        assert sum((fraction(c["volume"]) for c in overlaps), F()) == continuum
        result.append(
            {
                "probe": probe["name"],
                "members": members,
                "supplied_target": fw(supplied),
                "geometric_target": fw(geometric),
                "continuum_volume": fw(continuum),
                "annotation_error": fw(supplied - geometric),
                "quadrature_error": fw(geometric - continuum),
                "overlaps": overlaps,
            }
        )
    return result


def independent_moments(population, samples, masses):
    result = {}
    for method in METHODS:
        mean, cov = design_moments([x["analysis"] for x in samples], masses, method)
        bias, rows = [], []
        for q, average in zip(population, mean, strict=True):
            t, g, v = map(
                fraction, (q["supplied_target"], q["geometric_target"], q["continuum_volume"])
            )
            components = (average - t, t - g, g - v)
            assert sum(components, F()) == average - v
            bias.append(fw(components[0]))
            rows.append(
                {
                    "probe": q["probe"],
                    "mean": fw(average),
                    "finite_target": fw(t),
                    "true_finite_target": fw(g),
                    "continuum": fw(v),
                    "sampling_bias": fw(components[0]),
                    "annotation_error": fw(components[1]),
                    "quadrature_error": fw(components[2]),
                    "total_error": fw(average - v),
                }
            )
        result[method] = {
            "mean": list(map(fw, mean)),
            "bias": bias,
            "covariance": [list(map(fw, row)) for row in cov],
            "decompositions": rows,
        }
    return result


def independent_covariance(source, population, masses):
    cells = source["cells"]
    n = len(cells)
    pi = [sum((p for mask, p in enumerate(masses) if mask & (1 << i)), F()) for i in range(n)]
    pair = [
        [
            sum((p for mask, p in enumerate(masses) if mask & (1 << i) and mask & (1 << j)), F())
            for j in range(n)
        ]
        for i in range(n)
    ]
    kernel = [
        [
            fraction(cells[i]["supplied_mark"])
            * fraction(cells[j]["supplied_mark"])
            * (pair[i][j] / (pi[i] * pi[j]) - 1)
            for j in range(n)
        ]
        for i in range(n)
    ]
    memberships = [
        [i for i, c in enumerate(cells) if c["event"] in q["members"]] for q in population
    ]
    matrix = [
        [fw(sum((kernel[i][j] for i in left for j in right), F())) for right in memberships]
        for left in memberships
    ]
    pairs = sum(len(left) * len(right) for left in memberships for right in memberships)
    zeros = sum(
        pair[i][j] == 0
        for left in memberships
        for right in memberships
        for i in left
        for j in right
    )
    return matrix, pairs, zeros


def independent_case(name, design_name):
    source, design = independent_source(name), independent_design(design_name)
    population = independent_population(source)
    samples = []
    for mask in range(64):
        p = independent_packet(source, design, mask)
        samples.append({"problem": p, "analysis": independent_analysis(p)})
    masses = list(map(fraction, design["mask_probabilities"]))
    moments = independent_moments(population, samples, masses)
    cov, pairs, zeros = independent_covariance(source, population, masses)
    assert cov == moments["inclusion"]["covariance"]
    assert moments["inclusion"]["mean"] == [q["supplied_target"] for q in population]
    return {
        "case_id": name + "__" + design_name,
        "source": source,
        "design": design,
        "population": population,
        "samples": samples,
        "moments": moments,
        "joint_covariance": cov,
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(x["analysis"]["possible"] for x in samples),
            "questions": len(population),
            "source_member_terms": sum(len(q["members"]) for q in population),
            "observed_member_terms": sum(
                x["analysis"]["counts"]["observed_member_terms"] for x in samples
            ),
            "ordered_cell_pairs": pairs,
            "zero_joint_pairs": zeros,
            "packet_calls": 2 * len(samples),
        },
    }


@pytest.fixture(scope="session")
def expected_cases():
    return [independent_case(name, design) for name, design in SPECIFICATIONS]


@pytest.mark.parametrize("index", range(18))
def test_fixed_all_eighteen_complete_source_cell_packet_target_and_moment_wires(
    index, expected_cases, runner, executors
):
    name, design = SPECIFICATIONS[index]
    expected = expected_cases[index]
    assert wire(runner.build_case(name, design)) == wire(expected)
    for sample in expected["samples"]:
        before = wire(sample["problem"])
        for module in executors:
            assert wire(module.analyze(sample["problem"])) == wire(sample["analysis"])
            assert wire(sample["problem"]) == before


def positive_law(case):
    return [
        {"problem": x["problem"], "probability": x["analysis"]["probability"]}
        for x in case["samples"]
        if x["analysis"]["possible"]
    ]


def field_vector(case, key):
    return [q[key] for q in case["population"]]


def scaled_population(population, factor):
    answer = copy.deepcopy(population)
    for q in answer:
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            q[key] = fw(fraction(q[key]) * factor)
        for row in q["overlaps"]:
            row["volume"] = fw(fraction(row["volume"]) * factor)
    return answer


def scaled_moments(moments, factor):
    answer = copy.deepcopy(moments)
    for method in METHODS:
        for key in ("mean", "bias"):
            answer[method][key] = [fw(fraction(v) * factor) for v in answer[method][key]]
        answer[method]["covariance"] = [
            [fw(fraction(v) * factor * factor) for v in row] for row in answer[method]["covariance"]
        ]
        for row in answer[method]["decompositions"]:
            for key in row:
                if key != "probe":
                    row[key] = fw(fraction(row[key]) * factor)
    return answer


def independent_controls(cases):
    by = {c["case_id"]: c for c in cases}
    result = {
        key: [] for key in ("warp", "stale_marks", "boost", "dilation", "boundaries", "sampling")
    }
    for design in DESIGNS:
        a, b = by["grid__" + design], by["warp__" + design]
        unmarked = []
        for case in (a, b):
            records = []
            for sample in case["samples"]:
                packet = copy.deepcopy(sample["problem"])
                del packet["record"]["marks"]
                records.append(packet)
            unmarked.append(records)
        result["warp"].append(
            {
                "design": design,
                "unmarked_packets_equal": wire(unmarked[0]) == wire(unmarked[1]),
                "marked_positive_laws_equal": wire(positive_law(a)) == wire(positive_law(b)),
                "base_targets": field_vector(a, "supplied_target"),
                "warped_targets": field_vector(b, "supplied_target"),
                "base_volumes": field_vector(a, "continuum_volume"),
                "warped_volumes": field_vector(b, "continuum_volume"),
            }
        )
    for design in ("identity", "iid_half"):
        a, b, c = (by[name + "__" + design] for name in ("grid", "warp", "warp_stale"))
        result["stale_marks"].append(
            {
                "design": design,
                "packets_equal_base": wire(a["samples"]) == wire(c["samples"]),
                "geometric_targets_equal_warp": field_vector(b, "geometric_target")
                == field_vector(c, "geometric_target"),
                "supplied_targets": field_vector(c, "supplied_target"),
                "geometric_targets": field_vector(c, "geometric_target"),
                "annotation_errors": field_vector(c, "annotation_error"),
            }
        )
        for name, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
            t = by[name + "__" + design]
            packet_equal = True
            for left, right in zip(a["samples"], t["samples"], strict=True):
                for lq, rq in zip(
                    left["analysis"]["questions"], right["analysis"]["questions"], strict=True
                ):
                    packet_equal &= all(
                        fraction(rq["estimates"][m]) == factor * fraction(lq["estimates"][m])
                        for m in METHODS
                    )
                    assert [x["event"] for x in lq["observed_cells"]] == [
                        x["event"] for x in rq["observed_cells"]
                    ]
                    for lc, rc in zip(lq["observed_cells"], rq["observed_cells"], strict=True):
                        assert lc["inclusion"] == rc["inclusion"] and factor * fraction(
                            lc["volume"]
                        ) == fraction(rc["volume"])
            result[key].append(
                {
                    "design": design,
                    "order_equal": a["source"]["past"] == t["source"]["past"],
                    "packet_estimate_scaling": packet_equal,
                    "moment_scaling": wire(scaled_moments(a["moments"], factor))
                    == wire(t["moments"]),
                    "population_scaling": wire(scaled_population(a["population"], factor))
                    == wire(t["population"]),
                    "volume_factor": fw(factor),
                }
            )
    for name in ("grid", "warp", "warp_stale", "boost", "dilate"):
        c = by[name + "__identity"]
        result["boundaries"].append(
            {
                "source": name,
                "overlaps_sum_to_volume": all(
                    sum((fraction(x["volume"]) for x in q["overlaps"]), F())
                    == fraction(q["continuum_volume"])
                    for q in c["population"]
                ),
                "aligned_geometric_exact": all(
                    q["geometric_target"] == q["continuum_volume"] for q in c["population"][:3]
                ),
                "unaligned_quadrature_errors": field_vector(c, "quadrature_error")[3:],
            }
        )
    for name in ("grid", "warp"):
        for design in DESIGNS:
            c = by[name + "__" + design]
            result["sampling"].append(
                {
                    "case_id": c["case_id"],
                    "inclusion_unbiased": all(
                        v == [0, 1] for v in c["moments"]["inclusion"]["bias"]
                    ),
                    "uniform_bias": c["moments"]["uniform_rate"]["bias"],
                    "raw_bias": c["moments"]["raw"]["bias"],
                    "covariance_formula_equal": wire(c["moments"]["inclusion"]["covariance"])
                    == wire(c["joint_covariance"]),
                }
            )
    return result


@pytest.fixture(scope="session")
def expected_suite(expected_cases):
    totals = {
        "cases": len(expected_cases),
        **{k: sum(c["counts"][k] for c in expected_cases) for k in expected_cases[0]["counts"]},
    }
    return {
        "cases": expected_cases,
        "controls": independent_controls(expected_cases),
        "public_controls": {
            "ordinary_packet_calls": totals["packet_calls"],
            "independent_route_equal": True,
            "invalid_calls_rejected": 16,
        },
        "totals": totals,
        "scope": dict.fromkeys(
            (
                "unknown_geometry_reconstructed",
                "annotations_proved_necessary_or_minimal",
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


def test_fixed_complete_suite_controls_preserve_mark_information_and_all_three_errors(
    runner, expected_suite
):
    assert wire(runner.run_suite()) == wire(expected_suite)
    assert wire(runner.assemble_suite(expected_suite["cases"])) == wire(expected_suite)


def assert_psd(matrix):
    a = [list(map(fraction, row)) for row in matrix]
    assert a == list(map(list, zip(*a, strict=True)))
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot >= 0
        if pivot == 0:
            assert all(a[k][j] == 0 for j in range(k + 1, len(a)))
        else:
            for i in range(k + 1, len(a)):
                for j in range(k + 1, len(a)):
                    a[i][j] -= a[i][k] * a[k][j] / pivot


def test_fixed_full_covariance_and_three_error_terms_never_replace_one_another(expected_cases):
    for case in expected_cases:
        for method in METHODS:
            assert_psd(case["moments"][method]["covariance"])
            for row in case["moments"][method]["decompositions"]:
                assert sum(
                    (
                        fraction(row[k])
                        for k in ("sampling_bias", "annotation_error", "quadrature_error")
                    ),
                    F(),
                ) == fraction(row["total_error"])
        if case["design"]["name"] == "singleton":
            assert case["counts"]["zero_joint_pairs"] > 0
            assert all(x == [0, 1] for x in case["moments"]["inclusion"]["bias"])
            assert any(fraction(x) < 0 for row in case["joint_covariance"] for x in row)


def test_representative_on_fixed_probe_boundary_is_not_split_or_assigned_a_fraction(executors):
    p = problem_of(
        1,
        marks=[F(1, 2)],
        past=[[], [0], [0], [0, 1, 2]],
        fixed=[0, 2, 3],
        probes=[
            {"name": "whole", "source": 0, "target": 3},
            {"name": "lower", "source": 0, "target": 2},
            {"name": "upper", "source": 2, "target": 3},
        ],
    )
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independent_analysis(p))
        assert [q["estimates"]["raw"] for q in a["questions"]] == [[1, 2], [0, 1], [0, 1]]
        assert a["questions"][1]["observed_cells"] == a["questions"][2]["observed_cells"] == []


def test_generic_straddling_cell_quadrature_is_separate_from_mark_and_sampling_error(runner):
    source = {
        "name": "synthetic",
        "coordinates": [
            list(map(fw, c))
            for c in ((0, 0), (F(1, 4), F(1, 4)), (F(1, 2), F(1, 2)), (F(3, 4), F(3, 4)), (1, 1))
        ],
        "past": [list(range(i)) for i in range(5)],
        "fixed": [0, 2, 4],
        "eligible": [1, 3],
        "probes": fixed_internal_problem()["probes"],
        "cells": [
            {
                "event": 1,
                "bounds": list(map(fw, (0, F(1, 2), 0, 1))),
                "geometric_mark": [1, 4],
                "supplied_mark": [1, 3],
            },
            {
                "event": 3,
                "bounds": list(map(fw, (F(1, 2), 1, 0, 1))),
                "geometric_mark": [1, 4],
                "supplied_mark": [1, 4],
            },
        ],
        "mark_kind": "synthetic_stale",
    }
    expected = independent_population(source)
    assert wire(runner.population(source)) == wire(expected)
    assert expected[1]["supplied_target"] == [1, 3] and expected[1]["geometric_target"] == [1, 4]
    assert expected[1]["continuum_volume"] == [1, 8]
    assert expected[1]["annotation_error"] == [1, 12] and expected[1]["quadrature_error"] == [1, 8]
    assert expected[1]["overlaps"] == [
        {"event": 1, "volume": [1, 8]},
        {"event": 3, "volume": [0, 1]},
    ]


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


def test_fixed_complete_packet_corruptions_are_nonvacuous_and_rejected(runner, expected_cases):
    original = expected_cases[6]
    p = original["samples"][-1]["analysis"]
    changes = [
        replaced(p, ("input_sha256",), "0" * 64),
        replaced(p, ("mask",), p["mask"] + 1),
        add_fraction(p, ("probability",)),
        replaced(p, ("possible",), not p["possible"]),
        add_fraction(p, ("marginals", 0)),
        replaced(p, ("questions", 0, "probe"), "different"),
        replaced(p, ("questions", 0, "observed_cells"), p["questions"][0]["observed_cells"][:-1]),
        replaced(p, ("questions", 0, "observed_cells", 0, "event"), 0),
        add_fraction(p, ("questions", 0, "observed_cells", 0, "volume")),
        add_fraction(p, ("questions", 0, "observed_cells", 0, "inclusion")),
        *(add_fraction(p, ("questions", 0, "estimates", method)) for method in METHODS),
        replaced(p, ("counts", "retained_cells"), p["counts"]["retained_cells"] + 1),
        replaced(p, ("counts", "reserved_total_work"), p["counts"]["reserved_total_work"] + 1),
        replaced(p, ("scope", "mark_origin_authenticated"), True),
    ]
    assert len(changes) == 16
    before, packet_before = wire(original), wire(p)
    for bad in changes:
        assert wire(bad) != packet_before
        candidate = replaced(original, ("samples", 63, "analysis"), bad)
        assert wire(candidate) != before
        with pytest.raises(ValueError):
            runner.check_case(candidate, original)
    assert wire(original) == before


def test_fixed_complete_case_corruptions_cannot_hide_marks_boundaries_covariance_or_bias(
    runner, expected_cases
):
    original = expected_cases[12]
    changes = [
        replaced(original, ("case_id",), "other__identity"),
        add_fraction(original, ("source", "coordinates", 1, 0)),
        add_fraction(original, ("source", "cells", 0, "bounds", 1)),
        add_fraction(original, ("source", "cells", 0, "geometric_mark")),
        add_fraction(original, ("source", "cells", 0, "supplied_mark")),
        replaced(original, ("source", "mark_kind"), "geometric_cell_volume"),
        add_fraction(original, ("design", "mask_probabilities", 0)),
        replaced(original, ("population", 0, "members"), original["population"][0]["members"][:-1]),
        add_fraction(original, ("population", 0, "annotation_error")),
        add_fraction(original, ("population", 3, "quadrature_error")),
        add_fraction(original, ("population", 3, "overlaps", 0, "volume")),
        add_fraction(original, ("moments", "inclusion", "covariance", 1, 2)),
        add_fraction(original, ("moments", "inclusion", "decompositions", 3, "sampling_bias")),
        add_fraction(original, ("moments", "inclusion", "decompositions", 3, "total_error")),
        add_fraction(original, ("joint_covariance", 1, 2)),
        replaced(
            original, ("counts", "zero_joint_pairs"), original["counts"]["zero_joint_pairs"] + 1
        ),
    ]
    assert len(changes) == 16
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.check_case(bad, original)
    assert wire(original) == before


def test_fixed_complete_suite_corruptions_cannot_overstate_access_or_control_results(
    runner, expected_suite
):
    original = expected_suite
    changes = [
        replaced(
            original,
            ("controls", "warp", 0, "marked_positive_laws_equal"),
            not original["controls"]["warp"][0]["marked_positive_laws_equal"],
        ),
        replaced(
            original,
            ("controls", "stale_marks", 0, "packets_equal_base"),
            not original["controls"]["stale_marks"][0]["packets_equal_base"],
        ),
        add_fraction(original, ("controls", "boundaries", 0, "unaligned_quadrature_errors", 0)),
        replaced(original, ("public_controls", "invalid_calls_rejected"), 17),
        replaced(original, ("totals", "cases"), 19),
        replaced(original, ("scope", "annotations_proved_necessary_or_minimal"), True),
        replaced(original, ("cases",), list(reversed(original["cases"]))),
        {**original, "only_favorable_errors_retained": True},
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.check_suite(bad, original)
    assert wire(original) == before


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05ag_guards",Path(sys.argv[1]))
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
require(len(list(h.graph_inputs(valid)))==18,"graph fixture inventory")
for i,filename in enumerate(("volume.py","reference_qr05ag.py")):
    module=h.private_module("_qr05ag_guard_core"+str(i),filename)
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
    try:
        reject(module.analyze,h.replaced(valid,("record","past",4),[2,3]))
        reject(module.analyze,h.replaced(valid,("record","marks",1,"volume"),[0,1]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    hooks={n:getattr(module,n) for n in ("_members","_weight")}
    for n in hooks:setattr(module,n,forbidden)
    try:reject(module.analyze,h.problem_of(3,[1,0,0,0]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    for v in (h.nested(0,64),h.nested([],64)):module._native(v)
    for v in (h.nested(0,65),h.nested([],65)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,62)]);reject(module._native,[shared,h.nested(shared,63)])
    tiny=h.F(1,1<<4095)
    cancelled=h.problem_of(3,[1-2*tiny,0,tiny,tiny],marks=[tiny,tiny])
    require(h.wire(module.analyze(cancelled))==h.wire(h.independent_analysis(cancelled)),"unretained pbar cancellation")
    reject(module.analyze,h.problem_of(3,[1-tiny,0,0,tiny],marks=[1,1]))
    reject(module.analyze,h.problem_of(marks=[h.F(1<<4095),h.F(1<<4095)]))
    old=module.MAX_BITS;module.MAX_BITS=2
    try:require(module._weight("uniform_rate",h.F(1,2),h.F(9,49))==h.F(49,9),"unretained inverse must remain unbounded")
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
    result=module.analyze(shared_valid);result["questions"][0]["estimates"]["raw"][0]=-1
    result["marginals"][0][0]=2
    require(h.wire(module.analyze(shared_valid))==h.wire(h.independent_analysis(shared_valid)),"ownership and restored caps")
runner=h.private_module("_qr05ag_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,128),h.nested([],128)):runner.require_wire(v)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==60,"pre-serialization rejection inventory")
require(rejections==2*(len(invalid)+51)+22,"explicit rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ag.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 51) + 22,
        "pre_serialization_rejections": 60,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }
