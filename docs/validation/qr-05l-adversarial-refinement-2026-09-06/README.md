# QR-05L — adversarial closure and stable refinement

Protocol recorded before implementation, 6 September 2026.
Research base: `2f232c8f795df3eaa5e73ed3c3125e231abdd80e`.
Isolated mathematical research. No RET/core imports or edits, dependency
installation, empirical data, ontology, new physical law or Lean installation.
All previous sources and artifacts remain immutable.

## Question and scope

QR-05K established pair-summary closure on its declared finite family, not
in general. Append a prespecified adversarial pair without changing its
observation law. Test the failure and construct the coarsest strongly closed
refinement of the original pair partition on the expanded finite domain.

A closed expected-feature update, a full next-summary law, a joint sequence
of observed summaries, and a minimum-storage representation are different
contracts. The repair sought is a partition refinement, not an extra moment
tensor. A verified counterexample is a successful investigative result.

Design exploration, not captured evidence, predicts 257 observations, a
109-class B partition that fails, and a 110-class fixed-point refinement.
These are hypotheses to recheck independently, not values to emit without
computation. No refinement-round count or successful compression is assumed
by the mathematical construction.

## Source family and supplied observation frame

Original IDs are 0..7, with fixed bottom 0 and top 7. Every interior vertex
is above 0 and below 7. The source relation is transitively closed. Density
metadata is the supplied string "12", not an inferred geometry or unit.

The first four sources are unchanged from K, in this exact order:

1. ferrers6: interiors a_i=i+1 and b_j=j+4, i,j=0..2, with a_i<b_j iff i<=j.
2. standard_example3: a_i<b_j iff i!=j.
3. chain6: the total order on IDs 0..7.
4. ferrers6_fixed: the Ferrers relation, with fixed vertices [0,3,7].

All other sources fix [0,7]. Append these two height-two interior relations:

5. path6: 1<2, 1<4, 3<4, 3<6, 5<6.
6. cycle4_edge: 1<4, 1<6, 3<4, 3<6, 2<5.

The graph names describe undirected interior comparability graphs. The listed
relations, rather than an arbitrary graph orientation, define the actual
orders. Both are naturally labeled and have no three-interior-vertex chain.

A public frame is [density, fixed IDs, eligible IDs], with eligible IDs the
increasing 1..6 not fixed. Register frames at first source occurrence. For
each source enumerate all eligible masks in ascending order, retain fixed
plus selected IDs sorted, and express induced past relations in local kept
positions. Deduplicate by [public frame, kept IDs, induced past] at first
occurrence. State IDs follow that registration. Retain every source/mask
alias in scan order; aliases are provenance, not probability weights.

There are two frames and 352 aliases. The old 188-state domain is a prefix
and is closed under taking induced successors. Appending sources adds aliases
to some old observations; it does not change their observed features or
outgoing fine transitions. The new state total is measured, bounded by 316
(old 188 plus at most 128 new aliases). All valid successor masks are present,
including observations that had zero mass in an earlier acquisition design.

Hidden source names, aliases, old current-design tokens, first-stage masses
and an earlier final record do not enter compressed summary keys. A summary
observer has the public frame and current summary class, not an additional
labeled retained mask or hidden source. The full-record baseline explicitly
retains the labeled observation. A quotient predicts a stochastic update;
no deterministic mask updater is asserted.

## Observation calculus

Independently retain each currently observed eligible odd vertex with
probability x and each eligible even vertex with probability y, where
(x,y) ranges over [0,1]^2. Fixed vertices always survive. For an induced
successor U of S, with eligible color sizes (o,e) and (O,E), respectively,

```text
P_(x,y)(S,U) = x^o (1-x)^(O-o) y^e (1-y)^(E-e).
```

All other transitions have zero probability. Retain every structurally
attainable transition, including selected-rate zeros. Store the integer
monomial coefficients in a padded 4x4 table, x-power then y-power. The
bidegree bound is (O,E) <= (3,3). Identically zero atom polynomials are absent.
Rows normalize coefficientwise. All four corners are deterministic; (1,1)
is identity and (0,0) is the unique frame-specific fixed-only observation.
Boundary edges may be random.

Fresh independent decisions across two stages give

```text
P_(x,y) P_(a,b) = P_(xa,yb).
```

Each vertex survives both decisions with the product rate, independently of
other vertices. Reused coins or arbitrary adaptive rates are not covered.
This is composition of supplied observations, not physical time or event growth.

Let N_q(S), q=0..3, count chains with q internal vertices between the fixed
probes, once per vertex set; N0=1. Let D[q,o,e] count chains by their eligible
odd/even support sizes. Let B[q,r,o,e] count ordered chain pairs by the
eligible color sizes of their support union. Retain self-pairs, both
off-diagonal orientations and multiplicity of equal eligible supports.
Fixed interiors supply no sampling factor. Then B[0,r]=D[r] and

```text
E N_q = sum D[q,o,e] x^o y^e
E[N_q N_r] = sum B[q,r,o,e] x^o y^e
Cov(N_q,N_r) = E[N_q N_r] - E N_q E N_r
E[D_qoe(U) | S] = x^o y^e D_qoe(S)
E[B_qroe(U) | S] = x^o y^e B_qroe(S).
```

Verify all 16 coefficients for all 64 D and 256 B expected-feature updates
on every state, including padding zeros. These identities do not determine
the next realized B distribution.

## Basic partitions and strong closure

The four basic partitions remain ordered as:
mean_graded, pair_graded, color_order, full_record. Their keys are

```text
[frame,D]
[frame,B]
[frame,fixed-anchored named-color canonical order code]
[frame,kept IDs,induced past].
```

For the canonical order code, anchor all fixed vertices individually in
increasing order, then permute the remaining vertices. For positions i,j,
the relation integer is sum 2^(i*n+j) over order relations; the color integer
is sum 2^i over eligible odd positions. Minimize (relation,color)
lexicographically. Code is [n,relation,color]; fixed vertices are not colored.
Class IDs follow first state occurrence; member IDs are sorted.

For any partition Q, push the fine kernel to next classes:

```text
L_Q(S,c;x,y) = sum_{U:Q(U)=c} P_(x,y)(S,U).
```

Q is strongly closed only when every complete polynomial row agrees within
each present Q class. On failure retain the first collision: scan states
against their class's first member, then choose the first differing numeric
target class, with absent atoms interpreted as zero 4x4 tables. A failed
partition has no quotient or semigroup certificate.

For a closed partition, choose each class's first member only after checking
every member. Its quotient has coefficientwise row normalization and inherits
composition via P E=E Qbar and the injectivity of lifting class functions.
Additionally verify all 256 four-variable cells per reachable source/target
class pair. A coefficient c_ij in Qbar_(xa,yb) occupies powers (i,j,i,j).
One-hop and two-hop structural target sets agree; all structural paths count,
including those with selected-rate-zero probabilities.

This is a standard finite aggregation question, not a new physical law.
Background: [Buchholz (1994), exact and ordinary lumpability](https://doi.org/10.2307/3215235).
The actual closure and coarseness arguments for this gate are stated here.

## Canonical refinement certificate

Start Q0 at the basic pair_graded partition, including its public frame.
At each round compute complete L_Qr rows and define

```text
Q_(r+1)(S) = class of [ Q_r(S), L_Qr(S, . ; x,y) ].
```

Register the new classes at first state occurrence. The previous class MUST
remain in the key: grouping solely by outgoing rows could merge distinctions
already required by B. Rows are sparse sorted lists of all structural targets,
each carrying its complete coefficient table. Such probabilities are positive
in the open square, so an attainable aggregate cannot be identically zero.

Retain round 0 and every strict successor partition, followed by its own
pushforward-row check. The terminal round is stable exactly when applying
the rule again gives the same state-class vector, not merely the same number
of classes. Each nonterminal round strictly splits; at most N-|Q0| strict
rounds can occur before stability. No artificial round truncation is permitted.

Every non-first child of a split parent receives a separation witness. The
left state is the parent's first current member; the right state is that
next child's first member. Compare CURRENT-round pushed rows and retain
the smallest differing target class and both zero-padded coefficient tables.
child_class_id belongs to the NEXT round; parent_class_id and target_class
belong to the CURRENT round. Emit witnesses in ascending child_class_id.
The terminal round has no separation witnesses.

The terminal partition Q* is strongly closed and refines B. It is the
coarsest such refinement on this finite domain by this induction:

- Let R be any strongly closed partition refining B.
- If R refines Q_r, each Q_r block is a union of R blocks.
- Equal R states have equal masses to every such union at every rate.
- Thus the update rule cannot split an R block, and R refines Q_(r+1).
- At termination every admissible R refines Q*, which itself is admissible.

This is an ordinary mathematical proof supported by exact finite construction
checks, not an exhaustive enumeration of partitions or a Lean proof. It is
not a minimum-bit, minimum-runtime or smallest possible trace-predictive model.
Strong lumpability may be stricter than output-trace equivalence.

The reference uses an independent worklist of splitter blocks on the exact
16-node grid {0,1/3,2/3,1}^2. Freeze a splitter's member set while using it;
split every live block by its exact vector of probabilities to that set;
enqueue all newly created subblocks and skip obsolete queue entries.
After termination canonicalize by first state occurrence. Every final block
must have been tested as a live splitter. Polynomial uniqueness under the
(3,3) bound upgrades equality at these nodes to coefficient equality.
The [NIST interpolation identity](https://dlmf.nist.gov/3.3.i) supplies the
standard uniqueness background. The same induction proves worklist coarseness.
The reference also independently emits the canonical round certificate using
grid row signatures, and requires its final partition to equal the worklist
result. It never reads the primary's certificate.

## Executable interface and exact output

analyze(problem) accepts only the exact native dict
{"schema_version":"det8-qr05l-problem-v1","family":"qr05l_adversarial_iid"}.
Reject wrong keys, values, native types and subclasses normally and under -O.
Use standard library only, no I/O, prior artifacts/executor imports or other-route
imports. Separate utility code may be carried forward from each route's own K
source, with its lineage stated; runtime execution remains isolated.

Primary refinement.py uses observed chains/pairs and binomial kernel expansion,
then synchronous coefficient-row refinement. Reference reference_qr05l.py
uses source-chain full-count-law moments and exact tensor interpolation, then
the grid splitter worklist and its independent canonical certificate.

The base output retains K's exact field schemas, but on the expanded domain:

```text
{
 frames:[{frame_id,density,fixed,eligible}],
 profiles:[{profile_index,name,frame_id,past,state_ids}],
 states:[{
   state_id,frame_id,mask,kept,past,aliases:[{profile_index,mask}],
   color_sizes:[O,E],chain_counts:[N0,N1,N2,N3],
   mean_graded:D[4][4][4],pair_graded:B[4][4][4][4],color_order:[n,relation,color],
   classes:{basic_Q:id},
   transitions:[{target_state,coefficients:4x4}],
   summary_laws:{basic_Q:[{target_class,coefficients:4x4}]}
 }],
 partitions:{basic_Q:[{class_id,key,members}]},
 partition_refinement:4x4 booleans,
 closure:{basic_Q:{
   closed:boolean,
   first_collision:null|{
     class_id,left_state,right_state,target_class,left_coefficients:4x4,right_coefficients:4x4
   },
   quotient_rows:null|[{class_id,representative_state,transitions:[{target_class,coefficients:4x4}]}],
   semigroup:null|SEMIGROUP
 }},
 expected_updates:{
   verified:true,
   rows:[{state_id,mean_features:64,pair_features:256,coefficient_cells:5120,max_abs_residual:0}],
   coefficient_cells:5120*N
 },
 counts:{
   frames,profiles,aliases,states,partitions,
   fine_transition_atoms,summary_transition_atoms,transition_coefficient_cells,
   mean_feature_cells,pair_feature_cells,expected_update_coefficient_cells,
   closed_partitions,quotient_transition_atoms,
   semigroup_intermediate_paths,semigroup_coefficient_cells
 },
 stabilization:{
   initial_partition:"pair_graded",
   rounds:[{
     round_index,
     state_classes:[N class IDs],
     classes:[{class_id,members}],
     pushforward_rows:[{state_id,transitions:[{target_class,coefficients:4x4}]}],
     stable:boolean,
     separations:[{
       parent_class_id,child_class_id,left_state,right_state,target_class,
       left_coefficients:4x4,right_coefficients:4x4
     }]
   }],
   strict_rounds,final_round,
   state_classes:[N final class IDs],
   classes:[{class_id,members}],
   quotient_rows:[{class_id,representative_state,transitions:[{target_class,coefficients:4x4}]}],
   semigroup:SEMIGROUP,
   comparison:{
     names:["mean_graded","pair_graded","stable_pair","color_order","full_record"],
     refinement:5x5 booleans
   },
   counts:{
     rounds,strict_rounds,classes,round_transition_atoms,round_coefficient_cells,
     separation_witnesses,quotient_transition_atoms,
     semigroup_intermediate_paths,semigroup_coefficient_cells
   }
 }
}
SEMIGROUP = {
 verified:true,
 rows:[{class_id,transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual:0}],
 totals:{transition_pairs,intermediate_paths,coefficient_cells,max_abs_residual:0}
}
```

basic_Q is exactly the four basic names, in the declared order. Stabilized
class IDs do NOT overwrite the basic B class IDs or enter basic state keys.
Round classes omit redundant recursive keys; state_classes and pushed rows
retain the exact construction. All atoms are sorted by numeric target ID.
Class IDs, members, state order and first-occurrence registration are exact.

Base counts remain K's 15 fields: partitions and closed_partitions are integer
counts. Base coefficient cells equal 16*(fine atoms+all state/basic-Q atoms).
Base quotient counts include only closed BASIC partitions; stabilized counts
are separate. Feature counts are N*64, N*256 and N*5120. Stabilization
round_transition_atoms counts all state pushed atoms across all retained
rounds; round_coefficient_cells is 16 times that total. Each semigroup has
256 cells per structurally reachable source/target pair.

Only native dict/list with native string keys; native ints for IDs, counts,
coefficients/codes, native bool flags, null, and reduced rational strings.
No mathematical floats, tuples, Fraction objects, or bool/int substitutions.
Cap exact components at 4096 bits. Runtime floats belong only to outer metadata.

## Runner bridge, counterexamples and two-step traces

Pin all 16 earlier artifacts. Read captured JSON only; do not import earlier
executors. Match the entire K state prefix, original profile maps, frames,
features, fine rows, basic class assignments/pushed rows, pulled-back basic
partitions and expected-update rows. Filter aliases to profile_index<4 before
comparing old states. Additional aliases remain visible separately.

For Q* restricted to K, compare actual class memberships to old B, construct
the class-ID correspondence and verify the old B quotient coefficientwise.
Check that old fine rows do not leave old states and that quotient rows in the
old class image do not leave that image. Do not substitute equal class counts
for this restriction. Preserve the prior J/earlier bridge as retained evidence.

The runner independently audits fine/state/schema identities, all basic
partitions/closures, expected-feature updates, every refinement step and split,
terminal fixed-point closure, comparison matrix and full semigroup coefficients.
Also evaluate basic and stabilized rows at the same 22 distinct K rates:
the 16 grid points plus (1/2,1/2), (2/5,3/7), (1/5,4/5), (1/2,1/3),
(0,2/5) and (3/7,1).

Retain these controls:

- Full path6 and cycle4_edge at mask63 have identical complete D/B tensors
  and counts [1,6,5,0]. Both R22 polynomials are
  5xy + 4x^2 y + 4xy^2 + 12x^2 y^2.
- The B class of cycle4_edge mask45 (kept interiors {1,3,4,6}) has count vector
  [1,4,4,0]. Its next-B probability is 0 from path6 and
  x^2(1-x)y^2(1-y) from cycle4_edge. The full count-law atom [1,4,4,0] has the
  same respective probabilities. Verify all coefficients, 0 versus1/64 at half
  rates and 0 versus8/729 at (1/3,2/3). Retain the automatically first failure
  separately, even if its positive/negative orientation is reversed.
- Basic B fails on the expanded domain, so it has no quotient. Its refined
  class must distinguish the two sources. The source label is not a key.
- Mean D also fails. Retain K's selected star/path mean-law witness.
- Color order, full record and Q* pass closure. Retain a first pair in one
  Q* class with different color-order codes if one exists; otherwise null.
  This reports actual remaining compression without prescribing it.
- Each frame has its fixed-only absorbing state; all corners and degree bounds
  remain valid. The fresh-versus-reused coin diagnostic remains separate.

Additionally compare complete two-step ORIGINAL-B trace laws from fine paths
with those obtained by projecting the Q* quotient at four ordered stage pairs:

```text
((1/2,1/2),(1/2,1/2))
((1/3,2/3),(2/5,3/7))
((0,1/2),(2/3,1))
((1,1),(1/3,2/3)).
```

A trace records B(U),B(V) at both stages. Do not replace it with a terminal
product-rate marginal. Retain all structurally attainable trace atoms, including
selected-rate zeros. Verify complete equality, normalization and structural
target sets at every state/rate pair. This is an additional finite evaluation
audit; all-rate trace preservation follows from verified strong quotient
closure by inserting the B-class selectors between successive kernels.
No earliest distinguishing horizon, trace-minimal representation or deeper
delayed witness is claimed from a refinement-round number.

Runner trace schema:

```text
trace_audit:{
 stage_rate_pairs:[[[x,y],[a,b]],...],
 rows:[{
   state_id,rate_pair_index,
   atoms:[{first_pair_class,last_pair_class,probability:"reduced rational"}],
   probability_sum:"1",max_abs_residual:"0"
 }],
 checked_rows:4*N,
 structural_trace_atoms:sum row atom counts,
 verified:true
}
```

Atoms sort lexicographically by (first_pair_class,last_pair_class).
The protocol does not add a new covariance-tower experiment: K's tower and
the general moment identities remain intact. This gate focuses on adversarial
full-law failure and recursively sufficient refinement.

## Acceptance, lifecycle and claim boundary

Both complete native executor outputs must agree. Tests independently
reconstruct the new family, adversary, round rule, fixed point, coarseness
premises, K restriction and trace audit. Include early-stop, improper-merge,
fabricated quotient, split-witness, class-ID/type and source-identity mutations.
Run normally and under -O, including assertion-free optimized input guards.

Freeze README, refinement.py, reference_qr05l.py, study.py, test_qr05l.py and
test_capture.py after review, tests and formatting. Capture canonical
results.json once using exclusive creation/readback with fresh external
bytecode cache and isolated Python. Exact replay is read-only; check sources,
priors and artifact before/after. Mutation lifecycle tests use temporary stub
evidence only. RESULTS.md and the roadmap are outside the frozen source ledger.

No captured K claim is revoked: B closure was explicitly bounded there.
L tests a larger supplied family and a finite coarsest closed B-refinement.
No minimum bit cost, measured speedup, empirical noise calibration, RET
integration, quantum channel, metric, spacetime, continuum or gravity result
follows. Physical laws and ontology are not premises of this construction.

