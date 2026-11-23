"""Unified runner, re-entry gate audit, and closure accounting for kappa-gravity revival.

Evaluates both concurrent revival pathways on branch ``revival/kappa-gravity-pathways``:
1. Pathway 1 (``det8.models.kappa_t1_contraction``): T1 Markov kernel contraction
   + reciprocal aperture closure ``G_eff(r) = G / (1 - beta * kappa(r))``,
   expected default verdict ``PARTIAL_LIMITATION``.
2. Pathway 2 (``det8.models.pi_conformal_bridge``): Pi-conformal clock-metric
   bridge ``Delta tau = Pi * Delta N``, ``a = -c^2 grad(ln Pi)``,
   expected verdict ``REFUTED``.

This module never imports any module from ``legacy_gravity_quarantine.FULLY_RETIRED``
and maintains strict separation between DET-native items (``TH-DET`` / ``P``),
conditional correspondences (``CORR``), fitted closures (``FIT``), and external
empirical anchors (``EXTERNAL_ANCHOR``).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Final, Sequence

from det8.models.det_falsification import (
    claim_register,
    data_guardrail,
    gravity_emergence_note,
)
from det8.models.galaxy_observables import (
    KNOWN_GALAXIES,
    OBSERVABLE_PROVENANCE,
    SAMPLE_GALAXIES,
    load_sparc_subset_diagnostic,
)
from det8.models.kappa_t1_contraction import (
    DEFAULT_BETA,
    DEFAULT_DISK_SCALE_HEIGHT_KPC,
    DEFAULT_SIGMA_CRIT,
    closure_manifest as pathway1_closure_manifest,
    evaluate_pathway1_criteria,
)
from det8.models.pi_conformal_bridge import (
    closure_manifest as pathway2_closure_manifest,
    evaluate_pathway2_criteria,
)

PATHWAY1_EXPECTED_DEFAULT_STATUS: Final[str] = "PARTIAL_LIMITATION"
PATHWAY2_EXPECTED_STATUS: Final[str] = "REFUTED"

_VALID_PATHWAY1_STATUSES: Final[frozenset[str]] = frozenset(
    {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION", "REFUTED"}
)
_NATIVE_TAGS: Final[frozenset[str]] = frozenset({"TH-DET", "P"})
_NON_NATIVE_TAGS: Final[frozenset[str]] = frozenset(
    {"CORR", "FIT", "EXTERNAL_ANCHOR"}
)

_PATHWAY2_ENTRY_IDS: Final[tuple[str, ...]] = (
    "p2_m0_event_count_monotonicity",
    "p2_pi_participation_aperture",
    "p2_conformal_acceleration_and_phi",
    "p2_conformal_minkowski_metric",
    "p2_nonconformal_spatial_metric_variant_b",
    "p2_galactic_lambda_p_scale",
    "p2_t1_contraction_and_mond_scales",
    "p2_external_si_and_galaxy_anchors",
    "p2_cassini_vlbi_bounds",
    "p2_clock_product_bounds",
)


def reentry_gate_audit() -> dict[str, object]:
    """Audit which re-entry gates were relaxed vs. kept strict for revival work."""
    emergence_note = gravity_emergence_note()
    claims = claim_register()
    sparc_guardrail = data_guardrail("sparc_rotation_curves")
    eotvos_guardrail = data_guardrail("eotvos_eta")

    relaxed_gates: list[dict[str, str]] = [
        {
            "gate": "Gate 4: strict non-calibration prohibition",
            "source": "docs/CONTINUUM_LIMIT_FRAMEWORK.md §Re-entry gate #4; GOVERNANCE.md §1 (PIM)",
            "disposition": "RELAXED (with explicit FIT/CORR disclosure)",
            "scope_and_conditions": (
                "Permits fitted closures (Sigma_crit = 0.008, w_SFR, beta = 0.93, "
                "G_eff = G / (1 - beta * kappa), galactic lambda_P) for bounded "
                "exploration provided every parameter is tagged FIT/CORR, "
                "degeneracies (e.g. beta = 0.97-0.98) are reported, and native "
                "derivation gaps remain explicitly open."
            ),
        },
        {
            "gate": "T7 full-emergence prerequisite",
            "source": "archive/retired_kappa_gravity.md §Revisit condition; det_falsification.py",
            "disposition": "RELAXED (administrative precondition lifted)",
            "scope_and_conditions": (
                "Lifted as a blocking gate before exploring phenomenological "
                "closures in new modules outside FULLY_RETIRED, without promoting "
                "any FIT/CORR closure to TH-DET or Class-I claim status."
            ),
        },
        {
            "gate": "Concurrent two-pathway exploration",
            "source": "DISPATCH R2; GOVERNANCE.md §1",
            "disposition": "RELAXED (parallel evaluation until quantitative refutation)",
            "scope_and_conditions": (
                "Both Pathway 1 (T1 contraction + reciprocal aperture) and Pathway 2 "
                "(Pi-conformal clock-metric bridge) run under shared empirical anchors; "
                "Pathway 2 is recorded as REFUTED once all four criteria fail."
            ),
        },
    ]

    strict_gates_kept: list[dict[str, str]] = [
        {
            "gate": "Gates 1-3: record provenance, Level-2/3 separation & borrowed assumptions",
            "source": "docs/CONTINUUM_LIMIT_FRAMEWORK.md §Re-entry gate #1-3; docs/observable_anchoring.md",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "Galaxy inputs stay in det8.models.galaxy_observables with "
                "NEUTRAL_DATA_FIXTURE provenance; SI constants and Cassini/VLBI/"
                "MICROSCOPE/Eot-Wash/NIST bounds are tagged EXTERNAL_ANCHOR; "
                "Freeman disks and Newtonian kinematics are tagged CORR."
            ),
        },
        {
            "gate": "Gate 5: quantitative EP, conservation, covariance & SPARC checks",
            "source": "docs/CONTINUUM_LIMIT_FRAMEWORK.md §Re-entry gate #5",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "Executable thresholds govern both pathways: Pathway 1 yields "
                "PARTIAL_LIMITATION (4/4 core gates pass; 5/6 limitations open "
                "including Keplerian r^(-1/2) turnover and unclosed covariant lensing); "
                "Pathway 2 triggers REFUTED across C1_sign..C4_clock_gap."
            ),
        },
        {
            "gate": "Gate 6: pre-registered falsifiers & Novelty Ledger cost-if-null",
            "source": "docs/CONTINUUM_LIMIT_FRAMEWORK.md §Re-entry gate #6; FALSIFICATION_LEDGER.md; NOVELTY_LEDGER.md",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "Pre-registered quantitative falsifiers and null costs govern both "
                "pathways; Pathway 2 is logged as a null/refuted probe without "
                "erasing FL-1 or distorting the 5-entry DG-WARRANT baseline."
            ),
        },
        {
            "gate": "AST quarantine isolation (len(FULLY_RETIRED) == 28)",
            "source": "det8/models/legacy_gravity_quarantine.py; run_tests.py",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "Zero imports from FULLY_RETIRED in active det8/models/*.py; "
                "no legacy gravity module is un-retired or modified."
            ),
        },
        {
            "gate": "Option B Claim Register, FL-1 Rank Separation & Anti-Agency",
            "source": "det8/models/det_falsification.py; GOVERNANCE.md §2 & §4",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "det_falsification.claim_register() keeps clock_anomaly (PR) "
                "distinct from gravity_emergence (OPEN frontier); FL-1 requires "
                "rank r > 1 separation between kappa_env and kappa_dev; zero "
                "agency variables are permitted."
            ),
        },
        {
            "gate": "sparc_subset.json guardrail & PARTIAL_QUARANTINE product caveat",
            "source": "det8/models/galaxy_observables.py; det8/models/experimental_constraints.py",
            "disposition": "KEPT STRICT",
            "enforcement": (
                "det8/data/sparc_subset.json (56 records, # comments, M_gas == M_star, "
                "12 V_flat == 0.0) is audited diagnostically rather than fitted; "
                "NIST/PTB and GPS clock limits remain lambda_P * Delta kappa "
                "product bounds."
            ),
        },
    ]

    return {
        "relaxed_gates": relaxed_gates,
        "strict_gates_kept": strict_gates_kept,
        "relaxed_count": len(relaxed_gates),
        "strict_count": len(strict_gates_kept),
        "det_falsification_snapshot": {
            "gravity_emergence_status": emergence_note.get("status"),
            "gravity_emergence_note": emergence_note,
            "claim_register_keys": sorted(claims.keys()),
            "claim_register_count": len(claims),
            "clock_anomaly_status": claims.get("clock_anomaly", {}).get("status"),
            "gravity_claim_status": claims.get("gravity_emergence", {}).get("status"),
            "data_guardrails": {
                "sparc_rotation_curves": sparc_guardrail,
                "eotvos_eta": eotvos_guardrail,
            },
        },
    }


def combined_closure_manifest() -> dict[str, object]:
    """Normalize Pathway 1 (9 entries) and Pathway 2 (10 entries) manifests into 19 entries."""
    p1_raw = list(pathway1_closure_manifest())
    p2_raw = list(pathway2_closure_manifest())

    normalized: list[dict[str, object]] = []

    for entry in p1_raw:
        tag = str(entry["tag"])
        is_native = bool(entry["is_native_det"])
        if tag in _NATIVE_TAGS and not is_native:
            raise ValueError(f"Pathway 1 native tag {tag!r} must have is_native_det=True")
        if tag in _NON_NATIVE_TAGS and is_native:
            raise ValueError(f"Pathway 1 non-native tag {tag!r} cannot be marked native")
        normalized.append(
            {
                "pathway": "pathway1",
                "id": str(entry["id"]),
                "symbol_or_equation": str(entry["symbol_or_equation"]),
                "tag": tag,
                "evidence_level": str(entry["anchoring_level"]),
                "is_native_det": is_native,
                "origin_or_source": str(entry["calibration_dataset_or_source"]),
                "value_or_equation": entry["value_or_domain"],
                "units": str(entry["units"]),
                "limitations_or_caveat": str(entry["known_limitations_or_gaps"]),
                "native_derivation_opportunity_or_discriminator": str(
                    entry["native_derivation_opportunity"]
                ),
            }
        )

    for idx, entry in enumerate(p2_raw):
        tag = str(entry["epistemic_tag"])
        if tag not in (_NATIVE_TAGS | _NON_NATIVE_TAGS):
            raise ValueError(f"Unexpected Pathway 2 epistemic tag: {tag!r}")
        entry_id = (
            _PATHWAY2_ENTRY_IDS[idx]
            if idx < len(_PATHWAY2_ENTRY_IDS)
            else f"p2_entry_{idx + 1:02d}"
        )
        is_native = tag in _NATIVE_TAGS
        normalized.append(
            {
                "pathway": "pathway2",
                "id": entry_id,
                "symbol_or_equation": str(entry["symbol_or_relation"]),
                "tag": tag,
                "evidence_level": str(entry["evidence_level"]),
                "is_native_det": is_native,
                "origin_or_source": str(entry["origin"]),
                "value_or_equation": entry["equation_or_value"],
                "units": "context-dependent",
                "limitations_or_caveat": str(entry["status_m_or_caveat"]),
                "native_derivation_opportunity_or_discriminator": str(
                    entry["independent_discriminator"]
                ),
            }
        )

    all_tags = ("TH-DET", "P", "CORR", "FIT", "EXTERNAL_ANCHOR")
    tag_counts: dict[str, int] = {
        tag: sum(1 for item in normalized if item["tag"] == tag) for tag in all_tags
    }
    by_pathway_tag_counts: dict[str, dict[str, int]] = {
        "pathway1": {
            tag: sum(
                1
                for item in normalized
                if item["pathway"] == "pathway1" and item["tag"] == tag
            )
            for tag in all_tags
        },
        "pathway2": {
            tag: sum(
                1
                for item in normalized
                if item["pathway"] == "pathway2" and item["tag"] == tag
            )
            for tag in all_tags
        },
    }

    native_count = sum(1 for item in normalized if bool(item["is_native_det"]))
    non_native_count = len(normalized) - native_count

    return {
        "entries": normalized,
        "total_entries": len(normalized),
        "pathway1_count": len(p1_raw),
        "pathway2_count": len(p2_raw),
        "tag_counts": tag_counts,
        "by_pathway_tag_counts": by_pathway_tag_counts,
        "native_count": native_count,
        "non_native_count": non_native_count,
        "raw_manifests": {
            "pathway1": p1_raw,
            "pathway2": p2_raw,
        },
    }


def _strip_bulky_pathway1(p1_result: dict[str, object]) -> dict[str, object]:
    """Return a copy of Pathway 1 evaluation without per-galaxy sub_evaluations."""
    compact = {k: v for k, v in p1_result.items() if k != "sub_evaluations"}
    sub_eval = p1_result.get("sub_evaluations")
    if isinstance(sub_eval, dict):
        f6 = sub_eval.get("f6", {})
        sparc = sub_eval.get("sparc", {})
        asym = sub_eval.get("asymptotics", {})
        screen = sub_eval.get("screening", {})
        compact["sub_evaluation_summary"] = {
            "f6": {
                "n_increasing": f6.get("n_increasing"),
                "n_total": f6.get("n_total"),
                "all_increasing": f6.get("all_increasing"),
                "all_monotonic": f6.get("all_monotonic"),
            },
            "sparc": {
                "n_galaxies": sparc.get("n_galaxies"),
                "gas_mode": sparc.get("gas_mode"),
                "mean_error": sparc.get("mean_error"),
                "median_error": sparc.get("median_error"),
                "within_20pct": sparc.get("within_20pct"),
                "within_50pct": sparc.get("within_50pct"),
                "within_20_fraction": sparc.get("within_20_fraction"),
                "max_enhancement": sparc.get("max_enhancement"),
                "mass_bins": sparc.get("mass_bins"),
                "known_galaxies_comparison": sparc.get("known_galaxies_comparison"),
            },
            "asymptotics": {
                "regime_summaries": asym.get("regime_summaries"),
            },
            "screening": {
                "rho_crit_kg_m3": screen.get("rho_crit_kg_m3"),
                "regimes": screen.get("regimes"),
                "differential_eotvos": screen.get("differential_eotvos"),
                "fl1_rank_separation": screen.get("fl1_rank_separation"),
            },
        }
    return compact


def _strip_bulky_pathway2(p2_result: dict[str, object]) -> dict[str, object]:
    """Return a copy of Pathway 2 evaluation without per-galaxy audit arrays."""
    compact = {k: v for k, v in p2_result.items() if k != "audits"}
    audits = p2_result.get("audits")
    if isinstance(audits, dict):
        sign = audits.get("sign_consistency", {})
        lensing = audits.get("conformal_ppn_lensing", {})
        sparc = audits.get("sparc_mass_scaling", {})
        clock = audits.get("clock_scale_gap", {})
        compact["audit_summary"] = {
            "sign_consistency": {
                "passed": sign.get("passed"),
                "t1_repulsive_count": sign.get("t1_repulsive_count"),
                "f6_attractive_count": sign.get("f6_attractive_count"),
                "f6_reintroduces_inside_out_failure": sign.get(
                    "f6_reintroduces_inside_out_failure"
                ),
            },
            "conformal_ppn_lensing": {
                "passed": lensing.get("passed"),
                "gamma_ppn": lensing.get("gamma_ppn"),
                "deflection_factor": lensing.get("deflection_factor"),
                "abs_gamma_minus_one": lensing.get("abs_gamma_minus_one"),
                "cassini_violation_ratio": lensing.get("cassini_violation_ratio"),
                "vlbi_fractional_miss": lensing.get("vlbi_fractional_miss"),
            },
            "sparc_mass_scaling": {
                "passed": sparc.get("passed"),
                "v2_over_c2_dynamic_range": sparc.get("v2_over_c2_dynamic_range"),
                "unbound_literal_count": sparc.get("unbound_literal_count"),
                "best_sign_flipped_mean_error": sparc.get("best_sign_flipped_mean_error"),
            },
            "clock_scale_gap": {
                "passed": clock.get("passed"),
                "galactic_lambda_p": clock.get("galactic_lambda_p"),
                "nist_clock_bound": clock.get("nist_clock_bound"),
                "nist_gap_ratio": clock.get("nist_gap_ratio"),
                "gps_gap_ratio": clock.get("gps_gap_ratio"),
                "lab_acceleration_m_s2": clock.get("lab_acceleration_m_s2"),
            },
        }
    return compact


def run_all_pathway_evaluations(
    *,
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    w_sfr: float = 0.0,
    gas_mode: str = "1d",
    scale_height_kpc: float = DEFAULT_DISK_SCALE_HEIGHT_KPC,
    include_sub_evaluations: bool = True,
) -> dict[str, object]:
    """Execute unified Pathway 1, Pathway 2, dataset, gate, and manifest evaluations."""
    sparc_diag = load_sparc_subset_diagnostic()
    p1_full = evaluate_pathway1_criteria(
        sigma_crit=sigma_crit,
        beta=beta,
        w_sfr=w_sfr,
        gas_mode=gas_mode,
        scale_height_kpc=scale_height_kpc,
    )
    p2_full = evaluate_pathway2_criteria()
    gates = reentry_gate_audit()
    manifest = combined_closure_manifest()

    p1_sub = p1_full["sub_evaluations"]
    p1_f6 = p1_sub["f6"]
    p1_sparc = p1_sub["sparc"]
    p1_asym = p1_sub["asymptotics"]
    p1_screen = p1_sub["screening"]

    p2_audits = p2_full["audits"]
    p2_lensing = p2_audits["conformal_ppn_lensing"]
    p2_sparc = p2_audits["sparc_mass_scaling"]
    p2_clock = p2_audits["clock_scale_gap"]
    p2_variants = p2_full["variants"]

    is_default_params = (
        math.isclose(float(p1_full["parameters"]["sigma_crit"]), DEFAULT_SIGMA_CRIT, rel_tol=0.0, abs_tol=1e-15)
        and math.isclose(float(p1_full["parameters"]["beta"]), DEFAULT_BETA, rel_tol=0.0, abs_tol=1e-15)
        and math.isclose(float(p1_full["parameters"]["w_sfr"]), 0.0, rel_tol=0.0, abs_tol=1e-15)
        and str(p1_full["parameters"]["gas_mode"]) == "1d"
        and math.isclose(
            float(p1_full["parameters"]["scale_height_kpc"]),
            DEFAULT_DISK_SCALE_HEIGHT_KPC,
            rel_tol=0.0,
            abs_tol=1e-15,
        )
    )

    p1_status = str(p1_full["status"])
    p2_status = str(p2_full["status"])

    p1_status_matches = (
        p1_status == PATHWAY1_EXPECTED_DEFAULT_STATUS
        if is_default_params
        else p1_status in _VALID_PATHWAY1_STATUSES
    )
    p2_status_matches = p2_status == PATHWAY2_EXPECTED_STATUS
    no_p2_survivor = not bool(p2_variants["any_det_native_survivor"])
    manifest_counts_valid = (
        manifest["total_entries"] == 19
        and manifest["pathway1_count"] == 9
        and manifest["pathway2_count"] == 10
        and manifest["native_count"] == 3
        and manifest["non_native_count"] == 16
    )
    sparc_diag_ok = bool(sparc_diag["parsed_ok"]) and sparc_diag["record_count"] == 56

    consistent = bool(
        p1_status_matches
        and p2_status_matches
        and no_p2_survivor
        and manifest_counts_valid
        and sparc_diag_ok
    )

    comparative_summary: dict[str, object] = {
        "pathway1": {
            "module": "det8.models.kappa_t1_contraction",
            "status": p1_status,
            "core_passed": p1_full["summary"]["core_passed_count"],
            "core_total": p1_full["summary"]["core_total_count"],
            "limitation_passed": p1_full["summary"]["limitation_passed_count"],
            "limitation_total": p1_full["summary"]["limitation_total_count"],
            "f6_increasing": f"{p1_f6['n_increasing']}/{p1_f6['n_total']}",
            "sparc_mean_error": p1_sparc["mean_error"],
            "sparc_within_20pct": p1_sparc["within_20pct"],
            "sparc_within_50pct": p1_sparc["within_50pct"],
            "sparc_max_enhancement": p1_sparc["max_enhancement"],
            "outer_2_to_4_rmax_mean_slope": p1_asym["regime_summaries"][
                "outer_2_to_4_rmax"
            ]["mean_slope"],
            "exponential_1au_solar_wind_passes": p1_screen["regimes"][
                "local_1au_solar_wind"
            ]["exponential"]["passes_bound"],
            "power_law_1au_solar_wind_passes": p1_screen["regimes"][
                "local_1au_solar_wind"
            ]["power_law"]["passes_bound"],
            "fl1_requires_rank_r_gt_1": p1_screen["fl1_rank_separation"][
                "requires_rank_r_gt_1_separation"
            ],
            "open_limitations": p1_full["open_limitations"],
        },
        "pathway2": {
            "module": "det8.models.pi_conformal_bridge",
            "status": p2_status,
            "refuted_criteria": p2_full["refuted_criteria"],
            "passed_criteria": p2_full["passed_criteria"],
            "gamma_ppn": p2_lensing["gamma_ppn"],
            "cassini_violation_ratio": p2_lensing["cassini_violation_ratio"],
            "sparc_v2_over_c2_dynamic_range": p2_sparc["v2_over_c2_dynamic_range"],
            "sparc_unbound_literal_count": p2_sparc["unbound_literal_count"],
            "sparc_best_sign_flipped_mean_error": p2_sparc[
                "best_sign_flipped_mean_error"
            ],
            "nist_gap_ratio": p2_clock["nist_gap_ratio"],
            "gps_gap_ratio": p2_clock["gps_gap_ratio"],
            "any_det_native_survivor": p2_variants["any_det_native_survivor"],
            "survivor_conditions": p2_full["survivor_conditions"],
        },
    }

    pathway1_out = p1_full if include_sub_evaluations else _strip_bulky_pathway1(p1_full)
    pathway2_out = p2_full if include_sub_evaluations else _strip_bulky_pathway2(p2_full)

    return {
        "branch": "revival/kappa-gravity-pathways",
        "observables_and_datasets": {
            "module": "det8.models.galaxy_observables",
            "known_galaxies_count": len(KNOWN_GALAXIES),
            "sample_galaxies_count": len(SAMPLE_GALAXIES),
            "provenance": dict(OBSERVABLE_PROVENANCE),
            "sparc_subset_diagnostic": sparc_diag,
        },
        "pathway1": pathway1_out,
        "pathway2": pathway2_out,
        "reentry_gates": gates,
        "closure_manifest": manifest,
        "comparative_summary": comparative_summary,
        "verification_invariants": {
            "is_default_parameter_set": is_default_params,
            "sparc_subset_parsed_ok": sparc_diag_ok,
            "pathway1_status_matches": p1_status_matches,
            "pathway2_status_matches": p2_status_matches,
            "no_pathway2_native_survivor": no_p2_survivor,
            "closure_manifest_counts_valid": manifest_counts_valid,
            "consistent_with_expected_verdicts": consistent,
        },
    }


def build_cli_summary(
    evaluation: dict[str, object],
    *,
    include_details: bool = False,
) -> dict[str, object]:
    """Build a deterministic, JSON-serializable summary from a unified evaluation."""
    obs = evaluation["observables_and_datasets"]
    sparc_diag = obs["sparc_subset_diagnostic"]
    manifest = evaluation["closure_manifest"]
    gates = evaluation["reentry_gates"]

    summary: dict[str, object] = {
        "branch": evaluation["branch"],
        "datasets": {
            "known_galaxies_count": obs["known_galaxies_count"],
            "sample_galaxies_count": obs["sample_galaxies_count"],
            "provenance_claim_status": obs["provenance"]["det_claim_status"],
            "sparc_subset": {
                "parsed_ok": sparc_diag["parsed_ok"],
                "raw_json_valid": sparc_diag["raw_json_valid"],
                "parse_mode": sparc_diag["parse_mode"],
                "record_count": sparc_diag["record_count"],
                "anomalies": sparc_diag["anomalies"],
                "cross_comparison": sparc_diag["cross_comparison"],
            },
        },
        "comparative_summary": evaluation["comparative_summary"],
        "reentry_gates": {
            "relaxed_count": gates["relaxed_count"],
            "strict_count": gates["strict_count"],
            "relaxed_gates": gates["relaxed_gates"],
            "strict_gates_kept": gates["strict_gates_kept"],
            "det_falsification_snapshot": gates["det_falsification_snapshot"],
        },
        "native_vs_fitted_manifest": {
            "total_entries": manifest["total_entries"],
            "pathway1_count": manifest["pathway1_count"],
            "pathway2_count": manifest["pathway2_count"],
            "native_count": manifest["native_count"],
            "non_native_count": manifest["non_native_count"],
            "tag_counts": manifest["tag_counts"],
            "by_pathway_tag_counts": manifest["by_pathway_tag_counts"],
            "entries": manifest["entries"],
        },
        "verification_invariants": evaluation["verification_invariants"],
    }
    if include_details:
        summary["pathway1_evaluation"] = evaluation["pathway1"]
        summary["pathway2_evaluation"] = evaluation["pathway2"]
    return summary


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="det8.models.kappa_gravity_revival",
        description=(
            "Run concurrent Pathway 1 and Pathway 2 kappa-gravity revival evaluations "
            "and emit deterministic JSON summary."
        ),
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include full per-galaxy Pathway 1 and Pathway 2 diagnostic payloads.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit single-line compact JSON instead of pretty-printed JSON.",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point printing reproducible JSON summary and exiting 0 when consistent."""
    args = _parse_args(argv)
    evaluation = run_all_pathway_evaluations(include_sub_evaluations=bool(args.full))
    summary = build_cli_summary(evaluation, include_details=bool(args.full))
    print(
        json.dumps(
            summary,
            indent=None if args.compact else 2,
            sort_keys=True,
            allow_nan=False,
        )
    )
    consistent = bool(
        evaluation["verification_invariants"]["consistent_with_expected_verdicts"]
    )
    return 0 if consistent else 1


__all__ = (
    "PATHWAY1_EXPECTED_DEFAULT_STATUS",
    "PATHWAY2_EXPECTED_STATUS",
    "build_cli_summary",
    "combined_closure_manifest",
    "main",
    "reentry_gate_audit",
    "run_all_pathway_evaluations",
)


if __name__ == "__main__":
    sys.exit(main())
