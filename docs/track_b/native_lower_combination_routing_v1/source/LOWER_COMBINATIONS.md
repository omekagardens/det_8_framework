# Exact lower combinations and the exceptional canonical component

30 September 2026, Honolulu. RI228 source-only author result for independent
review. All new statements are conditional on the same accepted finite
baseline; the normalized H30 improvement-versus-optimality decision is open.

The new construction-level identity is

    beta_S=theta*alpha_S       for every S in J,              (L1)

where J contains all four C3 stem ideals. Thus the six formerly separate
strict-prefix ratios reduce to three fixed actual ratios. The exceptional
isolate-containing singleton is not covered by(L1). Its exact form is

    zeta_i=(35/36)*gamma_i*kappa_i,       i=0,1,               (L2)

with kappa_i the unchanged RI63 canonical boundary coefficient in the
precisely identified component below. It follows that zeta_i>=0, but
neither kappa_i nor zeta_i is assigned a value. Locating this component
is not a proof that the canonical optimizer gives it positive mass.

## 1. Accepted notation and complete Y row

Use RI225's I=C3, K=I disjoint {o}, Y=C4 disjoint {o}, and
the stem ideals S=empty,{r},{r,a},I with chain r<a<b<c in Y.
The notation is unchanged:

    k_S=q(K,S)=alpha_S*A_S,
    y_S=q(Y,S)=beta_S*B_S,
    k_S^+=q(K,S union {o}),  y_S^+=q(Y,S union {o}),
    gamma_i=k_{ {r} }^+,
    zeta_i=y_{ {r} }^+-theta*gamma_i.

A_S and B_S are the complete C3/C4 held rows restricted to these
precursors; their records are transported, not averaged. The isolate
record is removed from the value only by the accepted maximal-record
invariance theorem.

Y has precisely nine proper ideals: the five C4 ideals excluding o,
and S union {o} for all four S in J. Its sole full ideal is Y.
No individual slot is merged or dropped in what follows.

RI63 COMPLETION gives the actual size-five coefficient explicitly as

    actual coefficient=(35/36)*canonical coefficient+theta,
    theta=c5/36, c5=1/[2(1+M5)]>0.                          (L3)

Every active canonical component is everywhere defect-neutral.
Therefore a component containing even one raising role has canonical
coefficient zero. A neutral role by itself need not have a positive
or zero canonical coefficient.

## 2. All five no-isolate Y slots have zero canonical coefficient

For a stem ideal S, the omitted Y maxima are c and o. Its
maximal-deletion potential is

    u(Y,S)=B_S*k_S/A_S=alpha_S*B_S.                         (L4)

We now prove that its actual coefficient is theta, retaining the
case where the Y role itself is neutral.

For S=empty, the terminal is C4 disjoint A2. It has defect two:
deleting either isolate leaves C4 disjoint A1, and deleting a
chain vertex still leaves both isolates. None has a unique minimum,
whereas a nonempty Ferrers cell order does. Deleting both isolates
leaves C4. Since Y has defect one, this slot is raising.

For S={r,a} or I, the terminal is a non-Ferrers branched five-event
connected order disjoint {o}. Deleting o leaves incomparable tops
with chain principal ideals sharing respectively two or three stem
vertices, violating the accepted Ferrers-cell obstruction. Any other
single deletion leaves a nonempty connected-part remainder disjoint
from o. Deleting o and the newborn restores C4. Again the slot
raises defect one to two.

For S={r}, the Y role is neutral, so that argument would be invalid.
Let Hhook be C4 plus a new branch x above r. This five-event hook
is a Ferrers cell order. Its empty birth has terminal Hhook disjoint
{o}, of defect one: deleting o restores Hhook, while the terminal
has more than one minimum. That empty role is raising from zero to one.

The full marked diamond based at C4 with precursors {r} and empty
connects exactly this raising hook-empty role to the Y role at {r}.
Retain all C4 marks, both newborn bits and both ordered pairs.
The positive maximal-deletion potential satisfies the same ratio
identity, so division identifies the two component coefficients.
The raising hook role forces the component's canonical coefficient
to zero, including its neutral Y role. This also explains why
RI63's admitted all-record zero hook component is relevant without
guessing an ordinal component index.

The fifth no-isolate ideal is the entire C4. Its Y role connects,
by the complete empty/full diamond based at C4, to empty birth
from C5. C5 is a Ferrers chain and its empty terminal C5 disjoint
A1 has defect one. That raising role again makes the canonical
component zero. Equivalently its probability is the accepted
q(Y,C4)=theta*c.

Thus all five no-isolate proper probabilities are theta times
their original deletion potentials. For S in J, (L4) and
positive B_S give beta_S=theta*alpha_S, proving(L1), including
the neutral singleton case. Nothing has been substituted for a
full probability or for the exceptional with-isolate singleton.

## 3. The exceptional component and all of its presentations

RI225 already proves y_S^+=theta*k_S^+ for S=empty,{r,a},I:
those three with-isolate Y births raise defect one to two.
Together with section2, only the fourth with-isolate slot,
at precursor {r,o}, can carry canonical proper mass in Y.

Its terminal after birth x is

    Tstar: r<a<b<c,   r<x,   o<x.

There are only two maxima, c and x. The complete parent presentations
are

| Deleted newborn | Five-parent | Selected precursor |
| --- | --- | --- |
| x | Y=C4 disjoint {o} | {r,o} |
| c | P with r<a<b, r<x, o<x | {r,a,b} |

In original natural labels these may be represented as

    Y: (0,1,3,7,0), precursor mask17,
    P: (0,1,3,0,9), precursor mask7.

These are literal representatives, not assumed canonical root keys
or certificate indices. No other presentation can enter the component
because every newborn is maximal and both maxima are listed.

The common size-four base is K=r<a<b disjoint {o}. Its two birth
precursors are {r,a,b} and {r,o}. At fixed root bit i, the selected
o mark on the Y side has two values and the two extra selected chain
marks on the P side have four values. Each Y local node connects to
each P local node by the complete marked diamond, with all independent
base marks and both newborn bits retained. The two ordered precursors
are both included.

Their common compulsory selected vertex is exactly r. It is intrinsically
distinguished by the longer terminal branch. Its bit cannot change along
a ratio edge or marked isomorphism. Thus there are exactly two complete
components, one for each root bit, with no further selected-record sector.
Call their original canonical boundary coefficients kappa_0,kappa_1.

The Y potential at {r,o} is gamma_i by unique omitted-maximum deletion.
Equation(L3) then gives

    y_{ {r} }^+=gamma_i*(theta+(35/36)*kappa_i),

which proves(L2). This retains the canonical term in the actual law;
it does not replace that law by its boundary optimizer.

## 4. Native signs do not determine the canonical allocation

The exact canonical program in the admitted RI63 text has kappa_i>=0.
Since gamma_i>0, (L2) yields zeta_i>=0 and

    zeta_i=0 if and only if kappa_i=0.                       (L5)

In the canonical Y row every other proper slot is zero by section2
and the accepted three raising-slot identities. The only proper
mass is gamma_i*kappa_i. Complete row feasibility therefore gives

    0<=gamma_i*kappa_i<=1,
    0<=zeta_i<=35/36.                                      (L6)

The proved bound gamma_i>=1/64 in
[COMPONENT_ROUTING.md](COMPONENT_ROUTING.md) also gives kappa_i<=64.
Neither upper bound is asserted to be attained.

A further native sign can be proved without running the optimizer.
The component's role is neutral at both Y and P: each parent has
defect one, and deleting o from Tstar leaves the Ferrers hook with
four-chain long arm, so Tstar also has defect one.

Full birth at Y is neutral. Its terminal still has two minima, and
deleting o leaves a chain, so its defect remains one.

Full birth at P is raising. Write t for its new full maximum.
Deleting any vertex other than r or o leaves both minima. Deleting
r leaves a and o as two minima. Deleting o leaves the five-element
order r<a<b<t, r<x<t. This is not Ferrers: a Ferrers cell order
with a unique maximum is a rectangle, and a five-cell rectangle
is a chain, whereas this order has incomparable a and x. Deleting
both o and x does leave r<a<b<t, so the full terminal has defect
exactly two, not just a lower bound.

There are no other parent roles in this component. Consequently
RI63's objective coefficient is

    cost_i = -sum_(marked P rows in sector i)
                       pi_row*u_P({r,a,b}) < 0.             (L7)

The Y contributions are zero because their proper and full increments
are both zero. Every P contribution is negative because its proper
increment is zero and its full increment is one. Actual history
weights and potentials are strictly positive, and these P rows exist.
All marked-class multiplicities in the original objective remain;
no uniform history weighting is substituted.

Equation(L7) does NOT imply kappa_i>0. A coupled optimum can leave
a negative-cost component at zero because other components consume
its incident row capacity. RI63 explicitly supplies a negative-cost
hook component with zero canonical allocation. Nor does(L7) imply
that kappa_i reaches the upper bound in(L6). The exact canonical
values require their actual coupled optimal-face selection.

## 5. All lower combinations after the new identities

Retain the complete four-term stem sums, the held notation of RI225,
m=h^2/c=theta^2*c, nu=h^3/c^2, and the unchanged fixed rho,s.
Using beta_S=theta*alpha_S, its lower combinations become

    V_H=theta^2*sum_S alpha_S*G_S+2m+j,
    V_C=theta*sum_S alpha_S*D_S+theta*e+ell,

    R1=theta^3*sum_S alpha_S*A_S*G_S^3/B_S^3,
    R2=theta^2*(sum_S alpha_S*D_S*G_S/B_S+e),
    R4=theta*(sum_S alpha_S*D_S^2/B_S+e^2/c),

    P_Y=1-theta*(sum_S alpha_S*B_S+c),
    T=1-sum_S alpha_S*A_S.                                 (L8)

T remains the positive record-independent complete K mass on
precursors containing o. Define chi_i=(35/36)*kappa_i, so
zeta_i=gamma_i*chi_i. Then the two higher moments and full Y slot
are exactly

    M2=theta^2*T+gamma_i*(2theta*chi_i+chi_i^2),
    M3=theta^3*T+gamma_i*(3theta^2*chi_i
                                  +3theta*chi_i^2+chi_i^3),
    F_Y=1-theta*(sum_S alpha_S*B_S+c+T)-gamma_i*chi_i.        (L9)

These are exact hand substitutions into the accepted RI225 identities.
The zero-kappa branch is retained. All sums keep S=empty as well
as both proper nonempty prefixes and I. No empty or full ideal is
discarded just because its coefficient is record blind.

The complete proper potential at Y is

    U_Y=sum_S alpha_S*B_S+c+T.

It satisfies U_Y<=M5, with the same global M5 used in RI63.
Thus theta*U_Y<1/72 by theta=1/[72(1+M5)], without evaluating M5.
Equations(L6),(L9) then recover the strict full margin

    F_Y=1-zeta_i-theta*U_Y >1-zeta_i-1/72 >=1/72.            (L10)

This is a check on the unchanged actual mixture, not a new
half-mass condition on the repaired H30 law.

For explicit use, the accepted five disconnected profiles remain

    X=V_H+2F_Y+M2,       Z=V_C+P_Y,

    B1=4-rho*(E1+3X)+3rho^2*(j+F_Y)
                                +rho^3*(3nu+M3)+rho^4*R1,
    B2=3-rho*(E2+X+Z-F_Y)
                     +rho^2*(m+j+ell+F_Y+M2)+rho^3*R2,
    B3=2-rho-rho*(1-rho)*V_H,
    B4=3-rho*(E4+2Z)+rho^2*(2ell+P_Y)+rho^3*R4,
    B5=2-rho-rho*(1-rho)*V_C,
    g_i=1-s*B_i.                                           (L11)

E1,E2,E4 and every individual ideal occurrence are exactly those
already accepted in RI225. The 81 proper and five full ideal
occurrences, all records and both fair newborn bits remain binding.
Equations(L8)-(L9), not selected new coefficient values, are what
this sitting adds to(L11).

## 6. The exact normalized witness gap remains

Let l_i=L_i/rho be the original five shared linear forms.
For every original record their relative equations remain

    (1-s*B_i(0))*Delta l_i(W)
                         +s*Delta B_i*l_i(0;W)=0.           (L12)

Keep the accepted recovery with u2=-1,

    W1=-Gamma_10*u0+Gamma_12-Gamma_13*u3,
    W2=Gamma2>0, W3=-Gamma3*u3, Wj=Uj for j>=4,

and all eight connected conditions Uj*Delta f_j=0, j=4,...,11.
The full-child corrections are still recovered by the original
N12 formulas with positive reference denominators. They are not
independent fits. Constant f8,f11 retain their freedoms subject
to every(L12); no other Uj is set to zero here.

No tuple for all ten remaining unknowns or finite signed row
inconsistency identity has been established. The positive signs
and bounds above are not sufficient by themselves to declare
one. Actual improvement, ceiling optimality and maximal amplitude
remain open.

The newly exposed lower coefficient premise is now concretely:

- The three RI41 coefficients at(2,3,0),(6,3,0),(70,3,0),
  together with the preexisting alpha_I at(70,7,0).
- The two RI41 coefficients at(70,9,i), i=0,1, with exact
  potential multiplier1/8.
- The two RI63 canonical coefficients of the complete Tstar
  components described in section3, through chi_i=(35/36)kappa_i.

Only combinations(L8)-(L9) need be controlled for this lower-profile
route; exact coordinate values are not necessarily required if a
same-source identity or bound suffices for the full row witness.
This is a specified remaining premise, not a claim of global
information-theoretic minimality or analytic nonderivability.

The two newly admitted construction manuscripts give the actual
coefficient definitions, prefix potentials, global margins and
canonical feasibility. They do not state the assigned values at
these new roots or the two kappa components. Their references to
certificates, checkers and discovery do not authorize opening those
bodies, computing their coordinates, importing an optimizer, or
assuming a default at an unresolved root. No such action is taken.

All previously admitted fixed lower quantities, actual rho/s,
canonical q/N terms, shared T1/T2/T3 conditions, other eight connected
parents, five disconnected families and strict endpoints remain.
The original amplitude1/4 rejection and the accepted small-amplitude
family are unchanged.

## 7. Source scope and bounded handoff

The new results are the complete no-isolate zero-canonical proof,
beta=theta*alpha, exact size-four component routing and multipliers,
the exceptional two-parent component, its native negative-cost proof,
the sign/bounds for zeta and the simplified lower combinations.

They are conditional finite mathematical deductions, not DET-selected
physical laws, informative quantum dynamics, geometry or gravity.
The scalar quantum payload remains in the inherited whole maps.

Sources are the two exactly admitted RI41/RI63 construction notes,
the accepted RI225 proofs/root review, renewed RI189 routing,
and inherited literal analytic identities as bound in
[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json). No descendant
source, scientific body/vector/certificate, new numerical amplitude,
automatic mathematical arithmetic, graph/LP/runtime/fixture/card,
H/z reconstruction, repository/Git/index, measurement or RET work
occurred. No successor or source expansion is started.

Stop at this substantive native lemma and precise remaining full-
system gap for independent adjudication. Root owns publication,
Git and any subsequent authorization.
