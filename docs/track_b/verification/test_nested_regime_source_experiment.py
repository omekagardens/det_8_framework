"""
test_nested_regime_source_experiment.py

Comprehensive Unit & Mathematical Property Test Suite (18 tests) for Stage 8:
  - Five interval structural observables (antichain, total chain, bipartite crown)
  - Myrheim-Meyer exact evaluations & bisection inversion
  - Vectorized Minkowski & Rideout-Sorkin CSG transitivity invariants
  - Proposition 1.1: Exact 1D Future-Cone Markov chain vs full poset enumeration & MC
  - Pillar 1: 4D Minkowski vs Log-Quadratic transverse entry-width separation
  - Theorem 2.1: Coarse projection diamond commutation, omitted-chain non-Markovianity
    R_branch(m) = Z_{m+1} - 1, and shadow-volume Z_geom Markov sufficiency
  - Theorem 2.2 (2A): Arbitrary-horizon active root-martingale law (N_act = 8, 12),
    3,644 full 2x2 matrix diamonds, trajectory telescoping, and nonzero update contrast
  - Theorem 2.3 (2B): All-horizon two-mode CPTP instrument, complex operator diamonds,
    and exact isomorphism-invariant non-mixture separation
  - Pillar 3: Paired 3-arm zero-shift control (Arm B - Arm A == 0), positive coupled
    clock/focusing shift (Arm C - Arm A > 0), and two-way Bayesian residual recoil
"""

import os
import sys
import math
import unittest
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from nested_regime_source_experiment import (
    myrheim_meyer_f,
    invert_myrheim_meyer,
    compute_interval_five_observables,
    sample_minkowski_fast,
    sample_csg_fast,
    compute_log_partition_sequence,
    exact_future_cone_markov_distribution,
    exact_ensemble_expected_r2_via_future_cone,
    verify_future_cone_markov_proposition,
    verify_coarse_projection_theorems,
    verify_active_root_martingale_law,
    verify_two_mode_source_instrument_and_non_mixture,
    run_pillar3_paired_source_experiment,
    _get_ideals_adj,
    _extend_poset_adj,
    _csg_ideal_prob_exact,
)


class TestIntervalObservablesAndSamplers(unittest.TestCase):
    """Tests exact algebraic identities of the five interval observables and fast samplers."""

    def test_five_observables_antichain(self):
        m = 8
        sub_C = np.zeros((m, m), dtype=np.uint8)
        obs = compute_interval_five_observables(sub_C)
        self.assertEqual(obs["r2"], 0.0)
        self.assertEqual(obs["ell_link"], 0.0)
        self.assertAlmostEqual(obs["h_over_m"], 1.0 / m, places=14)
        self.assertEqual(obs["rho2"], 0.0)
        self.assertAlmostEqual(obs["wmin_over_m"], 1.0, places=14)

    def test_five_observables_total_chain(self):
        m = 9
        sub_C = np.tril(np.ones((m, m), dtype=np.uint8), k=-1)
        obs = compute_interval_five_observables(sub_C)
        self.assertAlmostEqual(obs["r2"], 1.0, places=14)
        self.assertAlmostEqual(obs["ell_link"], 2.0 / m, places=14)
        self.assertAlmostEqual(obs["h_over_m"], 1.0, places=14)
        # In an m-chain, C_2 = binom(m, 3) and C_3 = binom(m, 4) => rho_2 = (m - 3) / 4
        self.assertAlmostEqual(obs["rho2"], (m - 3) / 4.0, places=14)
        self.assertAlmostEqual(obs["wmin_over_m"], 1.0 / m, places=14)

    def test_five_observables_crown_bipartite(self):
        # Complete bipartite 2-layer poset K_{3, 3}: 3 minimal, 3 maximal, 9 links, no 2-chains
        sub_C = np.zeros((6, 6), dtype=np.uint8)
        sub_C[3:6, 0:3] = 1
        obs = compute_interval_five_observables(sub_C)
        self.assertAlmostEqual(obs["r2"], 9.0 / 15.0, places=14)
        self.assertAlmostEqual(obs["ell_link"], 1.0, places=14)
        self.assertAlmostEqual(obs["h_over_m"], 2.0 / 6.0, places=14)
        self.assertEqual(obs["rho2"], 0.0)
        self.assertAlmostEqual(obs["wmin_over_m"], 3.0 / 6.0, places=14)

    def test_myrheim_meyer_exact_values_and_monotone_inversion(self):
        self.assertAlmostEqual(myrheim_meyer_f(1.0), 1.0, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(2.0), 0.5, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(3.0), 8.0 / 35.0, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(4.0), 0.1, places=14)
        for d in (1.5, 2.0, 2.75, 3.5, 4.0, 5.25):
            self.assertAlmostEqual(invert_myrheim_meyer(myrheim_meyer_f(d)), d, places=11)

    def test_vectorized_minkowski_and_csg_transitivity(self):
        rng = np.random.default_rng(101)
        samples = [
            sample_minkowski_fast(2, 48, rng, "diamond"),
            sample_minkowski_fast(4, 48, rng, "diamond"),
            sample_minkowski_fast(2, 48, rng, "slab", 3.0),
            sample_csg_fast(48, "log_quadratic", {"c": 0.20, "q": 0.20}, rng)[0],
            sample_csg_fast(48, "finite_cutoff", {"c": 1.0, "k_max": 2}, rng)[0],
            sample_csg_fast(48, "percolation", {"p": 0.10}, rng)[0],
            sample_csg_fast(48, "random_dag_sparse", {"c_deg": 2.0}, rng)[0],
        ]
        for C in samples:
            self.assertEqual(int(np.sum(np.triu(C))), 0)
            C2 = C.astype(np.int32) @ C.astype(np.int32)
            self.assertEqual(int(np.sum((C2 > 0) & (C == 0))), 0)


class TestPillar1FutureConeAndGeometry(unittest.TestCase):
    """Tests Proposition 1.1 (exact 1D Future-Cone Markov chain) and geometric width separation."""

    def test_future_cone_markov_chain_exact_vs_full_poset_enumeration(self):
        # Enumerate ALL CSG trajectories up to N = 5 and check exact distribution of F_5(x_{n0})
        c_val, q_val = 0.25, 0.30
        t_seq = [(c_val ** k) * (q_val ** (k * (k - 1) // 2)) for k in range(8)]
        log_z, _ = compute_log_partition_sequence(5, "log_quadratic", {"c": c_val, "q": q_val})

        trajs = [(np.zeros((1, 1), dtype=bool), 1.0)]
        for _ in range(1, 5):
            nxt = []
            for adj, w in trajs:
                for S in _get_ideals_adj(adj):
                    nxt.append((_extend_poset_adj(adj, S), w * _csg_ideal_prob_exact(adj, S, t_seq)))
            trajs = nxt

        for n0 in range(5):
            enum_dist = np.zeros(5 - n0 + 1, dtype=np.float64)
            for adj, w in trajs:
                f_sz = 1 + int(np.sum(adj[n0, :]))
                enum_dist[f_sz] += w
            markov_dist = exact_future_cone_markov_distribution(5, n0, log_z)
            np.testing.assert_allclose(enum_dist, markov_dist, atol=1e-14)

    def test_future_cone_expected_r2_monte_carlo_agreement(self):
        prop = verify_future_cone_markov_proposition(N_mc=64, num_mc=250, seed=4242)
        self.assertLess(prop["abs_r2_error"], 3.5 * prop["mc_r2_sem"])
        for dk in prop["realized_octave_delta_K_q020"]:
            self.assertTrue(0.35 <= dk <= 0.44)

    def test_minkowski_4d_vs_log_quadratic_entry_width_separation(self):
        rng = np.random.default_rng(7070)
        w_mink, w_lq = [], []
        for _ in range(6):
            Cm = sample_minkowski_fast(4, 384, rng, "diamond")
            C2m = np.rint(Cm.astype(np.float32) @ Cm.astype(np.float32)).astype(np.int32)
            coords_m = np.argwhere((Cm == 1) & (C2m >= 12) & (C2m <= 24))
            for v, u in coords_m[:25]:
                zs = np.nonzero((Cm[v, :] == 1) & (Cm[:, u] == 1))[0]
                w_mink.append(compute_interval_five_observables(Cm[np.ix_(zs, zs)])["wmin_over_m"])

            Cl, _, _ = sample_csg_fast(384, "log_quadratic", {"c": 0.20, "q": 0.20}, rng)
            C2l = np.rint(Cl.astype(np.float32) @ Cl.astype(np.float32)).astype(np.int32)
            coords_l = np.argwhere((Cl == 1) & (C2l >= 12) & (C2l <= 24))
            for v, u in coords_l[:25]:
                zs = np.nonzero((Cl[v, :] == 1) & (Cl[:, u] == 1))[0]
                w_lq.append(compute_interval_five_observables(Cl[np.ix_(zs, zs)])["wmin_over_m"])

        self.assertGreater(float(np.mean(w_mink)), 0.55)
        self.assertLess(float(np.mean(w_lq)), 0.25)


class TestPillar2CoarseProjectionAndActiveLaws(unittest.TestCase):
    """Tests Theorem 2.1 (coarse projection) and Theorems 2.2-2.3 (active residual laws)."""

    @classmethod
    def setUpClass(cls):
        cls.proj_res = verify_coarse_projection_theorems()
        cls.act_res = verify_active_root_martingale_law()
        cls.twomode_res = verify_two_mode_source_instrument_and_non_mixture()

    def test_coarse_projection_diamond_commutation_vs_stage_parity(self):
        self.assertEqual(self.proj_res["total_diamonds_n_le_4"], 3644)
        self.assertEqual(self.proj_res["intrinsic_projection_diamond_violations"], 0)
        self.assertGreater(self.proj_res["stage_parity_projection_diamond_violations"], 0)

    def test_omitted_micro_interval_non_markovianity_exact_formulas(self):
        self.assertLess(self.proj_res["omitted_chain_max_formula_err"], 1e-14)
        tbl = self.proj_res["omitted_chain_non_markov_table"]
        # Strict monotonicity with omitted micro-interval length m
        ratios_lq = [row["logq_branch_over_empty"] for row in tbl]
        for i in range(len(ratios_lq) - 1):
            self.assertGreater(ratios_lq[i + 1], ratios_lq[i])

    def test_shadow_volume_zgeom_markov_sufficiency(self):
        self.assertGreater(self.proj_res["zgeom_multi_member_classes"], 10)
        self.assertLess(self.proj_res["max_zgeom_sufficiency_discrepancy"], 1e-14)
        self.assertGreater(self.proj_res["max_coarse_only_non_markov_gap"], 0.05)

    def test_active_root_martingale_positivity_normalization_and_anchor(self):
        for h_key in ("8", "12"):
            d = self.act_res[h_key]
            self.assertGreater(d["min_branch_matrix_entry"], 0.0)
            self.assertLess(d["max_row_normalization_err"], 1e-14)
            self.assertLess(d["max_uniform_anchor_err"], 1e-14)
            self.assertLess(d["max_martingale_err"], 1e-14)

    def test_active_root_martingale_3644_diamonds_and_telescoping(self):
        for h_key in ("8", "12"):
            d = self.act_res[h_key]
            self.assertEqual(d["total_diamonds_n_le_4"], 3644)
            self.assertEqual(d["diamond_violations_n_le_4"], 0)
            self.assertEqual(d["high_n_sampled_diamond_violations"], 0)
            self.assertLess(d["max_diamond_matrix_err"], 1e-14)
            self.assertLess(d["max_trajectory_telescope_err"], 1e-14)

    def test_active_update_contrast_vs_static_seed_and_forward_controls(self):
        for h_key in ("8", "12"):
            d = self.act_res[h_key]
            self.assertNotEqual(d["step1_chain_delta_update"], 0.0)
            self.assertAlmostEqual(
                d["update_over_current_ratio"],
                d["analytic_ratio_minus_half_one_minus_t"],
                places=12,
            )
            self.assertAlmostEqual(d["static_seed_control_delta_update"], 0.0, places=15)
            self.assertAlmostEqual(d["forward_only_control_delta_update"], 0.0, places=15)

    def test_two_mode_instrument_cptp_and_operator_diamonds(self):
        self.assertEqual(self.twomode_res["total_diamonds_n_le_4"], 3644)
        self.assertLess(self.twomode_res["max_cptp_trace_err"], 1e-14)
        self.assertEqual(self.twomode_res["operator_diamond_violations"], 0)
        self.assertLess(self.twomode_res["max_operator_diamond_err"], 1e-14)
        self.assertNotAlmostEqual(
            self.twomode_res["same_prefix_n128_p_empty_id"],
            self.twomode_res["same_prefix_n128_p_empty_UX"],
        )

    def test_non_mixture_separation_exact_isomorphism_invariant_ratio(self):
        for chk in self.twomode_res["non_mixture_exact_enumeration_checks"]:
            self.assertAlmostEqual(chk["total_intervened_probability_mass"], 1.0, places=13)
            self.assertAlmostEqual(
                chk["arbitrary_3component_mixture_ratio"],
                chk["universal_static_mixture_ratio"],
                places=13,
            )
            self.assertAlmostEqual(
                chk["intervened_UX_ratio"],
                chk["analytic_intervened_ratio"],
                places=13,
            )
            self.assertGreater(chk["non_mixture_discrepancy"], 0.9)


class TestPillar3PairedSourceAndRecoil(unittest.TestCase):
    """Tests Pillar 3 paired zero-shift uncoupled control, coupled clock response, and recoil."""

    @classmethod
    def setUpClass(cls):
        cls.p3_mini = run_pillar3_paired_source_experiment(
            n0=32, horizons=(128,), num_runs=12, p_anc=0.20, seed=99001
        )

    def test_pillar3_arm_b_exact_zero_structural_shift(self):
        c128 = self.p3_mini["horizons"]["128"]["paired_contrasts"]
        for ctrl_key in ("B_p05_minus_A", "B_p10_minus_A"):
            self.assertEqual(c128[ctrl_key]["src_l_max_ticks"]["mean"], 0.0)
            self.assertEqual(c128[ctrl_key]["src_cone_volume"]["mean"], 0.0)
            self.assertEqual(c128[ctrl_key]["coarse_anchor_r2"]["mean"], 0.0)
            self.assertEqual(c128[ctrl_key]["global_r2"]["mean"], 0.0)

        self.assertGreater(c128["C_p10_minus_A"]["src_l_max_ticks"]["mean"], 1.0)
        self.assertGreater(c128["C_p10_minus_A"]["src_cone_volume"]["mean"], 10.0)
        self.assertGreater(c128["C_p10_minus_A"]["coarse_anchor_r2"]["mean"], 0.05)

    def test_pillar3_coherent_recoil_and_single_history_decoherence(self):
        arms = self.p3_mini["horizons"]["128"]["arms"]
        b05 = arms["arm_B_uncoupled_p05"]
        c05 = arms["arm_C_coherent_p05"]

        # Uncoupled control preserves pure single-history |<0|Z_N|1>| == 0.5 and zero p1 recoil variance
        self.assertAlmostEqual(b05["residual_coherence_abs_mean"], 0.5, places=12)
        self.assertAlmostEqual(b05["residual_p1_var_between"], 0.0, places=14)

        # Coupled active arm exhibits strong single-history coherence collapse & Bayesian recoil variance
        self.assertLess(c05["residual_coherence_abs_mean"], 0.05)
        self.assertGreater(c05["residual_p1_var_between"], 0.10)


if __name__ == "__main__":
    unittest.main()
