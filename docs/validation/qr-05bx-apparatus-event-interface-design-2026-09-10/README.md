# QR-05BX: apparatus-to-event interface design

10 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This sheet defines the interface a physical apparatus or experiment must
present for the preceding QR-05 conditional results to apply, the evidence
each interface slot requires, and the conditions under which the interface
fails. It installs no apparatus, acquires no record, executes no
measurement or calibration, and derives no metric or dynamics. The
displayed statements are an interface specification and its failure
conditions, not a physical result.

Continue the verified [BV decision](../qr-05bv-acquisition-distortion-verification-2026-09-09/RESULTS.md)
and the [BW contract](../qr-05bw-reference-calibration-design-2026-09-10/README.md)
without changing their frozen sources or captures. BW's proposed
reference-calibration composition verification is deferred, not rejected;
this gate is the next active step as directed.

## 1. Purpose and boundary

The QR-05 chain is conditional. Given an ideal geometric family with
supplied marks, an actual nested iid record population, a fixed sampling
design, and a valid distortion allowance, it returns geometric target sets
with stated coverage and selection bounds. None of those inputs has been
connected to anything an apparatus measures. This gate specifies that
connection.

It does **not** claim:

- that any apparatus realizes the interface;
- that a measured population is nested, iid, stationary or loss-free;
- that a passing interface yields a physical geometry;
- that any geometry obeys Einstein dynamics or gravity.

Two downstream questions are deliberately reserved and must not be
promoted here:

- **Geometric interpretation.** Whether a valid interface plus measured
  data supports treating the retained relational structure as geometry.
  This requires its own gate and its own protocol.
- **Dynamical correspondence.** Whether any such geometry has
  Einstein-like dynamics. This is separate again; no metric or field
  equation follows from passing the interface.

The deliverable is an auditable interface with explicit unmet premises and
explicit failure conditions, in the same sense as BW.

## 2. What the chain consumes

The interface must deliver, at minimum, the following objects. Each is a
chain input that is currently supplied only abstractly.

| Input | Chain role | Supplied by |
|---|---|---|
| Ideal family `θ=(η,δ)` on marks `Q,I₁,I₂` | Target family and geometry parameter | Sections 3.R, 3.M |
| Density premise `B` containing `δ_true` | Nuisance family for the enlarged inverse | Section 4.B |
| Actual population `r∈S` with `π(r)=(1−r₂,r₂−r₁,0,r₁)` | Observed record law, nested support | Sections 3.E, 5 |
| Attempt law: `n` iid paired attempts | Sampling theorem and confidence box | Sections 3.D, 3.E, 5 |
| Fixed sampling design `n,m,α,ε` | Coverage event `E` | Section 3.D |
| Distortion allowance `e_cal=a+d` (BW) | Enlarged inverse and separation certificate | Sections 3.M, 3.R, 4 |
| Ideal target `τ(η) ∈ {1/4,17/80}` | The quantity being identified | Sections 3.R, 3.R′ |
| Fixed marks, no redefinition | Mark identity and target meaning | Section 3.R |

If an interface cannot supply one of these, the corresponding chain result
is inapplicable; it is not weakened silently.

## 3. The apparatus-to-event interface

Represent the interface as a tuple

```text
A = (M, E, R, R′, D, L, T),
```

with seven layers. Each layer supplies stated fields, discharges stated
BW premises, and carries stated error modes. Every layer has a status flag
`satisfied` / `unsupplied` / `refuted`; an `unsupplied` layer keeps the
chain conditional and a `refuted` layer makes it inapplicable.

### 3.M Metrology and calibration

- **Fields.** Channel map from physical readouts to numbers, units,
  dynamic range, timebase, and a calibration certificate or traceability
  chain. For a reference channel, the independence statement of BW
  Section 3.
- **Discharges.** The systematic part `a_sys` of the reference-validity
  claim (BW P5) and, where a second channel is compared, `d_sys` (P6).
- **Error modes.** Miscalibration and unit error appear directly in
  `a_sys`; a calibration valid only on a different population or mark set
  does not transfer.

### 3.E Event identification

- **Fields.** The rule mapping calibrated readouts to discrete
  events/records: thresholds, coincidence windows, clustering, and the
  declared record alphabet (here four symbols `00,01,10,11`, with `10`
  forbidden under nesting).
- **Discharges.** The record population `r` and, in part, nested support
  (P8) and loss (P10).
- **Error modes.** Missed, merged, double-counted or misassigned events
  change the support or the population. A merely small disagreement in
  frequencies does not certify `P(10)=0` (BW control C3); the nesting
  claim must be established independently of the marginal fit.

### 3.R Mark and region correspondence

- **Fields.** Definitions of the physical regions corresponding to
  `Q,I₁,I₂`, their inclusion relations `I₁⊂I₂⊂Q`, and the metrology
  (fiducials, registration) that fixes the correspondence. The ideal
  target `τ(η)=μ(I₁)/μ(Q)` must refer to these regions.
- **Discharges.** Mark identity (P3), target meaning (P4) and the
  coordinate part of `d_sys` (P6).
- **Error modes.** Registration or definition error between channels
  introduces a mapping error; if unbounded, `d` is undefined and the
  transfer claim fails.

### 3.R′ Reference characterization

- **Fields.** An independent reference procedure in BW's sense: it
  returns `(r_ref,a)` and asserts `G_a={||r_ref−q(θ_true)||∞≤a}` without
  using the record attempts. If no independent reference exists, the layer
  is `unsupplied` and the chain remains conditional, exactly as BW.
- **Discharges.** `G_a`, and hence whether `e_cal` can be bounded at all.
- **Error modes.** A reference that is fitted to the records it is meant
  to validate is not independent; it addresses `G_d` only and cannot
  establish `a_sys` (BW Corollary 1).

### 3.D Population and sampling declaration

- **Fields.** The population frame, the physical attempt unit, the
  stationarity window, the iid claim, and the fixed design
  `(n,m,α,ε)` with the four tail allocations. The attempt pairing or
  marginal-comparison rule for the transfer statistic.
- **Discharges.** The iid/stationarity premises (P9) and the sampling
  event `E` of budget `α`.
- **Error modes.** Drift, nonstationarity, or a changed attempt unit
  invalidates the fixed-`r` premise and therefore both the sampling and
  transfer statements.

### 3.L Loss and selection accounting

- **Fields.** Detection efficiency, dead time, postselection and any
  deletion or relabeling rule, each with a bound; the inclusion of that
  bound in `a_sys`/`d_sys`.
- **Discharges.** Loss/postselection (P10) and the support premise (P8)
  where loss would create or remove forbidden symbols.
- **Error modes.** Unmodeled or unbounded loss changes the population;
  deleting, relabeling or postselecting records to manufacture admissible
  support is forbidden (BW Section 7).

### 3.T Timebase and order

- **Fields.** The clock reference and the rule that assigns any causal
  order or relation structure between events, if the downstream question
  uses order at all.
- **Discharges.** Nothing in the present geometric-target chain; it is
  recorded because later geometric-interpretation and dynamics gates will
  need a declared order and clock.
- **Error modes.** Order ambiguity is a separate defect that this gate
  does not resolve; it must not be silently identified with unknown
  spacetime geometry.

## 4. Evidence and assumption interface

Each row maps a chain premise to the layer that must supply it and to the
evidence that would discharge it. No row is supplied by this gate.

| Premise (BW) | Interface layer | Evidence that would discharge it | Status |
|---|---|---|---|
| P1 ideal family complete | 3.R, 3.R′ | Declared geometry family with a justified parameter range | Unsupplied |
| P2 `δ_true∈B` | 3.R, 4.B | Independently bounded density premise | Unsupplied |
| P3 mark identity | 3.R | Traceable region definitions and registration | Unsupplied |
| P4 target meaning | 3.R | The reference reports the same `τ` on the same regions | Unsupplied |
| P5 reference validity `a_sys` | 3.M, 3.R′ | Independent reference with a validity argument | Unsupplied |
| P6 same ensemble / coordinates | 3.R, 3.D | Shared frame and coordinate correspondence | Unsupplied |
| P7 attempt pairing | 3.D, 3.E | Defined unit and association rule | Unsupplied |
| P8 nested support `P(10)=0` | 3.E, 3.L | Identification rule plus loss accounting, not a marginal fit | Unsupplied |
| P9 iid / stationarity | 3.D | Fixed population over the declared window | Unsupplied |
| P10 no unmodeled loss | 3.L | Bounded efficiency/dead time included in `a_sys`,`d_sys` | Unsupplied |
| P11 reference independence | 3.R′ | Reference does not use the record attempts | Unsupplied |
| P12 fixed design | 3.D | Pre-registered `n,m,α,ε` and budgets | Unsupplied |

Bridge-specific premises added by this gate:

| Premise | Layer | Evidence | Status |
|---|---|---|---|
| B1 readout well-defined (units, range, clock) | 3.M, 3.T | Instrument specification and calibration certificate | Unsupplied |
| B2 event rule total/deterministic or stochasticity modeled | 3.E | Declared rule and its response model | Unsupplied |
| B3 region map traceable | 3.R | Fiducial/metrology record | Unsupplied |
| B4 ensemble declaration testable | 3.D | A stated, falsifiable stationarity procedure | Unsupplied |
| B5 attempt unit matches the declared sampling design | 3.D, 3.E | Pre-registered protocol | Unsupplied |
| B6 loss quantified and included | 3.L | Efficiency/dead-time measurement | Unsupplied |

Rule: an `unsupplied` load-bearing layer keeps the chain conditional; a
`refuted` layer makes the chain inapplicable to that apparatus. A passing
arithmetic score at any layer does not repair a missing or false premise.

## 5. Uncertainty ledger

Apparatus error must be *bounded and placed*, not merely small. The
interface routes each error mode into the ledger the earlier gates already
distinguish:

```text
sampling uncertainty        -> alpha          (BU/BQ/BS; layer 3.D)
grid enclosure              -> h = 1/m        (BU; layer 3.D)
systematic distortion       -> a_sys + d_sys   (BW; layers 3.M, 3.R, 3.L)
allowance validity          -> beta            (BW; layer 3.R′)
acceptance / selection      -> H, R1-R3        (BW; layer 3.D, 3.L)
support / loss / marks      -> premises, not
                               probability      (layers 3.E, 3.R, 3.L)
```

An apparatus-level systematic that cannot be bounded is not a larger `α`;
it is a missing premise, and the guarantee reverts to the conditional BW
contract. A bounded systematic consumes separation through `e_cal=a+d`,
exactly as BW composes it.

## 6. Minimal admissible protocol (prospective)

A physical protocol would have to satisfy, at least:

1. Pre-register the marks/regions, the event-identification rule, the
   attempt unit, and the sampling design `(n,m,α,ε)`.
2. Supply a traceable region correspondence (B3) and a calibration
   certificate (B1).
3. Supply an independent reference and its validity argument, or declare
   that none exists and accept the conditional boundary (3.R′, P5).
4. Bound and include loss (B6, P10), and establish nested support
   independently of the marginal fit (P8).
5. State and test stationarity over the declared window (B4, P9).
6. Supply a distortion allowance `e_cal=a+d` by BW's composition, or state
   the envelope `e_max` and its budget `β_env`.
7. Fix `β_ref,β_tr,e_max,H` before acquisition and state the acceptance
   and repetition rules.

This gate does not execute or endorse a specific protocol, apparatus or
device. Measured tests and uncertainty models require a separate protocol.

## 7. Failure and refusal conditions

A failed interface is a result, not noise. The chain is:

- **inapplicable** if region correspondence or the event rule cannot be
  established (P3, B2, B3), if loss is unbounded (P10, B6), or if the
  population is shown nonstationary (P9);
- **conditional only** if no independent reference or transfer evidence is
  supplied (P5, P11) — the BW boundary;
- **refuted for the apparatus** if a declared identification, loss or
  stationarity claim is contradicted by the measured check;
- **void** if forbidden support is manufactured by deletion, relabeling or
  postselection.

None of these failures is to be reported as a setup artifact without the
evidence that would distinguish it from a genuine defect.

## 8. Falsification and controls

The interface must be falsifiable, in the same sense as the earlier
gates: each layer declares what observation would count against it.
Prospective design-only controls, none executed here:

| Control | Introduces | Expected outcome |
|---|---|---|
| F1 | Region registration offset | `d_sys` nonzero; transfer bound grows; unbounded if unmeasured |
| F2 | Event threshold causing merged/double records | Support or loss premise fails; `P(10)=0` not certified |
| F3 | Reference fitted to the records | `G_a` unproved; `e_cal` unbounded (BW Cor 1) |
| F4 | Slow drift across the window | P9 fails; both sampling and transfer void |
| F5 | Unmodeled dead time | P10 fails; population changed |
| F6 | Postselection to remove `10` | Support manufactured; chain void |

These are statements about which premise a guarantee depends on, to be
checked symbolically by a future bounded verification, not a fixture bank.

## 9. What remains open on the path to gravity

- **Geometric interpretation** is not established by a valid interface.
  A summary that predicts well is not yet spacetime distance.
- **Dynamical correspondence** is separate. No Einstein equations, field
  equation or gravitational coupling follows from this interface or from
  the earlier gates.
- **Continuum and scale** remain open; the chain is finite-domain.
- **Absolute scale** is not identified (BL/BM).

A valid interface would make the QR-05 conditional results *applicable to
a physical measurement*, and no more. Metric identification and dynamics
require their own gates and their own measured protocols.

## 10. Decision boundary and provenance

BX supplies an interface specification and its failure conditions, not a
measurement, a device, a calibration or a physical result. It preserves
BV's first capture, BW's contract, BU's design record and all pre-existing
core/RET/application work. The separate [decision record](RESULTS.md)
records the routing and the limitations; the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated.

Since no apparatus, reference or measured population is supplied, the
interface stands entirely `unsupplied` and the earlier results remain
conditional. Geometric interpretation, dynamics, general densities/metrics,
RET integration and the quantum adapter remain separate. Book work remains
archival; Lean installation, clocks and later gravity couplings stay
deferred.
