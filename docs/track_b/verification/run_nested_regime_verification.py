#!/usr/bin/env python3
"""
run_nested_regime_verification.py

Master deterministic verification harness for Stage 8:
  Nested-Regime Dynamics, Multi-Horizon Scale-Pattern Holdout, and Active
  Source-Perturbation Response on X = (C, Z).

Stages:
  1. Unit & Property Test Suite (18 tests in test_nested_regime_source_experiment.py)
  2. Pillar 1: Frozen Multi-Horizon & Multi-Observable Holdout Suite
     (N in {512, 1024, 2048} across 8 models + N = 4096 Log-Quadratic check +
     Proposition 1.1 Exact Future-Cone 1D Markov Chain audit)
  3. Pillar 2: Coarse Projection & Active Residual-to-Structure Coupling Audit
     (Theorem 2.1 omitted-chain & Z_geom Markov sufficiency; Theorem 2.2 N_act = 8, 12
     root-martingale active law across 3,644 diamonds; Theorem 2.3 all-horizon CPTP
     instrument & exact isomorphism-invariant non-mixture separation)
  4. Pillar 3: Paired 3-Arm Source-Perturbation, Clock-Tick & Recoil Experiment
     (n0 = 128 -> N in {512, 1024}, M = 40 paired histories)
  5. Deterministic JSON export & strict acceptance gates (exits 0 on full pass).
"""

import os
import sys
import time
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import test_nested_regime_source_experiment
from nested_regime_source_experiment import (
    run_pillar1_frozen_holdout_suite,
    verify_coarse_projection_theorems,
    verify_active_root_martingale_law,
    verify_two_mode_source_instrument_and_non_mixture,
    run_pillar3_paired_source_experiment,
    export_results_to_json,
)


def run_unit_tests():
    print("=" * 90)
    print("STAGE 1: RUNNING STAGE 8 UNIT & MATHEMATICAL PROPERTY TEST SUITE")
    print("=" * 90)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_nested_regime_source_experiment)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if not res.wasSuccessful():
        print("[FAIL] Unit test suite failed!")
        sys.exit(1)
    print(f"[PASS] All {res.testsRun} unit & property tests passed.\n")
    return res.testsRun


def main():
    t_wall_start = time.time()
    n_tests = run_unit_tests()

    print("=" * 90)
    print("STAGE 2: PILLAR 1 — FROZEN MULTI-HORIZON & MULTI-OBSERVABLE HOLDOUT SUITE")
    print("=" * 90)
    p1 = run_pillar1_frozen_holdout_suite(
        horizons=(512, 1024, 2048),
        runs_by_horizon={512: 8, 1024: 8, 2048: 6},
        n4096_runs=4,
        max_intervals_per_window=20,
        delta_bulk=0.05,
        base_seed=20260801,
    )
    for n_key in ("512", "1024", "2048"):
        print(f"  --- Horizon N = {n_key} ---")
        for mid, md in p1["horizons"][n_key].items():
            w12 = md["fixed_m_windows"]["12_24"]
            r2_str = f"{w12['r2_mean']:.4f}" if w12["r2_mean"] is not None else "n/a"
            ll_str = f"{w12['ell_link_mean']:.4f}" if w12["ell_link_mean"] is not None else "n/a"
            hm_str = f"{w12['h_over_m_mean']:.4f}" if w12["h_over_m_mean"] is not None else "n/a"
            rh_str = f"{w12['rho2_mean']:.4f}" if w12["rho2_mean"] is not None else "n/a"
            wm_str = f"{w12['wmin_over_m_mean']:.4f}" if w12["wmin_over_m_mean"] is not None else "n/a"
            print(
                f"  [{mid:20s}] GlobR2={md['global_r2_mean']:.4f}+/-{md['global_r2_std']:.4f} | "
                f"m[12,24]: R2={r2_str}, link={ll_str}, h/m={hm_str}, rho2={rh_str}, wmin/m={wm_str}"
            )
    n4k = p1["large_horizon_N4096_check"]
    w12_4k = n4k["fixed_m_windows"]["12_24"]
    print(
        f"  [log_quad_c02_q020 @ N=4096] GlobR2={n4k['global_r2_mean']:.4f}+/-{n4k['global_r2_std']:.4f} | "
        f"m[12,24]: R2={w12_4k['r2_mean']:.4f}, link={w12_4k['ell_link_mean']:.4f}, "
        f"h/m={w12_4k['h_over_m_mean']:.4f}, rho2={w12_4k['rho2_mean']:.4f}, wmin/m={w12_4k['wmin_over_m_mean']:.4f}"
    )
    print(f"  Disposition: {p1['decision_evaluation']['disposition']}\n")

    print("=" * 90)
    print("STAGE 3: PILLAR 2 — COARSE PROJECTION & ACTIVE RESIDUAL-TO-STRUCTURE AUDIT")
    print("=" * 90)
    p2_proj = verify_coarse_projection_theorems()
    p2_act = verify_active_root_martingale_law()
    p2_two = verify_two_mode_source_instrument_and_non_mixture()

    print(
        f"  Theorem 2.1 (Projection): {p2_proj['total_diamonds_n_le_4']} diamonds, "
        f"intrinsic violations={p2_proj['intrinsic_projection_diamond_violations']}, "
        f"Z_geom max discrepancy={p2_proj['max_zgeom_sufficiency_discrepancy']:.2e}, "
        f"coarse-only non-Markov gap={p2_proj['max_coarse_only_non_markov_gap']:.4f}"
    )
    for h_act in ("8", "12"):
        da = p2_act[h_act]
        print(
            f"  Theorem 2.2 (Active Root Martingale N_act={h_act}): min_entry={da['min_branch_matrix_entry']:.3e}, "
            f"diamond violations={da['diamond_violations_n_le_4']}/{da['total_diamonds_n_le_4']}, "
            f"Delta_update={da['step1_chain_delta_update']:.6e}"
        )
    print(
        f"  Theorem 2.3 (All-Horizon CPTP & Non-Mixture): CPTP err={p2_two['max_cptp_trace_err']:.2e}, "
        f"diamond violations={p2_two['operator_diamond_violations']}/{p2_two['total_diamonds_n_le_4']}"
    )
    for chk in p2_two["non_mixture_exact_enumeration_checks"]:
        print(
            f"    n0={chk['n0']}: Static-Mixture Ratio={chk['universal_static_mixture_ratio']:.4f} "
            f"(3-comp check={chk['arbitrary_3component_mixture_ratio']:.4f}) vs "
            f"Intervened Ratio={chk['intervened_UX_ratio']:.4f}"
        )
    print()

    print("=" * 90)
    print("STAGE 4: PILLAR 3 — PAIRED 3-ARM SOURCE-PERTURBATION & RECOIL EXPERIMENT")
    print("=" * 90)
    p3 = run_pillar3_paired_source_experiment(
        n0=128,
        horizons=(512, 1024),
        num_runs=40,
        p_anc=0.125,
        omega0=0.25,
        omega1=0.85,
        seed=20260803,
    )
    for h_key in ("512", "1024"):
        print(f"  --- Paired Readouts at Horizon N = {h_key} (from identical prefix n0 = 128, M = 40) ---")
        arms = p3["horizons"][h_key]["arms"]
        for an, ad in arms.items():
            print(
                f"  [{an:21s}] L_max={ad['src_l_max_ticks_mean']:.2f}+/-{ad['src_l_max_ticks_std']:.2f} | "
                f"|J+|={ad['src_cone_volume_mean']:.1f} | "
                f"R2_anc={ad['coarse_anchor_r2_mean']:.4f} | "
                f"p1={ad['residual_p1_excited_mean']:.4f} (Var={ad['residual_p1_var_between']:.4f}) | "
                f"|<0|Z|1>|={ad['residual_coherence_abs_mean']:.4f}"
            )
        ct = p3["horizons"][h_key]["paired_contrasts"]
        print(
            f"    Paired (B_p10 - A): L_max diff={ct['B_p10_minus_A']['src_l_max_ticks']['mean']:.4f} | "
            f"Paired (C_p10 - A): L_max diff=+{ct['C_p10_minus_A']['src_l_max_ticks']['mean']:.2f} "
            f"(t={ct['C_p10_minus_A']['src_l_max_ticks']['t_stat']:.2f}), "
            f"R2_anc diff=+{ct['C_p10_minus_A']['coarse_anchor_r2']['mean']:.4f} "
            f"(t={ct['C_p10_minus_A']['coarse_anchor_r2']['t_stat']:.2f})"
        )

    total_elapsed = time.time() - t_wall_start
    full_results = {
        "metadata": {
            "stage": "Stage 8: Nested-Regime Dynamics & Source-Perturbation Response",
            "unit_tests_passed": n_tests,
            "total_wall_seconds": round(total_elapsed, 3),
        },
        "pillar1_holdout": p1,
        "pillar2_coarse_projection": p2_proj,
        "pillar2_active_root_martingale": p2_act,
        "pillar2_two_mode_non_mixture": p2_two,
        "pillar3_source_response": p3,
    }
    json_path = os.path.join(SCRIPT_DIR, "nested_regime_experiment_results.json")
    export_results_to_json(full_results, json_path)

    print("\n" + "=" * 90)
    print("STAGE 5: ASSERTING ALL MATHEMATICAL & EMPIRICAL ACCEPTANCE GATES")
    print("=" * 90)

    # Gate 1: Pillar 1 holdout scale crossover, logarithmic drift diagnosis, & honest retirement
    lq_512 = p1["horizons"]["512"]["log_quad_c02_q020"]
    lq_1024 = p1["horizons"]["1024"]["log_quad_c02_q020"]
    lq_2048 = p1["horizons"]["2048"]["log_quad_c02_q020"]
    m4_512 = p1["horizons"]["512"]["minkowski_4d"]
    m4_2048 = p1["horizons"]["2048"]["minkowski_4d"]

    # Monotonic m-scale decrease at N = 2048 across fixed-cardinality windows
    assert (
        lq_2048["fixed_m_windows"]["6_11"]["r2_mean"]
        > lq_2048["fixed_m_windows"]["12_24"]["r2_mean"]
        > lq_2048["fixed_m_windows"]["25_48"]["r2_mean"]
        > lq_2048["fixed_m_windows"]["49_96"]["r2_mean"]
    )
    # Exact Future-Cone Markov monotonic global E[R_2] drift & fixed-m logarithmic upward drift
    fc_tbl = p1["future_cone_markov_proposition"]["exact_horizon_table"]
    assert (
        fc_tbl["512"]["q020_exact_expected_r2"]
        < fc_tbl["1024"]["q020_exact_expected_r2"]
        < fc_tbl["2048"]["q020_exact_expected_r2"]
        < fc_tbl["4096"]["q020_exact_expected_r2"]
    )
    assert (
        lq_512["fixed_m_windows"]["6_11"]["r2_mean"]
        < lq_1024["fixed_m_windows"]["6_11"]["r2_mean"]
        < lq_2048["fixed_m_windows"]["6_11"]["r2_mean"]
    )
    assert lq_2048["fixed_m_windows"]["6_11"]["r2_mean"] > lq_512["fixed_m_windows"]["6_11"]["r2_mean"] + 0.040
    assert n4k["fixed_m_windows"]["6_11"]["r2_mean"] > lq_512["fixed_m_windows"]["6_11"]["r2_mean"] + 0.040
    assert lq_2048["fixed_m_windows"]["12_24"]["rho2_mean"] > lq_512["fixed_m_windows"]["12_24"]["rho2_mean"] + 0.03
    assert n4k["fixed_m_windows"]["12_24"]["rho2_mean"] > lq_512["fixed_m_windows"]["12_24"]["rho2_mean"] + 0.08
    assert n4k["global_r2_mean"] > lq_512["global_r2_mean"] + 0.004
    # 4D Minkowski stationarity & wide minimal-layer hypersurface separation
    m4_1024 = p1["horizons"]["1024"]["minkowski_4d"]
    assert abs(m4_2048["fixed_m_windows"]["12_24"]["r2_mean"] - m4_1024["fixed_m_windows"]["12_24"]["r2_mean"]) < 0.02
    assert 0.09 <= m4_2048["global_r2_mean"] <= 0.11
    assert m4_2048["fixed_m_windows"]["12_24"]["wmin_over_m_mean"] > 0.60
    assert lq_2048["fixed_m_windows"]["12_24"]["wmin_over_m_mean"] < 0.20
    assert p1["decision_evaluation"]["passes_m_scale_crossover"] is True
    assert p1["decision_evaluation"]["passes_strict_fixed_m_stationarity"] is False
    assert p1["decision_evaluation"]["passes_4d_transverse_entry_width"] is False
    assert (
        p1["decision_evaluation"]["disposition"]
        == "RETIRE_STATIC_SCALAR_STANDALONE_GEOMETRY_RETAIN_AS_BASELINE_KERNEL"
    )
    print("  [PASS] Gate 1: Pillar 1 multi-observable holdout, Future-Cone drift, and honest retirement verified.")

    # Gate 2: Pillar 2 exact coarse projection & omitted-chain memory theorem
    assert p2_proj["intrinsic_projection_diamond_violations"] == 0
    assert p2_proj["stage_parity_projection_diamond_violations"] > 0
    assert p2_proj["omitted_chain_max_formula_err"] < 1e-14
    assert p2_proj["max_zgeom_sufficiency_discrepancy"] < 1e-14
    assert p2_proj["max_coarse_only_non_markov_gap"] > 0.05
    print("  [PASS] Gate 2: Theorem 2.1 coarse projection diamonds, non-Markovianity, and Z_geom sufficiency verified.")

    # Gate 3: Pillar 2 active residual laws (3,644 diamonds, N_act = 8 & 12, non-mixture separation)
    for hk in ("8", "12"):
        assert p2_act[hk]["min_branch_matrix_entry"] > 0.0
        assert p2_act[hk]["diamond_violations_n_le_4"] == 0
        assert p2_act[hk]["high_n_sampled_diamond_violations"] == 0
        assert p2_act[hk]["max_row_normalization_err"] < 1e-14
        assert abs(p2_act[hk]["step1_chain_delta_update"]) > 0.0
        assert p2_act[hk]["static_seed_control_delta_update"] == 0.0
        assert p2_act[hk]["forward_only_control_delta_update"] == 0.0
    assert p2_two["operator_diamond_violations"] == 0
    assert p2_two["max_cptp_trace_err"] < 1e-14
    for chk in p2_two["non_mixture_exact_enumeration_checks"]:
        assert abs(chk["arbitrary_3component_mixture_ratio"] - chk["universal_static_mixture_ratio"]) < 1e-13
        assert chk["non_mixture_discrepancy"] > 0.9
    print("  [PASS] Gate 3: Theorems 2.2 & 2.3 active residual laws (3,644 diamonds) and non-mixture separation verified.")

    # Gate 4: Pillar 3 paired 3-arm source response & two-way recoil accounting
    for hk in ("512", "1024"):
        ct = p3["horizons"][hk]["paired_contrasts"]
        arms = p3["horizons"][hk]["arms"]
        # Exact zero structural shift under uncoupled forward-only control Arm B
        assert ct["B_p10_minus_A"]["src_l_max_ticks"]["mean"] == 0.0
        assert ct["B_p10_minus_A"]["src_cone_volume"]["mean"] == 0.0
        assert ct["B_p10_minus_A"]["coarse_anchor_r2"]["mean"] == 0.0
        assert ct["B_p05_minus_A"]["src_l_max_ticks"]["mean"] == 0.0
        # Strong (> 6.5-sigma at N=512, > 10-sigma at N=1024) positive coupled response in Arm C_p10
        min_lmax_t = 6.5 if hk == "512" else 10.0
        min_cone_t = 8.0 if hk == "512" else 10.0
        assert ct["C_p10_minus_A"]["src_l_max_ticks"]["t_stat"] > min_lmax_t
        assert ct["C_p10_minus_A"]["src_cone_volume"]["t_stat"] > min_cone_t
        assert ct["C_p10_minus_A"]["coarse_anchor_r2"]["t_stat"] > 20.0
        assert abs(ct["C_p10_minus_A"]["matched_m12_24_r2"]["t_stat"]) > 4.0
        # Coherent p_exc = 0.5 positive shift + two-way Bayesian recoil & single-history decoherence
        assert ct["C_p05_minus_A"]["src_cone_volume"]["t_stat"] > 3.0
        assert ct["C_p05_minus_A"]["coarse_anchor_r2"]["t_stat"] > 4.0
        assert abs(arms["arm_B_uncoupled_p05"]["residual_coherence_abs_mean"] - 0.5) < 1e-12
        assert arms["arm_C_coherent_p05"]["residual_coherence_abs_mean"] < 1e-3
        assert arms["arm_C_coherent_p05"]["residual_p1_var_between"] > 0.15
    print("  [PASS] Gate 4: Pillar 3 paired 3-arm clock/focusing >10-sigma shift and Bayesian recoil verified.")

    print("\n" + "=" * 90)
    print(f"ALL STAGE 8 VERIFICATION GATES PASSED IN {total_elapsed:.2f}s WITH EXIT CODE 0.")
    print("=" * 90)


if __name__ == "__main__":
    main()
