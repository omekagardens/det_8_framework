# RI-17 — one finite probability and type composition contract

14 September 2026 UTC. **DESIGN_ONLY; CONDITIONAL_FINITE_PROTOCOL_CONTRACT;
IMPLEMENTATION_NOT_ASSIGNED.** Independently reviewed and accepted by the
coordinator as a bounded design on 14 September 2026 UTC.

This plan follows the accepted, published RI-16 checkpoint
22eca4e7eb1b73b84db6fe3b6ff613df932b15c1. It specifies one finite route,
not a general process SDK, another cone refinement or physical reconstruction.
The existing [premise ledger](OPERATIONAL_PREMISE_LEDGER.md) and
[finite observability synthesis](../research/FINITE_RECORD_OBSERVABILITY.md)
remain unchanged. RI-16 proves a countable-word limit under its premises;
it does not implement the finite representation/probability adapters below.

## 1. Existing interfaces and the missing arrow

The aliases in this document distinguish actual, different Python classes:

| Alias | Accepted source to inspect/use without editing | Relevant existing interface |
|---|---|---|
| `c` | [RI-08c model](../validation/t8-q-repeatable-record-instrument-2026-09-13/model.py) | Full local `State`; `branch`, `commit_pauli`, `run_control`; reusable Pauli outputs versus separate literal-cut terminals. |
| `d` | [RI-08d model](../validation/t8-q-joint-recordability-2026-09-13/model.py) | `LocalState`, `ReferenceState`, `Independence`, prospective/validated joint sources and separate terminals. |
| `bridge` | [RI-15 adapter](../validation/t8-q-local-joint-adapter-2026-09-13/adapter.py) | `prepare`, `promote`, `couple`; full original local context retained in wrappers. Its `commit` ends in a terminal. |
| `i` | [RI-08i model](../validation/t8-q-terminal-read-observability-2026-09-13/model.py) | Fixed t=3/5 `LocalInput`, `ReferenceInput`, `Context`, `State`; known commands, reusable literal cuts and scalar-only terminal reads. |

The [RI-15 contract](../validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md)
already implements exact local-to-joint representation conversion. The
[RI-08g theorem](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md)
proves K_t inclusion in the explicitly enlarged return cone L_t. The i
executor already contains the latter cone's cut/command/read operations.
There is **no accepted RI-15-to-i wrapper or full path-weight orchestrator**.
Loading similar matrices into unrelated constructors does not close that gap.

The new conversion point is exactly

    bridge.prepare -> promote -> couple -> promote
    -> coupled bridge.JointSource -> [missing preterminal adapter] -> i.State.

It is before `bridge.commit`, not after `bridge.JointTerminal`,
`d.TerminalState`, `c.TerminalState` or `i.TerminalResult`. None of those
terminal objects may be retagged as a reusable source.

## 2. One fully specified finite policy

### Starting boundary and supplied premises

Supply one normalized exact local snapshot, with empty initial record/pending
prefixes for the primary fixture:
\[
\rho_0=(I+3Y/5)/2,\qquad
D_0=D(\rho_0^T/2,1/20),\qquad m(D_0)=1.
\]
Here \(D(A,c)=\left(\begin{smallmatrix}A&cZ\\\bar cZ&ZAZ\end{smallmatrix}\right)\).
The eigenvalues of A are 2/5 and 1/10, so A≥|c|I: this is a legitimate
nonzero-c input in the full local C, not an assumed C0 preparation.
It has genuinely complex native entries. Do not replace it by J2Phi(D_0).

The law is conditional on this expressly supplied starting snapshot, with
root weight **1 supplied as the boundary convention**, not inferred from
provenance. An earlier experimentally selected source would need its own
numerical selection weight and complement/replay contract; this plan does
not reconstruct pre-boundary probabilities or invent a preparation event.

Supply the reusable local Y instrument and local Z control, the independent
reference-selection/preparation law below, the fixed shared coupler and
native index convention, the adopted fixed-interior L_t return contract,
its literal cuts and known A command, and the calibrated available tilted
terminal read. Each availability statement is an additional operational
premise. Neither constructor validity nor this composition design proves it.

### Complete branches, including reference unavailability

Use origins `signal`, `reference`, `joint` and a distinct `protocol-stop`.
Perform the local and reference processes independently; enumerating the
local branch first in the probability tree imposes no causal edge between
their input origins.

1. On the signal, execute the fixed-frame Y instrument with both outcomes
   r=0,1. Use `c.branch` for the unnormalized maps and `c.commit_pauli` only
   for positive selected outputs. Their weights at D_0 are p_0=4/5 and
   p_1=1/5. Each positive output is J2(Q_Y,r), with c=0 as a **consequence
   of this actual supplied branch**, not a repair or earlier-input ban.
2. Apply `c.run_control(state,"Z")` once to each selected local output.
   Its current quotient is \(\rho_r=(I-(-1)^rY)/2\). Its Y record remains;
   its local pending word is now `("Z",)`. The control has weight one and
   is not replayed during conversion or readout.
3. Independently perform a declared classical reference selector/preparer:
   `ready` has weight beta=2/3 and supplies normalized R_(3/5) in the fixed
   Z orientation; `unavailable` has weight 1/3 and supplies no reference
   state. Both outcomes produce an actual reference-origin selection record.
   This complete two-outcome law, conditional preparation and independence
   are supplied premises, not facts inferred from `ReferenceState`, a label,
   a matrix factorization or a provenance string.
4. On `unavailable`, stop with the full local prefix, local pending word and
   reference-unavailability record, plus a distinct scalar stop report.
   The two stop probabilities are p_r/3. No failed-reference kernel,
   normalized output state or later read is invented.
5. On `ready`, retain weight p_r beta and the complete ready reference
   record, then execute the existing RI-15 preterminal sequence above.
   Its local input is now C0, so the polarized coupled source is lawful.
   Preserve every entry of the resulting normalized sixteen-label K_t
   kernel, its input origins, fixed frame, coupler and permutation.
6. Convert this validated preterminal source losslessly into i's expressly
   adopted L_t source interface as specified in §3. No new coupling,
   preparation, projection, event or probability factor occurs here.
7. Execute exactly one reusable literal cut in L_t, retaining all four
   actual outcomes alpha=(a,b). Each conditional weight at this fixture is
   q_alpha=1/4. Select only positive weights; record both a and b. The
   unnormalized branch is P_alpha N P_alpha, not a scalar replacement.
8. Project the verified committed cut record to its outcome-only tuple (a,b).
   Choose new joint word empty when a=0,
   and `("A",)` when a=1; execute it once. This is a complete deterministic
   record-dependent policy, stored as the fixed immutable table
   `word_by_a=((),("A",))`, indexed by validated built-in bit a; accept no
   source-dependent policy callbacks.
   Pass neither the full i.JointRecord nor its Context to this decision:
   even a read-only record exposes raw input kernels through its Context.
   The full record stays in the envelope, outside the decision view.
   The decision reads neither the residual nor a reconstructed
   state, hidden c, unobserved branch id, probability or norm diagnostic.
9. Perform one tilted terminal read with every full (a',b',sign) outcome.
   On this single-cell source only (a',b')=alpha can have positive weight.
   The output is a scalar probability and full terminal record, with a
   pre-read source for audit only. The route ends; no postread residual.

The reference law does not depend on r. Computing its product weights after
the signal branch is enumeration, not adaptive reference preparation or an
independence proof. The reference selector record has no signal predecessor;
subsequent joint/stop records can refer to both inputs. A source-validation
failure is **not** another physical selector outcome: it rejects the declared
protocol contract and must not silently remove or reweight a branch.

## 3. Exact object and metadata conversion contract

The following wrappers and names are **proposed**, not existing APIs. Every
accepted object remains intact; no field is retrofitted into an old class.

| Stage | Exact existing object and retained fields | Proposed missing accounting or binding |
|---|---|---|
| Starting/local branch | `c.State(residual,records,settings,controller,source_kind,frame)`; full 4x4 Gaussian-rational kernel. `c.Record` retains event id, Y axis, integer r, actual settings, full same-origin precursor, action/controller/type/frame. | `WeightedLocal`: supplied root snapshot/weight, actual forward calls and returned conditional weights, current exact State and cumulative p_r. No probabilities inferred from record labels. |
| Reference decision | Ready `d.ReferenceState(t,origin,records,orientation)` derives its exact residual. `d.InputRecord` has event/action/outcome/settings/payload/precursor. | `ReferenceDecision`: the complete declared two-outcome law with exact rational weights, preparation id and independence premise, plus one selected origin-tagged record and its weight. The record is id0/action `reference_select_prepare`/outcome `ready` or `unavailable`, with empty precursor. Never append both alternatives to one history. Only ready has a ReferenceState. |
| Product/coupled source | `bridge.JointSource(context,target)`; `BridgeContext` retains original c.State, exact d.LocalState conversion, reference, independence, both input origins, joint origin and reference provenance. Target is `d.CompositeState` with residual/local/reference/independence/coupler/joint_origin/permutation. | `WeightedJoint`: original weighted-local and reference-decision anchors, the exact forward-verified bridge object and total p_r beta. Bare d.LocalState is insufficient: it lacks c's pending word, frame/controller/type. |
| Adopted L_t source | `i.State(domain,context,residual,records,pending)` with domain `i.INTERIOR_DOMAIN`, t=3/5 and `i.Context` fields listed below. | `LtEnvelope`: retain WeightedJoint and the exact i.State together, validate the cross-model numerical/metadata match and explicit return/read premises. New joint records and pending start empty, while the old local pending Z remains in the retained bridge anchor. |
| Literal cut/control | Existing `i.commit -> (q,i.State)` appends full `i.JointRecord` and clears only new joint pending; `i.run_word` preserves records and appends actual new command labels. | Envelope retains the original anchor and forward trace, multiplies cumulative weight by q once, and checks exact unnormalized branch identity. No reference reset or recoupling. |
| Terminal/stop | `i.TerminalResult(source,record,effect,probability)` supplies no residual; `i.TerminalRecord` retains domain, event id, full cell/sign, tagged precursor, context, actual command word and terminal action. | `WeightedTerminal` retains the preceding Lt/cut/control envelope, exact result, prior cumulative weight and complete path label. The anchor chain keeps WeightedJoint and BridgeContext.local_source; the bare i result is insufficient. Separate `StoppedBranch` retains WeightedLocal/current exact c.State as audit data, the selected ReferenceDecision, scalar probability and its own StopReport. Neither wrapper has a continuation or output-residual interface. |

For readiness, construct `d.ReferenceState(...,records=(ready_record,))`.
For unavailability, retain its standalone selected d.InputRecord and the
complete law, without a ReferenceState, bridge or joint Context. The proposed
StopReport has origin `protocol-stop`, event_id0, action `protocol_stop`,
outcome `reference_unavailable`, the fixed policy identifier and tagged
precursor `(("signal",0),("reference",0))` for this fixture. It is neither
a same-origin d.InputRecord nor an i.TerminalRecord requiring a joint Context.
Both terminal wrappers preserve their full preceding audit anchors directly,
not by reconstructing states or missing metadata from a prefix.

### Lossless preterminal adapter: required checks, in order

1. Require the exact bound `bridge.JointSource` class, with target coupler
   `d.SHARED_COUPLER` and the bridge's verified forward construction. Reject
   product-stage sources, prospectives, terminals and foreign lookalike classes.
2. Require the ready reference decision and its independently declared
   weight/payload to match `BridgeContext.reference` and provenance. Require
   t=3/5 and Z orientation: i's typed Context does not accept arbitrary
   interior t, although some mathematical helper formulas do. Check distinct
   origin names and exact independence pair. Do not infer either weight or
   independence from string payloads.
3. Copy every exact Gaussian component directly, using i.G(real,imag) for
   both input kernels and the coupled sixteen-label kernel. Preserve native
   index order 8a+4i+2b+j, the exact native-to-grouped permutation and coupler.
   No float cast, transpose omission, partial-trace projection or J2Phi repair.
4. Convert each d.InputRecord field-for-field to i.InputRecord. This includes
   the four ordered RI-15 payload pairs carrying original local axis,
   controller, source-kind and frame. Build i.LocalInput and i.ReferenceInput
   with unchanged origin/history; compare the latter's derived residual entry
   for entry with the converted ready reference. i.LocalInput enforces C0 at
   this stage. An ineligible earlier C snapshot is still legitimate earlier;
   it is not an eligible input to this adopted arrow without a lawful branch.
5. Build i.Independence and i.Context with those exact inputs, the explicitly
   supplied `i.TerminalReadPremise`, joint origin, shared coupler, permutation,
   `i.FRAME`, `i.CONTROLLER` and declared `setting_id`. Old local frame and
   controller remain separately in BridgeContext; changing interface labels
   is not declaring that the earlier control had the later semantics.
6. With `i_local` the constructed i.LocalInput and `fixed_t=i.F(3,5)`,
   verify the **entire converted preterminal kernel** equals
   `i.k_from_local(i_local.residual,fixed_t,normalized=True)` and passes
   `i.inverse_k_span(converted_kernel,fixed_t)` and
   `i.image_kernel(converted_kernel,fixed_t,normalized=True)`. Every API
   parameter is exact: Python's float expression `3/5` is not an accepted
   rational input. The inverse checks
   exact full-image reconstruction and equal blocks; no loose quotient or
   partial block comparison suffices. Construct i.State
   from the converted existing kernel with the explicit new domain/context,
   rather than physically executing `i.prepare_state` after the old coupling.
   The seed formula is an equality check, not a second preparation operation.
7. Set new joint `records=()` and `pending=()`, retaining the unmodified
   original c.State in the envelope. Local pending `("Z",)` is already
   applied and is not in i's A/B command vocabulary. Never flatten the two
   word namespaces, erase the old word or put Z into i.pending.
8. Check native mass is one and preserve cumulative p_r beta unchanged.
   Inclusion K_t→L_t is the same full kernel with a **separately declared
   reusable return contract**; it adds no probability, event or hidden reset.

The full retained record object is the original local prefix plus its current
typed pending word, independent reference decision/prefix, bridge context,
new joint literal-cut prefix and terminal or stop record. It is not a merged
matrix or a flattened total ordering of independent input events. For the
primary ready fixture the cut's `complete_precursor` is
`(("signal",0),("reference",0))`; the final read additionally retains
`("joint",0)` and uses event_id1. The cut has empty new command word; the
terminal has empty/A according to the observed a. The pending local Z remains
in the wrapper even after those joint records. The reference-unavailable
stop uses its distinct origin and both input predecessors; it is not an
i.TerminalRecord or an absent quantum outcome.

## 4. Proposed finite conditional composition theorem

Let x≥0 be an unnormalized local C input, with mass m(x). Let B_r be the
complete RI-08c Y branches and V_Z the actual local Z control, and write
T_r=V_Z B_r. Their ranges lie in C0 and sum of masses is m(x). Let G be the
fixed independent normalized-reference shared-coupling map C0→K_(3/5),
regarded by the explicit same-kernel inclusion in L_(3/5). G is positive,
real-linear and mass-preserving on this domain. Let C_alpha be literal cuts,
U_(w(alpha)) the supplied new empty/A commands, and e_gamma the complete
tilted scalar effects. Here w depends only on the retained alpha label.

For ready weight beta supplied independently, define unnormalized terminal
effects and reference-unavailable stop effects
\[
f_{r,\alpha,\gamma}(x)
=\beta\,e_\gamma\bigl(U_{w(\alpha)}C_\alpha G T_r x\bigr),
\qquad
g_r(x)=(1-\beta)m(T_r x).
\]
Each is a positive real-linear scalar effect on C. Under the stated complete
policy and type/availability premises,
\[
\boxed{\sum_r g_r(x)+\sum_{r,\alpha,\gamma}f_{r,\alpha,\gamma}(x)=m(x).}
\]
Thus the finite full-label output in the direct sum of scalar coordinates is
a mass-preserving positive map. Equal numerical outputs do not identify labels.
For a normalized start it is a probability law; multiplying by a separately
supplied incoming branch weight scales every leaf, not its conditional state.

**Proof obligation and argument.** The accepted local branch theorem puts
T_r x in C0 without altering the earlier domain. Fixed-reference tensor and
coupler maps are linear in this unnormalized signal input. On C0 they are
recordable and mass-preserving. The changed L_t contract closes literal cuts;
their masses sum to input mass. Commands preserve that mass and the terminal
effects sum to it. Summing gamma, then alpha, then r yields beta m(x); the
explicit stop effects give (1-beta)m(x). Composition proves positivity and
linearity, while the finite-tree telescoping proves completeness. It does not
claim the local unobserved instrument is the identity raw map.

For a **normalized parent** \(\widehat x\), every positive selected residual
branch obeys \(B\widehat x=p x_B\), where p is its conditional API
probability and x_B its normalized output. For a nonzero unnormalized parent,
\[
\boxed{Bx=m_{\rm in}(x)\,p(B\mid\widehat x)\,x_B,
\qquad \widehat x=x/m_{\rm in}(x).}
\]
Equivalently an external prefix weight lambda multiplies the normalized-parent
output as \(\lambda B\widehat x=\lambda p x_B\); a terminal scalar leaf
weighs \(\lambda e(\widehat x)\). Carry that incoming weight once at each
step. Multiplying all actual path factors must reproduce the displayed
unnormalized effect. Zero branches are retained as zero scalar law entries but supply no
conditional source or appended possible event. Faithful local and fixed
interior L_t mass make positive zero-mass residual branches zero; this design
does not extend that assertion through polarized endpoints.

Record/type invariants follow by induction only if each proposed wrapper
verifies the actual forward construction and preserves all prior anchors.
The only adaptive command decision receives the outcome-only tuple (a,b),
never a full record with a source-bearing Context or any raw source/audit
object. Domain-validation checks can reject an invalid
contract, but cannot serve as adaptive physical measurements. Terminal output
has no residual to feed into the recurrence. The fixed finite policy always
terminates in a read or explicit stop: there is no never-commit atom here and
no need to invoke RI-16 or silently assume an infinite history implementation.

## 5. Minimal exact acceptance fixture and refusals

The primary D_0, Y/Z policy and beta=2/3 are as in §2. They give
q_alpha=1/4 and conditional pre-read single-cell filtered Bloch coordinates
\[
(q,x,y,z)=(1,0,-4(-1)^r/5,3(-1)^b/5).
\]
For a=0 the new word is empty; for a=1, A transforms
\((y,z)\mapsto((-7y-24z)/25,(24y-7z)/25)\). Therefore the conditional
terminal plus probability s_(r,a,b) is

| Local r | Cut a | Cut b | s_(r,a,b) for sign + |
|---|---|---|---|
| either | 0 | 0 | 37/50 |
| either | 0 | 1 | 13/50 |
| 0 | 1 | 0 | 157/1250 |
| 0 | 1 | 1 | 13/50 |
| 1 | 1 | 0 | 37/50 |
| 1 | 1 | 1 | 1093/1250 |

Minus has probability 1-s. Each full successful leaf weighs
\(p_r\beta q_\alpha s=p_rs/6\) or \(p_r(1-s)/6\).
The sixteen positive read leaves total 2/3; the two unavailable-stop leaves
are 4/15 and 1/15, totaling 1/3. All eighteen labels remain distinct. In the
full eight-outcome read catalogue per cut, the six other-cell outcomes have
zero weight and cannot be selected. The complete prospective table has
2x4x8=64 ready-path coordinates (48 zero at this fixture), plus two stop
coordinates; zero entries are not fabricated committed records.
Conditionalizing on readiness, if asked,
is a separately named coarse question dividing by 2/3; it must not replace
the complete law or erase readiness/local/cut/word records.

Future acceptance must compare direct unnormalized native arithmetic with
the product of the actual accepted API weights, not only compare two wrappers
sharing the same formula. Reuse existing c branch/control/zero-selection,
RI-15 complex conversion/forward-target/context and i literal-cut/command/
terminal-source checks as references. Their accepted sources are dependencies,
not code to copy, edit or register again. New assertions must cover:

- Every native 4x4 and 16x16 Gaussian component, including the complex
  transpose convention; exact K_t equality and unchanged kernel at L_t entry.
- Both local weights, both independent selector branches, all cut/read
  outcomes, all eighteen positive leaves and exact total one. Readiness or
  root boundary weights must not be lost, inferred or multiplied twice.
- Full local/reference/joint/stop labels, input origins and exact precursors;
  local pending Z retained but never replayed or retagged as joint A; known
  a-based decisions demonstrably access labels only, not audited kernels.
- Refuse omitted/nonrational/out-of-range selector weights, noncomplete
  choice laws, unmatched supplied earlier weights, unavailable-read premise,
  and attempts to use provenance text as a verified numerical weight.
- Refuse direct nonzero-c conversion, wrong t/orientation/permutation/coupler,
  product rather than coupled source, changed raw target/context/history,
  foreign scalar/state classes, partial-trace repair and mismatched aliases.
- Refuse every terminal-as-source path, manufactured e(N)N/m(N), selection
  of zero weights, dropped reference-unavailable outcomes and merging labels
  merely because their matrices or probabilities match.
- Add a separate exact zero-local-branch input; preserve its zero scalar law
  coordinate without fabricating a selected record. Invalid protocol typing
  must fail the whole contract rather than masquerade as zero probability.

These are acceptance requirements, not tests added or executed by this plan.
Independent arithmetic during design review is not a new registered witness
suite or an implemented multi-API protocol.

## 6. Exact implementation scope, only if separately assigned

The minimal future files proposed for a reviewed implementation are:

| Proposed path (not created in this sitting) | Responsibility |
|---|---|
| `docs/validation/t8-q-finite-protocol-composition-2026-09-14/PROTOCOL_COMPOSITION.md` | Accepted-premise theorem, exact wrapper/policy contract and source-bound result; no new physical law. |
| `docs/validation/t8-q-finite-protocol-composition-2026-09-14/adapter.py` | Only the fixed weighted trace, reference decision/stop, lossless preterminal conversion and terminal envelopes described here. |
| `docs/validation/t8-q-finite-protocol-composition-2026-09-14/check.py` | Independent exact native/tree/metadata assertions and refusal cases above. |
| `scripts/run_qr_finite_protocol.py` | Separate source-pinned fixed-alias launcher; coordinator-owned, requiring its own reviewed source/closure contract. |
| `det8/tests/test_qr_finite_protocol.py` | Launcher/alias/source-binding and full orchestration regression contract. |

The actual executable dependency graph would bind the unchanged c model,
d model, RI-15 adapter and i model under unique aliases, plus the new adapter
and checks. In particular RI-15's literal imports `local_source` and
`joint_source` must resolve to those exact original modules; none of the
three different files named model.py may collide or be silently copied.
The [existing RI-15 launcher](../../scripts/run_qr_local_joint_adapter.py)
declares exactly four aliases and is not already a launcher for this graph.
Its [existing regressions](../../det8/tests/test_qr_local_joint_adapter.py)
show source-binding boundaries, not automatic acceptance of a changed loader.
No modification of that launcher, accepted sources, core, RET or the research
registry is needed or authorized by this design. Coordinator must explicitly
approve the separate implementation and loader scope before any files above
are created. New source hashes are pinned only after review, never auto-refreshed.

Completion of this sitting means a reviewed design and an exact missing-adapter
list. It is not protocol implementation, measured application performance,
physical operation availability, full QM, geometry/mass/gravity, or a launch
of another assignment. Design review and current source identity are recorded
in the [QR handoff](QR_HANDOFF.md). Stop for coordinator design acceptance.
