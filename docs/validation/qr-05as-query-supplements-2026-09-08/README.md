# QR-05AS protocol: query-specific supplemental linear readouts

8 September 2026. Prospective before fixed AS calculations.
Base: pushed AR commit cc02338677db72fecd729d69d7eb330a2e0a44d7.
Preserve unrelated RET/core/governance work and temporary sheets.

## Question and inherited scope

On AR's SAME normalized nonnegative source simplex, construct a minimum number
of additional fixed scalar LINEAR readouts that, together with coarse data,
determine every fine response. AR's retained joint-rank increment is five in
both families; AS selection, filters, decoder and indispensability witnesses
have not been calculated. Do not prescribe selected target indices, filter
support, decoder coefficients or witness values before execution.

Consume authenticated AR finite matrices and their source-column ordering.
Let O be coarse measurements, R the repair-moment bank, Q fine targets, G the
declared repair map, with Q=G R. AR already independently integrated these
tables. AS rechecks this selected algebra, not geometry, quadrature, source
positivity, old collisions or any historical executor. No new source family,
field model, supplied geometry, target question or normalization.

The structural interpretation of an inherited filter on integrable fields
comes from AR. The final reduced decoder here is certified ONLY on the full
declared source simplex. Its validity on arbitrary fields is not inferred.

## Native problem and public APIs

build_family(problem) input EXACT:
{family,target_labels,observations,bank,targets,filters}.
family nonempty native str. target_labels q native records {first,second},
signed native integer IDs, sorted unique lexicographically by (first,second).
Labels name questions; generic problems need not enumerate a Cartesian square.

observations=O has m rows, bank=R has r rows, targets=Q has q rows and n columns;
filters=G has q rows and r columns. Infer n from Q's first row.
Caps: 0<=m<=256, 0<=r<=1024, 1<=q<=64, 1<=n<=576.
Empty O and empty R are admitted. If R=[], G consists of q empty rows and
Q=G R requires all targets zero. No multiple-of-four constraint on generic
matrix row counts. Fixed projection has m32,r48,q64,n108 in grid then warp.

Native exact dict/list with exact keys; rational scalars reduced native
integer pairs [numerator,denominator], denominator>0. All retained integer
and rational components <=4096 bits. Reject bool/float/numeric or container
subclasses, malformed/ragged data, invalid labels, extra/missing keys, cap
excess and incompatible shapes via explicit ValueError normally and under -O.
Complete container inventories, dimensions and rational-pair SHAPES precede
fraction arithmetic, matrix multiplication or elimination. All rational
values are admitted before mathematical operations. Shared valid containers
are allowed; returned wires detached. Exact unretained intermediates may cancel.
No exhaustive hostile-object/graph, process-memory or production API claim.

produce(filters,bank_values): ONLY k by r raw filter coefficients and r values;
0<=k<=64, 0<=r<=1024. Return k exact scalar products. An empty filter list
returns []; no hidden geometry, Q, source weights, certificate or file access.
apply(intercept,matrix,observed): ONLY q intercepts, q by s raw coefficients
and s ordered values; 1<=q<=64, 0<=s<=320. Return intercept+matrix*observed.
Width need not be divisible by four. Empty observed and q empty matrix rows
are valid, including nonzero intercepts. These evaluators do NOT authenticate
model provenance or whether external values arise from a common source mixture.

## Canonical exact selection and full decoder

Unknown lambda>=0, sum(lambda)=1. Set A=[1^T;O].
Greedily scan ORIGINAL rows of A in order to obtain its lexicographically
first independent row_basis. Retain ascending pivot columns of its unique
RREF and the complementary free_columns. All ranks and equalities exact.

base EXACT:
{observation_rank,target_rank,joint_rank,delta,row_basis,pivot_columns,
free_columns,recoverable_rows,failed_rows}.
Here ranks are rank(A), rank(Q), rank([A;Q]); delta=joint-observation rank.
recoverable_rows/failed_rows are original Q indices inside/outside rowspace(A),
NOT membership after supplementation. Known normalization is not a measured row.

Starting with the original independent basis of A, scan Q rows in ORIGINAL
order. Select a row iff it is independent of A AND previously selected rows.
Append selected ORIGINAL rows unchanged to the basis, never residualized
functionals. Record every decision in target order, EXACT:
{target_row,rank_before,rank_after,selected,coefficients}.
Selected rows have coefficients=null and increment rank by one.
For a skipped row, coefficients are its UNIQUE expansion in the current
independent ORIGINAL basis; rank unchanged. Check every complete identity.
No target-first/free-column witness search is involved in this selection.

selection EXACT:
{target_rows,target_labels,decisions,filters,bank_support,values}.
target_rows ascending selected Q indices; target_labels corresponding copies.
filters are EXACT corresponding rows of supplied G, not optimized or refitted.
bank_support is a list of sorted nonzero coefficient indices for each filter.
values=H=filters*R must equal the selected ORIGINAL Q rows on every column.
If delta=0, all these lists except decisions are empty.
Require number selected=delta and terminal rank=joint_rank.

Set X=[O;H] (coarse rows first, then supplements) and M=[1^T;X].
Find the lexicographically first independent ORIGINAL row basis of M, in that
order. It consists of the base row_basis followed by indices 1+m+j for each
selected j. Use ascending RREF pivot columns and complementary free columns.
For every target obtain its unique coefficients D in this independent basis B.
D B=Q on ALL source columns. Densify D: row index0 contributes an intercept;
row index i>0 contributes to raw input coordinate i-1; omitted rows get zero.

decoder EXACT:
{row_basis,pivot_columns,free_columns,coefficients,intercept,matrix,
predicted,residuals,exact}.
coefficients q by joint_rank, intercept q, matrix q by (m+delta).
predicted=a*1^T+L X, residuals=predicted-Q; require all zero and exact=true.
The coefficient matrix is not transported using an arbitrary selected
submatrix of an observation coordinate change.

## Constructive indispensability witnesses

For EACH selected readout j in selection order, construct one canonical
right-inverse direction using the SAME full independent basis B above.
Let P be its ascending pivot columns; B[:,P] is an invertible square matrix.
Solve B[:,P]*w[P]=e_(observation_rank+j), and put every nonpivot component zero.
This sets the selected response j to one, other selected responses to zero
and all base measurements/normalization to zero:
sum(w)=0, O w=0, H w=e_j.
This is NOT an AR first-free-column null witness and requires no new search.
Require exact complete identities and the prescribed nonpivot zeros.

mass=sum(max(w,0))=sum(max(-w,0))>0.
lambda_plus=w_positive/mass, lambda_minus=w_negative/mass.
Both are normalized nonnegative disjoint-support mixtures.
Delete coordinate m+j from X to obtain the available observation interface.
The two mixtures have identical available values, but the omitted supplement
and its named target differ by 1/mass>0. This proves the necessity of each
member of this selected bank; the global minimum follows separately below.

witnesses is a list of delta records, EXACT:
{omitted_index,target_row,available_rows,null_vector,positive_mass,
weights_plus,weights_minus,bank_plus,bank_minus,coarse_plus,coarse_minus,
supplement_plus,supplement_minus,available_plus,available_minus,
truth_plus,truth_minus,truth_difference,predicted_plus,predicted_minus,
residual_plus,residual_minus}.
omitted_index is j; target_row=selection.target_rows[j].
available_rows lists all original X indices except m+j, in order.
null_vector is w above, a null vector only for the interface WITH j REMOVED.
bank/coarse/true vectors are direct R/O/Q products with each lambda.
Supplement vectors must be computed by restricted produce from bank vectors,
and equal H*lambda. Available vectors select coarse+supplement coordinates.
Predictions use restricted apply on the COMPLETE coarse+supplement vector,
not the deleted one; they must equal the two complete true vectors and all
residuals zero. truth_difference=Qw/mass. No normalized geometric scale is added.
Retain and check all vectors, not just the omitted component.

## Minimality statement and its limits

For any k fixed scalar linear readouts T on the same source weights, exact
recovery requires rowspace(Q) contained in rowspace([A;T]). Otherwise a null
direction splits into normalized nonnegative mixtures with identical data
and different truths, precluding even nonlinear decoding of those data.
Thus rank([A;Q])<=rank(A)+k and k>=delta. Selected rows construct k=delta.

Known affine offsets lie in the already included normalization row and do
not improve this bound. This is NOT a bound for arbitrary nonlinear encodings,
adaptive sensing, noisy/finite-precision observations or a smaller physical
source domain. The selected filters literally measure selected target
functionals. A source-side system with fine access emits their values;
a receiver with only coarse values cannot create those missing values.

The count is algebraic supplemental scalar interface minimality, not smallest
subset of individual bank moments, sensor count, locality, support, precision,
storage bytes or acquisition cost. Count filter support diagnostically without
minimizing it. Acquiring R to implement filters can still require many moments.
No full-field reconstruction, new physics, empirical noise or RET integration.

## Family wire, counts, independent routes and controls

Family EXACT {problem,base,selection,decoder,witnesses,checks,counts}.
checks EXACT, true only after corresponding verification:
inherited_filter_identity,base_certificate,greedy_selection,
selected_filter_identity,receiver_identity,witness_constraints,
online_witness_recovery,minimality_certificate.

counts EXACT:
source_columns,coarse_values,bank_values,target_rows,supplement_values,
receiver_values,input_matrix_entries,selected_filter_entries,
selected_filter_nonzero,selected_bank_rows,supplement_entries,
decision_coefficient_entries,decoder_compact_entries,decoder_raw_entries,
prediction_entries,residual_entries,witnesses,witness_entries.
input_matrix_entries=m*n+r*n+q*n+q*r.
selected_filter_entries=delta*r, selected_filter_nonzero counts nonzero
coefficients, selected_bank_rows is the union of all bank_support indices.
supplement_entries=delta*n.
decision_coefficient_entries sums all nonnull decision coefficient lengths.
decoder_compact_entries=q*joint_rank; decoder_raw_entries=q*(1+m+delta).
prediction/residual_entries=q*n each.
witness_entries sums all rational occurrences, including positive masses:
delta*(3*n+2*r+2*m+2*delta+2*(m+delta-1)+7*q+1), or zero if delta=0.
Retained zeros/repetitions count; indices and labels are not rational entries.

Primary: exact Gauss-Jordan elimination with basis transforms/right inverses.
Reference: independently authored forward echelon reduction and reverse
back-substitution with original row combinations. Tests: rational Gram-Schmidt
row/column projections without square roots. No shared math helper or
cross-reading another math implementation. Authors may reuse their OWN
previous generic patterns, but no historical import/execution or stored AS
selection/decoder/witness answer.

Synthetic controls: normalization-only/zero targets, zero O/R/selected widths,
partial recovery, duplicate/dependent source and target rows, tiny exact pivots,
nonzero intercepts, original-order decisions, nonunique declared G filters,
each omitted-readout collision, raw producer/receiver file blindness, strict
shape-before-arithmetic, input/output ownership and retained overflow versus
unretained cancellation. Full-wire, selected historical producer and lifecycle
mutations must be non-noop. Every fixed fixture is lazy and each fixed test
name contains fixed; prefreeze tests use -k 'not fixed'.

Affine/metamorphic controls use O'=P O, R'=S R, Q'=v Q, G'=v G S^-1,
with P,S invertible and v>0. Ranks, delta, target selection and available
readout indices persist. Canonical ORIGINAL-row basis indices persist only
for prefix-preserving P (including AR's block lower triangular coordinate
maps); recertify otherwise. Full-source pivot columns persist.
Selected filters transform by v*filters*S^-1 and H'=v H.
With T=blockdiag(P,v I_delta), transport the SAME full dense receiver by
a'=v a,L'=v L T^-1; independently recertify the canonical decoder and check
full identities. Canonical witness w'=w/v, mass'=mass/v and normalized weights
unchanged; targets and omitted truth differences scale v.
AR positive affine coordinates have v=k^4,P/S=k^3 times the four-monomial
change, k=alpha*beta. No fixed affine cases or geometry replay.

## Suite, historical bridge and evidence lifecycle

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Project only AR family name, fine response labels, O_coarse, O_repair,
Q_fine and repair.matrix. Require inherited repair.intercept all zero.
Admit grid then warp with fixed matrix dimensions above. AR's original
source dictionary and geometry remain authenticated provenance, not new inputs.
After builds compare base ranks, row_basis,pivot/free columns and base
recoverable/failed rows to selected AR certificate fields. No old AR decoder
or collision replay, no other historical mathematics.

prior_bridges EXACT:
{AR_selected_families:["grid","warp"],AR_selected_inputs_equal:true,
AR_zero_repair_intercept:true,AR_base_certificate_equal:true,
AR_filter_identity_rechecked:true,other_historical_mathematics_replayed:false,
older_executors_run:false}.
payload_sizes each EXACT:
{family,input_bytes,base_bytes,selection_bytes,decoder_bytes,witness_bytes,
producer_map_bytes,receiver_map_bytes,native_family_bytes}.
Named scopes canonical JSON+newline; producer_map is selection.filters;
receiver_map EXACT {intercept,matrix} from decoder. Overlapping byte scopes
are not additive unique storage or measured-value transmission packets.
totals sum all counts and add families=2.
scope EXACT all false:
source_dictionary_changed,geometry_reintegrated,old_collision_replayed,
full_field_recovery_tested,individual_bank_minimality_proved,
sensor_cost_minimality_proved,nonlinear_encoding_minimality_proved,
adaptive_readout_minimality_proved,empirical_noise_calibrated,
physical_sources_established,unknown_geometry_reconstructed,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.

AR pin:704842 bytes SHA256
c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8.
AR plus48 prior captures gives49 captures. AR's5 sources plus59 ancestors
gives64 ancestor sources. Five AS sources give118 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05as.py after generic
tests and independent reviews BEFORE root explicitly releases fixed AS input
projection, multiplication, rank, selection, decoder or witness calculation.
Disclose every post-first source/protocol/fixture/mathematical correction.

First primary/reference comparison, exactly ONE independent normal
reference-only read-only audit, full normal/-O tests, external create-only
preflight, exclusive final capture, fresh primary-normal/reference--O final
read-only replays. Audit and full tests may run concurrently after first;
both finish before preflight. Bracket all118 identities and exact capture
bytes; all non-runtime first/preflight/final fields must agree.
Isolated Python and external caches; no new dependencies.
Capture cap128MiB/serialized working cap192MiB are not process-memory bounds.
RESULTS.md and bridge roadmap outside ledger. Publish only this directory
and roadmap; preserve unrelated work.
