# QR-05DA results

10 September 2026 (Pacific/Honolulu). **Scale-free LGH convergence re-examined — the
estimator split, with the p99 statistic corrected.** Extending QR-05CZ to `N = 512`,
fitting the decay laws and localizing the ceiling in proper time shows the order-only
chain ceiling is fluctuation-limited at large proper time, while a T7-native
**order+count** reconstruction decays distinctly faster on every statistic. Neither
reconstruction is verified to converge. 21 tests pass. Supplied geometry; no metric,
continuum, curvature or gravity claim.

## 0. Correction record (supersedes the first capture)

The first DA capture mislabelled the **1st** percentile as `p99` (`index = int(0.01 n)`
instead of `ceil(0.99 n) − 1`). Every "bulk (p99)" figure in the first README/RESULTS
was therefore a *lower-tail* statistic read as a bulk/upper statistic. Both routes
shared the misindexing, so their agreement could not detect it. This capture corrects
`_p99`, adds a **median** (the actual bulk) so the typical / upper-tail / ceiling
separation is explicit, and adds **known-answer** tests that pin the statistic
independently of either route. The superseded capture is retained unchanged as
`results.superseded-p01-v1.json`. Full record: [SUPERSEDED.md](SUPERSEDED.md).

What changed: the reported `chain p99` at `N = 512` was `0.0017` → corrected `0.347`;
`count p99` was `0.0010` → corrected `0.187`. The claim "count `p99` below `10⁻²` for
`N ≥ 32`" is withdrawn. The log–log *exponents* were nearly unchanged (both tails of a
roughly self-similar distribution decay at similar rates), so the estimator split
survives; the "essentially exact" reading does not.

## 1. Two reconstructions and the support defects

Both are built from the same causal order on the same sprinkled points with the same
mean spacing `ℓ = √(AREA/N)`:

- order-only: `d_chain(i,j) = (longest chain i → j) · ℓ`;
- order+count: `d_count(i,j) = ℓ · √(1 + m_ij)`, `m_ij = #{k : i ≺ k ≺ j}`.

Support mismatches against the directed Lorentzian distance:

| N | chain vs directed | chain vs symmetric | count (offset) vs directed | count (raw `√m`) vs directed |
|---|---|---|---|---|
| 8 | 0 | 18 | 0 | 12 |
| 32 | 0 | 251 | 0 | 67 |
| 256 | 0 | 15 512 | 0 | 1 025 |

The chain support is exact (CZ's directed correction); the symmetric counterpart is
still flagged as the CZ defect; the unit offset in the count form is what removes its
own link defect (raw `√m` is zero on links, which have positive Lorentzian distance).

**The count form is a distance estimator, not a metric.** On a three-event chain
`a ≺ b ≺ c` with consecutive links, `m_ab = m_bc = 0` and `m_ac = 1`, so
`d(a,c) = ℓ√2` while `d(a,b) + d(b,c) = 2ℓ`: it violates the Lorentzian
reverse-triangle inequality. The directed Lorentzian distance satisfies it
(`2ℓ ≥ ℓ + ℓ`). A known-answer test pins both.

## 2. The trend and the decay law

Multi-seed means (seeds 0–4). For each reconstruction: **typical** = median (nearest
rank), **upper-tail** = 99th percentile (nearest rank), **ceiling** = maximum.

| N | ℓ | chain lower | chain typical (med) | chain upper-tail (p99) | chain ceiling (max) | count typical (med) | count upper-tail (p99) | count ceiling (max) |
|---|---|---|---|---|---|---|---|---|
| 8 | 0.2500 | 0.534544 | 0.245284 | 0.632867 | 0.632867 | 0.387820 | 0.709826 | 0.709826 |
| 16 | 0.1768 | 0.456960 | 0.266882 | 0.809348 | 0.809348 | 0.311755 | 0.709011 | 0.709011 |
| 32 | 0.1250 | 0.354347 | 0.221708 | 0.807275 | 0.819451 | 0.203578 | 0.581837 | 0.590306 |
| 64 | 0.0884 | 0.241945 | 0.171995 | 0.646420 | 0.755269 | 0.143703 | 0.458173 | 0.543114 |
| 128 | 0.0625 | 0.182732 | 0.136575 | 0.526314 | 0.668053 | 0.105538 | 0.344678 | 0.438733 |
| 256 | 0.0442 | 0.159286 | 0.111629 | 0.426187 | 0.597225 | 0.073110 | 0.245217 | 0.349919 |
| 512 | 0.0312 | 0.119507 | 0.089000 | 0.347243 | 0.528983 | 0.054458 | 0.186629 | 0.281019 |

Least-squares log–log decay exponents over the asymptotic range `N ≥ 32`
(`y ~ N^−α`):

| series | α (in N) | equivalent in ℓ (`2α`) |
|---|---|---|
| chain lower bound | 0.373920 | 0.747841 |
| chain typical (median) | 0.325723 | 0.651446 |
| chain upper-tail (p99) | 0.303521 | 0.607043 |
| chain ceiling (max) | 0.160159 | 0.320318 |
| count typical (median) | 0.477969 | 0.955938 |
| count upper-tail (p99) | 0.418272 | 0.836544 |
| count ceiling (max) | 0.277583 | 0.555166 |

The chain bracket does not close: its lower bound decays at `α ≈ 0.37` and its ceiling
at `α ≈ 0.16`. The count reconstruction decays faster on every statistic, and falls
below the chain on the ceiling and the upper tail from `N = 16` (on the median from
`N = 32`). Its 99th percentile at `N = 512` is `≈ 0.19`; smaller and faster-decaying
than the chain's `≈ 0.35`, but not "essentially exact".

## 3. Proper-time localization of the chain ceiling

At `N = 512` (seeds 0–4), pairs binned by `τ/ℓ = (Lorentzian distance)/ℓ`; `ratio` is
the raw longest-chain length divided by `τ/ℓ`.

| τ/ℓ bucket | pairs | max distortion | mean distortion | ratio mean ± sd |
|---|---|---|---|---|
| < 2⁻⁴ | 43 | 0.096413 | 0.086651 | 46.867 ± 51.784 |
| 2⁻⁴…2⁻³ | 155 | 0.089827 | 0.078131 | 10.889 ± 2.192 |
| 2⁻³…2⁻² | 491 | 0.174345 | 0.069433 | 5.499 ± 1.334 |
| 2⁻²…2⁻¹ | 1 605 | 0.223585 | 0.053021 | 2.920 ± 0.903 |
| 2⁻¹…2⁰ | 5 354 | 0.269773 | 0.034754 | 1.702 ± 0.677 |
| 2⁰…2¹ | 15 885 | 0.326802 | 0.057005 | 1.286 ± 0.527 |
| 2¹…2² | 42 503 | 0.373656 | 0.079821 | 1.181 ± 0.362 |
| 2²…2³ | 93 657 | 0.488134 | 0.103874 | 1.188 ± 0.237 |
| 2³…2⁴ | 127 697 | 0.604432 | 0.118209 | 1.232 ± 0.151 |
| 2⁴…2⁵ | 42 064 | 0.604432 | 0.132776 | 1.275 ± 0.110 |

The distortion rises monotonically from near-null pairs (`~0.10`) to large
proper-time pairs (`~0.60`) — the ceiling is **not** a near-null effect. For large
`τ/ℓ` the longest-chain ratio settles at a constant (`≈ 1.2`, absorbed by the scale)
while its relative spread shrinks (`sd 0.53 → 0.11`). What is left is the absolute
chain-length fluctuation, largest at large proper time: the finite-size fluctuation of
the longest-chain estimator.

## Findings

1. **The chain ceiling is fluctuation-limited, not defective.** The certified lower
   bound decays steadily (`α ≈ 0.37`); the natural-correspondence ceiling decays only
   `α ≈ 0.16` and is localized to large proper time. The mechanism is the finite-size
   fluctuation of the longest-chain length — not the directed-distance convention
   (corrected by CZ) and not the near-null pairs.
2. **The order+count reconstruction decays faster on every statistic.** On the same
   points, spacing and scale, its median decays `α ≈ 0.48`, its upper tail `α ≈ 0.42`,
   its ceiling `α ≈ 0.28`. Its 99th percentile is below the chain's from `N = 16`, and
   its ceiling falls below the chain's from `N = 16`. At `N = 512` its `p99` is
   `≈ 0.19` — smaller and faster-decaying, not essentially exact.
3. **The obstruction is estimator-specific.** The reopened convergence question does
   not depend on the directed-distance convention (settled by CZ); it depends on
   which discrete time-separation reconstruction is used.
4. **The count form is an estimator, not a metric.** It violates the Lorentzian
   reverse-triangle inequality on a three-event chain; it compares matrices.
5. **Convergence is not established.** The chain bracket closes at neither finite nor
   measured-asymptotic `N`, and the count ceiling is still `O(0.3)` and its `p99`
   `O(0.1)` at `N = 512` — smaller and faster-decaying than the chain, but not
   verified to reach zero.

## What this changes and what remains

**Changes.** CZ's reopened question is resolved into an estimator dependence: the
order-only longest-chain ceiling is a large-proper-time fluctuation artifact, and the
T7-native order+count reconstruction decays distinctly faster. The `p99` statistic is
corrected, the actual bulk (median) is reported, and the count form is demoted from
"metric" to "distance estimator".

**Remains.** A *constructive* vanishing bound for either reconstruction, and the
statement that the count family yields a metric space with a controlled limit; the
density/commensurability condition; ensemble convergence; manifoldlikeness of a limit.
No metric, continuum, curvature, dynamics or gravity is claimed. Curvature and the
imported BD operator stay parked; κ-gravity is retired and gravity is standard GR
under Option B.

## Verification and provenance

`primary.py` (forward (predecessor) chains, set-intersection counts, golden-section
scale search) and `reference.py` (reverse (successor) chains, bitmask counts, bisection
on the upper/lower envelope crossing) build the matrices, the support checks, the
trend, the decay fits, the localization buckets and the report independently; the
driver compares with a float tolerance and refuses on any difference. Because both
routes once shared the `_p99` misindexing, `test_qr05da.py` now also pins the
percentile and decay-fit semantics with known-answer checks, asserts the ordering
`0 ≤ median ≤ p99 ≤ max` (violated by the defective lower-tail statistic), and tests
the count estimator's reverse-triangle violation. The exact-grid identity-optimality
check (`N ≤ 7`) is retained from CZ; the random-correspondence control is `0.741193`
(identity) vs `3.300735` (random) at `N = 128`.

- Corrected capture: `results.json`, schema `qr05da-capture-v2`, SHA-256 `045c47f5bd9aca6a5a170cc65cdcafeb246c4724e789c7728119ad2d6b32c8cf`.
- Superseded capture: `results.superseded-p01-v1.json`, schema `qr05da-capture-v1`, SHA-256 `d7a9b4c58c34c9b139aa11f230d8e556107b8914b73a59951dca8c5c0da5a8fe`.
- Freeze: `source-freeze.json`, SHA-256 `355f84d4434c71a4e18b585e8d6bbee44a16ed1286126a80827d42da7d28df3a`.

DA continues the committed `qr-05-bridge` branch (from pushed CZ commit `b56af84`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md); the 231
pre-existing dirty entries remain outside it.
