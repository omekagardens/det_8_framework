"""Bounded tests for the QR-05CA synthetic pipeline rehearsal.

Definitions only at import; the mathematical checks and the suite entry
point live below. Exact native types, no floats.
"""

from __future__ import annotations

import importlib.util
import json
import signal
import sys
import unittest
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
EXPECTED_REFUSALS = {"integrity", "analysis_id", "mark", "support", "loss", "insufficient", "stationarity"}


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05ca_test_study", HERE / "study.py")
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


class RehearsalTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_schema_and_analysis_id(self):
        self.assertEqual(self.report["schema"], "qr05ca-report-v1")
        self.assertEqual(self.report["analysis_id"], self.protocol["analysis_id"])

    def test_datasets_match_declared_expectations(self):
        for fixture in self.protocol["datasets"]:
            expected = fixture["expected"]
            actual = by_id(self.report["datasets"], fixture["id"])
            self.assertEqual(actual["status"], expected["status"], fixture["id"])
            self.assertEqual(actual["K1"], expected["K1"], fixture["id"])
            self.assertEqual(actual["K2"], expected["K2"], fixture["id"])
            self.assertEqual(actual["n_eff"], expected["n_eff"], fixture["id"])
            self.assertEqual(actual["r_hat"], expected["r_hat"], fixture["id"])
            self.assertEqual(actual["inverse"]["targets"], expected["targets"], fixture["id"])
            self.assertEqual(actual["by"]["metric"], "pass", fixture["id"])
            self.assertEqual(actual["by"]["dynamics"], "pass", fixture["id"])

    def test_refusals_fire_declared_reason(self):
        seen = set()
        for fixture in self.protocol["refusals"]:
            expected = fixture["expected"]
            actual = by_id(self.report["refusals"], fixture["id"])
            self.assertEqual(actual["status"], expected["status"], fixture["id"])
            self.assertEqual(actual["reason"], expected["reason"], fixture["id"])
            seen.add(actual["reason"])
        self.assertEqual(seen, EXPECTED_REFUSALS - {"integrity"})

    def test_integrity_seal(self):
        primary = self.study.load_module("_qr05ca_test_primary", HERE / "primary.py")
        fixture = self.protocol["datasets"][0]
        core = {key: fixture[key] for key in primary.DATASET_KEYS if key in fixture}
        sealed = dict(core)
        sealed["seal"] = primary.seal_of(core)
        good = primary.reduce_dataset(sealed, self.protocol["analysis_id"])
        self.assertEqual(good["status"], "accepted")
        mutated = dict(sealed)
        mutated["attempts"] = [{"index": 0, "event": "00", "loss": False}] + list(sealed["attempts"][1:])
        bad = primary.reduce_dataset(mutated, self.protocol["analysis_id"])
        self.assertEqual(bad["status"], "refused")
        self.assertEqual(bad["reason"], "integrity")

    def test_allowances(self):
        for fixture in self.protocol["allowances"]:
            expected = fixture["expected"]
            actual = by_id(self.report["allowances"], fixture["id"])
            self.assertEqual(actual["e_cal"], expected["e_cal"], fixture["id"])
            self.assertEqual(actual["beta"], expected["beta"], fixture["id"])
            self.assertEqual(actual["within"], expected["within"], fixture["id"])

    def test_inverses(self):
        for fixture in self.protocol["inverses"]:
            actual = by_id(self.report["inverses"], fixture["id"])
            self.assertEqual(actual["targets"], fixture["expected"]["targets"], fixture["id"])

    def test_feasibility(self):
        for fixture in self.protocol["feasibility"]:
            expected = fixture["expected"]
            actual = by_id(self.report["feasibility"], fixture["id"])
            self.assertEqual(actual["s"], expected["s"], fixture["id"])
            self.assertEqual(actual["score"], expected["score"], fixture["id"])
            self.assertEqual(actual["certified"], expected["certified"], fixture["id"])

    def test_by_cases(self):
        for fixture in self.protocol["by_cases"]:
            expected = fixture["expected"]
            actual = by_id(self.report["by_tests"], fixture["id"])
            self.assertEqual(actual["metric"], expected["metric"], fixture["id"])
            self.assertEqual(actual["dynamics"], expected["dynamics"], fixture["id"])

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
        self.assertEqual(capture["schema"], "qr05ca-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    def suite_expired(_signum, _frame):
        raise KeyboardInterrupt("QR-05CA 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
