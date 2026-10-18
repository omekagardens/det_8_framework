# QR-05BR: bounded finite-record confidence verification

9 September 2026 (Pacific/Honolulu). Prospective specification, fixed before
the first numerical evaluation. Continue the analytical
[BQ contract](../qr-05bq-finite-record-uncertainty-design-2026-09-09/README.md)
and [decision](../qr-05bq-finite-record-uncertainty-design-2026-09-09/RESULTS.md).
This verifies a finite implementation of that construction, not its physical
sampling premises or a confidence level conditional on a selected answer.

## Model, construction and finite domain

Keep signature (+,−), Q=(0,1)², I₁=(0,1/2)², I₂=(0,3/4)×(0,1/2),
the supplied marked causal comparisons, and

```text
ds²=s(1+ηuv)du dv,       dμ=s(1+ηuv)du dv/2,
ρδ=1+δuv,               δ∈[0,2], η∈{0,1}, s∈{1,4},
q_i=∫Iiρδdμ/∫Qρδdμ,    τ=(16+η)/[16(4+η)].
```

The target is 1/4 or 17/80. Density bounds uniform, half, one, two are
[0,0], [0,1/2], [0,1], [0,2], selected externally and required to contain
the true δ for target coverage. Each of four fresh iid points answers BOTH
questions, with symbol probabilities (1−q₂,q₂−q₁,0,q₁) in order00,01,10,11.
Marks, association, iid/no-loss sampling and density/geometry remain supplied
premises. Attempt order is not a physical clock; counts are not exact laws.

Freeze n=4, total α=1/20, four one-sided allocations 1/80, grid G={j/256}.
For inclusive binomial tails T⁺(k;p)=P_p(K≥k), T⁻(k;p)=P_p(K≤k), use

```text
L(k)=max({0}∪{g∈G:T⁺(k;g)≤1/80}),
U(k)=min({1}∪{g∈G:T⁻(k;g)≤1/80}).
```

Use closed intervals, exact reduced rationals and explicit degenerate p=0,1
laws. L(0)=0 and U(4)=1. Selected nondefault grid endpoints satisfy the
tail threshold and their next inward grid neighbor has tail strictly above
it. The continuous-parameter coverage proof is BQ's threshold-in-count and
four-event union argument, not a scan over grid probabilities. Rounding
widens the exact inverse; grid precision is not acquired information.

Every valid batch has counts 0≤k₁≤k₂≤4, category exponents
(4−k₂,k₂−k₁,k₁) and multiplicity 4!/[(4−k₂)!(k₂−k₁)!k₁!]. Retain all
15 count states in k₁-major, then k₂ ascending order, not all ordered words.
Their exact probabilities use the multinomial law, not independent binomial
counts. The simultaneous box is [L(k₁),U(k₁)]×[L(k₂),U(k₂)].

For each of four geometric labels, region masses M_R=A_R+B_Rδ retain
actual scale s. The four affine inequalities M_Ii−L_iM_Q≥0 and
U_iM_Q−M_Ii≥0 constrain the SAME δ in the external bound. Retain the
complete empty/closed nuisance interval and coupled endpoint laws; coordinate
range products are not declared attainable. Targets remain discrete sets.

The [protocol](protocol.json) fixes six unit-scale fixtures: flat δ=0,1,16/11
and conformal δ=0,1,45/158. Each has 15 count-law probabilities. Keep all
24 fixture/bound summaries with original weights, including bounds excluding
the actual fixture δ. Population-box coverage holds for every fixture;
target coverage is enforced only when the true δ lies in the supplied bound.
An out-of-premise result is neither a theorem failure nor a calibrated bound.

Analytical controls are unchanged: all00 retains all nuisance domains and
both targets; all11 gives an empty inverse because L(4)≥5/16>q₁,max.
Neither output diagnoses hardware. The whole-point pair flat1/conformal0
has the same law and different targets. The two interior fixtures share
q₁=1/5 but differ in q₂; no promise of useful finite-record separation follows.
The three allowed categories are positive throughout δ∈[0,2], giving 15
positive count states, 81 possible and 175 zero four-attempt words analytically.

Two separate private-helper ties use ε=1/16, not the main budget:
T⁺(4;1/2)=1/16 and T⁻(0;1/2)=1/16. Their selected endpoints are1/2.
The main dyadic table cannot equal1/80. Preserve selected/adjacent witnesses
and reject an inward-endpoint substitution; do not claim such a substitution
necessarily fails a measured coverage test. A wrong independent-question
law assigns10 probability q₁(1−q₂)>0; retain this control per fixture.

Two fixed private-driver inverse regressions, not public packet inputs or
main report fixtures, use bound[0,2]: [1/16,1/16]×[0,1] must give an empty
answer without inverse-pole division; [3/16,17/80]×[21/64,3/8] must retain
flat δ=[1,1] and conformal δ=[0,0], plus their scale copies. These exercise
zero-slope and shared-parameter singleton guards without a further scan.

## Independent routes and exact report contract

Primary uses integer binomial numerators, monomial integration, affine
halfspaces and multinomial weights. Reference uses Bernoulli convolution/
cumulative tails, direct tensor Simpson integration, attainable-range-first
inversion and paired count-space dynamic programming (also for multiplicities).
Neither reads files, imports the other or executes historical engines. Tests
use n=4 closed tail polynomials, endpoint integrals and a breakpoint/cell
forward-ratio oracle. Compare the ENTIRE native report before encoding.

All trees use plain dict/list/str/int/bool and Fraction. All mathematical
scalars, masses, probabilities, roots and interval endpoints are Fractions;
metadata counts, k, η,s, grid denominator, exponents and multiplicities are
ints. No floats or None. Every δ interval is [] or [lo,hi], duplicating
singletons; endpoint-law rows are always two for a feasible hypothesis.

- Top: `schema`="qr05br-report-v1", `confidence`, `tails`, `intervals`,
  `counts`, `geometries`, `cases`, `fixtures`, `summaries`, `scale_pairs`,
  `comparisons`, `ties`, `obstruction`, `support`.
- `confidence`: `quota`=4, `alpha`=1/20 Fraction, `tail_allocations` four
  Fractions in query1lower/upper, query2lower/upper order, `grid_denominator`=256,
  `confidence_basis`="fixed_iid_paired_binomial_union",
  `bound_basis`="external_assumption", `coverage_kind`="unconditional_model_relative".
- `tails`: k-major0..4, then grid-index0..256; each `k` (int), `grid` (Fraction),
  `plus`, `minus` (Fractions). 1,285 rows contain 2,570 tail values.
- `intervals`: k0..4, each `k`, `interval`=[L,U], `lower`, `upper`.
  Each endpoint certificate has `kind`="default" or "tail", `grid` (selected
  endpoint), `tail` (actual tail at it), `neighbor`=[] for default or
  [[adjacent-grid, adjacent-tail]] otherwise. Lower default only k0, upper
  default only k4; their tail is Fraction1. Nondefault neighbor points one
  grid step inward and has tail>ε, while selected tail≤ε. Use this same
  certificate shape for the separate tie controls.
- `counts`: each `id`="k1/k2", `k`=[int,int], `category_counts`=[c00,c01,c11],
  `multiplicity` (int), `intervals` (two [L,U] Fraction rows),
  `nested_nonempty` (bool, L₁≤U₂).
- `geometries` in protocol order: `id`, `eta`, `scale`, `volumes` (Q,I₁,I₂),
  `target`, `mass_coefficients` (three [A,B] rows), `derivative_numerators`
  (two B_i A_Q−A_i B_Q values), `full_q_ranges` (two sorted endpoint ranges
  on[0,2]), `category_coefficients` (three [A,B] rows00,01,11), `strict_support`.
- `cases` bound-major then count order: `id`="bound/k1/k2", `bound`, `count`
  (count ID), `intervals`, `nested_nonempty`, `hypotheses`, `worlds`, `targets`,
  `status`="infeasible"|"identified"|"ambiguous". Worlds are feasible IDs in
  geometry order; targets sorted unique Fractions.
- Each hypothesis: `id`, `inequalities` (four rows, q1lower/upper thenq2),
  `query_sets` (two empty/closed intervals including the bound), `delta_set`,
  `status`="feasible"|"infeasible", `curve`. Inequality rows: `constant`,
  `slope`, `kind`="all"|"none"|"lower"|"upper", `boundary`=[] for zero slope,
  otherwise [raw root−constant/slope], even outside the bound.
- `curve`={} if infeasible; otherwise `domain`, `numerators` (two actual
  [A_i,B_i] rows), `denominator`=[A_Q,B_Q], `one_point_numerators` (four
  [A,B] rows00,01,10,11, including Fraction-zero row), `endpoints` (two rows
  `delta`, `q` [q₁,q₂], `one_point` four probabilities), `q_ranges` (two
  sorted endpoint projections). All endpoint probabilities use the same δ.
- `fixtures` in protocol order: `id`, `eta`, `delta` (Fraction), `target`,
  `q`, `one_point`, `count_law` (15 rows `count` ID, `p` Fraction,
  `population_covered` bool), `independent_10`=q₁(1−q₂),
  `count_covariance`=4q₁(1−q₂). Recompute the covariance from the full count
  law and verify binomial marginals, normalization and strict positivity.
- `summaries` fixture-major then bound: `id`="fixture/bound", `fixture`,
  `bound`, `in_premise` bool; Fractions `population_noncoverage`,
  `target_noncoverage`, `empty`, `singleton`, `wrong_singleton`, `ambiguous`;
  `conditional_wrong_singleton`=[] if singleton probability0, otherwise
  [wrong_singleton/singleton]; `population_bound_holds`, `target_bound_holds`
  bools comparing the respective noncoverage to α. Always retain actual
  values, including out-of-premise rows. Enforce population bound everywhere;
  enforce target-miss event containment and target≤population≤α only in-premise.
  Always enforce empty+singleton+ambiguous=1 and target_miss=empty+wrong_singleton.
- `scale_pairs`: flat/flat_x4 then conformal/conformal_x4; each `worlds`,
  `volume_factor` Fraction, `target_equal`, `nuisance_sets_equal`,
  `curve_laws_equal` bools across all60 cases. Check actual region/mass/curve
  scaling as well as normalized equality. No duplicate fixture probability bank.
- `comparisons`: `id`="whole_point" (flat_1/conformal_0), then
  "membership_only" (flat_interior/conformal_interior); each `fixtures`
  [twoIDs], `q1_equal`, `q2_equal`, `count_law_equal` bools (compare probability
  vectors, not fixture IDs), `target_gap` and `q2_gap` first−second Fractions.
- `ties`: protocol order; `id`, `side`, `k`, `epsilon` Fraction, `certificate`
  (endpoint shape above, evaluated with the private ε, unchanged grid).
- `obstruction`: `worlds`=[flat,conformal], `deltas`=[1,0] Fractions, `q`
  common pair, `point_equal` bool (check normalized whole-point polynomials,
  not just pair equality), `target_gap` Fraction; `cases` (60 rows `case`,
  `flat_present`, `conformal_present`, `both`, `target_ambiguous` bools),
  `coverage` (four bound-order rows `bound`, `both_in_premise`,
  `both_target_probability` Fraction, `bound_holds` bool for probability≥1−α).
  Sum using the common fixture count law; enforce this bound only when both
  actual compensated density parameters lie in the external bound.
- `support`: `symbols`=[[0,0],[0,1],[1,0],[1,1]], `allowed`=[[0,0],[0,1],[1,1]],
  `count_states`=15, `possible_words`=81, `zero_words`=175,
  `continuous_certificate` bool from all geometric category-mass certificates.

## New record interface

`study.infer_records(query)` accepts exactly plain-string keys `schema`,
`protocol_id`, `data_kind`, `records`, `density_bound`, `bound_basis`, in a
plain dict. String values are "qr05br-record-query-v1",
"qr05br-n4-g256-a20-v1", "paired_causal_records", uniform/half/one/two,
"external_assumption". `records` is a plain list of exactly four plain
dicts with keys `attempt`, `bits`. Attempts must be native ints1,2,3,4 in
that order; bits a plain length-two list of native ints0or1 (not bool).
Repeated symbol values are allowed. Validate EVERY field/row before any
counting or mathematical work, then detect10. A malformed later row must
not be hidden by an earlier10. Wrong types, quotas, IDs, schemas or extra
fields raise ValueError. Impossible10 is a separate well-shaped refusal.

Return exactly `schema`="qr05br-record-result-v1", `status`, `reason`,
`confidence`, `counts`, `intervals`, `answer`. Accepted status="accepted",
reason="", confidence=the report confidence metadata, counts=[k₁,k₂],
intervals=the constructed box; answer has exactly `nested_nonempty`,
`worlds`, `targets`, `status` and `nuisance` (feasible {`id`,`delta`:[lo,hi]}
rows). Refused status="refused", reason="impossible_nested_symbol",
confidence={}, counts=[], intervals=[], answer={}. This is not the ordinary
accepted answer with an empty target set. All output containers are detached.

The public routine computes directly from the fixed formulas, not fixture
lookup, prior outputs, files or engines. It uses no old external-population
API/provenance tag and accepts no caller-chosen budget/interval/frequency,
actual-world label, coordinate, seed or target. Its declaration does not
authenticate the record stream or physical independence. Correctness tests
cover all15 count states and4 bounds via canonical valid representative
packets plus fixed malformed/impossible/association controls, not a new
enumeration of all paired words.

## Freeze, validation and claim boundary

Before any mathematical run freeze eleven identities: six BR files
README/protocol/primary/reference/study/test_qr05br, BQ README/RESULTS,
BP README/RESULTS and the BM utility driver. Reuse only fresh authenticated
BM utility bytes (SHA-256
`157b4f19725d3ead456eda2b74f3e2452ceb067ef8b0edd463a2367e48bd8a55`)
for codecs/comparison, bounded I/O, exclusive writes and deadlines. Keep its
globals isolated; BR owns its analysis, public API and evidence wrappers.
No previous mathematical engine, estimator, publication wrapper or test runs.

Use `qr05br-source-freeze-v1` and `qr05br-capture-v1`, exact source maps,
freeze binding, full native comparison, canonical JSON, immutable inputs,
fresh checked code, create-only outputs and final source/freeze/capture
readbacks. Caps are262,144 bytes per source and16,777,216 per artifact;
analysis30s, suite120s. Run one normal and one optimized suite (one cached
full analysis each), one full replay per mode and exactly one alternate-
runtime reference-only analysis comparing whole native and canonical reports.
Retain failures; a post-first source correction needs new named evidence.

No outcome-dependent fixtures, adaptive cap/precision increase, additional
grid/world scan, old engine rerun, exponential paired-word bank, quantum/chart
enumeration, timing-sensitive RET overlap, dependencies, devices or external
data. Verify exact tail/certificate/coupling/count/coverage/interface and
evidence contracts; useful precision or a chosen singleton rate is NOT a
success condition. Continuous coverage is BQ's analytical theorem, not
exhaustive formal machine verification or evidence about a physical apparatus.

After capture, reproduce from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05br.py
python3 -I -O -B test_qr05br.py
```

Initial `--freeze source-freeze.json` and `--capture results.json` are
exclusive. Record outcomes in [RESULTS.md](RESULTS.md). Do not drop ordinary
empty sets, select singleton-only success rates, or claim coverage under a
false density premise. No ontology, altered physical law, metric/gravity
recovery, apparatus calibration, RET release or quantum advantage is claimed.
Book work remains archival; Lean, clocks and later dynamics remain separate.
