> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Exact shared sigma minimum and family closure

1 October 2026, OBSCURED-LOCATION. RI262 manual author result pending independent review.

The full supported compensation problem reduces to a convex function
with at most two hinges. Its minimum is attained at at most three
explicit scalar candidates. Unavailable eta/sigma, empty tight sets,
equal breakpoints and flat minimizing intervals are included.

Combined with the complete row bounds, this gives a primary/lex iff
for every xi support in the same circulation family. The no-zero,
equal-n endpoint has M_Z=G_Z=0 and is rejected by the original lex
selector, not lost under a strictly positive gain assumption.
The family is now closed; blocked parent caps remain a global issue.

## Normalize the tight zero companion cover

Use ALL_SUPPORT_CIRCULATION.md, including kappa_i>0, the actual
unknown zero set Z, T=Z intersect tight companion pairs, and H_Z.
Let b_*=p n_-/v>0. Set local rate coordinates

    x_l=h_l a_l/b_*,   lambda=c/b_*.                    (M1)

These are notation for direction rates, not new original canonical
or normalized-system coordinates. Positivity gives the inverse

    a_l=(b_*/h_l)x_l,   c=b_*lambda.                    (M2)

Unavailable eta forces x_l=0; unavailable sigma forces lambda=0.
A supported nonnegative rate vector covers the tight zeros iff

    x_l+s_lm lambda>=1, (l,m) in T.                    (M3)

The complete compensation cost becomes

    sum_l(v h_l/32)a_l+(7v bar_s/240)c
       =(p n_-/240)J(x,lambda),

    J=(15/2)(x_0+x_1)+7bar_s lambda.                   (M4)

Every coefficient is positive. The mean bar_s still uses ALL four
original s values, not only T or Z. Parent slacks H_Z are independent
necessary conditions; solving (M3) alone does not supply those slacks.

Let M_Z be the minimum cost in (M4) over supported (M3), with infinity
when the supported cover is infeasible. We prove its attainment
and exact formula below before using a minimum in a finite step.

## Eliminate both eta rates exactly

Write E_l for availability eta_(i,l)>0, and let

    A_T={l:T_l is nonempty},
    t_l=min_(m in T_l)s_lm>0, for l in A_T.              (M5)

For lambda>=0, each available eta block must have

    x_l>=max_(m in T_l)(1-s_lm lambda)_+
       =(1-t_l lambda)_+, l in A_T.                   (M6)

The same intercept one and nonnegative lambda make the smallest s
the strongest constraint. This is a proved domination of constraints,
not a removal of marked histories. For T_l empty the lower bound is
zero. Since x_l has strictly positive cost, its unique least-cost
value at fixed lambda is exactly that lower bound.

If E_l is false then x_l=0. A nonempty T_l is feasible precisely
when lambda>=1/t_l; an empty T_l imposes no restriction. Define

    U={l in A_T:E_l is false},
    L=max_(l in U)1/t_l, with L=0 if U is empty,
    H=max_(l in A_T)1/t_l, with H=0 if A_T is empty.    (M7)

All are finite and 0<=L<=H. No t_l is defined or divided by for
an empty block. Thus on its feasible sigma domain the exact
eta-eliminated cost is

    J_*(lambda)=(15/2)sum_(l in A_T with E_l true)
                                      (1-t_l lambda)_+
                                  +7bar_s lambda.     (M8)

The unique least-cost eta values are (M6) in available active
blocks, and zero in every other block. An available eta in a
block with no tight zero never helps this minimum: its positive
cost cannot reduce a required constraint in the other block.

## Sigma availability and finite attainment

If sigma_i=0, only lambda=0 is permitted. The cover is feasible iff
U is empty. In that case all active blocks have available eta and

    M_Z=(p n_-/240)J_*(0)
        =(p n_-/32)|A_T|.                             (M9)

If U is nonempty and sigma unavailable, M_Z=infinity. No absent
source is given a fictitious zero price or a nonzero rate.

If sigma_i>0, the feasible domain is exactly lambda>=L. It is
nonempty: lambda=H covers every tight zero without eta. For
lambda>=H all hinges vanish, so J_*(lambda)=7bar_s lambda,
a strictly increasing tail. Therefore its global minimum is
attained on the finite compact interval [L,H].

The only possible breakpoints of (M8) on that interval are 1/t_l
for AVAILABLE active blocks. Define

    C={L} union {1/t_l : l in A_T, E_l true,
                                      1/t_l>=L}.       (M10)

There are at most THREE distinct points: one lower endpoint
and at most two block hinges. H is included whenever needed:
if its maximizing block is unavailable then H=L; otherwise its
available hinge lies in C. If A_T is empty, L=H=0 and C={0}.

Between consecutive candidate points J_* is affine. Its minimum
on each segment occurs at an endpoint, or throughout a flat
segment with both endpoints minimizing. Repeated thresholds,
the case L=H, and a hinge at L do not create missing intervals.
Consequently the exact supported minimum is

    M_Z=(p n_-/240) min_(lambda in C)J_*(lambda),
                                             if sigma_i>0;

    M_Z=(p n_-/240)J_*(0),
                         if sigma_i=0 and U is empty;

    M_Z=infinity,        if sigma_i=0 and U nonempty.   (M11)

This is a symbolic finite reduction, not an evaluated canonical
cost or a sampled trial-rate procedure. It specializes the
admitted hinge-elimination method to this different gain and
the newly retained zero-group P_nu slacks.

For every minimizing candidate, reconstruct x by (M6), zero
unavailable/inactive blocks, then use (M2). All rates are finite
and supported. Under H_Z, the full bound in the companion note
supplies positive u, including exact cost equality. Ties need
no limit: every flat segment between adjacent minimizing candidates
also consists of minimizers and gives finite supported rates.
No minimizer lies beyond H because the tail is strictly increasing.

In particular T empty always gives M_Z=0, attained at all zero
compensator rates, whether or not any compensator is available.
Zero companions outside T still keep their finite slack/slope
bounds and every growing P_nu row; they have not been discarded.

## Complete original primary and lex criterion

All increases in this family are tau_i and BOTH nu_(i,j). RI258's
complete original component argument places all three after
kappa_i. Kappa strictly decreases for u>0. Every changed xi,
either eta, and sigma also decreases; zero xi and all unlisted
coordinates stay fixed. Thus an earlier changed compensator only
makes the first changed coordinate a decrease. Otherwise kappa
is first. Every feasible primary tie strictly improves the
original sequential lexicographic selector.

For the standing kappa>0 and arbitrary support set Z, the exact
necessary and sufficient criteria are

    strict primary descent in this family
          iff H_Z and M_Z<G_Z;

    strict primary OR primary-tie lex descent in this family
          iff H_Z and M_Z<=G_Z.                       (M12)

The necessity uses the full finite-feasibility theorem and the
fact that any supported compensation cost is at least M_Z.
A positive primary cost cannot be rescued by lex order.
For sufficiency take an attained minimizer from (M11), reconstruct
its finite supported rates, and choose a positive u through every
original bound. The exact cost is u(M_Z-G_Z); equality invokes
the complete earliest-change argument above.

This proof covers every one of the sixteen support patterns,
all eta/sigma availability patterns and every tight/slack zero
companion configuration. It requires no evaluation or enumeration
of the actual canonical pattern. It is an iff for this direction
family only, not for global optimality or the normalized system.

## Recover the no zero and single zero results

For Z empty, T is empty, M_Z=0, and no P_nu row grows.
G_Z=p Delta_n/240. If n differs, (M12) is strict descent exactly
when all larger-P rows are slack. If n agrees, H_Z is vacuous
and G_Z=0: a genuine finite PRIMARY TIE with zero compensation
still lowers the original lex selector. Strict primary descent
does not follow in that endpoint. This is exactly RI258's
canonical positive-kappa/all-positive-xi exclusion.

For Z={g}, if its companion is slack then T is empty and M_Z=0.
All four P_nu,g and any larger-P slacks remain. If it is tight,
only its block is active. An available eta in the OTHER block
uniquely minimizes at zero and cannot change either feasibility
or price for g. Formula (M11) therefore reduces exactly to

    M_Z=(p/240)min {
         (15/2)n_-       if eta_(i,ell)>0,
         7n_-bar_s/s_g   if sigma_i>0
    },                                                 (M13)

with empty minimum infinity. Flat price ties give the full
exact-coverage eta/sigma segment. Together with (M12), all finite
bounds and G_Z=p(Delta_n+3n_g)/240, this recovers RI260, including
slack-g, unavailable sources, equal n and primary equality.

When two zeros share a block, (M6) legitimately combines their
tight cover demands through the strongest s, but G_Z still counts
BOTH n_g terms and H_Z still requires both four-record P_nu groups.
This distinction also covers all-zero support without a new branch.

## Consolidated sigma threshold without xi support assumptions

Use any optimal full original row dual at the same canonical point.
Let B_g be the complete companion dual aggregate at pair g,
N_g its P_nu aggregate, and Q_l its Q aggregate. Under kappa_i>0,
accepted Y slack and the full tau inequality give

    sum_(g in I)B_g>=7v/240.                            (M14)

The original xi column, at ANY nonnegative xi allocation, gives

    n_g B_g+v N_g>=v n_g/80.                            (M15)

Positive xi would make equality, but no such premise is needed.
If sigma_i>0, its complete column is equality:

    7v bar_s/240=sum_(g in I)s_g B_g
                    +sum_(V5 records)gamma_i(record)z_V5,
    gamma_i=(v/40)[1_(first minimum bit=i)
                             +1_(second minimum bit=i)]. (M16)

Both V5 occurrences and every remaining original dual condition
remain. All dual terms are nonnegative.

For ANY pair g in I, suppose s_g>=7bar_s/3. If N_g=0, (M15)
implies B_g>=v/80. The single term s_g B_g is then already at
least the whole left side of (M16). Equality forces B_g=v/80,
the exact threshold, and all other companion aggregates zero,
because their s values are positive. This contradicts (M14).
Therefore

    kappa_i>0, sigma_i>0, s_g>=7bar_s/3
                         => N_g>0.                    (M17)

Some complete P_nu,g row is positively priced and tight. This
does NOT require xi_g=0, positivity of other xi, any particular Z,
equal n, positive eta/tau/nu, a tight g companion, or P-row slack.
It does require positive kappa and sigma, the admitted positive
lower probabilities and the COMPLETE original dual conditions.
The inequality at a zero xi is never replaced by equality.

The forced cap blocks H_Z only if g belongs to Z. For g outside Z
its P_nu rows are unchanged by this family, so their binding must
not be called a positive-slope obstruction. No particular record
or positive primal xi value is inferred from N_g>0.

## General zero coordinate reduced cost identity

Keep RI258's full original P block dual aggregates A_l,
companion block aggregates B_l=sum_m B_lm, and original
tau/nu reduced costs r_tau,e_0,e_1>=0. Kappa>0 still gives

    A_0+A_1=3p/80,
    r_tau=p(B_0+B_1-7v/240)>=0.                        (M18)

For each xi define its ORIGINAL reduced cost

    r_g=-v n_g/80+n_g B_g+v N_g>=0.

Complementarity makes r_g=0 outside Z. On Z it remains an
inequality and is not an arbitrary chosen parameter. Rearranging
each complete xi column gives

    N_g=n_g/80-(n_g/v)B_g+r_g/v.

Substituting into the sum of the complete two nu reduced costs,

    e_0+e_1=sum_l n_l A_l-(p/v)sum_l n_l B_l
                -p(n_0+n_1)/240+(p/v)sum_(g in Z)r_g.

Use (M18) and separate the common n_- contribution. For Delta_n>0,

    Delta_n[A_+-(p/v)B_+-p/240]
           +(p/v)sum_(g in Z)r_g
                         =(n_-/v)r_tau+e_0+e_1.       (M19)

For equal n=n_-=n_+, use the undivided identity

    (p/v)sum_(g in Z)r_g=(n/v)r_tau+e_0+e_1.           (M20)

Empty Z recovers the vanishing reduced costs of RI258; one zero
recovers RI260's extra inequality. A general Z cannot inherit
those vanishing conclusions without its zero-coordinate costs
being separately controlled. These are necessary original-dual
relations, not a full dual construction or a sufficient certificate.

## Close this family and identify the remaining blocker

For kappa>0 at the original canonical point, (M12) forces

    some zero-group P_nu row is tight,
    OR Delta_n>0 and some larger-n P row is tight,
    OR M_Z>G_Z, with infinity allowed.                 (M21)

Every support and compensation case within this direction family
has now been included. There is no remaining support pattern
to open as another extension of the same family. The formulas
and their primary-tie endpoint complete this bounded investigation,
subject to independent adjudication.

The unresolved issue is whether the ACTUAL full canonical support,
marked P/P_nu capacities and compensated tight-zero costs satisfy
the surviving obstruction together with every other original
constraint and the sequential selector. Parent residuals still
depend on the same actual mu,nu,eta,xi,sigma,tau,kappa allocations;
they are not independently tunable slack. A binding positive-slope
parent cap cannot be bypassed by further rearranging the already
included nonnegative eta/sigma rates. Their full family is exhausted.

This does not prove that a surviving case exists, that none exists,
or that the original global optimum is characterized. It gives
no kappa magnitude/cross-sector gap and no C_b decision. A new
question would need root selection; this packet designs or opens
no successor and performs no actual-value acquisition.

All 13 equations/10 coordinates, u2=-1, full recovery and actual
offsets/selector, accepted d=0!=d7 and full-system existence iff
actual C_b=0 remain. Whole records, labeled ideals, both newborns,
strict endpoints/restoration, 15 exact typed/raw boundaries and
423 unexpanded references remain. All original scientific routes
are closed; no body/hash/checker/JSON, new values, mathematical
engine, graph/vector/H/z, subject/measurement/RET, repository/Git/
index or publication. Stop at the sealed bounded author handoff.
