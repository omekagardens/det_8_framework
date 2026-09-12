# QR-05DM (direction A): a stronger adversary — the f-matched law and the interval-abundance distribution

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — no physical claim.** QR-05DL found that the interval self-similarity
`S = ⟨f(I(x,y))⟩ / f_global` separates sprinkles from the QR-05DK geometry-free
counterexamples — but DL's adversaries were only *incidentally* close in ordering fraction.
This gate builds the strongest cheap adversary: a geometry-free law whose `f_global` is
**bisected onto** a sprinkle's, so the 2-point statistic matches *by construction*. It then
tests it with a stricter instrument than a single mean — the **interval abundance**, the
per-size distribution of the interval ordering fraction. Every matched adversary fails.

This gate also found and records the correction of QR-05DL's `interval_density`
(a partial-sweep artifact; see [QR-05DL's SUPERSEDED.md](../qr-05dl-interval-self-similarity-2026-09-11/SUPERSEDED.md)).

## 1. Pre-specification

- **Question.** Can a geometry-free law *matched on the 2-point ordering fraction* be
  separated by the interval-abundance distribution — or does matching `f_global` defeat the
  higher-order invariants?
- **Adversaries** (all geometry-free; each matched by bisection onto the reference
  sprinkle's `f_global`):
  - **`tp_matched_d{2,3}`** — transitive percolation at `p*` (closure-dense, no foliation;
    QR-05DI/DJ's law).
  - **`ladder_matched_d2`** — a 2-block ladder: two blocks, each internally a transitive
    percolation at `p_intra`, every lower-block element below every upper-block element,
    closed (`p_intra = 0` reproduces QR-05DK's complete bipartite order) — a **foliation
    with ordered blocks**.
- **Instrument.** For each interval size `m ∈ {6, 10, 14, 18, 22}`: the **count, mean and
  sd** of `f(I)` and a 10-bin histogram. Separation: `|mean_adversary(m) − mean_sprinkle(m)| > 0.05`
  at some `m`, **or** the histogram L1 distance exceeds 3× the sprinkle's own split-half
  noise floor, **or** the adversary has no intervals in the window at all (degenerate).
  QR-05DL's mean instrument (`S`) is reported alongside for comparison.
- **Controls / known answers.** A chain (every interval is a chain: `f(I) = 1`, `sd = 0`,
  `ρ_int = (n−2)/n`) and the complete bipartite order (no intervals, `ρ_int = 0`).
- **Protocol.** `n = 192`, `seed = 11`, window `[6, 22]`, per-size `cap = 400`, 40 bisection
  steps on `[10⁻⁴, 1]`.

## 2. Results (`n = 192`)

| object | `f_global` | `match gap` | `ρ_int` | `S` (DL's instrument) | `⟨f(I)⟩` by size `6,10,14,18,22` |
|---|---|---|---|---|---|
| sprinkle d=2 | 0.5392 | — | 0.921 | 0.90 | 0.479, 0.475, 0.497, 0.500, 0.501 |
| **tp_matched_d2** | 0.5389 | 3.3e-4 | 0.945 | **0.99** | 0.656, 0.527, 0.457, 0.415, 0.397 |
| **ladder_matched_d2** | 0.5389 | 2.7e-4 | 0.856 | **1.00** | 0.562, 0.631, 0.423, 0.535, 0.366 |
| sprinkle d=3 | 0.1961 | — | 0.657 | 1.04 | 0.197, 0.197, 0.225, 0.218, 0.233 |
| **tp_matched_d3** | 0.1970 | 9.3e-4 | 0.874 | **3.06** | 0.673, 0.500, 0.425, 0.349, 0.353 |
| chain (control) | 1.0000 | — | 0.990 | 1.00 | 1.000, 1.000, 1.000, 1.000, 1.000 |
| bipartite (control) | 0.5026 | — | **0.000** | — *(no intervals)* | — |

| adversary vs reference | `|Δmean|` max | sizes failing the mean | histogram L1 (max) | sizes failing the histogram | verdict |
|---|---|---|---|---|---|
| tp_matched_d2 vs sprinkle d=2 | 0.177 (m=6) | 6, 10, 18, 22 | 1.03 | 10, 18, 22 | **fails** |
| ladder_matched_d2 vs sprinkle d=2 | 0.156 (m=10) | 6, 10, 14, 22 | 1.43 | 10, 14, 18, 22 | **fails** |
| tp_matched_d3 vs sprinkle d=3 | 0.475 (m=6) | 6, 10, 14, 18, 22 | 1.86 | 6, 10, 14, 18 | **fails** |

Matched parameters: `tp_matched_d2` `p* = 0.05568`, `tp_matched_d3` `p* = 0.03006`,
`ladder_matched_d2` `p_intra = 0.02564`. Matched Myrheim–Meyer dimension: d=2 sprinkle
`d_MM = 1.899` vs TP `1.900`; d=3 sprinkle `3.189` vs TP `3.183`.

- **The 2-point match is exact** (worst gap `9.3e-4`, i.e. ≤ 0.5% of `f`), so the comparison
  is like-for-like: each adversary *is* what a `f_global`-only discriminator would accept.
- **The mean instrument is not enough.** `tp_matched_d2` (`S = 0.99`) and
  `ladder_matched_d2` (`S = 1.00`) both sit **inside QR-05DL's `S ∈ [0.8, 1.7]` band** and
  would pass a mean-only test — yet both are separated by the abundance distribution.
- **The abundance distribution separates every adversary.** The per-size mean departs by up
  to `0.18` / `0.16` / `0.48` (vs the `0.05` tolerance) and the histograms sit outside the
  sprinkle's split-half noise floor.

## 3. Findings

1. **A geometry-free law matched on the 2-point statistic is still not manifoldlike** — in
   `f`, `d_MM` **and** the interval-abundance distribution. Matching the 2-point statistic
   is not sufficient.
2. **The interval-abundance distribution is a stricter instrument than DL's mean `S`**:
   both d = 2 adversaries pass the mean band and fail the distribution
   (`interval_abundance_is_stricter_than_the_self_similarity_mean`).
3. **Both closure-dense and foliation adversaries fail** — the separation is not an
   artifact of one family (TP is homogeneous; the 2-block ladder is a preferred foliation).
4. **No no-go is established.** A no-go would need an adversary matching the *whole*
   distribution — not tested here.

## 4. Boundaries

The invariants and the growth laws are **borrowed/simple**; this is a bounded
discrimination test, not a theorem, and novelty is **low–moderate**. Specific limits:

- The adversaries are two cheap families matched on **one** statistic; "geometry-free law"
  is still not precisely characterized, and a law **fitted to the whole interval
  distribution** (a covariance-matched adversary) is the untested next step.
- The `0.05` mean tolerance and the 3× split-half histogram factor are **choices**; the
  failing sizes are reported for every adversary so the reader can re-threshold.
- The window `[6, 22]` and `n = 192` are choices; at `n = 192` the large-`m` samples are
  thin (`tp_matched_d3` has 4 intervals at `m = 22`), so the small-`m` evidence carries the
  result.
- **Realization variance of `f`.** The sprinkle's `f_global` is `0.5392` at `n = 192`,
  `seed = 11` against the analytic `f(2) = 0.5`; across seeds the sd of `f` at `n ≈ 200–2000`
  is `0.029 → 0.005` — roughly **8–14× the naive binomial** (which ignores pair–pair
  correlations). `d_MM` inherits a `±0.1` wobble. This is why the comparison is
  **`f`-matched**: a single sprinkle realization is not a fixed target. (The sampler itself
  checks out: `P(t < ¼) = 0.125` and `E|x| = 1/6` on 20 000 points, both exact.)

No physical, metric, continuum, curvature, dynamics or gravity claim — correspondence-level
/ Status M.

## 5. Evidence

`primary.py` (order as **bitmask rows** with a bitset transitive closure) and `reference.py`
(order as a **boolean matrix** with **BFS reachability**) construct the same adversaries and
recoded statistics; the RNG streams and the deterministic bisection search are shared by
construction (documented). The driver refuses on any difference. `test_qr05dm.py` (12 tests)
pins the chain, bipartite and `p_intra = 0 ⇒ bipartite` known answers, the histogram binning,
and the flags. `study.py` writes create-only `results.json` and `source-freeze.json`.
Decision record: [RESULTS.md](RESULTS.md).
