# QR-05DN results

11 September 2026 (Pacific/Honolulu). **Direction J of the Track-B geometry program: the
T7 order-and-count geometry estimator is registered as a first-class, scoped
correspondence — `DET8-T7-LINK` — that the core may reference, with no promotion.**
Governance artifact (correspondence-level, Status M); 18 tests pass; no physical claim.

## 0. What was registered, and why these fields

| field | value | why |
|---|---|---|
| layer | `CORRESPONDENCE` | the link is a correspondence statement, not a physical claim |
| evidence status | `BOUNDED_CONDITIONAL_RESULT` | the estimator is verified only on **supplied** Minkowski samples (`CORR`); the O7 target is open |
| development status | `DEFERRED` | registering the link must not activate the gated research of the adopted sequence |
| priority | none, and **not** in `PRIMARY_DEVELOPMENT_SEQUENCE` | the registry's mechanism for sequence membership — absence is what makes the link unable to unlock gated work |
| dependencies | `DET8-CORE` | the only thing the link actually rests on (the supported formal core); deliberately not a gate dependency it does not have |
| falsifier | reading the link as manifoldlike emergence or native geometry, exceeding the scope, exhibiting a geometry-independent law as manifoldlike, or the estimator needing the Lorentzian structure it claims to recover | pins the O7 boundary in the registry itself |

The registry validates on import (`_validate_registry`), and the claim enters as the
**11th** entry with a single new *layer* label and **no** new evidence-status vocabulary.

## 1. Checks (`all_link_checks_pass = true`)

| check | result |
|---|---|
| registered / layer is `CORRESPONDENCE` | true |
| evidence status is `BOUNDED_CONDITIONAL_RESULT` | true |
| development status remains `DEFERRED` | true |
| not in the primary development sequence; priority null | true |
| evidence links resolve (file + declared heading) | true |
| names the O7 target anchor | true |
| title carries no promotion wording | true |
| falsifier pins the bounded scope (`manifoldlike emergence`, `native`) | true |
| estimator absent from the supported core exports | true |
| estimator does not classify as supported (`EXPERIMENTAL`) | true |
| scope and open gaps recorded, every gap pointer resolves | true |

`new_evidence_status_introduced = false`; `new_layer_label_introduced = true` (the link is
the registry's only `CORRESPONDENCE` claim — asserted directly).

## 2. The declared scope (pre-specified)

1+1 primary (3+1 not computed, PHYSICS §15) · supplied Minkowski samples, DET inserts no
geometry · verified: T7 estimator behaviour (ordering fraction → Myrheim–Meyer dimension,
link/null diagnostics, counts → conformal profile) as `CORR` · **not claimed**: manifoldlike
emergence, a native (DET-derived) geometry or law map, metric/continuum/curvature/dynamics,
gravity.

## 3. The open-gap register (each with a resolving pointer)

No native growth law is manifoldlike (the O7 target itself) → [QR-05DM](../qr-05dm-stronger-adversary-2026-09-11/RESULTS.md) ·
3+1 and 2+1 rates not computed → `PHYSICS.md` ·
no unconditional uniform LPP concentration proof → [QR-05DD](../qr-05dd-order-only-uniform-bound-2026-09-11/RESULTS.md) ·
density/commensurability uncharacterized → `GEOMETRY_NEXT.md` Tier 2 ·
scale and reference validity not identifiable from one channel → [QR-05CY](../qr-05cy-observational-quotient-2026-09-10/RESULTS.md) ·
the manifoldlikeness certificate is not built → `GEOMETRY_NEXT.md` Tier 2 ·
the Myrheim–Meyer realization wobble (~0.1 at `n ≈ 200`) is unfixed → [QR-05DM](../qr-05dm-stronger-adversary-2026-09-11/RESULTS.md).

## Findings

1. **The link is now referenceable without being promoted.** `DET8-T7-LINK` gives the core
   a scoped pointer to the geometry estimator: layer, evidence status, scope, O7 target and
   open gaps are all in the authoritative registry, so a reader of `det8.claims` cannot
   mistake the estimator benchmark for an emergence result.
2. **The non-promotion invariants are executable, not editorial.** The estimator stays out
   of `SUPPORTED_CORE_EXPORTS` and classifies `EXPERIMENTAL`; the claim holds no priority
   and is absent from the development sequence. Each invariant has a known-answer rejection
   test (a link without the O7 pointer, a promoted evidence status, an invented status
   label, a sequenced or prioritised link, an exported/promoted estimator, a wrong
   development status, an unresolvable link).
3. **This is the deferred change QR-05CY named.** CY mapped its blockage taxonomy onto the
   *existing* evidence axes and asserted `new_status_introduced = false`, explicitly
   deferring adoption into `det8.claims`. J adopts the link as a claim while preserving
   that discipline: no new evidence-status vocabulary, one declared new layer label.

## What this changes and what remains

**Changes.** "The core needs a link" is satisfied in the registry: the T7 estimator is a
first-class, scoped, gated correspondence with its O7 target and open gaps named. The
governed registry (`det8/claims.py`), its generated summary (`docs/CLAIM_REGISTRY.md`) and
its summary test are now committed artifacts.

**Remains.** The link's *content* is unchanged — O7 is still open, and every entry in the
open-gap register stands. The registry's pytest boundary test
(`det8/tests/test_claim_boundaries.py`) pins the claim-id set and has been updated for the
new claim, but is **not** committed here: it imports `det8.core`, whose committed
`event_graph.py` lacks `ScheduleLimitExceeded`, so landing it without the rest of the
uncommitted hardening layer would introduce a failing test. It is updated in the working
tree and should land with that layer. `pytest` is unavailable in this environment, so the
pytest suites are not run here; the executable checks used are the gate's 18 unittest tests
and `python3 scripts/export_claim_registry.py --check`.

No physical, metric, continuum, curvature, dynamics or gravity claim.

## Verification and provenance

`primary.py` reads the **live registry by import**; `reference.py` **parses
`det8/claims.py` with `ast`** and re-derives the entry, the development sequence, the
supported-core export map and the estimator's module status from source, so agreement also
shows the entry is static rather than computed at import. `study.py` refuses on any
difference and freezes the gate sources plus `det8/claims.py` by hash. `test_qr05dn.py`
(18 tests) pins the link's fields, the scope and gap registers, the new-layer assertion and
the seven known-answer failure modes.

- Capture: `results.json`, SHA-256 `6457d9c287de1b7560e297d2e11ef66ba8b04d2f86148d97c756c9e22b94ce1b`.
- Freeze: `source-freeze.json`, SHA-256 `97f977189b1da75b39c8c617bc0c0ffc89403b761f592fe1c4161f0a771109ca` (includes `det8/claims.py`).
- Registry summary: `docs/CLAIM_REGISTRY.md`, regenerated from the registry; verified with
  `PYTHONPATH=. python3 scripts/export_claim_registry.py --check`.

QR-05DN continues the committed `qr-05-bridge` branch (from the QR-05DM commit `f64976f`).
Publication is this directory, [`docs/CLAIM_REGISTRY.md`](../../CLAIM_REGISTRY.md) and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
