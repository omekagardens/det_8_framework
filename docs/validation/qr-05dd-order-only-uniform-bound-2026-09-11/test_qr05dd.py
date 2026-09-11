"""Bounded tests for QR-05DD (order-only longest-chain uniform bound).

Claims are covered by brute-force known answers for the longest chain, a
hand-computed distortion, and the integrated report with both routes.
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
    return _load("_qr05dd_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dd_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dd_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


def brute_chain(points):
    """O(n^3) longest-chain table (link lengths) for cross-checking."""
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                dx = points[j][1] - points[i][1]
                if dt > 0 and dt * dt > dx * dx:
                    prec[i][j] = True
    order = sorted(range(n), key=lambda i: points[i][0])
    chain = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            best = -1
            for i in range(n):
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > best:
                    best = dist[i] + 1
            if best > dist[j]:
                dist[j] = best
        chain[src] = [v if v > 0 else 0 for v in dist]
    return chain, prec


class OrderOnlyUniformBoundTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    # ---- T1/T3 convergence -------------------------------------------------

    def test_ceiling_is_a_power_law_that_vanishes(self):
        self.assertTrue(self.report["flags"]["ceiling_is_a_power_law"])
        self.assertTrue(self.report["flags"]["order_only_uniform_bound_vanishes"])
        fit = self.report["fit"]
        self.assertGreater(fit["alpha"], 0.1)
        self.assertGreater(fit["r_squared"], 0.9)

    def test_fit_is_consistent_with_the_lpp_prediction(self):
        self.assertTrue(self.report["flags"]["ceiling_consistent_with_lpp_prediction"])
        self.assertAlmostEqual(self.report["fit"]["predicted_alpha_lpp"], 1.0 / 3.0, places=9)
        self.assertLess(abs(self.report["fit"]["alpha"] - 1.0 / 3.0), 0.12)

    def test_ceiling_does_not_plateau(self):
        self.assertTrue(self.report["flags"]["ceiling_does_not_plateau"])
        by_n = self.report["by_n"]
        ns = sorted(int(k) for k in by_n)
        values = [by_n[str(n)] for n in ns]
        self.assertEqual(values, sorted(values, reverse=True))  # monotonically decreasing
        self.assertLess(values[-1], 0.7 * values[0])

    def test_nonmanifoldlike_control_does_not_vanish(self):
        self.assertTrue(self.report["flags"]["nonmanifoldlike_control_does_not_vanish"])
        control = self.report["control"]
        self.assertTrue(control["does_not_vanish"])
        self.assertGreater(control["ceiling_norm"], 0.5)

    def test_unconditional_proof_is_not_claimed(self):
        self.assertFalse(self.report["flags"]["unconditional_proof_established"])
        self.assertIn("LPP concentration", self.report["verdict"])

    # ---- known answers -----------------------------------------------------

    def test_longest_chain_matches_a_brute_force_table(self):
        import importlib.util as _u
        spec = _u.spec_from_file_location("_t7", HERE / "../../../det8/models/order_count_geometry.py")
        t7 = _u.module_from_spec(spec)
        with mock.patch.dict(sys.modules, {"_t7": t7}):
            spec.loader.exec_module(t7)
        for n in (24, 40):
            points = t7.sprinkle_diamond(2, n, seed=3)
            chain, prec = brute_chain(points)
            ref_values = sorted(chain[i][j] for i in range(n) for j in range(n) if prec[i][j])
            for module in (primary_module(), reference_module()):
                lengths, _taus = module.longest_chain_pairs(points)
                self.assertEqual(sorted(lengths), ref_values, module.__name__)
            # The light-cone dominance order is exactly the causal order.
            us = [p[0] - p[1] for p in points]
            vs = [p[0] + p[1] for p in points]
            for i in range(n):
                for j in range(n):
                    self.assertEqual(prec[i][j], us[i] < us[j] and vs[i] < vs[j])

    def test_distortion_known_answer(self):
        primary = primary_module()
        # Aligned data: zero distortion at c = 1.
        _c, dist, med = primary.distortion([1.0, 2.0], [1.0, 2.0], 80)
        self.assertAlmostEqual(dist, 0.0, places=9)
        # L = [1, 3], tau = [1, 2]: the minimax is 1/3 at c = 4/3.
        _c, dist, _med = primary.distortion([1.0, 3.0], [1.0, 2.0], 80)
        self.assertAlmostEqual(dist, 1.0 / 3.0, places=6)

    def test_reduction_consistency(self):
        # ceiling_links = ceiling_norm * mean_L (the reduction delta = ell * U).
        for row in self.report["convergence"]:
            self.assertAlmostEqual(row["ceiling_links"], row["ceiling_norm"] * row["mean_L"],
                                   places=6)

    def test_median_is_below_the_ceiling(self):
        for row in self.report["convergence"]:
            self.assertLessEqual(row["median_norm"], row["ceiling_norm"] + 1e-9)

    # ---- provenance --------------------------------------------------------

    def test_primary_reference_agree(self):
        _protocol, left, right = self.study.analyze_native()
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
        self.assertEqual(capture["schema"], "qr05dd-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
