# QR-05AT protocol: bank-level structural portability

8 September 2026. Prospective before fixed AT calculations.
Base: pushed AS commit e55e9c8869efa2e5a0d0fce029aafc3abf7f73f0.
Preserve unrelated RET/core/governance work and temporary sheets.

## Question and scope

Keep the SAME AS intercept a, receiver L, selected target rows and filters F,
and AR full bank map G and source matrices O,R,Q. Does the reduced frozen
receiver agree with G on every unrestricted raw bank vector, not only the
declared normalized source simplex? Retain failures without refitting.
No new sources, target questions, supplied geometry, integration or selection.

Derive a parent-sum map C from supplied positive rectangle partitions and
explicit bank-to-coarse tile indices. Recheck this selected partition
lineage and O=C R; do not infer C by fitting source matrices. Bounds and
source matrices are authenticated inherited data. This is finite partition
and matrix verification, not new moment/source/response integration.
Other cell/fine-tile provenance remains pinned, not reexecuted.

All moments use one shared GLOBAL four-function basis, in order (1,u,v,uv).
A child contributes its raw integral to its parent with unit coefficient,
not an area-weighted average. Geometric meaning of G comes from AR; arbitrary
bank vectors tested here are algebraic inputs, not automatically admissible
moment vectors, nonnegative fields, prepared states or measured observations.

## Native problem and admission

build_family(problem) input EXACT:
{family,coarse_tiles,bank_tiles,target_labels,observations,bank,targets,
geometric,selected_rows,filters,intercept,receiver}.

family nonempty native str. coarse_tiles is a list of c positive rectangles
[u0,u1,v0,v1]. bank_tiles is a list of b records {bounds,coarse_tile}.
Array order binds coordinates; coarse_tile is a native integer index in 0..c-1.
No event-ID inference or sorting/reordering of supplied tiles.
Coarse rectangles have pairwise disjoint interiors. Every bank rectangle is
contained in its named coarse rectangle; bank interiors are pairwise disjoint,
and their children cover EACH parent up to measure-zero boundaries.
Verify containment, disjointness and exact area sums. No global probe coverage
is claimed by the generic interface. Every parent has at least one child.
Caps 1<=c<=64,1<=b<=256; m=4c,r=4b.

target_labels q sorted unique records {first,second}, native signed integer IDs.
observations O is m by n, bank R is r by n, targets Q is q by n,
geometric G is q by r. selected_rows is an ascending unique list of k target
indices, 0<=k<=q. filters F is k by r and MUST literally equal selected G rows.
intercept a has q entries, receiver L is q by (m+k).
Infer n from first Q row; 1<=q<=64,1<=n<=576, hence m+k<=320.
No empty tile bank/coarse domain; empty supplements are admitted.

All containers native exact dict/list with exact keys. Rationals are reduced
native integer pairs [numerator,denominator], denominator>0; all retained
integer/rational components <=4096 bits. All container inventories, dimensions,
label/index and rational-pair SHAPES precede Fraction construction, partition
arithmetic and products. Admit all rational VALUES before mathematical work.
Reject bool/float/numeric or container subclasses, malformed/ragged schemas,
nonpositive/overlapping/uncovered rectangles, wrong selections and cap excess
with explicit ValueError in normal and -O modes. Active cycles are rejected;
valid shared children are allowed. Inputs unchanged; outputs detached.
Unretained exact intermediates may cancel. Caps are not exhaustive hostile-
object/graph, process-memory, arithmetic-work or production API guarantees.

Public produce(matrix,values): ONLY raw k by r coefficients and r values,
0<=k<=320,0<=r<=1024; returns their exact scalar products. This admits C,F,G
as raw matrices and empty widths/rows independently of build_family.
Public apply(intercept,matrix,observed): ONLY q offsets, q by s coefficients
and s values,1<=q<=64,0<=s<=320; returns a+Lx.
Both are file-blind, model/geometry/weight-blind numerical evaluators; they do
not authenticate external provenance, common-source consistency or physicality.

## Complete structural construction

For coarse tile i, bank tile j, and basis indices h,t in 0..3:
C[4i+h,4j+t]=1 iff bank j has coarse_tile i AND h=t, otherwise0.
Retain coarse_children in parent order, children in original bank-index order.
Retain all C entries and exact C R and C R-O; require residuals zero.

Split L horizontally into Lc (m columns) and Lh (k columns).
H=F R; require it equals selected Q rows. Require G R=Q.
Require a*1^T+L*[O;H]=Q on all source columns.
Construct K=Lc C+Lh F and E=K-G. Retain ALL entries, including zeros.
Retain E R and source residual a*1^T+E R; require all zero and equal the
direct receiver-source residual. Nonzero a or E is a VALID outcome.

On any bank vector z the signed response defect is d(z)=a+E z.
The SAME frozen map is unrestricted-bank exact iff a=0 and E=0.
Per-row structural exactness uses that row's intercept AND all coefficients.
No inference from finite source residuals alone; no rank/minimality search,
receiver recanonicalization, filter reselection or off-model constraint fit.

Family EXACT {problem,lineage,composition,classification,bank_controls,checks,counts}.
lineage EXACT {coarse_children,coarse_map,coarse_predicted,coarse_residuals}.
composition EXACT {supplement_source,geometric_source,geometric_residuals,
receiver_source,source_residuals,effective_map,coefficient_defect,defect_on_sources}.
These are respectively H,GR,GR-Q,a*1^T+L*[O;H],a*1^T+ER,K,E,ER.
Source residuals are checked through both constructions, not silently assumed.
Only input problem retains a; do not duplicate it as an independently fitted map.

classification EXACT {structural_rows,restricted_only_rows,
nonzero_intercept_rows,nonzero_defect_rows,unrestricted_exact,first_failure}.
All index lists ascending original target rows. restricted_only_rows is the
complement of structural_rows: every admitted family is source-simplex exact.
unrestricted_exact iff restricted_only_rows is empty.
first_failure is null if unrestricted_exact; otherwise EXACT
{control_index,target_row}, first failed control then first failed target row.
This is a canonical descriptive witness, not maximal or coordinate invariant.

## Prespecified full bank controls and independent routes

ALWAYS evaluate z=0, then e0,...,e(r-1), regardless of earlier outcome.
bank_controls has r+1 records EXACT:
{bank_index,bank_values,coarse_values,supplement_values,observed,truth,
predicted,residuals,affine_defect}.
bank_index null for zero, then j for unit ej; bank_values is the complete z.
coarse_values=produce(C,z), supplement_values=produce(F,z),
observed is their concatenation. truth=produce(G,z).
predicted MUST call restricted apply(a,L,observed).
residuals=predicted-truth; affine_defect=a+E z. Check every vector equality.
At zero residual=a; at ej residual=a+E[:,j], NOT E[:,j].
Every control passes iff a=E=0. Retain full vectors even when zero.
These controls are off-model algebra and do not establish physical realizability,
known-observable conflict, empirical robustness or interface insufficiency.

Primary independently constructs dense C,K,E by exact products and evaluates
the complete controls. Reference independently constructs the partition
incidence and recovers K[:,j] by frozen pipeline(ej)-pipeline(0), then checks
source columns and every control. Third test oracle uses direct indexed scalar
coefficient sums by parent/basis and supplement, plus analytic hands.
No shared math helper, other author's math source reading, old executor import
or stored AT numerical answer. Each author may reuse their OWN generic patterns.

Synthetic controls include structural pass; linear defects annihilating R;
nonzero intercept canceled only on normalized source columns; all unit probes
passing while zero fails; mixed structural/restricted rows; empty supplements;
unequal child areas with unit raw-integral sums; redundant source columns;
late shape/value guards; wrong/duplicate/missing parent coverage; arbitrary
raw API widths, nonzero offset at width0; detached aliases, active cycles,
tiny exact values, retained overflow versus unretained cancellation.

Use coordinate controls that respect incidence: a shared invertible four-basis
change U on every coarse/bank tile gives P=diag(U),S=diag(U), so P C=C S.
Use O'=P O,R'=S R,Q'=vQ,G'=vG S^-1,F'=vF S^-1 with v>0.
Transport SAME maps a'=va,Lc'=vLc P^-1,Lh'=Lh, without refitting.
Then K'=vK S^-1,E'=vE S^-1 and d'(S z)=v d(z).
Check full matrices and transported old probes; newly chosen unit probes are
different inputs, so first_failure/support/magnitudes need not be invariant.
Include signed non-prefix mixing, positive dilation, and independent tile
permutations with corresponding matrix/block/parent-index permutations.
These are finite algebra controls; no fixed affine families or geometry replay.

## Counts, selected historical bridge and suite

checks EXACT, true only after corresponding verification:
lineage_partition,coarse_source_identity,inherited_geometric_identity,
selected_filter_identity,source_receiver_identity,affine_probe_identity,
structural_classification.

counts EXACT:
coarse_tiles,bank_tiles,source_columns,coarse_values,bank_values,target_rows,
supplement_values,receiver_values,input_rational_entries,coarse_map_entries,
effective_map_entries,defect_entries,nonzero_defect_entries,
nonzero_intercept_entries,source_check_entries,bank_controls,
bank_control_entries,structural_rows,restricted_only_rows.

input_rational_entries=4c+4b+m*n+r*n+q*n+q*r+k*r+q+q*(m+k).
coarse_map_entries=m*r; effective_map_entries=defect_entries=q*r.
source_check_entries=2*m*n+k*n+5*q*n, counting the retained lineage and
composition source matrices. bank_controls=r+1.
bank_control_entries=(r+1)*(r+2*m+2*k+4*q).
Nonzero counts literal; row counts classification lengths. Rational entries
include zeros/repetitions, exclude indices/labels; counts are not sensor cost,
probabilities, unique storage or total-information minimality.

Suite EXACT {families,prior_bridges,payload_sizes,totals,scope}.
Project grid then warp. AS supplies only problem O,R,Q,G,target_labels,
selection.target_rows/filters and decoder.intercept/matrix. Recheck these
selected fields against AR observation/target labels, matrices and repair map;
require AR repair.intercept zero. No AS ranks, skipped decisions, decoder
basis/predictions, omission witnesses, or AR collisions are replayed.

AR supplies coarse rectangle bounds and repair {bounds,coarse_tile}; explicitly
check observation row labels are tile-major with basis0..3 and family inventory.
Authenticate repair fine_tile/owner/parent links to AR original fine tiles and
check each repair rectangle lies inside its referenced original fine rectangle.
This is selected index/bounds provenance, not cell-geometry or integration replay.
Fixed c8,b12,m32,r48,q64,n108,k5. Shape inventory is inherited, NOT AT outcome.

prior_bridges EXACT:
{AS_selected_families:["grid","warp"],AS_frozen_maps_equal:true,
AS_source_inputs_equal:true,AR_source_inputs_equal:true,
AR_lineage_inputs_equal:true,AR_observation_labels_checked:true,
AR_repair_links_checked:true,AR_zero_repair_intercept:true,
other_historical_mathematics_replayed:false,older_executors_run:false}.

payload_sizes each EXACT {family,input_bytes,lineage_bytes,composition_bytes,
classification_bytes,bank_controls_bytes,receiver_map_bytes,native_family_bytes}.
receiver_map EXACT {intercept,matrix}, from input a and receiver L.
Named projections canonical JSON+newline; overlapping scopes are not additive
unique storage or measured-value packet sizes. totals sum all counts plus families=2.

scope EXACT all false:
source_dictionary_changed,geometry_reintegrated,old_collision_replayed,
decoder_refitted,filters_reselected,off_model_normalization_inferred,
physical_bank_controls_established,full_field_recovery_tested,
measurement_interface_insufficiency_proved,minimality_recomputed,
empirical_noise_calibrated,unknown_geometry_reconstructed,
quantum_channel_constructed,gravity_derived,ret_integration_tested,
lean_verification_performed,generic_production_API_hardened,
fixed_affine_families_run,older_executors_run.

## Freeze and evidence lifecycle

AS pin:614211 bytes SHA256
901c7e1a7c53be35be5654fbb01e5bbde4044f6a50184dd80014df155129e366.
AS plus49 prior captures gives50 captures; AS's5 sources plus64 ancestors
gives69 ancestor sources. Five AT sources give124 distinct identity targets.
Freeze README.md,kernel.py,reference.py,study.py,test_qr05at.py after generic
tests and independent reviews BEFORE root explicitly releases fixed AT input
projection, C/K/defect/partition calculations or bank controls. Fixed fixtures
lazy; every fixed test name contains fixed; prefreeze use -k 'not fixed'.

First primary/reference comparison; exactly ONE independent normal reference-
only read-only audit; full normal/-O tests; external create-only comparison
preflight; exclusive final comparison capture; fresh primary-normal and
reference--O final read-only replays. Audit and full tests may run concurrently
after first; both finish before preflight. Bracket all124 identities and exact
capture bytes; first/preflight/final non-runtime fields must all agree.
Disclose every post-first source/protocol/fixture/mathematical correction.
Isolated Python and external caches, no dependencies. Capture cap128MiB and
serialized working cap192MiB are not process-memory or computation bounds.
RESULTS.md and roadmap outside ledger. Publish ONLY this directory and roadmap.
