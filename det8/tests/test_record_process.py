"""Contracts for separate residual activity, commit, and passive record access.

The exact phase example is a conditional finite-QM arithmetic witness, not a
quantum reconstruction, autonomous DET growth law, or physical first-record
mechanism. The classical example deliberately demonstrates that silent
activity by itself is not a quantum-selection principle.
"""

from __future__ import annotations

import math
import unittest
from dataclasses import FrozenInstanceError
from fractions import Fraction

from det8.models.record_process import (
    AccessibleRecord,
    CommittedRecord,
    CommittedSnapshot,
    ProcessState,
    RecordView,
    ResidualState,
    access_records,
    commit_record,
    evolve_residual,
)


def chain_state() -> ProcessState:
    """Use nonconsecutive IDs: names do not serve as a physical clock."""
    records = (
        CommittedRecord(10, frozenset(), label="source"),
        CommittedRecord(-4, frozenset({10}), label="middle"),
        CommittedRecord(30, frozenset({10, -4}), label="last"),
    )
    return ProcessState(CommittedSnapshot(records), ResidualState("bit", 0))


class CommittedHistoryTests(unittest.TestCase):
    def test_empty_snapshot_has_zero_record_count(self) -> None:
        self.assertEqual(CommittedSnapshot().count, 0)
        self.assertEqual(CommittedSnapshot().records, ())

    def test_full_past_relation_is_transitive_not_numeric_id_order(self) -> None:
        snapshot = chain_state().committed
        self.assertEqual(snapshot.count, 3)
        self.assertTrue(snapshot.precedes(10, -4))
        self.assertTrue(snapshot.precedes(-4, 30))
        self.assertTrue(snapshot.precedes(10, 30))
        self.assertFalse(snapshot.precedes(30, 10))
        self.assertFalse(snapshot.precedes(10, 10))
        with self.assertRaises(KeyError):
            snapshot.precedes(10, 999)

    def test_integer_event_ids_are_strict_and_not_boolean(self) -> None:
        for invalid in (True, 1.0, "1", None):
            with self.subTest(invalid=invalid), self.assertRaises(TypeError):
                CommittedRecord(invalid, frozenset())
            with self.subTest(past=invalid), self.assertRaises(TypeError):
                CommittedRecord(2, frozenset({invalid}))

    def test_mutable_record_payloads_and_containers_are_rejected(self) -> None:
        for invalid in ([1], {"x": 1}, {1}, ([],)):
            with self.subTest(invalid=invalid), self.assertRaises(TypeError):
                CommittedRecord(1, frozenset(), payload=invalid)
        with self.assertRaises(TypeError):
            CommittedRecord(1, set())
        with self.assertRaises(TypeError):
            CommittedSnapshot([])

    def test_records_snapshots_and_residuals_are_frozen(self) -> None:
        state = chain_state()
        for obj, field, value in (
            (state.committed.records[0], "label", "rewritten"),
            (state.committed, "records", ()),
            (state.residual, "value", 1),
            (state, "committed", CommittedSnapshot()),
        ):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)

    def test_unknown_or_future_predecessors_are_rejected(self) -> None:
        first = CommittedRecord(1, frozenset({2}))
        second = CommittedRecord(2, frozenset())
        with self.assertRaises((KeyError, ValueError)):
            CommittedSnapshot((first,))
        with self.assertRaises((KeyError, ValueError)):
            CommittedSnapshot((first, second))

    def test_cycle_and_self_predecessor_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            CommittedRecord(1, frozenset({1}))
        with self.assertRaises((KeyError, ValueError)):
            CommittedSnapshot(
                (
                    CommittedRecord(1, frozenset({2})),
                    CommittedRecord(2, frozenset({1})),
                )
            )

    def test_duplicate_events_are_rejected(self) -> None:
        first = CommittedRecord(1, frozenset())
        with self.assertRaises(ValueError):
            CommittedSnapshot((first, first))

    def test_commit_past_must_be_downward_closed(self) -> None:
        first = CommittedRecord(1, frozenset())
        second = CommittedRecord(2, frozenset({1}))
        missing_ancestor = CommittedRecord(3, frozenset({2}))
        with self.assertRaises(ValueError):
            CommittedSnapshot((first, second, missing_ancestor))

    def test_record_kind_label_and_receipt_reference_are_checked(self) -> None:
        for kwargs in ({"kind": "silent"}, {"kind": 1}, {"label": []}):
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                CommittedRecord(1, frozenset(), **kwargs)
        with self.assertRaises(ValueError):
            CommittedRecord(1, frozenset(), source_event_id=0)
        with self.assertRaises((TypeError, ValueError)):
            CommittedRecord(1, frozenset(), kind="receipt")
        with self.assertRaises(ValueError):
            CommittedRecord(1, frozenset(), kind="receipt", source_event_id=0)


class ResidualActivityTests(unittest.TestCase):
    def test_residual_types_and_nested_values_are_validated(self) -> None:
        for type_id in ("", "  ", None, 1):
            with self.subTest(type_id=type_id), self.assertRaises((TypeError, ValueError)):
                ResidualState(type_id, 0)
        for value in ([0], {"bit": 0}, ([0],), math.nan, complex(math.inf, 0)):
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                ResidualState("bit", value)
        self.assertEqual(ResidualState("exact", (Fraction(1, 3), 1j)).type_id, "exact")

    def test_silent_activity_preserves_exact_committed_object_and_count(self) -> None:
        before = chain_state()
        after = evolve_residual(before, lambda z: ResidualState(z.type_id, 1 - z.value))
        self.assertIs(after.committed, before.committed)
        self.assertEqual(after.committed.count, before.committed.count)
        self.assertEqual(before.residual.value, 0)
        self.assertEqual(after.residual.value, 1)

    def test_finite_silent_composition_does_not_create_order_or_ticks(self) -> None:
        before = chain_state()
        flip = lambda z: ResidualState(z.type_id, 1 - z.value)
        after = evolve_residual(evolve_residual(before, flip), flip)
        self.assertIs(after.committed, before.committed)
        self.assertEqual(after, before)

    def test_silent_operation_cannot_change_declared_system_type(self) -> None:
        before = chain_state()
        with self.assertRaises(ValueError):
            evolve_residual(before, lambda z: ResidualState("different-type", z.value))
        self.assertEqual(before.residual.type_id, "bit")

    def test_silent_operation_must_return_a_residual_state(self) -> None:
        before = chain_state()
        with self.assertRaises(TypeError):
            evolve_residual(before, lambda z: z.value)
        with self.assertRaises(TypeError):
            ProcessState(before.residual, before.committed)

    def test_classical_silent_bit_changes_later_readout_without_new_record(self) -> None:
        before = chain_state()
        after = evolve_residual(before, lambda z: ResidualState(z.type_id, 1 - z.value))
        self.assertEqual(access_records(before, (10, 30)), access_records(after, (10, 30)))
        # This supplied classical readout law is not a uniquely quantum principle.
        probability_one = lambda state: Fraction(state.residual.value)
        self.assertEqual(probability_one(before), 0)
        self.assertEqual(probability_one(after), 1)

    def test_exact_conditional_phase_witness_changes_future_readout_only(self) -> None:
        half = Fraction(1, 2)
        rho_plus = ((half, half), (half, half))
        before = ProcessState(CommittedSnapshot(), ResidualState("assumed-qubit", rho_plus))

        def phase_flip(z: ResidualState) -> ResidualState:
            rho = z.value
            signs = (1, -1)
            return ResidualState(
                z.type_id,
                tuple(tuple(signs[i] * rho[i][j] * signs[j] for j in range(2)) for i in range(2)),
            )

        def plus_readout(state: ProcessState) -> Fraction:
            rho = state.residual.value
            return sum(
                (rho_plus[i][j] * rho[j][i] for i in range(2) for j in range(2)), Fraction(0)
            )

        after = evolve_residual(before, phase_flip)
        self.assertIs(after.committed, before.committed)
        self.assertEqual(
            tuple(before.residual.value[i][i] for i in range(2)),
            tuple(after.residual.value[i][i] for i in range(2)),
        )
        self.assertEqual(plus_readout(before), 1)
        self.assertEqual(plus_readout(after), 0)
        self.assertEqual(evolve_residual(after, phase_flip), before)
        outcome = CommittedRecord(1, frozenset(), label="plus")
        recorded = commit_record(before, outcome, before.residual, plus_readout(before))
        self.assertEqual(recorded.committed.count, 1)
        with self.assertRaises(ValueError):
            commit_record(after, outcome, after.residual, plus_readout(after))


class CommitTests(unittest.TestCase):
    def test_positive_selected_commit_appends_once_without_mutating_history(self) -> None:
        before = chain_state()
        event = CommittedRecord(8, frozenset({10, -4, 30}), payload=("selected", 1))
        residual = ResidualState("different-output-system", Fraction(1, 2))
        after = commit_record(before, event, residual, Fraction(1, 3))
        self.assertEqual(after.committed.count, before.committed.count + 1)
        self.assertEqual(after.committed.records[:-1], before.committed.records)
        self.assertIs(after.committed.records[-1], event)
        self.assertIs(after.residual, residual)
        self.assertEqual(before.committed.count, 3)
        self.assertEqual(before.residual.value, 0)

    def test_zero_probability_branch_cannot_be_committed(self) -> None:
        state = chain_state()
        for zero in (0, 0.0, Fraction(0)):
            with self.subTest(zero=zero), self.assertRaises(ValueError):
                commit_record(state, CommittedRecord(99, frozenset()), state.residual, zero)
        self.assertEqual(state.committed.count, 3)

    def test_invalid_probabilities_fail_closed(self) -> None:
        state = chain_state()
        event = CommittedRecord(99, frozenset())
        for invalid in (True, -1, Fraction(4, 3), 1.1, math.nan, math.inf, "0.5", 1j):
            with self.subTest(invalid=invalid), self.assertRaises((TypeError, ValueError)):
                commit_record(state, event, state.residual, invalid)

    def test_strictly_positive_exact_probability_is_not_float_underflowed(self) -> None:
        state = chain_state()
        event = CommittedRecord(99, frozenset())
        after = commit_record(state, event, state.residual, Fraction(1, 10**500))
        self.assertEqual(after.committed.count, 4)

    def test_commit_checks_fresh_id_and_allowed_committed_ideal(self) -> None:
        state = chain_state()
        for event in (
            CommittedRecord(10, frozenset()),
            CommittedRecord(99, frozenset({404})),
            CommittedRecord(99, frozenset({30})),
        ):
            with self.subTest(event=event), self.assertRaises((KeyError, ValueError)):
                commit_record(state, event, state.residual, 1)
        self.assertEqual(state.committed.count, 3)

    def test_logged_null_is_a_record_not_a_silent_or_impossible_branch(self) -> None:
        state = chain_state()
        silent = evolve_residual(state, lambda z: ResidualState(z.type_id, 1))
        null = CommittedRecord(99, frozenset({10, -4, 30}), kind="null", label="no-click")
        logged = commit_record(state, null, silent.residual, Fraction(1, 2))
        self.assertEqual(silent.residual, logged.residual)
        self.assertEqual(silent.committed.count, 3)
        self.assertEqual(logged.committed.count, 4)
        self.assertEqual(logged.committed.records[-1].kind, "null")

    def test_delayed_receipt_adds_its_own_event_and_preserves_source(self) -> None:
        state = chain_state()
        receipt = CommittedRecord(
            99, frozenset({10, -4, 30}), kind="receipt", label="received-later", source_event_id=10
        )
        after = commit_record(state, receipt, state.residual, 1)
        self.assertEqual(after.committed.count, 4)
        self.assertIs(after.committed.records[0], state.committed.records[0])
        self.assertEqual(after.committed.records[-1].source_event_id, 10)
        self.assertTrue(after.committed.precedes(10, 99))
        self.assertFalse(after.committed.precedes(99, 10))


class RecordAccessTests(unittest.TestCase):
    def test_explicit_view_constructor_rejects_invalid_order_or_aliases(self) -> None:
        records = tuple(AccessibleRecord(i) for i in (1, 2, 3))
        for invalid_order in (
            frozenset({(1, 1)}),
            frozenset({(1, 4)}),
            frozenset({(1, 2), (2, 1)}),
            frozenset({(1, 2), (2, 3)}),
        ):
            with self.subTest(order=invalid_order), self.assertRaises(ValueError):
                RecordView(records, invalid_order)
        with self.assertRaises(ValueError):
            RecordView((records[0], records[0]))
        with self.assertRaises(TypeError):
            RecordView(records, set())
        with self.assertRaises(TypeError):
            RecordView(list(records))

    def test_missing_middle_keeps_induced_transitive_order(self) -> None:
        state = chain_state()
        view = access_records(state, (30, 10))
        self.assertEqual(tuple(record.event_id for record in view.records), (10, 30))
        self.assertEqual(view.order, frozenset({(10, 30)}))
        self.assertTrue(view.precedes(10, 30))
        self.assertFalse(view.precedes(30, 10))
        self.assertFalse(view.precedes(30, 30))
        self.assertFalse(any(hasattr(record, "past") for record in view.records))
        self.assertEqual(state.committed.count, 3)

    def test_access_can_be_non_past_closed_or_empty(self) -> None:
        state = chain_state()
        singleton = access_records(state, (30,))
        self.assertEqual(singleton.count, 1)
        self.assertEqual(singleton.order, frozenset())
        empty = access_records(state, ())
        self.assertEqual(empty.count, 0)
        self.assertEqual(empty.records, ())
        self.assertEqual(empty.order, frozenset())

    def test_access_rejects_unknown_duplicate_and_malformed_ids(self) -> None:
        state = chain_state()
        with self.assertRaises(KeyError):
            access_records(state, (404,))
        with self.assertRaises(ValueError):
            access_records(state, (10, 10))
        for invalid in (True, 10.0, "10"):
            with self.subTest(invalid=invalid), self.assertRaises(TypeError):
                access_records(state, (invalid,))
        with self.assertRaises(KeyError):
            access_records(state, (30,)).precedes(10, 30)

    def test_access_is_passive_immutable_and_not_an_implicit_receipt(self) -> None:
        state = chain_state()
        snapshot = state.committed
        residual = state.residual
        view = access_records(state, iter((10, 30)))
        self.assertIs(state.committed, snapshot)
        self.assertIs(state.residual, residual)
        self.assertEqual(state.committed.count, 3)
        with self.assertRaises(FrozenInstanceError):
            view.records = ()
        with self.assertRaises(FrozenInstanceError):
            view.records[0].label = "rewrite"

    def test_receipt_reference_does_not_create_an_accessible_source_vertex(self) -> None:
        state = chain_state()
        receipt = CommittedRecord(99, frozenset({10, -4, 30}), kind="receipt", source_event_id=10)
        after = commit_record(state, receipt, state.residual, 1)
        view = access_records(after, (99,))
        self.assertEqual(view.records[0].source_event_id, 10)
        self.assertEqual(tuple(record.event_id for record in view.records), (99,))
        self.assertEqual(view.order, frozenset())
        with self.assertRaises(KeyError):
            view.precedes(10, 99)


if __name__ == "__main__":
    unittest.main()
