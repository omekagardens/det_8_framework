# QR-05CL results

10 September 2026 (Pacific/Honolulu). **T5 local-kernel continuum (wave-like)
benchmark complete — positive.** A local conservative kernel generates the
d'Alembertian `∂_t² − ∂_x²`, exactly on quadratics and at second order on a
sinusoid, with the continuum coefficients read from the kernel's **second
moments**; an asymmetric kernel produces drift instead. 7 tests pass. Supplied
geometry; no gravity claim.

## A — exact on quadratics

With `h=0.1`, kernel second moment `μ₂ = 2h² = 0.02`:

| Quantity | Value |
|---|---|
| `S x²` | 0.02 |
| `T t²` | 0.02 |
| predicted `μ₂` | 0.02 |

`S x² = μ₂` and `T t² = μ₂` exactly, so the normalized wave operator
`box_h = (2/μ₂^t)T − (2/μ₂^s)S` equals `∂_t² − ∂_x²` exactly on `x²`, `t²` and
`xt` (the stencils are exact for quadratics).

## B — second-order convergence to `∂_t² − ∂_x²`

On `u = sin(2πx) + sin(2πt)` over a periodic lattice:

| M | h | mean abs error |
|---|---|---|
| 16 | 0.0625 | 0.406537 |
| 32 | 0.03125 | 0.102512 |
| 64 | 0.015625 | 0.025683 |
| 128 | 0.0078125 | 0.006424 |

The log-log exponent is **1.9948 ≈ 2**: the discrete wave operator from the
kernel converges to the continuum d'Alembertian at second order in `h`.

## C — the coefficient is the kernel moment

For three different kernels, `S x²` equals the kernel's second moment exactly:

| Kernel | `S x²` | moment `μ₂` | ratio |
|---|---|---|---|
| `nn` (1,−2,1) | 0.02 | 0.02 | 1.0 |
| `double` (2,−4,2) | 0.04 | 0.04 | 1.0 |
| `wide` (−1/12,4/3,−5/2,4/3,−1/12) | 0.02 | 0.02 | 1.0 |

So the continuum coefficient tracks the kernel moment — the T5 prescription.

## D — the drift control

The symmetric kernel has first moment `0`, so the operator is a pure second-order
(wave/Laplacian) generator. The asymmetric kernel `(1.1,−2,0.9)` has first moment
`−0.02`, so it generates a first-derivative (drift) term — drift-diffusion, not a
pure wave operator. Reversibility requires the symmetric (conservative) kernel.

## What this settles

The DET-native route to a wave-like operator is a local conservative kernel with
coefficients from its moments (T5), verified here. This replaces the imported
Benincasa–Dowker construction of QR-05CI (see its
[commitment-routing amendment](../qr-05ci-lorentzian-operator-2026-09-10/COMMITMENT_ROUTING.md)).

## Boundaries

A bounded estimator check on supplied geometry — not a Lorentzian continuum-limit
theorem, not curvature, and not gravity. It does not prove that order+count
forces geometry (T7 stays open; gravity stays out of scope until T7 succeeds).
Absolute scale is a convention (the moment ratio fixes only relative
coefficients). Curvature stays quarantined; κ-gravity is retired and gravity is
standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` implement the kernels, the moment prescription
and the operator independently; the driver compares with a float tolerance and
refuses on any difference.

- Capture: 1,226 bytes;
  SHA-256 `1f450331703d227e08295bfe0e8bb3d706e3bc9be0be0ff82b567d2c8650b75e`.
- Freeze: SHA-256
  `ddf0d50e9868c0aad25016ec4b65f0711340b384b5579cc561a419f8a5b8f4c0`.

CL continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
