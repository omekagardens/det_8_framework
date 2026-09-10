# QR-05CA: bounded synthetic pipeline rehearsal

10 September 2026 (Pacific/Honolulu). **Executable, explicitly non-physical.**
This gate rehearses the BZ physical protocol end-to-end on declared synthetic
data, to verify that the reduction, the refusal conditions, the BW allowance
composition, the enlarged inverse and the BY test registry close as
specified. It uses exact rational arithmetic and no randomness, acquires no
physical data, and asserts no metric or dynamics.

Continue the [BZ protocol](../qr-05bz-physical-protocol-design-2026-09-10/README.md),
the [BY preregistration](../qr-05by-metric-dynamics-design-2026-09-10/README.md),
the [BX interface](../qr-05bx-apparatus-event-interface-design-2026-09-10/README.md)
and the [BW contract](../qr-05bw-reference-calibration-design-2026-09-10/README.md)
without changing their frozen evidence.

## 1. Purpose and boundary

BZ fixed a protocol and a measured-data contract but supplied no data. CA
supplies *declared-model* data — small attempt lists with exact,
hand-computed expected outcomes — and runs the BZ pipeline over them. The
purpose is to show that the pipeline is internally consistent and that every
refusal condition fires; it is **not** a measurement, a calibration, or
evidence about any physical system.

The gate does not:

- sample, simulate or fabricate a physical measurement;
- use randomness or floating point;
- validate a device, a reference or an allowance;
- claim a metric, a continuum limit or any dynamics.

"Synthetic" here means a finite declared table of attempts, not a draw from a
physical process. The word is load-bearing: nothing below is evidence about
nature.

## 2. What the rehearsal exercises

| Stage | Source | Object |
|---|---|---|
| Schema, integrity seal, analysis-id token | BZ Section 4 | dataset admission |
| Reduction to `K₁≤K₂`, `n_eff`, `r̂` | BZ Section 5 | counts and loss/stationarity handling |
| Refusal conditions | BZ Section 10 | integrity, analysis-id, mark, support, loss, insufficient, stationarity |
| Allowance composition `e_cal`, `β`, envelope | BW Sections 3–6 | `e_cal=a_sys+a_stat+d_sys+d_stat`, `β=β_ref+β_tr+β_env`, `e_cal≤e_max` |
| Enlarged inverse | BU/BZ | discrete target set over a finite density set |
| Feasibility certificate | BU/BT | `s=D−2e_max−2h`, `n s²≥10` |
| BY test registry | BY Sections 3–4 | metric and dynamics predicates, pass/refute |

The rehearsal substitutes the reduced population point `r̂` for BU's finite
confidence box and a finite density set for the density interval, so the
object is the pipeline wiring, not the finite-`n` confidence construction
(that is BV's object, not re-run here).

## 3. Synthetic data model

Every fixture is a declared table, not a draw:

- attempts are four-symbol verdicts `00,01,10,11` with a boolean loss flag;
- counts are exact integers, and every rational is an exact
  `[numerator, denominator]` pair;
- the expected reduction and target set are declared in `protocol.json` and
  checked by the tests;
- there are no timestamps, no readouts, no covariates and no hidden state.

Two accepted datasets exercise the paths: `D1` (no loss) reduces to
`r̂=(1/4,3/8)` and, at `e=0` over `B={0}`, yields `T={1/4}`; `D2` (one loss)
reduces to `r̂=(1/7,2/7)` and, at `e=1/4`, yields `T={1/4,17/80}`. Seven
refusal fixtures target the seven refusal conditions. Independent
inverse-only fixtures exercise the discrete inverse, including the
ambiguity case.

## 4. Refusal conditions

A run is refused, and no analysis is produced, when any of these holds. Each
has a purpose-built fixture; the set is closed over
`{integrity, analysis_id, mark, support, loss, insufficient, stationarity}`.

| Reason | Trigger |
|---|---|
| `integrity` | dataset content does not match its seal |
| `analysis_id` | dataset token differs from the protocol token |
| `mark` | declared mark correspondence is false |
| `support` | a forbidden `10` symbol is present |
| `loss` | loss fraction exceeds the pre-declared bound |
| `insufficient` | fewer than four usable attempts |
| `stationarity` | first/second half frequency gap exceeds tolerance |

The integrity check is a real SHA-256 seal over the dataset core; the tests
also seal a valid dataset, mutate one attempt, and verify the refusal fires.
The refusal order is fixed: integrity, analysis-id, mark, support, loss,
insufficient, support (`K₁>K₂`), stationarity.

## 5. Independence, evidence and limits

Two routes build the whole report independently: `primary.py` reduces with a
direct scan and evaluates ideal points by polynomial masses; `reference.py`
reduces with a `Counter`, evaluates ideal points by the BU segment-parameter
formulas, nests the inverse loops in the opposite order, and writes the
feasibility and BY predicates differently. The driver compares the complete
encoded reports and refuses on any difference. `results.json` is a
create-only capture; `source-freeze.json` records source bytes and hashes.

Limits: sources ≤262,144 bytes, capture artifacts ≤16,777,216 bytes,
analyses ≤30 seconds, suite ≤120 seconds. No randomness, no floats, no
network, no dependency beyond the standard library.

## 6. What is not claimed

This is not a physical measurement, a calibration, an apparatus result, or
evidence about any geometry. The synthetic datasets are declared tables, and
a passing rehearsal says only that the BZ pipeline is self-consistent and its
refusal conditions fire. No metric, continuum limit, Einstein equation or
gravity result follows, and the earlier gates remain conditional on BW/BX.

## 7. Decision boundary and provenance

CA supplies a bounded executable rehearsal, not data and not a physical
result. It preserves BV's first capture, BW's contract, BX's interface, BY's
preregistration, BZ's protocol and all pre-existing core/RET/application
work. The separate [decision record](RESULTS.md) records the outcome and
limits; the [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated. General densities/metrics, RET integration and
gravity remain separate; book work stays archival.
