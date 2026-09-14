"""Independent local-clock, record and receiver-only interpretation checks."""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F

from clock_readings import (
    ClockReading,
    display_log,
    elapsed_bounds,
    log_bounds,
    parse_rational,
    spacing_ratio,
)
from local_records import (
    LocalRecord,
    Payload,
    RecordError,
    canonical_json,
    decode_record,
    validate_history,
)
from observer import infer, pulse_spacing


def payload(index=0, emitted=0):
    return Payload(
        f"emit:{index}",
        f"signal:{index}",
        "A",
        "B",
        f"crest:{index}",
        F(5),
        ClockReading(emitted, 0),
        "pulse-train-v1",
    )


def receipt(index=0, received=10, emitted=0, precursor="start:B"):
    return LocalRecord(
        f"receive:{index}",
        "B",
        "reception",
        ClockReading(received, 0),
        precursor,
        payload(index, emitted),
        F(5, 2),
        "ideal-v1",
        "simulation-v1",
    )


def closure(precursor="start:B", at=20):
    return LocalRecord(
        "closed:B",
        "B",
        "window_closed",
        ClockReading(at, 0),
        precursor,
        None,
        None,
        "ideal-v1",
        "simulation-v1",
    )


class RecordTests(unittest.TestCase):
    def test_log_series_certificate_has_independent_exact_endpoints(self):
        self.assertEqual(log_bounds(3, terms=1), (F(8, 9), F(10, 9)))
        self.assertEqual(log_bounds(3, terms=2), (F(16, 15), F(11, 10)))
        self.assertEqual(log_bounds(F(1, 3), terms=1), (F(-10, 9), F(-8, 9)))
        self.assertEqual(log_bounds(1), (F(0), F(0)))
        first, second = log_bounds(3, 1), log_bounds(3, 2)
        self.assertLess(first[0], second[0])
        self.assertGreater(first[1], second[1])
        # This finite identity checks the implemented certificate, not an all-input proof.
        remainder = 2 * F(1, 2) ** 3 / (3 * (1 - F(1, 2) ** 2))
        self.assertEqual(remainder, F(1, 9))

    def test_quantization_error_and_signed_log_coefficient_are_retained(self):
        reading = display_log(3, -2, 3, places=0, terms=1)
        self.assertEqual(reading, ClockReading(1, F(223, 1000)))
        self.assertGreaterEqual(reading.error, F(2, 9))
        self.assertLess(reading.error - F(1, 1000), F(2, 9))
        self.assertEqual(display_log(F(1, 3), 0, 1, places=1), ClockReading(F(3, 10), F(167, 5000)))
        self.assertEqual(display_log(F(1, 4), 0, 1, places=1), ClockReading(F(1, 5), F(1, 20)))
        self.assertEqual(display_log(F(7, 20), 0, 1, places=1), ClockReading(F(2, 5), F(1, 20)))
        shifted = display_log(10, -2, 3, places=0, terms=1)
        self.assertEqual(shifted.value - reading.value, 7)
        self.assertEqual(shifted.error, reading.error)

    def test_clock_input_and_exact_json_numbers_are_strict(self):
        for value in (True, 0.1, "1"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ClockReading(value, 0)
        with self.assertRaises(ValueError):
            ClockReading(0, F(-1, 10))
        for argument in (0, -1, True, 1.0):
            with self.subTest(argument=argument), self.assertRaises(ValueError):
                log_bounds(argument)
        for terms in (0, True, 1.0):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                log_bounds(2, terms)
        for places in (-1, 19, True):
            with self.subTest(places=places), self.assertRaises(ValueError):
                display_log(0, 1, 2, places=places)
        for encoded in ("2/4", "1.0", "01", "1/0", 1):
            with self.subTest(encoded=encoded), self.assertRaises((ValueError, ZeroDivisionError)):
                parse_rational(encoded)
        self.assertEqual(parse_rational("-2/3"), F(-2, 3))

    def test_same_clock_gaps_and_spacing_propagate_display_errors(self):
        first, second = ClockReading(1, F(1, 10)), ClockReading(4, F(1, 5))
        self.assertEqual(elapsed_bounds(first, second), (F(27, 10), F(33, 10)))
        shifted = tuple(replace(r, value=r.value + F(7, 3)) for r in (first, second))
        self.assertEqual(elapsed_bounds(*shifted), elapsed_bounds(first, second))
        result = spacing_ratio(
            ClockReading(0, F(1, 10)),
            ClockReading(2, F(1, 10)),
            ClockReading(10, F(1, 5)),
            ClockReading(13, F(1, 5)),
        )
        self.assertEqual(result["emission_gap"], (F(9, 5), F(11, 5)))
        self.assertEqual(result["reception_gap"], (F(13, 5), F(17, 5)))
        self.assertEqual(result["ratio_interval"], (F(13, 11), F(17, 9)))
        self.assertEqual(result["status"], "bounded_finite_spacing_not_instantaneous_redshift")
        same = ClockReading(0, 0)
        self.assertEqual(
            spacing_ratio(same, same, same, same)["status"], "unresolved_display_precision_or_order"
        )
        self.assertIsNone(spacing_ratio(same, same, same, same)["ratio_interval"])

    def test_payload_and_emission_bind_local_identity_time_and_reference(self):
        transmitted = payload()
        emission = LocalRecord(
            transmitted.emission_id,
            "A",
            "emission",
            transmitted.emitter_timestamp,
            "start:A",
            transmitted,
            None,
            "ideal-v1",
            "simulation-v1",
        )
        self.assertIs(validate_history("A", (emission,))[0].payload, transmitted)
        for changes in (
            {"event_id": "different-emission"},
            {"observer_id": "B"},
            {"timestamp": ClockReading(1, 0)},
            {"measured_frequency": F(5)},
        ):
            with self.subTest(changes=changes), self.assertRaises(RecordError):
                replace(emission, **changes)
        for changes in (
            {"target_id": "A"},
            {"signal_id": ""},
            {"reference_frequency": 0},
            {"reference_frequency": True},
            {"emitter_timestamp": 0},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(transmitted, **changes)

    def test_reception_and_window_closure_cannot_forge_an_emission_or_forecast(self):
        row = receipt()
        for changes in (
            {"event_id": row.payload.emission_id},
            {"observer_id": "A"},
            {"measured_frequency": 0},
            {"measured_frequency": -1},
            {"payload": None},
            {"kind": "never_arrives"},
            {"event_id": row.precursor_id},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                replace(row, **changes)
        for changes in ({"payload": payload()}, {"measured_frequency": F(1)}):
            with self.subTest(changes=changes), self.assertRaises(RecordError):
                replace(closure(), **changes)
        self.assertIsNone(closure().payload)

    def test_round_trip_excludes_geometry_hidden_times_and_unknown_fields(self):
        row = receipt()
        self.assertEqual(decode_record(canonical_json(row.to_dict())), row)
        self.assertEqual(row.to_dict()["payload"]["reference_frequency"], "5")
        self.assertEqual(row.to_dict()["timestamp"]["kind"], "bounded_local_clock_display")
        for extra in ("H", "q", "scale_factor", "coordinates", "global_time", "forecast"):
            with self.subTest(extra=extra), self.assertRaises(RecordError):
                decode_record(canonical_json({**row.to_dict(), extra: 1}))
        for invalid in (
            '{"schema_version":1,"schema_version":1}',
            '{"value":NaN}',
            "not-json",
            canonical_json({**row.to_dict(), "schema_version": True}),
        ):
            with self.subTest(invalid=invalid[:30]), self.assertRaises(RecordError):
                decode_record(invalid)
        exported = row.to_dict()
        exported["timestamp"]["q"] = "1"
        with self.assertRaises(RecordError):
            decode_record(canonical_json(exported))

    def test_local_history_retains_prefix_without_cross_observer_clock_order(self):
        row = receipt(received=-10, emitted=100)
        end = closure(row.event_id, at=-5)
        history = (row, end)
        self.assertIs(validate_history("B", history), history)
        result = infer("B", history, ("signal:0",), "ideal-v1")["results"][0]
        self.assertEqual(result["frequency_ratio"], "1/2")
        self.assertEqual(result["redshift"], "1")
        self.assertIsNone(result["flight_time"])
        self.assertEqual(result["flight_time_status"], "unknown_cross_observer_clock_offset")
        self.assertEqual(row.payload.emitter_timestamp.value, 100)

    def test_history_rejects_foreign_duplicate_broken_or_postclosure_events(self):
        row = receipt()
        end = closure(row.event_id)
        for history in (
            (row, row),
            (end,),
            (row, replace(end, precursor_id="other")),
            (row, replace(end, calibration_id="other")),
            (row, replace(end, provenance="other")),
            (closure(), replace(row, precursor_id="closed:B")),
            [row, end],
        ):
            with self.subTest(history=history), self.assertRaises(RecordError):
                validate_history("B", history)
        with self.assertRaises(RecordError):
            validate_history("A", (row, end))

    def test_display_interval_order_is_feasible_for_the_entire_prefix(self):
        first = receipt(0, received=10)
        middle = replace(receipt(1, precursor=first.event_id), timestamp=ClockReading(0, 10))
        end = closure(middle.event_id, at=1)
        with self.assertRaises(RecordError):
            validate_history("B", (first, middle, end))
        # Overlapping uncertain displays alone are not an ordering contradiction.
        possible = (first, middle, replace(end, timestamp=ClockReading(10, 0)))
        self.assertEqual(validate_history("B", possible), possible)
        same_display = (receipt(), closure("receive:0", at=10))
        self.assertEqual(validate_history("B", same_display), same_display)

    def test_infer_missing_ids_need_actual_window_closure_not_a_never_claim(self):
        result = infer("B", (closure(),), ("signal:0", "signal:1"), "ideal-v1")
        self.assertEqual(result["cutoff_event_id"], "closed:B")
        self.assertEqual([r["status"] for r in result["results"]], ["not_received_by_cutoff"] * 2)
        self.assertTrue(
            all(r["event_id"] is None and r["frequency_ratio"] is None for r in result["results"])
        )
        self.assertNotIn("horizon", canonical_json(result))
        for history in ((), (receipt(),)):
            with self.subTest(history=history), self.assertRaises(RecordError):
                infer("B", history, ("signal:0",), "ideal-v1")
        for expected in (["signal:0"], ("signal:0", "signal:0"), ("",)):
            with self.subTest(expected=expected), self.assertRaises(RecordError):
                infer("B", (closure(),), expected, "ideal-v1")
        with self.assertRaises(RecordError):
            infer("B", (closure(),), (), "other-calibration")

    def test_duplicate_signal_receipt_refuses_without_hiding_either_record(self):
        first = receipt()
        second = replace(
            first,
            event_id="receive:duplicate",
            precursor_id=first.event_id,
            timestamp=ClockReading(11, 0),
        )
        records = (first, second, closure(second.event_id))
        self.assertEqual(validate_history("B", records), records)
        with self.assertRaises(RecordError):
            infer("B", records, ("signal:0",), "ideal-v1")
        self.assertEqual(len(records), 3)

    def test_clock_offsets_do_not_change_local_frequency_or_spacing_answers(self):
        first, second = receipt(), receipt(1, received=14, emitted=2, precursor="receive:0")
        history = (first, second, closure(second.event_id))
        original = infer("B", history, ("signal:0", "signal:1"), "ideal-v1")
        shifted = []
        for row in history:
            p = row.payload
            if p is not None:
                p = replace(
                    p,
                    emitter_timestamp=replace(
                        p.emitter_timestamp, value=p.emitter_timestamp.value + 71
                    ),
                )
            shifted.append(
                replace(
                    row, payload=p, timestamp=replace(row.timestamp, value=row.timestamp.value - 37)
                )
            )
        self.assertEqual(infer("B", tuple(shifted), ("signal:0", "signal:1"), "ideal-v1"), original)
        self.assertEqual(pulse_spacing(first, second), pulse_spacing(*shifted[:2]))
        self.assertEqual(pulse_spacing(first, second)["ratio_interval"], ["2", "2"])
        for bad in (
            replace(second, payload=replace(second.payload, message="different-train")),
            replace(second, payload=replace(second.payload, crest_id=first.payload.crest_id)),
            replace(second, calibration_id="other"),
        ):
            with self.subTest(bad=bad), self.assertRaises(RecordError):
                pulse_spacing(first, bad)

    def test_records_and_payload_are_immutable_but_exports_are_independent(self):
        row = receipt()
        with self.assertRaises(FrozenInstanceError):
            row.measured_frequency = F(1)
        with self.assertRaises(FrozenInstanceError):
            row.payload.reference_frequency = F(1)
        exported = row.to_dict()
        exported["payload"]["message"] = "changed"
        self.assertEqual(row.payload.message, "pulse-train-v1")


if __name__ == "__main__":
    unittest.main()
