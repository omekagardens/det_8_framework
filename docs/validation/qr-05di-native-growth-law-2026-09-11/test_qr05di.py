"""Bounded tests for QR-05DI (native growth law -> manifoldlike emergence)."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
import unittest
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def load_study():
    return _load("_qr05di_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05di_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05di_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class NativeGrowthLawTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_mm_estimator_is_calibrated_on_sprinkles(self):
        self.assertTrue(self.report["flags"]["mm_estimator_is_calibrated"])
        for row in self.report["calibration"]:
            self.assertLess(abs(row["d_mm"] - row["dim"]), 0.35, row["dim"])

    def test_growth_law_matches_the_two_point_dimension(self):
        self.assertTrue(self.report["flags"]["growth_law_matches_the_two_point_dimension"])
        for dim, m in self.report["matched"].items():
            # at matched ordering fraction the 2-point MM dimension matches the intended dim
            self.assertLess(abs(m["d_mm_matched"] - float(dim)), 0.4, dim)

    def test_growth_law_mismatches_the_link_structure(self):
        self.assertTrue(self.report["flags"]["growth_law_mismatches_the_link_structure"])
        self.assertTrue(self.report["flags"]["two_point_mm_is_insufficient_for_manifoldlikeness"])
        for m in self.report["matched"].values():
            self.assertTrue(m["link_mismatch"])
            self.assertLess(m["link_ratio"], 0.85)

    def test_native_growth_law_is_not_manifoldlike(self):
        self.assertFalse(self.report["flags"]["native_growth_law_is_manifoldlike"])
        self.assertFalse(self.report["flags"]["o7_emergence_achieved_without_inserting_geometry"])

    def test_controls(self):
        by_name = {c["name"]: c for c in self.report["controls"]}
        self.assertAlmostEqual(by_name["chain"]["d_mm"], 1.0, places=6)
        self.assertGreater(by_name["antichain"]["d_mm"], 10.0)

    def test_known_answer_myrheim_meyer_curve(self):
        for module in (primary_module(), reference_module()):
            self.assertAlmostEqual(module._f_d(1.0), 1.0, places=9)
            self.assertAlmostEqual(module._f_d(2.0), 0.5, places=9)
            self.assertAlmostEqual(module._f_d(3.0), 0.22857142857142856, places=6)
            self.assertAlmostEqual(module.d_mm(0.5), 2.0, places=4)
            self.assertAlmostEqual(module.d_mm(1.0), 1.0, places=4)

    def test_known_answer_ordering_fraction(self):
        module = primary_module()
        n = 4
        chain = [[i < j for j in range(n)] for i in range(n)]
        self.assertAlmostEqual(module.stats(chain)[0], 1.0, places=9)
        antichain = [[False] * n for _ in range(n)]
        self.assertAlmostEqual(module.stats(antichain)[0], 0.0, places=9)

    def test_primary_reference_agree(self):
        _protocol, left, right = self.study.analyze_native()
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
        self.assertEqual(capture["schema"], "qr05di-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
