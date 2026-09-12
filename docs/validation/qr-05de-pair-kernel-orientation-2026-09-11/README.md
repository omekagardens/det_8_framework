# QR-05DE: does the pair-kernel force the conformal / orientation structure?

11 September 2026 (Pacific/Honolulu). **Executable, bounded, exact combinatorial.
Outcome: the pair-kernel does not force the signature/orientation — but strong
positivity couples it to the order.** `𝔇` is Hermitian, so `|𝔇|` is time-reversal
blind (orientation can only be in the phase), the naive "conformal ⊕ i·orientation" glue
is never strongly positive, and the admissible orientation magnitude is pinned by the
order. Direction **E** of [GEOMETRY_NEXT.md](../../track_b/GEOMETRY_NEXT.md); design note
[E_PAIR_KERNEL_GEOMETRY.md](../../track_b/E_PAIR_KERNEL_GEOMETRY.md).

## 1. Pre-specification

- **Question.** Does the pair-kernel `𝔇` (Sorkin decoherence functional: Hermitian,
  biadditive, normalized, strongly positive) force the light-cone / conformal structure
  of a causal set — and its time orientation?
- **Model.** A finite poset `P = (X, ≺)`. `C` = comparability (symmetric, diagonal 1);
  `Ω` = orientation (`+1` for `x≺y`, `−1` for `y≺x`, `0` else; antisymmetric, diagonal 0).
  A Hermitian pair-kernel splits as `𝔇 = G + iΩ`.
- **Constructions tested.** naive glue `𝔇₀ = C + iΩ`; unimodular orientation kernel
  `𝔇_r = I + i·r·Ω`, `r ∈ [0,1]`.
- **Admissible class.** all labeled posets with `n ≤ 5` (counts 3, 19, 219, 4231).
- **Strong positivity.** exact, by all principal minors (primary) / LDL (reference).
- **Consequence notion.** does `𝔇` determine `C`/`Ω`, and can orientation be carried by
  a strongly positive kernel at all?

## 2. The split and time reversal

`𝔇(A,B) = conj(𝔇(B,A))` forces `𝔇 = G + iΩ`, `G` symmetric, `Ω` antisymmetric — the
`𝔇 = G + iΩ` program of `record_kernel_physics.md` §3.4. Under time reversal `τ`
(`≺ ↦ ≺ᵒᵖ`): `G ↦ G`, `Ω ↦ −Ω`, so `|𝔇| = √(G²+Ω²)` is `τ`-invariant. Verified on all
4 472 posets: `C` invariant, `Ω` flipped, `|𝔇|` invariant. So the **magnitude is
orientation-blind**, and at most the **undirected** conformal structure (light cones as
sets — Malament; Hawking–King–McCarthy) is recoverable. `supp(|𝔇|)` off the diagonal is
exactly the comparability `C` (verified); the direction is not.

## 3. The obstruction: conformal ⊕ orientation is not strongly positive

For any comparable pair `x ≺ y`, the `2×2` principal minor of `𝔇₀ = C + iΩ` is
`[[1, 1+i], [1−i, 1]]`, with determinant `−1 < 0`. Hence:

| n | labeled posets | `𝔇₀` strongly positive | only the antichain? |
|---|---|---|---|
| 2 | 3 | 1 | yes |
| 3 | 19 | 1 | yes |
| 4 | 219 | 1 | yes |
| 5 | 4 231 | 1 | yes |

So `𝔇` is **not** freely assembled from "conformal ⊕ i·orientation": strong positivity
forbids the *product* of a full-magnitude comparability and a full-magnitude oriented
phase (off-diagonal modulus `√2 > 1`).

## 4. The positive result: orientation is carried, but its magnitude is pinned

`𝔇_r = I + i·r·Ω` is strongly positive for `r ≤ r*(P)`. `r*(P) ∈ (0,1]` is
poset-dependent — the more order structure, the smaller the coherent orientation:

| poset | 2-chain | V | 3-chain | diamond |
|---|---|---|---|---|
| `r*` | 1.00 | 0.70 | 0.57 | 0.50 |

Over all `n = 4` posets, `r*` spreads `0.41 … 1.0` (25 of 219 reach `r* = 1`);
over `n = 3`, `r* ∈ {0.57, 0.70, 1.0}`. The antichain and the 2-chain admit full
orientation; every poset with a longer order structure does not.

## 5. Findings

1. **`𝔇` is orientation-blind in magnitude (E1–E3).** Hermiticity fixes `G`, flips `Ω`
   under `τ`; only the phase `arg 𝔇` can carry orientation — so the *directed* order is
   not recoverable from `|𝔇|`.
2. **Conformal ⊕ i·orientation is obstructed (E4).** The naive glue is strongly
   positive only for the antichain; the interference magnitude is pinned by strong
   positivity, not free.
3. **Orientation is carryable but bounded (E5).** A unimodular orientation kernel is
   strongly positive up to a poset-dependent `r*(P) < 1` whenever the order has
   structure — **strong positivity couples the pair-kernel to the comparability**.

**Consequence (E refined).** The pair-kernel does **not** independently force the
geometry's signature/orientation — so the "single-primitive origin for signature" fails
as stated. But the two are **coupled**: the conformal class is the shared object
(`Re 𝔇` / support), orientation the directed remainder (`Im 𝔇`), and the admissible
orientation magnitude is set by the order. `𝔇` and `≺` are non-redundant and mutually
constrained.

## 6. Boundaries and evidence

Exhaustive exact combinatorics on all labeled posets with `n ≤ 5` (4 472 for the
time-reversal and support checks). It is a **toy/structural model** (`MATH`): `𝔇₀`/`𝔇_r`
are minimal Hermitian constructions, **not** Sorkin's physical decoherence functional,
and no metric, continuum, curvature or gravity claim is made. Replacing the toy `𝔇` with
a physical one (quantum sequential growth / Sorkin–Johnston) and testing whether `arg 𝔇`
reproduces the **light cones** (not just the comparability graph) is the next step.

`primary.py` (Boolean-matrix transitivity scan; principal-minor strong positivity) and
`reference.py` (predecessor-bitmask enumeration with ancestral-closure check; LDL strong
positivity) compute the split, the time-reversal action, the obstruction and the
orientation magnitude independently; the driver refuses on any difference.
`test_qr05de.py` (11 tests) pins the 2×2 determinant, the `r*` values and the flags.
`study.py` writes create-only `results.json` and `source-freeze.json`. Decision record:
[RESULTS.md](RESULTS.md).
