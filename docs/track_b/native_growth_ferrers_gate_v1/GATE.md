# RI-52 — intrinsic Ferrers admission: the first-free-layer gate is feasible

24 September 2026 UTC. **Exact conditional finite-layer result; independent
coordinator adjudication accepted.** With the complete accepted RI-41 prefix
unchanged, the infimum of the worst one-step departure probability over all
marked five-event Ferrers parents is **zero**. A four-nonzero-coefficient
rational boundary witness establishes this for every binary record assignment.
Mixing it with a strict RI-38 interior extension gives strictly positive laws
with arbitrarily small departure probability. The zero-leakage boundary itself
is **not** an admitted strict law; no strict law attains the infimum.

This passes one necessary candidate-admission gate. It does not supply an
all-size Ferrers-preserving law, repair arbitrary frozen histories, select a
corner distribution, prove near-square shapes, or establish any dimension,
metric, physical clock, source or gravity result.

## 1. Intrinsic family and the unchanged conditional model

Call a finite order Ferrers if it is isomorphic to a finite down-set of the
coordinatewise product order on `N^2`, with `N={0,1,...}`. A partition
`lambda_1>=...>=lambda_k>0` represents the cells

\[
 \{(i,j):0\leq i<k,\ 0\leq j<\lambda_{i+1}\},
 \qquad (i,j)\preceq(i',j')\ \Longleftrightarrow\ i\leq i',\ j\leq j'.
 \tag{1}
\]

Coordinates specify a combinatorial representative, not a supplied physical
metric or an embedding consumed by the birth law. Membership is by order
isomorphism. No uniform-corner or Plancherel probability is assumed.

Keep every row and component scale of the [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through parent size four, including its [rational certificate](../native_growth_height_normalization_v1/CERTIFICATE.json)
and earlier record feedback. The new choices occur only at parent size five.
Retain the [RI-38 model](../native_joint_growth_extension_criterion_v1/CRITERION.md):
all ideals strictly positive, immutable independent binary record coordinates,
strict precursor-record reads, permitted whole-unmarked-parent order access,
marked-parent equivariance, fair newborn marks and the complete passive maps
`B_(S,b)(D)=q(S)D/2`. All off-diagonal entries and unnormalized branch weights
remain in `D`; no informative quantum coupling is derived.

### The closure actually available

Every order ideal of a Ferrers order is Ferrers: its image is a down-set
inside a down-set of `N^2`, hence a down-set of `N^2`. In particular,
deleting a maximal vertex preserves membership. This is not closure under
arbitrary induced subposets: the two arms of shape `(2,1)` induce a
two-antichain, which is not a Ferrers order because a nonempty down-set
of `N^2` has a unique minimum.

A local proper-slot key `[P,S,r|S]` fixes its unmarked child `P+e_S`.
Erasing outside marks changes no order, and transporting the parent and
ideal transports the child. Every ratio edge compares two maximal last-birth
roles in one child. Thus a component with Ferrers terminal child can meet
only Ferrers parent rows: delete its newborn and use maximal-deletion
closure. This component-level closure is essential to the boundary argument.

## 2. Actual order types, births and multiplicities

List the seven partitions of five and the eleven of six and classify their
product orders by actual isomorphism. Transposition pairs their diagrams.
The resulting intrinsic representatives are four at size five and six at
size six; the checker tests all these partitions and full order relations.

The following masks list **all strict predecessors**, not just Hasse edges,
in row-major cell order. The parent labels in this note are `C,A,E,B`.

| Parent | Partition | Strict predecessor masks | Good proper precursor masks and child types | Full child |
|---|---|---|---|---|
| C | `(5)` | `(0,1,3,7,15)` | `1 -> (5,1)` | `(6)`, Ferrers |
| A | `(4,1)` | `(0,1,3,7,1)` | `15 -> (5,1)`; `19 -> (4,2)`; `17 -> (4,1,1)` | Not Ferrers |
| E | `(3,1,1)` | `(0,1,3,1,9)` | `7,25 -> (4,1,1)`; `11 -> (3,2,1)` | Not Ferrers |
| B | `(3,2)` | `(0,1,3,1,11)` | `7 -> (4,2)`; `9 -> (3,2,1)` | `(3,3)`, Ferrers |

The size-six representatives are `(6)`, `(5,1)`, `(4,2)`, `(4,1,1)`,
`(3,3)`, `(3,2,1)`. A Ferrers order with a unique maximum is a rectangle:
its unique maximum must dominate every cell, so the down-set consists of
exactly the rectangle below it. At size six these types are `(6)` and
`(3,3)`, including their transposes. Deleting their maximum gives C and B
respectively, proving the two full-child roles. Every other listed child
has at least two maxima and all its incoming roles are proper.

Heights and maximal-past sizes also separate representatives without a
general diagram-rigidity assumption. At size five, E and B both have height
three but maximal-past size multisets `{2,2}` and `{2,3}`. At size six,
`(4,2)` and `(4,1,1)` both have height four and two maxima but those
multisets are `{3,3}` and `{2,3}`. The remaining cases separate by height
or number of maxima.

| Proper child | Maximal-deletion parent multiset | Automorphism count |
|---|---|---:|
| `(5,1)` | C + A | 1 |
| `(4,2)` | A + B | 1 |
| `(4,1,1)` | A + E | 1 |
| `(3,2,1)` | E + 2 B | 2 |

Parent automorphism counts for C,A,E,B are `1,1,2,1`. Deletion counts
are not labeled ideal counts. If `m(P,T)` counts ideals of a fixed parent
whose child is isomorphic to `T`, and `d(P,T)` counts maximal deletions
of `T` yielding `P`, then counting the corresponding isomorphisms gives

\[
 m(P,T)|Aut(T)|=d(P,T)|Aut(P)|.
 \tag{2}
\]

In particular E has **two** distinct ideals giving `(4,1,1)`, while B
has only **one** giving `(3,2,1)` despite that child's two B deletions.
The exact matrix retains these distinctions.

## 3. Marked-local components and the target matrix

Use the genuine RI-38 local node `[whole P,S,r|S]`, not one variable
per unmarked child. Its positive potential is computed from actual fixed
smaller-parent rows by

\[
 u_{P,r}(S)=\prod_{\varnothing\ne Q\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus Q,\,r|_{P\setminus Q}}(S)^{(-1)^{|Q|+1}}.
 \tag{3}
\]

Every factor reads only permitted precursor marks. Quotient only by whole
parent/ideal/inside-record isomorphisms, and include every binary completion
and every ordered pair of distinct maximal last-birth roles in each proper
Ferrers child. Actual ratio equations, not presumed unit gains, connect
the nodes. The complete target inventory is:

| Child type | Local nodes | Ratio components | Marks invariant across its component |
|---|---:|---:|---|
| `(5,1)` | 18 | 2 | The root bit |
| `(4,2)` | 16 | 4 | The two common-past chain bits |
| `(4,1,1)` | 12 | 2 | The root bit |
| `(3,2,1)` | 10 | 2 | The root bit |
| Total | 56 | 10 | Distinct marked classes retained |

For a fixed terminal child, a maximal role reads that vertex's strict
past. Marks in the intersection of all these pasts survive every role,
modulo actual child automorphisms. Conversely, a mark outside the
intersection can be changed by moving to a role that does not read it,
changing its full-marking completion there, and moving back. All such
role comparisons occur on the independent full record cube. This explains
the component counts above; the explicit graph independently verifies them.
It does not erase additional marks from individual local node keys or
make their potential values equal. A component scale is shared; node
potentials and ratio gains can differ.

For each complete marked parent row `j=(P,r)` and target component `c`,
define

\[
 A_{jc}=\sum_{\substack{S\subsetneq P\text{ ideal}\\
                         P+e_S\text{ Ferrers},\ c(P,S,r|S)=c}}
             u_{P,r}(S).
 \tag{4}
\]

The sum counts labeled ideals, including both E-to-`(4,1,1)` slots.
There are 128 complete marked rows, 116 marked-parent isomorphism classes
and 288 target proper-slot occurrences. Equal numerical matrix rows do
not identify different marked states. All other proper slots and the full
slot are classified separately when defining leakage.

## 4. Why this boundary system is the exact zero-infimum gate

For a strict complete size-five extension, let `g_j=(A alpha)_j` be its
target proper mass and let `h_j` be its other proper mass. The full mass
is `1-g_j-h_j`. One-step Ferrers departure probability, summing newborn
marks, is therefore

\[
 \ell_j=\begin{cases}1-g_j,&P\text{ of type A or E},\\
                     h_j,&P\text{ of type C or B}.
        \end{cases}
 \tag{5}
\]

The infimum of `max_j ell_j` over strict extensions is zero **if and only
if** the following finite system is feasible:

\[
 \alpha\geq0,\qquad
 A\alpha=\mathbf1\text{ on every marked A/E row},\qquad
 A\alpha\leq\mathbf1\text{ on every marked C/B row}.
 \tag{6}
\]

**Necessity.** Take strict extensions with worst leakage tending to zero
and keep only their target-component scales. Every such component has a
positive occurrence in some target row, whose total mass is at most one;
thus that scale is bounded above by a finite reciprocal matrix entry.
The target vectors lie in a bounded closed nonnegative box. Pass to a
convergent subsequence. Equations (5) force equality on A/E and the row
caps give the C/B inequalities. No compactness of the open strict domain
is assumed.

**Sufficiency.** Given (6), extend its vector by zero on every non-target
component. Closure from section 1 means no outside parent row receives
any target mass. Its proper mass is zero; its full complement is one.
All Ferrers rows have proper mass at most one by (6), and all target
components still satisfy the homogeneous ratio equations. This is a
normalized nonnegative **boundary** extension, not an admitted strict law.

RI-38 supplies a complete strict interior extension `alpha*` of the same
fixed prefix, for example its common positive potential scale with full
complements greater than one half. Its existence is used analytically;
no complete next-layer table is built. For `0<t<1`, set

\[
 \alpha(t)=(1-t)\alpha(0)+t\alpha^*.
 \tag{7}
\]

Every proper component is now positive, full complements are the same
convex mixtures and positive, and locality, equivariance and all complete
scalar-kernel diamonds are preserved. Each marked Ferrers row has
`ell_j(t)=t ell_j(*)<=t`. This proves arbitrarily small worst leakage.
The proof concerns one next layer, not preservation of (6) at future sizes.

Every strict law nevertheless has positive leakage: from a nonempty Ferrers
parent, the empty-ideal birth has positive probability and introduces a
second minimum, so leaves the family. On A/E the positive full complement
also leaves. Thus the exact infimum is zero but no strict zero-leakage
extension attains it. Boundary zeros are not silently admitted.

## 5. Exact rational witness on all marked rows

Canonical components are ordered by their minimum canonical local triple
`(parent relation code, precursor mask, inside-record mask)`. The certificate
retains all ten components. Its only nonzero scales are:

| Component ID | Canonical root | Child class | Scale |
|---:|---|---|---|
| 0 | `(8606,15,0)` | `(5,1)`, root bit 0 | `43010/3321` |
| 1 | `(8606,15,1)` | `(5,1)`, root bit 1 | `1773200/132471` |
| 2 | `(8606,17,0)` | `(4,1,1)`, root bit 0 | `176/41` |
| 3 | `(8606,17,1)` | `(4,1,1)`, root bit 1 | `176/41` |

Components 4–7 are the four `(4,2)` record components, with roots
`(8606,19,r)`, `r=0,1,2,3`. Components 8–9 are the two `(3,2,1)`
components, with roots `(8734,7,r)`, `r=0,1`. Their scales are zero in
this boundary witness, not merged or omitted from the graph.

The active-slot potentials computed from the exact prefix are:

| Parent and slot | Root bit 0 | Root bit 1 |
|---|---:|---:|
| C to `(5,1)` | `1/352` | `1/352` |
| A to `(5,1)` | `81/1100` | `3231/44000` |
| A to `(4,1,1)` | `19/1760` | `7/1760` |
| Each of the two E to `(4,1,1)` slots | `41/352` | `41/352` |

These values hold across every completion of the other record bits as
checked, not by weakening the node keys. Multiplying by the chosen scales
gives the following full row certificate:

| Parent | Root bit | Target child masses | Full complement at the boundary |
|---|---:|---|---|
| C | 0 | `(5,1): 1955/53136` | `51181/53136` |
| C | 1 | `(5,1): 10075/264942` | `254867/264942` |
| A | 0 | `(5,1): 391/410`; `(4,1,1): 19/410` | 0 |
| A | 1 | `(5,1): 403/410`; `(4,1,1): 7/410` | 0 |
| E | either | `(4,1,1): 1`, from two distinct ideals | 0 |
| B | either | All target proper masses zero | 1 |

All non-target proper components have boundary scale zero. A/E equality
and C/B caps hold exactly for all 128 marked rows. The corresponding
full children for C/B remain Ferrers. The [certificate](CERTIFICATE.json)
pins the full target matrix, graph roots, rational scales and analytic
child-mass totals; the [standalone checker](check.py) uses exact fractions.

## 6. Frozen-prefix defects and the limit of this admission result

Every previously committed parent remains an **order ideal** of each later
order under maximal births. Therefore a non-Ferrers frozen parent cannot
later become part of an exact Ferrers whole order: ideal closure would
force the earlier parent to have been Ferrers already. This is stronger
and more specific than merely observing persistence of an arbitrary induced
subposet; section 1 explains why the latter alone would not suffice.

The fixed prefix already gives positive probability to non-Ferrers histories,
including the two-antichain. A strict extension also gives positive departure
probability from every nonempty Ferrers row. Such a departure cannot be
repaired into exact membership by later maximal births. This family is not
an absorbing class under a strict law, and the present witness does not
reset, discard or reclassify any committed record.

An eventual core-plus-tail/defect treatment, a different target, or another
justified construction would require additional premises. None is supplied
or designed here. The gate asks only whether already-Ferrers parents at
the first free layer can have arbitrarily small one-step leakage compatible
with the complete fixed law and all records. Its affirmative answer is not
an all-size feasibility invariant or a stochastic shape theorem.

In particular no concentration near squares, limiting height/width/density,
native dimension, informative quantum-to-order map, metric, mass/source
response, clock or gravity follows. No preferred corner law is imported.
The candidate family and seed remain chosen conditional mathematical
structure; Option B and metric-as-record Status M are unchanged.

## 7. Exact verification, discovery and bounded handoff

The checker re-expresses prefix formulas and RI-41 coefficient data from
the accepted [RI-45 standalone source](../native_growth_neutral_completion_v1/check.py).
Its final execution imports no project module, reads only the adjacent
certificate, uses only the standard library, and writes no file. Whole-parent
enumeration is explicitly capped at size four. At size five it constructs
only the four declared Ferrers representatives, with every mark assignment;
six-event orders are only candidate children and shape-classification inputs.

The complete target calculation covers 128 marked parent rows, 116 marked
row classes, 288 target proper-slot occurrences and 672 other proper-slot
occurrences. Its 56 local nodes form ten components. Four proper child types,
each with all 64 record completions, supply 768 ordered maximal-role ratio
checks: 128 each for `(5,1)`, `(4,2)`, `(4,1,1)`, and 384 for `(3,2,1)`.
There are 12 all-zero cases, zero equal-precursor cases, and 64 quotient
loops. These are complete representative target comparisons under order
transport, not an enumeration of every labeled global size-five diamond.
The closure proof justifies their sufficiency for the selected components.

The prefix reconstruction checks all 707 marked rows and 6065 labeled ideal
slots through parent size four, including strict positivity, normalization
and 585 canonical probability keys. It verifies 436 lower scalar diamonds
and all 7616 raw RI-41 ratios, with 305 local nodes and 109 components at
parent size four. The accepted minimum full mass `33901019/474368400`,
minimum ideal-slot mass `9/681472` and maximum height drift
`14082809/29648025` are recovered exactly. The target certificate is then
checked on all 128 raw marked rows, not only the 116 row-class representatives,
and on all 768 raw target ratios, including boundary-zero components.
A separate main audit also compared all 160 full-record occurrences of
the active slots directly with the potential table in section 5.

For the complete passive payload maps, each two-birth branch sends arbitrary
`D` to the corresponding scalar product times `D/4`. Thus the exact scalar
identities imply the complete-map identities algebraically. No numerical
payload test or informative quantum coupling is claimed.

The graph root manifest SHA-256 is
`b460e8c6a659513f824a619c62ec9d1dfa5c6c847b69c3c7af13325b96948581`;
the exact canonical marked-row matrix SHA-256 is
`bd5bcb1fe255e1018c13c9b3a71764516ecde06693c066dc27a8e73913bcfe04`.
The embedded RI-41 parameter JSON has canonical SHA-256
`465c5de48c69527fc59e8df1f494fd8cea33f8aec243f59b9b2820bd5b1c07a7`,
matched to the accepted certificate source identity
`3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.
The embedded parameter hash is recomputed by the checker. The source-file
identity is provenance metadata, separately verified against the accepted
file at handoff; the standalone checker does not read that accepted file.

Discovery was separate from the certificate: read-only exploratory calls
used accepted RI-45 helper definitions, without invoking its main routine,
and reconstructed only the size-four prefix. A manually keyed ten-column
matrix was checked by a floating linear-program feasibility search in an
external CPython 3.14.0 environment with NumPy 2.5.3 and SciPy 1.18.1. The
sparse rational witness above was then obtained directly from the active
row equations, not accepted on a solver tolerance. The final graph-based
checker reconstructs the actual marked matrix independently of that manual
component keying. No floating solver is part of its acceptance path.

Main replay used CPython 3.14.0 with `-I -S -B`, both normally and with `-O`.
Both runs exited zero with empty stderr in approximately 0.225 seconds each.
Their stdout was byte-identical: 1503 bytes, SHA-256
`3246d8ac8d5ae477e92f0456b796ff002f58e7806e5c96c3803f9405bd204aca`.
Two in-memory negative controls are required to fail for their exact reasons:
zeroing both `(4,1,1)` component scales violates an equality, and doubling
component 0 exceeds a row cap. Neither control changes the certificate file.

An independent reviewer read every checker and certificate line and the complete
note, then replayed both modes with the same interpreter and isolation flags.
Both runs exited zero with empty stderr in approximately 0.228 and 0.230
seconds and reproduced the identical stdout hash above. That reviewer also
compared the embedded roots/default/overrides directly to the accepted RI-41
certificate and the re-expressed seed formulas to RI-45; all matched. A
separate analytic review checked the boundary equivalence, strict mixing,
frozen-prefix obstruction and exact witness arithmetic. The checker author
also cross-checked the complete note against the actual matrix and certificate.
No mathematical or scope blocker was found in these internal reviews.
Coordinator adjudication is separate and recorded in the opening status.

Only `GATE.md`, `check.py` and `CERTIFICATE.json` in this new directory are
authored. Accepted research, coordinator records, measurement work and RET
remain unchanged; RET stays paused. The coordinator owns git/index/publication.
Stop at the source-stable handoff for independent adjudication; no successor,
defect-repair mechanism or all-size Ferrers selection is started.
