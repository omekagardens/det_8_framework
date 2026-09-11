"""Bounded tests for the QR-05CX LGH infimum at scale (branch-and-bound)."""

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
    spec = importlib.util.spec_from_file_location("_qr05cx_test_study", HERE / "study.py")
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


class LGHScaleTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_identity_is_optimal_on_the_exact_grid(self):
        self.assertTrue(self.report["identity_is_optimal"])
        for row in self.report["rows"]:
            self.assertLessEqual(row["improvement"], 1e-9)
            self.assertAlmostEqual(row["infimum"], row["identity"], places=9)

    def test_rows_are_well_formed(self):
        self.assertEqual(len(self.report["rows"]), len(self.protocol["n_exact"]))
        for row in self.report["rows"]:
            self.assertGreater(row["infimum"], 0.0)

    def test_branch_and_bound_agrees_with_brute_force(self):
        self.assertTrue(self.report["brute_agrees"])
        small = [row for row in self.report["rows"] if row["n"] <= self.protocol["n_brute_max"]]
        self.assertTrue(small)
        for row in small:
            self.assertIsNotNone(row["brute"])
            self.assertAlmostEqual(row["brute"], row["infimum"], places=9)

    def test_certified_floor_does_not_vanish_at_scale(self):
        # The sorted-multiset matching bound is a valid lower bound at any N; if it
        # stays above the floor threshold, the fixed-scale infimum does not vanish.
        self.assertGreater(self.report["certified_floor"], self.protocol["floor_threshold"])
        self.assertTrue(self.report["no_convergence_to_zero"])
        for row in self.report["scale"]:
            self.assertLessEqual(row["lower_bound"], row["identity_upper"] + 1e-9)

    def test_lower_bound_is_below_known_exact_infimum(self):
        exact = {row["n"]: row["infimum"] for row in self.report["rows"]}
        for row in self.report["scale"]:
            if row["n"] in exact:
                self.assertLessEqual(row["lower_bound"], exact[row["n"]] + 1e-9)

    def test_still_inconclusive_control_not_separated(self):
        self.assertFalse(self.report["control"]["distinct"])
        self.assertFalse(self.report["lgh_infimum_established"])
        self.assertIn("inconclusive", self.report["verdict"])

    def test_scale_degeneracy_is_recorded(self):
        self.assertEqual(self.report["scale_degeneracy"]["free_scale_infimum_control"], 0.0)

    def test_boundary_runs_are_recorded_and_consistent(self):
        boundary = self.protocol["boundary"]
        self.assertEqual([row["n"] for row in boundary], [11, 12])
        for row in boundary:
            self.assertTrue(row["identity_optimal"])
            self.assertTrue(row["perm_is_identity"])
            self.assertAlmostEqual(row["infimum"], row["identity"], places=9)
            self.assertGreater(row["nodes"], 0)
        # exact search cost grows steeply (the bottleneck-QAP hardness): ~5x or more per N
        for earlier, later in zip(boundary, boundary[1:]):
            self.assertGreater(later["nodes"], 5 * earlier["nodes"])

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
        self.assertEqual(capture["schema"], "qr05cx-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
