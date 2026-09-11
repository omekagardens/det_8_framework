# QR-05CE results

10 September 2026 (Pacific/Honolulu). **Executable result on real open data.**
The Bell-test dataset, routed to the commitment it instantiates, exhibits the
CHSH/Bell correlation and a strictly positive predictive-history distance. Two
independent routes agree; 7 tests pass.

## Dataset

`VBI_Coincidence_20230707.dat`, SHA-256
`a3e687354b71895096aee4e28d113d629e157953c7d240d33de3bd0aca653254`, 37(α)×32(β)
four-fold coincidence counts. Referenced from the CB gate by relative path and
hash-pinned.

## Correlation curves and the CHSH witness

Reproduced from the deposit's own reduction (`E(α,β)` for α=0 and α=π/2 over
β indices 0..27):

| Curve | E_min | E_max | amplitude | amplitude² | threshold 1/2 | over-threshold β points | κ |
|---|---|---|---|---|---|---|---|
| α=0 | −147/187 | 304/397 | 115207/148478 ≈ 0.7759 | 13272652849/22045716484 | > 1/2 ✓ | 7 | 0.565529595 |
| α=π/2 | −294/379 | 309/394 | 232947/298652 ≈ 0.7800 | 54264304809/89193017104 | > 1/2 ✓ | 6 | 0.569575102 |

Both amplitudes exceed `1/√2 ≈ 0.7071`, the exact visibility threshold for
CHSH violation (`amplitude² > 1/2`, tested rationally), and several individual
β points exceed it. So the dataset exhibits the **Bell/Tsirelson
correspondence** — the DET slot it belongs to — not a geometry signal.

## Predictive-history distance κ

Using `record_kernel_physics.md` §2.2, the two-outcome kernels at the extremal
settings of each curve give

```text
κ = (2/π)·arccos Σ_x √(K_a(x)K_b(x)),
```

with `K_β = ((1+E)/2, (1−E)/2)`. κ ≈ 0.566 (α=0) and ≈ 0.570 (α=π/2): the
setting-conditioned kernels are predictively distinguishable and strictly
between the identical-kernel (0) and disjoint-support (1) limits. This is the
DET-native object for such data — a measure of how the setting changes the
future/outcome kernel — and it is not a geometric quantity.

## What this corrects and what it does not claim

It corrects CB's routing: the same data now exercises the Bell/Tsirelson
commitment and the history distance, with no fabricated geometric side. It is
**not** a derivation of Tsirelson's bound, not a DET-specific prediction, not
evidence of new physics, and not a step on the geometry→gravity path. κ here
is the Fisher–Rao predictive-history distance, distinct from the materials
coordinate κ of the applied-physics program. No metric, manifold, continuum
limit or dynamics is claimed, and no apparatus or calibration is involved.

## Verification and provenance

`primary.py` and `reference.py` build the grid and curves independently
(different slicing and enumeration; identical declared κ expression); the
driver compares complete encoded reports and refuses on any difference.
Tests re-check the dataset hash, grid, exact CHSH witness, κ positivity and
cross-route agreement.

- Capture: 1,160 bytes;
  SHA-256 `12c64c2941c10715473cdec20fab5a7a97cde451e1bec840a0731d00de7d8b76`.
- Freeze: SHA-256
  `3469eac275662d7d8071583c556efb599c7d58a872d0f0a5c947d338b7677866`.

CE continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
