# QR-05DE results

11 September 2026 (Pacific/Honolulu). **The pair-kernel does not force the signature:
it is orientation-blind in magnitude, the conformal ⊕ orientation glue is obstructed,
and orientation is carryable only up to an order-pinned magnitude.** Direction E of the
Track-B geometry program. Toy/structural (`MATH`); 11 tests pass; no physical claim.

## 0. Setup

Finite poset `P = (X, ≺)`. Comparability `C` (symmetric, diagonal 1); orientation `Ω`
(`+1` if `x≺y`, `−1` if `y≺x`, else 0; antisymmetric, diagonal 0). A Hermitian
pair-kernel splits `𝔇 = G + iΩ`. Two constructions: `𝔇₀ = C + iΩ`; `𝔇_r = I + i·r·Ω`.

## 1. E1–E3 — Hermiticity, time reversal, blindness (exact)

**Claim.** `𝔇₀` is Hermitian for every poset; time reversal `τ` (`≺ ↦ ≺ᵒᵖ`) fixes `C`,
flips `Ω`, and preserves `|𝔇|`; `supp(|𝔇|)` off-diagonal is exactly `C`.

*Proof.* `C` symmetric and `Ω` antisymmetric give `𝔇₀† = C − iΩ = 𝔇₀`. `C` depends only on
comparability (invariant under `≺ ↦ ≺ᵒᵖ`), and `Ω` reverses sign. Then
`|𝔇₀| = √(C² + Ω²)` is invariant, and its off-diagonal support is `{C ≠ 0}` = the
comparability relation. ∎

Verified exhaustively (4 472 posets, `n ≤ 5`): `C_invariant`, `Omega_flipped`,
`magnitude_invariant`, `support_is_comparability` all **True**. Hence orientation cannot
be read from `|𝔇|`; at most the undirected conformal structure (Malament;
Hawking–King–McCarthy) can.

## 2. E4 — the naive glue is obstructed (exact)

**Claim.** `𝔇₀ = C + iΩ` is strongly positive **iff** `P` is an antichain.

*Proof.* If `x ≺ y`, the principal submatrix on `{x,y}` is
`[[1, 1+i], [1−i, 1]]`, whose determinant is `1 − (1+i)(1−i) = −1 < 0`; a PSD matrix has
all principal minors `≥ 0`, so `𝔇₀` is not PSD. If `P` is an antichain, `C = I` and
`Ω = 0`, so `𝔇₀ = I ⪰ 0`. ∎

Exhaustive: for `n = 2,3,4,5` exactly `1` of `3/19/219/4231` posets has `𝔇₀ ⪰ 0`, and it
is the antichain. So the interference modulus (`√2`) exceeds the diagonal (`1`): the
"conformal ⊕ i·orientation" product is forbidden by strong positivity.

## 3. E5 — orientation is carryable, magnitude pinned by the order

`𝔇_r = I + i·r·Ω` is Hermitian for every `r`; it is strongly positive for `r ≤ r*(P)`.
`r*(P)` (grid 0.01) is poset-dependent:

| poset | 2-chain | V | 3-chain | diamond |
|---|---|---|---|---|
| `r*` | 1.00 | 0.70 | 0.57 | 0.50 |

`n = 3` distribution: `r* = 1.0` (7 posets), `0.7` (6), `0.57` (6).
`n = 4` distribution: `r* ∈ {0.41(24), 0.44(36), 0.5(6), 0.51(48), 0.57(32), 0.61(24), 0.7(24), 1.0(25)}`.
The antichain and the 2-chain admit full orientation (`r* = 1`); every poset with a
longer order structure admits strictly less. So **strong positivity bounds the
orientation magnitude by the comparability**.

## Findings

1. **E1–E3:** `𝔇` is orientation-blind in magnitude; orientation can only live in
   `arg 𝔇` (the `Ω`/`Im` channel); the undirected conformal candidate is recoverable.
2. **E4:** conformal ⊕ i·orientation is never strongly positive (except antichain).
3. **E5:** orientation is carryable by a strongly positive kernel, but its magnitude is
   pinned by the order (`r*(P) < 1` for structured orders).
4. **Consequence:** the pair-kernel does **not** force the signature/orientation; the
   single-primitive origin for signature fails as stated, but `𝔇` and `≺` are
   **coupled** — the conformal class is shared (`Re 𝔇`), orientation is the directed
   remainder (`Im 𝔇`), and the admissible orientation magnitude is order-set.

## What this changes and what remains

**Changes.** Direction E is refined from a *derivation* ("geometry from `𝔇`") into a
**coupling theorem**: `𝔇` and `≺` are non-redundant and mutually constrained, and the
`𝔇 = G + iΩ` program (`record_kernel_physics.md` §3.4) acquires a geometric reading —
`G` ↔ conformal class, `Ω` ↔ time orientation.

**Remains.** Replace the toy `𝔇` with a **physical** one (quantum sequential growth,
Sorkin–Johnston) and test whether (i) the `G`/`Ω` (conformal/orientation) reading
survives and (ii) `arg 𝔇` reproduces the **light cones** (not just the comparability
graph); interpret `r*(P)` geometrically (a curvature/acceleration bound?); and connect
`r*` to the `why-ℂ` / complex-structure program (§3.4). No metric, continuum, curvature,
dynamics or gravity claim. Curvature and the imported BD operator stay parked; κ-gravity
is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (Boolean-matrix transitivity enumeration; principal-minor strong positivity,
`O(2ⁿ)` minors) and `reference.py` (predecessor-bitmask enumeration with an
ancestral-closure check; LDL semidefinite-Cholesky strong positivity) build the split,
the time-reversal action, the obstruction and the orientation magnitude independently;
the driver compares with a float tolerance and refuses on any difference. `test_qr05de.py`
pins the 2×2 determinant (`−1`), the `r*` values (`1.0 / 0.7 / 0.57 / 0.5`), and the flags.

- Capture: `results.json`, SHA-256 `9ddcca90c0224c87de3a18c375001e10ccc8f42a35adebe84c1d56f062b4d6d7`.
- Freeze: `source-freeze.json`, SHA-256 `4bd2b031293db1b6528422eae26bd3191c58a38fd715cc960a2c789faeedd20e`.

QR-05DE continues the committed `qr-05-bridge` branch (from the geometry-next map commit
`fd57a64`). Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
