# QR-05DK results

11 September 2026 (Pacific/Honolulu). **The no-go fails: a geometry-free 2-layer
(bipartite) order exceeds the sprinkle's link fraction at every dimension, so the
QR-05DI/DJ under-linking obstruction is class-specific (closure-dense), not a general
no-go; the link fraction alone does not capture manifoldlikeness.** Direction A of the
Track-B geometry program. Track-B exploratory (Status M); 9 tests pass; no physical claim.

## 0. Setup

Manifoldlike locus: sprinkles `d = 2..5` (`n = 200`), summarised by the ordering fraction
`f`, link fraction `ℓ`, mean interval `μ`. Geometry-free family: transitive percolation
(closure-dense) and 2-layer bipartite orders (sparse, no intermediates), plus layer-cake
controls.

## 1. The manifoldlike locus

| d | f | ℓ | μ |
|---|---|---|---|
| 2 | 0.494 | 0.079 | 0.108 |
| 3 | 0.238 | 0.300 | 0.036 |
| 4 | 0.074 | 0.638 | 0.006 |
| 5 | 0.043 | 0.792 | 0.003 |

## 2. Reachability at matched `f`

| dim | ℓ sprinkle | TP ℓ | TP ratio | bipartite ℓ | bipartite ratio |
|---|---|---|---|---|---|
| 2 | 0.079 | 0.059 | 0.74 | 1.00 | 12.70 |
| 3 | 0.300 | 0.111 | 0.37 | 1.00 | 3.34 |
| 4 | 0.638 | 0.277 | 0.43 | 1.00 | 1.57 |
| 5 | 0.792 | 0.391 | 0.49 | 1.00 | 1.26 |

- **Closure-dense (TP):** under-linked (`ratio < 0.85`) at every dimension — the QR-05DI/DJ
  obstruction.
- **Bipartite:** `ℓ = 1.0` for all `f ≤ ½` — **exceeds** the sprinkle at every dimension
  (ratio up to 12.7). A geometry-free law reaches and passes the manifoldlike locus. The
  **no-go fails**.

Layer-cake controls (complete `k` layers): `k = 2 → (f = 0.503, ℓ = 1.0, μ = 0)`;
`k = 4 → (0.754, 0.5, 0.167)` — likewise geometry-free and partly above the locus.

## Findings

1. **No-go fails.** Geometry-free laws reach/exceed the sprinkle's link fraction (the
   bipartite order).
2. **The obstruction is class-specific.** Under-linking is a closure-dense property, not a
   general no-go.
3. **Link fraction alone is insufficient.** The bipartite order matches/exceeds `ℓ` yet is
   non-manifoldlike (preferred 2-layer foliation; `μ = 0`).
4. **What a no-go needs.** A higher-order invariant (interval structure + covariance) with a
   provenance-independent bound.

## What this changes and what remains

**Changes.** The "no-go" hypothesis (raised as plausible in the QR-05DI/DJ discussion) is
**pursued and refuted** at the link-fraction level: the manifoldlike locus is reachable by
simple geometry-free laws. The obstruction is localized to closure-dense laws, and the
*correct* requirement for manifoldlikeness is a higher-order (interval/covariance) match —
not the link fraction. This corrects the earlier speculation.

**Remains.** Whether a no-go holds with a *higher-order* manifoldlike invariant; a precise
characterization of "geometry-free law" (a real theorem would need it); and the DET-native
law question from QR-05DJ (a record-independent-order law). No physical, metric, continuum,
curvature, dynamics or gravity claim. Unchanged: gravity standard GR (Option B); curvature
and the imported BD operator parked; κ-gravity retired.

## Verification and provenance

`primary.py` (interval causality; transitive percolation and bipartite recoded; statistics)
and `reference.py` (light-cone-dominance causality; recoded; statistics recoded) build the
locus, the geometry-free curves, the matched comparison and the flags independently — the
RNG streams are shared by construction (documented). The driver compares with a float
tolerance and refuses on any difference. `test_qr05dk.py` pins the bipartite (`ℓ = 1`,
`μ = 0`) and layer-cake (`ℓ = 1, ½`; `μ = 0, ⅙`) known answers and the flags.

- Capture: `results.json`, SHA-256 `d10dedc230696e63a3c98d67e820c511ccf015f5dc896d04cddd812cc6572fec`.
- Freeze: `source-freeze.json`, SHA-256 `e7550512dad4ab5e54a4bc9faddf8c57cef70740701eb589e6c25ea2e551023a`.

QR-05DK continues the committed `qr-05-bridge` branch (from the QR-05DJ commit `2c40863`).
Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
