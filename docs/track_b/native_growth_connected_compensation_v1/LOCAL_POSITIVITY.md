# RI127 — native connected signs and exact strict local intervals

27 September 2026 UTC. Author proof, source/manual algebra only.
The accepted H30 support, baseline B, seed z, and amplitude 1/4 are
unchanged. No held probability, H/z coordinate, actual rho/s, new
polynomial coefficient, scientific numerical fixture or executor is
evaluated. No K4/K5 data is read or introduced.

## 1. Result and its precise boundary

For the two proper columns added at RI124, the actual fixed baseline has
strictly positive pivot ratios beta2,beta3 and intercept coefficients
Gamma2,Gamma3. Subject to the complete all-record cancellation identities
proved in the companion manuscript, the entire positive local T_j family
(j=2,3) is exactly

\[
 t_j\in\left(\max\{-4,-4/\beta_j\},
                     \frac{z_j+4e_j}{\Gamma_j}\right),\qquad
 v_j=\beta_jt_j,\quad w_j=z_j-\Gamma_jt_j.
 \tag{L1}
\]

Every endpoint is excluded. With the accepted |z_j|<=1 and f_j(0)>1/2,
this interval is nonempty if and only if the single strict inequality

\[
 \boxed{z_j+4e_j+4\Gamma_j>0}
 \tag{L2}
\]

holds. Equivalently, without dividing by an unevaluated contrast,

\[
 \boxed{\mathcal M_j:=
  (z_j+4e_j+4k_j(0))\delta F_j+4f_j(0)\delta K_j>0},
 \tag{L3}
\]

where deltaF_j=f_j(1)-f_j(0)>0 and deltaK_j=k_j(0)-k_j(1)>0.
These are exact support-specific positivity tests, not asserted native
inequalities. Their actual signs are not decided in this note.
If either M_j<=0, the whole H30 repair is impossible. If both are
positive, exactly these two local subsystems pass; shared T1 and D_i
constraints and all other parents remain compulsory.

The complete cancellation premise means every RI124 N_j record minor,
including all identically zero members, vanishes. This note does not
substitute a selected pair for that proof. The same local interval
calculation is valid conditionally while that separate proof is reviewed.

## 2. Definitions inherited from the accepted H30 theorem

The shared child corrections are t2=y_Y2 and t3=y_Y3, with

    Y2 = C3 ordinal-sum (C2 disjoint A3),
    Y3 = C3 ordinal-sum ((A2 ordinal-sum A1) disjoint A2).

Set e_j=q_B(T_j,empty)>0, w_j=e_j*y_Jj, v_j=y_F(Tj),
f_j(r)=q_B(T_j,r,T_j), and k_j(r)=q_B(T_j,r,C3). Each value t_j is
shared with its other incoming parent T1, not independently adjustable
there. All e_j are record-blind. The T2 and T3 equations are

\[
 w_j+k_j(r)t_j+f_j(r)v_j=z_j
       \quad\hbox{for every retained record }r.
 \tag{L4}
\]

The supported child positivity requirements for this local block are

\[
 t_j>-4,\qquad v_j>-4,\qquad w_j>-4e_j.
 \tag{L5}
\]

Use reference record0 and pivot record1. RI122 supplies deltaF_j>0
at the actual unchanged scale. Define

\[
 \beta_j=-\frac{k_j(1)-k_j(0)}{f_j(1)-f_j(0)},\qquad
 \Gamma_j=k_j(0)+f_j(0)\beta_j,
\]
\[
 N_j(r)=[k_j(r)-k_j(0)]\delta F_j
            -[f_j(r)-f_j(0)][k_j(1)-k_j(0)].
 \tag{L6}
\]

The full reference/pivot elimination, without any division by t_j, is

\[
 v_j=\beta_jt_j,\quad w_j=z_j-\Gamma_jt_j,
 \quad t_jN_j(r)=0\quad\hbox{for every record }r.
 \tag{L7}
\]

The complete domains are all sixteen T2 eta values and all eight T3 xi
values, transported to their complete 128-mark cubes by RI117. The
conservative whole-support domain remains 2048 raw rows or its proved
384-row quotient, with every ideal counted. Neither the quotient nor
the shared-child support is enlarged or reduced by this note.

## 3. Native proper contrasts are strictly negative

Use restoration coefficient theta=c5/36>0, distinct from t2 and t3.
The accepted actual strict-mixture identities in RI102 and the RI120
prefix lemmas give

\[
 a=q_B(C_3,\xi,C_3)=41/44\quad\hbox{independent of }\xi,
\]
\[
 b_\xi=q_B(C_4,\xi,C_3)>0,\quad
 d_\xi=\theta b_\xi,\quad
 g_\xi=\theta b_\xi^2/a.
 \tag{L8}
\]

Only the record-independence and positivity of a are needed; its printed
accepted value is not recalculated. These are actual prefix identities,
not replacement of the size-five mixture by a later common half-scale.
The complete deletion-factor proof in RI124 gives

\[
 k_2(\xi)=s\rho^3\frac{a d_\xi g_\xi^3}{b_\xi^4}
          =s\rho^3\theta^4 b_\xi^3/a^2,
\]
\[
 k_3(\xi)=s\rho^2\frac{a g_\xi^3}{b_\xi^3}
          =s\rho^2\theta^3 b_\xi^3/a^2.
 \tag{L9}
\]

In particular k2=rho*theta*k3 as profiles; no scale is selected by this
identity. The positive constants multiplying b_xi^3 are independent of
records. The strict precursor C3 directly excludes all nonstem marks
from both coefficients.

RI115/117 accepts Delta_1 p<0 for RI111's profile

\[
 p_\xi=a^3g_\xi^6/b_\xi^8
       =\theta^6 b_\xi^4/a^3.
 \tag{L10}
\]

Since a and theta are strictly positive and record-independent, and
x -> x^4 is strictly increasing on positive x, (L10) implies b1<b0.
Monotonicity of x -> x^3 and (L9) then imply

\[
 k_j(1)-k_j(0)<0,\qquad \delta K_j>0\quad(j=2,3).
 \tag{L11}
\]

This is symbolic propagation of an already accepted sign. No held
probability is converted into a fresh numerical operand, and no claim
about the other records is obtained merely from this pivot inequality.

## 4. Native full contrasts and intercept signs are strictly positive

The accepted RI122 complete evidence has V1-V0>0 and every odd Q2
polynomial equal to a strictly negative scalar times its monic quadratic
g. Its separately accepted positivity proof gives g(rho)>0 on the
admissible interval containing actual rho. Thus Q2_1(rho)<0. RI117's
complete ideal/record identities give

\[
 \delta F_3=s\rho(1-\rho)(V_1-V_0)>0,
 \qquad \delta F_2=-s\rho Q2_1(\rho)>0.
 \tag{L12}
\]

Here s>0 and 0<rho<=R<1/2 are fixed accepted premises. A nonzero
polynomial alone would not give the second sign; the accepted root and
sign argument is essential. The historical saved-review note's pending
language is superseded by final RI122 root acceptance, not silently
treated as an earlier acceptance.

Combining (L11)-(L12),

\[
 \boxed{\beta_j=\delta K_j/\delta F_j>0},\qquad
 \boxed{\Gamma_j=k_j(0)+f_j(0)\beta_j>0}.
 \tag{L13}
\]

Every term in the latter sum is strictly positive. In particular the
actual H30 columns do not have a zero intercept, and their proper
profiles are not constant. These signs do not themselves prove the
local positivity inequality (L2).

## 5. Exact local open intervals and endpoint exclusions

Assume every N_j(r)=0, as required separately for the complete-record
branch. Then (L7) solves all rows for any finite t_j. By (L13), the
three strict inequalities (L5) become respectively

\[
 t_j>-4,\qquad t_j>-4/\beta_j,\qquad
 t_j<(z_j+4e_j)/\Gamma_j.
 \tag{L14}
\]

Their intersection is exactly (L1), proving necessity and sufficiency
for this stated local block. No unrelated parent constraint has been
used to widen the interval.

Equivalently, retaining the whole free empty-child correction instead,

\[
 w_j\in\left(-4e_j,\ z_j+4\Gamma_j\min\{1,1/\beta_j\}\right),
 \quad t_j=(z_j-w_j)/\Gamma_j,\quad v_j=\beta_jt_j.
 \tag{L14a}
\]

The direction reversal follows from Gamma_j>0. This is an exact full
interval, not a prescription to set w_j=0. Its upper endpoint can remain
negative even when the interval is nonempty.

For 0<beta_j<1 the lower endpoint is -4: Y_j has zero multiplier there.
For beta_j>1 the lower endpoint is -4/beta_j: F(T_j) has zero multiplier
there. At beta_j=1 both hit zero at the same endpoint. At the upper
endpoint J_j has zero multiplier. Equality at any endpoint never gives
a strict positive law. If the upper endpoint is at or below the lower,
the interval is empty; there is no boundary continuation.

If the interval is nonempty, its midpoint is one explicit symbolic local
witness. This is a conditional finite expression, not a numerical fit or
a chosen global solution. The entire open interval, rather than that
midpoint, must be retained for the shared-parent problem.

At any index with z_j+4e_j<0, every feasible t_j and v_j is negative,
and w_j>z_j. The new proper and full corrections jointly move the empty
child correction upward while canceling the record contrast. At equality
z_j+4e_j=0, t_j=0 is still forbidden, but any sufficiently small negative
t_j in (L1) works locally. If z_j+4e_j>0, t_j=0 is a valid local member.
RI122's strict disjunction ensures at least one of j=2,3 is in the first
case; this note does not select which by unperformed H/z evaluation.

## 6. A single exact local-feasibility margin

Write A_j=-z_j-4e_j. Because |z_j|<=1 and e_j>0,
A_j<1. Also f_j(0)>1/2, by the unchanged global half-scale bound on B.

If 0<beta_j<=1, the interval in (L1) is nonempty exactly when

\[
 -4<(z_j+4e_j)/\Gamma_j,
 \quad\hbox{equivalently}\quad z_j+4e_j+4\Gamma_j>0.
 \tag{L15}
\]

If beta_j>=1, its nonemptiness condition is instead

\[
 A_j<4\Gamma_j/\beta_j
       =4f_j(0)+4k_j(0)/\beta_j.
 \tag{L16}
\]

The right side exceeds 2, whereas A_j<1. Consequently this branch is
always locally feasible. In the same branch (L2) is also automatic,
since 4Gamma_j>4f_j(0)beta_j>2. Combining the two branches proves the
claimed if-and-only-if (L2), not just its necessity.

Equivalently,

\[
 \beta_j>
 c_j:=\frac{-z_j-4e_j-4k_j(0)}{4f_j(0)}.
 \tag{L17}
\]

Here c_j<1/2; it may be negative. Thus beta_j>=1/2 is a sufficient
local condition, as is Gamma_j>=1/4. Neither is asserted for the actual
coefficients. If c_j<=0 then beta_j>0 makes this local block feasible.
If c_j>0, its magnitude comparison with beta_j remains load-bearing.

Multiplying (L2) by the strictly positive deltaF_j gives (L3), because

\[
 \Gamma_j\delta F_j=k_j(0)\delta F_j+f_j(0)\delta K_j.
 \tag{L18}
\]

There is no sign-ambiguous multiplication. At M_j=0, the native local
interval is empty, not a null-result acceptance. In fact that equality
can occur only in the beta_j<1 branch under these bounds; the two
endpoints then coincide at -4.

The signs beta_j>0, Gamma_j>0 and the coarse bounds f_j(0)>1/2,
|z_j|<=1 do not alone force (L2): they supply no positive lower bound
on the magnitude of Gamma_j. The bounded source analysis here does
not establish M2>0 or M3>0, and does not establish either nonpositive.
It leaves these two exact strict predicates, not an unspecified
positivity question. They involve existing held expressions and the
unchanged fixed coefficients; no K4/K5 value is required to state them.

### Existing-input factorization and a limitation of the outer interval

For this subsection only write

    b2_xi = a*d_xi*g_xi^3/b_xi^4,
    b3_xi = a*g_xi^3/b_xi^3,
    delta_bj = bj_0-bj_1 > 0,
    epsilon2 = A_empty*D_empty*G_empty^3/B_empty^4,
    epsilon3 = A_empty*G_empty^3/B_empty^3.

Capital A,B,G,D here are the actual C3,C4,H5,C5 held rows, each at
its empty ideal; these probabilities are record-blind and positive.
The same deletion formulas at the empty ideal give

\[
 e_j=s\rho^{n_j}\epsilon_j,\qquad
 k_j(0)=s\rho^{n_j}b_{j,0},\qquad n_2=3,\ n_3=2.
 \tag{L18a}
\]

These are not new probability queries. Let q(rho)=-Q2_1(rho)>0 and
DV=V1-V0>0. Cancelling positive s factors in (L6) yields

\[
 \beta_2=\frac{\rho^2\delta_{b2}}{q(\rho)},\qquad
 \beta_3=\frac{\rho\delta_{b3}}{(1-\rho)DV}.
 \tag{L18b}
\]

If f_j(0)=1-sU_j0(rho), the unevaluated margin in (L2) is exactly

\[
 C_j(\rho,s)=z_j+4\beta_j+
 4s\{\rho^{n_j}(\epsilon_j+b_{j,0})-U_{j0}(\rho)\beta_j\}.
 \tag{L18c}
\]

The notation C_j here is a margin, not the indexed six-parent catalogue.
The held-probability arguments in (L18a)-(L18c) lie in existing held
records0/1 of C3,C4,C5,H5: eight complete rows and forty-four slots.
The fixed seed symbols and actual unevaluated scales remain separate
premises; they are not claimed to be probability slots in those rows.
Using this smaller domain for these particular expressions does not
replace the separately accepted full forty-row pattern/transport proof,
nor authorize extraction or new numerical arithmetic.

Multiplying C2 by q(rho), or C3 by (1-rho)DV, preserves its sign.
The resulting formal polynomials have degree at most five and three
in rho, respectively, and are affine in s; zero leading coefficients
are allowed. This observation defines a possible exact later sign
target, not a performed polynomial calculation or execution contract.
Seed coordinates z_j remain the fixed accepted symbols, not values
recomputed or refitted here.

There is an analytic reason not to assume that positivity will hold
uniformly on the whole current outer scale interval. The accepted
quadratic positivity includes g(0)>0, so q(0)>0. Formula (L18b) gives
beta2=O(rho^2), beta3=O(rho) as formal rho decreases to zero, while
U20 and U30 are polynomials with constant terms three and two.
Hence (L18c) implies C_j(rho,s)->z_j uniformly for bounded s, in
particular 0<s<=1/2. RI122's strict seed disjunction implies at least
one z_j<0. For that index C_j is therefore negative throughout a
sufficiently small positive-rho part of this formal outer box.

Thus both margins cannot be positive uniformly over every trial point
0<rho<=R, 0<s<=1/2. The same conclusion holds if the trial s domain
is narrowed by positive upper bounds but still permits arbitrarily
small rho. This is a limitation of an outer-domain positivity proof,
**not** an obstruction at the actual baseline scale. The actual rho
is fixed by its complete law and is not chosen or taken to a limit.
A stronger premise about its location, a relation between the actual
scales, or an exact argument at those fixed coefficients would be
needed to turn the remaining margin question into a native decision.
None is invented here.

## 7. Zero-safe branches retained rather than discarded

The native signs (L13) exclude some branches, but their exclusion is
proved from accepted premises rather than built into the algebra:

- If any N_j(r) is nonzero, (L7) forces t_j=0, v_j=0 and w_j=z_j.
  The local block is then strictly positive exactly when z_j>-4e_j.
  An all-zero minor family is a valid alternative, not a missing rank
  result or a reason to invent a nonzero common gcd.
- If the proper profile is constant and the full pivot is nonzero,
  beta_j=0 and all the minors vanish. Gamma_j=k_j(0)>0. The complete
  local interval is (-4,(z_j+4e_j)/k_j(0)), with v_j=0. Its feasibility
  condition is z_j+4e_j+4k_j(0)>0. This branch is absent natively by
  (L11), not invalid in the general theorem.
- If all minors vanish but Gamma_j=0, the intercept stays w_j=z_j.
  The only possible local feasibility requires z_j>-4e_j. If that
  holds, t_j=0 already meets t_j>-4 and beta_j*t_j>-4. Since k_j(0)
  and f_j(0) are positive, Gamma_j=0 would require beta_j<0; hence it
  is excluded by the native beta_j sign. No division by Gamma_j is
  made before excluding this branch.
- A zero pivot proper contrast by itself is not permission to erase
  all other proper contrasts. If beta_j=0 but some remaining contrast
  is nonzero, the corresponding N_j is nonzero and the first branch
  applies. If all remaining N_j vanish, the full proper profile is
  constant. The distinction is retained explicitly.

The coefficients k_j themselves cannot be zero: each is a strictly
positive eligible proper-ideal probability. No zero scientific field
is inferred from a zero contrast. Both full profiles are nonconstant
at the actual baseline by RI122, so this note does not transfer its
pivot division to constant-full parents such as T8 or T11.

## 8. Shared obligations that these intervals do not discharge

The same t2 and t3 enter every T1 row:

\[
 w_1+f_1(r)v_1+k_0(r)t_0+k_{12}(r)t_2+k_{13}(r)t_3=1.
 \tag{L19}
\]

Its record contrasts are already analytically discharged by RI124; its
reference intercept and strict bounds remain binding. Its older positive
family cannot be reused with arbitrary new t2,t3
without substituting them into the complete changed equation. In
particular the recovered full correction v1 is still required to exceed
-4; none of its terms is silently dropped.

Every D_i equation likewise remains

\[
 L_i(r;w)+e_{C_i}g_i(r)d_i=0,\qquad d_i>-4,
 \quad
 L_i(r;w)=\sum_{\text{individual supported }S}
                   q_B(C_i,r,S)w_{j(S)}.
 \tag{L20}
\]

The w2 and w3 determined by (L1) are the same values in these sums.
Every repeated ideal stays separate, and all reference and contrast
equations remain required. T4,...,T11 retain their own full-record and
strict-positivity constraints. No inference that nonconstant g_i forces
d_i=0 is made. No K4/K5 coefficients or D_i numerical decision are
introduced in this note.

If either connected local interval is empty, no completion of these
other equations can repair that necessary subsystem. If both intervals
are nonempty, the global problem is still their intersection with
(L19)-(L20) and all other parent equations using the same unknowns.
This distinction is part of the theorem, not a later caveat.

## 9. Read scope, provenance and handoff

Complete source texts read for this task include RI102 AMPLITUDE.md;
RI117 CONNECTED_CONSTRAINTS_LEMMA.md and ANALYTIC_REDUCTION.md; RI120
F2_ANALYTIC_CHECK.md; RI41 NORMALIZATION.md; RI115 RESULT_REVIEW.md;
the actual RI122 root final adjudication; the complete original RI122
INTERPRETATION.md and actual-audit ADDENDUM.md. The complete RI120 prefix
lemmas and F3 analytic check were read during the preceding author task,
as were the full RI111/103/85/99 proofs. Their relevant accepted
identities are explicitly restated in sections3-4. No scientific
certificate body was decoded or re-evaluated for this task.

The actual RI122 root decision is
/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json,
15,477 bytes, SHA-256
162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc.
It supersedes the historical pending language in its preserved review
notes. RI124 acceptance is the research owner's supplied premise; this
author does not self-adjudicate it or rewrite its evidence.

This author does not claim independent review of this note. The actual
complete result and companion all-record proof require fresh nonauthor
review before root adjudication. Only this new external manuscript and
optional opaque source identities are reserved. No predecessor evidence,
repository/index/Git, execution card, baseline, amplitude, support or
scientific input is changed. This bounded task stops at handoff.
