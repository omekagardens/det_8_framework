# RI-22 — scalar independence does not fix event-pair composition

14 September 2026 UTC. **CONDITIONAL_COMPOSITION_COUNTERMODEL;
ORDINARY_TENSOR_LAW_NOT_DERIVED_FROM_THE_LISTED_WEAKER_PREMISES.**
Independent complete mathematical and source/premise reviews passed;
three further complete coordinator reviews accepted this conditional proof/design. This is proof/design only: no existing
composition source, instrument, axiom or accepted theorem is changed.
[RI-21](QR_FINITE_COPY_WITNESS_PLAN.md) is accepted and published at
`14eba182f6d7f5ef3d8b709a9bb810403b0d4c19`, tree
`0c284b0625f5dd288ea7f40301260fe40b8df84e`, with accepted note SHA256
`62887089c6f661f543e066f23d2d141200c9d0b67f9cafa8dd06765072e12517`.
Publication was verified by the coordinator, which retains all git/index
ownership and separate acceptance authority for this note.

**Decision.** The alternative product below preserves a substantial list of
scalar consistency and marginal properties, admits every individually
normalized complex PSD kernel, and also admits a non-PSD kernel. It omits
the imaginary-by-imaginary term of ordinary tensor multiplication. Therefore
those weaker properties do not derive the full event-pair tensor law or
strong positivity. This is a countermodel to the **listed premises only**,
not an extension preserving the accepted QR instruments or a physical theory.

The matrix/tensor arguments are elementary and make no novelty claim.
[Dowker–Wilkes section 3, equations (3.3) and (3.5)](https://arxiv.org/html/2011.06120v2#S3)
explicitly impose multiplication on rectangular **event pairs**, then extend
by biadditivity. [Boës–Navascués equation (5)](https://arxiv.org/html/1609.09723v3#S2)
uses the same full-pair premise. That is stronger than multiplying diagonal
scalar event weights. Altering it does not refute their theorems or
[RI-20](QR_COMPOSITION_PREMISE_PLAN.md) and RI-21, which retain that premise.

## 1. Candidate class and alternative product

On an n-alternative carrier, n>=1, decompose a Hermitian matrix uniquely as

\[
D=R+iJ,\qquad R^T=R\in\mathbb R^{n\times n},\quad
J^T=-J\in\mathbb R^{n\times n}.
\]

R here means the **real-part matrix**, not a committed record. The original
record/residual distinction remains separate. Define the unnormalized cone
and normalized class

\[
\mathcal C_n=\{R+iJ:R\succeq0,\ J^T=-J\},\qquad
\mathcal A_n=\{D\in\mathcal C_n:M(D)=1\},\quad
M(D)=\mathbf1^\dagger D\mathbf1=\mathbf1^T R\mathbf1.
\tag{1}
\]

The ambient Hermitian space is a real vector space; the normalized class
is a convex slice, not a vector space. Composition ranges over **variable
carrier sizes**, with a product of n- and k-alternative objects having nk
alternatives. Complex scalars, biadditive event functions and this cone are
chosen mathematical inputs, not new DET consequences. M is total-entry
normalization mass, not trace, physical rest mass or a faithful norm.

For D=R+iJ and E=S+iK define

\[
\boxed{D\star E=R\otimes S+i(J\otimes S+R\otimes K).}
\tag{2}
\]

The composite carrier is the ordered Cartesian product, with its full Boolean
event algebra. For any matrix X its biadditive event-pair value is
X(A,B)=chi_A† X chi_B and its scalar weight is mu_X(A)=X(A,A).
Product origins and known records stay separately labeled. Formal scalar
factorization does not establish physical independent preparation.

## 2. Conditional countermodel theorem: preserved properties

**Theorem.** The classes (1) and rule (2) have the following properties.

| Property | Result and exact scope |
|---|---|
| Hermitian closure | C_n star C_k lies in C_nk |
| Weak positivity | Every Boolean event of every such composite has a nonnegative weight |
| Normalization | M(D star E)=M(D)M(E); hence A_n star A_k lies in A_nk |
| Associativity | Holds under canonical ordered-carrier identification |
| Swap and factor-permutation covariance | Holds under the corresponding index permutations |
| Unit | The one-alternative kernel [1] is a left and right unit |
| Linearity | Real bilinearity on ambient Hermitian spaces; separate convex affinity on normalized classes |
| Individual quantum kernels | Every complex Hermitian PSD D with M(D)=1 belongs to A_n |
| Non-PSD member | Di=[[1/2,i],[-i,1/2]] belongs to A_2 but has eigenvalues 3/2,-1/2 |
| Fixed signed seed | b=(1,-1,1), B=bb† belongs to A_3, with M(B)=1 and Tr(B)=3 |

**Proof.** R⊗S is real symmetric PSD. J⊗S+R⊗K is real antisymmetric,
so (2) is Hermitian and in the claimed cone. For any real indicator x,
x^T(J⊗S+R⊗K)x=0. Thus

\[
\mu_{D\star E}(A)=\chi_A^T(R\otimes S)\chi_A\ge0.
\tag{3}
\]

The same reasoning proves weak positivity for every member of C_n, and
summing whole-carrier indices gives M(D star E)=M(D)M(E). Induction applies
to arbitrary finite repeated or mixed star composites.

For F=T+iL, both parenthesizations expand to

\[
R\otimes S\otimes T
+i(J\otimes S\otimes T+R\otimes K\otimes T+R\otimes S\otimes L).
\tag{4}
\]

This proves associativity; permuting factors permutes the displayed terms,
and [1] has real part one and antisymmetric part zero. Real-part and
imaginary-part extraction on Hermitian matrices are real-linear, giving
ambient real bilinearity and the stated normalized affinity. If D is complex
PSD, then for every real x, x^T R x=x† D x>=0, so R is real PSD. This
proves individual inclusion, not equality of the classes. Di has R=I_2/2
and the stated negative eigenvalue. The seed is real PSD with total-entry
mass |1-1+1|²=1 and trace three. ∎

Inclusion of individual quantum kernels is not preservation of their usual
composites. For example Q=[[1/2,i/2],[-i/2,1/2]] is a normalized rank-one
PSD projector. Q star Q has eigenvalues 3/4,1/4,1/4,-1/4, and is not PSD,
although its scalar Boolean weights remain nonnegative. Thus this is not
an ordinary complex-QM subtheory with its tensor rule left intact.

### Complex bilinearity is not an exclusion

For an arbitrary complex matrix A, let A_a=(A-A^T)/2 and A_s=(A+A^T)/2,
using **transpose, not adjoint**. Then

\[
A\star B=A\otimes B-A_a\otimes B_a
=A_s\otimes B_s+A_a\otimes B_s+A_s\otimes B_a
\tag{5}
\]

is a complex-bilinear extension of (2): on the Hermitian slice A_a=iJ and
B_a=iK. Transpose is complex-linear, so no conjugate-linearity obstruction
appears. The symmetric part of (5) is A_s⊗B_s and its antisymmetric part
is A_a⊗B_s+A_s⊗B_a; the same expansion as (4) proves associativity of the
extension. Hermitian spaces themselves are still only real vector spaces.
Requiring complex bilinearity alone therefore does **not** eliminate this law.

## 3. Complex marginals, scalar independence and real-map naturality

### Whole-carrier marginals retain the complex entries

For normalized E, sum both E indices in the composite matrix. Because
sum_ab S_ab=1 and sum_ab K_ab=0,

\[
\sum_{a,b}(D\star E)_{(i,a),(j,b)}=R_{ij}+iJ_{ij}=D_{ij}.
\tag{6}
\]

The other whole-carrier marginal is E when D is normalized. More generally
the marginals are M(E)D and M(D)E. These are full **complex** event-functional
marginals, not partial traces. Formally retaining J in a marginal does not
make J observable through scalar event weights.

For local events A and C, skew symmetry gives J(A,A)=K(C,C)=0, and hence

\[
\mu_{D\star E}(A\times C)
=R(A,A)S(C,C)=\mu_D(A)\mu_E(C).
\tag{7}
\]

This is exact scalar rectangular-event independence. It is not factorization
of arbitrary event-pair values and not evidence of an actual preparation law.

### Separate real incidence maps commute with composition

For real rectangular matrices U,V, define Gamma_U(D)=UDU^T. On unnormalized
spaces, R maps to URU^T>=0 and J to UJU^T, which is real antisymmetric.
The Kronecker identity gives

\[
\Gamma_U(D)\star\Gamma_V(E)
=\Gamma_{U\otimes V}(D\star E).
\tag{8}
\]

This holds for real matrices generally, including Boolean incidence matrices;
no disjointness assumption is required for the unnormalized identity.
A partition coarse-graining matrix has one 1 per input column, so U^T1=1
and M(Gamma_U(D))=M(D). Such maps preserve normalized membership. They are
a **sufficient, not exclusive** family: U^T1=±1 also suffices for a real U.

Arbitrary overlapping or real maps need not preserve mass. For example
U=[[1,0],[1,1]] and D=I_2/2 give output mass 5/2, not one. A nonzero output
can even have zero mass: U=[[1,-1],[-1,1]] with D=I_2/2 gives
[[1,-1],[-1,1]], whose mass is zero. Thus normalization may only be applied
with an explicitly positive resulting mass; it is not part of (8), and
post-normalization need not retain separate affinity. Real congruence algebra
does not grant physical control or preparation availability.

## 4. The missing full event-pair law

Ordinary tensor multiplication contains the additional real term

\[
D\otimes E=R\otimes S-J\otimes K
+i(J\otimes S+R\otimes K)
=(D\star E)-J\otimes K.
\tag{9}
\]

For arbitrary local events A,B,C,F this gives

\[
(D\star E)(A\times C,B\times F)
=D(A,B)E(C,F)+J(A,B)K(C,F).
\tag{10}
\]

The correction vanishes for diagonal event pairs as in (7), but not generally.
For D=E=Di, the entry connecting histories (1,1) and (2,2) under star is
zero, whereas D_12 E_12=i²=-1. Full complex marginals and scalar independence
therefore do not determine this pair entry.

**Narrow sufficiency theorem.** On finite full Boolean algebras, if a
biadditive composite G obeys

\[
G(A\times C,B\times F)=D(A,B)E(C,F)
\quad\text{for all }A,B,C,F,
\tag{11}
\]

then G is the ordinary tensor functional. Indeed, apply (11) to singleton
event pairs to obtain every atomic entry
G_{(i,a),(j,b)}=D_ij E_ab. Finite biadditivity then fixes every other event
pair by summing these entries. Conversely ordinary tensor multiplication has
(11). This proves sufficiency/uniqueness **given** the full-pair law, not a
DET derivation of that law from scalar independence.

Requiring only real parts of some pair values, one selected record partition,
complex bilinearity, or diagonal rectangle weights does not supply (11).
The exact scope of any stronger replacement premise must be proved separately.

## 5. RI-21 under the changed product law

Induction on (2) gives

\[
D^{\star m}=R^{\otimes m}
+i\sum_{s=1}^m R^{\otimes(s-1)}\otimes J\otimes R^{\otimes(m-s)}.
\tag{12}
\]

No term with two or more J factors survives. With the same real seed B,
the real part of D^star(m) star B is R^tensor(m) tensor B, a PSD matrix.
All Boolean scalar weights therefore equal those computed from that real
matrix. In particular the **unchanged event definition** from
[RI-21 section 3](QR_FINITE_COPY_WITNESS_PLAN.md#3-explicit-boolean-event-and-determinant-identity)
now has weight

\[
\mu_{D^{\star m}\star B}(E_I)=m!\det(R_I)\ge0,
\tag{13}
\]

not m!det(D_I). Whole-carrier padding preserves this identity because
M(R)=M(D)=1. For Di, R=I_2/2 gives the two-copy parity event weight +1/2;
ordinary tensor composition gives -3/2. Explicitly, the star event contains
((1,2),0) and ((2,1),1); its two diagonal weights are 1/4 each and its
off-diagonal pair terms vanish. No seed coordinate or event history is erased.

This is a changed tensor-law premise, **not a counterexample to RI-21**.
The fixed seed is still normalized with its third alternative intact and
is not truncated into a zero-mass two-marker preparation. Likewise, the
strong-positivity selection theorems in RI-20 assume ordinary tensor closure,
not closure under an arbitrary associative product. The original real D3
countermodel is not a member of this new class, since its real part is not
PSD; Di is the required surviving non-PSD member here.

## 6. Material operational limits: lineality and scalar blindness

For n>=2 the cone C_n is closed and convex but **not pointed**:

\[
\mathcal C_n\cap(-\mathcal C_n)
=\{iJ:J\in\mathbb R^{n\times n},\ J^T=-J\}.
\tag{14}
\]

Both R and -R can be PSD only when R=0, proving the equality. Every
nonnegative real-linear scalar functional f on C_n must satisfy f(iJ)=0,
because iJ and -iJ both lie in the cone. Therefore all such functionals
factor through R. More explicitly they are exactly

\[
f(R+iJ)=\operatorname{Tr}(HR),\qquad H=H^T\succeq0\text{ real}.
\tag{15}
\]

This follows by representing a real-linear functional on real symmetric
matrices by trace pairing and testing all xx^T. No positive scalar functional
on this whole cone separates different retained J values with the same R.
Normalization mass is not faithful: nonzero iJ has mass zero; even a nonzero
real PSD R with R1=0 can have mass zero. The accepted faithful-cone/base-norm
results are therefore not inherited. For n=1 there is no skew sector; that
degenerate case does not remove the n>=2 countermodel.

If supplied **all** Boolean base weights exactly, one recovers the real part:
R_ii=mu({i}) and
2R_ij=mu({i,j})-mu({i})-mu({j}). But no such weight depends on J. Under
star composition and real congruences, the output real part depends only on
the input real parts. Induction therefore keeps J invisible throughout any
finite expression in that declared catalogue followed by scalar event tests.
Positive-mass normalization also depends only on R. These comparisons require
the same actual operations and observed metadata; distinct origins/records
are not erased to create observational equivalence. Complex marginal entries
remain formally present without becoming a scalar observation oracle.

**Weights are not automatically bounded operational effects.** If in addition
0<=f<=M on the entire cone, (15) implies
0<=H<=11^T. Since 11^T has rank one, H=a11^T with 0<=a<=1, so f=aM.
For x orthogonal to 1, positivity forces x^T Hx=0 and hence Hx=0, proving
the rank-one restriction. Thus these mass-dominated effects do not even
separate all normalized R. The formal Boolean weights used above need not
be mass-dominated: the seed's event {0,2} has weight four although M(B)=1.
There is no contradiction; these weights are not all probabilities of cells
in one available recorded partition. No faithful/proper operational cone or
scalar tomography of the full D has been constructed.

## 7. Stronger premises that exclude the countermodel

| Additional requirement | What it excludes or establishes | What it does not prove by itself |
|---|---|---|
| Full event-pair rectangle multiplication and biadditivity | Fixes ordinary tensor composition by (11), excluding this star rule on the full class | Admission of the seed/copies, or physical availability of every event |
| A pointed raw cone or positive scalar effects separating all retained states | Excludes the full lineal C_n for n>=2 | PSD or ordinary tensor composition; quotienting J instead gives a different real theory |
| Available positive tests v†Dv for every complex direction v | Forces D>=0 by definition of PSD, excluding Di | Why all those tests are admissible or physically available from DET |
| Preservation of this whole class by arbitrary complex congruences, including admissible reads | Fails, as the exact unitary witness below demonstrates | That any existing narrow QR control is available globally on this class |
| Usual PSD joint composition for all individually PSD quantum inputs | Fails for Q star Q above | A derivation of that stronger quantum-subtheory premise |
| Complex bilinearity alone | **Does not exclude** the law: extension (5) is complex bilinear | Full event-pair factorization or PSD |

For an exact normalized failure under a complex unitary, use

\[
U=\begin{pmatrix}3/5&4i/5\\4i/5&3/5\end{pmatrix},\quad UU^\dagger=I,
\qquad
U D_i U^\dagger=
\begin{pmatrix}73/50&-7i/25\\7i/25&-23/50\end{pmatrix}.
\tag{16}
\]

The output still has total-entry mass one, but its second singleton weight
is -23/50. Thus this stronger control-availability/positivity premise would
exclude the full countermodel even without renormalization. Alternatively,
the complex direction v=(1,i) has v†Di v=-1. Neither calculation grants
that control or read to the declared catalogue.

The repository does **not** silently supply the needed global premise:

- [PairKernel.compose](../../det8/models/pair_kernel.py), lines 309–319,
  implements the ordinary tensor entries, unchanged. Its PSD-domain theorem
  is a conditional sufficiency result, not selection among these weaker laws.
- [RI-08b controls](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md),
  lines 10–22 and 33–66, begin within a four-atom PSD exact-recordability
  domain and supply particular H/P/Z lifts and a terminal read. Lines 128–132
  expressly distinguish arbitrary-U algebra from arbitrary-U availability.
  They do not define every raw complex congruence on this new pre-PSD class.
- [RI-08d](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md),
  sections 1 and 7, supplies one tensor/coupler/read interface and denies a
  full joint-state or arbitrary-control availability claim. Changing its
  composition would change the accepted premises; this note does not do so.
- [RI-20's premise ledger](QR_COMPOSITION_PREMISE_PLAN.md#7-det-wide-premise-ledger-assumed-proved-still-missing)
  and [RI-21's resource ledger](QR_FINITE_COPY_WITNESS_PLAN.md#7-premises-to-result-ledger-and-the-remaining-det-gap)
  retain ordinary tensor multiplication as supplied. Their proofs and sources
  remain unchanged, not reinterpreted under star.

The remaining DET choice is now precise: independently justify full event-pair
multiplication, justify a different stronger separating/control premise with
its own consequence, or accept that the listed scalar axioms do not select
the desired composition. A premise can be explicitly proposed without being
proved or globally adopted. This note selects none of those choices.

## 8. Supplementary evidence, review and stop boundary

A temporary standard-library Gaussian-Fraction calculation passed **66
focused exact checks**, including 28 Boolean event weights and 16 scalar
rectangle identities. It also checked the full 8×8 associativity identity
for three complex factors, swap/unit, real parts, both complex marginals,
real-map naturality, partition/overlap/zero-mass examples, complex bilinearity,
the omitted pair term, both RI-21 parity weights, the unitary witness (16),
seed weight four and a negative quadratic form for Q star Q. These corroborate
the written proofs, not the reverse. No source file or DET executor was used;
this is not a registered suite, pinned execution or predecessor replay.

Three independent complete reviews passed with no blocker or mathematical
correction: proof and examples; composition-literature/exclusion reasoning;
and repository/source premises. They confirmed the complex-bilinear extension,
nonexclusive mass-preserving real-map condition, bounded-effect collapse,
normalized unitary witness and limits of the comparison to accepted QR work.
All 69 accepted predecessor/design/synthesis identities matched on entry and
at final check. All 139 local links across the four scoped documents resolve;
whitespace/conflict-marker checks have zero findings. Exact four-file hashes
accompany the [source-quiet handoff](QR_HANDOFF.md). Coordinator conditional-proof acceptance is complete. Only reversible
administrative acceptance/current-status wording differs from the reviewed
submission; its mathematical body is unchanged. Only this new note and the
three existing QR summaries are edited. No accepted source,
PairKernel.compose, dependency, registry, protected review, RET/core/
application/bank or other isolated research directory is changed.

The separate coordinator [RI-23 scalar-value/error contract](SCALAR_VALUE_ERROR_CONTRACT.md)
is independently accepted and published in verified `0410ccd`. Its acquisition
and execution interface remains unimplemented; it supplies no implementation assignment. No physical independent-preparation
law, new instrument, full QM, complex-field selection, native F/L, physical
time/rest mass, geometry or gravity result follows. Option B, Status M and
the primitive-input test remain unchanged. No QR-05BW–DO/coverage/noncollapse
sequel, clocks, book, retired kappa-gravity, executor or automatic successor
is opened. This assignment is conditionally accepted and source-quiet for
coordinator publication; every git/index operation stays with that owner.
