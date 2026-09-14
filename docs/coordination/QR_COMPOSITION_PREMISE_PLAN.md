# RI-20 — composition premises and exact probe adequacy

14 September 2026 UTC. **CONDITIONAL_PROOF_AND_PREMISE_AUDIT;
DET_NATIVE_STRONG_POSITIVITY_SELECTION_NOT_ESTABLISHED.**
Independent mathematical, primary-source and repository reviews passed.
Coordinator proof/audit acceptance is complete. This is one proof/design note,
not a new executor, operation family, axiom adoption or registered witness.
It addresses original [finding F3](../../indep%20ndent_review.md) upstream of
the accepted PSD cone results. The
[coordinator synthesis](../research/PROOF_SYNTHESIS_AND_PREMISE_SELECTION.md)
provides the connected roadmap; RI-19 is accepted and published at
`f6b8f18f8d7aa739c5b78209b7f69a5c1db87f67`, and the composition assignment
is published at `5a73cef979ca35b596728cc498127506159837f8`.

**Decision.** A known composition theorem supplies a conditional route to
strong positivity. DET has not yet justified its pre-PSD class, unrestricted
finite composition or interference-resource admission premises. The exact
fixed-probe criterion below is proved, including a normalized counterexample
whenever its test cone is proper. Neither result derives full QM or selects
the complex field. No successor is launched by naming the remaining gap.

## 1. Starting object and three different positivity questions

Fix a finite carrier with n alternatives and its full Boolean event algebra.
The unknown atomic matrix D is Hermitian over the **supplied** field C, with
biadditive event functional D(A,B)=chi_A† D chi_B and normalization

\[
m(D)=\mathbf1^\dagger D\mathbf1=\sum_{ij}D_{ij}=1.
\]

Weak positivity means mu_D(A)=chi_A† D chi_A>=0 for every Boolean event A.
Strong positivity means every finite event matrix is PSD; on this finite
full algebra this is equivalent to D>=0, since singleton events recover D
and other event matrices are its incidence congruences. The total-entry
normalization m is **not** trace normalization. Here normalization mass is
not physical rest mass. Biadditivity gives grade-two event weights without
forcing strong positivity or specifying imaginary entries from those weights.

Three claims must not be interchanged:

1. Every Boolean event has a nonnegative mathematical weight.
2. A particular partition is exactly recordable under a declared instrument.
3. An ancillary preparation and its independent composition are available.

An interference event weight need not be the probability of a cell in one
common recorded partition. In particular, this audit does not assign every
Boolean cut an available sharp operation. The
[strict derivation, section 4](../validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md#4-exactly-where-event-vectors-stop-being-measurement-operators)
shows that requiring all singleton cuts to descend as sharp all-history
operations would make the atomic matrix diagonal. That is a different and
excessively restrictive premise.

## 2. Exact primary-literature route and its hypotheses

Write W for normalized weakly positive systems, S for strongly positive
systems, and R+ for systems whose **every event-pair value** is real and
nonnegative. In the present finite setting R+ is exactly the real
entrywise-nonnegative Hermitian class. Let A be a class specified without
first restricting its unknown members to PSD matrices.
The class A ranges across finite carrier sizes (or the papers' more general
history systems); fixed n in sections 1 and 4 describes one audit slice,
not a same-size matrix class closed under tensor products.

**Known results, credited rather than rederived here.**
[Dowker–Wilkes v2](https://arxiv.org/html/2011.06120v2), Theorem 4, gives
A⊆S or A⊆R+ when A⊆W is tensor closed. Therefore one admitted negative or
nonreal event-pair resource forces A⊆S. Theorem 2 states that compatibility
with all of S is exactly S. Theorem 3 requires tensor closure and Galois
self-duality for A=S; neither self-duality nor all-S probe availability is
needed for the Theorem 4 containment inference. Do not replace this with an
unqualified claim that S is the unique inclusion-maximal tensor-closed class.

[Boës–Navascués v3](https://arxiv.org/html/1609.09723v3), Lemma 3, gives each
finite non-SP functional a tailored quantum-functional probe, constructed
with two measurement settings, whose product has a negative event weight.
Lemma 2 supplies, for every finite n, a functional valid at n self-copies but
invalid at n+1. A fixed copy cutoff therefore cannot certify unrestricted
composability. The rich quantum probe family is a premise of that testing
route, not a DET-derived preparation catalogue. We use these lemma statements,
not the printed norm manipulation in their equation (8).

For the class-containment application, the load-bearing requirements are:

| Premise | Exact content needed here | What would not supply it |
|---|---|---|
| Pre-PSD admission | An independently specified class A of the Hermitian normalized weak-positive objects above | Defining A to contain only PSD matrices, then claiming to have selected PSD |
| Product law | Independent members combine by the functional tensor product; the joint algebra contains all Boolean events on the product carrier, including nonrectangular subsets | A sequential Markov law, a matrix constructor, or one postcoupler record partition |
| Unbounded finite tensor closure | Every pair of members has its product in A, iterably for arbitrary finite mutual and self composition | One candidate's self-powers, a fixed copy-depth check or a terminal interface that forbids reuse |
| Interference resource | Some admitted member has a negative-real or nonreal event-pair value | A merely nonzero positive off-diagonal value; classical randomness; a matrix example without an admission premise |

Closure is a universal mathematical admissibility law. It is not proof of
laboratory preparation, arbitrary repeated apparatus access or an infinite
tensor-product limit. In the papers, events are closed under finite Boolean
operations; their general history setting does not add countable additivity
or an infinite-product construction to the present finite audit.

One may establish the existence of a **particular** PSD interference resource
without circularly assuming every candidate is PSD. What must be justified
independently is that resource's admission and the class-wide composition
law. For example b=(1,-1,1), B=bb† has m(B)=1 and a negative entry. This
exhibits a normalized mathematical resource, not a DET preparation theorem.

## 3. Premise-to-conclusion and countermodel decision table

| Hypotheses actually supplied | Conclusion or obstruction | Boundary |
|---|---|---|
| Hermitian, normalized, biadditive, weak event positivity | D3=(J3-I3)/6 passes but is non-PSD | Original F3 remains open from these premises |
| The same, plus positivity of all self-powers | D3 still passes every finite power | Self-copy consistency alone does not remove the nonnegative-entry alternative |
| Tensor-closed A⊆W, no resource excluding R+ | A=R+ remains possible | Mutual closure alone does not select S |
| Tensor-closed A⊆W plus one negative/nonreal event-pair resource | A⊆S by the cited class theorem | Conditional known selection, not A=S or an admission proof |
| All normalized PSD probes with all Boolean product events | D is PSD; section 5 gives the finite witness | Imports probe richness and product-event testing |
| All real PSD probes, arbitrary Boolean events | The complex Di of section 6 passes but is non-PSD | Its self-square fails, so it is not a tensor-closed-class countermodel |
| Classical diagonal ancillary probes | Only nonnegative sums of base event tests | No improvement over weak event positivity |
| A fixed finite list of ancillary matrices and events, plus all base events | Its test cone is proper for n>=2; section 4 supplies a normalized non-PSD separator | Fixed **linear** tests only, not candidate self-powers or an unbounded generated resource family |
| A finite phase alphabet with continuous magnitudes and Boolean grouping | Can already generate every rank-one test | Finite symbols are not a finite matrix/event menu |

## 4. Exact fixed-probe adequacy theorem

Fix n>=1. The allowed probe/event family is fixed independently of the unknown
D. Each probe B is a finite Hermitian PSD matrix with m(B)=1. A joint event
E is represented by Boolean incidence R, where R_ia=1 exactly when (i,a)∈E.
No row-disjointness assumption is needed. Direct expansion gives

\[
\begin{aligned}
\mu_{D\otimes B}(E)
 &=\sum_{ijab}R_{ia}R_{jb}D_{ij}B_{ab}\\
 &=\operatorname{Tr}(DT),\qquad
 T=(RBR^T)^T=\overline{RBR^T}\succeq0.
\end{aligned}
\tag{1}
\]

The transpose is load-bearing for complex matrices. Replacing T by RBR^T
inside the trace can test the wrong complex direction. Congruence preserves
PSD and complex conjugation preserves the PSD cone, proving T>=0.

Include the trivial ancilla B=[1] and **every** base indicator R=chi_A.
Thus the test matrices include chi_A chi_A†, in particular J=11†. Let

\[
K=\overline{\operatorname{cone}}\{T:\text{allowed probe/event tests}\}
\subseteq\operatorname{PSD}_n,
\quad
K^*=\{D=D^\dagger:\operatorname{Tr}(DT)\ge0\ (T\in K)\}.
\]

Both cones are in the real vector space Herm_n with trace pairing. There is
no extra prior block-form, fixed-entry or preparation restriction on D.

**Theorem (finite probe adequacy).** Positivity on the specified tests forces
every normalized Hermitian candidate D to be PSD **if and only if**
K=PSD_n. Equivalently,

\[
\{D\in K^*:m(D)=1\}\subseteq\operatorname{PSD}_n
\quad\Longleftrightarrow\quad K=\operatorname{PSD}_n.
\tag{2}
\]

**Proof.** Positivity on the original tests is equivalent to membership in
K*, by linearity and continuity. If K=PSD_n, its dual is PSD_n: a PSD D
pairs nonnegatively with every PSD T; conversely testing vv† gives v†Dv>=0
for every v, exactly the PSD condition.

If K is proper, choose X>=0 outside K. Finite-dimensional closed-cone
separation gives Hermitian D0 with Tr(D0T)>=0 for every T∈K and
Tr(D0X)<0. Hence D0∈K* but D0 is not PSD. The included J test implies
m(D0)>=0. Choose

\[
0<\delta<-\lambda_{\min}(D_0),\qquad
D_\delta=D_0+\delta I,\qquad
\widehat D=\frac{D_\delta}{m(D_0)+\delta n}.
\tag{3}
\]

I pairs nonnegatively with K⊆PSD_n. Consequently D_delta∈K*, while its
least eigenvalue remains negative. Its total-entry mass is strictly positive,
so the displayed normalization is legal and preserves both properties.
All base events are included, so D-hat is also weakly positive. This is the
required normalized non-PSD counterexample, proving the converse. ∎

In fact Tr(D_delta T)>=delta Tr(T)>0 for every nonzero T∈K. Thus the
counterexample is not an artifact of a zero test margin: perturbations H
with operator norm less than delta preserve test positivity before positive
normalization. The negative eigenvalue also persists under sufficiently small
perturbations. No finite-sample detection guarantee follows from this fact.

**Precise limits.** Closure in K is essential: a dense collection of rank-one
directions can suffice without literally containing each direction. The theorem
concerns exact inequalities, not noisy finite estimates. Including the base
events/J is load-bearing for the normalized converse. For an independently
restricted candidate subspace or cone, an appropriate relative criterion is
needed; proper K alone need not produce a counterexample in that restriction.
Probes B are already PSD and the Hermitian complex vector space is inherited.
Neither is selected by this argument.

For a **finite fixed** matrix/event menu, the extra 2^n base indicators still
leave finitely many generators. K is then polyhedral. For n>=2, PSD_n is not
polyhedral: its normalized rank-one rays vv† give infinitely many distinct
extreme rays. Rank one is extreme because PSD summands of vv† must vanish
on v's orthogonal complement and hence have the same one-dimensional range.
Therefore (3) supplies a counterexample to every such fixed finite menu.
For n=1, the base test already suffices.

Candidate-dependent tests D↦mu_(D tensor D)(E), or higher self-powers, are
**nonlinear in D**. They are not members of this fixed-ancilla linear-test
criterion and are not excluded by the polyhedral proof. Finite self-copy
cutoffs have the separate cited Lemma 2 obstruction; arbitrary mutual class
closure has the different quantifier in section 2.

## 5. An unrestricted probe illustration and finite-symbol caution

For arbitrary v∈C^n, including sum(v)=0, define

\[
b=(\overline v_1,\ldots,\overline v_n,
 1-\sum_i\overline v_i),\quad B=bb^\dagger,\quad
R=[I_n\mid0].
\]

Then sum(b)=1, so m(B)=|sum(b)|²=1 without division. Also Rb=bar(v),
T=(Rb b†R^T)^T=vv†, and (1) gives mu_(D tensor B)(E)=v†Dv for
E={(i,i):1<=i<=n}. The appended unused alternative makes this construction
normalized even for zero-sum directions; using b=bar(v) directly would have
zero total-entry mass. A PSD matrix with zero total-entry mass cannot be
normalized by scaling. No minimal ancillary dimension is claimed, and neither
trace(B)=1 nor norm(b)=1 is asserted.

This is an elementary illustration of the known composability route, not a
new physical derivation or a verbatim reproduction of either paper's probe.
It assumes an arbitrary complex-amplitude resource family and joint events.
If those resources are actually allowed, K contains all rank-one PSD matrices
and (2) applies. The formula itself does not establish their availability.

A finite phase alphabet is not automatically inadequate. With phases
{1,-1,i,-i} and arbitrary nonnegative magnitudes, any z is the sum

\[
z=(\Re z)_+\cdot1+(-\Re z)_+\cdot(-1)
 +(\Im z)_+\cdot i+(-\Im z)_+\cdot(-i).
\]

Allocate at most four distinct ancillary coordinates to each z_i=bar(v_i),
and let Boolean row i select that group. Use at most four further, unselected
coordinates for 1-sum(z_i). Their amplitude vector b has sum one and Rb=bar(v),
so B=bb† again produces T=vv†. Zero components can simply be omitted.
This needs continuous magnitudes, the indicated carrier/grouping freedom and
admitted coherent resources. It grants none of them to DET. It shows why a
finite alphabet or finite generating catalogue with unbounded composition
cannot be confused with a finite list of realized B,R tests.

## 6. Exact countermodels and what each one refutes

### Positive-entry F3 kernel: all self-powers still pass

Let D3=(J3-I3)/6. For an event containing k alternatives,
mu_D3(A)=k(k-1)/6; total mass is one, and all events are nonnegative.
Its eigenvalues are 1/3,-1/6,-1/6, with
(1,-1,0) D3 (1,-1,0)^T=-1/3. Biadditivity supplies grade two.
Every entry of every finite self tensor power is nonnegative; normalization
multiplies to one. Thus every Boolean event in every power remains positive
or zero. More generally the whole normalized real entrywise-nonnegative
class is tensor closed. This is the surviving R+ alternative, not a defect
in the PSD tensor-product sufficiency theorem.

### Complex defect invisible to real probes: self-square fails

Let

\[
D_i=\begin{pmatrix}1/2&i\\-i&1/2\end{pmatrix}.
\]

Its four event weights are 0,1/2,1/2,1 and its eigenvalues are 3/2,-1/2.
For every real PSD probe B and Boolean R, T is real symmetric PSD, so
Tr(D_i T)=Tr(T)/2>=0. This proves universal real-probe blindness; it is not
an inference from a numerical sample. Di nevertheless fails its own square:
the event {(1,1),(2,2)} has weight 1/4+1/4+i²+(-i)²=-3/2.
It therefore cannot inhabit a tensor-closed weak-positive class.

A diagonal classical probe B=diag(q_a), q_a>=0, sum(q_a)=1 gives
T=sum_a q_a r_a r_a^T, where r_a is column a of R. Its test is a
nonnegative weighted sum of base event tests and excludes neither weak-positive
countermodel. In contrast the complex rank-one helper with v=(1,i),
b=(1,-i,i) gives weight -1 against Di.

## 7. DET-wide premise ledger: assumed, proved, still missing

The references below identify existing obligations, not changes to their
accepted statements or to the original review.

| Repository evidence | What is established or explicitly supplied | Missing for pre-PSD selection |
|---|---|---|
| [Commit kernel](../../det8/models/markov_kernel.py), lines 202–217, 331–342 | Caller-supplied scalar probability law and ordinary sequential Markov composition | Complex independent tensor law and all Boolean composite-event positivity |
| [Pair kernel](../../det8/models/pair_kernel.py), lines 4–28, 64–69, 309–319, 361–379 | PSD is an input requirement; compose constructs a Kronecker matrix; PSD×PSD closure is credited mathematics | Necessity of PSD in a pre-PSD admissible class; constructing unchecked entries is not an admission theorem |
| [Record-kernel proposal](../record_kernel_physics.md), lines 190–191, 219–230 | SP is required by the candidate; relationality + composition + positive commitability ⇒ SP is expressly a target | A completed proof of those antecedents and their intended event quantifiers |
| [Strict derivation](../validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md), lines 23–38, 118–123 | Complex normalized SP functional and explicitly supplied preparations yield conditional Gram/Born-form results | Derivation of the SP premise or independently established preparation access |
| [Pair-kernel examples](../../det8/models/pair_kernel.py), lines 325–348 | MM† generates particular PSD resources, including nonclassical examples | An admission argument for one such resource and universal pre-PSD class closure; particular PSD examples alone are not circular, but do not prove either premise |
| [T8 growth](../track_b/covariant_record_growth.md), lines 222–240, 347–349 | Conditional finite classical record/order laws | DET-native law selection or quantum composite closure |
| [RI-08c model](../validation/t8-q-repeatable-record-instrument-2026-09-13/model.py), lines 1–10, 343–358, 442–452 | PSD source cone and supplied calibrated, positive same-cone repeatable branches | Pre-PSD global admission and arbitrary composite testing |
| [RI-08d interface](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md), sections 1, 4, 7 | Independent preparations, tensor rule, one shared coupler and one exact record partition are additional premises | All finite mutual products and every Boolean event; this finite interface does not assert global composite availability |
| [RI-15 adapter](../validation/t8-q-local-joint-adapter-2026-09-13/adapter.py), lines 84–90, 131–143; [RI-18 adapter](../validation/t8-q-finite-protocol-composition-2026-09-14/adapter.py), lines 1–8, 27–35, 158–182 | Exact snapshot/type conversion and one declared weighted forward route, preserving supplied references and histories | Unrestricted recursive tensor closure; terminal records do not acquire reusable residuals |
| [Operational completion](../validation/t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md) | Explicitly proposed operational postulates and an imported conditional reconstruction | Independent derivation of its composite/instrument/preparation richness |

The RI-08d rejection of c!=0 after the supplied coupler is especially
important. Such a residual can remain normalized PSD, hence positive on
**all** Boolean events, yet fail the chosen exact record partition through
nonzero complex cross forms ±tc. See its
[model](../validation/t8-q-joint-recordability-2026-09-13/model.py),
lines 419–425 versus 533–539. That is a recordability obstruction, not a
negative-event witness supplying the missing pre-PSD principle.

Two meanings of faithfulness also stay separate. Faithful normalization mass
excludes positive zero-mass states for cone/base-norm arguments; it does not
prove ancillary complete positivity. A proposed pure dynamically faithful
preparation distinguishes allowed processes. The
[principle-selection study](../validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md),
lines 170–193, explicitly leaves its physical preparation unproved and notes
that real quantum examples pass. Neither property gives a probe family
detecting all non-PSD event matrices. An injective representation is not an
available experiment.

This respects the (R,Z) distinction: live residual activity, its eventual
committed record, and access to that record remain different. A record
catalogue does not automatically reveal all residual directions or give
all Boolean tests on independent copies. Replacing the pair kernel by a
scalar record summary would discard the very complex structure being audited.

## 8. Smallest meaningful remaining obligation and halt boundary

The next unproved arrow is an **admission/composition premise contract**,
not another inverse or finite operation example. It would have to specify
the actual DET pre-PSD class A and independently justify:

1. Its Hermitian/biadditive/normalized event object, including the chosen
   complex completion and why every Boolean event is weakly positive.
2. The independent tensor product and joint event algebra, with closure for
   arbitrary finite mutual and self composition, not just a supplied coupler.
3. Admission of at least one negative/nonreal event-pair resource without
   presupposing the class-wide PSD conclusion.

If these do not follow from DET, label them **additional candidate premises**
and retain the gap. The older permission to explore extra axioms does not
make them proved or adopt them globally. If a restricted probe route is
chosen instead, declare its actual independently available B,R family;
equation (2) gives the exact adequacy obligation and (3) the failure route.
Neither route is automatically assigned by this note.

Containment in SP would still not establish equality with the full quantum
state class, select complex over real scalars, supply purification or local
tomography, make arbitrary instruments/apparatus available, or derive a
native growth law F/L. No Hilbert space, metric, supplied mesh, Minkowski
coordinates, Johnston kernel or borrowed growth law is claimed to have
emerged here. The primitive-input test, Option B and metric-as-record Status M
remain unchanged. No kinematic geometry bridge, physical time, rest mass,
Einstein dynamics or gravity result is inferred.

This assignment ends at reviewed source-quiet handoff. No approximate executor,
predecessor-suite replay, new registration, QR-05BW–DO/coverage/noncollapse
sequel, RET, clocks, book, retired kappa-gravity, application implementation
or automatic successor is opened. The other isolated research directories
and all accepted source/evidence remain held.

## 9. Review and verification record

The written separation proof and countermodels carry the conclusions.
Three independent complete reviews passed: mathematical derivations;
primary-paper attribution/hypotheses and countermodels; and repository
premises/source accuracy. Their clarifications are incorporated: arbitrary
nonrectangular joint events, variable carrier sizes for class closure, and
no minimal-ancilla claim for the appended-coordinate helper.

An independent temporary exact calculation checked all eight D3 base events,
the four Di base events, a finite real-PSD-probe sample and the negative
self-square event. The universal real-probe and all-self-power conclusions
follow from the written arguments, not that sample. These calculations are
supplementary only; no new source, suite or pinned execution is claimed.

All 66 accepted predecessor/design identities matched on entry and at the
post-review check. All 141 local links across the four scoped documents
resolve, with zero whitespace/conflict-marker findings. The exact four
document identities accompany the [source-quiet handoff](QR_HANDOFF.md).
Coordinator proof/audit acceptance is complete; the coordinator retains every git/index
operation and separate publication authority. No successor has been started.
