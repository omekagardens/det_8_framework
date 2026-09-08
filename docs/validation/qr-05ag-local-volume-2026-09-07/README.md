# QR-05AG protocol: supplied local-volume annotations

7 September 2026. Prospective specification before fixed AG calculations.
Base: pushed AF commit 39921dff4fc9e9bbc02817659473c87bda1bb430.
Keep all unrelated RET/core/governance files, dependencies and prior evidence unchanged.

## Question and scope

What becomes estimable when retained cell representatives carry externally
supplied positive local-volume marks? The first target is a finite marked
measure, not an unknown metric. Probe markers have zero volume. Cell marks
are fixed before all queries and selection, not fitted to query answers or
allowed to depend on the retained mask.

The observer sees a single retained induced order, original opaque IDs, fixed
probe markers, a finite eligible-ID frame, the complete selection law and
ONLY the marks of retained eligible cells. Coordinates, cell boundaries,
missing marks/relations, true weights, continuum targets and source moments
stay private to generator/auditor. The selection law alone is not the full
source-dependent observation law. A valid mark is not authenticated geometry;
a valid transitive order is not authenticated observation origin.

No inferred metric/density, minimal or necessary annotation, Poisson ensemble,
continuum limit, physical calibration, RET integration, Lean installation,
quantum-channel construction or gravitational dynamics is claimed. This gate
tests linear volume functionals, not AF's higher-chain scalar-kernel terms.
No new physical law is proposed.

## Mathematics and three signed errors

Use supplied flat null coordinates u=t+x, v=t-x, ds²=du dv. The volume of a
strict timelike rectangle is Δu Δv/2. Boundary sets have zero area in this
comparison geometry. A cell's supplied mark w_i is positive; its geometric
area g_i is generator/auditor-only. For probe q=(a,b), let M_q contain eligible
representatives with a<i<b in the full transitive order. Fixed probe markers
never enter M_q, even when they lie strictly inside another probe.

Finite supplied target T_q=sum_(i in M_q) w_i.
Geometric representative quadrature G_q=sum_(i in M_q) g_i.
Continuum comparison V_q=Δu_q Δv_q/2.
The source partition also verifies V_q by summing every cell's clipped
intersection area with that rectangle. The public API cannot use these
intersection fractions to change representative membership or repair a target.

For mask selection probability p(S), pi_i=sum_(S containing i) p(S)>0.
Methods, in this order:
raw: sum observed w_i;
uniform_rate: sum observed w_i/pbar, pbar=mean eligible pi_i;
inclusion: sum observed w_i/pi_i.
The last is ordinary inverse-inclusion weighting. It has E[estimate]=T_q
under this fixed-mark induced-observation contract, even if pair inclusion
vanishes. This expectation identity is not exact recovery from one sample.

The weighted indicator identity is derived directly here; established
inverse-inclusion graph-sampling context is
[Klusowski–Wu, §2.1](https://proceedings.mlr.press/v75/klusowski18a/klusowski18a.pdf).
No graph-estimation optimality result is transferred to these volume queries.

Retain for each method/probe:
mean - V_q = (mean - T_q) + (T_q - G_q) + (G_q - V_q).
These terms are sampling bias, annotation error and quadrature/boundary error.
Keep each signed term. Do not label a known deterministic discrepancy noise,
absorb it into covariance, or change marks/representatives/probes to remove it.

For source-aware corrected covariance, independently verify
Cov(q,r)=sum_(i in M_q,j in M_r)
 w_i w_j [pi_ij/(pi_i pi_j)-1],
where pi_ii=pi_i, and zero pair inclusion contributes a negative term rather
than being divided by. Keep ordered pairs, cross-probe dependence and diagonal
terms. Check the entire matrix both by centered sample products and an
independent second-moment route. This is not a single-record variance API.
Missing pair support does not obstruct these linear mean targets.

## Generic public input and output

Both independent stdlib modules expose analyze(problem).
Input exactly:
{schema_version:"det8-qr05ag-problem-v1",family:"qr05ag_local_volume",
 frame_size:n,fixed:[IDs],eligible:[IDs],probes:[{name,source,target}],
 mask_probabilities:[[num,den],...],
 record:{kept:[IDs],past:[[local predecessor indices],...],
         marks:[{event:ID,volume:[num,den]},...]}}

n is exact int 3..12. fixed and eligible are sorted unique exact-int lists
partitioning 0..n-1, with at least two fixed and 1..8 eligible IDs.
1..8 probes have unique names AND endpoint pairs; names match
[a-z][a-z0-9_]{0,39}. Endpoints are fixed, source<target; noncausal probes
are valid and have empty membership. All fixed IDs are retained.
kept is sorted. past rows are sorted unique local indices strictly below
their row and form a transitive order; never fill missing relations.

marks is in increasing original-ID order, exactly one row for each retained
eligible ID and no others. Missing/unretained/fixed/out-of-frame mark rows
are rejected. Empty eligible retention admits marks:[], including impossible
mask rows. Fixed markers have no mark row, not a synthesized positive mark.
All mark volumes are positive. No geometry or missing-mark field is accepted.

The eligible-list order defines all 2^M mask masses, including zeros, with
exact sum1. All singleton marginals must be positive. Fraction pairs are
native reduced exact ints, positive denominator, at most4096-bit components;
probabilities lie in[0,1]. No bool/int substitution, float, tuple, subclass
or extra-key coercion. Derive the observed mask from kept; preserve zero-mass
records with possible:false, without pruning or renormalization.

Output exactly:
{input_sha256,mask,probability,possible,marginals,questions,counts,scope}.
marginals is in eligible order. questions is in probe order, each exactly:
{probe,observed_cells,estimates}.
observed_cells is ID-sorted [{event,volume,inclusion}].
estimates maps raw,uniform_rate,inclusion to reduced fraction pairs.
No target, covariance, unknown marks or geometry is returned.
scope has exactly five false flags:
missing_marks_inferred,source_moments_inferred,geometry_inferred,
mark_origin_authenticated,observation_origin_authenticated.
Outputs are detached. No artifact/file reads or mutable cross-call cache.
Every retained rational is component-bit bounded; unretained intermediate
products/inverses may exceed the bound and cancel.

## Native/resource preflight

Live constants in both modules:
MAX_BITS4096, MAX_DEPTH64, MAX_NODES131072, MAX_BYTES4194304,
MAX_EVENTS12, MAX_ELIGIBLE8, MAX_PROBES8,
MAX_INCLUSION_TERMS1024, MAX_MEMBER_CANDIDATES64,
MAX_ESTIMATOR_TERMS192, MAX_TOTAL_WORK2000.

Before whole serialization enforce exact native types, root-zero depth
including leaves, expanded value nodes excluding keys, exact ensure_ascii
canonical bytes plus newline, and bounded strings/width. Reject cycles and
exponential shared expansion; admit bounded benign DAGs. Input and output
both obey the live native caps. Bound M before exponential allocation.

Parse ALL schema, normalization, transitivity and mark alignment before hooks.
For M eligible, K retained eligible, P probes:
L=2^M; I=M*2^(M-1); C=P*K; reserve 3C estimator terms;
W=L+I+4C+3P. Check every live cap before marginals, membership or division.
Positive marginals are checked after their construction but before weighting.
These are canonical logical visits, not literal CPU operation counts.

Hooks: _marginals(masses), returning Fraction list;
_members(kept,past,source,target,eligible), returning original-ID member list;
_weight(method,pi,pbar), returning Fraction multiplier.
No hook may run before the complete parse and all reservations.
If A is total observed member occurrences, counts exactly:
events,eligible_events,kept_events,retained_cells,mask_rows,questions,
inclusion_terms:I,member_candidates:C,observed_member_terms:A,
estimator_terms:3A,reserved_estimator_terms:3C,reserved_total_work:W,
total_work:L+I+C+3A+3P.

## Frozen source family and eighteen cases

Start with six rectangular cells on a 3-by-2 grid of [0,1]².
For i=0..2,j=0..1 use bounds [i/3,(i+1)/3,j/2,(j+1)/2],
representative ((2i+1)/6,(2j+1)/4), private label c_i_j.
Four fixed zero-volume markers: bottom=(0,0), aligned=(2/3,1/2),
unaligned=(3/5,2/5), top=(1,1).
Assign IDs0..9 ONCE by sorting base points by (u+v,u,v,label).
Keep these IDs and labels under all transformations; labels are not public inputs.
Source past is strict coordinate product order; primary generator uses the
equivalent t/x timelike inequalities, auditor uses u/v products.

Five probes in order:
whole(bottom,top), lower_aligned(bottom,aligned), upper_aligned(aligned,top),
lower_unaligned(bottom,unaligned), upper_unaligned(unaligned,top).
Use the same named endpoint IDs throughout.

Source names in order: grid,warp,warp_stale,boost,dilate.
grid is unchanged. warp and warp_stale transform every ORIGINAL point and
every boundary by (u,v)->(u²,v²). Do NOT recenter transformed representatives;
they generally are not the midpoints of the transformed cells.
boost transforms (u,v)->(2u,v/2); dilate transforms (u,v)->(2u,2v).
These are active comparisons in the stated metric; no unknown metric is fitted.
True geometric cell marks always equal transformed rectangle area/2.
Supplied marks equal these true marks except warp_stale, whose supplied marks
stay at their original base-cell values. Stale marks are valid public inputs,
not malformed data. All marks are fixed before queries and selections.

Designs in order:
identity: full mask1;
iid_half: all masses1/64;
heterogeneous: independent1/3,2/3 alternating by eligible-ID position;
all_or_none: empty/full each1/2;
fixed_size2: each size2 mask1/15;
singleton: each size1 mask1/6.
Run grid with all six, warp with all six, then warp_stale,boost,dilate each
with identity and iid_half, in that order. Eighteen cases, 64 rows each;
retain all1,152 rows including structural zeros. No case/probe selection by
outcomes, new designs or extra optimization after first fixed execution.

## Private suite wire and controls

Suite exactly {cases,controls,public_controls,totals,scope}.
Case exactly {case_id,source,design,population,samples,moments,joint_covariance,counts}.
case_id=source.name+"__"+design.name.
source exactly {name,coordinates,past,fixed,eligible,probes,cells,mark_kind}.
coordinates is ID-ordered [u-pair,v-pair]; past uses full original IDs.
cells is eligible-ID-ordered [{event,bounds,geometric_mark,supplied_mark}],
bounds is [u_low,u_high,v_low,v_high] in fraction pairs.
mark_kind="geometric_cell_volume", or "stale_base" for warp_stale.
design={name,mask_probabilities}.
population is probe-ordered:
{probe,members,supplied_target,geometric_target,continuum_volume,
 annotation_error,quadrature_error,overlaps}.
members is the full eligible membership list.
overlaps lists ALL six cells in eligible order as {event,volume}, using
clipped cell intersection, independently summing to continuum_volume.
samples is mask-ordered [{problem,analysis}].
moments maps each method to {mean,bias,covariance,decompositions}.
Vectors/matrices use probe order; decomposition rows exactly:
{probe,mean,finite_target,true_finite_target,continuum,
 sampling_bias,annotation_error,quadrature_error,total_error}.
joint_covariance is the full independently derived corrected matrix.
counts exactly {events,eligible_events,mask_rows,positive_rows,questions,
 source_member_terms,observed_member_terms,ordered_cell_pairs,zero_joint_pairs,
 packet_calls}. Pair counts include all ordered pairs across all probe pairs;
zero_joint_pairs counts these pairs whose joint inclusion is zero.
packet_calls counts two ordinary API calls per row.

controls exactly {warp,stale_marks,boost,dilation,boundaries,sampling}.
warp has six design-ordered rows:
{design,unmarked_packets_equal,marked_positive_laws_equal,
 base_targets,warped_targets,base_volumes,warped_volumes}.
Unmarked comparison erases record.marks from each public packet, across ALL rows;
this is an information projection, NOT a second valid public API input.
Marked positive laws compare complete {problem,probability} lists restricted
to positive rows, without erasing marks or renormalizing.
stale_marks has identity/half rows:
{design,packets_equal_base,geometric_targets_equal_warp,
 supplied_targets,geometric_targets,annotation_errors}.
boost and dilation have identity/half rows:
{design,order_equal,packet_estimate_scaling,moment_scaling,population_scaling,
 volume_factor}; factor1 for boost and4 for dilation; covariance factor squared.
Complete populations include overlap volumes and both signed error terms.
boundaries has one identity row for each of the five source names:
{source,overlaps_sum_to_volume,aligned_geometric_exact,
 unaligned_quadrature_errors}.
aligned includes whole/lower/upper aligned; report the two unaligned signed errors.
sampling has grid/warp design-ordered rows:
{case_id,inclusion_unbiased,uniform_bias,raw_bias,covariance_formula_equal}.
Compute every boolean from complete exact data, not from intended outcomes.

public_controls exactly {ordinary_packet_calls,independent_route_equal,
 invalid_calls_rejected}. Use eight invalid packets against each engine:
extra field, coordinate leak, bool ID, bad normalization, missing fixed marker,
nontransitive past, missing retained mark, mark on fixed marker.
totals contains cases and sums every case counts field.
scope has all false flags:
unknown_geometry_reconstructed,annotations_proved_necessary_or_minimal,
continuum_limit_established,poisson_ensemble_validated,
quantum_channel_constructed,gravity_derived,empirical_data_used,
ret_integration_tested,unknown_sampling_law_inferred.

## Verification and preservation

Pin AF results.json:11,744,906 bytes, SHA256
8a823b6253d4862bcea8f774f7d46278b288186a0361f38b39cdefd18974d7a3,
and its36 prior captures:37 total. AF's seven-source ledger is additionally
authenticated by the independent auditor. Prior results/claim boundaries
are preserved by identity, not represented as newly replayed prior arithmetic.
No historical engine is imported into the AG mathematics.

Freeze seven AG sources: README.md,volume.py,reference_qr05ag.py,study.py,
test_qr05ag.py,test_capture.py,audit_json.py. Each independent route may statically
carry its own native guards; no executable implementation sharing.
Auditor imports no engines/runner/tests: independently reconstruct sources,
cell intersections, every packet, all moments and controls from this protocol.
It checks new canonical envelope and all seven AG +37 prior +7 AF identity
targets. RESULTS.md and roadmap remain outside frozen source ledger.

Before fixed calculations, freeze this protocol, run independent generic hands,
and record primary/reference/runner identities. Report any required subsequent
implementation, fixture or rule correction explicitly. Freeze all seven sources
before external create-only preflight, then audit, full normal/-O tests, exclusive
final capture, fresh read-only exact replays and raw audit. Keep hashes unchanged.
Use Python -I with fresh external bytecode caches, no installs or RET imports.
Capture cap64MiB; working suite cap128MiB; retained rational components4096bits.
No overwriting/symlink-following final captures; temporary lifecycle checks only.
Canonical native exact JSON carries mathematics; runtime metadata is separate.
The next gate must follow the actual geometry evidence, not add a forecasting
prerequisite or silently promote a finite diagnostic to physical derivation.

