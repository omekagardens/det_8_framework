# RI173 canonical correction and weighted endpoint slope

30 September 2026. Manual author proof at the unchanged actual same-law
prefix, submitted for independent root review. No coefficient vector,
scientific JSON, engine or target/helper was executed or decoded.

## Result and unresolved actual comparison

The weighted expression has a strictly negative y-slope on the whole accepted
x-domain whenever the actual sensitivity satisfies v<=T_R, where

    T_R = lambda*j_0*U30(R)
          /[R(1-R)(1+eta)(j_0+G_*R)].                    (1)

Moreover T_R>(7957/891)B>8B, with the unchanged capacity threshold
B=12lambda*j_0*R/(1-R). Thus the substantive sufficient regime v<=8B
includes the capacity-failure side v<=B and part of the capacity-pass side.
Neither membership in that regime nor unconditional slope nonpositivity
is asserted for the actual prefix.

The companion [SLOPE_REGION.md](SLOPE_REGION.md) proves the region and strict
margin. This note supplies the full canonical substitution, keeps the three
signed correction products, and resolves the complementary regime into a
unique crossover followed by an exact selected-prefix upper-q comparison.
The source of any remaining gap is therefore specified without treating
the canonical correction or q as independently tunable quantities.

This is not another finite-layer contrast implication. RI172's varying
coefficient path is not used as an unchanged-law example or counterexample.
The actual fixed prefix and all its later same-law correlations remain fixed.

## Complete same-law data and the actual-containing domain

For the four distinct C3 stem ideals S=0,1,3,7 keep the entire row

    A(S)=(e,e,e,a_3),       e=1/44,       a_3=41/44.

Write the actual complete C4 rows as (w,p_i,s_i,b_i,c_i), i=0,1. Define
only aliases of the unchanged accepted quantities:

    theta=1/[72(1+M5)],       0<theta<1/144,
    K_i=sum_S B_i(S)^2/A(S)+2c_i,
    T_i=sum_S B_i(S)^3/A(S)^2,
    j_i=1-theta*K_i,
    h_i=theta*c_i,           m_i=theta^2*c_i,
    E_i=theta^3*T_i+3theta^2*c_i+3j_i,
    V_i=theta^3*T_i+2theta^2*c_i+j_i,
    v=V_1-V_0>0.                                          (2)

Every stem sum includes the empty ideal. The factor2 in K_i counts the
two distinct one-cap ideals of H5; it is not an orbit-divided contribution.
The actual lower-prefix probabilities, their global components and all
transported records have their inherited meanings.

The canonical-cap theorem RI157 proves

    Z=R=1/[2(1+max(E_0,E_1))],       1/8<R<12/95<1/4.    (3)

The extra canonical F_i cap terms are inactive at the actual prefix; neither
record's canonical correction was set to zero to prove that theorem.
R is an actual-containing cap, not the actual scale rho and not the global
M6 itself. Keep the full formal domain

    0<x<=R,       0<y<=1/d_dom(x),
    d_dom(x)=2(3-2x+x^2).                                (4)

It contains the unchanged actual pair (rho,s); x and y are not selectable
actual scales. The endpoint y=0 is excluded and used only as a limit.

For RI145's exact weighted identity, retain

    r=theta^3*b_0^3/a_3^2>0,
    lambda=1-(b_1/b_0)^3 in(0,1),
    eta=41^2*(w/b_0)^3 in(0,1/32),
    G_*=theta^3*c_0>0,       j=j_0>71/72.                 (5)

The empty/core restoration factor cancels in eta. It is not an independent
large inverse-theta parameter. Complete H5 normalization gives j+G_*R<1;
RI155 also proves V_0<1. These same-law inequalities are used in the
companion sign proof. No maximum, actual scale or probability is evaluated.

## Full canonical singleton correction

Use RI151's actual lower-prefix probabilities f_i and g_(i,u) from the
four-event V parent, and define

    chi_i=41p_i-f_i/2-min(g_(i,0),g_(i,1)),
    sigma_i=[chi_i]_+/c_i,       gamma=35/1476,
    N_i=gamma*sigma_i,
    omega_i=theta*p_i/e,
    ell_i=1-theta-gamma*sigma_i>0.                        (6)

Equation(6) is the exact canonical result, not a free nonnegative bound.
It follows from RI151's target coordinate
[chi_i]_+/(41p_i*c_i) and its strict-mixture factor35/36. The minimum of
the two g values is retained, including ties. No current positive-part
branch or root order is selected.

The full held proper rows remain

    G_i(S)=theta*B_i(S)^2/A(S)               for all S,
    D_i(S)=theta*B_i(S)                     for S=0,3,7,
    D_i(1)=theta*p_i+gamma*sigma_i.                       (7)

Thus dropping N would change the actual C5 singleton. Its nonnegativity
does not imply that it is positive, record-blind, or ordered across roots.
Likewise ell_i is its genuine full complement, not an independent entry.

To make the substitution explicit wherever the reference polynomial uses
N_0, retain the RI145 complete coefficients

    A20 = E_0+2+2(1-theta)h_0+(1-2theta)j
          +2gamma*sigma_0*(omega_0-1),
    B20 = 2m_0+2j+1-theta-gamma*sigma_0,
    C20 = theta*(E_0-2m_0-3j)
          +gamma*theta*sigma_0*omega_0^2,
    U20(x)=3-A20*x+B20*x^2+C20*x^3,
    U30(x)=2-x-x(1-x)V_0.                                (8)

The complete positive-sum interpretation and RI145 bounds still apply:
7/4<U20(x)<3 and 3/2<U30(x)<2. These are the actual reference functions
with(6) substituted, not an unrelated favorable polynomial pair. The zero
branch sigma_0=0 is included in(8).

## All three signed products in q

Let Delta mean record1 minus record0. Define the part without the explicit
singleton correction by

    T_core(x)=(1-theta*x^2)*v
       +(2-theta-2theta*x+theta^2*x^2)*Delta h
       +(3-2theta-2x+theta*x^2)*Delta j.                 (9)

This is a signed held expression; no positivity of T_core, Delta h or
Delta j is assumed. RI145 equation(29), with the full substitution(6), is

    q(x)=T_core(x)
       +gamma*((x-2)*Delta sigma
               +2*Delta(sigma*omega)
               -theta*x^2*Delta(sigma*omega^2)) > 0.     (10)

The final inequality is the separately accepted full-domain sign of the
complete actual q. It does not follow from a sign assigned to any one of
the three displayed differences. None of them is discarded. In particular
Delta(sigma*omega^2) is a difference of products, not the square of a
difference or a product of separate contrasts.

For a sign-explicit regrouping only, put

    k_i(x)=2-x-2omega_i+theta*x^2*omega_i^2.

Then the identical formula is

    q(x)=T_core(x)+gamma*(sigma_0*k_0(x)-sigma_1*k_1(x)). (11)

This follows by collecting each root's three products in(10). The sign of
the last difference is record0 minus record1, whereas Delta is record1
minus record0. Reversing those conventions would reverse the correction.

The accepted bounds 0<omega_i<11/36 and x<=R<1/4 give k_i>41/36>0.
Also k_i is decreasing in x, since
k_i'=-1+2theta*x*omega_i^2<0, and k_i(0)=2-2omega_i<2. Thus both factors
are positive. This does not determine the difference of their weighted
values. The exhaustive correction branches are

| Actual branch | Complete q expression | Correction sign only |
|---|---|---|
| chi_0<=0 and chi_1<=0 | T_core | zero |
| chi_0>0 and chi_1<=0 | T_core+gamma*sigma_0*k_0 | positive |
| chi_0<=0 and chi_1>0 | T_core-gamma*sigma_1*k_1 | negative |
| chi_0>0 and chi_1>0 | T_core+gamma*(sigma_0*k_0-sigma_1*k_1) | unresolved difference |

Equality chi_i=0 belongs to its zero branch. Each sigma_i and omega_i is
determined by the same actual p_i,c_i,f_i,g_(i,u) and theta. They cannot
be selected independently to make a row in this table favorable.

## Exact slope and the proved conditional region

Use Q(x)=q(x)(1-x)v>0 and RI145's exact polynomials a(x),b(x), so

    Q(x)*W(x,y)/r=a(x)+y*b(x).

With P(x)=(1+eta)(j+G_*x)>0, division of RI145 equation(23) by12xQ gives

    b(x)/(12xQ(x))
      = x*P(x)-lambda*j*U30(x)/((1-x)*v)
                -lambda*G_*x*U20(x)/q(x).              (12)

Every divisor is strictly positive on(4). Consequently b<=0 is exactly

    lambda*(G_*x*U20(x)/q(x)+j*U30(x)/((1-x)*v))
       >= x*(1+eta)*(G_*x+j).                           (13)

The q in(12)--(13) means precisely(10) or(11), and U20 means(8).
There is no cancellation that replaces q by a multiple of v, lambda or a
freely chosen component contrast.

The companion proves that

    T(x)=lambda*j*U30(x)/[x(1-x)P(x)]

is strictly decreasing on(0,R], with T(x) tending to infinity as x tends
to0. Its minimum is T_R in(1). If v<=T_R, the first two terms in(12)
sum to at most zero for every x. The last term is strictly negative,
because the complete actual q is positive and finite. Therefore b(x)<0
throughout the interval, even if v=T_R and x=R.

This estimate retains the full q contribution with its known sign; it
does not omit a negative canonical summand from the *denominator* or
replace that denominator. That is why the theorem holds with all four
canonical branches above, without deciding one of them.

The complete same-law bounds give

    T_R/B > 7957/891 > 8,
    v<=8B  implies  b(x)<0 for every 0<x<=R.             (14)

The companion proves the constants directly from V_0<1, R<12/95,
eta<1/32 and j+G_*R<1. On this sufficient regime it also gives the strict
normalized margin

    b(x)/(12xQ(x)) < -(829/7128)*x*P(x) < 0.             (15)

No value of the actual ratio v/B has been inferred. Equations(14)--(15)
are conditional same-law theorems, not a selected regime or actual W sign.

## Complementary regime and the remaining canonical comparison

Suppose instead that v>T_R. Strict monotonicity and the endpoint limits of
T give a unique formal crossover x_c in(0,R) with T(x_c)=v. This is an
implicit analytic point, not a numerically located or selectable scale.

Define the exact residual

    Delta_slope(x)=x*P(x)-lambda*j*U30(x)/((1-x)*v).

It is at most zero on(0,x_c] and strictly positive on(x_c,R]. Thus
b(x)<0 is already proved on the entire first interval. Only on the final
interval can a positive slope occur. There the exact remaining test is

    b(x)<=0 iff q(x)<=Q_upper(x),
    Q_upper(x)=lambda*G_*x*U20(x)/Delta_slope(x)>0.        (16)

Equality gives b=0; strict inequality gives b<0; a reversed strict
inequality gives b>0 at that formal x. These statements divide only by
the named strictly positive residual on its specified interval, never at
the crossover. At the crossover the retained q term still makes b<0.

Substitute the actual canonical expression rather than stopping at a
renamed q budget. The remaining selected-prefix comparison is

    gamma*(sigma_0*k_0(x)-sigma_1*k_1(x))
       <= Q_upper(x)-T_core(x),          x_c<x<=R,       (17)

with sigma_i=[41p_i-f_i/2-min(g_(i,0),g_(i,1))]_+/c_i,
omega_i=theta*p_i/e, and U20 in Q_upper given by(8). Thus both sides
depend on the same canonical/prefix data. In the double-zero branch it
reduces to T_core<=Q_upper. In each other branch the corresponding signed
term from the table remains; nonnegativity of N_i does not prove(17).
The complete known sign 0<q supplies its lower, not its required upper,
bound. No actual positive-part branch or comparison in(17) is decided here.

One further exact collection exposes the shared sigma_0 dependence on
the two sides. Define the algebraic part of(8) without its explicit N_0
terms by

    U_base(x)=3-x*[E_0+2+2(1-theta)h_0+(1-2theta)j]
       +x^2*[2m_0+2j+1-theta]
       +x^3*theta*(E_0-2m_0-3j).

Then, at the same unchanged law,

    U20(x)=U_base(x)+gamma*x*sigma_0*k_0(x).             (17a)

U_base is only a polynomial grouping, not a new parent law or probability;
no sign is asserted for it. On the interval where Delta_slope>0, multiply
(16) by that positive residual and insert(11),(17a). The complete
equivalent comparison is

    Delta_slope*T_core-lambda*G_*x*U_base
      +gamma*[(Delta_slope-lambda*G_*x^2)*sigma_0*k_0
               -Delta_slope*sigma_1*k_1] <= 0.         (17b)

All functions in(17b) are evaluated at the same x. No sign is assigned to
Delta_slope-lambda*G_*x^2. In particular the reference-root correction
cannot be enlarged on one side while being held fixed on the other;
(17b) preserves its simultaneous contribution to U20 and q. All four
positive-part branches still follow(6). This is an exact correlated form
of the remaining comparison, not an additional proved bound.

The genuinely additional information needed for unconditional endpoint
ordering is now delimited: either a selected-prefix bound placing v at
most T_R, or, if v>T_R, an upper estimate(17) on the *terminal interval*
after the unique crossover. The current manuscript proves a substantial
region and automatic initial interval before stating this remaining test.
It is not a theorem that no further analytic proof from the fixed data
exists, and it is not an arbitrary-coefficient counterexample.

## What endpoint ordering implies

Where b(x)<0, W(x,y) strictly decreases with y. Its larger endpoint value
on the positive-y interval is the unattained limit r*a(x)/Q(x) as y tends
to0. Proving W<=0 there still requires a(x)<=0. Conversely a(x)>0 gives
positive W for sufficiently small *formal* positive y by continuity; it
does not identify the actual y=s or x=rho.

There is a separate conditional intercept fact on the capacity-failure
side v<=B. Directly from RI145, without using slope ordering to infer it,

    a(R)/Q(R)=-1+12lambda*R*(G_*R/q(R)+j/((1-R)*v))>0.  (18)

Indeed the j term is at least1 because v<=B, and the q term is strictly
positive. Thus in that conditional regime full-domain W<=0 cannot hold:
formal positive-y points near the excluded lower endpoint at x=R have
W>0. This does not claim W(rho,s)>0, an actual C2/C3 sign, H30 feasibility
or a physical counterexample. Neither actual scale is chosen or changed.

Outside the proved uniform slope regime, the general two-endpoint criterion
from RI145 remains binding. In particular a favorable slope by itself
cannot certify the weighted obstruction or the original coupled system.

## Evidence and stopping boundary

The complete authenticated assignment, predecessor adjudication, root
review and independent recommendation were read. New literal mathematical
reads were the complete RI145 ENDPOINT_REDUCTION, RI151
COUPLED_EQUALITY_REDUCTION, RI155 CAPACITY_STRUCTURE and RI157
CANONICAL_CAP_BOUND. Their exact identities, alongside retained earlier
primary sources, are in the source manifests. The canonical substitution,
product signs, positive clearing, monotonic threshold, constants and
conditional intercept have been checked by manual algebra only.

No scientific body, vector, polynomial coefficient array or actual scale
was decoded or evaluated. Administrative hashes are not mathematical or
runtime acceptance. The frozen actual prefix, all prior proofs, reviews
and failures remain unchanged. This packet does not reuse RI172's varied
coefficient family as though it were the actual law.

Preserve P2/P3, numerical Y=1/4, all31/139/20/42, shared T1, other eight
parents, all five Di, strict endpoints and every labeled occurrence.
Actual capacity, joint q/v, global M5/M6/rho, W/C2/C3 and shared H30 remain
separate questions. RI170 measurement and RI171 qualification are separately
owned; RET alone stays paused. No new quantum, geometry, mass/gravity,
empirical or ontology claim is made. Root owns independent adjudication,
execution admission, the next justified assignment and repository/Git.
Stop at the sealed bounded handoff.
