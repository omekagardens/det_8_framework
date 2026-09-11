# QR-05CX: LGH infimum at scale (branch-and-bound + certified lower bound)

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: inconclusive for convergence; the exact infimum is certified further, and
a certified lower bound does not vanish at scale.** This extends the exhaustion of
[QR-05CW](../qr-05cw-lgh-infimum-2026-09-10/README.md) from brute force (N ≤ 8) to
a depth-first **branch-and-bound** (tested to N = 10; boundary runs to N = 12), and
adds a cheap **certified lower bound** (the sorted-multiset matching bound), valid
at any N, swept to N = 256. It is documented as inconclusive, not promoted.

Continue [QR-05CW](../qr-05cw-lgh-infimum-2026-09-10/README.md) (the small-space
bottleneck assignment this scales).

## 1. What is computed

For a sprinkle `X` with the discrete chain time-separation and its continuum
counterpart `Y` with the Lorentzian distance, both fixed to a common scale (the
mean over comparable pairs; the free-scale class is degenerate — see §2), the exact
infimum over bijections:

```text
inf_GH(X,Y) = min over bijections sigma of max over pairs |d_X(i,j) - d_Y(sigma i, sigma j)|.
```

1. **Exact infimum by branch-and-bound.** A depth-first search over bijections with
   a running-maximum cost, an identity seed and a greedy incumbent: a branch is
   pruned once its running maximum meets the incumbent. It reproduces exhaustive
   search exactly on the small grid (N ≤ 8, `8! = 40320` permutations).
2. **Certified lower bound.** Any bijection matches the multiset of ordered-pair
   distances of `X` to that of `Y`; hence the sorted (order-statistic) matching of
   the two distance multisets bounds the infimum from below at **any** N. It is
   `O(n^2 log n)` and needs no search.

## 2. Findings

| N | exact infimum (branch-and-bound) | identity optimal? | brute-force check |
|---|---|---|---|
| 5 | 1.713339476 | yes | agrees |
| 6 | 2.807017121 | yes | agrees |
| 7 | 2.318062855 | yes | agrees |
| 8 | 2.388728777 | yes | agrees |
| 9 | 2.473815890 | yes | — |
| 10 | 2.189744159 | yes | — |

Boundary runs (recorded in `protocol.json`, reproducible with `primary.py --n`):

| N | exact infimum | identity optimal? | search nodes | wall time |
|---|---|---|---|---|
| 11 | 2.405637178 | yes | 18,741,792 | ≈ 56 s |
| 12 | 2.468445727 | yes | 207,146,123 | ≈ 11 min (676 s) |

1. **Identity optimal through the extended grid (exact).** `improvement = 0` at every
   N ≤ 12: no bijection beats the natural correspondence. The geometry pins the
   correspondence, matching CW and extending it.
2. **No convergence to zero at scale (certified).** The sorted-multiset lower bound
   stays ≈ 0.90 for N = 8 … 256 (floor `0.896271`), while the natural-correspondence
   upper bound **grows** (2.389 → 3.333). Under the fixed mean scale the infimum is
   therefore bounded below by ≈ 0.90 through N = 256 and does not approach 0.
3. **Scale degeneracy (exact).** With the scale `s` free, `s = 0` makes any
   comparison trivial (the LGH class is conformal), so a distance must be
   scale-fixed; this gate fixes it, as CW does.
4. **Search cost is the wall.** Nodes grow ≈ 10× per N (164 → 1109 → 6850 → … →
   2 × 10^8), the bottleneck-QAP hardness: exact search cannot reach "at scale".

The incomparable control (`max d_X` = 1.953 at N = 10, rising to 3.541 by N = 256) is
still **not separated** from the manifold-like range, so the gate stays
**inconclusive** for LGH convergence: `lgh_infimum_established = false`.

## 3. Boundaries

A bounded exact computation plus a certified lower bound on supplied geometry. It
extends identity-optimality and existence of a non-vanishing floor, but does **not**
establish the LGH infimum at scale, the density/commensurability condition, ensemble
convergence, or manifoldlikeness of a limit; and the floor is a property of the
fixed mean-scale convention (the free-scale version is degenerate), not a claim about
the scale-free LGH class. No metric, manifold, curvature, dynamics or gravity is
claimed. Curvature and the imported BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## 4. Evidence and limits

`primary.py` (branch-and-bound, greedy incumbent) and `reference.py` (monotone
threshold feasibility by binary search — a different exact algorithm) must agree
before publication; the driver compares with a float tolerance and refuses on any
difference. `study.py` writes create-only `results.json` and `source-freeze.json`
(freezing the gate sources and the T7 module by hash); `test_qr05cx.py` checks
identity-optimality, agreement with brute force, the certified floor, the
lower-bound-below-known-infimum relation, the recorded boundary runs and their node
growth, the inconclusive verdict and route agreement. Fixed seeds make the run
deterministic. The default suite solves N ≤ 10 (≈ 20 s); N = 11 (≈ 56 s) and N = 12
(≈ 11 min) are re-run on demand. Limits: sources ≤ 262,144 bytes, artifacts
≤ 16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
