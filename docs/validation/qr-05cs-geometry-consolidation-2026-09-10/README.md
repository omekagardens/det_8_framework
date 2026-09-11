# QR-05CS: T7/T5 geometry program consolidation

10 September 2026 (Pacific/Honolulu). **Design-only consolidation.** This states,
in one place and without overclaim, what the geometry chord CF–CR establishes,
under which DET commitments, and what remains open. It performs no new
computation and promotes nothing.

Continue the chord [QR-05CF](../qr-05cf-t7-supplied-geometry-2026-09-10/README.md) …
[QR-05CR](../qr-05cr-no-double-counting-2026-09-10/README.md).

## 1. Commitment routing

Each gate is routed to the DET theorem it instantiates (`docs/record_kernel_physics.md` §10):

| Theorem | Gates | Content |
|---|---|---|
| **T7** Order-and-Count Geometry (kinematic) | CF, CG, CJ, CK | dimension, null structure, conformal factor up to scale, refinement/1+1-vs-3+1 rates |
| **T5** Local Kernel Continuum | CH, CL, CM, CP, CR | diffusion, wave and variable-coefficient drift-diffusion operators from kernel moments; the composed conservative operator |
| **T6** Correlation-Class | CE | Bell/Tsirelson + Fisher–Rao history distance (off this chord) |
| bridge | CN, CO | the T5 kernel derived from the same `(≺,#,L)`; compatibility (C1–C3) and scale consistency (C5) |
| control | CQ | adversarial non-manifoldlike rejection (charter §7.4) |
| reclassified | CI | the Benincasa–Dowker operator is imported causal-set MATH (CORR), not the DET-native T5 route |

## 2. What is established (bounded)

- **T7 kinematic reconstruction** on *supplied* Lorentzian sprinklings:
  dimension recovered for d=2,3,4; links nearer null than generic comparable
  pairs; conformal factor recovered from counts up to one scale; refinement-
  consistent and boost-covariant; covering rate −0.506 (1+1) vs −0.265 (3+1).
- **T5 operators from kernel moments**: diffusion (Laplace–Beltrami), the
  reversible wave operator `∂_t²−∂_x²`, and variable-coefficient drift-diffusion
  — exact on quadratics, second-order convergence, coefficients = the kernel's
  moments.
- **T7/T5 bridge**: the kernel derived from the same records is compatible with
  the geometry (0.973 vs 0.009 control), scale-consistent (C5), composed into one
  operator whose coefficient is the T7 geometry (0.993), and audited to have no
  hidden source (C6).
- **Control**: a non-manifoldlike order matched to `r(d)` is rejected by link
  structure.

## 3. What is **not** established

- **Manifoldlikeness / genuine emergence** — open. Every result is estimator
  verification (`CORR`) on supplied or synthetic geometry, not emergence.
- **Absolute scale** — not identified (BL/BM/BN).
- **Curvature** — the curvature/Bianchi modules are quarantined (retired
  gravity); no curvature claim is made.
- **A Lorentzian operator via the naive BD route** — not validated (CI
  reclassified); the DET-native wave route is T5/CL.
- **Continuum-limit theorems** (LGH metric convergence, Benincasa–Dowker action)
  — open and shared with causal-set theory.
- **Gravity / dynamics** — out of scope: T7 is kinematic and "gravity stays out
  of scope until this kinematic theorem succeeds"; κ-gravity is retired and
  gravity is standard GR under Option B.
- **The empirical bridge** — requires an apparatus satisfying BX; unsupplied.

## 4. Classification

Every gate in the chord is analytical derivation, exact finite verification, or
synthetic numerical `CORR` on supplied geometry, with an independent reference
and a control. None is a measured-data analysis, an emergence proof, or a
physical claim.

## 5. Charter obligations (§7)

| Obligation | Status |
|---|---|
| 1 specify events/records/order; modeled vs reconstructed | design done (CN §4); apparatus spec is BX (unsupplied) |
| 2 a single compatible history/composition model | witnessed (CN), composed (CP), audited (CR) — not proved |
| 3 scale consistency under grouping | witnessed (CO) |
| 4 estimators on known and adversarial models | CF/CG (known), CQ (adversarial) |
| 5 stable continuum geometry + dynamics | open (LGH; dynamics out of scope) |

## 6. Decision boundary

This is a consolidation only: no new result, no promotion, no metric, manifold,
curvature, dynamics or gravity claim. The chord's frontier is the empirical
bridge (BX) on one side and the continuum-limit theorems (LGH) on the other;
both are unsolved and neither is assumed here.
