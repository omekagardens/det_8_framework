"""Independent bounded fixtures for QR-01; no RET/package imports or sampling.

These tests supplement, rather than replace, the retained finite study.  Wire
fixtures are defined here without importing its fixture or execution helpers.
"""

import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import exact
import pytest
import reference

HALF = Fraction(1, 2)


def matrix(rows):
    result = []
    for row in rows:
        decoded = []
        for value in row:
            real, imag = value if type(value) is tuple else (value, 0)
            decoded.append([str(Fraction(real)), str(Fraction(imag))])
        result.append(decoded)
    return result


I = matrix(((1, 0), (0, 1)))
P0 = matrix(((1, 0), (0, 0)))
P1 = matrix(((0, 0), (0, 1)))
PX_PLUS = matrix(((HALF, HALF), (HALF, HALF)))
PX_MINUS = matrix(((HALF, -HALF), (-HALF, HALF)))
PY_PLUS = matrix(((HALF, (0, -HALF)), ((0, HALF), HALF)))
PY_MINUS = matrix(((HALF, (0, HALF)), ((0, -HALF), HALF)))
S = matrix(((1, 0), (0, (0, 1))))
ZERO = matrix(((0, 0), (0, 0)))
DAMP_KEEP = matrix(((1, 0), (0, Fraction(3, 5))))
DAMP_JUMP = matrix(((0, Fraction(4, 5)), (0, 0)))


def embed(local, qubit):
    """Independent explicit computational-basis embedding for two qubits."""
    output = []
    for row in range(4):
        output_row = []
        for column in range(4):
            row_bits, col_bits = (row // 2, row % 2), (column // 2, column % 2)
            output_row.append(
                deepcopy(local[row_bits[qubit]][col_bits[qubit]])
                if row_bits[1 - qubit] == col_bits[1 - qubit]
                else ["0", "0"]
            )
        output.append(output_row)
    return output


def event(name, outcomes, support=(0,), record=None):
    return {
        "event_id": name,
        "record_id": record or f"r_{name}",
        "support": list(support),
        "outcomes": [{"label": label, "kraus": deepcopy(kraus)} for label, kraus in outcomes],
    }


def problem(events, edges=(), qubits=1):
    return {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": qubits,
        "events": deepcopy(events),
        "precedence": [list(edge) for edge in edges],
    }


def z_event(name="Z", support=(0,), embedded=False):
    operators = (embed(P0, support[0]), embed(P1, support[0])) if embedded else (P0, P1)
    return event(name, (("0", [operators[0]]), ("1", [operators[1]])), support)


def x_event(name="X"):
    return event(name, (("+", [PX_PLUS]), ("-", [PX_MINUS])))


def matrix_pairs(value):
    return tuple(tuple((entry.real, entry.imag) for entry in row) for row in value)


def map_pairs(value):
    return {record: matrix_pairs(block) for record, block in value.items()}


def basis(dimension, row, column):
    return tuple(
        tuple(exact.q(int((i, j) == (row, column))) for j in range(dimension))
        for i in range(dimension)
    )


def single_output(wire, input_wire):
    parsed = exact.parse_problem(wire)
    outputs = exact.execute_operator(
        parsed, exact.schedules(parsed)[0], exact.decode_matrix(input_wire, parsed.dimension)
    )
    return outputs


def test_complex_arithmetic_and_adjoint_are_not_only_real_fixtures():
    assert exact.q(0, 1) * exact.q(0, 1) == exact.q(-1)
    wire = problem([event("phase", (("done", [S]),))])
    parsed = exact.parse_problem(wire)
    result = exact.execute_operator(parsed, ("phase",), basis(2, 0, 1))
    expected = ((exact.q(), exact.q(0, -1)), (exact.q(), exact.q()))
    assert result[(("r_phase", "done"),)] == expected
    maps = reference.reference_schedule(wire, ("phase",))
    assert maps[(("r_phase", "done"),)][1][1] == (Fraction(0), Fraction(-1))


@pytest.mark.parametrize(
    "wire",
    [
        problem([z_event()]),
        problem([event("Y", (("+", [PY_PLUS]), ("-", [PY_MINUS])))]),
        problem([event("damping", (("keep", [DAMP_KEEP]), ("jump", [DAMP_JUMP])))]),
        problem([event("dephase", (("all", [P0, P1]),))]),
        problem([z_event(), x_event()], (("Z", "X"),)),
        problem([event("phase", (("done", [S]),)), x_event()], (("phase", "X"),)),
    ],
    ids=["Z", "complex-Y", "damping", "multi-Kraus", "ordered-ZX", "complex-SX"],
)
def test_full_operator_basis_matches_independent_superoperator_reference(wire):
    parsed = exact.parse_problem(wire)
    for order in exact.schedules(parsed):
        actual_maps = exact.operator_maps(parsed, order)
        reference_maps = reference.reference_schedule(wire, order)
        assert map_pairs(actual_maps) == reference_maps
        for row in range(parsed.dimension):
            for column in range(parsed.dimension):
                operator = basis(parsed.dimension, row, column)
                outputs = exact.execute_operator(parsed, order, operator)
                for record, block in outputs.items():
                    expected = reference.apply_superoperator(
                        reference_maps[record], exact.matrix_wire(operator)
                    )
                    assert matrix_pairs(block) == expected


def test_multiple_kraus_are_summed_incoherently_within_one_outcome():
    wire = problem([event("D", (("discarded", [P0, P1]),))])
    parsed = exact.parse_problem(wire)
    output = exact.execute_operator(parsed, ("D",), basis(2, 0, 1))
    assert output[(("r_D", "discarded"),)] == exact.zeros(2)
    # Summing the Kraus operators first would incorrectly produce identity.
    plus_state = exact.decode_matrix(PX_PLUS, 2)
    output = exact.execute_operator(parsed, ("D",), plus_state)
    assert output[(("r_D", "discarded"),)] == exact.scale(exact.identity(2), exact.q(HALF))


def test_damping_has_exact_nontrivial_branch_weights_and_coherence():
    wire = problem([event("D", (("keep", [DAMP_KEEP]), ("jump", [DAMP_JUMP])))])
    outputs = single_output(wire, P1)
    assert exact.trace(outputs[(("r_D", "keep"),)]) == exact.q(Fraction(9, 25))
    assert exact.trace(outputs[(("r_D", "jump"),)]) == exact.q(Fraction(16, 25))
    parsed = exact.parse_problem(wire)
    off_diagonal = exact.execute_operator(parsed, ("D",), basis(2, 0, 1))
    assert off_diagonal[(("r_D", "keep"),)] == exact.scale(basis(2, 0, 1), exact.q(Fraction(3, 5)))
    assert off_diagonal[(("r_D", "jump"),)] == exact.zeros(2)


def test_zero_probability_does_not_erase_a_nonzero_outcome_map():
    wire = problem([z_event()])
    parsed = exact.parse_problem(wire)
    output_zero = single_output(wire, P0)
    output_one = single_output(wire, P1)
    key = (("r_Z", "1"),)
    assert key in output_zero and output_zero[key] == exact.zeros(2)
    assert output_one[key] == exact.decode_matrix(P1, 2)
    assert exact.operator_maps(parsed, ("Z",))[key] != exact.zeros(4)


def test_identically_zero_outcome_and_zero_kraus_are_retained():
    wire = problem([event("E", (("present", [I, ZERO]), ("zero", [ZERO])))])
    parsed = exact.parse_problem(wire)
    actual = exact.operator_maps(parsed, ("E",))
    assert set(actual) == {(("r_E", "present"),), (("r_E", "zero"),)}
    assert actual[(("r_E", "zero"),)] == exact.zeros(4)
    assert map_pairs(actual) == reference.reference_schedule(wire, ("E",))


def test_empty_graph_is_identity_but_has_no_independence_comparisons():
    wire = problem([])
    parsed = exact.parse_problem(wire)
    assert exact.schedules(parsed) == ((),)
    assert exact.incomparable_pairs(parsed) == ()
    assert exact.operator_maps(parsed, ()) == {(): exact.identity(4)}
    assert map_pairs(exact.operator_maps(parsed, ())) == reference.reference_schedule(wire, ())


def test_four_event_dag_transitive_order_and_schedule_enumeration():
    events = [event(name, (("done", [I]),)) for name in "ABCD"]
    parsed = exact.parse_problem(problem(events, (("A", "B"), ("B", "C"))))
    assert exact.schedules(parsed) == (
        ("A", "B", "C", "D"),
        ("A", "B", "D", "C"),
        ("A", "D", "B", "C"),
        ("D", "A", "B", "C"),
    )
    assert exact.incomparable_pairs(parsed) == (("A", "D"), ("B", "D"), ("C", "D"))
    # The transitive A<C relation is not mistaken for an independent pair.
    fully_unordered = exact.parse_problem(problem(events))
    assert len(exact.schedules(fully_unordered)) == 24
    assert len(exact.incomparable_pairs(fully_unordered)) == 6
    for order in exact.schedules(parsed):
        assert exact.total_map(exact.operator_maps(parsed, order)) == exact.identity(4)


def test_ordered_noncommuting_measurements_are_valid_but_cannot_be_swapped():
    wire = problem([z_event(), x_event()], (("Z", "X"),))
    parsed = exact.parse_problem(wire)
    assert exact.schedules(parsed) == (("Z", "X"),)
    assert exact.incomparable_pairs(parsed) == ()
    with pytest.raises(ValueError):
        exact.execute_operator(parsed, ("X", "Z"), exact.identity(2))
    with pytest.raises(ValueError):
        reference.reference_schedule(wire, ("X", "Z"))


def test_forgetting_all_records_hides_zx_schedule_conflict():
    parsed = exact.parse_problem(problem([z_event(), x_event()]))
    left = exact.operator_maps(parsed, ("Z", "X"))
    right = exact.operator_maps(parsed, ("X", "Z"))
    assert exact.incomparable_pairs(parsed) == (("X", "Z"),)
    assert exact.difference(left, right)["kind"] == "map_entry"
    assert exact.total_map(left) == exact.total_map(right)
    pure = exact.decode_matrix(P0, 2)
    left_branches = exact.execute_operator(parsed, ("Z", "X"), pure)
    right_branches = exact.execute_operator(parsed, ("X", "Z"), pure)
    assert [exact.trace(block) for block in left_branches.values()] == [
        exact.q(HALF),
        exact.q(),
        exact.q(HALF),
        exact.q(),
    ]
    assert {exact.trace(block) for block in right_branches.values()} == {exact.q(Fraction(1, 4))}


def test_equal_complete_joint_probabilities_still_hide_branch_state_conflict():
    parsed = exact.parse_problem(problem([z_event(), x_event()]))
    mixed = exact.scale(exact.identity(2), exact.q(HALF))
    left = exact.execute_operator(parsed, ("Z", "X"), mixed)
    right = exact.execute_operator(parsed, ("X", "Z"), mixed)
    assert set(left) == set(right)
    assert all(
        exact.trace(left[key]) == exact.trace(right[key]) == exact.q(Fraction(1, 4)) for key in left
    )
    assert left != right
    key = (("r_X", "+"), ("r_Z", "0"))
    assert left[key] == exact.scale(exact.decode_matrix(PX_PLUS, 2), exact.q(Fraction(1, 4)))
    assert right[key] == exact.scale(exact.decode_matrix(P0, 2), exact.q(Fraction(1, 4)))


def partial_trace_b(value):
    return tuple(
        tuple(value[2 * i][2 * j] + value[2 * i + 1][2 * j + 1] for j in range(2)) for i in range(2)
    )


def test_two_qubit_local_maps_and_entangled_records_agree_in_both_schedules():
    wire = problem([z_event("A", (0,), True), z_event("B", (1,), True)], qubits=2)
    parsed = exact.parse_problem(wire)
    left, right = (exact.operator_maps(parsed, order) for order in (("A", "B"), ("B", "A")))
    assert exact.difference(left, right) is None
    for order, maps in ((("A", "B"), left), (("B", "A"), right)):
        assert map_pairs(maps) == reference.reference_schedule(wire, order)
    bell = matrix(((HALF, 0, 0, HALF), (0, 0, 0, 0), (0, 0, 0, 0), (HALF, 0, 0, HALF)))
    outputs = exact.execute_operator(parsed, ("A", "B"), exact.decode_matrix(bell, 4))
    assert len(outputs) == 4
    assert {key: exact.trace(block) for key, block in outputs.items()} == {
        (("r_A", "0"), ("r_B", "0")): exact.q(HALF),
        (("r_A", "0"), ("r_B", "1")): exact.q(),
        (("r_A", "1"), ("r_B", "0")): exact.q(),
        (("r_A", "1"), ("r_B", "1")): exact.q(HALF),
    }


def test_unconditional_no_signalling_and_conditional_steering_are_distinct():
    instruments = [
        z_event("B", (1,), True),
        event("B", (("keep", [embed(DAMP_KEEP, 1)]), ("jump", [embed(DAMP_JUMP, 1)])), (1,)),
    ]
    for instrument in instruments:
        parsed = exact.parse_problem(problem([instrument], qubits=2))
        for row in range(4):
            for column in range(4):
                operator = basis(4, row, column)
                branches = exact.execute_operator(parsed, ("B",), operator)
                unconditioned = exact.zeros(4)
                for block in branches.values():
                    unconditioned = exact.add(unconditioned, block)
                assert partial_trace_b(unconditioned) == partial_trace_b(operator)
    bell = exact.decode_matrix(
        matrix(((HALF, 0, 0, HALF), (0, 0, 0, 0), (0, 0, 0, 0), (HALF, 0, 0, HALF))), 4
    )
    parsed = exact.parse_problem(problem([instruments[0]], qubits=2))
    branches = exact.execute_operator(parsed, ("B",), bell)
    branch = branches[(("r_B", "0"),)]
    assert exact.trace(branch) == exact.q(HALF)
    conditional_a = exact.scale(partial_trace_b(branch), exact.q(2))
    assert conditional_a == exact.decode_matrix(P0, 2)
    assert conditional_a != partial_trace_b(bell)


def test_input_order_and_consistent_record_relabeling_are_only_coordinates():
    wire = problem([z_event(), x_event()], (("Z", "X"),))
    expected = exact.operator_maps(exact.parse_problem(wire), ("Z", "X"))
    changed = deepcopy(wire)
    changed["events"].reverse()
    for item in changed["events"]:
        item["record_id"] = "new_" + item["record_id"]
        for outcome in item["outcomes"]:
            outcome["label"] = "new_" + outcome["label"]
    actual = exact.operator_maps(exact.parse_problem(changed), ("Z", "X"))
    canonical = {
        tuple((rid.removeprefix("new_"), label.removeprefix("new_")) for rid, label in key): value
        for key, value in actual.items()
    }
    assert canonical == expected
    assert map_pairs(actual) == reference.reference_schedule(changed, ("Z", "X"))
    assert exact.difference(expected, actual)["kind"] == "record_inventory"


def test_one_sided_fixed_label_swap_is_not_record_equivalence():
    wire = problem([z_event()])
    changed = deepcopy(wire)
    changed["events"][0]["outcomes"][0]["label"] = "1"
    changed["events"][0]["outcomes"][1]["label"] = "0"
    left = exact.operator_maps(exact.parse_problem(wire), ("Z",))
    right = exact.operator_maps(exact.parse_problem(changed), ("Z",))
    assert set(left) == set(right)
    assert exact.difference(left, right)["kind"] == "map_entry"
    assert exact.total_map(left) == exact.total_map(right)


@pytest.mark.parametrize(
    "operator",
    [
        matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0))),
        matrix(((1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, -1))),
    ],
    ids=["CNOT-changes-spectator", "spectator-dependent-diagonal"],
)
def test_hidden_nonlocal_kraus_support_is_rejected(operator):
    wire = problem([event("E", (("done", [operator]),), (0,))], qubits=2)
    with pytest.raises(ValueError):
        exact.parse_problem(wire)
    with pytest.raises(ValueError):
        reference.reference_schedule(wire, ("E",))


def test_empty_support_allows_only_scalar_identity_operators():
    scalar3 = matrix(((Fraction(3, 5), 0), (0, Fraction(3, 5))))
    scalar4 = matrix(((Fraction(4, 5), 0), (0, Fraction(4, 5))))
    wire = problem([event("coin", (("a", [scalar3]), ("b", [scalar4])), ())])
    parsed = exact.parse_problem(wire)
    assert map_pairs(exact.operator_maps(parsed, ("coin",))) == reference.reference_schedule(
        wire, ("coin",)
    )
    bad = problem([z_event()])
    bad["events"][0]["support"] = []
    with pytest.raises(ValueError):
        exact.parse_problem(bad)
    with pytest.raises(ValueError):
        reference.reference_schedule(bad, ("Z",))


def mutate(wire, path, value):
    copied = deepcopy(wire)
    item = copied
    for key in path[:-1]:
        item = item[key]
    item[path[-1]] = deepcopy(value)
    return copied


@pytest.mark.parametrize(
    "path,value",
    [
        (("schema_version",), "unknown"),
        (("extra",), True),
        (("qubits",), True),
        (("qubits",), 0),
        (("qubits",), 3),
        (("events",), "not-list"),
        (("events", 0, "event_id"), "bad id"),
        (("events", 0, "record_id"), "bad\nrecord"),
        (("events", 0, "outcomes", 0, "label"), "bad/label"),
        (("events", 0, "adaptive"), True),
        (("events", 0, "support"), [True]),
        (("events", 0, "support"), [0, 0]),
        (("events", 0, "support"), [1]),
        (("events", 0, "outcomes"), []),
        (("events", 0, "outcomes", 0, "kraus"), []),
        (("events", 0, "outcomes", 0, "kraus", 0), I[:1]),
        (("events", 0, "outcomes", 0, "kraus", 0, 0, 0), ["1"]),
        (("events", 0, "outcomes", 0, "label"), "1"),
        (("precedence",), [["Z", "absent"]]),
        (("precedence",), [["Z", "Z"]]),
    ],
)
def test_strict_wire_schema_rejects_invalid_structure_in_both_paths(path, value):
    wire = mutate(problem([z_event()]), path, value)
    with pytest.raises(ValueError):
        exact.parse_problem(wire)
    with pytest.raises(ValueError):
        reference.reference_schedule(wire, ("Z",))


@pytest.mark.parametrize(
    "token",
    [
        1,
        True,
        1.0,
        "",
        "01",
        "+1",
        "-0",
        "1/1",
        "2/2",
        "1/0",
        "NaN",
        "Infinity",
        "1e999999999",
        "1e-999999999",
        "1.0",
        " 1",
        str(2**64),
        "1/" + str(2**64),
        "1" * 257,
    ],
)
def test_bounded_rational_grammar_rejects_before_unbounded_expansion(token):
    wire = mutate(problem([z_event()]), ("events", 0, "outcomes", 0, "kraus", 0, 0, 0, 0), token)
    with pytest.raises(ValueError):
        exact.parse_problem(wire)
    with pytest.raises(ValueError):
        reference.reference_schedule(wire, ("Z",))


@pytest.mark.parametrize(
    "bad",
    [
        problem([event("incomplete", (("0", [P0]),))]),
        problem([z_event(), z_event()]),
        problem([z_event(), event("other", (("done", [I]),), record="r_Z")]),
        problem([z_event(), x_event()], (("Z", "X"), ("X", "Z"))),
        problem([z_event(), x_event()], (("Z", "X"), ("Z", "X"))),
        problem([event(name, (("done", [I]),)) for name in "ABCDE"]),
        problem([event("too_many", (("a", [P0]), ("b", [P1]), ("c", [ZERO])))]),
        problem([event("too_many", (("done", [I, ZERO, ZERO]),))]),
    ],
    ids=[
        "incomplete",
        "duplicate-event",
        "shared-record",
        "cycle",
        "duplicate-edge",
        "five-events",
        "three-outcomes",
        "three-Kraus",
    ],
)
def test_global_contract_rejections(bad):
    with pytest.raises(ValueError):
        exact.parse_problem(bad)
    order = tuple(item["event_id"] for item in bad["events"])
    with pytest.raises(ValueError):
        reference.reference_schedule(bad, order)


@pytest.mark.parametrize("order", [(), ("Z", "Z"), ("unknown",), ["Z"]])
def test_invalid_full_schedule_rejected_in_both_paths(order):
    wire = problem([z_event()])
    parsed = exact.parse_problem(wire)
    with pytest.raises(ValueError):
        exact.execute_operator(parsed, order, exact.identity(2))
    with pytest.raises(ValueError):
        reference.reference_schedule(wire, order)


def test_scalar_arithmetic_types_and_growth_bounds():
    for value in (True, 0.5, complex(1, 0), "1"):
        with pytest.raises(TypeError):
            exact.q(value)
    with pytest.raises(TypeError):
        exact.C(1, Fraction(0))
    with pytest.raises(ValueError):
        exact.q(Fraction(1 << 4096))


def test_safety_rejections_remain_active_in_optimized_python():
    # The child deliberately uses no asserts: -O must not remove safety checks.
    script = """
import json, sys
sys.path.insert(0, sys.argv[1])
import exact, reference
wire = json.loads(sys.argv[2])
checks = (lambda: exact.parse_problem(wire),
          lambda: reference.reference_schedule(wire, ('incomplete',)))
for check in checks:
    try:
        check()
    except ValueError:
        continue
    raise SystemExit('invalid instrument accepted with optimization')
print('both explicit validation paths reject under -O')
"""
    wire = problem([event("incomplete", (("0", [P0]),))])
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-B",
            "-c",
            script,
            str(Path(__file__).parent),
            json.dumps(wire),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert completed.stdout.strip() == "both explicit validation paths reject under -O"


class MemoryResult:
    """Result-path test double: artifact tests never create a real result file."""

    def __init__(self, raw):
        self.raw = raw

    def exists(self):
        return True

    def is_file(self):
        return True

    def is_symlink(self):
        return False

    def read_bytes(self):
        return self.raw

    def open(self, *args, **kwargs):
        raise AssertionError("artifact test attempted a result write")


def artifact_harness(monkeypatch, *, verify=True):
    # Importing the runner is confined to these artifact-boundary tests; none of
    # the independent quantum fixtures or expected values comes from its suite.
    import study

    ledger = {"protocol.py": {"bytes": 1, "sha256": "test-identity"}}
    suite = {"totals": {"tiny_fake_cases": 1}, "exact_value": ["1/2", "0"]}
    result = MemoryResult(
        study.canonical(
            {
                "schema_version": "det8-qr01-results-v1",
                "source_ledger": ledger,
                "suite": suite,
            }
        )
    )
    monkeypatch.setattr(study, "RESULT", result)
    monkeypatch.setattr(study, "source_ledger", lambda: deepcopy(ledger))
    monkeypatch.setattr(study, "run_suite", lambda: deepcopy(suite))
    # Replace only the runner's sys binding, not process-wide sys.flags.
    monkeypatch.setattr(
        study,
        "sys",
        SimpleNamespace(
            flags=SimpleNamespace(isolated=1, optimize=0),
            pycache_prefix="/tmp/det8-qr01-test-cache-never-created",
        ),
    )
    # argparse reads the actual process argv, which monkeypatch restores.
    monkeypatch.setattr(sys, "argv", ["study.py", *(["--verify"] if verify else [])])
    return study, result, ledger, suite


def test_artifact_replay_rejects_concurrent_result_byte_replacement(monkeypatch):
    study, result, _, suite = artifact_harness(monkeypatch)

    def replace_during_run():
        result.raw += b" "  # Same JSON meaning, different retained artifact bytes.
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", replace_during_run)
    with pytest.raises(ValueError, match="result changed during replay"):
        study.main()


def test_artifact_replay_rejects_source_ledger_drift(monkeypatch):
    study, _, ledger, suite = artifact_harness(monkeypatch)

    def change_source_during_run():
        ledger["protocol.py"]["sha256"] = "changed-source"
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", change_source_during_run)
    with pytest.raises(ValueError, match="source changed during execution"):
        study.main()


def test_artifact_replay_rejects_suite_mismatch(monkeypatch):
    study, _, _, suite = artifact_harness(monkeypatch)
    changed = deepcopy(suite)
    changed["exact_value"] = ["2/3", "0"]
    monkeypatch.setattr(study, "run_suite", lambda: changed)
    with pytest.raises(ValueError, match="exact replay differs"):
        study.main()


def test_artifact_capture_is_create_only_before_any_computation(monkeypatch):
    study, _, _, _ = artifact_harness(monkeypatch, verify=False)

    def forbidden_work():
        raise AssertionError("existing result should be refused before any work")

    monkeypatch.setattr(study, "run_suite", forbidden_work)
    monkeypatch.setattr(study, "source_ledger", forbidden_work)
    with pytest.raises(FileExistsError, match="results.json already exists"):
        study.main()


def test_artifact_replay_reports_hash_of_exact_verified_bytes(monkeypatch, capsys):
    study, result, _, suite = artifact_harness(monkeypatch)
    initial = result.raw
    study.main()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "VERIFIED_EXACT_REPLAY"
    assert report["result_sha256"] == study.digest(initial)
    assert report["totals"] == suite["totals"]
    assert result.raw == initial
