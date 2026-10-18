# Explicit principles for selecting a quantum QR-MAP completion

## Executive findings

There are explicit, mathematically meaningful principles that exclude each of
the three countermodels in the QR-MAP hypothesis audit. The strongest candidates
are not claims about ontology. They concern which preparations, transformations,
composites and compressed systems actually exist.

The recommended distinction is between **countermodel exclusion** and
**reconstruction of the whole theory**. Continuous reversible control or
identity-atomicity excludes the full finite classical model. Local tomography
excludes the standard real-quantum composite. Physical face compression excludes
the powers-of-two-only system catalogue. These exclusions have short proofs
below; their conjunction is not presented as a new quantum reconstruction
theorem.

A published route avoids taking purification as an initial postulate:
Masanes–Müller's classification, with continuous reversible pure-state symmetry.
Its additional framework, subspace and measurement assumptions matter, and its
endpoint does not by itself specify measurement updates or the physical growth
law. The existing CDP reconstruction remains the stronger already-identified
reference for the full finite instrument calculus.[^1][^2]

The logical boundary is decisive. The current DET fragment admits the audited
countermodels. Therefore no search can produce a sound proof that this
*unchanged* fragment entails principles those models violate. A stronger
completion may be proposed and justified independently; it cannot be relabeled
an implication of the old premises.

**Research status:** explicit proposed selection principles and conditional
reconstruction routes identified; no new axiom adopted, no countermodel
withdrawn, no full DET-native QM, mass or gravity derivation claimed. This is a
literature-and-deduction report, not a new QR-05 gate or executor.

## 1. The mathematical target and the three obstructions

The source fragment, denoted \(B_D\), consists of finite committed snapshots
\(C=(V,\prec,R)\), maximal event append with an allowed past ideal, immutable
previous records, cardinality, and a fixed normalized forward rule \(L\).
A finite possibility carrier has a complex Hermitian biadditive kernel \(D\)
whose atomic matrix \(d\) is positive semidefinite and satisfies
\(\sum_{ij}d_{ij}=1\). An exactly decoherent partition \(\{A_r\}\) supplies
record probabilities \(D(A_r,A_r)\). Possibilities are not uncommitted future
vertices.

Even these kernel axioms are granted candidate premises, not consequences of
an ontological slogan. They yield a Gram representation and finite forward
record-marginal consistency. They do not declare a complete physical inventory
of preparations, operations, ancillary systems or composites. The
[formal local audit](../t8-q-hypothesis-justification-2026-09-13/JUSTIFICATION.md)
contains the source definitions and countermodel proofs.

For operational statements below, \(\mathcal S(A)\) is the convex normalized
preparation space of a declared residual-system type \(A\); \(u_A\) is its
discarding effect. A physical transformation is an available process, not just
a linear formula. A pure preparation is operationally extremal. Complete
equality of processes includes their behavior with every allowed reference
system and continuation experiment.

The three audited models are:

- **Full classical theory:** every finite simplex, every ordinary stochastic
  process and Cartesian composite; \(d_p=\operatorname{diag}(p)\). A pure joint
  classical state is a point mass, whose marginal cannot be a mixed bit.
- **Real quantum theory:** real symmetric density matrices, real quantum
  operations and ordinary real tensor-product composites. This fits the granted
  complex-valued kernel language, but some joint degrees of freedom are invisible
  to every product of local effects.
- **Restricted classical catalogue:** only simplexes with \(1,2,4,8,\ldots\)
  vertices, with all ordinary processes between available types. The
  three-vertex face of a four-state system exists as a subset, but no
  three-state residual-system type exists to realize its ideal compression.

The third model is deliberately about a different missing premise; it is also
classical and thus fails several nonclassicality principles. The three models
are not an independence proof for three axioms.

## 2. Exclusion map

Here “passes” means that the specified model satisfies the principle, not that
the principle proves that model correct. The quantum columns refer to the full
finite real theory and its conventional composites. Nonclassical control and
readout principles concern residual systems, not independently readable
classical record outputs.

| Explicit principle | Full classical | Real QM | Restricted classical catalogue | Main obligation |
| --- | --- | --- | --- | --- |
| Continuous reversible pure-state transitivity | Excluded | Passes | Excluded | Available continuous reversible control, not random interpolation |
| Identity-atomicity / no information without disturbance | Excluded | Passes | Excluded | Complete process equality, including reference correlations |
| Pure dynamically faithful process probe | Excluded | Passes | Excluded | A physically preparable pure joint probe |
| Purification of every preparation | Excluded | Passes | Excluded | Physical extension; uniqueness if the chosen theorem requires it |
| No universal broadcasting | Excluded | Passes | Excluded | Identity marginals as complete processes |
| Local tomography | Passes | Excluded | Passes | Product local effects separate all joint states |
| Physical face compression | Passes | Passes | Excluded | An actual compressed type and available encoder/decoder |
| Energy-observability assignment on nontrivial residual types | Excluded | Excluded | Excluded | Reversible generators and nontrivial conserved observables; see §7 |
| Pure conditioning or absence of third-order interference alone | Passes | Passes | Passes | Neither is a sufficient selection principle |

The entries follow from the witnesses below, the cited operational results,
and the standard models just defined. They are not a classification of all
generalized probabilistic theories.

## 3. Excluding the full classical completion

### 3.1 Continuous reversible controllability

**Proposed principle.** On each designated nontrivial residual system, any
two pure preparations are connected by a continuous path of available
reversible transformations, beginning at the identity. Continuity is measured
through operational probabilities. This is the nonclassicality condition in
Hardy's original continuity axiom; his reconstruction also requires substantial
probability, simplicity, subspace and composite assumptions.[^3]

**Exclusion proof for the audited model.** An affine automorphism of a finite
simplex permutes its vertices. Its reversible group is finite. A continuous
path from the identity in that group is constant, so it cannot connect two
different pure states. Reversible permutations without continuity do not
suffice. Real quantum theory survives: real pure states are rays and continuous
orthogonal rotations connect them.

**DET assessment.** This is an intelligible new control principle, but a fixed
\(L\) is not proof of it. Neither a continuously variable probability parameter
nor a convex mixture of two operations establishes reversible controllability.
Discrete event append does not logically prohibit a continuous family of
residual interventions, but it also does not supply that family. The domain
must not require undoing committed records.

### 3.2 Identity-atomicity: informative readout cannot leave the process intact

**Proposed principle.** For every designated residual system \(A\), every
physical instrument satisfies

\[
\sum_x T_x=I_A
\quad\Longrightarrow\quad
T_x=p_x I_A,\qquad p_x\geq0,\quad\sum_xp_x=1.
\tag{1}
\]

The identity in (1) is a complete operational identity, not equality on one
input. D'Ariano–Perinotti–Tosini prove the equivalence with their precise
no-information-without-disturbance condition, and show that real QM satisfies
it without local discriminability.[^4]

**Exclusion proof for the audited model.** On a classical \(n\)-state system,
the available branches

\[
T_i(p)=p_i\delta_i
\]

sum to the identity. They reveal the classical coordinate while preserving the
discarded-outcome state and ordinary reference correlations. No branch is a
constant multiple of the identity when \(n>1\). The same witness works in the
restricted catalogue, already on its bit.

**DET assessment.** This is the most direct candidate for a record-level
selection principle: a new informative record cannot be a refinement of an
otherwise unchanged residual identity process. But ordinary committed-record
access does not entail it. Imposing it universally on autonomous classical
record registers would forbid legitimate record copying. The scope must be
the residual systems claimed to have irreducible quantum information.

“Some measurements disturb,” “the old records stay fixed,” and “the present
record probabilities stay fixed” are all weaker, different statements. None
rules out the classical witness.

### 3.3 A pure faithful probe: a more constructive alternative

**Proposed principle.** For each residual type \(A\), there is a physically
preparable pure joint state \(\Psi_{AC}\) such that, for all allowed processes
\(T,S:A\to B\),

\[
(T\otimes I_C)\Psi=(S\otimes I_C)\Psi\quad\Longrightarrow\quad T=S.
\tag{2}
\]

This asks for one process-discriminating pure probe per type, rather than
starting by postulating purification of every mixed state. It is a sufficient
condition for identity-atomicity in the operational literature.[^4]

**Direct argument.** Apply an instrument summing to identity to the probe.
Its output branches sum to \(\Psi\). Purity makes each branch proportional to
\(\Psi\); faithfulness then gives (1). In the full classical theory, a pure
joint probe is \(\delta_i\otimes\delta_j\). Identity and reset-to-\(i\) agree on
that probe but not on other inputs, so no such probe exists. Real maximally
entangled preparations, however, are faithful for real quantum processes.

**DET assessment.** This gives a concrete construction to seek, not a proof
already obtained. A rank-one Gram vector is not necessarily an operationally
pure physical preparation. An injective matrix encoding of processes is not a
physically available process probe.

### 3.4 Broadcasting and reversible dilation: alternatives, not shortcuts

**No universal broadcasting** forbids a channel \(B:A\to AA\) whose two
marginal processes are both \(I_A\). Classical theory violates this through
\(B(p)=\sum_i p_i\delta_i\otimes\delta_i\). Do not substitute independent
cloning \(p\mapsto p\otimes p\), which is nonlinear and unavailable even in
ordinary classical probability theory. The generalized no-broadcasting theorem
of Barnum and colleagues assumes a finite convex framework, unrestricted
affine effects and local tomography in its composite-system setup. It is not
a theorem about unspecified DET composites.[^5]

**Pure reversible dilation** requires every channel to arise by adjoining a
physically pure environment, applying an available reversible process and
discarding an output environment. A fair-coin preparation defeats this in
classical theory: pure point masses remain point masses under reversible
evolution and marginalization. With the appropriate background and uniqueness
conditions, the operational dilation formulation is equivalent to purification;
it is not an independent derivation of that postulate.[^6]

In particular, storing all random branch labels in an expanded history is not
enough. A mixed classical environment can supply randomness, but that abandons
the pure-environment requirement doing the exclusion.

### 3.5 A recent counterexample to overclaiming

Rolino–Erba–Tosini–Perinotti construct a bilocal simplicial operational theory
with identity-atomicity, no information without disturbance and no complete
broadcasting. Its restricted dynamics and nonstandard composites are not the
full classical theory audited here. It can copy local states while failing
the stronger correlation-preserving broadcasting condition.[^7]

Thus (1) excludes the named classical completion; it does not alone establish
nonsimplicial quantum state geometry, local tomography or the complex field.
This 2025 result makes the distinction especially important.

## 4. Excluding the real-quantum completion

### 4.1 Local tomography is an explicit composition principle

**Proposed principle.** For every declared composite \(AB\),

\[
(e\otimes f)(\omega)=(e\otimes f)(\tau)
\ \text{for all local effects }e,f
\quad\Longrightarrow\quad \omega=\tau.
\tag{3}
\]

This is the local-distinguishability assumption used in the existing CDP
route. It restricts composites, not just the vocabulary used to describe
states.[^2]

**Explicit real-theory obstruction.** Set

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
W=J\otimes J,\quad \rho_\pm=(I_4\pm W)/4.
\]

Both \(\rho_\pm\) are normalized real positive matrices. For every pair of
real symmetric local effects \(E,F\),

\[
\operatorname{tr}[(E\otimes F)(\rho_+-\rho_-)]
=\tfrac12\operatorname{tr}(EJ)\operatorname{tr}(FJ)=0.
\]

The allowed global real effect \(Q=(I_4+W)/2\) nevertheless has probabilities
one and zero. Hence (3) excludes this precise real composite. The matrices
are the local audit's witness, not a new numerical experiment.

**DET assessment.** “All possible records define the state” does not imply
(3): all possible *joint* records may include the global \(Q\) outcome.
Replacing joint records by products of local record tests is the additional
assumption. Locality of event attachment, independent scheduling and
no-signalling do not establish it.

Complex entries in \(D\) do not exclude real QM: real-valued kernels are
complex-valued kernels. A ban on globally hidden record degrees of freedom
would be a substantive choice of composition law, not a notational consequence.

### 4.2 Is there an alternative to local tomography?

There are algebraic and dynamical selection routes, but none is assumption-free.
Within Jordan-algebra frameworks, a compatible composite with a genuine complex
qubit can force complex matrix algebras. The Barnum–Wilce result also uses
homogeneous self-dual structure, locally tomographic composites and suitable
factorization of the self-dualizing inner product. Its conclusion allows
complex quantum superselection sectors. A preinserted complex qubit
cannot justify DET's first complex qubit.[^8]

A different route connects continuous reversible generators to conserved
observable quantities, discussed in section 7. It is attractive for subsequent
energy and mass research but requires an explicit dynamics–observable principle,
not merely a scalar called energy.

### 4.3 Experimental exclusions have extra premises

Renou and colleagues' network result distinguishes complex QM from conventional
real-Hilbert-space models in a specified multiple-source scenario. Source
composition and independence assumptions are essential; the result is not a
bare prohibition on writing a theory with real numbers. Its linear witness
also tolerates shared classical source randomness; arbitrary unobserved source
entanglement is a different allowance.[^9]

Wu and colleagues report a 5.30-standard-deviation violation of the tested
real-theory bound with strict locality arrangements. Fair sampling remains an
assumption. This is evidence against a specified physical model, not an internal
DET theorem or an assumption-free choice of numerical coordinates.[^20]

The scope remains an active foundational discussion. A March 2026 preprint by
Hoffreumon and Woods proposes a real formulation and challenges the inference
from operational independence to product preparation.[^10] An April 2026
response by Renou and colleagues contests the proposed criterion, including
its behavior in fermionic theory.[^11] These recent interpretations are not
used here as settled reconstruction theorems.

For an internal DET derivation, neither an external network inequality nor an
independence convention can silently become a DET axiom. If empirical selection
is pursued separately, its source model, reference correlations and observable
interface must be stated. No such experiment is launched by this report.

## 5. Excluding the missing-system catalogue

### 5.1 Physical face closure, not just a smaller matrix

**Proposed principle.** For every nonempty relevant preparation face
\(\mathcal F\subseteq\mathcal S(A)\), an allowed residual type \(B\) and
physical encoder/decoder \(E:A\to B\), \(D_c:B\to A\) exist with

\[
D_c E\sigma=\sigma\quad(\sigma\in\mathcal F),\qquad
E(\mathcal F)=\mathcal S(B).
\tag{4}
\]

The images in (4) are normalized physical preparations. The symbol \(D_c\)
denotes decoding, not the pair-kernel. This is the lossless-and-efficient
content of ideal compression for the face, with the actual processes and
system type included.[^2]

**Exclusion proof.** In the restricted catalogue, take
\(\rho=(1/3,1/3,1/3,0)\). Its minimal face has three extreme points.
Equation (4) makes the encoder an affine bijection between this face and
\(\mathcal S(B)\): decoding is its inverse. Consequently \(B\) must have
exactly three pure classical states. No available type does. Cardinality of a
subset does not create the missing physical object.

**DET assessment.** A record label for the three outcomes, a rank-three matrix
or an abstract isomorphic vector space cannot discharge (4). Conversely, a
larger system that stores the three possibilities losslessly but has additional
unused preparations does not meet the efficiency requirement.

### 5.2 A filter does not create an output type

The restricted catalogue already permits

\[
P=\operatorname{diag}(1,1,1,0).
\]

This substochastic idempotent fixes the face and preserves every nonzero pure
output. It still has a four-state output type. Even the deterministic
idempotent
\(R(p_1,p_2,p_3,p_4)=(p_1+p_4,p_2,p_3,0)\) does not create a three-state
system unless its image is allowed to split as a physical object.

This is a recognized structural distinction. In sharp theories with
purification, pure physical face projectors can exist while faces are not
autonomous systems. The literature explicitly gives qubits-only theory as an
example that still lacks ideal compression.[^12] Hardy's filter-based
reconstruction likewise explicitly treats filtered outputs as new types;
that step must not disappear in a DET translation.[^13]

Restrict a proposed splitting rule to the intended faces. Splitting *every*
physical idempotent is stronger: splitting quantum dephasing adds an autonomous
classical system. Requiring continuous pure-state transitivity on every such
system would then reject that enlarged theory. This is another reason to
distinguish residual quantum systems from record registers.[^12]

## 6. Complete reconstruction routes and their actual endpoints

### 6.1 Recommended non-purification benchmark

Masanes–Müller work in a finite convex operational framework. Their requirements
are finite-dimensional capacity-two systems, local tomography, equivalence of
subspaces, reversible pure-state transitivity, and availability of all valid
bit effects. The last condition can be replaced by their perfect-
distinguishability alternative. The classification allows classical and complex
quantum structures; continuous transitivity removes the classical branch.
Subspace equivalence transfers measurements and reversible transformations,
and identifies equal-capacity types. It is stronger than (4). Their conclusion
explicitly leaves measurement update and the Schrödinger equation requiring
further assumptions.[^1]

**Application to QR-MAP:** use this as a complete published benchmark for a
proposed *kinematic operational* completion. Do not invoke its conclusion from
only “continuity + local tomography + face closure.” The extra type-uniformity,
effect-richness, finite-dimensionality and closure hypotheses must be verified
or declared. Selecting a state-space geometry is also not selecting the event
order law \(L\).

### 6.2 The existing full-instrument benchmark

The CDP route assumes its full finite operational framework and causality,
perfect distinguishability, ideal compression, local distinguishability, pure
conditioning and purification with essential uniqueness. Its endpoint includes
all finite complex density states and the completely positive trace-
nonincreasing transformations, not just a vector embedding.[^2]

The [existing conditional construction](../t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
already uses that route and transports its instrument calculus into compatible
kernel cones. This search does not invalidate it or make its premises derived.
Its arbitrary available instruments and its particular chosen \(L_{XYZ}\)
remain different levels of specification.

### 6.3 Information-unit and Hardy routes

Masanes and colleagues' later information-unit reconstruction combines
continuous reversibility, local tomography, universal reversible encoding in
generalized bits, and no simultaneous encoding of additional information once
a bit is perfectly encoded. The generalized bit must also have finite
tomography, all effects available and a nonproduct continuous reversible
interaction. These conditions identify multi-qubit structure and represent
existing systems within it.[^14]

Universal encoding is not autonomous face closure. A catalogue consisting only
of qubit composites can encode every system it contains while omitting a
stand-alone qutrit. Thus this route does not repair the catalogue issue simply
by introducing a “universal information unit.”

Hardy's later framework offers another complete route through sharpness,
information and tomographic locality, specified reversible permutability and
filter sturdiness. Its exact version matters: the nonclassical strengthening,
operational closure assumptions and filtered-system type construction cannot
be replaced by the assertion that a particular matrix filter works.[^13]

### 6.4 Why the three attractive principles are not enough to claim all QM

Even before classification of state spaces, missing background assumptions can
leave physical measurements underdetermined. Here is an explicit mathematical
example, offered only for the weak formulation **without closure under limits**.

Take all finite complex quantum state spaces and standard composites. Admit
the zero map, every channel, and selective CP maps \(T\) satisfying
\(0<T^*(I)<I\) in strict Loewner order. Instruments sum to a channel.
Every selective event has a permitted complement, for example
\(S(\rho)=\operatorname{tr}[(I-T^*(I))\rho]\tau\), with fixed normalized
\(\tau\). The strict upper bound is necessary: merely positive definite
\(T^*(I)\leq I\) could have a singular nonzero complement and fail to belong
to any permitted instrument.

These events are closed under finite mixing, tensor products, coarse-graining
within a test and composition: if \(S^*(I)\geq cI\), then

\[
(S\circ T)^*(I)=T^*(S^*(I))\geq cT^*(I)>0.
\]

For a selective event the complementary strict upper bound is preserved too;
compositions of channels are channels. A proper coarse-graining leaving a
nonzero complementary branch has effect strictly below \(I\).

All unitaries remain, so continuous reversibility holds. Strictly positive
effects span the Hermitian space, so local tomography holds. Every quantum
support face can be compressed and decoded by channels, so (4) holds.
Nevertheless, no nonzero outcome vanishes on any normalized state: sharp
projective tests and perfect distinguishability are absent.

For completeness, if \(V:\mathbb C^r\to\mathbb C^n\) is an isometry onto
the face support \(P\), available compression can be
\(E(\rho)=V^*\rho V+\operatorname{tr}[(I-P)\rho]\tau\), with fixed normalized
\(\tau\); decoding is \(D_c(\sigma)=V\sigma V^*\). These channels establish
(4), including efficiency, without adding a sharp instrument.

This example is an independent conditional construction, not a counterexample
to the cited compact reconstruction frameworks. Its effects are not closed
under limits. Closing them restores the missing sharp effects. It demonstrates
why an omitted framework hypothesis cannot be dismissed as terminology.

## 7. Energy observability and the mass/gravity horizon

Another route starts from spectrality and symmetry of distinguishable pure
frames. Barnum–Hilgert classify strongly symmetric spectral compact convex
state spaces as simple finite Euclidean Jordan state spaces or simplexes.
These assumptions still permit real and other alternatives; they do not by
themselves choose complex QM.[^15]

**Proposed energy principle.** A designated nontrivial residual type has a
nonzero reversible-generator Lie algebra \(\mathfrak g_A\) and an injective
linear assignment

\[
\phi:\mathfrak g_A\longrightarrow V_A^*,\qquad \phi(X)\circ X=0.
\tag{5}
\]

For \(X\ne0\), \(\phi(X)\) must not be conserved by *all* reversible dynamics.
Barnum–Müller–Ududec's Definition 30 makes this precise; Theorem 31 combines it
with their state-space postulates to select complex quantum states and all
\(SU(N)\) conjugations. This is a single-system result, not a full instrument
or composite reconstruction.[^16]

**Exclusion:** the rebit's nontrivial continuous disk rotations conserve only
constant affine observables, violating (5)'s nontriviality requirement. Finite
classical simplexes have no nonzero continuous reversible-generator algebra.
Thus this principle excludes both audited theory families without relying on
local tomography for those exclusions. The full classification still needs its
additional hypotheses.[^16]

**DET research assessment.** This is a promising direction to examine alongside
mass-bearing dynamics because it asks what makes a generator physically
observable. But stable record weights, event counts and a fixed \(L\) do not
automatically define a reversible one-parameter group, an energy observable or
an energy scale. In particular, a numerical eigenvalue of an inserted operator
is not yet an inertial mass.

Mass, matter–geometry coupling and gravitational dynamics remain authorized
research objectives under the [expanded plan](../../track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md).
No reconstruction package above supplies a manifold-producing \(L\), a
count-to-volume theorem, spacetime translations, a mass spectrum or Einstein
dynamics. They can constrain a future joint model but do not produce it.

The existing two-port \(L_{XYZ}\) still has the separately proved width-two
obstruction to a dense, order-faithful, spatially extended continuum role.
Changing a purification premise cannot change that combinatorial fact.
The primitive-input test continues to distinguish derived structures from
inserted geometry, amplitudes or dynamics used only for correspondence checks.
This does not reinstate a blanket ban on investigating gravity or mass.

## 8. Record-sequence and amplitude reconstructions

These are especially relevant to QR-MAP's language, but not a shortcut around
the operational gaps. Goyal–Knuth–Skilling's original reconstruction starts
with a real-number pair assigned to each measurement sequence, together with
consistency conditions leading to complex amplitude rules.[^17] That pair
postulate is not the statement that \(D(A,B)\) has two event arguments.

Goyal's subsequent route starts from Feynman's rules and a particular
no-disturbance postulate; composite amplitudes and the amplitude–action rule
require additional assumptions.[^18] This no-disturbance condition must not be
confused with identity-atomicity in (1).

A newer composition-algebra analysis removes the initially fixed
two-dimensional amplitude space and carefully separates model axioms from
representation choices. Its admissible algebraic alternatives include
quaternionic and split forms; it does not uniquely select complex quantum
theory from sequence composition alone. It also identifies remaining assumed
regularity/algebraic properties.[^19]

**DET assessment.** Sequence composition can organize a candidate calculus.
Before calling it native, one must justify the amplitude representation,
probability map, regularity, scalar structure and realizable interventions.
An algebra allowing complex arithmetic is not a theorem that all and only
physical preparations or instruments are complex quantum ones.

Absence of third-order interference is likewise insufficient here: diagonal
classical kernels and real quantum probabilities already have that property.
Neither this absence nor familiar quadratic formulas remove the countermodels.

## 9. Recommended research decision

The search supports a concrete choice of proof targets, not automatic adoption
of a longer list of postulates.

**First, fix the operational domain.** Declare residual types, preparable
states, available tests, composites, references, mixing and closure under
limits. State separately how committed classical records are represented.
Do not identify all PSD pair-kernels with physical states by default.

**Second, choose a nonclassicality principle to justify.** Identity-atomicity
is the most direct record-facing candidate. A pure dynamically faithful probe
would establish it constructively. Continuous reversible pure-state control
is the clearest alternative and aligns directly with a published
non-purification reconstruction. These are alternatives for analysis, not a
claim that all are independent or minimal.

**Third, address composition explicitly.** Local tomography is the most direct
exclusion of the audited real composite. Give a reason why local record
continuations suffice for every joint residual preparation, or retain it as a
proposed physical-composition axiom. “All records are retained” is not that
reason. An energy-observability alternative requires its own complete theorem
environment.

**Fourth, address physical type closure.** Establish actual lossless efficient
face encoders/decoders. If using Masanes–Müller, also provide the stronger
subspace/equal-capacity operational equivalence and its remaining framework
and effect assumptions. A filter image alone does not suffice.

**Finally, select the desired endpoint.** For a non-purification derivation of
quantum state/effect/reversible structure, use the complete Masanes–Müller
benchmark. For a full finite instrument theory, keep the explicit CDP benchmark
or prove the missing instrument-availability result separately. Neither choice
selects the native record-growth law or completes the mass/gravity program.

The next mathematical deliverable, if pursued, should be a premise-to-theorem
argument on this declared operational domain: either a proof from genuinely
stronger, independently stated record principles, or an explicit failure of
that proposed implication. It should not be another finite fixture certificate,
an inverse of an inserted operator, or a new lettered QR-05 gate.

The admissible conclusion today is therefore precise: **the countermodels can
be excluded by explicit additional principles; the current DET premises do
not yet force those principles.** Their exclusion would strengthen a conditional
completion, not retroactively validate an ontological claim.

## Sources

The numbered references identify primary papers and the portions supporting
the associated claims. The finite witness calculations and DET translations
above are deductions applied to the local audited models, not claims of new
literature reconstruction theorems. Recent preprint disputes are separated
from established conditional results.

[^1]: L. Masanes and M. P. Müller, *A derivation of quantum theory from physical requirements*, New Journal of Physics 13, 063001 (2011). [Primary text](https://arxiv.org/html/1004.1483v4), §§II–III, Theorem 6, §V and Appendix Lemma 9. State-space classification, complete assumptions and explicit update/dynamics limitations.

[^2]: G. Chiribella, G. M. D'Ariano and P. Perinotti, *Informational derivation of Quantum Theory*, Physical Review A 84, 012311 (2011). [Primary text](https://arxiv.org/html/1011.6451v3), §§II–III; ideal-compression lemmas; Theorem 20 and Corollary 52. Full operational premise package and finite state/transformation endpoint.

[^3]: L. Hardy, *Quantum Theory From Five Reasonable Axioms* (2001). [Primary paper](https://arxiv.org/abs/quant-ph/0101012), axioms and §§6–8. Continuity, subspaces, simplicity and composite parameter assumptions.

[^4]: G. M. D'Ariano, P. Perinotti and A. Tosini, *Information and disturbance in operational probabilistic theories*, Quantum 4, 363 (2020). [Primary paper](https://arxiv.org/pdf/1907.07043), Definitions 14–16, Theorem 1, Corollary 2 and Proposition 10. Identity-atomicity, faithful probes and real-theory qualification.

[^5]: H. Barnum, J. Barrett, M. Leifer and A. Wilce, *A Generalized No-Broadcasting Theorem*, Physical Review Letters 99, 240501 (2007). [Primary text](https://arxiv.org/html/0707.0620), operational framework, joint-system clause (iii), Theorems 1–3. Framework restrictions are part of the result.

[^6]: G. Chiribella, G. M. D'Ariano and P. Perinotti, *Probabilistic theories with purification*, Physical Review A 81, 062348 (2010). [Primary paper](https://arxiv.org/pdf/0908.1583), background assumptions, Definition 46, Theorem 15 and Corollary 23. Reversible dilation and purification equivalence.

[^7]: D. Rolino, M. Erba, A. Tosini and P. Perinotti, *Minimal operational theories: classical theories with quantum features*, New Journal of Physics 27, 023004 (2025). [Primary paper](https://arxiv.org/pdf/2408.01368v4), Theorem 7, Corollaries 9–11 and §VIII. Bilocal simplicial counterexample and complete-versus-local broadcasting distinction.

[^8]: H. Barnum and A. Wilce, *Local tomography and the Jordan structure of quantum theory*, Foundations of Physics 44, 192–212 (2014). [Primary paper](https://arxiv.org/html/1202.4513), §1.4 Proposition 1 and §§2–3. Jordan, qubit and composite assumptions; superselection sectors allowed.

[^9]: M.-O. Renou and colleagues, *Quantum theory based on real numbers can be experimentally falsified*, Nature 600, 625–629 (2021). [Primary paper](https://arxiv.org/abs/2101.10873). Real-versus-complex network separation with specified source/composition assumptions.

[^10]: T. Hoffreumon and M. P. Woods, *Quantum theory based on real numbers cannot be experimentally falsified*, arXiv:2603.19208v1 (19 March 2026), preprint. [Primary paper](https://arxiv.org/html/2603.19208v1), Theorems 1–2 and C.1. Changed source-independence allowance; not settled adjudication.

[^11]: F. Moradi Kalarde, X. Xu and M.-O. Renou, *Comment on “Quantum theory based on real numbers cannot be experimentally falsified”: On the compatibility of physical principles with information theory for fermions*, arXiv:2604.07425v1 (8 April 2026), preprint. [Primary paper](https://arxiv.org/html/2604.07425v1), §2. Fermionic independence comparison; no general equivalence theorem is invoked here.

[^12]: H. Barnum, C. M. Lee, C. M. Scandolo and J. H. Selby, *Ruling out higher-order interference from purity principles*, Entropy 19, 253 (2017). [Primary paper](https://arxiv.org/pdf/1704.05106), §4, Propositions 5.6–5.7, §§5.4 and 6. Face projectors, idempotent splitting and the qubits-only compression obstruction.

[^13]: L. Hardy, *Reformulating and Reconstructing Quantum Theory* (2011). [Primary paper](https://arxiv.org/pdf/1104.2066), background assumptions, postulates, §§9.5 and 10.5–10.7, especially T38–T40. Filter sturdiness, physical output types and capacity closure.

[^14]: L. Masanes, M. P. Müller, R. Augusiak and D. Pérez-García, *Existence of an information unit as a postulate of quantum theory*, PNAS 110, 16373–16377 (2013). [Primary text](https://arxiv.org/html/1208.0493v2), §§III–IV and Appendices C–D. Bundled information-unit premises and encoding endpoint.

[^15]: H. Barnum and J. Hilgert, *Spectral Properties of Convex Bodies*, Journal of Lie Theory 30(2), 315–344 (2020), manuscript titled *Strongly symmetric spectral convex bodies are Jordan algebra state spaces*. [Primary manuscript](https://arxiv.org/html/1904.03753), Theorem 1.1 and §10.1; [published article](https://jolt.centre-mersenne.org/articles/10.5802/jolt.1118/). Jordan classification without a separate higher-order-interference postulate.

[^16]: H. Barnum, M. P. Müller and C. Ududec, *Higher-order interference and single-system postulates characterizing quantum theory*, New Journal of Physics 16, 123029 (2014). [Primary paper](https://arxiv.org/html/1403.4147), §VI Definition 30 and Theorem 31. Energy observability and single-system selection.

[^17]: P. Goyal, K. H. Knuth and J. Skilling, *Origin of Complex Quantum Amplitudes and Feynman's Rules*, Physical Review A 81, 022109 (2010). [Primary paper](https://arxiv.org/abs/0907.0909). Measurement sequences, the real-pair premise and amplitude rules.

[^18]: P. Goyal, *Derivation of Quantum Theory from Feynman's Rules*. [Primary paper](https://arxiv.org/abs/1403.3527). Feynman-rule starting point, a specific no-disturbance postulate, and extra composite/amplitude–action premises.

[^19]: J. Köplinger, M. Habeck and P. Goyal, *Operational reconstruction of Feynman rules for quantum amplitudes via composition algebras*, International Journal of Theoretical Physics 65, 128 (2026). [Primary text](https://arxiv.org/html/2508.14822v3), §§5.4–5.6 and 6.1; [publication record](https://researchconnect.suny.edu/en/publications/operational-reconstruction-of-feynman-rules-for-quantum-amplitude/). Remaining algebraic alternatives and explicit assumption audit.

[^20]: D. Wu and colleagues, *Experimental Refutation of Real-Valued Quantum Mechanics under Strict Locality Conditions*, Physical Review Letters 129, 140401 (2022). [Primary paper](https://arxiv.org/html/2201.04177v2), main inequality/result and supplementary §4. Experimental significance and retained fair-sampling assumption.
