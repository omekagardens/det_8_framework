# RI128 — actual-scale containment and a bounded sign-certificate reduction

27 September 2026 UTC. Analytic author manuscript; no scientific execution.
The accepted H30 support, baseline B, fixed seed and amplitude 1/4 remain.
RI127 already proves the complete connected cancellations, transport and
native beta/Gamma signs. None of that work is repeated as a new test here.

## 1. Analytic result and the unresolved native decision

The actual common half-scale definitions imply, without evaluating a single
new probability or either global maximum,

\[
 M_6\geq1,\quad M_7\geq1,\qquad
 0<\rho\leq\tfrac14,\quad 0<s\leq\tfrac14.
 \tag{B1}
\]

Consequently the fixed rectangle

\[
 X=\min\{R,\tfrac14\}>0,\qquad Y=\tfrac14,
 \qquad 0<x\leq X,\quad 0<y\leq Y
 \tag{B2}
\]

is proved to contain the unchanged actual pair (rho,s). This is an
analytic containing domain, not a chosen baseline, sampled range or
substitute for M6/M7.

The reviewed premises and bounds do not settle the actual signs of
C2 and C3 in this manuscript. In particular positive beta/Gamma gives
no sufficient magnitude estimate. This is the stopping point of this
bounded analytic examination, not a theorem of nonderivability or a
countermodel to the fully fixed baseline.

A simple remaining sufficient certificate on (B2) uses four
univariate endpoint polynomials and their exact signed-coefficient
envelopes. Their x-degrees remain at most five or three. No root finder,
new row family or actual-scale calculation is required to define that
certificate. Its result may be unresolved; failure of a sufficient bound
is not a positive continuation. Section5 proves the method and names
every remaining premise. It is not executed here.

## 2. Why the half-scale domain really tightens

RI85 fixes the actual size-six baseline to the RI38 common half-scale
continuation. RI102 explicitly applies the same construction at size
seven. For n=6,7 its definitions are

\[
 u(P,r,S)=
 \prod_{\varnothing\ne B\subseteq\operatorname{Max}(P)\setminus S}
 q_B(P\setminus B,r|_{P\setminus B},S)^{(-1)^{|B|+1}},
\]
\[
 U(P,r)=\sum_{S\subsetneq P\text{ individual ideal}}u(P,r,S),
 \quad M_n=\max_{|P|=n,r}U(P,r),\quad
 a_n=\frac1{2(1+M_n)}.
 \tag{B3}
\]

Here a6=rho and a7=s. The maximum covers every complete marked n-parent
row, not selected representatives or only supported perturbation rows.
It is finite by the already defined finite positive prefix. Its value
is neither queried nor reconstructed in this proof.

Take any (n-1)-parent Q and form P=F(Q), adding a new vertex v above
all of Q. Such an unmarked n-order is in that complete domain. It may
be taken to be a chain, but no new chain probability is needed.
Its unique maximum is v. Any ideal containing v contains all of Q
and hence is P itself. Thus the proper ideals of P are **exactly all
individual ideals of Q**, including the full ideal Q once.

For each such S the omitted-maxima set in (B3) is {v}. It has just
one nonempty subset, with exponent +1, so the potential is exactly

\[
 u(F(Q),r,S)=q_B(Q,r|_Q,S).
 \tag{B4}
\]

This applies to S=Q as well. That factor is the full probability of
the smaller parent, not a proper probability incorrectly substituted
for it. The complete smaller row is normalized. Counting every one
of its ideals gives

\[
 U(F(Q),r)=\sum_{S\text{ ideal of }Q}q_B(Q,r|_Q,S)=1.
 \tag{B5}
\]

All Q records are retained. The record on v is outside every proper
precursor; the deletion identity holds for either value, rather than
requiring a preferred mark. The original fair newborn factor and
whole scalar-passive payload maps are unchanged; (B5) is normalization
of the complete ideal probabilities, with both newborn bits summed in
the same convention as M_n. It neither erases an inherited record nor
conditions on support membership.

At n=6, Q is a size-five order with the actual strict-mixture row.
At n=7, Q is a size-six order with its already normalized actual row.
Only their normalization is used. No size-six or size-seven value is
evaluated. Since the full maximum includes these rows, (B5) proves
M6>=1 and M7>=1. Applying their actual definitions gives (B1), and
intersecting with the accepted 0<rho<=R proves (B2). Equality at 1/4
is conservatively retained; no unproved strict bound is needed.

This argument does not substitute a later common scale for RI63's
size-five strict mixture. At the size-five level it uses only the
actual normalized complete row. It also does not identify a maximum:
one known row sum gives a lower bound on M, not its value.

## 3. The exact accepted sign question

Use RI127's fixed held expressions

    r2_xi = a*d_xi*g_xi^3/b_xi^4,
    r3_xi = a*g_xi^3/b_xi^3,
    D2 = r2_0-r2_1 > 0,  D3 = r3_0-r3_1 > 0,
    v = V1-V0 > 0,  q(x) = -Q2_1(x) > 0 on (0,R].

The positive empty-slot expressions epsilon2,epsilon3 and the complete
reference proper-potential sums U20,U30 are exactly those in the
accepted DECISION_CONTRACT.md. In particular U20 has degree at most
three and U30 at most two. Both include every individual proper ideal;
their associated full complements are 1-sUj0(rho).

The accepted positively cleared targets are

\[
 P_2(x,y)=q(x)z_2+4x^2D_2+
 4y\{q(x)x^3(\epsilon_2+r_{2,0})-U_{20}(x)x^2D_2\},
\]
\[
 P_3(x,y)=(1-x)vz_3+4xD_3+
 4y\{(1-x)vx^2(\epsilon_3+r_{3,0})-U_{30}(x)xD_3\}.
 \tag{B6}
\]

At the actual baseline,

\[
 C_2=P_2(\rho,s)/q(\rho),\qquad
 C_3=P_3(\rho,s)/[(1-\rho)v].
 \tag{B7}
\]

The denominators are strictly positive throughout the selected domain
in x. Therefore one proved P_j(rho,s)<=0 rejects simultaneous local
positivity and hence H30. It does not require identifying the older
seed-bad index first. Two proved positive values establish only the
two connected local intervals, not a simultaneous whole-support law.

No z coordinate is calculated here. The inherited statement
z2<-4e2 OR z3<-4e3 is a disjunction. An argument assuming one particular
negative coordinate needs an additional justified premise. The method
below instead tests each fully defined target, so it cannot silently
replace that disjunction by a chosen index.

## 4. Why the new bounds are not already a sign proof

RI127 supplies the exact strict local margin

\[
 C_j=z_j+4(e_j+k_j(0)+f_j(0)\beta_j).
 \tag{B8}
\]

The positive terms in (B8) compete with a possibly negative z_j.
Bounds beta_j>0, Gamma_j>0, |z_j|<=1 and f_j(0)>1/2 do not decide
their magnitude comparison. The new **upper** scale bounds are valid
and can strengthen an obstruction certificate, but do not supply a
lower bound on Gamma or prove either native margin positive.

The source reading and hand elimination here have not proved a
uniform nonpositive P2 or P3 on (B2), nor a sufficient native lower
bound for both margins. No unpublished coefficient signs, pointwise
fits, numerical z values or actual-scale assignments are used to
bridge that gap.

The already accepted small-x limit still applies to (B2): q(0)>0,
beta2=O(x^2), beta3=O(x), and C_j(x,y)->z_j uniformly for bounded y.
At least one fixed z_j is negative. Shrinking only the upper bounds
to X,Y leaves arbitrarily small positive x, so a blanket certificate
of **both** margins positive on this whole rectangle is impossible
under the actual premises. This is not a negative conclusion at the
actual pair. It means that the fixed-box route can establish an
obstruction or remain unresolved; a claim of uniform simultaneous
positivity would conflict with an accepted analytic premise.

The rectangle is an outer domain, not a claim that every trial pair
defines the actual baseline or even an admissible complete law.
Uniform exclusion on it is sound because it contains the actual
point. A surviving portion of it does not establish that the actual
point lies in that portion.

## 5. A simple sufficient exact certificate

This is a source-only proof method, not an implemented checker or
permission to perform its arithmetic. Fix (B2) before any evaluation;
do not adapt the domain to a favorable outcome.

Write each target, exactly, as

\[
 P_j(x,y)=A_j(x)+y B_j(x),\quad
 E_{j,0}(x)=A_j(x),\quad E_{j,Y}(x)=A_j(x)+YB_j(x).
 \tag{B9}
\]

For 0<=y<=Y,

\[
 P_j(x,y)=(1-y/Y)E_{j,0}(x)+(y/Y)E_{j,Y}(x).
 \tag{B10}
\]

Thus it is enough to prove a sign of the two endpoint **polynomials
for every x**, not merely evaluate P at the four box corners. Both
endpoint degrees remain at most five for j=2 and three for j=3.
There is no need to divide by B_j or assert its sign.

For any one endpoint polynomial

\[
 E(x)=c_0+\sum_{i=1}^{d}c_i x^i,
\]

define exact bounds

\[
 L(E;X)=c_0+\sum_{i=1}^{d}\min(c_i,0)X^i,\qquad
 U(E;X)=c_0+\sum_{i=1}^{d}\max(c_i,0)X^i.
 \tag{B11}
\]

For x in [0,X], 0<=x^i<=X^i. A nonnegative coefficient contributes
between zero and c_i X^i; a negative coefficient contributes between
c_i X^i and zero. Summing these valid individual intervals proves

\[
 L(E;X)\leq E(x)\leq U(E;X)
       \quad\hbox{for every }x\in[0,X].
 \tag{B12}
\]

The constant term is included exactly once, not replaced by its
positive or negative part. This is an elementary rational envelope,
not a numerical root estimate or an assertion that the bound is sharp.

For each j the sound sufficient classifications are:

1. If both U(E_j0;X)<=0 and U(E_jY;X)<=0, then P_j<=0 throughout
   the containing rectangle. This proves a restricted H30 obstruction.
2. If both L(E_j0;X)>0 and L(E_jY;X)>0, then P_j>0 throughout
   the rectangle. This proves that one local interval exists at the
   actual pair; it is not a whole-support result.
3. Otherwise the sign is unresolved by this certificate. A failed
   envelope is not a polynomial counterexample, a zero result or a
   feasible point.

The two endpoints refer to y=0,Y; (B12) supplies the whole x interval.
The method conservatively includes x=0 and y=0 even though actual
scales are positive. Including excluded boundary points can weaken a
certificate but cannot create a false sufficient sign statement.
Exact zeros and degree drops are retained. A zero polynomial passes
the nonpositive test, never the strict-positive test. No floating
tolerance or excluded-upper-endpoint convention is allowed.

The resulting combined conclusion is: any nonpositive target rejects
H30; otherwise two positive targets would imply two local interval
existences; otherwise unresolved. Section4 independently precludes
the second combined outcome on this unchanged full rectangle for the
actual accepted premises. Retaining the logical distinction prevents
an unresolved envelope from being promoted to a local positive result.

This very small certificate is sufficient, not complete for polynomial
sign determination. If it is unresolved, no new adaptive subdivision,
root routine, larger input set or changed support is implied. Those
would require their own justified research-owner scope, not a silent
repair of this declared method.

## 6. Exact remaining premises for a later bounded certificate

All of the following remain separate from this analytic proof:

- Authenticated, already accepted complete RI115/122/124/127 premises,
  including native sign and record-pattern proofs. They cannot be
  replaced by selected two-record observations.
- The existing eight complete held rows at records0/1 of C3,C4,C5,H5,
  with 44 individual slots and all positive normalized full complements.
  Those suffice for the defined scalar targets only because the full
  forty-row/224-slot pattern is already accepted. No new row is needed.
- Explicit authority to reuse the authenticated fixed z2,z3 coordinates
  in numerical arithmetic, or a separately accepted analytic elimination
  of them. Their prior acceptance alone is not numerical extraction
  authority in this author task. No H/z reconstruction is proposed.
- Exact complete reconstruction of the held expressions and P2/P3,
  with their original E0/E1-derived R, positively justified denominators,
  all endpoint coefficients, and the fixed X=min(R,1/4),Y=1/4.
- A proved envelope sign from those exact coefficients. No such sign
  has been computed or supplied by this manuscript.

No actual rho, s, M6 or M7 is an input to the proposed certificate;
their membership in (B2) is the analytic theorem in section2. No
K4/K5 data, new q6/q7 row, native replay, global enumeration, altered
seed or amplitude is needed for this sufficient connected obstruction
attempt. This does not assert that the chosen envelopes will succeed.

Any implementation/source review and actual execution admission remain
separate. This note creates none of them and executes no target.

## 7. Two optional analytic observations, not new targets

### A stronger unused upper bound on s

For any five-parent A, take the seven-parent P=A ordinal-sum A2.
Its two maxima are above all of A. For every ideal S of A, deleting
either maximum gives F(A), a six-parent. By the unique-maximum
argument its proper probability at S is rho*q_B(A,S). Deleting both
maxima gives A. The two-maxima product is consequently

\[
 u(P,S)=\rho^2q_B(A,S).
\]

There are exactly two other proper ideals, A plus either maximum.
Each has potential equal to F(A)'s full complement 1-rho. Summing
the entire A row, including its full ideal, therefore gives

\[
 U(P)=\rho^2+2(1-\rho)=1+(1-\rho)^2.
 \tag{B13}
\]

Every inherited marking is covered: the smaller A row is complete,
the new top marks do not enter its proper factors, and the full
F(A) complement is exactly 1-rho for every mark. This is the same
identity already used for T8/T11 in RI103, not a new probability
calculation. Since rho<=1/4, U(P)>=25/16 and hence

\[
 s\leq\frac1{2(3-2\rho+\rho^2)}\leq\frac8{41}<\frac14.
 \tag{B14}
\]

This stronger bound is recorded as an analytic consequence only.
It does not change the fixed certificate domain Y=1/4 selected in
section1, introduce a rational-function domain or authorize a retry
on a different box after seeing an outcome.

### A seed-free necessary combination

The accepted complete K=C3 ordinal-sum A3 harmonic row, with z1=1,
is r3_0+3m0*z2+3j0*z3=0, where m0,j0 are strictly positive held
coefficients. Thus the weighted sum of the two local margins is

\[
 W=3m_0 C_2+3j_0 C_3
 =-r_{3,0}+12\{m_0(e_2+k_{20}+f_{20}\beta_2)
                    +j_0(e_3+k_{30}+f_{30}\beta_3)\}.
 \tag{B15}
\]

If both C2 and C3 were positive, W would be positive. Therefore a
proved W<=0 at actual scales, or on an actual-containing domain,
would also reject H30 without selecting a seed-bad index or using
numerical seed coordinates. Equation (B15) is an exact elimination
of the two z terms, not an assertion of its sign. Neither a sign
test nor an executable target for W is introduced here. The selected
bounded method remains the two original P2/P3 targets in section5.

## 8. Shared constraints and handoff boundary

The two connected local intervals are necessary blocks of the complete
system, not independent repairs. Any surviving values t2,t3 enter
the one shared T1 full/reference recovery and its strict bounds.
RI124 already discharged T1's contrasts; its intercept, full-child
positivity and D1 core-slot consequence remain binding. All eight
other connected parents and all five D_i retain their complete
reference/contrast equations, strict bounds and repeated individual
ideal multiplicities. The same recovered w2,w3 occur in those rows.

An actual connected nonpositive result cannot be repaired by those
additional equations; a positive or unresolved connected result cannot
omit them. No full H30 feasible tuple is supplied here. No all-size,
full QM, geometry/gravity, empirical or ontology conclusion follows.

Required review reads were completed: the RI127 independent proof
review Markdown and machine report, and the final root adjudication;
the complete RI127 DECISION_CONTRACT; the final integration change
to LOCAL_POSITIVITY, whose full author text was already read in the
preceding task. RI85, RI102, RI103 and RI117 source proofs were read
completely in the preceding author work and supply the explicitly
restated normalization/unique-maximum identities used here.

The first multi-file display clipped the tail of the independent
review and the opening of its machine report because of its combined
output budget. The machine report was then reread completely and
the Markdown tail through EOF reread; clipped output was not treated
as complete coverage. Two subsequent line ranges were beyond that
115-line Markdown and returned empty; the actual tail was then read.
These were read-only display issues, not scientific execution.

Only this fresh external ANALYTIC_BOUNDS.md is authored. No scientific
JSON body is numerically decoded, target/helper imported, compiled,
parsed as Python/AST, probed or run. No new held value, H/z, actual
scale or numerical polynomial coefficient is evaluated. Predecessor
evidence, repository/index/Git, cards/callers/freezes/admissions and
RET are unchanged. This author is not an independent reviewer of
the note. Complete fresh review and root adjudication remain required.
