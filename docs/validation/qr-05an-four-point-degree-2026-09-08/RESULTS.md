# QR-05AN: degree-aware four-point composition

8 September 2026. Research after pushed AM commit
`0e65df824a7e19d5b6420036d5e98f5a6073d81a`.
The [prospective protocol](README.md) fixes the input projection, degree-aware
representation, two controls and full verification sequence before fixed runs.

Status: exact fixed comparisons, all 66 normal/optimized tests, independent
reference audit and final read-only replays passed without a post-first correction.

## What the additional integration changes

The two intermediate points must remain coupled by their causal order:

    F_AB(z) = integral_B L_A(y) 1[y precedes z] dmu(y),
    U_ABCD = integral_C F_AB(z) R_D(z) dmu(z).

The first operation propagates the incoming volume through B. On a complete
rectangular breakpoint grid, F has degree at most two in each coordinate.
Multiplying by a bilinear outgoing volume requires moments through degree
three in each coordinate: sixteen raw entries in this sufficient declared
tensor contract. It does not follow that any fixed degree works for arbitrarily
many integrations, or that these sixteen entries are independent or minimal.

The representation is factored. Geometry/moments are stored once per third-region
tile; exact and forced propagated coefficients once per (A,B,tile); outgoing
coefficients once per (D,tile). Quadruple rows retain the complete scalar
diagnostics. All coefficients use the same global coordinate basis.

The primary derives branch polynomials and contracts antiderivative moments.
The independent reference interpolates coefficients from ordered-pair volumes,
uses exact tensor-Simpson moments and checks against ordered-atom simplex
integration for two, three and four continuum points. Repeated region labels
do not identify their points or prohibit strict ordering within that region.

## Two distinct approximation controls

The forced control replaces F by its four-corner bilinear interpolant on
each tile. This is not deletion of higher global-coordinate monomials, which
would not transport properly under translation. On the prescribed complete
grid, the nonnegative one-dimensional branch factors are constant, affine or
convex quadratic. Their secants majorize them, giving forced_U >= U.
This sign bound was specified before the fixed run, not selected from its results;
it does not cover arbitrary fields or grids missing saturation breakpoints.

A separate mean-only control uses P=(integral_C F)(integral_C R)/volume(C).
Its missing term is the integral of the centered product at the same z:
centered_integral=U-P and third_covariance=(U-P)/volume(C). Both engines
actually integrate centered functions, not just rename a subtraction.
The covariance has volume degree three; the centered integral has degree four.

These are distinct approximations even when symmetry makes their values
coincide. Nor does equality of a weighted integral certify a bilinear field
when outgoing support hides nonlinear tiles. Field admission uses coefficients,
not answer equality. Zero third-region denominators stay undefined; zero
endpoints with a positive third region retain valid raw zero products.

## Generic analytic anchor

For A=B=C=D=[0,1]^2 with dmu=du dv/2, F=u^2 v^2/16 and
R=(1-u)(1-v)/2. Exact U=1/9216, with normalized value 1/576.
The corner-bilinear forced F=uv/16 gives U=1/2304, normalized 1/144,
and forced-minus-exact error 1/3072. The mean-only control happens to give
the same 1/2304 here; the centered integral is -1/3072 and covariance -1/1536.

The highest mixed moment is M33=1/32 and contributes +M33/32 to this
contraction. Omitting only that entry produces -1/1152, not the true positive
answer. This is a failure of that deletion, not a proof of minimal encoding.

If the unit region is split vertically into equal left/right children,
all sixteen ordered child quadruples must remain in its additive block.
The five positive orders LLLL, LLLR, LLRR, LRRR, RRRR contribute respectively
1/147456, 1/36864, 1/24576, 1/36864, 1/147456, summing to 1/9216.
Keeping only identical-child quadruples gives 1/73728 and loses seven eighths
of the measure. Cross-child combinations cannot be discarded by treating
cell IDs as individual continuum points.

## Complete fixed results

The fixed scope projects only AM's original grid/warp whole-probe geometry,
with 6, 7 and 8 region IDs at l0, l1 and l2. No AM moments, endpoint queries,
coefficients or answers enter the engines. Both routes agree on every one of
298 pair rows, 2,142 triple rows and 15,586 quadruple rows. Both probes have
volume 1/2. At all six level/family contexts the complete partition sums are
J=1/16, T=1/288 and U=1/9216, independently matching V^2/4, V^3/36 and V^4/576.

| Four-point diagnostic | Count |
| --- | --- |
| Positive exact U | 804 |
| Zero exact U | 14,782 |
| Forced error positive / zero / negative | 612 / 14,974 / 0 |
| Mean error positive / zero / negative | 562 / 15,024 / 0 |
| Positive U with a bilinear propagated field | 192 |
| Positive U with a nonbilinear propagated field | 612 |
| Nonbilinear field with forced equality | 1,080 |
| Undefined full conditionals / empty third regions | 0 / 0 |

All 192 positive bilinear rows are forced-exact. Of the 804 positive rows,
the mean control is exact on 242 and overestimates 562. All 1,080 nonlinear
forced equalities have U=0; none is evidence of bilinear admission. Neither
control creates false-positive support in these fixed families. Empty clips
and undefined denominators are covered by generic tests, not this reduced
whole-probe inventory. Mean-error signs here are fixed observations, not a
claimed theorem about general causal fields.

Comparing absolute errors over ALL 15,586 rows, forced is better on 289,
mean-only on 254, and they tie on 15,043, including zero rows. Neither
approximation uniformly dominates the other query by query. Each family
has 402 positive quadruples and the same structural error counts, but their
rational measures, aggregate errors and control rankings need not coincide.

### Fixed witnesses

In grid, l0, the four distinct regions (A,B,C,D)=(1,2,5,8) give
U=1/248832, forced_U=1/165888, and P=U. The forced error is 1/497664,
while centered integral and covariance are zero. The propagated field is
not bilinear. Thus losing field degree can introduce error even when the
separate mean-product control is exact.

The same context reverses the comparison elsewhere:

| Regions (A,B,C,D) | Exact U | Forced U | Mean P |
| --- | --- | --- | --- |
| (1,2,2,2) | 1/2985984 | 1/1492992 | 1/995328 |
| (1,1,1,2) | 1/2985984 | 1/995328 | 1/1492992 |
| (1,1,7,7) | 1/331776 | 1/331776 | 1/331776 |
| (1,1,2,1) | 0 | 0 | 0 |

The first two rows favor opposite controls. The third has a positive bilinear
field response; the fourth has a nonbilinear field but zero outgoing-weighted
response. They must not be assigned the same structural admission merely
because both controls agree in the last two rows.

### Refinement and aggregate errors

All 38 whole-middle moment blocks preserve every one of sixteen raw moments.
The 1,550 propagated-field blocks contain 2,616 fine-tile pieces; all nine
coarse coefficients agree entrywise with the complete child-(a,b) sums in
the global basis. All 9,986 true quadruple blocks agree with their 21,186
child tuples; every one of the 2,592 direct l0->l2 blocks also agrees through
l1. These are exact supplied-geometry refinement identities.

The controls do not share that additivity. Summing fine forced values over
each true block decreases its coarse forced value in 224 blocks and leaves
9,762 unchanged. Fine mean products decrease in 42 and stay unchanged in
9,944. Neither increases here. These counts include all three links in both
families, so direct and adjacent comparisons are not independent observations.

All six context-level errors remain strictly positive:

| Family / level | Aggregate forced-minus-exact | Aggregate mean-minus-exact |
| --- | --- | --- |
| grid l0 | 7/165888 | 7/165888 |
| grid l1 | 17/442368 | 109/2654208 |
| grid l2 | 155/7077888 | 5099/127401984 |
| warp l0 | 19145/322486272 | 32971/322486272 |
| warp l1 | 368795/6879707136 | 2811157/27518828544 |
| warp l2 | 91065647/1761205026816 | 2158772401/21134460321792 |

The fixed decrease is not a continuum-limit result, a convergence rate or
a universal monotonicity statement for arbitrary approximations.

## Representation costs and coordinate boundary

The fixed contract has 42 positive middle regions, 52 tiles and 178 breakpoint
entries. Whole-middle moments contain 672 entries and tile moments 832.
Positive middle bounds add 168 coordinate entries; tile bounds add 208.
Input cell/probe geometry and the complete result rows remain separately present.

| Retained vectors / witnesses | Rational-pair entries |
| --- | --- |
| 2,752 propagated nine-entry vectors | 24,768 |
| 2,752 forced four-entry vectors | 11,008 |
| 376 outgoing four-entry vectors | 1,504 |
| 38 coarse/child-sum moment blocks | 1,216 |
| 2,616 coarse/child-sum field pieces | 47,088 |

There are 266 nonbilinear tile-field vectors. Field-piece checks refer to
3,856 implied child-(a,b) terms; these are not extra serialized vectors.
The 20,368 quadruple-tile visits count logical contract work, not processor
instructions. Entries include zeros, signed coefficients and repeated values.

| Family | Moment/field contract bytes | Coarsening witness bytes | Full family bytes |
| --- | --- | --- | --- |
| grid | 256,955 | 1,084,209 | 4,155,539 |
| warp | 260,832 | 1,088,794 | 4,207,797 |
| Total of separate canonical projections | 517,787 | 2,173,003 | 8,363,336 |

The protocol defines each byte projection completely. These scopes overlap,
retain redundant evidence and are not additive unique storage costs, a
compression ratio or a minimal wire. Sixteen raw moments are a sufficient
tensor vocabulary here, not sixteen independent geometric parameters.

Full affine transport is verified in generic families, including translation,
unequal positive axis scaling, all bounds, raw binomial moments, field
coefficient pullbacks, field/moment/quadruple blocks, scalars, flags and nulls.
Fixed boost, dilation, stale and partial-probe families were deliberately
not executed. AN derives its own sixteen moments from supplied geometry;
it does not claim to reuse AM's nine-moment snapshots. All selected AM input
IDs, bounds, levels and probe bounds match. Other AM data and older mathematics
are identity-only, not historically replayed calculations.

## Verification and evidence lifecycle

The protocol and four Python sources were reviewed and frozen before fixed
computation. All 88 distinct targets remain authenticated: five AN sources,
44 prior captures and 39 ancestor sources. No source, formula, fixed input
or protocol correction followed the first fixed calculation.

Before freeze, the protocol clarified that the public rectangle_moments helper
accepts only positive rectangles, not None. Reference's public guard/docstring
was aligned; its internal empty-clip zeros and admitted-geometry mathematics
were unchanged. The generic malformed-input check was updated and both engine
owners and root reran their checks. A separate wording clarification avoided
suggesting that positive-U nonlinear forced equalities had been established.
Initial test syntax/unused-local and lint/format cleanups were also pre-freeze.

All **66 tests** pass normally (68.81 seconds) and under -O (68.84 seconds).
The only optimized warning is pytest's expected notice about ordinary
non-rewritten assertions; engine guards use explicit exceptions.
Root's final pre-freeze repetitions passed 56 tests, with ten fixed tests
deselected, in 9.24 and 9.23 seconds.

The ten fixed tests comprise two complete independent family-oracle comparisons,
one complete suite/payload/partition/selected-AM comparison, three cached
orchestration routes, three mutation groups and one source/prior inventory.
The test oracle uses independent cumulative piecewise-polynomial prefix
integration for ordered volumes, moment formulas, interior field values,
all result fields, nulls and complete refinement witnesses.
Cached dispatch tests isolate orchestration, not extra independent integrations.

The 44 non-noop corruptions comprise 28 family-wire changes, nine suite/control
changes (six wire mutations and three direct controls), and seven selected-AM
projection mutations. Complete exact-wire comparisons are not a standalone
semantic validator for arbitrary imported geometry. Explicit subprocess checks
retain 54 ValueError rejections per normal/optimized mode: two engines, each
with 18 malformed builds and nine malformed rectangle-helper inputs.
Detachment, valid shared input containers, retained-integer overflow, evidence
caps, exclusive capture, symlink rejection and read-only replay are also tested.
This remains a bounded private diagnostic, not comprehensive hostile-resource
hardening.

Root's separate generic checker compares both engines in normal and optimized
Python on unequal 1->2->4 partitions with three whole/partial/corner probes.
Each build checks all 63 pairs, 219 triples and 819 quadruples, including
200 empty-third rows, 66 nonlinear forced equalities and 14 positive bilinear
responses. It checks 2,079 interior field values and 70 field pieces, and
repeats the entire family after u'=2u+3, v'=3v-5.
A separate normal-Python hand check compares 400 signed one-dimensional
interval chains against an ordered-atom simplex oracle. Engine owners also
ran independent synthetic suites. No generic hand is presented as a fixed
grid/warp result.

The first external comparison took 13.418780 seconds. Exactly one independent
fresh normal-Python reference-only read-only audit reproduced it in 8.853743
seconds, preserving the first artifact and all 88 identities. External
create-only preflight and final exclusive capture agree with the first run
on EVERY non-runtime envelope field, including all ledgers and the suite.

Fresh read-only final replays pass: primary in normal Python, 5.697882 seconds;
reference under -O, 8.877761 seconds. Both preserve final bytes and all
88 identities before and after. Full test modes and the independent audit
overlapped; final replays ran concurrently. Timings are verification observations,
not application benchmarks or rankings of implementations.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 8,378,523 | 13.418780 |
| External preflight | 8,378,527 | 13.565157 |
| Final retained capture | 8,378,531 | 13.481201 |

All three contain the same 8,365,472-byte canonical mathematical suite.
Capture differences are runtime metadata, not altered mathematics or ledgers.

    First SHA256:     2a07eac131c5b16afa69b3ce77f71a04b662be5a744bf4738078cf6bcba09bd8
    Preflight SHA256: 02dc1a8baf685ee33df37806b35263c65f5014b750868dfb3c3f7ba2e2332c70
    Final SHA256:     a455f43f65dea9da33692cd256fad942e2d21d0bfed9f54a0deed163ff5bd9c1
    Suite SHA256:     6f8dfd8af28e24f1ec40049163ce2c2adc17870172e1adbb6ac0762417fb2786

The [retained capture](results.json) is the repository evidence; first/preflight
files remain external working evidence. Runtime is isolated Python 3.11.6 on
macOS arm64 with fresh external bytecode caches. Suite timings exclude final
serialization. Read-only reproduction from the repository root:

```sh
qr05an_cache=$(mktemp -d /tmp/det8-qr05an-replay-XXXXXX)
.venv/bin/python -I -X "pycache_prefix=$qr05an_cache" \
  docs/validation/qr-05an-four-point-degree-2026-09-08/study.py --verify --route primary

qr05an_opt_cache=$(mktemp -d /tmp/det8-qr05an-replay-opt-XXXXXX)
.venv/bin/python -I -O -X "pycache_prefix=$qr05an_opt_cache" \
  docs/validation/qr-05an-four-point-degree-2026-09-08/study.py --verify --route reference
```

## Applicable value and next boundary

This gives an exact degree-aware representation for a specified two-middle
causal response on supplied geometry. It identifies what the outgoing query
needs from the incoming field, preserves that dependence across refinement,
and distinguishes two approximations that can fail differently. Those are
useful ingredients for geometric response calculations and later operator
interfaces, without requiring an ontological commitment.

The next proposed gate, QR-05AO, asks which coarse measurements of a field
preserve a declared family of geometric responses. Rather than add another
integration degree, compare coarse-tile field means with four weighted field
moments, integral_tile F*(1,u,v,uv). These are measurements OF THE FIELD,
not the geometry-only moments M_ij already supplied here.

Make the new information restriction explicit: an unknown convex mixture of
fine F_ab generators is available only through those measurements and its
known normalization. Keep geometry and the decoder public, but do not let the
decoder use the mixture weights or full fine field. Test exact recovery of
coarse responses and separately test finer responses; retain constructive
decoders or admissible equal-measurement/unequal-response witnesses. Outcomes,
ranks and collisions are not assumed in advance. The detailed AO protocol
must be frozen before any fixed AO computation.

AN's retained geometry and known region IDs still determine its fields, so
AN itself proves no irreversible loss of that full record. No empirical
observations, unknown-geometry reconstruction, minimal representation,
universal finite-degree closure, continuum limit, quantum channel, gravitational
dynamics, ontology validation, RET integration or Lean verification is established.
