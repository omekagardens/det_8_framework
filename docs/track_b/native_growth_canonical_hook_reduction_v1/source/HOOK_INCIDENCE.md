# RI149 — complete incidence of the C5 singleton-hook components

30 September 2026. Manual fixed-shape graph proof and author-side integration.
No global graph reconstruction, scientific-body decoding, source/helper
execution, numerical or symbolic engine, or actual coefficient evaluation.
This note is not an independent adjudication.

## 1. Result

For terminal hook (5,1), the accepted proper-slot ratio graph has **exactly
two components**, indexed by the intrinsic root bit. Each component consists
of one C5 singleton local node and eight (4,1)-hook long-arm local nodes.
All additional marked distinctions on the long arm are connected directly
to the same root-only C5 node; there is no further marked subdivision.

In the accepted naturally labelled source domain, each component has 80
incident raw marked rows: 16 C5 rows and 64 hook rows. These correspond to
32 canonical fully marked rows, retaining every mark. Each row contains one
occurrence of its target component and no occurrence of the other target
component. There are 64 directed raw diamond occurrences per component.
These counts are derived below from the two shapes and their mark sets,
not obtained by running an enumeration or reading a scientific output.

The complete row coefficients, marked transport, proper-ideal defect
classification and history-weighted objective contribution are explicit.
They do not establish an ordering or sufficient magnitude comparison of
the two actual canonical coefficients. The other columns and their global
canonical constraints remain in the face problem.

## 2. Intrinsic terminal and its two deletion roles

Let the terminal T have vertices

    r < a1 < a2 < a3 < a4,       r < b,

with no further comparabilities involving b. This is the Ferrers hook with
row lengths (5,1). Its only maximal vertices are a4 and b, and its unique
minimum is r. Its two maximal-deletion parents are:

| Newborn in T | Old parent | Selected precursor |
|---|---|---|
| b | C5 on r,a1,a2,a3,a4 | {r} |
| a4 | Q=(4,1) on r,a1,a2,a3,b | L={r,a1,a2,a3}, the full long C4 arm |

Every proper-slot node whose terminal is T must be one of these roles:
the newborn is maximal, and these are all maximal vertices. Conversely
both roles are valid proper births. There is no empty-precursor role,
since it would create an isolated newborn rather than this connected
terminal. The arms have unequal lengths, so T, C5 and Q have no nontrivial
unmarked automorphism. In particular their root and long-arm positions
are intrinsic.

Each graph edge in the accepted RI41/RI63 constructions is an ordinary
two-birth diamond. Its two node terminals agree up to swapping the two
newborns. Whole-parent/precursor isomorphisms also preserve the terminal.
Thus no path from these nodes can introduce another terminal class.
Removing both maximal vertices of T leaves exactly the long C4 arm L.
Every incident diamond therefore has base C4 and the two distinct precursor
ideals L and {r}. There are no additional incident base shapes, equal-
precursor edges or local-node loops in this terminal class.

The root is below both maximal vertices. It lies in both corresponding
precursors, remains in the base, and is transported with its binary mark
on every edge. Root0 and root1 cannot be identified by any path. The
following direct connectivity proof supplies the converse, so this is an
exact two-component result rather than merely a separation result.

## 3. Complete mark transport and connectivity

Write the marked base C4 in long-arm order as

    xi=(i,u1,u2,u3),       i,u1,u2,u3 in {0,1}.

Let t be the new long-tip bit at a4 and s the new short-leaf bit at b.
Both bits vary independently. The two routes to the same fully marked
terminal are:

| Route | First birth and intermediate full records | Second proper slot |
|---|---|---|
| Long tip then short leaf | Full C4 birth; C5 records (i,u1,u2,u3,t) | Root singleton {r}; newborn bit s |
| Short leaf then long tip | Root birth; Q records (i,u1,u2,u3,s) | Long C4 arm L; newborn bit t |

The C5 singleton local key reads only i. Its four other old bits remain
in the full marked row but not in that proper local key. The Q long-arm
local key reads all four bits xi; only the old short-leaf bit s lies
outside its precursor. Neither proper coefficient reads its newborn bit.
No physical record is deleted or averaged in this description: these
restrictions are exactly the accepted proper-slot locality and transported
whole-map diamond conventions.

Fix i. For every one of the 2^3 assignments (u1,u2,u3), either value of t
and either value of s, the diamond directly links the same C5 singleton
local node to the Q long-arm local node with marking xi. This gives one
hub and eight distinct neighbors. They are distinct local nodes because
Q has no automorphism that changes its intrinsic long-arm positions or
their bits. All are connected; none can reach the opposite root bit.
Together with the exhaustive two-role classification, this proves

    exactly two components, each with 1+8=9 local nodes.

No component index or encoded canonical key has been calculated.

For the source's ordered raw diamonds, the naturally labelled four-chain
has one order. For each root bit there are eight inherited base markings,
four independent newborn-bit pairs, and two orders of the distinct
precursors (full,root) and (root,full). Thus there are

    8 * 4 * 2 = 64 directed raw occurrences per component,
    128 across both components.

Each of the eight hub-neighbor adjacencies occurs eight times in this
directed raw inventory. The simple adjacency used to find components
does not replace those occurrences in the historical full raw contract.
Fair newborn factors1/2 occur on both legs of both routes and cancel in
the coefficient equality; the complete newborn-resolved maps are retained.

## 4. All incident marked rows and exact target coefficients

Use the unchanged actual fixed prefix q_B. Put

    beta_i = q_B(C4,xi,{r}) = B_i(1) > 0,
    c_xi   = q_B(C4,xi,L) > 0.

Beta_i is a singleton probability, not a local pivot ratio. Its independence
of u1,u2,u3 is proper-precursor locality. The full complement c_xi remains
the complete normalized C4 entry. Even where an earlier accepted theorem
reduces its record dependence, every full marking and row occurrence below
is retained; no new full-slot locality assumption is made.

The RI38 maximal-deletion potential gives:

| Parent and records | Target precursor | Potential coefficient in complete row cap |
|---|---|---|
| C5, (i,u1,u2,u3,t) | {r} | beta_i |
| Q, (i,u1,u2,u3,s) | L | c_xi |

For C5 there is one omitted maximal vertex, a4; deletion leaves the C4
singleton probability beta_i. For Q and L the only omitted maximum is b;
deletion leaves the genuine C4 full complement c_xi. It is not replaced
by a proper-potential formula.

The same diamond makes the coefficient identification explicit. Its
unscaled potential products are c_xi beta_i and beta_i c_xi. Multiplying
by the respective component coefficients and dividing by this positive
product equates those coefficients. Since xi varies freely with root i,
all eight Q local markings share the C5 singleton component coefficient.

Let alpha_i denote its actual canonical boundary coordinate and retain

    kappa_i=(35/36)alpha_i,     actual coefficient=theta+kappa_i.

Then its actual proper probabilities in the two roles are respectively
(theta+kappa_i)beta_i and (theta+kappa_i)c_xi. Alpha_i, kappa_i, theta,
beta_i and c_xi are not evaluated here.

For a fixed root bit, C5 has 2^4=16 fully marked canonical rows. Q also
has 2^4=16: all three nonroot long-arm bits and its leaf bit are retained.
The chain has one natural labelling. Q has four: after its mandatory first
root, its short leaf can occur in any of four positions among the three
ordered long-arm vertices. Transporting all marks gives four raw marked
rows for every canonical fully marked Q row. Hence, per component,

| Object | C5 | Q | Total |
|---|---:|---:|---:|
| Canonical fully marked incident rows | 16 | 16 | 32 |
| Naturally labelled fully marked incident rows | 16 | 64 | 80 |
| Target proper-slot occurrences in those raw rows | 16 | 64 | 80 |

Across the two components the corresponding totals are 64 canonical rows,
160 raw rows and 160 target occurrences. Each C5 local hub accounts for
16 raw occurrences. Each Q local node accounts for 4 natural labellings
times2 excluded leaf marks, namely8 raw occurrences. These totals agree
with one hub plus eight neighbors per component. Rows do not contain both
target components because the same intrinsic root has a single fixed bit.

## 5. Complete Q proper row, with all other columns retained

Use the natural representative Q=(0,1,3,7,1) with vertex order
(r,a1,a2,a3,b). Let J_zeta denote the existing actual prefix row on
Q4=(3,1)=(0,1,3,1), obtained by deleting a3 and transporting the records
to (r,a1,a2,b), denoted zeta=(i,u1,u2,s). Let A be the complete C3 row
on (r,a1,a2), and B_xi the complete C4 row on (r,a1,a2,a3).
These are symbolic evaluations of the already fixed prefix definition,
not new queried, reconstructed or decoded rows.

Q has exactly the eight proper ideals listed below, and full ideal31.
Its omitted maxima are subsets of {a3,b}. The table records every
individual ideal, including the full smaller-parent factors.

| Q mask | Precursor | Exact potential u_Q | Terminal type or obstruction | Defect increment |
|---|---|---|---|---:|
| 0 | empty | B_xi(0) J_zeta(0)/A(0) | isolated newborn | 1 |
| 1 | r | B_xi(1) J_zeta(1)/A(1) | three atoms above root | 1 |
| 3 | r,a1 | B_xi(3) J_zeta(3)/A(3) | incomparable chain-principal maxima sharing two vertices | 1 |
| 7 | r,a1,a2 | B_xi(7) J_zeta(7)/A(7) | incomparable chain-principal maxima sharing three vertices | 1 |
| 15 | L=r,a1,a2,a3 | c_xi=B_xi(15) | Ferrers (5,1) | 0 |
| 17 | r,b | J_zeta(9) | Ferrers (4,1,1) | 0 |
| 19 | r,a1,b | J_zeta(11) | Ferrers (4,2) | 0 |
| 23 | r,a1,a2,b | J_zeta(15), a full complement | nonchain five-vertex principal ideal with unique maximum | 1 |

For masks0,1,3,7, both maxima are omitted: the two single deletions leave
C4 and Q4 and the double deletion leaves C3. For masks17,19,23 only a3
is omitted, giving Q4 masks9,11,15 after transport. For mask15 only b is
omitted, giving the full C4 entry. Every denominator is positive.

The ideal list is exhaustive: without b there are the five prefixes of
the four-chain, including empty and full L; with b there must be r and
there can be zero, one, two or three further long-arm vertices. The last
of those four ideals is full Q and is excluded only from the proper sum.
No labelled-ideal multiplicity or full marked row is collapsed.

Q is Ferrers and has defect0. Each listed non-Ferrers terminal has defect1,
because deleting the newborn recovers Q. The obstructions are exact:
nonempty Ferrers orders have a unique minimum and at most two atoms;
incomparable chain-principal ideals in a Ferrers order intersect only at
the minimum; and any principal ideal in a Ferrers order is rectangular.
The principal ideal of the newborn at mask23 has five vertices, is nonchain
and has a unique maximum, whereas a five-cell rectangle is a chain.

The full birth at mask31 is not a proper-column entry. Its terminal F(Q)
has six vertices, a unique maximum and height5. A Ferrers order with a
unique maximum is rectangular; the six-cell rectangles are chains of
height6 or 2-by-3 rectangles of height4. Thus F(Q) is not Ferrers. Deleting
the new maximum recovers Q, so its full-birth defect increment is1.

For C5 the complete proper ideals are0,1,3,7,15. Only root mask1 gives
the neutral (5,1) hook. Empty birth is disconnected, and masks3,7,15 give
incomparable chain-principal maxima with a shared chain of at least two
vertices. Their increments are1. Full birth yields C6, still Ferrers,
so the C5 full increment is0.

The target terminals at Q masks15,17,19 have distinct shapes. Therefore
their component columns cannot coincide with one another. The other
columns still have their full transported precursor records and all their
incidences in other parent rows; no further marked quotient for them is
introduced in this note.

At the accepted canonical boundary point, every component with a raising
role has coefficient zero by RI63's exhaustive active-component theorem.
Accordingly the incident canonical row caps reduce, without changing any
other coordinate, to

    C5: beta_i alpha_i <= 1,

    Q:  c_xi alpha_i
           +J_zeta(9) alpha_c(Q,17,records)
           +J_zeta(11)alpha_c(Q,19,records) <= 1.

The unsimplified complete caps retain all proper columns in the table;
their omission in these last two expressions is solely the accepted zero
property at that canonical point. This is not a claim about an arbitrary
primary optimizer or the actual strict mixture. At the actual strict law,
the restoration terms in every proper slot remain positive. The full
complement is determined by normalization, not discarded as a missing
column. The two other neutral coordinates and every global constraint
on them remain fixed in any proposed one-coordinate comparison.

## 6. Complete history-weighted objective contribution

RI63's objective column is the sum over canonical marked rows of actual
prefix history mass pi_j times u_j(S)[d_j(S)-f_j]. Both target proper
births are neutral. The C5 full increment is0, so every incident C5
row contributes0 to this target objective column. The Q full increment
is1, so every incident Q row contributes -pi_j c_xi. Hence

    objective_column_i =
       -sum_(all16 canonical Q rows with root i) pi_Q(xi,s)c_xi < 0.

Every summand is strictly positive before the minus sign. There is no
uniform weighting of rows or omission of the marks ignored by a proper
coefficient. The actual pi_Q remains the sum of its four natural-history
weights, as in the literal `build_problem()` aggregation.

An optional exact identity checks these multiplicities independently.
Match each canonical Q marking (xi,s) with the C5 marking (xi,s), using
the same bit s now at the last chain vertex. Let H4(xi)>0 be the actual
marked history weight of the four-chain. In the Q history that births
the short leaf last,

    chain C5 weight = H4(xi)c_xi/2,
    Q leaf-last weight = H4(xi)beta_i/2.

The four linear extensions of Q differ by adjacent swaps of its short
leaf with incomparable nonroot long-arm vertices. Accepted complete marked
diamonds equate each pair of route products with the marks transported;
every route includes all five fair newborn factors. Q has no automorphism
identifying different intrinsic markings. Therefore

    pi_C5(xi,s)=H4(xi)c_xi/2,
    pi_Q(xi,s)=4 H4(xi)beta_i/2,
    pi_Q(xi,s)c_xi=4 pi_C5(xi,s)beta_i,

and the target objective column is equivalently

    -4 beta_i sum_(all16 C5 rows with root i) pi_C5(xi,s) < 0.

No history mass or coefficient is evaluated. This identity is for every
matched full marking, not a record average used to weaken the row caps.

## 7. Remaining premise and exact work boundary

The incidence class is complete. Its negative objective column and its
incident caps can now be used in a canonical-face argument, as developed
in the companion face note. Completeness here does not determine the
residual capacities in the Q caps: they contain the actual other neutral
coordinates, which also participate in their own complete row caps,
primary constraints and the accepted canonical tie-break. No ordering
between alpha0 and alpha1 follows merely from this shared incidence shape,
from negativity of both objective columns, or from component indices.

The historical literal sources reused here were read completely by this
author during the preceding RI145/RI147 work (the complete source-code
reads were in RI147); no fresh execution or scientific reconstruction is
claimed:

- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/check.py`
  and `NORMALIZATION.md` in that same directory: complete ratio graph,
  marked locality, potentials and fixed-prefix normalization.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/check.py`
  and `COMPLETION.md` in that same directory: complete source definitions
  of graph, raw rows, canonical row aggregation, objective, actual strict
  mixture and canonical active-component premise.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/COMPONENT_CONTRASTS.md`:
  accepted singleton coefficient correlation and terminal/root invariant.
- `/Volumes/AI_DATA/development/det-review-evidence/ri120-connected-sensitivity-source-xru78ysn/ANALYTIC_PREFIX_LEMMAS.md`
  and `F2_ANALYTIC_CHECK.md` in that same directory: accepted Ferrers
  chain-principal obstruction and C5 proper-slot classification.

The new administrative assignment and predecessor decision were read
completely at
`/Volumes/AI_DATA/development/det-review-evidence/ri147-root-scale-review-9dwcmsz2/NATIVE_SUCCESSOR_RESERVATION.json`
and `RI147_ROOT_ADJUDICATION.json` in that same directory. Complete current
mark transport, each deletion factor, all proper ideals, the two full-birth
increments, natural-label and mark multiplicities, objective signs, and
the history identity were checked manually. Findings were coordinated
with the main and canonical-face authors; this is author-peer work, not
independent review. No selected actual coefficients, scientific outputs,
runtime inventory, controller, fixture, card or admission were created.

The complete current
`/Volumes/AI_DATA/development/det-review-evidence/ri149-singleton-hook-incidence-yfjac93v/CANONICAL_REDUCTION_SYNTHESIS.md`
was also read as author-peer integration. Its incidence, history factors,
exact projected feasible set, zero-safe saturation, full-vector canonical
lexicographic reconstruction, dual-face statement and correlated q
substitution were checked manually; no concrete issue was found. This
does not constitute independent acceptance of that companion work.

Only this Markdown is authored. The fixed baseline/seed/amplitude/support,
strict endpoints, shared T1, eight other connected parents and all five Di
obligations remain. The 31/139/20/42 runtime obligations and original P2/P3
numerical target domain are unchanged. Actual W/C2/C3 signs and full H30
remain unresolved. RET and measurement are separate; predecessors,
repository/index/Git and actual runtimes are untouched. No geometry,
mass/gravity, empirical or full-QM conclusion follows.
