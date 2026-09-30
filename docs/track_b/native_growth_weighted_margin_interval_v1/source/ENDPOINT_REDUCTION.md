# RI145 — seed-free weighted margin and exact reference-sum bounds

30 September 2026. Author-side analytic contribution; manual algebra and
source-text reading only. This is not an independent adjudication, a scientific
execution, or an actual-scale sign decision.

## 1. Result and exact scope

The accepted weighted harmonic row eliminates both seed coordinates from
`W=3m0 C2+3j0 C3`. Positive clearing gives precisely two endpoint polynomials
for its nonpositivity on the requested curved domain. Additional accepted
held-row identities give the stronger, strict reference-sum bounds

\[
 \frac74<U_{20}(x)<3,\qquad \frac32<U_{30}(x)<2
 \quad(0<x\le X),\qquad X=\min(R,1/4).
 \tag{1}
\]

In particular, both formal reference complements remain positive throughout
the curved domain. The upper bound on U20 is obtained below from an **exact
positive-term decomposition**, not a generic coefficient envelope. The
singleton-root restoration correction is retained throughout.

No full-domain sign of W, actual C2/C3 sign, actual-scale containment in a
smaller negative interval, or H30 obstruction is established here. A positive
W would only fail this necessary weighted obstruction; it would not establish
either local interval, still less the simultaneous full system. This note
supplies no new held operand, seed, scale, support, row, enumeration, executor,
admission, controller, or runtime qualification.

## 2. Unchanged premises and notation

All held quantities are those of the accepted fixed baseline. For record
representatives i=0,1 and the four individual C3 stem ideals S=0,1,3,7, write
the existing complete held row entries as A_i(S), B_i(S), G_i(S), D_i(S).
Keep c_i as the C4 full probability, h_i as each H5 one-cap probability,
j_i as its full probability, and ell_i as the C5 full probability. All these
entries are strictly positive. H5 has two distinct one-cap slots; neither
is dropped or divided by an orbit multiplicity.

RI127 and RI128 retain

\[
 \begin{gathered}
 m_i=h_i^2/c_i,\quad
 E_i=\sum_S A_i(S)G_i(S)^3/B_i(S)^3+3m_i+3j_i,\quad
 V_i=E_i-m_i-2j_i,\\
 U_{20}(x)=3-A_{2,0}x+B_{2,0}x^2+C_{2,0}x^3,\quad
 U_{30}(x)=2-x-x(1-x)V_0,\\
 A_{2,i}=E_i+2E_{2,i}-j_i,\qquad
 B_{2,i}=2m_i+2j_i+\ell_i.
 \end{gathered}
 \tag{2}
\]

Here C_{2,i} is the old cubic *coefficient*, not the local margin C2.
The complete E2 sum and cubic coefficient remain

\[
 \begin{split}
 E_{2,i}&=\sum_S D_i(S)G_i(S)/B_i(S)
       +e_i^{\rm held}h_i/c_i+h_i+j_i+\ell_i,\\
 C_{2,i}&=\sum_S A_i(S)G_i(S)^3D_i(S)/B_i(S)^4
       +e_i^{\rm held}h_i^2/c_i^2.
 \end{split}
 \tag{3}
\]

Set

\[
 \begin{gathered}
 r_{2,i}=\theta r_{3,i},\quad D_2=\theta D_3,\quad
 D_3=r_{3,0}-r_{3,1}>0,\quad v=V_1-V_0>0,\\
 q(x)=-Q_{2,1}(x)=\Delta A_2-x\Delta B_2-x^2\Delta C_2>0
       \quad (0<x\le R),\\
 R=\frac1{2(1+\max(E_0,E_1))},\quad
 X=\min(R,1/4),\quad d(x)=2(3-2x+x^2).
 \end{gathered}
 \tag{4}
\]

Delta always means record1 minus record0. In contrast, D3 is record0 minus
record1 of the core profile; their signs must not be interchanged. The formal
domain assigned here is 0<x<=X and 0<y<=1/d(x). RI128 B14 proves that it
contains the unchanged actual pair (rho,s); it does not make x,y selectable
actual scales.

The empty coefficients are

\[
 \epsilon_2=A_EG_E^3D_E/B_E^4,\qquad
 \epsilon_3=A_EG_E^3/B_E^3.
 \tag{5}
\]

They are **not** the scaled expressions e_T2=y x^3 epsilon2 and
e_T3=y x^2 epsilon3, which equal the actual probabilities only at
(x,y)=(rho,s); nor is epsilon3 the historical size-three proper probability
or amplitude1/4. At the empty slot the accepted
C5 identity D_E=theta B_E is valid, so

\[
 \epsilon_2=\theta\epsilon_3,\qquad
 H_2:=\epsilon_2+r_{2,0}=\theta H_3,\qquad
 H_3:=\epsilon_3+r_{3,0}.
 \tag{6}
\]

This identity does not assert D_i(S)=theta B_i(S) at every stem slot.

## 3. The retained singleton correction

The RI120 prefix and F2 analytic notes prove, for all transported records,

\[
 \begin{gathered}
 G_i(S)=\theta B_i(S)^2/A_i(S)\quad(S=0,1,3,7),\\
 D_i(S)=\theta B_i(S)\quad(S=0,3,7),\qquad
 e_i^{\rm held}=\theta c_i,\quad h_i=\theta c_i,\quad
 m_i=\theta^2c_i,\\
 N_i:=D_i(1)-\theta B_i(1)\ge0,\qquad
 \ell_i=1-\theta-N_i>0.
 \end{gathered}
 \tag{7}
\]

Introduce only symbolic abbreviations of these held entries,

\[
 \omega_i:=G_i(1)/B_i(1),\qquad
 H_i^{\rm root}:=A_i(1)G_i(1)^3/B_i(1)^4=\theta\omega_i^2.
 \tag{8}
\]

The exact accepted simplifications are

\[
 \begin{split}
 E_{2,i}&=1+(1-\theta)(h_i+j_i)+N_i(\omega_i-1),\\
 C_{2,i}&=\theta(E_i-2m_i-3j_i)+N_iH_i^{\rm root},\\
 A_{2,i}&=E_i+2+2(1-\theta)h_i+(1-2\theta)j_i
                      +2N_i(\omega_i-1),\\
 B_{2,i}&=2m_i+2j_i+1-\theta-N_i.
 \end{split}
 \tag{9}
\]

In particular, N_i is not declared zero or record-independent. Discarding it
would change the held coefficients and could change q.

For the bounds needed here, the exact formula c5=1/[2(1+M5)] with M5>0
gives 0<theta=c5/36<1/72. RI41 fixes A_i(1)=1/44; strict complete C4
normalization gives B_i(1)<1. Thus

\[
 0<\omega_i=44\theta B_i(1)<11/18<1.
 \tag{10}
\]

These are deductions from displayed accepted definitions and positivity,
not evaluation of the scientific certificate or extraction of a new actual
coefficient. In particular no printed large value of M5 or c5 is used.

Since h_i+j_i<1, N_i>=0 and omega_i<1, (9) gives the strict bound

\[
 0<E_{2,i}<2.
 \tag{11}
\]

Its lower bound follows directly from the complete positive sum (3), not
from a difference of terms in (9).

## 4. Exact positive-term decomposition of U20

Use record0 and abbreviate

\[
 T_0:=E_0-3m_0-3j_0
     =\sum_S A_0(S)G_0(S)^3/B_0(S)^3>0,
 \qquad
 \mathscr P_0:=E_{2,0}-\ell_0-N_0\omega_0>0.
 \tag{12}
\]

The second strict inequality is a raw-sum fact: E2 contains ell0 and the
root summand (theta B0(1)+N0)omega0, leaving theta B0(1)omega0 plus all
other strictly positive summands after the two indicated subtractions.

Equations (2), (7)--(9) now give

\[
 \begin{split}
 A_{2,0}&=T_0+3m_0+2j_0+2E_{2,0},\\
 B_{2,0}&=2m_0+2j_0+\ell_0,\\
 C_{2,0}&=\theta(T_0+m_0)+\theta N_0\omega_0^2.
 \end{split}
 \tag{13}
\]

Substitution yields the exact identity

\[
 \boxed{U_{20}(x)=3-x\mathcal K_0(x)},
 \tag{14}
\]

where

\[
 \begin{split}
 \mathcal K_0(x)={}&(1-\theta x^2)T_0
 +(3-2x-\theta x^2)m_0+(2-2x)j_0+2\mathscr P_0\\
 &+(2-x)\ell_0+N_0\omega_0(2-\theta x^2\omega_0).
 \end{split}
 \tag{15}
\]

For 0<x<=1/4, 0<theta<1/72 and 0<omega0<1 every displayed bracket is
strictly positive. The last entire summand may be zero when N0=0; the
other positive summands still give K0>0. Thus U20<3, without assuming a
sign for a held contrast or using a coefficient-envelope estimate.

For the lower bound, (11) gives A20<E0+4. Since B20,C20 are positive
complete held expressions and xE0<=1/2-x by x<=R,

\[
 U_{20}(x)>3-x(E_0+4)\ge5/2-3x\ge7/4.
 \tag{16}
\]

Also V0=T0+2m0+j0>0 and V0<E0. Therefore

\[
 U_{30}(x)=2-x-x(1-x)V_0<2,
 \quad
 U_{30}(x)>2-x-xE_0\ge3/2.
 \tag{17}
\]

This proves (1) throughout the assigned formal x interval. It does not
assume that every formal pair extends to the actual complete baseline.

On 0<x<=1/4, d is decreasing and d(x)>=d(1/4)=41/8. Hence for every
allowed positive y,

\[
 \frac{17}{41}<1-yU_{20}(x)<1,\qquad
 \frac{25}{41}<1-yU_{30}(x)<1.
 \tag{18}
\]

The strict lower bounds use U20<3 and U30<2; they remain strict at the
allowed upper boundary y=1/d(x). These formal-complement inequalities
must not be relabelled as the separate actual-baseline bound f_j0>1/2
used in RI127's local-interval equivalence.

## 5. Seed-free normalized weighted identity

The accepted complete K harmonic row is

\[
 r_{3,0}+3m_0z_2+3j_0z_3=0.
 \tag{19}
\]

Use positive, fixed symbolic ratios

\[
 r:=r_{3,0}>0,\qquad
 \lambda:=D_3/r\in(0,1),\qquad
 \eta:=\epsilon_3/r>0,\qquad
 G_*:=\theta m_0=\theta^3c_0>0.
 \tag{20}
\]

G_* is not the held core probability g_i or held row G_i. Substituting
the RI127 margins, the beta formulas, (6), and (19) gives

\[
 \boxed{\begin{split}
 \frac{W(x,y)}r={}&-1
 +12\lambda x\left[
  \frac{G_*x}{q(x)}(1-yU_{20}(x))
  +\frac{j_0}{(1-x)v}(1-yU_{30}(x))\right]\\
 &+12yx^2(1+\eta)(G_*x+j_0).
 \end{split}}
 \tag{21}
\]

No seed coordinate remains. The s/y factors were neither omitted nor
counted twice: they appear in the empty/core contribution on the final
line and in the two reference complements, not inside epsilon_j.
Equation (18) makes every compensation term on the right of (21)
strictly positive on the assigned domain. Thus W>-r, but that lower
bound is not a sign decision.

## 6. Exact curved-domain endpoint reduction

Let the strictly positive clearing factor be

\[
 \mathcal Q(x)=q(x)(1-x)v.
 \tag{22}
\]

Define seed-free polynomials a,b by

\[
 \begin{split}
 a(x)={}&-q(x)(1-x)v
       +12\lambda x\{G_*x(1-x)v+j_0q(x)\},\\
 b(x)={}&12\{x^2(1+\eta)(G_*x+j_0)q(x)(1-x)v\\
 &\hspace{34mm}-\lambda x[
 G_*xU_{20}(x)(1-x)v+j_0U_{30}(x)q(x)]\}.
 \end{split}
 \tag{23}
\]

Then Q W/r=a+y b. The unnormalized root proposal Q W=A+y B is exactly
A=r a and B=r b, with H2/H3 defined by (6). In particular the positive
empty/core terms in B are 12m0 q(1-x)v x^3 H2 and
12j0 q(1-x)v x^2 H3, not expressions with an already-scaled e_Tj
inserted for H_j.

Set a_+(x)=d(x)a(x)+b(x). Its useful factored form is

\[
 \begin{split}
 a_+(x)={}&-d(x)q(x)(1-x)v\\
 &+12\lambda x\{G_*x[d(x)-U_{20}(x)](1-x)v
            +j_0[d(x)-U_{30}(x)]q(x)\}\\
 &+12x^2(1+\eta)(G_*x+j_0)q(x)(1-x)v.
 \end{split}
 \tag{24}
\]

The additional factors have proved signs:

\[
 d-U_{20}>d-3\ge17/8>0,\qquad
 d-U_{30}>d-2\ge25/8>0.
 \tag{25}
\]

For fixed x and t=d(x)y in (0,1],

\[
 \mathcal QW/r=(1-t)a(x)+t\,a_+(x)/d(x).
 \tag{26}
\]

Consequently, nonpositivity of W on the entire assigned curved domain is
equivalent to a(x)<=0 and a_+(x)<=0 for every 0<x<=X. Sufficiency is
the displayed convex combination. Necessity at y=1/d gives a_+<=0;
necessity for a follows by continuity as allowed positive y tends to zero.
The excluded lower endpoint is not treated as an actual scale.

The degree bounds are at most3 for a and at most6 for b and a_+; possible
degree drops remain exact. These formulas are not an executed sign method,
and no coefficient array has been instantiated. In particular the positive
terms in (23)--(24) do not by themselves compare with their negative term.

## 7. What the remaining endpoint gap actually requires

Already the lower-y limit imposes the exact necessary comparison

\[
 12\lambda x\left[\frac{G_*x}{q(x)}
                  +\frac{j_0}{(1-x)v}\right]\le1
 \quad(0<x\le X)
 \tag{27}
\]

for any full-domain W<=0 proof. At x=X it in particular requires
v>=12 lambda j0 X/(1-X) and q(X)>=12 lambda G_* X^2. These are necessary,
not sufficient, comparisons; positivity of q,v alone does not establish
their required magnitudes. No assertion is made that the actual held
coefficients violate or satisfy them.

The full-domain positive lower bound (18) also gives the conditional test

\[
 \frac Wr>
 -1+\frac{204}{41}\frac{\lambda G_*x^2}{q(x)}
    +\frac{300}{41}\frac{\lambda j_0x}{(1-x)v}.
 \tag{28}
\]

If the right-hand side were proved nonnegative at a specified formal x,
then W would be strictly positive for every permitted y at that x, and
the proposed full-domain nonpositivity statement would fail. No such
premise is proved here; (28) is not an invented numerical countermodel or
an assertion about the unchanged actual baseline.

The exact q identity exposes a genuine retained obstacle to cancelling
these sensitivity ratios. Using Delta=record1-record0, (9) yields

\[
 \begin{split}
 q(x)={}&(1-\theta x^2)v
 +(2-\theta-2\theta x+\theta^2x^2)\Delta h\\
 &+(3-2\theta-2x+\theta x^2)\Delta j
 +(x-2)\Delta N+2\Delta(N\omega)
             -\theta x^2\Delta(N\omega^2).
 \end{split}
 \tag{29}
\]

For example, this follows by writing A2=V+m+(3-2theta)j+
2(1-theta)h+2+2N(omega-1), C2=theta(V-m-j)+theta N omega^2,
and Delta m=theta Delta h before collecting q. No sign of an individual
Delta N, Delta(N omega), Delta(N omega^2), Delta h or Delta j is inferred
from its positive or nonnegative underlying entries. Nor does accepted
q>0 license discarding any of these terms. Thus this derivation does not
replace q by a multiple of v or D3, or replace the actual fixed component
law by a common-scale law.

The companion small-x proof is separately authored. The present endpoint
and positive-decomposition results neither place actual rho in its smaller
interval nor close the full-domain comparisons (23)--(24). A named remaining
comparison is the conclusion, not permission to run a sign computation.

## 8. Exact textual premises and reading scope

The following files were read completely for this contribution; equations
above retain their accepted context, not merely isolated displayed formulas:

- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/DECISION_CONTRACT.md`:
  local margins, empty coefficients, reference sums, pivots, scope.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/LOCAL_POSITIVITY.md`:
  actual-mixture identities, strict local criterion and scope restrictions.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/RECORD_TRANSPORT.md`:
  full-record transport and r2=theta r3, D2=theta D3, m=theta^2 c.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-independent-proof-review-F2Esp0RB/INDEPENDENT_PROOF_REVIEW.md`:
  accepted full-domain transport/sign premises, exact bounds and limitations.
- `/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/ANALYTIC_BOUNDS.md`:
  unchanged actual-containing domain, B14 and the seed-free B15 identity.
- `/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv/INPUT_FORMULAS.md`:
  complete held sums, epsilon notation, q and U formulas, fixed scientific
  input identity and prohibition on unauthenticated scientific extraction.
- `/Volumes/AI_DATA/development/det-review-evidence/ri128-independent-proof-source-review-Q4vXBzjt/INDEPENDENT_REVIEW.md`:
  independently reviewed B14/B15 and complete ideal multiplicities.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`:
  every H5 stem coefficient, singleton C5 exception and h=theta c.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/F2_ANALYTIC_CHECK.md`:
  N>=0, ell=1-theta-N and the exact E2/C2/A2/B2 substitutions.
- `/Volumes/AI_DATA/development/det-review-evidence/ri117-coupled-positive-family-QrAaK5YQ/CONNECTED_CONSTRAINTS_LEMMA.md`:
  complete proper-ideal tables and definitions of E,E2,U2,U3.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`:
  fixed C3 root probability1/44 and complete positive row normalization.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`:
  actual strict-mixture definition theta=c5/36 and c5=1/[2(1+M5)].

A combined earlier text display clipped part of LOCAL_POSITIVITY; its
remaining range was reread through EOF rather than credited as read. The
long RI128 analytic and input notes and the RI117 lemma were read in
successive ranges through EOF. Printed historical scientific constants in
the source text were not extracted into new operands or recomputed. No
scientific JSON body, source AST, symbolic engine, helper, target, probe,
fixture or runtime inventory was processed or executed.

Only this newly assigned Markdown is authored. This is an author-peer
derivation, not independent acceptance of itself or its companion proof.
All 31/139/20/42 runtime obligations remain untouched. The one shared T1
recovery, eight other connected-parent obligations, all five Di conditions,
strict endpoints, fixed seed/amplitude and fixed H30 support remain binding.
RET, other isolated tracks, predecessor evidence, repository/index/Git,
cards and actual runtimes are unchanged. No full QM, geometry, mass/gravity,
empirical or ontology conclusion is drawn.
