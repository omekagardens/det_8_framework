# RI-23 — scalar values, compatibility and deterministic positivity certificates

14 September 2026 UTC. Coordinator proof/design companion to
[RI-20's probe criterion](QR_COMPOSITION_PREMISE_PLAN.md),
[RI-21's finite-copy theorem](QR_FINITE_COPY_WITNESS_PLAN.md) and the
[application plan](APPLICATION_WORK_PLAN.md). **Independently accepted conditional proof/design;
no acquisition interface or executor is implemented.**

**Purpose.** Finitely many fixed tests can determine a Hermitian kernel from
their actual scalar values even when positivity of those values alone does
not force the kernel to be PSD. This note gives an explicit inverse, a
proved deterministic error radius, and sufficient certificates for all
compatible kernels. It also identifies why these tests cannot simply be
called fixed outcome probabilities on the unrestricted raw PSD domain.

The forward map, consistently supplied source/frame, calibration and error
bounds are explicit premises. No measured dataset, sampling-confidence law,
new preparation, physical tensor rule, RET integration or scientific novelty
is supplied. This is a mathematical inference contract and a specification
for what a future acquisition interface would need to justify.

## 1. A fixed scalar catalogue and its exact inverse

Fix n>=1 and a labeled complex Hermitian matrix D. For i<j define

\[
v_i=e_i,\qquad v^R_{ij}=e_i+e_j,\qquad
v^I_{ij}=e_i-i e_j,\qquad T_v=vv^\dagger.
\tag{1}
\]

Each T_v is PSD. There are n+2 binomial(n,2)=n² tests. Their scalar law is
**assumed to be** L_v(D)=Tr(DT_v)=v†Dv. These are real scalar values, not
necessarily probabilities or one common outcome partition. Direct expansion
of D_ij=a_ij+i b_ij gives

\[
q_i=D_{ii},\quad q^R_{ij}=D_{ii}+D_{jj}+2a_{ij},\quad
q^I_{ij}=D_{ii}+D_{jj}+2b_{ij}.
\tag{2}
\]

The minus sign in v^I is responsible for the plus sign before b_ij. The
unique Hermitian inverse is

\[
D_{ii}=q_i,\qquad
D_{ij}=\frac{q^R_{ij}-q_i-q_j}{2}
+i\frac{q^I_{ij}-q_i-q_j}{2},\qquad D_{ji}=\overline{D_{ij}}.
\tag{3}
\]

Thus the catalogue determines every Hermitian entry. This is the elementary
polarization identity in coordinates, not a new tomography theorem. Known
normalization adds a relation, so n² is a convenient full-Hermitian catalogue,
not a claimed minimal count for normalized inputs.

Under the expressly supplied ordinary event-pair tensor law, RI-20's helper
realizes each test algebraically: use ancillary amplitudes
b=(conj(v_1),...,conj(v_n),1−sum conj(v_i)), B=bb†, and the diagonal joint
event excluding the final ancillary coordinate. Then total-entry mass of B
is one and the joint-event weight is v†Dv. The finite vectors in (1) give
fixed probes independent of D. This construction establishes no preparation,
sharp operation or readout availability.[^1]

The inverse requires the **specified value law**. If the actual forward map
were L(Re D), every reported value would ignore Im D and (3) would return
Re D instead. Scalar independence or correct subsystem marginals alone
cannot be substituted for calibration of L. The separate RI-22 assignment
in the [implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md) studies
that composition-premise issue; this contract does not adopt another law.

## 2. Signs and values answer different questions

RI-20 characterizes inference from nonnegativity constraints on a fixed
probe family. Here actual values determine D, after which PSD can be checked
nonlinearly. No step concludes PSD merely because the finite menu values
are nonnegative. Nor does a mathematical negative direction automatically
become an available new ancillary test.[^1]

For example, consider

\[
D_*=
\begin{pmatrix}
1/10&3i/20&0\\-3i/20&1/10&0\\0&0&4/5
\end{pmatrix}.
\tag{4}
\]

Its total-entry mass is one. Every Boolean event weight is the sum of its
selected diagonal entries, so it is weakly positive. Its eigenvalues are
1/4,−1/20,4/5. The catalogue values are

| Values | In index order |
|---|---|
| Diagonal | 1/10, 1/10, 4/5 |
| Real-pair, (12),(13),(23) | 1/5, 9/10, 9/10 |
| Imaginary-pair, (12),(13),(23) | 1/2, 9/10, 9/10 |

Every displayed value lies between zero and one, yet (3) reconstructs a
non-PSD matrix. Re D_* is PSD and also passes every sign test, but its
imaginary-pair value for (12) is 1/5. The values distinguish the two;
their signs do not. A particular list lying in [0,1] does not prove a valid
probability interpretation on an entire source domain.

## 3. Bounded errors and the compatibility set

Inputs are a fixed catalog/frame identity, finite real estimates y_i,
y^R_ij,y^I_ij and finite nonnegative absolute error bounds eta_i, eta^R_ij,
eta^I_ij. Matching source, settings, units and calibration are prerequisites
of the forward-map contract. Negative estimates alone are not malformed;
measurement or estimation error can cross zero. Unsupported catalogues,
missing/mismatched metadata and invalid numerical bounds are input failures.

Let Dhat be the Hermitian inverse (3) applied to y. It is a linear estimate;
it is not automatically normalized, weakly positive, PSD or physically
prepared. Define the compatibility set

\[
\begin{split}
\mathcal C(y,\eta)=\{D=D^\dagger:\;&M(D)=\mathbf1^\dagger D\mathbf1=1,\\
&\chi_A^\dagger D\chi_A\ge0\quad(A\subseteq\Omega),\\
&|L_v(D)-y_v|\le\eta_v\quad\text{for every test in (1)}\}.
\end{split}
\tag{5}
\]

PSD is deliberately not an input constraint. All conditions in (5) are
linear equalities/inequalities in real Hermitian coordinates. Since the
catalogue is invertible and the intervals are finite, C is a bounded closed
polytope, possibly empty. This does not supply an efficient feasibility
solver; the Boolean inequalities themselves can be numerous.

A feasible witness must satisfy **every** condition in (5). It is a compatible
mathematical kernel, not evidence of an actual preparation. A failed witness
proves only that this witness failed. Without either a verified feasible
kernel or an emptiness proof, feasibility remains unresolved.

### Reconstruction radius

For any D∈C, the diagonal error is at most eta_i. Formula (3) bounds each
real and imaginary off-diagonal error by

\[
\alpha_{ij}=\frac{\eta^R_{ij}+\eta_i+\eta_j}{2},\qquad
\beta_{ij}=\frac{\eta^I_{ij}+\eta_i+\eta_j}{2}.
\]

Set

\[
r^2=\sum_i\eta_i^2+
\frac12\sum_{i<j}\left[
(\eta^R_{ij}+\eta_i+\eta_j)^2+
(\eta^I_{ij}+\eta_i+\eta_j)^2\right].
\tag{6}
\]

Counting both Hermitian off-diagonal entries proves

\[
\|D-\widehat D\|_{op}\le\|D-\widehat D\|_F\le r,
\qquad
|v^\dagger(D-\widehat D)v|\le r\|v\|^2.
\tag{7}
\]

Indeed the squared Frobenius norm is the sum of squared diagonal errors
plus twice the squared real and imaginary off-diagonal errors. Substitution
of alpha and beta gives (6); the quadratic-form bound follows by the
operator norm and Cauchy–Schwarz. Shared errors and extra constraints can
make this radius conservative. No sharpness or statistical coverage is claimed.

### Normalization is checked, not repaired

The exact inverse gives

\[
M(\widehat D)=\sum_{i<j}y^R_{ij}+(2-n)\sum_i y_i.
\tag{8}
\]

Consequently nonempty compatibility requires

\[
|M(\widehat D)-1|\le
\sum_{i<j}\eta^R_{ij}+|2-n|\sum_i\eta_i.
\tag{9}
\]

Violation is a verified emptiness certificate. Satisfaction is only a
necessary check; weak positivity or other intervals can still conflict.
Do not rescale Dhat to force mass one, clip its eigenvalues, or replace it
by an unverified feasible fit: those actions change the stated inverse or
data contract. An alternative constrained estimator would need its own bound.

## 4. Sound decisions require feasibility first

After verifying C is nonempty, either of the following is a sufficient
universal certificate:

\[
\widehat D-rI\succeq0
\quad\Longrightarrow\quad D\succeq0\quad(D\in\mathcal C),
\tag{10}
\]

\[
v\ne0,\quad v^\dagger\widehat Dv+r\|v\|^2<0
\quad\Longrightarrow\quad D\not\succeq0\quad(D\in\mathcal C).
\tag{11}
\]

Both follow immediately from (7). The negative-direction inequality is
strict; equality does not certify a negative value. If either conclusion
is used, its matrix/vector inequality must itself be verified exactly or
with rigorous numerical bounds. An unchecked floating-point eigensolver
output or rounded radius is not a certificate.

| Decision | Evidence required and meaning |
|---|---|
| Invalid input | The declared catalogue/data/bounds contract is malformed or unsupported. Rejection of an optional witness alone does not invalidate the input data. |
| Proven infeasible | A verified contradiction in (5), for example a violation of (9), proves there is no compatible kernel under the combined assumptions. This gives no positivity verdict about a real source. |
| Feasibility unresolved | Inputs are valid, but neither nonemptiness nor emptiness is verified. Failure of a solver or one candidate is insufficient. |
| All compatible kernels PSD | Verified nonemptiness and (10), or another independently established sufficient universal certificate. One PSD witness alone establishes only a PSD explanation exists. |
| All compatible kernels non-PSD | Verified nonemptiness and (11), or another independently established sufficient universal certificate. One non-PSD witness alone establishes only a non-PSD explanation exists. |
| Nonempty, inconclusive | A feasible witness exists, but neither universal conclusion is certified. Two compatible kernels with opposite PSD status establish actual ambiguity. |

These are proposed report semantics, not a new callable API. Feasibility and
positivity should remain separate report coordinates. Universal claims over
an empty set must not be presented as physical findings. A negative bound
in an indicator direction can instead contradict the weak-positivity premise
itself; verified nonempty feasibility prevents that misclassification.

At zero errors, feasibility makes C the singleton {Dhat}; an exact PSD or
negative-direction check then classifies it. For n=1, normalization fixes
D=[1], and feasibility is exactly |y_1−1|<=eta_1. That sole compatible
matrix is PSD; the generic radius test can be unnecessarily conservative.
No implication from a deterministic eta to a sampling-confidence level is made.

## 5. Exact interval examples

For n=2 use

\[
D_t=\begin{pmatrix}1/2&it\\-it&1/2\end{pmatrix},\qquad t\in\mathbb R.
\tag{12}
\]

Every D_t has mass one and Boolean weights 0,1/2,1/2,1. It is PSD precisely
when |t|<=1/2. Its catalogue is (1/2,1/2,1,1+2t). Fix the first three
values exactly and vary only the imaginary-pair interval:

| Imaginary-pair observation | Complete compatible t interval | Result |
|---|---|---|
| 2 ± 1/2 | [1/4,3/4] | D_(1/4) is PSD and D_(3/4) is non-PSD: verified ambiguity. Neither radius certificate resolves it. |
| 5/2 ± 1/4 | [5/8,7/8] | All are non-PSD. D_(3/4) is a feasible witness and (11) certifies the uniform conclusion. |
| 1 ± 1/4 | [−1/8,1/8] | All are PSD. D_0 is feasible and (10) certifies the uniform conclusion. |
| Any imaginary value, but exact real-pair observation 2 | Empty | In n=2 the real-pair value is total-entry mass; exact 2 contradicts normalization one. |

In the two certified rows r=1/(4 sqrt(2)). For the non-PSD row choose
v=(1,i): its squared norm is two and v†Dhat v=−1/2, giving
−1/2+1/(2 sqrt(2))<0. For the PSD row Dhat=I/2 and r<1/2. The ambiguity
row has r=1/(2 sqrt(2)); both displayed compatible witnesses meet every
interval and weak-positivity constraint. These checks use exact algebra,
not a fit, simulated sampling run or empirical calibration.

## 6. The operational obstruction must travel with the inverse

The raw total-entry-normalized PSD domain does not automatically support
the tests in (1) as fixed bounded outcome probabilities. Write J0=11†.
If a fixed PSD test T obeys

\[
0\le\operatorname{Tr}(DT)\le M(D)=\operatorname{Tr}(DJ_0)
\quad\text{for every PSD }D,
\tag{13}
\]

then quadratic rank-one tests imply 0<=T<=J0. For x orthogonal to 1,
0<=x†Tx<=x†J0x=0. PSD therefore gives Tx=0, so T has range in span{1}
and T=aJ0 for some 0<=a<=1. Its value is only aM(D). Hence n>=2
informationally complete tests cannot all satisfy (13).

The same conclusion follows if the bounds are required only for every
normalized PSD D: homogeneity covers positive-mass inputs, and adding a
small positive-mass PSD matrix followed by a limit covers zero-mass inputs.
This is the bounded-effect form of the already accepted full-domain
obstruction, not a new measurement mechanism.[^2]

A future acquisition design must consequently justify a restricted source
domain, a different normalization/encoding, or a different declared scalar
acquisition model. Merely naming the y values “measurements” does not do so.
The RI-08i three-setting inverse concerns a supplied restricted L_t source;
RI-18's ideal initial-source law has rank two. Neither supplies (1) on an
unrestricted initial kernel, and a later read cannot recover information
removed by an earlier branch.[^3]

The useful output here is a precise data/refusal and error contract: it says
what values, bounds and compatibility evidence would support a conclusion,
and which acquisition premise remains missing. It is not measured benefit,
a realizable all-domain instrument, a PSD-domain selection theorem, or a
license to import imaginary-coordinate values from a model audit as data.
The existing application requirements for an instrument/dataset, target and
tolerance, calibration/noise law, cost, baseline and held-out evaluation remain.

## Sources and review boundary

[^1]: [RI-20 composition-premise audit](QR_COMPOSITION_PREMISE_PLAN.md),
    sections 4–6: fixed linear-test adequacy, normalized ancillary helper,
    countermodels and explicit resource/composition assumptions. The fixed
    coordinate inverse and deterministic bounds above are proved directly.

[^2]: [Accepted full-domain operation obstruction](../validation/t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md)
    and [operational premise ledger](OPERATIONAL_PREMISE_LEDGER.md), sections
    2–3. The scalar rank-one-range argument above is included in full.

[^3]: [Connected proof synthesis](../research/PROOF_SYNTHESIS_AND_PREMISE_SELECTION.md),
    section 2, and [RI-18 complete finite protocol](../validation/t8-q-finite-protocol-composition-2026-09-14/PROTOCOL_COMPOSITION.md).
    These are accepted conditional source/rank boundaries, not measurements.

The contract is coordinator-owned and independent of the RI-22 QR files.
Three independent complete mathematical, source and application reviews passed.
Coordinator exact arithmetic also verified the displayed catalogue, interval
witnesses and sufficient-certificate examples. These are supplementary checks,
not a new registered suite. No accepted executable, pinned historical result, registry count,
original review or application corollary is changed by this note.
