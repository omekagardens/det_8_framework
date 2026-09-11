# QR-05CQ results

10 September 2026 (Pacific/Honolulu). **T7 adversarial non-manifoldlike control
complete — positive.** The ordering-fraction dimension estimator alone is fooled
by a non-manifoldlike order tuned to the same ordering fraction; a joint test
with the **link fraction** rejects it, while manifoldlike orders pass. 7 tests
pass. Supplied geometry; no gravity claim.

## The discriminator

Link fraction = share of comparable pairs with no intervening element.

| Case | r | link fraction | dim ok? | accepted? |
|---|---|---|---|---|
| manifoldlike d=2 | 0.5235 | 0.0538 | ✓ | **yes** |
| manifoldlike d=3 | 0.2287 | 0.2524 | ✓ | **yes** |
| manifoldlike d=4 | 0.0981 | 0.5462 | ✓ | **yes** |
| **bipartite (KR)** | 0.5017 | **1.0000** | ✓ (fooled) | **no** |
| chain | 1.0000 | 0.0067 | ✗ | **no** |
| antichain | 0.0000 | 0.0000 | ✗ | **no** |

The bipartite order — every "bottom" comparable to every "top", nothing in
between — has **r ≈ r(2) = 0.5**, so the ordering-fraction estimator reports
d=2, but **every** comparable pair is a link (link fraction 1), which no
manifoldlike order approaches (max 0.55 at d=4). The joint test rejects it. Chain
and antichain are rejected as outside the family range.

`discriminator.separates = true`: the manifoldlike link fractions lie below the
0.8 threshold, the bipartite link fraction (1.0) above it.

## What this establishes

Charter §7.4: a passing dimension summary is **not** sufficient for recovery —
a non-manifoldlike order can match `r(d)` and be rejected by the interval/link
structure. The T7 estimators, tested jointly, are not fooled by the adversarial
order.

## Boundaries

A bounded adversarial control on supplied geometry — **not** a manifoldlikeness
theorem, not curvature, and not gravity. The link fraction is a diagnostic, not
a proof that a passing order *is* a manifold; the emergence question stays open.
Curvature and the imported BD operator stay parked; κ-gravity is retired and
gravity is standard GR under Option B.

## Verification and provenance

`primary.py` and `reference.py` build the causality, the fractions and the
adversarial matrices independently; the driver compares with a float tolerance
and refuses on any difference.

- Capture: 1,498 bytes;
  SHA-256 `44ca44437672ac975b7519540e331bd603af753d31dbcfe683aea9be2195a66e`.
- Freeze: SHA-256
  `cb7b2bee32ca25975f4a6eede11fc6be968211a8bfe6369234ea72de4ed96752`.

CQ continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
