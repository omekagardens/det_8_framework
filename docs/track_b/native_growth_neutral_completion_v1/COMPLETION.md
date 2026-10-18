# RI-45 — first-free-layer preserving-only completion is infeasible

24 September 2026 UTC. **Exact fixed-layer obstruction; independent
coordinator adjudication accepted.** With the complete accepted
[RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
held fixed through parent size four, the preserving-only equations
`A_0 beta=1, beta>=0` fail at parent size **five**. A seven-row signed rational
separator proves this in the height-three block. Moreover, every strict
extension obeys

\[
 \tau(Q)>\frac{1756883}{3859907}\approx0.4552
 \tag{1}
\]

at the particular all-zero marked parent
`Q={a<b<c,d; e isolated}`: a two-vertex chain `a<b`, two tips `c,d` above
`b`, and isolated `e`. Consequently the layer's worst-row drift has this
positive lower bound. It is not asserted optimal.

This rejects zero-infimum completion at this first free layer. It does not
reject a sequence of positive layer infima tending to zero, determine typical
histories, or establish an all-size impossibility. No parent-size-six layer,
propagation analysis or new model is opened here.

## 1. Domain, source boundary and exact decision

Retain [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md):
finite committed orders, immutable independently variable binary marks,
every ideal strictly positive, precursor-record locality, permitted access
to the whole unmarked parent order, marked-parent equivariance, one birth
with total mass one, fair newborn marks and the passive full-kernel maps

\[
 \mathcal B^{P,r}_{S,b}(D)=q_{P,r}(S)D/2.
 \tag{2}
\]

The complete fixed-carrier complex PSD kernel, including off-diagonal entries
and unnormalized branch weights, remains in each map. No source, clock,
nonpassive quantum coupling, geometric or physical law is introduced.
The model premises and seed selection are conditional, not DET entailment.

The earlier `interior_a` parameters and **all** RI-41 parent-four component
coefficients remain fixed, not merely their height bound. The new potentials
`u` are computed from those actual rows by maximal deletion. No zero branch
is inserted into the accepted prefix. This is the first test of the new
criterion in [RI-43](../native_growth_sublinear_selection_v1/SELECTION.md),
not a replay of its rejected antichain-focused rule.

At the new layer, retain every distinct labeled proper ideal in

\[
 A_{jc}=\sum_{S\text{ in component }c}u_j(S),\qquad
 B_{jc}=\sum_{\substack{S\text{ in component }c\\H(S)<H(P_j)}}u_j(S),
 \qquad \tau=\mathbf1-B\alpha.
 \tag{3}
\]

Strict laws require `alpha>0,A alpha<1`; full complements are
`f=1-A alpha`. A preserving-only component has at least two tallest maxima
in its fixed terminal child. Mixed components have a unique tallest maximum
and both height-raising and height-preserving incoming roles. Write `A_0`
for preserving-only columns. On these columns `A_0=B_0`.

RI-43 proves that the strict infimum of worst-row drift is zero iff
`A_0 beta=1` has a nonnegative solution. Such a solution would be a closed
boundary completion, not an admitted law; strict mixing would be needed.
The present task is to decide that equality, not optimize a floating surrogate.

## 2. Height blocks and the two analytic completions

Every preserving-only component has a fixed unmarked terminal child `T`.
Deleting any of its maxima leaves height `H(T)` unchanged. Its column can
therefore meet only parent rows of that one height. Thus `A_0` decomposes
by parent height. This statement does not identify all marked representations
of a child as one component. Mixed columns of the full matrices can connect
adjacent heights, which matters for any drift bound.

### Height one: all antichain records

There is one unmarked five-antichain. Its only height-preserving precursor
is empty, giving the six-antichain. That node is private to this block and
erases every record. If `a_j=q_(Ant_j)(empty)` in the fixed prefix, its
potential is

\[
 u_0=\frac{a_4^5a_2^{10}}{a_3^{10}a_1^5}>0.
 \tag{4}
\]

This is the maximal-deletion formula; the empty-parent factor is one.
The single coefficient `beta_0=1/u_0` completes all 32 labeled record rows.
The six marked antichain isomorphism classes are not six different local
empty-slot variables.

### Height five: all chain records

The five-chain's sole preserving-only slot is its first four vertices.
Its child has two highest tips above that four-chain. For each of the 16
four-bit words `r` on the precursor, the component is private and has

\[
 u_r=q_{\mathrm{chain}_4,r}(\mathrm{full})>0,
 \qquad \beta_r=1/u_r.
 \tag{5}
\]

Both values of the fifth/top mark use this component, so all 32 marked
chain rows are completed. The four-chain's full probability happens to be
independent of its own top mark, by normalization and locality of its proper
slots. Equal values of `u_r` do **not** merge components: all four precursor
marks are retained, and a chain's core has no nontrivial automorphism.

These are closed auxiliary completions only. All full complements in these
completed blocks vanish. They do not supply a strict law or decide the middle
blocks; the obstruction below is in height three.

## 3. Seven parents and six terminal children

All seven separator rows have five events, height three and all-zero marks.
The natural predecessor masks below encode the complete transitive order:
entry `i` lists the predecessor labels through their bit mask. Each mask is
an ideal of the preceding order. These identify the rows without an image
or an arbitrary enumeration index.

Let `W(P)` be the fixed product of ideal probabilities along one natural
construction of that marked parent. It omits fair-bit factors. The accepted
prefix diamonds make it invariant under natural relabeling. It is **not**
an unlabeled orbit probability. The auxiliary `W(P)/|Aut(P)|` below is an
incidence-counting weight, not a normalized probability either.

| Parent | Predecessor masks | `Aut(P)` | `c(P)` | `W(P)` | Signed integer `y(P)` |
|---|---|---:|---:|---|---:|
| `Q` | `(0,1,3,3,0)` | 2 | -1 | `3859907/1533312000` | -3859907 |
| `P0` | `(0,1,3,0,0)` | 2 | 1 | `19/12266496` | 2375 |
| `P2` | `(0,1,3,1,0)` | 1 | 1/2 | `19/12266496` | 2375 |
| `P3` | `(0,1,3,0,8)` | 1 | 1/2 | `19/1393920` | 20900 |
| `P4` | `(0,1,3,3,3)` | 6 | 3 | `1/2044416` | 750 |
| `P5` | `(0,1,3,0,9)` | 1 | 1/2 | `19/253440` | 114950 |
| `P6` | `(0,1,3,0,11)` | 1 | 1/2 | `89167/69696000` | 1961674 |

The final column is exactly

\[
 y(P)=3066624000\,c(P)\frac{W(P)}{|\operatorname{Aut}(P)|}.
 \tag{6}
\]

Every unlisted row has coefficient zero; choose **one** representative of
each listed marked isomorphism class, not every labeled copy. Matrix row
sums still count all labeled ideals of that representative.

For `Q`, write the labels as `a=0,b=1,c=2,d=3,e=4`. A preserving ideal
cannot contain either highest tip `c,d`. There are exactly six such ideals.
Append a newborn `f` at each and delete each maximal vertex of the child.
The complete deletion inventory is:

| Newborn's precursor in `Q` | Parent types obtained by maximal deletion |
|---|---|
| Empty | `2 Q + 2 P0` |
| `{a}` | `Q + 2 P2 + R` |
| `{e}` | `Q + 2 P3` |
| `{a,b}` | `3 Q + P4` |
| `{a,e}` | `Q + 2 P5` |
| `{a,b,e}` | `Q + 2 P6` |

Here `R=(0,1,3,3,1)` and `c(R)=0`. Each row of this table has total
`c`-weight zero. Every other preserving-only child has no deletion yielding
`Q`, and all its nonzero `c`-weights are positive. Its total is nonnegative.

### Why deletion counts give a column certificate

Let `m(P,T)` count the distinct labeled ideals of a fixed parent `P` whose
child is isomorphic to `T`. Let `d(P,T)` count maximal vertices of `T` whose
deletion yields `P`. Counting isomorphisms of such pairs gives

\[
 m(P,T)|\operatorname{Aut}(T)|
 =d(P,T)|\operatorname{Aut}(P)|.
 \tag{7}
\]

For all-zero marked copies, marked and unmarked automorphism groups agree.
RI-38's common-child potential identity is `W(P)u_P(S)=Phi(T)`. All incoming
roles of this one all-zero completion lie in the same ratio component; this
does not merge other marked completions. Consequently pairing the row
weights `c(P)W(P)/Aut(P)` with that component's column gives

\[
 \frac{\Phi(T)}{|\operatorname{Aut}(T)|}
 \sum_{v\in\operatorname{Max}(T)}c(T\setminus v).
 \tag{8}
\]

The six-child table makes this zero for every preserving component touched
by the negative row. A column not touched by that row has only nonnegative
row coefficients. This proves nonnegativity on **every** preserving-only
column, including those using other record classes. It does not discard
marks or replace labeled ideal counts by a quotient count.

## 4. Exact separation and a stronger actual-drift bound

For the matrix at this fixed prefix, (6)--(8) give

\[
 y^T A_0\geq0,\qquad
 y^T\mathbf1=-1756883<0.
 \tag{9}
\]

If `A_0 beta=1` with `beta>=0`, the left pairing would be both nonnegative
and negative. This is a signed exact Farkas separator, with its contradiction
proved directly; no numerical infeasibility status is a premise.

There is also a direct quantitative bound that avoids estimating mixed
coefficients separately. Put

\[
 L=3859907,\qquad \sum_{P\ne Q}y(P)=2103024,\qquad
 \kappa=L-2103024=1756883,
\]
\[
 v_c=\sum_{P\ne Q}y(P)A_{Pc}-L B_{Qc}.
 \tag{10}
\]

Because `Q` already has two tallest maxima, every height-preserving birth
from `Q` lands in a preserving-only component. There (9) proves `v_c>=0`;
on a mixed component `B_Qc=0`, so (10) is a sum of nonnegative terms.
Thus `v>=0` on **all** components, including mixed components meeting other
height blocks.

For any strict extension `alpha`, with full complements `f_P=1-A_P alpha`,
the exact identity is

\[
 L\tau_Q-\kappa
   =\sum_{P\ne Q}y(P)f_P+v^T\alpha>0.
 \tag{11}
\]

All six positive coefficients multiply strictly positive full complements.
This proves (1); in the closed relaxation it proves the corresponding
nonstrict bound. It bounds the specified all-zero row and its transported
isomorphic copies, and hence the worst row. It does not bound every marking
or the average occupied row. The lower bound is not asserted to be an optimum
or an attained closed minimum.

### General separator bound, independently checked but not needed for (1)

For another separator `y`, split mixed columns as `A_1,B_1`, let
`R=A_1-B_1>=0`, `r_c=max_j R_jc>0`, and `y^T1=-kappa<0`. With
`delta=max_j tau_j`, the identity `tau=f+R alpha_1` implies
`f_j<=delta` and `alpha_c<=delta/r_c`. Therefore

\[
 \delta\geq
 \frac{\kappa}{\|y^-\|_1+
       \sum_c\max(0,-y^T A_{1,c})/r_c}>0.
 \tag{12}
\]

Indeed pair `1=A_0 alpha_0+A_1 alpha_1+f` with `y`, drop its nonnegative
neutral term, and bound each negative contribution using those inequalities.
The denominator is positive because `y^T1<0`. Using `||y||_1` instead gives
a valid weaker bound. The `r_c` maxima and `delta` must include the **complete
layer**: a mixed column can have its raising row outside the separator's
height block. We do not evaluate (12) or infer strict inequality from it;
the stronger explicit identity (11) supplies the certified number here.

## 5. Certificate and exact reconstruction

[CERTIFICATE.json](CERTIFICATE.json) records the seven explicit marked
parents, canonical row keys, path weights, automorphism counts, signed
coefficients, six-child deletion table and the exact bound. It also pins the
fixed RI-41 coefficient data and the deterministic component-root manifest.
There are no floating coefficients or optimized values to refit.

The standalone [checker](check.py) uses only Python's standard library and
imports no project code. Orders are tuples of transitive predecessor masks.
Appending every ideal generates each natural parent exactly once, up to
size five. Individual size-six **terminal children** are formed for height
and diamond/deletion checks; there is no size-six parent enumeration or law.

The fixed RI-41 roots and rational coefficients are re-expressed as local
data. Their canonical sorted compact JSON, with one final newline, has
SHA-256 `465c5de48c69527fc59e8df1f494fd8cea33f8aec243f59b9b2820bd5b1c07a7`,
independently obtained from the accepted certificate using `jq`. This binds
all its roots and coefficients, not just the reproduced extrema. The original
accepted certificate has SHA-256
`3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969`.

For a local key, minimize the triple of edge mask, ideal mask and internal
record mask over all carrier permutations, retaining the whole unmarked
parent. Components are ordered by their minimum canonical key. Full marked
row representatives use the same key with the full ideal; equal rows are
compared before deduplication. No record is dropped merely because two
potentials have equal values. Every distinct labeled ideal contributes before
aggregation.

All 798 reconstructed component roots are available in `--matrix` output.
Their compact JSON array without a newline has SHA-256
`fd4e67382b7ec0e12f7f058a911cf17fc54fb2e30b398b10e7451748fd012d59`.
The certificate explicitly lists the six preserving roots touched by `Q`:
`(134,3,0)`, `(142,3,0)`, `(398,3,0)`, `(398,16,0)`, `(398,17,0)`,
`(398,19,0)`. Separator coefficients are attached to explicit row keys,
not an ambiguous component traversal index.

The checker reconstructs the fixed parent-four table, then the new layer,
checks every raw ratio against the potentials, and verifies both (9) on all
516 preserving-only columns and (10) on all 798 columns. The common fair-bit
factor `1/4` cancels in the raw two-birth scalar equality; that equality
multiplies the complete arbitrary `D`, not a normalized or diagonal summary.
Locality/equivariance are structural from the quotient and deletion formula,
corroborated by agreement at each shared key. No separately counted
permutation-comparison suite or nonpassive matrix test is claimed.

The height helper is used only on full orders and ideals, never arbitrary
subsets. Extreme block reciprocals are checked against all 32 labeled record
assignments in each block. Path weights and automorphism counts are
reconstructed separately, and every maximal deletion in the six-child table
is checked. Two negative controls reject a reversed separator and omission
of the compensating `P4` row.

## 6. Actual coverage, verification and limits

The analytic block reduction and six-child cut came first. An independent
exact matrix reconstruction corroborated them. No floating solver was needed
or used, and no unrelated executor or accepted suite was run.

| Parent-five height | Marked labeled rows | Marked row classes | Preserving-only components |
|---|---:|---:|---:|
| 1 | 32 | 6 | 1 |
| 2 | 5024 | 382 | 82 |
| 3 | 5504 | 782 | 290 |
| 4 | 832 | 288 | 127 |
| 5 | 32 | 32 | 16 |

The complete new layer has 357 natural parents, 11,424 marked rows,
142,944 proper-ideal occurrences, 2,961 local quotient nodes, 798 components
(516 preserving-only and 282 mixed) and 1,490 marked row classes. All 216,128
raw new equations are retained, including 3,377 all-zero, 22,848
equal-precursor and 28,176 loop cases. Union-find component aggregation does
not deduplicate the raw checks or labeled normalization summands.

Reconstructing the fixed parent-four component table requires its 640 marked
rows, 5,072 proper slots, 305 nodes, 109 components and 7,616 raw ratios.
This is an in-process dependency reconstruction, not execution of the
accepted RI-41 checker. Earlier-prefix validity remains an accepted premise;
the 436 still-earlier diamonds are not replayed.

The reproducibility commands are

```sh
python3 -I -S -B docs/track_b/native_growth_neutral_completion_v1/check.py
python3 -I -S -B -O docs/track_b/native_growth_neutral_completion_v1/check.py
```

Main author runs on Python 3.14.0, Darwin arm64, passed in both modes with
byte-identical 1,242-byte stdout, SHA-256
`0cda0878682aa6165a41666a9cce147f80dfeba71d3ca704263eb9ef65144b12`.
An independent complete checker/certificate reviewer ran both commands,
also obtaining that hash (about 2.83 seconds per run). Explicit checks do not
depend on Python `assert`; no output or cache files are written by the checker.

Three read-only internal reviewers read the complete note and reported no
proof or scope blockers. The code reviewer also audited the full certificate;
the other two independently checked the analytic deletion/automorphism and
bound arguments, without rerunning the full matrix. These are internal reviews,
not coordinator acceptance or physical evidence. All five local Markdown
targets resolve; whitespace/conflict-marker checks are clean. Final SHA-256
source identities accompany the handoff.

The height-three separator alone decides the full completion question;
heights two and four are not separately classified as feasible or infeasible.
No strict mixture witness is supplied because no full neutral completion
exists here. In particular, RI-43's strongest zero-infimum-per-layer invariant
cannot begin at this layer with this fixed prefix.

The broader target remains open: one finite floor does not prevent positive
layer gaps tending to zero later, and a rare marked row does not determine
occupation-weighted drift. Nor would finite feasibility elsewhere prove
propagation by continuity: next-layer maximal-deletion denominators can
approach zero as strict mixtures approach boundary completions.

Return this exact obstruction for adjudication before choosing a revised
quantitative invariant or a typical-history selection candidate. Neither is
started here. Only these three reserved files are authored; accepted sources,
coordinator records, measurement work and RET remain untouched. Root owns
git/index/publication. Release the reservation and stop this packet at stable
handoff. Option B, Status M and the RET pause are unchanged.
