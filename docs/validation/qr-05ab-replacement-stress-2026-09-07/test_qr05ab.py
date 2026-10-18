"""Independent frozen-certificate stress oracle and native boundary controls.

The nominal oracle/fixture helpers are statically carried from our own AA tests.
No current or previous executor is imported to derive expected output.
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
AA_CHECKS = (
    "coarse_zero",
    "nested_uncertainty",
    "complete_argmax",
    "complete_argmin",
    "minimax_nonpositive",
    "bound_extension_non_decrease",
)
AA_COUNTS = {
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


def independently_decide_nominal(problem):
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
                    "checks": {key: True for key in AA_CHECKS},
                }
            )
            previous = worsts, best
    return {
        "input_sha256": digest(problem),
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "worlds": rows,
        "decisions": decisions,
        "counts": copy.deepcopy(AA_COUNTS),
    }


def nominal_problem(coarse=(1, 1, 1, 1), half=(1, 1, 1, 1), full=(1, 1, 1, 1)):
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


def nominal_signed_problem():
    return nominal_problem(half=(F(7, 8),) * 4, full=(F(1, 2), F(3, 4), F(2, 3), F(1, 4)))


def nominal_tie_problem():
    return nominal_problem(half=(1, F(3, 4), 1, F(1, 2)), full=(F(3, 4), 1, 1, F(1, 2)))


def nominal_global_rule_problem():
    return nominal_problem(half=(F(1, 2), F(3, 2), 1, 1), full=(F(3, 2), F(1, 2), 1, 1))


def nominal_varying_problem():
    p = nominal_problem(coarse=(0, 2, 1, 1), half=(1, 2, 1, 1), full=(1, 1, 1, 1))
    for t, world in enumerate(p["worlds"]):
        for s in range(1, 4):
            world["models"][s]["forecast_risks"][1:] = [
                fw(F(t + 2 * s + 1, 10)),
                fw(F(3 * t + s + 1, 10)),
            ]
    return p


def nominal_shared_problem():
    p = nominal_tie_problem()
    one = [1, 1]
    for world in p["worlds"]:
        world["coarse_risk"] = one
        for model in world["models"]:
            model["forecast_risks"][0] = one
    return p


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_nominals():
    p = nominal_varying_problem()
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


def mutable_ids(value):
    if type(value) not in (dict, list):
        return set()
    result = {id(value)}
    for child in value.values() if type(value) is dict else value:
        result |= mutable_ids(child)
    return result


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


AB_CHECKS = (
    "nominal_selection_preserved",
    "complete_argmax",
    "all_any_quantifiers",
    "signed_bound_comparison",
    "coarse_zero",
    "nested_worlds",
    "world_witnesses_complete",
)
AB_COUNTS = {
    "mechanisms": 2,
    "worlds": 8,
    "assumed_models": 8,
    "rules": 6,
    "certificates": 32,
    "candidate_certificates": 96,
    "stress_risk_cells": 96,
    "baseline_decision_work": 216,
    "stress_excess_terms": 96,
    "candidate_world_visits": 240,
    "shift_terms": 192,
    "candidate_classification_visits": 96,
    "total_work_terms": 840,
}


def wrap(nominal=None, forward=None, reverse=None):
    nominal = nominal_problem() if nominal is None else nominal
    return {
        "schema_version": "det8-qr05ab-problem-v1",
        "family": "qr05ab_replacement_stress",
        "nominal": copy.deepcopy(nominal),
        "mechanisms": [
            {
                "mechanism_id": name,
                "worlds": copy.deepcopy((nominal if source is None else source)["worlds"]),
            }
            for name, source in (("forward", forward), ("reverse", reverse))
        ],
    }


def independently_stress(problem):
    baseline = independently_decide_nominal(problem["nominal"])
    mechanisms, old_evaluations = [], 0
    for mechanism in problem["mechanisms"]:
        worlds = copy.deepcopy(mechanism["worlds"])
        excess = {}
        for world in worlds:
            t, coarse = world["actual_index"], fraction(world["coarse_risk"])
            for model in world["models"]:
                s = model["assumed_index"]
                model["excess_risks"] = []
                for a, risk in enumerate(model["forecast_risks"]):
                    excess[t, s, a] = fraction(risk) - coarse
                    model["excess_risks"].append(fw(excess[t, s, a]))
        certificates = []
        for old in baseline["decisions"]:
            s, bound = old["assumed_index"], old["bound_index"]
            original, value = old["minimizer_indices"], fraction(old["minimax_excess"])
            candidates = []
            for a in range(3):
                ranked = sorted((excess[t, s, a], t) for t in range(bound + 1))
                worst = ranked[-1][0]
                previous = fraction(old["candidates"][a]["worst_excess"])
                candidates.append(
                    {
                        "retained_weight": copy.deepcopy(WEIGHTS[a]),
                        "world_excesses": [fw(excess[t, s, a]) for t in range(bound + 1)],
                        "worst_excess": fw(worst),
                        "worst_world_indices": [t for e, t in ranked if e == worst],
                        "nominal_worst_excess": fw(previous),
                        "worst_shift": fw(worst - previous),
                        "bound_excess": fw(worst - value),
                        "nominal_minimizer": a in original,
                        "coarse_safe": worst <= 0,
                        "strict_benefit": worst < 0,
                        "original_bound_preserved": worst <= value,
                        "unsafe_world_indices": [
                            t for t in range(bound + 1) if excess[t, s, a] > 0
                        ],
                        "bound_breaking_world_indices": [
                            t for t in range(bound + 1) if excess[t, s, a] > value
                        ],
                    }
                )
            safe = [a for a in original if candidates[a]["coarse_safe"]]
            strict = [a for a in original if candidates[a]["strict_benefit"]]
            preserved = [a for a in original if candidates[a]["original_bound_preserved"]]
            old_evaluations += len(original)
            certificates.append(
                {
                    "assumed_index": s,
                    "bound_index": bound,
                    "world_indices": list(range(bound + 1)),
                    "nominal_minimax_excess": fw(value),
                    "old_minimizer_indices": copy.deepcopy(original),
                    "old_minimizer_weights": copy.deepcopy(old["minimizer_weights"]),
                    "candidates": candidates,
                    "safe_old_indices": safe,
                    "strictly_beneficial_old_indices": strict,
                    "bound_preserving_old_indices": preserved,
                    "unsafe_old_indices": [a for a in original if a not in safe],
                    "bound_breaking_old_indices": [a for a in original if a not in preserved],
                    "all_old_safe": safe == original,
                    "any_old_safe": bool(safe),
                    "all_old_strict": strict == original,
                    "any_old_strict": bool(strict),
                    "all_old_bound_preserved": preserved == original,
                    "any_old_bound_preserved": bool(preserved),
                    "checks": {key: True for key in AB_CHECKS},
                }
            )
        mechanisms.append(
            {
                "mechanism_id": mechanism["mechanism_id"],
                "worlds": worlds,
                "certificates": certificates,
            }
        )
    return {
        "input_sha256": digest(problem),
        "baseline": baseline,
        "mechanisms": mechanisms,
        "counts": {**AB_COUNTS, "old_rule_evaluations": old_evaluations},
    }


def tie_switch_problem():
    nominal = nominal_problem(half=(F(1, 2),) * 4, full=(F(1, 2),) * 4)
    forward = nominal_problem(half=(F(3, 4),) * 4, full=(F(5, 4),) * 4)
    reverse = nominal_problem(half=(F(5, 4),) * 4, full=(F(3, 4),) * 4)
    return wrap(nominal, forward, reverse)


def harmful_old_problem():
    return wrap(
        nominal_problem(half=(F(3, 4),) * 4, full=(F(1, 2),) * 4),
        nominal_problem(half=(F(3, 4),) * 4, full=(F(3, 2),) * 4),
    )


def boundary_problem():
    return wrap(
        nominal_problem(half=(F(3, 4),) * 4, full=(F(1, 2),) * 4),
        nominal_problem(full=(F(1, 2), 1, F(3, 2), 0)),
    )


def varying_problem():
    return wrap(
        nominal_problem(full=(F(1, 2),) * 4), nominal_varying_problem(), nominal_signed_problem()
    )


def extreme_problem():
    return wrap(
        nominal_problem(coarse=(2,) * 4, half=(2,) * 4, full=(0,) * 4),
        nominal_problem(coarse=(0,) * 4, half=(0,) * 4, full=(2,) * 4),
    )


def shared_problem():
    p = wrap(nominal_shared_problem())
    p["mechanisms"][0]["worlds"] = p["nominal"]["worlds"]
    p["mechanisms"][1]["worlds"] = p["nominal"]["worlds"]
    return p


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ab_test_primary", "stress.py"),
        private_module("_qr05ab_test_reference", "reference_qr05ab.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ab_test_runner", "study.py")


@pytest.mark.parametrize(
    "builder",
    [
        wrap,
        tie_switch_problem,
        harmful_old_problem,
        boundary_problem,
        varying_problem,
        extreme_problem,
        shared_problem,
    ],
)
def test_generic_full_wire_matches_independent_frozen_candidate_enumeration(executors, builder):
    p = builder()
    wanted, before = independently_stress(p), wire(p)
    for module in executors:
        assert wire(module.analyze(p)) == wire(wanted)
        assert wire(p) == before


def test_every_old_tie_is_frozen_and_per_mechanism_quantifiers_cannot_be_combined(executors):
    for module in executors:
        result = module.analyze(tie_switch_problem())
        forward, reverse = [m["certificates"][3] for m in result["mechanisms"]]
        for cert, safe, unsafe in ((forward, [1], [2]), (reverse, [2], [1])):
            assert cert["old_minimizer_indices"] == [1, 2]
            assert cert["old_minimizer_weights"] == [[1, 2], [1, 1]]
            assert cert["safe_old_indices"] == cert["strictly_beneficial_old_indices"] == safe
            assert cert["unsafe_old_indices"] == unsafe
            assert cert["all_old_safe"] is False and cert["any_old_safe"] is True
            assert cert["all_old_strict"] is False and cert["any_old_strict"] is True
            assert cert["bound_preserving_old_indices"] == []
            assert cert["bound_breaking_old_indices"] == [1, 2]
            assert cert["all_old_bound_preserved"] is cert["any_old_bound_preserved"] is False
            candidate = cert["candidates"][safe[0]]
            assert candidate["worst_excess"] == [-1, 4] and candidate["bound_excess"] == [1, 4]
        assert not set(forward["safe_old_indices"]) & set(reverse["safe_old_indices"])
        assert set(result) == {"input_sha256", "baseline", "mechanisms", "counts"}


def test_safe_unchosen_rule_does_not_rescue_a_harmful_frozen_choice(executors):
    for module in executors:
        cert = module.analyze(harmful_old_problem())["mechanisms"][0]["certificates"][3]
        assert cert["old_minimizer_indices"] == cert["unsafe_old_indices"] == [2]
        assert cert["safe_old_indices"] == [] and cert["any_old_safe"] is False
        assert cert["candidates"][1]["strict_benefit"] is True
        assert cert["candidates"][1]["nominal_minimizer"] is False
        assert cert["candidates"][2]["worst_excess"] == [1, 2]
        assert "minimizer_indices" not in cert


def test_bound_preservation_weak_safety_strict_benefit_and_interior_witnesses_are_distinct(
    executors,
):
    for module in executors:
        certificates = module.analyze(boundary_problem())["mechanisms"][0]["certificates"][:4]
        full = [c["candidates"][2] for c in certificates]
        assert [c["worst_excess"] for c in full] == [[-1, 2], [0, 1], [1, 2], [1, 2]]
        assert [c["original_bound_preserved"] for c in full] == [True, False, False, False]
        assert [c["coarse_safe"] for c in full] == [True, True, False, False]
        assert [c["strict_benefit"] for c in full] == [True, False, False, False]
        assert full[3]["worst_world_indices"] == full[3]["unsafe_world_indices"] == [2]
        assert full[3]["bound_breaking_world_indices"] == [1, 2]
        assert all(all(c["checks"].values()) for c in certificates)


def test_all_worst_world_and_old_rule_ties_are_retained_even_without_survival(executors):
    for module in executors:
        result = module.analyze(
            wrap(nominal_problem(), nominal_tie_problem(), nominal_problem(full=(2,) * 4))
        )
        cert = result["mechanisms"][0]["certificates"][3]
        assert cert["old_minimizer_indices"] == [0, 1, 2]
        assert [c["worst_world_indices"] for c in cert["candidates"]] == [
            list(range(4)),
            [0, 2],
            [1, 2],
        ]
        assert cert["all_old_safe"] is True and cert["any_old_strict"] is False
        assert result["counts"]["old_rule_evaluations"] == 96
        other = result["mechanisms"][1]["certificates"][3]
        assert other["safe_old_indices"] == [0, 1] and other["unsafe_old_indices"] == [2]
        assert other["all_old_safe"] is False and other["any_old_safe"] is True


def test_stressed_coarse_subtraction_precedes_max_and_no_nominal_family_constraints_are_imposed(
    executors,
):
    p = varying_problem()
    for module in executors:
        cert = module.analyze(p)["mechanisms"][0]["certificates"][1]
        assert cert["candidates"][2]["worst_excess"] == [1, 1]
        rows = p["mechanisms"][0]["worlds"][:2]
        wrong = max(fraction(w["models"][0]["forecast_risks"][2]) for w in rows) - max(
            fraction(w["coarse_risk"]) for w in rows
        )
        assert wrong == -1
        assert cert["any_old_safe"] is False


def test_nominal_wire_and_selection_do_not_depend_on_stressed_worlds_mechanism_or_old_survival(
    executors,
):
    p = tie_switch_problem()
    changed = replaced(p, ("mechanisms", 1, "worlds", 3, "models", 2, "forecast_risks", 1), [2, 1])
    for module in executors:
        old, new = module.analyze(p), module.analyze(changed)
        assert (
            wire(old["baseline"])
            == wire(new["baseline"])
            == wire(independently_decide_nominal(p["nominal"]))
        )
        assert wire(old["mechanisms"][0]) == wire(new["mechanisms"][0])
        for i, (a, b) in enumerate(
            zip(
                old["mechanisms"][1]["certificates"],
                new["mechanisms"][1]["certificates"],
                strict=True,
            )
        ):
            if i != 11:
                assert wire(a) == wire(b)
            assert a["old_minimizer_indices"] == b["old_minimizer_indices"]
        assert old["mechanisms"][1]["certificates"][11] != new["mechanisms"][1]["certificates"][11]


def test_new_signed_shifts_reach_both_four_endpoints_without_clipping(executors):
    positive = extreme_problem()
    negative = wrap(
        nominal_problem(coarse=(0,) * 4, half=(0,) * 4, full=(2,) * 4),
        nominal_problem(coarse=(2,) * 4, half=(2,) * 4, full=(0,) * 4),
    )
    for module in executors:
        first = module.analyze(positive)["mechanisms"][0]["certificates"][3]["candidates"][2]
        second = module.analyze(negative)["mechanisms"][0]["certificates"][3]["candidates"][2]
        assert first["worst_shift"] == first["bound_excess"] == [4, 1]
        assert second["worst_shift"] == [-4, 1] and second["bound_excess"] == [-2, 1]
        assert second["nominal_minimizer"] is False


def new_overflow_problem(kind="shift"):
    d = 1 << 4095
    if kind == "shift":
        nominal = nominal_problem(coarse=(0,) * 4, half=(0,) * 4, full=(F(1, d),) * 4)
    else:
        nominal = nominal_problem(coarse=(F(1, d),) * 4, half=(0,) * 4, full=(F(1, d),) * 4)
    return wrap(nominal, nominal_problem(coarse=(0,) * 4, half=(0,) * 4, full=(F(1, 3),) * 4))


@pytest.mark.parametrize("kind", ["shift", "bound"])
def test_new_retained_4097_bit_shift_or_bound_rejects_after_valid_nominal_AA(executors, kind):
    p = new_overflow_problem(kind)
    nominal = independently_decide_nominal(p["nominal"])
    # Every nominal and stressed excess is individually representable.
    native(p)
    for mechanism in p["mechanisms"]:
        for world in mechanism["worlds"]:
            for model in world["models"]:
                for risk in model["forecast_risks"]:
                    fraction(fw(fraction(risk) - fraction(world["coarse_risk"])))
    target = fraction([1, 3]) - fraction(
        nominal["decisions"][0]["candidates"][2]["worst_excess"]
        if kind == "shift"
        else nominal["decisions"][0]["minimax_excess"]
    )
    assert target.denominator.bit_length() == 4097
    for module in executors:
        assert wire(module._analyze_nominal(p["nominal"])) == wire(nominal)
        with pytest.raises(ValueError):
            module.analyze(p)


def test_large_exact_cancellation_preserves_tiny_signed_bound_breaking(executors):
    d = (1 << 4095) - 1
    p = wrap(nominal_problem(full=(F(d - 2, d),) * 4), nominal_problem(full=(F(d - 1, d),) * 4))
    wanted = independently_stress(p)
    for module in executors:
        result = module.analyze(p)
        assert wire(result) == wire(wanted)
        c = result["mechanisms"][0]["certificates"][3]["candidates"][2]
        assert c["worst_excess"] == [-1, d] and c["bound_excess"] == [1, d]
        assert c["strict_benefit"] is True and c["original_bound_preserved"] is False


def invalid_problems():
    p = wrap(nominal_varying_problem())
    bad = [None, [], True, DictChild(p)]
    bad.extend(replaced(p, ("nominal",), value) for value in invalid_nominals())
    for key in p:
        item = p.copy()
        del item[key]
        bad.append(item)
    for key in ("extra", "selector", "minimizer_indices", "artifact", "stress_optimizer"):
        bad.append({**p, key: 0})
    bad.extend(
        replaced(p, ("schema_version",), value)
        for value in ("wrong", StrChild(p["schema_version"]), None)
    )
    bad.extend(replaced(p, ("family",), value) for value in ("wrong", StrChild(p["family"]), False))
    mechanisms = p["mechanisms"]
    for value in (
        [],
        mechanisms[:1],
        mechanisms + [mechanisms[0]],
        mechanisms[::-1],
        tuple(mechanisms),
        ListChild(mechanisms),
    ):
        bad.append(replaced(p, ("mechanisms",), value))
    for k in range(2):
        m = mechanisms[k]
        for value in (
            {"worlds": m["worlds"]},
            {"mechanism_id": m["mechanism_id"]},
            {**m, "extra": 0},
            DictChild(m),
            [],
        ):
            bad.append(replaced(p, ("mechanisms", k), value))
        for value in (
            "other",
            "reverse" if k == 0 else "forward",
            StrChild(m["mechanism_id"]),
            None,
        ):
            bad.append(replaced(p, ("mechanisms", k, "mechanism_id"), value))
    worlds = p["mechanisms"][1]["worlds"]
    for value in (
        [],
        worlds[:3],
        worlds + [worlds[0]],
        worlds[::-1],
        tuple(worlds),
        ListChild(worlds),
    ):
        bad.append(replaced(p, ("mechanisms", 1, "worlds"), value))
    last = ("mechanisms", 1, "worlds", 3)
    for path, values in (
        (("actual_index",), [True, IntChild(3), 3.0, -1, 2]),
        (
            ("models",),
            [
                [],
                worlds[3]["models"][:3],
                worlds[3]["models"][::-1],
                ListChild(worlds[3]["models"]),
            ],
        ),
        (("models", 3, "assumed_index"), [True, IntChild(3), 3.0, 2]),
        (("coarse_risk",), [[0, 2], [3, 1], [False, 1], (1, 1)]),
        (("models", 3, "forecast_risks"), [[], [[0, 1]], ListChild([[1, 1]] * 3)]),
        (
            ("models", 3, "forecast_risks", 2),
            [
                [2, 4],
                [1, 0],
                [-1, 2],
                [3, 1],
                [True, 1],
                [1.0, 2],
                [IntChild(1), 2],
                (1, 2),
                [1, 1 << 4096],
            ],
        ),
    ):
        bad.extend(replaced(p, last + path, value) for value in values)
    bad.append(
        replaced(p, ("mechanisms", 1, "worlds", 0, "models", 3, "forecast_risks", 0), [1, 1])
    )
    item = p.copy()
    item[StrChild("family")] = item.pop("family")
    bad.extend([item, {**p, 1: None}])
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_nominal_and_stress_native_schemas_reject_without_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def test_new_work_caps_and_last_stress_schema_precede_all_nominal_and_stress_arithmetic(
    executors, monkeypatch
):
    p = tie_switch_problem()
    for module in executors:
        calls = {"_difference": 0, "_shift": 0}
        with monkeypatch.context() as patched:
            for name in calls:
                original = getattr(module, name)

                def observed(*args, original=original, name=name, calls=calls):
                    calls[name] += 1
                    return original(*args)

                patched.setattr(module, name, observed)
            a = module.analyze(p)
        assert calls == {"_difference": 144, "_shift": 192}
        assert a["counts"] == {**AB_COUNTS, "old_rule_evaluations": 64}
        for constant, cap in (
            ("MAX_RISK_CELLS", 48),
            ("MAX_DECISION_WORK", 216),
            ("MAX_STRESS_RISK_CELLS", 96),
            ("MAX_TOTAL_WORK", 840),
        ):

            def forbidden(*_args):
                raise RuntimeError("nominal or stressed arithmetic preceded full AB preflight")

            with monkeypatch.context() as patched:
                patched.setattr(module, constant, cap - 1)
                for name in ("_difference", "_shift", "_analyze_nominal"):
                    patched.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        bad = replaced(p, ("mechanisms", 1, "worlds", 3, "models", 3, "forecast_risks", 2), [2, 4])
        with monkeypatch.context() as patched:
            for name in ("_difference", "_shift", "_analyze_nominal"):
                patched.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(bad)


@pytest.mark.parametrize(
    "constant",
    [
        "MAX_BITS",
        "MAX_DEPTH",
        "MAX_NODES",
        "MAX_BYTES",
        "MAX_RISK_CELLS",
        "MAX_DECISION_WORK",
        "MAX_STRESS_RISK_CELLS",
        "MAX_TOTAL_WORK",
    ],
)
def test_all_eight_live_caps_reject_without_truncation_or_cross_call_cache(
    executors, monkeypatch, constant
):
    p = tie_switch_problem()
    for module in executors:
        before = wire(module.analyze(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == before


def test_entire_baseline_and_certificates_are_detached_from_shared_input_and_other_calls(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        first, second = module.analyze(p), module.analyze(p)
        wanted = wire(second)
        assert wanted == wire(independently_stress(p))
        assert mutable_ids(p).isdisjoint(mutable_ids(first))
        assert mutable_ids(first).isdisjoint(mutable_ids(second))
        first["baseline"]["worlds"][0]["models"][0]["forecast_risks"][0][0] = -1
        first["mechanisms"][0]["certificates"][0]["old_minimizer_weights"][0][0] = -1
        assert wire(p) == before and wire(second) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["mechanisms"][0]["worlds"][0]["models"][0]["forecast_risks"][2] = [2, 1]
        assert wire(detached) == wanted
        assert wire(module.analyze(changed)) != wanted


def test_native_scalar_empty_shared_depth_node_and_exact_ascii_boundaries(executors, monkeypatch):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    for module in executors:
        for boundary in (nested(0, 128), nested([], 128)):
            module._native(boundary)
        for boundary in (nested(0, 129), nested([], 129)):
            with pytest.raises(ValueError):
                module._native(boundary)
        shared = [0]
        module._native([shared, nested(shared, 126)])
        with pytest.raises(ValueError):
            module._native([shared, nested(shared, 127)])
        for constant, limit in (
            ("MAX_NODES", 8),
            ("MAX_DEPTH", 2),
            ("MAX_BYTES", len(wire(value))),
        ):
            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit)
                module._native(value)
                patched.setattr(module, constant, limit - 1)
                with pytest.raises(ValueError):
                    module._native(value)


def test_complete_wrapper_resources_precede_whole_serialization_and_output_has_separate_byte_limit(
    executors, monkeypatch
):
    p = shared_problem()
    nodes, depth = tree_resources(p)
    for module in executors:
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("outer tree reached serialization before native rejection")

            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit)
                patched.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        wanted = wire(module.analyze(p))
        assert len(wanted) > len(wire(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, "MAX_BYTES", len(wanted) - 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        with monkeypatch.context() as patched:
            patched.setattr(module, "MAX_BYTES", len(wanted))
            assert wire(module.analyze(p)) == wanted


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
    paths = [("nominal",), ("mechanisms",), ("mechanisms", 1), ("mechanisms", 1, "mechanism_id")]
    for prefix in (("nominal",), ("mechanisms", 1)):
        paths.extend(
            prefix + path
            for path in (
                ("worlds",),
                ("worlds", 0),
                ("worlds", 0, "coarse_risk"),
                ("worlds", 0, "models"),
                ("worlds", 0, "models", 0, "forecast_risks"),
                ("worlds", 0, "models", 0, "forecast_risks", 0),
            )
        )
    for path in paths:
        yield replaced(valid, path, dag)


def test_generic_json_auditor_matches_full_baseline_signed_statuses_and_complete_witnesses():
    audit = private_module("_qr05ab_test_audit_generic", "audit_json.py")
    for p in (tie_switch_problem(), boundary_problem(), varying_problem(), extreme_problem()):
        before = wire(p)
        assert wire(audit.expected_ab(p)) == wire(independently_stress(p))
        assert wire(p) == before


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_wrapper_native_work_and_detachment_guards_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (15, 15))
spec = importlib.util.spec_from_file_location("_qr05ab_guard_helpers", Path(sys.argv[1]))
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
for index, filename in enumerate(("stress.py", "reference_qr05ab.py")):
    module = helpers.private_module("_qr05ab_guard_core_" + str(index), filename)
    for builder in (helpers.tie_switch_problem, helpers.harmful_old_problem, helpers.boundary_problem, helpers.extreme_problem):
        p = builder()
        require(helpers.wire(module.analyze(p)) == helpers.wire(helpers.independently_stress(p)), "complete generic frozen certificate wire")
    reference = module.analyze(valid)
    for bad in invalid:
        reject(module.analyze, bad)
    graphs = list(helpers.graph_inputs(valid))
    require(len(graphs) == 20, "native graph placement inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)
    for constant, cap in (("MAX_RISK_CELLS",48), ("MAX_DECISION_WORK",216), ("MAX_STRESS_RISK_CELLS",96), ("MAX_TOTAL_WORK",840)):
        old_cap = getattr(module, constant)
        old_helpers = {name:getattr(module,name) for name in ("_difference","_shift","_analyze_nominal")}
        def forbidden(*args):
            raise RuntimeError("nominal or stress work began before full AB preflight")
        setattr(module, constant, cap - 1)
        for name in old_helpers:
            setattr(module, name, forbidden)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old_cap)
            for name, value in old_helpers.items():
                setattr(module, name, value)
    for constant in ("MAX_RISK_CELLS","MAX_DECISION_WORK","MAX_STRESS_RISK_CELLS","MAX_TOTAL_WORK","MAX_BITS","MAX_DEPTH","MAX_NODES","MAX_BYTES"):
        old = getattr(module, constant)
        setattr(module, constant, 1)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old)
    old_helpers = {name:getattr(module,name) for name in ("_difference","_shift","_analyze_nominal")}
    for name in old_helpers:
        setattr(module, name, forbidden)
    try:
        bad = helpers.replaced(valid,("mechanisms",1,"worlds",3,"models",3,"forecast_risks",2),[2,4])
        reject(module.analyze, bad)
    finally:
        for name, value in old_helpers.items():
            setattr(module,name,value)
    for kind in ("shift","bound"):
        p = helpers.new_overflow_problem(kind)
        require(module._analyze_nominal(p["nominal"]) == helpers.independently_decide_nominal(p["nominal"]), "overflow fixture nominal was not valid")
        reject(module.analyze,p)
    for value in (helpers.nested(0,128),helpers.nested([],128)):
        module._native(value)
    for value in (helpers.nested(0,129),helpers.nested([],129)):
        reject(module._native,value)
    shared = [0]
    module._native([shared,helpers.nested(shared,126)])
    reject(module._native,[shared,helpers.nested(shared,127)])
    require(module.analyze(valid) == helpers.independently_stress(valid), "sharing or cap restoration failed")
    reference["baseline"]["worlds"][0]["models"][0]["forecast_risks"][0][0] = -1
    require(module.analyze(valid)["baseline"]["worlds"][0]["models"][0]["forecast_risks"][0] == [1,1], "baseline ownership failed")
runner = helpers.private_module("_qr05ab_guard_runner","study.py")
for bad in helpers.graph_inputs(valid):
    reject_before_dump(runner.require_wire,bad)
for value in (helpers.nested(0,129),helpers.nested([],129)):
    reject(runner.require_wire,value)
shared = [0]
runner.require_wire([shared,helpers.nested(shared,126)])
reject(runner.require_wire,[shared,helpers.nested(shared,127)])
reject(lambda value:runner.require_same_wire({"x":0},value,"typed regression"),{"x":False})
require(before_serialization == 60,"pre-serialization inventory")
require(rejections == 2*(len(invalid)+38)+24,"explicit rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":before_serialization,
                  "invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ab.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=25, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 38) + 24,
        "pre_serialization_rejections": 60,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


PINS = {
    "aa": (
        "qr-05aa-uncertainty-decisions-2026-09-07",
        112206,
        "bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424",
    ),
    "z": (
        "qr-05z-fixed-attenuation-2026-09-07",
        31075315,
        "7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc",
    ),
    "w": (
        "qr-05w-noisy-readouts-2026-09-07",
        6756094,
        "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a",
    ),
}
PRODUCER_CONTROLS = {
    "nominal_AA_baseline_preserved": True,
    "whole_model_positive_rank_tilts": True,
    "complete_stressed_laws_and_support": True,
    "frozen_forecasts_and_weights": True,
    "literal_original_weight_risks": True,
    "clean_and_N_future_marginals_preserved": True,
    "affine_actual_joint_and_risk": True,
    "opposite_tilts_average_to_nominal": True,
    "full_replacement_tilted_quadratic_penalty": True,
    "upper_endpoint_and_opposite_bound_deviations": True,
    "all_original_ties_classified_without_reoptimization": True,
    "origin_authenticated_by_generic_API": False,
    "raw_history_reconstruction_performed_by_this_runner": False,
}


@pytest.fixture(scope="session")
def pinned():
    answer = {}
    for name, (directory, size, sha) in PINS.items():
        path = HERE.parent / directory / "results.json"
        assert path.is_file() and not path.is_symlink()
        raw = path.read_bytes()
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == sha
        envelope = json.loads(raw)
        assert (
            json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
        ).encode() == raw
        native(envelope["suite"])
        answer[name] = envelope["suite"]
    return answer


def replacement_laws(wsuite):
    distinct = {}
    for label in wsuite["model"]["labels"]:
        q = tuple(label["question"])
        distinct.setdefault(q[:5], set()).add(q)
    mechanisms = []
    for reverse, name in enumerate(("forward", "reverse")):
        alphabet = []
        for n, values in sorted(distinct.items()):
            ordered = sorted(values)
            m = len(ordered)
            alphabet.append(
                {
                    "N": list(n),
                    "values": [
                        {
                            "value": list(q),
                            "probability": fw(F(2 * (m - r if reverse else r + 1), m * (m + 1))),
                        }
                        for r, q in enumerate(ordered)
                    ],
                }
            )
        mechanisms.append({"mechanism_id": name, "alphabet": alphabet})
    return mechanisms


def read_law(rows):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in rows}


def law_wire(law):
    return [{"value": list(q), "probability": fw(p)} for q, p in sorted(law.items()) if p]


def outcome_risk(actual, forecast):
    assert sum(actual.values()) == sum(forecast.values()) == 1
    coordinates = actual.keys() | forecast.keys()
    return sum(
        probability * sum((forecast.get(q, F(0)) - (q == truth)) ** 2 for q in coordinates)
        for truth, probability in actual.items()
    )


def channel_joints(channel):
    return {
        (tuple(cell["value"]), tuple(atom["value"])): fraction(cell["probability"])
        * fraction(atom["probability"])
        for cell in channel["cells"]
        for atom in cell["prediction"]
    }


def tilted_channels(clean, alphabet):
    """Apply the stochastic matrix to each clean source atom individually."""
    mu = {tuple(row["N"]): read_law(row["values"]) for row in alphabet}
    channels = []
    for level in LEVELS:
        t, joint = fraction(level), {}
        for source in clean["cells"]:
            b, mass = tuple(source["value"]), fraction(source["probability"])
            for z, replacement in mu[b[:5]].items():
                chance = (1 - t if z == b else F(0)) + t * replacement
                for q, probability in read_law(source["prediction"]).items():
                    joint[z, q] = joint.get((z, q), F(0)) + mass * chance * probability
        cells = []
        for z in sorted({z for (z, _), p in joint.items() if p}):
            sublaw = {q: p for (r, q), p in joint.items() if r == z and p}
            mass = sum(sublaw.values())
            cells.append(
                {
                    "value": list(z),
                    "probability": fw(mass),
                    "prediction": law_wire({q: p / mass for q, p in sublaw.items()}),
                }
            )
        assert sum(fraction(c["probability"]) for c in cells) == 1
        channels.append({"level": copy.deepcopy(level), "cells": cells})
    return channels


def project_case(aacase, zcase, laws):
    assert aacase["case_id"] == zcase["case_id"]
    source = zcase["problem"]["experiment"]["beliefs"]
    zrows = zcase["analysis"]["beliefs"]
    mechanisms, stress_laws = [], []
    for mechanism in laws:
        rows = []
        risks = {(t, s, a): F(0) for t in range(4) for s in range(4) for a in range(3)}
        coarse = {t: F(0) for t in range(4)}
        for belief, zrow in zip(source, zrows, strict=True):
            assert belief["belief_id"] == zrow["belief_id"] and belief["weight"] == zrow["weight"]
            weight = fraction(belief["weight"])
            channels = tilted_channels(belief["channels"][0], mechanism["alphabet"])
            rows.append(
                {
                    "belief_id": belief["belief_id"],
                    "weight": copy.deepcopy(belief["weight"]),
                    "channels": channels,
                }
            )
            fallback = {
                tuple(row["value"]): read_law(row["prediction"]) for row in belief["fallbacks"]
            }
            maps = [
                {
                    tuple(c["value"]): [read_law(b["forecast"]) for b in c["blends"]]
                    for c in zrow["pairs"][12 + s]["cells"]
                }
                for s in range(4)
            ]
            for t, channel in enumerate(channels):
                for cell in channel["cells"]:
                    z = tuple(cell["value"])
                    mass = fraction(cell["probability"])
                    truth, g = read_law(cell["prediction"]), fallback[z[:5]]
                    coarse[t] += weight * mass * outcome_risk(truth, g)
                    for s in range(4):
                        assert maps[s][z][0] == g
                        for a in range(3):
                            risks[t, s, a] += weight * mass * outcome_risk(truth, maps[s][z][a])
        worlds = [
            {
                "actual_index": t,
                "coarse_risk": fw(coarse[t]),
                "models": [
                    {"assumed_index": s, "forecast_risks": [fw(risks[t, s, a]) for a in range(3)]}
                    for s in range(4)
                ],
            }
            for t in range(4)
        ]
        mechanisms.append({"mechanism_id": mechanism["mechanism_id"], "worlds": worlds})
        stress_laws.append({"mechanism_id": mechanism["mechanism_id"], "beliefs": rows})
    p = {
        "schema_version": "det8-qr05ab-problem-v1",
        "family": "qr05ab_replacement_stress",
        "nominal": copy.deepcopy(aacase["problem"]),
        "mechanisms": mechanisms,
    }
    return {"case_id": aacase["case_id"], "problem": p, "stress_laws": stress_laws}


@pytest.fixture(scope="session")
def laws(pinned):
    return replacement_laws(pinned["w"])


@pytest.fixture(scope="session")
def projected(pinned, laws):
    return [
        project_case(a, z, laws)
        for a, z in zip(pinned["aa"]["cases"], pinned["z"]["cases"], strict=True)
    ]


@pytest.fixture(scope="session")
def expected(projected):
    return [independently_stress(row["problem"]) for row in projected]


@pytest.mark.parametrize("case_index", range(6))
def test_fixed_six_complete_wires_and_nominal_baselines_match_independent_channel_risk_certificate_oracle(
    executors, pinned, projected, expected, case_index
):
    row, wanted = projected[case_index], expected[case_index]
    assert wire(wanted["baseline"]) == wire(pinned["aa"]["cases"][case_index]["analysis"])
    before = wire(row["problem"])
    for module in executors:
        assert wire(module.analyze(row["problem"])) == wire(wanted)
        assert wire(row["problem"]) == before


def test_fixed_whole_model_alphabet_rank_tilts_include_zero_prior_labels_and_singletons(
    pinned, laws
):
    expected_labels = {tuple(label["question"]) for label in pinned["w"]["model"]["labels"]}
    assert len(expected_labels) == 93
    assert [m["mechanism_id"] for m in laws] == ["forward", "reverse"]
    for m in laws:
        assert len(m["alphabet"]) == 72
        assert {
            tuple(atom["value"]) for row in m["alphabet"] for atom in row["values"]
        } == expected_labels
        assert [row["N"] for row in m["alphabet"]] == sorted(row["N"] for row in m["alphabet"])
    for forward, reverse in zip(laws[0]["alphabet"], laws[1]["alphabet"], strict=True):
        f, r = read_law(forward["values"]), read_law(reverse["values"])
        assert sum(f.values()) == sum(r.values()) == 1
        assert all(p > 0 for p in f.values()) and all(p > 0 for p in r.values())
        assert list(f) == list(r) == sorted(f)
        for q in f:
            assert (f[q] + r[q]) / 2 == F(1, len(f))
        if len(f) == 1:
            assert f == r


def marginal(joint):
    result = {}
    for (report, future), mass in joint.items():
        key = report[:5], future
        result[key] = result.get(key, F(0)) + mass
    return result


def test_fixed_complete_stress_joint_laws_support_original_weights_and_opposite_tilt_identities(
    pinned, projected, expected
):
    for zcase, projection, result in zip(pinned["z"]["cases"], projected, expected, strict=True):
        sources = zcase["problem"]["experiment"]["beliefs"]
        forward, reverse = projection["stress_laws"]
        for source, f, r in zip(sources, forward["beliefs"], reverse["beliefs"], strict=True):
            assert source["weight"] == f["weight"] == r["weight"]
            assert source["belief_id"] == f["belief_id"] == r["belief_id"]
            clean = channel_joints(source["channels"][0])
            for output in (f, r):
                assert wire(output["channels"][0]) == wire(source["channels"][0])
                full = channel_joints(output["channels"][3])
                for t, channel in enumerate(output["channels"]):
                    joint = channel_joints(channel)
                    assert marginal(joint) == marginal(clean)
                    if t:
                        assert [c["value"] for c in channel["cells"]] == [
                            c["value"] for c in source["channels"][t]["cells"]
                        ]
                    rate = fraction(LEVELS[t])
                    assert all(
                        joint.get(key, 0)
                        == (1 - rate) * clean.get(key, 0) + rate * full.get(key, 0)
                        for key in joint.keys() | clean.keys() | full.keys()
                    )
            for t in range(4):
                left, right, nominal = [channel_joints(c["channels"][t]) for c in (f, r, source)]
                assert all(
                    (left.get(key, 0) + right.get(key, 0)) / 2 == nominal.get(key, 0)
                    for key in left.keys() | right.keys() | nominal.keys()
                )
        for s in range(4):
            for bound in range(4):
                nominal = result["baseline"]["decisions"][4 * s + bound]
                f, r = [m["certificates"][4 * s + bound] for m in result["mechanisms"]]
                assert (
                    f["old_minimizer_indices"]
                    == r["old_minimizer_indices"]
                    == nominal["minimizer_indices"]
                )
                for a in range(3):
                    fc, rc, nc = f["candidates"][a], r["candidates"][a], nominal["candidates"][a]
                    assert bound in fc["worst_world_indices"] and bound in rc["worst_world_indices"]
                    assert (
                        fraction(fc["worst_excess"]) + fraction(rc["worst_excess"])
                    ) / 2 == fraction(nc["worst_excess"])
                    if a in nominal["minimizer_indices"]:
                        assert fraction(fc["bound_excess"]) + fraction(rc["bound_excess"]) == 0
                        assert (
                            fc["original_bound_preserved"] and rc["original_bound_preserved"]
                        ) == (fc["bound_excess"] == rc["bound_excess"] == [0, 1])


def test_generic_direct_channel_preserves_unnormalized_N_mass_and_zero_prior_labels(runner):
    a0, a1, a2 = [tuple([0] * 6 + [i]) for i in range(3)]
    b0 = (1, 0, 0, 0, 0, 0, 0)
    q0, q1, q2 = a0, a1, a2
    clean = {
        "level": [0, 1],
        "cells": [
            {"value": list(a0), "probability": [1, 12], "prediction": law_wire({q0: F(1)})},
            {"value": list(a1), "probability": [1, 6], "prediction": law_wire({q1: F(1)})},
            {"value": list(b0), "probability": [3, 4], "prediction": law_wire({q2: F(1)})},
        ],
    }
    alphabet = [
        {"N": list(a0[:5]), "values": law_wire({a0: F(1, 6), a1: F(1, 3), a2: F(1, 2)})},
        {"N": list(b0[:5]), "values": law_wire({b0: F(1)})},
    ]
    joints = channel_joints(clean)
    n_joint = runner.n_subjoints(joints)
    assert sum(n_joint[a0[:5]].values()) == F(1, 4)
    assert sum(n_joint[b0[:5]].values()) == F(3, 4)
    mu = {tuple(row["N"]): read_law(row["values"]) for row in alphabet}
    independently_pushed = tilted_channels(clean, alphabet)
    for t, expected_channel in zip(LEVELS, independently_pushed, strict=True):
        assert wire(runner.pushed_channel(joints, n_joint, mu, fraction(t))) == wire(
            expected_channel
        )
    assert wire(independently_pushed[0]) == wire(clean)
    full = {tuple(c["value"]): c for c in independently_pushed[3]["cells"]}
    assert [full[q]["probability"] for q in (a0, a1, a2, b0)] == [[1, 24], [1, 12], [1, 8], [3, 4]]
    assert all(read_law(full[q]["prediction"]) == {q0: F(1, 3), q1: F(2, 3)} for q in (a0, a1, a2))
    tiny = F(1, 1 << 128)
    pushed = runner.pushed_channel(joints, n_joint, mu, tiny)
    added = next(c for c in pushed["cells"] if tuple(c["value"]) == a2)
    assert fraction(added["probability"]) == tiny / 8
    reverse = copy.deepcopy(alphabet)
    reverse[0]["values"] = law_wire({a0: F(1, 2), a1: F(1, 3), a2: F(1, 6)})
    uniform = copy.deepcopy(alphabet)
    uniform[0]["values"] = law_wire({a0: F(1, 3), a1: F(1, 3), a2: F(1, 3)})
    f, r, nominal = [tilted_channels(clean, law)[1] for law in (alphabet, reverse, uniform)]
    conditionals = [
        read_law(next(c for c in channel["cells"] if tuple(c["value"]) == a0)["prediction"])[q0]
        for channel in (f, r, nominal)
    ]
    assert conditionals == [F(7, 9), F(3, 5), F(2, 3)]
    assert (conditionals[0] + conditionals[1]) / 2 != conditionals[2]
    left, right, middle = map(channel_joints, (f, r, nominal))
    assert all(
        (left.get(key, 0) + right.get(key, 0)) / 2 == middle.get(key, 0)
        for key in left.keys() | right.keys() | middle.keys()
    )


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_runner_complete_projection_laws_baseline_controls_and_inventory(
    runner, pinned, laws, projected, expected, aggregate
):
    assert set(aggregate) == {
        "producer",
        "replacement_laws",
        "cases",
        "independent_route_equal",
        "public_controls",
        "totals",
    }
    directory, size, sha = PINS["aa"]
    assert aggregate["producer"] == {
        "artifact": directory + "/results.json",
        "bytes": size,
        "sha256": sha,
    }
    assert aggregate["independent_route_equal"] is True
    assert aggregate["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        "raw_laws_histories_or_artifacts_given_to_core": False,
        "forecasts_refitted": False,
        "stressed_rules_reoptimized": False,
        "old_ties_selected_retrospectively": False,
        "mechanisms_combined": False,
    }
    counts = {key: sum(a["counts"][key] for a in expected) for key in expected[0]["counts"]}
    assert aggregate["totals"] == {
        "cases": 6,
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        **counts,
    }
    assert (
        wire(aggregate["replacement_laws"])
        == wire(laws)
        == wire(runner.replacement_laws(pinned["w"]))
    )
    assert wire(runner.fixtures()) == wire(pinned)
    for aa, z, p, wanted, actual in zip(
        pinned["aa"]["cases"],
        pinned["z"]["cases"],
        projected,
        expected,
        aggregate["cases"],
        strict=True,
    ):
        assert set(actual) == {"case_id", "problem", "analysis", "stress_laws", "producer_controls"}
        assert wire({key: actual[key] for key in ("case_id", "problem", "stress_laws")}) == wire(p)
        assert wire(actual["analysis"]) == wire(wanted)
        assert wire(actual["producer_controls"]) == wire(PRODUCER_CONTROLS)
        assert wire(runner.project_case(aa, z, laws)) == wire(p)


def output_corruptions(analysis):
    bad = []

    def add(path, value):
        changed = replaced(analysis, path, value)
        assert wire(changed) != wire(analysis)
        bad.append(changed)

    add(("input_sha256",), "0" * 64)
    add(("baseline", "decisions", 3, "minimizer_indices"), [])
    prefix = ("mechanisms", 0, "certificates", 3)
    add(prefix + ("old_minimizer_indices",), [])
    add(prefix + ("nominal_minimax_excess",), [1, 1])
    add(prefix + ("candidates", 0, "worst_world_indices"), [3])
    add(prefix + ("candidates", 0, "world_excesses"), [[1, 1]] * 4)
    add(prefix + ("candidates", 0, "worst_shift"), [1, 1])
    add(prefix + ("candidates", 0, "bound_excess"), [1, 1])
    add(prefix + ("candidates", 0, "unsafe_world_indices"), [0])
    add(prefix + ("candidates", 0, "bound_breaking_world_indices"), [0])
    add(
        prefix + ("all_old_safe",), not analysis["mechanisms"][0]["certificates"][3]["all_old_safe"]
    )
    add(
        prefix + ("any_old_bound_preserved",),
        not analysis["mechanisms"][0]["certificates"][3]["any_old_bound_preserved"],
    )
    add(prefix + ("checks", "all_any_quantifiers"), False)
    add(("counts", "old_rule_evaluations"), -1)
    add(("counts", "total_work_terms"), 839)
    return bad


def test_fixed_runner_rejects_nonvacuous_full_certificate_baseline_quantifier_and_work_corruption(
    runner, pinned, laws, projected, expected, monkeypatch
):
    aa, z, p, wanted = pinned["aa"]["cases"][0], pinned["z"]["cases"][0], projected[0], expected[0]
    # Projection correctness is separately checked in full; here isolate the
    # complete-wire checker without repeating law reconstruction for each edit.
    with monkeypatch.context() as patched:
        patched.setattr(runner, "project_case", lambda *_args: copy.deepcopy(p))
        for bad in output_corruptions(wanted):
            with pytest.raises(ValueError):
                runner.check_analysis(bad, aa, z, laws, p["stress_laws"])


def test_fixed_runner_rejects_nonvacuous_AA_source_forecast_weight_and_actual_law_corruption(
    runner, pinned, laws, projected, expected
):
    aa, z, p, wanted = pinned["aa"]["cases"][0], pinned["z"]["cases"][0], projected[0], expected[0]
    evidence = p["stress_laws"]
    args = [aa, z, evidence]
    corruptions = [
        (0, ("analysis", "decisions", 3, "minimizer_indices"), []),
        (
            1,
            (
                "analysis",
                "beliefs",
                0,
                "pairs",
                12,
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
        (1, ("problem", "experiment", "beliefs", 0, "weight"), [0, 1]),
        (2, (0, "beliefs", 0, "channels", 1, "cells", 0, "probability"), [0, 1]),
        (2, (1, "beliefs", 0, "channels", 1, "cells", 0, "prediction", 0, "probability"), [0, 1]),
        (2, (1, "beliefs", 0, "weight"), [0, 1]),
    ]
    for index, path, value in corruptions:
        changed = replaced(args[index], path, value)
        assert wire(changed) != wire(args[index])
        call = args.copy()
        call[index] = changed
        with pytest.raises(ValueError):
            runner.check_analysis(wanted, call[0], call[1], laws, call[2])
