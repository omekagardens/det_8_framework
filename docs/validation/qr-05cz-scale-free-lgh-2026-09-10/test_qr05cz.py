"""Bounded tests for the QR-05CZ scale-free LGH comparison and the correction."""

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
    spec = importlib.util.spec_from_file_location("_qr05cz_test_study", HERE / "study.py")
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


class ScaleFreeLGHTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_directed_distance_matches_the_chain_support(self):
        self.assertTrue(all(v == 0 for v in self.report["convention"]["chain_vs_directed"].values()))

    def test_symmetric_counterpart_is_detected_as_a_defect(self):
        mismatches = self.report["convention"]["chain_vs_symmetric"]
        self.assertTrue(all(v > 0 for v in mismatches.values()))
        self.assertEqual(mismatches[str(self.protocol["convention_n"][0])], 18)

    def test_symmetric_arm_reproduces_the_cw_cx_floor(self):
        # The CW/CX convention gives the non-vanishing floor (its min lower bound
        # is the value QR-05CX reported, ~0.896).
        self.assertGreater(self.report["symmetric_floor_lower_bound"], 0.5)
        for row in self.report["arm_symmetric"]:
            self.assertGreater(row["lower_bound"], 0.5)

    def test_directed_distance_gives_much_smaller_distortion(self):
        directed = {row["n"]: row["fixed_identity"] for row in self.report["arm_directed"]}
        for row in self.report["arm_symmetric"]:
            self.assertLess(directed[row["n"]], row["fixed_identity"] - 0.3)

    def test_directed_lower_bound_decays_and_removes_the_obstruction(self):
        self.assertTrue(self.report["directed_lower_bound_decays"])
        means = [row["lower_bound_mean"] for row in self.report["trend_directed"]]
        self.assertEqual(means, sorted(means, reverse=True))
        self.assertLess(self.report["directed_floor_lower_bound"],
                        self.report["symmetric_floor_lower_bound"] / 3.0)

    def test_identity_is_scale_free_optimal_on_the_exact_grid(self):
        self.assertTrue(self.report["identity_is_optimal_scale_free"])
        for row in self.report["rows_exact"]:
            self.assertTrue(row["identity_optimal"])
            self.assertAlmostEqual(row["scale_free_identity"], row["exact_scale_free_infimum"], places=9)

    def test_convergence_is_not_claimed(self):
        self.assertFalse(self.report["lgh_infimum_established"])
        self.assertIn("reopened", self.report["verdict"])
        self.assertIn("not shown to converge", self.report["verdict"])

    def test_relative_scale_is_near_one_for_the_directed_distance(self):
        for row in self.report["arm_directed"]:
            self.assertGreater(row["relative_scale"], 0.7)
            self.assertLess(row["relative_scale"], 1.3)

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
        self.assertEqual(capture["schema"], "qr05cz-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
