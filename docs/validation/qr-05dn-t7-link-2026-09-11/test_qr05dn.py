"""Bounded tests for QR-05DN (the governed T7 link entry, direction J)."""

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
    return _load("_qr05dn_test_study", HERE / "study.py")


@lru_cache(maxsize=1)
def primary_module():
    return _load("_qr05dn_test_primary", HERE / "primary.py")


@lru_cache(maxsize=1)
def context():
    study = load_study()
    return study, study.load_protocol(), study.analyze()


class GovernedLinkTests(unittest.TestCase):
    def setUp(self):
        self.study, self.protocol, self.report = context()

    def synthetic(self, **overrides):
        """A copy of the live link entry, mutated for a known-answer failure mode."""
        entry = dict(self.report["link"])
        entry["all_evidence_statuses"] = list(
            primary_module().EVIDENCE_STATUS_VOCABULARY)
        entry["known_layers"] = ["RESEARCH_PROGRAM", "APPLICATION"]
        entry.update(overrides)
        return entry

    def check(self, entry):
        return primary_module().check_link(entry, self.protocol)["checks"]

    # ── the link as delivered ───────────────────────────────────────────────

    def test_link_is_a_first_class_scoped_correspondence_claim(self):
        flags = self.report["flags"]
        self.assertTrue(flags["the_link_is_a_first_class_scoped_registry_claim"])
        self.assertEqual(self.report["link"]["layer"], "CORRESPONDENCE")
        self.assertEqual(self.report["link"]["evidence_status"], "BOUNDED_CONDITIONAL_RESULT")
        self.assertIn("correspondence", self.report["link"]["title"].lower())

    def test_link_remains_gated_and_cannot_unlock_research(self):
        flags = self.report["flags"]
        self.assertTrue(flags["the_link_remains_gated_and_cannot_unlock_research"])
        self.assertEqual(self.report["link"]["development_status"], "DEFERRED")
        self.assertIsNone(self.report["link"]["priority"])
        self.assertNotIn("DET8-T7-LINK", self.report["registry"]["primary_development_sequence"])

    def test_estimator_is_not_promoted_by_the_link(self):
        flags = self.report["flags"]
        self.assertTrue(flags["the_t7_estimator_is_not_promoted_by_the_link"])
        self.assertEqual(self.report["registry"]["estimator_module_status"], "EXPERIMENTAL")
        self.assertNotIn(self.report["registry"]["estimator_module"],
                         self.report["link"]["supported_core_export_modules"])
        self.assertFalse(self.report["link"]["estimator_is_supported"])

    def test_link_names_the_o7_target_and_its_evidence_resolves(self):
        self.assertTrue(self.report["flags"]["the_link_names_the_o7_target_and_resolves_its_evidence"])
        anchor = self.protocol["required"]["o7_pointer_anchor"]
        self.assertIn(anchor, self.report["link"]["evidence_links"])
        for item in self.report["evidence_links"]:
            self.assertTrue(item["exists"], item["link"])
            self.assertIsNot(item["anchor_ok"], False, item["link"])

    def test_link_records_its_scope_and_open_gaps(self):
        self.assertTrue(self.report["flags"]["the_link_records_its_scope_and_open_gaps"])
        self.assertTrue(self.report["open_gaps"])
        for gap in self.report["open_gaps"]:
            self.assertTrue(gap["resolves"], gap["pointer"])
        self.assertTrue(self.report["spec"]["scope"]["not_claimed"])

    def test_no_new_evidence_status_vocabulary_is_introduced(self):
        self.assertTrue(self.report["flags"]["no_new_evidence_status_vocabulary_is_introduced"])
        self.assertFalse(self.report["comparison"]["new_evidence_status_introduced"])

    def test_the_new_layer_label_is_recorded_as_such(self):
        self.assertTrue(self.report["flags"]["a_new_layer_label_is_introduced_for_the_link"])
        self.assertTrue(self.report["comparison"]["new_layer_label_introduced"])
        # The link is the only claim in the CORRESPONDENCE layer: the new label is
        # introduced by this entry, not borrowed from another claim.
        claims = primary_module().load_module(
            "_qr05dn_test_claims", HERE / "../../../det8/claims.py")
        holders = [claim.claim_id for claim in claims.CLAIMS.values()
                   if claim.layer == "CORRESPONDENCE"]
        self.assertEqual(holders, ["DET8-T7-LINK"])

    def test_all_link_checks_pass(self):
        self.assertTrue(self.report["flags"]["all_link_checks_pass"])

    # ── known-answer failure modes of the governance contract ───────────────

    def test_known_answer_a_link_without_the_o7_pointer_is_rejected(self):
        anchor = self.protocol["required"]["o7_pointer_anchor"]
        entry = self.synthetic(
            evidence_links=[link for link in self.report["link"]["evidence_links"] if link != anchor])
        self.assertFalse(self.check(entry)["names_the_o7_target"])

    def test_known_answer_a_promoted_evidence_status_is_rejected(self):
        promoted = self.synthetic(evidence_status="VERIFIED_SOFTWARE_CONTRACT")
        self.assertFalse(self.check(promoted)["evidence_status_is_bounded_conditional"])
        invented = self.synthetic(all_evidence_statuses=["MANIFOLD_EMERGENCE_ESTABLISHED"])
        comparison = primary_module().check_link(invented, self.protocol)
        self.assertTrue(comparison["new_evidence_status_introduced"])

    def test_known_answer_a_sequenced_or_prioritised_link_is_rejected(self):
        sequenced = self.synthetic(in_development_sequence=True)
        self.assertFalse(self.check(sequenced)["not_in_the_primary_development_sequence"])
        prioritised = self.synthetic(priority=5)
        self.assertFalse(self.check(prioritised)["priority_is_null"])

    def test_known_answer_a_promoted_estimator_is_rejected(self):
        exported = self.synthetic(
            supported_core_export_modules=self.report["link"]["supported_core_export_modules"]
            + [self.report["registry"]["estimator_module"]])
        self.assertFalse(
            self.check(exported)["estimator_is_absent_from_the_supported_core_exports"])
        supported = self.synthetic(estimator_is_supported=True)
        self.assertFalse(self.check(supported)["estimator_does_not_classify_as_supported"])

    def test_known_answer_a_deferred_status_that_is_not_deferred_is_rejected(self):
        active = self.synthetic(development_status="ACTIVE_DEVELOPMENT")
        self.assertFalse(self.check(active)["development_status_remains_deferred"])

    def test_known_answer_unresolvable_evidence_or_gap_is_rejected(self):
        broken = self.synthetic(evidence_links=["docs/track_b/DOES_NOT_EXIST.md"])
        self.assertFalse(self.check(broken)["evidence_links_resolve"])

    # ── routes and artifacts ────────────────────────────────────────────────

    def test_primary_reference_agree(self):
        _protocol, left, right = self.study.analyze_native()
        self.assertTrue(self.study.equivalent(left, right))
        self.assertEqual(self.study.encode(left), self.report)

    def test_frozen_fixture_hash_matches_the_live_registry(self):
        import hashlib
        frozen = self.study.freeze()["sources"]["../../../det8/claims.py"]
        live = hashlib.sha256((HERE / "../../../det8/claims.py").read_bytes()).hexdigest()
        self.assertEqual(frozen["sha256"], live)

    def test_source_byte_limit(self):
        limit = self.protocol["limits"]["source_bytes"]
        for name in self.study.SOURCE_PATHS:
            self.assertLessEqual((HERE / name).stat().st_size, limit, name)

    def test_capture_matches_if_present(self):
        path = HERE / "results.json"
        if not path.exists():
            self.skipTest("capture not generated yet")
        capture = json.loads(path.read_bytes())
        self.assertEqual(capture["schema"], "qr05dn-capture-v1")
        self.assertEqual(capture["report"], self.report)


if __name__ == "__main__":
    unittest.main()
