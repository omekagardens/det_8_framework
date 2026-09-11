# QR-05CZ results

10 September 2026 (Pacific/Honolulu). **Scale-free LGH comparison complete — with
the directed-distance correction.** Building the scale-free comparison exposed a
convention defect in CW/CX: the continuum counterpart was symmetric (violating LMS
axiom A3 and the directed chain support). Correcting it withdraws the CW/CX
non-vanishing floor and **reopens** the convergence question; it does not settle it.
11 tests pass. Supplied geometry; no metric, continuum, curvature or gravity claim.

## 1. The convention defect (corrected)

Chain support is directed; the symmetric counterpart is not. Mismatched pairs:

| N | chain vs symmetric | chain vs directed |
|---|---|---|
| 8 | 18 | 0 |
| 32 | 251 | 0 |
| 256 | 15 512 | 0 |

For every timelike pair the symmetric arm contributes `|0 − τ| = τ` on the reverse
entry — the largest terms in the comparison — which dominated the distortion.

## 2. Contaminated arm (reproduces QR-05CX) vs corrected arm

| N | symmetric `fixed_identity` | symmetric bound | directed `fixed_identity` | directed bound (`c=1`) |
|---|---|---|---|---|
| 8 | 2.388729 | 0.953512 | 0.924147 | 0.924147 |
| 16 | 2.553976 | 0.933910 | 0.763952 | 0.547354 |
| 32 | 2.706160 | 0.916641 | 1.130863 | 0.342713 |
| 64 | 2.738166 | 0.896271 | 0.650927 | 0.549758 |
| 128 | 3.168405 | 0.902380 | 0.773220 | 0.340394 |
| 256 | 3.333189 | 0.907912 | 0.554086 | 0.258468 |

The symmetric arm reproduces CX's floor exactly (`min 0.896271`); the directed arm
is much smaller throughout.

## 3. The scale-free comparison and its bracketed infimum

With each matrix mean-normalized, the homothety-invariant distortion and its
certified lower bound (multi-seed means, seeds 0–3; `c* ≈ 0.90–1.05`):

| N | ℓ | scale-free identity (mean ± sd) | certified lower bound | lower bound / ℓ |
|---|---|---|---|---|
| 8 | 0.250 | 0.621 ± 0.251 | 0.498 | 1.99 |
| 16 | 0.177 | 0.788 ± 0.202 | 0.431 | 2.44 |
| 32 | 0.125 | 0.811 ± 0.153 | 0.358 | 2.86 |
| 64 | 0.088 | 0.730 ± 0.066 | 0.239 | 2.71 |
| 128 | 0.063 | 0.691 ± 0.130 | 0.187 | 2.99 |
| 256 | 0.044 | 0.612 ± 0.080 | 0.158 | 3.57 |

## Findings

1. **The CW/CX floor was a convention artifact (corrected, reclassified).** With the
   directed Lorentzian distance the distortion is `≤ ~0.9` (vs `1.8–3.3`) and the
   certified lower bound decreases **monotonically** `0.498 → 0.158` over `N = 8…256`
   (`~2–3.6 × ℓ`). The earlier "non-vanishing floor / no convergence" verdict is
   **withdrawn**; CX's floor is an artifact of the symmetric counterpart.
2. **Identity is scale-free optimal (exact, `N ≤ 7`).** By enumeration the natural
   correspondence minimises the scale-free distortion; CW's identity-optimality
   sub-finding is retained under the corrected distance.
3. **The relative scale is ≈ 1** (`c* ≈ 0.90–1.05`): with the directed distance the
   two matrices are already comparable, unlike the symmetric arm.
4. **Convergence is reopened, not established.** The natural-correspondence upper
   bound is noisy and does **not** decay clearly (`0.61–0.81`), so the scale-free
   infimum — bracketed in `[lower bound, upper bound]` — is not pinned. The
   obstruction is removed; convergence is not shown.

## What this changes and what remains

**Changes.** QR-05CW/CX's "the fixed-scale infimum does not vanish" is reclassified:
it followed from a symmetric continuum matrix that violates LMS A3 and does not
match the chain support. The obstruction is withdrawn and the scale-free question is
reopened. CW/CX's identity-optimality and scale-degeneracy sub-findings stand.

**Remains.** The scale-free infimum and its convergence (the brackets do not meet),
the density/commensurability condition, ensemble convergence, and manifoldlikeness of
a limit. No metric, continuum, curvature, dynamics or gravity is claimed. Curvature
and the imported BD operator stay parked; κ-gravity is retired and gravity is
standard GR under Option B.

## Verification and provenance

`primary.py` (golden-section scale search) and `reference.py` (bisection on the
upper/lower envelope crossing) build the matrices, the support check, the certified
bound and the report independently; the driver compares with a float tolerance and
refuses on any difference.

- Capture: `results.json`, SHA-256
  `0f8e3fc8a2cb51ff32265ce6e51ac2d3c7f143fd0f0b53e4cf85ca02400c43e7`.
- Freeze: `source-freeze.json`, SHA-256
  `f344096b04d8f910cd8ad6de389235b6ce72d62337cc45fd7b20334fc03a967b`.

CZ continues the committed `qr-05-bridge` branch (from pushed CY commit `dba8965`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md); the 231
pre-existing dirty entries remain outside it.
