# QR-05BZ decision record

10 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone protocol](README.md) now specifies the physical protocol
and the measured-data contract that a later run would follow to assess the
BY metric/dynamics tests. This gate selected no device, acquired no record,
and executed no calibration or numerical study.

## Main result

BZ turns the BY preregistration into a checkable protocol by fixing six
stages — pre-registration, reference/calibration, data taking, reduction
and authentication, analysis, reporting — and by fixing the data contract,
the uncertainty model, the feasibility formulas and the refusal
conditions.

The **measured-data contract** is content-addressed, append-only and
complete: a header fixing marks, design `(n,m,α,ε)`, acceptance `(H,K)` and
the frozen `analysis_sha256`; reference and calibration records; an
`attempts` list carrying every attempt with its four-symbol verdict,
including failures, forbidden symbols and aborts; a loss block with a
pre-declared bound; and a hash chain. No attempt may be deleted, relabeled
or postselected, and a present `10` is a support refusal, not a correction.

The **reduction** is deterministic: verify hashes and the frozen analysis
hash, map events to `K₁ ≤ K₂`, apply the pre-declared loss correction, run
the pre-registered stationarity test, and emit `C(K)` plus the loss report
and the BX layer statuses. A post-hoc estimator is exploratory and cannot
support the primary claim.

The **uncertainty model** routes every error into the BX ledger:

```text
sampling  -> alpha;   enclosure -> h = 1/m;
systematic -> a_sys + d_sys (pre-declared);
validity  -> beta_ref + beta_tr;   acceptance -> H, R1-R3;
support/loss/marks -> premises, not probability.
```

**Feasibility** uses the BU/BT every-batch certificate
`s = D(B) − 2 e_max − 2h > 0`, `n s² ≥ 10`: for a declared separation and
planned envelope the minimum `n` follows, and the protocol reports
infeasibility rather than relaxing the certificate. A favorable realized
width is not sufficient.

## What the protocol pre-declares

Every decision that could otherwise be made after seeing the data is fixed
in pre-registration: marks and regions, the event rule, the attempt unit,
`(n,m,α,ε)`, the acceptance and repetition rules, primary versus
exploratory analyses, the systematic bounds `a_sys,d_sys`, and the
analysis-code hash. The reference must not choose the family it later
validates without a multiplicity control, and optional stopping is not
permitted (BW R2/R3).

## Refusal and falsification conditions

A failure is a result, not noise: schema/hash mismatch refuses the run; a
present `10` is a support refusal; loss beyond its bound or undefined
refuses; a failed stationarity test refuses; a mark/registration mismatch
makes the chain inapplicable; a records-fitted reference leaves `G_a`
unproved; a failed certificate is reported as not certified; and a failed
BY Section 3 or 4 test refutes the respective metric or dynamics claim.
First failures are retained and never overwritten.

## Applicable value and boundaries

The useful structure is a complete, pre-registered measurement protocol
with an auditable data contract and explicit refusal conditions, so that a
later run's evidence is checkable and its failures are visible. It does not
supply data, a device, a calibration, a metric, a continuum limit or a
dynamics. Because BX reports every interface layer `unsupplied` and BW
leaves P1–P12 unmet, the protocol stands conditional and cannot be executed
as a claim now.

It selects no device, acquires no record, simulates or fabricates no data,
executes no calibration and performs no numerical study. It implies no RET
integration, no quantum-adapter coupling and no gravity result.

## Review and next gate

Independent analytical review checked that every BY/BX/BW precondition has
a protocol stage, that every error mode maps into the BX ledger, that the
data contract enforces completeness and immutability, that all
post-data decisions are pre-registered, and that no metric or dynamics is
smuggled in. Review also confirmed that infeasibility is reported rather
than hidden by relaxing the certificate.

The closest next steps are a bounded synthetic rehearsal of this pipeline
on declared-model data (to verify the reduction and analysis close
end-to-end, explicitly not physical), or a real measured run once an
apparatus and reference exist. Neither is executed here.

## Provenance and publication

BZ continues the committed `qr-05-bridge` branch, which began from pushed
BV commit `8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`; the BW/BX
and BY contracts are the branch's prior commits. No BV or BU source, freeze
or capture was modified or re-executed, and the BV first capture remains
100,522 bytes, SHA-256
`44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`.

Publication is only this decision record, [README.md](README.md), and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
application work and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
