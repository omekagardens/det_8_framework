# QR-05CW: LGH infimum via bottleneck assignment (small spaces)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: inconclusive for convergence; two exact sub-findings.** This computes
the exact LGH-style Gromov–Hausdorff distortion — the minimum over
correspondences (bijections) of the maximum pairwise `|d_X − d_Y|` difference —
on small Lorentzian metric spaces. It is documented as inconclusive, not
promoted. Supplied geometry; no gravity claim.

Continue [QR-05CV](../qr-05cv-lgh-embedding-investigation-2026-09-10/README.md)
(the investigation this pursues).

## 1. What is computed

For a sprinkle `X` with the discrete chain time-separation and its continuum
counterpart `Y` with the Lorentzian distance, both normalized to comparable
units (mean over comparable pairs), the exact infimum over all bijections:

```text
inf_GH(X,Y) = min over bijections sigma of max over pairs |d_X(i,j) - d_Y(sigma i, sigma j)|,
```

computed by exhaustive search for N ≤ 8 (`8! = 40320` bijections).

## 2. Two exact sub-findings and an inconclusive verdict

1. **The identity correspondence is optimal** at fixed scale: for every N ≤ 8,
   `improvement = 0` — no relabeling reduces the distortion. The geometry pins
   the correspondence; the natural map is the LGH-minimizing one among
   bijections.
2. **The free-scale infimum is degenerate**: with the scale `s` free, `s = 0`
   makes any comparison trivial (`inf = 0` even against an incomparable space),
   because the LGH class is **conformal**. So an LGH distance must be
   **scale-fixed**; this gate fixes it.
3. **Inconclusive for convergence**: the distortion is large (≈1.7–2.8) and does
   not decrease over N = 5…8, and the **incomparable control is not separated**
   (2.16 vs a manifoldlike range of ≈1.7–2.8). Small spaces are too coarse to
   demonstrate LGH convergence, and the exact infimum over correspondences is
   NP-hard for larger N (backtracking), beyond this bounded scope.

`lgh_infimum_established = false`; verdict recorded as inconclusive.

## 3. Boundaries

A bounded exact computation with an inconclusive outcome, on supplied geometry.
It shows the identity-optimality and the scale-degeneracy exactly, but does not
establish the LGH infimum or convergence. No metric, manifold, curvature,
dynamics or gravity is claimed. Curvature and the imported BD operator stay
parked; κ-gravity is retired and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` and `reference.py` build the causality, the chain matrix, the
normalization and the exhaustive infimum independently; the driver compares with
a float tolerance and refuses on any difference. `study.py` writes create-only
`results.json` and `source-freeze.json` (freezing the gate sources and the T7
module by hash); `test_qr05cw.py` checks identity-optimality, the row structure,
the scale-degeneracy record, the inconclusive verdict and route agreement. Fixed
seeds make the run deterministic. Limits: sources ≤262,144 bytes, artifacts
≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
