"""Bounded tests for the QR-05CT Lorentzian-distance continuum step."""

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
    spec = importlib.util.spec_from_file_location("_qr05ct_test_study", HERE / "study.py")
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


class LorentzianDistanceTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_mean_ratio_is_stable(self):
        self.assertTrue(self.report["mean_stable"])
        constant = self.report["constant"]
        for row in self.report["manifoldlike"]:
            self.assertAlmostEqual(row["mean_ratio"], constant, delta=self.protocol["mean_tolerance"])

    def test_fluctuations_decrease(self):
        self.assertTrue(self.report["spread_decreasing"])
        spreads = [row["spread"] for row in self.report["manifoldlike"]]
        self.assertTrue(all(spreads[i] > spreads[i + 1] for i in range(len(spreads) - 1)))

    def test_random_order_control_is_distinct(self):
        self.assertTrue(self.report["control"]["distinct"])

    def test_lorentzian_distance_converges(self):
        self.assertTrue(self.report["lorentzian_distance_converges"])

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
        self.assertEqual(capture["schema"], "qr05ct-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
