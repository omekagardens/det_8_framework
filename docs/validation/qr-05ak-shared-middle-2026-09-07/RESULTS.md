# QR-05AK: shared-intermediate geometry and composition

7 September 2026. Research after pushed AJ commit
`8c410538cab848205f837d3b07a9237357609b87`.
The [prospective protocol](README.md) fixes every input, normalization,
decomposition and verification boundary before fixed AK computation.

Status: fixed comparison and normal/optimized tests passed; final evidence
verification recorded below. The exact triple measure is additive, but the
declared product of pair averages is not generally exact.

## What pair multiplication forgets

For clipped regions A,B,C in the supplied geometry, let h_B be middle volume,
J_AB the causal-pair measure and T_ABC the actual three-point chain measure.
The pair-table construction proposes P_ABC=J_AB*J_BC/h_B when h_B is positive.
Both have units of volume cubed, so this is a dimensionally matched comparison.

Let L_A(y) be the volume in A preceding a particular middle point y, and R_C(y)
the volume in C following that same point. The exact relations are

    J_AB = integral_B L_A(y) dmu(y),
    J_BC = integral_B R_C(y) dmu(y),
    T_ABC = integral_B L_A(y) R_C(y) dmu(y).

Pair multiplication replaces the shared-point average of the product with the
product of two averages. For a uniform middle point in B,

    T_ABC - P_ABC = h_B * Cov_B(L_A,R_C).

This specifies the information missing from this construction: dependence of
incoming and outgoing causal volumes on the same internal point. It is not an
ontological premise, a new force, or a universal claim that all pair summaries
are insufficient for every purpose. Full supplied geometry already allows the
triple integral to be evaluated.

## What refinement separates

True triple measure is finitely additive over complete Cartesian child blocks.
Pair products are additive under endpoint-only refinement, with the middle B
held fixed. Refining the middle changes which incoming and outgoing averages
are multiplied. With P_fine the sum over positive-volume child middles,

    P_coarse - T = (P_fine - T) + (P_coarse - P_fine).

The first term retains dependence within fine middle cells; the second is the
dependence lost by grouping them. These are signed errors, not assumed positive
or monotone by the acceptance rules. All ordered triples and child blocks are
retained, including repeated region labels. A repeated region is not a repeated
continuum point or a self-preceding event.

For a zero-volume middle region, raw triple measure is zero but the divided
product and its error are undefined. With a positive middle and an empty
endpoint, the product is a valid zero. Fully normalized triple fractions are
undefined whenever any of the three region volumes vanishes. Zero-measure terms
may be explicitly skipped in aggregate sums; individual null ratios remain null.

## Generic analytic controls

In one unit rectangle with dmu=du dv/2, h=1/2, T=1/288 and P=1/128.
The product excess is 5/1152, with middle covariance -5/576. The uniform-B
expectation of u(1-u)v(1-v)/4 is 1/144; each causal-volume mean is 1/8.
Thus the independently integrated covariance is 1/144 - 1/64 = -5/576.

Splitting the middle rectangle at u=1/3 gives P_fine=7/1152. The excess separates
into 1/384 within-child and 1/576 between-child contributions. Refining endpoint
cells without changing the middle leaves P=1/128 unchanged. This is an explicit
unequal synthetic split, not a result selected from the fixed family.

## Fixed results

The positive-part cubic primary engine and exact piecewise-Simpson reference
agree on the complete mathematical output for all five unchanged families:
grid, warp, warp_stale, boost and dilate. Each has three nested partitions and
five probes. The 25 family/probe definitions appear at all three levels.

| Retained quantity | Count / result |
| --- | --- |
| Directed level-pair rows | 3,725; complete AJ projection agrees |
| Ordered level triples | 26,775 |
| Complete parent-triple blocks | 19,375; every true child sum equals its parent |
| Child terms in those blocks | 34,175 |
| Direct l0-to-l2 blocks | 5,400; every true sum agrees through l1 |
| Positive true level triples | 1,530: 430 exact products, 1,100 overestimates |
| Defined level errors P-T | 1,100 positive, 12,730 zero, none negative |
| Undefined level products/errors | 12,945 zero-middle triples |
| Undefined fully normalized triple fractions | 19,455 |
| Defined between-child errors | 135 positive, 9,675 zero, none negative |
| Undefined block products/errors | 9,565 zero-middle blocks |

The 12,730 zero errors include 12,300 zero/zero comparisons; only 430 are
positive exact equalities. None of the retained triples has P>0 with T=0:
the observed failure is one of magnitude, not invented positive support.
Among the 1,530 positive triples, 1,140 use repeated region labels and 390
have three distinct labels. There are 6,510 positive-middle/zero-endpoint
triples: their products and errors are valid zeros, while their fully
normalized fractions remain undefined.

All blocks satisfy the exact within/between error decomposition, endpoint-only
product equality, middle-refined product equality, five-pattern partition of
true measure, and volume-weighted true conditional identity wherever defined.
There are 825 positive within-child errors and no negative ones. Across the
50 adjacent-level family/probe comparisons, aggregate product error decreases
30 times and is unchanged 20 times; it never increases in this fixed family.
All 75 level/probe aggregate errors remain positive. This finite collection
does not establish convergence, universal refinement monotonicity or exact
closure at some future resolution. Signs were retained, not imposed as
acceptance criteria. These overlapping deterministic contexts are not trials,
empirical error rates or independent validation samples.

### A distinct-region witness

For grid, whole probe, l1-to-l2 parent triple (1,2,3), all three parent regions
are distinct. The two child triples are (1,2,4) and (1,3,4), also all-distinct.

| Quantity | Exact value |
| --- | --- |
| True parent measure and complete child sum T | 1/41472 |
| Coarse product and endpoint-refined product | 1/27648 |
| Fine product and middle-refined product | 1/36864 |
| Total coarse product error | 1/82944 |
| Within-child error | 1/331776 |
| Between-child error | 1/110592 |
| Parent and weighted-child true conditional | 1/6 |

The last two error contributions sum to the total exactly. Middle refinement
improves this product, but a residual remains. Endpoint refinement alone does
not change it. Thus the obstruction is not confined to same-region diagonals.

A retained positive equality also matters: grid whole l0 triple (1,1,7) has
T=P=1/6912, zero covariance and true/product conditional 1/4. The conclusion
is that this pair-product construction can fail, not that it always fails.

### Whole-probe aggregate comparison

Grid and warp both have whole-probe volume 1/2 and exact total triple measure
1/288 at every level. Their aggregate product excesses differ:

| Family | l0 error | l1 error | l2 error |
| --- | --- | --- | --- |
| grid | 1/1536 | 23/36864 | 517/884736 |
| warp | 599/497664 | 12697/10616832 | 2433989/2038431744 |

Equal total volume and exact triple additivity do not make this projected
product independent of the partition's internal geometry.

### Controls and prior evidence

Boost agrees with grid on the complete geometry, coarsening and count output;
the supplied input coordinates and family label differ. Dilation multiplies volumes by
4, pair measures by 16, triple measures/products/errors by 64 and the derived
middle covariance by 16; normalized fractions and counts remain unchanged.
Stale warp agrees exactly with warp, including the input problem after dropping
only its family label. Supplied annotations never enter the new engines: this
does not authenticate or repair stale marks.

All five projected input problems and every clipped-volume/pair table agree
with authenticated AJ. AJ coarsening/annotation arithmetic and older mathematics
were not rerun. Their retained files were authenticated, not silently treated
as new AK arithmetic or experimental evidence.

## Verification and reproducibility

Before the first fixed run, the protocol and four Python sources were frozen.
The ledger covers 70 targets: five current sources, 41 prior captures and 24
ancestor sources. No source, mathematical rule, fixture or protocol was changed
after that first calculation. Before freeze, runner review strengthened the
stale-input comparison and a corresponding mutation check; routine lint/format
cleanup did not change the mathematics.

Generic verification preceded fixed execution. Root's separate endpoint-tile
and ordering oracle checked 3,375 rational interval triples against both
engines (6,750 comparisons), plus 450 pair comparisons, in normal and optimized
Python. It also checked affine transformations, an unequal three-level family,
explicitly centered covariance, null cases, complete block accounting and
detachment. Engine owners independently checked polynomial/Simpson primitives,
synthetic family outputs and malformed-input rejection.

The final test suite passes all **75 tests** in normal Python (52.08 seconds)
and optimized Python (52.05 seconds). The only optimized warning is pytest's
expected notice about ordinary non-rewritten assertions under -O; production
guards use explicit exceptions. Its 63 generic/lifecycle tests passed before
fixed release. The 12 fixed tests cover five complete independent family-oracle
comparisons, the whole-suite/AJ projection, three cached-route orchestration
checks and three mutation groups. The third arithmetic route integrates
piecewise affine coefficients; it is distinct from both production primitives.
The orchestration tests are not presented as extra mathematical engines.

There are 39 non-noop corruptions: 24 family, nine suite/control and six AJ
projection mutations. Explicit subprocess checks retain 48 ValueError
rejections per mode. Centered covariance is independently integrated in
generic controls; the retained fixed covariance field is derived from T and P,
not a third independent calculation. These are bounded private diagnostics,
not a complete production API or adversarial resource-hardening claim.

The first external comparison took 6.843639 seconds. An independently run
read-only reference audit reproduced it in 4.367906 seconds. External preflight
took 6.904207 seconds. First and preflight captures agree on every non-runtime
envelope field, including the frozen ledgers and complete exact suite.
All runs used isolated Python and fresh external bytecode caches; no dependency
or unrelated repository changes were required.

The final exclusive-create [capture](results.json) agrees with preflight on
every non-runtime envelope field. Fresh read-only primary replay in normal
Python (4.858456 seconds) and reference replay under -O (4.131371 seconds)
reproduce its complete exact suite, with final bytes and all 70 identity
targets unchanged before and after. The two final replays ran concurrently;
these timings are verification observations, not a performance comparison.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 16,462,741 | 6.843639 |
| External preflight | 16,462,736 | 6.904207 |
| Final retained capture | 16,462,744 | 6.897732 |

All three have the same 16,452,181-byte canonical mathematical suite. Capture
size/hash differences reflect runtime metadata, not different mathematical
results or ledgers.

    First SHA256:     eb736951e7d64ec1e6c26ecf2f74fc62ad6736b3831ef48ad56e1ef3134beb2d
    Preflight SHA256: ed95d1e57e0ce9bd4501cf8f4aef9a28fd0d28c04ddb0468b896ba7527007c47
    Final SHA256:     15fce56375af7e44bfc2f955559c55628c77338d11a1911161c4e3bb6f038db4
    Suite SHA256:     351e16f3ba934c4421d1d03a568695cf7fa90cab23f47ad41087f889083824fa

The retained metadata describe isolated Python 3.11.6 on macOS arm64. The
suite timing excludes final serialization and is not an application benchmark.
First/preflight captures are external working evidence; the final file above is
the repository artifact. Read-only reproduction from the repository root:

```sh
qr05ak_cache=$(mktemp -d /tmp/det8-qr05ak-replay-XXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05ak_cache/primary" docs/validation/qr-05ak-shared-middle-2026-09-07/study.py --verify --route primary
.venv/bin/python -I -O -X pycache_prefix="$qr05ak_cache/reference" docs/validation/qr-05ak-shared-middle-2026-09-07/study.py --verify --route reference
```

Independent final prose reviews checked the witnesses, null accounting and
AL scope against the retained JSON. They corrected the description of the
boost comparison to exclude its supplied input problem; no frozen source or
evidence changed. Ruff lint/format and scoped whitespace checks pass.

This gate supplies an exact accounting identity and finite geometric examples.
It does not infer geometry, establish an empirical observable, construct a
stochastic transition or quantum channel, prove a continuum limit, derive
gravity, validate an ontology or integrate RET/Lean. It does identify a concrete
mathematical target for preserving shared-intermediate information.

## Proposed next gate: QR-05AL

Test a breakpoint-aware middle-cell moment contract for the declared endpoint
and probe family. Split a clipped middle region at the relevant incoming and
outgoing coordinate breakpoints. On each tile, represent the causal-volume
functions in a bilinear basis and retain the geometric moments needed to
integrate their product. Compare the reconstructed pair means, shared-middle
triple measure and centered covariance against direct integration. Retain both
an original-middle mean-only control (AK's P) and a tilewise mean-only control:
the latter separates the effect of introducing breakpoints from the additional
effect of retaining dependence within each tile.

On each tile, use the basis (1,u,v,uv) and raw tensor moments
integral u^i v^j dmu for i,j in {0,1,2}. These nine distinct moments populate
a 4-by-4 Gram matrix, with endpoint coefficients contracting it to obtain the
product integral. Count the tiles, moments and full coefficient payload, not
just nine numbers. Nine moments are not nine independent geometric degrees of
freedom or a proved minimal encoding. Additivity requires a common coordinate
basis, or explicit affine transport when tile-local bases are used.

This is not a universal fixed-size summary, an unknown-geometry reconstruction
or closure under arbitrary future queries. New breakpoints may require new
refinement; longer products may require higher polynomial degrees. Exactness
would be limited to the declared endpoint/probe function family on supplied
geometry, not a physical derivation or a general dynamics theorem.
Freeze the detailed AL protocol before computation. No fixed AL outcomes or
implementation are included in this gate; RET/Lean interfaces remain separate.
