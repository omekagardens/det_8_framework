# QR-05CQ: T7 adversarial non-manifoldlike control

10 September 2026 (Pacific/Honolulu). **Executable, supplied geometry, bounded.**
Charter §7.4: the geometric estimators must not confuse recovery with emergence.
This shows that the ordering-fraction dimension estimator **alone** is fooled by
a non-manifoldlike order tuned to the same ordering fraction, while a **joint
test** with the link fraction rejects it. Supplied geometry; no gravity claim.

Continue [QR-05CF](../qr-05cf-t7-supplied-geometry-2026-09-10/README.md) (the
positive estimator benchmark).

## 1. The discriminator

The T7 dimension estimator uses the **ordering fraction** `r` = (comparable
pairs)/C(N,2) compared to the Myrheim–Meyer `r(d)`. A non-manifoldlike order can
match `r(d)` while having a completely different interval structure. The
discriminator is the **link fraction**: the share of comparable pairs that have
no intervening element (`|I(x,y)| = 0`).

- Manifoldlike orders: links are a **small** share (near-null neighbourhood);
- A **bipartite (Kleitman–Rothschild) order** — every "bottom" element comparable
  to every "top" element, nothing in between — has **every** comparable pair a
  link, so its link fraction is `1`.

## 2. What is verified

| Case | Construction | Expectation |
|---|---|---|
| Manifoldlike | diamond sprinkle, d=2,3,4, N=300 | `r` within 0.06 of `r(d)` **and** link fraction ≤ 0.8 → accepted |
| Bipartite | 150 bottom × 150 top, all comparable | `r ≈ r(2)` (fools the dimension estimator) but link fraction = 1 → **rejected** |
| Chain | total order | `r = 1` (outside the family) → rejected |
| Antichain | no comparabilities | `r = 0` (outside the family) → rejected |

Acceptance requires **both** `r` in the family range and a manifoldlike link
fraction, so the adversarial order that matches `r(2)` is rejected by the link
evidence.

## 3. Result

All manifoldlike orders pass; the bipartite order fools the dimension estimator
but is rejected by the link fraction; chain and antichain are rejected as
outside the family. Numbers in [RESULTS.md](RESULTS.md). This is the charter
§7.4 control: recovery is not certified by a summary that a non-manifoldlike
order can also match.

## 4. Boundaries

A bounded adversarial control on supplied geometry — not a manifoldlikeness
theorem, not curvature, and not gravity. The discriminator is a diagnostic, not
a proof that a passing order *is* a manifold (the emergence question stays
open). Curvature and the imported BD operator stay parked; κ-gravity is retired
and gravity is standard GR under Option B.

## 5. Evidence and limits

`primary.py` and `reference.py` build the causality, the fractions and the
adversarial matrices independently; the driver compares with a float tolerance
and refuses on any difference. `study.py` writes create-only `results.json` and
`source-freeze.json` (freezing the gate sources and the T7 module by hash);
`test_qr05cq.py` checks the manifoldlike acceptance, the bipartite fooling and
rejection, the chain/antichain rejections, the discriminator separation and
route agreement. Fixed inputs make the run deterministic. Limits: sources
≤262,144 bytes, artifacts ≤16,777,216 bytes. Decision record:
[RESULTS.md](RESULTS.md).
