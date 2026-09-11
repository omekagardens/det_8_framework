# QR-05CC results

10 September 2026 (Pacific/Honolulu). **Composition verification complete.**
BW's deferred gate is closed: the composition algebra, the finite-space union
bound, the selection regimes and the auditable-interface flag all verify
exactly, by two independent routes, with 10 tests passing. No data, device or
physical claim is involved.

## What verified

| Item | Fixtures | Outcome |
|---|---|---|
| Proposition 1 (triangle composition) | N1–N3 | bound holds; N1 is a tight witness (`e = a+d`) |
| Corollary 1 (close fit insufficient) | N4 | `d=0 ⇒ e_cal=a`, tight |
| Corollary 2 (allocation split) | S1, S2 | `e_cal = 9/64`, `= 3/200` |
| Proposition 2 (union bound) | P1, P2 | `P(Gᶜ) ≤ β` and `P(E∩G) ≥ 1−α−β` hold on both |
| Product not implied | P2 | `P(E∩G)=0 < (1−α)(1−β)=1/4` |
| Selection regime R2 | R2a–R2d | `P(H)=1/2→0`; `1/4→ cond 3/5`; `P(H)=0` undefined; `P(H)=1→1` |
| Repetition R3 | R3a, R3b | `5·(1/20)=1/4`; `1·(1/20)=1/20` |
| Auditable interface | complete, unmet | `conditional_only` false / true |

The two independent routes — coordinate `max` versus explicit comparisons, and
set-intersection weighting versus indicator sums — agree on the complete
encoded report. The union bound rests on event enumeration, not on a symbolic
argument, so P2's product refutation is a checked counterexample rather than an
assertion.

## What it closes and what it does not

This was the last open item on the geometry-path ledger (BW's explicitly
deferred successor). It does **not** supply a numerical `β`, an allowance,
calibration or a fixture sweep, and it changes no data. Every result stays
conditional on BW's premises P1–P12, which remain unmet. The geometry path
still needs a supplied Lorentzian geometry/sprinkling (T7) or a purpose-built
geometric-probe apparatus; no metric, continuum limit or dynamics follows.

## Verification and provenance

- Capture: 3,625 bytes;
  SHA-256 `5d5c935090e3edc689b5e2734098e19b6689eebd38a58e97b2b65f9b101acfdb`.
- Freeze: SHA-256
  `be5239cd26ec254c7850a3cdde4c6ac543d1efca03d691cb883e88e53e4715d9`.

CC continues the committed `qr-05-bridge` branch (from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`). Publication is this
directory and the [Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md);
the 231 pre-existing dirty entries remain outside it.
