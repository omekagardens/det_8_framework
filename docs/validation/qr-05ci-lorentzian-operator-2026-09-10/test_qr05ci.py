"""Bounded tests for the QR-05CI 2D Lorentzian operator benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05ci_test_study", HERE / "study.py")
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


class LorentzianOperatorTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_operator_forms_agree_exactly(self):
        # Eq. (2) matrix and Eq. (1) layer sums must agree on a deterministic
        # causal set, exactly (rational arithmetic).
        self.assertTrue(self.report["exact_form_agreement"])

    def test_constant_is_not_consistent_at_accessible_n(self):
        # Honest negative: the 2D operator's constant term is not consistently
        # annihilated across densities (0.354 at N=300, 0.490 at N=600), so the
        # continuum limit is not demonstrated here.
        self.assertFalse(self.report["validated"])
        self.assertFalse(self.report["constant_annihilated"])
        self.assertTrue(any(residual > self.protocol["constant_tolerance"]
                            for residual in self.report["constant_residuals"]))

    def test_ensemble_reports_layer_and_bconst(self):
        self.assertEqual(len(self.report["ensemble"]), len(self.protocol["n_grid"]))
        for row in self.report["ensemble"]:
            self.assertIsNotNone(row["layer_combo"])
            self.assertIsNotNone(row["mean_B_const"])

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
        self.assertEqual(capture["schema"], "qr05ci-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
