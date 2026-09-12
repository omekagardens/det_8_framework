# QR-05DM results

11 September 2026 (Pacific/Honolulu). **A stronger adversary: geometry-free laws matched
onto a sprinkle's ordering fraction fail the interval-abundance distribution.** Transitive
percolation and a two-block ladder are each **bisected onto** a reference sprinkle's
`f_global` (worst gap `9.3e-4`), so the 2-point statistic matches by construction — and
every one of them is separated by the per-size distribution of the interval ordering
fraction. Two of the three also sit **inside QR-05DL's mean self-similarity band**
(`S = 0.99, 1.00`) and so would pass a mean-only test. Direction A of the Track-B geometry
program. Track-B exploratory (Status M); 12 tests pass; no physical claim.

## 0. Setup

**Question.** Can a geometry-free law *matched on the 2-point ordering fraction* be
separated by the **interval abundance** — the distribution of `f(I)` over intervals of each
size `m` — or does matching `f_global` defeat the higher-order invariants?

**Adversaries** (geometry-free, each matched by bisection onto the reference sprinkle's
`f_global`):

- `tp_matched_d{2,3}` — **transitive percolation** at `p*` (closure-dense, homogeneous; the
  QR-05DI/DJ law).
- `ladder_matched_d2` — a **2-block ladder**: two contiguous blocks, each internally a
  transitive percolation at `p_intra`, every lower-block element below every upper-block
  element, transitively closed. A preferred **foliation with ordered blocks**;
  `p_intra = 0` degenerates to QR-05DK's complete bipartite order.

**Instrument.** For each size `m ∈ {6, 10, 14, 18, 22}`: count, mean and sd of `f(I)`, plus
a 10-bin histogram. An adversary **fails** if some size has
`|mean_adversary(m) − mean_sprinkle(m)| > 0.05`, **or** its histogram L1 distance exceeds
3× the sprinkle's own split-half noise floor, **or** it has no intervals in the window
(a degenerate interval structure). QR-05DL's mean instrument `S` is carried alongside.

**Controls / known answers.** chain (`f(I) = 1`, `sd = 0`, `ρ_int = (n−2)/n`); complete
bipartite order (`ρ_int = 0`, no intervals). **Protocol.** `n = 192`, `seed = 11`, window
`[6, 22]`, `cap = 400` per size, 40 bisection steps on `[10⁻⁴, 1]`.

## 1. Results (`n = 192`)

| object | `f_global` | match gap | `ρ_int` | `S` (DL's instrument) | `⟨f(I)⟩` at `m = 6,10,14,18,22` |
|---|---|---|---|---|---|
| sprinkle d=2 | 0.5392 | — | 0.921 | 0.90 | 0.479, 0.475, 0.497, 0.500, 0.501 |
| tp_matched_d2 | 0.5389 | 3.3e-4 | 0.945 | **0.99** | 0.656, 0.527, 0.457, 0.415, 0.397 |
| ladder_matched_d2 | 0.5389 | 2.7e-4 | 0.856 | **1.00** | 0.562, 0.631, 0.423, 0.535, 0.366 |
| sprinkle d=3 | 0.1961 | — | 0.657 | 1.04 | 0.197, 0.197, 0.225, 0.218, 0.233 |
| tp_matched_d3 | 0.1970 | 9.3e-4 | 0.874 | **3.06** | 0.673, 0.500, 0.425, 0.349, 0.353 |
| chain (control) | 1.0000 | — | 0.990 | 1.00 | 1.000, 1.000, 1.000, 1.000, 1.000 |
| bipartite (control) | 0.5026 | — | **0.000** | — | *(no intervals)* |

| adversary vs reference | max `|Δmean|` | mean-failing sizes | max histogram L1 | histogram-failing sizes | verdict |
|---|---|---|---|---|---|
| tp_matched_d2 vs sprinkle d=2 | 0.177 | 6, 10, 18, 22 | 1.03 | 10, 18, 22 | **fails** |
| ladder_matched_d2 vs sprinkle d=2 | 0.156 | 6, 10, 14, 22 | 1.43 | 10, 14, 18, 22 | **fails** |
| tp_matched_d3 vs sprinkle d=3 | 0.475 | 6, 10, 14, 18, 22 | 1.86 | 6, 10, 14, 18 | **fails** |

Matched parameters: `tp_matched_d2` `p* = 0.05568`, `tp_matched_d3` `p* = 0.03006`,
`ladder_matched_d2` `p_intra = 0.02564`. Matched dimension: d=2 sprinkle `d_MM = 1.899` vs
TP `1.900`; d=3 sprinkle `3.189` vs TP `3.183`.

## 2. What the table says

- **The 2-point match is exact.** Worst gap `9.3e-4` (≤ 0.5% of `f`), so each adversary is,
  by construction, what a `f_global`-only discriminator would accept — and the same for
  `d_MM` (matched to within `0.006`).
- **The mean instrument is not enough.** `tp_matched_d2` (`S = 0.99`) and
  `ladder_matched_d2` (`S = 1.00`) both pass QR-05DL's `S ∈ [0.8, 1.7]` band, yet the
  abundance distribution separates them: their per-size means depart by up to `0.18`/`0.16`
  and the histograms exceed the sprinkle's split-half floor.
- **The separation is not a single-family artifact.** The homogeneous TP adversary and the
  foliated ladder adversary both fail, at `d = 2` and `d = 3`.
- **The controls behave as known answers.** The chain has `f(I) = 1`, `sd = 0` at every size
  and `ρ_int = (n−2)/n = 0.990`; the bipartite order has no intervals at all.

## Findings

1. **Matching the 2-point statistic does not make a geometry-free law manifoldlike.** The
   stronger adversary does **not** defeat the higher-order invariants: `f`, `d_MM` and the
   interval-abundance distribution all still separate it.
2. **The interval-abundance distribution is strictly stricter than the mean `S`.** Two of
   three adversaries pass the mean band and fail the distribution
   (`interval_abundance_is_stricter_than_the_self_similarity_mean`), so QR-05DL's single
   mean was under-powered even where it "passed".
3. **Both a closure-dense and a foliation adversary fail** — the QR-05DK lesson (the link
   fraction alone is insufficient) extends to the *mean* interval self-similarity, and the
   distribution closes that gap.
4. **No no-go is established.** A no-go would need an adversary matching the whole
   distribution — the untested covariance-matched law.

**Incidental.** Building this gate exposed a defect in QR-05DL's `interval_density`: the
pair sweep stopped at the interval-sample `cap`, so the reported density was a partial-sweep
fraction. It is corrected there (`results.superseded-density-v1.json`,
[SUPERSEDED.md](../qr-05dl-interval-self-similarity-2026-09-11/SUPERSEDED.md)); this gate's
`ρ_int` is computed over a complete sweep.

## What this changes and what remains

**Changes.** Direction A's discriminator set is upgraded from "a single mean interval
self-similarity" (QR-05DL) to "the interval-abundance distribution", and the adversary is
upgraded from incidentally-similar to **`f`-matched by construction**. The stronger
adversary fails, so the multi-faceted-invariant picture is reinforced rather than refuted.

**Remains.** A law engineered to match the **whole** interval-size profile (a
covariance-matched adversary, including the interval-in-interval structure); a precise
characterization of "geometry-free law"; the unconditional LPP-concentration proof (QR-05DD
gave bounded 1+1 support, α = 0.27); and the 3+1 case. Also noted: the sprinkle's
`f_global` carries a realization wobble of `~0.03` at `n ≈ 200` (≈ 8–14× the naive
binomial, since pairs are correlated), so `d_MM` estimates inherit a `±0.1` spread — a
caveat for every `d_MM` figure in this program.

No physical, metric, continuum, curvature, dynamics or gravity claim. Unchanged: gravity
standard GR (Option B); curvature and the imported BD operator parked; κ-gravity retired.

## Verification and provenance

`primary.py` carries the order as **bitmask rows** and closes it with a bitset union;
`reference.py` carries it as a **boolean matrix** and closes it with **BFS reachability**,
with recoded statistics. The RNG streams and the deterministic bisection search are shared
by construction (documented). The driver compares with a float tolerance and refuses on any
difference. `test_qr05dm.py` (12 tests) pins the chain, bipartite and `p_intra = 0 ⇒
bipartite` known answers, the histogram binning, the matched-adversary claim, the
stricter-instrument claim and the flags.

- Capture: `results.json`, SHA-256 `8a3230a07f61474b0ccea3f87fc019729115dbe6f1aa47613fcdc71529cfbdcf`.
- Freeze: `source-freeze.json`, SHA-256 `d585664bda19569a49e7bf1c1f7cba765cd99859f20da1eb83aa297e30944b1f`.

QR-05DM continues the committed `qr-05-bridge` branch (from the QR-05DL correction commit
`3539e5f`). Publication is this directory and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
