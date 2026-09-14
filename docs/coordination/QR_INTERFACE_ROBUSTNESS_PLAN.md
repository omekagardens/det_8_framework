# RI-19 — exact admission and approximate-instrument law stability

14 September 2026 UTC. **DESIGN_AND_CONDITIONAL_PROOF_ONLY;
FULL_C_TO_C0_BRANCH_CLASSIFICATION; EXACT_ADMISSION_OBSTRUCTION;
MATCHED_SCALAR_LAW_STABILITY.** Independent mathematical and API/record
reviews found no remaining blocker after the wording corrections below.
The coordinator accepts this bounded conditional proof and design.
No executor, new API, witness registration or physical operation is supplied.

This bounded assignment follows published RI-18 checkpoint
ba129584e5c05a06f061e77cd3bf2daf18a02bdc, tree
eed0446c8f6fc88539d4f1ca08e1d14bd65d620b. Its accepted
[finite composition](../validation/t8-q-finite-protocol-composition-2026-09-14/PROTOCOL_COMPOSITION.md),
[RI-08e robustness](../validation/t8-q-repeatability-robustness-2026-09-13/ROBUSTNESS.md),
[RI-08d joint admission](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)
and [terminal-read interface](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md)
remain unchanged. This note closes a mathematical interface question without
assuming that a nearby output has an accepted reusable software type.

## 1. Domain, calibration and the actual question

Write
\[
D(A,c)=\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix},\quad
\mathcal C=\{D(A,c):A\succeq |c|I\},\quad
\mathcal C_0=\{D(A,0):A\succeq0\},\quad c=u+iv.
\]
The real spans have dimensions six and four. The mass, quotient and section
are
\[
m(D)=2\operatorname{Tr}A=\operatorname{Tr}D,\quad
\Phi(D)=2A^T=\rho,\quad J_2(\rho)=D(\rho^T/2,0).
\]
Consequently C is equivalent to \(\rho\succeq2|c|I\), and J2 is a
positive linear isomorphism from PSD2 to C0. Neither normalization nor
the earlier terminal catalogue discards the input c.

Let Q be a specified rank-one projector and set
\(p=e_Q(d)=\operatorname{Tr}(\Phi(d)Q)\). A candidate branch is
real-linear on the entire real input span, positive C→C0, with exact
calibration \(m(\widetilde B_Qd)=p\). Its repeatability defect is
\[
0\le(m-e_Q)(\widetilde B_Qd)\le\epsilon p
\quad(d\in\mathcal C),\qquad0\le\epsilon\le\tfrac12.
\tag{1}
\]
For the finite protocol Q_r=(I+(-1)^rY)/2, r=0,1. Both branches have
their respective exactly calibrated effects; their masses sum to m.
Their sum need not be the identity raw map. Whole-C positivity, exact
C0 output, operation availability and a uniform error guarantee are
distinct supplied premises. The existing ideal executor proves none of
them for an unspecified approximate instrument.

## 2. Complete rank-one-effect classification

**Theorem.** Every such positive calibrated C→C0 branch, before imposing
(1), has the unique form
\[
\boxed{\widetilde B_Q(D)=J_2(pH+uK+vL),}
\tag{2}
\]
where H,K,L are Hermitian 2x2 matrices with traces 1,0,0, respectively,
and
\[
\boxed{H+\tfrac12(\cos\theta K+\sin\theta L)\succeq0
\quad\text{for every real }\theta.}
\tag{3}
\]
Conversely every triple satisfying these conditions defines a positive
exactly calibrated branch on the whole cone.

**Necessity of the form.** On the c=0 section, transport the branch through
Phi/J2. In a basis with Q=|0><0|, its positive Hermitian map M has trace
effect rho_00. Faithfulness gives M(|1><1|)=0. Positivity on the unnormalized
rank-one inputs (1,t)(1,t)* for every real t makes M(X)=0, since otherwise
H+tM(X) has a negative vector expectation for one sufficiently large sign
of t. Inputs (1,it) similarly kill M(Y). Thus M(rho)=rho_00 H with
H≥0 and trace H=1. The two remaining independent real input directions
are u and v; real linearity gives (2), and exact trace calibration makes
K and L traceless. This is a whole-domain argument, not a finite preparation
catalogue assertion. The triple is unique on the full real span.

The projection of the positive input cone onto (p,u,v) is exactly
\[
\boxed{p\ge2\sqrt{u^2+v^2}.}\tag{4}
\]
Necessity follows from rho≥2|c|I. Conversely rho=pI realizes every point
of (4). It has mass 2p, not generally mass one. On the normalized slice
one additionally needs 1-p≥2|c|; normalizing the displayed cone witnesses
preserves c/p, so the full boundary circle remains necessary for a uniform
normalized-input theorem as well.

For p>0 the normalized output in (2) is H+(u/p)K+(v/p)L, where (u/p,v/p)
ranges over the disk of radius 1/2. The disk is the convex hull of its
circle, so positivity is equivalent to (3). At p=0, (4) forces c=0 and
the entire output is zero. This proves necessity and sufficiency without
an angle grid or a numerical positivity solver.

For an equivalent geometric certificate, write
H=(I+h·sigma)/2, K=k·sigma/2 and L=l·sigma/2. Then (3) says
\(|h+(k\cos\theta+l\sin\theta)/2|\le1\) for every theta.
It is a whole-circle condition; checking finitely many directions without
a separate complete certificate does not establish it.

### Uniform defect, descending subclass and exact limit

Put
\[
a=\operatorname{Tr}((I-Q)H),\quad
b=\operatorname{Tr}((I-Q)K),\quad
e=\operatorname{Tr}((I-Q)L).
\]
Under (3), (1) is equivalent to the single exact condition
\[
\boxed{a+\tfrac12\sqrt{b^2+e^2}\le\epsilon.}\tag{5}
\]
Indeed the normalized defect is a+(u/p)b+(v/p)e; its maximum on the
entire disk is the displayed expression, attained on the boundary when
(b,e) is nonzero. Positivity already implies its nonnegative minimum.
This derives the uniform condition rather than inferring it from samples.

The branch descends through Phi **iff K=L=0**. Sufficiency is immediate.
For necessity, vary c over a small disk at a fixed strictly positive rho;
Phi is unchanged, so descent forces both coefficient matrices to vanish.
This is branchwise descent with the outcome r retained. Cancellation in
an outcome-erased sum does not prove descent of the labeled instrument.

At epsilon=0 every trace-one circle output has zero expectation on I-Q.
Positivity confines it to the exposed ray Q, so it equals Q. Opposite
circle points then give K=L=0 and H=Q. The ideal branch pJ2(Q) is recovered
uniquely. For complementary branches, apply these conditions separately;
exact effect completeness requires no further raw-map identity.

## 3. Admission obstruction and a contrasting lawful family

### Arbitrarily small error does not give exact admission

For 0<epsilon≤1/2 set
\[
H_\epsilon=(1-\epsilon)Q+\epsilon(I-Q),\quad
h_\epsilon=D(H_\epsilon^T/2,\epsilon e^{i\theta}/2),\quad
\widehat B_Q(d)=p h_\epsilon.
\tag{6}
\]
The A eigenvalues are (1-epsilon)/2 and epsilon/2, so h_epsilon lies in
C and has mass one. This is a positive exactly calibrated full-C branch
with defect epsilon p; complete it with the ideal complementary branch.
Its output is not in C0 when p>0. Untwisting the raw difference from pJ2(Q)
gives eigenvalues 0,0,+epsilon p,-epsilon p, hence
\[
\|\widehat B_Qd-pJ_2(Q)\|_1=2\epsilon p.
\tag{7}
\]
Thus even uniform arbitrarily small raw error does not establish admission.

The actual subsequent local Z leaves output c unchanged. With RI-18's
fixed reference t=3/5 the normalized coupled cross forms include
\[
tc=3\epsilon e^{i\theta}/10,\qquad -tc,
\tag{8}
\]
and their conjugates. These are nonzero for every epsilon>0. The output
can remain positive and mass-normalized while failing exact recordability.
For a ready path of positive weight this is a rejected interface, not a
small-error lawful path. At beta=0 the joint interface is not attempted.
No J2Phi projection, reset, recoupling, renormalization or enlarged return
type is licensed to hide the failure. This family is C→C, deliberately
outside the admissible C→C0 classification above.

### C0 range does not force quotient descent

For Q=Q_0=(I+Y)/2 choose any
\(0<\kappa\le\sqrt{\epsilon(1-\epsilon)}\), and set
\[
H_0=(I+(1-2\epsilon)Y)/2,\quad K_0=2\kappa X,\quad
L_0=2\kappa Z;\qquad H_1=Q_1,\ K_1=L_1=0.
\tag{9}
\]
Every circle output of branch zero is
H_0+kappa(cos(theta)X+sin(theta)Z), with trace one and determinant
epsilon(1-epsilon)-kappa²≥0. Its defect is exactly epsilon. The complement
is ideal. Thus these branches are positive C→C0 with complete exact
calibration, but branch zero depends on both u and v. Rational
kappa=epsilon works for every rational epsilon in (0,1/2]; the example
epsilon=1/5,kappa=2/5 reaches equality in the circle determinant.

This establishes algebraic range eligibility for the fixed polarized
interface, not executable type interchange or physical availability.
Whether its two c directions survive the particular later observations
is proved in §6, rather than inferred from nonfactorization alone.

## 4. Honest hypothetical prefix and comparison alphabet

The approximate instrument is a proposed **new** typed prefix, not a
substitution into an accepted ideal object. The initial boundary remains
the exact normalized empty-record/pending full-C snapshot, fixed frame,
root weight one and explicitly supplied preparations.

| Required new design contract | What it must retain or verify |
|---|---|
| Approximate-instrument premise | Both branch triples, whole-C positivity/C0-range certificate, exact Y calibration, uniform epsilon_r, availability and honest analytical/implementation provenance. These are supplied premises, not metadata-derived facts. |
| Approximate record/state and weighted prefix | Original full boundary; actual positive branch result; exact p_r and normalized state; truthful approximate record at signal event0; nominal axis/setting/controller/frame, source type and empty same-origin precursor. No event or normalization if p_r=0. |
| Actual local Z step | Apply the unchanged full raw Z congruence once under the new forward contract; retain the record and local pending ("Z",). It is not an i command or a new commitment. |
| New joint forward wrapper | Retain the entire approximate prefix, declared independent reference decision and law, origins, exact raw conversion and actual once-coupled target. Verify that target against its forward construction. |
| New preterminal inclusion and weighted suffix envelopes | Same entire kernel in the explicitly adopted i interface, exact input records and metadata, new joint records/pending initially empty; retain the original approximate chain through cut, command and scalar read/stop. |

The existing RI-18 `WeightedLocal` derives `c.commit_pauli` and Z internally;
its output fields cannot be supplied. A different update cannot be inserted
there, represented by a forged ideal `c.Record`, or certified merely by
constructing a c.State with an ideal-catalogue prefix. RI-15 requires the
exact c.State snapshot and its declared record grammar; it does not verify
the snapshot's entire earlier forward history. RI-18's weighted suffix
envelopes additionally require the actual ideal WeightedLocal anchor chain.
Neither interface already implements this proposed approximate prefix.

The following accepted **operations** may remain unchanged in a future
separately reviewed adapter:

- `c.controls(raw,"Z")` supplies the raw congruence; its new typed use still
  requires the above domain, record and forward-result contract.
- RI-18 `ReferenceLaw` and `ReferenceDecision` retain the complete independent
  ready/unavailable probabilities, preparation/selector IDs and truthful
  reference-origin record. They do not require an ideal WeightedLocal.
- Convert the new signal prefix truthfully to `d.LocalState` and generic
  `d.InputRecord`, without impersonating RI-08c provenance. Then use
  `d.prepare_joint -> promote_joint -> couple_state -> promote_joint`.
  The new retained wrapper, not RI-15's exact-c.State wrapper, binds this route.
- Component-wise exact conversion plus `i.k_from_local`, `inverse_k_span`
  and `image_kernel` validate equality of the entire once-coupled source.
  Construct unchanged `i.Context`/`i.State` with explicit available calibrated
  terminal read, fixed t/orientation/coupler/permutation and empty new joint
  history/pending. This is no second preparation or coupling.
- Use unchanged `i.commit`, outcome-only fixed empty/A `policy_word`,
  `i.run_word` and `i.read_terminal`, within the new weighted envelopes.
  The policy sees only validated (a,b), never a record exposing source Context.

Reference unavailability gives a separate scalar stop with signal/reference
event0 precursors, distinct protocol-stop origin/action and retained local
audit source. It gives no ReferenceState, joint Context or performed read.
On a ready path the literal cut is joint event0 with both input precursors;
the terminal is joint event1 and additionally retains joint0. All known
settings and actual local Z/new joint empty-or-A words remain separate.
Scalar terminal results supply no postread residual or continuation.

### Explicit common scalar alphabet, not equal audit wrappers

Fix a declared nominal observation schema and identical known metadata k.
For r=0,1, alpha=(a,b) and gamma=(a',b',sign), retain 64 ready coordinates
\[
(k,r,\mathrm{ready},\alpha,w(\alpha),\gamma)
\]
and two unavailable coordinates
\[
(k,r,\mathrm{unavailable},\mathrm{protocol\_stop}).
\tag{10}
\]
Here k explicitly includes the nominal first-test action/Y setting and
controller/frame; boundary/preparation identity; reference preparation and
selector-law IDs; origin and precursor scheme; fixed coupler/permutation,
cut setting and policy ID; and planned terminal-setting/calibration ID.
Outcomes retain both cell bits and sign. The unavailable label has no
performed cut, command or terminal outcome. Its planned read setting remains.
The deterministic precursor labels described above are part of the schema,
not omitted observations or an ordering between independent input origins.

Both honest typed audit chains need explicit projections onto (10).
Analytical branch parameters, error certificates and implementation types
remain in the audit, not randomized outcomes, **only if that is the declared
observation contract**. This compares the ideal and approximate mathematical
models of the same nominal action; it does not assert equality of their
source or wrapper objects. In particular, if the accepted c action
`pauli_measure_prepare` or source type `repeatable_selected` versus a
different approximate action/source name, apparatus ID or error-model
ID is itself an observed record/setting, retain that difference: those laws
are not on this matched alphabet and the small-TV claim does not apply to
their full recorded labels. Changing or erasing known settings to force a
match is forbidden.

For an initial-state comparison, supplied alternatives share the same nominal
preparation/observation metadata; their distinct known raw kernels remain
distinct audit inputs, not an extra oracle observation. Distinct observed
preparation identifiers cannot be erased to invoke that comparison.
No ideal RI-18 record is retroactively relabeled by this design.

## 5. Whole-law stability from the correct input norm

Fix beta in [0,1] as the ready probability of the expressly supplied complete
reference law; unavailable has probability 1-beta. The selector/preparation
law is independent of the input and the local outcome r, and is identical
in both compared models. This independence and readiness calibration are
premises, not deductions from named origins, provenance or factorized kernels.

Let tau_r=Phi(tilde B_r d)=p_rH_r+uK_r+vL_r, and let its ideal counterpart
be p_rQ_r. Define S as the unchanged ready suffix **including** the local Z,
fixed-reference coupling, four literal cuts, the alpha-only empty/A choice
and one tilted read. Regard its output as 32 scalar coordinates per r:
four cut labels times eight read labels, including cross-cell zeros. It is
a positive linear mass-preserving map from Hermitian PSD2 to this scalar
cone. Consequently, for every signed Hermitian Delta,
\[
\|S(\Delta)\|_{\ell^1}\le\|\Delta\|_1.
\tag{11}
\]
**Proof.** Write the spectral positive/negative parts Delta=Delta_+-Delta_-.
Their images are positive scalar vectors, with masses trace Delta_+ and
trace Delta_-. The triangle inequality proves (11). Equivalently J2
identifies the C0 base norm with both the qubit trace norm and the C0 raw
trace norm. We make no claim of raw-trace contraction on native L_t; its
native mass generally differs from its raw trace. The complete scalar
suffix, not an unproved intermediate native norm inequality, is what contracts.

At p_r>0, in the Q_r basis write
\[
\tau_r/p_r=\begin{pmatrix}1-s_r&z_r\\\bar z_r&s_r\end{pmatrix},
\quad0\le s_r\le\epsilon_r,\quad |z_r|^2\le s_r(1-s_r).
\]
Its eigenvalue difference from Q_r gives
\[
\tfrac12\|\tau_r-p_rQ_r\|_1
=p_r\sqrt{s_r^2+|z_r|^2}\le p_r\sqrt{s_r}\le p_r\sqrt{\epsilon_r}.
\tag{12}
\]
At p_r=0 the whole output is zero; no conditional s_r, z_r, state or event
is assigned. Define that branch's contribution to all following bounds as zero.

The complete scalar measures on (10) are
\[
\widetilde P_{r,\mathrm{ready}}=\beta S(\tau_r),\quad
P^0_{r,\mathrm{ready}}=\beta S(p_rQ_r),\quad
\widetilde P_{r,\mathrm{stop}}=P^0_{r,\mathrm{stop}}=(1-\beta)p_r.
\tag{13}
\]
For normalized d they have total mass one. Equations (11)–(13) prove
\[
\boxed{\operatorname{TV}(\widetilde P,P^0)
\le\tfrac\beta2\sum_r\|\tau_r-p_rQ_r\|_1
\le\beta\sum_rp_r\sqrt{\epsilon_r}
\le\beta\sqrt\epsilon,}\tag{14}
\]
where epsilon bounds both branch defects. The pointwise s_r bound in (12)
can replace epsilon_r when its value is actually supplied or computed for
that positive input. No sharpness of this composed bound is claimed.

For two normalized inputs with the same initial Y component, p_r agrees and
the ideal complete laws coincide. Triangle inequality and (14) give
\[
\operatorname{TV}(\widetilde P(d_1),\widetilde P(d_2))
\le\beta\sum_rp_r\bigl(\sqrt{\epsilon_{r,1}}+
\sqrt{\epsilon_{r,2}}\bigr).
\tag{15}
\]
Here branch-specific bounds may be identical when one fixed instrument is
being compared at two inputs. Stops agree and the ready measures each have
mass beta, giving also TV≤beta. In the uniform case this yields the valid
slightly stronger cap
\[
\boxed{\operatorname{TV}(\widetilde P(d_1),\widetilde P(d_2))
\le\beta\min(1,2\sqrt\epsilon)
\le\min(1,2\beta\sqrt\epsilon).}\tag{16}
\]
This is a bound, not a claim of an attained optimal constant. At beta=0
the scalar laws are exactly the two calibrated stops; their approximate
audit prefixes may still differ. At beta=1 no stop is selected, but both
zero stop coordinates remain in the prospective alphabet.

For an unnormalized positive d, replace TV by one-half the l1 distance of
finite measures of common mass m(d). The bound is beta sum_r p_r sqrt(epsilon_r),
at most beta m(d) sqrt(epsilon). For two inputs with equal mass and Y
moment, (15) holds with those common unnormalized p_r and cap beta m(d).
When m(d)>0, divide the measures and bound by m(d) for normalized laws.
At m=0 the faithful cone contains only zero; no normalization is available.
A separately supplied external prefix weight multiplies every coordinate
and every bound once, not the normalized conditional state.

## 6. What the actual fixed suffix observes

This is not the larger all-word or three-separately-prepared-setting
catalogue of RI-08i. Only RI-18's fixed cut-dependent empty/A policy is used.
Let the unnormalized branch output **before local Z** be
\[
\tau=(pI+xX+yY+zZ)/2,\qquad s=(-1)^b.
\]
Local Z sends (x,y,z) to (-x,-y,z). With t=3/5 the four filtered cells
after coupling have
\[
q_b=(p+3sz/5)/4,\quad x_b=-x/5,\quad y_b=-y/5,\quad
z_b=(z+3sp/5)/4.
\tag{17}
\]
For a=0 use the tilted axis (3/5,0,4/5); for a=1 its A-pulled-back axis
is (3/5,96/125,-28/125). Let d_ab be the plus-minus scalar contrast in
the occupied cut cell, before the readiness factor. Then
\[
d_{0b}=-3x/25+z/5+3sp/25,\qquad
d_{1b}=-3x/25-96y/625-7z/125-21sp/625.
\tag{18}
\]
The complete ready suffix has weights (q_b+d_ab)/2 and (q_b-d_ab)/2
at terminal cell (a,b), and zero at its other six terminal coordinates.
These are unnormalized joint cut/read weights, not conditionals obtained
by division by a zero cell. Approximate inputs generally change q_b and
the sign weights: do not reuse the ideal fixture's q_b=1/4 or its number
of positive terminal leaves. All prospective coordinates stay retained.
For this fixed interior reference, p>0 implies q_b≥p/10>0; zero initial
branches and zero terminal-sign weights still require their separate guards.

Equations (17)–(18) prove that this fixed S has **rank four** on Herm2.
The two q_b recover p and z; d_00 then recovers x, and d_10 recovers y
because its y coefficient is -96/625≠0. In particular no nonzero signed
branch-output direction is invisible to the complete ready suffix.
The row minor formed by q_0, q_1, (q_0+d_00)/2 and (q_0+d_10)/2,
in columns (p,x,y,z), has exact determinant -27/78125. Multiplication of
the complete ready law by a positive beta preserves this rank.
This is an algebraic full-law statement, not conditional selection of an
impossible branch or an availability claim for arbitrary preparations.

For a fixed classified two-branch instrument and beta>0, r remains in
every scalar label, so the pair of branch outputs is observed injectively.
The initial six-dimensional coordinates enter that pair only through
\((m,y_{\rm in},u,v)\), with p_r=(m+(-1)^r y_in)/2. Traces recover
both p_r, while the c terms are traceless. Therefore the exact full-span
rank is
\[
\boxed{2+\operatorname{rank}_{\mathbb R}
\{(K_0,K_1),(L_0,L_1)\}\in\{2,3,4\},\qquad\beta>0.
\tag{19}
\]
There is no cancellation hidden in the retained outcome r. At beta=0
the rank is exactly two, independently of K/L; at epsilon=0 it is two
for every beta. On mass-one slices the affine dimension is one less.

The family (9) has rank four for every epsilon>0 and kappa>0. Thus both
input-c coordinates can indeed survive this particular suffix under an
admitted approximate branch. The original X and Z coordinates still do
not enter (2); even this rank-four law is not full initial-state tomography.

For a concrete positive-domain separator, use epsilon=1/5, kappa=2/5 and
the same initial A=I/4. The two inputs c=+1/8 and c=-1/8 have identical
Phi and p_0=p_1=1/2; their branch-zero payload difference has Bloch
Delta x=2/5, with all other output coordinates equal. Equations (17)–(18)
give full-law TV=12 beta/125. The analogous pair c=+i/8 and c=-i/8 has
Delta z=2/5 and full-law TV=7 beta/50. For example, the absolute z
coefficients of the eight scalar read effects sum to 7/10, hence its
TV is (beta/2)(2/5)(7/10)=7 beta/50. Stops and the branch-one law agree
in both comparisons. At beta=2/3 the distances are 8/125 and 7/75.
These are comparisons of complete unconditioned scalar laws, not of
postselected snapshots or of known audit matrices alone.

Exact rank can increase for arbitrarily small admitted errors while (14)
and (16) make all probabilities arbitrarily close. Rank alone proves no
finite-sample precision, uniform inverse stability, measured access to c,
unknown-instrument identification or practical advantage. Beta=0 and
kappa=0 are genuine singular boundaries, not evidence against the bounds.

## 7. Possible implementation obligations, not implementation authority

Only if separately assigned after acceptance, a bounded implementation
would need to:

1. Fix an exact certifiable branch family or a whole-circle positivity certificate;
   a circle grid is insufficient. Validate both effects, C0 range and
   uniform defect on the whole domain. A generic positivity solver is not
   supplied or requested here.
2. Implement the new truthful approximate prefix and forward-bound adapter
   of §4, preserving every complex entry, weight, action, setting, context,
   origin/precursor and both pending-word namespaces. Existing ideal wrappers
   remain unchanged. No partial-trace or J2Phi repair of an invalid output.
3. Freeze the explicit matched scalar alphabet separately from unequal audit
   types, and refuse comparisons with changed observed metadata. Preserve
   all 66 coordinates and actual zero-selection guards; validation failures
   reject the protocol rather than become physical zero-probability paths.
4. Check actual independent native arithmetic against the positive-map
   composition and (17)–(18), including singular inputs, selector endpoints,
   the near-ideal admission failure and genuinely observed c directions.
   These would supplement, not prove, whole-domain positivity and error.
5. Obtain independent proof/source review, a separate pinned import/launcher
   contract and scoped acceptance before claiming executable interchange.

This note creates none of those executables or registrations. Exact range
admission, typed executable interchange and supplied operation availability
remain three distinct questions. The named mathematical yields are the
classification, uniform condition, admission counterexample, law bounds
and exact fixed-catalogue observation rank—not a new physical law.

## 8. Evidence, source identity and stop boundary

The 60 previously held predecessor/design paths and all five accepted RI-18
statement/executable/launcher files match their entry identities: 65 held
paths, zero changes. No accepted theorem, source, design, launcher, registry,
RET/application/bank or protected evidence is edited.

An independent temporary exact native calculation using the unchanged i
model checked all 128 scalar coefficients (four signed Hermitian basis
inputs times four cut labels times eight terminal outcomes), the rank-four
minor, and the two positive-domain c distinguishability witnesses. This
arithmetic used signed mathematical helpers, not fabricated typed ideal
states or an implemented approximate prefix. It corrected a preliminary
imaginary-c hand sum to 7 beta/50 before the note was finalized. Main's
separate Fraction-only calculation passed four scalar checks: complete
effect mass, the minor, and both TV values. These are supplementary
calculations, not new registered tests, a new pinned execution, or a proof
of whole-circle positivity by sampling. The symbolic arguments above carry
the full-domain claims.

Independent complete mathematical review verified the classification,
admission counterexample, uniform condition, norm/bound arguments and exact
fixed-catalogue rank. Independent complete API/record review verified the
new-prefix versus unchanged-operation boundary and the common alphabet.
Review corrections distinguish whole-circle positivity from the stronger
ancillary notion of complete positivity, and RI-15's snapshot grammar from
RI-18's actual ideal forward history; literal action/source names now match
the accepted c model. Final source identities and scoped verification are
recorded in the [QR handoff](QR_HANDOFF.md). Coordinator proof/design acceptance
is complete; the [progress record](REVIEW_PROGRESS.md) tracks publication.

The bounded proof and design are accepted. This creates no executor assignment,
new control family, SDK, empirical calibration, full-QM derivation, physical
mass, geometry or gravity promotion. After resolving this interface, the
larger choice is consolidation with premise selection or a measured application
under supplied calibration/evaluation requirements, not another arbitrary
operation family. This note starts neither larger path.
