# QR-05CJ results

10 September 2026 (Pacific/Honolulu). **Metric-acceptance benchmark complete.**
On a supplied conformally-flat 1+1 geometry the conformal factor is recovered
from counts (up to scale), the causal order is conformal-invariant and
boost-covariant, and a non-conformal control fails. 8 tests pass. Supplied
geometry; no gravity claim.

## Conformal-factor recovery (BY M5)

`Ω²(x) = 1 + sin(πx)`, N=4000, 12 bins; recovered normalized count profile vs
the normalized truth, MSE = **0.003167** (below 0.01):

```text
recovered 0.741 0.837 0.930 1.059 1.254 1.167 1.269 1.263 1.050 0.921 0.777 0.732
truth     0.690 0.844 0.982 1.095 1.174 1.215 1.215 1.174 1.095 0.982 0.844 0.690
```

The profile is recovered up to sampling scatter; the `sin(πx)` shape is visible
and the endpoints are lowest.

## Order/count separation and scale (BY M5)

- **Order is conformal-invariant:** multiplying the interval by `Ω²>0` (tested
  at 0.5, 1, 3) leaves every causal sign unchanged — the order fixes only the
  conformal class.
- **Scale is not identified:** sampling accepts with probability `Ω²/Ω²_max`, so
  rescaling `Ω²` by a constant leaves the normalized recovered profile
  identical. The count profile fixes `Ω` only up to an overall factor.

## Covariance and control (BY M3)

- **Boost covariance:** the flat causal order is preserved exactly under a
  Lorentz boost β=0.4 (159,598 / 159,598 sampled non-null pairs).
- **Non-conformal control:** a uniform sprinkle gives MSE 0.0327 versus 0.0032
  for the conformal case — a 10× separation, so the recovery is doing real work.

## Boundaries

A bounded estimator check on supplied geometry — not a Lorentzian continuum
limit, not curvature convergence, and not gravity. It does not prove that
order+count forces geometry; manifoldlikeness stays open. Absolute scale is
explicitly not identified. The Lorentzian-operator / Benincasa–Dowker benchmark
is **parked** (the 2D operator could not be validated; see the roadmap), and the
curvature modules remain quarantined. κ-gravity is retired; gravity is standard
GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` share the supplied sprinkle (fixture) but
implement the recovery and the invariance/covariance checks independently; the
driver compares with a float tolerance and refuses on any difference. Fixed
seeds make the run deterministic.

- Capture: 959 bytes;
  SHA-256 `9819916ddf2c1065fece348cad94fe70db9c784e4787d28602eeef670420e7fa`.
- Freeze: SHA-256
  `287034dc6c436e21dbcf3350c2995606dcbd05d5e2246f7d7df31b421e408188`.

CJ continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
