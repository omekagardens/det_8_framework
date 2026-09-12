"""Bounded tests for QR-05DF (physical pair-kernel; E's next step)."""

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
    return _load("_qr05df_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05df_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05df_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class PhysicalPairKernelTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_directed_propagator_recovers_the_light_cones(self):
        self.assertTrue(self.report["flags"]["directed_propagator_recovers_light_cones"])
        for row in self.report["objects"]:
            self.assertTrue(row["directed_light_cone_recovered"], row["object"])
            self.assertTrue(row["undirected_comparability_is_support"], row["object"])

    def test_phase_sign_is_the_orientation(self):
        self.assertTrue(self.report["flags"]["phase_sign_is_the_orientation"])
        for row in self.report["objects"]:
            self.assertTrue(row["phase_sign_is_orientation"], row["object"])

    def test_time_reversal_acts_as_conjugation(self):
        self.assertTrue(self.report["flags"]["time_reversal_acts_as_conjugation"])
        self.assertTrue(self.report["flags"]["magnitude_is_orientation_blind"])
        tr = self.report["time_reversal"]
        self.assertEqual(tr["checked"], 6)
        self.assertTrue(tr["K_transposes"] and tr["G_invariant"] and tr["Omega_flipped"]
                        and tr["magnitude_invariant"])

    def test_strong_positivity_is_not_automatic(self):
        self.assertFalse(self.report["flags"]["naive_physical_kernel_is_strongly_positive_for_all_objects"])
        self.assertTrue(self.report["flags"]["strong_positivity_is_a_nontrivial_constraint"])
        sp = self.report["strong_positivity"]
        self.assertEqual(sp["objects"], 6)
        self.assertEqual(sp["strongly_positive_count"], 3)
        psd = {r["object"]: r["strongly_positive"] for r in self.report["objects"]}
        self.assertTrue(psd["2-chain"] and psd["V"] and psd["3-chain"])
        self.assertFalse(psd["diamond"] or psd["sprinkle_d2_n6"] or psd["sprinkle_d2_n8"])

    def test_kernel_and_order_are_coupled_not_reduced(self):
        self.assertTrue(self.report["flags"]["kernel_and_order_are_coupled_not_reduced"])

    def test_known_answer_two_chain_propagator(self):
        for module in (primary_module(), reference_module()):
            prec = [[False, True], [False, False]]
            L = module.link_matrix(prec)
            self.assertEqual(L, [[0, 1], [0, 0]])
            K = module.path_propagator(L)
            self.assertEqual(K, [[1, 1], [0, 1]])
            G, O = module.kernel(K)
            self.assertEqual(G, [[2, 1], [1, 2]])
            self.assertEqual(O, [[0, 1], [-1, 0]])
            D = module.complex_kernel(G, O)
            self.assertAlmostEqual(D[0][1], complex(1, 1))
            self.assertGreater(D[0][1].imag, 0)   # x≺y ⇒ positive phase
            self.assertLess(D[1][0].imag, 0)      # y≻x ⇒ negative phase
            self.assertTrue(module.hermitian_psd(D, 1e-9))

    def test_known_answer_diamond_covers(self):
        module = primary_module()
        rel = [[False] * 4 for _ in range(4)]
        rel[0][1] = rel[0][2] = rel[0][3] = rel[1][3] = rel[2][3] = True
        L = module.link_matrix(rel)
        self.assertEqual(sum(sum(r) for r in L), 4)  # 0-3 is transitive, not a cover

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
        self.assertEqual(capture["schema"], "qr05df-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
