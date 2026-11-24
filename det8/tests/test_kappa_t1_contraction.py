"""Unit tests for Pathway 1 (T1 Kernel-Contraction + Reciprocal Aperture)."""

from __future__ import annotations

import ast
import math
import unittest
from pathlib import Path
from unittest import mock

from det8.models import galaxy_observables as go
from det8.models import kappa_t1_contraction as kt1
from det8.models.legacy_gravity_quarantine import FULLY_RETIRED


FORBIDDEN_AGENCY_NAMES: frozenset[str] = frozenset(
    {
        "a_i",
        "will_coefficient",
        "agency_strength",
        "choice_field",
        "actualization_bias",
        "spirit_force",
        "intention_energy",
        "consciousness_field",
    }
)


class QuarantineAndGovernanceTests(unittest.TestCase):
    def test_quarantine_and_import_isolation(self) -> None:
        self.assertEqual(len(FULLY_RETIRED), 28)

        module_path = Path(kt1.__file__).resolve()
        source = module_path.read_text(encoding="utf-8")
        self.assertNotIn("QUARANTINE = quarantine_record(__name__)", source)

        tree = ast.parse(source, filename=str(module_path))
        imported_modules: set[str] = set()
        exp_constraints_names: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
                if node.module == "det8.models.experimental_constraints":
                    exp_constraints_names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)

        self.assertFalse(imported_modules & set(FULLY_RETIRED))
        det8_imports = {m for m in imported_modules if m.startswith("det8")}
        self.assertEqual(
            det8_imports,
            {
                "det8.models.experimental_constraints",
                "det8.models.galaxy_observables",
            },
        )
        self.assertEqual(exp_constraints_names, {"PUBLISHED_EOTVOS"})

    def test_no_forbidden_agency_variables(self) -> None:
        module_path = Path(kt1.__file__).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"), filename=str(module_path))

        found_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                found_names.add(node.id)
            elif isinstance(node, ast.arg):
                found_names.add(node.arg)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found_names.add(node.name)
            elif isinstance(node, ast.Attribute):
                found_names.add(node.attr)

        self.assertFalse(found_names & FORBIDDEN_AGENCY_NAMES)


class CoreEquationsAndDomainGuardTests(unittest.TestCase):
    def test_t1_contraction_kappa_values_monotonicity_and_guards(self) -> None:
        self.assertEqual(kt1.t1_contraction_kappa(0.0, 0.0, 1.0), 1.0)
        self.assertEqual(kt1.t1_contraction_kappa(5.0, 0.0, 0.0, 0.0, 0.0), 1.0)

        expected_s_star = 10.0 / (2.0 * math.pi * 4.0)
        expected_k = math.exp(-expected_s_star / 0.008)
        self.assertAlmostEqual(
            kt1.t1_contraction_kappa(0.0, 10.0, 2.0, sigma_crit=0.008),
            expected_k,
            places=15,
        )

        # Monotonic increase with radius.
        radii = (0.1, 0.5, 1.0, 3.0, 8.0, 20.0)
        kappas = [
            kt1.t1_contraction_kappa(
                r, 3.2, 1.4, 2.5, 3.0, sigma_crit=0.015, SFR=1.2, r_SFR=2.5, w_sfr=0.5
            )
            for r in radii
        ]
        for idx in range(len(kappas) - 1):
            self.assertGreaterEqual(kappas[idx + 1], kappas[idx])
            self.assertGreaterEqual(kappas[idx], 0.0)
            self.assertLessEqual(kappas[idx + 1], 1.0)

        # Critical 0.0 * inf = nan guard and clean underflow to 0.0.
        k_inf_guard = kt1.t1_contraction_kappa(
            0.0, 1e300, 1e-10, SFR=1e300, r_SFR=1e-10, w_sfr=0.0
        )
        self.assertEqual(k_inf_guard, 0.0)
        self.assertTrue(math.isfinite(k_inf_guard))

        self.assertEqual(kt1.t1_contraction_kappa(0.0, 1e6, 0.1, sigma_crit=1e-6), 0.0)

        # Invalid numeric domain values -> ValueError.
        bad_vals = (True, False, -0.1, float("nan"), float("inf"), float("-inf"))
        for bad in bad_vals:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(bad, 1.0, 1.0)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, bad, 1.0)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, M_gas=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, r_gas=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, SFR=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, w_sfr=bad)  # type: ignore[arg-type]

        for non_pos in (0.0, -1.0, True, float("nan"), float("inf")):
            with self.subTest(non_pos=non_pos):
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, sigma_crit=non_pos)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    kt1.t1_contraction_kappa(1.0, 1.0, 1.0, r_SFR=non_pos)  # type: ignore[arg-type]

        for bad_type in ("1.0", None):
            with self.assertRaises(TypeError):
                kt1.t1_contraction_kappa(bad_type, 1.0, 1.0)  # type: ignore[arg-type]

    def test_reciprocal_aperture_g_eff_series_and_guards(self) -> None:
        self.assertEqual(kt1.reciprocal_aperture_g_eff(0.0, beta=0.93), go.G_SI)
        self.assertEqual(kt1.reciprocal_aperture_g_eff(0.8, beta=0.0), go.G_SI)
        self.assertAlmostEqual(
            kt1.reciprocal_aperture_g_eff(1.0, beta=0.93) / go.G_SI,
            1.0 / (1.0 - 0.93),
            places=14,
        )

        # Perturbative geometric series check: sum_{m=0}^inf (beta * kappa)^m = 1 / (1 - beta * kappa).
        beta, kappa = 0.93, 0.8
        series_sum = go.G_SI * sum((beta * kappa) ** m for m in range(300))
        closed_form = kt1.reciprocal_aperture_g_eff(kappa, beta=beta)
        self.assertAlmostEqual(series_sum / closed_form, 1.0, places=12)

        for bad_k in (-0.01, 1.01, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                kt1.reciprocal_aperture_g_eff(bad_k)  # type: ignore[arg-type]
        for bad_b in (-0.01, 1.0, 1.1, False, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                kt1.reciprocal_aperture_g_eff(0.5, beta=bad_b)  # type: ignore[arg-type]
        for bad_g in (0.0, -1.0, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                kt1.reciprocal_aperture_g_eff(0.5, G=bad_g)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            kt1.reciprocal_aperture_g_eff("0.5")  # type: ignore[arg-type]

    def test_pathway1_rotation_velocity_modes_and_guards(self) -> None:
        sample_gal = go.SAMPLE_GALAXIES[0]
        v_1d = kt1.pathway1_rotation_velocity(sample_gal.r_max, sample_gal, gas_mode="1d")
        v_2d = kt1.pathway1_rotation_velocity(
            sample_gal.r_max, sample_gal, gas_mode="freeman_2d"
        )
        self.assertGreater(v_1d, 0.0)
        self.assertGreater(v_2d, 0.0)
        self.assertLessEqual(v_2d, v_1d)

        v_n = go.newton_rotation_velocity(
            sample_gal.r_max,
            sample_gal.M_star,
            sample_gal.r_d,
            sample_gal.M_gas,
            sample_gal.r_gas,
            gas_mode="1d",
        )
        kap = kt1.t1_contraction_kappa(
            sample_gal.r_max,
            sample_gal.M_star,
            sample_gal.r_d,
            sample_gal.M_gas,
            sample_gal.r_gas,
        )
        g_eff = kt1.reciprocal_aperture_g_eff(kap)
        self.assertAlmostEqual(v_1d, v_n * math.sqrt(g_eff / go.G_SI), places=13)

        known_gal = go.KNOWN_GALAXIES[0]
        v_known_no_sfr = kt1.pathway1_rotation_velocity(10.0, known_gal, w_sfr=0.0)
        v_known_with_sfr = kt1.pathway1_rotation_velocity(10.0, known_gal, w_sfr=0.5)
        self.assertGreater(v_known_no_sfr, 0.0)
        self.assertLessEqual(v_known_with_sfr, v_known_no_sfr)

        with self.assertRaises(TypeError):
            kt1.pathway1_rotation_velocity(5.0, {"M_star": 1.0})  # type: ignore[arg-type]
        for bad_r in (0.0, -1.0, True, float("nan")):
            with self.assertRaises(ValueError):
                kt1.pathway1_rotation_velocity(bad_r, sample_gal)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            kt1.pathway1_rotation_velocity(5.0, sample_gal, gas_mode="spherical")


class F6AndSparcEmpiricalTests(unittest.TestCase):
    def test_f6_sign_resolution_on_known_galaxies(self) -> None:
        for w_sfr in (0.0, 0.5, 100.0):
            with self.subTest(w_sfr=w_sfr):
                res = kt1.evaluate_f6_sign_check(sigma_crit=0.015, w_sfr=w_sfr)
                self.assertEqual(res["n_total"], 8)
                self.assertEqual(res["n_increasing"], 8)
                self.assertEqual(res["n_monotonic"], 8)
                self.assertTrue(res["all_increasing"])
                self.assertTrue(res["all_monotonic"])
                for gal in res["galaxies"]:
                    self.assertGreater(gal["delta_kappa"], 0.0)
                    self.assertTrue(gal["monotonic"])

        with self.assertRaises(ValueError):
            kt1.evaluate_f6_sign_check(r_core_kpc=10.0, r_out_kpc=5.0)
        with self.assertRaises(ValueError):
            kt1.evaluate_f6_sign_check(n_points=1)
        with self.assertRaises(ValueError):
            kt1.evaluate_f6_sign_check(n_points=True)  # type: ignore[arg-type]

    def test_sparc_43_fit_1d_freeman_2d_and_parity(self) -> None:
        from det8.models import sparc_analysis

        res_1d = kt1.evaluate_sparc_fit(0.008, 0.93, gas_mode="1d")
        self.assertEqual(res_1d["n_galaxies"], 43)
        self.assertAlmostEqual(res_1d["mean_error"], 0.14697319868091122, places=12)
        self.assertEqual(res_1d["within_20pct"], 30)
        self.assertEqual(res_1d["within_50pct"], 41)
        self.assertAlmostEqual(res_1d["max_enhancement"], 1.0 / (1.0 - 0.93), places=12)

        bins = res_1d["mass_bins"]
        self.assertEqual(bins["dwarf"]["count"], 13)
        self.assertEqual(bins["mid"]["count"], 13)
        self.assertEqual(bins["high"]["count"], 17)
        self.assertLess(bins["dwarf"]["mean_error"], 0.13)

        # Freeman 2D gas comparison.
        cmp_2d = res_1d["freeman_2d_comparison"]["freeman_2d"]
        self.assertAlmostEqual(cmp_2d["mean_error"], 0.14830183159854307, places=12)
        self.assertEqual(cmp_2d["within_20pct"], 30)
        self.assertEqual(cmp_2d["within_50pct"], 41)

        # High-beta trade-off check (33-50x degrades SPARC fit).
        self.assertGreater(res_1d["high_beta_tradeoff"]["beta_0.97"]["mean_error"], 0.30)
        self.assertGreater(res_1d["high_beta_tradeoff"]["beta_0.98"]["mean_error"], 0.45)

        # KNOWN_GALAXIES and sparc_subset.json audit checks.
        known_cmp = res_1d["known_galaxies_comparison"]
        self.assertAlmostEqual(
            known_cmp["at_max_5rd_8kpc"]["mean_error"], 0.41190247671781577, places=10
        )
        self.assertGreater(known_cmp["max_sample_over_known_M_star_ratio"], 11.0)
        self.assertEqual(res_1d["sparc_subset_audit"]["record_count"], 56)
        self.assertEqual(res_1d["sparc_subset_audit"]["m_gas_equals_m_star_count"], 56)

        # Cross-check Newtonian component against legacy sparc_analysis inside test only.
        for g in go.SAMPLE_GALAXIES:
            v_old_n = sparc_analysis.newton_rotation_velocity(
                g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas
            )
            k_r = kt1.t1_contraction_kappa(
                g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, sigma_crit=0.008
            )
            v_expected = v_old_n * math.sqrt(1.0 / (1.0 - 0.93 * k_r))
            v_new = kt1.pathway1_rotation_velocity(g.r_max, g, sigma_crit=0.008, beta=0.93)
            self.assertAlmostEqual(v_new, v_expected, delta=1e-11)

        # Newtonian baseline (beta=0.0) fails badly.
        res_newton = kt1.evaluate_sparc_fit(0.008, 0.0, gas_mode="1d")
        self.assertGreater(res_newton["mean_error"], 0.65)
        self.assertEqual(res_newton["within_20pct"], 0)


class AsymptoticsAndScreeningTests(unittest.TestCase):
    def test_radial_asymptotics_keplerian_turnover(self) -> None:
        asym = kt1.evaluate_radial_asymptotics(0.008, 0.93, gas_mode="1d")
        self.assertEqual(asym["n_galaxies"], 43)

        regimes = asym["regime_summaries"]
        self.assertGreater(regimes["four_rd_to_rmax"]["mean_slope"], 0.40)
        self.assertEqual(regimes["four_rd_to_rmax"]["declining_lt_minus_0_1_count"], 0)

        self.assertLess(regimes["rmax_to_2rmax"]["mean_slope"], -0.20)
        self.assertEqual(regimes["outer_2_to_4_rmax"]["steep_lt_minus_0_3_count"], 43)
        self.assertLess(regimes["outer_2_to_4_rmax"]["mean_slope"], -0.45)
        self.assertGreater(regimes["outer_2_to_4_rmax"]["mean_slope"], -0.51)

        mult_50 = asym["multiplier_summaries"]["50.0"]
        self.assertAlmostEqual(mult_50["mean_slope"], -0.5, places=4)
        self.assertEqual(mult_50["near_keplerian_lt_minus_0_45_count"], 43)
        self.assertTrue(asym["summary"]["keplerian_turnover_universal"])

        with self.assertRaises(ValueError):
            kt1.evaluate_radial_asymptotics(r_multipliers=())
        with self.assertRaises(ValueError):
            kt1.evaluate_radial_asymptotics(r_multipliers=(4.0, 2.0))
        with self.assertRaises(ValueError):
            kt1.evaluate_radial_asymptotics(r_multipliers=(0.0, 2.0))

    def test_screening_constraints_enclosed_vs_local_and_fl1(self) -> None:
        rho_crit = kt1.sigma_crit_to_rho_crit(0.008, 0.3, thickness_factor=1.0)
        self.assertAlmostEqual(rho_crit, 1.804745e-21, delta=1e-26)
        rho_crit_2h = kt1.sigma_crit_to_rho_crit(0.008, 0.3, thickness_factor=2.0)
        self.assertAlmostEqual(rho_crit_2h, 0.5 * rho_crit, places=30)

        scr = kt1.evaluate_screening_constraints(sigma_crit=0.008, beta=0.93)
        regimes = scr["regimes"]

        # Exponential screening passes Roche 1 AU, local 1 AU solar wind, and lab solid.
        self.assertTrue(regimes["enclosed_1au_roche"]["exponential"]["passes_bound"])
        self.assertTrue(regimes["local_1au_solar_wind"]["exponential"]["passes_bound"])
        self.assertLess(
            regimes["local_1au_solar_wind"]["exponential"]["delta_G_over_G"], 1e-23
        )
        self.assertTrue(regimes["lab_solid"]["exponential"]["passes_bound"])
        self.assertTrue(
            scr["differential_eotvos"]["microscope_ti_pt"]["exponential"]["passes_bound"]
        )
        self.assertTrue(
            scr["differential_eotvos"]["eot_wash_be_ti"]["exponential"]["passes_bound"]
        )

        # Power-law screening passes enclosed 1 AU Roche, but FAILS local 1 AU solar wind (~729x over).
        self.assertTrue(regimes["enclosed_1au_roche"]["power_law"]["passes_bound"])
        self.assertFalse(regimes["local_1au_solar_wind"]["power_law"]["passes_bound"])
        self.assertGreater(
            regimes["local_1au_solar_wind"]["power_law"]["delta_G_over_G"], 0.01
        )

        # Local 40 AU solar wind fails both forms.
        self.assertTrue(scr["summary"]["local_40au_solar_wind_fails_both_forms"])

        # FL-1 rank separation must be flagged.
        fl1 = scr["fl1_rank_separation"]
        self.assertTrue(fl1["requires_rank_r_gt_1_separation"])
        self.assertGreater(fl1["proxy_violation_factor_vs_microscope"], 1e12)
        self.assertGreaterEqual(len(scr["theoretical_caveats"]), 4)


class CriteriaAndClosureManifestTests(unittest.TestCase):
    def test_evaluate_pathway1_criteria_default_partial_limitation(self) -> None:
        res = kt1.evaluate_pathway1_criteria()
        self.assertEqual(res["status"], "PARTIAL_LIMITATION")
        self.assertEqual(res["summary"]["core_passed_count"], 4)
        self.assertEqual(res["summary"]["core_total_count"], 4)

        limits = res["limitation_checks"]
        self.assertFalse(limits["asymptotic_flatness_maintained"]["passed"])
        self.assertFalse(limits["known_galaxies_velocity_match"]["passed"])
        self.assertFalse(limits["power_law_local_1au_screening"]["passed"])
        self.assertFalse(limits["full_sparc_radial_profiles_tested"]["passed"])
        self.assertFalse(limits["covariant_metric_and_lensing_closed"]["passed"])
        self.assertTrue(limits["fl1_rank_separation_documented"]["passed"])

    def test_evaluate_pathway1_criteria_refuted_on_bad_params(self) -> None:
        cases = (
            ({"beta": 0.0}, "core:r6b_ceiling_and_dwarf"),
            ({"beta": 0.5}, "core:sparc_outer_point_fit"),
            ({"sigma_crit": 10.0}, "core:r6a_exponential_screening"),
            ({"sigma_crit": 1e-6}, "core:sparc_outer_point_fit"),
            ({"sigma_crit": 1e-20}, "core:f6_monotonicity"),
        )
        for kwargs, expected_failure in cases:
            with self.subTest(kwargs=kwargs):
                res = kt1.evaluate_pathway1_criteria(**kwargs)
                self.assertEqual(res["status"], "REFUTED")
                self.assertIn(expected_failure, res["failing_checks"])

    def test_evaluate_pathway1_criteria_viable_provisional_reachable(self) -> None:
        # Bare boolean promotion flags are rejected: actual computed results are required.
        with self.assertRaises(ValueError):
            kt1.evaluate_pathway1_criteria(has_covariant_lensing_action=True)
        with self.assertRaises(ValueError):
            kt1.evaluate_pathway1_criteria(has_full_radial_sparc_profiles=True)

        # Prove status is computed (not hardcoded to PARTIAL_LIMITATION/REFUTED)
        # when all core gates and actual profile/lensing evaluators pass simultaneously.
        mock_asym = {
            "regime_summaries": {"outer_2_to_4_rmax": {"mean_slope": -0.05}},
        }
        mock_sparc = kt1.evaluate_sparc_fit(0.008, 0.93)
        mock_sparc = dict(mock_sparc)
        mock_sparc["known_galaxies_comparison"] = {
            "at_max_5rd_8kpc": {"mean_error": 0.12}
        }
        mock_scr = kt1.evaluate_screening_constraints(sigma_crit=0.008, beta=0.93)
        mock_scr = dict(mock_scr)
        mock_regimes = dict(mock_scr["regimes"])
        mock_local_1au = dict(mock_regimes["local_1au_solar_wind"])
        mock_local_1au["power_law"] = {
            "kappa": 1e-6,
            "delta_G_over_G": 1e-6,
            "passes_bound": True,
        }
        mock_regimes["local_1au_solar_wind"] = mock_local_1au
        mock_scr["regimes"] = mock_regimes

        mock_heldout = dict(kt1.evaluate_heldout_radial_profiles())
        mock_heldout["passed"] = True
        passing_lensing = {
            "has_shared_action_law": True,
            "orbital_rms_error": 0.12,
            "cassini_shapiro_gamma_deviation": 1.0e-6,
            "galactic_lensing_to_dynamical_ratio": 1.0,
        }

        with (
            mock.patch.object(kt1, "evaluate_radial_asymptotics", return_value=mock_asym),
            mock.patch.object(kt1, "evaluate_sparc_fit", return_value=mock_sparc),
            mock.patch.object(
                kt1, "evaluate_screening_constraints", return_value=mock_scr
            ),
            mock.patch.object(
                kt1, "evaluate_heldout_radial_profiles", return_value=mock_heldout
            ),
        ):
            res = kt1.evaluate_pathway1_criteria(
                dynamical_lensing_result=passing_lensing
            )
        self.assertEqual(res["status"], "VIABLE_PROVISIONAL")
        self.assertEqual(res["open_limitations"], [])

    def test_heldout_radial_profiles_and_shared_dynamical_lensing_gates(self) -> None:
        heldout = kt1.evaluate_heldout_radial_profiles()
        self.assertTrue(heldout["strictly_disjoint_from_sample_galaxies"])
        self.assertEqual(heldout["overlap_with_sample_galaxies"], [])
        self.assertTrue(heldout["traceability_audit"]["all_9_verbatim_matched"])
        self.assertFalse(heldout["passed"])
        hp_sum = heldout["heldout_radial_profiles_summary"]
        self.assertEqual(hp_sum["n_galaxies"], 9)
        # On the 9 traceable SPARC rows with frozen (Sigma_crit=0.008, beta=0.93),
        # Pathway 1 has higher curve RMS, higher bend error at 2.2 r_d, and 8/9 late surge vs 0/9 for MOND.
        self.assertGreater(
            hp_sum["mean_curve_rms_pathway1"],
            hp_sum["mean_curve_rms_mond"],
        )
        self.assertGreater(
            hp_sum["mean_bend_velocity_error_pathway1"],
            hp_sum["mean_bend_velocity_error_mond"],
        )
        self.assertGreater(
            hp_sum["spirals_ge_1e9_mean_curve_rms_pathway1"],
            hp_sum["spirals_ge_1e9_mean_curve_rms_mond"],
        )
        self.assertEqual(hp_sum["late_surge_count_pathway1"], 8)
        self.assertEqual(hp_sum["late_surge_count_mond"], 0)
        self.assertEqual(heldout["heldout_sparc_subset_26_summary"]["n_galaxies"], 26)
        self.assertEqual(heldout["heldout_sparc_subset_28_summary"]["n_galaxies"], 28)
        sens = heldout["gas_convention_sensitivity"]
        for mode_key in (
            "recorded_m_gas_1d",
            "recorded_m_gas_freeman_2d",
            "stellar_only_m_gas_zero_1d",
        ):
            self.assertGreater(
                sens[mode_key]["mean_plateau_rms_pathway1"],
                sens[mode_key]["mean_plateau_rms_mond"],
            )
            self.assertEqual(sens[mode_key]["late_surge_count_mond"], 0)
            self.assertGreaterEqual(sens[mode_key]["late_surge_count_pathway1"], 8)

        lensing_default = kt1.evaluate_shared_dynamical_lensing()
        self.assertFalse(lensing_default["passed"])
        lensing_pass = kt1.evaluate_shared_dynamical_lensing(
            {
                "has_shared_action_law": True,
                "orbital_rms_error": 0.14,
                "cassini_shapiro_gamma_deviation": 1.0e-6,
                "galactic_lensing_to_dynamical_ratio": 1.0,
            }
        )
        self.assertTrue(lensing_pass["passed"])

    def test_closure_manifest_tags_and_native_derivations(self) -> None:
        manifest = kt1.closure_manifest()
        self.assertGreaterEqual(len(manifest), 9)

        valid_tags = {"TH-DET", "CORR", "FIT", "EXTERNAL_ANCHOR"}
        ids: set[str] = set()
        for entry in manifest:
            ids.add(str(entry["id"]))
            tag = str(entry["tag"])
            self.assertIn(tag, valid_tags)
            self.assertEqual(entry["is_native_det"], tag == "TH-DET")
            self.assertTrue(str(entry["native_derivation_opportunity"]).strip())
            self.assertTrue(str(entry["known_limitations_or_gaps"]).strip())

        self.assertIn("t1_markov_contraction", ids)
        self.assertIn("sigma_crit", ids)
        self.assertIn("beta", ids)
        self.assertIn("reciprocal_aperture_coupling", ids)
        self.assertIn("external_anchors", ids)

        by_id = {str(entry["id"]): entry for entry in manifest}
        self.assertIn("0.1370", str(by_id["sigma_crit"]["native_derivation_opportunity"]))
        self.assertIn(
            "sum_{m=0}^inf",
            str(by_id["reciprocal_aperture_coupling"]["native_derivation_opportunity"]),
        )


if __name__ == "__main__":
    unittest.main()
