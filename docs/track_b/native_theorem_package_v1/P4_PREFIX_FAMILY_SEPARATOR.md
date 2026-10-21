# A common P4 separator for an explicitly constrained prefix family

21 October 2026. Conditional manual finite-prefix theorem.

**Result.** The entire original prefix need not be fixed for this separator.
The admitted empty-slot identities give
\[
 q^0(C_4,\varnothing)=\frac1{352},\qquad
 q^0(C_5,\varnothing)=\frac{\theta}{352},\qquad
 U_0=\frac{\theta^2}{352}.
\]
Together with the already established \(U_{9,r}=\theta^2c_i\), they
cancel the member-dependent \(\theta\). The common exact law functional is
\[
 \boxed{\quad
 \mathcal G(p)=p(K_4)-\frac{648}{25}\,p(K_0).
 \quad}                                                       \tag{1}
\]
It is nonpositive on every baseline and strictly positive on every
admitted regular perturbed law in the precisely constrained family below,
even across different prefixes, nuisance parameters and hidden markings.
Each perturbed member uses its own conditional neighborhood and fixed
amplitude. No common numerical neighborhood is asserted.

The coefficient in (1) is now exactly calibrated from shared seed/held
identities. It is not a probability-effect estimate, finite-sample
guarantee or physical detector. The theorem is not universal over DET,
all canonical prefixes, or arbitrary tuples of scalar coefficients.
No second distinct qualifying prefix is constructed or established here.

## 1. Binding the empty slots to the named parents

The captured theorem package uses condensed held-row notation. The
binding must use its complete-row assertion, the actual ideal catalogues,
and the named scalar probabilities together.

Package §2 explicitly names
\[
\begin{gathered}
 I=C_3,\quad a=q^0(I,I),\quad b=q^0(C_4,I),\quad c=q^0(C_4,C_4),\\
 d=q^0(C_5,I),\quad e'=q^0(C_5,C_4),\quad f=q^0(C_5,C_5),\\
 H_5=I\oplus A_2,\quad
 g=q^0(H_5,I),\quad h=q^0(H_5,I+\text{one cap}),\quad
 j=q^0(H_5,H_5).
\end{gathered}
\]
Marks are implicit only in this displayed shorthand; all identities
retain their induced old markings.

Package §4 supplies the complete held rows over
\(\mathcal J=(\varnothing,\text{root},\text{initial pair},I)\).
The supplement §2 identifies the complete C4/H5/C5 rows, including
their full complements and the C5 singleton correction.
Unpacking these statements gives the following dictionary:

| Parent | Its complete ideal catalogue | Held-row entries |
| --- | --- | --- |
| \(C_3=I\) | \(\mathcal J\), with \(I\) full | \(A_S\), with \(A_I=a\) |
| \(C_4\) | \(\mathcal J\), then full \(C_4\) | \(B_S\), with \(B_I=b\), then \(c_i\) |
| \(H_5=C_3\oplus A_2\) | \(\mathcal J\), two individual one-cap ideals, then full | \(G_S\), with \(G_I=g_i\), then \(h_i,h_i,j_i\) |
| \(C_5\) | \(\mathcal J\), then proper \(C_4\), then full \(C_5\) | \(D_S\), with \(D_I=d_i\), then \(e'_i,f_i=\ell_i\) |

The geometric deletions check this dictionary: deleting the unique
maximum of \(C_5\) leaves \(C_4\), so the proper-slot potential for
\(S\in\mathcal J\) is \(B_S\). Deleting one or both caps of \(H_5\)
leaves \(C_4,C_4,C_3\), giving \(B_S^2/A_S\).
These are exactly the linear and quadratic entries of the printed
held identities
\[
 G_S=\theta B_S^2/A_S,\qquad
 D_S=\theta B_S+\mu_i\mathbf1_{\{S=\text{root}\}}.             \tag{2}
\]
The scalar anchors and complete complements agree as well:
\(D_I=d_i=\theta b_i\), \(e'_i=h_i=\theta c_i\),
\(f_i=\ell_i=1-\theta-\mu_i\), and
\(j_i=1-\theta Q_{2,i}-2\theta c_i\).
The supplement's \(e\) is the package's \(e'\), not its
smaller-seed \(e=1/44\).

This is an explicit unpacking of the admitted complete probability rows.
The deletion shapes alone would not select their component coefficients.
Nor would the isolated scalar symbols, without the complete-row premise,
justify identifying an arbitrary \(B_\varnothing\) with a C4 probability.

For the empty ideal the singleton indicator in (2) is zero.
The printed \(B_\varnothing=1/352\) therefore gives the actual slots
\[
 e_4:=q^0(C_4,\varnothing)=\frac1{352},\qquad
 e_5:=q^0(C_5,\varnothing)=D_\varnothing
                       =\theta B_\varnothing=\frac{\theta}{352}.
                                                               \tag{3}
\]
Proper-slot locality independently makes these empty-slot probabilities
mark-independent. Equivariance identifies isomorphic induced chains.
Neither principle fixes their numerical values: those come from the
admitted seed/witness and canonical held-law identities.

No original coefficient certificate is opened, re-executed or reconstructed.
The proof uses the accepted complete-row exposition, not a new
canonical-support or optimization argument.

## 2. Exact cancellation in the P4 calculation

Keep the tested parent class
\[
 P_4=C_4\oplus A_2
\]
with caps \(a,b\). The original prefix may later vary across family
members, but the parent and the two observed child shapes do not.
\(K_0\) is the empty-birth shape and \(K_4=T_9\) the C4-birth shape.
[The child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md) identifies them intrinsically by the maximal-principal-downset
multisets \(\{1,5,5\}\) and \(\{5,5,5\}\).
Each comes from one individual ideal; its two fair newborn bits sum
to the ideal probability.

At parent five apply the accepted proper-slot scaling by \(\lambda\),
with full complements rebuilt. Parents through four remain unchanged.
For either selected ideal, maximal deletion of the two caps gives
\[
 u_\lambda(P_4,r,S)=
 \frac{q_\lambda(P_4-a,r|,S)\,q_\lambda(P_4-b,r|,S)}
      {q^0(C_4,r|,S)}.
\]
Both numerator parents are five-chains and both selected ideals are
proper in them. Thus each numerator contributes one \(\lambda\).
The denominator is unchanged, including its full slot when \(S=C_4\).

Using (3), and the admitted all-mark identities
\(q^0(C_4,r,C_4)=c_i\) and
\(q^0(C_5,r',C_4)=\theta c_i\), yields
\[
 U_0=\frac{e_5^2}{e_4}=\theta^2 e_4=\frac{\theta^2}{352},
 \qquad U_{9,r}=\frac{(\theta c_i)^2}{c_i}=\theta^2c_i.       \tag{4}
\]
Here \(i\) is the chain root bit. Record locality alone would not make
the C4 full probability root-only; that step uses the complete held
all-mark identity.

The resulting two baseline probabilities, at common positive six-parent
scale \(\rho\), are
\[
 B(K_0)=\rho\lambda^2\theta^2 e_4,\qquad
 B(K_4)=\rho\lambda^2\theta^2c_i.                            \tag{5}
\]
For any hidden old-mark distribution, replace \(c_i\) by
\(\bar c\in[c_1,c_0]\). There is no averaging of numerator and denominator
factors before (4): the deletion calculation holds separately for every
marking, and only the resulting probabilities are mixed.

The two endpoint ratios are consequently
\[
 R_{\min}=\frac{c_1}{e_4}=352c_1,\qquad
 R_{\max}=\frac{c_0}{e_4}=352c_0
                         =\frac{648}{25},\qquad
 \frac{R_{\max}}{R_{\min}}=\frac{360}{359}.                  \tag{6}
\]
The common constants are
\[
 e_4=\frac1{352},\qquad c_0=\frac{81}{1100},\qquad
 c_1=\frac{3231}{44000}=\frac{359}{360}c_0.
\]
Unknown \(\theta\), and indirectly the original prefix choices determining
it, no longer enter the separator coefficient. Unknown \(\mu_i\) does
not enter the baseline ratio endpoints (6); it may still affect the
member's perturbation multiplier and accepted neighborhood.

## 3. A declared family of actual prefixes, not scalar candidates

Let \(\mathcal F\) be any collection, possibly a singleton, of complete
canonical prefixes \(q^{(\alpha)}\) satisfying all the following
requirements. The index \(\alpha\) names
an actual law, not an independently assigned tuple
\((\theta,\mu_0,\mu_1)\).

1. **Complete validity and canonical provenance.** Each member is a
   positive, normalized, equivariant, record-local prefix through parent
   five, on every parent, ideal and old marking, with the admitted
   complete unnormalized scalar-passive diamond identities and fair
   newborn bits. It has a justified instance of the stated
   primary-then-ordered-lexicographic parent-five
   construction and strict restoration. Its \(\theta_\alpha,\mu_{\alpha,i}\)
   are those of that law, not free numbers chosen from the printed bounds.
   The smaller seed conventions are retained. Off-held prefix entries
   may differ only if an actual valid canonical construction permits them.

2. **Common held calibration.** On every induced marking,
   \[
   \begin{gathered}
    q^{(\alpha)}(C_4,\varnothing)=e_4=1/352,\qquad
    q^{(\alpha)}(C_5,\varnothing)=\theta_\alpha e_4,\\
    q^{(\alpha)}(C_4,r,C_4)=c_i,\qquad
    q^{(\alpha)}(C_5,r',C_4)=\theta_\alpha c_i,\qquad
    \theta_\alpha>0,
   \end{gathered}                                             \tag{7}
   \]
   with the same \(c_0,c_1\) as (6). These are required shared
   identities, not consequences of allowing an arbitrary earlier witness.
   The package's complete held tables supply them for its admitted
   instance. A different candidate member must justify them for its own
   complete law.

3. **Admitted family operations.** For each baseline parameter
   \(0<\lambda\le1\), the parent-five proper scaling and complete full
   complements are valid, with parents through four unchanged.
   The rebuilt six-parent layer uses an admitted common positive scale
   \(\rho\) over its entire marked domain and the complete deletion
   potential. Every complete row and both newborn bits are retained.

The perturbable subclass additionally requires its **own** established
regular construction on the same eleven unmarked child classes.
All extra held identities, full marked harmonic equations and nonzero
pivots needed by that construction must be justified for the member;
(7) alone does not supply them.
Condition on that member's
\[
 \Xi_\alpha=\theta_\alpha+360\mu_{\alpha,1}-359\mu_{\alpha,0}>1,\quad
 \lambda_{\alpha,*}=\Xi_\alpha^{-1}\in(0,1),\quad
 \kappa_{\alpha,*}>1,\quad 0<\theta_\alpha<10^{-10}.
\]
Its fixed amplitude is
\(\eta_{\alpha,*}=(2\kappa_{\alpha,*})^{-1}\).
It must have an admitted compact neighborhood \(\mathcal I_{\alpha,*}\)
on which the complete perturbed rows are positive and normalized,
\(K_0\) and the full birth are unchanged, and
\[
 \big|\eta_{\alpha,*}(v_{\alpha,j}(\lambda)-w_{\alpha,j})\big|
           \le\frac14,\qquad
 w_{\alpha,9}=\frac{2\kappa_{\alpha,*}^2}
                   {\lambda_{\alpha,*}\theta_\alpha}.       \tag{8}
\]
The amplitude is fixed as \(\lambda\) varies within one member;
it need not be identical between different members.

This is an explicit conditional class of valid prefixes with shared
identities. No claim is made that the scalar bounds alone are sufficient
for membership, that all canonical prefixes satisfy (7)–(8), or that
another member can be obtained by independently varying \(\theta,\mu\).
The cited sources establish one fixed admitted original prefix; they
do not establish two distinct members of this enlarged class.
With its entire earlier witness and canonical selector fixed, that
original construction is already uniquely specified.
The present theorem does not manufacture additional realizable laws
or decide whether any actual member has \(\Xi_\alpha>1\).

The algebra below uses complete validity, (7), the admitted family
operations and the stated regular construction. Canonical provenance
and the smaller seed identify the intended research lane; their
optimization objective and ordered selector are not additional steps
in the separator proof.

## 4. One functional across different prefixes and nuisances

For any \(\alpha\in\mathcal F\), hidden marking distribution \(\pi\),
and admitted baseline \((\lambda,\rho)\), put
\[
 \bar c_\pi=\pi(i=0)c_0+\pi(i=1)c_1\in[c_1,c_0],
 \qquad s_\alpha=\rho\lambda^2\theta_\alpha^2>0.
\]
Equations (4)–(7) give
\[
 B_{\alpha,\lambda,\rho;\pi}(K_0)=s_\alpha e_4,\qquad
 B_{\alpha,\lambda,\rho;\pi}(K_4)=s_\alpha\bar c_\pi.
\]
For a perturbable member and \(\lambda\in\mathcal I_{\alpha,*}\),
\[
 Q_{\alpha,\lambda,\rho;\pi}(K_0)=s_\alpha e_4,\qquad
 Q_{\alpha,\lambda,\rho;\pi}(K_4)
                   =s_\alpha h_{\alpha,9}(\lambda)\bar c_\pi.
\]
No other shape is removed or renormalized.

From (8), separately for each perturbable member,
\[
 h_{\alpha,9}(\lambda)
 \ge\frac34+\frac{\kappa_{\alpha,*}}
                   {\lambda_{\alpha,*}\theta_\alpha}
 >\frac74>\frac{360}{359}.                                 \tag{9}
\]
There is no need for a common interval or amplitude to deduce this common
inequality. It is a symbolic multiplier comparison, not an evaluated
probability effect.

The same functional (1) therefore satisfies
\[
 \mathcal G(B_{\alpha,\lambda,\rho;\pi})
                    =s_\alpha(\bar c_\pi-c_0)\le0,
\]
\[
 \mathcal G(Q_{\alpha,\lambda,\rho;\pi})
 =s_\alpha\big(h_{\alpha,9}(\lambda)\bar c_\pi-c_0\big)
 \ge s_\alpha\big(h_{\alpha,9}(\lambda)c_1-c_0\big)>0.       \tag{10}
\]

**Common-family separation theorem.** Every admitted baseline built
from any member \(\alpha_0\in\mathcal F\) differs as a complete
unmarked P4 child-shape law from every admitted perturbed law built
from any perturbable member \(\alpha_1\), at its own
\(\lambda_1\in\mathcal I_{\alpha_1,*}\).
The two original prefixes, nuisance parameters and hidden marking
distributions may all differ.

**Proof.** Equal full laws would have equal values of the same bounded
linear functional (1), contradicting (10). \(\square\)

The ratio intervals give the equivalent statement: all baseline ratios
are at most \(648/25\), while every perturbed ratio exceeds that number.
Thus the original entire-prefix equality is replaceable by the precisely
shared calibration and member-validity premises above.
This theorem concerns model labels, not recovery of the prefix,
nuisance parameters, root mixture or actual \(\Xi\).

## 5. Separate corollary: mixtures across admitted family members

A mixture over prefixes or law parameters is a different experiment
from a fixed member's conditional law. Nevertheless, the common
functional gives a limited corollary without further coefficient work.

Take any probability mixture of admitted baseline shape laws, and
independently any probability mixture of admitted perturbed shape laws.
The latter probability measure is concentrated on actual admitted laws
satisfying their own conditional occurrence, positivity and neighborhood
requirements; this is not a claim about topological support or closure.
For finite or countable mixtures, complete laws and (10) directly give
\[
                  \mathcal G(\overline B)\le0,\qquad
                  \mathcal G(\overline Q)>0.                \tag{11}
\]
For a general probability mixture, require the seven shape probabilities
to be measurable functions of the mixing index. Their integrals then
define a complete probability law on the same finite shape space.
The functional is bounded, so linearity of integration applies.
Its perturbed integrand is strictly positive almost surely; its integral
is strictly positive even without a uniform lower bound.
For example, the sets where that integrand is at least \(1/n\) exhaust
its positive set, so at least one has positive measure.

This corollary allows dependence between the prefix, parameters and
marking distribution within a mixture. It does not mix baseline and
perturbed labels inside the purported perturbed class, admit zero-scale
boundary laws, or transfer positivity to nonmembers.
No history process, changing-parameter trajectory, sampler or physical
preparation channel is constructed. Arbitrary mixtures remain mixtures
of established complete laws, not recipes for making a new canonical
prefix.

## 6. Exact limits of the calibration

The cancellation does not follow from locality and equivariance alone.
Those principles imply empty-slot mark independence and transport across
isomorphic induced chains. They do not select
\(e_4=1/352\), \(e_5=\theta e_4\), the root-only full-chain table,
\(c_i\), the canonical objective, its ordering/restoration, the common-scale
law choice, or the regular perturbation and amplitude.
These are retained optional construction or admitted instance premises.

A useful boundary statement follows without asserting any new laws.
If a broader class retained \(U_{9,i}=\theta_\alpha^2c_{\alpha,i}\)
but allowed unrelated positive \(U_{0,\alpha}\), define its actual
baseline ratio endpoints
\[
 R_{\alpha,\max}=\max_i\frac{\theta_\alpha^2c_{\alpha,i}}{U_{0,\alpha}},
 \qquad
 R_{\alpha,\min}=\min_i\frac{\theta_\alpha^2c_{\alpha,i}}{U_{0,\alpha}}.
\]
A separator of the specific form \(p(K_4)-C p(K_0)\), nonpositive on
every baseline and strictly positive on every perturbed mixture of
markings, exists exactly when a finite real \(C\) satisfies
\[
 R_{\alpha,\max}\le C
       \quad\hbox{for every baseline member},\qquad
 h_{\beta,9}(\lambda)R_{\beta,\min}>C
       \quad\hbox{for every admitted perturbed member/parameter}. \tag{12}
\]
Necessity follows by taking pure root sectors; sufficiency follows by
their convex intervals and positive \(K_0\) mass.
A strict inequality against the infimum of all perturbed endpoints
is not necessary if that infimum is unattained.
For the class in §3, (6) and (9) explicitly supply \(C=648/25\).

Failure of (12) for another class would reject this particular oriented
two-shape functional, not prove full-law overlap or eliminate other
distinguishing statistics. No broader coefficient family or overlap
example is constructed here.

## 7. Exact calibration is not stability or physical observation

The coefficient \(648/25\) is an exact known constant in this
seed-calibrated mathematical class. Its availability is stronger than
leaving \(R_{\max}=\theta^2c_0/U_0\) unevaluated.
But the separation value in (10) still carries the factor
\(\rho\lambda^2\theta_\alpha^2\).

Fix one perturbable member and one admitted \(\lambda\).
Sending its positive common-layer scale \(\rho\) toward zero makes
every proper probability \(O(\rho)\) in each complete marked row,
while the unchanged full-birth shape \(K_f\) approaches probability one.
The same is true after any hidden-mark mixture.
Thus baseline and perturbed families still have \(\delta_{K_f}\)
in their closures. Scale zero is not an admitted member; no claim
based merely on \(\rho\lambda^2\to0\) with varying \(\lambda\) is used.
There is no uniform positive absolute probability margin, sample size,
error bar, or numerical effect bound in this result.

The fixed seed/held calibration, canonical-prefix validity, specified
P4 parent, eleven-class perturbation support and full marked harmonic
construction remain dependencies.
Observed shapes still require exact complete unmarked child-order access.
Labels, newborn identity, parent embedding and hidden old markings are
unnecessary for recognizing these two shapes, but no physical procedure
for obtaining that order is supplied.
Missing/noisy relations, empirical correspondence, QM reconstruction,
geometry/gravity and all-size growth are not established.
No fixed-pair or uniform-family statistical sufficiency is inferred.

## Public premises and evidence scope

The [theorem package](THEOREM_PACKAGE.md), §§1–4, and
[law-family supplement](LAW_FAMILY_SUPPLEMENT.md), §2, state the admitted
complete held rows, named parent/ideal probabilities and canonical-prefix
premises used in the dictionary. Their complete-row assertions and scalar
anchors are used together; notation or deletion shapes alone do not select
the held probabilities. References to captured expositions concern retained
private originals. The public expositions do not newly authenticate original
coefficient certificates or establish a second distinct qualifying prefix.

The [marking-mixture theorem](P4_MARKING_MIXTURES.md) supplies the fixed-prefix
hidden-mark comparison and its interval argument. The
[nuisance-identifiability theorem](P4_NUISANCE_IDENTIFIABILITY.md) distinguishes
exact model-label separation from parameter recovery and finite-sample
stability. The [child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md) supplies
intrinsic recognition of the two selected shapes. The
[baseline-scale theorem](BASELINE_SCALE_THEOREM.md) states the complete scaling,
deletion-potential and admitted common-scale construction. The
[regular-family theorem](REGULAR_OBSERVABLE_FAMILY.md) supplies the established
regular construction for its admitted fixed instance. Each additional
perturbable family member must justify its own construction, neighborhood
and fixed amplitude as required in §3.

All mathematics is manual.

The family may be a singleton and consists of actual complete laws satisfying
the declared membership conditions, not freely assigned scalar tuples.
The coefficient 648/25 calibrates the stated law functional; it is not a
numerical probability effect or a uniform absolute margin. The general-mixture
corollary retains measurability and almost-sure strict positivity on admitted
laws. The boundary criterion is pointwise and retains the unattained-infimum
qualification. No all-canonical-prefix, universal DET, statistical-sufficiency,
finite-sample stability or physical observation claim is added.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. Public dependency links identify mathematical
premises; they do not supply private custody records or original certificate
reproduction. This edition is conditional mathematical exposition, not an
executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).
