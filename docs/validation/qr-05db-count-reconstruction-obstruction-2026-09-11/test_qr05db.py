"""Bounded tests for QR-05DB (count-reconstruction metric-axiom obstruction).

The gate's claims are covered by: a hand-computed census (known answers), the
integrated report, and the two-route agreement check.
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
    return _load("_qr05db_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05db_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05db_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class CountReconstructionObstructionTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def rows(self, estimator):
        return [r for r in self.report["axiom_checks"] if r["estimator"] == estimator]

    # ---- R3: the order-only estimator is a Lorentzian premetric -------------

    def test_chain_estimator_satisfies_the_lorentzian_axioms(self):
        self.assertTrue(self.report["flags"]["chain_satisfies_all_axioms"])
        for row in self.rows("chain"):
            self.assertEqual(row["support_mismatches"], 0)
            self.assertEqual(row["zero_on_causal"], 0)
            self.assertEqual(row["reverse_triangle_violations"], 0)
            self.assertIsNone(row["witness"])
            self.assertGreaterEqual(row["worst_gap"], 0.0)

    # ---- R1: the QR-05DA count estimator is not a metric --------------------

    def test_count_offset_support_is_exact_but_reverse_triangle_fails(self):
        self.assertTrue(self.report["flags"]["count_offset_support_exact"])
        self.assertTrue(self.report["flags"]["count_offset_violates_reverse_triangle"])
        offending = [r for r in self.rows("count_offset") if r["reverse_triangle_violations"] > 0]
        self.assertTrue(offending, "expected at least one count-offset violation")
        for row in offending:
            self.assertIsNotNone(row["witness"])
            self.assertLess(row["worst_gap"], 0.0)

    def test_raw_count_fails_causal_support_on_links(self):
        self.assertTrue(self.report["flags"]["count_raw_fails_causal_support"])
        for row in self.rows("count_raw"):
            links = row["zero_on_causal"]
            self.assertGreaterEqual(links, 0)
        # At least one object has links (m = 0) that the raw form sends to zero.
        self.assertTrue(any(r["zero_on_causal"] > 0 for r in self.rows("count_raw")))
        self.assertTrue(self.report["flags"]["count_raw_reverse_triangle_fails_at_d2"])

    # ---- R2/R4: the trade-off and its structural mechanism ------------------

    def test_three_chain_witness_is_exact(self):
        w = self.report["three_chain"]
        self.assertEqual(w["counts"], {"m_ab": 0, "m_bc": 0, "m_ac": 1})
        self.assertAlmostEqual(w["count_offset"]["d_ac"], math.sqrt(2.0))
        self.assertFalse(w["count_offset"]["reverse_triangle_holds"])
        self.assertEqual(w["count_raw"]["d_ab"], 0.0)
        self.assertEqual(w["count_raw"]["d_bc"], 0.0)
        self.assertTrue(w["count_raw"]["reverse_triangle_holds"])
        self.assertTrue(w["chain"]["reverse_triangle_holds"])
        self.assertAlmostEqual(w["chain"]["L_ac"], 2.0)
        self.assertTrue(w["tau"]["reverse_triangle_holds"])

    def test_link_triple_violation_bound(self):
        b = self.report["link_triple_bound"]
        self.assertLess(b["gap_by_m_ac"]["1"], 0.0)
        self.assertLess(b["gap_by_m_ac"]["2"], 0.0)
        self.assertEqual(b["gap_by_m_ac"]["3"], 0.0)
        self.assertAlmostEqual(b["worst_lower_bound_on_unit_ell"], math.sqrt(2.0) - 2.0)

    def test_structural_superadditivity_lemma(self):
        lemma = self.report["structural_lemma"]
        self.assertEqual(lemma["violations"], 0)
        self.assertGreater(lemma["triples"], 0)
        self.assertEqual(lemma["objects_checked"], 7)

    # ---- known-answer census on a hand-built three-chain --------------------

    def test_axiom_census_known_answers(self):
        for module in (primary_module(), reference_module()):
            prec = [[False, True, True], [False, False, True], [False, False, False]]
            offset = [[0.0, 1.0, math.sqrt(2.0)], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
            rt = module.reverse_triangle_census(offset, prec, 1e-9)
            self.assertEqual(rt["reverse_triangle_violations"], 1)
            self.assertEqual(rt["triples"], 1)
            self.assertEqual(rt["witness"], [0, 1, 2])
            self.assertAlmostEqual(rt["worst_gap"], math.sqrt(2.0) - 2.0)
            self.assertEqual(
                module.support_census(offset, prec, 1e-9)["support_mismatches"], 0)
            raw = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
            raw_support = module.support_census(raw, prec, 1e-9)
            self.assertEqual(raw_support["support_mismatches"], 2)
            self.assertEqual(raw_support["zero_on_causal"], 2)
            chain = [[0.0, 1.0, 2.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
            self.assertEqual(
                module.reverse_triangle_census(chain, prec, 1e-9)["reverse_triangle_violations"], 0)

    def test_chain_superadditivity_is_strict_off_the_longest_path(self):
        # 0 -> 1 -> 4 and 0 -> 2 -> 3 -> 4: the longest 0->4 chain (3) avoids 1,
        # so L(0,1) + L(1,4) = 2 < 3 = L(0,4) -- a strict, valid superadditivity.
        rel = {0: {1, 2, 3, 4}, 1: {4}, 2: {3, 4}, 3: {4}, 4: set()}
        prec = [[j in rel[i] for j in range(5)] for i in range(5)]
        primary = primary_module()
        L = primary.chain_estimator(prec, list(range(5)), 1.0)
        self.assertEqual(L[0][4], 3.0)
        self.assertEqual(L[0][1] + L[1][4], 2.0)
        self.assertEqual(primary.reverse_triangle_census(L, prec, 1e-9)["reverse_triangle_violations"], 0)

    # ---- claims and provenance ---------------------------------------------

    def test_no_metric_claim_and_verdict_scope(self):
        self.assertFalse(self.report["flags"]["count_only_metric_established"])
        self.assertIn("no metric", self.report["verdict"].lower())
        self.assertIn("count-only", self.report["verdict"])

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
        self.assertEqual(capture["schema"], "qr05db-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
