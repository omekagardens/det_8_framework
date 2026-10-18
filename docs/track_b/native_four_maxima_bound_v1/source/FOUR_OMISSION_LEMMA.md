# Canonical support and the four omission bound

30 September 2026, Honolulu. Manual companion lemma for independent review.

Use the exact four-maxima domain and notation in the
[main proof](FOUR_MAXIMA.md): C has four caps, R has two events, its
precursor ideals E_i cover R, B=q_empty, and q_J is the actual row on
R plus caps J. For every ideal A of R, including full R, define the
all-four-omission summand

    c4(A) =
      [product_(|J|=3)q_J(A)] [product_(|J|=1)q_J(A)]
      /[B(A) product_(|J|=2)q_J(A)].                             (L1)

We prove, for all compatible precursor choices and all records,

    sum_(A in J(R)) c4(A) <= theta^4*243*110^15 < 1/128,
    theta=1/[72(1+M5)].                                         (L2)

The canonical support input is RI63's accepted finite theorem that every
positive canonical parent-five component is everywhere defect-neutral.
The defect uses arbitrary vertex deletion to a Ferrers cell order.
The literal fixed seed, strict positivity and every ordinary marked
diamond are inherited. None of their scientific certificates is read or
re-executed here.

## 1. A finite support lemma for six-event terminals

Let T0 be ANY six-event terminal with at least four maxima, and let z
be the newborn in a proper parent-five birth realizing T0. Let f(T0)
be the largest cardinality of an induced suborder isomorphic to a
Ferrers cell order; thus delta(T0)=6-f(T0).

A Ferrers diagram with at least four maximal cells must have at least
four distinct positive row lengths. Its size is at least 4+3+2+1=10.
Indeed a maximal cell is the right endpoint at a drop in row length;
four such drops require four distinct positive row lengths, and
additional rows cannot decrease the count. Therefore no Ferrers
suborder of a six-event order can contain four of its original maxima:
an original maximum that is retained remains maximal in any induced
suborder containing it.

Choose an induced Ferrers suborder F of size f(T0). Some original
maximum d is absent from F. Then

    f(T0 minus d)=f(T0),
    delta(T0)-delta(T0 minus d)=1.                              (L3)

The lower inequality for the first equality follows because F survives;
the upper follows because every induced suborder of T0 minus d is also
one of T0. This does not assume that Ferrers orders are hereditary under
arbitrary deletion. Restoring d is a proper birth: other terminal maxima
lie outside its past. Hence (L3) gives a raising proper role.

If d=z, the original role is already raising. If d differs from z, delete
both maxima and call the four-parent B0. Their two pasts are ideals of
B0. Adding d then z, or z then d, gives the same marked terminal T0.
Both second slots are proper because they exclude the other incomparable
maximum. The first birth probabilities are strictly positive. The
ordinary marked diamond therefore joins the two proper roles in the
parent-five ratio graph.

This argument holds for every original record and both newborn bits.
All marks on B0 and on d,z are transported on both routes; the component
quotient forgets only marks outside the selected precursor, just as in
the actual law. Equal precursor, loop and other coincidences do not
remove the equation.

Thus the component of ANY proper birth ending in such T0 contains a
raising role. By the admitted everywhere-neutral support theorem,

    alpha_c^(min,5)=0,
    q_Q(S)=theta*u5(Q,S)                                        (L4)

for every such proper slot. This does not set its ACTUAL probability
to zero. Nor is it an all-size support theorem or an assertion that a
neutral component must be active.

For every triple J subset C and A in J(R), the birth from Q_J at A
keeps the three caps maximal and adds a fourth incomparable maximum.
Extra old maxima, if any, do not harm the argument. A is proper in
Q_J even when A=R. Hence (L4) applies to all four size-five factors
q_J(A) in (L1), with the original cap records intact.

## 2. Uniform small-prefix floors from literal definitions

We need lower bounds only on size-one and size-three probabilities
appearing in correction denominators. These follow from the already
fixed rows, not from a new table search or coefficient body.

At size one the complete row is (a,1-a)=(2/3,1/3), so every entry
is at least 1/3. At size zero the sole probability is 1.
Every complete row entry at every admitted size is at most 1.

At size three use

    e=1/44, c=1/5, d=1/4, g=1/10, k=11/20,
    f_0=1/6, f_1=1/3, h_0=19/30, h_1=7/15.

The five possible order shapes exhaust the domain. Their literal
proper entries and full complements give the following hand check:

| Three-parent | Proper entries or their minimum | Full complement |
| --- | --- | --- |
| Antichain | e; singleton (2/5)e; pair (11/5)e | 4/5 |
| Edge plus isolate | e; e*f_s/c >=(5/6)e; e*h_s/c >=(7/3)e; e*k/g=(11/2)e | 65/88 |
| Fork | e; e*h_s/f_s >=(7/5)e | 43/55 or 49/55 |
| Join | four proper entries e | 10/11 |
| Chain | three proper entries e | 41/44 |

The antichain sum of proper entries is
e[1+3(2/5)+3(11/5)]=(44/5)e=1/5.
For edge plus isolate it is e[2+(f_s+h_s)/c+k/g]
=e[2+4+11/2]=23/88, since f_s+h_s=4/5 for BOTH marks.
For the fork the sums are e[2+2(19/5)]=12/55 at mark zero
and e[2+2(7/5)]=6/55 at mark one. Join and chain sums are
4e and 3e. This verifies all full complements in the table manually.

Every full complement is greater than 1/2. The smallest displayed
proper entry is (2/5)e=1/110. All original marks, not only one
representative, are covered. Therefore

    q1(S)>=1/3,          q3(S)>=1/110                            (L5)

for every ideal, including full. These are ideal probabilities q, not
the fair-mark-resolved q/2 probabilities.

## 3. Exact factors from extra old omitted maxima

For fixed A and cap triple J, let U_J(A) be the old maxima of Q_J
outside A, excluding its three caps. More explicitly,

    U_J(A) = [Max(R) minus A] minus union_(j in J) E_j.           (L6)

An old nonmaximum in R cannot become maximal by adding caps. An old
maximum remains maximal exactly when none of the retained caps covers it.
Thus the full omitted-maxima set for u5(Q_J,A) is J union U_J(A).
There are at most two extra old maxima.

If only caps were omitted, their seven factors would be

    t_J(A) = B(A) product_(H subset J, |H|=2)q_H(A)
                         / product_(i in J)q_i(A).              (L7)

Do NOT substitute t_J for the potential when U_J(A) is nonempty.
Partition every nonempty deleted subset into its old part X and its
cap part V. The exact full definition gives

    u5(Q_J,A) = t_J(A)
       product_(nonempty X subset U_J(A)) G_(J,X)(A),           (L8)

    G_(J,X)(A) =
       product_(V subset J)
        q_((R minus X)+(J minus V))(A)
                         ^((-1)^(|X|+|V|+1)).                  (L9)

Every cap retains its original precursor: since X consists of old
maxima uncovered by all caps in J, no E_j contains any element of X.
Since X is outside A, that ideal also survives. Thus every factor in
(L9) is a genuine smaller-law probability on its stated parent. Full
smaller-parent probabilities, when present, remain actual complements.

For |X|=1, the positive factors in (L9) are one size-four probability
(V empty) and three size-two probabilities (|V|=2). The denominators
are three size-three entries (|V|=1) and one size-one entry (V=J).
Using (L5) and bounding only numerator probabilities by 1 gives

    G_(J,X)(A) <= 3*110^3.                                     (L10)

For |X|=2, the positive factors are three size-two probabilities
(|V|=1) and the empty-parent probability 1 (V=J). The denominator
has one size-three entry (V empty) and three size-one entries
(|V|=2). Hence

    G_(J,X)(A) <= 27*110.                                      (L11)

The empty-parent factor in this case is legitimate: two extra old
maxima imply R is the antichain, A empty and the three retained
precursors empty. It is not an unmodeled normalization.

## 4. Original coverage limits the correction product

For each old vertex x, let C_x={i in C : x in E_i}. Original coverage
gives C_x nonempty. A vertex can lie in U_J(A) only if it is an old
maximum outside A and C_x is disjoint from J.

Each triple J is C minus one cap i. Therefore the disjointness condition
is C_x subset {i}, hence C_x={i}. A given old vertex can appear in
U_J(A) for AT MOST ONE of the four triples. Since R has two vertices,

    sum_(J subset C, |J|=3) |U_J(A)| <= 2.                      (L12)

This counts actual old-vertex occurrences, not arbitrary independent
correction choices. The possibilities are no extra occurrence, one
singleton, two singleton occurrences in different triples, or two
vertices in the same triple. The last case contributes two factors
of type (L10) and one of type (L11). Since both upper constants
exceed one, all cases are bounded by the same value:

    Gamma(A) =
      product_(|J|=3) product_(nonempty X subset U_J(A))G_(J,X)(A)
      <= (3*110^3)^2*(27*110)=243*110^7.                         (L13)

This includes repeated/empty/full E_i and, for example, the extreme
case of three empty precursors with the fourth equal to antichain R.
A caps-only product would miss precisely these corrections.

## 5. Cancellation of identical actual factors

By (L4) and (L8),

    product_(|J|=3)q_J(A)
      = theta^4 Gamma(A) product_(|J|=3)t_J(A).                 (L14)

Each pair H is contained in two of the four triples, each singleton
i in three, and each t_J supplies one B(A). Consequently

    product_(|J|=3)t_J(A)
       = B(A)^4 [product_(|H|=2)q_H(A)^2]
                         /[product_(i in C)q_i(A)^3].          (L15)

Substitution in the full fifteen-factor expression (L1) cancels only
the same actual positive factors and gives exactly

    c4(A)=theta^4 Gamma(A) B(A)^3
                  [product_(|H|=2)q_H(A)]
                         /[product_(i in C)q_i(A)^2].          (L16)

Here each q_i(A) is a size-three proper probability; the all-ideal
bound (L5) certainly applies. Each remaining q_H is a size-four
probability at most one. We do not replace its full canonical data
by a free scale. Thus

    c4(A) <= theta^4 * 243*110^7 * 110^8 * B(A)^3.              (L17)

All A in J(R), including full R, are present. B is a complete
positive size-two row, so

    sum_A B(A)^3 <= sum_A B(A)=1.

This proves the first inequality in (L2), without losing shared marks
or silently dropping additional maxima.

## 6. Strict hand comparison and scope

The inherited native witness gives M5>10^9. Therefore

    theta=1/[72(1+M5)] < 2^(-30),

because 2^30=1,073,741,824<72*10^9. Also 243<256=2^8 and
110<128=2^7, so

    243*110^15 < 2^(8+105)=2^113.
    theta^4*243*110^15 < 2^(-120+113)=1/128.                   (L18)

This is a manual sufficient bound, not numerical evaluation of M5 or
theta. The main theorem uses a stronger manual M5 lower bound from
the SAME native witness only to compare the total U6 with T.

The finite support argument, the correction multiplicities and coverage
bound are new analytic consequences of the named premises. They do not
replace those premises with an all-size neutrality assumption. No
canonical vector, scientific body, graph or LP was read or executed.
No higher-size law, actual W/H30 conclusion, full QM derivation or
physical interpretation follows from this companion alone.

The full class proof, source identities, and author administrative
evidence accompany this lemma. Root owns independent acceptance and
publication. Five/six-maxima classes remain open; no successor, new
executor, RET, clock, book or retired gravity work is started.
