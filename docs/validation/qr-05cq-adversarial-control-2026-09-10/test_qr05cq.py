"""Bounded tests for the QR-05CQ adversarial non-manifoldlike control."""

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
    spec = importlib.util.spec_from_file_location("_qr05cq_test_study", HERE / "study.py")
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


class AdversarialTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_manifoldlike_orders_are_accepted(self):
        for row in self.report["manifoldlike"]:
            self.assertTrue(row["dim_ok"], row["d"])
            self.assertTrue(row["link_ok"], row["d"])
            self.assertTrue(row["consistent"], row["d"])

    def test_bipartite_order_fools_dimension_but_is_rejected(self):
        bip = by_id(self.report["adversarial"], "bipartite")
        self.assertTrue(bip["dim_fooled"])       # ordering fraction matches r(2)
        self.assertFalse(bip["link_ok"])          # but the link fraction is 1
        self.assertTrue(bip["rejected"])

    def test_chain_and_antichain_are_rejected(self):
        self.assertTrue(by_id(self.report["adversarial"], "chain")["rejected"])
        self.assertTrue(by_id(self.report["adversarial"], "antichain")["rejected"])

    def test_discriminator_separates(self):
        disc = self.report["discriminator"]
        self.assertTrue(disc["separates"])
        self.assertLessEqual(disc["manifold_max_link"], disc["link_threshold"])
        self.assertGreater(disc["bipartite_link"], disc["link_threshold"])

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
        self.assertEqual(capture["schema"], "qr05cq-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
