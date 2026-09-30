# Seed free weighted margin obstruction

This manuscript proves an explicit symbolic interval on which the weighted
connected margin is nonpositive, and a smaller interval with a strict negative
gap. It also derives sharper exact endpoint conditions for the full correlated
domain. **It does not establish that the actual size six scale lies in either
interval, or decide the actual connected signs or H30 feasibility.**

This is the separately assigned RI145 analytic question. The accepted RI128
numerical P2/P3 targets and their fixed rectangle Y=1/4 are unchanged. No target,
numerical coefficient, probability table, seed or global maximum is evaluated.

## Accepted premises and notation

Use RI127 DECISION_CONTRACT, LOCAL_POSITIVITY and RECORD_TRANSPORT, and RI128
ANALYTIC_BOUNDS B14–B15 and INPUT_FORMULAS. All held expressions below refer to
the same accepted baseline and complete record transport. They are fixed
coefficients, not variables to fit. Write

\[
 X=\min(R,1/4),\quad R=\frac1{2(1+\max(E_0,E_1))},\quad
 d(x)=2(3-2x+x^2),\qquad
 \Omega=\{(x,y):0<x\le X,\ 0<y\le1/d(x)\}.
 \tag{1}
\]

The unchanged actual pair (rho,s) belongs to Omega by B14. Formal points in
Omega are not asserted to be complete admissible laws. Let

\[
 r=r_{3,0}>0,\quad j=j_0>0,\quad c=c_0>0,\quad
 v=V_1-V_0>0,\quad q(x)=-Q_{2,1}(x)=q_0+q_1x+q_2x^2.
 \tag{2}
\]

Here c is the full C4 probability, not the restoration scale. The accepted
quadratic sign proof gives q(0)>0 and q(x)>0 on (0,R]. It also expresses Q2_1
as a strictly negative scalar times a monic quadratic, hence q2>0. Subscripts
q0,q1,q2 in (2) are polynomial coefficients, not probability queries.

Use theta=c5/36, the actual size five restoration coefficient. It is not rho
or s. RI127 and RI120's prefix lemmas give

\[
 r_{2,i}=\theta r_{3,i},\quad D_2=\theta D_3,\quad
 m_0=\theta^2c,\quad
 \epsilon_2=\theta\epsilon_3.
 \tag{3}
\]

The last identity follows specifically from the empty-slot identity
D_E=theta B_E. It does not replace every C5 slot by theta times its C4 slot:
the singleton slot retains its nonnegative canonical correction. The epsilon
symbols are held empty coefficients; the scaled seven-parent empty
probabilities are y*x^3*epsilon2 and y*x^2*epsilon3 respectively.

Since r3_i=theta^3*b_i^3/a^2 and 0<b1<b0, define

\[
 \lambda=\frac{D_3}{r}=1-(b_1/b_0)^3\in(0,1),\quad
 \eta=\frac{\epsilon_3}{r}>0,\quad g=\theta^3c>0.
 \tag{4}
\]

The aggregate g in (4) is not the held core probability g_i or row G_i.
No value of theta, b_i, lambda, eta, q, rho or s is instantiated here.

## Exact elimination of the seed coordinates

The accepted harmonic identity with z1=1 is
r+3m0*z2+3j*z3=0. Substituting the two accepted margins and (3)–(4) gives

\[
 \frac{W(x,y)}r=-1+
 12\lambda\left\{
 \frac{g x^2[1-yU_{20}(x)]}{q(x)}+
 \frac{j x[1-yU_{30}(x)]}{(1-x)v}\right\}
 +12y x^2(1+\eta)(j+gx),
 \tag{5}
\]

where W=3m0*C2+3j*C3 at the actual scales. This is an identity of the formal
extensions of those margins, not a new seed. Both weights are strictly
positive. Therefore W<=0 at the actual pair rules out C2>0 and C3>0
simultaneously. W>0 supplies neither individual sign nor a full H30 solution.

For a direct clearing cross-check set H2=epsilon2+r20 and H3=epsilon3+r30,
Q=q(x)(1-x)v>0. Then QW=A+yB with

\[
 A=-rQ+12\{m_0x^2D_2(1-x)v+jxD_3q\},
\]
\[
 B=12\{m_0Qx^3H_2+jQx^2H_3
       -m_0U_{20}x^2D_2(1-x)v-jU_{30}xD_3q\}.
 \tag{6}
\]

Thus the proposed clearing is correct only with the held epsilon coefficients
inside H2/H3, not with already scaled empty probabilities. Every denominator
cleared is strictly positive on Omega.

## Positive reference sums throughout the containing domain

The following estimates use actual prefix structure, not assumed signs of
unevaluated coefficient arrays. RI63's definition c5=1/[2(1+M5)] and M5>0
give 0<theta<1/72 without evaluating M5. RI41 fixes the C3 singleton probability
to 1/44. Since the held C4 singleton probability B0(1) is strictly below one,

\[
 r_{\mathrm{root}}=G_0(1)/B_0(1)
 =44\theta B_0(1)<11/18<1.
 \tag{7}
\]

RI120 F2_ANALYTIC_CHECK retains N0=D0(1)-theta B0(1)>=0 and proves

\[
 E2_0=1+(1-\theta)(h_0+j)+N_0(r_{\mathrm{root}}-1).
 \tag{8}
\]

The complete positive H5 row gives h0+j<1. Equations (7)–(8), theta>0 and
theta<1 imply E2_0<2. It is also positive by its original complete sum of
positive terms. Consequently

\[
 A2_0=E_0+2E2_0-j<E_0+4.
 \tag{9}
\]

B2_0 and C2_0 are strictly positive by their displayed individual-ideal sums.
As x<=R, x(1+E0)<=1/2. Therefore, throughout 0<x<=X,

\[
 U_{20}=3-A2_0x+B2_0x^2+C2_0x^3
 >3-x(E_0+4)\ge5/2-3x\ge7/4.
 \tag{10}
\]

Similarly V0=E0-m0-2j is the sum of four positive stem terms plus 2m0+j,
so 0<V0<E0. Hence

\[
 U_{30}=2-x(1+V_0)+V_0x^2>3/2.
 \tag{11}
\]

There is also a positive-factor upper bound that keeps the singleton correction.
Write T0=E0-3m0-3j, ell0=1-theta-N0, and
J0=E2_0-ell0-N0*r_root. Each is strictly positive: T0 is the complete four-term
stem sum, ell0 is the C5 full complement, and removing N0*r_root from E2_0
leaves its positive restoration root term and the other positive terms.
The prefix formula gives C2_0=theta(T0+m0)+N0*theta*r_root^2. Expanding the
complete U20, without dropping an individual ideal, therefore gives

\[
 U_{20}=3-x\mathcal K(x),
\]
\[
 \mathcal K=(1-\theta x^2)T_0+(3-2x-\theta x^2)m_0
 +(2-2x)j+2J_0+(2-x)\ell_0
 +N_0r_{\mathrm{root}}(2-\theta x^2r_{\mathrm{root}})>0.
 \tag{11a}
\]

Every bracket is positive on 0<x<=1/4 with 0<theta<1/72 and
0<r_root<1; N0 may be zero and is not divided by. Also U30<2 directly from
2-x-x(1-x)V0 with V0>0. Thus the sharper whole-domain conclusions are

\[
 7/4<U_{20}<3,\qquad3/2<U_{30}<2,
 \quad17/41<1-yU_{20}<1,\quad25/41<1-yU_{30}<1.
 \tag{11b}
\]

These are formal-domain estimates, not a claim that each trial point defines
a normalized complete law. We need only the upper bounds by one below; the
actual-law f20>1/2 used in RI127 is not asserted on the entire formal domain.

## An explicit uniform bound and obstruction interval

The positive quadratic q has its minimum on [0,X] at

\[
 t_* = \min\{X,\max\{0,-q_1/(2q_2)\}\},\qquad
 \mu=q(t_*)>0.
 \tag{12}
\]

Completing the square proves this minimum formula. Its positivity follows
from the already accepted positivity on the entire closed interval, not from
a numerical minimum, root estimate or new sign test. Equation (12) is an
unevaluated expression in the accepted coefficients.

d decreases on [0,X] because d'(x)=4x-4<0. Set

\[
 Y_*=1/d(X)\le8/41,
 \quad L=\frac{12\lambda j}{(1-X)v}>0,
 \quad K=\frac{12\lambda g}{\mu}
              +12Y_*(1+\eta)(j+gX)>0.
 \tag{13}
\]

Dropping the negative yU terms in (5), using q>=mu, 1-x>=1-X,
y<=Y*, and x^3<=X*x^2 gives the exact sufficient bound

\[
 \boxed{\quad W(x,y)/r\le-1+Lx+Kx^2\quad}
 \qquad((x,y)\in\Omega).
 \tag{14}
\]

All bounding factors are nonnegative before each multiplication. In
particular no sign of the singleton record contrast or of B in (6) is
invented. The positive complements in (11b) and identity (5) also give
0<W/r+1. Together with (14), this yields the two-sided squeeze
0<W/r+1<=Lx+Kx^2, proving W tends uniformly to -r as x tends to zero
on the curved domain, because L and K are fixed finite constants.

For any margin parameter 0<=alpha<1, unrelated to the fixed amplitude or
component scales, define the positive expression

\[
 \delta_\alpha=\min\left\{X,
 \frac{2(1-\alpha)}{L+\sqrt{L^2+4K(1-\alpha)}}\right\}.
 \tag{15}
\]

The second entry is the positive root of Lx+Kx^2=1-alpha, rationalized
without subtraction. The polynomial is strictly increasing for x>=0.
Thus the proved quantitative conclusion is

\[
 0<x\le\delta_\alpha,\quad0<y\le1/d(x)
 \quad\Longrightarrow\quad W(x,y)\le-\alpha r.
 \tag{16}
\]

In particular delta0 gives a closed nonpositive interval, and delta_(1/2)
gives W<=-r/2<0. They are symbolic positive widths, not selected numerical
scales. No maximum, new scientific operand or favorable point was calculated.

An exact remaining sufficient coefficient premise for this bound to cover
the **whole** actual-containing domain is

\[
 LX+KX^2\le1.
 \tag{17}
\]

If proved, (17) would give delta0=X and an H30 obstruction. It is not proved
here. Alternatively a separately justified actual-scale bound rho<=delta0
would suffice. Current containment rho<=X alone supplies neither assertion.

## Sharper exact endpoint condition and the remaining gap

For clarity about what the estimate may lose, write

\[
 J(x)=\frac{g x^2}{q(x)}+\frac{jx}{(1-x)v},\qquad
 T(x)=x^2(1+\eta)(j+gx)
       -\lambda\left\{\frac{gx^2U_{20}}q+
                         \frac{jxU_{30}}{(1-x)v}\right\}.
\]

Equation (5) is F(x)+12yT(x), where F=-1+12lambda J. For each fixed x,
its supremum over 0<y<=1/d(x) is

\[
 \max\{F(x),F(x)+12T(x)/d(x)\}.
 \tag{18}
\]

The first endpoint may be a limiting value, not attained. It still belongs
in a nonpositivity criterion: if it is positive, continuity gives positive
values at sufficiently small positive y. Consequently uniform W<=0 on Omega
is equivalent to both entries in (18) being nonpositive for every 0<x<=X.
With positive clearing this is exactly A<=0 and dA+B<=0 from (6).

This exact one-dimensional condition is sharper than (17). A failure to
prove (17) cannot be called a positive W, a counterexample or failure of the
endpoint condition. The accepted nonnegative singleton corrections N0,N1 do
not determine their difference or the resulting q contrasts. We have not
proved an additional inequality settling either full-domain condition.

The result is therefore a quantified seed-free obstruction interval and
precise conditional full-domain criteria, **not an actual H30 obstruction**.
Neither the actual scale's membership in delta0 nor (17)/(18) over the full
domain has been established. No claim of nonderivability is made.

## Preserved obligations and evidence boundary

One shared T1 full/reference recovery, its strict bounds and D1 core-slot
consequence remain. The other eight connected parents and all five D_i keep
their complete equations, individual-ideal multiplicities and strict bounds,
using the same recovered variables. Positive W alone does not solve even the
two connected intervals, much less these simultaneous conditions.

All 31 focused variants, 139 policy cases, deeper 20 native/42 audit runtime
obligations and their thresholds remain unchanged. RI143's marker precheck,
fsync/finally-close, census-tail first-cause and provisional-restoration caveats
stay accepted; this proof does not work around them or admit execution.

No scientific body was numerically decoded, source/helper imported, compiled,
parsed as an AST, probed or run. No q6/q7, M6/M7 enumeration, H/z reconstruction,
new probability table, candidate, amplitude change, controller or fixture was
created. The old numerical certificate and Y=1/4 stay immutable. RET remains
paused and measurement remains separate. No geometry, gravity, full QM,
all-size, empirical or ontological claim follows from this finite inequality.

Exact source identities and accepted-review boundaries accompany the handoff.
The supporting cross-checks are author contributions, not independent acceptance.
Independent proof review and root adjudication remain required.
