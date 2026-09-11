# QR-05CY results

10 September 2026 (Pacific/Honolulu). **Observational quotient and
internal-reference no-go complete — identifiability is separable from empirical
applicability.** On a declared finite class of DET-style worlds the gate computes
the observational quotient exactly, classifies each target, and instantiates the
internal-reference no-go on BW's reference channel. 11 tests pass. No ontological
claim; supplied geometry; no gravity claim.

## The criterion

`W1 ~_O W2` iff the declared interface `O` cannot tell the worlds apart. **P1:**
`τ` is identifiable through `O` iff `τ` is constant on every `O`-class (factors
through `W/~_O`). **P2 (no-go):** if `W1 ~_O W2` and `τ(W1) ≠ τ(W2)`, no
`σ(O)`-measurable `f` — in particular no reference `r_ref = f(O)` from the same
channel — identifies `τ` on `{W1,W2}`. Both are elementary; the gate verifies their
finite instances.

## The computed classification

| family | interface `O` | target `τ` | verdict | witness |
|---|---|---|---|---|
| dimension (d = 2,3,4) | ordering fraction | dimension | IDENTIFIED | — |
| scale (c = 1,2,4) | normalized distances | absolute scale | NON_IDENTIFIABLE | scale1, scale2 |
| scale (c = 1,2,4) | normalized distances + anchor | absolute scale | IDENTIFIED | — |
| conformal (b = 0,2; same events) | interval signs (order) | conformal factor | NON_IDENTIFIABLE | omega0.0, omega2.0 |
| conformal (b = 0,2; sprinkled) | binned count density | conformal factor | IDENTIFIED | — |

## Findings

1. **Dimension factors through the quotient (positive control).** The framework is
   not uniformly negative; an identified target exists on the declared class.
2. **Absolute scale does not (P3).** The scale family is one `O`-class with distinct
   targets; an independent external anchor is *logically necessary*, and adding one
   makes the target identified. This re-derives the CW/CX free-scale degeneracy as
   a statement about identifiability — not about scale being unreal.
3. **The causal order is exactly blind to the conformal factor (P4).** The
   conformally flat worlds `Ω² = 1 + b·x` share the same interval signs, so the
   order channel cannot separate `b`; the count density (marks) identifies it.
4. **The internal-reference no-go holds on the declared channel.** On the witness
   class every declared reference constructor `f(O)` returns identical values, and
   by P2 so does every `σ(O)`-measurable reference: a reference built from the same
   record channel cannot certify a target that varies within an `O`-class. This
   closes the non-empirical half of the BW/P5 blockage *negatively*.

## Taxonomy on the existing registry

Each target carries a **blockage kind** — `DATA` / `CHANNEL` / `MATH` / `GAUGE` —
and an **existing** `det8.claims` evidence status; the gate validates the mapping
against `det8/claims.py` and introduces **no new status vocabulary**
(`new_status_introduced = false`). Adopting the blockage kind into `det8.claims`
would be a governance change through its validator, not this gate.

| target | blockage | evidence status |
|---|---|---|
| dimension | MATH | CORRESPONDENCE_ONLY |
| conformal factor | MATH | CORRESPONDENCE_ONLY |
| absolute scale | CHANNEL | NO_EMPIRICAL_SUPPORT |
| reference validity | CHANNEL | BOUNDED_CONDITIONAL_RESULT |

## What this adds and what remains

Adds an exact, DET-instantiated identifiability criterion, the finite instances P3
and P4, and the internal-reference no-go, and reconciles the blocked-gate taxonomy
with the existing registry. What remains: any claim that an `O`-class corresponds
to one ontology (P5 is Status M, not derived); the apparatus facts of Branch B
(metrology, marks, reference characterization, loss, timebase, support/nesting);
and the scale-free LGH comparison. No metric, manifold, curvature, dynamics or
gravity is claimed. Curvature and the BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (tolerant union–find partition) and `reference.py` (rounded canonical
grouping) build the worlds, the observables, the classification and the no-go
independently; the driver compares with a float tolerance and refuses on any
difference.

- Capture: `results.json`, SHA-256
  `2849ece6d0f077748d87d83038c24a0e221426171ab547b80c708b4f5e001700`.
- Freeze: `source-freeze.json`, SHA-256
  `2bcb7b95b9d29c6ce99d0c0e169c2b4938f5d6ebfe2ecbde3617bf48258c86a1`.

CY continues the committed `qr-05-bridge` branch (from pushed CX commit `b3702fc`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md); the 231
pre-existing dirty entries remain outside it.
