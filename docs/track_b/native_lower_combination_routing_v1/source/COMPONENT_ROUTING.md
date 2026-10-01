# Native lower component routing for the remaining mobility coefficients

30 September 2026, Honolulu. RI228 manual conditional result for independent
review. The actual normalized H30 mobility decision remains open.

This note locates the additional size-four coefficients needed by the
accepted RI225 profiles without loading the prescribed vector. It derives
their exact potential multipliers, component roots and complete marked
routing. A key locates a fixed coefficient; it does not supply its value,
its ordinal certificate index, or its default or override status.

## 1. The fixed prefix and the new routing identities

Use the admitted RI41 notation for the size-three proper scale and the
two-chain/two-antichain seed quantities, distinguishing them from later
held probabilities:

    epsilon=1/44,  c2=1/5,  g2=1/10,  k2=11/20.

These are literal prescribed prefix constants in NORMALIZATION.md, not
newly extracted entries of its size-four certificate. Every C3 proper
probability is epsilon, and its full complement is 41/44.

Write I=C3 on r<a<b and K=I disjoint {o}. Let V be
r<a<b with r<x, and let T be r<a<b with a<x. These are the
four-event orders I plus a birth above its initial singleton and
initial pair, respectively.

Let lambda(E,S_m,R_m) be the actual unchanged RI41 component coefficient
at that minimum root key. This names a coordinate, not a numerical query.
The new routing identities are

    alpha_empty=(5/44)*lambda(2,3,0),
    alpha_singleton=(5/44)*lambda(6,3,0),
    alpha_pair=(5/44)*lambda(70,3,0),

    gamma_i=(1/8)*lambda(70,9,i),       i=0,1.                (C1)

The existing ratio alpha_I=w/e_I additionally has the exact routing

    alpha_I=lambda(70,7,0).                                 (C2)

Here w=e_C4 and e_I=epsilon, as in RI223/225. No value of w is
chosen or calculated in (C2). Equations (C1)-(C2) name four distinct
empty-component roots and two distinct exceptional root sectors.

The complete ratio equations alone do not identify any of these six
coefficients with one another. Their terminal types or compulsory
record mark differ. In particular none is set to RI41's default1/8
merely because its override status is not known.

## 2. Potentials for the three strict-prefix empty ratios

For each of K,V,T, empty birth omits exactly two maxima. Its singleton
deletions leave the following size-three orders:

| Four-parent | Single maximum deletions | Double deletion |
| --- | --- | --- |
| K=C3 disjoint A1 | C3; edge disjoint A1 | C2 |
| V=three-chain with root branch | C3; rooted fork | C2 |
| T=three-chain with branch above its middle | C3; C3 | C2 |

Every displayed size-three empty probability is epsilon in the
prescribed RI41 prefix table, and the C2 empty probability is c2.
Thus all three empty potentials are epsilon^2/c2. Their probabilities
are that potential times their respective actual component coefficient.
Division by e_I=epsilon gives epsilon/c2=5/44 in (C1).
No component coefficient has been evaluated by that hand cancellation.

These products restrict each parent, precursor and marking together.
The empty precursor has no selected marks; this observation removes
record dependence from its value, not from the original record domain.

## 3. Complete presentations of the three empty components

An empty birth from a four-parent P has terminal P disjoint {z}.
Every presentation of that terminal is obtained by deleting one of
its maxima. The complete list for the three cases is:

| Terminal | Deleted newborn maximum | Remaining parent and selected precursor |
| --- | --- | --- |
| C3 disjoint {o,z} | o or z | K, empty |
| C3 disjoint {o,z} | chain top b | C2 disjoint A2, selected C2 |
| V disjoint {o} | isolate o | V, empty |
| V disjoint {o} | root-branch tip x | K, selected {r} |
| V disjoint {o} | long-arm tip b | rooted fork disjoint A1, selected arm {r,a} |
| T disjoint {o} | isolate o | T, empty |
| T disjoint {o} | either fork tip b or x | K, selected initial pair {r,a} |

Each repeated deletion is a separate role. No other parent exists for
these components: a possible newborn must be maximal, and all maxima
are listed. Ratio edges preserve the full terminal order, so a longer
path cannot introduce another terminal or an unlisted presentation.

Each nonempty-precursor presentation connects directly to an empty
presentation. Use the terminal with its isolate o and selected non-isolate
maximum v deleted as the common size-three base. The two new precursors
are empty and past(v). The full marked diamond connects the two roles.
For every base marking, retain both newborn bits and both ordered
precursor pairs. The empty local node forgets all selected marks because
there are none, so the complete graph joins every optional selected
record at the other roles into this same component.

This proves one complete component for each of the three terminal
types. It does not infer component identity merely from a shared
probability value. The terminals are nonisomorphic:
C3 disjoint two isolates has three connected components; the other two
have a four-event connected component and an isolate, and their unique
branch point is at different depth.

## 4. Exact minimum keys without a graph engine

Use precisely RI41's four-carrier convention

    E=sum_(v<w in the order) 2^(4*pi(v)+pi(w)),
    S_m=sum_(v in precursor) 2^pi(v),
    R_m=sum_(marked v in precursor) 2^pi(v).

The sum for E is over strict order relations, not cover edges.
The admitted RI189 topological-minimum lemma applies: a non-topological
labeling can be lowered by swapping a backwards-related pair at the
greatest offending source label. It is enough to inspect the fixed
topological labelings here, not to enumerate a graph.

The relevant minimum E values are:

| Parent | Minimum E and its labeling reason |
| --- | --- |
| C2 disjoint A2 | 2; put its only relation at 0<1 |
| rooted fork disjoint A1 | 6; root0 and two tips1,2 give2+4 |
| K=C3 disjoint A1 | 70; chain0<1<2 gives2+4+64 |
| V | 78; admitted RI189 minimum2+4+8+64 |
| T | 206; admitted RI189 minimum2+4+8+64+128 |
| C4 | 2254; admitted RI189 four-chain minimum |

For the fork disjoint isolate, the other isolate positions give E=10,
12 or192, so6 is minimal. For K the four positions of the isolate
give respectively70,138,2060,2240 when it is placed after all chain
vertices, before the chain top, after the root, or before the root.
These are manual fixed-order comparisons, not automatic canonicalization.

In the first terminal, E=2 beats K's70; the selected C2 mask is3.
In the second, the fork's6 beats K's70 and V's78; choose either
selected arm as mask3. In the third, K's70 beats T's206, and its
selected initial pair has mask3. The complete empty-role connectivity
allows the all-zero selected marking in each case. This proves roots
(2,3,0), (6,3,0), (70,3,0).

For (C2), the terminal is C4 disjoint an isolate. Its only presentations
are C4 at empty and K at the full three-chain precursor I. K has
E=70 rather than2254, and its precursor mask is7. The same empty
diamond joins all three selected chain marks, giving root(70,7,0).
The C4 empty potential is epsilon by unique-maximum deletion, so
e_C4=epsilon*lambda(70,7,0), proving (C2).

## 5. Complete routing of the two gamma sectors

In K=r<a<b disjoint {o}, gamma is the probability of precursor {r,o}.
Its terminal after birth x is

    r<a<b,    r<x,    o<x.

Its only maxima are b and x. Deleting x recovers K with precursor
{r,o}. Deleting b gives the four-parent N with relations

    r<a,    r<x,    o<x,

and selected precursor {r,a}. No other presentation is possible.

The common size-three base for the full diamond is r<a disjoint {o}.
The newborns are b above {r,a} and x above {r,o}. At fixed root bit i,
the mark on a and the mark on o vary independently. Thus each of the
two K local nodes (the o bit) connects to each of the two N local
nodes (the a bit). Every newborn bit is retained; reversing the
ordered pair yields the same required scalar equality, not a new
permitted record quotient.

The root r is the intersection of the strict pasts of the two terminal
maxima. Its bit survives every presentation and edge. It is intrinsically
distinguished from o by its longer chain. Therefore the two i sectors
are distinct components; all other selected bits are connected within
each sector. This is a complete finite routing argument.

The five topological labelings of N have E values:

| Vertex order | Relation-bit sum |
| --- | --- |
| r,o,a,x | 4+8+128=140 |
| r,o,x,a | 4+8+64=76 |
| r,a,o,x | 2+8+2048=2058 |
| o,r,a,x | 8+64+128=200 |
| o,r,x,a | 4+64+128=196 |

Thus the smallest N value76 is still larger than K's70.
In K's minimizing labeling the chain is0,1,2 and o is3, so {r,o}
has mask9. Its minimum selected mark at fixed root i is i, because
the o bit may be zero in the same connected component. The roots
are exactly(70,9,0) and(70,9,1).

The gamma precursor omits only the chain maximum b. Its potential
is consequently the prescribed size-three probability of {r,o}
in an edge r<a disjoint {o}. RI41's literal table gives

    u_gamma=epsilon*k2/g2
           =(1/44)*(11/20)/(1/10)=1/8.                     (C3)

Combining this with the actual component coefficient proves the
last line of(C1). This uses the fixed prefix formula, not a new
size-four table or a guessed certificate index.

## 6. Bounds and the exact remaining value premise

RI41's admitted finite result states min_c lambda_c=1/8 for its
unchanged witness. It gives, without resolving a new coordinate,

    alpha_empty,alpha_singleton,alpha_pair >=5/352,
    alpha_I>=1/8,          gamma_i>=1/64.                   (C4)

Equality is not asserted at any named root. Strict baseline
normalization supplies the other coupled restrictions; none of
these coefficients may be varied independently to fit N16-N17.

The three newly located empty coefficients and the two gamma
coefficients are exact unresolved RI41 roles:

    lambda(2,3,0), lambda(6,3,0), lambda(70,3,0),
    lambda(70,9,0), lambda(70,9,1).

The preexisting alpha_I also has routing(C2). No ordinal index,
default/override status, numerical value, monotonicity or spacing
is inferred from these keys. RI41's discovery narrative and the
existence of a default are not premises selecting any of them.

The companion [LOWER_COMBINATIONS.md](LOWER_COMBINATIONS.md) proves
that every beta_S equals theta*alpha_S and identifies the actual
canonical coefficient retained by zeta. Together these are substantive
native reductions of RI225's missing lower combinations. They are not
a completed normalized mobility witness or a proof that those
remaining values cannot be derived analytically.

All original records, fair newborn-bit maps, individual ideal
occurrences, actual rho/s, canonical corrections, seed and support
remain unchanged. No graph engine, coefficient extraction, scientific
body/certificate/vector, mathematical automation or successor was used.
