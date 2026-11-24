"""Unit tests for neutral empirical galaxy observables and geometry helpers."""

from __future__ import annotations

import ast
import json
import math
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from det8.models import galaxy_observables as go
from det8.models.legacy_gravity_quarantine import FULLY_RETIRED, PARTIALLY_QUARANTINED
from det8.models.reference_constants import NEWTONIAN_G_SI


class ConstantsAndProvenanceTests(unittest.TestCase):
    def test_constants_match_reference_and_unit_anchors(self) -> None:
        self.assertEqual(go.G_SI, NEWTONIAN_G_SI)
        self.assertEqual(go.G_SI, 6.67430e-11)
        self.assertEqual(go.C_SI, 2.99792458e8)
        self.assertEqual(go.M_SUN_KG, 1.989e30)
        self.assertEqual(go.KPC_TO_M, 3.086e19)
        self.assertEqual(go.KM_S_TO_M_S, 1000.0)

    def test_provenance_is_neutral_and_non_warrant_claiming(self) -> None:
        prov = go.OBSERVABLE_PROVENANCE
        self.assertEqual(prov["det_claim_status"], "NEUTRAL_DATA_FIXTURE")
        self.assertIn("none", str(prov["dg_warrant_impact"]).lower())
        self.assertEqual(
            prov["reference_constants_source"],
            "det8.models.reference_constants.NEWTONIAN_G_SI",
        )
        self.assertIn("M_star", str(prov["dataset_discrepancy_caveat"]))

    def test_quarantine_and_import_isolation(self) -> None:
        module_path = Path(go.__file__).resolve()
        source = module_path.read_text(encoding="utf-8")
        self.assertNotIn("QUARANTINE = quarantine_record(__name__)", source)

        tree = ast.parse(source, filename=str(module_path))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
            elif isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)

        self.assertFalse(imported_modules & set(FULLY_RETIRED))
        self.assertFalse(imported_modules & set(PARTIALLY_QUARANTINED))
        det8_imports = {m for m in imported_modules if m.startswith("det8")}
        self.assertEqual(det8_imports, {"det8.models.reference_constants"})


class DatasetIntegrityAndParityTests(unittest.TestCase):
    def test_known_and_sample_counts_and_frozen_dataclasses(self) -> None:
        self.assertEqual(len(go.KNOWN_GALAXIES), 8)
        self.assertEqual(len(go.SAMPLE_GALAXIES), 43)

        with self.assertRaises(FrozenInstanceError):
            setattr(go.KNOWN_GALAXIES[0], "M_star", 99.0)
        with self.assertRaises(FrozenInstanceError):
            setattr(go.SAMPLE_GALAXIES[0], "v_flat", 99.0)

        for g in go.KNOWN_GALAXIES:
            with self.subTest(known=g.name):
                self.assertGreater(g.M_star, 0.0)
                self.assertGreater(g.r_d, 0.0)
                self.assertGreater(g.M_gas, 0.0)
                self.assertGreater(g.r_gas, 0.0)
                self.assertGreater(g.SFR, 0.0)
                self.assertGreater(g.r_SFR, 0.0)
                self.assertGreater(g.V_flat, 0.0)

        for g in go.SAMPLE_GALAXIES:
            with self.subTest(sample=g.name):
                self.assertGreater(g.M_star, 0.0)
                self.assertGreater(g.r_d, 0.0)
                self.assertGreater(g.M_gas, 0.0)
                self.assertGreater(g.r_gas, 0.0)
                self.assertGreater(g.v_flat, 0.0)
                self.assertGreater(g.r_max, 0.0)

    def test_exact_parity_with_retired_reference_datasets(self) -> None:
        from det8.models import kappa_derivation, sparc_analysis

        self.assertEqual(len(go.KNOWN_GALAXIES), len(kappa_derivation.KNOWN_GALAXIES))
        for new_g, old_g in zip(go.KNOWN_GALAXIES, kappa_derivation.KNOWN_GALAXIES):
            with self.subTest(known=new_g.name):
                self.assertEqual(new_g.name, old_g.name)
                self.assertEqual(new_g.M_star, old_g.M_star)
                self.assertEqual(new_g.r_d, old_g.r_d)
                self.assertEqual(new_g.M_gas, old_g.M_gas)
                self.assertEqual(new_g.r_gas, old_g.r_gas)
                self.assertEqual(new_g.SFR, old_g.SFR)
                self.assertEqual(new_g.r_SFR, old_g.r_SFR)
                self.assertEqual(new_g.age, old_g.age)
                self.assertEqual(new_g.V_flat, old_g.V_flat)

        self.assertEqual(len(go.SAMPLE_GALAXIES), len(sparc_analysis.SAMPLE_GALAXIES))
        for new_g, old_g in zip(go.SAMPLE_GALAXIES, sparc_analysis.SAMPLE_GALAXIES):
            with self.subTest(sample=new_g.name):
                self.assertEqual(new_g.name, old_g.name)
                self.assertEqual(new_g.M_star, old_g.M_star)
                self.assertEqual(new_g.r_d, old_g.r_d)
                self.assertEqual(new_g.M_gas, old_g.M_gas)
                self.assertEqual(new_g.r_gas, old_g.r_gas)
                self.assertEqual(new_g.v_flat, old_g.v_flat)
                self.assertEqual(new_g.r_max, old_g.r_max)


class GeometryAndVelocityHelperTests(unittest.TestCase):
    def test_surface_densities_and_domain_guards(self) -> None:
        sigma_0 = go.stellar_surface_density(0.0, 10.0, 2.0)
        self.assertAlmostEqual(sigma_0, 10.0 / (2.0 * math.pi * 4.0), places=12)
        sigma_r = go.stellar_surface_density(2.0, 10.0, 2.0)
        self.assertAlmostEqual(sigma_r, sigma_0 * math.exp(-1.0), places=12)

        sfr_0 = go.sfr_surface_density(0.0, 2.0, 4.0)
        self.assertAlmostEqual(sfr_0, 2.0 / (2.0 * math.pi * 16.0), places=12)

        self.assertEqual(go.stellar_surface_density(1.0, 10.0, 0.0), 0.0)
        self.assertEqual(go.stellar_surface_density(1.0, 0.0, 2.0), 0.0)
        self.assertEqual(go.sfr_surface_density(1.0, 1.0, 0.0), 0.0)
        self.assertEqual(go.sfr_surface_density(1.0, 0.0, 2.0), 0.0)

        bad_vals = (-0.1, float("nan"), float("inf"), float("-inf"))
        for bad in bad_vals:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(bad, 10.0, 2.0)
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(1.0, 10.0, bad)
                with self.assertRaises(ValueError):
                    go.sfr_surface_density(bad, 1.0, 2.0)
                with self.assertRaises(ValueError):
                    go.sfr_surface_density(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.sfr_surface_density(1.0, 1.0, bad)

    def test_enclosed_disk_mass_branches_continuity_and_guards(self) -> None:
        self.assertEqual(go.stellar_disk_mass(0.0, 10.0, 2.0), 0.0)
        self.assertEqual(go.stellar_disk_mass(2.0, 10.0, 0.0), 0.0)
        self.assertEqual(go.stellar_disk_mass(2.0, 0.0, 2.0), 0.0)
        self.assertEqual(go.gas_mass_exponential_1d(0.0, 5.0, 3.0), 0.0)
        self.assertEqual(go.gas_mass_exponential_1d(2.0, 0.0, 3.0), 0.0)
        self.assertEqual(go.gas_mass_exponential_1d(2.0, 5.0, 0.0), 0.0)
        self.assertEqual(go.gas_mass_freeman_2d(0.0, 5.0, 3.0), 0.0)
        self.assertEqual(go.gas_mass_freeman_2d(2.0, 0.0, 3.0), 0.0)
        self.assertEqual(go.gas_mass_freeman_2d(2.0, 5.0, 0.0), 0.0)

        # Legacy small-r quadratic branch x < 0.01 in stellar_disk_mass
        self.assertAlmostEqual(
            go.stellar_disk_mass(0.01, 10.0, 2.0),
            10.0 * 0.5 * (0.005**2),
            places=15,
        )

        # Smooth small-x Taylor branch (x < 1e-4) and continuity across x = 1e-4 and x = 0.01 in gas_mass_freeman_2d
        m_gas, r_gas = 5.0, 2.0
        x_small = 5e-5
        self.assertAlmostEqual(
            go.gas_mass_freeman_2d(x_small * r_gas, m_gas, r_gas),
            m_gas * (0.5 * x_small**2 - x_small**3 / 3.0 + x_small**4 / 8.0),
            places=15,
        )
        for boundary in (1e-4, 0.01):
            g_left = go.gas_mass_freeman_2d(math.nextafter(boundary, 0.0) * r_gas, m_gas, r_gas)
            g_at = go.gas_mass_freeman_2d(boundary * r_gas, m_gas, r_gas)
            g_right = go.gas_mass_freeman_2d(math.nextafter(boundary, 1.0) * r_gas, m_gas, r_gas)
            self.assertLess(abs(g_at - g_left), 1e-16)
            self.assertLess(abs(g_right - g_at), 1e-16)
            self.assertLess(abs(g_at - g_left) / g_at, 1e-11)

        # Verify gas_mass_freeman_2d matches Simpson integral of 2*pi*r*Sigma(r) at x = 0.005 (< 0.01)
        r_upper = 0.01
        n_steps = 2000
        h = r_upper / n_steps
        simpson_sum = 0.0
        for i in range(n_steps + 1):
            r_i = i * h
            integrand = 2.0 * math.pi * r_i * go.stellar_surface_density(r_i, m_gas, r_gas)
            coeff = 1.0 if (i == 0 or i == n_steps) else (4.0 if i % 2 == 1 else 2.0)
            simpson_sum += coeff * integrand
        simpson_integral = simpson_sum * h / 3.0
        g_2d_small = go.gas_mass_freeman_2d(r_upper, m_gas, r_gas)
        self.assertLess(abs(g_2d_small - simpson_integral) / simpson_integral, 1e-12)

        # Exact Freeman vs 1D gas mass relation:
        # M_1d(r) - M_2d(r) = M_gas * x * exp(-x) > 0
        m_1d = go.gas_mass_exponential_1d(6.0, 5.0, 3.0)
        m_2d = go.gas_mass_freeman_2d(6.0, 5.0, 3.0)
        self.assertGreater(m_1d, m_2d)
        self.assertAlmostEqual(m_1d - m_2d, 5.0 * 2.0 * math.exp(-2.0), places=12)

        # Large-r saturation
        self.assertAlmostEqual(go.stellar_disk_mass(100.0, 10.0, 1.0), 10.0, places=12)

        bad_vals = (-1.0, float("nan"), float("inf"), float("-inf"))
        for bad in bad_vals:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    go.stellar_disk_mass(bad, 10.0, 2.0)
                with self.assertRaises(ValueError):
                    go.stellar_disk_mass(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.stellar_disk_mass(1.0, 10.0, bad)
                with self.assertRaises(ValueError):
                    go.gas_mass_exponential_1d(bad, 5.0, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_exponential_1d(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_exponential_1d(1.0, 5.0, bad)
                with self.assertRaises(ValueError):
                    go.gas_mass_freeman_2d(bad, 5.0, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_freeman_2d(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_freeman_2d(1.0, 5.0, bad)

    def test_extreme_finite_float_handling(self) -> None:
        self.assertEqual(go.stellar_disk_mass(1e308, 10.0, 0.5), 10.0)
        self.assertEqual(go.gas_mass_freeman_2d(1e308, 5.0, 0.5), 5.0)
        self.assertEqual(go.gas_mass_exponential_1d(1e308, 5.0, 0.5), 5.0)

        v_ext = go.newton_rotation_velocity(1e308, 10.0, 0.5, 5.0, 0.5, gas_mode="freeman_2d")
        self.assertTrue(math.isfinite(v_ext))
        self.assertGreaterEqual(v_ext, 0.0)

        v_large = go.newton_rotation_velocity(1e10, 10.0, 0.5, 5.0, 0.5, gas_mode="freeman_2d")
        self.assertTrue(math.isfinite(v_large))
        self.assertGreater(v_large, 0.0)

        s_huge = go.stellar_surface_density(1.0, 10.0, 1e155)
        self.assertTrue(math.isfinite(s_huge))
        self.assertGreaterEqual(s_huge, 0.0)
        self.assertEqual(go.stellar_surface_density(1.0, 10.0, 1e200), 0.0)

        sfr_huge = go.sfr_surface_density(1.0, 1.0, 1e155)
        self.assertTrue(math.isfinite(sfr_huge))
        self.assertGreaterEqual(sfr_huge, 0.0)
        self.assertEqual(go.sfr_surface_density(1.0, 1.0, 1e200), 0.0)

    def test_newton_rotation_velocity_parity_and_guards(self) -> None:
        from det8.models import sparc_analysis

        for g in go.SAMPLE_GALAXIES:
            with self.subTest(galaxy=g.name):
                v_new = go.newton_rotation_velocity(
                    g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="1d"
                )
                v_old = sparc_analysis.newton_rotation_velocity(
                    g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas
                )
                self.assertAlmostEqual(v_new, v_old, delta=1e-12)

                # Small-r (x < 0.01) parity check against sparc_analysis
                r_small = 0.005 * g.r_d
                v_small_new = go.newton_rotation_velocity(
                    r_small, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="1d"
                )
                v_small_old = sparc_analysis.newton_rotation_velocity(
                    r_small, g.M_star, g.r_d, g.M_gas, g.r_gas
                )
                self.assertAlmostEqual(v_small_new, v_small_old, delta=1e-12)

                v_2d = go.newton_rotation_velocity(
                    g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="freeman_2d"
                )
                self.assertGreater(v_2d, 0.0)
                self.assertLessEqual(v_2d, v_new)

        # M_gas = 0.0 returns finite star-only velocity for both gas modes
        v_no_gas_1d = go.newton_rotation_velocity(2.0, 10.0, 2.0, 0.0, 0.0, gas_mode="1d")
        v_no_gas_2d = go.newton_rotation_velocity(2.0, 10.0, 2.0, 0.0, 0.0, gas_mode="freeman_2d")
        self.assertGreater(v_no_gas_1d, 0.0)
        self.assertEqual(v_no_gas_1d, v_no_gas_2d)
        self.assertEqual(go.newton_rotation_velocity(2.0, 0.0, 2.0, 0.0, 0.0), 0.0)

        for bad_r in (0.0, -2.0, float("nan"), float("inf"), float("-inf")):
            with self.subTest(bad_r=bad_r), self.assertRaises(ValueError):
                go.newton_rotation_velocity(bad_r, 10.0, 2.0)

        for bad in (-5.0, float("nan"), float("inf"), float("-inf")):
            with self.subTest(bad_param=bad):
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(1.0, bad, 2.0, 5.0, 3.0)
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(1.0, 10.0, bad, 5.0, 3.0)
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(1.0, 10.0, 2.0, bad, 3.0)
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(1.0, 10.0, 2.0, 5.0, bad)

        with self.assertRaises(ValueError):
            go.newton_rotation_velocity(5.0, 10.0, 2.0, 1.0, 2.0, gas_mode="invalid")


class SparcSubsetDiagnosticTests(unittest.TestCase):
    def test_real_sparc_subset_json_audit(self) -> None:
        report = go.load_sparc_subset_diagnostic()

        self.assertTrue(report["exists"])
        self.assertTrue(report["parsed_ok"])
        self.assertEqual(report["byte_size"], 5055)
        self.assertEqual(report["line_count"], 62)
        self.assertFalse(report["raw_json_valid"])
        self.assertIsNotNone(report["raw_json_error"])
        self.assertEqual(report["parse_mode"], "comment_stripped_wrapped_array")
        self.assertEqual(report["comment_lines"], [1, 2, 3, 4, 5])
        self.assertTrue(report["missing_outer_brackets"])
        self.assertEqual(report["parse_errors"], [])
        self.assertEqual(report["record_count"], 56)

        flaw_kinds = {flaw["kind"] for flaw in report["syntax_flaws"]}
        self.assertTrue(
            {"comment_line", "missing_outer_brackets", "split_opening_brace", "missing_opening_brace", "trailing_comma"}
            <= flaw_kinds
        )

        anomalies = report["anomalies"]
        self.assertEqual(anomalies["m_gas_equals_m_star_count"], 56)
        self.assertEqual(anomalies["zero_v_flat_count"], 12)
        self.assertEqual(anomalies["positive_v_flat_count"], 44)
        self.assertEqual(anomalies["missing_galaxy_params_fields"], ["r_gas", "r_max"])
        self.assertEqual(
            anomalies["missing_galaxy_observables_fields"],
            ["r_gas", "SFR", "r_SFR", "age"],
        )
        self.assertIn("135", anomalies["count_discrepancy_note"])

        cross = report["cross_comparison"]
        self.assertEqual(cross["vs_sample_galaxies"]["overlap_count"], 17)
        self.assertEqual(cross["vs_known_galaxies"]["overlap_count"], 5)
        self.assertEqual(report["provenance"]["det_claim_status"], "NEUTRAL_DATA_FIXTURE")

    def test_heldout_radial_profiles_traceable_verbatim_to_sparc_subset_json(self) -> None:
        report = go.load_sparc_subset_diagnostic()
        records_by_name = {str(r["name"]): r for r in report["records"]}
        raw_lines = go.DEFAULT_SPARC_SUBSET_PATH.read_text(encoding="utf-8").splitlines()
        sample_canon = {go.canonicalize_sparc_catalog_name(g.name) for g in go.SAMPLE_GALAXIES}

        self.assertEqual(len(go.HELDOUT_RADIAL_PROFILES), 9)
        for hp in go.HELDOUT_RADIAL_PROFILES:
            with self.subTest(galaxy=hp.name):
                self.assertNotIn(go.canonicalize_sparc_catalog_name(hp.name), sample_canon)
                self.assertIn(hp.name, records_by_name)
                rec = records_by_name[hp.name]
                self.assertEqual(hp.M_star, float(rec["M_star"]))
                self.assertEqual(hp.r_d, float(rec["r_d"]))
                self.assertEqual(hp.M_gas, float(rec["M_gas"]))
                self.assertEqual(hp.v_flat, float(rec["V_flat"]))
                self.assertGreaterEqual(hp.sparc_subset_line, 1)
                self.assertIn(f'"{hp.name}"', raw_lines[hp.sparc_subset_line - 1])
                for (_, v_obs), m in zip(hp.radial_points, go.HELDOUT_PLATEAU_MULTIPLIERS):
                    self.assertEqual(v_obs, hp.v_flat)
                    self.assertGreater(m, 2.0)

    def test_synthetic_valid_malformed_and_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)

            valid_path = tmp_root / "valid.json"
            valid_payload = [
                {"name": "NGC 2403", "M_star": 3.2, "r_d": 1.4, "M_gas": 2.5, "V_flat": 131.0},
                {"name": "TestGal", "M_star": 1.0, "r_d": 1.0, "M_gas": 1.0, "V_flat": 0.0},
            ]
            valid_path.write_text(json.dumps(valid_payload), encoding="utf-8")
            valid_report = go.load_sparc_subset_diagnostic(valid_path)
            self.assertTrue(valid_report["exists"])
            self.assertTrue(valid_report["parsed_ok"])
            self.assertTrue(valid_report["raw_json_valid"])
            self.assertIsNone(valid_report["raw_json_error"])
            self.assertEqual(valid_report["parse_mode"], "standard_json")
            self.assertFalse(valid_report["missing_outer_brackets"])
            self.assertEqual(valid_report["syntax_flaws"], [])
            self.assertEqual(valid_report["record_count"], 2)
            self.assertEqual(valid_report["anomalies"]["m_gas_equals_m_star_count"], 1)
            self.assertEqual(valid_report["anomalies"]["zero_v_flat_count"], 1)
            self.assertEqual(valid_report["cross_comparison"]["vs_known_galaxies"]["overlap_count"], 1)

            malformed_path = tmp_root / "malformed.json"
            malformed_path.write_text(
                "\n".join(
                    [
                        "# header comment",
                        "{",
                        '"name": "DDO 154", "M_star": 0.28, "r_d": 0.37, "M_gas": 0.25, "V_flat": 47.0},',
                        '{"name": "Broken", "M_star": NOT_A_NUMBER},',
                        '{"name": "Recovered", "M_star": 2.0, "r_d": 1.5, "M_gas": 2.0, "V_flat": 95.0}',
                    ]
                ),
                encoding="utf-8",
            )
            malformed_report = go.load_sparc_subset_diagnostic(malformed_path)
            self.assertTrue(malformed_report["exists"])
            self.assertFalse(malformed_report["parsed_ok"])
            self.assertFalse(malformed_report["raw_json_valid"])
            self.assertEqual(malformed_report["parse_mode"], "line_recovery")
            self.assertEqual(malformed_report["record_count"], 2)
            self.assertEqual(len(malformed_report["parse_errors"]), 1)
            self.assertEqual(malformed_report["parse_errors"][0]["line"], 4)

            missing_report = go.load_sparc_subset_diagnostic(tmp_root / "does_not_exist.json")
            self.assertFalse(missing_report["exists"])
            self.assertFalse(missing_report["parsed_ok"])
            self.assertFalse(missing_report["raw_json_valid"])
            self.assertEqual(missing_report["parse_mode"], "missing_file")
            self.assertEqual(missing_report["record_count"], 0)
            self.assertEqual(len(missing_report["parse_errors"]), 1)

    def test_diagnostic_edge_cases_dir_non_utf8_empty_comments_dict_and_bool_nan(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)

            # Directory path must not raise IsADirectoryError
            dir_report = go.load_sparc_subset_diagnostic(tmp_root)
            self.assertTrue(dir_report["exists"])
            self.assertFalse(dir_report["parsed_ok"])
            self.assertEqual(dir_report["parse_mode"], "not_a_file")
            self.assertEqual(dir_report["record_count"], 0)
            self.assertEqual(dir_report["records"], [])
            self.assertEqual(len(dir_report["parse_errors"]), 1)
            self.assertIn("anomalies", dir_report)
            self.assertIn("cross_comparison", dir_report)
            self.assertIn("provenance", dir_report)

            # Non-UTF-8 binary file must not raise UnicodeDecodeError
            bad_bin = tmp_root / "bad.bin"
            bad_bin.write_bytes(b"\xff\xfe\x00\x00invalid_utf8")
            bin_report = go.load_sparc_subset_diagnostic(bad_bin)
            self.assertTrue(bin_report["exists"])
            self.assertFalse(bin_report["parsed_ok"])
            self.assertEqual(bin_report["parse_mode"], "decode_error")
            self.assertEqual(bin_report["record_count"], 0)
            self.assertEqual(bin_report["records"], [])
            self.assertEqual(len(bin_report["parse_errors"]), 1)

            # Empty file and comments-only file
            empty_path = tmp_root / "empty.json"
            empty_path.write_text("", encoding="utf-8")
            empty_report = go.load_sparc_subset_diagnostic(empty_path)
            self.assertTrue(empty_report["exists"])
            self.assertFalse(empty_report["parsed_ok"])
            self.assertEqual(empty_report["parse_mode"], "empty")
            self.assertEqual(empty_report["record_count"], 0)
            self.assertEqual(len(empty_report["parse_errors"]), 1)

            comments_path = tmp_root / "comments_only.json"
            comments_path.write_text("# comment 1\n# comment 2\n", encoding="utf-8")
            comments_report = go.load_sparc_subset_diagnostic(comments_path)
            self.assertTrue(comments_report["exists"])
            self.assertFalse(comments_report["parsed_ok"])
            self.assertEqual(comments_report["parse_mode"], "empty")
            self.assertEqual(comments_report["comment_lines"], [1, 2])
            self.assertEqual(comments_report["record_count"], 0)
            self.assertEqual(len(comments_report["parse_errors"]), 1)

            # Single-dict JSON root recovers cleanly as 1 record
            single_dict = tmp_root / "single_dict.json"
            single_dict.write_text(
                '{"name": "DDO 154", "M_star": 0.28, "r_d": 0.37, "M_gas": 0.25, "V_flat": 47.0}',
                encoding="utf-8",
            )
            single_report = go.load_sparc_subset_diagnostic(single_dict)
            self.assertTrue(single_report["exists"])
            self.assertTrue(single_report["parsed_ok"])
            self.assertFalse(single_report["raw_json_valid"])
            self.assertTrue(single_report["missing_outer_brackets"])
            self.assertEqual(single_report["parse_mode"], "comment_stripped_wrapped_array")
            self.assertEqual(single_report["record_count"], 1)

            # Bool, NaN, and Infinity values must not leak into numeric aggregations
            bool_nan_path = tmp_root / "bool_nan_inf.json"
            bool_nan_path.write_text(
                json.dumps(
                    [
                        {"name": "DDO 154", "M_star": True, "M_gas": True, "V_flat": False},
                        {"name": "NGC 2403", "M_star": float("nan"), "M_gas": float("nan"), "V_flat": float("nan")},
                        {"name": "NGC 3198", "M_star": float("inf"), "M_gas": float("inf"), "V_flat": float("inf")},
                    ]
                ),
                encoding="utf-8",
            )
            bool_report = go.load_sparc_subset_diagnostic(bool_nan_path)
            self.assertTrue(bool_report["parsed_ok"])
            self.assertEqual(bool_report["record_count"], 3)
            self.assertEqual(bool_report["anomalies"]["m_gas_equals_m_star_count"], 0)
            self.assertEqual(bool_report["anomalies"]["zero_v_flat_count"], 0)
            self.assertEqual(bool_report["anomalies"]["positive_v_flat_count"], 0)
            for overlap in bool_report["cross_comparison"]["vs_sample_galaxies"]["overlaps"]:
                self.assertIsNone(overlap["M_star_ratio"])
            for overlap in bool_report["cross_comparison"]["vs_known_galaxies"]["overlaps"]:
                self.assertIsNone(overlap["M_star_ratio"])


if __name__ == "__main__":
    unittest.main()
