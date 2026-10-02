> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Exact supported compensation criterion

1 October 2026, OBSCURED-LOCATION. RI260 manual author result pending independent review.

The single-zero-xi family has a closed analytic criterion: require
all growing parent rows to be slack, then compare its baseline
gain with the least supported compensation cost. If the g companion
is slack that minimum is zero. If it is tight, the minimum is
attained by the cheaper available eta or sigma capacity source,
with all mixtures retained when their unit prices tie.

Every feasible primary tie lowers the original lex selector.
Therefore equality at the cost threshold excludes a canonical
branch as well. These are exact statements for this family,
not a global canonical characterization or actual data evaluation.

## Feasible rates and attained minimum

Use SINGLE_ZERO_CIRCULATION.md notation and its exact one-zero
support assumption: kappa>0, xi_g=0 and the other three xi positive.
Keep its joint marked-parent condition H_parent and all finite
bounds. Put

    b_g=p n_-/v,
    A_eta=v h/32,
    C_sigma=7v bar_s/240,
    G=p(Delta_n+3n_g)/240>0.                            (S1)

Eta rate a and sigma rate c are nonnegative and must vanish when
their respective current allocations vanish. These availability
conditions concern actual unknown support, not assigned values.

If S_g>0, there is no companion rate inequality. Since both
prices are strictly positive, the unique least-cost pair is

    a=c=0,   M_g=0.                                    (S2)

The positive g slope b_g is allowed: its actual finite bound
S_g/b_g remains. Requiring nonpositive g slope in this branch
would incorrectly exclude feasible strict descents.

If S_g=0, feasibility instead requires

    h a+s_g c>=b_g.                                    (S3)

If neither compensator is available, no rate pair satisfies (S3);
define M_g=+infinity. Otherwise define the available unit prices

    rho_eta=A_eta/h=v/32         if eta_(i,ell)>0,
    rho_sigma=C_sigma/s_g
                =7v bar_s/(240s_g) if sigma_i>0.       (S4)

Let rho_* be their finite minimum. For every supported feasible pair,

    A_eta a+C_sigma c
       >=rho_*(h a+s_g c)>=rho_* b_g.                  (S5)

A cheapest available pure rate attains the lower bound:

    (a,c)=(b_g/h,0) for cheapest eta;
    (a,c)=(0,b_g/s_g) for cheapest sigma.               (S6)

Both are finite because every denominator is positive, and their
decreased allocation is positive by availability. The complete
finite-step construction then supplies an actual positive u under
H_parent. No hypothetical arbitrary-rate limit is required.

When both sources are available with equal unit price, ALL
nonnegative pairs with h a+s_g c=b_g attain the same minimum.
This is the full tie segment, including its pure endpoints.
With unequal unit prices, only the cheapest pure pair minimizes:
any positive expensive contribution or any oversupply makes (S5)
strict. The same argument covers a single available source.

Thus the exact attained tight-row minimum is

    M_g=b_g min {available rho_eta,rho_sigma}.          (S7)

Unavailable rates are omitted, not treated as free zero-cost
options. The convention for an empty available set is infinity.

## Equivalent normalized threshold

For a tight g companion, (S7) is equivalently

    M_g=(p/240)K_g,

    K_g=min {
       (15/2)n_-       if eta_(i,ell)>0,
       7n_-bar_s/s_g   if sigma_i>0
    },                                                 (S8)

again with empty minimum infinity. Hence the finite non-worsening
cost threshold is simply

    K_g<=Delta_n+3n_g.                                 (S9)

The costs still include every Q history for eta and every companion
history for sigma; the cancellation of common positive p,v,h in
(S8) does not delete their positivity from the reconstructed rates
or the finite step bounds.

There are exactly four support possibilities: neither rate is
available (infeasible tight-g compensation), eta only, sigma only,
or both with the lesser displayed price. If the two prices tie,
all exact-coverage mixtures attain the same result; mixing cannot
beat the lesser price. No generic solver, sampling or case engine
is involved.

## Original lex selector at primary equality

The only increasing coordinates in the WHOLE direction are tau_i
and BOTH nu_(i,j). RI258's accepted complete structural proof puts
each after kappa_i in the actual component ordering. It covers the
P and P_nu presentations of each compulsory nu marking, not just
one of the two nu coordinates.

Kappa decreases strictly since n_->0 and u>0. The three nonzero
xi also decrease, and any used eta or sigma compensator decreases.
Xi_g and all unlisted coordinates are fixed. Thus if an additional
decreasing coordinate precedes kappa, the first change is that
decrease; otherwise the first change is decreasing kappa. Every
increase is later. No unknown exact rank or earlier fixed coordinate
can reverse this sign.

Accordingly EVERY feasible exact primary tie in this family is
a strict improvement of the original sequential lexicographic
selector. The former only-tau-increases shortcut is not used.
The argument checks all increases and all possible earlier decreases.

## The exact family iff

Under the one-zero support assumption (Z1), the following are
necessary and sufficient:

    a strict primary descent in this family exists
        iff H_parent and M_g<G;

    a strict primary OR primary-tie lex descent exists
        iff H_parent and M_g<=G.                       (S10)

If g is slack, use M_g=0 from (S2); if tight, use (S7), including
infinity for unavailable compensation. In either case the complete
u minimum in the companion note is retained.

For sufficiency, choose the attained minimizing pair. It is
supported and satisfies the tight-row requirement when necessary.
H_parent and the finite-step theorem supply positive u. The
exact primary change u(M_g-G) has the required sign; at equality
the preceding structural proof gives strict lex descent.

For necessity, any improving step must satisfy every support and
marked-parent feasibility condition. Its rate cost is at least
M_g. A primary improvement therefore needs M_g<G; a primary tie
or improvement needs M_g<=G. A positive primary cost cannot be
repaired by an earlier lex decrease because the primary objective
has priority. This proves both directions, not just a sufficient ray.

## Canonical binding and support obstruction

At the actual canonical point with (Z1), absence of the forbidden
direction forces at least one of

    some carrying P_nu,g row is tight;
    Delta_n>0 and some larger-n P row is tight;
    the g companion is tight and M_g>G.                (S11)

The final alternative permits M_g=+infinity. If all relevant
parent rows are slack and g is tight, the stronger strict
inequality K_g>Delta_n+3n_g is mandatory. Equality would already
contradict the original lex selector.

If g is slack, no compensator is needed and the family gives
strict descent whenever H_parent holds. RI256 already proves
the stronger standalone fact that ANY slack companion at a
primary optimum forces its own P_nu group to bind, even for
zero xi. This packet preserves that result; it does not count
the slack-g restatement as a new exclusion. The new compensation
criterion addresses the TIGHT zero-xi obstruction and its ties.

A concrete new subcase appears when n_0=n_1=n and g is tight.
Then n_g=n, G=pn/80, and available eta alone costs pn/32>G.
An available sigma yields cost at most G exactly when

    s_g>=7bar_s/3.                                     (S12)

Consequently in this equal-n tight-g branch, (S10) reduces to

    all four P_nu,g rows slack,
    sigma_i>0, and s_g>=7bar_s/3.                       (S13)

These conditions are jointly necessary and sufficient for a
primary-or-tie lex descent in THIS family. Eta availability does
not change that conclusion: its price is already above G and
mixing cannot undercut sigma. Strict inequality in (S12) gives
strict primary descent; equality gives the lex descent.
No larger-P slack condition exists at equal n.

Thus an actual canonical candidate in this stated branch with
positive sigma and (S12) must have a binding P_nu,g row. This is
a newly excluded compensated sparse-support subcase, not an
assertion that its support, s comparison or slacks actually occur.
If the threshold fails or a parent binds, only this family is blocked.

## The zero xi reduced cost must remain an inequality

For an additional necessary ORIGINAL full-dual relation, use
RI258's marked aggregates: A_L is P dual mass in block L,
B_LM is companion dual mass at pair (L,M), B_L=sum_M B_LM,
and N_LM is the complete P_nu dual mass at that pair. Let
B_g,N_g denote the special pair.

Positive kappa and Y slack still give

    A_0+A_1=3p/80,
    r_tau=p(B_0+B_1-7v/240)>=0.                        (S14)

Let e_0,e_1>=0 be the two ORIGINAL nu reduced costs from RI258.
Each is zero if its nu allocation is positive, but not otherwise
assumed zero. Each of the three positive xi has its usual equality.
For the zero xi, however, retain

    r_g=-v n_g/80+n_g B_g+v N_g>=0.                    (S15)

This is a full original column inequality, not a new free price.
For all four pairs at once, with r_LM=0 away from g,

    N_LM=n_L/80-(n_L/v)B_LM+r_LM/v.                   (S16)

Substitute these into the sum of the two full nu reduced costs.
For unequal n the exact identity becomes

    Delta_n[A_+-(p/v)B_+-p/240]+(p/v)r_g
                         =(n_-/v)r_tau+e_0+e_1.       (S17)

The new nonnegative r_g term is essential. Solving for A_+ has
a NEGATIVE contribution -p r_g/(v Delta_n), so RI258's
all-positive-xi lower bound cannot simply be copied into this
one-zero branch.

At equal n use the identity without division:

    (p/v)r_g=(n/v)r_tau+e_0+e_1.                       (S18)

It no longer forces tau and both nu reduced costs to zero,
unless r_g=0 is separately established. Zero xi does not imply
zero r_g; assuming that equality would erase the actual support
obstruction.

For completeness the compensator reduced costs retain every
original carrying parent:

    r_eta=-A_eta+h(B_ell,0+B_ell,1)+v Q_ell>=0;

    r_sigma=-C_sigma+sum_(L,M)s_LM B_LM
                    +sum_(V5 records) gamma_i(record)z_V5>=0,
    gamma_i=(v/40)[1_(first minimum bit=i)
                              +1_(second minimum bit=i)]. (S19)

Q_ell sums every carrying marked Q dual. Sigma's two V5 singleton
occurrences are both counted. Supported decreases imply
a*r_eta=c*r_sigma=0 by original coordinate complementarity,
including a zero rate on an unavailable allocation. All other
original dual rows and columns remain; none of (S14)-(S19)
constructs a sufficient full dual certificate or actual dual vector.

## Positive Pnu price at the sigma threshold

Within the standing one-zero branch, suppose sigma_i>0 and
s_g>=7bar_s/3. Then the original full dual must have N_g>0,
REGARDLESS of the n contrast or whether a larger-n P row binds.

For contradiction take N_g=0. The retained zero-xi inequality
(S15), with n_g>0, gives B_g>=v/80. Positive sigma makes its
COMPLETE reduced cost in (S19) zero. Therefore

    C_sigma=s_g B_g
          +sum_(other pairs)s_LM B_LM
          +sum_(V5 records)gamma_i(record)z_V5
       >=s_g B_g>=7v bar_s/240=C_sigma.

All terms are nonnegative and every other s_LM is positive.
Equality throughout forces s_g=7bar_s/3, B_g=v/80 and every
other companion aggregate zero. The total B is then v/80,
contradicting (S14)'s lower bound 7v/240. Thus N_g>0.

At least one of the four actual P_nu,g rows is consequently
positively priced and tight; no particular marking or positive
xi allocation is inferred. This necessary full-dual consequence
strengthens the displayed equal-n sparse exclusion and remains
valid even if the larger-P cap already blocks the chosen ray.
It does not change the within-family iff (S10), assert an actual
s comparison, or turn its blocked cases into global optimality.


## Exact remaining limits

The minimum and finite-step theorem resolve this entire assigned
two-rate family, including slack-g, unavailable compensators,
ties, equal n and every original marked parent bound. They do
not decide actual canonical support, s or n comparisons, full
residual compatibility, the zero-xi reduced cost, kappa gap or C_b.
A blocked family is not global optimality.

All original 13 equations/10 coordinates, u2=-1, offsets/selector,
complete recovery, accepted d=0!=d7 and full-system existence iff
actual C_b=0, records, ideals, newborns and strict endpoints remain.
All 15 typed/literal boundaries and the 423 manifest references
remain unchanged. All original literal authorities stay closed.
No new body/hash/checker/scientific JSON, coefficient/support
acquisition, mathematical engine, reconstruction, subject execution,
measurement/RET, repository/Git/index, publication or successor.
Stop for independent root adjudication.
