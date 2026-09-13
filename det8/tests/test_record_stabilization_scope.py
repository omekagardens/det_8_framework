"""Regression checks for the classical copying/stabilization claim boundary.

These preserve the historical numerical APIs. They do not certify a physical
first-record mechanism, a decoherence rate, or a full quantum reconstruction.
"""

from __future__ import annotations

import math
import random
import unittest
from fractions import Fraction
from unittest.mock import patch

from det8.models.det_native_measurement import (
    MeasurementApparatus,
    TargetSystem,
    compare_det_vs_qm_measurement,
    det_native_measure,
    det_native_measurement_event,
)
from det8.models.record_formation import (
    chernoff_exponent,
    derivation_certificate,
    record_error_bound,
    redundancy_decay,
    run_t3,
)


class ClassicalStabilizationTests(unittest.TestCase):
    def test_known_chernoff_arithmetic_is_unchanged(self) -> None:
        # At p=4/5, 2 sqrt(p(1-p)) = 4/5 exactly.
        self.assertAlmostEqual(chernoff_exponent(0.8), -math.log(0.8))
        self.assertAlmostEqual(record_error_bound(5, 0.8), 0.8**5)

    def test_finite_classical_majority_error_is_below_the_bound(self) -> None:
        p = Fraction(4, 5)
        exact_error = sum(
            (
                math.comb(5, successes) * p**successes * (1 - p) ** (5 - successes)
                for successes in range(3)
            ),
            Fraction(0),
        )
        self.assertEqual(exact_error, Fraction(181, 3125))
        self.assertLess(float(exact_error), record_error_bound(5, float(p)))

    def test_existing_bound_domain_checks_are_preserved(self) -> None:
        for p in (0.5, 1.0, math.nan):
            with self.subTest(p=p), self.assertRaises(ValueError):
                chernoff_exponent(p)
        with self.assertRaises(ValueError):
            record_error_bound(0, 0.8)

    def test_redundancy_table_tracks_copy_count_not_first_record_selection(self) -> None:
        rows = redundancy_decay(0.8, N_max=5, step=2)
        self.assertEqual([row["N"] for row in rows], [1, 3, 5])
        self.assertGreater(rows[0]["bound"], rows[1]["bound"])
        self.assertGreater(rows[1]["bound"], rows[2]["bound"])
        for row in rows:
            self.assertAlmostEqual(row["bound"], 0.8 ** row["N"])
            self.assertAlmostEqual(row["exponent"], -math.log(0.8))

    def test_certificate_explicitly_excludes_unproved_formation_claims(self) -> None:
        certificate = derivation_certificate()
        self.assertEqual(certificate["status"], "CONDITIONAL_CLASSICAL_STABILIZATION")
        self.assertIn("Stabilization", certificate["theorem"])
        required_exclusions = {
            "first_record_formation",
            "quantum_decoherence_rate",
            "physical_irreversibility",
            "record_production_rate",
        }
        self.assertLessEqual(required_exclusions, set(certificate["exclusions"]))
        notes = " ".join(certificate["notes"]).lower()
        self.assertIn("assumed", notes)
        self.assertIn("independent", notes)
        self.assertTrue(any("MATH" in item for item in certificate["deliverables"].values()))

    def test_runner_keeps_certificate_and_diagnostic_scope(self) -> None:
        # Avoid a large stochastic check: only exercise the runner's reporting
        # contract here. The preceding test evaluates an exact binomial case.
        with patch("det8.models.record_formation.majority_vote_error", return_value=0.0) as mc:
            report = run_t3(p=0.8, seed=7)
        self.assertEqual(mc.call_count, 3)
        self.assertEqual(report["certificate"], derivation_certificate())
        self.assertEqual(report["p"], 0.8)
        self.assertAlmostEqual(report["exponent_C"], -math.log(0.8))
        interpretation = report["interpretation"].lower()
        self.assertIn("not a proof", interpretation)
        self.assertIn("assumed target", interpretation)
        self.assertIn("first-record formation is not derived", interpretation)


class ClassicalPointerCopyingTests(unittest.TestCase):
    def test_perfect_fidelity_copies_either_supplied_target(self) -> None:
        for value in (0, 1):
            with self.subTest(value=value):
                target = TargetSystem(value)
                apparatus = MeasurementApparatus(n_bits=3)
                event = det_native_measurement_event(
                    target, apparatus, fidelity=1.0, rng=random.Random(11)
                )
                self.assertEqual(event["outcome"], value)
                self.assertTrue(event["correct"])
                self.assertEqual(event["target_value"], value)
                self.assertEqual(sum(event["kernel"]), 1.0)
                self.assertEqual(event["kernel"][value], 1.0)
                self.assertEqual(target.value, value)
                self.assertEqual(apparatus.committed_count, 1)
                self.assertEqual(apparatus.pointer_value, value)

    def test_zero_fidelity_is_deterministic_inversion_not_quantum_randomness(self) -> None:
        for value in (0, 1):
            with self.subTest(value=value):
                apparatus = MeasurementApparatus(n_bits=1)
                event = det_native_measurement_event(
                    TargetSystem(value), apparatus, fidelity=0.0, rng=random.Random(11)
                )
                self.assertEqual(event["outcome"], 1 - value)
                self.assertFalse(event["correct"])
                self.assertEqual(apparatus.pointer_value, 1 - value)

    def test_full_apparatus_does_not_add_or_rewrite_a_copy(self) -> None:
        apparatus = MeasurementApparatus(n_bits=2)
        target = TargetSystem(1)
        rng = random.Random(3)
        det_native_measurement_event(target, apparatus, fidelity=1.0, rng=rng)
        det_native_measurement_event(target, apparatus, fidelity=1.0, rng=rng)
        before = tuple(bit.value for bit in apparatus.bits)
        event = det_native_measurement_event(TargetSystem(0), apparatus, fidelity=1.0, rng=rng)
        self.assertTrue(event["apparatus_full"])
        self.assertEqual(event["event"], "no_uncommitted_bits")
        self.assertEqual(tuple(bit.value for bit in apparatus.bits), before)
        self.assertEqual(apparatus.committed_count, 2)

    def test_pointer_none_and_tie_semantics_are_preserved(self) -> None:
        apparatus = MeasurementApparatus(n_bits=2)
        self.assertIsNone(apparatus.pointer_value)
        self.assertEqual(apparatus.pointer_strength, 0.0)
        apparatus.bits[0].value = 0
        apparatus.bits[1].value = 1
        self.assertIsNone(apparatus.pointer_value)
        self.assertEqual(apparatus.pointer_strength, 0.0)
        self.assertEqual(apparatus.committed_count, 2)

    def test_full_sequence_keeps_deterministic_copying_statistics(self) -> None:
        report = det_native_measure(target_value=1, n_bits=5, fidelity=1.0, seed=12)
        self.assertTrue(report["correct"])
        self.assertEqual(report["committed_count"], 5)
        self.assertEqual(report["pointer_value"], 1)
        self.assertEqual(report["pointer_strength"], 1.0)
        self.assertEqual(report["redundancy"], 5.0)
        self.assertEqual(report["pointer_trace"], [1.0] * 5)
        self.assertTrue(all(event["correct"] for event in report["history_sample"]))

    def test_comparison_retains_explicit_classical_and_interpretive_limits(self) -> None:
        comparison = compare_det_vs_qm_measurement()
        self.assertEqual(comparison["status"], "CLASSICAL_RECORD_COPYING_ONLY")
        native = comparison["det_native"]
        quantum = comparison["standard_qm"]
        self.assertIn("assumed", native["target_ontology"].lower())
        self.assertIn("classical", native["target_ontology"].lower())
        self.assertIn("does not resolve", native["collapse"].lower())
        self.assertIn("not derived", native["preferred_basis"].lower())
        self.assertIn("instrument", quantum["measurement_process"].lower())
        self.assertIn("interpretation", quantum["collapse"].lower())
        statistics = comparison["convergence"]["statistics"].lower()
        self.assertIn("classical", statistics)
        self.assertIn("no full qm", statistics)
        self.assertIn("cross-context", statistics)
        self.assertIn("not a universal", comparison["convergence"]["ontology"].lower())


if __name__ == "__main__":
    unittest.main()
