# QR-05AM: query reuse and explicit refinement

Started 7 September 2026; verification completed 8 September 2026 (Hawaii).
Research after pushed AL commit
`578c28311d747680771adc61923192c898720bbd`.
The [prospective protocol](README.md) fixes query construction, structural
admission, supplied-moment trust, refinement and the complete output wire.

Status: exact fixed comparisons, all 74 normal/optimized tests, independent
reference audit and final read-only replays passed without a post-first correction.

## What is being reused

AL retained rectangular middle tiles and nine global raw moments per tile.
For new incoming/outgoing endpoint regions, those same moment entries can
integrate new coefficients if both causal-volume functions remain bilinear
on every old tile. Reuse changes the functions' coefficients, not their saved
geometric moments. It still requires computation; it is not a zero-cost claim.

If a genuine clamp kink lies inside a tile, a single bilinear function cannot
represent that endpoint function there. This contract explicitly requires
refinement rather than silently treating a corner interpolation as exact.
The geometry-aware route derives new child moments from supplied old bounds
and checks that all nine add back to the old vector. The retained bounds
already supply the geometry needed for that refinement; no information-theoretic
impossibility for the complete old record is inferred.

Admission checks incoming and outgoing functions separately. An identically
zero function can have irrelevant coordinate breakpoints. Conversely, a zero
triple product does not certify that its individual pair-mean functions fit.
Even nonzero integrals can coincide accidentally under a wrong function fit.
The deliberately forced old-tile corner approximation is retained as a control
regardless of whether its answer differs.

## Trust and verification boundary

The primary engine consumes supplied moments without regenerating old higher
moments. It checks structure and volume/additivity, but does not authenticate
an arbitrary untrusted higher-moment vector. The pinned AL projection and the
independent reference provide that boundary. The reference independently
integrates the old moments from their bounds and rejects inconsistent values;
this is disclosed verification work, separate from new-child derivation.

The new-moment hook is called only for derived child pieces. Tests disable it
on reusable requests and count calls on mixed requests, checking that unchanged
pieces keep their original bounds/moment data. Queries independently start from
the original grid, so one query's refinement cannot conceal another's unsupported
function. No old endpoint coefficients or pair/triple answers enter the engines.

## Synthetic controls: structural admission is not answer matching

With B=[0,1]^2, dmu=du dv/2, incoming A=[0,1/2] x [0,1] and
outgoing C=B, the incoming function has an active interior kink. Its forced
old-tile fit is uv/4. Direct integration gives J_in=3/64 and T=7/2304;
the forced fit gives J_in=1/32 and T=1/576, an error of -1/768.
The explicit split at u=1/2 recovers both integrals and all nine old moments.

An equality control is equally important. For the same B, take incoming
A=[1/4,3/4] x [0,1] and outgoing C=[2,3]^2. Incoming still has active
kinks, but both exact and forced calculations give J_in=1/32 and T=1/64.
This remains a refinement request, not an admitted bilinear function. The
generic interface permits those external endpoint regions without clipping;
the fixed queries all lie inside their original probe.

The trust control changes old M22 coherently by delta=1/100 in the whole
middle and its sole tile. Its M00 and additive checks still pass. On a
unit-square self query the primary therefore returns 1/288+delta/4 rather
than silently replacing the supplied value. The independent reference rejects
that vector as geometrically inconsistent. This intentional difference tests
the declared provenance boundary; it is not a disagreement on authenticated
geometry or a claim that arbitrary moments describe a positive measure.

## Fixed reuse, refinement and payload

Both independent engines agree on all 2,625 query records in five families,
three levels and five probes. The 525 middle rows comprise 270 positive
rectangles and 255 empty clips. Every query uses the original AL snapshot.

| Query on each middle | Reuse | Refinement | Empty middle |
| --- | --- | --- | --- |
| Whole probe | 270 | 0 | 255 |
| Middle self | 270 | 0 | 255 |
| Incoming kink | 0 | 270 | 255 |
| Outgoing kink | 0 | 270 | 255 |
| Zero incoming endpoint | 270 | 0 | 255 |

The exact route has 1,080 positive triple integrals. The 540 positive-middle
kink queries all have strictly negative forced-minus-exact triple error;
270 have an incoming pair error and 270 an outgoing pair error. All 810
reusable queries have zero forced error. No positive forced error or refined
forced equality occurs in this fixed family; the synthetic equality above
remains part of the tests. Signs are observed outcomes, not acceptance rules
or universal claims about interpolating arbitrary functions.

There are 1,545 undefined fully normalized fractions: 1,275 empty-middle
queries plus 270 positive-middle/zero-endpoint queries. Only the former have
undefined divided pair products, covariance and centered integrals. Their
raw pairs, triples and errors are still zero. A positive-middle zero-endpoint
query keeps its valid outgoing pair measure even though the triple is zero.

Across repeated queries, 610 old-tile occurrences are replaced by 1,220 child
pieces. The new-moment hook runs exactly 1,220 times per route across the
five families. Another 965 piece occurrences retain their supplied moments;
20 of those occur inside queries that refine other tiles. Every one of the
1,575 old-tile occurrences has a complete nine-moment additive witness.
These occurrence counts must not be confused with the 315 snapshot tiles.

### Fixed mixed-reuse witness

Grid, whole probe, l1, middle event 8 is B=[1/3,2/3] x [1/2,1], originally
split at u=1/2. The incoming-kink query chooses A=[1/3,5/12] x [1/2,1]
and C=B. Only its first old tile needs splitting, at u=5/12; its second
tile stays byte-for-byte identical in bounds and moments. The query therefore
uses two derived pieces and one retained piece, with two new-moment calls.

| Quantity | Exact value |
| --- | --- |
| Incoming pair integral | 7/9216 |
| Forced incoming pair integral | 1/1536 |
| Outgoing pair integral, exact and forced | 1/576 |
| True triple integral | 37/3981312 |
| Forced triple integral | 7/995328 |
| Forced-minus-exact triple error | -1/442368 |
| Whole-middle centered integral | -13/1990656 |

Both parent blocks recover all nine original moments. The separately evaluated
middle-self query still reuses both original tiles with no new moment calls;
refining the incoming-kink query has not modified its starting snapshot.

### Explicit representation costs

The input snapshot contains 7,560 raw-moment entries (4,725 whole-middle,
including empty zeros, and 2,835 tile entries), plus 3,465 middle/tile/breakpoint
coordinate entries. Probe bounds remain separately present in its input wire.
Query endpoints add 11,760 coordinate entries. Reference geometric verification
checks all 840 old vectors, or 7,560 entries: 270 positive whole rectangles,
315 positive tiles and 255 explicit empty zero vectors. This work is separate
from the 1,220 newly derived vectors and is not called computation-free reuse.

| Repeated output payload | Entries |
| --- | --- |
| Forced old-tile coefficients: 3,150 four-entry vectors | 12,600 |
| Exact piece coefficients: 4,370 four-entry vectors | 17,480 |
| New child moments | 10,980 |
| Retained piece moments | 8,685 |
| Exact piece bounds | 8,740 |
| Old/summed moment witnesses | 28,350 |

These count serialized rational pairs including zeros and repeated values, not
independent geometric parameters. Complete byte scopes are separately defined
in the protocol; the exact update includes retained as well as new pieces.

| Family | Snapshot bytes | Query bytes | Exact update bytes | Full family bytes |
| --- | --- | --- | --- | --- |
| grid | 27,069 | 45,197 | 154,680 | 916,869 |
| warp | 30,282 | 45,711 | 168,222 | 963,733 |
| warp_stale | 30,288 | 45,711 | 168,222 | 963,739 |
| boost | 27,033 | 45,169 | 154,524 | 916,530 |
| dilate | 26,082 | 45,169 | 150,281 | 901,239 |

The five snapshots total 140,754 bytes; query projections 226,957; exact
updates 795,929; separately canonicalized full families 4,662,110. These scopes
overlap and retain redundant diagnostics. They are neither additive unique
storage costs, a minimal wire nor a compression benchmark.

### Coordinate and historical boundary

Full boost and dilation comparisons pass for inputs, probe/query/tile bounds,
old/new moments, forced/exact coefficients, admission, maps, counts and every
result field. Generic translated hands use binomial moment transport and the
corresponding coefficient pullback. Coordinate-dependent moments cannot simply
be copied while changing the basis. Stale warp equals warp after excluding only
its family label; this geometry-only computation does not authenticate marks.

Every consumed AL geometry/moment field and probe bound matches the pinned
artifact, and the prespecified queries are independently reconstructed. No old
endpoint coefficients or answers enter this gate's engine input. Reference
geometric rechecking of moments is disclosed; AL's other mathematics and all
older mathematical calculations are not replayed here.

## Verification and evidence lifecycle

The protocol and four Python sources were reviewed and frozen before fixed
computation. All 82 targets remain authenticated: five AM sources, 43 prior
captures and 34 ancestor sources. No source, formula, fixed query or protocol
correction followed the first fixed calculation. Before freeze, a wording
clarification explicitly permitted shared references among valid native input
containers while requiring detached outputs; lint/format cleanups did not
change the mathematics.

All **74 tests** pass normally (35.91 seconds) and under -O (35.62 seconds).
The only optimized warning is pytest's expected notice about ordinary
non-rewritten assertions; engine guards use explicit exceptions. The final
pre-fixed-run generic checks passed 62 tests in 1.53 and 1.56 seconds.
Twelve fixed tests comprise five complete independent family-oracle comparisons,
one complete suite/payload/AL projection comparison, three cached dispatch
checks and three corruption groups. Cached dispatch checks isolate orchestration,
not additional integrations. The independent test oracle uses factored moment
formulas, interior-node coefficient checks, polynomial convolution and separate
direct pair/triple polynomial integrals.

The 51 non-noop corruptions comprise 30 family-wire changes, 11 suite-field
changes, two complete-transform mutations and eight AL projection mutations.
Most check complete exact-wire comparison; transform/projection cases also
exercise their corresponding controls. These do not make the private consumer
a standalone semantic validator for arbitrary imported geometry. Explicit
normal/optimized subprocess tests retain 49 ValueError rejections per mode,
plus hook-disabled reuse, counted mixed-query derivations and the intentional
wrong-higher-moment trust boundary.

Root's separate generic ordering oracle checks 30 query rows per engine per
mode, and all 30 again after a signed affine translation/scaling. Each family
has 18 reusable, seven refined and five empty queries, 17 derived pieces and
three refined forced equalities. It checks every result field, old corner fit,
exact piece and moment block. Its independent direct pair/triple oracle uses
ordered-interval atoms with factorial tie volumes; its raw-moment oracle uses
rectangle means and variances. It also verifies coefficient/moment transport,
disabled-hook reuse and supplied wrong-moment behavior. Engine owners ran
their own independent synthetic checks. The
persisted 25-child grid test checks the maximum prescribed split, exact hook
order and all nine additive moments.

The first external compare capture took 6.713795 seconds.
Exactly one independent fresh normal-Python reference-only read-only audit
reproduced it in 5.400986 seconds, preserving its bytes
and all 82 identities. The external create-only preflight and final exclusive
capture agree with that first run on EVERY non-runtime envelope field,
including source ledgers and the complete mathematical suite.

Fresh read-only final replays pass: primary in normal Python,
4.320570 seconds; reference under -O, 5.431907
seconds. Both reproduce the complete retained suite with final bytes and all
82 identities unchanged before and after. Full tests and independent audit
overlapped; the two final replays also ran concurrently. These timings are
verification observations, not application benchmarks or performance rankings.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 4,676,696 | 6.713795 |
| External preflight | 4,676,700 | 6.713575 |
| Final retained capture | 4,676,696 | 6.786677 |

All three contain the same 4,664,468-byte canonical mathematical suite.
Capture differences are runtime metadata, not changed mathematics or ledgers.

    First SHA256:     571845f448c35b035aa4b15c580e7209c5a2786eb0ab27401835acff9c712279
    Preflight SHA256: d80b62e3cf549e8d1c19c371ff0dd20bc64fa0497a669ffd602ef3e3cc2d4c8f
    Final SHA256:     46abc46e884b8e4bc472948b4c67b3f3dd4b6dd1e8d99ced1d778912dddc085e
    Suite SHA256:     f5a990023037dbebfc0b78640922a789d172950ae41ce8544878a866339f19de

The [retained capture](results.json) is the repository artifact; first/preflight
files remain external working evidence. Recorded runtime is isolated Python
3.11.6 on macOS arm64 with fresh external bytecode caches. Suite timings exclude
final serialization. Read-only reproduction from the repository root:

```sh
qr05am_cache=$(mktemp -d /tmp/det8-qr05am-replay-XXXXXX)
.venv/bin/python -I -X "pycache_prefix=$qr05am_cache" \
  docs/validation/qr-05am-query-reuse-2026-09-07/study.py --verify --route primary

qr05am_opt_cache=$(mktemp -d /tmp/det8-qr05am-replay-opt-XXXXXX)
.venv/bin/python -I -O -X "pycache_prefix=$qr05am_opt_cache" \
  docs/validation/qr-05am-query-reuse-2026-09-07/study.py --verify --route reference
```

## Applicable value and next boundary

This supplies a bounded reusable integration contract: change endpoint
coefficients when the saved basis is adequate, make a structural refusal when
it is not, and explicitly account for new geometry/moments where refinement
is authorized. It separates a trusted snapshot consumer from an independent
geometric verifier. Those are useful design patterns for later mathematical
operators; this private diagnostic is not a hardened RET application.

Correct reuse still preserves shared-point dependence, not a product of
separate means. For a rectangular self query the exact normalized triple is
1/36 while the pair-product value is 1/16. Passing admission does not create
a stochastic transition, quantum channel, empirical calibration or dynamics.

The next proposed gate is degree-aware four-point composition: retain the
coupling of two middle points while one more integration creates a piecewise
biquadratic incoming field. Pairing that field with a bilinear outgoing
function motivates raw moments through degree three per coordinate, with a
forced bilinear truncation as a falsifiable control. The detailed next protocol
must be frozen before fixed calculations. No universal finite-degree closure,
minimal grid, unknown-geometry reconstruction, continuum limit, ontology,
gravity derivation, Lean verification or RET integration is established here.
