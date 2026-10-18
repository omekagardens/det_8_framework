# RI124 — symbolic coefficient closure and compensation obligations

26 September 2026, Hawaii. Contributor manuscript; not an independent review.
Only hand algebra and source reading were used. No probabilities, polynomial
coefficients, seed entries, scales, numerical ranks or feasibility values were
calculated; no scientific source/helper was run. This note changes no accepted
premise, baseline, seed, amplitude or predecessor result.

## 1. Outcome and precise scope

For the proposed support H30 = H28 union {Y2,Y3}, where

    I = C3,
    Y2 = I ordinal-sum (C2 disjoint A3),
    Y3 = I ordinal-sum (V3 disjoint A2),
    V3 = A2 ordinal-sum A1,

every newly added proper coefficient and every T1/T2/T3 contrast can be
expressed in the accepted forty complete held rows / 224 individual slots,
together with the unchanged, unevaluated scales rho=a6 and s=a7. The
remaining coefficients also have a finite symbolic closure: all connected
parents use those same four held shapes; the disconnected parents additionally
use only K4=C3 disjoint A1 and K5=C4 disjoint A1, the exact twelve-row /
112-slot domain already identified in RI117. No new numerical q6/q7 table is
needed to *state* this complete reduction.

This is not a positive continuation. The exact compensation minors,
reference intercepts, shared-parent equations and strict inequalities below
remain simultaneous requirements at the actual baseline. Even a successful
contrast span test would not discharge them. RI122's rejection of H28 and
RI117's local T1 positive family remain accepted and unchanged.

The main support manuscript supplies the complete closure. Independently
checking the new columns by hand: Y2's three isolated cap maxima delete to
T2, and its chain-tip maximum deletes to T1; Y3's two isolated cap maxima
delete to T3, and its V-tip deletes to T1. Thus these two columns create no
new incoming parent class. They do not create an unlisted h7=1 parent row.
No minimality claim is made.

## 2. Notation and the new individual coefficients

Use RI111/RI117 notation, with xi=0,...,7 and eta=xi+8 sigma,
sigma in {0,1}. For S in {0,1,3,7}, set

    A_xi(S)=q_B(C3,xi,S),
    B_xi(S)=q_B(C4,xi,S),
    G_xi(S)=q_B(H5,xi,S),       H5=C3 ordinal-sum A2,
    D_eta(S)=q_B(C5,eta,S).

Write a=A(7), b=B(7), g=G(7), d=D_eta(7),
c=q_B(C4,xi,15), h=q_B(H5,xi,15)=q_B(H5,xi,23),
j=q_B(H5,xi,31), e=q_B(C5,eta,15), ell=q_B(C5,eta,31).
Proper locality gives d=d_xi independent of sigma. Every denominator is
strictly positive at B. All equalities transport orders, individual ideals
and records together; they do not physically delete a committed record.

Let t0=y(Y0), t2=y(Y2), t3=y(Y3). The following are probabilities per
individual ideal, including the size-seven factor s:

| Parent | Individual new ideal(s) | Child | Probability per ideal |
| --- | --- | --- | --- |
| T1=I ordinal-sum A4 | I plus one of its four cap vertices | Y2 | s rho^3 nu_xi, with nu=h^3/c^2 |
| T1 | I plus two of its four cap vertices | Y3 | s rho^2 j_xi |
| T2 | I | Y2 | k2(xi)=s rho^3 b2_xi, with b2=a g^3 d/b^4 |
| T3 | I | Y3 | k3(xi)=s rho^2 b3_xi, with b3=a g^3/b^3 |

There are four T1 one-cap ideals and six T1 two-cap ideals, each retained
separately before summing. Their aggregated coefficients are

    K12(xi)=4 s rho^3 nu_xi,
    K13(xi)=6 s rho^2 j_xi.

Neither four nor six is an incoming-deletion multiplicity. At T2 and T3
the new core ideal is a single slot, despite the three/two corresponding
backward deletion roles of Y2/Y3.

Derivation: RI117's complete T2 proper-potential table gives the stem
potential rho^3 A(S)G(S)^3D(S)/B(S)^4, so set S=7. Its T3 table gives
rho^2 A(S)G(S)^3/B(S)^3. RI111's complete T1 proper-potential sum has
four one-cap terms rho^3 h^3/c^2 and six two-cap terms rho^2 j. The
coefficient identification follows by appending the new maximum at the
stated precursor; no new evaluation is involved.

The complete new core profiles k2,k3 depend on xi, not on T2's additional
record sigma. This follows from proper locality, not from a numerical
observation. All sixteen T2 rows must nevertheless be tested because f2
initially retains eta; none is silently discarded.

## 3. Exact compensation reduction, including intercept and positivity

Put w_j=e_Tj y(Jj), v_j=y(F(Tj)), d_i=y(F(Di)), where every e is the
actual positive record-blind empty probability. The changed connected rows
are exactly

    w1 + k0(xi)t0 + K12(xi)t2 + K13(xi)t3 + f1(xi)v1 = 1,
    w2 + k2(xi)t2 + f2(eta)v2 = z2,
    w3 + k3(xi)t3 + f3(xi)v3 = z3.                 (1)

Here k0=s rho^4 p with p=a^3 g^6/b^8. The new columns have no other
incoming parents. All equations quantify over the complete corresponding
record cubes, using the proved transports only.

RI122 supplies nonzero reference contrasts

    pi_j = f_j(1)-f_j(0) != 0,                j=2,3.

For each j define, without evaluating,

    alpha_j = -[k_j(1)-k_j(0)]/pi_j,
    Gamma_j = k_j(0)+f_j(0)alpha_j,
    N_j(r) = [k_j(r)-k_j(0)]pi_j
             -[f_j(r)-f_j(0)][k_j(1)-k_j(0)].

Subtracting the reference equation, using only the proved nonzero pivot,
shows that all Tj rows in (1) are equivalent to

    v_j=alpha_j t_j,
    w_j=z_j-Gamma_j t_j,
    N_j(r)t_j=0 for every record r.                            (2)

This equivalence includes t_j=0 and Delta k_j=0. Its strict child
positivity requirements are exactly

    t_j > -4,
    alpha_j t_j > -4,
    z_j-Gamma_j t_j > -4e_Tj.                                  (3)

If z_j<=-4e_Tj, a positive solution requires t_j nonzero, every N_j(r)=0,
and Gamma_j nonzero; more precisely Gamma_j t_j<z_j+4e_Tj<=0.
At least one of j=2,3 has the strictly bad seed value by the accepted
RI102 disjunction. Those facts alone neither choose that index nor satisfy
(3). If Gamma_j=0, the intercept still forces w_j=z_j even when every
contrast minor vanishes. If Delta k_j=0 for all records, alpha_j=0 and
the new coefficient may still change the intercept: a constant proper
coefficient must not be mistaken for an ineffective new column.

Using RI117's held expressions V and Q2, the exact contrast equations can
also be written without s:

    -Q2_eta(rho)v2 + rho^2 Delta_xi b2 t2 = 0,
    (1-rho)Delta_xi V v3 + rho Delta_xi b3 t3 = 0.              (4)

The accepted Q2_1(rho)!=0 and Delta_1 V!=0 give

    alpha2=rho^2 Delta_1 b2/Q2_1(rho),
    alpha3=-rho Delta_1 b3/[(1-rho)Delta_1 V].

For nonzero t2/t3, their remaining compatibility conditions are respectively

    Delta_xi b2 Q2_1(rho)-Delta_1 b2 Q2_eta(rho)=0
        for all eta=0,...,15,
    Delta_xi b3 Delta_1 V-Delta_1 b3 Delta_xi V=0
        for all xi=0,...,7.                                   (5)

These equations are not new accepted vanishing claims. No numerical minor,
root, rank or actual rho has been computed here.

For T1 use RI111's P_xi and accepted P_1(rho)!=0. Dividing its contrast
equation by positive s rho gives

    -P_xi(rho)v1 + rho^3 Delta_xi p t0
      +4rho^2 Delta_xi nu t2 +6rho Delta_xi j t3=0.             (6)

Set beta=rho^3 Delta_1 p/P_1(rho),
alpha12=4rho^2 Delta_1 nu/P_1(rho),
alpha13=6rho Delta_1 j/P_1(rho). Then

    v1=beta t0+alpha12 t2+alpha13 t3.                          (7)

RI115's accepted six zero minors first eliminate the t0 contribution from
the other six contrast rows. Before using their coefficient consequences,
the exact remaining T1 conditions are

    [4rho^2 Delta_xi nu-P_xi(rho)alpha12]t2
      +[6rho Delta_xi j-P_xi(rho)alpha13]t3=0,
          xi=2,...,7.                                       (8)

In fact the accepted *polynomial identities*, not merely zeros at the
actual rho, make both brackets in (8) identically zero. Here is the
additional hand-algebra argument. For every xi=2,...,7, RI115 accepts

    M_xi(x)=Delta_xi p P_1(x)-Delta_1 p P_xi(x) identically zero,
    P_xi(x)=-4Delta_xi E+6x Delta_xi j
              +4x^2 Delta_xi nu+x^3 Delta_xi K.

The coefficient of x in M gives

    Delta_xi p Delta_1 j=Delta_1 p Delta_xi j,

and its coefficient of x^2 gives

    Delta_xi p Delta_1 nu=Delta_1 p Delta_xi nu.

The accepted Delta_1 p<0 permits defining
lambda_xi=Delta_xi p/Delta_1 p. Thus P_xi=lambda_xi P_1 as
polynomials, Delta_xi j=lambda_xi Delta_1 j, and
Delta_xi nu=lambda_xi Delta_1 nu. Substitution into (8), using the
accepted nonzero actual P_1(rho), cancels each bracket separately.
No division by Delta_1 j or Delta_1 nu is used; their possible zero
values are included. The reference and pivot rows xi=0,1 already hold
by construction. Consequently every choice of t0,t2,t3 with (7) has
complete all-record T1 *signed contrast compatibility*. No new T1 minor
evaluation is an outstanding obligation for this support.

The T1 reference intercept still requires

    w1=1-[k0(0)+f1(0)beta]t0
          -[K12(0)+f1(0)alpha12]t2
          -[K13(0)+f1(0)alpha13]t3.                          (9)

Retain t0>-4, v1>-4, w1>-4e_T1, as well as (3). The old local T1
parameterization is recovered when t2=t3=0; it is not imposed unchanged
when the new columns are nonzero. D1 still implies w1<W*<4/41 because
its core slot and seed denominator are untouched. Complete D1 normalization
and positivity below imply that bound; it may additionally be retained as
an early necessary inequality.

Adding columns incident only to T1 would leave both old equations
Delta f_j v_j=0 at j=2,3. Their accepted nonzero contrasts would again
force v2=v3=0 and w2=z2,w3=z3, contradicting the bad-seed disjunction.
The present Y2/Y3 choices enter those exact obstructed parent equations;
whether they do enough is precisely (2)--(9), not an assumed rank gain.

## 4. Every remaining shared-parent equation remains binding

For j=4,...,11 the original conditions remain

    (z_j-w_j)[f_j(r)-f_j(0)]=0 for every record,
    -4e_Tj < w_j < z_j+4f_j(0),
    v_j=(z_j-w_j)/f_j(0).                                    (10)

Constant profiles retain their interval freedom. No blanket sensitivity
claim or assignment w_j=z_j is made. For each i=1,...,5 retain

    g_i(0)L_i(r;w)-g_i(r)L_i(0;w)=0 for every record,
    L_i(0;w)<4e_Ci g_i(0),
    d_i=-L_i(0;w)/[e_Ci g_i(0)].                              (11)

RI85 supplies all the supported individual six-parent potentials. In its
notation (ell is its held C5 full probability), the complete sums are

    L1=rho[(a g^3/b^3)w1+3(h^2/c)w2+3j w3],
    L2=rho[(d g/b)w2+(e h/c)w4+h w5+j w6+ell w7],
    L3=rho[g w3+2h w6+j w8],
    L4=rho[(d^2/b)w4+(e^2/c)w9+2ell w10],
    L5=rho[d w7+e w10+ell w11].                              (12)

Each integer factor denotes that many separately retained ideal slots,
not an orbit quotient. L1,L3 use xi and the other rows use eta with the
appropriate transported records. The same w2,w3 from (2) occur in L2,L3;
independent per-parent fits are inadmissible.

Equations (2)--(3), (7)--(11), all indicated compatibility rows, and
t0>-4 are a support-specific necessary-and-sufficient *conditional*
criterion once the unchanged coefficients and complete support closure
are supplied. Recover all v,w,d from the displayed intercepts. By the
RI111 normalization argument, these give every incoming row and every
strict child multiplier; outside rows remain unchanged by closure. The
common class correction makes both routes of each scalar-passive whole-map
diamond acquire the same terminal factor. This is a through-eight-birth
statement under the accepted model assumptions, not informative QM or an
all-size extension theorem. No feasible tuple has been supplied.

## 5. Exact finite closure for the outstanding coefficients

The remaining profiles f4,...,f11 and g1,...,g5 have not been newly
evaluated. It would nevertheless overstate the gap to say that their
specification requires a new q6/q7 campaign. A finite symbolic reduction
uses the same accepted maximal-deletion identity as RI85 and RI117.

For a proper ideal S of an n-parent P let M=Max(P) minus S. Define

    u(P,r,S)=product over nonempty B subset M of
      q_B(P minus B, r restricted and transported, S)
        raised to (-1)^(|B|+1).

At n=6, q_B(P,r,S)=rho u(P,r,S); at n=7 it is s u(P,r,S).
The full probability is one minus the sum over *every individual proper
ideal*, not only supported correction slots. This is a symbolic recursive
identity, not a program or permission to evaluate the recursion. Positive
denominators are guaranteed only for the actual accepted baseline; trial
scales are not silently promoted to baseline values.

### Connected closure

Every maximal deletion of a supported Tj leaves one of RI85's five
six-parent orders C_i=I ordinal-sum R_i, with three-cap R_i. Deleting
further nonempty sets of cap maxima leaves I with zero, one or two cap
vertices. The only held orders at size at most five are therefore

    C3, C4, C5, H5.

This proves that the complete f_j for *all* eleven connected parents,
the empty e_Tj, and the empty e_Ci reduce to the already held forty rows /
224 slots plus rho,s. It is not necessary to guess the missing full
complements: the displayed recursion sums their entire finite ideal sets.
All records are transported, including C5's retained nonmaximal cap bit.
The fact that some such symbolic expressions are not printed as expanded
polynomials does not permit omitting their corresponding equations.

### Disconnected closure

For D_i=C_i disjoint {o}, maximal deletion either removes o and leaves a
connected factor, or retains o. A retained-o factor of size six has its
two-cap remainder either a two-chain or a two-antichain. Thus the only
size-six disconnected intermediate orders are

    C5 disjoint A1,     H5 disjoint A1.

Their own maximal deletions leave the connected held shapes above or

    K4=C3 disjoint A1,  K5=C4 disjoint A1.

No stem vertex is maximal while a cap remains. Removing all remaining cap
maxima in these products leaves C3, or C3 with o still isolated; the
process creates no other held shape and does not require an unlisted
smaller-order probability. This exhausts the required factor closure for
all five g_i, not only g1. Every six-parent full complement includes its
complete proper-ideal sum before it is used as a seven-parent factor.

The exact additional complete held rows are:

| Order and natural tuple | Records retained | Complete ideal masks | Slots |
| --- | --- | --- | ---: |
| K4=(0,1,3,0), o at label 3 | bits 0,1 arbitrary; maximal bits 2,3 zero | 0,1,3,7,8,9,11,15 | 4 rows x 8 = 32 |
| K5=(0,1,3,7,0), o at label 4 | bits 0,1,2 arbitrary; maximal bits 3,4 zero | 0,1,3,7,15,16,17,19,23,31 | 8 rows x 10 = 80 |

These are precisely twelve complete rows / 112 slots, already identified
for D1 in RI117. The full ideals 15 and 31 remain full probabilities,
not proper potentials. Maximal-record invariance justifies the omitted
bits for these held representatives and transports back to every original
record. K4's smaller retained cube does not erase any D_i record.

Consequently an exact *sufficient finite input domain for symbolic whole
support feasibility* is the existing40/224 plus these additional12/112,
the unchanged seed z, and the actual rho,s or adequate analytic statements
about them. This totals52 complete held rows /336 slots. It is not an
information-theoretic minimality theorem. Further source identities could
remove some inputs, and some special feasible branches could avoid a
profile; neither is assumed here. No new q value is supplied in this note.

## 6. Precise remaining obligations and prospective contract boundary

1. Check or prove the T2/T3 compensation minors (5) and the reference
   intercept/strict inequalities at the unchanged actual baseline. Their
   symbolic inputs already lie in the held40/224 domain. T1's contrast
   conditions (8) are already identically satisfied by the accepted RI115
   polynomial identities, as proved above; this does not settle T1's
   reference equation, positivity, or its coupling through D1. Positive
   coefficients or an added column count do not settle the remaining tests.
2. Satisfy (10)--(12) with the *same* w variables, retaining every record
   and ideal. All L coefficients already lie in held40/224. For complete
   disconnected full profiles, supply analytic identities replacing the
   named K4/K5 rows or preserve those exact finite missing inputs.
3. Use the unchanged actual rho,s and seed. RI122 supplies an interval and
   specific nonzero contrasts, not numerical values or every inequality
   needed by (3), (9)--(11). One may prove a result uniformly over a
   justified domain; choosing a favorable point in that domain is not an
   admissible substitute for the actual scales.
4. A prospective later input contract, if authorized by the owner, must
   pin the actual accepted held baseline, all52 complete row identities,
   normalization, positivity, the literal individual ideal lists, complete
   record transports, and each inherited diamond identity used. It must
   reconstruct the complete symbolic coefficient system and distinguish
   zero/nonzero pivot cases, strict positivity from rank, and a surviving
   algebraic possibility from actual feasibility. This is a description
   of missing evidence, not an active card, executor, query request or
   authorization for q6/q7, global-scale, H/z or full-layer computation.

Allowed present yield: the frozen symbolic reduction and explicit finite
gaps. No positive continuation, new numerical obstruction, minimal support,
native geometry, gravity, mass, physical discriminator or ontology result
is claimed. Root alone adjudicates and authorizes any later computation.

## 7. Sources read and contributor boundary

Read completely for this note:

- RI111 external REPAIR.md at
  /Volumes/AI_DATA/development/det-review-evidence/ri111-one-column-repair-HRfi3z/REPAIR.md.
- RI117 external ANALYTIC_REDUCTION.md, CONNECTED_CONSTRAINTS_LEMMA.md,
  and D1_CATALOGUE_LEMMA.md in
  /Volumes/AI_DATA/development/det-review-evidence/ri117-coupled-positive-family-QrAaK5YQ/.
- RI85 DESIGN.md at
  /Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_four_vertex_cap_v1/DESIGN.md.

RI122's final nonconstancy/obstruction adjudication is an assigned accepted
premise, not a result independently rerun here. The old documents' historical
open-result wording is not adopted as the current adjudication. This author
contributed coefficient derivations and is not the fresh nonauthor reviewer
required for the final RI124 proof/support packet.
