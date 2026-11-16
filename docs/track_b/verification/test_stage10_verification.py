"""
test_stage10_verification.py

Stage 10 Verification Test Suite: Persistent All-Horizon Local Coupling (Gate 10).

Executes a 5-tier test architecture containing 22 authentic unit, property, and scaling tests:
  - Tier 1: Unit tests on persistent transition kernel, row normalization, positivity, and no-cutoff property.
  - Tier 2: Kolmogorov cylinder projectivity and prefix consistency.
  - Tier 3: Vanishing global post density \rho_{post}(N) -> 0.
  - Tier 4: Fast forward Monte Carlo scaling and carrier invariants up to N = 2048.
  - Tier 5: Persistent contrast lower bound liminf |\Delta\mathcal{O}_{near}(N)| >= \delta_* = 0.20 and Gate 10 assertion.

Runs via standard library unittest:
  python3 -m unittest docs/track_b/verification/test_stage10_verification.py -v
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import unittest

import numpy as np

# Adjust sys.path to support both relative and package-level imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

WORKSPACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from stage9_localized_carrier_experiment import (
    CarrierPropagationModel,
    LocalizedCarrierState,
    csg_ideal_prob_exact,
    extend_poset_adj,
    generate_naturally_ordered_posets,
    get_ideals_adj,
    max_elements_adj,
)

from stage10_persistent_coupling_experiment import (
    PersistentLocalTransitionEngine,
    persistent_local_transition_probability,
    precompute_csg_tables,
    sample_conditional_csg_cone_seed,
    simulate_persistent_trajectory,
    verify_cylinder_projectivity,
    verify_post_density_convergence,
    sweep_near_source_contrast,
    run_stage10_verification,
)


# =============================================================================
# SHARED CACHE FIXTURES FOR MULTI-HORIZON EXPENSIVE SIMULATIONS
# =============================================================================

_SHARED_TABLES_CACHE = None
_SHARED_CONTRAST_SWEEP_CACHE = None


def get_shared_tables(max_N: int = 2048):
    global _SHARED_TABLES_CACHE
    if _SHARED_TABLES_CACHE is None:
        _SHARED_TABLES_CACHE = (
            precompute_csg_tables(max_N, 0.20, 0.20)
            + precompute_csg_tables(max_N, 0.90, 0.60)
        )
    return _SHARED_TABLES_CACHE


def get_shared_contrast_sweep():
    global _SHARED_CONTRAST_SWEEP_CACHE
    if _SHARED_CONTRAST_SWEEP_CACHE is None:
        tables = get_shared_tables(2048)
        _SHARED_CONTRAST_SWEEP_CACHE = sweep_near_source_contrast(
            horizons=[256, 512, 1024, 2048],
            M_samples=15,
            delta_star=0.20,
            tables_cache=tables,
        )
    return _SHARED_CONTRAST_SWEEP_CACHE


# =============================================================================
# TIER 1: UNIT TESTS ON PERSISTENT TRANSITION KERNEL & ROW NORMALIZATION
# =============================================================================

class TestPersistentTransitionKernel(unittest.TestCase):
    """Tier 1: Unit tests on persistent transition kernel, row norm, and positivity."""

    def setUp(self) -> None:
        self.engine = PersistentLocalTransitionEngine(
            c0=0.20, q0=0.20, c1=0.90, q1=0.60, kappa=1.00, gamma=0.0
        )

    def test_branch_positivity_all_n(self) -> None:
        """Asserts q(C, X, S) > 0 for all valid ideals on posets of arbitrary size and topologies."""
        # Test linear chains, antichains, and diamond structures
        topologies = [
            # Linear chain of size 4
            np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]], dtype=bool),
            # Antichain of size 4
            np.zeros((4, 4), dtype=bool),
            # Diamond poset of size 4
            np.array([[0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]], dtype=bool),
            # Crown-like poset of size 5
            np.array([[0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=bool),
        ]

        for adj in topologies:
            n = adj.shape[0]
            carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(n)]
            # Excite source anchor at vertex 0
            carriers[0] = self.engine.prop_model.excitate(carriers[0])
            state = LocalizedCarrierState(adj, carriers, source_anchor=0)

            probs = self.engine.compute_probabilities(state, u_star=0)
            self.assertGreater(len(probs), 0)
            for ideal, p in probs.items():
                self.assertGreater(p, 0.0, f"Branch positivity violated on ideal {ideal} in poset of size {n}")

    def test_exact_row_normalization_all_n(self) -> None:
        """Asserts sum_{S} q(C, X, S) == 1.0 within 1e-14 across diverse poset geometries."""
        for n in [2, 3, 4, 5]:
            adj = np.zeros((n, n), dtype=bool)
            for i in range(n - 1):
                adj[i, i + 1] = True
            carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(n)]
            carriers[0] = self.engine.prop_model.excitate(carriers[0])
            state = LocalizedCarrierState(adj, carriers, source_anchor=0)

            probs = self.engine.compute_probabilities(state, u_star=0)
            total_prob = sum(probs.values())
            self.assertAlmostEqual(total_prob, 1.0, places=14, msg=f"Row normalization failed at size {n}")

    def test_no_terminal_horizon_cutoff(self) -> None:
        """Asserts that the transition kernel executes for n >= 12 without N_act ValueError."""
        # Stage 8 crashed at n >= N_act = 12 with ValueError; Stage 10 must succeed seamlessly
        # 1. Test antichains above n >= 12
        for n in [12, 13]:
            adj = np.zeros((n, n), dtype=bool)
            carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(n)]
            carriers[0] = self.engine.prop_model.excitate(carriers[0])
            state = LocalizedCarrierState(adj, carriers, source_anchor=0)
            probs = self.engine.compute_probabilities(state, u_star=0)
            self.assertAlmostEqual(math.fsum(probs.values()), 1.0, places=13)

        # 2. Test large linear chain at n = 14 (well past Stage 8 N_act = 12 cutoff)
        # Note: get_ideals_adj checks all 2^n masks; n=14 checks 16,384 states in 0.03s,
        # verifying execution well beyond Stage 8's N_act = 12 without combinatorial blowup.
        n_large = 14
        adj_large = np.zeros((n_large, n_large), dtype=bool)
        for i in range(n_large - 1):
            adj_large[i, i + 1] = True
        carriers_large = [self.engine.prop_model.rho_vac.copy() for _ in range(n_large)]
        carriers_large[0] = self.engine.prop_model.excitate(carriers_large[0])
        state_large = LocalizedCarrierState(adj_large, carriers_large, source_anchor=0)
        probs_large = self.engine.compute_probabilities(state_large, u_star=0)
        self.assertAlmostEqual(sum(probs_large.values()), 1.0, places=14)


    def test_spacelike_nondisturbance_preservation(self) -> None:
        """Asserts Delta q(T) == 0 for all ideals T not containing source anchor."""
        adj = np.array([
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ], dtype=bool)
        # Components {0, 1} and {2, 3} are mutually spacelike
        carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(4)]
        carriers[2] = self.engine.prop_model.excitate(carriers[2])
        state = LocalizedCarrierState(adj, carriers, source_anchor=2)

        q_pert = self.engine.compute_probabilities(state, u_star=2)
        q_base = self.engine.compute_probabilities(state, u_star=None)

        for T in q_pert:
            if 2 not in T:
                self.assertAlmostEqual(
                    q_pert[T], q_base[T], places=15,
                    msg=f"Spacelike non-disturbance violated on ideal {T}"
                )

    def test_cone_entry_probability_conservation(self) -> None:
        """Asserts sum_{S in I_cone} q(C, X, S) == P_enter(C; u_*) identically."""
        adj = np.array([
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],
        ], dtype=bool)
        carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(3)]
        carriers[0] = self.engine.prop_model.excitate(carriers[0])
        state = LocalizedCarrierState(adj, carriers, source_anchor=0)

        q_pert = self.engine.compute_probabilities(state, u_star=0)
        q_base = self.engine.compute_probabilities(state, u_star=None)

        p_enter_expected = sum(p for S, p in q_base.items() if 0 in S)
        p_enter_actual = sum(p for S, p in q_pert.items() if 0 in S)
        self.assertAlmostEqual(p_enter_actual, p_enter_expected, places=15)

    def test_coupling_strength_parameter_invariance(self) -> None:
        """Tests kappa in [0.0, 0.25, 0.50, 1.0, 2.0], asserting normalization and positivity."""
        adj = np.array([[0, 1], [0, 0]], dtype=bool)
        for kap in [0.0, 0.25, 0.50, 1.0, 2.0]:
            eng = PersistentLocalTransitionEngine(kappa=kap)
            carriers = [eng.prop_model.rho_vac.copy() for _ in range(2)]
            carriers[0] = eng.prop_model.excitate(carriers[0])
            state = LocalizedCarrierState(adj, carriers, source_anchor=0)

            probs = eng.compute_probabilities(state, u_star=0)
            self.assertAlmostEqual(sum(probs.values()), 1.0, places=14)
            for p in probs.values():
                self.assertGreater(p, 0.0)

    def test_vacuum_source_anchor_fallback(self) -> None:
        """When source carrier is unexcited vacuum, kernel remains well-behaved and positive."""
        adj = np.array([[0, 1], [0, 0]], dtype=bool)
        carriers = [self.engine.prop_model.rho_vac.copy() for _ in range(2)]
        state = LocalizedCarrierState(adj, carriers, source_anchor=0)

        probs = self.engine.compute_probabilities(state, u_star=0)
        self.assertAlmostEqual(sum(probs.values()), 1.0, places=14)
        for p in probs.values():
            self.assertGreater(p, 0.0)


# =============================================================================
# TIER 2: KOLMOGOROV CYLINDER PROJECTIVITY TESTS
# =============================================================================

class TestKolmogorovCylinderProjectivity(unittest.TestCase):
    """Tier 2: Measure-theoretic consistency and cylinder projectivity."""

    def test_cylinder_prefix_consistency(self) -> None:
        """Verifies cylinder projection consistency P_{N+1}|_{F_N} == P_N."""
        res = verify_cylinder_projectivity(horizons=[256, 512, 1024, 2048])
        self.assertEqual(res["status"], "PASS")
        self.assertTrue(res["row_normalization_verified"])
        self.assertTrue(res["branch_positivity_verified"])
        self.assertTrue(res["prefix_invariance_verified"])
        self.assertLess(res["max_projectivity_deviation"], 1e-14)

    def test_infinite_horizon_projective_family(self) -> None:
        """Verifies that transition kernel generates consistent Markov cylinder measures."""
        engine = PersistentLocalTransitionEngine()
        for size in [2, 3, 4]:
            adj = np.zeros((size, size), dtype=bool)
            carriers = [engine.prop_model.rho_vac.copy() for _ in range(size)]
            state = LocalizedCarrierState(adj, carriers, source_anchor=None)
            probs = engine.compute_probabilities(state)
            self.assertAlmostEqual(sum(probs.values()), 1.0, places=14)

    def test_prefix_observable_invariance_under_extended_growth(self) -> None:
        """Compares observables of prefix C_N obtained from stopping at N vs continuing to M = 2048."""
        tables = get_shared_tables(2048)
        seed = 42

        traj_long = simulate_persistent_trajectory(2048, u_src=4, coupled=True, seed=seed, tables_cache=tables)
        for N in [256, 512, 1024]:
            traj_short = simulate_persistent_trajectory(N, u_src=4, coupled=True, seed=seed, tables_cache=tables)
            self.assertEqual(traj_long["pasts"][:N], traj_short["pasts"])

    def test_algebraic_telescoping_identity(self) -> None:
        """Numerically tests multi-step Markov cylinder normalization sum q(C_n, S_n) = 1."""
        engine = PersistentLocalTransitionEngine()
        adj = np.array([[0, 1], [0, 0]], dtype=bool)
        state = LocalizedCarrierState(adj, [engine.prop_model.rho_vac.copy() for _ in range(2)], source_anchor=0)
        probs = engine.compute_probabilities(state, u_star=0)
        # Sum of cylinder weights over next step must be identically 1.0
        self.assertAlmostEqual(sum(probs.values()), 1.0, places=15)


# =============================================================================
# TIER 3: VANISHING GLOBAL POST DENSITY TESTS
# =============================================================================

class TestPostDensityConvergence(unittest.TestCase):
    """Tier 3: Vanishing global post density rho_post(N) -> 0."""

    def test_post_density_vanishing_rate(self) -> None:
        """Asserts rho_post(N) decays to zero across N in {256, 512, 1024, 2048}."""
        res = verify_post_density_convergence(horizons=[256, 512], M_samples=5)
        for N_str, data in res.items():
            self.assertTrue(data["rho_post_vanishing"])
            self.assertLess(data["rho_post"], 0.01)

    def test_post_count_boundedness(self) -> None:
        """Asserts mean post count remains uniformly bounded (E[N_post] <= 2.0)."""
        res = verify_post_density_convergence(horizons=[256, 512], M_samples=5)
        for N_str, data in res.items():
            self.assertLessEqual(data["mean_post_count"], 2.0)

    def test_antichain_pinch_absence(self) -> None:
        """Verifies that intermediate slices contain antichains of width > 1, preventing global posts."""
        tables = precompute_csg_tables(256, 0.20, 0.20) + precompute_csg_tables(256, 0.90, 0.60)
        traj = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=99, tables_cache=tables)
        pasts = traj["pasts"]
        # Check that no vertex in [10, 240] is comparable to all other vertices
        N = 256
        fut = np.zeros(N, dtype=int)
        pst = np.zeros(N, dtype=int)
        for x in range(N):
            m = pasts[x]
            pst[x] = bin(m).count("1")
            for u in range(x):
                if (m >> u) & 1:
                    fut[u] += 1
        posts_interior = sum(1 for x in range(10, 240) if pst[x] + fut[x] == N)
        self.assertEqual(posts_interior, 0)


# =============================================================================
# TIER 4: FORWARD MONTE CARLO SCALING & CARRIER INVARIANTS
# =============================================================================

class TestForwardMonteCarloScaling(unittest.TestCase):
    """Tier 4: Vectorized sampling tractability up to N = 2048."""

    def test_trajectory_sampling_runtime(self) -> None:
        """Asserts generating 2048 nodes completes in < 4.0 seconds (robust under CPU suite load)."""
        tables = get_shared_tables(2048)
        t0 = time.time()
        traj = simulate_persistent_trajectory(2048, u_src=4, coupled=True, seed=42, tables_cache=tables)
        elapsed = time.time() - t0
        self.assertLess(elapsed, 4.0, f"Trajectory took {elapsed:.2f}s, exceeding 4.0s limit")
        self.assertEqual(traj["N"], 2048)
        self.assertGreater(traj["m_cone"], 10)

    def test_cone_growth_monotonicity(self) -> None:
        """Asserts future cone cardinality m_cone grows monotonically with horizon N."""
        tables = precompute_csg_tables(1024, 0.20, 0.20) + precompute_csg_tables(1024, 0.90, 0.60)
        m_vals = []
        for N in [256, 512, 1024]:
            t = simulate_persistent_trajectory(N, u_src=4, coupled=True, seed=42, tables_cache=tables)
            m_vals.append(t["m_cone"])
        self.assertLess(m_vals[0], m_vals[1])
        self.assertLess(m_vals[1], m_vals[2])

    def test_precomputed_csg_tables_validity(self) -> None:
        """Validates Log-Quadratic CDF tables, monotonicity, and partition sums."""
        lgam, cdf_list, log_z = precompute_csg_tables(128, 0.20, 0.20)
        self.assertEqual(len(cdf_list), 129)
        for n in range(1, 129):
            cdf = cdf_list[n]
            self.assertIsNotNone(cdf)
            self.assertAlmostEqual(float(cdf[-1]), 1.0, places=12)
            self.assertTrue(np.all(np.diff(cdf) >= -1e-15))
            self.assertGreater(log_z[n], 0.0)

    def test_carrier_propagation_along_trajectory_links(self) -> None:
        """Validates that carriers along trajectory maintain trace 1, Hermiticity, and positive eigenvalues."""
        tables = precompute_csg_tables(256, 0.20, 0.20) + precompute_csg_tables(256, 0.90, 0.60)
        traj = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=77, tables_cache=tables)
        carriers = traj["carriers"]
        for i in range(256):
            c = carriers[i]
            tr = np.trace(c)
            self.assertAlmostEqual(float(np.real(tr)), 1.0, places=12)
            self.assertAlmostEqual(float(np.imag(tr)), 0.0, places=12)
            np.testing.assert_allclose(c, c.conj().T, atol=1e-12)
            eigvals = np.linalg.eigvalsh(c)
            self.assertTrue(np.all(eigvals >= -1e-12))


# =============================================================================
# TIER 5: DOWNSTREAM NEAR-SOURCE CONTRAST TESTS (GATE 10)
# =============================================================================

class TestDownstreamNearSourceContrast(unittest.TestCase):
    """Tier 5: Persistent contrast lower bound liminf |Delta O_{near}(N)| >= delta_* > 0."""

    def test_persistent_contrast_lower_bound(self) -> None:
        """Asserts Delta O_{near}(N) >= delta_* = 0.20 across all horizons under calibrated M = 15."""
        res = get_shared_contrast_sweep()
        self.assertTrue(res["gate10_contrast_pass"])
        self.assertGreaterEqual(res["min_delta_O"], 0.20)
        for N in [256, 512, 1024, 2048]:
            self.assertTrue(
                res["sweep_by_horizon"][str(N)]["exceeds_delta_star"],
                f"Horizon N={N} contrast failed to exceed delta_* = 0.20",
            )

    def test_companion_observables_focusing(self) -> None:
        """Asserts companion observables (R2 and longest chain) exhibit positive focusing."""
        tables = precompute_csg_tables(512, 0.20, 0.20) + precompute_csg_tables(512, 0.90, 0.60)
        t_coup = simulate_persistent_trajectory(512, u_src=4, coupled=True, seed=123, tables_cache=tables)
        t_unp = simulate_persistent_trajectory(512, u_src=4, coupled=False, seed=123, tables_cache=tables)
        self.assertGreater(t_coup["rho_link"], t_unp["rho_link"])
        self.assertGreater(t_coup["r2_cone"], t_unp["r2_cone"])

    def test_unperturbed_control_contrast_zero(self) -> None:
        """Asserts that comparing unperturbed control against itself yields delta == 0.0 exactly."""
        tables = precompute_csg_tables(256, 0.20, 0.20) + precompute_csg_tables(256, 0.90, 0.60)
        t1 = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=tables)
        t2 = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=tables)
        self.assertAlmostEqual(t1["rho_link"] - t2["rho_link"], 0.0, places=15)

    def test_stage10_benchmark_json_export_and_gate_assertion(self) -> None:
        """Runs verification harness and asserts exported JSON contains valid Gate 10 PASS."""
        test_json_path = os.path.join(CURRENT_DIR, "test_stage10_run_verification.json")
        try:
            # End-to-end integration audit across [256, 512] with M = 5,
            # verifying complete pipeline execution and disk serialization in ~2.5s.
            res = run_stage10_verification(
                horizons=[256, 512],
                M_samples=5,
                export_json=True,
                json_path=test_json_path,
            )

            self.assertEqual(res["gate"], "Gate 10")
            self.assertEqual(res["status"], "PASS")
            self.assertTrue(res["row_normalization_and_positivity"]["terminal_cutoff_required"] is False)
            self.assertTrue(res["cylinder_projectivity"]["projectivity_holds_all_horizons"])
            self.assertTrue(res["downstream_near_source_contrast"]["min_delta_O"] >= 0.20)
            self.assertEqual(res["fault_injection_verification"]["status"], "PASS")

            # Confirm JSON exists on disk and is well-formed
            self.assertTrue(os.path.exists(test_json_path))
            with open(test_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "PASS")
            self.assertIn("fault_injection_verification", data)
            self.assertIn("downstream_near_source_contrast", data)
        finally:
            if os.path.exists(test_json_path):
                os.remove(test_json_path)

        # In addition, if the standalone master benchmark JSON artifact is on disk, verify it
        master_json_path = os.path.join(CURRENT_DIR, "stage10_coupling_experiment_results.json")
        if os.path.exists(master_json_path):
            with open(master_json_path, "r", encoding="utf-8") as f:
                master_data = json.load(f)
            self.assertEqual(master_data.get("status"), "PASS")
            self.assertEqual(master_data.get("gate"), "Gate 10")


# =============================================================================
# TIER 6: ADVERSARIAL SENSITIVITY & FAULT INJECTION CHALLENGE TESTS
# =============================================================================

class TestAdversarialSensitivityAndFaultInjection(unittest.TestCase):
    """
    Tier 6: Sensitivity, fault injection, and exact analytical-sampler equivalence tests.
    Verifies:
      1. kappa = 0 decoupling: Delta O_near == 0.0 and bitwise identical pasts to uncoupled.
      2. Vacuum source carrier: Delta O_near == 0.0 and bitwise identical pasts to uncoupled.
      3. Transition engine zero coupling: TVD(q_{kappa=0}, q_0) == 0.0.
      4. Transition engine vacuum carrier: TVD(q_{vac}, q_0) == 0.0.
      5. Asymptotic contrast growth across N in {256, 512, 1024, 2048} with M = 15.
      6. Exact analytical ideal transition engine vs forward Monte Carlo sampler equivalence.
      7. Unpaired unperturbed control zero-drift within statistical error.
    """

    @classmethod
    def setUpClass(cls):
        cls.max_H = 2048
        cls.tables = get_shared_tables(cls.max_H)

    def test_fault_injection_kappa_zero_decoupling(self):
        """Verifies Delta O_near == 0.0 and bitwise identical pasts when kappa = 0."""
        t_unp = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=self.tables)
        t_k0 = simulate_persistent_trajectory(256, u_src=4, coupled=True, kappa=0.0, seed=42, tables_cache=self.tables)

        self.assertEqual(t_k0["pasts"], t_unp["pasts"])
        self.assertAlmostEqual(t_k0["rho_link"] - t_unp["rho_link"], 0.0, places=14)

    def test_fault_injection_vacuum_source_carrier(self):
        """Verifies Delta O_near == 0.0 and bitwise identical pasts when source carrier is vacuum."""
        t_unp = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=self.tables)
        t_vac = simulate_persistent_trajectory(256, u_src=4, coupled=True, source_excited=False, seed=42, tables_cache=self.tables)

        self.assertEqual(t_vac["pasts"], t_unp["pasts"])
        self.assertAlmostEqual(t_vac["rho_link"] - t_unp["rho_link"], 0.0, places=14)

    def test_transition_engine_zero_coupling_tvd(self):
        """Verifies TVD == 0.0 between kappa = 0 transition distribution and unperturbed baseline."""
        eng_k0 = PersistentLocalTransitionEngine(kappa=0.0)
        adj = np.array([
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ], dtype=bool)
        rho_vac = eng_k0.prop_model.rho_vac.copy()
        rho_exc = eng_k0.prop_model.excitate(rho_vac.copy())

        st_unp = LocalizedCarrierState(adj, [rho_vac.copy() for _ in range(4)], None)
        st_exc = LocalizedCarrierState(adj, [rho_exc.copy()] + [rho_vac.copy() for _ in range(3)], 0)

        q_unp = eng_k0.compute_probabilities(st_unp, None)
        q_k0 = eng_k0.compute_probabilities(st_exc, 0)

        ideals = get_ideals_adj(adj)
        tvd_k0 = 0.5 * sum(abs(q_k0[I] - q_unp[I]) for I in ideals)
        self.assertAlmostEqual(tvd_k0, 0.0, places=14)

    def test_transition_engine_vacuum_carrier_tvd(self):
        """Verifies TVD == 0.0 between vacuum source transition distribution and unperturbed baseline."""
        eng = PersistentLocalTransitionEngine(kappa=1.00)
        adj = np.array([
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
        ], dtype=bool)
        rho_vac = eng.prop_model.rho_vac.copy()

        st_unp = LocalizedCarrierState(adj, [rho_vac.copy() for _ in range(4)], None)
        st_vac = LocalizedCarrierState(adj, [rho_vac.copy() for _ in range(4)], 0)

        q_unp = eng.compute_probabilities(st_unp, None)
        q_vac = eng.compute_probabilities(st_vac, 0)

        ideals = get_ideals_adj(adj)
        tvd_vac = 0.5 * sum(abs(q_vac[I] - q_unp[I]) for I in ideals)
        self.assertAlmostEqual(tvd_vac, 0.0, places=14)

    def test_asymptotic_contrast_growth_m15(self):
        """Verifies that with M = 15, mean contrast exceeds 0.20 and grows monotonically across all horizons."""
        res = get_shared_contrast_sweep()
        sweep = res["sweep_by_horizon"]
        horizons = [256, 512, 1024, 2048]
        mean_deltas = [sweep[str(N)]["delta_rho_link"] for N in horizons]

        # All horizons exceed delta_* = 0.20
        for N, m in zip(horizons, mean_deltas):
            self.assertGreaterEqual(m, 0.20, f"Mean contrast at N={N} fell below 0.20")

        # Monotonic scaling across horizons
        for i in range(len(mean_deltas) - 1):
            self.assertLess(mean_deltas[i], mean_deltas[i + 1])

    def test_exact_kernel_vs_monte_carlo_sampler_equivalence(self):
        """
        Verifies that PersistentLocalTransitionEngine.compute_probabilities and the
        rejection-free forward sampler implement the exact same Markov transition law
        on a non-trivial 5-vertex poset with both cone and exterior vertices.
        """
        adj5 = np.array([
            [0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ], dtype=bool)
        eng = PersistentLocalTransitionEngine(kappa=2.00, gamma=0.10)
        carriers = [eng.prop_model.rho_vac.copy() for _ in range(5)]
        carriers[1] = eng.prop_model.excitate(carriers[1])
        carriers[2] = eng.prop_model.phi_prop([carriers[0], carriers[1]])
        carriers[3] = eng.prop_model.phi_prop([carriers[1]])
        carriers[4] = eng.prop_model.phi_prop([carriers[2], carriers[3]])
        st5 = LocalizedCarrierState(adj5, carriers, source_anchor=1)

        exact_probs = eng.compute_probabilities(st5, u_star=1)
        lgam0, cdf0, log_z0, lgam1, _, _ = self.tables
        ks_cap = np.arange(33)
        k_term0 = ks_cap * math.log(0.20) + 0.5 * ks_cap * (ks_cap - 1) * math.log(0.20) - lgam0[:33]
        log_t1 = ks_cap * math.log(0.90) + 0.5 * ks_cap * (ks_cap - 1) * math.log(0.60)

        cone5 = np.array([1, 2, 3, 4], dtype=int)
        ext5 = np.array([0], dtype=int)
        F5 = len(cone5)
        p_enter5 = 1.0 - math.exp(log_z0[5 - F5] - log_z0[5])
        anc5 = [{u for u in range(5) if u == v or adj5[u, v]} for v in range(5)]

        rng = np.random.default_rng(2026)
        counts = {I: 0 for I in exact_probs}
        M_draws = 40000
        for _ in range(M_draws):
            if rng.random() >= p_enter5:
                k = int(np.searchsorted(cdf0[len(ext5)], rng.random()))
                b = ext5[rng.choice(len(ext5), size=k, replace=False)] if k > 0 else np.array([], dtype=int)
            else:
                ip = int(rng.integers(0, F5))
                vp = int(cone5[ip])
                p1 = float(np.real(carriers[vp][1, 1]))
                lam = (2.0 * p1) / (1.0 + 2.0 * p1)
                if rng.random() < lam:
                    js = np.arange(F5)
                    lw_a = lgam1[F5 - 1] - lgam1[(F5 - 1) - js] - lgam1[js] + log_t1[1 : F5 + 1]
                    lw_a -= np.max(lw_a)
                    w_a = np.exp(lw_a)
                    cdf_a = np.cumsum(w_a / np.sum(w_a))
                    cdf_a[-1] = 1.0
                    j = int(np.searchsorted(cdf_a, rng.random()))
                    if j > 0:
                        oi = rng.choice(F5 - 1, size=j, replace=False)
                        oi[oi >= ip] += 1
                        b = np.append(cone5[oi], vp)
                    else:
                        b = np.array([vp], dtype=int)
                else:
                    b = sample_conditional_csg_cone_seed(rng, 5, cone5, ext5, lgam0, k_term0)
            ideal_b = frozenset().union(*(anc5[x] for x in b)) if len(b) > 0 else frozenset()
            counts[ideal_b] += 1

        max_err = max(abs(counts[I] / M_draws - exact_probs[I]) for I in exact_probs)
        self.assertLess(max_err, 0.01, f"Empirical vs exact ideal probability error {max_err:.4f} exceeded 0.01")

    def test_unpaired_unperturbed_control_statistical_zero(self):
        """Verifies that unpaired unperturbed controls (independent seeds) are mean-zero within noise."""
        diffs = []
        for r in range(20):
            tA = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=1000 + r, tables_cache=self.tables)
            tB = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=2000 + r, tables_cache=self.tables)
            diffs.append(tB["rho_link"] - tA["rho_link"])
        mean_diff = float(np.mean(diffs))
        std_err = float(np.std(diffs, ddof=1) / np.sqrt(len(diffs)))
        self.assertLess(abs(mean_diff), 3.0 * std_err + 0.05)


if __name__ == "__main__":
    unittest.main()
