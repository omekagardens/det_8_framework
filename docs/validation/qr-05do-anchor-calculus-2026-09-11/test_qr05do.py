"""Bounded tests for QR-05DO (direction B, the anchor calculus)."""

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
    return _load("_qr05do_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05do_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def reference_module():
    return _load("_qr05do_test_reference", HERE / "reference.py")


@lru_cache(maxsize=1)
def cy_module():
    return _load("_qr05do_test_cy", HERE / "../qr-05cy-observational-quotient-2026-09-10/primary.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class AnchorCalculusTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def row(self, channels):
        return next(entry for entry in self.report["lattice"]
                    if entry["channels"] == list(channels))

    # ── the calculus as delivered ───────────────────────────────────────────

    def test_lattice_is_complete_and_all_flags_hold(self):
        self.assertEqual(len(self.report["lattice"]), 2 ** len(self.protocol["channels"]))
        self.assertEqual(sorted(set(self.report["lattice"][0]["targets"])),
                         ["absolute_scale", "conformal_factor", "dimension"])
        for name, value in self.report["flags"].items():
            self.assertTrue(value, name)

    def test_identifiability_is_monotone_on_every_one_step_refinement(self):
        self.assertEqual(self.report["monotonicity_violations"], [])
        # Known answer: a synthetic lattice with an identified set whose
        # refinement is not identified must be reported as a violation.
        rows = [
            {"channels": ["a"], "size": 1, "targets": {"t": {"verdict": "IDENTIFIED", "witness": None}}},
            {"channels": ["a", "b"], "size": 2, "targets": {"t": {"verdict": "NON_IDENTIFIABLE",
                                                                  "witness": ["w1", "w2"]}}},
        ]
        self.assertEqual(len(primary_module().monotonicity_violations(rows)), 1)

    def test_each_declared_direction_has_a_minimal_channel(self):
        minima = self.report["minimal_sets"]
        self.assertEqual(minima["absolute_scale"], [["anchor"]])
        self.assertEqual(minima["conformal_factor"], [["counts"]])
        self.assertIn(["order"], minima["dimension"])
        self.assertEqual(self.report["single_channel_identifying_sets"]["scale"], ["anchor"])
        self.assertEqual(self.report["single_channel_identifying_sets"]["conformal"], ["counts"])

    def test_the_joint_minimum_is_recorded_and_the_design_is_identifying(self):
        self.assertEqual(self.report["joint_k_min"], len(self.report["joint_minimal_sets"][0]))
        self.assertTrue(self.report["joint_minimal_sets"])
        design = self.report["one_channel_per_direction_design"]
        self.assertEqual(sorted(design), sorted(["order", "counts", "anchor"]))
        design_row = next(entry for entry in self.report["lattice"]
                          if sorted(entry["channels"]) == design)
        for target, verdict in design_row["targets"].items():
            self.assertEqual(verdict["verdict"], "IDENTIFIED", target)

    def test_the_accidental_separation_caveat_is_recorded(self):
        # More than one channel separates the dimension worlds on this finite
        # class, so the lattice minimum is smaller than the per-direction design.
        self.assertTrue(self.report["flags"][
            "a_declared_channel_separates_a_family_beyond_its_mechanism"])
        self.assertGreater(len(self.report["single_channel_identifying_sets"]["dimension"]), 1)
        self.assertLess(self.report["joint_k_min"], 3)

    def test_every_internal_reference_is_blind_on_the_witness_class(self):
        blindness = self.report["internal_reference_blindness"]
        self.assertTrue(blindness["internal_subsets_all_blind"])
        self.assertTrue(blindness["anchor_bearing_subsets_all_sighted"])
        self.assertTrue(blindness["control_channels_are_blind"])
        self.assertTrue(blindness["target_differs"])
        self.assertEqual(blindness["n_internal_subsets"], 16)
        self.assertEqual(blindness["n_anchor_bearing_subsets"], 16)

    def test_the_anchor_is_external_to_the_record_channel(self):
        anchor = self.report["anchor_check"]
        self.assertTrue(anchor["anchor_is_external"])
        self.assertTrue(anchor["anchor_separates_the_witness"])
        self.assertEqual(anchor["internal_channels_separating_the_witness"], [])

    def test_scale_is_not_identified_without_the_anchor(self):
        for entry in self.report["lattice"]:
            if "anchor" in entry["channels"]:
                continue
            self.assertEqual(entry["targets"]["absolute_scale"]["verdict"],
                             "NON_IDENTIFIABLE", entry["channels"])

    # ── known answers of the quotient machinery ─────────────────────────────

    def test_known_answer_a_target_varying_within_a_class_is_not_identified(self):
        worlds = [
            {"label": "w1", "obs": {"c": (1.0,)}, "targets": {"t": 0}},
            {"label": "w2", "obs": {"c": (1.0,)}, "targets": {"t": 1}},
        ]
        for module in (primary_module(), reference_module()):
            verdict, witness = module.classify(worlds, ["c"], "t")
            self.assertEqual(verdict, "NON_IDENTIFIABLE")
            self.assertEqual(witness, ["w1", "w2"])

    def test_known_answer_a_target_constant_on_the_class_is_identified(self):
        worlds = [
            {"label": "w1", "obs": {"c": (1.0,)}, "targets": {"t": 7}},
            {"label": "w2", "obs": {"c": (1.0,)}, "targets": {"t": 7}},
            {"label": "w3", "obs": {"c": (2.0,)}, "targets": {"t": 7}},
        ]
        primary, reference = primary_module(), reference_module()
        self.assertEqual(primary.classify(worlds, ["c"], "t"), ("IDENTIFIED", None))
        self.assertEqual(reference.classify(worlds, ["c"], "t"), ("IDENTIFIED", None))
        self.assertEqual(len(primary.partition(worlds, ["c"])), 2)
        self.assertEqual(len(reference.agreement_rows(worlds, ["c"])), 2)

    def test_known_answer_the_recoded_chain_distance_matches_the_fixture(self):
        # The reference route's re-coded longest-chain construction must agree
        # exactly with QR-05CY's, which the primary route imports.
        cy, reference = cy_module(), reference_module()
        t7 = reference.load_module("_qr05do_test_t7",
                                   HERE / "../../../det8/models/order_count_geometry.py")
        points = t7.sprinkle_diamond(2, self.protocol["n_base"], seed=self.protocol["seed"])
        order = sorted(range(len(points)), key=lambda i: points[i][0])
        self.assertEqual(reference.longest_chains(points, reference.causal_pairs(points), order),
                         cy.chain_matrix(cy.causality(points), order))

    def test_primary_reference_agree(self):
        _protocol, left, right = self.study.analyze_native()
        self.assertTrue(self.study.equivalent(left, right))
        self.assertEqual(self.study.encode(left), self.report)

    def test_frozen_fixtures_match_the_live_sources(self):
        import hashlib
        for name, record in self.study.freeze()["sources"].items():
            if name.startswith(".."):
                live = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                self.assertEqual(record["sha256"], live, name)

    def test_source_byte_limit(self):
        limit = self.protocol["limits"]["source_bytes"]
        for name in self.study.SOURCE_PATHS:
            self.assertLessEqual((HERE / name).stat().st_size, limit, name)

    def test_capture_matches_if_present(self):
        path = HERE / "results.json"
        if not path.exists():
            self.skipTest("capture not generated yet")
        capture = json.loads(path.read_bytes())
        self.assertEqual(capture["schema"], "qr05do-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
