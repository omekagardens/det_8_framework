"""Bounded tests for QR-05DJ (DET-native record-κ law map)."""

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
    return _load("_qr05dj_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dj_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dj_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class DetNativeLawTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_record_driven_law_matches_the_two_point_dimension(self):
        self.assertTrue(self.report["flags"]["record_driven_law_matches_the_two_point_dimension"])
        # each mode's matched curve is matched at the sprinkle's ordering fraction
        for mode in self.report["modes"].values():
            self.assertTrue(mode["curve"])
            self.assertEqual(set(mode["matched"]), {"2", "3"})

    def test_record_driven_law_mismatches_the_link_structure(self):
        self.assertTrue(self.report["flags"]["record_driven_law_mismatches_the_link_structure"])
        for mode in self.report["modes"].values():
            for dim, m in mode["matched"].items():
                self.assertTrue(m["link_mismatch"])
                self.assertLess(m["link_ratio"], 0.85)

    def test_record_dependency_leaks_into_the_order(self):
        self.assertTrue(self.report["flags"]["record_dependency_leaks_into_the_order"])
        self.assertTrue(self.report["flags"]["record_legibility_vs_manifoldlikeness_tension"])
        # the "sum" coupling leaks; the κ-blind control does not.
        sum_leak = max(abs(m["leakage"]) for m in self.report["modes"]["sum"]["matched"].values())
        self.assertGreater(sum_leak, 0.15)
        self.assertTrue(self.report["flags"]["kappa_blind_control_has_no_leakage"])
        for m in self.report["modes"]["blind"]["matched"].values():
            self.assertLess(abs(m["leakage"]), 0.15)

    def test_det_native_law_is_not_manifoldlike(self):
        self.assertFalse(self.report["flags"]["det_native_law_is_manifoldlike"])
        self.assertFalse(self.report["flags"]["o7_emergence_achieved_without_inserting_geometry"])

    def test_matched_order_keeps_the_sprinkle_dimension(self):
        for ref in self.report["sprinkle_reference"]:
            self.assertLess(abs(ref["d_mm"] - ref["dim"]), 0.4, ref["dim"])

    def test_known_answer_leakage(self):
        for module in (primary_module(), reference_module()):
            # a star 0 -> {1,2,3} with κ = [1.5, 0, 0, 0] gives degree an affine function of κ
            n = 4
            prec = [[False] * n for _ in range(n)]
            for j in (1, 2, 3):
                prec[0][j] = True
            kappa = [1.5, 0.0, 0.0, 0.0]
            self.assertAlmostEqual(module.leakage(prec, kappa), 1.0, places=9)
            # the κ-blind kernel has no relation to κ: a chain with symmetric κ gives 0
            chain = [[i < j for j in range(3)] for i in range(3)]
            self.assertAlmostEqual(module.leakage(chain, [0.0, 0.5, 1.0]), 0.0, places=9)

    def test_controls(self):
        by_name = {c["name"]: c for c in self.report["controls"]}
        self.assertAlmostEqual(by_name["chain"]["d_mm"], 1.0, places=6)
        self.assertGreater(by_name["antichain"]["d_mm"], 10.0)

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
        self.assertEqual(capture["schema"], "qr05dj-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
