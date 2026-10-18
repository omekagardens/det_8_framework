# QR-05G: question-relative predictive compression

6 September 2026. Research base commit
`490c443186dbe1b862d377e197f3281ee261ad56`. Keep RET/core, dependencies and
prior sources/artifacts unchanged. Remote sync remains deferred. Freeze the six
listed sources after tests/review and before create-only capture. No ontology,
new physical laws, apparatus data or quantum/order coupling is introduced.

## Question and public context

What partial provenance preserves a declared continuation question? Distinguish
computing the current sequential estimator, preserving future count means,
preserving the full joint count distribution, and preserving the fully labeled
future observed-order distribution. These are different tasks.

Reuse exactly the ten QR-05F populations/designs and their first/final masks S,T.
Given S, draw an independent repeat U subset S under that case's second-stage
kernel K(U|S). This is a repeat acquisition from the same intermediate order,
not evolving geometry or a third quantum process. The observer's current public
record is the induced labeled order on T, together with the known design,
density, fixed vertices and eligible-ID frame. Source/profile names are audit
metadata, not available information. No hidden source relations are disclosed.

The primary route predicts from the observed induced S-order and known mask law.
The independent reference may use full-source chain indicators as an oracle.
Future U-order relations must be induced from S, never invented after deletion.

## Ten-case universe and exact laws

Use naturally labeled IDs0,...,7, fixed bottom0/top7, density12. Interiors1,2,3
are a_i;4,5,6 are b_j, with i,j=0,1,2. Ferrers6 has a_i<b_j iff i<=j;
standard_example3 (S3) iff i!=j; chain6 is a total order. Add bottom below
and top above all interiors. Profile ferrers6_fixed is the same Ferrers6 order
with fixed [0,3,7], eligible [1,2,4,5,6]; other profiles fix [0,7] and have
eligible [1,2,3,4,5,6]. Fixed internal vertices are never randomly weighted.

Case indices, in order:

0. ferrers6 / independent
1. ferrers6 / parity_adaptive
2. ferrers6 / common_coin
3. ferrers6 / parity_hole
4. ferrers6 / first_pair
5. standard_example3 / independent
6. chain6 / parity_adaptive
7. chain6 / parity_hole
8. chain6 / first_pair
9. ferrers6_fixed / independent

For M eligible vertices, masks use bit j for eligible[j]. P1(S)=2^-M except
first_pair, which is uniform on size-two S and zero elsewhere. Conditional
kernels are defined even for zero-P1 S, but those states are diagnostic only.

- independent/first_pair: independently retain members of S with r=1/2.
- parity_adaptive: IID conditional rate r(S)=1/3 for even |S|,2/3 for odd.
- parity_hole: IID conditional rate r(S)=1 for even |S|,0 for odd.
- common_coin: one fair coin retains all S or none. At S empty these outcomes
  coalesce to one empty outcome with probability one. Its token is1/2.

For IID kernels K(U|S)=r^|U|(1-r)^(|S|-|U|) on U subset S, including0^0=1.
The token is interpreted with the public design, so common_coin is never
treated as IID. First inclusion pi1(a) and conditional inclusion pi2(a|S)
are computed from these exact laws; empty-set inclusion is one.

Retain all 608 first states and all 6,804 nested histories (case,S,T), including
3,270 zero-joint-mass histories; 3,534 histories are supported. Likewise retain
all 6,804 repeat rows (case,S,U), including conditional probability zero.
History order is case index, then increasing S, then increasing T. Its global
history_id is the zero-based position in this full list, never renumbered after
removing zero-mass histories. Each state uses increasing S. No Monte Carlo.
positive_repeat_rows counts K(U|S)>0 even at zero-P1 diagnostic states (4,872
rows); positive_histories instead requires positive joint mass (3,534).
current_estimator_cells counts four entries per retained history (27,216).

## Questions and signatures

For each observed order, N_q is the number of increasing q-internal-vertex
chains between probes0 and7, q=0,1,2,3. Count each vertex set once. Let C[q][k]
count such S-chains with exactly k eligible vertices (0<=q,k<=3); retain the
full4x4 support-graded table, including zeros. Row sums give current counts.
The formal scalar coefficient is alpha_q N_q with
alpha_q=(-1)^q/(2^(q+1)12^q), for z^q, z=mass². This is not a CP map or Born
probability; fixed nonzero alpha means the count questions determine the
corresponding coefficient questions without a new prediction partition.

Four targets, in order:

1. current_estimate: the QR-05F sequential_supported vector on (S,T), summing
   1/[pi1(a)pi2(a|S)] over observed T-chains when both denominators are positive.
   Omit unsupported terms explicitly even on impossible histories. Retain the
   four omitted counts. This target depends on both S and T.
2. future_means: E[(N0,N1,N2,N3)(U)|S], with K as specified.
3. future_counts: the exact joint PMF of that count vector, not separate marginals.
4. future_records: the exact PMF of the fully labeled induced U-order, represented
   by kept IDs and local past lists. It includes relations as well as the U mask.

The last target is deliberately stronger than a bare mask law: across different
hidden source profiles the same mask law can push forward to different count
laws. It follows that future_records equality implies future_counts equality,
which implies future_means equality. No such nesting with current_estimate is
assumed. All predictions are conditioned on each particular S; averaging over
hidden histories gives a different, reduced-information forecasting task.

Store repeat count means/covariance and the coefficient mean/covariance obtained
by alpha scaling. Covariance is an exact weighted centered Gram matrix and must
be positive semidefinite. Zero-P1 state predictions are evaluations of the
declared kernel, not conditional expectations on null events.

## Candidate summaries, with no hidden-source names

Every key begins with the same base:
[context, final kept IDs, final local past], where
context=[design,density,fixed IDs,eligible IDs]. Thus different public designs or
frames are not merged; histories from different source profiles *are* compared
when their public context/final record agrees. Source index is never a key.

Candidate order and appended fields:

- final_only: append nothing.
- policy_token: append r(S).
- tagged_policy: append r(S), then whether eligible[0] belongs to S.
- counts_policy: append r(S), then the four current S-chain counts.
- graded_policy: append r(S), then C[q][k].
- tagged_graded: append r(S), C[q][k], then eligible[0] membership.
- unmarked_order: append r(S), then the canonical S-order preserving only
  boundary IDs0,7; a fixed interior vertex loses its distinguishing mark here.
- marked_order: append r(S), then the canonical S-order preserving every fixed
  vertex individually. Eligible labels are forgotten. This is a positive control
  for the label-equivariant repeat count law, not for the fully labeled law.
- full_record: append the kept IDs and local past of S. Its token is recoverable
  from S and the design. It must preserve all four targets.

Canonical-order signature is [n,code]. Put the anchored vertices first in
ascending original-ID order, then permute all other present vertices. For this
vertex order v, encode the strict relation as
sum_(i,j with v_i<v_j in the poset) 2^(i*n+j); take the smallest integer code
over the permitted permutations. Unmarked anchors are[0,7]; marked anchors
are the case's fixed list. The observed past used in this calculation is the
induced S-order, not hidden source relations. At most six vertices are permuted.

## Sufficiency, finite coarsest partitions and witnesses

Evaluate claims only on histories with P1(S)K(T|S)>0; keep zero-mass rows but
assign them null class IDs. Summary R is sufficient for target F iff F is
constant on every supported R-class, equivalently F=g(R) on this finite domain.

For each target, define its predictive class by [base,target signature]. This
is the unique coarsest partition refining the public base and preserving this
particular finite target. It is not universal minimal history, minimal bit cost,
posterior statistical sufficiency, or a dynamically closed state representation.
Class IDs for every candidate/target are assigned by first appearance in the
supported history scan. Class members list global history IDs in increasing
order; keep representative signatures and exact summed joint masses. Across
ten cases the masses sum to10, not1: they are per-case design masses, with no
prior distribution over source profiles. Do not normalize them into a pooled
posterior or interpret class mass as an observer's source probability.

For each candidate/target, retain sufficiency plus first_collision. Scan supported
histories in the fixed order and compare each against the first representative
of that candidate key. First differing target signature supplies the witness;
store only the two history IDs, whose case/state/target data are retained.

Retain the complete9x9 candidate refinement matrix and4x4 target refinement
matrix: row A refines column B iff equal A-class implies equal B-class on all
supported histories. For every candidate/target, also retain the class count
of their common refinement [candidate key,target signature]. Check minimality
in this finite sense: sufficiency iff no candidate class splits, and every
sufficient candidate partition refines the corresponding target partition.
No sufficiency assertion is justified only by matching class counts.

## Prespecified controls

- In Ferrers6, S_star={1,4,5,6} (mask57) and S_path={1,2,4,5} (mask27), T empty,
  have counts[1,4,3,0], the same token, same tagged membership and graded counts.
  Repeat means coincide. Under independent r=1/2, Var(R)=15/16 versus13/16;
  under parity-adaptive r=1/3,4/9 versus32/81. The joint atom N=3,R=0 has
  probability1/16 or2/81 for the star and zero for the path. These histories
  are supported: joint mass1/1024 or1/324, respectively, for each source state.
- In ferrers6_fixed, S={2,5} (mask10) versus S={4,6} (mask20), T empty, have
  the same plain counts[1,3,1,0] and unmarked order but repeat mean R=1/4
  versus1/2. The relation is eligible--eligible versus fixed--eligible. Graded
  counts and correctly fixed-marked orders distinguish them.
- Graded counts plus token preserve future means in every case: each chain
  support of size k has inclusion r^k (IID), or1/2 for nonempty common-coin
  support; empty supports always have inclusion one. This need not preserve
  full future count laws, as the star/path example shows.
- Marked-order isomorphism plus token preserves future count laws under these
  exchangeable laws. It is not necessary: the Ferrers up-star mask57 and
  down-star {1,2,3,6} mask39 are nonisomorphic but have equal entire joint
  count laws. Direction reversal preserves the counted chain sizes here.
- Isomorphic one-edge S={1,4} (mask9) and S={2,5} (mask18), T empty, have the
  same marked-order summary and count law but different fully labeled record
  laws. For example ID1 has repeat probability1/2 versus0 in independent.
- Under parity_hole, odd S and S empty have the same future empty-record law
  (with ordinary fixed endpoints), despite differing full intermediate records
  and even policy tokens. Thus full records can be unnecessarily detailed for
  a specified future law. No general dispensability of history follows.
- For common_coin, current counts plus token preserve the full count law;
  the corresponding claim fails for IID adaptive acquisition. Preserve this
  context dependence rather than declaring a universal summary.
- The original Ferrers6/S3 full-S endpoint collision also crosses the pooled
  source boundary under independent: final T empty, same public base/counts
  and means but different repeat count laws. Bare mask laws alone would miss it.

## Native exact interface

One integrated fixed input, exactly
{schema_version:"det8-qr05g-problem-v1",family:"qr05f_ten"}.
Reject all other keys/types/values, including under -O. The returned analysis
contains the full ten-case universe; no external input format/SDK is introduced.

```text
analysis:{cases,histories,candidate_partitions,target_partitions,assessments,
 candidate_refinement,target_refinement,counts}
cases:[{case_index,profile,design,density,past,fixed,eligible,stage1_inclusions,
 states}]
states:[{mask,probability,kept,past,policy_token,tagged_present,chain_counts,
 graded_counts,unmarked_order,marked_order,repeat_rows,count_law,
 count_mean,count_covariance,coefficient_mean,coefficient_covariance}]
repeat_rows:[{mask,probability,kept,past,chain_counts}]
count_law:[{counts,probability}]
histories:[{history_id,case_index,stage1_mask,final_mask,conditional_probability,
 joint_probability,current_estimate,omitted_terms,candidate_classes,target_classes}]
candidate_classes:{candidate_name:class_id|null}
target_classes:{target_name:class_id|null}
candidate_partitions:{name:[{class_id,members,joint_mass,key}]}
target_partitions:{name:[{class_id,members,joint_mass,base,signature}]}
assessments:{candidate_name:{target_name:{sufficient,first_collision,
 common_refinement_classes}}}
first_collision:null|{left_history,right_history}
counts:{cases,states,positive_states,repeat_rows,positive_repeat_rows,histories,
 positive_histories,zero_histories,candidates,targets,current_estimator_cells}
```

Candidate key is [context,final kept,final past,...appended fields], with every
append item as described (counts/graded/canonical arrays are single items).
Target base is [context,final kept,final past]. Target signatures are respectively
the four Fraction-string current estimates, four Fraction-string means,
the stored count_law, and a list of {kept,past,probability} for positive-probability
repeat rows in increasing U-mask order. Count-law atoms are sorted lexicographically
by the four integer counts; zero-mass atoms are omitted but repeat rows retain zeros.

States/repeat rows use increasing masks. All counts, IDs, degrees, canonical codes
and class IDs are native integers; flags native Booleans; density, probabilities, estimates,
means and covariance entries canonical Fraction strings, including integers.
Observed past lists use local indices in sorted kept; source past uses original
IDs. Native dict/list only, string keys, no float, tuple coercion or bool/int
equivalence. All exact arithmetic components fit4096 bits. Matrices use the
candidate/target orders above; every entry is Boolean. No unlisted wire fields.

Sources bound at capture: README.md, compression.py, reference_qr05g.py, study.py,
test_qr05g.py, test_capture.py. Pin QR-05F results SHA256
`0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917`
and its ten priors. Reproduce all608 first rows,6,804 transcript laws/current
estimates and6,804 conditional-repeat probabilities directly against pinned
QR-05F JSON, never its executors. Preserve earlier geometric/quantum witnesses
by identity, not new physics tests. Whole-aggregate native JSON round trips and
normal/optimized tests must pass before capture. Capture is create-only; replay
is read-only and exact. Outcomes go in RESULTS.md; post-freeze source changes
require a new version, never overwriting the original artifact.

## Attribution and interpretation

Grouping histories by equal declared predictive signatures is a standard
predictive-equivalence construction, not a new physical principle. Related
foundations include Shalizi and Crutchfield's
[computational mechanics](https://arxiv.org/abs/cond-mat/9907176) and their
[statistical-relevance comparison](https://arxiv.org/abs/nlin/0006025).
This gate does not establish their full-process epsilon-machine conclusions:
it tests a finite repeated-observation experiment with a specified question
family. No stationarity, infinite-future equivalence, recursive state update,
information-bottleneck optimum or ontology is inferred.

## Reproduction

From the checkout root, use the existing Python environment; no dependencies
are added. Use a fresh external cache for each invocation (also under -O):

```sh
qr05g_test_cache=$(mktemp -d /tmp/det8-qr05g-tests.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05g_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05g-predictive-compression-2026-09-06

qr05g_optimized_test_cache=$(mktemp -d /tmp/det8-qr05g-opt-tests.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05g_optimized_test_cache" -m pytest -q -p no:cacheprovider docs/validation/qr-05g-predictive-compression-2026-09-06

qr05g_capture_cache=$(mktemp -d /tmp/det8-qr05g-capture.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05g_capture_cache" docs/validation/qr-05g-predictive-compression-2026-09-06/study.py

qr05g_replay_cache=$(mktemp -d /tmp/det8-qr05g-replay.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr05g_replay_cache" docs/validation/qr-05g-predictive-compression-2026-09-06/study.py --verify

qr05g_optimized_replay_cache=$(mktemp -d /tmp/det8-qr05g-opt-replay.XXXXXXXX)
.venv/bin/python -I -O -X pycache_prefix="$qr05g_optimized_replay_cache" docs/validation/qr-05g-predictive-compression-2026-09-06/study.py --verify
```

The capture command succeeds only if results.json is absent. An existing result
must be verified, never deleted to recapture. Runtime metadata is descriptive
and outside the exact mathematical suite; this is not an SDK performance test.
Canonical JSON uses sorted keys, compact comma/colon separators and a trailing
newline. The compact encoding retains every row and signature without the
large whitespace expansion of these deeply nested repeat-record partitions.
