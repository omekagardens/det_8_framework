"""Bounded tests for the QR-05CC composition verification."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05cc_test_study", HERE / "study.py")
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
        if item["id"] == key:
            return item
    raise KeyError(key)


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_triangle_composition(self):
        for item in self.protocol["norms"]:
            expected = item["expected"]
            actual = by_id(self.report["norms"], item["id"])
            self.assertEqual(actual["e"], expected["e"], item["id"])
            self.assertEqual(actual["bound_ok"], expected["bound_ok"], item["id"])
            self.assertEqual(actual["tight"], expected["tight"], item["id"])

    def test_close_fit_does_not_improve(self):
        n4 = by_id(self.report["norms"], "N4")
        self.assertTrue(n4["tight"])
        self.assertEqual(F(*n4["e"]), F(*n4["nrr"]) + F(*n4["nrq"]))

    def test_split(self):
        self.assertEqual(by_id(self.report["splits"], "S1")["e_cal"], [9, 64])
        self.assertEqual(by_id(self.report["splits"], "S2")["e_cal"], [3, 200])

    def test_union_bound_and_product_refutation(self):
        for item in self.protocol["spaces"]:
            expected = item["expected"]
            actual = by_id(self.report["spaces"], item["id"])
            self.assertEqual(actual["alpha"], expected["alpha"], item["id"])
            self.assertEqual(actual["beta"], expected["beta"], item["id"])
            self.assertEqual(actual["p_EcapG"], expected["p_EcapG"], item["id"])
            self.assertEqual(actual["union_ok"], expected["union_ok"], item["id"])
            self.assertEqual(actual["product"], expected["product"], item["id"])
            self.assertEqual(actual["product_refuted"], expected["product_refuted"], item["id"])
        self.assertTrue(by_id(self.report["spaces"], "P2")["product_refuted"])

    def test_selection_regimes(self):
        self.assertEqual(by_id(self.report["regimes"], "R2a")["uncond"], [0, 1])
        r2b = by_id(self.report["regimes"], "R2b")
        self.assertEqual(r2b["uncond"], [3, 20])
        self.assertEqual(r2b["cond"], [3, 5])
        self.assertFalse(by_id(self.report["regimes"], "R2c")["defined"])
        r2d = by_id(self.report["regimes"], "R2d")
        self.assertEqual(r2d["uncond"], [1, 1])
        self.assertEqual(r2d["cond"], [1, 1])

    def test_repeats(self):
        self.assertEqual(by_id(self.report["repeats"], "R3a")["budget"], [1, 4])
        self.assertEqual(by_id(self.report["repeats"], "R3b")["budget"], [1, 20])

    def test_schema_flag(self):
        self.assertFalse(by_id(self.report["schemas"], "complete")["conditional_only"])
        self.assertTrue(by_id(self.report["schemas"], "unmet")["conditional_only"])

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
        self.assertEqual(capture["schema"], "qr05cc-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
