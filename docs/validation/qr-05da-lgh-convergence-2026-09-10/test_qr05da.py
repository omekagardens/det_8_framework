"""Bounded tests for the QR-05DA scale-free LGH convergence gate.

The percentile statistics in the first DA capture selected the *1st* percentile
(index ``int(0.01 n)``) under the name ``p99``. Beyond re-testing the trend this
module pins the corrected statistics with *known-answer* checks, so two
implementations cannot agree on the same conceptual error.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import unittest
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def load_study():
    return _load("_qr05da_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05da_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05da_test_reference", HERE / "reference.py")


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
        self.assertGreater(decay["chain_median"], decay["chain_upper"])

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
        self.assertTrue(self.report["flags"]["count_median_decays_faster_than_chain_median"])
        self.assertTrue(self.report["flags"]["count_p99_decays_faster_than_chain_p99"])
        self.assertGreater(decay["count_upper"], decay["chain_upper"])
        self.assertGreater(decay["count_median"], decay["chain_median"])
        crossover = self.report["flags"]["count_below_chain_from_n"]
        self.assertIsNotNone(crossover)
        self.assertLessEqual(crossover, 256)

    # ---- corrected-statistic tests (the p01 -> p99 repair) -----------------

    def test_p99_is_an_upper_tail_statistic_not_the_lower_tail(self):
        # Regression guard for the repaired defect. The first capture's "p99"
        # (index int(0.01 n)) sat *below* the median at every size; the correct
        # 99th percentile sits between the median and the ceiling.
        for row in self.report["trend"]:
            if row["n"] < 32:
                continue
            self.assertGreaterEqual(row["chain_p99_mean"], row["chain_median_mean"])
            self.assertGreaterEqual(row["count_p99_mean"], row["count_median_mean"])
            self.assertLessEqual(row["chain_p99_mean"], row["chain_upper_mean"] + 1e-9)
            self.assertLessEqual(row["count_p99_mean"], row["count_upper_mean"] + 1e-9)

    def test_corrected_p99_is_not_essentially_exact(self):
        # The superseded capture claimed count p99 < 1e-2 for N >= 32; the true
        # 99th percentile is O(0.1). Pin that, so the claim cannot resurface.
        by_n = {row["n"]: row for row in self.report["trend"]}
        self.assertGreater(by_n[512]["chain_p99_mean"], 0.1)
        self.assertGreater(by_n[512]["count_p99_mean"], 0.05)

    def test_count_is_below_the_chain_on_every_statistic_in_the_asymptotic_range(self):
        for row in self.report["trend"]:
            if row["n"] < 64:
                continue
            self.assertLess(row["count_median_mean"], row["chain_median_mean"])
            self.assertLess(row["count_p99_mean"], row["chain_p99_mean"])
            self.assertLess(row["count_upper_mean"], row["chain_upper_mean"])

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

    # ---- known-answer statistics and the count estimator -------------------

    def test_quantile_helpers_have_known_answers(self):
        # Explicit samples with hand-computed nearest-rank quantiles. The bug
        # being repaired would return the 1st percentile here.
        for module in (primary_module(), reference_module()):
            values = list(range(1, 101))  # 1..100
            self.assertEqual(module._p99(values), 99)          # index ceil(99)-1 = 98
            self.assertEqual(module._median(values), 50)        # index 49
            self.assertEqual(module._quantile(values, 0.01), 1)  # the old value
            self.assertNotEqual(module._p99(values), module._quantile(values, 0.01))
            sample = [i / 10000.0 for i in range(10000)]        # 0.0000 .. 0.9999
            self.assertAlmostEqual(module._p99(sample), 0.9899, places=9)
            self.assertAlmostEqual(module._median(sample), 0.4999, places=9)

    def test_decay_fit_has_a_known_answer(self):
        xs = [2 ** k for k in range(2, 10)]
        ys = [x ** -0.5 for x in xs]  # an exact power law
        self.assertAlmostEqual(primary_module()._loglog_slope(xs, ys), -0.5, places=12)
        self.assertAlmostEqual(reference_module()._slope(xs, ys), -0.5, places=12)

    def test_count_estimator_is_not_a_lorentzian_metric_on_a_chain(self):
        # a ≺ b ≺ c, consecutive links: m_ab = m_bc = 0, m_ac = 1.
        primary = primary_module()
        points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
        order = sorted(range(3), key=lambda i: points[i][0])
        prec = primary.causality(points)
        counts = primary.interval_counts(prec, order)
        self.assertEqual(counts[0][1], 0)
        self.assertEqual(counts[1][2], 0)
        self.assertEqual(counts[0][2], 1)
        d = primary.count_separation(prec, counts, 1.0)
        # The true directed Lorentzian distance satisfies the reverse triangle.
        tau = primary.tau_directed(points)
        self.assertGreaterEqual(tau[0][2], tau[0][1] + tau[1][2] - 1e-12)
        # The count estimator does not: d(a,c) = sqrt(2) < d(a,b)+d(b,c) = 2.
        self.assertAlmostEqual(d[0][2], math.sqrt(2.0))
        self.assertLess(d[0][2], d[0][1] + d[1][2])
        # It still has the estimator's support property: positive exactly on ≺.
        for i in range(3):
            for j in range(3):
                self.assertEqual(d[i][j] > 0.0, prec[i][j])
        # Both routes build the same estimator.
        self.assertEqual(d, reference_module()._count_separation(prec, counts, 1.0))

    def test_primary_reference_agree(self):
        _, left, right = self.study.analyze_native()
        self.assertTrue(self.study.equivalent(left, right))
        self.assertEqual(self.study.encode(left), self.report)

    def test_source_byte_limit(self):
        limit = self.protocol["limits"]["source_bytes"]
        for name in self.study.SOURCE_PATHS:
            self.assertLessEqual((HERE / name).stat().st_size, limit, name)

    def test_superseded_capture_is_preserved(self):
        path = HERE / "results.superseded-p01-v1.json"
        self.assertTrue(path.exists(), "the superseded p01 capture must be retained")
        old = json.loads(path.read_bytes())
        self.assertEqual(old["schema"], "qr05da-capture-v1")
        old_by_n = {row["n"]: row for row in old["report"]["trend"]}
        # The superseded "p99" was the 1st percentile; the corrected one is O(0.1).
        self.assertLess(old_by_n[512]["chain_p99_mean"], 0.01)
        by_n = {row["n"]: row for row in self.report["trend"]}
        self.assertGreater(by_n[512]["chain_p99_mean"], 0.1)

    def test_capture_matches_if_present(self):
        path = HERE / "results.json"
        if not path.exists():
            self.skipTest("capture not generated yet")
        capture = json.loads(path.read_bytes())
        self.assertEqual(capture["schema"], "qr05da-capture-v2")
        self.assertIn("results.superseded-p01-v1.json", capture["supersedes"])
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
