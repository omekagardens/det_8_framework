# QR-05CW results

10 September 2026 (Pacific/Honolulu). **LGH infimum via bottleneck assignment
complete — inconclusive, with two exact sub-findings.** On small spaces the
identity correspondence is optimal at fixed scale, the free-scale infimum is
degenerate, and convergence cannot be demonstrated. 7 tests pass. Supplied
geometry; no gravity claim.

## The computation (N ≤ 8, exhaustive over bijections)

`inf_GH` = min over bijections of the max pairwise normalized distortion:

| N | identity | infimum | improvement |
|---|---|---|---|
| 5 | 1.713339 | 1.713339 | 0.0 |
| 6 | 2.807017 | 2.807017 | 0.0 |
| 7 | 2.318063 | 2.318063 | 0.0 |
| 8 | 2.388729 | 2.388729 | 0.0 |

## Findings

1. **Identity optimal (exact).** `improvement = 0` at every N: no bijection beats
   the natural correspondence. The geometry pins the correspondence, so the
   natural map is LGH-minimizing among bijections.
2. **Scale degeneracy (exact).** With the scale `s` free, `s = 0` makes any
   comparison trivial (`inf = 0`, even against an incomparable space): the LGH
   class is **conformal**, so an LGH distance must be scale-fixed. This gate
   fixes it.
3. **Inconclusive for convergence.** The distortion is large (≈1.7–2.8) and does
   not decrease over N = 5…8, and the **incomparable control is not separated**
   (2.16 vs ≈1.7–2.8). Small spaces are too coarse to demonstrate LGH
   convergence, and the exact infimum over correspondences is NP-hard for larger
   N (backtracking), beyond this bounded scope.

`lgh_infimum_established = false`; verdict: *inconclusive at accessible N*.

## What this adds and what remains

Two exact sub-findings (identity-optimality; the conformal/scale degeneracy) and
an honest inconclusive verdict. What remains open: the LGH infimum and
convergence at scales large enough to matter, the density/commensurability
condition, ensemble convergence, and manifoldlikeness of the limit — all
research-grade. No metric, manifold, curvature, dynamics or gravity is claimed.

## Verification and provenance

`primary.py` and `reference.py` build the causality, the chain matrix, the
normalization and the exhaustive infimum independently; the driver compares with
a float tolerance and refuses on any difference.

- Capture: 1,209 bytes;
  SHA-256 `fbed2f51e26e2088c2d73611523869c42539be969fbe373f29eb1a9e2143625a`.
- Freeze: SHA-256
  `6191af92a9494ceff6a29d3f21810ba0dc16f1120feb23cd521dd8a44ce44357`.

CW continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
