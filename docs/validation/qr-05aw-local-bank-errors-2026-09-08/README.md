# QR-05AW protocol: local bank error coordinates

8 September 2026. Prospective before assembled fixed AW inputs or mathematics.
Base: pushed AV commit c8be4ee4b571953a9e79a9c2ab2695085b3a3b59.
Prior schema/bounds inventories may be inspected before freeze; no fixed AW
geometry checking, synthesis, scale, error-map, gain or witness calculation.
Do not edit prior research, RET/core work, dependencies or temporary sheets.

## Question and scope

Keep the underlying AU response operators carried by AV, B,G,D, with DB=G.
Define a NEW unit box in geometry-local repair-bank moment coordinates.
This is NOT AV's same raw-coordinate noise set, an optimized decoder, a new
measurement, empirical calibration or a proof of better equal-noise precision.
Geometry supplies reference units, not measured uncertainty magnitudes.
The chosen reference field amplitude is V²; this convention is not derived
as an apparatus law. No source or target polynomial integration is performed.

Authenticate actual AR repair-tile order and monomial bank labels against its
geometric response matrix and the maps inherited by AV. Never substitute AP
coarse tiles, original fine tiles, or a sorted/reordered bank detached from
its matrix columns. Recheck selected rectangle geometry/volumes only; no AR
overlay generation, moments, source dictionary, rank or decoder-fit replay.
Positive clipped cells/tiles are supplied already inside the probe.
A local moment-error box need not be realizable by a pointwise field error.

## Generic input, APIs and admission

Problem EXACT:
{family,probe,cells,tiles,bank_labels,target_labels,interface,geometric,decoder}.
family nonempty native str. probe positive rectangle [u0,u1,v0,v1].
cells c=1..8 entries {event,bounds}, sorted unique signed native int IDs.
bounds positive rectangle or null. Positive cells have disjoint interiors and
cover probe. tiles t=1..256 positive entries {event,bounds}, each inside its
named positive cell. Tiles have disjoint interiors and cover every positive
cell. Preserve their GIVEN order: arbitrary order is legal if all bank columns
are associated consistently. No zero-volume bank tile.
r=4*t; bank_labels EXACT [{tile:i,basis:j} for i in range(t),j in range(4)]
with native integer indices, basis order (1,u,v,uv).
target_labels q=1..64 sorted unique {first,second}, both valid cell IDs.
They may be a subset of cell pairs; all-undefined target queries are admitted.
interface B s*r, s=0..320; geometric G q*r; decoder D q*s.
For a target with either null cell, require its complete raw G row zero.
D's corresponding row need not vanish if it cancels on B. All DB=G rows checked.

Public functions:
build_family(problem);
synthesize(blocks,values): t four-by-four raw blocks applied to length4*t
values, t=0..256 (empty standalone call permitted); no geometry access;
produce(matrix,values): h*w times w, h=0..1024,w=0..1024;
apply(matrix,observed): v*s times s,v=0..64,s=0..320.
All three are raw linear evaluators, no intercept, files, sources or hidden
calibration. synthesize also evaluates supplied inverse blocks.

Exact native dict/list and keys; reduced [n,d],d>0 with native int components
<=4096 bits. Reject bool/float/subclasses, malformed labels/shapes, raggedness,
unknown owners, extra fields, caps, nonpositive/inconsistent rectangles.
ALL container/dimension/label/rectangle/pair SHAPES precede Fraction arithmetic;
all scalar values admitted before geometry/products. Explicit ValueError in
normal/-O. Active cycles rejected, shared children admitted, input unchanged,
detached native output. Unretained intermediates may cancel; retained inverse,
map and witness components obey the bit limit. No exhaustive graph/work/memory
or production hardening claim. Generic matrix semantics are conditional:
partition/label checks do not independently rederive arbitrary supplied G.

## Local synthesis and reference scales

dmu=du*dv/2; V is probe volume, h_t tile volume, h_C cell volume (0 for null).
For each ACTUAL bank tile:
a=u0, b=v0, du=u1-u0>0,dv=v1-v0>0;
local coordinates xi=(u-a)/du,eta=(v-b)/dv.
Local moments are integral_t F*(1,xi,eta,xi*eta)/(V²*h_t).
Let w_t=V²*h_t. Raw moments equal W_t times local moments, with

W_t = w_t *
[[1,0,0,0],
 [a,du,0,0],
 [b,0,dv,0],
 [a*b,du*b,a*dv,du*dv]].

Derive and retain each W_t and inverse Z_t. Check W_t*Z_t=Z_t*W_t=I4
blockwise; do not rely only on a determinant or one-sided inverse.
W and Z denote their block-diagonal actions; no dense r*r storage is required.
For target(C,D), sigma_i=V²*h_C*h_D, including literal0.
Positive sigma defines normalized errors; zero sigma is UNDEFINED, even when
the raw response is zero. No replacement by1 or normalized fabricated0.

First verify K=D*B=G on the full bank, R_bank=K-G=0.
Then H=B*W, J=G*W, L=D*H, R_error=L-J=0.
Retain K,R_bank,H,J,L,R_error as complete raw matrices.
For defined target i: A_i=J_i/sigma_i, beta_l=sum_j|H_lj|,
E_il=D_il*beta_l/sigma_i, alpha_i=sum|A_i|, gamma_i=sum|E_i|,
gap_i=gamma_i-alpha_i>=0.
For undefined i: A_i,E_i,alpha_i,gamma_i,gap_i are null, NOT zero rows.
beta remains complete on every receiver coordinate.
All strictly positive-scale zero-response rows are DEFINED with zero shared
gain; their enclosure gain may be positive when decoder contributions cancel
on the common bank but not throughout the larger receiver box.
When no target is defined, three maxima are null and maximum-row lists empty.

## Sharp error domains and actual endpoints

Primitive local error x satisfies |x_j|<=1; raw bank error e=W*x.
Shared response error is G*e=D*B*e; normalized row i lies in[-alpha_i,alpha_i].
Receiver-coordinate enclosure |y_l|<=beta_l has sharp row bound gamma_i.
No stochastic independence assertion, ratio, optimizer or feasibility solver.
epsilon>=0 scales this fixed error contract; retained endpoints use epsilon1.

For each defined target i, signs=sign(A_i), sign0=0; retain BOTH x=+signs
and -signs as rational vectors. Each endpoint MUST actually evaluate:
bank_error=synthesize(W_blocks,x),
roundtrip_primitive=synthesize(Z_blocks,bank_error),
observed_error=produce(B,bank_error),
direct_error=produce(G,bank_error),
decoded_error=apply(D,observed_error).
Require roundtrip_primitive=x, direct=decoded, observed=H*x,
normalized_error_h=decoded_h/sigma_h=A_h*x for every defined h,
and normalized_error_h=null for every undefined h.
Check all defined normalized errors within alpha, observed within beta, x
in unit box, and attained=normalized_error_i=+/-alpha_i.
Full raw q-vectors include undefined target coordinates, which remain checked.

Enclosure signs=sign(E_i) (zero-beta coordinates choose0); endpoints
observed_error=+/-beta*signs, decoded_error=actual apply(D,observed_error).
Retain full raw decoded vector, normalized components null precisely at
undefined targets, all defined bounds within gamma, attained=+/-gamma_i.
Undefined raw decoded components may be nonzero: arbitrary enclosing receiver
inputs need not be shared-bank errors. Never overwrite them with zero.
No fabricated primitive/bank preimage. A tied bound does not imply reachability.

Undefined designated target rows have null witnesses in BOTH groups.
Canonical endpoints are not entire maximizing faces. Retain all tied maximizing
DEFINED target indices, original indexing; signs/witnesses can repeat.
No single witness must simultaneously attain other targets' signed extrema.

## Complete wire and counts

Family EXACT {problem,geometry,coordinates,maps,shared,enclosure,comparison,
checks,counts}. problem detached input.
geometry EXACT {volume,cell_volumes,tile_volumes,target_scales,
defined_rows,undefined_rows}, values in input order.
coordinates EXACT {bank_scales,raw_from_local,local_from_raw};
bank_scales w_t, other fields t four-by-four blocks.
maps EXACT {decoder_bank,bank_residual,interface_error,target_error,
decoded_error,error_residual,normalized_target,enclosure_target}.
First6 correspond K,R_bank,H,J,L,R_error; last2 q lists of rows or null.

shared EXACT {row_gains,witnesses,max_gain,max_rows}.
enclosure EXACT {receiver_radii,row_gains,witnesses,max_gain,max_rows,
common_bank_feasibility_tested:false}.
Each witnesses list lengthq, null if undefined; otherwise EXACT
{target_row,signs,positive,negative}.
Shared endpoint EXACT {primitive,bank_error,roundtrip_primitive,observed_error,
direct_error,decoded_error,normalized_error,attained}.
Enclosure endpoint EXACT {observed_error,decoded_error,normalized_error,attained}.
comparison EXACT {gain_gap,strict_rows,tied_rows,undefined_rows,max_gap,max_gap_rows}.
Strict/tied/undefined ascending disjoint lists partition all q.
Maxima native rational pairs or null only when no defined rows.

checks EXACT all true only after full checks:
geometry_partitions,bank_label_identity,coordinate_inverse,frozen_bank_identity,
error_map_identity,normalization_domain,primitive_box,shared_pipeline,
shared_attainment,enclosure_box,enclosure_attainment,complete_gain_partition.

counts EXACT:
cells,positive_cells,tiles,bank_values,receiver_values,target_rows,defined_rows,
undefined_rows,geometry_input_entries,input_matrix_entries,geometry_entries,
coordinate_entries,map_entries,gain_entries,shared_witnesses,shared_sign_entries,
shared_witness_entries,enclosure_witnesses,enclosure_sign_entries,
enclosure_witness_entries,shared_maximizers,enclosure_maximizers,gap_maximizers,
strict_rows,tied_rows.
Let d=number defined, a=number positive cells.
geometry_input_entries=4+4*a+4*t; input_matrix_entries=s*r+q*r+q*s.
geometry_entries=1+c+t+q; coordinate_entries=33*t.
map_entries=5*q*r+s*r+d*(r+s).
gain_entries=s+3*d+(3 if d>0 else0).
shared_witnesses=2*d;shared_sign_entries=d*r;
shared_witness_entries=2*d*(3*r+s+2*q+d+1).
enclosure_witnesses=2*d;enclosure_sign_entries=d*s;
enclosure_witness_entries=2*d*(s+q+d+1).
Other counts literal lengths. Count rational zeros/repetitions, not nulls,
labels/indices; signs separately as named. No minimal-storage/measurement claim.

## Independent methods and synthetic controls

Primary: explicit triangular synthesis/inverse and blockwise products.
Reference: bilinear corner reconstruction of global monomials on each actual
tile, independent exact block inversion, raw bank/local column probes, and
interval-endpoint bounds. Tests: independently indexed monomial/binomial
expansion and inverse formulas, scalar products, exhaustive SMALL local and
receiver cube extrema. No fixed 2^48 enumeration, shared math helpers, cross-
reading engines, older math imports or stored AW answers. Authors may reuse
their OWN validation patterns. Root owns runner; fixed tests lazy/named fixed.

Controls: unequal translated/signed-origin tiles, own-tile versus stale
probe/coarse block, wrong label/basis/order producer mutations, thin positive
rectangles, positive zero-response targets versus null targets, mixed and
all-undefined queries, raw nonzero undefined enclosure outputs, empty receiver,
cancellation/ties, signed endpoints, epsilon scaling, actual call inventories,
native shapes/values/caps (separate small workloads), cycles/aliases,
detachment, inverse/map/witness retained overflow versus canceled intermediates.
Do not claim arbitrary G's geometric meaning is generically authenticated.
Selected historical bound/label/map mutations must be non-noop.

For synthetic u'=a*u+b,v'=c*v+d,a,c>0,k=a*c, explicitly use field convention
F'=k²F. Let P be the global monomial affine-change matrix
[[1,0,0,0],[b,a,0,0],[d,0,c,0],[b*d,a*d,b*c,a*c]].
Bank transport S=blockdiag(k³*P). Then V'=kV,h'=kh,
W'=S*W,Z'=Z*S^-1,sigma'=k⁴*sigma.
For an EXPLICIT invertible receiver transport T (no derived apparatus units):
B'=T*B*S^-1,G'=k⁴*G*S^-1,D'=k⁴*D*T^-1.
Verify transformed geometry/blocks/scales and full raw endpoint transport,
normalized shared map/signs/gains, defined/null sets and maxima.
General T mixing may change the receiver enclosure; signed monomial T preserves
its gains. Frozen means the SAME operators with transported coefficients,
not numerically unchanged matrices under coordinate change. No fixed transforms.

## Selected bridge and evidence lifecycle

Inputs come ONLY from AV family problem name/target_labels/B/G/D, and AR
problem.probe/fine_cells, geometry.repair_tiles {event,bounds} in retained order,
matrices.repair_observation_rows/fine_response_rows and repair.matrix.
Require AV G and target_labels EXACTLY equal AR repair.matrix and fine labels;
derive bank labels from retained AR rows, not inferred reordering.
Fixed grid then warp,c8,t12,r48,q64,s37. No fixed outcome prespecified.
AV old W/scales/maps/gains/witnesses are NOT used or replayed. AR old volumes,
scales/moments/outgoing/source/decoder/rank computations likewise excluded.
This gate rechecks selected partitions/volumes and DB=G, not those old routines.
project_inputs takes {AV:[families],AR:[families]} and returns (problems,previous).
prior_document reads AV; geometry_document reads pinned AR; load_inputs joins them.

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {selected_families:["grid","warp"],AV_frozen_maps_equal:true,
AR_selected_geometry_equal:true,AR_bank_target_labels_equal:true,
AR_geometric_map_equal:true,local_error_domain_is_new:true,
selected_partitions_rechecked:true,frozen_bank_identity_rechecked:true,
old_raw_error_analysis_replayed:false,other_historical_mathematics_replayed:false,
older_executors_run:false}.
payload_sizes per family EXACT {family,input_bytes,geometry_bytes,coordinate_bytes,
map_bytes,shared_bytes,enclosure_bytes,comparison_bytes,native_family_bytes}.
Canonical JSON+newline projections overlap; not additive unique storage/packets.
totals sums all counts plus families=2.

scope EXACT all false:
source_dictionary_changed,source_or_target_integrals_recomputed,
repair_overlay_regenerated,decoder_refitted,filters_reselected,measurements_added,
normalization_row_added,empirical_noise_calibrated,stochastic_independence_assumed,
field_realizable_errors_required,common_bank_feasibility_solved,
same_error_domain_as_AV_claimed,equal_noise_sensor_improvement_claimed,
full_field_stability_tested,minimality_recomputed,unknown_geometry_reconstructed,
physical_sensor_validated,quantum_channel_constructed,gravity_derived,
ret_integration_tested,lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.

AV pin1265211 bytes SHA256
db498dfae4d1659f0fe35eef72efc916c6d9c8fedbd375830145e78a680c4ef5.
AR pin704842 bytes SHA256
c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8.
AR is already in AV's prior ledger; no double count. AV plus52 priors gives53
captures; AV5 sources plus79 ancestors gives84 ancestors; AW5 =>142 identities.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05aw.py after generic
passes and independent reviews, BEFORE assembled fixed AW input/geometry/math.
Historical schema/bounds inspection before this freeze is not a scale/error run.

First comparison; exactly ONE independent normal reference-only read-only audit;
full normal/-O tests; post-test bracket; external create-only comparison
preflight; exclusive final capture; fresh primary-normal/reference--O read-only
replays. Audit/full tests may run concurrently; both finish before preflight.
Bracket all142 identities and capture bytes; first/preflight/final non-runtime
fields agree. Disclose every post-first source/protocol/fixture/math correction.
Isolated Python, fresh external caches, no dependencies. Capture128MiB,
serialized working192MiB caps are not process-memory/work bounds.
RESULTS.md and roadmap outside ledger. Publish ONLY this directory and roadmap.
