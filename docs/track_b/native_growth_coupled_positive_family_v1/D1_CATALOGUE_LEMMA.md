# RI-117 working lemma: the complete D1 coupling and its held closure

26 September 2026. Manual analytic derivation only. This note keeps the
accepted baseline, eleven-class seed, amplitude epsilon=1/4, and RI111's
fixed 28-child support. No probability, scale, H/z value, or coefficient is
newly evaluated. The resulting formulas are conditional identities for the
actual fixed baseline, not permission to query their arguments.

## 1. Precisely seven supported slots

Write I=C3, C=C1=I ordinal-sum A3, and D=D1=C disjoint {o}, where o is
the old isolated vertex. Give I labels 0,1,2, the three cap vertices
labels 3,4,5, and o label 6. The complete ideal masks of C are

    0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63.

A birth from D giving any Jj=Tj disjoint A1 must exclude o from its
precursor. Otherwise o ceases to be isolated, while every old vertex
in C already has a comparable neighbour and the newborn is not isolated.
The precursor is therefore an ideal S of C, and C+S must be Tj. RI85's
complete forward catalogue then gives, individually:

| Precursor in D | Child | Individual multiplicity |
| --- | --- | ---: |
| I, mask 7 | J1 | 1 |
| I plus cap 3, mask 15 | J2 | 1 |
| I plus cap 4, mask 23 | J2 | 1 |
| I plus cap 5, mask 39 | J2 | 1 |
| I plus caps 3,4, mask 31 | J3 | 1 |
| I plus caps 3,5, mask 47 | J3 | 1 |
| I plus caps 4,5, mask 55 | J3 | 1 |

These are 1+3+3 forward slots, not the backward deletion counts of the
J children. No orbit division is permitted. The other four ideals of C
give zero correction, and every ideal of D containing o except full D
also gives zero correction in this fixed support. Full D gives the private
child F(D) with correction d1. All zero-correction slots retain their
strictly positive baseline probabilities.

For stem record xi in {0,...,7}, retain RI85/RI111's positive held values
a,b,c,g,h,j and put

    Acore_xi = a_xi g_xi^3 / b_xi^3,
    Bcore_xi = h_xi^2 / c_xi,
    Ccore_xi = j_xi.

The maximal-record lemma removes only the three cap bits and isolated bit
from the D row; it does not average or delete any of the eight stem records.
The exact correction sum is

    L1(xi;w) = rho [Acore_xi w1 + 3 Bcore_xi w2 + 3 Ccore_xi w3].       (D1)

This follows directly from the accepted C1 deletion potentials and the
empty/ordinary-birth diamond used in RI111. In the row equation the full
term is e_C g1(xi) d1, where e_C is the record-blind empty probability.

## 2. The accepted harmonic relation removes the seed direction

The complete accepted RI88 six-parent harmonic identity, with z1=1, is

    Acore_xi + 3 Bcore_xi z2 + 3 Ccore_xi z3 = 0
    for every xi.                                                   (D2)

No value of z2 or z3 is computed here. With the two shared deviations

    x = w2-z2 w1,                  y = w3-z3 w1,

equation (D1) becomes exactly

    L1(xi;w) = 3 rho [Bcore_xi x + Ccore_xi y].                       (D3)

For reference xi=0, RI111 equation (23) for D1 is therefore equivalent to

    [g10 Bcore_xi - g1(xi) Bcore_0] x
      + [g10 Ccore_xi - g1(xi) Ccore_0] y = 0,   xi=1,...,7,          (D4)

    3 rho [Bcore_0 x + Ccore_0 y] < 4 e_C g10,                       (D5)

    d1 = -3 rho [Bcore_0 x + Ccore_0 y] / (e_C g10).                 (D6)

Every denominator is positive. Conversely (D4)-(D6) give the entire
complete-record D1 equation and d1>-4, not just its reference row.
The coefficients are fixed actual baseline quantities; x and y are not
chosen separately per record.

The connected parents T2 and T3 still require RI111 (22): for j=2,3,

    (zj-wj)[fj(r)-fj(r0)] = 0 for every complete record r,
    -4 e_Tj < wj < zj + 4 fj(r0),
    vj = (zj-wj)/fj(r0),

with w2=z2 w1+x and w3=z3 w1+y. No claim here that either f2 or f3 is
nonconstant is used. In particular x=y=0 automatically solves (D4) but
does not automatically solve these connected conditions: when w1<1,
zj-wj=zj(1-w1) is nonzero because the accepted zj are nonzero.

If a separate proof establishes both f2 and f3 nonconstant, then w2=z2
and w3=z3 are forced. Equation (D1) reduces to

    L1(xi;w) = rho Acore_xi (w1-1).

Since the positive T1 family has w1<W*<1, D1 in that special case requires
g1(xi)/Acore_xi to be record-constant, and recovers d1>0. Nonconstancy
of g1 alone would not rule this out. This is a conditional reduction, not
a proof of the two sensitivity premises or of ratio nonconstancy.

## 3. Exact symbolic full complement, with no q6/q7 query

The following derivation identifies the full complement needed in (D4).
It neither evaluates it nor assumes it is determined by the connected
C3/C4/H5 rows alone.

Let K4=I disjoint {o}, K5=C4 disjoint {o}, and K6=H5 disjoint {o},
where C4=I ordinal-sum A1 and H5=I ordinal-sum A2. Fix one stem
assignment xi throughout and suppress it in the notation. All additional
maximal bits are immaterial by the accepted maximal-record lemma.
For each T in the four stem ideals {0,1,3,7}, define

    A(T)=q_B(C3,T), B(T)=q_B(C4,T), G(T)=q_B(H5,T),
    Aminus(T)=q_B(K4,T),       Aplus(T)=q_B(K4,T union {o}),
    Bminus(T)=q_B(K5,T),       Bplus(T)=q_B(K5,T union {o}).

Also define

    c=q_B(C4,C4), h=q_B(H5,C4), j=q_B(H5,H5),
    cbar=q_B(K5,C4),          fbar=q_B(K5,K5).

Here h has the same value at each of the two individual one-cap ideals.
For K5, the two listed precursor roles C4 and full K5 are distinct;
cbar is not fbar. Aplus(7) is the full K4 probability and must not be
replaced by a proper-potential formula. All quantities are strictly
positive. The original C1 proper-potential sum is

    E = sum_T A(T)G(T)^3/B(T)^3 + 3h^2/c + 3j.                      (D7)

Apply RI38's deletion formula at K6, with size-six scale rho. Its complete
thirteen proper slots have these exact potentials:

| Precursor | Count | Potential per individual slot |
| --- | ---: | --- |
| T, excluding o | 4, one per T | G(T)A(T)Bminus(T)^2 / [B(T)^2 Aminus(T)] |
| I plus one cap, excluding o | 2 | h cbar/c |
| H5, excluding o | 1 | j |
| T union {o} | 4, one per T | Bplus(T)^2/Aplus(T) |
| I plus one cap and o | 2 | fbar |

Thus, with no new evaluation,

    Ebar = sum_T [G(T)A(T)Bminus(T)^2/(B(T)^2 Aminus(T))
                   + Bplus(T)^2/Aplus(T)]
             + 2h cbar/c + j + 2fbar,
    q_B(K6,K6) = 1-rho Ebar.                                      (D8)

For the first row, deleting one cap gives K5 twice, deleting o gives H5,
deleting both caps gives K4 in the denominator, deleting cap and o gives
C4 twice in the denominator, and deleting all three gives C3. This
explains every factor. The other rows omit respectively two, one, two
and one maxima and follow from the same complete subset product.

Now partition the twenty-one proper ideals of D into eleven excluding o
and ten including o. Their size-seven potentials are:

| Precursor | Count | Potential per individual slot |
| --- | ---: | --- |
| T, excluding o | 4, one per T | rho^4 A(T)^3 G(T)^3 Bminus(T)^3 / [B(T)^6 Aminus(T)^2] |
| I plus one cap, excluding o | 3 | rho^3 h^2 cbar/c^2 |
| I plus two caps, excluding o | 3 | rho^2 j |
| C, excluding o | 1 | 1-rho E |
| T union {o} | 4, one per T | rho^3 Bplus(T)^3/Aplus(T)^2 |
| I plus one cap and o | 3 | rho^2 fbar |
| I plus two caps and o | 3 | 1-rho Ebar |

For example, the first row initially equals

    q_B(K6,T)^3 q_B(C,T) Aminus(T) B(T)^3
        / [Bminus(T)^3 G(T)^3 A(T)].

Insert q_B(C,T)=rho A(T)G(T)^3/B(T)^3 and the first K6 row from
(D8). The displayed rho^4 expression follows by cancellation of strictly
positive factors. For the one-cap row the deletion product is

    q_B(K6,I+cap)^2 q_B(C,I+cap) c / [cbar h^2]
      = (rho h cbar/c)^2 (rho h^2/c) c/[cbar h^2].

For the two-cap row it is (rho j)^2/j. The row at full C has only o
omitted, hence potential q_B(C,C). For an o-containing stem precursor,
the product is q_B(K6,T+o)^3 Aplus(T)/Bplus(T)^3. The last two rows
follow by one- or two-cap deletion as shown. Every repeated cap choice
remains a separate ideal, even after its potential agrees with another.

The full complement is consequently

    g1(xi)=1-s UD_xi(rho),                                         (D9)

    UD_xi(rho)=4-rho(E+3Ebar)+3rho^2(j+fbar)
      +rho^3[3h^2 cbar/c^2 + sum_T Bplus(T)^3/Aplus(T)^2]
      +rho^4 sum_T A(T)^3G(T)^3Bminus(T)^3/[B(T)^6Aminus(T)^2].       (D10)

This is an exact complete-row formula. It retains all eight stem records
and every individual ideal. The actual baseline guarantees g1>0 and
indeed g1>1/2 under its size-seven half-scale rule, but no sign claim is
made for trial scales not belonging to that fixed baseline.

## 4. What is and is not missing

(D9)-(D10) give a two-shape additional held-probability closure at sizes
four and five, not a need for a new q6/q7 table. K4 has eight ideals:
the four T and four T+o. K5 has ten: the four T, four T+o, C4, and K5.
Their complete representative rows contain all data in the formula.

On K4 both the top of C3 and o are maximal. Its complete row therefore
ignores both bits, leaving four assignments of the first two chain bits.
On K5 its C4 top and o are maximal, leaving all eight assignments of the
first three chain bits. Thus a smallest complete-row domain justified by
these proved invariances for this particular two-shape closure is four
K4 rows times eight slots plus eight K5 rows times ten slots: twelve
complete rows, 112 slots. Keeping all eight xi for K4 instead is an
equivalent duplicated domain, not a new coefficient. All eight D1 stem
records are still required; no D1 record is dropped because K4 happens
to have this smaller inherited representative set.

This is minimal only relative to these two shapes and the stated
maximal-record quotient. It is not a claim of information-theoretic
minimality, nor proof that further accepted law-specific identities
cannot eliminate these inputs. No row has been queried, and no new
evaluation or campaign is requested or admitted here.

In particular, RI88's C3/C4/C5/H5 held table does not explicitly contain
either disconnected shape. An argument based solely on their unmarked
names cannot fill in the missing values. Formula (D10) exposes precisely
where a proof of record sensitivity/affine compatibility must either use
an additional analytic identity or retain an explicitly unevaluated
coefficient domain. The complete D1 coupling is not decided by this
catalogue lemma alone.

## 5. Sources, preserved obligations and work boundary

The complete RI111 REPAIR.md was read. The complete RI101 SIGNED.md was
read for incoming closure and the empty/ordinary diamond. RI85 DESIGN.md
sections 2-5 provide its literal ideals, coefficient catalogue and held
transport. RI38 CRITERION.md sections 4-5 provide the deletion product and
common half-scale. RI103 REPAIR.md's accepted maximal-record lemma is
used as reproduced in RI111, including full-complement invariance.
The complete RI115 RESULT_REVIEW.md and the independent provisional
ANALYTIC_NEXT_STEP.md were also read for current result boundaries.

This note does not impose w1=0. The parent manuscript must retain the
positive T1 interval, the T2/T3 connected conditions above, all T4,...,T11
equations, and all D2,...,D5 equations. Solving D1 alone cannot be called
the complete fixed-support extension. No new support, amplitude, seed,
actual rho/s, source import, parse/compile/probe, fixture, solver,
certificate calculation, repository/index edit or git action occurred.

Preparation incident: a read-only text search using an unexpanded shell
glob failed before any search or source execution (tool chunk f5f37b,
exit 1, `zsh: no matches found`). It was replaced by explicit-path
read-only searches. No target or historical evidence was modified.
