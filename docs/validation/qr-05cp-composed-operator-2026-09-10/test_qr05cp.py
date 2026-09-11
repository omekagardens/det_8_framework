"""Bounded tests for the QR-05CP composed T7+T5 operator construction."""

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
    spec = importlib.util.spec_from_file_location("_qr05cp_test_study", HERE / "study.py")
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


class ComposedOperatorTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_reconstruction_is_accurate(self):
        self.assertGreaterEqual(self.report["reconstruction_corr"], self.protocol["corr_high"])

    def test_composition_is_faithful(self):
        # The operator's coefficient is the T7 geometry: the continuum ratio
        # Sf/(h^2 f'') equals a single constant times D at every site.
        self.assertLessEqual(self.report["composition_dev"], self.protocol["dev_tol"])
        self.assertGreater(self.report["composition_constant"], 0.0)

    def test_independent_coefficient_fails(self):
        self.assertLessEqual(self.report["control_corr"], self.protocol["corr_low"])

    def test_model_is_composed(self):
        self.assertTrue(self.report["composed"])

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
        self.assertEqual(capture["schema"], "qr05cp-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
