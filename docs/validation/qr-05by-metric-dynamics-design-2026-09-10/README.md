# QR-05BY: metric interpretation and dynamics design

10 September 2026 (Pacific/Honolulu). **Analytical/design gate.**
This sheet preregisters what would be required to treat the retained
relational/record structure as a Lorentzian geometry, and what would be
required for a dynamics whose geometric limit is Einstein-like. It derives
no metric, executes no measurement, and asserts no dynamics. Every item is
an acceptance criterion, a required construction, or a falsification
condition, and every result is conditional on the apparatus interface and
reference evidence that BX/BW showed are not supplied.

Continue the [BW contract](../qr-05bw-reference-calibration-design-2026-09-10/README.md)
and the [BX interface design](../qr-05bx-apparatus-event-interface-design-2026-09-10/README.md)
without changing their frozen evidence. This gate is design-only and
depends on no measured data; without such data it cannot be more than a
preregistration.

## 1. Purpose and boundary

The QR-05 chain has produced, conditionally:

- exact finite-labelled record/order summaries and refinement structure
  (QR-05A–C, G–Z, AA–AR);
- supplied-geometry estimators of interval, volume and response quantities
  (QR-05AF–AV, AW–BA);
- identification results and explicit obstructions: whole-point and
  position ambiguity (BG, BH, BI), relative-volume and density
  compensation with unidentified absolute scale (BL, BM, BN), a
  sampling/observer identification collision (QR-05E), and an
  order-summary collision in which a 1+1 flat order and an S3 example share
  one entire endpoint kernel polynomial (QR-05D);
- a conditional distortion allowance (BW) and an apparatus interface (BX)
  under which those results could apply to a physical measurement.

None of this is a Lorentzian metric, a manifold, a continuum limit, or a
dynamical law. This gate fixes the criteria under which a later, measured
program could legitimately claim them, and the conditions under which the
claim fails. It does **not** claim:

- that a metric exists or is recoverable;
- that any retained summary is spacetime distance;
- that any dynamics holds, discretely or in a continuum;
- that Einstein's equations follow from passing BW/BX or from the earlier
  mathematics.

## 2. Inherited obstructions the design must confront

These are recorded results, not conjectures. Any metric-interpretation or
dynamics proposal must either break them with additional declared data or
state which equivalence class it identifies.

| Obstruction | Source | Consequence for a metric/dynamics claim |
|---|---|---|
| Order-summary collision: equal endpoint kernel for different geometries | QR-05D | A summary that is enough for one geometry is not enough to distinguish geometries; geometry must be a *target-relative* identification, not a summary lookup |
| Sampling/observer identification collision | QR-05E | Individual retained samples need not identify the population geometry |
| Whole-point/position ambiguity; target hull ≠ exact set | BG, BH, BI | Recovered target sets are unions/ambiguities, not a unique point |
| Relative-volume and density compensation; absolute scale open | BL, BM, BN | At most a conformal/causal structure and relative volumes, not an absolute metric |
| Supplied-geometry local estimators and error propagation | AF–AV, AW–BA | Estimators are validated **given** a geometry; they do not by themselves produce one |
| Finite-domain labelled results | A–C, G–AR | No continuum limit or scale invariance follows |
| No valid distortion allowance; apparatus unsupplied | BW, BX | No physical application yet; metric/dynamics stay conditional |

A design that ignores these is not admissible.

## 3. Metric interpretation: the claim and its acceptance tests

### 3.1 What the claim is

A **metric-interpretation claim** on a domain `D` (a declared family of
admissible orders/records with a fixed marks/target meaning) is a map

```text
Φ : admissible summary S  ->  [ (M, g) ] / ~
```

from retained summaries to an equivalence class of Lorentzian geometries
on a manifold `M`, where `~` is a declared equivalence (at least conformal
and scale, since the order fixes at most a causal structure; see BL/BM/BN).
The claim is not that `Φ` is an isometry, but that it is well-defined on
the declared domain up to `~` and falsifiable.

### 3.2 Acceptance tests

A candidate `Φ` is admissible only if all of the following hold, on a
declared domain and with the apparatus/reference evidence of BW/BX:

1. **Dimension estimate consistency.** An order-derived dimension estimator
   (for example a Myrheim–Meyer-type number–volume estimate) returns a
   stable value across refinement scales and agrees with a declared target
   dimension in the claimed limit. QR-05D's deterministic mesh bias and
   sampling ambiguity must be excluded, not averaged away.
2. **Causal/interval consistency.** An order-theoretic interval or
   longest-chain proxy maps consistently to proper time, and the induced
   causal relation matches `g`'s causal cones up to `~`, with provenance
   for every coefficient retained.
3. **Covariance.** Invariance under the declared physical symmetry, not
   merely under birth labels or execution schedules. The earlier gates
   repeatedly separated label/schedule invariance from
   Lorentz/diffeomorphism covariance; identifying them is not permitted.
4. **Collision handling.** For every recorded collision, `Φ` either breaks
   it with declared additional data (counts, volume, marks) or declares the
   identified object as the collision equivalence class. QR-05D's endpoint
   coincidence and BG's whole-point collision set the boundary.
5. **Scale declaration.** Scale is identified only if a separate,
   independently justified scale source is supplied. Otherwise the claim
   is conformal/relative-volume only; absolute scale is not reported
   (BL/BM/BN).
6. **Refinement consistency.** Local estimators must agree across the
   additivity/refinement structure established on supplied geometry
   (AH–AN), now applied to reconstructed rather than supplied geometry.
7. **Sampling robustness.** The claim must be stated on populations with
   the sampling law declared, not on individual retained samples
   (QR-05E); finite-shot certainty is not asserted.

### 3.3 Required constructions (not built here)

A measured program would need, at minimum: a declared domain and
equivalence `~`; a dimension estimator with an error model; an
interval/proper-time proxy with a covariance proof or a covariance test;
an explicit collision ledger; and a scale statement. None is constructed
by this gate.

## 4. Dynamical correspondence: the claim and its acceptance tests

### 4.1 What the claim is

A **dynamical-correspondence claim** is a well-defined law on the declared
structure together with a declared continuum/geometric limit whose
effective equations are Einstein-like on the metric of Section 3:

```text
L  --(continuum limit)-->  Einstein-Hilbert (+ matter) on (M,[g]).
```

Ordinary general relativity and ordinary quantum mechanics remain the
comparison baselines; the claim is a correspondence, not a new law unless
separately derived.

### 4.2 Acceptance tests

1. **Well-defined law.** A transition kernel or quantum measure on the
   declared structure, with normalization and no hidden external clock or
   preferred slicing. QR-05A–C established only finite joint consistency;
   they did not derive a law.
2. **Action / variational structure.** A discrete action with a declared
   continuum limit, or a causal-set d'Alembertian/Einstein–Hilbert
   correspondence. The limit must be computed, not asserted by analogy.
3. **Stable continuum limit.** The limit exists and is stable under
   refinement, with the regularization dependence controlled. BK's boundary
   work and the repo's separate continuum-limit efforts are inputs, not
   completed results.
4. **Baseline reduction.** In the appropriate limits the law reduces to the
   declared classical/quantum baselines; no new source, field or coupling is
   introduced silently.
5. **Falsifiability.** A stated observation or computation that would count
   against the correspondence.

### 4.3 Ordering

Dynamics presupposes at least a causal/conformal structure and a scale
statement from Section 3. A dynamics before a declared metric object is not
admissible; a metric without dynamics is a legitimate intermediate result.

## 5. Falsification criteria

A candidate metric or dynamics claim is **refuted** if any of these holds;
each is a result, not a setup artifact:

| Failure | Refutes |
|---|---|
| Dimension estimator inconsistent across scales | metric `Φ` (3.2.1) |
| Causal cones inconsistent with `g` | metric `Φ` (3.2.2) |
| Only label/schedule invariance | metric `Φ` (3.2.3) |
| A recorded collision survives unbroken and undeclared | metric `Φ` (3.2.4) |
| Absolute scale reported without an independent source | metric `Φ` (3.2.5) |
| Population claim rests on individual samples | metric `Φ` (3.2.7) |
| No well-defined law or hidden preferred clock | dynamics (4.2.1) |
| No variational/action limit, or wrong continuum equations | dynamics (4.2.2–4) |

## 6. Preconditions and conditional status

Every acceptance test in Sections 3–4 is conditional on BX's interface
being satisfied and BW's allowance being valid. Since BX reports every
layer `unsupplied` and BW leaves P1–P12 unmet, this gate is a
**preregistration**: it defines what a measured program must show, and it
cannot be executed as a claim now. A physical protocol and measured data
are prerequisites and require a separate protocol.

## 7. Decision boundary and provenance

BY supplies acceptance criteria, required constructions and falsification
conditions, not a metric, a manifold, a continuum limit or a dynamical law.
It preserves BV's first capture, BW's contract, BX's interface, BU's design
record and all pre-existing core/RET/application work. The separate
[decision record](RESULTS.md) records the review and limitations; the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md)
keeps later work gated.

The applicable structure is a disciplined preregistration: the program may
claim a geometry or a dynamics only through the stated tests, and the
recorded collisions, ambiguities and scale obstructions bound what may be
claimed. It is not general relativity, a quantum gravity theory, an
ontological proof or new physics. General densities/metrics, RET
integration and the quantum adapter remain separate. Book work remains
archival; Lean installation, clocks and later gravity couplings stay
deferred.
