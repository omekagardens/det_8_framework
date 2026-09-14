# RI-08f — same-image joint repeatability and question granularity

13 September 2026. **CONDITIONAL_SAME_IMAGE_REPEATABILITY_OBSTRUCTION;
SHARP_QUESTION_RELATIVE_TRADEOFF.** Internal mathematics for the fixed
reference/coupler image of RI-08d, not a composite-theory reconstruction.
Reusable algebraic return operations, where illustrated, are explicitly
additional premises. They are not literal terminal cuts reused as sources.

## 1. Fixed image and full raw payload

The accepted
[RI-08d interface](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)
supplies the local section and independently declared reference

\[
D(A,0)=\begin{pmatrix}A&0\\0&ZAZ\end{pmatrix},\quad
A=\rho^T/2,\quad B_t=(I+tZ)/4,\quad R_t=D(B_t,0),
\quad -1\le t\le1 .
\]

Here \(\rho\) is any positive Hermitian 2-by-2 matrix, not necessarily
normalized. The mathematical cone contains all such matrices; availability
of every preparation is not derived. Fix t, its known Z orientation,
the declared independent composition and the one shared coupler
\(U=(I\otimes H)\mathrm{CNOT}\), applied from right to left.
Varying t means a different fixed-image problem, not an allowed unrecorded
reference change within one protocol.

Retain every native label \((a,i,b,j)\), with \(q=8a+4i+2b+j\).
The joint cells are \((a,b)\), each containing all four choices of i,j.
The accepted signed permutation into untwisted grouped order is
\[
T_{8a+4b+2i+j,\;8a+4i+2b+j}=(-1)^{ai+bj}.
\]

Define the native sixteen-label real-linear image
\[
\mathcal J_t(\rho)
=T^\dagger\operatorname{diag}(M_t,M_t,M_t,M_t)T,\qquad
M_t=U\bigl((\rho^T/2)\otimes B_t\bigr)U^\dagger,
\]
\[
\boxed{K_t=\{\mathcal J_t(\rho):\rho\succeq0\}.}
\]

This is the coupled c=0 family with fixed reference and coupler.
At t=0 it is a **chosen section image**: RI-08d did not exclude nonzero c
using an unpolarized reference, and no such exclusion is inferred here.

The after-the-fact joint quotient convention is
\[
\sigma_t=4M_t^T
=\bar U(\rho\otimes\rho_t)U^T,\qquad \rho_t=(I+tZ)/2 .
\]
The conjugation/transpose is retained even though this particular U is real.
For complex \(\rho\), replacing \(\rho^T\) by \(\rho\) in the native
construction changes the raw kernel.

The map \(\mathcal J_t\) is a positive real-linear isomorphism between PSD2
and \(K_t\), with four-dimensional Hermitian span. Its inverse is
\[
\rho=4\left[\operatorname{Tr}_{\mathrm{ref}}
  (U^\dagger M_tU)\right]^T .
\]
Indeed the partial trace before the final transpose is
\((\rho^T/2)\operatorname{Tr}B_t=\rho^T/4\).
This works also at t=±1 where the reference has rank one. A positive
native image kernel has positive partial trace; the converse follows
from its construction. Membership requires reconstruction of **the whole
sixteen-label kernel**, including every block. Merely computing a partial
trace does not establish membership.

On this span, total-entry mass, ordinary raw trace and local trace agree:
\[
m(N)=\mathbf1^\dagger N\mathbf1
=\operatorname{Tr}N=\operatorname{Tr}\rho .
\]
The cell read vectors \(v_{ab}=(Z^ae)\otimes(Z^be)\), \(e=(1,1)^T\),
satisfy \(\sum_{ab}v_{ab}v_{ab}^\dagger=4I\), proving the mass identity.
Mass is faithful on \(K_t\). It is normalization mass, not rest mass;
these trace identities do not hold on arbitrary raw kernels.

## 2. Pullback of all four complete cell effects

The native effect is the full cell form
\[
q_{ab}(N)=v_{ab}^\dagger M_tv_{ab}
=\operatorname{Tr}(\rho E_{ab}),\qquad
\boxed{E_{ab}=\frac{I+(-1)^btZ}{4}.}
\]
All off-cell forms vanish on \(K_t\). These effects are independent of a;
this does not erase a from a committed record.

**Derivation.** Normalize the read vector as \(w_{ab}=v_{ab}/2\). Then
\[
U^\dagger w_{ab}
=\frac{|0,b\rangle+(-1)^a|1,1\mathbin{\oplus}b\rangle}{\sqrt2}.
\]
The fixed diagonal reference eliminates the cross term in its expectation
against \(\rho^T\otimes\rho_t\). The remaining diagonal entries give
\((\rho_{00}+\rho_{11}+(-1)^bt(\rho_{00}-\rho_{11}))/4\), proving the
identity on the entire signed Hermitian span, not only sampled states.
In A coordinates this is
\[
q_{ab}=\frac{m+(-1)^bt\,z_{\mathrm{un}}}{4},\qquad
z_{\mathrm{un}}=2(A_{00}-A_{11}).
\]
Both real coherence directions remain in the raw image but these immediate
effects do not see them. Completeness is \(\sum_{ab}E_{ab}=I\).
The largest normalized full-cell weight is
\[
p_{\mathrm f}=\max_{N\in K_t,\;m(N)=1}q_{ab}(N)
=\frac{1+|t|}{4}\le\frac12 .
\]
For t≠0 the maximizing normalized state is uniquely
\(h_b=\mathcal J_t(Q_b(t))\), where \(Q_b(t)\) is the local Z eigenprojector
with sign \((-1)^b\operatorname{sign}(t)\).
At t=0 every normalized image state attains the value 1/4.

## 3. General effect bound and exposed repeat face

Let K be a cone with faithful positive mass m. Let e and g be nonzero effects with
\(0\le e,g\le m\); let their normalized maxima \(\alpha,\beta>0\) be
attained. A branch B is real-linear on the actual span, positive K→K,
and mass-calibrated to the **first-branch** effect:
\[
m(Bx)=e(x).
\]
The **next-question** effect is g, which may or may not equal e. Then
\[
g(Bx)\le\beta m(Bx)=\beta e(x),\qquad
\boxed{(m-g)(Bx)\ge(1-\beta)e(x).}
\]
Therefore the minimum possible uniform relative bound
\((m-g)(Bx)\le\epsilon e(x)\) is \(1-\beta\).
For a normalized maximizing target h, the algebraic branch
\(B(x)=e(x)h\) is positive and calibrated and attains equality everywhere.
Its availability as an actual operation is an additional premise.

Every relatively optimal branch has its nonzero positive output range in
the face \(g=\beta m\). If that face is a ray, calibration determines the
branch uniquely on the cone and hence on its span. If it has higher
dimension, uniqueness need not follow. Perfect repeatability requires
\(\beta=1\) and output in the exposed repeat face \(g=m\).
The nonzero-effect conditions avoid the vacuous zero branch; attainment
ensures an algebraic target exists.

Using **original input mass** instead gives a different optimum:
\[
\inf_B\sup_{m(x)=1}(m-g)(Bx)=\alpha(1-\beta).
\]
The pointwise lower bound on an input attaining e=α proves necessity;
the reset branch proves sufficiency. This minimax criterion does not
generally force all outputs into the maximizing face. For e=g it reduces
to \(p_*(1-p_*)\), not the relative coefficient \(1-p_*\).

## 4. Same-image full-outcome obstruction and sharp completion

Apply the lemma to \(e=g=q_{ab}\) on K_t. Branches must be positive on
the whole fixed cone, calibrated to the actual full effect and return
**to the same K_t**. Then
\[
\boxed{\epsilon_{\mathrm f}^{\min}
=1-p_{\mathrm f}=\frac{3-|t|}{4}\ge\frac12.}
\]
No such branch can perfectly repeat full (a,b), even with maximal reference
polarization. This is an empty-repeat-face obstruction, not an unsuccessful
search for a Kraus representation. No ancillary or complete-positivity
premise was used.

For t≠0 use the h_b above; at t=0 choose
\(h_b=\mathcal J_0(I/2)\) for definiteness. The algebraic instrument
\[
\boxed{B_{ab}(N)=q_{ab}(N)h_b}
\]
attains all four optima simultaneously. Its branches are positive and
same-image, with masses summing to m. The targets for a=0 and a=1
coincide at fixed b, but their actual records do not. Zero effect gives
the **entire zero output**, never normalized or appended as a record.

For t≠0 the maximizing face is one ray, so these are the unique relatively
optimal branches on the full image span. This is uniqueness given the
optimum, not a claim that calibration alone forces a reset.
At t=0, \(q_{ab}=m/4\), and every positive calibrated branch has relative
defect 3/4. For example \(B_{ab}(N)=N/4\) is a complete calibrated
instrument, not a reset to a fixed target. No t=0 uniqueness is asserted.

For a fine branch with input-mass normalization, the sharp coefficient is
\[
\eta_{\mathrm f}^{\min}
=p_{\mathrm f}(1-p_{\mathrm f})
=\frac{(1+|t|)(3-|t|)}{16}.
\]
Do not transfer relative-optimum uniqueness to this alternative objective.
For \(0<|t|<1\), let \(Q_+\) maximize the selected full effect, \(Q_-\)
be its opposite, and \(\lambda_\pm=(1\pm|t|)/4\). On local matrices,
\[
L(\rho)=\lambda_+\rho_{++}Q_+
       +\lambda_-\rho_{--}Q_-
\]
is positive and calibrated and returns to the image through \(\mathcal J_t\).
Its worst input-mass defect is \(\lambda_+(1-\lambda_+)\), because both
eigenvalues are at most 1/2 and \(x(1-x)\) increases in that range.
Yet its relative defect on \(Q_-\) is the worse value \(1-\lambda_-\).
Thus it is a non-reset optimizer for the alternative normalization.

The reusable reset branches are **extra operation/preparation premises**,
not consequences of the accepted literal joint cuts. They act directly on
K_t; their image condition fixes the same reference parameter. This is
not a physical derivation of resetting a reference or reapplying the
original coupler after each commitment.

## 5. Coarser next question without deleting a record

Ask whether the next full record has the same b, allowing either next a:
\[
q_b=\sum_aq_{ab},\qquad E_b=\frac{I+(-1)^btZ}{2},\qquad
p_{\mathrm b}=\frac{1+|t|}{2}=2p_{\mathrm f}.
\]
After an actual first record (a,b), its branch mass is still \(q_{ab}(N)\).
The lemma with e=q_ab and g=q_b gives
\[
(m-q_b)(B_{ab}N)\ge(1-p_{\mathrm b})q_{ab}(N),\qquad
\boxed{\epsilon_{\mathrm b}^{\min}=\frac{1-|t|}{2}.}
\]
The same optimal h_b targets attain this bound and the fine bound at once.
At \(|t|=1\), b can repeat perfectly although full (a,b) cannot:
the next full outcomes (0,b) and (1,b) each have probability 1/2.
The earlier a remains in its earlier record. At t=0 the next b is fair,
with relative failure probability 1/2 under every calibrated branch.

| Fixed polarization | Maximum full-outcome success | Minimum full relative defect | Maximum same-b success | Minimum b relative defect |
| --- | --- | --- | --- | --- |
| t=0 | 1/4 | 3/4 | 1/2 | 1/2 |
| \(|t|=1/2\) | 3/8 | 5/8 | 3/4 | 1/4 |
| \(|t|=1\) | 1/2 | 1/2 | 1 | 0 |

These are fresh applications of the declared effects to the output.
Re-reading stored classical memory would return the stored label and is
a different operation, not the repeatability problem posed here.

There are two distinct input-mass coefficients for the b question:

1. After a particular actual fine branch, the optimum is
   \(p_{\mathrm f}(1-p_{\mathrm b})=(1-t^2)/8\).
2. For the analytically summed first-b branch \(B_b=\sum_aB_{ab}\), it is
   \(p_{\mathrm b}(1-p_{\mathrm b})=(1-t^2)/4\).

The second expression sums separately labeled histories. It does not
discard a, average away known records or replace actual fine commitments
by coarse commitments. The relative coefficient is the same in both
cases because their respective denominators are q_ab and q_b.
Confusing those denominators changes the question.

## 6. What this question change does not authorize

All outcomes including a remain distinct labels in the declared record
model even when a statistic uses only b. Evaluating that statistic does
not mutate a previous record or residual, or supply a different reference,
partition, apparatus context or enlarged return cone.

A nonzero literal full-cell cut of a K_t source is **not** back in K_t.
In the untwisted frame the image has four identical diagonal blocks.
A cut retains only one, so equality to an image kernel would force all
four to be zero. The accepted RI-08d terminal cut cannot therefore be
silently reused by this instrument. A zero-weight cell cut may even be
nonzero; it still cannot be normalized or committed. This differs from
the same-image algebraic branch, whose zero effect forces zero raw output.

The local [RI-08e bounds](../t8-q-repeatability-robustness-2026-09-13/ROBUSTNESS.md)
were for their stated local Pauli effects and source cones. They do not
automatically extend to this fixed joint image. Here the minimum full
relative defect is at least 1/2 and is strictly larger at interior
polarization, outside RI-08e's epsilon≤1/2 range. The repeated question,
source/range cone and normalization must be fixed before comparing bounds.
This is an interface obstruction, not a failure of quantum theory.

## 7. Executable contract and validation

[model.py](model.py) supplies exact Gaussian-rational native kernels and
the separately declared same-image algebraic instrument. Membership
reproduces the full raw kernel after inversion. Positivity and calibration
concern the whole chosen cone, not only sampled preparations.

The record-bearing fixture retains the fixed image/context, reference
polarization and orientation, independent input origins and their complete
initial histories, actual coupler/frame and return-instrument setting,
every full outcome (a,b), and complete origin-tagged precursors. Positive
updates return to the same image and append a fresh full record.
Impossible branches are not normalized or appended. Fine and b questions
analyze the next full-record distribution; neither rewrites a record.
Snapshot validation checks exact image/grammar consistency, not physical
independence or global preparation reachability.

[check.py](check.py) uses independent exact arithmetic, native indices
and full-span certificates, including t=0, both polarized endpoints,
interior signs, complex inputs, and zero/unnormalized cases. Finite
witnesses supplement the universal proofs, rather than replacing them
with a sampled-state or bounded-depth conclusion.

## 8. Bounded completion

The candidate obstruction and question-granularity tradeoff are proved
under the stated same-image, positivity and exact-calibration premises.
The algebraic reset family establishes attainability with its availability
premises separated. No DET-native selection of that family, complete
composite state space, new context, physical reset law, arbitrary ancillary
closure, full QM, geometry, mass or gravity derivation is established.
Option B and Status M remain unchanged.

Only this new bundle, the reserved QR map/plan files and the handoff are
in scope. Accepted bundles and coordinator-owned operational-premise,
application and registry work remain unchanged. No successor is designed
or started. The QR owner stops at a source-stable handoff for independent
acceptance.

~~~sh
.venv/bin/python -B docs/validation/t8-q-joint-repeatability-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-joint-repeatability-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-joint-repeatability-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-joint-repeatability-2026-09-13
~~~

Source pins, internal review and replay appear in the
[handoff](../../coordination/QR_HANDOFF.md). No external peer review,
proof-assistant certification or empirical verification is claimed.
