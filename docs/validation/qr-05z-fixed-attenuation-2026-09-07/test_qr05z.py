"""Independent Z fixed-attenuation scoring and boundary controls.

Pinned Y JSON supplies the complete experiment and certified baseline. No current or
previous raw-order executor is imported here; raw authentication is separate.
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
Y_SHA = "c4189b0f1bb0df4bb3e5f14c1969ede0ee754f59b4bc99e89aeac8d6b065891f"


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
    assert max(result.numerator.bit_length(), result.denominator.bit_length()) <= 4096
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


def symbol(index):
    return [0, 0, 0, 0, 0, 0, index]


def law(values):
    return [{"value": symbol(q), "probability": fw(p)} for q, p in sorted(values.items()) if p]


def read_law(prediction):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in prediction}


def bayes_risk(actual):
    assert sum(actual.values()) == 1
    # Disagreement of independent future draws, not risk of an arbitrary
    # point forecast computed under that forecast's own assumed truth.
    return sum(p * r for q, p in actual.items() for z, r in actual.items() if q != z)


def outcome_risk(actual, forecast):
    assert sum(actual.values()) == sum(forecast.values()) == 1
    alphabet = actual.keys() | forecast.keys()
    return sum(
        probability * sum((forecast.get(q, F(0)) - (q == truth)) ** 2 for q in alphabet)
        for truth, probability in actual.items()
    )


def squared_error(actual, forecast):
    return sum(
        (actual.get(q, F(0)) - forecast.get(q, F(0))) ** 2 for q in actual.keys() | forecast.keys()
    )


X_FIELDS = (
    "coverage",
    "unsupported_mass",
    "bayes_risk",
    "supported_bayes_risk",
    "supported_forecast_risk",
    "supported_regret",
    "forecast_risk",
    "regret",
    "complete",
)
SCORE_FIELDS = (
    "fallback_bayes_risk",
    "fallback_forecast_risk",
    "fallback_regret",
    "completed_forecast_risk",
    "completed_regret",
    "coarse_forecast_risk",
    "coarse_regret",
    "gain_over_coarse",
)
Y_CHECKS = (
    "policy_total",
    "mass_partition",
    "split_decomposition",
    "completed_decomposition",
    "coarse_decomposition",
    "gain_identity",
    "supported_forecasts_preserved",
    "zero_regret_iff_equal",
)


def independently_score_y(problem):
    rows = []
    input_cells = input_atoms = input_fallbacks = input_fallback_atoms = 0
    completed_terms = coarse_terms = 0
    for entry in problem["beliefs"]:
        channels = entry["channels"]
        fallback = {tuple(row["value"]): row["prediction"] for row in entry["fallbacks"]}
        input_cells += sum(len(channel["cells"]) for channel in channels)
        input_atoms += sum(
            len(cell["prediction"]) for channel in channels for cell in channel["cells"]
        )
        input_fallbacks += len(fallback)
        input_fallback_atoms += sum(map(len, fallback.values()))
        pairs = []
        for i, actual_channel in enumerate(channels):
            for j, assumed_channel in enumerate(channels):
                assumed_by = {tuple(cell["value"]): cell for cell in assumed_channel["cells"]}
                cells = []
                coverage = total_bayes = supported_bayes = supported_risk = supported_regret = F(0)
                fallback_bayes = fallback_risk = fallback_regret = F(0)
                completed_risk = completed_regret = coarse_risk = coarse_regret = gain = F(0)
                for actual in actual_channel["cells"]:
                    value = tuple(actual["value"])
                    p = read_law(actual["prediction"])
                    mass = fraction(actual["probability"])
                    assumed = assumed_by.get(value)
                    supported = assumed is not None
                    coarse_wire = fallback[value[:5]]
                    forecast_wire = assumed["prediction"] if supported else coarse_wire
                    f, g = read_law(forecast_wire), read_law(coarse_wire)
                    bayes = bayes_risk(p)
                    scored, regret = outcome_risk(p, f), squared_error(p, f)
                    coarse_scored, coarse_distance = outcome_risk(p, g), squared_error(p, g)
                    completed_terms += len(p) + len(f)
                    coarse_terms += len(p) + len(g)
                    equal, coarse_equal = p == f, p == g
                    local_gain = coarse_scored - scored
                    assert scored == bayes + regret
                    assert coarse_scored == bayes + coarse_distance
                    assert local_gain == coarse_distance - regret
                    assert (regret == 0) == equal and (coarse_distance == 0) == coarse_equal
                    assert 0 <= bayes <= 1
                    assert all(
                        0 <= score <= 2
                        for score in (scored, regret, coarse_scored, coarse_distance)
                    )
                    assert -2 <= local_gain <= 2
                    if supported:
                        coverage += mass
                        supported_bayes += mass * bayes
                        supported_risk += mass * scored
                        supported_regret += mass * regret
                        assert forecast_wire == assumed["prediction"]
                    else:
                        fallback_bayes += mass * bayes
                        fallback_risk += mass * scored
                        fallback_regret += mass * regret
                        assert forecast_wire == coarse_wire and local_gain == 0
                    total_bayes += mass * bayes
                    completed_risk += mass * scored
                    completed_regret += mass * regret
                    coarse_risk += mass * coarse_scored
                    coarse_regret += mass * coarse_distance
                    gain += mass * local_gain
                    cells.append(
                        {
                            "value": list(value),
                            "actual_probability": actual["probability"],
                            "assumed_probability": assumed["probability"] if supported else [0, 1],
                            "actual_prediction": actual["prediction"],
                            "assumed_forecast": assumed["prediction"] if supported else None,
                            "coarse_forecast": coarse_wire,
                            "forecast": forecast_wire,
                            "supported": supported,
                            "used_fallback": not supported,
                            "bayes_risk": fw(bayes),
                            "forecast_risk": fw(scored),
                            "regret": fw(regret),
                            "coarse_risk": fw(coarse_scored),
                            "coarse_regret": fw(coarse_distance),
                            "gain_over_coarse": fw(local_gain),
                            "predictions_equal": equal,
                            "coarse_predictions_equal": coarse_equal,
                        }
                    )
                complete = coverage == 1
                assert supported_risk == supported_bayes + supported_regret
                assert fallback_risk == fallback_bayes + fallback_regret
                assert total_bayes == supported_bayes + fallback_bayes
                assert (
                    completed_risk
                    == supported_risk + fallback_risk
                    == total_bayes + completed_regret
                )
                assert completed_regret == supported_regret + fallback_regret
                assert coarse_risk == total_bayes + coarse_regret
                assert gain == coarse_risk - completed_risk == coarse_regret - completed_regret
                assert abs(gain) <= 2 * coverage
                assert gain == sum(
                    fraction(c["actual_probability"]) * fraction(c["gain_over_coarse"])
                    for c in cells
                    if c["supported"]
                )
                assert (completed_regret == 0) == all(c["predictions_equal"] for c in cells)
                assert (coarse_regret == 0) == all(c["coarse_predictions_equal"] for c in cells)
                assert all(c["used_fallback"] is (not c["supported"]) for c in cells)
                pairs.append(
                    {
                        "actual_index": i,
                        "assumed_index": j,
                        "cells": cells,
                        "x_scores": {
                            "coverage": fw(coverage),
                            "unsupported_mass": fw(1 - coverage),
                            "bayes_risk": fw(total_bayes),
                            "supported_bayes_risk": fw(supported_bayes),
                            "supported_forecast_risk": fw(supported_risk),
                            "supported_regret": fw(supported_regret),
                            "forecast_risk": fw(supported_risk) if complete else None,
                            "regret": fw(supported_regret) if complete else None,
                            "complete": complete,
                        },
                        "fallback_bayes_risk": fw(fallback_bayes),
                        "fallback_forecast_risk": fw(fallback_risk),
                        "fallback_regret": fw(fallback_regret),
                        "completed_forecast_risk": fw(completed_risk),
                        "completed_regret": fw(completed_regret),
                        "coarse_forecast_risk": fw(coarse_risk),
                        "coarse_regret": fw(coarse_regret),
                        "gain_over_coarse": fw(gain),
                        "checks": dict.fromkeys(Y_CHECKS, True),
                    }
                )
        rows.append({"belief_id": entry["belief_id"], "weight": entry["weight"], "pairs": pairs})
    aggregate_pairs = []
    for index in range(16):
        complete_count = sum(row["pairs"][index]["x_scores"]["complete"] for row in rows)
        complete = complete_count == len(rows)
        x_scores = {
            key: fw(
                sum(
                    fraction(row["weight"]) * fraction(row["pairs"][index]["x_scores"][key])
                    for row in rows
                )
            )
            for key in X_FIELDS
            if key not in ("forecast_risk", "regret", "complete")
        }
        x_scores.update(
            {
                "forecast_risk": x_scores["supported_forecast_risk"] if complete else None,
                "regret": x_scores["supported_regret"] if complete else None,
                "complete": complete,
            }
        )
        scores = {
            key: fw(
                sum(fraction(row["weight"]) * fraction(row["pairs"][index][key]) for row in rows)
            )
            for key in SCORE_FIELDS
        }
        assert (fraction(x_scores["coverage"]) == 1) == complete
        assert fraction(x_scores["coverage"]) + fraction(x_scores["unsupported_mass"]) == 1
        assert fraction(scores["completed_forecast_risk"]) == (
            fraction(x_scores["supported_forecast_risk"])
            + fraction(scores["fallback_forecast_risk"])
        )
        assert fraction(scores["completed_regret"]) == (
            fraction(x_scores["supported_regret"]) + fraction(scores["fallback_regret"])
        )
        assert fraction(scores["completed_forecast_risk"]) == (
            fraction(x_scores["bayes_risk"]) + fraction(scores["completed_regret"])
        )
        assert fraction(scores["coarse_forecast_risk"]) == (
            fraction(x_scores["bayes_risk"]) + fraction(scores["coarse_regret"])
        )
        assert fraction(scores["gain_over_coarse"]) == (
            fraction(scores["coarse_regret"]) - fraction(scores["completed_regret"])
        )
        assert abs(fraction(scores["gain_over_coarse"])) <= 2 * fraction(x_scores["coverage"])
        for key, flag in (
            ("completed_regret", "predictions_equal"),
            ("coarse_regret", "coarse_predictions_equal"),
        ):
            assert (fraction(scores[key]) == 0) == all(
                c[flag] for row in rows for c in row["pairs"][index]["cells"]
            )
        aggregate_pairs.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "x_scores": x_scores,
                **scores,
                "checks": dict.fromkeys(Y_CHECKS, True),
                "complete_before_beliefs": complete_count,
                "incomplete_before_beliefs": len(rows) - complete_count,
            }
        )

    predicates = {
        "fallback": lambda pair: fraction(pair["x_scores"]["unsupported_mass"]) > 0,
        "positive_fallback_regret": lambda pair: fraction(pair["fallback_regret"]) > 0,
        "positive_completed_regret": lambda pair: fraction(pair["completed_regret"]) > 0,
        "better_than_coarse": lambda pair: fraction(pair["gain_over_coarse"]) > 0,
        "equal_to_coarse": lambda pair: fraction(pair["gain_over_coarse"]) == 0,
        "worse_than_coarse": lambda pair: fraction(pair["gain_over_coarse"]) < 0,
    }
    witnesses = {
        "first_" + name: [
            next((row["belief_id"] for row in rows if predicate(row["pairs"][i])), None)
            for i in range(16)
        ]
        for name, predicate in predicates.items()
    }
    counts = {
        "beliefs": len(rows),
        "input_cells": input_cells,
        "input_prediction_atoms": input_atoms,
        "input_fallbacks": input_fallbacks,
        "input_fallback_atoms": input_fallback_atoms,
        "pair_cells": [sum(len(row["pairs"][i]["cells"]) for row in rows) for i in range(16)],
        "supported_pair_cells": [
            sum(c["supported"] for row in rows for c in row["pairs"][i]["cells"]) for i in range(16)
        ],
        "fallback_pair_cells": [
            sum(c["used_fallback"] for row in rows for c in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "completed_scoring_terms": completed_terms,
        "coarse_scoring_terms": coarse_terms,
        "complete_before_beliefs": [
            sum(row["pairs"][i]["x_scores"]["complete"] for row in rows) for i in range(16)
        ],
        "incomplete_before_beliefs": [
            sum(not row["pairs"][i]["x_scores"]["complete"] for row in rows) for i in range(16)
        ],
        **{
            name + "_beliefs": [
                sum(predicates[name](row["pairs"][i]) for row in rows) for i in range(16)
            ]
            for name in (
                "positive_fallback_regret",
                "positive_completed_regret",
                "better_than_coarse",
                "equal_to_coarse",
                "worse_than_coarse",
            )
        },
    }
    return copy.deepcopy(
        {
            "input_sha256": digest(problem),
            "levels": LEVELS,
            "beliefs": rows,
            "aggregate": {"total_weight": [1, 1], "pairs": aggregate_pairs},
            "witnesses": witnesses,
            "counts": counts,
        }
    )


RETAINED_WEIGHTS = [[0, 1], [1, 2], [1, 1]]
Z_CHECKS = (
    "normalization",
    "score_decomposition",
    "quadratic_risk_identity",
    "quadratic_gain_identity",
    "endpoint_recovery",
    "fallback_preserved",
    "zero_regret_iff_equal",
    "jensen_bound",
)
BLEND_SCORES = ("forecast_risk", "regret", "gain_over_coarse", "gain_over_base")


def wrap(experiment):
    return {
        "schema_version": "det8-qr05z-problem-v1",
        "family": "qr05z_fixed_attenuation",
        "experiment": experiment,
    }


def law_wire(values):
    return [{"value": list(q), "probability": fw(p)} for q, p in sorted(values.items()) if p]


def independently_score(problem):
    baseline = independently_score_y(problem["experiment"])
    rows = []
    mixture_terms = distance_terms = blend_terms = blend_atoms = 0
    for old_row in baseline["beliefs"]:
        pairs = []
        for old_pair in old_row["pairs"]:
            cells = []
            for old in old_pair["cells"]:
                p, f, g = (
                    read_law(old[key])
                    for key in ("actual_prediction", "forecast", "coarse_forecast")
                )
                distance = F(0)
                for q, value in f.items():
                    distance += (value - g.get(q, F(0))) ** 2
                    distance_terms += 1
                for q, value in g.items():
                    if q not in f:
                        distance += value**2
                    distance_terms += 1
                assert 0 <= distance <= 2
                blends = []
                coarse_risk, base_risk = (
                    fraction(old["coarse_risk"]),
                    fraction(old["forecast_risk"]),
                )
                bayes, base_gain = fraction(old["bayes_risk"]), fraction(old["gain_over_coarse"])
                for retention in RETAINED_WEIGHTS:
                    a = fraction(retention)
                    mixture = {}
                    for q, probability in g.items():
                        mixture[q] = mixture.get(q, F(0)) + (1 - a) * probability
                        mixture_terms += 1
                    for q, probability in f.items():
                        mixture[q] = mixture.get(q, F(0)) + a * probability
                        mixture_terms += 1
                    h = {q: probability for q, probability in mixture.items() if probability}
                    assert sum(h.values()) == 1 and all(
                        probability > 0 for probability in h.values()
                    )
                    blend_atoms += len(h)
                    scored, regret = outcome_risk(p, h), squared_error(p, h)
                    blend_terms += len(p) + len(h)
                    gain, base_improvement = coarse_risk - scored, base_risk - scored
                    equal = p == h
                    assert scored == bayes + regret
                    assert scored == (1 - a) * coarse_risk + a * base_risk - a * (1 - a) * distance
                    assert gain == a * base_gain + a * (1 - a) * distance
                    assert base_improvement == gain - base_gain
                    assert 0 <= scored <= 2 and 0 <= regret <= 2
                    assert -2 <= gain <= 2 and -2 <= base_improvement <= 2
                    assert (regret == 0) == equal
                    assert scored <= (1 - a) * coarse_risk + a * base_risk
                    if a == 0:
                        assert h == g and scored == coarse_risk
                    elif a == 1:
                        assert h == f and scored == base_risk
                    else:
                        assert h.keys() == f.keys() | g.keys()
                    if old["used_fallback"]:
                        assert f == g == h and distance == 0 and scored == coarse_risk == base_risk
                    blends.append(
                        {
                            "retained_weight": retention,
                            "forecast": law_wire(h),
                            "forecast_risk": fw(scored),
                            "regret": fw(regret),
                            "gain_over_coarse": fw(gain),
                            "gain_over_base": fw(base_improvement),
                            "predictions_equal": equal,
                        }
                    )
                cells.append(
                    {"value": old["value"], "forecast_distance": fw(distance), "blends": blends}
                )
            distance = sum(
                fraction(old["actual_probability"]) * fraction(cell["forecast_distance"])
                for old, cell in zip(old_pair["cells"], cells, strict=True)
            )
            blends = []
            for index, retention in enumerate(RETAINED_WEIGHTS):
                a = fraction(retention)
                scores = {
                    key: sum(
                        fraction(old["actual_probability"]) * fraction(cell["blends"][index][key])
                        for old, cell in zip(old_pair["cells"], cells, strict=True)
                    )
                    for key in BLEND_SCORES
                }
                assert (
                    scores["forecast_risk"]
                    == fraction(old_pair["x_scores"]["bayes_risk"]) + scores["regret"]
                )
                assert scores["forecast_risk"] == (
                    (1 - a) * fraction(old_pair["coarse_forecast_risk"])
                    + a * fraction(old_pair["completed_forecast_risk"])
                    - a * (1 - a) * distance
                )
                assert scores["gain_over_coarse"] == (
                    a * fraction(old_pair["gain_over_coarse"]) + a * (1 - a) * distance
                )
                assert scores["gain_over_base"] == scores["gain_over_coarse"] - fraction(
                    old_pair["gain_over_coarse"]
                )
                assert (scores["regret"] == 0) == all(
                    c["blends"][index]["predictions_equal"] for c in cells
                )
                blends.append(
                    {
                        "retained_weight": retention,
                        **{key: fw(value) for key, value in scores.items()},
                    }
                )
            pairs.append(
                {
                    "actual_index": old_pair["actual_index"],
                    "assumed_index": old_pair["assumed_index"],
                    "cells": cells,
                    "forecast_distance": fw(distance),
                    "blends": blends,
                    "checks": dict.fromkeys(Z_CHECKS, True),
                }
            )
        rows.append(
            {"belief_id": old_row["belief_id"], "weight": old_row["weight"], "pairs": pairs}
        )
    aggregate = []
    for k in range(16):
        distance = sum(
            fraction(row["weight"]) * fraction(row["pairs"][k]["forecast_distance"]) for row in rows
        )
        blends = []
        old_pair = baseline["aggregate"]["pairs"][k]
        for index, retention in enumerate(RETAINED_WEIGHTS):
            a = fraction(retention)
            scores = {
                key: sum(
                    fraction(row["weight"]) * fraction(row["pairs"][k]["blends"][index][key])
                    for row in rows
                )
                for key in BLEND_SCORES
            }
            assert scores["forecast_risk"] == (
                (1 - a) * fraction(old_pair["coarse_forecast_risk"])
                + a * fraction(old_pair["completed_forecast_risk"])
                - a * (1 - a) * distance
            )
            assert scores["gain_over_coarse"] == (
                a * fraction(old_pair["gain_over_coarse"]) + a * (1 - a) * distance
            )
            assert scores["gain_over_base"] == scores["gain_over_coarse"] - fraction(
                old_pair["gain_over_coarse"]
            )
            assert (scores["regret"] == 0) == all(
                c["blends"][index]["predictions_equal"]
                for row in rows
                for c in row["pairs"][k]["cells"]
            )
            blends.append(
                {"retained_weight": retention, **{key: fw(value) for key, value in scores.items()}}
            )
        aggregate.append(
            {
                "actual_index": k // 4,
                "assumed_index": k % 4,
                "forecast_distance": fw(distance),
                "blends": blends,
                "checks": dict.fromkeys(Z_CHECKS, True),
            }
        )
    predicates = {
        "positive_regret": lambda blend: fraction(blend["regret"]) > 0,
        "better_than_coarse": lambda blend: fraction(blend["gain_over_coarse"]) > 0,
        "equal_to_coarse": lambda blend: fraction(blend["gain_over_coarse"]) == 0,
        "worse_than_coarse": lambda blend: fraction(blend["gain_over_coarse"]) < 0,
        "better_than_base": lambda blend: fraction(blend["gain_over_base"]) > 0,
        "equal_to_base": lambda blend: fraction(blend["gain_over_base"]) == 0,
        "worse_than_base": lambda blend: fraction(blend["gain_over_base"]) < 0,
    }
    witnesses = {
        "first_positive_deviation": [
            next(
                (
                    row["belief_id"]
                    for row in rows
                    if fraction(row["pairs"][k]["forecast_distance"]) > 0
                ),
                None,
            )
            for k in range(16)
        ],
        **{
            "first_" + name: [
                next(
                    (
                        row["belief_id"]
                        for row in rows
                        if predicate(row["pairs"][k]["blends"][index])
                    ),
                    None,
                )
                for k in range(16)
                for index in range(3)
            ]
            for name, predicate in predicates.items()
        },
    }
    baseline_terms = (
        baseline["counts"]["completed_scoring_terms"] + baseline["counts"]["coarse_scoring_terms"]
    )
    counts = {
        "beliefs": len(rows),
        "pair_cells": [sum(len(row["pairs"][k]["cells"]) for row in rows) for k in range(16)],
        "blend_cells": [
            sum(len(row["pairs"][k]["cells"]) for row in rows) for k in range(16) for _ in range(3)
        ],
        "blend_atoms": blend_atoms,
        "mixture_terms": mixture_terms,
        "distance_terms": distance_terms,
        "blend_scoring_terms": blend_terms,
        "baseline_scoring_terms": baseline_terms,
        "total_work_terms": baseline_terms + mixture_terms + distance_terms + blend_terms,
        "positive_deviation_beliefs": [
            sum(fraction(row["pairs"][k]["forecast_distance"]) > 0 for row in rows)
            for k in range(16)
        ],
        **{
            name + "_beliefs": [
                sum(predicate(row["pairs"][k]["blends"][index]) for row in rows)
                for k in range(16)
                for index in range(3)
            ]
            for name, predicate in predicates.items()
        },
    }
    return copy.deepcopy(
        {
            "input_sha256": digest(problem),
            "levels": LEVELS,
            "retained_weights": RETAINED_WEIGHTS,
            "baseline": baseline,
            "beliefs": rows,
            "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
            "witnesses": witnesses,
            "counts": counts,
        }
    )


@pytest.fixture(scope="session")
def pinned_y():
    path = HERE.parent / "qr-05y-explicit-fallback-2026-09-07" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 16474309 and hashlib.sha256(raw).hexdigest() == Y_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


def case_problem(case):
    return wrap(copy.deepcopy(case["problem"]))


@pytest.fixture(scope="session")
def problems(pinned_y):
    return [case_problem(case) for case in pinned_y["cases"]]


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05z_test_direct", "attenuation.py"),
        private_module("_qr05z_test_reference", "reference_qr05z.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, problems):
    result = []
    for p in problems:
        before = wire(p)
        result.append(tuple(module.analyze(p) for module in executors))
        assert wire(p) == before
    return result


@pytest.fixture(scope="session")
def expected(problems):
    return [independently_score(p) for p in problems]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05z_test_runner", "study.py")
    return runner, runner.run_suite()


def cell(report, probability, prediction):
    return {"value": symbol(report), "probability": fw(probability), "prediction": law(prediction)}


def problem_of(channels):
    marginal = {}
    prefixes = set()
    for channel in channels:
        prefixes.update(tuple(c["value"][:5]) for c in channel)
    for c in channels[0]:
        for q, probability in read_law(c["prediction"]).items():
            marginal[q] = marginal.get(q, F(0)) + fraction(c["probability"]) * probability
    prediction = [
        {"value": list(q), "probability": fw(p)} for q, p in sorted(marginal.items()) if p
    ]
    return {
        "schema_version": "det8-qr05y-problem-v1",
        "family": "qr05y_explicit_fallback",
        "beliefs": [
            {
                "belief_id": 0,
                "weight": [1, 1],
                "channels": [
                    {"level": list(level), "cells": copy.deepcopy(cells)}
                    for level, cells in zip(LEVELS, channels, strict=True)
                ],
                "fallbacks": [
                    {"value": list(prefix), "prediction": copy.deepcopy(prediction)}
                    for prefix in sorted(prefixes)
                ],
            }
        ],
    }


def binary_channels(prior=F(1, 2)):
    channels = []
    for level in LEVELS:
        t = fraction(level)
        cells = []
        for z in (0, 1):
            joint = {
                q: probability * ((1 - t) * (z == q) + t / 2)
                for q, probability in ((0, prior), (1, 1 - prior))
            }
            mass = sum(joint.values())
            if mass:
                cells.append(cell(z, mass, {q: p / mass for q, p in joint.items() if p}))
        channels.append(cells)
    return channels


def micro_problem(kind="balanced"):
    actual = [cell(0, F(1, 2), {0: F(1)}), cell(1, F(1, 2), {1: F(1)})]
    if kind in ("balanced", "biased"):
        return problem_of(binary_channels(F(1, 2) if kind == "balanced" else F(3, 4)))
    if kind == "opposed":
        swapped = [cell(0, F(1, 2), {1: F(1)}), cell(1, F(1, 2), {0: F(1)})]
        return problem_of([actual, swapped, actual, swapped])
    if kind == "disjoint":
        return problem_of([[cell(i, F(1), {0: F(1)})] for i in range(4)])
    if kind == "partial":
        actual = [cell(0, F(1, 4), {0: F(1)}), cell(1, F(3, 4), {1: F(1)})]
        assumed = [
            cell(0, F(1, 2), {1: F(1)}),
            cell(2, F(1, 2), {0: F(1, 2), 1: F(1, 2)}),
        ]
        p = problem_of([actual, assumed, actual, assumed])
        p["beliefs"][0]["fallbacks"][0]["prediction"] = law({0: F(1, 2), 1: F(1, 2)})
        return p
    if kind == "same_law":
        shared = {0: F(1, 2), 1: F(1, 2)}
        return problem_of(
            [
                [cell(0, probability, shared), cell(1, 1 - probability, shared)]
                for probability in (F(1, 4), F(1, 2), F(3, 4), F(1, 3))
            ]
        )
    if kind == "equal_scalar":
        a, b = {0: F(1, 4), 1: F(3, 4)}, {0: F(3, 4), 1: F(1, 4)}
        actual = [cell(0, F(1, 2), a), cell(1, F(1, 2), b)]
        swapped = [cell(0, F(1, 2), b), cell(1, F(1, 2), a)]
        return problem_of([actual, swapped, actual, swapped])
    raise ValueError("unknown test fixture")


def multi_prefix_problem():
    actual = [cell(0, F(1, 2), {0: F(1)}), cell(1, F(1, 2), {1: F(1)})]
    swapped = [cell(0, F(1, 2), {1: F(1)}), cell(1, F(1, 2), {0: F(1)})]
    for channel in (actual, swapped):
        channel[1]["value"][0] = 1
    p = problem_of([actual, swapped, actual, swapped])
    p["beliefs"][0]["fallbacks"] = [
        {"value": [0, 0, 0, 0, 0], "prediction": law({0: F(1)})},
        {"value": [1, 0, 0, 0, 0], "prediction": law({1: F(1)})},
    ]
    return p


def tiny_problem(probability):
    actual = [cell(0, F(1), {0: F(1)})]
    assumed = [cell(z, p, {0: F(1)}) for z, p in ((0, probability), (1, 1 - probability)) if p]
    p = problem_of([actual, assumed, actual, actual])
    p["beliefs"][0]["fallbacks"][0]["prediction"] = law({1: F(1)})
    return p


def adverse_fallback_problem():
    p = micro_problem("disjoint")
    p["beliefs"][0]["fallbacks"][0]["prediction"] = law({2: F(1)})
    return p


def midpoint_problem():
    actual = [cell(0, F(1), {0: F(1, 2), 1: F(1, 2)})]
    assumed = [cell(0, F(1, 2), {1: F(1)}), cell(1, F(1, 2), {0: F(1)})]
    p = problem_of([actual, assumed, actual, assumed])
    p["beliefs"][0]["fallbacks"][0]["prediction"] = law({0: F(1)})
    return wrap(p)


@pytest.fixture(scope="session")
def micro_analyses(executors):
    inputs = {
        "midpoint": midpoint_problem(),
        "multi_prefix": wrap(multi_prefix_problem()),
        "adverse_fallback": wrap(adverse_fallback_problem()),
        "partial": wrap(micro_problem("partial")),
        "zero": wrap(tiny_problem(F(0))),
        "tiny": wrap(tiny_problem(F(1, 1 << 256))),
    }
    result = {}
    for kind, p in inputs.items():
        a, b = (module.analyze(p) for module in executors)
        assert wire(a) == wire(b) == wire(independently_score(p))
        result[kind] = a
    return result


@pytest.mark.parametrize("case_index", range(6))
def test_all_six_complete_Z_wires_equal_literal_loss_and_full_mixture_oracle(
    analyses, expected, case_index
):
    a, b = analyses[case_index]
    assert wire(a) == wire(b) == wire(expected[case_index])
    assert wire(json.loads(wire(a))) == wire(a)
    assert len(wire(a)) <= 128 * 1024 * 1024


def test_generic_json_audit_matches_complete_schema_counts_and_equality_witnesses():
    audit = private_module("_qr05z_test_json_audit_generic", "audit_json.py")
    for problem in (midpoint_problem(), wrap(adverse_fallback_problem())):
        baseline = independently_score_y(problem["experiment"])
        before = wire(problem), wire(baseline)
        assert wire(audit.expected_z(problem, baseline)) == wire(independently_score(problem))
        assert (wire(problem), wire(baseline)) == before


def test_entire_Y_baseline_and_original_X_nulls_are_preserved(pinned_y, problems, expected):
    assert sum(len(case["problem"]["beliefs"]) for case in pinned_y["cases"]) == 482
    for old, p, a in zip(pinned_y["cases"], problems, expected, strict=True):
        assert p["experiment"] == old["problem"]
        assert a["input_sha256"] == digest(p)
        assert a["baseline"]["input_sha256"] == digest(p["experiment"])
        assert wire(a["baseline"]) == wire(old["analysis"])
        for row, baseline in zip(a["beliefs"], a["baseline"]["beliefs"], strict=True):
            assert row["belief_id"] == baseline["belief_id"] and row["weight"] == baseline["weight"]
            for pair, original in zip(row["pairs"], baseline["pairs"], strict=True):
                assert [c["value"] for c in pair["cells"]] == [
                    c["value"] for c in original["cells"]
                ]
                assert pair["blends"][0]["forecast_risk"] == original["coarse_forecast_risk"]
                assert pair["blends"][2]["forecast_risk"] == original["completed_forecast_risk"]
                assert pair["blends"][2]["gain_over_coarse"] == original["gain_over_coarse"]
                assert pair["blends"][2]["gain_over_base"] == [0, 1]


def test_family_specific_quadratic_controls_are_verified_from_complete_endpoint_laws(expected):
    for a in expected:
        for row, baseline in zip(a["beliefs"], a["baseline"]["beliefs"], strict=True):
            for pair, old in zip(row["pairs"], baseline["pairs"], strict=True):
                for c, source in zip(pair["cells"], old["cells"], strict=True):
                    distance = fraction(c["forecast_distance"])
                    if pair["actual_index"] == 3:
                        assert source["actual_prediction"] == source["coarse_forecast"]
                        for b in c["blends"]:
                            weight = fraction(b["retained_weight"])
                            assert fraction(b["gain_over_coarse"]) == -(weight**2) * distance
                    if pair["actual_index"] == pair["assumed_index"]:
                        assert source["actual_prediction"] == source["forecast"]
                        for b in c["blends"]:
                            assert (
                                fraction(b["regret"])
                                == (1 - fraction(b["retained_weight"])) ** 2 * distance
                            )
                    if pair["assumed_index"] == 3 or source["used_fallback"]:
                        assert source["forecast"] == source["coarse_forecast"]
                        assert c["forecast_distance"] == [0, 1]
                        assert all(b["forecast"] == source["coarse_forecast"] for b in c["blends"])


def test_all_weighting_indices_counts_and_first_sign_witnesses_refer_to_retained_objects(expected):
    predicates = {
        "positive_regret": lambda b: fraction(b["regret"]) > 0,
        "better_than_coarse": lambda b: fraction(b["gain_over_coarse"]) > 0,
        "equal_to_coarse": lambda b: fraction(b["gain_over_coarse"]) == 0,
        "worse_than_coarse": lambda b: fraction(b["gain_over_coarse"]) < 0,
        "better_than_base": lambda b: fraction(b["gain_over_base"]) > 0,
        "equal_to_base": lambda b: fraction(b["gain_over_base"]) == 0,
        "worse_than_base": lambda b: fraction(b["gain_over_base"]) < 0,
    }
    for a in expected:
        rows = a["beliefs"]
        for k, pair in enumerate(a["aggregate"]["pairs"]):
            assert pair["forecast_distance"] == fw(
                sum(
                    fraction(row["weight"]) * fraction(row["pairs"][k]["forecast_distance"])
                    for row in rows
                )
            )
            for index, blend in enumerate(pair["blends"]):
                slot = 3 * k + index
                assert slot == 12 * pair["actual_index"] + 3 * pair["assumed_index"] + index
                for key in BLEND_SCORES:
                    assert blend[key] == fw(
                        sum(
                            fraction(row["weight"])
                            * fraction(row["pairs"][k]["blends"][index][key])
                            for row in rows
                        )
                    )
                for name, predicate in predicates.items():
                    ids = [
                        row["belief_id"]
                        for row in rows
                        if predicate(row["pairs"][k]["blends"][index])
                    ]
                    assert a["witnesses"]["first_" + name][slot] == (ids[0] if ids else None)
                    assert a["counts"][name + "_beliefs"][slot] == len(ids)
                assert a["counts"]["blend_cells"][slot] == sum(
                    len(row["pairs"][k]["cells"]) for row in rows
                )
        assert a["counts"]["baseline_scoring_terms"] == (
            a["baseline"]["counts"]["completed_scoring_terms"]
            + a["baseline"]["counts"]["coarse_scoring_terms"]
        )
        assert a["counts"]["total_work_terms"] == sum(
            a["counts"][key]
            for key in (
                "baseline_scoring_terms",
                "mixture_terms",
                "distance_terms",
                "blend_scoring_terms",
            )
        )


def test_midpoint_can_beat_equal_risk_distinct_endpoint_forecasts(micro_analyses):
    a = micro_analyses["midpoint"]
    pair = a["beliefs"][0]["pairs"][1]
    assert pair["forecast_distance"] == [2, 1]
    assert [b["forecast_risk"] for b in pair["blends"]] == [[1, 1], [1, 2], [1, 1]]
    assert [b["gain_over_coarse"] for b in pair["blends"]] == [[0, 1], [1, 2], [0, 1]]
    c = pair["cells"][0]
    assert c["blends"][0]["forecast"] != c["blends"][2]["forecast"]
    assert [b["predictions_equal"] for b in c["blends"]] == [False, True, False]
    assert c["blends"][1]["forecast"] == law({0: F(1, 2), 1: F(1, 2)})
    assert a["witnesses"]["first_equal_to_coarse"][5] == 0
    assert a["witnesses"]["first_positive_deviation"][1] == 0


def test_correct_coarse_harmful_detail_and_correct_detail_wrong_coarse_keep_signed_gains(
    micro_analyses,
):
    row = micro_analyses["multi_prefix"]["beliefs"][0]
    harmful, helpful = row["pairs"][1], row["pairs"][5]
    assert [b["forecast_risk"] for b in harmful["blends"]] == [[0, 1], [1, 2], [2, 1]]
    assert [b["gain_over_coarse"] for b in harmful["blends"]] == [[0, 1], [-1, 2], [-2, 1]]
    assert [b["forecast_risk"] for b in helpful["blends"]] == [[2, 1], [1, 2], [0, 1]]
    assert [b["gain_over_coarse"] for b in helpful["blends"]] == [[0, 1], [3, 2], [2, 1]]
    assert [b["gain_over_base"] for b in helpful["blends"]] == [[-2, 1], [-1, 2], [0, 1]]
    # The generic API does not impose W's actual-full-replacement law.
    assert any(fraction(c["forecast_distance"]) > 0 for c in row["pairs"][15]["cells"])


def test_positive_generic_fallback_regret_is_unchanged_and_forecasts_need_not_have_true_marginal(
    micro_analyses,
):
    a = micro_analyses["adverse_fallback"]
    pair = a["beliefs"][0]["pairs"][1]
    baseline = a["baseline"]["beliefs"][0]["pairs"][1]
    assert baseline["x_scores"]["forecast_risk"] is None
    assert pair["forecast_distance"] == [0, 1]
    assert all(b["forecast_risk"] == b["regret"] == [2, 1] for b in pair["blends"])
    assert all(b["gain_over_coarse"] == b["gain_over_base"] == [0, 1] for b in pair["blends"])
    c = pair["cells"][0]
    assert all(b["forecast"] == law({2: F(1)}) for b in c["blends"])
    assert baseline["cells"][0]["actual_prediction"] == law({0: F(1)})
    assert all(b["forecast"] != baseline["cells"][0]["actual_prediction"] for b in c["blends"])


def test_complete_union_atoms_are_retained_at_midpoint_and_pruned_only_at_exact_endpoints(
    micro_analyses,
):
    a = micro_analyses["adverse_fallback"]
    c = a["beliefs"][0]["pairs"][0]["cells"][0]
    assert c["blends"][0]["forecast"] == law({2: F(1)})
    assert c["blends"][1]["forecast"] == law({0: F(1, 2), 2: F(1, 2)})
    assert c["blends"][2]["forecast"] == law({0: F(1)})
    assert [len(b["forecast"]) for b in c["blends"]] == [1, 2, 1]


def test_tiny_positive_assumed_support_is_not_attenuated_into_a_fallback_branch(micro_analyses):
    zero = micro_analyses["zero"]["beliefs"][0]["pairs"][1]
    tiny = micro_analyses["tiny"]["beliefs"][0]["pairs"][1]
    assert [b["forecast_risk"] for b in zero["blends"]] == [[2, 1]] * 3
    assert [b["forecast_risk"] for b in tiny["blends"]] == [[2, 1], [1, 2], [0, 1]]
    assert micro_analyses["tiny"]["baseline"]["beliefs"][0]["pairs"][1]["cells"][0][
        "assumed_probability"
    ] == [1, 1 << 256]


def test_no_actual_index_selects_weight_or_changes_chosen_mixed_law(micro_analyses):
    for a in micro_analyses.values():
        assert a["retained_weights"] == RETAINED_WEIGHTS
        for row in a["beliefs"]:
            for j in range(4):
                seen = {}
                for i in range(4):
                    for c in row["pairs"][4 * i + j]["cells"]:
                        for index, blend in enumerate(c["blends"]):
                            key = tuple(c["value"]), index
                            if key in seen:
                                assert blend["forecast"] == seen[key]
                            seen[key] = blend["forecast"]


def test_uneven_report_weights_and_jensen_do_not_imply_midpoint_beats_both_endpoints(
    micro_analyses,
):
    a = micro_analyses["partial"]
    pair = a["beliefs"][0]["pairs"][1]
    assert pair["forecast_distance"] == [1, 8]
    assert [b["forecast_risk"] for b in pair["blends"]] == [[1, 2], [21, 32], [7, 8]]
    assert pair["blends"][1]["gain_over_coarse"] == [-5, 32]
    assert pair["blends"][1]["gain_over_base"] == [7, 32]
    unweighted = sum(fraction(c["blends"][1]["forecast_risk"]) for c in pair["cells"]) / 2
    assert unweighted == F(13, 16) != F(21, 32)


def test_original_history_weights_are_preserved_at_every_retained_weight(executors):
    inner = micro_problem("balanced")
    inner["beliefs"][0]["weight"] = [1, 4]
    other = micro_problem("partial")["beliefs"][0]
    inner["beliefs"].append({**other, "belief_id": 1, "weight": [3, 4]})
    p = wrap(inner)
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        midpoint = a["aggregate"]["pairs"][1]["blends"][1]
        assert midpoint["forecast_risk"] == [9, 16]
        assert midpoint["gain_over_coarse"] == [-1, 16]
        assert midpoint["gain_over_base"] == [1, 8]
        uniform = (
            sum(fraction(r["pairs"][1]["blends"][1]["forecast_risk"]) for r in a["beliefs"]) / 2
        )
        assert uniform == F(15, 32) != F(9, 16)


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_experiments():
    p = micro_problem()
    cases = [
        None,
        [],
        {},
        DictChild(p),
        {**p, "extra": 0},
        {**p, "fallback": "uniform"},
        {**p, "family": "other"},
        {**p, "schema_version": "det8-qr05w-problem-v1"},
        {**p, "beliefs": []},
    ]
    mutations = [
        (("schema_version",), StrChild(p["schema_version"])),
        (("beliefs",), ListChild(p["beliefs"])),
        (("beliefs", 0), DictChild(p["beliefs"][0])),
        (("beliefs", 0, "belief_id"), False),
        (("beliefs", 0, "belief_id"), 1),
        (("beliefs", 0, "weight"), [0, 1]),
        (("beliefs", 0, "weight"), [1, 2]),
        (("beliefs", 0, "weight"), [2, 2]),
        (("beliefs", 0, "weight"), [True, 1]),
        (("beliefs", 0, "weight"), (1, 1)),
        (("beliefs", 0, "channels"), []),
        (("beliefs", 0, "channels"), p["beliefs"][0]["channels"][:3]),
        (("beliefs", 0, "channels"), p["beliefs"][0]["channels"] + p["beliefs"][0]["channels"][:1]),
        (("beliefs", 0, "channels", 0, "level"), [1, 1]),
        (("beliefs", 0, "channels", 1, "level"), [2, 4]),
        (("beliefs", 0, "channels", 0, "level"), [False, 1]),
        (("beliefs", 0, "channels", 0, "cells"), []),
        (
            ("beliefs", 0, "channels", 0, "cells"),
            list(reversed(p["beliefs"][0]["channels"][0]["cells"])),
        ),
        (("beliefs", 0, "channels", 0, "cells"), [p["beliefs"][0]["channels"][0]["cells"][0]] * 2),
        (("beliefs", 0, "channels", 0, "cells", 0, "value"), [0] * 6),
        (("beliefs", 0, "channels", 0, "cells", 0, "value"), [0] * 8),
        (("beliefs", 0, "channels", 0, "cells", 0, "value", 0), True),
        (("beliefs", 0, "channels", 0, "cells", 0, "value", 0), IntChild(0)),
        (("beliefs", 0, "channels", 0, "cells", 0, "value", 0), -1),
        (("beliefs", 0, "channels", 0, "cells", 0, "value", 0), 1 << 64),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [0, 1]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [1, 3]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [2, 4]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [2, 1]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [-1, 2]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [1, 0]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [1.0, 2]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [True, 2]),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), "1/2"),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), (1, 2)),
        (("beliefs", 0, "channels", 0, "cells", 0, "probability"), [1, 1 << 4096]),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction"), []),
        (
            ("beliefs", 0, "channels", 0, "cells", 0, "prediction"),
            (p["beliefs"][0]["channels"][0]["cells"][0]["prediction"] * 2),
        ),
        (
            ("beliefs", 0, "channels", 1, "cells", 0, "prediction"),
            list(reversed(p["beliefs"][0]["channels"][1]["cells"][0]["prediction"])),
        ),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value", 0), False),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value", 0), -1),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value", 0), 1 << 64),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value"), tuple(symbol(0))),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "probability"), [0, 1]),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "probability"), [1, 2]),
        (("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "probability"), [2, 2]),
    ]
    cases += [replaced(p, path, value) for path, value in mutations]
    cases.append({StrChild(k): value for k, value in p.items()})
    for path in (
        ("beliefs", 0),
        ("beliefs", 0, "channels", 0),
        ("beliefs", 0, "channels", 0, "cells", 0),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0),
    ):
        item = p
        for key in path:
            item = item[key]
        cases.append(replaced(p, path, {**item, "extra": 0}))
        cases.append(replaced(p, path, {k: v for k, v in item.items() if k != next(iter(item))}))
    # Each modified channel remains normalized, but has the wrong shared
    # unconditional future. Normalization alone must not certify it.
    cases.append(
        replaced(
            p,
            ("beliefs", 0, "channels", 1, "cells"),
            [cell(0, F(1, 2), {0: F(1)}), cell(1, F(1, 2), {0: F(1)})],
        )
    )
    fallback = p["beliefs"][0]["fallbacks"]
    cases.append(
        {
            **p,
            "beliefs": [
                {key: value for key, value in p["beliefs"][0].items() if key != "fallbacks"}
            ],
        }
    )
    mutations = [
        (("beliefs", 0, "fallbacks"), []),
        (("beliefs", 0, "fallbacks"), ListChild(fallback)),
        (("beliefs", 0, "fallbacks"), fallback * 2),
        (("beliefs", 0, "fallbacks", 0), DictChild(fallback[0])),
        (("beliefs", 0, "fallbacks", 0, "value"), [0] * 4),
        (("beliefs", 0, "fallbacks", 0, "value"), [0] * 6),
        (("beliefs", 0, "fallbacks", 0, "value", 0), True),
        (("beliefs", 0, "fallbacks", 0, "value", 0), IntChild(0)),
        (("beliefs", 0, "fallbacks", 0, "value", 0), -1),
        (("beliefs", 0, "fallbacks", 0, "value", 0), 1 << 64),
        (("beliefs", 0, "fallbacks", 0, "value"), [1, 0, 0, 0, 0]),
        (("beliefs", 0, "fallbacks", 0, "prediction"), []),
        (("beliefs", 0, "fallbacks", 0, "prediction"), fallback[0]["prediction"] * 2),
        (("beliefs", 0, "fallbacks", 0, "prediction"), list(reversed(fallback[0]["prediction"]))),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "value", 0), False),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "value"), tuple(symbol(0))),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), [0, 1]),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), [1, 3]),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), [-1, 2]),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), [2, 4]),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), [1.0, 2]),
        (("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"), (1, 2)),
    ]
    cases += [replaced(p, path, value) for path, value in mutations]
    cases.append(
        replaced(
            p,
            ("beliefs", 0, "fallbacks"),
            fallback + [{"value": [1, 0, 0, 0, 0], "prediction": law({0: F(1)})}],
        )
    )
    for path in (("beliefs", 0, "fallbacks", 0), ("beliefs", 0, "fallbacks", 0, "prediction", 0)):
        item = p
        for key in path:
            item = item[key]
        cases.append(replaced(p, path, {**item, "extra": 0}))
        cases.append(
            replaced(
                p, path, {key: value for key, value in item.items() if key != next(iter(item))}
            )
        )
    multi = multi_prefix_problem()
    cases.append(
        replaced(
            multi, ("beliefs", 0, "fallbacks"), list(reversed(multi["beliefs"][0]["fallbacks"]))
        )
    )
    return cases


def invalid_problems():
    valid = wrap(micro_problem())
    cases = [wrap(bad) for bad in invalid_experiments()]
    cases.extend(
        [
            None,
            [],
            {},
            DictChild(valid),
            {**valid, "extra": 0},
            {**valid, "weights": [[0, 1], [1, 1]]},
            {**valid, "selector": "actual_best"},
            {**valid, "artifact": "results.json"},
            {**valid, "schema_version": "det8-qr05y-problem-v1"},
            {**valid, "family": "other"},
            {key: value for key, value in valid.items() if key != "experiment"},
            {**valid, "schema_version": StrChild(valid["schema_version"])},
            {StrChild(key): value for key, value in valid.items()},
            {**valid, "experiment": DictChild(valid["experiment"])},
        ]
    )
    return cases


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_outer_and_inherited_inner_native_contracts_reject_without_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def singleton_problem(denominator=11):
    pred = {0: F(1, denominator), 1: F(denominator - 1, denominator)}
    return wrap(problem_of([[cell(0, F(1), pred)]] * 4))


def midpoint_overflow_problem():
    m = 1 << 2046
    denominator = m * m + 1
    u, v = F(1 - m * m, 8 * denominator), F(m, 4 * denominator)
    g = {0: F(1, 4) + u, 1: F(1, 4) - u, 2: F(1, 4) + v, 3: F(1, 4) - v}
    uniform = dict.fromkeys(range(4), F(1, 4))
    inner = problem_of([[cell(0, F(1), uniform)]] * 4)
    inner["beliefs"][0]["fallbacks"][0]["prediction"] = law(g)
    assert sum(g.values()) == 1 and sum(value**2 for value in g.values()) == F(9, 32)
    assert max(value.denominator.bit_length() for value in g.values()) == 4096
    assert max(((g[q] + F(1, 4)) / 2).denominator.bit_length() for q in g) == 4097
    return wrap(inner)


def test_new_midpoint_probability_overflow_is_distinct_from_valid_carried_Y_scores(executors):
    p = midpoint_overflow_problem()
    baseline = independently_score_y(p["experiment"])
    native(baseline)
    pair = baseline["beliefs"][0]["pairs"][0]
    assert pair["completed_forecast_risk"] == [3, 4]
    assert pair["coarse_forecast_risk"] == [25, 32]
    assert pair["gain_over_coarse"] == [1, 32]
    for module in executors:
        assert wire(module._analyze_y(p["experiment"])) == wire(baseline)
        with pytest.raises(ValueError):
            module.analyze(p)


def test_large_intermediate_cancellation_remains_valid_and_retained_overflow_still_fails(executors):
    denominator = 1 << 4095
    prediction = {0: F(1, 2), 1: F(1, 2)}
    cells = [
        cell(0, F(1, denominator), prediction),
        cell(1, F(denominator - 1, denominator), prediction),
    ]
    p = wrap(problem_of([cells] * 4))
    assert (2 * denominator).bit_length() == 4097
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert all(
            b["forecast_risk"] == [1, 2] and b["regret"] == [0, 1]
            for pair in a["beliefs"][0]["pairs"]
            for b in pair["blends"]
        )
        with pytest.raises(ValueError):
            module.analyze(singleton_problem((1 << 2048) + 1))


def mutable_ids(value):
    seen, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in seen:
            continue
        seen.add(id(item))
        stack.extend(item.values() if type(item) is dict else item)
    return seen


def shared_problem():
    inner = micro_problem("same_law")
    shared = inner["beliefs"][0]["channels"][0]["cells"][0]["prediction"]
    for channel in inner["beliefs"][0]["channels"]:
        for c in channel["cells"]:
            c["prediction"] = shared
    inner["beliefs"][0]["fallbacks"][0]["prediction"] = shared
    return wrap(inner)


def test_entire_output_baseline_and_three_laws_are_detached_from_inputs_and_other_calls(executors):
    for module in executors:
        p = shared_problem()
        a, b = module.analyze(p), module.analyze(p)
        before, wanted = wire(p), wire(b)
        assert wire(a) == wire(independently_score(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(b))
        a["baseline"]["beliefs"][0]["pairs"][0]["cells"][0]["forecast"][0]["value"][0] = 99
        a["beliefs"][0]["pairs"][0]["cells"][0]["blends"][1]["forecast"][0]["probability"][0] = -1
        a["retained_weights"][0][0] = 99
        assert wire(p) == before and wire(b) == wanted and wire(module.analyze(p)) == wanted
        bad = replaced(p, ("experiment", "beliefs", 0, "belief_id"), IntChild(0))
        with pytest.raises(ValueError):
            module.analyze(bad)
        p["experiment"]["beliefs"][0]["channels"][0]["cells"][0]["probability"][0] = -1
        assert wire(b) == wanted
        with pytest.raises(ValueError):
            module.analyze(p)


def planned_work(p):
    pair_cells = atoms = baseline = mixture = distance = scored = 0
    for b in p["experiment"]["beliefs"]:
        fallback = {tuple(row["value"]): read_law(row["prediction"]) for row in b["fallbacks"]}
        for actual in b["channels"]:
            for assumed in b["channels"]:
                forecasts = {tuple(c["value"]): read_law(c["prediction"]) for c in assumed["cells"]}
                for c in actual["cells"]:
                    truth = read_law(c["prediction"])
                    g = fallback[tuple(c["value"][:5])]
                    f = forecasts.get(tuple(c["value"]), g)
                    support_sizes = [len(g), len(f.keys() | g.keys()), len(f)]
                    pair_cells += 1
                    baseline += 2 * len(truth) + len(f) + len(g)
                    atoms += sum(support_sizes)
                    mixture += 3 * (len(f) + len(g))
                    distance += len(f) + len(g)
                    scored += 3 * len(truth) + sum(support_sizes)
    return {
        "pair_cells": pair_cells,
        "blend_cells": 3 * pair_cells,
        "blend_atoms": atoms,
        "baseline_scoring_terms": baseline,
        "mixture_terms": mixture,
        "distance_terms": distance,
        "blend_scoring_terms": scored,
        "total_work_terms": baseline + mixture + distance + scored,
    }


def test_all_work_is_preplanned_before_any_Y_or_Z_forecast_score_and_evaluated_exactly(
    executors, monkeypatch
):
    p = wrap(adverse_fallback_problem())
    plan = planned_work(p)
    caps = {
        "MAX_PAIR_CELLS": "pair_cells",
        "MAX_SCORING_TERMS": "baseline_scoring_terms",
        "MAX_BLEND_CELLS": "blend_cells",
        "MAX_BLEND_ATOMS": "blend_atoms",
        "MAX_TOTAL_WORK_TERMS": "total_work_terms",
    }
    for module, helper in zip(executors, ("_score", "_score_supported"), strict=True):
        original, calls = getattr(module, helper), []

        def observed(*args, original=original, calls=calls, **kwargs):
            calls.append(1)
            return original(*args, **kwargs)

        with monkeypatch.context() as patched:
            patched.setattr(module, helper, observed)
            a = module.analyze(p)
        assert len(calls) == 5 * plan["pair_cells"]
        for key in (
            "blend_atoms",
            "baseline_scoring_terms",
            "mixture_terms",
            "distance_terms",
            "blend_scoring_terms",
            "total_work_terms",
        ):
            assert a["counts"][key] == plan[key]
        assert sum(a["counts"]["blend_cells"]) == plan["blend_cells"]
        for constant, key in caps.items():

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("Y or Z score loop began before complete Z work preflight")

            with monkeypatch.context() as patched:
                patched.setattr(module, constant, plan[key] - 1)
                patched.setattr(module, helper, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)


@pytest.mark.parametrize(
    "constant",
    [
        "MAX_BELIEFS",
        "MAX_CELLS_PER_CHANNEL",
        "MAX_ATOMS_PER_PREDICTION",
        "MAX_INPUT_CELLS",
        "MAX_INPUT_PREDICTION_ATOMS",
        "MAX_FALLBACKS_PER_BELIEF",
        "MAX_INPUT_FALLBACKS",
        "MAX_INPUT_FALLBACK_ATOMS",
        "MAX_PAIR_CELLS",
        "MAX_SCORING_TERMS",
        "MAX_BITS",
        "MAX_DEPTH",
        "MAX_NODES",
        "MAX_BYTES",
        "MAX_BLEND_CELLS",
        "MAX_BLEND_ATOMS",
        "MAX_TOTAL_WORK_TERMS",
    ],
)
def test_all_inherited_and_new_live_caps_fail_instead_of_truncating(
    executors, monkeypatch, constant
):
    p = wrap(micro_problem())
    if constant == "MAX_BELIEFS":
        p["experiment"]["beliefs"][0]["weight"] = [1, 2]
        p["experiment"]["beliefs"].append(
            {**copy.deepcopy(p["experiment"]["beliefs"][0]), "belief_id": 1}
        )
    if constant in ("MAX_FALLBACKS_PER_BELIEF", "MAX_INPUT_FALLBACKS"):
        p = wrap(multi_prefix_problem())
    if constant == "MAX_BITS":
        p = singleton_problem()
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as patched:
            patched.setattr(module, constant, 6 if constant == "MAX_BITS" else 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def test_outer_wrapper_size_expanded_nodes_and_leaf_depth_precede_serialization(
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
                raise RuntimeError("outer wrapper reached serialization before resource rejection")

            with monkeypatch.context() as patched:
                patched.setattr(module, constant, limit)
                patched.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def test_runner_exact_scalar_empty_and_cached_subtree_depth_boundaries(aggregate):
    runner, _ = aggregate
    for value in (nested(0, 128), nested([], 128)):
        runner.require_wire(value)
    for value in (nested(0, 129), nested([], 129)):
        with pytest.raises(ValueError):
            runner.require_wire(value)
    shared = [0]
    runner.require_wire([shared, nested(shared, 126)])
    with pytest.raises(ValueError):
        runner.require_wire([shared, nested(shared, 127)])


def test_runner_full_baseline_mixed_outputs_producer_controls_and_all_counts(
    aggregate, pinned_y, expected
):
    runner, suite = aggregate
    assert set(suite) == {
        "producer",
        "cases",
        "independent_route_equal",
        "public_controls",
        "totals",
    }
    assert wire(suite) == runner.canonical(suite)
    assert wire(runner.fixtures()) == wire(pinned_y)
    assert suite["producer"] == {
        "artifact": "qr-05y-explicit-fallback-2026-09-07/results.json",
        "bytes": 16474309,
        "sha256": Y_SHA,
    }
    assert suite["independent_route_equal"] is True
    for original, case, wanted in zip(pinned_y["cases"], suite["cases"], expected, strict=True):
        assert case["case_id"] == original["case_id"]
        assert case["problem"] == case_problem(original) == runner.case_problem(original)
        assert wire(case["analysis"]) == wire(wanted)
        assert case["producer_controls"] == {
            "complete_Y_baseline_and_X_nulls_preserved": True,
            "fixed_weights_not_selected_using_actual_level": True,
            "W_full_replacement_quadratic_penalty": True,
            "W_correct_specification_quadratic_regret": True,
            "W_assumed_full_replacement_all_blends_equal_coarse": True,
            "W_fallback_forecasts_unchanged": True,
            "origin_authenticated_by_generic_API": False,
            "raw_history_reconstruction_performed_by_this_runner": False,
        }
    assert suite["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 16,
        "raw_orders_or_artifacts_given_to_core": False,
        "weights_optimized": False,
        "actual_level_used_to_select_weight": False,
        "all_three_forecasts_scored": True,
    }
    assert suite["totals"]["cases"] == 6 and suite["totals"]["analyze_calls"] == 12
    assert suite["totals"]["invalid_analyze_calls_rejected"] == 16
    for key, value in expected[0]["counts"].items():
        wanted = (
            [sum(a["counts"][key][i] for a in expected) for i in range(len(value))]
            if type(value) is list
            else sum(a["counts"][key] for a in expected)
        )
        assert suite["totals"][key] == wanted


def output_mutations(a):
    return [
        (("input_sha256",), "0" * 64),
        (("baseline", "input_sha256"), "0" * 64),
        (("baseline", "beliefs", 0, "pairs", 0, "cells", 0, "forecast", 0, "value", 0), -1),
        (("baseline", "beliefs", 0, "pairs", 0, "x_scores", "forecast_risk"), None),
        (("beliefs", 0, "pairs", 0, "cells", 0, "blends", 1, "forecast", 0, "value", 0), -1),
        (("beliefs", 0, "pairs", 0, "cells", 0, "blends", 1, "forecast_risk"), [2, 1]),
        (("beliefs", 0, "pairs", 0, "blends", 0, "gain_over_coarse"), [-2, 1]),
        (("beliefs", 0, "pairs", 0, "checks", "endpoint_recovery"), False),
        (("counts", "total_work_terms"), 0),
        (("witnesses", "first_worse_than_coarse", 0), 0),
    ]


def test_runner_rejects_nonvacuous_baseline_law_midpoint_gain_work_and_witness_corruption(
    aggregate, pinned_y, expected
):
    runner, _ = aggregate
    original, a = pinned_y["cases"][0], expected[0]
    before = wire(a)
    assert runner.check_analysis(a, original)["complete_native_output_equal"] is True
    for path, value in output_mutations(a):
        bad = replaced(a, path, value)
        assert wire(bad) != before, path
        with pytest.raises(ValueError):
            runner.check_analysis(bad, original)
    assert wire(a) == before


def test_runner_authenticates_entire_Y_producer_before_recomputing_wrapper(
    aggregate, pinned_y, expected
):
    runner, _ = aggregate
    original, a = pinned_y["cases"][0], expected[0]
    for bad in (
        replaced(original, ("problem", "beliefs", 0, "belief_id"), False),
        replaced(
            original,
            ("problem", "beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"),
            [0, 1],
        ),
        replaced(original, ("analysis", "counts", "coarse_scoring_terms"), 0),
    ):
        assert wire(bad) != wire(original)
        with pytest.raises(ValueError):
            runner.check_analysis(a, bad)


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_wrapper_graph_planned_work_and_ownership_guards_in_bounded_subprocess(
    tmp_path, optimized
):
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("_qr05z_guard_helpers", path)
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
def dag():
    value = []
    for _ in range(40):
        value = [value, value]
    return value
def graph_inputs(valid):
    cycle_list = []
    cycle_list.append(cycle_list)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    deep = []
    for _ in range(1500):
        deep = [deep]
    for value in (cycle_list, cycle_dict, deep, dag()):
        bad = copy.deepcopy(valid)
        bad["extra"] = value
        yield bad
    yield {**valid, "experiment": dag()}
    for value in (cycle_list, cycle_dict, deep, dag()):
        bad = copy.deepcopy(valid)
        bad["experiment"]["extra"] = value
        yield bad
    for path in (
        ("beliefs",), ("beliefs", 0, "channels"), ("beliefs", 0, "weight"),
        ("beliefs", 0, "channels", 0, "cells"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction"),
        ("beliefs", 0, "channels", 0, "cells", 0, "value"),
        ("beliefs", 0, "channels", 0, "cells", 0, "probability"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "probability"),
        ("beliefs", 0, "fallbacks"), ("beliefs", 0, "fallbacks", 0, "value"),
        ("beliefs", 0, "fallbacks", 0, "prediction"),
        ("beliefs", 0, "fallbacks", 0, "prediction", 0, "value"),
        ("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"),
    ):
        yield helpers.replaced(valid, ("experiment",) + path, dag())
def reject_before_dump(call, value):
    global before_serialization
    original = json.dumps
    def forbidden(*args, **kwargs):
        raise RuntimeError("unsafe outer tree reached serialization")
    json.dumps = forbidden
    try:
        reject(call, value)
        before_serialization += 1
    finally:
        json.dumps = original
invalid = helpers.invalid_problems()
for index, (filename, helper) in enumerate((
    ("attenuation.py", "_score"), ("reference_qr05z.py", "_score_supported")
)):
    module = helpers.private_module("_qr05z_explicit_guard_" + str(index), filename)
    valid = helpers.wrap(helpers.micro_problem())
    reference = module.analyze(valid)
    midpoint = module.analyze(helpers.midpoint_problem())["beliefs"][0]["pairs"][1]
    require([b["forecast_risk"] for b in midpoint["blends"]] == [[1,1],[1,2],[1,1]], "midpoint control")
    adverse = module.analyze(helpers.wrap(helpers.adverse_fallback_problem()))
    require(adverse["baseline"]["beliefs"][0]["pairs"][1]["x_scores"]["forecast_risk"] is None,
            "original X null was overwritten")
    require(all(b["regret"] == [2,1] for b in adverse["beliefs"][0]["pairs"][1]["blends"]),
            "blend falsely repaired wrong fallback")
    for bad in invalid:
        reject(module.analyze, bad)
    graphs = list(graph_inputs(valid))
    require(len(graphs) == 23, "wrapper/inner graph inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)
    plan = helpers.planned_work(valid)
    for constant, key in (
        ("MAX_PAIR_CELLS","pair_cells"), ("MAX_SCORING_TERMS","baseline_scoring_terms"),
        ("MAX_BLEND_CELLS","blend_cells"), ("MAX_BLEND_ATOMS","blend_atoms"),
        ("MAX_TOTAL_WORK_TERMS","total_work_terms")
    ):
        old_cap, old_score = getattr(module, constant), getattr(module, helper)
        def forbidden(*args, **kwargs):
            raise RuntimeError("Y or Z scoring began before full work cap preflight")
        setattr(module, constant, plan[key] - 1)
        setattr(module, helper, forbidden)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old_cap)
            setattr(module, helper, old_score)
    for constant in ("MAX_INPUT_CELLS", "MAX_INPUT_PREDICTION_ATOMS", "MAX_NODES", "MAX_DEPTH", "MAX_BYTES"):
        old = getattr(module, constant)
        setattr(module, constant, 1)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old)
    for constant in ("MAX_FALLBACKS_PER_BELIEF", "MAX_INPUT_FALLBACKS", "MAX_INPUT_FALLBACK_ATOMS"):
        old = getattr(module, constant)
        setattr(module, constant, 0)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old)
    arithmetic = helpers.singleton_problem()
    require(module.analyze(arithmetic)["beliefs"][0]["pairs"][0]["blends"][0]["forecast_risk"] == [20,121],
            "retained arithmetic control")
    old = module.MAX_BITS
    module.MAX_BITS = 6
    try:
        reject(module.analyze, arithmetic)
    finally:
        module.MAX_BITS = old
    shared = helpers.shared_problem()
    require(module.analyze(shared) == helpers.independently_score(shared), "shared input rejected")
    reference["baseline"]["beliefs"][0]["pairs"][0]["cells"][0]["actual_probability"][0] = -1
    require(module.analyze(valid)["baseline"]["beliefs"][0]["pairs"][0]["cells"][0]["actual_probability"] == [1,2],
            "caller mutation escaped into later baseline")
runner = helpers.private_module("_qr05z_explicit_guard_runner", "study.py")
for bad in graph_inputs(helpers.wrap(helpers.micro_problem())):
    reject_before_dump(runner.require_wire, bad)
reject(lambda value: runner.require_same_wire({"x": 0}, value, "typed regression"), {"x": False})
require(before_serialization == 69, "pre-serialization inventory")
expected = 2 * (len(invalid) + 23 + 14) + 24
require(rejections == expected, "explicit rejection inventory")
print(json.dumps({"rejections": rejections, "pre_serialization_rejections": before_serialization,
                  "invalid_fixture_cases": len(invalid), "optimized": bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05z.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 23 + 14) + 24,
        "pre_serialization_rejections": 69,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }
