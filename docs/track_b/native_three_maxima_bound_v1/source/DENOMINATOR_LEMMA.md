# Covering precursors bound the triple denominator

30 September 2026, Honolulu. Manual lemma for independent review.

Let R be ANY three-event order with arbitrary binary marks. Let E1,E2,E3
be ideals whose union is R, and Q_i=R+i_Ei be its marked four-event
extensions, with arbitrary cap bits. For every ideal A of R, including
empty and full R, put B(A)=q_R(A) and q_i(A)=q_Q_i(A). Then the unchanged
native prefix satisfies

    q_1(A) q_2(A) q_3(A) >= B(A) epsilon^2/16,
    epsilon=9/681472.                                            (D1)

The proof is pointwise and keeps the covering condition; it is not three
independent applications of the floor. It uses the explicitly admitted
inherited RI41 finite facts

    q4(S)>=epsilon for ALL ideal slots,
    q4(S)=alpha_c u4(S)>=u4(S)/8 for PROPER slots only.           (D2)

Neither finite theorem is reverified here. A is always proper in Q_i,
even when A=R. Thus every use of the second inequality below is in its
proper-slot domain. No formula for u4 at a full four-parent is invoked.

## 1. Fixed seed and two sufficient reductions

Use the literal accepted prefix, with all indicated record choices:

    a=2/3, c=1/5, d=1/4, g=1/10, e=1/44,
    f_s in {1/6,1/3},       h_s in {19/30,7/15}.

The singleton row is (a,1-a), the two-chain row is (c,f_s,h_s),
and the two-antichain row is (d,g,g,k), k=11/20. In every three-parent
the empty probability is e. The other proper three-parent entries used
below are exactly RI41's fixed definitions:

| Shape and selected ideal | Probability |
| --- | --- |
| A3, one vertex | e*g/d |
| A3, two vertices | e*k/d |
| edge s<t plus isolate u, ideal {s} | e*f_s/c |
| same parent, ideal {u} | e |
| three-chain, root | e |
| fork s<t,s<u, root | e |
| join s<v,u<v, either root | e |

No record vector is substituted. f_s is the fixed seed entry selected by
the actual bit at s; every estimate is valid for both values. Other old and cap bits
remain arbitrary; their absence from a displayed seed entry follows from
the literal prefix and precursor locality, not deletion from the domain.

Write u_i(A)=u4(Q_i,A). Since 8*44^3=681472, we have

    epsilon=9e^3/8,       nu=4epsilon=(9/2)e^3.                  (D3)

If an extension has no omitted maximum except its new cap, its potential
is B(A). Then (D2) gives q_i(A)>=B(A)/8; the other two factors are each
at least epsilon, proving the stronger product B(A)epsilon^2/8.

Alternatively, it suffices to find two DISTINCT indices i,j such that

    u_i(A)u_j(A) >= nu B(A).                                    (D4)

Indeed (D2) gives q_i q_j>=nu B/64=B epsilon/16, and the third actual
probability is at least epsilon. Repeated precursor values are allowed;
indices still denote distinct cap occurrences, not independent scales.

## 2. Immediate cases and exhaustive shape reduction

If some E_i=R, its cap is the unique maximum of Q_i. Every A in J(R)
omits only that maximum, so the first reduction applies.

If |A|>=2, there is at most one vertex of R outside A. If there is one,
the covering condition places it in some E_i; any remaining old maxima
of Q_i then lie in A. If A=R this holds for every i. Again the new cap
is the only omitted maximum and the first reduction applies. This
explicitly includes the full R term without using a full-slot potential.

It remains to consider empty or singleton ideals, with every E_i proper.
Up to isomorphism there are exactly five three-event orders: a chain,
a join, a fork, an edge plus an isolate, and A3. To check completeness,
zero relations give A3, one gives the edge plus isolate, two without a
third transitive relation give fork or join, and a comparable length-two
path forces the full chain. Chain and join have a unique maximum; a
covering ideal containing it must be R, already handled. The remaining
three shapes and all their empty/singleton ideals are treated below.

## 3. Fork base

Let R have s<t and s<u. Without a full precursor, covering both tips
requires two selected precursor ideals E={s,t} and F={s,u}. The only
remaining ideals A of size below two are empty and {s}. For both B=e.
The two extension parents are a three-chain with a leaf at the root.
Deleting their two omitted maxima gives

| A | u_E(A) | u_F(A) | u_E(A)u_F(A)/B(A) |
| --- | --- | --- | --- |
| empty | e^2/c | e^2/c | 25e^3 |
| {s} | e^2/f_s | e^2/f_s | e^3/f_s^2 >=9e^3 |

For example, at {s} the two singleton deletions give the fork-root and
chain-root entries e,e; the double deletion gives the two-chain root
entry f_s. At empty the same double-deleted parent contributes c.
Both product ratios exceed nu=(9/2)e^3, proving (D4) for all marks.

## 4. Edge plus isolate base

Let R have s<t and isolated u. Since no precursor is full, coverage
requires one E={s,t} and another F equal to {u} or {s,u}. The possible
small ideals are empty, {s}, {u}. Direct maximal deletions give

| A | B(A) | u_E(A) | u_F(A) |
| --- | --- | --- | --- |
| empty | e | e^2/c | e^2/d, for either F |
| {s} | e*f_s/c | e^2/c | e^2*f_s/(c*g), for either F |
| {u} | e | e | e^2*f_u/(c*g) if F={u}; e^2/g if F={s,u} |

For E, the two-maxima deletion parents are R and the three-chain,
with two-chain double deletion. At {u}, u itself is a selected maximum,
so the only omitted maximum is the new cap and u_E=B=e.
For F, the deletion opposite R is either an edge plus isolate or a join;
the double deletion is the two-antichain on {s,u}. The selected entry
is its g for either singleton and d for empty. These descriptions give
every numerator and denominator in the table, with f_s and f_u retaining
their separate old bits.

The three product ratios u_E u_F/B are respectively

    20e^3,       50e^3,
    e^2*f_u/(c*g) or e^2/g.

In the last line f_u/(c*g)>=25/3>1 and 1/g=10>1. Thus that ratio is
at least e^2>nu, since (9/2)e=9/88<1. The other two ratios also exceed
nu. This proves (D4) for both choices of F and every permitted marking.

## 5. Antichain with a covering pair

Let R=A3. If two proper precursors cover R, they are either two distinct
two-vertex subsets, or a two-vertex subset and its complementary singleton.
No other proper pair can cover three vertices. Let u_E denote the potential
for an extension above E.

At A=empty the needed values are

    B=e,
    u_E=e^2/d=4e^2                    if |E|=2,
    u_E=e^3*a/(c*d^2)=(160/3)e^3       if |E|=1.                (D5)

The pair case has two omitted maxima, with three-antichain and join
single deletions and two-antichain double deletion. The singleton case
has three omitted maxima: its singleton deletions give three e factors,
its pair deletions give c,d,d, and its triple deletion gives singleton
empty entry a. Thus all alternating factors in (D5) are retained.

For two pair precursors u_E u_F/B=16e^3>nu. For a pair and complementary
singleton it is (640/3)e^4>nu: after canceling e^3, this is
640/(3*44)>9/2, equivalent to 1280>1188.

For A={s}, write B=e*g/d=(2/5)e. The complete needed values are

| Precursor E | u_E({s}) |
| --- | --- |
| pair containing s | e^2/d=4e^2 |
| pair excluding s | B |
| singleton other than s | e^2/d=4e^2 |
| singleton {s} | e^3*(1-a)*f_s/(c^2*d*g)=(1000/3)f_s e^3 |

For a pair containing s, the two singleton deletions give B and a join
root entry e; the double deletion gives g. The same quotient B*e/g
applies to a singleton other than s, with an edge-plus-isolate entry e
instead of the join. A pair excluding s leaves only its cap omitted,
so the potential is B. For E={s}, there are three omitted maxima. Its
singleton deletions contribute B,(e*f_s/c),(e*f_s/c); its pair deletions
contribute g,g,f_s; and its triple deletion contributes singleton FULL
probability 1-a. Their full product is exactly the last table entry.
This use of a full smaller-parent probability is part of the legitimate
proper four-parent deletion product, not a full four-slot scale formula.

If both covering pairs contain s, the product ratio is 40e^3. If one
pair excludes s, the other pair contains it and the ratio is 4e^2>nu.
For a pair and complementary singleton, either both relevant potentials
are 4e^2, giving 40e^3, or the pair excludes s and the ratio is
(1000/3)f_s e^3>=(500/9)e^3>nu. Thus every covering pair satisfies (D4).

## 6. Antichain requiring all three precursors

Suppose no two proper precursors cover A3. If one had two vertices,
another would contain the missing vertex and form a covering pair.
Therefore all three must be distinct singleton precursors; none can be
empty. These are the only cases not yet covered.

For A={s}, choose the two precursor singletons other than s. The preceding
table gives both potentials 4e^2 and B=(2/5)e, so their product ratio is
40e^3>nu. They need not themselves cover R: they already satisfy (D4)
for this particular A. The third factor retains the actual floor.

For A=empty, every potential is (160/3)e^3 by (D5). Applying the three
proper-slot scale bounds gives

    q_1(A)q_2(A)q_3(A)/B(A)
        >= (160/3)^3 e^8/512
         > 81e^6/1024 = epsilon^2/16.                           (D6)

The strict hand comparison is (160/3)^3 e^2>81/2. Indeed 160/3>50 and
44^2=1936<2000 give (160/3)^3 e^2>50^3/2000=125/2>81/2.
No new coefficient lookup, vector evaluation or scientific-body read was used.
Empty-precursor locality makes these particular seed factors independent
of marks; the original six-event record domain is unchanged.

## 7. Conclusion and scope

The immediate cases cover every |A|>=2 and every full precursor; the
chain and join necessarily have a full precursor. Sections 3-6 cover
all remaining fork, edge-plus-isolate and antichain possibilities and
all empty/singleton ideals, including repeated precursor cases whenever
compatible with coverage. This proves (D1) for every natural labeling by
the inherited marked-parent equivariance. No graph enumeration or new
scientific body was used.

The fixed coefficients were never treated as freely selectable. Only
their accepted uniform lower theorem was used; their exact values, shared
components and all mark dependence remain the original ones. In particular
the minimum alpha bound is not assigned to a full four-parent slot.
The [main proof](THREE_MAXIMA.md) applies (D1) to the exact triple-omission
product. This lemma alone makes no global M6 or actual W claim.
