# QR-05CH: graph-Laplacian action benchmark (supplied torus)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This implements the roadmap's DET-specific "bond Laplacian" step: a
graph-Laplacian estimator built from a supplied geometry is checked against the
known continuum Laplace–Beltrami action. It uses a flat torus and two
eigenfunction modes, a non-eigenfunction negative control, and an N-scaling
check. Curvature convergence is **not** attempted (the relevant module is
quarantined); this is the Laplacian part only, and it is not gravity.

Continue [QR-05CG](../qr-05cg-dimension-convergence-2026-09-10/README.md).

## 1. What is measured

On the unit flat torus, sprinkle N points and build the Gaussian graph

```text
(Lf)(x_i) = (1/N) Σ_j exp(−d(x_i,x_j)²/4ε) (f(x_j) − f(x_i)).
```

For a Fourier mode `f = sin(kπ x₁)` the continuum action is a Gaussian
smoothing of the Laplace–Beltrami operator,

```text
Lf ≈ 4πε (e^{−εk²} − 1) f = 4πε (e^{−εμ} − 1) f,
```

so the **response-adjusted constant** `slope / (e^{−εμ} − 1)` should be
**mode-independent** and equal `4πε`. Two modes (`μ=(2π)²`, `μ=(4π)²`) must give
the same constant; a non-eigenfunction (`f=(x₁−½)²`, `Δf=2`, not proportional
to `f`) must break the proportionality; and the residual must fall with N.

## 2. Result

Both modes give the same response-adjusted constant within ~1.3% and match
`4πε` to ~1.1%; the non-eigenfunction control fails; the residual decreases
with N. See [RESULTS.md](RESULTS.md) for the numbers.

## 3. Boundaries

A bounded estimator check on supplied, *Riemannian* geometry — not a
Lorentzian continuum limit, not curvature convergence, and **not gravity**. It
does not prove that order+count forces geometry; the manifoldlikeness problem
stays open. **Curvature is deferred**: the `continuum_limit_curvature` and
Bianchi modules are quarantined (retired gravity), and a curved-geometry
normalization was not reconciled, so no curvature claim is made here. κ-gravity
remains retired; gravity is standard GR under Option B. No apparatus is
involved.

## 4. Evidence and limits

`primary.py` and `reference.py` share the supplied sprinkling but implement the
action and the fit independently; the driver compares with a float tolerance
and refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json`; `test_qr05ch.py` checks proportionality, mode
independence, the negative control, the N-scaling and route agreement. Fixed
seeds make the run deterministic. Limits: sources ≤262,144 bytes, artifacts
≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
