# QR-05DD: the order-only uniform bound — the longest-chain ceiling vanishes

11 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: the order-only (longest-chain) reconstruction's scale-free uniform distortion
is shown to decay as a power law with no plateau, exponent ≈ 0.27, consistent with the
last-passage-percolation prediction 1/3 — so the longest-chain reconstruction is the
axiom-compliant (DB/DC) object and its ceiling is supported to vanish.**
**Scope: bounded 1+1 numerics on supplied Minkowski geometry — correspondence-level
(the T7 order→geometry *link*), not DET manifold emergence; the LPP-concentration proof
and the 3+1 case (PHYSICS §15) remain open.** No metric, continuum, curvature or gravity
claim.

Follows [QR-05DC](../qr-05dc-max-plus-closure-2026-09-11/README.md) and gives a bounded
1+1 numerical answer to the scale-free convergence question reopened by
[QR-05CZ](../qr-05cz-scale-free-lgh-2026-09-10/README.md) and left open by
[QR-05DA](../qr-05da-lgh-convergence-2026-09-10/README.md).

## 1. Pre-specification (fixed before the computation)

- **Question.** Does the order-only longest-chain reconstruction's scale-free uniform
  (max-over-pairs) distortion vanish as the sprinkling density grows?
- **Geometry.** 1+1 Minkowski, Poisson sprinkle into the unit diamond; mean spacing
  `ℓ = √(AREA/n)`, `n ∈ {128, 256, 512, 1024, 2048}`, seeds `{0, 1, 2}`.
- **Order.** In light-cone coordinates `u = t−x`, `v = t+x` the causal order is exactly
  the 2-D **dominance order**: `p ≺ q ⇔ (u_p < u_q and v_p < v_q)`. The longest chain
  is therefore a **last-passage-percolation / LIS** functional, computed in
  `O(n² log n)`.
- **Scale/anchor.** Homothety only; the absolute scale is non-identifiable (QR-05CY).
- **Convergence notion.** Scale-free `L∞` distortion
  `δ = min_{c>0} max_{x≺y} |ℓ·L(x,y) − c·τ(x,y)|`.
- **Constructive bounds.** The reduction `δ = ℓ·U` (§2) and the LPP prediction (§3).
- **Adversarial control.** A 3-layer Kleitman–Rothschild-style order (non-manifoldlike),
  in which the longest chain is bounded while the reference time varies.

## 2. The reduction (T1, exact)

Let `U = min_{c>0} max_{x≺y} |L(x,y) − c·τ(x,y)|` be the uniform fluctuation of the
longest chain (in link units). Then

```
δ_order = ℓ · U .
```

Because `ℓ = ρ^{-1/2}` (d = 2), `δ_order → 0` **iff** `U = o(ρ^{1/2})`, i.e. iff the
longest-chain fluctuation is sublinear in the mean chain length. So the order-only
uniform question is *exactly* a uniform concentration question for the longest chain —
not a causal-set-specific question. The census confirms `δ = ℓ·U` (`ceiling_links =
ceiling_norm · mean_L` on every row).

## 3. The measurement (T3) — a power law, no plateau

Scale-free `L∞` ceiling (seed means; `δ/⟨L⟩`, dimensionless — the DA-comparable
statistic):

| n | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|
| ceiling `δ/⟨L⟩` | 0.7447 | 0.6340 | 0.5914 | 0.4238 | 0.3520 |

Least-squares log–log fit over `n = 128 … 2048`: **exponent α = 0.274, R² = 0.958**, on a
range of 16× in `N`. This is steeper than QR-05DA's small-range fit (α = 0.16 over
`N = 32 … 512`, a finite-size transient) and consistent with the LPP prediction
`N^{-1/3}` (α = 0.333, within 0.06). The sequence is monotonically decreasing with no
plateau: `δ` falls by a factor 2.1 over 16× in `N`, matching a power law (a plateau
would flatten).

**The LPP prediction (T2, imported).** A pair at time-separation `τ` has an interval of
`M ≈ ρ·c₂·τ²` points; the longest chain is a last-passage-percolation time,
`L = a₂·ρ^{1/2}·τ` with fluctuation `ρ^θ`, and in 1+1 `θ = 1/6` (Baik–Deift–Johansson).
Then `U ~ ρ^{θ}` and `δ = ℓ·U ~ ρ^{θ−1/2} = ρ^{-1/3} = N^{-1/3}`.

**The adversarial control.** A 3-layer Kleitman–Rothschild-style order has a *bounded*
longest chain (`≤ 2`) while the reference time-separation varies (including spacelike
cross-layer pairs with `τ = 0`): its normalized ceiling is `0.75` and does **not**
vanish. Convergence therefore needs the manifoldlike/Poisson input; the reduction T1
alone does not give it.

## 4. Findings

1. **Reduction (T1, exact).** The order-only scale-free uniform distortion is exactly
   `ℓ` times the uniform fluctuation of the longest chain; it vanishes iff that
   fluctuation is sublinear in `ρ^{1/2}`.
2. **Prediction (T2).** Imported LPP/BDJ scaling gives a per-pair fluctuation `ρ^{1/6}`
   and hence `δ ~ N^{-1/3}` in 1+1.
3. **Measurement (T3).** Over `N = 128 … 2048` the ceiling decays as a power law,
   α = 0.27 (R² = 0.96), no plateau — consistent with the 1/3 prediction and steeper
   than DA's transient.
4. **Control.** A non-manifoldlike layered order does not vanish.
5. **Consequence (scoped).** The **longest-chain (order-only) reconstruction is the
   axiom-compliant (DB/DC) one and its ceiling is supported to vanish** in bounded 1+1
   numerics. This is correspondence-level — the T7 order→geometry *link* on supplied
   geometry, the route that produced the finite-observation calculus — not a
   DET-emergence claim. The remaining gaps are an *unconditional* proof of the uniform
   longest-chain fluctuation bound (a LPP concentration problem) and the 3+1 case.

## 5. Boundaries

A bounded numerical study on supplied geometry plus an exact reduction. It supports
(does **not** prove) the vanishing of the order-only uniform distortion: the fit spans
16× in `N` and is consistent with the LPP rate, but a finite range cannot prove an
asymptotic statement, and the LPP fluctuation scaling is imported. It makes no metric,
continuum, curvature, dynamics or gravity claim. Curvature and the imported BD operator
stay parked; κ-gravity is retired and gravity is standard GR under Option B.

## 6. Evidence and limits

`primary.py` (Fenwick prefix-max longest chain over the light-cone dominance order) and
`reference.py` (max segment tree) build the longest chains, the distortion, the fit and
the report independently; the driver compares with a float tolerance and refuses on any
difference. `test_qr05dd.py` (12 tests) cross-checks the longest chain against a
brute-force `O(n³)` table and the light-cone equivalence, pins the distortion on a
hand-computed case (`L=[1,3], τ=[1,2] ⇒ 1/3`), and asserts the flags/verdict.
`study.py` writes create-only `results.json` and `source-freeze.json`. Fixed seeds make
the run deterministic. Limits: sources ≤ 262 144 bytes, artifacts ≤ 16 777 216 bytes.
Decision record: [RESULTS.md](RESULTS.md).
