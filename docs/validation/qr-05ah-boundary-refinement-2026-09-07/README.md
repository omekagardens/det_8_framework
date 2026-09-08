# QR-05AH protocol: partition refinement and boundary-error certificates

7 September 2026. Prospective specification before fixed AH computations.
Base: pushed AG commit f603b02ffba1d6965695eb13e572ad554f7d1827.
Keep unrelated RET/core/governance sources, dependencies and prior captures unchanged.

## Question and two access layers

Can a prescribed nested partition tighten a certified geometric enclosure while
preserving separate annotation, quadrature and observation errors?
This gate uses a supplied flat geometry; it does not reconstruct a metric.

The NEW generic certificate API is explicitly source-aware: it receives the
whole domain, cell bounds, interior representatives, supplied marks, probe
rectangles and parent lineage. It may calculate geometric areas and bounds.
Do not describe its result as available from one retained order-only record.

The observation API remains the unchanged, pinned AG analyze(problem), through
both existing independent AG implementations. It sees only retained induced
order, fixed marker IDs, the selection law and retained-cell marks. No domain,
bounds, parent labels, missing marks, source certificate or geometric targets
are passed to it. Reusing those verified engines does not constitute two new
independent implementations of the certificate; those are written separately.

No unknown metric/density, necessary/minimal annotation, continuum limit,
Poisson ensemble, Lorentz-invariant ensemble, physical calibration, RET/Lean
integration, quantum channel or gravitational dynamics is claimed.

## Geometric and refinement mathematics

Use ds²=du dv and rectangle volume Δu Δv/2 in the supplied flat comparison.
A domain and every cell/probe are positive rectangles [ul,uh,vl,vh].
Cells partition the domain up to zero-area boundaries: each is contained in
the domain, distinct interiors do not overlap, and their geometric areas sum
to the domain area. Area equality ALONE is not sufficient. The independent
route checks endpoint-arrangement tiles are covered exactly once.
Every representative lies STRICTLY inside its own cell. Every probe lies
inside the domain, including allowed common boundaries.

For each probe rectangle Q and cell i with geometric area g_i:
inner if its entire rectangle is contained in Q up to zero-area boundaries;
outer if its clipped intersection with Q has strictly positive area;
representative if its representative lies strictly inside Q.
A boundary-only touch is not outer membership. Fixed bookkeeping markers are
not cells and carry no volume.

L=sum inner g_i; U=sum outer g_i; G=sum representative g_i;
T=sum representative supplied w_i; V=volume(Q); gap=U-L.
Verify BOTH L<=G<=U and L<=V<=U; do not order G and V.
Retain the signed certificate G-U <= G-V <= G-L, so |G-V|<=gap.
The bounds use geometric areas, never stale supplied marks. T need not lie
between L and U. All supplied marks w_i are positive.

Each level after the first declares exactly one previous-level parent for
every cell. Children are contained in that parent, form a partition of it,
and their supplied marks sum exactly to its supplied mark. Every parent has
children; an unchanged cell is its own single child. Parent representatives
are retired when split. Geometric child areas sum to the parent's area.
The generic API permits a one-child refinement to rename that cell or choose
a new strict-interior representative; fixed-family unchanged cells preserve both.
Do not accept merely global coverage/mark totals as proof of the stated lineage.

Then L_fine>=L_coarse, U_fine<=U_coarse and gap_fine<=gap_coarse.
The signed and absolute representative quadrature errors need not improve.
This is an exact finite enclosure result under declared geometric premises,
not an asymptotic convergence or unknown-metric theorem.

Observation estimates retain AG's three signed errors:
mean - V = (mean-T) + (T-G) + (G-V).
These are sampling bias, annotation error and quadrature error. The geometric
enclosure does not bound the sampling error of an individual retained record.
Do not repair stale marks, fit densities or relabel deterministic errors noise.

## New generic native certificate contract

Both new stdlib modules expose certify(problem).
Input exactly:
{schema_version:"det8-qr05ah-problem-v1",family:"qr05ah_partition_bounds",
 domain:[ul,uh,vl,vh],probes:[{name,bounds}],
 levels:[{name,cells:[{name,parent,bounds,representative,volume}]}]}.

All coordinates and volumes are reduced native fraction pairs [num,den],
positive denominator and at most4096-bit components. Coordinates may be signed;
volumes must be positive. Rectangles have strict positive widths.
representative is [u-pair,v-pair]. Names match [a-z][a-z0-9_]{0,39}.
There are1..4 levels with distinct names in declared order,1..8 cells per
level in increasing cell-name order with unique names, and1..8 probes with
unique names in declared order. Equal probe rectangles are allowed.
First-level parents are null; later parents are exact previous-level cell
names. No extra fields, non-native containers, subclasses, bool/int coercions,
floats, unreduced fractions or implicit geometry conversion.

Output exactly {input_sha256,domain_volume,levels,refinements,counts,scope}.
Each level: {name,cells,questions}; cells is input-cell ordered
[{name,geometric_volume,annotation_error}], where annotation_error=w_i-g_i.
Each probe-ordered question:
{probe,inner_cells,outer_cells,representative_cells,
 lower_bound,upper_bound,boundary_gap,geometric_target,supplied_target,
 continuum_volume,annotation_error,quadrature_error,total_error,
 error_lower,error_upper}.
Membership arrays are increasing cell names.
annotation_error=T-G; quadrature_error=G-V; total_error=T-V;
error_lower=G-U; error_upper=G-L. All scalars are reduced fraction pairs.

Each consecutive refinement:
{coarse,fine,parents,questions}.
parents is previous-cell ordered:
[{parent,children,geometric_volume,supplied_volume}].
children is increasing names; the volumes are the authenticated parent totals.
questions is probe-ordered:
[{probe,lower_gain,upper_drop,gap_drop,quadrature_error_change,absolute_error_change}],
with fine-minus-coarse lower/error values, coarse-minus-fine upper/gap values.
All three gains/drops are nonnegative; error changes may have either sign.

scope has exactly six false flags:
observer_has_geometry,marks_authenticated,unknown_geometry_reconstructed,
monotone_absolute_error_guaranteed,continuum_limit_established,gravity_derived.
Every retained rational is component-bit checked. Internal products may
temporarily exceed that bound and cancel. Outputs are detached; no artifact
reads or mutable cross-call caches.

## Native validation and bounded planning

Live caps:
MAX_BITS4096, MAX_DEPTH64, MAX_NODES131072, MAX_BYTES4194304,
MAX_LEVELS4, MAX_CELLS8, MAX_PROBES8,
MAX_TILE_CHECKS9248, MAX_PAIR_CHECKS112,
MAX_QUERY_CELL_TERMS256, MAX_TOTAL_WORK12000.

Both input and output obey exact ensure_ascii canonical JSON bytes plus newline,
root-zero depth including leaves, expanded native value nodes excluding keys,
bounded strings/width and native types. Reject cycles/exponential DAG expansion,
but admit benign shared containers. Validate before whole serialization.

Parse every field, fraction, rectangle containment, strict representative
interiority and parent-name reference before any computational hook. Compute
the complete conservative plan first. With C_l cells at level l and P probes:
T=sum C_l*(2C_l+1)^2; D=sum C_l*(C_l-1)/2; Q=P*sum C_l;
R=sum C_l over levels after the first; W=T+D+3Q+R.
Check all live caps before partition coverage, refinement sums or query work.
These are conservative canonical logical visits, not CPU-operation counts.

Hooks in both implementations:
_partition(domain,cells), _refinement(coarse,fine), _questions(cells,probes).
Parsed hook argument representations are internal; wrappers may delegate to
the real hook. All partitions and refinements must validate before any
_questions hook runs. No hook runs before full schema parsing and reservations.
counts exactly {levels,cells,probes,tile_checks,pair_checks,query_cell_terms,
refinement_links,total_work}; cells is sum C_l, probes=P, other entries T,D,Q,R,W.
No data-dependent under-reservation, cache reuse after cap changes or hidden
geometry read is permitted.

## Fixed three-level partition family

Level names l0,l1,l2.
l0 is AG's six cells c_i_j on a3-by-2 grid of [0,1]^2:
bounds [i/3,(i+1)/3,j/2,(j+1)/2], i=0..2,j=0..1.
l1 replaces c_1_0 with c_1_0_l and c_1_0_r, split at base u=1/2.
l2 replaces c_1_0_l with c_1_0_lb and c_1_0_lt, split at base v=1/4.
All other cells persist as their own single child. Every NEW base representative
is its cell's arithmetic midpoint. Parent points are retired, not retained
on the split boundary. Marks are fixed before queries and selection.
These prespecified splits cross the unaligned probes' boundary geometry;
their choice is not tuned to computed AH outcomes.

Fixed zero-volume markers and five probes are AG's:
bottom=(0,0), aligned=(2/3,1/2), unaligned=(3/5,2/5), top=(1,1);
whole(bottom,top), lower_aligned(bottom,aligned), upper_aligned(aligned,top),
lower_unaligned(bottom,unaligned), upper_unaligned(unaligned,top).

Five source families, in order: grid,warp,warp_stale,boost,dilate.
Apply each transform to every base cell boundary, its declared base
representative, all probes and the domain:
grid identity; warp/warp_stale (u²,v²); boost (2u,v/2); dilate (2u,2v).
Never recenter in transformed cells.
Supplied marks equal transformed cell area/2 except warp_stale, where they
remain base cell area/2 at each level, an additive but stale annotation.
The true geometric and supplied parent sums are both preserved.

For observation at EACH level assign a fresh original ID map by sorting its
cell representatives plus four markers by (base u+v,base u,base v,label).
Keep that level's map under transforms. Do not claim IDs persist across levels.
Fixed marker IDs are derived from that map; the6/7/8 cell IDs are eligible.
Construct full strict timelike order by t/x inequalities in the runner and
strict u/v comparisons in the independent auditor, then induce each sample.
The old AG schema/caps are unchanged (at most12 events,8 eligible,5 probes).
No finer-source relations or parent-label fields enter an AG packet.

At all three levels run grid and warp with identity,iid_half,singleton, in that
design order; run warp_stale,boost,dilate with identity only.
Case order: source family, then level, then its designs.
For M eligible cells: identity puts1 on the full mask; iid_half gives1/2^M
to every mask; singleton gives1/M to each size1 mask.
Twenty-seven cases and4,032 mask rows, including structural zeros.
These are separate level-specific designs, NOT a coupled/coarsened observation
process across levels. No dynamic transport, conditional refinement law or
coarse-record reconstruction of fine marks is assumed.

## Explicit generic non-monotone countercontrol

Also pass both new certifiers this fixed synthetic two-level input:
domain [0,1]^2; one probe q=[0,1/5]x[0,1];
level a has cell c covering domain, representative(3/4,1/2), mark1/2;
level b has c_l:[0,1/2]x[0,1], representative(1/10,1/2), mark1/4,
and c_r:[1/2,1]x[0,1], representative(3/4,1/2), mark1/4.
Both children name parent c. This is an explicit constructive counterexample
to a general monotone-error claim, not a stochastic experiment or a member
of the main midpoint-generated source family. Retain its complete input/output
and computed strict bound-tightening/absolute-error-increase booleans.

## Private suite, bridges and complete wire

Suite exactly {certificates,cases,controls,prior_bridges,public_controls,totals,scope}.
certificates is source-family ordered [{source,problem,analysis}], each full
new certificate packet and common exact output. Call both new engines and
compare full native bytes against an independent literal source-aware oracle.

Each observation case exactly:
{case_id,level,source,design,population,samples,moments,joint_covariance,counts}.
case_id=source.name+"__"+level+"__"+design.name.
The source/design/population/sample/moment/covariance/count schemas are exactly
AG's private wire, with cell coordinates and marks generated at that level.
No new observer output fields. The runner independently rebuilds all source
moments and the ordered-cell joint-inclusion covariance, rather than importing
AG's runner. Compare T,G,V and signed geometric errors against the matching
new certificate via the declared label-to-ID map.

controls exactly {enclosures,refinement,stale_marks,boost,dilation,counterexample}.
enclosures source-ordered:
{source,sandwiches_hold,annotation_separate,aligned_exact}.
sandwiches checks both full G/V enclosures at every level/probe;
annotation_separate checks all T-G/G-V/T-V identities, not T enclosure.
aligned_exact checks L=U=G=V for the first three probes at all levels.
refinement source-ordered:
{source,lower_nondecreasing,upper_nonincreasing,gap_nonincreasing,
 all_absolute_errors_nonincreasing,absolute_error_changes}.
Last list is consecutive-refinement order then probe order of exact changes.
stale_marks level-ordered:
{level,geometric_certificate_equal_warp,public_samples_equal_base,
 annotation_errors}. First compares all geometric fields/memberships/refinement
values after removing supplied-target/annotation/total-error and supplied parent
mark totals; public comparison is on identity case's complete sample wires;
annotation_errors is probe-ordered T-G.
boost/dilation each {volume_factor,complete_certificate_scaling,
 complete_observer_scaling,complete_moment_scaling}.
Check all levels using identity samples; include new cell/parent marks,
all question scalars and refinement gains/errors, not only one selected probe.
factor1/4 respectively; covariance scales by factor squared.
counterexample {problem,analysis,bounds_tightened,absolute_error_increased}.

prior_bridges exactly {AG_level0_case_ids,AG_level0_complete_cases_equal,
 AG_other_math_replayed:false}. List the nine matching AG case IDs in AH case
order. Drop AH's level field and restore AG's case_id to compare the entire
level0 case against authenticated AG JSON, including original packets and all
moments/controls internal to those case objects. Do not claim a new full AG or
forecasting-suite replay.

public_controls exactly {certificate_calls,observer_calls,
 independent_certificate_routes_equal,independent_observer_routes_equal,
 invalid_certificate_calls_rejected}. There are12 certificate calls (five
families and countercontrol through two routes). Use eight malformed certificate
inputs against both routes: extra field, unreduced mark, representative on cell
boundary, missing cell, overlapping cell replacing another (gap+overlap),
unknown parent, nonadditive child marks, outside probe. Require16 rejections.
totals contains cases plus sums of each observation counts field.
scope allfalse:
unknown_geometry_reconstructed,continuum_limit_established,
marks_authenticated,observer_bounds_inferred,monotone_absolute_error_guaranteed,
cross_level_observation_transport_proved,quantum_channel_constructed,
gravity_derived,empirical_data_used,ret_integration_tested.

## Freeze and verification

Pin AG results.json:3,027,867 bytes, SHA256
5af957be534af3096c7f61ec444349ec49c739ebf70364146b7f4568a8832f91,
and its37 prior captures:38 total. Authenticate AG's seven-source ledger before
loading its two reused observers and during independent raw audit.
Only the stated nine AG level0 cases are consumed mathematically.
Preserve all other results/claim boundaries by identity, not pretend replay.

Freeze seven AH sources: README.md,certificate.py,reference_qr05ah.py,study.py,
test_qr05ah.py,test_capture.py,audit_json.py. New independent engines share no
executable implementation; each may statically carry its own native guard.
The auditor imports no AH/AG engines, runner or tests; independently reconstruct
the new certificates, overlap/partition/lineage proof, source sampling,
all errors/covariances/controls and consumed AG bridges. Its inventory is
seven AH +38 prior +seven AG source identity targets, plus current capture.

Before fixed calculations freeze this protocol, complete generic hands and
record four protocol/implementation identities. Disclose any later rule,
fixture or implementation correction. Freeze all seven sources before external
create-only preflight, independent audit, full normal/-O tests, exclusive final
capture, fresh read-only exact replays and raw audit. Keep identity bytes unchanged.
Use isolated Python and fresh external bytecode caches; no dependency installs.
Capture cap64MiB, working-suite cap128MiB, retained component cap4096bits.
Never overwrite/follow symlinks for evidence; temporary lifecycle tests only.
RESULTS.md and roadmap remain outside the frozen ledger. Standard whitespace
checks should pass before freezing the protocol; do not reformat captured bytes.
