# QR-05DL — supersession of the v1 capture (interval-density statistic)

11 September 2026 (Pacific/Honolulu). **The `interval_density` column of the original
QR-05DL capture is a partial-sweep artifact and is corrected here; the v1 capture is
retained as evidence.** No other quantity, flag or conclusion of QR-05DL changes.

## 1. The defect

QR-05DL reports the **interval density** `ρ_int = P(I(x,y) nonempty)` over comparable
pairs of a causal set, which the gate's own pre-specification defines as `1 − ℓ` (one
minus the link fraction). `interval_stats` accumulated

    if I: nonempty += 1
    ...
    if len(fis) >= cap: break          # v1: breaks the *pair sweep*
    ...
    rho = nonempty / len(comp)         # ... over the *whole* comparable-pair list

so once the interval sample reached `cap = 800`, the loop **ended**, leaving `nonempty`
counted over only the prefix of pairs already scanned while the denominator stayed the
full comparable-pair count. The result is a fraction of the wrong thing — roughly the
fraction of the sweep completed — not the interval density.

The error is invisible to the gate's own route-agreement check: `primary.py` and
`reference.py` shared the same sweep structure, so both routes agreed on the same wrong
value (the same failure mode as QR-05DA's `p99`, where a mislabelled statistic was
consistent across routes).

It was found while building QR-05DM (the stronger-adversary gate), which re-derives the
interval density over a complete sweep.

## 2. What changed

The sweep is now complete in both routes; `cap` limits only the *collection* of interval
ordering fractions (the sampled `fis`, and therefore `mean_f_interval`,
`d_mm_interval`, `dimension_mismatch` and `self_similarity`, are unchanged). The schema
is bumped `qr05dl-report-v1 → qr05dl-report-v2`, `qr05dl-capture-v1 → qr05dl-capture-v2`.

| object | `ρ_int` v1 (wrong) | `ρ_int` v2 (corrected) | `1 − ℓ` check |
|---|---|---|---|
| sprinkle d=2 | 0.094 | **0.929** | ℓ ≈ 0.071 |
| sprinkle d=3 | 0.168 | **0.733** | ℓ ≈ 0.267 |
| sprinkle d=4 | 0.419 | 0.419 | cap not reached in v1 either |
| TP p=0.02 | 0.420 | **0.844** | ℓ ≈ 0.156 |
| TP p=0.05 | 0.081 | **0.955** | ℓ ≈ 0.045 |
| TP p=0.1 | 0.093 | **0.973** | ℓ ≈ 0.027 |
| bipartite | 0.000 | 0.000 | no intervals |
| layer-cake k=3 | 0.335 | 0.335 | cap not reached in v1 either |
| layer-cake k=4 | 0.503 | 0.503 | cap not reached in v1 either |

Rows whose interval sample never reached `cap` (sprinkle d=4, both layer-cakes, the
bipartite order) are unaffected — which is exactly the fingerprint of the defect.

## 3. What did *not* change

- `f_global`, `d_mm_global`, `mean_f_interval`, `d_mm_interval`, `dimension_mismatch`,
  `intervals_sampled` and **`self_similarity`** are **bit-identical** to v1.
- **All six flags are identical**, including `degenerate_counterexamples_fail_interval_self_similarity`
  (satisfied by the bipartite order's `ρ_int = 0` and the layer-cakes' zero sampled
  intervals), and the report `verdict` string is unchanged.
- The QR-05DL **conclusion** is unchanged: interval self-similarity separates sprinkles
  from the QR-05DK counterexamples, manifoldlikeness is multi-faceted, and no no-go is
  established.
- Only the **interpretation of the `interval_density` column** changes: sprinkles are
  interval-dense (`ρ_int ≈ 0.93, 0.73, 0.42`), not interval-sparse — i.e. most
  comparable pairs in a sprinkle are *not* links, which is the manifoldlike behaviour.

## 4. Provenance

- Superseded capture: `results.superseded-density-v1.json`, SHA-256
  `741204843b0882c2a020cf7eecde8c89f6f03811214c3597b23332e8556f1906` (schema
  `qr05dl-report-v1`; identical to the capture recorded in the QR-05DL commit `78a2166`,
  `results.json`).
- Corrected capture: `results.json`, schema `qr05dl-capture-v2` — current SHA-256 in
  [RESULTS.md](RESULTS.md).
- Regression test: `test_known_answer_interval_density_is_a_complete_sweep` pins
  `ρ_int = (n−2)/n` exactly for a chain of `n = 10` under a deliberately small
  `cap = 5` (which the v1 code would have failed: `0.4 < 0.8`).

Track-B exploratory (Status M); no physical, metric, continuum, curvature or gravity
claim.
