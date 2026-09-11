# QR-05CJ: metric-acceptance benchmark (supplied geometry)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This resumes the metric/dynamics path by exercising BY's metric-interpretation
acceptance tests on a supplied conformally-flat 1+1 geometry. It verifies that
the conformal factor is recovered from counts (up to an overall scale), that
the causal order is conformal-invariant and boost-covariant, and that a
non-conformal control fails. Supplied geometry; no gravity claim.

Continue [QR-05CH](../qr-05ch-laplacian-convergence-2026-09-10/README.md), the
[BY preregistration](../qr-05by-metric-dynamics-design-2026-09-10/README.md) and
the T7 module `det8/models/order_count_geometry.py`.

## 1. What is measured

On the supplied box `[0,1]²` with the conformally-flat metric
`Ω²(x) = 1 + b·sin(πx)` (b=1), sprinkle N points with density `∝ Ω²(x)` and:

| BY test | Check |
|---|---|
| M5 scale declaration | recover the normalized `Ω²` profile from binned counts; MSE below tolerance |
| order/count separation | the causal order is conformal-invariant (`Ω²>0` preserves interval signs); only counts see `Ω` |
| M3 covariance | the flat causal order is preserved under a Lorentz boost |
| negative control | a uniform, non-conformal sprinkle carries no `Ω` signal |

Scale is **not** identified: because sampling accepts with probability
`Ω²/Ω²_max`, rescaling `Ω²` by a constant leaves the normalized profile
unchanged — the count profile fixes `Ω` only up to a factor.

## 2. Result

Recovery MSE, the invariance/covariance checks and the control are in
[RESULTS.md](RESULTS.md). The gate confirms the T7/BY statement: order fixes the
conformal class, counts fix the conformal factor up to scale.

## 3. Boundaries

A bounded estimator check on supplied geometry — not a Lorentzian continuum
limit, not curvature convergence, and **not gravity**. It does not prove that
order+count forces geometry; the manifoldlikeness problem stays open. Absolute
scale is explicitly *not* identified (BL/BM/BN). The Lorentzian operator /
Benincasa–Dowker benchmark remains **parked** (the 2D operator could not be
validated; see the roadmap), and the curvature modules stay quarantined.
κ-gravity remains retired; gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` share the supplied sprinkle but implement the
recovery and the invariance/covariance checks independently; the driver
compares with a float tolerance and refuses on any difference. `study.py`
writes create-only `results.json` and `source-freeze.json`; `test_qr05cj.py`
checks recovery, invariance, covariance, the control and route agreement.
Fixed seeds make the run deterministic. Limits: sources ≤262,144 bytes,
artifacts ≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
