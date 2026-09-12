"""Bounded tests for QR-05DM (stronger adversary / interval abundance)."""

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
    return _load("_qr05dm_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dm_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05dm_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


def abundance(module, order, sizes, cap, seed):
    """Dispatch a boolean matrix to the route's own representation.

    The primary route carries the order as bitmask rows; the reference route as
    a boolean matrix.  The sampling (shuffle + per-size cap) is identical.
    """
    n = len(order)
    if hasattr(module, "pred_from_succ"):  # bitmask route
        succ = [sum(1 << j for j in range(n) if order[i][j]) for i in range(n)]
        return module.interval_abundance(succ, module.pred_from_succ(succ, n), n, sizes, cap, seed)
    return module.interval_abundance(order, n, sizes, cap, seed)


class StrongerAdversaryTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def row(self, name):
        return next(r for r in self.report["objects"] if r["object"] == name)

    def comparison(self, name):
        return next(c for c in self.report["comparisons"] if c["adversary"] == name)

    def test_adversaries_are_two_point_matched(self):
        self.assertTrue(self.report["flags"]["the_adversaries_are_two_point_matched"])
        for comp in self.report["comparisons"]:
            self.assertLessEqual(comp["f_gap"], 0.01, comp["adversary"])

    def test_sprinkle_abundance_windows_are_populated(self):
        self.assertTrue(self.report["flags"]["sprinkle_abundance_windows_are_populated"])
        for name in ("sprinkle_d2", "sprinkle_d3"):
            self.assertTrue(all(c > 0 for c in self.row(name)["abundance_count"]), name)

    def test_two_point_matched_laws_fail_the_abundance_test(self):
        self.assertTrue(self.report["flags"][
            "two_point_matched_geometry_free_laws_fail_the_abundance_test"])
        self.assertTrue(self.report["flags"]["the_matched_closure_dense_law_fails_the_abundance_test"])
        self.assertTrue(self.report["flags"]["the_matched_ladder_law_fails_the_abundance_test"])
        for comp in self.report["comparisons"]:
            self.assertTrue(comp["fails_the_abundance_test"], comp["adversary"])

    def test_the_mean_self_similarity_is_not_enough(self):
        # The substantive claim: a matched geometry-free law can sit inside QR-05DL's
        # mean self-similarity band and still be separated by the interval abundance.
        self.assertTrue(self.report["flags"][
            "interval_abundance_is_stricter_than_the_self_similarity_mean"])
        stricter = [c for c in self.report["comparisons"]
                    if c["adversary"] != "" and 0.8 <= (self.row(c["adversary"])["self_similarity"] or -1)
                    <= 1.7 and c["fails_the_abundance_test"]]
        self.assertTrue(stricter)
        for comp in stricter:
            self.assertTrue(comp["mean_fail_sizes"] or comp["hist_fail_sizes"]
                            or comp["adversary_has_no_intervals_in_window"], comp["adversary"])

    def test_no_go_is_not_established(self):
        self.assertFalse(self.report["flags"]["a_no_go_is_established"])

    def test_known_answer_chain_abundance(self):
        n = 12
        chain = [[i < j for j in range(n)] for i in range(n)]
        for module in (primary_module(), reference_module()):
            rho, stats, overall = abundance(module, chain, [3, 5, 7, 9], 50, 0)
            self.assertAlmostEqual(rho, (n - 2) / n, places=9)   # links have empty intervals
            self.assertGreater(overall["count"], 0)
            for size in (3, 5, 7, 9):
                self.assertGreater(stats[size]["count"], 0)
                self.assertAlmostEqual(stats[size]["mean"], 1.0, places=9)  # intervals are chains
                self.assertAlmostEqual(stats[size]["sd"], 0.0, places=9)

    def test_known_answer_bipartite_has_no_intervals(self):
        n = 12
        order = [[i < n // 2 <= j for j in range(n)] for i in range(n)]
        for module in (primary_module(), reference_module()):
            rho, stats, overall = abundance(module, order, [3, 5], 50, 0)
            self.assertEqual(rho, 0.0)
            self.assertEqual(overall["count"], 0)
            for size in (3, 5):
                self.assertEqual(stats[size]["count"], 0)

    def test_known_answer_ladder_with_antichain_blocks_is_bipartite(self):
        # p_intra = 0 collapses the two-block ladder onto QR-05DK's complete bipartite
        # order, in both routes.
        n = 32
        primary, reference = primary_module(), reference_module()
        bits = primary.ladder_bits(n, 2, 0.0, seed=3)
        self.assertEqual(bits, primary.bipartite_bits(n))
        matrix = reference.ladder_matrix(n, 2, 0.0, seed=3)
        self.assertEqual(matrix, reference.bipartite_matrix(n))

    def test_known_answer_histogram_bins(self):
        for module in (primary_module(), reference_module()):
            self.assertEqual(module._hist([0.0, 0.5, 1.0]), [1 / 3, 0.0, 0.0, 0.0, 0.0,
                                                            1 / 3, 0.0, 0.0, 0.0, 1 / 3])
            self.assertEqual(sum(module._hist([0.1, 0.2, 0.3, 0.4])), 1.0)

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
        self.assertEqual(capture["schema"], "qr05dm-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
