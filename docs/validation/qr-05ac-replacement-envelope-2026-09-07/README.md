# QR-05AC protocol: whole-fiber replacement envelope

7 September 2026. Prospective specification before AC fixed-case outcomes.
Base: pushed AB commit 578543f6480eede54c23d0a74bfe54cca50c8d3e.

## Frozen question and evidence

Freeze AA's six experiments, 482 histories, H2/K3/Q3, original history
likelihoods, target, four levels [0,1/2,3/4,1], weights [0,1/2,1], complete
nominal AA minimizing sets and all Z forecast maps h_a=(1-a)g+a f_s.
No refit, stressed argmin, retrospective tie choice or per-history adversary.
Pin AB results.json: 1,805,554 bytes, SHA256
7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009.
AB plus its 32 prior artifacts gives 33 immutable producer artifacts.
AA, Z and their raw chain remain pinned through AB's ledger.

Use the same distinct whole-model NMT alphabet: 93 labels in 72 current-N
fibers, including clean-zero labels, not class multiplicities or a
history-specific support. N has five nonnegative integer components;
NMT has seven, starting with N. Both fibers and their labels are strictly
lexicographically sorted and distinct.

## Declared replacement class and exact reduction

The uncertainty class is the PRODUCT of CLOSED probability simplices:
one arbitrary distribution mu_N on each existing whole-model N alphabet.
The same mu_N applies across all histories, reports and actual noise levels.
It can depend on N, but NOT on history, future outcome or the clean label
within N. This is a restricted state-independent replacement channel, not
every possible observation-error channel. The class contains nominal
uniform and both AB tilts. It does not constitute sensor calibration.

For clean report/future joint J_H,0(b,q), define the UNNORMALIZED subjoint

    J_H,N(q) = sum_{b with prefix N} J_H,0(b,q).

The actual law is

    J_H,t,mu(z,q) = (1-t) J_H,0(z,q) + t mu_N(z) J_H,N(q).

At full replacement the actual future law at every POSITIVE report is g_H,N.
Using original history weights w_H, define for each fixed assumed model s
and candidate retained weight a:

    B_s,a,N(z) = sum_H w_H sum_q J_H,N(q)
                  [loss(q,h_H,s,a(z)) - loss(q,g_H,N)].

Equivalently B=sum_H w_H P_H(N)||h_H,s,a(z)-g_H,N||^2 >=0.
Aggregate histories BEFORE any label maximization. A history with zero
P_H(N) contributes zero; do not remove its alphabet labels.

Let c_s,a be the nominal clean case-average excess, and S_s,a=sum_N max_z B.
Then for one fixed mechanism,

    E(t,mu)=(1-t)c+t sum_N sum_z mu_N(z) B_N(z),

and the exact per-world envelope is U_t=(1-t)c+t S.
Maximize U_t over the SAME existing finite levels t<=u to obtain M(s,u,a).
The generic API must enumerate every maximizing world: it permits c>0,
so clean can dominate. Producer controls establish c<=0 and S>=0, hence
its upper endpoint is a worst world. Do not assume that property generically.

If zero is a worst envelope world, EVERY mechanism attains M via t=0.
Otherwise the complete maximizing-mechanism face is the product of the
per-fiber maximizing-label faces. Retain each face's complete label indices.
For a particular positive world the maximizing face is the profile's
per-fiber argmax; at zero it is the entire alphabet. Together with the
complete maximizing-world list this specifies every maximizing (world,law)
pair, not just one selected witness.

Choose a deterministic lexicographically first point mass from the GLOBAL
maximizing face in each fiber. This is a mechanism witness, not a new
forecasting rule. Recompute its full coefficient sum, all applicable world
excesses and its OWN complete worst-world list. When clean dominates, this
witness can have fewer worst worlds than the envelope; do not copy the list.

The maximum over the closed simplex equals the supremum over strictly
positive laws. A full-support maximum is attained iff zero is a worst world
OR every fiber's coefficients are constant over its complete alphabet.
Report both a uniform negative margin (M<0) and the different statement

    every_full_support_mechanism_strict =
       M<0 OR (M==0 AND full-support maximum is not attained).

Positive M implies a harmful full-support law by sufficiently small uniform
smoothing, and M>V0 similarly implies an old-bound-breaking full-support law.
A boundary witness alone need not have full support. At u=0 all labels
maximize; unused fibers and the coarse candidate likewise retain all labels.
Do not carry AB's full-support law-coincidence equivalence over to an
arbitrary boundary law with missing support.

For the fixed Z family B_s,a=a^2 B_s,1. Verify common maximal faces/witness
structure across positive weights for each assumed model, not across s.
These are anticipated controls, not required survival outcomes.

## Generic exact API and resource contract

Both stdlib engines export analyze(problem). Exact native JSON only:

    {schema_version:"det8-qr05ac-problem-v1",
     family:"qr05ac_replacement_envelope",
     nominal:<unchanged AA input problem>,
     alphabet:[{N:[five ints],values:[[seven ints],...]}],
     models:[{assumed_index:0..3,
              full_coefficients:[[[fraction_for_a0,
                                     fraction_for_ahalf,
                                     fraction_for_a1],...labels],...fibers]}]}

The nominal schema is exactly AA's four levels, three weights, four ordered
actual-world rows with coarse_risk and four ordered assumed-model rows
containing three forecast_risks. Risks are reduced fraction pairs in [0,2];
the first rule equals same-world coarse. The output baseline is the entire
independently recomputed nominal AA analysis, unchanged.

Generic alphabet: 1..72 fibers, 1..93 total labels, each fiber nonempty.
Indices/coordinates must be native nonnegative ints, never bool/subclasses.
All fraction pairs are native reduced integers, positive denominator,
4096-bit components. Full coefficients lie in [0,2]; all coarse coefficients
are exactly zero. Require each profile's final S<=2. Clean excess is derived
from nominal actual zero after all preflight, not independently supplied.
The generic API does NOT enforce nominal affinity, uniform-coefficient
consistency, a-squared scaling, producer origins or c<=0. These belong to
the producer/auditor. Generic nomination tables can be nonaffine.

Live limits in each implementation:
MAX_BITS=4096, MAX_DEPTH=128, MAX_NODES=262144, MAX_BYTES=4194304,
MAX_RISK_CELLS=48, MAX_DECISION_WORK=216,
MAX_FIBERS=72, MAX_LABELS=93, MAX_COEFFICIENT_CELLS=1116,
MAX_TOTAL_WORK=10548.

Native budgets apply to the OUTER AC input and detached full output.
Depth is root-zero, including leaves. Nodes count expanded value occurrences,
not keys; bytes are exact canonical ensure_ascii JSON plus newline.
Preflight before whole serialization; early width/depth/string checks,
benign-DAG memoization, cycles and exponential expansion rejected.
No cross-call mutable cache. Do not claim replaying historical AA public
byte/node admission boundaries inside the new wrapper.

Parse ALL nominal/coefficient/alphabet schemas and plan ALL work limits
before nominal subtraction, profile maxima/sums, envelopes or witness work.
Each engine statically carries its own AA nominal implementation; no
cross-engine/prior-executor imports. Retained excesses and S are in [-2,2]
or [0,2] as appropriate; new signed differences are in [-4,4].
Retained rational components must fit 4096 bits. Unretained exact intermediates
may exceed this bound and cancel; no clipping, tolerance or float conversion.

For F fibers and L total labels, planned work counts exactly:

    baseline_decision_work = 216
    profile_coefficient_visits = 12 L
    profile_fiber_terms = 12 F
    world_envelope_terms = 48
    candidate_world_visits = 120
    face_label_visits = 48 L
    witness_coefficient_terms = 48 F
    witness_world_terms = 120
    shift_terms = 96
    candidate_classifications = 48
    total_work_terms = 648 + 60 L + 60 F <=10548.

Visit every declared coefficient/face label, including coarse and unselected
rules; no short-circuit counts. All face-label visits are counted regardless
of how many are selected. Metrics exclude parsing, copy/serialization,
invariant checks and comparisons internal to an independent audit.
Expose _analyze_nominal, _profile_coefficient, _envelope, _witness_term and
_shift as nonpublic test hooks. _profile_coefficient takes a Fraction and
returns it; _witness_term likewise. _envelope(c,S,t) returns (1-t)c+t*S.
_shift(left,right) returns left-right with retained signed bounds checked.
A hook call's implementation may check its result; no work before planning.

## Complete output wire

    {input_sha256,baseline,alphabet,profiles,certificates,counts}

Hashes are SHA256 of canonical ensure_ascii JSON plus newline.
alphabet is a detached exact copy. profiles ordered s outer, a inner:

    {assumed_index,retained_weight,clean_excess,full_upper_excess,
     fibers:[{N,maximum,maximizer_indices}],all_fibers_flat}

The maximum index lists are complete, increasing, and refer to output
alphabet. all_fibers_flat iff all labels in every fiber maximize.
Each profile stores all coefficient maxima and its final sum, not an
unauthenticated fitted risk.

Sixteen certificates ordered assumed outer, bound inner:

    {assumed_index,bound_index,world_indices,
     nominal_minimax_excess,old_minimizer_indices,old_minimizer_weights,
     candidates,
     safe_old_indices,strictly_beneficial_old_indices,
     bound_preserving_old_indices,interior_strict_old_indices,
     unsafe_old_indices,bound_breaking_old_indices,
     all_old_safe,any_old_safe,all_old_strict,any_old_strict,
     all_old_bound_preserved,any_old_bound_preserved,
     all_old_interior_strict,any_old_interior_strict,checks}

All three candidates retained in order:

    {retained_weight,profile_index,world_upper_excesses,worst_excess,
     worst_world_indices,nominal_worst_excess,worst_shift,bound_excess,
     nominal_minimizer,coarse_safe,strict_benefit,original_bound_preserved,
     full_support_maximum_attained,every_full_support_mechanism_strict,
     maximizing_face_indices,witness_label_indices,witness_full_excess,
     witness_world_excesses,witness_worst_world_indices,
     potentially_unsafe_world_indices,potentially_bound_breaking_world_indices,
     witness_unsafe_world_indices,witness_bound_breaking_world_indices}

maximizing_face_indices contains one complete index list per alphabet fiber;
witness_label_indices selects its first index. world_upper_excesses and
witness_world_excesses align with world_indices. Potentially unsafe/breaking
lists use U_t>0/U_t>V0; witness lists use its ACTUAL E_t>0/E_t>V0.
The witness attains the same worst value but need not share all witnesses.
worst_shift=M-M0(candidate); bound_excess=M-V0(nominal optimum).
coarse_safe=M<=0; strict_benefit=M<0; original_bound_preserved=M<=V0.
Old-subset lists preserve every original tie, with separate all/any flags.
No new minimizing weight, data-dependent bound or mechanism-fitted forecast.

checks has exactly these true fields after actual invariant checks:
nominal_selection_preserved,complete_envelope_argmax,
complete_mechanism_faces,global_witness_attains_envelope,
witness_argmax_complete,full_support_attainment,
all_any_quantifiers,signed_bound_comparison,coarse_zero,nested_worlds.
Survival classifications may be false; they are NOT acceptance controls.

counts={fibers:F,labels:L,assumed_models:4,rules:3,certificates:16,
candidate_certificates:48,old_rule_evaluations:<sum old-set lengths>,
nominal_risk_cells:48,coefficient_cells:12L,
 plus every named work count in the preceding work table}.

## Producer suite and independent checks

Suite exactly:
{producer,alphabet,cases,independent_route_equal,public_controls,totals}.
producer={artifact:"qr-05ab-replacement-stress-2026-09-07/results.json",
bytes:1805554,sha256:<pinned AB>}.
alphabet is the whole-model 72-fiber/93-label wire, identical across cases.
cases exactly {case_id,problem,analysis,witness_laws,
witness_certificate_map,producer_controls}.

For every candidate certificate construct the actual global pointmass
mechanism from witness_label_indices, including all whole-model fibers.
Deduplicate identical index vectors WITHIN a case, lexicographically order
them and assign consecutive witness_id. witness_certificate_map is ordered
s,u,a and has {assumed_index,bound_index,rule_index,witness_id}.
witness_laws entries have {witness_id,label_indices,beliefs}; beliefs preserve
ordered original belief_id,weight, and four channels {level,cells}.
Cells retain positive report probability and complete positive conditional
prediction atoms in standard {value,probability,prediction} wire.
Omit only exactly zero cells/atoms. Witness laws can lose nominal support.
Retain all four actual channels, even if one certificate has a smaller bound.

Runner coefficient route: original-weight squared forecast distances with
unnormalized N masses. Independent auditor/test route: literal outcome loss
difference against coarse, aggregated from source N/future subjoint atoms.
Check complete baseline, both AB risk tensors, and all nominal AA world
risks reconstructed from uniform coefficients. Compare the entire AC wire.
Rebuild each unique witness's actual law and literally rescore ALL frozen
candidates; check the appropriate certificate/world scores and maxima.
Do not normalize N mass, maximize individual histories, refit forecasts,
change history weights or reject adverse finite outcomes.

producer_controls has exactly these true fields:
nominal_AA_baseline_preserved,whole_model_alphabet_preserved,
original_weight_coefficients,nonnegative_full_replacement_coefficients,
uniform_family_recovered,both_AB_tilt_risks_recovered,
frozen_forecasts_and_weights,clean_and_N_future_marginals_preserved,
complete_boundary_witness_laws,literal_global_witness_scores,
coefficient_weight_square_scaling,upper_endpoint_is_worst,
nominal_and_AB_enclosed,all_original_ties_classified_without_reoptimization.
Two false fields:
origin_authenticated_by_generic_API,raw_history_reconstruction_performed_by_this_runner.

public_controls exactly {analyze_calls:12,invalid_analyze_calls_rejected:16,
raw_laws_histories_or_artifacts_given_to_core:false,
forecasts_refitted:false,stressed_rules_reoptimized:false,
old_ties_selected_retrospectively:false,
historywise_adversary_used:false}.
totals={cases:6,analyze_calls:12,invalid_analyze_calls_rejected:16,
 plus sums of every scalar analysis counts field,
 witness_mechanisms:<sum unique per-case witnesses>}.
Counts are inventory/work, never pooled risks.

## Verification, publication and limits

Seven frozen files: README.md,envelope.py,reference_qr05ac.py,study.py,
test_qr05ac.py,test_capture.py,audit_json.py.
JSON-only audit statically carries raw AB lineage, importing no executor,
runner or tests. Authenticate 33 prior artifacts and seven sources each for
AC/AB/AA/Z/Y/X, six for W: 81 source/prior targets before/after.
Inherited polynomial digest is identity, not a new polynomial derivation;
prior APIs/performance and broader operator/minimality proofs are not replayed.

Hand tests include aggregation-before-max versus a stronger per-history
adversary; zero bound and zero-weight fibers; multiple maximizers; different
envelope/witness worst-world sets; generic positive clean; zero unattained
supremum with all full-support laws strictly beneficial; attained zero;
harmful and merely bound-breaking old rules; all/any ties; coefficient and
retained sum/witness/shift overflow versus cancellation; every live cap,
pre-work rejection, native ownership, full output/law corruption nonvacuity.
Use explicit exceptions, not assertions, in normal/-O guard subprocesses.

First fixed complete comparison only after protocol/engines/runner are
recorded, with four source identities and all 33 priors before/after.
Then create-only external preflight/full raw audit; freeze all seven files;
full isolated normal/-O tests with fresh external bytecode caches;
exclusive results.json capture, fresh exact read-only replays and final audit.
RESULTS.md and roadmap are outside the frozen source ledger. Publish only
AC research files/roadmap; preserve unrelated RET/core/governance work.

No AC fixed-case coefficient, maximizing law or envelope has been computed
at protocol creation. No sensor calibration, deployment, RET adapter, Lean
proof, quantum experiment, physical law, ontology, metric or gravity claim.

