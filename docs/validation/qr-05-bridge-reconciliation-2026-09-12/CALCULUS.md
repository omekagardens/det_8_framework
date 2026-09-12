# Reconciled finite measurement-channel calculus

12 September 2026. Prospective contract for a new local verification, not
adoption of the concurrent branch's gate-completion labels. The motivating
source is `qr-05-bridge` commit
`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`, especially CY/DO. This calculus
requires no DET ontology, apparatus, stochastic model or physical law.

## One common world class

Fix a nonempty finite set W. Every channel O_c:W→Y_c and every target
τ_j:W→T_j is defined on this SAME W. For selected channels S let O_S be
their tuple, and let τ be the joint target tuple. Define

`u ~_S v iff O_c(u)=O_c(v) for every c∈S`.

The target is identifiable exactly when it is constant on every ~_S
class, equivalently when a function f exists with τ=f∘O_S on W.
For each pair with τ(u)≠τ(v), define its separator set

`D_uv={c: O_c(u)≠O_c(v)}`.

Then S identifies τ iff it hits every D_uv. Proof: an unhit pair is an
equal-observation/different-target obstruction; conversely, if every such
pair is hit, no observation class contains different targets. This is a
general finite-set theorem, independently testable by partition and
pair-separator algorithms.

Consequences:

- Adding channels refines the partition and cannot destroy identification
  on the unchanged W and target. It need not improve noise robustness or cost.
- Enlarging W can destroy identification. Slice-wise identification does
  not imply joint identification on the full world class.
- A deterministic function of existing observations cannot split their
  equal-observation classes. This is relative to those channels, not every
  conceivable instrument or reference.
- Inclusion-minimal identifying sets can have different sizes. The
  minimum cardinality and all inclusion-minimal sets are distinct outputs.
- A constant target is identified by no channels. If an empty D_uv exists,
  even the full declared channel set cannot identify the target.
- An observation explicitly equal to the scale target is a perfect injected
  anchor oracle. Its availability/calibration is not proved by this table.

## Fixed verification domain and wire

[protocol.json](protocol.json) fixes five packets and 27 channel subsets:

1. Four binary (a,b) worlds with channels a,b,a XOR b and joint target (a,b).
   The three two-channel sets identify; XOR alone does not. On either axis
   slice XOR identifies the varying coordinate, exposing DO's invalid
   slice-to-joint implication.
2. Four colour/scale worlds with colour, its duplicate, and external_scale.
   The latter is explicitly an oracle. Both colour-plus-anchor pairs are
   inclusion-minimal; all anchor-free sets remain blind to scale.
3. Two worlds, no channels, constant target: the empty set identifies.
4. Two different targets and one constant channel: nothing identifies.
5. The XOR world class with target a only: {a} and {b,xor} are both
   inclusion-minimal, but only {a} has minimum cardinality.

`calculus.py` is a pure bounded utility. Packet fields are exactly
`channels,rows`; each row has exactly `id,observations,target`. Channels and
IDs are unique plain strings; empty strings are permitted. All observation
and target coordinates are plain ints, not bools. Lists/dicts are plain,
all rows use the same channel count and positive target width, and W is
nonempty. Limits are eight channels, 64 worlds, eight target coordinates.
Selections contain unique declared channel names. No coercion, files,
network, physical truth extraction, or historical executor is admitted.

`partition(packet,selected)` returns blocks of IDs in first-world order.
`identifying(packet,selected)` checks joint target constancy.
`analyze(packet)` returns exactly `channels,partitions,
minimal_identifying_sets,minimum_size,minimum_identifying_sets,obstructions`.
Subsets are ordered by cardinality then input-channel index; each partition
row is `selected,blocks,identifying`. Minimum size is [] if impossible or
[k] otherwise. Obstructions retain EVERY different-target world pair in
input-pair order as `worlds,separators`, including empty separators.
Fresh output containers must not mutate/alias caller-owned inputs.

An independent test oracle uses pair separators/hitting sets rather than
the implementation's grouping route. It checks the entire native result,
all fixed subsets, refinement, explicit slice failure, input refusals,
constant/empty cases and minimal-versus-minimum distinctions. Extra inputs
are malformed/schema or named proof counterexamples, not a fitted fixture
bank. No random seeds or statistical success estimates enter this gate.

## Corrected calibration composition adopted from BW/BX

Keep the ideal probability point q, production population r, reference
population v, and finite-data estimates z distinct. They are not interchangeable.
For q,r,v in the nested probability triangle S, if

`||v-q||∞≤a` and `||r-v||∞≤d`, then `||r-q||∞≤min(1,a+d)`.

The cap 1 follows from the diameter of S. Missing reference validity means
no justified SMALL allowance, not an unbounded distance between probabilities.
A supplied upper bound a is not a lower bound on the actual error. The
triangle bound is sharp only in its declared feasible worst-case sense;
actual errors may be smaller, including by cancellation.

Reference/model validity still needs a substantive justification. Finite
sample agreement cannot by itself validate the ideal world or production
transfer, iid sampling, zero forbidden support, marks or loss handling.
Use an explicit validity event G_a for reference mapping and G_d for transfer.
If justified marginal failure bounds α,β_a,β_d apply to E,G_a,G_d under the
ACTUAL procedure, then with γ=min(1,α+β_a+β_d),

`P(E∩G_a∩G_d)≥1-γ`.

No independence is needed, even if events use the same data. Data reuse
requires rechecking validity after selection/adaptation; it does not
invalidate the union bound once those marginal bounds are established.
Simultaneously valid coordinate intervals can form a confidence rectangle;
intersecting with a known support constraint preserves true-point coverage.
One need not forbid rectangles merely because the support is a triangle.

For random allowances, either use a fixed passing envelope with its own
failure budget included in γ, or a declared acceptance event H that includes
the passing every-box separation check and all prior BV admissibility
premises. On H∩E∩G_a∩G_d (and the envelope-validity event when that route is
used), the prior BV theorem then gives a correct singleton. Thus

`P(H and correct singleton)≥max(0,P(H)-γ)`,
`P(correct singleton | H)≥max(0,1-γ/P(H))` when P(H)>0.

H with zero probability has no conditional guarantee. Repeated calibration
up to K rounds permits a summed validity budget when the required round-wise
bounds hold for the actual adaptive scheme; it does not automatically
control repeated production/selection errors. No unbounded repeat-until-pass
or multiplicative independence bound is inherited. There is no numerical
calibration allocation or device claim here.

BX's layer separation is retained as an evidence checklist: metrology,
event identification, marks/target, reference, sampling population, loss/
selection, and optional order/timebase. A status flag records a judgment
and evidence pointer; it does not mathematically prove a physical premise.
All such apparatus premises remain unsupplied in this checkout.

## Named mathematical regressions

These exact controls preserve lessons from the branch audit without importing
its numerical engines or interpreting synthetic controls as new physical data:

- Same-data dependent events on three equiprobable atoms: E={0,1}, G={1,2}
  have intersection 1/3, matching the union lower bound but below product 4/9.
- Three-chain weights w01=w12=1,w02=3: reverse triangle holds; max-plus
  closure of all pair weights gives 3, link-only closure gives 2. In general
  the all-pair closure is the least superadditive majorant. Link weights
  alone need not characterize every superadditive reconstruction.
- Local deterministic Bell correlations E=[[1,−1],[1,−1]] have full visibility
  amplitude 1 in each row but every CHSH sign combination is at most 2.
  Visibility alone is not a general CHSH violation test.
- For the branch's three-chain BINOMIAL-LAYER toy operator, diagonal −a and
  lower entries (3,−3,3), the inverse entry G20=3(a−3)/a³ cancels at a=3;
  at a=5 the antisymmetric entries Δ01=3/25 and Δ02=−6/125 have opposite
  signs. Causal support containment is not support equality or sign recovery.

These regressions are mathematical counterexamples to specific implications,
not repaired physical operators, apparatus calibration or new laws.

## Evidence discipline

Freeze this contract, protocol, calculus implementation, tests, driver and
the literal-hash-pinned BM evidence utility before the first new mathematical
run (six sources). The audit prose and branch source inventory are separate
publication records. The driver uses only BM bounded/strict/canonical/native
equality/deadline/exclusive-write helpers, never an earlier mathematical
executor. Capture and replay authenticate the complete freeze and source
identities before analysis, pass fresh inputs, and recheck bytes afterward.

Use 30-second analysis and 60-second suite limits. Run first capture, normal
and optimized tests and replays, then one alternate Python 3.11 replay.
No source tuning after first execution; retain failures if encountered.
This is local exact finite mathematics, not acceptance of the branch's 45
gate labels or a claim that its geometry/quantum tracks are physically closed.
