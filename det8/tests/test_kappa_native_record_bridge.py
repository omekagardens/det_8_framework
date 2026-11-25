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
        self.assertEqual(adm_c4["p_D5_prep1_minus_prep0_on_11_exact"], "-9/44000")

        min_rel = res["minimal_relational_information_at_birth_5"]
        by_id = {item["scheme_id"]: item for item in min_rel["hierarchy"]}
        self.assertEqual(by_id["current_2bit_Y4_D4"]["n_cells"], 3)
        self.assertFalse(by_id["current_2bit_Y4_D4"]["all_cells_structurally_unaliased"])
        # Adding 1-bit counter-1 relay R_4 cuts max preparation discrepancy by >12x
        self.assertLess(
            by_id["current_2bit_plus_1bit_relay_R4"]["max_preparation_discrepancy"],
            by_id["current_2bit_Y4_D4"]["max_preparation_discrepancy"] / 12.0,
        )
        # Adding 2-bit relay state (N_{c=1}, is_min(c=1)) to ((Y_3,D_3),(Y_4,D_4)) resolves all 14/14 classes
        self.assertEqual(
            by_id["prior_plus_current_2bit_plus_2bit_relay_state"]["n_cells"], 14
        )
        self.assertTrue(
            by_id["prior_plus_current_2bit_plus_2bit_relay_state"][
                "all_cells_structurally_unaliased"
            ]
        )
        # Adding 1-bit committed root mark r_a = i restores 100% preparation invariance
        self.assertTrue(
            by_id["full_unaliased_relay_plus_1bit_root_mark"]["all_cells_prep_invariant"]
        )
        self.assertEqual(
            by_id["full_unaliased_relay_plus_1bit_root_mark"][
                "max_preparation_discrepancy"
            ],
            0.0,
        )

        no_standin = knrb.evaluate_admitted_next_birth_reusability_without_standin()
        self.assertFalse(no_standin["uses_half_scale_standin"])
        self.assertTrue(
            no_standin["birth5_on_admitted_C4"][
                "predicts_full_birth5_Y5_D5_R5_distribution_exactly"
            ]
        )
        self.assertEqual(
            no_standin["birth5_on_admitted_C4"][
                "dominant_H5_plus_C5_mass_fraction_by_prep"
            ][0],
            "349/352",
        )
        b6 = no_standin["birth6_on_admitted_H5_and_C5"]
        self.assertTrue(b6["H5_state_100_predicts_full_Y6_D6_R6_without_mu"])
        self.assertTrue(b6["C5_state_111_predicts_full_Y6_R6_without_mu"])
        self.assertTrue(b6["C5_D6_split_requires_canonical_carrier_mu_i"])

        row101 = no_standin["birth6_complete_row_sum_on_101_parents_K5_vs_Hsharp"]
        self.assertTrue(row101["c4_attachment_lands_in_101_with_full_on_both"])
        self.assertTrue(row101["sigma_i_and_beta_i_cancel_in_cell_101"])
        self.assertTrue(row101["all_three_carriers_cancel_in_joint_D6_R6"])
        self.assertTrue(row101["cell_100_agrees_identically"])
        self.assertTrue(row101["joint_D6_R6_agrees_identically"])
        self.assertTrue(row101["full_Y6_D6_R6_differs_on_001_vs_101"])
        self.assertTrue(
            row101["cell_001_diff_strictly_positive_for_all_nonnegative_gamma_ij"]
        )
        self.assertTrue(
            row101["ri41_certificate_direct_verification"]["sha256_verified"]
        )
        self.assertTrue(
            row101["ri63_certificate_carrier_specialization"]["sha256_verified"]
        )

        # Verify dynamically summed Birth-6 cells (both symbolic in (sigma_i, beta_i, gamma_{ij})
        # and RI-63 certificate-verified) for i=0 and i=1:
        p0 = row101["by_prep"][0]
        p1 = row101["by_prep"][1]
        self.assertEqual(
            p0["Hsharp_summed_Y6_D6_R6_cells_symbolic"]["(0, 0, 1)"],
            "(1)*(35/36)*g_ij*gamma_ij + (1255263/3520000)*theta",
        )
        self.assertEqual(
            p0["cell_001_difference_Hsharp_minus_K5_symbolic"],
            "(1)*(35/36)*g_ij*gamma_ij + (1887761/77440000)*theta",
        )
        self.assertEqual(
            p1["cell_001_difference_Hsharp_minus_K5_symbolic"],
            "(1)*(35/36)*g_ij*gamma_ij + (2579343/6050000)*theta",
        )
        self.assertEqual(
            p0["K5_summed_Y6_D6_R6_cells"]["(1, 0, 0)"],
            {"const": "0", "theta_coeff": "8077/70400"},
        )
        self.assertEqual(
            p0["Hsharp_summed_Y6_D6_R6_cells"]["(1, 0, 0)"],
            {"const": "0", "theta_coeff": "8077/70400"},
        )
        self.assertEqual(
            p1["K5_summed_Y6_D6_R6_cells"]["(1, 0, 0)"],
            {"const": "0", "theta_coeff": "40303/352000"},
        )
        self.assertEqual(
            p1["Hsharp_summed_Y6_D6_R6_cells"]["(1, 0, 0)"],
            {"const": "0", "theta_coeff": "40303/352000"},
        )
        self.assertEqual(
            p0["K5_summed_Y6_D6_R6_cells"]["(0, 0, 1)"],
            {"const": "0", "theta_coeff": "1029121/3097600"},
        )
        self.assertEqual(
            p0["Hsharp_summed_Y6_D6_R6_cells"]["(0, 0, 1)"],
            {"const": "35/36", "theta_coeff": "1255263/3520000"},
        )
        self.assertEqual(
            p0["cell_001_difference_Hsharp_minus_K5"]["const_diff_exact"],
            "35/36",
        )
        self.assertEqual(
            p0["cell_001_difference_Hsharp_minus_K5"]["theta_coeff_diff_exact"],
            "1887761/77440000",
        )
        self.assertTrue(
            p0["cell_001_difference_Hsharp_minus_K5"][
                "strictly_positive_for_all_nonnegative_gamma_ij"
            ]
        )
        self.assertEqual(
            p1["cell_001_difference_Hsharp_minus_K5"]["const_diff_exact"],
            "35/36",
        )
        self.assertEqual(
            p1["cell_001_difference_Hsharp_minus_K5"]["theta_coeff_diff_exact"],
            "2579343/6050000",
        )
        self.assertTrue(
            p1["cell_001_difference_Hsharp_minus_K5"][
                "strictly_positive_for_all_nonnegative_gamma_ij"
            ]
        )

        # Test A: Root counter c_a resolution where (Y_6, D_6, R_6) differs
        test_a = row101["test_A_root_counter_resolution"]
        self.assertEqual(test_a["K5_root_counter_c_a"], 3)
        self.assertEqual(test_a["Hsharp_root_counter_c_a"], 4)
        self.assertTrue(test_a["root_counter_resolves_K5_vs_Hsharp_at_birth6"])
        self.assertTrue(
            test_a["all_5_C4_children_uniquely_separated_by_Y5_D5_R5_ca"]
        )

        # Test B: Keep smaller record where K_5 and H^# agree at Birth 6, and test one birth deeper (Birth 7)
        test_b = row101["test_B_one_birth_deeper_at_birth7_for_agreed_readouts"]
        self.assertEqual(test_b["K6_100_counters"], (4, 3, 2, 0, 0, 0))
        self.assertEqual(test_b["H6_100_counters"], (0, 3, 2, 0, 0, 0))
        self.assertTrue(
            test_b["wrapped_root_on_H6_100_refires_R7_eq_1_on_all_nonempty_ideals"]
        )
        self.assertTrue(
            test_b["cell_000_possible_on_K6_100_for_every_admitted_birth7_law"]
        )
        self.assertFalse(
            test_b["cell_000_possible_on_H6_100_for_any_admitted_birth7_law"]
        )
        self.assertEqual(test_b["K6_100_legal_ideals_producing_000"], [[0, 1, 2]])
        self.assertEqual(test_b["H6_100_legal_ideals_producing_000"], [])
        self.assertFalse(
            test_b["smaller_record_agrees_at_birth7_on_shared_100_children_Y7_D7_R7"]
        )
        self.assertFalse(
            test_b["smaller_record_agrees_at_birth7_on_D7_R7_readout"]
        )
        self.assertEqual(test_b["K5_birth6_children_with_reachable_R7_eq_0"], "10/10")
        self.assertEqual(
            test_b["Hsharp_birth6_children_with_reachable_R7_eq_0"], "2/9"
        )
        b7_0 = test_b["by_prep"][0]
        self.assertTrue(b7_0["cell_000_reachable_on_K6_100"])
        self.assertFalse(b7_0["cell_000_reachable_on_H6_100"])
        self.assertEqual(
            b7_0["unnormalized_u_potential_ratio_D7eq0_R7eq0_K6_over_H6"],
            "75096511/3125",
        )

        nc = no_standin["birth6_non_closures"]
        self.assertFalse(nc["is_universal_fixed_dimension_markov_state"])
        self.assertTrue(nc["non_closure_1_mu_i_carrier_coupling_on_C5_D6"])
        self.assertTrue(nc["non_closure_2_counter3_vs_counter4_aliasing_C4uz_vs_Hsharp"])
        self.assertTrue(nc["non_closure_3_modulo5_counter_wrap_on_C6_vs_C5uw"])
        self.assertEqual(nc["shared_mod5_counter_multiset"], [0, 0, 1, 2, 3, 4])

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
