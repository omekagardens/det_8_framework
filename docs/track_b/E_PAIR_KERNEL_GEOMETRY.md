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

## Physical 𝔇 (QR-05DF)

E's next step replaces the toy `𝔇` with a **directed, local, physical-flavored kernel**:
the free link-path propagator `K = (I − L)⁻¹` (`K(x,y)` = number of link-chains `x → y`),
with `G = K + Kᵀ`, `Ω = K − Kᵀ`, `𝔇_K = G + iΩ`. On small causal sets:

- `supp(K)` off the diagonal is exactly the **directed** causal relation — the local
  propagator recovers the **light cones**;
- `G` is the **undirected** (conformal) comparability, orientation-invariant;
- the **sign of `arg 𝔇_K`** is the orientation (`+` for `x≺y`, `−` for `y≻x`);
- time reversal acts as conjugation (`K↦Kᵀ`), `|𝔇_K|` invariant;
- **strong positivity is not automatic** (3 of 6 objects).

So E's coupling **survives** the toy → physical step: the conformal class and orientation
are realized as `supp` + `arg`, and strong positivity remains the binding constraint.
See [QR-05DF](../validation/qr-05df-physical-pair-kernel-2026-09-11/README.md).

## Physical 𝔇: Sorkin–Johnston (QR-05DG)

E's next step takes the **physical** structure explicitly: a retarded Green function
`G_R`, its **Pauli–Jordan** part `Δ = G_R − G_Rᵀ` (antisymmetric; the commutator) and its
**Hadamard** part `H = G_R + G_Rᵀ`, and the **Wightman** two-point function
`W = ½H + ½iΔ`. With the causal-set chain (resolvent) propagator `G_R(m) = (I − e^{−m}L)⁻¹`:

- **`supp Δ` is exactly the causal relation — the light cones** (the physical locality
  statement, and precisely E's coupling);
- `W` is Hermitian, with symmetric (conformal) `H` and antisymmetric (orientation) `iΔ`;
- time reversal flips `Δ` and fixes `H`;
- the **SJ state condition `W ⪰ 0` holds only above a critical mass** (`m = 0`: 3 of 6
  objects; `m ≥ 0.5`: 6 of 6) — a physical, mass-dependent binding constraint.

So the physical two-point function **realizes E's coupling** and needs a mass/IR
regularisation on a finite causal set. See
[QR-05DG](../validation/qr-05dg-sorkin-johnston-2026-09-11/README.md).

## True SJ vacuum (QR-05DH)

Using the **Benincasa–Dowker d'Alembertian** `B = −I + Σ_{n}(−1)^{n+1}C(N,n)A_n` (layer
adjacencies) and its retarded inverse `G_R = (B − m²I)⁻¹`, the **true SJ state** is
`W = ½(|Δ| + iΔ)`, `Δ = G_R − G_Rᵀ`, `|Δ| = √(−Δ²)`. It is **Hermitian and strongly
positive by construction** (`−Δ² ⪰ 0`, eigenvalues `{0, ν_j}`) for every causal set and
mass — **no critical mass** — while the naive symmetrisation of the same propagator is
positive in **0 / 24** cases. `supp Δ` is again the causal relation (the light cones). So
the QR-05DG "critical mass" is **superseded**: it was an artifact of symmetricising `G_R`
instead of taking the positive part of `Δ`. E's coupling now holds with a genuine
physical positive state. See
[QR-05DH](../validation/qr-05dh-sj-vacuum-bd-2026-09-11/README.md).

## Ontological reading — the relational coupling (Status M)

The "strong no / coupled yes" is DET's ontological view, stated explicitly:

- **Strong no:** `𝔇` does not reduce to — and does not subsume — the causal order.
  `𝔇` and `≺` are **non-redundant**.
- **Coupled yes:** they are **mutually constrained** — the conformal class is the shared
  object (`Re 𝔇` / `supp`), orientation the directed remainder (`arg 𝔇` / `Im`), and
  strong positivity bounds how they combine. This **relational coupling** (not a
  reduction) is exactly the ontology DET adopts.

DET may be **missing primitives** for a complete account — the true physical `𝔇`
(Sorkin–Johnston / QSG) is unbuilt and the coupling strength uninterpreted — so this is
used **exploratorily** in Track B: coherent and motivating, but **not hardened** into a
core claim. Its role is to *shape* the search for the missing primitives, not to assert
their existence.

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
