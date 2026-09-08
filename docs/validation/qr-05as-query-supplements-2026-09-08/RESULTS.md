# QR-05AS results: query-specific supplemental linear readouts

8 September 2026. Completed bounded mathematical gate.
Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AR commit `cc02338677db72fecd729d69d7eb330a2e0a44d7`.

## Main result

Exactly FIVE additional fixed scalar linear readouts suffice, and fewer cannot
suffice, for all 64 fine responses on the declared normalized source simplex,
conditional on retaining the existing 32 coarse measurements. Both grid and
warp now have complete exact decoders. All thirteen previously unrecoverable
response rows are recovered without changing the sources or questions.

The producer receives fine-bank measurements and emits five selected response
functionals. The receiver receives only the 32 coarse values and those five
supplements: 37 measured values, plus the separately known source normalization.
This is not five new sensors, a globally minimal total packet, or full-field
reconstruction.

| Per family | Grid | Warp |
|---|---:|---:|
| Unchanged source columns | 108 | 108 |
| Coarse measured values / full bank values | 32 / 48 | 32 / 48 |
| rank A / rank [A;Q] | 32 / 37 | 33 / 38 |
| Minimal additional scalar linear readouts | 5 | 5 |
| Complete target rows / source-column predictions | 64 / 6,912 | 64 / 6,912 |
| Nonzero prediction residuals | 0 | 0 |
| Selected-filter nonzero coefficients | 12 | 12 |
| Bank coordinates in the union of filter supports | 6 | 6 |
| Complete one-readout-removal witnesses | 5 | 5 |

Here A=[1^T;O]. Its rank includes known normalization, not an extra measured
channel. The 64 target rows still include AR's 33 identically-zero functions;
recovery counts are not success probabilities. The normalized source simplex
and inherited source-column meanings are unchanged.

## The actual five readouts

The prescribed original-order greedy rule selects the same target rows in
both cases: zero-based indices [1,9,10,11,14], with labels
(1,2), (2,2), (2,3), (2,4), (2,9).

Write r_i for raw zero-based bank coordinate i. Every coefficient below is
copied from the selected inherited geometric filter, not refitted:

| Target | Grid supplement | Warp supplement |
|---|---|---|
| (1,2) | r0/48-r2/12 | 5r0/1152-5r2/72 |
| (2,2) | r8/16-r9/8-r10/4+r11/2 | r8/128-r9/32-r10/8+r11/2 |
| (2,3) | r8/16-r9/8 | 3r8/128-3r9/32 |
| (2,4) | r8/24-r10/12 | 7r8/288-7r10/72 |
| (2,9) | r8/6-r9/4 | r8/6-3r9/8 |

The support union is {0,2,8,9,10,11}. With the inherited tile-major
(1,u,v,uv) ordering, these are two moments on bank tile0 and four on tile2.
Their values depend on the unknown incoming field: geometry supplies filter
coefficients, not the values.

Mathematically these filters depend on six bank coordinates. That is a
support diagnostic, not a proof that six individual moment measurements are
minimal. The implemented producer still accepts a full 48-coordinate vector;
a separate sparse acquisition interface has not been implemented or tested.
The five filters literally compute five target answers, which the receiver
uses with coarse information to recover the remaining questions.

## Why five is minimal

AS consumes the authenticated AR matrices O, R, Q and G and verifies Q=G R
on every source column. It does not repeat AR geometry integration or source
positivity checks. Set delta=rank([A;Q])-rank(A).

Scan original target rows, selecting a row only if independent of A and all
earlier selected rows. Retain all 64 decisions, their prefix ranks, and exact
original-basis expansions of skipped rows. The selected rows increase rank
by exactly delta=5. Their literal G rows yield H=G_selected R=Q_selected.

The full decoder satisfies

```text
a*1^T + L*[O;H] = Q.
```

Its compact original-row basis and dense raw-input form are both retained.
Each complete identity and all predictions are independently checked.

For any k fixed scalar linear extra readouts T, exact recovery requires
rowspace(Q) contained in rowspace([A;T]). Otherwise a null direction can be
split into two normalized nonnegative mixtures with identical available data
and different truths, ruling out even nonlinear decoding of those data.
Since k rows increase rank by at most k, k>=delta. The construction attains
that bound.

This does not bound arbitrary nonlinear encodings, adaptive acquisition,
finite-precision/noisy instruments or a smaller physical source family.
Known affine offsets add no information beyond the normalization row.

## Every selected member is indispensable

For each selected readout j, the canonical pivot-supported right-inverse
direction w satisfies

```text
sum(w)=0,  O*w=0,  H*w=e_j.
```

Its positive and negative parts have equal mass. Dividing by that mass
produces two normalized nonnegative mixtures. All coarse values and all FOUR
other supplements coincide; the omitted supplement and its named target
differ by exactly 1/mass>0. Adding the omitted value back lets the SAME
restricted receiver recover both complete true response vectors.

The first witness is especially simple. With e_g denoting unit weight on
zero-based source generator g:

| First omitted target (1,2) | Grid | Warp |
|---|---|---|
| lambda_plus | (3/4)e0+(1/4)e9 | (9/10)e0+(1/10)e10 |
| lambda_minus | e1 | (9/10)e1+(1/10)e9 |
| Canonical right-inverse positive mass | 663552 | 10616832 |
| Omitted true response difference | 1/663552 | 1/10616832 |

All other four supplements are zero for these first pairs. All five complete
witnesses per geometry are retained: weights, raw bank/coarse values,
supplements, remaining observations, truths, predictions and zero residuals.
The directions are unit-response right inverses, not AR's first-free-column
null vectors. Their masses carry reciprocal response units; they are not
noise amplification factors or optimized error bounds.

Indispensability of this selected bank and the rank lower bound are separate
parts of the certificate. The former alone would not establish global
minimality among all allowed linear supplements.

## Normalization and application boundary

The grid canonical decoder has one nonzero intercept:
1/864 at target row63=(10,10). All warp intercepts are zero.
The grid map therefore explicitly uses the known normalization. This is valid
on the declared simplex and must not silently become an arbitrary-field
claim. A different decoder or wider domain would require a separate analysis;
a frozen-map limitation is not automatically measurement insufficiency.

The practical mathematical application is a query-specific producer/receiver
interface. A system with fine access can transmit five extra scalars to an
existing coarse-data receiver. It does not identify the 108 source weights,
calibrate a sensor, authenticate external measurements, or derive a metric,
quantum channel or gravitational dynamics. RET and Lean were not integrated.

## Representation and validation

Across both families, the capture retains 37,248 inherited input matrix entries,
480 selected-filter entries (24 nonzero), 1,080 supplement source-column values,
4,355 skipped-row expansion coefficients, 4,800 compact decoder coefficients
and 4,864 raw decoder coefficients including intercepts.
It retains 13,824 predictions, 13,824 zero residuals and 10,150 rational
occurrences in ten omission witnesses. Counts include zeros and repetitions.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Inherited problem | 118,632 | 121,454 |
| Base certificate | 743 | 746 |
| Complete selection certificate | 23,571 | 24,099 |
| Complete decoder certificate | 114,733 | 116,059 |
| Complete witness list | 35,424 | 38,029 |
| Producer map alone | 1,464 | 1,471 |
| Receiver intercept and matrix alone | 14,809 | 14,822 |
| Complete native family | 293,838 | 301,122 |

Suite size is 596,785 bytes. These overlapping verification scopes are not
additive unique storage or measured-value transmission packet sizes.

All 57 tests pass normally and optimized: 41.23 s / 41.50 s in the recorded
concurrent runs. Before freeze, 48 generic tests passed in both modes
(3.23 s / 3.19 s); all nine fixed tests were deselected.
The independent Gauss-Jordan, forward-elimination/back-substitution and
rational Gram-Schmidt routes agree on complete fixed wires.

Controls include zero supplements/banks/widths, nonzero known intercepts,
redundant rows, tiny exact pivots, nonunique supplied filters, all omission
vectors, arbitrary-width file-blind producer/receiver calls, and detached
shared inputs. Coordinate changes preserve selection while distinguishing
canonical row-basis changes; witness directions and masses scale by 1/v,
normalized weights stay fixed, and full dense-map transport is checked.

Each isolated guard subprocess mode performs 268 explicit rejections across
both engines. Shape/value admission precedes arithmetic; cyclic inputs are
rejected without rejecting shared children. Retained overflow is distinguished
from canceled intermediate products. There are 328 rejected non-noop
corruptions: 184 generic, 122 fixed-family, eight suite and fourteen selected
historical-producer changes. Two unselected prior decoder/collision mutations
are deliberately admitted by selected-bridge helpers; the real prior capture
remains fully pinned. No historical executor or old collision was replayed.

The optimized pytest warning concerns assertions in non-test modules; engine
admission uses explicit exceptions and separate normal/-O subprocess guards.
Capture/working byte caps are not process-memory or exhaustive hostile-input
guarantees.

## Freeze and evidence lifecycle

Five sources were frozen at 2026-09-08 21:52:07 UTC, before any fixed AS
projection, multiplication, selection, decoder or witness calculation.
All 118 identities were bracketed: five AS sources, 49 prior captures and
64 ancestor sources.

1. First external primary/reference comparison: 3.2114 s.
2. Exactly ONE independent normal reference-only read-only audit: 1.4434 s.
3. Full normal/-O tests and post-test identity/first-byte bracket.
4. External create-only comparison preflight: 3.1202 s.
5. Exclusive final comparison capture: 3.1590 s.
6. Fresh primary-normal / reference--O read-only replays: 2.3266 s / 1.5182 s.

The audit and full tests ran concurrently after the first comparison; both
finished before preflight. All non-runtime fields of first, preflight and final
captures agree, with all identities and capture bytes unchanged.

Prefreeze review added the primary's active-cycle admission guard and moved
a test-oracle state update outside an assertion. Synthetic checks were
strengthened before freeze. No model or mathematical correction was needed.
There were NO post-first source, protocol, fixture or mathematical changes.

Final capture: 614,211 bytes, SHA256
`901c7e1a7c53be35be5654fbb01e5bbde4044f6a50184dd80014df155129e366`.
Suite: 596,785 bytes, SHA256
`aa57d394aa905a55078371027bf455cb436bb229b5ca25fa16a94c7dfad5776b`.

## Next proposed gate

QR-05AT should test bank-level structural portability of the SAME frozen maps.
Derive the coarse parent-sum map C from authenticated supplied tile lineage,
verify O=C R, and split the receiver matrix horizontally as L=[Lc Lh].
Then compare K=Lc C+Lh G_selected with the full bank map G.

The simplex identity a*1^T+(K-G)R=0 is weaker than the unrestricted
coefficient conditions a=0 and K=G. Retain the entire intercept and defect
matrix, not just residuals on old source columns. A failure must remain visible;
do not refit the decoder or invent off-model normalization constraints from
the observed residuals. This structural question should precede a shared-bank
measurement-error study. No AT map construction or defect calculation has run.
