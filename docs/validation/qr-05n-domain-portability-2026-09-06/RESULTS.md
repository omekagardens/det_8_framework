# QR-05N results: finite domain-portability stress

6 September 2026. **Completed investigative gate; candidate portability fails.**
Research base: pushed QR-05M checkpoint `c991bc2`.

## Outcome

The unchanged summary C=(frame,B,M) does not have a closed next-summary
law on the prespecified larger family. Equal complete pair tensors and
equal K2,2 motif counts can still conceal different sampled observations.

This is a mathematical obstruction, not a test-suite failure or a reason
to change the feature retrospectively. Both independent implementations
retain the same exact witness. No refined global quotient or replacement
feature was constructed.

| Partition on 2,470 observations | Classes | Full next-summary law |
|---|---:|:---:|
| Pair-overlap B, with frame | 165 | Not closed |
| B plus unchanged motif M, with frame | 166 | Not closed |
| Original M-domain restriction of (B,M) | 110 | Closed on its original 257 states |

The old finite success remains intact. Neither this failure nor that
success is evidence for a physical law, metric or ontology.

## A small explicit obstruction

The first candidate failure compares two complete observations with fixed
bottom 0/top 7 and all six eligible interior vertices:

    A: 1<4, 1<6, 3<2, 5<2
    B: 1<2, 1<6, 3<4, 5<2

All odd interior vertices form the lower color layer. The underlying
undirected comparability graphs are two disjoint two-edge stars versus a
three-edge path plus a separate edge. These graph descriptions do not
replace the explicit directed orders above.

The records have identical complete D/B tensors and M=0. Both have
N=(1,6,4,0), and their common second edge-count moment is

    E[N2(U)²] = 4xy + 2x²y + 2xy² + 8x²y².

Yet A alone can leave four mutually incomparable eligible vertices:
retain its four leaves {3,4,5,6} and remove the two centers {1,2}.
Writing p=x²(1-x)y²(1-y), the full count-law event N=(1,4,0,0) has
probabilities p from A and zero from B. At half retention this is
1/64 versus zero. The complete count-law polynomials are retained;
no distributional difference was inferred merely from a scalar feature.

The automatically first next-C witness uses target class 11: two eligible
vertices of each color with exactly one interior comparison.
Its probabilities are zero from A and 3p from B, or zero versus 3/64
at half rates. At (1/3,2/3), they are zero versus 8/243.
The first distinguishing prescribed grid point is (1/3,1/3).
Structural zero atoms and all 22 evaluation points remain recorded.

A/B are states 612/625, first aliases (profile 84, mask 63) and
(profile 91, mask 63), named layered_oe_078 and layered_oe_085.
Their current candidate class is 147. These IDs locate the evidence;
the summary does not use them. The original path/cycle B failure also
remains, as B class 105 with states 232/256 and target 11.

This witness shows a distinction beyond pair overlap and four-cycle
counting. It does not show that one particular new statistic will repair
every failing class.

## What was broadened—and what stayed fixed

The first six M profiles remain unchanged. N appends all 512 row-major
3-by-3 odd-to-even incidence matrices, then all 512 matrices with every
comparison reversed. The incidence bit convention is unchanged on reversal;
the matrix is not transposed. Density, fixed probes, eligible color marks
and independent retention rates are unchanged.

The resulting inventory is 1,030 profiles, 65,888 source/mask aliases and
2,470 deduplicated observations. There are 2,213 new states, and 29,217
new aliases attach to old states. Aliases remain provenance, never weights
or hidden feature inputs.

Numeric vertex labels are no longer topological labels. Chain recognition
now uses the supplied strict relation, allowing comparisons such as 3<2.
The separate observed-subset and directed-source-chain algorithms agree;
a single descending-ID edge gives N=(1,6,1,0) in either orientation.
This generalization exists only in the new N sources; prior executors
were not edited.

Complete K3,3 in either direction gives N=(1,6,9,0), nine overlapping
K2,2 supports, and expected motif count 9x²y². Across the larger domain,
495 observations have positive M; there are 739 support occurrences and
the maximum is 9. The motif is no longer a Bernoulli-valued observable.

## Mean identities survive; full recursive closure does not

Every support-graded D/B expected update and every motif update still
holds exactly. In particular,

    E[M(U)|S] = x²y²M(S).

The motif proof uses induced support preservation and linearity; overlapping
supports need not survive independently. All 12,646,400 D/B cells and
39,520 motif cells pass. These identities are insufficient to make equal
current summaries imply equal full next-summary laws.

Accordingly both expanded quotient arrays are empty and both expanded
composition certificates are null. This gate does not invent a Markov
update for an insufficient summary. Fresh fine thinning retains its
per-vertex composition argument; no expanded coarse semigroup is claimed.

## Exact preservation of QR-05M

The first 257 states retain M's frame, kept/past observation, mask, colors,
counts, D/B, motif supports and every fine/pushed coefficient. Filtering
aliases to the first six sources reproduces all 352 original aliases.
Old induced transitions stay inside that subset-closed prefix.

Actual class maps and pulled-back memberships reproduce M's old partitions.
The old 110-class candidate quotient is rebuilt using only old members;
all 1,154 quotient atoms and its 295,424 four-variable composition cells
match M exactly. This is the quotient of the restricted old process,
not a restriction of a nonexistent globally closed N quotient.

N deliberately omits expanded color-order canonicalization, stable
refinement rounds, covariance towers and joint-trace experiments. Those
prior artifacts remain pinned and unchanged. The slimmer N output is
not described as a whole-schema reproduction of M.

## Verification and evidence

The primary computes observed chain sets, ordered support unions, binomial
kernels and explicit motif quartets. The reference traverses source-directed
chains, obtains B from complete induced count-law moments, interpolates
cached exact rational-grid kernels and recognizes motifs through common
neighbors. Features are computed once per deduplicated observation.
Neither executor reads prior artifacts, earlier executors or the other route.

Independent runner/tests reconstruct incidence matrices, observations,
features, classes, kernel rows and the old-domain bridge. Review found and
fixed a native-type gap before capture: boolean IDs/indices could otherwise
alias integers in tuple lookup. Early type guards and first-alias canonical
record checks now reject this, including regressions on newly added states.

| Exact check | Total |
|---|---:|
| Fine / pushed transition atoms | 99,180 / 97,536 |
| Fine plus pushed coefficient cells | 3,147,456 |
| D / B feature cells | 158,080 / 632,320 |
| D/B / motif expected-update cells | 12,646,400 / 39,520 |
| Fine / pushed rational-rate atom checks | 2,181,960 / 2,145,792 |
| Deterministic corner rows | 9,880 |
| Original restricted quotient composition cells | 295,424 |
| Expanded closed quotients | 0 |

Validation passed:

- 101 tests normally (150.61s) and 101 optimized (151.23s). The runs were
  concurrent; measurements are descriptive, not performance benchmarks.
  Optimized pytest emits its standard non-test-assertion warning;
  executor/runner checks and optimized subprocess guards explicitly raise.
- Ruff check/format and all six new-source whitespace checks passed before
  freezing. All 18 prior artifacts retain their published identities.
- Exclusive create-only capture: 22,260,768 bytes, below the 64 MiB cap;
  suite time 37.357302625023294s.
- Exact read-only replay: normal 38.301052332972176s, optimized
  38.353077665989986s. Neither altered the capture.
- Independent JSON-only postflight: 25,503,340 explicit checks in 16.532s,
  with no executor, runner or test imports. It rebuilt the entire declared
  incidence/alias domain, features, fine/pushed rows, expected-update cells,
  actual fibers and witnesses, complete witness count laws, rate/corner
  checks and old M restriction including all 295,424 composition cells.
  Six source and 18 prior identities were checked before/after; bytes stayed
  unchanged. No files were edited by the postflight.

Mutation tests cover label-order/count errors, reversed incidence indexing,
alias loss/weighting, lost or duplicated motifs, same-sized incorrect fibers,
native boolean/integer substitutions, coefficient corruption, hidden
failures, fabricated failed quotients and incorrect prior class maps.
Lifecycle tests use temporary stub evidence and check the 64 MiB cap in both
capture and replay; no real artifact is modified for negative tests.

Artifact SHA-256:
`f2d666285afef41cd8a7f977399d3626a620da39174967a38047714f5f26f93e`.

All six source identities are frozen. The artifact was created once,
read back, and replayed without overwriting. Reports and roadmap updates
are outside the source ledger. RET/core, earlier evidence and unrelated
checkout work were untouched; no dependency installation occurred.

## Applicable value and proposed next gate

The useful result is a concrete boundary on summary-based prediction.
Matching means, covariance polynomials and one interpretable motif does
not ensure that a supplied abstract thinning process can be
updated from that summary alone. Any proposed implementation needs either
a stronger observation contract, additional structure, or access to a
richer record. A different sampling law would be a separately stated model,
not a repair of this unchanged-law counterexample.

**Next proposed gate: QR-05O, obstruction-targeted observable repair.**
Freeze an explicit candidate T counting eligible induced color-layered
four-vertex paths: two vertices of each named color, no same-color
comparisons and exactly three uniformly directed cross-color comparisons.
Test (frame,B,M,T) on the unchanged N domain, without assuming success.
Compare actual fibers and full pushed laws, preserve prior observation/feature/kernel evidence,
and keep T's support-survival expectation separate from recursive closure.
Any remaining failure must remain visible. No T implementation, expected
update certificate or global repair is claimed by N.

For Track B this remains mathematical model checking of coarse relational
descriptions. It is not event growth, physical time, a metric, gravity,
a quantum law or an ontology proof. There are no empirical data, apparatus
noise/calibration results, RET integration or Lean proof in this gate.

See the fixed [protocol](README.md) and canonical [results.json](results.json).
