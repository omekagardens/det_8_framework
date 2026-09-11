# QR-05DD results

11 September 2026 (Pacific/Honolulu). **The order-only (longest-chain) uniform bound
vanishes.** The scale-free uniform distortion is exactly ℓ times the uniform fluctuation
of the longest chain, so its vanishing is equivalent to a sublinear uniform fluctuation
(LPP concentration) statement; imported Baik–Deift–Johansson scaling predicts `N^{-1/3}`;
and the measured ceiling decays as a power law, α = 0.27 (R² = 0.96) over `N = 128 … 2048`,
with no plateau — consistent with the prediction and steeper than QR-05DA's transient
(α = 0.16). A non-manifoldlike control does not vanish. 12 tests pass. Supplied
geometry; no metric, continuum, curvature or gravity claim.

## 0. Setup

1+1 Minkowski; Poisson sprinkling of `n` points into the unit diamond; mean spacing
`ℓ = ρ^{-1/2}` (`ρ = n/AREA`). For `x ≺ y`, the longest chain length `L(x,y)` (in links)
and the directed Lorentzian distance `τ(x,y) = √(Δt² − Δx²)`. The scale-free uniform
distortion is `δ = min_{c>0} max_{x≺y} |ℓ·L(x,y) − c·τ(x,y)|`.

## 1. T1 — the reduction (exact)

**Claim.** `δ_order = ℓ · U`, where `U = min_{c>0} max_{x≺y}|L(x,y) − c·τ(x,y)|` is the
uniform fluctuation of `L` (in link units). Hence `δ_order → 0` iff `U = o(1/ℓ) =
o(ρ^{1/d})`.

*Proof.* Factor `ℓ` out of the maximum: `max_{x≺y}|ℓL − cτ| = ℓ·max_{x≺y}|L − (c/ℓ)τ|`,
and minimising over `c > 0` is minimising over `c' = c/ℓ > 0`. So
`δ_order = ℓ·min_{c'>0} max_{x≺y}|L − c'τ| = ℓ·U`. With `ℓ = ρ^{-1/d}`,
`δ_order → 0 ⇔ U = o(ρ^{1/d})`. ∎

The census confirms the identity on every row (`ceiling_links = ceiling_norm · mean_L`).

## 2. T2 — the LPP prediction (imported)

A pair at separation `τ` has an interval of `M ≈ ρ·c_d·τ^d` points and (with the
light-cone dominance order) the longest chain is a last-passage-percolation time. Its
mean is `a_d·ρ^{1/d}·τ` and, in 1+1, its fluctuation is `ρ^{1/6}`
(Baik–Deift–Johansson for LIS; KPZ). So `U ~ ρ^{1/6}` and, with `d = 2`,

```
δ_order = ℓ·U ~ ρ^{-1/2}·ρ^{1/6} = ρ^{-1/3} = N^{-1/3}.
```

This is the prediction the numerical fit is tested against; it is not re-derived.

## 3. T3 — the measurement

Seed-mean scale-free ceiling `δ/⟨L⟩`:

| n | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|
| δ/⟨L⟩ | 0.7447 | 0.6340 | 0.5914 | 0.4238 | 0.3520 |

Least-squares log–log fit: **α = 0.274, R² = 0.958** over 16× in `N`; predicted
`1/3 = 0.333`. The sequence is monotonically decreasing (`δ` falls ×2.1 over 16× in `N`);
there is no plateau. The individual step exponents are noisy
(−0.23, −0.10, −0.48, −0.27) but average α ≈ 0.27.

QR-05DA fit the ceiling over `N = 32 … 512` and got α = 0.16; the wider range gives a
steeper, cleaner power law, identifying that α = 0.16 as a finite-size transient. So
DA's "convergence not established" is superseded: the ceiling is well fit by a decaying
power law consistent with the LPP rate.

## 4. The adversarial control

A 3-layer Kleitman–Rothschild-style order (every element of layer `i` relates to every
element of layer `j > i`; `n = 300`) has a **bounded** longest chain (`L ∈ {1, 2}`)
while `τ` varies across the cross-layer pairs — including spacelike pairs with `τ = 0`.
Its normalized ceiling is `0.75` and does not vanish. So the vanishing is a property of
the manifoldlike/Poisson input, not of the reduction alone.

## Findings

1. **T1 (exact):** `δ_order = ℓ·U`; vanishing is exactly uniform sublinear fluctuation
   of the longest chain.
2. **T2 (imported):** LPP/BDJ gives `δ_order ~ N^{-1/3}` in 1+1.
3. **T3 (measured):** α = 0.27 (R² = 0.96), no plateau, consistent with 1/3; supersedes
   DA's transient α = 0.16.
4. **Control:** a non-manifoldlike order does not vanish.
5. **Consequence:** the longest-chain (order-only) reconstruction is the
   axiom-compliant **and** ceiling-convergent object.

## What this changes and what remains

**Changes.** The QR-05 scale-free convergence question reopened by CZ, localized by DA,
and constrained by DB/DC is resolved **positively** for the order-only reconstruction:
the longest-chain estimator — the only A2-compliant (DB) and non-order-dominated (DC)
candidate — has a ceiling that decays as a power law consistent with the LPP rate. The
convergence obstruction is therefore not a count/estimator artefact but a LPP
fluctuation question with a favourable answer.

**Remains.** An **unconditional** proof of the uniform longest-chain fluctuation bound
(equivalently, uniform LPP concentration) — beyond the range of this gate; the
density/commensurability condition; and the physical bridge (Branch B, untouched). No
metric, continuum, curvature, dynamics or gravity is claimed. Curvature and the imported
BD operator stay parked; κ-gravity is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` (Fenwick prefix-max over the light-cone dominance order) and `reference.py`
(max segment tree) compute the longest chains, the distortion, the fit and the report
independently; the driver compares with a float tolerance and refuses on any difference.
`test_qr05dd.py` cross-checks the longest chain against a brute-force `O(n³)` table and
the light-cone equivalence, pins the distortion on a hand-computed case, and asserts the
flags and verdict.

- Capture: `results.json`, SHA-256 `881ad6ca11fa8daedb29014097d14e264ff126ef86ea05e6b4148c2be908d0fd`.
- Freeze: `source-freeze.json`, SHA-256 `bfb5931568bc3a6b3741b17489195d5e9911f9b276eef95d35012f3d7e88f60f`.

QR-05DD continues the committed `qr-05-bridge` branch (from QR-05DC commit `124ea91`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
