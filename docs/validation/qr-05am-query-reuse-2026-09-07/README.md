# QR-05AM protocol: query reuse and explicit refinement

7 September 2026. Prospective before fixed AM calculations.
Base: pushed AL commit 578c28311d747680771adc61923192c898720bbd.
Prior research, RET/core work, dependencies and temporary sheets remain unchanged.

## Question and boundary

Can new endpoint functions reuse AL's frozen middle-tile moments, and can
unsupported functions trigger an explicit, verified geometry-aware refinement?
Separate genuine reuse from silent moment regeneration, and structural function
admission from accidental equality of integrated answers. Retain a deliberately
incorrect forced old-tile corner fit for every query, including equalities.
This is a PRIVATE bounded diagnostic on supplied rectangular geometry, not a
production API, arbitrary-query interface, minimal grid, unknown-geometry
reconstruction, universal composition closure, physical or ontological proof.

## Input projection and prespecified queries

Authenticate AL's retained capture. Project only its middle geometry/moments;
do not consume old endpoint coefficients, pairs, triples or coarsening answers.
The five families remain grid,warp,warp_stale,boost,dilate in that order.
The three levels, five probes and all middle rows remain unchanged.

Engine input exactly {family,contexts}. Contexts follow level outer/probe inner,
each {level,probe,probe_bounds,middles}. Each middle exactly
{event,bounds,u_breaks,v_breaks,moments,tiles,queries}. The first six fields
come verbatim from AL, except each tile is projected to {bounds,moments}.
Whole-middle and tile moment lists use AL's i-outer/j-inner ordering
(00,01,02,10,11,12,20,21,22). Retain empty middles with null bounds, empty
breakpoint/tile lists and nine zero whole moments. Queries are [{name,incoming,
outgoing}], where each endpoint is a positive rectangle or null (empty).
No implicit endpoint clipping is performed: the supplied endpoint region is
the mathematical domain. Fixed endpoints lie within the retained probe Q;
generic hands may supply other finite rectangles in the same coordinate plane.

For each middle B, prespecify these five queries, in this order:

1. whole_probe: incoming=Q,outgoing=Q.
2. middle_self: incoming=B,outgoing=B.
3. incoming_kink: incoming=[B.u0,k,B.v0,B.v1],outgoing=B.
4. outgoing_kink: incoming=B,outgoing=[k,B.u1,B.v0,B.v1].
5. zero_endpoint: incoming=null,outgoing=B.

For positive B, k is the midpoint of the FIRST retained tile's u interval,
chosen from geometry before any new calculation, not from observed errors.
For empty B, queries 2..5 have null endpoints; whole_probe still has Q,Q.
Every query is assessed independently against the ORIGINAL frozen tile grid;
refining one query must not change any other query's admission or moments.

Private native bounds: 1..15 contexts, at most three distinct level labels and
five distinct probe labels, unique (level,probe) pairs; labels/family nonempty
strings. Each context has 1..8 sorted unique signed native-integer middle IDs
and a positive probe rectangle. Positive middle rectangles are interior-disjoint,
inside Q and cover Q. Each middle has 1..5 unique nonempty query names. Positive
middle grids have strictly ordered boundary-complete u/v breakpoints and exactly
their u-outer/v-inner Cartesian tiles, at most 289. Tiles are positive, with
their nine moments; M00 equals geometric volume. Whole moments equal complete
tile sums entrywise. All integer components are native and at most 4096 bits;
all rational pairs [n,d] are reduced with d>0. Reject floats, boolean IDs/rational
components, unknown/missing fields, bad grids, overlap/coverage holes and
non-native mathematical types/subclasses. Shared references among otherwise
valid native input containers need not be rejected; outputs must be detached.

## Supplied-moment trust and independent routes

Both stdlib engines expose build_family(problem) and derive_moments(bounds),
the latter taking a native four-rational rectangle and returning nine raw
moments. It is the explicit NEW-child moment derivation hook. Within a build,
call this hook exactly once for each derived piece and never for an unchanged
retained piece; do not cache away these declared per-piece calls. Generic tests
must disable/count the hook to prove the coefficient-only route really reuses
the supplied old moments. No historical executors or engine cross-imports.

Primary performs structural/input checks but does NOT geometrically regenerate
old moments. Old geometric authenticity comes from the runner's pinned AL
projection and the independent reference. Primary contracts the SUPPLIED old
values for reuse and forced fits, and uses exact tensor antiderivatives only
for derived child moments. A coherent wrong higher moment can pass structural
checks; primary is not advertised as its geometric authenticator. Never repair
or silently replace old moments. An untrusted direct engine call lacks the
runner's provenance guarantee; generic mutation tests must expose this boundary.

Reference independently integrates every supplied old moment from its bounds
and rejects disagreement. This geometric validation is separate from the new
moment hook and is explicitly counted as reference verification work, not
computation-free reuse. Reference uses exact tensor-Simpson evaluation for raw
moments and direct clamp/product/centered integrals, with coefficient contraction
agreement checks. Primary uses branch coefficients and Gram contractions.
Both consume the same frozen moment wire; neither may read stored new answers.

Use dmu=du dv/2 and strict product order. Incoming L_A(y) and outgoing R_C(y)
are predecessor/successor VOLUMES, products of the one-dimensional nonnegative
clamp lengths divided by 2. For B, h=mu(B), J_in=integral_B L_A dmu,
J_out=integral_B R_C dmu, T=integral_B L_A R_C dmu. Endpoint volumes are the
complete supplied endpoint rectangle volumes, zero for null.

## Admission, forced fits and exact refinement

Assess L_A and R_C SEPARATELY on every positive old tile. A function identically
zero on the tile is bilinear regardless of inactive coordinate breakpoints.
Otherwise it is bilinear iff neither coordinate factor has an endpoint
breakpoint STRICTLY inside its tile interval. Incoming factor is identically
zero if tile.high<=endpoint.low; outgoing if tile.low>=endpoint.high.
Boundary kinks are allowed. A zero outgoing function does not excuse an
unsupported incoming function merely because their product integrates to zero.

Primary certifies these branch conditions. Reference independently certifies
the whole bilinear corner interpolant by comparing clamp values on the full
grid of tile boundaries plus endpoint breakpoints: each subrectangle's function
is bilinear, so agreement at all subrectangle corners is exact certification.
Use (1,u,v,uv) in one GLOBAL coordinate basis. For every old tile retain the
four corner-fit coefficients for BOTH functions even when not admissible;
these are the declared FORCED control. They may be exact or wrong. They must
not be relabeled as admitted coefficients based on integral equality.

If B is empty: admission="empty_middle". If both functions are admissible on
every old tile: admission="reuse". Otherwise admission="refine". For each
old tile in a positive-middle query:

- If BOTH functions fit, retain that exact tile bounds/moment wire as one piece.
- Otherwise split THAT old tile at all incoming/outgoing endpoint coordinate
  boundaries strictly inside it. Use every positive Cartesian child, u outer/v
  inner; bounds from null endpoints contribute none. This deliberately simple
  rule may include inactive cuts once a tile needs refinement; no minimality
  is claimed. At most 25 children per old tile (two endpoints, four cuts/axis).
- Derive nine moments for EACH new child through derive_moments. Compute exact
  bilinear coefficients on each piece; verify admissibility there. Preserve
  unsplit old pieces exactly, including in a query that refines other tiles.
- For EVERY old tile, retain the complete piece index list and verify that
  the nine child/piece moments sum to the supplied old nine, not only volume.

Contract exact piece coefficients with m and G derived from moments, where
basis e=((0,0),(1,0),(0,1),(1,1)), m_a=M_ea and G_ab=M_(ea+eb). Sum pair/triple
contractions. Reference separately integrates the exact clamp functions on
piece quadrature nodes; every pair, triple and centered contraction must agree.
The forced route contracts its old-tile corner fits against the ORIGINAL old
moments. No new moments or refined coefficients enter that forced control.

For h>0, P=J_in*J_out/h and covariance=(T-P)/h. Compute centered_integral by
centering each exact function by its whole-B mean before integration, not by
renaming T-P; require equality with T-P. Forced pair-product is formed from
the forced incoming/outgoing pair means with the same h. Errors are FORCED
minus EXACT, retaining every sign/equality; no fixed sign is an acceptance rule.
Normalize exact/forced triples and pair-products by mu(A)*h*mu(C) only when
that full volume product is positive. Zero-middle raw pairs/triples/errors are
valid zero but divided products, covariance and centered integral are null.
A positive middle with an empty endpoint has defined raw zeros as appropriate,
with fully normalized fractions null. Reuse-result fields are populated ONLY
for admission="reuse"; refinement/empty cases retain null reuse fields.

## Exact mathematical output

Return exactly {problem,contexts,counts}. Contexts follow input order, each
{level,probe,middles}; middles [{event,queries}], and each query exactly
{name,admission,old_tiles,pieces,moment_blocks,result,counts}.
old_tiles follows snapshot order, each
{tile,incoming_admissible,outgoing_admissible,forced_incoming,forced_outgoing},
where tile is its zero-based index and forced vectors have four rationals.
pieces follows old-parent order then child-grid order, each
{parent,bounds,moments,moment_source,incoming_coefficients,outgoing_coefficients},
moment_source is "retained" or "derived". moment_blocks follows old tile order,
each {parent,children,old_moments,piece_moment_sum}; children are complete
zero-based indices into pieces. Empty middles have all three lists empty.

result exactly:

    middle_volume, incoming_volume, outgoing_volume, volume_product,
    incoming_pair, outgoing_pair, causal_integral, pair_product,
    conditional, product_conditional, middle_covariance, centered_integral,
    forced_incoming_pair, forced_outgoing_pair, forced_integral,
    forced_pair_product, forced_conditional, forced_product_conditional,
    incoming_pair_error, outgoing_pair_error, forced_error,
    reuse_incoming_pair, reuse_outgoing_pair, reuse_integral.

Query counts exactly:

    old_tiles, admissible_old_tiles, unsupported_old_tiles,
    retained_pieces, derived_pieces, replaced_old_tiles, moment_derivation_calls,
    forced_coefficient_vectors, forced_coefficient_entries,
    exact_coefficient_vectors, exact_coefficient_entries,
    new_moment_entries, retained_moment_entries, piece_bound_entries,
    moment_blocks, moment_block_entries.

These count serialized entries including zeros/repeats: two four-coefficient
vectors per old tile or exact piece, nine moments per piece, four bounds per
piece, and 18 moment entries per block (old and summed). Derivation calls equal
derived pieces; replaced_old_tiles equals unsupported_old_tiles.

Family counts sum all query counts and add exactly:

    contexts, middle_rows, positive_middle_rows, snapshot_tiles,
    snapshot_moment_entries, snapshot_bound_entries, endpoint_bound_entries,
    queries, empty_middle_queries, reuse_queries, refinement_queries,
    positive_exact_queries, forced_positive_errors, forced_zero_errors,
    forced_negative_errors, refinement_forced_equalities,
    incoming_pair_disagreements, outgoing_pair_disagreements.

snapshot_moment_entries counts whole plus tile vectors once per input middle;
snapshot_bound_entries counts positive middle bounds, tile bounds and u/v
breakpoint lists (not the separately retained probe bounds).
endpoint_bound_entries counts four for each nonnull query endpoint.
Forced sign and pair-disagreement counts include only positive-middle queries;
refinement_forced_equalities means admission refine AND forced_error=0.
positive_exact_queries means T>0. Snapshot tiles are unique input occurrences,
whereas old_tiles counts their repeated use across queries. No results selected
by positivity, admission outcome, label or forced-fit discrepancy are omitted.

## Suite, payload, transformations and provenance

Suite exactly {families,controls,prior_bridges,payload_sizes,totals,scope}.
Totals sum complete family counts plus families=5. Controls exactly
{boost:true,dilation:true,stale_geometric:true} after comparing COMPLETE family
wires including inputs/queries, old and new moments, coordinates, coefficients,
admission, results, piece maps and counts (only family label excluded).
For positive coordinate scales alpha,beta, k=alpha*beta: bounds/breakpoints
scale by coordinate; M_ij by k*alpha^i*beta^j; coefficient of u^i v^j by
k/(alpha^i*beta^j); volumes by k, pairs/covariance by k^2, triple/product/error/
centered quantities by k^3. Normalized fractions/counts/indices unchanged.
Boost=(2,1/2); dilation=(2,2); stale warp equals warp after only label removal.
Generic translated hands require binomial moment and coefficient transport.

prior_bridges exactly {AL_family_names,AL_geometry_moment_projection_equal,
AL_probe_bounds_equal,AL_other_math_replayed:false,older_math_replayed:false}.
Both true flags require comparison of EVERY consumed old geometry/moment field
and probe bound against authenticated AL. Fixed query construction is separately
checked in project_inputs and tests. Reference geometrically rechecks consumed
moments; no old endpoint/pair/triple/coarsening engine is executed or claimed.

payload_sizes has one row per family: {family,snapshot_bytes,query_bytes,
exact_update_bytes,native_family_bytes}. Snapshot is canonical engine problem
with queries removed from every middle. Query bytes are canonical
[{level,probe,middles:[{event,queries}]}] projected from input. Exact update bytes
are canonical [{level,probe,middles:[{event,queries:[{name,admission,pieces}]}]}]
from output. Native family bytes include the complete problem, diagnostics,
forced control and witnesses. These overlapping explicit research scopes are
NOT additive unique data inventories, wire-minimality or a compression benchmark.

Scope flags all false: generic_production_API_hardened,
untrusted_primary_moments_geometrically_authenticated,minimal_grid_proved,
universal_query_interface,unknown_geometry_reconstructed,
arbitrary_dynamics_closure,continuum_limit_established,marks_authenticated,
stochastic_transition_constructed,quantum_channel_constructed,gravity_derived,
empirical_data_used,ret_integration_tested,lean_verification_performed.

## Verification and publication

Pin AL: 13,515,233 bytes SHA256
1e0f3ac8822afcd4407a176e1bfa4a2c3f5e45c43724e4e70bf3f66f01580a52.
AL plus its 42 prior captures gives 43 artifacts; AL's five sources plus its
29 ancestors gives 34 ancestor sources; with five AM sources authenticate
82 targets. Source names README.md,kernel.py,reference.py,study.py,test_qr05am.py.
Freeze all five after generic hands and independent review, BEFORE fixed AM
builds. Root explicitly releases fixed computation. No after-first correction
may be hidden; disclose changes to source, mathematics, protocol or fixture.

Generic checks include disabled/counting derivation hooks, coherent wrong old
moments versus pinned/geometric verification, aligned/active/inactive/boundary
kinks, separate function admission despite zero products, forced-fit failures
AND accidental integral equalities, per-query independence, unchanged retained
pieces, all nine additive moments, mixed-grid/unequal pieces, centered integrals,
signed/reassigned IDs, translated moments/coefficients, nulls, full payload
counting/detachment and explicit normal/-O guards. Use an independent full
family oracle and targeted non-noop corruption tests before calling it complete.

Use isolated Python and fresh external bytecode caches; no dependency edits.
First comparison, one independent read-only reference audit, normal/-O full
tests, external create-only preflight, exclusive final capture and fresh
read-only primary/reference replays must agree. Bracket all identities and
preserve final bytes. Capture cap 128 MiB, canonical working suite cap 192 MiB;
these private limits are not an exhaustive hostile-resource admission contract.
Never overwrite evidence or follow a final-file symlink. Runtime is outside
mathematics. RESULTS.md/roadmap remain outside the frozen ledger. Publish only
this gate directory and the research roadmap; do not include unrelated changes.
