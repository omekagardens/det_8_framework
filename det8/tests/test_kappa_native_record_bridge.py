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

    def test_successive_birth_unconditional_readouts_retain_quenched_and_surviving_branches(
        self,
    ) -> None:
        uncond = knrb.evaluate_successive_birth_unconditional_readouts()
        self.assertTrue(uncond["all_branches_retained_at_every_birth"])
        self.assertTrue(uncond["history_effect_survives_unconditional_averaging"])

        z_traj = uncond["antichain_Z_n_across_births_1_to_4"]
        self.assertEqual(
            z_traj["contrasts_by_birth_exact"],
            ["0", "1/12672", "5/25344", "263/1115136"],
        )
        self.assertTrue(z_traj["survives_at_n4"])
        for step in z_traj["steps"]:
            self.assertEqual(
                Fraction(step["p_surviving_s_pos_exact"])
                + Fraction(step["p_quenched_s_pos_exact"]),
                Fraction(1, 1),
            )
            self.assertEqual(
                Fraction(step["p_surviving_s_neg_exact"])
                + Fraction(step["p_quenched_s_neg_exact"]),
                Fraction(1, 1),
            )

        d_res_traj = uncond["total_chain_D_n_residual_across_births_1_to_4"]
        self.assertEqual(
            d_res_traj["contrasts_by_birth_exact"],
            ["0", "-1/6336", "-19/190080", "-779/8363520"],
        )
        self.assertTrue(d_res_traj["survives_after_local_coupling_quenched"])

        d_mark_traj = uncond["total_chain_D_n_mark_across_births_2_to_4"]
        self.assertEqual(
            d_mark_traj["contrasts_by_birth_exact"],
            ["0", "-1/6", "-41/264"],
        )
        self.assertTrue(d_mark_traj["survives_at_n4"])

        y_mark_traj = uncond["counter_two_Y_n_mark_across_births_2_to_4"]
        self.assertEqual(
            y_mark_traj["contrasts_by_birth_exact"],
            ["0", "0", "-7/44"],
        )
        self.assertTrue(y_mark_traj["cancels_at_birth_3_under_branch_averaging"])
        self.assertTrue(
            y_mark_traj["re_emerges_at_birth_4_via_asymmetric_fork_quenching"]
        )

    def test_independently_enumerated_kernel_and_two_bit_sufficiency_birth4_vs_birth5(
        self,
    ) -> None:
        res = knrb.evaluate_independently_enumerated_kernel_and_two_bit_sufficiency()
        self.assertTrue(res["enumerated_15_branch_kernel_matches_ledger"])
        self.assertEqual(res["total_birth4_branches"], 15)
        self.assertEqual(res["total_birth5_ideal_continuations"], 119)

        b34 = res["birth_3_to_4_two_bit_model"]
        self.assertTrue(b34["two_bits_suffice_at_birth_4"])
        self.assertEqual(
            b34["p_Y4_eq_1_given_Y3_D3_exact"],
            {
                "edge_plus_isolate_00": "21/22",
                "fork_10": "1/44",
                "three_chain_11": "43/44",
            },
        )
        self.assertEqual(b34["reconstructed_P0_Y4_exact"], "179/220")
        self.assertEqual(b34["reconstructed_P1_Y4_exact"], "36/55")

        b45 = res["birth_4_to_5_two_bit_test"]
        self.assertFalse(b45["two_bits_suffice_at_birth_5"])
        self.assertEqual(
            b45["branches_per_cell_at_birth_4"],
            {"(Y4=0, D4=0)": 7, "(Y4=1, D4=0)": 7, "(Y4=1, D4=1)": 1},
        )
        half_diff = b45["p_Y5_eq_1_given_Y4_D4_half_scale"]["prep1_minus_prep0_exact"]
        self.assertNotEqual(half_diff["(0,0)"], "0")
        self.assertNotEqual(half_diff["(1,0)"], "0")
        adm_c4 = b45["p_Y5_eq_1_given_Y4_D4_admitted_C4"]
        self.assertEqual(adm_c4["prep_0_on_11_exact"], "351/352")
        self.assertEqual(adm_c4["prep_1_on_11_exact"], "5473/5500")
        self.assertEqual(adm_c4["prep1_minus_prep0_on_11_exact"], "-91/44000")
        self.assertEqual(adm_c4["p_D5_prep1_minus_prep0_on_11_exact"], "-41/22000")

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
