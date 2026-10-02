> Public redacted derivative. The prose below records historical research and review; local paths, private file fingerprints and execution identifiers have been obscured. Raw custody, host/runtime logs and administrative scripts are withheld. Claims about exact copies, complete transcripts, byte identities, manifests or execution permissions describe the private original archive, not this derivative. Only the new PUBLICATION_MANIFEST.json hashes verify the redacted payloads. This copy grants no execution authority and cannot replay original custody checks.

# Circulation with one zero xi allocation

1 October 2026, OBSCURED-LOCATION. RI260 manual author result pending independent review.

Omitting the forbidden decrease of the single zero xi leaves four
P_nu rows growing. They must all have genuine positive slack.
The larger-n P rows retain their separate slack requirements.
Eta and sigma compensation can repair a tight zero-xi companion,
but is unnecessary when that companion is already slack.

This note proves every finite-step constraint and the complete
history-weighted cost. SUPPORTED_CRITERION.md solves the supported
two-rate minimization and the primary-equality lex endpoint.
All results concern this fixed direction family, not a global
canonical solution, actual support evaluation or C_b decision.

## Fixed sector and the single zero support branch

Work in the unchanged original canonical problem. Fix root i and
one pair g=(ell,m_g). Assume

    kappa_i>0, xi_g=0,
    xi_(i,L,M)>0 for the other three pairs (L,M).        (Z1)

Abbreviate only already admitted positive lower probabilities

    p=p_i, v=v_i, h=h_(i,ell), n_L=n_(i,L),
    n_g=n_ell, s_g=s_(i,ell,m_g), a0=41/352,
    n_-=min(n_0,n_1), n_+=max(n_0,n_1),
    Delta_n=n_+-n_->=0,
    bar_s=(s_00+s_01+s_10+s_11)/4>0.                   (Z2)

Delta_n is not the inherited hook correction d. No n or s value,
support indicator or canonical coordinate is acquired or assigned.

The complete original rows and all residuals are those admitted
in RI248 and retained in RI258:

    C_P(i,j,k,L,M)=a0 kappa_i+t(record)mu_(i,L)
                                     +v tau_i+n_L nu_(i,j),

    C_tau(i,j,L,M,t)=p tau_i+h_L eta_(i,L)
                         +n_L xi_(i,L,M)+s_LM sigma_i,

    C_nu(i,j,L,M,k)=B_nu(record)+p nu_(i,j)+v xi_(i,L,M),
    C_Q(i,L,other marks)=B_Q(record)+v eta_(i,L).        (Z3)

Every row is at most one. B_nu excludes the two displayed terms;
B_Q excludes its displayed eta term. Each contains ALL other
original proper contributions, held fixed under this direction.
The positive lower t(record) is not assumed constant. Its symbol
is distinct from the companion's final record bit t.

The four marked companion rows at fixed pair (L,M) have the same
coefficient mass and slack by accepted transport, but retain all
four history contributions. The four P_nu rows at that pair are
kept individually; their residual slacks are not identified.

## The supported two-rate direction

For finite a,c>=0 and u>0, change only

    Delta nu_(i,0)=Delta nu_(i,1)=u,
    Delta tau_i=n_-u/v,
    Delta kappa_i=-2n_-u/a0,

    Delta xi_(i,L,M)=-p u/v for (L,M)!=g,
    Delta xi_g=0,

    Delta eta_(i,ell)=-a u,
    Delta sigma_i=-c u.                                (Z4)

The other eta and every other original coordinate are fixed.
The rates are local direction parameters, not new law parameters
or the earlier normalized-system coefficients with similar names.

A positive rate is allowed only on positive current allocation:

    a>0 => eta_(i,ell)>0;
    c>0 => sigma_i>0.                                  (Z5)

If a compensator allocation is zero its rate is zero. No minimum
positive rate is imposed. The original complete terminal components
make all the named coordinates distinct, including both nu marks.

## Exhaustive slopes on all carrying parents

Direct substitution into every original marked row gives

    Delta C_P(i,j,k,L,M)=(n_L-n_-)u;
    Delta C_Y=-n_-u/(32a0);

    Delta C_tau(i,j,L,M,t)/u
       =-(p/v)(n_L-n_-)
          +(p n_g/v)1_((L,M)=g)
          -h a 1_(L=ell)-s_LM c;

    Delta C_nu(i,j,L,M,k)=p u 1_((L,M)=g);

    Delta C_Q(i,L,other marks)=-v a u 1_(L=ell).       (Z6)

Every V5 record with its two minimum bits b,d has

    Delta C_V5=-(v/40)c u[1_(b=i)+1_(d=i)].             (Z7)

Both singleton occurrences are retained, including a factor of two
when both minima have bit i. V5 may involve another root sector,
but every occurrence of the changed sigma_i is included in (Z7).
P_mu and every other original row are unchanged.

For the zero-xi companion, write its slope per u as

    L_g=b_g-h a-s_g c,   b_g=p n_-/v>0.                (Z8)

Every other companion slope in (Z6) is nonpositive. Q and V5 relax
or stay fixed. The nu/xi cancellation still holds on EACH P_nu
row away from g. At g the fixed zero xi cannot supply that
cancellation; all four (j,k) rows have strictly positive slope p,
regardless of a,c. No eta/sigma decrease enters those rows.

Thus the only possible positive row slopes are the four P_nu,g
rows, the eight larger-n P rows when Delta_n>0, and the four
equivalent g-companion rows when L_g>0.

## Complete finite feasibility and the slack companion distinction

Write the ACTUAL complete row slacks as

    S_nu,g(j,k)=1-C_nu(i,j,ell,m_g,k);
    S_P(j,k,L,M)=1-C_P(i,j,k,L,M);
    S_g=1-C_tau(i,j,ell,m_g,t).                         (Z9)

Let H_parent denote the following joint condition:

    all four S_nu,g(j,k)>0;
    if Delta_n>0, all eight S_P(j,k,l_+,M)>0,
       where l_+ is the unique larger-n block.         (Z10)

No larger-block condition is imposed when the two n values coincide.

Under (Z1), for a chosen finite a,c>=0 a positive step in (Z4)
exists iff (Z5), (Z10), and

    S_g=0 => h a+s_g c>=b_g                           (Z11)

hold. If S_g>0, (Z11) imposes NO restriction. In particular a=c=0
is then feasible for a sufficiently small u despite L_g=b_g>0.

The entire positive-step upper bound is the minimum of

    a0 kappa_i/(2n_-);
    v xi_(i,L,M)/p for all three pairs other than g;
    eta_(i,ell)/a if a>0;
    sigma_i/c if c>0;
    S_nu,g(j,k)/p for ALL four j,k;
    S_P(j,k,l_+,M)/Delta_n for ALL eight rows
                                           if Delta_n>0;
    S_g/L_g if L_g>0.                                 (Z12)

If L_g>0, (Z11) ensures S_g>0. No bound is divided by a zero
rate, zero contrast or zero slope. Every included bound is
strictly positive and finite under the stated conditions.
The always-present kappa bound makes the finite family nonempty.
Take any u through its minimum, including the closed endpoint.

All decreasing coordinates then stay nonnegative. Every growing
marked row remains at most one; all other rows relax or are fixed.
This proves sufficiency on the COMPLETE original problem.
Conversely, a violated support condition, any tight positive-slope
P_nu/P row, or a tight g row with L_g>0 forbids every positive u.
This proves necessity for the stated family.

A repeated companion coefficient row is not a discarded record;
its identical bound stands for all four occurrences. Distinct
P_nu and P residual slacks cannot be replaced by an average or by
nominal unused capacity. Original strict restoration and both
newborn bits remain distinct from closed canonical endpoints.

## Exact complete history cost

RI258 proved that the full four-xi circulation has cost per u

    -p Delta_n/240.

Relative to that algebraic direction, omitting the xi_g decrease
adds +p/v to the xi_g direction coefficient. This comparison is
only linear bookkeeping; the original four-xi ray is not claimed
feasible at xi_g=0.

RI254 derived the COMPLETE xi coefficient -v n_g/80. Thus that
omission changes cost by -p n_g/80, not by a guessed companion-only
quantity. Equivalently, its additional companion mass contributes

    -(7v/960)(p n_g/v)=-7p n_g/960,

and all four growing P_nu,g rows contribute

    -(n_g/192)p=-p n_g/192.

Together these are -p n_g/80, using actual original history masses.

The complete eta-decrease price from RI254 includes both companion
rows of its block AND every Q history:

    A_eta=v h/32.

The complete sigma-decrease price includes ALL four companion
coefficients, including any slack rows:

    C_sigma=(7v/240)bar_s.

V5 has zero full defect increment but retains its constraints and
multiplicity. No s_g-only substitute for bar_s is permitted.
Consequently the exact finite objective variation is

    Delta Phi=u[-G+A_eta a+C_sigma c],
    G=p Delta_n/240+p n_g/80
                         =p(Delta_n+3n_g)/240>0.       (Z13)

The baseline gain is strictly positive even at equal n. A compensator
can offset it, so support and cost must be solved together rather
than inferring descent merely from an omitted zero allocation.

## Original system and stopping boundary

SUPPORTED_CRITERION.md gives the attained minimum and an iff for
strict primary or primary-tie lex descent in this exact family,
including unavailable rates and the slack-g case. It also explains
the extra original reduced-cost inequality caused by zero xi_g.

No actual support, n contrast, slack, compensator cost, residual
maximum, full dual vector, kappa gap or C_b is evaluated. Keep all
13 equations/10 coordinates, u2=-1, complete original recovery,
actual offsets/selector, accepted d=0!=d7 and full-system existence
iff actual C_b=0. Whole records, labeled ideals, both newborns,
strict restoration/endpoints, all 15 typed/literal boundary objects
and the 423-source by-reference manifest remain.

All original scientific-body/hash/checker/JSON routes, including
RI250 GAP-INDEX, stay closed. No engine, coefficient/support
acquisition, graph/vector/H/z reconstruction, subject execution,
measurement/RET, repository/Git/index, publication or successor.
Stop at bounded handoff for independent root adjudication.
