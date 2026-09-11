# QR-05CM results

10 September 2026 (Pacific/Honolulu). **T5 drift-diffusion / variable-coefficient
benchmark complete — positive.** A local kernel whose moments vary with position
generates a drift-diffusion operator with position-dependent coefficients equal
to the local kernel moments. 7 tests pass. Supplied geometry; no gravity claim.

## A — exact on quadratics

At `x₀=0.37`, `h=0.05`, with `D=1+0.5 sin(2πx)`, `V=0.3 cos(2πx)`:

| Quantity | Value |
|---|---|
| `S x` | −0.020536413 |
| `μ₁ = 2hV` | −0.020536413 |
| `S x²` | −0.008374524 |
| `μ₁·2x + ½μ₂·2` | −0.008374524 |

`S x = μ₁` and `S x² = μ₁ f' + ½μ₂ f''` exactly, so the moment prescription is
exact on quadratics for the variable-coefficient kernel.

## B — variable-coefficient convergence

On `f = sin(2πx)` with `D(x), V(x)` varying, `S f` converges to
`μ₁(x) f' + ½ μ₂(x) f''`:

| M | h | relative error |
|---|---|---|
| 16 | 0.0625 | 0.024150 |
| 32 | 0.03125 | 0.006290 |
| 64 | 0.015625 | 0.001597 |
| 128 | 0.0078125 | 0.000401 |

Log-log exponent **1.9716 ≈ 2**: second-order convergence for the
position-dependent drift-diffusion operator.

## C — the coefficients are the local moments

| x | μ₁ (drift moment) | μ₂ (diffusion moment) | D(x) | V(x) |
|---|---|---|---|---|
| 0.0 | 0.03 | 0.005 | 1.0 | 0.30 |
| 0.125 | 0.021213 | 0.006768 | 1.354 | 0.212 |
| 0.25 | 0.0 | 0.0075 | 1.5 | 0.0 |
| 0.375 | −0.021213 | 0.006768 | 1.354 | −0.212 |
| 0.5 | −0.03 | 0.005 | 1.0 | −0.30 |

Both coefficients track the supplied position-dependent `D(x), V(x)` and vary
across the domain — the spatially varying moments of the kernel supply the
drift-diffusion coefficients (T5).

## D — the constant-kernel control

A constant kernel has zero coefficient variation; the variable kernel has
variation `0.005` in `μ₂`. So the position-dependence is carried by the varying
moments, not an artifact (`coefficients_vary = true`).

## What this settles

The T5 triangle is now covered on supplied geometry: diffusion (CH), the
reversible wave operator (CL), and variable-coefficient drift-diffusion (CM),
all with coefficients from the discrete-kernel moments.

## Boundaries

A bounded estimator check on supplied geometry — not a continuum-limit theorem,
not curvature, and not gravity. It does not prove that order+count forces
geometry (T7 stays open; gravity stays out of scope until T7 succeeds). Absolute
scale is a convention. Curvature and the imported BD operator stay parked;
κ-gravity is retired and gravity is standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` implement the kernels, the local-moment
prescription and the operator independently; the driver compares with a float
tolerance and refuses on any difference.

- Capture: 1,606 bytes;
  SHA-256 `e234d16330d9fefdebfd3d8784d424f640fd514732f63a40fac83f5edd56b87a`.
- Freeze: SHA-256
  `50b22558a4219147313f680a1f0bd32977d8260bb36082e9bd49065ce50c9cc6`.

CM continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
