"""Bounded tests for the QR-05CN T7/T5 compatibility witness."""

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
    spec = importlib.util.spec_from_file_location("_qr05cn_test_study", HERE / "study.py")
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


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_derived_kernel_is_compatible(self):
        self.assertGreaterEqual(self.report["corr_derived"], self.protocol["corr_high"])

    def test_independent_kernel_is_not_compatible(self):
        self.assertLessEqual(self.report["corr_control"], self.protocol["corr_low"])

    def test_verdict_is_compatible(self):
        self.assertTrue(self.report["compatible"])

    def test_profiles_are_well_formed(self):
        for key in ("t7_profile", "t5_kernel_profile", "control_profile"):
            self.assertEqual(len(self.report[key]), self.protocol["bins"])

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
        self.assertEqual(capture["schema"], "qr05cn-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
