"""Bounded tests for the QR-05DA scale-free LGH convergence gate."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05da_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load study driver")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class LHGConvergenceTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_directed_distance_matches_the_chain_support(self):
        self.assertTrue(all(v == 0 for v in self.report["convention"]["chain_vs_directed"].values()))

    def test_symmetric_counterpart_is_still_detected_as_a_defect(self):
        mismatches = self.report["convention"]["chain_vs_symmetric"]
        self.assertTrue(all(v > 0 for v in mismatches.values()))
        self.assertEqual(mismatches[str(self.protocol["convention_n"][0])], 18)

    def test_count_offset_matches_directed_and_raw_count_does_not(self):
        self.assertTrue(all(v == 0 for v in self.report["convention"]["count_offset_vs_directed"].values()))
        raw = self.report["convention"]["count_raw_vs_directed"]
        self.assertTrue(all(v > 0 for v in raw.values()))
        self.assertTrue(self.report["flags"]["count_support_matches_directed"])

    def test_chain_lower_bound_decays_steadily(self):
        means = [row["chain_lower_mean"] for row in self.report["trend"]]
        self.assertEqual(means, sorted(means, reverse=True))
        self.assertGreater(self.report["decay"]["chain_lower"], 0.25)

    def test_chain_ceiling_decays_much_slower_than_the_lower_bound(self):
        decay = self.report["decay"]
        self.assertTrue(self.report["flags"]["chain_ceiling_decays_slowly"])
        self.assertLess(decay["chain_upper"], decay["chain_lower"] / 2.0)
        self.assertGreater(decay["chain_p99"], decay["chain_upper"])

    def test_ceiling_is_localized_to_large_proper_time(self):
        self.assertTrue(self.report["flags"]["ceiling_is_at_large_proper_time"])
        by_bucket = {row["bucket"]: row["mean_abs"] for row in self.report["localization"]}
        self.assertGreater(by_bucket["2^3..2^4"], by_bucket["lt_2^-4"])
        self.assertGreater(by_bucket["2^2..2^3"], by_bucket["2^-2..2^-1"])

    def test_chain_length_ratio_converges_to_a_constant(self):
        # For large proper time the longest-chain ratio L/(tau/ell) stabilises
        # (the scale absorbs the constant) while its relative spread shrinks.
        by_bucket = {row["bucket"]: row for row in self.report["localization"]}
        for bucket in ("2^2..2^3", "2^3..2^4", "2^4..2^5"):
            self.assertGreater(by_bucket[bucket]["ratio_mean"], 1.1)
            self.assertLess(by_bucket[bucket]["ratio_mean"], 1.4)
        self.assertLess(by_bucket["2^4..2^5"]["ratio_sd"], by_bucket["2^0..2^1"]["ratio_sd"])

    def test_count_reconstruction_decays_faster_and_crosses_over(self):
        decay = self.report["decay"]
        self.assertTrue(self.report["flags"]["count_max_decays_faster_than_chain_max"])
        self.assertTrue(self.report["flags"]["count_bulk_decays_faster_than_chain_bulk"])
        self.assertGreater(decay["count_upper"], decay["chain_upper"])
        crossover = self.report["flags"]["count_below_chain_from_n"]
        self.assertIsNotNone(crossover)
        self.assertLessEqual(crossover, 256)

    def test_count_bulk_is_essentially_exact(self):
        for row in self.report["trend"]:
            if row["n"] >= 32:
                self.assertLess(row["count_p99_mean"], 0.01)
            if row["n"] >= 128:
                # Beyond the N = 64 seed-noise crossover the count bulk is below
                # the chain bulk throughout the asymptotic range.
                self.assertLess(row["count_p99_mean"], row["chain_p99_mean"])

    def test_identity_is_scale_free_optimal_on_the_exact_grid(self):
        self.assertTrue(self.report["flags"]["exact_identity_optimal"])
        for row in self.report["exact"]:
            self.assertTrue(row["identity_optimal"])
            self.assertAlmostEqual(row["scale_free_identity"], row["exact_scale_free_infimum"], places=9)

    def test_random_correspondence_is_much_worse(self):
        control = self.report["random_control"]
        self.assertGreater(control["random"], 2.0 * control["identity"])

    def test_convergence_is_not_claimed(self):
        self.assertFalse(self.report["flags"]["lgh_infimum_established"])
        self.assertIn("not established", self.report["verdict"])
        self.assertIn("estimator-specific", self.report["verdict"])

    def test_primary_reference_agree(self):
        _, left, right = self.study.analyze_native()
        self.assertTrue(self.study.equivalent(left, right))
        self.assertEqual(self.study.encode(left), self.report)

    def test_source_byte_limit(self):
        limit = self.protocol["limits"]["source_bytes"]
        for name in self.study.SOURCE_PATHS:
            self.assertLessEqual((HERE / name).stat().st_size, limit, name)

    def test_capture_matches_if_present(self):
        path = HERE / "results.json"
        if not path.exists():
            self.skipTest("capture not generated yet")
        capture = json.loads(path.read_bytes())
        self.assertEqual(capture["schema"], "qr05da-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
