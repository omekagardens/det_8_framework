# QR-05DL results

11 September 2026 (Pacific/Honolulu). **A higher-order manifoldlike invariant: the
interval self-similarity `S = ⟨f(I(x,y))⟩ / f_global`.** Sprinkles are self-similar
(`S ≈ 0.88–1.07` at `n = 250`, and the interval ordering fraction gives the same Myrheim–Meyer
dimension as the global one) while the QR-05DK geometry-free counterexamples fail it
(no intervals, or a large dimension mismatch). Direction A of the Track-B geometry program.
Track-B exploratory (Status M); 11 tests pass; no physical claim.

## 0. Setup

**Invariant.** A manifoldlike causal set is *self-similar*: the interval `I(x,y) = {z : x ≺ z ≺ y}`
of a sprinkle is again a sprinkle of the same dimension, so its ordering fraction should
match the global one —

    S = ⟨f(I(x,y))⟩ / f_global        (over intervals with m_min ≤ |I| ≤ m_max)

with `f(I)` the ordering fraction of the induced order on `I`. Supporting invariants: the
**interval density** `ρ_int = P(I(x,y) nonempty) = 1 − ℓ` over the **complete**
comparable-pair sweep (ℓ the link fraction), and the
**dimension match** `|d_MM(⟨f(I)⟩) − d_MM(f_global)|` (Myrheim–Meyer).

**Objects.** sprinkles `d = 2, 3, 4` (`n = 250`, `seed 7`); transitive percolation
(closure-dense, no geometry) `p = 0.02, 0.05, 0.1`; the complete 2-layer **bipartite** order
(QR-05DK's counterexample); layer-cake `k = 3, 4`. Interval window `m ∈ [3, 30]`, `cap 800`.

## 1. Results (`n = 250`)

| object | `f_global` | `d_MM(global)` | interval density | `⟨f(I)⟩` | `d_MM(interval)` | `S` |
|---|---|---|---|---|---|---|
| sprinkle d=2 | 0.471 | 2.08 | 0.929 | 0.505 | 1.99 | **1.07** |
| sprinkle d=3 | 0.242 | 2.93 | 0.733 | 0.214 | 3.08 | **0.88** |
| sprinkle d=4 | 0.083 | 4.22 | 0.419 | 0.076 | 4.32 | **0.92** |
| TP p=0.02 | 0.120 | 3.78 | 0.844 | 0.815 | 1.32 | **6.77** |
| TP p=0.05 | 0.544 | 1.89 | 0.955 | 0.618 | 1.71 | 1.14 |
| TP p=0.1 | 0.811 | 1.32 | 0.973 | 0.585 | 1.79 | 0.72 |
| bipartite | 0.502 | 1.99 | **0.000** | — | — | — |
| layer-cake k=3 | 0.669 | 1.60 | 0.335 | *(no intervals in range)* | — | — |
| layer-cake k=4 | 0.753 | 1.43 | 0.503 | *(no intervals in range)* | — | — |

The **interval density** column is the corrected v2 statistic (`ρ_int` over the complete
comparable-pair sweep, `= 1 − ℓ`); the original v1 capture reported a partial-sweep
fraction for the rows whose interval sample reached `cap` — see
[SUPERSEDED.md](SUPERSEDED.md). Every other column, the flags and the verdict are
unchanged from v1.

(Sprinkle `d = 4` used 507 intervals; every other row with a defined `S` used the full
`cap = 800`.)

## 2. What the table says

- **Sprinkles pass.** `S` is `1.07, 0.88, 0.92` for `d = 2, 3, 4` — ≈1 up to finite-size
  bias — and the interval ordering fraction reproduces the global dimension to within
  `|Δd_MM| ≤ 0.16` (`0.093, 0.155, 0.098`). The `d = 4` case, which the earlier `n = 120`
  run could not resolve (`S = 0.51`, 46 intervals), is recovered at `n = 250`.
- **Degenerate orders fail (undefined `S`).** The bipartite order has **no intervals**
  (density `0`: every comparability is a cover, so `I(x,y) = ∅`), and the layer-cake's
  intervals are whole layers of size `> 30`, so no interval falls in the tested window.
  Both are geometry-free and leave `S` undefined.
- **Closure-dense laws fail at low `f`.** Transitive percolation at `p = 0.02`
  (`f = 0.120`) has `S = 6.77`: its intervals are far *more* ordered than a sprinkle's
  (`⟨f(I)⟩ = 0.815` vs `0.505`), a dimension mismatch `|Δd_MM| = 2.46`. At higher `f`
  (`p = 0.05, 0.1`) TP is no longer separated by `S` — consistent with QR-05DK's finding
  that the separation is `f`-dependent.
- **Sprinkles are interval-dense.** `ρ_int` is `0.929, 0.733, 0.419` for `d = 2, 3, 4`:
  most comparable pairs in a sprinkle are *not* links (`= 1 − ℓ`), which is the
  manifoldlike behaviour — the degenerate orders are the interval-*sparse* extreme
  (`0` for the bipartite order). *(This bullet reflects the corrected v2 statistic; v1's
  partial-sweep fractions are retained in [SUPERSEDED.md](SUPERSEDED.md).)*

## Findings

1. **Interval self-similarity is a genuine higher-order manifoldlike invariant.** It
   separates sprinkles (`S ≈ 1`) from the QR-05DK geometry-free counterexamples.
2. **It closes the QR-05DK gap.** DK concluded "the link fraction alone is insufficient
   and a no-go needs a higher-order invariant"; this gate exhibits one that *does*
   distinguish — the interval (3-point and higher) structure.
3. **Manifoldlikeness is multi-faceted.** No single invariant (2-point `f`, link `ℓ`,
   interval self-similarity `S`) is sufficient; a no-go is **not** established.
4. **Finite-size caveat.** `S` for sprinkles is finite-size-biased and the `S ∈ [0.8, 1.7]`
   band is a choice; only the low-`f` TP row is cleanly separated by `S` alone.

## What this changes and what remains

**Changes.** Direction A's discriminating invariant is upgraded from the 2-point/link
level (QR-05DK: insufficient) to the higher-order interval level (QR-05DL: sufficient for
the tested counterexamples). The QR-05DK "remains" item — *is the no-go restored with a
higher-order invariant?* — is answered in the negative for these families: a higher-order
invariant separates them, so no no-go is established here.

**Remains.** Whether a no-go holds against a *stronger* adversary (a law engineered to match
`S` at all interval sizes — a covariance/self-similar-ensemble match); a precise
characterization of "geometry-free law"; and the DET-native law question of QR-05DI/DJ. No
physical, metric, continuum, curvature, dynamics or gravity claim. Unchanged: gravity
standard GR (Option B); curvature and the imported BD operator parked; κ-gravity retired.

## Verification and provenance

`primary.py` (interval causality; transitive percolation / bipartite / layer-cake recoded;
`S`, interval density, dimension) and `reference.py` (light-cone-dominance causality;
recoded causality and recoded statistics) compute the invariants and the flags
independently — the RNG streams are shared by construction (documented). The driver
compares with a float tolerance and refuses on any difference. `test_qr05dl.py` (11 tests)
pins the chain known answer (`S = 1`, an interval of a chain is a chain), the bipartite
known answer (`no intervals`), the layer-cake known answer (intervals are whole layers,
so none fall in the window while `ρ_int = s₀s₂/Σsᵢsⱼ` exactly), and the complete-sweep
known answer (`ρ_int = (n−2)/n` for a chain under a small `cap` — the regression test for
the v1 density defect), plus the flags and the capture byte limit.

- Capture: `results.json` (schema `qr05dl-capture-v2`), SHA-256 `cee8dbbce71d6664dc6e42e3a4eab8195da18ec2ae69a403729de72bc635116e`.
- Freeze: `source-freeze.json`, SHA-256 `b392b39dec1e066d5604606a818d35f939010341bef6037facf751a94a2398cb`.
- Superseded capture: `results.superseded-density-v1.json`, SHA-256 `741204843b0882c2a020cf7eecde8c89f6f03811214c3597b23332e8556f1906`
  (v1 `interval_density`; see [SUPERSEDED.md](SUPERSEDED.md)).

QR-05DL continues the committed `qr-05-bridge` branch (from the QR-05DK commit `d41a283`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
