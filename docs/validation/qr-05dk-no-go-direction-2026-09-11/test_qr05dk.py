"""Bounded tests for QR-05DK (the no-go direction)."""

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
    return _load("_qr05dk_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dk_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dk_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class NoGoDirectionTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_manifoldlike_locus_is_mapped(self):
        self.assertTrue(self.report["flags"]["manifoldlike_locus_is_mapped"])
        locus = self.report["manifoldlike_locus"]
        self.assertEqual([r["dim"] for r in locus], self.protocol["sprinkle_dims"])
        # link fraction increases as the ordering fraction decreases
        links = [r["link_fraction"] for r in locus]
        fs = [r["f"] for r in locus]
        self.assertEqual(links, sorted(links))
        self.assertEqual(fs, sorted(fs, reverse=True))

    def test_closure_dense_laws_are_under_linked(self):
        self.assertTrue(self.report["flags"]["closure_dense_laws_are_under_linked"])
        for m in self.report["matched"]:
            self.assertTrue(m["tp_under_links"], m["dim"])
            self.assertLess(m["tp_ratio"], 0.85)

    def test_a_geometry_free_law_exceeds_the_link_fraction(self):
        self.assertTrue(self.report["flags"]["a_geometry_free_law_exceeds_the_link_fraction"])
        for m in self.report["matched"]:
            self.assertTrue(m["bipartite_exceeds"], m["dim"])
            self.assertGreater(m["bipartite_ratio"], 1.15)

    def test_no_go_is_not_established(self):
        self.assertFalse(self.report["flags"]["no_go_established"])
        self.assertTrue(self.report["flags"]["obstruction_is_class_specific_to_closure_dense_laws"])
        self.assertTrue(self.report["flags"]["link_fraction_alone_does_not_capture_manifoldlikeness"])

    def test_known_answer_bipartite_is_maximally_linked(self):
        for module in (primary_module(), reference_module()):
            for p in (0.2, 0.6, 1.0):
                f, link, mu = module.stats(module.bipartite(60, p, seed=1))
                self.assertAlmostEqual(link, 1.0, places=9)  # no intermediates
                self.assertAlmostEqual(mu, 0.0, places=9)

    def test_known_answer_layer_cake(self):
        mp = primary_module()
        n = 200
        f, link, mu = mp.stats(mp.layered(n, 2))
        # complete 2-layer order: comparable pairs = (n/2)^2, all links, no intervals
        self.assertAlmostEqual(f, 2 * (n // 2) ** 2 / (n * (n - 1)), places=6)
        self.assertAlmostEqual(link, 1.0, places=9)
        self.assertAlmostEqual(mu, 0.0, places=9)
        _f4, link4, mu4 = mp.stats(mp.layered(n, 4))
        self.assertAlmostEqual(link4, 0.5, places=9)
        self.assertAlmostEqual(mu4, 1.0 / 6.0, places=6)

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
        self.assertEqual(capture["schema"], "qr05dk-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
