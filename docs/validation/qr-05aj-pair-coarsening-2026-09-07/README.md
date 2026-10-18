# QR-05AJ protocol: additive cell-pair geometry across scales

7 September 2026. Prospective protocol, before fixed AJ calculations.
Base: pushed AI commit e77482fccb3d72ab21f1b50ebbb4aee632a7831d.
Prior research, RET/core work, dependencies and temporary model sheets stay unchanged.

## Question and boundary

Can the supplied two-point causal measure be aggregated exactly across the
existing three nested partitions? Compare all ordered parent-cell pairs with
their complete child blocks, including within-child and same-parent cross-child
terms. Test normalized conditional fractions with their actual geometric
product-volume weights, not uniform or annotation-derived substitutes.

This is a PRIVATE bounded exact diagnostic, not a production API. Geometry is
supplied, not inferred from representative order or observations. No sampling
law is rerun or transported, no RET/Lean integration is undertaken, and no
metric reconstruction, quantum channel, continuum limit or gravity is claimed.
The same geometry is already present in AI; this gate tests its scale accounting.

## Inputs and independent computation

Read the authenticated AI artifact, selecting ONLY the identity-design source
data for grid, warp, warp_stale, boost and dilate, in that order, at l0,l1,l2.
No new split, geometry, probe or event numbering is introduced. Each family
has 6,7,8 cells and the five existing probes in their original order.
No observed masks, previous pair answers or historical engines enter the new
mathematical engines. The runner separately compares their computed geometry
with all consumed AI pair rows and clipped volumes.

The engine input problem has exactly
{family,probes,levels}, where probes are [{name,bounds}] and levels are
[{level,cells}], cells [{event,bounds,supplied_mark}]. Bounds are
[u_low,u_high,v_low,v_high]. The root runner projects these from authenticated
AI coordinates/cells, checking the probe bounds agree at all three levels.
Supplied marks are retained ONLY to test an incorrect weighting candidate;
they do not determine the geometric measure or the correct weights.

Each independently written stdlib engine exposes build_family(problem) and
causal_area(a,b,c,d), the directed integral over x in [a,b], y in [c,d] of
1(x<y). Primary uses an exact positive-part integral; reference integrates
piecewise affine overlap lengths. Neither imports the other or reads files.
Both independently validate full rectangles, derive lineage, clip cells,
integrate every pair, form all block sums and normalize them.

Trusted native inputs are bounded to exactly three distinct level labels,
1..8 positive cells per level and 1..5 positive rectangular probes. Family,
level and probe labels are nonempty native strings; probe names are unique.
Cells are event-ordered with unique native integer IDs (signed IDs allowed)
within a level. Supplied marks
are positive. Cell interiors must be disjoint, and their clips must cover
every query. IDs are level-local: equal IDs at different levels do NOT mean
the same cell. No generic adversarial resource-safety claim is made.

## Measure and lineage

Use strict product order x≺y iff u_x<u_y AND v_x<v_y, with dmu=du dv/2.
For probe Q and full cell A_i, let h_i=mu(A_i intersect Q) and
J_ij=integral_(A_i intersect Q)x(A_j intersect Q) 1(x≺y) dmu(x)dmu(y).
Empty clips give h=0 and J=0. J factorizes as one quarter of the two directed
one-dimensional integrals. Retain all ordered pairs, not just causal
representatives, and require sum_ij J_ij=mu(Q)^2/4.

Derive parentage from unique FULL-rectangle containment before clipping.
For each of (l0,l1),(l1,l2),(l0,l2), every child has exactly one parent;
each parent has children contained in it whose geometric areas sum to its
area. Check disjointness, not only total areas. Verify the direct l2-to-l0
map equals the composed l2-to-l1-to-l0 map. No mark or event-ID matching.

For every query and ordered parent pair (A,B), verify

    h_A = sum_(a child of A) h_a,
    J_AB = sum_(a child of A,b child of B) J_ab.

Retain diagonal-child sum (a=b) and off-diagonal-child sum (a!=b) separately.
For A=B the second term includes same-parent cross-child pairs. A positive
rectangular cell has J_AA=h_A^2/4: this measures two distinct continuum points
in a region, NOT a self-preceding event or the zero-measure locus x=y.

## Conditional fractions and deliberately incorrect candidates

If h_A*h_B>0, define C_AB=J_AB/(h_A*h_B). Otherwise C_AB is JSON null,
explicitly undefined, not zero or a silently filled ratio. For a positive
parent product, geometric child weight is h_a*h_b/(h_A*h_B). It is zero for
zero child products; their undefined C_ab contributes zero without division.
Verify C_AB=sum_ab geometric_weight_ab*C_ab.

Keep two comparison candidates, with no requirement that they fail everywhere:

1. unweighted_child_conditional: average C_ab over positive-volume child pairs.
2. annotation_weighted_child_conditional: put s_a=w_a*h_a/g_a, where g_a is
   full true cell volume and w_a its supplied mark; normalize s_a*s_b over
   the complete block and weight the defined C_ab. This is a declared clipped
   annotation heuristic, not another geometric measure. It agrees with true
   weighting when all w_a=g_a, and may fail with stale marks.

If no positive child pair exists, both candidates are null. Retain every
candidate equality and discrepancy through the exact numeric values; do not
present unchanged blocks as evidence of general validity.

For the direct l0,l2 link, also aggregate the l1,l2 blocks through the independently
derived l0,l1 map. Use middle volumes reconstructed by sums of l2 volumes;
normalize intermediate reconstructed measures, then combine with these middle
product-volume weights. Compare resulting integrals and conditional fractions
with direct l0,l2 aggregation. Adjacent-link via-middle fields are null.

## Exact output contract

Rationals are reduced native [numerator,positive_denominator] pairs. JSON null
marks undefined conditional quantities. No floats in the mathematical suite;
native scalar integer components at most4096bits. Canonical JSON: sorted keys,
compact separators, ensure_ascii, trailing newline. Inputs/outputs are detached.

build_family returns exactly {problem,levels,coarsenings,counts}.
problem is the unmodified detached input.
levels is [{level,geometry}]. Geometry follows probe order, each exactly
{probe,volume,cells,pairs}. Cells are [{event,clipped_volume}]. Pairs follow
the complete event-ordered Cartesian product and are exactly
{first,second,clipped_product,causal_integral,conditional}.

coarsenings follows index links (0,1),(1,2),(0,2). Each exactly
{coarse,fine,parents,geometry}; parents are [{parent,children}] in coarse
event order, child IDs in fine event order. Each geometry row is
{probe,volumes,blocks}; volumes are [{parent,coarse_volume,child_volume_sum}].
Blocks follow the full coarse Cartesian product and have exactly:

    first, second, children, coarse_integral, child_integral_sum,
    child_diagonal_integral, child_offdiagonal_integral,
    coarse_conditional, weighted_child_conditional,
    unweighted_child_conditional, annotation_weighted_child_conditional,
    via_middle_integral, via_middle_conditional.

children follows the complete Cartesian child block; each row exactly
{first,second,geometric_weight,annotation_weight}. Weights are null only if
their whole parent block denominator is zero, otherwise exact rationals.
They include zero weights; no diagonal, reverse direction or zero row omitted.

counts exactly {levels,probes,level_pairs,blocks,child_terms,
undefined_level_pairs,undefined_blocks,unweighted_mismatches,
annotation_mismatches,diagonal_omission_mismatches,cross_child_omission_mismatches}.
The last two count blocks where child_offdiagonal_integral or
child_diagonal_integral, respectively, differs from coarse_integral. They
describe incorrect omitted-term candidates, not experimental failure rates.

Suite exactly {families,controls,prior_bridges,composition_witness,totals,scope}.
Families follow the input family order; totals sum each family count and add
families=5. Controls compare complete geometry/coarsening wires (not just
selected entries): boost equals grid, dilation scales volumes by4 and pair
integrals by16 while fractions/weights are unchanged, and warp_stale equals
warp geometrically except annotation weights/candidate values and input marks.
Counts tracking annotation mismatches are excluded ONLY from that last equality.

prior_bridges retains the 15 consumed AI identity case IDs and true booleans
for exact projected input equality and complete clipped-volume/pair-table
equality. No AI sampling mathematics or other prior mathematics is replayed.

## Composition boundary: analytic control, not the next gate

A separate one-unit-rectangle hand control has volume h=1/2. For independent
uniform X,Y,Z, P(X≺Y)=1/4, whereas P(X≺Y≺Z)=(1/3!)^2=1/36. The latter
also follows by integrating u(1-u)v(1-v) over the middle point. Squaring
the pair fraction instead gives1/16 because it redraws the intermediate point.
The dimensionally matched measures J^2/h=h^3/16 and h^3/36 differ.
composition_witness records h, pair_fraction, squared_pair_fraction,
shared_middle_fraction, pair_measure, block_product_measure,
shared_middle_measure and signed_product_error, with these field names.
Root computes the analytic wire; generic independent integral tests verify it.
This is not a fixed-family higher-chain experiment or third production engine.

The one-entry conditional matrix has row sum1/4, not1; row-normalizing it to1
would change the statistic. Region conditionals are not a strict event order
or automatically transition probabilities. Exact pair block additivity does
NOT establish matrix-power/higher-chain composition closure.

scope flags all false: generic_production_API_hardened,
unknown_geometry_reconstructed,marks_authenticated,continuum_limit_established,
cross_level_observation_transport_proved,higher_chain_composition_closed,
stochastic_transition_constructed,quantum_channel_constructed,gravity_derived,
empirical_data_used,ret_integration_tested.

## Verification and evidence lifecycle

Pin AI results.json:14,980,342bytes, SHA256
17dbb103c56b6489d5aef75f4eda77108fea12bfc475fc65ffcfd82710bf6786.
Authenticate AI's39 prior captures as40 total, its five sources, and all14
ancestor sources already authenticated there. Replay only the stated AI
geometry projections. No historical mathematical engine is imported.

Freeze README.md,kernel.py,reference.py,study.py,test_qr05aj.py before fixed
execution. Engines/tests may run generic synthetic hands beforehand, but no
fixed AJ build_family until root explicitly releases the comparison. Complete
exact two-engine comparisons, independent generic oracles, malformed nested
partitions, input detachment, changed zero/diagonal/reverse/normalization rows,
control/projection mutations, and capture lifecycle must be exercised.
Any post-first source/protocol correction must be disclosed, not silently hidden.

Use isolated Python with external fresh bytecode caches, normal and optimized
test runs, no dependency installations or unrelated edits. Capture cap64MiB,
working native suite cap96MiB. Identity checks bracket executions. After first
comparison, use an external create-only preflight, exclusive final capture,
then fresh read-only primary and reference replays. Never overwrite evidence
or follow final-file symlinks. Runtime metadata is outside mathematical data.
This private runner is not a generic untrusted-JSON admission boundary.
RESULTS.md and the research roadmap are outside the frozen ledger.
Publication includes only this gate directory and the research roadmap.
