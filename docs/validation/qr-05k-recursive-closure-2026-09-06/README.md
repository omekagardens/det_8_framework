# QR-05K — recursive observation-summary closure

Protocol recorded before implementation, 2026-09-06.
Research base: `a2d3b5f3ad7637939835140a9fe9acc6f66b28e2`.
Isolated mathematical research; no RET/core imports or edits, dependency
installation, empirical data, new physical laws, ontology or Lean installation.
All earlier evidence remains immutable.

## Question

Can a present summary determine the complete probability law of its next
realized summary under a declared observation procedure? This is stronger
than determining a mean or covariance at a fixed observation stage.
Separate three statements:

1. Fine observations compose under fresh independent thinning.
2. Expected single-chain and pair-union feature counts update diagonally.
3. A summary admits a well-defined stochastic update kernel on its classes.

This gate tests the third claim coefficientwise on a finite, subset-closed
observed-state space. It does not assume that expected updates imply stochastic
closure, or that a static count-law summary is an arbitrary dynamical state.
Either a retained failure or a verified bounded quotient completes the gate.
No outcome for pair-summary closure is prescribed.

## State domain and information access

Use original IDs0..7 with fixed bottom0 and top7, density metadata"12".
Interiors are a_i=i+1,b_j=j+4 for i,j=0..2. Sources, in order:
ferrers6 with a_i<b_j iff i<=j; standard_example3 with iff i!=j;
chain6 with total order; ferrers6_fixed with the Ferrers relation and fixed
[0,3,7]. Other sources fix[0,7]. Every interior is above0 and below7.
Eligible IDs are increasing1..6 excluding fixed interiors. All source past
relations are transitively closed. Parity marks eligible original IDs only;
fixed interiors are deterministic and never receive a sampling probability.

A public frame is [density,fixed IDs,eligible IDs]. Frames are registered at
first source occurrence, giving two frames. For each source enumerate all
masks of eligible vertices, ascending. Kept IDs are fixed plus selected
eligible IDs, sorted; induced past uses local positions in that kept list.
Deduplicate observations by [frame,kept,induced past] at first occurrence.
Retain all aliases (source index,mask). This gives224 aliases and188 unique
labeled states. Different hidden sources can issue the same observation.
A source alias is not a probability weight, and source names never enter
summary keys.

Every induced successor U of every S must resolve to a state in this domain.
Include all states, even aliases that were zero-probability diagnostics under
an earlier current-history design. No old current-design token, final T,
first-stage mass, or empirical source prior is carried into the new state.
This is an explicitly changed state space for a new update question; it is
not a reinterpretation of the previous positive-history partitions.
No requested final record is conditioned to survive the update.

The fine state is the entire supplied observation S. A summary-only observer
has the public frame and its summary class, not a hidden source, the original
S relation, or the labeled retained mask. A stochastic quotient predicts the
next summary's law; it is not a deterministic updater given a retained mask.

## Independent thinning and exact transition polynomials

Under rates(x,y) in[0,1]^2, independently keep each eligible odd member of S
with probability x and each even member with probability y. Fixed members
always survive. If S has O,E eligible color counts and U has o,e, then

```text
P_(x,y)(S,U) = x^o(1-x)^(O-o) y^e(1-y)^(E-e), if U is induced from S;
P_(x,y)(S,U) = 0 otherwise.
```

Each transition has integer monomial coefficients, bidegree at most(O,E),
hence at most(3,3), padded4x4 with x power first. Retain every structurally
possible transition, including those zero at chosen boundary rates. Signed
coefficients are valid; nonnegativity on the square follows from the subset
formula. Row coefficients sum to the constant-one polynomial. At(1,1) the
kernel is identity, at(0,0) it retains the frame's fixed-only state, and each
mixed corner is deterministic. Boundary edges need not be deterministic.

Two independent stages at(x,y) and(a,b), using fresh independent per-vertex
decisions across stages, give

```text
P_(x,y) P_(a,b) = P_(xa,yb).
```

Proof: each vertex survives both stages with the product of its two rates,
and the surviving indicators remain independent across vertices. This is
observation composition, not physical time or event-growth dynamics.
Reused random coins and adaptive rates are outside this fixed-rate premise.

## Summaries

N_q(S), q=0..3, counts q-internal-vertex chains between fixed probes, once per
vertex set; N0=1. Let D[q,o,e] count chains by eligible odd/even support size.
Let B[q,r,o,e] count ordered chain pairs by the eligible color sizes of their
support union, retaining self-pairs and both off-diagonal orientations.
B[0,r]=D[r]. Chains with identical eligible supports retain multiplicity.

Four partitions, in this order:

- mean_graded: key[frame,D].
- pair_graded: key[frame,B].
- color_order: key[frame,color-preserving fixed-marked canonical order code].
- full_record: key[frame,kept,induced past].

The color-order code anchors all fixed vertices individually in increasing
order, then permutes remaining vertices. For positions i,j, relation code is
sum2^(i*n+j) over order relations. Color code is sum2^i over eligible odd
positions. Minimize(relation,color) lexicographically; code[n,relation,color].
Fixed vertices are not decorated. Density is supplied metadata, not a
measured quantity or inferred spacetime scale.

Register class IDs by first state occurrence, retain sorted state members,
and compare the4x4 refinement matrix on this same state domain. No class
masses are invented.

## Expected updates versus strong closure

For each feature with support/union color size(o,e),

```text
E[D_qoe(U)|S] = x^o y^e D_qoe(S)
E[B_qroe(U)|S] = x^o y^e B_qroe(S).
```

The proof is indicator survival and linearity. Verify these equations in all
16 coefficient cells for every feature, including padding zeros.
These equations alone do not specify the joint distribution of those features.

For a partition Q define the pushed row to successor class c:

```text
L_Q(S,c;x,y) = sum_{U:Q(U)=c} P_(x,y)(S,U).
```

Strong closure means every coefficient of every L_Q row agrees for S,S'
in the same current Q class. Then, and only then, define a quotient row
Qbar(Q(S),c) using a representative. On failure, store the first collision
against the first class representative and the first differing target class;
do not emit a quotient kernel for that partition.

All polynomial rows have bidegree at most(3,3); equality is a full-domain
coefficient identity, not an inference from a few selected rates. The
independent reference reconstructs rows by exact tensor interpolation on
{0,1/3,2/3,1}². Four roots in each variable imply uniqueness under this degree
bound. See the standard [NIST DLMF interpolation identity](https://dlmf.nist.gov/3.3.i).
This finite proof and computational verification are not Lean formalization.

If P E=E Qbar denotes lifting coarse functions to fine states, strong closure
and fine composition give E Qbar_(x,y) Qbar_(a,b)=E Qbar_(xa,yb). Every class
is represented, so quotient kernels inherit composition. Additionally verify
this coefficientwise: multiply transition polynomials in independent variables
(x,y,a,b), each with degree at most3, and compare with the product-rate row.
A coefficient c_ij on the right embeds at powers(i,j,i,j). Check all256 cells
per reachable two-step target, including zero residual cells. Reusing the
same parameter pair can create degree-six polynomials and is not certified
by a two-variable four-node grid.

## Frozen executable interface and wire schema

analyze(problem) accepts only the exact native dict
{"schema_version":"det8-qr05k-problem-v1","family":"qr05j_recursive_iid"}.
Reject unknown keys/values, subclasses, and native-type substitutions normally
and with-O. Standard library only; no I/O, captured-artifact reads, earlier
executor imports, or imports of the other route.

Primary closure.py uses observed induced relations, observed chain/pair
counts and binomial expansion of transitions. Reference reference_qr05k.py
uses source-chain indicators and full count-law moments for summaries, and
exact grid interpolation for transition coefficients. It does not count
observed chain pairs or use binomial expansion for transition coefficients.
Both independently enumerate/deduplicate states and form every partition,
pushforward, closure witness, quotient and composition check.

Exact output schema:

```text
{
 frames: [{frame_id,density,fixed,eligible}],
 profiles: [{profile_index,name,frame_id,past,state_ids}],
 states: [{
   state_id,frame_id,mask,kept,past,aliases:[{profile_index,mask}],
   color_sizes:[O,E],chain_counts:[N0,N1,N2,N3],
   mean_graded: D[4][4][4], pair_graded: B[4][4][4][4],
   color_order:[n,relation_code,color_code],
   classes:{mean_graded:id,pair_graded:id,color_order:id,full_record:id},
   transitions:[{target_state,coefficients:4x4}],
   summary_laws:{Q:[{target_class,coefficients:4x4}]}
 }],
 partitions:{Q:[{class_id,key,members}]},
 partition_refinement:4x4 booleans,
 closure:{Q:{
   closed:boolean,
   first_collision:null|{class_id,left_state,right_state,target_class,
                         left_coefficients:4x4,right_coefficients:4x4},
   quotient_rows:null|[{class_id,representative_state,
                        transitions:[{target_class,coefficients:4x4}]}],
   semigroup:null|{
     verified:true,
     rows:[{class_id,transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual:0}],
     totals:{transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual:0}
   }
 }},
 expected_updates:{
   verified:true,
   rows:[{state_id,mean_features:64,pair_features:256,
          coefficient_cells:5120,max_abs_residual:0}],
   coefficient_cells:962560
 },
 counts:{
   frames,profiles,aliases,states,partitions,
   fine_transition_atoms,summary_transition_atoms,transition_coefficient_cells,
   mean_feature_cells,pair_feature_cells,expected_update_coefficient_cells,
   closed_partitions,quotient_transition_atoms,
   semigroup_intermediate_paths,semigroup_coefficient_cells
 }
}
```

Q ranges over exactly the four partition names in the declared order.
Profile state_ids arrays are indexed by original eligible mask; aliases are
in ascending source/mask scan order. All row atoms are sorted by numeric
target ID. Every structurally attainable atom is present once; identically
zero polynomials are absent. Quotient rows follow class IDs and use the first
member as representative only after all members pass closure.
First collision: scan states ascending against first current-class member,
then choose the smallest successor class with unequal coefficient arrays;
missing atoms are compared as all-zero4x4 tables.

For each closed partition, intermediate_paths counts all two-hop structural
paths through its quotient rows. transition_pairs counts the distinct reachable
(start class,final class) pairs; two-step and one-step target sets must agree.
coefficient_cells=256*transition_pairs, and totals sum row counters.
The full_record quotient is also the fine-kernel semigroup check.
transition_coefficient_cells=16*(fine_transition_atoms+summary_transition_atoms).
Feature totals are188*64 and188*256; expected update checks188*320*16.
closed_partitions and quotient/composition counts are measured, not prescribed.

Only native dict/list with native string keys; count/code/ID/coefficient fields
are native ints, flags native bool, density and other rationals reduced strings.
No float, tuple, Fraction object or implicit bool/int coercion in retained math.
All exact components are capped at4096bits. Descriptive runtime floats belong
only in the outer capture metadata.

## Runner, prior bridge and controls

Pin all15 earlier artifacts. Match every one of224 aliases to J representative
cases0,5,6,9, including source/frame, induced order, colors, counts, D, B and
color-order codes. Match all608 J state occurrences through those profiles,
not only old positive histories. Earlier current-history partitions remain
unchanged evidence and are not relabeled as the new188-state partitions.

Independently audit frame/state/alias closure, coefficient normalization,
expected updates, class assignments, pushforward rows, first collisions,
quotient validity and all four-variable semigroup coefficients.
Also evaluate fine/pushed/quotient rows at22 distinct rates: the16 interpolation
nodes plus(1/2,1/2),(2/5,3/7),(1/5,4/5),(1/2,1/3),(0,2/5),(3/7,1).

Retain these specific controls:

- Ferrers star mask57 versus path27 have equal D but unequal next-D laws.
  The successor mean class of mask41 has probabilities x(1-x)y² and0,
  including1/16 versus0 at half rates. Preserve the selected witness even
  if a different collision is first in enumeration.
- Full record and color-marked order are positive closure controls.
  Mean grading fails; pair grading's outcome must be measured.
- Every frame has its fixed-only absorbing state. All corners deterministic;
  edge randomness remains allowed.
- Verify the covariance tower for each of188 states at four ordered stage-rate
  pairs: ((1/2,1/2),(1/2,1/2)); ((1/3,2/3),(2/5,3/7));
  ((0,1/2),(2/3,1)); ((1,1),(1/3,2/3)).
  Retain mean, within-record covariance, between-record covariance and total
  covariance for all752 rows; total equals the direct product-rate covariance.
  On an odd singleton under two half stages, final variance3/16 splits into
  within1/8 and between1/16.
- A reused Bernoulli-half coin at both stages gives singleton retention1/2,
  not1/4. This is an out-of-premise diagnostic, not an IID semigroup failure.

No larger one-color graphs, empirical apparatus or extra transition policies
are added in this gate. Future generalizations need a separate protocol.

## Acceptance and lifecycle

Both complete native outputs must agree; all independent checks and positive/
negative controls pass normally and under-O. The tests independently reconstruct
subset outcomes, polynomial pushforwards and closure; they must test failed-
partition handling and singular/zero covariance without adding regularization.

Freeze README,closure.py,reference_qr05k.py,study.py,test_qr05k.py and
test_capture.py only after review/tests/formatting. Run isolated Python with a
fresh external bytecode cache. Capture canonical results.json once by exclusive
creation and readback. Replay never overwrites; it checks exact suite, sources,
priors and unchanged result bytes. Sources/priors are checked before and after.
Lifecycle mutations use temporary stub evidence only. RESULTS.md and the
roadmap are human reports outside the frozen source ledger.

Even successful pair closure would concern this finite observed-state family
and this independent-thinning policy family. It does not establish general
Markov sufficiency, minimal memory, deterministic reconstruction, empirical
performance, quantum evolution, event growth, spacetime geometry or gravity.
