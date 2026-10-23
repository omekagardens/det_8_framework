## Parameter identification after fixed-size uniform thinning

The reviewed [parameter-identifiability theorem](PARAMETER_IDENTIFIABILITY.md) closes the prior small-case-only limitation for every fixed known original size and survivor count of at least two. Its intrinsic comparable-pair density has a strictly increasing expectation within the declared optional Bernoulli family. The [finite thinning likelihood](THINNED_ORDER_LIKELIHOOD.md), [full-order likelihood](BERNOULLI_ORDER_LIKELIHOOD.md), [auxiliary-seed result](AUXILIARY_SEED_IDENTIFIABILITY.md) and [vertex-erasure convention](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md) remain unchanged dependencies. Known original size, uniform actual-subset selection and faithful completed comparisons are essential. This is distribution identifiability, not exact one-order recovery, calibration, hidden-mechanism identification or physical readout.

Independent manual review and coordinator adjudication accepted this conditional theorem. Public editorial acceptance remains separate. The assigned law-dependence continuation is pending independent admission and excluded. Earlier pending statements below remain historical.

---

## Exact likelihood after faithful uniform thinning

The reviewed [finite thinning theorem](THINNED_ORDER_LIKELIHOOD.md) pushes the accepted full-order likelihood through independent uniform fixed-size survivor selection and completed-order restriction. It separates natural-label and survivor-subset multiplicities, proves normalization/endpoints, and gives a manual three-vertex/two-survivor counterexample to naive size substitution with distribution identification in that small case. General thinning identifiability is pending; auxiliary seed nonidentifiability persists. Known true size and faithful complete comparisons are stipulated, with no physical readout or efficient computation claim.


## Native records and auxiliary seed independence

The reviewed [auxiliary-seed theorem](AUXILIARY_SEED_IDENTIFIABILITY.md) constructs distinct seed mechanisms with identical native transition kernels, all finite marked histories and coarse payload maps. The accepted native parameter remains identifiable within its family, while hidden seed independence does not follow from those records. This is a conditional representation result; physical readout and application value remain open. The five research lanes retain separate review, execution and claim boundaries.

## Reviewed finite order likelihood

The [intrinsic Bernoulli order likelihood](BERNOULLI_ORDER_LIKELIHOOD.md) gives the exact probability of a complete unlabelled order under the fixed from-empty independent-edge law. Cover and incomparable-pair counts are minimal sufficient statistics; the family is identifiable, with an interior maximum-likelihood estimate when both counts are positive and unattained endpoint suprema otherwise. This is a conditional finite mathematical result. Physical readout, inference calibration and application value remain open. The separate unknown-size height theorem and historical results retain their own premises.

# Law dependence: structural identities versus prescribed choices

18 October 2026. Bounded initial result accompanying THEOREM_PACKAGE.md.

The [20 October law-family supplement](LAW_FAMILY_SUPPLEMENT.md) proves a fixed-seed obstruction and an explicit moving-seed classification for a declared parent-five family. It keeps the possible exceptional parameter conditional and does not transfer the fixed-law 30/33/38 conclusions. See the [publication note](PUBLICATION_NOTE.md) for review and evidence boundaries.

## 1. Question and answer

Which conclusions follow from the declared record-marked growth principles, and which depend on the selected seed, normalization and canonical objective?

The principles do not uniquely select the admitted law. A concrete one-parameter alternative finite prefix is proved below. At parent size four, taking its parameter to be \(1/2\) changes the fixed-law full-slot ratio \(c_1/c_0=359/360\) while preserving strict positivity, record locality, marked equivariance and every diamond contained in that prefix.

This is a change of law, not a coordinate renormalization. It does not refute the existing fixed-law theorems. It shows why their numerical coefficients and cross-sector comparisons must not be promoted to consequences of the model principles alone.

The alternative is deliberately a **finite-prefix construction**. Keeping the old later layers unchanged is not part of the result. In particular a uniform proper-only scaling at every layer, with full complements filled independently, is not proved covariant and generally fails a mixed full/proper diamond.

## 2. Premises and exact prefix boundary

Use the conditional model of THEOREM_PACKAGE.md §1: every ideal has positive probability; full normalization; strict precursor-record locality; whole-unmarked-parent access; transported marked equivariance; fair immutable newborn bits; and complete incomparable-birth diamonds acting on the entire arbitrary complex PSD payload by \(q_1q_2/4\).

Fix any admissible law prefix through parent size \(n\ge1\). “Through parent size \(n\)” means its transitions from sizes \(0,\ldots,n\), hence through \(n+1\) births. Its largest internal diamond has base size \(n-1\), two intermediate parents of size \(n\), and terminal size \(n+1\).

Choose a single constant \(0<t\le1\), the same for every parent, marking and proper ideal at size \(n\). Define

\[
 q^{(t)}(P,r,S)=
 \begin{cases}
 q(P,r,S),&|P|<n,\\
 t\,q(P,r,S),&|P|=n,\ S\subsetneq P,\\
 (1-t)+t\,q(P,r,P),&|P|=n,\ S=P .
 \end{cases}                                             \tag{L1}
\]

No probability at parent size \(n+1\) or above is specified by (L1). Their old values are not held fixed.

### Proposition 1: complete finite-prefix admissibility

For every admitted prefix and every \(0<t\le1\), (L1) is an admitted prefix through the same parent size.

**Proof.**

For each changed complete row,

\[
 \sum_{S\subsetneq P}tq(P,r,S)+(1-t)+tq(P,r,P)=1.
\]

Every proper term is strictly positive; the full complement is positive as a convex combination of one and the old positive full probability. There is more than one eligible ideal for nonempty \(P\), so each probability is also less than one. The two newborn branches remain \(q^{(t)}/2\).

A common record-independent scalar preserves every proper locality restriction and equivariance. The full complement is permitted to depend on all marks and is equivariant by its complete row sum.

All diamonds based below size \(n-1\) are unchanged. For a diamond with base \(C\) of size \(n-1\), let its independent precursors be \(S,T\subseteq C\). Its second precursor is \(T\) in \(C+x_S\), or \(S\) in \(C+y_T\). Each is necessarily **proper in its intermediate parent**, because it excludes the other newborn. Thus both route products acquire exactly one factor \(t\):

\[
 q(C,S)\,tq(C+x_S,T)
     =q(C,T)\,tq(C+y_T,S).
 \tag{L2}
\]

This includes \(S=C\) or \(T=C\), and \(S=T\). A full *first* birth at the old base \(C\) is unchanged because \(|C|=n-1\); its corresponding second precursor is proper at size \(n\) and is scaled like every other second precursor. All old and newborn marks and the common \(1/4\) payload factor remain. Hence every diamond contained in the prefix is preserved. ∎

No exclusion of full-first-birth diamonds is used. The result depends instead on the exact location of the changed last layer.

### Why extending the same scaling rule beyond the boundary is not justified

Suppose an original admissible continuation at parent size \(n+1\) is available. Consider a diamond based at a changed parent \(P\) of size \(n\), with first precursors \(P\) and a proper ideal \(S\). Let

\[
 a=q(P,P),\ b=q(P,S),\
 c=q(P+x_P,S),\ d=q(P+y_S,P),\qquad ac=bd .
\]

If the old size-\(n+1\) rows were left unchanged, the new route products would be

\[
 [(1-t)+ta]c\quad\text{and}\quad tb\,d=tac .
\]

Their difference is \((1-t)c>0\) for \(0<t<1\). Thus that attempted extension fails. If one also applied a common proper-only scaling \(t'\) at size \(n+1\), both second factors would be scaled, leaving difference \(t'(1-t)c>0\). Uniform proper-only scaling across layers does not fix the problem.

This explicit mixed-diamond calculation is the reason (L1) is only a prefix transformation. It is not a loophole in the diamond definition.

Conditional on the admitted ratio-potential extension theorem, the changed valid prefix has some positive continuation: its new potentials must be computed from the changed prefix and its new component scales chosen consistently. Such a continuation is not the old law with unchanged coefficients, and is not an already verified continuation with any preferred geometric or optimization property.

## 3. A concrete admitted alternative and a non-invariant ratio

Apply (L1) at parent size four to the fixed admitted prefix and take \(t=1/2\). All rows at smaller sizes, including the seed, are unchanged. All proper parent-four component scales are halved in the existing potential normalization. This is an exact alternative prescription; it needs no new coefficient search.

At the four-chain, the original held values are

\[
 B_\varnothing=B_{\rm root}=1/352,\quad
 c_0=81/1100,\quad c_1=3231/44000,\quad c_1/c_0=359/360 .
\]

The alternative has

\[
 B^{(1/2)}_\varnothing=B^{(1/2)}_{\rm root}=1/704,
\]
\[
 c^{(1/2)}_0=(1+c_0)/2=1181/2200,\qquad
 c^{(1/2)}_1=(1+c_1)/2=47231/88000,
\]
\[
 \frac{c^{(1/2)}_1}{c^{(1/2)}_0}
       =\frac{47231}{47240}\ne\frac{359}{360}.             \tag{L3}
\]

Indeed \(47231/47240=1-9/47240\), whereas \(359/360=1-1/360\); their deficits differ because \(9\cdot360=3240\ne47240\).

This alternative belongs to the same conditional model through parent four. It is not asserted to preserve the optional half-height target for which the original parent-four witness was selected. Failure of that additional performance target, if it occurs, would not be failure of the model's positivity/locality/diamond principles.

### Bounded conclusion

The numerical ratio \(359/360\), and therefore the specific coefficients \(360,359,1\) in the fixed-law residual test

\[
 \mu_1=\mu_0\quad\Longleftrightarrow\quad360R_1-359R_0=1,
\]

are not forced by the declared model principles and the unchanged smaller seed alone. They use the prescribed parent-four law.

This does **not** establish that the new law has a different signed-kernel dimension, excludes the old endpoint by a different mechanism, or changes the actual \(\mu\) branch. Its parent-five optimization, canonical active support, \(\theta,\mu\), later potentials and harmonic direction have not been derived. No original formula requiring those quantities is transplanted.

If a new law separately satisfies a corresponding saturation relation
\(\sigma_i=(1-R_i)/c_i\) and has a common positive \(\mu/\sigma\) factor, then its equality test is

\[
 c_0(1-R_1)=c_1(1-R_0).
 \tag{L4}
\]

The form is elementary algebra under those explicit hypotheses. Their satisfaction for the changed canonical instance is not assumed.

## 4. Optional law choices are not coordinate gauges

### Potential gauge: no probability changes

For a ratio component \(\mathcal C\), replace a positive potential by
\(u'_{\mathcal C}=\lambda_{\mathcal C}u_{\mathcal C}\), with
\(\lambda_{\mathcal C}>0\), and replace its scale by
\(\alpha'_{\mathcal C}=\alpha_{\mathcal C}/\lambda_{\mathcal C}\).
Every product \(u'\alpha'=u\alpha\), full complement and path probability is unchanged.

This is a representation change, not a new law. A “common scale” prescription depends on the potential convention: unequal component gauges turn a common coefficient into unequal coefficients. A specified gauge must therefore precede comparisons of common-scale families.

### Harmonic normalization: distinguish a paired change from a new amplitude

For \(h_7=1+\epsilon Z\), the paired substitution
\(Z'=kZ,\epsilon'=\epsilon/k\), with \(k>0\), leaves \(h_7\) unchanged. The convention \(z_1=1\) fixes this freedom.

Changing \(\epsilon\) alone while retaining the normalized \(z\) changes \(h_7\) and the law. The sufficiently-small-amplitude theorem and the \(1/4\) rejection are not different coordinate readings of one endpoint.

### Natural versus historical coordinates

The natural identities
\(\delta x=\epsilon\delta y\),
\(W_j=e_j\delta y_{J_j}\), and
\(\delta\alpha(H)=s\epsilon\delta y_H/\prod h_7(H-v)\)
are exact representation maps at the fixed baseline and amplitude.

The historical \(u/\Gamma\) dictionary is not fully source-bound. Treating it as a gauge without first specifying its child classes, scaling and possible mixing would conceal a missing premise. The package retains the gap rather than defining it away.

### Genuine choices

The seed values, the parent-four witness, the expected-Ferrers-defect objective, whole-history weighting, canonical lexicographic ordering, the strict mixing schedule, the common half-scale continuation, the normalized harmonic direction and the requested amplitude are prescriptions beyond the basic conditional model.

Some satisfy additional design goals. That does not make those goals consequences of the diamond identities or of DET primitives. The model itself also contains chosen assumptions—fair bits, scalar-passive payload maps, and one committed birth per bookkeeping step—not yet derived from bare DET.

## 5. What remains structural under a changed law?

The ratio graph at a fixed layer is built from order/precursor/mark presentations and complete diamonds. With strict positivity and the same eligibility/locality conventions, changing positive numerical coefficients does not change which terminal presentations or compulsory marks occur. Positivity matters: admitting zero branches could invalidate cancellations and change the relevant family.

Consequently the following are structural:

- The shared-child meaning of a record-blind \(x_H\), and the affine system \(Ax=h_7\).
- The distinction between forward ideal multiplicities and backward deletion counts.
- Exhaustive carrier types for a specified terminal and their marked connectivity.
- Complete-row capacity formulas using the *new* probabilities and potentials.
- The telescoping harmonic argument and the empty-birth lift theorem when their explicit baseline/support/harmonic premises hold.

The natural numerical matrix \(A\), a selected harmonic vector \(z\), the signs of its coefficient contrasts, the canonical objective coefficients, and the minimizing active set can change.

For example, at the concrete parent-four alternative,

\[
 p_i^{(t)}=tp_i,\quad g_{ij}^{(t)}=tg_{ij},\quad
 h_*^{(t)}=th_*,\quad v_i^{(t)}=v_i,
\]

because \(p,g,h_*\) are proper parent-four probabilities while \(v\) is a parent-three probability. The two-maximum potentials for the neutral staircase carriers therefore become

\[
 e_{im}^{(t)}=t^2(p_i/v_i)g_{im},\qquad
 w_{ijm}^{(t)}=t^2g_{ij}g_{im}/v_i .
 \tag{L5}
\]

These identities describe lower-law potentials, not the new canonical allocation. If \(\xi_i^{(t)}\) denotes the new staircase component coefficient, its corresponding direct loads obey
\(Y_i^{(t)}=(p_i^{(t)}\bar g_i^{(t)}/v_i)\xi_i^{(t)}\) and
\(Z_i^{(t)}=((\bar g_i^{(t)})^2/v_i)\xi_i^{(t)}\).
Thus the algebraic coupling
\(\bar g_i^{(t)}Y_i^{(t)}=p_i^{(t)}Z_i^{(t)}\) survives for those component loads.

This does not prove that all other canonical carrier terms vanish for the changed instance. The original finite everywhere-neutral active-support result must be reproved before reducing its entire capacities to the same small subsystem.

## 6. Claim-by-claim classification

“Principle-forced” below means forced by the *declared conditional model*, not proved from DET's original ontology.

| Claim | Classification | Dependence / boundary |
| --- | --- | --- |
| Two newborn \(1/2\) factors give a full \(1/4\) diamond map | Forced identity within the fair scalar-passive model | Fairness and scalar passivity are themselves admitted assumptions |
| Component ratios constant along complete ratio edges | Forced identity with positivity | Does not select component amplitudes |
| Positive last-layer scaling (L1) | Theorem for an explicit family of admissible prefixes | Later layers must be rebuilt; cross-layer naive scaling fails |
| Numerical \(c_1/c_0=359/360\) | Example-specific | Counterexample (L3) within the same prefix model |
| Canonical carrier aliases for fixed terminal shapes | Structural theorem under complete eligibility/locality | No claim about their numerical coefficients or positivity at a boundary |
| Small-amplitude empty-birth lift | Theorem under explicit support and harmonic hypotheses | Does not supply those hypotheses for a newly chosen law |
| One-/two-dimensional natural kernel | Fixed-law theorem using stated coefficient lemmas | Not a universal property of all positive growth laws |
| 30/33/38 rejection at \(1/4\) | Fixed-law, fixed-support, fixed-amplitude theorem | Depends on \(z_2,e_2\), contrasts and prescribed restorations |
| Four marked prefix roles have equal value \(4693/17600\) | Example-specific equality | Distinct components; numerical equality is not mark erasure |
| Every active canonical component at parent five is neutral | Admitted finite instance result | Not forced for every prefix, objective, primary optimum or later layer |
| Strict mixing restores all branches | Theorem for a boundary-feasible vector and positive interior mixture | Choice of mixture schedule is optional |
| Primary minimizer versus lexicographic minimizer | Definition plus finite optimization theorem | Primary optimum can be nonunique; ordering selects one |
| Scalar canonical saturation under complete carrier slack | Conditional optimization theorem | Must retain all competitor loads and objective contributions |
| \(\bar g_iY_i=p_iZ_i\) | Structural component/load identity | Numerical loads remain selector-dependent |
| Sublinear defect / manifoldlike growth | Unproved candidate asymptotic claims | Finite low-drift or exact inverses do not establish them |
| Informative QM / physical geometry / gravity | Not established | No borrowed input may be claimed as its own derivation |

## 7. What a change invalidates, and the remaining questions

Changing an earlier layer changes later maximal-deletion products, complete row maxima, history weights, objective coefficients and canonical solutions. It can also change which sign or zero-contrast branch a later theorem occupies. Old numerical coefficients, canonical-support facts and endpoint certificates must not be reused without a new proof.

The existing theorems remain valid for their unchanged instance. The concrete alternative demonstrates nonuniqueness at the declared principle level without claiming a superior performance law or opening a search over alternatives.

The remaining questions have bounded roles:

1. The original \(\mu\) comparison is needed only for a claim selecting the actual dimension, rather than the already complete branch-conditional classification.
2. A law-comparison claim using specified contrast or support lemmas for a changed prefix must reprove those lemmas for that prefix.
3. Calling an optional normalization, objective or canonical ordering DET-forced requires an independent law-selection principle.

This result includes no coefficient sweep, new canonical allocation, xi allocation, optimization, enlarged support, uniform-coverage or noncollapse theorem, or geometry extension. It is a bounded law-dependence result accompanying the conditional theorem package, not a new theorem about the actual canonical branch or a completed historical-coordinate reconciliation.

The metric-as-record interpretation remains unvalidated, the previously retired gravity proposal is not rehabilitated, and no production readiness or missing validation evidence is supplied. Separate software and empirical projects are outside this analysis; their prior status is unchanged. The broader kinematic horizon is not a claim. No physical time, informative quantum dynamics, mass/gravity derivation or empirical discriminator follows.

## 8. Provenance and verification scope

This manual argument uses the model/ratio statements, fixed prefix values and carrier proofs summarized in §§1, 4, 8 and 9 of THEOREM_PACKAGE.md and the supporting proofs named there. Their exact source identities are recorded separately. No scientific certificate was parsed, no historical checker replayed, and no numerical alternative table computed.

Proposition 1 is a new symbolic finite-prefix proof. The mixed full/proper diamond is explicitly included as a boundary check and as a counterexample to the overbroad cross-layer variant. Equations (L3)–(L5) are manual consequences of the displayed definitions, not executed arithmetic. The fresh administrative checks concern bytes and receipts only; inherited custody limitations remain preserved.

## Law-dependent all-layer height consequence

[The height-growth theorem](HALF_SCALE_HEIGHT_GROWTH.md) derives a uniform
conditional full-birth floor and almost-sure linear intrinsic height under
the optional all-layer half-scale baseline, with the source prefix and
infinite classical history measure admitted. The prescription changes
actual probabilities and is not a coordinate gauge. Its finite-layer
alternative shows why that floor is law-dependent; it is not an infinite
sublinear-height counterexample or a universal height no-go. The proof
assumes no iid native history and gives no exact limiting speed,
coefficient-branch selection, physical dimension or validation. No result
is transferred to the separate optimizer or an unproved infinite harmonic
extension.

## Optional target choice and the intrinsic height screen

[The intrinsic target screen](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) conditions
on the selected all-layer half-scale law and declares a fixed intrinsic
target with a sublinear height envelope. It gives finite-time bounds and
an almost-sure lower bound on the normalized deletion distance. The native
law and narrower target are not forced by DET or obtained by a coordinate
gauge. Occupancy and aspect are both required for the stated Ferrers
example; thin hooks defeat aspect-only height control. The proof does not
settle unrestricted Ferrers defect, the separate optimizer, or an infinite
harmonic extension, and provides no physical readout or geometry bridge.

## Complete height drift and optional law design

[The height-drift criterion](HEIGHT_DRIFT_LAW_SELECTION.md) shows why a
candidate must control all height-spanning ideals along its actual history,
not just the full slot. Its proper-ideal example is a finite mechanism,
not an alternative all-size stochastic counterlaw. The proposed separate
height objective uses the full marked capacity polytope, actual history
weights and every ideal occurrence; strict restoration preserves conditional
admissibility but does not prove sublinear growth or geometry. Almost-sure
drift decay remains distinct from the weaker expectation and probability
modes. Paired coordinate gauges preserve the law, while changed allocations
require recomputing subsequent prefixes. No existing Ferrers objective,
physical readout or DET-forced selector is supplied or replaced.

## Universal finite-prefix neutral-support witnesses

[Neutral-support feasibility](NEUTRAL_SUPPORT_FEASIBILITY.md) proves zero
closed-boundary minima at parent sizes two and three for every admitted
strictly positive lower prefix of the corresponding length, not just an
optional numerical seed. Each is a separate next-layer construction; a
zero boundary cannot supply the positive prefix required by the next
argument. Strict next layers have positive objective and an unattained
infimum of zero. Globally neutral support must still satisfy shared row
capacities. Paired gauges preserve feasibility, while actual prefix changes
require rebuilding later layers. No all-size feasibility, asymptotic
sublinear growth, target geometry or physical readout is established.

## A selected sublinear-height law from empty

[The factorial-subset construction](FACTORIAL_SUBSET_HEIGHT_LAW.md) gives
an optional admitted all-size law, initialized from empty, with
\(\limsup H_N/\sqrt N\le2\mathrm e\) almost surely. This contrasts with
the selected half-scale law's linear height without contradicting it.
The per-subset factorial choice is neither an independent-inclusion rule
nor an arbitrary-prefix-preserving extension. Its complete height drift
is \(1-Z_{n-t(P)}/Z_n\) for nonempty parents, includes proper raising
ideals and has no asserted uniform decay over all rows. Actual-history
Cesaro drift tends to zero under this selected law. No DET-forced choice,
optimizer theorem, sharp constant, matching lower bound, geometric limit
or physical readout follows.

## Pair density under the same optional law

[The ordering-fraction theorem](ORDERING_FRACTION_OF_FACTORIAL_LAW.md)
keeps the accepted factorial-subset law fixed from empty. Its incomparable
fraction tends to zero almost surely despite its \(O(\sqrt N)\) height
bound. The proof uses independent birth coordinates and an auxiliary
filtration; it assumes no independent inclusions within a subset or
independence between paths, pairs or sizes. The target-deletion consequence
requires a separately declared fixed positive incomparable-density premise
and induced restriction of the completed order, not recomputed DAG
reachability. It does not establish that premise for Ferrers targets,
eventual total ordering, a DET-forced selector or a physical exclusion.

## A target-specific consequence for the unchanged factorial law

[The dense Ferrers screen](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md)
establishes a positive incomparable-pair density floor for the existing
target with fixed occupancy and bounded aspect. Combined with the fixed
factorial-subset law's ordering-fraction theorem, it gives induced deletion
fraction tending to one almost surely, consistently with that law's
sublinear height. The target is not narrowed to rectangles or unique
representations; a contained rectangle is proved. The hypotheses are
sufficient, with no necessity claim, and balanced thin hooks are not density
counterexamples. No conclusion is transferred to changing target parameters,
unrestricted Ferrers, another optional law, the separate optimizer or
physical geometry.

## Distinct factorial-power laws, without exact height exponents

[The factorial-power family](FACTORIAL_POWER_LAW_FAMILY.md) gives a
different optional law for each fixed integer \(q\ge1\), as witnessed by
the full-to-empty branch ratio \(2^{-q}\) at the two-vertex antichain.
Paired gauges preserve that ratio.
The family has complete positive marked admissibility and changing proved
height upper bounds; it does not establish distinct exact height-growth
exponents. Its multiblock argument proves vanishing incomparable fraction
for each fixed member, so the fixed dense occupancy/aspect target obstruction
persists. No growing or history-dependent exponent, arbitrary-prefix
preservation, universal admitted-law result, unrestricted Ferrers objective,
separate optimizer or physical interpretation is supplied.

## Quadratic subset penalty: a second incomparability behavior

The [quadratic subset-penalty law screen](QUADRATIC_SUBSET_PENALTY_LAW_SCREEN.md)
gives an explicit strictly positive admitted optional law whose height is
eventually at most \(\lceil16e[\log_2(N+1)]^2\rceil\) almost surely, while
its intrinsic incomparable-pair fraction has full-sequence lower limit at
least \(1/4096\) almost surely. Both statements hold under the same
from-empty measure. This is an upper-height result and a lower-limit result;
neither an exact height rate nor a limiting incomparability constant is proved.

At a three-vertex antichain, the full-subset/empty-subset ratio \(1/8\)
differs from \(6^{-q}\) for every fixed integer \(q\ge1\). The distinction
is an actual probability-law distinction, not a paired gauge change.
Together with the factorial-power results, it shows that the declared
admission conditions do not force vanishing incomparability across all
admitted laws. No target approximation, physical claim or arbitrary-prefix
preservation follows.

## Height obstruction despite different pair densities

The [Ferrers height and retention obstruction](FERRERS_HEIGHT_RETENTION_OBSTRUCTION.md)
gives the sharp size bound \(|Q|\le H(Q)(H(Q)+1)/2\) for filled coordinatewise
partition cell orders. The induced-retention ceiling
\(\min\{|P|,H(P)(H(P)+1)/2\}\) is sharp over parents with a given size and
height, not necessarily attained in each parent.

For the quadratic law and each separately fixed integer factorial-power law
\(q\ge2\), the accepted height bounds imply that the deletion fraction tends to one
almost surely for the unrestricted filled Ferrers cell class, under each law's own
measure. The quadratic law's positive incomparable-fraction lower limit
and this retention obstruction hold together; the earlier actual-law
distinction remains intact. At \(q=1\), height alone does not settle
unrestricted retention, while the prior fixed dense-target deletion result
still holds. This extends the obstruction to the already defined cell
class without redesigning the target or extending the result to every
admitted law, every dimension-two order, other Ferrers notions or physics.

## Joint premises close the fixed first-exponent boundary

The [joint Ferrers obstruction](FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md)
combines a square-root height upper bound with vanishing incomparable-pair
density. For the unrestricted class of filled coordinatewise partition
cell orders, it proves that the deletion fraction tends to one almost
surely for each separately fixed integer factorial-power law \(q\ge1\),
under its own measure. At \(q=1\), the additional density premise is
essential to this argument; height alone remains inconclusive.

The finite reduction fixes its parameters before varying size or choosing
a subsequence. It preserves the prior height-only results and the distinct
quadratic-law obstruction; the quadratic law's positive density lower
limit is not a vanishing-density premise. No convergence rate is extracted
from unspecified little-o, no simultaneous-law coupling is assumed, and
no target redesign, all-law theorem, all-dimension-two conclusion or
physical interpretation is supplied.

## A fixed Bernoulli law separates the retention diagnostics

The [Bernoulli-subset counterexample](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md)
provides a completely admitted optional law for each fixed \(p\in(0,1)\)
in the declared model. Under the same measure, the height and unrestricted
filled Ferrers cell retention fractions have lower limits at least \(p\),
the deletion fraction has upper limit at most \(1-p\), and incomparable-pair
density tends to zero, almost surely. The expectation bound is
\(\mathbb E_p I(P_N)\le N(1-p)/p^2\).

Only the greedy chain has the proved exact speed \(p\); no exact
longest-chain or retention limit is asserted. This law fails the joint
obstruction's square-root height premise, so it leaves that theorem and
the factorial laws unchanged. Each fixed dense occupancy/aspect target
remains obstructed, with deletion fraction tending to one almost surely. A chain is
not two-dimensional geometry. The distinction concerns actual optional
laws in the conditional model, not all DET formulations or physical
predictions, and makes no novelty claim.

## Finite observation under two specified optional law families

[Finite intrinsic-height law separation](FINITE_HEIGHT_LAW_SEPARATION.md)
provides a predeclared finite two-family rule on one exact completed
unmarked order. Its class-conditional errors apply separately to each
fixed Bernoulli \(p\in[p_0,1)\), for predeclared \(p_0\in(0,1)\), and each
fixed integer factorial-power \(q\ge1\), with the stated from-empty law
premises. The symbolic size and sufficient computation bounds do not
identify every admitted law or provide a posterior. Neither a universal
classifier, physical readout nor application execution follows. This is
an intrinsic-height observation guarantee under specified optional laws.

## A bounded erasure channel with the original law marginal

The [vertex-erasure height diagnostic](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md)
transfers the predeclared finite two-family test, with \(p_0\in(0,1)\),
to a known true integer size \(N\ge2\), a known nonnegative integer
deletion budget \(d\le\lfloor p_0(N-1)/4\rfloor\), and the exact completed
induced order on all survivors. It retains surviving
comparisons rather than recomputing reachability after deletion.
History-dependent erasure channels are allowed only while preserving the
specified generative marginal. The class-conditional errors are
unconditional over the joint law and channel at fixed \(N\), not
conditional on observed survivor count \(m\). The separately fixed
Bernoulli \(p\in[p_0,1)\) and integer factorial-power \(q\ge1\) laws retain
their from-empty premises; survivors are not a fresh \(m\)-vertex law. No physical readout,
universal classifier or application execution is supplied.

## Unknown-size observation under two specified law families

The [unknown-original-size height diagnostic](UNKNOWN_SIZE_HEIGHT_DIAGNOSTIC.md)
uses a predeclared cutoff and exact abstention rule to give finite unconditional
wrong-family error guarantees without supplying the original size to the
observer. Each experiment still has a fixed deterministic original size.
A fixed hard deletion bound, faithful completed induced survivor comparisons,
and preservation of the specified generative marginal are essential.
The result concerns the stated Bernoulli and factorial-power optional laws;
it gives no conditional-on-decision confidence, physical prediction,
acquisition channel or application result.
