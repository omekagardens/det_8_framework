# QR-05T protocol: local stable refinement

6 September 2026. Prospective bounded gate, fixed before T outcome execution.
Base: pushed S commit 814203ed6f386cc27e1351d0427ddfe89fadbc18.

## Question and dependency

On exactly S's raw domain, start from C=(frame,B,M), construct the coarsest
stable refinement by odd/even single-deletion counts, and independently by
full subset profiles. Compare their actual terminal fibers with one another
and with H=(frame,B,M,T). Equality with H is an outcome, not a premise.
Different traces/round counts are allowed. No domain extension or feature
repair, physical dynamics, ontology, Lean or RET integration is introduced.

The runner supplies S's suite.problem.model, exactly Q/R's raw projection.
Pin S results.json: 7,128,993 bytes, SHA256
8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3,
and its 23 priors (24 artifacts total). Neither executor reads artifacts,
imports another/previous executor, or uses mutable RET/core code. Static
copies of each route's own S utilities are allowed. Features and raw fine
deletions/subsets are recomputed. Do not use S's H-grouped rows to construct
either refinement. Do not regenerate the source/mask-alias universe.

## Input and unchanged calculus

analyze(problem) accepts exactly
{schema_version:"det8-qr05t-problem-v1",family:"qr05t_local_refinement",
 model:{frames,states}}.
Frames are exactly:
{frame_id:0,density:"12",fixed:[0,7],eligible:[1,2,3,4,5,6]},
{frame_id:1,density:"12",fixed:[0,3,7],eligible:[1,2,4,5,6]}.
States are {state_id,frame_id,kept,past}, contiguous supplied IDs; sorted
original kept IDs and sorted local predecessor indices. Require every fixed
vertex, strict transitivity, 0 bottom/7 top, distinct raw observations, both
frames and every single-deletion successor. Induce the full supplied relation,
not surviving cover edges. Numeric IDs are not a topological order.

Preserve S's N/D/B/M/T definitions: endpoint chains with q internal vertices
(q=0..3), eligible chain-support grades D (4x4x4), ordered pair-union grades B
(4x4x4x4), including self-pairs/both orders and B[0]=D. M and T are eligible
uniformly color-oriented induced K2,2 and P4 supports (2 odd/2 even, no
same-color comparison, respectively 4/3 cross comparisons; missing T pair
incomparable). Recognize both orientations from induced transitive relations.
Fixed interior 3 is excluded from eligibility.
C key=[frame_value,B,M]; H adds T; frame_value=[density,fixed,eligible].
First occurrence assigns canonical class IDs.
Verify O=B[0][1][1][0], E=B[0][1][0][1] on every state. C fixes frame/rank,
and all subsequent partitions must refine C and preserve that measurability.

Independently retaining eligible colors at x,y assigns each subset probability
x^m(1-x)^(O-m)y^n(1-y)^(E-n). No alias weights or normalized Bernstein
prefactors. All structural atoms remain even at selected-rate zeros.
Raw fine polynomial rows use S's integer 4x4 tables, x degree outermost.

Bounds: 2..4,447 raw states; 168,388 fine subset atoms; 26,682 fine deletion
choices; at most 3 eligible vertices of either color. C/H and every retained
refinement partition have at most 512 classes; breach fails, never truncates.
The supplied experiment is the exact pinned model; these parser bounds do
not certify arbitrary alternative tables. Arithmetic components <=4,096 bits,
working JSON <=512MiB, final artifact <=64MiB.

## Raw count rows and public local refinement

Fine local rows are
{state_id,frame_id,parent_color_sizes,odd,even},
where odd/even are sorted unique [{target_state,multiplicity}].
Actual raw observations have multiplicity 1 per deleted vertex/target state;
aggregate repeated class targets with their full deleted-vertex multiplicity.
Every edge preserves frame and lowers exactly its color rank; row masses O/E.
Raw full count rows are
{state_id,frame_id,parent_color_sizes,transitions:
 [{target_state,multiplicity}]}.
They enumerate all raw retained subsets, not prior profiles. Target rows fix
retained ranks. Full-rank raw mass is exactly the self delta; all rank totals
are choose(O,m)choose(E,n). Fine local rows must equal the corresponding
one-deletion slices of these full rows.

Public refine_local(local_problem) accepts exactly
{schema_version:"det8-qr05t-local-v1",state_classes,rows}.
rows are the fine local schema above, with 1..4,447 contiguous states,
native frame 0/1 and native ranks 0..3. Each color row has <=3 sorted unique
targets and multiplicities 1..3; row sums/rank loss/frame must hold.
There are <=26,682 weighted choices/atoms. Initial labels are first-occurrence
canonical, <=512 classes, and every initial fiber fixes frame/rank.
Neither H, features, raw observations, full profiles nor artifacts are supplied.
Return the local trace defined below, detached from inputs/other calls.
This helper certifies local count stability relative to its supplied initial
partition, not H labels, observed-poset realization or full-subset integrality.

Both routes retain S's reconstruct_profiles API and exact
det8-qr05s-local-v1 input/output contract, copied locally without runtime
imports. Its rank induction / independent word-factorial routes reconstruct
terminal profiles from class-local rows only. All S structural, divisibility,
normalization, operator, ownership and resource guards remain active.
Internal _refine_full(rows,state_classes) returns the full trace below for
raw full-count rows; synthetic controls may call it. Validate native targets,
ranks/frame, self delta, binomial rank totals and bounds; this is not a new SDK.

Reject malformed/native-coerced data with ValueError, including bool/subclass
substitutions, cycles, explosive shared DAGs and missing structural premises.
Per-call traversal memoization is allowed; mutable result-identity caches are
not. Validate native inputs before canonical-content caches. Preserve valid
shared inputs but return no mutable input/output or cross-call aliases.

## Synchronous traces

For current partition v, aggregate raw local rows into target classes, giving
S-shaped rows {state_id,frame_id,parent_color_sizes,odd,even}, now using
target_class. Aggregate raw full rows into R-shaped profiles:
{state_id,parent_color_sizes,transitions:
 [{target_class,retained_color_sizes,multiplicity}]}.
At every round verify inherited frame/ranks and rank normalization/row masses.

Local next keys are [old class, complete odd row, complete even row].
Full next keys are [old class, complete full transitions].
Assign new IDs by first occurrence. Old class membership forbids merging.
Regenerate all signatures, including missing-target zeros, rather than
accepting only digests or witnesses. Compare every nonrepresentative member
with its current representative, even after detecting a split.

trace={mode,rounds,strict_rounds,state_classes,classes,counts},
mode is "local" or "full"; terminal classes are [{class_id,members}].
counts={rounds,signature_atoms,member_comparisons,separations}.
Each round is
{round_index,state_classes,classes,rows_sha256,signature_atoms,
 member_comparisons,stable,separations}.
The round retains its CURRENT partition and current aggregated row digest;
separations describe the computed NEXT partition. signature_atoms counts
nonzero color/target atoms (both colors) or full profile atoms.
member_comparisons=n-current_class_count, all actually checked.
Stop at the first unchanged canonical vector; retain that stable round once.

For each non-first child of a current class, compare its representative with
the old parent's representative. Order witnesses by ascending new child ID.
Local separation:
{parent_class_id,child_class_id,left_state,right_state,color,target_class,
 left_multiplicity,right_multiplicity},
first differing odd before even, then ascending target ID.
Full separation:
{parent_class_id,child_class_id,left_state,right_state,target_class,
 retained_color_sizes,left_multiplicity,right_multiplicity},
first differing target ID. Absent counts are zero. There must be one witness
per increase in class count, no omitted/extra/reordered witnesses.

Strict rounds are bounded by min(6,n-initial_classes), then one stable round.
Reason: rank 0 is already stable; rank k can no longer change after all smaller
ranks have stabilized and its next split has occurred. Full same-rank mass is
only the self delta, whose class is already represented by the old-class key.
Thus at most 7 retained rounds; class/byte caps are separate resource bounds.
Do not assume one strict round or equal local/full traces.

For a rank-preserving partition, its full split refines its local split,
because local counts are full-profile rank slices. Monotonicity then implies
the full partition at each aligned round refines the local one; extend a
terminated trace's last vector for this comparison. Verify actual maps.

## Terminal certificate and relative coarseness

Under finite subset closure and measurable frame/ranks, S's argument makes
local constancy equivalent to full-profile constancy. Every stable refinement
of C refines each synchronous round: every current block is a union of its
blocks, so equality of weighted laws into those blocks forces equality into
current blocks. At termination the partition is stable. This proves the unique
coarsest stable refinement preserving C on this finite domain.

Both terminal partitions must therefore have identical actual fibers.
Compare H only after construction; do not force equality. Independently check
H local closure. If H is closed it is a closed C-refinement and must refine
the terminal partition; any strict difference must be retained.
This is a premise-based finite proof plus executable premise/signature
certificates, not Lean verification, enumeration of all partitions, unrestricted
minimal memory, minimum bytes, performance optimality, or arbitrary-order
sufficiency. P's smaller-domain minimality is not assumed or replayed.

## Analyze schema

analysis is exactly
{model_sha256,features,partitions,fine_kernel,fine_deletions,
 local_refinement,full_refinement,comparison,terminal,minimality,counts}.
features are exactly S's state-ordered N/D/B/M/T records.
partitions={C,H}, with {state_classes,classes:[{class_id,key,members}]}.
fine_kernel={sha256,atoms}; digest covers complete S-shaped fine polynomials.
fine_deletions={sha256,atoms,choices}; digest covers raw fine local rows.
Both traces follow the schema above.

comparison={names,refinement,maps,same_terminal_memberships,
 same_memberships_as_H,H_local_closed,aligned_full_refines_local}.
names=["C","L","F","H"]; refinement is the complete 4x4 boolean relation
(row partition refines column partition).
maps has L_to_C,F_to_C,L_to_F,F_to_L,L_to_H,H_to_L; each is a list indexed
by source class, or null if not a refinement.
same_memberships_as_H refers to L/H.
aligned_full_refines_local has one boolean per max(number of retained rounds).
same_terminal_memberships and every aligned comparison must be true;
if H_local_closed, H_to_L must exist. Equality with H is not required.

terminal={local_rows,class_profiles,reconstruction,closure,comparison}.
local_rows are class-local rows in S's
{class_id,representative_state,frame_id,parent_color_sizes,odd,even} schema.
class_profiles are S/R's
{class_id,representative_state,parent_color_sizes,transitions} schema.
reconstruction={certificate,operator_checks}, the exact S contract.
closure={local_closed,full_closed,classes_checked,member_comparisons};
both closures must hold after every member is checked.
terminal.comparison={direct_profiles_sha256,reconstructed_profiles_sha256,
 pushed_rows_sha256,quotient_rows_sha256,profile_cells,power_cells,max_abs_residual}.
Direct profiles come from raw full subsets aggregated into L. Reconstructed
state profiles substitute actual class reconstructions into all members.
Both digests must match; compare all fine-to-L polynomial coefficients with
expanded profiles. profile_cells=power_cells=16*direct profile atoms.
All residuals zero. Do not rerun S's complete H reconstruction to obtain L.

minimality={verified,initial_partition,terminal_partition,
 all_rounds_refine_C,all_rounds_rank_frame_measurable,local_full_terminals_equal,
 H_used_in_construction,strict_round_bound,relative_to_C,
 arbitrary_partitions_enumerated}.
Values are true,"C","L",true,true,true,false,min(6,n-|C|),true,false,
supported by the checked premises and proof above.

counts={states,C_classes,H_classes,L_classes,F_classes,fine_atoms,
 fine_local_choices,local_strict_rounds,full_strict_rounds,
 terminal_local_atoms,terminal_profile_atoms}.

## Independent checks and lifecycle

Primary constructs local splits directly and independently checks full-count
splits; reference prioritizes raw full-profile splits and computes local splits
separately. Use independent S feature lineages. The runner independently
rebuilds raw features/counts, every round/signature/witness, terminal fibers,
profiles, recurrences/operators and all bridges. It separately calls each
public local refiner on raw local rows and each constructor on terminal rows,
comparing whole native outputs with the raw audit. It must not import either
executor for its reconstruction.

Prescribed synthetic controls: valid rank-lowering local systems with (i) two
strict local rounds but one full round and equal terminals; (ii) equal supports
and row totals but different multiplicities; (iii) identical empty local rows
in distinct inherited classes. Recompute synthetic full profiles independently
and label these algebraic controls, not observed C realizations.
Test early stopping, dropped old-class key, omitted/reordered/extra rounds and
witnesses, signature/digest corruption, same-cardinality wrong fibers, false
H equality/maps, terminal reconstruction/operator errors, native/cache/DAG,
missing induced transitivity, detached ownership, bounds and explicit -O guards.

Bridge the exact raw model, features, actual H fibers and fine law to S, and
verify S's H local rows by independent raw regrouping. Do not presume L=H:
compare terminal laws with S only through a verified L/H map if applicable.
No source-alias regeneration, R probability helper, Q four-variable certificate,
P consumer/minimality replay, or SDK changes are hidden in this gate.

Canonical native JSON is sorted/compact ASCII with one final newline.
Run normal/-O tests with fresh external caches via explicit -X pycache_prefix.
Freeze README plus local_refinement.py, reference_qr05t.py, study.py,
test_qr05t.py and test_capture.py. Create results.json exclusively, never
overwrite. Run exact normal/-O read-only fresh-process replays and a separate
stdlib JSON-only postflight (source bytes only for hashes; no executor/runner/
test imports). Check six source,24 prior and artifact identities before/after.
Write RESULTS.md/roadmap outside the frozen ledger. Disclose pre-capture
corrections. Commit/push only scoped T research files and roadmap, preserving
all unrelated RET/core/Track-B and temporary model-sheet work.
