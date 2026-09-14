# RI-08b — control-selected qubit operational quotient

13 September 2026. **CONDITIONAL_MAXIMAL_VIABLE_CONE_THEOREM;
CATALOGUE_RELATIVE_QUBIT_QUOTIENT.** Internal mathematical result, submitted
for coordinator acceptance. No DET axiom, physical availability claim,
complex-field selection, geometry result or release promotion is made.

## 1. Question and explicit premises

Start from the **full** four-label exact-recordability cone, not a
block-diagonal or quantum-image restriction. With partition
\(\mathcal P=\{\{0,1\},\{2,3\}\}\), write

\[
D=\begin{pmatrix}A&F\\F^\dagger&B\end{pmatrix}\succeq0,
\quad e=(1,1)^T,\quad
\beta_0=(e,0)^T,\quad\beta_1=(0,e)^T.
\]

Exact recordability is \(\beta_0^\dagger D\beta_1=e^\dagger Fe=0\).
The real Hermitian linear space \(E_{\mathcal P}\) has dimension 14;
\(K_{\mathcal P}=E_{\mathcal P}\cap\mathrm{PSD}_4\). Define

\[
q_r(D)=\beta_r^\dagger D\beta_r,\qquad
m(D)=\mathbf1^\dagger D\mathbf1.
\]

On the recordable cone, \(m=q_0+q_1\). This is total-entry mass, not
ambient trace and not physical rest mass. The four labels and partition are
supplied record-context data inherited from the previous obligation.

The following are **additional candidate premises**, not consequences of
bare DET record growth, positivity or exact recordability:

1. At a fixed declared record prefix and apparatus/controller type, reversible
   residual controls H, quarter-phase P and Z, including their inverses, are
   available independently of hidden residual values. Put
   \[
   Z=\operatorname{diag}(1,-1),\quad
   H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad
   P=\operatorname{diag}(1,i),\quad
   W_U=\operatorname{diag}(U,ZUZ),\quad S_U(D)=W_UDW_U^\dagger.
   \]
   H and Z are self-inverse. Availability depends on the declared type and
   controller, never an oracle inspecting an unrecorded state.
2. Every finite word in those controls preserves total-entry mass and exact
   two-cell recordability at that same type. Controls themselves append no
   record; their externally known setting word remains accessible.
3. **Readout-swap calibration**, including at every reachable source state:
   \[
   q_0(S_ZD)=q_1(D),\qquad q_1(S_ZD)=q_0(D).
   \]
   This is a calibration constraint, **not an extra block-swap control**.
4. The observation catalogue consists of those finite words followed by an
   available terminal binary cell read. Its literal residual branch is
   \(E_rDE_r\), where \(E_r\) projects onto cell r. Positive branches append
   the outcome, actual setting word and precursor. The output has a distinct
   terminal type, with no source-type continuation supplied.

The maximal viable cone is the set of all initial raw kernels satisfying
these conditions. Maximality describes a mathematical domain; it does not
assert that every member is physically preparable. The proof below uses a
complex kernel space already declared in the candidate. In particular the
quarter-phase control inserts i; recovering complex qubit notation is not a
derivation choosing complex rather than real quantum theory.

## 2. Maximal viable cone theorem

**Theorem.** The maximal viable cone is exactly

\[
\mathcal C=\left\{D(A,c)=
\begin{pmatrix}A&cZ\\\bar cZ&ZAZ\end{pmatrix}:
A\succeq |c|I,\quad c\in\mathbb C\right\}.
\]

In particular, cross-cell payload need not vanish and c is not restricted
to be real. The real span has dimension six, and \(m(D)=2\operatorname{Tr}A\)
is faithful on this cone.

**Necessity.** Set \(G=FZ\), \(C_B=ZBZ\), \(K=A-C_B\). The fixed unitary
\(V=\operatorname{diag}(I,Z)\) changes raw coordinates to

\[
VDV^\dagger=\begin{pmatrix}A&G\\G^\dagger&C_B\end{pmatrix}.
\]

In these coordinates a control conjugates all three blocks by U. With
\(f=Ze=(1,-1)^T\), recordability for I, Z and H requires

\[
e^\dagger Gf=0,\qquad f^\dagger Ge=0,\qquad
e^\dagger HGHf=2G_{01}=0.
\]

The first two equations make G diagonal in the X eigenbasis, so
\(G=aI+bX\) with complex a,b. The third forces b=0. Thus \(F=cZ\).
Neither Hermiticity of D nor these equations require c to be real.

At the initial state the two swap-calibration equations become
\(e^\dagger Ke=f^\dagger Kf=0\). Hence
\(\operatorname{Tr}K=\operatorname{Tr}(XK)=0\). Once G is scalar, cross-cell
mass vanishes after every control and

\[
m(S_UD)=\operatorname{Tr}(A+C_B)
       +\operatorname{Tr}(U^\dagger XU K).
\]

Using \(H^\dagger XH=Z\) and \(P^\dagger XP=-Y\), mass preservation under
H and P kills \(\operatorname{Tr}(ZK)\) and \(\operatorname{Tr}(YK)\).
The Hermitian Pauli basis then gives K=0, or \(B=ZAZ\). These finitely many
necessary conditions already force the claimed linear form.

**Positivity.** In the V coordinates the matrix is
\(\left(\begin{smallmatrix}A&cI\\\bar cI&A\end{smallmatrix}\right)\).
Diagonalizing its two-dimensional cell factor gives blocks
\(A+|c|I\) and \(A-|c|I\). Thus full raw positivity is equivalent to
\(A\succeq |c|I\), including c=0 and singular boundary cases.

**All-word sufficiency.** Directly,

\[
S_U D(A,c)=D(UAU^\dagger,c).
\]

Positivity, recordability, mass and swap calibration therefore hold after
every finite word and inverse in the declared catalogue. This proves
maximality, rather than merely testing words up to a chosen depth. The
identity holds algebraically for arbitrary unitary U; **it does not grant
availability of arbitrary U**. Four real A coordinates and two real c
coordinates are independent, with an interior \(A\succ |c|I\) in this
six-dimensional span. Finally \(m=2\operatorname{Tr}A\), and m=0 forces
A=c=0. The normalized raw base has affine dimension five. ∎

## 3. Qubit quotient, image and exact future equivalence

Define the positive linear projection and its positive section by

\[
\Phi(D(A,c))=\rho=2A^T,\qquad
J_2(\rho)=D(\rho^T/2,0).
\]

The image is exactly \(\mathrm{PSD}_2\), with
\(\operatorname{Tr}\rho=m\), because \(\Phi J_2=\mathrm{id}\). Normalized
images are qubit density matrices. J2 is a mathematical section, not a
physically available preparation, reset, or return from a terminal state.
With this transpose convention the control correspondence is

\[
\rho\longmapsto\bar U\rho U^T,
\]

not \(U\rho U^\dagger\). The terminal read probabilities satisfy

\[
q_0(S_UD)=\operatorname{Tr}(\rho Q_U),\quad
Q_U=\tfrac12(U^\dagger ee^\dagger U)^T,\quad
q_1=m-q_0.
\]

I, H and P give respectively the positive X, Z and Y projectors:

\[
q_0(D)=\tfrac12(m+\operatorname{Tr}\rho X),\quad
q_0(S_HD)=\tfrac12(m+\operatorname{Tr}\rho Z),\quad
q_0(S_PD)=\tfrac12(m+\operatorname{Tr}\rho Y).
\]

**Equivalence theorem.** At the same declared prefix, type and known settings,
two normalized source kernels have identical probabilities for all declared
control-word/terminal-read experiments iff their A blocks agree. For
unnormalized kernels compare both branch weights, retaining total mass.
The three displayed readouts prove necessity by Pauli tomography; the
control formula proves sufficiency. Committed history and externally known
settings are not identified with one another by this residual quotient.
For the same word and outcome, equal A also gives identical full raw cell
cuts: the literal cut deletes c. The limitation concerns extra **source,
pre-read** effects that could inspect c, not effects on these identical
terminal cut outputs.

The generated conjugation catalogue has 24 distinct signed-Pauli actions.
These are discrete controls, not all qubit rotations. The result does not
supply all preparations, effects, POVMs, instruments, composites or ancillas.

## 4. Raw information is not universal gauge

Take \(A=I/4\) and \(c=+1/8\) or \(-1/8\). Both raw kernels are normalized
and positive. They are distinct, including their cross-cell payload, but
every experiment in the declared catalogue has identical predictions.

This cannot be promoted to equivalence for **all** bounded effects on
\(\mathcal C\). Since

\[
|c|\le\lambda_{\min}(A)\le\tfrac12\operatorname{Tr}A=m/4,
\]

the real-linear functional
\(g(D)=m(D)/2+\operatorname{Re}c\) is bounded between m/4 and 3m/4.
It is a valid mathematical effect on the entire selected cone and gives
5/8 versus 3/8 for the two states. For a fixed normalized candidate h,
\(T_g(D)=g(D)h\) and \(T_{\mathrm{rest}}(D)=(m-g)(D)h\) are positive
complete mathematical branch maps that also fail to descend through A.
Neither effect nor map is admitted as available by this sitting.

Thus selecting this cone alone does not force the qubit quotient. The
restricted observation/control catalogue is load-bearing. c is retained
raw information, only invisible to this catalogue, not universally
unobservable or a proved physical gauge degree of freedom.

Nor do the premises force preparation richness. The invariant ray
\(\{D(\lambda I,0):\lambda\ge0\}\) also satisfies every control and
calibration requirement. All controls act trivially there and normalized
reads give 1/2,1/2. A physical preparation catalogue confined to this ray
is not excluded. The maximal cone theorem does not itself rule out all
restricted classical operational models.

## 5. Terminal cut, records and zero probability

For every nonzero source candidate, both A and ZAZ are nonzero. A literal
cell cut retains exactly one diagonal block and deletes the other. It
therefore **leaves the source cone**, including at c=0. Even when all
probability lies in the selected cell, the other raw block can remain
nonzero before the cut. No same-type serial measurement closure follows.

For a normalized source state and q_r>0, the implemented transition is

\[
(C,D;w)\longmapsto
\left(C\cup\{(r,w,\mathrm{precursor})\},
\frac{E_rDE_r}{q_r};\ \text{terminal-cell-cut type}\right).
\]

The full four-label residual survives; it is not silently replaced by a
two-dimensional compressed or rebuilt quantum state. The actual finite
setting word w, outcome, fresh event id and entire earlier committed prefix
as chosen precursor are retained. This prefix-chain rule is a declared
recording fixture, not a spatial growth or geometry law. Earlier records
remain unchanged. The model validates prefix grammar but does not assert
global preparation reachability of every supplied snapshot.

Source controls reject terminal states. One may not reinterpret the section
J2 as an authorized reset or use a constructor to bypass this type boundary.
No reusable Lüders, repreparation or reset instrument is inferred.

**Zero-weight nonzero cut.** For v=(1,-1)^T, let A=vv†/4 and c=0. Then m=1,
q0=0 and q1=1, but E0 D E0 is nonzero and positive. The zero branch is never
normalized, selected or appended as a record. More generally a zero cell
weight forces A to have a null vector, hence c=0, but need not make the raw
selected block zero. The terminal constructor is used only for positive
branches; impossible outputs remain raw algebraic branch values.

## 6. Deletion tests on the whole remaining word-closed catalogue

Retain positivity, the same record partition and all premises except the
one named. In V coordinates, write \(G=FZ\), \(C_B=ZBZ\), \(K=A-C_B\).
The maximal remaining families are:

| Deleted premise | Remaining linear form, subject to full PSD |
| --- | --- |
| H and its availability | G=cI, K=δZ |
| Quarter-phase P and its inverse | G=cI, K=δY |
| Z readout-swap calibration, not the Z control | G=cI, K=δI |

Here c is complex and δ is real. **Proof:** recordability for U and ZU
removes both off-diagonal entries of UGU† in the X basis. A second retained
axis, obtained from P or H, makes G scalar. Mass preservation makes the
coefficients of K along the retained signed Pauli orbit equal; the presence
of both signs makes each zero. Calibration removes its trace. Without H,
the X orbit is ±X,±Y and the remaining Z line is invariant under P and Z.
Without P it is ±X,±Z and the remaining Y line changes sign under H and Z.
Without calibration the full orbit removes all traceless components but
leaves I. Each stated family is invariant under all retained generators
and inverses, proving all-word sufficiency as well as necessity.

Exact normalized witnesses, all with G=0, are:

- No H: A=I/4+Z/8 and C_B=I/4−Z/8. Every retained word is lawful;
  restoring H changes mass from 1 to 3/2.
- No P: A=I/4+Y/8 and C_B=I/4−Y/8. Every retained word is lawful;
  restoring P changes mass from 1 to 1/2.
- No swap calibration: A=I/8 and C_B=3I/8. Every full-catalogue word
  preserves mass and recordability, but Z leaves weights (1/4,3/4)
  unchanged rather than swapping them.

The exact checks independently close the signed-Pauli action groups:
24 actions for the full catalogue, 4 without H and 8 without P. Group
closure plus action representatives, not a depth cutoff, certifies the
deletion witnesses over all words. Known setting words remain distinct
labels even when their residual actions coincide. These are relative
indispensability statements for this presentation, **not absolute axiom
minimality**. In particular other supplied controls could provide the
missing axes; DET necessity has not been proved.

## 7. Relation to earlier constructions and the open premise

The [operational completion](../t8-q-operational-completion-2026-09-12/RECONSTRUCTION.md)
assumed a full reconstruction package and transported quantum instruments
onto image cones built using supplied flat frames. Its n=2 section, in the
Hadamard frame and cell-first label order, is precisely the c=0 J2 above.
Here that slice is obtained as a positive section after the viability
calculation; it is not imposed as the whole raw starting domain. This
sitting derives less operational availability, not more of full QM.

The [coherent-readout candidate](../t8-q-coherent-readout-2026-09-12/CANDIDATE.md)
used a supplied noncommutative composition algebra and compression/rebuilding
to implement selective updates. This sitting does not import those updates:
its literal cell cut stays raw and terminal. Both constructions explicitly
depend on extra quantum-compatible mathematical structure.

The [RI-08a full-domain theorem](../t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md)
is not contradicted. Its full K_P bounded effects see only cell weights.
The present controls are not mass-preserving on all of K_P; their all-word
viability selects a proper subcone. Furthermore not every bounded effect
on that subcone belongs to this experiment catalogue. Both departures are
explicit. Existing [first-commit results](../t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md)
are not invoked to grant repeated readouts or arbitrary growing histories.

**Remaining premise:** justify the actual preparation/control/observation
availability from DET, or continue to label it as additional structure.
Tailored block-twisted controls, same-type reversible availability, exact
mass/record closure, swap calibration and quarter-phase availability have
not been derived from DET. Neither has physical preparation richness or a
lawful return from the terminal output type. This note does not design or
authorize their successor; the QR owner stops for coordinator acceptance.

## 8. Reproduction and claim boundary

[model.py](model.py) retains complex raw kernels with exact Gaussian-rational
arithmetic. H congruence uses an integer matrix and factor 1/2, avoiding an
approximate square root. Full PSD checks use exact Schur complements.
[check.py](check.py) independently checks the real linear ranks, control
actions, quotient, deletion families, and terminal record/type boundary.
The real/complex cone proofs apply beyond the rational executable examples.
Tests are regression witnesses, not an external review or Lean certificate.

```sh
.venv/bin/python -B docs/validation/t8-q-control-selected-qubit-2026-09-13/check.py
.venv/bin/python -B -O docs/validation/t8-q-control-selected-qubit-2026-09-13/check.py
.venv/bin/ruff check --no-cache docs/validation/t8-q-control-selected-qubit-2026-09-13
.venv/bin/ruff format --check --no-cache docs/validation/t8-q-control-selected-qubit-2026-09-13
```

The [handoff](../../coordination/QR_HANDOFF.md) records final verification and
source hashes. Accepted earlier bundles remain unchanged. This obligation
does not extend RET, RI-11, QR-05 coverage/noncollapse/identifiability work,
clocks, book work, κ-gravity, unbounded histories, growth or geometry.
There is no physical discriminator or release claim. Option B and Status M
remain unchanged; no staging, commit or push is part of this sitting.
