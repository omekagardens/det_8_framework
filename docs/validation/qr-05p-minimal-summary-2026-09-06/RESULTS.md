# QR-05P results: finite minimality and summary-consumer contract

6 September 2026. **Completed gate; H is the finite coarsest closed C-refinement.**
Research base: pushed QR-05O checkpoint `35831db`.

## Outcome

On the unchanged supplied O observation domain, the independently computed
coarsest strongly closed refinement R of C=(frame,B,M) has exactly the
same members as H=(frame,B,M,T). It is not merely a match of class counts.

Refinement starts from the old C, without consulting H or T to decide
splits. One strict round changes 166 classes to 167; the next round is
stable. Exactly one C fiber splits. The observed path count from O thus
realizes the required finite refinement.

| Partition | Classes | Role |
|---|---:|---|
| C=(frame,B,M) | 166 | Fixed baseline; not closed |
| R, computed from complete transition signatures | 167 | Coarsest closed C-refinement |
| H=(frame,B,M,T) | 167 | Same actual fibers as R |

This minimality is relative to preserving C, on this exact finite domain,
under this complete polynomial observation law. It is not unrestricted
predictive minimality, minimum storage, runtime optimality or universal
sufficiency. T is an interpretable way to encode the additional distinction;
this does not prove it is the only possible feature or representation.

## Why the coarseness statement follows

Each refinement key contains the old class and its complete probability
polynomials into every old class. Therefore a round can only split, never
merge. It stops only when those full laws agree throughout every fiber.

Let Q be any closed refinement of C. Initially Q refines C. If Q refines
a current partition, each current block is a union of Q blocks. Equal
probabilities into Q blocks imply equal probabilities into those unions,
so Q also refines the next partition. Induction makes Q refine the
terminal R. Terminal stability establishes closure of R itself.

The finite computation verifies these premises and every exact signature;
it does not enumerate all partitions or replace the argument with matching
cardinalities. The primary groups coefficient signatures. The reference
groups independently calculated probabilities at all 16 exact rational
nodes, using the explicit bidegree(3,3) bound. Tests also check a bottom-up
proper-successor construction. No Lean proof was installed or completed.

The single retained split is C class 147: states 612/625 separate into
new classes 147/151, with first differing target 11 and first distinguishing
rates (1/3,1/3). These are N's original star/path obstruction. IDs locate
the evidence; they do not enter the feature or refinement rule.

## A concrete application contract

The retained consumer payload contains only a bound model identifier,
class identifier convention, coarse transition rows and declared
class-measurable observable values. It needs no underlying order table
to evaluate a future summary distribution.

All four prespecified summary questions are measurable in R:

- Chain-count vector (N0,N1,N2,N3).
- K2,2 count M.
- Induced P4 count T.
- Joint vector (N0,N1,N2,N3,M,T).

For each, the full marginal polynomial from the quotient equals the
fine-process marginal from every member of every class. This is a
distributional check, not a comparison of just means or variances.

The bounded research helper
`predict(consumer, question, class_id, rates)` returns exact rational
probabilities, including structural outcomes that happen to have zero
probability at selected rates. It rejects undeclared and nonmeasurable
questions. The initial class must come from an observation actually in the
bound domain, and the caller must use verified pinned evidence. A matching
H key from an unseen order is not a membership certificate. Structural
payload validation is not authentication.

Fresh independent fixed-rate stages obey
Q_(x,y)Q_(a,b)=Q_(xa,yb). The retained certificate checks all four-variable
coefficients. This supplies repeated summary-level prediction under its
stated premises; it does not certify adaptive or correlated sampling,
physical time, event growth, or a general operational SDK.

## A supported rejection is part of the result

Consider the frame 0 observations with kept vertices {0,1,7} and {0,3,7},
both three-vertex chains. They have the same C, H and R class: one eligible
odd vertex between the fixed probes. In the full retained model they are
states 1/4, both class 1.

But the named relation1<7 is present in the first and absent in the second.
After thinning, its probabilities are x and 0, or 1/2 and 0 at half rates.
There is no summary-only answer to that named-vertex question without
additional information about the fine state. The consumer rejects it
instead of assigning an unstated prior over class members.

At the boundary x=0 these probabilities coincide. That does not make the
observable measurable over the full class/domain or license the globally
unsupported question. This example distinguishes a sufficient summary for
specified questions from reconstruction of a labeled record.

## What was checked and what was reused

P takes O's raw two-frame, 2,470-observation table as explicit input.
The input contains only state/frame IDs, kept vertices, past relations and
frame marks—not B/M/T, transition coefficients, class vectors or aliases.

Both executors rebuild chains, tensors, motifs and all 99,180 fine atoms.
Every reconstructed feature and actual C/H membership agrees with pinned O,
as does the canonical digest of the complete fine polynomial rows.
The source/alias universe is not independently regenerated in P.
O and its 19 earlier artifacts remain pinned; P does not replay O's entire
earlier expectation or restricted-domain certificate suite.

| Exact check | Total |
|---|---:|
| Supplied observations / fine atoms | 2,470 / 99,180 |
| Fine coefficient cells | 1,586,880 |
| Retained refinement rounds / strict rounds | 2 / 1 |
| Round-pushed atoms / coefficient cells | 97,536 / 1,560,576 |
| Separation witnesses | 1 |
| Terminal quotient atoms | 2,364 |
| Two-hop paths / composition coefficient cells | 15,571 / 605,184 |
| Consumer fine marginal coefficient cells | 997,584 |
| Class/rate/question prediction checks | 14,696 |
| Separate public prediction calls, both implementations | 528 |

The synthetic two-strict-round and old-class-preservation controls are
separate finite Markov examples, not additional certified O observations.
They check that the refinement algorithm neither hardcodes a one-round
answer nor silently merges distinctions it was required to preserve.

## Verification and artifact

Final validation passed:

- 204 tests normally (188.49s) and 204 optimized (188.60s), in isolated
  Python 3.11.6 with external bytecode caches and no pytest repository
  cache. The runs were concurrent, not application benchmarks.
  Optimized pytest emits its standard non-test-assertion warning;
  production guards explicitly raise and the optimized subprocess checks pass.
- Initial full runs had 191 passes and 13 failures in each mode, all caused
  by primary native-type rejection using TypeError where the shared public
  contract/tests expected ValueError. The exception contract was aligned,
  without changing mathematical output or weakening tests; the affected
  76-test selection and both complete final suites then passed.
- Pre-freeze review hardened rate syntax/length checks before rational
  construction, finite observable bounds, canonical representatives,
  payload atom limits and grouped-probability arithmetic limits.
  Supplementary normal/optimized checks verified that individually bounded
  atoms cannot silently produce an oversized grouped probability.
- Ruff check/format and six new-source whitespace checks passed before
  freeze. The sources and all 20 priors stayed unchanged across final tests.
- Exclusive create-only capture: 3,882,409 bytes, below the 64 MiB cap;
  suite time 70.31886045800638s.
- Read-only exact replay passed normally (72.03552970901364s) and optimized
  (71.83647808397654s), reproducing the complete P suite without changing
  any captured bytes.
- Independent JSON-only postflight passed 22,515,319 exact/native/identity
  checks in 16.725191542005632s, importing no executor, runner or test.
  It rebuilt the raw-order features, all fine atoms and their digest,
  C/H fibers, direct-product-grid refinement rounds and witnesses,
  terminal quotient/composition, all consumer marginals and the named
  singleton exclusion. The artifact, six sources and twenty prior
  identities matched before and after. O's raw model remained explicitly
  supplied input; the older source/alias universe and entire O certificate
  suite were not regenerated or replayed here.

Tests also cover two-strict-round refinement, false merges, equally sized
wrong fibers, early/extra rounds, corrupted witnesses/maps/digests,
bad quotient/composition and marginal laws, false measurability, invalid
rates/native types, and rejection of unsupported questions. Detached-return
and same-object mutation checks protect consumer/cache boundaries.
The runner's expected-evidence cache uses exact model content and immutable
bytes, not object identity. Lifecycle negatives use temporary stub evidence,
never the real capture.

Artifact SHA-256:
`c43435c4916e5c15efb373ff70795ed733d7c4e360ebec4e9a1b32f4e050b048`.

The frozen source ledger and complete certificate are in
[results.json](results.json). It was created once and never overwritten.
RESULTS.md and the roadmap are human reports outside that ledger.
Unrelated RET/core, temporary model-sheet and prior work were left untouched;
no dependency installation or integration occurred.

## Applicable value and next decision

The result supplies a precise, finite contract for forgetting fine relational
detail while retaining specified stochastic predictions. It also tells a
consumer when to refuse a question. That is useful structure for developing
relational estimators and validation interfaces, without requiring an
ontological commitment.

No measured speed/memory gain, materials monitoring result, anomaly-triage
performance, RET adapter, apparatus/noise validation, metric, gravitational
dynamics or continuum limit follows. The contract cannot be used to dismiss
conflicting known observables as noise.

**Next proposed gate: QR-05Q, three-layer portability stress.** Keep H,
the thinning law, six eligible vertices and parity colors unchanged. Append
all 256 adjacent-incidence masks on layers {1,2}->{3,4}->{5,6}, then their
256 reversals, preserving the old family as an exact restriction. Take full
source transitive closure before induced observation: removing an intermediary
must not erase an established comparison. Layers are not the named colors.

Freeze the bit ordering, resource bounds and failure rules before any Q
execution. Test unchanged H first; if it fails, retain the obstruction and
no global quotient, without automatic feature repair or re-refinement.
No Q domain generation or outcome search was performed by P. This tests
more transitive and mixed-color structure before treating the contract as
a general summary calculus. Lean and RET remain separately gated.
