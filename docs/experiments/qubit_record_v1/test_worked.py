"""End-to-end simulator boundaries, held-out isolation and serial information loss."""

import json
import tempfile
import unittest
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

import simulator
import worked_example
from inference import ExperimentPlan, InferenceRefusal, fit, score
from qubit import Bloch, nonselective_update, plus_probability
from records import decode_record, validate_sequence
from simulator import DEFAULT_TRUTH, replay_sequence, simulate_fresh, simulate_sequence


def small_plan():
    return ExperimentPlan(
        recipe_ids=("recipe",),
        shots=64,
        training_epsilon=F(1, 2),
        held_epsilon=F(1, 2),
        calibration=F(0),
        drift=F(0),
        future_calibration=F(0),
        future_drift=F(0),
    )


class WorkedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="qubit_record_tests-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.output = Path(cls.temporary.name) / "worked"
        cls.generation_order = []

        def observed_generation(plan, split, **kwargs):
            cls.generation_order.append(
                (
                    split,
                    (cls.output / "predictions.json").exists(),
                    (cls.output / "partial_xz_prediction.json").exists(),
                    (cls.output / "truth_audit.json").exists(),
                )
            )
            return simulate_fresh(plan, split, **kwargs)

        with patch("worked_example.simulate_fresh", side_effect=observed_generation):
            cls.summary = worked_example.run(cls.output)
        cls.training = tuple(
            decode_record(line) for line in (cls.output / "training.jsonl").read_text().splitlines()
        )
        cls.heldout = tuple(
            decode_record(line) for line in (cls.output / "heldout.jsonl").read_text().splitlines()
        )

    def test_worked_generation_freezes_predictions_before_heldout_and_truth(self):
        self.assertEqual(
            self.generation_order,
            [
                ("training", False, False, False),
                ("heldout", True, True, False),
            ],
        )
        self.assertEqual(
            self.summary["pipeline_order"],
            [
                "plan",
                "training",
                "frozen_prediction",
                "heldout",
                "score",
                "truth_audit",
            ],
        )
        self.assertTrue(self.summary["frozen_prediction_unchanged"])
        self.assertEqual(self.summary["status"], "synthetic_worked_example_not_physical_validation")
        saved = json.loads((self.output / "score.json").read_text())
        self.assertEqual(saved["prediction_sha256"], self.summary["prediction_sha256"])
        frozen = fit(ExperimentPlan(), self.training)
        self.assertEqual(frozen.fingerprint, self.summary["prediction_sha256"])

    def test_worked_export_retains_every_attempt_and_separates_audit_truth(self):
        self.assertEqual((len(self.training), len(self.heldout)), (4608, 1536))
        all_rows = self.training + self.heldout
        self.assertEqual(len({r.record_id for r in all_rows}), 6144)
        self.assertEqual(len({r.preparation_id for r in all_rows}), 6144)
        self.assertTrue(all(r.step == 0 and len(r.commands) == 1 for r in all_rows))
        self.assertEqual({r.setting for r in self.training}, {"X", "Y", "Z"})
        self.assertEqual({r.setting for r in self.heldout}, {"W"})
        self.assertEqual(
            self.summary["training_missing"], sum(r.status == "missing" for r in self.training)
        )
        self.assertEqual(
            self.summary["heldout_missing"], sum(r.status == "missing" for r in self.heldout)
        )
        self.assertGreater(self.summary["training_missing"], 0)
        for record in all_rows:
            self.assertTrue(
                {"truth", "bloch", "state", "latent_outcome", "rng", "seed"}.isdisjoint(
                    record.to_dict()
                )
            )
            if record.status == "missing":
                self.assertIsNone(record.outcome)
                self.assertTrue(record.measurement_occurred)
        truth = json.loads((self.output / "truth_audit.json").read_text())
        self.assertIn("simulation-only", truth["provenance"])
        self.assertEqual(set(truth["states"]), {"phase_plus", "phase_minus", "mixed"})

    def test_phase_and_mixed_expected_laws_are_exact_not_fitted(self):
        plus = DEFAULT_TRUTH["phase_plus"]
        minus = DEFAULT_TRUTH["phase_minus"]
        mixed = DEFAULT_TRUTH["mixed"]
        self.assertEqual(plus.r, (F(0), F(3, 5), F(0)))
        self.assertEqual(minus.r, (F(0), F(-3, 5), F(0)))
        self.assertEqual(plus_probability(plus, "Z"), F(1, 2))
        self.assertEqual(plus_probability(minus, "Z"), F(1, 2))
        self.assertEqual(
            (plus_probability(plus, "Y"), plus_probability(minus, "Y")), (F(4, 5), F(1, 5))
        )
        self.assertEqual(
            (plus_probability(plus, "W"), plus_probability(minus, "W")), (F(17, 25), F(8, 25))
        )
        self.assertEqual(plus_probability(mixed, "W"), F(12, 25))
        self.assertTrue(all(row["same_conventional_point"] for row in self.summary["results"]))
        self.assertTrue(all(row["point_estimate"] is None for row in self.summary["partial_XZ"]))
        self.assertTrue(
            all(len(row["unresolved_alternatives"]) == 2 for row in self.summary["partial_XZ"])
        )

    def test_outcome_dependent_erasure_does_not_select_a_detected_only_sample(self):
        plan = small_plan()
        truth = {"recipe": Bloch((0, 1, 0))}
        rows = simulate_fresh(plan, "training", truth, seed=19, erasure_plus=1, erasure_minus=0)
        self.assertEqual(len(rows), 3 * plan.shots)
        self.assertTrue(all(r.status == "missing" for r in rows if r.setting == "Y"))
        self.assertTrue(all(r.outcome == -1 for r in rows if r.status == "detected"))
        self.assertEqual(len({r.preparation_id for r in rows}), 3 * plan.shots)
        result = fit(plan, rows).results[0]
        self.assertEqual(result.axes[1].missing, plan.shots)
        self.assertIsNone(result.point_estimate)
        with self.assertRaises(InferenceRefusal):
            fit(plan, tuple(r for r in rows if r.status == "detected"))
        erased = simulate_fresh(plan, "training", truth, seed=19, erasure_plus=1, erasure_minus=1)
        self.assertEqual(tuple(r.record_id for r in rows), tuple(r.record_id for r in erased))
        self.assertTrue(all(r.status == "missing" and r.outcome is None for r in erased))

    def test_simulator_is_reproducible_with_strict_explicit_truth_and_seed(self):
        plan = small_plan()
        truth = {"recipe": Bloch((0, 0, 1))}
        rows = simulate_fresh(plan, "training", truth, seed=7, erasure_plus=0, erasure_minus=0)
        self.assertEqual(
            rows, simulate_fresh(plan, "training", truth, seed=7, erasure_plus=0, erasure_minus=0)
        )
        self.assertTrue(all(r.status == "detected" for r in rows))
        self.assertTrue(all(r.outcome == 1 for r in rows if r.setting == "Z"))
        for kwargs in ({"seed": True}, {"erasure_plus": 0.1}, {"erasure_minus": F(6, 5)}):
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                simulate_fresh(plan, "training", truth, **kwargs)
        for invalid_truth in ({}, {"recipe": (0, 0, 1)}, {"other": Bloch((0, 0, 1))}):
            with self.subTest(truth=invalid_truth), self.assertRaises(ValueError):
                simulate_fresh(plan, "training", invalid_truth)
        with self.assertRaises(ValueError):
            simulate_fresh(plan, "sequential", truth)
        serial_metadata = []
        for seed in (34151, 59261):
            serial = simulate_sequence(
                plan,
                truth["recipe"],
                ("X", "Z"),
                seed=seed,
                sequence_id="fixed-nominal-control",
            )
            metadata = []
            for record in serial:
                data = record.to_dict()
                self.assertNotIn(str(seed), json.dumps(data))
                del data["outcome"]
                metadata.append(data)
            serial_metadata.append(metadata)
        self.assertEqual(*serial_metadata)
        for sequence_id in ("", "bad/label", True):
            with self.subTest(sequence_id=sequence_id), self.assertRaises(ValueError):
                simulate_sequence(plan, truth["recipe"], ("X",), sequence_id=sequence_id)

    def test_mutating_truth_and_W_cannot_change_fit_of_given_training_records(self):
        plan = small_plan()
        truth = {"recipe": Bloch((0, F(3, 5), 0))}
        training = simulate_fresh(plan, "training", truth, seed=8, erasure_plus=0, erasure_minus=0)
        frozen = fit(plan, training)
        before = frozen.fingerprint
        truth["recipe"] = Bloch((0, F(-3, 5), 0))
        heldout = simulate_fresh(plan, "heldout", truth, seed=9, erasure_plus=0, erasure_minus=0)
        changed_W = tuple(replace(r, outcome=-r.outcome) for r in heldout)
        with (
            patch.object(simulator, "DEFAULT_TRUTH", object()),
            patch.object(
                simulator,
                "simulate_fresh",
                side_effect=AssertionError("inference accessed generator"),
            ),
        ):
            repeated = fit(plan, training)
            original_score = score(frozen, heldout)
            changed_score = score(frozen, changed_W)
        self.assertEqual(repeated, frozen)
        self.assertEqual(frozen.fingerprint, before)
        self.assertEqual(original_score["prediction_sha256"], changed_score["prediction_sha256"])
        self.assertNotEqual(original_score["heldout_sha256"], changed_score["heldout_sha256"])

    def test_sequential_erasure_stops_without_future_attempt_or_residual(self):
        plan = small_plan()
        initial = Bloch((0, 1, 0))
        for erased_step in (0, 1):
            rows = simulate_sequence(plan, initial, ("Y", "Y", "Z"), seed=12, erase_at=erased_step)
            self.assertEqual(len(rows), erased_step + 1)
            self.assertEqual(len(rows[-1].commands), erased_step + 1)
            self.assertEqual(rows[-1].status, "missing")
            self.assertIsNone(rows[-1].outcome)
            self.assertTrue(rows[-1].measurement_occurred)
            self.assertIs(validate_sequence(rows), rows)
            report = replay_sequence(rows, initial)
            self.assertEqual(report["status"], "unresolved_no_selected_update")
            self.assertIsNone(report["residual"])
            self.assertEqual(report["retained_record_ids"], tuple(r.record_id for r in rows))
        with self.assertRaises(ValueError):
            simulate_sequence(plan, initial, ("Y",), erase_at=True)
        with self.assertRaises(ValueError):
            simulate_sequence(plan, initial, ("Y",), erase_at=1)

    def test_zero_probability_serial_observation_is_retained_as_mismatch(self):
        plan = small_plan()
        initial = Bloch((0, 1, 0))
        lawful = simulate_sequence(plan, initial, ("Y", "Y", "Z"), seed=16)
        contradictory = (lawful[0], replace(lawful[1], outcome=-lawful[0].outcome))
        report = replay_sequence(contradictory, initial)
        self.assertEqual(report["status"], "model_mismatch_zero_probability")
        self.assertEqual(report["mismatch_record_id"], contradictory[-1].record_id)
        self.assertEqual(report["retained_record_ids"], tuple(r.record_id for r in contradictory))
        self.assertIsNone(report["residual"])
        self.assertEqual(contradictory[-1].outcome, -1)
        self.assertEqual(lawful[1].outcome, 1)
        failed = replace(
            lawful[0],
            status="failed",
            outcome=None,
            measurement_occurred=False,
            reason="unspecified failure law",
        )
        self.assertEqual(
            replay_sequence((failed,), initial)["status"], "unresolved_no_selected_update"
        )

    def test_disturbance_erases_earlier_phase_not_independent_tomography(self):
        plan = small_plan()
        plus, minus = DEFAULT_TRUTH["phase_plus"], DEFAULT_TRUTH["phase_minus"]
        self.assertNotEqual(plus_probability(plus, "Y"), plus_probability(minus, "Y"))
        self.assertEqual(nonselective_update(plus, "Z"), Bloch((0, 0, 0)))
        self.assertEqual(nonselective_update(minus, "Z"), Bloch((0, 0, 0)))
        self.assertEqual(plus_probability(nonselective_update(plus, "Z"), "Y"), F(1, 2))
        paths = [
            simulate_sequence(plan, initial, ("Z", "Y", "Y"), seed=24) for initial in (plus, minus)
        ]
        self.assertEqual(paths[0], paths[1])
        self.assertEqual(paths[0][1].outcome, paths[0][2].outcome)
        replay = replay_sequence(paths[0], plus)
        self.assertEqual(replay["residual"], (F(0), F(paths[0][-1].outcome), F(0)))
        self.assertEqual(len({r.preparation_id for r in paths[0]}), 1)
        with self.assertRaises(InferenceRefusal):
            fit(plan, paths[0])

    def test_output_is_outside_checkout_and_existing_results_are_not_overwritten(self):
        self.assertNotIn(worked_example.CHECKOUT, self.output.resolve().parents)
        before = (self.output / "summary.json").read_bytes()
        with self.assertRaises(ValueError):
            worked_example.run(self.output)
        self.assertEqual((self.output / "summary.json").read_bytes(), before)
        for destination in (worked_example.CHECKOUT, worked_example.BUNDLE / "not-created"):
            with self.subTest(path=destination), self.assertRaises(ValueError):
                worked_example.run(destination)
        self.assertFalse((worked_example.BUNDLE / "not-created").exists())
        with self.assertRaises(ValueError):
            worked_example.run(Path(self.temporary.name) / "invalid-seed", seed=True)


if __name__ == "__main__":
    unittest.main()
