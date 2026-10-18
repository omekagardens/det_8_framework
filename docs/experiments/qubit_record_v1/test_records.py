"""Adversarial checks of observable records, independent of simulator truth."""

import unittest
from dataclasses import FrozenInstanceError, replace

from records import (
    ERASURE_MODEL,
    Command,
    RecordError,
    TrialRecord,
    canonical_json,
    decode_record,
    fresh_identity,
    validate_sequence,
)


def fresh_record(index=0, setting="X", split="training", **changes):
    trial, preparation, record = fresh_identity("session", "recipe", split, setting, index)
    command = Command("command:" + trial, "prepare:" + preparation, setting)
    result = TrialRecord(
        record,
        trial,
        preparation,
        "recipe",
        "session",
        split,
        0,
        "prepare:" + preparation,
        (command,),
        setting,
        "frame",
        "calibration",
        "simulation:test",
        ERASURE_MODEL,
        "successful",
        "detected",
        True,
        1,
    )
    return replace(result, **changes)


def sequential_records():
    first_command = Command("command:serial:0", "prepare:serial", "Z")
    first = TrialRecord(
        "record:serial:0",
        "serial",
        "serial",
        "recipe",
        "session",
        "sequential",
        0,
        "prepare:serial",
        (first_command,),
        "Z",
        "frame",
        "calibration",
        "simulation:test",
        ERASURE_MODEL,
        "successful",
        "detected",
        True,
        1,
    )
    second_command = Command("command:serial:1", first_command.command_id, "Y")
    second = replace(
        first,
        record_id="record:serial:1",
        step=1,
        precursor_id=first.record_id,
        commands=(first_command, second_command),
        setting="Y",
        outcome=-1,
    )
    return first, second


class RecordTests(unittest.TestCase):
    def test_exact_json_round_trip_has_only_observable_fields(self):
        record = fresh_record()
        encoded = canonical_json(record.to_dict())
        self.assertEqual(decode_record(encoded), record)
        self.assertEqual(record.to_dict()["commands"], [record.commands[0].to_dict()])
        self.assertNotIn("truth", record.to_dict())
        self.assertNotIn("state", record.to_dict())
        self.assertEqual(record.precursor_id, "prepare:" + record.preparation_id)

    def test_json_rejects_duplicate_unknown_nonfinite_and_boolean_version(self):
        record = fresh_record().to_dict()
        cases = [
            '{"schema_version":1,"schema_version":1}',
            '{"schema_version":NaN}',
            "not JSON",
            canonical_json({**record, "schema_version": True}),
            canonical_json({**record, "truth": [0, 0, 1]}),
            canonical_json({key: value for key, value in record.items() if key != "status"}),
        ]
        for encoded in cases:
            with self.subTest(encoded=encoded[:50]), self.assertRaises(RecordError):
                decode_record(encoded)
        command = record["commands"][0]
        with self.assertRaises(RecordError):
            Command.from_dict({**command, "inferred": True})

    def test_binary_outcomes_are_actual_strict_signed_integers(self):
        for invalid in (True, False, 1.0, 0, 2, "1", None):
            with self.subTest(outcome=invalid), self.assertRaises(RecordError):
                fresh_record(outcome=invalid)
        self.assertEqual(fresh_record(outcome=-1).outcome, -1)
        with self.assertRaises(RecordError):
            fresh_record(measurement_occurred=False)
        with self.assertRaises(RecordError):
            fresh_record(reason="invented qualifier")

    def test_missing_means_completed_read_with_erased_outcome_not_zero(self):
        missing = fresh_record(status="missing", outcome=None, reason="outcome_erased")
        self.assertTrue(missing.measurement_occurred)
        self.assertIsNone(missing.outcome)
        self.assertEqual(decode_record(canonical_json(missing.to_dict())), missing)
        for changes in (
            {"measurement_occurred": False},
            {"outcome": 0},
            {"outcome": -1},
            {"reason": None},
            {"reason": "failed preparation"},
        ):
            with self.subTest(changes=changes), self.assertRaises(RecordError):
                replace(missing, **changes)

    def test_failed_or_unknown_preparation_is_retained_not_repaired(self):
        for preparation_status in ("failed", "unknown"):
            record = fresh_record(
                preparation_status=preparation_status,
                status="failed",
                measurement_occurred=False,
                outcome=None,
                reason="preparation unresolved",
            )
            self.assertEqual(record.preparation_status, preparation_status)
            self.assertIsNone(record.outcome)
            self.assertEqual(decode_record(canonical_json(record.to_dict())), record)
            with self.assertRaises(RecordError):
                replace(record, outcome=1)
        with self.assertRaises(RecordError):
            fresh_record(preparation_status="assumed successful")

    def test_command_prefix_is_ordered_complete_and_setting_bound(self):
        record = fresh_record()
        command = record.commands[0]
        for changes in (
            {"commands": ()},
            {"commands": [command]},
            {"commands": (replace(command, precursor_id="other"),)},
            {"setting": "Z"},
            {"commands": (replace(command, setting="Y"),)},
        ):
            with self.subTest(changes=changes), self.assertRaises(RecordError):
                replace(record, **changes)
        with self.assertRaises(RecordError):
            replace(command, kind="inferred_update")
        with self.assertRaises(RecordError):
            Command("same", "same", "X")
        first, second = sequential_records()
        with self.assertRaises(RecordError):
            repeated = replace(second.commands[1], command_id=first.commands[0].command_id)
            replace(second, commands=(first.commands[0], repeated))
        repeated_later = Command(first.commands[0].command_id, second.commands[1].command_id, "Z")
        with self.assertRaises(RecordError):
            replace(
                second,
                record_id="record:serial:2",
                step=2,
                precursor_id=second.record_id,
                setting="Z",
                commands=(*second.commands, repeated_later),
            )
        reused_anchor = replace(second.commands[1], command_id=first.commands[0].precursor_id)
        with self.assertRaises(RecordError):
            replace(second, commands=(first.commands[0], reused_anchor))

    def test_identifiers_steps_and_statuses_do_not_accept_loose_values(self):
        record = fresh_record()
        for name in (
            "record_id",
            "trial_id",
            "recipe_id",
            "session_id",
            "frame_id",
            "calibration_id",
            "provenance",
            "acquisition_model",
        ):
            with self.subTest(field=name), self.assertRaises(RecordError):
                replace(record, **{name: ""})
        for step in (True, 0.0, -1):
            with self.subTest(step=step), self.assertRaises(RecordError):
                replace(record, step=step)
        for changes in (
            {"measurement_occurred": 1},
            {"status": "discarded"},
            {"split": "truth"},
            {"setting": "unknown"},
            {"precursor_id": "unrelated preparation"},
            {"record_id": record.precursor_id},
        ):
            with self.subTest(changes=changes), self.assertRaises(RecordError):
                replace(record, **changes)

    def test_frozen_schedule_ids_do_not_depend_on_detected_outcomes(self):
        entries = [fresh_record(index) for index in range(4)]
        entries[1] = replace(entries[1], status="missing", outcome=None, reason="outcome_erased")
        self.assertEqual(
            [r.trial_id for r in entries],
            [fresh_identity("session", "recipe", "training", "X", n)[0] for n in range(4)],
        )
        self.assertEqual(len({r.preparation_id for r in entries}), 4)
        self.assertNotEqual(entries[0].trial_id, fresh_record(split="heldout").trial_id)
        for invalid in (True, 0.0, -1):
            with self.subTest(index=invalid), self.assertRaises(RecordError):
                fresh_identity("session", "recipe", "training", "X", invalid)

    def test_serial_prefix_preserves_commands_precursors_and_object_identity(self):
        records = sequential_records()
        self.assertIs(validate_sequence(records), records)
        self.assertEqual(records[1].commands[:-1], records[0].commands)
        self.assertEqual(records[1].precursor_id, records[0].record_id)
        self.assertEqual(tuple(command.setting for command in records[1].commands), ("Z", "Y"))
        self.assertEqual(tuple(record.outcome for record in records), (1, -1))

    def test_serial_reordering_duplicates_context_or_history_changes_refused(self):
        first, second = sequential_records()
        for records in (
            (second,),
            (second, first),
            (first, first),
            (first, replace(second, session_id="foreign")),
            (first, replace(second, calibration_id="foreign")),
            (first, replace(second, preparation_status="unknown")),
            (first, replace(second, precursor_id="other record")),
            (first, replace(second, preparation_status="unknown", split="training")),
        ):
            with self.subTest(records=records), self.assertRaises(RecordError):
                validate_sequence(records)
        altered_command = replace(second.commands[0], setting="X")
        changed = replace(second, commands=(altered_command, second.commands[1]))
        with self.assertRaises(RecordError):
            validate_sequence((first, changed))

    def test_unresolved_serial_record_ends_actual_prefix(self):
        first, second = sequential_records()
        missing = replace(first, status="missing", outcome=None, reason="outcome_erased")
        failed = replace(
            first,
            status="failed",
            outcome=None,
            measurement_occurred=False,
            reason="update law unavailable",
        )
        for unresolved in (missing, failed):
            self.assertEqual(validate_sequence((unresolved,)), (unresolved,))
            with self.subTest(status=unresolved.status), self.assertRaises(RecordError):
                validate_sequence((unresolved, second))
        with self.assertRaises(RecordError):
            validate_sequence(())

    def test_records_and_command_prefixes_are_immutable(self):
        record = fresh_record()
        with self.assertRaises(FrozenInstanceError):
            record.outcome = -1
        with self.assertRaises(FrozenInstanceError):
            record.commands[0].setting = "Z"
        copied = record.to_dict()
        copied["commands"][0]["setting"] = "Z"
        self.assertEqual(record.commands[0].setting, "X")


if __name__ == "__main__":
    unittest.main()
