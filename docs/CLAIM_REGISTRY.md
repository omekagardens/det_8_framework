# DET8 public-program claim registry

Generated from `det8.claims`; do not maintain a separate status table by hand.
Run `python scripts/export_claim_registry.py --check` to verify synchronization.

This is the bounded supported/public-program registry, not validation of every
historical research claim. Software evidence does not promote physical claims.
Unlisted research APIs are experimental by default. Gate completion requires
its own dated report under `docs/validation/`.

| ID | Layer | Evidence status | Development status |
|---|---|---|---|
| DET8-ANOMALY-TRIAGE | APPLICATION | NOT_YET_VALIDATED | PLANNED |
| DET8-BOOK | PUBLICATION_WORKSTREAM | NOT_APPLICABLE | DEPRECATED |
| DET8-CAUSAL-GROWTH | RESEARCH_PROGRAM | BOUNDED_CONDITIONAL_RESULT | DEFERRED |
| DET8-CORE | FORMAL_SOFTWARE_CORE | VERIFIED_SOFTWARE_CONTRACT | MAINTAINED |
| DET8-F9-DISCRIMINATOR | PROPOSED_PHYSICAL_DISCRIMINATOR | NO_EMPIRICAL_SUPPORT | REDESIGN_REQUIRED |
| DET8-GRAVITY | RETIRED_PHYSICAL | NO_EMPIRICAL_SUPPORT | RETIRED |
| DET8-KAPPA-CLOCK | PROPOSED_PHYSICAL | NO_EMPIRICAL_SUPPORT | DEFERRED_REDESIGN_REQUIRED |
| DET8-MATERIALS | APPLICATION | NOT_YET_VALIDATED | PLANNED |
| DET8-QUANTUM | RESEARCH_PROGRAM | CORRESPONDENCE_ONLY | DEFERRED |
| DET8-RET-SDK | ENGINEERING_PLATFORM | NOT_YET_VALIDATED | ACTIVE_DEVELOPMENT |
| DET8-T7-LINK | CORRESPONDENCE | BOUNDED_CONDITIONAL_RESULT | DEFERRED |

## DET8-ANOMALY-TRIAGE — Conservative offline anomaly-triage pilot

Dependencies: DET8-RET-SDK, DET8-MATERIALS.

Failure or withdrawal condition: Locked null and seeded-fault benchmarks exceed the declared false-escalation, calibration, abstention, sensitivity, or matched-cost limits.

Evidence / scope links:

- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#6-phase-4--anomaly-triage-pilot](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#6-phase-4--anomaly-triage-pilot)

## DET8-BOOK — Book-development workstream

Dependencies: none.

Failure or withdrawal condition: Book work displaces the adopted core, SDK, application, or gated research sequence without an explicit governance reprioritization.

Evidence / scope links:

- [GOVERNANCE.md#development-authority-and-priority--september-4-2026](../GOVERNANCE.md#development-authority-and-priority--september-4-2026)
- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#1-working-authority-and-program-order](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#1-working-authority-and-program-order)

## DET8-CAUSAL-GROWTH — Causal and record-dependent growth research

Dependencies: DET8-CORE, DET8-RET-SDK, DET8-MATERIALS, DET8-ANOMALY-TRIAGE.

Failure or withdrawal condition: A declared certificate premise fails, a finite counterexample violates the claimed covariance or consistency property, or no compatible extension exists.

Evidence / scope links:

- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry)
- [docs/track_b/covariant_record_growth.md](../docs/track_b/covariant_record_growth.md)

## DET8-CORE — Validated formal record, measure, event, and commit core

Dependencies: none.

Failure or withdrawal condition: A supported core operation accepts an invalid state, measure, graph, or commit; mutates partially on failure; or violates a declared invariant.

Evidence / scope links:

- [docs/validation/g1-core-hardening-2026-09-04.md](../docs/validation/g1-core-hardening-2026-09-04.md)
- [det8/tests/test_core_validation.py](../det8/tests/test_core_validation.py)
- [det8/tests/test_event_contracts.py](../det8/tests/test_event_contracts.py)
- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#3-phase-1--harden-the-core](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#3-phase-1--harden-the-core)

## DET8-F9-DISCRIMINATOR — Temperature-independence versus annealing discriminator

Dependencies: DET8-CORE, DET8-RET-SDK, DET8-MATERIALS, DET8-ANOMALY-TRIAGE, DET8-CAUSAL-GROWTH, DET8-QUANTUM.

Failure or withdrawal condition: A preregistered measured-data protocol cannot distinguish the proposed temperature-independent recovery from an adequate conventional model ensemble, or the required matched structural states cannot be operationalized.

Evidence / scope links:

- [det8/models/f9_execution.py](../det8/models/f9_execution.py)
- [det8/models/kappa_discriminator.py](../det8/models/kappa_discriminator.py)
- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals)

## DET8-GRAVITY — Kappa-sourced or modified gravity

Dependencies: none.

Failure or withdrawal condition: Any active DET8 import, result, or summary advertises a kappa-gravity prediction, constant, force law, or experimental readiness.

Evidence / scope links:

- [GOVERNANCE.md#4-claim-status-register](../GOVERNANCE.md#4-claim-status-register)
- [det8/models/legacy_gravity_quarantine.py](../det8/models/legacy_gravity_quarantine.py)

## DET8-KAPPA-CLOCK — Kappa-participation clock hypothesis

Dependencies: DET8-CORE, DET8-RET-SDK, DET8-MATERIALS, DET8-ANOMALY-TRIAGE, DET8-CAUSAL-GROWTH, DET8-QUANTUM, DET8-F9-DISCRIMINATOR.

Failure or withdrawal condition: A future experiment-specific protocol with independent kappa preparation and measurement excludes its preregistered identifiable estimand.

Evidence / scope links:

- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#8-phase-6--later-physical-proposals)
- [GOVERNANCE.md#4-claim-status-register](../GOVERNANCE.md#4-claim-status-register)

## DET8-MATERIALS — Materials condition-monitoring pilot

Dependencies: DET8-RET-SDK.

Failure or withdrawal condition: The preregistered held-out material data show no useful calibrated forecasting or alerting benefit over the declared conventional baselines.

Evidence / scope links:

- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#5-phase-3--materials-monitoring-pilot](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#5-phase-3--materials-monitoring-pilot)

## DET8-QUANTUM — Quantum reconstruction and correspondence research

Dependencies: DET8-CORE, DET8-RET-SDK, DET8-MATERIALS, DET8-ANOMALY-TRIAGE.

Failure or withdrawal condition: An independent reference disagrees with the declared toy calculation or a required reconstruction assumption cannot be derived without inserting the target structure.

Evidence / scope links:

- [det8/tests/test_quantum_correctness.py](../det8/tests/test_quantum_correctness.py)
- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#7-phase-5--causal-growth-and-quantum-research-re-entry)

## DET8-RET-SDK — Offline relational-evidence tooling SDK

Dependencies: DET8-CORE.

Failure or withdrawal condition: The frozen reference cases cannot be replayed with calibrated uncertainty, provenance, and deterministic decisions through one versioned public API.

Evidence / scope links:

- [docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#4-phase-2--deliver-the-ret-sdk](../docs/CORE_HARDENING_AND_APPLICATION_PLAN.md#4-phase-2--deliver-the-ret-sdk)

## DET8-T7-LINK — T7 order-and-count geometry link (correspondence, bounded)

Dependencies: DET8-CORE.

Failure or withdrawal condition: The link is read as manifoldlike emergence or as a native (DET-derived) geometry rather than a correspondence: its declared scope is exceeded (dimensions beyond 1+1 primary, or geometry not supplied), or a geometry-independent growth law is exhibited whose order is manifoldlike on the declared invariants, or the estimator is shown to require the Lorentzian structure it claims to recover.

Evidence / scope links:

- [docs/track_b/GEOMETRY_NEXT.md#2-the-open-target--a-native-derivation-of-geometry-o7](../docs/track_b/GEOMETRY_NEXT.md#2-the-open-target--a-native-derivation-of-geometry-o7)
- [MODEL_CARD.md#6-open-problem-status-revised-per-mathematical-review-aug-2026](../MODEL_CARD.md#6-open-problem-status-revised-per-mathematical-review-aug-2026)
- [docs/validation/qr-05cf-t7-supplied-geometry-2026-09-10/README.md#3-result](../docs/validation/qr-05cf-t7-supplied-geometry-2026-09-10/README.md#3-result)
- [docs/validation/qr-05cy-observational-quotient-2026-09-10/RESULTS.md#taxonomy-on-the-existing-registry](../docs/validation/qr-05cy-observational-quotient-2026-09-10/RESULTS.md#taxonomy-on-the-existing-registry)
- [docs/validation/qr-05dn-t7-link-2026-09-11/README.md](../docs/validation/qr-05dn-t7-link-2026-09-11/README.md)

## Supported public modules

- `det8`
- `det8.claims`
- `det8.core`

## Unvalidated development-preview namespaces

- `det8.ret` — G2 is not closed; see [RET_SDK.md](RET_SDK.md).

Exact exports, partial quarantine, and the retired-module ledger are available
through `det8.claims.registry_document()`. See [CORE_API.md](CORE_API.md) for
compatibility notes and explicit historical opt-in behavior.
