# QR-05AL protocol: breakpoint-aware middle moments

7 September 2026. Prospective protocol before fixed AL mathematics.
Base: pushed AK commit 8527e35b565e2005e918209f125efd8bd8c9de1f.
All previous research, RET/core work and dependencies remain unchanged.

## Question and scope

On AK's supplied rectangular partitions, test an explicit finite moment contract
for the declared incoming/outgoing causal-volume functions. Does contracting
piecewise bilinear coefficients against shared-middle raw moments reproduce
direct pair/triple integration? Separate the effect of breakpoint subdivision
from that of within-tile dependence using two mean-only controls. Count the
whole contract payload. This is not an unknown-geometry reconstruction, minimal
encoding theorem, constant-size universal summary, continuum limit, stochastic
transition, quantum channel, ontology claim, gravity derivation or RET interface.
It is a PRIVATE bounded exact research diagnostic, not a hardened public API.

## Inputs, independent engines and geometry

Authenticate AK results and project ONLY its five problem inputs, in order
grid, warp, warp_stale, boost, dilate. They are already geometry-only:
{family,probes,levels}, probes [{name,bounds}], levels [{level,cells}],
cells [{event,bounds}]. Do not pass old computed answers, parent maps, marks,
observations, old source engines or proposed coefficients to either new engine.
No fixture, probe, level, split, coordinate or event-ID changes are allowed.

Each stdlib engine exposes build_family(problem) and rectangle_moments(bounds).
The latter accepts four native rational pairs for a positive rectangle and
returns the nine reduced raw moments in the ordering specified below.
Primary constructs exact polynomial coefficients and tensor antiderivative
moments, then uses moment contractions for pair/triple results. Reference uses
independent corner interpolation for coefficients and exact tensor-Simpson
integration for moments and direct clamp pair/triple/centered integrals; it
checks its contractions against those direct integrals. They may not import
each other or historical engines, or read stored answers. Caches, if used, are
local to one build and keyed by geometry. Generic hands precede fixed execution.

Native inputs: exactly three distinct nonempty level labels, 1..8 positive
rectangular cells per level, 1..5 positive rectangular probes with unique
nonempty names, and a nonempty family string. Bounds are [u0,u1,v0,v1], each
coordinate a reduced [numerator,positive_denominator] native integer pair.
Event IDs are sorted unique native integers within a level; signed and
reassigned IDs are allowed. They are level-local region labels, not points.
All retained integer components are at most 4096 bits; reject booleans as IDs
or rational components, unreduced/float coordinates, duplicate/unknown fields.
Cell interiors are disjoint and clips cover each query. Derive full-rectangle
parenthood on links (0,1),(1,2),(0,2), before clipping; each child has one parent,
children cover every full parent, and direct/composed lineage agrees.
Inputs and outputs must be detached native structures. No floating mathematics.

Use dmu=du dv/2 and strict product order in u,v. For clipped A,B,C define h_A,
J_AB and T_ABC as in AK: cell volume, directed pair measure and shared-middle
three-point measure. Repeated region labels do not identify continuum points.
Retain every ordered pair/triple, including repeats, reverse IDs and empty clips.
Require sum J=V^2/4 and sum T=V^3/36 for each rectangular query of volume V.

## Shared breakpoint grid and exact moment contract

Use GLOBAL supplied coordinates, not a different untransported basis per tile.
For each (level,probe,middle B), start with B's clipped boundary coordinates.
Insert every u or v endpoint of EVERY nonempty clipped endpoint region at that
level that lies strictly inside the corresponding middle coordinate interval.
These are the full declared endpoint family, shared across all (A,C), not a
triple-specific grid or an error-selected refinement. Deduplicate and sort.
Take every positive Cartesian tile, u interval outer and v interval inner.
Tiles have disjoint interiors and cover clipped B; at most 289 per middle.
An empty middle has no tiles, no breakpoints, null bounds and nine zero moments.

For one coordinate, incoming length is clamp(y-a,0,b-a), outgoing length is
clamp(d-y,0,d-c). On each tile these functions are affine. Their two-coordinate
products divided by 2 are the incoming and outgoing VOLUMES L_A and R_C.
For phi=(1,u,v,uv), retain all four coefficients of each L_A and each R_C,
including zeros and all endpoint IDs in order. An empty endpoint has four zero
coefficients. No coefficient may omit the geometric 1/2 normalization.

Retain M_ij=integral_tile u^i v^j dmu for i,j in {0,1,2}, ordered i outer,
j inner: (00,01,02,10,11,12,20,21,22). Odd moments may be negative.
For basis exponents e=((0,0),(1,0),(0,1),(1,1)), form

    m_a = M_(e_a),       G_ab = M_(e_a+e_b),
    J_AB(tile) = ell_A^T m,    J_BC(tile) = r_C^T m,
    T_ABC(tile) = ell_A^T G r_C.

G is the 4-by-4 raw Gram matrix DERIVED from nine moments, not 16 new payload
numbers. Nine raw moments are not nine independent geometric parameters or a
proved minimum. Check contractions, G symmetry/repeated entries, G_00=h_tile,
and the centered matrix G-mm^T/h_tile's zero constant row/column. Generic hands
also test positive quadratic forms and affine basis transformations. Sum tile
moments to independently computed whole-middle moments in the same global basis.

Sum tile pair/triple integrals to obtain J and T. For h_B>0 define

    P = J_AB*J_BC/h_B,
    P_tile = sum_t J_At*J_tC/h_t,
    original_error = P-T,
    tile_error = P_tile-T,
    between_error = P-P_tile,
    original_error = tile_error + between_error.

These are original-middle and tilewise mean-only controls using the SAME
functions and declared tiles. Do not assume a sign, strict improvement or
monotonicity in acceptance. Also compute centered_integral by integrating
(L_A-J_AB/h_B)*(R_C-J_BC/h_B) over B, and within_tile_centered_integral by
centering independently in each tile and summing. In primary use centered
coefficient contractions; reference directly integrates centered clamps.
Require centered_integral=T-P, within_tile_centered_integral=T-P_tile and
middle_covariance=centered_integral/h_B. The centered contractions share the
same moments; they are consistency checks, not a third independent engine.

If h_B=0, J and T remain zero but P,P_tile, their errors, both centered
integrals and middle covariance are null. If h_B>0 but an endpoint is empty,
all these raw values are valid zeros. T/(h_A*h_B*h_C), P/(h_A*h_B*h_C) and
P_tile/(h_A*h_B*h_C) are null unless the full product is positive. Aggregate
product sums explicitly skip zero-middle nulls as zero-measure terms; this does
not turn individual undefined ratios into zeros.

## Exact mathematical output wire

Every mathematical rational is a reduced native [n,d] pair, d>0, at most
4096 bits per component. Lists/dictionaries are detached. Canonical JSON uses
sorted keys, compact separators, ensure_ascii, no NaN and a terminal newline.
Build returns exactly {problem,levels,coarsenings,counts}.

levels follows input order: [{level,geometry}]. geometry follows probe order,
each exactly {probe,volume,cells,middles,pairs,triples,summary}.
cells is [{event,clipped_volume}] in input ID order.
middles has one row per cell ID, exactly
{event,bounds,u_breaks,v_breaks,moments,tiles}. Nonempty bounds is its clipped
rectangle; moments is its nine whole-middle moments. tiles follows grid order,
each {bounds,moments,incoming,outgoing}; incoming/outgoing each has EVERY endpoint
row {event,coefficients}, coefficients in (1,u,v,uv) order. No Gram matrix is
serialized, since it is recoverable from the raw moment list.

pairs uses complete first-outer/second-inner ID order and exactly AK fields:
{first,second,clipped_product,causal_integral,conditional}.
triples uses complete first-outer/middle/last-inner order, exactly:

    first, middle, last, volume_product, causal_integral,
    pair_product, product_error, conditional, product_conditional,
    middle_covariance, tile_pair_product, tile_product_error,
    between_tile_error, tile_product_conditional,
    centered_integral, within_tile_centered_integral.

The first ten named fields project to AK exactly. summary exactly
{true_integral,continuum_integral,original_product_sum,tile_product_sum,
original_error,tile_error,between_error}.

coarsenings follows (0,1),(1,2),(0,2), each exactly
{coarse,fine,parents,geometry}; parents [{parent,children}] in ID order.
Each geometry item exactly {probe,moment_blocks,blocks}. moment_blocks has one
row per coarse cell {parent,children,coarse_moments,child_moment_sum}, retaining
all nine moments and checking exact child additivity in common coordinates.
blocks retains EVERY ordered coarse triple with complete Cartesian children:
{first,middle,last,children,coarse_integral,child_integral_sum,via_middle_integral}.
True integrals add exactly. Direct l0-to-l2 also sums l1-to-l2 true blocks through
the l0-to-l1 map; adjacent via_middle_integral is null, direct is rational even
when zero. No cross-level identity is assumed for either mean-only product.

Counts exactly:

    levels, probes, level_pairs, level_triples, blocks, child_terms,
    middle_cells, positive_middle_cells, tiles, breakpoint_entries,
    middle_bound_entries, tile_bound_entries,
    middle_moment_entries, tile_moment_entries,
    coefficient_vectors, coefficient_entries,
    coarsening_moment_blocks, coarsening_moment_entries,
    zero_middle_level_triples, undefined_level_conditionals, positive_triples,
    original_positive_errors, original_zero_errors, original_negative_errors,
    tile_positive_errors, tile_zero_errors, tile_negative_errors,
    between_positive_errors, between_zero_errors, between_negative_errors.

Payload entry counts include repeated serialized values, not unique numbers:
middle_bound_entries=4*positive_middle_cells; tile_bound_entries=4*tiles;
middle_moment_entries=9*middle_cells; tile_moment_entries=9*tiles;
coefficient_vectors=sum_tiles 2*N_level; coefficient_entries=4*vectors;
breakpoint_entries=sum_middle(len(u_breaks)+len(v_breaks));
coarsening_moment_entries=18*coarsening_moment_blocks (both retained vectors).
Do not count derived G entries as transmitted data. Error sign counts exclude
nulls; zero_middle_level_triples records their number. positive_triples means T>0.

## Suite, transformations, prior bridges and payload sizes

Suite exactly {families,controls,prior_bridges,payload_sizes,totals,scope}.
families fixed order above; totals sum all counts plus families=5.
controls exactly {boost:true,dilation:true,stale_geometric:true} only after
complete transformed family comparisons, including problem bounds (family label
excluded), coefficients, raw moments, breakpoints, geometry and coarsening.
Warp_stale equals warp after dropping ONLY the input family label.

For boost (u',v')=(2u,v/2) and dilation (2u,2v), let alpha,beta be the coordinate
scales and k=alpha*beta. Bounds/breakpoints scale by coordinate; raw moment M_ij
scales by k*alpha^i*beta^j; bilinear coefficient at u^i v^j scales by
k/(alpha^i*beta^j). Volumes scale by k, pairs/covariance by k^2 and triple
measures/products/errors/centered integrals by k^3. Normalized fractions, IDs
and counts stay unchanged. Raw moment and coefficient wires are NOT themselves
boost-invariant. Generic translated affine hands must use binomial moment
transport and corresponding coefficient transport, not simple homogeneity.

prior_bridges exactly {AK_family_names,AK_projected_inputs_equal,
AK_complete_clipped_volumes_pairs_triples_equal,AK_true_coarsening_equal,
other_AK_math_replayed:false,other_prior_math_replayed:false}.
Verify every complete AK input, clipped volume, pair, ten-field triple projection
and the seven-field true coarsening-block projection (including parents).
Other AK fields and older math are identity-only, not rerun. No marks are used.

payload_sizes is a five-row list in family order, each exactly
{family,native_family_bytes,moment_contract_bytes}. Native size is canonical
family JSON. Contract size is canonical [{level,geometry:[{probe,middles}]}]
over all levels/probes, retaining all middle bounds/breakpoints/moments/tiles and
every coefficient vector, with labels. This explicitly redundant research wire
is not a compression benchmark. Full family bytes also include problem inputs,
pair/triple results, coarsening witnesses and counts; state both sizes.

Scope flags all false: generic_production_API_hardened,
unknown_geometry_reconstructed,minimal_encoding_proved,universal_query_closure,
arbitrary_dynamics_closure,continuum_limit_established,marks_authenticated,
stochastic_transition_constructed,quantum_channel_constructed,gravity_derived,
empirical_data_used,ret_integration_tested,lean_verification_performed.

## Verification and publication discipline

Pin AK results: 16,462,744 bytes, SHA256
15fce56375af7e44bfc2f955559c55628c77338d11a1911161c4e3bb6f038db4.
AK plus its 41 prior captures gives 42 retained prior artifacts. AK's five
sources plus its 24 ancestors gives 29 ancestor sources. With five AL sources,
authenticate 76 targets. No old engine imports; replay only declared AK bridges.

Freeze README.md,kernel.py,reference.py,study.py,test_qr05al.py before ANY fixed
AL build. Generic synthetic verification and independent source review precede
that freeze; root explicitly releases fixed execution. Unit tile controls,
translated nonsquare moments, negative odd moments, positive Gram forms,
centered constant rows, affine transport, signed/reassigned IDs, empty middle
versus empty endpoint, unequal splits, breakpoint-only versus full-moment
controls, all coarsening moments, full payload accounting and detachment are
required. Use complete independent family-oracle comparisons and non-noop
mutations, normal and optimized tests with explicit exception guards.

Use isolated Python with fresh external bytecode caches, no dependency changes.
Follow first comparison, independent read-only reference audit, external
create-only preflight, exclusive final capture and fresh read-only final
primary/reference replays. Bracket with all source/prior identities and preserve
final bytes. Disclose every source/protocol/fixture correction after first fixed
math. Capture cap 128 MiB; native serialized working suite cap 192 MiB. Bounds
on dimensions/counts are private diagnostic limits, not a complete adversarial
resource contract. Never overwrite evidence or follow final-file symlinks.
Runtime is outside mathematics; RESULTS.md and roadmap are outside frozen ledger.
Publication includes only this gate directory and the research roadmap.
