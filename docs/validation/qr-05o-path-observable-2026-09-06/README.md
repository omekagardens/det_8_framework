# QR-05O protocol: obstruction-targeted path observable

6 September 2026. Prospective bounded investigative gate.
Research base: pushed QR-05N commit
`0be2929dc9b6fc0ebba68f17ed2980e52ed31104`.

## Question and scope fixed before the outcome

QR-05N found equal (frame,B,M) summaries with unequal next-summary laws.
Add only the proposed T observable below. Does
H(S)=(frame,B(S),M(S),T(S)) have a complete closed next-H law on exactly
the same 2,470-state domain?

The T definition, domain and decision rules are fixed here before the new
candidate closure search. It is not permissible to modify T after seeing
the result, substitute a stable lookup partition, silently broaden the
sources, or omit a remaining failure. A failure is a valid research outcome.

N's complete analysis is reproduced independently and retained unchanged.
Adding T is guaranteed to refine the existing summary; it is not assumed
to preserve every old fiber. Even a closed H would not automatically be
the coarsest closed refinement, uniquely necessary feature, or minimum
memory representation. No stable-refinement search is included in O.

No new physical law, RET integration, dependency/Lean installation, empirical
noise/calibration claim or prior source/artifact edit is part of this gate.

## Fixed domain, marks and sampling calculus

Original vertex IDs are 0..7. Fixed bottom0 and top7 bound every interior
vertex. Source profiles0..5 are exactly the earlier six:

0. ferrers6: i+1<j+4 iff i<=j, i,j in {0,1,2}.
1. standard_example3: i+1<j+4 iff i!=j.
2. chain6: the total order.
3. ferrers6_fixed: profile0 with vertex3 also fixed.
4. path6: 1<2,1<4,3<4,3<6,5<6.
5. cycle4_edge: 1<4,1<6,3<4,3<6,2<5.

Profiles6+h, h=0..511, are layered_oe_h with three-digit mask names;
profiles518+h are layered_eo_h. Bit3*i+j of h pairs odd2*i+1 with
even2*j+2. A set bit means odd<even in oe and even<odd in eo.
Reversal keeps the incidence bit convention; it does not transpose it.
There are no other interior comparisons.

The public frames are [density,fixed IDs,eligible IDs], with density the
exact string "12", first-occurrence frame IDs. Frame0 has fixed[0,7],
eligible[1,2,3,4,5,6]. Frame1, used only by profile3, has fixed[0,3,7],
eligible[1,2,4,5,6]. Eligible original-ID parity supplies the named colors.
Original IDs and local array positions are not topological labels:
a comparison such as3<2 is valid.

Enumerate source profiles in that order and eligible masks ascending.
Keep fixed vertices, sort surviving original IDs, and restrict the supplied
transitively closed strict relation. Past arrays contain sorted local
predecessor indices, which may exceed the target index. Deduplicate by
[frame,kept,past], numbering states by first occurrence. All aliases remain
visible provenance and never become weights or summary inputs.

N's exact inventory remains1,030 profiles,65,888 aliases,2,470 states,
99,180 fine atoms. Its first257 states remain the M prefix. These inventories
are not recomputed by reading prior artifacts inside the executors.

Given current S, independently retain each eligible odd vertex at rate x,
each eligible even vertex at y, and every fixed vertex with certainty.
For induced U with retained counts o,e from current O,E:

    P_(x,y)(S,U)=x^o(1-x)^(O-o)y^e(1-y)^(E-e).

Rates range over[0,1]^2. Keep every structurally attainable atom, including
selected-rate zeros. Exact signed native integer coefficient tables are
4x4, x-power outermost; the bidegree is at most(3,3).

Rows normalize coefficientwise. All four rate corners are deterministic;
(1,1) is identity and (0,0) the frame's fixed-only observation. Fresh
independent stages compose:

    P_(x,y)P_(a,b)=P_(xa,yb).

Any closed candidate quotient must additionally pass the full four-variable
coefficient check,256 cells per structural start/end pair. A same-rate
two-variable grid cannot substitute for that certificate. Reused coins,
correlated/adaptive rates, physical time and event growth are not premises.

Hard bounds retained from N: at most2,579 states,100,393 fine atoms, six
eligible vertices and three per color, chain order q<=3, exact components
<=4,096bits, canonical capture<=64MiB. The added path partition has at most
99,180 state-pushed atoms; a maximally fine quotient would require at most
25,390,080 conceptual four-variable cells, not stored dense tensors.

## Existing observables, unchanged

N_q counts chains from0 to7 having q internal vertices, q=0,1,2,3, N_0=1.
Count each chain vertex set once: all its unordered pairs are comparable
in the supplied relation and the endpoint relations hold. Equivalent directed
traversal is allowed; ascending numeric IDs do not define a chain.

D_qoe counts individual chains by eligible odd/even support.
B_qroe counts ordered pairs of chains by their eligible union sizes.
Self-pairs, both orders of distinct pairs and repeated equal supports count.
Fixed internal vertex3 can occur in chains but not eligible support.
D has shape4x4x4, B shape4x4x4x4, and B_0r=D_r. These give exact first and
second count moments, not a full law.

M is the unchanged count of eligible color-layered induced K2,2 supports:
two eligible vertices per named color, no within-color comparisons, all
four cross comparisons uniformly oriented in either direction. Each
four-set counts once; outside vertices/relations do not invalidate it.

The two original N partitions, their failures and their full pushed rows
remain intact in the base analysis. Do not relabel them as successful just
because the new candidate may close.

## New observed T, defined independently of the repaired law

A four-element subset A of observed eligible vertices contributes once
to T(S) iff:

- It contains exactly two odd and two even eligible vertices.
- Each same-color pair is incomparable in both directions.
- Exactly three of the four possible cross-color pairs are comparable.
- Those three comparisons are all odd<even, or all even<odd.
  The remaining cross pair is incomparable in both directions.

This is a color-layered induced P4: its undirected comparability graph is a
four-vertex path. It is NOT a directed path of length three, a chain of four
vertices, an embedding count, a cover-graph count, or a Feynman trajectory.
A full K2,2 has T=0, not four paths obtained by deleting one edge.

Use the entire supplied strict transitive relation. If an outside
intermediary made the missing comparison true, the four-set is K2,2 and
T=0; removing the intermediary preserves that induced comparison and cannot
create a T support. Outside vertices that leave the induced relation intact
do not disqualify the support.

Fixed vertices, including fixed interior3, do not participate.
The public helper is:

    path_supports(kept,past,eligible) -> sorted list of sorted four-ID lists

Only these observation/mark inputs may enter recognition. It may not read
profile names, source IDs, mask histories, B/M values, state/class IDs or
transition tables. The integer T is the support-list length. Under these
marks M and T are disjoint on each four-set, so M+T<=binom(o,2)binom(e,2)<=9.

Primary recognition enumerates eligible four-sets and tests their complete
induced relation. Reference recognition uses a P4's unique central edge:
choose the opposite-color edge between its two degree-two vertices, one
opposite-color leaf on each end, incomparable same-color pairs and the
unique incomparable cross leaf pair. Repeat in the reversed orientation.
Check no support is counted twice; do not call the other implementation.

Recognizer inputs in unit tests are well-formed finite strict orders.
This is not a new general-purpose public poset parser; malformed top-level
problem/native-wire contracts remain strict.

## Expectation is separate from recursive prediction

Let A range over T supports of S. Induced restriction gives

    T(U)=sum_A 1[A is retained],
    E[T(U)|S]=x²y²T(S).

Linearity uses no independence between overlapping supports. Independence
of eligible vertex retention supplies the support-inclusion factor.
This is a general premise-based motif expectation statement; it does not
prove a full marginal/joint law or recursive summary sufficiency.

Check this identity coefficientwise on all2,470 states and retain actual
and expected4x4 tables:39,520 cells. N's D/B and M update evidence must
also remain unchanged and be replayed, not inferred from T.

Construct H classes by first occurrence of [frame,B,M,T] before consulting
any closure outcome. Retain exact keys and actual fibers. Push each state's
complete fine polynomial row to H classes. Compare all members to the first
member of their class. The canonical first failure scans class ID, subsequent
member ID, then target ID over the union of structural supports; absent
targets are zero tables.

If H fails, retain that witness, quotient_rows=[], semigroup=null.
If H closes, retain representative quotient rows only after every member
row agrees, then check normalization, all corners and full fresh-stage
composition. Do not substitute a refinement or infer closure from the
expected T update.

Compare actual H memberships to N's B and C=(B,M) memberships.
H must refine both; record whether C refines H and whether the normalized
class vectors are equal. Count the C fibers split by T from actual members,
not by subtracting class cardinalities. No coarseness/minimality theorem
is asserted in this gate.

## Prespecified controls

The runner will retain deterministic recognizer cases and their exact
inputs/expected outputs, independently checked by both recognizers:

- All four choices of missing cross edge from K2,2 in each orientation:
  one T support per four-set, not one per traversal.
- Two cross edges: no T. Complete K2,2: T=0,M=1.
- A same-color comparison, incorrect layer coloring and wrong2+2
  cardinality: no T.
- A four-vertex total order, even though its Hasse graph is P4: no T.
- A motif corner marked fixed: no T, including original odd vertex3.
- Non-topological local order, parity-preserving relabeling and color
  exchange transport the support correctly.
- A harmless outside vertex preserves T.
- An outside intermediary creating the fourth comparison, both before
  and after induced removal of that intermediary: T remains zero.
- K2,3 minus edge3<6 on odd{1,3},even{2,4,6}: T supports
  {1,2,3,6} and {1,3,4,6}, with one separate K2,2 support.
  Retain all32 induced outcomes and verify mean2x²y²; joint support survival
  x²y³ is not the product of the two marginal survival probabilities.

These synthetic recognizer cases are outside the certified sampling-domain
inventory. They do not add sources or imply general closure.

Inside the fixed N domain, locate controls by profile/mask, not hardcoded
new IDs: complete incidence511 in both orientations has T=0,M=9; incidence510
in both orientations (one missing edge) has T=4,M=5. N's star/path obstruction,
first aliases(profile84,63)/(profile91,63), has T=0/1.
These local feature facts do not presume global closure.

A test-private empty-recognizer mutation must recover exactly N's C
partition and its retained failure, with no quotient or silent repair.
No cached successful candidate may survive that change. This diagnostic
does not alter any real source/artifact or add a certified case.

## Exact new output schema

Accept exactly
{"schema_version":"det8-qr05o-problem-v1","family":"qr05o_path_iid"}.
Reject missing/extra fields and non-native/subclass problem types.
Expose analyze(problem), unchanged motif_supports, and path_supports.

Emit the entire N-shaped analysis, unchanged, plus "path_observable".
The new object has exactly:

- definition: "eligible_color_layered_induced_p4".
- states: [{state_id,path_supports,path_count}], in state-ID order.
- state_classes: first-occurrence H class vector.
- classes: [{class_id,key,members}], with key=[frame,B,M,T].
- pushforward_rows: [{state_id,transitions}], with target-sorted
  {target_class,coefficients}4x4 integer atoms, retaining structural zeros.
- closed: boolean.
- first_failure: null or {class_id,left_state,right_state,target_class,
  left_coefficients,right_coefficients}.
- quotient_rows: [] on failure; otherwise {class_id,representative_state,
  transitions} rows in the same schema as N/M quotient certificates.
- semigroup: null on failure; otherwise {verified,rows,totals}, rows
  {class_id,transition_pairs,intermediate_paths,coefficient_cells,
  max_abs_residual} and totals {transition_pairs,intermediate_paths,
  coefficient_cells,max_abs_residual}.
- comparison: {candidate_refines_pair,candidate_refines_motif_pair,
  motif_pair_refines_candidate,same_memberships_as_motif_pair}, all computed
  booleans, not assumed class-count equivalences.
- expected_update: {verified,coefficient_cells,rows}; rows
  {state_id,coefficients,expected_coefficients,max_abs_residual:0}.
- counts: {states,path_positive_states,path_support_occurrences,
  max_path_count,classes,split_motif_pair_classes,state_transition_atoms,
  state_coefficient_cells,expected_update_coefficient_cells,
  quotient_transition_atoms,semigroup_intermediate_paths,
  semigroup_coefficient_cells}.

All mathematical data use native string-keyed dictionaries, lists, ints,
strings, booleans and null only. No floating values or implicit coercion.
Counts are recomputed from retained records.

Locally carry utilities from each route's own N lineage. Neither executor
imports previous executors, captured evidence or the other route. The base
primary retains observed chains/pairs and binomial kernels; the reference
retains source-directed chains, full count-law moments and cached exact
rational interpolation. Only the runner/tests read pinned JSON afterward.

## Prior evidence and audit boundary

After removing only "path_observable", the decoded analysis must equal
pinned N's complete analysis type-exactly. N's base audit, prior M bridge
and controls must also be equal. This includes all old observations,
aliases, features, kernels, two failed partitions, expected updates and
the old restricted M quotient.

The new candidate may refine old C fibers. Do not demand that H's quotient
equal M's or N's failed candidate; preserved evidence refers to the old
features and law, not an assumed identity of the new partition.

The runner independently reconstructs T supports, keys/fibers, pushed laws,
all expectation cells, closure decisions, any quotient/composition certificate,
and recognizer controls. Rate audit points are N's22points:
{0,1/3,2/3,1}² followed by
(1/2,1/2),(2/5,3/7),(1/5,4/5),(1/2,1/3),(0,2/5),(3/7,1).
Keep selected-rate zero atoms and verify all9,880 state/corner rows.
The 16-node grid supplements degree-bounded polynomial checks; it does
not replace four-variable composition.

Suite-level candidate_closed describes H; base_candidate_closed describes
N's unchanged C. Retain a separate path audit/control object and a prior
N bridge, so the two outcomes cannot be confused.

No expanded stable-refinement, trace or covariance-tower experiment is
added. Strong closure, if verified, is the stated stochastic recursive
contract; no separately measured trace-minimality or storage claim follows.

## Verification, frozen sources and publication

Frozen sources are README.md, path_observable.py, reference_qr05o.py,
study.py, test_qr05o.py and test_capture.py. RESULTS.md and the roadmap
are human reports outside the ledger. Pin19prior artifacts: N plus its18.

Test normal and optimized isolated Python3.11 with external task-specific
bytecode caches and no pytest repository cache. Independently reconstruct
features/classes/laws and test corrupt supports, native bool/int IDs,
equally sized wrong fibers, wrong coefficient tables, false closure,
missing failures, invalid quotients and prior-projection tampering.
Ensure optimized guards do not rely on non-test asserts.
Finish Ruff check/format and new-source whitespace checks before freeze.

Capture is canonical, <=64MiB, exclusive create-only and read back under
frozen source/prior identities. Never overwrite existing results. Replays
rerun the exact suite read-only, both normally and optimized; verify artifact
bytes and source/prior ledgers before/after. Finish with independent
JSON-only postflight importing no executor, runner or test. Lifecycle
negative tests use temporary stub evidence, never the real capture.

Preserve unrelated checkout and RET/core work. Publish only this gate and
its roadmap in a scoped commit/push, then verify remote HEAD and unchanged
artifact identity. Source changes after capture require separately versioned
evidence, not silent regeneration.

## Interpretation and next decision

T tests whether a specific observed structure repairs the obstruction,
not whether ontology, quantum theory or gravity is derived.
The model uses supplied finite orders and an observation law; it does not
identify thinning with physical time, event growth or a Feynman trajectory.
No metric, field equation, continuum limit, empirical apparatus/noise
calibration, RET adapter or Lean proof is established here.

If H closes, a subsequent gate may compare it with the coarsest closed
C-refinement and state an application contract; neither is presumed here.
If it fails, retain the obstruction and decide a separately scoped
next feature or richer record contract. Do not interpret either result
as permission to dismiss conflicts with known observables as noise.
