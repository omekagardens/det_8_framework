# QR-05DI (direction A): a native growth law and manifoldlike emergence

11 September 2026 (Pacific/Honolulu). **Executable, bounded. Track-B exploratory
(Status M) — no physical claim.** The O7 criterion: can a geometry-free **law map `L`**
grow a **manifoldlike** order — stable Myrheim–Meyer dimension plus a manifoldlikeness
test — **without inserting Minkowski**? Tested on the simplest native law, **transitive
percolation**: it matches the **2-point** dimension but **not the link structure**, so it
is **not manifoldlike** and the 2-point test is **insufficient**. O7's emergence is not
achieved; its obstruction is now a concrete higher-order statistic.

## 1. Pre-specification

- **Question (O7).** Can a geometry-free native growth law grow a manifoldlike order?
- **Growth law (no geometry inserted).** Transitive percolation `TP(n, p)`: elements in
  birth order `0…n−1`; each pair `i < j` related with probability `p` independently; take
  the transitive closure. A definite "law map `L`" that never references a manifold
  (borrowed: Rideout–Sorkin / Dowker–Sorkin).
- **Manifoldlikeness tests (geometry-free).**
  - **2-point:** the Myrheim–Meyer dimension `d_MM` from the ordering fraction `f`, with
    `f_d = Γ(d+1) Γ(d/2) / (2 Γ(3d/2))` (`f_1 = 1`, `f_2 = ½`, `f_3 ≈ 0.229`). Calibrated:
    sprinkles must return `d_MM ≈ d`.
  - **3-point / link:** the **link fraction** `ℓ` (Hasse edges / comparable pairs) and the
    mean interval fraction — statistics a sprinkle fixes but a 2-point match need not.
- **Objects.** sprinkles `d = 2, 3, 4`, `n = 150` (positive control); `TP(n, p)` swept over
  `p`; chain and antichain (controls).

## 2. Results

**Calibration (the estimator works).** Sprinkles return `d_MM ≈ d`, and a distinct link
fraction per dimension:

| sprinkle | f | d_MM | link fraction ℓ |
|---|---|---|---|
| d = 2 | 0.477 | 2.06 | 0.102 |
| d = 3 | 0.263 | 2.83 | 0.317 |
| d = 4 | 0.082 | 4.23 | 0.676 |

**The growth law spans dimensions.** `TP`'s ordering fraction runs from `f ≈ 0.006` at
`p = 0.005` (`d_MM ≈ 7.25`) down to `f ≈ 0.98` at `p = 0.5` (`d_MM ≈ 1.03`); its link
fraction runs `0.775 → 0.021`. So `p` tunes an effective dimension — but the link fraction
**decreases** with `p`, whereas for sprinkles `ℓ` **increases** with `d`: the two families
trend oppositely.

**Matched at the ordering fraction (the decisive test).** Interpolating `TP` to each
sprinkle's `f` (so the 2-point `d_MM` matches by construction), the **link fraction does
not match**:

| dim | `ℓ` sprinkle | `ℓ` TP (matched) | ratio | mismatch |
|---|---|---|---|---|
| 2 | 0.102 | 0.078 | 0.76 | yes |
| 3 | 0.317 | 0.138 | 0.44 | yes |
| 4 | 0.676 | 0.269 | 0.40 | yes |

So `TP` can mimic the **2-point** Myrheim–Meyer dimension of a sprinkle, but its
**link/interference structure is only 40–76%** of the sprinkle's — it is a different kind
of order (chain-like, closure-dense). **The 2-point MM test is insufficient for
manifoldlikeness.**

## 3. Findings

1. **The MM estimator is calibrated** (`d_MM ≈ 2, 3, 4` on sprinkles) — a geometry-free
   dimension estimator that works.
2. **The native law matches the 2-point dimension** at a tuned small `p`.
3. **But it mismatches the link structure** (40–76% of the sprinkle's at matched order) —
   the simplest geometry-free growth law is **not manifoldlike**.
4. **The 2-point MM test is insufficient**; a genuine manifoldlikeness test needs
   higher-order (link/interval) statistics.
5. **O7's emergence is not achieved** without inserting geometry; the obstruction is now a
   concrete, checkable higher-order statistic that a genuine native law must also match.

## 4. Boundaries

`TP`, the Myrheim–Meyer estimator, and the link/interval statistics are **borrowed**
(Rideout–Sorkin; Myrheim–Meyer; and manifoldlikeness tests à la Bombelli–Henson–Sorkin).
The gate is a bounded, calibrated **discrimination test**, not a theorem: the `n = 150`
finite-size calibration for `d = 3` is ~0.17 low, and transitive percolation's
manifoldlikeness is a known-hard question, so the novelty is **low–moderate**. It carries
no physical, metric, continuum, curvature, dynamics or gravity claim, and remains
correspondence-level / Status M. The next step for A is a **DET-native law map** (T8's
record-dependent growth) tested against the same link/interval discriminator.

## 5. Evidence

`primary.py` (interval causality; transitive percolation; bisection on the `f_d` curve;
link/interval statistics) and `reference.py` (light-cone-dominance causality; percolation
recoded; bracketing on `f_d`; statistics recoded) compute the calibration, the `TP` sweep,
the matched link comparison and the flags independently — the `TP` RNG stream is shared by
construction (documented). The driver refuses on any difference. `test_qr05di.py`
(10 tests) pins the `f_d` curve (`f_1 = 1`, `f_2 = ½`), the chain/antichain controls, and
the flags. `study.py` writes create-only `results.json` and `source-freeze.json`. Decision
record: [RESULTS.md](RESULTS.md).
