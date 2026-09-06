# QR-05C results: finite coarse dynamics and delayed information loss

5 September 2026. **Bounded dynamic-consistency investigation completed.**
Five full analyses agree between the direct Kraus executor and the independent
diagonal-coefficient reference. All 92 tests pass normally and under optimized
Python; the retained capture replays exactly.

This establishes an exact finite coarse-transition contract and tests a nested
family of record resolutions. It does **not** establish physical spatial scale
invariance, a continuum limit, manifold emergence, or gravitational dynamics.

## What changed from QR-05B

QR-05B identified summaries that lose future information. QR-05C tests whether
a summary can support its own transition law, without consulting the discarded
fine record, and whether that law remains correct after another step.

For each fine parent h and coarse target b, sum its outgoing quantum maps into
that target. A universal coarse law exists exactly when these summed maps
agree for every pair of fine parents in the same coarse class. This compares
full maps on arbitrary intermediate quantum blocks, not just probabilities
or a particular source-produced state.

When the condition holds, use the common row once per coarse parent. Growing
then coarsening equals coarsening then growing. Checking the condition at each
intervening level gives the corresponding iterative identity. If it fails,
the chosen representative's row remains a normalized trial model, not a valid
universal quotient. Its apparent success for one step can fail at the next.

## Positive result and limits of compression

For every tested growth/instrument case, retaining the marked event order up
to isomorphism supports exact one- and two-step quotient dynamics. The fine
history counts through four events are 1,2,8,56,640; marked-order counts are
1,2,7,32,192. Each fine history is counted once, including zero branches.

This removes natural birth labels while retaining the order and its
setting/outcome marks. It is a genuine finite quotient, but not yet an
economical geometric summary. At p=2/5, none of the three tested summaries
that discard more marked-order information is universally closed.

The nested summaries are marked order; unmarked shape plus total ones;
reduced counts (n,links,incomparable pairs,total ones); and size plus total
ones. Their respective class counts at n=4 are 192,80,50,5. Reduced counts
omit minimal/maximal counts explicitly; they are not QR-05B's five-count tuple.

| Case | Marked order | Shape + ones | Reduced counts + ones | Size + ones |
|---|---|---|---|---|
| Weak phase, p=2/5 | Pass all | Fail at n=2,3 | Fail at n=2,3 | Fail at n=2,3 |
| Grouped dephasing, p=2/5 | Pass all | Fail at n=2,3 | Fail at n=2,3 | Fail at n=2,3 |
| Weak phase, p=0 | Pass all | Pass all | Pass all | Pass all |
| Weak phase, p=1 | Pass all | Pass all | Fail at n=3 | Pass all |
| Uniform-ideal growth control | Pass all | Fail at n=2,3 | Fail at n=2,3 | Fail at n=2,3 |

Here n is the parent event count; one-step tests cover n=0,...,3. For either
p=2/5 instrument and the uniform control, the three non-marked summaries also
fail two-step comparisons starting at n=1 and n=2. Marked-order two-step
comparisons pass throughout. Both boundary cases pass the tested two-step
comparisons, which start only at n=0,1,2; the p=1 qualification below matters.

## Exact delayed-failure control

Start with a single event whose recorded outcome is one. Under shape-plus-ones
compression, its immediate coarse row is exactly correct: the parent class
contains only one fine history.

After a birth that produces chain record 10, the trial model selects the
canonical chain record 01 for its next prediction. Both have the same shape
and total ones, but the phase-setting control reads different past records.

At p=2/5 with weak-phase operations, two steps toward a fork containing one
recorded one give these outputs on the same intermediate P+X input:

```text
actual = [[486, -864], [-864, 1536]] / 78125
trial  = [[486, -864i], [864i, 1536]] / 78125
```

Both traces are 2022/78125. Nevertheless, a subsequent P+X measurement has
joint probability **147/78125 versus 1011/78125**. Thus checking only the
immediate step or only this later branch's probability misses a predictive
failure in the residual quantum state. Full-rank physical witnesses are also
retained; the pure-state example makes the phase difference especially clear.

The simpler one-step control compares two-event chain records 01 and 10.
Into the fork-with-one-one target, their maps are `(6/25) D0(.)D0` and
`(6/25) V D0(.)D0 V-dagger`. Their E01 coefficients are 72/625 and -72i/625.
Matrix units are an equality-test basis, not physical preparations.

These are discrepancies within the stated quantum-instrument model, not
attributed to experimental noise or a setup fault. The shared qubit is not
asserted to model physically spacelike-separated operations.

## Three distinctions that matter for Track-B

**More retained counts do not automatically give a closed description.**
At p=1, growth appends a new top event. Size plus total ones predicts its own
updates and quantum setting. Reduced link counts ask an additional question:
how many links are added? That requires the old number of maximal elements,
which this summary omitted. A three-event fork and join share its parent label
but produce different new link counts. The coarser size summary closes while
the finer reduced-count summary fails. Closure is not monotone with resolution.

**Restricted-source agreement is not universal closure.** The p=1 process
started from the empty source reaches chains, not the conflicting fork.
All of its fixed-source-branch comparisons pass. Its bounded two-step trials
also avoid the problematic intermediate fork and use the correct join
representative where needed. Neither observation repairs the universal
one-step failure on formal parent CQ blocks. The zero source maps remain in
the evidence rather than being pruned.

**Quotient dynamics is not completed-history birth-label covariance.** Uniform
choice among ideals gives normalized, relabeling-equivariant one-step rows,
so the marked-order quotient exists. But its complete natural-history source
maps differ within some marked classes at sizes three and four. All four
percolation cases pass those separate source-map comparisons. A successful
quotient therefore does not automatically satisfy the stronger birth-label
condition adopted elsewhere in the research.

The previous fork/join and record-location controls remain present. At p=2/5,
the fork and join share reduced parent counts but have probabilities 4/25 and
2/5 that the next total incomparable-pair count stays one. The same-shape
records 001 and 010 also induce different coarse transition rows.

## Multiplicity and verification

The coarse generator uses outgoing transitions from one representative, because
the coarse input already sums the populations of equivalent parents. Summing
those parent generator rows again doubles the first non-singleton marked
class's total trace: two instead of one. This deliberately wrong row is still
CP; positivity alone is not normalization or predictive validity.

- **92 tests passed** normally in 26.07 s and under optimized Python in 25.95 s.
  The latter emitted pytest's expected warning about assertions outside
  rewritten test modules. Executable validators use explicit exceptions.
- Independent algorithms agree on all five complete outputs, including class
  keys, map-bank interning, full comparison tables, zero entries, witnesses,
  source restrictions, and analytical controls. Independent design review
  checked both implementations and the capture runner before capture.
- A separate post-capture, JSON-only audit, without importing either executor,
  verified all source/prior hashes, partitions, CP/normalization checks,
  comparison tables and prior conformance. It also recomputed all 37 retained
  full-rank discrepancy witnesses and 30 analytical output/trace checks;
  the result interpretation passed its claim-boundary review.
- 3,535 fine histories and 3,530 outcome-resolved birth edges across five cases.
- 94,700 one-step and 13,910 two-step full-map comparisons: **108,610 total**.
  These include repeated and zero comparisons, not that many distinct maps.
- 1,610 map-bank CP checks, summed per case; 2,620 trace-normalization checks
  on source-level totals and proper fine/coarse rows. The deliberately doubled
  row is tested as a failure control, not required to normalize.
- All 335 checked QR-05A source maps and all 3,584 checked QR-05B continuation
  blocks are reproduced exactly from the new dynamics. Prior implementations
  are not imported; pinned result data are compared directly.
- 14 malformed inputs are retained as rejected by both executors. Additional
  tests cover parser types/fields, optimized validation, schema and canonical
  artifact checks, symlinks, source/prior identity changes, create-only capture,
  and byte-preserving replay. Ruff checks passed before capture.
- Maximum retained rational component: 52 bits, below the 4,096-bit guard.
  No sampling, tolerance equality, fitted data, RET imports or new dependencies.

The exact CP test uses the supported 2x2 Choi block of these diagonal
matrix-unit superoperators; it is not a general numerical positivity solver.
Nonselective quantum measurements preserve total trace, not generally the
state. That distinction is maintained throughout this study.

## Retained artifact and next gate

[results.json](results.json) is a create-only 9,923,514-byte artifact with SHA-256:

```text
4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1
```

It binds seven source identities and six unchanged prior artifacts. Capture
used isolated Python 3.11.6 on macOS arm64 with a fresh external bytecode cache:
18.518 s for the suite and an 86,523,904-byte process RSS high-water mark.
These exclude serialization and are not application-performance claims.
Fresh optimized replay matched the full suite in 18.654 s and left the artifact
bytes unchanged. See the [protocol](README.md#reproduction) for commands.

The next planned gate is QR-05D: diagnostic geometric correspondence on
**supplied generating models**, with non-geometric adversaries. Choose declared
order/count or propagation-related questions, compare them to the geometry
provided by those models, and state sampling, density and boundary assumptions.
Do not treat the failed coarse models here as certified predictive theories.

Physical spatial coarse-graining, continuum behavior, an apparatus-to-order
interface and gravitational dynamics remain unestablished. The present result
provides a tested criterion for preserving relational predictions, not a metric
or an ontological commitment. See the [research plan](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
