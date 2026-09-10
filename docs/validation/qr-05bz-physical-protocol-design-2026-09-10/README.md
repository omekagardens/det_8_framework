# QR-05BZ: physical protocol and measured-data design

10 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This sheet specifies the physical protocol and the measured-data contract
that would be required to move the preregistered metric/dynamics tests from
a conditional statement to an assessment on data. It selects no device,
acquires no record, executes no calibration, and asserts no metric or
dynamics. Every item is a protocol requirement, a data-schema obligation, a
pre-registered decision or a failure condition.

Continue the [BY preregistration](../qr-05by-metric-dynamics-design-2026-09-10/README.md),
the [BX interface](../qr-05bx-apparatus-event-interface-design-2026-09-10/README.md)
and the [BW contract](../qr-05bw-reference-calibration-design-2026-09-10/README.md)
without changing their frozen evidence. This gate runs nothing and depends
on no data; it is the protocol a later measured program would follow.

## 1. Purpose and boundary

BY fixed the acceptance tests for a metric interpretation and a dynamical
correspondence but stated that they require a physical protocol and
measured data. BZ supplies that protocol specification: the stages, the
data contract, the reduction and authentication, the uncertainty model, the
power/feasibility formulas, the pre-registration and blinding rules, and
the abort and falsification conditions.

It does **not**:

- choose or model a device;
- acquire, simulate or fabricate measured records;
- execute a calibration or a numerical study;
- claim a metric, a continuum limit, or any dynamics.

The difference between this gate and a measured run is exactly the data:
BZ is the contract; a run would be a separate, data-bearing gate.

## 2. Preconditions from BW, BX and BY

BZ is executable only when all of the following are supplied. None is
supplied here.

| Precondition | Source | Status |
|---|---|---|
| Apparatus interface layers `M,E,R,R′,D,L,T` satisfied | BX | Unsupplied |
| Reference characterization or explicit absence | BW 3, BX 3.R′ | Unsupplied |
| Same-population transfer premise and bound | BW 4 | Unsupplied |
| Valid allowance `e_cal=a+d` or envelope `e_max` with budget | BW 5–6 | Unsupplied |
| Declared metric domain and equivalence `~` | BY 3.1 | Unsupplied |
| Fixed sampling design `n,m,α,ε` and budgets | BU/BQ/BS | Declared, not realized |

If a precondition is unsupplied, the protocol stops at its conditional
boundary and reports so; it must not substitute a fitted value.

## 3. Protocol stages

Each stage declares its inputs, its outputs, its pre-registered decisions,
and its failure modes.

1. **Pre-registration.** Fix the marks/regions, the event-identification
   rule, the attempt unit, the sampling design `(n,m,α,ε)`, the acceptance
   and repetition rules (`H`, `K`), and the primary versus exploratory
   analyses. Freeze the analysis-code hash before any data exist.
2. **Reference and calibration.** Run the reference procedure (BW) and the
   region/loss characterization (BX 3.R, 3.L). Establish `a_sys`, `d_sys`,
   `β_ref`, `β_tr` and `e_max`, or record their absence.
3. **Data taking.** Collect the pre-registered number of attempts,
   recording every attempt including failures, forbidden symbols and
   aborts. No deletion, relabeling or postselection (BX 3.L, BW 7).
4. **Reduction and authentication.** Validate the schema and hashes, map
   readouts to the declared records, apply the pre-declared loss/dead-time
   correction, and run the pre-registered stationarity test.
5. **Analysis.** Form the count box `C(K)` (BU), apply the enlarged inverse
   with the valid allowance, obtain the target set, then assess the BY
   Section 3–4 tests.
6. **Reporting.** Publish the complete result, including every failure,
   abort and negative outcome. A failed interface is a result.

## 4. Measured-data contract

The data contract is content-addressed, append-only and complete. Required
structure (field names illustrative, types exact):

```text
{
  "header": {
    "schema": "qr05bz-measured-v1",
    "protocol_id": "...",
    "analysis_sha256": "...",          // frozen analysis-code hash
    "marks": { "Q": ..., "I1": ..., "I2": ... },
    "design": { "n": ..., "m": ..., "alpha": [...], "tails": [...] },
    "acceptance": { "H_rule": ..., "K": ... },
    "primary_analyses": [...], "exploratory_analyses": [...]
  },
  "reference": {
    "present": true|false,
    "r_ref": [...], "a_sys": [...], "a_stat": [...],
    "beta_ref": [...], "validity_argument": "..."
  },
  "calibration": [ { "id": ..., "records": [...], "hashes": [...] } ],
  "attempts": [
    { "index": ..., "timestamp": ...,
      "channels": [...], "event": "00"|"01"|"10"|"11",
      "marks": {...}, "loss": false|true, "quality": [...],
      "covariates": {...} }
  ],
  "loss": { "efficiency": ..., "dead_time": ..., "bound": [...] },
  "provenance": { "prev_sha256": ..., "self_sha256": ... }
}
```

Obligations:

- **Completeness.** Every attempted record appears, with its event verdict.
  A `10` is retained and reported, never deleted, relabeled or masked
  (BW Section 7); deletion to manufacture admissible support is forbidden.
- **Immutability.** Attempts are append-only and hash-chained; the frozen
  `analysis_sha256` must match the code that produces the reduction.
- **Blinding.** Where the design permits, the reference/calibration stage is
  blinded to the analysis model, and the analysis is run once on the frozen
  bytes.
- **Reduction fidelity.** The reduction is a declared function of the frozen
  bytes and the schema; no manual step may alter a record.

## 5. Reduction and authentication

The reduction must be deterministic and reproducible:

1. Verify the self-hash and the hash chain; reject any edited or missing
   attempt rather than repairing it.
2. Verify `analysis_sha256` equals the hash of the frozen analysis code.
3. Map each `event` to its four-symbol verdict; form `K_i = sum_j Y_ji`
   with `Y` the retained marks, enforcing `0 ≤ K₁ ≤ K₂ ≤ n`. A present `10`
   is a support refusal, not a silent correction.
4. Apply the pre-declared loss/dead-time correction; if the correction is
   undefined or the loss bound is exceeded, refuse (BX F5, P10).
5. Run the pre-registered stationarity test; failure refuses the run
   (BX F4, P9).
6. Emit the reduction outputs: `C(K)`, the loss report, the BX layer
   statuses, and the reference/allowance record.

The reduction introduces no estimator not fixed in pre-registration; a
post-hoc estimator is an exploratory analysis and cannot support the
primary claim.

## 6. Uncertainty model

The protocol routes every error into the ledger fixed by BX Section 5:

```text
sampling            -> alpha        (BQ/BS theorem; attempt unit as reduced)
enclosure           -> h = 1/m      (BU)
systematic          -> a_sys + d_sys (BW; pre-declared, not fitted)
validity            -> beta_ref + beta_tr (BW; from the calibration procedure)
acceptance/selection-> H, R1-R3     (BW; fixed before data)
support/loss/marks  -> premises     (BX; refuted or satisfied, not averaged)
```

Requirements:

- **Pre-declared systematics.** `a_sys` and `d_sys` are engineering or
  traceability bounds fixed before data; a bound chosen after seeing the
  data is exploratory and voids the primary guarantee (BW Corollary 1).
- **Attempt-unit consistency.** The binomial sampling theorem applies to
  the reduced attempt unit; the protocol must show the mapping from
  physical attempts to the reduced unit, including any loss correction.
- **Multiplicity.** All primary tests are pre-registered; multiple domains,
  targets or reference choices require a declared family-wise control
  (BW Section 7, BX 3.R′).
- **Selection.** The acceptance rule `H` and repetition bound `K` are fixed
  in pre-registration; optional stopping is not permitted (BW R2/R3).

## 7. Power and feasibility planning (formulas only)

The BU/BT every-batch certificate must hold for the prespecified envelope:

```text
s = D(B) − 2 e_max − 2 h > 0,        n s² ≥ 10,        h = 1/m.
```

Given a declared ideal separation `D(B)` and a planned `e_max`, the
minimum `n` follows from `n ≥ 10 / s²`, and `m` from the rounding budget.
This is a design formula, not an executed allocation: no device, grid or
quota is chosen here, and a favorable realized width is **not** sufficient
(BU Section 5). If the required `n` is infeasible for the apparatus, the
protocol reports infeasibility rather than relaxing the certificate.

## 8. Analysis pipeline and reporting

From the reduction outputs:

1. Form `C(K)` and use the valid allowance `e_cal` (or `e_max`) to compute
   BU's enlarged inverse and the discrete target set `T` (a set, not a
   hull).
2. Apply the BY Section 3 acceptance tests for the metric claim and, if and
   only if a metric object is declared, the BY Section 4 tests for
   dynamics.
3. Report `T`, every BX layer status, the allowance components, the
   coverage/validity/selection events, the seed and every failure, abort
   and negative outcome.

A reported target set with an unsupplied interface or an invalid allowance
is reported as conditional, never promoted.

## 9. Pre-registration, blinding and integrity

- Freeze the protocol, the analysis code and the acceptance rules before
  data; publish their hashes.
- Label every analysis primary or exploratory; an exploratory result is
  reported as such and does not support the primary claim.
- Do not let the reference choose the family it then validates without a
  multiplicity control (BW Section 7, C8).
- Retain first failures; do not overwrite an aborted or refused run.

## 10. Falsification, aborts and quality gates

The protocol pre-declares the conditions under which it refuses or
refutes, so a failure is a result rather than noise:

| Condition | Action |
|---|---|
| Schema/hash mismatch or edited attempt | Refuse the run (integrity) |
| Present `10` symbol | Support refusal; no correction (P8) |
| Loss bound exceeded or undefined | Refuse (P10, BX F5) |
| Stationarity test fails | Refuse (P9, BX F4) |
| Registration/mark mismatch | Inapplicable (P3, BX F1) |
| Reference fitted to the records | `G_a` unproved; conditional only (BW Cor 1, BX F3) |
| Certificate `s>0`, `n s²≥10` fails | Report not certified; do not relax |
| Metric acceptance test fails (BY 3) | Refute the metric claim |
| Dynamics test fails (BY 4) | Refute the dynamics claim |

None of these is to be reported as a setup artifact without the evidence
that would distinguish it from a genuine defect.

## 11. What is deliberately excluded

No device or apparatus is selected or modeled; no record is acquired,
simulated or fabricated; no calibration or numerical study is executed; no
RET integration or quantum-adapter coupling is implied. The protocol
supplies no metric, continuum limit or dynamics, and no gravity result.
General densities/metrics, the continuum limit and later gravity couplings
remain separate. Book work remains archival; Lean installation, clocks and
later gravity couplings stay deferred.

## 12. Decision boundary and provenance

BZ supplies a protocol and a data contract, not data and not a physical
result. It preserves BV's first capture, BW's contract, BX's interface,
BY's preregistration and all pre-existing core/RET/application work. The
separate [decision record](RESULTS.md) records the review and limitations;
the [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated.

The applicable structure is a complete, pre-registered measurement
protocol with an auditable data contract and explicit refusal conditions,
so that a later run's evidence is checkable and its failures are visible.
It is not an experiment, a calibrated instrument, a metric or a dynamics.
