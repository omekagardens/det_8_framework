# QR-05AV protocol: shared-bank error propagation

8 September 2026. Prospective before fixed AV calculations.
Base: pushed AU commit dfbd1f7208bd3ba5659012c96b5839eb917f2760.
Do not edit prior research, RET/core work, dependencies or temporary sheets.

## Question and scope

Hold AU's complete source-independent decoder D, interface B and target G
fixed. For a common raw bank error e, x_measured=B(z+e) and
D*x_measured-G*z=D*B*e=G*e. Compare sharp response-error bounds with the
conservative receiver-coordinate box that discards shared dependence.

The fixed benchmark uses W=I48 and sigma=ones64 in the stored NUMERICAL
coordinates. This is an explicitly basis-dependent raw unit-box convention,
NOT dimensionless apparatus noise, error calibration, a probability distribution
or a dimensionally universal comparison. No geometry or local-coordinate
synthesis is imported. No AP normalization or noise bound is inherited.
No claim that corrupted raw moments are realizable fields; no clipping.
A Cartesian enclosure means independently variable coordinates, not an
assertion of stochastic independence.

Generic primitive errors xi satisfy |xi_j|<=1, e=W*xi. W may be rectangular,
rank-deficient, signed, zero, or have no columns. Target reference scales sigma
are strictly positive, supplied rational constants, NOT observed responses.
All bounds describe errors only. epsilon>=0 scales all prescribed witnesses
and bounds linearly; fixed retained endpoints use epsilon=1.
No fixed AV projection, error map, gain or witness before source freeze.

## Generic API and validation

Both independent engines expose build_family(problem),
produce(matrix,values) and apply(matrix,observed).
Problem EXACT:
{family,target_labels,interface,geometric,decoder,primitive_map,target_scales}.
family nonempty native str.
target_labels q sorted unique {first,second}, signed native int coordinates.
interface B s*r; geometric G q*r; decoder D q*s;
primitive_map W r*p; target_scales sigma q.
q=1..64,r=1..1024,s=0..320,p=0..256.
Infer r from first G row, p from first W row. No multiple-of-four requirement.
No sources, normalized-mixture weights, geometry, affine offset or fitted map.

produce: matrix h*w,values w, h=0..1024,w=0..1024; raw matrix product.
apply: matrix v*s,observed s,v=0..64,s=0..320; raw matrix product.
Empty rows/widths allowed. Neither has an intercept or external data access;
supplied values/maps are not authenticated physical measurements.

Every container exact native dict/list with exact keys, scalars reduced native
[n,d],d>0, native int components <=4096 bits; bool/float/subclasses rejected.
ALL container/dimension/label/pair SHAPES before Fraction arithmetic; all scalar
values before mathematical products. Reject ragged inputs, bad labels, extra
fields, caps, nonpositive scales. Explicit ValueError normally and under -O.
Reject active container cycles; admit shared children; leave input unchanged
and return detached native output. Unretained intermediates may cancel before
bit checks on retained results. No exhaustive hostile-object/graph, work,
memory or production hardening claim.

## Exact maps and sharp bounds

First require every coefficient of D*B=G. Checking only D*B*W=G*W is inadequate
when W is rank-deficient. No refit or rank/recoverability replay.
Retain:
K=D*B, R_bank=K-G,
H=B*W, J=G*W, L=D*H, R_error=L-J,
A_ij=J_ij/sigma_i,
beta_l=sum_j |H_lj|,
E_il=D_il*beta_l/sigma_i.
A is the normalized shared-error map; E maps a numerical unit cube into the
normalized independent receiver-box errors. All residuals must be zero.

alpha_i=sum_j |A_ij|; gamma_i=sum_l |E_il|.
The sharp shared interval is [-alpha_i,+alpha_i].
The sharp interval for the larger receiver-coordinate box
|eta_l|<=beta_l is [-gamma_i,+gamma_i].
Triangle inequality gives gap_i=gamma_i-alpha_i>=0. Strict gaps, ties and
all-zero cases are retained without a prespecified fixed ordering/count.
No ratio gamma/alpha, feasibility solver, decoder optimization or fitted bound.

For each target i, shared signs=sign(A_i), sign(0)=0.
Retain BOTH endpoints xi=+signs and xi=-signs as rational vectors.
Each endpoint MUST actually call:
bank_error=produce(W,xi),
observed_error=produce(B,bank_error),
direct_error=produce(G,bank_error),
decoded_error=apply(D,observed_error).
Require full direct=decoded, observed_error=H*xi,
normalized_error=decoded_error/sigma=A*xi, componentwise
|normalized_error_h|<=alpha_h and |observed_error_l|<=beta_l.
attained=normalized_error_i equals +alpha_i or -alpha_i.
All primitive values are in the unit box. Signs remain original native ints.

For each i, enclosure signs=sign(E_i), so zero-beta coordinates choose0.
Retain BOTH endpoints eta_l=+beta_l*signs_l and its negative.
Each MUST call decoded_error=apply(D,eta); normalized=decoded/sigma;
verify all normalized coordinates obey gamma and attained=+/-gamma_i.
These are explicitly enclosure-only inputs. No primitive/bank antecedent or
asserted feasibility/infeasibility is fabricated. Even a tied alpha=gamma
does NOT imply this canonical enclosure vector is in H's primitive-box image.

Every endpoint retains FULL vectors, not just its designated target.
A row witness need not simultaneously attain other rows' signed extrema.
For zero-gain rows both canonical shared endpoints are zero, although other
primitive vectors also attain zero. Canonical endpoints do not enumerate
maximizing faces. Retain every tied target index for maximum alpha,gamma,gap,
including all q target rows when the maximum is zero.

## Complete native wire and counts

Family EXACT {problem,maps,shared,enclosure,comparison,checks,counts}.
problem detached exact copy.
maps EXACT {decoder_bank,bank_residual,interface_error,target_error,
decoded_error,error_residual,normalized_target,enclosure_target}
in the K,R_bank,H,J,L,R_error,A,E order above.

shared EXACT {row_gains,witnesses,max_gain,max_rows}.
row_gains=alpha. witnesses q entries EXACT {target_row,signs,positive,negative}.
Each endpoint EXACT
{primitive,bank_error,observed_error,direct_error,decoded_error,
normalized_error,attained}.
enclosure EXACT {receiver_radii,row_gains,witnesses,max_gain,max_rows,
common_bank_feasibility_tested}.
receiver_radii=beta,row_gains=gamma,common_bank_feasibility_tested=false.
witnesses q entries EXACT {target_row,signs,positive,negative}.
Each endpoint EXACT {observed_error,decoded_error,normalized_error,attained}.
comparison EXACT {gain_gap,strict_rows,tied_rows,max_gap,max_gap_rows}.
Lists ascending original indices; strict/tied partition all q.

checks EXACT all true only after complete checks:
frozen_bank_identity,error_map_identity,normalized_error_identity,
primitive_box,shared_pipeline,shared_attainment,enclosure_box,
enclosure_attainment,complete_gain_partition.

counts EXACT:
bank_values,receiver_values,primitive_values,target_rows,input_matrix_entries,
map_entries,gain_entries,shared_witnesses,shared_sign_entries,
shared_witness_entries,enclosure_witnesses,enclosure_sign_entries,
enclosure_witness_entries,shared_maximizers,enclosure_maximizers,
gap_maximizers,strict_rows,tied_rows.
input_matrix_entries=s*r+q*r+q*s+r*p+q (includes sigma).
map_entries=2*q*r+s*p+4*q*p+q*s.
gain_entries=s+3*q+3 (beta,alpha,gamma,gap and three maxima).
shared_witnesses=2*q;shared_sign_entries=q*p.
shared_witness_entries=2*q*(p+r+s+3*q+1).
enclosure_witnesses=2*q;enclosure_sign_entries=q*s.
enclosure_witness_entries=2*q*(s+2*q+1).
Three maximizer counts are lengths of corresponding maximum-row lists.
Count retained zeros/repetitions, exclude indices/labels/signs except explicitly
named sign entries. Counts are not independent measurements/storage minima.

## Independence and synthetic controls

Primary uses dense exact products and direct absolute sums.
Reference reconstructs K,H,J,L through bank/primitive column probes and actual
restricted evaluations; gains use independent coordinate interval endpoints.
The separate test oracle uses independent indexed scalar contractions and
exhaustive small primitive/receiver unit-cube vertices (not 2^48 fixed vertices).
No shared math helpers, cross-reading other engines, historical math imports
or stored AV answers. Authors may reuse their OWN generic validation patterns.
Root owns orchestration. Fixed tests lazy and all named with fixed.

Synthetic cases: genuine cancellation alpha0<gamma, strict positive gap,
equal gain with a canonical enclosure vector outside the shared image,
opposite signed maximizing directions, all-zero maps/all maximum ties,
zero beta despite nonzero D, unequal sigma, signed/redundant/inactive primitive
columns, rectangular/rank-deficient/no-column W, empty receiver, repeated
target rows, no offset, raw widths, epsilon scaling, no clipping.
Reject a wrong D*B even if D*B*W=G*W on a deficient primitive map.
Test full endpoint products and actual produce/apply call inventories.
Native guards/early admission, tiny values, cancellation versus retained
overflow, cycles/aliases, detached outputs, all cap edges separately bounded.

For invertible bank S and receiver T, positive response multiplier v:
B'=T*B*S^-1,G'=v*G*S^-1,D'=v*D*T^-1,
W'=S*W,sigma'=v*sigma.
Then H'=T*H,J'=v*J,A'=A; shared signs, normalized errors and alpha stay equal;
raw bank/receiver/target endpoints transport accordingly.
General T mixing may change beta,gamma and their maximum sets; never demand
enclosure invariance. Signed monomial receiver rescalings preserve gamma.
Do not reset W=I after bank transport and call it the same error domain.
Primitive signed permutations preserve the unit cube, arbitrary mixing does not.
Only synthetic transports; no fixed transformed families.

## Selected bridge, suite and lifecycle

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Project ONLY AU family name/labels, interface B, problem.geometric G,
decoder.matrix D and the complete original decoder target-row indexing.
Require AU decoder.target_rows=range64; no AU rank/source/collision/control
replay or reliance on old decoder-complete booleans.
Add fixed W=I48,sigma=ones64. Grid then warp,s37,r48,q64,p48.
Require selected dimensions. Engines explicitly recheck the selected D*B=G
identity; all other AU mathematics remains identity-only.

prior_bridges EXACT {AU_selected_families:["grid","warp"],
AU_interface_inputs_equal:true,AU_target_inputs_equal:true,
AU_decoder_inputs_equal:true,AU_complete_target_indexing:true,
fixed_raw_unit_box:true,frozen_bank_identity_rechecked:true,
other_historical_mathematics_replayed:false,older_executors_run:false}.
payload_sizes per family EXACT {family,input_bytes,map_bytes,shared_bytes,
enclosure_bytes,comparison_bytes,native_family_bytes}.
Canonical JSON+newline projections overlap and are NOT additive unique storage
or measured-value transmission packets. totals sums all counts plus families=2.

scope EXACT all false:
source_dictionary_changed,geometry_reintegrated,decoder_refitted,
filters_reselected,measurements_added,normalization_row_added,
empirical_noise_calibrated,stochastic_independence_assumed,
field_realizable_errors_required,common_bank_feasibility_solved,
dimensionally_universal_noise_claimed,full_field_stability_tested,
minimality_recomputed,unknown_geometry_reconstructed,
physical_sensor_validated,quantum_channel_constructed,gravity_derived,
ret_integration_tested,lean_verification_performed,
generic_production_API_hardened,fixed_affine_families_run,older_executors_run.

AU pin:1073452 bytes SHA256
25e2fabfcf9e18df3ee3bf41fcac15a8b18cf3be1c4e14858be87316b48257ad.
AU plus51 prior captures gives52 captures; AU's5 sources plus74 ancestors
gives79 ancestor sources. Five AV sources give136 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05av.py after generic
tests and independent reviews BEFORE root releases any fixed AV math.

First primary/reference comparison; exactly ONE independent normal reference-
only read-only audit; full normal/-O tests; post-test bracket; external
create-only comparison preflight; exclusive final comparison capture; fresh
primary-normal and reference--O read-only final replays.
Audit/full tests may run concurrently after first; both finish before preflight.
Bracket all136 identities and capture bytes; first/preflight/final non-runtime
fields agree. Disclose all post-first source/protocol/fixture/math corrections.
Isolated Python, fresh external caches, no dependencies. Capture cap128MiB,
serialized-working cap192MiB are not process-memory/work bounds.
RESULTS.md and roadmap outside ledger. Publish ONLY this directory and roadmap.
