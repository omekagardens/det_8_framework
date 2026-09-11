"""Bounded tests for the QR-05CJ metric-acceptance benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05cj_test_study", HERE / "study.py")
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


class MetricAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_conformal_factor_recovered_from_counts(self):
        block = self.report["conformal_recovery"]
        self.assertLess(block["mse"], self.protocol["mse_tolerance"])
        self.assertEqual(len(block["recovered"]), self.protocol["bins"])

    def test_order_is_conformal_invariant(self):
        self.assertTrue(self.report["order_invariant"])

    def test_scale_is_not_identified(self):
        # The normalized count profile cannot distinguish Omega^2 from c*Omega^2.
        self.assertTrue(self.report["scale_invariant"])

    def test_order_covariant_under_boost(self):
        block = self.report["boost"]
        self.assertGreater(block["total"], 0)
        self.assertTrue(block["order_preserved"])
        self.assertEqual(block["preserved"], block["total"])

    def test_non_conformal_control_fails(self):
        control = self.report["negative_control"]
        self.assertTrue(control["control_required"])

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
        self.assertEqual(capture["schema"], "qr05cj-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
