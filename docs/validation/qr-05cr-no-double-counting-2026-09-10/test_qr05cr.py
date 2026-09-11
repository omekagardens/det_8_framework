"""Bounded tests for the QR-05CR no-double-counting audit."""

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
    spec = importlib.util.spec_from_file_location("_qr05cr_test_study", HERE / "study.py")
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


class NoDoubleCountingTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_no_source_term(self):
        self.assertTrue(self.report["source_term"]["no_source"])
        self.assertLess(self.report["source_term"]["pointwise_max"], 1e-12)
        self.assertLess(self.report["source_term"]["divergence_max"], 1e-12)

    def test_divergence_form_conserves_flux(self):
        flux = self.report["flux"]
        self.assertLess(abs(flux["divergence_total"]), 1e-9)
        # the pointwise-coefficient form is not flux-conserving
        self.assertTrue(flux["conservative_form_required"])

    def test_coefficient_is_the_t7_geometry(self):
        self.assertTrue(self.report["coefficient_matches_t7"]["matches"])
        self.assertLess(self.report["coefficient_matches_t7"]["max_dev"], 1e-12)

    def test_added_source_is_detected(self):
        self.assertTrue(self.report["source_control"]["flagged"])

    def test_audit_passes(self):
        self.assertTrue(self.report["no_double_counting"])

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
        self.assertEqual(capture["schema"], "qr05cr-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
