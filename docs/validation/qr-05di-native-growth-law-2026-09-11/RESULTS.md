# QR-05DI results

11 September 2026 (Pacific/Honolulu). **A geometry-free native growth law (transitive
percolation) matches the 2-point Myrheim–Meyer dimension of a sprinkle but not its link
structure — it is not manifoldlike, and the 2-point MM test is insufficient.** Direction A
of the Track-B geometry program. Track-B exploratory (Status M); 10 tests pass; no
physical claim.

## 0. Setup

Transitive percolation `TP(n, p)`: birth order `0…n−1`; pair `i < j` related w.p. `p`;
transitive closure. Myrheim–Meyer dimension `d_MM` from the ordering fraction `f`, with
`f_d = Γ(d+1)Γ(d/2)/(2Γ(3d/2))`. Link fraction `ℓ` = Hasse edges / comparable pairs.
`sprinkle_diamond(d, n)` gives the (known manifoldlike) positive control. `n = 150`.

## 1. Calibration — the estimator is validated

| sprinkle | f | d_MM | ℓ |
|---|---|---|---|
| d = 2 | 0.4766 | 2.06 | 0.102 |
| d = 3 | 0.2627 | 2.83 | 0.317 |
| d = 4 | 0.0821 | 4.23 | 0.676 |

`d_MM ≈ d` (within ~0.2), so the geometry-free estimator recovers the sprinkling
dimension — it is a valid, calibrated tool. (The `d = 3` value is ~0.17 low from
finite-size.)

## 2. The native law spans dimensions, but with the wrong link trend

`TP`'s ordering fraction and dimension over `p`:

| p | 0.005 | 0.01 | 0.02 | 0.03 | 0.05 | 0.07 | 0.1 | 0.2 | 0.5 |
|---|---|---|---|---|---|---|---|---|---|
| f | 0.0059 | 0.0204 | 0.0681 | 0.1459 | 0.3562 | 0.5532 | 0.6948 | 0.8753 | 0.9809 |
| d_MM | 7.25 | 5.85 | 4.45 | 3.55 | 2.44 | 1.86 | 1.55 | 1.21 | 1.03 |
| ℓ | 0.775 | 0.551 | 0.287 | 0.188 | 0.098 | 0.065 | 0.052 | 0.034 | 0.021 |

`p` tunes a dimension — but `ℓ` **decreases** with `p`, while for sprinkles `ℓ`
**increases** with `d`. The two families trend oppositely.

## 3. Matched comparison — the decisive mismatch

Interpolating `TP` to each sprinkle's ordering fraction (2-point `d_MM` matches by
construction):

| dim | f | d_MM (matched) | ℓ sprinkle | ℓ TP | ratio | mismatch |
|---|---|---|---|---|---|---|
| 2 | 0.4766 | 2.06 | 0.102 | 0.078 | 0.76 | **yes** |
| 3 | 0.2627 | 2.83 | 0.317 | 0.138 | 0.44 | **yes** |
| 4 | 0.0821 | 4.23 | 0.676 | 0.269 | 0.40 | **yes** |

So `TP` can **match the 2-point dimension** of a sprinkle at a tuned small `p`, but its
**link structure is only 40–76%** of the sprinkle's. It is a different kind of order
(chain-like / closure-dense), not a manifoldlike one.

## Findings

1. **The MM estimator is calibrated** (`d_MM ≈ 2, 3, 4`).
2. **The growth law matches the 2-point dimension** at tuned `p`.
3. **It mismatches the link structure** (40–76%) → **not manifoldlike**.
4. **The 2-point MM test is insufficient**; higher-order statistics are needed.
5. **O7 not achieved** without inserting geometry; the obstruction is a concrete
   higher-order statistic.

## What this changes and what remains

**Changes.** Direction A is opened with a calibrated test and a clear negative: the
simplest geometry-free growth law does **not** produce manifoldlike orders, and the
obstruction is localized to the link/interference structure — not the 2-point dimension.
This *sharpens* O7: the requirement is now a specific higher-order match.

**Remains.** A **DET-native law map** (T8's record-dependent order growth — currently
*assumed* not to affect order growth) tested against the same link/interval discriminator;
whether any geometry-free law satisfies it (or a no-go). No physical, metric, continuum,
curvature, dynamics or gravity claim. Unchanged: gravity standard GR (Option B); curvature
and the imported BD operator parked; κ-gravity retired.

## Verification and provenance

`primary.py` (interval causality; transitive percolation; bisection on the `f_d` curve;
link/interval statistics) and `reference.py` (light-cone-dominance causality; percolation
recoded; bracketing on `f_d`; statistics recoded) compute the calibration, the `TP` sweep,
the matched link comparison and the flags independently — the `TP` RNG stream is shared by
construction (documented). The driver compares with a float tolerance and refuses on any
difference. `test_qr05di.py` pins the `f_d` curve (`f_1 = 1`, `f_2 = ½`), the
chain/antichain controls, and the flags.

- Capture: `results.json`, SHA-256 `bc78cff86e673cf75424e493ec004fac6c918414c42e39f8eec3e1be64d43f77`.
- Freeze: `source-freeze.json`, SHA-256 `32dcdcae178482c21a743be533c78c5be36e774ea9513610fd4a86bfaf05e92f`.

QR-05DI continues the committed `qr-05-bridge` branch (from the E-closure commit
`1f7d32a`). Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
