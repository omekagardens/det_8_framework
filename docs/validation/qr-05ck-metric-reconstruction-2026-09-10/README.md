# QR-05CK: metric reconstruction / refinement benchmark (supplied geometry)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This extends the metric path by reconstructing the conformal factor from counts
at three densities on a supplied conformally-flat 1+1 geometry, checking BY's
refinement consistency (M6), grid/position robustness, the whole-point
granularity of a count-based estimate (BG), and a non-conformal control.
Supplied geometry; no gravity claim.

Continue [QR-05CJ](../qr-05cj-metric-acceptance-2026-09-10/README.md), the
[BY preregistration](../qr-05by-metric-dynamics-design-2026-09-10/README.md) and
the T7 module `det8/models/order_count_geometry.py`.

## 1. What is measured

On the supplied box with `Ω²(x) = 1 + 4b·x(1−x)` (b=1, a bump vanishing at the
edges), sprinkle N points with density `∝ Ω²(x)` and recover the normalized
conformal-factor profile from binned counts:

| BY test | Check |
|---|---|
| M6 refinement consistency | profiles at N = 1000, 4000, 16000 agree pairwise; MSE-to-truth non-increasing |
| grid / position robustness | the profile is stable under a half-bin grid offset |
| whole-point granularity (BG) | the count-based estimate is granular to `1/mean_count = bins/N` at the lowest density |
| negative control | a uniform sprinkle carries no `Ω` signal |

The whole-point block makes BG's position ambiguity operational: a count in a
bin is a whole number, so a single sprinkling point shifts the local estimate by
`1/mean_count`; this is the irreducible single-point granularity (it shrinks as
N grows, but is never zero at one point).

## 2. Result

Refinement is consistent, MSE-to-truth falls with density, the profile is
grid-robust, the granularity equals `bins/N₀`, and the uniform control fails.
Numbers are in [RESULTS.md](RESULTS.md).

## 3. Boundaries

A bounded estimator check on supplied geometry — not a Lorentzian continuum
limit, not curvature convergence, and **not gravity**. It does not prove that
order+count forces geometry; manifoldlikeness stays open; absolute scale is not
identified. The Lorentzian operator (CI) and curvature stay parked/quarantined.
κ-gravity remains retired; gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` share the supplied sprinkle but implement the
recovery, the pairwise agreement and the control independently; the driver
compares with a float tolerance and refuses on any difference. `study.py`
writes create-only `results.json` and `source-freeze.json`; `test_qr05ck.py`
checks refinement consistency, MSE monotonicity, grid robustness, the
whole-point granularity, the control and route agreement. Fixed seeds make the
run deterministic. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes.
Decision record: [RESULTS.md](RESULTS.md).
