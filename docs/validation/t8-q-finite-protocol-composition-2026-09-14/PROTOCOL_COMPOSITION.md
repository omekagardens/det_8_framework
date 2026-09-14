# RI-18 — one exact finite probability and type composition

14 September 2026 UTC. **CONDITIONAL_FINITE_PROTOCOL_COMPOSITION;
FULL_LABEL_WEIGHT_ACCOUNTING; PRETERMINAL_TYPE_AND_CONTEXT_INTERCHANGE.**
Implementation, exact checks and independent full proof/source review are
complete. Coordinator review accepts the bounded mathematical theorem and
source contracts. Source-pinned launcher verification and publication are
tracked separately in the [coordination progress record](../../coordination/REVIEW_PROGRESS.md).

This implements the bounded route of the accepted
[RI-17 design](../../coordination/QR_PROTOCOL_COMPOSITION_PLAN.md), published
at ad04963b28a9232b6496f233d2f475c12f333d4c. It changes no accepted model,
instrument or physical claim. The [adapter](adapter.py) and independent
[checks](check.py) compose supplied mathematical operations. They are not a
general process SDK or a claim that those operations describe an apparatus.

## 1. Exact boundary and retained premises

The executable starts with the exact bound RI-08c `State`, normalized in
the full local cone
\[
\mathcal C=\{D(A,c):A\succeq |c|I\},\qquad
D(A,c)=\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix},\quad
Z=\operatorname{diag}(1,-1),\qquad m(D)=2\operatorname{Tr}A.
\]
Initial committed records and pending settings must both be empty, with the
accepted fixed local source-kind, controller and Pauli frame. Root weight is
one. This is an explicit conditional starting boundary, not an inference
about earlier preparation success. Wider histories, foreign/terminal source
types and different incoming weights are refused, not attached to the
fixture's id0 precursors. The mathematical homogeneous extension below does
not broaden that executable boundary.

The whole 4x4 complex Gaussian-rational input is retained. The initial c is
not set to zero, and the input is never replaced by J2Phi(D). The implemented
route explicitly supplies the accepted reusable local Y branches and local
Z control; a complete independent reference-ready/unavailable law; the
normalized t=3/5, Z-oriented reference on readiness; native tensor, signed
index convention and one shared coupler; the expressly adopted fixed-interior
L_t return type; its literal cuts and known A command; and the calibrated
available tilted terminal read. These are conditional operation/availability
premises, not consequences of bare DET, provenance or this software.

The ready/unavailable probabilities are exact nonnegative rationals summing
to one. Write them beta and 1-beta. The independently supplied law and its
named independence declaration are not inferred from source values or from
strings describing a selected reference. Each positive selected reference
branch has one origin-tagged record. A zero-weight choice has only a zero
prospective law coordinate, not an invented selected record or reference.
Unavailability yields an explicit scalar stop with its audit anchors, never
a fabricated failed-reference kernel.

`ReferenceLaw` requires both weights, the exact bound independence object
naming `signal` and `reference`, nonempty preparation and selector-law IDs,
and an explicit true declaration of conditional preparation availability.
The terminal-read premise is also supplied explicitly, not defaulted by the
protocol entry point. Its declared setting ID belongs to every prospective
scalar coordinate. On a stop this is planned-setting metadata, not evidence
that a read occurred. The read's fixed calibration and availability remain
validated even when beta=0. A known setting change cannot be flattened into
the same full-label law.

## 2. Finite conditional mass theorem

The theorem concerns unnormalized positive inputs in C. Set
\[
\Phi(D)=2A^T,\qquad J_2(\rho)=D(\rho^T/2,0),\qquad
Q_r=(I+(-1)^rY)/2,
\]
\[
p_r(x)=\operatorname{Tr}(\Phi(x)Q_r),\qquad
B_rx=p_r(x)J_2(Q_r),\qquad T_r=V_ZB_r.
\]
Here B_r is the already proved and separately supplied RI-08c reusable
branch, and V_Z is its actual mass-preserving Z control. It follows that
\[
T_rx=p_r(x)J_2(Q_{1-r}),\qquad
p_r(x)\ge0,\quad p_0(x)+p_1(x)=m(x).
\tag{1}
\]
The **output** c is zero because the supplied branch has that range. Earlier
nonzero-c inputs remain legitimate. Neither a hidden projection nor a global
C0 ban supplies this transition.

Let G be the accepted fixed normalized-reference tensor/shared-coupling map
from C0 to the full sixteen-label equal-block K_(3/5) image. It is positive,
real-linear and mass-preserving on C0. The new type adapter verifies equality
of every entry with that image before regarding the **same kernel** as an
L_(3/5) source under the expressly adopted larger return contract. It applies
no second coupler or reference preparation.

Let alpha=(a,b) range over four actual literal-cut outcomes and gamma=(a',b',s)
over eight actual terminal cell/sign outcomes. On L_(3/5), define
\[
C_\alpha N=P_\alpha NP_\alpha,\qquad
w(\alpha)=\begin{cases}()&a=0,\\(A)&a=1,\end{cases}
\]
and let U_(w(alpha)) be the supplied mass-preserving command map. It acts on
the filtered blocks by its known unitary congruence; it is not a clock or
an identified Hamiltonian. The e_gamma are the accepted positive tilted
scalar effects, summing to native total-entry mass m_16.

Define 64 prospective ready/read effects and two stop effects:
\[
f_{r,\alpha,\gamma}(x)
=\beta\,e_\gamma\bigl(U_{w(\alpha)}C_\alpha GT_rx\bigr),\qquad
g_r(x)=(1-\beta)m(T_rx).
\tag{2}
\]
Each coordinate retains its full path label, including readiness or
unavailability, local Y outcome, cut, actual new command word and terminal
cell/sign when applicable. Coincident numerical values do not merge labels.

**Theorem.** These 66 coordinates define a positive real-linear map on the
real span of C, with
\[
\boxed{\sum_r g_r(x)+\sum_{r,\alpha,\gamma}f_{r,\alpha,\gamma}(x)=m(x)
\quad(x\in\mathcal C).}\tag{3}
\]
Its output on normalized inputs is the complete finite protocol probability
law, including the separately declared unavailable-reference stops.

**Proof.** Equation (1) gives positive linear C→C0 branches and mass
completeness. Fixed-reference tensoring and the shared congruence are linear
in this signal input; their C0 image is recordable and preserves mass.
L_t's literal cuts have complete masses, and each subsequent supplied command
preserves them. The terminal effects sum to mass. Therefore summing gamma,
alpha and r in that order gives beta m(x). Stop effects contribute
(1-beta)m(x). Composing positive linear maps proves positivity and linearity
of each coordinate, and the scalar sum proves (3). This argument does not
assert that the local unobserved instrument preserves the full raw input;
its summed branch map generally does not equal the identity. ∎

For any normalized positive parent \(\widehat x\) and selected residual
branch B of positive weight p, the accepted API gives
\(B\widehat x=p x_B\) with normalized x_B. For a nonzero unnormalized
positive parent x, faithfulness guarantees m_in(x)>0 and
\[
\boxed{Bx=m_{\rm in}(x)\,p(B\mid\widehat x)\,x_B,
\qquad\widehat x=x/m_{\rm in}(x).}\tag{4}
\]
Thus a prefix weight lambda multiplies each returned conditional API factor
once: a residual becomes lambda p x_B and a terminal scalar weighs
\(\lambda e_\gamma(\widehat x)\). Successive normalization factors cancel
algebraically, recovering (2). No earlier branch probability is reconstructed
from a normalized snapshot, a label, an audit source or reference provenance.

Local and fixed-interior L_t mass are faithful: a positive zero-weight
residual branch is zero. Zero law coordinates remain explicit, but no
normalization, selected state or possible record is constructed for them.
Likewise beta=0 or 1 permits a zero selector branch without fabricating its
selected reference/stop event. Contract-validation failures are different:
they reject the declared operation, rather than being caught and relabeled
as a physical zero-weight outcome.

This fixed finite policy always terminates in a tilted read or explicit stop.
There is no never-commit atom and no infinite-history claim. RI-16's separate
countable-word convergence theorem neither implements this adapter nor is
needed for the finite sum proof.

### Initial-state information retained by this policy

Fix the complete reference law and all declared settings. Write
\(y(x)=\operatorname{Tr}(\Phi(x)Y)\), so
\(p_r(x)=(m(x)+(-1)^r y(x))/2\). Equation (1) shows that the first
Y branch erases the initial quotient's X and Z components and the initial
c from every subsequent normalized physical state. Consequently there are
fixed nonnegative 66-coordinate vectors \(v_0,v_1\), each of total mass
one and supported only on its own retained local-outcome label r, such that
\[
\mathcal P(x)=p_0(x)v_0+p_1(x)v_1.
\tag{5}
\]
Each vector includes its ready/read distribution and unavailable stop.
This holds also at beta=0 and beta=1; the two supports remain disjoint.
Thus the scalar law has real-linear rank two on the full input span, and
only one affine degree of freedom on normalized inputs. For two normalized
inputs with the same declared settings and reference law,
\[
\operatorname{TV}(\mathcal P(x_1),\mathcal P(x_2))
=\tfrac12\sum_r|p_r(x_1)-p_r(x_2)|
=\frac{|y(x_1)-y(x_2)|}{2}.
\tag{6}
\]
The first equality follows from the disjoint unit-mass supports; the second
from the displayed formula for p_r. Both Y eigenstates are legitimate C
inputs, so the rank statement is exact, not merely an upper bound.

In particular, \(\rho_\pm=(I\pm X/2)/2\) with respectively
\(c_+=1/20\) and \(c_-=\mathrm i/20\) give distinct raw and quotient
inputs \(D(\rho_\pm^T/2,c_\pm)\) but identical complete scalar laws.
Their A eigenvalues are 3/8 and 1/8, exceeding |c|=1/20, so both are lawful.
Their original known inputs remain different in the audit envelopes.
Equations (5)–(6) concern observation probabilities, not equality of those
audit objects. Conditional on r, later reads add no information about this
initial input. This protocol is therefore not initial-state tomography;
completing its composition cannot be reported as such.

## 3. Full-kernel and record/type invariants

The numerical interchange is component-wise exact. The bound c, d and i
models use distinct `G` classes: copy real and imaginary Fractions into the
target class without float conversion. The preterminal native order remains
8a+4i+2b+j, with the same signed native/grouped convention and shared coupler.
Compare **all** entries of the coupled RI-15 source to
`i.k_from_local(i_local.residual,i.F(3,5),normalized=True)`, then validate full
K_t and L_t membership. A partial trace that projects an outsider, an omitted
complex transpose or a new preparation call is not this interchange.

The accepted RI-15 wrapper binds the current local source, product and single
coupling by exact forward construction. It accepts the prior actual local
Y branch and pending Z without replay. The new L_t envelope consumes that
validated **coupled preterminal** object, never the old `JointTerminal`.
It adds the explicit L_t domain/context and terminal-read premise while
leaving the same native kernel and cumulative probability unchanged.

The typed history invariant is inductive: each stage retains its immutable
prior anchor and its actual accepted forward result. The local Y record is
event0 in origin `signal`; the selected reference decision is event0 in
`reference`, with no cross-input predecessor. Ready coupling establishes a
new joint context but is not itself a committed record. The L_t literal cut
is joint event0, with predecessors `(("signal",0),("reference",0))`.
The final tilted read is joint event1 and additionally retains `(joint,0)`.
Listing independent input prefixes does not order one origin before the other.

The local pending `("Z",)` remains in the original c.State retained by the
RI-15 context and every subsequent audit anchor. It is not an i command word.
New i pending starts empty; the literal cut stores that empty new word, then
the terminal read stores exactly empty or A from the one later command.
No word is erased, flattened into another namespace, reapplied or reconstructed
from its resulting matrix. Fixed original local frame/controller/source-kind
and later fixed joint frame/controller remain separately retained.

The only adaptive choice receives a validated outcome-only tuple (a,b), not
even a read-only `JointRecord`, whose Context would expose raw input kernels.
The fixed immutable table is `((),("A",))`. No source-bearing callback,
probability diagnostic, c value, norm or audit payload is a policy input.
Validators inspect raw data for contract validity, never to choose another
physical branch or conceal a rejected positive path.

Reference unavailability has one selected reference record and a separate
`protocol-stop` report with event0, both tagged input predecessors and its
distinct action/outcome. The stopped wrapper retains the exact weighted local
source as audit data but supplies no failed-reference state. Successful
terminal wrappers retain their full preceding L_t/control/cut/bridge chain,
not just i's pre-read source, which alone lacks some original local metadata.

The terminal result is only its scalar effect/probability and full record,
with pre-read audit data. Neither that audit nor an external weight licenses
the generally nonlinear putative residual e(N)N/m(N). No old terminal object
is retagged reusable and no postread residual, reset or continuation is added.

## 4. Exact fixture and acceptance boundaries

The primary input is
\[
\rho_0=(I+3Y/5)/2,\qquad D_0=D(\rho_0^T/2,1/20).
\]
The eigenvalues of A=\(\rho_0^T/2\) are 2/5 and 1/10, so A≥|c|I;
nonzero c and complex off-diagonal entries are genuine input payload. The
actual Y branch gives p_0=4/5 and p_1=1/5. The following Z control gives
\(\rho_r=(I-(-1)^rY)/2\) in C0. With beta=2/3, every K_t cell has
conditional weight 1/4. After its literal cut the occupied filtered block has
Bloch coordinates
\[
(q,x,y,z)=(1,0,-4(-1)^r/5,3(-1)^b/5).
\]
For a=1, A sends \((y,z)\) to
\(((-7y-24z)/25,(24y-7z)/25)\); for a=0 the command is empty. The
terminal-plus conditional probabilities in cell order 00,01,10,11 are

| Local Y outcome | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| 0 | 37/50 | 13/50 | 157/1250 | 13/50 |
| 1 | 37/50 | 13/50 | 37/50 | 1093/1250 |

For each row/cell write this value h. The two full read weights are
\(p_rh/6\) and \(p_r(1-h)/6\). They sum over all sixteen positive
read leaves to 2/3. The two unavailable stops weigh 4/15 and 1/15,
totaling 1/3. The full law has 66 prospective coordinates: eighteen positive
and forty-eight zero. The latter are not fabricated committed records.

A separate normalized input J2(Q_Y,0) has p_0=1 and p_1=0. The entire
zero-r branch must stay present as zero law coordinates without calling
positive-selection constructors, inventing its Y/reference records or
claiming a later conditional state. Selector endpoints and invalid laws,
foreign/terminal/broad-history inputs, metadata/source mismatches and denied
operations delimit the executable contract; the independent checks must
exercise each implemented boundary.

## 5. Source contract, verification and handoff

The six module aliases are fixed: `local_source` (c), `joint_source` (d),
`local_joint_adapter` (RI-15), `terminal_read_source` (i), `finite_protocol`
(this adapter) and `check`. RI-15's literal local_source/joint_source imports
must resolve to the identical module instances used here, not copied or
lookalike classes. The new adapter imports the four accepted aliases; its
checker imports finite_protocol. Exact source-byte pins and the isolated
launcher are separate coordinator responsibilities, not properties that
module-name assertions alone establish.

The public entry is `run_protocol(boundary, law, terminal_read)` or the
equivalent `ProtocolRun(boundary, law, terminal_read)`. Its immutable result
has `coordinates`, `probabilities`, positive selected `leaves` and `total`.
Stage constructors derive their outputs and weights from actual forward
calls; callers cannot supply those derived fields:

| Interface | Required inputs |
|---|---|
| `Boundary` | Exact c.State; root_weight defaults to 1 and must equal 1; the complete fixed availability tuple is retained. |
| `ReferenceLaw` | ready, unavailable, independence, preparation_id, law_id, preparation_available. |
| `WeightedLocal`; `ReferenceDecision` | boundary and local outcome; complete law and selected reference outcome. |
| `WeightedJoint`; `LtEnvelope` | weighted local and ready decision; weighted joint and terminal_read. |
| `convert_preterminal` | Exact coupled source, matching WeightedJoint anchor and terminal_read. |
| `CutEnvelope`; `CommandEnvelope` | LtEnvelope and cell outcome; CutEnvelope only. |
| `WeightedTerminal` | CommandEnvelope and complete terminal outcome. |
| `StopReport`; `StoppedBranch` | WeightedLocal, unavailable ReferenceDecision and planned terminal_read premise. |
| `LawEntry` | PathLabel, exact scalar weight and matching selected leaf, or None for zero. |

`PathLabel` retains local_outcome, reference_outcome, preparation_id, law_id,
cut_outcome, command_word, terminal_outcome, policy_id and terminal_setting_id.
Nonperformed cut/read fields are None on unavailable paths; the planned
setting ID remains. `policy_word(outcome)` accepts validated outcome bits
only. `primary_boundary()`, `zero_local_boundary()` and `primary_law()`
are expressly supplied fixture helpers, and `validate_aliases()` checks
dependency module identity, not source-byte pins.

The new adapter's standard-library imports are only `dataclasses` and
`fractions`, alongside the four fixed source aliases. The check source uses
`unittest`, `dataclasses`, `fractions`, `itertools` and `finite_protocol`.
It implements its own Gaussian Fraction-pair matrix arithmetic, native
tensor/grouping/congruence, cuts, weighted controls and scalar effects.
It does not use accepted branch/coupling/cut/control/read arithmetic to
produce its independent unnormalized expected law.

Draft execution may use an explicit temporary alias loader. Such runs are
not accepted source-pinned launcher integration. Neither the earlier
four-alias RI-15 launcher nor the general registry is modified here. The new
coordinator launcher/regressions, their independent review and publication
remain outside this task's file ownership. No accepted sources are copied
or edited to manufacture compatibility.

All 31 focused exact checks pass with the temporary six-alias loader, normally
and under Python optimization. The checked actual path factors reproduce the
independent unnormalized native law and full intermediate kernels. Coverage
includes the primary and zero-local fixtures, selector endpoints, retained
settings/history and refusal boundaries, and the same-Y distinct-input
counterexample. These are 31 new focused checks, not a replay or expansion of
the existing 411-witness registry inventory. Both new sources pass scoped
lint and formatting checks; all 60 held predecessor/design identities match.
Independent full checker/API and proof/source reviews found no blocker;
review details and exact handoff identities are recorded in the
[QR handoff](../../coordination/QR_HANDOFF.md). Finite tests supplement the
written finite theorem, not substitute for it.
No broad predecessor-suite replay, new physical selection, RET/application
work, measured pilot, generic SDK or automatic successor is part of this bundle.
Coordinator review accepts this bounded theorem and source contract; the
[progress record](../../coordination/REVIEW_PROGRESS.md) tracks separate pinned
execution and publication.
