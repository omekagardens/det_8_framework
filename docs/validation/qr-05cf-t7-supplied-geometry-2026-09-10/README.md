# QR-05CF: supplied-geometry (T7) benchmark

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This is the geometry path's legitimate input: the T7 order-and-count estimators
run on *known* Lorentzian sprinklings. It verifies that the estimators recover
dimension, null structure and the conformal factor on data whose geometry is
supplied, and that a non-diamond control fails. It does not derive geometry and
does not touch gravity.

Continue [QR-05CD](../qr-05cd-det-data-routing-2026-09-10/README.md) (routing)
and the T7 module `det8/models/order_count_geometry.py`.

## 1. Purpose

Per the routing rule, the geometry chain consumes a **supplied Lorentzian
geometry and its causal order/count**. Here the supplied geometry is a
Minkowski causal diamond, sprinkled with a fixed seed, so the causal order and
the counting measure are the module's `(≺, #)` and the analytic geometry is
known. The benchmark checks the estimators against that known geometry; it is
`CORR` (estimator verification), not emergence — the manifoldlikeness problem
stays open, exactly as the module's certificate states.

## 2. What is verified

| Check | Fixture | Criterion |
|---|---|---|
| Dimension recovery (order+count) | sprinkled diamonds, d=2,3,4, N=400 | ordering fraction within tolerance of `r(d)=Γ(d+1)Γ(d/2)/[2Γ(3d/2)]`; nearest-reference dimension equals d |
| Order → null structure | d=2, N=60 | mean link nullness is nearer null than the mean over all comparable pairs |
| Count → conformal factor | 1+1 conformal sprinkle, `Ω²=1+bx`, b=1 | recovered count profile matches the normalized truth; MSE below tolerance; profile monotone |
| Conformal invariance of order | toy interval signs | causal order unchanged for `Ω²∈{0.5,1,3,100}` |
| Negative control | uniform box (not a diamond) | its ordering fraction differs from the diamond `r(2)` |

`primary.py` calls the module's estimators; `reference.py` re-implements the
causality, ordering fraction, links/nullness, analytic fraction and conformal
recovery independently, taking only the sprinklings from the module. The two
reports must agree exactly (floats rounded to 12 decimals).

## 3. Result

All five checks pass; see [RESULTS.md](RESULTS.md) for the numbers. The point
is narrow and honest: the T7 estimators work on supplied geometry, and the
dimension estimator is calibrated to the *diamond* — a box sprinkling does not
recover it, which is why the routing rule requires the correct supplied
geometry rather than any point cloud.

## 4. Boundaries

Estimator verification on supplied geometry, not emergence. No manifoldlike
uniqueness, no continuum-limit theorem, no curvature, and **no gravity** is
claimed. The module's own derivation certificate governs: order⇒conformal and
count⇒conformal-factor are imported mathematics, the verification is
synthetic/CORR, and manifoldlikeness is open. κ-gravity is retired; gravity is
standard GR under Option B. This gate changes no data and makes no physical
claim.

## 5. Evidence and limits

`study.py` writes create-only `results.json` and `source-freeze.json` (freezing
the gate sources and the T7 module by hash); tests in `test_qr05cf.py`
re-check every section plus route agreement and the negative control. Fixed
seeds make the run deterministic and replayable. Limits: sources ≤262,144
bytes, artifacts ≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
