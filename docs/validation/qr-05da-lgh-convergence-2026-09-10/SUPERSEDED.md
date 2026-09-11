# QR-05DA supersession record

10 September 2026 (Pacific/Honolulu). **The first DA capture is superseded.** Its
`p99` series is invalid: the function named `_p99` selected the **1st** percentile,
not the 99th, so every statistic labelled "bulk (p99)" in the first README/RESULTS
was a *lower-tail* statistic while being reported and interpreted as a bulk/upper
statistic.

## The defect

Both routes implemented

```python
def _p99(values):
    ordered = sorted(values)
    return ordered[min(int(0.01 * len(ordered)), len(ordered) - 1)]   # 1st percentile
```

`int(0.01 n)` is the index of the 1st percentile. Indexing for the 99th percentile
is `ceil(0.99 n) - 1` (nearest rank). Because *both* routes carried the same
misindexing, the cross-route agreement check in `study.py` could not detect it —
the two implementations agreed on the same conceptual error. That is exactly the
failure mode the known-answer tests in `test_qr05da.py` now block.

## Effect on the claims

- The reported `chain p99` at `N = 512` was `0.0017`; the true 99th percentile is
  `≈ 0.35`.
- The reported `count p99` at `N = 512` was `0.0010`; the true 99th percentile is
  `≈ 0.19`.
- The headline "count `p99` is below `10⁻²` for `N ≥ 32`" is **false** and is
  withdrawn.
- The log–log *decay exponents* were nearly unchanged (both tails of a roughly
  self-similar distortion distribution decay at similar rates: chain `≈ 0.30`,
  count `≈ 0.41`), so the qualitative estimator split survives — but the
  magnitudes, and therefore the "essentially exact" reading, do not.

## The repair

- `_p99` is now the nearest-rank 99th percentile; a `_median` (nearest-rank 50th
  percentile) is reported alongside it, so each reconstruction has a clearly
  separated **typical / upper-tail / ceiling** triple. "p99 is the bulk" is not
  asserted; the median is the bulk statistic.
- `count_separation` (`ℓ·√(1+m_ij)`) is a named function and is tested against the
  Lorentzian reverse-triangle inequality: on a three-event chain `a ≺ b ≺ c` it
  gives `d(a,c) = ℓ√2 < d(a,b) + d(b,c) = 2ℓ`, so it is a **distance estimator**,
  not a Lorentzian metric.
- Known-answer tests pin the percentile and decay-fit semantics with hand-computed
  values, independent of either route's implementation.

## Preserved evidence

- Superseded capture: [`results.superseded-p01-v1.json`](results.superseded-p01-v1.json),
  schema `qr05da-capture-v1`, SHA-256
  `d7a9b4c58c34c9b139aa11f230d8e556107b8914b73a59951dca8c5c0da5a8fe`
  (unchanged bytes of the first capture).
- Corrected capture: [`results.json`](results.json), schema `qr05da-capture-v2`
  (records `"supersedes": ["results.superseded-p01-v1.json"]`).

No metric, continuum, curvature, dynamics or gravity claim is made by either
capture.
