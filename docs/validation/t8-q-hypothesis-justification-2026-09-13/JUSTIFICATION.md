# QR-MAP hypothesis justification: what DET entails and what it does not

13 September 2026. **PARTIAL_DERIVATION; FULL_PACKAGE_NOT_ENTAILED.**

The owner requests formal justification of the operational hypotheses from DET,
followed by a relativity/geometry plan. The result is not six successful proofs:
the current declared premises admit countermodels to the proposed package.
Consequently a proof of that entire package from those unchanged premises
cannot be supplied. This is a mathematical obstruction, not merely an unfinished
search. The earlier [conditional reconstruction](../t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
remains correct and conditional.

Here “formal” means explicit premises, deductive proofs and countermodels.
The accompanying exact arithmetic checks are not Lean verification. No Lean
project, new global axiom, physical experiment or geometry executor is created.

## 1. Fix the source theory before making an implication claim

The [MODEL_CARD primitives](../../../MODEL_CARD.md#2-primitives),
[pair-kernel proposal](../../record_kernel_physics.md#31-proposed-pair-kernel)
and [licensed QR-MAP](../../track_b/QR_MAP.md) supply the following relevant
mathematical premises. We call their finite record-growth fragment B_D:

1. C=(V,≺,R) is a finite committed marked poset at each snapshot; a birth
   appends a fresh maximal event with an allowed committed ideal as its past.
   Previous records and relations are unchanged. Counting is cardinality.
2. L is a fixed rule using the permitted past and retained residual data.
   Its joint precursor/action/outcome transitions are normalized and nonnegative.
   Incomparable-birth covariance, when claimed, concerns full transitions,
   not just supports or scalar weights.
3. A finite possibility carrier Ω, distinct from future event vertices,
   has a complex Hermitian biadditive pair-kernel D. Its atomic matrix d is
   positive semidefinite and its total-entry mass is one.
4. A declared **exactly** decoherent partition P={A_r} gives commit weights
   K(r)=D(A_r,A_r). Approximate decoherence is not silently treated as exact.

D is still a candidate premise in the source theory. We grant it here to make
the attempted implication as strong as these declarations permit. A theorem
not entailed even after granting D cannot follow from the weaker record/order
grammar alone. Status-M interpretations are not extra mathematical axioms.

The source theory does **not** declare that every PSD kernel is physically
preparable, every linear map is realizable, every subsystem split exists, or
every residual state admits a pure physical extension. Mathematical finite
matrix spaces do not by themselves supply physical convex mixing, operational
closure, ancillary tests or preparation-independent system types.

The previous note additionally assumed the full CDP operational framework and
six postulates. Their exact meanings remain those of
[CDP sections II–III](https://arxiv.org/html/1011.6451v3#S3), not weakened DET
synonyms. In particular, purification requires physical existence and
reversible uniqueness; local distinguishability requires product tests to
separate joint states. The question is whether B_D forces those assumptions,
not whether standard QM satisfies them.

## 2. Positive theorem: complete future tests preserve committed marginals

**Premises.** A finite recorded prefix h has weight w(h). Two possible future
test procedures t and t′ use only data available at their execution and have
complete normalized kernels at each subsequent branch. They do not change the
preparation or the rules that already produced h. Future procedures may be
adaptive. Sum over all their outcomes; do not postselect.

**Theorem.** For any fixed finite number k of later steps,

\[
\sum_{f:\,|f|=k} P_t(h,f)=w(h)=\sum_{f:\,|f|=k}P_{t'}(h,f).
\tag{1}
\]

**Proof.** At a leaf the remaining continuation mass is one. Backward induction
replaces each sum over next branches by Σ_β K(β|h)=1. Applying this k times
leaves precisely w(h). Adaptive choices merely choose another normalized
kernel at an intermediate node, so the same induction applies. For bounded
early stopping, a terminal record may be represented by an absorbing branch
of weight one. This proves the finite statement. ∎

This is genuine forward record-marginal consistency. In an additional typed
operational completion whose tests are all realized by these complete
procedures, it supplies the no-future-test-dependence part of operational
causality. If states span the operational vector space, any two deterministic
effects agree on every normalized preparation and therefore on that span.
This gives uniqueness there, conditional on that operational interpretation.

Acyclicity alone is insufficient: the proof also uses normalized forward
kernels and exclusion of future-test data from the prefix law. Conditioning on
a selected future result can change P(h|result) without violating (1).
No unbounded stopping theorem, infinite-history measure or spacetime
no-signalling theorem is asserted.

## 3. Countermodel theorem: purification is not forced

Consider the full finite **classical** operational model. An n-valued residual
system has preparations p in the probability simplex; effects have entries in
[0,1]; processes are substochastic matrices; complete tests sum to a stochastic
map. Composites have ordinary joint distributions on Cartesian products.

For a preparation p set

\[
D_p(A,B)=\sum_{i\in A\cap B}p_i,\qquad d_p=\operatorname{diag}(p).
\tag{2}
\]

These kernels satisfy every pair-kernel condition in B_D, including strong
positivity as **complex-valued** kernels. Every classical test produces
normalized recorded outcomes and residual classical states, which have the
same form (2). A fixed protocol can be executed by a fixed lookup rule L
using past control records and appending a chain of committed events. All
ideals are legitimate, past records remain intact and covariance on that
chain is vacuous. Independent classical tests can also be appended on disjoint
ports with commuting transitions if a nontrivial incomparable example is wanted.
Thus this is a compatible operational completion, not merely one isolated d.

**Theorem.** This model satisfies B_D but the mixed bit p=(1/2,1/2) has no
pure classical purification, of any finite environment size.

**Proof.** The extreme normalized preparations of any finite classical joint
simplex are point masses δ_(i,e). Every such preparation has marginal δ_i,
which is pure. Therefore no pure joint preparation can have marginal
(1/2,1/2). A correlated joint distribution such as
q(0,0)=q(1,1)=1/2 does have that marginal, but q is a nontrivial mixture
of two distinct point masses and is not pure. This works for every finite
environment, without enumerating environment sizes. ∎

Therefore B_D does not entail purification, and consequently does not entail
the full six-postulate package. Requiring some interference would exclude this
classical example, but interference is not itself a purification proof.

**Why Gram factorization does not repair this.** Factoring d=VV† creates
vectors in a mathematical space. Writing √p_0|0,0⟩+√p_1|1,1⟩ in an
enlarged complex space would give a quantum purification, but that preparation
is not in this model's classical state simplex. Admitting it changes the
physical preparation set. Neither the availability of such a vector nor a
“complete relational description” proves that this new joint preparation and
its reversible transformations are allowed by L.

## 4. Countermodel theorem: interference does not force local tomography

Use real quantum operational systems as a second admissible alternative:
real symmetric PSD density matrices, real effects and real completely positive
instruments, with real tensor-product composites. Such instruments generate
ordinary positive record probabilities. Their finite history kernels
D_ij=Tr(ρ h_iᵀh_j) are real and strongly positive, hence also admissible
complex-valued D. This is a **countermodel representation**, not a proposed
Hilbert-space input to a DET derivation.

For two two-level real systems, set

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
W=J\otimes J,\qquad
\rho_\pm=\frac{I_4\pm W}{4}.
\tag{3}
\]

W is real symmetric, W²=I and Tr W=0. Thus ρ_± are normalized PSD
matrices with eigenvalues 0,0,1/2,1/2. For any real symmetric local effect E,
Tr(JE)=0: transposing the trace changes its sign. Hence, for every product
effect E⊗F,

\[
\operatorname{Tr}[(\rho_+-\rho_-)(E\otimes F)]
=\tfrac12\operatorname{Tr}(JE)\operatorname{Tr}(JF)=0.
\tag{4}
\]

But the legitimate **joint** real effect Q_+=(I+W)/2 gives
Tr(ρ_+Q_+)=1 and Tr(ρ_-Q_+)=0. The joint states differ operationally,
while all local product statistics agree. This is a deductive failure of local
tomography. The local symmetric matrix space has dimension three; its products
span nine dimensions, whereas the joint symmetric matrix space has dimension
ten. W supplies the missing direction.

This well-known real-quantum obstruction is derived explicitly here; see also
the discussion of real quantum theory in the authors' operational reconstruction
[review, local tomography](https://arxiv.org/html/1506.00398v1).
The conclusion is narrower than an independence theorem for every CDP axiom:
the admitted pair-kernel and composition conditions do not exclude this model.
Complex codomain, nonzero off-diagonal kernels, normalization and schedule
covariance are therefore not enough to establish local tomography.

For an entirely explicit normalized history representation of these states,
use the product Walsh frame in J_4 from the preceding reconstruction note.
Equation (1) of that note gives 16×16 strongly positive real kernels with a
specified inverse. It is a faithful coordinate encoding of the countermodel,
not a change of its restricted real local effect set. Availability of extra
complex local effects would be an additional physical assumption.

For completeness, the exact commit rule is realized for any complete real
instrument by preparing the branch-tagged kernel

\[
D_{\rm pre}((x,z),(y,w))
=\delta_{xy}\,[J_m(\Phi_x\rho)]_{zw}.
\tag{5}
\]

Its blocks are PSD, its total mass is one and its exactly decoherent x-partition
has weights Tr Φ_xρ. A positive commit retains the corresponding normalized
residual block and appends a record. This verifies the full record-partition
rule, not only positivity of Born probabilities. Residual J_n(ρ) and the
new precommit carrier are different objects; no claim that fixed Boolean
partitions of one residual kernel realize every POVM is needed.

## 5. Countermodel theorem: ideal compression needs available system types

Restrict the classical operational model to residual systems with cardinalities
1,2,4,8,…, keeping all stochastic/substochastic transformations between
available systems, all preparations and ordinary Cartesian composites.
Products remain within this family. All states and record kernels still have
the diagonal form (2). Classical outcome labels are not automatically new
residual system types.

On a four-state system, p=(1/3,1/3,1/3,0) has refinement face Δ_3,
the entire simplex supported on its first three entries. Suppose it admits
ideal compression by allowed encoding E into an available system B and
decoding T, with exact recovery T E σ=σ on that face and efficient image
E(Δ_3)=St_1(B).

For normalized σ in the face, substochasticity gives

\[
1=u_A T E\sigma\le u_B E\sigma\le1.
\]

Thus encoding succeeds with probability one on the face even if it is not
globally deterministic. Its affine restriction is injective because T is a
left inverse, and it is onto the full normalized state space of B by efficiency.
Hence Δ_3 and St_1(B) are affinely isomorphic. Their dimensions must agree:
2=|B|−1, requiring |B|=3. No such system is available. This contradiction
proves failure of ideal compression. Postselecting and renormalizing would
change the exact losslessness requirement, not repair the proof. ∎

The lossless/efficient meaning used here is the operational one, as formalized
in [CDP sections III.1.3 and IV.1](https://arxiv.org/html/1011.6451v3#S3.SS1.SSS3).
Constructing a three-dimensional Gram support or a three-outcome record does
not produce the missing physical residual type and its allowed maps.

## 6. Account for every proposed hypothesis without overstating independence

| Proposed ingredient | Justification available from current declarations | What remains unproved |
| --- | --- | --- |
| Full finite operational framework | Finite carriers and composable record procedures in specified models | Common system types, physical mixing, closure, ancillas and all required wiring |
| Causality | Finite forward-marginal theorem (1) | Application to every test in a fully specified operational completion |
| Perfect distinguishability | Committed record labels are distinguishable by the declared readout | Zero-error tests for every non-completely-mixed operational preparation |
| Ideal compression | Not entailed: restricted-system classical countermodel in section 5 | A physically allowed efficient encoding/decoding of every refinement face |
| Local distinguishability | Not entailed: real-quantum countermodel (3)–(4) | A principle excluding locally invisible joint information |
| Pure conditioning | Rank-one same-carrier restriction lemma below | Operational purity and local conditioning on physical composites |
| Purification | Not entailed: classical countermodel (2) | Pure joint preparations and reversible uniqueness for every mixed state |

**Rank-one restriction lemma.** If d=vv† and E_A is an indicator cut, then
E_A d E_A=(E_Av)(E_Av)†. Whenever its total mass is positive, normalizing
leaves rank one. This proves a fact about mathematical same-carrier cuts,
not CDP pure conditioning on one part of a composite. In the compatible J_n
representation, a pure physical state has history-kernel rank n, not generally
one; identifying these two meanings of purity would be incorrect.

Likewise, an allowed noisy bit readout can have probabilities 1/4 and 3/4
on its two endpoint preparations while satisfying every proper-kernel condition.
Normalization does not force this menu to include a zero-error test. This is
a **limited-menu witness**, not a claim to have constructed a complete,
norm-closed operational countertheory to the entire distinguishability axiom.
Taking operational limits or enlarging the menu can change that question.

Rows without a dedicated countermodel are reported as missing proof obligations,
not as independently disproved axioms. The complete countermodels already
rule out deriving the whole package from B_D. None rules out a stronger DET
theory with additional precisely stated principles.

## 7. What an actual stronger justification would have to accomplish

Rewording a hypothesis as “relational completeness” does not derive it.
A successful stronger argument must supply all of the following, with provenance:

1. An operational interpretation defining preparations, effects, transformations,
   composites and physical equivalence from specified DET record procedures.
2. A precise new selection principle or an overlooked existing axiom, together
   with a proof that the classical and real countermodels violate it.
3. Proofs of physical preparation/operation existence, not only mathematical
   factorization, PSD completion or arbitrary enlargement of the allowed maps.
4. For purification specifically: an allowed pure extension of every mixed
   preparation and a reversible comparison of any two extensions on the same
   environment. For local tomography: separation by product tests, not the
   definitional separation by **all** possible global records.
5. A final implication with every premise marked existing, new, or imported.
   If new principles are necessary, the result must remain a theorem of that
   strengthened theory, not retroactively of the old one.

This identifies the exact missing work. It does not assert a minimal axiom
count or automatically adopt the previous six as physical truths. Empirical
motivation could justify a physical axiom choice, but would not turn that choice
into an internal derivation from weaker premises.

## 8. Verification and handoff

The standalone [witness checker](check_witnesses.py) checks displayed finite
arithmetic, not the universal statements by enumeration. **5/5 tests pass**
in normal and optimized Python; Ruff lint and formatting checks pass. Source
SHA-256: `136500400e32c676a10576f1bf92fec8696f16b3fa8d20ec54bfef7921f1b877`.
The checks include all nine real product-basis probes, 25 actual product
effects, the explicit J_4 PSD factorization/inverse, ten illustrative classical
point masses, forward-marginal/postselection controls and the noisy-menu example.
The classical proof quantifies over all finite environment sizes; the
real-quantum proof covers all product effects by (4). Ideal compression is
proved by the affine-dimension argument, not a finite search. The mathematical
argument also received independent read-only review.

Reproduce from the repository root:

```sh
.venv/bin/python -B docs/validation/t8-q-hypothesis-justification-2026-09-13/check_witnesses.py
.venv/bin/python -B -O docs/validation/t8-q-hypothesis-justification-2026-09-13/check_witnesses.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-hypothesis-justification-2026-09-13/check_witnesses.py
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-hypothesis-justification-2026-09-13/check_witnesses.py
```

The requested [relativity/geometry dependency plan](../../track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md)
uses this finding rather than pretending the hypotheses have been proved.
Quantum axiom work and native order-kinematics can be investigated separately;
their eventual joint correspondence must keep both records and the quantum
payload. No new QR-05 letter, capture series, RET work or gravity promotion
follows from this note.
