"""Governance gates for proposing relations from predictive residuals.

The existing RG1 rule requires relational identification before an optional
extension is interpreted.  RG2 governs the earlier model-generation step:
candidate relations may be proposed only after predictive failure replicates
on disjoint evidence and improves prediction on untouched data.
"""

from __future__ import annotations

from dataclasses import dataclass


RG2 = "RG2: Model generation follows replicated predictive failure."
DISCOVERY_IS_NOT_PROOF = (
    "A discovery candidate is a replicated predictive relation within its "
    "declared evidence scope; it is not a universal mathematical proof or an "
    "ontological conclusion."
)

DISCOVERY_STATES = (
    "EVIDENCE_INVALID",
    "MODEL_REVISION",
    "NEEDS_FRESH_VALIDATION",
    "NEEDS_REPLICATION",
    "NO_HELDOUT_GAIN",
    "DIAGNOSTIC_FAILURE",
    "DISCOVERY_CANDIDATE",
    "BOUNDED_EXACT_COMPUTATION",
    "EXACT_CERTIFICATE",
)


@dataclass(frozen=True)
class DiscoveryThresholds:
    minimum_disjoint_replications: int = 2
    minimum_heldout_log_score_gain: float = 2.0
    maximum_open_model_probability: float = 0.10

    def __post_init__(self) -> None:
        if self.minimum_disjoint_replications < 2:
            raise ValueError("RG2 requires at least two disjoint replications")
        if self.minimum_heldout_log_score_gain <= 0.0:
            raise ValueError("held-out score gain must be positive")
        if not 0.0 < self.maximum_open_model_probability < 1.0:
            raise ValueError("open-model threshold must lie between zero and one")


@dataclass(frozen=True)
class DiscoveryEvidence:
    candidate_name: str
    source_sets_are_disjoint: bool
    directional_replications: int
    heldout_log_score_gain: float
    posterior_predictive_diagnostics_passed: bool
    open_model_probability: float | None
    exact_certificate_verified: bool = False
    exact_certificate_scope: str | None = None
    proof_language_requested: bool = False
    bounded_exact_computation_verified: bool = False
    bounded_exact_scope: str | None = None
    model_revision_required: bool = False
    model_revision_reason: str | None = None
    open_model_probability_calibrated: bool = True
    validation_is_historically_fresh: bool = True

    def __post_init__(self) -> None:
        if not self.candidate_name:
            raise ValueError("candidate name is required")
        if self.directional_replications < 0:
            raise ValueError("replication count cannot be negative")
        if self.open_model_probability is None:
            if self.open_model_probability_calibrated:
                raise ValueError(
                    "a calibrated open-model probability cannot be unavailable"
                )
        elif not 0.0 <= self.open_model_probability <= 1.0:
            raise ValueError("open-model probability must lie in [0, 1]")
        if self.exact_certificate_verified and not self.exact_certificate_scope:
            raise ValueError("an exact certificate requires an explicit scope")
        if (
            self.bounded_exact_computation_verified
            and not self.bounded_exact_scope
        ):
            raise ValueError("a bounded exact computation requires an explicit scope")
        if self.exact_certificate_verified and self.bounded_exact_computation_verified:
            raise ValueError("choose exact certificate or bounded computation, not both")
        if self.model_revision_required and not self.model_revision_reason:
            raise ValueError("model revision requires a reason")
        if not isinstance(self.open_model_probability_calibrated, bool):
            raise ValueError("open-model calibration flag must be Boolean")
        if not isinstance(self.validation_is_historically_fresh, bool):
            raise ValueError("historical-validation flag must be Boolean")


def evaluate_discovery_candidate(
    evidence: DiscoveryEvidence,
    thresholds: DiscoveryThresholds = DiscoveryThresholds(),
) -> dict[str, object]:
    """Evaluate an ordered, conservative RG2 decision ladder."""

    if evidence.exact_certificate_verified:
        state = "EXACT_CERTIFICATE"
        reason = (
            "an exact certificate was independently verified only for its "
            "declared scope"
        )
    elif evidence.bounded_exact_computation_verified:
        state = "BOUNDED_EXACT_COMPUTATION"
        reason = (
            "an exact-arithmetic finite computation was internally "
            "cross-checked only for its declared scope; it is not an "
            "independently replayable certificate or a second full reproduction"
        )
    elif not evidence.source_sets_are_disjoint:
        state = "EVIDENCE_INVALID"
        reason = "training, replication, or holdout sources overlap"
    elif evidence.model_revision_required:
        state = "MODEL_REVISION"
        reason = str(evidence.model_revision_reason)
    elif not evidence.open_model_probability_calibrated:
        state = "MODEL_REVISION"
        reason = "the open-model probability has not been calibrated"
    elif (
        evidence.open_model_probability is not None
        and evidence.open_model_probability > thresholds.maximum_open_model_probability
    ):
        state = "MODEL_REVISION"
        reason = "the robust open model remains too probable"
    elif evidence.heldout_log_score_gain <= 0.0:
        state = "NO_HELDOUT_GAIN"
        reason = "the proposed relation does not improve the declared validation record"
    elif not evidence.validation_is_historically_fresh:
        state = "NEEDS_FRESH_VALIDATION"
        reason = "the positive validation record was used in an earlier analysis"
    elif evidence.directional_replications < thresholds.minimum_disjoint_replications:
        state = "NEEDS_REPLICATION"
        reason = "the residual direction has not replicated on enough disjoint records"
    elif evidence.heldout_log_score_gain < thresholds.minimum_heldout_log_score_gain:
        state = "NO_HELDOUT_GAIN"
        reason = "the proposed relation does not improve untouched prediction enough"
    elif not evidence.posterior_predictive_diagnostics_passed:
        state = "DIAGNOSTIC_FAILURE"
        reason = "posterior-predictive diagnostics remain inadequate"
    else:
        state = "DISCOVERY_CANDIDATE"
        reason = "replicated disjoint residual improves held-out prediction"

    proof_language_allowed = (
        state == "EXACT_CERTIFICATE"
        and evidence.exact_certificate_verified
        and bool(evidence.exact_certificate_scope)
    )
    if evidence.proof_language_requested and not proof_language_allowed:
        reason += "; requested proof language is blocked outside an exact certificate"
    return {
        "state": state,
        "reason": reason,
        "candidate": evidence.candidate_name,
        "rg2": RG2,
        "warning": DISCOVERY_IS_NOT_PROOF,
        "source_sets_are_disjoint": evidence.source_sets_are_disjoint,
        "directional_replications": evidence.directional_replications,
        "heldout_log_score_gain": evidence.heldout_log_score_gain,
        "open_model_probability": evidence.open_model_probability,
        "open_model_probability_calibrated": (
            evidence.open_model_probability_calibrated
        ),
        "validation_is_historically_fresh": (
            evidence.validation_is_historically_fresh
        ),
        "proof_language_allowed": proof_language_allowed,
        "exact_certificate_scope": evidence.exact_certificate_scope,
        "bounded_exact_scope": evidence.bounded_exact_scope,
    }
