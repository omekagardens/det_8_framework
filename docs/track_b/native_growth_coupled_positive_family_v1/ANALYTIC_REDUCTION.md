# RI117 — the coupled positive family, with exact open conditions

26 September 2026. External analytic manuscript for research-owner review.
No new executor, numerical evaluation, scale selection or active admission.

## Outcome

The accepted six zero minors imply a nonempty **local** positive T1
family with a genuinely free parameter. They do not settle the fixed
28-child extension. This note reduces the complete D1 equation and its
coupling to T2/T3, proves a necessary record-constancy alternative, and
classifies the remaining four-parent subsystem conditionally on its
fixed baseline profiles. All twelve other parent conditions are retained.

The actual fixed baseline's branch in this classification is not decided.
In particular no nonconstancy is inferred merely from permission to read
a record, from another profile's variation, or from a nonzero polynomial
that might vanish at the actual scale. No full positive repair is claimed.

## 1. Unchanged object and premises

Use RI111's actual baseline B, eleven-class seed z with z1=1,
all zj nonzero and |zj|<=1, amplitude epsilon=1/4, and exactly its
28 unmarked child classes: eleven Jj, sixteen full children F(P),
and Y0. The incoming parents are T1,...,T11 and D1,...,D5.
Every correction is shared by its child class, not chosen per parent
or per record. The complete record cubes and individual ideals remain.

Let I be the three-chain, K=I ordinal-sum A3, T1=I ordinal-sum A4,
and D1=K disjoint A1. The indexed six-parent orders C_i of RI85
are distinct notation from a chain Cn; C_1=K. Set

    e_j = q_B(Tj,empty)>0,       e_K=q_B(K,empty)>0,
    wj = e_j y(Jj),             vj=y(F(Tj)),
    di = y(F(Di)),              t=y(Y0),
    fj(r)=q_B(Tj,r,full),       gi(r)=q_B(Di,r,full).

Empty probabilities are record-blind. The actual positive half-scales
rho=a6 and s=a7 are unchanged and unevaluated. Full probabilities
fj,gi exceed 1/2 at this baseline; these bounds are not asserted at
arbitrary trial scales. The local/marked scalar-passive model premises
and complete whole-map diamonds remain assumptions, not new DET theorems.

The root RI115 adjudication accepts all six exact minors as identically
zero and leaves feasibility open. Together with the accepted saved signs
Delta_1 p<0, P1(0)<0 and the root-free pivot on (0,R], this supplies
the conditional premises used below. The historical 27-child rejection
and the fixed-amplitude signed-lift obstruction are not reversed.

## 2. Exact positive T1 family

Using RI111's held profiles, write

    beta = rho^3 Delta_1 p/P1(rho),
    Gamma = k0+f1(0) beta,          k_xi=q_B(T1,xi,I)>0.

Continuity, P1(0)<0 and no pivot root on (0,R] imply P1(rho)<0.
Hence beta>0 and Gamma>0 at the actual baseline. Subtraction of the
eight T1 equations yields

    rho^3 Delta_xi p t-P_xi(rho) v1=0.

The nonzero pivot forces v1=beta t. Each other row follows from its
accepted zero minor, so k_xi+beta f1(xi)=Gamma for all eight records.
Consequently the **entire** T1 affine family is

    w1=lambda,   t=(1-lambda)/Gamma,   v1=beta(1-lambda)/Gamma.       (1)

Let R_xi=q_B(K,xi,I)/e_K>41 and q_xi=q_B(D1,xi,I). The accepted
empty/ordinary diamond gives q_xi=R_xi e_1. Define

    W*=min_xi 4(1-q_xi)/R_xi
      =4/max_xi R_xi-4e_1,        0<W*<4/41<1.

The T1 equations, positivity of its three affected children, and all
eight necessary D1 core-slot bounds are equivalent to

    -4e_1 < lambda < W*, with (1).                                (2)

Indeed the lower endpoint is J1 positivity; the upper endpoint makes
t and v1 strictly positive and enforces every slot bound. Conversely
the original subsystem forces both endpoints and (1). Zero lies in
this interval, but it is only a local witness, not a prescribed choice.
No old 27-child necessity for v1 is silently transferred: its new sign
has just been proved from the accepted signs and zero minors.

The complete proof and endpoint transport are in T1_LEMMA_REVIEW.md.

## 3. D1 retains seven supported individual slots

For each of the eight stem records xi, let

    a_core,xi = a_xi g_xi^3/b_xi^3,
    m_xi = h_xi^2/c_xi,           j_xi=q_B(H5,xi,full)>0,

using RI111's positive C3/C4/H5 held values, H5=I ordinal-sum A2.
The exact supported ideals of K, retained separately in D1, are

| Masks | Child | Number of individual ideals | K probability per ideal |
| --- | --- | ---: | --- |
| 7 | J1 | 1 | rho a_core |
| 15,23,39 | J2 | 3 | rho m |
| 31,47,55 | J3 | 3 | rho j |

Thus L1=rho(a_core w1+3m w2+3j w3). The accepted harmonic identity
a_core+3m z2+3j z3=0 holds at each record. Put

    x=w2-z2 lambda,   y=w3-z3 lambda,   delta=e_K d1/(3rho),
    theta_xi=m_xi/j_xi,                eta_xi=g1(xi)/j_xi.

Since all divisors are positive, the complete D1 row is equivalent to

    theta_xi x+y+eta_xi delta=0 for xi=0,...,7.                    (3)

It is not permissible to infer delta=0 from nonconstant g1 alone.
The other terms can vary together with it. Equation (3), plus
delta> -4e_K/(3rho), includes precisely D1's full correction positivity.
The shared J-child positivity is enforced separately, not discarded.

### Complete zero-safe algebraic classification

Eliminate only y, giving y=-theta_0 x-eta_0 delta and

    Delta_xi theta x+Delta_xi eta delta=0, xi=1,...,7.             (4)

There are exactly four cases:

1. Both theta and eta constant: x and delta are free; recover y as above.
2. Theta constant and eta nonconstant: delta=0, x free, y=-theta_0 x.
3. Theta nonconstant and eta affine in theta: choose a proved nonzero
   contrast Delta_p theta and put kappa=Delta_p eta/Delta_p theta.
   If Delta_xi eta=kappa Delta_xi theta for every xi, then
   x=-kappa delta and y=(theta_0 kappa-eta_0)delta, with delta free.
4. Theta nonconstant and the affine condition fails: x=delta=y=0.

Proof: when theta is constant (4) gives the first two cases. Otherwise
the selected nonzero pivot yields x=-kappa delta. Substituting in every
remaining equation gives (Delta eta-kappa Delta theta)delta=0.
This proves both directions in cases 3 and 4, including kappa=0.
Lambda remains free subject to (2) and the connected/positivity tests.
No numerical branch of the fixed baseline is selected by this theorem.

## 4. Connected sensitivity is a condition to prove

For j=2,3 the complete connected equation is exactly

    (zj-wj)[fj(r)-fj(0)]=0 for every record,
    -4e_j<wj<zj+4fj(0),        vj=(zj-wj)/fj(0).                 (5)

A nonconstant fj forces wj=zj. A constant fj leaves an interval, not
that equality. CONNECTED_CONSTRAINTS_LEMMA.md supplies full individual
ideal derivations for the fourteen T2 and twelve T3 proper ideals:

    f3(xi)=1-s[2-rho-rho(1-rho)V_xi],
    V_xi=E_xi-m_xi-2j_xi,

    f2(eta)=1-s[3-rho A2_eta+rho^2 B2_eta+rho^3 C2_eta].           (6)

Here eta in (6) is the sixteen-record index, not the positive D1 ratio
eta_xi of (3); they never occur in the same equation. The connected
lemma defines all held expressions and transports the formulas to
the full record cubes. Equivalently f3 is constant iff all eight V
values agree, and f2 is constant iff all fifteen polynomials

    Q2_eta(rho)=-Delta_eta A2+rho Delta_eta B2+rho^2 Delta_eta C2

vanish at the actual rho. Positivity of s rho(1-rho) justifies both
criteria. Neither criterion has been evaluated here. Variation of E,
j or the T1 pivot is not a proof of variation of these combinations.

### Necessary constancy alternative

The accepted complete signed-lift row in RI102 proves the strict fact

    z2 < -4e_2 OR z3 < -4e_3.                                   (7)

If both f2 and f3 are nonconstant, (5) forces w2=z2,w3=z3 and (7)
contradicts strict child positivity. Thus every positive repair requires

    f2 constant OR f3 constant.                                 (8)

More sharply, any j in {2,3} with zj<=-4e_j must have constant fj.
The equality case is excluded by strict positivity just as the strict
case is. Fact (7) does not identify which index fails; proving variation
of one unselected index is insufficient. This is a theorem about the
fixed support, not a new assumption excluding countermodels.

## 5. Exact four-parent family, including the surviving cases

### Both profiles nonconstant

There is no positive solution for these four parents by (7). No D1
ratio test is needed in this case.

### Both profiles constant

All solutions are precisely (2), the complete zero-safe classification
(3)-(4), and the three strict bounds

    delta>-4e_K/(3rho),
    -4e_2<z2 lambda+x<z2+4f2(0),
    -4e_3<z3 lambda+y<z3+4f3(0),                                 (9)

with corrections recovered from (1) and (5). This case is nonempty:
take lambda=x=y=delta=0, hence w1=w2=w3=d1=0,
t=1/Gamma, v1=beta/Gamma, v2=z2/f2(0), v3=z3/f3(0).
Since |zj|<=1 and fj(0)>1/2, v2,v3>-2>-4. Every required child is
positive; the eight D1 rows have L1=d1=0; all three connected rows
hold. This is a witness for exactly T1,T2,T3,D1, not the whole system
and not a replacement of the free parameter in the general family.

### Exactly one profile nonconstant

Let a be its index and b the other index in {2,3}. Necessarily
wa=za, va=0, and za>-4e_a; otherwise the subsystem is empty.
Set c2_xi=m_xi, c3_xi=j_xi and define positive ratios

    alpha_xi=c_a,xi/c_b,xi,       gamma_xi=g1(xi)/c_b,xi,
    u=1-lambda>0,                mu=delta/u.

Equation (3) before division by j now reads, after division by c_b u,

    za alpha_xi+(wb-zb lambda)/u+mu gamma_xi=0.

Therefore define the exact, possibly empty compatibility set

    M={mu real: za Delta_xi alpha+mu Delta_xi gamma=0
                 for all xi=1,...,7}.                           (10)

It is completely classified without an invalid division:

- If some Delta_p gamma is nonzero, mu must equal
  -za Delta_p alpha/Delta_p gamma and must satisfy every other row.
- If gamma is constant and alpha is constant, M is all real numbers.
- If gamma is constant and alpha is nonconstant, M is empty,
  because za is an accepted nonzero seed entry.

For mu in M put C=za alpha_0+mu gamma_0. All positive solutions are
exactly the u satisfying

    1-W* < u < 1+4e_1,
    mu u > -4e_K/(3rho),
    -4fb(0) < u(zb+C) < zb+4e_b,                                (11)

with recovery

    lambda=1-u,         wb=zb-u(zb+C),        wa=za,
    delta=mu u,         d1=3rho mu u/e_K,
    t=u/Gamma,          v1=beta u/Gamma,
    vb=u(zb+C)/fb(0),   va=0.                                   (12)

Proof of necessity follows by subtracting reference row zero, then
solving it for wb. The lower bound in the last line of (11) is vb>-4;
its upper bound is wb>-4e_b. The other bounds are exactly (2) and
d1>-4. Conversely (10) restores all eight D1 equations, (11)
restores every strict bound, and (12) solves both connected parents.
No sign of mu or zb+C is assumed, so zero and sign-changing cases
are included without reversing an inequality improperly. For fixed mu
these are intersections of open affine inequalities in u; emptiness
is left as an explicit condition, not claimed away.

This conditional classification is an exact reduced family for the
four-parent subsystem. It does not determine the actual baseline's
constancy branch or claim a positive member of all sixteen rows.

## 6. All twelve other parents still bind the same variables

The eight connected parents T4,...,T11 retain, for every record,

    (zj-wj)[fj(r)-fj(0)]=0,
    -4e_j<wj<zj+4fj(0),        vj=(zj-wj)/fj(0).                 (13)

For each of the four disconnected parents D2,...,D5 let
Li(r;w)=sum over its individual supported C_i ideals of
q_B(C_i,r,S) w_j(S). The forward child classes remain:

| Parent coefficient row | Individual masks to connected child index |
| --- | --- |
| C_2 | 7:2; 15:4; 23:5; 31:6; 47:7 |
| C_3 | 7:3; 15:6; 23:6; 31:8 |
| C_4 | 7:4; 15:9; 31:10; 47:10 |
| C_5 | 7:7; 15:10; 31:11 |

Every repeated mask/class is still an individual summand. Require

    gi(0) Li(r;w)-gi(r) Li(0;w)=0 for every record,
    Li(0;w)<4e_Ci gi(0),
    di=-Li(0;w)/(e_Ci gi(0)).                                   (14)

In particular the w2,w3 chosen in the first four-parent block still
enter D2,D3. The blocks cannot be solved with incompatible copies of
the same child. Constant f8 and f11 are accepted cases and retain their
interval freedoms. The original all-record transport/coverage remains;
no record is dropped by this presentation.

By the RI111 closure and equations (6)-(9) there, a tuple from section 5
extended by w4,...,w11 satisfies the complete positive 28-child repair
if and only if (13)-(14) also hold. This is a necessary-and-sufficient
conditional test, not an assertion that such a tuple exists. All
outside-support corrections remain zero. Nothing asserts all-size growth.

## 7. Exact coefficient gaps and stopping point

The connected sensitivity formulas need only the existing RI88 held
domain: C3 (8 complete rows/32 slots), C4 (8/40), H5 (8/56), and
C5 (16/96), totalling 40 rows/224 slots. A sufficient fixed-pair
rejection could use two complete rows of each shape: 8 rows/44 slots,
provided it proves BOTH V1-V0 nonzero and Q2_1(rho) nonzero at the
unchanged actual scale. A zero selected contrast proves no constancy.
The latter may instead be proved by root exclusion on the already
justified outer interval; a surviving root does not select rho.
No such evaluation, root decision, executor or admission occurs here.

D1_CATALOGUE_LEMMA.md independently derives g1=1-s UD from all
twenty-one individual proper ideals of D1 and thirteen of its needed
six-parent deletion. Its explicit symbolic closure additionally retains
K4=C3 disjoint A1 and K5=C4 disjoint A1. The justified representative
domain is four complete K4 rows of eight slots and eight complete K5
rows of ten slots: 12 rows/112 slots. These disconnected shapes are not
in the named RI88 held slice. The exact quartic UD is in that lemma;
no new q6/q7 table is needed to express it.

This is the smallest complete-row domain under the particular closure
and proved maximal-bit invariances, not a proof of global information
minimality. Further symbolic identities could reduce it. The baseline
law is not undefined: the gap is that these profiles have not been
supplied/evaluated in the accepted held slice, and no analytic identity
read here settles the needed ratios. No values are invented to close it.

Thus the precise remaining obstructions are: determine/prove the
connected sensitivity branch; if a constancy case survives, satisfy
the explicit ratio equations and strict bounds of section 5; then
satisfy (13)-(14) with those same shared variables. This handoff supplies
a reduced family and named finite gaps, not another numerical campaign.

## 8. Review, custody and claim boundary

The three accompanying lemmas give complete supporting derivations.
Independent whole-manuscript and cross-lemma reviews are required before
research-owner acceptance. This manuscript does not self-admit execution
or publication. Root retains repository/index/Git/push and every future
active admission. Only newly reserved external analytic files are edited.

Allowed yield: conditional theorems, exact reduced equations and a named
gap. No full QM derivation, ontology proof, native kinematic geometry,
gravity/mass correspondence, empirical result or all-size positive law
follows. No new lettered QR gate, support/amplitude/seed change, selected
rho/s, RET, clocks, book or retired kappa-gravity work is started.
This completes the bounded analytic assignment when independently
reviewed; it does not terminate the broader research programme.
