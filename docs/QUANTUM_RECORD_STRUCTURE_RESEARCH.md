# Quantum and record structures in DET8

**Started:** September 5, 2026

**Status:** Active, bounded mathematical research charter; no new physical law proposed.

**First result:** Analytical examples and a conditional composition argument below; no new computational or empirical study has been executed for this document.

**Working source:** This primary checkout. RET SDK hardening continues separately.

## 1. Purpose and authorization

Investigate whether expressing familiar quantum mechanics through DET's events,
possibilities, relationships, and records reveals useful mathematical structure.
Success may be a clearer formulation, a reusable algorithm, a consistency
certificate, an informative counterexample, or a better experimental question.
A different physical law or proof of the ontology is not required.

The owner's September 5 direction authorizes this narrow parallel research lane.
It is a limited exception to the earlier deferral of quantum research in the
[hardening and application plan](CORE_HARDENING_AND_APPLICATION_PLAN.md), not a
declaration that G2–G5 have closed or that all deferred research has reopened.
The main delivery sequence remains RET SDK, materials monitoring, then anomaly
triage. Clock experiments, modified gravitational dynamics, public scientific
claims, and book development are not authorized by this charter.

The central question is:

> Can a finite network of DET-described quantum operations preserve quantum
> predictions and complete outcome records under every permitted reordering
> of independent events, and does that formulation make useful structure explicit?

### Should this wait for RET hardening?

**The mathematical work need not wait. Integration and application claims do.**

| Work | Can start independently? | Boundary |
|---|---|---|
| Definitions, analytical examples, proofs and counterexamples | Yes | State premises and credit established mathematics |
| Small isolated quantum-reference prototypes | Yes, after the fixture contract is reviewed | Separate research files, bounded resources, no RET package changes |
| Exploratory Track-B connections to ordering and geometry | Yes | Questions and conditional mathematics, not gravitational predictions |
| Quantum adapter built on the RET public API | Later | Wait for a stable reviewed API; validate quantum likelihoods separately |
| Claims of calibrated experiment selection or application benefit | No, not yet | Require the appropriate SDK and application evidence |

No RET sources, benchmark manifests, acceptance rules, retained artifacts,
dependency locks, or validation material are to be changed by this lane. Small
research runs must not overlap a timing-sensitive SDK rehearsal. Shared source
files must remain untouched while another task verifies a source-bound run.
Do not import another checkout or treat its results as this checkout's evidence.

## 2. What compatibility means

The target is operational compatibility with established quantum predictions
within an explicitly stated domain, followed by comparison with relevant
measurements where available. A finite test suite cannot certify all of physics.

Keep these levels separate:

1. **Description:** express an existing quantum operation in DET notation.
2. **Mathematical structure:** prove something about composition, records, or
   coarse-graining under declared premises.
3. **Computational value:** show a useful diagnostic, simpler implementation,
   stronger check, or measured computational advantage.
4. **Empirical compatibility:** compare predictions with acquired records using
   a declared apparatus, uncertainty, and selection model.
5. **Physical novelty or ontology:** neither is an automatic consequence of 1–4.

The same distinction applies to other interpretations of quantum theory.
Methodological success can support DET's fruitfulness without uniquely selecting
its ontology. Conversely, the absence of a new physical prediction does not make
a useful reformulation worthless.

### Noise, setup and model artifacts are hypotheses, not exemptions

It is legitimate to challenge an idealized noise model, an apparatus model, a
data reduction, or a numerical artifact. It is not legitimate to preserve DET
by declaring every disagreement an experimental problem.

For any apparent conflict:

- Retain the raw registrations, calibration records, exclusions and uncertainty
  assumptions. Distinguish detector output from inferred quantities.
- First check the mathematics and implementation against an independent
  standard-QM calculation of the **same** experiment.
- State a concrete conventional explanation: preparation error, readout error,
  loss, drift, crosstalk, selection bias, finite sampling, or another specified
  mechanism. Specify how it changes the predicted distribution.
- Constrain that explanation using independent calibration, a control, or fresh
  evidence. Fitting a nuisance model to the disputed residual is not independent
  confirmation; account for its fitted parameters and selection.
- Preserve unsuccessful explanations. A revised apparatus model creates a new
  analysis version; it does not erase the original discrepancy.
- Keep nondetections, discarded outcomes, and postselection visible. No-signalling
  tests concern unconditional local statistics, not only selected subsets.
- If a reproducible disagreement survives the declared checks, mark the
  formulation or its claimed domain as incompatible or unresolved. A proposal
  for different laws would require a separate authorization and protocol.

Compatibility is not exact agreement with every random finite sample. It means
agreement at the level justified by the declared statistical and systematic
uncertainties. Synthetic correspondence, measured compatibility, and robustness
to misspecified noise must be reported separately. See
[observable anchoring](observable_anchoring.md).

## 3. Present foundation and gaps

| Existing component | What it supplies | What it does not supply |
|---|---|---|
| [MAM-Q](../det8/models/mamq.py) | Pure-qubit states, restricted Kraus instruments, outcome probabilities and pointer commits | General mixed-state instruments, an ontology proof, or a gravity model |
| [Quantum correctness tests](../det8/tests/test_quantum_correctness.py) | Analytic and adversarial fixtures, including asymmetric probabilities and amplitude damping | Universal quantum or experimental validation |
| [T8 record growth](track_b/covariant_record_growth.md) | Conditional finite classical schedule, birth-label and joint-record consistency | Quantum composition, physical spacelike locality or Lorentz covariance |
| [Pair-kernel exploration](../det8/models/pair_kernel.py) | Finite interference and coarse-graining demonstrations | A hardened general positive-semidefinite library or a derivation of all QM |
| [T7 geometry](../det8/models/order_count_geometry.py) | Selected order/count estimators on samples from supplied Lorentzian geometries | Emergent spacetime, uniqueness or gravitational dynamics |
| [RET SDK](RET_SDK.md) | Developing evidence, model and decision contracts | A calibrated quantum measurement adapter |

Current MAM-Q uses one Kraus operator per distinct outcome label in its
pure-qubit instrument. The more general density-matrix, multi-Kraus-per-outcome
formulation below is a proposed research representation, not an existing public
SDK capability.

Two reviewed cautions must not become premises of new work:

- An older paragraph in [Record-Kernel Physics](record_kernel_physics.md)
  incorrectly locates interference only in the imaginary part of a pair-kernel.
  For disjoint alternatives it is the term `2 Re D(A,B)` that enters the
  union weight. A real off-diagonal kernel can interfere.
- The exploratory pair-kernel Cholesky path rejects zero pivots, so it rejects
  some valid rank-deficient positive-semidefinite matrices. It cannot serve as
  the independent positivity oracle for this research.

For example, the real matrix with all four entries equal to `1/4` is normalized
by the sum of its entries, positive-semidefinite and rank one. Its two singleton
weights sum to `1/2`, while their union has weight `1`: the remaining `1/2` is
the interference term. These singletons are not a decoherent probability
partition. This one analytical fixture exposes both cautions above.

These are limitations identified by source inspection, not repaired by creating
this document. Existing research prose and code are starting material, not an
unqualified authority.

## 4. A precise DET-shaped quantum formulation

Fix a finite-dimensional quantum system with density matrix `rho`: a positive
semidefinite, unit-trace operator. Keep the quantum state distinct from the
classical acquisition record `R`; the chosen interpretation of the state is
not an additional measured variable.

For event `e`, setting `s`, and outcome `x`, use a quantum instrument:

\[
\mathcal I_{e,x}^{s}(\rho)
  = \sum_a M_{e,x,a}^{s}\rho (M_{e,x,a}^{s})^\dagger,
\qquad
\sum_{x,a}(M_{e,x,a}^{s})^\dagger M_{e,x,a}^{s}=I.
\]

Each outcome map is completely positive and trace-nonincreasing; summing all
outcomes is trace-preserving. These are adopted standard-QM ingredients, not
derived DET laws. [Preskill, measurement and quantum operations](https://www.preskill.caltech.edu/ph219/chap3_15.pdf)

Their DET indexing is:

\[
K_e(x\mid R^-,s)=\operatorname{Tr}\mathcal I_{e,x}^{s}(\rho_{R^-}),
\qquad
\rho_{R^+}=\frac{\mathcal I_{e,x}^{s}(\rho_{R^-})}
 {K_e(x\mid R^-,s)}.
\]

The normalized update is defined only when the outcome probability is positive.
A zero-probability outcome on a given input has zero unnormalized output; retain
its instrument map because it may have positive probability on another input.
Do not divide by zero or silently remove small but nonzero branches. A simulation
seed provides reproducibility, not a physical mechanism of actualization.

The appended record binds at least the event ID, setting, observed outcome,
declared dependencies, preparation/calibration context and source provenance.
Record slots are indexed by event ID, not by the arbitrary execution order.
Execution logs may have different orderings while the abstract event record
and its probability law remain the same.

The combined record is an analysis representation, not a claim that remote
outcomes become instantly accessible. Access to another event's outcome requires
an allowed communication or causal dependency in the modeled apparatus.

If the setting is adaptive, it may read only declared causal-past records.
Hidden dependence on a scheduler counter or an incomparable event's outcome
would invalidate a claim of independence.

### Preserve quantum information before forming an ordinary kernel

The states `( |0> + |1> ) / sqrt(2)` and `( |0> - |1> ) / sqrt(2)` share the
same Z-measurement probabilities but have opposite certain X outcomes.
Consequently, storing only one measurement's probability vector cannot replace
the state or its relative-phase information.

A separate histories-based representation can use a decoherence functional
`D(A,B)`. For disjoint `A,B`, biadditivity and Hermiticity give

\[
\mu(A\cup B)=\mu(A)+\mu(B)+2\operatorname{Re}\mathfrak D(A,B),
\qquad \mu(A)=\mathfrak D(A,A).
\]

This connects to existing quantum-measure mathematics. On an exactly decoherent,
complete partition, normalized diagonal weights form an ordinary probability
distribution. Approximate decoherence requires an explicit error bound; it does
not justify exact normalization or exact equivalence by assertion.
[Sorkin, quantum measure theory](https://arxiv.org/abs/gr-qc/9401003)

Quantum instruments and general history pair-kernels are related research
routes, not interchangeable data types. Any translation must specify the event
algebra, composition and conditioning rules. Do not infer a unique full quantum
theory from positivity or a finite interference example alone.

## 5. First study: complete quantum-record composition

**Identifier:** QR-01

**Status:** Analytical formulation and worked cases; computational verification not run.

**Question:** When does changing a permitted execution schedule preserve the
complete quantum state and classical record law?

### 5.1 The object to compare

Lift each event instrument to a quantum-plus-classical-record map. For a fresh
record slot `r_e`, suppressing unchanged older slots,

\[
\widehat{\mathcal I}_e(\rho)
  = \sum_x \mathcal I_{e,x}(\rho)
    \otimes |x\rangle\langle x|_{r_e}.
\]

For adaptive events this is a linear map on the full classical-quantum state,
controlled by the allowed past-record blocks. Compare compositions only after
identifying the same event-indexed output slots. Compare unnormalized branch
maps or the complete lifted map, not nonlinear normalized conditional updates.

For incomparable events `e` and `f`, the sufficient condition is

\[
\widehat{\mathcal I}_f\circ\widehat{\mathcal I}_e
 =\widehat{\mathcal I}_e\circ\widehat{\mathcal I}_f
\]

on the complete allowed input operator space. In the nonadaptive case with
separate fixed outcome labels, this can be checked outcome by outcome:

\[
\mathcal I_{f,y}\circ\mathcal I_{e,x}
 =\mathcal I_{e,x}\circ\mathcal I_{f,y}
\quad\text{for every }x,y.
\]

This is stronger than matching a few outcome probabilities or commuting only
after discarding all outcomes. It is a deliberately strong sufficient guarantee
for all subsequent quantum measurements represented in the model, not a
necessary criterion for every restricted observational task. A weaker
task-specific equivalence must explicitly state which future questions it covers.

### 5.2 Conditional finite argument

Fix a finite acyclic event order. Every permitted schedule is a linear extension
of that order. Any two linear extensions can be connected by adjacent swaps of
incomparable events. If each such swap preserves the complete lifted map, every
schedule has the same composite map after canonical record-slot identification.

This is the familiar commuting-map argument applied to quantum-record maps,
not a new theorem of physics. The substantive work is specifying and checking
its premises. Agreement for a selected state is not operator equality.
It establishes schedule independence within the model, not Lorentz covariance,
background independence, a preferred present, or a gravitational equation.

### 5.3 Positive example: separate subsystems, including entanglement

Let Alice's outcome map act only on subsystem A and Bob's only on subsystem B.
Their Kraus operators have forms `A_xa tensor I` and `I tensor B_yb`.
Those operators commute; the outcome-resolved maps therefore commute, including
on entangled inputs. Give the events separate record slots and forbid each
setting from reading the other outcome.

For the Bell state `( |00> + |11> ) / sqrt(2)`, local Z measurements produce
`P(0,0)=P(1,1)=1/2`, with the other two outcomes zero, in either schedule.
Correlations are retained; no classical factorization of the joint law is
assumed. Local unconditional marginals are unchanged by a remote complete
local instrument. Conditional correlations are not a signalling channel.

### 5.4 Negative example: forgetting records hides a conflict

On one qubit, consider projective Z and X measurements. Their outcome-discarded
dephasing channels commute: applying both sends every qubit state to `I/2`.
Nevertheless, their **recorded instruments do not commute**.

Starting in `|0>`, with records always displayed as `(Z outcome, X outcome)`:

| Record | Z then X | X then Z |
|---|---:|---:|
| `(0,+)` | 1/2 | 1/4 |
| `(0,-)` | 1/2 | 1/4 |
| `(1,+)` | 0 | 1/4 |
| `(1,-)` | 0 | 1/4 |

Thus an outcome-discarding check would certify an equality that is false for
the retained evidence. This is an immediate useful consequence of making
records part of the mathematical object. It is standard QM, not a new effect.
These same-system measurements must be ordered or treated as conflicting
operations, not declared physically independent because a graph omitted an edge.

An even stronger control starts from the maximally mixed state `I/2`. Both
schedules then give all four joint records probability `1/4`, but the final
state in each branch is an X eigenstate for Z then X and a Z eigenstate for
X then Z. Even complete joint outcome probabilities can therefore miss an
operator-level disagreement; the unnormalized quantum output blocks must also
be compared.

### 5.5 Bounded computational protocol to implement next

Start with fixed graphs, at most two qubits, four events and two outcomes per
event. Exclude dynamic graph growth, continuous outcomes and adaptive settings
from the first executable milestone; the general definitions above do not make
those features implemented.

1. Specify each instrument independently of the DET execution wrapper. Validate
   dimensions, finite entries, completeness and explicit record supports.
2. Use exact rational complex entries where possible. Z/X projectors, Bell
   density matrices and a damping instrument with Kraus coefficients `3/5`
   and `4/5` permit exact finite calculations.
3. Compare complete linear maps on an operator basis, or their Choi matrices,
   for each incomparable pair. For two qubits, 16 Pauli strings span the
   operator space. Retain every outcome block.
4. Enumerate every permitted schedule on the selected graphs and compare the
   full composite maps, not only Monte Carlo trajectories. Include entangled
   states as explanatory regressions, not as a replacement for map equality.
5. Keep the independent reference distinct from the code under test: direct
   tensor/Kraus composition versus the event-record executor, plus the worked
   analytic examples above. A second call to the same helper is not independent.
6. Include deliberately invalid controls: incomplete instruments, inconsistent
   one-sided swaps of fixed outcome labels, shared record writes, hidden nonlocal
   dependencies, and the Z/X counterexample. The verifier must reject the relevant
   false claim. Consistent relabeling on both sides is a valid coordinate change
   and must preserve the comparison after record-slot identification.
7. Report time, memory, exact arithmetic growth and the number of schedules and
   basis elements actually checked. Freeze numerical tolerances before any
   floating-point extension; do not turn near-equality into an exact theorem.

**Exit criterion:** an independently reviewed finite certificate and meaningful
negative controls, with all premises, bounds and differences preserved. A valid
counterexample narrowing the proposed condition is also a useful research
outcome. No change to a DET gate or physical claim follows automatically.

## 6. Useful structures to explore after QR-01

| ID | Question | Possible deliverable | Dependency / exclusion |
|---|---|---|---|
| QR-02 | Can classical outcome coarse-graining preserve composition and stated downstream questions? | Exact sum-over-outcomes maps; sufficient-record versus information-loss counterexamples | QR-01; do not sum amplitudes when merely forgetting a recorded outcome |
| QR-03 | Which past records can be forgotten without changing declared future predictions? | Bounded predictive-history summaries and counterexamples to scalar sufficiency | Explicit future instrument family; no universal scalar κ assumption |
| QR-04 | Can record-conditioned settings preserve causal-past restrictions and schedule independence? | Audited adaptive finite instruments on classical-quantum states | QR-01; no dependence on incomparable records; not yet RET integration |
| QR-05 | Can a coherent history model yield stable coarse-grained event relations? | A specified quantum-to-record-to-order mapping with refinement tests | QR-01/02; no claim that all graphs resemble spacetime |
| QR-06 | Can the same evidence structure improve quantum measurement planning? | Separately validated RET quantum adapter and matched-cost comparison | Stable reviewed RET API plus quantum likelihood and policy calibration |

These are questions, not six promised successes. Their value must be recorded:
clearer assumptions, stronger verification, fewer stored variables for a fixed
prediction task, measured computational improvement, or better measurement
decisions. Merely renaming a familiar object is not a demonstrated advantage.

The QR-03 connection may also be useful in materials and other systems with
memory: two histories matched on measured present variables can still imply
different future distributions. A history summary may be unnecessary, scalar,
multidimensional, or nontransferable. The result determines its scope; the
ontology does not determine the answer in advance.

## 7. Track-B geometry bridge: a separate conditional ladder

The retained [metric-as-record idea](track_b/gravity.md) motivates questions
about relations among events. It does not supply a new gravitational source.

There is mathematical precedent for reconstructing geometry from causal order
and volume information under appropriate continuum assumptions. Discrete event
counts stand in for volume only with an additional density/embedding model;
detector counts or the number of software records are not automatically
fundamental spacetime volume. [Surya, causal-set review](https://arxiv.org/html/1903.11544v2)

Useful bridge obligations are:

1. Specify what constitutes an event, record and precedence relation, and which
   elements are modeled versus reconstructed from instrument data.
2. Define a single compatible history/composition model. Attaching an unrelated
   quantum module to an unrelated geometry module is not a unification.
3. Show consistency when records or histories are grouped at different scales.
4. Test geometric estimators on known generating models and adversarial
   non-manifoldlike graphs without confusing recovery with emergence.
5. Only then ask whether the model selects a stable continuum geometry and
   what dynamics it supplies. Reproducing GR dynamics would be a further
   correspondence obligation, not an automatic consequence of an event graph.

Classical record-to-order feedback in the existing T8 program is an adjacent
question, not a prerequisite already solved by QR-01. Neither quantum schedule
independence nor classical birth-label independence establishes spacelike
locality, Lorentz covariance, or diffeomorphism invariance.

The route is compatible with retaining ordinary GR. No modification of the
Einstein equations, κ source, instantaneous gravitational action, or clock
coupling is proposed here. Physical novelty would be a different project.

## 8. Evidence record and next action

Each future study should retain:

- its question, version, date, scope and premise inventory;
- adopted mathematical results and precisely attributed DET contributions;
- exact models, settings, event order, record supports and expected controls;
- code/runtime/dependency identity, seeds if used, and computational bounds;
- an independent reference and the full discrepancy report, including failures;
- classification as analytical argument, exact finite verification, numerical
  test, synthetic simulation, or measured-data analysis;
- a specific usefulness claim and the evidence needed to support it;
- known limits and an explicit statement of what was not tested.

For measured work, add raw-source provenance, calibration and nuisance models,
selection rules, uncertainty budgets, held-out design and correction history.
Local hashes support integrity, not authentication of an experiment or physical
independence of its records.

**Next action:** review the QR-01 instrument/record contract, then implement only
its bounded reference and verification examples in isolated research files.
Do not wait for RET calibration to do this mathematics; do wait for the relevant
API and application gates before integrating it or claiming decision quality.

This document creates the research starting point. It does not report new
empirical results, certify complete quantum compatibility, or close G5.
