> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Original dual compatibility and forced parent caps

1 October 2026, OBSCURED-LOCATION. RI256 manual author result pending independent review.

The signed redistribution forces more than a possibly tight Q row.
When both xi are positive, every optimal dual of the COMPLETE original
problem must place Q mass at least h_l/160 plus the specified P_nu
mass. More generally the bound depends on which companion rows are
tight. A slack companion row independently forces positive P_nu mass.

Combined with positive kappa, these are new quantitative restrictions
on the three- and four-tight-row branches left by RI254. They do not
evaluate the actual support, residuals, dual vector, kappa gap or C_b.

## Dual weights are from the original problem

Let z_R be ANY optimal nonnegative row dual of the original full
canonical problem. Retain every original row, column, reduced-cost
inequality and complementary-slackness condition. No reduced dual
problem or candidate full dual vector is constructed here.

At fixed i, write v=v_i and use the accepted positive h_l,n_l.
Define sums over actual original marked rows, not uniform surrogates:

    Z_lm = sum_(j,t) z_Ptau(i,j,l,m,t),
    Q_l  = sum_(j,m,k) z_Q(i,j,l,m,k),
    N_lm = sum_(j,k) z_Pnu(i,j,l,m,k).                  (D1)

Each Z sums four records, each Q eight, each N four. They are
nonnegative. Introduce normalized aggregate NOTATION only,

    zeta_lm=Z_lm/v,   chi_l=Q_l/h_l,   delta_lm=N_lm/n_l. (D2)

These are unevaluated functions of the same full original dual.
No numerical dual allocation or additional coefficient is acquired.

The complete eta column has h_l in each carrying companion row and
v in every carrying Q row; its primary coefficient is -v h_l/32.
The complete xi column has n_l in each carrying companion row and
v in every carrying P_nu row; its coefficient is -v n_l/80.
The accepted complete incidence therefore gives exactly

    zeta_l0+zeta_l1+chi_l >= 1/32,
      equality if eta_(i,l)>0;

    zeta_lm+delta_lm >= 1/80,
      equality if xi_(i,l,m)>0.                         (D3)

The implications to equality are coordinate complementarity, not
assumed because a role is named. In particular a zero xi does NOT
permit its reduced-cost inequality to be replaced by equality.

Row complementarity gives

    S_lm>0 => zeta_lm=0;
    every carrying Q row slack => chi_l=0;
    every carrying P_nu,lm row slack => delta_lm=0.       (D4)

A positive aggregate implies at least one positively priced tight
row in its complete marked group, not that every row in the group
is tight or that its residual has a chosen value.

Under the ADDITIONAL assumption kappa_i>0, the inherited complete
P/Y and tau reduced-cost argument gives

    sum_(l,m) zeta_lm >= 7/240,
      equality if tau_i>0.                              (D5)

This uses actual Pi_tau,i=7v/240 and the accepted Y slack, rather
than omitting the P/Y columns. All other original dual constraints,
including sigma and every residual component, remain. Equations
(D3)-(D5) are necessary relations, not a sufficient certificate of
full dual feasibility or global optimality.

## Forced Q price from the requested signed move

If xi_(i,l,0)>0 and xi_(i,l,1)>0, add their equalities in (D3) and
substitute into the eta inequality. This yields

    chi_l >= 1/160+delta_l0+delta_l1,                    (D6)

with equality when eta_(i,l)>0. In original units,

    Q_l >= h_l/160+(h_l/n_l)(N_l0+N_l1).                (D7)

Since h_l>0 and both N terms are nonnegative, every such primary
optimal dual has Q_l>0. Hence some carrying Q row is positively
priced and tight. Eta may be zero; the inequality still holds.

The margin 1/160 is the exact primary advantage of the signed
mass-preserving move. Merely claiming that an unspecified Q row
might bind would miss the quantitative original-dual requirement.
Conversely no positive P_nu price follows from (D6) alone: either
N term may vanish unless another condition forces it.

For the more general subset move in SIGNED_REDISTRIBUTION.md, put
t_l=|T_l|. If every xi on a tight companion row is positive, off-T_l
zeta terms are zero and on-T_l xi equalities apply. Then

    chi_l >= (5-2t_l)/160
                        +sum_(m in T_l)delta_lm,        (D8)

with equality if eta_(i,l)>0. The constant is respectively 5/160,
3/160 or 1/160 for zero, one or two tight coefficient rows; all are
strictly positive. Thus the localized Q obstruction has a positive
dual price even when some xi on SLACK companion rows is zero.

No equality for those zero xi is used. This is why (D8) is valid
in support cases not covered by the two-positive-xi assumption in
(D6). A zero xi on a TIGHT companion row prevents this derivation
and blocks the corresponding decreasing-coordinate direction.

## Every slack companion forces its P_nu group to bind

If S_lm>0, (D4) and the xi inequality imply

    delta_lm>=1/80, i.e. N_lm>=n_l/80>0.                (D9)

Equality holds if xi_(i,l,m)>0. This conclusion does not require
positive xi: when xi is zero its inequality may be strict.

Therefore some carrying complete P_nu row must be positively priced
and tight whenever that companion row is slack. The direct xi-increase
descent proves the same tightness in primal terms. A zero allocation
can still sit at a zero residual cap; positive dual price alone is
not a proof of a positive primal allocation.

## Exact residual cap identities

Retain the complete residuals from SIGNED_REDISTRIBUTION.md and define

    BQ_l^max=max_(j,m,k) B_Q(j,m,k),
    BN_lm^max=max_(j,k) B_nu,m(j,k).                    (D10)

These maxima run over all eight or four original records. They
are not evaluated. Every row constraint is retained. It follows
directly that

    Q_l>0 => eta_(i,l)=(1-BQ_l^max)/v,
    N_lm>0 => xi_(i,l,m)=(1-BN_lm^max)/v.               (D11)

For example, every Q row gives eta<=(1-B_Q)/v; a positively priced
tight Q row attains the smallest such cap, equivalently the greatest
complete residual. Multiple maximizing rows and zero caps are allowed.

These are identities involving actual OTHER original allocations,
not a license to assign their residuals. In particular the second
residual contains the original nu contribution as well as every other
proper term. No full row is replaced by its selected eta/xi term.

## Surviving positive kappa with three tight rows

Assume kappa_i>0, exactly three of the four companion coefficient
rows are tight, and every xi on those tight rows is positive. Do not
assume anything about the remaining xi or about sigma.

Only the three tight zeta values can be nonzero. Their xi equalities
bound each by 1/80. Equation (D5) then forces, for EACH tight row,

    1/240 <= zeta_lm <= 1/80.                           (D12)

Indeed the other two contribute at most 2/80=6/240, while the total
is at least 7/240. Thus all three tight groups are positively priced,
a stronger conclusion than unpriced tightness.

Summing their xi equalities gives

    0<=sum_(T)delta_lm<=1/120,
      equality at the upper bound if tau_i>0.           (D13)

The missing fourth row is slack, so it has zeta=0 and
delta>=1/80 by (D9), with equality if its xi is positive.
Its complete P_nu cap in (D11) is therefore attained, including
the possible zero-allocation/zero-cap case.

The block with two tight rows must satisfy

    chi_l >= 1/160+sum_(its two tight m)delta_lm,

and the block with one tight row must satisfy

    chi_l >= 3/160+delta_(its tight row).               (D14)

Thus BOTH Q caps in (D11) are attained with positive dual mass.
Equality in each bound holds if that block's eta is positive.

If tau_i>0 as well, (D13) has positive sum 1/120, so at least one
P_nu group attached to a TIGHT companion is additionally positively
priced. This is distinct from the P_nu group forced by the missing
fourth row. If tau_i=0, only the weak bound is retained; this extra
positive P_nu conclusion is not asserted.

Consequently the three-tight branch must meet the exact simultaneous
conditions

    p tau_i+(h_l/v)(1-BQ_l^max)+n_l xi_(i,l,m)
                            +s_lm sigma_i=1 on T,

    p tau_i+(h_l/v)(1-BQ_l^max)
       +(n_l/v)(1-BN_lm^max)+s_lm sigma_i<1
                            on the missing row,         (D15)

alongside (D12)-(D14), all complete Q/P_nu rows and all other original
constraints. No residual maximum or actual support has been guessed.

## Surviving positive kappa with all four xi positive

Assume kappa_i>0 and all four xi are positive. Their full equalities
give

    sum_(l,m)delta_lm=1/20-sum_(l,m)zeta_lm
                    <=1/48.                           (D16)

If tau_i>0, equality holds at 1/48. Every block obeys (D6), so its
Q cap is positively priced and attained, irrespective of which
companion rows are tight.

In particular this applies to RI254's all-four-tight, nonconstant-s
branch. If any carrying Q group were entirely slack, the signed
mass-preserving move would strictly descend despite the former
nonnegative-cover obstruction. This is a new exclusion, independent
of sigma availability or the s contrast.

When tau_i>0 as well, (D16) forces at least one positively priced
P_nu group and hence at least one further cap in (D11). Also

    chi_0+chi_1>=1/30,                                  (D17)

with equality if both eta allocations are positive. If tau_i=0,
(D16) is only an upper bound and may permit all delta to vanish;
do not promote that endpoint to a forced P_nu price.

The four companion constraints (equalities only on tight rows), both
Q residual-cap identities and these dual balances are retained together.
They have not been
shown incompatible with the actual full law. No candidate primal
or dual vector is supplied to claim their simultaneous realization.

## Exact remaining question and retained boundaries

This packet excludes the previously surviving Q-slack signed-support
case by an actual strict finite descent. It also makes the Q-bound
alternative quantitative and forces complete P_nu caps where companion
slack exists. What remains unknown is whether the fixed canonical
residual maxima, support and tight set can satisfy those binding
relations together with the full original problem. Neither the
residuals nor dual masses may be replaced by free parameters.

No canonical kappa gap or C_b decision follows yet. A local stationarity
subsystem is not global optimality, a full normalized witness or signed
inconsistency. Retain all 13 equations/10 coordinates, complete recovery,
actual canonical selector/offsets, accepted d=0!=d7 and normalized-system
iff actual C_b=0, records, ideals, both newborns and strict endpoints.
All 15 source boundaries and the 423-source manifest remain unchanged
by reference. All original literal exceptions remain closed.

No scientific body/hash/checker, coefficient or support acquisition,
scientific JSON, mathematical engine, dual-vector reconstruction,
subject execution, measurement/RET, repo/Git/index, publication or
successor is started. Stop for independent root adjudication.
