# Present activity, record formation and observation: a DET-wide audit

13 September 2026. **Initial audit: PROPOSED_SEMANTIC_REFINEMENT;
PARTIAL_ARCHITECTURAL_SUPPORT.**

**Implementation follow-through:** the owner subsequently authorized the
recommendations. [RECORD_PROCESS_CONTRACT.md](RECORD_PROCESS_CONTRACT.md)
records the adopted semantic convention, isolated experimental contracts and
legacy claim corrections. No new physical law or quantum-selection postulate
was adopted. The audit below preserves the evidence and gaps at the time of
the proposal; statements about the then-current source are historical.

This note evaluates the proposed distinction between present relational
activity, formation of a committed record, and subsequent observation of that
record. It records an architectural assessment and explicit mathematical
consequences. It does not adopt new global primitives, change executable laws,
or promote a Track-B interpretation to an observed fact.

## 1. Main finding

The proposed distinction is compatible with—and partly already present in—the
newer QR-MAP calculus. The core mathematical state there is
\(X=(C,\mathfrak D_C)\), not the committed record alone. The operational
completion expressly permits reversible processes on residual systems without
running the committed poset backward.

However, the current chosen growth law is commit-indexed, and older DET text
explicitly says that both record and state freeze between commits. The proposal
therefore does two different things:

1. It makes an existing state-versus-record distinction explicit.
2. It challenges a stronger, incompletely justified identification of all
   activity, event counting and committed-record growth.

The recommended research wording is:

> Record-time measures the ordering and growth of committed records. It has
> not been established that record growth exhausts present relational
> transformation. A residual state may contain distinctions absent from the
> currently accessible record, provided their meaning is specified through
> lawful future interventions and record probabilities.

This is not a theorem that an unobserved ontological substrate exists. It is
a refusal to infer state completeness from a record log that has not been
proved sufficient.

## 2. Three distinctions are needed, not just two symbols

Let

\[
C=(V,\prec,R_{\mathrm{comm}}),\qquad X=(C,\mathcal Z).
\]

Here \(R_{\mathrm{comm}}\) is the committed record included in a **declared
model scope**, while \(\mathcal Z\) denotes the current residual relational
state. Use \(\mathcal Z\) to avoid confusing this proposed state notation with
the Pauli operator \(\sigma_z\).

An observer's accessible record \(R_{\mathrm{acc}}\) is a third object. It can
be a restricted, delayed or noisy view of \(R_{\mathrm{comm}}\), under a
declared observation mechanism. It need not be a complete past-closed snapshot
of the underlying committed graph.

The proposed transitions are then distinct:

\[
\begin{aligned}
\text{Residual activity:}&\quad (C,\mathcal Z)\longmapsto(C,\mathcal Z'),\\
\text{Commit:}&\quad (C,\mathcal Z)\longmapsto
  (C\mathbin{\oplus}(e,r),\mathcal Z_r),\\
\text{Record access:}&\quad R_{\mathrm{acc}}\longmapsto
  R_{\mathrm{acc}}'\ \text{through an observation process}.
\end{aligned}
\tag{1}
\]

These classify functions, not mutually exclusive kinds of physical interaction.
Reading a detector can produce a new record at the reader; an interaction can
both change the residual state and create a record. A record may be committed
without ever being read by a human. Conversely, no new entry in a chosen
observer's log does not show that no record was formed elsewhere.

Append-only committed history is not a claim that every physical memory carrier
lasts forever. A carrier can change or become unreadable; that changes present
state or access without making the earlier event unoccur. Logical history,
current physical storage and an observer's evidence must remain distinguishable.

Consequently the following three assertions must remain separate:

- no new record accessible to this observer;
- no new committed record anywhere inside the specified model scope;
- no physical or relational transformation.

The first does not establish the second. Neither the first nor the second
establishes the third without an explicit exhaustivity premise.

## 3. Is the proposed live state already the pair-kernel?

The lowest-assumption starting point is

\[
\mathcal Z:=\mathfrak D_C
\]

together with its declared residual-system interface and available operations.
This is a clarification of the newer QR-MAP state, not a new hidden variable.
[QR-MAP](QR_MAP.md) already rejects \(F(C)\) as sufficient unless residual
reconstruction from \(C\) has been proved.

Two cases must not be conflated:

**The kernel is the complete operational residual state.** Differences that
alter an allowed future record distribution must already be represented in
that state. Merely adding a second name \(\mathcal Z\) does not add explanatory
content.

**The current kernel is only a restricted summary.** Additional apparatus,
environmental or memory structure may be needed. Then the proposal must state
which information the kernel loses, how the enlarged state evolves, and how
it changes predictions. The enlargement is a new mathematical hypothesis.

Neither version automatically supplies a pure-state space, a physical tensor
product, continuous reversibility or a unique quantum law. An arbitrary
strongly positive pair-kernel is not the same object as a completed quantum
operational theory.

### 3.1 Fixed law does not mean frozen state

The model-card shorthand \(L:R^-\to(\Omega,\Sigma,K,\mathcal C)\) is adequate
only when its record input, initial conditions and declared context suffice
for the predictions being claimed. If two reachable states have the same
complete input record and context but different future laws, this shorthand
must be enlarged or its sufficiency claim withdrawn.

A **fixed** rule may depend on the current residual state:
\(L(C,\mathcal Z;a)\), with \(a\) a lawful interaction/context. Updating
\(\mathcal Z\) does not itself change \(L\), just as a fixed transition rule
can act on different states. An external setting or hidden controller cannot
be omitted from the accounting simply to manufacture “identical records.”

### 3.2 Present equality is not future operational equivalence

For a declared family \(\mathscr T\) of allowed continuation experiments,
define

\[
x\sim_{\mathscr T}y
\quad\Longleftrightarrow\quad
P(t\text{ produces }r\mid x)=P(t\text{ produces }r\mid y)
\quad\text{for every }t\in\mathscr T,r.
\tag{2}
\]

Process comparisons also include allowed ancillary references. If some later
intervention distinguishes two states, they were not equivalent under this
full future-testing definition in the first place. They were merely identical
on the current record, or on a narrower question family.

Thus the precise QR lesson is: **equal current records need not identify the
same predictive state**. “Observational equivalence need not imply relational
identity” is valid for a stated restricted observation family. If every
possible allowed future test agrees, a further identity distinction is not an
established operational difference; it may be gauge or an interpretation.

This also rules out using an unobservable global quantum phase as an example
of consequential \(\mathcal Z\)-change. A relative phase must be defined
against a physical interference/readout context.

## 4. What quantum observation does—and does not—support

### 4.1 The double-slit analogue needs an overlap factor

For a pure path-marker model, the state reaching a screen has amplitudes
\(\psi_A(x)|m_A\rangle+\psi_B(x)|m_B\rangle\), where normalized marker states
can represent an apparatus or environmental degree of freedom. Ignoring the
marker gives

\[
P(x)=|\psi_A(x)|^2+|\psi_B(x)|^2+
2\operatorname{Re}\!\left[
\psi_A(x)\psi_B(x)^*\langle m_B|m_A\rangle\right].
\tag{3}
\]

Identical markers preserve the coherent cross term; orthogonal markers remove
it from this unconditioned screen distribution. At fixed coherent input and
readout geometry, a marker overlap of modulus strictly between zero and one
reduces the interference term correspondingly. This is physical correlation, not a requirement
for conscious observation. The visibility/which-way tradeoff is formalized in
[Englert's inequality](https://doi.org/10.1103/PhysRevLett.77.2154).

Two qualifications matter for DET. First, absence of accessible which-path
information does not guarantee visible fringes: phase averaging, source
incoherence and detector averaging can also suppress them. Second, an
orthogonal coherent marker does not by itself prove that a unique immutable
classical fact has been selected. A reversible path marker and a robust
macroscopic record are not identical constructions.

Quantum erasure can recover interference in suitably conditioned correlations;
it does not rewrite previously registered outcomes or change an already
unconditioned marginal through a later choice. See the primary
[double-slit quantum-eraser experiment](https://arxiv.org/abs/quant-ph/0106078).
The distinction between premeasurement, reduced-state decoherence and definite
outcomes is developed in
[Schlosshauer's review, §§II–III](https://arxiv.org/html/quant-ph/0312059).

Equation (3) is a **standard-QM correspondence model**, not a new derivation
of quantum laws from DET. It supports separating coherent transformation,
record formation and record access; it does not establish DET presentism or
define the fundamental commit boundary.

### 4.2 An exact conditional witness of silent residual change

Inside the explicitly assumed finite-QM completion, take

\[
\rho_+=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
U=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
\rho_-=U\rho_+U^*=\tfrac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
\tag{4}
\]

The transformation is reversible. The two states have the same computational-
basis probabilities \((1/2,1/2)\), but a subsequent effect
\(E_+=\rho_+\) gives probabilities one and zero. If \(U\) is admitted as an
unrecorded residual process relative to \(C\), it realizes the first line of
(1) and produces a later detectable difference.

In the existing compatible-kernel representation this is

\[
\mathfrak D\longmapsto
J_2\!\left(U\,J_2^{-1}(\mathfrak D)\,U^*\right),
\tag{5}
\]

on the specified image of \(J_2\). The
[operational-completion construction](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
already transports all such quantum processes there. Equation (5) does not
license arbitrary unitary conjugation of the unrestricted original kernel
matrix: its normalization is total-entry mass, not matrix trace.

This is an analytical compatibility witness. It does not prove that the
current \(L_{XYZ}\) autonomously performs \(U\) without a commit, nor that a
laboratory phase manipulation leaves every record in the universe unchanged.
The control apparatus and the meaning of “same \(C\)” remain part of the
specified scope.

### 4.3 A no-click interval is not necessarily a no-record interval

A detector's registered null result can carry information. If a monitored
interval has been defined and no click occurs, the conditional state may
change. An inefficient detector can also miss actual emissions. These are
different from neither monitoring nor creating any record in the model scope.
The quantum-trajectory literature explicitly treats conditional no-detection
evolution and detector inefficiency; see
[Plenio–Knight, quantum-jump review](https://arxiv.org/html/quant-ph/9702007).

Accordingly distinguish a zero-probability branch, a logged null outcome, an
unreported outcome, and a genuine no-append transition. The current
\(L_{XYZ}\) formal \(\bot\) branch is zero-probability bookkeeping, not a
mechanism for unrecorded relational evolution.

## 5. What the present repository actually supports

| Component | Evidence in this checkout | Assessment under the proposal |
| --- | --- | --- |
| Track-B present/record distinction | [ONTOLOGY.md §2](../../ONTOLOGY.md#2-the-primacy-of-the-present-radical-presentism) calls the record a trace; [record/person note](record_vs_person.md) rejects identity with the record | Supports nonreduction to records as an interpretation; does not supply silent dynamics |
| Pair-kernel architecture | [Record-kernel physics §3](../record_kernel_physics.md#3-the-missing-quantum-object-is-not-another-scalar) distinguishes pre-commit relational structure from ordinary probabilities | Already supports more information than a commit kernel or current record |
| New QR-MAP state | [QR_MAP.md](QR_MAP.md), full residual payload requirement | Already \((C,\mathfrak D_C)\), not record-only |
| Full operational completion | [RECONSTRUCTION.md §1](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md) separates residual reversibility from committed history | Conditional process calculus can express no-append residual transformations |
| Chosen event-growth law | Same reconstruction, explicit \(F_L\) and \(L_{XYZ}\) | Every realized growth step appends an event; no endogenous silent-process scheduler supplied |
| Older two-level propagator | [time_evolution.py](../../det8/models/time_evolution.py), `evolve_state` versus `discrete_evolution_sequence` docstring | Fixed-record algebraic evolution exists, but lines 130–132 explicitly assert that state freezes between commits |
| Classical record-redundancy model | [record_formation.py](../../det8/models/record_formation.py) | A concentration bound on already-assumed noisy commits; not a first-commit derivation |
| Apparatus-copying model | [det_native_measurement.py](../../det8/models/det_native_measurement.py), `TargetSystem` and `det_native_measurement_event` | Assumes a pre-existing binary target value and noisy copying; not a derivation of quantum observation |
| Time/count helpers | [det8_core.py](../../det8/models/det8_core.py), `proper_time_increment` and `accumulate_proper_time` | Enforce a chosen count-to-time formula; do not establish that count exhausts activity |
| Legacy mutable node state | Same module, `NodeRecord`, especially lines 93–120 | Stores current phase/coherence/material variables under a “record” name and updates them in place; it is not the same data structure as the immutable committed QR-MAP history |
| T7/order reconstruction | [gravity.md §§2–3](gravity.md) and [geometry plan](QR_MAP_RELATIVITY_GEOMETRY_PLAN.md) | Counts and causal order require an observational bridge; supplied geometry remains a fixture |
| RET | [RET_SDK.md](../RET_SDK.md), observation/missingness contracts | Already distinguishes evidence and inference; not a live-state dynamics engine |

This is a targeted DET-wide semantic audit, not a claim that every legacy file
has been reconciled. Global and concurrent edits have been left intact.

### 5.1 Record stabilization is not yet first-record formation

`record_formation.py` proves a standard majority-error concentration bound
given independent weak records with reliability \(p>1/2\). That is a result
about the reliability of an aggregate record after records already exist.
The module's prose connecting it to suppression of pair-kernel cross terms
does not implement a pair-kernel interaction or derive that suppression rate;
its own certificate notes the missing quantitative tie.

`det_native_measurement.py` is more explicit: `TargetSystem.value` is an
already committed binary fact. The apparatus copies it noisily. This is a
classical measurement/copying example, not a solution to selecting an outcome
from a coherent state without an assumed target value.

The proposal therefore reveals a central distinction in the old T3 language:

- formation of the first committed record from a residual process;
- amplification, copying and stabilization of an existing record;
- acquisition of that record by a later reader.

The present concentration result addresses the second. It cannot discharge
the first merely because both were called “record formation.” These source
files are not rewritten in this assessment.

## 6. Record-time: the proposed weakening is warranted

Record order and record count remain well-defined on the committed graph.
They do not automatically determine a duration or parametrize every residual
change. A partial causal order is also not a universal observer's clock.

The existing helper uses

\[
\Delta\tau_{\mathrm{model}}=\Pi\,\Delta N.
\tag{6}
\]

It is algebraically consistent. If \(N\) means committed-record count, then
\(\Delta N=0\) makes this *defined quantity* zero. The formula alone cannot
prove that every process is physically frozen during a no-record interval.
Conversely, redefining \(N\) to count silent transformations or underlying
activity would introduce a different counting object, not preserve
\(N=|V|\) by a change of words.

A silent-dynamics proposal therefore owes a specification of sequencing and,
if needed, duration. A relational interaction label, a local clock interface,
or a derived ordering might serve different purposes. None should be silently
identified with an external universal tick or preferred foliation. The
continuous parameter in a standard unitary correspondence example does not
solve this native time problem.

This refinement does not invalidate the numerical implementation of (6),
justify the deferred \(\kappa\)-clock prediction, or revive retired
\(\kappa\)-gravity. It limits the interpretation attached to a definition.

## 7. Geometry, missing records and delayed records

### 7.1 What QR-05 retains

QR-05A's payload-only fork/join failure and QR-05D's order-diagnostic blindness
remain valid for their stated objects. They never proved that every present
interaction must be a vertex in the retained graph. A record graph can be the
output of a richer process without invalidating either counterexample.

However, calling it a “shadow” is not yet a mathematical construction. One
must specify the process-to-record map and what it preserves. Until such a
map exists, **observation channel or restricted record image** is more precise
than asserting a quotient with unproved properties.

The two-port width obstruction also remains true for the actual
\(L_{XYZ}\) graph. Positing a richer latent process does not turn that graph
into a volume-filling spacetime. A geometric target assigned to an additional
latent object is a new target requiring its own construction and proof.

### 7.2 Thinning does not preserve all geometry

If a committed poset \(P\) is already given and only a subset \(S\) is
observed, its induced order is \(\prec\) restricted to \(S\times S\).
Relative order among retained comparable elements survives; counts and
interval contents do not. This assumes access to that induced order, which
an actual detector log does not automatically provide.

The cover graph must not be substituted for the order relation. In
\(a\prec b\prec c\), omitting \(b\) still leaves \(a\prec c\) in the induced
order. Deleting \(b\) from an edge list containing only \(a\to b\to c\)
and keeping no transitive relation would falsely make \(a,c\) unrelated.

For a fixed collection of actual candidate events and indicator \(I_v\) that
event \(v\) is retained, linearity alone gives

\[
\mathbb E[N_{\mathrm{obs}}]=\sum_v P(I_v=1).
\tag{7}
\]

Independence is not needed for (7), but is needed for the usual binomial
distribution and simple variance formula. If recording probability depends on
the live state, selection can change both spatial distribution and later
outcome statistics. Missingness cannot simply be called noise and ignored.

### 7.3 A precise count-to-volume ambiguity

As a **conditional comparison only**, suppose an underlying process were
Poisson with intensity \(\nu\,dV_g\) on a supplied geometry. Let independent
per-point recording/access retain a point with probability \(q(x)\). Then the
observed intensity is

\[
d\Lambda_{\mathrm{obs}}(x)=\nu q(x)\,dV_g(x).
\tag{8}
\]

This is the ordinary thinning model, not a DET generator. It illustrates the
identification problem even under unusually favorable assumptions. In spacetime
dimension \(d\), a smooth positive conformal change \(g'=a^2g\) preserves causal
order and changes volume to \(a^d dV_g\). Choosing
\(q'=q/a^d\), where both retention probabilities are admissible, preserves
(8). Under this model, the same observed order-and-count law can therefore
arise from different metric scales and recording efficiencies.

Thus unknown recording efficiency can obstruct metric reconstruction, not
merely make an estimator less precise. Constant known retention, unknown
constant retention, and state-dependent retention are different cases.
Fundamental record formation and instrument access must also be separated:
their probabilities multiply only under a stated conditional model.

The example establishes an ambiguity on supplied comparison structures. It
does not prove that a DET-native process is Poisson, manifoldlike or described
by either metric.

### 7.4 Delayed access is not delayed formation

If a record was already committed but is received later, its receipt event is
not the event it describes. A new receipt record can be appended with a
reference to an earlier event. The immutable history need not be edited.
The observer's inferred history can change as evidence arrives without the
underlying committed facts changing.

If record *formation itself* occurs after an underlying interaction, the
formation order need not simply be the interaction order restricted to a
subset. A formation/latency model is then required. Treating receipt order as
causal order, or inserting a late-discovered ancestor as an ordinary maximal
birth, would violate the existing licensed-G semantics.

No general robustness theorem for these alternatives is currently established.
They require a specified observation/formation map, not a generic missing-data
certificate or another inverse on an inserted mesh.

## 8. Effect on the new quantum-selection principles

The distinction makes the intended domain of the
[principle-selection research](../validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md)
clearer, but does not establish its unproved principles.

**No information without disturbance is one-way.** Proposed for the designated
residual-system theory, not universally for classical record registers,
identity-atomicity says
that an instrument whose discarded-outcome residual process is the complete
identity has only input-independent branch probabilities. It does not say
that every change must yield information or a new committed record. A silent
unitary is fully compatible with it. Nor does the principle forbid copying a
known classical record or leaving a particular eigenstate unchanged. Its
universal process identity, not the preservation of one state, does the work.
See [the operational theorem](https://arxiv.org/pdf/1907.07043).

**Local tomography concerns future tests, not current snapshots.** The
incompleteness of \(R_{\mathrm{acc}}\) does not refute local tomography. The
question is whether all allowed product-local tests distinguish joint residual
states. It is also not a justification for that postulate.

**Reversibility and energy observability get a better-defined target:**
residual transformations at fixed committed history, not reversal or deletion
of historical facts. This removes a possible conceptual obstacle to analyzing
continuous control, but does not derive continuity, a conserved observable
assignment, a Hamiltonian, or its scale.

**Purification and compression remain availability questions.** Allowing a
live state does not prove that pure joint preparations, ancillary systems,
or physical compressed face types exist.

An elementary classical counterexample makes this limitation explicit. Let a
hidden classical bit \(z\) change by \(z\mapsto1-z\) without changing the
current log, and let a later readout return \(z\). It satisfies the proposed
“same record, different future probabilities” criterion. Real quantum residuals
can also change silently, and a restricted catalogue still lacks its missing
types. **Live activity without a new record is not a uniquely quantum
selection principle.**

## 9. RET, materials and anomaly triage

The record/state distinction is already normal in inference: evidence is not
identical to the system being inferred. DET's
[predictive-history proposal](../record_kernel_physics.md#2-a-det-native-definition-of-κ)
already allows matched present measurements to hide different future-response
distributions. Such differences may reflect ordinary latent material state,
measurement context or unmodeled history, not a new field.

The RET preview explicitly retains observation provenance and missingness
reasons. Its documentation warns that projecting missing axes does not make
missingness ignorable. It is a bounded inference SDK, not a general latent
state-space evolution engine; the proposed \(\mathcal Z\) should not be
silently inserted into its schemas or likelihoods.

For later applications, the practical question is whether an apparent change
belongs to the specimen/process, to record formation, or to acquisition.
Materials may transform between samples; a quieter sensor need not imply a
less active material. Conversely, a lost or delayed acquisition need not imply
that a new physical mechanism is present. These are candidate nuisance/model
distinctions, not application results established here.

No RET modification, data collection, clock run or materials experiment is
started by this note.

## 10. Direct answers and proposed follow-through

| Research question | Current answer | Missing obligation |
| --- | --- | --- |
| Can the architecture represent evolution without immediate record formation? | Yes in the conditional residual-process calculus; not as a specified autonomous step of the chosen growth law | A native admissible silent-transition rule, with composition and sequencing semantics |
| Can later records depend on that evolution? | Yes conditionally; equations (4)–(5) demonstrate it | Reachability and physical/native justification of the actual interaction law |
| Is record-production efficiency variable? | It can be modeled; current copying fidelity, event production and detector retention are distinct quantities | Separate formation and access mechanisms; no universal efficiency law derived |
| Is order/geometry reconstruction robust to absent or delayed records? | Not in general; §§7.2–7.4 identify explicit losses and ambiguities | A declared formation/observation model and a theorem appropriate to its assumptions |

Recommended follow-through is a **semantic and theorem-level reconciliation**:

1. Fix the scope of committed versus accessible records; start with
   \(\mathcal Z=\mathfrak D_C\) unless a demonstrated insufficiency requires
   more state.
2. Specify what distinguishes a residual operation, a commit, a recorded null
   outcome and a receipt event. Determine how silent transformations are
   sequenced without importing a preferred global clock. If arbitrarily many
   silent steps are allowed, do not presume that another record occurs almost
   surely; termination/eventual-commit conditions need justification.
3. Separate the first-record problem from copying/stabilization. Keep the
   current redundancy result in its proved role and state the missing
   interaction/record-selection premises explicitly.
4. Apply the quantum-selection principles to the declared residual systems,
   retaining classical records and their legitimate copying operations.
5. Only after a formation/observation map is specified, state what geometry
   conclusions survive it. A named nonidentification or failed construction
   is a valid result; no new lettered QR-05 gate is needed.

Mass and gravity remain within the separately authorized research horizon.
This consideration makes the activity-to-record interface a dependency of
claims inferred from record geometry; it does not establish a matter–gravity
coupling or revive retired \(\kappa\)-gravity. Option B and Status M are not
promoted or silently replaced.

**Conclusion:** the proposed refinement improves the coherence of the
record-kernel program. Its strongest immediate consequence is to make
record sufficiency, record formation and observation explicit mathematical
questions. The next burden is not to assert that \(\mathcal Z\) is reality,
but to specify how its lawful transformations produce committed records and
which distinctions those records can preserve.
