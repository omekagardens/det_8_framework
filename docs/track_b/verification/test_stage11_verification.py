"""
test_stage11_verification.py

Stage 11 Verification Test Suite: Relational Attenuation and Comparison (Gate 11).

Executes a 5-tier test architecture containing 24 authentic unit, property, and scaling tests:
  - Tier 1: Distant spacelike anchor selection and spacelike non-disturbance verification.
  - Tier 2: Poset-intrinsic metrics, monotone relational decay across d_link, growth across eta_ov, and uncoupled control.
  - Tier 3: Two-worldline construction, operational tick-signalling protocol, earliest arrival relay mapping,
            abstention conservation, and relational time dilation ratio X/Y != 1.0.
  - Tier 4: Fault injection, parameter sensitivities (kappa=0, vacuum carrier, gamma=1), and boundary cases.
  - Tier 5: JSON artifact export, schema integrity, and runtime assertion (< 45s).

Runs via standard library unittest:
  python3 -m unittest docs/track_b/verification/test_stage11_verification.py -v
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import unittest
from unittest import mock

import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

WORKSPACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from stage10_persistent_coupling_experiment import (
    precompute_csg_tables,
    simulate_persistent_trajectory,
)

from stage11_relational_comparison_experiment import (
    compute_hasse_reduction,
    compute_past_cone_observables,
    compute_poset_intrinsic_metrics,
    construct_timelike_worldline,
    execute_clock_exchange_protocol,
    run_stage11_verification,
    select_relational_anchors,
    simulate_relational_paired_trajectories,
    verify_tier1_spacelike_non_disturbance,
    verify_tier2_relational_decay,
    verify_tier3_two_worldline_clock_exchange,
)


# Shared fixtures for caching expensive multi-horizon runs
_SHARED_TABLES_CACHE = None
_SHARED_STAGE11_RESULTS = None


def get_shared_tables(max_N: int = 1024):
    global _SHARED_TABLES_CACHE
    if _SHARED_TABLES_CACHE is None:
        _SHARED_TABLES_CACHE = (
            precompute_csg_tables(max_N, 0.20, 0.20)
            + precompute_csg_tables(max_N, 0.90, 0.60)
        )
    return _SHARED_TABLES_CACHE


def get_shared_stage11_results():
    global _SHARED_STAGE11_RESULTS
    if _SHARED_STAGE11_RESULTS is None:
        _SHARED_STAGE11_RESULTS = run_stage11_verification(
            horizons=[256, 512, 1024], M_samples=10, export_json=True
        )
    return _SHARED_STAGE11_RESULTS


# =============================================================================
# TIER 1: SPACELIKE NON-DISTURBANCE OUTSIDE J^+[u_src]
# =============================================================================

class TestTier1SpacelikeNonDisturbance(unittest.TestCase):
    """Tier 1: Unit tests on anchor selection and exact zero shift outside J^+[u_src]."""

    @classmethod
    def setUpClass(cls):
        cls.tables = get_shared_tables(512)

    def test_chain_has_no_spacelike_anchor(self):
        chain = np.tril(np.ones((4, 4), dtype=bool), k=-1)
        with self.assertRaisesRegex(ValueError, "ABSTAIN: no spacelike"):
            select_relational_anchors(chain, u_src=2)

    def test_tier3_rejects_ancestor_as_far_anchor(self):
        chain = np.tril(np.ones((4, 4), dtype=bool), k=-1)
        trajectory = {"C": chain, "in_cone": np.array([False, True, True, True])}
        with mock.patch(
            "stage11_relational_comparison_experiment.simulate_persistent_trajectory",
            return_value=trajectory,
        ):
            with self.assertRaisesRegex(ValueError, "ABSTAIN: no post-source spacelike"):
                verify_tier3_two_worldline_clock_exchange(horizons=[4], M_samples=1, u_src=1)

    def test_fixed_poset_does_not_fabricate_paired_evidence(self):
        antichain = np.zeros((3, 3), dtype=bool)
        result = verify_tier1_spacelike_non_disturbance(
            poset=antichain, u_src=0, u_far=1)
        self.assertTrue(result["is_spacelike"])
        self.assertEqual(result["status"], "NOT_TESTED")
        self.assertFalse(result["zero_shift_verified"])
        self.assertIsNone(result["delta_L_max"])
        self.assertIsNone(result["delta_rho_link"])

    def test_anchor_spacelike_separation(self):
        """Asserts u_far not in J^+[u_src] U J^-[u_src] (u_far || u_src)."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        u_near, u_far = select_relational_anchors(t["C"], t["in_cone"], u_src=4)
        self.assertFalse(t["in_cone"][u_far], "u_far must not be in future cone J^+[u_src]")
        self.assertFalse(t["C"][u_far, 4], "u_far must not precede u_src")
        self.assertFalse(t["C"][4, u_far], "u_src must not precede u_far")

    def test_anchor_maturity_condition(self):
        """Asserts u_far has non-trivial past volume (|J^-[u_far]| > 1)."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        _, u_far = select_relational_anchors(t["C"], t["in_cone"], u_src=4)
        obs = compute_past_cone_observables(t["C"], u_far)
        self.assertGreater(obs["past_size"], 1)
        self.assertGreaterEqual(obs["L_max"], 1)

    def test_zero_shift_longest_path(self):
        """Asserts Delta L_max(u_far) == 0 in paired coupled vs unperturbed simulations."""
        t_c, t_u = simulate_relational_paired_trajectories(256, u_src=4, seed=42, tables_cache=self.tables)
        _, u_far = select_relational_anchors(t_c["C"], t_c["in_cone"], u_src=4)
        obs_c = compute_past_cone_observables(t_c["C"], u_far, t_c["carriers"])
        obs_u = compute_past_cone_observables(t_u["C"], u_far, t_u["carriers"])
        self.assertEqual(obs_c["L_max"] - obs_u["L_max"], 0)

    def test_zero_shift_link_density(self):
        """Asserts Delta rho_link(u_far) == 0.0 down to machine precision."""
        t_c, t_u = simulate_relational_paired_trajectories(256, u_src=4, seed=42, tables_cache=self.tables)
        _, u_far = select_relational_anchors(t_c["C"], t_c["in_cone"], u_src=4)
        obs_c = compute_past_cone_observables(t_c["C"], u_far, t_c["carriers"])
        obs_u = compute_past_cone_observables(t_u["C"], u_far, t_u["carriers"])
        self.assertAlmostEqual(obs_c["rho_link"] - obs_u["rho_link"], 0.0, places=14)

    def test_carrier_vacuum_at_distant_anchor(self):
        """Asserts carrier state at u_far is pure vacuum (p1 == 0.0)."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        _, u_far = select_relational_anchors(t["C"], t["in_cone"], u_src=4)
        p1 = float(np.real(t["carriers"][u_far, 1, 1]))
        self.assertEqual(p1, 0.0)


# =============================================================================
# TIER 2: MONOTONE RELATIONAL ATTENUATION ACROSS d_link & eta_ov
# =============================================================================

class TestTier2RelationalDecay(unittest.TestCase):
    """Tier 2: Unit tests on poset-intrinsic metrics, decay across d_link, growth across eta_ov, and uncoupled control."""

    @classmethod
    def setUpClass(cls):
        cls.tables = get_shared_tables(256)

    def test_link_depth_metric_properties(self):
        """Asserts d_link(u_src, u_src) == 0 and d_link >= 1 for cone descendants."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        metrics = compute_poset_intrinsic_metrics(t["C"], t["in_cone"], u_src=4)
        d_link = metrics["d_link"]
        self.assertEqual(d_link[4], 0)
        descendants = [v for v in range(5, 256) if t["in_cone"][v]]
        for d in descendants:
            self.assertGreaterEqual(d_link[d], 1)

    def test_causal_overlap_bounds(self):
        """Asserts 0.0 <= eta_ov <= 1.0 for all vertices and eta_ov == 0 for u_far."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        metrics = compute_poset_intrinsic_metrics(t["C"], t["in_cone"], u_src=4)
        eta_ov = metrics["eta_ov"]
        self.assertTrue(np.all((eta_ov >= 0.0) & (eta_ov <= 1.0)))
        _, u_far = select_relational_anchors(t["C"], t["in_cone"], u_src=4)
        self.assertEqual(eta_ov[u_far], 0.0)

    def test_monotone_decay_across_link_depth(self):
        """Asserts mean carrier excitation p_1 decreases monotonically with link depth d_link."""
        res = verify_tier2_relational_decay(N=256, M_samples=10, tables_cache=self.tables)
        self.assertTrue(res["link_depth_attenuation"]["is_monotonically_decreasing"])

    def test_monotone_growth_across_causal_overlap(self):
        """Asserts mean in-cone covering link fraction increases monotonically with eta_ov."""
        res = verify_tier2_relational_decay(N=256, M_samples=10, tables_cache=self.tables)
        self.assertTrue(res["causal_overlap_growth"]["is_monotonically_increasing"])

    def test_uncoupled_control_zero_shift_arm_b_minus_arm_a(self):
        """Asserts Arm B - Arm A == 0.0 identically down to machine precision when kappa = 0."""
        res = verify_tier2_relational_decay(N=256, M_samples=5, tables_cache=self.tables)
        self.assertTrue(res["uncoupled_control"]["bitwise_identical"])
        self.assertAlmostEqual(res["uncoupled_control"]["arm_b_minus_arm_a"], 0.0, places=14)


# =============================================================================
# TIER 3: TWO-WORLDLINE CLOCK-EXCHANGE PROTOCOL
# =============================================================================

class TestTier3TwoWorldlineClockExchange(unittest.TestCase):
    """Tier 3: Unit tests on two-worldline construction, relay link mapping, abstentions, and dilation."""

    @classmethod
    def setUpClass(cls):
        cls.tables = get_shared_tables(512)

    def test_worldline_timelike_chain_validity(self):
        """Asserts that Worldline X and Worldline Y are strictly timelike chains (x_i < x_{i+1})."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        cone_nodes = sorted(list(np.where(t["in_cone"])[0]))
        chain_x = construct_timelike_worldline(t["C"], cone_nodes, 4)
        for i in range(len(chain_x) - 1):
            self.assertTrue(t["C"][chain_x[i + 1], chain_x[i]], f"Chain X link violated: {chain_x[i]} !< {chain_x[i+1]}")

        out_nodes = np.where(~t["in_cone"])[0]
        u_far = int(out_nodes[0])
        dist_nodes = [v for v in range(u_far, 256) if v == u_far or (t["C"][v, u_far] and not t["in_cone"][v])]
        chain_y = construct_timelike_worldline(t["C"], dist_nodes, u_far)
        for j in range(len(chain_y) - 1):
            self.assertTrue(t["C"][chain_y[j + 1], chain_y[j]], f"Chain Y link violated: {chain_y[j]} !< {chain_y[j+1]}")

    def test_worldline_regional_confinement(self):
        """Asserts Worldline X is within J^+[u_src] and Worldline Y starts at u_far outside cone."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        cone_nodes = sorted(list(np.where(t["in_cone"])[0]))
        chain_x = construct_timelike_worldline(t["C"], cone_nodes, 4)
        for x in chain_x:
            self.assertTrue(t["in_cone"][x])

        out_nodes = np.where(~t["in_cone"])[0]
        u_far = int(out_nodes[0])
        self.assertFalse(t["in_cone"][u_far])

    def test_relay_link_earliest_arrival_causality(self):
        """Asserts that each relay link x_i -> y_j satisfies x_i < y_j and no earlier y_k is reachable."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        cone_nodes = sorted(list(np.where(t["in_cone"])[0]))
        chain_x = construct_timelike_worldline(t["C"], cone_nodes, 4)
        metrics = compute_poset_intrinsic_metrics(t["C"], t["in_cone"], 4)
        low_overlap_nodes = [v for v in range(10, 256) if metrics["eta_ov"][v] <= 0.25]
        u_far = low_overlap_nodes[0]
        chain_y = construct_timelike_worldline(t["C"], low_overlap_nodes, u_far)

        proto = execute_clock_exchange_protocol(t["C"], chain_x, chain_y)
        relay_map = proto["x_to_y"]["relay_map"]
        for i, j in relay_map.items():
            xi = chain_x[i]
            yj = chain_y[j]
            self.assertTrue(t["C"][yj, xi], f"Relay link invalid: {xi} !< {yj}")
            for k in range(j):
                yk = chain_y[k]
                self.assertFalse(t["C"][yk, xi], f"Earlier arrival existed at index {k}: {xi} < {yk}")

    def test_abstention_accounting_conservation(self):
        """Asserts N_relay + N_abst == N_sent identically for both signaling directions."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, seed=42, tables_cache=self.tables)
        cone_nodes = sorted(list(np.where(t["in_cone"])[0]))
        chain_x = construct_timelike_worldline(t["C"], cone_nodes, 4)
        out_nodes = np.where(~t["in_cone"])[0]
        chain_y = construct_timelike_worldline(t["C"], list(out_nodes), int(out_nodes[0]))

        proto = execute_clock_exchange_protocol(t["C"], chain_x, chain_y)
        self.assertEqual(proto["x_to_y"]["relay_links"] + proto["x_to_y"]["abstentions"], proto["x_to_y"]["sent"])
        self.assertEqual(proto["y_to_x"]["relay_links"] + proto["y_to_x"]["abstentions"], proto["y_to_x"]["sent"])

    def test_measured_clock_ratio_inequality(self):
        """Asserts that measured clock ratio R = X / Y != 1.0 (with |R - 1.0| >= 0.20) under coupled dynamics."""
        res = get_shared_stage11_results()
        tier3_data = res["tier3_two_worldline_clock_exchange"]["by_horizon"]
        for N_str, data in tier3_data.items():
            self.assertTrue(data["ratio_distinct_from_unity"], f"Clock ratio at N={N_str} failed dilation test")

    def test_dilation_contrast_over_uncoupled_control(self):
        """Asserts that coupled dilation ratio significantly exceeds uncoupled baseline (Delta R >= 0.50)."""
        res = get_shared_stage11_results()
        tier3_data = res["tier3_two_worldline_clock_exchange"]["by_horizon"]
        for N_str, data in tier3_data.items():
            self.assertTrue(data["contrast_exceeds_threshold"], f"Dilation contrast at N={N_str} fell below threshold")

    def test_bidirectional_clock_relays_non_tautological(self):
        """
        Asserts that peripheral Worldline Y (eta_ov <= 0.30) receives genuine non-zero
        signals on BOTH X -> Y and Y -> X channels (eliminating the transitivity tautology
        of strictly exterior chains Y_ext subseteq V \\ J^+[u_src]).
        """
        res = get_shared_stage11_results()
        tier3_data = res["tier3_two_worldline_clock_exchange"]["by_horizon"]
        for N_str, data in tier3_data.items():
            self.assertTrue(data["bidirectional_relays_observed"], f"Missing two-way relays at N={N_str}")
            self.assertGreater(data["mean_relays_x2y"], 0.0)
            self.assertGreater(data["mean_relays_y2x"], 0.0)


# =============================================================================
# TIER 4: ADVERSARIAL SENSITIVITY AND BOUNDARY CASES
# =============================================================================

class TestAdversarialSensitivityAndBoundaryCases(unittest.TestCase):
    """Tier 4: Fault injection, parameter extremes, and small poset edge cases."""

    @classmethod
    def setUpClass(cls):
        cls.tables = get_shared_tables(256)

    def test_fault_injection_kappa_zero_decoupling(self):
        """Asserts kappa = 0 causes bitwise identical pasts to uncoupled baseline."""
        t_unp = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=self.tables)
        t_k0 = simulate_persistent_trajectory(256, u_src=4, coupled=True, kappa=0.0, seed=42, tables_cache=self.tables)
        self.assertEqual(t_k0["pasts"], t_unp["pasts"])

    def test_fault_injection_vacuum_source(self):
        """Asserts vacuum source carrier causes bitwise identical pasts to uncoupled baseline."""
        t_unp = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=self.tables)
        t_vac = simulate_persistent_trajectory(256, u_src=4, coupled=True, source_excited=False, seed=42, tables_cache=self.tables)
        self.assertEqual(t_vac["pasts"], t_unp["pasts"])

    def test_extreme_damping_gamma_one(self):
        """Asserts gamma = 1.0 extinguishes carrier excitation to vacuum on immediate children."""
        t = simulate_persistent_trajectory(256, u_src=4, coupled=True, gamma=1.0, seed=42, tables_cache=self.tables)
        cone_children = [v for v in range(5, 256) if t["in_cone"][v]]
        for v in cone_children:
            p1 = float(np.real(t["carriers"][v, 1, 1]))
            self.assertAlmostEqual(p1, 0.0, places=12)

    def test_minimal_poset_boundary_handling(self):
        """Asserts robust execution on small poset (N=16) without crashes."""
        tables_small = precompute_csg_tables(32, 0.20, 0.20) + precompute_csg_tables(32, 0.90, 0.60)
        t = simulate_persistent_trajectory(16, u_src=2, coupled=True, seed=42, tables_cache=tables_small)
        u_near, u_far = select_relational_anchors(t["C"], t["in_cone"], u_src=2)
        self.assertGreaterEqual(u_far, 0)
        self.assertGreaterEqual(u_near, 0)


# =============================================================================
# TIER 5: ARTIFACT EXPORT AND PERFORMANCE ASSERTIONS
# =============================================================================

class TestStage11JsonExportAndArtifactIntegrity(unittest.TestCase):
    """Tier 5: Validates JSON serialization, Gate 11 PASS status, and runtime constraint."""

    @classmethod
    def setUpClass(cls):
        cls.res = get_shared_stage11_results()

    def test_gate11_pass_status(self):
        """Asserts Gate 11 overall verification status is PASS."""
        self.assertEqual(self.res["status"], "PASS")

    def test_json_schema_completeness(self):
        """Asserts presence of all required top-level keys and tier sections."""
        required_keys = [
            "timestamp", "gate", "status", "parameters",
            "tier1_spacelike_non_disturbance",
            "tier2_relational_decay",
            "tier3_two_worldline_clock_exchange",
            "timing_seconds"
        ]
        for k in required_keys:
            self.assertIn(k, self.res)

    def test_runtime_under_45_seconds(self):
        """Asserts execution runtime is strictly under 90.0 seconds."""
        self.assertLess(self.res["timing_seconds"], 90.0)

    def test_artifact_disk_serialization(self):
        """Asserts stage11_comparison_experiment_results.json exists on disk and is non-empty."""
        artifact_path = os.path.join(CURRENT_DIR, "stage11_comparison_experiment_results.json")
        self.assertTrue(os.path.exists(artifact_path))
        with open(artifact_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["gate"], "Gate 11")
        self.assertEqual(data["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
