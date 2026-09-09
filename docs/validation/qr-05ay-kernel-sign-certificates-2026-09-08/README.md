# QR-05AY protocol: kernel sign certificates and bounded-field envelopes

8 September 2026 (Honolulu). Prospective before fixed AY projection or mathematics.
Base: pushed AX commit ba75d99766fed10b7b826119fbf579cad6125c86.
Prior published schemas/results may be inspected to specify the bridge.
Freeze all five sources before assembling fixed inputs or evaluating any fixed
kernel corners, integrals, maps, bounds or witnesses. Preserve older evidence.

## Question and mathematical domain

For the SAME supplied geometry, measure dmu=du*dv/2, B,G,D with DB=G,
amplitude V² and target scales sigma_(C,D)=V² h_C h_D, investigate ALL
measurable signed perturbations |deltaF|<=V² almost everywhere on the probe.
Discontinuous tile boundaries are permitted; shared edges have measure zero.
This is a broader error class than AX's bilinear fields, not new physical laws,
a new source dictionary, measurements, continuity or total-source positivity.

The raw response kernel on actual tile t is
k_it(u,v)=sum_j G_i,4t+j (1,u,v,uv)_j.
Actual raw target response is sum_t integral_tile deltaF*k_it dmu.
For defined sigma_i>0, the mathematical sharp all-bounded-field gain is
S_i=(V²/sigma_i) sum_t integral_tile |k_it| dmu.
This analytic identity follows from the pointwise triangle bound and the
admitted measurable sign(k) field. AY does NOT numerically integrate absolute
mixed bilinear kernels or construct their general sign-field moments.

Evaluate the FOUR ACTUAL kernel corner values in order00,10,01,11.
A bilinear kernel is a convex combination of these values.
Classify each tile into disjoint strings:
zero (all0), nonnegative (all>=0 but not zero), nonpositive (all<=0 but not
zero), mixed (both strictly positive and strictly negative values).
Zeros at corners/edges do not obstruct a sign-definite certificate.

For each defined row:
C_i=(V²/sigma_i) sum_t |integral k_it|, attained by tilewise constants.
A_i,4t+a=(V²/sigma_i) integral_tile k_it*phi_ta,
where phi is AX's four nonnegative corner functions.
L_i=sum_a,t |A_i,4t+a|, sharp for the bilinear subclass and a LOWER bound on S.
U_i=(V²/sigma_i) sum_t h_t max_corner |k_it|, a finite upper envelope.
Always C_i<=L_i<=S_i<=U_i. Corner-sup U need NOT be sharp even on certified rows.

If every tile is sign-definite, certify S_i=C_i=L_i and retain this exact gain.
If any tile is mixed, retain EVERY mixed tile and canonical first positive/
negative corner indices; exact gain is NULL (uncertified by this route),
not zero, infinity, a failed sensor or a failure of boundedness.
Mixed-tile constants are deficient for the true absolute integral, but this
gate does not compute that deficit or claim AX's lower bound always suffices.
Different tiles can require different signs; no global constant extremizer
is assumed. Nonnegative integrated A columns do NOT prove pointwise positivity.

## Generic input, admission and public APIs

Problem EXACT {family,probe,cells,tiles,bank_labels,target_labels,
interface,geometric,decoder}, the SAME nine AX fields.
family native nonempty str. probe positive [u0,u1,v0,v1].
cells c=1..8, sorted unique signed native-int IDs, records {event,bounds};
bounds positive rectangle or null. Positive cells partition probe.
tiles t=1..256 positive {event,bounds}, inside named positive cell, disjoint
interiors and covering every positive cell; preserve GIVEN order.
bank_labels exactly [{tile:i,basis:j} for i in range(t),j in range(4)];
global monomial order1,u,v,uv; r=4t.
target_labels q=1..64 sorted unique {first,second}, valid cell IDs.
B s*r,s=0..320; G q*r; D q*s. Null-cell targets require entire G row0;
nonzero D rows canceling on B are admitted. Check full DB=G.

Public APIs:
build_family(problem).
inspect_kernel(probe,tiles,coefficients): positive probe, t=0..256 positive
rectangle BOUNDS (not event records), disjoint inside probe but need not cover,
and native q=0..64 rows each length4t; empty tiles/rows admitted. Actual global
kernel coefficients, not normalized coefficients. Return kernels object below.
integrate(probe,tiles,corners): same geometry, arbitrary signed length4t
corner values, including partial/empty coverage; field zero elsewhere.
Return EXACT {local_coefficients,global_coefficients,local_moments,raw_moments,
minima,maxima}. First4 lengthr,last2 lengtht. ACTUAL deltaF coefficients in
local(1,xi,eta,xi eta)/global(1,u,v,uv); raw actual integrals, local moments
divided by V² h_t; actual extrema V² min/max(c_t). Same semantics as AX.
produce(matrix,values): h*w times w, h=0..1024,w=0..1024.
apply(matrix,observed): q*s times s, q=0..64,s=0..320.
Raw produce/apply are file/geometry blind and have no intercept.

Exact native dict/list/key/rational [n,d] syntax, reduced,d>0; all rational
components native ints<=4096 bits. Reject bool/float/subclasses, malformed
shapes/labels/owners/caps/geometry, unknown fields and active cycles; shared
children admitted. Complete dimensions/labels/pair SHAPES before Fraction,
all scalar values before geometry/products; explicit ValueError normal/-O.
Inputs unchanged, detached native outputs. Retained kernel corners/integrals,
coefficients, maps, bounds and endpoint values obey bits; unretained products,
nodes and antiderivative terms may cancel. Not exhaustive hostile graph,
work/memory or production hardening. Geometry validation does not rederive
the physical meaning of arbitrary G.

## Family outputs and actual endpoints

Family EXACT {problem,geometry,kernels,maps,bounds,certification,witnesses,
comparison,checks,counts}.
geometry EXACT {volume,cell_volumes,tile_volumes,target_scales,
defined_rows,undefined_rows}; V,h_C,h_t,sigma,partition q.
Undefined normalized values NULL; full raw maps/corner data remain complete.

kernels EXACT (also inspect_kernel output):
{corner_values,tile_integrals,bernstein_integrals,tile_abs_upper,
tile_minima,tile_maxima,tile_classes}.
corner_values q*t*4; tile_integrals q*t are actual integral k;
bernstein_integrals q*r are actual integral k*phi (NO V² or sigma);
tile_abs_upper q*t=h_t max|corner|; minima/maxima q*t actual kernel extrema;
tile_classes q*t strings above. Corners are evaluations, not field coefficients.
All kernel rational entries are retained, including zeros and undefined rows.

maps EXACT {decoder_bank,bank_residual,raw_bilinear_target,normalized_bilinear_target};
K=DB, K-G (zero), J=V²*bernstein_integrals, A_i=J_i/sigma or null.
First3 q*r, last q rows lengthr or null.

bounds EXACT {constant_lower,bilinear_lower,corner_upper,certified_gain,maxima}.
First3 q rational-or-null vectors C,L,U, null iff undefined.
certified_gain q rational iff defined and no mixed tiles, otherwise null.
maxima EXACT {constant_lower,bilinear_lower,corner_upper,certified_gain};
each {gain,rows}, all maximizing ties in its own nonnull domain;
empty domain gain null/rows[]. Certified maximum is over certified subset,
NOT an all-target exact maximum when other defined rows are uncertified.

certification EXACT {status,mixed_obstructions,certified_rows,uncertified_rows,
undefined_rows,nonnegative_rows,nonpositive_rows,zero_rows,
integrated_nonnegative_rows,integrated_nonpositive_rows,integrated_zero_rows,
integrated_nonnegative_mixed_rows}.
status q strings undefined/certified/uncertified, partition q.
mixed_obstructions q lists of {tile,positive_corner,negative_corner}, ordered
tiles and FIRST matching corner index in00,10,01,11. Undefined G0 lists empty.
nonnegative/nonpositive rows test ALL actual corners on defined rows; zero
their intersection. Integrated lists test A analogously.
integrated_nonnegative_mixed_rows is intersection of integrated nonnegative
rows and uncertified rows; preserve this diagnostic even when nonempty.
Tilewise sign-definite rows can have globally opposite signs across tiles.

witnesses EXACT {tile_constant,bilinear,constant_positive,constant_negative}.
First2 q entries {target_row,signs,positive,negative} if defined, else null.
tile_constant signs lengtht = sign(integral_tile k_it), zero->0;
actual corners repeat each tile sign4 times. bilinear signs lengthr=sign(A_i).
Each positive/negative endpoint EXACT
{corners,local_coefficients,global_coefficients,local_moments,bank_error,
tile_minima,tile_maxima,observed_error,direct_error,decoded_error,
normalized_error,attained}.
First5 lengthr,tile extrema t,observed s,raw direct/decoded q,
normalized q(null precisely undefined),attained rational.
ACTUAL call integrate(probe,tile_bounds,c), produce(B,bank), produce(G,bank),
apply(D,observed) for EVERY endpoint. Retain all off-target values.
Check field bounded byV², decoded=direct, normalized=A c, all defined outputs
within L and U; designated attained +/-C or +/-L as appropriate.
On certified rows require C=L=certified_gain and tile signs align with kernel
where nonzero. This is an analytic exactness certificate plus an actual witness,
not an exhaustive sign-field search or a claim that U is attained.

Also run two complete all+1/all-1 global constant corner pipelines even if
all queries undefined. constant_positive/negative use same endpoint EXCEPT
attained OMITTED; normalized output equals +/-sum(A_i), not assumed +/-L.
No generic simultaneous attainment or full maximizing-face claim.
There are exactly4d+2 public integrate,8d+4 produce,4d+2 apply calls REQUIRED
for endpoints/constant controls; reference may have additional independent
probes but must contain this complete call multiset.

comparison EXACT {bilinear_minus_constant,upper_minus_bilinear,upper_minus_certified}.
Each {gain_gap,strict_rows,tied_rows,unavailable_rows,max_gap,max_gap_rows}.
First2 use L-C,U-L over defined domain; third U-certified over certified
domain. Unavailable includes undefined AND uncertified where applicable;
every comparison partitions q, maximum over available domain only.

checks EXACT true after actual verification:
geometry_partitions,bank_label_identity,frozen_bank_identity,kernel_corner_identity,
kernel_integrals,bernstein_integrals,corner_envelope,normalization_domain,
bound_order,sign_partition,obstruction_inventory,certified_exactness,
endpoint_field_bound,endpoint_pipeline,lower_attainment,constant_controls,
complete_comparisons.

counts EXACT:
cells,positive_cells,tiles,bank_values,receiver_values,target_rows,defined_rows,
undefined_rows,geometry_input_entries,input_matrix_entries,geometry_entries,
kernel_entries,map_entries,bound_entries,comparison_entries,mixed_tiles,
mixed_rows,certified_rows,pointwise_nonnegative_rows,pointwise_nonpositive_rows,
pointwise_zero_rows,integrated_nonnegative_rows,integrated_nonpositive_rows,
integrated_zero_rows,integrated_nonnegative_mixed_rows,tile_constant_witnesses,
bilinear_witnesses,constant_witnesses,tile_sign_entries,bilinear_sign_entries,
endpoint_entries,constant_endpoint_entries,constant_gap_strict,upper_gap_strict,
certified_upper_gap_strict,constant_maximizers,bilinear_maximizers,
upper_maximizers,certified_maximizers.
Let a=positive cells,d=defined rows,z=certified rows.
geometry_input_entries=4+4a+4t; input_matrix_entries=sr+qr+qs.
geometry_entries=1+c+t+q; kernel_entries=12qt; map_entries=(3q+d)r.
bound_entries=3d+z+(3 if d else0)+(1 if z else0).
comparison_entries=2d+z+(2 if d else0)+(1 if z else0).
tile_constant_witnesses=bilinear_witnesses=2d; constant_witnesses=2;
tile_sign_entries=dt; bilinear_sign_entries=dr.
endpoint_entries=4d*(5r+2t+s+2q+d+1).
constant_endpoint_entries=2*(5r+2t+s+2q+d).
Remaining counts literal list lengths, mixed_tiles=sum obstruction lengths.
Count rational zeros/repetitions, not nulls/labels/sign indices or counts.

## Independence and controls

Primary: explicit global bilinear corner evaluation and monomial antiderivatives,
separable corner-basis expansion and scalar/matrix propagation.
Reference: local interpolation from independently evaluated physical vertices,
tensor-Simpson actual kernel/field integrals and independent response probes.
Third tests: independent polynomial dictionaries/antiderivatives/scalar products,
literal small examples and small corner cubes. No shared mathematical helpers,
other engine/oracle source reading, older executor imports or stored AY answers.
Authors may reuse their OWN AX code/admission/integration patterns in the NEW
standalone source, with no runtime imports of prior executors. Root owns runner.
Fixed tests lazy; names contain fixed. Generic tests must not load fixed inputs.

Required synthetic failures/controls: k=xi-1/4 with all integrated A columns
positive but mixed physical corners; +1/-1 kernels on different tiles needing
tilewise signed constants; k=xi eta with zero edges and loose U despite exact
certification; saddle alternating signs and zero mean; defined zero kernels;
mixed/null/all-undefined subsets with cancelling D; no receivers; actual
endpoint call inventories; signed/unequal/translated tiles and matching tile/
column permutations; partial/empty API geometry; cap edges as separate small
workloads; shape/value-before-arithmetic, bits/cancellation/cycles/detachment.
No fitting or changing the model after observing a fixed failure.

Synthetic positive affine u'=a*u+b,v'=c*v+d,k=ac>0, existing conventionF'=k²F.
Under monomial transport S=blockdiag(k³M) and explicit invertible T,
B'=T B S^-1,G'=k⁴G S^-1,D'=k⁴D T^-1,sigma'=k⁴sigma.
Actual kernel corners/extrema scale k; tile kernel and Bernstein integrals and
tile_abs_upper scale k²; raw field moments transform S, actual field extrema
and local coefficients scale k²; normalized C,L,U,certificates/gaps and endpoint
responses invariant. All full raw responses/observed values transform as declared.
No fixed affine variants or claim fixed grid/warp are one affine transform.

## Historical bridge and frozen evidence

Input ONLY AX family.problem's same nine fields, grid then warp,c8,t12,r48,s37,q64.
Newly recheck selected geometry and full DB=G. Independently compute J,A,L and
constant_response=sumA from actual kernel/basis integrals and require equality
to AX maps.target_error/normalized_target,field.row_gains and
positivity.constant_response. No AX endpoint, Q/W/inverse, AW baseline,
enclosure, source integral, overlay, rank, fit or older executor replay.
New AY kernel and witness integrals are explicitly permitted calculations.
project_inputs(previous) accepts AX FAMILIES LIST, returns(problems,previous).
load_inputs reads prior_document()['suite']['families'].

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {selected_families:["grid","warp"],AX_problem_equal:true,
AX_geometry_equal:true,AX_bilinear_map_equal:true,AX_bilinear_gain_equal:true,
AX_constant_response_equal:true,same_response_maps:true,
broader_field_error_domain:true,AX_endpoints_replayed:false,
other_historical_mathematics_replayed:false,older_executors_run:false}.
payload per family EXACT {family,input_bytes,geometry_bytes,kernel_bytes,map_bytes,
bound_bytes,certification_bytes,witness_bytes,comparison_bytes,native_family_bytes}.
Canonical JSON+newline projections overlap, not additive unique storage or packets.
totals sum39 counts plus families=2.

scope EXACT all false:
source_dictionary_changed,old_source_or_target_integrals_recomputed,
repair_overlay_regenerated,decoder_refitted,filters_reselected,measurements_added,
normalization_row_added,empirical_noise_calibrated,total_source_nonnegativity_guaranteed,
global_field_continuity_required,mixed_absolute_kernel_integrated,
uncertified_exact_gain_claimed,corner_envelope_sharpness_claimed,
integrated_positivity_used_as_pointwise_certificate,equal_noise_sensor_improvement_claimed,
full_field_stability_tested,unknown_geometry_reconstructed,physical_sensor_validated,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.

AX pin1925803 bytes SHA256
80020730e21d2c5731b6f6d5a94add1faa6739c815ac3e82087126d45667f1b0.
AX plus54 priors=55 captures; AX5 sources plus89 ancestors=94 ancestors;
AY5 sources=154 distinct identity targets. Freeze README.md,kernel.py,
reference.py,study.py,test_qr05ay.py after generic normal/-O tests and reviews,
BEFORE any assembled fixed AY input or math. First compare; exactly ONE
independent normal reference-only read-only audit; full normal/-O tests;
post-test identity/first-byte bracket; external create-only comparison preflight;
exclusive final capture; fresh primary-normal/reference--O read-only replays.
Audit and full tests may run concurrently but finish before preflight.
All154 identities/capture bytes bracketed; first/preflight/final nonruntime equal.
Disclose every post-first correction. Isolated Python/fresh external caches,
no dependencies. Capture128MiB/serialized working192MiB are not work/memory caps.
RESULTS.md/roadmap outside five-source ledger. Publish ONLY this gate's seven
files and roadmap, preserving previous captures and unrelated tracks/temp sheet.

