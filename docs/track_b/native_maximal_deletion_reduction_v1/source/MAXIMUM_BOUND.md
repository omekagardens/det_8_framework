# RI199 global maximum target and canonical overlap remainder

30 September 2026. Manual analytic submission for independent root review.

The assigned sufficient target is correct, including equality:

    M6 <= T,       T = 4lambda*j0/v - 1/2,
    implies W(rho,s)>0.

This packet does not establish that global inequality or a parent exceeding
it. It establishes three reductions before identifying the remaining native
dependency: T>13/(10theta)-1/2>1867/10; every six-parent with a unique maximum
has complete potential sum exactly 1; and the unresolved contribution can
be written as an explicit fixed-canonical overlap remainder for parents
with two through six maxima. A concrete two-cap family retains its complete
singleton correction and is below the target. No freely varied law or
new containing cap substitutes for the global comparison.

## 1. Independent check of the assigned target

Use the complete RI145 identity, with all symbols from the unchanged law:

    W(x,y)/r = -1
      +12lambda*[G_*x^2*(1-yU20(x))/q(x)
                 +j0*x*(1-yU30(x))/((1-x)*v)]
      +12y*x^2*(1+eta)*(j0+G_*x).

The actual pair satisfies 0<rho<=R and 0<s<=1/d(rho), where
d(x)=6-4x+2x^2. RI178 proves C30(x)=1-U30(x)/d(x)>2/3, while U30>0.
Consequently 1-yU30(x)>=C30(x)>2/3. The retained core contribution is
strictly positive because G_*,x,q and 1-yU20 are positive; the final term
is strictly positive as well. Multiplying only positive factors gives

    W(x,y)/r > -1 + 8lambda*j0*x/((1-x)*v).

At the actual scale rho=1/[2(1+M6)], positive algebra gives

    rho/(1-rho)=1/(1+2M6),
    W(rho,s)/r > -1 + 8lambda*j0/[v*(1+2M6)].       (1)

If M6<=T, then v*(1+2M6)<=8lambda*j0, so the right side of (1) is
nonnegative and W>0 strictly. At M6=T, strict positivity still follows;
neither equality nor the omitted positive contributions have been lost.
No M7 selection, actual s evaluation or replacement q has entered the proof.

Equivalently, the target asks for the actual lower scale bound
rho>=v/(v+8lambda*j0). Earlier upper caps on rho do not supply it.
Failure of M6<=T would invalidate only this sufficient route. It would not
prove W<=0. Conversely W>0 would remove only this weighted obstruction,
not prove both C2,C3 positive or the full shared H30 system feasible.

## 2. A same-law lower bound on the target

RI197 has already established the two original component values
alpha_7,0=197/200 and alpha_7,1=983/1000. RI187's fixed chain identity
b_i=(41/44)*alpha_7,i therefore gives b1/b0=983/985. No new coefficient
is read, selected, fitted or recomputed from a scientific body.

Let t=2/985, only an algebraic abbreviation for this accepted ratio gap.
The actual lambda satisfies

    lambda=1-(983/985)^3=3t-3t^2+t^3
           >3t*(1-t)=5898/970225 >3/500.             (2)

The last hand comparison is 5898*500=2949000 >2910675=3*970225.
RI187 and the accepted RI197 premises retain

    0<v<2theta*D_-,       0<D_-<U=1147/126280,
    j0>71/72,            0<theta<1/144.

All are coupled facts about the same law, not independently chosen ranges.
Using only positive denominators and the strict upper bound on v,

    4lambda*j0/v > 2lambda*j0/(theta*U)
      >53795280/(41292000*theta) >13/(10theta).

Here 53795280=6*71*126280 and 41292000=500*72*1147.
The final hand cross-product is
10*53795280=537952800 >536796000=13*41292000. Hence

    T >13/(10theta)-1/2 >1867/10.                   (3)

This is a proved lower bound on the assigned target, not a new estimate
of M6 or an assertion that a generic upper cap holds. The exact target T
continues to control every parent comparison below. Theta remains the
actual 1/[72(1+M5)]; no numerical M5 or theta is substituted.

## 3. Complete global domain and maximal deletion partition

For every six-element parent P, every binary record r_mark on P and every
proper ideal S, define O(P,S)=Max(P) minus S. Every proper ideal omits a
maximum: otherwise it contains the downsets of all maxima and therefore P.
Thus O is nonempty. The unchanged RI38 potential is exactly

    u(P,r_mark,S)
      = product over nonempty H subset O
          q(P minus H, r_mark restricted to P minus H, S)
             ^((-1)^(|H|+1)).                      (4)

All q in (4) have parent size at most five and are the actual strict law.
Every denominator is positive. If P minus H is empty, its unique full
probability is 1. The global maximum is

    U6(P,r_mark)=sum over all proper ideals S of u(P,r_mark,S),
    M6=max over all six-parents and all records of U6(P,r_mark). (5)

No parent family, supported component or isomorphism orbit replaces this
maximum. Repeated canonical keys still contribute once per labeled ideal.
In particular A6 is an admissible competitor, not an assumed maximizer.

Write m=|Max(P)| and Q_d=P minus d for each maximal d. Let J_d be the
set of ideals of Q_d containing every vertex of Max(P) other than d.
An ideal of Q_d is an ideal of P excluding d, since d is maximal.
Therefore J_d is exactly the set of proper P ideals whose O is {d}.
For every such ideal, (4) has one factor: q(Q_d,S).

Retain the entire normalized Q_d row and define the omitted row mass

    L_d(P,r_mark)=sum over ideals A of Q_d outside J_d of q(Q_d,A),
    L(P,r_mark)=sum over d in Max(P) of L_d(P,r_mark),
    C(P,r_mark)=sum over proper P ideals S with |O(P,S)|>=2 of u(P,r_mark,S).

Every record restriction is the original one in (4), even when notation
suppresses it. Since the complete Q_d row sums to 1, the exact identity is

    U6(P,r_mark)=m-L(P,r_mark)+C(P,r_mark).           (6)

The J_d groups are disjoint, and their complement is precisely the C sum.
No ideal, full complement, mark or correction has been dropped. Full Q_d
is in J_d. For m>=2, empty is outside J_d and has positive probability;
hence 0<L_d<1, 0<L<m and C>0. The latter includes the positive empty-ideal
term with O=Max(P). These strict signs do not select the sign of C-L.

## 4. Every unique maximum row is settled

When m=1, J_d is the complete ideal set of Q_d. Thus L=0 and C=0,
and (6) gives

    U6(P,r_mark)=1<T                              (7)

for every such parent and every record. Equivalently, every proper ideal
of a finite order with a unique maximum omits that vertex, so (4) is the
complete preceding row. This is not restricted to chains or to a record
representative and uses no graph enumeration. These parents cannot be
counterexamples to the assigned sufficient bound.

The unsolved part of (5) remains every parent with 2<=m<=6, with every
record and ideal. Equation (7) does not justify assuming that one selected
multi-maximal family attains the remaining maximum.

## 5. Concrete two-cap check with the canonical term retained

Consider the admissible parent P=C4 ordinal-sum A2: a four-chain
0<1<2<3 below two incomparable caps 4 and 5. Take the two concrete records
with root bit i=0 or 1 and all other bits zero. This subsection treats
those actual records; it does not silently settle the other records.

There are exactly seven proper ideals. Five are the full set of C4 ideals
S=0,1,3,7,15, omitting both caps. The other two ideals contain the complete
C4 stem and exactly one cap. Deleting either cap leaves C5; deleting both
leaves C4. Let B_i(S) be the complete C4 row and D_i(S) the proper C5 row.
The accepted RI120 prefix lemma retains

    D_i(S)=theta*B_i(S) for S=0,3,7,15,
    D_i(1)=theta*p_i+N_i,
    ell_i=q(C5,full)=1-theta-N_i,
    sum over S=0,1,3,7,15 of B_i(S)=1.

The two cap-deleted rows have the same chosen record, but their two
one-cap ideal occurrences remain distinct. Applying (4) to every ideal gives

    U6(P,i)=sum_S D_i(S)^2/B_i(S)+2ell_i
           =theta^2+2theta*N_i+N_i^2/p_i+2(1-theta-N_i)
           =1+ell_i^2+N_i^2*(1/p_i-1).              (8)

The final expression is the already bounded RI157 F_i, not a newly
discovered cap. Its same-law proof gives

    U6(P,i)=F_i<35743/12100<71/24<T.                 (9)

This supplies a complete check against the present target for two actual
marked parents. It is not a global M6 bound or a new counterexample. The
canonical N_i^2/p_i overlap term in (8) is essential; replacing the C5
row by restoration alone would give a different result. At N_i=0 the
identity still holds, and no zero canonical coordinate is divided by.

## 6. Exact fixed canonical form of the remaining overlap

Let c(Q,A,r) denote RI63's actual size-five ratio component, with the whole
parent and transported precursor marks retained. Define the held coefficient

    beta_c=(35/36)*alpha_c^(min,5)>=0,
    q(Q,A)=u5(Q,A)*(theta+beta_c(Q,A,r)) for A proper in Q. (10)

The canonical vector is the unique prescribed lexicographic optimum on
the accepted full optimal face, not an arbitrary primary optimum. All 798
coordinates and their actual component incidence remain binding; the
known count of 69 positive coordinates is not their joint incidence map.

For a term S in C, let O=O(P,S), k=|O|>=2 and
c_d=c(Q_d,S,r_mark restricted to Q_d). S is proper in every Q_d, because
at least one other omitted maximum remains. Separating the singleton H
factors in (4) and substituting (10) gives the exact positive coefficient

    K(P,r_mark,S)
      =[product over d in O of u5(Q_d,S)]
       *[product over H subset O with |H|>=2
             of q(P minus H,S)^((-1)^(|H|+1))] >0,

    u(P,r_mark,S)=K(P,r_mark,S)*product over d in O of (theta+beta_c_d),

    C(P,r_mark)=sum over S with |O(P,S)|>=2
                   K(P,r_mark,S)*product over d in O(P,S) of (theta+beta_c_d). (11)

K depends only on the unchanged layers through size four: u5 itself uses
those layers. Every smaller-law factor in the parity product is retained.
All denominators are positive strict-prefix probabilities, not boundary
probabilities that might vanish.

For L, every A outside J_d is proper in Q_d because full Q_d belongs to
J_d. Therefore its exact companion is

    L(P,r_mark)=sum over d and A outside J_d
                   u5(Q_d,A)*(theta+beta_c(Q_d,A,r)). (12)

Equations (11)-(12) are a fixed-canonical product description, not a
new coefficient array or computational reconstruction. Repeated c_d values
give repeated factors, not independently variable coordinates. Expanding
one product by hand would give

    product_d(theta+beta_c_d)
      =sum over A subset O of theta^(k-|A|)*product over d in A of beta_c_d.

Thus k>=2 does not imply an O(theta^2) bound: nonzero canonical factors
can leave constant or linear powers of theta. The everywhere-neutral
support theorem may set a particular beta to zero when a raising role is
proved in its component; it does not set every beta in (11) to zero.

In particular the canonical singleton block remains

    N_i=(35/1476)*[41p_i-f_i/2-min{g_(i,0),g_(i,1)}]_+/c_i,
    omega_i=44theta*p_i.

Its zero branches, tied minima, normalization and all product contrasts
remain. They are not replaced by independent bounds on N_i or by a freely
variable beta box.
The complete weighted polynomial also remains

    q(x)=(1-theta*x^2)*v
       +(2-theta-2theta*x+theta^2*x^2)*Delta h
       +(3-2theta-2x+theta*x^2)*Delta j
       +(x-2)*Delta N+2Delta(N*omega)-theta*x^2*Delta(N*omega^2).

Delta is record1 minus record0, with contrasts of whole products. The
target check in section 1 used the proved positivity of this exact q;
none of these terms was deleted from the law.

## 7. Precise remaining native dependency

Combining (3), (6) and (7), the exact unresolved comparison is now

    For every six-parent P with 2<=m<=6 and every record:
        C(P,r_mark)-L(P,r_mark) <= T-m,               (13)

with C and L given by (11)-(12), not unspecified residual symbols.
Equation (13) is equivalent to the assigned global bound after the settled
unique-maximum rows are removed. It is not a proposed generic containing cap.
A concrete violation would require an actual admitted marked parent and
the strict opposite of (13), not a free choice of its canonical factors.

The one-deletion sector cannot produce a counterexample by itself: its
sum is m-L<m<=6. More quantitatively, any counterexample must have

    C > T-m+L > 1807/10,                            (14)

using T>1867/10, m<=6 and L>0. This lower requirement on a violating
overlap sum is a consequence, not a claimed upper bound on C.

The missing native-law input is a proved joint contraction of the fixed
canonical components across all maximal-deletion cards in (11), against
the same cards' exact loss (12) and the unchanged theta,v,lambda,j0. An
explicit dependency map for such a proof is

    (P,r_mark,S,d) -> (c(Q_d,S,r_mark restricted to Q_d), u5(Q_d,S)),

together with the actual smaller-law parity factors in K and the accepted
canonical alpha^(min,5). Row normalization controls the one-card sums used
in L. The currently selected analytic results do not supply the required
joint degree-two-through-six product inequality or a violating marked
parent. The single C5 canonical block controls (8), not every card in (11).
The 69-active count and neutrality classification alone do not identify
which shared coordinates occur simultaneously in those products.

This is the exact remainder after exhaustive one-deletion normalization,
not a theorem of nonderivability from DET or from the full prescribed law.
No claim is made that a further manual proof cannot settle it. No new
scientific body or canonical vector was read to construct the missing
projection, and no graph/LP/numerical computation was run. Neither the
complete global upper bound nor a same-law parent above T is established
by this packet; consequently actual W remains undecided.

## 8. Evidence and stop

Exact read sources and inherited acceptance are bound in
[SOURCE_REFERENCES.json](SOURCE_REFERENCES.json). RI197's accepted audit
supplies the two values used in (2); its certificate is not reread. RI63's
accepted analytic definitions supply (4) and (10); no scientific certificate,
canonical table, numerical M5/M6, runtime or verifier is evaluated.
The 423-file inherited manifest is retained by exact reference, with no
claim of a fresh traversal of all its scientific or opaque descendants.

All parents, records, ideals, canonical minima, positive parts, shared T1,
other eight connected parents, five Di and original P2/P3,Y=1/4 remain.
The 92/34/35 and 31/139/20/42 executable-route obligations are unchanged
and uncredited. RET remains paused. No completed packet, repository, Git,
fixture, card, runtime, new agent/thread or physical claim is changed.
Root owns independent review, publication and any successor. Stop at the
bounded analytic result and precisely identified remaining dependency.
