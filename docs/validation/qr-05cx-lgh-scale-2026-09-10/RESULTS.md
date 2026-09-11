# QR-05CX results

10 September 2026 (Pacific/Honolulu). **LGH infimum at scale complete —
inconclusive for convergence, with three exact/certified sub-findings.** The exact
infimum over bijections is extended from brute force (N ≤ 8, CW) to a
branch-and-bound (tested to N = 10, boundary to N = 12), and a certified lower
bound on supplied geometry does not vanish to N = 256. The gate is documented as
inconclusive, not promoted. 11 tests pass. No gravity claim.

## The exact grid (branch-and-bound, brute-force validated)

`inf_GH` = min over bijections of the max pairwise normalized distortion:

| N | exact infimum | identity optimal? | brute-force check |
|---|---|---|---|
| 5 | 1.713339476 | yes | agrees |
| 6 | 2.807017121 | yes | agrees |
| 7 | 2.318062855 | yes | agrees |
| 8 | 2.388728777 | yes | agrees |
| 9 | 2.473815890 | yes | — |
| 10 | 2.189744159 | yes | — |

## Boundary runs (recorded, reproducible with `primary.py --n`)

| N | exact infimum | identity optimal? | nodes | wall time |
|---|---|---|---|---|
| 11 | 2.405637178 | yes | 18,741,792 | ≈ 56 s |
| 12 | 2.468445727 | yes | 207,146,123 | ≈ 11 min (676 s) |

Node growth is ≈ 10–11× per N (164 → 1109 → 6850 → … → 2 × 10^8): the exact
bottleneck-QAP search is the wall.

## The certified lower bound at scale

The sorted-multiset matching bound (valid at any N, no search) versus the
natural-correspondence upper bound:

| N | certified lower bound | identity upper bound | incomparable control (`max d_X`) |
|---|---|---|---|
| 8 | 0.953512 | 2.388729 | 2.160 |
| 16 | 0.933910 | 2.553976 | 2.290 |
| 32 | 0.916641 | 2.706160 | 2.820 |
| 64 | 0.896271 | 2.738166 | 3.288 |
| 128 | 0.902380 | 3.168405 | 3.495 |
| 256 | 0.907912 | 3.333189 | 3.541 |

## Findings

1. **Identity optimal through the extended grid (exact).** `improvement = 0` at
   every N ≤ 12 — the natural map is LGH-minimizing among bijections, matching CW
   and extending it.
2. **No convergence to zero at scale (certified).** The lower bound stays ≈ 0.90
   through N = 256 (floor `0.896271`) while the natural-correspondence upper bound
   grows (2.389 → 3.333). Under the fixed mean scale the infimum is bounded below by
   ≈ 0.90 and does not approach 0.
3. **Scale degeneracy (exact).** With the scale free, `s = 0` trivializes any
   comparison; the LGH class is conformal, so a distance must be scale-fixed. The
   floor in finding 2 belongs to that fixed convention, not to the scale-free class.
4. **Control not separated (inconclusive).** The incomparable control rises only to
   3.541 by N = 256, below twice the manifold-like infimum, so
   `control.distinct = false` and `lgh_infimum_established = false`.

## What this adds and what remains

Extends CW's two sub-findings (identity-optimality; conformal/scale degeneracy) to
N ≤ 12 and adds a certified, non-vanishing lower bound to N = 256, with a
demonstrated search-cost wall. What remains open: the infimum and its convergence
under a *scale-free* (not merely fixed) comparison, the density/commensurability
condition, ensemble convergence, and manifoldlikeness of a limit — all
research-grade. No metric, manifold, curvature, dynamics or gravity is claimed.

## Verification and provenance

`primary.py` (branch-and-bound) and `reference.py` (monotone threshold feasibility
by binary search) build the causality, the chain matrix, the normalization, the
exact infimum and the certified lower bound independently; the driver compares with
a float tolerance and refuses on any difference. Branch-and-bound also agrees with
brute force for N ≤ 8 in both routes.

- Capture: `results.json`, SHA-256
  `f650ab1a7b12fd9155b24d672e0b111f36d193c6be44f01189b4f7e7015070a6`.
- Freeze: `source-freeze.json`, SHA-256
  `0705d7df3ef56f9095fba1566e5395e7d9aec6ed402a66712780b1c5ef4d53ec`.

CX continues the committed `qr-05-bridge` branch (from pushed CW commit
`acd4cef`). Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md); the 231
pre-existing dirty entries remain outside it.
