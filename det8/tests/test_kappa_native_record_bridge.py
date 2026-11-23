"""Unit tests for det8.models.kappa_native_record_bridge."""

from __future__ import annotations

from fractions import Fraction
import unittest

from det8.models import kappa_native_record_bridge as knrb


class TestKappaNativeRecordBridge(unittest.TestCase):
    def test_four_birth_active_residual_witness_and_pure_update_contraction(self) -> None:
        res = knrb.evaluate_four_birth_native_kappa()
        witness = res["witness_identities"]
        self.assertTrue(witness["matches_1_over_6336"])
        self.assertTrue(witness["matches_1_over_25344"])
        self.assertEqual(witness["update_over_current_ratio"], "1/4")

        pure = res["pure_residual_update_contraction"]
        self.assertEqual(pure["contraction_rate_t_per_step"], 0.5)
        self.assertTrue(pure["shrinks_monotonically_at_fixed_prefix"])
        self.assertTrue(pure["inactive_controls_identically_zero"])
        self.assertAlmostEqual(
            pure["fixed_mark_readout_ratio_Z_over_D"], -3945.0 / 779.0, places=9
        )

    def test_four_birth_structural_stepping_and_rank2_readouts(self) -> None:
        res = knrb.evaluate_four_birth_native_kappa()
        stepping = res["structural_birth_stepping"]["two_chain_mark_stepping"]
        self.assertTrue(stepping["all_n3_branches_shrink_vs_n2"])
        self.assertFalse(stepping["uniform_exponential_across_branches"])
        self.assertEqual(stepping["kappa_fr_n3_given_S3_full_3chain"], 0.0)
        self.assertGreater(stepping["kappa_fr_n3_given_S3_root_fork"], 0.10)
        self.assertGreater(stepping["kappa_fr_n3_given_S3_empty_edge_isolate"], 0.04)

        rank_test = res["two_readout_scalar_test"]
        self.assertEqual(rank_test["pure_residual_only_rank"], 1)
        self.assertEqual(rank_test["combined_mark_and_residual_rank"], 2)
        self.assertFalse(rank_test["one_scalar_works_across_readouts"])
        self.assertEqual(rank_test["two_chain_n2_contrast_D_exact"], "-41/264")
        self.assertEqual(rank_test["two_chain_n2_contrast_Y_exact"], "-7/44")
        self.assertEqual(rank_test["two_chain_Y_over_D_ratio_exact"], "42/41")
        self.assertGreater(rank_test["gram_determinant_Z_vs_D"], 0.0)

    def test_qr05do_interaction_scale_quotient_anchor_blindness(self) -> None:
        do_res = knrb.evaluate_qr05do_interaction_scale_quotient()
        self.assertEqual(do_res["n_subsets"], 32)
        self.assertEqual(do_res["monotonicity_violations"], 0)
        self.assertEqual(do_res["anchor_free_subsets_total"], 16)
        self.assertEqual(do_res["anchor_free_blind_on_scale_witness"], 16)
        self.assertEqual(do_res["anchor_bearing_sighted_on_scale_witness"], 16)
        self.assertFalse(do_res["scale_identifiable_on_any_anchor_free_subset"])
        self.assertEqual(
            do_res["minimal_identifying_sets_for_mass_per_area_scale"], [["anchor"]]
        )

    def test_qr05cr_two_region_conservative_flux_audit(self) -> None:
        cr_res = knrb.evaluate_qr05cr_two_region_flux_audit()
        self.assertTrue(cr_res["constant_annihilation_passed"])
        self.assertTrue(cr_res["divergence_conserves_flux"])
        self.assertTrue(cr_res["pointwise_violates_flux_balance"])
        self.assertGreater(cr_res["response_boost_factor"], 1.5)
        self.assertLess(cr_res["explicit_source_max_residual"], 1e-14)
        self.assertLess(cr_res["kernel_moment_coefficient_error"], 1e-14)
        self.assertTrue(cr_res["added_source_control_detected"])


if __name__ == "__main__":
    unittest.main()
