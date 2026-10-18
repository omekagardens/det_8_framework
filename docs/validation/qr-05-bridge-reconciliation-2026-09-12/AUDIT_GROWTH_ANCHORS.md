# Audit: QR-05DI–DM growth studies and QR-05DO anchor calculus

12 September 2026 (Pacific/Honolulu). Review of the concurrent `qr-05-bridge`
branch at the immutable commit
[`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`](https://github.com/omekagardens/det_8_framework/tree/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8).
This is an audit and selective-adoption recommendation, not a merge, an
apparatus validation, or evidence for manifoldlike emergence.

## Scope and verification

The audit read the README/result documents, protocols, primary/reference
implementations, tests and relevant drivers for DI, DJ, DK, DL, DM and DO;
it also inspected DO's CY fixture and the shared `order_count_geometry.py`
generator. The pinned branch was inspected in an isolated archive. No archive
source, stored capture or freeze was edited, regenerated or overwritten.

The six existing suites were run with `python3 -B`, with a 50-second process
timeout per suite. All **67 tests passed**:

| Gate | Tests | Reported suite runtime |
| --- | ---: | ---: |
| DI | 10 | 2.857 s |
| DJ | 10 | 7.083 s |
| DK | 9 | 6.764 s |
| DL | 11 | 3.632 s |
| DM | 12 | 1.871 s |
| DO | 15 | 0.233 s |

These suites check selected fixture results, known answers and route agreement.
Their success does not establish population-level calibration, a covariance
theorem, or a general manifoldlikeness/no-go result. Additional diagnostics
described below ran in memory, under a 50-second alarm, without changing the
stored protocol or evidence. They are audit counterexamples, not a new
pre-registered statistical study or gate capture. Broader source-freeze and
artifact-provenance checks belong to the reconciliation's repository-wide audit.

## 1. DO: familywise identification is not joint identification

DO evaluates each target within a separate one-variable family and then combines
the resulting booleans to report a joint minimum. The first operation is a valid
conditional slice calculation; the second does not generally follow. The
implementation never checks the joint target on one common class containing the
simultaneous alternatives. See
[`primary.py:208–212`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05do-anchor-calculus-2026-09-11/primary.py#L208-L212)
and
[`primary.py:315–321`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05do-anchor-calculus-2026-09-11/primary.py#L315-L321).

The executed exact counterexample is `O(a,b) = a XOR b`, with binary `a,b`.
On the slice `b=0`, O identifies a. On the slice `a=0`, O identifies b.
On all four worlds, however, `00` and `11` agree observationally while both
target coordinates differ; likewise `01` and `10`. DO's own `classify`
function returns `IDENTIFIED` on the two slices and `NON_IDENTIFIABLE` on
the common class.

This does not assert that the particular stored minimum changes under every
possible enlargement of DO's fixtures. It establishes that the code does not
verify the advertised common-world joint claim. Retain the slice results as
such; recompute joint identification on an explicitly declared common class.

## 2. DO: the conformal world combines two different point panels

DO retains order, signs and distance ratios from its `b=0` sample while replacing
counts with counts from a newly generated `b=2` sample. This is not the stated
single set of fixed events with all channels computed from that record. See
[`primary.py:129–142`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05do-anchor-calculus-2026-09-11/primary.py#L129-L142).

Recomputing the channels of the actual count panel, with the frozen `n=48`,
`seed=6` fixture, gives:

| Quantity | Stored b=2 world | Actual b=2 count panel |
| --- | ---: | ---: |
| Ordering fraction | 0.45035461 | 0.460992908 |
| Count profile | Same as count panel | Same |
| Pair-sign comparison | 574 of 1128 signs differ between the panels | — |

Conformal invariance of the causal relation for fixed events is distinct from
invariance of the finite sampled order after resampling. An explicitly declared
two-panel synthetic interface could be legitimate, but its joint observation
law and interpretation must be stated. Otherwise compute every channel from
the same declared record, or separate fixed-event causal invariance from
population-density estimation into different experiments.

The anchor also directly receives the generating scale `c`, while the target
is `c`; see
[`primary.py:118–125`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05do-anchor-calculus-2026-09-11/primary.py#L118-L125).
This is an admissible **perfect injected anchor oracle**, not a demonstration
that an independently calibrated physical anchor exists. Its mathematical
ability to distinguish the selected scale worlds must remain separate from
apparatus/reference validity and uncertainty.

## 3. DI–DM: fixture differences do not certify non-manifoldlikeness

DI and DJ do not instantiate an exactly matched growth-law sample for their
principal matched comparison. They interpolate link/leakage summary curves
against the selected sprinkle's ordering fraction. DI additionally sets its
two-point-match flag to literal `True`. See
[`DI primary.py:152–188`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05di-native-growth-law-2026-09-11/primary.py#L152-L188)
and
[`DJ primary.py:183–207`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dj-det-native-law-2026-09-11/primary.py#L183-L207).
The interpolated curves are useful exploratory summaries, not separately
verified matched realizations or calibrated rejection tests.

DM improves this by constructing parameter-matched adversaries. Its rejection
criterion is nevertheless a chosen mean-gap threshold of `0.05`, or a
histogram L1 distance exceeding three times the reference sample's split-half
distance. See
[`DM primary.py:409–428`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dm-stronger-adversary-2026-09-11/primary.py#L409-L428).
Overlapping intervals are dependent, and splitting intervals within one causal
set does not by itself measure variability between independently generated
causal sets. The README acknowledges that the thresholds are choices; that
caveat does not convert them into a calibrated manifoldlikeness classifier.

### Known-manifoldlike diagnostic

The audit used DM's unmodified `n=192`, sizes `{6,10,14,18,22}`, `cap=400`,
shuffle seed 11 and rejection thresholds. Its genuine d=2 Minkowski sprinkle
at seed 11 was the reference. Independently generated d=2 sprinkles at seeds
12, 13 and 14 were compared by the same rule.

| Comparison seed | Ordering fraction | Largest absolute per-size mean gap | Mean-failing sizes | Histogram-failing sizes |
| --- | ---: | ---: | --- | --- |
| 12 | 0.556064572425829 | 0.03951382649495855 | None | None |
| 13 | 0.4870746073298429 | 0.06280660131943139 | 6 | None |
| 14 | 0.4987456369982548 | 0.03067703623319462 | None | None |

Thus a known-manifoldlike sample is rejected by the advertised abundance rule.
These comparison samples were **not fitted to match the reference's global
ordering fraction**. The diagnostic does not estimate a false-positive rate,
nor resolve a conditional test given a matched global statistic. It does show
why abundance-rule rejection alone cannot be promoted to a determination of
non-manifoldlikeness. A conditional matched-statistic test needs its own
explicit null law and calibration.

Prospective work should fix the statistic and thresholds before held-out
whole-realization validation, distinguish exploratory tuning from evaluation,
include genuine-manifoldlike nulls, account for the multiple tested sizes and
any parameter fitting, and report false-rejection uncertainty. Until then,
retain descriptive separation of these selected fixtures only.

## 4. DM: the no-go flag has an invalid logical trigger

DM sets `a_no_go_is_established` to true if every adversary passes the abundance
test. See
[`primary.py:453–454`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dm-stronger-adversary-2026-09-11/primary.py#L453-L454).
The reference repeats the same rule. In the audit's in-memory diagnostic,
changing only `deviation_tol` to 1 and `hist_factor` to 100 made all three
`fails_the_abundance_test` values false and the no-go flag true.

No stored protocol or capture was changed. This diagnostic exposes the logical
problem: neither passing nor failing a finite set of selected statistics
establishes a general no-go theorem. Such a claim requires a defined law class,
a stated mathematical proposition and an independent proof. The current
captured false flag should remain an unestablished claim, not a predicate
that can become established by relaxing a threshold.

There is also a boundary bug in the threshold calculation: a split-half noise
floor of zero is treated as absent rather than as a zero threshold at
[`primary.py:409–410`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dm-stronger-adversary-2026-09-11/primary.py#L409-L410).

## 5. DJ: record association is not a covariance theorem

DJ describes record leakage as breaking covariance, while its actual quantity
is Pearson correlation between κ and comparability degree. See
[`README.md:6–8`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dj-det-native-law-2026-09-11/README.md#L6-L8)
and
[`primary.py:110–118`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dj-det-native-law-2026-09-11/primary.py#L110-L118).
That statistic is invariant under jointly relabeling the vertices and their
κ-values. Association is not itself a counterexample to covariance. The
record-legibility/manifoldlikeness tension flag is literal `True` at
[`primary.py:207`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dj-det-native-law-2026-09-11/primary.py#L207).

Retain the observed κ–degree association in the selected `sum` fixtures. Before
claiming a covariance cost or monotonic tradeoff, define the relevant symmetry,
its action on the marked growth law, the invariance condition, and the actual
violation or parameter-dependent comparison.

## 6. Reference independence and the DL correction

DI advertises an independent light-cone reference, but its two causal predicates
are identical: compare
[`primary.py:53–62`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05di-native-growth-law-2026-09-11/primary.py#L53-L62)
with
[`reference.py:34–43`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05di-native-growth-law-2026-09-11/reference.py#L34-L43).
Closures, interval counting, MM evaluation and report-selection logic are also
very similar across the early growth routes. Shared seeds can be appropriate
for implementation comparison, but agreement between near copies does not
independently validate the statistical estimand or inference.

DL's preserved
[`SUPERSEDED.md`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dl-interval-self-similarity-2026-09-11/SUPERSEDED.md)
correctly records the consequence: both routes originally stopped the pair
sweep at the interval-sample cap and agreed on the same wrong interval density.
The v2 complete sweep, retained v1 artifact and small-cap chain regression are
valuable corrections. DM's bitmask-versus-BFS reachability is also a genuine
improvement in algorithmic independence.

However, DL's corrected report still states that the layer-cakes have no
intervals and density zero at
[`primary.py:224`](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dl-interval-self-similarity-2026-09-11/primary.py#L224).
The corrected table gives positive densities approximately 0.335 and 0.503;
only the selected interval-size window is empty. This distinction must also
be corrected in machine-readable conclusion strings, not just table columns.

## Valuable structure and the bounded local repair

Retain, with explicit hypotheses:

- Exact finite observational equivalence and target factorization.
- Monotonicity of identification under adding channels.
- The obstruction that processing identical observations cannot distinguish
  different targets on the same observation fiber.
- Complete-population `interval_density = 1 - link_fraction` and exact chain,
  bipartite and layer-cake controls.
- Higher-order interval profiles as exploratory diagnostics, without promoting
  chosen-threshold differences to population/no-go conclusions.
- Explicitly ideal external anchors, distinct from the evidence needed to
  justify a physical reference or calibration.

The corrected common-world proposition is elementary. Fix one nonempty finite
world class W; define every channel O_c and joint target τ on W. For each pair
u,v with `τ(u) != τ(v)`, let

`D_uv = { c : O_c(u) != O_c(v) }`.

A channel set S identifies τ if and only if `S ∩ D_uv` is nonempty for every
such pair. Indeed, identification fails exactly when a differing-target pair
agrees on every selected channel. This proves monotonicity under refinement
and supplies an independent pair-separator/hitting-set verification route
alongside a direct observation-fiber partition route. Inclusion-minimal
identifying sets and minimum-cardinality identifying sets must be reported
separately.

The fixed four-world XOR control, with channels `a`, `b` and `x=a XOR b`, has
joint inclusion-minimal sets `{a,b}`, `{a,x}` and `{b,x}`, all of size 2.
The single x channel fails on the common class despite succeeding on each
one-variable slice. Constant-target and inseparable different-target controls
should cover the opposite boundaries.

This review motivated the separately authored local [calculus.py](calculus.py).
Its input is an exact declared mathematical table, not acquired apparatus
data. The local build uses its own frozen contract, independent oracle,
strict validation and source-bound [verification evidence](RESULTS.md). None of the audited
growth-law or apparatus-validity claims is inherited by that mathematical
construction.
