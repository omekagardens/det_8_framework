# QR-05CU results

10 September 2026 (Pacific/Honolulu). **Minguzzi–Suhr LGH distance attempt
complete — bounded positive.** A bounded **upper estimate** of the Lorentzian
Gromov–Hausdorff distance between a supplied Minkowski sprinkling and the
continuum decreases with refinement (≈ the discreteness scale), and a random
correspondence is far larger. 7 tests pass. Supplied geometry; no gravity claim.

## The estimate

Natural correspondence (identity on the sprinkle; nearest sprinkle for continuum
probes), one optimized scale `s`, distortion = mean absolute deviation, pairs
with `τ ≥ 0.1·max τ`:

| N | ℓ | scale | forward | covering | **d_ub** |
|---|---|---|---|---|---|
| 200 | 0.05 | 0.957637 | 0.041439 | 0.039402 | **0.041439** |
| 400 | 0.035355 | 0.838879 | 0.032893 | 0.036857 | **0.036857** |
| 800 | 0.025 | 0.805687 | 0.029277 | 0.029349 | **0.029349** |
| 1600 | 0.017678 | 0.778264 | 0.022838 | 0.024419 | **0.024419** |

The distortion decreases monotonically and tracks the discreteness scale `ℓ`
(≈ `N^{−1/2}` in 1+1). The fitted scale `s` (0.96 → 0.78) is a **convention** —
absolute scale is not identified (BL/BM/BN).

## Control

A random correspondence of the chain distances gives distortion **0.221130**,
versus ≈0.02–0.04 for the natural correspondence — so the natural correspondence
is genuinely close, and the result is not an artifact of the point set.

## What this establishes and what remains

Establishes a **bounded upper estimate** of the LGH distance, converging with
refinement, for the natural correspondence. It does **not** establish the
Minguzzi–Suhr LGH distance: the causal-embedding construction, the infimum over
correspondences, and the manifoldlikeness of the limit remain open
(research-grade, shared with causal-set theory). No curvature, dynamics or
gravity is claimed.

## Verification and provenance

`primary.py` and `reference.py` build the causality, the chain DP, the estimate
and the control independently; the driver compares with a float tolerance and
refuses on any difference.

- Capture: 1,047 bytes;
  SHA-256 `c934968f7adc5c0a3ed0c10df0d89745417a1ef4dbdf9d9def53c5d2351629e5`.
- Freeze: SHA-256
  `446755ee526e061849f3419cfcf8dc51b9028cf51a22765cb9c0e6537c8552b4`.

CU continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
