# QR-05DH: the true Sorkin–Johnston vacuum from the Benincasa–Dowker inverse

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — a physical *model*, not a physical claim.** E's next step, done properly:
the **true SJ vacuum**. With the Benincasa–Dowker d'Alembertian `B` and its retarded
inverse `G_R = (B − m²I)⁻¹`, the Pauli–Jordan function `Δ = G_R − G_Rᵀ` is supported
**exactly on causally related pairs — the light cones** — and the SJ Wightman function
`W = ½(|Δ| + iΔ)` (`|Δ| = √(−Δ²)`) is **Hermitian and strongly positive by
construction, for every causal set and every mass — no critical mass.** The
QR-05DG critical mass was an artifact of the naive symmetrisation.

## 1. Pre-specification

- **Question (E next step).** The true physical pair-kernel: SJ vacuum from the BD
  inverse — light cones and a positive state.
- **BD operator.** `B = −I + Σ_{n=1}^{N} c_n A_n`, `c_n = (−1)^{n+1} C(N,n)`, `A_n[x][y] = 1`
  iff `y ∈ L_n(x)` (the `n`-th layer below `x`, `|I(y,x)| = n−1`); `N = 3`.
- **Retarded Green function.** `G_R = (B − m²I)⁻¹` (lower-triangular in a linear
  extension ⇒ retarded).
- **SJ state.** Pauli–Jordan `Δ = G_R − G_Rᵀ` (real antisymmetric); `|Δ| = √(−Δ²)` (PSD
  square root); Wightman `W = ½(|Δ| + iΔ)` — the unique state determined by `Δ` alone.
- **Objects / masses.** `2-chain`, `V`, `3-chain`, `diamond`, sprinklings `n = 6, 8`;
  `m ∈ {0, 0.5, 1, 2}`.
- **Status.** Track-B exploratory; `N` and the overall normalisation are conventions (the
  SJ structure is scale-invariant).

## 2. Results

**H1 — the Pauli–Jordan light cones.** `supp(Δ)` off the diagonal is exactly the causal
relation (sign = orientation), on every object and mass.

**H2 — the SJ state is Hermitian and strongly positive by construction.** `|Δ|` is a
function of `Δ`, so it commutes with `iΔ`; the eigenvalues of `W = ½(|Δ|+iΔ)` are
`{0, ν_j}` with `ν_j = √(eig(−Δ²)) ≥ 0`. Verified: `W ⪰ 0` for **6 / 6 objects at every
mass** (24 / 24).

**H3 — time reversal.** `≺ ↦ ≺ᵒᵖ` gives `B ↦ Bᵀ`, `G_R ↦ G_Rᵀ`, so `Δ ↦ −Δ` and `|Δ| ↦ |Δ|`
(`|W|` invariant). Verified.

**H4 — the naive symmetrisation is not positive.** QR-05DG's kernel
`W₀ = ½(G_R + G_Rᵀ) + ½iΔ` (the same BD propagator) is positive for **0 / 24**
(object, mass) cases. So the SJ positive-frequency prescription genuinely *creates* the
positive state — the "critical mass" was a symplectic-structure artifact.

| m | 0.0 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|
| SJ state `W ⪰ 0` / 6 | 6 | 6 | 6 | 6 |
| naive `W₀ ⪰ 0` / 6 | 0 | 0 | 0 | 0 |

## 3. Reading

The **true** physical two-point function realizes E's coupling:
**light cones = `supp Δ`**, **conformal = `|Δ|`** (orientation-invariant), **orientation
= `iΔ`**, and the **SJ state is positive** — so the relational coupling holds with a
genuine positive state, not a critical-mass-tuned one. This closes the E thread of the
bridge with a physical, not toy, object.

## 4. Boundaries

The SJ structure is realized with the **chain/resolvent** retarded Green function `G_R`
(as in QR-05DG) generalized to the **BD d'Alembertian's inverse**; `N` and the overall
normalisation are conventions (the structure is invariant). The exact SJ state's
**uniqueness** (Sorkin's conjecture) and the continuum limit are not addressed. No
physical, metric, continuum, curvature or gravity claim. The geometry/quantum link
remains correspondence-level and Status M.

## 5. Evidence

`primary.py` (interval causality; BD operator; Gauss–Jordan retarded inverse;
principal-minor positivity) and `reference.py` (light-cone causality; interval-size
layers; triangular back-substitution inverse; LDL positivity) compute the BD operator,
the retarded inverse, `Δ`, the SJ state and its positivity independently; both share a
real-symmetric Jacobi eigensolve for the PSD square root `|Δ|` (a standard primitive,
documented). The driver refuses on any difference. `test_qr05dh.py` (10 tests) pins the
2-chain `B`/`G_R`/`Δ`, the PSD square root, and the flags. `study.py` writes create-only
`results.json` and `source-freeze.json`. Decision record: [RESULTS.md](RESULTS.md).
