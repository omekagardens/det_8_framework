# QR-05M protocol: constructive observable realization

6 September 2026. Prospective bounded investigative gate.
Research base: pushed QR-05L checkpoint
`156a644350d7649c69aaf2316e78446d3fcdbed0`.

## Question and decision rule

Can a feature computed from the supplied observed order itself realize the
stable recursive distinction found in QR-05L, without consulting a source
name, state ID, class ID or transition table?

The candidate is the count M of eligible color-layered induced K2,2 orders.
Construct C(S) = (frame, B(S), M(S)) independently, then compare its actual
partition memberships with L's stable B-refinement Q*. A class-count match
alone is not a success criterion. Record a mismatch or closure failure if
one occurs; do not alter the feature after looking at that outcome.

This gate retains exactly L's six-source, 257-observation domain and fresh
independent two-color thinning law. It does not broaden the source family,
change a physical law, integrate RET, install Lean, or alter prior evidence.
Synthetic recognizer tests below are unit controls, not additional states
in the certified sampling domain.

## Supplied observations and sampling

Vertices are original IDs 0 through 7. Fixed bottom 0 and top 7 bound all
six interior vertices. Six source orders are enumerated in this order:

1. ferrers6: i+1 < j+4 iff i <= j, i,j in {0,1,2}.
2. standard_example3: i+1 < j+4 iff i != j.
3. chain6: the total order.
4. ferrers6_fixed: the first order, but vertex 3 is also fixed.
5. path6: interior comparisons 1<2, 1<4, 3<4, 3<6, 5<6.
6. cycle4_edge: 1<4, 1<6, 3<4, 3<6, 2<5.

Except in source 4, eligible vertices are 1 through 6. Source 4 excludes
fixed vertex 3 from eligibility. Public frames are [density, fixed IDs,
eligible IDs], with density the exact string "12". Frames are numbered by
first occurrence. Eligible color is the explicitly supplied mark encoded
here by original-ID parity: odd and even are named colors. Relabeling
controls preserve those marks; parity is not inferred from local positions.

Enumerate every eligible subset in ascending mask order for each source.
Keep fixed vertices, sort surviving original IDs, and restrict the supplied
transitively closed strict order to them. Past arrays use local positions.
Deduplicate by [frame, kept original IDs, past arrays], with first-occurrence
state IDs. Source/mask aliases remain provenance, never weights or features.

Expected inventory inherited from L: 352 aliases, 257 unique observations,
two frames. Reconstruct this inventory, do not import it into the executors.
The runner subsequently compares the whole L-shaped analysis projection to
the pinned L artifact using type-exact canonical equality. L in turn pins
K's original 188-state subset and quotient restriction.

Given observed S, retain each currently eligible odd vertex with probability
x and each eligible even vertex with probability y, independently of all
others. Fixed vertices always survive. For U induced from S, with O,E
currently eligible and o,e retained:

    P_(x,y)(S,U) = x^o (1-x)^(O-o) y^e (1-y)^(E-e).

The parameter domain is [0,1]^2. Every structurally attainable atom remains
represented, including zero-probability atoms at selected boundary rates.
Coefficient tables use exact signed native integers, padded 4 by 4,
x-power outermost and y-power innermost. No floats enter mathematical data.

Fresh independent stages obey P_(x,y) P_(a,b) = P_(xa,yb).
The composition certificate checks all 256 cells of the four independent
variables for every structural start/end pair, not just a same-rate grid.
Reuse of random coins, adaptive rates and physical time are outside this law.

## Existing statistics retained unchanged

N_q counts chains from 0 to 7 having q internal vertices, q=0,1,2,3;
N_0=1. Chains are counted once per vertex set. D_qoe counts individual
chains having o odd and e even eligible support vertices. B_qroe counts
ordered pairs of such chains by the odd/even sizes of their eligible union.
Self-pairs, both orders of distinct pairs and repeated equal supports count.
Fixed internal vertices can occur in chains but not eligible supports.

D has shape 4x4x4 and B has shape 4x4x4x4. B_0roe = D_roe.
These tensors give the exact two-color first and second count moments,
not the entire future law. L demonstrated two observations with equal B
and different next-B laws; that failure must remain in this evidence.

The four old partitions (frame,D), (frame,B), fixed-anchored color-marked
order, and complete labeled record remain unchanged. The stable partition
starts with B and iterates the exact key [previous class, full polynomial
row pushed to previous classes], stopping on vector stability. The initial
class is retained in the key, so no required B distinctions can merge.

The carried primary route reconstructs chains/pairs and binomial kernels,
then synchronous coefficient refinement. The carried reference reconstructs
source count moments and exact interpolated kernels, then a live-block
splitter worklist and an independent synchronous grid certificate.
Each route carries local utilities from its own L lineage; neither imports
the other route, any previous executor, or captured evidence at runtime.

## Candidate motif, defined before its outcome

For an observed finite strict order S with eligible marks, let A be a
four-element subset of observed eligible vertices. A contributes exactly
one to M(S) precisely when:

- A contains two vertices of each named color;
- within each color pair there is no comparison in either direction;
- either every odd member is below every even member, or every even
  member is below every odd member.

Thus the induced order on A has exactly four strict comparisons. All
comparisons are evaluated in the supplied transitive relation, not merely
a cover graph. Outside vertices/relations do not disqualify a motif.
There is no requirement that the four vertices be a connected component
of S. Fixed vertices, including fixed interior 3, never participate.
A support counts once, not once per ordering, orientation or automorphism.

The public implementation interface is:

    motif_supports(kept, past, eligible) -> sorted list of sorted 4-ID lists

It reads only those three supplied observation/mark arguments. The exact
integer count is the length of this support list. Source/profile identity,
mask, history mass, state ID, B value and transition/class tables are not
inputs to the recognizer. Synthetic unit inputs are well-formed finite
strict orders; malformed-problem rejection remains the exact top-level
two-field schema contract, not a new general-purpose public order parser.

Primary recognition enumerates four-vertex subsets and checks their full
induced relation. Reference recognition enumerates incomparable same-color
pairs and incomparable pairs of common opposite-color successors or
predecessors. It canonicalizes supports, checking no duplicate counting.
The two implementations must not call each other.

Candidate classes are numbered by first state occurrence of
[frame, B, len(motif_supports)]. Feature values are computed before any
comparison with Q*. Both exact fibers and both directions of refinement
must be checked. Agreement of normalized class vectors then certifies the
membership match; matching cardinalities alone does not.

## Universal expectation versus finite recursive closure

For any finite supplied marked order under this same independent vertex
thinning, induced restriction cannot create or destroy the motif property
on a surviving fixed support. Each contributing four-set has exactly two
eligible vertices of each color, so survives with probability x²y².
Writing M as a sum of support indicators and using linearity:

    E[M(U) | S] = x² y² M(S).

Overlapping supports need not survive independently. No such independence
is used in the expectation proof. This proof applies beyond the small
certified domain whenever the stated order/marks/law assumptions hold;
the finite checks do not establish an unrestricted full-law theorem.

Independently check the expectation coefficientwise in all 257 states:
sum_U P(S,U) M(U) equals the 4x4 table with M(S) only at [2][2].
Retain both actual and expected tables, every residual and all 16 cells
per state. Boundary-rate zeros are retained.

For recursive prediction, push each state's complete fine row to candidate
classes. Strong closure requires equality of all such polynomial rows for
every pair of members of each candidate class. Report the first failure
if any, in ascending class/member/target order. A quotient is emitted only
when closure succeeds. Check normalization, boundary behavior and fresh-stage
composition independently of the expectation identity.

If C and Q* match, compare the actual class vectors, class members, full
state-pushed rows, representative quotient rows and all composition
coefficients/certificates. Then C inherits the already established coarsest
closed B-refinement property on this domain. This does not make M uniquely
necessary as an encoding, prove minimum storage, or imply closure on
unseen orders. The original B failure remains an explicit counterexample
to confusing equal moment updates with equality of full next-state laws.

## Exact new analysis schema

The executors accept exactly
{"schema_version":"det8-qr05m-problem-v1","family":"qr05m_observable_iid"}
and emit the complete L-shaped analysis, unchanged, plus the key
"observable". Native dictionaries have native string keys; lists, booleans,
integers, strings and null are the only mathematical wire types.

The new object has exactly these keys:

- definition: "eligible_color_layered_induced_k22"
- states: [{state_id, motif_supports, motif_count}], in state-ID order
- state_classes: the first-occurrence candidate class vector
- classes: [{class_id, members}], in class-ID order
- pushforward_rows: [{state_id, transitions}], one per state; transitions
  are sorted {target_class, coefficients} records, 4x4 integer tables
- closed: boolean
- first_failure: null if closed, otherwise {class_id, left_state,
  right_state, target_class, left_coefficients, right_coefficients};
  absent target atoms in the witness are represented by zero tables
- quotient_rows: empty if not closed, otherwise [{class_id,
  representative_state, transitions}], same schema/order as L's Q* quotient
- semigroup: null if not closed, otherwise the existing L certificate schema
  {verified, rows, totals}, with rows {class_id, transition_pairs,
  intermediate_paths, coefficient_cells, max_abs_residual} and totals
  {transition_pairs, intermediate_paths, coefficient_cells, max_abs_residual}
- comparison: {same_memberships_as_stable_pair, candidate_refines_stable,
  stable_refines_candidate}; all booleans computed, not presumed
- expected_update: {verified, coefficient_cells, rows}; rows are
  {state_id, coefficients, expected_coefficients, max_abs_residual}
- counts: {states, motif_positive_states, motif_support_occurrences,
  max_motif_count, classes, state_transition_atoms, state_coefficient_cells,
  expected_update_coefficient_cells, quotient_transition_atoms,
  semigroup_intermediate_paths, semigroup_coefficient_cells}.

Counts are recalculated from retained records. Full base analysis remains
byte/type-exact equal to the decoded L analysis after removing "observable";
M's input/schema and suite-level new controls are not part of that comparison.

## Prespecified controls

Retain the L controls, including the full path/cycle B collision, selected
next-B event, old D collision, fixed-only observations, and a stable class
merging distinct named-color marked orders. Inspect M for the full
path6/cycle4_edge and the cycle support {1,3,4,6} without using these IDs
inside the feature. Candidate values in each old B fiber remain inspectable.

Independent unit controls cover:

- one valid layered K2,2 in either orientation, counted once;
- incomplete cross relation, a same-color comparison, wrong two/two coloring
  and nonuniform cross orientation: not motifs;
- a total order and a same-color-layer violation: not motifs;
- fixed-vertex exclusion and use of eligible original IDs rather than local
  position parity, including a fixed interior vertex;
- arbitrary changes of local vertex ordering and parity-preserving original
  label permutations preserve the count and mapped supports;
- a K2,3 layered order has three overlapping supports, not one and not
  an automorphism multiple; its motif mean identity holds despite overlap;
- additional outside vertices do not erase a valid induced four-set.

A runner control inventory will retain deterministic synthetic observation
inputs, expected supports and outputs from both recognizers, including
the overlapping-motif expectation check under exact subset enumeration.
These controls do not change the six source profiles or the closure claim.

Mutation tests must reject corrupted motif values/supports, missing supports,
wrong candidate classes, equally sized but different fibers, false closure,
incorrect expected tables, quotient coefficients and fabricated comparison
flags. A candidate mismatch must be reported honestly, not overwritten with
the stable partition. Preserve existing source/schema/native-type guards.

## Runner, evidence and verification lifecycle

Files are isolated in this gate directory. Frozen sources are README.md,
observable.py, reference_qr05m.py, study.py, test_qr05m.py and test_capture.py.
RESULTS.md and the roadmap are human reports outside the source ledger.
The runner reads pinned prior JSON only; all 17 prior artifacts, including
L and its 16 priors, must retain their published hashes.

The runner independently audits the carried L analysis/refinement/trace and
K restriction, checks all new motif supports from observed relations,
reconstructs candidate classes and pushed rows, validates the expectation
and full quotient, and compares the L projection to its pinned JSON.
It retains a new observable audit and synthetic controls alongside the old
suite evidence. Output records distinguish a candidate success from the
premise-only general motif expectation.

Use isolated Python 3.11 with an external task-specific bytecode cache and
no pytest repository cache. Perform normal and optimized tests and lint/
format checks; check new-file whitespace before capture. Resolve review
findings before freezing. Capture uses exclusive creation, canonical JSON
and readback; it must not overwrite existing evidence.

Replay is read-only and reruns the exact suite against the frozen source/
prior ledger, comparing native mathematical data exactly. Perform normal
and optimized replays plus independent JSON-only postflight that imports
no executor, runner or test. Source changes after capture require separately
versioned evidence, not silently regenerated results. Lifecycle negative
tests use temporary stub evidence, never the real capture.

Keep all unrelated checkout changes and previous artifacts untouched.
Publish only this gate and its roadmap update in a scoped commit, then
verify remote head and unchanged evidence identity.

## Claim boundary and next decision

A successful result means one explicit observable realizes the finite
recursive repair, separating an interpretable statistic from a lookup
partition. It supplies a model-checking tool for relational coarse
descriptions under a declared observation law.

It does not derive quantum theory or gravity, identify a metric or field
equation, change known observables, identify thinning with time or causal
growth, prove ontology, validate empirical noise/calibration, or certify a
RET integration. No empirical data are used.

If this gate passes, the next proposed gate is prespecified domain-portability
testing of (B,M) on a broader finite family, preserving this result as a
restriction and retaining new counterexamples instead of redefining M.
If it fails, record the actual missed distinctions and decide a replacement
feature in a separately scoped protocol. Neither branch is executed here.
