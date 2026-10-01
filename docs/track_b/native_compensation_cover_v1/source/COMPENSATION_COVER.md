# Complete support restricted compensation criterion

1 October 2026, Honolulu. RI254 manual author result pending independent review.

The joint eta/xi/sigma direction reduces exactly to a four-row,
support-restricted covering problem. Its primary prices include the
complete Q and P_nu losses, not just the released companion capacity.
After normalization those prices are 15/14 for eta coverage and 3/7
for each xi coverage. A cover costing at most one gives a forbidden
primary-or-equal-primary lexicographic descent when kappa_i>0.

PIECEWISE_REDUCTION.md eliminates the two eta/xi blocks and proves
a finite test with at most five sigma candidate values. No actual
canonical support, tight set, lower coefficients or C_b is evaluated.

## Fixed sector and distinct coordinates

Keep the original canonical problem alpha>=0, A alpha<=1, its full
actual-history objective Phi and complete sequential lexicographic
selector. Fix i in {0,1} and abbreviate only existing lower probabilities

    p=p_i>0, v=v_i>0, h_l=h_(i,l)>0,
    n_l=n_(i,l)>0, s_lm=s_(i,l,m)>0, a0=41/352.

For epsilon>0 and finite nonnegative rates a_l,b_lm,c, change only

    Delta tau_i=epsilon,
    Delta kappa_i=-(v/a0)epsilon,
    Delta eta_(i,l)=-a_l epsilon,
    Delta xi_(i,l,m)=-b_lm epsilon,
    Delta sigma_i=-c epsilon.                           (C1)

The rates a_l,b_lm,c are NOT the inherited seed or normalized-system
parameters with similar names. All other original coordinates remain
fixed. Rates on zero decreasing allocations must be zero.

RI248's complete terminal-incidence proof distinguishes kappa, tau,
eta, xi and sigma. Eta and xi retain their compulsory ordered minimum
marks, and xi also retains the join-top mark; their terminals distinguish
the two minima. Different compulsory assignments within those families
are not merged. The sigma and tau root bits are retained too. Distinct
terminal types separate the families, including the original nu family.
Thus no named increase and decrease secretly refer to one coordinate.

The complete companion mass and slack are

    C_lm=p tau_i+h_l eta_(i,l)+n_l xi_(i,l,m)+s_lm sigma_i,
    S_lm=1-C_lm>=0.                                     (C2)

Each (l,m) row represents all four original (j,t) assignments. Their
coefficients and slack agree by the admitted transports, but their
history contributions remain. Write

    T={(l,m):S_lm=0},    T_l={m:(l,m) in T}.             (C3)

T counts distinct coefficient rows, not raw records; its size is at
most four. No originally slack row is removed from finite feasibility.

## Complete incidence and a finite feasible step

The accepted full incidence gives

    Delta C_P=0,
    Delta C_Y=-v epsilon/(64 a0),
    Delta C_Ptau(l,m)=[p-h_l a_l-n_l b_lm-s_lm c]epsilon,
    Delta C_Q(i,l,other marks)=-v a_l epsilon,
    Delta C_Pnu(i,l,m,other marks)=-v b_lm epsilon,
    Delta C_V5(b,d,other marks)
       =-(v/40)c epsilon[1_(b=i)+1_(d=i)].               (C4)

All other original rows, including P_mu, are unchanged. P cancels
exactly. In P_nu the original nu contribution stays fixed; every Q,
P_nu and V5 residual is the complete unchanged original residual.
Both V5 singleton occurrences count, including two when b=d=i.

For a positive step kappa_i must be positive. The other coordinate
conditions are exactly the stated support restrictions. On each tight
row (C4) requires

    h_l a_l+n_l b_lm+s_lm c >= p,   (l,m) in T.          (C5)

Let D_lm=p-h_l a_l-n_l b_lm-s_lm c. The complete upper step bounds are

    epsilon<=a0 kappa_i/v;
    epsilon<=eta_(i,l)/a_l for every a_l>0;
    epsilon<=xi_(i,l,m)/b_lm for every b_lm>0;
    epsilon<=sigma_i/c when c>0;
    epsilon<=S_lm/D_lm for every slack row with D_lm>0.   (C6)

Support makes every applicable coordinate bound positive, and each
included slack ratio has positive numerator and denominator. The
finite minimum is positive. Taking epsilon at most that minimum
satisfies every original row and coordinate. Tight rows with zero
slope stay tight, negative slopes relax, and slack rows with nonpositive
slope need no new bound. Repeated marked rows are all included.

Conversely a positive slope at a tight row or a decreasing zero
coordinate forbids every positive epsilon. Hence support, positive
kappa and (C5) are necessary and sufficient for a local positive step
in this family. Endpoint equality is allowed in the closed canonical
problem; the unchanged strict-restoration law is not replaced by a
boundary canonical vector.

## Derive the other parent weights by hand

RI252 established w_N(i,j,l,m)=1/384 for the rigid four-event parent
N: r<a, r<x, o<x. It also established

    Pi_tau(i,j,l,m,t)=7v/3840,
    W=Pi_tau,i=7v/240,
    bar_s=(s_00+s_01+s_10+s_11)/4.                       (C7)

Keep the two other parents and a newborn z with bit k:

    Q: r<a<z, o<z, r<x, o<x;
    P_nu: r<a, r<x, o<x, a<z, x<z.

Q has eight linear extensions. If r is first, choosing a second
leaves o then x,z in two orders, while choosing o second leaves
a,x,z with a<z in three orders: five in total. If o is first,
r is forced next and the same a<z triple has three orders.
P_nu has a unique final z, and its remaining N has five extensions.

Both parents are rigid. In Q the minima have different descendant
counts and the maxima have different past sizes. In P_nu the unique
top is fixed and its N suborder is rigid. Thus there is no automorphism
divisor. Complete prefix diamonds equate the full marked path products
across each parent's linear extensions, retaining all newborn factors.

Deleting the selected final z leaves N. Its birth probabilities are
h_l for Q and n_l for P_nu, by the accepted lower diamonds. Therefore
for EVERY full marking, not just a selected representative,

    Pi_Q(i,j,l,m,k)=(8/5)(h_l/2)w_N=h_l/480,
    Pi_Pnu(i,j,l,m,k)=(5/5)(n_l/2)w_N=n_l/768.           (C8)

Summing all eight (j,m,k) assignments at fixed i,l gives
Pi_Q,i,l=h_l/60. Summing all four (j,k) assignments at fixed i,l,m
gives Pi_Pnu,i,l,m=n_l/192. Both newborn bits are retained.

The companion totals needed for those same coordinates are

    Pi_tau,i,l=7v/480,
    Pi_tau,i,l,m=7v/960.                                (C9)

These are actual history sums, not substitutes of uniform counts.

## Exact compensation prices and primary cost

RI248's complete objective includes the full P, P_tau, Q and P_nu
terms. P cancels; Y and V5 have zero full defect increment but retain
their constraints. The primary price per unit decreasing rate is

    A_l=h_l Pi_tau,i,l+v Pi_Q,i,l
       =7v h_l/480+v h_l/60=v h_l/32,

    B_lm=n_l Pi_tau,i,l,m+v Pi_Pnu,i,l,m
        =7v n_l/960+v n_l/192=v n_l/80,

    C_sigma=sum_(all carrying records)Pi_tau s_lm
           =W bar_s.                                   (C10)

Thus the EXACT finite objective change is

    Delta Phi=epsilon[-pW+sum_l A_l a_l
                             +sum_lm B_lm b_lm+C_sigma c]. (C11)

All prices are strictly positive. In particular Q and P_nu supply
positive losses when eta and xi decrease; ignoring them would change
the criterion.

Introduce dimensionless COVER AMOUNTS, not new law coordinates,

    x_l=h_l a_l/p,   y_lm=n_l b_lm/p,   lambda=c/p.       (C12)

Positive p,h_l,n_l make this a bijection with the finite nonnegative
rates, subject to the same zero-support restrictions. Dividing the
cost by epsilon pW yields

    Delta Phi/(epsilon pW)=J(x,y,lambda)-1,
    J=(15/14)sum_l x_l+(3/7)sum_lm y_lm+bar_s lambda.    (C13)

The tight-row cover is simply

    x_l+y_lm+s_lm lambda>=1,  (l,m) in T.                (C14)

The fractions in (C13) follow from the actual weights:
A_l/(W h_l)=15/14 and B_lm/(W n_l)=3/7.
They are derived identities, not acquired canonical coefficients.

Define support indicators only from the unknown ACTUAL allocations:

    E_l: eta_(i,l)>0;
    X_lm: xi_(i,l,m)>0;
    G: sigma_i>0.                                       (C15)

When E_l is false force x_l=0; when X_lm is false force y_lm=0;
when G is false force lambda=0. Magnitudes of positive allocations
enter (C6), not these finite-rate cover restrictions. No support
indicator is evaluated here.

## Attainment and the exact family criterion

Let F be the nonnegative finite vectors (x,y,lambda) satisfying
(C14) and (C15). If F is empty define M=+infinity.

If F is nonempty, choose any one finite feasible vector with cost K.
The portion of F with J<=K is nonempty and closed. Strictly positive
prices in (C13) bound every allowed coordinate, so this portion is
compact. The linear cost therefore attains a finite minimum M there.
This proves existence BEFORE using a minimum; no optimizer is run.
For an empty tight set, the all-zero vector gives M=0.

Tau is the ONLY increasing coordinate. Kappa strictly decreases and
its accepted original component key precedes tau. Every other changed
coordinate also decreases, and the components are distinct. Hence the
earliest changed coordinate is negative, whether it is kappa or an
earlier compensator. A feasible exact primary tie is therefore an
original lexicographic descent. No eta/xi key catalogue is required.

Consequently, for the specified entire nonnegative family,

    a primary-or-equal-primary lex descent exists
       iff kappa_i>0 and M<=1;                           (C16)

    a strict primary descent exists
       iff kappa_i>0 and M<1.                            (C17)

Attainment matters at M=1: it supplies finite rates and then a positive
epsilon from (C6), not merely a limiting direction. If M>1 or F is
empty, this family has no descent. If kappa_i=0, its required decrease
makes every positive step infeasible regardless of M.

At the ACTUAL canonical point the new necessary obstruction is

    kappa_i>0 => M>1, with +infinity allowed.             (C18)

This is a complete local-family criterion, not a criterion for global
optimality or for the full normalized system.

## Remaining premises and full retention

The next note gives a complete finite piecewise-linear formula for M
and explicit support/tight-set consequences. Actual support, T and
the four s-values remain unknown. No magnitude bound on positive
kappa, comparison between root sectors or sign of C_b follows without
additional same-law evidence about them.

Retain all ten unknowns u0,u3,U4,...,U11, u2=-1, all five complete
disconnected and eight connected equations, actual canonical offsets
and complete recovery in admitted RI248 CANONICAL_BINDING.md section 7.
No forced-zero consequence removes a coordinate or equation. The
accepted d=0!=d7 and normalized existence iff actual C_b=0 remain.
All whole records, labeled ideals, both newborns, strict endpoints,
fifteen boundary objects and the 423-source by-reference manifest remain.

RI250's GAP-INDEX and any needed absent-entry rule remain; all original
literal exceptions are closed. No new body/hash/checker, coefficient
acquisition, scientific JSON, engine, reconstruction, subject execution,
measurement/RET, repository/Git/index, publication or successor work
is authorized. Stop for independent root adjudication.
