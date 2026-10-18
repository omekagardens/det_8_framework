# QR-05AQ protocol: frozen-decoder source-span portability

8 September 2026. Prospective before fixed AQ mathematics.
Base: pushed AP commit 5b4d767a1942640c38b8205b9a30d50208becdb0.
Keep prior research, RET/core work, dependencies and temporary sheets untouched.

## Question and fixed boundary

Do the SAME two frozen coarse-response maps remain exact on an alternative
nonnegative source dictionary? Keep AO's geometry, full four-moment observation
interface, canonical compact policy and direct geometric policy unchanged.
This is noiseless SOURCE mismatch, not AP's arbitrary observation-corruption box.
Do not fit/select a new decoder, alter the incoming measurements or discard
intercepts. A canonical failure is not measurement insufficiency when the
geometric policy remains exact.

Use grid then warp, whole probe, AO l1 coarse/l2 fine: seven coarse/eight fine
cells, eight coarse/twelve fine tiles, 32 observations, all 49 coarse responses.
Nine new generators per positive fine tile give 108 columns per fixed family.
The new piecewise-polynomial span is larger than AO's rank-23 field span, but
no inclusion of AO's normalized convex hull in the new convex hull is claimed.
These nonnegative test fields need not be causal F_ab constructions, physical
sources, quantum states or gravitational sources. No full-field recovery test.

Authenticate AP's retained capture and AO through that ancestry. Consume AP's
embedded original coarse inputs/maps and AO's clipped fine cells/tiles.
The original O_old,Q_old and policies are inherited INPUTS. Recheck BOTH complete
old response identities; do not reconstruct old fields/ranks/noise bounds.
Derive all new geometry moments, outgoing branches, generators, measurements
and true responses independently. Do not feed stored moments or outgoing
coefficients into the engines. Selected old geometry moments are checked only
AFTER new calculations. No historical executor imports or execution.
No fixed AQ integration/residual/witness calculation before source freeze.

## Exact generic input and admission

Each independent engine exposes build_family(problem) and
apply(intercept,matrix,observed). Problem EXACT:
{family,probe,coarse_cells,fine_cells,coarse_tiles,fine_tiles,
old_observations,old_targets,canonical,geometric}.
family nonempty native string; probe positive rectangle [u0,u1,v0,v1].
Coarse/fine cells each 1..8 rows {event,bounds}; bounds positive rectangle or
null, sorted unique signed native integer IDs. These are ALREADY CLIPPED
regions inside the probe. Positive cells at each level have disjoint interiors
and cover the probe. Each positive fine cell has one containing coarse cell;
positive fine cells cover each positive coarse cell. Empty fine cells have
parent null. Full UNCLIPPED parenthood is not newly asserted by this generic
interface; fixed-case original parenthood remains inherited AO provenance.

Coarse tiles: 1..64 positive {event,bounds} rows, ordered by
(event,u0,v0,u1,v1), inside their named positive coarse cell, disjoint and
covering each cell. Fine tiles: 1..64 positive rows
{event,bounds,coarse_tile}, similarly ordered by their FINE event/bounds.
Each belongs to its positive fine cell and to the named GLOBAL coarse-tile
index; its fine-cell parent must equal that coarse tile's coarse-cell owner.
Fine tiles are disjoint and cover each fine cell and each coarse tile.
No empty source tile is serialized. Event IDs at different levels are local.

With c coarse cells, t coarse tiles, f fine tiles, m=4*t,q=c*c:
old_observations is m by n_old, old_targets q by n_old, 1<=n_old<=64.
canonical EXACT {row_basis,decoder}: 1..64 sorted unique native indices,
first0, last<=m, and q by basis-length coefficients. Index0 is known weight
normalization; indexk>0 is raw observation column k-1. geometric is q by m.
All shapes/caps admitted before exact geometry/integration loops.
New matrices have n_new=9*f columns (up to576), NOT the old 64-column cap.

Native exact dict/list containers and exact keys only; rationals reduced
native integer pairs [n,d], d>0, retained components <=4096 bits. Reject
bool/float/subclasses in numeric positions, unknown/missing fields, ragged
matrices, invalid indices, gaps/overlaps, bad ownership and nonpositive bounds.
Shared valid native containers allowed; outputs detached. Explicit ValueError
guards work normally/-O. Unretained exact intermediates may cancel.
No exhaustive hostile-object/graph/resource or production-hardening claim.

## Supplied geometry, moments and the geometric control

dmu=du*dv/2; strict product order. For clipped coarse region D,
R_D(u,v)=clamp(d_u1-u,0,d_u1-d_u0)*clamp(d_v1-v,0,d_v1-d_v0)/2.
An empty D gives R_D=0. On every coarse tile this must be bilinear.
If either axis tail is identically zero over the tile, allow knots in the
other axis and retain a zero R polynomial. Otherwise reject any D endpoint
strictly inside either tile axis interval. Endpoints on tile boundaries are
allowed. Derive the coefficients in (1,u,v,uv) order from bounds, not G.

Retain M_ij=integral_tile u^i*v^j dmu for 0<=i,j<=3, i outer/j inner,
for EVERY coarse and fine tile. Check all sixteen coarse moments equal
the sums of their complete fine-tile children.
Retain every coarse tile's R_D coefficients for every coarse D.
Construct a geometric matrix independently: target(C,D) uses those
coefficients only in tiles owned by C, zero elsewhere.
Require this ENTIRE matrix equal the inherited geometric policy.

Thus for any integrable incoming F, the coarse response integral_C F*R_D dmu
depends on the four weighted moments on each C-owned coarse tile.
This is a structural geometry argument, not inferred from old G*O_old=Q_old.

Densify the canonical policy without changing it: raw intercept a and matrix L,
with omitted coefficients zero. Geometric has a=0,L=G.
Require a*1^T+L*O_old=Q_old for BOTH maps on every row/column.
An empty C or D requires the old target row zero; a canonical raw row may
nevertheless be nonzero and cancel only on the old model. Preserve that row
and any NEW raw failure, even when normalized comparisons are undefined.

## New nonnegative generators and direct integrations

For each positive fine tile f with its OWN bounds [a,b,c,d], local coordinates
xi=(u-a)/(b-a), eta=(v-c)/(d-c). Let
B_0(x)=(1-x)^2, B_1(x)=2*x*(1-x), B_2(x)=x^2.
Generator phi_fij=V^2*B_i(xi)*B_j(eta) in the INTERIOR of f, zero elsewhere,
including tile boundaries; V is probe volume. Ordering: global fine tile outer,
i=0,1,2 next, j=0,1,2 inner. Local factors are nonnegative on [0,1] and sum1.
Boundary values have measure zero. Integration/quadrature on a support tile
MUST use the one-sided polynomial extension at endpoints, not zeroed indicator
values at quadrature nodes. Source discontinuities do not alter these integrals.

Retain nine GLOBAL monomial coefficients (u^p*v^q, p/q0..2, p outer) per source
on its support tile, not a full coefficient matrix over other tiles.
All nine sources on f sum to V^2*1_f almost everywhere; this SUM is not
a normalized mixture. Each source integral is V^2*h_f/9.
The sum across all sources is constant V^2 almost everywhere in the probe,
and its total integral is V^3, not1. Unknown fields are convex mixtures:
lambda>=0,sumlambda=1. No old V^4/576 chain-sum identity is inherited here.

O_new rows are coarse-tile outer, basis (1,u,v,uv) inner. Source columns
contribute their four exact field moments only to their owning coarse tile.
Q_new rows are every ordered coarse(C,D), C outer/D inner in ID order:
integral_C phi_fij*R_D dmu. Zero outside the support's coarse-cell owner.
Compute TRUE Q_new independently of multiplying inherited G by O_new.

Primary uses explicit global Bernstein coefficient triples, antiderivative
moments and direct phi-times-R contractions.
Reference derives coefficients by independent quadratic interpolation, uses
direct Bernstein values and knot-split tensor Simpson integration for O_new
and Q_new, with direct clamped R values. It may split supports at outgoing
knots even when the coarse bilinearity guard makes them inactive/boundary.
No cross-imports, shared math helper, hidden file reads or stored AQ answers.
A third test oracle uses separable Bernstein beta/antiderivative integration.

Retain constant_observations=V^2*integral_coarse_tile(1,u,v,uv)dmu and
constant_targets=V^2*integral_C R_D dmu, directly from geometry.
Check their entries equal the sums of ALL O_new/Q_new generator columns.
Check all generator integrals and the complete coefficient partition-of-unity.
No normalized mixture is substituted for the unweighted source sum.

## Frozen-policy residuals and complete counterexamples

For each policy, predicted=a*1^T+L*O_new and residuals=predicted-Q_new,
including all zero, positive and negative entries.
exact is true iff EVERY raw residual vanishes. Retain nonzero entry count,
all failed row indices and all failed generator indices in ascending order.
The geometric policy MUST be exact as a structural control. No canonical
outcome, count, first witness or extremal value is prescribed.

For s_CD=V^2*h_C*h_D>0 retain normalized_residuals=residuals/s_CD.
For s=0 keep scale ZERO and normalized residual/bound rows NULL; do not
erase raw predictions/residuals, failed rows or witnesses.

For each defined row, retain the minimum, maximum and maximum absolute
normalized residual over generators and ALL attaining generator indices for
each. These are sharp noiseless convex-mixture mismatch extrema: affine
response errors are convex combinations because sumlambda=1.
They are NOT AP box-error gains, stochastic confidence intervals, universal
field bounds or empirical risks. At a zero row all source indices attain all
three extrema. Nonzero intercepts prevent automatic extension of column
identities to arbitrary UNNORMALIZED linear combinations.

If exact, witness=null. Otherwise choose the FIRST generator with any nonzero
RAW residual, then its FIRST detecting response row. Retain this actual
unit-simplex weight vector e_g and COMPLETE raw observation, true response,
predicted response, signed residual and normalized-residual vectors (with nulls).
Check weights nonnegative/sum1, support/order and every vector entry; do not
replace it with a signed difference, selected scalar or fitted new decoder.

apply receives ONLY dense raw intercept a, raw matrix L and observations x;
returns a+L*x, never geometry/weights/true responses. Shapes1..64 output rows,
observed positive multiple-of-four length<=256; exact pairs, no null raw rows.
It applies an externally supplied affine map, not a provenance verifier.

## Complete family wire and counts

Family EXACT {problem,geometry,generators,matrices,decoders,checks,counts}.
problem detached input copy.
geometry EXACT {volume,coarse_cells,fine_cells,parents,coarse_tiles,fine_tiles,
response_scales}.
cells {event,bounds,volume}; parents [{event,parent}] in fine-cell order.
coarse tiles {event,bounds,moments,outgoing}; outgoing [{event,coefficients}]
for all coarse D in ID order. fine tiles {event,bounds,coarse_tile,moments}.
response_scales in coarse response order.
generators [{tile,i,j,coefficients}], coefficients nine global entries.
matrices EXACT {observation_rows,response_rows,observations,targets,
generator_integrals,constant_observations,constant_targets}.
observation_rows [{tile,basis}], basis0..3; response_rows [{first,second}].
observations and targets are O_new and Q_new.

decoders canonical then geometric, each EXACT
{name,intercept,matrix,predicted,residuals,normalized_residuals,exact,
nonzero_entries,failed_rows,failed_generators,row_bounds,witness}.
row_bounds entries null or EXACT
{minimum,minimum_generators,maximum,maximum_generators,max_abs,max_abs_generators}.
witness null or EXACT {generator,separating_row,weights,observed,truth,predicted,
residual,normalized_residual}.
All matrix/vector entries exact pairs; indices/counts native ints, exact nativebool.

checks EXACT true only after complete verification:
old_response_identities,geometric_policy_authenticated,moment_additivity,
bernstein_partition,generator_integrals,constant_field_observations,
constant_field_responses,geometric_portability,witnesses_valid.
counts EXACT:
coarse_cells,fine_cells,positive_coarse_cells,positive_fine_cells,
coarse_tiles,fine_tiles,old_generators,new_generators,observation_rows,response_rows,
defined_response_rows,undefined_response_rows,coarse_moment_entries,fine_moment_entries,
coarse_outgoing_entries,source_coefficient_entries,observation_entries,target_entries,
generator_integral_entries,constant_observation_entries,constant_target_entries,
raw_decoder_entries,prediction_entries,residual_entries,normalized_residual_entries,
nonzero_residual_entries,failed_rows,failed_generators,row_bound_entries,
bound_attainer_indices,witnesses,witness_entries.
Counts sum BOTH policies where applicable. raw_decoder_entries includes intercepts.
row_bound_entries counts THREE rational extrema per defined row/policy, not indices.
bound_attainer_indices counts all occurrences in the three attainer lists.
witness_entries counts rational entries in weights,observed,truth,predicted,residual,
normalized_residual, excluding nulls/indices: n_new+m+3*q+defined_rows per witness.
Every retained zero/repeated rational occurrence counts. No storage minimality claim.

## Suite, affine checks and evidence lifecycle

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {AP_selected_families:["grid","warp"],
AP_frozen_inputs_equal:true,AO_selected_fine_geometry_equal:true,
AO_selected_coarse_moments_equal:true,AO_selected_fine_moments_equal:true,
old_maps_consumed:true,old_response_identities_rechecked:true,
other_historical_mathematics_replayed:false,older_executors_run:false}.
Input identity is admitted before builds and rechecked AFTER new builds;
selected AO moments are checked only AFTER new builds. No old moment or
outgoing answer enters engine inputs.
payload_sizes entries {family,input_bytes,geometry_bytes,generator_bytes,
measurement_bytes,target_bytes,decoder_bytes,native_family_bytes}.
Measurement scope is canonical {rows:observation_rows,matrix:observations};
target scope is {rows:response_rows,matrix:targets}; others named projections.
Newline included, overlapping scopes not additive unique storage or online packets.
totals sums counts and adds families=2.
scope ALL false: decoder_refitted,old_convex_hull_inclusion_proved,
full_field_recovery_extended,physical_sources_established,empirical_noise_calibrated,
arbitrary_field_error_bound_proved,unknown_geometry_reconstructed,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,fixed_affine_families_run.

Generic positive affine axes: u'=alpha*u+du,v'=beta*v+dv,k=alpha*beta.
Transport both geometries, old/raw new moments by P=k^3*(global monomial change),
targets/predictions/raw residuals by k^4; SAME maps a'=k^4*a,L'=k^4*L*P^-1.
Reencode dense canonical basis0..m only on generic cases where m+1<=64.
Source coefficients pull back with amplitude factor k^2; moments with Jacobian
and binomial factors, outgoing coefficients with factor k and basis pullback.
New local Bernstein labels stay fixed; normalized residuals, all extrema,
attainer sets and witness indices remain invariant. Check complete data, not ranks.
No new canonical solve. No fixed affine/partial family.

Generic controls: all nine unit Bernstein anchors; nonzero intercept; an old-exact
alternate with both signed residual directions; same-map portable control;
null response scales with retained raw failures; inactive-axis outgoing-knot
exception versus active knot rejection; unequal/signed/multitile partitions;
boundary quadrature one-sided values; complete affine and source-sum identities;
restricted apply/detachment; malformed guards normal/-O; full-wire mutations;
selected-input/old-moment provenance; capture caps/source changes/create-only/read-only.

Pin AP:361276 bytes SHA256
823d9f5a5511853fe3dbff800f1a6561db985021002c24ec2beb0c55199ba048.
Pin AO:451698 bytes SHA256
55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1.
AP plus46 prior captures gives47 captures; its5 sources plus49 ancestors gives54
ancestor sources; five AQ sources give106 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05aq.py after generic checks
and independent source reviews, BEFORE root releases fixed calculations.
Disclose every post-first source/protocol/fixture/mathematical correction.
One first comparison, EXACTLY ONE independent normal reference-only read-only
audit, full normal/-O tests, external create-only preflight, exclusive final
capture, fresh primary-normal/reference--O final replays. Bracket all106 identities
and final bytes. Isolated Python, external caches, no dependencies/old executors.
Capture cap128MiB, working cap192MiB, not exhaustive resource hardening.
RESULTS.md/roadmap outside ledger; publish only this directory and bridge roadmap.
