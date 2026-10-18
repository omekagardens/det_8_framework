# QR-05AX protocol: bounded bilinear field-error realization

8 September 2026 (Honolulu). Prospective before fixed AX inputs or mathematics.
Base: pushed AW commit 2557a122da2341c87f0bdf544909676ea74ae5c5.
Prior published schema/results may be read to specify this bridge; no assembled
fixed AX input, field integration, corner map, gain or witness calculation
before the five-source freeze. Preserve other tracks and previous evidence.

## Question and scope

Replace AW's freely variable local moment errors with explicitly integrated
signed tilewise bilinear field perturbations. Keep the SAME supplied geometry,
B,G,D with DB=G and target reference convention. Four corner coefficients per
tile remain four coordinates: a smaller full-dimensional error body, not
dimension reduction, new measurements or improved equal-noise precision.

DeltaF_t = V² sum_a c_ta phi_a(xi,eta), |c_ta|<=1,
with corners/basis functions in order
00:(1-xi)(1-eta), 10:xi(1-eta), 01:(1-xi)eta, 11:xi eta.
The basis is nonnegative and sums to1 on the tile. Therefore its corner extrema
bound the entire field by +/-V². Tile-boundary jumps are permitted; shared
edges have zero area. This is not a continuous field or a positivity guarantee
for the perturbed total source, an empirical noise model or an apparatus law.
V² is the SAME declared amplitude convention as AW.

Only the declared finite bilinear error class has a sharpness claim. No
arbitrary bounded-field sharpness, underlying source-dictionary extension,
new physical law, gravity, metric recovery or ontology is inferred.

## Generic input and public APIs

Problem EXACT:
{family,probe,cells,tiles,bank_labels,target_labels,interface,geometric,decoder}.
family native nonempty str; probe positive [u0,u1,v0,v1].
cells c=1..8 sorted unique signed native int event IDs, entries {event,bounds};
bounds positive rectangle or null. Positive cells partition the probe.
tiles t=1..256 positive {event,bounds}, each inside a named positive cell,
pairwise disjoint interiors, covering every positive cell. Keep GIVEN tile order.
bank_labels EXACT [{tile:i,basis:j} for i in range(t),j in range(4)];
raw basis order (1,u,v,uv), native indices. r=4t.
target_labels q=1..64 sorted unique {first,second}, valid cell IDs.
Subsets/all-undefined target queries admitted. B s*r,s=0..320; G q*r; D q*s.
For a target containing a null cell require full G row0; D can be nonzero if
it cancels on B. Check DB=G on ALL raw rows before any error restriction.

APIs:
build_family(problem);
synthesize(blocks,values): t four-by-four blocks and length4t values,
t=0..256; supplied forward/inverse actions, no geometry or files;
produce(matrix,values): h*w times w,h=0..1024,w=0..1024;
apply(matrix,observed): q*s times s,q=0..64,s=0..320;
integrate(probe,tiles,corners): positive probe, list of t=0..256 positive
rectangle BOUNDS (not event records), and length4t corner vector. Tiles inside
probe, disjoint interiors; standalone tiles need NOT cover probe (field zero
outside them). Empty tiles/corners admitted. Arbitrary signed corners allowed;
the unit bound is imposed on family witnesses, not on this integration
API's inputs. Coefficients and moments are linear in corners; extrema are not.
Output EXACT {local_coefficients,global_coefficients,
local_moments,raw_moments,minima,maxima}, first4 lengthr, last2 lengtht.
Coefficients represent ACTUAL deltaF, not deltaF/V²: local basis(1,xi,eta,xi eta),
global basis(1,u,v,uv). Local moments are divided by V² h_t; raw moments are
actual integrals against global monomials. Min/max are actual field extrema
V²*min/max(c_t), not extrema of the moment coordinates.

All native dict/list/keys, reduced [n,d],d>0, native integer components<=4096
bits. Reject bool/float/container/scalar subclasses, unknown fields, malformed
labels/shapes/pairs/raggedness/caps/owners/nonpositive geometry. Complete
container/dimension/label/rectangle/pair SHAPES before Fraction arithmetic,
all scalar admission before geometry/products. Explicit ValueError normal/-O.
Active cycles rejected; shared children accepted; inputs unchanged and detached
native outputs. Retained coefficients, inverses, maps, moments, extrema and
witness components obey bit limit; unretained products/quadrature nodes may
cancel. No exhaustive graph/work/memory or production hardening claim.
Raw synthesis/produce/apply do not access geometry, hidden sources or files.
Generic geometry checks do not rederive the physical meaning of arbitrary G.

## Geometry, moments, baselines and new maps

dmu=du*dv/2, V=probe volume, h_t tile volume, h_C=cell volume or0.
sigma_(C,D)=V² h_C h_D; defined iff positive, otherwise UNDEFINED.
w_t=V² h_t. For actual tile origin(a,b), widths(du,dv):
W_t=w_t*[[1,0,0,0],[a,du,0,0],[b,0,dv,0],
          [a*b,du*b,a*dv,du*dv]]; Z_t=W_t^-1.
Derive and check both WZ=ZW=I4 blockwise. Never use stale coarse/probe blocks.

Derive the universal Q by integrating each corner basis against
m=(1,xi,eta,xi eta) on [0,1]². Rows m, columns corners:
[[1/4,1/4,1/4,1/4],
 [1/12,1/6,1/12,1/6],
 [1/12,1/12,1/6,1/6],
 [1/36,1/18,1/18,1/9]].
Independently derive inverse U=Q^-1; check QU=UQ=I4.
Q entries nonnegative, row sums rho=(1,1/2,1/2,1/4)<=1 prove containment
of Q[-1,1]^4 in AW's moment cube. This does not reduce dimension.
P_t=W_t Q; x=Qc tilewise, e=P c=W x.
Retain Q,U,rho ONCE and W,Z,P per tile; no dense r*r representation required.

Recheck selected AW local-box baselines, not its endpoint executors:
H0=B W, J0=G W, A0_i=J0_i/sigma_i if defined else null.
beta0_l=sum|H0_l|, alpha0_i=sum|A0_i|,
gamma0_i=sum_l |D_il| beta0_l/sigma_i (undefined null).
These baseline maps/gains and geometry/W/Z must equal selected AW records in
fixed suite. Do not replay AW witnesses, ranks, old source integrals or earlier
executors. Recomputing these selected baselines is an explicit AX check.

K=DB, Rbank=K-G=0; H=B P, J=G P, L=DH, Rerror=L-J=0.
A_i=J_i/sigma_i, beta_l=sum|H_l|, E_il=D_il beta_l/sigma_i.
alpha_i=sum|A_i|, gamma_i=sum|E_i|, for defined targets only.
A/E/alpha/gamma are null iff undefined; raw maps and beta always complete.
Verify alpha<=gamma, alpha<=alpha0, gamma<=gamma0 and beta<=beta0.
Defined alpha=0 iff alpha0=0 (invertible Q/W); enclosure gain may remain positive.
Do NOT assume the gap gamma-alpha shrinks relative to the old gap.
For no defined targets, target maxima null/lists[]; for s=0 receiver maximum
gap null/list[]. Zero-valued defined gains have real witnesses/maxima.

## Actual field witnesses and constant-field diagnostics

For each defined target i, signs=sign(A_i), sign0=0; c=+/-signs.
Call integrate(probe, tile_bounds,c) to reconstruct BOTH local and global field
polynomials, actual raw/local integrals and actual tile extrema anew.
Separately call synthesize([Q]*t,c) and synthesize(P_blocks,c).
Require these equal integrated local/raw moments, respectively.
Call synthesize(Z_blocks,bank_error) to recover Qc,
and synthesize([U]*t,roundtrip_local) to recover c.
Then actual produce(B,bank_error), produce(G,bank_error) and apply(D,observed).
Retain complete vectors including undefined raw outputs. Require direct=decoded,
observed=Hc, all defined normalized outputs=A_h c and within alpha_h,
all receiver values within beta, tile field extrema within +/-V²,
|c_j|<=1 and designated attained=+/-alpha_i.
All zero/nonzero/off-target components checked, not only designated scalar.

Endpoint EXACT {corners,local_coefficients,global_coefficients,local_moments,
bank_error,integrated_bank_error,roundtrip_local,roundtrip_corners,
tile_minima,tile_maxima,observed_error,direct_error,decoded_error,
normalized_error,attained}. First8 fields lengthr, tile fields lengtht,
observed lengths, direct/decoded lengthq, normalized lengthq with nulls precisely
undefined. attained rational. Witness EXACT {target_row,signs,positive,negative}.
Undefined designated witnesses null. Each defined witness has both signs.

Also evaluate TWO actual global constant corner vectors c=all+1 and all-1
through the SAME integration/synthesis/inverse/produce/apply pipeline. Retain
constant_positive and constant_negative with the same endpoint fields EXCEPT
attained omitted. These two controls exist even if all targets undefined.
They need not attain sharp gains for arbitrary G. Complete constants are
additional controls, not chosen optimizing signs.

Enclosure |y_l|<=beta_l uses NEW field-body receiver radii. For each defined
i, signs=sign(E_i), y=+/-beta*signs, actual apply(D,y).
Endpoint EXACT {observed_error,decoded_error,normalized_error,attained}.
Full raw undefined outputs can be nonzero; never erase them.
Check all defined bounds and signed gamma_i attainment.
No fabricated field/corner/bank preimage and no general feasibility solver.
Canonical sign witnesses are not complete maximizing faces or simultaneous
attainment claims. All tied maximizing target indices are retained.

Classify each DEFINED A row: nonnegative if all>=0, nonpositive if all<=0,
mixed if both signs occur, zero if all0. Zero rows lie in BOTH nonnegative
and nonpositive lists. Mixed is complement of their union; zero intersection.
constant_response_i=sum_j A_ij (undefined null), and actual constant endpoints
must normalize to +/-constant_response. positive_constant_attains lists
defined rows where sumA=alpha; negative_constant_attains where -sumA=alpha.
These are tested diagnostics, not a premise that arbitrary G is nonnegative.

## Complete family wire and literal counts

Family EXACT {problem,geometry,coordinates,baseline,maps,field,enclosure,
comparison,positivity,checks,counts}.
geometry EXACT {volume,cell_volumes,tile_volumes,target_scales,
defined_rows,undefined_rows}, ordered as inputs.
coordinates EXACT {bank_scales,raw_from_local,local_from_raw,local_from_corner,
corner_from_local,raw_from_corner,corner_moment_row_sums};
w,W,Z,Q,U,P,rho respectively; Q,U single4x4, rho length4.
baseline EXACT {interface_error,target_error,normalized_target,receiver_radii,
shared_gains,enclosure_gains}: H0,J0,A0,beta0,alpha0,gamma0.
maps EXACT {decoder_bank,bank_residual,interface_error,target_error,
decoded_error,error_residual,normalized_target,enclosure_target}:K,Rbank,H,J,L,
Rerror,A,E.
field EXACT {row_gains,witnesses,max_gain,max_rows}.
enclosure EXACT {receiver_radii,row_gains,witnesses,max_gain,max_rows,
common_bank_feasibility_tested:false}.

comparison EXACT {field_vs_enclosure,field_vs_local,enclosure_vs_local,
receiver_reduction}. First3 EXACT {gain_gap,strict_rows,tied_rows,undefined_rows,
max_gap,max_gap_rows} for gamma-alpha, alpha0-alpha, gamma0-gamma.
Strict/tied/undefined partition q. receiver_reduction EXACT
{gain_gap,strict_rows,tied_rows,max_gap,max_gap_rows} for beta0-beta, lists over s.
Each maximum retains ALL tied indices; maxima null only when its domain empty.
positivity EXACT {nonnegative_rows,nonpositive_rows,mixed_rows,zero_rows,
constant_response,positive_constant_attains,negative_constant_attains,
constant_positive,constant_negative}.

checks EXACT true only after checks:
geometry_partitions,bank_label_identity,coordinate_inverse,moment_integrals,
moment_inverse,local_box_containment,frozen_bank_identity,error_map_identity,
baseline_dominance,normalization_domain,field_bound,field_pipeline,
field_attainment,enclosure_box,enclosure_attainment,constant_fields,
coefficient_sign_partition,complete_gain_partitions.

counts EXACT:
cells,positive_cells,tiles,bank_values,receiver_values,target_rows,defined_rows,
undefined_rows,geometry_input_entries,input_matrix_entries,geometry_entries,
coordinate_entries,baseline_entries,map_entries,gain_entries,comparison_entries,
positivity_entries,field_witnesses,field_sign_entries,field_witness_entries,
enclosure_witnesses,enclosure_sign_entries,enclosure_witness_entries,
constant_witnesses,constant_witness_entries,field_maximizers,enclosure_maximizers,
field_enclosure_strict,field_local_strict,enclosure_local_strict,receiver_strict,
nonnegative_rows,nonpositive_rows,mixed_rows,zero_rows.
Let d=number defined,a=positive cells.
geometry_input_entries=4+4a+4t; input_matrix_entries=sr+qr+qs.
geometry_entries=1+c+t+q; coordinate_entries=49t+36.
baseline_entries=(s+q+d)r+s+2d; map_entries=5qr+sr+d(r+s).
gain_entries=s+2d+(2 if d else0).
comparison_entries=3d+s+(3 if d else0)+(1 if s else0).
positivity_entries=d (constant_response, not constant controls).
field_witnesses=2d;field_sign_entries=dr;
field_witness_entries=2d*(8r+2t+s+2q+d+1).
enclosure_witnesses=2d;enclosure_sign_entries=ds;
enclosure_witness_entries=2d*(s+q+d+1).
constant_witnesses=2;constant_witness_entries=2*(8r+2t+s+2q+d).
Remaining counts literal lengths. Count zeros/repetitions, not nulls or
labels/indices. No minimal-storage/measurement-cost claim.

## Independent implementations and controls

Primary: independently derived separable corner-basis integrals for Q,
triangular W/Z, exact block products; integrate actual expanded field
polynomials directly with physical monomial antiderivatives.
Reference: tensor Simpson integration of ACTUAL bilinear fields times local/
global monomials (coordinatewise degree<=2), separate pivoted inverses,
actual column probes and coordinate interval bounds; check WQ against direct
integrals rather than defining the integral by WQ.
Third test oracle: independent polynomial coefficient dictionaries and exact
antiderivatives/scalar contractions, with exhaustive SMALL corner/receiver
cube vertices. No shared math helpers, other-engine/oracle source reading,
older executors or stored AX answers. Authors may reuse OWN admission/lifecycle
patterns. Root owns runner. Fixed tests lazy and names contain fixed.

Controls: unit mass tying AW, higher-moment strict reduction, sign-changing
response where constant fields fail to attain, explicit constant fields,
cancelling and zero maps, unequal/translated/signed-origin tiles, wrong corner/
monomial/tile order, discontinuities, thin rectangles, null versus defined zero,
all-undefined queries, nonzero raw undefined enclosure output, empty receiver,
epsilon scaling, actual pipeline call inventories, bounds/inverses/retained
coefficients/maps/witness overflow versus canceled intermediate arithmetic,
shape-before-Fraction/value-before-geometry, cycles/shared inputs/detachment.
Cap edges in SEPARATE small workloads, not simultaneous worst case.

Synthetic positive affine u'=a*u+b,v'=c*v+d,k=ac:
F'=k²F, V'=kV,h'=kh,sigma'=k⁴sigma; normalized corners/Q/U unchanged.
Let M map global monomials under affine change and S=blockdiag(k³M).
W'=S W,P'=S P,Z'=Z S^-1.
For supplied invertible receiver transport T:
B'=T B S^-1,G'=k⁴G S^-1,D'=k⁴D T^-1.
Check transformed integrated raw errors S e, actual field extrema scaling k²,
local coefficient scaling k², local moments/corners unchanged, full target
outputs/scales k⁴, normalized maps/gains/null sets/maximizers and constants.
General T can change receiver reboxing; signed monomial T preserves gamma.
No fixed affine families or claim that grid and warp are such a transform.

## Historical bridge, suite and evidence lifecycle

Input ONLY the nine AW family.problem fields, fixed grid then warp,
c8,t12,r48,s37,q64. New engine rechecks geometry,W/Z,DB and SELECTED local-box
baseline maps/gains. Require exact equality with AW geometry, coordinates
bank_scales/raw_from_local/local_from_raw, maps interface_error/target_error/
normalized_target, enclosure.receiver_radii/row_gains and shared.row_gains.
No AW endpoint/constant (none existed) replay, historical overlay/rank/source
integration or older executor run. New field-error integrals are explicitly AX.
project_inputs(previous) takes the AW FAMILIES LIST, returns(problems,previous).
load_inputs uses prior_document()['suite']['families'].

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {selected_families:["grid","warp"],AW_problem_equal:true,
AW_geometry_equal:true,AW_coordinates_equal:true,AW_local_baseline_equal:true,
same_response_maps:true,new_field_error_domain:true,
AW_endpoints_replayed:false,other_historical_mathematics_replayed:false,
older_executors_run:false}.
payload_sizes EXACT per family {family,input_bytes,geometry_bytes,
coordinate_bytes,baseline_bytes,map_bytes,field_bytes,enclosure_bytes,
comparison_bytes,positivity_bytes,native_family_bytes}.
Canonical JSON+newline projections overlap, not additive unique storage or packets.
totals sums counts plus families=2.

scope EXACT all false:
source_dictionary_changed,old_source_or_target_integrals_recomputed,
repair_overlay_regenerated,decoder_refitted,filters_reselected,measurements_added,
normalization_row_added,empirical_noise_calibrated,stochastic_independence_assumed,
total_source_nonnegativity_guaranteed,global_field_continuity_required,
arbitrary_bounded_field_sharpness_claimed,common_bank_feasibility_solved,
same_error_domain_as_AW_claimed,equal_noise_sensor_improvement_claimed,
field_coordinate_dimension_reduced,full_field_stability_tested,
minimality_recomputed,unknown_geometry_reconstructed,physical_sensor_validated,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.

AW pin1341549 bytes SHA256
e14e357309ff98f9f93c8f23c603f62d9bf17b01b4515ee122a464671b205916.
AW plus53 priors =>54 captures; AW5 sources plus84 ancestors =>89 ancestors;
AX5 sources =>148 distinct identity targets. Freeze README.md,kernel.py,
reference.py,study.py,test_qr05ax.py after generic passes and independent
reviews BEFORE any assembled fixed AX input or field/baseline/map calculation.
First comparison; exactly ONE independent normal reference-only read-only
audit; full normal/-O tests; post-test bracket; external create-only comparison
preflight; exclusive final capture; fresh primary-normal/reference--O read-only
replays. Audit/full tests can run concurrently but both finish before preflight.
Bracket all148 identities and capture bytes; all first/preflight/final
non-runtime fields equal. Disclose every post-first correction.
Isolated Python/fresh external caches/no dependencies. Capture128MiB and
serialized working192MiB caps are not process-memory/work limits.
RESULTS.md and roadmap outside source ledger. Publish only this directory
and the roadmap; preserve RET/core/governance/temp sheet and earlier evidence.
