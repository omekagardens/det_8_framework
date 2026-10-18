> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Original nu dual constraint and forced larger block price

1 October 2026, OBSCURED-LOCATION. RI258 manual author result pending independent review.

The complete original nu columns force positive P dual mass in the
larger-n block whenever kappa and all four xi are positive and n differs.
Its lower bound is p/240 plus the stated companion-price and reduced-cost
terms. This is stronger than unpriced tightness and does not assume nu
or tau is positive.

When n values coincide, the same identity forces the original tau and
BOTH nu reduced costs to vanish, even if those allocations are zero.
These are conditional primary-dual endpoint statements; the companion
circulation proof separately rejects this support branch by the actual
canonical lex selector. No reduced dual is offered as a sufficient
global certificate and no actual full dual vector is constructed.

## Actual nu price from every carrying record

Use the fixed sector and positive p,v,n_l,a0 of PARENT_CIRCULATION.md.
The complete nu_(i,j) incidence is P with potential n_l and P_nu with
potential p. It has no Q or P_tau occurrence. The other original
columns, including xi and all residual components, remain.

The accepted marked weights are

    Pi_P(i,j,k,l,m)=3p/1280,
    Pi_Pnu(i,j,l,m,k)=n_l/768.                           (N1)

The first follows from RI248 and RI252 as shown in the companion note.
The second is RI254's full marked history identity: P_nu has the unique
final top, its remaining rigid N has five extensions, and retaining
the final fair newborn factor gives (n_l/2)(1/384).

At fixed i,j,l each parent has four records (k,m or m,k), giving

    sum_(k,m)Pi_P=3p/320,
    sum_(m,k)Pi_Pnu=n_l/192.                            (N2)

Thus the COMPLETE primary coefficient of this one nu coordinate is

    beta_nu(i,j)
       =-sum_l [n_l(3p/320)+p(n_l/192)]
       =-7p(n_0+n_1)/480.                              (N3)

Both compulsory j values have this coefficient by the proved marked
weight identity, not by silently deleting the j record.

## Necessary relations in the full original dual

Let z_R be any optimal nonnegative row dual of the original complete
canonical problem, paired with the same canonical candidate. Introduce
unevaluated aggregate notation at fixed i:

    A_lj=sum_(k,m) z_P(i,j,k,l,m),   A_l=sum_j A_lj;
    B_lm=sum_(j,t) z_Ptau(i,j,l,m,t), B_l=sum_m B_lm;
    D_lmj=sum_k z_Pnu(i,j,l,m,k),     N_lm=sum_j D_lmj. (N4)

Each A_lj sums four records; each B_lm sums four; each D_lmj sums two.
All are nonnegative sums over complete original rows, not uniform
surrogates. B_l and B_lm here are dual aggregates, not row residuals.

Using beta+A^T z>=0, the full nu column is

    sum_l n_l A_lj+p sum_(l,m) D_lmj
                      >=7p(n_0+n_1)/480,  j=0,1.      (N5)

Let e_j be its left side minus right side. Then e_j>=0, with e_j=0
if nu_(i,j)>0 by coordinate complementarity. For a zero nu coordinate
the inequality is retained unless a separate argument proves equality.

Assume now kappa_i>0 and all four xi_(i,l,m)>0. The accepted Y slack
forces z_Y=0. Kappa complementarity and the full actual P weight give

    A_0+A_1=3p/80.                                      (N6)

The complete tau reduced cost becomes

    r_tau=p[B_0+B_1-7v/240]>=0,                         (N7)

with r_tau=0 if tau_i>0. This follows by substituting (N6) into its
full P/P_tau column, not by deleting the P contribution.

For each positive xi its COMPLETE original column is equality:

    n_l B_lm+v N_lm=vn_l/80,
    N_lm=n_l[1/80-B_lm/v]>=0.                          (N8)

In particular each B_lm<=v/80. No value of any aggregate is supplied.
Q constraints, eta reduced costs, sigma, mu and all other original
rows/columns are still required. Relations (N5)-(N8) alone are not
a sufficient dual feasibility or optimality certificate.

## The exact circulation identity in original dual variables

Sum (N5) over j and substitute (N8). This gives the exact identity

    e_0+e_1=sum_l n_l A_l-(p/v)sum_l n_l B_l
                                  -p(n_0+n_1)/240.     (N9)

For unequal n put d=n_+-n_->0 and let l_+ be the larger-n block.
Write A_+=A_(l_+) and B_+=B_(l_+). Using (N6)-(N7) in (N9),

    d[A_+-(p/v)B_+-p/240]
                    =(n_-/v)r_tau+e_0+e_1.            (N10)

This can also be checked directly against the circulation: the
reduced-cost pairing with its increasing tau and two nu coordinates
is (n_-/v)r_tau+e_0+e_1. Every decreasing kappa/xi reduced cost is
zero under the stated support. Pairing its original row slopes
with z and adding its exact primary cost yields the left side.
Y contributes zero since z_Y=0; Q and P_nu cancel on EACH row.

Consequently the larger P block must carry

    A_+=p/240+(p/v)B_+
                +(n_-/(v d))r_tau+(e_0+e_1)/d
         >=p/240+(p/v)B_+>=p/240>0.                    (N11)

This is an identity followed by lower bounds, valid even when tau
or either nu is zero. The first inequality is equality exactly when
r_tau=e_0=e_1=0. Positive tau and both positive nu suffice for that
equality, but are not necessary; zero allocations can have zero
reduced cost.

Since the sector total is 3p/80, even the weakest bound p/240 is
one ninth of its total original P dual mass. Thus at least one
of the eight marked rows in the larger-n block is positively
priced and tight. Neither all rows nor a particular marking is
identified, and the smaller block may also carry positive mass.

This matches the primal obstruction: if every larger-block P row
were slack then A_+=0 by row complementarity, contradicting (N11).
A binding Q or P_nu cap does not itself block this circulation.

## The complete P residual cap that must remain

Retain the fixed lower t coefficient and every original record from
PARENT_CIRCULATION.md. Define, without evaluating it,

    RP_+^max=max_(j,k,m)
          [t(i,j,k,l_+,m)mu_(i,l_+)+n_+ nu_(i,j)].     (N12)

Every one of the eight complete P inequalities has common remaining
part a0 kappa_i+v tau_i. A positively priced tight row in this block
therefore gives the exact necessary identity

    a0 kappa_i+v tau_i=1-RP_+^max.                      (N13)

All other blocks and full original constraints remain. RP_+^max
depends on the actual mu and nu allocations and fixed lower law;
it is not independently assignable or replaced by zero. Equations
(N11) and (N13) have not been proved incompatible with the remaining
original problem. They do not evaluate kappa or its cross-sector gap.

## Equal n forces column equalities before lex rejects the branch

For n_0=n_1=n>0, apply (N9) directly without dividing by a contrast.
Equations (N6)-(N7) give

    0=(n/v)r_tau+e_0+e_1.                              (N14)

Each term is nonnegative and n/v>0. Hence a hypothetical primary
optimal candidate with this support must obey

    r_tau=e_0=e_1=0,
    B_0+B_1=7v/240.                                    (N15)

Both nu reduced-cost inequalities and the tau inequality are
therefore equalities EVEN IF one or more of those increasing
coordinates initially has zero allocation. This is proved by
(N14), not assumed from an invalid converse of complementarity.

Summing the four xi equalities also gives in this endpoint case

    sum_(l,m)N_lm=n/48>0.                               (N16)

Thus at least one complete P_nu group is positively priced. With
RI256's chi_l=Q_l/h_l and both xi positive in each block,

    chi_0+chi_1>=1/30,                                  (N17)

with equality if both eta allocations are positive. Here positive
tau is NOT needed: the equality normally obtained from positive
tau has already been forced by (N14). These are conditional
primary-stationarity facts, not a surviving canonical branch.

PARENT_CIRCULATION.md proves more at n equality. Its finite
zero-cost step decreases kappa and all xi, while every increase
(tau and both nu) lies after kappa in the ACTUAL component ordering.
The earliest change is therefore a decrease, contradicting the
canonical sequential lex minimum. Necessary dual column equalities
cannot rescue that lexicographically rejected branch.

## Scope of the completed obstruction

The new result is a strict finite descent when larger-block P
slack permits it, a complete lex exclusion at equal n, and a
quantitative original-dual binding relation in the remaining
unequal-n positive-support branch. This is not another incidence
catalogue and not a global characterization of the canonical point.

If any xi is zero, this particular circulation is infeasible.
If n differs and the larger P block binds, it is blocked without
deciding whether another direction exists. Actual support,
n contrast, residual maximum, full dual vector, kappa gap and
C_b remain unevaluated. No full normalized witness or signed
inconsistency follows.

All original equations/coordinates, actual offsets and selector,
complete recovery, accepted d=0!=d7 and normalized existence iff
actual C_b=0, records, labeled ideals, both newborns and strict
restoration remain. All 15 inherited boundary objects and the
423-source manifest stay intact by reference; all original literal
exceptions remain closed. No new original body/hash/checker,
scientific JSON, coefficient acquisition, mathematical engine,
measurement/RET, repository/Git/index, publication or successor.
Stop for independent root adjudication.
