# QR-05CT: Lorentzian-distance continuum step (LGH route)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
A **necessary-condition step** toward Lorentzian Gromov–Hausdorff (LGH)
convergence: the discrete time-separation of supplied Minkowski sprinklings
converges to the continuum Lorentzian distance, up to one scale constant, with
narrowing fluctuations. Full LGH convergence (Minguzzi–Suhr) is **not**
attempted. Supplied geometry; no gravity claim.

Continue [QR-05CS](../qr-05cs-geometry-consolidation-2026-09-10/README.md).

## 1. What is measured

For a 1+1 Minkowski sprinkle with discreteness scale `ℓ = √(area/N)`, take a
source `p` and each later point `q`, and compare the discrete time-separation

```text
tau_hat(p,q) = (longest-chain length from p to q) * ell
```

with the continuum Lorentzian distance `tau(p,q) = √((Δt)² − (Δx)²)`. LGH
convergence requires the *distance function* to converge; this checks that the
discrete estimate does, up to a global constant (a scale convention).

## 2. Result

Across N = 200, 400, 800, 1600 the mean ratio `tau_hat/tau` is **stable**
(≈1.2), and its **spread decreases** with N — the discrete time-separation
converges to the continuum Lorentzian distance up to one constant. A random
total order on the same points is distinct (no convergence). Numbers in
[RESULTS.md](RESULTS.md).

## 3. Boundaries

A bounded necessary-condition step on supplied geometry. It is **not** LGH
convergence: the full Minguzzi–Suhr distance, the embedding arguments, and the
manifoldlikeness of the limit remain open (research-grade, shared with causal-set
theory). The constant ≈1.2 is a scale convention — absolute scale is not
identified (BL/BM/BN) — so only the *shape* of the distance function converges.
No curvature, dynamics or gravity is claimed. Curvature and the imported BD
operator stay parked; κ-gravity is retired and gravity is standard GR under
Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` build the causality, the longest-chain DP, the
ratios and the control independently; the driver compares with a float tolerance
and refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05ct.py` checks the stable mean, the decreasing spread, the control
distinctness and route agreement. Fixed seeds make the run deterministic.
Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
