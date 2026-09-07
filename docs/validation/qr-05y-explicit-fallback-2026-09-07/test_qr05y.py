"""Independent Y explicit-fallback scoring and boundary controls.

Pinned X JSON and W N cells supply conditional experiments and fallback laws. No current or
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
X_SHA = "1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4"
W_SHA = "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a"


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
CHECKS = (
    "policy_total",
    "mass_partition",
    "split_decomposition",
    "completed_decomposition",
    "coarse_decomposition",
    "gain_identity",
    "supported_forecasts_preserved",
    "zero_regret_iff_equal",
)


def independently_score(problem):
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
                        "checks": dict.fromkeys(CHECKS, True),
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
                "checks": dict.fromkeys(CHECKS, True),
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


def pinned_json(directory, size, sha):
    path = HERE.parent / directory / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == size and hashlib.sha256(raw).hexdigest() == sha
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


@pytest.fixture(scope="session")
def pinned_x():
    return pinned_json("qr-05x-noise-misspecification-2026-09-07", 8842933, X_SHA)


@pytest.fixture(scope="session")
def pinned_w():
    return pinned_json("qr-05w-noisy-readouts-2026-09-07", 6756094, W_SHA)


def case_problem(case, w_case):
    assert case["case_id"] == w_case["case_id"]
    w_rows = {row["belief_id"]: row for row in w_case["analysis"]["beliefs"]}
    rows = []
    for row in case["problem"]["beliefs"]:
        old = w_rows[row["belief_id"]]
        assert row["weight"] == old["weight"]
        rows.append(
            {
                **copy.deepcopy(row),
                "fallbacks": [
                    {
                        "value": copy.deepcopy(c["value"]),
                        "prediction": copy.deepcopy(c["prediction"]),
                    }
                    for c in old["controls"]["N"]["cells"]
                ],
            }
        )
    return {
        "schema_version": "det8-qr05y-problem-v1",
        "family": "qr05y_explicit_fallback",
        "beliefs": rows,
    }


@pytest.fixture(scope="session")
def problems(pinned_x, pinned_w):
    by_id = {case["case_id"]: case for case in pinned_w["cases"]}
    return [case_problem(case, by_id[case["case_id"]]) for case in pinned_x["cases"]]


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05y_test_direct", "fallback.py"),
        private_module("_qr05y_test_reference", "reference_qr05y.py"),
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
    runner = private_module("_qr05y_test_runner", "study.py")
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


@pytest.fixture(scope="session")
def micro_analyses(executors):
    inputs = {
        kind: micro_problem(kind)
        for kind in (
            "balanced",
            "biased",
            "opposed",
            "partial",
            "disjoint",
            "same_law",
            "equal_scalar",
        )
    }
    inputs.update(
        {
            "multi_prefix": multi_prefix_problem(),
            "adverse_fallback": adverse_fallback_problem(),
            "zero_assumed": tiny_problem(F(0)),
            "tiny_assumed": tiny_problem(F(1, 1 << 256)),
        }
    )
    result = {}
    for kind, p in inputs.items():
        a, b = (module.analyze(p) for module in executors)
        assert wire(a) == wire(b) == wire(independently_score(p))
        result[kind] = a
    return result


@pytest.mark.parametrize("case_index", range(6))
def test_all_16_pair_wires_equal_independent_literal_outcome_coordinate_scoring(
    analyses, expected, case_index
):
    a, b = analyses[case_index]
    assert wire(a) == wire(b) == wire(expected[case_index])
    assert wire(json.loads(wire(a))) == wire(a)
    assert len(wire(a)) <= 128 * 1024 * 1024


def test_projection_authenticates_X_channels_and_W_N_fallbacks(pinned_x, pinned_w, problems):
    assert sum(len(case["problem"]["beliefs"]) for case in pinned_x["cases"]) == 482
    by_id = {case["case_id"]: case for case in pinned_w["cases"]}
    for xcase, p in zip(pinned_x["cases"], problems, strict=True):
        w_rows = by_id[xcase["case_id"]]["analysis"]["beliefs"]
        for entry, xold, wold in zip(
            p["beliefs"], xcase["problem"]["beliefs"], w_rows, strict=True
        ):
            assert entry["belief_id"] == xold["belief_id"] == wold["belief_id"]
            assert entry["weight"] == xold["weight"] == wold["weight"]
            assert entry["channels"] == xold["channels"]
            assert entry["fallbacks"] == [
                {key: c[key] for key in ("value", "prediction")}
                for c in wold["controls"]["N"]["cells"]
            ]
            union = {
                tuple(c["value"][:5]) for channel in entry["channels"] for c in channel["cells"]
            }
            assert {tuple(f["value"]) for f in entry["fallbacks"]} == union


def test_fixed_family_controls_preserve_X_nulls_and_verify_full_fallback_laws(
    pinned_x, pinned_w, expected
):
    by_id = {case["case_id"]: case for case in pinned_w["cases"]}
    for xcase, a in zip(pinned_x["cases"], expected, strict=True):
        wcase = by_id[xcase["case_id"]]
        for row, xold, wold in zip(
            a["beliefs"], xcase["analysis"]["beliefs"], wcase["analysis"]["beliefs"], strict=True
        ):
            n_cells = {tuple(c["value"]): c for c in wold["controls"]["N"]["cells"]}
            for index, pair in enumerate(row["pairs"]):
                original = xold["pairs"][index]
                assert pair["x_scores"] == {key: original[key] for key in X_FIELDS}
                assert pair["fallback_regret"] == [0, 1]
                assert pair["completed_regret"] == original["supported_regret"]
                assert pair["completed_forecast_risk"] == fw(
                    fraction(original["supported_forecast_risk"])
                    + fraction(original["bayes_risk"])
                    - fraction(original["supported_bayes_risk"])
                )
                assert pair["coarse_forecast_risk"] == wold["controls"]["N"]["expected_risk"]
                assert len(pair["cells"]) == len(original["cells"])
                w_channel = {tuple(c["value"]): c for c in wold["channels"][index // 4]["cells"]}
                for c, old_cell in zip(pair["cells"], original["cells"], strict=True):
                    assert c["actual_probability"] == old_cell["actual_probability"]
                    assert c["actual_prediction"] == old_cell["actual_prediction"]
                    if c["supported"]:
                        assert c["assumed_forecast"] == c["forecast"] == old_cell["forecast"]
                        assert c["forecast_risk"] == old_cell["forecast_risk"]
                        assert c["regret"] == old_cell["regret"]
                    else:
                        n = n_cells[tuple(c["value"][:5])]
                        received = w_channel[tuple(c["value"])]
                        assert received["posterior"] == n["posterior"]
                        assert received["prediction"] == n["prediction"] == c["coarse_forecast"]
                        assert c["forecast"] == c["actual_prediction"] and c["regret"] == [0, 1]
                        assert c["used_fallback"] is True and c["gain_over_coarse"] == [0, 1]
                if original["complete"]:
                    assert pair["completed_forecast_risk"] == original["forecast_risk"]
                    assert pair["completed_regret"] == original["regret"]
                if index // 4 == index % 4:
                    assert pair["completed_regret"] == [0, 1]
        for pair, original in zip(
            a["aggregate"]["pairs"], xcase["analysis"]["aggregate"]["pairs"], strict=True
        ):
            assert pair["x_scores"] == {key: original[key] for key in X_FIELDS}
            assert pair["coarse_forecast_risk"] == wcase["analysis"]["aggregate"]["N_risk"]


def test_split_decomposition_coverage_bound_aggregate_weights_and_first_witnesses(expected):
    predicates = {
        "first_fallback": lambda p: fraction(p["x_scores"]["unsupported_mass"]) > 0,
        "first_positive_fallback_regret": lambda p: fraction(p["fallback_regret"]) > 0,
        "first_positive_completed_regret": lambda p: fraction(p["completed_regret"]) > 0,
        "first_better_than_coarse": lambda p: fraction(p["gain_over_coarse"]) > 0,
        "first_equal_to_coarse": lambda p: fraction(p["gain_over_coarse"]) == 0,
        "first_worse_than_coarse": lambda p: fraction(p["gain_over_coarse"]) < 0,
    }
    for a in expected:
        for index, aggregate_pair in enumerate(a["aggregate"]["pairs"]):
            for key in SCORE_FIELDS:
                assert aggregate_pair[key] == fw(
                    sum(
                        fraction(row["weight"]) * fraction(row["pairs"][index][key])
                        for row in a["beliefs"]
                    )
                )
            assert aggregate_pair["x_scores"]["complete"] == all(
                row["pairs"][index]["x_scores"]["complete"] for row in a["beliefs"]
            )
            for key, predicate in predicates.items():
                ids = [row["belief_id"] for row in a["beliefs"] if predicate(row["pairs"][index])]
                assert a["witnesses"][key][index] == (ids[0] if ids else None)
            assert a["counts"]["pair_cells"][index] == (
                a["counts"]["supported_pair_cells"][index]
                + a["counts"]["fallback_pair_cells"][index]
            )
            assert sum(
                a["counts"][key][index]
                for key in (
                    "better_than_coarse_beliefs",
                    "equal_to_coarse_beliefs",
                    "worse_than_coarse_beliefs",
                )
            ) == len(a["beliefs"])
            for row in a["beliefs"]:
                pair = row["pairs"][index]
                x = pair["x_scores"]
                assert abs(fraction(pair["gain_over_coarse"])) <= 2 * fraction(x["coverage"])
                assert pair["fallback_forecast_risk"] == fw(
                    fraction(pair["fallback_bayes_risk"]) + fraction(pair["fallback_regret"])
                )
                assert pair["completed_forecast_risk"] == fw(
                    fraction(x["supported_forecast_risk"])
                    + fraction(pair["fallback_forecast_risk"])
                )
                assert fraction(pair["gain_over_coarse"]) == (
                    fraction(pair["coarse_regret"]) - fraction(pair["completed_regret"])
                )
                assert pair["checks"] == dict.fromkeys(CHECKS, True)


def test_no_fallback_preserves_supported_forecasts_even_when_they_are_harmful(micro_analyses):
    pair = micro_analyses["opposed"]["beliefs"][0]["pairs"][1]
    assert pair["x_scores"]["complete"] is True and pair["x_scores"]["unsupported_mass"] == [0, 1]
    assert pair["fallback_forecast_risk"] == pair["fallback_regret"] == [0, 1]
    assert pair["completed_forecast_risk"] == pair["x_scores"]["forecast_risk"] == [2, 1]
    assert pair["coarse_forecast_risk"] == [1, 2] and pair["gain_over_coarse"] == [-3, 2]
    assert all(
        c["forecast"] == c["assumed_forecast"] and not c["used_fallback"] for c in pair["cells"]
    )
    assert micro_analyses["opposed"]["witnesses"]["first_worse_than_coarse"][1] == 0


def test_partial_fallback_retains_original_X_nulls_and_unrenormalized_contributions(micro_analyses):
    pair = micro_analyses["partial"]["beliefs"][0]["pairs"][1]
    assert pair["x_scores"]["coverage"] == [1, 4]
    assert pair["x_scores"]["forecast_risk"] is pair["x_scores"]["regret"] is None
    assert pair["x_scores"]["supported_forecast_risk"] == [1, 2]
    assert pair["fallback_forecast_risk"] == pair["fallback_regret"] == [3, 8]
    assert pair["completed_forecast_risk"] == pair["completed_regret"] == [7, 8]
    assert pair["coarse_forecast_risk"] == [1, 2] and pair["gain_over_coarse"] == [-3, 8]
    supported, missing = pair["cells"]
    assert supported["forecast"] == supported["assumed_forecast"] and supported[
        "forecast_risk"
    ] == [2, 1]
    assert missing["actual_probability"] == [3, 4] and missing["forecast_risk"] == [1, 2]
    assert missing["gain_over_coarse"] == [0, 1] and missing["used_fallback"] is True
    assert fraction(pair["fallback_forecast_risk"]) != (
        fraction(pair["fallback_forecast_risk"]) / fraction(pair["x_scores"]["unsupported_mass"])
    )


def test_generic_fallback_can_be_wrong_and_add_future_symbols_absent_everywhere_else(
    micro_analyses,
):
    a = micro_analyses["adverse_fallback"]
    pair = a["beliefs"][0]["pairs"][1]
    assert pair["x_scores"]["coverage"] == [0, 1]
    assert pair["x_scores"]["forecast_risk"] is pair["x_scores"]["regret"] is None
    assert pair["fallback_forecast_risk"] == pair["fallback_regret"] == [2, 1]
    assert pair["completed_forecast_risk"] == pair["coarse_forecast_risk"] == [2, 1]
    assert pair["gain_over_coarse"] == [0, 1]
    c = pair["cells"][0]
    assert c["actual_prediction"] == law({0: F(1)})
    assert c["coarse_forecast"] == c["forecast"] == law({2: F(1)})
    assert c["assumed_forecast"] is None and c["predictions_equal"] is False
    assert a["witnesses"]["first_positive_fallback_regret"][1] == 0


def test_exact_zero_not_a_numerical_threshold_selects_fallback(micro_analyses):
    zero = micro_analyses["zero_assumed"]["beliefs"][0]["pairs"][1]
    tiny = micro_analyses["tiny_assumed"]["beliefs"][0]["pairs"][1]
    assert zero["x_scores"]["coverage"] == [0, 1] and zero["completed_forecast_risk"] == [2, 1]
    assert tiny["x_scores"]["coverage"] == [1, 1] and tiny["completed_forecast_risk"] == [0, 1]
    c = tiny["cells"][0]
    assert c["assumed_probability"] == [1, 1 << 256]
    assert c["supported"] is True and c["used_fallback"] is False
    assert c["forecast"] == c["assumed_forecast"] != c["coarse_forecast"]


def test_multi_prefix_comparator_may_vary_with_actual_law_and_gain_attains_both_extremes(
    micro_analyses,
):
    a = micro_analyses["multi_prefix"]
    row = a["beliefs"][0]
    assert row["pairs"][0]["coarse_forecast_risk"] == [0, 1]
    assert row["pairs"][4]["coarse_forecast_risk"] == [2, 1]
    assert row["pairs"][1]["completed_forecast_risk"] == [2, 1]
    assert row["pairs"][1]["gain_over_coarse"] == [-2, 1]
    assert row["pairs"][5]["completed_forecast_risk"] == [0, 1]
    assert row["pairs"][5]["gain_over_coarse"] == [2, 1]
    assert a["witnesses"]["first_worse_than_coarse"][1] == 0
    assert a["witnesses"]["first_better_than_coarse"][5] == 0
    assert all(c["supported"] and not c["used_fallback"] for p in row["pairs"] for c in p["cells"])


def test_policy_is_independent_of_actual_level_and_has_no_hidden_branch_inputs(micro_analyses):
    for a in micro_analyses.values():
        for row in a["beliefs"]:
            for j in range(4):
                policies = {}
                for i in range(4):
                    for c in row["pairs"][4 * i + j]["cells"]:
                        value = tuple(c["value"])
                        decision = (c["forecast"], c["coarse_forecast"], c["used_fallback"])
                        if value in policies:
                            assert policies[value] == decision
                        policies[value] = decision


def test_equal_scalar_risk_is_not_zero_regret_and_different_report_laws_can_be_harmless(
    micro_analyses,
):
    pair = micro_analyses["equal_scalar"]["beliefs"][0]["pairs"][1]
    assert pair["x_scores"]["bayes_risk"] == [3, 8]
    assert pair["completed_forecast_risk"] == [7, 8] and pair["completed_regret"] == [1, 2]
    assert all(not c["predictions_equal"] for c in pair["cells"])
    for pair in micro_analyses["same_law"]["beliefs"][0]["pairs"]:
        assert (
            pair["completed_regret"] == pair["coarse_regret"] == pair["gain_over_coarse"] == [0, 1]
        )
        assert pair["completed_forecast_risk"] == [1, 2]


def test_original_history_and_report_weights_are_preserved_through_completion(executors):
    p = micro_problem("balanced")
    p["beliefs"][0]["weight"] = [1, 4]
    other = micro_problem("partial")["beliefs"][0]
    p["beliefs"].append({**other, "belief_id": 1, "weight": [3, 4]})
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        pair = a["aggregate"]["pairs"][1]
        assert pair["x_scores"]["coverage"] == [7, 16]
        assert pair["x_scores"]["forecast_risk"] is pair["x_scores"]["regret"] is None
        assert pair["completed_forecast_risk"] == [11, 16]
        assert pair["fallback_forecast_risk"] == [9, 32]
        assert pair["coarse_forecast_risk"] == [1, 2]
        assert pair["gain_over_coarse"] == [-3, 16]
        assert pair["complete_before_beliefs"] == pair["incomplete_before_beliefs"] == 1
        uniform = sum(fraction(r["pairs"][1]["completed_forecast_risk"]) for r in a["beliefs"]) / 2
        assert uniform == F(1, 2) != F(11, 16)


def test_fallback_keys_cover_full_report_union_including_currently_unused_prefixes(executors):
    channels = []
    for i in range(4):
        c = cell(0, F(1), {0: F(1)})
        c["value"][0] = i
        channels.append([c])
    p = problem_of(channels)
    assert len(p["beliefs"][0]["fallbacks"]) == 4
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert len(a["beliefs"][0]["pairs"][0]["cells"]) == 1
        bad = replaced(p, ("beliefs", 0, "fallbacks"), p["beliefs"][0]["fallbacks"][:1])
        with pytest.raises(ValueError):
            module.analyze(bad)


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
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


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_public_exact_native_contract_rejects_without_repair(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def singleton_problem(denominator=11):
    prediction = {0: F(1, denominator), 1: F(denominator - 1, denominator)}
    return problem_of([[cell(0, F(1), prediction)] for _ in range(4)])


def test_probability_components_may_exceed_64_bits_when_within_4096(executors):
    denominator = (1 << 80) + 1
    p = singleton_problem(denominator)
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert a["beliefs"][0]["pairs"][0]["x_scores"]["bayes_risk"] == fw(
            F(2 * (denominator - 1), denominator**2)
        )


def test_large_intermediate_denominators_are_not_retained_bit_overflows(executors):
    denominator = 1 << 4095
    prediction = {0: F(1, 2), 1: F(1, 2)}
    cells = [
        cell(0, F(1, denominator), prediction),
        cell(1, F(denominator - 1, denominator), prediction),
    ]
    p = problem_of([cells] * 4)
    assert denominator.bit_length() == 4096
    assert (2 * denominator).bit_length() == 4097
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert all(
            pair["x_scores"]["bayes_risk"] == pair["completed_forecast_risk"] == [1, 2]
            and pair["completed_regret"] == [0, 1]
            for pair in a["beliefs"][0]["pairs"]
        )


def test_genuinely_retained_risk_denominator_overflow_is_rejected(executors):
    denominator = (1 << 2048) + 1
    retained_risk = F(2 * (denominator - 1), denominator**2)
    assert denominator.bit_length() <= 4096 < retained_risk.denominator.bit_length()
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(singleton_problem(denominator))


def mutable_ids(value):
    seen, stack = set(), [value]
    while stack:
        item = stack.pop()
        if type(item) not in (dict, list) or id(item) in seen:
            continue
        seen.add(id(item))
        stack.extend(item.values() if type(item) is dict else item)
    return seen


def test_entire_output_is_detached_from_inputs_and_other_calls(executors):
    for module in executors:
        p = micro_problem("partial")
        a, b = module.analyze(p), module.analyze(p)
        before, wanted = wire(p), wire(b)
        assert mutable_ids(a).isdisjoint(mutable_ids(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(b))
        a["beliefs"][0]["pairs"][1]["cells"][0]["forecast"][0]["value"][0] = 99
        a["aggregate"]["pairs"][1]["x_scores"]["coverage"][0] = -1
        a["levels"][0][0] = 99
        assert wire(p) == before and wire(b) == wanted and wire(module.analyze(p)) == wanted
        p["beliefs"][0]["channels"][0]["cells"][0]["probability"][0] = -1
        assert wire(b) == wanted
        with pytest.raises(ValueError):
            module.analyze(p)


def shared_problem():
    p = micro_problem("same_law")
    shared = p["beliefs"][0]["channels"][0]["cells"][0]["prediction"]
    for channel in p["beliefs"][0]["channels"]:
        for c in channel["cells"]:
            c["prediction"] = shared
    p["beliefs"][0]["fallbacks"][0]["prediction"] = shared
    return p


def test_benign_shared_containers_are_accepted_without_mutable_cache_aliases(executors):
    p = shared_problem()
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert mutable_ids(a).isdisjoint(mutable_ids(p))
        bad = replaced(p, ("beliefs", 0, "belief_id"), IntChild(0))
        with pytest.raises(ValueError):
            module.analyze(bad)
        assert wire(module.analyze(p)) == wire(a)


def planned_work(p):
    pair_cells = completed = coarse = 0
    for b in p["beliefs"]:
        fallback = {tuple(row["value"]): row["prediction"] for row in b["fallbacks"]}
        for actual in b["channels"]:
            for assumed in b["channels"]:
                forecasts = {tuple(c["value"]): c for c in assumed["cells"]}
                pair_cells += len(actual["cells"])
                for c in actual["cells"]:
                    g = fallback[tuple(c["value"][:5])]
                    f = (
                        forecasts[tuple(c["value"])]["prediction"]
                        if tuple(c["value"]) in forecasts
                        else g
                    )
                    completed += len(c["prediction"]) + len(f)
                    coarse += len(c["prediction"]) + len(g)
    return pair_cells, completed, coarse


def test_pair_and_scoring_work_caps_reject_before_any_supported_score_loop(executors, monkeypatch):
    p = micro_problem()
    cells, completed, coarse = planned_work(p)
    work = (cells, completed + coarse)
    for module, helper in zip(executors, ("_score", "_score_supported"), strict=True):
        expected = wire(module.analyze(p))
        for constant, count in zip(("MAX_PAIR_CELLS", "MAX_SCORING_TERMS"), work, strict=True):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("score loop reached before rejecting planned work overflow")

            with monkeypatch.context() as limited:
                limited.setattr(module, constant, count - 1)
                limited.setattr(module, helper, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
            assert wire(module.analyze(p)) == expected


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
    ],
)
def test_all_live_caps_reject_instead_of_truncating(executors, monkeypatch, constant):
    p = micro_problem()
    if constant == "MAX_BELIEFS":
        p["beliefs"][0]["weight"] = [1, 2]
        p["beliefs"].append({**copy.deepcopy(p["beliefs"][0]), "belief_id": 1})
    if constant in ("MAX_FALLBACKS_PER_BELIEF", "MAX_INPUT_FALLBACKS"):
        p = multi_prefix_problem()
    if constant == "MAX_BITS":
        p = singleton_problem()
    for module in executors:
        expected = wire(module.analyze(p))
        with monkeypatch.context() as limited:
            limited.setattr(module, constant, 6 if constant == "MAX_BITS" else 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == expected


def tree_resources(value, depth=0):
    nodes, maximum_depth = 1, depth
    if type(value) in (dict, list):
        items = value.values() if type(value) is dict else value
        for child in items:
            child_nodes, child_depth = tree_resources(child, depth + 1)
            nodes += child_nodes
            maximum_depth = max(maximum_depth, child_depth)
    return nodes, maximum_depth


def test_expanded_shared_node_size_and_scalar_leaf_depth_caps_precede_serialization(
    executors, monkeypatch
):
    p = shared_problem()
    nodes, depth = tree_resources(p)
    assert nodes > len(mutable_ids(p))
    for module in executors:
        expected = wire(module.analyze(p))
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("unvalidated oversized native tree reached serialization")

            with monkeypatch.context() as limited:
                limited.setattr(module, constant, limit)
                limited.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        assert wire(module.analyze(p)) == expected


def test_maximum_belief_count_is_inclusive_and_extra_belief_fails(executors):
    p = problem_of([[cell(0, F(1), {0: F(1)})]] * 4)
    template = p["beliefs"][0]["channels"]
    fallbacks = p["beliefs"][0]["fallbacks"]
    p["beliefs"] = [
        {"belief_id": i, "weight": [1, 512], "channels": template, "fallbacks": fallbacks}
        for i in range(512)
    ]
    for module in executors:
        a = module.analyze(p)
        assert a["counts"]["beliefs"] == 512
        assert a["aggregate"]["pairs"][0]["completed_forecast_risk"] == [0, 1]
        bad = {
            **p,
            "beliefs": [
                {"belief_id": i, "weight": [1, 513], "channels": template, "fallbacks": fallbacks}
                for i in range(513)
            ],
        }
        with pytest.raises(ValueError):
            module.analyze(bad)


def test_both_policy_and_coarse_scores_are_evaluated_and_counted_even_on_fallback_cells(
    executors, monkeypatch
):
    p = adverse_fallback_problem()
    planned_cells, completed, coarse = planned_work(p)
    for module, helper in zip(executors, ("_score", "_score_supported"), strict=True):
        original, calls = getattr(module, helper), []

        def observed(*args, original=original, calls=calls, **kwargs):
            calls.append(1)
            return original(*args, **kwargs)

        with monkeypatch.context() as patched:
            patched.setattr(module, helper, observed)
            a = module.analyze(p)
        assert len(calls) == 2 * planned_cells == 2 * sum(a["counts"]["pair_cells"])
        assert a["counts"]["completed_scoring_terms"] == completed
        assert a["counts"]["coarse_scoring_terms"] == coarse
        assert sum(a["counts"]["fallback_pair_cells"]) > 0
        assert wire(a) == wire(independently_score(p))


def test_runner_complete_projection_outputs_controls_and_actual_counts(
    aggregate, pinned_x, problems, expected
):
    runner, suite = aggregate
    assert set(suite) == {
        "producer",
        "cases",
        "independent_route_equal",
        "public_controls",
        "totals",
    }
    assert wire(suite) == runner.canonical(suite) == wire(json.loads(wire(suite)))
    assert wire(runner.fixtures()) == wire(pinned_x)
    assert suite["producer"] == {
        "artifact": "qr-05x-noise-misspecification-2026-09-07/results.json",
        "bytes": 8842933,
        "sha256": X_SHA,
    }
    assert suite["independent_route_equal"] is True
    for producer, p, actual, wanted in zip(
        pinned_x["cases"], problems, suite["cases"], expected, strict=True
    ):
        assert actual["case_id"] == producer["case_id"]
        assert actual["problem"] == p == runner.case_problem(producer)
        assert wire(actual["analysis"]) == wire(wanted)
        assert actual["producer_controls"] == {
            "X_laws_and_W_N_fallbacks_are_declared_dependencies": True,
            "complete_original_X_scores_and_nulls_preserved": True,
            "supported_forecasts_and_scores_preserved": True,
            "W_fallback_future_laws_equal_actual": True,
            "W_fallback_regret_zero": True,
            "W_completion_identity": True,
            "coarse_only_W_N_risk_equal": True,
            "channel_or_fallback_origin_authenticated_by_generic_API": False,
            "raw_history_reconstruction_performed_by_this_runner": False,
        }
    assert suite["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 14,
        "raw_orders_histories_or_artifacts_given_to_core": False,
        "fallback_rule_explicit": True,
        "fallback_optimized": False,
        "actual_level_used_to_select_forecast": False,
    }
    assert suite["totals"]["cases"] == 6 and suite["totals"]["analyze_calls"] == 12
    assert suite["totals"]["invalid_analyze_calls_rejected"] == 14
    for key, value in expected[0]["counts"].items():
        wanted = (
            [sum(a["counts"][key][i] for a in expected) for i in range(16)]
            if type(value) is list
            else sum(a["counts"][key] for a in expected)
        )
        assert suite["totals"][key] == wanted


def output_mutations(a):
    return [
        (("input_sha256",), "0" * 64),
        (("levels", 0), [1, 1]),
        (("beliefs", 0, "belief_id"), False),
        (("beliefs", 0, "weight"), [0, 1]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "actual_probability"), [0, 1]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "assumed_forecast"), None),
        (("beliefs", 0, "pairs", 0, "cells", 0, "coarse_forecast", 0, "value", 0), -1),
        (("beliefs", 0, "pairs", 0, "cells", 0, "forecast"), None),
        (("beliefs", 0, "pairs", 0, "cells", 0, "used_fallback"), True),
        (("beliefs", 0, "pairs", 0, "cells", 0, "predictions_equal"), False),
        (("beliefs", 0, "pairs", 0, "x_scores", "coverage"), [0, 1]),
        (("beliefs", 0, "pairs", 0, "x_scores", "forecast_risk"), None),
        (("beliefs", 0, "pairs", 0, "fallback_regret"), [2, 1]),
        (("beliefs", 0, "pairs", 0, "completed_regret"), [2, 1]),
        (("beliefs", 0, "pairs", 0, "gain_over_coarse"), [-2, 1]),
        (("beliefs", 0, "pairs", 0, "checks", "supported_forecasts_preserved"), False),
        (("aggregate", "pairs", 0, "complete_before_beliefs"), 0),
        (("aggregate", "pairs", 0, "completed_forecast_risk"), None),
        (("witnesses", "first_fallback", 0), 0),
        (("witnesses", "first_positive_completed_regret", 0), 0),
        (("counts", "completed_scoring_terms"), 0),
        (("counts", "coarse_scoring_terms"), 0),
    ]


def test_runner_rejects_complete_forecast_policy_null_gain_and_count_corruption(
    aggregate, pinned_x, expected
):
    runner, _ = aggregate
    case, a = pinned_x["cases"][0], expected[0]
    before = wire(a)
    assert runner.check_analysis(a, case)["complete_native_output_equal"] is True
    for path, value in output_mutations(a):
        bad = replaced(a, path, value)
        assert wire(bad) != before, path
        with pytest.raises(ValueError):
            runner.check_analysis(bad, case)
    assert wire(a) == before


def test_runner_authenticates_pinned_X_problem_and_scores_before_accepting_policy(
    aggregate, pinned_x, expected
):
    runner, _ = aggregate
    case, a = pinned_x["cases"][0], expected[0]
    report = runner.check_analysis(a, case)
    assert report["analysis_sha256"] == digest(a)
    for bad in (
        replaced(case, ("problem", "beliefs", 0, "belief_id"), False),
        replaced(case, ("problem", "beliefs", 0, "channels", 0, "cells", 0, "probability"), [0, 1]),
        replaced(case, ("analysis", "beliefs", 0, "pairs", 0, "forecast_risk"), None),
        replaced(case, ("analysis", "counts", "scoring_terms"), 0),
    ):
        assert wire(bad) != wire(case)
        with pytest.raises(ValueError):
            runner.check_analysis(a, bad)
    assert runner.check_analysis(a, case) == report


def test_runner_wire_equality_keeps_native_bool_and_integer_distinct(aggregate):
    runner, _ = aggregate
    for value in ({"x": (0,)}, {"x": 0.5}, {1: "x"}, {StrChild("x"): 0}, {"x": IntChild(0)}):
        with pytest.raises(ValueError):
            runner.require_wire(value)
    for left, right in (({"x": [True]}, {"x": [1]}), ({"x": [0]}, {"x": [False]})):
        runner.require_wire(left)
        runner.require_wire(right)
        with pytest.raises(ValueError):
            runner.require_same_wire(left, right, "typed regression")


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_native_DAG_work_caps_and_ownership_guards_in_bounded_subprocess(
    tmp_path, optimized
):
    program = r"""
import copy, importlib.util, json, resource, sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (12, 12))
path = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("_qr05y_guard_helpers", path)
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
    result = []
    for _ in range(40):
        result = [result, result]
    return result
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
    for path in (
        ("beliefs",), ("beliefs", 0, "channels"), ("beliefs", 0, "weight"),
        ("beliefs", 0, "channels", 0, "cells"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction"),
        ("beliefs", 0, "channels", 0, "cells", 0, "value"),
        ("beliefs", 0, "channels", 0, "cells", 0, "probability"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "value"),
        ("beliefs", 0, "channels", 0, "cells", 0, "prediction", 0, "probability"),
        ("beliefs", 0, "fallbacks"),
        ("beliefs", 0, "fallbacks", 0, "value"),
        ("beliefs", 0, "fallbacks", 0, "prediction"),
        ("beliefs", 0, "fallbacks", 0, "prediction", 0, "value"),
        ("beliefs", 0, "fallbacks", 0, "prediction", 0, "probability"),
    ):
        yield helpers.replaced(valid, path, dag())
def reject_before_dump(call, value):
    global before_serialization
    original = json.dumps
    def forbidden(*args, **kwargs):
        raise RuntimeError("unsafe tree reached serialization")
    json.dumps = forbidden
    try:
        reject(call, value)
        before_serialization += 1
    finally:
        json.dumps = original
invalid = helpers.invalid_problems()
for index, (filename, score_helper) in enumerate((
    ("fallback.py", "_score"), ("reference_qr05y.py", "_score_supported")
)):
    module = helpers.private_module("_qr05y_explicit_guard_" + str(index), filename)
    valid = helpers.micro_problem()
    wanted = module.analyze(valid)
    opposed = module.analyze(helpers.micro_problem("opposed"))
    require(opposed["beliefs"][0]["pairs"][1]["completed_forecast_risk"] == [2, 1], "risk two")
    disjoint = module.analyze(helpers.adverse_fallback_problem())
    pair = disjoint["beliefs"][0]["pairs"][1]
    require(pair["x_scores"]["coverage"] == [0, 1] and pair["x_scores"]["forecast_risk"] is None
            and pair["fallback_forecast_risk"] == pair["completed_forecast_risk"] == [2, 1],
            "total fallback must not overwrite X nulls or invent correctness")
    partial = module.analyze(helpers.micro_problem("partial"))["beliefs"][0]["pairs"][1]
    require(partial["x_scores"]["coverage"] == [1, 4] and partial["fallback_forecast_risk"] == [3, 8]
            and partial["completed_forecast_risk"] == [7, 8] and partial["x_scores"]["forecast_risk"] is None,
            "partial fallback is not renormalized or conflated with X scores")
    for bad in invalid:
        reject(module.analyze, bad)
    graphs = list(graph_inputs(valid))
    require(len(graphs) == 18, "graph inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)
    pair_cells, completed, coarse = helpers.planned_work(valid)
    for constant, count in zip(("MAX_PAIR_CELLS", "MAX_SCORING_TERMS"), (pair_cells, completed + coarse)):
        old_cap, old_score = getattr(module, constant), getattr(module, score_helper)
        def forbidden(*args, **kwargs):
            raise RuntimeError("score loop began before work cap validation")
        setattr(module, constant, count - 1)
        setattr(module, score_helper, forbidden)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, old_cap)
            setattr(module, score_helper, old_score)
    for constant in ("MAX_INPUT_CELLS", "MAX_INPUT_PREDICTION_ATOMS", "MAX_NODES",
                     "MAX_DEPTH", "MAX_BYTES"):
        original = getattr(module, constant)
        setattr(module, constant, 1)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, original)
    for constant in ("MAX_FALLBACKS_PER_BELIEF", "MAX_INPUT_FALLBACKS", "MAX_INPUT_FALLBACK_ATOMS"):
        original = getattr(module, constant)
        setattr(module, constant, 0)
        try:
            reject(module.analyze, valid)
        finally:
            setattr(module, constant, original)
    arithmetic = helpers.singleton_problem()
    require(module.analyze(arithmetic)["beliefs"][0]["pairs"][0]["x_scores"]["bayes_risk"] == [20, 121],
            "retained arithmetic control")
    old_bits = module.MAX_BITS
    module.MAX_BITS = 6
    try:
        reject(module.analyze, arithmetic)
    finally:
        module.MAX_BITS = old_bits
    shared = helpers.shared_problem()
    require(module.analyze(shared) == helpers.independently_score(shared), "shared input rejected")
    wanted["beliefs"][0]["pairs"][0]["cells"][0]["actual_probability"][0] = -1
    require(module.analyze(valid)["beliefs"][0]["pairs"][0]["cells"][0]["actual_probability"] == [1, 2],
            "caller mutation escaped into later result")
runner = helpers.private_module("_qr05y_explicit_guard_runner", "study.py")
for bad in graph_inputs(helpers.micro_problem()):
    reject_before_dump(runner.require_wire, bad)
reject(lambda value: runner.require_same_wire({"x": 0}, value, "typed regression"), {"x": False})
require(before_serialization == 54, "pre-serialization rejection inventory")
expected = 2 * (len(invalid) + 18 + 11) + 19
require(rejections == expected, "explicit rejection inventory")
print(json.dumps({"rejections": rejections, "pre_serialization_rejections": before_serialization,
                  "invalid_fixture_cases": len(invalid), "optimized": bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05y.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 18 + 11) + 19,
        "pre_serialization_rejections": 54,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }
