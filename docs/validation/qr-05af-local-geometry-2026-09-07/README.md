# QR-05AF protocol: local supplied-geometry observation interface

7 September 2026. Prospective specification before AF fixed calculations.
Base: pushed AE commit 7109ae7e0d46598424484aa8f0a74dae07d4b875.
This gate returns to geometry; no further forecast optimization is a prerequisite.
Keep unrelated RET/core/governance work, dependencies and prior evidence unchanged.

## Question and access boundary

Can an explicit record-local interface estimate marked interval/count and
low-order scalar-kernel quantities, while separating sampling error from
finite-model geometric discrepancy? Compare a bounded supplied flat geometry,
not an inferred metric. Exact sampling means are not single-record answers.

The public API sees one retained induced transitive order, opaque original IDs,
a declared finite ID frame, fixed probes, externally supplied density and a
complete mask selection law. It sees NO coordinates, source/fixture name,
missing relations, full-source chains, targets or geometry. A separate
producer/auditor enumerates all source observations and computes exact moments,
support and comparison errors. The selection law is not the observation law:
it does not disclose missing order relations. Neither schema validity nor
transitivity authenticates the record's origin as an induced order.

This is a new generic packet API, unlike E's public fixture dispatcher.
No raw-geometry recovery, metric identification, continuum limit, Poisson
sprinkling validation, empirical calibration, RET integration, Lean installation,
quantum-channel coupling or gravitational dynamics is claimed. The scalar
kernel is not a CP map, Born probability or QR-05A's qubit operation.

## Supplied mathematics and three separate errors

Use c=hbar=1, signature (+,-), u=t+x, v=t-x. The generating flat comparison
has ds²=du dv, tau²=delta_u delta_v and interval volume V=tau²/2.
All coordinate probes below are strictly timelike; no null/distributional
endpoint convention or nonlinear square-root proper-time estimator is tested.

For a marked interval (a,b), N_q counts chains with q internal vertices,
q=0,1,2. N_0 is the causal indicator, N_1 the intervening-event count,
N_2 the ordered comparable-pair count. Each chain set is counted once.
At supplied rho>0 the coefficient of z^q, z=mass², is

    k_q = alpha_q N_q,  alpha_q = (-1)^q / (2^(q+1) rho^q).

The supplied timelike continuum comparison coefficients are
[1/2, -tau²/8, tau^4/128]. These are established scalar-kernel inputs,
not laws derived from DET; see [Johnston, §§2--3](https://arxiv.org/pdf/0806.3083).
The deterministic meshes are not Poisson samples, and a three-coefficient
comparison is not finite-mass accuracy or a continuum-convergence theorem.

For every method/question with a geometric comparison, retain exactly

    mean estimate - continuum
      = (mean estimate - finite target) + (finite target - continuum).

Call the first term design-estimation bias and the second finite-model
geometric discrepancy. Keep signs; do not absorb either into covariance,
fit rho to remove it, or call it experimental noise. Volume estimates H_1/rho
and squared-time estimates 2H_1/rho are linear transforms only.

For an observed chain A, T=A intersect eligible and
pi(T)=sum_(S superset T) P(S). Fixed probe events inside another interval
are genuine internal vertices with no random inclusion factor.
Inverse joint-inclusion weighting is established sampling mathematics,
not a new physical postulate; see the induced-vertex sampling estimator in
[Klusowski--Wu, §2.1](https://proceedings.mlr.press/v75/klusowski18a/klusowski18a.pdf).

Methods, in this order:
raw:1; marginal_product:1/product_(v in T) pi({v});
uniform_rate:1/pbar^|T| with pbar the mean eligible marginal;
joint_supported:1/pi(T) if positive, otherwise omit explicitly.
Empty products equal1. All vertex marginals must be positive, but higher
joint support may vanish. Probability-zero mask rows remain in evidence.
Never normalize them, divide by zero, or infer full-target support from
one packet. Joint weighting estimates the supported source-chain count;
full-target unbiasedness needs every actual target chain supported.

Exact covariance is a full-source/design oracle quantity. Independently check

    Cov(H_q,H_r) =
      sum_(supported A,B) [pi(T_A union T_B)/(pi(T_A)pi(T_B))-1].

Keep ordered cross-question chain pairs, shared fixed vertices and cross-probe
dependence. A zero union inclusion contributes -1; it is not a divisor.
Degree2 covariance can require FOUR-vertex inclusions. Coefficient covariance
is alpha_q alpha_r times count covariance, including negative cross signs.
Also compute covariance as the exact centered outer-product sum over the SAME
original selection law. Positive semidefiniteness follows from that identity,
not positivity of individual entries or a quantum-channel interpretation.

## Public native input and output

Both independent stdlib engines expose analyze(problem). Input exactly:

    {schema_version:"det8-qr05af-problem-v1",
     family:"qr05af_local_geometry",
     frame_size:n, fixed:[IDs], eligible:[IDs],
     probes:[{name,source,target}], density:[num,den],
     mask_probabilities:[[num,den],...],
     record:{kept:[IDs],past:[[local predecessor indices],...]}}

n is an exact int2..12. fixed and eligible are sorted unique exact-int lists,
partitioning0..n-1; eligible has1..8 members. Every probe endpoint is fixed.
There are1..8 probes, unique names AND endpoint pairs; names match
[a-z][a-z0-9_]{0,39}. source<target; a pair need not be comparable.
kept is sorted, contains all fixed IDs and only frame IDs. past has one row
per kept ID in that order, each sorted unique exact-int predecessors below
its local index; require transitivity, without repairing missing relations.

The eligible-list bit order defines all2^M mask probabilities, including
zeros, with exact sum1. Density is positive. All fraction pairs are native
reduced exact integers, positive denominator, <=4096-bit components;
probabilities lie in[0,1]. No bool/int, float, tuple, subclass or extra-key
coercion. The record's mask is derived from kept. A zero-probability record
is admitted and flagged possible:false; it does not become observed evidence.

Output exactly:

    {input_sha256,mask,probability,possible,inclusion_probabilities,
     questions,counts,scope}

Question order is probe order then degree0,1,2. Each question exactly:

    {probe,degree,scale,observed_count,observed_chains,
     unsupported_observed_terms,count_estimates,coefficient_estimates}

observed_chains is lexicographically ordered:
{vertices:[original IDs],eligible_mask,inclusion}. A comparable degree0 chain
has vertices:[]; a noncausal question has no chains. count_estimates and
coefficient_estimates map the four method names to reduced fraction pairs.
The joint omission count is the number of observed chains with pi(T)=0;
other methods still score those impossible-row chains.

scope has exactly five false flags:
full_target_support_inferred, source_moments_inferred, geometry_inferred,
observation_origin_authenticated, kernel_is_quantum_channel.
There are no inferred targets, variances or geometry in the public output.
Every retained rational (including inverses after summation, scales, estimates
and probabilities) is component-bit checked. Internal products may exceed
the cap and cancel; output groups/scalars cannot evade it through net cancellation.
Outputs are detached, with no file/artifact reads or mutable cross-call caches.

## Native preflight and resource contract

Live constants in both engines:
MAX_BITS4096, MAX_DEPTH64, MAX_NODES131072, MAX_BYTES4194304,
MAX_EVENTS12, MAX_ELIGIBLE8, MAX_PROBES8,
MAX_INCLUSION_TERMS6561, MAX_CHAIN_CANDIDATES632,
MAX_ESTIMATOR_TERMS2528, MAX_TOTAL_WORK20000.

Before whole serialization: root-zero depth including leaves, expanded native
value nodes excluding keys, exact ensure_ascii canonical bytes plus newline;
bound width/strings/depth, reject cycles/exponential shared expansion, and
memoize benign DAGs. Enforce input and output byte/native caps. Detach outputs.

Parse every schema, mask-law normalization and transitivity first. Bound M
before exponential allocation. For K retained events, P probes, Q=3P:
L=2^M, I=3^M, C=P*(1+K+K*(K-1)/2),
reserve 4C estimator visits and W=L+I+5C+4Q total logical visits.
Check ALL live caps before inclusion construction, chain enumeration, weight
division or density scale arithmetic. Probability normalization is parse work.
Positive singleton marginals are checked after inclusions but before weights.

These are implementation-independent counts for the canonical subset/chain
enumeration, not CPU operations: an independent route may use a subset transform
or interval matrix identities. A is the number of observed chain terms.
counts exactly:
events,eligible_events,kept_events,mask_rows,questions,
inclusion_terms:I,chain_candidates:C,observed_chain_terms:A,
estimator_terms:4A,coefficient_evaluations:4Q,
reserved_estimator_terms:4C,reserved_total_work:W,
total_work:L+I+C+4A+4Q.
Hooks for preflight tests:
_inclusions(masses), _chains(kept,past,source,target,degree),
_weight(method,support,inclusions,pbar), _scale(rho,degree).
_weight returns None only for joint_supported zero inclusion; otherwise Fraction.
_chains returns original-ID vertex lists. No hook is called before reservations.

## Frozen twenty-case supplied family

Twenty cases, each with6 eligible IDs and64 mask rows, including zeros.
Their1280 rows are protocol metadata, not AF estimates. Source order and
coordinates are producer/auditor-only. Case order is the list below.

Base mesh3: epsilon=1/12; for i,j=1,2,3 in lexicographic order,
u=(i+epsilon*j)/(4*(1+epsilon)),
v=(j+epsilon*i)/(4*(1+epsilon)).
Add (0,0) ID0 and (1,1) ID10. Use fixed[0,3,5,7,10] and
eligible[1,2,4,6,8,9]. The seven probes in order:
whole(0,10), bottom_to_p5(0,5), p5_to_top(5,10),
bottom_to_p3(0,3), p3_to_top(3,10),
bottom_to_p7(0,7), p7_to_top(7,10).
IDs3,5,7 stay fixed under every transformation; never select new midpoints.

mesh3 rho18 (whole-diamond calibration, not independently recovered density).
mesh3_boost: (u,v)->(2u,v/2), rho18.
mesh3_dilate: (u,v)->(2u,2v), rho9/2.
mesh3_dilate_wrong_density: same dilation, rho18.
mesh3_warp: (u,v)->(u²,v²), rho18, an ACTIVE change in the same flat metric,
not a passive coordinate transformation. It preserves order/global volume,
not local volume. Deterministic meshes are not a stochastic spacetime ensemble.

Designs in order, M=6:
identity(full mask probability1);
iid_half(all masks1/64);
heterogeneous(independent1/3,2/3 alternating by eligible position);
all_or_none(empty/full each1/2);
fixed_size2(each size2 mask1/15);
singleton(each size1 mask1/6).
Run mesh3 with all six designs, then boost, dilate, wrong_density and warp
in that order, each with identity then iid_half: fourteen geometric cases.

Then ferrers6 with identity,iid_half; standard_example3 with identity,iid_half;
ferrers6 with singleton; chain6 with singleton: six additional cases.
For these add bottom0/top7 around six interiors IDs1..6, fixed[0,7],
eligible[1,2,3,4,5,6], whole(0,7), rho12.
Ferrers interiors a_i<b_j iff i<=j, S3 iff i!=j, i,j=0,1,2.
Chain6 is total order. Ferrers coordinates are D's six points
(2,6),(4,4),(6,2),(3,14),(5,12),(14,10), divided by16, with bottom/top.
S3 and chain6 coordinates/geometric comparisons are null; rho is algebraic only.
Ferrers rho is a supplied whole-volume calibration. Names never enter packets.

## Producer suite and independent audit wire

The producer constructs each complete full-source transitive order from the
supplied coordinates (or abstract recipe), then restricts it for every mask.
The public engines receive ONLY the packet above. Compare whole native output
bytes, not Python's coercive equality. Retain all sample packets and analyses.

Suite exactly:
{cases,controls,prior_bridges,public_controls,totals,scope}.
Each case exactly:
{case_id,source,design,population,samples,moments,
 joint_covariance_formula,hasse_control,counts}.
case_id = source name + "__" + design name.
source:{name,coordinates,past,fixed,eligible,probes,density,density_kind};
density_kind is "whole_volume_calibrated", "intentionally_wrong" for the
wrong-density control, or "algebraic_only" for S3/chain. Whole-volume calibration
describes the supplied full mesh, never the realized retained sample.
design:{name,mask_probabilities}.
population:{questions,interval_geometry}.
Full-source question rows:
{probe,degree,scale,chains,target_count,target_coefficient,
 supported_count,zero_inclusion_chains,full_target_supported,
 continuum_coefficient,finite_geometry_error}.
chains use the same vertex/mask/inclusion wire as observed chains.
zero_inclusion_chains contains vertex lists only. Comparisons null if no geometry.
interval_geometry is null or probe-ordered
{probe,source,target,tau_squared,volume,finite_count_volume,volume_error}.
samples:[{problem,analysis}] in increasing mask order.

moments maps each method to:
{mean_counts,bias_counts,covariance_counts,
 mean_coefficients,bias_coefficients,covariance_coefficients,
 geometry_comparisons}.
Vectors/matrices use question order. geometry_comparisons is null if no
coordinates; otherwise one row per question:
{probe,degree,continuum,mean,sampling_bias,finite_model_discrepancy,total_discrepancy}.
joint_covariance_formula is the full count matrix, ordered supported chain-pair
sum above; require exact equality to centered joint_supported covariance.
No covariance or source mean is presented as obtainable from one packet.
counts:{events,eligible_events,mask_rows,positive_rows,questions,
 source_chain_terms,observed_chain_terms,packet_calls}.
packet_calls is2 per sample, excluding the separate wrong-channel check below.

hasse_control:{mismatch_probability,first_mismatch}.
Restrict original full-source Hasse links to kept IDs and compute reachability
as a SEPARATE deliberately wrong channel. Sum original positive probabilities
where any fixed probe comparison differs from the induced record.
first_mismatch null or earliest positive-mask
{mask,kept,past,failed_probes,analysis}; past is wrong-channel local past.
Call both public engines on this valid but wrong-origin packet and compare.
Do not repair it from hidden source relations. This is not malformed input.

controls contains six named complete comparisons, not outcome assumptions:
boost,correct_dilation,wrong_density,active_warp,endpoint_collision,
singleton_observation_collision. Each is a dictionary of explicit boolean
identity/inequality checks with descriptive keys, plus exact witness data
(probe/question index, coefficients or laws) for a failed identification.
Controls must independently recompute claimed equality/inequality; true scope
checks must not substitute for numeric evidence. Detailed reporting layout
may be specified by runner/reference agreement before first fixed execution;
the above mathematical tests, source family and access cannot change silently.

Required controls:
- Boost: all count/coefficient/geometry means and covariance agree.
- Correct dilation: count laws unchanged, density quartered, all coefficient
  and continuum degreeq terms scale4^q, covariance(q,r) scales4^(q+r).
- Wrong density: public packet analyses agree with base, supplied geometric
  comparisons differ; retain whole/local signed errors without repair.
- Active warp: every public packet and analysis agrees with base for each
  matching design, but local geometric comparison values differ. Retain the
  fixed-ID local witness, not a reselected midpoint. No metric identification.
- Ferrers/S3 identity endpoint targets agree; half-sampling responses need
  not agree. Compare full joint means/covariance and preserve D's narrow
  embedding obstruction by pinned evidence, not a fresh embedding proof.
- Ferrers/chain singleton positive observation packet laws agree but full
  pair targets differ. This is distinct from a mere unsupported-chain warning.

prior_bridges authenticates D-v2 mesh3 order/coordinates and three shared probe
targets, Ferrers/S3 first three endpoint coefficients, and E's corresponding
Ferrers/S3 identity/half moments and singleton observation-law/target witness.
Preserve D-v1/v2 mathematical suite identity and packaging correction history.
Do not claim a strict fresh replay of D-v1, AE or unrelated forecasting gates.

public_controls records ordinary packet calls, wrong-channel packet calls,
complete primary/reference equality, and rejected malformed calls.
Use eight invalid packets (extra field, coordinate leak, bool ID, bad
normalization, missing fixed event, nontransitive past, unreduced density,
wrong family) against both engines; require16 explicit rejections.
totals sums case counts and records cases20, rows1280; no pooled geometric error.
suite scope has allfalse:
unknown_geometry_reconstructed, continuum_limit_established,
poisson_ensemble_validated, quantum_channel_constructed, gravity_derived,
empirical_data_used, ret_integration_tested, unknown_sampling_law_inferred.

## Verification and preservation

Pin AE results.json:6327929 bytes, SHA256
5b7946512ea77e076387a25d5cf46c30d25a42d37fdd66ae39a4edadb179bbde,
and its35 prior artifacts:36 total. AE is a sequencing/provenance checkpoint,
not an input to new geometric arithmetic. No unrelated forecasting replay is
claimed. Independently rebuild all new geometry/order/sampling arithmetic and
only the consumed D/E bridges; hash-preserve all other prior evidence.

Freeze seven sources: README.md, geometry.py, reference_qr05af.py, study.py,
test_qr05af.py, test_capture.py, audit_json.py.
Independent routes share no executable implementation; each may statically
carry its own native guard. The auditor imports no engines/runner/tests.
It independently derives coordinates, full orders, local chains, every packet,
means, centered and union-inclusion covariances and geometric discrepancies.

Before fixed calculations: freeze this protocol, complete generic hand controls
and record the primary/reference/runner source identities. Then compare every
fixed packet plus full oracle evidence. No source/outcome tuning without an
explicit retained correction disclosure. Finish and freeze all seven sources
before exclusive external preflight; audit it, run full tests normal/-O,
exclusive-create final capture, then fresh exact read-only replays and raw audit.
Identity checks cover all seven current sources and36 prior captures before/
after; the audit additionally authenticates the directly consumed D-v2/E source
ledgers by their captures. Reports/roadmap are outside the source ledger.

Use Python -I and fresh external bytecode caches; no dependency installs.
Capture cap64MiB, exact working-suite cap128MiB, retained component cap4096bits.
Reject existing/symlink result targets; create-only writes and read-only replay.
All mathematical output must be native canonical JSON; runtime is separate
metadata, not a benchmark. Temporary lifecycle tests never overwrite real evidence.
Keep all observed failures/support limits, old D/E geometric ambiguities and
quantum-record counterexamples. A diagnostic failure can close this gate without
certifying the failed interpretation. Later gate choice follows the evidence,
not automatic additional forecasting optimization.

## Pre-execution reporting-layout completion

This layout completes the reporting detail explicitly reserved above, before
any fixed AF run. It changes no fixture, question, estimator or acceptance rule.

controls.boost.pairs (identity then iid_half):
{design,public_samples_equal,population_equal,moments_equal}.
Each equality is on the complete corresponding native wire.

controls.correct_dilation.pairs:
{design,count_estimates_equal,population_scaling,coefficient_packet_scaling,
 complete_moment_congruence,squared_length_factor:[4,1]}.
Full population comparisons include support inventories, geometric volumes
and every coefficient; full moment comparisons retain both biases/covariances.

controls.wrong_density.pairs and controls.active_warp.pairs:
{design,public_samples_equal,supplied_geometry_differs,witness}.
Witness:{probe,probe_index,base_volume,transformed_volume,base_error,
transformed_error}; select first differing volume, requiring index>0 for warp.
The errors are finite count-volume minus supplied volume, not sampling bias.

controls.endpoint_collision:
{identity_cases,finite_coefficients,iid_joint_mean_equal,
 iid_joint_covariance_equal,ferrers_iid_pair_variance,S3_iid_pair_variance,
 embedding_reassessed:false}.
Compare complete joint count mean/covariance, not only the pair variance.

controls.singleton_observation_collision:
{case_ids,positive_packets_equal,full_pair_targets:{ferrers6,chain6},
 full_pair_targets_differ,observation_law_sha256}.
Hash the canonical positive-law list [{problem,probability}], in mask order;
problem includes only the public packet. Full conditional observation packets,
including their original probabilities, must agree; no fixture name is present.

prior_bridges exactly:
{D_v1_v2_mathematical_suite_equal,D_mesh3_order_coordinates_match,
 D_shared_mesh3_probe_coefficients_checked:9,
 D_ferrers_S3_endpoint_coefficients_checked:6,E_matched_moment_cases:4,
 E_matched_q0_q1_q2_vectors_and_matrices,E_singleton_observation_laws_preserved,
 E_singleton_pair_targets_preserved,E_other_controls_preserved_by_identity,
 prior_forecasting_math_replayed:false}.
The other fields are true only after the stated comparisons. E moment matching
covers all four methods and q0..q2 submatrices in the four Ferrers/S3
identity/half cases. All evidence bytes are pinned; other E controls are not
reported as new AF computations.

public_controls exactly:
{ordinary_packet_calls,wrong_channel_packet_calls,independent_route_equal,
 invalid_calls_rejected}.
ordinary_packet_calls is2 times the retained sample rows.
wrong_channel_packet_calls is2 per non-null first_mismatch.
totals contains cases and the sum of every case counts field; mask_rows=1280
(no separate duplicated rows field). No pooled geometric residual is introduced.

Hook support is the eligible bit mask; _chains source/target are original frame
IDs and kept/past use the public local-index form. Individual _weight results
and pbar are unretained internal values. All retained inclusions, scales and
summed estimates are independently component-bit bounded.
