# QR-05CT results

10 September 2026 (Pacific/Honolulu). **Lorentzian-distance continuum step
complete — positive.** The discrete time-separation of supplied Minkowski
sprinklings converges to the continuum Lorentzian distance, up to one scale
constant, with narrowing fluctuations; a random order is distinct. 7 tests pass.
Supplied geometry; no gravity claim.

## The measurement

`tau_hat(p,q) = (longest chain from p to q) · ℓ` versus the continuum
`tau(p,q) = √((Δt)² − (Δx)²)`, `ℓ = √(area/N)`:

| N | ℓ | mean `tau_hat/tau` | spread |
|---|---|---|---|
| 200 | 0.05 | 1.142190 | 0.250271 |
| 400 | 0.035355 | 1.202110 | 0.191620 |
| 800 | 0.025 | 1.181639 | 0.130524 |
| 1600 | 0.017678 | 1.198144 | 0.117215 |

The mean is **stable** (constant 1.181021, all within 0.06) and the **spread
decreases** with N — the discrete time-separation converges to the continuum
Lorentzian distance up to a single constant. That constant (≈1.18) is a **scale
convention** (absolute scale not identified, BL/BM/BN); the convergent content
is the *shape* of the distance function.

## Control

A random total order on the same points gives mean ratio **120.0** and spread
**343.7** — no convergence. So the convergence is specific to the causal order,
not an artifact of the point set.

## What this establishes and what remains

Establishes a **necessary-condition step** for Lorentzian Gromov–Hausdorff
convergence: the Lorentzian distance function converges (up to scale) with
narrowing fluctuations, and a non-causal order fails. It does **not** establish
LGH convergence: the full Minguzzi–Suhr distance, the causal-embedding
arguments, and the manifoldlikeness of the limit remain open (research-grade,
shared with causal-set theory). No curvature, dynamics or gravity is claimed.

## Verification and provenance

`primary.py` and `reference.py` build the causality, the longest-chain DP, the
ratios and the control independently; the driver compares with a float tolerance
and refuses on any difference.

- Capture: 929 bytes;
  SHA-256 `694b8da2e0420970b95989ba7566567cea716228c63459b26e8a464dac6c0699`.
- Freeze: SHA-256
  `9ec8a7c816c37ef6f8ec78913efe3bc3b0ad59ea63c919fa74b35fd7766935f5`.

CT continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
