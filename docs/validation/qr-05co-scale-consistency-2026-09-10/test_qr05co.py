"""Bounded tests for the QR-05CO T7/T5 scale-consistency witness."""

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
    spec = importlib.util.spec_from_file_location("_qr05co_test_study", HERE / "study.py")
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


class ScaleConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_coarse_graining_identity(self):
        self.assertTrue(self.report["coarse_graining_identity"])

    def test_geometry_is_scale_consistent(self):
        self.assertTrue(self.report["geometry_consistent"])
        self.assertLessEqual(self.report["geometry_ratio_dev"], self.protocol["ratio_tol"])

    def test_operator_is_scale_consistent(self):
        self.assertTrue(self.report["operator_consistent"])
        self.assertGreaterEqual(self.report["operator_corr"], self.protocol["corr_high"])
        self.assertAlmostEqual(self.report["operator_scale_ratio"], 1.0,
                               delta=self.protocol["ratio_tol"])

    def test_bridge_holds_at_both_scales(self):
        self.assertTrue(self.report["bridge_consistent"])
        self.assertGreaterEqual(self.report["bridge_coarse"], self.protocol["corr_high"])
        self.assertGreaterEqual(self.report["bridge_fine"], self.protocol["corr_high"])

    def test_raw_counts_are_not_scale_consistent(self):
        control = self.report["control"]
        self.assertAlmostEqual(control["raw_scale_ratio"], 2.0, delta=0.2)
        self.assertFalse(control["raw_scale_consistent"])
        self.assertAlmostEqual(control["normalized_scale_ratio"], 1.0, delta=0.05)

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
        self.assertEqual(capture["schema"], "qr05co-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
