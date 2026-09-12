"""Bounded tests for QR-05DH (true Sorkin–Johnston vacuum from the BD inverse)."""

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
    return _load("_qr05dh_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dh_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dh_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class SorkinJohnstonVacuumTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_pauli_jordan_support_is_the_light_cone(self):
        self.assertTrue(self.report["flags"]["pauli_jordan_supported_on_causal_pairs"])
        self.assertTrue(self.report["flags"]["light_cones_recovered_from_the_pauli_jordan"])

    def test_sj_state_is_hermitian(self):
        self.assertTrue(self.report["flags"]["sj_state_is_hermitian"])

    def test_sj_state_is_strongly_positive_for_all_objects_and_masses(self):
        self.assertTrue(self.report["flags"]["sj_state_is_strongly_positive_by_construction"])
        self.assertTrue(self.report["flags"]["no_critical_mass_required"])
        self.assertTrue(self.report["flags"]["negative_dsquared_is_psd"])
        for m in self.protocol["masses"]:
            self.assertEqual(self.report["mass_sweep"][str(m)], 6)

    def test_time_reversal_flips_the_pauli_jordan(self):
        self.assertTrue(self.report["flags"]["time_reversal_flips_the_pauli_jordan"])

    def test_naive_symmetrisation_is_not_always_positive(self):
        self.assertTrue(self.report["flags"]["naive_symmetrisation_is_not_always_positive"])
        for row in self.report["objects"]:
            self.assertFalse(any(row["naive_psd_by_mass"].values()), row["object"])

    def test_known_answer_bd_operator_and_pauli_jordan(self):
        for module in (primary_module(), reference_module()):
            prec = [[False, True], [False, False]]
            B = module.bd_operator(prec, 3)
            self.assertEqual(B, [[-1.0, 0.0], [3.0, -1.0]])
            GR = module.retarded_green(prec, 3, 0.0)
            D = module.pauli_jordan(GR)
            self.assertAlmostEqual(D[0][1], 3.0)
            self.assertAlmostEqual(D[1][0], -3.0)

    def test_known_answer_psd_sqrt(self):
        for module in (primary_module(), reference_module()):
            if module.__name__.endswith("reference"):
                sq = module.psd_sqrt([[4.0, 0.0], [0.0, 9.0]])
                self.assertAlmostEqual(sq[0][0], 2.0, places=6)
                self.assertAlmostEqual(sq[1][1], 3.0, places=6)
            else:
                sq, min_eig = module.psd_sqrt([[4.0, 0.0], [0.0, 9.0]])
                self.assertAlmostEqual(sq[0][0], 2.0, places=6)
                self.assertAlmostEqual(sq[1][1], 3.0, places=6)
                self.assertAlmostEqual(min_eig, 4.0, places=9)

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
        self.assertEqual(capture["schema"], "qr05dh-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
