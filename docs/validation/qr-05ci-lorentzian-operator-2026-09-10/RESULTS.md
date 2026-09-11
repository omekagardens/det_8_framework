# QR-05CI results

10 September 2026 (Pacific/Honolulu). **2D Lorentzian operator benchmark
complete. Outcome: implementation verified; continuum limit not demonstrated
at accessible N.** This resumes the parked gate with the correct 2D operator,
verifies its two forms exactly, attempts the continuum limit, and re-parks it
with the evidence. Supplied geometry; no gravity claim.

## The operator

Sorkin, gr-qc/0703099, Eq. (1):

```text
B phi(x) = (4/l^2)[ -1/2 phi(x) + (sum_{L1} - 2 sum_{L2} + sum_{L3}) phi(y) ]
```

`L_k` = ancestors `y` of `x` with `k-1` intervening elements (`L1` = links),
`l^2 = 1/rho`; matrix form (Eq. 2): `-1/2` diagonal, `1, -2, 1` for
`n(x,y)=0,1,2`, else `0`.

## Implementation verified exactly

On a deterministic 1+1 causal mesh, the Eq. (1) layer sums and the Eq. (2)
matrix action agree exactly in rational arithmetic (`exact_form_agreement =
true`). So the implementation is correct.

## Continuum limit not demonstrated

The constant term vanishes only if `E|L₁|−2E|L₂|+E|L₃| = ½`. Measured on
supplied sprinklings (interior points, 8 seeds):

| N | mean layer combo | mean `B·1` | residual from ½ |
|---|---|---|---|
| 300 | 0.353821 | −350.83 | 0.146179 |
| 600 | 0.490262 | −46.74 | 0.009738 |

The combination is **not consistent** across densities (0.354 → 0.490, with
separate probes at N=1200 giving 0.583), so the constant term does not vanish
and the continuum limit is not demonstrated. `constant_annihilated = false`,
`validated = false`. This matches Sorkin's own caveat that 2D fluctuations grow
with N and that 2D links are long (strong nonlocality); a clean validation would
need a careful large-diamond, boundary-controlled treatment beyond this
environment's budget.

## What this settles

- The right 2D operator is now recorded (it was previously unknown here), and
  the implementation is exact.
- The operator is **re-parked**: correct in specification, not numerically
  validated, so a Lorentzian dynamics benchmark stays blocked on it.

## Boundaries

A bounded implementation check plus a failed continuum-limit attempt on
supplied geometry. Not a dynamics result, not curvature, not gravity. Curvature
stays quarantined; κ-gravity remains retired; gravity is standard GR under
Option B.

## Verification and provenance

`primary.py` and `reference.py` implement the operator independently and agree
(float-tolerant); the driver refuses on any difference. Fixed seeds make the run
deterministic.

- Capture: 899 bytes;
  SHA-256 `75472caf2e78c555ec9978bd2178b48d0a9e4da17be54dd649f35958c08cc29f`.
- Freeze: SHA-256
  `e40c8b38128357ae7e65e4e72f832ddeebdb1d708af141f8eca4f23720a843f9`.

CI continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
