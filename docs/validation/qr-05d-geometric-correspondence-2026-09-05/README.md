# QR-05D: supplied geometry and order-derived propagation diagnostics

5 September 2026. Research after QR-05C commit
`34483a602987369f52c41179daf1dd63e06aa0ed`. Freeze this protocol and executable
sources before retained capture. Outcomes belong in RESULTS.md. Prior evidence,
RET/core sources, the temporary model sheet and dependencies remain untouched.

## Question and claim boundary

Which geometric questions can a finite order answer when a geometry and density
are supplied for comparison? Test exact causal support, interval cardinality,
and the first three formal mass-squared coefficients of a retarded kernel.
Include order-preserving transformations and an obstruction to embedding in
the chosen 1+1-dimensional flat comparison geometry.

This is an algebraic diagnostic, not a derivation of the generating geometry,
a continuum limit, a quantum field theory, a stochastic sprinkling validation,
an apparatus model, or gravitational dynamics. No new physical laws or
ontological commitments are assumed. The new scalar kernel is not a CP quantum
channel, a Born probability, or the one-qubit payload map of QR-05A--C.

The continuum order/volume motivation needs strong additional assumptions;
finite order and total count are not a metric-reconstruction theorem. In
particular, the continuum HKMM statement in Surya's review assumes dimension
greater than two. Here the comparison is derived directly in null coordinates,
not by applying that theorem. See [Surya, sections 2--3](https://arxiv.org/html/1903.11544).

## Supplied comparison and diagnostic

Use units c=hbar=1 and signature (+,-). Let u=t+x, v=t-x, so
`ds²=du dv`, `tau²=delta_u delta_v`, and an Alexandrov interval has spacetime
volume `V=tau²/2`. The retained coordinate fixtures have no equal u or v
coordinates between distinct points: every comparable pair is strictly
timelike. We do not choose values of continuum distributions on null or
coincident pairs. Matrix diagonals are zero by the strict-order convention.

Let C[i,j]=1 exactly when event i precedes event j, oriented from past to
future. These matrices act in that stated index convention; transposing all
matrices would give the usual future-row convention. C²[i,j] counts the
strictly intervening events, and C³[i,j] counts ordered comparable pairs in
that interval. All intermediate events are counted once.

For a supplied positive density rho and formal variable z=mass², define

```text
K(z) = sum_(k=1)^(n-1) (-z)^(k-1) C^k / (2^k rho^(k-1))
     = C/2 - z C²/(4 rho) + z² C³/(8 rho²) + ... .
```

The finite series follows from strict upper triangularity. It obeys
`K = C/2 - z C K/(2 rho)`. It is the chain-sum specialization motivated by
the standard 1+1 retarded scalar kernel; compare the continuum coefficients
of `J0(mass*tau)/2`: `1/2, -tau²/8, tau⁴/128` on timelike pairs.
The density-dependent amplitudes and continuum expression are established
inputs, not results of DET. See [Johnston, equations 3.23 and 3.31](https://arxiv.org/pdf/0806.3083).

We compare coefficients, not the value at a chosen finite mass or the remainder
of a truncated continuum series. Johnston's sprinkling expectation result does
not apply automatically to these deterministic samples. No probabilities,
error bars, likelihoods, fitted dimensions or finite-mass accuracy claims.

Retain C, its link matrix, C², C³, longest-chain edge counts, all three kernel
coefficient matrices, and all endpoint chain counts through k=n-1. For each
supplied timelike pair retain coordinate tau², V, C²/rho, their signed
difference (order estimate minus coordinate value), continuum coefficients,
and signed coefficient errors. Noncausal matrix entries are retained as zero;
no positive-distance prediction is assigned to them.

## Nine fixed fixtures

Every order has an explicitly supplied bottom and top, at indices 0 and n-1.
They are probe endpoints, not counted in the density calibration. Every probed
continuum Alexandrov interval is contained in the supplied diamond; missing
intermediate points outside the simulated region do not enter these probes.

1. `mesh3`, `mesh5`, `mesh7`: for m=3,5,7, let epsilon=1/(4m), and for
   i,j=1,...,m supply
   `u=(i+epsilon*j)/((m+1)*(1+epsilon))`,
   `v=(j+epsilon*i)/((m+1)*(1+epsilon))`.
   List interiors in increasing i then j between (0,0) and (1,1).
   They have the product-grid order without null ties. n=m²+2 <= 51;
   rho=2m², calibrated to the known whole-diamond volume 1/2.
2. `mesh5_boost`: transform every mesh5 point by `(u,v)->(2u,v/2)`;
   rho=50. This one exact Lorentz transformation must preserve intervals,
   order and coefficients. It does not certify a Lorentz-invariant ensemble.
3. `mesh5_dilate`: `(u,v)->(2u,2v)`, rho=25/2. Distances squared and volumes
   grow by four, while density falls by four; coefficient k in z grows by
   4^k. A dilation is not a Lorentz isometry.
4. `mesh5_dilate_wrong_density`: the same dilated coordinates but rho=50.
   This deliberately inconsistent density must not be silently repaired.
5. `mesh5_warp`: `(u,v)->(u²,v²)`, rho=50. Treat these as new point positions
   in the same flat metric, not a passive coordinate change with a transformed
   metric. Order and global volume persist, local volumes change, and sampling
   becomes nonuniform. This probes information absent from order plus one
   global density. No variable-density correction is implemented.
6. `ferrers6`: interiors, in order, are (2,6),(4,4),(6,2),(3,14),(5,12),
   (14,10), all divided by 16. Add (0,0),(1,1); rho=12. This supplies the
   six-event two-level order a_i < b_j iff i <= j, for i,j=0,1,2.
7. `standard_example3`: six abstract interiors with a_i < b_j iff i != j,
   then an added bottom/top; rho=12 is only a common algebraic scale parameter,
   not a claimed physical density. No coordinates or geometric error values.

The meshes are deterministic, mildly tilted quadratures, not independent
uniform or Poisson samples and not a Lorentz-invariant generation procedure.
Three sizes provide finite diagnostics, not statistical validation or a proved
continuum limit. Whole-diamond C²/rho agreement is true by calibration, not an
independent recovery of volume. Local probes and C³ supply distinct questions.

For each mesh case also designate bottom-to-central-event and central-event-to-top
as local probes; the untransformed central event is (1/2,1/2). Include the
whole-diamond probe for all fixtures. Probe names and order are `whole`,
`bottom_to_middle`, `middle_to_top` (only `whole` for the six-interior cases).
All timelike pairs, not only these examples, remain in evidence.

## Prespecified controls and analytical checks

For the untransformed meshes the interior count is N=m² and its number of
comparable pairs is R=m²*(m²+2m-3)/4. At the whole-diamond endpoints the first
three coefficients are `1/2, -1/8, (m²+2m-3)/(128m²)`. The third differs from
the supplied continuum value 1/128. Retain this discrepancy, even where its
size decreases across m=3,5,7. The midpoint interval contains ((m+1)/2)²-1
events; its count-derived volume is not forced to equal its coordinate volume.

Boosting must preserve all comparison data. Correct dilation rescales all
order-derived and continuum coefficients equally; the wrong-density control
preserves the original order-derived coefficients instead. Warping preserves
all order diagnostics but changes local continuum comparison values. These
are deterministic consequences of the chosen model, not unexplained noise.

The six interiors of ferrers6 and standard_example3 have the same event count,
relation count, link count, incomparability count, number of minima/maxima and
height. Both have six relations and no three-element chains. Therefore their
complete bottom-to-top chain-count arrays are `[1,6,6,0,0,0,0]`, and at rho=12
their entire endpoint polynomials agree: `1/2 - z/8 + z²/192`.
The full interval tables do not agree. Endpoint propagation alone cannot
certify this generating geometry.

For these two six-event interiors only, enumerate every linear extension and
every ordered pair of such extensions. Retain the lexicographically first pair
whose intersection equals the order and the number of all such pairs.
Ferrers6 must admit one; standard_example3 must admit none. This is an exact
obstruction to representation by two linear orders, hence to an exact/induced
order embedding (preserving and reflecting causal comparisons) in this 1+1
flat null-coordinate model. It is not a no-go theorem for all
dimensions or all curved spacetimes. Analytically, reversing a_i,b_i requires
b_i<a_i in an extension, and one extension cannot reverse two such pairs
because the cross relations would create a cycle. Two extensions cannot
reverse all three. Any finite 2D product-order embedding can have coordinate
ties broken consistently to give a pair of linear extensions.

## Connection to the quantum-record results

Pin the QR-05C artifact. Reanalyze its retained fork/join, chain-record and
record-location parent orders after adding explicit probe endpoints, using
rho=2 times the interior event count. Compare the new order diagnostics across
both independent executors. Preserve the earlier CP-map differences by
referencing their exact retained controls; do not rerun or import QR-05C code.

Fork/join global chain polynomials coincide despite their different local
orders. Same-order different-record histories have identical order diagnostics
despite the previously demonstrated quantum-prediction discrepancies. Retain
the delayed quantum control as a separate prior witness as well. Thus these
geometric questions supplement, not replace, the retained quantum record and
its specified measurement access. No coupling from K(z) to the qubit is assumed.

## Interface and evidence format

Input is exactly `{schema_version:"det8-qr05d-problem-v1",case:case_name}`.
Reject malformed fields/types and unknown fixtures, including under -O.
Internal `order_analysis(past,density)` accepts a naturally labeled transitive
strict-past list of lists, 1 to 51 events, and a positive density of exact type
Fraction (not bool, integer or float). Indices are exact ints, sorted and unique;
it is a bounded research helper, not a public general SDK.

All arithmetic is integer or Fraction, with a 4096-bit retained-component
guard. Rational wire values use canonical Fraction strings; matrices are
row-major lists. No floating-point equality or random generator.

```text
analysis:{case,density,coordinates,order,geometry,two_order,probes}
order:{n,relation,links,interval_cardinality,chain_pairs,longest_chain_edges,
       kernel_coefficients,summary,endpoint}
summary:{events,relations,links,incomparable,minimal,maximal,height}
endpoint:{chain_counts,coefficients}
geometry:null | {pairs,metrics}
pairs:[{source,target,tau_squared,volume,count_volume,volume_error,
        continuum_coefficients,coefficient_errors}]
metrics:{timelike_pairs,exact_volume_pairs,max_abs_volume_error,
         mean_abs_volume_error,max_abs_coefficient_errors}
two_order:null | {linear_extensions,realizer_count,first_realizer}
probes:[{name,source,target}]
```

`kernel_coefficients` has shape [3,n,n], ordered by powers z^0,z^1,z^2.
`coordinates` is a list of [u,v] canonical fraction strings, or null for the
abstract control. `two_order` is non-null only
for the two six-event interiors and uses local indices 0,...,5, not the added
endpoints. Enumerated extensions and realizer pairs are lexicographically
ordered. Pair tables use increasing source then target. Longest-chain entries
are edge counts (zero for noncausal pairs); summary height is event count.
`endpoint` means the 0-to-(n-1) entry; zero coefficients are not pruned.
Summary covers all supplied events, including probe endpoints. The collision
also compares summaries of the six interiors separately.

The primary route uses (t,x) interval inequalities and integer matrix powers.
The reference uses null-coordinate inequalities, interval-set counts and
independently counted chains. No executor imports the other or any DET/RET
source. Full outputs must agree; an independent reviewer checks the retained
artifact without importing either executor. Test normal and optimized modes.

The create-only capture records all inputs, analyses, malformed rejections,
control comparisons, prior witnesses, source/prior hashes and runtime metadata.
Replay is read-only and exact, ignoring only new runtime measurements. Runtime
is not an application benchmark. Use -I with fresh external bytecode caches
and disable pytest's cache. Protocol, geometry.py, reference_qr05d.py, study.py,
test_qr05d.py and test_capture.py form the source ledger. RESULTS.md and the
bridge roadmap remain interpretation documents outside it. No new dependencies.

## Reproduction

From the checkout root, use a fresh external cache for each run:

```sh
qr05d_test_cache=$(mktemp -d /tmp/det8-qr05d-test.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05d_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05d-geometric-correspondence-2026-09-05/
qr05d_opt_cache=$(mktemp -d /tmp/det8-qr05d-opt.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05d_opt_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05d-geometric-correspondence-2026-09-05/
```

Capture only when results.json does not exist; never overwrite evidence:

```sh
qr05d_capture_cache=$(mktemp -d /tmp/det8-qr05d-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05d_capture_cache" docs/validation/qr-05d-geometric-correspondence-2026-09-05/study.py
```

Replay without changing the artifact:

```sh
qr05d_replay_cache=$(mktemp -d /tmp/det8-qr05d-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05d_replay_cache" docs/validation/qr-05d-geometric-correspondence-2026-09-05/study.py --verify
```

Source hashes are checked before and after execution. The prior-artifact ledger
pins QR-01 through QR-05C; only the declared QR-05C controls are consumed as
earlier mathematical evidence in this suite. Hashes document identity, not
experimental authentication. Later interpretation edits must not alter the
ledgered protocol, executors, tests or retained capture.
