# QR-05AL: breakpoint-aware middle moments

7 September 2026. Research after pushed AK commit
`8527e35b565e2005e918209f125efd8bd8c9de1f`.
The [prospective protocol](README.md) fixes the query family, tile contract,
controls, complete output and validation sequence before fixed computation.

Status: exact fixed reconstruction and all 73 tests passed in normal and
optimized Python. Final capture/replay verification is recorded below.

## What the proposed contract retains

Pair averages integrate incoming and outgoing causal volume separately. AK's
missing term depends on both functions at the same middle point. For supplied
rectangular geometry those functions are piecewise bilinear. A breakpoint grid
shared by all declared endpoints makes them bilinear on each positive tile.

In the global coordinate basis phi=(1,u,v,uv), write those functions as
L=ell^T phi and R=r^T phi. With m=integral phi dmu and
G=integral phi phi^T dmu,

    integral L dmu = ell^T m,
    integral R dmu = r^T m,
    integral L R dmu = ell^T G r.

The 4-by-4 matrix has repeated raw moments. Nine values
M_ij=integral u^i v^j dmu, i,j in {0,1,2}, supply its distinct entries.
They are not nine independent geometric degrees of freedom or a proved minimum.
The contract also needs tile geometry and incoming/outgoing coefficients for
every declared endpoint, including explicit zeros. Both counts and serialized
sizes must include these data; this is not a nine-number global model.

Two mean-only controls isolate different losses. The original-middle product
is P=J_AB*J_BC/h_B. The tilewise product sums the corresponding products within
the same declared tiles. Their errors satisfy

    P-T = (P_tile-T) + (P-P_tile).

The first term is dependence remaining inside tiles; the second is the effect
of using separate tile means. No strict improvement or universal monotonicity
is assumed. Zero-middle products remain undefined, while a positive middle
with an empty endpoint gives a valid zero.

## Coordinate and scope discipline

Moment vectors and coefficients are coordinate-dependent; their contractions
must transform together. All additivity checks use a common global basis.
A translated coordinate system mixes moment degrees, so neither copying raw
moments nor applying only a scalar weight is valid in general. Very large
translations may exceed this diagnostic's retained rational-component limit;
that is a payload limitation, not failure of affine mathematical covariance.

Exact reconstruction would apply to these declared functions on supplied
geometry. New endpoint queries can introduce new breakpoints and coefficients;
longer products can need higher moments. No unknown geometry, arbitrary dynamics,
continuum gravity, empirical validation, ontology or RET/Lean integration is
established by this gate.

## Fixed reconstruction and controls

Moment contractions and independent direct tensor-Simpson integration agree on
all 26,775 ordered triples and 3,725 directed pairs in the unchanged five
families, three levels and five probes. Of those triples, 1,530 have positive
true measure. Every complete true triple child block is additive: 19,375 blocks,
34,175 child terms and 5,400 direct l0-to-l2 reconstructions through l1 agree.
All 475 middle-moment aggregation blocks preserve each of the nine global raw
moments exactly. The complete declared AK input, cell-volume, pair, ten-field
triple and true coarsening projections agree with the authenticated prior file.

The mean-only controls remain distinguishable from this exact reconstruction:

| Retained comparison | Outcome |
| --- | --- |
| Original-middle positive product errors | 1,100 |
| Tilewise positive product errors | 1,100 |
| Positive triples exact under either mean-only control | 430 |
| Individual errors reduced by breakpoint subdivision | 205; all retain positive residual error |
| Aggregate level/probe errors reduced | 20 of 75; 55 unchanged |
| Aggregate tilewise errors still positive | All 75 |

Neither mean-only control invents positive support where T=0 in this fixed
family. Both have 12,730 defined zero errors, including 12,300 zero/zero rows.
There are 12,945 zero-middle triples with undefined products and errors;
19,455 fully normalized triple fractions are undefined. The difference is
6,510 positive-middle/zero-endpoint cases with defined raw zero products.
Between-tile errors are positive in 205 rows, zero in 13,625 and never negative.
No sign or improvement was required by the acceptance rules. These are finite,
overlapping deterministic contexts, not independent trials or empirical rates.

### A distinct-region fixed witness

Grid whole l2 triple (1,4,7) has three distinct region labels. Its middle is
[1/2,2/3] x [0,1/2], split by the shared endpoint grid at v=1/4 into two tiles.

| Quantity | Exact value |
| --- | --- |
| True T, recovered by full moments | 1/20736 |
| Original-middle product P | 1/13824 |
| Tilewise mean-only product P_tile | 1/18432 |
| Original product error | 1/41472 |
| Residual within-tile error | 1/165888 |
| Between-tile error | 1/55296 |
| Whole-middle centered integral | -1/41472 |
| Sum of tile-centered integrals | -1/165888 |

Subdivision reduces the error but does not remove it. Full moment contraction
retains the shared-point product that both kinds of averaging discard. The
effect is not limited to repeated-region diagonals.

For grid whole at l0,l1,l2, the original aggregate errors are respectively
1/1536, 23/36864 and 517/884736. The tilewise errors are 1/1536, 11/18432 and
7/16384. The true whole-region triple measure remains 1/288 at every level.
This is not a continuum-convergence or universal refinement-monotonicity result.

### Full payload accounting

The 525 retained middle rows include 270 positive and 255 empty clips. Among
positive middles, 225 have one tile and 45 have two, giving 315 positive tiles.
Every tile retains all incoming/outgoing vectors for its level's endpoint
inventory, including explicit zero vectors.

| Serialized rational entries | Count |
| --- | --- |
| Nine raw moments per tile | 2,835 |
| Nine whole-middle moments per row, including zeros | 4,725 |
| Four coefficients per vector (4,550 vectors) | 18,200 |
| Positive middle bounds | 1,080 |
| Tile bounds | 1,260 |
| Middle breakpoint lists | 1,125 |
| Coarsening witnesses, two nine-moment vectors per block | 8,550 |

These count repeated serialized rational pairs, not distinct numbers or
independent parameters. The labeled moment contract contains 29,225 such
entries before the separate coarsening witnesses; the full research output
also retains inputs, IDs, labels, pair/triple results and counts. No derived
4-by-4 Gram matrix is transmitted as an extra sixteen-entry payload.

| Family | Complete moment-contract bytes | Complete family bytes |
| --- | --- | --- |
| grid | 76,804 | 2,694,191 |
| warp | 80,341 | 2,714,316 |
| warp_stale | 80,341 | 2,714,322 |
| boost | 76,750 | 2,694,096 |
| dilate | 75,660 | 2,684,910 |

The five separately canonicalized contracts total 389,896 bytes. This is
explicit storage accounting for a redundant research representation, not a
compression ratio: the full family contains answer tables and witnesses that
the contract does not store, while the supplied rectangles already allow fresh
calculation of moments. No minimal encoding or information-theoretic loss of
the complete supplied geometry is claimed.

### Coordinate controls and historical boundary

Complete family transport passes for boost and dilation, including the input
problem, clipped/tile bounds, breakpoints, raw moments, all coefficient entries,
centered quantities, scalar results, coarsening and counts; only the family
label is excluded. Raw moments and coefficients change even when boost leaves
the final geometric measures unchanged. Warp_stale agrees with warp after
excluding only that label. No annotations enter the engines, so no stale mark
is authenticated or repaired.

AK's specified input/pair/triple/true-coarsening mathematics is reproduced.
Its other coarsening diagnostics and older calculations remain identity-only.
Historical source authentication is not a claim to have rerun every old gate.

## Verification and evidence lifecycle

Both independent engine implementations, the runner and the protocol were
reviewed before fixed computation. The protocol plus four Python files were
frozen, authenticating 76 targets: five current sources, 42 prior captures and
29 ancestor sources. No source, formula, fixture or protocol correction followed
the first fixed calculation. Prefreeze cleanups were lint/format changes and an
inherited test comment clarifying AL's arithmetic routes, not changed formulas.

Root's separate generic oracle checked, per engine and per Python mode:
100 signed/nonsquare rectangles (900 basic raw-moment comparisons plus unequal
split checks), 4,104 triple rows from base and translated 5/6/7-cell synthetic
families, and 17,136 interior coefficient evaluations. Its direct triple oracle
enumerates ordered interval atoms and their factorial tie volumes; it does not
reuse either engine's moment or Simpson calculation. It also checks Gram forms,
centered constant rows, complete endpoint inventories, affine moment transport,
coarsening, nulls, detachment and rejection of oversized retained moments.

All **73 AL tests** pass normally (73.02 seconds) and under -O (72.71 seconds).
The only optimized warning is pytest's expected notice concerning ordinary
non-rewritten assertions; engine guards use explicit exceptions. The 61 generic
tests passed before fixed release, most recently in 3.85 and 3.71 seconds.
Twelve fixed tests cover five complete independent family-oracle comparisons,
the full suite/payload/prior bridge, three cached dispatch checks and three
mutation groups. The independent test oracle uses factored moment formulas,
interior-node coefficient reconstruction and explicit polynomial convolution,
plus separate direct pair/triple polynomial integrals. Cached dispatch tests
isolate orchestration and are not extra mathematical integrations.

The 49 non-noop corruptions comprise 30 family/payload/math/coarsening changes,
11 suite/control changes and eight AK projection changes. Most test complete
wire comparison; two directly exercise full transformed-input/payload controls,
and the AK changes exercise the declared bridge. They are not advertised as a
standalone semantic validator for arbitrary imported moment contracts. Explicit
subprocess checks retain 44 ValueError rejections per mode. Engine owners also
ran their own separate synthetic polynomial/corner/quadrature/affine checks.

The first external compare capture took 12.801422 seconds. Exactly one
independent fresh normal-Python reference-only read-only audit reproduced it
in 9.031607 seconds, preserving its bytes and all 76 identities. Full test runs
and that audit overlapped; their timings are verification observations, not
an application benchmark or relative-performance experiment.

External create-only preflight and the final exclusive-create
[retained capture](results.json) agree with the first comparison on every
non-runtime envelope field. All source and historical ledgers and the entire
exact mathematical suite are identical. Fresh read-only primary replay in normal
Python took 8.838010 seconds; reference replay under -O took 8.912788 seconds.
Both reproduce the retained suite exactly, with final bytes and all 76 identities
unchanged before and after. The final replays ran concurrently; these are not
performance rankings.

| Capture | Bytes | Suite time (seconds) |
| --- | --- | --- |
| First external comparison | 13,515,231 | 12.801422 |
| External preflight | 13,515,227 | 12.692431 |
| Final retained capture | 13,515,233 | 12.567514 |

All three contain the same 13,503,835-byte canonical mathematical suite.
Capture byte/hash differences arise only from runtime metadata, not changed
mathematics or source ledgers.

    First SHA256:     ec132b0c8583ffd6729576278a9b18ea67fc9ea304915df940ee4ee80f6a3008
    Preflight SHA256: 29dd9b0319cf7d5843554f2de83e9a830889e4ded3b020f2816667cd0b024f41
    Final SHA256:     1e0f3ac8822afcd4407a176e1bfa4a2c3f5e45c43724e4e70bf3f66f01580a52
    Suite SHA256:     368a749163b31afec19f1c25e543f5ee74d84c99cde0861a341d5f38bcea9d2d

The retained runtime is isolated Python 3.11.6 on macOS arm64 with a fresh
external bytecode cache. Recorded suite timing excludes final serialization.
First/preflight files are external working evidence; the linked final file is
the repository artifact. Read-only reproduction from the repository root:

```sh
qr05al_cache=$(mktemp -d /tmp/det8-qr05al-replay-XXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05al_cache/primary" docs/validation/qr-05al-middle-moments-2026-09-07/study.py --verify --route primary
.venv/bin/python -I -O -X pycache_prefix="$qr05al_cache/reference" docs/validation/qr-05al-middle-moments-2026-09-07/study.py --verify --route reference
```

Two independent read-only scientific reviews checked the exact witnesses,
moment/coordinate units, payload entry and byte counts, null accounting and
next-gate boundaries against retained evidence. Both passed without requiring
a mathematical or scientific prose correction. Ruff lint/format checks and
scoped publication whitespace checks pass. No RET/core source, dependency,
temporary model sheet or prior research file was changed for this gate.

## Generic analytic controls

For a unit rectangle, the nine moments are M_ij=1/[2(i+1)(j+1)]. There is one
tile. Incoming coefficients are (0,0,0,1/2), outgoing coefficients are
(1/2,-1/2,-1/2,1/2). Their full contraction gives T=1/288; both mean-only
controls give 1/128. Subdivision at existing breakpoints alone does not remove
the within-tile dependence. The integrated centered term is -5/1152 and the
normalized middle covariance is -5/576.

A separate synthetic five-cell partition splits the unit square into three
horizontal bands. Split the bottom band at u=2/3 and the top band at u=1/3;
leave the middle band B unsplit. For A the bottom-left region and C the
top-right region, L_A=min(u,2/3)/6 and R_C=(1-max(u,1/3))/6 on B. The shared
grid introduces three middle tiles. Direct integration gives

    h_B = 1/6,          J_AB = J_BC = 1/81,
    T = 25/34992,       P = 2/2187,       P_tile = 17/23328,
    P-P_tile = 13/69984,                 P_tile-T = 1/69984.

Thus both subdivision and within-tile moments have a nonzero effect in a
declared hand example. These are generic controls, not outcomes selected from
the fixed five-family AL comparison.

## Proposed next gate: QR-05AM, query reuse and explicit refinement

Test whether this contract is useful for new declared endpoint queries, not only
the original family used to construct it. Freeze the original middle domains,
tile grids and moment payloads. Prespecify a small endpoint-query extension
containing an aligned case and a genuine clamp kink inside an old tile.

For new functions certified bilinear on every old tile, change coefficients
only and reuse the unchanged moments. For an unsupported kink, require an
explicit refinement decision; separately permit a geometry-aware route that
splits affected tiles, derives new moments from the supplied bounds and checks
additive recovery of all old moments. Compare both admitted routes with direct
integration. Retain a declared incorrect forced old-tile bilinear fit as a
falsifiable control, including any equalities, not only discrepancies.

Count coefficient-only reuse separately from added tiles, moments and complete
payload. This is not an impossibility theorem for the old full record: it
already includes tile bounds from which further moments can be calculated.
No universally minimal grid or arbitrary-query interface is assumed. Freeze
the detailed AM protocol before calculations; none have been performed here.

A subsequent degree-aware four-point/operator study could ask what happens
under one more causal integration. It would introduce another coupled
intermediate point and potentially higher polynomial degrees; multiplying the
present local summaries is not automatically a closed operator calculus.
That larger extension, RET/Lean integration and physical interpretation remain
separate from this completed finite moment-reconstruction gate.
