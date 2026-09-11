# QR-05CE: Bell correspondence and history distance (correct Bell-data gate)

10 September 2026 (Pacific/Honolulu). **Executable, real open data, correct
routing.** This gate applies the Bell-test dataset to the DET commitment it
actually instantiates — the **Bell/Tsirelson correspondence** and the
**predictive-history distance κ** — rather than to the T7 geometry program.
It is not a geometry test and makes no metric or gravity claim.

Continue [QR-05CD](../qr-05cd-det-data-routing-2026-09-10/README.md) (routing)
and the [QR-05CB amendment](../qr-05cb-open-data-applicability-2026-09-10/ONTOLOGY_AMENDMENT.md).

## 1. Routing

Per `docs/record_kernel_physics.md` §5 and `PHYSICS.md` §5, "Bell/Tsirelson" is
a **correspondence target**, distinct from "causal geometry from order and
count" (T7). The Bell dataset supplies setting-conditioned outcome statistics,
so it belongs here. The geometry side (supplied marks) is absent and is not
fabricated.

## 2. What is computed

The dataset's own reduction is reproduced faithfully: CC4 reshaped to the
37(α)×32(β) grid, and correlation curves

```text
E(α,β_i) = [N(α,β_i) + N(α+π,β_{i+4}) − N(α,β_{i+4}) − N(α+π,β_i)] / Σ
```

for α = 0 and α = π/2 over i = 0..27. Then, exactly:

- **Visibility / CHSH witness.** The amplitude `A=(max−min)/2`. For a
  sinusoidal correlation, `|S|max = 2√2·A`, and `A > 1/√2` (⇔ `A²>1/2`) is the
  exact visibility threshold for CHSH violation. The witness test is rational.
- **History distance κ.** `record_kernel_physics.md` §2.2:
  `κ = (2/π)·arccos Σ_x √(K_a(x)K_b(x))` between the two-outcome kernels
  `K_β = ((1+E)/2, (1−E)/2)` at the extremal settings of each curve. κ is
  transcendental and is reported to 9 decimals; its inputs are exact.

## 3. Result

Both curves show amplitude ≈ 0.78, above the `1/√2 ≈ 0.7071` threshold, so the
dataset exhibits the CHSH/Bell correlation — the correspondence DET reserves a
slot for. The extremal-setting history distance is strictly positive
(κ ≈ 0.5–0.6), i.e. the setting-conditioned kernels are predictively
distinguishable, exactly the object κ is defined to measure. Exact values are
in [RESULTS.md](RESULTS.md).

## 4. Boundaries

This is a correspondence check on public data, not a derivation of
Tsirelson's bound, not a DET-specific prediction, and not evidence of new
physics. It does not touch the geometry→gravity path. No metric, manifold,
continuum limit or dynamics is claimed, and no apparatus or calibration is
involved. kappa here is the Fisher–Rao predictive-history distance, distinct
from the materials coordinate κ of the applied-physics program.

## 5. Evidence and limits

`primary.py` and `reference.py` independently build the grid and curves
(different slicing/enumeration; identical declared κ expression) and must
agree. `study.py` writes create-only `results.json` and `source-freeze.json`;
tests in `test_qr05ce.py` re-check the dataset hash, the grid, the exact CHSH
witness, κ positivity and route agreement. The dataset is referenced from the
CB gate by relative path and hash-pinned. Limits: sources ≤262,144 bytes,
artifacts ≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
