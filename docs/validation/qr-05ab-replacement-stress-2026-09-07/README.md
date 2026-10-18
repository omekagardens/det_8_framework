# QR-05AB protocol: replacement-mechanism stress

7 September 2026. Prospective specification before AB fixed-case outcomes.
Base: pushed AA commit f486271e01de688be100ec0a7bfd256791ed0422.

## Frozen question and evidence

Keep AA's six separate experiments, 482 histories, H2/K3/Q3, actual/assumed
levels [0,1/2,3/4,1], weights [0,1/2,1], original history likelihoods, Z's
complete forecast rules h_a=(1-a)g+a f_s, and EVERY nominal AA minimizing
weight. Change only the actual replacement mechanism. No forecast refitting,
reoptimization, surviving-tie selection or actual-world-dependent rule.

Pin AA results.json: 112,206 bytes, SHA256
bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424.
AA plus its 31 immutable prior artifacts gives 32 producer artifacts.
Z's complete laws and Y/X evidence stay in the pinned Z artifact:
31,075,315 bytes, SHA256
7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc.
Do not overwrite or duplicate the entire prior chain in the new envelope.

## Two prespecified actual mechanisms

Use the SAME distinct whole-model NMT alphabet within each current-N fiber
as W: 93 distinct labels across 72 fibers, including currently zero-prior
labels. Derive it from the full model, not an individual history's support,
class multiplicities, forecast risks or observed outcomes. Order distinct
seven-component labels lexicographically within each five-component N prefix.

For m labels and zero-based rank r, define exactly

    mu_forward(z_r|N) = 2(r+1)/(m(m+1)),
    mu_reverse(z_r|N) = 2(m-r)/(m(m+1)).

Both are positive, normalized, and their pointwise average is uniform 1/m.
Singleton fibers legitimately give identical laws. These canonical-label
tilts are mathematical stress controls, not calibrated sensor models.
One declared mechanism applies globally across all histories. Report forward
and reverse SEPARATELY; do not optimize or maximize across mechanisms.

The non-disturbing N-preserving actual channel is

    C_{t,mu}(z|b) = (1-t)1[z=b] + t mu(z|N(b)).

For each history, J0(b,q) is the clean report/future joint, and
J_N(q)=sum_{b in A_N}J0(b,q) is UNNORMALIZED; its mass is P(N), not one.
Construct the full actual joint

    J_{t,mu}(z,q) = (1-t)J0(z,q) + t mu(z|N) J_N(q).

Retain all positive actual report masses and complete conditional future
laws. Exactly-zero cells/atoms are omitted, never positive ones. N/future
marginals and history likelihoods remain unchanged. At positive t the support
matches the nominal positive-noise support because both replacement laws
have full support; at t=0 the complete nominal clean experiment is recovered.

Use frozen Z forecast maps from nominal actual-full-replacement rows, which
cover the complete report union. Check actual-index independence and complete
law identity; do not substitute newly inferred tilted posterior forecasts.
Matching t=s does NOT imply correct specification after the mechanism changes.
Do not enforce nominal diagonal Bayes-correctness or its regret identity.

## Frozen-certificate stress mathematics

Recompute original-history/report-weighted Brier risk R_mu(t,s,a) for EVERY
one of the three frozen rules. Let G_mu(t) be coarse risk under the SAME
actual law and E_mu=R_mu-G_mu. Retain all 48 risk entries per mechanism/case.

For S_u={existing actual levels<=u}, compute

    M_mu(s,u,a) = max_{t in S_u} E_mu(t,s,a).

Subtract coarse before maximization, and average histories/reports before
the actual-world maximum. Never pool cases or choose a different actual
mechanism/noise level separately for each history/report.

Reconstruct the complete nominal AA analysis once. Preserve its minimizing
set A0(s,u), every old tied weight, nominal candidate worst values M0, and
nominal optimum V0. DO NOT compute a stressed argmin or a replacement policy.

For every candidate a, retain

    worst_shift = M_mu - M0,
    bound_excess = M_mu - V0,
    coarse_safe = (M_mu <= 0),
    strict_benefit = (M_mu < 0),
    original_bound_preserved = (M_mu <= V0).

Classify all/any of the ORIGINAL minimizing set separately. A positive
bound_excess may leave a rule strictly beneficial relative to coarse; weakening
the old negative certificate is not necessarily harm. If coarse was an old
minimizer, at least one old safe rule is automatic and is not a discovery.
Retain every unsafe old index and every original-bound-breaking old index,
plus actual-world witnesses. No sign/survival is required for acceptance.

## Generic standalone exact API

Each stdlib engine exports analyze(problem), accepting exactly

    {schema_version:"det8-qr05ab-problem-v1",
     family:"qr05ab_replacement_stress",
     nominal:<AA input problem>,
     mechanisms:[{mechanism_id:"forward",worlds:[...]},
                 {mechanism_id:"reverse",worlds:[...]}]}

The nominal problem has exactly AA's input schema, fixed labels and four
worlds. Each stressed worlds list has exactly AA's input world shape:
{actual_index,coarse_risk,models:[{assumed_index,forecast_risks}]}.
There are four actual worlds, four assumed models and three ordered risks.
No supplied minimizing set, artifact path, new mechanism, selector or metadata.

Risks are reduced native [n,d], d>0, in [0,2]; a=0 equals same-world coarse
risk. Every input/retained rational component is at most 4096 bits.
Excesses and candidate/nominal worst values are in [-2,2]; new worst_shift
and bound_excess use [-4,4]. Intermediate cross-products may exceed the bit
cap and cancel; every newly retained difference must satisfy its own cap.

The supplied-risk API does not authenticate origins, mixture laws, midpoint
relations, common coarse risk across mechanisms, affine or monotone actual
risk, or calibrated sensors. Generic countercontrols must allow varying
coarse/non-affine/nonmonotone tables and interior worst worlds. Producer
law controls below are separate. The complete nominal mathematical AA wire
is recomputed with locally carried own-lineage AA code, not supplied as a
trusted answer and not imported from another executor.

Strict native types only: no bool/subclass indices or integer components,
floats, tuples, subclasses, non-native keys, reduction/normalization repair,
implicit defaults, reordered/duplicate/missing/extra fields or rows.
Before whole-tree serialization, native tree/DAG preflight counts root depth
zero including scalar leaves, expanded value nodes (keys excluded), and
exact compact sorted ASCII JSON bytes including one newline.
Reject cycles/explosive sharing; benign sharing is allowed. Early depth,
width and string-size checks prevent avoidable expansion. No cross-call
mutable cache; outputs are detached and satisfy the output byte bound.

Live constants in BOTH cores:
MAX_BITS=4096, MAX_DEPTH=128, MAX_NODES=262144, MAX_BYTES=4194304,
MAX_RISK_CELLS=48, MAX_DECISION_WORK=216,
MAX_STRESS_RISK_CELLS=96, MAX_TOTAL_WORK=840.
AB applies its outer native budgets to the complete wrapper/output; locally
carried nominal AA schema/work checks retain 48 and 216. No claim of replaying
the former public API's independent byte/node admission boundary is made.

Validate ALL nominal/stress schemas and plan ALL work before ANY nominal AA
subtraction/minimax scan or stressed subtraction/scan. Nominal work is 216.
Stressed work is exactly 96 risk-minus-coarse subtractions, 240 candidate-world
visits over the nested sets, 192 signed shift/bound subtractions (two per
candidate certificate), and 96 candidate-classification visits. Total 840.
Iterate all three candidate slots, even when only one was originally optimal;
this lets the full work budget be reserved before nominal minimizers exist.
Executed counts must match. These are declared arithmetic/decision visits,
not all validation, copying, invariant checks or CPU instructions.
Expose _difference(risk,coarse) and _shift(left,right) so tests can prove
live-cap rejection before either retained subtraction route.

## Exact complete output wire

Return exactly {input_sha256,baseline,mechanisms,counts}.
input_sha256 hashes the entire validated AB input with compact sorted ASCII
JSON plus newline. baseline is the complete unchanged nominal AA analysis,
including its input hash, all risks, counts, decisions and complete ties.

Each output mechanism is exactly {mechanism_id,worlds,certificates}.
worlds retains its input risks and adds model.excess_risks as in AA.
certificates has 16 entries, assumed-index outermost then bound-index.

Each certificate is exactly
{assumed_index,bound_index,world_indices,nominal_minimax_excess,
 old_minimizer_indices,old_minimizer_weights,candidates,
 safe_old_indices,strictly_beneficial_old_indices,bound_preserving_old_indices,
 unsafe_old_indices,bound_breaking_old_indices,
 all_old_safe,any_old_safe,all_old_strict,any_old_strict,
 all_old_bound_preserved,any_old_bound_preserved,checks}.

Candidates are all three weights in original order, each exactly
{retained_weight,world_excesses,worst_excess,worst_world_indices,
 nominal_worst_excess,worst_shift,bound_excess,nominal_minimizer,
 coarse_safe,strict_benefit,original_bound_preserved,
 unsafe_world_indices,bound_breaking_world_indices}.
world_excesses follows world_indices=[0,...,bound_index].
Retain ALL exact maximizing worlds, all worlds with E>0, and all worlds
with E>V0 in increasing index order. Old index lists are exact ordered
subsets/complements within old_minimizer_indices, never new selections.
Every boolean uses exact rational comparisons; scalar equality is not
complete-law equality. No combined-across-mechanisms selection is returned.

checks has exactly seven true fields after verification:
{nominal_selection_preserved,complete_argmax,all_any_quantifiers,
 signed_bound_comparison,coarse_zero,nested_worlds,world_witnesses_complete}.
Survival booleans above may be false; do not replace them with check flags.

counts exactly
{mechanisms:2,worlds:8,assumed_models:8,rules:6,certificates:32,
 candidate_certificates:96,old_rule_evaluations:<actual old slots across both>,
 stress_risk_cells:96,baseline_decision_work:216,stress_excess_terms:96,
 candidate_world_visits:240,shift_terms:192,
 candidate_classification_visits:96,total_work_terms:840}.
old_rule_evaluations counts every old minimizing index once per mechanism/
certificate, not just surviving rules. Nominal AA counts remain nested.

## Producer evidence, identities and prospective controls

The suite is exactly
{producer,replacement_laws,cases,independent_route_equal,public_controls,totals}.
producer identifies the pinned AA relative artifact path/bytes/hash.
replacement_laws is [{mechanism_id,alphabet:[{N,values:[{value,probability}]}]}],
forward then reverse, sorted N prefixes and report labels. Include all 72
fibers/93 labels in each, without dropping zero-prior labels or singletons.

cases preserves the six original IDs/order:
[{case_id,problem,analysis,stress_laws,producer_controls}].
stress_laws is [{mechanism_id,beliefs:[{belief_id,weight,channels}]}],
forward then reverse; each channel={level,cells}, each positive cell is
{value,probability,prediction}, prediction sorted positive {value,probability}.
These are actual laws, not changed forecast laws. All conditional/report
laws normalize and retain original history weights. Every prior complete
law and nominal AA certificate remains in the authenticated producer chain.

The runner independently constructs joints from J0 and unnormalized J_N,
rescoring every frozen forecast by literal outcome-coordinate Brier loss.
The raw auditor independently applies the stochastic channel to authenticated
clean/raw evidence and reconstructs the complete W/X/Y/Z/AA chain once.
It compares every new law, risk, certificate, tie, count and reporting field.

Check full clean recovery; N/future marginal preservation; same positive-noise
support as nominal; coarse risk unchanged; complete frozen forecast identity.
At each fixed rule, joint laws and risk are affine in actual t. Forward/
reverse JOINT laws and original-weight risks average to nominal; unweighted
conditional posterior averages need not. Clean excess is nonpositive and
full replacement has true p=g and the TILTED report-weighted a^2||f_s-g||^2
penalty. Positive support preserves full-bound law-coincidence controls.
Both stressed excess vectors are nondecreasing, so u is a worst-world member.

Consequently, for THIS family and upper-set construction,
(M_forward+M_reverse)/2=M0, and each original minimizer's two signed
bound_excess values cancel. Both opposite tilts preserve an original bound
only if both meet it exactly. Verify these prespecified consequences without
requiring any particular survival/failure outcome or choosing a favorable
tilt. They are algebraic controls, not empirical robustness discoveries.

producer_controls has exactly these true fields:
nominal_AA_baseline_preserved, whole_model_positive_rank_tilts,
complete_stressed_laws_and_support, frozen_forecasts_and_weights,
literal_original_weight_risks, clean_and_N_future_marginals_preserved,
affine_actual_joint_and_risk, opposite_tilts_average_to_nominal,
full_replacement_tilted_quadratic_penalty,
upper_endpoint_and_opposite_bound_deviations,
all_original_ties_classified_without_reoptimization.
It also has origin_authenticated_by_generic_API=false and
raw_history_reconstruction_performed_by_this_runner=false.

public_controls exactly {analyze_calls:12,invalid_analyze_calls_rejected:16,
raw_laws_histories_or_artifacts_given_to_core:false,
forecasts_refitted:false,stressed_rules_reoptimized:false,
old_ties_selected_retrospectively:false,mechanisms_combined:false}.
totals={cases:6,analyze_calls:12,invalid_analyze_calls_rejected:16,
 plus the sum of every scalar analysis counts field across cases}.
Inventory/work totals are not pooled risks or decisions.

## Verification and publication

Primary/reference are separately implemented; no cross/prior executor
imports. Each statically carries its own nominal AA lineage. The independent
runner's nominal and stressed scoring/decision oracles remain separate from
the cores. The JSON-only auditor statically carries its raw AA lineage and
imports no executor, runner or test. Source content is bytes for identity.
Authenticate 32 prior artifacts and seven sources each for AB/AA/Z/Y/X,
six for W: 73 source/prior targets before/after.

The inherited polynomial digest stays producer identity, not a fresh
polynomial derivation or broader operator/minimality certificate. Historical
API/runtime fields are metadata, not replayed public APIs or reproduced
performance. No large jobs, SDK imports or dependency changes.

Tests: all six complete wires and complete law projections; harmful old
choice despite a safe unchosen rule; beneficial but original-bound-breaking
rules; all/any tie distinctions; changing which tied rule survives by
mechanism without combining quantifiers; interior worst/witness sets;
signed shifts reaching 4; exact new retained overflow versus cancellation;
native/DAG/depth/bytes, all live caps before nominal/stress work, output
ownership and nonvacuous complete-output/producer corruptions.
Normal/-O guard subprocesses must use explicit checks, not assertions.

Seven frozen files:
README.md,stress.py,reference_qr05ab.py,study.py,test_qr05ab.py,
test_capture.py,audit_json.py.
Run create-only external preflight/full audit before final freeze, then
full isolated normal/-O tests with fresh external bytecode caches, exclusive
results.json capture, fresh exact read-only replays and final raw audit.
Verify identities and disclose corrections. RESULTS.md and roadmap remain
outside the frozen ledger. Publish only AB research files/roadmap; preserve
all other RET/core/governance/Track-B work.

No AB fixed-case outcome has been computed at protocol creation.
No fitting, calibrated sensor, deployment, empirical validation, RET adapter,
Lean proof, ontology, new physical law, metric reconstruction or gravity claim.
