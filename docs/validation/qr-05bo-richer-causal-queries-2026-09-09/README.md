# QR-05BO: richer marked-causal queries under density uncertainty

9 September 2026 (Pacific/Honolulu). Prospective specification, written
before implementations or fixed numerical execution. Continue the
[BN result](../qr-05bn-bounded-density-identification-2026-09-09/RESULTS.md)
by adding one specified observation, not by changing physical laws.

## Continuous model and supplied access

Keep auxiliary null coordinates u,v, signature (+,−), marked events
o=(0,0), m₁=(1/2,1/2), t=(1,1), and add m₂=(3/4,1/2). Their strict
causal intervals are Q=(0,1)², I₁=(0,1/2)² and
I₂=(0,3/4)×(0,1/2); I₁⊂I₂⊂Q. For η∈{0,1}, s∈{1,4},

```text
ds²=s(1+ηuv)du dv,  dμ=s(1+ηuv)du dv/2,
ρδ=1+δuv,  δ∈[0,2],
dν=ρδdμ/∫Qρδdμ,
τ=μ(I₁)/μ(Q)=(16+η)/[16(4+η)].
```

The density is scalar relative to proper volume. It is not another metric
Jacobian. Four externally supplied closed bounds are [0,0], [0,1/2],
[0,1], [0,2]. Geometry/density parameters remain unknown. The continuous
δ family is not replaced by the finite implementation fixtures below.
Scale labels remain distinct even when targets or laws coincide.

Marks, causal-comparator access, a loss-free sampler and four fresh iid
points are supplied premises. For each point Xj observe the same-attempt
pair (Y₁j,Y₂j)=(1{Xj∈I₁},1{Xj∈I₂}). The bits within a pair are not
independent. Exact population q=(q₁,q₂) gives one-point probabilities,
in lexicographic symbol order 00,01,10,11,

```text
p=(1−q₂, q₂−q₁, 0, q₁).
```

Four-attempt probabilities are products across attempts only. Retain all
256 ordered symbol words, including zero branches. The wrong product of
marginal Bernoulli laws assigns q₁(1−q₂)>0 to 10 for every admitted world;
retain this as a rejected channel control, not a physical alternative.
The old Y₁ marginal must exactly recover its full four-bit Bernoulli law.
Under the stipulated nested iid model the two counts determine all three
nonzero category counts; preserving pairing for channel/packet auditing
does not imply that attempt order is statistically necessary for estimation.

## Polynomial reconstruction versus geometric factorization

Write the normalized sampling density relative to du dv as
f=c₀+c₁uv+c₂u²v². It belongs to span{1,uv,u²v²} in this model. For an
origin-anchored rectangle with t=ab, its moment row is
(t,t²/4,t³/9). Let M have rows for Q,I₁,I₂ in that order. These have
three distinct positive t values, so the determinant is a nonzero scaled
Vandermonde product. The executable certificate retains M, its exact
determinant, inverse and both inverse identities.

Thus M c=(1,q₁,q₂) reconstructs the complete normalized polynomial within
this span, not an arbitrary density outside it. A unique moment solution
can be signed or outside the geometric family; call it `moment_solution`
until admission is established. It is not automatically a physical density.

For family admission, c₀ must be positive. Define α=c₁/c₀, β=c₂/c₀.
For each η, the only factorization candidate is δ=α−η. Require
β=ηδ, the externally supplied closed bound, normalization and both forward
probabilities. Preserve both scale labels. The positive constant coefficient
is checked before division, including a prespecified c₀=0 control.

An independent inverse uses the first query alone:

```text
q₁=(a+bδ)/(c+dδ),
(a,b,c,d)=(144+9η,9+η,576+144η,144+64η),
(dq₁−b)δ=a−cq₁.
```

Guard the zero divisor, retain every nonpole algebraic candidate, intersect
with the closed bound, then test the second query with its own forward
mass ratio. A point-law reconstruction and this η-wise inverse must yield
the same admitted labeled worlds, exact δ values and discrete target sets.
Do not infer factorization merely from the rank of M.

The unchanged whole-point collision η=0,δ=1 versus η=1,δ=0 must survive
every common added channel. Their targets differ by 3/80. Test whether
this particular second mark separates BN's q₁=1/5 pair, η=0,δ=16/11
versus η=1,δ=45/158; unequal point laws alone do not prove that it will.
Metric scale s must remain absent from normalized observations.

## Fixed verification domain

The [protocol](protocol.json) fixes 16 validation worlds: for each scale,
flat δ∈{0,1,2,16/11} and conformal δ∈{0,1,2,45/158}. These probe the
continuous solver; compatible δ values must be derived, never looked up
from this grid. World order is the eight scale-one fixtures below, then
their scale-four copies. IDs are flat_0, flat_1, flat_2, flat_interior,
conformal_0, conformal_1, conformal_2, conformal_interior, then each ID
with `_x4` appended.

Population data comprise those eight scale-one pairs, in the same order,
then four declared pairs: `zero`=(0,0), `one`=(1,1),
`equal`=(1/4,1/4), `zero_constant`=(1/16,9/64). The last is the
moment pair for normalized density 4uv, outside this positive-constant
factor family. The controls are valid nested probability pairs, not extra
admitted worlds. They test model infeasibility independently of input syntax.
Population data are stipulated exact laws, not probabilities accessible
from one four-attempt packet or frequencies promoted to exact inputs.

Four bounds ×12 data give 48 cases, each retaining all four geometry/scale
hypotheses. Also retain all 36 adjacent-bound inclusion checks. No adaptive
data selection, density fitting, extra mark or post-run fixture expansion.

Every admissible density is positive and each of Q\I₂, I₂\I₁ and I₁ has
positive measure. Hence the same 81 four-attempt words have positive
probability for every admissible parameter; the other 175 contain 10.
Support alone cannot select geometry from a possible word, and an impossible
word does not identify a detector fault or authorize data repair. No finite-
shot confidence procedure is implemented. Preserve all 256 support rows.

## Exact native report contract

Independent `primary.py` and `reference.py` expose `analyze(protocol)` and
use no shared mathematical code or file access. Native trees contain only
plain dict/list/str/int/bool and Fraction; no float/None. All computed
scalar numbers, including polynomial/matrix entries and zero probabilities,
are Fractions. Metadata η,s, exponents and record bits are ints. Empty sets
use []. Coefficient vectors follow basis (1,uv,u²v²).

- Top: `schema`="qr05bo-report-v1", `reconstruction`, `worlds`, `data`,
  `cases`, `classes`, `collisions`, `scale_pairs`, `monotonicity`, `support`.
- `reconstruction`: `moments` (3×3 Fraction rows Q,I₁,I₂), `determinant`,
  `inverse` (3×3), `left_identity`, `right_identity` (bools).
- World rows in protocol order: `id`, `eta`, `scale`, `delta` (Fraction),
  `volumes` ([Q,I₁,I₂] Fractions), `target`, `mass_coefficients`
  (three [constant,δ] Fraction rows in Q,I₁,I₂ order), `mass` (three
  Fractions), `normalized_coefficients` ([c₀,c₁,c₂]), `q` ([q₁,q₂]),
  `one_point` (four Fractions), `records`, `marginal`, `recovered`
  (three Fractions), `reconstruction_equal`, `marginal_equal` (bools),
  `independent_10` (Fraction). Every lexicographic four-symbol `records`
  row has `y` (four two-int lists), `p` (Fraction). Every lexicographic
  four-bit `marginal` row has `y` (four ints), `p` (Fraction).
- Data rows in specified order: `id`, `q` (two Fractions),
  `moment_solution` (three Fractions), `one_point` (four Fractions).
- Case rows bound-major then data order: `id`=`bound/data`, `bound`,
  `data`, `q`, `hypotheses`, `worlds` (feasible geometry labels, not fixture
  IDs), `targets` (sorted unique Fractions), `status` ("infeasible",
  "identified", "ambiguous"). Geometry-label order is flat,conformal,
  flat_x4,conformal_x4; each labels a continuous δ family.
- Each hypothesis: `id`, `inverse_numerator`, `inverse_denominator`
  (Fractions from actual I₁/Q affine mass coefficients including scale),
  `candidate` ([] at a pole, else singleton Fraction list even if rejected),
  `delta_set` ([] or one admitted Fraction), `status` ("infeasible" or
  "feasible"), `second_residual` ([] unless candidate lies in bound;
  otherwise singleton Fraction equal to M(I₂)−q₂M(Q)),
  `normalized_coefficients` ([] unless admitted, else three Fractions).
  Bound-admitted candidates may still fail the second query.
- `classes`: `first`, `joint`, `point`, each a list of classes in first
  member order across all 16 fixtures. Each class has `worlds` (fixture IDs),
  `targets` (sorted unique Fractions), `identified` (bool). Use complete
  first/paired record laws and complete polynomial coefficients separately.
- Collisions in order inherited_whole_point, membership_only: `id`,
  `worlds` ([flat_1,conformal_0] or [flat_interior,conformal_interior]),
  `first_equal`, `joint_equal`, `point_equal` (bools), `q2_gap` (left−right
  Fraction), `target_gap` (left−right Fraction).
- Eight scale pairs, scale-one fixture order: `worlds` ([id,id_x4]),
  `volume_factor` (Fraction), `target_equal`, `point_equal`, `joint_equal`
  (bools). Absolute volumes in all three regions must scale consistently.
- 36 monotonicity rows, adjacent-bound-major then data: `tight`, `broad`,
  `data`, `world_subset`, `target_subset`, `nuisance_preserved` (bools).
- 256 support rows, lexicographic symbol-word order: `y`, `possible`
  (bool), `worlds` (all four geometry labels if possible, else []),
  `targets` ([17/80,1/4] if possible, else []). This supports all four
  bounds and every continuous admissible δ, not only the validation grid.

Primary integrates monomials, uses elimination for matrix inversion and
the q₁ inverse plus q₂ residual for admission. Reference integrates direct
functions by tensor Simpson, uses a cofactor inverse, interpolates point
coefficients and admits through reconstructed factorization. It still
retains q₁ candidates/residuals for comparable diagnostics. A third test
oracle independently uses rectangle endpoint moments, a determinant/linear
solve, forward substitution and exact scalar word laws. Compare entire
native reports with exact types before canonical encoding or hashing.

## Public population-pair boundary

`study.identify(query)` accepts exactly a plain dict with keys `schema`,
`data_kind`, `q`, `density_bound`, `bound_basis`. Plain string metadata are
`qr05bo-query-v1`, `population_pair`, one of uniform/half/one/two, and
`external_assumption`. `q` is a plain list of two plain two-int reduced
rational lists; denominators positive, 0≤q₁≤q₂≤1. Each supplied integer
has absolute value at most 2³¹−1, checked before gcd/Fraction arithmetic.
No records, frequency-specific schema, hidden geometry/density/world/state
fields, bool/float/subclass substitution or extra fields are accepted.
Malformed/out-of-cap/non-nested inputs raise ValueError. A legal nested
pair outside the model returns an empty compatibility result.

This solver accepts bounded rational pairs beyond the twelve fixtures;
its continuous inverse is analytically specified above. Finite tests do
not exhaust all permitted machine inputs or certify arbitrary densities.
Two prespecified non-fixture API checks use δ=1/3 for η=0 and η=1,
each under the half bound; these are not additional report worlds or scans.
It uses only public family formulas and query premises, not fixture IDs,
previous captures, files or engines. It returns exactly `worlds`, `targets`,
`status`, `nuisance` ([{`id`, `delta` Fraction}] for feasible hypotheses).
All containers are detached. Neither a number nor its provenance tag can
authenticate population knowledge or a density bound; a disguised finite
frequency cannot be detected solely from its value.

## Evidence discipline and work limits

Reuse only fresh authenticated bytes of BM's utility driver, SHA-256
`157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55`,
for exact codecs/comparison, bounded regular I/O, exclusive writes and
deadline helpers. Keep its isolated globals; never call earlier mathematical
engines, estimators or publication wrappers. BO owns its source inventory,
protocol pin, schemas and freeze/capture/replay lifecycle.

Create a new source freeze before any mathematical execution. Nine identities
bind BO README, protocol, primary, reference, study, test_qr05bo plus BN
README/RESULTS and the BM utility driver. Use `qr05bo-source-freeze-v1` and
`qr05bo-capture-v1`; bind exact source bytes and the freeze digest. Enforce
strict JSON/native types, immutable inputs, fresh checked-source execution,
create-only writes, final source/freeze/artifact readback and full replay.
Any post-first-evaluation source correction requires a separately named
freeze/capture, preserving all previous evidence and recording the failure.

Coverage: 16 worlds/4,096 paired-record rows/256 first-marginal rows,
12 data/48 cases/192 hypothesis rows, 36 inclusion checks, 256 support rows,
two collision and eight scale controls. Caps are 262,144 bytes per source,
16,777,216 per artifact, 30 seconds per analysis and 120 seconds per suite.
Run one normal suite and one optimized suite, one complete replay per mode,
and exactly one alternate-runtime reference-only analysis comparing full
native and canonical reports. Cache one full analysis per suite and use
small mocks/retained mutations for lifecycle tests. No adaptive cap increase,
fixture scan, extra quantum/chart enumeration, timing-sensitive RET overlap,
dependency installation, hardware or external-data collection.

## Reproduction and limits

Once the evidence exists, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bo.py
python3 -I -O -B test_qr05bo.py
```

Initial `--freeze source-freeze.json` and `--capture results.json` are
exclusive operations, not overwrite commands. Record outcomes in
[RESULTS.md](RESULTS.md). No result here validates ontology, derives QM or
gravitational dynamics, identifies general metrics, calibrates acquisition,
or releases RET applications. Book work remains archival; physical clocks,
Lean installation and later gravity couplings remain separate.
