"""Independent exact finite-decision oracle and native boundary controls.

Only pinned Z JSON is read for fixed experiments. The generic oracle enumerates
finite candidate/world pairs; it imports no current or prior decision executor.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
WEIGHTS = [[0, 1], [1, 2], [1, 1]]
Z_SHA = "7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc"
CHECKS = (
    "coarse_zero",
    "nested_uncertainty",
    "complete_argmax",
    "complete_argmin",
    "minimax_nonpositive",
    "bound_extension_non_decrease",
)
COUNTS = {
    "worlds": 4,
    "assumed_models": 4,
    "rules": 3,
    "decisions": 16,
    "world_rule_cells": 48,
    "excess_terms": 48,
    "candidate_world_visits": 120,
    "candidate_selection_visits": 48,
    "total_decision_work": 216,
}
PRODUCER_CONTROLS = {
    "risk_table_matches_Z": True,
    "literal_forecast_risks_checked": True,
    "original_history_report_weights_preserved": True,
    "fixed_rule_forecasts_actual_index_independent": True,
    "W_affine_actual_joint_and_risk": True,
    "W_constant_coarse_risk": True,
    "W_clean_forecast_segment_and_excess": True,
    "W_full_replacement_quadratic_penalty": True,
    "W_excess_monotonicity_and_upper_endpoint": True,
    "W_full_bound_coarse_and_coincidence_ties": True,
    "origin_authenticated_by_generic_API": False,
    "raw_history_reconstruction_performed_by_this_runner": False,
}


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


def independently_decide(problem):
    """Enumerate Cartesian entries; sort exact values to expose every tie."""
    rows = copy.deepcopy(problem["worlds"])
    excess = {}
    for world in rows:
        t = world["actual_index"]
        coarse = fraction(world["coarse_risk"])
        for model in world["models"]:
            s = model["assumed_index"]
            model["excess_risks"] = []
            for a, risk in enumerate(model["forecast_risks"]):
                excess[t, s, a] = fraction(risk) - coarse
                model["excess_risks"].append(fw(excess[t, s, a]))
    decisions = []
    for s in range(4):
        previous = None
        for bound in range(4):
            worlds = list(range(bound + 1))
            candidates = []
            worsts = []
            for a in range(3):
                ranked = sorted((excess[t, s, a], t) for t in worlds)
                worst = ranked[-1][0]
                worsts.append(worst)
                argmax = [t for value, t in ranked if value == worst]
                candidates.append(
                    {
                        "retained_weight": copy.deepcopy(WEIGHTS[a]),
                        "world_excesses": [fw(excess[t, s, a]) for t in worlds],
                        "worst_excess": fw(worst),
                        "worst_world_indices": argmax,
                    }
                )
            ordered = sorted((value, a) for a, value in enumerate(worsts))
            best = ordered[0][0]
            argmin = [a for value, a in ordered if value == best]
            assert worsts[0] == 0 and best <= 0
            if previous is not None:
                assert all(old <= new for old, new in zip(previous[0], worsts, strict=True))
                assert previous[1] <= best
            decisions.append(
                {
                    "assumed_index": s,
                    "bound_index": bound,
                    "world_indices": worlds,
                    "candidates": candidates,
                    "minimax_excess": fw(best),
                    "minimizer_indices": argmin,
                    "minimizer_weights": [copy.deepcopy(WEIGHTS[a]) for a in argmin],
                    "checks": {key: True for key in CHECKS},
                }
            )
            previous = worsts, best
    return {
        "input_sha256": digest(problem),
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "worlds": rows,
        "decisions": decisions,
        "counts": copy.deepcopy(COUNTS),
    }


def problem_of(coarse=(1, 1, 1, 1), half=(1, 1, 1, 1), full=(1, 1, 1, 1)):
    return {
        "schema_version": "det8-qr05aa-problem-v1",
        "family": "qr05aa_uncertainty_decision",
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "worlds": [
            {
                "actual_index": t,
                "coarse_risk": fw(coarse[t]),
                "models": [
                    {
                        "assumed_index": s,
                        "forecast_risks": [fw(coarse[t]), fw(half[t]), fw(full[t])],
                    }
                    for s in range(4)
                ],
            }
            for t in range(4)
        ],
    }


def signed_problem():
    return problem_of(half=(F(7, 8),) * 4, full=(F(1, 2), F(3, 4), F(2, 3), F(1, 4)))


def tie_problem():
    return problem_of(half=(1, F(3, 4), 1, F(1, 2)), full=(F(3, 4), 1, 1, F(1, 2)))


def global_rule_problem():
    return problem_of(half=(F(1, 2), F(3, 2), 1, 1), full=(F(3, 2), F(1, 2), 1, 1))


def varying_problem():
    p = problem_of(coarse=(0, 2, 1, 1), half=(1, 2, 1, 1), full=(1, 1, 1, 1))
    for t, world in enumerate(p["worlds"]):
        for s in range(1, 4):
            world["models"][s]["forecast_risks"][1:] = [
                fw(F(t + 2 * s + 1, 10)),
                fw(F(3 * t + s + 1, 10)),
            ]
    return p


def shared_problem():
    p = tie_problem()
    one = [1, 1]
    for world in p["worlds"]:
        world["coarse_risk"] = one
        for model in world["models"]:
            model["forecast_risks"][0] = one
    return p


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05aa_test_direct", "decision.py"),
        private_module("_qr05aa_test_reference", "reference_qr05aa.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05aa_test_runner", "study.py")


@pytest.mark.parametrize(
    "builder",
    [problem_of, signed_problem, tie_problem, global_rule_problem, varying_problem, shared_problem],
)
def test_generic_complete_wires_equal_independent_finite_enumeration(executors, builder):
    p = builder()
    before = wire(p)
    wanted = independently_decide(p)
    for module in executors:
        actual = module.analyze(p)
        assert wire(actual) == wire(wanted)
        assert wire(p) == before


def test_signed_benefits_are_not_clamped_and_generic_worst_world_can_be_interior(executors):
    p = signed_problem()
    for module in executors:
        decision = module.analyze(p)["decisions"][3]
        assert [c["worst_excess"] for c in decision["candidates"]] == [[0, 1], [-1, 8], [-1, 4]]
        assert decision["minimax_excess"] == [-1, 4]
        assert decision["minimizer_indices"] == [2]
        assert decision["candidates"][2]["worst_world_indices"] == [1]
        clipped = [max(F(0), fraction(c["worst_excess"])) for c in decision["candidates"]]
        assert clipped == [0, 0, 0]
        assert max(fraction(decision["candidates"][2]["world_excesses"][t]) for t in (0, 3)) == F(
            -1, 2
        )


def test_all_argmin_and_argmax_ties_are_retained_without_retrospective_tie_breaker(executors):
    for module in executors:
        decisions = module.analyze(tie_problem())["decisions"]
        assert decisions[0]["minimizer_indices"] == [2]
        assert decisions[1]["minimizer_indices"] == [0, 1, 2]
        assert decisions[3]["minimizer_weights"] == WEIGHTS
        assert [c["worst_world_indices"] for c in decisions[3]["candidates"]] == [
            list(range(4)),
            [0, 2],
            [1, 2],
        ]
        all_tied = module.analyze(problem_of())["decisions"]
        for d in all_tied:
            assert d["minimizer_indices"] == [0, 1, 2]
            assert all(c["worst_world_indices"] == d["world_indices"] for c in d["candidates"])


def test_one_rule_is_global_and_minimax_cannot_switch_using_the_actual_world(executors):
    for module in executors:
        decision = module.analyze(global_rule_problem())["decisions"][1]
        assert decision["minimizer_indices"] == [0] and decision["minimax_excess"] == [0, 1]
        assert [c["worst_excess"] for c in decision["candidates"]] == [[0, 1], [1, 2], [1, 2]]
        illegal = max(
            min(fraction(c["world_excesses"][t]) for c in decision["candidates"]) for t in range(2)
        )
        assert illegal == F(-1, 2)
        # Uniformly averaging possible actual worlds is not robust maximization.
        assert [sum(map(fraction, c["world_excesses"])) / 2 for c in decision["candidates"]] == [
            0,
            0,
            0,
        ]


def test_coarse_is_subtracted_under_each_actual_law_before_maximization(executors):
    p = varying_problem()
    for module in executors:
        a = module.analyze(p)
        candidate = a["decisions"][1]["candidates"][1]
        assert candidate["world_excesses"] == [[1, 1], [0, 1]]
        assert candidate["worst_excess"] == [1, 1]
        wrong = max(fraction(w["models"][0]["forecast_risks"][1]) for w in p["worlds"][:2]) - max(
            fraction(w["coarse_risk"]) for w in p["worlds"][:2]
        )
        assert wrong == 0
        assert a["decisions"][3]["candidates"] != a["decisions"][7]["candidates"]


def test_prefix_bounds_include_every_declared_world_but_never_outside_worlds(executors):
    p = signed_problem()
    changed = copy.deepcopy(p)
    changed["worlds"][3]["models"][2]["forecast_risks"][2] = [2, 1]
    for module in executors:
        old, new = module.analyze(p), module.analyze(changed)
        for s in range(4):
            for bound in range(4):
                index = 4 * s + bound
                assert old["decisions"][index]["world_indices"] == list(range(bound + 1))
                if s != 2 or bound != 3:
                    assert wire(old["decisions"][index]) == wire(new["decisions"][index])
        assert old["decisions"][11] != new["decisions"][11]


def test_nested_values_monotone_does_not_mean_minimizer_sets_are_nested(executors):
    p = problem_of(half=(F(1, 2), 1, 1, 1), full=(F(3, 4), F(3, 4), 1, 1))
    for module in executors:
        d = module.analyze(p)["decisions"][:4]
        assert [x["minimizer_indices"] for x in d] == [[1], [2], [0, 1, 2], [0, 1, 2]]
        assert [x["minimax_excess"] for x in d] == [[-1, 2], [-1, 4], [0, 1], [0, 1]]
        assert all(all(x["checks"].values()) for x in d)


def test_full_native_risk_range_and_generic_nonaffine_tables_are_not_physics_validators(executors):
    p = problem_of(coarse=(2, 0, 2, 0), half=(0, 2, 0, 2), full=(2, 0, 0, 2))
    expected = independently_decide(p)
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(expected)
        assert a["worlds"][0]["models"][0]["excess_risks"][1] == [-2, 1]
        assert a["worlds"][1]["models"][0]["excess_risks"][1] == [2, 1]


def test_large_exact_ties_and_cancelling_intermediates_are_not_float_comparisons(executors):
    d = (1 << 4095) - 1
    cases = [
        problem_of(full=(F(d - 1, d),) * 4),
        problem_of(coarse=(F(d - 1, d),) * 4, half=(F(d - 2, d),) * 4, full=(F(d - 3, d),) * 4),
        problem_of(coarse=(0,) * 4, half=(F(1, d),) * 4, full=(F(1, d - 2),) * 4),
    ]
    for p in cases:
        wanted = independently_decide(p)
        for module in executors:
            assert wire(module.analyze(p)) == wire(wanted)
    for module in executors:
        tiny = module.analyze(cases[0])["decisions"][3]
        assert tiny["minimizer_indices"] == [2]
        assert tiny["minimax_excess"] == [-1, d]


def overflow_problem():
    d = 1 << 4095
    return problem_of(coarse=(F(1, d),) * 4, half=(F(1, 3),) * 4, full=(F(1, d),) * 4)


def test_genuinely_retained_4097_bit_difference_is_rejected(executors):
    p = overflow_problem()
    native(p)
    overflow = fraction(p["worlds"][0]["models"][0]["forecast_risks"][1]) - fraction(
        p["worlds"][0]["coarse_risk"]
    )
    assert overflow.denominator.bit_length() == 4097
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
    p = varying_problem()
    bad = [None, [], 0, True, "problem", DictChild(p)]
    for key in p:
        item = copy.deepcopy(p)
        del item[key]
        bad.append(item)
    for key in ("extra", "artifact", "history_weights", "selector"):
        bad.append({**p, key: 0})
    for key, values in {
        "schema_version": ["det8-qr05z-problem-v1", StrChild(p["schema_version"]), None],
        "family": ["unknown", StrChild(p["family"]), True],
        "levels": [tuple(LEVELS), ListChild(LEVELS), LEVELS[::-1], LEVELS[:-1], LEVELS + [[2, 1]]],
        "retained_weights": [
            tuple(WEIGHTS),
            ListChild(WEIGHTS),
            WEIGHTS[::-1],
            WEIGHTS[:-1],
            WEIGHTS + [[1, 3]],
        ],
        "worlds": [
            tuple(p["worlds"]),
            ListChild(p["worlds"]),
            [],
            p["worlds"][:-1],
            p["worlds"] + [p["worlds"][0]],
            p["worlds"][::-1],
        ],
    }.items():
        bad.extend(replaced(p, (key,), value) for value in values)
    for path in (("worlds", 0), ("worlds", 0, "models", 0)):
        node = p[path[0]][path[1]] if len(path) == 2 else p["worlds"][0]["models"][0]
        for key in node:
            item = node.copy()
            del item[key]
            bad.append(replaced(p, path, item))
        bad.extend(
            replaced(p, path, value) for value in (DictChild(node), {**node, "extra": 0}, [], None)
        )
    for path in (("worlds", 0, "actual_index"), ("worlds", 0, "models", 0, "assumed_index")):
        bad.extend(
            replaced(p, path, value) for value in (True, IntChild(0), 0.0, "0", -1, 1, 4, None)
        )
    models = p["worlds"][0]["models"]
    for value in (
        tuple(models),
        ListChild(models),
        [],
        models[:-1],
        models + [models[0]],
        models[::-1],
    ):
        bad.append(replaced(p, ("worlds", 0, "models"), value))
    risks = p["worlds"][0]["models"][0]["forecast_risks"]
    for value in (tuple(risks), ListChild(risks), [], risks[:-1], risks + [[0, 1]], None):
        bad.append(replaced(p, ("worlds", 0, "models", 0, "forecast_risks"), value))
    fractions = [
        None,
        1,
        True,
        0.5,
        F(1, 2),
        (1, 2),
        ListChild([1, 2]),
        [],
        [1],
        [1, 2, 3],
        [True, 1],
        [1, False],
        [IntChild(1), 2],
        [1, IntChild(2)],
        [1.0, 2],
        [1, 2.0],
        ["1", 2],
        [1, "2"],
        [1, 0],
        [1, -2],
        [-1, 2],
        [3, 1],
        [2, 4],
        [0, 2],
        [1, 1 << 4096],
    ]
    bad.extend(
        replaced(p, ("worlds", 3, "models", 3, "forecast_risks", 2), value) for value in fractions
    )
    bad.extend(
        replaced(p, ("worlds", 2, "coarse_risk"), value)
        for value in ([2, 2], [False, 1], (1, 1), [3, 1])
    )
    bad.append(replaced(p, ("worlds", 0, "models", 3, "forecast_risks", 0), [1, 1]))
    bad.append(replaced(p, ("levels", 0, 0), False))
    bad.append(replaced(p, ("retained_weights", 1), [2, 4]))
    item = p.copy()
    item[StrChild("family")] = item.pop("family")
    bad.append(item)
    bad.append({**p, 7: None})
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_native_schema_and_order_are_rejected_without_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def mutable_ids(value):
    if type(value) not in (dict, list):
        return set()
    result = {id(value)}
    for child in value.values() if type(value) is dict else value:
        result |= mutable_ids(child)
    return result


def test_shared_inputs_outputs_and_separate_calls_have_no_mutable_aliases(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        first, second = module.analyze(p), module.analyze(p)
        wanted = wire(second)
        assert wire(first) == wanted == wire(independently_decide(p))
        assert mutable_ids(p).isdisjoint(mutable_ids(first))
        assert mutable_ids(first).isdisjoint(mutable_ids(second))
        first["worlds"][0]["models"][0]["forecast_risks"][0][0] = -1
        first["decisions"][0]["minimizer_weights"][0][0] = -1
        assert wire(second) == wanted and wire(p) == before
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["worlds"][0]["models"][0]["forecast_risks"][2] = [2, 1]
        assert wire(detached) == wanted
        assert wire(module.analyze(changed)) != wanted
        assert wire(module.analyze(p)) == wanted


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def test_all_work_caps_are_planned_before_difference_and_all_visits_are_counted(
    executors, monkeypatch
):
    p = varying_problem()
    for module in executors:
        original = module._difference
        calls = []

        def observed(risk, coarse, calls=calls, original=original):
            calls.append((risk, coarse))
            return original(risk, coarse)

        with monkeypatch.context() as patched:
            patched.setattr(module, "_difference", observed)
            a = module.analyze(p)
        assert len(calls) == 48
        assert a["counts"] == COUNTS
        for key, cap in (("MAX_RISK_CELLS", 48), ("MAX_DECISION_WORK", 216)):

            def forbidden(*_args):
                raise RuntimeError("decision arithmetic began before complete work plan")

            with monkeypatch.context() as patched:
                patched.setattr(module, key, cap - 1)
                patched.setattr(module, "_difference", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
            with monkeypatch.context() as patched:
                patched.setattr(module, key, cap)
                assert wire(module.analyze(p)) == wire(a)


def test_complete_last_model_validation_precedes_the_first_subtraction(executors, monkeypatch):
    p = replaced(varying_problem(), ("worlds", 3, "models", 3, "forecast_risks", 2), [2, 4])
    for module in executors:

        def forbidden(*_args):
            raise RuntimeError("subtraction preceded complete schema validation")

        with monkeypatch.context() as patched:
            patched.setattr(module, "_difference", forbidden)
            with pytest.raises(ValueError):
                module.analyze(p)


@pytest.mark.parametrize(
    "constant",
    ["MAX_RISK_CELLS", "MAX_DECISION_WORK", "MAX_BITS", "MAX_DEPTH", "MAX_NODES", "MAX_BYTES"],
)
def test_each_live_cap_rejects_instead_of_truncating_and_is_not_cached(
    executors, monkeypatch, constant
):
    p = varying_problem()
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def test_input_expanded_nodes_leaf_depth_and_exact_ascii_size_precede_serialization(
    executors, monkeypatch
):
    p = shared_problem()
    nodes, depth = tree_resources(p)
    assert nodes > len(mutable_ids(p))
    for module in executors:
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("unvalidated input reached whole-tree serialization")

            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit)
                patched.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        # Native input boundary alone; the complete output is a larger tree.
        for constant, limit in (("MAX_NODES", nodes), ("MAX_DEPTH", depth)):
            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit)
                module._native(p)


def test_output_has_its_own_live_byte_cap_and_exact_success_boundary(executors, monkeypatch):
    p = problem_of()
    for module in executors:
        wanted = wire(module.analyze(p))
        assert len(wanted) > len(wire(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, "MAX_BYTES", len(wanted) - 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        with monkeypatch.context() as patched:
            patched.setattr(module, "MAX_BYTES", len(wanted))
            assert wire(module.analyze(p)) == wanted


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def graph_inputs(valid):
    cycle_list = []
    cycle_list.append(cycle_list)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    dag = []
    for _ in range(40):
        dag = [dag, dag]
    for value in (cycle_list, cycle_dict, nested([], 1500), dag):
        yield {**valid, "extra": value}
    for path in (
        ("levels",),
        ("retained_weights",),
        ("worlds",),
        ("worlds", 0),
        ("worlds", 0, "actual_index"),
        ("worlds", 0, "coarse_risk"),
        ("worlds", 0, "models"),
        ("worlds", 0, "models", 0),
        ("worlds", 0, "models", 0, "assumed_index"),
        ("worlds", 0, "models", 0, "forecast_risks"),
        ("worlds", 0, "models", 0, "forecast_risks", 0),
    ):
        yield replaced(valid, path, dag)


def test_runner_exact_scalar_empty_container_and_shared_subtree_depth_boundaries(runner):
    for value in (nested(0, 128), nested([], 128)):
        runner.require_wire(value)
    for value in (nested(0, 129), nested([], 129)):
        with pytest.raises(ValueError):
            runner.require_wire(value)
    shared = [0]
    runner.require_wire([shared, nested(shared, 126)])
    with pytest.raises(ValueError):
        runner.require_wire([shared, nested(shared, 127)])


def test_core_native_exact_scalar_empty_and_cached_subtree_depth_boundaries(executors):
    for module in executors:
        for value in (nested(0, 128), nested([], 128)):
            module._native(value)
        for value in (nested(0, 129), nested([], 129)):
            with pytest.raises(ValueError):
                module._native(value)
        shared = [0]
        module._native([shared, nested(shared, 126)])
        with pytest.raises(ValueError):
            module._native([shared, nested(shared, 127)])


def test_exact_ascii_escape_and_key_bytes_include_newline_but_keys_are_not_nodes(
    executors, monkeypatch
):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    size = len(wire(value))
    nodes, depth = tree_resources(value)
    assert nodes == 8 and depth == 2
    for module in executors:
        for constant, cap in (("MAX_NODES", nodes), ("MAX_DEPTH", depth), ("MAX_BYTES", size)):
            with monkeypatch.context() as patched:
                patched.setattr(module, constant, cap)
                module._native(value)
                patched.setattr(module, constant, cap - 1)
                with pytest.raises(ValueError):
                    module._native(value)


def test_generic_auditor_reproduces_entire_wire_including_all_tie_sets():
    audit = private_module("_qr05aa_test_audit_generic", "audit_json.py")
    for p in (signed_problem(), tie_problem(), varying_problem(), global_rule_problem()):
        before = wire(p)
        assert wire(audit.expected_aa(p)) == wire(independently_decide(p))
        assert wire(p) == before


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_native_graph_work_and_ownership_guards_in_bounded_subprocess(tmp_path, optimized):
    program = r"""
import importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
spec = importlib.util.spec_from_file_location("_qr05aa_guard_helpers", Path(sys.argv[1]))
if spec is None or spec.loader is None:
    raise RuntimeError("helpers unavailable")
helpers = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = helpers
spec.loader.exec_module(helpers)
rejections = before_serialization = 0
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def reject(call, value):
    global rejections
    try:
        call(value)
    except ValueError:
        rejections += 1
    else:
        raise RuntimeError("malformed input was accepted")
def reject_before_dump(call, value):
    global before_serialization
    original = json.dumps
    def forbidden(*args, **kwargs):
        raise RuntimeError("unsafe native tree reached whole serialization")
    json.dumps = forbidden
    try:
        reject(call, value)
        before_serialization += 1
    finally:
        json.dumps = original
invalid = helpers.invalid_problems()
valid = helpers.shared_problem()
for index, filename in enumerate(("decision.py", "reference_qr05aa.py")):
    module = helpers.private_module("_qr05aa_guard_core_" + str(index), filename)
    for builder in (helpers.signed_problem, helpers.tie_problem, helpers.global_rule_problem, helpers.varying_problem):
        p = builder()
        require(helpers.wire(module.analyze(p)) == helpers.wire(helpers.independently_decide(p)), "complete generic decision wire")
    reference = module.analyze(valid)
    for bad in invalid:
        reject(module.analyze, bad)
    graphs = list(helpers.graph_inputs(valid))
    require(len(graphs) == 15, "native graph placement inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)
    for constant, cap in (("MAX_RISK_CELLS",48), ("MAX_DECISION_WORK",216)):
        old_cap, old_difference = getattr(module, constant), module._difference
        def forbidden(*args):
            raise RuntimeError("subtraction began before full work preflight")
        setattr(module, constant, cap - 1)
        module._difference = forbidden
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old_cap)
            module._difference = old_difference
    for constant in ("MAX_RISK_CELLS", "MAX_DECISION_WORK", "MAX_BITS", "MAX_DEPTH", "MAX_NODES", "MAX_BYTES"):
        old = getattr(module, constant)
        setattr(module, constant, 1)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old)
    reject(module.analyze, helpers.overflow_problem())
    for value in (helpers.nested(0,128), helpers.nested([],128)):
        module._native(value)
    for value in (helpers.nested(0,129), helpers.nested([],129)):
        reject(module._native, value)
    shared = [0]
    module._native([shared,helpers.nested(shared,126)])
    reject(module._native, [shared,helpers.nested(shared,127)])
    require(module.analyze(valid) == helpers.independently_decide(valid), "benign sharing or cap restoration failed")
    reference["worlds"][0]["models"][0]["forecast_risks"][0][0] = -1
    require(module.analyze(valid)["worlds"][0]["models"][0]["forecast_risks"][0] == [1,1], "output alias escaped into later call")
runner = helpers.private_module("_qr05aa_guard_runner", "study.py")
for bad in helpers.graph_inputs(valid):
    reject_before_dump(runner.require_wire, bad)
for value in (helpers.nested(0,129), helpers.nested([],129)):
    reject(runner.require_wire, value)
shared = [0]
reject(runner.require_wire, [shared,helpers.nested(shared,127)])
reject(lambda value: runner.require_same_wire({"x":0}, value, "typed regression"), {"x":False})
require(before_serialization == 45, "pre-serialization inventory")
require(rejections == 2*(len(invalid)+27)+19, "explicit rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":before_serialization,
                  "invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05aa.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 27) + 19,
        "pre_serialization_rejections": 45,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


@pytest.fixture(scope="session")
def pinned_z():
    path = HERE.parent / "qr-05z-fixed-attenuation-2026-09-07" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 31075315 and hashlib.sha256(raw).hexdigest() == Z_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


def case_problem(case):
    """Read only Z's complete experiment-weighted scalars, retaining all 48."""
    p = problem_of()
    z = case["analysis"]
    assert z["levels"] == LEVELS and z["retained_weights"] == WEIGHTS
    for t in range(4):
        p["worlds"][t]["coarse_risk"] = copy.deepcopy(
            z["baseline"]["aggregate"]["pairs"][4 * t]["coarse_forecast_risk"]
        )
        for s in range(4):
            pair = z["aggregate"]["pairs"][4 * t + s]
            assert (pair["actual_index"], pair["assumed_index"]) == (t, s)
            assert [b["retained_weight"] for b in pair["blends"]] == WEIGHTS
            p["worlds"][t]["models"][s]["forecast_risks"] = [
                copy.deepcopy(b["forecast_risk"]) for b in pair["blends"]
            ]
    return p


@pytest.fixture(scope="session")
def problems(pinned_z):
    return [case_problem(case) for case in pinned_z["cases"]]


@pytest.fixture(scope="session")
def expected(problems):
    return [independently_decide(p) for p in problems]


@pytest.fixture(scope="session")
def analyses(executors, problems):
    answer = []
    for p in problems:
        before = wire(p)
        answer.append(tuple(module.analyze(p) for module in executors))
        assert wire(p) == before
    return answer


@pytest.mark.parametrize("case_index", range(6))
def test_fixed_all_six_complete_wires_equal_independent_enumeration(
    problems, analyses, expected, case_index
):
    p, results, wanted = problems[case_index], analyses[case_index], expected[case_index]
    assert wanted["input_sha256"] == digest(p)
    for a in results:
        assert wire(a) == wire(wanted)


def read_law(rows):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in rows}


def outcome_risk(actual, forecast):
    assert sum(actual.values()) == sum(forecast.values()) == 1
    coordinates = actual.keys() | forecast.keys()
    return sum(
        probability * sum((forecast.get(q, F(0)) - (q == truth)) ** 2 for q in coordinates)
        for truth, probability in actual.items()
    )


def test_fixed_projection_preserves_original_history_report_weights_and_complete_law_scores(
    pinned_z, problems
):
    for case, p in zip(pinned_z["cases"], problems, strict=True):
        z = case["analysis"]
        beliefs = case["problem"]["experiment"]["beliefs"]
        assert sum(fraction(b["weight"]) for b in beliefs) == 1
        risks = {(t, s, a): F(0) for t in range(4) for s in range(4) for a in range(3)}
        coarse = {t: F(0) for t in range(4)}
        fixed_forecasts = {}
        for source, certified in zip(beliefs, z["beliefs"], strict=True):
            assert (
                source["belief_id"] == certified["belief_id"]
                and source["weight"] == certified["weight"]
            )
            history_weight = fraction(source["weight"])
            fallbacks = {
                tuple(row["value"]): read_law(row["prediction"]) for row in source["fallbacks"]
            }
            for t, channel in enumerate(source["channels"]):
                actual_cells = {tuple(cell["value"]): cell for cell in channel["cells"]}
                assert sum(fraction(cell["probability"]) for cell in actual_cells.values()) == 1
                for s in range(4):
                    pair = certified["pairs"][4 * t + s]
                    assert [tuple(cell["value"]) for cell in pair["cells"]] == list(actual_cells)
                    local_risks = [F(0)] * 3
                    for cell in pair["cells"]:
                        report = tuple(cell["value"])
                        actual = actual_cells[report]
                        report_weight = fraction(actual["probability"])
                        truth = read_law(actual["prediction"])
                        g = fallbacks[report[:5]]
                        cg = outcome_risk(truth, g)
                        if s == 0:
                            coarse[t] += history_weight * report_weight * cg
                        for a, blend in enumerate(cell["blends"]):
                            forecast = read_law(blend["forecast"])
                            if a == 0:
                                assert forecast == g
                            key = source["belief_id"], s, a, report
                            assert key not in fixed_forecasts or fixed_forecasts[key] == forecast
                            fixed_forecasts[key] = forecast
                            risk = outcome_risk(truth, forecast)
                            assert fw(risk) == blend["forecast_risk"]
                            assert fw(cg - risk) == blend["gain_over_coarse"]
                            local_risks[a] += report_weight * risk
                            risks[t, s, a] += history_weight * report_weight * risk
                    assert [fw(r) for r in local_risks] == [
                        b["forecast_risk"] for b in pair["blends"]
                    ]
        for t, world in enumerate(p["worlds"]):
            assert world["coarse_risk"] == fw(coarse[t])
            for s, model in enumerate(world["models"]):
                assert model["forecast_risks"] == [fw(risks[t, s, a]) for a in range(3)]
                for a in range(3):
                    assert (
                        fw(coarse[t] - risks[t, s, a])
                        == z["aggregate"]["pairs"][4 * t + s]["blends"][a]["gain_over_coarse"]
                    )


def test_fixed_family_controls_do_not_replace_the_generic_interior_world_contract(
    pinned_z, expected
):
    for case, analysis in zip(pinned_z["cases"], expected, strict=True):
        worlds = analysis["worlds"]
        assert all(w["coarse_risk"] == worlds[0]["coarse_risk"] for w in worlds)
        for s in range(4):
            for a in range(3):
                risks = [fraction(w["models"][s]["forecast_risks"][a]) for w in worlds]
                excess = [fraction(w["models"][s]["excess_risks"][a]) for w in worlds]
                assert risks[1] == (risks[0] + risks[3]) / 2
                assert risks[2] == (risks[0] + 3 * risks[3]) / 4
                assert excess == sorted(excess) and excess[0] <= 0 <= excess[3]
                for bound in range(4):
                    assert (
                        bound
                        in analysis["decisions"][4 * s + bound]["candidates"][a][
                            "worst_world_indices"
                        ]
                    )
            d = analysis["decisions"][4 * s + 3]
            assert 0 in d["minimizer_indices"] and d["minimax_excess"] == [0, 1]
            full_cells = [
                cell
                for belief in case["analysis"]["baseline"]["beliefs"]
                for cell in belief["pairs"][12 + s]["cells"]
            ]
            coincide = all(
                read_law(cell["forecast"]) == read_law(cell["coarse_forecast"])
                for cell in full_cells
            )
            assert (d["minimizer_indices"] == [0, 1, 2]) == coincide
            assert all(
                read_law(cell["actual_prediction"]) == read_law(cell["coarse_forecast"])
                for cell in full_cells
            )


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_runner_full_wire_producer_controls_inventory_and_no_risk_pooling(
    runner, pinned_z, problems, expected, aggregate
):
    assert set(aggregate) == {
        "producer",
        "cases",
        "independent_route_equal",
        "public_controls",
        "totals",
    }
    assert aggregate["producer"] == {
        "artifact": "qr-05z-fixed-attenuation-2026-09-07/results.json",
        "bytes": 31075315,
        "sha256": Z_SHA,
    }
    assert aggregate["independent_route_equal"] is True
    assert aggregate["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        "raw_laws_histories_or_artifacts_given_to_core": False,
        "bounds_inferred_from_data": False,
        "actual_level_used_to_select_rule": False,
        "all_ties_retained": True,
        "finite_menu_only": True,
    }
    assert aggregate["totals"] == {
        "cases": 6,
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        **{key: 6 * value for key, value in COUNTS.items()},
    }
    assert len(aggregate["cases"]) == 6
    assert wire(runner.fixtures()) == wire(pinned_z)
    for case, row, p, wanted in zip(
        pinned_z["cases"], aggregate["cases"], problems, expected, strict=True
    ):
        assert set(row) == {"case_id", "problem", "analysis", "producer_controls"}
        assert row["case_id"] == case["case_id"]
        assert wire(row["problem"]) == wire(p) == wire(runner.case_problem(case))
        assert wire(row["analysis"]) == wire(wanted)
        assert wire(row["producer_controls"]) == wire(PRODUCER_CONTROLS)
        assert wire(runner.check_analysis(row["analysis"], case)) == wire(PRODUCER_CONTROLS)


def output_corruptions(analysis):
    corruptions = []

    def add(path, value):
        bad = replaced(analysis, path, value)
        assert wire(bad) != wire(analysis)
        corruptions.append(bad)

    add(("input_sha256",), "0" * 64)
    add(("worlds", 0, "models", 0, "excess_risks", 0), [1, 1])
    add(("decisions", 0, "world_indices"), [1])
    add(("decisions", 0, "candidates", 0, "world_excesses"), [[1, 1]])
    add(("decisions", 3, "candidates", 0, "worst_world_indices"), [3])
    add(("decisions", 3, "candidates", 0, "worst_excess"), [1, 1])
    add(("decisions", 3, "minimax_excess"), [-1, 1])
    add(("decisions", 3, "minimizer_indices"), [])
    add(("decisions", 3, "minimizer_weights"), [])
    add(("decisions", 0, "checks", "complete_argmax"), False)
    add(("counts", "total_decision_work"), 215)
    add(("levels", 0, 0), False)
    return corruptions


def test_fixed_runner_rejects_nonvacuous_complete_decision_wire_corruption(
    runner, pinned_z, expected
):
    case, wanted = pinned_z["cases"][0], expected[0]
    for bad in output_corruptions(wanted):
        with pytest.raises(ValueError):
            runner.check_analysis(bad, case)


def test_fixed_runner_authenticates_nonvacuous_projected_risks_weights_and_laws(
    runner, pinned_z, expected
):
    case, wanted = pinned_z["cases"][0], expected[0]
    corruptions = [
        replaced(
            case, ("analysis", "aggregate", "pairs", 0, "blends", 0, "forecast_risk"), [-1, 1]
        ),
        replaced(case, ("analysis", "baseline", "beliefs", 0, "weight"), [0, 1]),
        replaced(
            case,
            (
                "analysis",
                "beliefs",
                0,
                "pairs",
                0,
                "cells",
                0,
                "blends",
                1,
                "forecast",
                0,
                "probability",
            ),
            [0, 1],
        ),
        replaced(
            case,
            ("problem", "experiment", "beliefs", 0, "channels", 0, "cells", 0, "probability"),
            [0, 1],
        ),
        replaced(case, ("problem", "experiment", "beliefs", 0, "weight"), [0, 1]),
        replaced(
            case,
            ("problem", "experiment", "beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"),
            [0, 1],
        ),
    ]
    for bad in corruptions:
        assert wire(bad) != wire(case)
        with pytest.raises(ValueError):
            runner.check_analysis(wanted, bad)
