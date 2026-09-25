# RI-103 — private full-birth compensation and record compatibility

25 September 2026. External analytic proof/design proposal. Actual baseline
B, the original eleven-class direction Z, epsilon=1/4 and every record
configuration are fixed. No coefficient evaluation or native execution.

**Result.** The specified complete incoming repair family has 27 child
variables and sixteen parent classes. Positivity in that family requires
the full-birth probability of T1=C3 ordinal-sum A4 to be exactly constant
over its complete record cube. Otherwise the RI-102 offending row cannot
be repaired, regardless of the other private full-child values. A new
maximal-record invariance lemma proves that changing an old isolated
record cannot test this requirement. Two supported parents also have
genuinely constant full probabilities, so blanket record sensitivity is
false. The remaining T1 condition reduces to a nonzero polynomial of
degree at most three at the actual rational scale. Its root exclusion
has **not** been established;
positive feasibility of this compensation family remains undecided.

## 1. Exact candidate and complete incoming closure

Retain [RI-101](../native_growth_signed_extension_v1/SIGNED.md) and
[RI-102](../native_growth_fixed_amplitude_lift_v1/AMPLITUDE.md).
Let T_j (j=1,...,11) be the accepted seven-parent support, z the fixed
RI-88 vector, J_j=T_j disjoint A1, and

\[
 e_P=q_B(P,r,\varnothing)>0.
 \tag{1}
\]

Empty probabilities are record-blind. Let C_i (i=1,...,5) denote the
six-parent classes called P_i in
[RI-85](../native_growth_four_vertex_cap_v1/DESIGN.md), and put
D_i=C_i disjoint A1. RI-101 proves that the complete incoming parent
closure of the eleven J_j is

\[
 {\cal P}=\{T_1,\ldots,T_{11},D_1,\ldots,D_5\}.
 \tag{2}
\]

For each P in this set, let F(P) be P plus a new vertex above all of P.
Consider exactly the candidate support

\[
 {\cal H}=\{J_1,\ldots,J_{11}\}
            \ \cup\ \{F(P):P\in{\cal P}\}.
 \tag{3}
\]

Allow arbitrary signed corrections y on these classes, requiring
h8=1+y/4>0. Set y=0 on every other eight-event class.
This is a proposed bounded support, not a claim that positive weights
exist there. One unmarked variable is shared over all occurrences,
records and natural labels.

Every F(P) has a unique maximum. Deleting it recovers P, so F is
injective and its column has no other incoming parent. No F(P) is a J_j:
each J_j has at least three maxima. Thus (3) has exactly 27 distinct
candidate columns and still only sixteen incoming parent classes.

The RI-101 inventory had 38 individual maximal-deletion roles and
34 supported forward ideal slots. Each new full child adds one role
of each kind. Hence the candidate has 54 backward roles and 50 forward
slots, before any zero correction is chosen. These numbers are not
interchangeable normalization weights. Every complete parent row still
sums all of its individual ideals, including the unchanged slots.

There are 16*128=2048 raw marked rows on these representatives. No
outside parent can reach a column in (3); outside rows therefore remain
baseline with RHS correction zero. Adding further private full children
of outside parents alone cannot help: their row would give
q_B(P,r,P)*y_F(P)=0, forcing y_F(P)=0 by positivity.

## 2. A maximal-record invariance theorem

**Lemma.** In this strictly positive, normalized scalar-passive family
with strict precursor-record locality, marked equivariance and complete
marked diamonds, every ideal probability q(P,r,S), including the full
complement, is independent of the record on each maximal vertex of P.

The statement concerns actual dependence, not a new read permission.
A full ideal is permitted to read all parent marks, but the other
retained equations impose this additional invariance. Nonmaximal marks
are not erased by the lemma.

**Proof by parent size.** At a singleton, the empty probability reads
no mark and its full complement is one minus it. Suppose the claim
holds for all smaller complete rows. Fix a maximal vertex w of P.

For a proper ideal S excluding w, locality gives the conclusion directly.
If w belongs to S, choose a maximal vertex v outside S; one exists
because a proper ideal cannot contain all maxima. In particular v differs
from w. Set C=P without v and T=past_P(v). The vertex w remains maximal
in C and cannot belong to T, since w and v are distinct maxima.

Compare births v with past T and x with past S from C. Their full
marked diamond gives the coefficient equality

\[
 q_B(C,r_C,T)\,q_B(P,r_P,S)
 =
 q_B(C,r_C,S)\,q_B(C+x_S,r_C\mathbin{\|}b_x,T).
 \tag{4}
\]

The equality comes from whole maps multiplying D/4, with both newborn
bits and named terminal coordinates retained. Both T factors ignore
the mark on w by strict locality. The old factor q_B(C,S) ignores it
by induction, including the possible case S=C. The first factor is
strictly positive, so division proves that q_B(P,S) ignores it.
Changing the w bit while fixing every other inherited/newborn bit
is allowed by the complete record cube. Finally the full complement
is one minus the sum of all proper probabilities and inherits the
same invariance. Induction completes the proof.

This holds at every defined level of an admissible prefix with the
required diamonds; it is not a new all-size existence theorem.

### Consequences for this candidate

The isolated vertex of every D_i is maximal. Its bit therefore cannot
produce a full-probability contrast. Attempting to force a full-child
correction to zero by changing that isolated bit is ruled out
analytically, rather than left as a numerical test.

Set maximal bits to zero while retaining every other bit. The cap
maxima counts of T1 through T11 are
(4,3,2,3,2,2,2,2,3,2,2). They yield respectively
(8,16,32,16,32,32,32,32,16,32,32) representative rows, totaling 280.
The maxima counts of D1 through D5 are (4,3,2,3,2), yielding
(8,16,32,16,32), totaling 104. Thus this lemma alone reduces the
2048-row quantifier to 384 representative rows with proved equalities
to every omitted marking. It assumes no further automorphism or
stem-record reduction, and no table has been generated.

In particular T1 has four maximal cap vertices. Its full probability
can depend only on its three stem records. All eight stem assignments
must still be retained.

## 3. Native compensation equations, not independent row fits

Write

\[
 w_j=e_{T_j}y_{J_j},\quad v_j=y_{F(T_j)},\quad d_i=y_{F(D_i)},
\]
\[
 f_j(r)=q_B(T_j,r,T_j)>0,\qquad
 g_i(r)=q_B(D_i,r,D_i)>0.
 \tag{5}
\]

The variables w_j are not probabilities. They absorb only fixed positive
empty-birth coefficients; their values are shared across all parents.

At connected parent T_j the only proper child in (3) is its empty-birth
child J_j. Therefore its **complete** correction equation is

\[
 w_j+f_j(r)v_j=z_j\qquad\text{for every marking }r.
 \tag{6}
\]

At D_i=C_i disjoint {w}, each supported proper precursor is an ideal
S of C_i excluding w, and C_i+S must be a T_j. The baseline empty/S
whole-map diamond supplies

\[
 q_B(C_i,r,S)e_{C_i+S}
    =e_{C_i}q_B(D_i,\widetilde r,S).
 \tag{7}
\]

Define, summing every individual supported ideal rather than one per
child class,

\[
 L_i(r;w)=
   \sum_{S:\,[C_i+S]=T_j}q_B(C_i,r,S)w_j.
 \tag{8}
\]

The complete D_i equation is exactly

\[
 L_i(r;w)+e_{C_i}g_i(\widetilde r)d_i=0.
 \tag{9}
\]

Unsupported and full slots other than the named full correction have
zero correction, not zero baseline probability. The old isolated bit
in tilde-r is irrelevant by the proved lemma; all remaining records
and multiplicities are retained. Equation (7) holds separately for
every inherited marking and both newborn bits.

All rows outside (2) vanish in the correction system by section 1.
Consequently (6),(9), together with the following strict inequalities,
are necessary and sufficient for this specific finite support:

\[
 w_j>-4e_{T_j},\qquad v_j>-4,\qquad d_i>-4.
 \tag{10}
\]

Indeed these make every h8 positive, and h7=1+Z/4 is the unchanged
positive accepted seed. The RI-99/101 transform q_Q=q_B*h8(child)/h7(parent)
then gives complete normalization, direct record locality, marked
equivariance and the whole-map diamond identities. Conversely any
positive transform confined to (3) has these equations and inequalities.

### The exact record compatibility left by private full columns

Choose one reference record r0 for each parent. Connected rows require

\[
 v_j=\frac{z_j-w_j}{f_j(r_0)},\qquad
 (z_j-w_j)\,[f_j(r)-f_j(r_0)]=0\quad\text{for every }r.
 \tag{11}
\]

Thus any actual record contrast in f_j forces v_j=0 and w_j=z_j.
If f_j is constant, this conclusion does not follow.

For a disconnected parent the reference recovery and all remaining
compatibilities are

\[
 d_i=-\frac{L_i(r_0;w)}{e_{C_i}g_i(r_0)},\qquad
 g_i(r_0)L_i(r;w)-g_i(r)L_i(r_0;w)=0
       \quad\text{for every }r.
 \tag{12}
\]

A generic nonmaximal-record contrast changes both L_i and g_i, so
nonconstant g_i alone does not force d_i=0. Its isolated bit cannot
supply the needed one-sided contrast, by section 2.

Recovered full-child positivity is still required:

\[
 w_j<z_j+4f_j(r_0),\qquad
 L_i(r_0;w)<4e_{C_i}g_i(r_0).
 \tag{13}
\]

These supplement w_j>-4e_Tj. They are strict; a vanishing full
multiplier is not a repair.

As a conditional consistency check, if all d_i=0 then (8),(9) are
the complete original RI-88 harmonic matrix on w. Its accepted
rank-ten/one-dimensional-kernel result implies w=lambda*z.
If some f_j then has a record contrast, (11) and z_j nonzero force
lambda=1, returning the rejected RI-102 values on every J_j.
Neither premise of this conditional argument is assumed.

## 4. A positive repair forces an exceptional T1 full profile

Use K=C3 ordinal-sum A3, D1=K disjoint A1 and I=C3. The accepted
RI-102 bound, for every stem marking xi, is

\[
 {\cal R}_\xi=\frac{q_B(K,r,I)}{e_K}>41.
 \tag{14}
\]

In the present repair, D1 still has h7=1. Its I birth produces J1,
so (7) gives the exact formal entry

\[
 \widehat q(D_1,\widetilde r,I)
   =q_B(D_1,\widetilde r,I)+\frac14{\cal R}_\xi w_1.
 \tag{15}
\]

The private full-child corrections do not change this slot. If the
complete repaired row is positive and normalized, this entry is
strictly less than one. Baseline q_B(D1,I)>0 then implies

\[
 w_1<
 \frac{4[1-q_B(D_1,\widetilde r,I)]}{{\cal R}_\xi}
 <\frac4{41}<1.
 \tag{16}
\]

The RI-102 stronger proper-mass cap of 1/2 is **not** imposed on the
repaired row: its full probability can now change. Using only the
unit row bound makes (16) valid with arbitrary private full corrections.

Since z1=1, the connected equation (6) consequently forces

\[
 v_1=\frac{1-w_1}{f_1(r)}>0,\qquad
 f_1(r)=\frac{1-w_1}{v_1}
       \text{ exactly independent of all records}.
 \tag{17}
\]

**Native necessary condition.** Any positive repair on (3) must have
a record-constant actual T1 full-birth probability. This is not a
choice of v1 separately per record.

**Conditional obstruction.** If even one pair of T1 markings has
different full probabilities, (11) forces w1=1. Equation (15) then
exceeds 41/4, exactly the RI-102 offending slot. No choices of the
other 26 correction variables can repair that normalized positive row.
This rejects the entire support (3) under the stated contrast, not
just its original empty-birth point.

The contrast has not yet been proved for the actual B. In particular
RI-95's nonzero expression involving differences of D and U does not
imply a nonzero difference of U alone. RI-79's accepted contrast uses
a different unmarked parent and cannot replace the T1 condition.

### Some supported full probabilities really are constant

Let A be any five-parent and P=A ordinal-sum A2. In each six-parent
A ordinal-sum A1, the unique-maximum identity gives proper probabilities
rho*q_B(A,r,S) for every ideal S of A, and full complement 1-rho.

For P, each S contained in A has proper potential
rho^2*q_B(A,r,S), by the two singleton deletions and one double
deletion. The two remaining proper ideals, A plus either top, have
potential 1-rho. Summing the complete A row gives

\[
 U(P,r)=\rho^2+2(1-\rho),\qquad
 q_B(P,r,P)=1-s(2-2\rho+\rho^2).
 \tag{18}
\]

This is genuinely record-constant. Taking A=H5 or A=C5 gives the
supported classes T8 and T11 respectively. Therefore an argument
assuming that every f_j varies would be false within the actual
baseline, not merely unsupported by data.

## 5. The remaining T1 condition is a fixed nonzero polynomial

Use only the already specified RI-89/94 held notation, with records
r=0,1 on T1 changing its first stem bit and leaving others zero.
For stem ideals S in {0,1,3,7}, write

\[
 A_r(S)=q_B(C_3,r,S),\quad
 B_r(S)=q_B(C_4,r,S),\quad
 G_r(S)=q_B(H_5,r,S),\qquad H_5=C_3\oplus A_2.
\]
\[
 c_r=q_B(C_4,r,15),\quad
 h_r=q_B(H_5,r,15)=q_B(H_5,r,23),\quad
 j_r=q_B(H_5,r,31),
\]
\[
 E_r=\sum_{S=0,1,3,7}\frac{A_r(S)G_r(S)^3}{B_r(S)^3}
                  +3h_r^2/c_r+3j_r,\qquad
 v_r^{\,*}=h_r^3/c_r^2,
\]
\[
 K_r=\sum_{S=0,1,3,7}
                 \frac{A_r(S)^3G_r(S)^6}{B_r(S)^8}.
 \tag{19}
\]

The star distinguishes this held scalar v_r* from a full-child
correction v_j in (5). All denominators are positive. These are
symbolic expressions in existing held rows, not newly evaluated
coefficients.

The accepted T1 proper-potential sum is

\[
 U_r(\rho)=4-4\rho E_r+6\rho^2j_r
                    +4\rho^3v_r^{\,*}+\rho^4K_r,\qquad
 f_1(r)=1-sU_r(\rho).
 \tag{20}
\]

Let Delta mean record1 minus record0. Since rho,s>0,

\[
 f_1(1)=f_1(0)
 \quad\Longleftrightarrow\quad
 P_{01}(\rho)=0,
\]
\[
 P_{01}(x)=-4\Delta E+6x\Delta j
                      +4x^2\Delta v^{\,*}+x^3\Delta K.
 \tag{21}
\]

The accepted RI-94 consequence (j1-j0)*z3>0 gives Delta j nonzero.
Thus P01 is a **nonzero** polynomial of degree at most three:
its coefficient of x is 6*Delta j. This does not imply that it is
nonzero at the actual rho.

All actual held prefix probabilities are rational. Each six-parent
proper potential and row sum is a finite rational expression in those
probabilities. There are finitely many complete six-parent rows, so
their maximum M6 is rational. Hence the actual
rho=1/[2(1+M6)] is a positive rational number, without computing M6.

With the unchanged rigorous outer bound

\[
 R=\frac1{2(1+\max(E_0,E_1))},\qquad 0<\rho\leq R,
 \tag{22}
\]

any positive repair therefore requires the actual rho to be a rational
root of the fixed nonzero P01 in (0,R]. There are at most three such
candidates, but none has been calculated here. Satisfying this necessary
condition would not satisfy the rest of (6),(9),(10).

## 6. Smallest justified next contrast design, not execution authority

The first bounded decision needs exactly the already retained six
complete C3/C4/H5 rows at records0,1: 32 probability slots in total.
It needs neither the other eight z coordinates nor new six/seven-parent
probabilities or a global M6/M7 table. Delta j nonzero is already an
accepted premise; the new decision would evaluate the previously
specified coefficients Delta E, Delta j, Delta v* and Delta K, and R.

A separately authorized exact arithmetic review could test whether
P01 has an admissible rational root. A complete rational-root exclusion
in (0,R] suffices to reject this compensation support. A Sturm proof
of no real root there is a stronger sufficient result. Real roots
that are irrational do not match the rational actual baseline scale.

If an admissible rational root survives, the outcome is **unresolved**,
not acceptance of the repair and not identification of the actual rho.
One must not substitute that root as a newly selected scale.

The smallest justified all-record refinement for this same parent
retains all eight stem assignments: eight C3 rows, eight C4 rows and
eight H5 rows, totaling 24 complete rows /128 slots. They are a subset
of the existing RI-88 forty-row/224-slot held domain. Omitted maximal
bits are removed only by the proved invariance and existing transport.
No new parent shape is required.

Relative to reference stem0, form the seven polynomials P_(0,xi) from
(21). Their monic rational gcd is well-defined because P01 is nonzero;
identically zero differences impose no constraint. A constant gcd, or
a gcd with no rational root in the admitted interval, rules out
simultaneous T1 constancy and hence rejects (3). An actual surviving
common root remains only a candidate scale. Excluding it would require
a justified additional bound on actual rho or other native equations,
not an unauthorized complete-layer calculation.

These domains are the smallest justified fixed-pair and full-stem
tests for this derived obstruction, not a claim of global input
minimality. No saved certificate has been decoded, coefficient
calculated, test implemented or expansion authorized by this design.

## 7. A minimal structural alternative, conditional on rejection

Additional private full children outside (2) are ineffective by section1.
If a T1 contrast rejects (3), repairing T1 must change at least one
additional proper child incident to it; changes only to other parents
would leave its conflicting equation unchanged.

One structurally minimal extra column is RI-99's

\[
 Y_0=C_3\oplus A_5.
 \tag{23}
\]

It is connected with five maxima, so it is neither a J_j nor a full
child. Every maximal deletion gives T1. Thus adding this one column
introduces no new incoming parent class; it adds five backward roles
but only the one forward core-ideal slot of T1. If separately pursued,
the totals would be 28 columns, sixteen parents, 59 backward roles
and 51 forward slots. Its new equation would be

\[
 w_1+q_B(T_1,r,C_3)y_{Y_0}+f_1(r)v_1=1,
 \tag{24}
\]

with all its record compatibilities and y_Y0>-4 still required.
The other parent equations would not acquire this column.

One is the least possible positive increase in number of child
variables. This is only a minimal structural alternative: no claim
of feasibility, optimality, completed repair or new execution follows,
and Y0 is **not** included in the current candidate (3).

## 8. Status, source boundary and handoff

New analytic results are maximal-record invariance, the exact native
27-column compensation system and record quotient, the quantitative
necessary bound w1<4/41, the resulting record-constant T1 requirement,
the actual constant-profile counterexamples T8/T11, and reduction of
a possible rejection to a fixed nonzero polynomial of degree at most
three at a rational scale.
The original compensation family's actual positive feasibility remains
unresolved. This is not a repeated declaration of RI99 elimination
as if it solved that question.

No inference of full sensitivity is taken from permission to read
records, no isolated-bit contrast is presumed, and RI95's different
obstruction is not reused as a T1 full-profile contrast. The complete
row inequalities and shared child values remain load-bearing.

Load-bearing accepted sources are RI-38, RI-85/88, RI-89/94,
RI-99/101 and the accepted RI-102 obstruction. The external PREMISES.json
pins their source identities and root decisions. This is manual symbolic
research, not proof-assistant verification or a new empirical result.

Only explicit Markdown source paths were searched. One read-only
search also named a nonexistent anticipated result-note path; its
error was retained, the actual result-note filename was then resolved,
and no scientific certificate body was accessed by that search.
Prior RI102 discovery/read incidents and their corrected evidence
remain unchanged. No helper/checker was imported, compiled or run,
no native coefficient or global table was evaluated, and no scale,
amplitude, seed or numerical search was selected.

The proposed research artifact is this REPAIR.md for
docs/track_b/native_growth_full_birth_repair_v1/. External premise,
source and review metadata are not executors. Coordinator acceptance,
all repository edits, index/git/publication, and any arithmetic
admission remain coordinator-owned. RET stays paused; Option B and
metric-as-record Status M are unchanged. No full QM, measurement,
geometry, mass/gravity or all-size positivity claim follows, and
this bounded handoff does not pause the parallel programme.
