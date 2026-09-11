"""Bounded tests for QR-05DC (max-plus closure; order-domination of the uniform
bound).  Claims are covered by hand-computed known answers, the integrated report,
and the two-route agreement check.
"""

from __future__ import annotations

import importlib.util
import json
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
    return _load("_qr05dc_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dc_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dc_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class MaxPlusClosureTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def rows(self, estimator):
        return [r for r in self.report["axiom_checks"] if r["estimator"] == estimator]

    # ---- T1 existence and axiom compliance ---------------------------------

    def test_closure_satisfies_the_lorentzian_axioms(self):
        self.assertTrue(self.report["flags"]["closure_satisfies_all_axioms"])
        self.assertTrue(self.report["flags"]["axiom_compliant_mixed_reconstruction_exists"])
        for row in self.rows("closure_a1"):
            self.assertEqual(row["support_mismatches"], 0)
            self.assertEqual(row["zero_on_causal"], 0)
            self.assertEqual(row["reverse_triangle_violations"], 0)

    def test_chain_satisfies_the_lorentzian_axioms(self):
        self.assertTrue(self.report["flags"]["chain_satisfies_all_axioms"])
        for row in self.rows("chain"):
            self.assertEqual(row["support_mismatches"], 0)
            self.assertEqual(row["reverse_triangle_violations"], 0)

    def test_count_violates_the_reverse_triangle(self):
        self.assertTrue(self.report["flags"]["count_violates_reverse_triangle"])
        self.assertTrue(any(r["reverse_triangle_violations"] > 0 for r in self.rows("count")))

    # ---- T2 pointwise domination and T3 order-domination -------------------

    def test_closure_dominates_the_weighted_longest_chain(self):
        self.assertTrue(self.report["flags"]["closure_dominates_the_weighted_longest_chain"])
        self.assertTrue(all(r["domination_violations"] == 0 for r in self.report["domination"]))

    def test_closure_tracks_the_chain(self):
        self.assertTrue(self.report["flags"]["closure_a1_tracks_the_chain"])
        for row in self.report["sweep"]:
            self.assertLessEqual(abs(row["closure_by_weight"]["1.0"] - row["chain"]),
                                 0.05 * row["chain"])

    def test_closure_never_beats_the_count_ceiling(self):
        self.assertTrue(self.report["flags"]["closure_never_beats_the_count_ceiling"])
        for row in self.report["sweep"]:
            self.assertGreater(row["best_closure"], row["count"])
            self.assertLess(row["count"], row["chain"])  # the count's ceiling is smaller

    def test_tuned_weight_does_not_recover_the_count_ceiling(self):
        self.assertFalse(self.report["flags"]["tuned_link_weight_recovers_the_count_ceiling"])
        self.assertTrue(self.report["flags"]["mixed_uniform_bound_reduces_to_order_only"])
        for row in self.report["sweep"]:
            for weight, value in row["closure_by_weight"].items():
                self.assertGreater(value, row["count"], weight)

    # ---- known answers -----------------------------------------------------

    def test_closure_known_answers(self):
        # 0 -> {1,2,3,4}; 1 -> 4; 2 -> {3,4}; 3 -> 4.  Colouring: 0->2->3->4 is
        # the longest chain (3 links); 0->1->4 is 2.
        rel = {0: {1, 2, 3, 4}, 1: {4}, 2: {3, 4}, 3: {4}, 4: set()}
        prec = [[j in rel[i] for j in range(5)] for i in range(5)]
        order = list(range(5))
        for module in (primary_module(), reference_module()):
            w = [[1.0 if prec[i][j] else 0.0 for j in range(5)] for i in range(5)]
            D = module.closure(prec, order, w)
            L = module.chain_matrix(prec, order)
            # Constant weight: the closure equals the longest-chain estimator.
            self.assertEqual(D, [[float(L[i][j]) for j in range(5)] for i in range(5)])
            self.assertEqual(D[0][4], 3.0)
            # Positive weights only on causal pairs; superadditive (A2) exactly.
            self.assertEqual(module.reverse_triangle_census(D, prec, 1e-9)[0], 0)
            self.assertTrue(all(D[i][j] >= w[i][j] - 1e-12
                                for i in range(5) for j in range(5)))

    def test_closure_is_superadditive_on_a_weighted_poset(self):
        # One big edge 0 -> 2 (weight 5) forces the closure 0 -> 4 to route through 2.
        rel = {0: {1, 2, 3, 4}, 1: {4}, 2: {3, 4}, 3: {4}, 4: set()}
        prec = [[j in rel[i] for j in range(5)] for i in range(5)]
        w = [[1.0 if prec[i][j] else 0.0 for j in range(5)] for i in range(5)]
        w[0][2] = 5.0
        D = primary_module().closure(prec, list(range(5)), w)
        self.assertEqual(D[0][4], 7.0)  # 5 + 1 + 1
        self.assertGreater(D[0][4], D[0][2] + D[2][4] - 1e-12)

    # ---- claims and provenance ---------------------------------------------

    def test_no_metric_claim_and_verdict_scope(self):
        self.assertIn("no metric", self.report["verdict"].lower())
        self.assertIn("order-only", self.report["verdict"])

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
        self.assertEqual(capture["schema"], "qr05dc-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
