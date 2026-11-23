"""Tier 5 white-box adversarial coverage and edge-case regression tests (M1–M4)."""

from __future__ import annotations

import contextlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from det8.models import det8_core
from det8.models import det_falsification
from det8.models import det_units
from det8.models import galaxy_observables as go
from det8.models import kappa_gravity_revival as kgr
from det8.models import kappa_t1_contraction as kt1
from det8.models import legacy_gravity_quarantine as lgq
from det8.models import pi_conformal_bridge as p2

REPO_ROOT: Path = Path(__file__).resolve().parents[2]


def _reject_nonfinite_json_constant(token: str) -> object:
    raise ValueError(f"Non-standard JSON constant {token!r} is forbidden")


class TestTier5ObservablesAndPathway1Hardening(unittest.TestCase):
    """Challenger 1 (M1 + M2) Tier 5 adversarial coverage & bug regressions."""

    def test_t5_screening_rho_crit_underflow_zero_division_boundary(self) -> None:
        underflow_cases = (
            {"sigma_crit": 1e-300, "scale_height_kpc": 1e300},
            {"sigma_crit": 1e-300, "scale_height_kpc": 1e50},
            {"sigma_crit": 1e-290, "scale_height_kpc": 1.0, "thickness_factor": 1e50},
        )
        for kwargs in underflow_cases:
            with self.subTest(underflow=kwargs):
                with self.assertRaises(ValueError):
                    kt1.sigma_crit_to_rho_crit(**kwargs)
                with self.assertRaises(ValueError):
                    kt1.evaluate_screening_constraints(**kwargs)

        with self.assertRaises(ValueError):
            kt1.evaluate_pathway1_criteria(sigma_crit=1e-300, scale_height_kpc=1e300)

        # Overflow of rho_crit -> inf is also rejected cleanly before JSON serialization
        with self.assertRaises(ValueError):
            kt1.sigma_crit_to_rho_crit(sigma_crit=1e300, scale_height_kpc=1e-300)
        with self.assertRaises(ValueError):
            kt1.evaluate_screening_constraints(sigma_crit=1e300, scale_height_kpc=1e-300)

        # Near-extreme valid regime still produces finite, JSON-serializable outputs
        scr = kt1.evaluate_screening_constraints(sigma_crit=1e-20, scale_height_kpc=1.0)
        encoded = json.dumps(scr, allow_nan=False)
        self.assertTrue(math.isfinite(float(scr["rho_crit_kg_m3"])))
        self.assertGreater(len(encoded), 0)

    def test_t5_sparc_diagnostic_huge_json_integers_no_overflow(self) -> None:
        huge_pos = 2**1024
        huge_neg = -(2**1024)
        payload = [
            {
                "name": "NGC 2403",
                "M_star": huge_pos,
                "r_d": 1.4,
                "M_gas": huge_pos,
                "V_flat": huge_pos,
            },
            {
                "name": "DDO 154",
                "M_star": huge_neg,
                "r_d": 0.37,
                "M_gas": huge_neg,
                "V_flat": huge_neg,
            },
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "huge_ints.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            report = go.load_sparc_subset_diagnostic(path)

        self.assertTrue(report["parsed_ok"])
        self.assertEqual(report["record_count"], 2)
        anomalies = report["anomalies"]
        self.assertEqual(anomalies["m_gas_equals_m_star_count"], 0)
        self.assertEqual(anomalies["zero_v_flat_count"], 0)
        self.assertEqual(anomalies["positive_v_flat_count"], 0)
        for ov in report["cross_comparison"]["vs_sample_galaxies"]["overlaps"]:
            self.assertIsNone(ov["M_star_ratio"])
        for ov in report["cross_comparison"]["vs_known_galaxies"]["overlaps"]:
            self.assertIsNone(ov["M_star_ratio"])

        # Huge ints in geometry/contraction helpers raise ValueError (not OverflowError)
        for huge in (huge_pos, huge_neg):
            with self.subTest(huge=huge):
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(1.0, huge, 1.0)
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(huge, 1.0, 1.0)
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, huge, 1.0)

        # Non-numeric types raise TypeError
        with self.assertRaises(TypeError):
            go.stellar_surface_density("1.0", 10.0, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            go.newton_rotation_velocity(None, 10.0, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            kt1.t1_contraction_kappa("1.0", 1.0, 1.0)  # type: ignore[arg-type]

    def test_t5_known_galaxies_comparison_empty_overlap_and_empty_known(self) -> None:
        orig_sample = kt1.SAMPLE_GALAXIES
        orig_known = kt1.KNOWN_GALAXIES
        try:
            kt1.SAMPLE_GALAXIES = []
            res_no_overlap = kt1._evaluate_known_galaxies_comparison(0.008, 0.93, "1d")
            self.assertEqual(res_no_overlap["n_galaxies"], len(orig_known))
            self.assertEqual(res_no_overlap["at_matched_sample_rmax"]["count"], 0)
            self.assertEqual(res_no_overlap["at_matched_sample_rmax"]["mean_error"], 0.0)
            self.assertIsNone(res_no_overlap["max_sample_over_known_M_star_ratio"])
            self.assertTrue(math.isfinite(float(res_no_overlap["at_max_5rd_8kpc"]["mean_error"])))
            self.assertIn("no shared galaxy names", str(res_no_overlap["discrepancy_note"]))

            kt1.SAMPLE_GALAXIES = orig_sample
            kt1.KNOWN_GALAXIES = []
            res_no_known = kt1._evaluate_known_galaxies_comparison(0.008, 0.93, "1d")
            self.assertEqual(res_no_known["n_galaxies"], 0)
            self.assertEqual(res_no_known["at_max_5rd_8kpc"]["mean_error"], 0.0)
            self.assertEqual(res_no_known["at_matched_sample_rmax"]["mean_error"], 0.0)
            self.assertIsNone(res_no_known["max_sample_over_known_M_star_ratio"])
        finally:
            kt1.SAMPLE_GALAXIES = orig_sample
            kt1.KNOWN_GALAXIES = orig_known

    def test_t5_radial_asymptotics_extreme_multipliers_and_short_disk_branch(self) -> None:
        with self.assertRaises(ValueError):
            kt1.evaluate_radial_asymptotics(r_multipliers=(1e290,))
        with self.assertRaises(ValueError):
            kt1.evaluate_radial_asymptotics(r_multipliers=(1e-170,), gas_mode="freeman_2d")
        res_tiny_1d = kt1.evaluate_radial_asymptotics(r_multipliers=(1e-170,), gas_mode="1d")
        self.assertEqual(res_tiny_1d["n_galaxies"], 43)
        self.assertTrue(math.isfinite(float(res_tiny_1d["summary"]["max_multiplier_mean_slope"])))

        orig_sample = kt1.SAMPLE_GALAXIES
        try:
            kt1.SAMPLE_GALAXIES = [
                go.GalaxyParams("ShortDisk", 1.0, 2.0, 0.5, 3.0, 100.0, 4.0)
            ]
            short_res = kt1.evaluate_radial_asymptotics(
                r_multipliers=[1.0], gas_mode="freeman_2d"
            )
            self.assertEqual(short_res["n_galaxies"], 1)
            gal_out = short_res["galaxies"][0]
            self.assertEqual(gal_out["slope_4rd_to_rmax"], gal_out["slope_at_r_max"])
        finally:
            kt1.SAMPLE_GALAXIES = orig_sample

        for bad_mults in ("123", [1.0, 1.0], (True,)):
            with self.subTest(bad_mults=bad_mults):
                with self.assertRaises(ValueError):
                    kt1.evaluate_radial_asymptotics(r_multipliers=bad_mults)  # type: ignore[arg-type]

    def test_t5_observables_v_sq_overflow_and_tiny_x_gas_precision(self) -> None:
        with self.assertRaisesRegex(ValueError, "Non-finite or negative squared velocity"):
            go.newton_rotation_velocity(1.0, 1e280, 1.0)

        tiny_gas = go.gas_mass_exponential_1d(1e-20, 5.0, 1.0)
        self.assertTrue(math.isclose(tiny_gas, 5e-20, rel_tol=1e-12, abs_tol=0.0))

        sub_threshold_gas = go.gas_mass_exponential_1d(1e-10, 5.0, 1.0)
        self.assertTrue(
            math.isclose(sub_threshold_gas, -5.0 * math.expm1(-1e-10), rel_tol=1e-14, abs_tol=0.0)
        )

        # Commented empty array aligns with standard "[]" (parsed_ok=True, record_count=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_arr = Path(tmpdir) / "commented_empty.json"
            empty_arr.write_text("[\n]\n# only brackets\n", encoding="utf-8")
            rep = go.load_sparc_subset_diagnostic(empty_arr)
            self.assertTrue(rep["parsed_ok"])
            self.assertEqual(rep["parse_mode"], "comment_stripped_wrapped_array")
            self.assertEqual(rep["record_count"], 0)
            self.assertEqual(rep["parse_errors"], [])

    def test_t5_sparc_diagnostic_all_recovery_and_anomaly_branches(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            # Missing both v_flat and V_flat
            no_vflat = root / "no_vflat.json"
            no_vflat.write_text(
                json.dumps([{"name": "A", "M_star": 1.0, "r_d": 1.0, "M_gas": 0.5}]),
                encoding="utf-8",
            )
            rep_nv = go.load_sparc_subset_diagnostic(no_vflat)
            self.assertIn("v_flat", rep_nv["anomalies"]["missing_galaxy_params_fields"])
            self.assertIn("V_flat", rep_nv["anomalies"]["missing_galaxy_observables_fields"])

            # Trailing comma in comment_stripped_wrapped_array
            trail = root / "trailing_comma.json"
            trail.write_text(
                '# comment\n{"name": "A", "M_star": 1.0, "V_flat": 50.0},\n',
                encoding="utf-8",
            )
            rep_tr = go.load_sparc_subset_diagnostic(trail)
            self.assertTrue(rep_tr["parsed_ok"])
            self.assertEqual(rep_tr["parse_mode"], "comment_stripped_wrapped_array")
            self.assertEqual(rep_tr["record_count"], 1)

            # Outer [ and ] present alongside # comment -> missing_outer_brackets=False
            bracketed = root / "bracketed_comment.json"
            bracketed.write_text(
                '# comment\n[{"name": "A", "M_star": 1.0, "V_flat": 50.0}]\n',
                encoding="utf-8",
            )
            rep_br = go.load_sparc_subset_diagnostic(bracketed)
            self.assertTrue(rep_br["parsed_ok"])
            self.assertFalse(rep_br["missing_outer_brackets"])
            self.assertEqual(rep_br["parse_mode"], "comment_stripped_wrapped_array")

            # Valid JSON non-object array falls back to line_recovery
            non_obj = root / "non_obj.json"
            non_obj.write_text("[1, 2, 3]\n", encoding="utf-8")
            rep_no = go.load_sparc_subset_diagnostic(non_obj)
            self.assertFalse(rep_no["parsed_ok"])
            self.assertEqual(rep_no["parse_mode"], "line_recovery")

            # Complex line_recovery: [ / ] lines, consecutive {, missing {, missing }, dangling {
            complex_bad = root / "complex_recovery.json"
            complex_bad.write_text(
                "\n".join(
                    [
                        "[",
                        "{",
                        "{",
                        '"name": "B", "M_star": 1.0, "V_flat": 80.0',
                        '"name": "C", "M_star": 2.0, "V_flat": 90.0}',
                        "]",
                        "{",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rep_cx = go.load_sparc_subset_diagnostic(complex_bad)
            self.assertFalse(rep_cx["parsed_ok"])
            self.assertEqual(rep_cx["parse_mode"], "line_recovery")
            self.assertEqual(rep_cx["record_count"], 2)
            err_msgs = [str(e["error"]) for e in rep_cx["parse_errors"]]
            self.assertTrue(any("Unmatched lone '{'" in m for m in err_msgs))
            self.assertTrue(any("Dangling lone '{'" in m for m in err_msgs))

            # PermissionError / io_error branch (when not running as root)
            if os.geteuid() != 0:
                unreadable = root / "unreadable.json"
                unreadable.write_text("[]", encoding="utf-8")
                os.chmod(unreadable, 0o000)
                try:
                    rep_io = go.load_sparc_subset_diagnostic(unreadable)
                    self.assertFalse(rep_io["parsed_ok"])
                    self.assertEqual(rep_io["parse_mode"], "io_error")
                finally:
                    os.chmod(unreadable, 0o644)

    def test_t5_kappa_t1_unhit_guards_median_and_freeman_2d_modes(self) -> None:
        with self.assertRaises(ValueError):
            kt1._median([])
        self.assertEqual(kt1._median([1.0, 3.0, 2.0, 4.0]), 2.5)

        with self.assertRaises(TypeError):
            kt1.evaluate_f6_sign_check(n_points="2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            kt1.evaluate_f6_sign_check(n_points=2.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            kt1.evaluate_f6_sign_check(r_core_kpc=5.0, r_out_kpc=5.0)
        f6_min = kt1.evaluate_f6_sign_check(r_core_kpc=0.0, n_points=2)
        self.assertEqual(f6_min["n_points"], 2)
        self.assertTrue(f6_min["all_increasing"])

        with self.assertRaises(TypeError):
            kt1.evaluate_pathway1_criteria(has_covariant_lensing_action=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            kt1.evaluate_pathway1_criteria(has_full_radial_sparc_profiles="no")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            kt1.evaluate_pathway1_criteria(scale_height_kpc=0.0)

        p1_2d = kt1.evaluate_pathway1_criteria(
            gas_mode="freeman_2d", w_sfr=0.5, scale_height_kpc=0.2
        )
        self.assertEqual(p1_2d["status"], "PARTIAL_LIMITATION")
        self.assertEqual(p1_2d["parameters"]["gas_mode"], "freeman_2d")

        sparc_2d = kt1.evaluate_sparc_fit(gas_mode="freeman_2d")
        self.assertEqual(
            sparc_2d["mean_error"],
            sparc_2d["freeman_2d_comparison"]["freeman_2d"]["mean_error"],
        )

        for bad_scr_kw in (
            {"fl1_delta_kappa_proxy": 0.0},
            {"fl1_delta_kappa_clock": 0.0},
            {"fl1_delta_kappa_proxy": 1.01},
            {"scale_height_kpc": 0.0},
            {"thickness_factor": 0.0},
            {"solar_wind_1au_kg_m3": 0.0},
            {"lab_density_kg_m3": 0.0},
        ):
            with self.subTest(bad_scr_kw=bad_scr_kw):
                with self.assertRaises(ValueError):
                    kt1.evaluate_screening_constraints(**bad_scr_kw)  # type: ignore[arg-type]

        scr_edge = kt1.evaluate_screening_constraints(
            beta=0.0, fl1_delta_kappa_proxy=1.0, fl1_delta_kappa_clock=1.0
        )
        self.assertEqual(
            scr_edge["fl1_rank_separation"]["conflated_scalar_delta_G_over_G_proxy"],
            0.0,
        )
        self.assertEqual(
            scr_edge["differential_eotvos"]["microscope_ti_pt"]["exponential"]["eta"],
            0.0,
        )

    def test_t5_sigma_crit_to_rho_crit_intermediate_scaling_and_screening_inf_guards(self) -> None:
        unit_scale = (1e9 * go.M_SUN_KG) / (go.KPC_TO_M ** 3)
        resilient_cases = (
            ((1e270, 1.0), {}, 1e270 * unit_scale),
            ((1e270, 1e270), {}, unit_scale),
            ((1e300, 1e290), {}, 1e10 * unit_scale),
            ((1e200, 1e200), {"thickness_factor": 1e200}, 1e-200 * unit_scale),
            ((1e-290, 1.0), {}, 1e-290 * unit_scale),
        )
        for args, kwargs, expected in resilient_cases:
            with self.subTest(args=args, kwargs=kwargs):
                val = kt1.sigma_crit_to_rho_crit(*args, **kwargs)
                self.assertTrue(math.isfinite(val))
                self.assertGreater(val, 0.0)
                self.assertTrue(math.isclose(val, expected, rel_tol=1e-12, abs_tol=0.0))

        # Exact default parity preserved
        self.assertEqual(
            kt1.sigma_crit_to_rho_crit(0.008, 0.3, thickness_factor=1.0),
            1.804744596618292e-21,
        )

        # True overflow and underflow still raise ValueError
        for bad_args in ((1e300, 1e-300), (1e-300, 1e300)):
            with self.subTest(bad_args=bad_args):
                with self.assertRaises(ValueError):
                    kt1.sigma_crit_to_rho_crit(*bad_args)

        # Screening inf / -inf ratio and log10_kappa guards
        for bad_scr in (
            {"sigma_crit": 1e-290, "scale_height_kpc": 1.0},
            {"lab_density_kg_m3": 1e300},
            {"solar_wind_1au_kg_m3": 1e300},
        ):
            with self.subTest(bad_scr=bad_scr):
                with self.assertRaises(ValueError):
                    kt1.evaluate_screening_constraints(**bad_scr)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            kt1.evaluate_pathway1_criteria(sigma_crit=1e-290, scale_height_kpc=1.0)
        with self.assertRaises(ValueError):
            kt1._eval_screening_law(1e300, 1e-20, 0.93, 1e-5)
        with self.assertRaises(ValueError):
            kt1._eval_differential_eotvos(1e300, 1.0, 1e-20, 0.93, 1e-15)

        # Valid extreme finite runs remain strictly JSON-serializable with allow_nan=False
        scr_tiny = kt1.evaluate_screening_constraints(sigma_crit=1e-280, scale_height_kpc=1.0)
        self.assertGreater(len(json.dumps(scr_tiny, allow_nan=False)), 0)
        scr_balanced = kt1.evaluate_screening_constraints(
            sigma_crit=1e270, scale_height_kpc=1e270
        )
        self.assertGreater(len(json.dumps(scr_balanced, allow_nan=False)), 0)
        crit_balanced = kt1.evaluate_pathway1_criteria(
            sigma_crit=1e270, scale_height_kpc=1e270
        )
        self.assertGreater(len(json.dumps(crit_balanced, allow_nan=False)), 0)

    def test_t5_chord_log_slope_degenerate_velocity_and_observables_r2_coverage(self) -> None:
        # _chord_log_slope degenerate velocity ValueError guard
        orig_sample = kt1.SAMPLE_GALAXIES
        try:
            kt1.SAMPLE_GALAXIES = [
                go.GalaxyParams("ChordEdge", 1.0, 1.0, 0.5, 1.0, 100.0, 5e288)
            ]
            with self.assertRaisesRegex(ValueError, "on chord"):
                kt1.evaluate_radial_asymptotics(r_multipliers=(1.0,))
        finally:
            kt1.SAMPLE_GALAXIES = orig_sample

        # gas_mass_exponential_1d continuity across x = 1e-4
        m_gas, r_gas = 5.0, 2.0
        g_left = go.gas_mass_exponential_1d(math.nextafter(1e-4, 0.0) * r_gas, m_gas, r_gas)
        g_at = go.gas_mass_exponential_1d(1e-4 * r_gas, m_gas, r_gas)
        g_right = go.gas_mass_exponential_1d(math.nextafter(1e-4, 1.0) * r_gas, m_gas, r_gas)
        self.assertLessEqual(g_left, g_at)
        self.assertLessEqual(g_at, g_right)
        self.assertLess(abs(g_at - g_left), 1e-16)
        self.assertLess(abs(g_right - g_at), 1e-16)
        self.assertLess(abs(g_at - g_left) / g_at, 1e-11)

        # galaxy_observables bool guards
        for bad_bool in (True, False):
            with self.subTest(bad_bool=bad_bool):
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(bad_bool, 10.0, 2.0)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(1.0, bad_bool, 2.0)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(bad_bool, 10.0, 2.0)  # type: ignore[arg-type]

        # Comma-less NDJSON line_recovery & tiny M_star=1e-320 JSON allow_nan=False safety
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            ndjson_path = root / "commaless.ndjson"
            ndjson_path.write_text(
                '{"name": "NGC 2403", "M_star": 3.2, "r_d": 1.4, "M_gas": 2.5, "V_flat": 131.0}\n'
                '{"name": "DDO 154", "M_star": 0.28, "r_d": 0.37, "M_gas": 0.25, "V_flat": 47.0}\n',
                encoding="utf-8",
            )
            rep_nd = go.load_sparc_subset_diagnostic(ndjson_path)
            self.assertTrue(rep_nd["parsed_ok"])
            self.assertEqual(rep_nd["parse_mode"], "line_recovery")
            self.assertEqual(rep_nd["parse_errors"], [])
            self.assertEqual(rep_nd["record_count"], 2)
            self.assertGreater(len(json.dumps(rep_nd, allow_nan=False)), 0)

            tiny_path = root / "tiny_mstar.json"
            tiny_path.write_text(
                json.dumps(
                    [
                        {"name": "NGC 2403", "M_star": 1e-320, "r_d": 1.4, "M_gas": 2.5, "V_flat": 131.0},
                        {"name": "DDO 154", "M_star": 1e-320, "r_d": 0.37, "M_gas": 0.25, "V_flat": 47.0},
                    ]
                ),
                encoding="utf-8",
            )
            rep_tiny = go.load_sparc_subset_diagnostic(tiny_path)
            self.assertTrue(rep_tiny["parsed_ok"])
            for ov in rep_tiny["cross_comparison"]["vs_sample_galaxies"]["overlaps"]:
                self.assertIsNone(ov["M_star_ratio"])
            for ov in rep_tiny["cross_comparison"]["vs_known_galaxies"]["overlaps"]:
                self.assertIsNone(ov["M_star_ratio"])
            self.assertGreater(len(json.dumps(rep_tiny, allow_nan=False)), 0)


class TestTier5Pathway2BridgeHardening(unittest.TestCase):
    """Challenger 2 (M3) Tier 5 Pathway 2 boundary & bug regressions."""

    def test_proper_time_step_domain_boundaries_and_overflow_behavior(self) -> None:
        self.assertEqual(p2.proper_time_step(0.5, delta_n=0.0), 0.0)
        self.assertEqual(p2.proper_time_step(0.5, delta_n=1.0, eta=0.0), 0.0)
        with self.assertRaises(ValueError):
            p2.proper_time_step(0.5, delta_n=-1e-9)
        with self.assertRaises(ValueError):
            p2.proper_time_step(0.0, delta_n=1e308, sigma=2.0)

    def test_conformal_clock_lapse_sigma_floor_clamping_and_extreme_underflow(self) -> None:
        self.assertEqual(p2.conformal_clock_lapse(0.0, sigma=1e-15), 1e-12)
        self.assertEqual(p2.conformal_clock_lapse(0.0, sigma=1e-12), 1e-12)
        self.assertEqual(p2.conformal_clock_lapse(0.0, sigma=2e-12), 2e-12)
        self.assertEqual(p2.conformal_clock_lapse(0.0, F=1e308, H=1e308), 0.0)

    def test_conformal_acceleration_1d_extreme_steps_and_callable_errors(self) -> None:
        with self.assertRaises(TypeError):
            p2.conformal_acceleration_1d(5.0, None)  # type: ignore[arg-type]

        def boom(_r: float) -> float:
            raise RuntimeError("custom kappa_fn failure")

        with self.assertRaisesRegex(RuntimeError, "custom kappa_fn failure"):
            p2.conformal_acceleration_1d(5.0, boom)

        for bad_ret in (None, "0.5"):
            with self.assertRaises(ValueError):
                p2.conformal_acceleration_1d(5.0, lambda _r, v=bad_ret: v)  # type: ignore[arg-type, return-value]

        for inc in (True, False):
            fn = (
                (lambda r: 0.9 if r < 5.0 else (0.95 if r == 5.0 else 1.0))
                if inc
                else (lambda r: 1.0 if r < 5.0 else (0.95 if r == 5.0 else 0.9))
            )
            res = p2.conformal_acceleration_1d(
                5.0, fn, lambda_p=sys.float_info.max, dr_kpc=1e-4
            )
            self.assertTrue(math.isfinite(float(res["a_conformal"])))
            self.assertTrue(math.isfinite(float(res["a_phi"])))
            self.assertEqual(float(res["a_conformal"]) + float(res["a_phi"]), 0.0)

        # BUG-1: r_kpc + dr_kpc overflow must raise ValueError before calling kappa_fn(inf)
        seen_r: list[float] = []

        def capture_kappa(r: float) -> float:
            seen_r.append(r)
            return 0.5

        with self.assertRaises(ValueError):
            p2.conformal_acceleration_1d(1.5e308, capture_kappa, lambda_p=1.0, dr_kpc=1.0e308)
        self.assertEqual(seen_r, [])

        # BUG-2: subnormal dr_kpc causing non-finite acceleration overflow raises ValueError
        r_sub, dr_sub = 1e-315, 1e-316
        with self.assertRaises(ValueError):
            p2.conformal_acceleration_1d(
                r_sub,
                lambda r: 0.0 if r < r_sub else (0.5 if r == r_sub else 1.0),
                lambda_p=1.0,
                dr_kpc=dr_sub,
            )

        # BUG-4: sub-ULP dr_kpc below float64 resolution raises ValueError
        with self.assertRaises(ValueError):
            p2.conformal_acceleration_1d(
                10.0, lambda r: 1.0 - math.exp(-r), lambda_p=1e-7, dr_kpc=1e-16
            )

    def test_pathway2_audit_parameter_guards_and_custom_regimes(self) -> None:
        with self.assertRaises(ValueError):
            p2.audit_sign_consistency(w_sfr=-0.1)
        with self.assertRaises(ValueError):
            p2.audit_sign_consistency(dr_kpc=0.0)
        with self.assertRaises(ValueError):
            p2.audit_sign_consistency(dr_kpc=5.0)
        sign_wsfr = p2.audit_sign_consistency(w_sfr=0.5)
        self.assertFalse(sign_wsfr["passed"])
        self.assertEqual(sign_wsfr["t1_repulsive_count"], 8)

        with self.assertRaises(ValueError):
            p2.audit_conformal_ppn_lensing(vlbi_precision=0.0)
        self.assertFalse(p2.audit_conformal_ppn_lensing(cassini_bound=3.0)["passed"])
        self.assertTrue(
            p2.audit_conformal_ppn_lensing(cassini_bound=3.0, vlbi_precision=2.0)["passed"]
        )

        for bad_sparc in (
            {"lambda_p_grid": ()},
            {"sigma_crit_grid": ()},
            {"sigma_crit_grid": [0.0]},
            {"sigma_crit_grid": [-0.01]},
            {"lambda_p_grid": [0.0]},
        ):
            with self.subTest(bad_sparc=bad_sparc):
                with self.assertRaises(ValueError):
                    p2.audit_sparc_mass_scaling(**bad_sparc)  # type: ignore[arg-type]

        sparc_1x1 = p2.audit_sparc_mass_scaling(
            lambda_p_grid=[1e-7], sigma_crit_grid=[0.008]
        )
        self.assertFalse(sparc_1x1["passed"])
        self.assertTrue(math.isfinite(float(sparc_1x1["best_sign_flipped_mean_error"])))
        self.assertEqual(sparc_1x1["best_sign_flipped_fit"]["lambda_p"], 1e-7)
        self.assertEqual(sparc_1x1["best_sign_flipped_fit"]["sigma_crit"], 0.008)

        with self.assertRaises(ValueError):
            p2.audit_clock_scale_gap(max_kappa_diff=1.1)
        zero_grad = p2.audit_clock_scale_gap(max_kappa_diff=1.0, lab_grad_kappa_per_m=0.0)
        self.assertEqual(zero_grad["lab_acceleration_m_s2"], 0.0)
        passing_clock = p2.audit_clock_scale_gap(galactic_lambda_p=1e-19)
        self.assertTrue(passing_clock["passed"])
        self.assertLess(passing_clock["nist_gap_ratio"], 1.0)
        self.assertLess(passing_clock["gps_gap_ratio"], 1.0)

    def test_explore_modified_variants_bond_network_and_gamma_sweep_exactness(self) -> None:
        variants = p2.explore_modified_variants()
        var_b = variants["variant_b_non_conformal_metric"]
        bnet = var_b["bond_network_check"]
        self.assertEqual(bnet["n_bonds"], 2)
        self.assertEqual(bnet["bond_12_sigma"], 1.0)
        self.assertGreater(bnet["bond_01_sigma"], 1.0)
        self.assertFalse(bnet["bonds_py_has_mass_coupling"])

        u_weak = float(var_b["u_weak_field"])
        pi_t = math.exp(u_weak)
        self.assertAlmostEqual(float(bnet["bond_01_sigma"]), 1.0 / (pi_t**2), places=14)
        for row in var_b["gamma_param_sweep"]:
            gamma_param = float(row["gamma_param"])
            self.assertAlmostEqual(float(row["gamma_eff"]), gamma_param, places=5)
            self.assertAlmostEqual(
                float(row["deflection_factor"]),
                0.5 * (1.0 + float(row["gamma_eff"])),
                places=14,
            )


class TestTier5UnifiedRunnerAndManifestHardening(unittest.TestCase):
    """Challenger 2 (M4) unified runner, manifest, re-entry gates, and CLI tests."""

    def test_combined_closure_manifest_positional_id_semantic_alignment_and_guards(self) -> None:
        p2_raw = p2.closure_manifest()
        self.assertEqual(len(p2_raw), 10)
        self.assertEqual(len(kgr._PATHWAY2_ENTRY_IDS), 10)

        expected_pairs = (
            ("m0", "M0"),
            ("participation_aperture", "Pi(kappa)"),
            ("conformal_acceleration", "grad(ln Pi)"),
            ("conformal_minkowski", "g_mu_nu = Pi(x)^2"),
            ("nonconformal_spatial", "Non-conformal spatial"),
            ("lambda_p", "lambda_P"),
            ("t1_contraction", "T1 contraction"),
            ("external_si", "C_SI, G_SI"),
            ("cassini_vlbi", "CASSINI_GAMMA_PPN_BOUND"),
            ("clock_product", "PUBLISHED_CLOCK_COMPARISONS"),
        )
        for idx, (id_tok, sym_tok) in enumerate(expected_pairs):
            self.assertIn(id_tok, kgr._PATHWAY2_ENTRY_IDS[idx])
            self.assertIn(sym_tok, str(p2_raw[idx]["symbol_or_relation"]))

        combined = kgr.combined_closure_manifest()
        ids = [str(e["id"]) for e in combined["entries"]]
        self.assertEqual(len(ids), 19)
        self.assertEqual(len(set(ids)), 19)

        orig_p1 = kgr.pathway1_closure_manifest
        orig_p2 = kgr.pathway2_closure_manifest
        try:
            # Native tag with is_native_det=False raises ValueError
            bad_p1_native = [dict(orig_p1()[0], tag="TH-DET", is_native_det=False)]
            kgr.pathway1_closure_manifest = lambda: bad_p1_native
            with self.assertRaises(ValueError):
                kgr.combined_closure_manifest()

            # Non-native tag with is_native_det=True raises ValueError
            bad_p1_fit = [dict(orig_p1()[0], tag="FIT", is_native_det=True)]
            kgr.pathway1_closure_manifest = lambda: bad_p1_fit
            with self.assertRaises(ValueError):
                kgr.combined_closure_manifest()

            kgr.pathway1_closure_manifest = orig_p1
            # Unknown Pathway 2 epistemic_tag raises ValueError
            bad_p2_tag = [dict(orig_p2()[0], epistemic_tag="BOGUS")]
            kgr.pathway2_closure_manifest = lambda: bad_p2_tag
            with self.assertRaises(ValueError):
                kgr.combined_closure_manifest()

            # >10 entries in Pathway 2 manifest uses fallback ID p2_entry_11
            extra_p2 = list(orig_p2()) + [dict(orig_p2()[0])]
            kgr.pathway2_closure_manifest = lambda: extra_p2
            ext_manifest = kgr.combined_closure_manifest()
            self.assertEqual(ext_manifest["pathway2_count"], 11)
            self.assertEqual(ext_manifest["entries"][-1]["id"], "p2_entry_11")
        finally:
            kgr.pathway1_closure_manifest = orig_p1
            kgr.pathway2_closure_manifest = orig_p2

    def test_run_all_pathway_evaluations_overrides_compact_parity_and_errors(self) -> None:
        res_b0 = kgr.run_all_pathway_evaluations(beta=0.0, include_sub_evaluations=False)
        self.assertEqual(res_b0["pathway1"]["status"], "REFUTED")
        inv_b0 = res_b0["verification_invariants"]
        self.assertFalse(inv_b0["is_default_parameter_set"])
        self.assertTrue(inv_b0["pathway1_status_matches"])
        self.assertTrue(inv_b0["consistent_with_expected_verdicts"])

        res_b98 = kgr.run_all_pathway_evaluations(beta=0.98, include_sub_evaluations=False)
        self.assertEqual(res_b98["pathway1"]["status"], "REFUTED")

        res_2d = kgr.run_all_pathway_evaluations(
            gas_mode="freeman_2d",
            w_sfr=0.5,
            sigma_crit=0.002,
            scale_height_kpc=0.5,
            include_sub_evaluations=False,
        )
        self.assertIn(
            res_2d["pathway1"]["status"],
            {"PARTIAL_LIMITATION", "REFUTED", "VIABLE_PROVISIONAL"},
        )
        self.assertFalse(res_2d["verification_invariants"]["is_default_parameter_set"])

        for bad_kw in (
            {"scale_height_kpc": 0.0},
            {"scale_height_kpc": -1.0},
            {"w_sfr": -0.1},
            {"sigma_crit": float("inf")},
        ):
            with self.subTest(bad_kw=bad_kw):
                with self.assertRaises(ValueError):
                    kgr.run_all_pathway_evaluations(**bad_kw)

        # Compact vs full parity
        full = kgr.run_all_pathway_evaluations(include_sub_evaluations=True)
        compact = kgr.run_all_pathway_evaluations(include_sub_evaluations=False)
        p1_sum = compact["pathway1"]["sub_evaluation_summary"]
        p1_full = full["pathway1"]["sub_evaluations"]
        self.assertEqual(p1_sum["f6"]["n_increasing"], p1_full["f6"]["n_increasing"])
        self.assertEqual(p1_sum["sparc"]["mean_error"], p1_full["sparc"]["mean_error"])
        self.assertEqual(
            p1_sum["asymptotics"]["regime_summaries"],
            p1_full["asymptotics"]["regime_summaries"],
        )
        self.assertEqual(
            p1_sum["screening"]["rho_crit_kg_m3"],
            p1_full["screening"]["rho_crit_kg_m3"],
        )

        p2_sum = compact["pathway2"]["audit_summary"]
        p2_full = full["pathway2"]["audits"]
        self.assertEqual(
            p2_sum["sign_consistency"]["t1_repulsive_count"],
            p2_full["sign_consistency"]["t1_repulsive_count"],
        )
        self.assertEqual(
            p2_sum["conformal_ppn_lensing"]["gamma_ppn"],
            p2_full["conformal_ppn_lensing"]["gamma_ppn"],
        )
        self.assertEqual(
            p2_sum["sparc_mass_scaling"]["best_sign_flipped_mean_error"],
            p2_full["sparc_mass_scaling"]["best_sign_flipped_mean_error"],
        )
        self.assertEqual(
            p2_sum["clock_scale_gap"]["nist_gap_ratio"],
            p2_full["clock_scale_gap"]["nist_gap_ratio"],
        )

    def test_reentry_gate_audit_deep_schema_and_guardrails(self) -> None:
        audit = kgr.reentry_gate_audit()
        relaxed_keys = {"gate", "source", "disposition", "scope_and_conditions"}
        strict_keys = {"gate", "source", "disposition", "enforcement"}
        for item in audit["relaxed_gates"]:
            self.assertEqual(set(item.keys()), relaxed_keys)
        for item in audit["strict_gates_kept"]:
            self.assertEqual(set(item.keys()), strict_keys)

        snap = audit["det_falsification_snapshot"]
        self.assertEqual(
            snap["claim_register_keys"],
            [
                "clock_anomaly",
                "gravity_emergence",
                "kappa_distinct_field",
                "structural_proxy",
            ],
        )
        self.assertEqual(
            set(snap["data_guardrails"].keys()),
            {"sparc_rotation_curves", "eotvos_eta"},
        )
        self.assertEqual(
            snap["gravity_emergence_note"]["revival_track"]["runner"],
            "det8.models.kappa_gravity_revival",
        )

    def test_cli_full_flag_help_invalid_arg_and_nonzero_exit_path(self) -> None:
        base_cmd = [sys.executable, "-B", "-m", "det8.models.kappa_gravity_revival"]

        full_proc = subprocess.run(
            base_cmd + ["--full"], cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(full_proc.returncode, 0, msg=full_proc.stderr)
        self.assertEqual(full_proc.stderr, "")
        self.assertGreater(len(full_proc.stdout.splitlines()), 10)
        full_json = json.loads(full_proc.stdout, parse_constant=_reject_nonfinite_json_constant)
        self.assertIn("pathway1_evaluation", full_json)
        self.assertIn("pathway2_evaluation", full_json)

        help_proc = subprocess.run(
            base_cmd + ["--help"], cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(help_proc.returncode, 0)
        self.assertIn("usage:", help_proc.stdout.lower())

        bogus_proc = subprocess.run(
            base_cmd + ["--bogus-flag"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(bogus_proc.returncode, 2)
        self.assertEqual(bogus_proc.stdout, "")
        self.assertIn("usage:", bogus_proc.stderr.lower())

        orig_expected = kgr.PATHWAY2_EXPECTED_STATUS
        try:
            kgr.PATHWAY2_EXPECTED_STATUS = "VIABLE"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = kgr.main(["--compact"])
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue(), parse_constant=_reject_nonfinite_json_constant)
            self.assertFalse(payload["verification_invariants"]["consistent_with_expected_verdicts"])
        finally:
            kgr.PATHWAY2_EXPECTED_STATUS = orig_expected

        eval_full = kgr.run_all_pathway_evaluations(include_sub_evaluations=True)
        sum_compact = kgr.build_cli_summary(eval_full, include_details=False)
        sum_full = kgr.build_cli_summary(eval_full, include_details=True)
        self.assertNotIn("pathway1_evaluation", sum_compact)
        self.assertIn("pathway1_evaluation", sum_full)
        self.assertEqual(sum_compact["comparative_summary"], sum_full["comparative_summary"])


class TestTier5CoreAlignmentAndQuarantineHardening(unittest.TestCase):
    """Challenger 2 (Core Alignment & Quarantine) Tier 5 boundary contracts."""

    def test_det_falsification_revival_track_and_decision_boundaries(self) -> None:
        note = det_falsification.gravity_emergence_note()
        track = note["revival_track"]
        self.assertEqual(
            set(track.keys()),
            {"runner", "pathway_1", "pathway_2", "claim_promotion"},
        )
        self.assertEqual(track["runner"], "det8.models.kappa_gravity_revival")
        self.assertIn("PARTIAL_LIMITATION", track["pathway_1"])
        self.assertIn("REFUTED", track["pathway_2"])
        self.assertIn("unpromoted", track["claim_promotion"].lower())
        claims = det_falsification.claim_register()
        self.assertEqual(claims["gravity_emergence"]["status"], "OPEN frontier (not claimed)")

        with self.assertRaises(ValueError):
            det_falsification.classify_clock_result(0.0, sigma=0.0)
        self.assertEqual(
            det_falsification.classify_clock_result(1e-18, sigma=1e-18)["verdict"],
            "anomalous",
        )
        self.assertEqual(
            det_falsification.classify_clock_result(-0.5e-18, sigma=1e-18)["verdict"],
            "null",
        )
        self.assertEqual(
            det_falsification.classify_discriminator_result(0.5, 1e-6)["verdict"],
            "inconclusive",
        )
        self.assertEqual(
            det_falsification.classify_discriminator_result(1.0, 1.0)["verdict"],
            "inconclusive",
        )

    def test_det_units_and_det8_core_boundary_contracts(self) -> None:
        nu = det_units.natural_units()
        self.assertEqual(nu["kappa_range"], "[0, 1]")
        self.assertIn("2.99792458e8", nu["dimensional_anchors"]["c"])
        self.assertEqual(float(nu["dimensional_anchors"]["c"].split()[0]), go.C_SI)
        self.assertIn(f"{go.G_SI:.5e}", nu["dimensional_anchors"]["G"])

        with self.assertRaises(ValueError):
            det_units.lambda_p_from_clock_shift(0.1, kappa=0.0)
        with self.assertRaises(ValueError):
            det_units.alpha_from_gravity_shift(0.1, chi=0.0)
        with self.assertRaises(ValueError):
            det_units.kappa_from_proxy_response(-0.1)
        with self.assertRaises(ValueError):
            det_units.kappa_from_proxy_response(0.5, p=0.0)
        with self.assertRaises(ValueError):
            det_units.coupling_implications(kappa_earth=0.0)

        rec = det8_core.NodeRecord(
            kappa=-0.5, sigma=1e-20, H=-1.0, eta=-0.2, F=-0.3
        )
        self.assertEqual(rec.kappa, 0.0)
        self.assertEqual(rec.sigma, 1e-12)
        self.assertEqual(rec.H, 0.0)
        self.assertEqual(rec.eta, 0.0)
        self.assertEqual(rec.F, 0.0)
        rec_hi = det8_core.NodeRecord(kappa=1.5, eta=1.5, _proper_time=2.5)
        self.assertEqual(rec_hi.kappa, 1.0)
        self.assertEqual(rec_hi.eta, 1.0)
        rec_copy = rec_hi.copy()
        self.assertEqual(rec_copy.kappa, 1.0)
        self.assertEqual(rec_copy._proper_time, 2.5)

        # Documented NaN clamping behavior in det8_core.NodeRecord
        rec_nan = det8_core.NodeRecord(
            kappa=float("nan"),
            eta=float("nan"),
            sigma=float("nan"),
            H=float("nan"),
            F=float("nan"),
        )
        self.assertEqual(rec_nan.kappa, 1.0)
        self.assertEqual(rec_nan.eta, 1.0)
        self.assertEqual(rec_nan.sigma, 1e-12)
        self.assertEqual(rec_nan.H, 0.0)
        self.assertEqual(rec_nan.F, 0.0)

        with self.assertRaises(ValueError):
            det8_core.participation_aperture(det8_core.NodeRecord(), velocity_fraction=1.0)
        self.assertEqual(
            det8_core.participation_aperture(det8_core.NodeRecord(), velocity_fraction=-0.5),
            1.0,
        )
        with self.assertRaises(ZeroDivisionError):
            det8_core.participation_aperture(
                det8_core.NodeRecord(kappa=1.0), lambda_p=-1.0
            )

    def test_legacy_gravity_quarantine_immutability_and_partial_rejection(self) -> None:
        self.assertEqual(len(lgq.FULLY_RETIRED), 28)
        for mapping in (
            lgq.FULLY_RETIRED,
            lgq.PARTIALLY_QUARANTINED,
            lgq.SALVAGED_CORRESPONDENCE,
        ):
            with self.assertRaises(TypeError):
                mapping["__probe__"] = None  # type: ignore[index]
        with self.assertRaises(KeyError):
            lgq.quarantine_record("det8.models.det8_core")


if __name__ == "__main__":
    unittest.main()
