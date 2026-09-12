# QR-05DH results

11 September 2026 (Pacific/Honolulu). **The true Sorkin–Johnston vacuum from the
Benincasa–Dowker inverse: the Pauli–Jordan function is the light cone, and the SJ state
`W = ½(|Δ| + iΔ)` is Hermitian and strongly positive by construction — no critical mass.**
Track-B exploratory (Status M); a physical *model*. 10 tests pass.

## 0. Setup

BD operator `B = −I + Σ_{n=1}^{N}(−1)^{n+1}C(N,n)A_n` (layer adjacencies), `N = 3`;
retarded Green function `G_R = (B − m²I)⁻¹`; Pauli–Jordan `Δ = G_R − G_Rᵀ`;
`|Δ| = √(−Δ²)`; SJ Wightman `W = ½(|Δ| + iΔ)`. Objects: `2-chain`, `V`, `3-chain`,
`diamond`, sprinklings `n = 6, 8`; masses `m ∈ {0, 0.5, 1, 2}`.

## 1. H1–H3 — light cones, positivity by construction, time reversal (exact)

**H1.** `G_R` is lower-triangular in a linear extension (`B`'s diagonal is `−1−m²`), so
`Δ(x,y) = G_R(x,y) − G_R(y,x)` is nonzero iff `x,y` are causally related — **supp(Δ) is
the light cone** — with sign = orientation. Verified on all 6 objects × 4 masses.

**H2.** `|Δ| = √(−Δ²)` is a function of `Δ`, so `[|Δ|, iΔ] = 0`; the eigenvalues of
`W = ½(|Δ| + iΔ)` are `{0, ν_j}` with `ν_j = √(eig(−Δ²)) ≥ 0`. Hence `W` is Hermitian and
**strongly positive by construction**. Verified `W ⪰ 0` on **24 / 24** (object, mass)
cases.

**H3.** Time reversal `≺ ↦ ≺ᵒᵖ` gives `B ↦ Bᵀ`, `G_R ↦ G_Rᵀ`, `Δ ↦ −Δ`, `|Δ| ↦ |Δ|`; `|W|`
invariant. Verified.

## 2. H4 — the naive symmetrisation fails everywhere here

QR-05DG's kernel `W₀ = ½(G_R + G_Rᵀ) + ½iΔ` (the same BD propagator) is **not** strongly
positive in any of the 24 cases:

| m | 0.0 | 0.5 | 1.0 | 2.0 |
|---|---|---|---|---|
| SJ `W ⪰ 0` / 6 | 6 | 6 | 6 | 6 |
| naive `W₀ ⪰ 0` / 6 | 0 | 0 | 0 | 0 |

So the SJ positive-frequency prescription (the `|Δ|` term) genuinely *creates* the
positive state; the QR-05DG "critical mass" was an artifact of symmetricising `G_R`
instead of taking the positive part of `Δ`.

## Findings

1. **H1:** the physical (Pauli–Jordan) commutator's support is the causal relation — the
   light cones.
2. **H2:** the true SJ state `W = ½(|Δ| + iΔ)` is Hermitian and strongly positive **by
   construction** (`−Δ² ⪰ 0`), for every causal set and mass — **no critical mass**.
3. **H3:** time reversal flips `Δ`, fixes `|Δ|`.
4. **H4:** the naive symmetrisation is not positive; the SJ prescription is what supplies
   the state.
5. **E's coupling, physically:** light cones = `supp Δ`, conformal = `|Δ|`, orientation =
   `iΔ`, and the state is positive — the relational coupling realized by a physical
   two-point function.

## What this changes and what remains

**Changes.** The E thread now has its **physical** conclusion: the true SJ vacuum (BD
inverse + positive-frequency projection) exists, is positive by construction, and its
Pauli–Jordan part is the light cone. The weaker QR-05DG result (a "critical mass") is
superseded — an artifact of the naive symmetrisation, not a physical obstruction.

**Remains.** Sorkin's **uniqueness** conjecture (is the SJ state the unique positive
state determined by `Δ`?); the continuum limit of the BD/SJ construction; the
interpretation of the coupling strength. No physical, metric, continuum, curvature,
dynamics or gravity claim. Curvature and the imported BD operator stay parked; κ-gravity
is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (interval causality; BD operator; Gauss–Jordan retarded inverse;
principal-minor positivity) and `reference.py` (light-cone causality; interval-size
layers; triangular back-substitution inverse; LDL positivity) build the BD operator, the
retarded inverse, `Δ`, the SJ state and its positivity independently; both share a
real-symmetric Jacobi eigensolve for the PSD square root `|Δ|` (standard primitive,
documented). The driver compares with a float tolerance and refuses on any difference.
`test_qr05dh.py` pins the 2-chain `B`/`G_R`/`Δ`, the PSD square root, and the flags.

- Capture: `results.json`, SHA-256 `b8085560432e2c3e09da82684181b7cdf13ee0e4466e23fd76a5a3d2a1ce4741`.
- Freeze: `source-freeze.json`, SHA-256 `f884925277d7418b66be0640606417c027c801a69e4823a4e27af733f076bdee`.

QR-05DH continues the committed `qr-05-bridge` branch (from QR-05DG commit `1b1487c`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
