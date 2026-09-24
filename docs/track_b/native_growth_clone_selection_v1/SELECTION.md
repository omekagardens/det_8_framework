# RI-46 — a clone selector with occupation-controlled sublinear height

24 September 2026 UTC. **Conditional analytic result; independent coordinator
adjudication accepted.** The complete accepted RI-41 law through parent size
four has an explicit all-size extension with

\[
 \mathbb E H(P_N)=\Theta(\log N),\qquad
 H(P_N)/N\longrightarrow0\ \text{almost surely},\qquad
 H(P_N)\longrightarrow\infty\ \text{almost surely}.
 \tag{1}
\]

The normalized height also converges to zero in every finite positive moment.
The construction does **not** make every row's height drift small. It makes
high-drift parents rare under its actual history law and rapidly returns from
them. RI-45's fixed-row obstruction remains valid.

These are conditional order-regime results, not a DET derivation of the
selector, informative quantum dynamics, manifold correspondence, physical
time, sources or gravity. No next-layer enumeration or executor is introduced.

## 1. Domain, fixed prefix and notation

Keep the complete [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
through **parent size four**, including every component coefficient in its
[exact certificate](../native_growth_height_normalization_v1/CERTIFICATE.json),
all binary marks and earlier record feedback. Free choices begin at parent
size `n=5`, not at the transition from size four to five. The prefix is a
law table, not a stipulation of one realized initial history.

Retain [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md):
finite orders `P`, immutable independently variable binary records `r`, every
ideal strictly positive, reads of records only inside the selected precursor,
permitted access to the whole **unmarked** parent order, marked-parent
equivariance, fixed context, one committed birth per step and a fair newborn
bit. For every ideal `S` and bit `b`, the full scalar-passive map is

\[
 \mathcal B^{P,r}_{S,b}(D)=\tfrac12q_{P,r}(S)D.
 \tag{2}
\]

The complete fixed-carrier complex PSD residual, including off-diagonal
entries and unnormalized branch weights, is retained. Probabilities do not
read `D`. No silent or halt branch is added; this restricted commit model
does not identify all present relational activity with record production.

Write `H(empty)=0`, with height counting vertices in a longest chain.
Appending a vertex whose strict past is `S` changes height by

\[
 H(P+e_S)-H(P)=\mathbf1_{\{H(S)=H(P)\}}.
 \tag{3}
\]

In particular a full birth, `S=P`, always raises height by exactly one.
The proof is `H(P+e_S)=max(H(P),H(S)+1)`.

## 2. Suitable parents and the private-component lemma

Call a nonempty parent **suitable** if every maximal vertex has the same
strict past `C`. Every nonmaximal vertex lies below a maximal vertex in a
finite order, so this condition is equivalent to

\[
 P=C\mathbin{\oplus}\operatorname{Ant}_k,\qquad k\geq1,
 \qquad C=P\setminus\operatorname{Max}(P).
 \tag{4}
\]

Here the ordinal sum places every one of the `k` incomparable top vertices
above every vertex of the core `C`. The core is intrinsic and unique, may
be empty, and is a proper ideal. The preferred precursor is precisely `C`.
Its newborn clones a top vertex's past, yielding
`C op Ant_(k+1)`, still suitable with height `H(C)+1=H(P)`.

Every full birth from **any** parent `P` instead gives `P op Ant_1`. It
has a unique maximum and is suitable, irrespective of the old parent's
suitability or marks. Thus unsuitable parents are not an absorbing class.

### Exact ratio-graph statement

At a fixed size, RI-38's proper nodes are `[P,S,r|S]`: quotient by
isomorphisms of the whole unmarked parent carrying the ideal and its internal
marks together, and erase only marks outside the ideal. Every raw diamond
compares two possible last births in the same unmarked terminal child.
For a preferred node its child is

\[
 T=C\mathbin{\oplus}\operatorname{Ant}_{k+1}.
 \tag{5}
\]

All maximal vertices of `T` are tops. Deleting any one leaves the same
parent/core pair `(C op Ant_k,C)`; deleting two leaves the old diamond base
`C op Ant_(k-1)`. Both old precursors in that base are exactly `C`.
Consequently every raw edge incident to the preferred node has gain
`q_base(C)/q_base(C)=1` and returns to the same node. This includes equal
precursors, both newborn marks, every inherited mark, reversed and parallel
edges, loops and all-zero records. For `k=1` the old base is `C` and its
precursor is full; for empty `C` the argument is the antichain case.

Core marks are present in both precursors and cannot change along such an
edge. Isomorphisms of (5) preserve its core and restrict to core
automorphisms. Thus a preferred component is **one node with unit loops**,
private to its unmarked parent and marked-core isomorphism class. Its
maximal-deletion potential has a single value `u_c>0`.
Core mark assignments may coincide under an actual core automorphism;
unrelated marked-core classes do not merge merely because their potentials
or assigned probabilities happen to be equal. Top marks are absent from
the local key, not deleted from the committed state.

No nonsuitable row can contain a preferred component: its occurrence would
have child (5), and deleting its newborn would give (4). A suitable row
contains exactly **one labeled preferred ideal**, namely its unique core.
It therefore receives exactly one preferred-component contribution, not one
for each of its `k` tops. This controls labeled multiplicities as well as
component identities.

## 3. The fixed recursive selection

Suppose all rows at smaller parent sizes have already been fixed. Use their
actual probabilities in the RI-38 potential

\[
 u_{P,r}(S)=
 \prod_{\varnothing\ne B\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus B,\,r|_{P\setminus B}}(S)^{(-1)^{|B|+1}},
 \qquad S\subsetneq P.
 \tag{6}
\]

Every factor is positive and uses a smaller parent. Each factor reads only
`r|S`; there is no forbidden read later hidden by cancellation. Deletion
is an evaluation of the law on a mathematical input, not record erasure
from an actual history. RI-38 proves this equivariant potential satisfies
all new ratio equations whenever the inherited prefix is admissible.

For example, on (4) its preferred value can also be written

\[
 u_c=\prod_{j=1}^{k}
 q_{C\oplus\operatorname{Ant}_{k-j},\,r|C}(C)
       ^{(-1)^{j+1}\binom{k}{j}}>0.
 \tag{7}
\]

Top marks in this notation are arbitrary extensions of `r|C`; locality
makes their choice irrelevant. The `j=k` term is `q_C(C)`, including the
empty-parent probability one when applicable. This is not permission to
identify distinct marked cores having equal values.

Let `K_n` be the set of **all** preferred components at size `n`. Define

\[
 V_n=\max_{|P|=n,\,r\in\{0,1\}^P}
 \sum_{\substack{S\subsetneq P\text{ ideal}\\c(P,S,r|S)\notin K_n}}
       u_{P,r}(S),\qquad
 \eta_n=\frac1{n+1},\qquad
 \lambda_n=\frac{\eta_n}{2(1+V_n)}.
 \tag{8}
\]

The maximum ranges over the complete marked table, and each row sum counts
every distinct labeled ideal. It excludes **every** preferred component,
not just one selected for the currently realized row. There are finitely
many entries, so `0<=V_n<infinity` and `lambda_n>0`, also if `V_n=0`.
Set component scales and new probabilities, for `n>=5`, by

\[
 \alpha_c=
 \begin{cases}(1-\eta_n)/u_c,&c\in K_n,\\
 \lambda_n,&c\notin K_n,
 \end{cases}
 \qquad q_{P,r}(S)=\alpha_{c(P,S,r|S)}u_{P,r}(S)
 \quad(S\subsetneq P),
\]
\[
 q_{P,r}(P)=1-\sum_{S\subsetneq P\text{ ideal}}q_{P,r}(S).
 \tag{9}
\]

All these quantities are fixed from the law table once at each size. They
are not normalized after inspecting the actual current record assignment.
At evaluation a proper slot uses its local key; the full slot may read
all parent records. The preferred key retains only its permitted core
marks. The parameter `n=|P|` is intrinsic record count, not a physical clock.

### Strictness and all-size consistency

Let `a(P,r)` denote the total new mass of nonpreferred proper ideals.
Equations (8)–(9) give uniformly

\[
 0\leq a(P,r)\leq\lambda_n V_n<\eta_n/2.
 \tag{10}
\]

A suitable row has preferred mass `1-eta_n` exactly and full complement
`eta_n-a(P,r)>eta_n/2`. An unsuitable row has no preferred slot, and its
full complement is `1-a(P,r)>1-eta_n/2>eta_n/2`.
Every proper probability, full complement and fair-bit branch is strictly
positive; all rows sum to one. No zero boundary law is used.

The private-component lemma makes the large preferred scales compatible
across every occurrence. All remaining scales are positive component
constants. Each new diamond has its two proper slots in one component;
rescaling its potential by the same constant preserves its ratio. A new
full complement cannot be a second precursor in a new incomparable-birth
diamond because that precursor excludes the other newborn. Inherited rows
and diamonds are unchanged. Equality of the resulting scalar multipliers
therefore gives equality of the **entire** maps (2), not only total masses
or diagonal entries, for every admitted `D`.

The potential's locality and equivariance, the invariant preferred keys
and the complete-table maximum give locality and equivariance of (9),
including its full complement. The resulting level satisfies every premise
needed for the next application of (6). Induction constructs one all-size
strict law from the actual RI-41 prefix. Potentials must be recomputed after
each selection; copying later potentials from another normalization would
not be this law. No efficient evaluation or physical implementability is
asserted for these finite-table formulas.

## 4. Conditional occupation and height estimates

Normalization gives the classical marked-history measure by the construction
in [RI-39](../native_growth_history_height_v1/HISTORY_HEIGHT.md); its particular
linear-height normalization is **not** used. Let `F_n` contain the complete
marked history through size `n`, `H_n=H(P_n)`, and

\[
 U_n=\mathbf1_{\{P_n\text{ unsuitable}\}},\qquad
 t_n=\mathbb E[H_{n+1}-H_n\mid\mathcal F_n]
     =\sum_{S:H(S)=H(P_n)}q_{P_n,r_n}(S).
 \tag{11}
\]

All births outside the nonpreferred proper set give a suitable next parent:
full births always do, and preferred births stay suitable. Both fair marks
have the same unmarked child. Equations (3) and (10) thus imply, at **every**
history and for every `n>=5`,

\[
 \Pr(U_{n+1}=1\mid\mathcal F_n)<\eta_n/2,\qquad
 \Pr(\text{full birth at step }n\mid\mathcal F_n)>\eta_n/2,
 \qquad t_n\leq\eta_n+U_n.
 \tag{12}
\]

For the last bound, a suitable row has a height-preserving preferred birth
of mass `1-eta_n`, so its drift is at most `eta_n`. An unsuitable row's
drift is at most one. No independence or averaging uniformly over parent
types is used. In fact unsuitable rows have drift greater than
`1-eta_n/2`; their actual occupation, not their rowwise drift, is controlled.

### Expected height and occupation, with exact cutoff

Fix any `m>=5` and condition on an arbitrary positive-probability finite
history `h_m`. All following sums start at this cutoff; `H_m` and `U_m`
are its realized offsets. For `n>=m+1`, the tower rule applied to (12) gives

\[
 \mathbb E[U_n\mid\mathcal F_m]\leq\frac1{2n}.
 \tag{13}
\]

Write `L_(m,N)=sum_(k=m+1)^N 1/k`. For `N>m`, summing conditional height
increments and using full births for the lower bound yields

\[
 H_m+\tfrac12 L_{m,N}
 <\mathbb E[H_N\mid\mathcal F_m]
 \leq H_m+U_m+L_{m,N}
                  +\tfrac12\sum_{n=m+1}^{N-1}\frac1n
 \leq H_m+U_m+\tfrac32\log(N/m).
 \tag{14}
\]

Here `L_(m,N)<=log(N/m)` by integral comparison, while
`L_(m,N)>=log((N+1)/(m+1))`. Thus expected height is actually
`Theta(log N)` for fixed cutoff, and in particular `O(log N)`.
The unsuitable-parent count

\[
 B_{m,N}=\sum_{n=m}^{N-1}U_n
 \quad\text{satisfies}\quad
 \mathbb E[B_{m,N}\mid\mathcal F_m]
 \leq U_m+\tfrac12\sum_{n=m+1}^{N-1}\frac1n=O(\log N).
 \tag{15}
\]

Taking `m=5` includes every possible initial state from the fixed prefix.
Since there are finitely many such marked histories, unconditioning gives
the same asymptotic conclusions. Conditioning later requires (14)–(15)
with that later cutoff and offsets, not reuse of a previously centered sum.

### Almost-sure sublinearity and all finite positive moments

The logarithmic expectation alone is not being mistaken for almost-sure
convergence. Both `H_N` and `B_(m,N)` are nonnegative and nondecreasing in
`N`. For either quantity `Z_N`, (14) or (15) and Markov's inequality give,
for fixed `epsilon>0` and all sufficiently large integers `j`,

\[
 \Pr\{Z_{2^j}/2^j>\epsilon\mid h_m\}
 \leq\frac{C_m(1+j)}{\epsilon 2^j}.
 \tag{16}
\]

The series is finite. The first Borel--Cantelli argument, at every positive
rational threshold, gives dyadic convergence to zero almost surely. If
`2^j<=N<2^(j+1)`, monotonicity gives
`Z_N/N<=2 Z_(2^(j+1))/2^(j+1)`. Thus both height density and unsuitable
occupation density tend to zero along **all** sizes almost surely.

Since `0<=H_N/N<=1`, dominated convergence gives, for every `0<p<infinity`,

\[
 \mathbb E[(H_N/N)^p\mid h_m]\longrightarrow0.
 \tag{17}
\]

These are ordinary `L^p` norm limits for `p>=1`, finite positive moment
limits also for `p<1`, and unconditional limits after the finite mixture.
No `L^infinity` limit or almost-sure `O(log N)` height bound is claimed.
The occupation bound does not assert eventual permanent suitability:
the upper bounds in (13) are not summable. Equations (12), (15)–(16) make the
cumulative predictable drift sublinear, consistently with the martingale
criterion in [RI-43](../native_growth_sublinear_selection_v1/SELECTION.md).

### Height diverges: a conditional product, not an expected-count inference

Let `J_(n+1)` indicate a full birth at parent size `n`. Fix a deterministic
cutoff `l>=5`. Conditional on the entire `F_n`, (12) implies
`Pr(J_(n+1)=0|F_n)<=1-1/[2(n+1)]`. Iterating the tower rule on the event
that all preceding births since `l` were nonfull gives

\[
 \Pr(J_{l+1}=\cdots=J_N=0\mid\mathcal F_l)
 \leq\prod_{n=l}^{N-1}\left(1-\frac1{2(n+1)}\right)
 \leq\exp\left(-\tfrac12\sum_{n=l}^{N-1}\frac1{n+1}\right)
 \longrightarrow0.
 \tag{18}
\]

Continuity from above gives probability zero of no full birth after `l`.
The event of finitely many full births is the countable union of these
events over `l`, hence also has probability zero. Every full birth raises
height exactly one and no birth lowers it. Therefore `H_N->infinity`
almost surely, also after conditioning on any finite admitted history.
The argument needs neither independent births nor divergence of an
expected count as a substitute for occurrence.

As a finite-order corollary, partition vertices by the length of a longest
chain ending there. Each of the `H_N` classes is an antichain, so
`N<=H_N width(P_N)`. From `H_N/N->0`, width therefore diverges almost
surely as well. These are order invariants at each finite size; density
limits refer to this specified birth-prefix exhaustion, not arbitrary
infinite natural re-enumerations.

## 5. Reconciliation and the boundary of the result

[RI-45](../native_growth_neutral_completion_v1/COMPLETION.md) proves
`tau(Q)>1756883/3859907` for every strict extension of the fixed prefix at
the all-zero five-parent `Q=(0,1,3,3,0)`. Its maxima have strict pasts
`{a,b}`, `{a,b}` and empty, so it is unsuitable. This selector gives the
stronger rowwise bound `tau(Q)>=q_Q(Q)>1-eta_5/2=11/12`.
There is no cancellation or escape from the separator at that fixed row.
Its next child is suitable with probability greater than `11/12`.
At later sizes (12) controls entry into any unsuitable row, regardless of
the current history; (15)–(16) control total occupation.

In contrast, RI-43's antichain-only rule had an absorbing non-antichain
high-drift class. Here full birth returns from any unsuitable parent to a
suitable one without removing a single relation or record. The wider
suitable class is the explicit repair, not an assumption that the previous
negative result was wrong. For every size at least five there are unsuitable
parents (for example a nontrivial chain plus an isolated vertex), so the
worst-row drift of this very law tends to one, not zero.

The proved yield is a **fixed conditional definition and its theorems**:
strict local/equivariant scalar growth, all diamonds, logarithmic expected
height, sublinear but diverging typical height, and diverging width.
It does not settle the stronger uniform vanishing-drift selection question.
No manifold dimension, Lorentzian metric, typical local geometry, physical
clock, matter coupling, mass response or gravity follows from these screens.
The seed and this component selection remain extra chosen mathematical
structure; the passive payload is not made informative. No metric, mesh
or borrowed growth kernel defines (6)–(9), but that input fact alone is not
a native quantum-to-geometry derivation. Option B and metric-as-record
Status M are unchanged.

## 6. Evidence and bounded handoff

All new claims above are analytic. No simulation, new layer table, executor,
certificate or numerical optimizer was created or run. Accepted source
checks are premises, not tests replayed in this packet.

Three read-only internal reviewers read the complete note and independently
passed its proof and scope checks with no mathematical blockers. Their
checks covered component privacy and marked-core multiplicities, the fixed
recursive law and full scalar diamonds, exact conditional cutoffs, both
harmonic bounds, dyadic almost-sure convergence, the conditional-product
divergence argument, width and the RI-45 reconciliation. The explicit
limitations distinguish vanishing occupation from eventual suitability and
expected logarithmic growth from an unproved almost-sure logarithmic bound.
No reviewer edited source or executed a research check. These reviews are
not coordinator acceptance, machine-checked proofs or empirical evidence.

All six local Markdown targets exist. Scoped trailing-whitespace and
conflict-marker scans are clean. SHA-256 checks of the six referenced
accepted sources agree with their accepted identities, including the full
RI-41 certificate and the published RI-45 note; none was modified. A final
source identity accompanies the handoff. Coordinator adjudication is recorded in the opening status.

Only this new note is authored. Accepted sources, coordination records,
measurement work and RET remain unchanged; RET is paused. The coordinator
owns git/index/publication. Stop this bounded packet at source-stable handoff
for independent adjudication; no alternate family or successor is opened.
