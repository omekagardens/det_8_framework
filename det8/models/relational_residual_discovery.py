"""Joint RG2 pressure test for distribution-level mathematical discovery."""

from __future__ import annotations

import json

from det8.models.examples.collatz_valuation_discovery import (
    run_collatz_valuation_discovery,
)
from det8.models.examples.riemann_multiscale_discovery import (
    run_riemann_multiscale_discovery,
)
from det8.models.relational_discovery_governance import (
    RG2,
    DiscoveryEvidence,
    DiscoveryThresholds,
    evaluate_discovery_candidate,
)


RESIDUAL_DISCOVERY_WARNING = (
    "RG2 discovery candidates are replicated predictive relations. They "
    "remain separate from bounded exact computations, independently "
    "checkable certificates, and universal proof claims."
)


def _riemann_governance(run: dict[str, object]) -> dict[str, object]:
    training = run["training"]
    holdout = run["locked_holdout"]
    calibration = run["synthetic_calibration"]
    sources = run["source_disjointness"]
    assert isinstance(training, dict)
    assert isinstance(holdout, dict)
    assert isinstance(calibration, dict)
    assert isinstance(sources, dict)
    candidate = str(training["selected_family"])
    holdout_scores = holdout["family_log_scores"]
    assert isinstance(holdout_scores, dict)
    alternative_score = max(
        float(score) for name, score in holdout_scores.items() if name != candidate
    )
    heldout_gain = float(holdout_scores[candidate]) - alternative_score
    exploratory_prequential_wins = 0
    for row in training["prequential_trace"]:
        increments = row["log_predictive_increment"]
        winner = max(increments, key=increments.get)
        exploratory_prequential_wins += int(winner == candidate)
    gates = calibration["calibration_gate"]
    diagnostics_passed = bool(
        gates["clean_recovery_at_least_0.75"]
        and gates["attack_detection_at_least_0.75"]
    )
    evidence = DiscoveryEvidence(
        candidate_name=(
            f"Riemann generalized-Wigner {candidate} calibration reference"
        ),
        source_sets_are_disjoint=bool(sources["source_disjoint"]),
        # The candidate is selected from the six-block training sequence.
        # Per-block wins are exploratory stability, not post-selection
        # replications; the previously published extension also summarized a
        # window overlapping validation block 8.
        directional_replications=0,
        heldout_log_score_gain=heldout_gain,
        posterior_predictive_diagnostics_passed=diagnostics_passed,
        open_model_probability=float(training["posterior"]["M_bottom"]),
        proof_language_requested=True,
        validation_is_historically_fresh=False,
    )
    return {
        **evaluate_discovery_candidate(evidence),
        "training_family": candidate,
        "locked_holdout_family": holdout["best_family"],
        "candidate_over_best_alternative_holdout_log_score_gain": heldout_gain,
        "exploratory_prequential_blocks_won": exploratory_prequential_wins,
        "historically_fresh_validation": False,
        "synthetic_attack_detection_rate": calibration["attack_detection_rate"],
    }


def _collatz_governance(run: dict[str, object]) -> dict[str, object]:
    comparison = run["locked_tree_comparison"]
    height = run["height_band_stability"]
    frontier = run["frontier"]
    escalation = run["exact_anomaly_escalation"]
    assert isinstance(comparison, dict)
    assert isinstance(height, dict)
    assert isinstance(frontier, dict)
    assert isinstance(escalation, dict)
    selected = comparison["model_comparison"][0]
    first_jump = next(
        row
        for row in comparison["model_comparison"]
        if row["model"] == "first_jump_controlled"
    )
    open_reference = comparison["robust_open_reference"]
    boundary_audit = comparison["selection_boundary_audit"]
    null_audit = comparison["null_adequacy_audit"]
    assert isinstance(open_reference, dict)
    assert isinstance(boundary_audit, dict)
    assert isinstance(null_audit, dict)
    heldout_gain = (
        float(selected["holdout_mean_student_t_log_score"])
        - float(first_jump["holdout_mean_student_t_log_score"])
    )
    protocol = comparison["protocol"]
    assert isinstance(protocol, dict)
    train_range = tuple(protocol["train_range_half_open"])
    holdout_range = tuple(protocol["locked_holdout_range_half_open"])
    statistical_ranges_are_disjoint = bool(
        train_range[1] <= holdout_range[0]
    )
    diagnostics_available = bool(
        comparison["posterior_predictive_diagnostics_available"]
    )
    revision_reasons = []
    if (
        boundary_audit["selected_depth_equals_declared_minimum"]
        or boundary_audit["selected_depth_equals_declared_maximum"]
    ):
        revision_reasons.append("the selected tree is at a declared depth boundary")
    if not open_reference["calibrated_posterior_probability_available"]:
        revision_reasons.append("the robust open branch is not probability-calibrated")
    if not null_audit["adequate_for_novel_relation_claim"]:
        revision_reasons.append(
            "residue bits need a multistep parity/valuation null"
        )
    if not diagnostics_available:
        revision_reasons.append("posterior-predictive residual diagnostics are absent")
    evidence = DiscoveryEvidence(
        candidate_name="Collatz residue-resolution workload relation",
        source_sets_are_disjoint=statistical_ranges_are_disjoint,
        # The higher band selected the panel winner. It is validation, not a
        # post-selection replication of that winner.
        directional_replications=0,
        heldout_log_score_gain=heldout_gain,
        posterior_predictive_diagnostics_passed=diagnostics_available,
        # The broad reference is useful for score sensitivity, but its scale
        # does not define a calibrated inadequacy probability.
        open_model_probability=None,
        proof_language_requested=True,
        model_revision_required=bool(revision_reasons),
        model_revision_reason="; ".join(revision_reasons),
        open_model_probability_calibrated=False,
    )
    governed = evaluate_discovery_candidate(
        evidence,
        DiscoveryThresholds(
            minimum_disjoint_replications=2,
            minimum_heldout_log_score_gain=0.02,
            maximum_open_model_probability=0.10,
        ),
    )
    certified_range = tuple(frontier["certified_range"])
    exact_scope = (
        f"positive integer starts {certified_range[0]} through "
        f"{certified_range[1]}"
    )
    exact_evidence = DiscoveryEvidence(
        candidate_name=(
            f"Collatz bounded convergence computation through "
            f"{certified_range[1]}"
        ),
        source_sets_are_disjoint=True,
        directional_replications=0,
        heldout_log_score_gain=0.0,
        posterior_predictive_diagnostics_passed=True,
        open_model_probability=0.0,
        bounded_exact_computation_verified=bool(
            frontier["all_reached_one"]
            and escalation["all_independent_audits_match"]
            and not frontier["exceptions"]
            and frontier["accelerated_odd_map"]["ordinary_toll_identity_holds"]
        ),
        bounded_exact_scope=exact_scope,
        proof_language_requested=True,
    )
    return {
        **governed,
        "selected_model": selected["model"],
        "exploratory_height_bands_with_same_sign": len(height["bands"]),
        "post_selection_replication_required": True,
        "post_selection_replication_count": 0,
        "validation_mean_student_t_log_score_gain_over_first_jump": heldout_gain,
        "posterior_predictive_diagnostics_available": diagnostics_available,
        "statistical_train_validation_ranges_are_disjoint": (
            statistical_ranges_are_disjoint
        ),
        "controlled_mod8_contrast": comparison["mod8_7_minus_5"],
        "block_score_audit": comparison["block_score_audit"],
        "selection_boundary_audit": comparison["selection_boundary_audit"],
        "null_adequacy_audit": comparison["null_adequacy_audit"],
        "model_revision_reasons": tuple(revision_reasons),
        "robust_open_reference": open_reference,
        "bounded_exact_branch": evaluate_discovery_candidate(exact_evidence),
    }


def run_relational_residual_discovery() -> dict[str, object]:
    """Run both mechanisms and evaluate their statistical and exact claims."""

    riemann = run_riemann_multiscale_discovery()
    collatz = run_collatz_valuation_discovery()
    riemann_gate = _riemann_governance(riemann)
    collatz_gate = _collatz_governance(collatz)
    return {
        "method": "Relational Residual Discovery",
        "rg2": RG2,
        "warning": RESIDUAL_DISCOVERY_WARNING,
        "evidence_core": {
            "provenance_overlap_protection": True,
            "prequential_scoring": True,
            "locked_holdout_support": True,
            "predictive_families": (
                "Gaussian",
                "StudentT",
                "Binomial",
                "BetaBinomial",
                "Poisson",
                "NegativeBinomial",
                "Multinomial",
                "DirichletMultinomial",
            ),
        },
        "governance": {
            "riemann": riemann_gate,
            "collatz": collatz_gate,
        },
        "runs": {
            "riemann_multiscale": riemann,
            "collatz_valuation_tree": collatz,
        },
        "discovery_summary": {
            "riemann": riemann_gate["state"],
            "collatz": collatz_gate["state"],
            "collatz_exact": collatz_gate["bounded_exact_branch"]["state"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_relational_residual_discovery(), indent=2))
