# QR-05P protocol: finite minimality and summary-consumer contract

6 September 2026. Prospective bounded investigative gate.
Research base: pushed QR-05O commit
`35831db06b3f5089fdb36d066cfb741b1c2984cb`.

## Fixed question, dependence and scope

On exactly the O observation domain, construct the coarsest strongly closed
refinement R of C=(frame,B,M), using the full polynomial thinning law.
Compare actual R memberships with H=(frame,B,M,T). Equality is a possible
outcome, not a premise or an inference from equal class counts.
Then certify which prespecified observables a summary-only consumer can
predict. Do not expand the domain or change the observation law.

This gate is deliberately narrower than O: its runner supplies the raw
observation model extracted type-exactly from pinned O evidence. It does not
independently regenerate the 1,030-source/65,888-alias universe. Neither
executor reads any artifact or imports another executor. Supplied inputs
contain no features, class IDs, kernels, source aliases or outcome flags.
Each route validates and reconstructs features and fine laws from the
observation table. The runner compares these with pinned O afterward.
No previous source or evidence is edited.

O artifact: 27,143,093 bytes, SHA-256
`3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1`.
Pin this artifact and its 19 priors. Hashes establish byte identity, not
empirical provenance or a physical interpretation.

## Input model and calculus

Public analyze(problem) accepts exactly:
{schema_version:"det8-qr05p-problem-v1",
 family:"qr05p_summary_contract",model:{frames,states}}.

The runner's certified input has O's two frames and 2,470 states.
Frames are exactly:
{frame_id:0,density:"12",fixed:[0,7],eligible:[1,2,3,4,5,6]},
{frame_id:1,density:"12",fixed:[0,3,7],eligible:[1,2,4,5,6]}.
Each state has exactly {state_id,frame_id,kept,past}.
State IDs are contiguous in supplied order. Kept original IDs are sorted,
unique in0..7, contain every fixed vertex, and otherwise belong to the
frame's eligible set. Past rows are sorted unique local predecessor indices.
They encode a strict transitive relation with0 below every other kept
vertex and7 above every other kept vertex. Local indices need not be
topological. Reject native bool/int substitutions, subclasses, duplicate
observations, cycles, nontransitive relations, missing endpoints, invalid
marks and missing induced successors. No alias multiplicities are weights.

Both routes support only bounded well-formed tables with2..2,470 states,
both frames represented, all induced eligible-subset successors present,
and at most99,180 fine atoms. These parser bounds do not certify arbitrary
alternative tables: the retained case is bound to O's exact projection.
The complete study also requires the prespecified singleton controls below;
their absence is an explicit case-constraint error, not a fabricated result.
Public validation failures use ValueError, including rejected native-type
coercions, so callers do not need implementation-specific error branches.

Independently retain each currently eligible odd vertex at x and even
vertex at y, keeping fixed vertices. For a subset retaining o,e out of O,E,
its probability is x^o(1-x)^(O-o)y^e(1-y)^(E-e).
All structural atoms remain, even at selected-rate zeros.
Use native integer4x4 coefficient tables, x degree outermost, degree<=3
per color. Rows normalize coefficientwise; all four corners are deterministic.

N_q counts endpoint chains with q internal vertices, q=0..3.
D_qoe counts chains by their eligible odd/even support.
B_qroe counts ordered pairs of chains by the size of their eligible union.
Self-pairs and both orders count; fixed internal3 is not eligible.
D is4x4x4, B is4x4x4x4, B_0r=D_r and N_r=sum_oe D_roe.

M counts induced eligible uniformly color-layered K2,2 supports.
T counts induced eligible uniformly color-layered P4 supports: two of each
color, no within-color comparisons, exactly three uniformly oriented
cross comparisons, and the remaining cross pair incomparable.
Both orientations count; each four-set once. Supplied transitive relations,
not cover edges, are used. M/T cannot share a support.
These are observed features, not lookup labels or Feynman trajectories.

The primary uses observed chain subsets, ordered support unions, quartet
recognition and binomial kernels. The reference uses directed chain
traversal, complete induced count-law moments for B, common-neighbor and
central-edge motif recognition, and exact rational interpolation of direct
product probabilities. Locally copied utility code from each route's own
O lineage is allowed; runtime imports/reads of prior executors are not.

## Refinement and finite coarseness argument

Form C and H by first occurrence of exact keys [frame,B,M] and
[frame,B,M,T], where frame=[density,fixed,eligible].
Start v0 at C, never H. At each synchronous round push every fine row into
the current classes. The next class key is the pair
[current class ID, complete target-class polynomial row].
Reassign first-occurrence IDs. Including the old class forbids merges.

The primary groups exact coefficient signatures. The reference groups
block probabilities at all16 nodes {0,1/3,2/3,1}², calculated from direct
product probabilities, not from the primary's coefficients.
An explicit bidegree(3,3) bound and invertible tensor evaluation map make
this grid equality equivalent to coefficient equality. A selected rate or
an unbounded sampled grid is not sufficient.

Retain every round's vector, actual classes, pushed-row canonical digest,
atom count, stability flag and canonical split witnesses. For each non-first
child of an old class, compare its representative with the old representative;
retain the first differing old target, both coefficient tables and the first
distinguishing node. Order separations by ascending new child class ID.
Recompute all exact row signatures during audit:
digests and a few witnesses alone are not a partition certificate.

Stop at the first unchanged canonical vector. Strict rounds increase class
count, so there are at most n-|C| strict rounds and one final stable round.
Do not assume a one-round repair. The normal runner imposes a512MiB
working-output cap through retained JSON checks and a64MiB final-artifact cap;
any exceeded cap is an explicit error, never a truncated successful result.
Exact components are bounded to4,096 bits.

For any closed partition Q refining C, induction shows Q refines every
round: each current block is a union of Q blocks, so equality of probabilities
into Q blocks implies equality into current blocks. At stability R is closed.
Thus R is the unique coarsest closed C-refinement on this domain and law.
This is a premise-based finite mathematical argument plus an exact
certificate of its premises, not a Lean proof or exhaustive enumeration of
all possible partitions. It is not unrestricted minimality, minimum bytes,
runtime optimality or a general sufficiency theorem.

After every terminal fiber is checked, retain its representative quotient
and verify Q_(x,y)Q_(a,b)=Q_(xa,yb) coefficientwise in four independent
variables (256 cells per structural start/end pair). Fresh independent
predetermined stages are the premise. No adaptive/correlated law is tested.

## Output schema

All mathematical data are native string-keyed dicts, lists, ints, strings,
booleans and null. Canonical JSON is sorted/compact ASCII with one final
newline; SHA-256 digests always hash those bytes. No float or implicit
tuple/bool/integer coercion.

analysis has exactly:
{model_sha256,features,partitions,fine_kernel,refinement,consumer,consumer_audit,counts}.

features is the state-ordered list of
{state_id,color_sizes,chain_counts,mean_graded,pair_graded,
 motif_supports,motif_count,path_supports,path_count}.

partitions has C and H, each
{state_classes,classes:[{class_id,key,members}]}.

Fine rows are reconstructed internally as
[{state_id,transitions:[{target_state,coefficients}]}], with sorted targets.
They are not duplicated in the output. fine_kernel is
{sha256,transition_atoms,coefficient_cells,normalization_rows,
 deterministic_corner_rows,rate_points,evaluated_atoms}.
rate_points is the native integer22, not an additional list of rates.
The audit rates are the16 nodes above followed by
(1/2,1/2),(2/5,3/7),(1/5,4/5),(1/2,1/3),(0,2/5),(3/7,1).
The pinned O bridge checks the complete reconstructed fine rows' digest
and every reconstructed feature, not just counts.

refinement is
{initial_partition:"C",rounds,strict_rounds,final_round,state_classes,
 classes,quotient_rows,semigroup,comparison,counts}.
Each round is
{round_index,state_classes,classes,pushed_rows_sha256,pushed_atoms,
stable,separations}.
The vector/classes are the current round's partition; separations describe
the computed next partition. A final stable round is retained once.
Round and terminal classes are [{class_id,members}].
Each separation is
{parent_class_id,child_class_id,left_state,right_state,target_class,
 left_coefficients,right_coefficients,first_distinguishing_rates}.
Quotient rows are
[{class_id,representative_state,transitions:[{target_class,coefficients}]}].
semigroup follows O's exact {verified,rows,totals} schema, including all
transition_pairs, intermediate_paths, coefficient_cells and max_abs_residual.
comparison is
{names:["C","R","H"],refinement:[[bool]],same_memberships_as_H,
 R_to_C,R_to_H,H_to_R}; maps are native integer lists indexed by source
class, or null when that refinement fails.
counts is
{rounds,strict_rounds,classes,round_transition_atoms,round_coefficient_cells,
 separation_witnesses,quotient_transition_atoms,
 semigroup_intermediate_paths,semigroup_coefficient_cells}.

## Summary-only consumer demonstration

Freeze these questions, in order:
chain_counts (vector N0..N3), motif_count (M), path_count (T),
counts_motif_path (vector N0..N3,M,T), named_relation_1_7
(the integer indicator that original-ID relation1<7 is present).
For each question compare values within actual R fibers.
Do not presume T or the joint vector is R-measurable before comparing H/R.

consumer has exactly
{schema_version:"det8-qr05p-consumer-v1",model_sha256,
 state_classes_sha256,class_count,quotient_rows,observables}.
observables is [{name,measurable,class_values,first_failure}].
A measurable question has one value per class and null first_failure;
a nonmeasurable question has null class_values and the canonical first
{class_id,left_state,right_state,left_value,right_value} failure.
The quotient is copied here so the payload needs no raw order/state table.

Public predict(consumer,question,class_id,rates) uses only this payload,
a native question string/class int and two canonical rational strings in
[0,1]. It returns exactly
{question,class_id,rates,outcomes:[{value,probability}]}.
Group by exact observable value, sort by its canonical JSON bytes, and
retain structural zero outcomes at selected rates. Probabilities are
canonical rational strings. Reject unknown/nonmeasurable questions,
invalid/native-coercing IDs/rates and malformed payload structure.
Validate row/table shape, native coefficients, row normalization and
selected-rate nonnegativity on the requested row. Representative IDs are
strictly increasing and start at0; at most99,180 quotient atoms are allowed.
Observable values obey the declared finite combinatorial bounds:
N0=1,N1<=6,N2<=15,N3<=20 and0<=M,T<=9. Named indicators are0 or1.
Rates must pass canonical integer/fraction syntax and a3,000-character
length cap before rational construction; reject scientific notation before
it can trigger large arithmetic. Parsed rates, evaluated atoms and final
grouped probabilities respect the4,096-bit exact-component bound.
This is not artifact authentication: the caller must use a pinned verified
payload and ensure the initial observed
order belongs to the bound input domain before supplying its trusted class.
Matching an H key from an unseen order is not a membership certificate.
No general domain encoder, RET API or packaged SDK is added.

For every measurable question, build exact marginal polynomial rows from
the quotient, compare them with all fine-state rows, and retain them in
consumer_audit.marginals. Each item is
{name,rows:[{class_id,outcomes:[{value,coefficients}]}],fine_coefficient_cells}.
Check predict against those polynomials at all22 rates for every class.
This exhaustive audit may validate the payload once and use the exact same
prediction core called by public predict. Separately exercise the public
validation/API path at all22 rates for class0, the middle class and the
last class, for every measurable question in both implementations.
fine_coefficient_cells counts16 times the sum, over fine source states,
of structural distinct observable-value outcomes after grouping each row.
prediction_checks counts class/rate/measurable-question combinations.
Nonmeasurable questions must be rejected, not guessed.

consumer_audit has exactly
{marginals,prediction_checks,nonmeasurable_questions,named_singleton_control,
verified}.
nonmeasurable_questions is the ordered list of their names.
The prespecified exclusion compares observations kept[0,1,7] and[0,3,7]
in frame0, both chains. Locate IDs by raw observation, not assumed numbers.
They have the same C/H and the same closed summary evolution, but the
future event1<7 has probabilities x and0. Retain
{state_ids,C_classes,H_classes,R_classes,current_values,
 next_coefficients,half_probabilities,same_R_class}.
Require same_R_class by the verified refinement theorem/H closure, not
by replacing R. This is a model-relative labeled-query exclusion.

Top counts is exactly
{states,features,C_classes,H_classes,R_classes,fine_atoms,
 refinement_rounds,strict_rounds,measurable_questions,
 consumer_prediction_checks,consumer_fine_coefficient_cells}.

## Controls, independent audit and publication

Tests independently reconstruct raw features, kernels, every refinement
round/key, actual terminal membership, quotient, composition and consumer
marginals. Include synthetic finite Markov examples requiring two strict
rounds, a stable input, and a false merge if old-class membership is omitted.
Synthetic helpers are outside the O case and do not expand certification.
Include native type/subclass errors, wrong same-size fibers, altered digests,
missing/reordered/extra rounds, early stopping, missing witnesses, false H
equality/maps, bad quotient/semigroup, false measurability, corrupted marginal
laws, unnormalized/bad-rate payloads and nonmeasurable-query rejection.
Optimized production guards explicitly raise.

The runner reconstructs the raw-model/feature/fine-law bridge to pinned O
and audits P independently of both routes. It does not replay O's entire
D/B/M expectation and prior-domain certificates; they remain pinned old
evidence. State exactly this boundary in RESULTS.md.

Freeze six sources: README.md, closure.py, reference_qr05p.py, study.py,
test_qr05p.py, test_capture.py. RESULTS.md and roadmap are outside the ledger.
Run normal and optimized isolated Python3.11 tests with fresh external
bytecode caches, Ruff and new-file whitespace checks before freezing.
Capture canonical results.json exclusively, never overwrite, and run normal
and optimized read-only exact replays under unchanged source/prior identities.
Finish with a JSON-only postflight importing no executor/runner/test.
Lifecycle negatives use temporary stub evidence, never the real capture.

Commit/push only this gate and its roadmap. Preserve all unrelated RET/core,
temporary model-sheet and other checkout work. No dependency installation,
new physical law, apparatus data, noise dismissal, metric, gravity,
continuum or ontology claim follows. Broader portability and RET/Lean
integration remain separate gates.
