# QR-05CO results

10 September 2026 (Pacific/Honolulu). **T7/T5 scale-consistency witness (C5)
complete — positive.** Grouping records at two scales gives a consistent
reconstructed geometry and a consistent T5 operator, and the bridge holds at
both scales; the raw (extensive) count is not scale-consistent, so the
reconstruction must be intensive. 8 tests pass. Supplied geometry; no gravity
claim.

## Checks (one sprinkle, Ω²=1+a sin(2πx), N=8000)

| Check | Value | Verdict |
|---|---|---|
| Coarse-graining identity (fine aggregated == coarse) | exact | ✓ |
| Geometry scale-consistency (normalized fine vs coarse) | dev 0.0 | ✓ |
| Operator scale-consistency (KDE at w vs 2w) | corr 0.978226, scale ratio 1.0 | ✓ |
| Bridge at both scales: coarse / fine | 0.953062 / 0.994955 | ✓ |

The operator's pointwise deviation is 0.211 — that is finite-bandwidth
resolution, not a scale error: both profiles are normalized (mean 1, scale
ratio 1.0) and correlate at 0.978.

## The control

The un-normalized count is scale-dependent: its mean magnitude doubles from the
fine binning to the coarse (`raw_scale_ratio = 2.0`), so `raw_scale_consistent
= false`, while the normalized profile has ratio `1.0`. So C5 forces the
reconstruction to be **intensive** — a density, not a count — which is exactly
what T7's conformal factor and T5's kernel-moment coefficients are.

## What this establishes and what remains

Establishes C5 (charter §7.3) on supplied geometry: the CN bridge survives
coarse-graining, for both the geometry and the derived operator, with a single
shared normalization. Remains open: the full composed-model construction, the
empirical bridge, and any gravitational dynamics. No gravity, curvature or new
source is introduced.

## Verification and provenance

`primary.py` and `reference.py` implement the two scales, the profiles, the
bridge correlations and the control independently; the driver compares with a
float tolerance and refuses on any difference.

- Capture: 634 bytes;
  SHA-256 `232b159c1fb6123e73f1259efff22275c73dd2eda24a9d7646429a498aa6bebf`.
- Freeze: SHA-256
  `7124055ffc42baa98a5a399cd50569b21f15207ed262f9b3fe6b4e171045d5cb`.

CO continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
