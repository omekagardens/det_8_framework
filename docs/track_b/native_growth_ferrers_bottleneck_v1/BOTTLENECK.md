# RI-54 — rectangle bottleneck and an infeasible first-face capacity gate

24 September 2026 UTC. **Conditional analytic obstruction and exact finite
certificate; independent coordinator adjudication accepted.** The accepted
RI-52 one-step result remains correct. Its sparse boundary witness, however,
cannot support high two-step Ferrers survival under any later completion.
More strongly, the entire fixed-prefix first-layer system fails the necessary
capacity test `b_B>=1/2` on every marked `(3,2)` parent. Exact pointwise duals
give smaller ceilings, and a different boundary vector attains those ceilings.

This rejects arbitrarily small departure at both consecutive layers under
the fixed prefix. It does not reject every Ferrers construction under other
premises, prove optimal two-step survival, or replace the model with a
zero-probability law. No later-layer table or repair mechanism is constructed.

## 1. Fixed premises and probability meanings

Preserve the complete [RI-41 prefix](../native_growth_height_normalization_v1/NORMALIZATION.md)
and the [RI-38 extension model](../native_joint_growth_extension_criterion_v1/CRITERION.md).
All ideal/bit branches of an admitted law are positive. The ideal weight
`q_(P,r)(S)` reads only precursor marks `r|S`, may read the whole unmarked
parent order, and is equivariant under marked-parent isomorphisms. Newborn
bits are fair. The complete passive maps are `q(S)D/2`; no informative
quantum coupling or new amplitude rule is added.

The [RI-52 gate](../native_growth_ferrers_gate_v1/GATE.md) fixes the ten
marked-local target components, their potentials, all labeled multiplicities
and the first-free-layer matrix. A nonnegative boundary vector is an auxiliary
relaxation; strict interior mixing is required for an admitted law.

Fix a five-event parent `B=(3,2)` with predecessor masks
`(0,1,3,1,11)` and a full inherited record `r`. Set

\[
 S_0=7,\quad S_1=9,\qquad
 b_r=q_{B,r}(S_0)+q_{B,r}(S_1),\qquad
 f_r=q_{B,r}(B).
 \tag{1}
\]

These are the two good proper Ferrers slots and the good full slot.
All other first births leave the family. The full birth gives
`R=B+x_B=(3,3)`, with masks `(0,1,3,1,11,31)`.
For either bit `u` on `x`, let `g_(r,u)` be the total probability that
the next birth from `(R,r+u)` is Ferrers, summing its newborn bit.

All statements below are conditional on this specified starting `(B,r)`.
Two-step survival sums over first branches and both fair newborn bits; it
is not the conditional survival probability from R alone, and it is not an
unconditional probability from the empty history. No weighting over different
starting parents or record assignments is substituted for a pointwise claim.

## 2. Intrinsic corner classification and the non-chain rectangle lemma

The following classification uses order relations, not a supplied geometry.
For any non-chain Ferrers down-set, the vertices whose principal ideals
are chains form two coordinate-axis chains joined at the unique minimum.
After removing that minimum, these are precisely two nonempty incomparable
chains. They are therefore intrinsic, up to exchanging them. Each vertex
is uniquely determined by its two axis initial segments below it. An order
isomorphism between such diagrams consequently preserves the diagram up
to axis exchange; it cannot create extra labeled corner ideals.

Let R be a product of chains of lengths `a,b>=2`, and let B be R with its
unique maximum removed. In a Ferrers realization B has row lengths
`(b,...,b,b-1)`. Its only addable cells are the two outer-axis corners and
the missing rectangle maximum. The first two have the distinct axis ideals
as precursors; the third has all of B as its precursor. These are exactly
two good proper labeled slots and one good full slot.

For R itself the only addable cells are the two outer-axis corners, again
with those two distinct proper axis ideals. There is no good full slot.
To justify using these diagram corners intrinsically, delete the newborn
maximum from any proposed Ferrers child. The remaining down-set must be
isomorphic to B or R, so the preceding axis characterization identifies it
with the declared diagram up to transpose. A non-chain rectangle has no
further addable cell. In a square the two outer ideals are still distinct
labeled subsets even though exchanging axes is an automorphism.

For `a=2,b=3`, this gives exactly masks 7 and 9 in both B and R.
The corresponding R children are `(4,3)` and `(3,3,1)`. No seven-event
layer is enumerated to establish this classification. The lemma deliberately
excludes chains: a chain has a good full extension and does not have the
two nonempty axis components used in the proof.

## 3. The rectangle bottleneck, with marks and transported labels

Keep old vertices labeled as B, and append each proposed new vertex last.
For `i=0,1`, let `C_i=B+y_(S_i)` be the competing proper first child.
The old set B is an ideal of C_i, but excludes `y`. In the common child
of the two independent births, `x` has past B and `y` has past `S_i`;
the two possible birth orders differ only by transporting the last labels.
The complete two-birth diamond reduces, since both branch maps are scalar
multiples of `D/4`, to

\[
 f_r\,q_{R,r+u}(S_i)
 =q_{B,r}(S_i)\,q_{C_i,r+v}(B)
 \qquad(u,v\in\{0,1\}).
 \tag{2}
\]

Equivalently, equality for all D implies this scalar identity. No diagonal
or normalized-only payload reduction is being made. The second factor on
the right reads B's marks and excludes `v`. The left second factor reads
only `S_i` and excludes `u`. Thus `g_(r,u)` is independent of `u`; write it
as `g_r`. These record permissions, rather than a mean over unequal mark
classes, justify removing the newborn-bit labels. Each companion probability
is at most one (strictly below one in an admitted strict row), so

\[
 f_r g_r
 =\sum_{i=0}^1 q_{B,r}(S_i)q_{C_i,r}(B)
 \leq b_r.
 \tag{3}
\]

Each ideal occurs once. An axis symmetry does not divide or double its
labeled probability. The same proof applies to every non-chain rectangle
and its maximum-deleted predecessor from section 2, using its two axis ideals.
It needs only coherent diamonds and normalized nonnegative rows; strict
positivity strengthens (3) to a strict inequality.

Let `H_r` be the probability that both the sixth and seventh orders are
Ferrers, conditional on `(B,r)`. If `h_(i,v)<=1` is the next-step survival
probability from the proper first child with newborn bit `v`, then

\[
 H_r=\sum_i q_{B,r}(S_i)\frac{h_{i,0}+h_{i,1}}2
          +f_r\frac{g_{r,0}+g_{r,1}}2
 \leq b_r+f_rg_r\leq2b_r.
 \tag{4}
\]

Bad first branches contribute nothing. Moreover a non-Ferrers child cannot
later become an exact Ferrers whole order: committed prefixes persist as
order ideals and the family is ideal-closed. The factors of one half in (4)
account for fair newborn marks explicitly. The expression is a probability
from B, not `g_r`; one must not drop the factor `f_r`.

For strict laws `f_r,b_r>0`, every companion in (3) is below one, and hence
`H_r<2b_r`. The upper bound need not be sharp as a survival bound. It can
exceed one for other parameter choices, where the trivial bound also applies.

### Boundary case and the RI-52 sparse witness

If `f_r=0` in an auxiliary nonnegative boundary, (3) is still valid, but
it cannot be divided by `f_r` and supplies no bound on `g_r`. The full
branch is then not reached from B; the R row is a counterfactual kernel row.
This boundary case is not admitted as a strict law.

RI-52's sparse witness instead has `b_r=0,f_r=1` for every B marking.
Any normalized nonnegative later rows satisfying (2) must then have `g_r=0`.
Now mix that witness with the same strict RI-38 interior extension used in
RI-52, whose total proper mass is below one half in every row. For mixture
parameter `0<t<1`,

\[
 b_r(t)=t b_r^*<t/2,\qquad H_r(t)<t.
 \tag{5}
\]

This holds under **every** admissible later completion, even though RI-52
gives worst first-layer departure at most t. It rejects this route from
the particular sparse witness to high two-step survival, without by itself
rejecting other points on the first-layer face.

## 4. Prospective error bound and the necessary capacity gate

Suppose B's departure probability is at most `epsilon_5`, and its full
rectangle child's departure is at most `epsilon_6`, for the specified
records. Assume `0<=epsilon_i<=1`; uniform layer bounds imply these particular
ones. Then

\[
 b_r+f_r\geq1-\epsilon_5,\qquad
 f_r(1-\epsilon_6)\leq f_rg_r\leq b_r.
\]

Multiplying the first inequality by `1-epsilon_6` and applying the second
gives the exact necessary condition

\[
 b_r\geq
 \frac{(1-\epsilon_5)(1-\epsilon_6)}{2-\epsilon_6}.
 \tag{6}
\]

The denominator lies in `[1,2]`. No division by `f_r` or by
`1-epsilon_6` occurs. If either error equals one the right side is zero;
at `epsilon_6=0` it equals `(1-epsilon_5)/2`. Along any sequence with both
errors for a specified marked B row tending to zero, that row must satisfy
`liminf b_r>=1/2`. Requiring those bounds for every marking gives the
condition on every row. This does not assert `b_r>=1/2` at arbitrary fixed
positive errors.

For the prospective uniform requirement, suppose the first-layer departure
bound tends to zero over **all** marked Ferrers parents, and the relevant
second-layer bounds tend to zero for every marked B-to-R state. RI-52's
finite compactness argument then gives a limiting nonnegative first-layer
vector satisfying its A/E equalities, C/B caps, and `b_r>=1/2` on all B
rows. The pointwise B/R assumptions alone would not imply A/E equalities.
This augmented system is only a necessary escape gate, not a sufficient
two-layer construction.

## 5. Exact per-mark dual certificate: the gate is infeasible

Keep RI-52's canonical component scales `alpha_0,...,alpha_9` and all
128 raw marked rows. Let `rho` be the root bit and `sigma` the other bit
in the common two-chain precursor for child `(4,2)`. Define
`z_(rho,sigma)=alpha_(4+rho+2 sigma)`. The exact matrix gives these matching
row masses; other full-record completions do not change their values:

| Root bit | A target mass `a` | E target mass `e` | B target mass `b` |
|---|---|---|---|
| 0 | `(81/1100) alpha_0+(19/1760) alpha_2+(1677/5000) z_(0,sigma)` | `(41/176) alpha_2+(719433/5000000) alpha_8` | `(41/352) z_(0,sigma)+(741/160000) alpha_8` |
| 1 | `(3231/44000) alpha_1+(7/1760) alpha_3+(8869/11000) z_(1,sigma)` | `(41/176) alpha_3+(1605289/2200000) alpha_9` | `(41/352) z_(1,sigma)+(1267/352000) alpha_9` |

Both values of sigma are retained; in particular components 4 and 6, or
5 and 7, are not replaced by an average. E's coefficient `41/176` includes
its two distinct `(4,1,1)` ideals. B's `(3,2,1)` coefficient counts its
one labeled ideal, not that child's two deletion roles.

Matching uses the actual canonical marked-local keys, including transport
of the whole parent, precursor and its retained bits. For B's row-major
record mask r, the checker finds A rows containing the same `(4,2)` component
and E rows containing the same `(3,2,1)` component, then chooses their least
record masks: `r&3` and `r&1` respectively. There are eight matching A
completions and sixteen E completions for each B row. These are normalized
rows of the same complete law, so their caps apply; different whole marked
states are not identified. All 32 B markings and both sigma values are kept.

For root bit zero the exact coefficient identity is

\[
 \frac{25625}{73788}a+\frac{2375}{73788}e-b
 =\frac{27675}{1082224}\alpha_0
   +\frac{97375}{8657792}\alpha_2\geq0.
 \tag{7}
\]

For root bit one it is

\[
 \frac{5125}{35476}a+\frac{25}{5068}e-b
 =\frac{132471}{12487552}\alpha_1
   +\frac{3075}{1783936}\alpha_3\geq0.
 \tag{8}
\]

Every admissible row has `a,e<=1`, even away from the zero-departure face.
Consequently the **pointwise** capacity ceilings are

\[
 b_r\leq c_\rho,\qquad
 c_0=\frac{7000}{18447}<\frac12,\quad
 c_1=\frac{1325}{8869}<\frac12.
 \tag{9}
\]

The contradictions to the proposed half-capacity cut are respectively
`4447/36894` and `6219/17738`. These rational dual combinations use only
nonnegative scales and matching A/E row caps. Thus they prove more than
infeasibility on the equality face: the ceilings hold for every first-layer
extension of the fixed prefix. In strict laws the ceilings are strict,
because A/E have positive non-target/full mass (and all scales are positive).
The checker verifies the dual residual in all ten columns for each of the
32 raw marked B rows, not merely a representative or a marked average.

### Sharp capacity ceilings, not sharp survival probabilities

The nonnegative boundary vector

\[
 \alpha=\left(0,0,0,0,
 \frac{5000}{1677},\frac{11000}{8869},
 \frac{5000}{1677},\frac{11000}{8869},
 \frac{5000000}{719433},\frac{2200000}{1605289}\right)
 \tag{10}
\]

satisfies every original RI-52 first-layer constraint. It gives C target
mass zero, A/E mass one, and every B mass exactly its corresponding ceiling
in (9). All other proper components can be set to zero, using RI-52's
terminal-child closure argument. This shows both capacity ceilings are
simultaneously sharp on the boundary. Mixing with a strict interior extension
approaches them through admitted first-layer laws, but does not attain them.
It also shows why the whole face was not rejected merely from RI-52's sparse
point: (10) is a different point with larger, yet still insufficient, B capacity.

Combining (4) and (9), every strict completion has conditional two-step
survival from a root-bit-one B state below `2650/8869`. Its two-step failure
probability is therefore above `6219/8869`. This is a certified bound, not
a proved optimal survival value. No unconditional-from-empty numerical
probability follows without also accounting for the starting-state weight.

Combining (6) and (9) for root bit one gives

\[
 (1-\epsilon_5)(1-\epsilon_6)
 \leq\frac{1325}{8869}(2-\epsilon_6).
 \tag{11}
\]

In the zero-first-departure boundary or a limit with `epsilon_5->0`, the
second error must be at least `6219/7544` (a liminf statement for sequences).
At `epsilon_6=0`, the first error must be at least `6219/8869`. Exact zeros
are not asserted to occur in a strict law. In particular both errors cannot
converge to zero. This is the quantified reason the augmented gate is rejected.

## 6. Bounded checker, provenance and review evidence

The [certificate](CERTIFICATE.json) stores exact dual weights, ceilings and
the sharp boundary vector. The [checker](check.py) uses standard-library
fractions and the SHA-pinned accepted RI-52 source as an explicit read-only
dependency. It loads helper definitions without invoking that source's main,
reconstructs only the same prefix and first-layer marked target matrix, and
checks the accepted RI-52 certificate before this new certificate.

No full size-five or size-six order layer is enumerated. No R successor row
or seven-event table is evaluated. The rectangle statements are analytic
theorems; checker coverage is the complete already-fixed first-layer matrix,
not an empirical or exhaustive later-layer test. Matrix reconstruction retains
all marked-local components and labeled slots. This is reuse of accepted
source, not an independently reimplemented matrix generator.

The two dependency files are verified before their use:

| Accepted RI-52 dependency | SHA-256 |
|---|---|
| `check.py` | `822d49b766a2ef2862f289f9e4abb4a262cfafcf58ac3ff4c34c044e75f6c654` |
| `CERTIFICATE.json` | `33dd1a9d3659b92d02009185bc1e681309380c03c08fc83a8cb6555198203d6b` |

The reconstructed root manifest remains
`b460e8c6a659513f824a619c62ec9d1dfa5c6c847b69c3c7af13325b96948581`;
the canonical marked-row matrix remains
`bd5bcb1fe255e1018c13c9b3a71764516ecde06693c066dc27a8e73913bcfe04`.
The accepted baseline certificate is rechecked, including its prefix coverage
of 707 marked rows, 6065 slots, 436 lower diamonds and 7616 RI-41 ratios.
The new dual check covers every one of 32 B rows (16 per root bit) in all
ten columns: 64 residual entries are positive and 256 are zero. The sharp
boundary is checked on all 128 raw marked rows, all 116 canonical rows,
and all 768 target scalar diamonds. Every B row attains its certified cap.

Two new in-memory controls must fail for their exact intended reasons.
Zeroing the root-zero A multiplier, while updating its declared cap to keep
the weight-sum identity, yields a negative dual coefficient. Doubling primal
component 4 exceeds a row cap. Neither control writes or changes a file;
the accepted RI-52 baseline controls are also rerun by its verifier.

Discovery was separate: a floating linear-program query against the accepted
RI-52 matrix reported the augmented system infeasible. The displayed duals
and boundary vector were then derived from exact row coefficients and checked
with fractions. No numerical solver verdict is used for acceptance. The
external discovery environment was CPython 3.14.0, NumPy 2.5.3, SciPy 1.18.1.

Main execution used CPython 3.14.0 with `-I -S -B`, normally and with `-O`.
Both runs exited zero with empty stderr in approximately 0.240 and 0.241
seconds. Their stdout was byte-identical: 1301 bytes, SHA-256
`ce50217fea43e06cf9605d2b71906c539a2e8759bb56d585b473e92903aa738f`.
The author independently reproduced these outputs in both modes.

An analytic reviewer read the complete note, proved the intrinsic corner
classification and marked bottleneck, and independently reconstructed the
new active matrix coefficients and exact dual identities. A separate
Fraction-only audit of the accepted matrix verified all canonical rows of
the sharp boundary and all 32 per-mark duals without using the new checker.
That separate reviewer then read every line of the new checker and certificate
and the complete note, and replayed normal and optimized modes with the same
interpreter and isolation flags. Both runs exited zero with empty stderr in
approximately 0.242 and 0.245 seconds and reproduced the identical 1301-byte
stdout and hash above. The checker author also cross-checked note/certificate
alignment. A review clarification makes the uniform first-layer premise of
the A/E compactness argument explicit; the pointwise bounds need no such
uniformity. No mathematical or source blocker remained. Coordinator
adjudication is separate and recorded in the opening status.

## 7. Disposition and halt

The assigned first-face capacity gate is **rejected**. The earlier one-step
Ferrers admission theorem remains accepted, but its fixed-prefix construction
cannot have arbitrarily small departure at both of these consecutive layers.
The general rectangle bottleneck is an internal conditional theorem, not a
law selecting any shape distribution.

No all-size Ferrers law, near-square concentration, alternative seed, defect
or core-tail repair, Plancherel/uniform-corner rule, weak-zero admitted law,
metric, informative quantum coupling, clock, source or gravity claim is made.
Option B and metric-as-record Status M remain unchanged; RET remains paused.
Only `BOTTLENECK.md`, `check.py`, and `CERTIFICATE.json` in this new directory
are authored. Accepted research and coordinator/measurement files remain
untouched. The coordinator owns git/index/publication. Stop at the stable
handoff for independent adjudication; no successor is started here.
