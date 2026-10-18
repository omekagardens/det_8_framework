"""Exact adversarial inference checks; observations never contain simulator truth."""

import unittest
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F

from inference import (
    ExperimentPlan,
    InferenceRefusal,
    box_witness,
    conventional_tomography,
    fit,
    score,
    tail_certificate,
)
from records import ERASURE_MODEL, Command, TrialRecord, fresh_identity


def make_plan(**changes):
    values = {
        "recipe_ids": ("recipe",),
        "shots": 500,
        "calibration": F(0),
        "drift": F(0),
        "future_calibration": F(0),
        "future_drift": F(0),
    }
    return ExperimentPlan(**{**values, **changes})


def observations(plan, counts=None, *, axes=("X", "Y", "Z"), split="training"):
    """Build the full scheduled roster from explicitly supplied counts, no state."""
    counts = {} if counts is None else counts
    rows = []
    for recipe in plan.recipe_ids:
        for setting in axes:
            plus, minus = counts.get(setting, (plan.shots // 2, plan.shots - plan.shots // 2))
            if plus < 0 or minus < 0 or plus + minus > plan.shots:
                raise ValueError("malformed test fixture")
            for index in range(plan.shots):
                trial, prep, record_id = fresh_identity(
                    plan.session_id,
                    recipe,
                    split,
                    setting,
                    index,
                )
                missing = index >= plus + minus
                command = Command("command:" + trial, "prepare:" + prep, setting)
                rows.append(
                    TrialRecord(
                        record_id,
                        trial,
                        prep,
                        recipe,
                        plan.session_id,
                        split,
                        0,
                        "prepare:" + prep,
                        (command,),
                        setting,
                        plan.frame_id,
                        plan.calibration_id,
                        plan.provenance,
                        ERASURE_MODEL,
                        "successful",
                        "missing" if missing else "detected",
                        True,
                        None if missing else 1 if index < plus else -1,
                        "outcome_erased" if missing else None,
                    )
                )
    return tuple(rows)


class InferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = make_plan()
        cls.training = observations(cls.plan)
        cls.frozen = fit(cls.plan, cls.training)

    def test_hoeffding_certificate_is_exact_conservative_and_frozen(self):
        self.assertEqual(ExperimentPlan().training_strata, 9)
        self.assertTrue(tail_certificate(1, F(1), F(1, 2), terms=3))
        self.assertEqual(F(1) + 2 + 2 + F(4, 3), F(19, 3))
        self.assertFalse(tail_certificate(1, F(1), F(1, 2), terms=0))
        self.assertTrue(tail_certificate(500, F(1, 10), F(1, 300)))
        for args in ((0, F(1), F(1, 2)), (True, F(1), F(1, 2)), (1, 0.1, F(1, 2)), (1, F(1), F(0))):
            with self.subTest(args=args), self.assertRaises(InferenceRefusal):
                tail_certificate(*args)

    def test_plan_rejects_uncertified_nonexact_or_unsupported_premises(self):
        for changes in (
            {"shots": 0},
            {"shots": True},
            {"shots": 1},
            {"training_epsilon": 0.1},
            {"calibration": F(-1, 10)},
            {"alpha_train": 1},
            {"alpha_score": 1},
            {"alpha_train": F(3, 5), "alpha_score": F(3, 5)},
            {"recipe_ids": ("recipe", "recipe")},
            {"sampling_contract": "detected-only-iid"},
            {"preparation_contract": "unknown"},
            {"calibration_contract": "inferred-from-W"},
        ):
            with self.subTest(changes=changes), self.assertRaises(InferenceRefusal):
                make_plan(**changes)

    def test_missing_completion_bounds_use_all_attempts_not_detections(self):
        plan = make_plan(calibration=F(1, 100), drift=F(1, 50))
        rows = observations(plan, {"X": (100, 200)})
        result = fit(plan, rows).results[0]
        x = result.axes[0]
        self.assertEqual((x.attempted, x.plus, x.minus, x.missing), (500, 100, 200, 200))
        self.assertEqual(x.midpoint, F(-1, 5))
        self.assertNotEqual(x.midpoint, F(100 - 200, 100 + 200))
        self.assertEqual(x.eta, F(33, 100))
        self.assertEqual(x.interval, (F(-43, 50), F(23, 50)))
        completion = (F(100, 500), F(300, 500))
        self.assertEqual(
            tuple(
                2 * (p + shift) - 1
                for p, shift in zip(
                    completion,
                    (F(-13, 100), F(13, 100)),
                )
            ),
            x.interval,
        )
        self.assertEqual(len(rows), 1500)

    def test_missing_scheduled_attempt_duplicate_or_replacement_is_refused(self):
        for rows in (
            self.training[:-1],
            self.training + (self.training[0],),
            (self.training[0],) + self.training[:-1],
            list(self.training),
        ):
            with self.subTest(length=len(rows)), self.assertRaises(InferenceRefusal):
                fit(self.plan, rows)
        changed = replace(self.training[0], record_id="not-on-schedule")
        with self.assertRaises(InferenceRefusal):
            fit(self.plan, (changed,) + self.training[1:])

    def test_source_recipe_frame_calibration_and_status_mismatches_refuse(self):
        changes_list = [
            {"session_id": "other"},
            {"recipe_id": "other"},
            {"frame_id": "other"},
            {"calibration_id": "other"},
            {"provenance": "measured:unverified"},
            {"trial_id": "other"},
            {"acquisition_model": "unknown-missingness"},
            {"preparation_status": "failed"},
            {"preparation_status": "unknown"},
            {
                "status": "failed",
                "outcome": None,
                "reason": "unknown forward law",
                "measurement_occurred": False,
            },
        ]
        for changes in changes_list:
            changed = replace(self.training[0], **changes)
            with self.subTest(changes=changes), self.assertRaises(InferenceRefusal):
                fit(self.plan, (changed,) + self.training[1:])

    def test_fitting_refuses_withheld_W_serial_or_mixed_axis_rosters(self):
        heldout = observations(self.plan, axes=("W",), split="heldout")
        training_w = observations(self.plan, axes=("W",))
        serial = replace(self.training[0], split="sequential")
        for rows in (heldout, training_w, self.training + heldout, (serial,) + self.training[1:]):
            with self.subTest(length=len(rows)), self.assertRaises(InferenceRefusal):
                fit(self.plan, rows)
        for axes in (("W",), ("Z", "X"), ("X", "X"), (), ["X", "Y", "Z"]):
            with self.subTest(axes=axes), self.assertRaises(InferenceRefusal):
                fit(self.plan, self.training, axes=axes)

    def test_nearest_zero_box_witness_not_radial_projection(self):
        intervals = ((F(9, 10), F(9, 10)), (F(0), F(1)), (F(0), F(0)))
        self.assertEqual(box_witness(intervals), (F(9, 10), F(0), F(0)))
        center = (F(9, 10), F(1, 2), F(0))
        squared_norm = sum(x * x for x in center)
        self.assertEqual(squared_norm, F(53, 50))
        self.assertLess(center[0] ** 2 / squared_norm, intervals[0][0] ** 2)
        self.assertIsNone(box_witness(((F(4, 5), F(1)), (F(4, 5), F(1)), (0, 0))))
        self.assertEqual(
            box_witness(((F(-1), F(-3, 5)), (F(0), F(0)), (F(4, 5), F(1)))),
            (F(-3, 5), F(0), F(4, 5)),
        )

    def test_box_bounds_handle_zero_coordinates_empty_and_nonexact_inputs(self):
        self.assertEqual(box_witness(((-2, 2), (-2, 2), (-2, 2))), (F(0), F(0), F(0)))
        self.assertIsNone(box_witness(((2, 3), (0, 0), (0, 0))))
        self.assertIsNone(box_witness(((1, -1), (0, 0), (0, 0))))
        for intervals in ([(-1, 1)] * 3, ((0, 0),), ((0.0, 1), (0, 0), (0, 0))):
            with self.subTest(intervals=intervals), self.assertRaises(InferenceRefusal):
                box_witness(intervals)

    def test_physical_midpoint_and_baseline_use_identical_revealed_counts(self):
        counts = {"X": (300, 200), "Y": (350, 150), "Z": (200, 300)}
        rows = observations(self.plan, counts)
        result = fit(self.plan, rows).results[0]
        expected = (F(1, 5), F(2, 5), F(-1, 5))
        self.assertEqual(result.point_estimate, expected)
        self.assertEqual(result.conventional_midpoint, expected)
        self.assertEqual(result.conventional_point, expected)
        self.assertEqual(
            conventional_tomography(rows, "recipe", ("X", "Y", "Z")), (expected, expected)
        )
        self.assertEqual(result.point_probability, F(27, 50))
        self.assertEqual(result.trace_radius_squared, F(3, 100))
        self.assertEqual(result.ideal_probability_interval, (F(2, 5), F(17, 25)))
        first = rows[0]
        bad_rows = [
            (replace(first, preparation_status="unknown"),) + rows[1:],
            (replace(first, preparation_status="failed"),) + rows[1:],
            (replace(first, acquisition_model="unknown"),) + rows[1:],
            rows + (first,),
            rows + (replace(first, record_id="another-record"),),
            tuple(r for r in rows if r.setting != "Y"),
        ]
        prep_anchor = "prepare:" + first.preparation_id
        prep_alias = replace(
            rows[1],
            preparation_id=first.preparation_id,
            precursor_id=prep_anchor,
            commands=(replace(rows[1].commands[0], precursor_id=prep_anchor),),
        )
        bad_rows.append((first, prep_alias) + rows[2:])
        later_command = Command("later-command", first.commands[0].command_id, "X")
        nonfresh = replace(
            first,
            step=1,
            precursor_id="prior-record",
            commands=(*first.commands, later_command),
        )
        bad_rows.append((nonfresh,) + rows[1:])
        for invalid in bad_rows:
            with self.subTest(count=len(invalid)), self.assertRaises(InferenceRefusal):
                conventional_tomography(invalid, "recipe", ("X", "Y", "Z"))

    def test_nonphysical_midpoint_is_not_silently_projected_or_called_a_fit(self):
        rows = observations(self.plan, {axis: (500, 0) for axis in ("X", "Y", "Z")})
        result = fit(self.plan, rows).results[0]
        self.assertEqual(result.status, "incompatible_bounds")
        self.assertEqual(result.reference_midpoint, (F(1), F(1), F(1)))
        self.assertIsNone(result.witness)
        self.assertIsNone(result.point_estimate)
        self.assertIsNone(result.conventional_point)
        self.assertIsNone(result.ideal_probability_interval)
        self.assertIsNone(result.frozen_frequency_band)
        report = score(fit(self.plan, rows), observations(self.plan, axes=("W",), split="heldout"))
        self.assertEqual(report["results"][0]["status"], "not_scored_incompatible_training")

    def test_feasible_uncertainty_does_not_repair_a_nonphysical_midpoint(self):
        plan = make_plan(training_epsilon=F(1, 4))
        rows = observations(plan, {axis: (500, 0) for axis in ("X", "Y", "Z")})
        result = fit(plan, rows).results[0]
        self.assertEqual(result.status, "interval_only")
        self.assertEqual(result.witness, (F(1, 2), F(1, 2), F(1, 2)))
        self.assertIsNone(result.point_estimate)
        self.assertIsNone(result.point_probability)
        self.assertIsNone(result.conventional_point)

    def test_XZ_only_retains_unresolved_Y_and_distinct_withheld_alternatives(self):
        rows = observations(self.plan, {"X": (400, 100)}, axes=("X", "Z"))
        result = fit(self.plan, rows, axes=("X", "Z")).results[0]
        self.assertEqual(result.axes[1].attempted, 0)
        self.assertEqual(result.intervals[1], (F(-1), F(1)))
        self.assertIsNone(result.point_estimate)
        self.assertIsNone(result.conventional_point)
        self.assertIsNone(result.point_probability)
        self.assertEqual(result.status, "interval_only")
        self.assertEqual(len(result.unresolved_alternatives), 2)
        probabilities = []
        for alternative in result.unresolved_alternatives:
            self.assertLessEqual(sum(x * x for x in alternative), 1)
            self.assertTrue(
                all(lo <= x <= hi for x, (lo, hi) in zip(alternative, result.intervals))
            )
            probabilities.append((1 + F(3, 5) * alternative[1] + F(4, 5) * alternative[2]) / 2)
        self.assertNotEqual(*probabilities)
        exact_alternatives = ((F(3, 5), F(-4, 5), F(0)), (F(3, 5), F(4, 5), F(0)))
        self.assertEqual(
            tuple((1 + F(3, 5) * r[1]) / 2 for r in exact_alternatives), (F(13, 50), F(37, 50))
        )
        with self.assertRaises(InferenceRefusal):
            fit(self.plan, self.training, axes=("X", "Z"))

    def test_all_erased_training_is_retained_and_yields_no_point(self):
        rows = observations(self.plan, {axis: (0, 0) for axis in ("X", "Y", "Z")})
        result = fit(self.plan, rows).results[0]
        self.assertEqual(tuple(a.missing for a in result.axes), (500, 500, 500))
        self.assertEqual(result.status, "interval_only")
        self.assertEqual(result.witness, (F(0), F(0), F(0)))
        self.assertIsNone(result.point_estimate)
        self.assertEqual(result.ideal_probability_interval, (F(0), F(1)))

    def test_scoring_erasure_completion_and_brier_use_total_scheduled_N(self):
        heldout = observations(self.plan, {"W": (100, 200)}, axes=("W",), split="heldout")
        before = self.frozen.fingerprint
        report = score(self.frozen, heldout)["results"][0]
        self.assertEqual(
            (report["attempted"], report["plus"], report["minus"], report["missing"]),
            (500, 100, 200, 200),
        )
        self.assertEqual(report["completion_interval"], ["1/5", "3/5"])
        self.assertEqual(report["full_attempt_brier_interval"], ["1/4", "1/4"])
        self.assertEqual(self.frozen.fingerprint, before)
        all_erased = observations(self.plan, {"W": (0, 0)}, axes=("W",), split="heldout")
        self.assertEqual(
            score(self.frozen, all_erased)["results"][0]["status"], "uninformative_all_erased"
        )

    def test_impossible_point_outcomes_are_reported_not_dropped(self):
        rows = observations(self.plan, {"Y": (400, 100), "Z": (450, 50)})
        frozen = fit(self.plan, rows)
        self.assertEqual(frozen.results[0].point_probability, 1)
        heldout = observations(self.plan, {"W": (0, 500)}, axes=("W",), split="heldout")
        report = score(frozen, heldout)["results"][0]
        self.assertEqual(report["status"], "model_or_budget_mismatch")
        self.assertEqual(report["minus"], 500)
        self.assertEqual(len(report["point_zero_probability_record_ids"]), 500)
        self.assertEqual(
            set(report["point_zero_probability_record_ids"]), {r.record_id for r in heldout}
        )
        self.assertEqual(report["full_attempt_brier_interval"], ["1", "1"])

    def test_frozen_prediction_is_unchanged_by_revealed_W_and_input_order(self):
        before = self.frozen.to_dict()
        all_plus = observations(self.plan, {"W": (500, 0)}, axes=("W",), split="heldout")
        all_minus = observations(self.plan, {"W": (0, 500)}, axes=("W",), split="heldout")
        plus_score = score(self.frozen, all_plus)
        minus_score = score(self.frozen, all_minus)
        self.assertEqual(plus_score["prediction_sha256"], minus_score["prediction_sha256"])
        self.assertNotEqual(plus_score["heldout_sha256"], minus_score["heldout_sha256"])
        self.assertEqual(self.frozen.to_dict(), before)
        self.assertEqual(fit(self.plan, tuple(reversed(self.training))), self.frozen)
        with self.assertRaises(FrozenInstanceError):
            self.frozen.results = ()
        with self.assertRaises(FrozenInstanceError):
            self.frozen.results[0].point_probability = F(1)
        before["results"][0]["point_probability"] = "1"
        self.assertEqual(self.frozen.results[0].point_probability, F(1, 2))

    def test_scoring_rejects_training_or_incomplete_foreign_heldout_records(self):
        heldout = observations(self.plan, axes=("W",), split="heldout")
        for rows in (
            self.training,
            heldout[:-1],
            heldout + (heldout[0],),
            (replace(heldout[0], calibration_id="other"),) + heldout[1:],
        ):
            with self.subTest(length=len(rows)), self.assertRaises(InferenceRefusal):
                score(self.frozen, rows)
        with self.assertRaises(InferenceRefusal):
            score(self.frozen.to_dict(), heldout)

    def test_training_and_future_error_budgets_stay_separate(self):
        plan = make_plan(
            calibration=F(1, 100),
            drift=F(1, 50),
            future_calibration=F(3, 100),
            future_drift=F(1, 25),
        )
        result = fit(plan, observations(plan)).results[0]
        self.assertEqual(tuple(axis.eta for axis in result.axes), (F(13, 100),) * 3)
        self.assertEqual(result.ideal_probability_interval, (F(159, 500), F(341, 500)))
        self.assertEqual(result.future_probability_interval, (F(31, 125), F(94, 125)))
        self.assertEqual(result.frozen_frequency_band, (F(37, 250), F(213, 250)))
        self.assertEqual(result.trace_radius_squared, F(507, 10000))


if __name__ == "__main__":
    unittest.main()
