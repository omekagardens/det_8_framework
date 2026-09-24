# RI-41 — exact finite-layer normalization versus height growth

24 September 2026 UTC. **Conditional finite-layer result; independent
coordinator adjudication accepted.** For the preselected `interior_a` prefix
through parent size three, a common scale fails the requested half-height
screen at parent size four. Component scales pass: the exact rational
[certificate](CERTIFICATE.json) has every branch strictly positive and

\[
 \max_{P,r}\Pr\{H(P_{\rm next})=H(P)+1\mid P,r\}
 =\frac{14082809}{29648025}<\frac{19}{40}<\frac12.
 \tag{1}
\]

This is one finite law-table extension, not an optimal scale, an asymptotic
height law, a DET-selected law, geometry or gravity. It does not undo
[RI-39's rejection](../native_growth_history_height_v1/HISTORY_HEIGHT.md)
of its particular all-size normalization. It shows that its half-mass
constraint is not forced at this layer by the retained ratio equations.

## 1. Fixed premises and precisely the selected prefix

Retain [RI-38](../native_joint_growth_extension_criterion_v1/CRITERION.md):
finite committed orders, immutable independently variable binary marks,
every ideal eligible with strictly positive probability, strict reads of
records only in the selected precursor, whole-unmarked-parent order access,
marked-parent equivariance, one commit and total probability one. Newborn
marks are fair; the complete fixed-carrier complex PSD kernel is retained
by the maps

\[
 \mathcal B^{P,r}_{S,b}(D)=q_{P,r}(S)D/2.
 \tag{2}
\]

The scalar probabilities do not read `D`; the whole unnormalized payload,
including off-diagonal entries, remains in composed maps. These are
conditional mathematical premises, not a derivation of quantum dynamics
or a claim that all present activity produces a record. No silent/halt
branch, physical clock, source/mass model or nonpassive map is introduced.

Use exactly the prescribed RI-38 `interior_a` fixture:

\[
 a=2/3,\quad c=1/5,\quad d=1/4,\quad f(0)=1/6,\quad f(1)=1/3,
\]
\[
 g=(1-a)c/a=1/10,\quad k=1-d-2g=11/20,
 \quad h_0=19/30,\quad h_1=7/15.
 \tag{3}
\]

The singleton, two-chain and two-antichain rows are respectively
`(a,1-a)`, `(c,f(r),h_r)` and `(d,g,g,k)`. Keep the **unchanged**
[RI-36 size-three extension](../native_joint_growth_extension_v1/EXTENSION.md)
with fixed scale `e=1/44`. Its proper-slot table is:

| Parent shape | Proper probabilities (full slot is the complement) |
|---|---|
| Three-antichain | Empty `e`; each singleton `e*g/d`; each pair `e*k/d`. |
| Edge `u<v` plus isolated `w` | Empty and `{w}`: `e`; `{u}`: `e*f(r_u)/c`; `{u,v}`: `e*h_(r_u)/c`; `{u,w}`: `e*k/g`. |
| Fork `u<v,u<w` | Empty and `{u}`: `e`; each root-plus-leaf ideal: `e*h_(r_u)/f(r_u)`. |
| Join `u<w,v<w` | Empty, each singleton root and the root pair: `e`. |
| Three-chain | Empty, root and initial pair: `e`. |

Each distinct labeled ideal is counted. None of these seed rows, their
feedback or accepted source files is changed. Only the new size-four layer
is selected below; all new incomparable-birth diamonds have size-three
bases and size-five terminals.

## 2. General common-scale tradeoff

Fix any admissible finite prefix and a next **nonempty** parent size `n`.
Use the strictly positive RI-38 maximal-deletion potential

\[
 u_{P,r}(S)=
 \prod_{\varnothing\ne T\subseteq\operatorname{Max}(P)\setminus S}
 q_{P\setminus T,r|_{P\setminus T}}(S)^{(-1)^{|T|+1}},
 \qquad S\subsetneq P.
 \tag{4}
\]

The nonempty omitted-maxima set exists for every proper ideal. These are
evaluations of a fixed smaller-parent law, not deletions of actual records.
The potential obeys every inherited ratio constraint, strict record locality
and equivariance. A common scale refers specifically to this chosen potential;
independent rescalings of its components would define a different common
family.

For each complete marked row `j=(P,r)` define

\[
 U_j=\sum_{S\subsetneq P}u_j(S),\quad
 B_j=\sum_{\substack{S\subsetneq P\\H(S)<H(P)}}u_j(S),\quad
 M=\max_j U_j,\quad b=\min_j B_j.
 \tag{5}
\]

Sums run over **distinct labeled ideals**, not just distinct quotient
nodes. The empty ideal preserves height for a nonempty parent, so `b>0`;
also `M>0`. Proper probabilities `epsilon*u` and full complements are
strictly positive exactly when `0<epsilon<1/M`.

Since `H(P+e_S)=max(H(P),H(S)+1)`, the full ideal and any proper ideal
containing a longest chain raise height by one. No ideal raises it by more
than one. Summing both newborn marks, the actual height-raising probability is

\[
 \tau_j=(1-\varepsilon U_j)+\varepsilon(U_j-B_j)
        =1-\varepsilon B_j.
 \tag{6}
\]

Thus

\[
 \max_j\tau_j=1-\varepsilon b,\qquad
 \inf_{0<\varepsilon<1/M}\max_j\tau_j=1-\frac bM.
 \tag{7}
\]

The infimum is **not attained**: `b>0` and reaching `epsilon=1/M` makes
at least one full complement zero. In particular, every row can have
`tau_j<=1/2` under a common scale iff `M<2b`, not `M<=2b`. Equality gives
only a forbidden boundary solution. These formulas concern `n>=1`; the
empty parent's sole birth necessarily raises height and has no proper slot.

## 3. Component-scale feasibility and its strict domain

Retain exactly RI-38's proper-slot node quotient
`[P,S,r|S]`: whole parent order, selected ideal and all its marks are
transported together. Only marks outside `S` are forgotten. Include every
raw ratio equation, including loops, parallel edges, equal precursors,
all-zero assignments and both newborn marks. Let `c(i)` index the connected
components of its bidirected ratio graph. Every positive solution of the
ratio equations is

\[
 q_j(S)=\alpha_{c([P,S,r|S])}u_j(S),\qquad\alpha_c>0.
 \tag{8}
\]

Indeed the ratio between any positive solution and `u` is constant along
each edge and hence each component; conversely such scales preserve all
ratios. Isolated nodes must be retained as components too. New full slots
do not enter these diamond equations; normalization fixes them.

Define finite matrices

\[
 A_{jc}=\sum_{\substack{S\subsetneq P\\c([P,S,r|S])=c}}u_j(S),\qquad
 B_{jc}=\sum_{\substack{S\subsetneq P,\ H(S)<H(P)\\c([P,S,r|S])=c}}u_j(S).
 \tag{9}
\]

Every occurrence of a labeled ideal contributes, even when several map to
one node. Then the full exact feasibility condition is

\[
 \alpha>0,\qquad A\alpha<\mathbf1,\qquad
 \tau=\mathbf1-B\alpha.
 \tag{10}
\]

The requested target adds `B alpha>=1/2` in every row. The inequalities
`alpha>0` and `A alpha<1` are strict; a zero proper branch or full complement
is not an admitted law. Scales are fixed from the entire law table, never
adapted to forbidden actual record reads. Full complements can read full
records; proper slots retain their original local keys. Equivariance follows
from the quotient and the complete labeled sums.

A closed linear-program relaxation `alpha>=0,A alpha<=1` may guide discovery
or give bounds. It cannot by itself certify a strict law. Each component
occurs positively in some row, so this closed feasible set is bounded; it is
also closed and nonempty. A strictly feasible point exists by taking all
scales sufficiently small. Mixing any closed feasible point with that
interior point approaches its value through strict laws. Consequently the
closed maximum of `min_j(B alpha)_j` is the supremum for strict laws.

That supremum is not attained in the strict domain: at any strict point one
can increase all scales by a factor slightly above one, still keep all full
complements positive, and increase every `B alpha` since each is positive.
Thus a closed optimum **equal** to one half would not certify the target;
strict feasibility of the half-height target is equivalent to that closed
optimum being **greater** than one half. We do not compute or claim this
optimum. An exact positive primal witness suffices here.

## 4. The common-scale family fails for the fixed prefix

Exact enumeration of this fixed layer gives

\[
 M=\frac{7657469}{2371842},\qquad
 b=\frac{256}{1185921},\qquad
 \inf\max_j\tau_j=\frac{7656957}{7657469}>\frac12.
 \tag{11}
\]

Both extrema occur at the four-antichain; its records do not change these
values. A smaller analytic obstruction establishes the rejection without
trusting the enumerated maximum. At that antichain, only the empty ideal
preserves height, and (4) gives

\[
 u_{A_4}(\varnothing)=\frac{e^4a^4}{d^6}
                    =\frac{256}{1185921}.
 \tag{12}
\]

The half-height target would need `epsilon>=1185921/512`. But the four-chain
has a unique maximum; its proper ideals are precisely all ideals of the
remaining three-chain. Formula (4) gives their complete old row, whose sum
is one. Its positive full complement therefore requires `epsilon<1`.
These requirements conflict. This is a common-scale obstruction only:
antichain-empty and chain slots need not share one ratio component.

## 5. Exact component-scale witness

[CERTIFICATE.json](CERTIFICATE.json) supplies a rational vector for all
109 components. It specifies default `alpha=1/8`, explicit overrides and
the complete ordered list of component roots. Nothing is optimized or
refitted when the certificate is checked.

The component convention is reproducible. For each local slot, minimize
lexicographically over all 24 carrier permutations the triple

\[
 \left(\sum_{(v,w)\in\prec}2^{4\pi(v)+\pi(w)},\quad
       \sum_{v\in S}2^{\pi(v)},\quad
       \sum_{v\in S:r_v=1}2^{\pi(v)}\right).
 \tag{13}
\]

Sort the ratio-graph components by their minimum such key. Certificate
indices are zero-based; its root list must match the reconstructed list
exactly. All old and newborn records, including zero marks, remain in the
graph construction. This is not an undocumented traversal ordering.

The standalone [checker](check.py) reconstructs the chosen seed and
maximal-deletion potentials using exact `Fraction` arithmetic. It builds
all proper slots and raw ratio equations, verifies potential agreement on
the exact quotient and every raw edge, constructs components, and sums the
complete labeled rows. It checks every certificate coefficient is positive,
every full complement is positive and every row satisfies the target.
Independently within the checker it appends each possible birth, recomputes
height and sums the actual height-increasing probabilities; it does not
substitute full-birth probability for `tau`.

The certified margins are

\[
 \min_c\alpha_c=\frac18,\qquad
 \min_j q_j(P_j)=\frac{33901019}{474368400}>0,
\]
\[
 \max_j\tau_j=\frac{14082809}{29648025}<\frac{19}{40},\qquad
 \min_{j,S\in J(P_j)}q_j(S)=\frac9{681472}>0.
 \tag{14}
\]

The last minimum is over ideal probabilities; each newborn-mark-resolved
probability is half of that. No closed-boundary solution is admitted.
All 7,616 raw diamonds also pass the scaled full-map multiplier check:
each route multiplies the entire arbitrary retained `D` by the same product
of two `q/2` factors. This is an equality of the full scalar maps, not an
equality tested only after normalizing or diagonalizing a chosen payload.

## 6. What this finite decision does and does not settle

Common-scale failure and component-scale success both concern exactly this
seed and this new layer. A worst-row obstruction at one level cannot rule
out a typical asymptotic regime; the obstructing rows might be rare. Here the
stronger all-row half-height target is feasible at size four, but that alone
does not show that such rows dominate or that the bound persists at size five.

Nor would a persistent upper bound below one half by itself establish
`H(P_N)/N -> 0`: a positive constant height drift can still yield linear
growth. Conversely suppressing full births alone is insufficient because
proper precursors can contain a longest chain. The relevant predictable
quantity is total `tau`, as used throughout this note.

Changing the size-four scales changes the prefix used to compute later
potentials. They must be recomputed from that changed law; later RI-39 tables
cannot be reused unchanged. RI-38 guarantees **some** further positive
extension of this accepted finite prefix, not preservation of the desired
height bound and not an asymptotic geometric regime.

**Smallest next question, not started here:** with this exact finite prefix
held fixed, what condition on the sequence of actual conditional height
drifts would be sufficient and necessary for sublinear height, and which part
would require an additional all-size component-scale selection theorem?
A bounded analytic drift criterion should precede further layer enumeration.
It must separate pathwise/typical cumulative drift from uniform worst-row
control and not assume the selector whose existence is at issue. No successor
simulator, higher-size search or new nonpassive model is opened by this note.

## 7. Evidence, reproducibility and handoff

The common-scale algebra, component characterization, strict-domain arguments
and small obstruction are analytic. The component result is a finite exact
rational certificate, not a floating solver conclusion or an all-size proof.

For discovery only, an external temporary environment used SciPy 1.18.1 /
NumPy 2.5.3 and HiGHS on the finite matrices. A floating positive-slack candidate
was multiplied by `21/20` and rounded upward to multiples of `1/1000`, then
expressed as rational strings. These operations were a way to find the
witness; their floating inputs are not proof premises. Both positive full
complements and height inequalities were recomputed exactly afterward.
No solver package or discovery script is a repository dependency.

The new checker uses only the Python standard library, imports no project
source, writes no files and does not run predecessor suites. It reads only
the neighboring certificate. `--matrix` optionally emits its exact rational
matrices for inspection; default mode verifies the frozen witness. Main
author executions used Python 3.14.0:

```sh
python3 -I -S -B docs/track_b/native_growth_height_normalization_v1/check.py
python3 -I -S -B -O docs/track_b/native_growth_height_normalization_v1/check.py
```

Both passed with identical reported results: 40 naturally labeled parents,
640 marked rows, 5,072 proper-ideal occurrences, 305 local quotient nodes,
109 components and 7,616 raw equations (238 all-zero, 1,280 equal-precursor,
1,536 loops). Every one of the 5,712 complete ideal slots was included in
the direct height/positivity check. The three negative controls rejected a
zero component, a zero full complement and an otherwise positive normalized
common-scale table that fails the height target. Explicit runtime checks,
not Python `assert`, retain verification under `-O`.

Earlier-prefix validity is inherited from accepted RI-36/RI-38; the 436
earlier diamonds are not replayed here. Locality and equivariance follow
structurally from the declared quotient and deletion formula, corroborated
by agreement of potential values at every shared quotient key. No separately
enumerated locality/permutation-comparison count is claimed. The full-map
checks compare arbitrary-`D` scalar multipliers in this passive class; they
do not execute a nonpassive instrument or a terminal-record transport test.
An additional normal/optimized stdout comparison on Python 3.14.0, Darwin
arm64, was byte-identical: 600 bytes, SHA-256
`d9cceb8a462564d01a0f5e4aded95f3e3ee5d50f4cd9623b20f1de16ba7fa706`.

Three internal read-only reviewers read the complete note and reported no
proof or scope blockers. Two also audited the complete checker/certificate;
one independently ran both stated commands and reproduced the results.
The third checked the analytic formulas and interpretation without regenerating
the certificate. The requested evidence-scope clarification is incorporated
above. These are internal reviews, not coordinator acceptance or empirical
evidence. All five distinct local Markdown targets exist; whitespace and
conflict-marker checks are clean. Final SHA-256 source identities accompany
the handoff. Coordinator adjudication and publication are separate from this
authorship. Only the
three files in this new reserved directory are authored; accepted sources,
coordinator records, measurement inputs and RET are unchanged. Root owns
all git/index/publication operations. Release this reservation at stable
handoff and stop the packet. Option B, Status M and the RET pause are unchanged.
