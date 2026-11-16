"""
test_cr1_discriminating_experiment.py

Comprehensive Unit & Property Test Suite for Conjecture CR-1.
Covers:
  - PosetMetrics (R_2, global posts, chain ratio rho_2, open intervals, BD actions)
  - Positive geometric controls: 2D/4D Minkowski Diamonds (CR-1 + SS-1) and
    2D Minkowski Wide-Slab Cylinder (CR-1 satisfied, SS-1 falsified)
  - Negative controls: Bimodal 10/90 mixture, 3-layer Kleitman-Rothschild,
    finite-cutoff k_max=1 recursive forest (exact tree-interval identity R_2(I) == 1.0),
    Bernoulli transitive percolation, and QR-LD037 non-diamond law
  - Exact diamond commutation audit on poset_generator.py (N <= 4)
  - Multi-horizon scaling behavior (Gevrey upward drift vs Log-Quadratic spine contrast)
"""

import os
import sys
import math
import unittest
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from cr1_discriminating_experiment import (
    PosetMetrics,
    myrheim_meyer_f,
    invert_myrheim_meyer,
    exact_d2_pair_volume_cdf,
    sample_minkowski_poisson,
    sample_csg_history,
    sample_bernoulli_percolation,
    sample_random_dag,
    sample_bimodal_extremal_mixture,
    sample_kleitman_rothschild_3layer,
    verify_exact_diamond_and_readout_properties,
    run_discriminating_experiment,
    run_multi_alpha_profile_experiment,
)


class TestPosetMetrics(unittest.TestCase):
    """Tests mathematical correctness of poset metrics, post density, chain ratios, and intervals."""

    def test_empty_poset(self):
        C = np.zeros((4, 4), dtype=int)
        metrics = PosetMetrics.compute_all_metrics(C)
        self.assertEqual(metrics["c1"], 0)
        self.assertEqual(metrics["total_pairs"], 6)
        self.assertEqual(metrics["r2"], 0.0)
        self.assertEqual(metrics["post_count"], 0)
        self.assertEqual(metrics["rho2_chain_ratio"], 0.0)
        self.assertEqual(metrics["intervals_ge4_count"], 0)

    def test_total_chain(self):
        C = np.zeros((4, 4), dtype=int)
        for v in range(4):
            C[v, :v] = 1
        metrics = PosetMetrics.compute_all_metrics(C, min_interval_size=1)
        self.assertEqual(metrics["c1"], 6)
        self.assertEqual(metrics["r2"], 1.0)
        self.assertEqual(metrics["post_count"], 4)
        self.assertEqual(metrics["post_density"], 1.0)
        self.assertEqual(metrics["c2_chains"], 4)
        self.assertEqual(metrics["c3_chains"], 1)
        self.assertAlmostEqual(metrics["rho2_chain_ratio"], 0.25)

    def test_diamond_poset(self):
        C = np.zeros((4, 4), dtype=int)
        C[1, 0] = 1
        C[2, 0] = 1
        C[3, 1] = 1
        C[3, 2] = 1
        C[3, 0] = 1
        metrics = PosetMetrics.compute_all_metrics(C, min_interval_size=2)
        self.assertEqual(metrics["c1"], 5)
        self.assertAlmostEqual(metrics["r2"], 5.0 / 6.0)
        # Vertices 0 and 3 are global posts; 1 and 2 are spacelike
        self.assertEqual(metrics["post_count"], 2)
        self.assertEqual(metrics["intervals_ge4_count"], 1)
        self.assertEqual(metrics["sub_interval_r2_values"], [0.0])

    def test_benincasa_dowker_scalar_actions(self):
        C = np.zeros((4, 4), dtype=int)
        for v in range(4):
            C[v, :v] = 1
        metrics = PosetMetrics.compute_all_metrics(C)
        self.assertEqual(metrics["bd2_action"], 4.0)
        self.assertEqual(metrics["bd4_action"], 3.0)

    def test_myrheim_meyer_exact_normalization_and_inversion(self):
        # Verifies unordered-pair comparability f(d) = Gamma(d+1)Gamma(d/2) / (2 Gamma(3d/2))
        self.assertAlmostEqual(myrheim_meyer_f(1.0), 1.0, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(2.0), 0.5, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(3.0), 8.0 / 35.0, places=14)
        self.assertAlmostEqual(myrheim_meyer_f(4.0), 0.1, places=14)
        self.assertAlmostEqual(invert_myrheim_meyer(1.0), 1.0, places=12)
        self.assertAlmostEqual(invert_myrheim_meyer(0.5), 2.0, places=12)
        self.assertAlmostEqual(invert_myrheim_meyer(8.0 / 35.0), 3.0, places=12)
        self.assertAlmostEqual(invert_myrheim_meyer(0.1), 4.0, places=12)


class TestGeometricControls(unittest.TestCase):
    """Tests 2D/4D Minkowski Diamonds and 2D Minkowski Slab (CR-1 vs SS-1)."""

    def test_2d_and_4d_minkowski_transitivity(self):
        for dim in (2, 4):
            C, traj = sample_minkowski_poisson(dim=dim, N=24, seed=42)
            self.assertTrue(np.all(np.triu(C) == 0))
            C2 = C @ C
            self.assertEqual(np.sum((C2 > 0) & (C == 0)), 0)
            self.assertEqual(len(traj), 24)

    def test_2d_and_4d_diamond_comparability(self):
        r2_2d = [np.sum(sample_minkowski_poisson(2, 64, seed=2000 + s)[0]) / (64 * 63 / 2.0) for s in range(20)]
        r2_4d = [np.sum(sample_minkowski_poisson(4, 64, seed=3000 + s)[0]) / (64 * 63 / 2.0) for s in range(20)]
        self.assertTrue(0.45 <= np.mean(r2_2d) <= 0.55)
        self.assertTrue(0.07 <= np.mean(r2_4d) <= 0.13)

    def test_2d_slab_separates_cr1d_from_ss1(self):
        # In [0, 1] x [0, 3], global E[R_2] = 11/54 ~= 0.2037, while internal intervals have E[R_2(I)] = 0.5000
        glob_r2s, int_r2s = [], []
        for s in range(20):
            C, _ = sample_minkowski_poisson(2, 96, seed=4000 + s, geometry="slab", slab_width=3.0)
            m = PosetMetrics.compute_all_metrics(C, min_interval_size=4)
            glob_r2s.append(m["r2"])
            if m["intervals_ge4_count"] > 0:
                int_r2s.append(m["sub_interval_r2_mean"])
        self.assertTrue(0.16 <= np.mean(glob_r2s) <= 0.25)
        self.assertTrue(0.42 <= np.mean(int_r2s) <= 0.58)
        self.assertGreater(np.mean(int_r2s) - np.mean(glob_r2s), 0.20)

    def test_d2_near_lightlike_pair_volume_cdf(self):
        # Verifies exact D_2 unordered pair-volume CDF F_{D_2}(v) = (2v + v^2)ln(1/v) - 2v + (5/2)v^2
        # against null-coordinate Monte Carlo on (xi, eta) in (0, 1)^2 and near-lightlike log enhancement.
        self.assertEqual(exact_d2_pair_volume_cdf(0.0), 0.0)
        self.assertEqual(exact_d2_pair_volume_cdf(-0.5), 0.0)
        self.assertEqual(exact_d2_pair_volume_cdf(1.0), 0.5)
        self.assertAlmostEqual(exact_d2_pair_volume_cdf(1.0), myrheim_meyer_f(2.0), places=14)

        rng = np.random.default_rng(20261117)
        m_pairs = 200_000
        xi1 = rng.uniform(0.0, 1.0, m_pairs)
        eta1 = rng.uniform(0.0, 1.0, m_pairs)
        xi2 = rng.uniform(0.0, 1.0, m_pairs)
        eta2 = rng.uniform(0.0, 1.0, m_pairs)
        dxi = xi2 - xi1
        deta = eta2 - eta1
        comp = (dxi * deta) > 0.0
        vol_norm = np.abs(dxi * deta)

        for v in (0.01, 0.05, 0.20):
            mc_cdf = float(np.mean(comp & (vol_norm <= v)))
            exact_val = exact_d2_pair_volume_cdf(v)
            self.assertLess(abs(mc_cdf - exact_val), 4e-3)

        # Asymptotic near-lightlike shell enhancement: (F(1.5*v) - F(0.5*v)) / (v * ln(1/v)) -> 2.0 as v -> 0
        ratios = [
            (exact_d2_pair_volume_cdf(1.5 * v) - exact_d2_pair_volume_cdf(0.5 * v))
            / (v * math.log(1.0 / v))
            for v in (1e-6, 1e-18, 1e-120)
        ]
        self.assertLess(abs(2.0 - ratios[2]), abs(2.0 - ratios[1]))
        self.assertLess(abs(2.0 - ratios[1]), abs(2.0 - ratios[0]))
        self.assertAlmostEqual(ratios[2], 2.0, delta=0.02)

    def test_d4_near_lightlike_shell_exponent(self):
        # Exact rejection-free slice sampling on D_4 (slice radius R = 0.5 * u^{1/4}):
        # verifies 100x volume reduction v_1 = 1e-3 -> v_2 = 1e-5 gives shell probability ratio
        # p(v_1)/p(v_2) near 100^{2/d} = 100^{1/2} = 10 (in [5.0, 22.0]) rather than naive smooth 100.
        rng = np.random.default_rng(20261118)
        m_pairs = 400_000

        def sample_d4_points(n):
            r_slice = 0.5 * (rng.uniform(0.0, 1.0, n) ** 0.25)
            t = np.where(rng.random(n) < 0.5, 1.0 - r_slice, r_slice)
            rad = r_slice * (rng.uniform(0.0, 1.0, n) ** (1.0 / 3.0))
            dirs = rng.normal(size=(n, 3))
            dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
            return t, dirs * rad[:, None]

        t1, x1 = sample_d4_points(m_pairs)
        t2, x2 = sample_d4_points(m_pairs)
        w = (t2 - t1) ** 2 - np.sum((x2 - x1) ** 2, axis=1)
        comp = w > 0.0
        self.assertAlmostEqual(float(np.mean(comp)), myrheim_meyer_f(4.0), delta=5e-3)

        v_norm = np.where(comp, w * w, -1.0)
        v1, v2, v3 = 1e-3, 1e-5, 1e-7
        p_v1 = float(np.mean(comp & (v_norm >= 0.5 * v1) & (v_norm <= 1.5 * v1)))
        p_v2 = float(np.mean(comp & (v_norm >= 0.5 * v2) & (v_norm <= 1.5 * v2)))
        p_v3 = float(np.mean(comp & (v_norm >= 0.5 * v3) & (v_norm <= 1.5 * v3)))

        ratio_12 = p_v1 / p_v2
        ratio_23 = p_v2 / p_v3
        self.assertGreaterEqual(ratio_12, 5.0)
        self.assertLessEqual(ratio_12, 22.0)
        self.assertGreaterEqual(ratio_23, 7.5)
        self.assertLessEqual(ratio_23, 13.0)


class TestNegativeAndExactControls(unittest.TestCase):
    """Tests bimodal mixture, Kleitman-Rothschild, k_max=1 tree intervals, percolation, and exact diamonds."""

    def test_bimodal_mixture_fails_single_history_concentration(self):
        r2s = [PosetMetrics.compute_all_metrics(sample_bimodal_extremal_mixture(32, 0.10, seed=100 + s)[0])["r2"]
               for s in range(100)]
        # Every single history is at 0.0 or 1.0, never near 0.10
        for val in r2s:
            self.assertIn(val, (0.0, 1.0))
        self.assertGreater(np.var(r2s, ddof=1), 0.05)

    def test_kleitman_rothschild_3layer_zero_3chains(self):
        r2s = []
        for s in range(20):
            C, _ = sample_kleitman_rothschild_3layer(48, edge_prob=0.50, seed=500 + s)
            C2 = C @ C
            self.assertEqual(np.sum((C2 > 0) & (C == 0)), 0)
            m = PosetMetrics.compute_all_metrics(C)
            self.assertEqual(m["c3_chains"], 0)
            self.assertEqual(m["rho2_chain_ratio"], 0.0)
            r2s.append(m["r2"])
        self.assertTrue(0.28 <= np.mean(r2s) <= 0.45)

    def test_cutoff_kmax1_intervals_are_exact_total_chains(self):
        # In k_max = 1 CSG, every vertex chooses <= 1 parent, so J^-(v) is a total chain
        # and EVERY open interval I(u, v) with m >= 2 has R_2(I(u, v)) == 1.0 identically!
        checked_intervals = 0
        for s in range(25):
            C, _, _ = sample_csg_history(64, "finite_cutoff", {"c": 2.0, "k_max": 1}, seed=700 + s)
            m = PosetMetrics.compute_all_metrics(C, min_interval_size=2)
            for val in m["sub_interval_r2_values"]:
                self.assertAlmostEqual(val, 1.0, places=12)
                checked_intervals += 1
        self.assertGreater(checked_intervals, 10)

    def test_exact_diamond_audit_with_poset_generator(self):
        audit = verify_exact_diamond_and_readout_properties()
        self.assertGreater(audit["total_diamonds_n_le_4"], 500)
        self.assertEqual(audit["gevrey_diamond_violations"], 0)
        self.assertEqual(audit["log_quadratic_diamond_violations"], 0)
        self.assertEqual(audit["intrinsic_compensation_proper_violations"], 0)
        self.assertGreater(audit["stage_n_exponent_damping_violations"], 0)
        self.assertLess(audit["local_cone_routed_max_row_err"], 1e-14)
        self.assertGreater(audit["local_cone_routed_diamond_violations"], 0)
        self.assertFalse(audit["qr_ld037_diamond_commutes"])

    def test_percolation_monotonicity_with_p(self):
        r2_low = [sample_bernoulli_percolation(32, 0.05, seed=100 + s)[1][-1] for s in range(15)]
        r2_high = [sample_bernoulli_percolation(32, 0.20, seed=200 + s)[1][-1] for s in range(15)]
        self.assertGreater(np.mean(r2_high), np.mean(r2_low))


class TestCandidateCSGAndSpineDiscrimination(unittest.TestCase):
    """Tests Gevrey & Log-Quadratic CSG and the sub-interval spine discriminator."""

    def test_gevrey_and_log_quadratic_transitivity(self):
        for ctype, pms in [("gevrey", {"c": 0.2, "beta": 2.0}), ("log_quadratic", {"c": 0.2, "q": 0.10})]:
            C, _, pasts = sample_csg_history(20, ctype, pms, seed=42)
            for n in range(20):
                for u in pasts[n]:
                    self.assertTrue(pasts[u].issubset(pasts[n]))
            C2 = C @ C
            self.assertEqual(np.sum((C2 > 0) & (C == 0)), 0)

    def test_geometric_self_similarity_vs_csg_spine(self):
        mink_sub_r2s = []
        for s in range(30):
            C, _ = sample_minkowski_poisson(dim=4, N=32, seed=5000 + s)
            m = PosetMetrics.compute_all_metrics(C, min_interval_size=4)
            if m["intervals_ge4_count"] > 0:
                mink_sub_r2s.append(m["sub_interval_r2_mean"])

        csg_sub_r2s = []
        for s in range(30):
            C, _, _ = sample_csg_history(32, "log_quadratic", {"c": 0.2, "q": 0.10}, seed=6000 + s)
            m = PosetMetrics.compute_all_metrics(C, min_interval_size=4)
            if m["intervals_ge4_count"] > 0:
                csg_sub_r2s.append(m["sub_interval_r2_mean"])

        mean_mink_sub = float(np.mean(mink_sub_r2s))
        mean_csg_sub = float(np.mean(csg_sub_r2s))
        self.assertLess(mean_mink_sub, 0.25)
        self.assertGreater(mean_csg_sub, 0.70)
        self.assertGreater(mean_csg_sub - mean_mink_sub, 0.50)

    def test_mini_experiment_pipeline(self):
        test_configs = [
            {
                "model_id": "test_gevrey",
                "family": "candidate_gevrey",
                "label": "Test Gevrey",
                "type": "csg",
                "coupling_type": "gevrey",
                "params": {"c": 0.2, "beta": 2.0},
            },
            {
                "model_id": "test_minkowski",
                "family": "geometric_control",
                "label": "Test Minkowski",
                "type": "geometric",
                "dim": 4,
            },
        ]
        results = run_discriminating_experiment(configs=test_configs, horizons=[16], num_runs=5, base_seed=999)
        self.assertIn("16", results["horizons_data"])
        self.assertIn("r2_mean", results["horizons_data"]["16"]["test_gevrey"])

    def test_multi_alpha_profile_pipeline(self):
        prof = run_multi_alpha_profile_experiment(
            horizons=(128,),
            alphas=(0.35, 0.65),
            num_runs=3,
            max_intervals_per_alpha=20,
            seed=777,
        )
        self.assertIn("128", prof["horizons"])
        h128 = prof["horizons"]["128"]
        self.assertIn("minkowski_4d", h128)
        self.assertIn("log_quad_c02_q020", h128)
        lq = h128["log_quad_c02_q020"]["alphas"]
        self.assertGreater(lq["0.35"]["r_int_mean"], lq["0.65"]["r_int_mean"])


if __name__ == "__main__":
    unittest.main()
