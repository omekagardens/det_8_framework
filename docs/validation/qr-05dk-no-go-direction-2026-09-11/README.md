# QR-05DK (direction A, no-go): is the manifoldlike locus reachable by a geometry-free law?

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — no physical claim.** The no-go direction: **the no-go fails.** The
QR-05DI/DJ obstruction — geometry-free laws being *under-linked* — holds only for the
**closure-dense** family; a sparse **2-layer (bipartite) order** is a geometry-free law that
**exceeds** the sprinkle's link fraction at every dimension. So geometry-free laws *do*
reach the manifoldlike locus in link fraction, and the link fraction alone does not capture
manifoldlikeness. A genuine no-go needs a higher-order invariant.

## 1. Pre-specification

- **Question.** Is the **manifoldlike locus** (sprinkles) reachable by any **geometry-free
  law**, or is *no* geometry-free law manifoldlike?
- **Manifoldlike locus.** Sprinkles `d = 2, 3, 4, 5` (`n = 200`), summarised by the
  ordering fraction `f`, the link fraction `ℓ` (Hasse / comparable), and the mean interval
  `μ`.
- **Geometry-free family.**
  - **transitive percolation** (closure-dense: pair related w.p. `p`, then closure);
  - **2-layer bipartite** (sparse: layer-0 → layer-1 relations w.p. `p`, no intermediates);
  - **layer-cake** (`k` complete layers) as a further control.
- **Test.** At each sprinkle's `f`, compare the link fraction of the geometry-free laws.

## 2. Results

**Manifoldlike locus** (as `f` falls, high-`d` sprinkles have shorter intervals → more links):

| d | f | ℓ | μ |
|---|---|---|---|
| 2 | 0.494 | 0.079 | 0.108 |
| 3 | 0.238 | 0.300 | 0.036 |
| 4 | 0.074 | 0.638 | 0.006 |
| 5 | 0.043 | 0.792 | 0.003 |

**Matched comparison** at each sprinkle `f`:

| dim | ℓ sprinkle | ℓ (transitive percolation) | TP ratio | ℓ (bipartite) | bipartite ratio |
|---|---|---|---|---|---|
| 2 | 0.079 | 0.059 | 0.74 (under) | **1.00** | **12.7 (over)** |
| 3 | 0.300 | 0.111 | 0.37 (under) | **1.00** | **3.34 (over)** |
| 4 | 0.638 | 0.277 | 0.43 (under) | **1.00** | **1.57 (over)** |
| 5 | 0.792 | 0.391 | 0.49 (under) | **1.00** | **1.26 (over)** |

The bipartite order has **ℓ = 1.0 at every `f ≤ ½`** (no intermediates, so every comparable
pair is a cover) — a geometry-free law that reaches *and exceeds* the manifoldlike locus.

## 3. Findings

1. **The no-go fails.** Geometry-free laws are **not** confined below the sprinkle's link
   fraction: a 2-layer bipartite order exceeds it at every dimension.
2. **The QR-05DI/DJ obstruction is class-specific.** Closure-dense laws (transitive
   percolation, record-κ) are under-linked; that is a property of *that* family, not a
   general no-go.
3. **The link fraction alone does not capture manifoldlikeness.** The bipartite order
   matches/exceeds the sprinkle's link fraction yet is plainly non-manifoldlike — a
   preferred 2-layer foliation, and empty intervals (`μ = 0`).
4. **What a genuine no-go needs:** a higher-order manifoldlike invariant (interval
   structure and covariance) with a provenance-independent bound — the link fraction is
   insufficient (both sprinkles and layer-cakes make links).

## 4. Boundaries

`TP`, the bipartite/layer-cake orders, and the `(f, ℓ, μ)` statistics are **borrowed/simple**
constructions; the gate is a bounded discrimination test, not a theorem, and novelty is
**low–moderate**. "Reachable" here means in the tested invariants; a no-go over *all*
geometry-free laws is not addressed. No physical, metric, continuum, curvature, dynamics or
gravity claim; correspondence-level / Status M. The honest state of the no-go: **not
established, and refuted at the link-invariant level**; the interval structure (`μ`)
separates the specific bipartite construction but is not a proof.

## 5. Evidence

`primary.py` (interval causality; transitive percolation and bipartite recoded; statistics
and the report) and `reference.py` (light-cone-dominance causality; recoded; statistics
recoded) compute the locus, the geometry-free curves, the matched comparison and the flags
independently — the RNG streams are shared by construction (documented). The driver refuses
on any difference. `test_qr05dk.py` (9 tests) pins the bipartite (`ℓ = 1`, `μ = 0`) and
layer-cake (`ℓ = 1, ½`; `μ = 0, ⅙`) known answers and the flags. `study.py` writes
create-only `results.json` and `source-freeze.json`. Decision record: [RESULTS.md](RESULTS.md).
