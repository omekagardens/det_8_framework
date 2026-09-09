# QR-05BP: interval-valued population-pair identification

9 September 2026 (Pacific/Honolulu). Prospective specification, written
before implementation or numerical execution. Continue the
[BO result](../qr-05bo-richer-causal-queries-2026-09-09/RESULTS.md)
with externally supplied population tolerances, not inferred error bars.

## Continuous model and observation premises

Keep signature (+,−), auxiliary null coordinates u,v, supplied marks
o=(0,0), m₁=(1/2,1/2), m₂=(3/4,1/2), t=(1,1), and strict intervals
Q=(0,1)², I₁=(0,1/2)², I₂=(0,3/4)×(0,1/2). For η∈{0,1}, s∈{1,4},

```text
ds²=s(1+ηuv)du dv,  dμ=s(1+ηuv)du dv/2,
ρδ=1+δuv,  δ∈[0,2],  dν=ρδdμ/∫Qρδdμ,
τ=μ(I₁)/μ(Q)=(16+η)/[16(4+η)].
```

The density is scalar relative to proper volume. Geometry/scale labels are
flat, conformal, flat_x4, conformal_x4, in that order. Density bounds
uniform, half, one, two denote [0,0], [0,1/2], [0,1], [0,2]. They are
external acquisition premises, not estimates from these observations.

Each fresh point answers both nested causal questions. With qᵢ(δ)=ν(Iᵢ),
the same-point symbol law in order 00,01,10,11 is
(1−q₂,q₂−q₁,0,q₁). Four attempts are iid across points, not across
questions within a point. Marks, comparison access, loss-free sampling and
iid assumptions remain supplied. No clock, coordinates or apparatus is
inferred. Finite sample frequencies are not population probabilities.

The new input is a Cartesian box [L₁,U₁]×[L₂,U₂] of simultaneous
population bounds. Both inequalities must hold at the SAME δ. The box is
intersected with the nested-probability cone and then with each model's
coupled forward curve; its corners need not all be nested. A wholly
nonnested box is well-shaped input with no compatible model, not a syntax
error. Neither membership in a box nor a provenance tag certifies its
coverage, calibration, construction from data or likelihood.

## Exact coupled inverse

For each region R, let M_R(δ)=A_R+B_Rδ=∫Rρδdμ. Retain actual mass
coefficients, including scale. M_Q is strictly positive throughout the
declared density domain. Each probability constraint becomes two affine
halfspaces:

```text
M_Ii − L_i M_Q ≥ 0,
U_i M_Q − M_Ii ≥ 0.
```

Intersect each pair with the closed density bound to obtain a per-query
δ interval, then intersect those intervals. Each result is empty or one
closed interval, including a singleton. A zero-slope inequality admits all
δ if its constant is nonnegative and none otherwise. Nonzero slopes yield
closed lower/upper bounds, even if their roots lie outside the density
domain. Never invert an unreachable raw probability endpoint across a pole.

The reference instead computes each monotone ratio's attainable range on
the density bound, clips the supplied probability interval to that range,
and inverts only reachable endpoints. Constant ratios need an all/none
branch; nonconstant ratios have no inverse pole in their attained range.
Both routes must produce the same coupled interval and labels. A third
test oracle partitions the density bound at all exact box-face roots,
checks endpoints and open-cell witnesses against the original forward
inequalities, then merges admitted pieces. No floating tolerances or grid
approximation replace the continuous feasible set.

Retain the shared-δ rational curve and paired endpoint images, not merely
separate q ranges. Coordinate ranges are descriptive projections; their
Cartesian product is not declared attainable. Likewise, targets remain
the discrete subset of {17/80,1/4}, not an interval hull. Robust target
identification means every admitted parameter has the same target, not
that nuisance, scale or metric have been uniquely recovered.

## Fixed inputs and comparisons

The [protocol](protocol.json) fixes twelve BO population pairs as point
boxes and eleven further boxes. Small/wide boxes about flat_interior and
conformal_interior use half-widths 1/65536 and 1/1024 in BOTH coordinates.
The whole-point collision uses half-width 1/65536. These are stipulated
tolerances, not adjusted after evaluating the answers.

Additional literal boxes are: full=[0,1]²;
inconsistent=[1/4,1/4]×[19/64,21/64];
touch=[3/16,17/80]×[21/64,3/8];
crossing=[1/5,2/5]×[3/10,1/2];
non_nested=[3/4,1]×[0,1/4];
pole_band=[1/16,1/16]×[0,1].
Test shared-parameter incompatibility, singleton contact, partly/wholly
nonnested inputs and zero-slope pole-face inequalities explicitly.

Four density bounds ×23 boxes give 92 cases and 368 hypothesis rows.
Retain all 69 adjacent-density-bound checks and all 48 comparisons from
twelve declared box inclusions ×four density bounds. Compare all 48
zero-width cases with the stored BO capture: same labeled worlds, exact
target sets and statuses, with old δ singletons becoming [δ,δ]. Data IDs
label supplied probability constraints, not the actual generator given to
an observer. Do not compare aggregate case counts with BO as a performance
score: the domains differ.

The old whole-point collision has q=(17/80,21/64), flat δ=1 and conformal
δ=0. Retain its admission indicators in every case; when both parameters
fit, their unequal targets cannot be separated. Preserve both scale pairs
through every interval case. Positivity of the three allowed category
masses is certified on the continuous domain, implying 81 possible and
175 impossible four-attempt words. Retain this analytic support certificate,
not another enumeration of BO's 4,096 record rows. Possible finite packets
still do not imply exact population knowledge. No quantum/chart rerun.

## Exact report contract

Independent primary.py/reference.py expose `analyze(protocol)` with no file
access or shared mathematical code. Native trees contain only plain
dict/list/str/int/bool and Fraction. Computed scalars, roots, interval
endpoints, matrix/mass coefficients and probabilities are Fractions.
Metadata η,s, counts and symbol bits are ints. No floats or None in outputs.
Every δ interval is [] if empty or [lower,upper], duplicating a singleton.

- Top: `schema`="qr05bp-report-v1", `geometries`, `data`, `cases`,
  `density_monotonicity`, `box_monotonicity`, `scale_pairs`, `obstruction`,
  `support`.
- Geometries in protocol order: `id`, `eta`, `scale`, `volumes`
  ([Q,I₁,I₂] Fractions), `target`, `mass_coefficients` (three [A,B] rows),
  `derivative_numerators` (two B_i A_Q−A_i B_Q Fractions),
  `full_q_ranges` (two [min,max] rows over δ∈[0,2]),
  `category_coefficients` (three [A,B] rows for 00,01,11),
  `strict_support` (bool).
- Data in protocol point order then box order: `id`, `intervals` (two
  [L,U] Fraction rows), `nested_nonempty` (bool, L₁≤U₂).
- Cases bound-major then data: `id`=`bound/data`, `bound`, `data`,
  `intervals`, `nested_nonempty`, `hypotheses`, `worlds` (feasible geometry
  IDs), `targets` (sorted unique Fractions), `status` ("infeasible",
  "identified", "ambiguous").
- Hypotheses in geometry order: `id`, `inequalities`, `query_sets` (two
  empty/closed δ intervals including the density bound), `delta_set`,
  `status` ("feasible" or "infeasible"), `curve`. Four inequality rows in
  query-one lower/upper then query-two lower/upper order have `constant`,
  `slope` (Fractions), `kind` ("all", "none", "lower", "upper"), `boundary`
  ([] for zero slope, otherwise a singleton Fraction list of −constant/slope).
- `curve` is {} when infeasible. Otherwise it has `domain` (same δ interval),
  `numerators` (two actual [A_i,B_i] rows), `denominator` ([A_Q,B_Q]),
  `one_point_numerators` (four [A,B] rows in 00,01,10,11 order, retaining
  the [0,0] Fraction row), `endpoints` (two rows, even for a singleton;
  each `delta`, `q` [q₁,q₂], `one_point` four Fractions), `q_ranges`
  (two sorted endpoint ranges; not an attainable rectangle).
- Density monotonicity: adjacent-bound-major then data; each row
  `tight`, `broad`, `data`, `world_subset`, `target_subset`, `nuisance_subset`
  (three bools). Box monotonicity: protocol inclusion-major then bound;
  each `tight`, `broad`, `bound` and the same three bools. Compare every
  labeled δ interval, including empty sets, not only existence.
- Scale pairs in flat/flat_x4, conformal/conformal_x4 order: `worlds`,
  `volume_factor` (Fraction), `target_equal`, `nuisance_sets_equal`,
  `curve_laws_equal` (bools across all cases). Check all three regions and
  numerator/denominator scaling; equal normalized laws do not mean equal
  unnormalized coefficients.
- Obstruction: `worlds`=[flat,conformal], `deltas`=[1,0] Fractions,
  `q` (common paired probabilities), `point_equal` (bool), `target_gap`
  (flat−conformal Fraction), `cases` (one per case, each `case`,
  `flat_present`, `conformal_present`, `both`, `target_ambiguous` bools).
  Both-present implies ambiguity, not its converse.
- Support: `quota`=4, `symbols`=[[0,0],[0,1],[1,0],[1,1]],
  `allowed`=[[0,0],[0,1],[1,1]], `possible_words`=81, `zero_words`=175,
  `continuous_certificate` (bool). This is whole-family support, not the
  support of an infeasible particular box.

Primary integrates monomials and clips affine halfspaces. Reference uses
direct tensor Simpson integration and range-first inversion. Tests use
endpoint antiderivatives and breakpoint/sign partition. Whole native
reports are compared with exact types before canonical encoding/hashing.

## Public interval-query boundary

`study.identify(query)` accepts exactly a plain dict with plain-string keys
`schema`, `data_kind`, `intervals`, `density_bound`, `bound_basis`,
`uncertainty_basis`. String values are `qr05bp-query-v1`,
`population_intervals`, uniform/half/one/two, `external_assumption`, and
`external_population_bounds` respectively. `intervals` is a plain list of
two plain [lower,upper] lists; each endpoint is a plain two-int reduced
rational list with positive denominator. Validate all integer absolute
values ≤2³¹−1 before any gcd/Fraction arithmetic. Require 0≤L_i≤U_i≤1
for each coordinate, but do not require all corners—or any corner—to be
nested. A wholly nonnested box returns empty compatibility, not ValueError.
Malformed types/order/caps/schema or extra fields raise ValueError.

The output has exactly `nested_nonempty`, `worlds`, `targets`, `status`,
`nuisance` (feasible {`id`, `delta`:[lower,upper] Fraction} rows). The solver
uses public continuous-family formulas, not fixture lookup, files, engines
or previous captures. Containers are detached. It accepts bounded rational
intervals beyond the fixed study inputs; finite tests are not exhaustive
machine-input verification. Two prespecified non-fixture point-box API
checks use η=0,1 and δ=1/3 with the half bound. Neither this interface nor
its provenance tags authenticate an uncertainty construction or detect a
finite frequency disguised as an exact population constraint.

## Evidence and bounded execution

Reuse only fresh authenticated BM utility-driver bytes, SHA-256
`157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55`,
for exact codecs/comparison, bounded I/O, exclusive writes and deadlines.
Keep isolated utility globals; BP owns all mathematical/publication wrappers.
No historical engine, estimator or old test tree is run.

Before mathematical execution, create a source freeze with ten identities:
BP README/protocol/primary/reference/study/test_qr05bp, BO README/RESULTS,
BO capture, and BM utility driver. The BO capture is separately pinned to
SHA-256 `df967357d18bf384a9e1fb05a560e9b791a17382463eb2f25ba0a547e1bca105`
before parsing. It supplies only read-only point-recovery comparisons, not
answers to the new interval problem or automatic revalidation of old source.
The driver compares the 48 old point-case projections after independent
new reports agree. Exact old δ values map to duplicated BP endpoints.

Use `qr05bp-source-freeze-v1` and `qr05bp-capture-v1` with exact source maps
and freeze-digest binding, fresh checked execution, immutable engine inputs,
strict JSON/native types, create-only writes, final source/freeze/artifact
readbacks and complete replays. Source text caps remain 262,144 bytes;
the prior capture and artifacts use the separate 16,777,216-byte cap.
Each analysis has 30 seconds and each suite 120 seconds. Preserve failed
evidence; any post-first source correction requires new named freeze/capture.

Run one normal and one optimized suite, one full replay per mode, and
exactly one alternate-runtime reference-only analysis comparing full native
and canonical reports plus old point recovery. Cache one new analysis per
suite; use focused mocks for lifecycle tests. No adaptive cap increase,
additional fixture scan, record/quantum/chart enumeration, timing-sensitive
RET overlap, dependencies, hardware or external-data collection.

## Reproduction and limits

After retained evidence exists, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bp.py
python3 -I -O -B test_qr05bp.py
```

Initial `--freeze source-freeze.json` and `--capture results.json` are
exclusive. Record outcomes in [RESULTS.md](RESULTS.md). Passing this gate
does not calibrate probability intervals, produce finite-shot confidence,
recover general density/metric structure, derive QM/gravity, validate
ontology or release RET applications. Book work remains archival; Lean,
physical clocks and later gravity couplings remain separate.
