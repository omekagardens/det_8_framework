"""Unit tests for the unified kappa-gravity revival runner, gates, manifest, and docs."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

from det8.models import det8_core
from det8.models import det_falsification
from det8.models import det_units
from det8.models import kappa_gravity_revival as kgr
from det8.models import legacy_gravity_quarantine as lgq

REPO_ROOT: Path = Path(__file__).resolve().parents[2]

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

EXPECTED_DOC_FILES: tuple[str, ...] = (
    "PHYSICS.md",
    "MODEL_CARD.md",
    "README.md",
    "ROADMAP.md",
    "NEXT_STEPS.md",
    "GOVERNANCE.md",
    "FALSIFICATION_LEDGER.md",
    "NOVELTY_LEDGER.md",
    "archive/retired_kappa_gravity.md",
    "docs/CONTINUUM_LIMIT_FRAMEWORK.md",
    "docs/applied_physics.md",
    "docs/track_b/gravity.md",
    "docs/observable_anchoring.md",
)


def _reject_nonfinite_json_constant(token: str) -> object:
    raise ValueError(f"Non-standard JSON constant {token!r} is forbidden")


class QuarantineAndIsolationTests(unittest.TestCase):
    def test_quarantine_and_ast_import_isolation(self) -> None:
        self.assertEqual(len(lgq.FULLY_RETIRED), 28)

        module_path = Path(kgr.__file__).resolve()
        source = module_path.read_text(encoding="utf-8")
        marker = "QUARANTINE = quarantine_record(__name__)"
        self.assertNotIn(marker, source)
        self.assertNotIn(marker, Path(lgq.__file__).resolve().read_text(encoding="utf-8"))

        tree = ast.parse(source, filename=str(module_path))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
            elif isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)

        self.assertFalse(imported_modules & set(lgq.FULLY_RETIRED))
        det8_imports = {m for m in imported_modules if m.startswith("det8")}
        self.assertEqual(
            det8_imports,
            {
                "det8.models.det_falsification",
                "det8.models.galaxy_observables",
                "det8.models.kappa_t1_contraction",
                "det8.models.pi_conformal_bridge",
            },
        )

    def test_no_forbidden_agency_identifiers_and_all_exports(self) -> None:
        module_path = Path(kgr.__file__).resolve()
        tree = ast.parse(
            module_path.read_text(encoding="utf-8"), filename=str(module_path)
        )
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
        for symbol in kgr.__all__:
            self.assertTrue(hasattr(kgr, symbol), f"Missing __all__ symbol: {symbol}")


class UnifiedEvaluationAndConsistencyTests(unittest.TestCase):
    def test_run_all_pathway_evaluations_defaults(self) -> None:
        result = kgr.run_all_pathway_evaluations()

        obs = result["observables_and_datasets"]
        self.assertEqual(obs["known_galaxies_count"], 8)
        self.assertEqual(obs["sample_galaxies_count"], 43)
        self.assertEqual(obs["provenance"]["det_claim_status"], "NEUTRAL_DATA_FIXTURE")
        sparc_diag = obs["sparc_subset_diagnostic"]
        self.assertTrue(sparc_diag["parsed_ok"])
        self.assertEqual(sparc_diag["record_count"], 56)

        p1 = result["pathway1"]
        self.assertEqual(p1["status"], "PARTIAL_LIMITATION")
        self.assertEqual(p1["summary"]["core_passed_count"], 4)
        self.assertEqual(p1["summary"]["core_total_count"], 4)
        self.assertEqual(p1["summary"]["limitation_passed_count"], 1)
        self.assertEqual(p1["summary"]["limitation_total_count"], 6)
        p1_sparc = p1["sub_evaluations"]["sparc"]
        self.assertAlmostEqual(p1_sparc["mean_error"], 0.14697319868091122, places=6)
        self.assertEqual(p1_sparc["within_20pct"], 30)
        self.assertEqual(p1_sparc["within_50pct"], 41)

        p2 = result["pathway2"]
        self.assertEqual(p2["status"], "REFUTED")
        self.assertEqual(
            p2["refuted_criteria"],
            ["C1_sign", "C2_lensing", "C3_sparc_btfr", "C4_clock_gap"],
        )
        self.assertEqual(p2["passed_criteria"], [])
        self.assertFalse(p2["variants"]["any_det_native_survivor"])

        comp = result["comparative_summary"]
        self.assertEqual(comp["pathway1"]["status"], "PARTIAL_LIMITATION")
        self.assertEqual(comp["pathway2"]["status"], "REFUTED")
        self.assertTrue(result["verification_invariants"]["consistent_with_expected_verdicts"])

    def test_compact_mode_and_domain_guards(self) -> None:
        compact = kgr.run_all_pathway_evaluations(include_sub_evaluations=False)
        self.assertNotIn("sub_evaluations", compact["pathway1"])
        self.assertIn("sub_evaluation_summary", compact["pathway1"])
        self.assertNotIn("audits", compact["pathway2"])
        self.assertIn("audit_summary", compact["pathway2"])

        for bad_kwargs in (
            {"beta": 1.0},
            {"beta": -0.1},
            {"sigma_crit": 0.0},
            {"sigma_crit": float("nan")},
            {"gas_mode": "invalid_mode"},
            {"w_sfr": True},
        ):
            with self.subTest(bad_kwargs=bad_kwargs):
                with self.assertRaises(ValueError):
                    kgr.run_all_pathway_evaluations(**bad_kwargs)  # type: ignore[arg-type]


class ReentryGatesAndManifestTests(unittest.TestCase):
    def test_reentry_gate_audit_relaxed_vs_strict(self) -> None:
        audit = kgr.reentry_gate_audit()
        self.assertEqual(audit["relaxed_count"], len(audit["relaxed_gates"]))
        self.assertEqual(audit["strict_count"], len(audit["strict_gates_kept"]))
        self.assertGreaterEqual(audit["relaxed_count"], 2)
        self.assertGreaterEqual(audit["strict_count"], 5)

        relaxed_text = json.dumps(audit["relaxed_gates"]).lower()
        strict_text = json.dumps(audit["strict_gates_kept"]).lower()
        self.assertIn("gate 4", relaxed_text)
        self.assertIn("t7", relaxed_text)
        self.assertIn("fully_retired", strict_text)
        self.assertIn("fl-1", strict_text)

        snap = audit["det_falsification_snapshot"]
        self.assertIn("OPEN", snap["gravity_emergence_status"])
        self.assertEqual(snap["claim_register_count"], 4)
        self.assertIn("PR", snap["clock_anomaly_status"])

    def test_combined_closure_manifest_normalization_and_counts(self) -> None:
        manifest = kgr.combined_closure_manifest()
        self.assertEqual(manifest["pathway1_count"], 9)
        self.assertEqual(manifest["pathway2_count"], 10)
        self.assertEqual(manifest["total_entries"], 19)
        self.assertEqual(len(manifest["entries"]), 19)

        self.assertEqual(
            manifest["tag_counts"],
            {
                "TH-DET": 2,
                "P": 1,
                "CORR": 6,
                "FIT": 6,
                "EXTERNAL_ANCHOR": 4,
            },
        )
        self.assertEqual(manifest["native_count"], 3)
        self.assertEqual(manifest["non_native_count"], 16)

        required_keys = {
            "pathway",
            "id",
            "symbol_or_equation",
            "tag",
            "evidence_level",
            "is_native_det",
            "origin_or_source",
            "value_or_equation",
            "units",
            "limitations_or_caveat",
            "native_derivation_opportunity_or_discriminator",
        }
        for entry in manifest["entries"]:
            self.assertEqual(set(entry.keys()), required_keys)
            if entry["tag"] in {"FIT", "CORR", "EXTERNAL_ANCHOR"}:
                self.assertFalse(entry["is_native_det"])
            else:
                self.assertTrue(entry["is_native_det"])

        self.assertEqual(len(manifest["raw_manifests"]["pathway1"]), 9)
        self.assertEqual(len(manifest["raw_manifests"]["pathway2"]), 10)


class CliAndCoreAlignmentTests(unittest.TestCase):
    def test_cli_determinism_and_flags(self) -> None:
        cmd = [sys.executable, "-B", "-m", "det8.models.kappa_gravity_revival"]
        run1 = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        run2 = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(run1.returncode, 0, msg=run1.stderr)
        self.assertEqual(run2.returncode, 0, msg=run2.stderr)
        self.assertEqual(run1.stdout, run2.stdout)

        payload = json.loads(run1.stdout, parse_constant=_reject_nonfinite_json_constant)
        self.assertEqual(payload["comparative_summary"]["pathway1"]["status"], "PARTIAL_LIMITATION")
        self.assertEqual(payload["comparative_summary"]["pathway2"]["status"], "REFUTED")
        self.assertEqual(payload["native_vs_fitted_manifest"]["total_entries"], 19)
        self.assertTrue(payload["verification_invariants"]["consistent_with_expected_verdicts"])

        compact = subprocess.run(
            cmd + ["--compact"], cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(compact.returncode, 0, msg=compact.stderr)
        self.assertEqual(len(compact.stdout.strip().splitlines()), 1)
        compact_payload = json.loads(
            compact.stdout, parse_constant=_reject_nonfinite_json_constant
        )
        self.assertEqual(compact_payload, payload)

        full = subprocess.run(
            cmd + ["--full", "--compact"], cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(full.returncode, 0, msg=full.stderr)
        full_payload = json.loads(
            full.stdout, parse_constant=_reject_nonfinite_json_constant
        )
        self.assertIn("pathway1_evaluation", full_payload)
        self.assertIn("pathway2_evaluation", full_payload)

    def test_core_alignment_and_doc_invariants(self) -> None:
        note = det_falsification.gravity_emergence_note()
        self.assertIn("OPEN", note["status"])
        self.assertIn("revival_track", note)
        self.assertEqual(note["revival_track"]["runner"], "det8.models.kappa_gravity_revival")
        self.assertEqual(len(det_falsification.falsification_ladder()), 3)
        claims = det_falsification.claim_register()
        self.assertEqual(len(claims), 4)
        self.assertIn("PR", claims["clock_anomaly"]["status"])
        self.assertEqual(det8_core.LAMBDA_P, 1.0)
        self.assertEqual(det_units.dimensional_analysis()["G"], (-1, 3, -2))

        for core_path in (
            lgq.__file__,
            det8_core.__file__,
            det_units.__file__,
            det_falsification.__file__,
        ):
            text = Path(core_path).read_text(encoding="utf-8")
            self.assertIn("revival", text.lower(), msg=core_path)
            self.assertIn("kappa_gravity_revival", text, msg=core_path)

        for rel in EXPECTED_DOC_FILES:
            doc_path = REPO_ROOT / rel
            self.assertTrue(doc_path.is_file(), msg=f"Missing doc: {rel}")
            lower = doc_path.read_text(encoding="utf-8").lower()
            self.assertNotIn("pathway 2: viable", lower, msg=rel)
            self.assertNotIn("pathway 2 passed", lower, msg=rel)
            self.assertTrue(
                ("pathway 1" in lower) or ("kappa_t1_contraction" in lower),
                msg=f"Missing Pathway 1 reference in {rel}",
            )
            self.assertTrue(
                ("pathway 2" in lower) or ("pi_conformal_bridge" in lower) or ("conformal" in lower),
                msg=f"Missing Pathway 2 reference in {rel}",
            )


if __name__ == "__main__":
    unittest.main()
