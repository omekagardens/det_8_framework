"""Bounded tests for the QR-05CE Bell-correspondence / history-distance run."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05ce_test_study", HERE / "study.py")
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


class BellCorrespondenceTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_dataset_hash(self):
        self.assertEqual(self.report["dataset_sha256"], self.protocol["dataset"]["sha256"])

    def test_grid(self):
        self.assertEqual(self.report["grid"]["beta_step"], 32)
        self.assertEqual(self.report["grid"]["alpha_steps"], 37)

    def test_chsh_visibility_witness(self):
        for curve in self.report["curves"]:
            amp = F(*curve["amplitude"])
            self.assertTrue(F(7, 10) < amp < F(9, 10), curve["id"])
            self.assertTrue(curve["chsh_witness"], curve["id"])
            self.assertTrue(F(*curve["amplitude_sq"]) > F(1, 2), curve["id"])
            self.assertGreater(curve["over_threshold_count"], 0, curve["id"])

    def test_history_distance_positive(self):
        for curve in self.report["curves"]:
            self.assertTrue(0.0 < curve["kappa"] < 1.0, curve["id"])

    def test_primary_reference_agree(self):
        _, left, right = self.study.analyze_native()
        self.assertEqual(self.study.encode(left), self.study.encode(right))
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
        self.assertEqual(capture["schema"], "qr05ce-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
