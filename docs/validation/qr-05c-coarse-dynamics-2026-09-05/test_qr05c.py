"""Black-box QR-05C wire, complete-map, and coarse-dynamics tests.

Only this bounded research directory is loaded.  Exact Fraction-pair helpers
below are independent of both executors and their pinned arithmetic sources.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CASES = (
    "weak_phase",
    "grouped_dephase",
    "zero_link_boundary",
    "chain_boundary",
    "normalized_noncovariant_growth",
)
SUMMARIES = ("marked_order", "shape_ones", "link_counts_ones", "size_ones")
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
HALF = Fraction(1, 2)


def problem(case="weak_phase"):
    return {"schema_version": "det8-qr05c-problem-v1", "case": case}


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
        private_module("_qr05c_test_primary", "dynamics.py"),
        private_module("_qr05c_test_reference", "reference_qr05c.py"),
    )


@pytest.fixture(scope="session")
def results(executors):
    return {case: tuple(module.analyze(problem(case)) for module in executors) for case in CASES}


def pair(value):
    return Fraction(value[0]), Fraction(value[1])


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def negate(value):
    return -value[0], -value[1]


def mul(left, right):
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def scaled(value, scalar):
    return value[0] * scalar, value[1] * scalar


def summed(values):
    values = tuple(values)
    return sum((value[0] for value in values), Fraction(0)), sum(
        (value[1] for value in values), Fraction(0)
    )


def diagonal(result, index):
    assert type(index) is int and 0 <= index < len(result["map_bank"])
    return tuple(pair(value) for value in result["map_bank"][index])


def sum_maps(result, indices):
    maps = [diagonal(result, index) for index in indices]
    return tuple(summed(matrix[i] for matrix in maps) for i in range(4))


def trace_preserving(matrix):
    return matrix[0] == matrix[3] == ONE


def is_cp(matrix):
    a, b, c, d = matrix
    return (
        a[1] == d[1] == 0
        and a[0] >= 0
        and d[0] >= 0
        and b == (c[0], -c[1])
        and a[0] * d[0] >= b[0] ** 2 + b[1] ** 2
    )


def input_state(bloch):
    x, y, z = map(Fraction, bloch)
    return (
        (HALF * (1 + z), Fraction(0)),
        (HALF * x, -HALF * y),
        (HALF * x, HALF * y),
        (HALF * (1 - z), Fraction(0)),
    )


def apply(matrix, state):
    return tuple(mul(a, b) for a, b in zip(matrix, state))


def effect_probability(state, effect):
    if effect == "P0":
        value = state[0]
    elif effect == "P1":
        value = state[3]
    elif effect in ("Px", "P+X"):
        value = scaled(summed(state), HALF)
    elif effect in ("Py", "P+Y"):
        value = scaled(
            add(
                add(state[0], state[3]),
                mul((Fraction(0), Fraction(1)), add(state[1], negate(state[2]))),
            ),
            HALF,
        )
    else:
        raise AssertionError(f"unknown fixed witness effect {effect!r}")
    assert value[1] == 0
    return value[0]


def quotient(result, name):
    return next(row for row in result["quotients"] if row["name"] == name)


def class_indices(partition, count):
    lookup = [None] * count
    for index, group in enumerate(partition):
        assert group["members"] == sorted(set(group["members"]))
        assert group["members"]
        for history in group["members"]:
            assert type(history) is int and 0 <= history < count
            assert lookup[history] is None
            lookup[history] = index
    assert all(index is not None for index in lookup)
    assert [group["members"][0] for group in partition] == sorted(
        group["members"][0] for group in partition
    )
    return lookup


@pytest.mark.parametrize("case", CASES)
def test_complete_dual_implementation_agreement(results, case):
    direct, reference = results[case]
    assert direct == reference
    assert json.loads(json.dumps(direct, allow_nan=False)) == direct


@pytest.mark.parametrize("case", CASES)
def test_inventory_and_canonical_unique_cp_map_bank(results, case):
    for result in results[case]:
        assert result["case"] == case
        assert result["counts"]["level_histories"] == [1, 2, 8, 56, 640]
        assert [len(level["histories"]) for level in result["levels"]] == [1, 2, 8, 56, 640]
        assert result["counts"]["raw_birth_edges"] == 706
        bank = result["map_bank"]
        assert result["counts"]["map_bank_entries"] == len(bank)
        flattened = []
        for index, encoded in enumerate(bank):
            assert type(encoded) is list and len(encoded) == 4
            for cell in encoded:
                assert type(cell) is list and len(cell) == 2
                assert all(type(token) is str and str(Fraction(token)) == token for token in cell)
            flattened.append(tuple(token for cell in encoded for token in cell))
            assert is_cp(diagonal(result, index))
        assert diagonal(result, 0) == (ZERO, ZERO, ZERO, ZERO)
        assert len(set(flattened)) == len(flattened)
        assert flattened[1:] == sorted(flattened[1:])
        assert sum(len(row) for step in result["fine_steps"] for row in step["rows"]) == 706


@pytest.mark.parametrize("case", CASES)
def test_complete_fine_and_representative_rows_preserve_trace_not_state(results, case):
    for result in results[case]:
        nonidentity = []
        for step in result["fine_steps"]:
            assert len(step["rows"]) == len(result["levels"][step["births"]]["histories"])
            for row in step["rows"]:
                matrix = sum_maps(result, [edge["kernel"] for edge in row])
                assert trace_preserving(matrix)
                assert is_cp(matrix)
                nonidentity.append(matrix != (ONE, ONE, ONE, ONE))
                assert [(tuple(edge["precursor"]), edge["outcome"]) for edge in row] == sorted(
                    (tuple(edge["precursor"]), edge["outcome"]) for edge in row
                )
        for q in result["quotients"]:
            for step in q["steps"] + q["two_steps"]:
                for row in step["actual_rows"] + step["representative_rows"]:
                    matrix = sum_maps(result, row)
                    assert trace_preserving(matrix)
                    assert is_cp(matrix)
        assert any(nonidentity), "trace preservation must not be confused with the identity channel"


@pytest.mark.parametrize("case", CASES)
def test_nested_partitions_class_counts_and_refinements(results, case):
    for result in results[case]:
        assert [q["name"] for q in result["quotients"]] == list(SUMMARIES)
        for name, expected in (
            ("marked_order", [1, 2, 7, 32, 192]),
            ("shape_ones", [1, 2, 6, 20, 80]),
            ("size_ones", [1, 2, 3, 4, 5]),
        ):
            assert [len(p) for p in quotient(result, name)["partitions"]] == expected
        assert result["counts"]["marked_classes"] == [1, 2, 7, 32, 192]
        assert len(quotient(result, "link_counts_ones")["partitions"][3]) < 20
        for q in result["quotients"]:
            for n, partition in enumerate(q["partitions"]):
                class_indices(partition, len(result["levels"][n]["histories"]))
        assert [(r["fine"], r["coarse"]) for r in result["refinements"]] == list(
            pairwise(SUMMARIES)
        )
        for refinement in result["refinements"]:
            fine, coarse = (
                quotient(result, refinement["fine"]),
                quotient(result, refinement["coarse"]),
            )
            assert len(refinement["levels"]) == 5
            for row in refinement["levels"]:
                n = row["births"]
                fine_partition, coarse_partition = fine["partitions"][n], coarse["partitions"][n]
                lookup = class_indices(coarse_partition, len(result["levels"][n]["histories"]))
                expected = [lookup[group["members"][0]] for group in fine_partition]
                assert row["parent_classes"] == expected and row["valid"] is True
                assert all(
                    all(lookup[h] == expected[i] for h in group["members"])
                    for i, group in enumerate(fine_partition)
                )


@pytest.mark.parametrize("case", CASES)
def test_marked_order_universal_one_and_two_step_closure(results, case):
    for result in results[case]:
        marked = quotient(result, "marked_order")
        assert [row["births"] for row in marked["steps"]] == [0, 1, 2, 3]
        assert [row["births"] for row in marked["two_steps"]] == [0, 1, 2]
        for step in marked["steps"] + marked["two_steps"]:
            assert step["consistent"] is True
            assert step["all_fixed_source_branches_equal"] is True
            assert step["conflicts"] == [] and step["first_witness"] is None


def test_uniform_growth_quotient_closure_does_not_certify_source_covariance(results):
    for result in results["normalized_noncovariant_growth"]:
        marked = quotient(result, "marked_order")
        assert all(row["consistent"] for row in marked["steps"] + marked["two_steps"])
        by_size = {row["births"]: row for row in result["source_covariance"]}
        assert by_size[3]["constant"] is False and by_size[3]["conflicts"]
        assert by_size[4]["constant"] is False and by_size[4]["conflicts"]
    for case in CASES[:-1]:
        for result in results[case]:
            assert all(
                row["constant"] and not row["conflicts"] for row in result["source_covariance"]
            )


@pytest.mark.parametrize("case", CASES)
def test_conflicts_source_relative_flags_and_witnesses_are_recomputed(results, case):
    allowed_inputs = {("0", "0", "0"), ("1/2", "0", "0"), ("0", "1/2", "0"), ("0", "0", "1/2")}
    for result in results[case]:
        for q in result["quotients"]:
            for step in q["steps"] + q["two_steps"]:
                n = step["births"]
                parents = q["partitions"][n]
                history_rows = result["levels"][n]["histories"]
                lookup = class_indices(parents, len(history_rows))
                expected_conflicts, source_equal = [], True
                for h, actual in enumerate(step["actual_rows"]):
                    class_index = lookup[h]
                    representative = parents[class_index]["members"][0]
                    trial = step["representative_rows"][class_index]
                    targets = [i for i, (a, b) in enumerate(zip(actual, trial)) if a != b]
                    assert len(actual) == len(trial)
                    if targets:
                        expected_conflicts.append(
                            {"history": h, "representative": representative, "targets": targets}
                        )
                    source = diagonal(result, history_rows[h]["source"])
                    for target in targets:
                        left, right = (
                            diagonal(result, actual[target]),
                            diagonal(result, trial[target]),
                        )
                        if any(
                            mul(add(a, negate(b)), s) != ZERO
                            for a, b, s in zip(left, right, source)
                        ):
                            source_equal = False
                assert step["conflicts"] == expected_conflicts
                assert step["consistent"] is (not expected_conflicts)
                assert step["all_fixed_source_branches_equal"] is source_equal
                witness = step["first_witness"]
                if not expected_conflicts:
                    assert witness is None
                    continue
                first = expected_conflicts[0]
                assert witness["history"] == first["history"]
                assert witness["representative"] == first["representative"]
                assert witness["target"] == first["targets"][0]
                bloch = tuple(witness["input_bloch"])
                assert bloch in allowed_inputs
                assert sum(Fraction(value) ** 2 for value in bloch) < 1
                actual_index = step["actual_rows"][witness["history"]][witness["target"]]
                trial_index = step["representative_rows"][lookup[witness["history"]]][
                    witness["target"]
                ]
                state = input_state(bloch)
                actual = effect_probability(
                    apply(diagonal(result, actual_index), state), witness["effect"]
                )
                proposed = effect_probability(
                    apply(diagonal(result, trial_index), state), witness["effect"]
                )
                assert actual == Fraction(witness["actual_probability"])
                assert proposed == Fraction(witness["proposed_probability"])
                assert 0 <= actual <= 1 and 0 <= proposed <= 1 and actual != proposed


def test_chain_record_control_keeps_equal_traces_but_distinct_outputs(results):
    for result in results["weak_phase"]:
        control = result["controls"]["chain_record"]
        assert control["births"] == 2 and control["quotient"] == "shape_ones"
        records = [result["levels"][2]["histories"][i] for i in control["histories"]]
        assert [r["order"] for r in records] == [[[], [0]], [[], [0]]]
        assert [r["outcomes"] for r in records] == [[0, 1], [1, 0]]
        first, second = (diagonal(result, i) for i in control["kernels"])
        assert first[0] == second[0] and first[3] == second[3]
        assert first[1] == (Fraction(72, 625), Fraction(0))
        assert second[1] == (Fraction(0), Fraction(-72, 625))
        assert first != second
        assert control["trace_probabilities"][0] == control["trace_probabilities"][1]
        assert control["probabilities_Px"][0] != control["probabilities_Px"][1]


def test_delayed_failure_first_step_matches_but_full_two_step_outputs_differ(results):
    for result in results["weak_phase"]:
        control = result["controls"]["delayed"]
        assert control["births"] == 1 and control["quotient"] == "shape_ones"
        assert control["one_step_exact"] is True
        source = result["levels"][1]["histories"][control["history"]]
        assert source["order"] == [[]] and source["outcomes"] == [1]
        assert control["input_bloch"] == ["1", "0", "0"]
        state = input_state(control["input_bloch"])
        actual = apply(diagonal(result, control["actual"]), state)
        proposed = apply(diagonal(result, control["proposed"]), state)
        scale = Fraction(1, 78125)
        assert actual == (
            (486 * scale, Fraction(0)),
            (-864 * scale, Fraction(0)),
            (-864 * scale, Fraction(0)),
            (1536 * scale, Fraction(0)),
        )
        assert proposed == (
            (486 * scale, Fraction(0)),
            (Fraction(0), -864 * scale),
            (Fraction(0), 864 * scale),
            (1536 * scale, Fraction(0)),
        )
        assert [
            tuple(pair(cell) for row in matrix for cell in row) for matrix in control["outputs"]
        ] == [actual, proposed]
        assert list(map(Fraction, control["trace_probabilities"])) == [Fraction(2022, 78125)] * 2
        assert list(map(Fraction, control["probabilities_Px"])) == [
            Fraction(147, 78125),
            Fraction(1011, 78125),
        ]
        assert effect_probability(actual, "P+X") == Fraction(147, 78125)
        assert effect_probability(proposed, "P+X") == Fraction(1011, 78125)


def test_fork_join_coarse_counts_can_fail_growth_prediction(results):
    for result in results["weak_phase"]:
        control = result["controls"]["fork_join"]
        assert control["parent_class_same"] is True
        assert control["one_step_rows_equal"] is False
        assert control["counts_probe_incomparable"] == 1
        assert list(map(Fraction, control["probabilities"])) == [Fraction(4, 25), Fraction(2, 5)]


@pytest.mark.parametrize("case", CASES)
def test_record_location_control_is_resolved_in_actual_rows(results, case):
    for result in results[case]:
        control = result["controls"]["record_location"]
        assert control["births"] == 3 and control["quotient"] == "shape_ones"
        assert control["parent_class_same"] is True
        q = quotient(result, "shape_ones")
        step = next(s for s in q["steps"] if s["births"] == 3)
        left, right = [step["actual_rows"][i] for i in control["histories"]]
        targets = [i for i, (a, b) in enumerate(zip(left, right)) if a != b]
        assert control["row_equal"] is (not targets)
        assert control["first_target"] == (targets[0] if targets else None)
        assert control["kernels"] == ([left[targets[0]], right[targets[0]]] if targets else [])


@pytest.mark.parametrize("case", CASES)
def test_parent_multiplicity_cannot_be_summed_twice(results, case):
    for result in results[case]:
        control = result["controls"]["wrong_parent_sum"]
        assert control["births"] == 2 and control["quotient"] == "marked_order"
        assert len(control["members"]) == 2
        correct = sum_maps(result, control["correct_row"])
        wrong = sum_maps(result, control["wrong_row"])
        assert trace_preserving(correct) and not trace_preserving(wrong)
        assert wrong == tuple(scaled(cell, 2) for cell in correct)
        assert Fraction(control["correct_trace"]) == 1
        assert Fraction(control["wrong_trace"]) == 2
        assert (
            effect_probability(apply(wrong, input_state(["0", "0", "0"])), "P0")
            + effect_probability(apply(wrong, input_state(["0", "0", "0"])), "P1")
            == 2
        )


def test_fixed_source_equality_does_not_replace_universal_closure(results):
    for result in results["chain_boundary"]:
        q = quotient(result, "link_counts_ones")
        step = next(s for s in q["steps"] if s["births"] == 3)
        assert step["consistent"] is False
        assert step["all_fixed_source_branches_equal"] is True
        assert step["conflicts"]
        # Every discrepant branch is source-impossible here, not removed.
        for conflict in step["conflicts"]:
            source = result["levels"][3]["histories"][conflict["history"]]["source"]
            assert diagonal(result, source) == (ZERO, ZERO, ZERO, ZERO)


def malformed_inputs():
    base = problem()
    return [
        None,
        [],
        True,
        False,
        "weak_phase",
        {},
        {"schema_version": base["schema_version"]},
        {"case": "weak_phase"},
        {**base, "extra": 0},
        {**base, "births": 3},
        *({**base, "schema_version": value} for value in (None, True, False, 1, [], "wrong")),
        *(
            {**base, "case": value}
            for value in (None, True, False, 1, [], {}, "unknown", "weak_dephase", "")
        ),
    ]


@pytest.mark.parametrize("wire", malformed_inputs())
def test_strict_input_schema_rejects_unknown_fields_types_and_booleans(executors, wire):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(copy.deepcopy(wire))


def test_optimized_execution_retains_explicit_schema_rejections(tmp_path):
    script = r"""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1])
valid = {"schema_version":"det8-qr05c-problem-v1", "case":"zero_link_boundary"}
outputs = []
for number, filename in enumerate(("dynamics.py", "reference_qr05c.py")):
    name = "_qr05c_optimized_test_" + str(number)
    spec = importlib.util.spec_from_file_location(name, root / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("executor unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    output = module.analyze(valid)
    if output["counts"]["level_histories"] != [1,2,8,56,640]:
        raise RuntimeError("valid optimized execution differs")
    marked = next(q for q in output["quotients"] if q["name"] == "marked_order")
    if not all(row["consistent"] for row in marked["steps"] + marked["two_steps"]):
        raise RuntimeError("marked closure failed")
    outputs.append(output)
    for bad in (True, {**valid,"extra":1}, {**valid,"case":True}, {**valid,"case":False},
                {**valid,"schema_version":True}, {**valid,"case":"unknown"}):
        try:
            module.analyze(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("optimized validation accepted an invalid input")
if outputs[0] != outputs[1]:
    raise RuntimeError("optimized implementations disagree")
print(json.dumps({"valid_routes":2,"explicit_rejections":12}))
"""
    environment = dict(os.environ, PYTHONPYCACHEPREFIX=str(tmp_path / "bytecode"))
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
        env=environment,
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    assert json.loads(completed.stdout) == {"valid_routes": 2, "explicit_rejections": 12}
