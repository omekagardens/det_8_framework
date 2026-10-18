# QR-05AO: response-preserving coarse field measurements

8 September 2026. Research after pushed AN commit
`8ed22a74c2dd6a576f862daf6e07e584d3c9567b`.
The [prospective protocol](README.md) specifies the unknown-mixture family,
measurement access, exact response targets and evidence lifecycle.

Status: both independent implementations, all 75 normal/optimized tests,
independent reference audit and final read-only replays passed. No post-first
source, protocol, fixture or mathematical correction was needed.

Main result: in BOTH fixed families, weighted coarse measurements recover
the entire declared fine field, not merely the coarse responses. Tile integrals
alone fail all three targets. This is exact recovery within the supplied
generator span, not arbitrary fields or noisy-measurement robustness.

## What is observed, and what is hidden

The supplied geometry and its fine causal fields F_ab form a public dictionary.
An unknown field is a convex mixture F_lambda=sum lambda_ab F_ab, with
nonnegative coefficients summing to one. This normalizes the mixture weights,
not its field integral and not a quantum state.

The online interface receives either one integral per coarse tile or four
weighted field integrals, integral F*(1,u,v,uv). These measurements contain
information about the field; geometry-only moments used to compute them are
different data. Geometry and certified decoder coefficients remain public.
The mixture weights and complete fine field do not enter the online call.

The three targets are all declared coarse responses, all finer responses,
and the full piecewise field on positive fine tiles. Even exact field recovery
need not identify mixture weights when generator columns are dependent.
The offline artifact retains the full matrices and field dictionary, so an
interface-level information loss is not loss of that complete artifact.

## Exact certificates, not selected examples alone

For raw measurement matrix O, augment A=[1^T;O]. A complete target Q is
recoverable for every convex mixture exactly when ker(A) is contained in
ker(Q), equivalently rank([A;Q])=rank(A). A passing certificate gives
Q=D*A[row_basis,:], with D in the lexicographically first independent original
observation rows. Every target row and generator column is checked.

A failure supplies a canonical zero-sum direction w invisible to all
observations but visible to Q. Its positive and negative parts, each divided
by their equal positive mass, give two normalized nonnegative mixtures.
Their full observation vectors agree and their target vectors differ.
A signed null vector without normalization would not establish that admissible
collision. Selection is first detecting free column, then first separating
target row; normalized target differences are distinct from Q*w.

Four weighted field moments per tile constructively recover coarse outgoing
responses because those test functions are bilinear on the shared coarse grid.
The incoming field itself need not be bilinear there. The direct geometric
decoder G satisfies Q_coarse=G*O_weighted without a normalization term.
Fine/full-field recovery is a separate finite-span calculation, not a consequence
of that geometric coarse-response argument alone.

The public decode function only applies the supplied compact linear map to
measurements and known normalization. It does not authenticate the semantics
of an arbitrary externally supplied decoder. Offline certificate verification
and trusted model/provenance remain necessary.

## Complete fixed recovery results

Grid and warp each retain seven coarse cells, eight fine cells, eight coarse
tiles and twelve fine tiles, with the original AN IDs and coordinates.
Each dictionary has 64 ordered generators. The targets have 49 coarse response
rows, 64 fine response rows and 108 fine coefficient rows. The full coefficient
matrix S has rank 23 in each family.

The following complete certificate table holds separately for grid and warp:

| Observations | Raw rows | Rank with normalization | Target | Target rank | Joint rank | Recovery |
| --- | --- | --- | --- | --- | --- | --- |
| Tile integrals | 8 | 9 | Coarse responses | 14 | 20 | No |
| Tile integrals | 8 | 9 | Fine responses | 15 | 21 | No |
| Tile integrals | 8 | 9 | Full fine field | 23 | 24 | No |
| Weighted field moments | 32 | 24 | Coarse responses | 14 | 24 | Yes |
| Weighted field moments | 32 | 24 | Fine responses | 15 | 24 | Yes |
| Weighted field moments | 32 | 24 | Full fine field | 23 | 24 | Yes |

All six failed certificates retain admissible mixture collisions; all six
successful certificates retain complete exact decoders. No failed case was
discarded, and the unexpectedly strong full-field recovery was not replaced
with a presumed information-loss conclusion.

### Why 64 generators do not mean 64 independent fields

Each family has 33 identically zero field-generator columns and 31 nonzero
columns, with dependencies among the latter. The field space has dimension
23. Because weighted observations are linear functions of S, their raw rank
is at most 23. Their augmented rank is 24, so the raw rank is at least 23:
it is exactly 23. This deduction is also supported by reconstructing every
weighted matrix row from the retained fine moments and S.

Normalization supplies the extra independent row: it is one even at a zero
field generator. All successful canonical decoder normalization coefficients
are zero in these fixed cases. The basis lists select 23 raw measurement rows
plus normalization; those 23 measurements suffice for these targets on this
span. The public interface still takes the declared 32-entry measurement
vector; no new 23-value packet codec or universal minimum is claimed.

The 64 weights have 40 normalized invisible linear directions because the
augmented observation rank is 24. That is not 40 lost field directions:
S annihilates them. Distinct mixtures can yield the same field. Conversely,
equal tile integrals can conceal genuinely different fields and responses.

### A retained grid collision

The integral-only coarse, fine and field certificates choose the same pair:

    F_plus = (F_1,7 + F_1,9)/26 + 12*F_2,2/13,
    F_minus = (F_1,2 + F_1,3 + F_1,4)/13 + F_1,10/52 + 3*F_2,1/4.

All eight weights shown are nonnegative and each mixture's weights sum to one.
F_2,1 is an identically zero field, but its mixture weight still counts toward
normalization. All eight coarse tile integrals agree exactly:

    (0, 1/1078272, 1/359424, 0,
     1/134784, 1/359424, 1/119808, 1/39936).

Yet the responses differ:

| Separating target | F_plus | F_minus | Difference |
| --- | --- | --- | --- |
| Coarse (C,D)=(2,2) | 11/3312451584 | 1/310542336 | 1/9937354752 |
| Fine (c,d)=(2,2) | 1/3312451584 | 1/4968677376 | 1/9937354752 |
| Fine tile 2, coefficient of v^2 | 1/156 | -1/936 | 7/936 |

Coarse and fine IDs are level-local; the two (2,2) rows have different
geometric regions. The negative polynomial coefficient is not a negative
field or mixture weight. Fine tile indices are zero-based global indices.

Warp has its own retained rational mixture weights and target differences;
equal ranks and support patterns do not make its numerical collision identical
to grid. The full observation and target vectors, not only these selected
components, are checked and retained.

## Geometry, representation and historical boundary

The engines derive field measurements by summing exact fine-piece integrations,
not by fitting the field onto coarse tiles. All fine-tile owners, four weighted
observation sums, complete child-(c,d) response sums and direct geometric
decoder identities pass. Each family's complete unweighted response sum is
1/9216=V^4/576, with V=1/2. This sums weight one over all 64 generators;
it is not the response of a normalized uniform mixture.

Across the two families:

| Retained quantity | Entries |
| --- | --- |
| Whole input / clipped-cell / tile bounds | 128 / 120 / 160 |
| Coarse / fine geometry moments | 256 / 384 |
| Coarse / fine outgoing coefficients | 448 / 768 |
| Two coarse observation maps | 5,120 |
| Fine weighted verification map | 6,144 |
| Three target maps | 28,288 |
| Direct geometric decoders | 3,136 |
| Successful compact canonical decoders | 10,608 |
| Failed-certificate rational vectors | 2,574 |

The 128 generator count is two occurrences of a 64-column dictionary, not
128 independent physical or mathematical field dimensions. Basis-index and
pivot-index lists each contain 198 entries across repeated certificates.
All matrices retain zero/signed entries and redundant verification witnesses.

| Family | Geometry bytes | Measurement-map bytes | Target-map bytes | Geometric decoder bytes | Certificate bytes | Full family bytes |
| --- | --- | --- | --- | --- | --- | --- |
| grid | 14,135 | 20,328 | 93,903 | 9,553 | 49,233 | 210,096 |
| warp | 15,328 | 22,635 | 96,349 | 9,569 | 56,363 | 225,647 |
| Sum of separate canonical projections | 29,463 | 42,963 | 190,252 | 19,122 | 105,596 | 435,743 |

These protocol-defined byte scopes overlap and omit separate diagnostics.
They are not additive unique storage or a compressed online packet.
Each online unknown field contributes eight or 32 raw measurement values;
the fixed dictionary, geometry and decoder costs must remain separately visible.

Both engines receive ONLY the selected AN input geometry. Afterwards, the
runner verifies all selected fine synthesis coefficients against AN's retained
l2 tiles and all 8,192 selected fine four-point answers across grid/warp.
Flat-tile bounds, event IDs, generator order and exponent labels are compared.
No AN answer enters engine inputs, and no historical executor runs.
Other AN mathematics and older calculations remain identity-only.

Generic checks verify complete positive affine coordinate transport: geometry
moments obey Jacobian-weighted binomial transport; weighted field moments
combine volume degree three with coordinate-basis mixing. Responses have
volume degree four, and field coefficients pull back with degree two.
Translation mixes weighted rows. Certificate validity is checked after independent
recertification, not by incorrectly assuming a coordinate-dependent canonical
decoder is unchanged. No fixed transformed or partial-probe family was run.

## Generic anchors and verification

Normalization matters: O=[0,1], Q=[1,2] is recovered as Q=1^T+O.
For O=[0,1,2], Q=[0,0,1], the standard null difference (1,-2,1)
gives mixtures (1/2,0,1/2) and (0,1,0), equal measurement one, and responses
1/2 versus zero. Dividing by the entire absolute sum would subnormalize them.

With synthesis columns (1,0), (0,1), (1/2,1/2), one measured first component
plus normalization recovers the whole field but not individual weights.
This explicitly tests field recovery rather than silently using identity
on generator weights as the target.

For one unit-square generator F=u^2*v^2/16, the four field moments are
(1/288,1/384,1/384,1/512), not the geometry volume 1/2.
The geometric decoder (1,-1,-1,1)/2 recovers U=1/9216.
Other synthetic families retain real field collisions and empty clipped
generators; their outcomes are not promoted to the fixed grid/warp result.

All **75 tests** pass normally (33.13 seconds) and under -O (33.09 seconds).
The final pre-freeze generic repetitions passed 65 tests, with ten fixed tests
deselected, in 3.97 and 3.99 seconds. The sole optimized warning is pytest's
expected notice about ordinary non-rewritten assertions; public guards use
explicit exceptions.

The ten fixed tests comprise two complete independent family-oracle comparisons,
one complete suite/payload/selected-AN comparison, three cached orchestration
routes, three mutation groups and one source/prior inventory check.
Cached dispatch tests isolate routing, not additional independent integrations.

The independent test oracle uses cumulative prefix-polynomial ordered integrals,
interior interpolation and polynomial convolution. Exact orthogonal residuals
supply ranks, canonical row/column bases, decoders and collision certificates
independently of either engine's elimination. All geometry, matrix, certificate,
count and payload fields are compared, including transformed complete families.

The 57 non-noop corruptions comprise 16 generic semantic certificate/collision
checks, 22 fixed family-wire changes, nine suite/control changes and ten
selected-AN geometry/coefficient/answer mutations. Generic semantic checks
exercise the test oracle; most fixed corruptions exercise complete exact-wire
comparison, not a standalone production semantic verifier. Explicit normal/-O
subprocess guards retain 92 ValueError rejections per mode:
two engines, each with 16 family, 14 matrix and 16 decode malformed inputs.
Restricted online access, detachment, exact tiny ranks, retained-versus-internal
integer bounds, source changes, capture caps and exclusive/read-only behavior
are also tested. Hostile-object/resource hardening remains incomplete.

Root's separate determinant/Cramer oracle checks 39 abstract matrix cases
per engine per Python mode. It also checks six complete synthetic families
(three geometries before/after unequal positive scaling and signed translation),
using independent ordered-prefix integrals, central-moment formulas and
interior field values. Each route/mode checks 36 geometric certificates,
2,088 field-node values, 136 coarse-response entries and 1,186 fine-response
entries, including empty clips. Engine owners additionally ran their own
normal/optimized independent hand suites.

## Evidence lifecycle

All 94 distinct targets remain authenticated: five AO sources, 45 prior
captures and 44 ancestor sources. The protocol and four Python sources were
reviewed and frozen before fixed AO mathematics.

Before freeze, validation order was aligned so full parenthood and child
coverage are checked before probe coverage clipping. Reference's guard block
was moved after source review and all generic checks were repeated; admitted
mathematical outputs were unchanged. Formatting, documentation spacing and
a declared decode-basis cap test were also completed before freeze.
No source, formula, fixed input or protocol correction followed the first run.

The first comparison, exactly one independent fresh normal reference-only
audit (7.170720 seconds), external create-only preflight and final exclusive
capture agree. All non-runtime envelope fields, including the complete
mathematical suite and source ledgers, match across captures.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 451,691 | 8.798310 |
| External preflight | 451,694 | 8.648914 |
| Final retained capture | 451,698 | 8.618880 |

All three contain the same 437,783-byte canonical mathematical suite.

    First SHA256:     020474d682fc784f14859759d2fcbc5d336eec2a8762689e71716a2833d56ccc
    Preflight SHA256: 64b30097ca50ccc84ae5ecf3c2d6e39a7609ba6c993ada958f4e671283333b60
    Final SHA256:     55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1
    Suite SHA256:     ddd703e8e4b9c2c7f80aff8894ee8d16edf48562b846f259753a80366a2934f1

Fresh read-only final replays pass: primary in normal Python, 2.811337 seconds;
reference under -O, 7.012695 seconds. Both preserve final bytes and all
94 identities before and after. Full tests/audit overlapped; final replays ran
concurrently. Timings exclude final serialization and are verification
observations, not application benchmarks or implementation rankings.

The [retained capture](results.json) is the repository artifact; first/preflight
files remain external working evidence. Runtime is isolated Python 3.11.6 on
macOS arm64 with fresh external caches. Read-only replay from the repository root:

```sh
qr05ao_cache=$(mktemp -d /tmp/det8-qr05ao-replay-XXXXXX)
.venv/bin/python -I -X "pycache_prefix=$qr05ao_cache" \
  docs/validation/qr-05ao-field-measurements-2026-09-08/study.py --verify --route primary

qr05ao_opt_cache=$(mktemp -d /tmp/det8-qr05ao-replay-opt-XXXXXX)
.venv/bin/python -I -O -X "pycache_prefix=$qr05ao_opt_cache" \
  docs/validation/qr-05ao-field-measurements-2026-09-08/study.py --verify --route reference
```

## Applicable value and next gate

This supplies a concrete restricted-measurement interface for exact geometric
responses. Mean-only observations lose identifiable predictive information;
the richer moment interface recovers all selected responses and the full field
on these dictionaries. It separates model-dependent reconstruction, physical
preparation, measurement access and numerical stability instead of treating
them as the same achievement.

The next proposed gate is QR-05AP: bounded measurement-error stability of the
TWO FROZEN coarse-response decoders, canonical and geometric. Exact agreement
on noiseless model data need not mean equal behavior on corrupted measurements.
No decoder fitting, optimization or source-span expansion is proposed there.

Use dimensionless tile-local moments, with xi=(u-u0)/width_u and
eta=(v-v0)/width_v, normalized by V^2*h_tile. Keep mixture normalization exact.
Normalize a positive-volume coarse response by V^2*h_C*h_D.
After transporting the frozen decoder to y_hat=b+Bz, the hypothetical box
|delta_z_i|<=epsilon gives a sharp per-response bound
epsilon*sum_i abs(B_ji), attained by its retained sign-vector witness.
The detailed protocol must fix all rows, ties, null cases and coordinate
transport before any fixed AP calculation; none has been performed.

This error box would be a stated mathematical assumption, not calibrated
sensor noise or necessarily a realizable field perturbation. Source-span
portability, fine/full-field robustness, arbitrary fields, unknown geometry,
minimal sensing, physical mixture preparation, quantum channels, gravity,
RET integration and Lean verification remain separate unestablished boundaries.
