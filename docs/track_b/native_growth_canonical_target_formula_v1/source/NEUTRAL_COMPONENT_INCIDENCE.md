# RI151 — complete neutral-component incidence and marked transport

30 September 2026. Manual fixed-shape graph proof, using the accepted literal
component/deletion definitions. No global graph enumeration, engine, scientific-body
decoding, coefficient evaluation or source/helper execution was performed.
This is author work, not independent adjudication.

## 1. Exact component result and notation

The two new terminal classes have exactly the following marked components:

- Terminal (4,1,1): two components b_i, indexed only by root bit i.
- Terminal (4,2): four components d_(i,u), indexed by root bit i and the
  first long-arm atom bit u; that atom is intrinsically distinguished.

The globally required staircase terminal (3,2,1), included at the main
author's explicit direction to close the incident neutral rows, has two
components h_i indexed only by the root bit. These labels denote canonical
parent-five **boundary coordinates**. They are not the older held b/h
probabilities. The already accepted singleton-hook target is a_i.

All four types retain their actual original component identities; no
component index, numerical coordinate, or alternative coefficient vector
is reconstructed or chosen. Strict-law coefficients remain theta+(35/36)
times their corresponding canonical coordinate. A canonical equality does
not make the strictly restored actual full probability zero.

Use four five-vertex parent shapes, with names fixed in this note:

| Name | Shape | Natural representative | Intrinsic vertices |
|---|---|---|---|
| C | C5 | (0,1,3,7,15) | one chain |
| Q | (4,1) | (0,1,3,7,1) | r<a<A<T, r<b |
| P | (3,1,1) | (0,1,3,1,9) | r<a<A, r<b<B |
| U | (3,2) | (0,1,3,1,11) | r<a<A, r<b<c and a<c |

P has precisely the arm-exchange automorphism. The other three parents
have no nontrivial automorphism. In U, atom a is distinguished from b:
a has two successors A,c, whereas b has only c. Marks are immutable binary
labels transported with the entire parent and selected precursor.

## 2. Terminal (4,1,1): all roles and all marks

The six-vertex terminal is the two-arm hook

    r<a<A<T,       r<b<B.

Its unequal arms have lengths4 and3, so it has no nontrivial automorphism.
Its two maxima are T and B. There are exactly two maximal-deletion roles:

| Deleted/newborn maximum | Parent | Selected precursor |
|---|---|---|
| B | Q, long arm r,a,A,T and short leaf b | {r,b}, Q mask17 |
| T | symmetric P, arms r,a,A and r,b,B | complete arm {r,a,A}, P mask7 |

Choosing the other arm of P gives the same intrinsic role under P's arm
exchange, but remains a second **individual ideal occurrence** in its row.
It must not be omitted or orbit-divided.

Deleting both terminal maxima leaves V=(3,1), with vertices r,a,A,b and
natural representative (0,1,3,1). The two diamond precursors are its full
long arm7 and short arm9. Give the base marks (i,u,v,s), and give the new
long tip and short tip arbitrary bits t,w. The full-arm-first route gives
Q records (i,u,v,t,s), whose selected short arm reads (i,s). The
short-arm-first route gives P records (i,u,v,s,w), whose selected complete
long arm reads (i,u,v). Neither role reads its newborn bit; excluded old
bits remain in the full marked row.

For fixed i, every s in {0,1} links directly to every (u,v) in {0,1}^2.
Thus the local component graph is K_(2,4): two Q local nodes and four P
selected-arm local nodes. P's automorphism identifies the choice of arm,
not the ordered two bits along the chosen arm. It does not halve the two
occurrences in a complete row. The intrinsic terminal root lies in every
precursor and is preserved on every edge, so the two root components
cannot meet. The two maximal-deletion roles exhaust every node and edge
terminal presentation; hence there is no other marked subdivision.

This proves the labels b_i rather than b_(i,s) or b_(i,u,v).

## 3. Terminal (4,2): all roles and retained atom mark

The six-vertex terminal has top chain r<a<A<T and lower chain r<b<c,
with a<c. Its maxima are T,c. It has no nontrivial automorphism: a is
the atom lying below both maxima, whereas b lies below c only.

| Deleted/newborn maximum | Parent | Selected precursor |
|---|---|---|
| c | Q | {r,a,b}, Q mask19 |
| T | U=(3,2) | complete top arm {r,a,A}, U mask7 |

The common deletion base is again V=(3,1), now with precursor pair7 and11.
For base marks (i,u,v,s), the Q selected local marks are (i,u,s); the U
selected local marks are (i,u,v). The new bits at T,c independently take
both values. Thus for fixed (i,u), every s links to every v, giving K_(2,2).
Both i and u lie in every precursor. The root and distinguished atom a
are intrinsic, so neither is removed or exchanged by a quotient or edge.
The remaining bits vary freely in the direct diamonds.

There are therefore exactly four components d_(i,u), each with two Q and
two U local nodes. Each incident Q or U row has one target occurrence.
No U automorphism creates a second target ideal: U's two atoms and its
two maxima are distinguished by their order structure.

## 4. Required staircase closure, including the third maximal pair

The staircase terminal S=(3,2,1) has vertices

    r<a<A,       r<b<B,       a<c and b<c,

with maxima A,B,c. Its only nontrivial automorphism exchanges the axes
a,A and b,B, fixing r,c. Deleting c gives P and precursor {r,a,b}, its
inner V3 ideal11. Deleting A or B gives a parent isomorphic to U; the
corresponding precursor is its short C2 arm, U mask9.

The P local marking is (i,{u,s}), an unordered pair of near-arm bits.
The U short-arm local marking is (i,u) or (i,s), according to the deleted
axis end. Diamonds based at V=(3,1), with precursors9 and11, connect
P_(i,{u,s}) to both U_(i,u) and U_(i,s). In particular the mixed pair
{0,1} joins the two U local marks. The three P patterns {0,0},{0,1},{1,1}
and two U patterns consequently form one connected component per root.

The remaining maximal pair A,B leaves D4=(2,2), the four-vertex diamond.
Its two C2 precursors give additional U-to-U edges; equal selected atom
bits give local-node loops. They are retained, not dismissed as redundant
raw obligations. They do not change the root invariant or introduce an
extra component. All three maximal-deletion pairs and both parent-role
orbits have now been covered, proving exactly two staircase components h_i.

Each P row has one staircase ideal11. Each U row has one staircase
ideal9, not two: the two isomorphic terminal deletions present the same
unique short-arm ideal of U. This is different from the two individual
complete-arm ideals of P belonging to b_i.

## 5. Canonical and raw multiplicities, proved structurally

All counts below concern the accepted naturally labelled source domain,
not a run or partial substitute for its full graph. In a canonical fully
marked row, **all five old marks** remain, even when a local coefficient
reads fewer marks. Proper local-node counts use only the selected marks.

Q has four natural labellings: after its root, interleave its leaf among
the three ordered long-arm events. U has five: after the root, if a is
first there are three allowed orders of A,b,c; if b is first there are
two, respecting a<A,c and b<c. Their automorphism groups are trivial.

P has six arm-interleavings but an unmarked arm swap, giving three natural
orders. For fixed root bit its marked canonical rows are unordered pairs
of four possible two-bit arm words. Four equal-word pairs have marked
automorphism group of size2 and raw multiplicity3. The six unequal-word
pairs have trivial marked automorphism and raw multiplicity6. Therefore
P has ten canonical rows and 4*3+6*6=48 raw rows per root bit. The two
complete-arm ideals still contribute separately in **each** of those rows.

| Terminal component | Local nodes/component | Canonical incident rows/component | Raw incident rows/component | Raw target ideal occurrences/component |
|---|---:|---:|---:|---:|
| b_i, (4,1,1) | 2 Q + 4 P = 6 | 16 Q + 10 P = 26 | 64 Q + 48 P = 112 | 64 Q + 96 P = 160 |
| d_(i,u), (4,2) | 2 Q + 2 U = 4 | 8 Q + 8 U = 16 | 32 Q + 40 U = 72 | 72 |
| h_i, (3,2,1) | 3 P + 2 U = 5 | 10 P + 16 U = 26 | 48 P + 80 U = 128 | 128 |

The first and last families each have two components; the middle family
has four. Rows shared by different families must not be counted as new
distinct rows when combining this table.

The ordered raw diamond counts retain both newborn bits, both precursor
orders, and all inherited bits, including all-zero assignments:

| Component | Complete base contribution | Directed raw occurrences/component |
|---|---|---:|
| b_i | 3 V orders * 8 inherited assignments * 4 newborn pairs * 2 orders | 192 |
| d_(i,u) | 3 V orders * 4 inherited assignments * 4 newborn pairs * 2 orders | 96 |
| h_i | V:3*8*4*2; D4:1*8*4*2 | 256 |

The D4 count uses its single natural order, since its two atoms are
interchangeable. V has three natural orders and no automorphism. For h_i,
the two axis/corner maximal pairs are the same V-role orbit under the
terminal axis swap; they are not multiplied a second time. All their
distinct inherited mark assignments are already in the V factor8.
The D4 part retains its U-to-U loops. For b_i and d_(i,u), every incident
edge is between the two different parent shapes and is nonloop.

Together with RI149's a_i components, the four Ferrers parent shapes
C,Q,P,U have 116 distinct canonical marked rows and 416 raw marked rows:
per root bit the raw counts are16,64,48,80 respectively. The neutral
individual proper-slot count is1024: per root bit there is one target
slot in each C row, three in each Q row, three in each P row (including
its two arms), and two in each U row. These derived local counts grant
no execution or global-enumeration credit.

## 6. Actual prefix identities needed to compress the potentials

Let V=(3,1) have vertices r,a,A,b and fixed actual row J. Let F3 be the
three-vertex fork r<a,r<b, and D4 the four-vertex diamond. Define positive
held expressions

    p_i = q_B(C4, root-bit i, root singleton),
    e_i = q_B(F3, root-bit i, either root-plus-atom ideal),
    v_i = q_B(F3, root-bit i, full ideal).

Here v_i is a fork full probability, not the older contrast v=V1-V0.
The literal size-three `row()` formula makes e_i and v_i independent of
the two maximal fork bits, and equal for the two atom choices. No values
are evaluated. All probabilities below are actual fixed-prefix entries,
not canonical boundary coordinates.

The following stage-four component proofs use the same complete diamond
definition at the preceding layer, with no enumeration:

1. V long-arm ideal7 has terminal (4,1), the same terminal as the C4 root
   singleton. A C3 full/root diamond connects all long-arm markings with
   the same root bit to that singleton. Their potentials are the C3 full
   and root probabilities. Therefore J(7)=41p_i, using their accepted
   ratio (41/44)/(1/44), with no actual coefficient substitution.
2. V short-arm ideal9 has symmetric terminal (3,1,1). Its two maximal
   deletions both give V with a selected short arm. A fork-base diamond
   swaps the two root-plus-atom precursors; varying the atom bits connects
   both local marks at fixed root. Thus J(9)=f_i>0 depends only on i.
3. V inner-V3 ideal11 has terminal (3,2). Its other deletion role is a
   selected C2 ideal in D4. The common fork-base diamond preserves the
   root and the distinguished long-atom mark u while varying the other
   atom bit. Thus J(11)=g_(i,u)>0. This does not identify g_(i,0) with
   g_(i,1). V's potential here is the fork full v_i; D4's selected C2
   potential is e_i. Positive coefficient cancellation gives

       q_B(D4, selected C2 with atom bit u) = e_i*g_(i,u)/v_i.

These arguments include arbitrary excluded old marks and both newborn
bits, as at size five. The root-only statements in1/2 and the two retained
bits in3 are proved component implications, not assumed record locality
of a full probability.

For the C4 full complement, accepted RI127 transport already gives
c_xi=c_i: nu_xi=theta^3 c_xi and Delta_xi nu=chi(root)Delta_1 nu, with
theta>0; its accepted chain-maximal-bit transport handles the fourth
mark. This inference remains valid if Delta_1 nu=0. No full record is
dropped from the present incident row counts.

## 7. Complete P and U proper rows before canonical simplification

For P records (i,u,v,s,t) along r,a,A,b,B, write J_A for the actual V row
on r,a,A,b and J_B for the row on r,b,B,a. Let F be the actual fork row
on r,a,b. The full marked rows, and their transported restrictions in
each factor, remain implicit in these symbols. P has nine proper ideals
and full ideal31:

| P mask | Exact potential | Terminal/obstruction | Increment |
|---|---|---|---:|
| 0 | J_A(0)J_B(0)/F(0) | isolated newborn | 1 |
| 1 | J_A(1)J_B(1)/F(1) | third atom above root | 1 |
| 3 | J_A(3)J_B(9)/F(3) | chain-principal intersection | 1 |
| 7 | J_A(7) | (4,1,1), first complete arm | 0 |
| 9 | J_A(9)J_B(3)/F(5) | reflected chain-principal intersection | 1 |
| 11 | J_A(11)J_B(11)/F(7) | (3,2,1) | 0 |
| 15 | J_A(15), a full complement | nonchain five-cell principal ideal | 1 |
| 25 | J_B(7) | (4,1,1), second complete arm | 0 |
| 27 | J_B(15), a full complement | reflected five-cell principal ideal | 1 |

The list follows from empty plus the nine choices of two arm-prefix
lengths after the root, one of which is full P. For a precursor omitting
both tips A,B, the deletion product is its two V probabilities divided
by the fork probability; otherwise there is exactly one V factor. This
explains every table entry, including transported masks3/5 and9.

Full P birth has increment1. Its six-vertex terminal has a unique maximum
and height4, but is not a 2-by-3 rectangle: the two old tips have chain
principal ideals of size3, whereas the two coatoms of a 2-by-3 rectangle
have principal sizes3 and4. The only other six-cell rectangles are chains
of height6. Thus it is non-Ferrers; deleting the newborn recovers P.

For U records (i,u,v,s,t) along r,a,A,b,c, write J for its V deletion on
r,a,A,b, D for its D4 deletion on r,a,b,c, and F for the fork on r,a,b.
Its eight proper ideals and full31 are:

| U mask | Exact potential | Terminal/obstruction | Increment |
|---|---|---|---:|
| 0 | J(0)D(0)/F(0) | isolated newborn | 1 |
| 1 | J(1)D(1)/F(1) | third atom above root | 1 |
| 3 | J(3)D(3)/F(3) | chain-principal intersection | 1 |
| 7 | J(7) | (4,2) | 0 |
| 9 | J(9)D(5)/F(5) | (3,2,1) | 0 |
| 11 | J(11)D(7)/F(7) | two principal rectangles intersect in a nonrectangular V3 | 1 |
| 15 | J(15), a full complement | nonchain five-cell principal ideal | 1 |
| 27 | D(15), a full complement | nonchain five-cell principal ideal | 1 |

For both omitted maxima A,c the quotient has the two displayed smaller
parents and fork denominator; otherwise the sole deletion gives the
displayed genuine full or proper factor. The ideal list consists exactly
of the Ferrers subdiagrams of U, verified by its relations a<A,c and b<c.
At mask11, the two incomparable top vertices have four-cell principal
ideals whose intersection is the three-cell fork; intersections of
principal rectangles in a Ferrers order are rectangular, so this is not
Ferrers. The other obstructions are the accepted chain-principal and
five-cell-principal tests. Each non-Ferrers child has defect1 because
deleting the newborn returns the Ferrers parent.

Full U birth has increment0: adding the missing top-right cell gives the
2-by-3 rectangle (3,3). It is a **full** birth, not a third neutral proper
column and not a reason to make every canonical U cap tight.

The complete Q table and its full increment1 are retained from RI149.
Its only neutral proper masks are15(a_i),17(b_i),19(d_(i,u)). C has its
one neutral proper singleton(a_i) and full increment0. Every other
proper column in these four parent types has a raising occurrence and
therefore zero coefficient at the accepted canonical boundary point.
No such term is set to zero in the actual strict mixture.

## 8. Compressed potentials, objective columns and all coupled caps

The proved prefix identities reduce the neutral potentials, still with
every occurrence retained, to:

| Parent/slot | Component | Potential |
|---|---|---|
| C singleton | a_i | p_i |
| Q15 | a_i | c_i |
| Q17 | b_i | f_i |
| Q19 | d_(i,u) | g_(i,u) |
| P7 and P25, separately | b_i | 41p_i each |
| P11 | h_i | g_(i,u)g_(i,s)/v_i |
| U7 | d_(i,u) | 41p_i |
| U9 | h_i | f_i g_(i,s)/v_i |

For U9 the cancellation is exact:
J(9)D(5)/F(5)=f_i[e_i g_(i,s)/v_i]/e_i. For P11, the two V deletions
distinguish their respective long-atom marks u,s and the denominator is
the genuine fork full v_i. Neither identity omits a record or a full slot.

The objective rule is pi_j u_j(S)[proper increment-full increment].
Let sums below run over complete canonical fully marked rows, with actual
history masses pi. These masses include all natural-history multiplicities
(in particular the unequal3/6 marked multiplicities for P), not uniform
weights. The new objective columns are exactly

    beta_obj,b_i = -sum_Q(root i) pi_Q f_i
                   -sum_P(root i) pi_P (82p_i) < 0,

    beta_obj,d_(i,u) = -sum_Q(root i,longatom u) pi_Q g_(i,u) < 0,

    beta_obj,h_i = -sum_P(root i) pi_P g_(i,u)g_(i,s)/v_i < 0.

P contributes twice to the b column because it has two target ideals.
U contributes zero to d/h because its full birth is neutral. Every
displayed negative sum is strict since its row set is nonempty and all
history masses and potentials are positive. No mass or column is evaluated.

At the actual canonical point, O01 supplies every marked Q equality.
The same accepted RI63 premises give every P equality: P is Ferrers,
hence cannot be critical (defect0 cannot drop to-1), and its full birth
raises while all active proper components are neutral. Zero canonical
drift in every noncritical row forces its full complement to zero.
For C and U the full increment0 does not force this equality.

The resulting complete neutral Ferrers sector, for every permitted u,s,
is therefore

    C: p_i a_i <= 1,
    Q: c_i a_i + f_i b_i + g_(i,u)d_(i,u) = 1,
    P: 82p_i b_i + [g_(i,u)g_(i,s)/v_i]h_i = 1,
    U: 41p_i d_(i,u) + [f_i g_(i,s)/v_i]h_i <= 1,
    a_i,b_i,d_(i,0),d_(i,1),h_i >= 0.

For P the unordered pair {u,s} has all three possibilities00,01,11;
writing both orders preserves the same equations without replacing
the row's separate arm occurrences by half weights. For Q/U, u and s
are distinguished intrinsic marks and all ordered choices remain.

This system does not assume g_(i,0)=g_(i,1). For example, subtraction
of the P00 and P01 equalities gives

    g_(i,0)[g_(i,0)-g_(i,1)]h_i = 0.

Thus unequal actual g values imply h_i=0 and b_i=1/(82p_i); equal g
values leave one coupled P equality. This is a zero-safe conditional
branch, not a claim about which branch the actual fixed prefix occupies.
Likewise the two Q equalities imply g_(i,0)d_(i,0)=g_(i,1)d_(i,1).
No positive g, p or v denominator has been confused with a potentially
zero boundary coordinate.

All parent roles for these columns have been included. More generally,
a maximal deletion from a Ferrers downset is again Ferrers. Consequently
these Ferrers-terminal columns have no hidden incidence in a non-Ferrers
parent. Up to transposition, the Ferrers parent shapes on five cells are
exactly C,Q,P,U; their proper Ferrers six-cell terminals are (5,1),
(4,1,1),(4,2),(3,2,1). The other six-cell Ferrers shapes, chain and
rectangle, arise here only as full births. This finite shape classification
is checked directly by the possible row lengths and corner deletions,
not by a global algorithm.

The companion equality/face derivation can therefore test proposed
sector variations against these complete rows while keeping all other
coordinates and constraints fixed. The canonical tie-break still refers
to the original reconstructed full vector. No ordering or selected value
of a_i follows merely from the incidence counts or negative column signs.

## 9. Read scope, author checks and preserved boundary

The RI151 assignment and predecessor root decision were read completely:

- `/Volumes/AI_DATA/development/det-review-evidence/ri149-root-canonical-review-25_k3ysa/NATIVE_SUCCESSOR_RESERVATION.json`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri149-root-canonical-review-25_k3ysa/RI149_ROOT_ADJUDICATION.json`,
  including accepted O01 and its boundary/strict-law distinction.

The literal source definitions freshly reread in this sitting were at
`/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/check.py`:
complete row()/potential() at250–315, complete reconstruct_prefix() at340–415,
the complete new marked-diamond loop and row coefficient/objective aggregation
at629–687, and the accepted active-neutral/noncritical zero-drift checks at
970–979. The complete file and its RI41 counterpart were previously read
through EOF in RI147; this sitting does not claim another whole-file read.
These are source-text reads, not calls to those functions.

The c_xi compression was checked against the freshly read70–185 passage of
`/Volumes/AI_DATA/development/det-review-evidence/ri127-connected-compensation-nMyz57P5/RECORD_TRANSPORT.md`;
the complete text was read in preceding work. Other previously read,
unchanged literal premises reused here are RI149 HOOK_INCIDENCE.md,
the published RI41 NORMALIZATION.md and RI63 COMPLETION.md, and the external
RI120 ANALYTIC_PREFIX_LEMMAS.md and F2_ANALYTIC_CHECK.md, all at the exact
paths already bound in the inherited source selection. No new historical
alias, scientific certificate body or probability output was accessed.

Manual checks covered all maximal-deletion roles, terminal invariants,
the P arm swap and staircase axis swap, complete local connectivity,
retained newborn and inherited bits, repeated proper-ideal multiplicities,
canonical/raw marked counts and directed raw diamonds (including loops),
every displayed deletion potential, full-birth increment and objective
contribution, stage-four coefficient cancellations and the boundary
equalities/inequalities. Findings were shared with the main and equality
authors as author-peer integration, not independent acceptance.

Only this new Markdown is authored. Actual W/C2/C3 signs, rho membership
and full H30 remain unproved here. All original coordinates, complete
canonical constraints, strict restoration, fixed seed/amplitude/support,
shared T1, eight other connected parents and all five Di remain. The
31/139/20/42 runtime obligations and P2/P3 numerical domain are unchanged.
No source/helper/engine run, controller, fixture, runtime inventory, card,
admission, repository/index/Git or predecessor mutation occurred. RET is
paused; measurement stays separate. No physical, geometry/gravity or full-QM result
is promoted.
