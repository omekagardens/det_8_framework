# Track B — geometry & gravity: next directions (exploratory)

11 September 2026 (Pacific/Honolulu). **Scope: Track-B mathematics, correspondence-level.
"Gravity" here means the kinematic order→geometry link plus the retired dynamics — no
physical claim.** This is a directions map, not a plan commitment.

## 1. What the program is — the quantum↔relativity bridge

The QR-05 program is *"quantum records to geometric structure"*: one primitive set is
meant to generate **both** sides of the quantum/relativity divide.

Primitives (`docs/record_kernel_physics.md` §4): causal event order `(V, ≺)`; counting
measure `#`; local committed record `R`; law map `L`; pair-kernel `𝔇`; composition/commit.

```
R⁻ ──L──▶ (Ω, 𝔄, 𝔇, 𝓒) ──recordable partition──▶ K_𝒫 ──commit──▶ X ──▶ R⁺
```

- **Quantum side (T2/T6):** `𝔇` (Hermitian, biadditive, normalized, strongly positive) ⇒
  an ordinary commit kernel on decoherent partitions, `I₃ = 0`, a Gram representation
  `μ(A)=‖v_A‖²`, and a **correlation class** (T6). This is **Sorkin's decoherence
  functional** — borrowed mathematics, correctly credited.
- **Geometry side (T7/T5):** the order `≺` and the count `#` are meant to reconstruct a
  stable **manifoldlike Lorentzian geometry** (T7), with local operators (d'Alembertian,
  Laplacian) from **kernel moments** (T5).

**The intended bridge is common-primitive:** quantum = pre-commit relational
possibility; geometry = the order-and-count kinematic limit of the same record
structure. **Current status: correspondence/synthetic on both sides** — T6 is borrowed
(dec-Gram), and T7 is validated on *supplied* Minkowski sprinklings (MODEL_CARD **O7:
"Synthetic CORR only"**). There is **no native derivation** from DET primitives yet.

## 2. The open target — a native derivation of geometry (O7)

T7's target theorem: `(≺, #, L, 𝔇) ⇒ stable manifoldlike Lorentzian geometry`, **without
inserting Minkowski**. Stated as four forced objects:

| Object | Native requirement | Anchor / prior art |
|---|---|---|
| **Order** | `≺` must be **generated** by `L`/commit, not declared | Rideout–Sorkin classical sequential growth; transitive percolation (Dowker–Sorkin) |
| **Signature** | Lorentzian (not Riemannian/Galilean), forced by order + dimension | Malament (1977); Hawking–King–McCarthy (1976) — continuum order fixes the metric **up to a conformal factor** |
| **Dimension** | at best *a* `d`; `3+1` is **not** derivable (record_kernel_physics §5) | Myrheim–Meyer dimension estimator |
| **Scale/anchor** | a native scale (order alone is conformal; CY: scale/reference non-identifiable from one channel) | count fixes volume/conformal; an anchor is still needed |

Known edge: the *continuum* order→conformal-metric implication is a theorem; the
*discrete emergence* of a distinguishing manifoldlike order from a growth law is open,
and is exactly where DET can be native rather than correspondence.

## 3. Directions

### Tier 1 — frontier (DET-relevant, research-grade)

| # | Direction | Commitment | Decisive question | Feasibility |
|---|---|---|---|---|
| **A** | **Native growth law → manifoldlike emergence** | T7 (O7) + T8 | Can a DET **law map `L`** grow an order that is manifoldlike — stable Myrheim–Meyer dimension + Bombelli–Henson–Sorkin test — **without inserting Minkowski**? | Bounded: simulate a small sequential-growth / transitive-percolation law, measure MM dimension stability and BHS manifoldlikeness vs sprinkled + adversarial controls. T8 currently **assumes records do not affect order growth** — that assumption is itself a target. **Opened** (QR-05DI): the MM estimator is calibrated, but transitive percolation matches the sprinkle's 2-point dimension and **not** its link structure → the simplest geometry-free law is **not manifoldlike**, and the 2-point test is insufficient — the obstruction is a higher-order statistic. **DET-native step** (QR-05DJ): record-dependent order feedback (T8's assumed-away direction) also fails O7 — it mismatches the link structure and **leaks the record into the order** (κ–degree correlation up to 0.34), a **manifoldlikeness vs record-legibility tension**. **No-go pursued** (QR-05DK): the no-go **fails** — a geometry-free 2-layer bipartite order exceeds the sprinkle's link fraction at every dimension, so the under-linking obstruction is class-specific (closure-dense) and the link fraction alone is insufficient (a preferred foliation, empty intervals). |
| **B** | **The anchor calculus** | identifiability (CY) | What is the **minimal additional channel/anchor** that makes scale + reference + geometry identifiable? | Bounded, executable: extend CY's quotient to `k` channels; show where identifiability flips. This is the finite-observation calculus applied to the link. |
| **C** | **DET-native curvature from kernel moments** | T5 | Can the **T5 kernel-moment** route (not imported Benincasa–Dowker) yield a d'Alembertian→Ricci estimator correct on known curved sprinklings? | Research-grade but sliceable: one estimator, tested on 2-D de Sitter / lumpy manifolds of known scalar curvature. |
| **D** | **LGH convergence as an obstruction** | T7/T5 | Is LGH convergence **equivalent** to uniform LPP concentration + a commensurability condition? (DB/DC/DD reduced order-only to LPP.) | Research-grade: state minimal hypotheses; test where `Vol ∝ τ^d` fails (singular / non-commensurate density). |
| **E** | **𝔇 → conformal/null structure** | T7 + T2/T6 | Does the pair-kernel `𝔇` **force** the light-cone/conformal structure of the emergent geometry (a single-primitive origin for signature)? | Speculative; the most distinctively DET-native bridge idea. **Opened** (QR-05DE): `𝔇` is orientation-blind in magnitude and strong positivity *couples* the kernel to the order, so the single-primitive origin fails as stated — see [E note](E_PAIR_KERNEL_GEOMETRY.md) and [QR-05DE](../validation/qr-05de-pair-kernel-orientation-2026-09-11/README.md); **extended** (QR-05DF): a directed physical propagator recovers the light cones (support) and orientation (phase), with strong positivity the binding constraint; **SJ step** (QR-05DG): the Pauli–Jordan function's support is the light cone and the state condition `W ⪰ 0` holds only above a critical mass; **true SJ vacuum** (QR-05DH): from the Benincasa–Dowker inverse, `W = ½(|Δ|+iΔ)` is positive **by construction** (no critical mass — supersedes DG's). **CLOSED (2026-09-11): relational coupling, not a derivation** — see [E note](E_PAIR_KERNEL_GEOMETRY.md). |

### Tier 2 — benchmark fill-ins (low novelty; the framework explicitly flags them)

| # | Direction | Note |
|---|---|---|
| **F** | **3+1 (and 2+1) rates** | PHYSICS §15: 3+1 is "the slowest and not computed." Needs a d-dim longest-chain (dominance in 4 coords; range-tree DP). Same phenomenon, new dimension. |
| **G** | **Manifoldlikeness certificate from order+count** | BHS/MM test; the "admissibility" predicate for A/D. Borrowed test. |
| **H** | **Estimator-family comparison** | MM estimate, link-based distance, count-corrected chain — compare *uniform* rates. Re-benchmarking. |
| **I** | **Commensurability / density singularities** | Where the volume law fails. |

### Tier 3 — the link into the core

| # | Direction | Note |
|---|---|---|
| **J** | **Governed link entry** | Make the T7 estimator a first-class, scoped component the core references: layer = Correspondence, validation = `BOUNDED_CONDITIONAL_RESULT`, pointer to O7, scope (1+1, supplied geometry) and open gaps. This is the concrete form of "the core needs a link." |

## 4. Recommended sequence

1. **J — link** (cheap; unblocks the core by naming the geometry link explicitly).
2. **B — anchor calculus** (DET-native, novel-flavored, bounded; it is the finite-observation calculus applied to the link).
3. **A — native growth law** (the only direction that addresses O7's actual resolution criterion rather than re-testing supplied geometry).
4. **C** as the operator/curvature step; **E** kept as a flagged long-shot.

Tier 2 (F–I) is worth logging when it closes an explicit framework caveat, not otherwise.

## 5. Discipline (per repo convention)

- **Classification** per `record_kernel_physics.md` §6: `MATH` / `AX-DET` / `TH-DET` /
  `CORR` / `FIT` / `PR` / `EV`. A native derivation must be `TH-DET` with a derivation
  certificate; a supplied-geometry benchmark is `CORR`.
- **Forbidden dependencies** for anything claiming nativity: Lorentzian metric, Minkowski
  coordinates, Hilbert space, target observable formula — unless reconstructed.
- Two independent routes; create-only capture; source freeze; bounded artifacts.
- **Retired / out of scope:** gravity modification, Einstein dynamics (L4), the κ-gravity
  field equation. Reopening any requires a new operational proposal and a named
  discriminator.
- No physical promotion: the geometry link is a correspondence target; Branch B (the
  apparatus) stays `OPEN — PHYSICAL EVIDENCE REQUIRED`.
