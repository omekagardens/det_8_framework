"""Bounded tests for the QR-05CG dimension-convergence benchmark."""

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
    spec = importlib.util.spec_from_file_location("_qr05cg_test_study", HERE / "study.py")
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


def by_id(items, key):
    for item in items:
        if item["d"] == key:
            return item
    raise KeyError(key)


class ConvergenceTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_exponents_match_covering_rate(self):
        for curve in self.report["curves"]:
            self.assertTrue(curve["within_tolerance"], curve["d"])
            self.assertLess(curve["exponent"], 0.0)
            self.assertEqual(curve["expected"], self.protocol["expected_exponent"][str(curve["d"])])

    def test_3plus1_is_slowest(self):
        d2 = by_id(self.report["curves"], 2)
        d4 = by_id(self.report["curves"], 4)
        self.assertLess(abs(d4["exponent"]), abs(d2["exponent"]))
        self.assertEqual(self.report["slowest_dim"], 4)

    def test_nearest_neighbour_decreases_with_n(self):
        for curve in self.report["curves"]:
            means = curve["mean_nn"]
            self.assertTrue(all(means[i] > means[i + 1] for i in range(len(means) - 1)), curve["d"])

    def test_primary_reference_agree(self):
        _, left, right = self.study.analyze_native()
        self.assertEqual(self.study.encode(left), self.study.encode(right))
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
        self.assertEqual(capture["schema"], "qr05cg-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
