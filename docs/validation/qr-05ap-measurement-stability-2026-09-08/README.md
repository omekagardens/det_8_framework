# QR-05AP protocol: bounded measurement-error stability

8 September 2026. Prospective before fixed AP calculations.
Base: pushed AO commit a3286f68dd35be7d60b9abad6fc914dbbbd5af8f.
Do not edit prior research, RET/core work, dependencies or temporary sheets.

## Question and scope

Compare measurement-error amplification in TWO FROZEN AO coarse-response
decoders: canonical (omitted measurement coefficients padded with zero) and
direct geometric. Both agree on noiseless model measurements. This does not
fix their action on inconsistent measurements outside the model span.
No new fit, rank selection, decoder optimization, field integration or
source-span expansion. AO's full-field recovery remains established on its
declared dictionaries; this gate tests only coarse-response stability.

Use grid then warp, whole probe, l1->l2, all 49 coarse response rows and
32 raw weighted observations per family. Consume AO's AUTHENTICATED geometry,
weighted observation matrix, coarse target matrix and two decoders as inputs.
This is an explicitly inherited-map calculation, not independent rederivation
of AO fields, responses, ranks or certificate canonicality. No historical
executor is imported or run. Other AO data remain identity-only.
No fixed AP gain, normalized decoder or witness calculation before freeze.

Unknown incoming fields remain AO's convex mixtures with exact weight sum one.
The error box below is hypothetical observation corruption, not calibrated
noise, a probability distribution, physical sensor performance, or necessarily
a valid field perturbation. Corrupted moments may be inconsistent; decoded
responses may be negative or outside model ranges. No clipping/projection.

## Generic input and validation

Each independent engine exposes build_family(problem) and apply(intercept,matrix,z).
Problem EXACT:
{family,probe,cells,tiles,observations,targets,canonical,geometric}.
probe is a positive rectangle [u0,u1,v0,v1].
cells is 1..8 rows {event,bounds}, bounds positive rectangle or null.
IDs are sorted unique signed native integers. Nonempty cells lie in probe,
have disjoint interiors and cover probe. Empty cells retain their IDs.
tiles is 1..64 positive rows {event,bounds}, ordered by
(event,u0,v0,u1,v1), contained in their named nonempty cell; disjoint interiors,
and completely cover each cell. dmu=du*dv/2. No fine geometry is input.

With t tiles, m=4*t, c cells, q=c*c, n=1..64 generator columns:
observations is m by n; targets is q by n in first-cell outer/second-cell
inner order. canonical EXACT {row_basis,decoder}; basis is 1..64 sorted
unique native indices, first 0, all <=m; decoder is q by len(basis).
geometric is q by m. All list/matrix sizes checked before arithmetic loops.
No generic claim that supplied basis is independent/canonical: AO provenance
fixes that policy; generic admission checks its full response identity.

All containers must be exact native dict/list types with exact keys; family
a nonempty native string. Rational scalars are native reduced [n,d], d>0,
both exact native ints, each retained component <=4096 bits. Reject bools,
floats, subclasses, unknown/missing fields, ragged matrices, nonpositive
rectangles, overlap/gaps, unknown tile owners, malformed basis and dimensions.
Inputs may share valid native containers; outputs detached. Explicit ValueError
guards work normally and under -O. Internal exact intermediates may cancel
before retention. No exhaustive hostile-object/graph or resource guarantee.

Dense canonical raw intercept a and matrix L are reconstructed from the
compact basis: index0 feeds a, index k>0 feeds L[:,k-1]; all omitted entries
are zero. Geometric a=0 and L=geometric. Require for BOTH policies
a*1^T+L*observations=targets on EVERY row/column.
An empty cell in either target label requires the full target row zero;
a nonzero raw decoder row cancelling on the model is still admissible.

## Dimensionless measurement coordinates and frozen-map transport

V is probe volume; h_t is tile volume. For every tile t with its OWN bounds
[u0,u1,v0,v1] (not the probe bounds), define
xi=(u-u0)/du, eta=(v-v0)/dv, du=u1-u0>0,dv=v1-v0>0.
z_t,j=integral_t F*(1,xi,eta,xi*eta)_j/(V^2*h_t).
The four local coordinates are dimensionless; zero-volume tiles do not exist.

Let x_t be the raw AO field moments in basis (1,u,v,uv). x_t=T_t*z_t,
where T_t=V^2*h_t times the four by four matrix with rows
(1,0,0,0),
(u0,du,0,0),
(v0,0,dv,0),
(u0*v0,du*v0,u0*dv,du*dv).
Retain T_t and its inverse K_t; verify both products equal identity.
Retain the complete dimensionless observation map Z, blockwise K_t*O_t.

For target (C,D), s_CD=V^2*h_C*h_D. For s>0, y=U_CD/s.
For s=0 retain normalization zero but normalized target/decoder/gain/witness
rows null, not fabricated zero observations or a defined normalized response.

Transport the SAME frozen raw decoder:
b_j=a_j/s_j, B_j,t=L_j,t*T_t/s_j.
Then y_hat=b+B*z and normalized target Y=Q/s satisfies b*1^T+B*Z=Y.
Keep known mixture normalization EXACT: no error on b, no extra noisy coordinate.
The public apply takes ONLY b,B,z and returns b+B*z, preserving null rows;
no mixture weights, geometry, observation/target dictionaries enter this call.
It applies a supplied map, not an authentication of external map semantics.
apply admits 1..64 paired output rows, z length a positive multiple of four
<=256, exact scalars; b and B rows either both null or nonnull with width len(z).

Under u'=alpha*u+shift_u,v'=beta*v+shift_v, alpha,beta>0,k=alpha*beta,
transport raw moment blocks by P=k^3 times the global monomial basis change.
Geometry volumes scale k, targets k^4, raw intercept a'=k^4*a,
raw linear blocks L'=k^4*L*P^-1. Re-encode a transported dense canonical map
using all indices 0..m only in generic cases with m+1<=64.
Do NOT recertify canonical coefficients after transport.
The dimensionless Z,Y,b,B,gains and witnesses must remain identical.
Also check transformed geometry and T/K blocks, not only scalar maxima.

## Sharp error certificate and comparisons

For the declared box |delta_z_i|<=epsilon, epsilon>=0,
delta_y=B*delta_z. Each defined row's sharp absolute bound is
epsilon*g_j, g_j=sum_i abs(B_ji).
No stochastic independence is asserted by a deterministic Cartesian box.
For epsilon=1 choose w_ji=sign(B_ji), with sign(0)=0.
Retain ALL signs and complete output vector B*w_j (null on undefined targets),
and attained=(B*w_j)_j=g_j. Its negative attains the symmetric lower endpoint.
Every witness obeys the unit box. Zero-gain rows retain the all-zero witness.
Witness output means ERROR only, not b+B*w and not a physically valid field.
Other coordinates may attain different signed changes.
Individual row witnesses need not attain every row bound simultaneously.
A finite gain is not operational robustness without an error budget and
response tolerance, nor a uniform bound over shrinking geometric cells.

For each decoder retain the maximum over every defined row and ALL maximizing
row indices, including every defined row when the maximum is zero.
Per-row sign witnesses are canonical witnesses, not an enumeration of the
entire maximizing face of the box. Null rows are excluded from comparisons.
Retain canonical-minus-geometric signed row gain differences and all row lists:
canonical_lower_rows,geometric_lower_rows,tied_rows,undefined_rows.
No expected ordering, strict improvement, fixed gain or tie count is prescribed.
A smaller worst-case gain need not give smaller error for every error vector.

## Complete wire

Family EXACT {problem,geometry,coordinates,decoders,comparison,checks,counts}.
problem is a detached exact input copy.
geometry EXACT {volume,cell_volumes,tile_volumes,response_rows,response_scales};
response_rows [{first,second}] in cell order, other lists implicit same order.
coordinates EXACT {raw_from_local,local_from_raw,observations,targets};
first two are t four-by-four blocks; latter are Z and Y (null undefined rows).

decoders is canonical then geometric, each EXACT
{name,raw_intercept,raw_matrix,intercept,matrix,row_gains,witnesses,max_gain,max_rows}.
witnesses has q entries, each null or {signs,output,attained}.
Signs native ints -1/0/1, output a length-q rational/null vector.
comparison EXACT {gain_difference,canonical_lower_rows,geometric_lower_rows,
tied_rows,undefined_rows}; every row occurs in exactly one list.
checks EXACT all true only after complete validation:
raw_response_identity,coordinate_inverse,normalized_response_identity,
witness_box,witness_attainment,complete_gain_partition.
counts EXACT:
cells,positive_cells,tiles,generators,observations,responses,defined_responses,
undefined_responses,transform_entries,dimensionless_observation_entries,
dimensionless_target_entries,raw_decoder_entries,normalized_decoder_entries,
gain_entries,witnesses,witness_sign_entries,witness_output_entries,
maximizing_rows,canonical_lower_rows,geometric_lower_rows,tied_rows.
Raw/normalized decoder entries include intercepts; defined rational entries only
for null-bearing matrices/vectors. Gains count both policies. Witness output
entries count rational scalars including zero, not nulls. Transform entries
count T AND K. Indices/signs excluded except separately named count fields.
Repeated serialized occurrences are not independent information.

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
prior_bridges EXACT {AO_selected_families:["grid","warp"],
AO_selected_inputs_equal:true,AO_frozen_decoders_consumed:true,
AO_selected_response_identities_rechecked:true,AO_other_mathematics_replayed:false,
older_executors_run:false}.
payload_sizes per family EXACT {family,input_bytes,geometry_bytes,
coordinate_bytes,decoder_bytes,comparison_bytes,native_family_bytes}.
Each is canonical corresponding projection, newline included; overlapping
scopes are NOT additive unique storage or an online packet.
totals sums all counts and adds families=2.
scope ALL false: empirical_noise_calibrated,field_realizable_errors_required,
decoder_optimized,canonical_policy_refitted,source_span_expanded,
fine_response_stability_tested,full_field_stability_tested,
unknown_geometry_reconstructed,physical_sensor_validated,quantum_channel_constructed,
gravity_derived,ret_integration_tested,lean_verification_performed,
generic_production_API_hardened,fixed_affine_families_run.

## Independent methods, controls and lifecycle

Primary uses explicit triangular local/raw blocks and direct row L1 sums.
Reference builds raw-from-local by evaluating the bilinear basis at local
corners and converting corner values to coefficients, inverts by independent
exact elimination, and evaluates the SAME raw affine map at zero and each
local unit vector to obtain b and every B column by output differences.
Reference sharp bounds use sums of independent coordinate interval endpoints,
with full witness products independently checked. No shared math helpers,
cross-imports, hidden files, historical executors or stored AP answers.
A separate test oracle checks complete wires and exact small corner extrema.

Generic controls: translated unequal tile widths/areas, multiple/empty cells,
zero and nonzero intercepts, positive/negative/zero coefficients, all-zero
targets/gains with all ties, genuine different off-span maps with equal
noiseless targets, normalized-versus-raw noise, epsilon scaling, no clipping,
complete affine transport of the SAME map, restricted online application,
detachment, malformed native guards normally/-O, complete non-noop wire
mutations, source mutation, capture size/exclusive/read-only/symlink behavior.

Pin AO: 451,698 bytes SHA256
55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1.
AO plus 45 prior captures gives 46 captures; AO's five sources plus 44 ancestors
gives 49 ancestor sources. Five AP sources give 100 distinct authenticated targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05ap.py after generic
checks and source reviews BEFORE fixed AP mathematics; root explicitly releases.
Disclose all subsequent source/protocol/fixture/mathematical corrections.

Isolated Python and fresh external caches. First comparison, exactly one
independent normal reference-only read-only audit, full normal/-O tests,
external create-only preflight, exclusive final capture, fresh primary-normal
and reference under -O read-only final replays. Bracket all 100 identities and final
bytes. No prior artifact overwrite. Capture cap 128 MiB, working cap 192 MiB;
not exhaustive resource hardening. RESULTS.md and roadmap stay outside ledger.
Publish only this gate directory and the Track-B bridge roadmap.
