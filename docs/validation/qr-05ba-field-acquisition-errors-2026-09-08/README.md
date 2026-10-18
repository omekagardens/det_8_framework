# QR-05BA protocol: field-plus-acquisition error composition

8 September 2026 (Honolulu). Prospective BEFORE fixed BA projection or math.
Base: pushed AZ commit fb8170842b5d3efca57908c4699f645babc1baf1.
Freeze all FIVE sources before assembling fixed budgets/radii, field
summaries, acquisition maps, composed bounds or signed BA witnesses.
Inspecting prior published schemas/results to specify this bridge is allowed.

## Question, locations and deterministic uncertainty set

The SAME supplied geometry, kernels, target regions, receiver list and decoder
are used at parent/child integration resolutions. With actual raw global
field moments e(deltaF), additional receiver acquisition error n enters as

```text
y = B e(deltaF) + n
decoded = D y
D B = G                            full raw-bank identity, zero intercept
|deltaF| <= epsilon V² a.e.         SAME probe and amplitude at both levels
n_j = rho_j z_j, |z_j| <= eta       rho_j >= 0, epsilon >= 0, eta >= 0
```

The allowed set is the CARTESIAN PRODUCT of these field and acquisition
sets. This is deterministic separate admissibility, not stochastic
independence, a noise distribution, confidence coverage or calibration.
The field-induced receiver contribution B e(deltaF) is not counted twice
as n. Arbitrary correlations between actual errors can lie inside the set;
product-domain sharpness does not certify sharpness for a smaller coupled set.

Use dmu=du*dv/2, probe volume V, target sigma_i=V² h_C h_D.
For defined sigma_i>0, field C/L/S/U retain AZ's meaning:
C sharp tile-constant gain; L sharp independent corner-bilinear gain;
S=(V²/sigma_i) integral |k_i| the analytic full bounded-field gain;
U the conservative tile-volume times corner-supremum envelope.
C<=L<=S<=U. Do not integrate absolute mixed bilinear kernels.

K=D diag(rho) is the RAW acquisition map. H_i=K_i/sigma_i only if defined;
gamma_i=sum_j |H_ij|. Then the composed row quantities are

```text
Cbar_i = epsilon C_i + eta gamma_i
Lbar_i = epsilon L_i + eta gamma_i
Ubar_i = epsilon U_i + eta gamma_i
Sbar_i = epsilon S_i + eta gamma_i   analytic sharp product-domain gain
```

Numerically certify Sbar where the field S is certified OR epsilon=0.
Zero field budget makes the COMPOSED response exact without changing the
field kernel's certificate. Undefined normalized rows remain NULL even
if both budgets are zero; their raw Dn can be nonzero.
Partial available-exact maxima are over their OWN subset, not the full query.
A target-specific field and acquisition sign alignment proves sharpness;
do not claim one joint endpoint simultaneously attains all row bounds.

Refinement leaves rho, z, n, D and receiver ordering unchanged.
Parent corners restrict through convex E to correlated child corners.
Physical field, raw-moment sums, observations and composed responses agree.
Independent child corners still enlarge only the finite bilinear subclass.
Cbar/Lbar child-parent and Ubar parent-child gaps are epsilon times the
field gaps; the acquisition term cancels. Exact inherited values agree.

## Generic input and admission

Input EXACT {refinement,receiver_radii,budgets}.
refinement EXACT {parent,children}, the standalone AZ contract restated here.
parent EXACT nine fields:
{family,probe,cells,tiles,bank_labels,target_labels,interface,geometric,decoder}.
family nonempty native str. probe positive rectangle [u0,u1,v0,v1].
cells n=1..8 sorted unique signed native-int IDs, {event,bounds}; bounds
positive rectangle or NULL; positive cells partition probe.
Parent tiles p=1..256 positive {event,bounds}, partition named positive cells,
disjoint interiors, supplied order. Canonical bank_labels {tile:i,basis:j},
tile-outer, j=0..3=(1,u,v,uv), r_p=4p.
q=1..64 sorted unique target_labels {first,second}, valid IDs.
B s*r_p, s=0..320; G q*r_p; D q*s. FULL DB=G must hold.
Any null-cell target has sigma0 and entire G row0; cancelling nonzero D allowed.
No claim that geometry admission derives arbitrary supplied G's physical origin.

children native list m=1..256 EXACT {parent,bounds}: parent native tile INDEX
0..p-1, not an event ID. Positive child rectangles partition each named parent
with disjoint interiors. Arbitrary order/unequal cuts and one-child identities
allowed. Children inherit event IDs; r_c=4m, canonical child bank labels.
Child B/G duplicate each named parent's four global columns, D unchanged.

receiver_radii native list length s of nonnegative rationals rho.
budgets native list b=1..8 EXACT records {name,field,acquisition}.
name nonempty native str, unique within supplied list, preserve order.
field epsilon and acquisition eta nonnegative rational scalars; zero allowed.

ALL shapes/keys/labels/indices/uniqueness and rational pair SHAPES across
refinement, radii AND budgets checked BEFORE ANY Fraction construction.
ALL scalar values admitted before geometry, products or bound arithmetic.
Native reduced [n,d], d>0, native ints <=4096 bits; reject bool/float/subclasses,
unknown fields, malformed/cap/shape/ownership violations and active cycles
with explicit ValueError normal/-O. Shared containers allowed, no mutation,
detached native outputs. All retained rational components <=4096 bits,
including E, field evidence, K/H, composed bounds and endpoint values;
unretained products/antiderivative terms may cancel.
Not exhaustive hostile-graph, memory, work or generic production hardening.

## Standalone public APIs

build_family(input).
integrate(probe,tiles,corners); inspect_kernel(probe,tiles,coefficients);
produce(matrix,values); apply(matrix,observed).
New standalone sources; no runtime imports of older engines/executors.

integrate: positive probe; t=0..256 positive disjoint rectangle BOUNDS inside
probe, partial/empty coverage allowed. Native arbitrary signed 4t corners.
deltaF=V² sum c_a phi_a on each tile and zero elsewhere; no caller field cap.
Output EXACT {local_coefficients,global_coefficients,local_moments,raw_moments,
minima,maxima}. First4 length4t; last2 lengtht.
Coefficients ACTUAL field in local/global (1,x,y,xy).
Raw moments actual integral deltaF*(1,u,v,uv)dmu; local moments / (V² h_t).
Extrema V² min/max corners. A BA field budget scales corners, NOT V.

inspect_kernel: same geometry, native q=0..64 rows of length4t.
Return kernels EXACT {corner_values,tile_integrals,bernstein_integrals,
tile_abs_upper,tile_minima,tile_maxima,tile_classes}.
corners q*t*4, integrals q*t actual integral k; Bernstein q*4t actual
integral k phi (NO V²/sigma); upper q*t=h_t max_corner |k|;
min/max q*t actual corner extrema. Disjoint tile classes:
zero, nonnegative(nonzero), nonpositive(nonzero), mixed.

produce: h*w times w, h=0..1024,w=0..1024.
apply: q*s times s,q=0..64,s=0..320.
Both geometry/file blind, zero-intercept.

## Family, field and acquisition records

Family EXACT {input,field,acquisition,cases,checks,counts}.
field EXACT {child_problem,geometry,restriction_blocks,levels}.
child_problem the derived nine-field child problem above.
geometry EXACT {volume,cell_volumes,target_scales,defined_rows,undefined_rows,
parent_tile_volumes,child_tile_volumes,child_parents}.
V; n cell volumes (0 for null); q scales (0 undefined); p/m tilevolumes;
m native lineage indices (not rational pairs).
restriction_blocks m*4*4, actual parent corner basis at child vertices
in order00,10,01,11. E>=0 and row sums1; sparse blocks, no dense R/E.

levels EXACT {parent,child}, each field level EXACT
{kernels,maps,bounds,certification}, as restated below.
maps EXACT {decoder_bank,bank_residual,raw_bilinear_target,
normalized_bilinear_target}: DB, DB-G, J=V² Bernstein, A=J/sigma.
First3 q*4t; normalized q rows length4t or NULL precisely undefined.
Compute independent parent/child integrals then check kernel corner restriction,
J_parent=J_child E, A_parent=A_child E, not use these as definitions.
Actual paired pipelines below independently check raw-moment additivity.

Field bounds EXACT {constant_lower,bilinear_lower,corner_upper,certified_gain,maxima}.
First3 C/L/U q nullable ONLY undefined. certified_gain q NULL for undefined OR
any mixed tile. If defined/all tiles sign-definite, certify C=L=S.
maxima EXACT those FOUR long fieldnames -> {gain,rows}; all ties in each
own nonnull domain; empty domain NULL/[].

Field certification EXACT {status,mixed_obstructions,certified_rows,
uncertified_rows,undefined_rows,nonnegative_rows,nonpositive_rows,zero_rows,
integrated_nonnegative_rows,integrated_nonpositive_rows,integrated_zero_rows,
integrated_nonnegative_mixed_rows}.
status q undefined/certified/uncertified. Obstructions q lists EVERY mixed tile
{tile,positive_corner,negative_corner} in supplied order, FIRST signed corner.
Pointwise lists test ALL actual corners on defined rows; integrated lists test A.
Zero is the intersection. integrated_nonnegative_mixed_rows is integrated
nonnegative AND uncertified. Undefined G0 kernels remain retained as zero.

acquisition EXACT {raw_map,normalized_map,gain,maxima}.
K raw q*s, H q rows length s or NULL precisely undefined.
gain gamma q NULL precisely undefined; maxima {gain,rows} all defined ties.
K may be nonzero on a null target even though the field G row is zero.
rho0/eta0/s0 cases remain explicit. K/H/gamma shared by both resolutions.

## Budget cases, exact availability and comparisons

cases list b, each EXACT {budget,levels,comparison,exact_bridge,witnesses}.
budget detached input budget record, same order.
levels EXACT {parent,child}; each case level EXACT {bounds,exactness}.
Case bounds EXACT {constant_lower,bilinear_lower,corner_upper,exact_gain,maxima}.
First3 Cbar/Lbar/Ubar q NULL ONLY undefined.
exact_gain q: NULL undefined; eta*gamma if epsilon=0; otherwise
epsilon*certified_field_gain+eta*gamma when field certified, NULL otherwise.
Maxima EXACT these four fieldnames -> {gain,rows}, all ties in own nonnull domain.
An available-subset exact maximum is NOT an all-target exact maximum.

exactness EXACT {reason,available_rows,unavailable_rows,undefined_rows}.
reason q, precedence:
undefined if sigma0;
zero_field_budget if defined and epsilon0 (even if field certified);
field_certified if defined, epsilon>0 and field certified;
unavailable otherwise.
The three index lists completely partition q. Do not modify field certificates.

comparison EXACT {constant_increase,bilinear_increase,upper_decrease}.
Each EXACT {gain_gap,strict_rows,tied_rows,unavailable_rows,max_gap,max_gap_rows}.
Cbar_child-Cbar_parent, Lbar_child-Lbar_parent, Ubar_parent-Ubar_child,
nonnegative on defined rows, NULL only undefined; full partitions/all max ties.
Empty available domain NULL/[]; epsilon0 makes all defined comparison gaps0.

exact_bridge EXACT {inherited_rows,newly_exact_rows,unavailable_rows,
undefined_rows,inherited_gain_residuals}.
First4 partition q: parent available; child available minus parent available;
child unavailable; undefined. Inherited cannot be lost.
q gain residual child-parent is rational0 only on inherited rows, NULL elsewhere.
Previously mixed field rows may be inherited exact when epsilon0, without
becoming field-certified. Epsilon>0 permits new child field certificates.

## Actual joint pipelines and canonical witnesses

Pipeline EXACT16:
{corners,acquisition_coordinates,global_coefficients,bank_error,
field_observed_error,acquisition_error,total_observed_error,
field_direct_error,field_decoded_error,acquisition_direct_error,
acquisition_decoded_error,total_direct_error,total_decoded_error,
normalized_error,tile_minima,tile_maxima}.
corners/globalcoeff/bank length4t; acquisition_coordinates z length s;
three observed/error vectors length s; SIX direct/decoded vectors length q;
normalized q NULL precisely undefined; extrema t.
Actual integrate -> produce(B,e),produce(G,e),produce(K,z);
n=diag(rho)z, y=field_observed+n;
apply(D,field_observed),apply(D,n),apply(D,y).
Total direct = field_direct + acquisition_direct; ALL direct/decoded pairs
equal, total equals component sum; normalized = A*c + H*z.
Check |c|<=epsilon, |z|<=eta, actual |field|<=epsilon V², |n_j|<=eta rho_j;
all defined actual total responses inside Lbar and Ubar.
No normalized local moments or implicit noise budget change.

PAIR EXACT15:
{parent,child,aggregated_bank_error,bank_residual,
field_observed_residual,acquisition_residual,total_observed_residual,
field_direct_residual,field_decoded_residual,acquisition_direct_residual,
acquisition_decoded_residual,total_direct_residual,total_decoded_residual,
normalized_residual,field_coefficient_residual}.
Two actual pipelines: parent c and child E c; EXACT same z and n.
Aggregate bank by plain lineage sum of four global entries, length r_p;
bank residual vs parent length r_p; three receiver residuals length s;
six direct/decoded residuals length q; normalized q nullableundefined;
field_coefficient_residual length r_c compares child ACTUAL global
coefficients with duplicated parent coefficients. Every residual zero
where defined. Keep complete raw off-target outputs including null targets.

witnesses EXACT8:
parent_pattern,parent_constant,parent_constant_maximizer,
parent_bilinear_maximizer,parent_exact_maximizer,
child_constant_maximizer,child_bilinear_maximizer,child_exact_maximizer.
First2 always {positive,negative} PAIRS.
Pattern positive parent corners epsilon*(-1,0,1,1/2) repeated per tile;
z_j=eta*(-1,0,1,1/2) by receiver index mod4.
Constant positive all parent corners epsilon; all z_j=eta.
Negative controls negate BOTH field corners and z.

Six maximizer groups NULL when indicated gain's nonnull domain is empty;
otherwise EXACT {target_row,field_signs,acquisition_signs,positive,negative}.
Choose FIRST maximizing row of that case level's indicated Cbar/Lbar/exact.
All ties remain in bounds. Constant/exact field_signs length t,
sign(integral k) at chosen row; bilinear field_signs length4t=sign(A).
If epsilon0 use all field_signs0 in ALL groups; exact with epsilon>0
requires certified field and its tilewise constant signs.
acquisition_signs length s: sign(K_ij), but ALL0 if eta0; rho0 yields sign0.
Physical corners = epsilon*field_signs (repeat4 for constant/exact);
z=eta*acquisition_signs. sign(0)=0; negative negates both complete inputs.
Parent groups positive/negative are PAIRS; child groups actual pipelines.
Designated total normalized response equals +/- indicated MAXIMUM gain.
No generic simultaneous attainment, no claim child maximizers have a parent preimage.
No per-row endpoint enumeration or mixed absolute-field integration.

Per case, with d defined rows and zp/zc available-exact rows:
parent PAIRS = 4 + 4*[d>0] + 2*[zp>0];
standalone child pipelines = 4*[d>0] + 2*[zc>0].
Actual public calls per pipeline: 1 integrate,3 produce,3 apply.
All-undefined still4PAIRS/8pipelines. Additional independent probes allowed;
complete mandatory call multisets must be present, not just total counts.

## Methods, controls and literal counts

Primary: own global monomial/separable-basis physical integrals and direct
contractions; reference: own physical interpolation/tensor-Simpson field
integrals and independent raw bank/receiver column probes; third oracle:
polynomial dictionaries/antiderivatives and scalar contractions/small cubes.
Authors may copy their OWN AZ/AY helpers into new standalone source,
not read other engine/oracle mathematical code or import older runtime engines.
Do not compute discarded full AZ families or replay its old endpoints.
Only the selected field geometry/E/level evidence is recomputed; BA endpoints
are new declared field-plus-acquisition calculations.

Controls: Cartesian vs coupled-error cancellation; opposite component signs;
nonzero rho with eta0, rho0, epsilon0, both budgets0; s0; definedzero,
mixed/null/cancellingD, all-undefined. Mixed field remains uncertified when
zero-field-budget total is exact. Exact subset maxima and all ties.
New child sign certificate vs unresolved mixed kernel, identity refinement,
strict finite-class/envelope changes vs epsilon0 ties; nonconstant paired
fields plus SAME n; input shape/value order incl budget/radius malformed
before geometry; cycles/sharing, bits/cancellation, caps and detachment.

Independent positive-affine synthetic field transports use F'=k²F and
unchanged normalized gains/E as AZ. For receiver transformations restrict
to positive diagonal scale/permutation T with rho'=T rho, so
B'=T B Sraw^-1, G'=k^4 G Sraw^-1, D'=k^4 D T^-1,
sigma'=k^4 sigma, n'=T n, eps/eta unchanged.
Sraw=blockdiag(k³ M), where M transports raw global monomials.
Allow signed T only with corresponding absolute-radius/sign transport.
General mixed receiver transforms turn boxes into zonotopes, NOT fresh
independent boxes: keep this as a synthetic counterexample, not a new API.
No fixed affine variants or intrinsic cross-geometry physical noise ranking.

checks EXACT16 true ONLY after verification:
parent_geometry,
child_partition,
lineage_identity,
full_bank_identity,
same_receiver_contract,
restriction_convexity,
field_level_evidence,
response_transport,
acquisition_map,
normalization_domain,
composed_bounds,
exact_availability,
refinement_comparison,
paired_field_noise_pipelines,
joint_maximum_attainment,
complete_inventory.

counts EXACT35 fields:
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
budgets,
input_geometry_entries,
input_matrix_entries,
input_budget_entries,
geometry_entries,
restriction_entries,
parent_kernel_entries,
child_kernel_entries,
parent_map_entries,
child_map_entries,
field_bound_entries,
acquisition_entries,
case_bound_entries,
case_exact_bridge_entries,
case_comparison_entries,
parent_paired_witnesses,
child_witnesses,
sign_entries,
witness_entries,
constant_strict,
bilinear_strict,
upper_strict,
inherited_exact_rows,
newly_exact_rows,
unavailable_exact_rows.
Let n,a,p,m,rp4p,rc4m,s,q,d,b as above; zfp/zfc=field-certified row counts;
for case k, zkp/zkc=available exact counts, Pk/Ck as prescribed witness counts.
input_geometry=4+4a+4p+4m; input_matrix=s*rp+q*rp+q*s;
input_budget_entries=s+2b.
geometry_entries=1+n+q+p+m; restriction_entries=16m.
parent/child kernels=12q*p /12q*m; maps=(3q+d)*rp /(3q+d)*rc.
field_bound_entries=sum levels[3d+zf+3*[d>0]+[zf>0]].
acquisition_entries=q*s+d*s+d+[d>0].
case_bound_entries=sum cases/levels[3d+zk+3*[d>0]+[zk>0]].
case_exact_bridge_entries=sum cases zkp.
case_comparison_entries=b*(3d+3*[d>0]).
Ep=3rp+4s+6q+d+2p; Ec=3rc+4s+6q+d+2m.
Epair=Ep+Ec+2rp+3s+6q+d+rc.
witness_entries=sum cases(Pk*Epair+Ck*Ec).
sign_entries per case:
[d>0]*(p+rp+m+rc+4s)+[zkp>0]*(p+s)+[zkc>0]*(m+s).
Remaining counts literal dimensions/row/pipeline totals; strict and exact
counts sum over cases (budget-target occurrences, NOT unique target rows).
Count rational zeros/repetitions; not NULLs, signs, labels, lineage indices,
reason/status strings, checks or count values.

## Fixed projection and suite

ONLY AZ's original input refinement, derived child_problem, geometry,
restriction.blocks and parent/child levels are selected for this bridge.
For EACH grid then warp, after freeze project:
refinement=AZfamily.input;
receiver_radii=[[1,1]] repeated s=37;
budgets in EXACT order:
{name:"zero",field:[0,1],acquisition:[0,1]},
{name:"field",field:[1,1],acquisition:[0,1]},
{name:"acquisition",field:[0,1],acquisition:[1,1]},
{name:"joint",field:[1,1],acquisition:[1,1]}.
The radius1 denotes ONE EXISTING RAW RECEIVER-COORDINATE UNIT, solely a
declared mathematical box; it is not apparatus data or matched physical
noise across differently scaled receiver coordinates/geometries.
No fitting, tuning or calibration from observed BA results.

Fixed n8,p12,m48,rp48,rc192,s37,q64. No new subdivision in BA.
Independently recomputed selected field evidence must match AZ exactly.
Do NOT consume AZ moment-block/transport/witness/comparison/count fields
as mathematical inputs or reconstruct discarded AZ endpoint families.
Older source/target integrals, overlay, decoder fitting/filter/rank paths
and all older executors remain excluded.

project_inputs(previousAZfamiliesLIST)->(inputs,previous).
load_inputs reads prior_document()['suite']['families'].
Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {selected_families:["grid","warp"],
AZ_refinement_equal:true,AZ_child_problem_equal:true,AZ_geometry_equal:true,
AZ_restriction_blocks_equal:true,AZ_levels_equal:true,
same_physical_field_domain:true,same_receiver_contract:true,
AZ_endpoints_replayed:false,AZ_unselected_mathematics_replayed:false,
older_executors_run:false}.
payload per family EXACT {family,input_bytes,field_bytes,acquisition_bytes,
case_bytes,native_family_bytes}. Canonical JSON+newline overlapping
projections, not additive unique/minimal storage or transmission packets.
totals sum35 counts plus families2.
scope EXACT all false:
source_dictionary_changed,
old_source_or_target_integrals_recomputed,
repair_overlay_regenerated,
decoder_refitted,
filters_reselected,
measurements_added,
normalization_row_added,
empirical_noise_calibrated,
statistical_independence_assumed,
field_receiver_error_double_counted,
total_source_nonnegativity_guaranteed,
global_field_continuity_required,
mixed_absolute_kernel_integrated,
uncertified_exact_gain_claimed,
corner_envelope_sharpness_claimed,
subset_exact_max_called_full_query_max,
independent_child_fields_called_parent_fields,
full_bounded_field_domain_changed,
equal_noise_sensor_improvement_claimed,
cross_geometry_physical_noise_ranking_claimed,
full_field_stability_tested,
unknown_geometry_reconstructed,
physical_sensor_validated,
quantum_channel_constructed,
gravity_derived,
ret_integration_tested,
lean_verification_performed,
generic_production_API_hardened,
fixed_affine_families_run,
older_executors_run.

AZ pin 2380556 bytes SHA256
cbb04f7a4af49a5714ecf80652393933557f490f7e16dab0848b8d32cda27585.
AZ+56priors=57captures; AZ5+99ancestor sources=104ancestors;
BA5sources =>166distinct identities.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05ba.py after generic
normal/-O passes and independent reviews, BEFORE any fixed BA projection/math.
First compare; exactly ONE independent NORMAL reference-only read-only audit;
full normal/-O tests (may overlap audit); post-test identity/first-byte bracket;
external create-only comparison preflight; exclusive final capture; fresh
primary-normal/reference--O read-only replays. All166/capturebytes bracketed;
first/preflight/final non-runtime equal. Disclose every post-first correction.
Isolated Python/fresh external caches; no new dependencies.
Capture128MiB/serializedworking192MiB are not process-memory/work caps.
RESULTS.md/roadmap outside five-source ledger. Publish only seven gate files
plus roadmap. Preserve unrelated RET/core/governance work and temp model sheet.

## Roadmap checkpoint after this gate

BA closes only the declared deterministic composition question. Next is an
explicit bridge-design checkpoint: specify one operational event/readout
interface, one conventional geometric comparison, information access,
uncertainty sources and a possible failure criterion BEFORE more fixed
studies. Do not treat another sequence of algebraic checks as an empirical
gravity bridge. RET integration/quantum likelihood calibration, apparatus
data, Lean formalization and dynamical correspondence remain separate.
