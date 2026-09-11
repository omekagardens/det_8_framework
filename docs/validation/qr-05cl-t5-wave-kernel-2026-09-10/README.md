# QR-05CL: T5 local-kernel continuum — wave-like kernel benchmark

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
This is the DET-native T5 route to a wave-like (Lorentzian) operator: a local
conservative kernel whose continuum limit is the d'Alembertian, with the
continuum coefficients read from the kernel's **second moments**
(`docs/record_kernel_physics.md` T5). It replaces the imported Benincasa–Dowker
construction of QR-05CI. Supplied geometry; no gravity claim.

Continue [QR-05CI](../qr-05ci-lorentzian-operator-2026-09-10/COMMITMENT_ROUTING.md)
(the routing that motivated this) and [QR-05CH](../qr-05ch-laplacian-convergence-2026-09-10/README.md)
(the diffusion case of the same method).

## 1. What is measured

On a periodic lattice with spacing `h`, a local conservative kernel `K` acts as
`S f(x) = Σ_j K_j (f(x+jh) − f(x))`. The moment expansion gives

```text
S f = (Σ_j K_j (jh)) f'  +  (1/2)(Σ_j K_j (jh)²) f''  +  ...
```

so the continuum coefficient is the kernel's **second moment** `μ₂ = Σ K_j (jh)²`.
Composing a spatial and a temporal kernel with opposite signs gives the
normalized wave operator

```text
box_h = (2/μ₂^t) T − (2/μ₂^s) S   →   ∂_t² − ∂_x²  =  box.
```

Checks: **(A)** exact on quadratics (`S x² = μ₂^s`, `T t² = μ₂^t`; `box_h = box`
for `x²`, `t²`, `xt`); **(B)** the wave operator converges to `∂_t² − ∂_x²` at
second order in `h` on a sinusoid; **(C)** the coefficient equals the kernel
moment for three different kernels; **(D)** the drift control — a symmetric
kernel has zero first moment, an asymmetric one does not (drift-diffusion, not a
pure wave operator).

## 2. Result

All checks pass; numbers in [RESULTS.md](RESULTS.md). The wave-like continuum
operator emerges from the local conservative kernel with its coefficients
supplied by the kernel's moments — the T5 statement, made concrete and exact on
quadratics.

## 3. Boundaries

A bounded estimator check on supplied geometry. It is **not** a Lorentzian
continuum-limit theorem, not curvature, and **not gravity**. It does not prove
that order+count forces geometry (T7 stays open, and gravity stays out of scope
until T7 succeeds). Absolute scale is a convention (the moment ratio fixes only
relative coefficients). Curvature stays quarantined; κ-gravity remains retired
and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` implement the kernels, the moment prescription
and the operator independently; the driver compares with a float tolerance and
refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json`; `test_qr05cl.py` checks the exact quadratics, the
moment-coefficient identity, the second-order convergence, the drift control and
route agreement. Fixed inputs make the run deterministic. Limits: sources
≤262,144 bytes, artifacts ≤16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
