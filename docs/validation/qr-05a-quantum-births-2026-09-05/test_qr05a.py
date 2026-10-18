"""Black-box exact checks for the fixed QR-05A research wire contract.

No RET or mutable DET implementation is imported.  Both executors are loaded
once, privately, and independently compared to mathematical identities and
prespecified positive/negative controls.  No tolerance or sampling is used.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
CASE_SPECS = {
    "phase": ("weak_phase", "2/5", (True, True, True, True)),
    "dephase": ("weak_dephase", "2/5", (True, True, True, True)),
    "phase_zero": ("weak_phase", "0", (True, True, True, True)),
    "phase_one": ("weak_phase", "1", (True, True, True, True)),
    "parity": ("parity_zx", "2/5", (True, False, False, False)),
    "parity_zero": ("parity_zx", "0", (True, False, True, True)),
    "stage": ("stage_zx", "2/5", (True, False, False, False)),
    "uniform": ("weak_phase", None, (True, True, False, False)),
}
FLAG_KEYS = (
    "normalized",
    "unweighted_diamonds_equal",
    "weighted_diamonds_equal",
    "terminal_relabeling_equal",
)


def problem(instrument="weak_phase", p="2/5", births=3):
    growth = {"kind": "uniform_ideals"} if p is None else {"kind": "percolation", "p": p}
    return {
        "schema_version": "det8-qr05a-problem-v1",
        "births": births,
        "growth": growth,
        "instrument": instrument,
    }


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("test-private module name already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load research executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05a_test_primary", "growth.py"),
        private_module("_qr05a_test_reference", "reference_qr05a.py"),
    )


@pytest.fixture(scope="session")
def results(executors):
    return {
        name: tuple(module.analyze(problem(family, probability)) for module in executors)
        for name, (family, probability, _) in CASE_SPECS.items()
    }


def decode(matrix):
    return tuple(tuple((Fraction(cell[0]), Fraction(cell[1])) for cell in row) for row in matrix)


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def mul(left, right):
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def conjugate(value):
    return value[0], -value[1]


def scale(value, weight):
    return value[0] * weight, value[1] * weight


def summed(matrices):
    matrices = tuple(matrices)
    return tuple(
        tuple(
            (
                sum((m[i][j][0] for m in matrices), Fraction(0)),
                sum((m[i][j][1] for m in matrices), Fraction(0)),
            )
            for j in range(4)
        )
        for i in range(4)
    )


def zero_map(matrix):
    return all(cell == ZERO for row in decode(matrix) for cell in row)


def history(result, order, outcomes):
    return next(
        (i, row)
        for i, row in enumerate(result["levels"][-1]["histories"])
        if row["order"] == order and row["outcomes"] == outcomes
    )


@pytest.mark.parametrize("case", CASE_SPECS)
def test_dual_implementation_agrees_on_complete_evidence(results, case):
    primary, reference = results[case]
    assert primary == reference
    assert json.loads(json.dumps(primary, allow_nan=False)) == primary


@pytest.mark.parametrize("case", CASE_SPECS)
def test_prespecified_flags_and_inventory(results, case):
    for result in results[case]:
        assert tuple(result["flags"][key] for key in FLAG_KEYS) == CASE_SPECS[case][2]
        counts = result["counts"]
        assert counts["level_histories"] == [1, 2, 8, 56]
        assert counts["normalization_rows"] == 11
        assert counts["diamond_contexts"] == 9
        assert counts["diamond_outcome_pairs"] == 36
        assert counts["terminal_relabelings"] == 160
        assert counts["nonidentity_relabelings"] == 104
        assert counts["terminal_classes"] == (54 if case == "stage" else 32)
        assert all(
            row["growth_sum"] == "1"
            and row["instrument_complete"]
            and row["birth_sum_trace_preserving"]
            for row in result["normalization"]
        )
        assert all(level["trace_preserving"] for level in result["levels"])


@pytest.mark.parametrize("case", CASE_SPECS)
def test_group_pushforward_is_partition_and_exact_map_sum(results, case):
    for result in results[case]:
        terminal = result["levels"][-1]
        members = [index for group in result["classes"] for index in group["members"]]
        assert sorted(members) == list(range(56))
        for group in result["classes"]:
            assert group["members"] == sorted(set(group["members"]))
            selected = (decode(terminal["histories"][i]["superoperator"]) for i in group["members"])
            assert summed(selected) == decode(group["superoperator"])
        assert summed(decode(group["superoperator"]) for group in result["classes"]) == decode(
            terminal["total_map"]
        )


@pytest.mark.parametrize(
    "case, expected", [("phase_zero", 48), ("phase_one", 48), ("parity_zero", 54)]
)
def test_zero_histories_are_retained_through_grouping(results, case, expected):
    for result in results[case]:
        rows = result["levels"][-1]["histories"]
        zero_indices = {i for i, row in enumerate(rows) if zero_map(row["superoperator"])}
        assert len(zero_indices) == expected == result["counts"]["zero_terminal_maps"]
        retained = {i for group in result["classes"] for i in group["members"]}
        assert zero_indices <= retained


def test_zero_growth_does_not_excuse_unweighted_quantum_conflict(results):
    for result in results["parity_zero"]:
        failures = [row for row in result["diamonds"] if not row["unweighted_equal"]]
        assert failures
        assert all(row["weighted_equal"] for row in result["diamonds"])
        assert all(row["forward_weight"] == row["reverse_weight"] == "0" for row in failures)
        assert any(
            branch["forward"] != branch["reverse"] for row in failures for branch in row["branches"]
        )


def test_stage_control_detects_pure_label_automorphisms(results):
    for result in results["stage"]:
        rows = result["levels"][-1]["histories"]
        failures = [
            r
            for r in result["relabelings"]
            if r["history"] == r["target"]
            and r["permutation"] != [0, 1, 2]
            and not r["settings_equal"]
        ]
        assert failures
        for row in failures:
            assert row["map_equal"] and not row["equal"]
            source = rows[row["history"]]
            assert row["settings_expected"] == [source["settings"][i] for i in row["permutation"]]
            assert row["settings_expected"] != rows[row["target"]]["settings"]


def test_closed_physical_parity_witness(results):
    for result in results["parity"]:
        _, forward = history(result, [[], [0], []], [1, 0, 0])
        _, reverse = history(result, [[], [], [0]], [1, 0, 0])
        assert forward["weight"] == reverse["weight"] == "18/125"
        # Input P_1 is the last row-major matrix unit, so column 3 is its output.
        forward_output = tuple(row[3] for row in decode(forward["superoperator"]))
        reverse_output = tuple(row[3] for row in decode(reverse["superoperator"]))
        assert forward_output == ((Fraction(9, 250), Fraction(0)), ZERO, ZERO, ZERO)
        assert reverse_output == (ZERO, ZERO, ZERO, ZERO)


def test_nonisomorphic_orders_can_have_identical_quantum_maps(results):
    for result in results["phase"]:
        left_index, left = history(result, [[], [0], [0]], [0, 0, 0])
        right_index, right = history(result, [[], [], [0, 1]], [0, 0, 0])
        assert left["superoperator"] == right["superoperator"]
        assert left["weight"] == right["weight"] == "12/125"
        left_group = next(g for g in result["classes"] if left_index in g["members"])
        right_group = next(g for g in result["classes"] if right_index in g["members"])
        assert left_group["key"]["relation"] != right_group["key"]["relation"]
        assert left_group is not right_group


def closed_order_weight(order, probability):
    if probability is not None:
        p = Fraction(probability)
        links = sum(1 for past in order for i in past if not any(i in order[j] for j in past))
        incomparable = len(order) * (len(order) - 1) // 2 - sum(map(len, order))
        return p**links * (1 - p) ** incomparable
    weight = Fraction(1)
    for n in range(len(order)):
        count = sum(
            all(not bits[j] or all(bits[i] for i in order[j]) for j in range(n))
            for bits in product((False, True), repeat=n)
        )
        weight /= count
    return weight


def closed_positive_map(row, family, probability):
    bits, order = row["outcomes"], row["order"]
    n0, n1 = bits.count(0), bits.count(1)
    odd = sum(sum(bits[i] for i in past) % 2 for past in order)
    a = Fraction(3, 5) ** n0 * Fraction(4, 5) ** n1
    b = Fraction(4, 5) ** n0 * Fraction(3, 5) ** n1
    phase = (
        ONE,
        (Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(-1)),
    )[odd % 4]
    diagonal = ((a, Fraction(0)), scale(phase, b))
    weight = closed_order_weight(order, probability)
    output = []
    for i, j in product(range(2), repeat=2):
        entry = scale(mul(diagonal[i], conjugate(diagonal[j])), weight)
        if family == "weak_dephase" and i != j:
            entry = scale(entry, Fraction(-7, 25) ** len(bits))
        output.append(tuple(entry if k == 2 * i + j else ZERO for k in range(4)))
    return weight, tuple(output)


@pytest.mark.parametrize("case", ("phase", "dephase", "phase_zero", "phase_one", "uniform"))
def test_independent_closed_form_all_positive_family_histories(results, case):
    family, probability, _ = CASE_SPECS[case]
    for result in results[case]:
        for level in result["levels"]:
            for row in level["histories"]:
                weight, expected = closed_positive_map(row, family, probability)
                assert Fraction(row["weight"]) == weight
                assert decode(row["superoperator"]) == expected


@pytest.mark.parametrize(
    "births, levels, parents, diamonds, comparisons, nonidentity",
    [(1, [1, 2], 1, 0, 2, 0), (2, [1, 2, 8], 3, 1, 12, 4)],
)
@pytest.mark.parametrize("family", ("weak_phase", "weak_dephase", "parity_zx", "stage_zx"))
def test_smaller_birth_bounds_and_vacuity(
    executors, births, levels, parents, diamonds, comparisons, nonidentity, family
):
    outputs = [module.analyze(problem(family, births=births)) for module in executors]
    assert outputs[0] == outputs[1]
    for result in outputs:
        counts = result["counts"]
        assert counts["level_histories"] == levels
        assert counts["normalization_rows"] == parents
        assert counts["diamond_contexts"] == diamonds
        assert counts["diamond_outcome_pairs"] == 4 * diamonds
        assert counts["terminal_relabelings"] == comparisons
        assert counts["nonidentity_relabelings"] == nonidentity
        assert result["flags"]["normalized"]
        if births == 1:
            assert result["diamonds"] == []
            assert all(result["flags"].values())


BAD_PROBABILITIES = [
    True,
    False,
    0,
    0.4,
    None,
    [],
    {},
    "",
    " 2/5",
    "2/5 ",
    "0.4",
    "+1",
    "02/5",
    "2/05",
    "4/10",
    "0/1",
    "1/1",
    "-0",
    "-0/1",
    "1/0",
    "NaN",
    "inf",
    "1e-1",
    "-1/5",
    "6/5",
    "1/18446744073709551616",
    "9" * 257,
]


@pytest.mark.parametrize("value", BAD_PROBABILITIES)
def test_probability_schema_and_64_bit_boundary_rejections(executors, value):
    wire = problem(births=1)
    wire["growth"]["p"] = value  # None here is invalid, not the uniform-rule helper sentinel.
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(copy.deepcopy(wire))


@pytest.mark.parametrize(
    "value", ("0", "1", "1/18446744073709551615", "18446744073709551614/18446744073709551615")
)
def test_canonical_probability_boundary_values_are_accepted(executors, value):
    first, second = (module.analyze(problem(p=value, births=1)) for module in executors)
    assert first == second
    assert first["flags"]["normalized"]


@pytest.mark.parametrize("value", (True, False, 0, -1, 4, 1.0, "2", None, []))
def test_birth_count_is_a_strict_bounded_integer(executors, value):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(problem(births=value))


def invalid_shapes():
    base = problem(births=1)
    cases = [None, [], "problem"]
    for key in base:
        value = copy.deepcopy(base)
        del value[key]
        cases.append(value)
    cases.append({**base, "future": 1})
    for key, value in (
        ("schema_version", "wrong"),
        ("schema_version", True),
        ("instrument", "unknown"),
        ("instrument", []),
        ("growth", None),
        ("growth", []),
        ("growth", {"kind": "percolation"}),
        ("growth", {"kind": "percolation", "p": "2/5", "extra": 0}),
        ("growth", {"kind": "uniform_ideals", "p": "2/5"}),
        ("growth", {"kind": "unknown"}),
        ("growth", {"kind": True}),
    ):
        cases.append({**base, key: value})
    return cases


@pytest.mark.parametrize("wire", invalid_shapes())
def test_unknown_missing_and_malformed_fields_are_rejected(executors, wire):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(copy.deepcopy(wire))


def test_optimized_python_retains_valid_execution_and_explicit_rejections(tmp_path):
    # The subprocess intentionally contains no Python assertions: -O cannot
    # erase its acceptance/rejection checks or turn a bad validator into a pass.
    script = r"""
import copy, importlib.util, json, sys
from pathlib import Path
base = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05a-problem-v1", "births":1,
         "growth":{"kind":"percolation", "p":"2/5"}, "instrument":"weak_phase"}
outputs = []
for number, filename in enumerate(("growth.py", "reference_qr05a.py")):
    name = "_qr05a_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, base / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    output = module.analyze(valid)
    if output["counts"]["level_histories"] != [1, 2] or not all(output["flags"].values()):
        raise RuntimeError("valid optimized execution differs")
    outputs.append(output)
    bad = []
    for value in (True, False, 0, 4):
        bad.append({**valid, "births": value})
    for value in ("4/10", "1/18446744073709551616", "NaN", 0.4):
        bad.append({**valid, "growth": {"kind":"percolation", "p":value}})
    bad.append({**valid, "extra": 1})
    for wire in bad:
        try:
            module.analyze(copy.deepcopy(wire))
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized validation accepted invalid input")
if outputs[0] != outputs[1]:
    raise RuntimeError("optimized routes disagree")
print(json.dumps({"valid_routes": 2, "explicit_rejections": 18}))
"""
    environment = dict(os.environ, PYTHONPYCACHEPREFIX=str(tmp_path / "bytecode"))
    completed = subprocess.run(
        [sys.executable, "-O", "-c", script, str(HERE)],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 18}
