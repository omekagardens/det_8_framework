# RI-99 — next-layer record-blind harmonic extension

25 September 2026. Proof/design only; no new native execution or numerical
search. The accepted RI-95 positive-amplitude obstruction is retained.

**Result of this bounded investigation.** The specified two-record subsystem
has eight child-class variables, rank two and a strictly positive
six-dimensional feasible slice. Explicit formulas below characterize it
exactly. Its complete one-step maximal-deletion closure has seven parent
classes and thirty deletion roles. This is not a positive layer-wide
extension: shared-child normalization is still open. A proposal changing
only these eight children and resetting all other h8 values to one is
rejected. Full birth/deletion closure reaches the whole seven-parent layer,
as an analytic statement, not an enumerated table.

## 1. Fixed premises and the question that changed

Use the accepted strictly positive baseline B, the actual held prefix
through parent size five, including the actual mixed q5, and the strict
seven-birth perturbation from
[RI-85](../native_growth_four_vertex_cap_v1/DESIGN.md) and
[RI-88](../native_growth_four_vertex_cap_check_v1/RESULT_REVIEW.md).
Let Z(P)=z_j on the eleven supported seven-order classes T_j and zero
elsewhere. The direction is fixed, with z1=1, every z_j nonzero and
|z_j|<=1. Write

\[
 h_n=1\quad(n\leq6),\qquad
 h^\epsilon_7(P)=1+\epsilon Z(P),\qquad
 m_j=1+\epsilon z_j,\qquad 0<\epsilon\leq\tfrac14.
 \tag{1}
\]

In particular m1=1+epsilon and every h7 is positive. This is the
[RI-94 amplitude family](../native_growth_relative_amplitude_v1/AMPLITUDE.md),
not a new null vector or modified prefix. Baseline B, including its
unknown global half-scales rho=a6 and s=a7, is fixed independently of
epsilon. Neither scale or global maximum is assigned a numerical value.

The model restrictions remain: complete ideal eligibility, strict positive
probabilities, immutable fair independent newborn bits, strict
precursor-record locality, marked-parent equivariance, and whole
unnormalized scalar-passive maps q(P,r,S)D/2. Probabilities do not read D.
The whole unmarked parent may be inspected; old marks outside a proper
precursor may not. These are conditional mathematical premises, not newly
derived DET axioms or informative quantum dynamics.

RI-95 has now been independently accepted after reconstruction of all
seventeen certificate sections and completed execution-custody review.
Its fixed positive-amplitude obstruction excludes the relative
record-blind **common-level-scale** continuation of this seed on the
accepted domain. It is not merely a prospective sufficient test now.

The actual root decision is
/Volumes/AI_DATA/development/det-review-evidence/ri98-qualification-root-ftbqnblc/RI95_ROOT_FINAL_MATHEMATICAL_ADJUDICATION.json,
3937 bytes, SHA256
1d3efa2f0555646749c8805b555fbcfaca27368cd7b053f8b4a2aa547d6876bc.
Its independent arithmetic report is 680187 bytes, SHA256
2a6086d81d31ab8765d0a0aa521de1b63b81d6eeb5ddf3be0b18e5b822de958f.
This note takes that adjudication as a premise; it does not rerun or
reinterpret the obstruction.

The present question drops only the rejected *ansatz*, as assigned:
is there a positive unmarked next-layer weight x_T=h8(T) with the fixed
h7 and baseline B? No child-dependent choice is presumed to work.
Strict positivity, the full record cubes, held prefix and covariance
obligations are not weakened. No h8 is reset outside a selected list.

## 2. Exact variables, equations and structural constraints

For every unmarked eight-order isomorphism class T use one finite real
unknown x_T>0. The **same** value must be used at every occurrence:
different natural labels, inherited markings, newborn bits, individual
ideals and maximal-deletion parents do not create new copies of x_T.

For each size-seven parent P, every full marking r in {0,1}^P and every
individual ideal S, the only candidate transition in this relative
record-blind class is

\[
 q_Q(P,r,S)=q_B(P,r,S)\frac{x_{[P+S]}}{h^\epsilon_7(P)}.
 \tag{2}
\]

Here P+S is the mathematical prospective child obtained by appending one
maximal vertex with past S. Its unmarked class can be computed from P,S;
this is not a read of future records or a preallocated geometry.

Define

\[
 a_{P,r,T}=\sum_{\substack{S\ {\rm ideal\ of}\ P\\[P+S]=T}}q_B(P,r,S).
 \tag{3}
\]

Every labeled ideal is counted once, including repeated occurrences of
one child class. No automorphism division is allowed. The complete
next-layer requirements are exactly

\[
 \sum_T a_{P,r,T}x_T=h^\epsilon_7(P)\quad\text{for every }P,r,
 \qquad x_T>0\quad\text{for every }T.
 \tag{4}
\]

Equivalently, choose one reference marking r0 per parent and retain its
normalization together with **all** record differences:

\[
 a_{P,r_0}\cdot x=h^\epsilon_7(P),\qquad
 (a_{P,r}-a_{P,r_0})\cdot x=0\quad\text{for every }r.
 \tag{5}
\]

These are finite-layer quantifiers, not authorization to construct a
global poset/probability table.

### Why these are the actual locality and covariance constraints

The [RI-81 harmonic construction and converse, sections 7–10](../native_growth_local_mixture_criterion_v1/MIXTURES.md)
apply with the already fixed prefix. Necessity of (2) follows by dividing
the two positive last-birth central-weight identities, using
W_Q(P,r)/W_B(P,r)=h7(P) and the desired record-independent child ratio.
Normalization then gives (4).

Conversely, (4) makes (2) normalized and strictly positive. For a fixed
P,S its multiplier reads no marks, so the baseline's strict record
locality survives directly. Unmarked isomorphism invariance supplies
marked equivariance. On a new diamond based at a six-parent C, both
paths acquire x_H/h6(C)=x_H. The intermediate h7 factors cancel.
Thus both complete unnormalized maps are the same baseline map times
x_H, with all inherited records and both fair newborn bits retained.
Equal precursors still represent two distinct incomparable births.

No additional cross-child equality follows merely from a diamond:
both paths end in the same unmarked H. The necessary identifications
are the shared x_H across its occurrences, not equality of unrelated
child values. Full births yield unique-maximal children and their
single x_[P+top] must be shared over every record of P. A full ideal
may read all old marks, but that permission does not waive this
record-blind relative-weight condition.

Consequently (4), with the complete shared-variable domain, is necessary
and sufficient for an extension **through eight births** in this class.
It is neither an all-size law nor a claim that (4) is feasible.

### Relation to the RI-38 proper-node components

For a proper birth with terminal H, put

\[
 \mathcal T(H)=\prod_{v\in\operatorname{Max}(H)}
                    h^\epsilon_7(H\setminus\{v\}).
 \tag{6}
\]

All maximal deletions are counted, even when their parents are isomorphic.
The accepted [RI-89 proper-product identity, section 2](../native_growth_relative_continuation_v1/CONTINUATION.md)
gives u_h/u_B=J(P,S) and h7(P)J(P,S)=T(H). Therefore (2) is

\[
 q_Q(P,r,S)=\alpha(H)u_h(P,r,S),\qquad
 \alpha(H)=\frac{s\,x_H}{\mathcal T(H)}>0.
 \tag{7}
\]

RI-38's nodes retain the whole unmarked parent, proper ideal and only its
internal marks. An edge retains the same terminal H. Hence (7) respects
the ratio equations. If several marked/local components have the same
unmarked H, record-blindness ties their amplitudes to the **same**
s*x_H/T(H). Arbitrary independent per-occurrence or per-component scales
would not establish (2).

The rejected common-level ansatz instead fixes alpha(H)=t for every
proper terminal, forcing x_H=(t/s)T(H). RI-95's accepted necessary t=s
and nonzero full-complement contrast rule out that restriction for the
fixed family. Equations (4)–(7) do not reintroduce it, and do not claim
that its removal supplies a solution.

## 3. Complete child inventory of the fixed witness

Keep

\[
 P_\star=C_3\oplus A_4=(0,1,3,7,7,7,7),\qquad r=0,1,
 \tag{8}
\]

with only vertex zero changed and all four cap marks zero. C_k is a
chain, A_k an antichain, ordinal sum is written \oplus and disjoint union
\sqcup. C0 and A0 mean the empty order.

There are nineteen individual ideals. The stem-only masks are 0,1,3,7.
An ideal containing any cap contains all of C3 and an arbitrary subset
of the four incomparable caps. Define the eight child types

\[
 X_\ell=C_\ell\oplus[(C_{3-\ell}\oplus A_4)\sqcup A_1],
       \quad \ell=0,1,2,
\]
\[
 Y_k=C_3\oplus[(A_k\oplus A_1)\sqcup A_{4-k}],
       \quad k=0,1,2,3,4.
 \tag{9}
\]

The X_l birth has the first l stem vertices as its past; Y_k has the
whole stem and exactly k caps as its past. Permutations of the four old
caps prove equality within each cap-subset class, without removing the
individual ideals from a row sum.

These eight types are distinct. X0,X1,X2,Y0 have five maxima and a
universal initial chain of lengths zero, one, two and three respectively.
Y1,Y2,Y3,Y4 have respectively four, three, two and one maxima. This also
distinguishes the full-birth type Y4.

Use unknowns in the fixed order

\[
 x=(x_{X_0},x_{X_1},x_{X_2},x_{Y_0},
                  x_{Y_1},x_{Y_2},x_{Y_3},x_{Y_4}).
 \tag{10}
\]

Their individual-ideal multiplicities are (1,1,1,1,4,6,4,1), summing to
nineteen. This is a hand-derived local inventory, not a global catalogue.

## 4. Exact two-row coefficients and positive domain

All coefficients below are symbolic expressions in the unchanged six held
C3/C4/H5 rows of RI-89 section 6, where H5=C3 ordinal-sum A2. For the
four stem ideals S=0,1,3,7 let A_r(S), B_r(S), G_r(S) be the corresponding
held probabilities. Set

\[
 c_r=q_{C_4,r}(15),\quad
 h_r=q_{H_5,r}(15)=q_{H_5,r}(23),\quad
 j_r=q_{H_5,r}(31),
\]
\[
 L_r(S)=\frac{A_r(S)^3G_r(S)^6}{B_r(S)^8},\quad
 p_r=L_r(7),\quad v_r=\frac{h_r^3}{c_r^2},
\]
\[
 E_r=\sum_{S=0,1,3,7}\frac{A_r(S)G_r(S)^3}{B_r(S)^3}
                  +3h_r^2/c_r+3j_r,\qquad
 K_r=\sum_{S=0,1,3,7}L_r(S),
\]
\[
 U_r=4-4\rho E_r+6\rho^2j_r+4\rho^3v_r+\rho^4K_r.
 \tag{11}
\]

The lower-case h_r is a held probability, not h7 or h8. Positive
denominators and the full-record unique-top/twin-top transport lemmas
are inherited from RI-85 sections 4–5; no additional record erasure is
assumed. No values or new native polynomial coefficients are evaluated.

The baseline aggregate row weights, in order (10), are

\[
 w_r=\big(s\rho^4L_r(0),\,s\rho^4L_r(1),\,s\rho^4L_r(3),
 s\rho^4p_r,\,4s\rho^3v_r,\,6s\rho^2j_r,\,
 4s(1-\rho E_r),\,1-sU_r\big).
 \tag{12}
\]

They count all nineteen ideals, including the full complement. Their
sum is one by (11). These are the baseline weights, not the already
rejected modified common-scale weights.

The inherited rigorous outer domain is

\[
 0<\rho\leq R=\frac1{2(1+\max(E_0,E_1))},\qquad
 0<s\leq\min_{i=0,1}\frac1{2(1+U_i(\rho))}.
 \tag{13}
\]

It contains the actual unknown baseline half-scales, not a selection of
them. On this domain rho*E_r<1/2, so every entry of (12) is positive and
1-sU_r>1/2. The candidate Q is required to be strictly positive and
normalized; no unassigned global half-scale selector is silently imposed
on Q. Full-cube and covariance gates in section 2 remain unchanged.

## 5. Exact local feasibility: six degrees, not a new extension law

For this one parent h7(P*)=m1=1+epsilon. The two selected harmonic rows
are precisely

\[
 w_0\cdot x=m_1,\qquad w_1\cdot x=m_1,\qquad x>0.
 \tag{14}
\]

They always have the positive solution x=m1*1, since each w_r sums to
one. Thus **this isolated subsystem cannot obstruct a general positive
record-blind h8**. The statement holds for every parameter in (1),(13),
without evaluating a native coefficient.

The two equations are independent. RI-94 section 5 proves from the
accepted RI-91 anchor that

\[
 (j_1-j_0)z_3>0,
 \tag{15}
\]

so j1 differs from j0. The Y2 coefficient difference is
d=6*s*rho^2*(j1-j0), which is nonzero. Strict precursor-record locality
also gives w_(0,X0)=w_(1,X0)=e>0, because X0 is the empty-precursor birth.
The minor using columns X0 and Y2 is exactly e*d, hence nonzero. This
is a structural rank-two proof, not a numerical rank computation.

For an explicit complete parameterization, put Delta_i=w_(1,i)-w_(0,i)
and choose the six free coordinates indexed by

\[
 J=\{X_1,X_2,Y_0,Y_1,Y_3,Y_4\}.
\]

Then the remaining values are forced:

\[
 x_{Y_2}=-\frac{\sum_{i\in J}\Delta_i x_i}{d},\qquad
 x_{X_0}=\frac{m_1-w_{0,Y_2}x_{Y_2}
                         -\sum_{i\in J}w_{0,i}x_i}{e}.
 \tag{16}
\]

Necessary and sufficient local inequalities are: every free x_i>0,
the first expression in (16) is positive, and the numerator of the
second is positive. No sign of d is guessed and no inequality is
multiplied by d without its sign. Equations (16) themselves suffice.

Equivalently the feasible set is

\[
 \{m_1\mathbf1+v:\ w_0\cdot v=w_1\cdot v=0,\
                         m_1+v_i>0\text{ for all }i\}.
 \tag{17}
\]

It is a nonempty relatively open bounded convex slice of affine
dimension six. Positivity holds in a neighborhood of v=0; boundedness
follows from 0<x_i<m1/w_(0,i), since every other positive row summand
is present. No uniform neighborhood size over the excluded rho or s
boundaries is claimed.

Indeed the constant assignment solves *every record row of P* in
isolation, by baseline normalization. This does not establish rank or
degrees of freedom for that larger block. The selected pair does not
replace the other stem markings: RI-89 proves cap-mark invariance,
not permission to erase all remaining stem bits.

As a consistency check on scope, the local constant assignment gives
alpha(X0)=s but alpha(Y0)=s/m1^4 by (6)–(7). For positive epsilon these
differ. The local solution is outside the rejected common-level
restriction; this observation does not show that it extends globally.

## 6. Shared-child closure: all thirty first deletion roles

A child value cannot be chosen only for the route from P*. For each
child in (9), delete **each maximal vertex** to find every other parent
whose transitions must use that same value.

Define three seven-parent types and one unique-top type:

\[
 Q_\ell=C_\ell\oplus[(C_{3-\ell}\oplus A_3)\sqcup A_1],
       \quad \ell=0,1,2,\qquad
 U=C_3\oplus A_3\oplus A_1.
 \tag{18}
\]

Each Q_l has an initial universal chain of length l<3; it is outside the
eleven-class support. U has a unique maximum and is also outside it.
Thus h7(Q_l)=h7(U)=1. The other two parents below are exactly the
accepted support types T2=C3⊕(C2 disjoint A2) and
T3=C3⊕((A2 ordinal-sum A1) disjoint A1).

| Child | Every maximal-deletion parent, with multiplicity | Product T(H) for a proper terminal |
| --- | --- | --- |
| X0 | P* once; Q0 four times | m1 |
| X1 | P* once; Q1 four times | m1 |
| X2 | P* once; Q2 four times | m1 |
| Y0 | P* five times | m1^5 |
| Y1 | P* once; T2 three times | m1*m2^3 |
| Y2 | P* once; T3 twice | m1*m3^2 |
| Y3 | P* once; U once | m1 |
| Y4 | P* once, unique maximum | Not a proper-terminal constraint |

For X_l the newborn is incomparable with all four old caps; deleting it
returns P*, while deleting an old cap gives Q_l. For Y_k the maxima are
the newborn plus the 4-k unselected caps. Deleting the newborn returns
P*; deleting an unselected cap gives the displayed parent. At k=0 all
five deletions are isomorphic P*. At k=4 there is no other maximum.
These arguments exhaust maxima, not just representative birth roles.

The complete first deletion closure therefore has seven parent classes
and thirty individual roles: P* occurs twelve times, each Q_l four,
T2 three, T3 two and U once. Backward deletion multiplicities are not
normalization coefficients. Each new parent's forward row must still sum
its own individual ideals by (3), rather than substituting these counts.

In particular each Q_l,T2,T3,U contributes its **whole** marked-parent
block (4), with RHS respectively 1,m2,m3,1. All existing child values
are shared; additional children introduce additional unknown class
values, never independent copies of an existing x. No probabilities for
these extra rows are reconstructed in this note, and they have not been
solved. The positive center in section 5 does not settle their record
differences or their remaining proper/full complements.

### A rejected shortcut: no reset outside these eight children

Suppose one proposed arbitrary x on the eight listed children but h8=1
on every other eight-order. None of T4,...,T11 is a maximal-deletion
parent of a listed child, by the exhaustive table. Therefore every
child of each such T_j would have h8=1. Its harmonic row would read
1=h7(T_j)=1+epsilon*z_j, impossible because epsilon>0 and every accepted
z_j is nonzero.

Thus correction support confined to these eight children is rejected,
regardless of how their six local free coordinates are chosen.
This is a support-coverage necessity, not a no-go for all h8 or a
permission to enumerate a larger native domain. Exterior values remain
unknown. More generally every parent with nonzero Z(P) must have at
least one child with nonzero h8(child)-1.

## 7. Why complete incidence closure is not a small sealed block

Form the undirected graph of unmarked seven-parent classes: two are
adjacent when they are maximal-deletion parents of one eight-order.
This graph is connected.

To prove it, take any non-antichain seven-parent P. A comparable pair
has an upper element that can be extended upward to a maximal v with
nonempty strict past. The order H=P disjoint {y}, with new isolated y,
has both v and y maximal. Its two deletion parents are P and
P'=(P without v) disjoint {y}. P' has exactly |past_P(v)| fewer strict
order relations. Repeating this step reaches A7 in finitely many steps.
All steps are legitimate common-child incidences because the past of a
restored maximal vertex is an ideal. Adjacency is symmetric. Therefore
every class is connected to A7.

It follows that any nonempty parent family closed under **all** eligible
birth children and **all** their maximal-deletion parents is the full
seven-parent layer. The seven-parent first closure in section 6 is not
such a closed family. No global table has been constructed to establish
this fact.

This does not mean that a future proof must enumerate every class.
Structural lemmas might discharge many equations at once. It means that
a claim of layer-wide sufficiency must discharge the complete
shared-variable system, not stop because the first eight children or
seven parents have been listed.

## 8. Exact remaining feasibility problem

Let A denote the full finite incidence-weight matrix in (3), with all
complete marked seven-parent rows and all unmarked eight-child columns.
Every row sums to one. In vector notation write Z for the fixed
seven-parent value, repeated across that parent's record rows. Then

\[
 A x=\mathbf1+\epsilon Z,\quad x>0.
 \tag{19}
\]

Since epsilon>0 and B is independent of epsilon, the substitution
x=1+epsilon*y gives the exact equivalent problem

\[
 A y=Z,\qquad y_T>-1/\epsilon\quad\text{for every child class }T.
 \tag{20}
\]

No rationality or existence of y is assumed. The unknown actual baseline
scales remain fixed premises, not adjustable solver parameters.
A signed solution of the equalities is not sufficient at the requested
amplitude; the strict inequalities and all shared occurrences remain.
Conversely this full system, if proved, would suffice for this layer by
section 2. Neither signed feasibility nor its failure is established here.

The unresolved obligations are now precise:

1. Account for every shared child across its maximal-deletion parents
   and all record/local-component fibers, preserving ideal multiplicities.
2. Discharge reference normalization and every remaining record difference
   with the fixed baseline coefficients, including the unique-maximal
   full-birth values; do not average records or infer full-cube success
   from the two selected markings.
3. Prove a single finite positive assignment satisfying the coupled
   system, or produce an exact contradiction valid for that system.
   The local positive center is not that assignment.
4. Keep finite-layer sufficiency separate from compatible positive
   extensions at all later sizes, sustained width or any geometry.

These are proof conditions, not a new checker, admitted global catalogue,
coefficient calculation, numerical search or successor execution plan.
RI-38 guarantees some conditional continuation of the seed, but not that
its relative central weights are record-blind. RI-95 continues to reject
the common-level-scale relative family exactly as adjudicated.

## 9. Provenance, result boundary and handoff

The cited load-bearing proof sources are RI-38 sections 1–5; RI-81
sections 7–10; RI-85 sections 2–5 and 8; RI-88's accepted result;
RI-89 sections 1–4 and 6; RI-94 sections 1–5; and the actual RI-95
root adjudication. Complete source files were read for this preparation.
Their exact identities, together with opaque accepted RI-88 and RI-95
audit evidence, are retained in the external PREMISES.json.

New results are the explicit rank-two positive local parameterization,
the eight-child/seven-parent/thirty-role consistency closure, the
rejected eight-child-only correction support, and the incidence
connectivity warning. These are manual finite proofs and exact symbolic
algebra, not proof-assistant formalization or executable verification.

No supplied checker, helper, target or native row reconstruction was
imported, compiled or run. No scientific certificate body was decoded
for new arithmetic; no global poset table, source admission, numerical
search or new scientific domain was created. All earlier sources,
custody and failed history remain unchanged.

No complete h8 has been constructed. No all-size record-blind law,
informative quantum coupling, measurement forward map, Lorentzian
geometry, mass, gravity, empirical discriminator or unique DET selection
follows. Option B, metric-as-record Status M and RET's pause are unchanged.

The sole proposed repository research artifact is this EXTENSION.md,
for docs/track_b/native_growth_harmonic_extension_v1/. The external
packet is for independent review; coordinator acceptance, repository
edits, git/index/publication and any further scoped assignment remain
root-owned. This bounded worker handoff does not pause or end the wider
programme.
