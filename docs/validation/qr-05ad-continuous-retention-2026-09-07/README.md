# QR-05AD protocol: continuous robust retention

7 September 2026. Prospective specification before AD coefficients, weights
or outcomes. Base: pushed AC commit 7712aa398b0c04eabdbcfa3d97c1ddf884f6e1d0.

## Frozen scope and evidence

Keep the six experiments, 482 original weighted histories, H2/K3/Q3,
four assumed/actual levels [0,1/2,3/4,1], declared finite sets t<=u,
whole-model 72 N-fibers/93 labels and AC's product of closed replacement
simplices. The same replacement law is shared across histories and levels.
Keep frozen g and f_s and EVERY AA/AC certificate unchanged.

Pin AC results.json: 1,783,649 bytes, SHA256
3fc5a502c214ba408e5f539133156b0ad81a2ef243545645dc980e7936932c18.
AC plus its 33 prior artifacts gives 34 immutable producer artifacts.

Now allow h_a=(1-a)g+a f_s for a in the CLOSED interval [0,1]. Choose one
weight for an entire experiment given an assumed model and declared bound,
not per history, report or unknown actual world. No forecasts outside this
segment, new calibration, changed target or history distribution.
Keep the three-weight menu [0,1/2,1] as a comparator in the SAME gate.

## Model-specific quadratic reduction

Using original clean history/report probabilities, independently derive

    D0 = E_clean ||f_s-g||^2,
    C0 = E_clean <p0-g,f_s-g>,
    S1 = sum_N max_z sum_H w_H P_H(N)||f_H,s(z)-g_H,N||^2.

The last quantity is the unchanged authenticated AC full-retention envelope.
Do not fit these coefficients to selected outcomes or polynomial samples.
Runner uses conditional-vector inner products; auditor expands literal
outcome-coordinate Brier loss using indicators I[q=coordinate] and original
UNNORMALIZED source joint masses.

The authenticated clean segment f_s-g=beta(p0-g), beta in [0,1], implies
C0>=D0>=0 and clean excess a^2 D0-2a C0<=0 for EVERY a in [0,1].
Full-replacement coefficients scale exactly as a^2. Thus

    E_t(a,mu*) = A_t a^2 - 2 B_t a,
    A_t=(1-t)D0+t S1, B_t=(1-t)C0.

A full-retention coefficient-maximizing mechanism mu* is a common witness
for every positive a; it also works at a=0, where every mechanism is tied.
The derivative in actual noise is a^2 S1+2a C0-a^2 D0>=0.
Hence at each declared bound u the robust objective is EXACTLY

    Q_u(a)=A_u a^2-2 B_u a.

Check all original three-weight Q values against AC candidate worst values.
The generic optimizer does NOT derive or assume this observation-model
reduction; those are separate producer/auditor obligations.

At a=0 or u=0 every mechanism is maximizing. Otherwise complete positive-
weight faces are AC's full-retention per-fiber faces. A canonical S1 witness
need not be AC's lex-first all-simplex witness when u=0; both are valid.
Retain a common witness, complete face rules and its actual laws.

## Generic convex-quadratic API

Two independent stdlib engines export analyze(problem), accepting EXACTLY

    {schema_version:"det8-qr05ad-problem-v1",
     family:"qr05ad_continuous_retention",
     levels:[[0,1],[1,2],[3,4],[1,1]],
     retained_weights:[[0,1],[1,2],[1,1]],
     decisions:[{assumed_index,bound_index,
                 quadratic_coefficient:A,half_linear_coefficient:B}]}

There are exactly 16 rows, assumed index outer 0..3 and bound index inner
0..3. Native indices, never bool/subclasses. Reduced native fraction pairs,
positive denominator, components <=4096 bits; A in [0,2], B in [-2,2].
No optional fields. This API certifies SUPPLIED convex quadratics on [0,1].
It authenticates no laws, prior certificates or physical realizability.

If A>0, the optimizer is clip(B/A,0,1), UNIQUE even when B=0 or B=A.
Only form and retain a stationary ratio when 0<B<A. No outside ratio is
computed or retained. If A=0: B>0 selects1, B<0 selects0, and ONLY B=0
makes the WHOLE interval optimal.

Critical candidates are the sorted distinct endpoints0,1 plus the isolated
strictly interior stationary ratio when present. This finite list is
sufficient for convex minimization; it is NOT every stationary point of a
flat polynomial. The whole optimizer interval is represented explicitly.

Point proof: gradient g*=2A a*-2B, second derivative2A>=0, correct lower/
upper/interior KKT sign, and the polynomial identity

    Q(a)-Q(a*) = A(a-a*)^2 + g*(a-a*).

For a flat interval proof, A=B=0, anchor and gradient are null; no preferred
representative is selected. Validate the identity and signs, not just flags.

Generic ranges:
Q(a) in [-4,6], minimum in [-4,0], linear coefficient -2B in [-4,4],
second derivative2A in [0,4], anchor gradient in [-4,8].
Each menu value minus minimum is in [0,6]. Best-menu minus continuous
minimum is in [0,1/8], with the sharper check 16*gap<=A.
For a boundary optimizer the menu contains it. For an interior optimizer,
nearest menu weight is within1/4 and regret=A(a-a*)^2.
These generic approximation bounds are prespecified, not AD outcomes.
Producer Brier excesses remain in [-2,2]; do not impose that narrower range
on arbitrary generic Q values.

Every retained ratio, coefficient, value, gradient and gap must have reduced
4096-bit components. Unretained products/sums may exceed the bound and
cancel exactly. No floats, tolerances, clipping of values or approximations.

## Native and work limits

Live caps in each engine:
MAX_BITS=4096, MAX_DEPTH=128, MAX_NODES=65536, MAX_BYTES=1048576,
MAX_DECISIONS=16, MAX_CRITICAL_POINTS=48, MAX_VALUE_EVALUATIONS=96,
MAX_TOTAL_WORK=320.

Exact native JSON trees; root-zero depth including leaves, expanded value
nodes excluding keys, exact ensure_ascii canonical bytes plus newline.
Preflight before whole serialization with early string/width/depth guards,
benign-DAG memoization, no cycles/explosive expansion, detached outputs and
no mutable cross-call cache. Native guards can be statically carried from
each implementation's OWN lineage; do not import another/prior executor.
This is a new API, not a replay of historical admission boundaries.

Parse ALL schemas first. By coefficient comparisons only, plan I rows with
0<B<A, P nonflat rows, C=32+I critical candidates. Reserve ALL caps before
division, polynomial evaluation, gradient/coefficient work or minimization.

Exact named work counts:
optimizer_classifications=16, coefficient_visits=16, gradient_terms=P,
stationary_divisions=I, critical_value_terms=C, menu_value_terms=48,
critical_selection_visits=C, menu_selection_visits=48, gap_terms=64.
total_work_terms=192+P+I+2C<=320.
The coefficient visit produces BOTH -2B and2A. Fresh menu evaluations are
counted even when a critical candidate has the same weight.
Counts describe these declared visits, not every scalar operation, schema
check, invariant comparison, copy/serialization or CPU cost.

Nonpublic test hooks:
_stationary(A,B) returns B/A (called only for strict interior rows);
_coefficients(A,B) returns (linear_coefficient,second_derivative);
_gradient(A,B,a) returns2Aa-2B for point optimizers;
_evaluate(A,B,a) returnsAa^2-2Ba;
_gap(left,right) returns left-right with retained gap range checked.
All hooks follow all planning. Classification and selection work must be
counted explicitly; no skipped coarse, duplicate-menu or tied entries.

## Complete generic output

    {input_sha256,levels,retained_weights,decisions,counts}

Input hash is SHA256 of canonical ensure_ascii JSON plus newline.
Each output decision, in the fixed original order, has exactly

    {assumed_index,bound_index,quadratic_coefficient,half_linear_coefficient,
     linear_coefficient,critical_candidates,
     optimizer,minimum,finite_menu,finite_menu_minimum,
     finite_menu_minimizer_indices,finite_menu_minimizer_weights,
     finite_menu_gap,proof,checks}

critical_candidates=[{retained_weight,value}], strictly increasing weights.
optimizer={"kind":"point","weight":fraction} OR
{"kind":"interval","lower":[0,1],"upper":[1,1]}.
finite_menu=[{retained_weight,value,excess_over_minimum}], all three in order.
Retain EVERY finite-menu minimizing index/weight, not a tie representative.
finite_menu_gap=finite_menu_minimum-minimum.
proof={kind:"point_kkt",anchor:weight,gradient,second_derivative} OR
{kind:"zero_polynomial",anchor:null,gradient:null,second_derivative:[0,1]}.
Minimum scalar alone is not an optimizer-set certificate.

checks has exactly these true fields after actual invariant checks:
convexity,critical_candidates_complete,optimizer_set_complete,
global_kkt_certificate,finite_menu_complete,finite_menu_argmin_complete,
finite_menu_gap_nonnegative,menu_grid_error_bound,coarse_option_available.

counts={decisions:16,critical_candidates:C,value_evaluations:C+48,
point_optimizers:P,interval_optimizers:16-P,interior_point_optimizers:I,
lower_endpoint_optimizers:<count>,upper_endpoint_optimizers:<count>,
finite_menu_minimizer_occurrences:<sum lengths>,
 plus EVERY named work count including total_work_terms above}.

## Producer evidence wire

Suite exactly {producer,alphabet,cases,independent_route_equal,public_controls,totals}.
producer={artifact:"qr-05ac-replacement-envelope-2026-09-07/results.json",
bytes:1783649,sha256:<pinned AC>}. alphabet is the unchanged AC whole-model wire.
cases exactly {case_id,problem,analysis,producer_coefficients,prior_certificates,
forecast_families,family_certificate_map,mechanism_certificates,witness_laws,
witness_certificate_map,world_certificates,producer_controls}.

producer_coefficients ordered s:
{assumed_index,clean_distance:D0,clean_cross:C0,full_replacement_upper:S1}.
prior_certificates is a detached EXACT copy of the parent's entire AC
certificate list, preserving every candidate, old AA set and failure.

Deduplicate forecast families by EXACT (s,optimizer-set), assigning family_id
on first occurrence in fixed certificate order. A family is
{family_id,assumed_index,optimizer,beliefs}. Each belief keeps ordered
{belief_id,weight,cells}. Cells cover ALL frozen nominal full-support reports,
sorted, with exactly
{value,coarse_forecast,detailed_forecast,point_forecast}.
Forecast laws use standard sorted positive {value,probability} atoms.
For a point optimizer, point_forecast is the complete exact mixture.
For an interval optimizer, it is NULL deliberately: the two endpoints
define the ENTIRE parametric family, not an absent/unsupported forecast.
family_certificate_map has16 ordered {assumed_index,bound_index,family_id} rows.

mechanism_certificates has16 ordered rows:
{assumed_index,bound_index,full_retention_profile_index:3s+2,
positive_weight_face_indices,zero_weight_face_indices,zero_bound_face_indices,
common_witness_label_indices,common_witness_valid_for_entire_segment:true}.
Positive faces come from the parent's AC full-retention profile; zero-weight
and zero-bound faces contain every label. The common witness selects the
first positive-face index in each fiber, independently of the chosen weight.

Deduplicate common witness index vectors within a case, lexicographically
order them, then assign witness_id. witness_laws use AC's complete wire
{witness_id,label_indices,beliefs}, including every original history weight
and four actual channels {level,cells}. Each cell has positive probability
and complete conditional prediction. Reconstruct actual joints with the SAME
global pointmass map across histories and levels; omit only exact zeros.
witness_certificate_map has16 ordered {assumed_index,bound_index,witness_id} rows.

world_certificates has16 ordered rows:
{assumed_index,bound_index,world_indices,polynomials,optimizer,
point_world_excesses,point_worst_world_indices,whole_interval_minimax,
upper_bound_value,common_witness_id,checks}.
world_indices contains original t<=u; polynomials align with it and have
{actual_index,quadratic_coefficient:A_t,half_linear_coefficient:B_t}.
For point optima retain complete exact world excesses and every maximizing
world. For intervals both point fields are null; whole_interval_minimax is
true (false for points). upper_bound_value is the generic minimum.
World checks exactly {point_or_parametric_laws_complete,
all_worlds_below_optimum_value,common_witness_attains_optimum}:true.

Independently expand literal actual-outcome loss on each common witness
to authenticate ALL world-polynomial coefficients, not sampled weights.
Literally rescore every unique point-forecast family at ALL four actual
levels under its assumed model's common witness. Check all mapped bound
worlds and their maximum. For interval optima prove every lower-world
polynomial<=0 on[0,1] and the upper polynomial identically zero.
Do NOT infer all lower worlds are identically zero from a generic flat
upper objective. Evaluated-support risk equality is not global law identity.

## Producer controls and interpretation

True producer_controls exactly:
frozen_AC_certificates_preserved,original_weight_clean_coefficients,
clean_segment_premises,full_replacement_envelope_preserved,
complete_quadratic_reduction,all_AC_menu_values_recovered,
finite_menu_minimax_comparator,complete_optimal_forecast_families,
interval_optima_not_point_selected,global_common_mechanism_witnesses,
complete_witness_laws_and_marginals,literal_point_forecast_scores,
literal_parametric_world_polynomials,old_failures_preserved_without_relabeling,
no_per_history_weight_selection.
False fields exactly:
origin_authenticated_by_generic_API,raw_history_reconstruction_performed_by_this_runner.

public_controls exactly {analyze_calls:12,invalid_analyze_calls_rejected:16,
raw_laws_histories_or_artifacts_given_to_core:false,
weights_selected_per_history:false,actual_world_used_to_select_weight:false,
forecasts_outside_frozen_segment_used:false,prior_certificates_replaced:false}.
totals={cases:6,analyze_calls:12,invalid_analyze_calls_rejected:16,
 plus sums of every scalar analysis counts field,
 forecast_families:<sum per-case unique>,witness_mechanisms:<sum per-case unique>}.

The finite-menu comparator is reoptimized under AC's enlarged class, not
silently substituted for AA's original nominal selection. Continuous gain
means smaller worst-case value, NOT pointwise dominance at every world,
restored original AA numerical guarantees, or empirical improvement.
Report zero gains and harmful unselected rules as well as positive gains.
Coarse weight0 makes nonpositive optimum automatic; substantive questions
include strict improvement, complete optimum sets and cost of discretization.

## Verification and publication

Seven frozen files: README.md,retention.py,reference_qr05ad.py,study.py,
test_qr05ad.py,test_capture.py,audit_json.py.
JSON-only auditor statically carries its full AC raw chain, importing no
executor, runner or test. Authenticate34 prior artifacts and seven sources
each for AD/AC/AB/AA/Z/Y/X, six for W:89 identity targets before/after.
Inherited polynomial identity is not a fresh polynomial derivation; old
runtime/API metadata and broader operator/minimality proofs are not replayed.

Hands: all linear/convex endpoint/interior cases, flat interval versus
zero-gradient unique endpoint, quarter/three-quarter menu ties and sharp
1/8 gap, critical duplicates/nonminimal equal values, signed extremes,
new retained coefficient/ratio/value/gradient/gap overflow versus cancellation,
native/DAG/depth/bytes/detachment, every work cap BEFORE solve/evaluate hooks.
Producer tests cover original-weight coefficient derivation, exact complete
point/interval forecast laws, global witness versus historywise choice,
parametric world polynomials, preserved AC failures and nonvacuous full
output/law/coefficient/family-map corruption. Normal/-O guard subprocesses
use explicit exceptions, not assertions.

First fixed complete comparison only after protocol/engines/runner exist,
with four source identities and all34 priors before/after.
Then create-only external preflight/full raw audit, freeze seven sources,
full isolated normal/-O tests with fresh external bytecode caches, exclusive
results.json capture, fresh exact read-only replays and final raw audit.
Capture/suite caps remain64MiB/128MiB; no large jobs/dependency changes.
RESULTS.md and roadmap stay outside the frozen source ledger. Publish only
AD research files/roadmap; preserve unrelated RET/core/governance work.

No AD coefficient, optimizer weight or outcome has been calculated at this
protocol's creation. No calibration/deployment/RET integration, Lean proof,
new quantum experiment, physical law, ontology, metric or gravity claim.
