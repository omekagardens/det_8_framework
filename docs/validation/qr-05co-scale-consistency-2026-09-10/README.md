# QR-05CO: T7/T5 scale-consistency witness (C5)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
Charter §7.3: the T7/T5 bridge must survive **grouping records at different
scales**. From one sprinkle this witnesses that the coarse-grained
reconstruction is consistent for both the T7 geometry and the T5 operator, and
that the bridge holds at both scales. Supplied geometry; no gravity claim.

Continue [QR-05CN](../qr-05cn-t7-t5-bridge-2026-09-10/README.md) (the bridge it
this tests).

## 1. What is measured

One sprinkle with `Ω²(x) = 1 + a sin(2πx)`, N=8000. Two record scales: a fine
binning (`m_fine = 16`) and a coarse binning (`m_coarse = 8 = m_fine/2`), with
the T5 kernel evaluated at bandwidths `w` and `2w`.

| Check | Definition |
|---|---|
| **Coarse-graining identity** | aggregating the fine counts pairwise equals the directly-binned coarse counts (exact) |
| **Geometry scale-consistency** | the aggregated fine *normalized* profile equals the coarse normalized profile (ratio 1) |
| **Operator scale-consistency** | the T5 kernel coefficient from bandwidth `w` equals that from `2w` (correlation high, ratio 1) |
| **Bridge at both scales** | corr(T7 profile, T5 kernel) high at both `w` and `2w` |
| **Control** | the *raw* count is scale-dependent (its magnitude doubles from fine to coarse), so it is **not** scale-consistent; only the intensive (normalized) reconstruction is |

## 2. Result

All consistency checks pass and the control exhibits the raw-count scale
dependence; numbers in [RESULTS.md](RESULTS.md). The finding is that the
reconstruction must be **intensive** (a density, not a count) to be
scale-consistent — which is exactly what T7's conformal factor and T5's
kernel-moment coefficients are.

## 3. Boundaries

A bounded witness on supplied geometry — not a coarse-graining theorem, not
curvature, and not gravity. It does not prove that order+count forces geometry
(T7 stays open). The full composed model (CN) and the empirical bridge remain
open. Curvature and the imported BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` implement the two scales, the profiles, the
bridge correlations and the control independently; the driver compares with a
float tolerance and refuses on any difference. `study.py` writes create-only
`results.json` and `source-freeze.json`; `test_qr05co.py` checks the
coarse-graining identity, geometry and operator scale-consistency, the
both-scale bridge, the raw-count control and route agreement. Fixed inputs make
the run deterministic. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216
bytes. Decision record: [RESULTS.md](RESULTS.md).
