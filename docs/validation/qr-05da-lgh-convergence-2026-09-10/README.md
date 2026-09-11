# QR-05DA: scale-free LGH convergence and the estimator split

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: the chain ceiling is shown to be fluctuation-limited, and a T7-native
order+count reconstruction decays markedly faster — the reopening of QR-05CZ is
resolved into an estimator dependence.** QR-05CZ corrected the continuum
counterpart (the directed Lorentzian distance) and *reopened* the scale-free
convergence question: the certified lower bound decayed, but the
natural-correspondence upper bound was noisy and did not visibly decay. This gate
extends the trend to `N = 512`, fits the decay laws, localizes the ceiling in
proper time, and puts a second, count-based discrete time-separation on the same
scale-free footing. No metric, continuum, curvature or gravity is claimed.

Continue [QR-05CZ](../qr-05cz-scale-free-lgh-2026-09-10/README.md) and the recorded Next.

## 1. Two discrete time-separations, one comparison

Both reconstructions are built from the same causal order `prec` on the same
sprinkled points and the same mean spacing `ℓ = √(AREA/N)`, and are compared to the
directed Lorentzian distance under a global homothety:

```text
inf over c > 0 of  min over bijections sigma of  max over pairs |d_X(i,j) - c d_Y(sigma i, sigma j)|.
```

- **order-only** (QR-05CW…CZ): `d_chain(i,j) = (longest chain i → j) · ℓ`.
- **order+count** (T7-native): `d_count(i,j) = ℓ · √(1 + m_ij)`, where
  `m_ij = #{k : i ≺ k ≺ j}` is the number of points strictly between `i` and `j`.

The unit offset keeps links positive so the count support matches the directed
Lorentzian distance; the raw `√m` form is zero on links (a support defect — 12/67/1025
mismatches at N = 8/32/256, vs 0 with the offset), which is the reason for the offset.

## 2. The trend and the decay law

Multi-seed means (seeds 0–4). The certified lower bound is the scale-optimized
sorted-multiset matching bound; `p99` is the 99th-percentile pair distortion at the
optimal scale (the bulk).

| N | ℓ | chain ceiling | chain lower bound | chain bulk (p99) | count ceiling | count bulk (p99) |
|---|---|---|---|---|---|---|
| 8 | 0.250 | 0.6329 | 0.5345 | 0.0192 | 0.7098 | 0.0599 |
| 16 | 0.177 | 0.8093 | 0.4570 | 0.0146 | 0.7090 | 0.00659 |
| 32 | 0.125 | 0.8195 | 0.3543 | 0.0039 | 0.5903 | 0.00281 |
| 64 | 0.088 | 0.7553 | 0.2419 | 0.0031 | 0.5431 | 0.00339 |
| 128 | 0.063 | 0.6681 | 0.1827 | 0.0026 | 0.4387 | 0.00210 |
| 256 | 0.044 | 0.5972 | 0.1593 | 0.0021 | 0.3499 | 0.00145 |
| 512 | 0.031 | 0.5290 | 0.1195 | 0.0017 | 0.2810 | 0.00104 |

Least-squares log–log exponents over the asymptotic range `N ≥ 32` (the smallest
sizes carry a coarse-chain transient that is not the asymptotic rate):

| series | decay exponent α in `y ~ N^-α` | equivalent in ℓ (`2α`) |
|---|---|---|
| chain lower bound | 0.374 | 0.748 |
| chain bulk (p99) | 0.307 | 0.614 |
| **chain ceiling (max)** | **0.160** | **0.320** |
| count ceiling (max) | 0.278 | 0.555 |
| count bulk (p99) | 0.409 | 0.818 |

The chain's own bracket does not close: its lower bound decays at `α ≈ 0.37` while
its ceiling decays at `α ≈ 0.16`. The count reconstruction decays faster than the
chain on both statistics, and its ceiling drops below the chain ceiling from
`N = 16`.

## 3. The chain ceiling is localized at large proper time

At `N = 512` (seeds 0–4), pairs binned by `τ/ℓ = (Lorentzian distance)/ℓ`. `ratio`
is the raw longest-chain length divided by `τ/ℓ`.

| τ/ℓ bucket | pairs | max distortion | mean distortion | ratio mean ± sd |
|---|---|---|---|---|
| < 2⁻⁴ | 43 | 0.0964 | 0.0867 | 46.9 ± 51.8 |
| 2⁻⁴…2⁻³ | 155 | 0.0898 | 0.0781 | 10.9 ± 2.2 |
| 2⁻³…2⁻² | 491 | 0.1743 | 0.0694 | 5.50 ± 1.33 |
| 2⁻²…2⁻¹ | 1 605 | 0.2236 | 0.0530 | 2.92 ± 0.90 |
| 2⁻¹…2⁰ | 5 354 | 0.2698 | 0.0348 | 1.70 ± 0.68 |
| 2⁰…2¹ | 15 885 | 0.3268 | 0.0570 | 1.29 ± 0.53 |
| 2¹…2² | 42 503 | 0.3737 | 0.0798 | 1.18 ± 0.36 |
| 2²…2³ | 93 657 | 0.4881 | 0.1039 | 1.19 ± 0.24 |
| 2³…2⁴ | 127 697 | 0.6044 | 0.1182 | 1.23 ± 0.15 |
| 2⁴…2⁵ | 42 064 | 0.6044 | 0.1328 | 1.28 ± 0.11 |

The distortion grows monotonically from near-null pairs (`~0.10`) to large
proper-time pairs (`~0.60`): the chain ceiling is **not** a near-null discretisation
effect. For large `τ/ℓ` the longest-chain ratio settles at a constant
(`ratio → ≈ 1.2`, absorbed by the scale) while its **relative** spread shrinks
(`sd 0.53 → 0.11`). What remains is the absolute chain-length fluctuation, which is
largest at large proper time — the finite-size fluctuation of the longest-chain
estimator.

## 4. Findings

1. **The chain ceiling is fluctuation-limited, not defective.** The certified lower
   bound decays steadily (`α ≈ 0.37`), but the natural-correspondence ceiling decays
   only `α ≈ 0.16` and is localized to large proper time (§3). The mechanism is the
   finite-size fluctuation of the longest-chain length, not the directed-distance
   convention (corrected by CZ) and not the near-null pairs.
2. **The order+count reconstruction decays faster.** On the same points, scale and
   conventions, the count reconstruction has a ceiling decaying `α ≈ 0.28` and a
   bulk `p99` decaying `α ≈ 0.41` (consistent with Poisson counting, which predicts
   a `~m^{-1/2}` relative error and hence `~N^{-1/2}` bulk decay). Its `p99` is
   below `10⁻²` for `N ≥ 32`, and below the chain `p99` for `N ≥ 128` (the small-`N`
   values cross a few times within seed noise).
3. **The obstruction is estimator-specific.** The reopened convergence question does
   **not** depend on the directed-distance convention (settled by CZ); it depends on
   which discrete time-separation reconstruction is used. The order-only
   longest-chain reconstruction does not converge at the measured rate; the
   T7-native order+count reconstruction converges distinctly faster.
4. **Not established.** The chain bracket closes neither here nor asymptotically at
   the measured rate, and the count ceiling is still `O(0.3)` at `N = 512` — smaller
   and faster-decaying than the chain, but not verified to reach zero. Convergence
   of either is **not** established; the gate localizes the obstruction and shows the
   estimator dependence.

## 5. Boundaries

A bounded computation on supplied geometry. It fits decay laws, localizes the ceiling
in proper time, and compares two reconstructions. It does **not** establish the
scale-free LGH infimum or convergence for either reconstruction, the
density/commensurability condition, ensemble convergence, or manifoldlikeness of a
limit, and it makes no metric, continuum, curvature, dynamics or gravity claim. The
count reconstruction is a *bounded diagnostic*, not a convergence theorem; its
distortion is a matrix comparison, not a proof that the count family yields a metric
space with a controlled limit. Curvature and the imported BD operator stay parked;
κ-gravity is retired and gravity is standard GR under Option B.

## 6. Evidence and limits

`primary.py` (forward (predecessor) chains, set-intersection counts, golden-section
scale search) and `reference.py` (reverse (successor) chains, bitmask counts,
bisection on the upper/lower envelope crossing) build the matrices, the support
checks, the trend, the decay fits, the localization buckets and the report
independently; the driver compares with a float tolerance and refuses on any
difference. The exact-grid identity-optimality check (`N ≤ 7`) is retained from CZ;
a random-correspondence control separates the natural correspondence from chance
(0.74 vs 3.30 at `N = 128`). `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05da.py` checks the support defects, the trend and decay ordering, the
proper-time localization, the count crossover, the non-claim of convergence and
route agreement. Fixed seeds make the run deterministic. Limits: sources
≤ 262 144 bytes, artifacts ≤ 16 777 216 bytes. Decision record: [RESULTS.md](RESULTS.md).
