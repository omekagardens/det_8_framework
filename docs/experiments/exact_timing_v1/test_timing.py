"""Independent exact timing fixtures and raw observation/chronology oracles.

These supplied rational records are mathematical fixtures, not measurements.
No native event law, calibrated clock or statistical coverage is inferred.
"""

import re
import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction

from timing import Bounds, Interval, Record, Request, fingerprint, infer, witness

F = Fraction
SLOTS = ("A1", "B2", "B3", "A4")
COMPATIBLE = "compatible_given_premises"
INCOMPATIBLE = "incompatible_given_premises"
INSUFFICIENT = "insufficient_records"
UNSUPPORTED = "unsupported_clock_or_channel_model"


def records_for(values=(0, 5, 7, 8)):
    return tuple(
        Record(
            record_id="record-" + slot,
            exchange_id="exchange-1",
            slot=slot,
            clock_id="clock-A" if slot in ("A1", "A4") else "clock-B",
            message_id="outbound" if slot in ("A1", "B2") else "reply",
            unit="s",
            value=F(value),
        )
        for slot, value in zip(SLOTS, values, strict=True)
    )


def request_for(values=(0, 5, 7, 8), **changes):
    fields = {
        "exchange_id": "exchange-1",
        "clock_a": "clock-A",
        "clock_b": "clock-B",
        "unit": "s",
        "premise_id": "declared-shared-time-model",
        "clock_model": "shared_unit_rate_constant_offsets",
        "uncertainty_model": "exact",
        "records": records_for(values),
        "bounds": Bounds(),
        "tolerance": F(3),
    }
    fields.update(changes)
    return Request(**fields)


def change_row(request, index, **changes):
    rows = list(request.records)
    if "disposition_reason" not in changes:
        if changes.get("status") == "missing":
            changes["disposition_reason"] = "acquisition record unavailable"
        elif changes.get("status") == "not_received_by_cutoff":
            changes["disposition_reason"] = "no receipt by the declared finite cutoff"
        elif changes.get("role") == "proposed":
            changes["disposition_reason"] = "planned acquisition, not executed"
        elif changes.get("role") == "withheld":
            changes["disposition_reason"] = "reserved for held-out evaluation"
        elif changes.get("selected") is False:
            changes["disposition_reason"] = "excluded by fixed fixture selection"
    rows[index] = replace(rows[index], **changes)
    return replace(request, records=tuple(rows))


class ExactAssertions(unittest.TestCase):
    def assert_interval(self, request, lower, upper, precision):
        result = infer(request)
        lower, upper = F(lower), F(upper)
        self.assertEqual(result.status, COMPATIBLE)
        self.assertEqual(result.reason, "exact_projection")
        self.assertIs(type(result.interval), Interval)
        self.assertEqual((result.interval.lower, result.interval.upper), (lower, upper))
        self.assertEqual(result.estimate, (lower + upper) / 2)
        self.assertEqual(result.radius, (upper - lower) / 2)
        for value in (result.interval.lower, result.interval.upper, result.estimate, result.radius):
            self.assertIs(type(value), Fraction)
        self.assertIs(result.precision_met, precision)
        self.assertEqual(result.input_id, fingerprint(request))
        self.assertRegex(result.input_id, re.compile(r"\A[0-9a-f]{64}\Z"))
        return result

    def assert_no_inference(self, request, status, reason):
        result = infer(request)
        self.assertEqual((result.status, result.reason), (status, reason))
        for field in ("interval", "estimate", "radius", "precision_met"):
            self.assertIsNone(getattr(result, field))
        self.assertEqual(result.input_id, fingerprint(request))
        self.assertIsNone(witness(request, F(0)))
        return result

    def assert_raw_witness(self, request, theta):
        result = witness(request, F(theta))
        self.assertIsNotNone(result)
        self.assertEqual(result.input_id, fingerprint(request))
        self.assertEqual(result.theta, theta)
        self.assertEqual((result.beta_a, result.beta_b), (F(0), F(theta)))
        self.assertIs(type(result.times), tuple)
        self.assertEqual(len(result.times), 4)
        values = (
            result.theta,
            result.beta_a,
            result.beta_b,
            result.forward_delay,
            result.reverse_delay,
            result.turnaround,
        ) + result.times
        self.assertTrue(all(type(value) is Fraction for value in values))
        rows = {row.slot: row for row in request.records if row.role == "actual" and row.selected}
        for slot, actual_time in zip(SLOTS, result.times, strict=True):
            beta = result.beta_a if slot in ("A1", "A4") else result.beta_b
            self.assertEqual(actual_time + beta, rows[slot].value)
        for earlier, later in zip(result.times, result.times[1:]):
            self.assertLessEqual(earlier, later)
        self.assertEqual(result.forward_delay, result.times[1] - result.times[0])
        self.assertEqual(result.turnaround, result.times[2] - result.times[1])
        self.assertEqual(result.reverse_delay, result.times[3] - result.times[2])
        for bound, value in (
            (request.bounds.forward, result.forward_delay),
            (request.bounds.reverse, result.reverse_delay),
            (request.bounds.asymmetry, result.forward_delay - result.reverse_delay),
        ):
            if bound is not None:
                self.assertLessEqual(bound.lower, value)
                self.assertLessEqual(value, bound.upper)
        return result


class MathematicalFixtures(ExactAssertions):
    def test_fixture_unrestricted_delays(self):
        request = request_for()
        self.assert_interval(request, -1, 5, True)
        first = self.assert_raw_witness(request, 2)
        second = self.assert_raw_witness(request, 1)
        self.assertEqual((first.forward_delay, first.reverse_delay), (3, 3))
        self.assertEqual((second.forward_delay, second.reverse_delay), (4, 2))

    def test_fixture_reciprocity(self):
        request = request_for(bounds=Bounds(asymmetry=Interval(F(0), F(0))), tolerance=F(0))
        self.assert_interval(request, 2, 2, True)
        self.assertEqual(self.assert_raw_witness(request, 2).times, (0, 3, 5, 8))

    def test_fixture_bounded_asymmetry(self):
        request = request_for(bounds=Bounds(asymmetry=Interval(F(-1), F(1))))
        self.assert_interval(request, F(3, 2), F(5, 2), True)
        self.assert_raw_witness(request, F(3, 2))
        self.assert_raw_witness(request, F(5, 2))

    def test_fixture_directional_bounds(self):
        request = request_for(bounds=Bounds(Interval(F(2), F(4)), Interval(F(2), F(4))))
        self.assert_interval(request, 1, 3, True)
        for theta in (1, 2, 3):
            self.assert_raw_witness(request, theta)

    def test_fixture_impossible_asymmetry(self):
        request = request_for(bounds=Bounds(asymmetry=Interval(F(7), F(7))))
        self.assert_no_inference(request, INCOMPATIBLE, "empty_compatibility")

    def test_fixture_negative_turnaround(self):
        self.assert_no_inference(request_for((0, 5, 4, 8)), INCOMPATIBLE, "negative_turnaround")

    def test_fixture_negative_roundtrip(self):
        self.assert_no_inference(request_for((0, 1, 3, 1)), INCOMPATIBLE, "negative_roundtrip")

    def test_three_simultaneous_optional_bounds(self):
        request = request_for(
            (0, 5, 7, 10),
            bounds=Bounds(Interval(F(3), F(4)), Interval(F(4), F(5)), Interval(F(-1), F(1))),
        )
        self.assert_interval(request, 1, F(3, 2), True)
        for theta in (F(1), F(5, 4), F(3, 2)):
            self.assert_raw_witness(request, theta)

    def test_one_directional_bound_alone(self):
        for bounds, low, high in (
            (Bounds(forward=Interval(F(2), F(4))), 1, 3),
            (Bounds(reverse=Interval(F(2), F(4))), 1, 3),
            (Bounds(forward=Interval(F(0), F(0))), 5, 5),
            (Bounds(reverse=Interval(F(0), F(0))), -1, -1),
        ):
            with self.subTest(bounds=bounds):
                request = request_for(bounds=bounds)
                self.assert_interval(request, low, high, True)
                self.assert_raw_witness(request, low)
                self.assert_raw_witness(request, high)

    def test_zero_delay_and_coincident_events_remain_distinct_records(self):
        request = request_for((3, 7, 7, 3), tolerance=F(0))
        self.assert_interval(request, 4, 4, True)
        result = self.assert_raw_witness(request, 4)
        self.assertEqual(result.times, (3, 3, 3, 3))
        self.assertEqual(len({row.record_id for row in request.records}), 4)

    def test_tolerance_uses_radius_with_inclusive_equality(self):
        for tolerance, met in ((F(3), True), (F(3) - F(1, 10000), False), (F(4), True)):
            self.assert_interval(request_for(tolerance=tolerance), -1, 5, met)
        request = request_for(
            (0, 1003, 1005, 8), bounds=Bounds(asymmetry=Interval(F(0), F(0))), tolerance=F(0)
        )
        self.assert_interval(request, 1000, 1000, True)

    def test_witness_refuses_only_outside_points_in_bounded_compatible_case(self):
        request = request_for()
        for theta in (F(-1), F(7, 3), F(5)):
            self.assert_raw_witness(request, theta)
        for theta in (F(-1) - F(1, 10**6), F(5) + F(1, 10**6)):
            self.assertIsNone(witness(request, theta))

    def test_minimax_endpoints_against_competing_estimates(self):
        request = request_for()
        low, high = (
            self.assert_raw_witness(request, -1).theta,
            self.assert_raw_witness(request, 5).theta,
        )
        for estimate in (F(-10), low, F(0), F(2), F(5, 2), high, F(9)):
            loss = max(abs(estimate - low), abs(estimate - high))
            self.assertGreaterEqual(loss, 3)
            self.assertEqual(loss == 3, estimate == 2)

    def test_generated_physical_schedules_and_raw_feasibility_grid(self):
        # Generate physical event times first; do not copy the interval formula.
        configurations = (
            (F(-2), F(1, 3), F(2, 3), F(0), F(0)),
            (F(3, 2), F(2), F(1), F(4), F(-10)),
            (F(0), F(0), F(3), F(1, 2), F(7)),
            (F(-5), F(4), F(0), F(2), F(1)),
        )
        for theta, forward, reverse, turnaround, start in configurations:
            physical = (
                start,
                start + forward,
                start + forward + turnaround,
                start + forward + turnaround + reverse,
            )
            displayed = (physical[0], physical[1] + theta, physical[2] + theta, physical[3])
            bounds = Bounds(Interval(F(0), F(5)), Interval(F(0), F(5)), Interval(F(-3), F(4)))
            request = request_for(displayed, bounds=bounds)
            result = infer(request)
            self.assertEqual(result.status, COMPATIBLE)
            self.assert_raw_witness(request, theta)
            for target in (F(n, 6) for n in range(-42, 43)):
                times = (displayed[0], displayed[1] - target, displayed[2] - target, displayed[3])
                p, r, q = times[1] - times[0], times[2] - times[1], times[3] - times[2]
                feasible = 0 <= p <= 5 and r >= 0 and 0 <= q <= 5 and -3 <= p - q <= 4
                self.assertEqual(result.interval.lower <= target <= result.interval.upper, feasible)
                self.assertEqual(witness(request, target) is not None, feasible)

    def test_common_epoch_shift_preserves_offset_and_delays(self):
        original = request_for()
        shifted = request_for(tuple(row.value + F(100, 3) for row in original.records))
        before, after = infer(original), infer(shifted)
        self.assertEqual(before.interval, after.interval)
        first, second = self.assert_raw_witness(original, 1), self.assert_raw_witness(shifted, 1)
        self.assertEqual(second.times, tuple(value + F(100, 3) for value in first.times))
        self.assertEqual(
            (first.forward_delay, first.reverse_delay), (second.forward_delay, second.reverse_delay)
        )
        self.assertNotEqual(before.input_id, after.input_id)

    def test_independent_clock_epoch_shifts_translate_offset_interval(self):
        original = request_for()
        alpha, beta = F(7, 3), F(-5, 2)
        values = tuple(
            row.value + (alpha if row.slot in ("A1", "A4") else beta) for row in original.records
        )
        shifted = request_for(values)
        delta = beta - alpha
        self.assert_interval(shifted, -1 + delta, 5 + delta, True)
        result = self.assert_raw_witness(shifted, 2 + delta)
        self.assertEqual((result.forward_delay, result.reverse_delay, result.turnaround), (3, 3, 2))


class RecordAndIdentityTests(ExactAssertions):
    def test_extra_nontraining_rows_do_not_change_the_interval(self):
        base = request_for()
        for role, selected in (
            ("actual", False),
            ("proposed", True),
            ("withheld", True),
            ("withheld", False),
        ):
            extra = replace(
                base.records[0],
                record_id="unused",
                role=role,
                selected=selected,
                exchange_id="different-exchange",
                clock_id="different-clock",
                unit="ms",
                message_id="different-message",
                value=F(-100),
                error=F(1, 10),
                disposition_reason="retained outside this training exchange",
            )
            request = replace(base, records=base.records + (extra,))
            self.assert_interval(request, -1, 5, True)
            self.assertNotEqual(fingerprint(request), fingerprint(base))

    def test_role_or_selection_cannot_fill_a_missing_actual_slot(self):
        base = request_for()
        for change in ({"role": "proposed"}, {"role": "withheld"}, {"selected": False}):
            request = change_row(base, 1, **change)
            self.assert_no_inference(request, INSUFFICIENT, "incomplete_exchange")

    def test_missing_slot_and_explicit_missing_record(self):
        base = request_for()
        self.assert_no_inference(
            replace(base, records=base.records[:-1]), INSUFFICIENT, "incomplete_exchange"
        )
        for index in range(4):
            request = change_row(base, index, value=None, status="missing")
            self.assert_no_inference(request, INSUFFICIENT, "incomplete_exchange")

    def test_finite_absence_is_not_an_arrival(self):
        base = request_for()
        for index in (1, 3):
            request = change_row(base, index, value=None, status="not_received_by_cutoff")
            self.assert_no_inference(request, INSUFFICIENT, "incomplete_exchange")

    def test_duplicate_effective_slot_never_selects_one_by_order(self):
        base = request_for()
        extra = replace(base.records[0], record_id="another-send", value=F(1))
        for rows in (base.records + (extra,), (extra,) + base.records):
            self.assert_no_inference(replace(base, records=rows), UNSUPPORTED, "ambiguous_slots")

    def test_record_associations(self):
        base = request_for()
        variants = (
            change_row(base, 0, exchange_id="wrong-exchange"),
            change_row(base, 1, clock_id="clock-A"),
            change_row(base, 3, clock_id="clock-B"),
            change_row(base, 1, message_id="wrong-outbound"),
            change_row(base, 3, message_id="wrong-reply"),
            change_row(change_row(base, 2, message_id="outbound"), 3, message_id="outbound"),
        )
        for request in variants:
            self.assert_no_inference(request, UNSUPPORTED, "record_association")

    def test_unit_mismatch_is_unsupported_not_converted(self):
        self.assert_no_inference(change_row(request_for(), 2, unit="ms"), UNSUPPORTED, "unit")

    def test_uncertain_reading_is_not_replaced_by_its_midpoint(self):
        self.assert_no_inference(
            change_row(request_for(), 1, error=F(1, 100)), UNSUPPORTED, "nonexact_reading"
        )

    def test_drift_and_joint_uncertainty_need_separate_models(self):
        self.assert_no_inference(
            request_for(clock_model="linear_drift"), UNSUPPORTED, "clock_model"
        )
        self.assert_no_inference(
            request_for(uncertainty_model="correlated_polytope"), UNSUPPORTED, "uncertainty_model"
        )

    def test_documented_status_precedence(self):
        base = request_for()
        self.assert_no_inference(
            replace(base, records=(), clock_model="drift", uncertainty_model="interval"),
            UNSUPPORTED,
            "clock_model",
        )
        self.assert_no_inference(
            replace(base, records=(), uncertainty_model="interval"),
            UNSUPPORTED,
            "uncertainty_model",
        )
        duplicate = replace(
            base.records[0],
            record_id="extra",
            status="missing",
            value=None,
            disposition_reason="duplicate slot with unavailable acquisition",
        )
        self.assert_no_inference(
            replace(base, records=(base.records[0], duplicate)), UNSUPPORTED, "ambiguous_slots"
        )
        mixed = change_row(base, 0, exchange_id="wrong", unit="ms", error=F(1))
        self.assert_no_inference(mixed, UNSUPPORTED, "record_association")
        mixed = change_row(base, 0, unit="ms", error=F(1))
        self.assert_no_inference(mixed, UNSUPPORTED, "unit")
        self.assert_no_inference(
            change_row(request_for((0, 5, 4, 8)), 0, error=F(1)), UNSUPPORTED, "nonexact_reading"
        )
        self.assert_no_inference(request_for((0, 5, 4, -2)), INCOMPATIBLE, "negative_turnaround")

    def test_all_request_declarations_bind_identity(self):
        base = request_for()
        variants = (
            replace(base, exchange_id="new-exchange"),
            replace(base, clock_a="new-clock-A"),
            replace(base, clock_b="new-clock-B"),
            replace(base, unit="ms"),
            replace(base, premise_id="different-premise"),
            replace(base, clock_model="drift"),
            replace(base, uncertainty_model="interval"),
            replace(base, tolerance=F(4)),
            replace(base, bounds=Bounds(forward=Interval(F(0), F(100)))),
            replace(base, bounds=Bounds(reverse=Interval(F(0), F(100)))),
            replace(base, bounds=Bounds(asymmetry=Interval(F(-100), F(100)))),
        )
        identities = [fingerprint(base)] + [fingerprint(request) for request in variants]
        self.assertEqual(len(identities), len(set(identities)))

    def test_every_record_field_binds_even_an_excluded_record(self):
        base = request_for()
        extra = replace(
            base.records[0],
            record_id="excluded",
            selected=False,
            disposition_reason="excluded by fixed fixture selection",
        )
        original = replace(base, records=base.records + (extra,))
        changes = (
            {"record_id": "renamed"},
            {"exchange_id": "another-exchange"},
            {"slot": "B3"},
            {"clock_id": "another-clock"},
            {"message_id": "another-message"},
            {"unit": "ms"},
            {"value": F(999)},
            {"role": "proposed"},
            {"selected": True},
            {"status": "missing", "value": None},
            {"error": F(1, 10)},
            {"disposition_reason": "independent alternative exclusion declaration"},
        )
        for change in changes:
            request = replace(original, records=base.records + (replace(extra, **change),))
            self.assertNotEqual(fingerprint(request), fingerprint(original))

    def test_record_order_binds_identity_but_not_mathematics(self):
        base = request_for()
        reordered = replace(base, records=tuple(reversed(base.records)))
        self.assert_interval(reordered, -1, 5, True)
        self.assertNotEqual(fingerprint(reordered), fingerprint(base))
        self.assert_raw_witness(reordered, F(1, 3))

    def test_equivalent_reduced_fractions_have_the_same_identity(self):
        base = request_for()
        equal = replace(
            base,
            records=tuple(
                replace(row, value=F(row.value.numerator * 7, row.value.denominator * 7))
                for row in base.records
            ),
            tolerance=F(9, 3),
        )
        self.assertEqual(fingerprint(base), fingerprint(equal))
        self.assertEqual(infer(base), infer(equal))

    def test_frozen_inputs_and_outputs(self):
        request = request_for()
        report = infer(request)
        attained = witness(request, F(2))
        for obj, name, value in (
            (request, "tolerance", F(99)),
            (request.records[0], "value", F(99)),
            (request.bounds, "forward", Interval(F(0), F(1))),
            (report.interval, "lower", F(-99)),
            (report, "radius", F(0)),
            (attained, "theta", F(99)),
        ):
            with self.assertRaises((FrozenInstanceError, AttributeError)):
                setattr(obj, name, value)


class InputAndResourceTests(ExactAssertions):
    def test_rational_fields_refuse_inexact_and_nonfraction_types(self):
        class FractionSubclass(Fraction):
            pass

        for invalid in (
            0,
            True,
            False,
            0.0,
            float("nan"),
            float("inf"),
            "0",
            None,
            FractionSubclass(0),
        ):
            constructors = (
                lambda value=invalid: Interval(value, F(1)),
                lambda value=invalid: Interval(F(-1), value),
                lambda value=invalid: replace(records_for()[0], value=value),
                lambda value=invalid: replace(records_for()[0], error=value),
                lambda value=invalid: request_for(tolerance=value),
                lambda value=invalid: witness(request_for(), value),
            )
            for construct in constructors:
                with (
                    self.subTest(value=repr(invalid), constructor=construct),
                    self.assertRaises(ValueError),
                ):
                    construct()

    def test_interval_and_bound_declaration_refusals(self):
        constructors = (
            lambda: Interval(F(1), F(0)),
            lambda: Bounds(forward=Interval(F(-1), F(1))),
            lambda: Bounds(reverse=Interval(F(-1), F(1))),
            lambda: Bounds(forward=(F(0), F(1))),
            lambda: Bounds(asymmetry={"lower": F(0), "upper": F(1)}),
            lambda: request_for(bounds=None),
            lambda: request_for(bounds={}),
            lambda: request_for(tolerance=F(-1)),
        )
        for construct in constructors:
            with self.assertRaises(ValueError):
                construct()

    def test_record_status_role_and_payload_refusals(self):
        base = records_for()[0]
        variants = (
            {"slot": "unknown"},
            {"role": "unknown"},
            {"status": "unknown"},
            {"selected": 1},
            {"selected": None},
            {"value": None},
            {"error": F(-1)},
            {"status": "missing"},
            {"status": "missing", "value": None, "error": F(1)},
            {"status": "not_received_by_cutoff", "value": None},
        )
        for change in variants:
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(base, **change)
        with self.assertRaises(ValueError):
            replace(records_for()[2], status="not_received_by_cutoff", value=None)

    def test_disposition_reason_required_for_every_nontraining_or_absent_record(self):
        base = records_for()[1]
        for change in (
            {"selected": False},
            {"role": "proposed"},
            {"role": "withheld"},
            {"status": "missing", "value": None},
            {"status": "not_received_by_cutoff", "value": None},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                replace(base, **change)
            retained = replace(
                base, disposition_reason="retained disposition explanation", **change
            )
            self.assertTrue(retained.disposition_reason)
        for invalid in (None, 0, True, "r" * 129):
            with self.assertRaises(ValueError):
                replace(base, disposition_reason=invalid)
        self.assertEqual(replace(base, disposition_reason="r" * 128).disposition_reason, "r" * 128)

    def test_bounded_string_types_and_lengths(self):
        base = request_for()
        for value in (None, 0, True, "", "x" * 129):
            for field in (
                "exchange_id",
                "clock_a",
                "clock_b",
                "unit",
                "premise_id",
                "clock_model",
                "uncertainty_model",
            ):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    replace(base, **{field: value})
            for field in ("record_id", "exchange_id", "clock_id", "message_id", "unit"):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    replace(base.records[0], **{field: value})
        self.assertEqual(replace(base, premise_id="p" * 128).premise_id, "p" * 128)

    def test_distinct_clock_ids_and_unique_all_record_ids(self):
        base = request_for()
        with self.assertRaises(ValueError):
            replace(base, clock_b=base.clock_a)
        for extra in (
            base.records[0],
            replace(
                base.records[0],
                selected=False,
                role="withheld",
                disposition_reason="held out from this fit",
            ),
        ):
            with self.assertRaises(ValueError):
                replace(base, records=base.records + (extra,))

    def test_strict_record_container_and_element_types(self):
        base = request_for()
        for rows in (list(base.records), iter(base.records), {}, "records", None, (object(),)):
            with self.assertRaises(ValueError):
                replace(base, records=rows)

    def test_request_count_limit_includes_excluded_records(self):
        base = request_for()
        extras = tuple(
            replace(
                base.records[0],
                record_id="excluded-" + str(n),
                selected=False,
                disposition_reason="excluded by fixed fixture selection",
            )
            for n in range(60)
        )
        request = replace(base, records=base.records + extras)
        self.assert_interval(request, -1, 5, True)
        with self.assertRaises(ValueError):
            replace(
                request,
                records=request.records
                + (
                    replace(
                        base.records[0],
                        record_id="one-too-many",
                        selected=False,
                        disposition_reason="excluded by fixed fixture selection",
                    ),
                ),
            )

    def test_request_rejects_oversized_numeric_inputs_even_in_unused_records(self):
        base = request_for()
        too_large = F(1 << 256)
        too_precise = F(1, 1 << 256)
        for value in (too_large, -too_large, too_precise):
            record = replace(
                base.records[0],
                record_id="unused",
                selected=False,
                value=value,
                disposition_reason="excluded by fixed fixture selection",
            )
            with self.assertRaises(ValueError):
                replace(base, records=base.records + (record,))
        for value in (too_large, too_precise):
            with self.assertRaises(ValueError):
                replace(base, tolerance=value)
            record = replace(
                base.records[0],
                record_id="unused",
                selected=False,
                error=value,
                disposition_reason="excluded by fixed fixture selection",
            )
            with self.assertRaises(ValueError):
                replace(base, records=base.records + (record,))
            for bounds in (
                Bounds(forward=Interval(F(0), value)),
                Bounds(reverse=Interval(F(0), value)),
                Bounds(asymmetry=Interval(-value, value)),
            ):
                with self.assertRaises(ValueError):
                    replace(base, bounds=bounds)

    def test_largest_legal_input_produces_larger_exact_endpoint_and_witness(self):
        largest = F((1 << 256) - 1)
        request = request_for((-largest, largest, largest, largest), tolerance=largest)
        self.assert_interval(request, 0, 2 * largest, True)
        result = self.assert_raw_witness(request, 2 * largest)
        self.assertGreater(result.theta.numerator.bit_length(), 256)
        self.assertEqual((result.forward_delay, result.reverse_delay), (0, 2 * largest))
        self.assertEqual(Interval(F(0), 2 * largest).upper, 2 * largest)

    def test_large_derived_denominator_is_not_clipped_or_rejected(self):
        a, b = (1 << 255) - 1, (1 << 255) + 1
        request = request_for((-F(1, a), F(1, b), F(1, b), F(1, b)))
        result = self.assert_interval(request, 0, F(1, a) + F(1, b), True)
        self.assertGreater(result.interval.upper.denominator.bit_length(), 256)
        self.assert_raw_witness(request, result.interval.upper)

    def test_public_functions_refuse_wrong_request_classes(self):
        for invalid in (None, {}, (), "request", object()):
            for call in (
                lambda invalid=invalid: fingerprint(invalid),
                lambda invalid=invalid: infer(invalid),
                lambda invalid=invalid: witness(invalid, F(0)),
            ):
                with self.assertRaises(ValueError):
                    call()


if __name__ == "__main__":
    unittest.main()
