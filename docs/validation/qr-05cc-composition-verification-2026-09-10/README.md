# QR-05CC: reference-calibration composition verification

10 September 2026 (Pacific/Honolulu). **Executable, symbolic, bounded.**
This closes BW's deferred gate by verifying the composition algebra and the
auditable interface that BW specified. It uses exact rational arithmetic over
declared fixtures, acquires no data, and makes no physical claim.

Continue the [BW contract](../qr-05bw-reference-calibration-design-2026-09-10/README.md)
(the deferred successor it names) and the [routing note](../qr-05cd-det-data-routing-2026-09-10/README.md).

## 1. What is verified

| Item | Statement checked | Fixtures |
|---|---|---|
| Proposition 1 (triangle composition) | `‖r−q‖∞ ≤ a+d` whenever `a ≥ ‖r_ref−q‖∞` and `d ≥ ‖r−r_ref‖∞`, with a tight witness | N1–N3 |
| Corollary 1 (close fit insufficient) | `d=0 ⇒ e_cal=a`; `e = nrr + nrq` at tightness | N4 |
| Corollary 2 (allocation split) | `e_cal = a_sys+a_stat+d_sys+d_stat` | S1, S2 |
| Proposition 2 (union bound, no independence) | `P(Gᶜ) ≤ β_ref+β_tr` and `P(E∩G) ≥ 1−α−β` on finite spaces | P1, P2 |
| Product is not implied | a coupling with `P(E∩G) < (1−α)(1−β)` | P2 |
| Selection regime R2 | `max(0, P(H)−α−β)` and `1−(α+β)/P(H)`, undefined at `P(H)=0` | R2a–R2d |
| Repetition R3 | `K` repeats give budget `Kβ` | R3a, R3b |
| Auditable interface | any unmet load-bearing premise forces `conditional_only = true` | complete, unmet |

All probabilities are computed by enumerating a declared finite sample space
with rational weights; no independence is assumed and the product is actively
refuted by P2. The separation envelope and every-window certificate are the
same identity as BW's and are not re-derived here.

## 2. Result

Every fixture matches its declared expectation; `primary.py` and `reference.py`
compute the whole report by different routes (coordinate `max` vs explicit
comparisons; set-intersection weighting vs indicator sums) and agree exactly.
The decisive checks are that the union bound holds on both spaces while the
independence product fails on P2, and that `conditional_only` tracks unmet
premises. Exact values are in [RESULTS.md](RESULTS.md).

## 3. Boundaries

This is a symbolic audit of the composition algebra and the interface flag. It
is not apparatus calibration, not a numerical `β`/allowance, not a fixture
sweep, and it makes no metric, continuum or gravity claim. Every result stays
conditional on BW's premises P1–P12, which remain unmet. It does not touch the
geometry→gravity path's remaining needs (a supplied geometry or apparatus).

## 4. Evidence and limits

`study.py` writes create-only `results.json` and `source-freeze.json`; tests
in `test_qr05cc.py` re-check every norm, split, space, regime, repeat and
schema fixture plus route agreement. Limits: sources ≤262,144 bytes,
artifacts ≤16,777,216 bytes. Decision record: [RESULTS.md](RESULTS.md).
