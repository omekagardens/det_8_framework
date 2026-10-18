# RI-08e — domain-aware repeatability robustness

13 September 2026. **CONDITIONAL_C0_BRANCH_CLASSIFICATION;
SHARP_ONE_STEP_RAW_BOUNDS; FINITE_RECORD_PROTOCOL_ROBUSTNESS.**
Uniform error is an assumed mathematical full-domain bound, not an estimate
inferred from the finite witnesses or experimental calibration.

## 1. Two domains, not one combined premise set

The [RI-08b local-only cone](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md) is

\[
\mathcal C=\left\{D(A,c)=
\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix}:A\succeq |c|I\right\},
\quad Z=\operatorname{diag}(1,-1),\quad c\in\mathbb C.
\]

It has a six-dimensional real span V. Total-entry mass, the positive
quotient and section are

\[
m(D)=2\operatorname{Tr}A=\operatorname{Tr}D,\quad
\Phi(D)=2A^T,\quad J_2(\rho)=D(\rho^T/2,0).
\]

Mass is faithful on this cone. The equality with ordinary trace holds on
this span, not on arbitrary raw kernels. The untwist
\(V_0=\operatorname{diag}(I,Z)\) gives blocks
\(\left(\begin{smallmatrix}A&cI\\\bar cI&A\end{smallmatrix}\right)\).

If [RI-08d's additional composite viability](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)
is imposed, the surviving local cone is instead

\[
\mathcal C_0=\{D(A,0):A\succeq0\}.
\]

Its real span has dimension four, and Φ is injective with inverse J2.
This is the **primary domain** for the branch classification below. It
must not admit a nonzero-c input imported from the broader local-only
model. Results expressly labeled “on C” do not simultaneously impose
RI-08d's composite premises. Neither choice here establishes a globally
selected composite theory.

For a declared rank-one Pauli outcome Q, let
\(e_Q(d)=\operatorname{Tr}(\Phi(d)Q)\), and choose a domain K equal to C0
or, where explicitly stated, C. An approximate branch \(\widetilde B_Q\)
is assumed real-linear on the **entire actual span**, positive K→K, with

\[
m(\widetilde B_Qd)=e_Q(d),\qquad
0\le(m-e_Q)(\widetilde B_Qd)\le\epsilon e_Q(d),
\qquad 0\le\epsilon\le\tfrac12.
\]

The complementary branch has the complementary exact effect, so summed
mass is complete. The uniform ε may bound several axes, controllers or
histories, but must hold for every permitted branch on its whole declared
cone. Domain, calibration, same-domain range, availability and the uniform
bound are additional mathematical premises. They are not derived from DET
or from a finite set of tested preparations.

The ideal comparison branch is the
[RI-08c repeatable branch](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md),
\(B_Q(d)=e_Q(d)J_2(Q)\). No Kraus or ancillary positivity premise is used.

## 2. C0 classification before any repeatability requirement

**Theorem.** Let \(S_0=\operatorname{span}_{\mathbb R}\mathcal C_0\).
Every positive real-linear \(\widetilde B:S_0\to S_0\) on this
four-dimensional span with exact mass effect e_Q has the form

\[
\boxed{\widetilde B(d)=e_Q(d)h_Q,\qquad h_Q\in\mathcal C_0,\quad m(h_Q)=1.}
\]

Conversely every such h_Q gives a positive calibrated branch. Thus the
branch is uniquely specified **by** h_Q, but calibration alone does not
uniquely choose h_Q. No repeatability or quantum instrument form is assumed.

**Proof.** Transport the branch through the positive linear isomorphism
between C0 and PSD2. In a Q-diagonal basis, let L be the resulting positive
real-linear map on Hermitian 2×2 matrices, with
\(\operatorname{Tr}L(\rho)=\rho_{00}\).
Positivity and faithful trace give \(L(|1\rangle\langle1|)=0\).
Write \(H=L(|0\rangle\langle0|)\); then H≥0 and TrH=1.

For every real t, positivity on the rank-one input formed from (1,t)
implies \(H+tL(X)\succeq0\), because the t² term maps to zero. A Hermitian
line of this form can be positive for all positive and negative t only
if L(X)=0: otherwise some vector expectation changes sign for large t.
The same argument with (1,it) kills L(Y). These four Hermitian directions
span the input, so \(L(\rho)=\rho_{00}H\). Transporting back proves the
formula with h_Q=J2(H). Its converse is immediate. ∎

The use of arbitrary-coherence rank-one inputs is a **whole-cone positivity
requirement**, not an assertion that all such preparations are physically
available. It cannot be replaced by positivity only on the previously
reachable stabilizer octahedron without another proof.

The uniform repeatability defect on C0 is equivalent to

\[
e_Q(h_Q)\ge1-\epsilon.
\]

Necessity follows by applying the branch to J2(Q); sufficiency follows from
the classified formula. At ε=0 positivity gives h_Q=J2(Q), recovering
perfect-repeatability uniqueness. At every ε>0 an entire cap of density
matrices is allowed. This is a complete classification of the mathematical
C0 branches under the stated requirements, not just example reset maps.
Nearby outputs outside the old preparation catalogue require additional
approximate-instrument availability; they are not silently inferred as
preparable by the previously supplied Clifford/Pauli controls.

## 3. Sharp one-step raw trace-norm bound on either domain

Use the Hermitian trace norm \(\|M\|_1=\operatorname{Tr}\sqrt{M^\dagger M}\).
Fix positive d and p=e_Q(d). Faithful mass and calibration imply that p=0
gives \(\widetilde B_Q(d)=0\) as the **entire raw kernel**. No conditional
normalization or record is assigned to this branch.

For p>0, write the normalized quotient output in a Q-diagonal basis as

\[
\rho_{\mathrm{out}}=\frac{\Phi(\widetilde B_Qd)}p
=\begin{pmatrix}1-s&z\\\bar z&s\end{pmatrix},
\qquad 0\le s\le\epsilon.
\]

Positivity gives \(|z|^2\le s(1-s)\). On the broader C domain the output
raw coordinate also obeys

\[
|c_{\mathrm{out}}|\le\lambda_{\min}(A_{\mathrm{out}})
\le ps/2\le\epsilon p/2.
\]

On C0, c_out=0 already follows from range. For the difference from the
ideal raw branch, put \(a=\sqrt{s^2+|z|^2}\). The traceless block difference
\(\Delta A=A_{\mathrm{out}}-pQ^T/2\) has eigenvalues ±pa/2. After untwist,
the full raw difference has eigenvalues

\[
\pm pa/2\ \pm |c_{\mathrm{out}}|.
\]

Since \(|c_{\mathrm{out}}|\le ps/2\le pa/2\), their absolute values sum to
2pa. Consequently the raw and quotient distances in this particular
comparison agree exactly, even on C:

\[
\boxed{\|\widetilde B_Qd-pJ_2(Q)\|_1
=2p\sqrt{s^2+|z|^2}
\le2p\sqrt\epsilon.}
\]

This equality is **not** a general assertion that Φ preserves distances
between arbitrary raw C states. It uses positivity and comparison with
the corresponding pure ideal ray. The inequality follows from
\(s^2+|z|^2\le s\le\epsilon\).

### Sharpness and nonuniqueness

For every ε in (0,1/2], a pure tilted target with quotient

\[
H_\theta=\begin{pmatrix}
1-\epsilon&e^{i\theta}\sqrt{\epsilon(1-\epsilon)}\\
e^{-i\theta}\sqrt{\epsilon(1-\epsilon)}&\epsilon
\end{pmatrix}
\]

and raw h=J2(Hθ) attains the distance bound for the calibrated branch
\(\widetilde B_Q=e_Qh\). Complete it with an ideal complementary branch.
This proves the constant and square-root dependence cannot be improved
uniformly, even on C0. Different θ and interior targets also establish
nonuniqueness for positive ε. Perfect repeatability is the limiting unique
case, on C0 and, by RI-08c, on C as well.

Separately on C, the normalized target with
\(A=\operatorname{diag}(1-\epsilon,\epsilon)/2\) and
\(c=e^{i\theta}\epsilon/2\) is positive and attains the raw-coordinate
bound. Its distance to J2(Q) is only 2ε. The pure tilted targets must have
c=0 because their A has rank one. Thus the two bounds are sharp separately
and cannot be simultaneously saturated for ε>0 in the stated range.
No nonzero-c output is permitted by the composite-consistent C0 range.

Exact witnesses include ε=9/25, with pure target diagonal entries 16/25,
9/25 and off-diagonal 12/25, giving raw distance 6/5; and ε=1/5 with the
diagonal maximal-c target c=1/10. These are conditional mathematical
instruments, not empirical calibrations or native availability claims.

## 4. Broader-C approximate branches need not descend through Φ

The C0 classification must not be transplanted to the larger C domain.
Here is a positive full-C counterexample, with Q=Z-positive,
ε=1/5, κ=2/5 and p=e_Q(d)=2A_in,00:

\[
\widetilde B_+(d)=D(A_{\mathrm{out}},0),\qquad
A_{\mathrm{out}}=
\begin{pmatrix}
p(1-\epsilon)/2&\kappa c_{\mathrm{in}}\\
\kappa\bar c_{\mathrm{in}}&p\epsilon/2
\end{pmatrix}.
\]

Use the ideal Z-negative branch as complement. This is real-linear on all
six input coordinates. Positivity of the input gives
\(|c_{\mathrm{in}}|\le A_{\mathrm{in},00}=p/2\), so

\[
\det A_{\mathrm{out}}
\ge\frac{p^2}{4}\bigl(\epsilon(1-\epsilon)-\kappa^2\bigr)=0.
\]

Both diagonal entries are nonnegative, hence the output is positive.
Its mass is p and its repeatability deficit is exactly εp. The complement
is positive and exact, so the instrument is mass-complete on the full C
cone. If p=0 the input bound forces c_in=0 and the whole output is zero.

For A_in=I/4 and c_in=±1/4, the two normalized sources have the same Φ,
but their normalized positive outputs have quotients

\[
\begin{pmatrix}4/5&\pm2/5\\\pm2/5&1/5\end{pmatrix}.
\]

A later ideal X-positive read gives conditional probabilities 9/10 and
1/10, or joint Z-positive/X-positive probabilities 9/20 and 1/20.
Approximate repeatability therefore does not preserve the old Φ equivalence,
even though this example outputs c=0. The nonzero-c **inputs** are not
allowed if RI-08d's additional composite premises are imposed. On C0,
Φ is injective, and restriction of this example is an ordinary fixed
diagonal reset rather than a non-descent counterexample.

## 5. Ideal-suffix contraction on the full signed span

This step avoids assuming complete positivity, signed trace-norm contraction
or quotient descent for approximate maps.

For any Hermitian signed X in V, pinching the untwisted raw matrix to its
two cell-diagonal blocks gives diag(A,A). Pinching is the average of unitary
conjugations by I and diag(I,−I), so the triangle inequality gives

\[
\|\Phi(X)\|_1=2\|A\|_1\le\|X\|_1.
\]

For a Pauli ideal instrument, \(\|J_2(Q_r)\|_1=1\) and

\[
\sum_r\|B_r(X)\|_1
=\sum_r|\operatorname{Tr}(\Phi(X)Q_r)|
\le\|\Phi(X)\|_1\le\|X\|_1.
\]

The middle inequality follows by pinching Φ(X) in that measurement basis.
The existing raw Clifford controls are unitary congruences and preserve
trace norm. A stopped leaf uses the identity map, also contractive.
Induction therefore makes every specified finite **ideal suffix** contractive
in the sum of trace norms over its fully labeled leaves. This works on
the four-dimensional C0 span and the full six-dimensional C span.

Only approximate **positive-prefix** states will be fed into the assumed
defect bound. No approximation map is asked to contract arbitrary signed
differences, and no absent approximate Φ-descent is used.

## 6. Finite serial, feedback and early-stop bounds

Fix one declared domain and the same full normalized initial state in
both models, including earlier records, controller, frame and pending
actual settings. A common controller chooses a finite Clifford word,
Pauli setting, or stopping action using only the known full history.
There are at most N recorded tests. Outcomes, settings, source type,
precursors and residuals remain explicit; impossible histories can be
represented by zero unnormalized kernels, never fabricated commitments.

Approximate and ideal branches model the **same declared nominal actions**.
Their model parameters (ε, chosen targets, analytical provenance) are not
different randomized outcome labels. If two implementations actually record
different apparatus identifiers or settings, those labels must be retained,
and this common-record-alphabet comparison does not identify them.

Let \(D_\ell^{\mathrm{approx}}\) and \(D_\ell^{\mathrm{ideal}}\) be the
unnormalized full raw residuals at the common labeled leaves. Then

\[
\boxed{\sum_\ell\|D_\ell^{\mathrm{approx}}-D_\ell^{\mathrm{ideal}}\|_1
\le\min(2,2N\sqrt\epsilon).}
\]

For the distributions of those full classical records,

\[
\boxed{\operatorname{TV}(P_{\mathrm{approx}},P_{\mathrm{ideal}})
\le\min(1,(N-1)\sqrt\epsilon),\qquad N\ge1.}
\]

For N=0 both errors are zero. At N=1 the recorded outcome laws agree
exactly, although post-outcome residuals can already differ maximally within
the one-step bound.

**Hybrid proof.** Let H_k use approximate updates for the first k recorded
tests and ideal updates afterward. Adjacent hybrids have a common positive
approximate prefix through depth k−1. At any active node h, local calibration
and the one-step bound give

\[
\sum_r\|\widetilde B_r d_h-B_r d_h\|_1
\le2\sqrt\epsilon\,m(d_h).
\]

Active prefix masses sum to at most one. The remaining ideal suffix
contracts the signed differences by §5, even with the common history-based
feedback and early-stop rules. Summing N replacements proves the residual
bound. The additional cap 2 follows from positivity and unit total leaf
mass in each protocol, since positive raw source residuals have trace norm
equal to m.

For records, \(|m(X)|=|\operatorname{Tr}X|\le\|X\|_1\), so each hybrid
contributes at most √ε to total variation. The replacement at depth N
contributes **zero**: its probabilities are exactly calibrated and there
can be no later recorded test. Earlier stopped leaves also incur no later
change. Removing that replacement yields N−1 rather than N. This argument
requires stopping/feedback to depend on the common full record, not on a
hidden residual, approximation model label or undeclared diagnostic. ∎

These are valid finite-horizon bounds, not optimal general horizon rates.
They retain full raw residuals and do not substitute a record-only quotient.
They do not cover undeclared c-sensitive terminal tests, approximate ancillary
diamond norms, arbitrary observation catalogues or unbounded stopping times.

### A sharper bound for this Clifford/Pauli record catalogue

Set \(\delta=\sqrt{\epsilon(1-\epsilon)}\). For N≥1,

\[
\operatorname{TV}(P_{\mathrm{approx}},P_{\mathrm{ideal}})
\le1-(1-\delta)^{N-1}.
\]

After a matched record, the ideal conditional state is its Pauli projector;
the approximate conditional state has deficit s≤ε relative to that same
projector. Common Clifford controls preserve this relation and map a Pauli
projector to another Pauli projector. For the next parallel/opposite-axis
read the binary probability discrepancy is s≤ε≤δ. For a transverse Pauli
read it is at most \(|z|\le\sqrt{s(1-s)}\le\delta\).
The first record is exact by calibration. Sequential maximal coupling
therefore keeps the entire recorded histories matched with probability at
least \((1-\delta)^{N-1}\); matched early stops incur no further risk.
The defect bound is re-established on each actual approximate branch, so
the broader-C non-descent example does not invalidate the argument.

For two records the transverse bound δ is attained by first reading Q on
the initial J2(Q), using its pure tilted approximate output, then making
the corresponding transverse Pauli read. This does not assert optimality
of the displayed rate for arbitrary larger horizons. At ε=9/25, δ=12/25
is exact and rational.

## 7. Executable and record contract

[model.py](model.py) declares the domain on both states and instruments.
Composite-consistent states reject c≠0. Fixed-target instruments validate
normalized positive outputs in the declared domain and the exact deficit;
the classified formula certifies their uniform bound. The separately labeled
local-only counterinstrument is the §4 full-C family, not a composite
instrument accepting prohibited inputs.

Controls act once on the current full raw residual in the fixed frame.
A positive commitment records the same nominal setting, Pauli axis,
outcome, controller/frame/domain, actual pending control word and entire
earlier prefix as precursor, then clears only the pending word. Earlier
records remain unchanged. No zero branch is normalized or appended.
Changing a known nominal setting is retained, not silently equated across
protocols. Source and record constructors validate finite grammar/domain,
not global physical preparation reachability.

The exact witnesses in [check.py](check.py) retain all record-bearing
branches and compare like-labeled leaves. Their rational inputs and analytic
trace-norm calculations are not a finite-test certification of the uniform
premise. That premise is either proved for a stated mathematical family or
explicitly assumed for the general theorem. Nothing here turns empirical
calibration data into a uniform guarantee.

## 8. Completion and scope

The result reconciles the domains rather than combining incompatible claims:
C0 has a full calibrated-branch classification and injective Φ; C has sharp
one-step bounds but can lose Φ-descent under approximate updates. Both
support the stated finite protocol bounds under their explicitly matched
domain, calibration and uniform-defect premises.

No native controls, new ancillary/composite closure, complex-field selection,
full physical preparation access, full QM, quantum advantage, infinite-history
law, empirical calibration, geometry or physical promotion is established.
The allowed yields are the conditional classification, quantitative theorems
and counterexamples. The QR owner stops for independent acceptance; no next
obligation is designed here. Accepted sources, RET, coordinator-owned
application/registry work, QR-05 atlas, clocks/book and κ-gravity remain
untouched. Option B and Status M are unchanged.

```sh
.venv/bin/python -B docs/validation/t8-q-repeatability-robustness-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-repeatability-robustness-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-repeatability-robustness-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-repeatability-robustness-2026-09-13
```

Final hashes, source review and replay appear in the
[handoff](../../coordination/QR_HANDOFF.md). The work is not an external
peer review, proof-assistant certificate or empirical validation.
