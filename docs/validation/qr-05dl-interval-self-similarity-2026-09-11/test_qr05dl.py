"""Bounded tests for QR-05DL (interval self-similarity)."""

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
    return _load("_qr05dl_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dl_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dl_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class IntervalSelfSimilarityTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def row(self, name):
        return next(r for r in self.report["objects"] if r["object"] == name)

    def test_sprinkles_are_interval_self_similar(self):
        self.assertTrue(self.report["flags"]["sprinkles_are_interval_self_similar"])
        for r in self.report["objects"]:
            if r["object"].startswith("sprinkle_"):
                self.assertIsNotNone(r["self_similarity"])
                self.assertTrue(0.8 <= r["self_similarity"] <= 1.7, r["object"])

    def test_degenerate_counterexamples_fail(self):
        self.assertTrue(self.report["flags"]["degenerate_counterexamples_fail_interval_self_similarity"])
        self.assertEqual(self.row("bipartite_complete")["interval_density"], 0.0)
        self.assertEqual(self.row("layer_cake_k3")["intervals_sampled"], 0)
        self.assertEqual(self.row("layer_cake_k4")["intervals_sampled"], 0)

    def test_closure_dense_laws_fail_at_low_f(self):
        self.assertTrue(self.report["flags"]["closure_dense_laws_fail_interval_self_similarity_at_low_f"])
        tp = [r for r in self.report["objects"] if r["object"].startswith("transitive_percolation_")]
        self.assertTrue(any(r["self_similarity"] is not None and r["self_similarity"] > 1.7
                            for r in tp))

    def test_no_go_is_not_established_and_manifoldlikeness_is_multi_faceted(self):
        self.assertFalse(self.report["flags"]["a_no_go_is_established"])
        self.assertTrue(self.report["flags"]["manifoldlikeness_is_multi_faceted_no_single_invariant_sufficient"])
        self.assertTrue(self.report["flags"]["interval_self_similarity_is_a_higher_order_manifoldlike_invariant"])

    def test_known_answer_chain_is_self_similar(self):
        for module in (primary_module(), reference_module()):
            n = 10
            chain = [[i < j for j in range(n)] for i in range(n)]
            mean_fI, cnt, rho = module.interval_stats(chain, 3, 9, 100, 0)
            self.assertGreater(cnt, 0)
            self.assertAlmostEqual(mean_fI, 1.0, places=9)   # intervals of a chain are chains
            self.assertAlmostEqual(module.fglobal(chain), 1.0, places=9)
            self.assertAlmostEqual(mean_fI / module.fglobal(chain), 1.0, places=9)

    def test_known_answer_bipartite_has_no_intervals(self):
        for module in (primary_module(), reference_module()):
            prec = module.bipartite(50, 1.0, seed=1)
            _mean, cnt, rho = module.interval_stats(prec, 3, 30, 100, 0)
            self.assertEqual(cnt, 0)
            self.assertAlmostEqual(rho, 0.0, places=9)

    def test_known_answer_layer_cake_intervals_are_whole_layers(self):
        # A 3-layer cake's only nonempty intervals are a whole middle layer. With
        # n = 250 that layer has n//3 = 83 elements, outside the [3, 30] window, so
        # nothing is sampled, while the interval density is s0*s2 over all comparable
        # pairs (s = layer sizes).
        for module in (primary_module(), reference_module()):
            n, k = 250, 3
            prec = module.layered(n, k)
            per = n // k
            s = (per, per, n - 2 * per)
            comparable = s[0] * s[1] + s[0] * s[2] + s[1] * s[2]
            _mean, cnt, rho = module.interval_stats(prec, 3, 30, 800, 0)
            self.assertEqual(cnt, 0)
            self.assertAlmostEqual(rho, s[0] * s[2] / comparable, places=9)
            self.assertAlmostEqual(module.fglobal(prec),
                                   2.0 * comparable / (n * (n - 1)), places=9)

    def test_known_answer_interval_density_is_a_complete_sweep(self):
        # A chain of n has C(n,2) comparable pairs, of which the C(n-1,2) pairs with
        # j > i+1 have a nonempty interval, so rho = (n-2)/n exactly.  A small cap
        # must limit only the collected interval sample, never the pair sweep: the
        # original v1 capture broke the sweep at the cap and reported a partial
        # fraction (see SUPERSEDED.md).
        for module in (primary_module(), reference_module()):
            n = 10
            chain = [[i < j for j in range(n)] for i in range(n)]
            _mean, cnt, rho = module.interval_stats(chain, 3, 9, 5, 0)
            self.assertEqual(cnt, 5)
            self.assertAlmostEqual(rho, (n - 2) / n, places=12)

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
        self.assertEqual(capture["schema"], "qr05dl-capture-v2")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
