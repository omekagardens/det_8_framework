"""Independent end-to-end checks of observable traces, not a geometry derivation."""

import json
import tempfile
import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

import kinematics
import sim
import worked_example
from clock_readings import elapsed_bounds
from kinematics import Geometry, QTime, StaticTime
from local_records import canonical_json, decode_record, validate_history
from observer import infer, pulse_spacing
from sim import EmissionSpec, ObserverConfig, simulate


def receipts(result, observer="B"):
    return tuple(row for row in result.history(observer) if row.kind == "reception")


def observers(ell=F(1, 4), offsets=(0, 0)):
    return (ObserverConfig("A", 0, offsets[0]), ObserverConfig("B", ell, offsets[1]))


def signal(name="one", moment=None, emitter="A", target="B", frequency=1):
    return EmissionSpec(
        name,
        emitter,
        target,
        QTime(1) if moment is None else moment,
        reference_frequency=frequency,
        crest_id="crest:" + name,
    )


class WorkedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="observer_signal_tests-")
        cls.output = Path(cls.temporary.name) / "worked"
        cls.summary = worked_example.run(cls.output)
        cls.reports = {row["fixture"]: row for row in cls.summary["results"]}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_worked_exports_retain_all_emissions_and_separate_audit(self):
        self.assertEqual(self.summary["fixture_count"], 10)
        self.assertEqual(sum(row["emissions"] for row in self.reports.values()), 11)
        self.assertEqual(sum(row["receptions"] for row in self.reports.values()), 8)
        self.assertIsNone(self.summary["actualization_to_geometry_rule"])
        self.assertIn("not_actualization_derivation_or_measurement", self.summary["status"])
        closures = 0
        forbidden = {"H", "q", "chi", "offset", "forecast", "geometry", "global_time"}

        def check_fields(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for nested in value.values():
                    check_fields(nested)
            elif isinstance(value, list):
                for nested in value:
                    check_fields(nested)

        for name in self.reports:
            directory = self.output / name
            plan = json.loads((directory / "observer_plan.json").read_text())
            for observer in ("A", "B"):
                rows = tuple(
                    decode_record(line)
                    for line in (directory / (observer + ".jsonl")).read_text().splitlines()
                )
                self.assertEqual(validate_history(observer, rows), rows)
                closures += sum(row.kind == "window_closed" for row in rows)
                self.assertEqual(set(plan[observer]), {"expected_signals", "calibration_id"})
                check_fields([row.to_dict() for row in rows])
                self.assertEqual(
                    infer(observer, rows, tuple(plan[observer]["expected_signals"]), "ideal-v1"),
                    self.reports[name]["observer_reports"][observer],
                )
            self.assertTrue((directory / "model_audit.json").is_file())
        self.assertEqual(closures, 20)
        self.assertEqual(json.loads((self.output / "summary.json").read_text()), self.summary)

    def test_mixed_arrival_classes_never_drop_an_actual_emission(self):
        values = (F(1), F(3, 4), F(5, 16), F(1, 4), F(1, 8))
        schedule = tuple(signal(f"s{n}", QTime(q), frequency=7) for n, q in enumerate(values))
        result = simulate(Geometry(H=1), observers(), tuple(reversed(schedule)), QTime(F(1, 8)))
        emitted = tuple(row for row in result.history("A") if row.kind == "emission")
        self.assertEqual(
            tuple(row.payload.signal_id for row in emitted), tuple(f"s{n}" for n in range(5))
        )
        received = receipts(result)
        self.assertEqual(tuple(row.payload.signal_id for row in received), ("s0", "s1"))
        self.assertEqual(tuple(row.measured_frequency for row in received), (F(21, 4), F(14, 3)))
        for row in received:
            self.assertEqual(
                row.payload, next(e.payload for e in emitted if e.payload == row.payload)
            )
        report = infer("B", result.history("B"), tuple(f"s{n}" for n in range(5)), "ideal-v1")
        self.assertEqual(
            [row["status"] for row in report["results"]],
            ["received", "received"] + ["not_received_by_cutoff"] * 3,
        )
        forecasts = {f["signal_id"]: f["forecast"]["status"] for f in result.audit["forecast"]}
        self.assertEqual(forecasts["s2"], "finite")
        self.assertEqual(forecasts["s3"], "asymptotic_future_only")
        self.assertEqual(forecasts["s4"], "beyond_future_horizon")
        self.assertNotIn("horizon", canonical_json(report))

    def test_cutoff_decision_uses_exact_arrival_not_equal_rounded_displays(self):
        schedule = (signal(moment=QTime(F(3, 8))),)
        exact = simulate(Geometry(H=1), observers(), schedule, QTime(F(1, 8)), places=0)
        earlier = simulate(
            Geometry(H=1), observers(), schedule, QTime(F(1, 8) + F(1, 10**12)), places=0
        )
        self.assertEqual(len(receipts(exact)), 1)
        self.assertEqual(len(receipts(earlier)), 0)
        self.assertEqual(
            exact.history("B")[-1].timestamp.value, earlier.history("B")[-1].timestamp.value
        )
        self.assertEqual(receipts(exact)[0].timestamp.value, exact.history("B")[-1].timestamp.value)
        self.assertEqual(receipts(exact)[0].measured_frequency, F(1, 3))
        self.assertEqual(exact.history("B")[-1].precursor_id, "receive:one")
        self.assertEqual(earlier.history("B")[-1].precursor_id, "start:B")

    def test_invalid_schedule_or_clock_failure_refuses_instead_of_filtering(self):
        g, configs, cutoff = Geometry(H=1), observers(), QTime(F(1, 2))
        valid = signal()
        for schedule in (
            (valid, signal("future", QTime(F(1, 4)))),
            (valid, valid),
            (replace(valid, target_id="unknown"),),
            (replace(valid, emitted_at=StaticTime(0)),),
            [valid],
        ):
            with self.subTest(schedule=schedule), self.assertRaises((ValueError, TypeError)):
                simulate(g, configs, schedule, cutoff)
        for invalid in (list(configs), (configs[0], configs[0]), configs[:1]):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                simulate(g, invalid, (valid,), cutoff)
        # No dropped receipt, "absent" substitution, or partial Simulation is returned.
        with (
            patch.object(sim, "display_log", side_effect=ValueError("display failed")),
            self.assertRaisesRegex(ValueError, "display failed"),
        ):
            simulate(g, configs, (valid,), cutoff)
        with self.assertRaises(ValueError):
            ObserverConfig("A", 0.1)
        with self.assertRaises(ValueError):
            replace(valid, reference_frequency=True)

    def test_reverse_direction_and_contraction_use_absolute_separation(self):
        schedule = (signal("ab", frequency=4), signal("ba", emitter="B", target="A", frequency=4))
        result = simulate(Geometry(H=-1), observers(), schedule, QTime(2))
        for name in ("A", "B"):
            rows = result.history(name)
            self.assertEqual([row.kind for row in rows], ["emission", "reception", "window_closed"])
            self.assertEqual(receipts(result, name)[0].measured_frequency, 5)
            expected = ("ba",) if name == "A" else ("ab",)
            answer = infer(name, rows, expected, "ideal-v1")["results"][0]
            self.assertEqual(answer["frequency_ratio"], "5/4")
            self.assertEqual(answer["redshift"], "-1/5")
            self.assertIsNone(answer["flight_time"])
        self.assertEqual([f["comoving_separation"] for f in result.audit["forecast"]], ["1/4"] * 2)

    def test_colocated_distinct_observers_keep_payload_not_clock_synchronization(self):
        configs = (ObserverConfig("A", F(7, 3), 7), ObserverConfig("B", F(7, 3), -3))
        result = simulate(Geometry(H=1), configs, (signal(frequency=9),), QTime(1))
        emitted, received = result.history("A")[0], receipts(result)[0]
        self.assertEqual(emitted.payload, received.payload)
        self.assertEqual(received.measured_frequency, 9)
        self.assertEqual(emitted.timestamp.value, 7)
        self.assertEqual(received.timestamp.value, -3)
        self.assertEqual([row.kind for row in result.history("B")], ["reception", "window_closed"])
        answer = infer("B", result.history("B"), ("one",), "ideal-v1")["results"][0]
        self.assertEqual((answer["frequency_ratio"], answer["redshift"]), ("1", "0"))
        self.assertIsNone(answer["flight_time"])
        self.assertEqual(result.audit["forecast"][0]["forecast"]["delay"]["constant"], "0")

    def test_coordinate_translation_and_compensated_rescaling_preserve_traces(self):
        schedule = (signal(),)
        cutoff = QTime(F(1, 2))
        base = simulate(Geometry(H=1), observers(), schedule, cutoff)
        translated = simulate(
            Geometry(H=1), (ObserverConfig("A", 5), ObserverConfig("B", F(21, 4))), schedule, cutoff
        )
        rescaled = simulate(Geometry(H=1, a_star=3), observers(F(1, 12)), schedule, cutoff)
        self.assertEqual(base.histories, translated.histories)
        self.assertEqual(base.histories, rescaled.histories)
        self.assertNotEqual(base.audit["geometry"], rescaled.audit["geometry"])
        self.assertNotEqual(base.audit["observers"], translated.audit["observers"])

    def test_offgrid_clock_offsets_can_reduce_spacing_resolution_without_changing_frequency(self):
        schedule = (signal("first", StaticTime(F(1, 25))), signal("second", StaticTime(F(3, 50))))
        base = simulate(Geometry(), observers(0), schedule, StaticTime(1), places=1)
        shifted = simulate(
            Geometry(), observers(0, (F(1, 20), F(1, 20))), schedule, StaticTime(1), places=1
        )
        first, second = receipts(base)
        shifted_first, shifted_second = receipts(shifted)
        self.assertEqual((first.timestamp.value, second.timestamp.value), (0, F(1, 10)))
        self.assertEqual(
            (shifted_first.timestamp.value, shifted_second.timestamp.value), (F(1, 10),) * 2
        )
        self.assertEqual(elapsed_bounds(first.timestamp, second.timestamp), (F(1, 50), F(9, 50)))
        self.assertEqual(
            elapsed_bounds(shifted_first.timestamp, shifted_second.timestamp), (F(-1, 50), F(1, 50))
        )
        self.assertIsNotNone(pulse_spacing(first, second)["ratio_interval"])
        self.assertIsNone(pulse_spacing(shifted_first, shifted_second)["ratio_interval"])
        self.assertEqual(
            infer("B", base.history("B"), ("first", "second"), "ideal-v1"),
            infer("B", shifted.history("B"), ("first", "second"), "ideal-v1"),
        )
        self.assertEqual(len(receipts(shifted)), 2)

    def test_finite_pulse_spacing_is_not_either_instantaneous_redshift(self):
        report = self.reports["finite_pulses"]
        answers = report["observer_reports"]["B"]["results"]
        self.assertEqual([row["frequency_ratio"] for row in answers], ["1/2", "1/3"])
        lower, upper = map(F, report["finite_spacing"]["ratio_interval"])
        self.assertGreater(lower, 2)
        self.assertLess(upper, 3)
        # Independent monotonic-log certificate for 2 < ln(2)/ln(4/3) < 3.
        self.assertLess(F(4, 3) ** 2, 2)
        self.assertLess(2, F(4, 3) ** 3)
        self.assertEqual(
            report["finite_spacing"]["status"], "bounded_finite_spacing_not_instantaneous_redshift"
        )

    def test_equal_redshift_does_not_identify_delay_or_a_clock_offset(self):
        first, second = self.reports["expanding"], self.reports["same_redshift_different_delay"]
        self.assertEqual(first["observer_reports"]["B"], second["observer_reports"]["B"])
        delay1 = first["separate_model_forecasts"][0]["forecast"]["delay"]
        delay2 = second["separate_model_forecasts"][0]["forecast"]["delay"]
        self.assertEqual((delay1["constant"], delay2["constant"]), ("0", "0"))
        self.assertEqual((delay1["argument"], delay2["argument"]), ("2", "2"))
        self.assertEqual((delay1["coefficient"], delay2["coefficient"]), ("1", "1/2"))
        self.assertIsNone(first["observer_reports"]["B"]["results"][0]["flight_time"])

    def test_receiver_is_blind_to_mutated_audit_and_disabled_geometry_producer(self):
        result = simulate(Geometry(H=1), observers(), (signal(),), QTime(F(1, 2)))
        history = result.history("B")
        before = tuple(row.to_dict() for row in history)
        answer = infer("B", history, ("one", "missing"), "ideal-v1")
        result.audit["geometry"] = {"H": "unrelated", "q": "private"}
        result.audit["forecast"].clear()
        with (
            patch.object(sim, "arrive", side_effect=AssertionError("producer unavailable")),
            patch.object(kinematics, "arrive", side_effect=AssertionError("geometry unavailable")),
            patch.object(kinematics, "Geometry", side_effect=AssertionError("not observable")),
        ):
            self.assertEqual(infer("B", history, ("one", "missing"), "ideal-v1"), answer)
        self.assertEqual(tuple(row.to_dict() for row in history), before)
        with self.assertRaises(FrozenInstanceError):
            result.histories = ()
        with self.assertRaises(ValueError):
            result.history("unknown")

    def test_generated_output_is_outside_checkout_and_never_overwritten(self):
        self.assertNotIn(worked_example.CHECKOUT, self.output.resolve().parents)
        before = (self.output / "summary.json").read_bytes()
        with self.assertRaises(ValueError):
            worked_example.run(self.output)
        self.assertEqual((self.output / "summary.json").read_bytes(), before)
        for forbidden in (worked_example.CHECKOUT, worked_example.BUNDLE / "not-created-by-test"):
            with self.subTest(forbidden=forbidden), self.assertRaises(ValueError):
                worked_example.run(forbidden)
        self.assertFalse((worked_example.BUNDLE / "not-created-by-test").exists())


if __name__ == "__main__":
    unittest.main()
