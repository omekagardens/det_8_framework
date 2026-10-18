# QR-05AP: bounded measurement-error stability

8 September 2026. Research after pushed AO commit
`a3286f68dd35be7d60b9abad6fc914dbbbd5af8f`.
The [prospective protocol](README.md) fixes the error coordinates, two inherited
decoders, complete witnesses and evidence lifecycle.

Status: both independent implementations, all 61 normal/optimized tests,
one independent reference-only audit and both final read-only replays PASS.
No source, protocol, fixture or mathematical correction followed the first
fixed calculation.

Main result: the geometric decoder has a much smaller worst-case amplification
over all coarse responses: 4 in both families, versus 535/6 for the canonical
grid decoder and 7313/50 for warp. Neither decoder has the smaller bound on
every row. This is an exact result for a declared dimensionless error box,
not calibrated sensor robustness.

## What was tested

AO's supplied geometry, weighted measurement matrix O, coarse response matrix Q
and two frozen decoders are authenticated INPUTS here. AP does not independently
reconstruct AO fields, integrate its responses, select a new row basis or fit
a new decoder. It rechecks both complete inherited identities on all generator
columns and transports their fixed linear maps.

Each family retains seven positive coarse cells, eight tiles, 32 weighted
observations, 64 source-generator columns and all 49 ordered coarse responses.
All 49 response normalizations are defined. The 64-column dictionary and exact
mixture-weight normalization remain AO's model; they are not quantum states.

The canonical compact map is padded with zero coefficients in omitted raw
measurement columns. Its normalization coefficient is a separate intercept.
The geometric map has no normalization term. All fixed intercepts happen
to be zero, but generic nonzero-intercept cases are verified.

## Error coordinates and exact bound

For EACH tile t with its own bounds [u0,u1,v0,v1], use
xi=(u-u0)/(u1-u0), eta=(v-v0)/(v1-v0), and

    z_t = integral_t F*(1,xi,eta,xi*eta) dmu / (V^2*h_t).

V is probe volume, h_t is tile volume, and dmu=du*dv/2.
For coarse response (C,D), use y_CD=U_CD/(V^2*h_C*h_D).
Thus the error coordinate units do not silently change under positive
affine axis scaling or translation. Empty generic response regions retain
zero normalization scales and null normalized targets, maps and bounds;
they are not zero-gain measurements.

The SAME frozen map becomes y_hat=b+B*z. Mixture normalization is exact,
so b receives no error. Under |delta_z_i|<=epsilon,

    |delta_y_j| <= epsilon*g_j,   g_j=sum_i |B_ji|.

Every bound is sharp: at epsilon=1, sign(B_j) attains the upper endpoint,
with sign(0)=0, and its negative attains the lower endpoint. Each retained
witness includes the full output-error vector B*sign(B_j), not only the selected
coordinate and not the prediction b+B*sign(B_j). A single error vector need
not attain every row's bound simultaneously.

This deterministic box does not assert random-error independence. Its points
need not be moments of any valid nonnegative field. There is no clipping,
projection, empirical probability, or supplied operational error tolerance.

## Complete fixed comparison

| Family | Canonical maximum gain | Geometric maximum gain | Canonical lower rows | Geometric lower rows | Tied rows |
| --- | --- | --- | --- | --- | --- |
| grid | 535/6 = 89.166666... | 4 | 6 | 4 | 39 |
| warp | 7313/50 = 146.26 | 4 | 6 | 4 | 39 |

Canonical reaches its maximum only at (C,D)=(8,9), zero-based row 41, in each family.
Geometric reaches 4 at ALL six diagonal rows
(1,1), (2,2), (3,3), (4,4), (6,6), (9,9).
The remaining diagonal (8,8) does not tie that maximum.

The ratios of the GLOBAL maxima are 535/24 (about 22.29) and
7313/200 (36.565). They are not same-row ratios: geometric gain at (8,9)
is 2, not 4. For illustration only, epsilon=1/1000 gives global normalized
response-error bounds 0.004 for geometric, about 0.089167 for canonical grid,
and 0.14626 for canonical warp. No evidence establishes that error budget
for a real apparatus or that these bounds meet an application tolerance.

All ten unequal row comparisons, separately in each family:

| Response (C,D) | Canonical grid | Geometric grid | Canonical warp | Geometric warp |
| --- | --- | --- | --- | --- |
| (1,1) | 1/16 | 4 | 1/16 | 4 |
| (1,2) | 1/4 | 2 | 1/4 | 2 |
| (1,3) | 1/4 | 2 | 1/4 | 2 |
| (1,4) | 1/4 | 2 | 1/4 | 2 |
| (1,6) | 1/4 | 2 | 1/4 | 2 |
| (4,4) | 1/2 | 4 | 1/2 | 4 |
| (3,3) | 19/3 | 4 | 19/3 | 4 |
| (6,6) | 83/12 | 4 | 83/12 | 4 |
| (8,8) | 323/24 | 5/2 | 375931/14400 | 61/24 |
| (8,9) | 535/6 | 2 | 7313/50 | 2 |

For example, canonical's bound at (1,1) is 1/64 of geometric's.
The 39 tied rows comprise 25 zero rows and 14 positive-gain rows; in these
fixed results all tied rows also have identical normalized maps. Every zero
target row has both maps zero. There are no fixed zero-gain/positive-alternate
rows. Equal noiseless targets do not imply equal off-model maps.

### A retained worst-case witness

For grid canonical response (8,9), the unit-box sign witness, grouped into
the eight tile-local blocks (1,xi,eta,xi*eta), is

    ( 1, 0, 0, 0)
    (-1, 1, 0, 1)
    (-1, 1,-1, 0)
    ( 1, 0,-1, 0)
    ( 0, 0, 0, 0)
    (-1, 1, 1,-1)
    ( 1,-1, 0, 0)
    ( 0, 0, 0, 0).

It attains 535/6 at (8,9). The same witness produces 323/24 at (8,8),
-1 at (2,2), and 1/16 at (1,1); all 49 error coordinates are retained
and checked. These signed ERROR values are not negative field weights.
Warp has a different map and witness: its second block is (-1,1,1,1),
and it attains 7313/50 at (8,9). The complete capture retains all 196
row witnesses, including zero rows and every maximum tie.

## Verification and accounting

Primary uses explicit triangular coordinate maps and row absolute sums.
Reference reconstructs each raw/local block from bilinear corner values,
inverts it independently, then evaluates the same raw affine map at zero
and each local unit vector. Independent coordinate-interval endpoints give
its sharp bounds; direct evaluation of each raw-map perturbation also checks
the complete witness output.

The test oracle uses polynomial binomial substitution and inverse substitution,
a separate cell/tile partition check, complete products and literal counts.
Exhaustive 4-/8-coordinate corner checks verify the sharp endpoints.
Generic affine tests transport the SAME dense policy, not a newly chosen
canonical decoder. They compare full geometry/transforms/maps/witnesses,
not merely the maximum. Fixed affine or partial-probe families were not run.

Useful generic anchors distinguish:

- a nonzero exact normalization intercept with zero error gain from a
  measurement-based map with gain 4 on the same one-generator model;
- unnormalized raw-output gain 2, normalized-output gain 32 under RAW unit
  errors, and normalized-output gain 4 under LOCAL unit errors;
- null response rows from supported zero-gain rows, retaining nonzero raw
  rows that cancel on the model;
- smaller worst-case gain from smaller error for every perturbation;
- exact tiny coefficients from zero, intermediate cancellation from
  retained overflow, and online application from hidden model access.

All **61 tests** pass normally and under -O, both in 16.22 seconds.
Final pre-freeze repetitions passed 52 generic tests, nine fixed deselected,
in 1.61 and 1.59 seconds. The sole optimized warning is pytest's expected
notice about non-rewritten assertions; admission guards use explicit exceptions.

The nine fixed tests comprise two independent complete-family comparisons,
one complete suite/payload/selected-input comparison, three cached routing
checks, one family/suite mutation group, one selected-producer mutation group,
and one source/prior inventory check. Cached routing tests are not additional
independent mathematical implementations.

There are 102 rejected non-noop mathematical comparisons:
31 generic family/null mutations, 54 fixed family mutations, eight suite
mutations and nine selected AO producer mutations. These mostly test complete
wire comparison, not a standalone production semantic verifier. One additional
unselected AO field-target mutation is intentionally invisible to the projection
helper, while full-file authentication would still reject a changed artifact.

Isolated normal/-O subprocesses each retain 166 explicit ValueError rejections:
two engines times (58 malformed families + 24 malformed applications +
one retained application overflow). Shared native inputs, detached outputs,
restricted apply, maximum application dimensions, source changes, capture
caps, symlinks and read-only/create-only behavior are also checked.
Hostile-object/resource and production API hardening remain incomplete.

Root's independent hand checks cover six complete synthetic base families and
their affine partners per engine, normally and optimized: 24 builds per mode.
They check every transported map, full witness output and maximum tie, plus
small-box corner extrema. A separate compact-padding translated-tile hand
checks mixed formerly omitted coordinates and exact gain 35/3.
Primary's own hand suite covers 20 complete synthetic wires per mode;
reference's covers three base plus three affine wires per mode.

Across both fixed families:

| Retained quantity | Entries |
| --- | --- |
| Raw/local transform coefficients, both directions | 512 |
| Dimensionless observation map | 4,096 |
| Dimensionless target map | 6,272 |
| Dense raw decoder coefficients, including intercepts | 6,468 |
| Normalized decoder coefficients, including intercepts | 6,468 |
| Row gains / complete witnesses | 196 / 196 |
| Witness signs | 6,272 |
| Rational witness-output entries | 9,604 |
| Maximum-row indices, across both decoders/families | 14 |

These are repeated serialized occurrences, not independent information or
a compressed sensing claim.

| Family | Input bytes | Geometry bytes | Coordinate bytes | Decoder bytes | Comparison bytes | Full family bytes |
| --- | --- | --- | --- | --- | --- | --- |
| grid | 52,206 | 1,737 | 34,980 | 79,525 | 552 | 169,723 |
| warp | 55,261 | 1,804 | 36,747 | 80,065 | 560 | 175,160 |

Scopes are canonical protocol projections, including a newline. They overlap
and omit separate diagnostics; they are not additive unique storage or online
packet costs. Fixed model/geometry/map data are separate from each incoming
32-value measurement vector.

## Evidence lifecycle

Five AP sources, 46 prior captures and 49 ancestor sources give 100 distinct
authenticated targets. The five AP sources were fully read, independently reviewed,
generically tested and frozen before the first fixed AP calculation.

Before freeze, a draft TEST oracle used the probe's origin/width for every
tile. It was corrected to each tile's own coordinates, and the protocol
wording was made explicit. Both engines already used per-tile coordinates.
A second test-only clarification compared raw/local noise in the same output
units (32 versus 4), retaining raw-output gain 2 with its proper units.
Formatting was completed before freeze. No fixed outcome or engine formula
was changed; no source/protocol/fixture/mathematical correction followed first capture.

The first comparison, exactly one independent fresh normal reference-only
audit (2.653185 seconds), external create-only preflight and final exclusive
capture agree on EVERY non-runtime field, including complete mathematics
and ledgers. Final read-only replays also agree.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 361,275 | 3.368866 |
| External preflight | 361,280 | 3.059937 |
| Final retained capture | 361,276 | 3.164151 |

All contain the same 346,502-byte canonical suite.

    First SHA256:     876a22c5cdf61ba6fb78c32d57496ee301011bb43f184329b99a81b0efb49245
    Preflight SHA256: 17a8d41872148d3242bd11513bfce93419487fddb79e930343d86918ba7785c5
    Final SHA256:     823d9f5a5511853fe3dbff800f1a6561db985021002c24ec2beb0c55199ba048
    Suite SHA256:     076b2135a4de7037d4c00ec5293b9ce6733d448ae0eb68cc7b3bf294b4795313

Fresh final replays: primary normal 0.647469 seconds; reference -O
2.706724 seconds. All 100 identities and final bytes remain unchanged.
Full tests/audit overlapped; final replays ran concurrently. Timings exclude
final serialization and are verification observations, not application
benchmarks or implementation rankings. Runtime: isolated Python 3.11.6,
macOS arm64, fresh external bytecode caches.

The [retained capture](results.json) is the repository artifact; first and
preflight captures remain external working evidence. From the repository root:

```sh
qr05ap_cache=$(mktemp -d /tmp/det8-qr05ap-replay-XXXXXX)
.venv/bin/python -I -X "pycache_prefix=$qr05ap_cache" \
  docs/validation/qr-05ap-measurement-stability-2026-09-08/study.py --verify --route primary

qr05ap_opt_cache=$(mktemp -d /tmp/det8-qr05ap-replay-opt-XXXXXX)
.venv/bin/python -I -O -X "pycache_prefix=$qr05ap_opt_cache" \
  docs/validation/qr-05ap-measurement-stability-2026-09-08/study.py --verify --route reference
```

## Applicable value and next gate

Exact model reconstruction and stable response evaluation are different
requirements. For this full-response box-error criterion, the inherited
geometric map is a better worst-case choice. For selected rows the canonical
map can have a smaller bound. The research now supplies explicit amplification
budgets and attaining witnesses for deciding which contract an application
actually needs; it has not selected or calibrated a physical sensor.

A useful next question is QR-05AQ: frozen-decoder SOURCE-SPAN portability.
Keep AO's geometry, four-moment observation interface and two coarse-response
maps fixed; test nonnegative, fine-tile-supported tensor Bernstein
biquadratics with amplitude V^2. This alternative source family has a larger
piecewise-polynomial span; no claim that its normalized convex hull contains
AO's entire original mixture family is required.

Independently compute all new measurements and responses, retain all signed
frozen-map residuals and any single-generator counterexample. The geometric
map is the structural control: its bilinear outgoing test functions make
coarse responses depend on the four moments without requiring AO's particular
source span. A canonical policy failure would therefore be model-portability
failure, not proof that those measurements are insufficient.

The detailed AQ protocol, dictionary, boundaries, ordering and audit must be
frozen before calculation; none has been performed. No refitting, new degree
gate, old chain-sum normalization for the new dictionary, full-field recovery
extension, physical source preparation, unknown geometry, quantum channel,
gravity derivation, RET integration or Lean verification is established here.
