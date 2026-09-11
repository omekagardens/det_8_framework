# QR-05CK results

10 September 2026 (Pacific/Honolulu). **Metric reconstruction / refinement
benchmark complete.** On a supplied conformally-flat 1+1 geometry the conformal
factor is reconstructed from counts, refinement is consistent, MSE-to-truth
falls with density, the profile is grid-robust, the whole-point granularity is
the declared `bins/N`, and a non-conformal control fails. 8 tests pass.
Supplied geometry; no gravity claim.

## Refinement consistency (BY M6)

`Ω²(x) = 1 + 4x(1−x)`, 12 bins, fixed seed:

| N | mean count/bin | MSE to truth |
|---|---|---|
| 1000 | 83.33 | 0.021401 |
| 4000 | 333.33 | 0.002923 |
| 16000 | 1333.33 | 0.000260 |

MSE-to-truth is monotonically decreasing, and consecutive profiles agree
pairwise (MSE 0.012687, 0.002783 — both below the 0.05 consistency tolerance).
So the reconstruction is refinement-consistent and improves with density.

## Grid robustness and whole-point granularity (BG)

- **Grid robustness:** shifting the bin grid by half a bin changes the profile
  by MSE 0.007712 (< 0.05) — the reconstruction is not an artifact of bin
  placement.
- **Whole-point granularity:** a bin count is a whole number, so a single
  sprinkling point shifts the local estimate by `1/mean_count = bins/N`. At the
  lowest density this is `12/1000 = 0.012`. This is BG's position ambiguity made
  operational: the pointwise conformal factor is determined only to within the
  effect of one whole point, an ambiguity that shrinks with N but is never zero
  at a single point.

## Negative control

A uniform (non-conformal) sprinkle gives MSE 0.040215 versus 0.000260 for the
conformal case at N=16000 — the reconstruction is detecting the supplied `Ω`,
not a bias.

## Boundaries

A bounded estimator check on supplied geometry — not a Lorentzian continuum
limit, not curvature convergence, and not gravity. It does not prove that
order+count forces geometry; manifoldlikeness stays open; absolute scale is not
identified. The Lorentzian operator (CI) and curvature stay parked/quarantined.
κ-gravity remains retired; gravity is standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` share the supplied sprinkle (fixture) but
implement the recovery, the pairwise agreement and the control independently;
the driver compares with a float tolerance and refuses on any difference. Fixed
seeds make the run deterministic.

- Capture: 2,602 bytes;
  SHA-256 `d8208d30ccd3280bd4a47423df10e1826793776ee7a9cc77d399f0997fc899b5`.
- Freeze: SHA-256
  `847adc93f0c170f8dbf0db18cc14be4bbc2a8d93285742b5eb4ff26a8677e13f`.

CK continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
