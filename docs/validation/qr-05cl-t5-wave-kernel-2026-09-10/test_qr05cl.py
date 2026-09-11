"""Bounded tests for the QR-05CL T5 wave-kernel benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05cl_test_study", HERE / "study.py")
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


class WaveKernelTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_quadratics_exact(self):
        block = self.report["exact_quadratics"]
        self.assertTrue(block["match"])
        self.assertAlmostEqual(block["S_x2"], block["moment"], places=12)
        self.assertAlmostEqual(block["T_t2"], block["moment"], places=12)

    def test_coefficient_is_the_kernel_moment(self):
        rows = self.report["coefficient_from_moment"]
        self.assertEqual(len(rows), len(self.protocol["kernels"]))
        for row in rows:
            self.assertAlmostEqual(row["ratio"], 1.0, places=9, msg=row["kernel"])

    def test_wave_operator_converges_at_second_order(self):
        exponent = self.report["convergence_exponent"]
        self.assertAlmostEqual(exponent, 2.0, delta=self.protocol["exponent_tolerance"])
        errors = [row["mean_abs_error"] for row in self.report["convergence"]]
        self.assertTrue(all(errors[i] > errors[i + 1] for i in range(len(errors) - 1)))

    def test_asymmetric_kernel_is_drift_not_wave(self):
        drift = self.report["drift"]
        self.assertAlmostEqual(drift["symmetric_first_moment"], 0.0, places=12)
        self.assertGreater(abs(drift["asymmetric_first_moment"]), 1e-6)
        self.assertTrue(drift["asymmetric_is_drift"])

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
        self.assertEqual(capture["schema"], "qr05cl-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
