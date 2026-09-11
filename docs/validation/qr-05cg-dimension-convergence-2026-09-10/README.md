# QR-05CG: dimension-convergence benchmark (1+1 vs 3+1)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This addresses the recorded caveat that the continuum diagnostics were measured
only in 1+1 Minkowski and the physically relevant 3+1 rate was not computed
(PHYSICS §15). It measures the covering/fill-in rate of supplied sprinklings in
d=2 (1+1) and d=4 (3+1). It is a finite convergence diagnostic, not a
continuum-limit theorem and not gravity.

Continue [QR-05CF](../qr-05cf-t7-supplied-geometry-2026-09-10/README.md) and the
T7 module `det8/models/order_count_geometry.py`.

## 1. What is measured

For a sprinkle of N points in the d-dimensional unit causal diamond, the mean
nearest-neighbour distance scales as the covering scale

```text
<NN>(N)  ~  N^(−1/d).
```

So the log-log exponent is −1/2 in d=2 (1+1) and −1/4 in d=4 (3+1) — the
"3+1 is the slowest" statement, made quantitative. N runs over a declared grid
with several seeds; the exponent is a least-squares fit; the two routes compute
the nearest-neighbour statistic and the fit independently.

## 2. Result

Both exponents land within the declared 0.05 tolerance of `−1/d`, and the
3+1 magnitude is the smaller (slowest). See [RESULTS.md](RESULTS.md). The point
is narrow: the physically relevant dimension converges more slowly, as
recorded, and the diagnostic is now computed rather than assumed.

## 3. Boundaries

A bounded finite-range exponent fit on supplied sprinklings — not a
continuum-limit proof, not manifoldlikeness, not curvature, and **not gravity**.
The measured exponents carry finite-N and finite-range error and are
implementation diagnostics. κ-gravity remains retired; gravity is standard GR
under Option B. No apparatus is involved and no physical claim is made.

## 4. Evidence and limits

`study.py` writes create-only `results.json` and `source-freeze.json` (freezing
the gate sources and the T7 module by hash); `test_qr05cg.py` checks the
exponents, the 3+1-slowest ordering, monotone `<NN>` and route agreement. Fixed
seeds make the run deterministic. Limits: sources ≤262,144 bytes, artifacts
≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
