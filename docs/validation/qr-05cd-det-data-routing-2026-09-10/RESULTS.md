# QR-05CD decision record

10 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [routing note](README.md) fixes the rule that a dataset may address only
the DET structural target it actually instantiates. This gate ran nothing and
supplies no physical result.

## Main result

DET's primitives (`record_kernel_physics.md` §4) feed several *separate*
structural targets, and the charter forbids connecting unrelated modules. The
note routes each target to its legitimate data:

| Target | Data |
|---|---|
| Causal geometry from order and count (T7) | supplied Lorentzian sprinkling (order/count) |
| Bell / Tsirelson | setting-conditioned outcome statistics |
| Quadratic weights / `I₃=0` | multi-path interference counts |
| Pointer records | redundant-record / error-rate data |
| Diffusion / relaxation, and predictive-history κ | repeated kernel measurements under a known channel |
| κ materials descriptor | instrumented materials response |

It also gives a five-point admissibility checklist, whose core rule is: **name
the target, name which side of the bridge the data supplies, and require the
other side to be supplied or declared independently.**

## The CB case

The Bell dataset instantiates Bell/Tsirelson (E(α,β) correlations) and nothing
of the geometry side. CB fabricated the missing supplied marks, so the bridge
had only one real side — the misroute this note prevents. The reclassification
stands ([amendment](../qr-05cb-open-data-applicability-2026-09-10/ONTOLOGY_AMENDMENT.md)).

## Boundary and next gate

A routing discipline, not a result. It supplies no metric, dynamics or
physical claim, and changes no data or capture. The next gates are the correct
Bell-data application (quantum-correspondence / history distance) and the
deferred QR-05CC composition verification for the geometry path.

## Provenance

CD continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
