"""Independent closed-simplex envelope and canonical-witness controls.

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


AC_CHECKS = (
    "nominal_selection_preserved",
    "complete_envelope_argmax",
    "complete_mechanism_faces",
    "global_witness_attains_envelope",
    "witness_argmax_complete",
    "full_support_attainment",
    "all_any_quantifiers",
    "signed_bound_comparison",
    "coarse_zero",
    "nested_worlds",
)


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


def marginal(joint):
    result = {}
    for (report, future), mass in joint.items():
        key = report[:5], future
        result[key] = result.get(key, F(0)) + mass
    return result


def work_counts(problem):
    fibers = len(problem["alphabet"])
    labels = sum(len(row["values"]) for row in problem["alphabet"])
    return {
        "fibers": fibers,
        "labels": labels,
        "assumed_models": 4,
        "rules": 3,
        "certificates": 16,
        "candidate_certificates": 48,
        "nominal_risk_cells": 48,
        "coefficient_cells": 12 * labels,
        "baseline_decision_work": 216,
        "profile_coefficient_visits": 12 * labels,
        "profile_fiber_terms": 12 * fibers,
        "world_envelope_terms": 48,
        "candidate_world_visits": 120,
        "face_label_visits": 48 * labels,
        "witness_coefficient_terms": 48 * fibers,
        "witness_world_terms": 120,
        "shift_terms": 96,
        "candidate_classifications": 48,
        "total_work_terms": 648 + 60 * labels + 60 * fibers,
    }


def problem_of(nominal=None, coefficients=None, sizes=(2,)):
    alphabet = [
        {"N": [n, 0, 0, 0, 0], "values": [[n, 0, 0, 0, 0, 0, z] for z in range(size)]}
        for n, size in enumerate(sizes)
    ]
    if coefficients is None:
        coefficients = [[[0, 0, 0] for _ in row["values"]] for row in alphabet]
    return {
        "schema_version": "det8-qr05ac-problem-v1",
        "family": "qr05ac_replacement_envelope",
        "nominal": copy.deepcopy(nominal_problem() if nominal is None else nominal),
        "alphabet": alphabet,
        "models": [
            {
                "assumed_index": s,
                "full_coefficients": [
                    [[fw(value) for value in values] for values in fiber] for fiber in coefficients
                ],
            }
            for s in range(4)
        ],
    }


def curve_problem(clean, coefficients, sizes=(2,)):
    coarse = max(F(0), -F(clean))
    nominal = nominal_problem(coarse=(coarse,) * 4, half=(coarse,) * 4, full=(coarse + clean,) * 4)
    return problem_of(nominal, [[[0, 0, value] for value in row] for row in coefficients], sizes)


def independently_envelope(problem):
    baseline = independently_decide_nominal(problem["nominal"])
    profiles, curves = [], []
    for s, model in enumerate(problem["models"]):
        for a in range(3):
            clean = fraction(baseline["worlds"][0]["models"][s]["excess_risks"][a])
            fibers, upper, flat = [], F(0), True
            for shape, coefficients in zip(
                problem["alphabet"], model["full_coefficients"], strict=True
            ):
                ranked = sorted((fraction(row[a]), z) for z, row in enumerate(coefficients))
                maximum = ranked[-1][0]
                indices = [z for value, z in ranked if value == maximum]
                fibers.append(
                    {
                        "N": copy.deepcopy(shape["N"]),
                        "maximum": fw(maximum),
                        "maximizer_indices": indices,
                    }
                )
                upper += maximum
                flat &= len(indices) == len(shape["values"])
            profiles.append(
                {
                    "assumed_index": s,
                    "retained_weight": copy.deepcopy(WEIGHTS[a]),
                    "clean_excess": fw(clean),
                    "full_upper_excess": fw(upper),
                    "fibers": fibers,
                    "all_fibers_flat": flat,
                }
            )
            curves.append([(1 - fraction(t)) * clean + fraction(t) * upper for t in LEVELS])
    certificates, old_slots = [], 0
    for nominal in baseline["decisions"]:
        s, u = nominal["assumed_index"], nominal["bound_index"]
        worlds, original = list(range(u + 1)), nominal["minimizer_indices"]
        bound = fraction(nominal["minimax_excess"])
        candidates = []
        for a in range(3):
            k = 3 * s + a
            profile = profiles[k]
            values = curves[k][: u + 1]
            ranked = sorted((value, t) for t, value in enumerate(values))
            worst = ranked[-1][0]
            maxima = [t for value, t in ranked if value == worst]
            face = [
                list(range(len(row["values"])))
                if 0 in maxima
                else copy.deepcopy(p["maximizer_indices"])
                for row, p in zip(problem["alphabet"], profile["fibers"], strict=True)
            ]
            witness = [indices[0] for indices in face]
            witness_full = sum(
                fraction(problem["models"][s]["full_coefficients"][n][z][a])
                for n, z in enumerate(witness)
            )
            clean = fraction(profile["clean_excess"])
            witness_values = [
                (1 - fraction(LEVELS[t])) * clean + fraction(LEVELS[t]) * witness_full
                for t in worlds
            ]
            witness_worst = max(witness_values)
            assert witness_worst == worst
            attained = 0 in maxima or profile["all_fibers_flat"]
            previous = fraction(nominal["candidates"][a]["worst_excess"])
            candidates.append(
                {
                    "retained_weight": copy.deepcopy(WEIGHTS[a]),
                    "profile_index": k,
                    "world_upper_excesses": [fw(v) for v in values],
                    "worst_excess": fw(worst),
                    "worst_world_indices": maxima,
                    "nominal_worst_excess": fw(previous),
                    "worst_shift": fw(worst - previous),
                    "bound_excess": fw(worst - bound),
                    "nominal_minimizer": a in original,
                    "coarse_safe": worst <= 0,
                    "strict_benefit": worst < 0,
                    "original_bound_preserved": worst <= bound,
                    "full_support_maximum_attained": attained,
                    "every_full_support_mechanism_strict": worst < 0
                    or (worst == 0 and not attained),
                    "maximizing_face_indices": face,
                    "witness_label_indices": witness,
                    "witness_full_excess": fw(witness_full),
                    "witness_world_excesses": [fw(v) for v in witness_values],
                    "witness_worst_world_indices": [
                        t for t in worlds if witness_values[t] == witness_worst
                    ],
                    "potentially_unsafe_world_indices": [t for t in worlds if values[t] > 0],
                    "potentially_bound_breaking_world_indices": [
                        t for t in worlds if values[t] > bound
                    ],
                    "witness_unsafe_world_indices": [t for t in worlds if witness_values[t] > 0],
                    "witness_bound_breaking_world_indices": [
                        t for t in worlds if witness_values[t] > bound
                    ],
                }
            )
        safe = [a for a in original if candidates[a]["coarse_safe"]]
        strict = [a for a in original if candidates[a]["strict_benefit"]]
        preserved = [a for a in original if candidates[a]["original_bound_preserved"]]
        interior = [a for a in original if candidates[a]["every_full_support_mechanism_strict"]]
        old_slots += len(original)
        certificates.append(
            {
                "assumed_index": s,
                "bound_index": u,
                "world_indices": worlds,
                "nominal_minimax_excess": fw(bound),
                "old_minimizer_indices": copy.deepcopy(original),
                "old_minimizer_weights": copy.deepcopy(nominal["minimizer_weights"]),
                "candidates": candidates,
                "safe_old_indices": safe,
                "strictly_beneficial_old_indices": strict,
                "bound_preserving_old_indices": preserved,
                "interior_strict_old_indices": interior,
                "unsafe_old_indices": [a for a in original if a not in safe],
                "bound_breaking_old_indices": [a for a in original if a not in preserved],
                "all_old_safe": safe == original,
                "any_old_safe": bool(safe),
                "all_old_strict": strict == original,
                "any_old_strict": bool(strict),
                "all_old_bound_preserved": preserved == original,
                "any_old_bound_preserved": bool(preserved),
                "all_old_interior_strict": interior == original,
                "any_old_interior_strict": bool(interior),
                "checks": {key: True for key in AC_CHECKS},
            }
        )
    return {
        "input_sha256": digest(problem),
        "baseline": baseline,
        "alphabet": copy.deepcopy(problem["alphabet"]),
        "profiles": profiles,
        "certificates": certificates,
        "counts": {**work_counts(problem), "old_rule_evaluations": old_slots},
    }


def zero_supremum_problem():
    return curve_problem(F(-1), [[0, 1]])


def clean_dominates_problem():
    return curve_problem(F(3, 2), [[F(1, 2), 1]])


def unequal_world_sets_problem():
    return curve_problem(F(1), [[0, 1]])


def tie_problem():
    return problem_of(
        nominal_problem(half=(F(1, 2),) * 4, full=(F(1, 2),) * 4), [[[0, 0, 0], [0, 0, 2]]]
    )


def unused_fiber_problem():
    return curve_problem(F(-1), [[0, F(1, 2), F(1, 2)], [0, 0]], sizes=(3, 2))


def generic_nonscaling_problem():
    p = problem_of(nominal_signed_problem(), [[[0, 1, 0], [0, 0, 1]]])
    p["models"][2]["full_coefficients"][0][0][1] = [1, 2]
    return p


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ac_test_primary", "envelope.py"),
        private_module("_qr05ac_test_reference", "reference_qr05ac.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ac_test_runner", "study.py")


@pytest.mark.parametrize(
    "builder",
    [
        problem_of,
        zero_supremum_problem,
        clean_dominates_problem,
        unequal_world_sets_problem,
        tie_problem,
        unused_fiber_problem,
        generic_nonscaling_problem,
    ],
)
def test_generic_complete_wire_equals_independent_faces_worlds_and_witness_oracle(
    executors, builder
):
    p = builder()
    before, wanted = wire(p), independently_envelope(p)
    for module in executors:
        assert wire(module.analyze(p)) == wire(wanted)
        assert wire(p) == before


def test_closed_zero_supremum_can_be_unattained_with_every_full_support_law_strictly_beneficial(
    executors,
):
    for module in executors:
        result = module.analyze(zero_supremum_problem())
        c = result["certificates"][1]["candidates"][2]
        assert c["worst_excess"] == [0, 1] and c["worst_world_indices"] == [1]
        assert c["strict_benefit"] is False and c["coarse_safe"] is True
        assert c["full_support_maximum_attained"] is False
        assert c["every_full_support_mechanism_strict"] is True
        assert c["maximizing_face_indices"] == [[1]] and c["witness_label_indices"] == [1]
        assert c["witness_world_excesses"] == [[-1, 1], [0, 1]]
        for mass, expected in ((F(3, 4), F(-1, 8)), (F(7, 8), F(-1, 16))):
            assert (F(-1) + mass) / 2 == expected < 0
        harmful = result["certificates"][3]["candidates"][2]
        assert harmful["worst_excess"] == [1, 1] and harmful["coarse_safe"] is False
        assert F(3, 4) > 0  # A full-support smoothing is already harmful at t=1.


def test_attained_zero_is_not_a_uniform_or_pointwise_strict_benefit(executors):
    for module in executors:
        c = module.analyze(curve_problem(-1, [[0, 0]]))["certificates"][3]["candidates"][2]
        assert c["worst_excess"] == [0, 1]
        assert c["full_support_maximum_attained"] is True
        assert c["strict_benefit"] is c["every_full_support_mechanism_strict"] is False
        assert c["maximizing_face_indices"] == [[0, 1]]


def test_zero_bound_clean_dominance_and_coarse_rule_preserve_the_entire_mechanism_simplex(
    executors,
):
    for module in executors:
        zero = module.analyze(zero_supremum_problem())["certificates"][0]["candidates"][2]
        assert zero["worst_excess"] == [-1, 1] and zero["maximizing_face_indices"] == [[0, 1]]
        assert (
            zero["witness_label_indices"] == [0] and zero["full_support_maximum_attained"] is True
        )
        result = module.analyze(clean_dominates_problem())
        c = result["certificates"][3]["candidates"][2]
        assert c["worst_excess"] == [3, 2] and c["worst_world_indices"] == [0]
        assert c["maximizing_face_indices"] == [[0, 1]] and c["witness_label_indices"] == [0]
        assert c["witness_full_excess"] == [1, 2]
        assert c["full_support_maximum_attained"] is True
        for cert in result["certificates"]:
            coarse = cert["candidates"][0]
            assert coarse["worst_excess"] == [0, 1]
            assert coarse["maximizing_face_indices"] == [[0, 1]]
            assert coarse["full_support_maximum_attained"] is True


def test_lex_witness_need_not_realize_every_envelope_maximizing_world(executors):
    for module in executors:
        c = module.analyze(unequal_world_sets_problem())["certificates"][3]["candidates"][2]
        assert c["world_upper_excesses"] == [[1, 1]] * 4
        assert c["worst_world_indices"] == [0, 1, 2, 3]
        assert c["maximizing_face_indices"] == [[0, 1]] and c["witness_label_indices"] == [0]
        assert c["witness_world_excesses"] == [[1, 1], [1, 2], [1, 4], [0, 1]]
        assert c["witness_worst_world_indices"] == [0]
        assert c["potentially_unsafe_world_indices"] == [0, 1, 2, 3]
        assert c["witness_unsafe_world_indices"] == [0, 1, 2]


def test_all_maximizing_labels_unused_fibers_and_lex_pointmasses_are_explicit(executors):
    for module in executors:
        result = module.analyze(unused_fiber_problem())
        p, c = result["profiles"][2], result["certificates"][3]["candidates"][2]
        assert [row["maximizer_indices"] for row in p["fibers"]] == [[1, 2], [0, 1]]
        assert p["all_fibers_flat"] is False
        assert c["maximizing_face_indices"] == [[1, 2], [0, 1]]
        assert c["witness_label_indices"] == [1, 0] and c["witness_full_excess"] == [1, 2]
        assert c["full_support_maximum_attained"] is False
        assert module.analyze(problem_of(sizes=(1,)))["profiles"][2]["all_fibers_flat"] is True


def test_old_ties_are_not_reoptimized_and_benefit_does_not_preserve_the_old_negative_bound(
    executors,
):
    for module in executors:
        result = module.analyze(tie_problem())
        c = result["certificates"][1]
        assert c["old_minimizer_indices"] == [1, 2]
        assert c["safe_old_indices"] == c["strictly_beneficial_old_indices"] == [1]
        assert c["unsafe_old_indices"] == [2]
        assert c["all_old_safe"] is False and c["any_old_safe"] is True
        assert c["bound_preserving_old_indices"] == [] and c["bound_breaking_old_indices"] == [1, 2]
        assert c["candidates"][1]["worst_excess"] == [-1, 4] and c["candidates"][1][
            "bound_excess"
        ] == [1, 4]
        assert (
            c["candidates"][0]["coarse_safe"] is True
            and c["candidates"][0]["nominal_minimizer"] is False
        )
        assert "minimizer_indices" not in c
        assert wire(result["baseline"]) == wire(
            independently_decide_nominal(tie_problem()["nominal"])
        )


def test_generic_coefficients_need_not_scale_with_weight_or_match_nominal_affinity(executors):
    p = generic_nonscaling_problem()
    for module in executors:
        result = module.analyze(p)
        assert result["profiles"][1]["fibers"][0]["maximizer_indices"] == [0]
        assert result["profiles"][2]["fibers"][0]["maximizer_indices"] == [1]
        assert result["profiles"][7]["full_upper_excess"] == [1, 2]


def overflow_problem(kind):
    d = 1 << 4095
    if kind == "sum":
        return curve_problem(0, [[F(1, d)], [F(1, 3)]], sizes=(1, 1))
    if kind == "envelope":
        return curve_problem(-F(1, d), [[0, 0]])
    if kind == "witness_sum":
        return curve_problem(2, [[F(1, d), 1], [F(1, 3), 1]], sizes=(2, 2))
    if kind == "witness_world":
        return curve_problem(F(1, d), [[0, F(1, d)]])
    if kind == "shift":
        p = curve_problem(0, [[F(2, 3), F(2, 3)]])
        p["nominal"]["worlds"][1]["models"][0]["forecast_risks"][2] = [1, d]
        return p
    nominal = nominal_problem(coarse=(F(1, d),) * 4, half=(0,) * 4, full=(F(1, d),) * 4)
    return problem_of(nominal, [[[0, F(3, d), F(2, 3)], [0, F(3, d), F(2, 3)]]])


@pytest.mark.parametrize(
    "kind", ["sum", "envelope", "witness_sum", "witness_world", "shift", "bound"]
)
def test_new_retained_bit_overflow_is_rejected_after_valid_nominal_AA(executors, kind):
    p = overflow_problem(kind)
    native(p)
    d = 1 << 4095
    targets = {
        "sum": F(1, d) + F(1, 3),
        "envelope": F(-1, 2 * d),
        "witness_sum": F(1, d) + F(1, 3),
        "witness_world": F(1, 2 * d),
        "shift": F(1, 3) - F(1, d),
        "bound": F(1, 3) + F(1, d),
    }
    assert targets[kind].denominator.bit_length() == 4097
    for module in executors:
        assert wire(module._analyze_nominal(p["nominal"])) == wire(
            independently_decide_nominal(p["nominal"])
        )
        with pytest.raises(ValueError):
            module.analyze(p)


def test_intermediate_4097_bit_envelope_terms_can_cancel_to_valid_retained_values(executors):
    d = 1 << 4094
    p = curve_problem(F(-3, d), [[F(1, d), F(1, d)]])
    assert F(3, 4 * d).denominator.bit_length() == 4097
    wanted = independently_envelope(p)
    for module in executors:
        result = module.analyze(p)
        assert wire(result) == wire(wanted)
        assert result["certificates"][3]["candidates"][2]["world_upper_excesses"] == [
            [-3, d],
            [-1, d],
            [0, 1],
            [1, d],
        ]


def test_signed_shift_can_reach_four_and_profile_sum_cannot_exceed_two(executors):
    p = curve_problem(-2, [[2, 2]])
    bad = curve_problem(0, [[2], [2]], sizes=(1, 1))
    for module in executors:
        c = module.analyze(p)["certificates"][3]["candidates"][2]
        assert c["bound_excess"] == c["worst_shift"] == [4, 1]
        with pytest.raises(ValueError):
            module.analyze(bad)


def invalid_problems():
    p = problem_of(sizes=(2, 1))
    bad = [None, [], True, DictChild(p)]
    bad.extend(replaced(p, ("nominal",), value) for value in invalid_nominals())
    for key in p:
        item = p.copy()
        del item[key]
        bad.append(item)
    for key in ("extra", "clean_excess", "selector", "minimizer_indices", "artifact", "witness"):
        bad.append({**p, key: 0})
    for key in ("schema_version", "family"):
        bad.extend(replaced(p, (key,), value) for value in ("wrong", StrChild(p[key]), None))
    letters = p["alphabet"]
    for value in (
        [],
        letters[::-1],
        letters + [letters[0]],
        tuple(letters),
        ListChild(letters),
        problem_of(sizes=(1,) * 73)["alphabet"],
        problem_of(sizes=(94,))["alphabet"],
    ):
        bad.append(replaced(p, ("alphabet",), value))
    for value in (
        [],
        {"N": letters[0]["N"]},
        {"values": letters[0]["values"]},
        {**letters[0], "extra": 0},
        DictChild(letters[0]),
    ):
        bad.append(replaced(p, ("alphabet", 0), value))
    for value in (
        [],
        [0] * 4,
        [0] * 6,
        (0,) * 5,
        ListChild([0] * 5),
        [-1, 0, 0, 0, 0],
        [False, 0, 0, 0, 0],
        [IntChild(0), 0, 0, 0, 0],
        [0.0, 0, 0, 0, 0],
    ):
        bad.append(replaced(p, ("alphabet", 0, "N"), value))
    values = letters[0]["values"]
    for value in ([], tuple(values), ListChild(values), values[::-1], values + [values[0]]):
        bad.append(replaced(p, ("alphabet", 0, "values"), value))
    for value in (
        [0] * 6,
        [0] * 8,
        tuple([0] * 7),
        ListChild([0] * 7),
        [1, 0, 0, 0, 0, 0, 0],
        [0] * 6 + [-1],
        [0] * 6 + [False],
        [0] * 6 + [IntChild(0)],
        [0] * 6 + [0.0],
        [0] * 6 + [1 << 4096],
    ):
        bad.append(replaced(p, ("alphabet", 0, "values", 0), value))
    models = p["models"]
    for value in (
        [],
        models[:3],
        models + [models[0]],
        models[::-1],
        tuple(models),
        ListChild(models),
    ):
        bad.append(replaced(p, ("models",), value))
    last = ("models", 3)
    for value in (
        {"assumed_index": 3},
        {"full_coefficients": models[3]["full_coefficients"]},
        {**models[3], "extra": 0},
        DictChild(models[3]),
    ):
        bad.append(replaced(p, last, value))
    for value in (True, 3.0, IntChild(3), -1, 2, "3"):
        bad.append(replaced(p, last + ("assumed_index",), value))
    coefficients = models[3]["full_coefficients"]
    for value in (
        [],
        coefficients[:1],
        coefficients + [coefficients[0]],
        tuple(coefficients),
        ListChild(coefficients),
    ):
        bad.append(replaced(p, last + ("full_coefficients",), value))
    for path, values in (
        (
            ("full_coefficients", 0),
            [
                [],
                coefficients[0][:1],
                coefficients[0] + [coefficients[0][0]],
                tuple(coefficients[0]),
            ],
        ),
        (
            ("full_coefficients", 1, 0),
            [
                [],
                [[0, 1]] * 2,
                [[0, 1]] * 4,
                tuple(coefficients[1][0]),
                ListChild(coefficients[1][0]),
            ],
        ),
        (
            ("full_coefficients", 1, 0, 2),
            [
                None,
                [2, 4],
                [1, 0],
                [-1, 2],
                [3, 1],
                [True, 1],
                [1.0, 2],
                [IntChild(1), 2],
                (1, 2),
                [1, 1 << 4096],
                [0, 2],
            ],
        ),
        (("full_coefficients", 1, 0, 0), [[1, 2]]),
    ):
        bad.extend(replaced(p, last + path, value) for value in values)
    item = p.copy()
    item[StrChild("family")] = item.pop("family")
    bad.extend([item, {**p, 1: None}])
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_nominal_alphabet_and_coefficient_schema_fail_without_coercion_or_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


HOOKS = ("_analyze_nominal", "_profile_coefficient", "_envelope", "_witness_term", "_shift")
CAPS = (
    "MAX_BITS",
    "MAX_DEPTH",
    "MAX_NODES",
    "MAX_BYTES",
    "MAX_RISK_CELLS",
    "MAX_DECISION_WORK",
    "MAX_FIBERS",
    "MAX_LABELS",
    "MAX_COEFFICIENT_CELLS",
    "MAX_TOTAL_WORK",
)


def planned_caps(p):
    counts = work_counts(p)
    return {
        "MAX_RISK_CELLS": 48,
        "MAX_DECISION_WORK": 216,
        "MAX_FIBERS": counts["fibers"],
        "MAX_LABELS": counts["labels"],
        "MAX_COEFFICIENT_CELLS": counts["coefficient_cells"],
        "MAX_TOTAL_WORK": counts["total_work_terms"],
    }


def test_all_work_is_reserved_before_any_nominal_profile_envelope_witness_or_shift_hook(
    executors, monkeypatch
):
    p = unused_fiber_problem()
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as patched:
            for name in HOOKS:
                original = getattr(module, name)

                def observed(*args, name=name, original=original, calls=calls):
                    calls[name] += 1
                    return original(*args)

                patched.setattr(module, name, observed)
            result = module.analyze(p)
        assert calls == {
            "_analyze_nominal": 1,
            "_profile_coefficient": 60,
            "_envelope": 168,
            "_witness_term": 96,
            "_shift": 96,
        }
        assert result["counts"] == {**work_counts(p), "old_rule_evaluations": 16}

        def forbidden(*_args):
            raise RuntimeError("nominal or envelope work began before complete preflight")

        for constant, limit in planned_caps(p).items():
            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit - 1)
                for name in HOOKS:
                    patched.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        bad = replaced(p, ("models", 3, "full_coefficients", 1, 1, 2), [2, 4])
        with monkeypatch.context() as patched:
            for name in HOOKS:
                patched.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(bad)


@pytest.mark.parametrize("constant", CAPS)
def test_every_live_cap_rejects_and_restoration_has_no_cross_call_cache(
    executors, monkeypatch, constant
):
    p = unused_fiber_problem()
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def shared_problem():
    p = unused_fiber_problem()
    common = p["models"][0]["full_coefficients"]
    for model in p["models"]:
        model["full_coefficients"] = common
    return p


def test_complete_baseline_alphabet_faces_witnesses_and_calls_are_detached(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        first, second = module.analyze(p), module.analyze(p)
        wanted = wire(second)
        assert wanted == wire(independently_envelope(p))
        assert mutable_ids(p).isdisjoint(mutable_ids(first))
        assert mutable_ids(first).isdisjoint(mutable_ids(second))
        first["baseline"]["worlds"][0]["coarse_risk"][0] = -1
        first["alphabet"][0]["N"][0] = -1
        first["certificates"][0]["candidates"][2]["maximizing_face_indices"][0].clear()
        assert wire(p) == before and wire(second) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["models"][0]["full_coefficients"][0][0][2] = [1, 1]
        assert wire(detached) == wanted and wire(module.analyze(changed)) != wanted


def test_native_depth_shared_memo_exact_ascii_and_expanded_nodes(executors, monkeypatch):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    for module in executors:
        for v in (nested(0, 128), nested([], 128)):
            module._native(v)
        for v in (nested(0, 129), nested([], 129)):
            with pytest.raises(ValueError):
                module._native(v)
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


def test_complete_outer_native_preflight_and_exact_output_byte_limit(executors, monkeypatch):
    p = shared_problem()
    nodes, depth = tree_resources(p)
    for module in executors:
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("unsafe outer tree reached whole serialization")

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
    cycle = []
    cycle.append(cycle)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    dag = []
    for _ in range(40):
        dag = [dag, dag]
    for value in (cycle, cycle_dict, nested([], 1500), dag):
        yield {**valid, "extra": value}
    for path in (
        ("nominal",),
        ("nominal", "worlds"),
        ("nominal", "worlds", 0, "coarse_risk"),
        ("alphabet",),
        ("alphabet", 0),
        ("alphabet", 0, "N"),
        ("alphabet", 0, "values"),
        ("alphabet", 0, "values", 0),
        ("models",),
        ("models", 0),
        ("models", 0, "assumed_index"),
        ("models", 0, "full_coefficients"),
        ("models", 0, "full_coefficients", 0),
        ("models", 0, "full_coefficients", 0, 0),
        ("models", 0, "full_coefficients", 0, 0, 2),
        ("nominal", "levels"),
    ):
        yield replaced(valid, path, dag)


def test_generic_auditor_matches_complete_faces_witnesses_and_interior_strictness():
    audit = private_module("_qr05ac_test_generic_audit", "audit_json.py")
    for p in (
        zero_supremum_problem(),
        unequal_world_sets_problem(),
        tie_problem(),
        unused_fiber_problem(),
    ):
        before = wire(p)
        assert wire(audit.expected_ac(p)) == wire(independently_envelope(p))
        assert wire(p) == before


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_checks_are_active_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05ac_guards",Path(sys.argv[1]))
if spec is None or spec.loader is None: raise RuntimeError("missing helpers")
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
rejections=pre=0
def require(value,message):
    if not value: raise RuntimeError(message)
def reject(call,value):
    global rejections
    try: call(value)
    except ValueError: rejections+=1
    else: raise RuntimeError("invalid input accepted")
def before_dump(call,value):
    global pre
    original=json.dumps
    def forbidden(*args,**kwargs): raise RuntimeError("unsafe tree serialized")
    json.dumps=forbidden
    try: reject(call,value);pre+=1
    finally: json.dumps=original
invalid=h.invalid_problems();valid=h.shared_problem()
for i,filename in enumerate(("envelope.py","reference_qr05ac.py")):
    module=h.private_module("_qr05ac_guard_core"+str(i),filename)
    for builder in (h.zero_supremum_problem,h.unequal_world_sets_problem,h.tie_problem,h.unused_fiber_problem):
        p=builder();require(h.wire(module.analyze(p))==h.wire(h.independently_envelope(p)),"complete generic wire")
    for bad in invalid: reject(module.analyze,bad)
    graphs=list(h.graph_inputs(valid));require(len(graphs)==20,"graph inventory")
    for bad in graphs: before_dump(module.analyze,bad)
    def forbidden(*args): raise RuntimeError("work preceded complete preflight")
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
    try:reject(module.analyze,h.replaced(valid,("models",3,"full_coefficients",1,1,2),[2,4]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    for kind in ("sum","envelope","witness_sum","witness_world","shift","bound"):
        p=h.overflow_problem(kind)
        require(module._analyze_nominal(p["nominal"])==h.independently_decide_nominal(p["nominal"]),"nominal overflow fixture invalid")
        reject(module.analyze,p)
    for v in (h.nested(0,128),h.nested([],128)):module._native(v)
    for v in (h.nested(0,129),h.nested([],129)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,126)]);reject(module._native,[shared,h.nested(shared,127)])
    result=module.analyze(valid);result["alphabet"][0]["N"][0]=-1
    require(module.analyze(valid)==h.independently_envelope(valid),"ownership or cap restoration")
runner=h.private_module("_qr05ac_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==60,"pre-serialization inventory")
require(rejections==2*(len(invalid)+46)+24,"rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ac.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 46) + 24,
        "pre_serialization_rejections": 60,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


PINS = {
    "ab": (
        "qr-05ab-replacement-stress-2026-09-07",
        1805554,
        "7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009",
    ),
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
    key: True
    for key in (
        "nominal_AA_baseline_preserved",
        "whole_model_alphabet_preserved",
        "original_weight_coefficients",
        "nonnegative_full_replacement_coefficients",
        "uniform_family_recovered",
        "both_AB_tilt_risks_recovered",
        "frozen_forecasts_and_weights",
        "clean_and_N_future_marginals_preserved",
        "complete_boundary_witness_laws",
        "literal_global_witness_scores",
        "coefficient_weight_square_scaling",
        "upper_endpoint_is_worst",
        "nominal_and_AB_enclosed",
        "all_original_ties_classified_without_reoptimization",
    )
}
PRODUCER_CONTROLS.update(
    origin_authenticated_by_generic_API=False,
    raw_history_reconstruction_performed_by_this_runner=False,
)


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


def alphabet(wsuite):
    groups = {}
    for label in wsuite["model"]["labels"]:
        q = tuple(label["question"])
        assert q[:5] == tuple(label["observation"])
        groups.setdefault(q[:5], set()).add(q)
    return [
        {"N": list(n), "values": [list(q) for q in sorted(values)]}
        for n, values in sorted(groups.items())
    ]


def frozen_maps(zcase):
    return [
        [
            {
                tuple(c["value"]): [read_law(b["forecast"]) for b in c["blends"]]
                for c in row["pairs"][12 + s]["cells"]
            }
            for s in range(4)
        ]
        for row in zcase["analysis"]["beliefs"]
    ]


def independent_coefficients(zcase, letters):
    totals = [[[[F(0) for _ in WEIGHTS] for _ in row["values"]] for row in letters] for _ in LEVELS]
    for source, models in zip(
        zcase["problem"]["experiment"]["beliefs"], frozen_maps(zcase), strict=True
    ):
        weight = fraction(source["weight"])
        subjoint = {}
        for (report, q), mass in channel_joints(source["channels"][0]).items():
            subjoint.setdefault(report[:5], {})[q] = (
                subjoint.setdefault(report[:5], {}).get(q, F(0)) + mass
            )
        for n, row in enumerate(letters):
            atoms = subjoint.get(tuple(row["N"]), {})
            if not atoms:
                continue
            for z, report in enumerate(row["values"]):
                for s in range(4):
                    forecasts = models[s][tuple(report)]
                    g = forecasts[0]
                    for a, h in enumerate(forecasts):
                        # Literal losses against each unnormalized source N/future
                        # atom. Individual differences may be negative; never clip.
                        totals[s][n][z][a] += weight * sum(
                            mass * (outcome_risk({q: F(1)}, h) - outcome_risk({q: F(1)}, g))
                            for q, mass in atoms.items()
                        )
    assert all(v >= 0 for model in totals for fiber in model for row in fiber for v in row)
    return [
        {
            "assumed_index": s,
            "full_coefficients": [[[fw(v) for v in row] for row in fiber] for fiber in model],
        }
        for s, model in enumerate(totals)
    ]


def project_case(aacase, zcase, letters):
    assert aacase["case_id"] == zcase["case_id"]
    return {
        "case_id": aacase["case_id"],
        "problem": {
            "schema_version": "det8-qr05ac-problem-v1",
            "family": "qr05ac_replacement_envelope",
            "nominal": copy.deepcopy(aacase["problem"]),
            "alphabet": copy.deepcopy(letters),
            "models": independent_coefficients(zcase, letters),
        },
    }


def witness_evidence(zcase, analysis):
    vectors = sorted(
        {
            tuple(c["witness_label_indices"])
            for cert in analysis["certificates"]
            for c in cert["candidates"]
        }
    )
    laws = []
    for wid, vector in enumerate(vectors):
        # Keep zero replacement probabilities during stochastic application so
        # unchosen clean labels remain present at t<1; omit zero joint atoms only.
        mu = [
            {
                "N": row["N"],
                "values": [
                    {"value": q, "probability": [int(i == chosen), 1]}
                    for i, q in enumerate(row["values"])
                ],
            }
            for row, chosen in zip(analysis["alphabet"], vector, strict=True)
        ]
        beliefs = [
            {
                "belief_id": source["belief_id"],
                "weight": copy.deepcopy(source["weight"]),
                "channels": tilted_channels(source["channels"][0], mu),
            }
            for source in zcase["problem"]["experiment"]["beliefs"]
        ]
        laws.append({"witness_id": wid, "label_indices": list(vector), "beliefs": beliefs})
    mapping = [
        {
            "assumed_index": cert["assumed_index"],
            "bound_index": cert["bound_index"],
            "rule_index": a,
            "witness_id": vectors.index(tuple(candidate["witness_label_indices"])),
        }
        for cert in analysis["certificates"]
        for a, candidate in enumerate(cert["candidates"])
    ]
    return {"witness_laws": laws, "witness_certificate_map": mapping}


def mini_z_case():
    x, y = tuple([0] * 7), tuple([0] * 6 + [1])
    source, rows, base = [], [], []
    for bid, (weight, px) in enumerate(((F(1, 4), F(1, 4)), (F(3, 4), F(3, 4)))):
        g = {x: px, y: 1 - px}
        clean = {
            "level": [0, 1],
            "cells": [
                {"value": list(q), "probability": fw(p), "prediction": law_wire({q: F(1)})}
                for q, p in g.items()
            ],
        }
        source.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "channels": [clean],
                "fallbacks": [{"value": [0] * 5, "prediction": law_wire(g)}],
            }
        )
        cells, originals = [], []
        for q in (x, y):
            blends = []
            for a in map(fraction, WEIGHTS):
                h = {r: (1 - a) * g[r] + a * (r == q) for r in g}
                blends.append({"retained_weight": fw(a), "forecast": law_wire(h)})
            cells.append({"value": list(q), "blends": blends})
            originals.append(
                {"value": list(q), "coarse_forecast": law_wire(g), "forecast": law_wire({q: F(1)})}
            )
        rows.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "pairs": [copy.deepcopy({"cells": cells}) for _ in range(16)],
            }
        )
        base.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "pairs": [copy.deepcopy({"cells": originals}) for _ in range(16)],
            }
        )
    return {
        "case_id": "generic-two-history",
        "problem": {"experiment": {"beliefs": source}},
        "analysis": {"beliefs": rows, "baseline": {"beliefs": base}},
    }


def test_original_history_aggregation_precedes_one_global_label_maximum(runner, executors):
    zcase = mini_z_case()
    letters = problem_of()["alphabet"]
    wanted = independent_coefficients(zcase, letters)
    assert wire(runner.coefficients_from_case(zcase, letters)) == wire(wanted)
    assert wire(runner.coefficients_from_case(zcase, letters, literal=True)) == wire(wanted)
    coefficients = [fraction(row[2]) for row in wanted[0]["full_coefficients"][0]]
    assert coefficients == [F(3, 8), F(7, 8)]
    assert max(coefficients) == F(7, 8)
    stronger_historywise = F(1, 4) * F(9, 8) + F(3, 4) * F(9, 8)
    wrong_uniform = (F(9, 8) + F(1, 8)) / 2
    assert stronger_historywise == F(9, 8) and wrong_uniform == F(5, 8)
    p = curve_problem(F(-3, 8), [[F(3, 8), F(7, 8)]])
    for module in executors:
        c = module.analyze(p)["certificates"][1]["candidates"][2]
        assert c["worst_excess"] == [1, 4] and c["witness_label_indices"] == [1]


def test_boundary_witness_keeps_unchosen_clean_labels_until_full_replacement(runner):
    zcase = mini_z_case()
    analysis = independently_envelope(zero_supremum_problem())
    wanted = witness_evidence(zcase, analysis)
    assert wire(runner.build_witness_evidence(zcase, analysis)) == wire(wanted)
    for law in wanted["witness_laws"]:
        chosen = analysis["alphabet"][0]["values"][law["label_indices"][0]]
        for source, row in zip(
            zcase["problem"]["experiment"]["beliefs"], law["beliefs"], strict=True
        ):
            assert row["weight"] == source["weight"]
            assert wire(row["channels"][0]) == wire(source["channels"][0])
            assert len(row["channels"][1]["cells"]) == 2
            assert [c["value"] for c in row["channels"][3]["cells"]] == [chosen]
            assert row["channels"][3]["cells"][0]["probability"] == [1, 1]
            assert marginal(channel_joints(row["channels"][3])) == marginal(
                channel_joints(source["channels"][0])
            )


@pytest.fixture(scope="session")
def letters(pinned):
    return alphabet(pinned["w"])


@pytest.fixture(scope="session")
def projected(pinned, letters):
    return [
        project_case(aa, z, letters)
        for aa, z in zip(pinned["aa"]["cases"], pinned["z"]["cases"], strict=True)
    ]


@pytest.fixture(scope="session")
def expected(projected):
    return [independently_envelope(row["problem"]) for row in projected]


@pytest.fixture(scope="session")
def evidence(pinned, expected):
    return [witness_evidence(z, a) for z, a in zip(pinned["z"]["cases"], expected, strict=True)]


@pytest.mark.parametrize("case_index", range(6))
def test_fixed_six_complete_wires_equal_independent_literal_coefficients_and_envelope_witness_oracle(
    executors, pinned, projected, expected, case_index
):
    p, wanted = projected[case_index]["problem"], expected[case_index]
    assert wire(wanted["baseline"]) == wire(pinned["aa"]["cases"][case_index]["analysis"])
    before = wire(p)
    for module in executors:
        assert wire(module.analyze(p)) == wire(wanted)
        assert wire(p) == before


def test_fixed_whole_model_alphabet_coefficients_recover_uniform_AA_and_both_AB_risk_tensors(
    pinned, letters, projected, expected
):
    assert len(letters) == 72 and sum(len(row["values"]) for row in letters) == 93
    assert letters == sorted(letters, key=lambda row: row["N"])
    for aa, ab, p, analysis in zip(
        pinned["aa"]["cases"], pinned["ab"]["cases"], projected, expected, strict=True
    ):
        models = p["problem"]["models"]
        for s in range(4):
            for a in range(3):
                clean = fraction(analysis["profiles"][3 * s + a]["clean_excess"])
                uniform = sum(
                    sum(fraction(row[a]) for row in fiber) / len(fiber)
                    for fiber in models[s]["full_coefficients"]
                )
                for t, level in enumerate(LEVELS):
                    rate = fraction(level)
                    coarse = fraction(aa["problem"]["worlds"][t]["coarse_risk"])
                    assert (
                        fw(coarse + (1 - rate) * clean + rate * uniform)
                        == aa["problem"]["worlds"][t]["models"][s]["forecast_risks"][a]
                    )
                for mu, mechanism in zip(
                    pinned["ab"]["replacement_laws"], ab["problem"]["mechanisms"], strict=True
                ):
                    total = sum(
                        fraction(row[a]) * fraction(atom["probability"])
                        for fiber, alphabet_row in zip(
                            models[s]["full_coefficients"], mu["alphabet"], strict=True
                        )
                        for row, atom in zip(fiber, alphabet_row["values"], strict=True)
                    )
                    for t, level in enumerate(LEVELS):
                        rate = fraction(level)
                        coarse = fraction(mechanism["worlds"][t]["coarse_risk"])
                        assert (
                            fw(coarse + (1 - rate) * clean + rate * total)
                            == mechanism["worlds"][t]["models"][s]["forecast_risks"][a]
                        )
            for fiber in models[s]["full_coefficients"]:
                assert all(
                    fraction(row[0]) == 0 and fraction(row[1]) == fraction(row[2]) / 4
                    for row in fiber
                )
            assert [f["maximizer_indices"] for f in analysis["profiles"][3 * s + 1]["fibers"]] == [
                f["maximizer_indices"] for f in analysis["profiles"][3 * s + 2]["fibers"]
            ]
            for u in range(4):
                cert = analysis["certificates"][4 * s + u]
                for c in cert["candidates"]:
                    assert u in c["worst_world_indices"]
                assert (
                    cert["candidates"][1]["maximizing_face_indices"]
                    == cert["candidates"][2]["maximizing_face_indices"]
                )


def test_fixed_every_unique_witness_law_is_rebuilt_and_all_frozen_candidates_are_literally_scored(
    pinned, projected, expected, evidence
):
    for zcase, projection, analysis, observed in zip(
        pinned["z"]["cases"], projected, expected, evidence, strict=True
    ):
        p = projection["problem"]
        policies = frozen_maps(zcase)
        vectors = [law["label_indices"] for law in observed["witness_laws"]]
        assert vectors == sorted(vectors) and len(set(map(tuple, vectors))) == len(vectors)
        scores = {}
        for wid, law in enumerate(observed["witness_laws"]):
            assert law["witness_id"] == wid
            sums = {(t, s, a): F(0) for t in range(4) for s in range(4) for a in range(3)}
            coarse = {t: F(0) for t in range(4)}
            for source, row, maps in zip(
                zcase["problem"]["experiment"]["beliefs"], law["beliefs"], policies, strict=True
            ):
                assert row["belief_id"] == source["belief_id"] and row["weight"] == source["weight"]
                w = fraction(source["weight"])
                clean = channel_joints(source["channels"][0])
                for t, channel in enumerate(row["channels"]):
                    assert marginal(channel_joints(channel)) == marginal(clean)
                    if t == 0:
                        assert wire(channel) == wire(source["channels"][0])
                    for cell in channel["cells"]:
                        report, mass, truth = (
                            tuple(cell["value"]),
                            fraction(cell["probability"]),
                            read_law(cell["prediction"]),
                        )
                        g = maps[0][report][0]
                        cg = outcome_risk(truth, g)
                        coarse[t] += w * mass * cg
                        if t == 3:
                            assert truth == g
                        for s in range(4):
                            assert maps[s][report][0] == g
                            for a in range(3):
                                sums[t, s, a] += w * mass * outcome_risk(truth, maps[s][report][a])
            for s in range(4):
                for a in range(3):
                    full = sum(
                        fraction(fiber[z][a])
                        for fiber, z in zip(
                            p["models"][s]["full_coefficients"], law["label_indices"], strict=True
                        )
                    )
                    clean = fraction(analysis["profiles"][3 * s + a]["clean_excess"])
                    curve = [sums[t, s, a] - coarse[t] for t in range(4)]
                    assert curve == [
                        (1 - fraction(level)) * clean + fraction(level) * full for level in LEVELS
                    ]
                    scores[wid, s, a] = curve
        assert len(observed["witness_certificate_map"]) == 48
        for i, mapping in enumerate(observed["witness_certificate_map"]):
            s, u, a = i // 12, (i % 12) // 3, i % 3
            assert {
                key: mapping[key] for key in ("assumed_index", "bound_index", "rule_index")
            } == {"assumed_index": s, "bound_index": u, "rule_index": a}
            c = analysis["certificates"][4 * s + u]["candidates"][a]
            assert vectors[mapping["witness_id"]] == c["witness_label_indices"]
            curve = scores[mapping["witness_id"], s, a][: u + 1]
            assert [fw(v) for v in curve] == c["witness_world_excesses"]
            assert fw(max(curve)) == c["worst_excess"]
            assert [t for t, v in enumerate(curve) if v == max(curve)] == c[
                "witness_worst_world_indices"
            ]


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_runner_complete_projection_laws_controls_and_nonpooled_inventory(
    runner, pinned, letters, projected, expected, evidence, aggregate
):
    assert set(aggregate) == {
        "producer",
        "alphabet",
        "cases",
        "independent_route_equal",
        "public_controls",
        "totals",
    }
    directory, size, sha = PINS["ab"]
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
        "historywise_adversary_used": False,
    }
    counts = {key: sum(a["counts"][key] for a in expected) for key in expected[0]["counts"]}
    assert aggregate["totals"] == {
        "cases": 6,
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        **counts,
        "witness_mechanisms": sum(len(e["witness_laws"]) for e in evidence),
    }
    assert wire(aggregate["alphabet"]) == wire(letters) == wire(runner.alphabet(pinned["w"]))
    assert wire(runner.fixtures()) == wire(pinned)
    for aa, z, p, a, e, actual in zip(
        pinned["aa"]["cases"],
        pinned["z"]["cases"],
        projected,
        expected,
        evidence,
        aggregate["cases"],
        strict=True,
    ):
        assert set(actual) == {
            "case_id",
            "problem",
            "analysis",
            "witness_laws",
            "witness_certificate_map",
            "producer_controls",
        }
        assert wire({key: actual[key] for key in ("case_id", "problem")}) == wire(p)
        assert wire(actual["analysis"]) == wire(a)
        assert wire(
            {key: actual[key] for key in ("witness_laws", "witness_certificate_map")}
        ) == wire(e)
        assert wire(actual["producer_controls"]) == wire(PRODUCER_CONTROLS)
        assert wire(runner.project_case(aa, z, letters)) == wire(p)


def output_corruptions(analysis):
    bad = []

    def add(path, value):
        changed = replaced(analysis, path, value)
        assert wire(changed) != wire(analysis)
        bad.append(changed)

    add(("input_sha256",), "0" * 64)
    add(("baseline", "decisions", 3, "minimizer_indices"), [])
    add(("profiles", 0, "full_upper_excess"), [1, 1])
    add(("profiles", 0, "fibers", 0, "maximizer_indices"), [])
    add(("certificates", 3, "old_minimizer_indices"), [])
    c = ("certificates", 3, "candidates", 0)
    add(c + ("worst_world_indices",), [3])
    add(c + ("maximizing_face_indices", 0), [])
    add(c + ("witness_label_indices",), [])
    add(c + ("witness_full_excess",), [1, 1])
    add(c + ("witness_world_excesses", 0), [1, 1])
    add(c + ("witness_worst_world_indices",), [0])
    add(c + ("full_support_maximum_attained",), False)
    add(c + ("every_full_support_mechanism_strict",), True)
    add(("certificates", 3, "checks", "global_witness_attains_envelope"), False)
    add(("counts", "total_work_terms"), analysis["counts"]["total_work_terms"] - 1)
    return bad


def test_fixed_complete_wire_corruptions_are_nonvacuous_without_replaying_projection_for_each_edit(
    runner, pinned, letters, projected, expected, evidence, monkeypatch
):
    aa, z, ab = (pinned[name]["cases"][0] for name in ("aa", "z", "ab"))
    # Full independent projection/law checks above establish this input. This
    # bounded test isolates the complete-wire validator, not producer rebuilding.
    with monkeypatch.context() as patched:
        patched.setattr(runner, "project_case", lambda *_args: copy.deepcopy(projected[0]))
        for bad in output_corruptions(expected[0]):
            with pytest.raises(ValueError):
                runner.check_analysis(bad, aa, z, ab, letters, evidence[0])


def test_fixed_producer_risk_forecast_weight_boundary_law_and_mapping_corruptions(
    runner, pinned, letters, expected, evidence
):
    args = [
        pinned["aa"]["cases"][0],
        pinned["z"]["cases"][0],
        pinned["ab"]["cases"][0],
        evidence[0],
    ]
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
        (2, ("problem", "mechanisms", 0, "worlds", 0, "models", 0, "forecast_risks", 0), [-1, 1]),
        (3, ("witness_laws", 0, "beliefs", 0, "weight"), [0, 1]),
        (
            3,
            (
                "witness_laws",
                0,
                "beliefs",
                0,
                "channels",
                3,
                "cells",
                0,
                "prediction",
                0,
                "probability",
            ),
            [0, 1],
        ),
        (3, ("witness_certificate_map", 0, "witness_id"), -1),
    ]
    for index, path, value in corruptions:
        changed = replaced(args[index], path, value)
        assert wire(changed) != wire(args[index])
        call = args.copy()
        call[index] = changed
        with pytest.raises(ValueError):
            runner.check_analysis(expected[0], call[0], call[1], call[2], letters, call[3])
