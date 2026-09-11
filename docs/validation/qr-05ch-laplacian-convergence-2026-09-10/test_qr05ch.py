"""Bounded tests for the QR-05CH graph-Laplacian convergence benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05ch_test_study", HERE / "study.py")
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


class LaplacianTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_laplacian_action_is_proportional_to_the_eigenfunction(self):
        for key in ("mode1", "mode2"):
            block = self.report[key]
            self.assertLess(block["residual"], self.protocol["residual_tolerance"], key)
            self.assertLess(block["slope"], 0.0, key)

    def test_intrinsic_constant_is_mode_independent(self):
        self.assertTrue(self.report["mode_independent"])
        self.assertLessEqual(self.report["mode_gap"], self.protocol["gap_tolerance"])

    def test_local_proportionality_is_required(self):
        control = self.report["negative_control"]
        self.assertTrue(control["control_required"])
        self.assertGreater(control["residual"], self.protocol["control_factor"] * control["local_residual"])

    def test_residual_decreases_with_n(self):
        self.assertTrue(self.report["residual_decreasing"])
        residuals = [row["residual"] for row in self.report["residual_grid"]]
        self.assertTrue(all(residuals[i] > residuals[i + 1] for i in range(len(residuals) - 1)))

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
        self.assertEqual(capture["schema"], "qr05ch-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
