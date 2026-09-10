# QR-05BX decision record

10 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone interface specification](README.md) now defines what an
apparatus or experiment must present for the preceding QR-05 conditional
results to apply, the evidence each interface layer requires, and the
conditions under which the interface fails. This gate installed no
apparatus, acquired no record, and executed no measurement, calibration or
numerical study.

## Routing

BW proposed a reference-calibration composition verification as the next
gate. The program owner directed that it be deferred and that the later
apparatus-to-event interface be designed instead. BW's proposal is retained
and not rejected; it remains available as a later bounded verification.
This gate is therefore QR-05BX, the apparatus-to-event interface design.

## Main result

The interface is a seven-layer tuple

```text
A = (M, E, R, R′, D, L, T),
```

metrology, event identification, mark/region correspondence, reference
characterization, population and sampling declaration, loss and selection
accounting, and timebase/order. Each layer declares the fields it supplies,
the BW premises it discharges, and its error modes. Each layer is flagged
`satisfied`, `unsupplied` or `refuted`.

The interface connects every chain input to a physical source: the ideal
family and marks (3.R), the density premise (3.R, 4.B), the actual nested
population and attempt law (3.E, 3.D), the fixed sampling design (3.D), the
distortion allowance `e_cal=a+d` (3.M, 3.R′, 3.L), and the ideal target
`τ(η)` (3.R). No layer is supplied by this gate.

The uncertainty ledger places each apparatus error into the structure the
earlier gates already distinguish:

```text
sampling          -> alpha
enclosure         -> h = 1/m
systematic        -> a_sys + d_sys
validity          -> beta
acceptance        -> H, R1-R3
support/loss/marks-> premises, not probability
```

An apparatus systematic that cannot be bounded is a missing premise, not a
larger `α`; the guarantee then reverts to the conditional BW contract.

## What the interface distinguishes

| Layer | Discharges | Refuted when |
|---|---|---|
| 3.M metrology | `a_sys`, `d_sys` | calibration/unit error on the wrong population |
| 3.E event identification | record population, nested support | merged/double/misassigned events; `P(10)>0` |
| 3.R mark/region correspondence | mark identity, target meaning | registration or definition error between channels |
| 3.R′ reference characterization | `G_a` | reference fitted to the records it validates |
| 3.D population/sampling | iid/stationarity, `E` | drift or changed attempt unit |
| 3.L loss/selection | `P(10)=0`, loss premise | unbounded loss, or postselection |
| 3.T timebase/order | (later gates only) | order ambiguity left unresolved |

Bridge-specific premises B1–B6 (readout well-defined, event rule declared,
region map traceable, ensemble declaration testable, attempt unit matches
the design, loss quantified) are all `unsupplied`. The BW premise list
P1–P12 is carried through unchanged and remains `unsupplied`.

## Falsification and failure conditions

A failed interface is a result, not noise. The chain is:

- **inapplicable** if region correspondence or the event rule cannot be
  established, if loss is unbounded, or if the population is shown
  nonstationary;
- **conditional only** if no independent reference or transfer evidence is
  supplied (the BW boundary);
- **refuted for the apparatus** if a declared identification, loss or
  stationarity claim is contradicted;
- **void** if forbidden support is manufactured by deletion, relabeling or
  postselection.

Six design-only controls (F1–F6) state which premise each apparatus defect
voids: registration offset, event merging, a records-fitted reference,
drift, dead time, and postselection. None is executed; each is a statement
about premise dependence for a future bounded verification.

## Applicable value and boundaries

The useful structure is a precise division of a physical measurement into
interface layers with explicit evidence requirements and explicit failure
modes, so that the QR-05 conditional results can be applied only when the
corresponding premises hold. It does not supply a device, a reference, a
measured population or a calibrated allowance, so every layer stands
`unsupplied` and the earlier results remain conditional.

In particular:

- **Geometric interpretation** is not established by a valid interface. A
  summary that predicts well is not yet spacetime distance.
- **Dynamical correspondence** is separate. No Einstein equation, field
  equation, metric or gravitational coupling follows from this interface or
  from passing the earlier gates.
- **Continuum, scale and general metrics** remain open, and absolute scale
  is not identified.

A valid interface would make the conditional results applicable to a
physical measurement, and no more. Measured tests and uncertainty models
require a separate protocol.

## Review and next gate

Independent analytical review checked that every chain input has a
responsible layer, that each layer's error modes map into the declared
ledger or premise list, that the failure conditions are exhaustive and
falsifiable, and that no geometric or dynamical conclusion is smuggled in.
Review also confirmed the routing note and that BW's composition
verification remains deferred rather than dropped.

The closest available next step is a bounded symbolic verification of the
interface's premise dependence and error routing, or the geometric-
interpretation gate once a physical protocol and data exist. Neither is
executed here. No apparatus, device, measured record, numerical `β`,
allowance, fixture sweep or calibration is produced or implied.

## Provenance and publication

BX began from pushed BV commit
`8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on authoritative branch `ret`,
and continues the uncommitted BW contract of the same session. No BV or BU
source, freeze or capture was modified or re-executed; the BV first capture
remains 100,522 bytes, SHA-256
`44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`.

Publication is only this decision record, [README.md](README.md), and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
application work and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
