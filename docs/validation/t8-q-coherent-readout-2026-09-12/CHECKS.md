# Coherent readout: executed arithmetic checks

12 September 2026. **15/15 tests pass in normal and optimized Python 3.11.6.**
This checks the [conditional construction](CANDIDATE.md), not a physical
apparatus, a uniquely DET-derived law or a new QR-05 gate.

The exact result is a fixed-diagonal separation. Both admitted two-port
kernels have 16 atomic diagonal entries equal to 1/16, at the same empty
committed C and the same setting. The joint branch ({a},0) has weight
**1/4 versus 1/12**, or **3/4 versus 1/4 conditional on action {a}**.
Its full unnormalized residual remains part of the branch, not just this
scalar prediction. Every action marginal is still 1/3.

## What was checked

- All 16 history-coordinate basis inputs agree with the independent
  downstream representation and reconstruct without information loss.
- All 12 action/context/outcome maps agree on every one of the 16
  functional-coordinate basis inputs: **192 complete linear-map comparisons**.
  Linearity extends this equality to complex inputs; coordinate probes are
  not asserted to be positive preparations.
- **256 complete incomparable-composition comparisons** cover every
  coordinate probe, context pair and outcome pair. A correlated Bell input
  supplies an additional positive-state example, including an impossible
  outcome. No product-state restriction enters the analytical proof.
- Exact rational complex coherence detects the density/functional transpose
  mistake; real fixtures alone would not. Mixtures preserve unnormalized
  branches and use probability-weighted conditional states.
- Derived idempotence, compatibility closure, total-mass normalization,
  actual and formal zero branches, same-port noncommutation, and refusal of
  a positive but algebra-incompatible kernel all pass.
- A nonzero source history block with zero total mass is retained as a
  counterexample to naive conditioning. The law's **rebuilt compression
  residual**, not that raw block, is identically zero.

The symbolic implementation and conventional comparison share no mathematical
helper imports and were written by separate agents. A further read-only
review found no blocking discrepancy in the equations, implementations or
scope statements. The finite tests do not prove positivity for all states;
that follows conditionally from the displayed positive-functional argument.
The compatibility helper explicitly does **not** claim to validate positivity.

## Reproduction and source record

From the repository root, the final formatted sources passed:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/validation/t8-q-coherent-readout-2026-09-12/check.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -O docs/validation/t8-q-coherent-readout-2026-09-12/check.py
.venv/bin/python -m ruff check docs/validation/t8-q-coherent-readout-2026-09-12
```

Both mathematical runs finished in about 1.1 seconds, with no errors or
failures. The checker uses only standard-library exact arithmetic; Ruff
is a separate development lint check. These are unit/arithmetic checks,
**not a second create-only certificate or growth census**.

SHA-256 of the checked sources:

| File | SHA-256 |
| --- | --- |
| CANDIDATE.md | `3ab9f1d8c3685aa295364204859d4c0a0f8b0065905a4cc8c30bcddd2f71272c` |
| algebra.py | `ad2486e0c5eba1ecb561c01fa345989dbeeb052b7e871a9ad13ac9763b19f180` |
| reference.py | `cc071a052bcf562cc7935a6084b7f24ad03fb32f03d604f7c786dfde0621e5eb` |
| check.py | `8dd0fde8bf136ef68bee00c9fcd8202dec61dbcb192f9322c01e750e0424163e` |

**Decision:** the conditional readout definition, consistency theorem and
diagonal-summary counterexample stand. Adopting the noncommutative algebra
and compression rule remains a substantial added quantum-kinematic
assumption. Their DET-native origin/selection, quantum-sensitive order
selection and the kinematic geometry map remain unestablished. No successor
gate is opened or scheduled; Option B and Status M are unchanged.
