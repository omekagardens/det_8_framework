#!/usr/bin/env python3
"""
run_cr1_verification.py

Master verification harness for Conjecture CR-1 (Cross-Regime Differentiated Coherence):
  - Stage 1: Unit & property test suite (17 tests, including Myrheim-Meyer normalization/inversion)
  - Stage 2: Exact finite-poset diamond commutation & QR-LD037 / local-compensation audit
  - Stage 3: Full discriminating experiment at N in {16, 32} (M = 50 runs x 14 models = 1,400 histories)
  - Stage 4: Extended multi-horizon scaling sweep N in {16, 32, 64, 128, 256, 512, 1024} (M = 25 runs)
  - Stage 4b: Multi-alpha nested-regime profile R_int(alpha) at N in {512, 1024} (alpha in {0.25..0.65})
"""

import os
import sys
import json
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from cr1_discriminating_experiment import (
    verify_exact_diamond_and_readout_properties,
    run_discriminating_experiment,
    run_extended_multi_horizon_scaling,
    run_multi_alpha_profile_experiment,
    export_results_to_json,
    print_formatted_summary_table,
)
import test_cr1_discriminating_experiment


def run_unit_tests():
    print("=" * 88)
    print("STAGE 1: RUNNING CR-1 UNIT & PROPERTY TEST SUITE")
    print("=" * 88)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_cr1_discriminating_experiment)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print("[FAIL] Unit test suite failed!")
        sys.exit(1)
    print("[PASS] All unit & property tests passed.\n")


def main():
    run_unit_tests()

    print("=" * 88)
    print("STAGE 2: EXACT DIAMOND COMMUTATION & QR-LD037 / COMPENSATION AUDIT (poset_generator)")
    print("=" * 88)
    diamond_audit = verify_exact_diamond_and_readout_properties()
    print(f"  Total diamonds audited (N <= 4):                 {diamond_audit['total_diamonds_n_le_4']}")
    print(f"  Gevrey CSG diamond violations:                   {diamond_audit['gevrey_diamond_violations']}")
    print(f"  Log-Quadratic CSG diamond violations:            {diamond_audit['log_quadratic_diamond_violations']}")
    print(f"  Intrinsic-past compensation proper violations:   {diamond_audit['intrinsic_compensation_proper_violations']}")
    print(f"  Stage-n-exponent damping violations (expected>0): {diamond_audit['stage_n_exponent_damping_violations']}")
    print(f"  Local-cone-routed max row-sum error:             {diamond_audit['local_cone_routed_max_row_err']:.2e}")
    print(f"  Local-cone-routed overlap diamond violations:    {diamond_audit['local_cone_routed_diamond_violations']}")
    print(f"  QR-LD037 4-birth diamond routes:                 Pi_1={diamond_audit['qr_ld037_pi1']:.6f} != Pi_2={diamond_audit['qr_ld037_pi2']:.6f}")
    assert diamond_audit["gevrey_diamond_violations"] == 0
    assert diamond_audit["log_quadratic_diamond_violations"] == 0
    assert diamond_audit["intrinsic_compensation_proper_violations"] == 0
    assert diamond_audit["stage_n_exponent_damping_violations"] > 0
    assert diamond_audit["local_cone_routed_max_row_err"] < 1e-14
    assert diamond_audit["local_cone_routed_diamond_violations"] > 0
    assert not diamond_audit["qr_ld037_diamond_commutes"]
    print("[PASS] Exact diamond & readout audit verified.\n")

    print("=" * 88)
    print("STAGE 3: SMALL-TO-MODERATE HORIZON SUITE (N=16, N=32, M=50 RUNS x 14 MODELS)")
    print("=" * 88)
    results = run_discriminating_experiment(horizons=[16, 32], num_runs=50, base_seed=1000)
    results["exact_diamond_audit"] = diamond_audit

    print("\n" + "=" * 88)
    print("STAGE 4: EXTENDED MULTI-HORIZON SCALING SWEEP (N=16..1024, M=25 RUNS)")
    print("=" * 88)
    scaling = run_extended_multi_horizon_scaling(
        horizons=(16, 32, 64, 128, 256, 512, 1024),
        num_runs=25,
        seed=20261115,
    )
    results["extended_scaling_n16_to_1024"] = scaling

    for mid, per_n in scaling.items():
        summary_parts = []
        for n_key in ("32", "128", "512", "1024"):
            if n_key in per_n:
                d = per_n[n_key]
                ir2 = f"{d['meso_int_r2_mean']:.3f}" if d.get("meso_int_r2_mean") is not None else "n/a"
                summary_parts.append(f"N={n_key}: R2={d['r2_mean']:.4f}+/-{d['r2_std']:.4f} (Int={ir2})")
        print(f"  [{mid:20s}] " + " | ".join(summary_parts))

    print("\n" + "=" * 88)
    print("STAGE 4B: MULTI-ALPHA NESTED-REGIME PROFILE R_int(alpha) (N=512, 1024; M=20 RUNS)")
    print("=" * 88)
    multi_alpha = run_multi_alpha_profile_experiment(
        horizons=(512, 1024),
        alphas=(0.25, 0.35, 0.45, 0.50, 0.65),
        c_minus=0.5,
        c_plus=1.5,
        delta_bulk=0.05,
        num_runs=20,
        max_intervals_per_alpha=100,
        seed=20261116,
    )
    results["multi_alpha_profile"] = multi_alpha
    for n_key in ("512", "1024"):
        print(f"  --- Horizon N = {n_key} ---")
        for mid, mdata in multi_alpha["horizons"][n_key].items():
            alpha_str = " | ".join(
                f"a={ak}: {av['r_int_mean']:.4f}+/-{av['r_int_std']:.4f} (d={av['d_mm_mean']:.2f}+/-{av['d_mm_std']:.2f}, <m>={av['mean_m_realized']:.1f})"
                for ak, av in mdata["alphas"].items()
            )
            print(
                f"  [{mid:20s}] Glob={mdata['global_r2_mean']:.4f}+/-{mdata['global_r2_std']:.4f} "
                f"(d={mdata['global_d_mm_mean']:.2f}+/-{mdata['global_d_mm_std']:.2f}) || {alpha_str}"
            )

    json_path = os.path.join(SCRIPT_DIR, "cr1_experiment_results.json")
    export_results_to_json(results, json_path)
    print_formatted_summary_table(results)

    print("\n" + "=" * 88)
    print("STAGE 5: ASSERTING ALL MATHEMATICAL & EMPIRICAL ACCEPTANCE GATES")
    print("=" * 88)
    h16 = results["horizons_data"]["16"]
    h32 = results["horizons_data"]["32"]

    # Gate 1: Positive geometric controls (non-vacuity + CR-1d vs SS-1 separation)
    assert 0.07 <= h32["minkowski_4d"]["r2_mean"] <= 0.13
    assert 0.45 <= h32["minkowski_2d"]["r2_mean"] <= 0.55
    assert h32["minkowski_4d"]["sub_interval_r2_mean"] < 0.25
    assert 0.15 <= h32["minkowski_2d_slab"]["r2_mean"] <= 0.27
    assert 0.40 <= h32["minkowski_2d_slab"]["sub_interval_r2_mean"] <= 0.60
    print("  [PASS] Gate 1: Geometric controls satisfy CR-1; 2D slab separates CR-1d from SS-1.")

    # Gate 2: Negative controls fail their exact targeted pillars
    assert h16["bimodal_mix_10_90"]["var_between_r2"] > 0.05
    assert h32["bimodal_mix_10_90"]["var_between_r2"] > 0.03
    assert h32["bimodal_mix_10_90"]["var_between_r2"] > 30.0 * h32["minkowski_4d"]["var_between_r2"]
    assert h32["kr_3layer"]["rho2_chain_ratio_mean"] == 0.0
    assert abs(h32["cutoff_kmax1"]["sub_interval_r2_mean"] - 1.0) < 1e-12
    assert h32["percolation_p008"]["r2_mean"] > h16["percolation_p008"]["r2_mean"]
    print("  [PASS] Gate 2: Bimodal mixture, 3-layer KR, k_max=1 forest, and fixed-p percolation verified.")

    # Gate 3: Gevrey upward drift beyond N=32 vs Log-Quadratic logarithmic window
    g15_32 = scaling["gevrey_c02_beta15"]["32"]["r2_mean"]
    g15_1024 = scaling["gevrey_c02_beta15"]["1024"]["r2_mean"]
    g20_32 = scaling["gevrey_c02_beta20"]["32"]["r2_mean"]
    g20_1024 = scaling["gevrey_c02_beta20"]["1024"]["r2_mean"]
    assert g15_1024 > g15_32 + 0.20, f"Expected Gevrey beta=1.5 upward drift: {g15_32} -> {g15_1024}"
    assert g20_1024 > g20_32 + 0.08, f"Expected Gevrey beta=2.0 upward drift: {g20_32} -> {g20_1024}"
    print(f"  [PASS] Gate 3: Gevrey upward drift verified (beta=1.5: {g15_32:.4f}->{g15_1024:.4f}; beta=2.0: {g20_32:.4f}->{g20_1024:.4f}).")

    # Gate 4: Log-Quadratic critical logarithmic window & spine interval contrast up to N=1024
    lq02_1024 = scaling["log_quad_c02_q020"]["1024"]
    lq50_1024 = scaling["log_quad_c10_q050"]["1024"]
    mink4_512 = scaling["minkowski_4d"]["512"]
    assert 0.08 <= lq02_1024["r2_mean"] <= 0.14
    assert lq02_1024["var_between_r2"] < 0.0002
    assert lq02_1024["link_deg_mean"] < lq02_1024["k_seed_mean"]
    assert 0.44 <= lq50_1024["r2_mean"] <= 0.52
    assert lq02_1024["meso_int_r2_mean"] > 0.35
    assert mink4_512["meso_int_r2_mean"] < 0.14
    assert (lq02_1024["meso_int_r2_mean"] - mink4_512["meso_int_r2_mean"]) > 0.25
    print(
        f"  [PASS] Gate 4: Log-Quadratic (0.2,0.2) holds global R_2(1024)={lq02_1024['r2_mean']:.4f} "
        f"(Var_b={lq02_1024['var_between_r2']:.6f}), while mesoscopic Sub-R2={lq02_1024['meso_int_r2_mean']:.4f} "
        f"vs 4D Minkowski={mink4_512['meso_int_r2_mean']:.4f}."
    )

    # Gate 5: Multi-alpha nested-regime profile R_int(alpha) (4D Minkowski flat vs Log-Quadratic scale-dependent)
    ma1024_mink = multi_alpha["horizons"]["1024"]["minkowski_4d"]["alphas"]
    ma1024_lq = multi_alpha["horizons"]["1024"]["log_quad_c02_q020"]["alphas"]
    ma512_lq = multi_alpha["horizons"]["512"]["log_quad_c02_q020"]["alphas"]
    for ak in ("0.25", "0.35", "0.45", "0.50", "0.65"):
        assert 0.07 <= ma1024_mink[ak]["r_int_mean"] <= 0.14, f"4D Minkowski alpha={ak} out of band"
    assert (
        ma1024_lq["0.25"]["r_int_mean"]
        > ma1024_lq["0.35"]["r_int_mean"]
        > ma1024_lq["0.45"]["r_int_mean"]
        > ma1024_lq["0.50"]["r_int_mean"]
        > ma1024_lq["0.65"]["r_int_mean"]
    ), "Expected monotonic scale decrease in Log-Quadratic R_int(alpha)"
    assert ma1024_lq["0.25"]["r_int_mean"] > 0.85
    assert ma1024_lq["0.65"]["r_int_mean"] < 0.32
    # Exact binary-scale cardinality collapse check: 512^0.50 == 1024^0.45 == 2^4.5 (m in [12, 33])
    assert abs(ma512_lq["0.50"]["r_int_mean"] - ma1024_lq["0.45"]["r_int_mean"]) < 0.05
    print(
        f"  [PASS] Gate 5: Multi-alpha profile verified at N=1024 "
        f"(4D Minkowski flat ~0.10; Log-Quad 0.25->0.65: "
        f"{ma1024_lq['0.25']['r_int_mean']:.4f} -> {ma1024_lq['0.65']['r_int_mean']:.4f}; "
        f"m~2^4.5 collapse: N=512@0.50={ma512_lq['0.50']['r_int_mean']:.4f} vs N=1024@0.45={ma1024_lq['0.45']['r_int_mean']:.4f})."
    )

    print("\n" + "=" * 88)
    print("ALL CR-1 VERIFICATION STAGES PASSED WITH EXIT CODE 0.")
    print("=" * 88)


if __name__ == "__main__":
    main()
