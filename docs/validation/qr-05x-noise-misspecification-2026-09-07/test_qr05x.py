"""Independent X conditional-experiment scoring and boundary controls.

Pinned W JSON supplies complete conditional experiments. No current or
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
    assert type(n) is int and type(d) is int and n >= 0 and d > 0
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


def independently_score(problem):
    rows = []
    scoring_terms = 0
    input_cells = input_atoms = 0
    for entry in problem["beliefs"]:
        channels = entry["channels"]
        input_cells += sum(len(channel["cells"]) for channel in channels)
        input_atoms += sum(
            len(cell["prediction"]) for channel in channels for cell in channel["cells"]
        )
        pairs = []
        for i, actual_channel in enumerate(channels):
            for j, assumed_channel in enumerate(channels):
                forecasts = {tuple(cell["value"]): cell for cell in assumed_channel["cells"]}
                cells = []
                coverage = total_bayes = supported_bayes = supported_risk = supported_regret = F(0)
                equalities = []
                for actual in actual_channel["cells"]:
                    value = tuple(actual["value"])
                    p = read_law(actual["prediction"])
                    mass = fraction(actual["probability"])
                    bayes = bayes_risk(p)
                    total_bayes += mass * bayes
                    forecast = forecasts.get(value)
                    cell = {
                        "value": list(value),
                        "actual_probability": actual["probability"],
                        "assumed_probability": [0, 1]
                        if forecast is None
                        else forecast["probability"],
                        "actual_prediction": actual["prediction"],
                        "forecast": None,
                        "bayes_risk": fw(bayes),
                        "forecast_risk": None,
                        "regret": None,
                        "supported": forecast is not None,
                        "predictions_equal": None,
                    }
                    if forecast is not None:
                        f = read_law(forecast["prediction"])
                        scoring_terms += len(p) + len(f)
                        risk, regret = outcome_risk(p, f), squared_error(p, f)
                        equal = p == f
                        assert risk == bayes + regret
                        assert (regret == 0) == equal
                        assert 0 <= bayes <= 1 and 0 <= risk <= 2 and 0 <= regret <= 2
                        coverage += mass
                        supported_bayes += mass * bayes
                        supported_risk += mass * risk
                        supported_regret += mass * regret
                        equalities.append(equal)
                        cell.update(
                            {
                                "forecast": forecast["prediction"],
                                "forecast_risk": fw(risk),
                                "regret": fw(regret),
                                "predictions_equal": equal,
                            }
                        )
                    cells.append(cell)
                complete = coverage == 1
                assert supported_risk == supported_bayes + supported_regret
                assert (supported_regret == 0) == all(equalities)
                assert 0 <= supported_bayes <= coverage
                assert 0 <= supported_risk <= 2 * coverage and 0 <= supported_regret <= 2 * coverage
                if complete:
                    assert supported_bayes == total_bayes
                pairs.append(
                    {
                        "actual_index": i,
                        "assumed_index": j,
                        "cells": cells,
                        "bayes_risk": fw(total_bayes),
                        "coverage": fw(coverage),
                        "unsupported_mass": fw(1 - coverage),
                        "supported_bayes_risk": fw(supported_bayes),
                        "supported_forecast_risk": fw(supported_risk),
                        "supported_regret": fw(supported_regret),
                        "forecast_risk": fw(supported_risk) if complete else None,
                        "regret": fw(supported_regret) if complete else None,
                        "complete": complete,
                        "checks": {
                            "mass_partition": True,
                            "supported_decomposition": True,
                            "full_decomposition": True if complete else None,
                            "zero_regret_iff_equal": True,
                        },
                    }
                )
        rows.append({"belief_id": entry["belief_id"], "weight": entry["weight"], "pairs": pairs})
    aggregate_pairs = []
    for index in range(16):
        i, j = divmod(index, 4)
        complete_beliefs = sum(row["pairs"][index]["complete"] for row in rows)
        complete = complete_beliefs == len(rows)
        pair = {
            "actual_index": i,
            "assumed_index": j,
            **{
                key: fw(
                    sum(
                        fraction(row["weight"]) * fraction(row["pairs"][index][key]) for row in rows
                    )
                )
                for key in (
                    "bayes_risk",
                    "coverage",
                    "unsupported_mass",
                    "supported_bayes_risk",
                    "supported_forecast_risk",
                    "supported_regret",
                )
            },
            "forecast_risk": None,
            "regret": None,
            "complete": complete,
            "complete_beliefs": complete_beliefs,
            "incomplete_beliefs": len(rows) - complete_beliefs,
            "checks": {
                "mass_partition": True,
                "supported_decomposition": True,
                "full_decomposition": True if complete else None,
                "zero_regret_iff_equal": True,
            },
        }
        assert fraction(pair["coverage"]) + fraction(pair["unsupported_mass"]) == 1
        assert (fraction(pair["coverage"]) == 1) == complete
        assert fraction(pair["supported_forecast_risk"]) == (
            fraction(pair["supported_bayes_risk"]) + fraction(pair["supported_regret"])
        )
        equalities = [
            cell["predictions_equal"]
            for row in rows
            for cell in row["pairs"][index]["cells"]
            if cell["supported"]
        ]
        assert (fraction(pair["supported_regret"]) == 0) == all(equalities)
        if complete:
            pair["forecast_risk"] = pair["supported_forecast_risk"]
            pair["regret"] = pair["supported_regret"]
        aggregate_pairs.append(pair)

    def first(index, predicate):
        return next((row["belief_id"] for row in rows if predicate(row["pairs"][index])), None)

    counts = {
        "beliefs": len(rows),
        "input_cells": input_cells,
        "input_prediction_atoms": input_atoms,
        "pair_cells": [sum(len(row["pairs"][i]["cells"]) for row in rows) for i in range(16)],
        "supported_pair_cells": [
            sum(cell["supported"] for row in rows for cell in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "unsupported_pair_cells": [
            sum(not cell["supported"] for row in rows for cell in row["pairs"][i]["cells"])
            for i in range(16)
        ],
        "scoring_terms": scoring_terms,
        "complete_beliefs": [sum(row["pairs"][i]["complete"] for row in rows) for i in range(16)],
        "incomplete_beliefs": [
            sum(not row["pairs"][i]["complete"] for row in rows) for i in range(16)
        ],
        "positive_supported_regret_beliefs": [
            sum(fraction(row["pairs"][i]["supported_regret"]) > 0 for row in rows)
            for i in range(16)
        ],
        "positive_full_regret_beliefs": [
            sum(
                row["pairs"][i]["complete"] and fraction(row["pairs"][i]["regret"]) > 0
                for row in rows
            )
            for i in range(16)
        ],
    }
    answer = {
        "input_sha256": digest(problem),
        "levels": LEVELS,
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate_pairs},
        "witnesses": {
            "first_incomplete": [first(i, lambda pair: not pair["complete"]) for i in range(16)],
            "first_positive_supported_regret": [
                first(i, lambda pair: fraction(pair["supported_regret"]) > 0) for i in range(16)
            ],
            "first_positive_full_regret": [
                first(i, lambda pair: pair["complete"] and fraction(pair["regret"]) > 0)
                for i in range(16)
            ],
        },
        "counts": counts,
    }
    return copy.deepcopy(answer)


@pytest.fixture(scope="session")
def pinned_w():
    path = HERE.parent / "qr-05w-noisy-readouts-2026-09-07" / "results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 6756094 and hashlib.sha256(raw).hexdigest() == W_SHA
    envelope = json.loads(raw)
    assert (
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode() == raw
    native(envelope["suite"])
    return envelope["suite"]


def case_problem(case):
    return {
        "schema_version": "det8-qr05x-problem-v1",
        "family": "qr05x_noise_misspecification",
        "beliefs": [
            {
                "belief_id": row["belief_id"],
                "weight": row["weight"],
                "channels": [
                    {
                        "level": channel["level"],
                        "cells": [
                            {key: cell[key] for key in ("value", "probability", "prediction")}
                            for cell in channel["cells"]
                        ],
                    }
                    for channel in row["channels"]
                ],
            }
            for row in case["analysis"]["beliefs"]
        ],
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05x_test_direct", "misspecification.py"),
        private_module("_qr05x_test_reference", "reference_qr05x.py"),
    )


@pytest.fixture(scope="session")
def analyses(executors, pinned_w):
    result = []
    for case in pinned_w["cases"]:
        problem = case_problem(case)
        before = wire(problem)
        result.append(tuple(module.analyze(problem) for module in executors))
        assert wire(problem) == before
    return result


@pytest.fixture(scope="session")
def expected(pinned_w):
    return [independently_score(case_problem(case)) for case in pinned_w["cases"]]


@pytest.fixture(scope="session")
def aggregate():
    runner = private_module("_qr05x_test_runner", "study.py")
    return runner, runner.run_suite()


def cell(report, probability, prediction):
    return {"value": symbol(report), "probability": fw(probability), "prediction": law(prediction)}


def problem_of(channels):
    return {
        "schema_version": "det8-qr05x-problem-v1",
        "family": "qr05x_noise_misspecification",
        "beliefs": [
            {
                "belief_id": 0,
                "weight": [1, 1],
                "channels": [
                    {"level": list(level), "cells": copy.deepcopy(cells)}
                    for level, cells in zip(LEVELS, channels, strict=True)
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
        return problem_of([actual, assumed, actual, assumed])
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


@pytest.fixture(scope="session")
def micro_analyses(executors):
    result = {}
    for kind in (
        "balanced",
        "biased",
        "opposed",
        "disjoint",
        "partial",
        "same_law",
        "equal_scalar",
    ):
        p = micro_problem(kind)
        actual = tuple(module.analyze(p) for module in executors)
        assert wire(actual[0]) == wire(actual[1]) == wire(independently_score(p))
        result[kind] = actual[0]
    return result


@pytest.mark.parametrize("case_index", range(6))
def test_all_16_pair_outputs_equal_independent_outcome_scoring_oracle(
    analyses, expected, case_index
):
    a, b = analyses[case_index]
    assert wire(a) == wire(b) == wire(expected[case_index])
    assert wire(json.loads(wire(a))) == wire(a)
    assert len(wire(a)) <= 128 * 1024 * 1024


def test_exact_projection_preserves_482_histories_and_original_actual_weights(pinned_w, expected):
    assert sum(len(case["analysis"]["beliefs"]) for case in pinned_w["cases"]) == 482
    for case, a in zip(pinned_w["cases"], expected, strict=True):
        p = case_problem(case)
        assert a["input_sha256"] == digest(p)
        assert [row["weight"] for row in p["beliefs"]] == [
            row["weight"] for row in case["analysis"]["beliefs"]
        ]
        for projected, producer in zip(p["beliefs"], case["analysis"]["beliefs"], strict=True):
            for channel, original in zip(projected["channels"], producer["channels"], strict=True):
                assert channel["level"] == original["level"]
                assert channel["cells"] == [
                    {key: c[key] for key in ("value", "probability", "prediction")}
                    for c in original["cells"]
                ]


def test_fixed_W_diagonals_positive_noise_support_and_N_forecasts_are_controls(pinned_w, expected):
    for case, a in zip(pinned_w["cases"], expected, strict=True):
        for row, producer in zip(a["beliefs"], case["analysis"]["beliefs"], strict=True):
            for i in range(4):
                diagonal = row["pairs"][4 * i + i]
                assert diagonal["complete"] is True and diagonal["regret"] == [0, 1]
                assert diagonal["forecast_risk"] == producer["channels"][i]["expected_risk"]
                for j in (1, 2, 3):
                    assert row["pairs"][4 * i + j]["complete"] is True
                full_replacement = row["pairs"][4 * i + 3]
                assert (
                    full_replacement["forecast_risk"] == producer["controls"]["N"]["expected_risk"]
                )
        for i in range(4):
            assert (
                a["aggregate"]["pairs"][4 * i + 3]["forecast_risk"]
                == (case["analysis"]["aggregate"]["N_risk"])
            )


def test_coverage_decomposition_counts_and_first_witnesses_are_not_sign_assumptions(expected):
    for a in expected:
        rows = a["beliefs"]
        for index, aggregate_pair in enumerate(a["aggregate"]["pairs"]):
            i, j = divmod(index, 4)
            assert (aggregate_pair["actual_index"], aggregate_pair["assumed_index"]) == (i, j)
            for key in (
                "bayes_risk",
                "coverage",
                "unsupported_mass",
                "supported_bayes_risk",
                "supported_forecast_risk",
                "supported_regret",
            ):
                assert aggregate_pair[key] == fw(
                    sum(
                        fraction(row["weight"]) * fraction(row["pairs"][index][key]) for row in rows
                    )
                )
            assert aggregate_pair["complete"] == all(
                row["pairs"][index]["complete"] for row in rows
            )
            assert aggregate_pair["checks"]["full_decomposition"] is (
                True if aggregate_pair["complete"] else None
            )
            for key, predicate in (
                ("first_incomplete", lambda p: not p["complete"]),
                ("first_positive_supported_regret", lambda p: fraction(p["supported_regret"]) > 0),
                (
                    "first_positive_full_regret",
                    lambda p: p["complete"] and fraction(p["regret"]) > 0,
                ),
            ):
                ids = [row["belief_id"] for row in rows if predicate(row["pairs"][index])]
                assert a["witnesses"][key][index] == (ids[0] if ids else None)
            assert a["counts"]["pair_cells"][index] == (
                a["counts"]["supported_pair_cells"][index]
                + a["counts"]["unsupported_pair_cells"][index]
            )
            assert a["counts"]["complete_beliefs"][index] + a["counts"]["incomplete_beliefs"][
                index
            ] == len(rows)
            for row in rows:
                pair = row["pairs"][index]
                cells = pair["cells"]
                coverage = sum(fraction(c["actual_probability"]) for c in cells if c["supported"])
                assert pair["coverage"] == fw(coverage)
                assert sum(fraction(c["actual_probability"]) for c in cells) == 1
                assert pair["supported_forecast_risk"] == fw(
                    fraction(pair["supported_bayes_risk"]) + fraction(pair["supported_regret"])
                )
                for c in cells:
                    if c["supported"]:
                        assert c["predictions_equal"] == (c["forecast"] == c["actual_prediction"])
                        assert fraction(c["forecast_risk"]) == fraction(c["bayes_risk"]) + fraction(
                            c["regret"]
                        )
                        assert (fraction(c["regret"]) == 0) == c["predictions_equal"]
                    else:
                        assert c["assumed_probability"] == [0, 1]
                        assert (
                            c["forecast"]
                            is c["forecast_risk"]
                            is c["regret"]
                            is c["predictions_equal"]
                            is None
                        )


def test_opposed_deterministic_forecasts_attain_risk_and_regret_two(micro_analyses):
    a = micro_analyses["opposed"]
    pair = a["beliefs"][0]["pairs"][1]
    assert pair["bayes_risk"] == [0, 1]
    assert pair["forecast_risk"] == pair["regret"] == [2, 1]
    assert pair["complete"] is True and pair["coverage"] == [1, 1]
    for cell_row in pair["cells"]:
        assert cell_row["forecast_risk"] == cell_row["regret"] == [2, 1]
        assert cell_row["predictions_equal"] is False
    assert a["aggregate"]["pairs"][1]["forecast_risk"] == [2, 1]


def test_zero_coverage_is_supported_and_does_not_create_zero_full_risk(micro_analyses):
    a = micro_analyses["disjoint"]
    for index, pair in enumerate(a["beliefs"][0]["pairs"]):
        i, j = divmod(index, 4)
        if i == j:
            assert pair["coverage"] == [1, 1] and pair["forecast_risk"] == [0, 1]
            continue
        assert pair["coverage"] == [0, 1] and pair["unsupported_mass"] == [1, 1]
        assert pair["bayes_risk"] == [0, 1]
        assert (
            pair["supported_bayes_risk"]
            == pair["supported_forecast_risk"]
            == pair["supported_regret"]
            == [0, 1]
        )
        assert pair["forecast_risk"] is pair["regret"] is None and pair["complete"] is False
        assert pair["checks"]["zero_regret_iff_equal"] is True
        assert pair["checks"]["full_decomposition"] is None
        assert len(pair["cells"]) == 1 and pair["cells"][0]["supported"] is False
        assert a["aggregate"]["pairs"][index]["forecast_risk"] is None
        assert a["witnesses"]["first_incomplete"][index] == 0
        assert a["witnesses"]["first_positive_full_regret"][index] is None


def test_partial_coverage_keeps_unweighted_cell_loss_but_unrenormalized_supported_contributions(
    micro_analyses,
):
    pair = micro_analyses["partial"]["beliefs"][0]["pairs"][1]
    assert pair["coverage"] == [1, 4] and pair["unsupported_mass"] == [3, 4]
    assert pair["supported_bayes_risk"] == pair["bayes_risk"] == [0, 1]
    assert pair["supported_forecast_risk"] == pair["supported_regret"] == [1, 2]
    assert pair["forecast_risk"] is pair["regret"] is None
    supported, unsupported = pair["cells"]
    assert supported["actual_probability"] == [1, 4]
    assert supported["assumed_probability"] == [1, 2]
    assert supported["forecast_risk"] == [2, 1]
    assert unsupported["actual_probability"] == [3, 4] and unsupported["supported"] is False
    assert fraction(pair["supported_forecast_risk"]) != (
        fraction(pair["supported_forecast_risk"]) / fraction(pair["coverage"])
    )
    assert fraction(supported["assumed_probability"]) * fraction(supported["forecast_risk"]) == F(1)
    assert F(1) != fraction(pair["supported_forecast_risk"])


def test_equal_scalar_bayes_risks_do_not_imply_equal_future_laws(micro_analyses):
    pair = micro_analyses["equal_scalar"]["beliefs"][0]["pairs"][1]
    assert pair["bayes_risk"] == [3, 8]
    assert pair["forecast_risk"] == [7, 8] and pair["regret"] == [1, 2]
    for c in pair["cells"]:
        assert (
            bayes_risk(read_law(c["actual_prediction"]))
            == bayes_risk(read_law(c["forecast"]))
            == F(3, 8)
        )
        assert c["predictions_equal"] is False and c["regret"] == [1, 2]


def test_different_report_laws_need_not_change_forecasts_or_add_regret(micro_analyses):
    a = micro_analyses["same_law"]
    for pair in a["beliefs"][0]["pairs"]:
        assert pair["complete"] is True and pair["regret"] == [0, 1]
        assert pair["forecast_risk"] == pair["bayes_risk"] == [1, 2]
        assert all(c["predictions_equal"] for c in pair["cells"])
    assert any(
        c["actual_probability"] != c["assumed_probability"]
        for c in a["beliefs"][0]["pairs"][1]["cells"]
    )


def test_actual_not_assumed_report_weighting_and_no_symmetry_of_regret(micro_analyses):
    row = micro_analyses["biased"]["beliefs"][0]
    forward, reverse = row["pairs"][1], row["pairs"][4]
    assert forward["forecast_risk"] == forward["regret"] == [7, 50]
    wrong_risk = sum(
        fraction(c["assumed_probability"]) * fraction(c["forecast_risk"]) for c in forward["cells"]
    )
    assert wrong_risk == F(1, 5) != fraction(forward["forecast_risk"])
    assert reverse["forecast_risk"] == [1, 2] and reverse["bayes_risk"] == [3, 10]
    assert reverse["regret"] == [1, 5] != forward["regret"]


def test_case_aggregation_preserves_history_weights_and_incompleteness(executors):
    p = micro_problem("balanced")
    p["beliefs"][0]["weight"] = [1, 4]
    other = micro_problem("biased")["beliefs"][0]
    p["beliefs"].append({**other, "belief_id": 1, "weight": [3, 4]})
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert a["aggregate"]["pairs"][1]["forecast_risk"] == [109, 800]
        uniform = sum(fraction(row["pairs"][1]["forecast_risk"]) for row in a["beliefs"]) / 2
        assert uniform == F(53, 400) != F(109, 800)

    p["beliefs"][1]["channels"] = micro_problem("partial")["beliefs"][0]["channels"]
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        pair = a["aggregate"]["pairs"][1]
        assert pair["coverage"] == [7, 16]
        assert pair["forecast_risk"] is pair["regret"] is None
        assert pair["complete_beliefs"] == pair["incomplete_beliefs"] == 1
        assert pair["supported_forecast_risk"] == [13, 32]
        assert a["witnesses"]["first_incomplete"][1] == 1
        assert a["witnesses"]["first_positive_full_regret"][1] == 0


def test_generic_shared_marginals_are_not_a_certificate_of_W_channel_physics(executors):
    p = micro_problem("opposed")
    # Generic symbols need not satisfy N0=1 or chain/rank bounds. This API
    # scores complete experiments and must not secretly reimpose geometry.
    for b in p["beliefs"]:
        for channel in b["channels"]:
            for c in channel["cells"]:
                c["value"] = [(1 << 64) - 1] + c["value"][1:]
                for atom in c["prediction"]:
                    atom["value"] = [(1 << 64) - 1] + atom["value"][1:]
    for module in executors:
        a = module.analyze(p)
        assert wire(a) == wire(independently_score(p))
        assert a["beliefs"][0]["pairs"][1]["regret"] == [2, 1]


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
        assert a["beliefs"][0]["pairs"][0]["bayes_risk"] == fw(
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
            pair["bayes_risk"] == pair["forecast_risk"] == [1, 2] and pair["regret"] == [0, 1]
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
        a["aggregate"]["pairs"][1]["coverage"][0] = -1
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
    pair_cells = scoring = 0
    for b in p["beliefs"]:
        for actual in b["channels"]:
            for assumed in b["channels"]:
                forecasts = {tuple(c["value"]): c for c in assumed["cells"]}
                pair_cells += len(actual["cells"])
                scoring += sum(
                    len(c["prediction"]) + len(forecasts[tuple(c["value"])]["prediction"])
                    for c in actual["cells"]
                    if tuple(c["value"]) in forecasts
                )
    return pair_cells, scoring


def test_pair_and_scoring_work_caps_reject_before_any_supported_score_loop(executors, monkeypatch):
    p = micro_problem()
    work = planned_work(p)
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
    p["beliefs"] = [{"belief_id": i, "weight": [1, 512], "channels": template} for i in range(512)]
    for module in executors:
        a = module.analyze(p)
        assert a["counts"]["beliefs"] == 512
        assert a["aggregate"]["pairs"][0]["forecast_risk"] == [0, 1]
        bad = {
            **p,
            "beliefs": [
                {"belief_id": i, "weight": [1, 513], "channels": template} for i in range(513)
            ],
        }
        with pytest.raises(ValueError):
            module.analyze(bad)


def test_runner_complete_projection_outputs_controls_and_actual_counts(
    aggregate, pinned_w, expected
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
    assert wire(runner.fixtures()) == wire(pinned_w)
    assert suite["producer"] == {
        "artifact": "qr-05w-noisy-readouts-2026-09-07/results.json",
        "bytes": 6756094,
        "sha256": W_SHA,
    }
    assert suite["independent_route_equal"] is True
    for producer, actual, wanted in zip(pinned_w["cases"], suite["cases"], expected, strict=True):
        assert actual["case_id"] == producer["case_id"]
        assert actual["problem"] == case_problem(producer) == runner.case_problem(producer)
        assert wire(actual["analysis"]) == wire(wanted)
        assert actual["producer_controls"] == {
            "W_laws_are_declared_pinned_dependencies": True,
            "complete_projection_checked": True,
            "diagonal_W_risks_equal": True,
            "positive_assumed_noise_covers_actual_reports": True,
            "assumed_full_replacement_N_risk_equal": True,
            "W_channel_origin_authenticated_by_generic_API": False,
            "raw_history_reconstruction_performed_by_this_runner": False,
        }
    assert suite["public_controls"] == {
        "analyze_calls": 12,
        "invalid_analyze_calls_rejected": 14,
        "raw_orders_histories_or_artifacts_given_to_core": False,
        "noise_parameters_fitted": False,
        "fallback_forecasts_invented": False,
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
        (("beliefs", 0, "weight"), [1, 1]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "actual_probability"), [1, 2]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "assumed_probability"), [0, 1]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "actual_prediction", 0, "value", 0), -1),
        (("beliefs", 0, "pairs", 0, "cells", 0, "forecast"), None),
        (("beliefs", 0, "pairs", 0, "cells", 0, "forecast_risk"), [2, 1]),
        (("beliefs", 0, "pairs", 0, "cells", 0, "predictions_equal"), False),
        (("beliefs", 0, "pairs", 0, "coverage"), [0, 1]),
        (("beliefs", 0, "pairs", 0, "supported_regret"), [2, 1]),
        (("beliefs", 0, "pairs", 0, "checks", "full_decomposition"), None),
        (("aggregate", "pairs", 0, "forecast_risk"), None),
        (("aggregate", "pairs", 0, "complete_beliefs"), 0),
        (("witnesses", "first_incomplete", 0), 0),
        (("witnesses", "first_positive_full_regret", 0), 0),
        (("counts", "scoring_terms"), 0),
    ]


def test_runner_rejects_complete_output_law_coverage_null_and_count_corruption(
    aggregate, pinned_w, expected
):
    runner, _ = aggregate
    case, a = pinned_w["cases"][0], expected[0]
    before = wire(a)
    assert runner.check_analysis(a, case)["complete_native_output_equal"] is True
    for path, value in output_mutations(a):
        bad = replaced(a, path, value)
        assert wire(bad) != before, path
        with pytest.raises(ValueError):
            runner.check_analysis(bad, case)
    assert wire(a) == before


def test_runner_authenticates_pinned_producer_case_before_accepting_projection(
    aggregate, pinned_w, expected
):
    runner, _ = aggregate
    case, a = pinned_w["cases"][0], expected[0]
    report = runner.check_analysis(a, case)
    assert report["analysis_sha256"] == digest(a)
    for bad in (
        replaced(case, ("analysis", "beliefs", 0, "belief_id"), False),
        replaced(
            case, ("analysis", "beliefs", 0, "channels", 0, "cells", 0, "probability"), [0, 1]
        ),
        replaced(case, ("analysis", "beliefs", 0, "controls", "H", "expected_risk"), [2, 1]),
        replaced(case, ("analysis", "channel_model", "alphabet", 0, "values"), []),
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
spec = importlib.util.spec_from_file_location("_qr05x_guard_helpers", path)
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
    ("misspecification.py", "_score"), ("reference_qr05x.py", "_score_supported")
)):
    module = helpers.private_module("_qr05x_explicit_guard_" + str(index), filename)
    valid = helpers.micro_problem()
    wanted = module.analyze(valid)
    opposed = module.analyze(helpers.micro_problem("opposed"))
    require(opposed["beliefs"][0]["pairs"][1]["forecast_risk"] == [2, 1], "risk two")
    disjoint = module.analyze(helpers.micro_problem("disjoint"))
    pair = disjoint["beliefs"][0]["pairs"][1]
    require(pair["coverage"] == [0, 1] and pair["forecast_risk"] is None
            and pair["supported_forecast_risk"] == [0, 1], "zero coverage is not zero full risk")
    partial = module.analyze(helpers.micro_problem("partial"))["beliefs"][0]["pairs"][1]
    require(partial["coverage"] == [1, 4] and partial["supported_forecast_risk"] == [1, 2]
            and partial["forecast_risk"] is None, "partial support is not renormalized")
    for bad in invalid:
        reject(module.analyze, bad)
    graphs = list(graph_inputs(valid))
    require(len(graphs) == 13, "graph inventory")
    for bad in graphs:
        reject_before_dump(module.analyze, bad)
    for constant, count in zip(("MAX_PAIR_CELLS", "MAX_SCORING_TERMS"), helpers.planned_work(valid)):
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
    arithmetic = helpers.singleton_problem()
    require(module.analyze(arithmetic)["beliefs"][0]["pairs"][0]["bayes_risk"] == [20, 121],
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
runner = helpers.private_module("_qr05x_explicit_guard_runner", "study.py")
for bad in graph_inputs(helpers.micro_problem()):
    reject_before_dump(runner.require_wire, bad)
reject(lambda value: runner.require_same_wire({"x": 0}, value, "typed regression"), {"x": False})
require(before_serialization == 39, "pre-serialization rejection inventory")
expected = 2 * (len(invalid) + 13 + 8) + 14
require(rejections == expected, "explicit rejection inventory")
print(json.dumps({"rejections": rejections, "pre_serialization_rejections": before_serialization,
                  "invalid_fixture_cases": len(invalid), "optimized": bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05x.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 13 + 8) + 14,
        "pre_serialization_rejections": 39,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }
