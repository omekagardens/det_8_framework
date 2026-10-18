# QR-05R protocol: nonnegative deletion-profile contract

6 September 2026. Prospective bounded gate, fixed before R execution.
Research base: pushed Q commit
`7598cdfbf3b4a17ad27c1187973108ba74fea525`.

## Question, domain dependency and boundary

Give Q's unchanged H=(frame,B,M,T) thinning law a direct nonnegative
subset-counting interface. Verify the finite basis equivalence and nested
subset counting identities. Do not expand the domain, change H, compute
minimality/stable refinement, introduce another selection law, or infer
spacetime, gravity, ontology or physical observations.

The runner supplies exactly the raw {frames,states} projection of pinned Q.
This is a declared mathematical input dependency, not independent regeneration
of Q's 1,542-source/98,656-alias universe. Neither executor reads artifacts
or imports another executor. Each validates/reconstructs features, H and
fine laws from the supplied observations. The runner independently does the
same, then compares the complete relevant Q restriction. No prior source
or evidence is edited.

Pinned Q: 13,821,257 bytes, SHA256
`1e9b9443ee5d55cd888d5ea62e594fad197ca0baeecfee1f1efac34ada8125aa`.
Also pin Q's 21 priors, giving 22 previous artifacts. Hashes establish
identity, not an empirical or physical interpretation.

## Raw model and unchanged observables

Public analyze(problem) accepts exactly
{schema_version:"det8-qr05r-problem-v1",
 family:"qr05r_deletion_profile",model:{frames,states}}.

Frames are exactly
{frame_id:0,density:"12",fixed:[0,7],eligible:[1,2,3,4,5,6]},
{frame_id:1,density:"12",fixed:[0,3,7],eligible:[1,2,4,5,6]}.
states are {state_id,frame_id,kept,past}, contiguous IDs in supplied order.
Kept original IDs are sorted, unique, within the marked frame and contain
all fixed vertices. Past rows are sorted unique local predecessor indices,
encoding a strict transitive relation with0 bottom/7 top. Numeric IDs are
not necessarily topological. Reject duplicate observations, cycles, missing
transitivity/endpoints, changed marks, and missing induced successors.
Observations restrict an already-transitively-closed relation; do not
recompute reachability from surviving generators.

Supported parser bounds: 2..4,447 states, both frames represented, at most
168,388 fine atoms, at most six eligible vertices/three of each parity.
These general syntax bounds do not authenticate alternative inputs as Q.
The certified case remains exactly Q's raw projection.

Retain eligible odd vertices independently at x and even at y; fixed
vertices always remain. A particular subset retaining o,e out of O,E has
probability x^o(1-x)^(O-o)y^e(1-y)^(E-e). Structural atoms remain at rate zero.

N_q counts endpoint chains with q internal vertices, q=0..3.
D_qoe grades chains by eligible odd/even support.
B_qroe grades ordered chain pairs by eligible union sizes, counting
self-pairs and both orders. Fixed interior3 never contributes eligible rank.
D is4x4x4, B is4x4x4x4, and B[0]=D.
M and T are the same eligible induced uniformly color-oriented K2,2 and
P4 counts: two odd/two even, no within-color comparison, all four or
exactly three cross comparisons in one uniform direction, respectively.
The missing T cross pair is incomparable; both orientations count, each
support once. Full induced comparisons, not covers or trajectories, are used.

H key=[frame_value,B,M,T], frame_value=[density,fixed,eligible].
Canonical class IDs are first occurrence. Because every retained interior
vertex lies between the probes,
O=B[0][1][1][0] and E=B[0][1][0][1].
Check this against raw eligible colors for every state and every class.
Fixed3 contributes only to D[1][0][0]. Thus H fixes both parent and
successor color ranks. This premise is essential below.

## Counting calculus and finite argument

A_s(h,o,e) counts retained eligible subsets of observation s whose induced
observation has H class h and retained colors(o,e). It is a native
nonnegative integer, with no source-alias weights. Each target H fixes
(o,e), so a sparse row has one positive multiplicity per structural target.

For fixed parent colors(O,E), let
b_oe=x^o(1-x)^(O-o)y^e(1-y)^(E-e).
These are the UNNORMALIZED Bernstein tensor monomials. The next-H law is
P_s(h)=sum_oe A_s(h,o,e)b_oe. Conventional binomially normalized Bernstein
coefficients would be A_s(h,o,e)/(choose(O,o)choose(E,e)); do not conflate them.

Expansion into the x/y power basis is triangular, with diagonal1 in each
one-dimensional factor, hence invertible at fixed(O,E).
For power coefficients c_ij the inverse is
A_oe=sum_{i<=o,j<=e} c_ij choose(O-i,o-i)choose(E-j,e-j).
Therefore, within a common H fiber (and thus common parent colors),
equality of all A values is equivalent to equality of the complete
polynomial next-H laws. This is a finite algebraic argument plus executable
checks of its premises, not a Lean proof or general sufficiency theorem
for H on unseen orders. Equal polynomials across DIFFERENT parent degrees
need not have equal A profiles (degree elevation).

Verify every complete 4x4 grade table, including zeros, and
sum_h A_s(h,o,e)=choose(O,o)choose(E,e), with out-of-range choices zero.
Total subsets are2^(O+E). Nonnegative multiplicities times nonnegative
basis terms prove nonnegative probabilities throughout [0,1]^2.
Rankwise normalization proves total probability1 throughout that domain;
selected-rate checks are supplementary, not this proof.

Compare every member's profile with its H representative, scanning all
classes/members. Canonical first failure: ascending class, then first unequal
member, then first target in the union of supports with unequal multiplicity.
Return the exact witness, no replacement feature or partition. Class profiles
and composition are only produced after ALL fibers pass.

For a closed profile and parent colors(O,E), fix final target g of
colors(m,n) and intermediate colors(k,l). Count nested subsets V⊆U⊆s:
sum_h A_s(h,k,l) A_h(g,m,n)
 = A_s(g,m,n) choose(O-m,k-m)choose(E-n,l-n).
Missing targets and out-of-range choices are zero.
The LHS sums intermediate H classes of colors(k,l); the RHS counts the
intermediate supersets of each final subset. Verify all16 intermediate
rank pairs for every structural final target, including impossible pairs,
and equality of one/two-step structural target sets. Other final ranks
for a fixed g are identically zero because H fixes its colors.
Summing nested pairs gives3^(O+E), not4^(O+E).
This is the combinatorial counterpart of composition under fresh independent
predetermined thinning; it is not a growth, adaptive or correlated law.

## Independent routes and output

Primary: observed chain supports/pair unions/quartets; binomial fine law;
direct induced-subset census for A; expand A into power coefficients.
Reference: directed chain traversal/full induced count-law moments and
alternative motif recognition; fine interpolation from exact product
probabilities; recover A by an independently implemented exact inverse basis
transform and compare a separate direct subset census. The runner rebuilds
the raw observation features/laws/profile certificate independently.
Static local copies of each route's own P/Q utilities are allowed; no runtime
imports/reads of other executors, earlier executors, or mutable RET/core code.

analysis has exactly
{model_sha256,features,partition,profiles,closure,class_profiles,
 conversion,composition,evaluation,counts}.

features: state-ordered
{state_id,color_sizes,chain_counts,mean_graded,pair_graded,
 motif_supports,motif_count,path_supports,path_count}.
partition={state_classes,classes:[{class_id,key,members}]}.

profiles=[{state_id,parent_color_sizes,transitions:
 [{target_class,retained_color_sizes,multiplicity}]}].
All target lists are sorted, unique, and include every structural target.
class_profiles use the same payload with class_id and representative_state
instead of state_id. Empty list on failed closure.

closure={closed,classes_checked,member_comparisons,witness}.
witness=null on success, otherwise
{class_id,left_state,right_state,target_class,retained_color_sizes,
 left_multiplicity,right_multiplicity,first_distinguishing_rates}.
Rates are the first distinguishing node of{0,1/3,2/3,1}² in product order;
degree<=3 per color makes this an exact bounded cross-check.

conversion={fine_kernel_sha256,pushed_rows_sha256,quotient_rows_sha256,
 profile_cells,power_cells,normalization_cells,max_abs_residual}.
Internally reconstruct Q-shaped fine rows with target_state and integer4x4
coefficients; pushed rows have target_class; quotient rows have class_id,
representative_state and transitions. Digests cover their complete canonical
rows. quotient_rows_sha256=null on failed closure.
profile_cells=power_cells=16 times profile atom count;
normalization_cells=16 times state count. Residual must be zero.

composition=null on failed closure, otherwise
{verified,rows:[{class_id,final_targets,rank_cells,nested_pairs,max_abs_residual}],
 totals:{final_targets,rank_cells,nested_pairs,max_abs_residual}}.
rank_cells=16 times structural final-target count; nested_pairs is the sum
of integer nested multiplicities over targets and intermediate ranks.

evaluation={rate_points,profile_atoms,probability_evaluations,
 normalization_rows,max_abs_residual}.
At22 exact points compare every profile atom's direct nonnegative expression
with its converted power polynomial, and verify row normalization.
rate_points=22; probability_evaluations=22 times profile atoms;
normalization_rows=22 times states. The points are the16 nodes above then
(1/2,1/2),(2/5,3/7),(1/5,4/5),(1/2,1/3),(0,2/5),(3/7,1).

counts={states,classes,fine_atoms,profile_atoms,class_profile_atoms}.

## Summary-only probability-row helper

Both routes expose evaluate_row(payload,rates), accepting exactly
payload={parent_color_sizes,transitions} with the sparse profile atoms above,
and rates=[x,y] as two canonical rational strings in[0,1].
Return {rates,outcomes:[{target_class,probability}]} with every structural
target, sorted, even when probability is zero. No raw observation,
representative lookup, source alias or hidden artifact is available to this call.

Validate native dict/list/int/string types exactly; reject bool/int or subclass
coercion, extra fields, duplicate/unsorted target IDs, wrong grade lengths,
grades outside parent bounds, zero/negative/noninteger counts, missing
rank-normalization contributions and more than64 atoms. Target IDs0..4446;
parent/child colors0..3; multiplicity at most9 and at most its binomial rank
count. Validate per-rank totals, not merely total subsets.
A single row cannot authenticate H labels, global child-class color mappings
or domain membership: callers must supply a trusted row from pinned verified
evidence. Structural validation is not authentication or an SDK integration.

Before Fraction construction, require canonical unsigned rational syntax and
at most3,000 characters per rate; then require reduced canonical spelling,
[0,1] and4,096-bit numerator/denominator limits. Guard final exact probabilities
and normalization sums to4,096 bits as well; a bound breach rejects, never
rounds/clips/truncates. No identity-only mutable payload cache; detach returned
values. All public validation failures use ValueError.

The runner calls both helpers independently for every verified class at
all22 rates, compares with independently computed fine/converted laws, and
records the call count. Helper rejection controls are separate from analyze
invalid-model controls.

## Controls, retention and publication

Prespecified controls: fixed3 eligible exclusion; all original parity marks;
closure-before-deletion inherited from raw Q; exact complete basis inversion
for every parent degree0..3; distinguish normalized/unnormalized Bernstein
factors; rankwise versus total normalization; degree-elevation counterexample;
source-alias multiplicity excluded; missing/duplicate/incorrect rank atoms;
zero-rate atoms; deterministic endpoints; canonical first closure witness and
all-member scan on synthetic failure; no quotient/composition after failure;
nested supersets with missing binomial factor; absent final targets; malformed
and same-cardinality wrong fibers; native and optimized-mode rejection;
input/cache mutation and final exact-bit guards.

Canonical native JSON: sorted compact ASCII with one final newline.
All SHA256 values cover those bytes. Arithmetic components<=4,096 bits;
working-output cap512MiB and final artifact cap64MiB. Breaches explicitly fail.
Only the supplied Q raw projection is the certified experiment; alternative
synthetic examples exercise mathematical premises and failure paths.

Run normal and optimized isolated tests with fresh external bytecode caches.
Freeze README and five Python source/test files, then create results.json
exclusively, never overwrite. Run exact read-only normal and optimized
fresh-process replays. A separate stdlib JSON-only postflight reconstructs
the retained result with no executor/runner/test imports. Verify all source,
22 prior and artifact identities before/after retained operations.

After capture, write RESULTS.md and roadmap outside the frozen source ledger.
Preserve earlier evidence and unrelated dirty RET/core/Track-B files.
Commit/push only scoped R files and roadmap. Disclose any post-exploration
protocol or implementation correction; never change the domain or criterion
silently in response to an inconvenient outcome.
