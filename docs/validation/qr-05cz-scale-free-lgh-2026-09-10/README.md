# QR-05CZ: scale-free LGH comparison and the directed-distance correction

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.
Outcome: a convention defect is corrected, the CW/CX obstruction is withdrawn, and
convergence is reopened — not proved.** Building the scale-free comparison required
fixing the continuum counterpart: CW/CX built it symmetrically, which violates the
Minguzzi–Suhr axiom A3 and does not match the directed chain support. This gate
exhibits the defect, reproduces the contaminated arm, recomputes with the directed
Lorentzian distance, and answers the open scale-free question. No metric, continuum,
curvature or gravity is claimed.

Continue [QR-05CX](../qr-05cx-lgh-scale-2026-09-10/README.md) and the recorded Next.

## 1. The convention defect

The discrete chain time-separation is **directed**: `a[i][j] > 0` only for
`i ≺ j`, and `a[j][i] = 0` on the reverse (this is what CV checks as axiom A3 for
the chain). The Lorentzian distance is directed too: `d(x,y) > 0 ⇒ d(y,x) = 0`.

CW/CX's continuum counterpart used `|dt|²`, so it is **symmetric**,
`b[i][j] = b[j][i] > 0` on every timelike pair. That injects a reverse-direction
term `|0 − τ| = τ` at every timelike pair — the largest entries in the comparison —
so the distortion was dominated by them. The support mismatch (chain vs the
symmetric counterpart) is exact and grows:

| N | mismatched pairs (chain vs symmetric) | mismatched pairs (chain vs directed) |
|---|---|---|
| 8 | 18 | 0 |
| 32 | 251 | 0 |
| 256 | 15 512 | 0 |

## 2. The contaminated arm and the corrected arm

`fixed_identity` = `max |d_X(i,j) − d_Y(i,j)|`; the certified bound is the
sorted-multiset matching bound at the fixed scale `c = 1` for both arms here (the
scale-optimised bound appears in §3).

| N | symmetric `fixed_identity` | symmetric bound | directed `fixed_identity` | directed bound (`c=1`) |
|---|---|---|---|---|
| 8 | 2.388729 | 0.953512 | 0.924147 | 0.924147 |
| 16 | 2.553976 | 0.933910 | 0.763952 | 0.547354 |
| 32 | 2.706160 | 0.916641 | 1.130863 | 0.342713 |
| 64 | 2.738166 | 0.896271 | 0.650927 | 0.549758 |
| 128 | 3.168405 | 0.902380 | 0.773220 | 0.340394 |
| 256 | 3.333189 | 0.907912 | 0.554086 | 0.258468 |

The symmetric arm reproduces QR-05CX exactly (`lower_bound` min `0.896271`). The
directed arm is much smaller throughout.

## 3. The scale-free comparison

With each matrix mean-normalized (the overall pair scale is a gauge), the free
parameter is the **global relative scale** `c` (a homothety):

```text
inf over c > 0 of  min over bijections sigma of  max over pairs |d_X(i,j) - c d_Y(sigma i, sigma j)|.
```

Using the directed distance, multi-seed means (seeds 0–3); the relative scale is
`c* ≈ 0.90–1.05` (single-seed arm):

| N | ℓ = √(AREA/N) | scale-free identity (mean ± sd) | certified lower bound | lower bound / ℓ |
|---|---|---|---|---|
| 8 | 0.250 | 0.621 ± 0.251 | 0.498 | 1.99 |
| 16 | 0.177 | 0.788 ± 0.202 | 0.431 | 2.44 |
| 32 | 0.125 | 0.811 ± 0.153 | 0.358 | 2.86 |
| 64 | 0.088 | 0.730 ± 0.066 | 0.239 | 2.71 |
| 128 | 0.063 | 0.691 ± 0.130 | 0.187 | 2.99 |
| 256 | 0.044 | 0.612 ± 0.080 | 0.158 | 3.57 |

## 4. Findings

1. **The CW/CX floor was a convention artifact (corrected).** The symmetric
   counterpart injected reverse-direction terms; with the directed Lorentzian
   distance the distortion is `≤ ~0.9` (vs `1.8–3.3`) and the certified lower bound
   decreases **monotonically** from `0.498` (N=8) to `0.158` (N=256) — roughly
   `2–3.6 × ℓ`. So the earlier "non-vanishing floor / no convergence" verdict is
   **withdrawn and reclassified**.
2. **Identity is scale-free optimal on the exact grid** (`N ≤ 7`, by enumeration):
   the natural correspondence minimises the scale-free distortion, extending CW's
   sub-finding (which is retained).
3. **The relative scale is ≈ 1** (`c* ≈ 0.90–1.05`): with the directed distance the
   two matrices are already in comparable units, unlike the symmetric arm.
4. **Convergence is reopened, not established.** The natural-correspondence upper
   bound does **not** visibly decay (`0.61–0.81`, noisy); the scale-free infimum is
   bracketed in `[lower bound, upper bound]` and neither bracket pins it. The
   obstruction is removed; convergence is not shown.

## 5. Boundaries

A bounded computation on supplied geometry. It corrects a convention defect, reclassifies
the CW/CX floor, and reports a decaying certified lower bound with a non-decaying
natural-correspondence upper bound. It does **not** establish the scale-free LGH
infimum or convergence, the density/commensurability condition, ensemble convergence,
or manifoldlikeness of a limit, and it makes no metric, continuum, curvature, dynamics
or gravity claim. Curvature and the imported BD operator stay parked; κ-gravity is
retired and gravity is standard GR under Option B.

## 6. Evidence and limits

`primary.py` (golden-section scale search) and `reference.py` (bisection on the
upper/lower envelope crossing) build the matrices, the support check, the certified
bound and the report independently; the driver compares with a float tolerance and
refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05cz.py` checks the support defect, the reproduced symmetric floor, the
directed reduction, the monotone lower-bound decay, the exact-grid optimality, the
non-claim of convergence and route agreement. Fixed seeds make the run deterministic.
Limits: sources ≤ 262,144 bytes, artifacts ≤ 16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
