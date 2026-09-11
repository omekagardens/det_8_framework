# QR-05CF results

10 September 2026 (Pacific/Honolulu). **T7 supplied-geometry benchmark
complete.** The order-and-count estimators recover dimension, null structure
and the conformal factor on supplied Minkowski sprinklings, and a non-diamond
order falls outside the calibrated family. Two independent routes agree; 9
tests pass. This is estimator verification on known geometry, not emergence,
and not gravity.

## Dimension recovery (order + count)

Fixed-seed sprinklings, N=400 in the unit causal diamond; ordering fraction
`r = R/C(N,2)` compared to `r(d) = Γ(d+1)Γ(d/2)/[2Γ(3d/2)]`:

| d | r (measured) | r(d) analytic | abs error | nearest-reference d |
|---|---|---|---|---|
| 2 | 0.516441 | 0.5 | 0.016441 | **2** |
| 3 | 0.219774 | 8/35 ≈ 0.228571 | 0.008797 | **3** |
| 4 | 0.106078 | 0.1 | 0.006078 | **4** |

Every dimension is recovered by nearest reference, well inside the declared
0.06 tolerance. Analytic `r(d)` decreases with d (0.5, 0.228571, 0.1), the
Myrheim–Meyer signature.

## Order → null structure (links)

d=2, N=60: mean null separation over **links** is 0.050613 versus 0.184478
over all comparable pairs (190 links of 810 comparable pairs). Links are
nearer null, the finite-density null-cone diagnostic.

## Count → conformal factor

1+1 conformal sprinkle, `Ω(x)² = 1+b·x`, b=1, N=2000, 10 bins. Recovered
normalized count profile vs the normalized truth, MSE = 0.005873 (below the
0.01 tolerance); the truth is monotone and the recovered profile trends up,
with the expected sampling scatter:

```text
recovered 0.665 0.760 0.885 1.070 0.925 1.050 0.960 1.160 1.275 1.250
truth     0.700 0.767 0.833 0.900 0.967 1.033 1.100 1.167 1.233 1.300
```

## Conformal invariance and the negative control

The causal order is invariant under `Ω² ∈ {0.5, 1, 3, 100}` (order is blind to
the conformal factor). A **chain** (every pair comparable) has r = 1.0 and an
**antichain** (no comparable pairs) has r = 0.0; the diamond family spans
`[r(4), r(2)] = [0.1, 0.5]`, so both controls lie **outside** the calibrated
family. The dimension estimator is therefore calibrated to the supplied
diamond, not to arbitrary point clouds — the operational meaning of the
routing rule.

## Boundaries and what is not claimed

Estimator verification (`CORR`), not emergence. The manifoldlikeness problem
(the question whether a bare order+count structure embeds uniquely into a
Lorentzian manifold) stays **open**, as the module's certificate states.
Nothing here derives curvature, a continuum limit, an Einstein equation or any
gravitational dynamics; κ-gravity remains retired and gravity is standard GR
under Option B. The measured monte-carlo errors are implementation
diagnostics, not a continuum-limit theorem. No apparatus or calibration is
involved.

## Verification and provenance

`primary.py` calls the module's estimators; `reference.py` re-implements
causality, ordering fraction, links/nullness, the analytic fraction and the
conformal recovery independently, taking only the sprinklings from the module.
The driver compares complete encoded reports (floats rounded to 12 decimals)
and refuses on any difference. Fixed seeds make the run deterministic.

- Capture: 1,810 bytes;
  SHA-256 `9ffa11cb69b371ab404c5c49e7df4fafcef541674031d9b41d0900a42e4967c9`.
- Freeze: SHA-256
  `ad5b912af5f062e0b1c6921ef106cf3261bcfde97764e2e9c7a373490b50671b`.

CF continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
