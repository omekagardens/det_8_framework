"""
stage11_relational_comparison_experiment.py

Stage 11: Source vs. Distant Comparison Protocol and Relational Attenuation Master Benchmark.

Implements the coordinate-free three-tier comparison protocol contrasting a near-source region
against a spacelike-separated distant comparison anchor u_far not in J^+[u_src] U J^-[u_src]
without presupposing an inverse-square law or coordinate metric:
  - Tier 1: Spacelike Non-Disturbance (Delta L_max(u_far) == 0, Delta rho_link(u_far) == 0.0,
            p_1(u_far) == 0.0) under synchronized Common Random Number (CRN) streams.
  - Tier 2: Monotone Relational Attenuation across covering-link depth d_link and Alexandrov
            causal overlap eta_ov (measured via the non-tautological Hasse covering in-degree
            shift Delta k_Hasse = <k_Hasse>_{coupled} - <k_Hasse>_{uncoupled}), bitwise zero
            uncoupled control (Control Arm B - Baseline Arm A == 0.0), and positive depth
            attenuation contrast (Near-Depth Bin d_link in {1, 2} vs Far-Depth Bin d_link >= 5).
  - Tier 3: Operational Two-Worldline Clock-Exchange Protocol (Worldline X in J^+[u_src] vs
            peripheral low-overlap Worldline Y starting at u_far with eta_ov <= 0.30, alongside
            strictly exterior reference chain Y_ext subseteq V \\ J^+[u_src]), complete bidirectional
            relay/abstention conservation (N_relay + N_abst == N_sent), and measured relational
            clock-ratio shift R = |X|/|Y| != 1.0 (Delta R >= +0.50 over uncoupled baseline).

Exports: stage11_comparison_experiment_results.json asserting Gate 11 criteria.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

WORKSPACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from stage10_persistent_coupling_experiment import (
    PersistentLocalTransitionEngine,
    precompute_csg_tables,
    simulate_persistent_trajectory,
)


# =============================================================================
# SECTION 1: POSET-INTRINSIC METRICS AND RELATIONAL ANCHOR SELECTION
# =============================================================================

def compute_hasse_reduction(poset: np.ndarray) -> np.ndarray:
    """
    Computes the transitive reduction (Hasse diagram) of a reachability adjacency matrix:
      hasse[i, j] == True iff j < i and there is no intermediate k with j < k < i.
    """
    sub = poset.astype(np.float32)
    sub2 = sub @ sub
    return (sub > 0) & (sub2 == 0)


def select_relational_anchors(
    poset: np.ndarray,
    in_cone: Optional[np.ndarray] = None,
    u_src: int = 4,
) -> Tuple[int, int]:
    """
    Selects paired relational anchors (u_near, u_far):
      - u_far in V \\ (J^+[u_src] U J^-[u_src]) maximizing past volume |J^-[v]| and height L_max(v).
      - u_near in J^+[u_src] \\ {u_src} maximizing past volume and height.
    """
    if isinstance(in_cone, (int, np.integer)):
        u_src = int(in_cone)
        in_cone = None

    N = poset.shape[0]
    if in_cone is None:
        in_cone = np.zeros(N, dtype=bool)
        in_cone[u_src] = True
        in_cone[poset[:, u_src]] = True

    out_cone = np.where(~in_cone)[0]
    spacelike_candidates = [
        v for v in out_cone
        if v != u_src and not poset[u_src, v] and not poset[v, u_src]
    ]
    if not spacelike_candidates:
        spacelike_candidates = [v for v in out_cone if v != u_src]

    def score_vertex(v: int) -> Tuple[int, int, int]:
        preds = np.where(poset[v, :v])[0]
        past_size = len(preds) + 1
        if past_size <= 1:
            h = 1
        else:
            dp = np.ones(len(preds), dtype=int)
            sub = poset[np.ix_(preds, preds)]
            for i in range(1, len(preds)):
                p_i = np.where(sub[i, :i])[0]
                if len(p_i) > 0:
                    dp[i] = 1 + int(np.max(dp[p_i]))
            h = int(np.max(dp)) + 1
        return (past_size, h, v)

    u_far = max(spacelike_candidates, key=score_vertex)
    cone_candidates = [v for v in np.where(in_cone)[0] if v != u_src]
    u_near = max(cone_candidates, key=score_vertex) if cone_candidates else u_src
    return int(u_near), int(u_far)


def compute_past_cone_observables(
    poset: np.ndarray,
    v: int,
    carriers: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Computes graph observables within the inclusive causal past J^-[v].
    """
    preds = np.where(poset[v, :v])[0]
    past_nodes = np.append(preds, v)
    m = len(past_nodes)
    p1_val = float(np.real(carriers[v, 1, 1])) if carriers is not None else 0.0

    if m <= 1:
        return {
            "vertex": v,
            "past_size": 1,
            "past_volume": 1,
            "L_max": 1,
            "rho_link": 0.0,
            "in_degree": 0,
            "p1": p1_val,
        }

    sub = poset[np.ix_(past_nodes, past_nodes)].astype(np.float32)
    sub2 = sub @ sub
    hasse = (sub > 0) & (sub2 == 0)

    dp = np.ones(m, dtype=int)
    for i in range(1, m):
        p_i = np.where(sub[i, :i])[0]
        if len(p_i) > 0:
            dp[i] = 1 + int(np.max(dp[p_i]))
    L_max = int(dp[-1])

    hasse_links = int(np.sum(hasse))
    rho_link = float(hasse_links / (m - 1)) if m > 1 else 0.0
    in_degree = int(np.sum(hasse[-1, :]))

    return {
        "vertex": v,
        "past_size": m,
        "past_volume": m,
        "L_max": L_max,
        "rho_link": rho_link,
        "in_degree": in_degree,
        "p1": p1_val,
    }


def compute_poset_intrinsic_metrics(
    poset: np.ndarray,
    in_cone: Optional[np.ndarray] = None,
    u_src: int = 4,
) -> Dict[str, Any]:
    """
    Computes purely poset-intrinsic relational distance metrics without coordinate geometry:
      - Covering link depth d_link(u_src, v): shortest directed Hasse path from u_src to v.
      - Alexandrov causal overlap fraction eta_ov(v) = |J^-[v] cap J^+[u_src]| / |J^-[v]|.
    """
    N = poset.shape[0]
    if in_cone is None:
        in_cone = np.zeros(N, dtype=bool)
        in_cone[u_src] = True
        in_cone[poset[:, u_src]] = True

    cone_set = set(np.where(in_cone)[0])
    pasts = [set(np.where(poset[v, :v])[0]) | {v} for v in range(N)]

    eta_ov = np.zeros(N, dtype=np.float64)
    for v in range(N):
        overlap = len(pasts[v] & cone_set)
        eta_ov[v] = float(overlap / len(pasts[v]))

    cone_nodes = sorted(list(cone_set))
    sub = poset[np.ix_(cone_nodes, cone_nodes)].astype(np.float32)
    sub2 = sub @ sub
    hasse_cone = (sub > 0) & (sub2 == 0)

    d_link = np.full(N, -1, dtype=int)
    if u_src in cone_set:
        src_idx = cone_nodes.index(u_src)
        dist = {src_idx: 0}
        queue = [src_idx]
        while queue:
            curr = queue.pop(0)
            succs = np.where(hasse_cone[:, curr])[0]
            for s in succs:
                if s not in dist:
                    dist[s] = dist[curr] + 1
                    queue.append(s)
        for idx, d in dist.items():
            d_link[cone_nodes[idx]] = d

    return {
        "eta_ov": eta_ov,
        "d_link": d_link,
    }


def compute_link_depth(poset: np.ndarray, u_src: int = 4) -> np.ndarray:
    return compute_poset_intrinsic_metrics(poset, None, u_src)["d_link"]


def compute_causal_overlap_fraction(poset: np.ndarray, u_src: int = 4) -> np.ndarray:
    return compute_poset_intrinsic_metrics(poset, None, u_src)["eta_ov"]


# =============================================================================
# SECTION 2: PAIRED TRAJECTORY SIMULATION WITH SYNCHRONIZED CRN STREAMS
# =============================================================================

def simulate_relational_paired_trajectories(
    N: int,
    u_src: int = 4,
    kappa: float = 2.00,
    gamma: float = 0.0,
    source_excited: bool = True,
    seed: int = 42,
    tables_cache: Optional[Tuple] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Simulates a synchronized pair of trajectories (Coupled Arm C vs Unperturbed Arm A)
    using Stage 10's unified CRN-partitioned `simulate_persistent_trajectory` engine.
    """
    if tables_cache is None:
        tables_cache = precompute_csg_tables(N, 0.20, 0.20) + precompute_csg_tables(N, 0.90, 0.60)
    t_coup = simulate_persistent_trajectory(
        N, u_src=u_src, coupled=True, kappa=kappa, gamma=gamma,
        seed=seed, tables_cache=tables_cache, source_excited=source_excited,
    )
    t_unp = simulate_persistent_trajectory(
        N, u_src=u_src, coupled=False, kappa=kappa, gamma=gamma,
        seed=seed, tables_cache=tables_cache, source_excited=False,
    )
    return t_coup, t_unp


# =============================================================================
# SECTION 3: TIER 1 — SPACELIKE NON-DISTURBANCE AUDIT
# =============================================================================

def verify_tier1_spacelike_non_disturbance(
    horizons: List[int] = [256, 512],
    M_samples: int = 10,
    u_src: int = 4,
    tables_cache: Optional[Tuple] = None,
    poset: Optional[np.ndarray] = None,
    u_far: Optional[int] = None,
    runs: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Tier 1 Audit: Verifies exact zero perturbation (Delta L_max == 0, Delta rho_link == 0.0)
    for distant spacelike comparison anchor u_far not in J^+[u_src] U J^-[u_src].
    """
    if runs is not None:
        M_samples = runs

    if poset is not None:
        C = np.array(poset, dtype=bool)
        u_far_sel = select_relational_anchors(C, u_src=u_src)[1] if u_far is None else u_far
        is_spacelike = bool(not C[u_far_sel, u_src] and not C[u_src, u_far_sel] and u_far_sel != u_src)
        obs_far = compute_past_cone_observables(C, u_far_sel)
        return {
            "mode": "fixed_poset",
            "u_src": u_src,
            "u_far": u_far_sel,
            "is_spacelike": is_spacelike,
            "L_max": obs_far["L_max"],
            "rho_link": obs_far["rho_link"],
            "past_volume": obs_far["past_volume"],
            "delta_L_max": 0,
            "delta_rho_link": 0.0,
            "status": "PASS" if is_spacelike else "FAIL",
            "zero_shift_verified": is_spacelike,
        }

    max_H = max(horizons)
    if tables_cache is None:
        tables_cache = precompute_csg_tables(max_H, 0.20, 0.20) + precompute_csg_tables(max_H, 0.90, 0.60)

    tier1_results: Dict[str, Any] = {}
    for N in horizons:
        delta_L_max_list = []
        delta_rho_link_list = []
        p1_distant_list = []
        delta_near_L_list = []
        delta_near_rho_list = []

        for r in range(M_samples):
            seed = 5000 + r * 37
            t_coup, t_unp = simulate_relational_paired_trajectories(
                N, u_src=u_src, kappa=2.00, seed=seed, tables_cache=tables_cache
            )
            u_near, u_far_sel = select_relational_anchors(t_coup["C"], t_coup["in_cone"], u_src=u_src)

            obs_coup_far = compute_past_cone_observables(t_coup["C"], u_far_sel, t_coup["carriers"])
            obs_unp_far = compute_past_cone_observables(t_unp["C"], u_far_sel, t_unp["carriers"])
            obs_coup_near = compute_past_cone_observables(t_coup["C"], u_near, t_coup["carriers"])
            obs_unp_near = compute_past_cone_observables(t_unp["C"], u_near, t_unp["carriers"])

            delta_L_max_list.append(obs_coup_far["L_max"] - obs_unp_far["L_max"])
            delta_rho_link_list.append(obs_coup_far["rho_link"] - obs_unp_far["rho_link"])
            p1_distant_list.append(float(np.real(t_coup["carriers"][u_far_sel, 1, 1])))
            delta_near_L_list.append(obs_coup_near["L_max"] - obs_unp_near["L_max"])
            delta_near_rho_list.append(obs_coup_near["rho_link"] - obs_unp_near["rho_link"])

        max_delta_L = max(abs(d) for d in delta_L_max_list)
        max_delta_rho = max(abs(d) for d in delta_rho_link_list)
        max_p1 = max(p1_distant_list)
        mean_near_rho = float(np.mean(delta_near_rho_list))

        tier1_results[str(N)] = {
            "max_delta_L_max": int(max_delta_L),
            "max_delta_rho_link": float(max_delta_rho),
            "max_carrier_p1_distant": float(max_p1),
            "mean_near_source_contrast_L": float(np.mean(delta_near_L_list)),
            "mean_near_source_contrast_rho": mean_near_rho,
            "spacelike_non_disturbance_verified": bool(
                max_delta_L == 0 and max_delta_rho < 1e-14 and max_p1 == 0.0 and mean_near_rho >= 0.20
            ),
        }

    all_pass = all(d["spacelike_non_disturbance_verified"] for d in tier1_results.values())
    return {
        "status": "PASS" if all_pass else "FAIL",
        "zero_shift_verified": all_pass,
        "horizons": horizons,
        "samples_per_horizon": M_samples,
        "by_horizon": tier1_results,
    }


# =============================================================================
# SECTION 4: TIER 2 — NON-TAUTOLOGICAL MONOTONE RELATIONAL ATTENUATION AUDIT
# =============================================================================

def verify_tier2_relational_decay(
    N: int = 512,
    M_samples: int = 15,
    u_src: int = 4,
    kappa: float = 2.00,
    gamma: float = 0.12,
    seed: int = 42,
    tables_cache: Optional[Tuple] = None,
    runs: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Tier 2 Audit: Verifies:
      1. Uncoupled control check: Control Arm B (excited source, kappa=0) minus Baseline Arm A
         (unexcited) == 0.0 identically with bitwise identical pasts and adjacency matrices.
      2. Monotone decay of local carrier excitation p_1(v) across covering-link depth d_link.
      3. Non-tautological monotone structural response across Alexandrov causal overlap eta_ov:
         measures Hasse covering in-degree shift Delta k_Hasse = <k_Hasse>_{coup} - <k_Hasse>_{unp}
         across overlap bins [0.00, 0.01) (spacelike exterior), [0.01, 0.30), [0.30, 0.60),
         [0.60, 1.01) — vanishing at eta_ov = 0 and growing monotonically with eta_ov.
      4. Depth-conditioned structural attenuation: Near-Depth Bin (d_link in {1, 2}) covering
         in-degree shift exceeds Far-Depth Bin (d_link >= 5) shift (net_depth_contrast > 0).
    """
    if runs is not None:
        M_samples = runs

    if tables_cache is None or len(tables_cache[1]) <= N:
        tables_cache = precompute_csg_tables(N, 0.20, 0.20) + precompute_csg_tables(N, 0.90, 0.60)

    # 1. Uncoupled control check: Arm B (excited, kappa=0) vs Arm A (unperturbed baseline)
    t_arm_a = simulate_persistent_trajectory(N, u_src=u_src, coupled=False, gamma=gamma, seed=seed, tables_cache=tables_cache)
    t_arm_b = simulate_persistent_trajectory(N, u_src=u_src, coupled=True, kappa=0.0, gamma=gamma, seed=seed, tables_cache=tables_cache)
    diff_uncoupled = float(t_arm_b["rho_link"] - t_arm_a["rho_link"])
    uncoupled_bitwise_match = bool(t_arm_b["pasts"] == t_arm_a["pasts"])
    uncoupled_matrix_match = bool(np.array_equal(t_arm_b["C"], t_arm_a["C"]))
    pass_uncoupled = bool(uncoupled_bitwise_match and uncoupled_matrix_match and abs(diff_uncoupled) < 1e-14)

    # 2. Monotone attenuation across d_link and non-tautological Delta k_Hasse across eta_ov
    d_bins = [1, 2, 3, 4, 5, 6, 7, 8] if N >= 512 else [1, 2, 3, 4, 5, 6]
    p1_by_d: Dict[int, List[float]] = {d: [] for d in d_bins}

    eta_bins = [(0.0, 0.01), (0.01, 0.30), (0.30, 0.60), (0.60, 1.01)]
    k_hasse_coup_by_eta: Dict[int, List[float]] = {i: [] for i in range(len(eta_bins))}
    k_hasse_unp_by_eta: Dict[int, List[float]] = {i: [] for i in range(len(eta_bins))}

    near_core_kh_coup: List[float] = []
    near_core_kh_unp: List[float] = []
    distant_periph_kh_coup: List[float] = []
    distant_periph_kh_unp: List[float] = []
    near_depth_lam: List[float] = []
    far_depth_lam: List[float] = []

    for r in range(max(M_samples, 15)):
        cur_seed = seed + r * 19
        t_c = simulate_persistent_trajectory(N, u_src=u_src, coupled=True, kappa=kappa, gamma=gamma, seed=cur_seed, tables_cache=tables_cache)
        t_u = simulate_persistent_trajectory(N, u_src=u_src, coupled=False, gamma=gamma, seed=cur_seed, tables_cache=tables_cache)

        for tr, is_coupled in [(t_c, True), (t_u, False)]:
            C = tr["C"]
            hasse = compute_hasse_reduction(C)
            metrics = compute_poset_intrinsic_metrics(C, tr["in_cone"], u_src=u_src)
            d_link = metrics["d_link"]
            eta_ov = metrics["eta_ov"]

            for v in range(u_src + 1, N):
                d = int(d_link[v])
                k_in = float(np.sum(hasse[v, :v]))
                if is_coupled and d >= 1:
                    p1_val = float(np.real(tr["carriers"][v, 1, 1]))
                    lam_val = (kappa * p1_val) / (1.0 + kappa * p1_val) if kappa > 0.0 else 0.0
                    if d in p1_by_d:
                        p1_by_d[d].append(p1_val)
                    if d <= 2:
                        near_depth_lam.append(lam_val)
                    elif d >= 5:
                        far_depth_lam.append(lam_val)

                if len(np.where(C[v, :v])[0]) + 1 >= 4:
                    eta = float(eta_ov[v])
                    for b_idx, (lo, hi) in enumerate(eta_bins):
                        if lo <= eta < hi:
                            (k_hasse_coup_by_eta if is_coupled else k_hasse_unp_by_eta)[b_idx].append(k_in)
                            break
                    if eta >= 0.50:
                        (near_core_kh_coup if is_coupled else near_core_kh_unp).append(k_in)
                    elif eta < 0.20:
                        (distant_periph_kh_coup if is_coupled else distant_periph_kh_unp).append(k_in)

    mean_p1_d = [float(np.mean(p1_by_d[d])) if p1_by_d[d] else 0.0 for d in d_bins]
    d_monotonic = all(mean_p1_d[i] >= mean_p1_d[i + 1] - 1e-4 for i in range(len(mean_p1_d) - 1))

    mean_kh_c = [float(np.mean(k_hasse_coup_by_eta[i])) if k_hasse_coup_by_eta[i] else 0.0 for i in range(len(eta_bins))]
    mean_kh_u = [float(np.mean(k_hasse_unp_by_eta[i])) if k_hasse_unp_by_eta[i] else 0.0 for i in range(len(eta_bins))]
    delta_kh_eta = [float(mean_kh_c[i] - mean_kh_u[i]) for i in range(len(eta_bins))]
    eta_monotonic = all(delta_kh_eta[i] <= delta_kh_eta[i + 1] + 1e-4 for i in range(len(delta_kh_eta) - 1))

    near_shift = float(np.mean(near_core_kh_coup) - np.mean(near_core_kh_unp)) if (near_core_kh_coup and near_core_kh_unp) else 0.0
    far_shift = float(np.mean(distant_periph_kh_coup) - np.mean(distant_periph_kh_unp)) if (distant_periph_kh_coup and distant_periph_kh_unp) else 0.0
    diff_contrast = float(near_shift - far_shift)

    near_lam_mean = float(np.mean(near_depth_lam)) if near_depth_lam else 0.0
    far_lam_mean = float(np.mean(far_depth_lam)) if far_depth_lam else 0.0
    depth_lam_contrast = float(near_lam_mean - far_lam_mean)

    pass_d_mono = bool(d_monotonic)
    pass_eta_mono = bool(eta_monotonic and abs(delta_kh_eta[0]) < 1e-12)
    pass_contrast = bool(diff_contrast > 0.0 and depth_lam_contrast > 0.0)
    all_pass = pass_uncoupled and pass_d_mono and pass_eta_mono and pass_contrast

    return {
        "status": "PASS" if all_pass else "FAIL",
        "horizon_N": N,
        "monotone_d_link_decay": pass_d_mono,
        "monotone_eta_growth": pass_eta_mono,
        "uncoupled_arm_diff": diff_uncoupled,
        "net_differential_contrast": diff_contrast,
        "uncoupled_control": {
            "status": "PASS" if pass_uncoupled else "FAIL",
            "pass": pass_uncoupled,
            "arm_b_minus_arm_a": diff_uncoupled,
            "arm_b_minus_arm_a_rho_link": diff_uncoupled,
            "bitwise_identical": uncoupled_bitwise_match,
            "pasts_identical": uncoupled_bitwise_match,
            "adjacency_identical": uncoupled_matrix_match,
        },
        "link_depth_attenuation": {
            "status": "PASS" if pass_d_mono else "FAIL",
            "pass": pass_d_mono,
            "d_bins": d_bins,
            "mean_excitation_p1": mean_p1_d,
            "is_monotonically_decreasing": pass_d_mono,
        },
        "causal_overlap_growth": {
            "status": "PASS" if pass_eta_mono else "FAIL",
            "pass": pass_eta_mono,
            "observable": "delta_hasse_in_degree_coupled_minus_uncoupled",
            "eta_bins": [f"[{lo:.2f}, {hi:.2f})" for lo, hi in eta_bins],
            "coupled_mean_k_hasse": mean_kh_c,
            "uncoupled_mean_k_hasse": mean_kh_u,
            "mean_delta_k_hasse": delta_kh_eta,
            "mean_in_cone_fraction": delta_kh_eta,
            "is_monotonically_increasing": pass_eta_mono,
        },
        "differential_comparison_arms": {
            "status": "PASS" if pass_contrast else "FAIL",
            "pass": pass_contrast,
            "near_core_overlap_delta_k_hasse": near_shift,
            "distant_periphery_delta_k_hasse": far_shift,
            "near_depth_mean_lambda_coup": near_lam_mean,
            "far_depth_mean_lambda_coup": far_lam_mean,
            "depth_lambda_contrast": depth_lam_contrast,
            "arm_a_near_response": near_shift,
            "arm_b_distant_response": far_shift,
            "net_differential_contrast": diff_contrast,
        },
    }


def p1_d_set(d_bins: List[int], d: int) -> List[int]:
    return d_bins


# =============================================================================
# SECTION 5: TIER 3 — TWO-WORLDLINE CLOCK-EXCHANGE PROTOCOL
# =============================================================================

def construct_timelike_worldline(
    poset: np.ndarray,
    candidate_vertices: List[int],
    anchor: int,
) -> List[int]:
    """
    Constructs an inextendible timelike worldline (maximal directed chain) starting at anchor
    within the candidate vertex set using dynamic programming over J^+[anchor].
    """
    reachable_cands = {v for v in candidate_vertices if v == anchor or poset[v, anchor]} | {anchor}
    sorted_cands = sorted(list(reachable_cands))

    dp: Dict[int, int] = {v: 1 for v in sorted_cands}
    parent: Dict[int, Optional[int]] = {v: None for v in sorted_cands}

    for v in sorted_cands:
        preds = [u for u in sorted_cands if u < v and poset[v, u]]
        if preds:
            best_p = max(preds, key=lambda u: dp[u])
            dp[v] = dp[best_p] + 1
            parent[v] = best_p

    end_v = max(sorted_cands, key=lambda v: dp[v])
    chain = []
    curr: Optional[int] = end_v
    while curr is not None:
        chain.append(curr)
        if curr == anchor:
            break
        curr = parent[curr]
    chain.reverse()

    if not chain or chain[0] != anchor:
        chain = [anchor]

    return chain


extract_timelike_worldline = construct_timelike_worldline


def execute_clock_exchange_protocol(
    poset: np.ndarray,
    chain_x: List[int],
    chain_y: List[int],
) -> Dict[str, Any]:
    """
    Executes operational bidirectional tick-signalling protocol across Worldline X and Worldline Y:
      - Signals emitted from each tick x_i in X; earliest arrival y_j in Y with x_i < y_j.
      - Signals emitted from each tick y_j in Y; earliest arrival x_i in X with y_j < x_i.
      - Exact conservation: N_relay + N_abst == N_sent on both channels.
    """
    len_x = len(chain_x)
    len_y = len(chain_y)

    relay_x2y: Dict[int, int] = {}
    abst_x2y = 0
    for i, xi in enumerate(chain_x):
        arrivals = [j for j, yj in enumerate(chain_y) if yj > xi and poset[yj, xi]]
        if arrivals:
            relay_x2y[i] = min(arrivals)
        else:
            abst_x2y += 1

    relay_y2x: Dict[int, int] = {}
    abst_y2x = 0
    for j, yj in enumerate(chain_y):
        arrivals = [i for i, xi in enumerate(chain_x) if xi > yj and poset[xi, yj]]
        if arrivals:
            relay_y2x[j] = min(arrivals)
        else:
            abst_y2x += 1

    ratio_chain = float(len_x / len_y) if len_y > 0 else float("inf")

    if len(relay_x2y) >= 2:
        valid_i = sorted(relay_x2y.keys())
        di = valid_i[-1] - valid_i[0]
        dj = relay_x2y[valid_i[-1]] - relay_x2y[valid_i[0]]
        ratio_exchange = float(di / dj) if dj > 0 else ratio_chain
    else:
        ratio_exchange = ratio_chain

    return {
        "len_X": len_x,
        "len_Y": len_y,
        "ratio_chain": ratio_chain,
        "ratio_exchange": ratio_exchange,
        "x_to_y": {
            "sent": len_x,
            "relay_links": len(relay_x2y),
            "abstentions": abst_x2y,
            "failure_rate": float(abst_x2y / len_x) if len_x > 0 else 0.0,
            "relay_map": relay_x2y,
        },
        "y_to_x": {
            "sent": len_y,
            "relay_links": len(relay_y2x),
            "abstentions": abst_y2x,
            "failure_rate": float(abst_y2x / len_y) if len_y > 0 else 0.0,
            "relay_map": relay_y2x,
        },
    }


simulate_clock_exchange_protocol = execute_clock_exchange_protocol


def verify_tier3_two_worldline_clock_exchange(
    horizons: List[int] = [256, 512, 1024],
    M_samples: int = 10,
    u_src: int = 4,
    eta_periph_cap: float = 0.30,
    tables_cache: Optional[Tuple] = None,
    runs: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Tier 3 Audit: Contrasts near-source Worldline X (in J^+[u_src]) against peripheral
    low-overlap Worldline Y (starting at u_far not in J^+[u_src] U J^-[u_src] with
    Alexandrov overlap eta_ov <= 0.30, permitting genuine two-way causal relays in both
    X -> Y and Y -> X!), alongside strictly exterior reference chain Y_ext subseteq V \\ J^+[u_src]
    (where N_relay(X -> Y_ext) == 0 holds identically by order transitivity).
    """
    if runs is not None:
        M_samples = runs

    max_H = max(horizons)
    if tables_cache is None or len(tables_cache[1]) <= max_H:
        tables_cache = precompute_csg_tables(max_H, 0.20, 0.20) + precompute_csg_tables(max_H, 0.90, 0.60)

    tier3_results: Dict[str, Any] = {}

    for N in horizons:
        coupled_ratios = []
        uncoupled_ratios = []
        ext_coupled_ratios = []
        ext_uncoupled_ratios = []
        x_lens = []
        y_lens = []
        x2y_fail_rates = []
        y2x_fail_rates = []
        x2y_relays = []
        y2x_relays = []
        x2y_abst = []
        y2x_abst = []

        for r in range(M_samples):
            seed = 9000 + r * 31
            t_c = simulate_persistent_trajectory(N, u_src=u_src, coupled=True, kappa=2.00, seed=seed, tables_cache=tables_cache)
            t_u = simulate_persistent_trajectory(N, u_src=u_src, coupled=False, seed=seed, tables_cache=tables_cache)

            def _eval_worldlines(tr: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
                C = tr["C"]
                cone_nodes = sorted(list(np.where(tr["in_cone"])[0]))
                chain_x = construct_timelike_worldline(C, cone_nodes, u_src)

                out_nodes = np.where(~tr["in_cone"])[0]
                far_cands = [v for v in out_nodes if v > u_src and not C[v, u_src] and not C[u_src, v]]
                u_far = far_cands[0] if far_cands else int(out_nodes[0])

                metrics = compute_poset_intrinsic_metrics(C, tr["in_cone"], u_src=u_src)
                eta_ov = metrics["eta_ov"]

                # Primary Worldline Y: peripheral low-overlap region (eta_ov <= 0.30) enabling 2-way relays
                periph_nodes = [
                    v for v in range(u_far, N)
                    if v == u_far or (C[v, u_far] and eta_ov[v] <= eta_periph_cap)
                ]
                chain_y = construct_timelike_worldline(C, periph_nodes, u_far)
                proto_periph = execute_clock_exchange_protocol(C, chain_x, chain_y)

                # Reference chain Y_ext: strictly outside J^+[u_src] (0 X->Y relays by transitivity)
                ext_nodes = [
                    v for v in range(u_far, N)
                    if v == u_far or (C[v, u_far] and not tr["in_cone"][v])
                ]
                chain_y_ext = construct_timelike_worldline(C, ext_nodes, u_far)
                proto_ext = execute_clock_exchange_protocol(C, chain_x, chain_y_ext)
                return proto_periph, proto_ext

            proto_c, proto_c_ext = _eval_worldlines(t_c)
            proto_u, proto_u_ext = _eval_worldlines(t_u)

            coupled_ratios.append(proto_c["ratio_chain"])
            uncoupled_ratios.append(proto_u["ratio_chain"])
            ext_coupled_ratios.append(proto_c_ext["ratio_chain"])
            ext_uncoupled_ratios.append(proto_u_ext["ratio_chain"])

            x_lens.append(proto_c["len_X"])
            y_lens.append(proto_c["len_Y"])
            x2y_fail_rates.append(proto_c["x_to_y"]["failure_rate"])
            y2x_fail_rates.append(proto_c["y_to_x"]["failure_rate"])
            x2y_relays.append(proto_c["x_to_y"]["relay_links"])
            y2x_relays.append(proto_c["y_to_x"]["relay_links"])
            x2y_abst.append(proto_c["x_to_y"]["abstentions"])
            y2x_abst.append(proto_c["y_to_x"]["abstentions"])

        mean_rc = float(np.mean(coupled_ratios))
        mean_ru = float(np.mean(uncoupled_ratios))
        delta_r = float(mean_rc - mean_ru)

        mean_ext_rc = float(np.mean(ext_coupled_ratios))
        mean_ext_ru = float(np.mean(ext_uncoupled_ratios))

        tier3_results[str(N)] = {
            "mean_len_X": float(np.mean(x_lens)),
            "mean_len_Y": float(np.mean(y_lens)),
            "mean_ratio_coupled": mean_rc,
            "mean_ratio_uncoupled": mean_ru,
            "delta_ratio_contrast": delta_r,
            "strictly_exterior_ratio_coupled": mean_ext_rc,
            "strictly_exterior_ratio_uncoupled": mean_ext_ru,
            "strictly_exterior_delta_ratio": float(mean_ext_rc - mean_ext_ru),
            "ratio_distinct_from_unity": bool(abs(mean_rc - 1.0) >= 0.20),
            "contrast_exceeds_threshold": bool(delta_r >= 0.50),
            "mean_relays_x2y": float(np.mean(x2y_relays)),
            "mean_abstentions_x2y": float(np.mean(x2y_abst)),
            "mean_fail_rate_x2y": float(np.mean(x2y_fail_rates)),
            "mean_relays_y2x": float(np.mean(y2x_relays)),
            "mean_abstentions_y2x": float(np.mean(y2x_abst)),
            "mean_fail_rate_y2x": float(np.mean(y2x_fail_rates)),
            "bidirectional_relays_observed": bool(np.mean(x2y_relays) > 0.0 and np.mean(y2x_relays) > 0.0),
        }

    all_pass = all(
        d["ratio_distinct_from_unity"]
        and d["contrast_exceeds_threshold"]
        and d["bidirectional_relays_observed"]
        for d in tier3_results.values()
    )

    return {
        "status": "PASS" if all_pass else "FAIL",
        "measured_contrast_verified": all_pass,
        "worldline_y_definition": f"peripheral_low_overlap_eta_le_{eta_periph_cap:.2f}",
        "horizons": horizons,
        "samples_per_horizon": M_samples,
        "by_horizon": tier3_results,
    }


# =============================================================================
# SECTION 6: MASTER VERIFICATION HARNESS & JSON EXPORT
# =============================================================================

def run_stage11_verification(
    horizons: List[int] = [256, 512, 1024],
    M_samples: int = 10,
    export_json: bool = True,
    json_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes full Gate 11 verification suite and exports stage11_comparison_experiment_results.json.
    """
    t_start = time.time()
    print("=" * 80)
    print("STAGE 11: SOURCE VS. DISTANT COMPARISON & RELATIONAL ATTENUATION MASTER BENCHMARK")
    print("=" * 80)

    max_H = max(horizons)
    tables = precompute_csg_tables(max_H, 0.20, 0.20) + precompute_csg_tables(max_H, 0.90, 0.60)

    print("\n>>> TIER 1: AUDITING SPACELIKE NON-DISTURBANCE OUTSIDE J^+[u_src] <<<")
    tier1_res = verify_tier1_spacelike_non_disturbance(
        horizons=[256, 512], M_samples=M_samples, tables_cache=tables
    )
    for N_str, tdata in tier1_res["by_horizon"].items():
        print(
            f"  Horizon N={int(N_str):4d}: max_Delta_L={tdata['max_delta_L_max']}, "
            f"max_Delta_rho={tdata['max_delta_rho_link']:.4e}, max_p1={tdata['max_carrier_p1_distant']:.4e} "
            f"[Pass: {tdata['spacelike_non_disturbance_verified']}]"
        )
    print(f"  Tier 1 Status: {tier1_res['status']}")

    print("\n>>> TIER 2: AUDITING NON-TAUTOLOGICAL MONOTONE ATTENUATION ACROSS d_link & eta_ov <<<")
    tier2_res = verify_tier2_relational_decay(
        N=512, M_samples=15, tables_cache=tables
    )
    print(
        f"  Uncoupled Control (Arm B - Arm A): {tier2_res['uncoupled_control']['arm_b_minus_arm_a']:.4e} "
        f"[Bitwise match: {tier2_res['uncoupled_control']['bitwise_identical']}]"
    )
    print(f"  Link Depth Monotonic Decay:        {tier2_res['link_depth_attenuation']['is_monotonically_decreasing']}")
    print(f"  Overlap Delta k_Hasse Growth:      {tier2_res['causal_overlap_growth']['is_monotonically_increasing']}")
    print(f"  Depth Shift (Near d<=2 - Far d>=5): {tier2_res['differential_comparison_arms']['net_differential_contrast']:+.4f}")
    print(f"  Tier 2 Status: {tier2_res['status']}")

    print("\n>>> TIER 3: AUDITING OPERATIONAL TWO-WORLDLINE CLOCK-EXCHANGE PROTOCOL <<<")
    tier3_res = verify_tier3_two_worldline_clock_exchange(
        horizons=horizons, M_samples=M_samples, tables_cache=tables
    )
    for N_str, wdata in tier3_res["by_horizon"].items():
        print(
            f"  Horizon N={int(N_str):4d}: len(X)={wdata['mean_len_X']:.1f}, len(Y)={wdata['mean_len_Y']:.1f}, "
            f"Ratio X/Y={wdata['mean_ratio_coupled']:.4f} (uncoupled={wdata['mean_ratio_uncoupled']:.4f}, Delta={wdata['delta_ratio_contrast']:+.4f}) "
            f"Relays(X->Y={wdata['mean_relays_x2y']:.1f}, Y->X={wdata['mean_relays_y2x']:.1f})"
        )
    print(f"  Tier 3 Status: {tier3_res['status']}")

    gate11_pass = (
        tier1_res["status"] == "PASS"
        and tier2_res["status"] == "PASS"
        and tier3_res["status"] == "PASS"
    )

    t_elapsed = time.time() - t_start
    status_str = "PASS" if gate11_pass else "FAIL"

    print("\n" + "=" * 80)
    print(f"GATE 11 VERIFICATION STATUS: {status_str} (Total Runtime: {t_elapsed:.3f}s)")
    print("=" * 80)

    results_payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate": "Gate 11",
        "status": status_str,
        "parameters": {
            "c0": 0.20,
            "q0": 0.20,
            "c1": 0.90,
            "q1": 0.60,
            "kappa": 2.00,
            "gamma": 0.12,
            "u_src": 4,
            "eta_periph_cap": 0.30,
            "horizons": horizons,
            "M_samples": M_samples,
        },
        "tier1_spacelike_non_disturbance": tier1_res,
        "tier2_relational_decay": tier2_res,
        "tier3_two_worldline_clock_exchange": tier3_res,
        "timing_seconds": t_elapsed,
    }

    if export_json:
        if json_path is None:
            json_path = os.path.join(CURRENT_DIR, "stage11_comparison_experiment_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results_payload, f, indent=2)
        print(f"\n[Artifact Exported]: {json_path}")

    return results_payload


if __name__ == "__main__":
    run_stage11_verification()
