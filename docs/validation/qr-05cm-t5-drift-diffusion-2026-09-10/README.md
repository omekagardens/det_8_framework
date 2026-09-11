# QR-05CM: T5 drift-diffusion / variable-coefficient benchmark

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
Extends the T5 local-kernel route to **spatially varying** kernel moments, so
the continuum operator is a **drift-diffusion** generator with
position-dependent coefficients read from the local kernel moments
(`docs/record_kernel_physics.md` T5). Supplied geometry; no gravity claim.

Continue [QR-05CL](../qr-05cl-t5-wave-kernel-2026-09-10/README.md) (the
constant-coefficient wave case of the same method).

## 1. What is measured

At each site `x` a local kernel `K^x` (here `{+1: D(x)+V(x), −1: D(x)−V(x),
0: −2D(x)}`, conservative) acts as `S f(x) = Σ_j K^x_j (f(x+jh) − f(x))`. Its
**local moments** are

```text
mu1(x) = Σ_j K^x_j (jh) = 2h V(x)      (drift)
mu2(x) = Σ_j K^x_j (jh)^2 = 2h^2 D(x)  (diffusion)
```

and the moment expansion gives `S f(x) → mu1(x) f'(x) + (1/2) mu2(x) f''(x)`.
With `D(x) = 1 + a sin(2πx)` and `V(x) = b cos(2πx)`, both coefficients vary
with position. Checks: **(A)** exact on quadratics; **(B)** second-order
convergence of `S f` to the variable-coefficient operator on a sinusoid;
**(C)** the coefficients equal the local moments and vary with `x`;
**(D)** the constant-kernel control (no `x`-dependence → no variation).

## 2. Result

All checks pass; numbers in [RESULTS.md](RESULTS.md). The continuum
drift-diffusion coefficients are supplied by the local kernel moments — the T5
"drift-diffusion" branch, made concrete and exact on quadratics.

## 3. Boundaries

A bounded estimator check on supplied geometry — not a continuum-limit theorem,
not curvature, and not gravity. It does not prove that order+count forces
geometry (T7 stays open). Absolute scale is a convention; only relative
coefficients are fixed. Curvature and the imported BD operator stay parked;
κ-gravity is retired and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` implement the kernels, the local-moment
prescription and the operator independently; the driver compares with a float
tolerance and refuses on any difference. `study.py` writes create-only
`results.json` and `source-freeze.json`; `test_qr05cm.py` checks the exact
quadratics, the variable-coefficient convergence, the local-moment identity, the
constant-kernel control and route agreement. Fixed inputs make the run
deterministic. Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes.
Decision record: [RESULTS.md](RESULTS.md).
