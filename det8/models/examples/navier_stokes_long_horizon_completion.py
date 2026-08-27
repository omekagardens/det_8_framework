"""Governed completion of the phase-two Navier--Stokes long-horizon branch.

The phase-two ``N=48, nu=0.01, T=1.25`` result was admitted, but its matched
``N=40`` member failed the spectral-tail gate and no timestep check existed.
This module freezes the next three actions before execution:

1. reproduce the exact phase-two ``N=48`` anchor;
2. extend the same action to ``N=56``; and
3. run ``N=48`` with half the timestep cap only if the anchor reproduces and
   every declared ``48 -> 56`` spatial-transport gate passes.

The selected observation is spatially checked at N=56 while temporal
stability is checked at N=48.  This is not timestep convergence at N=56 and
does not complete a full spatiotemporal convergence rectangle.  All outputs
remain bounded development numerics with no replication, RG2, singularity,
regularity, posterior, or proof claim.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Sequence

from det8.models.relational_evidence import (
    EvidenceLedger,
    EvidenceRecord,
    evidence_payload_digest,
)
from det8.models.examples.navier_stokes_near_singularity import (
    PROOF_WARNING,
    SpectralRunConfig,
    compare_resolution_pair,
    compare_timestep_pair,
)
from det8.models.examples.navier_stokes_relational_discovery import (
    DISCOVERY_WARNING,
    prepare_discovery_protocol,
    ret_bundle_reports,
    run_relational_discovery,
)


SCHEMA_VERSION = "navier-stokes-long-horizon-completion-v1"
PRIOR_FINDINGS_DIGEST = (
    "a233a6bae2df47212aacb62290304c1cc01981e83b9ff8b427170ccd81f2f095"
)
ANCHOR_CONFIGURATION_DIGEST = (
    "2b5145f36fd7bf701e2c0981e0ff026cb358a62ae6dbb2e3d54b18ce07c0f55f"
)
ANCHOR_NUMERICAL_RUN_DIGEST = (
    "b717450dddc08b4971f69ae9e9ec8411798d1877fb8577b803ee7f209b98af0d"
)
EXPECTED_N56_CONFIGURATION_DIGEST = (
    "7d0b6aa0a3b9d68be38ea329e7359149433fc21e22daaa747f0ae316ae47f753"
)
EXPECTED_FINE_N48_CONFIGURATION_DIGEST = (
    "b32d1ae1ab803c47818ce1614a687b6f8039558d4f337fb0a26e392eaa92175a"
)
PRIOR_FINDINGS_PATH = (
    Path(__file__).resolve().parents[2]
    / "data/navier_stokes_phase_two_findings_2026-08-26.json"
)

COMPLETION_WARNING = (
    "A successful phase-three bundle gives N=56 spatial transport with "
    "timestep stability checked at N=48. It is not N=56 timestep convergence, "
    "a complete spatiotemporal convergence rectangle, an independent "
    "replication, or evidence of singularity or regularity."
)


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_prior_findings() -> dict[str, object]:
    """Load and verify the immutable phase-two parent record."""

    findings = json.loads(PRIOR_FINDINGS_PATH.read_text())
    recorded = str(findings.pop("findings_digest"))
    computed = evidence_payload_digest(findings)
    if recorded != PRIOR_FINDINGS_DIGEST or computed != PRIOR_FINDINGS_DIGEST:
        raise RuntimeError("phase-two parent findings digest does not verify")
    findings["findings_digest"] = recorded
    return findings


def long_horizon_actions() -> tuple[SpectralRunConfig, ...]:
    """Return the anchor, N=56 extension, and frozen conditional time check."""

    common = {
        "initial_condition": "random_low_mode",
        "viscosity": 0.01,
        "final_time": 1.25,
        "amplitude": 1.0,
        "cfl": 0.35,
        "sample_interval": 0.025,
        "maximum_steps": 100_000,
        "seed": 20260826,
    }
    anchor = SpectralRunConfig(
        resolution=48,
        maximum_dt=0.00375,
        role="phase_two_underresolved_spatial_recovery",
        **common,
    )
    extension = SpectralRunConfig(
        resolution=56,
        maximum_dt=0.00375,
        role="phase_three_resolution_transport",
        **common,
    )
    fine = SpectralRunConfig(
        resolution=48,
        maximum_dt=0.001875,
        role="phase_three_timestep_transport",
        **common,
    )
    if anchor.digest != ANCHOR_CONFIGURATION_DIGEST:
        raise RuntimeError("phase-three anchor configuration drifted")
    if extension.digest != EXPECTED_N56_CONFIGURATION_DIGEST:
        raise RuntimeError("phase-three N=56 configuration drifted")
    if fine.digest != EXPECTED_FINE_N48_CONFIGURATION_DIGEST:
        raise RuntimeError("phase-three fine N=48 configuration drifted")
    return anchor, extension, fine


def runtime_metadata() -> dict[str, object]:
    """Return implementation and numerical-runtime provenance."""

    try:
        import numpy
    except ImportError:
        numpy_version = "unavailable"
    else:
        numpy_version = numpy.__version__

    from det8.models.examples import navier_stokes_near_singularity as solver_module
    from det8.models.examples import navier_stokes_relational_discovery as discovery_module

    return {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "numpy_version": numpy_version,
        "solver_implementation_sha256": _file_sha256(Path(solver_module.__file__)),
        "discovery_implementation_sha256": _file_sha256(
            Path(discovery_module.__file__)
        ),
        "completion_implementation_sha256": _file_sha256(Path(__file__)),
    }


def prepare_long_horizon_protocol() -> dict[str, object]:
    """Freeze all actions and the literal conditional predicate before running."""

    prior = load_prior_findings()
    anchor, extension, fine = long_horizon_actions()
    discovery_protocol = prepare_discovery_protocol((anchor, extension, fine))
    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "parent_findings_digest": PRIOR_FINDINGS_DIGEST,
        "parent_suite_digest": prior["suite_digest"],
        "selection_consumed_parent_outcomes": True,
        "actions_frozen_before_phase_three": tuple(
            asdict(config) for config in (anchor, extension, fine)
        ),
        "action_digests": tuple(
            config.digest for config in (anchor, extension, fine)
        ),
        "anchor_expected_numerical_run_digest": ANCHOR_NUMERICAL_RUN_DIGEST,
        "discovery_protocol": discovery_protocol,
        "conditional_action_digest": fine.digest,
        "conditional_predicate": (
            "execute fine N=48 iff the anchor numerical run digest reproduces "
            "and the matched N=48->56 compare_resolution_pair transport passes"
        ),
        "spatial_match_requirements": {
            "maximum_dt_equal": True,
            "cfl_equal": True,
            "sample_interval_equal": True,
            "maximum_steps_equal": True,
        },
        "timestep_match_requirements": {
            "exact_cap_ratio_coarse_to_fine": 2.0,
            "resolution": 48,
        },
        "conditional_trigger_uses_det_features": False,
        "conditional_trigger_uses_lps_shape": False,
        "conditional_trigger_uses_growth_model_score": False,
        "historically_fresh_confirmation": False,
        "independent_replication": False,
        "rg2_evaluation_authorized": False,
        "posterior_model_probabilities_authorized": False,
        "formal_singularity_claim": False,
        "global_regularity_claim": False,
        "proof_language_allowed": False,
        "runtime_and_implementation": runtime_metadata(),
        "warning": COMPLETION_WARNING,
    }
    manifest["manifest_digest"] = evidence_payload_digest(manifest)
    return manifest


def compare_matched_resolution_pair(
    lower: Mapping[str, object], higher: Mapping[str, object]
) -> dict[str, object]:
    """Require a one-axis spatial intervention before core comparison."""

    lower_config = lower["configuration"]
    higher_config = higher["configuration"]
    for field in ("maximum_dt", "cfl", "sample_interval", "maximum_steps"):
        if lower_config[field] != higher_config[field]:
            raise ValueError(f"spatial transport requires matched {field}")
    comparison = compare_resolution_pair(lower, higher)
    return {
        "matched_maximum_dt": lower_config["maximum_dt"],
        "matched_cfl": lower_config["cfl"],
        "matched_sample_interval": lower_config["sample_interval"],
        **comparison,
    }


def compare_exact_timestep_pair(
    coarser: Mapping[str, object], finer: Mapping[str, object]
) -> dict[str, object]:
    """Require the predeclared exact two-to-one cap intervention."""

    coarse_dt = float(coarser["configuration"]["maximum_dt"])
    fine_dt = float(finer["configuration"]["maximum_dt"])
    if not math.isclose(coarse_dt, 2.0 * fine_dt, rel_tol=0.0, abs_tol=1.0e-15):
        raise ValueError("phase-three timestep comparison requires an exact 2:1 cap")
    comparison = compare_timestep_pair(coarser, finer)
    return {
        "declared_cap_ratio": coarse_dt / fine_dt,
        "coarse_step_count": coarser["step_count"],
        "fine_step_count": finer["step_count"],
        "fine_run_used_more_steps": int(finer["step_count"])
        > int(coarser["step_count"]),
        **comparison,
    }


def conditional_timestep_authorized(
    *, anchor_reproduced: bool, resolution_comparison: Mapping[str, object]
) -> bool:
    """Apply only the frozen numerical trigger for the conditional run."""

    return bool(anchor_reproduced and resolution_comparison["transport_passed"])


def _compact_run(discovery: Mapping[str, object]) -> dict[str, object]:
    result = discovery["numerical_result"]
    snapshots = discovery["relational_snapshots"]
    growth = discovery["ret_layer"]["growth_model_comparison"]
    graph = discovery["det_layer"]["intense_vorticity_feature_graph"]
    l9_initial = float(snapshots[0]["velocity_lq_norms"]["9"])
    l9_final = float(snapshots[-1]["velocity_lq_norms"]["9"])
    return {
        "role": discovery["configuration"]["role"],
        "configuration_digest": discovery["configuration_digest"],
        "resolution": discovery["configuration"]["resolution"],
        "maximum_dt": discovery["configuration"]["maximum_dt"],
        "step_count": result["step_count"],
        "sample_count": result["sample_count"],
        "state": result["numerical_admission"]["state"],
        "numerical_gates": result["numerical_admission"]["numerical_gates"],
        "vorticity_amplification": result["vorticity_amplification"],
        "enstrophy_amplification": result["enstrophy_amplification"],
        "palinstrophy_amplification": result["palinstrophy_amplification"],
        "peak_high_wavenumber_energy_fraction": result["maxima"][
            "high_wavenumber_energy_fraction"
        ],
        "energy_balance_relative_defect": result["energy_balance"][
            "relative_defect"
        ],
        "enstrophy_balance_relative_defect": result["enstrophy_balance"][
            "sample_trapezoid_relative_defect"
        ],
        "initial_normalized_mean_l9": l9_initial,
        "final_to_initial_l9_ratio": l9_final / max(l9_initial, 1.0e-300),
        "q9_phi_normalized_mean_norm": discovery["lps_diagnostics"][
            "q_greater_than_3"
        ]["9"]["normalized_mean_norm_time_average_phi"],
        "best_growth_model": growth["best_declared_model"],
        "best_model_including_open": growth["best_model_including_open"],
        "growth_mean_score_margin": growth["best_declared_mean_score_margin"],
        "feature_graph_event_counts": graph["event_counts"],
        "run_digest": result["run_digest"],
        "discovery_digest": discovery["discovery_digest"],
    }


def _long_horizon_evidence_ledger(
    discoveries: Sequence[Mapping[str, object]],
    resolution_comparison: Mapping[str, object],
    timestep_comparison: Mapping[str, object],
    prior: Mapping[str, object],
    protocol: Mapping[str, object],
) -> tuple[EvidenceLedger, dict[str, object]]:
    """Commit one source-deduplicated record for the full consumed lineage."""

    reports = ret_bundle_reports(discoveries)
    if len(reports) != 1 or not reports[0]["eligible_for_ret_ledger"]:
        raise RuntimeError("long-horizon bundle is not eligible for RET commitment")
    selected = max(
        discoveries, key=lambda item: int(item["configuration"]["resolution"])
    )
    selected_result = selected["numerical_result"]
    prior_horizon = next(
        row for row in prior["runs"] if row["role"] == "phase_two_horizon_scout"
    )
    all_amplifications = [
        float(prior_horizon["vorticity_amplification"]),
        *(
            float(item["numerical_result"]["vorticity_amplification"])
            for item in discoveries
        ),
    ]
    observation = math.log(float(selected_result["vorticity_amplification"]))
    numerical_uncertainty = max(
        abs(math.log(value) - observation) for value in all_amplifications
    )
    source_run_digests = {
        str(prior_horizon["run_digest"]),
        *(str(item["numerical_result"]["run_digest"]) for item in discoveries),
    }
    lineage_digest = str(prior["provisional_long_horizon_bundle"]["lineage_digest"])
    record = EvidenceRecord(
        record_id=f"ns-det-ret-long-horizon-{lineage_digest[:12]}",
        source_ids=tuple(f"ns-run-{digest}" for digest in sorted(source_run_digests)),
        action="navier_stokes_long_horizon_completion_bundle",
        coordinate=None,
        digest=evidence_payload_digest(observation),
        family="navier_stokes_log_peak_vorticity_amplification",
        scope=(
            "transported_bounded_development_with_N56_spatial_and_"
            "N48_temporal_stability"
        ),
        observation=observation,
        metadata={
            "parent_findings_digest": PRIOR_FINDINGS_DIGEST,
            "protocol_digest": protocol["manifest_digest"],
            "selected_observation_resolution": 56,
            "timestep_check_resolution": 48,
            "spatiotemporal_convergence_rectangle_complete": False,
            "resolution_transport": resolution_comparison,
            "timestep_transport": timestep_comparison,
            "numerical_uncertainty_log_scale": numerical_uncertainty,
            "selected_feature_graph_digest": selected["det_layer"][
                "intense_vorticity_feature_graph"
            ]["graph_digest"],
            "selected_growth_score_digest": selected["ret_layer"][
                "growth_model_comparison"
            ]["score_digest"],
            "counts_as_replication": False,
            "historically_fresh": False,
            "ret_model_calibration_required": True,
            "posterior_model_probabilities_authorized": False,
            "formal_singularity_claim": False,
        },
        joint=True,
    )
    ledger = EvidenceLedger((record,))
    return ledger, {
        "lineage_digest": lineage_digest,
        "observation_log_peak_vorticity_amplification": observation,
        "numerical_uncertainty_log_scale": numerical_uncertainty,
        "selected_observation_resolution": 56,
        "timestep_check_resolution": 48,
        "spatiotemporal_convergence_rectangle_complete": False,
    }


def run_long_horizon_completion(
    *, execute_conditional_timestep: bool = True
) -> dict[str, object]:
    """Run the frozen resolution stage and its governed conditional time check."""

    prior = load_prior_findings()
    protocol = prepare_long_horizon_protocol()
    discovery_protocol = protocol["discovery_protocol"]
    anchor_config, extension_config, fine_config = long_horizon_actions()

    anchor = run_relational_discovery(anchor_config, protocol=discovery_protocol)
    anchor_result = anchor["numerical_result"]
    anchor_reproduced = bool(
        anchor_result["run_digest"] == ANCHOR_NUMERICAL_RUN_DIGEST
        and int(anchor_result["sample_count"]) == 51
        and math.isclose(
            float(anchor_result["final"]["time"]), 1.25, rel_tol=0.0, abs_tol=1.0e-12
        )
    )
    if not anchor_reproduced:
        raise RuntimeError("phase-three N=48 anchor failed exact reproduction")

    extension = run_relational_discovery(
        extension_config, protocol=discovery_protocol
    )
    resolution_comparison = compare_matched_resolution_pair(
        anchor_result, extension["numerical_result"]
    )
    authorized = conditional_timestep_authorized(
        anchor_reproduced=anchor_reproduced,
        resolution_comparison=resolution_comparison,
    )
    fine = None
    timestep_comparison = None
    skip_reason = None
    if authorized and execute_conditional_timestep:
        fine = run_relational_discovery(fine_config, protocol=discovery_protocol)
        timestep_comparison = compare_exact_timestep_pair(
            anchor_result, fine["numerical_result"]
        )
    elif not authorized:
        skip_reason = "N=48 anchor or N=48->56 spatial transport gate failed"
    else:
        skip_reason = "conditional timestep execution disabled by caller"

    discoveries = (anchor, extension) + ((fine,) if fine is not None else ())
    ledger = EvidenceLedger()
    evidence_summary = None
    if (
        authorized
        and timestep_comparison is not None
        and bool(timestep_comparison["transport_passed"])
    ):
        ledger, evidence_summary = _long_horizon_evidence_ledger(
            discoveries,
            resolution_comparison,
            timestep_comparison,
            prior,
            protocol,
        )
        state = (
            "TRANSPORTED_LONG_HORIZON_DEVELOPMENT_BUNDLE_REQUIRES_"
            "INDEPENDENT_REPLICATION"
        )
    elif authorized:
        state = "LONG_HORIZON_SPATIAL_TRANSPORT_PENDING_TIMESTEP_STABILITY"
    else:
        state = "LONG_HORIZON_NUMERICAL_MODEL_REVISION"

    suite: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "scientific_state": state,
        "protocol": protocol,
        "protocol_digest": protocol["manifest_digest"],
        "parent_findings_digest": PRIOR_FINDINGS_DIGEST,
        "anchor_reproduced": anchor_reproduced,
        "anchor_expected_run_digest": ANCHOR_NUMERICAL_RUN_DIGEST,
        "resolution_discoveries": (anchor, extension),
        "resolution_comparison": resolution_comparison,
        "conditional_decision": {
            "authorized": authorized,
            "executed": fine is not None,
            "skip_reason": skip_reason,
            "predicate_used_det_features": False,
            "predicate_used_lps_shape": False,
            "predicate_used_growth_score": False,
        },
        "timestep_discovery": fine,
        "timestep_comparison": timestep_comparison,
        "ret_evidence": evidence_summary,
        "ret_evidence_ledger": {
            "record_ids": ledger.record_ids,
            "source_ids": ledger.source_ids,
            "record_count": len(ledger.records),
            "counts_as_replication": False,
            "historically_fresh": False,
            "posterior_model_probabilities_authorized": False,
        },
        "selected_observation_resolution": 56 if ledger.records else None,
        "timestep_check_resolution": 48 if timestep_comparison else None,
        "spatiotemporal_convergence_rectangle_complete": False,
        "near_singular_candidate": False,
        "rg2_state": "NOT_EVALUATED_NO_SOURCE_DISJOINT_REPLICATION",
        "formal_singularity_claim": False,
        "global_regularity_claim": False,
        "proof_language_allowed": False,
        "proof_warning": PROOF_WARNING,
        "discovery_warning": DISCOVERY_WARNING,
        "completion_warning": COMPLETION_WARNING,
    }
    suite["suite_digest"] = evidence_payload_digest(suite)
    return suite


def compact_completion_summary(suite: Mapping[str, object]) -> dict[str, object]:
    """Return a persisted-sized summary without field samples or spectra."""

    discoveries = list(suite["resolution_discoveries"])
    if suite["timestep_discovery"] is not None:
        discoveries.append(suite["timestep_discovery"])
    return {
        "scientific_state": suite["scientific_state"],
        "protocol_digest": suite["protocol_digest"],
        "parent_findings_digest": suite["parent_findings_digest"],
        "runtime_and_implementation": suite["protocol"][
            "runtime_and_implementation"
        ],
        "anchor_reproduced": suite["anchor_reproduced"],
        "runs": tuple(_compact_run(discovery) for discovery in discoveries),
        "resolution_comparison": suite["resolution_comparison"],
        "conditional_decision": suite["conditional_decision"],
        "timestep_comparison": suite["timestep_comparison"],
        "ret_evidence": suite["ret_evidence"],
        "ret_evidence_ledger": suite["ret_evidence_ledger"],
        "selected_observation_resolution": suite[
            "selected_observation_resolution"
        ],
        "timestep_check_resolution": suite["timestep_check_resolution"],
        "spatiotemporal_convergence_rectangle_complete": suite[
            "spatiotemporal_convergence_rectangle_complete"
        ],
        "near_singular_candidate": suite["near_singular_candidate"],
        "rg2_state": suite["rg2_state"],
        "formal_singularity_claim": suite["formal_singularity_claim"],
        "global_regularity_claim": suite["global_regularity_claim"],
        "proof_language_allowed": suite["proof_language_allowed"],
        "suite_digest": suite["suite_digest"],
        "completion_warning": suite["completion_warning"],
    }


if __name__ == "__main__":
    try:
        print(json.dumps(compact_completion_summary(run_long_horizon_completion()), indent=2))
    except RuntimeError as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, indent=2))
