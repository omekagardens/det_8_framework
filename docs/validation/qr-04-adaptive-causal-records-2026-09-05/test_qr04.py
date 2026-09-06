"""Independent exact fixtures for adaptive causal-record access and composition."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import product
from pathlib import Path
from types import SimpleNamespace

import adaptive
import pytest
import reference_qr04

H = Fraction(1, 2)


def matrix(rows):
    result = []
    for row in rows:
        cells = []
        for value in row:
            real, imag = value if type(value) is tuple else (value, 0)
            cells.append([str(Fraction(real)), str(Fraction(imag))])
        result.append(cells)
    return result


I = matrix(((1, 0), (0, 1)))
X = matrix(((0, 1), (1, 0)))
S = matrix(((1, 0), (0, (0, 1))))
P0 = matrix(((1, 0), (0, 0)))
P1 = matrix(((0, 0), (0, 1)))
ZERO = matrix(((0, 0), (0, 0)))
PX = (matrix(((H, H), (H, H))), matrix(((H, -H), (-H, H))))
PY = (matrix(((H, (0, -H)), ((0, H), H))), matrix(((H, (0, H)), ((0, -H), H))))


def identity(dimension):
    return matrix([[int(row == column) for column in range(dimension)] for row in range(dimension)])


def weight(operator, amplitude):
    return [
        [[str(Fraction(real) * amplitude), str(Fraction(imag) * amplitude)] for real, imag in row]
        for row in operator
    ]


def embed(operator, qubit):
    output = []
    for row in range(4):
        entries = []
        for column in range(4):
            r, c = (row // 2, row % 2), (column // 2, column % 2)
            entries.append(
                deepcopy(operator[r[qubit]][c[qubit]])
                if r[1 - qubit] == c[1 - qubit]
                else ["0", "0"]
            )
        output.append(entries)
    return output


def outcomes(items):
    return [{"label": label, "kraus": deepcopy(kraus)} for label, kraus in items]


def unitary(operator=I):
    return outcomes((("done", [operator]),))


def measurement(operators=(P0, P1), labels=("0", "1")):
    return outcomes(
        tuple((label, [operator]) for label, operator in zip(labels, operators, strict=True))
    )


def policy(reads, choose, labels=None):
    domains = [labels[rid] if labels is not None else ("0", "1") for rid in reads]
    return [
        {
            "when": [[rid, value] for rid, value in zip(reads, assignment, strict=True)],
            "setting": choose(dict(zip(reads, assignment, strict=True))),
        }
        for assignment in product(*domains)
    ]


def event(name, settings=None, *, support=(0,), reads=(), available=None, table=None, record=None):
    settings = settings if settings is not None else {"identity": unitary()}
    if table is None:
        table = policy(reads, lambda record: next(iter(settings)))
    return {
        "event_id": name,
        "record_id": record or name,
        "support": list(support),
        "available_records": list(reads if available is None else available),
        "read_records": list(reads),
        "settings": [
            {"setting": name, "outcomes": deepcopy(value)} for name, value in settings.items()
        ],
        "policy": deepcopy(table),
    }


def wire(events=None, edges=(), qubits=1):
    return {
        "schema_version": "det8-qr04-problem-v1",
        "qubits": qubits,
        "events": deepcopy(events if events is not None else [event("E")]),
        "precedence": [list(edge) for edge in edges],
    }


def reset_wire():
    past = event("D", {"Z": measurement()})
    future = event(
        "A",
        {"identity": unitary(), "flip": unitary(X)},
        reads=("D",),
        table=policy(("D",), lambda r: "identity" if r["D"] == "0" else "flip"),
    )
    return wire([past, future], (("D", "A"),))


def conflict_wire(*, impossible=False):
    source_outcomes = (
        outcomes((("0", [I]), ("1", [ZERO])))
        if impossible
        else outcomes(
            (
                ("0", [weight(I, Fraction(3, 5))]),
                ("1", [weight(I, Fraction(4, 5))]),
            )
        )
    )
    past = event("D", {"emit": source_outcomes}, support=())
    adaptive_a = event(
        "A",
        {"identity": unitary(), "phase": unitary(S)},
        reads=("D",),
        table=policy(("D",), lambda r: "identity" if r["D"] == "0" else "phase"),
    )
    independent_b = event("B", {"X": unitary(X)})
    return wire([past, adaptive_a, independent_b], (("D", "A"), ("D", "B")))


def restricted_range_wire():
    past = event("D", {"dephase": outcomes((("all", [P0, P1]),))})
    a, b = event("A", {"phase": unitary(S)}), event("B", {"X": unitary(X)})
    return wire([past, a, b], (("D", "A"), ("D", "B")))


def common_past_local_wire():
    past = event(
        "D",
        {
            "emit": outcomes(
                (
                    ("0", [weight(identity(4), Fraction(3, 5))]),
                    ("1", [weight(identity(4), Fraction(4, 5))]),
                )
            )
        },
        support=(),
    )
    children = []
    for name, qubit in (("A", 0), ("B", 1)):
        settings = {
            "X": measurement(tuple(embed(op, qubit) for op in PX), ("+", "-")),
            "Y": measurement(tuple(embed(op, qubit) for op in PY), ("+", "-")),
        }
        children.append(
            event(
                name,
                settings,
                support=(qubit,),
                reads=("D",),
                table=policy(("D",), lambda r: "X" if r["D"] == "0" else "Y"),
            )
        )
    return wire([past, *children], (("D", "A"), ("D", "B")), qubits=2)


def two_read_wire():
    coin = {
        "emit": outcomes((("0", [weight(I, Fraction(3, 5))]), ("1", [weight(I, Fraction(4, 5))])))
    }
    first, second = event("R0", coin, support=()), event("R1", coin, support=())
    relay = event("R2")
    target = event(
        "T",
        {"identity": unitary(), "flip": unitary(X)},
        available=("R0", "R1", "R2"),
        reads=("R0", "R1"),
        table=policy(("R0", "R1"), lambda r: "identity" if r["R0"] == r["R1"] else "flip"),
    )
    return wire([first, second, relay, target], (("R0", "R2"), ("R2", "T"), ("R1", "T")))


def record_key(record):
    return tuple(tuple(triple) for triple in record)


def first_difference(left_maps, right_maps):
    left = {record_key(item["record"]): item["superoperator"] for item in left_maps}
    right = {record_key(item["record"]): item["superoperator"] for item in right_maps}
    if set(left) != set(right):
        return {
            "kind": "record_inventory",
            "left": [[list(t) for t in r] for r in sorted(left)],
            "right": [[list(t) for t in r] for r in sorted(right)],
        }
    for record in sorted(left):
        for i, (left_row, right_row) in enumerate(zip(left[record], right[record], strict=True)):
            for j, (a, b) in enumerate(zip(left_row, right_row, strict=True)):
                if a != b:
                    delta = [str(Fraction(x) - Fraction(y)) for x, y in zip(a, b, strict=True)]
                    return {
                        "kind": "map_entry",
                        "record": [list(t) for t in record],
                        "output_index": i,
                        "input_index": j,
                        "left": a,
                        "right": b,
                        "delta": delta,
                    }
    return None


@pytest.mark.parametrize(
    "problem,schedule_equal,pair_equal",
    [
        (reset_wire(), True, True),
        (common_past_local_wire(), True, True),
        (two_read_wire(), True, True),
        (conflict_wire(), False, False),
        (conflict_wire(impossible=True), True, False),
        (restricted_range_wire(), True, False),
    ],
    ids=[
        "adaptive-reset",
        "common-past-local",
        "two-read-transitive",
        "real-conflict",
        "zero-context-hidden",
        "nonzero-range-hidden",
    ],
)
def test_complete_canonical_results_match_independent_reference(
    problem, schedule_equal, pair_equal
):
    actual = adaptive.analyze(problem)
    assert actual == reference_qr04.analyze(problem)
    assert actual["schedule_equal"] is schedule_equal
    assert actual["universal_pair_equal"] is pair_equal
    assert actual["nontrivial_schedule_comparison"] is (len(actual["schedules"]) > 1)


@pytest.mark.parametrize(
    "problem",
    [conflict_wire(), conflict_wire(impossible=True), restricted_range_wire(), two_read_wire()],
)
def test_stored_witnesses_and_work_counts_are_independently_consistent(problem):
    result = adaptive.analyze(problem)
    schedules = {tuple(row["order"]): row["maps"] for row in result["schedules"]}
    assert list(schedules) == sorted(schedules)
    assert len(result["schedule_comparisons"]) == len(schedules) - 1
    for comparison in result["schedule_comparisons"]:
        difference = first_difference(
            schedules[tuple(comparison["left"])], schedules[tuple(comparison["right"])]
        )
        assert comparison["difference"] == difference
        assert comparison["equal"] is (difference is None)
    pair_contexts = 0
    pair_maps = 0
    for pair in result["pairs"]:
        for context in pair["contexts"]:
            pair_contexts += 1
            pair_maps += len(context["forward"]) + len(context["reverse"])
            difference = first_difference(context["forward"], context["reverse"])
            assert context["difference"] == difference
            assert context["equal"] is (difference is None)
        assert pair["universal_equal"] is all(context["equal"] for context in pair["contexts"])
    counts = result["counts"]
    assert counts["schedules"] == len(schedules)
    assert counts["schedule_map_blocks"] == sum(len(value) for value in schedules.values())
    assert counts["incomparable_pairs"] == len(result["pairs"])
    assert counts["pair_contexts"] == pair_contexts
    assert counts["pair_map_blocks"] == pair_maps
    assert counts["matrix_unit_executions"] == (2 ** problem["qubits"]) ** 2 * (
        len(schedules) + 2 * pair_contexts
    )
    assert counts["zero_schedule_blocks"] == sum(
        all(cell == ["0", "0"] for row in block["superoperator"] for cell in row)
        for maps in schedules.values()
        for block in maps
    )


def test_adaptive_reset_retains_selected_setting_and_zero_branches():
    problem = adaptive.parse(reset_wire())
    results = adaptive.execute_operator(problem, ("D", "A"), adaptive.ex.decode_matrix(P1, 2))
    expected_records = {
        (("A", "identity", "done"), ("D", "Z", "0")),
        (("A", "flip", "done"), ("D", "Z", "1")),
    }
    assert set(results) == expected_records
    assert results[(("A", "flip", "done"), ("D", "Z", "1"))] == adaptive.ex.decode_matrix(P0, 2)
    assert results[(("A", "identity", "done"), ("D", "Z", "0"))] == adaptive.ex.zeros(2)
    analysis = adaptive.analyze(reset_wire())
    assert analysis["adaptive_events"] == ["A"]
    assert not analysis["nontrivial_schedule_comparison"]
    assert analysis["pairs"] == []


def test_setting_labels_cannot_be_erased_even_for_identical_quantum_maps():
    first = wire(
        [
            event(
                "E",
                {"alpha": unitary(), "beta": unitary()},
                table=[{"when": [], "setting": "alpha"}],
            )
        ]
    )
    second = deepcopy(first)
    second["events"][0]["policy"][0]["setting"] = "beta"
    operator = adaptive.ex.decode_matrix(PX[0], 2)
    left = adaptive.execute_operator(adaptive.parse(first), ("E",), operator)
    right = adaptive.execute_operator(adaptive.parse(second), ("E",), operator)
    assert set(left) == {(("E", "alpha", "done"),)}
    assert set(right) == {(("E", "beta", "done"),)}
    assert list(left.values()) == list(right.values())
    assert left != right
    assert adaptive.analyze(first)["adaptive_events"] == []


def test_real_noncommutation_has_a_physical_complex_state_witness():
    parsed = adaptive.parse(conflict_wire())
    plus = adaptive.ex.decode_matrix(PX[0], 2)
    left = adaptive.execute_operator(parsed, ("D", "A", "B"), plus)
    right = adaptive.execute_operator(parsed, ("D", "B", "A"), plus)
    key = (("A", "phase", "done"), ("B", "X", "done"), ("D", "emit", "1"))
    assert left[key] == adaptive.ex.decode_matrix(weight(PY[1], Fraction(16, 25)), 2)
    assert right[key] == adaptive.ex.decode_matrix(weight(PY[0], Fraction(16, 25)), 2)
    assert (
        adaptive.ex.trace(left[key])
        == adaptive.ex.trace(right[key])
        == adaptive.ex.q(Fraction(16, 25))
    )


def test_impossible_context_is_retained_in_the_universal_certificate():
    result = adaptive.analyze(conflict_wire(impossible=True))
    assert result["schedule_equal"] and not result["universal_pair_equal"]
    assert result["adaptive_events"] == ["A"]
    pair = result["pairs"][0]
    assert pair["events"] == ["A", "B"]
    assert [context["read_context"] for context in pair["contexts"]] == [[["D", "0"]], [["D", "1"]]]
    assert [context["equal"] for context in pair["contexts"]] == [True, False]
    assert result["counts"]["zero_schedule_blocks"] == 2
    for context in pair["contexts"]:
        # Context is metadata, not a newly written past record in the pair maps.
        assert all(
            {triple[0] for triple in row["record"]} == {"A", "B"} for row in context["forward"]
        )


def test_nonzero_reachable_subspace_can_hide_universal_noncommutation():
    result = adaptive.analyze(restricted_range_wire())
    assert result["schedule_equal"] and not result["universal_pair_equal"]
    assert result["counts"]["zero_schedule_blocks"] == 0
    assert result["pairs"][0]["contexts"][0]["read_context"] == []
    assert result["adaptive_events"] == []
    # Dephasing loses only off-diagonal components, not every input's trace.
    parsed = adaptive.parse(restricted_range_wire())
    for physical in (P0, P1, PX[0], PY[0]):
        operator = adaptive.ex.decode_matrix(physical, 2)
        assert adaptive.execute_operator(
            parsed, ("D", "A", "B"), operator
        ) == adaptive.execute_operator(parsed, ("D", "B", "A"), operator)


def test_two_read_policy_uses_transitive_ancestors_and_has_every_context():
    problem = two_read_wire()
    assert ["R0", "T"] not in problem["precedence"]
    result = adaptive.analyze(problem)
    assert result["adaptive_events"] == ["T"]
    assert len(problem["events"][-1]["policy"]) == 4
    assert len(result["schedules"]) == 3
    for schedule in result["schedules"]:
        for block in schedule["maps"]:
            records = {rid: (setting, outcome) for rid, setting, outcome in block["record"]}
            expected = "identity" if records["R0"][1] == records["R1"][1] else "flip"
            assert records["T"] == (expected, "done")


def test_instruments_and_table_order_are_not_semantic():
    original = common_past_local_wire()
    changed = deepcopy(original)
    changed["events"].reverse()
    changed["precedence"].reverse()
    for item in changed["events"]:
        item["settings"].reverse()
        item["policy"].reverse()
        for setting in item["settings"]:
            setting["outcomes"].reverse()
    assert adaptive.analyze(original) == adaptive.analyze(changed)
    assert reference_qr04.analyze(original) == reference_qr04.analyze(changed)


def test_shared_selector_preserves_joint_context_correlation():
    coin = {
        "emit": outcomes((("0", [weight(I, Fraction(3, 5))]), ("1", [weight(I, Fraction(4, 5))])))
    }
    axes = {"X": measurement(PX, ("+", "-")), "Y": measurement(PY, ("+", "-"))}
    parent_d = event("D", coin, support=())
    a = event(
        "A", axes, reads=("D",), table=policy(("D",), lambda r: "X" if r["D"] == "0" else "Y")
    )
    shared_b = event(
        "B", axes, reads=("D",), table=policy(("D",), lambda r: "X" if r["D"] == "0" else "Y")
    )
    shared = wire([parent_d, a, shared_b], (("D", "A"), ("D", "B")))
    shared_result = adaptive.analyze(shared)
    assert shared_result == reference_qr04.analyze(shared)
    assert shared_result["universal_pair_equal"]
    assert len(shared_result["pairs"][0]["contexts"]) == 2
    assert [row["selected_settings"] for row in shared_result["pairs"][0]["contexts"]] == [
        [["A", "X"], ["B", "X"]],
        [["A", "Y"], ["B", "Y"]],
    ]

    parent_e = event("E", coin, support=())
    independent_b = event(
        "B", axes, reads=("E",), table=policy(("E",), lambda r: "X" if r["E"] == "0" else "Y")
    )
    independent = wire([parent_d, parent_e, a, independent_b], (("D", "A"), ("E", "B")))
    independent_result = adaptive.analyze(independent)
    assert independent_result == reference_qr04.analyze(independent)
    pair = next(row for row in independent_result["pairs"] if row["events"] == ["A", "B"])
    assert [row["equal"] for row in pair["contexts"]] == [True, False, False, True]
    assert not independent_result["schedule_equal"]
    assert not independent_result["universal_pair_equal"]


def mutate(problem, path, value):
    copied = deepcopy(problem)
    target = copied
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = deepcopy(value)
    return copied


def rejects(problem):
    with pytest.raises(ValueError):
        adaptive.parse(problem)
    with pytest.raises(ValueError):
        reference_qr04.analyze(problem)


@pytest.mark.parametrize(
    "change",
    [
        "unavailable-ancestor",
        "incomparable-even-if-earlier",
        "self",
        "future",
        "unknown",
        "unreachable-forbidden",
    ],
)
def test_record_access_is_permission_and_ancestry_not_scheduler_position(change):
    if change == "unavailable-ancestor":
        bad = reset_wire()
        bad["events"][1]["available_records"] = []
    elif change == "incomparable-even-if-earlier":
        bad = reset_wire()
        bad["precedence"] = []  # A D-first schedule cannot confer read permission.
    elif change == "unreachable-forbidden":
        bad = conflict_wire(impossible=True)
        bad["events"][1]["available_records"] = ["B", "D"]
        bad["events"][1]["read_records"] = ["B", "D"]
    else:
        bad = reset_wire()
        target = bad["events"][1]
        forbidden = "A" if change == "self" else ("future" if change == "unknown" else "F")
        if change == "future":
            bad["events"].append(event("F"))
            bad["precedence"].append(["A", "F"])
        target["available_records"] = [forbidden]
        target["read_records"] = [forbidden]
        target["policy"] = policy((forbidden,), lambda r: "identity")
    rejects(bad)


@pytest.mark.parametrize(
    "change",
    [
        "missing-unreachable",
        "duplicate",
        "extra-read",
        "wrong-outcome",
        "unknown-setting",
        "wildcard",
        "fallback",
        "noncanonical",
        "setting-read",
        "scheduler-read",
    ],
)
def test_policy_tables_are_total_explicit_and_have_no_hidden_inputs(change):
    bad = conflict_wire(impossible=True)
    target = bad["events"][1]
    if change == "missing-unreachable":
        target["policy"] = target["policy"][:1]
    elif change == "duplicate":
        target["policy"][1] = deepcopy(target["policy"][0])
    elif change == "extra-read":
        target["policy"][0]["when"].append(["B", "done"])
    elif change == "wrong-outcome":
        target["policy"][1]["when"][0][1] = "unknown"
    elif change == "unknown-setting":
        target["policy"][1]["setting"] = "missing"
    elif change == "wildcard":
        target["policy"][1]["when"][0][1] = "*"
    elif change == "fallback":
        target["fallback"] = "identity"
    elif change == "noncanonical":
        bad = two_read_wire()
        bad["events"][-1]["policy"][0]["when"].reverse()
    elif change == "setting-read":
        target["policy"][0]["when"] = [["D", "emit", "0"]]
    else:
        target["scheduler_index"] = 0
    rejects(bad)


def test_unused_setting_is_still_checked_for_completeness():
    bad = wire(
        [
            event(
                "E",
                {"good": unitary(), "unused": outcomes((("done", [P0]),))},
                table=[{"when": [], "setting": "good"}],
            )
        ]
    )
    rejects(bad)


def test_unused_setting_must_have_the_same_outcome_inventory():
    bad = wire(
        [
            event(
                "E",
                {"good": unitary(), "unused": measurement(PX, ("+", "-"))},
                table=[{"when": [], "setting": "good"}],
            )
        ]
    )
    rejects(bad)


def test_same_label_inventory_does_not_mean_different_settings_have_same_maps():
    valid = reset_wire()
    assert adaptive.analyze(valid)["adaptive_events"] == ["A"]
    altered = deepcopy(valid)
    altered["events"][1]["settings"][1]["outcomes"][0]["label"] = "different"
    rejects(altered)


def test_hidden_nonlocal_support_in_an_unused_setting_is_rejected():
    valid = common_past_local_wire()
    target = valid["events"][1]
    cnot = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
    target["settings"][1]["outcomes"] = outcomes(
        (("+", [weight(cnot, Fraction(3, 5))]), ("-", [weight(cnot, Fraction(4, 5))]))
    )
    for row in target["policy"]:
        row["setting"] = "X"  # The bad Y setting is now unused, but must fail.
    rejects(valid)


@pytest.mark.parametrize(
    "path,value",
    [
        (("schema_version",), "unknown"),
        (("unknown",), True),
        (("qubits",), True),
        (("qubits",), 0),
        (("qubits",), 3),
        (("events",), []),
        (("events", 0, "event_id"), "bad event"),
        (("events", 0, "record_id"), "bad/record"),
        (("events", 0, "support"), [True]),
        (("events", 0, "support"), [0, 0]),
        (("events", 0, "settings"), []),
        (("events", 0, "policy"), []),
        (("events", 0, "available_records"), ["missing"]),
        (("events", 0, "read_records"), ["missing"]),
        (("events", 0, "callback"), True),
        (("events", 0, "policy", 0, "when"), "hidden"),
        (("events", 0, "settings", 0, "setting"), "bad setting"),
        (("events", 0, "settings", 0, "outcomes", 0, "kraus"), []),
        (("precedence",), [["E", "E"]]),
        (("precedence",), [["E", "missing"]]),
    ],
)
def test_strict_wire_schema_rejects_invalids(path, value):
    rejects(mutate(wire(), path, value))


@pytest.mark.parametrize(
    "token", [True, 0.5, "01", "1/1", "NaN", "1e999999999", "1e-999999999", str(2**64), "1" * 257]
)
def test_bounded_rational_grammar_is_reused_before_conversion(token):
    bad = mutate(wire(), ("events", 0, "settings", 0, "outcomes", 0, "kraus", 0, 0, 0, 0), token)
    rejects(bad)


@pytest.mark.parametrize(
    "change",
    [
        "cycle",
        "duplicate-edge",
        "duplicate-event",
        "duplicate-record",
        "duplicate-setting",
        "duplicate-outcome",
        "five-events",
        "three-settings",
        "three-reads",
        "duplicate-available",
    ],
)
def test_global_scope_and_uniqueness_rejections(change):
    bad = two_read_wire()
    if change == "cycle":
        bad["precedence"].append(["T", "R0"])
    elif change == "duplicate-edge":
        bad["precedence"].append(deepcopy(bad["precedence"][0]))
    elif change == "duplicate-event":
        bad["events"][1]["event_id"] = "R0"
    elif change == "duplicate-record":
        bad["events"][1]["record_id"] = "R0"
    elif change == "duplicate-setting":
        bad["events"][-1]["settings"][1]["setting"] = "identity"
    elif change == "duplicate-outcome":
        bad["events"][0]["settings"][0]["outcomes"][1]["label"] = "0"
    elif change == "five-events":
        bad["events"].append(event("extra"))
    elif change == "three-settings":
        bad["events"][-1]["settings"].append({"setting": "third", "outcomes": unitary()})
    elif change == "three-reads":
        bad["events"][-1]["read_records"] = ["R0", "R1", "R2"]
    else:
        bad["events"][-1]["available_records"] = ["R0", "R0", "R1"]
    rejects(bad)


@pytest.mark.parametrize("order", [(), ("A", "D"), ("D", "D"), ["D", "A"]])
def test_executor_refuses_invalid_full_schedules(order):
    with pytest.raises(ValueError):
        adaptive.execute_operator(adaptive.parse(reset_wire()), order, adaptive.ex.identity(2))


def test_reused_qr01_sources_are_the_frozen_bytes():
    prior = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05"
    expected = {
        "exact.py": "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56",
        "reference.py": "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f",
    }
    assert Path(adaptive.ex.__file__).resolve() == (prior / "exact.py").resolve()
    for name, expected_hash in expected.items():
        assert hashlib.sha256((prior / name).read_bytes()).hexdigest() == expected_hash


@pytest.mark.parametrize("implementation", ["executor", "reference"])
def test_pinned_source_loader_rejects_changed_bytes_without_execution(monkeypatch, implementation):
    fake = SimpleNamespace(
        is_file=lambda: True,
        is_symlink=lambda: False,
        read_bytes=lambda: b"raise RuntimeError('must not execute')",
    )
    if implementation == "executor":
        monkeypatch.setattr(adaptive, "BASE_PATH", fake)
        load, message = adaptive._load_exact, "source identity differs"
    else:
        monkeypatch.setattr(reference_qr04, "QR01_REFERENCE_PATH", fake)
        load, message = reference_qr04._load_qr01_reference, "reference SHA changed"
    with pytest.raises(ValueError, match=message):
        load()


@pytest.mark.parametrize("implementation", ["executor", "reference"])
def test_pinned_module_collision_cannot_be_hidden_by_a_spoofed_path(monkeypatch, implementation):
    if implementation == "executor":
        name, path, load = "qr04_pinned_exact", adaptive.BASE_PATH, adaptive._load_exact
    else:
        name, path, load = (
            "qr04_pinned_reference_qr01",
            reference_qr04.QR01_REFERENCE_PATH,
            reference_qr04._load_qr01_reference,
        )
    monkeypatch.setitem(sys.modules, name, SimpleNamespace(__file__=str(path)))
    with pytest.raises(ValueError, match="module name collision"):
        load()


def test_validation_is_explicit_under_optimized_python():
    bad = conflict_wire(impossible=True)
    bad["events"][1]["policy"] = bad["events"][1]["policy"][:1]
    script = """
import json, sys
sys.path.insert(0, sys.argv[1])
import adaptive, reference_qr04
wire = json.loads(sys.argv[2])
for check in (lambda: adaptive.parse(wire), lambda: reference_qr04.analyze(wire)):
    try:
        check()
    except ValueError:
        continue
    raise SystemExit('missing impossible-context policy accepted under -O')
print('both QR-04 paths explicitly reject under -O')
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-O",
            "-B",
            "-c",
            script,
            str(Path(__file__).parent),
            json.dumps(bad),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert result.stdout.strip() == "both QR-04 paths explicitly reject under -O"


class MemoryResult:
    """Fake artifact path; no publication or retained-result writes in tests."""

    def __init__(self, raw):
        self.raw = raw
        self.present = True
        self.symlink = False

    def exists(self):
        return self.present

    def is_file(self):
        return self.present and not self.symlink

    def is_symlink(self):
        return self.symlink

    def read_bytes(self):
        return self.raw

    def open(self, *args, **kwargs):
        raise AssertionError("artifact test attempted a real result write")


def artifact_harness(monkeypatch, *, verify=True):
    name = "qr04_artifact_test_study"
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("study.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the specific QR-04 artifact runner")
    study = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, study)
    spec.loader.exec_module(study)
    ledger = {"source": {"bytes": 1, "sha256": "source-identity"}}
    priors = {
        name: {"bytes": i, "sha256": f"{name}-identity"}
        for i, name in enumerate(("qr01", "qr02", "qr03"), 2)
    }
    suite = {"totals": {"tiny_fake_cases": 1}, "exact_entry": ["1/2", "0"]}
    result = MemoryResult(
        study.canonical(
            {
                "schema_version": "det8-qr04-results-v1",
                "source_ledger": ledger,
                "prior_artifacts": priors,
                "suite": suite,
            }
        )
    )
    monkeypatch.setattr(study, "RESULT", result)
    monkeypatch.setattr(study, "source_ledger", lambda: deepcopy(ledger))
    monkeypatch.setattr(study, "prior_identity", lambda: deepcopy(priors))
    monkeypatch.setattr(study, "run_suite", lambda: deepcopy(suite))
    monkeypatch.setattr(
        study,
        "sys",
        SimpleNamespace(
            flags=SimpleNamespace(isolated=1, optimize=0),
            pycache_prefix="/tmp/det8-qr04-test-cache-never-created",
        ),
    )
    monkeypatch.setattr(sys, "argv", ["study.py", *(["--verify"] if verify else [])])
    return study, result, ledger, priors, suite


def test_artifact_replay_rejects_concurrent_byte_replacement(monkeypatch):
    study, result, _, _, suite = artifact_harness(monkeypatch)

    def replace_during_run():
        result.raw += b" "
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", replace_during_run)
    with pytest.raises(ValueError, match="result changed during replay"):
        study.main()


@pytest.mark.parametrize("identity", ["source", "qr01", "qr02", "qr03"])
def test_artifact_replay_rejects_source_or_each_prior_drift(monkeypatch, identity):
    study, _, ledger, priors, suite = artifact_harness(monkeypatch)

    def change_during_run():
        if identity == "source":
            ledger["source"]["sha256"] = "changed-source"
        else:
            priors[identity]["sha256"] = "changed-prior"
        return deepcopy(suite)

    monkeypatch.setattr(study, "run_suite", change_during_run)
    with pytest.raises(ValueError, match="source/prior changed during execution"):
        study.main()


def test_artifact_replay_rejects_map_or_suite_mismatch(monkeypatch):
    study, _, _, _, suite = artifact_harness(monkeypatch)
    changed = deepcopy(suite)
    changed["exact_entry"] = ["2/3", "0"]
    monkeypatch.setattr(study, "run_suite", lambda: changed)
    with pytest.raises(ValueError, match="exact replay differs"):
        study.main()


@pytest.mark.parametrize("dangling_symlink", [False, True])
def test_artifact_capture_refuses_existing_path_before_computation(monkeypatch, dangling_symlink):
    study, result, _, _, _ = artifact_harness(monkeypatch, verify=False)
    if dangling_symlink:
        result.present = False
        result.symlink = True

    def forbidden_work():
        raise AssertionError("existing result path must be refused before work")

    monkeypatch.setattr(study, "source_ledger", forbidden_work)
    monkeypatch.setattr(study, "prior_identity", forbidden_work)
    monkeypatch.setattr(study, "run_suite", forbidden_work)
    with pytest.raises(FileExistsError, match="results.json already exists"):
        study.main()


def test_artifact_replay_hashes_the_exact_verified_bytes(monkeypatch, capsys):
    study, result, _, _, suite = artifact_harness(monkeypatch)
    original = result.raw
    study.main()
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "VERIFIED_EXACT_REPLAY"
    assert report["result_sha256"] == study.digest(original)
    assert report["totals"] == suite["totals"]
    assert result.raw == original
