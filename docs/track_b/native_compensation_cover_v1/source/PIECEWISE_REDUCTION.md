# Exact finite elimination of the compensation cover

1 October 2026, Honolulu. RI254 manual author result pending independent review.

The normalized covering minimum from COMPENSATION_COVER.md can be
computed symbolically from at most five sigma candidates, with all
support cases and ties retained. This is a proved finite reduction,
not numerical sampling, a solver run or an evaluation of the actual
canonical allocations.

Keep its notation: T is the tight subset of the four (l,m) coefficient
rows, E_l denotes available eta, X_lm available xi, G available sigma,
and s_lm>0. The actual mean bar_s is over ALL four s-values, including
slack rows. The normalized cost is

    J=(15/14)sum x_l+(3/7)sum y_lm+bar_s lambda,
    x_l+y_lm+s_lm lambda>=1 on T.                        (P1)

Unavailable coordinates are fixed to zero. Availability means strictly
positive actual canonical allocation, not a guessed or acquired value.

## Eliminate xi and eta at fixed sigma

For a fixed permitted lambda>=0 define

    r_lm(lambda)=(1-s_lm lambda)_+,
    A_l={m in T_l:X_lm is available},
    B_l=T_l minus A_l,
    R_l(lambda)=max_(m in B_l) r_lm(lambda),              (P2)

where the maximum of the empty set is defined as zero here. No rate
y on a non-tight row is needed at a minimum: it covers no constraint
and has strictly positive cost. All originally slack rows remain in
the original finite epsilon bounds.

If eta is unavailable in block l, x_l=0. This block is feasible exactly
when r_lm=0 for every m in B_l. On that domain its unique least-cost
choice and price are

    y_lm=r_lm for m in A_l,
    psi_l(lambda)=(3/7)sum_(m in A_l)r_lm.               (P3)

All other y rates in that block are zero.

If eta is available, every missing-xi row forces x_l>=R_l. For any
such x_l, the least-cost available xi choices are

    y_lm=(r_lm-x_l)_+,   m in A_l.

Its block objective is

    (15/14)x_l+(3/7)sum_(m in A_l)(r_lm-x_l)_+.          (P4)

Increasing x_l by any positive amount can save at most two xi amounts
of that size. Its cost therefore rises by at least

    [15/14-2(3/7)] times that amount
       =(3/14) times that amount >0.

The exact block minimum is consequently attained at

    x_l=R_l,
    y_lm=(r_lm-R_l)_+ for m in A_l,
    psi_l(lambda)=(15/14)R_l
                    +(3/7)sum_(m in A_l)(r_lm-R_l)_+.   (P5)

This proves the whole two-by-two block elimination, including zero,
one or two tight rows. An eta allocation is used only to meet rows
whose xi is unavailable. If every tight xi in that block is available,
R_l=0 and optimal eta usage is zero, even if eta itself is positive.

All reconstructed rates are finite and supported. Multiplying back
by p/h_l, p/n_l and p gives the original rates a_l,b_lm,c. The finite
epsilon construction in COMPENSATION_COVER.md then enforces every
original constraint, not just the cover.

## Exact sigma feasibility domain

Let U be the tight rows with neither eta nor their own xi available:

    U={(l,m) in T:not E_l and not X_lm}.

Define

    L=max_(U)(1/s_lm), with L=0 if U is empty;
    H=max_(T)(1/s_lm), with H=0 if T is empty.           (P6)

Both are finite, and L<=H. Rows in U must be covered by sigma alone;
these are exactly the feasibility restrictions omitted from (P5).

If sigma is available, feasible sigma values are exactly lambda>=L.
There is always a finite cover: at lambda=H all deficits vanish and
x=y=0 suffices.

If sigma is unavailable, only lambda=0 is allowed. A cover is feasible
iff U is empty. If U is nonempty the cover is infeasible and M=+infinity.
No amount of unavailable eta or xi is introduced to repair it.

On the appropriate feasible domain define

    J_*(lambda)=bar_s lambda+psi_0(lambda)+psi_1(lambda). (P7)

Equations (P3) and (P5) prove that this is the attained optimum over
all eta/xi rates at that fixed lambda. No allocation magnitude other
than its zero/nonzero support is needed for this local-rate elimination.

## Prove every breakpoint and attainment

Each deficit r_lm is continuous and piecewise linear, with its only
positive breakpoint at 1/s_lm. When B_l is nonempty,

    R_l=(1-s_B lambda)_+,
    s_B=min_(m in B_l)s_lm.                             (P8)

All these affine deficits share the intercept one. Thus for an available
row m, r_lm>=R_l for every lambda>=0 iff s_lm<=s_B; if s_lm>=s_B,
r_lm<=R_l everywhere. At equal slopes their difference is identically
zero. There is no hidden positive crossing between these deficits.

It follows that each term (r_lm-R_l)_+ is either zero everywhere or
r_lm-R_l everywhere, with breaks only at the two constituent zero
thresholds. For example, if

    A_l^-={m in A_l:s_lm<s_B},

then (P5) is exactly

    psi_l=[15/14-(3/7)|A_l^-|]R_l
                         +(3/7)sum_(m in A_l^-)r_lm.    (P9)

The coefficient of R_l is positive. For B_l empty, (P5) reduces to
(3/7)sum_A r_lm; (P3) already has this form on its domain.
Consequently J_* is continuous, convex and piecewise linear on its
feasible domain. Every possible breakpoint belongs to the original
tight-row threshold set {1/s_lm:(l,m) in T}. Repeated thresholds,
zero-length intervals and equal slopes are allowed; no branch is
inferred from a generic-position assumption.

For lambda>=H every deficit is zero and J_*(lambda)=bar_s lambda.
Since bar_s>0 this tail is strictly increasing. With sigma available,
the global minimum is therefore attained on the compact interval
[L,H]. Its complete candidate set is

    B={L} union {1/s_lm:(l,m) in T and 1/s_lm>=L}.        (P10)

There are at most five distinct candidates. H is included whenever
T is nonempty, and if T is empty B={0}. Between consecutive candidates
J_* is affine, so a minimum occurs at an endpoint; if it is constant
on an interval, both endpoints attain the same minimum. No sampling
or numerical enumeration is needed to prove completeness.

The covering minimum is exactly

    M=min_(lambda in B)J_*(lambda), if G is true;

    M=J_*(0), if G is false and U is empty;

    M=+infinity, if G is false and U is nonempty.         (P11)

This also provides an explicit attaining cover via (P3)/(P5), including
the equality M=1. The abstract compact-sublevel attainment argument in
the companion note does not hide an unattained limiting direction.

## Canonical obstruction in finite form

For kappa_i>0, an available supported cover with M<1 gives strict primary
descent; M=1 gives exact primary equality and strict lexicographic
descent. Tau is the only increase, kappa decreases before tau, and all
additional changed compensators decrease. Every rate and epsilon is
finite, and all slack-row restrictions remain.

Thus at the actual canonical point, whenever kappa_i>0 and G is true,

    J_*(lambda)>1 for EVERY lambda in B.                 (P12)

When kappa_i>0 and G is false, either U is nonempty (infeasible cover)
or J_*(0)>1.
These are exact obstructions for this entire family, not inferred
numerical facts about the actual point.

Setting eta and xi usage to zero recovers the accepted sigma-only
test: for nonempty T, sigma must have lambda>=1/min_T s, with cost
bar_s/min_T s at its best endpoint. Equality is still a lexicographic
descent. The full cover may be cheaper because it admits additional
supported compensators; it never silently removes that existing ray.

## Exact zero sigma and support consequences

Suppose G is false. If every tight xi is available, (P5) uses no eta
and every tight deficit at lambda=0 equals one, so

    M=3|T|/7.                                          (P13)

If a tight xi is unavailable, its eta is either unavailable too,
making the cover infeasible, or it must supply x_l>=1. In the latter
case its eta cost alone is 15/14>1. Therefore, with kappa_i>0 and
sigma_i=0, a descent in the COMPLETE family exists exactly when

    every xi on a tight coefficient row is positive
    and |T|<=2.                                        (P14)

This includes the empty-tight-set case, where M=0. There is no primary
tie in (P13): integer |T| between zero and four cannot make 3|T|/7=1.

The lambda=0 choice is also permitted when sigma is available.
Consequently the actual canonical point with kappa_i>0 must satisfy

    |T|>=3 OR some tight row has xi_(i,l,m)=0.           (P15)

This condition is necessary regardless of sigma or eta availability.
For G=false it exactly characterizes absence of a descent in this
family; for G=true the other finite candidates impose further tests.
The count is of the four distinct coefficient rows, with every repeated
original marked row and its cost already retained.

## Exact all four tight row case

If all four coefficient rows are tight, average their cover inequalities.
Using the ACTUAL four-row mean from RI252 gives

    (1/2)sum_l x_l+(1/4)sum_lm y_lm+bar_s lambda>=1.

Subtracting this expression from the objective yields

    J>=1+(4/7)sum_l x_l+(5/28)sum_lm y_lm.               (P16)

Thus any cover costing at most one must have x=y=0. Its remaining
four inequalities are s_lm lambda>=1, while their mean must equal
one. Each inequality must therefore be equality. Such a cover exists
exactly when sigma is available and ALL FOUR s-values are equal,
in which case lambda=1/s and J=1.

For T containing all four rows,

    M<=1 iff G is true and s_00=s_01=s_10=s_11.          (P17)

The common positive s makes the candidate finite. Attainment proved
above excludes an unattained infimum at one in other cases. Thus
additional eta/xi compensation cannot overcome the all-tight,
nonconstant-s obstruction at non-worsening primary cost, regardless
of their support. This is a limitation of this specified family,
not a proof that the actual canonical point has all four rows tight
or that any particular s-values differ.

## What remains undecided

The formula now needs only the actual tight-row set, eta/xi/sigma
zero/nonzero support and the four fixed lower s-values. The positive
h_l,n_l,p,v factors cancel from the normalized cover prices; their
positivity is retained in rate reconstruction and step bounds.
No support or lower value has been acquired or assigned.

The original kappa gap and actual C_b remain unresolved. These local
support/contrast conditions impose no proved bound on a positive
kappa magnitude and no cross-sector comparison. They are not a
global optimality certificate, full normalized witness or signed
inconsistency. All full-system, recovery, canonical-selector, record,
strict-endpoint and source boundaries in COMPENSATION_COVER.md remain.
No new source admission, executor, successor or publication is started.
