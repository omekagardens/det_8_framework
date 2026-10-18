# QR-05H: observation-law portability

6 September 2026. Research base cdfe6334ecf764a452c6d2dab0ed9970aef2e1e8.
This isolated finite research gate changes continuation acquisition laws, not
the current observation history or physical dynamics. RET/core, dependencies,
prior frozen sources/artifacts and temp_qr.md remain unchanged. No remote push.
Freeze the six listed sources after normal/optimized tests and review, before
create-only capture. No new ontology, quantum channel or apparatus data.

## Domain and public information

Reuse exactly G's ten populations/current designs, 608 intermediate states S
and 6,804 nested histories (case,S,T), with 3,534 positive joint mass and 3,270
zero-mass diagnostic histories. Global history_id is the index in case/S/T
ascending order, including zero rows. Keep P1(S)K_current(T|S) unchanged.
All eligible U subset S are available as potential continuation observations,
whether a particular continuation law assigns them positive probability or not.
Never expand (S,T,U) histories: cache future calculations per S.

IDs0..7; fixed bottom0/top7; density12. Interiors a_i=1,2,3 and b_j=4,5,6,
i,j=0,1,2. Ferrers6 has a_i<b_j iff i<=j; standard_example3 (S3) iff i!=j;
chain6 is totally ordered. Add bottom below and top above all interiors.
ferrers6_fixed uses the Ferrers order, fixed[0,3,7], eligible[1,2,4,5,6].
Otherwise fixed[0,7], eligible[1,2,3,4,5,6]. Bit j is eligible[j].
Fixed interior3 is always kept and is never part of a random color/block.

Case order:
0 ferrers6/independent;1 ferrers6/parity_adaptive;2 ferrers6/common_coin;
3 ferrers6/parity_hole;4 ferrers6/first_pair;5 standard_example3/independent;
6 chain6/parity_adaptive;7 chain6/parity_hole;8 chain6/first_pair;
9 ferrers6_fixed/independent.

For M eligible IDs, P1(S)=2^-M except first_pair, uniform on size-two S.
Current second stage: independent/first_pair IID1/2; parity_adaptive IID
r(S)=1/3 for even |S|,2/3 for odd; parity_hole IID r=1 for even,0 for odd.
common_coin keeps all S or none with equal probability; empty outcomes coalesce.
The current policy token r(S) is1/2 for common_coin, interpreted with design.
Current kernels are defined even at zero-P1 states, only as diagnostic inputs.
Empty support inclusion is one. Store the exact P1 joint-inclusion table.

Every candidate retains base=[context,T kept,T local past], with
context=[current design,density,fixed IDs,eligible IDs]. Hidden profile names
are audit metadata, never keys. Pool different profiles when this public base
agrees. The complete fixed menu below is globally known, not a random policy
label added to the base. Compare the same histories across all policies.

The primary issues each S observation from the supplied source, then predicts
only from the induced S-order and public law. All U-orders are induced from S.
The independent oracle may enumerate full-source chain indicators. Neither
executor imports prior executors or reads prior JSON; only the driver bridges
to pinned artifacts.

## Continuation-policy menu (fixed order)

1. iid_half: independently keep every eligible member of S with probability1/2.
2. iid_color: independently keep odd original-ID eligible members with1/3
   and even original-ID eligible members with2/3.
3. block_coin: one fair coin per nonempty odd/even eligible block of S,
   independent between blocks; a selected block is kept in full. Empty blocks
   introduce no extra multiplicity. U that splits a block has probability zero.

All fixed vertices are kept under every policy. These laws do not depend on the
current design/token; the token remains in old candidate keys for exact G
comparability. Original-ID parity is a supplied apparatus mark, not a physical
property or an invariant under arbitrary relabeling. A relabeling comparison
must carry its marks and entire law with it.

For each S store observations for every U subset S in increasing mask order:
kept original IDs, induced local-index past, and N_q(U), q=0..3, counting
q-internal-vertex chains between0 and7. Count vertex sets once, N0=1.
Each policy stores a probability vector aligned with these observations,
the lexicographically sorted positive joint count PMF, mean vector and scaled
coefficient mean alpha_q E[N_q], alpha_q=(-1)^q/(2^(q+1)*12^q).
The scalar coefficient remains formal, not a CP map or Born probability.
Covariance is not a new target in H; G's covariance evidence remains pinned.

Also retain G's chain counts, support-graded C[q][k], and new color-graded
D[q][o][e]: chains with o odd and e even eligible vertices. Retain all4x4x4
cells (q,o,e0..3), including zeros. Fixed vertices contribute no color degree.
Summing D at o+e=k recovers C. Mean factors are respectively
2^-(o+e), (1/3)^o(2/3)^e, and2^-([o>0]+[e>0]).
These yield an explicit menu-mean predictor, not a full-distribution theorem.
There is a specific extra positive control for block_coin: D also determines
its entire count law. The four odd/even coin assignments give the count vectors
from neither color, odd only, even only and both; use equal mass1/4 and coalesce
duplicates (including absent blocks). No analogous IID full-law claim is made.

## Summaries and canonization

Candidate order: the nine exact G keys followed by three new keys:
final_only,policy_token,tagged_policy,counts_policy,graded_policy,tagged_graded,
unmarked_order,marked_order,full_record,color_graded,block_order,color_order.

Append to the common base:
- final_only: nothing.
- policy_token: current r(S).
- tagged_policy: r(S), bool eligible[0] in S.
- counts_policy: r(S), four N_q(S).
- graded_policy: r(S), C.
- tagged_graded: r(S), C, tagged bool.
- unmarked_order: r(S), G signature[n,code], anchor only IDs0,7.
- marked_order: r(S), G signature[n,code], anchor each fixed ID individually.
- full_record: S kept,S local past.
- color_graded: r(S), D (whole3D array as one item).
- block_order: r(S), anonymous block-decorated signature.
- color_order: r(S), named color-decorated signature.

All array-valued additions are single items. G order code is
sum_(i precedes j) 2^(i*n+j) in an arranged vertex list. Anchors come first,
sorted by original ID; permute the other vertices. Minimize integer code.

For each decorated signature anchor all fixed IDs first, then permute all
eligible vertices. In each arrangement compute relation_code as above and:
- color decoration: sum_i 2^i over positions occupied by odd eligible vertices.
  Even eligible vertices and anchored fixed vertices have bit0; anchors cannot
  be exchanged with eligible vertices.
- block decoration: sum_(i<j) 2^(i*n+j) over pairs of eligible positions in
  the same parity block. This preserves an anonymous equivalence relation:
  block names may be exchanged, but their correlations may not be discarded.
Take lexicographically minimum (relation_code,decoration_code) over permutations.
Return[n,relation_code,decoration_code]. At most six vertices are permuted.
All canonization uses only the observed S relation and public eligibility/marks.

Color order is a whole-menu sufficient control: its isomorphisms transport
all three kernels, including correlations. Anonymous block order should
preserve iid_half and block_coin count laws, but not iid_color. Marginal
probabilities alone do not encode shared-coin correlations.

## Targets, partitions and finite claims

Eight targets, in this order:
iid_half_means,iid_half_counts,iid_color_means,iid_color_counts,
block_coin_means,block_coin_counts,menu_means,menu_counts.

Individual signatures are the stored count_mean/count_law. Menu signatures are
the ordered lists of all three policy means/laws. This is one vector of
counterfactual predictions on each same history, not a distribution over
policies and not a union of disjoint policy contexts. No policy prior.

Use the G partition contract: only positive current histories enter classes;
zero histories retain null candidate/target IDs. First-appearance class IDs,
sorted global members and exact summed joint mass. Each partition mass is10,
not a pooled posterior over profiles. Candidate keys contain no source names.
Target keys are [base,signature]. Retain12x12 candidate and8x8 target Boolean
refinement matrices; row A refines column B iff A-equality implies B-equality.

Assess all96 candidate/target pairs by actual fiber constancy and the first
collision against each candidate class's first positive representative. Retain
common-refinement class counts. Menu target partitions must equal the common
refinements of their three individual target partitions (same domain/base).
Menu counts refine menu means; each count law refines its mean. Do not claim
the mean/count summaries are recursively updateable or minimal in bytes.

## Fine and coarse law transport

For every S retain all nine ordered source→target policy pairs (source outer,
target inner in menu order), including identities. Scope is the labeled induced
U-record on that S; a mask uniquely identifies that record here. Do not confuse
this with identifying geometry across source profiles.

Let q(U),p(U) be source/target laws. For each observation row:
w(U)=p(U)/q(U) if q(U)>0, otherwise null (including0/0).
Missing masks have p(U)>0,q(U)=0. Fine missing mass is their summed target mass;
fine_supported iff it is zero. Weighted fine pushforward over count z is
sum_(N(U)=z,q(U)>0) q(U)w(U), retaining only positive atoms. It has mass
1-fine_missing_mass. Never renormalize this subprobability measure.

For every distinct count vector among *all* potential U observations, retain
a coarse row in lexicographic count order, even when both policy masses vanish.
Let Q(z),P(z) be their count pushforwards and A(z) the target mass at z on
fine-source-supported records. Store:
source_probability=Q, target_probability=P,
fine_supported_target_probability=A, missing_fine_probability=P-A,
weight=P/Q if Q>0 else null,
conditional_fine_weight=A/Q if Q>0 else null,
weighted_probability=P if Q>0 else0.
The coarse missing mass is sum_(Q=0)P; coarse_supported iff zero.
Store positive coarse weighted count PMF, total mass1-coarse_missing_mass.

Important exact residual on Q>0:
weight - conditional_fine_weight = (P-A)/Q.
Its Q-weighted sum is fine_missing_mass - coarse_missing_mass.
Full fine support implies full coarse support and the usual conditional-weight
identity, but the converse need not hold. Conditional fine weights are only
defined on source-positive count atoms. No inaccessible count atom is inferred.

Separate fine_weight_count_measurable: among source-positive U, is w constant
on each count fiber? Compare increasing U against the first source-positive U
with those counts; retain first_weight_collision={left_mask,right_mask} or null.
This can fail even with full fine support and correct coarse transport.
Measurability does not certify support, nor does predictive sufficiency certify
weight access. H assumes the relevant S/laws are supplied for these diagnostics.

## Prespecified controls

All controls use Ferrers6/current independent (case0), final T empty, with
positive current joint mass. S is the eligible set, excluding fixed endpoints.

- Singleton odd S={1},mask1 vs even S={2},mask2: identical marked/anonymous-block
  orders but iid_color E[N1]=1/3 vs2/3. The G marked summary fails portability.
- Antichains S={1,3},mask5 vs S={1,2},mask3: identical marked orders and iid_half
  count laws. Every eligible block_coin marginal is1/2, but P(N1=1)=0 vs1/2.
  Correlation marks, not merely per-vertex marginals, matter.
- G star/path masks57/27 retain equal D and all menu means, while their iid_half
  count laws differ (R variances15/16 vs13/16, computed from the retained PMFs).
  Color grading preserves means but need not preserve distributions.
  Their iid_color means are N1=2,N2=5/9 but relation variances68/81 vs52/81;
  their block_coin joint count laws are identical.
- On S={1,2},mask3, iid_half→iid_color, singleton masks1/2 share counts[1,1,0,0]
  but weights4/9 and16/9. Fine support is full; coarse weight at that count
  is10/9, their source-conditional average.
- On S={1,3},mask5, iid_half→block_coin, weights2 on empty/full and0 on
  singletons. Reverse transport misses masks1/4 with target mass1/2; here
  coarse support also fails at N1=1. Do not renormalize the half-mass result.
- On S={1,2,3},mask7, block_coin→iid_half, source masks[0,2,5,7] each have
  probability1/4. Missing fine masks[1,3,4,6] total target mass1/2. All four
  count atoms N1=0..3 are source-positive: coarse support holds and weights
  are[1/2,3/2,3/2,1/2]. Fine weights are1/2 on every accessible record.
  At N1=1,2, conditional fine weights1/2 differ from coarse weights3/2.
- Fixed interior3 stays outside every random parity block. Preserve G's fixed
  grading/order controls and hidden-profile pooling; color computations must
  not assign an inclusion penalty or random block to fixed3.

## Exact native wire schema

One exact input dictionary:
{schema_version:"det8-qr05h-problem-v1",family:"qr05g_menu3"}.
Only native dict/string keys/string values with exact keys/values are accepted;
reject subclasses, extra keys and bool/int substitutions, also under -O.

analysis:{cases,histories,candidate_partitions,target_partitions,assessments,
candidate_refinement,target_refinement,counts}
cases:[{case_index,profile,design,density,past,fixed,eligible,stage1_inclusions,states}]
states:[{mask,probability,kept,past,policy_token,tagged_present,chain_counts,
graded_counts,unmarked_order,marked_order,color_graded,block_order,color_order,
observations,predictions,transports}]
observations:[{mask,kept,past,chain_counts}]
predictions:{policy:{probabilities,count_law,count_mean,coefficient_mean}}
count_law:[{counts,probability}]
transports:[{source,target,fine_weights,missing_masks,fine_missing_mass,
fine_supported,weighted_count_law,coarse_rows,coarse_missing_mass,coarse_supported,
coarse_weighted_count_law,fine_weight_count_measurable,first_weight_collision}]
coarse_rows:[{counts,source_probability,target_probability,
fine_supported_target_probability,missing_fine_probability,weight,
conditional_fine_weight,weighted_probability}]
histories:[{history_id,case_index,stage1_mask,final_mask,conditional_probability,
joint_probability,candidate_classes,target_classes}]
candidate_classes:{candidate_name:class_id|null}
target_classes:{target_name:class_id|null}
candidate_partitions:{candidate_name:[{class_id,members,joint_mass,key}]}
target_partitions:{target_name:[{class_id,members,joint_mass,base,signature}]}
assessments:{candidate_name:{target_name:{sufficient,first_collision,
common_refinement_classes}}}
first_collision:null|{left_history,right_history}
first_weight_collision:null|{left_mask,right_mask}
counts:{cases,states,positive_states,observations,policies,predictions,
probability_cells,histories,positive_histories,zero_histories,candidates,targets,
transports,fine_weight_cells,coarse_weight_cells}

All probability/mean/weight/mass/density values are canonical Fraction strings;
zero-source weights/conditionals are null. IDs/masks/counts/codes are integers,
flags Boolean; no floats, tuple coercion, non-string keys or unlisted fields.
Native JSON round trips must be type-exact. All exact components <=4096 bits.
Prespecified totals:10 cases,608 states,510 positive states,6,804 observations,
3 policies,1,824 predictions,20,412 probability cells,6,804 histories,
3,534 positive,3,270 zero,12 candidates,8 targets,5,472 transports,
61,236 fine-weight cells. Coarse cells are counted, not tuned.

## Capture, reference bridge and limits

Frozen sources: README.md,portability.py,reference_qr05h.py,study.py,
test_qr05h.py,test_capture.py. Pin G results SHA256
62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74
and all its11 priors. Compare all608 state metadata/graded/canonical values,
all6,804 current-history laws and all nine old candidate partitions/IDs
directly to G JSON. Recompute old current-kernel predictions from new U
observations and compare G PMFs/means without importing any old executor.
Preserve earlier mathematical/quantum/geometric evidence by identity, not
by silently changing its scope.

Use the existing .venv Python, -I and a fresh external pycache_prefix for
each normal/optimized test, capture and replay. Pytest uses -p no:cacheprovider.
Create-only results.json; --verify is read-only exact replay; never delete or
overwrite evidence to recapture. Sorted compact JSON with comma/colon separators
and trailing newline. Runtime metadata is separate from the exact suite.
Outcomes belong in RESULTS.md. Source changes after capture require new version.

The constructions are finite predictive equivalence, exact change of measure
and probability pushforward—not new physical postulates. No unknown sampling
law inference, real-data accuracy, geometry reconstruction, continuum limit,
quantum coupling, recursive closure, RET integration or minimal bit cost follows.

## Attribution and reproduction

Target-within-source support is the finite counterpart of absolute continuity
for change of measure. This is standard importance-sampling mathematics;
see Agapiou, Papaspiliopoulos, Sanz-Alonso and Stuart,
[Importance Sampling: Intrinsic Dimension and Computational Cost](https://arxiv.org/html/1511.06196),
sections1.1 and2.1. H performs exact enumeration, not Monte Carlo estimation,
and makes none of that paper's computational-cost or asymptotic claims.
The finite predictive-equivalence basis and its limits remain as attributed
in [G's protocol](../qr-05g-predictive-compression-2026-09-06/README.md).

Run from the checkout root, with no new dependencies:

```sh
qr05h_test_cache=$(mktemp -d /tmp/det8-qr05h-tests.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05h_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05h-law-portability-2026-09-06

qr05h_opt_test_cache=$(mktemp -d /tmp/det8-qr05h-opt-tests.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05h_opt_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05h-law-portability-2026-09-06

qr05h_capture_cache=$(mktemp -d /tmp/det8-qr05h-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05h_capture_cache" docs/validation/qr-05h-law-portability-2026-09-06/study.py

qr05h_replay_cache=$(mktemp -d /tmp/det8-qr05h-replay.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05h_replay_cache" docs/validation/qr-05h-law-portability-2026-09-06/study.py --verify

qr05h_opt_replay_cache=$(mktemp -d /tmp/det8-qr05h-opt-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05h_opt_replay_cache" docs/validation/qr-05h-law-portability-2026-09-06/study.py --verify
```

The creation command must refuse an existing results.json. Use replay for an
existing artifact; never remove it to produce replacement evidence.
