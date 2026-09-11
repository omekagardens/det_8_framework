# QR-05CN results

10 September 2026 (Pacific/Honolulu). **T7/T5 compatibility bridge: design
complete; bounded witness passes.** From one sprinkle the T7-reconstructed
conformal profile and a T5 kernel built as a count-based functional of the same
points agree (correlation 0.973), while an independently supplied kernel with a
different profile is uncorrelated (0.009). This witnesses the *derived-kernel*
requirement (C1–C3); it is not a full unification. 7 tests pass. Supplied
geometry; no gravity claim.

## The design

The bridge requires the T5 local kernel `K` to be a **functional of the same**
`(V, ≺, #, L)` that T7 uses, not an independently supplied input, under six
compatibility conditions (C1 one event set, C2 derived kernel, C3 geometric
consistency, C4 one shared scale, C5 scale consistency, C6 no double counting);
see [README.md](README.md).

## The witness

One sprinkle, `Ω²(x) = 1 + a sin(2πx)`, N=4000, 12 bins:

| Route | object |
|---|---|
| T7 | conformal profile `P₇` from binned counts |
| T5 | kernel profile `d₅` from a count-based (KDE) functional of the *same* points |
| control | an independently supplied `1 + a cos(2πx)` profile |

| Correlation | Value | Threshold |
|---|---|---|
| T7 vs derived T5 kernel | **0.973189** | ≥ 0.9 |
| T7 vs independent kernel | **0.008573** | ≤ 0.5 |

`compatible = true`. So a kernel *derived from the record structure* is
compatible with the T7 geometry (they share one model), whereas an
*independently supplied* kernel is juxtaposed — the charter's §7.2 failure mode,
exhibited as a control.

## What this establishes and what remains

Establishes the operational core of C1–C3 on supplied geometry: T7 and T5 can be
read off one `(≺, #)` structure with the kernel derived from it. Remains open:
the full composed-model construction, **C5 scale consistency** (coarse-graining),
C4's single-shared-scale statement at higher order, and the empirical bridge. No
gravity, curvature or dynamics is claimed; no new source or coupling is
introduced.

## Verification and provenance

`primary.py` and `reference.py` implement the sprinkle, the two profiles, the
control and the correlation independently; the driver compares with a float
tolerance and refuses on any difference.

- Capture: 952 bytes;
  SHA-256 `0125053070a70be75b45358c1a3b74c603ced4f208b473f77ffb4ab3bf6cf161`.
- Freeze: SHA-256
  `65c93c48d13eb8f8c11d233798f2e1a4d55eaaf71ffc6ecda5f55bc4d2408bfa`.

CN continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
