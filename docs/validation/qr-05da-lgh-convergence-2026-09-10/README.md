# QR-05DA: scale-free LGH convergence and the estimator split

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: the chain ceiling is shown to be fluctuation-limited, and a T7-native
order+count reconstruction decays markedly faster on every statistic — the
reopening of QR-05CZ is resolved into an estimator dependence.**

> **Correction (10 September 2026).** The first capture of this gate is
> superseded: its `p99` series was the **1st** percentile, not the 99th, so every
> "bulk (p99)" figure in the first README/RESULTS was a lower-tail statistic
> mislabelled as a bulk/upper statistic. The statistics are corrected here, a
> median (the actual bulk) is reported alongside, and known-answer tests now block
> the shared-error mode. See [SUPERSEDED.md](SUPERSEDED.md).

QR-05CZ corrected the continuum counterpart (the directed Lorentzian distance) and
*reopened* the scale-free convergence question: the certified lower bound decayed,
but the natural-correspondence upper bound was noisy and did not visibly decay.
This gate extends the trend to `N = 512`, fits the decay laws, localizes the ceiling
in proper time, and puts a second, count-based discrete time-separation on the same
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

`d_count` is a **distance estimator, not a Lorentzian metric**. On a three-event
chain `a ≺ b ≺ c` (consecutive links) it gives `d(a,c) = ℓ√2` while
`d(a,b) + d(b,c) = 2ℓ`, so it violates the Lorentzian reverse-triangle inequality
`d(a,c) ≥ d(a,b) + d(b,c)` that a time-separation must satisfy; the directed
Lorentzian distance itself satisfies it. This is pinned by a known-answer test.

## 2. The trend and the decay law

Multi-seed means (seeds 0–4). The certified lower bound is the scale-optimized
sorted-multiset matching bound. For each reconstruction three clearly separated
statistics are reported: the **typical** distortion (median, the bulk), the
**upper-tail** distortion (nearest-rank 99th percentile), and the **ceiling**
(maximum).

| N | ℓ | chain lower | chain typical (med) | chain upper-tail (p99) | chain ceiling (max) | count typical (med) | count upper-tail (p99) | count ceiling (max) |
|---|---|---|---|---|---|---|---|---|
| 8 | 0.250 | 0.5345 | 0.2453 | 0.6329 | 0.6329 | 0.3878 | 0.7098 | 0.7098 |
| 16 | 0.177 | 0.4570 | 0.2669 | 0.8093 | 0.8093 | 0.3118 | 0.7090 | 0.7090 |
| 32 | 0.125 | 0.3543 | 0.2217 | 0.8073 | 0.8195 | 0.2036 | 0.5818 | 0.5903 |
| 64 | 0.088 | 0.2419 | 0.1720 | 0.6464 | 0.7553 | 0.1437 | 0.4582 | 0.5431 |
| 128 | 0.063 | 0.1827 | 0.1366 | 0.5263 | 0.6681 | 0.1055 | 0.3447 | 0.4387 |
| 256 | 0.044 | 0.1593 | 0.1116 | 0.4262 | 0.5972 | 0.0731 | 0.2452 | 0.3499 |
| 512 | 0.031 | 0.1195 | 0.0890 | 0.3472 | 0.5290 | 0.0545 | 0.1866 | 0.2810 |

Least-squares log–log exponents over the asymptotic range `N ≥ 32` (the smallest
sizes carry a coarse-chain transient that is not the asymptotic rate):

| series | decay exponent α in `y ~ N^-α` | equivalent in ℓ (`2α`) |
|---|---|---|
| chain lower bound | 0.374 | 0.748 |
| chain typical (median) | 0.326 | 0.651 |
| chain upper-tail (p99) | 0.304 | 0.607 |
| **chain ceiling (max)** | **0.160** | **0.320** |
| count typical (median) | 0.478 | 0.956 |
| count upper-tail (p99) | 0.418 | 0.837 |
| count ceiling (max) | 0.278 | 0.555 |

The chain's own bracket does not close: its lower bound decays at `α ≈ 0.37` while
its ceiling decays at `α ≈ 0.16`. The count reconstruction decays faster on every
statistic, and its ceiling drops below the chain ceiling from `N = 16`. Its
99th percentile is still `O(0.1)` at `N = 512` — far smaller than the chain's, but
not "essentially exact".

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
2. **The order+count reconstruction decays faster on every statistic.** On the same
   points, scale and conventions, its median decays `α ≈ 0.48`, its upper tail
   `α ≈ 0.42`, and its ceiling `α ≈ 0.28`. It is below the chain on the ceiling and
   the upper tail from `N = 16`, and on the median from `N = 32`. But its 99th
   percentile at `N = 512` is `≈ 0.19` (not `10⁻²`): under the corrected statistics
   the count reconstruction is *smaller and faster-decaying*, not essentially exact.
3. **The obstruction is estimator-specific.** The reopened convergence question does
   **not** depend on the directed-distance convention (settled by CZ); it depends on
   which discrete time-separation reconstruction is used. The order-only
   longest-chain reconstruction does not converge at the measured rate; the
   T7-native order+count reconstruction decays distinctly faster.
4. **The count form is an estimator, not a metric.** `ℓ·√(1+m)` violates the
   Lorentzian reverse-triangle inequality on a three-event chain (`§1`); it compares
   matrices, it does not furnish a metric space.
5. **Not established.** The chain bracket closes neither here nor asymptotically at
   the measured rate, and the count ceiling is still `O(0.3)` and its `p99`
   `O(0.1)` at `N = 512` — smaller and faster-decaying than the chain, but not
   verified to reach zero. Convergence of either is **not** established; the gate
   localizes the obstruction and shows the estimator dependence.

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
difference. Because both routes originally shared the `_p99` misindexing, agreement
alone did not certify the statistic: `test_qr05da.py` now pins the percentile and
decay-fit semantics with **known-answer** checks, guards that `p99 ≥ median ≥ 0`
(which the defective lower-tail statistic violated), and tests the count estimator's
reverse-triangle violation. The exact-grid identity-optimality check (`N ≤ 7`) is
retained from CZ; a random-correspondence control separates the natural
correspondence from chance (0.74 vs 3.30 at `N = 128`). `study.py` writes create-only
`results.json` and `source-freeze.json` (freezing the gate sources and the T7 module
by hash); the superseded first capture is retained as
`results.superseded-p01-v1.json` (see [SUPERSEDED.md](SUPERSEDED.md)). Fixed seeds
make the run deterministic. Limits: sources ≤ 262 144 bytes, artifacts ≤ 16 777 216
bytes. Decision record: [RESULTS.md](RESULTS.md).
