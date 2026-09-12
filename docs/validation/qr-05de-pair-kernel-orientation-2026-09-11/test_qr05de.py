"""Bounded tests for QR-05DE (pair-kernel orientation; direction E)."""

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
    return _load("_qr05de_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05de_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05de_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class PairKernelOrientationTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def test_pair_kernel_is_hermitian_and_splits(self):
        self.assertTrue(self.report["flags"]["pair_kernel_hermitian_and_splits"])
        primary = primary_module()
        rel = [[False, True], [False, False]]
        D0 = primary.naive_glue(rel)
        self.assertAlmostEqual(D0[0][1], complex(1, 1))
        self.assertAlmostEqual(D0[1][0], complex(1, -1))  # conjugate -> Hermitian

    def test_magnitude_is_orientation_blind(self):
        self.assertTrue(self.report["flags"]["magnitude_is_time_reversal_invariant"])
        self.assertTrue(self.report["flags"]["orientation_not_recoverable_from_magnitude"])
        tr = self.report["time_reversal"]
        self.assertTrue(tr["C_invariant"] and tr["Omega_flipped"] and tr["magnitude_invariant"])
        self.assertEqual(tr["checked"], 4472)

    def test_support_is_the_undirected_comparability(self):
        self.assertTrue(self.report["flags"]["support_is_undirected_comparability"])
        primary = primary_module()
        # 2-chain vs its time reverse: same |D|, different orientation.
        p = [[False, True], [False, False]]
        pt = primary.transpose(p)
        self.assertNotEqual(p, pt)  # non-isomorphic directed orders
        Dp, Dt = primary.naive_glue(p), primary.naive_glue(pt)
        self.assertAlmostEqual(abs(Dp[0][1]), abs(Dt[0][1]))

    def test_naive_glue_is_strongly_positive_only_for_the_antichain(self):
        self.assertTrue(self.report["flags"]["naive_conformal_plus_orientation_never_strongly_positive"])
        for n in ("2", "3", "4", "5"):
            row = self.report["naive_glue"][n]
            self.assertEqual(row["naive_glue_psd"], 1)
            self.assertTrue(row["psd_only_antichain"])
        self.assertEqual(self.report["poset_totals"], {"2": 3, "3": 19, "4": 219, "5": 4231})

    def test_orientation_kernel_exists_but_magnitude_is_pinned(self):
        self.assertTrue(self.report["flags"]["orientation_carrying_strongly_positive_kernel_exists"])
        self.assertTrue(self.report["flags"]["orientation_magnitude_pinned_by_order"])
        ex = self.report["examples"]
        self.assertEqual(ex["2-chain"]["r_star"], 1.0)
        self.assertEqual(ex["V"]["r_star"], 0.7)
        self.assertEqual(ex["3-chain"]["r_star"], 0.57)
        self.assertEqual(ex["diamond"]["r_star"], 0.5)
        for name in ex:
            self.assertFalse(ex[name]["naive_glue_psd"])

    def test_signature_is_not_forced_by_the_pair_kernel_alone(self):
        self.assertFalse(self.report["flags"]["signature_forced_by_the_pair_kernel_alone"])
        self.assertTrue(self.report["flags"]["strong_positivity_couples_the_kernel_to_the_order"])

    def test_known_answer_two_by_two_obstruction(self):
        primary = primary_module()
        # Any comparable pair yields [[1, 1+i],[1-i, 1]] with determinant -1.
        self.assertAlmostEqual(primary._det([[1 + 0j, 1 + 1j], [1 - 1j, 1 + 0j]]), -1 + 0j)
        self.assertFalse(primary.hermitian_psd([[1 + 0j, 1 + 1j], [1 - 1j, 1 + 0j]], 1e-9))
        # Unimodular 2-chain is PSD at r <= 1.
        self.assertTrue(primary.hermitian_psd([[1 + 0j, 0 + 1j], [0 - 1j, 1 + 0j]], 1e-9))

    def test_known_answer_max_coherent_r(self):
        primary = primary_module()
        c3 = [[i < j for j in range(3)] for i in range(3)]
        self.assertEqual(primary.max_coherent_r(c3, 0.01, 1e-9), 0.57)

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
        self.assertEqual(capture["schema"], "qr05de-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
