# DET v8.0 — Track B: Gravity and the Record

**Status:** Status-M interpretation note.
**Empirical content:** No independent DET gravity prediction or discriminator.
**Baseline:** Gravitational calculations remain those of unmodified GR with separately declared source models.
**Date revised:** September 3, 2026.

## 1. Scope

This note records a candidate interpretation of gravitational geometry. It does not answer experimentally what gravity *is*, derive the Einstein equations, identify a new gravitational source, or establish that spacetime is fundamentally discrete.

The retired κ-gravity programs (archive/retired_kappa_gravity.md) attempted physical modifications or source models. Their failures and retirement support a governance decision: DET does not alter gravitational dynamics unless it first states a distinct observable consequence and a falsifier. They do not, by themselves, support the ontology proposed here.

The safe form of the proposal is:

> **DET proposes, as a Status-M interpretation, that the relational pattern represented in GR by \(g_{\mu\nu}\) may be understood as a coarse-grained description of an actualized record. This identity is neither directly observed nor currently derived by DET.**

“May be understood as” is load-bearing. Replacing it with “is” would turn an interpretation into an unsupported physical identity.

## 2. Evidence boundary

The four-level ladder in docs/observable_anchoring.md applies without exception:

| Level | Gravity example | What DET may claim |
|---|---|---|
| **1. Instrument record** | local clock readings, detector timestamps, interferometer output, image pixels, accelerometer or displacement readouts, calibration logs | These are direct records when acquisition and uncertainty are specified |
| **2. Derived empirical quantity** | frequency ratio, differential acceleration, arrival delay, strain, lensing angle, orbital parameters | These are empirical results conditional on analysis, synchronization, source, propagation, and instrument models |
| **3. Formal representation** | \(g_{\mu\nu}\), curvature, geodesics, \(J^-(e)\), ADM constraints, Wheeler–DeWitt equations, causal sets, sprinkling density | These are model structures, not raw observations; this note borrows them |
| **4. Interpretation** | metric-as-record, time-as-record-growth, gravity/quantum/time as one openness | These are Status M and have no known independent discriminator |

Two terms need special care:

- \(\prec\) is not presented here as a direct observation. Relativistic causal order is inferred from localized signal and timing records using synchronization and propagation assumptions. In T7 it is supplied by the synthetic generating geometry.
- \(\#\) is not automatically a fundamental spacetime count. Registered detector events can be counted, but equating a count of fundamental events with Lorentzian volume is a borrowed causal-set premise.

No result in this note closes either bridge.

## 3. What is borrowed

The proposal uses, but does not derive:

1. GR's metric and causal structure.
2. Canonical/ADM constraint formalisms.
3. Wheeler–DeWitt-style statements from particular approaches to quantum gravity.
4. Causal-set order-and-number reconstruction results and estimators.
5. Relational and growing-record interpretations discussed in the foundations literature.

These sources supply formal and conceptual scaffolding. Their empirical successes, mathematical results, and open problems do not transfer automatically into evidence for DET's ontology.

T7 (det8/models/order_count_geometry.py) is correspondingly a **synthetic estimator test**: known Lorentzian geometries generate samples, and borrowed estimators attempt to recover features of those generating geometries. Success supports the implementation and its internal correspondence claim. It does not show that physical events form such a causal set or that a metric is ontologically a record.

## 4. The metric-as-record proposal

In GR, a metric represents invariant interval, causal, clock, geodesic, and curvature relations even though its individual components depend on coordinates. DET asks whether this relational pattern can be interpreted as a coarse-grained description of actualized records rather than as a further substance.

That is a legitimate Track-B question, but the following stronger moves are not licensed:

- GR does not experimentally establish that the metric is a record.
- The equivalence principle motivates geometric formulations but does not uniquely select DET's ontology or prove that gravity is “not a field.”
- Diffeomorphism invariance or background independence does not by itself imply event-record primitivism.
- A mathematical reconstruction of metric information from order and volume does not establish that physical spacetime is fundamentally an order-and-count structure.
- Removing a new κ source avoids one unsupported physical posit; it does not prove the remaining interpretation.

The proposal is therefore judged by clarity and coherence while remaining explicitly underdetermined by current observations.

## 5. “Present-tense” gravity

“Gravity operates in the present” is retained only as an interpretation and not as a statement about propagation.

In suitable formulations of GR, local evolution is causal: gravitational disturbances do not provide instantaneous action at a distance. A local solution is not determined by matter in \(J^-(e)\) alone; it also depends on admissible gravitational initial/boundary data. \(J^-(e)\) itself is a GR-defined formal object, not a device record.

DET's restricted reading is:

> At an event represented by the adopted spacetime model, predictions use locally available field data and admissible prior data; DET interprets this without positing an already-actual future.

The first clause is conditional on the GR formalism. The second is Status M. Neither establishes that \(R^- = J^-(e)\), and this note does not identify a frame-dependent “present boundary” with the boundary of a causal past.

## 6. Canonical constraints and the Problem of Time

Canonical GR includes Hamiltonian and momentum constraints on admissible hypersurface data. Those constraints are not observations and should not be described as instantaneous gravitational influences. Evolution equations and constraints play different mathematical roles within a chosen formulation.

Likewise, \(\hat H\Psi=0\) belongs to canonical quantum-gravity programs, and the “Problem of Time” has several formulation-dependent versions and proposed responses. DET has not derived a quantum theory of gravity.

DET may use the following analogy:

> Constraint formalisms do not supply a preferred external time parameter; DET interprets experienced temporal succession as ordered record formation.

This does **not** show that the Problem of Time dissolves. “Time is record growth” remains Status M. The process tick expression

\[
\Pi_a(e)=\lim_{\Delta N\to\infty}
\frac{\mathbb E[\Delta N_a\mid R_e]}{\Delta N}
\]

is a DET formal definition conditional on an event/count model. It is not an observation that fundamental record count is time, nor an empirical derivation of that identity.

## 7. The “one openness” proposal is quarantined

DET notices a possible analogy among:

| Domain | Borrowed or interpreted feature |
|---|---|
| Temporal ontology | an unactualized future in DET's reading |
| Quantum theory | outcomes not fixed by the state description in DET's reading |
| Canonical gravity | absence of a preferred external time parameter in selected formalisms |

The claim that these are **one relational openness** is not entailed by their shared vocabulary. The three rows arise from different theories and different conceptual problems. In particular, \(H\approx0\) does not observationally mean “the future is open,” and a superposition does not formally state DET's metaphysics of becoming.

The unification remains a quarantined Status-M comparison:

- no independent empirical interface;
- no use as a premise in a physical derivation;
- no promotion from verbal economy or cross-domain resemblance;
- no claim to resolve the measurement problem or Problem of Time.

It may motivate questions, but it cannot certify answers.

## 8. Background and gravitational energy

An event graph can be specified without first assigning coordinates or a continuum metric. That is an architectural property of the formal model. Whether it yields the correct continuum, dynamics, degrees of freedom, and quantum behavior remains open. Calling the graph “background-free” does not solve quantum gravity.

GR also limits generally covariant localization of gravitational energy in ways that differ from ordinary matter stress-energy. ADM and Bondi quantities are associated with asymptotic structures; Brown–York constructions are quasi-local. These formal facts do not uniquely entail that gravity is “only connectivity” or that energy non-localization confirms the record ontology.

Both topics are motivations for inquiry, not evidential fruits of the interpretation.

## 9. Anti-smuggling audit

| Question | Answer |
|---|---|
| New field or parameter? | **No.** |
| New gravitational dynamics? | **No.** GR is an adopted baseline, not a DET derivation. |
| New prediction or falsifier? | **No.** |
| Independent empirical test of metric-as-record? | **None currently known.** |
| Evidence from standard gravity tests? | **No independent DET evidence.** Compatibility is inherited conditionally because DET leaves the successful GR predictions unchanged. |
| Directly observed primitives? | **None at the fundamental order-and-count level.** Instrument records and derived gravity quantities sit below the borrowed formal representation. |
| Status? | **M.** |
| Borrowed dependencies? | **GR causal/metric structure, canonical constraints, selected quantum-gravity formalisms, and causal-set reconstruction mathematics.** |

The note must not use checkmarks beside equivalence-principle, wave, lensing, or redshift observations as if those observations selected DET over empirically equivalent readings.

## 10. Ledger and promotion rules

The proposal has three different kinds of possible support:

| Support type | What would count | What it would not establish |
|---|---|---|
| **Internal derivational support** | a correct theorem or estimator from declared order/count premises | that the premises describe nature or that metric = record |
| **Empirical correspondence** | a declared bridge from instrument records to graph quantities reproduces measured relations | uniqueness over alternative models or ontologies |
| **Empirical discriminator** | a pre-registered observable difference from GR plus named rival interpretations | automatically an ontological identity |

T7 can currently contribute only to the first category and, on generated data, limited formal correspondence. Even a future manifoldlikeness theorem would be a conditional mathematical result. Promotion of “metric = record” to a physical claim requires a separately declared empirical bridge and discriminator; none exists now.

The Metaphysics Ledger therefore carries two explicit rows:

| Term | Status | Physical content | Promotion criteria |
|---|---|---|---|
| Gravity as relational geometry | M | None unique. Interprets GR's metric as a coarse-grained actualized record; neither directly observed nor currently derived by DET. | Internal T7 results are reported separately. Physical promotion requires an operational bridge and predeclared discriminator from named alternatives; none is known. |
| One relational openness | M | None unique. A comparison among DET temporal/quantum readings and selected canonical-gravity formalisms. | Remains M absent an independent empirical discriminator; coherence or formal analogy alone cannot promote it. |

## 11. Current limits and next work

Current conclusions are intentionally narrow:

1. DET adopts unmodified GR predictions and separately declared conventional source models as baselines.
2. Metric-as-record and time-as-record-growth are interpretations, not observations or DET theorems.
3. T7 checks borrowed estimators on synthetic data. Genuine emergence, physical event identification, continuum uniqueness, and dynamics remain open.
4. No gravity observation currently favors this ontology over empirically equivalent alternatives.
5. The retired \(\Pi/\kappa\) conformal factor and κ-gravity source models remain retired.

Useful next work is governance and bridge work: specify how laboratory registrations would operationally define candidate events and precedence; expose detector-efficiency and localization assumptions; test estimator robustness against non-manifoldlike adversaries; and keep those results distinct from any ontological claim.

No gravity novelty-ledger entry is created until there is a concrete observable discriminator.

**See also:** docs/observable_anchoring.md, docs/record_kernel_physics.md §6/T7, ONTOLOGY.md §6, MODEL_CARD.md, FALSIFICATION_LEDGER.md, archive/retired_kappa_gravity.md, and docs/track_b/cosmic_record.md.
