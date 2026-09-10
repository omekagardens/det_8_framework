# QR-05BY decision record

10 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone preregistration](README.md) now fixes what a measured
program would have to show to legitimately claim a Lorentzian metric
interpretation and an Einstein-like dynamics, and what would refute each
claim. This gate derived no metric, executed no measurement and asserted
no dynamical law.

## Main result

Two claims are separated and each is given acceptance tests.

**Metric interpretation** is a map from admissible retained summaries to an
equivalence class of Lorentzian geometries,

```text
Phi : summary S -> [ (M, g) ] / ~,
```

with `~` at least conformal-and-scale, because the retained order fixes at
most a causal structure and BL/BM/BN leave absolute scale unidentified. It
is admissible only if: the dimension estimate is refinement-stable; the
causal/interval proxy matches the cones of `g` up to `~`; covariance holds
under the declared physical symmetry and not merely under birth labels or
schedules; every recorded collision is broken with declared data or
declared as the identified equivalence class; scale is reported only with
an independent source; local estimators agree across the established
refinement structure; and the claim is on populations with a declared
sampling law, not individual samples.

**Dynamical correspondence** is a well-defined law with a declared
continuum limit,

```text
L --(continuum limit)--> Einstein-Hilbert (+ matter) on (M,[g]),
```

admissible only if the law is normalized with no hidden preferred clock,
carries an action or variational limit that is computed rather than
asserted, has a stable continuum limit, reduces to the declared classical
and quantum baselines in the appropriate regimes, and is falsifiable.
Dynamics presupposes a declared metric/causal object; a metric without
dynamics is a legitimate intermediate result.

## Inherited obstructions carried forward

The preregistration is constrained by recorded results, each of which a
candidate must confront rather than ignore:

| Obstruction | Source |
|---|---|
| Equal endpoint kernel for different geometries | QR-05D |
| Sampling/observer identification collision | QR-05E |
| Whole-point/position ambiguity; hull != exact set | BG, BH, BI |
| Density compensation; absolute scale unidentified | BL, BM, BN |
| Estimators validated only given a supplied geometry | AF–AV, AW–BA |
| Finite-domain labelled results, no continuum limit | A–C, G–AR |
| No valid allowance; apparatus unsupplied | BW, BX |

The order-summary collision (QR-05D) and the whole-point collision (BG) are
the sharpest: a geometry is at most a *target-relative* identification, and
must be declared up to the collision equivalence, never recovered by
summary lookup.

## Falsification criteria

A metric claim is refuted by a scale-inconsistent dimension estimate,
causal cones inconsistent with `g`, label/schedule-only invariance, an
unbroken and undeclared collision, reported absolute scale without an
independent source, or a population claim resting on individual samples. A
dynamics claim is refuted by an ill-defined law or hidden preferred clock,
or by the absence of a variational/action limit or a wrong continuum
equation. Each failure is a result, not a setup artifact.

## Applicable value and boundaries

The useful structure is a disciplined preregistration: geometry and
dynamics may be claimed only through the stated tests, and the recorded
collisions, ambiguities and scale obstructions bound what can be claimed.
Because BX reports every interface layer `unsupplied` and BW leaves P1–P12
unmet, the gate is conditional and cannot be executed as a claim now. It
does not supply a metric, a manifold, a continuum limit or a dynamical
law, and it asserts no Einstein equation, field equation or gravitational
coupling. A physical protocol and measured data are prerequisites and
require a separate protocol.

## Review and next gate

Independent analytical review checked that each acceptance test maps to a
recorded obstruction or to a stated physical requirement, that no
invariance, scale or continuum claim is smuggled in, and that the
falsification criteria are exhaustive for the two claims. Review also
confirmed that the gate remains conditional on BW/BX.

The closest next steps are a bounded symbolic verification of the
preregistration's test structure, or a physical protocol and measured data,
after which the metric and dynamics claims could be assessed. Neither is
executed here. No apparatus, device, measured record, numerical `β`,
allowance, fixture sweep or calibration is produced or implied. No metric,
continuum limit, Einstein equation or gravity result is claimed.

## Provenance and publication

BY continues the committed `qr-05-bridge` branch, which began from pushed
BV commit `8b34191a8d05966cb8f60e856bfdbf1e30c2da45` on `ret`. The BW/BX
contracts are the branch's prior commit; no BV or BU source, freeze or
capture was modified or re-executed, and the BV first capture remains
100,522 bytes, SHA-256
`44b2f745b4fae5e602bd004d0a33bb4c4c203c57e006e195dbadc95d25687e7b`.

Publication is only this decision record, [README.md](README.md), and the
[Track-B roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
The 231 pre-existing dirty status entries, including separate core, RET,
application work and the local temporary model sheet, remain outside it.
Book work stays archival; Lean installation, clocks and later gravity
couplings remain deferred.
