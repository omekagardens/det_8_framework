"""Bounded tests for the QR-05CK metric reconstruction / refinement benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05ck_test_study", HERE / "study.py")
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


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_refinement_consistency(self):
        self.assertTrue(self.report["refinement_consistent"])
        self.assertEqual(len(self.report["refinement"]), len(self.protocol["n_grid"]))
        for row in self.report["refinement"]:
            self.assertEqual(len(row["recovered"]), self.protocol["bins"])

    def test_mse_decreases_with_density(self):
        self.assertTrue(self.report["mse_decreasing"])
        mses = [row["mse"] for row in self.report["refinement"]]
        self.assertTrue(all(mses[i] >= mses[i + 1] for i in range(len(mses) - 1)))

    def test_grid_robustness(self):
        self.assertTrue(self.report["grid"]["robust"])
        self.assertLessEqual(self.report["grid"]["mse_between_offsets"], self.protocol["grid_tolerance"])

    def test_whole_point_granularity(self):
        block = self.report["whole_point"]
        n0 = self.protocol["n_grid"][0]
        bins = self.protocol["bins"]
        self.assertAlmostEqual(block["mean_count_lowest"], n0 / bins, places=6)
        self.assertAlmostEqual(block["granularity"], bins / n0, places=6)

    def test_non_conformal_control_fails(self):
        self.assertTrue(self.report["negative_control"]["control_required"])

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
        self.assertEqual(capture["schema"], "qr05ck-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
