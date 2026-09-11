"""Bounded tests for the QR-05CF T7 supplied-geometry benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05cf_test_study", HERE / "study.py")
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


class T7BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_analytic_ordering_fraction_decreases_with_dimension(self):
        values = [self.report["analytic_r"][str(d)] for d in (2, 3, 4)]
        self.assertAlmostEqual(values[0], 0.5, places=6)
        self.assertGreater(values[0], values[1])
        self.assertGreater(values[1], values[2])

    def test_dimension_recovery(self):
        for row in self.report["dimension"]:
            self.assertTrue(row["within_tolerance"], row["d"])
            self.assertTrue(row["recovers"], row["d"])
            self.assertEqual(row["estimated"], row["d"])

    def test_links_are_nearer_null(self):
        nullness = self.report["nullness"]
        self.assertTrue(nullness["links_nearer"])
        self.assertGreater(nullness["n_links"], 0)
        self.assertGreater(nullness["n_comparable"], nullness["n_links"])

    def test_conformal_factor_recovery(self):
        conformal = self.report["conformal"]
        self.assertLess(conformal["mse"], self.protocol["conformal_mse_tolerance"])
        self.assertTrue(conformal["truth_monotone"])
        self.assertTrue(conformal["trend_up"])
        self.assertEqual(len(conformal["recovered"]), self.protocol["conformal_bins"])

    def test_conformal_invariance_of_order(self):
        self.assertTrue(self.report["invariance"]["invariant"])

    def test_negative_control_outside_diamond_family(self):
        control = self.report["negative_control"]
        self.assertTrue(control["outside_family"])
        self.assertGreater(control["chain_r"], control["family_max"])
        self.assertLess(control["antichain_r"], control["family_min"])

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
        self.assertEqual(capture["schema"], "qr05cf-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
