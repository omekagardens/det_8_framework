# RI189 — exact routing of the six selected C4 component roles

30 September 2026, Hawaii. Manual source-author proof, not independent
acceptance. The prescribed size-four vector is fixed and not instantiated.

## 1. Result and novelty boundary

The accepted RI168 incidence theorem already classifies the C4 initial
singleton, pair and triple families as two, four and eight components:

\[
 P_i,\qquad S_{i,u},\qquad B_{i,u,v},\qquad i,u,v\in\{0,1\}.
\tag{1}
\]

The six roles used by RI187 are \(P_0,P_1,S_{0,0},S_{1,0},B_{0,0,0},
B_{1,0,0}\). This note does not relabel the inherited classification as
a new discovery. Its new routing result is the exact minimum-key map in
the original RI41 convention:

\[
\begin{split}
 \operatorname{root}(P_i)&=(78,7,i),\\
 \operatorname{root}(S_{i,u})&=(206,7,i+2u),\\
 \operatorname{root}(B_{i,u,v})&=(2254,7,i+2u+4v).
\end{split}
\tag{2}
\]

Each selected root-record pair has consecutive ranks in the sorted
component-root list, without determining either numerical rank. Neither
consecutiveness nor a component key implies a coefficient order or gap.
No coefficient, default/override status or table index is evaluated here.

The exact diamond witnesses below close the intrinsic routing question.
They cannot join the six selected roles to one another: terminal type and
compulsory trunk marks prohibit such paths. The remaining RI187 decision
therefore needs a quantitative statement about the fixed coefficients at
the named keys, not an assumed undiscovered diamond identification.

## 2. All presentations of the three terminal types

Write the four-chain as \(r<a<b<c\), with marks at the first three
vertices \((i,u,v)\). Its natural predecessor masks are \((0,1,3,7)\).
Appending a new maximum \(x\) above the selected initial ideal gives

| C4 ideal | Five-event terminal, exact relations | Compulsory trunk | Maxima |
|---|---|---|---|
| 1 | \(r<a<b<c\), \(r<x\) | \(r\) | \(c,x\) |
| 3 | \(r<a<b<c\), \(a<x\) | \(r<a\) | \(c,x\) |
| 7 | \(r<a<b<c\), \(b<x\) | \(r<a<b\) | \(c,x\) |

Equivalently these are
\(C_1\oplus(C_3\sqcup C_1)\),
\(C_2\oplus(C_2\sqcup C_1)\), and \(C_3\oplus A_2\).
The unique branching vertex has distance zero, one or two from the unique
minimum in the cover graph. Hence the terminal orders are pairwise
nonisomorphic even before marks are considered.

The compulsory trunk is the intersection of the strict pasts of the two
maxima. Every trunk vertex survives either maximal deletion and belongs
to the selected precursor in that presentation. Its ordered marks cannot
be erased by local-node formation or changed by a marked isomorphism.
Thus all one, two or three trunk bits, not only the root bit, are graph
invariants for the respective families.

Define the two alternative parent shapes

\[
 V=(r<a<b,\ r<x),\qquad T=(r<a<b,\ a<x).
\]

Their predecessor masks in order \((r,a,b,x)\) are respectively
\((0,1,3,1)\) and \((0,1,3,3)\). Deleting a possible newborn maximum
exhausts every parent presentation:

| Terminal family | Delete \(x\) | Delete \(c\) |
|---|---|---|
| singleton | C4, selected \(\{r\}\) | V, selected long arm \(\{r,a,b\}\) |
| pair | C4, selected \(\{r,a\}\) | T, selected arm \(\{r,a,b\}\) |
| triple | C4, selected \(\{r,a,b\}\) | C4, selected \(\{r,a,b\}\) |

T's other arm is an isomorphic local role but a second distinct ideal in
its full row. V has no nontrivial automorphism. T exchanges its two tips,
not the two ordered stem vertices. The triple terminal exchanges its two
maxima, not its three ordered trunk vertices.

This is also an all-parent completeness proof for each target component.
Every appended event is maximal; every representation must therefore be
one of the two maximal deletions shown. Every ratio edge preserves the
terminal order. A longer path cannot acquire a hidden parent role or
cross between the three terminal types.

## 3. Finite marked diamond certificates

Use the old base C3 on \(r<a<b\), marks \((i,u,v)\), and arbitrary
newborn bits \(t,w\). Its accepted proper probabilities for masks 1
and 3 are \(e=1/44\), and its full probability is \(A=41/44\).
Every instance retains both newborn bits; the scalar quantum maps include
the same factor \(1/4\) on both complete routes.

### Singleton

For ordered precursor pairs \((1,7)\) and \((7,1)\),

\[
 e\,q_V(7;i,u,v)=A\,q_{C4}(1;i),\qquad
 q_V(7;i,u,v)=41p_i.
\tag{3}
\]

At fixed \(i\), all four V local nodes indexed by \((u,v)\) connect
directly to the one C4 singleton node. Their potential values are \(A\)
and \(e\), so they carry the same original component coefficient.
This is the complete five-node star \(K_{1,4}\). It retains
\(4\cdot4\cdot2=32\) raw diamonds per root: four old optional bit
assignments, four newborn pairs and two ordered precursor pairs.

### Pair

For \((3,7)\) and \((7,3)\),

\[
 e\,q_T(\text{arm};i,u,v)=A\,q_{C4}(3;i,u),\qquad
 q_T(7)=q_T(11)=41s_{i,u}.
\tag{4}
\]

At fixed \((i,u)\), both selected-arm tip values \(v\) connect to
the C4 pair node. The complete graph is \(K_{1,2}\), with three nodes.
The optional tip mark is removed from the *value* by the diamond through
the C4 node, not forgotten at the T node. There are
\(2\cdot4\cdot2=16\) raw instances per component. The two arms remain
two labeled normalization/height occurrences even if they have equal
local labels or values.

### Triple

The equal pair \((7,7)\) occurs once, and gives

\[
 A\,q_{C4}(7;i,u,v)=A\,q_{C4}(7;i,u,v).
\tag{5}
\]

At fixed \((i,u,v)\) there is one node and four raw loops, one for each
newborn pair. No loop changes a trunk mark. The equal precursor pair is
not doubled as though it had a distinct reverse ordering.

The six selected components consequently have 104 raw diamond instances:
\(2(32+16+4)\). Their incident-row union, as proved in RI168, is 72
raw rows or 38 canonical marked rows; the selected ideal-occurrence counts
are 92 and 56 respectively. These totals account for overlapping C4 rows
and T's two individual arms, not a sum treating each family as disjoint.
The formulas (3)–(5), the marked domains and maximal-deletion exhaustion
form a finite analytic routing witness. No global graph enumeration is
needed to verify it.

## 4. Canonical minimum-key proof

RI41 assigns to a local node the minimum over all four-carrier permutations
of the lexicographic triple

\[
 (E,S_m,R_m)=
 \left(\sum_{v\prec w}2^{4\pi(v)+\pi(w)},\quad
       \sum_{v\in S}2^{\pi(v)},\quad
       \sum_{v\in S:r_v=1}2^{\pi(v)}\right).
\tag{6}
\]

A component root is the minimum of these node keys. The order term is
primary, so first minimize \(E\).

**Topological-minimum lemma.** A minimizing labeling has no relation
whose source label exceeds its target label. Otherwise take the greatest
source label \(k\) with such a relation, with source vertex \(x\),
and a descendant \(y\) with lower label \(h\). Swap the labels of
\(x,y\). Every source row above \(k\) is unchanged: by the choice
of \(k\), it has no relation to either lower-labeled vertex. Row \(k\)
now contains the outgoing relations of \(y\). They are a strict subset
of those of \(x\), after removing the old relation to \(y\), because
the order is transitive and \(y\) cannot precede \(x\). Hence row
\(k\) decreases. All lower rows together cannot offset a decrease in
its binary block. This strictly lowers \(E\), a contradiction.

It is therefore enough to inspect the following finite topological
labelings. This is a hand proof over fixed four-vertex orders, not an
execution of a graph or canonicalization engine.

| Parent | Topological vertex order | Relation-bit sum |
|---|---|---|
| V | \(r,a,b,x\) | \(2+4+8+64=78\) |
| V | \(r,a,x,b\) | \(2+4+8+128=142\) |
| V | \(r,x,a,b\) | \(2+4+8+2048=2062\) |
| T | \(r,a,b,x\) or \(r,a,x,b\) | \(2+4+8+64+128=206\) |
| C4 | \(r,a,b,c\) | \(2+4+8+64+128+2048=2254\) |

For \(P_i\), the V nodes beat the C4 node since \(78<2254\).
The minimizing V long arm has mask 7 and mark mask \(i+2u+4v\).
The component includes all \(u,v\), so its minimum mark mask is \(i\).
This proves the first line of (2).

For \(S_{i,u}\), the T nodes beat the C4 node since \(206<2254\).
Tip exchange puts the selected arm at mask 7 rather than 11, retaining
the selected tip's actual bit. Both selected tip bits occur in the
component, so the minimum mark mask is \(i+2u\). The ordered trunk
bits cannot be interchanged. This proves the second line of (2).

For \(B_{i,u,v}\), there is only the C4 local node. Its unique chain
labeling fixes ideal mask 7 and record mask \(i+2u+4v\). This proves
the final line of (2).

Thus the requested six component roots are exactly

\[
 (78,7,0),(78,7,1),\quad(206,7,0),(206,7,1),\quad
 (2254,7,0),(2254,7,1).
\tag{7}
\]

No integer triple lies lexicographically strictly between \((E,7,0)\)
and \((E,7,1)\). Each pair therefore has consecutive ranks in the
sorted list of component minima. This determines neither the rank of
the first member nor any coefficient at that rank.

## 5. Component identity, actual value equality and the remaining premise

Write \(\alpha(E,S_m,R_m)\) for the prescribed coefficient belonging
to the component with that root key. This names an existing coordinate;
it does not load the vector or supply a default/override value. Equations
(2)–(5) give the precise selected-row routing

\[
\begin{split}
 p_i&=e\alpha(78,7,i),\\
 s_i&=e\alpha(206,7,i),\\
 b_i&=41e\alpha(2254,7,i).
\end{split}
\tag{8}
\]

The first equality is local component transport. Writing \(s_i,b_i\)
for the full actual root sectors additionally uses the inherited RI127
actual-value theorem: \(b_{i,u,v}=b_i\), \(c_{i,u,v}=c_i\), and
complete C4 normalization then gives \(s_{i,u}=s_i\). This is not a
new path connecting different \(u,v\) components. Equality of their
actual values is retained without collapsing their global identities.

Define the three selected coefficient contrasts

\[
 X=\alpha(78,7,1)-\alpha(78,7,0),\quad
 Y=\alpha(206,7,1)-\alpha(206,7,0),\quad
 Z=\alpha(2254,7,0)-\alpha(2254,7,1)>0.
\tag{9}
\]

Here \(Z\) is only this contrast, not the growth cap \(Z_6\).
The sign of \(Z\) is an inherited actual-law fact, not a property of
key ordering. The exact RI187 rejection premise becomes

\[
 X_++Y_+\le \frac{20854404}{3875}Z.
\tag{10}
\]

Since \(X_++Y_+=\max(0,X,Y,X+Y)\) and \(Z>0\), an equivalent
finite analytic certificate consists of the three inequalities

\[
 X\le LZ,\qquad Y\le LZ,\qquad X+Y\le LZ,
 \qquad L=20854404/3875.
\tag{11}
\]

Equality is retained: (10) would imply \(v<B_6\) strictly by RI187.
The strict opposite of (10) is only a necessary condition for passing
that capacity branch, not a proof of the weighted endpoint.

The complete marked diamonds prove constancy of \(q/u\) *within*
each of the components. Their terminal/trunk invariants forbid paths
between the six roots in (7). Normalization determines full complements,
not a comparison between those six chosen scales. The shared complete
row inequalities still constrain all global coordinates together. No
absence of a diamond path licenses varying the six coefficients freely.
In particular, a coefficient inequality might yet follow from the full
fixed construction; the present routing proof is not a nonimplication
theorem for that law.

The minimal unresolved dependency is now stated without a 109-vector
search: an accepted quantitative coefficient lemma implying (10), its
strict opposite, or a sufficient narrower condition on the two explicitly
named core entries. The companion main analysis investigates that
coefficient-law boundary. A new routing attempt is not needed to locate
the selected roles. This sitting neither resolves the literal selected
entries nor assumes a coefficient lattice from discovery history.

## 6. Sources and exact scope

All required predecessor documents, current authority and the current
independent manual review were read completely. The current assignment
is 2,659 bytes, SHA256
`2561837f162343aba66ca3bc96ab7b257b2b83e8132ae69215745dfc5596bc0f`;
the predecessor decision is 1,294 bytes, SHA256
`24ebf0a227877c3b6455c8b31e0310c9e9ee6c3b04e972d22b501ea5f8859a6f`.
The direct current root review is 5,812 bytes, SHA256
`bf207dcd49c14bea01ec11fe04c6b711a0f693e30d0594bb485a4c22e994a8c6`.

Fresh complete inherited analytic reads relevant to the new key proof:

- `/Volumes/AI_DATA/development/det-review-evidence/ri168-terminal-row-coupling-f50p8xyj/INCIDENCE.md`,
  25,166 bytes, SHA256
  `e74357b08a2dd13a364b3c0a460f9fbc8be6766b2e2cb80b60971c23a9d3e6b7`:
  complete terminal/marked incidence, labeled multiplicities, and the
  distinction between component identity and inherited value equality.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`,
  16,243 bytes, SHA256
  `567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8`:
  exact local quotient, global component convention, complete row
  inequalities and minimum-key/sorted-root rule. Its certificate and
  numerical discovery history are not evaluated or promoted to new premises.

The required RI187 proofs and notes were read at their unchanged literal
paths in `/Volumes/AI_DATA/development/det-review-evidence/ri187-same-law-endpoint-certificate-fh41wfew`:
`ENDPOINT_CERTIFICATE.md` (13,499 bytes,
`a805476d3df8fe1054f60a79ddfa16287f1b10033ff19a8672016831a632a4fe`),
`LOWER_LAW_TRACE.md` (11,631 bytes,
`3b74151edeb6316c00ac09f752727899abf24ea5cc6da75c7da080435a7e6d6e`),
and `DEPENDENCY_NOTES.md` (19,286 bytes,
`d6744f2b2fa23d164cdba14ff7fec0e2f5a8e328926ae4389ab007bd3c8b0fa6`).
No new historical mathematical source path or alias was added.

Source/read receipts through drafting were `7f74ec`, `184012`, `8b57db`,
`ec8550`, `ac2fcb`, `4c003e`, `6c7dc5`, `07670f`, `1813de` and
`08c6ac`, all exit zero and unclipped. Hash checks are opaque administrative
operations, not validation by execution of the law. Author-peer review
does not replace the root's separate independent adjudication.

All fixed-law corrections, theta/M5, canonical q/N products, P2/P3,
Y=1/4, shared T1, other eight parents, five Di and 31/139/20/42 obligations
remain unchanged. No actual vector/table instantiation, scientific JSON
decode, numerical/symbolic/graph engine, source/helper import, compile,
AST, probe, run, fixture, runtime/admission, new agent, repository/index/Git
or predecessor mutation occurred. RET stays paused. No actual endpoint,
H30, geometry, gravity or physical sign is claimed. Stop at the frozen
manual source handoff.
