# QR-05DJ (direction A, DET-native): a record-κ law map

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — no physical claim.** T8 currently **assumes** records do not affect order
growth. This gate tests the opposite — **record-dependent order feedback** — and finds a
**tension**: record-driven growth is still **not manifoldlike** (the link mismatch
persists), and making the order depend on the record makes the **record leak into the
order** (breaking the covariance T8 assumes). O7's emergence is not achieved.

## 1. Pre-specification

- **Question.** Does a DET-native **record-driven law map** grow a manifoldlike order
  (O7), or does record feedback trade manifoldlikeness for record-legibility (T8)?
- **Law map (DET-native).** Each element carries a record coordinate `κ ∈ [0,1]`; the
  relation probability is κ-dependent, `p_ij = p0·φ(κ_i, κ_j)`, with
  `φ ∈ { blind: 1 , sum: (κ_i+κ_j)/2 , similar: 1−|κ_i−κ_j| }`, then the order is
  transitively closed. (`blind` is the κ-independent control = transitive percolation.)
  This is **record-dependent order feedback** — the direction T8 assumes away.
- **Tests.**
  - **Manifoldlikeness (O7):** at a matched 2-point ordering fraction, the link fraction
    vs the sprinkle's (the QR-05DI discriminator).
  - **Record-legibility (T8 / covariance):** the correlation between `κ` and an
    order-derived statistic (the element's comparability degree) — does the order encode
    the record?
- **Objects.** sprinkles `d = 2, 3` (`n = 150`) as the reference; three κ-modes swept over
  `p0`; chain and antichain controls.

## 2. Results

**Reference (sprinkles).** `d = 2`: `f = 0.477`, `d_MM = 2.06`, link fraction `0.102`;
`d = 3`: `f = 0.263`, `d_MM = 2.83`, link `0.317`.

**Matched at the ordering fraction** (2-point `d_MM` matches by construction):

| mode | dim | `ℓ` sprinkle | `ℓ` law | ratio | κ–degree corr. (leakage) |
|---|---|---|---|---|---|
| blind (TP) | 2 | 0.102 | 0.072 | 0.70 | −0.04 |
| blind (TP) | 3 | 0.317 | 0.134 | 0.42 | −0.04 |
| **sum** | 2 | 0.102 | 0.066 | 0.65 | **+0.34** |
| **sum** | 3 | 0.317 | 0.121 | 0.38 | **+0.28** |
| similar | 2 | 0.102 | 0.073 | 0.71 | −0.02 |
| similar | 3 | 0.317 | 0.122 | 0.38 | −0.04 |

- **Record-driven growth does not close the link mismatch** — the link fraction is only
  `0.38–0.71` of the sprinkle's, in every mode.
- **The record leaks into the order** — the `sum` coupling gives a `κ`–degree correlation
  of `0.28–0.34`, so the order *encodes* the record; the κ-blind control does not
  (`≈ 0`).

## 3. Findings

1. **Not manifoldlike:** the DET-native record-driven law matches the 2-point dimension
   but mismatches the link structure just like the κ-blind law.
2. **Record-legibility:** κ-dependence leaks the record into the order (κ–degree
   correlation up to 0.34) — a **covariance cost** (T8's assumption is, in effect,
   protecting manifoldlikeness).
3. **The tension (the point):** the more the order depends on the record (DET-native,
   T7↔T8 coupling), the less it looks like a manifold (O7). Record feedback and
   manifoldlike emergence pull against each other in this law family.
4. **O7 not achieved** without inserting geometry.

## 4. Boundaries

`TP`, the Myrheim–Meyer estimator, and the link/leakage statistics are **borrowed**; the
gate is a bounded, calibrated **discrimination test**, not a theorem, and novelty is
**low–moderate**. It carries no physical, metric, continuum, curvature, dynamics or
gravity claim; correspondence-level / Status M. "Record-legibility" here is a proxy
(κ–degree correlation), not a full covariance proof; and the κ-modes are a small, chosen
family, not all record-driven laws.

## 5. Evidence

`primary.py` (interval causality; record-κ percolation; link/interval + leakage statistics)
and `reference.py` (light-cone-dominance causality; percolation recoded; statistics
recoded) compute the reference, the mode curves, the matched comparison and the flags
independently — the RNG streams are shared by construction (documented). The driver
refuses on any difference. `test_qr05dj.py` (10 tests) pins the leakage known-answer
(a star gives 1; a symmetric chain gives 0), the controls, and the flags. `study.py`
writes create-only `results.json` and `source-freeze.json`. Decision record:
[RESULTS.md](RESULTS.md).
