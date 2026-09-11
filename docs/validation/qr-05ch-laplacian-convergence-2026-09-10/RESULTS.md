# QR-05CH results

10 September 2026 (Pacific/Honolulu). **Graph-Laplacian action benchmark
complete.** On a supplied flat torus the graph-Laplacian action is proportional
to the eigenfunction, the response-adjusted constant is mode-independent and
matches the continuum prediction, a non-eigenfunction control fails, and the
residual falls with N. 7 tests pass. Laplacian only; curvature deferred; not
gravity.

## Proportionality and mode independence

`Lf ≈ 4πε(e^{−εμ}−1) f` for `f = sin(kπx₁)`, `μ=k²`. Response-adjusted
constant `slope/(e^{−εμ}−1)`:

| Mode | μ | slope | residual | constant |
|---|---|---|---|---|
| k=2 (`sin 2πx₁`) | 39.478417604 | −0.040534851 | 0.089357436 | 0.124273493 |
| k=4 (`sin 4πx₁`) | 157.913670417 | −0.099913235 | 0.064234040 | 0.125859560 |

Mode gap = 0.01276 (within 0.05): the two modes give the **same** constant.
Both residuals are below 0.1, so the action is proportional to the
eigenfunction in each case.

## Continuum prediction

The predicted constant is `4πε = 0.125663706`; the measured value is
0.124273493, a ratio of **0.98894** — the graph Laplacian reproduces the
continuum Laplace–Beltrami response to ~1.1%.

## Negative control and convergence

The non-eigenfunction `f=(x₁−½)²` (`Δf=2`, not proportional to `f`) gives a
residual of 0.783 versus 0.089 for the local eigenfunction case — an 8.8×
separation, so locality/proportionality is doing real work. The residual on
`sin(2πx₁)` falls with N: 0.1395 (N=500), 0.1130 (1000), 0.0746 (2000).

## Boundaries

A bounded estimator check on supplied, *Riemannian* geometry — not a Lorentzian
continuum limit, not curvature convergence, and not gravity. It does not prove
that order+count forces geometry; the manifoldlikeness problem stays open.
**Curvature is deferred**: the `continuum_limit_curvature` and Bianchi modules
are quarantined (retired gravity), and a curved-geometry normalization was not
reconciled, so no curvature claim is made. κ-gravity remains retired; gravity
is standard GR under Option B. No apparatus is involved.

## Verification and provenance

`primary.py` and `reference.py` share the supplied sprinkling (fixture) but
implement the action and the fit independently; the driver compares with a
float tolerance and refuses on any difference. Fixed seeds make the run
deterministic.

- Capture: 1,021 bytes;
  SHA-256 `75000decfde7d4ca5c7c1f468359db77d1ca166fefdebbd59c6c55328b330c4f`.
- Freeze: SHA-256
  `423569b1b95c721c62461ec72907dfd4458df59e0b1b20a1eca1aeee4a0cde66`.

CH continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
