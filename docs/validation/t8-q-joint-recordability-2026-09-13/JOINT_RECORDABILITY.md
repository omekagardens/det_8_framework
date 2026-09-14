# RI-08d — polarized-reference joint recordability

13 September 2026. **CONDITIONAL_LOCAL_SUBCONE_SELECTION;
FULL_PAYLOAD_JOINT_RECORDABILITY_OBSTRUCTION.** Internal mathematical
classification for one explicitly supplied composite interface, not a
globally selected composite theory or a DET-derived entangler.

## 1. Question and declared interface

The accepted [RI-08b local cone](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md)
retains a locally invisible complex raw parameter:

\[
D(A,c)=\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix},\quad
A\succeq |c|I,\quad Z=\operatorname{diag}(1,-1),\quad
m(D)=2\operatorname{Tr}A.
\]

Its full real span is six-dimensional. The normalized slice has m=1;
\(\Phi(D)=2A^T\) is the previously proved catalogue-relative qubit
quotient. c is **not** discarded at input and is not a universal gauge.

Supply a separately prepared section reference

\[
B_t=\frac{I+tZ}{4},\qquad R_t=D(B_t,0),\qquad -1\le t\le1.
\]

Here t is real, known reference polarization in the declared Z orientation;
\(\operatorname{Tr}B_t=1/2\) and m(R_t)=1. The initial case t=1 is the
Z-positive section preparation, conditionally available under
[RI-08c's reusable Pauli instrument](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md).
Intermediate t requires the appropriate explicitly declared preparation or
mixture. RI-08c does not prove physical preparation availability from DET.

The following are **additional composite-interface premises**:

1. The two inputs have explicitly independent preparations. Their separate
   labeled record histories and known apparatus/reference settings remain
   intact. Distinct origin labels do not themselves establish independence.
2. Their raw composite is the tensor product \(N=D(A,c)\otimes R_t\), with
   the label permutation and readout partition specified below. This
   composition rule is supplied, not derived from bare record growth.
3. A single shared-system lift of
   \(U=(I\otimes H)\mathrm{CNOT}\), first system controlling the second,
   is available in the explicitly untwisted frame. CNOT acts first and H
   acts on its target second. Availability and the lift are supplied.
4. After this operation the same declared four-cell joint partition must
   remain **exactly** recordable: every complex cross-cell form vanishes.
   It is not sufficient that their real parts, their sum, or total mass
   vanish or normalize correctly.

These premises test viability of the whole proposed local input cone at a
fixed composite interface. They do not assume an allowed global composite
state space, arbitrary ancillas, arbitrary controls or native entangling
dynamics. The conclusion is conditional on them.

## 2. All sixteen native labels, permutation and untwisting

Write a local label as (a,i) and a reference label as (b,j), each coordinate
in {0,1}. The cell labels are a,b; i,j label the two members of each local
cell. The original tensor order and regrouped joint order are respectively

\[
q(a,i,b,j)=8a+4i+2b+j,\qquad
p(a,b,i,j)=8a+4b+2i+j.
\]

Thus the native four-cell partition, with no label omitted, is

| Joint cell (a,b) | Native tensor indices |
| --- | --- |
| (0,0) | 0,1,4,5 |
| (0,1) | 2,3,6,7 |
| (1,0) | 8,9,12,13 |
| (1,1) | 10,11,14,15 |

The local untwist is \(V=\operatorname{diag}(I,Z)\), so

\[
VD(A,c)V^\dagger=
\begin{pmatrix}A&cI\\\bar cI&A\end{pmatrix}=\widetilde D,
\qquad VR_tV^\dagger=\operatorname{diag}(B_t,B_t).
\]

Let Π perform the q-to-p permutation and set \(T=\Pi(V\otimes V)\).
Explicitly,

\[
T_{p(a,b,i,j),q(a,i,b,j)}=(-1)^{ai+bj},
\qquad T^\dagger T=TT^\dagger=I_{16}.
\]

This is a real signed permutation, not a projection. The full untwisted
kernel \(\widetilde N=TNT^\dagger\) has four-by-four system blocks indexed
by joint cells α=(a,b), β=(a',b'):

\[
\widetilde N_{ab,a'b'}=\delta_{bb'}\,\widetilde D_{aa'}\otimes B_t.
\]

For \(e=(1,1)^T\) and \(f=Ze=(1,-1)^T\), a native cell indicator becomes
the following system read vector in its own block:

\[
v_{ab}=(Z^ae)\otimes(Z^be),\qquad
\sum_{a,b}v_{ab}v_{ab}^\dagger=4I_4.
\]

Define the complete cell-form matrix and total-entry mass by

\[
\Gamma_{\alpha\beta}(N)
=v_\alpha^\dagger\widetilde N_{\alpha\beta}v_\beta,
\quad q_\alpha=\Gamma_{\alpha\alpha},\quad
m_{16}(N)=\mathbf1^\dagger N\mathbf1=\sum_{\alpha,\beta}\Gamma_{\alpha\beta}.
\]

Exact recordability means \(\Gamma_{\alpha\beta}=0\) for α≠β as complex
numbers. Positivity then makes diagonal q values nonnegative, and their
sum is the total mass. All conjugate cross entries are retained.

Initially the tensor product is PSD and exactly recordable for **every**
allowed local c: different reference-cell blocks vanish, and the remaining
off-a contraction contains \(e^\dagger If=0\). Its mass is
\(m_{16}(N)=m(D)m(R_t)=2\operatorname{Tr}A\). Thus the later exclusion does
not come from imposing c=0 in composition or initial validation.

## 3. The fixed shared-system coupler

On system basis (i,j), use

\[
\mathrm{CNOT}|i,j\rangle=|i,j\oplus i\rangle,\qquad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
U=(I\otimes H)\mathrm{CNOT}.
\]

Every joint-cell block is conjugated by that **same** U. The native
sixteen-label lift is

\[
\mathcal U=T^\dagger(I_{\mathrm{cells}}\otimes U)T,
\qquad N'=\mathcal U N\mathcal U^\dagger.
\]

In particular one must not simply apply a four-by-four gate to incorrectly
grouped native label bits. The untwist, permutation and reference orientation
are part of the declared interface. The implementation uses the integer
numerator \(U_0=(I\otimes H_0)\mathrm{CNOT}\) and congruence factor 1/2,
with \(U_0U_0^\dagger=2I\); no approximate square root is inserted.

After the shared lift, every diagonal joint-cell block is
\(M=U(A\otimes B_t)U^\dagger\). Only off-a blocks at equal b can remain,
and they are c times

\[
R_U=U(I\otimes B_t)U^\dagger
=\frac{I+t Z\otimes X}{4}.
\]

Indeed CNOT sends \(I\otimes Z\) to \(Z\otimes Z\), and the final target H
sends target Z to X. Reverse off-a blocks contain \(\bar c R_U\), not c.

## 4. Local surviving-subcone theorem

**Theorem.** For fixed real t≠0 in [-1,1], the maximal local subcone whose
independent composite remains exactly recordable after the specified lift
is precisely

\[
\boxed{\mathcal C_{\mathrm{survive}}(t)
=\{D(A,0):A\succeq0\}.}
\]

For t=0 the whole original local cone survives. Normalized slices impose
\(2\operatorname{Tr}A=1\); the cone statement also includes unnormalized
positive inputs and zero.

**Necessity.** Direct contraction gives

\[
\Gamma'_{00,10}=c\,(e\otimes e)^\dagger R_U(f\otimes e)=tc,
\]

because the identity term vanishes and
\((e^\dagger Zf)(e^\dagger Xe)/4=1\). Similarly,

\[
\Gamma'_{01,11}=-tc,
\quad\Gamma'_{10,00}=t\bar c,
\quad\Gamma'_{11,01}=-t\bar c.
\]

Every other off-cell form is zero. Thus exact recordability with nonzero
t forces both the real and imaginary parts of c to vanish, independently
of A. For imaginary c the offending form is imaginary; a test that checks
only real additivity would miss this exact-recordability obstruction.

**Sufficiency.** If c=0, every off-cell raw block already vanishes and
remains zero under the shared lift. Positivity is preserved by unitary
congruence, for every A≥0, including singular boundary states. Using the
read-vector resolution,

\[
\sum_{a,b}q'_{ab}=4\operatorname{Tr}M
=4\operatorname{Tr}A\operatorname{Tr}B_t=2\operatorname{Tr}A=m(D).
\]

Hence all c=0 states survive with the correct mass; no normalization
repair is needed. This proves maximality relative to the fixed interface. ∎

The cross-form linear map has real rank two on the full six-dimensional
local span when t≠0, with the four A coordinates as its kernel. At t=0
its rank is zero. These are exact linear identities, not conclusions from
sampling a finite collection of A matrices.

This is a **domain-viability exclusion**, not a dynamics that sets an
initial c to zero. A valid local c≠0 input and its full prospective coupled
kernel remain available for inspection as mathematical data, but cannot
be declared a lawful source for this joint record partition. No outcome
carrying “the measured value of c” is inferred from an inadmissible record
context.

## 5. Mass is not a substitute for recordability

For the chosen U, the two off-a forms tc and −tc cancel in the total-entry
sum. Consequently, **even when c≠0**, the raw coupled output satisfies

\[
m_{16}(N')=\sum_{ab}q'_{ab}=2\operatorname{Tr}A,
\qquad\operatorname{Tr}N'=2\operatorname{Tr}A.
\]

Thus a normalized, positive output can nevertheless fail exact
recordability. Checking only its norm, total mass or diagonal weights is
insufficient. The checker must inspect all complex cross-cell forms before
authorizing any joint commitment. Renormalization cannot repair a nonzero
cross form in this normalized example.

Ordinary trace and total-entry mass must still not be identified generally.
For an arbitrary algebraic shared system unitary W, put
\(R_W=W(I\otimes B_t)W^\dagger\) and
\(z_b=v_{0b}^\dagger R_Wv_{1b}\). Then

\[
m_{16}(N_W)=2\operatorname{Tr}A+2\operatorname{Re}\bigl(c(z_0+z_1)\bigr),
\quad \operatorname{Tr}N_W=2\operatorname{Tr}A.
\]

For example SWAP gives z0=z1=t, so the total-entry mass is
\(2\operatorname{Tr}A+4t\operatorname{Re}c\). The requested coupler's mass
preservation does not extend to every shared unitary on the full local
input cone. This countercontrol asserts only a mathematical action, not
SWAP availability in the supplied catalogue.

## 6. Countercontrols and the limited larger closure

**Local products are blind to c.** For any algebraic
\(W=W_1\otimes W_2\),

\[
R_W=I\otimes W_2B_tW_2^\dagger.
\]

Every off-a contraction therefore contains \(e^\dagger f=0\). All local
c values survive all product-unitary tests, including their finite words,
with positivity, exact recordability and correct total-entry mass. This
does not depend on sampling a finite Clifford subgroup.

**An unpolarized reference is blind under every shared unitary.** At t=0,
\(R_W=I_4/4\) for any W, so the same off-a contractions vanish. The entire
local cone survives any single shared-unitary test with that reference;
finite compositions of shared unitaries are again shared unitaries. This
is not a statement about additional references, intermediate changes of
the partition or unrestricted composite protocols.

**Not every entangling gate suffices.** CNOT alone gives
\(R=(I+tZ\otimes Z)/4\), but the target read vectors have zero Z
expectation, so this test is still blind to c. The final target H in the
specified witness is significant. No generic “entanglers remove c” rule
is established.

**The c=0 section survives every shared unitary algebraically.** Its
off-cell blocks are all zero, and the same four-vector resolution proves
normalization for any W. The diagonal system block becomes
\(M_W=W(A\otimes B_t)W^\dagger\). An after-the-fact quotient convention is

\[
\rho_{\mathrm{joint}}=4M_W^T
=\bar W\bigl((2A^T)\otimes(2B_t^T)\bigr)W^T.
\]

The transpose/conjugation is essential for complex W or A; the requested
coupler itself is real. This is a correspondence on the surviving family,
not an assertion that all PSD four-dimensional quotient states or all W
are available. The fixed reference and one coupler do not span a globally
selected composite preparation cone.

## 7. Typed validity and joint record contract

The executable separates:

- Local inputs, retaining the full normalized D(A,c) and their separate
  labeled histories. Validating a local input does not demand c=0.
- The independently declared reference, with t, Z orientation, its full
  section kernel and separate input history.
- A full sixteen-label **prospective** joint kernel with input origins,
  tensor/permutation convention and actual coupler metadata. Positivity
  or normalization alone does not confer lawful-source status.
- An explicitly validated joint source, requiring full positivity,
  normalization and every complex cross-cell form to vanish.
- A separately typed full raw terminal cell-cut output after a positive
  lawful joint commitment. No further source reuse or return map is given.

The independent product starts recordable even for c≠0. Applying the one
coupler may produce an invalid prospective object, which remains unchanged
for audit. It cannot undergo a lawful cut, be silently renormalized or be
reused as a lawful source. All applicable checks occur before commitment
or normalization. Raw matrix countercontrols are algebraic diagnostics;
they are not additional couplers admitted by the typed primary path.
The declaration of independence records the premise; its validation does
not prove that real preparations are independent.
Permutation metadata preserves compatible numeric-equivalent inputs under
the existing exact equality check, then stores the canonical built-in-integer
permutation in both snapshots and joint records. One-shot iterables remain
supported; no floating-point kernel arithmetic or label rounding is introduced.

For a lawful normalized joint source and cell α with qα>0, the terminal
raw residual is exactly \(E_\alpha N'E_\alpha/q_\alpha\) on all sixteen
labels. Its record retains the cell outcome (a,b), the actual coupler,
reference polarization/orientation, independent origin labels and both
complete input histories. Every input event appears in the new joint
event's precursor with its origin tag. Equal local event numbers from
different origins are not merged. Joining the two complete prefixes does
not impose an ordering between their independent events.

A zero-weight cell may still have a nonzero raw cut; it is never
normalized or committed. This possible dark terminal behavior is distinct
from RI-08c's faithful same-source-cone repeatable branch. No reusable
joint measurement, general composite SDK, history-schedule covariance or
new event-growth law follows. Snapshot/history validation establishes the
declared finite grammar, not physical preparation provenance or global
reachability.
The terminal constructor does additionally check its available exact source:
the selected source probability must be positive, and the supplied output
must equal that source's full normalized literal cut. Matching support or
record metadata alone cannot create a valid terminal result.

## 8. Relation to prior image constructions and scope

The [earlier operational reconstruction](../t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
started with supplied reconstruction principles and flat-frame image cones.
The [coherent-readout candidate](../t8-q-coherent-readout-2026-09-12/CANDIDATE.md)
supplied a compatible noncommutative matrix-algebra encoding. This sitting
does not assume either restricted local image at input: all allowed
complex c values enter the independent tensor product and are initially
recordable. The extra joint viability requirement then excludes nonzero c
for the fixed polarized interface.

That distinction does not make the new premises DET-derived. The tensor
composition and independence rule, labeled factor regrouping, polarized
reference, shared-system lift, gate availability and fixed exact joint
recordability requirement remain supplied. The result would not follow
from local record predictions alone; the required countercontrols show
that neither local product controls nor an unpolarized reference imposes
the same exclusion.

The result does not infer all composites, arbitrary ancilla complete
positivity, full preparation richness, native entangler availability,
complex-field selection, entanglement advantage, full QM, geometry or
physical promotion. It neither proves laboratory access to c nor changes
Option B or Status M. It does not prove that a local state failing this
interface cannot occur under some other interface or physical theory.

The QR owner stops at this bounded handoff for independent acceptance.
Accepted bundles, RET, coordinator-owned application/registry work, QR-05
atlas, clocks/book work and κ-gravity remain untouched. Approximate
repeatability/robustness is a separate queued question, not designed or
implemented here. No successor is opened by this note.

## 9. Reproduction

[model.py](model.py) retains full complex kernels with exact Gaussian-rational
arithmetic, explicit sixteen-label transformations, typed validity and
positive-branch record handling. [check.py](check.py) supplies independent
exact witnesses and linear identities; it does not replace the universal
proof with a depth-limited or state-sampled claim. The mathematical proofs
apply to real t and complex kernels beyond the rational executable inputs.

```sh
.venv/bin/python -B docs/validation/t8-q-joint-recordability-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-joint-recordability-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-joint-recordability-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-joint-recordability-2026-09-13
```

Final source hashes, replay and internal review are recorded in the
[handoff](../../coordination/QR_HANDOFF.md). No external peer review, proof
assistant verification or empirical experiment is claimed.
