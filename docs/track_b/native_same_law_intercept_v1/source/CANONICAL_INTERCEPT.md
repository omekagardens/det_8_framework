# RI175 canonical intercept and endpoint reduction

30 September 2026. Manual author proof, submitted for independent review.
The unchanged prefix and all inherited shared-system obligations remain fixed.

## Result and the load-bearing inherited premise

The normalized intercept

    I(x)=a(x)/Q(x)
        =-1+12lambda*[G_*x^2/q(x)+j_0*x/((1-x)*v)]     (1)

is strictly increasing for every 0<x<=R at the actual unchanged law.
This is stronger than a conditional sign region, but its evidential basis
must remain explicit: it uses the previously certified RI122 fixed-prefix
quadratic sign, not a new proof of that sign from general DET axioms.

RI122's final decision accepts a monic quadratic g with g(1)>0 and
g'(1)<0. The accepted RI127 sign review identifies the same pivot
Q2_1 as a strictly negative scalar multiple of g. RI145 defines
q=-Q2_1. Thus q=k*g for a fixed positive k. No coefficient, scale or
scientific certificate is decoded or evaluated here. The analytical step
from this accepted premise to monotonicity is new and proved below.

RI175_HISTORICAL_PREMISE_SCOPE.json explicitly permits literal use of that
final decision while keeping its inherited opaque provenance classification.
Its other operational references are not traversed. Provisional historical
review language alone is not being promoted into final acceptance.

Combining the new intercept result with the separately conditional RI173
slope theorem gives one exact endpoint criterion on that regime. The actual
membership in the slope regime and the endpoint comparison are still open.

## Fixed quantities and complete canonical quadratic

Retain RI145 and RI173's complete same-law domain and positive quantities:

    0<x<=R,       1/8<R<12/95<1/4,
    0<y<=1/d(x),       d(x)=2(3-2x+x^2),
    Q(x)=q(x)(1-x)v>0,
    G_*=theta^3*c_0>0,       j_0>71/72,
    0<lambda=1-(b_1/b_0)^3<1,       v=V_1-V_0>0,
    theta=1/[72(1+M5)],       0<theta<1/144.             (2)

The formal domain contains the unchanged actual pair (rho,s); it does not
make either scale selectable. y=0 is excluded and appears only as a limit.
R=1/[2(1+max(E_0,E_1))] is the accepted canonical cap, not M6 or rho.
All stem sums include S=0,1,3,7 and both separate H5 one-cap ideals.

The lower-prefix aliases retain their existing meanings. In particular
h_i=theta*c_i, m_i=theta^2*c_i and j_i=1-theta*K_i, where
K_i=sum_S B_i(S)^2/A(S)+2c_i. With
T_i=sum_S B_i(S)^3/A(S)^2, one has

    V_i=theta^3*T_i+2theta^2*c_i+j_i,
    v=theta^3*Delta T+2theta*Delta h+Delta j.            (3)

Delta throughout this note is record1 minus record0. The full RI151
canonical correction is

    gamma=35/1476,
    chi_i=41p_i-f_i/2-min(g_(i,0),g_(i,1)),
    sigma_i=[chi_i]_+/c_i,
    N_i=gamma*sigma_i,
    omega_i=44theta*p_i.                               (4)

Both zero and positive branches, equality chi_i=0 and tied minima remain.
This is an identity for the unchanged actual canonical law, not a choice
of nonnegative parameters. No sign of a contrast follows merely from
positivity of its entries.

Collecting RI145 equation29, with(4) fully substituted, gives exactly

    q(x)=q_0+q_1*x+q_2*x^2,

    q_0=v+(2-theta)*Delta h+(3-2theta)*Delta j
          -2gamma*Delta sigma+2gamma*Delta(sigma*omega),
    q_1=-2theta*Delta h-2Delta j+gamma*Delta sigma,
    q_2=-theta*v+theta^2*Delta h+theta*Delta j
          -theta*gamma*Delta(sigma*omega^2).            (5)

The subscripts in q_0,q_1,q_2 indicate polynomial powers, not record
indices. All three canonical products are retained. The last is a
difference of products, not the square of a contrast. Equation(3) also
gives the correlated identity

    q_2=-theta^4*Delta T-theta^2*Delta h
          -theta*gamma*Delta(sigma*omega^2),            (6)

without assigning a sign to any individual term. None of theta,M5,M6,
v,lambda,j_0,G_* or the canonical entries is tuned independently.

Equivalently, the previously checked same-law collection is

    q(x)=T_core(x)+gamma*[sigma_0*k_0(x)-sigma_1*k_1(x)],
    k_i(x)=2-x-2omega_i+theta*x^2*omega_i^2,
    T_core(x)=(1-theta*x^2)*v
       +(2-theta-2theta*x+theta^2*x^2)*Delta h
       +(3-2theta-2x+theta*x^2)*Delta j.                 (7)

Equations(5)--(7) describe the same polynomial whose historical sign is
used below. They do not replace it with a freely chosen quadratic.

## Exact derivative and retained dependence

Differentiate(1) only with respect to the formal variable x. The fixed
prefix values, global maxima and actual scales do not change. Since q>0
on the assigned domain, the quotient rule gives

    I'(x)/(12lambda)
       =G_*x*[2q(x)-x*q'(x)]/q(x)^2
          +j_0/[v(1-x)^2].                             (8)

For the exact quadratic in(5),

    H(x):=2q(x)-x*q'(x)=2q_0+q_1*x.                    (9)

The q_2 term cancels from this numerator algebraically. It remains in
the denominator q(x)^2 and in the actual correlated sign premise; it is
not discarded from the problem. Expanded in canonical data, the numerator is

    H(x)=2v+(4-2theta-2theta*x)*Delta h
       +(6-4theta-2x)*Delta j
       +gamma*[(x-4)*Delta sigma+4Delta(sigma*omega)].  (10)

No sign is assigned term by term in(10). In particular a positive-part
branch in(4) cannot be selected to force H positive, and the absent explicit
Delta(sigma*omega^2) in(10) does not erase its role in(8).

## Why the accepted historical polynomial is this q

The source linkage is mathematical, not inferred from similarly named files:

1. RI122's complete native family has Q2_1=c*g, where g is monic
   quadratic and the scalar c is strictly negative. The complete native
   reconstruction and final decision, not a synthetic fixture, are the
   historical source of this fact.
2. RI127's independently reviewed native-pivot sign theorem explicitly
   reuses that accepted Q2_1=-k*g relation, with k=-c>0, on the same
   unchanged baseline. Its section5 establishes this linkage and section8
   explicitly records q(0)>0 from the accepted quadratic evidence.
3. RI145 equation4 fixes q=-Q2_1 for the weighted identity. Its equation29
   is the complete held/canonical expression expanded in(5).
4. RI151's canonical formula and RI173's substitution are identities at
   that same prefix. Neither changes the underlying law. RI172's varied
   finite-layer family is not used at any point in this argument.

RI122_ROOT_FINAL_ADJUDICATION.json states mathematical_result_accepted:true
and explicitly accepts g(1)>0, g'(1)<0 and 0<R<1. The current narrow
scope authority permits using that historical finite result. Its physical
and all-size limits remain unchanged. We neither recalculate its rational
coefficients nor treat its old operational authority as current permission.

Write g(x)=alpha+beta*x+x^2 merely as symbolic notation. Because R<1,

    g'(x)=beta+2x <= beta+2=g'(1)<0
           for 0<=x<=R.

Positive multiplication by the same fixed k gives

    q'(x)<0,       q(x)>0,       q_0=q(0)>0.            (11)

The positivity is also already accepted on(0,R]. It can independently be
deduced from these historical signs because g decreases on[0,1] and
g(1)>0. This does not make x=1 an allowed growth scale: it is solely a
polynomial comparison point of the inherited finite proof.

Thus H=2q-xq'>2q>0 for x>0. Equation(8) proves the strict actual-law result

    I'(x)>12lambda*j_0/[v(1-x)^2]>0,
                    0<x<=R.                           (12)

This conclusion is unconditional with respect to the RI173 slope regime
v<=T_R, but is conditional on the stated accepted fixed-prefix premises.
It is not a theorem for every hypothetical DET prefix or every positive
quadratic. The historically certified sign is not renamed a new general
analytic consequence of the canonical positive-part formula alone.

For clarity, the correlated coefficient information now available is
q_2=k>0, q_1+2q_2=k*g'(1)<0 and
q_0+q_1+q_2=k*g(1)>0. These are inherited finite sign consequences on
the complete expressions(5), not independently chosen coefficient signs.
They exclude the adverse derivative regime without assigning signs to
Delta h,Delta j or individual canonical products.

## Lower-end degeneracies without illegal division

Although the actual accepted q_0 is strictly positive, the derivative
identity must not silently divide by it. For any retained positive
quadratic on(0,R], continuity first gives q_0>=0. The exhaustive
zero-constant cases are:

| Lower-end case | Consequence of q>0 | Derivative of x^2/q | Limit of I at zero |
| --- | --- | --- | --- |
| q_0=0, q_1>0 | q_1+q_2*x>0 on the domain | q_1/(q_1+q_2*x)^2>0 | -1 |
| q_0=q_1=0 | q_2>0 | 0 | -1+12lambda*G_*/q_2 |

q_0=0,q_1<0 would make q negative for sufficiently small positive x
and is impossible. In both displayed cases the remaining j_0 term in(8)
is strictly positive, so I still strictly increases. The double-zero
case cannot be assigned limit -1. No division by q_0 or q_1 was made
before its branch was fixed. These are general zero-safe audits, not
claims that either branch occurs in the historically accepted prefix.

At the actual law, q_0>0 and therefore I(x) tends to -1 as x tends to0.
Strict monotonicity gives three exact possibilities: I(R)<0 means the
intercept is negative throughout; I(R)=0 means it is negative before R
and zero at R; I(R)>0 gives exactly one formal zero x_I in(0,R).
This is an existence/uniqueness statement, not a numerical root location
or an assertion about whether actual rho is above or below it.

## Endpoint implication with the separate slope hypothesis

RI145 gives W/r=I(x)+y*b(x)/Q(x). The new theorem alone proves

    a(x)<=0 for every 0<x<=R  iff  I(R)<=0.             (13)

It says nothing by itself about the upper-y endpoint when b is positive.
Now additionally assume RI173's proved sufficient slope condition v<=T_R
(in particular v<=8B suffices). Then b(x)<0 on the full x interval and

    W(x,y)<=0 for every allowed (x,y)
       iff I(R)<=0.                                   (14)

For sufficiency, I(x)<=I(R)<=0 and y*b/Q<0 actually give W<0 at every
allowed positive-y point, including x=R when I(R)=0. For necessity,
if I(R)>0, continuity in y gives W(R,y)>0 at sufficiently small allowed
positive y. The limit y=0 need not be included or physically selectable.

The endpoint comparison itself can be written without ambiguous clearing:

    I(R)=-1+12lambda*G_*R^2/q(R)+B/v,
    B=12lambda*j_0*R/(1-R)>0.                          (15)

Since the q term is strictly positive, I(R)<=0 requires v>B strictly.
For v>B, multiply only by positive quantities to obtain the exact iff

    I(R)<=0
       iff q(R)>=12lambda*G_*R^2*v/(v-B).              (16)

Consequently, within the separately assumed v<=T_R regime, the full-domain
weighted criterion is precisely v>B together with(16). Equality in(16)
is retained and gives I(R)=0, with W still strictly negative for y>0.
Neither comparison has been evaluated or proved for the actual prefix.
For v<=B the intercept at R is strictly positive, consistently with
RI173's separately derived formal-domain failure on that regime.

Without v<=T_R, equation(13) still reduces the intercept requirement to R,
but RI145's other endpoint a_+=d*a+b remains a separate requirement.
Nothing here selects rho or s, proves actual W/C2/C3 signs, supplies a
simultaneous H30 tuple or turns the weighted necessary question into
sufficient full-system feasibility.

## Reading and stopping boundary

The assignment, current predecessor decision, root review and historical
scope authority were authenticated and read completely. Fresh complete
primary reads covered RI145 ENDPOINT_REDUCTION, RI151
COUPLED_EQUALITY_REDUCTION, RI127 INDEPENDENT_PROOF_REVIEW, both named
RI122 literal reviews, and the explicitly permitted final RI122 decision.
The companion [INTERCEPT_REGION.md](INTERCEPT_REGION.md) supplies the
parallel derivative and endpoint proof. Exact paths and pins, the narrow
historical-read exception and genuine diagnostics are retained in the
provenance manifests and author record.

This uses an accepted finite native sign theorem as a premise; it is not
a new scientific execution, new coefficient reconstruction or purely
axiomatic QM/geometry derivation. All predecessor evidence remains immutable.
No numerical/symbolic engine, scientific JSON/vector decode, source/helper
import, compile, AST, probe, fixture, runtime capture, new agent or
repository/index/Git mutation was used. RET stays paused; measurement and
supervisor repair stay separately owned. Preserve P2/P3,Y=1/4,
31/139/20/42,shared T1,other eight parents,five Di,strict endpoints and
every labeled occurrence. Root owns independent adjudication and any
successor or publication. Stop at the sealed bounded handoff.
