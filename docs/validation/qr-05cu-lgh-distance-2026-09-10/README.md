# QR-05CU: Minguzzi–Suhr LGH distance attempt (bounded)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
A bounded attempt at the Lorentzian Gromov–Hausdorff distance between a supplied
Minkowski sprinkling and the continuum manifold, via the natural correspondence
and an optimized scale. It is an **upper estimate**, not the Minguzzi–Suhr
infimum; the embedding theory and the manifoldlikeness of the limit remain open.
Supplied geometry; no gravity claim.

Continue [QR-05CT](../qr-05ct-lorentzian-distance-2026-09-10/README.md) (its
distance convergence is the input here).

## 1. The estimate

Two Lorentzian spaces: `X` = the sprinkled points with the discrete
chain-time-separation `d̂ = (longest chain)·ℓ`, and `M` = the continuum with the
Lorentzian distance `τ`. The natural correspondence is the identity on `X`
(plus, for continuum probes `y`, the nearest sprinkle point `g(y)`). After
fitting one scale `s`, the **bounded distortion** is

```text
d_ub = max( mean |s·d̂ − τ| over sprinkle pairs ,  mean |τ − s·d̂| over probe pairs ),
```

restricted to pairs with `τ ≥ 0.1·max τ` (near-null pairs are where the discrete
approximation is worst and would dominate a max). This is an upper bound on the
LGH distance for the specified correspondence, not its infimum.

## 2. Result

Across N = 200, 400, 800, 1600 the distortion decreases ≈ linearly in the
discreteness scale `ℓ` (i.e. `≈ N^{−1/2}` in 1+1), and a random correspondence
control is far larger — so the natural correspondence is genuinely close.
Numbers in [RESULTS.md](RESULTS.md).

## 3. Boundaries

A bounded upper estimate on supplied geometry. It is **not** the Minguzzi–Suhr
LGH distance: the causal-embedding construction, the infimum over
correspondences, and the manifoldlikeness of the limit remain open
(research-grade, shared with causal-set theory). The scale `s` is a convention —
absolute scale is not identified (BL/BM/BN). No curvature, dynamics or gravity is
claimed. Curvature and the imported BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` build the causality, the chain DP, the estimate
and the control independently; the driver compares with a float tolerance and
refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05cu.py` checks the row structure, the decreasing distortion, the
control separation and route agreement. Fixed seeds make the run deterministic.
Limits: sources ≤262,144 bytes, artifacts ≤16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
