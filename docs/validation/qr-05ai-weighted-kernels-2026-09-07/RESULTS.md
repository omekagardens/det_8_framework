# QR-05AI: weighted causal-kernel refinement

7 September 2026. Research after pushed AH commit
`c387b55054eeb2b33bd6a9027b3178701968e3c9`.
The [prospective protocol](README.md) declares every fixture, normalization,
observation law, decomposition and verification boundary before fixed AI work.
The gate is complete; verification and claim boundaries are recorded below.

## Main result

The two independent engines agree exactly across all 27 cases and 4,032 mask
rows. All first-order volume targets, observed estimates, means and covariance
blocks match AH under the declared scaling. The second-order calculation
exposes geometric information that exact first-order volume does not preserve:
causal pairs within a cell and partially causal pairs across cells.

Twenty of fifty consecutive-level second-coefficient absolute errors improve;
thirty stay unchanged. No worsening occurs in this prescribed family, but
these finite comparisons establish neither a monotone-error theorem nor a
continuum limit. The warped lower-unaligned error changes from negative to
positive at the final level even though its absolute size improves.

Inclusion correction recovers every supported supplied target in expectation.
Singleton sampling leaves ten nonzero pair questions unsupported, even though
the first-order means remain correct. Zero variance then does not imply a
correct full-target estimate.

## The mathematical bridge being tested

For a supplied causal interval of volume V in flat 1+1 geometry, compare the
first three coefficients of a scalar retarded series in mass-squared. The
continuum coefficients are 1/2, -V/4 and V²/32, from the flat scalar convention
used in [Johnston, §§3.1–3.2](https://arxiv.org/pdf/0806.3083).
This study does not test finite-mass accuracy or a stochastic sprinkling limit.

Let w_i be the supplied volume weight of a cell whose representative lies in
the interval. The finite coefficients are

    k0 = 1/2,
    k1 = -(1/4) sum_i w_i,
    k2 = +(1/8) sum_(i precedes j) w_i w_j.

Only eligible cell representatives carry quadrature weight. The fixed probe
markers have zero weight, including markers inside another interval. Pairs
are strict, distinct, directed and counted once. No amplitude squaring, Born
probability, quantum channel or ontological premise is used here.

The first-order coefficient is precisely the preceding volume calculus with
a fixed negative factor. The second-order coefficient adds causal pair
structure. Its adequacy cannot be inferred from volume accuracy alone.
This is not an exact replay of AF's density-weighted count: AF also counted
fixed internal probe events, whereas these bookkeeping markers have zero weight.

## Exact volume does not imply an exact pair coefficient

The whole-probe geometric coefficients are:

| Source | Level 0 k2 | Level 1 k2 | Level 2 k2 | Continuum k2 |
| --- | ---: | ---: | ---: | ---: |
| Grid | 1/384 | 7/2304 | 11/3072 | 1/128 |
| Warp | 23/13824 | 107/55296 | 1777/884736 | 1/128 |

Both sources already have exact whole volume at every level. Their pair
coefficients still differ from each other and from the continuum comparison.
The active warp preserves representative order, but correct local volumes
change these weighted coefficients. It is not a passive coordinate change.

The upper-aligned grid interval is an especially direct witness. Its volume
is exactly 1/12, but its finite pair coefficient is zero at every level,
versus continuum 1/4608. That probe contains one whole cell. A single
representative has no distinct partner, while the cell contains distinct
causally ordered continuum points. This is a deterministic representation
discrepancy, not an anomalous physical observation or experimental noise.

The lower-aligned grid coefficient is also zero at levels 0 and 1 despite
exact volume. At level 2 it becomes 1/3072, approaching but not equaling the
continuum value 1/1152. For the warped lower-unaligned probe the final value
95/2654208 exceeds its continuum 81/3125000; the signed discrepancy is
+10235519/1036800000000. We retain that sign crossing rather than reporting
only an absolute improvement.

## What a point-order approximation omits

Use true cell volumes g_i for the geometric finite pair sum P_g. Let h_i be
the clipped cell volume inside the probe, even if that cell's representative
lies outside it. Define K by weighting the representative-order Boolean with
h_i h_j over distinct cells. Separately integrate the actual continuum causal
relation over every ordered pair of clipped cells, obtaining J_ij.

Jcross sums all distinct-cell integrals, including pairs of cells whose
representatives are incomparable. Jdiag sums the same-cell integrals. The
latter is not the zero-measure diagonal x=y: it includes two distinct points
inside one cell. For rectangular clips it equals sum_i h_i²/4.

The exact accounting identity is

    P_g − V²/4 = (P_g − K) + (K − Jcross) − Jdiag.

The three displayed terms record probe-boundary selection, cross-cell order
approximation, and omitted within-cell pairs. They depend on the specified
intermediate K and are not a unique division into physical mechanisms.
Multiplying by 1/8 gives the second-coefficient discrepancy. There is no
inherited AH kernel-error bound or assumed monotone refinement improvement.

For the whole grid probe at level 0, the unscaled terms are

    boundary = 0, cross-order = -1/32, omission = -1/96,
    total = -1/24; coefficient error = -1/192.

Thus a probe with no boundary error can still have substantial pair error.
At the first lower-aligned refinement, the within-cell integral decreases
from 1/288 to 1/384 while the finite pair coefficient remains zero: the
cross-order term changes in the opposite direction and cancels that gain.
Across the full family, thirty within-cell terms decrease and twenty remain
unchanged. Improving one component is not automatically improving their sum.

## Incomplete observations

An observed chain with eligible support A is weighted by its full joint
inclusion probability pi(A). Positive individual inclusion suffices for k1,
but positive pair inclusion is needed for each nonzero k2 target term.
Zero-support terms are explicitly omitted and recorded, never divided by zero.

The corrected mean equals the supported supplied target T+. Its difference
from the full supplied target T is T+−T, not a failure of the weighting identity.
Each comparison retains sampling/support bias, annotation error and geometric
approximation error separately. A zero-variance estimate of an unsupported
target is not certified correct.

Across the six singleton cases there are ten unsupported question occurrences
and 44 omitted full-source chain occurrences. Every positive singleton record
has zero pair output, and every pair variance is zero. The ten nonempty
supplied targets nevertheless have negative full-target bias. Empty pair
targets elsewhere are supported vacuously; they are not misclassified as
failures. These counts repeat source/design/level/probe contexts and are not
distinct experiments. A retained record alone does not reveal the inventory
of missing source pairs; that inventory belongs to the source-aware audit.

Covariance couples the same observation law across all probes and degrees.
Two pair chains can require up-to-four-cell inclusion. Shared cells and zero
union-inclusion terms remain in the calculation; covariance entries may be
negative, particularly across coefficients with opposite signs.

For independent-half observation on the grid, the whole k2 variance increases
from 13/1327104 to 19/1769472 to 1007/84934656. Over the same levels the
whole k1 variance decreases. On the correctly marked warp the k2 variance
decreases instead. Refinement therefore has no single observed variance trend
shared by all coefficients and these two supplied geometries. Selection is
fresh on each level's eligible frame, not a coupled cross-level experiment.

Boost controls preserve all geometric, population, sample and moment fields.
Dilation scales degree-q coefficients by 4^q and covariance(q,r) by 4^(q+r);
pair measures scale by sixteen. The stale warp retains complete public sample
wires identical to the grid at each level, while its true geometric pair data
equal the correct warp. Marks are neither authenticated nor repaired.

## Scope and verification design

This is a private bounded research diagnostic, not a newly hardened production
API. It consumes authenticated AH source/design data for five supplied families,
three partition levels and 27 cases. Reuse of those fixtures is explicit.
Each of two independent engines recomputes their geometry, record-local chains,
all mask outcomes, moments and support accounting. The primary uses a directed
integral formula and centered covariance; the reference uses endpoint tiles
and second moments minus mean products.

The reference also supplies the independent read-only mathematical replay.
Shared orchestration checks controls and provenance; it is not a third
independent arithmetic implementation. Both observer helpers receive only
retained order/marks and the declared frame, probes and mask law, never hidden
cell geometry or absent weights. Geometric comparisons and full-design moments
remain source-aware audit data.

Before fixed execution, root's independent piecewise-linear integral check
passed 784 rational interval pairs through both engines in both normal and
optimized Python: 1,568 route comparisons per mode, each also checking
directed-complement and affine-scaling identities. Thirty-two synthetic
observer packets gave 64 route comparisons per mode, including singleton,
all-or-none and zero-weight internal-marker controls.

Both engines also passed their own synthetic geometry/support/covariance
checks. The test suite's 67 generic and temporary-lifecycle tests passed before
any fixed AI calculation, in normal and optimized Python (0.35s each in root's
final generic runs). The 34 fixed tests remained deselected at that point.
These tests include a separate literal case oracle, not another production
implementation or a claim of generic API resource hardening.

Prospective review strengthened the named transformation checks to cover
possibility flags and recomputed packet hashes alongside records and all
coefficient/moment fields. Complete AH sample projections also check marked
members, probabilities and hashes. All five protocol/implementation/test files
were frozen before the first fixed comparison. No fixture selection changed.

The first complete two-engine comparison passed in 29.47086212499562s.
All five current sources, 39 prior captures and fourteen AH/AG sources stayed
unchanged: 58 identity targets plus the current capture. Its mathematical suite
is 14,971,482 bytes, SHA256
`485090bd0e813fd4e34772b0bfdc14fba29eca6515299bcf3b6ed32108e1c377`.
There was no mathematical, implementation or fixture correction after that run.

The suite retains 405 coefficient questions, 738 full-source chain occurrences,
62,928 observed chain occurrences, 19,194 ordered supported chain-pair
occurrences and 1,152 zero-union-inclusion occurrences. The largest covariance
union has four eligible cells. Geometry retains all 6,705 ordered cell-pair
integrals across the repeated case/probe contexts, including diagonals and
zero clips. Of 4,032 mask rows, 953 are positive and 3,079 structural zeros.
These are bounded enumeration counts, not physical experiments.

A fresh reference-only read-only replay of the first capture passed in
21.31968929199502s. The exclusive external preflight passed in
29.67207766699721s; all its non-runtime fields equal the first capture.
Then all 101 frozen tests passed normally (90.60s) and optimized (90.78s),
including complete independent literal reconstructions of every case and
the suite controls/AH projections. Thirty nonvacuous corruption controls cover
eighteen finite-result fields, six suite fields and six historical projections.
Only the expected pytest optimization warning occurred.

The final capture was exclusively created in 29.752892249998695s. All its
non-runtime fields match the preflight and first capture. Final identity:

- Path: `results.json`.
- Bytes: 14,980,342.
- SHA256: `17dbb103c56b6489d5aef75f4eda77108fea12bfc475fc65ffcfd82710bf6786`.
- Isolated Python 3.11.6, macOS arm64, optimization off, separate external
  bytecode cache, both independent engines compared.
- Suite-end RSS high-water: 465,174,528 bytes. Runtime/RSS exclude final
  serialization and are not application-performance benchmarks.

Fresh read-only final replays passed through the primary in normal Python
(12.271955333002552s) and the independent reference in optimized Python
(21.348274792006123s). They preserve the complete mathematical suite and
capture bytes. The two replay processes ran concurrently, so the timings are
not a controlled engine-speed comparison. All 58 source/prior identities and
the final capture remained unchanged. The reference route imports no primary
engine; source/design fixture reuse and shared orchestration remain explicit.

Scientific review checked the reported fractions, refinement/support counts
and variance directions directly against retained JSON. No empirical,
apparatus, RET or new quantum-channel evidence is added. Ruff and formatting
checks pass for all four Python files; standard scoped whitespace checks pass.
Publication is limited to this gate and its research roadmap, excluding
unrelated RET/core/governance work and temporary model notes.

## Next question: additive cell-pair geometry across scales

Proposed QR-05AJ tests the supplied two-point causal measure as a coarse-grained
representation. On the same nested cells, compare each ordered parent-pair
integral with the complete sum of its child-pair integrals, including
within-child and same-parent cross-child terms. Compare adjacent-level and
direct two-level aggregation, with no new observation-law claim or additional
mask enumeration required.

Where both clipped volumes are positive, normalized causal fractions must
aggregate with product-volume weights, not unweighted averaging. Zero-volume
normalization is undefined and should remain explicit. Use geometric volumes,
not stale marks. Such fractions are conditional pair-causality statistics,
not automatically row-stochastic transitions or a strict event order.

Exact block sums would establish two-point measure consistency only. They do
not imply closure of matrix powers or longer-chain composition, whose
intermediate points are shared rather than independently redrawn. A nonzero
region diagonal means distinct causal points inside a region, not an event
preceding itself. The input still supplies geometry; no reconstruction,
quantum channel, continuum-limit or gravity claim follows. Freeze a detailed
AJ protocol before calculation. No AJ calculations have been performed.
