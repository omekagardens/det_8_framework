# Track B — E: does the pair-kernel force the conformal / orientation structure?

11 September 2026 (Pacific/Honolulu). **Status: opened; first bounded result obtained
(QR-05DE). Track-B mathematics; toy/structural model, no physical claim.**

## The question

Direction E of [GEOMETRY_NEXT.md](GEOMETRY_NEXT.md): the DET bridge thesis is that the
pair-kernel `𝔇` (the quantum primitive — Sorkin's decoherence functional: Hermitian,
biadditive, normalized, strongly positive) and the causal order `≺` (the geometry
primitive) are two faces of one record-relational structure. The sharp form:

> Does `𝔇` **force** the light-cone / conformal structure — and, if so, its **time
> orientation**?

## The structure

For a finite causal set, `𝔇(A,B) = conj(𝔇(B,A))` (Hermiticity) forces the split

```
𝔇 = G + iΩ ,   G symmetric (real),   Ω antisymmetric (real) ,
```

matching the `𝔇 = G + iΩ` program of `record_kernel_physics.md` §3.4. Under **time
reversal** `τ` (`≺ ↦ ≺ᵒᵖ`), `G ↦ G` and `Ω ↦ −Ω`. Two immediate consequences:

1. **The magnitude is orientation-blind.** `|𝔇| = √(G²+Ω²)` is `τ`-invariant, so the
   *directed* order cannot be recovered from `|𝔇|`; at most the **undirected**
   conformal structure (light cones as sets — Malament; Hawking–King–McCarthy) can be.
2. **Orientation can only live in the phase** `arg 𝔇 = atan2(Ω, G)`, which is
   `τ`-odd.

## First bounded result (QR-05DE)

On all posets with `n ≤ 5` (labeled counts 3, 19, 219, 4231):

- **Obstruction.** The naive glue `𝔇₀ = C + iΩ` (comparability `C` + orientation `Ω`)
  is strongly positive **only for the antichain** — for any comparable pair `x ≺ y`,
  the `2×2` minor `[[1, 1+i],[1−i, 1]]` has determinant `−1 < 0`. So `𝔇` is **not**
  freely assembled from "conformal ⊕ i·orientation": strong positivity forbids it.
- **Positive.** A unimodular orientation kernel `𝔇_r = I + i·r·Ω` **is** strongly
  positive up to a poset-dependent maximal magnitude `r*(P) ∈ (0,1]`: `2`-chain `1.0`,
  `V` `0.7`, `3`-chain `0.57`, diamond `0.5`; over `n = 4`, `r*` spreads `0.41 … 1.0`.
  So **orientation can be carried in the phase, but its magnitude is pinned by the
  order** — the more order structure, the smaller the coherent orientation.

## Resolution of E

`𝔇` does **not** independently force the conformal/orientation structure: the
magnitude is `τ`-blind, and the orientation is a phase whose admissible magnitude is
set by the order. But the two are **coupled**: strong positivity bounds the interference
magnitude (the orientation carrier) by the comparability structure. So E refines from a
*derivation* ("geometry from `𝔇`") into a **coupling theorem** — `𝔇` and `≺` are
non-redundant and mutually constrained, and the conformal class is the shared object
(`Re 𝔇`/support), orientation the directed remainder (`Im 𝔇`).

So the single-primitive origin for signature **fails as stated**; a *shared-origin*
refinement survives, and the pair-kernel is not a substitute for the order.

## Prior art

Sorkin decoherence functional / quantum measure theory (Hermiticity, strong positivity);
Malament (1977), Hawking–King–McCarthy (1976) (order ⇒ conformal metric; orientation
extra); quantum sequential growth (Rideout–Sorkin) for a physical `𝔇`; the `𝔇 = G + iΩ`
complex-structure program (`record_kernel_physics.md` §3.4).

## What would advance E

- Replace the toy `𝔇` with a **physical** one (QSG / Sorkin–Johnston) and test the
  `G`/`Ω` (conformal/orientation) reading there.
- Determine whether the maximal coherent orientation `r*(P)` has a geometric
  interpretation (e.g., a bound on the field's curvature/acceleration).
- Test whether the phase structure `arg 𝔇` reproduces the **light cones** (not just the
  comparability graph) — the local/interval condition.

## Bounded gate

[QR-05DE](../validation/qr-05de-pair-kernel-orientation-2026-09-11/README.md) — two
independent routes, exhaustive small-`n`, create-only capture. MATH/toy; no physical
claim.
