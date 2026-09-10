# QR-05BT: bounded separation and budget verification

9 September 2026 (Pacific/Honolulu). Prospective specification, fixed before
the first mathematical evaluation. Continue the analytical
[BS contract](../qr-05bs-separation-budget-design-2026-09-09/README.md) and
[decision](../qr-05bs-separation-budget-design-2026-09-09/RESULTS.md).
This gate verifies exact separation and rational planning certificates.
It does NOT evaluate a large-quota confidence table or collect records.

## Model and fixed domain

Keep signature (+,−), Q=(0,1)², I₁=(0,1/2)² and I₂=(0,3/4)×(0,1/2):

```text
ds²=s(1+ηuv)du dv,         dμ=s(1+ηuv)du dv/2,
ρδ=1+δuv,                η∈{0,1}, s∈{1,4}, δ∈[0,2],
M_z(δ)=(s/2)[z+(η+δ)z²/4+ηδz³/9],
q_i=M_Ii/M_Q,            τ=(16+η)/[16(4+η)].
```

Density bounds uniform, half, one, two are [0,b] with b=0,1/2,1,2.
The six unit-scale fixtures are flat δ=0,1,16/11 and conformal δ=0,1,45/158.
Each true point is compared with the ENTIRE opposite-target segment on
the same external bound, not a chosen competing fixture. Preserve actual
true-bound membership, including out-of-premise rows.

Every normalized family is an exact segment. For z∈{1/4,3/8},

```text
q_0,z=(1−t₀)z+t₀z²,              t₀=δ/(4+δ),
q_1,z=(1−t₁)(4z+z²)/5+t₁(9z²+4z³)/13,
                                t₁=13δ/(45+13δ).
```

The supporting lines are −20q₁+16q₂=1 and −9520q₁+7296q₂=371.
Their only intersection P=(17/80,21/64) comes from flat δ=1 and
conformal δ=0. Retain the identical normalized whole-point polynomial
(4/5)(1+uv) and unequal targets there. Scale does not change normalized
curves, distances or targets.

For a point p, write its competing segment a+t v, t∈[0,1]. Primary
chooses t*=clip((p₁+p₂−a₁−a₂)/(v₁+v₂)); b=0 is a point and has t*=0.
Reference selects the minimizer independently from t=0,1 and the in-range
roots of r₁, r₂, r₁−r₂ and r₁+r₂, where r=p−a−tv. It must not use the
balance quotient to choose the minimizer. Deduplicate candidates and handle
constant/identically-zero equations explicitly. Both routes retain the
same closed contact, raw-balance diagnostic and exact sup distance d.

Recover competing density by 4bt/[4+b(1−t)] for flat, or
45bt/[45+13b(1−t)] for conformal. Verify the original mass-ratio forward
point, not only a line equation. Both segment directions are strictly
negative when b>0; all mass normalizers are positive on [0,2].

## Canonical lower certificates

Retain w with ||w||₁≤1 and the affine function
w·(p−a−tv)=c+mt. Its two endpoint values must be ≥d and its value at
t* must equal the attained norm d. This proves a lower bound on the
whole segment and equality at the witness, not a grid search.

Canonical contact kind is point if b=0, otherwise start for t*=0,
end for t*=1, interior otherwise. Independently retain raw location
point/before/start/interior/end/after according to the unclipped balance.

Choose w by these rules, in this order:

- If d=0, w=(0,0), retaining the geometric contact kind.
- Point with d>0: first coordinate attaining |r_j|=d, w=sign(r_j)e_j.
- Start with d>0: first coordinate with r_j=d, w=e_j.
- End with d>0: first coordinate with r_j=−d, w=−e_j.
- Interior with d>0: w=(sign(r₁)|v₂|,sign(r₂)|v₁|)/(|v₁|+|v₂|).

For the whole-class margin, choose density contact (b,0) for b<1 and
(1,0) for b≥1. Use w=(0,1) in the first branch, w=(0,0) in the second.
For segments a_F+t v_F and a_C+s v_C, retain the bilinear-domain affine
lower function w·(a_F−a_C+t v_F−s v_C). Its four corner values in
(t,s)=(0,0),(0,1),(1,0),(1,1) order must be ≥d, with equality at the
contact. The segments are complete continuous families, so their affine
corner certificate covers every pair. Compare the attained value with

```text
D([0,b])=3(1−b)/[16(4+b)] for b<1, and 0 otherwise.
```

An attained zero plus norm nonnegativity certifies zero separation; a
failed positive budget check does not certify impossibility.

## Fixed planning and derived controls

Keep n=65,536, m=256, h=1/m, α=1/20 and four ε=1/80. For every pointwise
distance and whole-class margin, retain slack=d−2h, score=n·slack²,
the SEPARATE signs/checks slack>0 and score≥10, their conjunction and
true-premise eligibility. Preserve the actual score even if slack≤0;
squaring must not hide the sign requirement.

BS proves ln(80)<5 and maximum confidence-box side width at most
2sqrt(ln(80)/(2n))+2h. Thus the rational check with slack>0 and score≥10
is sufficient for strict width<d. Only when the true premise also holds
does this give P(correct singleton)≥19/20 and
P(wrong | singleton)≤1/20. Retain failed and out-of-premise rows honestly.
These are design certificates, not observed-record or posterior answers.

Recompute the six positive exponential-series terms 5^j/j!, j=0..5,
whose sum is 1097/12>80. One separate algebraic helper control uses
n=40,m=8,R=1/4,d=3/4: both 2nR²=5 and 2R+2h=d, equivalently score=10.
Strict logarithmic slack makes those rational equalities safe. No n=40
tail/count law, geometric fixture, acquisition or new scan is introduced.

Exactly six box controls use the two interior fixture/B=two rows.
In fixture order construct half_square centered at p with radius d/2,
touch_square centered at p with radius d, and contact_rectangle, the
coordinatewise bounding rectangle of p and its nearest competing point.
Retain the exact coupled opposite-density interval using the SAME δ.
The first excludes the opponent; the other two admit the closed nearest
contact. The contact rectangle has full max width d and half-width d/2<d,
showing that neither a half-width rule nor a non-strict full-width≤d rule
proves exclusion. The half-square also shows strict full-width<d is
sufficient, not necessary. These are algebraic boxes, not newly acquired
confidence outputs.

Read only the authenticated stored BR five count intervals for the coarse
baseline. Retain their widths, maximum, all maximizing k and strict
maximum-width comparisons against all 28 distances. This is not a BR rerun
or a claim that failure of this bound prevents individual identification.

## Independent execution and native report wire

Both new engines expose analyze(protocol, baseline). Primary uses monomial
mass coefficients, clipped balance and affine inequalities for boxes.
Reference uses independently integrated masses, breakpoint minimization
and probability-segment box clipping. Neither imports the other, reads
files, executes old mathematics or loops over the large quota/grid.
Tests use forward contacts with dual/affine lower bounds, original ratio
constraints, analytical class margins and rational arithmetic.
Both inputs must remain unchanged. Validate their exact native contracts
before mathematical work, including bool-versus-int and rational types.

All report containers are plain dict/list; all keys and strings plain str.
Metadata η,s,n,m,k/counts are native int, flags bool, mathematical values
Fraction (including zeros). No floats, None, tuples or reserved $ keys.
Empty/singleton nuisance sets are [] or [lo,hi] with duplicated singleton
endpoints. Rows have exactly the fields listed below, in the stated order.

- Top: schema="qr05bt-report-v1", geometries, fixtures, distances, classes,
  plans, scale_pairs, baseline, boxes, rational_bound, rational_controls,
  obstruction.
- geometries: protocol order. id, eta, scale, volumes (Q,I₁,I₂),
  mass_coefficients (three [A,B] rows), derivative_numerators
  (B_i A_Q−A_i B_Q, two values), target, line (three Fractions
  [−20,16,1] or [−9520,7296,371]), positive_normalizer, decreasing.
  Actual scale is retained. Enforce positive normalization and negative
  derivative numerators on the full continuous density domain.
- fixtures: protocol order. id, eta, delta Fraction, target, masses (three
  unit-scale masses), q (two Fractions), one_point (00,01,10,11).
- segment object: start, end, vector, each two Fractions.
- distances: fixture-major then bound order. id="fixture/bound", fixture,
  bound, in_premise, opposite_eta, p (two Fractions), segment, projection,
  lower. Projection: raw=[] if point else[unclipped Fraction], t Fraction,
  location="point"|"before"|"start"|"interior"|"end"|"after", delta Fraction,
  q (contact), residual (p−contact), distance Fraction. Lower: kind=
  "point"|"start"|"interior"|"end", normal (two Fractions), coefficients
  [c,m], endpoint_values [c,c+m], norm (sum of absolute normal entries),
  value (minimum endpoint value). Require value=distance and contact
  evaluation=distance; raw endpoint ties keep start/end, not before/after.
- classes: bound order. bound, upper Fraction, segments [flat,conformal],
  kind="ordered"|"collision", deltas [flat,conformal] Fractions,
  parameters [t,s] Fractions, points [flat q,conformal q], residual,
  distance Fraction, closed_form Fraction, lower. The lower object has
  normal (two Fractions), coefficients [c,m_t,m_s], corner_values (four
  Fractions in declared order), norm Fraction and value (minimum corner).
  Canonical parameter at any point segment is 0, never 0/0.
- plans: all 24 distance rows then four class rows. id="pointwise/"+distance
  id or "class/"+bound; kind="pointwise"|"class", source (distance id or bound),
  distance Fraction, in_premise (actual flag, True for class), slack,
  score (Fractions), grid_positive, threshold_holds, sufficient, eligible,
  status="out_of_premise" if false premise, otherwise "certified" if sufficient
  or "not_certified"; guarantees=[] if ineligible, otherwise one dict with
  correct_singleton_at_least Fraction 19/20 and
  conditional_wrong_singleton_at_most Fraction 1/20.
- scale_pairs: flat/flat_x4 then conformal/conformal_x4. worlds (two IDs),
  volume_factor Fraction 4, actual_scaling, target_equal, segments_equal,
  distances_equal (bools). Verify actual volume/mass scaling and normalized
  input/contact/lower-certificate equality across the relevant fixed rows;
  this is a fixed scale comparison, not a new fixture probability bank.
- baseline: schema="qr05bt-br-baseline-v1", quota=4, grid_denominator=256,
  alpha Fraction 1/20, intervals (five rows k int, interval [L,U], width),
  max_width Fraction, maximizers (all k ints), comparisons (one per plan
  in plan order, id=plan id, distance Fraction, strict_width_sufficient bool).
- boxes: fixture-major then kind order specified above. id="fixture/kind",
  distance_id, kind, intervals (two [L,U] Fraction rows), widths (two
  Fractions), max_width, half_width (Fractions), contains_true,
  contains_contact, opposite_delta_set, admits_opposite,
  strict_width_condition (max_width<d), half_width_condition
  (half_width<d), nonstrict_width_condition (max_width≤d).
- rational_bound: terms (six Fractions), partial_sum Fraction, threshold
  Fraction 80, log_upper Fraction 5, strict bool.
- rational_controls: one row. quota=40, grid_denominator=8, radius,
  distance, step, square_score=2nR², width=2R+2h, main_score=n(d−2h)²
  (all Fractions except quota/grid denominator), radius_test (conjunction
  of R≥0, square_score≥5, width≤distance), direct_test (slack>0 and
  main_score≥10), strict_slack_basis="ln80_lt_5". Enforce both tests and
  both equality boundaries without evaluating logarithms.
- obstruction: deltas [1,0] Fractions, q common two Fractions,
  targets [1/4,17/80] Fractions, target_gap Fraction 3/80,
  normalized_polynomials (two equal length-three Fraction rows in basis
  1,uv,u²v²), point_equal bool.

The driver supplies exactly baseline={schema:"qr05bt-br-baseline-v1",
quota:4,grid_denominator:256,alpha:Fraction(1,20),intervals:[{k,interval}]}.
Its five intervals, inherited unchanged from BR, are [0,171/256],
[0,109/128], [3/64,61/64], [19/128,1], [85/256,1].
Engines validate that exact native baseline; the driver authenticates the
entire BR capture before parsing or extracting it. No confidence tail is
recomputed. The full [protocol](protocol.json) fixes all inputs and census.
No main outcome-dependent number of passing certificates is required.

## Source freeze, validation and boundary

Freeze twelve identities before any helper/oracle/engine/test evaluation:
six BT README/protocol/primary/reference/study/test files; BS README/RESULTS;
BR README/RESULTS/capture; and the BM utility driver. All source reads have
cap 262,144 bytes, except the BR capture has the artifact cap 16,777,216.
Its literal SHA-256 pin is
`9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c`,
checked before parsing. Only the five interval rows are new mathematical
inputs; full capture authentication is not inherited revalidation of BR.

Reuse only fresh authenticated BM codecs/comparison, bounded reads,
exclusive writes and deadlines, with isolated globals and literal source pin
`157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55`.
BT owns its analyze/freeze/capture/replay wrappers and schemas
qr05bt-source-freeze-v1 / qr05bt-capture-v1. Retain exact source maps,
freeze binding, native equality before encoding, fresh engine inputs,
canonical JSON, create-only outputs and final source/freeze/capture readbacks.
Do not execute any historical engine, estimator, publication wrapper or test.

Run one normal and one optimized suite (one cached full analysis per suite),
one full replay per mode, and exactly one alternate-runtime reference-only
analysis with whole native/canonical equality and final input/source checks.
Limits are 30s analysis, 120s suites and 16MiB artifacts. Retain failures; a
post-first source correction needs a new named freeze/capture, never a
silent overwrite. No adaptive cap, fixture, quota or precision change.

This gate has no new record-observer API. Actual fixture parameters and
planning certificates are research inputs/outputs, not inferred hidden
properties of a record stream. A certified quota is neither minimal nor
an acquisition command. Marks, iid/no-loss sampling and a correct external
density/model premise remain essential; conditional singleton reliability
is asserted only with the proved stronger separation/width conditions.

No numerical logarithms, large-quota tail/count computation, exponential
word bank, grid/world sweep, dependencies, timing-sensitive RET overlap,
devices, data collection, quantum-state/chart enumeration or RET integration.
No ontology, general metric or gravity recovery, scale identification,
instrument calibration, physical validation or quantum advantage is claimed.
Book work remains archival; Lean, clocks and later dynamics stay separate.

After capture, reproduce from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bt.py
python3 -I -O -B test_qr05bt.py
```

Initial --freeze source-freeze.json and --capture results.json are exclusive.
Record outcomes in [RESULTS.md](RESULTS.md), keeping every failed and
out-of-premise certificate visible.
