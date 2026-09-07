# QR-05S protocol: local single-deletion criterion

6 September 2026. Prospective bounded gate, fixed before S execution.
Base: pushed R commit `cf8bc54386d5c7833f81c5da62c4ea4c90107b10`.

## Scope and declared dependency

Keep Q/R's raw observation domain, H=(frame,B,M,T), parity marks and
independent thinning law unchanged. Establish a local deletion criterion
and reconstruct the full subset profiles from local class counts alone.
No new domain, feature repair, stable refinement, minimality claim, physical
time, event growth, geometry, gravity or ontology is introduced.

The runner supplies the raw {frames,states} model already retained in
R's suite.problem.model. This explicit data dependency is Q's original
raw projection; source/mask aliases are not regenerated. Neither executor
reads artifacts or imports other executors. Features and H are reconstructed
from raw observations. Local-only reconstruction is a separate operation:
its input must contain no raw observations, full subset profiles, fine kernels
or prior outcomes. Full subset enumeration is allowed afterward/independently
as the ground-truth audit and for reference feature reconstruction.

Pinned R: 12,028,200 bytes, SHA256
`cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001`.
Also pin its 22 priors, giving 23 previous artifacts. Hashes establish
identity, not empirical provenance.

## Input and unchanged mathematical definitions

analyze(problem) accepts exactly
{schema_version:"det8-qr05s-problem-v1",
 family:"qr05s_local_deletion",model:{frames,states}}.
Frames:
{frame_id:0,density:"12",fixed:[0,7],eligible:[1,2,3,4,5,6]},
{frame_id:1,density:"12",fixed:[0,3,7],eligible:[1,2,4,5,6]}.
States: {state_id,frame_id,kept,past}, contiguous supplied IDs, sorted unique
original kept IDs and sorted unique local predecessor indices.
Every fixed vertex remains; relations are strict/transitive, with0 bottom
and7 top. Numeric IDs are not topological. Induce the supplied closed relation;
do not recompute reachability from surviving generators or cover edges.
Reject changed marks, cycles, missing transitivity/endpoints, duplicates and
missing single-deletion successors. Finite induction on the number deleted
then gives full subset closure; full audits check the resulting subsets too.

Parser bounds: 2..4,447 states, both frames represented, at most168,388
fine subset atoms (sum of2^(current eligible count)), at most512 H classes,
and at most26,682 fine single-vertex deletion choices (4447*6).
There are at most three eligible vertices of either original-ID parity.
The class cap512 is a prospective resource bound above Q/R's416, not a
claim that every alternatively supplied table meeting other bounds fits.
The certified experiment remains exactly the retained raw model.

N_q counts endpoint chains with q internal vertices, q=0..3.
D_qoe grades chain eligible supports; B_qroe grades ordered chain-pair
eligible unions, including self-pairs and both orders. D is4x4x4, B4x4x4x4,
B[0]=D. Fixed interior3 is excluded from eligible rank.
M/T count the same eligible uniformly color-oriented induced K2,2/P4 supports:
two odd/two even, no within-color comparison, respectively four/three
uniformly directed cross comparisons, with the missing T pair incomparable.
Both orientations count once per support, using full induced relations.

H key=[frame_value,B,M,T], frame_value=[density,fixed,eligible].
Assign first-occurrence class IDs. Verify on every state/class that
O=B[0][1][1][0], E=B[0][1][0][1] are exactly current eligible colors.
Fixed3 contributes only to D[1][0][0]. H therefore fixes parent/target color
ranks and frame. Matching a key is not proof of membership in this domain.

A_s(g,m,n) is R's integer count of retained subsets with target H class g
and retained colors(m,n). Its probability contribution is
A_s(g,m,n)x^m(1-x)^(O-m)y^n(1-y)^(E-n).
All structural atoms remain even at selected-rate zeros. No normalized
Bernstein prefactor or source-alias weight is inserted.

## Local criterion and constructive argument

L_odd(s,h) counts eligible odd vertices v whose individual deletion produces
H class h; L_even is analogous. Distinct deleted vertices can share h and
must retain their multiplicity. Row sums are O and E, not1.
An empty-color row is zero; a zero-deletion operator is identity.
Each edge preserves frame and decreases exactly the indicated color rank.

Compute fine local rows directly from single-vertex induced observations.
Check all members of each H class against its representative, even after
the first failure. First obstruction: ascending class, first unequal member,
odd before even, then first unequal target ID. On failure retain the witness
and no class-local/reconstruction/operator certificate; do not replace H.

On a finite subset-closed domain with H-measurable ranks/frame,
full A-constancy implies local constancy by selecting retained ranks
(O-1,E) and(O,E-1). Conversely, if local rows are constant, every ordered
single-deletion word has a well-defined class count. Smaller-parent induction
or word counting reconstructs all A values and proves their constancy.
This is a premise-based finite argument plus executable certificates, not
a Lean proof or a theorem that H satisfies the premises on arbitrary orders.

For a source class s of rank(O,E) and target g of rank(m,n):
other-frame or out-of-range target ranks have A=0.
At equal rank, A_s(g)=1 if g=s and0 otherwise.
For lower ranks,
sum_h L_odd(s,h) A_h(g)=(O-m)A_s(g) when O>m;
sum_h L_even(s,h) A_h(g)=(E-n)A_s(g) when E>n.
Process sources by increasing O+E, tie by class ID, never by presumed ID
topology. Use the odd recurrence when available, otherwise even.
Require exact nonnegative integer division. When both denominators are
positive, check both recurrences independently. Check all target classes,
including unreachable zeros. Rank totals must be choose(O,m)choose(E,n).

Independent word construction:
(L_odd^a L_even^b)[s,g]=a!b! A_s(g,O-a,E-b).
One fixed color order is used; summing over all color permutations would add
another combinatorial factor. Verify exact divisibility, zero deletions and
impossible counts. For actual fine deletions, different-color words commute.

After local constancy is established, verify on class operators:
L_odd L_even=L_even L_odd=A at retained rank(O-1,E-1),
L_odd²=2*A at rank(O-2,E), L_even²=2*A at rank(O,E-2).
Row masses are OE, O(O-1), E(E-1), including empty/impossible cases.
Compare complete structural target maps; absent targets mean zero.
Mixed commutation alone is insufficient for full reconstruction.

## Local-only constructor and trust boundary

Both routes expose reconstruct_profiles(local_model), accepting exactly
{schema_version:"det8-qr05s-local-v1",classes:[...]}.
Each class is exactly
{class_id,frame_id,parent_color_sizes,odd,even}.
odd/even are sorted unique target lists [{target_class,multiplicity}].
Class IDs are contiguous supplied labels, not assumed topological.
There are1..512 classes; frame_id is native0/1; ranks are two native
integers0..3. Counts are native positive integers1..3. Each color row has
at most3 atoms and its multiplicities sum to the corresponding parent rank.
Targets must exist, preserve frame, and decrease the indicated color exactly.
At most3,072 class-local atoms and32,768 output profile atoms (512*64).
Reject malformed/coerced fields, rank/target/frame inconsistencies, duplicate
targets, wrong totals, mixed-order disagreement, noninteger recurrence/word
division, wrong base/normalization and any arithmetic/resource bound breach.

Output is exactly {profiles,certificate,operator_checks}.
profiles are [{class_id,parent_color_sizes,transitions:
 [{target_class,retained_color_sizes,multiplicity}]}],
in class order, with sorted positive structural target atoms.
Multiplicity is at most its binomial rank count (<=9).
No observations, prior files or full-profile lookup are available to this call.
It returns newly owned/detached native structures; no mutable identity cache.
All public validation failures use ValueError. Components<=4,096 bits,
working output<=512MiB. This structural/algebraic validation cannot
authenticate H labels, domain membership or realization as an observed order.
A trusted local model must come from the independently verified raw domain.

certificate={target_cells,base_cells,recurrence_cells,
 normalization_cells,max_abs_residual}.
target_cells=number of classes squared, including incompatible zero targets.
base_cells counts ordered same-frame pairs of equal ranks (delta checks).
recurrence_cells counts, for each same-frame componentwise-compatible pair,
each positive color difference separately; both colors count when applicable.
normalization_cells=16 times classes, including impossible retained ranks.
All residuals must be zero. These counts describe required audited equations,
not an implementation's private arithmetic instruction count.

operator_checks={verified,rows,totals}.
Each row is
{class_id,odd_odd_targets,even_even_targets,mixed_targets,
 coefficient_cells,odd_odd_pairs,even_even_pairs,mixed_pairs,max_abs_residual}.
coefficient_cells=odd_odd_targets+even_even_targets+2*mixed_targets,
counting both mixed orders. Pairs are weighted deletion-word counts, not
just numbers of intermediate class labels.
totals sums all row numeric fields except class_id; verified must be true.

## analyze output and independent comparison

analysis has exactly
{model_sha256,features,partition,local_rows,local_closure,local_classes,
 reconstruction,comparison,counts}.
features retain the R fields:
{state_id,color_sizes,chain_counts,mean_graded,pair_graded,
 motif_supports,motif_count,path_supports,path_count}.
partition={state_classes,classes:[{class_id,key,members}]}.
local_rows=[{state_id,frame_id,parent_color_sizes,odd,even}].
local_classes use class_id and representative_state instead of state_id;
they are empty on failed local closure.

local_closure={closed,classes_checked,member_comparisons,witness}.
witness is null or
{class_id,left_state,right_state,color,target_class,left_multiplicity,right_multiplicity},
where color is"odd" or"even".
reconstruction is null on failure, otherwise
{class_profiles,certificate,operator_checks}.
class_profiles match R's exact
{class_id,representative_state,parent_color_sizes,transitions} schema.

comparison={
 direct_profiles_sha256,reconstructed_profiles_sha256,full_profile_closed,
 local_full_equivalent,fine_kernel_sha256,pushed_rows_sha256,
 quotient_rows_sha256,profile_cells,power_cells,max_abs_residual}.
Full direct profiles are R-shaped state rows, independently enumerated
from raw subsets. Reconstructed state profiles substitute each verified
class profile into its actual members, never source-alias weights.
Profile cells=16 times direct profile atoms on success,0 on failure.
Power cells=16 times direct profile atoms in all cases.
Compare complete power expansions with internally reconstructed fine/pushed
Q-shaped laws; these use integer4x4 coefficient tables with x power outermost.
full_profile_closed is independently measured from all direct profiles.
local_full_equivalent must hold under the checked premises.
On failed local closure reconstructed_profiles_sha256 and quotient_rows_sha256
are null; no class reconstruction is claimed. SHA256 covers canonical bytes.

counts={states,classes,fine_atoms,fine_local_choices,
 local_atoms,class_local_atoms,direct_profile_atoms,class_profile_atoms}.
fine_local_choices counts raw deleted-vertex choices over all observations;
local_atoms/class_local_atoms count nonzero target-class atoms across both
colors. Direct profiles/digests may be rebuilt internally without duplicating
all full state profiles in this artifact.

Primary uses observed chain-support/pair-union/quartet features, direct local
deletions and smaller-parent recurrence. Reference uses its independent
traversal/count-moment/motif lineage and ordered-word powers/factorials.
Both reconstruct full raw subset profiles separately for comparison.
The runner rebuilds all features, local rows, full profiles and certificates
independently. Static local copies of each route's own utilities are allowed;
no runtime imports of previous/other executors or mutable RET/core code.
The runner separately calls both local-only constructors and compares every
returned profile with raw-subset ground truth and pinned R. R's probability
helper, Q's four-variable certificate and source-alias universe are not
re-run or silently integrated into this gate.

## Controls and lifecycle

Controls: twins/identical successors retain deleted-vertex multiplicity;
row masses and empty colors; full-rank delta and zero-deletion identity;
other-frame/impossible-rank zeros; reversed class-ID topology; exact divisors
versus incorrect total-parent division; fractional-division rejection despite
valid local row totals; odd/even mixed-order failure; same-color factor2!;
all source/target ranks, absent targets and rankwise binomial normalization.
Preserve fixed3, original parity and raw induced transitivity.
Synthetic failed local fibers must scan all members and produce no class
reconstruction. Exercise wrong/omitted atoms, same-cardinality wrong fibers,
native bool/subclass/float errors, changed inputs and detached outputs,
resource caps, and explicit guards under optimized Python.

Canonical native JSON uses sorted keys, compact ASCII and one final newline.
Final artifact cap64MiB, working cap512MiB. All exact components<=4,096 bits.
Bound breaches fail explicitly, never truncate or silently reduce scope.
Run normal/-O tests with fresh external bytecode caches.
Freeze README plus five Python files, create results.json exclusively,
then exact read-only normal/-O fresh-process replays. A separate stdlib
JSON-only postflight reconstructs the retained mathematics without importing
executors, runner or tests. Verify six source,23 prior and artifact byte
identities before/after retained operations.

Write RESULTS.md and roadmap outside the frozen ledger after verification.
Preserve earlier evidence and unrelated dirty RET/core/Track-B work.
Commit/push only scoped S files and roadmap. Disclose corrections made after
exploratory execution; do not change criteria based on the outcome.
