# Finite kernel transport repair (RET032-v2)

The T5 finite Markov example now uses one outgoing-row convention throughout: Q[i][j] transports probability from i to j, and a column probability vector evolves by Q transpose. The previous asymmetric example mixed row and column conventions and could lose probability mass. The repair checks the complete probability law before reporting normalized moments and does not silently renormalize an invalid result.

The signed first jump moment uses outgoing rates, so positive rightward bias has positive drift. The fixed driver expectation is +0.6. Endpoint rows retain their finite-chain meaning; homogeneous unbounded reference formulas are labelled separately from synthetic finite-law summaries. The relaxation fit is a separately symmetric experiment.

Symmetric-only helpers require exact equality of the represented finite off-diagonal rates. A positive one-way rate of 2**-44 must not pass because it is below an absolute tolerance. Generator balance uses a dimensionless per-row relative test, with an explicit all-zero case. It rejects tiny outgoing-only or diagonal-only rows. This is validation after floating conversion, not exact real arithmetic, a universal solver-accuracy theorem or an arbitrary-scale convergence guarantee.

## Verification

An independent source review accepted the repaired implementation, two new scale regressions, the existing complete-law controls, and the exact T5 function replacement. A different coordinator then ran the frozen candidate in two isolated standard-library checks on 2026-11-01:

- Eleven unittest methods passed, including 135 fixed finite laws from independent ticket counting, stationary laws, signed local moments, invalid/degenerate cases and tiny-rate controls.
- All sixteen checks in the exact replacement T5 function passed with strict local callbacks.

The machine-readable record is [ret032-finite-transport-checks.json](ret032-finite-transport-checks.json). The installed regression test has the same class and eleven test bodies as the executed frozen test; its reviewed loader resolves the local models directory. That repository-layout file and the complete top-level test driver were not executed in these checks. Each checkout received only the reviewed T5 function span; its unrelated prefix and suffix were preserved byte for byte.

The regression suite can be run from this checkout with:

```sh
python3 -I -S -B det8/tests/test_kernel_transport.py
```

The two recorded runs were ordinary software checks, not performance benchmarks or whole-job resource qualification. No empirical observation, physical diffusion scale, heat equation, native gravity prediction, calibration, hardware readiness or measurement-executor qualification follows. Numerical results remain conditional on the declared finite models and represented-input policy.
