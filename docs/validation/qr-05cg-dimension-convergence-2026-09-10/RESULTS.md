# QR-05CG results

10 September 2026 (Pacific/Honolulu). **Dimension-convergence benchmark
complete.** The covering/fill-in rate of supplied sprinklings is measured in
1+1 and 3+1; both exponents match `−1/d` within tolerance and the 3+1 magnitude
is the slowest, making the recorded caveat quantitative. Finite diagnostic;
not a continuum-limit theorem and not gravity.

## Measured exponents

Mean nearest-neighbour distance `<NN>(N)` over N ∈ {125, 250, 500, 1000} and
five seeds; the exponent is a least-squares fit to `log<NN>` vs `log N`.

| d | `<NN>` at N=125 … 1000 | measured exponent | expected `−1/d` | abs error |
|---|---|---|---|---|
| 2 (1+1) | 0.032293, 0.022790, 0.015902, 0.011307 | **−0.506145** | −0.5 | 0.006145 |
| 4 (3+1) | 0.118894, 0.097234, 0.081542, 0.068344 | **−0.265026** | −0.25 | 0.015026 |

Both are inside the declared 0.05 tolerance, and `|−0.265| < |−0.506|`: the
physically relevant 3+1 case converges **slowest**, at about half the 1+1 rate.
`<NN>` decreases monotonically with N in both dimensions.

## What this addresses

PHYSICS §15 recorded that the empirical convergence rates were all measured in
1+1 Minkowski and that the 3+1 rate (`N^(−1/4)`) was "not yet computed". This
gate computes it on supplied geometry and confirms the dimensionality of the
covering scale, with the 3+1 slowness made explicit.

## Boundaries

A bounded finite-range exponent fit on supplied sprinklings: not a
continuum-limit proof, not manifoldlikeness, not curvature, and not gravity.
The exponents carry finite-N and finite-range error (the 3+1 error is larger,
consistent with its smaller separation) and are implementation diagnostics, not
a theorem. κ-gravity remains retired; gravity is standard GR under Option B. No
apparatus is involved and no physical claim is made.

## Verification and provenance

`primary.py` and `reference.py` compute the nearest-neighbour statistic
(per-point scan vs full pairwise list) and the least-squares fit independently;
the driver compares complete encoded reports and refuses on any difference.
Fixed seeds make the run deterministic; 6 tests pass.

- Capture: 806 bytes;
  SHA-256 `959faf2601cc2c650c834af924c496eb925431cd2b0a5e75d2fee69014bd03ab`.
- Freeze: SHA-256
  `af2d764c797a901f6eee39e0ef6436da953f33abc149b4b47b3521289a3e6b96`.

CG continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
