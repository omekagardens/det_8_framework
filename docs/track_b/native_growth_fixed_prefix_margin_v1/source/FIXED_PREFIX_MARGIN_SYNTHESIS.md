# Fixed prefix bounds and the joint margin threshold

The new result has three parts: tighter weighting bounds from complete
prefix normalization; an endpoint theorem for a nonnegative singleton
contribution; and an exact expression for the quantitative q floor needed
by BOTH retained joint budgets. These turn the unresolved comparison into
explicit conditions on the same fixed prefix. They do not establish that
those conditions hold at that prefix.

RI151's canonical coefficient formula is now an accepted premise. This
note does not repeat its optimization proof or replace its fixed inputs.
PREFIX_STRUCTURE.md proves the new smaller-component and full-complement
identities. WEIGHTED_PREFIX_COMPARISON.md proves the weighted ratio and
endpoint results. All three notes are manual author work awaiting fresh
independent review, not numerical evaluation or execution admission.

## What the prefix now controls

Retain the accepted notation

    L_i=41p_i,  G_i=min(g_i0,g_i1),
    H_i=L_i-f_i/2-G_i,  sigma_i=[H_i]_+/c_i,
    C_sigma=35/1476,
    q(x)=T_core(x)+C_sigma S(x),
    S(x)=sigma_0 k_0(x)-sigma_1 k_1(x),
    k_i(x)=2-x-2omega_i+theta x^2 omega_i^2,
    omega_i=44theta p_i.                                (1)

The p,c,f,g entries are the unchanged size-four prefix probabilities
defined in RI151. In particular c_i is the complete C4 full probability,
not an independently selectable denominator. Theta is the unchanged
strict-restoration coefficient. The sigma positive parts encode the
actual canonical boundary coefficients; N_i=C_sigma sigma_i is their
actual singleton correction, not the whole proper probability.

Complete Q4 normalization gives L_i+f_i+g_iu<1 because the other three
proper entries and the genuine full complement are strictly positive.
Consequently

    0<p_i<1/41,
    0<omega_i<44theta/41<11/1476.                       (2)

The final inequality uses the already accepted theta<1/144. No numerical
probability or maximum is calculated. This is materially sharper than
using only p_i<1. For every x in the same actual-containing [0,Z],
where 0<Z<1/4,

    k_i'(x)=-1+2theta x omega_i^2<0,
    k_i(Z)<=k_i(x)<=k_i(0),
    k_i(x)>2-Z-88theta/41>2561/1476.                   (3)

The last constant also holds on the larger closed [0,1/4]. Every bound
is strict as shown, although a non-strict version is safe in a floor.

The structural note proves more than this bound. Its new root-only J3
component result means that in the complete Q4 row only g_iu and its
full complement t_iu can vary with the distinguished atom bit. With
the other entries combined as a fixed root-dependent sum B_i,

    g_iu+t_iu=1-L_i-f_i-B_i,
    g_i0-g_i1=t_i1-t_i0,
    H_i=2L_i+f_i/2+B_i+max(t_i0,t_i1)-1.               (4)

B_i here denotes the Q4 sum J0+J1+J3, not the earlier complete C4 row
also denoted B in inherited notes. Formula (4) uses the actual full
complement, not a free slack. The square-parent remainder identity and
its strict upper bounds on g are retained in the companion proof.
Thus the unknown positive-part branch is now exactly a comparison of
the complete fixed prefix row with a stated threshold. No branch or
root ordering follows merely from positivity of its individual entries.

## Nonnegative singleton floors need only two endpoints

The weighted comparison proof establishes the following theorem for
the actual fixed sigma_i>=0 and omega_i satisfying (2): for any m>=0,

    S(x)>=m for every x in [0,Z]
      if and only if S(0)>=m and S(Z)>=m.                (5)

The endpoints are the explicit prefix expressions

    S(0)=2[sigma_0(1-omega_0)-sigma_1(1-omega_1)],
    S(Z)=sigma_0[2-Z-2omega_0+theta Z^2 omega_0^2]
          -sigma_1[2-Z-2omega_1+theta Z^2 omega_1^2].    (6)

The restriction m>=0 is essential. For omega_0>=omega_1, the ratio
k_1/k_0 is nondecreasing; a nonnegative floor at Z therefore bounds S
throughout the interval. For omega_0<=omega_1 and sigma_0<=sigma_1,
S is concave, so its minimum lies at an endpoint. If instead sigma_0>
sigma_1, its derivative is strictly negative under (2), so Z is minimal.
These cases include equality and zero sigma values without dividing by
a sigma or a contrast. The companion gives the complete factorization.

For a floor that may be negative, three valid comparisons remain:

    K_box = k_0(Z)sigma_0-k_1(0)sigma_1,
    R_max = max_{x in [0,Z]} k_1(x)/k_0(x),
    D = sigma_0-R_max sigma_1,
    K_ratio = k_0(Z)[D]_+-k_0(0)[-D]_+,
    K_other = (k_1(Z)/R_max)[D]_+
                -(k_1(0)/R_max)[-D]_+.                (7)

R_max is an endpoint ratio: it is the ratio at Z if p_0>=p_1, and at
0 otherwise. This is a proved case distinction, not a selection of
the actual root ordering. The ratio floor follows by factoring S as
k_0(x)[sigma_0-(k_1/k_0)(x)sigma_1] and retaining the sign of D.
The other anchor follows from
S(x)=k_1(x)[sigma_0/R(x)-sigma_1]>=k_1(x)D/R_max.

Let K_end=min(S(0),S(Z)). Define a certified uniform floor K by taking
max(K_box,K_ratio,K_other), and also including K_end in that maximum only when
K_end>=0. Equations (5)-(7) then prove S(x)>=K on [0,Z]. A negative
K_end is NOT used as a uniform lower bound. The stronger constant
bound from (3) may also be included, but is unnecessary for this definition.

K_box alone strictly improves the RI151 separated bound
(41/36)sigma_0-2sigma_1 whenever either sigma is nonzero: k_0(Z)>41/36
and k_1(0)<2. The ratio floor preserves additional correlation between
the factors; it is not claimed always to exceed K_box. Taking their
maximum never weakens a proved floor. This is a strict strengthening of
the lower-bound expression, not a claim that the strengthened expression
passes the required threshold at the actual prefix.

## The exact amount required by both joint budgets

Keep every definition from RI147 at the SAME correlated actual law:

    r=r3_0>0, lambda=D3/r>0, eta=epsilon3/r>0,
    g=theta^3 c_0>0, j=j_0>0, v=V_1-V_0>0,
    Y=1/d(Z), u_2=U20(Z), u_3=U30(Z).

Here g is the inherited aggregate, not either g_iu; v is the sensitivity
contrast, not a fork full probability. The accepted bounds ensure
0<Z<1/4 and 1-Yu_2>0, 1-Yu_3>0. Set

    A=12lambda g Z^2>0,
    B=12lambda j Z/(1-Z)>0,
    E=12 Z^2(1+eta)(j+gZ)>0,
    mu=min_{x in [0,Z]} q(x)>0,
    C_0=1-B/v,
    C_1=1-(1-Yu_3)B/v-YE.                              (8)

The two original sufficient envelope budgets are precisely

    A/mu+B/v<=1,
    (1-Yu_2)A/mu+(1-Yu_3)B/v+YE<=1.                  (9)

Since A/mu>0 and 1-Yu_2>0, (9) forces C_0>0 and C_1>0.
If either is nonpositive, no finite positive mu can pass this particular
envelope. That fact does not determine the actual W sign and does not
rule out a direct proof with the exact cleared endpoint polynomials.

When both capacities are positive, positive division gives the exact
equivalence

    both inequalities (9)
       iff mu>=Q_req,
    Q_req=A max{1/C_0,(1-Yu_2)/C_1}>0.                 (10)

This is not two separately adequate but jointly insufficient bounds.
The maximum is exactly what satisfies both inequalities simultaneously.
The required uniform ratio floor is Q_req/D3, not an arbitrary positive
number. The separate v comparison cannot disappear: the positive-capacity
condition in (10) is itself equivalent to

    YE<1,
    v>B max{1,(1-Yu_3)/(1-YE)}.                       (11)

To prove this, C_1>0 forces 1-YE>0 because B/v>0 and 1-Yu_3>0;
then divide by the positive factors. Conversely (11) gives both capacities
strictly positive. These are necessary conditions for this envelope,
not claimed necessary conditions for the underlying weighted obstruction.

## A stronger sufficient prefix comparison

Let m_T be the exact minimum of T_core on [0,Z], and let K be the
proved singleton floor above. Then

    mu >= Q_cert := m_T+C_sigma K.                      (12)

There is no assumption that the minima of the two summands occur at the
same x: a sum of separate lower bounds is sufficient without that claim.
It can be conservative. Combining (10)-(12) gives the explicit sufficient
prefix condition

    C_0>0, C_1>0, and m_T+C_sigma K >= Q_req.            (13)

This supplies an adequate uniform q/D3 floor, namely Q_req/D3, IF the
displayed fixed-prefix comparison is proved. It also satisfies both
joint budgets, rather than treating each as a separate later guess.
The improved K never weakens the analogous RI151 separated-factor test.
It strictly raises its q lower-bound side when at least one sigma is
nonzero. We have not established (11) or (13) for the unchanged prefix.

A particularly compact sufficient test uses only two singleton endpoints.
Under the positive capacities, put

    m_req=max{0,(Q_req-m_T)/C_sigma}.

If S(0)>=m_req and S(Z)>=m_req, theorem (5) implies (13). This test
may leave unused negative-singleton compensation when m_T>Q_req. In that
case use (12)-(13) or the exact joint-polynomial test below; do not apply
the nonnegative endpoint theorem to a negative proposed floor.

All appearances of Z, Y, u_j, g, j, v, theta, m_T and sigma come from
the same fixed-law substitutions. In particular N_i=C_sigma sigma_i
must also be used in the C5 full complement, its parent-wise scale cap
and the reference sums. Holding an old favorable Z while replacing N_i
would invalidate this comparison. The numerical certificate's original
Y=1/4 domain is not replaced by this analytic envelope's Y=1/d(Z).

## Exact polynomial alternative and the proved remaining relation

For an explicit source-level representation of m_T, write
T_core(x)=t_0+t_1 x+t_2 x^2. With the accepted C4 contrasts
d_S=B_0(S)-B_1(S), P_S=(B_0(S)+B_1(S))/A(S), and
T_S=(B_0(S)^2+B_0(S)B_1(S)+B_1(S)^2)/A(S)^2,

    t_0=theta sum_S d_S[(4-2theta)P_S-theta^2 T_S+5theta-6],
    t_1=theta sum_S d_S[4-2theta-2P_S],
    t_2=theta sum_S d_S[theta^3 T_S-theta^2].            (14)

The sum is over all four stem ideals0,1,3,7; d_0=0 is an exact contrast
identity, not an omitted probability. The earlier symbol A(S) is the
complete C3 row and is distinct from the envelope A in (8).

If t_2>0 and 0<-t_1/(2t_2)<Z, m_T=t_0-t_1^2/(4t_2).
Otherwise m_T=min{t_0,T_core(Z)}. This is a manual quadratic identity
including linear, constant and endpoint cases, not an evaluated minimum.

One can avoid the separate-minimum loss in (12). Write q(x)=q_0+q_1x+q_2x^2:

    q_0=t_0+2C_sigma[sigma_0(1-omega_0)-sigma_1(1-omega_1)],
    q_1=t_1-C_sigma(sigma_0-sigma_1),
    q_2=t_2+C_sigma theta(sigma_0 omega_0^2-sigma_1 omega_1^2).
                                                               (15)

The accepted actual q_2>0 remains a premise; no new numerical sign test
is performed. With C_0,C_1>0, the exact uniform comparison in (10) is
equivalent to the following fixed-prefix conditions:

    q_0>=Q_req,
    q_0+q_1 Z+q_2 Z^2>=Q_req,
    and, if -2q_2 Z<q_1<0,
        4q_2(q_0-Q_req)-q_1^2>=0.                      (16)

Indeed the convex quadratic has its minimum at an endpoint unless its
vertex lies strictly inside; the last inequality is its positively
cleared vertex value. Vertex-at-endpoint equality is already covered by
the first two lines. Unlike (5), this tests the whole q polynomial and
therefore remains valid with a negative singleton contribution or an
interior minimum. It keeps core/singleton correlations at the same x.

Equations (11) and (16) now isolate the precise remaining prefix relation
equivalent to success of BOTH old envelope budgets. Equation (13) or
the nonnegative endpoint test supplies an explicit sufficient route.
No actual positive-part branch, prefix root ordering, capacity sign, or
inequality in (13)/(16) has been established here. The normalization and
remainder identities restrict these expressions but are not themselves
the missing quantitative dominance proof. We do not assert that the
fixed prefix fails, nor offer freely chosen probabilities as its proxy.

## Preserved scope

The new yield is structural prefix identities, improved strict factor
bounds, an endpoint theorem, and an exact joint-budget threshold with
the remaining prefix conditions proved necessary and sufficient FOR
THAT ENVELOPE. A failed sufficient test would not prove positive W.
A passed one would establish W<=0 on its actual-containing domain,
exclude simultaneous strict positivity of C2 and C3, and therefore
obstruct this fixed H30 candidate. It would not construct a positive
continuation or settle other candidate families. No such pass is proved.

Actual rho membership in the earlier small-x obstruction interval,
the individual connected margins, the same shared T1 recovery, the
other eight connected parents and all five Di systems remain binding.
P2/P3, numerical Y=1/4, all31/139/20/42 obligations, complete records,
individual ideal multiplicities and strict endpoints are unchanged.
Canonical tightness and positive actual strict restoration are never
identified. RET stays paused and measurement remains separate.

All retained arguments are manual and source-only. The structural note
discloses one withdrawn seed-order comparison proposed during author
coordination; it supplies no premise or sign to this proof. No actual
numerical coefficient/probability/history/maximum/scale/H/z value was
computed or substituted. No scientific-body decoding, engine,
global graph enumeration, source/helper import,
compile, AST, probe or run, runtime/controller/card/admission, repository/
index/Git or predecessor mutation occurred. Exact literal premises and
author diagnostics are bound by the manifests and final handoff.
No physical QM, geometry, gravity, all-size or empirical result is
promoted. Stop for independent review and root adjudication; this note
assigns no successor.
