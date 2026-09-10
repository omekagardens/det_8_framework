# QR-05CA results

10 September 2026 (Pacific/Honolulu). **Bounded synthetic rehearsal complete.**
The first frozen capture passed with no revision after freezing. Both
independent routes agree on the complete native report and all 11 tests
pass. The rehearsal is explicitly non-physical: its datasets are declared
tables, not measurements, and nothing here is evidence about nature.

The [prospective contract](README.md), [fixed protocol](protocol.json),
[source freeze](source-freeze.json) and [complete capture](results.json)
retain the evidence.

## What the rehearsal produced

| Section | Fixtures | Outcome |
|---|---|---|
| Datasets | `D1`, `D2` | both accepted; exact `K₁,K₂,n_eff,r̂` |
| Refusals | 6 static + 1 sealed-mutation | all seven reasons fire |
| Inverses | `INV0`–`INV4` | exact discrete target sets |
| Allowances | `A1`, `A2` | `e_cal=9/64`, `β=3/100`; envelope passes/fails |
| Feasibility | `F1`–`F4` | `100, 16` certified; `4, 4/9` not |
| BY registry | `pass_all`, `fail_dim`, `fail_limit` | pass/pass, refute/pass, pass/refute |

Reduction: `D1` (no loss) → `K₁=2, K₂=3, n_eff=8, r̂=(1/4,3/8)`; `D2` (one
loss) → `K₁=1, K₂=2, n_eff=7, r̂=(1/7,2/7)`, loss fraction `1/8` under the
`1/4` bound. With `B={0}`, `D1` at `e=0` gives `T={1/4}` and `D2` at `e=1/4`
gives `T={1/4,17/80}`.

## What the fixtures distinguish

- **Refusal closure.** The seven refusal reasons are each triggered by a
  purpose-built fixture: forbidden `10` (support), loss beyond bound,
  first/second-half frequency drift, mark mismatch, analysis-id mismatch,
  fewer than four usable attempts, and a SHA-256 seal mismatch (verified by
  sealing a valid dataset, mutating one attempt, and observing the refusal).
- **Envelope.** `A1` has `e_cal=9/64 ≤ e_max=3/16`; `A2` has the same
  `e_cal` but `e_max=1/8`, so it is flagged outside the envelope. Both keep
  `β=3/100`; the envelope is a separate condition from the budget.
- **Ambiguity is real.** `INV2` at `e=3/128` over `B={0}` admits both
  `17/80` and `1/4`, the synthetic instance of BW's bound-only collision:
  when the allowance reaches half the separation, both ideal targets remain
  admissible on the same population.
- **Feasibility matches BV.** `F1` and `F2` reproduce the certified
  uniform rows (`s=5/128, score 100`; `s=1/64, score 16`); `F3` (contact,
  `s=−1/128`) and `F4` (half/quarter, `s=1/384, score 4/9`) are not
  certified, matching the BV rows. A positive `s` with a failing score, and
  a negative `s`, are kept distinct.
- **BY registry.** `fail_dim` refutes the metric claim while the dynamics
  claim passes; `fail_limit` refutes the dynamics claim while the metric
  claim passes. The registry reports each predicate, not only a summary.

## Independence and evidence integrity

The primary route reduces with a direct scan and evaluates ideal points by
polynomial masses. The reference route reduces with a `Counter`, evaluates
ideal points by the BU segment-parameter formulas, nests the inverse loops
in the opposite order, and writes the feasibility and BY predicates
differently. The driver compares the complete encoded reports and refuses
on any difference; the suite also re-derives both reports and asserts
equality.

| Check | Outcome |
|---|---|
| Normal suite | 11/11 passed |
| Primary vs reference native report | Exact agreement |
| Capture matches `analyze()` | Exact |
| Frozen-source byte limit (262,144) | Passed |

During drafting, before the first freeze, a hand-computed ideal point for
`INV1`/`INV3` was corrected against the declared model (`q(1,0)=(17/80,21/64)`
and `q(0,1/2)=(11/48,67/192)`); the dataset expected values were fixed then
and were not changed after the freeze. No randomness, floats or
non-standard-library imports are used.

- First freeze: 853 bytes;
  SHA-256 `c43a864cf1a177fb6b431c61f809a064c0d8792973aa4317230a8e5d09dea888`.
- First capture: 8,761 bytes;
  SHA-256 `d4c195d863e6d860b792e84ec525faa40e5380a066cf004858f20ad00fbe6fda`.

## Value, boundaries and next gate

The useful result is a checkable demonstration that the BZ pipeline closes:
schema and seal admission, deterministic reduction, every refusal condition,
the BW allowance composition, the enlarged inverse and the BY test registry
all run end-to-end and agree across two independent routes. It removes the
"does the protocol even wire together" question from the later measured
work.

It does not supply data, a device, a calibration, a metric or a dynamics.
The datasets are declared tables, so a passing rehearsal is consistency of
the pipeline, not a measurement. The earlier gates remain conditional on
BW/BX, and the measured metric/dynamics assessment still requires a real
apparatus and reference.

The next step is a real measured run once an apparatus and reference exist,
assessed with the BZ protocol and the BY tests. No apparatus, device,
fabricated physical claim, numerical `β` or gravity result is produced or
implied.

## Provenance and publication

CA continues the committed `qr-05-bridge` branch, which began from pushed
BV commit `8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`; BW/BX, BY
and BZ are the branch's prior commits. No BV or BU source, freeze or
capture was modified or re-executed, and the BV first capture remains
100,522 bytes, SHA-256
`44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`.

Publication is this results directory (README, protocol, primary,
reference, study, tests, freeze, capture) and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
application work and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
