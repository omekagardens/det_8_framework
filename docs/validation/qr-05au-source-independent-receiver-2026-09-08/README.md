# QR-05AU protocol: source-independent receiver construction

8 September 2026. Prospective before fixed AU calculations.
Base: pushed AT commit c99368b7ffc9ef84b3f1b700ca1e48570cdc76dd.
Preserve unrelated RET/core/governance work and temporary sheets.

## Question and construction boundary

Does the SAME interface x=Bz, B=[C;F], admit a zero-intercept receiver for
Gz on unrestricted raw bank vectors? C is AT's authenticated coarse parent
sum and F the SAME five AS filters. G is the full geometric bank response map.
Construct an explicitly NEW decoder, without rewriting AS/AT evidence.

The decoder MUST be determined from B and G alone. Source matrices R,O,Q
serve only as consistency/application checks, never fitting data. Do not add
a normalization/constant row, infer an off-model constraint, alter filters,
add measurements, rebuild geometry or integrate sources/targets.
No fixed rank, recovered-row inventory, decoder coefficient or witness is
prescribed. Grid/warp outcomes remain unknown until the frozen calculation.

G factors through B iff every G row lies in rowspace(B), equivalently
ker(B) is contained in ker(G). If it does not, raw inputs0 and w with
Bw=0,Gw!=0 disprove even nonlinear decoding on the unrestricted bank domain.
Any globally correct affine receiver must have intercept0 since z=0 is included.
Neither result alone establishes physically realizable moments, source
preparation, full-field reconstruction, minimum sensor/packet cost or gravity.

## Native problem and public APIs

build_family(problem) input EXACT:
{family,target_labels,coarse_map,filters,geometric,selected_rows,
bank,observations,targets}.

family nonempty native str; target_labels q sorted unique native records
{first,second}, signed native integer IDs. C=coarse_map is m by r,
F=filters k by r, G=geometric q by r. selected_rows is an ascending unique
list of k target indices; F must literally equal the corresponding G rows.
R=bank is r by n, O=observations m by n, Q=targets q by n.
Caps 0<=m<=256,0<=k<=q<=64,1<=r<=1024,1<=n<=576,s=m+k<=320.
Infer r from first G row and n from first Q row. Empty coarse/supplement
interfaces are admitted; there is no multiple-of-four generic constraint.
C is a generic supplied linear map; geometric incidence is inherited provenance,
not a new generic rectangle claim.

Native exact dict/list with exact keys; rational scalars reduced native pairs
[numerator,denominator], positive denominator; retained integer/rational
components <=4096 bits. Complete container inventories, dimensions, labels,
indices and rational-pair SHAPES precede Fraction construction/elimination.
All rational VALUES are admitted before matrix work. Reject bool/float/numeric
or container subclasses, malformed/ragged data, invalid selections and cap
excess with explicit ValueError normally and under -O.
Reject active cycles, accept valid shared children, preserve inputs and detach
outputs. Unretained exact intermediates may cancel. No exhaustive hostile
graph/object, process-memory, arithmetic-work or production API guarantee.

certify(interface,geometric) receives ONLY B and G, native s by r and q by r,
0<=s<=320,1<=q<=64,1<=r<=1024; r from first G row. It returns the exact
certificate below, with no source columns, old decoder or file access.
produce(matrix,bank_values) receives ONLY a raw h by r matrix and r values,
0<=h<=320,0<=r<=1024; returns h scalar products.
apply(matrix,observed) receives ONLY a raw v by s matrix and s values,
0<=v<=64,0<=s<=320; returns v scalar products. There is NO intercept argument.
Empty rows/widths are admitted, with exact zero outputs where appropriate.
Evaluators do not authenticate external values, common-source consistency or
physical provenance. Failed response rows must not be passed as fabricated zeros.

## Deterministic zero-intercept certificate

Greedily scan ORIGINAL B rows in their supplied order, retaining the first
independent rows as row_basis. There is NO normalization row, and raw row0
is a measured interface coordinate, not an intercept. Let M be this independent
original-row basis. Retain ascending pivot columns of its unique RREF and the
complementary free_columns. Empty/rank-zero interfaces have empty bases/pivots
and every bank column free.

interface_rank=rank(B),target_rank=rank(G),joint_rank=rank([B;G]).
For each original target row i, decide exact membership in rowspace(B).
If recoverable, row_coefficients[i] is its unique expansion d_i in M,
verified on ALL bank columns: d_i M=G_i. If failed, that entry is null.
Do not serialize a zero coefficient row as a substitute for a failed target.

certificate EXACT:
{interface_rank,target_rank,joint_rank,row_basis,pivot_columns,free_columns,
recoverable_rows,failed_rows,row_coefficients,recoverable,collision}.
Index lists ascending; recoverable iff failed_rows is empty.
Ranks and all membership decisions exact. No tolerances or numerical libraries.

If all rows recover, collision=null. Otherwise, for each free column j in
ascending order define w_j[j]=1, other free coordinates0, pivot coordinates
-RREF(M)[:,j]. Choose the FIRST free column for which G w_j is nonzero,
then the FIRST detecting original target row. No target-first selection or
sign flip. Verify the canonical pivot/free rule and complete B w=0,G w!=0.

collision EXACT:
{free_column,separating_row,null_vector,bank_a,bank_b,observed_a,observed_b,
truth_a,truth_b,truth_difference}.
null_vector=w, bank_a=0,bank_b=w; observed vectors MUST use actual restricted
produce(B,bank), true vectors MUST use produce(G,bank).
truth_difference=truth_b-truth_a=G w, with all observed entries equal zero
and the separating response nonzero. These are signed/raw bank inputs:
sum(w)=0 is NOT required, and no positive/negative or probability normalization
is performed. One canonical global collision certifies full-interface failure;
per-row membership is separately certified.

Primary uses Gauss-Jordan elimination with original-basis transformations.
Reference uses independently authored forward echelon reduction/original-row
combinations and reverse back-substitution. Third oracle uses rational
Gram-Schmidt row/column projection without square roots.
No shared math helper, other author's math-source reading, historical engine
import/execution or stored AU numerical answer. Own generic patterns may be reused.

## Full family, recovered receiver and actual application

Family EXACT {problem,interface,source,certificate,decoder,bank_controls,checks,counts}.
interface is B, coarse rows first then supplemental rows.

source EXACT {interface_values,geometric_values,coarse_residuals,target_residuals}.
interface_values=B R, geometric_values=G R.
Require the first m interface rows equal O, geometric_values=Q, and last k
interface rows equal selected Q rows. Retain coarse_residuals=(CR-O) and
target_residuals=(GR-Q), both zero. Source checks never change the certificate.

For each recoverable row, densify its unique compact expansion using row_basis:
place its coefficient at the corresponding RAW interface index and set omitted
coordinates zero. No index shift and no intercept extraction.
decoder EXACT {target_rows,matrix,bank_predicted,bank_residuals,
source_predicted,source_residuals,complete}.
target_rows is certificate.recoverable_rows; let v be its length.
matrix D is v by s and maps ONLY those indexed target rows.
bank_predicted=D B=G_recovered; bank_residuals all zero.
source_predicted=D*(B R)=Q_recovered; source_residuals all zero.
complete iff v=q. If v=0, every decoder list is empty and complete=false.
A partial recovered-only receiver is not a full target prediction.

ALWAYS evaluate the r+1 bank controls z=0,e0,...,e(r-1), even on partial failure.
bank_controls each EXACT:
{bank_index,bank_values,coarse_values,supplement_values,observed,
truth,predicted,residuals}.
bank_index null then0..r-1. coarse_values=produce(C,z),
supplement_values=produce(F,z), observed is their concatenation,
truth=produce(G_recovered,z), predicted=MUST call apply(D,observed).
Check every vector against its direct exact product; residuals zero.
These controls cover ONLY recovered rows. Failed rows remain explicitly null
in the certificate and are handled by the full-target collision above.
All-zero recovered-control residuals alone do NOT imply complete recovery.

checks EXACT, true only after corresponding verification:
selected_filter_identity,source_inputs_consistent,source_independent_certificate,
decoder_bank_identity,decoder_source_identity,restricted_application,
collision_valid,complete_classification.

## Synthetic and transport controls

Include normalization-dependent traps that AU must reject; rank-zero/empty
interfaces; zero/nonzero/duplicate target rows; redundant/zero original rows;
partial recovery with one global collision; a free-column-first witness that
differs from target-first selection; first invisible free directions;
tiny exact pivots, retained overflow versus intermediate cancellation; raw
width0/non-multiple-of-four APIs, active cycles, shared-input detachment,
shape/value-before-arithmetic and actual restricted call inventories.

Hold C,F,G fixed while changing source matrices and source-column counts
consistently: certificate and D must stay identical. Spy on build_family's
certify call to verify it receives ONLY B,G. Do not read old source-fit decoders.

For invertible coarse-row P and bank-coordinate S, and positive v_scale:
C'=P C S^-1,F'=v_scale F S^-1,G'=v_scale G S^-1,
R'=S R,O'=P O,Q'=v_scale Q.
Then B'=T B S^-1 with T=blockdiag(P,v_scale I_k).
Transport a SAME dense recovered decoder as D'=v_scale D T^-1 and a SAME
null witness as w'=S w. Check full identities and transported raw probes.
Independently recertify canonical maps: ranks/recovered target indices persist,
but dense canonical coefficients can differ from the transported map.
Non-prefix P may change original-row basis indices; S may change pivot/free
columns and canonical first witnesses. Do not require their invariance.
No fixed affine families, source/geometry integration or physical interpretation
of signed transformed bank vectors.

## Literal counts, projection and suite

counts EXACT:
coarse_values,bank_values,source_columns,target_rows,supplement_values,
receiver_values,input_matrix_entries,interface_entries,source_check_entries,
compact_decoder_entries,raw_decoder_entries,bank_prediction_entries,
bank_residual_entries,source_prediction_entries,source_residual_entries,
bank_controls,bank_control_entries,collisions,collision_entries,
recovered_rows,failed_rows.

input_matrix_entries=m*r+k*r+q*r+r*n+m*n+q*n.
interface_entries=s*r; source_check_entries=(s+m+2*q)*n.
compact_decoder_entries=v*interface_rank; raw_decoder_entries=v*s.
bank_prediction/residual_entries=v*r each.
source_prediction/residual_entries=v*n each.
bank_controls=r+1; bank_control_entries=(r+1)*(r+2*s+3*v).
collisions=0 or1; collision_entries=0 or3*r+2*s+3*q.
Retained zeros/repetitions count; indices/labels are excluded. Rank fields are
not added into counts as a new information/acquisition-minimality result.

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Consume ONLY authenticated AT family input name/labels, F,G,selected_rows,
R,O,Q and lineage.coarse_map C. Fixed grid then warp,m32,k5,r48,q64,n108.
Cross-check selected dimensions and F=selected G rows through engines.
Do NOT replay AT's old a/L/K/E, row status, controls, geometry partitions,
source predictions or earlier ranks/decoders/collisions.
Rechecking O=CR and GR=Q here is explicitly selected input consistency.

prior_bridges EXACT:
{AT_selected_families:["grid","warp"],AT_interface_inputs_equal:true,
AT_target_inputs_equal:true,AT_source_inputs_equal:true,
old_affine_decoder_replayed:false,old_bank_defect_replayed:false,
other_historical_mathematics_replayed:false,older_executors_run:false}.

payload_sizes each EXACT {family,input_bytes,interface_bytes,source_bytes,
certificate_bytes,decoder_bytes,bank_controls_bytes,receiver_map_bytes,
native_family_bytes}. receiver_map EXACT {target_rows,matrix}, from decoder.
Named projections are canonical JSON+newline and overlap; not additive unique
storage or measured-value transmission packets. totals sum all counts plus families=2.

scope EXACT all false:
source_dictionary_changed,geometry_reintegrated,old_collision_replayed,
old_decoder_modified,filters_reselected,measurements_added,
normalization_row_added,source_dependent_fit_performed,
physical_bank_controls_established,full_field_recovery_tested,
physical_interface_insufficiency_proved,minimality_recomputed,
empirical_noise_calibrated,unknown_geometry_reconstructed,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.
A new decoder construction here does not mean an old decoder file was modified.

## Freeze and evidence lifecycle

AT pin:1147189 bytes SHA256
3fe96ced94f7b4d45feec43d0415a908d656825e21f04a6796329825de4d651a.
AT plus50 prior captures gives51 captures; AT's5 sources plus69 ancestors
gives74 ancestor sources. Five AU sources give130 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05au.py after generic
tests and independent reviews BEFORE root releases fixed AU input projection,
rank, decoder, null-witness or bank-control calculations.
Fixed fixtures lazy; every fixed test name contains fixed; prefreeze -k 'not fixed'.

First primary/reference comparison; exactly ONE independent normal reference-
only read-only audit; full normal/-O tests; external create-only comparison
preflight; exclusive final comparison capture; fresh primary-normal and
reference--O final read-only replays. Audit/full tests may run concurrently
after first; both complete before preflight. Bracket all130 identities and
capture bytes; first/preflight/final non-runtime fields must agree.
Disclose every post-first source/protocol/fixture/mathematical correction.
Isolated Python/external caches; no dependencies. Capture cap128MiB and serialized
working cap192MiB are not process-memory/computation bounds.
RESULTS.md and roadmap outside ledger. Publish ONLY this directory and roadmap.
