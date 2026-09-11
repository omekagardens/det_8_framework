"""Bounded tests for the QR-05CB open-data applicability run."""

from __future__ import annotations

import hashlib
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
    spec = importlib.util.spec_from_file_location("_qr05cb_test_study", HERE / "study.py")
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


class ApplicabilityTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_dataset_hash_and_grid(self):
        digest = hashlib.sha256((HERE / "data/VBI_Coincidence_20230707.dat").read_bytes()).hexdigest()
        self.assertEqual(digest, self.protocol["dataset"]["sha256"])
        self.assertEqual(self.report["grid"]["rows"], 1184)
        self.assertEqual(self.report["grid"]["cols"], 29)
        self.assertEqual(self.report["grid"]["beta_step"], 32)
        self.assertEqual(self.report["grid"]["alpha_steps"], 37)

    def test_nesting_holds_by_construction(self):
        primary = self.study.load_module("_qr05cb_test_primary", HERE / "primary.py")
        columns = self.protocol["columns"]
        rows = primary.parse(HERE / "data" / "VBI_Coincidence_20230707.dat")
        for row in rows:
            cc4 = primary.cell(row, columns, "cc4")
            alice = primary.cell(row, columns, "cc_alice")
            single = primary.cell(row, columns, "single1")
            self.assertTrue(0 <= cc4 <= alice <= single)

    def test_family_range(self):
        self.assertEqual(self.report["family_q2_max"], [3, 8])
        self.assertEqual(self.report["family_q2_min"], [567, 2272])

    def test_single_normalized_gap(self):
        mapping = by_id(self.report["mappings"], "single_normalized")
        self.assertTrue(mapping["valid_all"])
        r2_min = F(*mapping["r2_min"])
        r2_max = F(*mapping["r2_max"])
        self.assertTrue(F(7, 100) < r2_min < r2_max < F(8, 100))
        gap = F(*mapping["dist_min"])
        self.assertTrue(F(1, 8) < gap < F(1, 4))
        self.assertEqual(mapping["admitted_at_e"], 0)

    def test_no_mapping_admits_a_target(self):
        for mapping in self.report["mappings"]:
            self.assertEqual(mapping["admitted_at_e"], 0, mapping["id"])
            self.assertTrue(mapping["valid_all"], mapping["id"])

    def test_allowance_value(self):
        self.assertEqual(self.report["allowance"]["e_cal"], [3, 200])

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
        self.assertEqual(capture["schema"], "qr05cb-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
