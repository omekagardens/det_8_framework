# QR-05DL (direction A): a higher-order manifoldlike invariant — interval self-similarity

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — no physical claim.** QR-05DK showed the 2-point and link invariants are
insufficient (a geometry-free bipartite order reaches the sprinkle's link fraction). This
gate tests a genuinely **higher-order** invariant: the **interval self-similarity**
`S = ⟨f(I(x,y))⟩ / f_global` — a manifoldlike set is self-similar (its intervals are
sprinkles of the same dimension, so `S ≈ 1`). Sprinkles pass; the QR-05DK counterexamples
fail.

## 1. Pre-specification

- **Question.** Is the interval self-similarity `S = ⟨f(I(x,y))⟩ / f_global ≈ 1` for
  sprinkles (self-similar) and **violated** by the geometry-free counterexamples?
- **Invariants.** `S`; the **interval density** `ρ_int = P(I(x,y) nonempty) = 1 − ℓ`; the
  **dimension match** `|d_MM(⟨f(I)⟩) − d_MM(f_global)|`.
- **Objects.** sprinkles `d = 2, 3, 4` (`n = 250`); transitive percolation `p = 0.02, 0.05, 0.1`;
  the complete bipartite order; layer-cake `k = 3, 4`. Intervals of size `m ∈ [3, 30]`
  (`cap 800`).

## 2. Results

| object | `f_global` | `d_MM(global)` | interval density | `⟨f(I)⟩` | `S` |
|---|---|---|---|---|---|
| sprinkle d=2 | 0.471 | 2.08 | 0.929 | 0.505 | **1.07** |
| sprinkle d=3 | 0.242 | 2.93 | 0.733 | 0.214 | **0.88** |
| sprinkle d=4 | 0.083 | 4.22 | 0.419 | 0.076 | **0.92** |
| TP p=0.02 | 0.120 | 3.78 | 0.844 | 0.815 | **6.77** |
| TP p=0.05 | 0.544 | 1.89 | 0.955 | 0.618 | 1.14 |
| TP p=0.1 | 0.811 | 1.32 | 0.973 | 0.585 | 0.72 |
| bipartite | 0.502 | 1.99 | **0.000** | — | — |
| layer-cake k=3 | 0.669 | 1.60 | 0.335 | *(no intervals in range)* | — |
| layer-cake k=4 | 0.753 | 1.43 | 0.503 | *(no intervals in range)* | — |

The **interval density** column is the corrected v2 statistic (`ρ_int` over the complete
comparable-pair sweep, `= 1 − ℓ`); the original v1 capture reported a partial-sweep
fraction instead — see [SUPERSEDED.md](SUPERSEDED.md). Nothing else in the table changed.

- **Sprinkles are self-similar:** `S ≈ 0.88–1.07` (≈1 up to finite-size bias), and the
  interval ordering fraction yields the same dimension as the global one.
- **The counterexamples fail:** the bipartite order has **no intervals** (density 0), and
  the layer-cake has **no intervals in the tested size range** (its intervals are whole
  layers) — both leave `S` undefined. Transitive percolation has a large **dimension
  mismatch** at low `f` (`S = 6.77` at `f = 0.12`): its intervals are far *more* ordered
  than a sprinkle's.

## 3. Findings

1. **The interval self-similarity is a genuine higher-order manifoldlike invariant** — it
   separates sprinkles (`S ≈ 1`) from the QR-05DK geometry-free counterexamples.
2. **It closes the QR-05DK gap:** DK's "the link fraction is insufficient" is answered —
   the interval structure (3-point and higher) *does* distinguish.
3. **Manifoldlikeness is multi-faceted:** no single invariant (2-point, link, or interval
   self-similarity) is sufficient, and **a no-go is not established**.
4. **Finite-size caveat:** `S` for sprinkles is biased (0.88–1.07 at `n = 250`); at small
   `n` (120) the `d = 4` value was 0.51 with only 46 intervals sampled.

## 4. Boundaries

The invariants (Myrheim–Meyer, interval self-similarity) and the growth laws are
**borrowed/simple**; this is a bounded discrimination test, not a theorem, and novelty is
**low–moderate**. `S` is finite-size-noisy, the interval-size window `[3, 30]` is a choice,
and "geometry-free law" is not precisely characterized. No physical, metric, continuum,
curvature, dynamics or gravity claim; correspondence-level / Status M.

## 5. Evidence

`primary.py` (interval causality; transitive percolation / bipartite / layer-cake;
`S`, interval density, dimension) and `reference.py` (light-cone-dominance causality;
recoded) compute the invariants and the flags independently — RNG streams shared by
construction (documented). The driver refuses on any difference. `test_qr05dl.py`
(11 tests) pins the chain (`S = 1`, interval = chain), bipartite (`no intervals`),
layer-cake (intervals are whole layers, out of window) and complete-sweep
(`ρ_int = (n−2)/n`) known answers and the flags. `study.py` writes create-only
`results.json` and `source-freeze.json`. The v1 capture's `interval_density` column is
corrected and retained as superseded ([SUPERSEDED.md](SUPERSEDED.md)). Decision record:
[RESULTS.md](RESULTS.md).
