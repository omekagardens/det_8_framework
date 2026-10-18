# QR-05AO protocol: response-preserving coarse field measurements

8 September 2026. Prospective before fixed AO mathematics.
Base: pushed AN commit 8ed22a74c2dd6a576f862daf6e07e584d3c9567b.
Keep prior research, RET/core changes, dependencies and temporary sheets untouched.

## Question, information restriction and fixed scope

Which coarse observations of an unknown nonnegative field preserve declared
coarse responses, fine responses, or the full piecewise field? These are
different targets. This PRIVATE exact rational diagnostic is not an empirical
sensor, physical mixture preparation, quantum state/channel, unknown-geometry
reconstruction, universal compression/minimality, production API or gravity claim.

Use supplied geometry. Fine generator g=(a,b) denotes the same F_ab as AN.
A field is F_lambda=sum_g lambda_g F_g with lambda_g>=0 and sum lambda_g=1.
Normalization concerns generator weights, NOT unit field integral or quantum
normalization. Individual generators can vanish or be linearly dependent.
Full-field recovery is not recovery of individual mixture weights.

The online decoder receives only raw measurements, known normalization and
a certified fixed decoder/basis-index list. It must not read lambda, the
generating process, a full fine field or a target evaluated from it.
Offline verification retains geometry, all generator coefficients, matrices
and witnesses. Consequently loss for this restricted online interface is NOT
loss of the complete retained research artifact. Supplied coordinate changes
are reversible; discarding hidden field information may not be.

Authenticate AN and project ONLY its input problem grid/warp in that order,
whole probe, l1 as coarse and l2 as fine, with seven/eight cells. Keep all
original IDs and coordinates. There are 64 ordered generator columns,
49 coarse response rows and 64 fine response rows per family. No fixed
transformed/stale/partial family is added. No fixed AO rank, success, failure,
mixture collision, field synthesis or matrix calculation before source freeze.

Problem exactly:
{family,probe:{name,bounds},coarse:{level,cells},fine:{level,cells}},
cells [{event,bounds}]. Generic: nonempty native strings, distinct level labels;
1..8 positive full cells per level, sorted unique signed native integer IDs;
positive probe. Full same-level interiors disjoint, clipped cells cover probe.
Find each fine cell's unique FULL coarse parent before clipping, require
children cover each full coarse parent. Empty clips are allowed and keep IDs.
Bounds are native four-entry lists of reduced rational [n,d] pairs, d>0.
Reject booleans in numeric positions, floats, foreign/subclass types and
unknown/missing fields. Every retained integer component has <=4096 bits.
Valid shared native containers are admitted; outputs must be detached.
Unretained exact elimination intermediates may cancel before retention.
No exhaustive hostile-object/graph/resource-hardening claim.

## Geometry and independent integration

dmu=du dv/2, strict product order. Clip all regions ONLY to common probe Q.
L_a(y) is predecessor volume; R_d(z) is successor volume.
F_ab(z)=integral_b L_a(y)1[y precedes z]dmu(y).
For each axis with intervals a=[a0,a1],b=[b0,b1],
H_a(t)=((t-a0)_+^2-(t-a1)_+^2)/2,
f_ab(t)=H_a(clamp(t,b0,b1))-H_a(b0).
F_ab(u,v)=f_ab(u)f_ab(v)/4. Empty a/b gives zero. Do not clip a/b to C.
An empty outgoing region gives zero R.

Independently construct each level's shared breakpoint grid: on each nonempty
clipped C, insert every clipped-cell boundary strictly inside its axis extent,
deduplicate/sort; order C by ID, u intervals outer/v inner. Every positive
Cartesian tile remains, including inactive cuts. Empty C has no tiles.
Use GLOBAL flat tile indices in this gate, not AN's C-local tile indices.
Every fine tile lies inside one coarse tile, with the appropriate full parent.
Verify that containment and coarse outgoing bilinearity on each fine tile.

M_ij=integral_tile u^i v^j dmu for i,j=0..3, i outer/j inner (sixteen entries).
Fine F coefficients use i,j=0..2, i outer/j inner (nine entries).
Outgoing and weighted-observation basis is (1,u,v,uv), exponents
(0,0),(1,0),(0,1),(1,1), in that order.

Primary derives branch polynomials, antiderivative moments and exact coefficient
contractions. Reference independently evaluates F using ordered-interval atom
pair volumes, derives its nine coefficients by tensor quadratic interpolation,
and integrates F times weighted monomials or outgoing functions by exact
tensor-Simpson quadrature (degree <=3 each axis). It verifies causal responses
against direct ordered four-point atom/simplex integrals, including repeated
regions. Reference geometry moments use Simpson, not primary formulas.
Modules must not import each other or old executors, read stored answers,
read hidden files or use a shared mathematical helper module.

## Observation, response and synthesis maps

Generator columns in ascending fine first-ID outer/second-ID inner order.
Coarse tiles are flattened as above. O_integral has one row per coarse tile:
integral_tile F_g. Known tile volumes make this equivalent to a tile mean.
O_weighted has four rows per coarse tile, basis order:
integral_tile F_g*(1,u,v,uv). These are FIELD moments, not geometry moments M.
Fine_weighted has the analogous four rows per fine tile, for verification only.
Derive coarse observations by SUMMING exact fine-piece integrals into their
unique coarse tile. Never corner-fit F on a coarse tile.

Q_coarse has every ordered coarse (C,D) row:
integral_C F_g R_D dmu, C outer/D inner.
Q_fine analogously has every ordered fine (c,d) row.
Q_field=S stacks all nine fine field coefficients, tile outer/exponent inner.
Equality under S means equal polynomial fields on all positive tiles
(and hence almost everywhere on Q), not unique generator coefficients.

Retain a direct geometric decoder G for Q_coarse from O_weighted:
row (C,D), tile t/basis j gets R_D's coefficient j if t belongs to C,
otherwise zero. Require Q_coarse=G O_weighted. No normalization term needed
for this particular constructive decoder.

Require O_weighted[4t]=O_integral[t]; all four coarse field moments equal
the complete fine-weighted sums over tile children; Q_coarse equals complete
child-(c,d) sums of Q_fine per generator. Require complete unweighted sums
over ALL generators AND response rows equal V^4/576 for coarse and fine maps.
That last identity uses generator weight one, not a normalized convex mixture.
All zero rows/columns, signed field coefficients/moments and reverse/repeated
region labels remain.

## Exact canonical certificates

Each independent module exposes build_family(problem), certify(O,Q), and
decode(row_basis,decoder,observed). All public numeric data are native reduced
rational pairs; certificate/index fields use native integers/booleans.
certify accepts O with 0..32768 rows and Q with 1..32768 rows; same 1..64
columns, native list rows. Empty O obtains its column dimension from Q.
Matrix size admission occurs before elimination. Retained components obey
4096 bits; this is not a polynomial-time or universal resource guarantee.

Augment O with a FIRST row of ones: A=[1^T;O].
Recovery criterion: ker(A) subset ker(Q), equivalently
rank([A;Q])=rank(A). This condition on the whole linear space is also necessary
for responses of ALL convex mixtures: a nonzero kernel difference has zero
coefficient sum and splits into two normalized nonnegative mixtures.

Canonical certificate EXACT keys:
{observation_rank,target_rank,joint_rank,row_basis,pivot_columns,
recoverable,decoder,collision}.
target_rank is rank(Q), not augmented Q. row_basis is the lexicographically
earliest independent ROW indices of A, found greedily in original order.
It includes normalization index 0. pivot_columns are the ascending pivot
columns of the UNIQUE reduced row echelon form of A.

If recoverable: collision=null. decoder has one row per Q row and one column
per row_basis entry: unique coefficients expressing that target in the chosen
original independent A rows. Require D*A[row_basis,:]=Q on ALL columns.
This compact decoder is canonical; omitted observation coefficients are zero.

If not recoverable: decoder=null. For each free generator column j in ascending
order, form the standard RREF null vector w_j: free entry j=1, other free
entries zero, pivot entries minus RREF[pivot_row,j].
Choose the FIRST free j for which the COMPLETE vector Q*w_j is nonzero,
then the first target row detecting this chosen vector. This ordering is
free-column-first, not failed-target-row-first. Do not rescale or flip w.
Let m=sum positive(w)=-sum negative(w)>0,
lambda_plus=positive(w)/m, lambda_minus=negative_part_magnitude(w)/m.
Retain collision EXACT keys:
{free_column,difference,positive_weights,negative_weights,
observed_positive,observed_negative,target_positive,target_negative,
target_difference,separating_row}.
difference is the unnormalized standard w. Observed vectors are RAW O*lambda,
without the normalization row. Target vectors are Q*lambda.
target_difference is Q*(lambda_plus-lambda_minus), NOT the unnormalized Q*w.
Check every weight nonnegative, each sum=1, complete observation equality,
all target differences, and the first nonzero separating row.

Different elimination methods must agree on this mathematical canonical wire.
Primary may use Gauss-Jordan and basis solves; reference must independently
implement elimination/solves (e.g. column-basis reduction/forward elimination
and back substitution), not copy primary solver code.

decode receives ONLY row_basis, compact decoder and the raw observed vector.
Prepend normalization one internally. Require sorted unique native indices,
first index 0, within this augmented vector; len basis 1..64; nonempty decoder
with <=32768 rows and matching width; observed length <=32768. Validate all
native rational components and return the exact target vector.
It applies a supplied certificate's linear map; it does not authenticate an
arbitrary externally supplied decoder's semantics or recoverability.
No weights/full fields/geometry/target matrix enter this online function.

## Complete family wire

Family EXACT {problem,geometry,matrices,certificates,checks,counts}.
geometry EXACT {volume,parents,coarse_cells,fine_cells,coarse_tiles,fine_tiles}.
parents [{parent,children}], full IDs in sorted order.
Clipped cell rows {event,bounds,volume}; empty bounds=null and volume zero.
Coarse tile rows {event,bounds,moments,outgoing};
fine tile rows {event,bounds,coarse_tile,moments,outgoing}.
outgoing contains EVERY SAME-LEVEL D in ID order:
{event,coefficients}, four entries including zeros.
Fine tile's coarse_tile is a global integer index.

matrices EXACT {generators,observations,targets,fine_weighted,coarse_decoder}.
generators [{first,second}].
observations [{name,rows,matrix}], names integral,weighted in that order.
Observation row labels {tile,basis}, basis integer 0 only for integral,
0..3 for weighted. targets same {name,rows,matrix}, names coarse,fine,field.
Coarse/fine row labels {first,second}; field labels {tile,power:[i,j]}.
fine_weighted is a matrix in implicit fine-tile/basis order.
coarse_decoder is the direct geometric G matrix, without normalization column.

certificates [{observation,target,certificate}], observation outer
integral/weighted, target inner coarse/fine/field, exactly six entries.
Require weighted/coarse recovery and that adding O_weighted to O_integral
cannot turn a recoverable target into an unrecoverable one.
No other pass/fail outcome or exact rank is required prospectively.

checks EXACT booleans, all true only after checking:
weighted_contains_integral,coarse_decoder_exact,coarse_refinement_exact,
response_partition_exact,measurement_refinement_exact.

counts EXACT:
coarse_cells,fine_cells,positive_coarse_cells,positive_fine_cells,generators,
coarse_tiles,fine_tiles,input_bound_entries,clipped_bound_entries,tile_bound_entries,
coarse_moment_entries,fine_moment_entries,coarse_outgoing_vectors,
coarse_outgoing_entries,fine_outgoing_vectors,fine_outgoing_entries,
observation_rows,observation_entries,fine_weighted_rows,fine_weighted_entries,
coarse_response_rows,fine_response_rows,field_rows,target_entries,
geometric_decoder_entries,certificates,recoverable,failed,
row_basis_entries,pivot_column_entries,canonical_decoder_entries,collision_entries.
All entries count serialized occurrences, including zeros/repeats.
Input bounds include the probe plus every full coarse/fine cell.
Moment counts are sixteen per corresponding tile; outgoing entries four/vector.
observation counts sum both maps; target entries sum all three target matrices.
For each failed cert, collision_entries counts every rational scalar in its
three generator vectors, two observation vectors and three target vectors:
3*n+2*O_rows+3*Q_rows. Integers naming indices are excluded.
No rank sum, source dimension, row count or decoder storage is called universal
or minimal observation information.

## Suite, historical projection and affine checks

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Two families grid/warp. totals sums ALL count fields plus families=2.
prior_bridges EXACT:
{AN_selected_families:["grid","warp"],AN_selected_input_geometry_equal:true,
AN_selected_fine_coefficients_equal:true,AN_selected_fine_quadruples_equal:true,
AN_answers_consumed_by_engines:false,AN_other_mathematics_replayed:false,
older_executors_run:false}.
After new builds, compare the fine synthesis rows against AN's selected l2
whole-probe fine tile propagated coefficients and Q_fine against ALL selected
AN l2 quadruple answers (8,192 scalar comparisons across the two families).
Verify bounds/order/IDs when flattening AN's C-local tiles. These are selected
answer RECHECKS using new geometry-only engines, not answer inputs or execution
of historical source. Other prior mathematics remains identity-only.

payload_sizes per family EXACT:
{family,geometry_bytes,measurement_map_bytes,target_map_bytes,
geometric_decoder_bytes,certificate_bytes,native_family_bytes}.
Geometry is canonical geometry; measurement map is canonical
{generators,observations}; target map is canonical targets; geometric decoder
is canonical G; certificates the complete canonical list; native family is
complete family. Scopes overlap/omit separate diagnostics, not additive unique
storage costs or a compressed online packet. Account separately for fixed
decoder/model/geometry versus each unknown mixture's measurement vector.

Generic coordinate checks use u'=alpha*u+du,v'=beta*v+dv, alpha,beta>0,k=alpha*beta.
All geometry/bounds transport, raw geometric moments binomially with factor k;
F coefficients pull back with k^2, outgoing coefficients with k.
O_integral scales k^3. Every weighted block transforms by k^3 times
(1,u',v',u'v')=(1,alpha*u+du,beta*v+dv,
k*u*v+alpha*dv*u+beta*du*v+du*dv).
Q_coarse/Q_fine scale k^4; S transports by the nine-entry coefficient pullback.
Normalization remains one. Compare COMPLETE transformed geometry/matrices,
not just scalar ranks. Verify certificate validity/response transport.
Do not require a naively transported canonical decoder to match newly chosen
canonical coefficients. Independently recertify transformed targets or check
transported dense decoders. Ranks/recovery and actual collision validity are
coordinate-invariant under these invertible changes.

Scope flags ALL false:
generic_production_API_hardened,unknown_geometry_reconstructed,
minimal_encoding_proved,universal_compression_proved,mixture_weights_recovered,
physical_mixture_preparation_established,empirical_measurements_used,
noisy_measurement_robustness_tested,quantum_channel_constructed,gravity_derived,
continuum_limit_established,ret_integration_tested,lean_verification_performed,
fixed_affine_families_run,full_retained_artifact_information_lost.

## Verification and publication

Pin AN: 8,378,531 bytes SHA256
a455f43f65dea9da33692cd256fad942e2d21d0bfed9f54a0deed163ff5bd9c1.
AN plus 44 prior artifacts gives 45 captures; AN's five sources plus 39 ancestors
gives 44 ancestor sources. Add five AO sources for 94 distinct targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05ao.py after generic
verification and independent source reviews, BEFORE fixed AO computation.
Root explicitly releases fixed builds. Disclose every source/protocol/fixture/
mathematical correction after the first fixed build.

Generic controls: normalization-only and normalization-enabled recovery;
rank-deficient/duplicate/zero generators; exact tiny rank differences;
full-field versus mixture-weight identifiability; concrete nonnegative field
collisions; weighted information cannot reduce recoverability; full decoder
identities and all collision fields; coarse/fine response additivity; signed
IDs/coordinates, unequal refinement and empty clips; complete affine matrices;
native malformed guards in normal/-O; detachment; restricted online decode;
non-noop full-wire/certificate/projection corruptions and evidence lifecycle.

Isolated Python, fresh external bytecode caches, no dependency changes or
old executors. First comparison; exactly one independent reference-only
read-only audit; full normal/-O tests; external create-only preflight;
exclusive final capture; fresh read-only primary normal/reference -O replays.
All must agree, with all 94 identities and final bytes bracketed.
Capture cap 128 MiB, canonical working cap 192 MiB, not exhaustive resource hardening.
Never overwrite evidence or follow a final symlink.
RESULTS.md/roadmap stay outside frozen ledger. Publish only this gate directory
and docs/track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md.
