# QR-05AA protocol: declared uncertainty-bound decisions

7 September 2026. Prospective specification before AA fixed-case outcomes.
Base: pushed QR-05Z commit 4b550f7499ae1d00db3f3abeddd7de344e8b0252.

## Question and unchanged evidence

Keep Z's six separate experiments, 482 positive histories, H2, K3, Q3,
four actual/assumed noise levels [0,1/2,3/4,1] and three retained-detailed
weights [0,1/2,1]. Pin Z results.json at 31,075,315 bytes, SHA256
7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc.
Z plus its 30 immutable prior artifacts gives 31 producer artifacts.
The entire Z baseline, complete laws, original X nulls and negative outcomes
remain immutable in that pinned artifact, not duplicated in the AA envelope.

For each case, assumed noise s, and declared upper bound u, compare the
three FIXED experiment-wide rules h_a=(1-a)g+a f_s. The chosen rule applies
to every history and report. Actual noise t is fixed but unknown; no
per-history adversary, report-wise selector, hidden-state access, future
outcome, observed actual-index selector or retrospective tie breaker.

Use only finite uncertainty sets S_u={existing levels t<=u}, where u is
one of the four existing levels. Supplied bounds are assumptions, not
inferred calibration. Record every decision for every bound and assumed
model; do not choose a favorable bound retrospectively.

Let R(t,s,a) be the original-history/report-weighted Brier risk from Z,
and G(t) the coarse-only risk under the SAME actual law. Define

    E(t,s,a) = R(t,s,a) - G(t),
    M(s,u,a) = max over t in S_u of E(t,s,a),
    V(s,u) = min over a in {0,1/2,1} of M(s,u,a).

Subtract coarse risk BEFORE maximization, never max(R)-max(G).
Keep signed excess and worst-case values; negative values must not be
clipped to zero. Retain every exact maximizing actual index for every
candidate, and every minimizing weight. Returning the entire minimizer set
is the certificate; this gate does not choose one tied deployment rule.

Because a=0 is coarse, E(t,s,0)=0 and V<=0. This is a consequence of including
coarse in the menu, not a new guarantee that informative retention is safe.
Nested bounds imply every M and V is nondecreasing in u. These are generic
finite-decision identities. No strict gain or nonzero chosen weight is an
acceptance requirement. Optimality is only within these three fixed rules.

## Narrow standalone exact risk-table API

Each independent stdlib core exports analyze(problem), accepting exactly

    {schema_version:"det8-qr05aa-problem-v1",
     family:"qr05aa_uncertainty_decision",
     levels:[[0,1],[1,2],[3,4],[1,1]],
     retained_weights:[[0,1],[1,2],[1,1]],
     worlds:[{actual_index,coarse_risk,models:[{assumed_index,forecast_risks}]}]}

There are exactly four worlds in actual-index order 0..3. Each has exactly
four models in assumed-index order 0..3 and exactly three forecast_risks in
weight order. Risks are reduced native [n,d], d>0, 0<=n<=2d, each component
at most 4096 bits. Every model's a=0 risk must equal that world's coarse risk.
No artifact paths, priors, history weights, selectors or extra fields.

This is a generic supplied-risk decision API, NOT a forecast-law validator.
It need not enforce affinity, monotonicity, constant coarse risk, Jensen's
bound, or realizability by the Z mixture family. Weight labels identify the
three declared choices; numerical risk tables alone do not authenticate
their construction or physical provenance. Generic countercontrols must
include varying coarse risks and non-affine/nonmonotone tables. The runner
and raw auditor separately authenticate the fixed Z projection and laws.

Reject native-type coercions: bool or subclass indices/integers, non-native
containers or keys, floats, tuple fractions, unreduced or out-of-range
fractions, reordered/missing/extra rows, duplicate IDs and implicit defaults.
All retained differences also satisfy [-2,2] and the 4096-bit component cap.
Intermediate cross-products may exceed the cap and cancel; do not reject
valid retained values merely because of an unretained intermediate.

Before whole-tree serialization, perform per-call native tree/DAG preflight:
root depth zero including scalar leaves, MAX_DEPTH=128,
MAX_NODES=65536 expanded value nodes (keys not nodes),
MAX_BYTES=1048576 canonical sorted ASCII JSON bytes including one newline.
Reject cycles/explosive sharing; benign shared containers are allowed.
Exact scalar JSON sizing is allowed inside preflight; do not expand shared
subtrees or serialize the whole unvalidated tree. No cross-call mutable cache.
Inputs and outputs are detached; output also obeys MAX_BYTES.

After schema validation but BEFORE any risk subtraction or minimax scan,
plan and enforce live caps MAX_RISK_CELLS=48 and MAX_DECISION_WORK=216.
Expose the same live constants in both cores, including MAX_BITS=4096.
Risk cells count 4*4*3=48. Decision work means exactly these bounded visits:
48 risk-minus-coarse subtractions, 120 candidate-world visits (4 assumed
models * 3 rules * sum bound sizes 1+2+3+4), and 48 candidate-selection visits
(16 decisions * 3 rules). Total 216. These are declared decision-work
metrics, not every comparison, validation, copying, hashing or CPU operation.
Check executed counts against planned counts. Tests must lower both work
caps nonvacuously and verify rejection before subtraction/decision work.

## Exact complete output wire

Return exactly
{input_sha256,levels,retained_weights,worlds,decisions,counts}.
input_sha256 is SHA256 of the validated input's compact sorted ASCII JSON
with one trailing newline. levels and retained_weights preserve input.

worlds retains all input rows and original risk values. Each model adds
exactly excess_risks, the three signed differences under that actual world.
Thus world={actual_index,coarse_risk,models}; each model has exactly
{assumed_index,forecast_risks,excess_risks}.

decisions has 16 entries, assumed-index outermost then bound-index 0..3.
Each entry is exactly
{assumed_index,bound_index,world_indices,candidates,minimax_excess,
 minimizer_indices,minimizer_weights,checks}.
world_indices=[0,...,bound_index].
candidates has exactly three entries, in declared weight order:
{retained_weight,world_excesses,worst_excess,worst_world_indices}.
world_excesses are in world_indices order; worst_world_indices includes
ALL exact maximizers in increasing actual-index order, not just an endpoint.
minimizer_indices and minimizer_weights include ALL exact minimizers in
declared order. No randomized mixture of minimizing rules is constructed.

checks has exactly six true fields after verification:
{coarse_zero,nested_uncertainty,complete_argmax,complete_argmin,
 minimax_nonpositive,bound_extension_non_decrease}.
The final check covers both each candidate M and the selected minimum V
against the previous bound; at the first bound it is vacuous.
Equality of scalar risk does not assert equality of forecast laws.

counts exactly
{worlds:4,assumed_models:4,rules:3,decisions:16,world_rule_cells:48,
 excess_terms:48,candidate_world_visits:120,candidate_selection_visits:48,
 total_decision_work:216}.
No experiment pooling or redundant global average. Input/decision hashes
and complete wires, not selected summary scalars, must agree across routes.

## Authenticated W-family controls and mathematical limits

The runner derives each case table from Z's original weighted risks and
independently rescores every complete forecast from actual laws/report
masses/history weights using literal coordinate Brier loss. It verifies
risk-minus-coarse agrees with negative Z gain and that the a=0 forecasts
are the common coarse rule. It preserves all 48 risk values per case.

For a fixed assumed model and retained weight, the W joint report/future law
is affine in actual replacement t. Hence case-weighted expected risk is
affine, even though actual conditional future laws need not be. Explicitly
check R(1/2)=(R(0)+R(1))/2 and R(3/4)=(R(0)+3R(1))/4,
and similarly G and E. Keep original history weights; do not take the risk
of an averaged forecast or average per-history worst cases.

N-preserving W replacement and true N fallback make G constant in t.
On clean-positive reports f_s=g+beta_s(z)(p_0-g), 0<=beta_s<=1, so the fixed
blends have clean excess <=0. At full actual replacement p=g and
E(1,s,a)=a^2 times the full-actual-weight mean ||f_s-g||^2 >=0.
For the fixed W family these controls plus affinity imply nondecreasing
excess in t, with the upper endpoint among every candidate's worst worlds.
Verify the whole risk table and every maximizing-world set; endpoint
membership is not necessarily uniqueness.

At the full uncertainty bound the coarse choice must minimize. A nonzero
weight can tie it only when f_s=g on every positive full-replacement
history/report cell. Check complete laws for that coincidence condition,
not merely same risk at one world. Assuming full replacement makes every
rule coincide; earlier uninformative cases remain tie controls.

These are prospective consequences of W/Z premises, not discoveries of
empirical robustness. The generic API does not enforce them. Do not extend
finite-set certificates to arbitrary noise families, unknown models,
calibrated sensors or a continuum uncertainty claim.

## Capture suite wire

The suite is exactly {producer,cases,independent_route_equal,public_controls,totals}.
producer={artifact:<Z relative result path>,bytes:31075315,sha256:<pinned Z SHA>}.
cases preserves Z's six case IDs/order and is
[{case_id,problem,analysis,producer_controls}], with the narrow problem above.
independent_route_equal=true after complete native/canonical comparisons.

Each producer_controls dictionary has exactly these true fields:
risk_table_matches_Z, literal_forecast_risks_checked,
original_history_report_weights_preserved,
fixed_rule_forecasts_actual_index_independent,
W_affine_actual_joint_and_risk, W_constant_coarse_risk,
W_clean_forecast_segment_and_excess, W_full_replacement_quadratic_penalty,
W_excess_monotonicity_and_upper_endpoint,
W_full_bound_coarse_and_coincidence_ties.
It also has origin_authenticated_by_generic_API=false and
raw_history_reconstruction_performed_by_this_runner=false.
Verify the affine actual joint law, the clean-positive forecast segment,
and full-replacement complete-law coincidence, not only their scalar risk
consequences. The independent auditor reproduces the same reporting wire;
the false raw-reconstruction field describes the runner, not the auditor.

public_controls exactly {analyze_calls:12,invalid_analyze_calls_rejected:16,
raw_laws_histories_or_artifacts_given_to_core:false,
bounds_inferred_from_data:false,actual_level_used_to_select_rule:false,
all_ties_retained:true,finite_menu_only:true}.
totals contains cases:6,analyze_calls:12,invalid_analyze_calls_rejected:16,
plus the sum of every scalar analysis counts field across cases. Summing
inventory/work counts is not pooling experiment risks or decisions.

## Verification, ownership and publication

Primary and reference decision engines are separately implemented, with no
cross-imports and no prior executor imports. The root runner has its own
decision oracle and literal forecast scorer; it authenticates Z's pinned
projection but does not repeat the raw-history reconstruction.

The separate JSON-only stdlib auditor statically carries its own Z raw
audit lineage into the AA directory. It reconstructs the full W/X/Y/Z laws
and canonical reports, then independently projects and decides AA.
No executor, runner or test import. Source contents are bytes for identity
only. Pin 31 prior artifacts; authenticate all seven sources each for Z,Y,X,
six for W, and seven new AA files before/after. The inherited polynomial
digest remains producer identity, not a fresh polynomial derivation or a
broader operator/minimality certificate. Historical API/runtime fields are
metadata, not replayed public APIs or reproduced performance measurements.

Tests cover the six complete fixed wires AFTER this protocol, generic
negative worst-case gains, all ties, interior worst worlds, varying coarse
risks and max-after-subtraction, nested bounds, exact fractions, positive
retained overflow versus intermediate cancellation, original-weight
projection and nonvacuous output/producer corruption. Include normal/-O
explicit guard subprocesses whose rejections do not rely on assertions.

Seven frozen files: README.md,decision.py,reference_qr05aa.py,study.py,
test_qr05aa.py,test_capture.py,audit_json.py.
Complete an exclusive external preflight and audit before final freeze.
Then full isolated normal/-O tests with fresh external bytecode caches,
exclusive final results.json capture, fresh exact read-only replays in both
modes, and final raw audit. Verify identities throughout and disclose fixes.
RESULTS.md and the research roadmap are outside the frozen ledger.

Publish only this gate's research files and roadmap. Preserve all existing
RET/core/governance/Track-B changes; no dependency changes or SDK imports.
No AA fixed-case outcomes have been computed at protocol creation.
No fitting, calibration data, empirical validation, RET integration, Lean
proof, ontology, physical law, metric reconstruction or gravity claim.
