# Sigma compensated exchange and the strict tight row obstruction

1 October 2026, Honolulu. RI252 manual author result pending independent review.

For the fixed original canonical problem, the positive three-coordinate
ray has an exact feasibility and descent criterion. If both kappa_i and
sigma_i are positive at the canonical optimizer, some tight carrying
companion row must have s strictly below the actual history-weighted
sector mean. Equality is excluded by the original lexicographic selector,
not by primary duality alone. No actual kappa gap or C_b sign is decided.

## Fixed problem and the positive ray

Keep the original closed canonical feasible set alpha>=0, A alpha<=1,
its actual history-weighted primary objective Phi, and the complete
sequential lexicographic minimizer of its primary optimal face. These
are not replaced by a reduced optimization problem. The fixed strictly
positive lower law and eventual strict restoration remain unchanged.

Fix i in {0,1}. Abbreviate p=p_i>0, v=v_i>0 and a0=41/352. For a finite
compensation parameter c>=0 consider epsilon>0 and only

    Delta tau_i=epsilon,
    Delta kappa_i=-(v/a0)epsilon,
    Delta sigma_i=-c epsilon.                              (S1)

Every other original coordinate is fixed. Here c is the exchange
parameter, not the parameter named c in the inherited normalized
disconnected forms. This note treats the positive ray (S1), not
negative epsilon or arbitrary coupled directions.

For each complete marked P_tau record r=(i,j,l,m,t), retain

    C_r=p tau_i+h_(i,l)eta_(i,l)+n_(i,l)xi_(i,l,m)
                                               +s_(i,l,m)sigma_i,
    S_r=1-C_r>=0,
    s_r=s_(i,l,m)>0,
    w_r=Pi_tau(i,j,l,m,t)>0.                               (S2)

There are sixteen carrying records for this fixed i: each of the four
(l,m) coefficient rows retains all four (j,t) assignments. Let

    W=sum_r w_r>0,
    bar_s=(sum_r w_r s_r)/W>0,
    T={r:S_r=0}.                                         (S3)

If T is nonempty set s_*=min_(r in T)s_r. Do not replace this with
the minimum over all rows. A slack row can have a lower s.

## Complete affected rows and nonnegativity

RI248's complete component incidence gives exactly these changes:

    P with root i:       Delta C_P=0,
    Y with root i:       Delta C_Y=-v epsilon/(64 a0),
    P_tau carrying i:    Delta C_r=(p-c s_r)epsilon,
    V5 record (b,d,...): Delta C_V5
                         =-c epsilon(v/40)
                                  [1_(b=i)+1_(d=i)].      (S4)

Here b,d are the marks on V5's two minimal vertices. When b=d=i,
the bracket is TWO: both distinct singleton ideals remain. When
exactly one matches i it is one; when neither matches it is zero.
All other original rows are unchanged, including Q, P_nu and P_mu.
All their original residual allocations are retained.

The P cancellation is a0 Delta kappa+v Delta tau=0. Y and V5
only lose proper mass. No slack is borrowed from an unchanged row,
and no hidden compensation of eta,xi or any other coordinate is used.

Coordinate nonnegativity gives the exact upper bounds

    epsilon<=a0 kappa_i/v,
    epsilon<=sigma_i/c when c>0.                          (S5)

Tau increases even if initially zero. If kappa_i=0 no positive epsilon
is feasible. If sigma_i=0 then c must be zero. For c=0 there is no
sigma bound, including at sigma_i=0.

At every tight carrying row, positive epsilon requires

    p-c s_r<=0.                                         (S6)

For every originally slack row with p-c s_r>0, require

    epsilon<=S_r/(p-c s_r).                              (S7)

Rows with zero slope keep their slack and rows with negative slope
gain slack. Thus, subject to kappa_i>0, sigma_i>0 whenever c>0,
and (S6), the minimum of (S5) and all applicable (S7) is positive.
There are finitely many rows, each retained numerator and denominator
in (S7) is strictly positive, and the kappa bound is finite positive.

Any positive epsilon up to that minimum is feasible in the ORIGINAL
closed canonical problem; a smaller epsilon retains all originally
positive decreasing coordinates. Equality may put a coordinate at zero
or make a previously slack row tight, and is still allowed in that
closed problem. This is not a claim that a boundary canonical vector
alone is a strict law: the unchanged strict restoration is retained.

These conditions are necessary as well as sufficient. If a tight row
has positive slope it fails for every epsilon>0; a decreasing zero
coordinate fails similarly. Conversely (S4) exhausts all row changes.

## Exact primary cost and earliest changed coordinate

The P contribution to the primary variation vanishes exactly. Y and
V5 have full defect increment zero; their constraints still matter,
but they add no primary cost. RI248's full objective identity therefore
gives the exact finite change

    Delta Phi=-epsilon sum_r w_r(p-c s_r)
             =epsilon W(c bar_s-p).                     (S8)

This is not merely a first-order approximation. Both newborns,
all marked rows and actual natural-history multiplicities remain.

SIGMA_KEYS_AND_WEIGHTS.md proves the actual component order

    kappa_i at (8590,17,i)
       < sigma_i at (8604,15,i)
       < tau_i at (8604,17,i).                           (S9)

For every feasible positive epsilon the earliest changed original
coordinate is therefore kappa_i, and it DECREASES. No earlier coordinate
changes. Consequently:

- c<p/bar_s gives strict primary descent.
- c=p/bar_s gives exactly equal primary objective and strict
  lexicographic descent on the original primary face.
- c>p/bar_s increases the primary objective and is not a descent,
  irrespective of any lexicographic improvement.

This explicitly checks every changed coordinate, including sigma.
Knowing only the kappa/tau order would not establish (S9).

## Necessary and sufficient local descent criterion

For a fixed finite c>=0, the positive ray gives a primary-or-equal-primary
lexicographic descent if and only if ALL of the following hold:

    kappa_i>0;
    c=0 or sigma_i>0;
    T is empty, or c>=p/s_*;
    c<=p/bar_s.                                         (S10)

The preceding finite epsilon bound supplies a nonzero step whenever
these conditions hold. Thus this is a complete criterion for this
specified ray family, not a global optimality certificate.

Eliminating c gives the following cases.

If kappa_i=0, no positive ray in this family is feasible.

If kappa_i>0 and sigma_i=0, only c=0 is possible. It gives strict
primary descent exactly when T is empty. If T is nonempty, every
carrying tight row has slope p>0, so no ray is feasible.

If kappa_i>0 and sigma_i>0 and T is empty, c=0 already gives strict
primary descent. No minimum over an empty set is assigned a value.

If kappa_i>0, sigma_i>0 and T is nonempty, feasible descent parameters
are exactly

    p/s_* <= c <= p/bar_s.                               (S11)

There is strict primary descent for some c iff s_*>bar_s.
There is primary-or-equal-primary lexicographic descent for some c
iff s_*>=bar_s. At the tie s_*=bar_s, the only such parameter is
c=p/bar_s: all minimum-s tight rows have zero slope, other tight
rows relax, and every positively sloped slack row is handled by (S7).

Multiple tight rows are governed by their smallest s, not their average.
All tied minima and repeated marked rows are retained. No assumption
that tau_i, eta, xi or other residual allocations are positive is used.

## New strict obstruction at the actual canonical point

The actual canonical point admits none of the descents just proved.
RI248 already supplies T nonempty when kappa_i>0. Combining this with
(S11) gives the new necessary condition

    kappa_i>0 and sigma_i>0  =>  s_*<bar_s.               (S12)

Equivalently, some tight carrying row lies strictly below the sector
mean. It does not say that every tight row lies below it, or that the
row with the globally smallest s must be tight.

At a primary optimizer without lexicographic selection only
s_*<=bar_s follows from this family. Strictness in (S12) needs the
actual earliest-coordinate proof and the exact zero-cost tie.

This distinction can also be seen in the primary dual. Write z for
any optimal row dual. Positive sigma gives

    sum_(carrying P_tau) z_r s_r
      + sum_V5 z_V5(v/40)[1_(b=i)+1_(d=i)]
          =W bar_s.                                     (S13)

Complementarity puts every positive carrying z_r on a tight row.
For positive kappa, RI248 gives sum_r z_r>=W. Therefore

    s_* W <= s_* sum_r z_r
           <= sum_r z_r s_r <= W bar_s.                 (S14)

These inequalities alone allow equality. In that endpoint they force
sum_r z_r=W, no positive carrying dual weight above s_* and zero
weighted V5 contribution. They do not forbid the endpoint. The
lexicographic descent at c=p/bar_s forbids it canonically. No actual
dual allocation is instantiated or acquired.

## Exact mean and conditional constant coefficient consequence

The companion note derives, from the admitted seed and complete
prefix diamonds rather than a uniform-weight assumption,

    bar_s=(s_(i,0,0)+s_(i,0,1)
                     +s_(i,1,0)+s_(i,1,1))/4.           (S15)

Thus (S12) is a four-coefficient strict comparison, with all sixteen
original records still represented.

If the prescribed lower law were proved to have constant s across
this sector's four (l,m) rows, any nonempty T would have s_*=bar_s.
Then (S12) implies

    constant s in sector i => kappa_i sigma_i=0.         (S16)

No constant-s premise is assumed or proved here. In particular,
the admitted minimum-swap symmetry is not a record-flip symmetry.

## Remaining decision and retained system

This restricted exchange does not decide whether sigma_i is zero,
which complete companion rows are tight, or their s-values. If both
coordinates are positive, a tight row below the mean is an exact
remaining obstruction; if sigma_i=0, this compensation cannot be used.
The criterion supplies neither a magnitude bound on positive kappa
nor a comparison between the two kappa sectors.

In particular, kappa0-kappa1<=1/70 remains unproved and actual C_b
remains open. A sufficient comparison failing or being unavailable
does not prove C_b=0. No original rank lookup or sparse-entry inference
is attempted; RI250's accepted GAP-INDEX and its conditional absent-entry
rule requirement remain. Its literal authority is closed.

Retain all ten unknowns u0,u3,U4,...,U11, fixed u2=-1, all five complete
disconnected and eight connected equations, actual canonical offsets
and the complete recovery in RI248 CANONICAL_BINDING.md section 7.
Forced-zero consequences do not remove coordinates or constraints.
The accepted d=0!=d7 branch and normalized existence iff actual C_b=0
remain. Every record, labeled ideal, both newborns, strict endpoint,
all 15 boundary objects and the 423-source by-reference manifest remain.

This is a finite same-law analytic result, not a full witness, signed
inconsistency, all-size QM, geometry, mass or gravity result. No new
coefficient or original body, scientific JSON, mathematical engine,
subject execution, measurement/RET, repository/Git/index or successor
is authorized. Stop for independent root adjudication.
