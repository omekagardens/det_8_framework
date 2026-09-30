# RI181 — complete four-cap classification and marked restoration

30 September 2026. Manual coauthor derivation for independent review.
The six-parent P=C2 ordinal-sum A4 has exactly seventeen proper ideals.
Their complete potentials reduce to the smaller fixed laws below. Every
proper component of the needed five-parent C2 ordinal-sum A3 is proved
restoration-only, including its locally neutral roles. No independence of
full-slot records, component value evaluation or global enumeration is used.

## 1. Parents, ideals and transported records

Let T={r,a} with r<a. For a finite cap set B define

    L(B)=T ordinal-sum B,

so every cap is above both stem vertices and distinct caps are incomparable.
Write L_n for this unmarked shape when |B|=n. Thus L_0=C2, L_1=C3,
L_2 is the four-vertex stem-fork, L_3 is the five-parent needed below,
and the new six-parent is P=L_4. Fix B={b1,b2,b3,b4} and an arbitrary
binary record on all six vertices. The stem bits i=r(r), u=r(a) and
four cap bits are independently variable; no root-bit flip is imposed.

An ideal not containing a cap is empty, {r}, or T. An ideal containing
a cap must contain T, and may otherwise contain any cap subset. Hence
the complete proper list is

| Ideal type | Explicit choices | Number |
| --- | --- | ---: |
| Empty | empty | 1 |
| Root | {r} | 1 |
| Whole stem | T | 1 |
| One cap | T+b1, T+b2, T+b3, T+b4 | 4 |
| Two caps | T+b1+b2, T+b1+b3, T+b1+b4, T+b2+b3, T+b2+b4, T+b3+b4 | 6 |
| Three caps | T+b1+b2+b3, T+b1+b2+b4, T+b1+b3+b4, T+b2+b3+b4 | 4 |

The sole excluded ideal is the full P. Thus 3+4+6+4=17, including
the empty and whole-stem ideals. Isomorphic cap subsets are still
separate labeled occurrences, not divided by automorphism multiplicity.

For a marked smaller parent use q_{L(B),r}(S) for its actual scalar birth
probability. Restrict and transport the entire marked order when deleting
vertices. The accepted maximal-deletion potential is

    u_{P,r}(S)= product over nonempty H subset (B\S)
        q_{P\H,r restricted to P\H}(S)^((-1)^(|H|+1)). (1)

Every denominator is a strictly positive smaller-law probability. The
maxima of P are precisely B. Proper locality forgets only marks outside
the selected S; a full probability retains all its parent marks unless
another proved identity removes them. Formula (1) has no newborn-bit
factor: q is the scalar probability, with the separate fair factors already
handled by the inherited whole-map diamond construction.

## 2. All marked cases and smaller-law inputs

The cap permutation group S4 fixes r,a. Equivariance carries each ideal
and its marks together, so for each of the four fixed pairs (i,u), the
parent records have five cap-Hamming-weight classes m=0,1,2,3,4. Their
actual record multiplicities are respectively 1,4,6,4,1. This accounts for
all 4*(1+4+6+4+1)=64 records. It proves only permutation covariance,
not equality between different m, between stem pairs, or under bit flips.

More finely, among the k-cap ideals of a row with m one-bits there are

    binom(m,j)*binom(4-m,k-j)                           (2)

occurrences with j selected one-bits, using zero for invalid binomial
arguments. Summing (2) over j gives binom(4,k). The formulas below retain
each actual subset, so these multiplicities are never silently merged.

To abbreviate the transported probabilities without erasing their marks,
let S range over J(T)={empty,{r},T}, and define

    a_S = q_{L_0,r|T}(S),
    z_S = q_{L_2,r'}(S),
    t_b = q_{L({b,c}),r|T+b+c}(T+b),
    c_{bc} = q_{L({b,c}),r|T+b+c}(T+b+c).              (3)

In z_S the two caps are outside the proper precursor; locality removes
their bits, and equivariance removes their names. Thus z_S reads only
the marks on S, with the whole fixed L_2 order retained. In t_b the
other cap c is outside the proper precursor, so its identity and bit do
not matter, but both stem marks and b's mark remain allowed inputs.
The full c_{bc} retains both stem and both selected cap marks; only
c_{bc}=c_{cb} under simultaneous transport is used. We do not declare
c_{bc} independent of either cap bit.

RI41 retains the exact RI36 C3 row

    q_{L_1}(S)=e=1/44 for S in J(T),
    q_{L_1}(L_1)=a3=1-3e=41/44.                       (4)

These accepted record-independent constants are literal construction
premises, not extracted current values. All size-two entries a_S and
size-four entries in (3) remain the actual fixed law. In particular no
common coefficient replaces the size-four component vector, and no
canonical correction is removed from an unrelated parent-five row.

## 3. A finite defect lemma, with arbitrary deletions

The defect here is the minimum number of arbitrary vertices deleted to
leave a Ferrers cell order. The following elementary Ferrers facts suffice:

- A nonempty Ferrers order has one least cell; a disconnected union of
  two nonempty orders cannot itself be Ferrers.
- A cell has a chain principal ideal only when it lies on an axis.
  Thus two incomparable chain-principal cells can share only the minimum,
  not a two-element chain of common predecessors.
- An antichain of three cells requires at least six cells in its Ferrers
  down-set. Order its three distinct horizontal coordinates; the necessary
  row lengths contain the staircase 3,2,1. Consequently a Ferrers order
  on at most five vertices has width at most two.
- A Ferrers order with at least four cells contains a four-cell Ferrers
  suborder, by repeatedly deleting a maximal corner.

For L_3 any four-vertex subset either keeps two stem vertices and two
caps, or one stem vertex and three caps. The first has two incomparable
chain-principal caps sharing the two-element stem; the second has width
three. Neither is Ferrers. A three-vertex chain is retained, so

    defect(L_3)=2.                                    (5)

The same four-vertex argument for L_4 adds the possible four-cap antichain,
also non-Ferrers. No larger Ferrers suborder exists by the corner fact.
A retained three-chain gives

    defect(L_4)=3.                                    (6)

Also L_3 plus an isolated newborn has largest Ferrers suborder of size
three: a Ferrers subset cannot mix the isolated vertex with the other
component. Its defect is therefore three. Thus births at empty and T
are already defect-raising roles at L_3. This argument includes deletions
of stem vertices; it is not a maximal-deletion-only defect test.

## 4. Neutral roles also have zero canonical coefficient

The other proper ideals of L_3 are {r}, its three one-cap ideals T+b,
and its three two-cap ideals T+b+c. Let z be a newborn at one of them,
and choose an old cap d not in that ideal. The common diamond base is
L_2=L({b,c}), after deleting d, with the obvious selected cap names in
each case. Its two precursors are T (which births d) and S (which births
z). They are incomparable newborn events because neither precursor uses
the other newborn. The two intermediate parents are L_3 and
Q=L_2+z_S, with the same six-vertex terminal L_3+z_S.

The complementary five-parent Q and a single deletion proving defect one
are as follows. It is non-Ferrers in every case because its two original
caps b,c have chain principal ideals sharing T.

| L_3 selected S | Complementary Q | One deletion leaving Ferrers |
| --- | --- | --- |
| {r} | L_2 with an extra leaf z above r | Delete c: r<a<b and r<z, the four-cell hook |
| T+b | L_2 with z above b | Delete a: r<b<z and r<c, the four-cell hook |
| T+b+c | Full cone over L_2 | Delete a: r<b,c<z, the four-cell square |

Thus defect(Q)=1. The common terminal has defect exactly two. To prove
its lower bound, deleting z leaves the non-Ferrers L_3. Deleting one old
cap leaves two incomparable old caps with chain principal ideals sharing
T. Deleting either stem vertex leaves all three mutually incomparable
old caps in a five-vertex order, violating the width bound. These are all
six single-vertex deletions. For its upper bound, first delete d to obtain
Q and then use the indicated hook/square deletion. Hence

    defect(L_3+z_S)=2=defect(L_3),
    defect(Q+newborn over T)=2>defect(Q)=1.             (7)

The L_3 role is neutral but the opposite role of its same ratio component
is raising. This connection is not merely an unmarked terminal analogy:
the ordinary base-L_2 diamond explicitly joins the two local nodes.
All four old base bits and both newborn bits are arbitrary. In particular
the old cap d's bit and z's bit are distinct free newborn records on the
two routes, transported to the identical terminal assignment. Every one
of the 32 marked L_3 parents, every selected ideal, and both newborn bits
is covered. No cap-bit average or root-only hypothesis is used.

RI63's accepted exhaustive statement says every positive canonical
component is everywhere defect-neutral. Its contrapositive therefore
makes the coefficient zero for each component just shown to contain a
raising role, including neutral L_3 roles in (7). Combined with the two
directly raising types from (5)--(6), this covers all nine proper ideals
of L_3: 3 stem-contained, 3 one-cap, and 3 two-cap occurrences.

Consequently the complete actual strict-mixture law on this parent is

    q_{L_3,r}(S)=theta*u_{L_3,r}(S) for every proper S,
    q_{L_3,r}(L_3)=1-theta*K_3(r),
    K_3(r)=sum over all nine proper S of u_{L_3,r}(S). (8)

Here theta=c5/36=1/[72(1+M5)] is unchanged. The proof eliminates these
particular canonical components; it does not assume every neutral
component elsewhere vanishes. It says nothing about a common scale at
parent size four, whose actual entries in (3) remain intact.

## 5. Exact deletion products and cancellation

First retain the unsimplified parity of every deletion in (1). A
stem-contained S omits four caps, with subset counts 4,6,4,1 and
alternating exponents +,-,+,-. A one-cap ideal omits three caps with
counts 3,3,1; a two-cap ideal omits two with counts 2,1; a three-cap
ideal omits one. Thus all fifteen, seven, three or one factors,
respectively, are present before any equality substitution.

For a three-cap set D, the analogous deletion formula and (3)--(4) give

    u_{L(D)}(S)=z_S^3*a_S/e^3             (S in J(T)),
    u_{L(D)}(T+b)=t_b^2/a3               (b in D),
    u_{L(D)}(T+b+c)=c_{bc}               ({b,c} subset D),

    K_3(D)=sum_{S in J(T)} z_S^3*a_S/e^3
          +sum_{b in D} t_b^2/a3
          +sum_{{b,c} subset D} c_{bc}.               (9)

All symbols in (9) have the particular parent's restricted marks.
The three full c_{bc} terms are distinct pair occurrences. Define
j_3(D)=1-theta*K_3(D); this full complement may retain all marked
dependence present in (9). We do not erase it by proper locality.

Applying the four-cap formula and then (8)--(9) gives the complete table:

| Proper ideal | Exact deletion product before restoration substitution | Reduced potential |
| --- | --- | --- |
| S in J(T) | q_3(S)^4 e^4 / (z_S^6 a_S) | theta^4 z_S^6 a_S^3/e^8 |
| T+b | q_3(T+b)^3 a3/t_b^3 | theta^3 t_b^3/a3^2 |
| T+b+c | q_3(T+b+c)^2/c_{bc} | theta^2 c_{bc} |
| T+b+c+d | Full q_{L({b,c,d})} | j_3({b,c,d}) |

The repeated proper q_3 factors are equal only after locality forgets
the omitted cap marks and equivariance transports the remaining order;
the selected precursor marks are unchanged. Full factors are not subjected
to that shortcut. Every displayed division is by an accepted strictly
positive smaller-law entry. The exponents, including e^8 in the first
row, come from all four deletion levels rather than a pairwise truncation.

Summing exactly the seventeen occurrences yields

    U_4(r)=theta^4*sum_{S in J(T)} z_S^6*a_S^3/e^8
           +theta^3*sum_{b in B} t_b^3/a3^2
           +theta^2*sum_{{b,c} subset B} c_{bc}
           +sum_{{b,c,d} subset B} j_3({b,c,d}).       (10)

No scientific operand has been reconstructed. Formula (10) identifies
the complete required smaller-law inputs: the C2 row, the accepted C3
row, and the properly marked L_2 row. The needed L_3 row is derived
from them by (8)--(9), rather than borrowed from a numerical table.

## 6. Immediate complete-row consequence and scope

Because K_3(D) is one complete marked parent-five proper-potential sum,
its value is at most the unchanged global M5. The exact strict-mixture
definition therefore gives

    j_3(D)>=1-theta*M5=71/72+theta.                   (11)

There are four distinct such terms in (10), and each of the other
thirteen potentials is strictly positive. Thus every one of the 64 rows
satisfies

    U_4(r)>71/18+4theta.                              (12)

This does not assert cap-record independence or identify a maximizing
row. The companion bound proof gives the resulting cap on the unchanged
actual rho and the properly scoped endpoint implication. No value of
M5, M6, rho, a component, or an actual endpoint is computed here.
The q2 full corrections and every marked ideal occurrence remain bound
to the same law; (12) is not a free-prefix counterexample or a new law.

## 7. Literal sources and actual diagnostics

The RI181 assignment was authenticated as `840041`,`40d66d` and read
completely as `0bfc39`; the RI178 decision was authenticated as
`0c6009`,`eb8bc9` and read as `0ed60e`. All exited 0.

Fresh accepted analytic reads, at already selected exact paths, were:

- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_height_normalization_v1/NORMALIZATION.md`, 16243 bytes, SHA256 `567596a17c69e20b33328b2d0c39f22d98a78f7d25d81949fd57cd07df5e53c8`. Complete `e47043`,`06cece`: fixed C2/C3 prefix, locality/equivariance, maximal-deletion potential, full marked graph and labeled-slot multiplicities.
- `/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_growth_expected_defect_completion_v1/COMPLETION.md`, 17102 bytes, SHA256 `e99ea92b13687d7de6ad4db2bec9161397edb8ddacac18f6b32966e58ca85122`. Complete recovered reads `07b78c`,`388dce`,`ee152a`: everywhere-neutral active canonical components, complete diamond graph, arbitrary-vertex defect and unchanged strict-mixture definition. No linked scientific artifact was read.
- `/Volumes/AI_DATA/development/det-review-evidence/ri147-native-scale-membership-q4lxbpke/ACTUAL_SCALE_BOUND.md`, 13744 bytes, SHA256 `2cdaa5fa384f81a5b253a28f26c088ee6a3dd83e4fe7e60dde56f1a5b6aa7577`. Complete `c56e08`,`589e1b`: complete-parent/global-maximum relation and its inequality direction, strict mixture and distinct ideal occurrences.

Fresh lengths/hashes `963ff2`,`10488b` matched the inherited pins;
`90d2c0` reconciled the RI41/RI63 paths and identities in the selected
manifest. An initial combined display clipped part of RI63 (`d8dd9b`);
the explicit consecutive recovery ranges above cover its entire text.
No failed read or source execution occurred. Historical commands and
numeric outcomes printed inside accepted notes were not run or decoded
into current scientific operands. No additional historical path was needed.

Only this assigned external Markdown is authored. No scientific JSON,
vector, helper/source import, compile, AST, probe, numerical/symbolic
engine, runtime, fixture, new agent, repository/index/Git operation or
predecessor edit occurred. This is author work, not independent acceptance.
RET stays paused; measurement and RI180 remain separate. Preserve P2/P3,
Y=1/4, all31/139/20/42, shared T1, other eight parents, five Di, strict
endpoints and every labeled ideal. Root owns review and continuation.
