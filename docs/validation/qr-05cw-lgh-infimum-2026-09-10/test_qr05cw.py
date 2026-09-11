"""Bounded tests for the QR-05CW LGH infimum via bottleneck assignment."""

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
    spec = importlib.util.spec_from_file_location("_qr05cw_test_study", HERE / "study.py")
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


class LGHInfimumTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_identity_is_optimal_at_fixed_scale(self):
        self.assertTrue(self.report["identity_is_optimal"])
        for row in self.report["rows"]:
            self.assertLessEqual(row["improvement"], 1e-9)
            self.assertAlmostEqual(row["infimum"], row["identity"], places=9)

    def test_rows_are_well_formed(self):
        self.assertEqual(len(self.report["rows"]), len(self.protocol["n_grid"]))
        for row in self.report["rows"]:
            self.assertGreater(row["infimum"], 0.0)

    def test_scale_degeneracy_is_recorded(self):
        self.assertEqual(self.report["scale_degeneracy"]["free_scale_infimum_control"], 0.0)

    def test_small_space_is_inconclusive(self):
        # Honest negative: the incomparable control is not separated at N<=8, so
        # the LGH infimum is not established by small-space bottleneck assignment.
        self.assertFalse(self.report["control"]["distinct"])
        self.assertFalse(self.report["lgh_infimum_established"])
        self.assertIn("inconclusive", self.report["verdict"])

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
        self.assertEqual(capture["schema"], "qr05cw-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
