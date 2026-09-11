# QR-05CI: 2D Lorentzian (Benincasa–Dowker/Sorkin) operator benchmark

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: implementation verified; continuum limit not demonstrated at
accessible N. Amended: reclassified as an imported causal-set correspondence,
not the DET-native route.** The Benincasa–Dowker operator is a borrowed
causal-set field-theory tool; DET's own commitments place a *wave-like*
operator in **T5** (local conservative kernels; coefficients from kernel
moments), not in an order-layer construction. See the
[commitment-routing amendment](COMMITMENT_ROUTING.md).

Continue [QR-05CK](../qr-05ck-metric-reconstruction-2026-09-10/README.md) and
the T7 module `det8/models/order_count_geometry.py`.

## 1. The operator

The authoritative 2D operator is from Sorkin, *Does locality fail at
intermediate length-scales?* (gr-qc/0703099, Eq. 1):

```text
B phi(x) = (4/l^2)[ -1/2 phi(x) + (sum_{L1} - 2 sum_{L2} + sum_{L3}) phi(y) ]
```

with `L_k` = the ancestors `y` of `x` having `k-1` intervening elements (`L1` =
links), and `l^2 = 1/rho`. Equivalently the matrix (Eq. 2):
`l^2 B_xy/4 = -1/2` on the diagonal, `1, -2, 1` for `n(x,y) = 0,1,2`, and `0`
otherwise, where `n(x,y) = |I(x,y)|`.

## 2. What is verified

| Check | Fixture | Result |
|---|---|---|
| Eq. (1) layer sums == Eq. (2) matrix, exactly (rational arithmetic) | deterministic 1+1 causal mesh | **passes** |
| constant annihilation `E|L₁|−2E|L₂|+E|L₃| = ½` | supplied sprinklings, N=300/600, 8 seeds | **fails** at accessible N |
| operator on `phi=1` (mean `B·1`) | supplied sprinklings | large and N-dependent |

## 3. Outcome

The implementation is correct — the two forms of the operator agree exactly on
a deterministic causal set. But the continuum limit is **not** demonstrated:
the layer combination `|L₁|−2|L₂|+|L₃|` does not stabilise at `½` at accessible
N (the residuals are well above the 0.05 tolerance), so the constant term of
`B` does not vanish. This matches Sorkin's own warning that 2D fluctuations
grow with N and that links in 2D are long (strong nonlocality), and it is why
the operator is **re-parked** rather than presented as validated. See
[RESULTS.md](RESULTS.md) for the numbers.

## 4. Boundaries

A bounded implementation check plus a failed continuum-limit attempt on
supplied geometry. It is not a Lorentzian dynamics result, not curvature, and
**not gravity**. The operator is correctly specified but not numerically
validated here; a dynamics benchmark remains blocked on it. Curvature stays
quarantined; κ-gravity remains retired and gravity is standard GR under
Option B.

## 5. Evidence and limits

`primary.py` and `reference.py` implement the operator independently and must
agree (float-tolerant); `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05ci.py` checks the exact form agreement, the honest non-annihilation
result, the ensemble fields and route agreement. Fixed seeds make the run
deterministic. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes.
Decision record: [RESULTS.md](RESULTS.md).
