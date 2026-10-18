# QR-05AK protocol: shared-intermediate geometry and composition

7 September 2026. Prospective specification before fixed AK computations.
Base: pushed AJ commit 8c410538cab848205f837d3b07a9237357609b87.
All prior research, RET/core work, dependencies and temporary model sheets remain unchanged.

## Question and scope

Compare actual shared-middle three-point causal measures with products of the
projected pair measures on AJ's supplied nested rectangular partitions. Test
true triple block additivity independently of pair-product composition. Identify
dependence lost by this particular construction, not a universal impossibility
of recovering triples from all possible pair summaries or supplied geometry.

This is a PRIVATE bounded exact diagnostic, not a hardened production API.
No geometry is inferred, no observation masks are enumerated or transported,
and no RET/Lean integration, empirical validation, stochastic transition,
quantum channel, continuum limit, ontology or gravity derivation is claimed.

## Inputs and independent engines

Authenticate AJ's retained results and select the five problem inputs, ordered
grid, warp, warp_stale, boost, dilate. Project away supplied_mark: the new
geometry-only problem is exactly {family,probes,levels}; probes [{name,bounds}],
levels [{level,cells}], cells [{event,bounds}]. No old computed pair/triple
answers, parent maps, observations or historical executors enter either engine.
No fixture, split, probe, coordinate or event numbering changes are allowed.

Each independent stdlib engine exposes build_family(problem),
causal_area(a,b,c,d), and triple_area(a,b,c,d,e,f). The last is the directed
one-dimensional measure of x<y<z for x in[a,b], y in[c,d], z in[e,f]. Primary
uses positive-part cubic antiderivatives; reference uses exact Simpson panels
of the piecewise-quadratic shared-middle integrand. They independently compute
all volumes, pair and triple integrals, lineage and coarsening. They may cache
exact interval primitives within one build, not read stored results or import
each other. Reference is also the independent replay route, not a third engine.

Bounded native inputs have exactly three distinct nonempty string level labels,
1..8 positive rectangular cells per level and 1..5 positive rectangular probes
with unique nonempty names; family is a nonempty string. Event IDs are ordered,
unique native integers within each level, signed IDs allowed. They are local
to the level, not persistent cell identifiers. Full cell interiors are disjoint,
and their clips cover every query. For each link (0,1),(1,2),(0,2), derive each
child's unique parent by FULL-rectangle containment before clipping; children
must cover every parent, not just preserve a global area. Verify direct and
composed lineage maps agree. Inputs/outputs are detached native data.

## Exact measures and null conventions

Strict order x≺y means u_x<u_y AND v_x<v_y, with dmu=du dv/2.
Let h_A=mu(A intersect Q), J_AB=integral 1(x≺y)dmu(x)dmu(y) over clipped
A,B, and T_ABC=integral 1(x≺y≺z)dmu(x)dmu(y)dmu(z) over clipped A,B,C.
Retain every ordered pair and triple, including repeated region labels,
reverse IDs and zero clips. Repeated regions do not identify the continuum
points or assert that an event precedes itself. Strict point-order diagonals
have zero measure, but T_AAA=h_A^3/36 for a rectangular clip.

For one coordinate, predecessor length is L(y)=clamp(y-a,0,b-a) and successor
length R(y)=clamp(f-y,0,f-e). triple_area integrates L(y)R(y) over[c,d].
In two dimensions T is the product of the u/v triple_area values divided by8;
J is the product of the u/v causal_area values divided by4.
Require sum_AB J_AB=V^2/4 and sum_ABC T_ABC=V^3/36 for query volume V.

The projected pair product is P_ABC=J_AB*J_BC/h_B when h_B>0. If h_B=0,
T and both J factors are zero but P and its product error are JSON null,
explicitly undefined. If h_B>0 and an endpoint volume is zero, both T and P
are defined zero. The normalized triple fractions T/(h_A*h_B*h_C) and
P/(h_A*h_B*h_C) are null whenever that full product is zero.

Retain signed product_error=P-T and middle_covariance=(T-P)/h_B whenever
h_B>0. The covariance interpretation is exact: with a uniform point Y in
clipped B, let L_A(Y) be predecessor volume in A and R_C(Y) successor volume
in C. Then T-P=h_B*Cov_B(L_A,R_C). This retained covariance is DERIVED from
the independently computed pair/triple moments; it is not a third independent
arithmetic route or an additional measured observable. Generic centered-integral
hands independently check the interpretation. Do not impose an error-sign or
refinement-monotonicity acceptance criterion; retain every sign and equality.

## Coarsening and dependence accounting

For every ordered parent triple A,B,C and complete Cartesian child block,
verify T_ABC=sum_abc T_abc and the analogous clipped-volume additivity.
Retain five child equality-pattern integral sums: all_equal (a=b=c),
first_middle (a=b!=c), first_last (a=c!=b), middle_last (b=c!=a), and
all_distinct. They partition every child triple; their sum is the full measure.

If the parent middle volume is positive, define P_fine as the sum of child
products for h_b>0. Child triples with h_b=0 make an explicitly skipped zero
contribution to this SUM; their own normalized product stays null. Retain the
number of such child triples. If h_B=0, P_fine and all product/error accounting
fields for that parent block remain null, while true raw integrals remain zero.

Retain and verify the exact decomposition

    coarse_product_error = P_coarse - T,
    within_child_error   = P_fine - T,
    between_child_error  = P_coarse - P_fine,
    coarse_product_error = within_child_error + between_child_error.

These errors are signed and specific to the declared pair-product construction.
Endpoint refinement alone must agree: reconstruct J_aB=sum_b J_ab and
J_Bc=sum_b J_bc from fine pair data, and verify
endpoint_refined_product=sum_ac J_aB*J_Bc/h_B equals P_coarse.
Likewise middle_refined_product=sum_(b:h_b>0) (sum_a J_ab)*(sum_c J_bc)/h_b
must equal P_fine. These use geometric volumes, never stale annotations.

For positive parent volume product, verify the true normalized conditional
by weighting child true conditionals with h_a*h_b*h_c/(h_A*h_B*h_C).
Zero child products contribute zero without defining their conditional ratios.
For a zero parent volume product, both parent and aggregated conditionals are null.

For direct l0,l2, also sum the l1,l2 TRUE triple blocks through the independently
derived l0,l1 map and compare with the direct true sum. This via-middle route
does not multiply newly averaged intermediate pair tables. No equality is
assumed between projected products formed at different middle resolutions.

## Complete mathematical wire

All mathematical rationals are reduced [numerator,positive_denominator] native
integer pairs; components at most4096bits. Counts/IDs are native integers, flags
native booleans, and undefined ratios JSON null. No floats in mathematics.
Canonical JSON has sorted keys, compact separators, ensure_ascii and newline.

build_family returns exactly {problem,levels,coarsenings,counts}.
problem is a detached unmodified input. levels is [{level,geometry}], in level
order. Each geometry item, in probe order, exactly
{probe,volume,cells,pairs,triples,summary}. Cells [{event,clipped_volume}].
Pairs follow the full event-ordered Cartesian product and exactly match AJ's
wire: {first,second,clipped_product,causal_integral,conditional}.
Triples follow the full first-outer/middle/last-inner event order, exactly
{first,middle,last,volume_product,causal_integral,pair_product,product_error,
conditional,product_conditional,middle_covariance}.
Summary exactly {true_integral,continuum_integral,extended_product_sum,product_error}.
The extended sum skips zero-middle nulls as explicit zero-measure terms;
individual products and ratios remain null as specified above.

Coarsenings follow (0,1),(1,2),(0,2). Each exactly
{coarse,fine,parents,geometry}; parents [{parent,children}], in parent/child
event order. Each geometry item exactly {probe,volumes,blocks}, with volumes
[{parent,coarse_volume,child_volume_sum}]. Blocks follow complete coarse triple
Cartesian order, each exactly:

    first, middle, last, children, zero_middle_children,
    coarse_integral, child_integral_sum, child_pattern_integrals,
    coarse_conditional, weighted_child_conditional,
    coarse_pair_product, child_pair_product_sum,
    endpoint_refined_product, middle_refined_product,
    coarse_product_error, within_child_error, between_child_error,
    via_middle_integral.

children is the complete Cartesian child list [[first,middle,last],...], not
filtered by region equality, direction, zero volume or positive point order.
child_pattern_integrals has exactly the five pattern keys specified above.
via_middle_integral is null on adjacent links and a rational (including zero)
on the direct link. It is not a normalized quantity.

Counts exactly {levels,probes,level_pairs,level_triples,blocks,child_terms,
zero_middle_level_triples,undefined_level_conditionals,positive_level_errors,
zero_level_errors,negative_level_errors,zero_middle_blocks,
positive_between_errors,zero_between_errors,negative_between_errors,
positive_repeated_region_triples}. Undefined errors are excluded from sign
counts and reported by the separate zero-middle counts. The final count means
T>0 and fewer than three distinct region IDs, not coincident point triples.

Suite exactly {families,controls,prior_bridges,totals,scope}. Family order is
fixed above; totals sum each family count and add families=5. Controls compare
COMPLETE levels/coarsenings/counts wires: boost equals grid; dilation scales
volumes by4, pair measures by16, triple measures/products/errors by64, and
middle_covariance by16, preserving normalized conditionals and counts; stale
warp equals warp exactly once only the input family label is excluded.
Controls exactly {boost:true,dilation:true,stale_geometric:true}, after checks.

prior_bridges exactly {AJ_family_names,AJ_projected_inputs_equal,
AJ_complete_clipped_volumes_and_pairs_equal,AJ_coarsening_math_replayed:false,
other_prior_math_replayed:false}. The two equality booleans may be true only
after checking all five input projections and all fifteen level/five-probe
clipped-volume and complete directed pair tables against authenticated AJ.
AJ annotation/coarsening calculations and older mathematics are identity-only.

Scope flags all false: generic_production_API_hardened,
unknown_geometry_reconstructed,marks_authenticated,continuum_limit_established,
cross_level_observation_transport_proved,higher_chain_composition_closed,
universal_pair_summary_insufficiency_proved,stochastic_transition_constructed,
quantum_channel_constructed,gravity_derived,empirical_data_used,ret_integration_tested.

## Verification and publication

Pin AJ results.json:1,825,670bytes, SHA256
4be2fbc4a7f62322416fd2a2e256a529eb03f54fad3ca88674c060d31d94e8d1.
Authenticate AJ's40 prior captures as41 total. AJ's five sources plus its19
ancestor sources give24 ancestor sources here. With five AK sources:70 targets.
No historical engine imports. Prior arithmetic replay is limited to the stated
AJ pair/volume projections. The geometry-only input deliberately drops marks.

Freeze README.md,kernel.py,reference.py,study.py,test_qr05ak.py before fixed
execution. Generic synthetic hands and source review precede that freeze;
no fixed build_family until root explicitly releases it. Generic cases include
the unit-rectangle T=1/288 versus P=1/128, exact separated-region equality,
repeated/signed/reassigned IDs, zero-middle versus zero-endpoint cases, unequal
splits, centered covariance, endpoint-only refinement and true triple additivity.
Complete independent family-oracle comparisons, targeted non-noop mutations,
source ownership and explicit normal/-O guards are required. No full generic
adversarial resource admission contract is advertised.

Use isolated Python with fresh external bytecode caches; no dependencies or
unrelated edits. Run fixed comparisons and normal/-O tests, an independent
read-only reference audit, external create-only preflight, exclusive final
capture and fresh read-only primary/reference replays. Bracket operations by
all source/prior identities and preserve final bytes. Disclose every source,
protocol or fixture correction after the first fixed calculation.
Capture cap96MiB, working native suite cap128MiB; at most five families,
three levels, eight cells and five probes per family. No unbounded computation.
Never overwrite evidence or follow final-file symlinks. Runtime metadata are
outside mathematics. RESULTS.md and the roadmap are outside the frozen ledger;
publication includes only this gate directory and the research roadmap.
