# RI-08c — repeatable source-cone record instruments

13 September 2026. **CONDITIONAL_EXPOSED_RAY_INSTRUMENT_THEOREM;
FINITE_SERIAL_RECORD_CLOSURE; RESTRICTED_PREPARATION_REACHABILITY.**
Internal mathematical classification under new operational premises.
No Kraus or Lüders update is inserted as a premise. No strict DET derivation
of those operational premises or physical implementation is claimed.

## 1. Input, question and additional premises

The accepted [RI-08b result](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md)
supplies a conditional maximal viable cone on the **full** four-label raw
kernel space, including cross-cell payload:

\[
\mathcal C=\left\{D(A,c)=
\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix}:
A\succeq |c|I,\ c\in\mathbb C\right\},\qquad Z=\operatorname{diag}(1,-1).
\]

Its actual real span V has dimension six: four Hermitian A coordinates and
two real coordinates of c. Its faithful total-entry mass and positive
quotient/section are

\[
m(D)=2\operatorname{Tr}A,\quad \Phi(D)=2A^T=\rho,\quad
J_2(\rho)=D(\rho^T/2,0),\quad \Phi J_2=\mathrm{id}.
\]

Here m is normalization mass, **not rest mass**. The section is a
mathematical map; its definition alone does not authorize an operation.
The c=0 slice is not the entire starting domain.

For a declared fixed-frame Pauli setting \(a\in\{X,Y,Z\}\) and outcome
\(r\in\{0,1\}\), define

\[
Q_{a,r}=\frac{I+(-1)^r\sigma_a}{2},\quad
e_{a,r}(D)=\operatorname{Tr}(\Phi(D)Q_{a,r}),\quad
h_{a,r}=J_2(Q_{a,r}).
\]

These effects are the RI-08b Pauli readout questions. I/H/P followed by
the base cell read gave the positive X/Z/Y questions respectively. Direct
availability of the reusable fixed-frame instrument below is a **new**
premise, not inferred from those terminal readouts.

We seek branches \(B_{a,r}:V\to V\) satisfying, for every \(d\in\mathcal C\):

1. **Real linearity and same-cone range:** \(B_{a,r}d\in\mathcal C\).
   Outputs have the same declared source type and coordinate frame, not
   the earlier separately typed raw terminal-cut range.
2. **Effect calibration:** \(m(B_{a,r}d)=e_{a,r}(d)\). Thus the two branch
   masses sum to m(d); their summed raw map need not be the identity.
3. **Perfect same-setting repeatability:**
   \(e_{a,r}(B_{a,r}d)=m(B_{a,r}d)\).
4. **Operational availability:** these fixed setting branches and their
   recorded outcomes are available at the declared type/controller. Actual
   controls and choices depend on known settings and committed history,
   not on an oracle inspecting hidden residual values.

The equalities are required on the **entire** cone, not merely on a small
preparation set reachable in a particular experiment. Same-cone range,
repeatability, calibration and availability are additional candidate
principles. They do not follow from bare DET or from the old literal cut.

## 2. General finite-dimensional exposed-ray lemma

Let K be a closed convex cone spanning a finite-dimensional real vector
space W. Let m be a real-linear functional strictly positive on
\(K\setminus\{0\}\), and let e be an effect: \(0\le e\le m\) on K.
Suppose the repeat face is a normalized ray,

\[
F_e=\{x\in K:(m-e)(x)=0\}=\mathbb R_{\ge0}h,
\qquad m(h)=e(h)=1.
\]

It is an exposed face because \(m-e\) is nonnegative on K. This is a
finite-dimensional cone lemma, not an assumption that K is polyhedral.

**Lemma.** There is exactly one positive real-linear map B on W with
\(mB=e\) and \(eB=mB\). It is

\[
B(x)=e(x)h.
\]

**Proof.** Positivity puts Bx in K, and repeatability puts it in F_e for
every x in K. Hence Bx=α(x)h for a nonnegative scalar. Applying m gives
α(x)=e(x), fixing B on K. Since K spans W, real linearity fixes its value
on every signed direction of W. Conversely \(B=e\otimes h\) is positive,
has the specified mass, and is repeatable because e(h)=1. ∎

Consequences include \(B^2=B\), a positive normalized conditional output h
whenever e(x)>0, and Bx=0 whenever e(x)=0. Faithful mass rules out positive
nonzero zero-mass outputs. For effects \(e_r\) summing to m and normalized
ray faces h_r, the branches \(e_r\otimes h_r\) form a mass-complete
instrument. The lemma classifies mathematical maps; it does not prove
their physical availability.

## 3. Application: repeatability forces the full raw output

**Exposed-face theorem.** For every Pauli rank-one projector Q,

\[
\{d\in\mathcal C:e_Q(d)=m(d)\}=\mathbb R_{\ge0}J_2(Q).
\]

**Proof.** Let \(\rho=\Phi(d)\succeq0\). The face condition is
\(\operatorname{Tr}(\rho(I-Q))=0\). In a basis diagonalizing Q, the
complementary diagonal entry of ρ vanishes. Positivity forces both
off-diagonal entries to vanish, so \(\rho=tQ\), with t=m(d)≥0.
Consequently \(A=tQ^T/2\) has rank at most one. Since
\(A\succeq |c|I\), its null direction forces c=0, including at t=0.
Thus \(d=tJ_2(Q)\). The converse follows by substitution. ∎

The general lemma now proves existence and **uniqueness on all six real
coordinates**:

\[
\boxed{B_{a,r}(d)=e_{a,r}(d)h_{a,r}
=\operatorname{Tr}(\Phi(d)Q_{a,r})J_2(Q_{a,r}).}
\]

In particular c is zero **as a conclusion about the output range**, not
by deleting it from the input or assuming a quantum image cone. For a
nonzero source with e=0 the entire output is exactly the zero 4×4 kernel;
there is no surviving dark raw branch inside this faithful source cone.
The implementation refuses normalization or commitment of that zero branch.

For e>0 the conditional output is exactly h. It preserves the full
four-label matrix representation rather than replacing it with an unlabeled
qubit state. In the quotient,

\[
\Phi B_{a,r}(d)=\operatorname{Tr}(\rho Q_{a,r})Q_{a,r}
=Q_{a,r}\rho Q_{a,r}.
\]

The last identity uses rank one and is a **derived correspondence**, not
an inserted Kraus/Lüders update. No claim is made about general projectors,
degenerate measurements, arbitrary POVMs or all quantum instruments.

For a fixed axis, \(e_{a,s}(h_{a,r})=\delta_{sr}\), so

\[
B_{a,s}B_{a,r}=\delta_{sr}B_{a,r}.
\]

This is same-setting repeatability on unnormalized branches. Summing the
branches preserves m and dephases the quotient in that Pauli basis; it
does not preserve all raw information. Representing this sum for aggregate
statistics does not license erasing the actual committed outcome record.
For any two declared rank-one outcomes Q and R, the serial formula is
\(B_RB_Q(d)=e_Q(d)\operatorname{Tr}(QR)J_2(R)\); Pauli transition
probabilities are consequently 0, 1/2 or 1 after the first selected outcome.

## 4. Settings, frames and actual controls

The RI-08b controls remain
\(S_U D=W_UDW_U^\dagger\), \(W_U=\operatorname{diag}(U,ZUZ)\), with
H, P, P inverse and Z as the finite declared generators. They act on the
quotient as \(\rho\mapsto\bar U\rho U^T\). They are actual residual
transformations, not changes of the record or passive relabelings.

Use a fixed pair-coordinate frame and keep these distinct:

- **Actual control word w:** controls already applied, once, to the current
  raw residual since the preceding commitment. The word remains known.
- **Measurement axis a:** the projector Q_a in that unchanged fixed frame.
  Committing that measurement does not apply w again or secretly apply
  its inverse.
- **Controller/type and history:** retained external context determining
  which actions are legal and, for feedback, which action is chosen next.

If the current residual is \(S_wd\), measurement is
\(B_{a,r}(S_wd)\). Its record contains a, r, w, the source type, frame,
controller and actual precursor. The normalized posterior is h_a,r **in
the same frame**. A repeat with no intervening control applies B_a again,
not \(B_aS_w\). After recording w, the pending word is cleared, but the
committed word is never deleted.

For example an H control sends an X-positive source to Z-positive. A Z
read then returns its positive outcome certainly. Repeating Z returns the
same result certainly. Reapplying the old H would instead give probabilities
1/2,1/2; that is a different operation, not repeatability.

An axis change, or a new explicit control, is legal but changes the
experiment. Three fixed Pauli instrument families are being supplied here;
no arbitrary continuum of rotations or settings is inferred. Algebraic
conjugation identities do not themselves establish availability.

## 5. Mixtures, finite serial composition and feedback

For source preparations with the same declared operational context and
explicit convex weights, \(d=\sum_i p_i d_i\) gives

\[
B_r(d)=\sum_i p_i B_r(d_i),\qquad
e_r(d)=\sum_i p_i e_r(d_i).
\]

When the branch probability p=e_r(d)>0, conditioning reweights components
by \(p_i e_r(d_i)/p\). Every positive component has the same posterior h_r.
This does not justify combining incompatible known records into one state:
a joint ensemble retains its selector and all component histories. A
residual-only mixture is an explicitly declared preparation or marginal
description, not record erasure.

**Finite serial/feedback theorem.** At each node of a finite protocol tree,
let a known controller choose a finite actual control word and Pauli axis
using only the committed prefix and declared settings. Append the outcome
and actual action metadata on each positive branch. Then every branch map

\[
T_{h,r}=B_{a(h),r}S_{w(h)}
\]

is real-linear, positive on \(\mathcal C\), same-source-typed and locally
mass-complete when summed over r. Products along every finite history remain
positive. Induction from the leaves gives
\(\sum_{\text{leaves }\ell}m(T_\ell d)=m(d)\), including declared early-stop
leaves. Every positive conditional state is normalized inside the same cone.
Any zero-mass source-cone branch is the entire zero kernel and is never
normalized or selected. Thus there is no hidden zero-probability commitment.

All outcomes, actual words, frames/controllers and earlier records remain
distinct even if different histories happen to have equal residual matrices.
The implementation uses fresh consecutive event ids and the entire current
prefix as the chosen precursor. This is a finite chain-recording fixture;
it neither derives a general event-growth law nor identifies records with
all present activity. Supplied snapshot validation checks grammar and type,
not global preparation reachability from an earlier history.

The theorem applies to every specified finite legal tree, not just the
tested examples. It asserts no unbounded stopping-time limit, autonomous
silent dynamics, arbitrary policy oracle, global growth or geometry.

## 6. Countermodels locating the additional premises

### 6.1 Same effects and same range do not force repeatable outputs

For any fixed normalized \(h\in\mathcal C\), the branches
\(R_{a,r}(d)=e_{a,r}(d)h\) are positive, real-linear, same-cone and
mass-complete. Choose \(h_*=J_2(I/2)\). Then

\[
e_{a,r}(R_{a,r}d)=\tfrac12 e_{a,r}(d),
\]

so a positive first outcome need not repeat. One can even choose a mixed
normalized h with c≠0. Effect calibration and source-cone range alone
therefore do not select the new branch or force its output c to vanish.
Perfect repeatability is load-bearing.

### 6.2 Leaving the source cone permits the old raw-cut behavior

For the base X question, extend the target to the full two-cell
recordability cone \(K_{\mathcal P}\), explicitly using target effects
\(\widetilde e_r(d)=q_r(d)=\beta_r^\dagger d\beta_r\) and total-entry mass.
On the source \(\widetilde e_r=e_{X,r}\); this target extension is essential,
since the source-only Φ/e formula is not defined on arbitrary cut outputs.

The literal maps \(L_r(d)=E_rdE_r\) are positive into that larger target,
have the same prescribed source effects and satisfy
\(\widetilde e_r(L_rd)=m(L_rd)\). Nevertheless they leave \(\mathcal C\)
for every nonzero source and differ from B_X,r as full raw maps.
For d=h_*, a positive cut is supported in one cell; B_X,r has both
paired blocks. For d=J2(Q_X,1), the r=0 literal cut is nonzero with zero
mass, whereas B_X,0(d)=0 exactly.

This locates the same-source-range premise. It does not authorize applying
the new source instruments to the separately typed earlier terminal cuts,
nor does it supply a reset or return map on that target. The implementation
rejects terminal inputs to source controls and commitments.

## 7. Preparation reachability is a separate, smaller result

Fix the initial normalized preparation \(h_*=J_2(I/2)\). Allow only the
finite Clifford control catalogue, the Pauli instruments just derived under
their additional premises, positive-outcome conditioning and finite
record-based feedback. Availability of this initial preparation is explicit.

**Fine-history reachability theorem.** With every known selection and outcome
retained and conditioned upon, the reachable normalized raw residuals are
exactly

\[
\{h_*\}\ \cup\ \{J_2(Q_{a,r}):a=X,Y,Z,\ r=0,1\}.
\]

**Proof.** Controls leave h_* fixed. Every Pauli outcome from h_* has
probability 1/2, so all six eigenstates are reachable. Clifford controls
permute these six projectors, including the Y transpose convention.
Every subsequent positive Pauli outcome resets to one of the same six.
Finite induction proves closure and excludes all other conditional
residuals. No operation creates a nonzero c from this c=0 preparation. ∎

Distinct committed histories leading to one of these residuals remain
distinct full states. This theorem concerns their residual projection, not
a quotient identifying the histories.

**Explicit finite-mixture interface.** If finite classical preparation
randomization and the corresponding record-blind residual marginal are
additionally available, their normalized quotient marginal set is exactly
the Pauli stabilizer octahedron:

\[
\rho=\tfrac12(I+xX+yY+zZ),\qquad |x|+|y|+|z|\le1.
\]

The joint ensemble retains its selector, actual controls and all component
histories. Its average kernel is a declared marginal, not a new single
state made by deleting committed records or silently forgetting a known
controller. Conditioning on a retained selector returns its component.
Thus randomization alone does not enlarge the fine-history-conditioned
seven-state set when all choices remain known.
This is a set-of-marginals reachability theorem, not a predictive quotient
for selector-aware feedback: if later actions consult the selector or
history, the full joint ensemble remains necessary.

**Proof of marginal classification.** The six vertices have Bloch vectors
±e_x, ±e_y, ±e_z; h_* is their center. Convexity gives the upper bound.
Conversely any vector v with ℓ1 norm s≤1 has the finite decomposition
\(\sum_a |v_a|\,\operatorname{sgn}(v_a)e_a+(1-s)0\), omitting zero terms.
Each term is an available conditioned preparation, so explicitly permitted
randomization produces that marginal. Controls preserve the octahedron;
any subsequent positive Pauli outcome is again a vertex. Normalized
posterior mixtures reweight nonnegative coefficients, preserving closure
under finite randomized feedback. ∎

Arbitrary finite **real** weights attain the full closed octahedron;
exact rational weights attain exactly its rational-coordinate points.
The executable uses the latter. Neither premise is automatically the same
as a particular finite fair-coin-only implementation. If outcome averaging
or selector forgetting is admitted elsewhere, it is already a mixture
interface and must not be silently placed in the “without mixing” case.
For example, measuring X on h_* and applying H only after the negative
outcome gives conditional X-positive or Z-negative states; their
record-blind average has Bloch vector (1/2,0,−1/2), outside the seven-state
set but inside the octahedron. Both recorded histories remain intact.

The octahedron is strictly smaller than the Bloch ball. The exact state
with Bloch vector (3/5,0,3/5) is positive because its squared Euclidean
norm is 18/25<1, but its ℓ1 norm is 6/5>1. Its c=0 section is admitted
by the maximal mathematical cone and is not reachable under this
preparation catalogue. Raw admitted c≠0 states are also unreachable from
h_* with these operations. Maximal-cone tomography and full-cone branch
uniqueness do **not** supply full physical preparation richness.

## 8. What has and has not been derived

The new result is stronger than a terminal-read correspondence: the stated
range/effect/repeatability premises uniquely determine a reusable raw
instrument, including the fate of c, and prove finite serial record closure.
It is weaker than full QM or a DET-native selection theorem. In particular:

- The six-dimensional input cone itself still rests on RI-08b's supplied
  controls and calibration. No quarter-phase or complex-field selection
  is proved here.
- Same-cone output, perfect repeatability on the whole cone, calibrated
  effects and reusable availability are additional operational principles.
  They have not been formally entailed by DET's existing axioms.
- Rank-one qubit projector form is a conditional output theorem, not
  all-POVM/all-instrument availability or an ancillary complete-positivity
  theorem. No composite systems or quantum advantage are established.
- Full preparation richness remains false for the stated initial state
  and catalogue, even allowing the explicit finite-mixture marginal.
- No reset on earlier terminal targets, unbounded-history law, native
  growth, mass, geometry, gravity, empirical or release promotion follows.

This is the bounded RI-08c answer, not an authorization or design for a
successor. The remaining open questions concern justification and physical
availability of the additional principles. The QR owner stops for
coordinator acceptance. Accepted bundles, RI-11, RET, coordinator-owned
registries/trackers, QR-05 atlas, clocks/book work and κ-gravity remain
untouched. Option B and Status M remain unchanged.

## 9. Exact witnesses and reproduction

[model.py](model.py) implements Gaussian-rational full raw kernels, signed
span branches, declared fixed-frame controls and immutable record-preserving
reusable commitments. The literal-cut countermodel has a separate terminal
type. Mixing is an explicitly requested residual marginal, not a history
rewrite. [check.py](check.py) supplies independent exact witnesses.

The general proofs hold on the full real/complex cones. The finite exact
checks are regression and algebraic witnesses, not proof-assistant
certificates or empirical validation. Final replay, review and source hashes
are recorded in the [handoff](../../coordination/QR_HANDOFF.md).

```sh
.venv/bin/python -B docs/validation/t8-q-repeatable-record-instrument-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-repeatable-record-instrument-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-repeatable-record-instrument-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-repeatable-record-instrument-2026-09-13
```
