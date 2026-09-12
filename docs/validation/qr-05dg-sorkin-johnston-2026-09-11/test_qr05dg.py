"""Bounded tests for QR-05DG (Sorkin–Johnston-structured pair-kernel)."""

from __future__ import annotations

import importlib.util
import json
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
    return _load("_qr05dg_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dg_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dg_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class SorkinJohnstonTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_pauli_jordan_support_is_the_light_cone(self):
        self.assertTrue(self.report["flags"]["pauli_jordan_supported_on_causal_pairs"])
        self.assertTrue(self.report["flags"]["light_cones_recovered_from_the_pauli_jordan"])

    def test_two_point_is_hermitian_with_the_sj_split(self):
        self.assertTrue(self.report["flags"]["two_point_is_hermitian"])
        self.assertTrue(self.report["flags"]["real_part_symmetric_imag_antisymmetric"])

    def test_time_reversal_flips_delta_and_fixes_H(self):
        self.assertTrue(self.report["flags"]["time_reversal_flips_delta_and_fixes_H"])

    def test_sj_state_condition_is_mass_dependent(self):
        self.assertFalse(self.report["flags"]["sj_state_condition_holds_at_all_masses"])
        self.assertTrue(self.report["flags"]["sj_state_condition_is_mass_dependent"])
        self.assertTrue(self.report["flags"]["sj_state_condition_holds_above_a_critical_mass"])
        sweep = self.report["mass_sweep"]
        self.assertEqual(sweep["0.0"], 3)
        self.assertEqual(sweep["0.25"], 4)
        self.assertEqual(sweep["0.5"], 6)
        crit = {r["object"]: r["critical_mass"] for r in self.report["objects"]}
        self.assertEqual(crit["2-chain"], 0.0)
        self.assertEqual(crit["diamond"], 0.5)
        self.assertEqual(crit["sprinkle_d2_n6"], 0.25)
        self.assertEqual(crit["sprinkle_d2_n8"], 0.5)

    def test_known_answer_two_chain_sj_structure(self):
        for module in (primary_module(), reference_module()):
            L = [[0, 1], [0, 0]]
            Gr = module.retarded_green(L, 0.0)
            self.assertEqual(Gr, [[1.0, 1.0], [0.0, 1.0]])
            H, D, W = module.sj_structure(Gr)
            self.assertEqual(H, [[2.0, 1.0], [1.0, 2.0]])
            self.assertEqual(D, [[0.0, 1.0], [-1.0, 0.0]])
            self.assertAlmostEqual(W[0][1], complex(0.5, 0.5))
            self.assertAlmostEqual(W[1][0], complex(0.5, -0.5))
            self.assertTrue(module.hermitian_psd(W, 1e-9))

    def test_known_answer_delta_vanishes_for_spacelike_and_antichain(self):
        module = primary_module()
        # 2-chain: Δ(0,1) is the forward orientation.
        H, D, _W = module.sj_structure(module.retarded_green([[0, 1], [0, 0]], 0.0))
        self.assertEqual(D[0][1], 1.0)
        self.assertEqual(D[1][0], -1.0)
        # antichain: no relations ⇒ Δ = 0.
        H2, D2, _ = module.sj_structure(module.retarded_green([[0, 0], [0, 0]], 0.0))
        self.assertEqual(D2, [[0.0, 0.0], [0.0, 0.0]])

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
        self.assertEqual(capture["schema"], "qr05dg-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
