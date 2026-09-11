"""Bounded tests for the QR-05CY observational quotient and no-go."""

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
    spec = importlib.util.spec_from_file_location("_qr05cy_test_study", HERE / "study.py")
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


def probe(report, interface):
    return next(item for item in report["probes"] if item["interface"] == interface)


class ObservationalQuotientTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_dimension_factors_through_the_quotient(self):
        self.assertEqual(probe(self.report, "order")["verdict"], "IDENTIFIED")

    def test_absolute_scale_is_not_identifiable_from_the_same_channel(self):
        item = probe(self.report, "scaled_distance")
        self.assertEqual(item["verdict"], "NON_IDENTIFIABLE")
        self.assertEqual(item["witness"], ["scale1", "scale2"])

    def test_an_independent_anchor_resolves_absolute_scale(self):
        self.assertEqual(probe(self.report, "scaled_distance+anchor")["verdict"], "IDENTIFIED")
        self.assertTrue(self.report["external_anchor_resolves"])

    def test_order_is_blind_to_the_conformal_factor(self):
        item = probe(self.report, "order_signs")
        self.assertEqual(item["verdict"], "NON_IDENTIFIABLE")
        self.assertEqual(item["witness"], ["omega0.0", "omega2.0"])

    def test_counts_identify_the_conformal_factor(self):
        self.assertEqual(probe(self.report, "counts")["verdict"], "IDENTIFIED")

    def test_internal_reference_no_go(self):
        no_go = self.report["internal_reference_no_go"]
        self.assertTrue(no_go["targets_differ"])
        self.assertTrue(no_go["all_blind"])
        self.assertTrue(no_go["reference_family"])

    def test_taxonomy_uses_the_existing_registry(self):
        self.assertFalse(self.report["taxonomy"]["new_status_introduced"])
        self.assertEqual(self.report["taxonomy"]["validated_against"], "det8.claims")
        claims = self.study.load_module("_qr05cy_test_claims",
                                        HERE / "../../../det8/claims.py")
        registered = {
            claims.VERIFIED_SOFTWARE_CONTRACT, claims.NOT_YET_VALIDATED,
            claims.BOUNDED_CONDITIONAL_RESULT, claims.CORRESPONDENCE_ONLY,
            claims.NO_EMPIRICAL_SUPPORT, claims.NOT_APPLICABLE,
        }
        for entry in self.report["taxonomy"]["mapping"].values():
            self.assertIn(entry["evidence_status"], registered)
            self.assertIn(entry["blockage"], {"DATA", "CHANNEL", "MATH", "GAUGE"})

    def test_makes_no_ontological_claim(self):
        self.assertFalse(self.report["ontological_claim"])
        self.assertIn("Status M", self.report["status_m_guard"])
        p5 = next(p for p in self.report["propositions"] if p["id"] == "P5")
        self.assertEqual(p5["status"], "governance_status_m")

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
        self.assertEqual(capture["schema"], "qr05cy-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
