# QR-05DN (direction J): the governed T7 geometry-link entry

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Governance artifact —
correspondence-level (Status M); no physical claim.** Direction J of the Track-B
geometry program: make the T7 order-and-count geometry estimator a **first-class, scoped
component the core may reference, without promoting it**. The link is registered in the
authoritative registry (`det8/claims.py`) as `DET8-T7-LINK`, and this gate checks that
record executably by two independent routes.

This is the concrete form of "the core needs a link" (`GEOMETRY_NEXT.md` §3, Tier 3).

## 1. The link record

| field | value |
|---|---|
| claim ID | `DET8-T7-LINK` |
| title | "T7 order-and-count geometry link (correspondence, bounded)" |
| layer | `CORRESPONDENCE` |
| evidence status | `BOUNDED_CONDITIONAL_RESULT` |
| development status | `DEFERRED` |
| priority | none — **not** in `PRIMARY_DEVELOPMENT_SEQUENCE` |
| dependencies | `DET8-CORE` |
| O7 pointer | `docs/track_b/GEOMETRY_NEXT.md#2-the-open-target--a-native-derivation-of-geometry-o7` |
| falsifier | the link being read as manifoldlike emergence or native geometry, scope exceeded, a geometry-independent law exhibited as manifoldlike, or the estimator shown to need the Lorentzian structure it claims to recover |

Why these fields: the link's *content* is an estimator benchmark — verified on **supplied**
Minkowski samples as `CORR` — so its evidence is bounded and conditional, not a
derivation. Its *development* stays `DEFERRED`: registering the link must not activate the
gated research of the adopted sequence (a registered correspondence is not a licence).
`dependencies=("DET8-CORE",)` records the only thing it actually rests on — the supported
formal core — rather than implying a gate dependency it does not have. It is deliberately
**not** given a `priority`, which is the registry's mechanism for sequence membership.

## 2. Declared scope (pre-specified, in `protocol.json`)

- **Dimensions.** 1+1 primary; 3+1 not computed (PHYSICS §15).
- **Geometry.** Supplied Minkowski samples; DET inserts no geometry.
- **What is verified.** T7 estimator behaviour — ordering fraction → Myrheim–Meyer
  dimension, link/null diagnostics, counts → conformal profile — as `CORR` on generated
  samples.
- **Not claimed.** Manifoldlike emergence · a native (DET-derived) geometry or law map ·
  metric, continuum, curvature or dynamics · gravity.

## 3. Open gaps (recorded, each with a resolving pointer)

| gap | pointer |
|---|---|
| no native growth law is manifoldlike (the O7 target itself) | [QR-05DM](../qr-05dm-stronger-adversary-2026-09-11/RESULTS.md) |
| 3+1 and 2+1 rates are not computed | `PHYSICS.md` |
| no unconditional uniform LPP/longest-chain concentration proof | [QR-05DD](../qr-05dd-order-only-uniform-bound-2026-09-11/RESULTS.md) |
| density/commensurability where `V ∝ τ^d` fails is uncharacterized | [GEOMETRY_NEXT.md](../../track_b/GEOMETRY_NEXT.md) (Tier 2) |
| absolute scale and reference validity are not identifiable from one record channel | [QR-05CY](../qr-05cy-observational-quotient-2026-09-10/RESULTS.md) |
| the manifoldlikeness certificate (BHS/interval test) is not built | [GEOMETRY_NEXT.md](../../track_b/GEOMETRY_NEXT.md) (Tier 2) |
| Myrheim–Meyer estimates carry an unfixed realization wobble (~0.1 at `n ≈ 200`) | [QR-05DM](../qr-05dm-stronger-adversary-2026-09-11/RESULTS.md) |

## 4. Non-promotion invariants (the point of the gate)

Checked executably, and each has a known-answer rejection test:

1. The T7 module (`det8.models.order_count_geometry`) is **absent** from the supported
   core exports and **classifies `EXPERIMENTAL`** — registering the link must not smuggle
   the estimator into the supported surface.
2. The claim is **not** in `PRIMARY_DEVELOPMENT_SEQUENCE` and has **no** `priority`, so it
   cannot unlock gated work.
3. Only the **existing** evidence-status vocabulary is used
   (`new_evidence_status_introduced = false`). One new *layer* label —
   `CORRESPONDENCE` — is introduced, reported explicitly as
   `new_layer_label_introduced = true`; that label is the link's own classification and is
   not an evidence promotion.
4. The title carries no promotion wording and the falsifier pins the bounded scope.

## 5. Evidence

`primary.py` reads the **live registry by import**; `reference.py` **parses
`det8/claims.py` with `ast`** and re-derives the entry, the development sequence, the
supported-core export map and the estimator's module status from source — so agreement
also shows the entry is static, not computed at import. `study.py` refuses on any
difference and freezes the gate sources plus `det8/claims.py` by hash.
`test_qr05dn.py` (18 tests) pins the link's fields, the scope and gap registers, and the
five known-answer failure modes above. The registry's own generated summary
(`docs/CLAIM_REGISTRY.md`) is regenerated from the registry and checked with
`python3 scripts/export_claim_registry.py --check`. Decision record:
[RESULTS.md](RESULTS.md).
