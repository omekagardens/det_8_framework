# QR-05L results: adversarial closure and stable refinement

6 September 2026. **Completed bounded investigative gate.**
Research base: the pushed QR-05K checkpoint `2f232c8`.

## Outcome

Pair-overlap summaries are not generally sufficient even for this unchanged
independent-thinning law. Two added supplied orders have identical complete
mean and pair tensors but different next-summary and full count laws.

The failure has a small exact repair on the expanded finite family:
split the one ambiguous pair class. This produces the coarsest strongly
closed refinement of B on the declared domain, while leaving every old
QR-05K class and quotient transition unchanged.

| Description | Classes | Complete next-description law |
|---|---:|:---:|
| Color-graded chain means D | 100 | No |
| Eligible-union chain pairs B | 109 | No |
| Stable refinement Q* of B | 110 | Yes |
| Fixed-anchored color-marked order | 142 | Yes |
| Complete labeled observation | 257 | Yes |

Actual memberships form a strict refinement chain from full record through
color order, Q*, B and D. Class counts are not storage costs or measured speedups.
Q* is coarsest among strongly closed partitions required to refine B on this
finite state/rate family, not among every possible predictor or encoding.

## A realized equal-moment, unequal-law counterexample

Append these height-two interior relations on the same six eligible IDs,
with fixed bottom 0 and top 7, the same public frame and the same odd/even rates:

```text
path6:       1<2, 1<4, 3<4, 3<6, 5<6
cycle4_edge: 1<4, 1<6, 3<4, 3<6, 2<5
```

The names refer to undirected comparability graphs; these explicit directions
define the supplied orders. Both full observations have N=(1,6,5,0), three
eligible vertices of each color and five mixed-color relations. They agree
in all 64 D and 256 B coefficient cells, so every two-color mean and covariance
polynomial agrees. In particular,

```text
E N1 = 3x + 3y
E N2 = 5xy
E[N2²] = 5xy + 4x²y + 4xy² + 12x²y².
```

Only cycle4_edge can produce the four-cycle observation on {1,3,4,6}.
Its probability, both as a next-B event and as the count-law atom
N=(1,4,4,0), is

```text
path6:       0
cycle4_edge: x²(1-x)y²(1-y).
```

At half rates this is 0 versus 1/64; at (1/3,2/3), 0 versus 8/729.
This is a realized induced-order counterexample inside the supplied model,
not merely an abstract pair of probability distributions and not empirical
data. It cannot be repaired by treating the two predicted laws as equal
because their means/covariances match.

The artifact keeps both complete count-law polynomials. Full path/cycle
states are IDs 232/256; the selected four-cycle target is state 242,
original B class 106, from cycle mask45. The automatically first B collision
has the opposite orientation: target B class 11 has the same nonzero
polynomial from path and zero from cycle. Both witnesses remain explicit.

## Exact recursive repair

Start Q0=B and repeat the declared rule

```text
Q_(r+1)(S) = class of [Q_r(S), complete polynomial row to Q_r classes].
```

Keeping the previous class in the key prevents an improper merge of required
B distinctions. Here the recorded sequence is

```text
round 0: 109 classes, not closed
round 1: 110 classes, closed.
```

Only B class 105, containing states [232,256], splits. Path retains class105;
cycle moves to new class109. The retained separation uses the first differing
current target class11. Every other state-class assignment is unchanged.

Each refinement step and separation is rechecked; stopping requires exact
state-class-vector stability, not just equal class counts. The final quotient
is defined only after all member rows agree. Its 1,154 transition atoms
satisfy coefficientwise fresh-thinning composition, with 295,424 four-variable
cells checked over 6,205 two-hop structural paths.

Why this is the coarsest closed B-refinement: any other closed refinement R
starts finer than B. Every current block is a union of R blocks; states in
one R block have equal probabilities into each such union. Therefore no
refinement step can split an R block. At termination every admissible R
refines Q*, which is itself closed. The [protocol](README.md) states the full
induction and finite termination argument.

The result combines that ordinary mathematical proof with exact finite
construction checks. It is not an exhaustive search over every partition,
a Lean proof, a trace-minimality theorem or a minimum-memory implementation.
It sits in the standard finite-aggregation setting discussed by
[Buchholz (1994)](https://doi.org/10.2307/3215235); no new physical law is used.

Q* still forgets some color-marked-order distinctions. For example, states9/18
share stable class6 but have different named-color order codes; their complete
stable pushed rows agree. This is a concrete retained compression witness,
not a claim that all lost order information is physically irrelevant.

## QR-05K survives as an exact restriction

The expanded domain has six profiles, two public frames, 352 source/mask
aliases and 257 unique observations. The original 188 observations form a
subset-closed prefix; 69 observations are new. Appending sources contributes
47 new aliases to old states, which remain visible but do not become weights.

After filtering aliases to the original four sources, every old state record,
profile map, frame, D/B/color feature, fine transition, basic class assignment
and pushed polynomial row matches K. Actual pulled-back partitions and old
expected-update rows match as well.

The stable quotient restricts to K's original 91-class B quotient by actual
memberships and an explicit class map. Old fine rows stay in the old state
domain, the old coarse class image is closed, and every quotient coefficient
and its composition certificate matches. No old history mass or hidden source
name enters the new summary.

K's bounded success is therefore not retracted. L demonstrates why its
finite-family qualifier mattered and supplies a repair on the expanded family.
Earlier J and geometric/quantum bridge evidence remain pinned and unchanged.

## Joint observation sequences

A two-step original-B trace records both B(U) and B(V). It is not just the
terminal B(V) distribution at product retention rates.

For every state at four ordered stage-rate pairs, the complete fine-path
trace law equals the projection of the repaired quotient law. The artifact
retains all 1,028 state/rate-pair rows and 42,388 structural trace atoms,
including atoms with zero probability at selected boundary rates.

All-rate finite-trace preservation follows from the verified strong quotient
by inserting the original-B observation selectors between successive kernels.
The four rate-pair checks are additional exact evaluation checks, not an
interpolation proof for arbitrary trace polynomials.

No refinement-round label is interpreted as an earliest distinguishing
horizon. The retained adversary already differs after one observation.
Fresh independent thinning composes; reused coins remain an explicitly
out-of-premise diagnostic. Neither thinning nor its quotient is physical
time, event growth or gravitational evolution.

## Verification and evidence

The primary constructs observed chain pairs, expands binomial kernels and
refines coefficient rows synchronously. The reference uses source-count-law
moments, exact interpolation and an independent live-block splitter worklist;
its independently emitted grid-based round certificate must agree with that
worklist. Separate utilities are carried from each route's own K lineage;
no earlier executor or other route is imported at runtime.

The tests additionally construct stable classes bottom-up from proper
induced successors. This third construction checks the result using the
decreasing-size structure of thinning.

| Quantity | Total |
|---|---:|
| Fine / state-basic-summary atoms | 3,464 / 10,410 |
| Fine plus basic-pushed coefficient cells | 221,984 |
| D / B feature cells | 16,448 / 65,792 |
| Expected-update coefficient cells | 1,315,840 |
| Retained refinement rounds / strict splits | 2 / 1 |
| Round pushed atoms / coefficient cells | 4,534 / 72,544 |
| Basic closed quotient atoms | 5,038 |
| Stable quotient atoms | 1,154 |
| Basic / stable semigroup cells | 1,289,728 / 295,424 |
| All semigroup cells | 1,585,152 |
| Rational audit points | 22 |
| Joint two-step trace rows / atoms | 1,028 / 42,388 |
| Matched K states / original aliases | 188 / 224 |
| Largest retained exact component | 59 bits |

Validation passed:

- 109 tests normally (55.28s) and 109 with `-O` (55.43s).
  Optimized pytest emits its standard warning about non-test assertions;
  the executors and runner use explicit checks, and optimized subprocess
  tests verify output agreement and rejection without relying on assertions.
- Ruff check and format verification passed.
- Create-only capture: 5,463,084 bytes; suite time 15.35531462499057s.
- Exact unchanged replay: normal 15.487524124997435s,
  optimized 15.554344459000276s.
- Independent JSON-only postflight: 3,731,479 explicit checks in 4.39s,
  with no executor, runner or test imports. It rechecked all state/alias
  and observed-feature identities, fine/pushed rows, expected updates,
  basic closure fibers, refinement rounds/separation, all 1,585,152
  composition cells, actual K state/class/quotient restriction and all
  1,028 trace rows/42,388 atoms. Source/prior ledgers and artifact bytes
  were unchanged.
- A supplemental 7,777 JSON-only checks covered the remaining rate/corner,
  control, rejection and complete-counter inventories: 3,739,256 checks
  in total, with the artifact still unchanged.

The tests include early stopping, extra stable rounds, improper merges,
missing/altered separation witnesses, fabricated quotients for failed D/B,
coefficient and class-ID corruption, bool/int substitutions, source identity
and old-domain quotient tampering. Both routes reject all 19 malformed runner
fixtures; additional native-subclass and optimized guards are tested.

Artifact SHA-256:
`0df1b47e1219191783a9ec229540fd433e2129121ce2c5f6e5262e5f3c00e0ff`.

All six source identities and all 16 prior artifact identities are frozen.
Canonical [results.json](results.json) was created once by exclusive creation
and was not overwritten. Exact replays are read-only; lifecycle mutations
use temporary stub evidence. Human reports and the roadmap are outside the
frozen source ledger. Runtime measurements are descriptive, not benchmarks.
The frozen protocol retains one harmless extra blank line at EOF, reported
by `git diff --check`; it was not normalized after capture.

## Applicable value and next step

This is a usable diagnostic and repair principle for a relational summary:
identify an actual future observation that it loses, then retain only the
extra distinctions required for the declared recursive prediction contract.
Equal overlap statistics need not encode all relevant relational structure.

For Track B, it provides a consistency criterion for coarse descriptions.
It does not identify the classes with geometry, infer a metric or field
equation, change quantum observables, or turn a supplied sampling law into
a physical law. Units, apparatus noise, calibration and physical dynamics
still need separate definitions. RET/core and unrelated checkout work were
untouched; no SDK integration or dependency installation occurred.

**Proposed QR-05M: constructive observable realization.** Test whether the
single new distinction can be represented by an explicit observed motif
count rather than only a finite partition table. Candidate M(S): the number
of induced four-eligible-vertex K2,2 orders with two vertices of each named
color, no same-color comparisons and all four comparisons from one color
layer to the other (either orientation).

The candidate uses only observed relations and eligible marks, not a profile,
state ID, class ID or transition-table lookup. Compare the actual memberships
of (frame,B,M) with Q* across the same domain; do not assume equivalence.
Separately derive and verify E[M(T)|S]=x²y²M(S) by motif survival, keeping that
mean identity distinct from full-law closure.

If it matches, this replaces the lookup-only split with a readable structural
observable. It would not prove sufficiency on unseen orders or arbitrary
acquisition laws, nor minimum storage cost. This candidate is proposed only,
outside L's captured certificate. Lean installation, RET integration and the
apparatus-to-physics interface remain separate gates.
