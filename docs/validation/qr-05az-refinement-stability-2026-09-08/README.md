# QR-05AZ protocol: refinement stability of bounded-field responses

8 September 2026 (Honolulu). Prospective before fixed AZ projection or mathematics.
Base: pushed AY commit f40149f5db5edcb62981e0a969df45e22574a99e.
Freeze all FIVE sources before constructing fixed child rectangles or evaluating
fixed restrictions, moments, kernels, transports, bounds or witnesses.
Prior published schemas/results may be inspected to specify the bridge.

## Question and unchanged domain

Subdivide the supplied integration tiles WITHOUT changing the physical kernel,
probe, target-cell regions, measure dmu=du*dv/2, reference amplitude V²,
target scales sigma_i=V² h_C h_D, receiver list or decoder.
ALL measurable signed fields |deltaF|<=V² a.e. form the SAME domain before
and after refinement; boundaries may jump and edges have measure zero.

Raw GLOBAL monomial moments add: e_parent=R e_child, where R sums each
child's four (1,u,v,uv) entries into its named parent. NO volume, local
coordinate or Jacobian factor belongs in this summation.
B_child=B_parent R; G_child=G_parent R; D_child=D_parent.
Equivalently duplicate each parent's four B/G columns onto its children.
New moment coordinates are representation, not new physical measurements.

For parent bilinear corner data c, child corners are E c. Each child has
a4x4 block evaluating the parent's four corner functions at actual child
vertices in order00,10,01,11. E entries>=0, each row sums1.
Correlated child data describe EXACTLY the same parent field.
Allowing independent child corners enlarges the FINITE bilinear subclass,
not the full measurable bounded-field domain.

Let P_t be the4x4 map from normalized field corners to actual raw global
moments on tile t, with field deltaF=V² sum_a c_a phi_ta.
Compute parent and child blocks INDEPENDENTLY by integrating their own
physical basis fields, then verify P_parent=R P_child E.
Kernel integral and Bernstein transport, J_parent=J_child E and
A_parent=A_child E must also hold, not be used as definitions.

For each defined target:
C=(V²/sigma)sum_tiles|integral k|;
L=sum|A|, A=(V²/sigma)integral k phi;
U=(V²/sigma)sum_tiles h_t max_corner|k|.
C<=L<=S<=U, with analytic S=(V²/sigma)integral_probe|k| over all bounded fields.
C_child>=C_parent; L_child>=L_parent; U_child<=U_parent.
These inequalities need not be strict. Exact S is representation-invariant.
Sign-definite parent tiles remain sign-definite after restriction.
Parent-certified rows stay certified with the SAME exact gain.
A previously mixed parent may become certified or remain uncertified.
Parent-route exact NULL remains NULL in that level's record even when child
certification newly supplies the numerical gain of the SAME functional.
Do not integrate absolute mixed bilinear kernels or assume every refinement
resolves their sign boundary. Integrated nonnegative coefficients alone
are not pointwise certificates. No U sharpness or strict-improvement promise.

## Generic input and admission

Input EXACT {parent,children}.
parent is AY's EXACT nine-field problem
{family,probe,cells,tiles,bank_labels,target_labels,interface,geometric,decoder}.
family nonempty native str. probe positive [u0,u1,v0,v1].
cells n=1..8 sorted unique signed native-int IDs, {event,bounds}; bounds
positive rectangle or NULL; positive cells partition probe.
Parent tiles p=1..256 positive {event,bounds}, partition named positive cells,
disjoint interiors, preserve given order. Parent bank_labels exactly
{tile:i,basis:j}, tile-outer/basis-inner j=0..3=(1,u,v,uv), r_p=4p.
q=1..64 sorted unique target_labels {first,second}, valid cell IDs.
B s*r_p,s=0..320; G q*r_p; D q*s. Check FULL DB=G.
Null-cell targets have sigma0 and entire G row0; nonzero cancelling D admitted.

children native list m=1..256 of EXACT {parent,bounds}, where parent is a
native int index0..p-1, not an event ID; bounds positive rectangle.
Each parent's children partition that parent, with disjoint interiors.
A one-child identical rectangle is admitted; arbitrary child order,
unequal cuts and unchanged parents are admitted. No prescribed global grid.
Children inherit the parent's event; preserve supplied child order.

ALL shapes/keys/labels/indices and rational pair SHAPES of BOTH parent and
children must be checked BEFORE ANY Fraction construction. ALL scalar values
must be admitted before geometry, restriction or products.
Rationals native reduced [n,d],d>0,native ints<=4096bits.
Reject bool/float/subclasses, unknown fields, malformed/cap/shape/ownership
violations and active cycles with explicit ValueError normal/-O.
Shared children allowed; input unchanged and native outputs detached.
All retained rational components<=4096bits, including E/P, kernel values,
maps, residuals, bounds and endpoint fields. Unretained products/nodes/
antiderivative terms may cancel. Not exhaustive hostile-graph, memory,
work-budget or generic production hardening. Arbitrary G's physical meaning
is NOT derived by geometry admission.

## Public APIs and common level records

build_family(input).
integrate(probe,tiles,corners), inspect_kernel(probe,tiles,coefficients),
produce(matrix,values), apply(matrix,observed) retain AY's exact public
contracts below, implemented in NEW standalone source, no old runtime imports.

integrate: positive probe; native list of t=0..256 positive disjoint rectangle
BOUNDS inside probe, partial/empty coverage allowed; arbitrary signed4t corners.
Field zero outside supplied tiles. Output EXACT
{local_coefficients,global_coefficients,local_moments,raw_moments,minima,maxima}.
First4 length4t,last2 lengtht. Coefficients actual deltaF in local/global
(1,x,y,xy); raw actual integrals; local moments divided by V² h_t;
minima/maxima=V² min/max corners. No field bound imposed on standalone callers.
inspect_kernel: same probe/tiles; native q=0..64 coefficient rows of length4t.
Output kernels EXACT {corner_values,tile_integrals,bernstein_integrals,
tile_abs_upper,tile_minima,tile_maxima,tile_classes}.
For t tiles: corners q*t*4 actual kernel evaluations, integrals q*t actual
integral k, Bernstein q*4t actual integral k phi (NO V²/sigma),
upper q*t=h_t max|corner|, minima/maxima q*t actual kernel extrema,
classes q*t strings zero/nonnegative/nonpositive/mixed, disjoint as AY.
produce: h*w times w,h=0..1024,w=0..1024.
apply: q*s times s,q=0..64,s=0..320.
Both file/geometry blind, zero-intercept.

A level EXACT {kernels,maps,bounds,certification}.
maps EXACT {decoder_bank,bank_residual,raw_bilinear_target,normalized_bilinear_target}.
K=DB,K-G,J=V²*Bernstein, A=J/sigma. First3 q*4t,lastq rows length4t orNULL.
bounds EXACT {constant_lower,bilinear_lower,corner_upper,certified_gain,maxima}.
First3 C/L/U nullableONLYundefined; certified_gain nullableundefined OR
any mixed tile. Certify C=L=exact iff defined and all tiles sign-definite.
maxima exactly those4 fieldnames -> {gain,rows}, all ties in own nonnull domain.
Empty domain NULL/[]; certified subset maximum is not all-target exact maximum.

certification EXACT {status,mixed_obstructions,certified_rows,uncertified_rows,
undefined_rows,nonnegative_rows,nonpositive_rows,zero_rows,
integrated_nonnegative_rows,integrated_nonpositive_rows,integrated_zero_rows,
integrated_nonnegative_mixed_rows}.
status q undefined/certified/uncertified; mixed_obstructions q lists of
{tile,positive_corner,negative_corner}, EVERY mixed tile in supplied order
and FIRST matching positive/negative corner index. Pointwise lists test ALL
actual corners on defined rows; integrated lists test A; zero is intersection.
integrated_nonnegative_mixed_rows is integrated nonnegative & uncertified.
Undefined G0 kernels remain fully retained as zero; maxima/null domains explicit.

## Family record and complete transport

Family EXACT {input,child_problem,geometry,restriction,levels,transport,
comparison,certification_bridge,witnesses,checks,counts}.
child_problem same9 fields, SAME family/probe/cells/target_labels/D,
child tiles and canonical child bank_labels, duplicated B/G blocks as above.
geometry EXACT {volume,cell_volumes,target_scales,defined_rows,undefined_rows,
parent_tile_volumes,child_tile_volumes,child_parents}.
volume V; cell_volumes n (zero for NULL); scales q (zero undefined);
tile volumes p/m; child_parents m native indices (not rationals).

restriction EXACT {blocks,parent_moment_blocks,child_moment_blocks,
aggregated_moment_blocks,moment_residuals,row_sums,min_weights,max_weights}.
blocks m*4*4 are E_child; parent P p*4*4; child P m*4*4.
aggregated P p*4*4=sum_children P_child E_child; residual aggregated-parent.
row_sums m*4 all1; min/max weights lengthm over each4x4 E block.
Sparse lineage+4x4 blocks represent R/E; do NOT store dense R/E.
levels EXACT {parent,child}, level records above.

transport EXACT {aggregate_kernel_integrals,aggregate_bernstein_integrals,
kernel_integral_residuals,bernstein_residuals,restricted_raw_target,
raw_target_residuals,restricted_normalized_target,normalized_target_residuals}.
aggregate kernel q*p sums child integral k by lineage;
aggregate Bernstein q*r_p sums child Bernstein row blocks times E_child;
residuals aggregate-parent corresponding integrals.
restricted raw q*r_p=J_child E; residual restricted-J_parent.
restricted normalized q rows lengthr_p orNULL=A_child E;
residual restricted-A_parent, NULL precisely undefined.
Verify child kernel corners=E_child times parent kernel corners, with
identical global kernel coefficient blocks. Preserve actual child corners.

comparison EXACT {constant_increase,bilinear_increase,upper_decrease}.
Each EXACT {gain_gap,strict_rows,tied_rows,unavailable_rows,max_gap,max_gap_rows}.
gaps C_child-C_parent,L_child-L_parent,U_parent-U_child over defined rows,
nonnegative, NULL only undefined. Complete q partitions and ALL maximum ties;
empty available domain NULL/[].

certification_bridge EXACT {inherited_rows,newly_certified_rows,
still_uncertified_rows,undefined_rows,inherited_gain_residuals}.
First4 partition q; inherited=parent certified; newly=child certified minus
parent certified; still=child uncertified. Parent-certified rows cannot be
lost. inherited_gain_residuals q rational0 only inherited, NULL elsewhere.
Do NOT require parent/child certificate statuses equal in general.

## Actual bounded witness pipelines

A pipeline EXACT {corners,global_coefficients,bank_error,observed_error,
direct_error,decoded_error,normalized_error,tile_minima,tile_maxima}.
corners/globalcoeff/bank length4t, observed s, direct/decoded q,
normalized q(NULL precisely undefined), extrema t.
ACTUAL integrate -> produce(B,bank),produce(G,bank) -> apply(D,observed).
Check |field|<=V², actual globalcoefficients/moments, decoded=direct=J*c,
normalized=A*c, all outputs within L and U. No hidden local normalization.

A parent/child PAIR EXACT {parent,child,aggregated_bank_error,bank_residual,
observed_residual,direct_residual,decoded_residual,normalized_residual,
field_coefficient_residual}.
parent/child are actual pipeline records for c and E*c.
aggregate bank lengthr_p by plain global-moment summation; residual vsparent.
observed s,direct/decoded q,normalized q(NULLundefined) residual child-parent.
field_coefficient_residual lengthr_c = actual child globalcoeff minus
duplicated parent globalcoeff. All residuals ZERO where defined.

witnesses EXACT {parent_pattern,parent_constant,parent_constant_maximizer,
parent_bilinear_maximizer,child_constant_maximizer,child_bilinear_maximizer}.
First2 always {positive,negative} PAIRS:
parent_pattern positive corners repeat(-1,0,1,1/2) perparenttile;
parent_constant all+1. Negative cases negate every corner.
The four maximizer groups NULL if no defined rows; otherwise EXACT
{target_row,signs,positive,negative}. Select FIRST maximizing row of C or L
at indicated level (all maximizing ties remain in that level's bounds).
C signs per tile=sign(integral k),zero->0, repeat4 to get corners.
L signs percorner=sign(A),zero->0.
Parent maximizer positive/negative are PAIRS; child maximizers are pipelines.
Check indicated level's designated response equals +/- its maximum C or L.
Child maximizers need NOT be parent-bilinear; do not claim a parent preimage.
These are canonical MAXIMUM witnesses, not per-row endpoint enumeration.
All-row sharp finite-class gains still follow from the exact row-coefficient
formula and sign choice; no infinite-field search or numerical mixed-|k| work.

With at least one defined row, actual witness requirements per family:
20 integrate,40 produce,20 apply calls (eight PAIRS plus four child pipelines).
All-undefined:8 integrate,16 produce,8 apply (four PAIRS).
Additional independent basis/column probes allowed, but all prescribed
pipeline calls must be present. No older endpoint replay.

## Counts, methods and controls

checks EXACT true only after verification:
parent_geometry,
child_partition,
lineage_identity,
frozen_bank_identity,
restriction_convexity,
raw_moment_additivity,
kernel_restriction,
kernel_integral_additivity,
bernstein_transport,
response_transport,
normalization_domain,
bound_monotonicity,
certification_inheritance,
parent_field_pipelines,
child_extremizer_pipelines,
constant_controls,
complete_comparisons.

counts EXACT34 fields:
cells,
positive_cells,
parent_tiles,
child_tiles,
parent_bank_values,
child_bank_values,
receiver_values,
target_rows,
defined_rows,
undefined_rows,
input_geometry_entries,
input_matrix_entries,
child_problem_geometry_entries,
child_problem_matrix_entries,
geometry_entries,
restriction_entries,
parent_kernel_entries,
child_kernel_entries,
parent_map_entries,
child_map_entries,
bound_entries,
certification_bridge_entries,
transport_entries,
comparison_entries,
parent_paired_witnesses,
child_witnesses,
sign_entries,
witness_entries,
constant_strict,
bilinear_strict,
upper_strict,
inherited_rows,
newly_certified_rows,
still_uncertified_rows.
Let n=cells,a=positivecells,p=parenttiles,m=childtiles,r_p=4p,r_c=4m,
s=receivers,q=targets,d=defined,z_p/z_c=parent/child certified.
input_geometry=4+4a+4p+4m; input_matrix=s*r_p+q*r_p+q*s.
child_problem_geometry=4+4a+4m; child_problem_matrix=s*r_c+q*r_c+q*s.
geometry_entries=1+n+q+p+m.
restriction_entries=38m+48p.
parent/child_kernel_entries=12q*p /12q*m.
parent/child_map_entries=(3q+d)*r_p /(3q+d)*r_c.
bound_entries=sum over levels[3d+z+(3 if d else0)+(1 if z else0)].
certification_bridge_entries=z_p.
transport_entries=2q*p+4q*r_p+2d*r_p.
comparison_entries=3d+(3 if d else0).
parent_paired_witnesses=8 if d else4; child_witnesses=4 if d else0.
sign_entries=p+r_p+m+r_c if d else0.
For a parent pipeline E_p=3r_p+s+2q+d+2p, child E_c analogously;
a PAIR contains E_pair=E_p+E_c+2r_p+s+2q+d+r_c rational occurrences.
witness_entries=parent_paired_witnesses*E_pair+child_witnesses*E_c.
Remaining counts literal sizes/strict rows. Count rational zeros/repetitions,
not NULLs, signs, labels, lineage/corner indices or count values.

Primary: global monomial antiderivatives, separable physical basis blocks
and exact local parent-basis evaluation at child corners.
Reference: physical polynomial reconstruction/vertex interpolation and
independent tensor-Simpson parent/child integrals, endpoint-grid coverage
checks and independent response probes.
Third tests: polynomial dictionaries/antiderivatives/scalar contractions,
literal synthetics and small parent/child cubes.
Authors may reuse OWN prior AY admission/integration patterns in NEW source,
but no old runtime imports, old build_family replay, shared mathematical
helpers, other engine/oracle source reading or stored AZ answers.
Root owns orchestration. Test names containing fixed are the ONLY users of
fixed input projection and calculations; generic tests/collection stay lazy.

Synthetic controls: one-child identity; unequal/reordered/signed/translated
partitions; midpoint split of k=u-1/4 remains partly mixed with increased L;
split along its zero certifies a previously mixed parent; unresolved mixed
saddle; parent-corner restrictions vs child vectors outside their image;
parent/child corner cube bounds and C/L/U monotonicities incl ties;
two-stage restriction and raw aggregation composition; sameV²not childV²;
raw moments not unweighted normalized local moments; preserved target cells/
scales, receiver observations and D; zero/null/all-undefined/cancellingD;
no receivers; complete pipelines; malformed lineage/holes/overlaps/caps/
shapes/values, cycles vs sharing, bits/cancellation, detachment and ordering.
Independent synthetic positive affine transports preserve normalized gains
and restriction blocks under the declared F'=k²F convention; kernel values,
raw moments and target scales transform as AY. No fixed affine variants.

## Fixed bridge, suite and frozen evidence

Fixed input ONLY AY's family.problem nine fields, grid then warp,p12,r_p48,
s37,q64,n8. For EACH actual parenttile, AFTERfreeze construct midpoints and
FOUR child rectangles in order00,10,01,11 (lowerleft,lowerright,upperleft,
upperright), parent-outer/child-inner. m48,r_c192. No tuned/refit geometry.

Independently recomputed parent geometry, kernels, maps,bounds,certification
must equal those SELECTED AY records. Reorganize geometry keys explicitly;
child_parent lineage/childvolumes are new. AY witnesses/comparisons/counts,
AX auxiliary maps and older executors are not replayed. New AZ parent/child
basis/kernel/field integrals are permitted; no old source/target integrals,
overlay construction, decoder refitting, filtering or rank regeneration.

project_inputs(previousAYfamiliesLIST)->(inputs,previous).
load_inputs uses prior_document()['suite']['families'].
Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {selected_families:["grid","warp"],AY_problem_equal:true,
AY_geometry_equal:true,AY_kernels_equal:true,AY_maps_equal:true,
AY_bounds_equal:true,AY_certification_equal:true,same_physical_kernel:true,
same_receiver_observations:true,same_bounded_field_domain:true,
AY_endpoints_replayed:false,other_historical_mathematics_replayed:false,
older_executors_run:false}.
payload per family EXACT {family,input_bytes,child_problem_bytes,
geometry_bytes,restriction_bytes,level_bytes,transport_bytes,comparison_bytes,
certification_bridge_bytes,witness_bytes,native_family_bytes}.
Canonical JSON+newline overlapping projections, not additive unique storage/
minimal encoding/transmission packets. totals sum34 counts plus families2.

scope EXACT all false:
source_dictionary_changed,old_source_or_target_integrals_recomputed,
repair_overlay_regenerated,decoder_refitted,filters_reselected,measurements_added,
normalization_row_added,empirical_noise_calibrated,total_source_nonnegativity_guaranteed,
global_field_continuity_required,mixed_absolute_kernel_integrated,
uncertified_exact_gain_claimed,corner_envelope_sharpness_claimed,
independent_child_fields_called_parent_fields,full_bounded_field_domain_changed,
equal_noise_sensor_improvement_claimed,full_field_stability_tested,
unknown_geometry_reconstructed,physical_sensor_validated,quantum_channel_constructed,
gravity_derived,ret_integration_tested,lean_verification_performed,
generic_production_API_hardened,fixed_affine_families_run,older_executors_run.

AY pin2115070 bytes SHA256
a4dda392b4dd8f148389cb82c4187611c10b11e3f3e05f82e2779fbe3bf90874.
AY+55priors=56captures; AY5+94ancestor sources=99ancestors;
AZ5sources =>160distinct identities.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05az.py after generic
normal/-O passes and independent reviews, BEFORE fixed AZ child construction
or math. Firstcompare; exactlyONE independent NORMAL reference-only read-only
audit; full normal/-O tests (may run concurrently with audit); posttest
identity/first-byte bracket; external create-only comparison preflight;
exclusive final capture; fresh primary-normal/reference--O read-only replays.
All160identities/capturebytes bracketed; first/preflight/final nonruntime equal.
Disclose every post-first correction. Isolated Python/fresh external caches,
no dependencies. Capture128MiB/serializedworking192MiB are not work/memory caps.
RESULTS.md/roadmap outside five-source ledger. Publish ONLY gate's seven
files and roadmap; preserve older evidence, unrelated work and temp model sheet.
