# QR-05AN protocol: degree-aware four-point composition

8 September 2026. Prospective before fixed AN mathematics.
Base: pushed AM commit 0e65df824a7e19d5b6420036d5e98f5a6073d81a.
Prior research, RET/core changes, dependencies and temporary sheets stay untouched.

## Question and fixed boundary

Does one further causal integration admit an explicit higher-degree finite
representation on the same supplied rectangular geometry? Preserve the coupling
of TWO intermediate points. Test a corner-bilinear truncation of the propagated
field separately from a product-of-means control. Count the complete contract,
not just sixteen raw moments. This is a PRIVATE bounded exact diagnostic, not
a production API, physical propagation law, universal fixed-degree closure,
minimal encoding, unknown-geometry reconstruction, ontology or gravity proof.

Authenticate AM. Select ONLY grid and warp, in that order, the whole probe,
and levels l0,l1,l2 with 6,7,8 region IDs. Project their original input contexts:
engine problem exactly {family,probes,levels}, probes [{name,bounds}], levels
[{level,cells}], cells [{event,bounds}]. The whole-probe middle bounds become
cell bounds, without coordinate/ID changes; verify they are positive. Probe
bounds come from the same context and must agree across levels. No AM moments,
tiles, endpoint queries, coefficients or computed answers enter either engine.
No fixed transformed, stale or partial-probe families are added. Generic tests
cover those mathematical edge cases and affine transport separately.

Exactly 298 pair rows, 2,142 triple rows and 15,586 quadruple rows follow from
this fixed inventory, before any new integration. Every ordered tuple remains,
including repeats, reverse numerical IDs and zero measures. Region IDs are
level-local labels; repeating a region does not identify its continuum points.

Generic native admission: exactly three distinct nonempty level labels; 1..8
positive rectangular cells per level with sorted unique signed native integer
IDs; 1..3 positive rectangular probes with unique nonempty names; nonempty
family string. Each full level's cell interiors are disjoint. Clips cover
each probe. Derive full-rectangle parenthood on (0,1),(1,2),(0,2) BEFORE
clipping: each child lies in exactly one parent, children cover each full parent,
and direct/composed lineage agrees. Probe clipping may produce empty cells.
Bounds are native four-coordinate lists of reduced rational pairs [n,d], d>0.
Every retained integer component has at most 4096 bits. Reject booleans in
numeric input, floats, unreduced rationals, unknown/missing fields and non-native
types/subclasses. Valid shared native input containers are allowed; outputs
must be detached. No complete hostile-graph/resource-hardening claim.

## Mathematics, independent routes and common grid

Both independent stdlib modules expose build_family(problem) and
rectangle_moments(bounds), the latter accepting a positive native rectangle
and returning SIXTEEN rational moments. Null empty clips are internal only;
rectangle_moments(None) must be rejected.
No cross-imports, historical executors, stored answers or hidden file reads.
Caches are local to one build and keyed by explicit geometry/data.

Use dmu=du dv/2 and strict product order in u,v. Clip every region ONLY to
the common probe Q. In particular, do NOT preclip A or B to the third region C.
With nonnegative predecessor/successor volumes L_A(y),R_D(z), define

    F_AB(z) = integral_B L_A(y) 1[y precedes z] dmu(y),
    J_CD = integral_C R_D(z) dmu(z),
    T_ABC = integral_C F_AB(z) dmu(z),
    U_ABCD = integral_C F_AB(z) R_D(z) dmu(z).

For coordinate intervals A=[a0,a1], B=[b0,b1], set
H_A(t)=((t-a0)_+^2-(t-a1)_+^2)/2 and
f_AB(t)=H_A(clamp(t,b0,b1))-H_A(b0).
Then F_AB(u,v)=f_AB(u)f_AB(v)/4, using the respective axis intervals.
An empty A or B gives zero F; empty D gives zero R. F is piecewise
degree at most two in EACH coordinate, not necessarily total degree two.

For each (level,probe,third region C), form one shared grid: start with C bounds,
insert all coordinates of ALL nonempty clipped cells strictly inside C's
corresponding axis intervals, deduplicate/sort, and take every positive Cartesian
tile, u interval outer/v inner. This includes all A/B/D branch boundaries.
Do not choose grids from observed errors; inactive cuts remain. At most 289
tiles per C. Empty C has null bounds, empty breaks/tiles and sixteen zero moments.

Use a GLOBAL monomial basis: propagated coefficients ordered (i,j), i outer,
j inner, i,j=0..2 (nine entries). Outgoing and forced coefficients use the
older four-entry order (1,u,v,uv). M_ij=integral_tile u^i v^j dmu, i,j=0..3,
i outer/j inner (sixteen entries). Coefficients, moments and whole-C moment
sums must retain zeros and signed values, in a common coordinate system.

The exact cross-moment contraction is 9-by-4:

    T_ABC(tile) = sum_(i,j=0..2) f_ij M_ij,
    U_ABCD(tile) = sum_(i,j=0..2),(k,l in 00,10,01,11)
                       f_ij r_kl M_(i+k,j+l).

Sixteen distinct raw entries suffice for this declared tensor contract; they
are not sixteen independent geometric parameters or a proved minimum.
J_CD uses outgoing coefficients and the same moments. Sum tiles to get J,T,U.
Require complete partition identities for probe volume V:
sum J=V^2/4, sum T=V^3/36, sum U=V^4/576.

Primary derives branch-polynomial coefficients from the clipped primitives and
uses tensor antiderivative moments plus exact contractions. Reference recovers
propagated coefficients by tensor quadratic interpolation of independent
ordered-pair volumes at tile nodes, and outgoing/forced coefficients by corner
interpolation. Reference moments use exact tensor-Simpson integration through
degree three. It verifies exact contracted J,T,U against independently ordered
interval-atom simplex integrals for two/three/four points, and may also check
piece quadrature. Strict ordering within a shared atom contributes width^m/m!,
not an exclusion of repeated region labels. The two axes contribute the
appropriate 1/2^number_of_points normalization.

## Two controls, structural admission and nulls

For each (A,B,C,tile), retain the FORCED four-corner bilinear interpolant
of F_AB, not the polynomial formed by simply discarding high-degree monomials.
This geometric interpolation transports under affine coordinates; deleting
global coefficients generally does not. Contract forced F with the original
tile moments and exact R. Also retain its integral over C in the triple row.

A propagated polynomial is bilinear iff every coefficient with i=2 OR j=2
is zero. This is an exact polynomial certificate on a positive tile.
Record bilinear_admissible for each propagated tile row; a triple/quadruple's
propagated_bilinear is true iff all its C-tile fields are bilinear (vacuously
true for empty C). Assess the field independently of outgoing support:
Classify field admission structurally, not by testing U=forced_U.

Prospective branch-local fact: on this complete breakpoint grid, the
one-dimensional f_AB factors are nonnegative constant/affine/convex-quadratic
functions. Their secants majorize them, so the corner-bilinear forced F is a
pointwise upper bound, and forced_U-U>=0. Check that inequality, retaining all
signed rational errors and equalities. Do not generalize it to grids missing
B's saturation breakpoint or arbitrary incoming fields. A positive strict error
is not required in every row. Field nonbilinearity and zero weighted error can
coexist when outgoing support hides the nonlinear tiles.

For h_C>0, define P=T_ABC*J_CD/h_C, mean_error=P-U,
third_covariance=(U-P)/h_C. Compute centered_integral by actually centering
F_AB and R_D by their whole-C means before integrating, not by renaming U-P;
verify centered_integral=U-P. Primary uses centered coefficient contractions;
reference directly integrates centered functions on tile quadrature nodes.
The covariance has volume degree three, centered integral degree four.
Do not infer stochastic transitions, associativity of projected products or
arbitrary dynamics closure from exact representation of this declared query.

If C is empty, raw J,T,U and forced integrals/errors are zero, but P,
mean_error,covariance,centered_integral are null. If A,B or D is empty while
C is positive, raw U and P are valid zeros. An empty A/B does not make J_CD
zero. Full normalized U,forced_U,P divide by h_A*h_B*h_C*h_D only when positive.
Triple normalized T/forced_T divide by h_A*h_B*h_C; pair J divides by h_C*h_D.
No normalization across undefined denominators. Aggregate P skips null
zero-C terms as zero-measure contributions, without changing row-level nulls.

## Complete output wire

Return exactly {problem,levels,coarsenings,counts}.
levels [{level,geometry}], each geometry exactly
{probe,volume,cells,middles,pairs,triples,quadruples,summary}.
cells [{event,clipped_volume}] in input ID order.
middles [{event,bounds,u_breaks,v_breaks,moments,tiles}], one per third-region ID.
tiles [{bounds,moments,propagated,outgoing}] in grid order.
propagated has EVERY ordered (A,B), A outer/B inner:
{first,second,coefficients,forced_coefficients,bilinear_admissible}.
outgoing has EVERY D: {event,coefficients}.
Store these vectors once per tile, not repeatedly in quadruple rows.
No derived 9-by-4 cross-moment matrix is transmitted as extra data.

pairs in first-outer/second-inner ID order:
{first,second,volume_product,causal_integral,conditional}.
triples in first/second/third order:
{first,second,third,volume_product,causal_integral,forced_integral,forced_error,
conditional,forced_conditional,propagated_bilinear}.
quadruples in first/second/third/last order:
{first,second,third,last,volume_product,causal_integral,forced_integral,
forced_error,mean_product,mean_error,conditional,forced_conditional,
mean_conditional,third_covariance,centered_integral,propagated_bilinear}.
Triple/quad forced_error always means forced minus exact.
summary exactly {pair_integral,pair_continuum_integral,triple_integral,
triple_continuum_integral,quadruple_integral,quadruple_continuum_integral,
forced_integral,forced_error,mean_product,mean_error}.
The last four summary fields refer to quadruples.

coarsenings on links (0,1),(1,2),(0,2), each
{coarse,fine,parents,geometry}; parents [{parent,children}] in ID order.
Each geometry exactly {probe,moment_blocks,field_blocks,blocks}.
moment_blocks [{parent,children,coarse_moments,child_moment_sum}], sixteen
global moments in each vector, with complete clipped-child additivity.

field_blocks has EVERY ordered coarse triple {first,second,third,pieces}.
pieces follows children of coarse C in ID order, then their fine tile order:
{child,fine_tile,coarse_tile,coarse_coefficients,child_coefficient_sum}.
Indices are zero-based within the corresponding C's tile list. Every fine
tile must lie in exactly one coarse C tile. The two nine-entry vectors are
the coarse F_AB polynomial there and the sum of fine F_ab coefficients over
ALL children a of A and b of B, evaluated in the SAME global basis.
Require entrywise equality, even when coefficients are zero. Empty third
regions yield empty piece lists. No equality is required for forced fields.

blocks has EVERY ordered coarse quadruple:
{first,second,third,last,children,coarse_integral,child_integral_sum,
via_middle_integral}. children is the full Cartesian list of four-ID child
tuples, including same-parent cross-child combinations and repeats. Require
coarse U equals sum child U. For direct l0->l2 additionally sum l1->l2 true
block values through the l0->l1 map; adjacent via_middle_integral is null.
Do not assume forced or mean-only controls are additive across levels.

Counts exactly:

    levels, probes, level_pairs, level_triples, level_quadruples,
    middle_cells, positive_middle_cells, tiles, breakpoint_entries,
    middle_bound_entries, tile_bound_entries, middle_moment_entries,
    tile_moment_entries, propagated_vectors, propagated_entries,
    forced_vectors, forced_entries, outgoing_vectors, outgoing_entries,
    nonbilinear_propagated_vectors, quadruple_tile_visits,
    positive_quadruples, undefined_quad_conditionals, zero_third_quadruples,
    forced_positive_errors, forced_zero_errors, forced_negative_errors,
    mean_positive_errors, mean_zero_errors, mean_negative_errors,
    nonbilinear_quadruples, nonbilinear_forced_equalities,
    coarsening_moment_blocks, coarsening_moment_entries,
    field_blocks, field_pieces, field_child_terms, field_coefficient_entries,
    blocks, child_terms, via_middle_blocks.

Entry counts are serialized occurrences including zeros/repeats:
16 per whole/tile moment vector; 9 per propagated vector; 4 per forced/outgoing
vector; 4 per positive middle/tile bounds; 32 per moment block; 18 per field
piece. Field_child_terms counts implied child (a,b) vector references over all
field pieces, not an extra serialized vector inventory. quadruple_tile_visits
is n^3*sum_C(tile_count), a logical contract-work count, not CPU instructions.
Forced sign counts include all quadruples; mean sign counts exclude nulls.
nonbilinear_quadruples means propagated_bilinear=false; corresponding forced
equalities have forced_error=0. via_middle_blocks counts all direct-link blocks.

## Suite, provenance, bytes and coordinate tests

Suite exactly {families,controls,prior_bridges,payload_sizes,totals,scope}.
families fixed grid,warp order; totals sum all counts plus families=2.
controls exactly {pair_partition:true,triple_partition:true,quadruple_partition:true}
after verifying every corresponding summary identity.

prior_bridges exactly {AM_selected_families,AM_selected_whole_bounds_ids_equal,
AM_selected_probe_bounds_equal,AM_moments_consumed:false,
AM_query_answers_replayed:false,older_math_replayed:false}.
Compare every selected AM input middle ID/bound, level/probe label and Q bound.
Other AM contexts/data and older mathematics are identity-only; no old engine
execution is claimed. AN derives its own higher moments from supplied geometry.

payload_sizes [{family,moment_contract_bytes,coarsening_witness_bytes,
native_family_bytes}]. Contract bytes are canonical
[{level,geometry:[{probe,middles}]}] with all geometry/moments/fields.
Coarsening witness bytes are the complete canonical coarsenings list.
Native family bytes are the complete canonical family. These scopes overlap,
retain redundant witnesses and are not additive unique storage or compression.

Generic tests compare COMPLETE family wires under u'=alpha*u+du,
v'=beta*v+dv, alpha,beta>0, k=alpha*beta. Raw moments transform binomially
with volume factor k; propagated/forced coefficients pull back with factor k^2,
outgoing coefficients with k. Zero-translation factors for coefficient u^i v^j
are k^2/(alpha^i beta^j) and k/(alpha^i beta^j), respectively. Volumes scale k;
pair integrals k^2; triple integrals/errors and third_covariance k^3;
quad integrals/products/errors/centered quantities k^4. Normalized values,
indices, counts and structural flags remain unchanged. This must cover fields,
blocks and entire input as well as scalar results. Fixed affine families are
NOT run in this reduced fixed suite; report generic coverage separately.

Scope flags all false: generic_production_API_hardened,AM_moment_reuse_tested,
minimal_encoding_proved,universal_fixed_degree_closure,unknown_geometry_reconstructed,
arbitrary_dynamics_closure,continuum_limit_established,marks_authenticated,
stochastic_transition_constructed,quantum_channel_constructed,gravity_derived,
empirical_data_used,ret_integration_tested,lean_verification_performed,
fixed_affine_families_run.

## Verification and publication

Pin AM: 4,676,696 bytes SHA256
46abc46e884b8e4bc472948b4c67b3f3dd4b6dd1e8d99ced1d778912dddc085e.
AM plus its 43 prior artifacts gives 44 captures; AM's five sources plus
34 ancestors gives 39 ancestor sources. With five AN sources authenticate
88 targets. Freeze README.md,kernel.py,reference.py,study.py,test_qr05an.py
after generic verification and independent source review, BEFORE fixed AN
builds. Root explicitly releases fixed computation. Disclose every correction
to source, protocol, fixture or mathematics after first fixed computation.

Generic controls include the unit-square quadratic field, positive exact
bilinear fields, zero-support/nonbilinear equalities, multiple breakpoint
tiles, unequal refinement, signed/reassigned IDs, empty middle/endpoints,
complete cross-child quadruples, sixteen-moment and pointwise-field additivity,
complete affine transport, explicit normal/-O exception guards, detachment,
full independent family oracles and targeted non-noop corruptions.

Use isolated Python with fresh external bytecode caches, no dependencies changed.
First comparison, exactly one independent read-only reference audit, normal/-O
full tests, external create-only preflight, exclusive final capture and fresh
read-only primary/reference replays must agree. Bracket all identities and
final bytes. Capture cap 128 MiB; canonical working cap 192 MiB; not an
exhaustive hostile-resource contract. Never overwrite evidence or follow a
final-file symlink. Runtime is outside mathematics. RESULTS.md/roadmap stay
outside the frozen ledger. Publish only this gate directory and research roadmap.
