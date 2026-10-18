# RI-101 — a global signed one-layer lift by empty birth

25 September 2026. External proof-only proposal for coordinator adjudication.
No native coefficients, global tables, checker, solver or numerical scales
have been evaluated or selected.

**Result.** The actual accepted RI-88 direction has an explicit solution of
the complete RI-99 signed system Ay=Z. It is supported on eleven
eight-event classes, each obtained by adjoining one isolated event to a
supported seven-event class. All incoming marked rows are discharged by
a sixteen-parent closure and the baseline empty/ordinary-birth diamond.
Consequently a strictly positive relative record-blind extension through
eight births exists for sufficiently small positive amplitude. This does
**not** certify the previously used amplitude epsilon=1/4.

## 1. Fixed object and complete signed equations

Keep the accepted baseline B and the fixed RI-88 direction, not a new
null vector, prefix or fitted growth law. Write

\[
 T_j=C_3\oplus Q_j\quad(1\leq j\leq11),\qquad
 Z(P)=
 \begin{cases}z_j,&[P]=T_j,\\0,&\text{otherwise},\end{cases}
 \tag{1}
\]

where the eleven four-event caps Q_j are exactly those in
[RI-85 sections 2–3](../native_growth_four_vertex_cap_v1/DESIGN.md).
They have at least two maxima. All z_j are nonzero, z1=1 and |z_j|<=1,
as accepted in [RI-88](../native_growth_four_vertex_cap_check_v1/RESULT_REVIEW.md).
The direction is harmonic at every complete six-parent record row:

\[
 \sum_{S\ {\rm individual\ ideal\ of}\ C}
       q_B(C,r,S)Z(C+S)=0
 \quad\text{for every }|C|=6,\ r\in\{0,1\}^{C}.
 \tag{2}
\]

For the five affected six-parent classes this is the accepted complete
harmonic system; for every other C it follows from RI-85's exhaustive
maximal-deletion closure. All unsupported slots, including full births,
remain in (2) with zero correction, not zero baseline probability.

Retain h_n=1 for n<=6 and h7(P)=1+epsilon*Z(P), with
0<epsilon<=1/4. Baseline B, including its actual unknown half-scales
rho=a6 and s=a7, is fixed independently of epsilon. Amplitude variation
is the already defined RI-94 family, not authorization to change the
original epsilon=1/4 prefix in an implementation.

The inherited conditional model has strictly positive probabilities for
every ideal, immutable independent fair newborn bits, complete record
cubes, marked-parent equivariance, strict precursor-record locality,
and full scalar-passive maps q_B(P,r,S)D/2. Whole unmarked parent order
is permitted input. These are premises, not new derivations from DET.
The payload is retained but not made informative by this construction.

For every unmarked eight-event class H use one shared variable y_H.
Define the complete finite matrix

\[
 A_{P,r,H}=\sum_{\substack{S\ {\rm individual\ ideal\ of}\ P\\
                           [P+S]=H}}q_B(P,r,S),\qquad |P|=7.
 \tag{3}
\]

All parent markings and all individual ideals are retained; same-child
slots are summed, never orbit-divided. A child variable is shared across
every parent, marking and relabeling. Every row of A sums to one.
[RI-99](../native_growth_harmonic_extension_v1/EXTENSION.md) proves that

\[
 Ay=Z,\qquad 1+\epsilon y_H>0\text{ for every }H
 \tag{4}
\]

is exactly the one-layer positive extension problem, by setting
h8(H)=1+epsilon*y_H. Here the RHS repeats Z(P) for every marking of P.
Finiteness is a mathematical fact about a fixed finite layer; no global
order or probability table is being constructed.

## 2. Signed solvability and sufficiently small amplitude

**Finite-layer equivalence.** With A, B and Z fixed as above, a finite
real solution of Ay=Z exists if and only if there exists some
0<epsilon<=1/4 with a positive solution of
Ax=1+epsilon*Z. Indeed, more strongly, signed solvability gives positive
solutions for every sufficiently small positive epsilon.

For the forward implication, let y solve Ay=Z. Define

\[
 \eta_y=\min_{H:y_H<0}\frac{-1}{y_H},
 \tag{5}
\]

with the minimum of the empty set interpreted as +infinity. There are
finitely many finite coordinates, so eta_y>0. For
0<epsilon<=1/4 and epsilon<eta_y, x=1+epsilon*y is strictly positive,
and Ax=1+epsilon*Z because A1=1. Conversely, for any positive solution
x at any epsilon>0, y=(x-1)/epsilon solves Ay=Z.

This is not the assertion that every signed solution is positive at
epsilon=1/4. At that prescribed amplitude the additional exact
inequalities are y_H>-4, for every H. Neither a weak inequality nor
positivity on selected children suffices. A positive extension at
epsilon0 also interpolates to smaller positive amplitudes by
x(epsilon)=1+(epsilon/epsilon0)(x(epsilon0)-1), but changing a prescribed
amplitude remains a distinct decision.

## 3. Eliminate private full-birth variables without losing positivity

Let F(P)=P plus a new vertex above all of P. This child has a unique
maximum, and deleting it uniquely determines P. Conversely, every
eight-event child with a unique maximum arises this way. A proper ideal
omits an old maximum, which remains incomparable with the newborn, so
a proper birth cannot yield a unique-maximal child.

Thus full-child columns are private to one unmarked parent class,
whereas every multiple-maximal child keeps its single global variable.
For one parent P, write a'_r for its row restricted to all
multiple-maximal child columns and b_r=q_B(P,r,P)>0. Each marked row is

\[
 a'_r y_{\rm proper}+b_r y_{F(P)}=Z(P).
 \tag{6}
\]

Choose one reference marking r0, write b0=b_(r0), and eliminate the one
full variable. The exact reduced system is

\[
 (b_0a'_r-b_ra'_0)y_{\rm proper}=(b_0-b_r)Z(P)
       \quad\text{for every }r\ne r_0,
 \tag{7}
\]
\[
 y_{F(P)}=\frac{Z(P)-a'_0y_{\rm proper}}{b_0}.
 \tag{8}
\]

To prove equivalence, multiply the r row by b0, subtract b_r times the
reference row, and obtain (7). Conversely (8) solves the reference row;
substituting it into any other row and using (7) proves that row.
Apply this independently to each P, without splitting any shared proper
column or averaging any records.

At a prescribed epsilon, reduced signed solvability must still retain

\[
 1+\epsilon y_H>0\quad(H\text{ multiple-maximal}),\qquad
 b_0+\epsilon\bigl(Z(P)-a'_0y_{\rm proper}\bigr)>0
       \quad\text{for every }P.
 \tag{9}
\]

The second inequality is the recovered full-child positivity condition,
using b0>0. Elimination does not remove it.

## 4. Native construction and exhaustive incoming closure

For any nonempty parent P set

\[
 E(P)=P\sqcup A_1,\qquad e_P=q_B(P,r,\varnothing)>0.
 \tag{10}
\]

Strict precursor-record locality makes e_P independent of every old
mark: the empty precursor has no record to read. Equivariance makes it
an unmarked-class quantity. This is an actual fixed baseline probability,
not a new free coefficient or selected scale.

Every T_j is connected and has no isolated vertex: all its cap vertices
lie above the common three-chain. Therefore

\[
 J_j=E(T_j)=T_j\sqcup A_1
 \tag{11}
\]

has exactly one isolated vertex. Removing it uniquely recovers T_j, so
the eleven J_j are distinct unmarked classes. Define on the entire
eight-event layer

\[
 \boxed{\displaystyle
 y_H=
 \begin{cases}
 z_j/e_{T_j},&[H]=J_j,\quad 1\leq j\leq11,\\
 0,&\text{otherwise}.
 \end{cases}}
 \tag{12}
\]

There are eleven nonzero coordinates, all finite. Setting other
coordinates to zero here is part of a fully verified support
construction, not an unproved reset after solving selected rows.

Let C_i (i=1,...,5) denote the five six-event parents called P_i in
RI-85: C3 ordinal-sum, respectively, A3, C2 disjoint A1,
A2 ordinal-sum A1, A1 ordinal-sum A2, and C3. Put

\[
 D_i=E(C_i)=C_i\sqcup A_1.
 \tag{13}
\]

Each C_i is connected and isolate-free. Deleting the isolated maximum
of J_j yields T_j. Deleting any other maximum yields
E(T_j without that maximum), hence one of the D_i. The inherited
cap-deletion table gives the complete inventory:

| Child | Isolated-vertex deletion | All other maximal deletions |
| --- | --- | --- |
| J1 | T1 once | D1 four times |
| J2 | T2 once | D2 twice; D1 once |
| J3 | T3 once | D3 once; D1 once |
| J4 | T4 once | D4 once; D2 twice |
| J5 | T5 once | D2 twice |
| J6 | T6 once | D3 once; D2 once |
| J7 | T7 once | D5 once; D2 once |
| J8 | T8 once | D3 twice |
| J9 | T9 once | D4 three times |
| J10 | T10 once | D5 once; D4 once |
| J11 | T11 once | D5 twice |

These are 38 individual deletion roles, comprising 11 isolated deletions
and the inherited 27 cap deletions. There are exactly sixteen parent
classes: eleven connected T_j and five disconnected D_i. Connectedness
separates the two groups; removing the unique isolated vertex
distinguishes the five D_i.

This is exhaustive globally, not just within a cap catalogue: any parent
of a J_j birth is obtained by deleting its newborn, and that vertex is
maximal. The table lists every such deletion. Relabeling cannot create
an additional parent type.

Forward row counts are different. At T_j only its empty birth can
produce any J_k: an existing connected parent cannot acquire an isolated
old vertex, so the isolated vertex of the terminal must be the newborn.
This gives eleven individual supported birth slots across these parents.

At D_i=C_i plus an isolated old vertex w, any birth producing a J_j
must leave w isolated. Otherwise the old C_i has no isolated vertices
and neither would the terminal. Thus its precursor is an ideal S of
C_i excluding w, and C_i+S must be T_j. Conversely each such S works.
Exactly RI-85's 23 individual supported slots are inherited, with
counts 7,5,4,4,3 for the five D_i. There are 34 forward supported
slots across the sixteen parent representatives, not 38. All other
forward slots keep y=0; none has its baseline probability removed.

## 5. Complete marked-row proof of Ay=Z

### Connected supported parents

For any complete marking r of T_j, only S=empty has a nonzero child
correction. Therefore

\[
 \sum_S q_B(T_j,r,S)y_{[T_j+S]}
   =e_{T_j}\frac{z_j}{e_{T_j}}=z_j=Z(T_j).
 \tag{14}
\]

This holds for all 128 markings independently, not just all-zero marks.
It also shows that within the eleven-child support (12) the values are
forced; it makes no global support-minimality claim.

### Disconnected leakage parents

Fix any C=C_i, every marking r of C and both newborn bits beta,gamma.
Consider two incomparable births: x with past S, and w with empty past.
The two full baseline maps, with named coordinates transported to the
same marked terminal, are

\[
 \frac14q_B(C,r,S)
       q_B(C+x_S,r\mathbin{\|}\beta,\varnothing)\,D
 =
 \frac14q_B(C,r,\varnothing)
       q_B(C+w_\varnothing,r\mathbin{\|}\gamma,S)\,D.
 \tag{15}
\]

This is the inherited RI-38 whole-map diamond. It is not merely equality
of traces or normalized outcomes. Comparing the scalar coefficients of
these maps gives

\[
 q_B(C,r,S)e_{C+S}
   = e_C q_B(E(C),r\mathbin{\|}\gamma,S).
 \tag{16}
\]

Both empty probabilities ignore all marks, including beta in the left
intermediate state. The two factors of 1/2 are retained equally in (15);
none is lost in (16). Proper precursor locality on the right excludes
gamma from the probability's record input. The full diamond itself
holds separately for every r,beta,gamma, so this is not a record average.

Sum over every individual ideal S of C. Unsupported terms have
Z(C+S)=0. On each supported term, the terminal is E(C+S)=J_j,
and (12),(16) give

\[
\begin{aligned}
 \sum_{S\ {\rm ideal\ of}\ C}
 q_B(E(C),r\mathbin{\|}\gamma,S)y_{[E(C)+S]}
 &=\sum_{S\ {\rm ideal\ of}\ C}
       \frac{q_B(C,r,S)}{e_C}\,Z(C+S)\\
 &=0
 =Z(E(C)).
\end{aligned}
 \tag{17}
\]

Here the first equality includes zero terms: for S=empty the terminal
has two isolated vertices and is not in (12); for every other unsupported
S, C+S is not a T_j and neither is its isolated extension a J_j.
Ideals of E(C) that contain w cannot produce a J_j and also contribute
zero, as proved in section 4. Thus (17) is the **complete** row equation
of E(C), not conditioning on its supported or proper births.
The last equality is exactly the accepted harmonic identity (2).

Every marking of D_i decomposes uniquely into a marking of C_i and
the bit gamma on its isolated vertex, after a marked isomorphism.
Consequently all 128 records of each D_i are covered. Marked
equivariance transports the proof to all labeled copies. Repeated
same-child ideals remain separate summands throughout (17);
backward-deletion counts are never substituted as forward weights.

### All remaining parents

No parent outside the sixteen classes has any child J_j, by the
complete maximal-deletion table. Its whole row in Ay is therefore zero.
Its Z(P) is also zero since it is not a T_j. This discharges every
remaining marked row simultaneously, without evaluating a global table.

Equations (14),(17) and this exhaustion prove **Ay=Z on the complete
shared-child/full-record domain**.

Every J_j has at least three maxima, so all full-child coordinates in
(12) are zero. Hence a'_r y_proper=Z(P) for every P,r. The reduced
equations (7) hold and the recovery (8) gives y_F(P)=0 identically.
Its full-child multiplier is exactly one and automatically positive.

In particular no exact signed obstruction v with A^T v=0 and v^T Z!=0
can exist for this system: v^T Z=v^T Ay=0. A dual rejecting a narrower
ansatz would not contradict this construction.

## 6. Exact positivity boundary and preservation of the model

For this explicit lift define

\[
 \epsilon_{\rm lift}
    =\min_{j:z_j<0}\frac{e_{T_j}}{-z_j}>0.
 \tag{18}
\]

The negative set is nonempty: the accepted C1 reference equation has
strictly positive coefficients and z1=1, so not all its z coordinates
can be nonnegative. There are only eleven coordinates and every e_Tj
is strictly positive. Thus the minimum in (18) is a finite positive
number, even though it has not been numerically evaluated.

Within 0<epsilon<=1/4, this lift is strictly positive **if and only if**

\[
 \epsilon<\epsilon_{\rm lift}.
 \tag{19}
\]

Positive z_j cause no restriction. Equality at any limiting negative
coordinate gives h8=0 and is inadmissible. For all amplitudes in (19),
h7 is already positive by |z_j|<=1 and the shared-child transform is

\[
 q_Q(P,r,S)=q_B(P,r,S)
 \frac{1+\epsilon y_{[P+S]}}{1+\epsilon Z(P)}.
 \tag{20}
\]

The proved complete harmonic equations make every row normalized.
All factors are positive. The multiplier is unmarked and class-invariant,
so it reads no forbidden record, preserves marked equivariance, and
keeps the immutable fair bits. On every new six-parent diamond, the
h7 intermediate factors cancel; both complete baseline D/4 maps are
multiplied by the same h8 of the terminal. The smaller accepted prefix
is unchanged. These are precisely RI-81/RI-99's finite extension
conditions, not additional tests on a few selected routes.

On T_j the formula is especially transparent:

\[
 q_Q(T_j,r,\varnothing)=
       \frac{e_{T_j}+\epsilon z_j}{1+\epsilon z_j},\qquad
 q_Q(T_j,r,S)=
       \frac{q_B(T_j,r,S)}{1+\epsilon z_j}\quad(S\ne\varnothing).
 \tag{21}
\]

For epsilon=1/4 this particular construction passes exactly when

\[
 e_{T_j}>-z_j/4\qquad\text{for every }j\text{ with }z_j<0.
 \tag{22}
\]

No such inequalities have been evaluated or proved here. Failure of
(22) would reject this particular lift at that amplitude, **not every**
solution of Ax=1+Z/4. Success for sufficiently small amplitude does not
change that quantifier or silently replace the prescribed seed.

All e_Tj are native symbolic quantities in the existing fixed law.
For example RI-38 supplies directly

\[
 e_{T_j}=s
 \prod_{\varnothing\ne B\subseteq\operatorname{Max}(T_j)}
       q_B(T_j\setminus B,\varnothing)^{(-1)^{|B|+1}}.
 \tag{23}
\]

Singleton deletions use the five six-parent shapes C_i; their empty
probabilities are rho times their inherited positive proper potentials.
Further deletions use only C3, C4, C5 or C3 ordinal-sum A2, the already
accepted held closure. Formula (23) is a symbolic identification, not
a new query, coefficient calculation or permission to load a helper.
No scale selection, supplied geometry or new order catalogue is needed
for the signed proof.

The RI-95 obstruction remains intact: it rejected the common-level
relative continuation, not every child-dependent h8. On the RI-99
witness T1, this lift changes only X0=T1 disjoint A1 among its eight
children. In its proper-component formula alpha(H)=s*h8(H)/T(H),
both X0 and X1 have T(H)=1+epsilon, but h8(X0)=1+epsilon/e_T1
and h8(X1)=1. Their alpha values differ for every positive epsilon.
Thus this lift does not reinstate the rejected common-level ansatz.

## 7. Result boundary, provenance and handoff

The completed mathematical obligation is global **one-layer signed
solvability for the actual fixed direction and baseline**, with an
explicit eleven-coordinate construction and a proof covering all
incoming marked rows. It also proves existence of positive finite
extensions for sufficiently small amplitude. The full-birth elimination,
its strict positivity conditions and the exact boundary of this lift
are recorded above.

Remaining distinctions are load-bearing:

- Positivity at the previously fixed epsilon=1/4 is unresolved. No
  amplitude change or implementation has been selected.
- No all-size positive record-blind relative law, uniform-in-depth
  amplitude, persistent width improvement or geometric regime follows.
  The new nonzero support contains isolated vertices; simply repeating
  the isolate-free-support argument is not a proved iteration.
- This is a conditional record/growth theorem with the unchanged passive
  quantum payload, not a full QM derivation, quantum measurement map,
  Lorentzian correspondence, mass or gravity result. Option B,
  metric-as-record Status M and RET's pause are unchanged.

The load-bearing mathematical sources are RI-38, RI-81, RI-85, RI-88
and the accepted RI-99 complete-domain proof. RI-94 fixes the already
authorized amplitude family; the accepted RI-95 adjudication is retained
as the separate common-level restriction. Exact source identities and
review provenance are in the external PREMISES.json and review record.
Historical source-only wording in earlier design packets remains history,
not reversal of later acceptance.

The proof uses manual finite combinatorics and exact symbolic identities.
No native target/helper/checker was imported, compiled or run, no
scientific certificate body was decoded for new arithmetic, and no
global order table, numerical search, new native coefficient evaluation
or proof-assistant formalization was performed.

The sole proposed repository research artifact is this SIGNED.md for
docs/track_b/native_growth_signed_extension_v1/. External metadata
records provenance, not new executors or a new scientific test domain.
Prior accepted sources and failed evidence remain unchanged.
Coordinator mathematical acceptance, repository edits, git/index,
publication and any subsequent scoped assignment remain coordinator-owned.
This finite proof handoff neither authorizes a successor execution nor
pauses the wider programme.
