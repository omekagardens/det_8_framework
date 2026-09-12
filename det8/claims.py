"""Authoritative claim and module-status registry for DET8.

This is a bounded registry of supported public programs and enforced research
boundaries, not a validation of every detailed claim in the historical
repository.  Passing a software test can verify a software contract; it cannot
promote a physical or ontological claim.  Unlisted claims and research modules
remain experimental by default and are never treated as supported merely
because their source exists or can be imported.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from types import MappingProxyType
from typing import Final

# Development status and evidence status are intentionally separate axes.
ACTIVE_HARDENING: Final = "ACTIVE_HARDENING"
MAINTAINED: Final = "MAINTAINED"
ACTIVE_DEVELOPMENT: Final = "ACTIVE_DEVELOPMENT"
PLANNED: Final = "PLANNED"
DEFERRED: Final = "DEFERRED"
DEFERRED_REDESIGN_REQUIRED: Final = "DEFERRED_REDESIGN_REQUIRED"
REDESIGN_REQUIRED: Final = "REDESIGN_REQUIRED"
RETIRED: Final = "RETIRED"
DEPRECATED: Final = "DEPRECATED"

VERIFIED_SOFTWARE_CONTRACT: Final = "VERIFIED_SOFTWARE_CONTRACT"
NOT_YET_VALIDATED: Final = "NOT_YET_VALIDATED"
BOUNDED_CONDITIONAL_RESULT: Final = "BOUNDED_CONDITIONAL_RESULT"
CORRESPONDENCE_ONLY: Final = "CORRESPONDENCE_ONLY"
NO_EMPIRICAL_SUPPORT: Final = "NO_EMPIRICAL_SUPPORT"
NOT_APPLICABLE: Final = "NOT_APPLICABLE"


class RetiredResearchError(RuntimeError):
    """Raised when retired research is used outside its explicit opt-in path."""


@dataclass(frozen=True, slots=True)
class ClaimRecord:
    """One bounded public claim or development program.

    ``falsifier`` is the condition that defeats, blocks, or forces withdrawal
    of the registered claim.  For planned engineering programs this is an
    acceptance-gate failure, not a claim of physical falsification.
    """

    claim_id: str
    title: str
    layer: str
    evidence_status: str
    development_status: str
    dependencies: tuple[str, ...]
    falsifier: str
    evidence_links: tuple[str, ...]
    priority: int | None = None

    def as_dict(self) -> dict[str, object]:
        """Return a detached, JSON-serializable representation."""

        return asdict(self)


def _claim(
    claim_id: str,
    title: str,
    layer: str,
    evidence_status: str,
    development_status: str,
    *,
    dependencies: tuple[str, ...] = (),
    falsifier: str,
    evidence_links: tuple[str, ...],
    priority: int | None = None,
) -> ClaimRecord:
    return ClaimRecord(
        claim_id=claim_id,
        title=title,
        layer=layer,
        evidence_status=evidence_status,
        development_status=development_status,
        dependencies=dependencies,
        falsifier=falsifier,
        evidence_links=evidence_links,
        priority=priority,
    )


_CLAIMS = {
    "DET8-CORE": _claim(
        "DET8-CORE",
        "Validated formal record, measure, event, and commit core",
        "FORMAL_SOFTWARE_CORE",
        VERIFIED_SOFTWARE_CONTRACT,
        MAINTAINED,
        falsifier=(
            "A supported core operation accepts an invalid state, measure, graph, or commit; "
            "mutates partially on failure; or violates a declared invariant."
        ),
        evidence_links=(
            "docs/validation/g1-core-hardening-2026-09-04.md",
            "det8/tests/test_core_validation.py",
            "det8/tests/test_event_contracts.py",
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#3-phase-1--harden-the-core",
        ),
        priority=1,
    ),
    "DET8-RET-SDK": _claim(
        "DET8-RET-SDK",
        "Offline relational-evidence tooling SDK",
        "ENGINEERING_PLATFORM",
        NOT_YET_VALIDATED,
        ACTIVE_DEVELOPMENT,
        dependencies=("DET8-CORE",),
        falsifier=(
            "The frozen reference cases cannot be replayed with calibrated uncertainty, "
            "provenance, and deterministic decisions through one versioned public API."
        ),
        evidence_links=(
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#4-phase-2--deliver-the-ret-sdk",
        ),
        priority=2,
    ),
    "DET8-MATERIALS": _claim(
        "DET8-MATERIALS",
        "Materials condition-monitoring pilot",
        "APPLICATION",
        NOT_YET_VALIDATED,
        PLANNED,
        dependencies=("DET8-RET-SDK",),
        falsifier=(
            "The preregistered held-out material data show no useful calibrated forecasting "
            "or alerting benefit over the declared conventional baselines."
        ),
        evidence_links=(
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#5-phase-3--materials-monitoring-pilot",
        ),
        priority=3,
    ),
    "DET8-ANOMALY-TRIAGE": _claim(
        "DET8-ANOMALY-TRIAGE",
        "Conservative offline anomaly-triage pilot",
        "APPLICATION",
        NOT_YET_VALIDATED,
        PLANNED,
        dependencies=("DET8-RET-SDK", "DET8-MATERIALS"),
        falsifier=(
            "Locked null and seeded-fault benchmarks exceed the declared false-escalation, "
            "calibration, abstention, sensitivity, or matched-cost limits."
        ),
        evidence_links=(
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#6-phase-4--anomaly-triage-pilot",
        ),
        priority=4,
    ),
    "DET8-CAUSAL-GROWTH": _claim(
        "DET8-CAUSAL-GROWTH",
        "Causal and record-dependent growth research",
        "RESEARCH_PROGRAM",
        BOUNDED_CONDITIONAL_RESULT,
        DEFERRED,
        dependencies=(
            "DET8-CORE",
            "DET8-RET-SDK",
            "DET8-MATERIALS",
            "DET8-ANOMALY-TRIAGE",
        ),
        falsifier=(
            "A declared certificate premise fails, a finite counterexample violates the claimed "
            "covariance or consistency property, or no compatible extension exists."
        ),
        evidence_links=(
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry",
            "docs/track_b/covariant_record_growth.md",
        ),
        priority=5,
    ),
    "DET8-QUANTUM": _claim(
        "DET8-QUANTUM",
        "Quantum reconstruction and correspondence research",
        "RESEARCH_PROGRAM",
        CORRESPONDENCE_ONLY,
        DEFERRED,
        dependencies=(
            "DET8-CORE",
            "DET8-RET-SDK",
            "DET8-MATERIALS",
            "DET8-ANOMALY-TRIAGE",
        ),
        falsifier=(
            "An independent reference disagrees with the declared toy calculation or a required "
            "reconstruction assumption cannot be derived without inserting the target structure."
        ),
        evidence_links=(
            "det8/tests/test_quantum_correctness.py",
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry",
        ),
        priority=6,
    ),
    "DET8-T7-LINK": _claim(
        "DET8-T7-LINK",
        "T7 order-and-count geometry link (correspondence, bounded)",
        "CORRESPONDENCE",
        BOUNDED_CONDITIONAL_RESULT,
        DEFERRED,
        dependencies=("DET8-CORE",),
        falsifier=(
            "The link is read as manifoldlike emergence or as a native (DET-derived) "
            "geometry rather than a correspondence: its declared scope is exceeded "
            "(dimensions beyond 1+1 primary, or geometry not supplied), or a "
            "geometry-independent growth law is exhibited whose order is manifoldlike "
            "on the declared invariants, or the estimator is shown to require the "
            "Lorentzian structure it claims to recover."
        ),
        evidence_links=(
            "docs/track_b/GEOMETRY_NEXT.md#2-the-open-target--a-native-derivation-of-geometry-o7",
            "MODEL_CARD.md#6-open-problem-status-revised-per-mathematical-review-aug-2026",
            "docs/validation/qr-05cf-t7-supplied-geometry-2026-09-10/README.md#3-result",
            "docs/validation/qr-05cy-observational-quotient-2026-09-10/RESULTS.md#taxonomy-on-the-existing-registry",
            "docs/validation/qr-05dn-t7-link-2026-09-11/README.md",
        ),
    ),
    "DET8-F9-DISCRIMINATOR": _claim(
        "DET8-F9-DISCRIMINATOR",
        "Temperature-independence versus annealing discriminator",
        "PROPOSED_PHYSICAL_DISCRIMINATOR",
        NO_EMPIRICAL_SUPPORT,
        REDESIGN_REQUIRED,
        dependencies=(
            "DET8-CORE",
            "DET8-RET-SDK",
            "DET8-MATERIALS",
            "DET8-ANOMALY-TRIAGE",
            "DET8-CAUSAL-GROWTH",
            "DET8-QUANTUM",
        ),
        falsifier=(
            "A preregistered measured-data protocol cannot distinguish the proposed "
            "temperature-independent recovery from an adequate conventional model ensemble, "
            "or the required matched structural states cannot be operationalized."
        ),
        evidence_links=(
            "det8/models/f9_execution.py",
            "det8/models/kappa_discriminator.py",
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals",
        ),
        priority=7,
    ),
    "DET8-KAPPA-CLOCK": _claim(
        "DET8-KAPPA-CLOCK",
        "Kappa-participation clock hypothesis",
        "PROPOSED_PHYSICAL",
        NO_EMPIRICAL_SUPPORT,
        DEFERRED_REDESIGN_REQUIRED,
        dependencies=(
            "DET8-CORE",
            "DET8-RET-SDK",
            "DET8-MATERIALS",
            "DET8-ANOMALY-TRIAGE",
            "DET8-CAUSAL-GROWTH",
            "DET8-QUANTUM",
            "DET8-F9-DISCRIMINATOR",
        ),
        falsifier=(
            "A future experiment-specific protocol with independent kappa preparation and "
            "measurement excludes its preregistered identifiable estimand."
        ),
        evidence_links=(
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals",
            "GOVERNANCE.md#4-claim-status-register",
        ),
        priority=8,
    ),
    "DET8-GRAVITY": _claim(
        "DET8-GRAVITY",
        "Kappa-sourced or modified gravity",
        "RETIRED_PHYSICAL",
        NO_EMPIRICAL_SUPPORT,
        RETIRED,
        falsifier=(
            "Any active DET8 import, result, or summary advertises a kappa-gravity prediction, "
            "constant, force law, or experimental readiness."
        ),
        evidence_links=(
            "GOVERNANCE.md#4-claim-status-register",
            "det8/models/legacy_gravity_quarantine.py",
        ),
    ),
    "DET8-BOOK": _claim(
        "DET8-BOOK",
        "Book-development workstream",
        "PUBLICATION_WORKSTREAM",
        NOT_APPLICABLE,
        DEPRECATED,
        falsifier=(
            "Book work displaces the adopted core, SDK, application, or gated research sequence "
            "without an explicit governance reprioritization."
        ),
        evidence_links=(
            "GOVERNANCE.md#development-authority-and-priority--september-4-2026",
            "docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#1-working-authority-and-program-order",
        ),
    ),
}

CLAIMS: Final[Mapping[str, ClaimRecord]] = MappingProxyType(_CLAIMS)
CLAIM_REGISTRY: Final[Mapping[str, ClaimRecord]] = CLAIMS

# This order is policy, not an evidence ranking.  Retired and deprecated work is
# deliberately absent.  Causal/quantum work remains gated behind the first four.
PRIMARY_DEVELOPMENT_SEQUENCE: Final[tuple[str, ...]] = (
    "DET8-CORE",
    "DET8-RET-SDK",
    "DET8-MATERIALS",
    "DET8-ANOMALY-TRIAGE",
    "DET8-CAUSAL-GROWTH",
    "DET8-QUANTUM",
    "DET8-F9-DISCRIMINATOR",
    "DET8-KAPPA-CLOCK",
)


# The public supported surface is intentionally much smaller than ``det8.models``.
SUPPORTED_PUBLIC_MODULES: Final[frozenset[str]] = frozenset({"det8", "det8.claims", "det8.core"})
PREVIEW_PUBLIC_MODULES: Final[frozenset[str]] = frozenset({"det8.ret"})
SUPPORTED_CORE_IMPLEMENTATION_MODULES: Final[frozenset[str]] = frozenset(
    {
        "det8.models.bonds",
        "det8.models.event_graph",
        "det8.models.mam0",
        "det8.models.markov_kernel",
        "det8.models.validation",
    }
)

# Symbol-level allowlist used by ``det8.core``.  The partially quarantined
# ``det8_core`` module contributes only its validated record container.
SUPPORTED_CORE_EXPORTS: Final[Mapping[str, tuple[str, ...]]] = MappingProxyType(
    {
        "det8.models.validation": (
            "normalize_nonnegative_weights",
            "require_nonnegative_finite",
            "require_positive_finite",
            "require_real_finite",
        ),
        "det8.models.det8_core": ("NodeRecord",),
        "det8.models.markov_kernel": (
            "DETCommitKernel",
            "MeasurableSpace",
            "ProbabilityMeasure",
            "TransitionKernel",
            "compose_kernels",
            "make_mam0_kernel",
            "validate_kernel",
        ),
        "det8.models.mam0": (
            "Actualizer",
            "CommitMap",
            "EventDomain",
            "EventScheduler",
            "LawMap",
            "PossibilityObject",
            "Record",
            "Regime",
        ),
        "det8.models.event_graph": (
            "CausalGraph",
            "CausalPastRecord",
            "CausalScheduler",
            "Event",
            "ScheduleLimitExceeded",
        ),
        "det8.models.bonds": (
            "BondFluxEvent",
            "BondNetwork",
            "BondRecord",
            "apply_bond_flux",
            "generate_bond_flux_possibilities",
            "verify_network_conservation",
        ),
    }
)


# This is the complete existing Option-B gravity/continuum retirement ledger.
# Reasons are centralized here so the claim registry and executable quarantine
# cannot drift independently.
RETIRED_MODULE_REASONS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "det8.models.q_gravity": "Treats structural history as gravitational charge.",
        "det8.models.det_gravity": ("Maps kappa conservation to a gravitational Poisson equation."),
        "det8.models.gravity_v2": "Adds an underived kappa response to Newtonian gravity.",
        "det8.models.gravity_experiment": (
            "Simulates an experiment for the withdrawn kappa-force law."
        ),
        "det8.models.newton_correspondence": (
            "Calibrates the withdrawn kappa source to Newtonian mass."
        ),
        "det8.models.unified_simulation": (
            "Integrates the withdrawn kappa-gravity sector as active physics."
        ),
        "det8.models.kappa_derivation": (
            "Constructs a galactic kappa profile for the withdrawn force law."
        ),
        "det8.models.sparc_analysis": "Fits rotation curves with the withdrawn force law.",
        "det8.models.cluster_dynamics": (
            "Reinterprets inferred cluster masses through kappa-gravity."
        ),
        "det8.models.post_newtonian": ("Inserts a kappa-dependent G into standard PPN formulas."),
        "det8.models.flyby_anomaly": ("Attributes flyby residuals to the withdrawn force law."),
        "det8.models.remaining_items": ("Bundles retired galaxy, cluster, and BAO gravity claims."),
        **{
            f"det8.models.{name}": (
                "Uses inserted continuum geometry and/or the retired Pi/kappa gravity "
                "identification."
            )
            for name in (
                "continuum_limit_proof",
                "continuum_limit_l234",
                "continuum_limit_step1",
                "continuum_limit_step2",
                "continuum_limit_step3",
                "continuum_limit_step4",
                "continuum_limit_step4p",
                "continuum_limit_concentration",
                "continuum_limit_lgh",
                "continuum_limit_bianchi",
                "continuum_limit_curvature",
                "continuum_limit_einstein",
                "continuum_limit_geometric",
                "o7_causal_spacetime",
                "o7_continuum_limit",
                "o7_derivation",
            )
        },
    }
)

PARTIALLY_QUARANTINED_MODULES: Final[Mapping[str, tuple[str, ...]]] = MappingProxyType(
    {
        "det8.models.det8_core": (
            "LAMBDA_GAMMA",
            "GAMMA_B",
            "NodeRecord.gamma",
            "effective_gravity_source",
            "clock and participation ansatzes are not supported facade exports",
        ),
        "det8.models.det_units": (
            "gravity_shift_from_alpha",
            "alpha_from_gravity_shift",
            "gravity entries in coupling_implications and fit_lab_example",
        ),
        "det8.models.experimental_constraints": ("gravity and orbital-anomaly sections",),
        "det8.models.gps_analysis": (
            "kappa-gravity interpretation; clock-ratio arithmetic may survive",
        ),
        "det8.models.track_a": (
            "gravity_sensitivity retired compatibility guard",
            "clock and combined calculations deferred for redesign",
        ),
    }
)

DEFERRED_RESEARCH_MODULE_CLAIMS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "det8.models.clock_anomaly": "DET8-KAPPA-CLOCK",
        "det8.models.clock_experiment": "DET8-KAPPA-CLOCK",
        "det8.models.covariant_causal_growth": "DET8-CAUSAL-GROWTH",
        "det8.models.covariant_record_growth": "DET8-CAUSAL-GROWTH",
        "det8.models.f9_execution": "DET8-F9-DISCRIMINATOR",
        "det8.models.joint_record_growth": "DET8-CAUSAL-GROWTH",
        "det8.models.kappa_discriminator": "DET8-F9-DISCRIMINATOR",
        "det8.models.mamq": "DET8-QUANTUM",
        "det8.models.quantum_validation": "DET8-QUANTUM",
        "det8.models.time_evolution": "DET8-QUANTUM",
    }
)
DEFERRED_RESEARCH_MODULES: Final[frozenset[str]] = frozenset(DEFERRED_RESEARCH_MODULE_CLAIMS)

MODULE_SUPPORTED: Final = "SUPPORTED"
MODULE_SUPPORTED_INTERNAL: Final = "SUPPORTED_INTERNAL"
MODULE_PARTIAL_QUARANTINE: Final = "PARTIAL_QUARANTINE"
MODULE_DEFERRED_RESEARCH: Final = "DEFERRED_RESEARCH"
MODULE_RETIRED: Final = "RETIRED"
MODULE_LEGACY_OPT_IN: Final = "LEGACY_OPT_IN"
MODULE_EXPERIMENTAL: Final = "EXPERIMENTAL"
MODULE_UNVALIDATED_PREVIEW: Final = "UNVALIDATED_PREVIEW"

REGISTRY_METADATA: Final[Mapping[str, object]] = MappingProxyType(
    {
        "scope": "SUPPORTED_PUBLIC_PROGRAMS_AND_ENFORCED_BOUNDARIES",
        "historical_detailed_claims_validated": False,
        "unlisted_claims_validated": False,
        "default_unlisted_module_status": MODULE_EXPERIMENTAL,
        "automatic_evidence_promotion": False,
    }
)


@dataclass(frozen=True, slots=True)
class ModuleClassification:
    """Bounded classification for a Python module name."""

    module: str
    status: str
    public: bool
    claim_id: str | None
    note: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def get_claim(claim_id: str) -> ClaimRecord:
    """Return a registered claim, rejecting unknown identifiers."""

    try:
        return CLAIMS[claim_id]
    except KeyError as exc:
        raise KeyError(f"unknown DET8 claim ID {claim_id!r}") from exc


def claim_summary() -> tuple[dict[str, object], ...]:
    """Return the complete registry in deterministic, serializable order."""

    return tuple(CLAIMS[claim_id].as_dict() for claim_id in sorted(CLAIMS))


def classify_module(module_name: str) -> ModuleClassification:
    """Classify a module without promoting unlisted research code.

    Only the explicit facade and registry are supported public namespaces.
    Existing implementation modules behind the facade are supported internal
    dependencies.  Every other ``det8.models`` module defaults to
    ``EXPERIMENTAL`` unless it is explicitly deferred, partial, or retired.
    """

    if not isinstance(module_name, str):
        raise TypeError("module_name must be a string")
    if not module_name or module_name != module_name.strip():
        raise ValueError("module_name must be a nonempty canonical module name")

    if module_name in SUPPORTED_PUBLIC_MODULES:
        return ModuleClassification(
            module_name,
            MODULE_SUPPORTED,
            True,
            "DET8-CORE",
            "documented supported public namespace",
        )
    if module_name in PREVIEW_PUBLIC_MODULES:
        return ModuleClassification(
            module_name,
            MODULE_UNVALIDATED_PREVIEW,
            True,
            "DET8-RET-SDK",
            "versioned development preview; G2 calibration and independent gate review remain open",
        )
    if module_name in SUPPORTED_CORE_IMPLEMENTATION_MODULES:
        return ModuleClassification(
            module_name,
            MODULE_SUPPORTED_INTERNAL,
            False,
            "DET8-CORE",
            "supported only through the det8.core facade",
        )
    if module_name in RETIRED_MODULE_REASONS:
        return ModuleClassification(
            module_name,
            MODULE_RETIRED,
            False,
            "DET8-GRAVITY",
            RETIRED_MODULE_REASONS[module_name],
        )
    if module_name in PARTIALLY_QUARANTINED_MODULES:
        return ModuleClassification(
            module_name,
            MODULE_PARTIAL_QUARANTINE,
            False,
            "DET8-GRAVITY" if module_name != "det8.models.track_a" else "DET8-KAPPA-CLOCK",
            "; ".join(PARTIALLY_QUARANTINED_MODULES[module_name]),
        )
    if module_name in DEFERRED_RESEARCH_MODULES:
        return ModuleClassification(
            module_name,
            MODULE_DEFERRED_RESEARCH,
            False,
            DEFERRED_RESEARCH_MODULE_CLAIMS[module_name],
            "research re-entry is gated by the registered development sequence",
        )
    if module_name == "det8.legacy" or module_name.startswith("det8.legacy."):
        return ModuleClassification(
            module_name,
            MODULE_LEGACY_OPT_IN,
            False,
            "DET8-GRAVITY",
            "historical reproduction requires explicit retired-research opt-in",
        )
    return ModuleClassification(
        module_name,
        MODULE_EXPERIMENTAL,
        False,
        None,
        "unlisted modules are experimental and receive no automatic evidence promotion",
    )


def module_status(module_name: str) -> str:
    """Return only the bounded module status string."""

    return classify_module(module_name).status


def is_supported_module(module_name: str) -> bool:
    """Whether a module is in the explicit supported public namespace."""

    classification = classify_module(module_name)
    return classification.public and classification.status == MODULE_SUPPORTED


def registry_document() -> dict[str, object]:
    """Return a complete detached policy document suitable for JSON output."""

    return {
        "metadata": dict(REGISTRY_METADATA),
        "claims": [CLAIMS[claim_id].as_dict() for claim_id in sorted(CLAIMS)],
        "primary_development_sequence": list(PRIMARY_DEVELOPMENT_SEQUENCE),
        "supported_public_modules": sorted(SUPPORTED_PUBLIC_MODULES),
        "preview_public_modules": sorted(PREVIEW_PUBLIC_MODULES),
        "supported_core_exports": {
            module: list(symbols) for module, symbols in SUPPORTED_CORE_EXPORTS.items()
        },
        "retired_modules": dict(RETIRED_MODULE_REASONS),
        "partial_quarantine": {
            module: list(symbols) for module, symbols in PARTIALLY_QUARANTINED_MODULES.items()
        },
        "default_unlisted_module_status": MODULE_EXPERIMENTAL,
    }


def _validate_registry() -> None:
    allowed_development = {
        ACTIVE_HARDENING,
        MAINTAINED,
        ACTIVE_DEVELOPMENT,
        PLANNED,
        DEFERRED,
        DEFERRED_REDESIGN_REQUIRED,
        REDESIGN_REQUIRED,
        RETIRED,
        DEPRECATED,
    }
    allowed_evidence = {
        VERIFIED_SOFTWARE_CONTRACT,
        NOT_YET_VALIDATED,
        BOUNDED_CONDITIONAL_RESULT,
        CORRESPONDENCE_ONLY,
        NO_EMPIRICAL_SUPPORT,
        NOT_APPLICABLE,
    }
    for key, claim in CLAIMS.items():
        if key != claim.claim_id:
            raise RuntimeError(f"claim key {key!r} does not match record ID {claim.claim_id!r}")
        if claim.development_status not in allowed_development:
            raise RuntimeError(f"invalid development status for {key}")
        if claim.evidence_status not in allowed_evidence:
            raise RuntimeError(f"invalid evidence status for {key}")
        if not claim.layer or not claim.falsifier or not claim.evidence_links:
            raise RuntimeError(f"claim {key} is missing required registry metadata")
        unknown = set(claim.dependencies) - set(CLAIMS)
        if unknown:
            raise RuntimeError(f"claim {key} has unknown dependencies {unknown!r}")
    if len(set(PRIMARY_DEVELOPMENT_SEQUENCE)) != len(PRIMARY_DEVELOPMENT_SEQUENCE):
        raise RuntimeError("development sequence contains duplicate claim IDs")
    if set(PRIMARY_DEVELOPMENT_SEQUENCE) - set(CLAIMS):
        raise RuntimeError("development sequence contains unknown claim IDs")
    sequence_positions = {
        claim_id: position
        for position, claim_id in enumerate(PRIMARY_DEVELOPMENT_SEQUENCE, start=1)
    }
    for claim_id, position in sequence_positions.items():
        claim = CLAIMS[claim_id]
        if claim.priority != position:
            raise RuntimeError(f"claim {claim_id} priority does not match the development sequence")
        late_dependencies = {
            dependency
            for dependency in claim.dependencies
            if dependency in sequence_positions and sequence_positions[dependency] >= position
        }
        if late_dependencies:
            raise RuntimeError(
                f"claim {claim_id} precedes dependencies {sorted(late_dependencies)!r}"
            )
    if set(SUPPORTED_PUBLIC_MODULES) & set(RETIRED_MODULE_REASONS):
        raise RuntimeError("a supported public module is also retired")
    if PREVIEW_PUBLIC_MODULES & (SUPPORTED_PUBLIC_MODULES | set(RETIRED_MODULE_REASONS)):
        raise RuntimeError("preview modules may not be simultaneously supported or retired")


_validate_registry()


__all__ = [
    "ACTIVE_DEVELOPMENT",
    "ACTIVE_HARDENING",
    "BOUNDED_CONDITIONAL_RESULT",
    "CLAIMS",
    "CLAIM_REGISTRY",
    "CORRESPONDENCE_ONLY",
    "DEFERRED",
    "DEFERRED_REDESIGN_REQUIRED",
    "DEFERRED_RESEARCH_MODULES",
    "DEFERRED_RESEARCH_MODULE_CLAIMS",
    "DEPRECATED",
    "MAINTAINED",
    "MODULE_DEFERRED_RESEARCH",
    "MODULE_EXPERIMENTAL",
    "MODULE_LEGACY_OPT_IN",
    "MODULE_PARTIAL_QUARANTINE",
    "MODULE_RETIRED",
    "MODULE_SUPPORTED",
    "MODULE_SUPPORTED_INTERNAL",
    "MODULE_UNVALIDATED_PREVIEW",
    "NOT_APPLICABLE",
    "NOT_YET_VALIDATED",
    "NO_EMPIRICAL_SUPPORT",
    "PARTIALLY_QUARANTINED_MODULES",
    "PLANNED",
    "PREVIEW_PUBLIC_MODULES",
    "PRIMARY_DEVELOPMENT_SEQUENCE",
    "REDESIGN_REQUIRED",
    "REGISTRY_METADATA",
    "RETIRED",
    "RETIRED_MODULE_REASONS",
    "SUPPORTED_CORE_EXPORTS",
    "SUPPORTED_CORE_IMPLEMENTATION_MODULES",
    "SUPPORTED_PUBLIC_MODULES",
    "VERIFIED_SOFTWARE_CONTRACT",
    "ClaimRecord",
    "ModuleClassification",
    "RetiredResearchError",
    "claim_summary",
    "classify_module",
    "get_claim",
    "is_supported_module",
    "module_status",
    "registry_document",
]
