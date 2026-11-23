"""Unit tests for Pathway 2 (Π-Conformal Clock-Metric Bridge) and refutation audits."""

from __future__ import annotations

import ast
import math
import unittest
from pathlib import Path

from det8.models import det8_core
from det8.models import galaxy_observables as go
from det8.models import pi_conformal_bridge as p2
from det8.models.legacy_gravity_quarantine import FULLY_RETIRED, PARTIALLY_QUARANTINED


_FORBIDDEN_QUARANTINED_SYMBOLS = frozenset(
    {
        "LAMBDA_GAMMA",
        "effective_gravity_source",
        "constrain_lambda_gamma_from_eotvos",
        "KNOWN_ANOMALIES",
        "analyze_gravity_anomalies",
        "combined_parameter_constraints",
    }
)


class QuarantineAndProvenanceTests(unittest.TestCase):
    def test_ast_quarantine_and_symbol_isolation(self) -> None:
        module_path = Path(p2.__file__).resolve()
        source = module_path.read_text(encoding="utf-8")

        # Must never carry the retired-module marker
        self.assertNotIn("QUARANTINE = quarantine_record(__name__)", source)

        tree = ast.parse(source, filename=str(module_path))
        imported_modules: set[str] = set()
        imported_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
                imported_names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)

        self.assertEqual(len(FULLY_RETIRED), 28)
        self.assertFalse(imported_modules & set(FULLY_RETIRED))
        self.assertFalse(imported_names & _FORBIDDEN_QUARANTINED_SYMBOLS)

        det8_imports = {m for m in imported_modules if m.startswith("det8")}
        self.assertLessEqual(
            det8_imports,
            {
                "det8.models.det8_core",
                "det8.models.galaxy_observables",
                "det8.models.experimental_constraints",
                "det8.models.bonds",
            },
        )
        # Only permitted partially quarantined modules are det8_core and experimental_constraints
        self.assertLessEqual(
            imported_modules & set(PARTIALLY_QUARANTINED),
            {"det8.models.det8_core", "det8.models.experimental_constraints"},
        )

    def test_all_exports_and_closure_manifest(self) -> None:
        for symbol in p2.__all__:
            self.assertTrue(hasattr(p2, symbol), f"Missing __all__ export: {symbol}")

        manifest = p2.closure_manifest()
        self.assertGreaterEqual(len(manifest), 8)
        tags = {entry["epistemic_tag"] for entry in manifest}
        self.assertEqual(tags, {"TH-DET", "P", "CORR", "FIT", "EXTERNAL_ANCHOR"})
        required_keys = {
            "symbol_or_relation",
            "epistemic_tag",
            "evidence_level",
            "origin",
            "equation_or_value",
            "status_m_or_caveat",
            "independent_discriminator",
        }
        for entry in manifest:
            self.assertEqual(set(entry.keys()), required_keys)


class CoreEquationsAndDomainGuardTests(unittest.TestCase):
    def test_conformal_clock_lapse_and_proper_time_parity(self) -> None:
        cases = [
            (0.0, 0.5, {}),
            (0.25, 0.5, {}),
            (0.5, 0.5, {"sigma": 1.2, "eta": 0.9, "F": 0.1, "H": 0.2, "velocity_fraction": 0.3}),
            (1.0, 2.0e-7, {"sigma": 0.8, "eta": 1.0, "F": 0.0, "H": 0.0, "velocity_fraction": 0.0}),
        ]
        for kappa, lp, kw in cases:
            with self.subTest(kappa=kappa, lambda_p=lp, kw=kw):
                pi_val = p2.conformal_clock_lapse(kappa, lambda_p=lp, **kw)
                rec = det8_core.NodeRecord(
                    kappa=kappa,
                    sigma=kw.get("sigma", 1.0),
                    eta=kw.get("eta", 1.0),
                    F=kw.get("F", 0.0),
                    H=kw.get("H", 0.0),
                )
                expected_pi = det8_core.participation_aperture(
                    rec, velocity_fraction=kw.get("velocity_fraction", 0.0), lambda_p=lp
                )
                self.assertAlmostEqual(pi_val, expected_pi, places=15)

                dtau = p2.proper_time_step(kappa, delta_n=2.5, lambda_p=lp, **kw)
                expected_dtau = det8_core.proper_time_increment(
                    rec, delta_N=2.5, velocity_fraction=kw.get("velocity_fraction", 0.0), lambda_p=lp
                )
                self.assertAlmostEqual(dtau, expected_dtau, places=15)

        # Zero eta gives zero lapse
        self.assertEqual(p2.conformal_clock_lapse(0.5, eta=0.0), 0.0)

    def test_kappa_potential_phi_values(self) -> None:
        self.assertEqual(p2.kappa_potential_phi(0.0, lambda_p=0.5), 0.0)
        self.assertEqual(p2.kappa_potential_phi(0.5, lambda_p=0.0), 0.0)
        for k in (0.25, 0.5, 1.0):
            expected = (go.C_SI**2) * math.log1p(0.5 * k)
            self.assertAlmostEqual(p2.kappa_potential_phi(k, lambda_p=0.5), expected, delta=1e-6)

    def test_conformal_acceleration_numerical_stability_and_sign_opposition(self) -> None:
        # NGC 2403 T1 contraction: at r=2.0 kpc, lambda_p * kappa ~ 4.88e-12;
        # naive ln(Pi_+) - ln(Pi_-) fails by ~1.45%, whereas log1p gives < 1e-7 rel error.
        g = go.KNOWN_GALAXIES[0]
        sc = 0.008
        lp = 2.0e-7

        def kappa_t1(r: float) -> float:
            s_star = go.stellar_surface_density(r, g.M_star, g.r_d)
            s_gas = go.stellar_surface_density(r, g.M_gas, g.r_gas)
            return math.exp(-(s_star + s_gas) / sc)

        for r_kpc in (2.0, 5.0, 10.0, 20.0):
            with self.subTest(r_kpc=r_kpc):
                s_star = go.stellar_surface_density(r_kpc, g.M_star, g.r_d)
                s_gas = go.stellar_surface_density(r_kpc, g.M_gas, g.r_gas)
                k_val = math.exp(-(s_star + s_gas) / sc)
                dk_dr_m = k_val * ((s_star / g.r_d) + (s_gas / g.r_gas)) / sc / go.KPC_TO_M
                a_exact = (go.C_SI**2) * lp * dk_dr_m / (1.0 + lp * k_val)

                res = p2.conformal_acceleration_1d(r_kpc, kappa_t1, lambda_p=lp, dr_kpc=1.0e-4)
                rel_err = abs(float(res["a_conformal"]) - a_exact) / a_exact
                self.assertLess(rel_err, 1.0e-6)
                self.assertGreater(float(res["a_conformal"]), 0.0)
                self.assertLess(float(res["a_phi"]), 0.0)
                self.assertAlmostEqual(float(res["a_conformal_plus_a_phi"]), 0.0, places=20)
                self.assertTrue(res["is_repulsive"])
                self.assertFalse(res["is_attractive"])
                self.assertFalse(res["sign_consistent_with_attractive_phi"])

        # Constant kappa yields zero acceleration
        flat = p2.conformal_acceleration_1d(5.0, lambda r: 0.4, lambda_p=lp)
        self.assertEqual(flat["a_conformal"], 0.0)
        self.assertEqual(flat["a_phi"], 0.0)
        self.assertTrue(flat["sign_consistent_with_attractive_phi"])

    def test_conformal_acceleration_decreasing_kappa_extreme_lambda_p_and_zero_lambda_p(
        self,
    ) -> None:
        def dec_kappa(r: float) -> float:
            if r < 5.0:
                return 1.0
            if r == 5.0:
                return 0.5
            return 0.0

        for lp in (1.0e16, 1.0e308):
            with self.subTest(lambda_p=lp):
                res = p2.conformal_acceleration_1d(5.0, dec_kappa, lambda_p=lp, dr_kpc=1.0e-4)
                a_conf = float(res["a_conformal"])
                a_phi = float(res["a_phi"])
                self.assertTrue(math.isfinite(a_conf))
                self.assertTrue(math.isfinite(a_phi))
                self.assertLess(a_conf, 0.0)
                self.assertGreater(a_phi, 0.0)
                self.assertEqual(a_conf + a_phi, 0.0)
                self.assertEqual(res["a_conformal_plus_a_phi"], 0.0)
                self.assertTrue(res["is_attractive"])
                self.assertFalse(res["is_repulsive"])
                self.assertFalse(res["sign_consistent_with_attractive_phi"])

        # Non-constant kappa at lambda_p = 0.0 produces consistent zero acceleration
        zero_lp = p2.conformal_acceleration_1d(
            5.0, lambda r: 0.2 + 0.01 * r, lambda_p=0.0, dr_kpc=1.0e-4
        )
        self.assertEqual(zero_lp["a_conformal"], 0.0)
        self.assertEqual(zero_lp["a_phi"], 0.0)
        self.assertFalse(zero_lp["is_repulsive"])
        self.assertFalse(zero_lp["is_attractive"])
        self.assertTrue(zero_lp["sign_consistent_with_attractive_phi"])

    def test_exhaustive_domain_guards(self) -> None:
        bad_reals = (
            True,
            False,
            "0.5",
            None,
            float("nan"),
            float("inf"),
            float("-inf"),
            10**400,
        )
        for bad in bad_reals:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(0.5, lambda_p=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.proper_time_step(0.5, delta_n=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(0.5, lambda_p=bad)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.conformal_acceleration_1d(bad, lambda r: 0.5)  # type: ignore[arg-type]
                with self.assertRaises(ValueError):
                    p2.conformal_acceleration_1d(5.0, lambda r: 0.5, dr_kpc=bad)  # type: ignore[arg-type]

        # Out-of-domain values that det8_core would silently clamp or crash on
        for out_k in (-1.0e-9, -0.5, 1.0 + 1.0e-9, 1.5):
            with self.subTest(out_k=out_k):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(out_k)
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(out_k)
                with self.assertRaises(ValueError):
                    p2.conformal_acceleration_1d(5.0, lambda r, v=out_k: v)

        for bad_lp in (-1.0e-12, -1.0, -2.0):
            with self.subTest(bad_lp=bad_lp):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(1.0, lambda_p=bad_lp)
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(0.8, lambda_p=bad_lp)

        # Aperture kwarg guards
        with self.assertRaises(TypeError):
            p2.conformal_clock_lapse(0.5, unknown_arg=1.0)  # type: ignore[call-arg]
        for bad_kw in (
            {"sigma": 0.0},
            {"sigma": -1.0},
            {"sigma": float("nan")},
            {"eta": -0.1},
            {"eta": 1.1},
            {"F": -0.1},
            {"H": -0.1},
            {"velocity_fraction": -0.5},
            {"velocity_fraction": 1.0},
            {"velocity_fraction": True},
        ):
            with self.subTest(bad_kw=bad_kw):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(0.5, **bad_kw)  # type: ignore[arg-type]

        # eta=0.0 disallowed in conformal_acceleration_1d (ln Pi undefined)
        with self.assertRaises(ValueError):
            p2.conformal_acceleration_1d(5.0, lambda r: 0.5, eta=0.0)

        # r_kpc / dr_kpc / kappa_fn guards
        with self.assertRaises(TypeError):
            p2.conformal_acceleration_1d(5.0, "not_callable")  # type: ignore[arg-type]
        for bad_r in (0.0, -2.0):
            with self.assertRaises(ValueError):
                p2.conformal_acceleration_1d(bad_r, lambda r: 0.5)
        for bad_dr in (0.0, -1.0e-4, 5.0, 6.0):
            with self.assertRaises(ValueError):
                p2.conformal_acceleration_1d(5.0, lambda r: 0.5, dr_kpc=bad_dr)
        for bad_ret in (float("nan"), True, -0.01, 1.01):
            with self.assertRaises(ValueError):
                p2.conformal_acceleration_1d(5.0, lambda r, v=bad_ret: v)  # type: ignore[arg-type, return-value]

        # Audit parameter guards
        with self.assertRaises(ValueError):
            p2.audit_sign_consistency(lambda_p=0.0)
        with self.assertRaises(ValueError):
            p2.audit_sign_consistency(sigma_crit=0.0)
        with self.assertRaises(ValueError):
            p2.audit_conformal_ppn_lensing(cassini_bound=0.0)
        with self.assertRaises(ValueError):
            p2.audit_sparc_mass_scaling(gas_mode="invalid")
        with self.assertRaises(ValueError):
            p2.audit_clock_scale_gap(max_kappa_diff=0.0)
        with self.assertRaises(ValueError):
            p2.audit_clock_scale_gap(lab_grad_kappa_per_m=-1.0)


class RefutationAuditTests(unittest.TestCase):
    def test_audit_sign_consistency_and_legacy_f6_parity(self) -> None:
        from det8.models import kappa_derivation

        res = p2.audit_sign_consistency()
        self.assertEqual(res["n_galaxies"], 8)
        self.assertEqual(res["t1_monotone_increasing_count"], 8)
        self.assertEqual(res["t1_repulsive_count"], 8)
        self.assertEqual(res["f6_monotone_increasing_count"], 0)
        self.assertEqual(res["f6_monotone_decreasing_count"], 8)
        self.assertEqual(res["f6_attractive_count"], 8)
        self.assertTrue(res["f6_reintroduces_inside_out_failure"])
        self.assertFalse(res["passed"])

        # Cross-check local F6 parity against retired kappa_derivation in test code only
        for new_g, old_g in zip(go.KNOWN_GALAXIES, kappa_derivation.KNOWN_GALAXIES):
            for r_kpc in (0.5, 5.0, 20.0):
                self.assertAlmostEqual(
                    p2._legacy_f6_kappa(r_kpc, new_g),
                    kappa_derivation.kappa_from_galaxy_properties(r_kpc, old_g),
                    places=14,
                )

    def test_audit_conformal_ppn_lensing(self) -> None:
        res = p2.audit_conformal_ppn_lensing()
        self.assertEqual(res["gamma_ppn"], -1.0)
        self.assertEqual(res["deflection_factor"], 0.0)
        self.assertEqual(res["abs_gamma_minus_one"], 2.0)
        self.assertAlmostEqual(res["cassini_violation_ratio"], 2.0 / 2.3e-5, places=6)
        self.assertGreater(res["cassini_violation_ratio"], 8.69e4)
        self.assertEqual(res["vlbi_fractional_miss"], 1.0)
        self.assertFalse(res["passed"])
        for sample in res["null_invariance_samples"]:
            self.assertEqual(sample["conformal_null_ds_sq"], 0.0)

    def test_audit_sparc_mass_scaling(self) -> None:
        res = p2.audit_sparc_mass_scaling(gas_mode="1d")
        self.assertEqual(res["n_galaxies"], 43)
        self.assertEqual(res["v2_over_c2_min_galaxy"], "NGC 3741")
        self.assertEqual(res["v2_over_c2_max_galaxy"], "NGC 2841")
        self.assertAlmostEqual(res["v2_over_c2_dynamic_range"], (290.0 / 44.0) ** 2, places=9)
        self.assertGreater(res["v2_over_c2_dynamic_range"], 43.4)
        self.assertAlmostEqual(res["btfr"]["ols_slope"], 0.2869, delta=0.002)
        self.assertGreater(res["btfr"]["pearson_r"], 0.95)
        self.assertAlmostEqual(res["btfr"]["btfr_scatter_dex"], 0.3089, delta=0.002)
        self.assertEqual(res["unbound_literal_count"], 38)
        self.assertGreater(res["best_sign_flipped_mean_error"], 0.35)
        self.assertFalse(res["passed"])

        res_2d = p2.audit_sparc_mass_scaling(gas_mode="freeman_2d")
        self.assertGreater(res_2d["best_sign_flipped_mean_error"], 0.35)
        self.assertFalse(res_2d["passed"])

    def test_audit_clock_scale_gap(self) -> None:
        res = p2.audit_clock_scale_gap()
        self.assertEqual(res["nist_product_bound"], 2.0e-18)
        self.assertEqual(res["nist_clock_bound"], 4.0e-18)
        self.assertAlmostEqual(res["nist_gap_ratio"], 5.0e10, delta=1.0)
        self.assertAlmostEqual(res["gps_gap_ratio"], 2.0e-7 / 3.5e-9, places=9)
        self.assertAlmostEqual(res["lab_acceleration_m_s2"], (go.C_SI**2) * 2.0e-7 * 1.0e-12, places=12)
        self.assertFalse(res["passed"])


class ModifiedVariantsAndCriteriaVerdictTests(unittest.TestCase):
    def test_explore_modified_variants(self) -> None:
        res = p2.explore_modified_variants()
        self.assertFalse(res["any_det_native_survivor"])

        var_a = res["variant_a_decoupled_pi"]
        self.assertTrue(var_a["resolves_clock_gap"])
        self.assertTrue(var_a["still_fails_conformal_lensing"])
        self.assertTrue(var_a["still_fails_sparc_mass_scaling"])

        var_b = res["variant_b_non_conformal_metric"]
        self.assertFalse(var_b["bond_network_check"]["bonds_py_has_mass_coupling"])
        sweep = var_b["gamma_param_sweep"]
        self.assertEqual([row["gamma_param"] for row in sweep], [-1.0, 0.0, 1.0])
        self.assertEqual([row["passes_cassini"] for row in sweep], [False, False, True])
        self.assertAlmostEqual(sweep[0]["deflection_factor"], 0.0, delta=1.0e-5)
        self.assertAlmostEqual(sweep[1]["deflection_factor"], 0.5, delta=1.0e-5)
        self.assertAlmostEqual(sweep[2]["deflection_factor"], 1.0, delta=1.0e-5)

        var_c = res["variant_c_mass_coupled_or_poisson"]
        self.assertAlmostEqual(var_c["lambda_p_mass_min"], 1.720e-8, delta=1.0e-10)
        self.assertAlmostEqual(var_c["lambda_p_mass_max"], 4.283e-7, delta=1.0e-9)
        self.assertGreater(var_c["t1_mass_coupled_mean_error"], 0.35)
        self.assertLess(var_c["deep_mond_btfr_mean_error"], 0.20)
        self.assertAlmostEqual(
            var_c["ngc2841_log_potential_depth_over_c2_01_to_50kpc"], 5.815e-6, delta=1.0e-8
        )

    def test_evaluate_pathway2_criteria_refuted(self) -> None:
        verdict = p2.evaluate_pathway2_criteria()
        self.assertEqual(verdict["status"], "REFUTED")
        self.assertEqual(
            verdict["refuted_criteria"],
            ["C1_sign", "C2_lensing", "C3_sparc_btfr", "C4_clock_gap"],
        )
        self.assertEqual(verdict["passed_criteria"], [])
        self.assertEqual(len(verdict["survivor_conditions"]), 4)
        for key in ("C1_sign", "C2_lensing", "C3_sparc_btfr", "C4_clock_gap"):
            self.assertEqual(verdict["criteria"][key]["status"], "REFUTED")
            self.assertFalse(verdict["criteria"][key]["passed"])


if __name__ == "__main__":
    unittest.main()
