"""Invented deterministic inputs only; no scientific review or native endpoints.

The trust=True path SIMULATES a trusted caller to test software control flow.
It supplies no accepted scientific premise. No sampling or acquisition occurs.
"""

from copy import deepcopy
from dataclasses import FrozenInstanceError
from fractions import Fraction
from hashlib import sha256
import json
import unittest
from unittest.mock import patch

from det8.models import envelope_admission as adapter


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def synthetic_fixture():
    artifacts = {role: ("SYNTHETIC UNVERIFIED " + role).encode("ascii")
                 for role, _ in adapter.REFERENCE_CLAIMS}
    comparison = {
        "schema": "d4a-frozen-comparison-v1",
        "protocol": "approximate-certificate-A",
        "selection": "pre-held-out-fixed-comparison",
        "target": adapter.canonical_d4a_target(),
        "references": {role: {"sha256": sha256(artifacts[role]).hexdigest(), "claim": claim}
                       for role, claim in adapter.REFERENCE_CLAIMS},
        "budgets": {
            "B": {"proxy": [1, 1], "bit_width": 8, "rounding": [1, 1]},
            "Q": {"proxy": [1, 1], "bit_width": 8, "rounding": [1, 1]},
            "other_certificate_risk": [0, 1], "kappa_budget": [1, 25],
            "max_intermediate_bits": adapter.REQUIRED_PRECISION_BITS,
            "max_work_bits": adapter.REQUIRED_WORK_BITS,
        },
    }
    descriptor = {
        "schema": "d4a-full-row-envelope-v1",
        "comparison_sha256": "", "review_scope_sha256": "",
        "target": adapter.canonical_d4a_target(),
        "outcome_dictionary": adapter.canonical_d4a_outcomes(),
        "arms": {arm: {
            "arm": arm,
            "endpoints": [{"lower": [1, 22], "upper": [1, 22]} for _ in range(22)],
            "coverage": {"mode": "deterministic", "scope": "simultaneous-full-unconditional-joint-row",
                         "selection": "pre-held-out-fixed-comparison", "failure": [0, 1]},
            "evidence": {"derivation": arm + "_enclosure", "coverage": arm + "_coverage"},
        } for arm in ("B", "Q")},
    }
    return descriptor, comparison, artifacts


def bind(descriptor, comparison):
    comparison_raw = encode(comparison)
    descriptor["comparison_sha256"] = sha256(comparison_raw).hexdigest()
    scope = {key: value for key, value in descriptor.items() if key != "review_scope_sha256"}
    descriptor["review_scope_sha256"] = sha256(encode(scope)).hexdigest()
    return encode(descriptor), comparison_raw


class TestEnvelopeAdmission(unittest.TestCase):
    def setUp(self):
        self.descriptor, self.comparison, self.artifacts = synthetic_fixture()

    def admit(self, trust=True):
        raw, comparison_raw = bind(self.descriptor, self.comparison)
        return adapter.admit_d4a_envelope(raw, comparison_raw, self.artifacts,
                                          trusted_review_applicable=trust)

    def refuses(self, expected, result=None):
        result = self.admit() if result is None else result
        self.assertEqual(result.status, expected)
        self.assertEqual(result.operational_admission, "ABSTAIN")
        self.assertTrue(result.reasons)
        self.assertEqual(result.arms, ())
        return result

    def wide(self, arm="B"):
        self.descriptor["arms"][arm]["endpoints"] = [
            {"lower": [0, 1], "upper": [1, 11]} for _ in range(22)]

    def test_regenerates_all_eleven_ideals_and_twenty_two_ordered_outcomes(self):
        masks = [0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63]
        self.assertEqual(adapter.canonical_d4a_outcomes(), [[m, b] for m in masks for b in (0, 1)])

    def test_synthetic_factory_and_map_witnesses_always_abstain(self):
        with patch.object(adapter.CategoricalMap, "map_word", side_effect=AssertionError("no draw")):
            result = self.admit()
        self.assertEqual(result.status, "COMPONENT_PREMISES_REVIEWED")
        self.assertEqual(result.operational_admission, "ABSTAIN")
        self.assertEqual(len(result.operational_reasons), 4)
        self.assertEqual(len(result.arms), 2)
        for arm in result.arms:
            self.assertEqual(arm.envelope.certificate.proxy_weights, (Fraction(1, 22),) * 22)
            self.assertEqual(arm.envelope.certificate.tv_bound, 0)
            self.assertEqual(arm.categorical_map.cell_counts, (12,) * 14 + (11,) * 8)
            self.assertEqual(arm.categorical_map.rounding_tv, Fraction(7, 352))
            self.assertIsNone(arm.envelope.provenance_reference)

    def test_digest_strings_cannot_unlock_factory(self):
        raw, comp = bind(self.descriptor, self.comparison)
        with patch.object(adapter, "certify_probability_envelope", side_effect=AssertionError("untrusted")) as factory:
            for kwargs in ({}, {"trusted_review_applicable": False}, {"trusted_review_applicable": "accepted"},
                           {"trusted_review_applicable": 1}):
                self.refuses("ABSTAIN_COVERAGE_OR_REVIEW", adapter.admit_d4a_envelope(raw, comp, self.artifacts, **kwargs))
            factory.assert_not_called()

    def test_factory_receives_original_arrays_after_trust(self):
        self.wide()
        factory = adapter.certify_probability_envelope
        with patch.object(adapter, "certify_probability_envelope", wraps=factory) as calls:
            result = self.admit()
        self.assertEqual(result.status, "COMPONENT_PREMISES_REVIEWED")
        self.assertEqual(calls.call_count, 2)
        self.assertEqual(calls.call_args_list[0].args[1], (Fraction(0),) * 22)
        self.assertEqual(calls.call_args_list[0].args[2], (Fraction(1, 11),) * 22)
        self.assertEqual(result.arms[0].original_lower, ((0, 1),) * 22)
        self.assertEqual(result.arms[0].original_upper, ((1, 11),) * 22)
        self.assertEqual(result.arms[0].envelope.certificate.tv_bound, Fraction(1, 2))

    def test_exact_input_bytes_and_immutable_copies_retained(self):
        result = self.admit()
        original = result.descriptor_bytes
        self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = [0, 1]
        self.artifacts["B_enclosure"] = b"changed after call"
        self.assertEqual(result.descriptor_bytes, original)
        self.assertEqual(dict(result.reference_bytes)["B_enclosure"], b"SYNTHETIC UNVERIFIED B_enclosure")
        self.assertEqual(result.arms[0].original_lower[0], (1, 22))
        with self.assertRaises(FrozenInstanceError):
            result.status = "PASS"

    def test_exact_comparison_and_artifact_bytes_are_bound(self):
        raw, comp = bind(self.descriptor, self.comparison)
        self.refuses("ABSTAIN_BINDING", adapter.admit_d4a_envelope(raw, comp + b" ", self.artifacts, trusted_review_applicable=True))
        for role in self.artifacts:
            changed = dict(self.artifacts, **{role: self.artifacts[role] + b" "})
            self.refuses("ABSTAIN_BINDING", adapter.admit_d4a_envelope(raw, comp, changed, trusted_review_applicable=True))

    def test_stale_endpoint_review_binding_refuses(self):
        raw, comp = bind(self.descriptor, self.comparison)
        self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = [0, 1]
        self.refuses("ABSTAIN_COVERAGE_OR_REVIEW", adapter.admit_d4a_envelope(encode(self.descriptor), comp, self.artifacts, trusted_review_applicable=True))

    def test_target_parameters_parent_marking_and_embedding_cannot_change(self):
        original = deepcopy(self.descriptor)
        for key, value in (("lambda", [2, 1]), ("epsilon", [1, 3]), ("z1", [1, 2]),
                           ("old_bits", [1, 0, 0, 0, 0, 0]), ("labels", ["c0", "c1", "c2", "c3", "a0", "a1"]),
                           ("sector", "conditional-supported-classes"), ("embedding_reference", "another-parent")):
            self.descriptor = deepcopy(original)
            self.descriptor["target"][key] = value
            self.refuses("ABSTAIN_TARGET_OR_COMPLETENESS")

    def test_row_count_is_not_completeness_and_no_reordering_or_prefix_dropping(self):
        row = adapter.canonical_d4a_outcomes()
        for wrong in (row[6:], row[::-1], [row[1]] + row[1:], row[:-1], row + [row[-1]]):
            self.descriptor["outcome_dictionary"] = wrong
            self.refuses("ABSTAIN_ROW_DICTIONARY")

    def test_missing_endpoint_slot_refuses_and_upper_zero_conflicts_with_target(self):
        self.descriptor["arms"]["B"]["endpoints"].pop()
        self.refuses("ABSTAIN_ROW_COMPLETENESS")
        self.wide()
        self.descriptor["arms"]["B"]["endpoints"][0] = {"lower": [0, 1], "upper": [0, 1]}
        self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")

    def test_original_box_infeasibility(self):
        self.descriptor["arms"]["B"]["endpoints"] = [{"lower": [1, 11], "upper": [1, 10]} for _ in range(22)]
        self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")

    def test_fair_bit_disjoint_intervals_are_not_averaged(self):
        self.wide()
        self.descriptor["arms"]["B"]["endpoints"][:2] = [
            {"lower": [0, 1], "upper": [1, 100]}, {"lower": [1, 50], "upper": [1, 25]}]
        result = self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")
        self.assertEqual(result.reasons[0].field, "B.fair_bit")

    def test_local_overlap_without_normalized_fair_bit_row_refuses(self):
        for pair in (({"lower": [1, 20], "upper": [1, 10]}, {"lower": [0, 1], "upper": [1, 10]}),
                     ({"lower": [0, 1], "upper": [1, 10]}, {"lower": [0, 1], "upper": [1, 100]})):
            self.descriptor["arms"]["B"]["endpoints"] = [deepcopy(pair[i % 2]) for i in range(22)]
            result = self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")
            self.assertEqual(result.reasons[0].field, "B.fair_bit")

    def test_rational_pairs_are_exact_reduced_bounded_and_ordered(self):
        for pair in ([2, 44], [1, 0], [-1, 22], [23, 22], [1], "1/22", [1, 22, 1]):
            self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = pair
            self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")
        self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = [1, 11]
        self.refuses("ABSTAIN_ENDPOINT_SEMANTICS")
        self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = [1, 2**256]
        self.refuses("ABSTAIN_RESOURCE")

    def test_float_bool_null_and_nonfinite_json_are_rejected(self):
        for value in (True, False, None, 0.5, float("nan"), float("inf")):
            self.descriptor["arms"]["B"]["endpoints"][0]["lower"] = [value, 22]
            self.refuses("ABSTAIN_SCHEMA")

    def test_duplicate_unknown_and_missing_fields_refuse(self):
        raw, comp = bind(self.descriptor, self.comparison)
        duplicate = b'{"schema":"d4a-full-row-envelope-v1",' + raw[1:]
        self.refuses("ABSTAIN_SCHEMA", adapter.admit_d4a_envelope(duplicate, comp, self.artifacts))
        duplicate_nested = raw.replace(b'"lower":[1,22]', b'"lower":[1,22],"lower":[1,22]', 1)
        self.refuses("ABSTAIN_SCHEMA", adapter.admit_d4a_envelope(duplicate_nested, comp, self.artifacts))
        self.descriptor["arms"]["B"]["coverage"]["reviewer"] = "accepted"
        self.refuses("ABSTAIN_SCHEMA")
        del self.descriptor["arms"]["B"]["coverage"]["reviewer"]
        del self.descriptor["arms"]["Q"]
        self.refuses("ABSTAIN_SCHEMA")

    def test_plain_types_reject_adapters_without_running_hooks(self):
        class Bomb:
            def __str__(self):
                raise AssertionError("hook")
            def __iter__(self):
                raise AssertionError("hook")
        class BytesSubclass(bytes):
            pass
        class DictSubclass(dict):
            pass
        raw, comp = bind(self.descriptor, self.comparison)
        for bad in (Bomb(), BytesSubclass(raw), memoryview(raw), bytearray(raw), raw.decode()):
            self.refuses("ABSTAIN_SCHEMA", adapter.admit_d4a_envelope(bad, comp, self.artifacts))
        self.refuses("ABSTAIN_SCHEMA", adapter.admit_d4a_envelope(raw, comp, DictSubclass(self.artifacts)))
        self.artifacts["B_coverage"] = Bomb()
        self.refuses("ABSTAIN_SCHEMA", adapter.admit_d4a_envelope(raw, comp, self.artifacts))

    def test_byte_depth_text_node_and_item_limits(self):
        raw, comp = bind(self.descriptor, self.comparison)
        for bad in (b" " * (adapter.MAX_JSON_BYTES + 1), b"[" * 11 + b"0" + b"]" * 11,
                    encode("x" * 257), encode([0] * 65), encode([[0] * 64] * 32)):
            self.refuses("ABSTAIN_RESOURCE", adapter.admit_d4a_envelope(bad, comp, self.artifacts))
        with patch.object(adapter.json, "loads", side_effect=AssertionError("must reject before parser")) as loader:
            self.refuses("ABSTAIN_RESOURCE", adapter.admit_d4a_envelope(b"[" * 11, comp, self.artifacts))
            loader.assert_not_called()
        self.artifacts["B_coverage"] = b"x" * (adapter.MAX_ARTIFACT_BYTES + 1)
        self.refuses("ABSTAIN_RESOURCE", adapter.admit_d4a_envelope(raw, comp, self.artifacts))

    def test_invalid_encoding_json_and_integer_token_refuse(self):
        raw, comp = bind(self.descriptor, self.comparison)
        for bad in (b"\xff", b"{", b"", b'{"x":01}', raw.decode().encode("utf-16-le")):
            result = adapter.admit_d4a_envelope(bad, comp, self.artifacts)
            self.assertIn(result.status, ("ABSTAIN_SCHEMA", "ABSTAIN_RESOURCE"))
        self.refuses("ABSTAIN_RESOURCE", adapter.admit_d4a_envelope(b"[" + b"9" * 10000 + b"]", comp, self.artifacts))

    def test_reference_claims_arm_bindings_and_coverage_scope_cannot_change(self):
        for section, key, value, expected in (
                (self.descriptor["arms"]["B"], "arm", "Q", "ABSTAIN_BINDING"),
                (self.descriptor["arms"]["B"], "evidence", {"derivation": "Q_enclosure", "coverage": "B_coverage"}, "ABSTAIN_BINDING"),
                (self.descriptor["arms"]["B"]["coverage"], "scope", "marginal-only", "ABSTAIN_PROOF_SCOPE"),
                (self.descriptor["arms"]["B"]["coverage"], "selection", "after-success", "ABSTAIN_PROOF_SCOPE")):
            original = section[key]
            section[key] = value
            self.refuses(expected)
            section[key] = original
        self.comparison["references"]["B_enclosure"]["claim"] = "different law"
        self.refuses("ABSTAIN_BINDING")

    def test_risk_is_summed_in_kappa_never_added_to_eta(self):
        for arm in ("B", "Q"):
            self.descriptor["arms"][arm]["coverage"].update(mode="statistical", failure=[1, 100])
            self.comparison["budgets"][arm]["proxy"] = [0, 1]
        self.comparison["budgets"]["other_certificate_risk"] = [1, 100]
        self.comparison["budgets"]["kappa_budget"] = [3, 100]
        result = self.admit()
        self.assertEqual(result.status, "COMPONENT_PREMISES_REVIEWED")
        self.assertEqual(result.endpoint_failure_sum, Fraction(1, 50))
        self.assertEqual(result.total_certificate_risk, Fraction(3, 100))
        self.assertEqual([a.envelope.certificate.tv_bound for a in result.arms], [0, 0])
        self.comparison["budgets"]["kappa_budget"] = [1, 50]
        self.refuses("ABSTAIN_RISK_BUDGET")
        self.comparison["budgets"]["kappa_budget"] = [1, 20]
        self.refuses("ABSTAIN_RISK_BUDGET")

    def test_deterministic_label_does_not_override_risk_requirement(self):
        self.descriptor["arms"]["B"]["coverage"]["failure"] = [1, 100]
        self.refuses("ABSTAIN_COVERAGE_OR_REVIEW")

    def test_resource_preflight_before_factory_and_rational_array_arithmetic(self):
        for name in ("max_intermediate_bits", "max_work_bits"):
            original = self.comparison["budgets"][name]
            self.comparison["budgets"][name] = original - 1
            with patch.object(adapter, "certify_probability_envelope") as factory, patch.object(adapter, "Fraction") as fraction:
                self.refuses("ABSTAIN_RESOURCE")
                factory.assert_not_called()
                fraction.assert_not_called()
            self.comparison["budgets"][name] = original

    def test_proxy_and_rounding_refusals_expose_no_partial_component(self):
        self.wide("Q")
        self.comparison["budgets"]["Q"]["proxy"] = [0, 1]
        self.refuses("ABSTAIN_BUDGET")
        self.comparison["budgets"]["Q"]["proxy"] = [1, 1]
        self.comparison["budgets"]["Q"].update(bit_width=0, rounding=[0, 1])
        self.refuses("ABSTAIN_ROUNDING_BUDGET")

    def test_unexpected_failure_and_interrupt_are_non_admission(self):
        for error in (RuntimeError("synthetic factory failure"), MemoryError()):
            with patch.object(adapter, "certify_probability_envelope", side_effect=error):
                self.refuses("ABSTAIN_EXCEPTION")
        with patch.object(adapter, "certify_probability_envelope", side_effect=KeyboardInterrupt()), self.assertRaises(KeyboardInterrupt):
            self.admit()


if __name__ == "__main__":
    unittest.main()
