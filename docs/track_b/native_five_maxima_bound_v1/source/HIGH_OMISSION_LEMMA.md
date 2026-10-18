# Four and five omission sectors in the five maxima class

30 September 2026, Honolulu. Manual companion proof for independent review.

Use the marked domain in the [main proof](FIVE_MAXIMA.md): R={x},
five caps C with E_i empty or R, and their union R. Every q_J is
an actual complete row on R plus caps J with the original records.
We prove

    C4_i <= theta^4*3*110^11 < 2^(-73) < 1/128,
    C5 <= 2*theta^5*3^8*110^24 < 1/256.                        (H1)

All extra old maxima in the smaller-parent potentials are retained.
No supplied canonical vector or numerical maximum is evaluated.

## 1. Inherited finite facts and their domains

The accepted RI205 support lemma states that a proper parent-five
birth ending in a six-event terminal with at least four maxima has

    q_Q(S)=theta*u5(Q,S),   theta=1/[72(1+M5)].                  (H2)

For context, its finite proof chooses a largest induced Ferrers
suborder. Four Ferrers maxima need at least ten cells, so some
original maximum of such a six-terminal is absent. Deleting that
maximum preserves the largest Ferrers cardinality, making its
restoration defect-raising. Any other proper birth role of the same
terminal is joined to this role by an ordinary marked diamond on the
four-parent obtained by deleting both incomparable maxima. Every
original/newborn mark is transported. RI63's everywhere-neutral active
canonical support forces its boundary coefficient to zero, but
theta remains positive. This finite result is used on its proved
domain; no all-size support statement is made.

The unchanged literal seed and RI205's complete manual check supply

    q1(S)>=1/3,    q3(S)>=1/110                                (H3)

for ALL ideals including full. The singleton row is (2/3,1/3).
At size three the least proper probability is the antichain singleton
(2/5)e=1/110, e=1/44. The full probabilities for antichain, edge plus
isolate, fork, join, and chain are respectively
4/5, 65/88, 43/55 or 49/55, 10/11, and 41/44. The fork alternatives
retain both actual root bits; the other proper seed entries are no
smaller than 1/110. These are inherited proved seed facts, not a new
table lookup. Every probability is at most one, and the empty-parent
probability is one.

Finally M5>5 billion by the SAME native antichain witness, so the
main proof's hand comparison gives theta<2^(-38).

## 2. Four omissions with one retained selected cap

Fix retained cap i and O=C minus {i}, with four omitted caps.
For S=A+i, E_i subset A, define rows on the base B_i=R+i by

    b(S)=q_i(S),
    p_J(S)=q_(i+J)(S),             J proper subset O.

The exact four-omission summand is

    c4_i(S) =
      [product_(|J|=3)p_J(S)] [product_(|J|=1)p_J(S)]
          /[b(S) product_(|J|=2)p_J(S)].                        (H4)

The four p_J with |J|=3 are size-five probabilities. A birth at S
covers i but none of these three other caps. They and the newborn
are four terminal maxima, regardless of any extra old maximum.
Every S is proper in these parents, so (H2) gives p_J=theta*u5.

For a triple J subset O, the caps-only deletion product is

    t_J(S)=b(S) product_(H subset J, |H|=2)p_H(S)
                       /product_(h in J)p_h(S).                (H5)

The retained cap i is SELECTED, so it is not an omitted maximum,
even if its precursor is empty. The only possible extra omitted
maximum is x. It occurs exactly when A is empty, E_i is empty,
and every E_j with j in J is empty. In all other cases the actual
potential is t_J. When x is extra, the exact remaining factor is

    G_J(S)=product_(V subset J)
       q_((B_i minus {x})+(J minus V))(S)^((-1)^|V|).           (H6)

This includes all eight V, not only nonempty cap deletions. All
precursors and S survive removal of x because no retained cap
covers x in this exceptional case and S={i}. Thus every entry in
(H6) is a genuine smaller-law probability.

For V of even size, (H6) has a size-four numerator once and size-two
numerators three times. For V of odd size it has size-three
denominators three times and a size-one denominator once.
Equation (H3) and numerator probabilities at most one imply

    G_J(S) <= 3*110^3.                                         (H7)

The smallest parent contains the selected i, so its probability may
be full; (H3) includes that full singleton probability. No full-slot
potential formula has been introduced.

If A=R there are no extra omitted old maxima. If A is empty, E_i is
empty and original coverage says the set
D={h in O : E_h=R} is nonempty. For x to be uncovered in a triple
J=O minus {h}, D must equal {h}. Consequently x can be extra in
AT MOST ONE of the four triples. Hence the product Gamma_i(S)
of every exceptional correction satisfies

    Gamma_i(S) <= 3*110^3.                                     (H8)

This is selected-ideal coverage. The four omitted precursors are
not asserted to cover the retained base B_i, since none contains i.

In the product of the four t_J, each pair H occurs twice, each
singleton h occurs three times in the denominator, and b occurs
four times. After substituting the four exact theta factors into
(H4), cancellation of only identical positive actual entries gives

    c4_i(S)=theta^4 Gamma_i(S) b(S)^3
                    product_(|H|=2)p_H(S)
                       /product_(h in O)p_h(S)^2.              (H9)

Here each p_h is a size-three probability at least 1/110; each
p_H with |H|=2 is a size-four probability at most one. Thus

    c4_i(S) <= theta^4*3*110^11*b(S)^3.                         (H10)

The S permitted by (6) of the main proof form a subset of the ideals
of the complete two-parent row b, including its full ideal when A=R.
Therefore sum_S b(S)^3<=sum_S b(S)<=1. This proves

    C4_i <= theta^4*3*110^11.                                   (H11)

By theta<2^-38, 3<2^2 and 110<2^7, the right side is strictly less
than 2^(-152+2+77)=2^-73<1/128. This argument covers every retained
i, including E_i=R (when only A=R is allowed).

## 3. All five omissions and the full thirty-one factors

For all five omissions S=A is empty or R. The exact summand is

    c5(A)=B(A)
       [product_(|J|=4)q_J(A)] [product_(|J|=2)q_J(A)]
        /[product_(|J|=3)q_J(A) product_(|J|=1)q_J(A)].         (H12)

All five q_J with |J|=4 have size five and are proper at A.
A birth at A preserves all four caps as maxima and adds a fifth.
The support condition in (H2) therefore holds for each one.

For each such quadruple J, its caps-only potential is the full
four-cap alternating product

    t_J(A)=
       [product_(H subset J, |H|=3)q_H(A)]
       [product_(h in J)q_h(A)]
        /[B(A) product_(H subset J, |H|=2)q_H(A)].              (H13)

Its multiplicities are 4,6,4,1, including B in the denominator.
The only possible additional omitted maximum is x, and it occurs
exactly if A is empty and every E_j for j in J is empty.
If it occurs, the full potential is t_J(A) times

    G_J(A)=product_(V subset J)
                 r_(J minus V)(A)^((-1)^|V|).                  (H14)

In (H14), r_H is the actual row on the caps H alone, with NO x;
all their original precursors are empty. This separate notation
distinguishes the x-deleted parent from q_H, which retains R.
A is empty in this case. All sixteen V, including empty and full,
are part of (H14).

To avoid any substitution of the wrong row, write the same factor
without the cap-row shorthand as

    G_J(empty)=product_(V subset J)
        q_(Q_J minus ({x} union V))(empty)^((-1)^|V|).          (H15)

Even |V| gives numerator parent sizes four once, two six times,
and zero once. Odd |V| gives denominator sizes three four times
and one four times. Thus

    G_J(empty) <= 3^4*110^4.                                   (H16)

The empty-parent factor is exactly one. It is included, not replaced
by an unknown normalization. Full smaller-parent probabilities,
where applicable, remain their actual row entries.

Let D={h in C:E_h=R}; it is nonempty by original coverage.
A quadruple J=C minus {h} can leave x uncovered only if D={h}.
Thus at most ONE of the five quadruples has an extra omitted maximum.
For the total correction Gamma(A),

    Gamma(A)<=3^4*110^4,                                      (H17)

and Gamma(R)=1. This proves the multiplicity bound without treating
five correction factors as independent choices.

## 4. Exact cancellation in the five-omission sector

In the product over the five quadruples J of (H13), each triple H
is contained in two quadruples, each pair in three, and each
singleton in four; B appears five times in the denominator.
Using the five theta factors and (H17),

    product_(|J|=4)q_J(A)
      =theta^5 Gamma(A)
         [product_(|H|=3)q_H(A)^2]
         [product_(|H|=1)q_H(A)^4]
          /[B(A)^5 product_(|H|=2)q_H(A)^3].                   (H18)

Insert this into (H12), retaining its outer B and every factor:

    c5(A)=theta^5 Gamma(A)
       [product_(|H|=3)q_H(A)]
       [product_(|H|=1)q_H(A)^3]
          /[B(A)^4 product_(|H|=2)q_H(A)^2].                   (H19)

There are ten remaining size-four numerator entries, five size-two
numerator entries each cubed, ten size-three denominator entries
each squared, and the fourth power of the singleton B.
All are entries of the original fixed law with original restricted
marks. No independently adjustable parameters were introduced.

Bound the numerator probabilities by one, the singleton denominator
by 1/3 and all size-three denominators by 1/110. Equations (H17)
and (H19) give

    c5(A) <= theta^5*3^8*110^24.                               (H20)

There are exactly TWO ideals of R, not two record assignments or
two quotient classes. Both empty and full R remain in the sum, so

    C5 <= 2*theta^5*3^8*110^24.                                (H21)

The manual comparison is 3^8=6561<8192=2^13 and 110^24<2^168.
Together with theta^5<2^-190 this yields

    2*theta^5*3^8*110^24 < 2^(1-190+13+168)=2^-8=1/256.        (H22)

The printed numerical M5 and actual theta are not inputs to this bound.

## 5. What the lemmas establish

There are five C4_i sectors and one C5, so (H11) and (H22) imply
sum_i C4_i+C5<5/128+1/256=11/256. Their stronger individual bounds
are not needed to tighten or change the target T.

All original/cap marks, compatible repetitions and empty/full
precursors remain. The only simplification of the canonical
mixture is the exact support theorem at the specifically verified
proper slots. Additional old maxima are accounted for before
cancellation; selected retained caps are never falsely required to
be covered by an omitted precursor.

These conditional lemmas establish only the two higher omission
bounds used by the main five-maxima theorem. No six-maxima or global
comparison, W, H30, physical law or quantum reconstruction is proved.
No scientific body or executor was used. Root retains independent
acceptance, publication and successors; RET remains paused.
