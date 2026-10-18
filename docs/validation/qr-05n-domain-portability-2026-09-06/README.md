# QR-05N protocol: finite domain-portability stress

6 September 2026. Prospective bounded investigative gate.
Research base: pushed QR-05M commit
`c991bc2fba906d88824e337e41c28d651f9c7674`.

## Question fixed before closure search

Keep the observed motif M and summary C=(frame,B,M) unchanged. Does its
complete next-summary law remain closed after appending every 3-by-3
two-color layered incidence pattern in both directions?

The source inventory below was checked combinatorially and by relation-only
enumeration before this protocol. No new D/B/C partition or closure outcome
was searched before fixing the family and decision rules. A failure is a
valid investigative outcome: retain the first exact counterexample, do not
silently refine C or replace M. A success certifies only this finite family
and the supplied observation law.

No source/feature selection based on outcome, adaptive rates, correlated
thinning, new physical law, RET integration, Lean installation or earlier
artifact/source modification is authorized by this gate. Synthetic controls
do not enlarge the certified domain. All prior work remains pinned.

## Append-only source family and explicit labels

Vertices are original IDs 0 through 7. Fixed bottom 0 and top 7 bound every
interior vertex. The first six profiles, in this order, are exactly M's:

0. ferrers6: i+1 < j+4 iff i<=j, i,j in {0,1,2}.
1. standard_example3: i+1 < j+4 iff i!=j.
2. chain6: the total order.
3. ferrers6_fixed: profile0 but vertex3 also fixed.
4. path6: 1<2,1<4,3<4,3<6,5<6.
5. cycle4_edge: 1<4,1<6,3<4,3<6,2<5.

Append 512 profiles named "layered_oe_000" through "layered_oe_511", then
512 named "layered_eo_000" through "layered_eo_511". For incidence integer
h in 0..511, bit 3*i+j denotes the cell pairing odd vertex 2*i+1 with
even vertex 2*j+2, i,j=0,1,2. In oe profiles a set bit gives odd<even;
in eo profiles the SAME indexed bit gives even<odd. Reversal does not
transpose the bit matrix. No other interior comparisons are present.

Thus profile index 6+h is oe(h), and 518+h is eo(h). All appended profiles
have fixed [0,7] and eligible [1,2,3,4,5,6]. Profile3 alone has fixed [0,3,7]
and eligible [1,2,4,5,6]. Density is the exact string "12". Public frames
[density,fixed IDs,eligible IDs] are numbered by first occurrence.

Original-ID parity is the supplied named color mark. Sorted original IDs
are wire order, NOT a causal/topological order. A valid comparison such as
3<2 must survive induction and chain recognition. A past array lists sorted
local indices of strict predecessors; an index can exceed its target index.
Supplied strict relations must be irreflexive and transitively closed.
They are not cover/Hasse graphs.

For every profile in order, enumerate eligible masks ascending. Keep fixed
vertices, sort surviving original IDs and restrict the supplied strict
relation. Deduplicate by [frame,kept,past], with first-occurrence IDs.
Every profile/mask alias remains visible; aliases are never weights,
features or current-state source labels.

Exact declared inventory: 1,030 profiles, 65,888 aliases, 2,470 states and
99,180 fine induced-subset atoms. The first 257 states remain M's prefix.
There are 2,213 new states. Relations alone establish this inventory.
The pure two-orientation family has
sum_(o,e) binom(3,o)binom(3,e)(2*2^(oe)-1)=2,322 states;
the remainder is old-domain observations not in that family.

Hard deterministic bounds: at most 2,579 states, 100,393 fine atoms,
six eligible vertices with at most three per color, source masks <64,
incidence masks <512, exact integer/rational components <=4,096 bits,
and canonical captured artifact <=64 MiB. Check counts/caps explicitly.
No dense four-variable residual tensors need be stored. Descriptive
runtime measurements are not application benchmarks.

## Unchanged observation law and exact coefficients

For an observed S, retain each currently eligible odd vertex with rate x
and each eligible even vertex with rate y, independently. Fixed vertices
always remain. All structurally attainable induced observations U are
present, including atoms that have zero probability at selected rates.

    P_(x,y)(S,U)=x^o(1-x)^(O-o)y^e(1-y)^(E-e).

O,E count currently eligible colors; o,e count survivors. The rate domain
is [0,1]^2. Encode the exact polynomial as a padded 4x4 signed integer
table, x-power outermost. Fine atoms retain explicit coefficient tables
for direct comparison with prior evidence; internal caches may share
their 100 possible color-size kernels.

Rows must normalize coefficientwise; all four corners are deterministic.
(1,1) is identity and (0,0) sends each frame to its fixed-only state.
Fresh independent stages obey P_(x,y)P_(a,b)=P_(xa,yb). Equal or reused
random coins and observation-dependent rates are not tested premises.

The fine-law composition follows by independent per-vertex survival.
For any actually closed coarse quotient, additionally check all 256
coefficient cells of x,y,a,b for every structural start/end pair.
Do not replace four independent variables with a same-rate grid.

## Unchanged calculus, generalized label handling

N_q counts chains from 0 to 7 with q internal vertices, q=0,1,2,3;
N_0=1. Each vertex set counts once. A selected internal set is a chain
when every unordered pair is comparable in the supplied strict relation
and the endpoint relations hold. Equivalently traverse directed chains;
numeric ID order must not enter the criterion.

D_qoe counts these chains by eligible odd/even support. B_qroe counts
ordered pairs of chains by their eligible union. Self-pairs, both ordered
copies of distinct pairs and multiplicities of equal supports remain.
Fixed internal vertex3 can belong to chains but never eligible support.
D has shape4x4x4; B shape4x4x4x4; B_0r=D_r.
These determine exact first and second count moments, not a full law.

M is precisely M's existing eligible color-layered induced K2,2 count.
Four observed eligible vertices contribute once iff there are two of each
named color, no same-color comparisons in either direction, and all four
cross comparisons uniformly directed either odd<even or even<odd.
Outside vertices/edges do not disqualify an induced support. Use transitive
relations, not cover edges. The recognizer reads only (kept,past,eligible);
no profile, state ID, mask, class or transition lookup is an input.
Its output is a sorted list of sorted four-original-ID supports.
The candidate value is the length of that list, between0 and9 here.

Keep two partitions, in order: "pair_graded"=(frame,B) and
"motif_pair"=(frame,B,M). Class IDs are assigned by first state occurrence.
Retain exact keys and sorted member lists. Do not infer equal fibers
from equal cardinalities and do not construct a stable repair in this gate.

For each state, recompute the D/B support-graded expectation updates and

    E[M(U)|S]=x²y²M(S).

The motif identity follows from induced support heredity and linearity;
overlapping supports are not assumed to survive independently.
It is a premise-based general expectation identity, distinct from finite
complete-law closure. A count up to9 is not a Bernoulli observable.

## Closure decision and counterexamples

Push every complete fine polynomial row to both partitions. For each,
scan classes by ID, comparing its first member with each subsequent member
in ascending order. Find the first differing target class in sorted order
over the union of their structural supports, with absent targets interpreted
as zero tables. This fixes the first-collision ordering.

If a partition fails, retain its witness; quotient_rows=[] and
semigroup=null. Do not suppress the witness or substitute a refined
partition. If it closes, retain a representative quotient only after every
member row agrees; independently verify normalization and composition.

At suite level retain both first witnesses, all22 exact evaluation points
below and the witnesses' full count-law polynomials. A next-C difference
need not imply a difference in full N count law; record that comparison
as measured. Current equal summary keys and unequal target coefficients
must be independently verified. At least one point of the16-node grid
must distinguish a nonzero polynomial of these degree bounds.

Audit rates: the16 grid points {0,1/3,2/3,1}² followed by
(1/2,1/2),(2/5,3/7),(1/5,4/5),(1/2,1/3),(0,2/5),(3/7,1),
with duplicate removal preserving order. Cache exact evaluations but
retain structural zeros. Coefficient equality is the all-rate certificate;
selected-rate checks additionally audit positivity and boundary behavior.

## Exact M restriction, including a possible global failure

Pin M's canonical results.json by published hash. The first six source
records/257 states must reproduce all old frame/kept/past/mask/count/D/B
values, eligible colors and motif supports/counts. Filter aliases to the
first six profiles when comparing old provenance; added aliases remain
explicit. Every old fine polynomial and induced target matches M and
stays in the old subset-closed prefix.

Compare old pair and candidate class assignments by actual membership
maps, not counts. The first-occurrence vectors must agree with M's old
pair vector and observable vector. Pull back expanded fibers to the old
domain. Compare every old state-pushed B and C row with M.
The extra class keys cannot affect old restrictions.

Always reconstruct a quotient of the restricted old C domain, using only
old members. Its memberships, representative rows and full composition
certificate must equal M's110-class quotient. This remains valid even if
the expanded partition fails globally. Only if global C closes, also
restrict its actual quotient to the old class image and verify that image
is closed. Never fabricate a global quotient merely because the restricted
old quotient exists.

N deliberately does not recompute color-order canonicalization, stable
refinement rounds, joint B traces or covariance towers over the larger
family. Those earlier experiments remain pinned; this gate preserves their
observation/feature/kernel inputs on the old prefix but makes no expanded
trace-minimality, stable-repair or physical correspondence claim.
Do not describe the slimmer N output as a whole-schema copy of M.

## Executor interface and retained analysis schema

The exact top-level input is
{"schema_version":"det8-qr05n-problem-v1","family":"qr05n_layered_iid"}.
Reject missing/extra fields and non-native/subclass types. Mathematical
wire data are native dictionaries with native string keys, lists, integers,
booleans, strings and null only; no floats or coercions.

Both independent executors expose analyze(problem) and
motif_supports(kept,past,eligible). The complete analysis has exactly:

- frames: [{frame_id,density,fixed,eligible}].
- profiles: [{profile_index,name,frame_id,past,state_ids}], M-compatible.
- states: [{state_id,frame_id,mask,kept,past,aliases,color_sizes,
  chain_counts,mean_graded,pair_graded,motif_supports,motif_count,
  classes,transitions,summary_laws}].
  aliases are {profile_index,mask}; classes has the two partition names.
  Fine atoms are {target_state,coefficients}; pushed atoms are
  {target_class,coefficients}; atoms are target-sorted, full structural rows.
- partitions: {"pair_graded":[{class_id,key,members}],
  "motif_pair":[{class_id,key,members}]}.
- closure: each name maps to {closed,first_collision,quotient_rows,semigroup}.
  first_collision is null or {class_id,left_state,right_state,target_class,
  left_coefficients,right_coefficients}. quotient_rows are
  {class_id,representative_state,transitions}.
  Semigroup uses M's {verified,rows,totals} schema, rows
  {class_id,transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual},
  totals {transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual}.
- expected_updates: {verified,rows,coefficient_cells}; each row is
  {state_id,mean_features:64,pair_features:256,coefficient_cells:5120,
  max_abs_residual:0}, reconstructed exactly as M's D/B expected-update rows.
- motif_expected_update: {verified,rows,coefficient_cells}; rows are
  {state_id,coefficients,expected_coefficients,max_abs_residual:0};
  retain actual and expected4x4 tables and all16cells per state.
- counts: {frames,profiles,aliases,states,partitions,fine_transition_atoms,
  summary_transition_atoms,transition_coefficient_cells,mean_feature_cells,
  pair_feature_cells,motif_support_occurrences,motif_positive_states,
  max_motif_count,expected_update_coefficient_cells,
  motif_expected_update_coefficient_cells,closed_partitions,
  quotient_transition_atoms,semigroup_intermediate_paths,
  semigroup_coefficient_cells}.

All counts are derived from retained records. Polynomial normalization,
subsetting, label independence and exact caps are explicit guards, not
Python asserts in executors or runner. Failed expected identities are errors;
failed candidate closure is a retained research result.

Primary route: observed chain vertex sets and ordered support unions,
direct binomial expansion, explicit motif quartets and polynomial row sums.
Reference route: source-directed-chain subsets / full induced count outcomes,
raw moments of the exact count law rather than chain-pair enumeration,
cached rational-grid interpolation of kernel laws, common-neighbor motifs.
Compute features once per distinct observation, not once per source alias.
Neither executor reads files, captured artifacts, the other route or earlier
executors. Locally carried utilities from each own lineage are documented.

## Prespecified controls and testing

Retain source/mask-based locations for these controls, not hardcoded new IDs:

- A descending-ID edge, oe incidence8 (3<2), and its order reverse:
  the full count vector is [1,6,1,0], and N2 must not disappear.
- Complete incidence511 in both orientations: counts[1,6,9,0],
  M=9, with nine distinct overlapping supports and mean9x²y².
- Empty incidence0 duplicates across both directions; it adds aliases,
  not source-weighted states or duplicate observations.
- The old path/cycle equal-B/unequal-next-B witness remains intact on the
  restricted M domain.
- M's two fixed-only states, fixed interior eligibility and boundary rates.
- All M recognizer controls can be carried as unit tests, especially
  original-ID marks versus local positions, order reversal, fixed exclusion,
  wrong color cardinality, and overlapping support multiplicity.

Independent tests reconstruct source incidence matrices, observations,
chains/pairs/motifs, candidate keys and pushed rows. They check the exact
M restriction, negative schema/native guards, corner/expectation laws,
closure and any quotient coefficients. Mutation coverage must include
incorrect descending-label chain counts, a reversed bit convention,
alias loss/weighting, missing/duplicated motif supports, same-count wrong
fibers, altered coefficients, false closure/omitted failure, fabricated
failed quotients and invalid prior restriction maps. Test negative cases
in temporary/in-memory data, never by altering real frozen evidence.

Use normal and optimized Python3.11 with external task-specific bytecode
caches, no pytest repository cache, Ruff check/format and source whitespace
checks before freeze. Subprocess guards must remain active under -O.

## Runner and immutable capture lifecycle

Frozen sources: README.md, portability.py, reference_qr05n.py, study.py,
test_qr05n.py and test_capture.py. RESULTS.md and the roadmap are reports
outside the ledger. Pin18 prior artifacts: M plus its17priors.

The runner independently validates the complete retained math, rates,
counts, controls, witnesses and old-domain restriction using pinned JSON
only for postconstruction comparison. Capture is canonical, exclusive
create-only, <=64MiB, with source/prior ledgers, runtime metadata and
readback. An existing artifact cannot be overwritten. Source changes after
capture require separately versioned evidence, never silent regeneration.

Replay is read-only and reruns the exact suite under frozen source/prior
identities; normal and optimized replays must preserve bytes. Finish with
independent JSON-only postflight importing no executor, runner or tests.
Source/prior ledgers and artifact identity are checked before and after.
Preserve all unrelated checkout work; publish only this gate and roadmap
by scoped commit/push, then verify remote HEAD and artifact identity.

## Interpretation and next decision

This tests portability of a record-computable coarse predictor under an
explicit sampling law. It does not establish universal sufficient memory,
minimum storage, event growth, physical time, a metric, quantum theory,
gravity, ontology, empirical apparatus/noise calibration or a RET adapter.

If C fails, the next gate should study the retained obstruction and propose
a new explicit feature under a separate protocol; no automatic repair is
executed here. If C passes, the next decision is a separately bounded
larger-support or different-shape stress test, not general sufficiency.
In either case the motif expectation proof and M's finite success survive
under their original premises. Broader-domain research is not evidence
that a conflict with known observables can be dismissed as noise.
