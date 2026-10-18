# QR-05AR protocol: fine-response measurement sufficiency

8 September 2026. Prospective before fixed AR calculations.
Base: pushed AQ commit 8e1bac5f1e0e6d7c01f9d08708e56db8c0ad8ed8.
Keep unrelated RET/core/governance work, dependencies and temporary sheets intact.

## Question and fixed scope

Keep AQ's source dictionary and supplied clipped geometry. Can its four
incoming-field moments per COARSE tile determine all FINE-region responses?
A failed inherited decoder does not settle this. Test actual sufficiency on
the normalized source simplex, retaining either a full exact decoder or two
nonnegative mixtures with identical observations and different responses.
Per-row recovery flags/decoders distinguish questions preserved from questions lost.
No fixed rank, recoverability outcome, collision or repair-tile count is prescribed.

Use grid then warp, whole probe, l1 coarse/l2 fine, the same seven/eight
cells and eight/twelve original tiles. The 108 Bernstein generators per family,
their amplitudes, original supports and ordering are UNCHANGED from AQ.
No old source enlargement, full-field reconstruction, measurement-error study,
source preparation, empirical interface, unknown geometry or gravity result.

The repair is explicitly NEW incoming-field measurements: four moments on
a deterministic refinement of the fine tiles. Supplied geometry can specify
where to measure but cannot provide the unknown field's missing moments.
The conservative refinement below is not claimed minimal. It must not restart
the source polynomials or change their mixture normalization.

## Native input and bounded admission

Public engines expose build_family(problem), certify(observations,targets)
and apply(intercept,matrix,observed). Problem EXACT:
{family,probe,coarse_cells,fine_cells,coarse_tiles,fine_tiles}.
No stored moments, coefficients, matrices, old decoder or AQ outcome is an input.
family nonempty native str; probe positive [u0,u1,v0,v1] rectangle.
Each cell level has1..8 rows {event,bounds}, sorted unique native signed int IDs.
bounds is positive rectangle or null. All positive cells are already clipped
inside probe; each level has disjoint interiors and covers probe.
Every positive fine cell has exactly one containing positive coarse parent,
and its siblings cover that parent. Empty fine cells have parent null.
Unclipped parenthood remains inherited provenance, not a new generic assertion.

Coarse tiles1..64: positive {event,bounds}, sorted (event,u0,v0,u1,v1),
contained in named positive coarse cell, disjoint and covering each cell.
Fine tiles1..64: positive {event,bounds,coarse_tile}, same order using FINE ID.
coarse_tile is the global coarse-tile index. The tile lies inside its named
fine cell and indexed coarse tile, whose owner equals its fine-cell parent.
Fine tiles cover every fine cell and every coarse tile. IDs are level-local.
No zero-volume tile is serialized.

Native exact dict/list with exact keys; rationals reduced native integer
pairs[n,d], d>0; retained integer/rational components <=4096bits.
Reject bool/float/numeric or container subclasses, ragged/malformed data,
out-of-range IDs/indices, overlap/gap/nonpositive bounds and extra/missing keys
with explicit ValueError in normal/-O execution. Shared valid native containers
are admitted; returned native wires are detached. Exact unretained
intermediates may cancel. No exhaustive hostile-object/graph/resource claim.

All container inventories and shapes are admitted before geometry/elimination.
The additional repair-piece count is admitted before moments, integrations,
matrix allocations or elimination. Caps are computational scope, not a
geometric impossibility theorem: at most256 repair pieces, 576 source columns,
256 coarse measurement rows,1024 repair measurement rows and64 target rows.
No new dependency or historical engine import/execution.

## Deterministic geometry refinement and unchanged sources

dmu=du*dv/2, V=probe volume. For every original fine tile, collect its endpoints
and every endpoint of each POSITIVE fine cell lying strictly inside its u or v
interval. Form ALL positive Cartesian subrectangles. This unconditional
endpoint overlay may split inactive knots; do not remove such pieces.
Order: original fine-tile index outer, then(u0,v0,u1,v1). For each repair piece
retain its original fine_tile index, fine event owner and coarse_tile index.
There must be at least one piece per original fine tile; sum counts before
constructing moments or matrices and reject a total above256.

Retain16 geometric moments M_ij=integral u^i*v^j dmu,0<=i,j<=3,i outer,
on every coarse, original fine and repair tile. Check every original fine
moment is the sum of its repair pieces, and every coarse moment the sum of
its original fine children and of its repair descendants.

For clipped cell D:
R_D(u,v)=clamp(d_u1-u,0,d_u1-d_u0)*clamp(d_v1-v,0,d_v1-d_v0)/2;
R_empty=0. Retain its bilinear coefficients in (1,u,v,uv) order for every
coarse D on each coarse tile, and every fine D on each repair piece.
If either tail is identically zero on a tile, return all-zero coefficients
even if the other axis has a knot inside. Otherwise an interior endpoint is
an admission failure; endpoints on tile boundaries are allowed.
Fine-destination knots inside a COARSE observation tile are allowed and are
part of this investigation, not grounds for rejection.

Each original fine tile f with bounds[a,b,c,d] carries nine sources
phi_fij=V^2*B_i((u-a)/(b-a))*B_j((v-c)/(d-c)) in its INTERIOR, zero elsewhere
including boundaries. B0=(1-x)^2,B1=2x(1-x),B2=x^2.
Order fine_tile outer,i0..2,j0..2; retain nine GLOBAL coefficients in
u^p*v^q order,p/q0..2,p outer. All repair integrations use THESE original
coordinates and coefficients, not new Bernstein sources on the pieces.
Use one-sided polynomial extension at quadrature endpoints, not zeroed
indicator values. Sources are nonnegative; their per-tile sum is V^2 a.e.
Each source integral is V^2*h_f/9 and total dictionary integral is V^3.
Unknown weights lambda>=0,sumlambda=1; the unweighted source sum is NOT a mixture.

## Independent measurements, targets and repair

Retain three observation matrices O_coarse,O_fine,O_repair, with tile outer,
basis(1,u,v,uv) inner, source columns in unchanged order. Each entry is a
direct exact integral of the original source times that global monomial on
the named tile. A source contributes only to its original fine tile, its
coarse ancestor and its own repair pieces. Check all rowwise sums over
repair pieces -> original fine -> coarse, and direct repair -> coarse.

Retain Q_coarse and Q_fine for every ordered pair(C,D) at the respective
level, C outer/D inner in sorted ID order:
integral_C phi_g R_D dmu. Empty C/D gives zero, all rows retained.
True targets MUST be integrated independently of geometric-map multiplication.
Check coarse Q equals sums of fine Q over both parent labels, every source
column included. This is response additivity, not a product/composition rule.

Construct G_coarse from derived outgoing coefficients on C-owned coarse
tiles, and G_repair analogously on C-owned repair pieces for fine targets.
Check complete G_coarse*O_coarse=Q_coarse and G_repair*O_repair=Q_fine.
The latter has zero intercept and is the structural repair, not a fitted map.
On admitted supplied geometry this representation gives responses for any
integrable incoming F; the finite source-simplex sufficiency certificate
below has a narrower domain and must not be conflated with that argument.

Derive directly from geometry the V^2-constant field observations for all
three tile levels and its coarse/fine responses. Check these equal ALL source
column sums of the respective matrices; retain them and generator integrals.
Retain coarse scales V^2*h_C*h_D and fine scales similarly, including zero.
Only normalized collision differences are serialized; zero fine scale gives
null there, while raw target/collision vectors and recovery flags remain.

Primary route: explicit Bernstein polynomial coefficients and antiderivative
moments, direct polynomial-times-clamped-branch contractions on repair pieces;
independent direct coarse targets on original support branches.
Reference route: quadratic interpolation for retained source coefficients,
direct Bernstein evaluation and knot-split tensor Simpson observations/targets
on original support, with direct clamped R, not G. Geometry moments may use
Simpson. Third test oracle: separable incomplete-beta/clamped-tail integration.
Implementations may reuse their OWN previous generic authoring patterns, but
no cross-reading/imports/shared mathematical helper or stored AR answers.

## Exact source-simplex sufficiency certificate

certify(O,Q) is a geometry-independent finite linear contract.
O native m by n,0<=m<=256; Q native q by n,1<=q<=64,1<=n<=576.
n comes from Q's first row, so zero-observation normalization-only problems
are admitted. Exact rational/schema/shape guards precede elimination.

Set A=[1^T;O]. Greedily scan ORIGINAL rows in order and retain the
lexicographically first independent row indices, row_basis (always starts0).
Let B be those rows. Use ascending pivot columns of its unique RREF R;
remaining columns are free_columns. All ranks are exact, no tolerances:
observation_rank=rank(A),target_rank=rank(Q),joint_rank=rank([A;Q]).

For every target row q_j, decide actual membership in rowspace(A).
If recoverable, row_decoders[j] is the UNIQUE coefficient row d_j with
d_j*B=q_j; otherwise it is null. Retain sorted recoverable_rows and failed_rows.
recoverable is true iff failed_rows is empty. decoder equals the complete
row_decoders matrix if all rows recover, otherwise null. Duplicate retained
entries are counted as such; no sparse/full-field/physical minimality claim.

Primary may carry basis transforms in Gauss-Jordan elimination.
Reference uses forward echelon reduction with retained row combinations and
reverse back-substitution, not the primary implementation.
Tests use exact rational Gram-Schmidt without square roots for row/column
independence and coefficient/null relations. No Gaussian/tolerance library.
Verify every recovered complete identity; verify membership decisions over
all columns, joint/target ranks and the complete canonical witness rule.

If recoverable, collision=null. Otherwise, for each free column j ascending,
construct canonical w_j: free component j=+1, all other free components0,
pivot components -R[:,j]. Select FIRST free column with Q*w_j nonzero,
then FIRST detecting target row. No sign flip or target-first selection.
A*w=0 includes exact sumw=0. Set mass=sum positive entries=sum negative
magnitudes, require mass>0, and lambda_plus=max(w,0)/mass,
lambda_minus=max(-w,0)/mass. Both are genuine normalized nonnegative mixtures.

collision EXACT:
{free_column,separating_row,null_vector,positive_mass,weights_plus,weights_minus,
observed_plus,observed_minus,truth_plus,truth_minus,truth_difference}.
observed vectors are O*lambda, true vectors Q*lambda;
truth_difference=truth_plus-truth_minus=Q*w/mass, NOT unnormalized Q*w.
Verify all complete vectors, normalization, disjoint positive/negative support,
exact identical observations, first witness ordering and a nonzero true difference.

certificate EXACT:
{observation_rank,target_rank,joint_rank,row_basis,pivot_columns,free_columns,
recoverable,decoder,recoverable_rows,failed_rows,row_decoders,collision}.
Standalone certify does not authenticate geometry, source preparation or
external matrix provenance. Its mathematical simplex claim is conditional
on the supplied columns/normalization.

## Restricted application and repair witness

apply(a,L,x) receives ONLY raw intercept, dense matrix and observations.
Return a+L*x. q1..64, positive multiple-of-four observed width<=1024,
all exact pairs; matrix q by width, no null raw rows. No hidden geometry,
source weights, true targets, certificate or file read.
It is an affine evaluator, not an external-map provenance verifier.
A compact certificate decoder is densified through row_basis (index0 is
normalization; indexk>0 maps to raw observation k-1) for application tests.

repair EXACT {intercept,matrix,predicted,residuals,exact,collision}.
intercept all zero; matrix G_repair; predicted=G_repair*O_repair;
residuals=predicted-Q_fine; require exact=true and all residuals zero.
If the coarse certificate has no collision, repair.collision=null.
Otherwise retain EXACT:
{fine_observed_plus,fine_observed_minus,observed_plus,observed_minus,difference,
predicted_plus,predicted_minus,residual_plus,residual_minus,normalized_truth_difference}.
fine_observed uses ORIGINAL fine moments. observed uses NEW repair moments.
difference is repair plus-minus and MUST be nonzero when truths differ.
Do not require original fine observations to differ: extra overlay measurements
can matter in the generic interface. Raw repair predictions equal both true
fine responses separately; residual vectors are zero. Normalize the true
difference using fine scales, retaining null for zero scale. All entries checked.

## Full family wire and literal counts

Family EXACT {problem,geometry,generators,matrices,certificate,repair,checks,counts}.
problem detached input.
geometry EXACT:
{volume,coarse_cells,fine_cells,parents,coarse_tiles,fine_tiles,repair_tiles,
coarse_response_scales,fine_response_scales}.
cells {event,bounds,volume}; parents [{event,parent}], fine-cell order.
coarse tiles {event,bounds,moments,outgoing}, outgoing [{event,coefficients}]
for all coarse D. Original fine tiles {event,bounds,coarse_tile,moments}.
repair tiles {event,bounds,fine_tile,coarse_tile,moments,outgoing}, outgoing
for all fine D. generators [{tile,i,j,coefficients}], identical to AQ labels.

matrices EXACT:
{coarse_observation_rows,fine_observation_rows,repair_observation_rows,
coarse_response_rows,fine_response_rows,coarse_observations,fine_observations,
repair_observations,coarse_targets,fine_targets,coarse_geometric,
generator_integrals,constant_coarse_observations,constant_fine_observations,
constant_repair_observations,constant_coarse_targets,constant_fine_targets}.
Observation labels {tile,basis}; response labels {first,second}.
All scalars exact pairs except native indices/counts/bools; null only where specified.

checks EXACT all true only after the named verifications:
geometry_partitions,bernstein_partition,generator_integrals,moment_additivity,observation_additivity,response_additivity,geometric_coarse_identity,geometric_fine_identity,coarse_certificate_valid,collision_valid,repair_collision_valid,constant_field_sums.

counts EXACT:
coarse_cells,fine_cells,positive_coarse_cells,positive_fine_cells,coarse_tiles,fine_tiles,repair_tiles,added_repair_tiles,generators,coarse_observation_rows,fine_observation_rows,repair_observation_rows,coarse_response_rows,fine_response_rows,defined_fine_response_rows,undefined_fine_response_rows,coarse_moment_entries,fine_moment_entries,repair_moment_entries,outgoing_entries,source_coefficient_entries,observation_entries,target_entries,constant_observation_entries,constant_target_entries,generator_integral_entries,raw_geometric_entries,certificate_decoder_entries,recoverable_rows,failed_rows,collisions,collision_entries,repair_prediction_entries,repair_residual_entries,repair_collision_entries.
added_repair_tiles=r-f. Observation/target/constant counts sum their THREE/TWO
declared matrices/vectors. outgoing_entries=4*(t*c+r*d), with d fine-cell count.
raw_geometric_entries=c^2*(4*t)+d^2*(1+4*r), including repair intercepts.
certificate_decoder_entries counts all rational occurrences in nonnull
row_decoders PLUS full decoder if nonnull; do not count row_basis/indices.
collision_entries counts all rational occurrences in collision (including mass):
3*n+2*m_coarse+3*q_fine+1, or0.
repair_collision_entries if present:
2*m_fine+3*m_repair+4*q_fine+defined_fine_rows, otherwise0.
All retained zeros/repeats count; indices are excluded from rational counts.
Rank fields are not added to counts/totals as an information-minimality result.

## Suite, prior bridges and affine controls

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Input projection consumes ONLY AQ problem's six declared geometry fields.
Admit fixed grid/warp family order and seven/eight-cell,eight/twelve-tile
inventories. Authenticate the entire AQ capture and its ancestry.
After builds, compare selected AQ geometry (coarse/fine cells,parents,original
tiles with all moments/outgoing,volume,coarse scales), generators,
O_coarse,Q_coarse,G_coarse,labels,integrals and coarse constant vectors.
Never replay AQ canonical residuals, bounds/witnesses, old original O/Q
identities or any historical executor. No old numerical answer enters engines.

prior_bridges EXACT:
{AQ_selected_families:["grid","warp"],AQ_geometry_inputs_equal:true,
AQ_selected_geometry_equal:true,AQ_sources_equal:true,
AQ_coarse_measurements_equal:true,AQ_coarse_targets_equal:true,
AQ_geometric_map_equal:true,AQ_source_sums_equal:true,
other_historical_mathematics_replayed:false,older_executors_run:false}.
payload_sizes rows EXACT
{family,input_bytes,geometry_bytes,generator_bytes,measurement_bytes,target_bytes,
certificate_bytes,repair_bytes,native_family_bytes}.
measurement projection uses the six observation label/matrix fields;
target projection uses the four target label/matrix fields.
Other scopes are named projections, canonical JSON plus newline.
Overlapping byte counts are not additive unique storage or an online packet.
totals sums every count and adds families=2.
scope EXACT all false:
source_dictionary_changed,old_convex_hull_inclusion_proved,full_field_recovery_tested,repair_minimality_proved,fine_measurements_recovered_from_coarse,physical_sources_established,empirical_noise_calibrated,unknown_geometry_reconstructed,quantum_channel_constructed,gravity_derived,ret_integration_tested,lean_verification_performed,generic_production_API_hardened,fixed_affine_families_run,older_executors_run.

Generic positive affine axes u'=alpha*u+du,v'=beta*v+dv,k=alpha*beta:
source labels, original/repair lineage and normalized mixture weights unchanged.
Transport moments with Jacobian/binomial factors, coefficients with amplitude
k^2 and coordinate pullback, outgoing coefficients with factor k,
observations by block P=k^3*(global monomial change), targets by k^4.
All observation levels and coarse/fine targets/constant sums participate.
Ranks,row_basis,pivot/free columns, recovery flags and canonical null weights/
indices are invariant. The block lower-triangular observation transform
preserves prefix row ranks. Collision truths/differences scale k^4,
normalized differences remain invariant. Check full wires, not ranks alone.
Do NOT assume compact decoder transport uses only the selected P submatrix:
omitted dependent rows can mix. Independently recertify and verify full
identities; separately transport the full dense map a'=k^4*a,L'=k^4*L*P^-1.
Repair structural map obeys the latter formula. No fixed affine cases.

Generic controls: same-level recovery; an analytic normalized two-mixture
coarse collision with unequal fine truths; zero/normalization-only targets;
duplicate/dependent source columns; tiny exact pivots; free-column-first
versus target-first witness ordering; explicit overlay that changes measurement
tiles but not source coordinates; active fine knots inside coarse tiles;
empty regions; complete affine/source/response sums; restricted apply,
detachment, bounded guards normal/-O; full-wire/selected-producer mutations;
source/capture changes, serialization caps, exclusive capture and read-only replay.

## Freeze, capture and publication

AQ pin:934498 bytes SHA256
c9c0bb0b20cd3646217e6ad97eaf2f41ca40406fc94d8fac975b67267eec6a08.
AQ plus47 prior captures gives48 captures; AQ's5 sources plus54 ancestors
gives59 ancestor sources; five AR sources give112 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05ar.py after generic
checks and independent reviews, BEFORE root explicitly releases any fixed
AR projection/integration/rank/collision/refinement calculation.
Disclose every post-first source/protocol/fixture/mathematical correction.

First primary/reference comparison, exactly ONE independent normal
reference-only read-only audit, full normal/-O tests, external create-only
preflight, exclusive final capture, fresh primary-normal/reference--O final
read-only replays. Audit and full tests may run in parallel after first
comparison; both must complete before preflight. Bracket all112 identities
and exact capture bytes. Isolated Python/external caches, no dependencies.
Capture limit128MiB and serialized working-document limit192MiB are not
process-memory or exhaustive adversarial-resource guarantees.
RESULTS.md/bridge roadmap outside ledger; publish only this directory and roadmap.

