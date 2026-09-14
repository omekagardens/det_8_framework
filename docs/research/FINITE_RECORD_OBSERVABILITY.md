# Conditional observability and stability of a finite record cone

13 September 2026. **RI-08 consolidation — conditional synthesis;
accepted by the coordinator 14 September 2026 UTC.**
This document assembles one conditional finite-dimensional theorem from
accepted constructions. It makes the input matrices, observation law and
record contract explicit; it does not establish that DET selects physical
QM, its complex field, tensor composition or measurement rule. No ontology
is required to assess the theorem. Mathematical states below need not be
physically available preparations.

## 1. Object, finite premises and record scope

Write \(X,Y,Z\) for the Pauli matrices, \(I\) for the two-dimensional identity,
and \(\|\cdot\|_1\) for the trace norm. Explicitly,
\[
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]
Fix a known real \(|t|<1\), reference/frame and coupler
\(U=(I\otimes H)\mathrm{CNOT}\), where
\(\mathrm{CNOT}|i,j\rangle=|i,i\mathbin\oplus j\rangle\).
All four label coordinates \((a,i,b,j)\) are binary. Native order has index
\(8a+4i+2b+j\); a fixed signed permutation T groups cells
\(\alpha=(a,b)\):
\[
T_{8a+4b+2i+j,\,8a+4i+2b+j}=(-1)^{ai+bj},\qquad
B_t=(I+tZ)/4,
\]
\[
M_t(\rho)=U\bigl((\rho^T/2)\otimes B_t\bigr)U^\dagger,\qquad
\mathcal I_t((\rho_\alpha))
=T^\dagger\operatorname{diag}\bigl(M_t(\rho_{00}),M_t(\rho_{01}),
M_t(\rho_{10}),M_t(\rho_{11})\bigr)T,
\]
\[
L_t=\{\mathcal I_t((\rho_\alpha)):\rho_\alpha\succeq0
\text{ independently}\}.
\]
These are supplied interface definitions. Complex transposes remain literal.
The image has real span dimension sixteen, not the 256-dimensional Hermitian
space of all sixteen-label matrices. Undoing T and taking each block's
partial trace gives
\[
\rho_\alpha=4\bigl[\operatorname{Tr}_{\rm ref}
(U^\dagger M_\alpha U)\bigr]^T.
\]
This proves injectivity. Membership also requires reconstituting every native
entry, including off-block zeros; a partial trace must not project an outsider
into the cone. These facts and the following mass formulas are proved in
[RI-08g §§1–3](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md).

Native normalization is total-entry mass, not generally raw trace:
\[
E_{ab}=(I+(-1)^btZ)/4,\quad
\sigma_\alpha=E_\alpha^{1/2}\rho_\alpha E_\alpha^{1/2}
=\tfrac12(q_\alpha I+r_\alpha\cdot(X,Y,Z)),
\]
\[
m(N)=\mathbf1^\dagger N\mathbf1=\sum_\alpha q_\alpha,
\qquad \tau(N)=\operatorname{Tr}N=\tfrac14\sum_\alpha\operatorname{Tr}\rho_\alpha.
\]
The positive filters are invertible; positivity means
\(q_\alpha\ge\|r_\alpha\|_2\). The normalized slice \(m=1\) has affine
dimension fifteen. “Mass” here is a normalization functional, not rest mass.

Supply the known finite command
\[
U_A=\tfrac35I-\tfrac45iX,\qquad
\sigma_\alpha\longmapsto U_A\sigma_\alpha U_A^\dagger,
\]
and its two successive applications. On raw \(\rho\) this is a weighted
congruence through the filter, not ordinary unitary conjugation. Supply one
exactly calibrated, available, terminal internal read:
\[
n=(3/5,0,4/5),\quad Q_\pm=(I\pm n\cdot(X,Y,Z))/2,\quad
p_{\alpha,\pm}=\operatorname{Tr}(Q_\pm\sigma_\alpha)
=\tfrac12(q_\alpha\pm n\cdot r_\alpha).
\]
The read retains the cell: eight full outcomes, not a global binary law or
cell-conditioned probabilities. Positive effects do not establish physical
availability or calibration. These finite premises suffice; an all-real
group, inverse commands, continuity and a Hamiltonian are unnecessary.
([RI-08i §§1–2](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md).)

The three settings are alternative additional words \((),(A),(A,A)\) on
the same supplied normalized snapshot. Its full committed prefix, context,
frame, calibration, initial pending word and nominal metadata must match in
comparisons. Previously applied pending commands are retained, not reapplied.
Equal matrices never identify different actual words. This mathematical
comparison supplies neither repeated preparation access nor earlier
local/reference-selection probabilities.

The read has no specified postmeasurement output. Retaining its pre-read
source is an audit operation, not reconstruction of a reusable state from an
effect. Raw payload is not a policy oracle. These terminal-only and
conditional-snapshot restrictions follow
[RI-08i §§4,7](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md).

## 2. Combined finite observability and stability theorem

Under §1, three complete resolved tables characterize compatible normalized
sources uniquely, reconstruct every native entry, and satisfy the sharp
filtered and stated native-distance bounds below.

**Compatibility and reconstruction.** Conjugating the read backwards by the
known commands gives rows of
\[
V=\begin{pmatrix}
3/5&0&4/5\\
3/5&96/125&-28/125\\
3/5&-1344/3125&-2108/3125
\end{pmatrix},\qquad \det V=-73728/78125.
\]
For each cell, tables must share
\(q_\alpha=p^{(k)}_{\alpha,+}+p^{(k)}_{\alpha,-}\).
Their differences \(d_k=p^{(k)}_{\alpha,+}-p^{(k)}_{\alpha,-}\)
satisfy \(d=Vr_\alpha\), with exact inverse
\[
x=\frac{125d_0+70d_1+125d_2}{192},\quad
y=\frac{-55d_0+180d_1-125d_2}{192},\quad
z=\frac{195d_0-70d_1-125d_2}{256}.
\]
The necessary and sufficient conditions are
\[
q_\alpha\ge0,\qquad \sum_\alpha q_\alpha=1,\qquad
q_\alpha^2\ge x_\alpha^2+y_\alpha^2+z_\alpha^2,
\]
together with those shared cell sums. Necessity follows from positive
filtering. Conversely, these inequalities construct positive \(\sigma\);
set \(\rho_\alpha=E_\alpha^{-1/2}\sigma_\alpha E_\alpha^{-1/2}\)
and apply \(\mathcal I_t\). The inverse identities reproduce every table
entry; injectivity establishes uniqueness. Zero cell mass forces its whole
block to zero without division by q. Incompatible exact tables are refused,
not clipped, fitted or renormalized. Fewer than three resolved binary settings
leave a Bloch direction undetermined in some positive interior neighborhood;
resolved randomized choices still count as their actual settings.
([RI-08i §6](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md).)

**Stability.** For two compatible sources define
\[
\epsilon_k=\operatorname{TV}(p_k,p'_k)
=\tfrac12\sum_{\alpha,\pm}|p^{(k)}_{\alpha,\pm}-p^{\prime(k)}_{\alpha,\pm}|,
\quad d_F=\tfrac12\sum_\alpha\|\Delta\sigma_\alpha\|_1,
\quad d_N=\tfrac12\|\Delta N\|_1.
\]
Put \(B=V^{-1}\), \(b_k=\|B_{\cdot k}\|_2\), \(C=\sum_kb_k\). Then
\[
\boxed{\max_k\epsilon_k\le d_F\le\sum_kb_k\epsilon_k
\le C\max_k\epsilon_k},\qquad
\boxed{\frac{d_F}{1+|t|}\le d_N\le\frac{d_F}{1-|t|}}.
\]
Here \(d_F\le1\); raw kernels are not trace-one states, so \(d_N\) is
not a probability distance.

For a Hermitian block difference, its two eigenvalues give
\[
\|\Delta\sigma\|_1=\max(|\delta q|,\|\delta r\|_2),\qquad
\epsilon_k=\tfrac12\sum_\alpha
\max(|\delta q_\alpha|,|v_k\cdot\delta r_\alpha|).
\]
Unit-length axes prove the lower bound. Writing
\(\delta r=\sum_kB_{\cdot k}\delta d_k\) gives the upper bound by the
triangle inequality; \(b_k\ge1\) since \(v_k\cdot B_{\cdot k}=1\),
so the same weighted maximum also controls \(|\delta q|\).

For the native norm, \(\operatorname{Tr}B_t=1/2\), tensor trace norms,
transposition and unitary invariance give
\[
\|\Delta N\|_1=\tfrac14\sum_\alpha\|\Delta\rho_\alpha\|_1.
\]
Congruence by \(E^{1/2}\) and the corresponding inverse inequality give
\[
\frac{1-|t|}{4}\|\Delta\rho\|_1
\le\|\Delta\sigma\|_1
\le\frac{1+|t|}{4}\|\Delta\rho\|_1.
\]
Summation yields the native comparison.
Thus reconstruction and stability concern the same full native object,
not unrelated inverse and distance conventions.
([RI-08j §§1–4](../validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md).)

At the fixed tilt,
\[
b_0=b_2=\frac{125\sqrt{41}}{768},\quad
b_1=\frac{5\sqrt{6409}}{384},\qquad C\approx3.126749168936497.
\]
For executable bounds, positive square checks establish
\[
\sqrt{41}\le640313/100000,\quad\sqrt{6409}\le1000703/12500,
\quad\widehat b_0=\widehat b_2=640313/614400,\quad
\widehat b_1=1000703/960000.
\]
The decimal is explanatory; the rational enclosures are certified but not
sharp. The accepted implementation fixes \(t=3/5\); the proof covers each
fixed known interior t.

**Deterministic budget consequence.** For supplied complete normalized
tables \(y_k\), which may disagree in cell mass across settings, and exact
\(\eta_k\ge0\), define
\[
\mathcal F=\{N\in L_t:m(N)=1,
\operatorname{TV}(p_k(N),y_k)\le\eta_k\ \forall k\}.
\]
A supplied exact positive candidate satisfying the inequalities proves
\(\mathcal F\ne\varnothing\). For any two feasible candidates,
triangle TV gives \(\epsilon_k\le2\eta_k\), hence
\[
\operatorname{diam}_{d_F}\mathcal F\le2\sum_kb_k\eta_k
\le2\sum_k\widehat b_k\eta_k,\qquad
\operatorname{diam}_{d_N}\mathcal F
\le\frac{2\sum_k\widehat b_k\eta_k}{1-|t|}.
\]
Failure of one candidate is inconclusive, not infeasibility. Exact-inverse
refusal can coexist with budget feasibility; no solver searches for a fit.
Raw audits require `metadata=None`. Only a typed State binds matching
context/history/pending metadata; that check does not certify empirical
provenance. Audit objects are not prepared states or terminal continuations.
Budgets are deterministic premises, not confidence levels. These diameter
bounds and the composed \(C/(1-|t|)\) coefficient are not claimed sharp.
([RI-08j §5](../validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md).)

## 3. Construction route and the separate classification

The route is conditional, not one implemented end-to-end process. In the
table, “restriction” means viability under a specified interface, not a
dynamics deleting inconvenient input data.

| Route | Mathematical or implementation status |
| --- | --- |
| Maximal \(K_P\) → cell weights | **Proved effect restriction:** for the full PSD exact-recordability cone of a fixed partition, every real-linear \(0\le f\le m_P\) factors through cell weights. “Bounded” means whole-cone mass domination, not arbitrary norm-bounded probes. [RI-08a §§1–3](../validation/t8-q-maximal-record-domain-2026-09-13/MAXIMAL_DOMAIN_QUOTIENT.md). |
| Supplied local controls → \(\mathcal C\) | **Additional control/calibration premises plus proved viable-domain restriction:** the stated H/P/Z words, mass/recordability preservation and swap calibration select \(D(A_{\rm loc},c)=\left(\begin{smallmatrix}A_{\rm loc}&cZ\\\bar cZ&ZA_{\rm loc}Z\end{smallmatrix}\right)\), \(A_{\rm loc}\succeq\lvert c\rvert I\). [RI-08b §§1–2](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md). |
| \(\mathcal C\) → \(\mathcal C_0=\{c=0\}\) at the direct joint interface | **Additional independent tensor/reference/coupler premises plus proved restriction:** nonzero reference polarization gives cross-cell forms \(\pm tc\), forcing c=0 for exact joint recordability. At t=0 all \(\mathcal C\) survives. [RI-08d §§1,4,8](../validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md). |
| Local reusable snapshot → joint interface | **Separately implemented conditional adapter:** RI-15 transfers every kernel entry, preserving histories and pending/frame/controller context in immutable wrappers, not added legacy fields. It validates the supplied independent product and single coupling, retains invalid prospective inputs, and preserves terminal output types. [RI-15 §§1–4](../validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md). |
| Coupled \(\mathcal C_0\) → \(K_t\) | **Fixed image construction:** local \(J_2(\rho)=D(\rho^T/2,0)\), independently composed with the specified reference and coupled, has four equal \(M_t(\rho)\) blocks. Thus \(K_t=\{\mathcal I_t((\rho,\rho,\rho,\rho)):\rho\succeq0\}\), not a supplied reset or adapter into reusable \(L_t\). [RI-08f §1](../validation/t8-q-joint-repeatability-2026-09-13/JOINT_REPEATABILITY.md). |
| Equal-block \(K_t\) → independent-block \(L_t\) | **Proved convex construction and explicitly changed return type:** the smallest convex cone containing \(K_t\) and closed under literal cuts is \(L_t\). Reusable cuts are separately supplied on that type. [RI-08g §§1–4](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md). |

The local quotient \(\Phi(D)=2A_{\rm loc}^T\) has section
\(J_2(\rho)=D(\rho^T/2,0)\), but \(J_2\Phi\) is not identity on
\(\mathcal C\). Nonzero c remains legitimate local payload, invisible
only to its declared catalogue; other mathematical effects can see it.
Neither the joint viability test nor RI-15 silently replaces an input by
its section. Choosing the c=0 image at t=0 is a construction, not a
polarization-derived exclusion. The raw \(\mathcal C\) span has dimension
six, normalized affine dimension five; its qubit quotient and \(\mathcal C_0\)
each have real span dimension four and normalized affine dimension three.
Neither is the enlarged \(L_t\).
([RI-08b §§3–4](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md).)

The supplied local controls are not mass-preserving on all \(K_P\);
restricting to \(\mathcal C\) therefore does not contradict the full-domain
effect theorem ([RI-08b §7](../validation/t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md)).
There is also a distinct conditional record-producing route: RI-08c adds
positive real-linear same-cone branches, calibration, perfect repeatability
and availability. Its exposed-ray theorem forces
\(B_Q(D)=\operatorname{Tr}(\Phi(D)Q)J_2(Q)\) for a Pauli rank-one Q.
Here c=0 is an output conclusion, not a ban on earlier \(\mathcal C\)
inputs or a reinterpretation of their older terminal cuts. The branch also
changes the A block to a selected ray: it is not \(J_2\Phi\). A proposed
local tree must check every positive leaf actually entering the polarized
joint interface for \(\mathcal C_0\) viability, without excluding earlier
states or leaves that stop locally.
([RI-08c §§1–3](../validation/t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md).)

Convex closure does not supply every independent preparation. RI-15 does
not connect its terminal wrappers to reusable \(L_t\) states or implement
the entire chain. Physical availability and a uniquely selected combined
theory remain open; earlier terminal cuts are never retagged as reusable
sources. A probability- and type-complete operational route still needs
separate orchestration of earlier branch/reference-selection weights;
provenance alone does not supply them. Literal cuts are unnecessary for
§2's three-table theorem. If the
accepted cut/command/stop catalogue is separately retained, known maps and
matching nominal policies give finite predictive equivalence by induction
on their retained-history trees ([RI-08i §4](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md)).

**Separate classification proposition.** Add a real-linear, strongly
continuous, two-sided positive, mass-preserving group indexed by every real
s on fixed interior \(L_t\). Then each cell is invariant and
\(\sigma_\alpha(s)=e^{-isH_\alpha}\sigma_\alpha e^{isH_\alpha}\),
with Hermitian generators modulo scalar identity. Continuity fixes the
four extreme-point components; affine Bloch-ball automorphisms become
rotations, and the continuous group law gives their generators. These are
twelve nontrivial real parameters, not identified energies or physical
clock rates. This stronger hypothesis classifies possible groups; §2
neither needs it nor identifies an unknown Hamiltonian.
([RI-08h §§1–3](../validation/t8-q-reversible-generator-2026-09-13/REVERSIBLE_GENERATOR.md).)

## 4. Sharpness and boundary counterexamples

Write \(Q_{J\pm}=(I\pm J)/2\) for \(J\in\{X,Y,Z\}\).
Alternative axes and endpoints below are mathematical diagnostics, not
newly available reads or preparations.

Sharpness is attainable on the full mathematical cone: give each cell
q=1/4; in three distinct cells choose opposite Bloch vectors
\(\pm\epsilon_kB_{\cdot k}\), with \(\epsilon_kb_k\le1/4\), leaving
the fourth centered. Actual setting errors equal \(\epsilon_k\) and
\(d_F=\sum b_k\epsilon_k\). Equal small errors attain C; a center-mass
transfer attains the lower coefficient one. No preparation procedure is
thereby established.

For general unit read axes, put \(a=|n_x|\), \(b=\|n_\perp\|\), both
positive with \(a^2+b^2=1\). The same calculation yields
\[
C(a,b)=\frac{25}{96}\sqrt{9/a^2+25/b^2}
+\frac1{32}\sqrt{49/a^2+625/b^2},\quad
aC\to1\ (a\to0),\quad bC\to25/12\ (b\to0).
\]
Poor interior conditioning is distinct from exact rank loss. A Z/YZ-only
read has rank twelve, an X-only read rank eight, versus sixteen for a
tilted read; normalized affine dimensions are eleven, seven and fifteen.
Opposite X states are indistinguishable under every common-X word followed
by Z read, yet have tilted plus probabilities 4/5 and 1/5.
([RI-08i §§3,5](../validation/t8-q-terminal-read-observability-2026-09-13/TERMINAL_READ_OBSERVABILITY.md);
[RI-08j §§2–3](../validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md).)

A bounded endpoint counterexample moves \(Q_{Z-}\) from cell00 to cell10,
keeping \(\rho_{01}=(3+t)Q_{Z-}/(1+t)\) common and other blocks zero,
for \(0<t<1\). Both sources are normalized and
\[
d_N=1/4,\qquad d_F=\epsilon_k=(1-t)/4.
\]
At t=1 their raw difference persists while all whole-cone mass-dominated
effects are blind. Faithful inverse filtering cannot cross that boundary.

For rare records, put \(qQ_{X+}\) or \(qQ_{X-}\) in one filtered cell and
the same centered remainder elsewhere. Then \(d_F=q\),
\(\epsilon_k=3q/5\), but conditional trace distance stays one. A positive
cell-weight floor is necessary; at q=0 conditioning is undefined. Finally,
simultaneously conjugating the filtered source and unknown read by W=X
preserves all common-X setting laws, although opposite filtered Z sources
have \(d_F=1\).
Calibration cannot be recovered from that paired ambiguity.
([RI-08j §§4,6](../validation/t8-q-observation-stability-2026-09-13/OBSERVATION_STABILITY.md).)

## 5. Source identity and evidence

The source baseline is the accepted, remotely verified checkpoint
`da8fe99a1b1b91dab962ec0ed17bde349a06458c`. Registered QR statements,
executors, import declarations and hashes remain in the existing
[research registry](registry.json); RI-15 retains its separate
[fixed-alias launcher contract, §5](../validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md).
This synthesis neither replaces nor extends either source inventory.
The corrected J source passed staged normal and
optimized verification. Such witnesses check finite identities and
contracts; universal conclusions depend on the written proofs above and
their cited sections, not suite counts. This consolidation adds no executable,
operation, empirical evidence or release claim.

## 6. Two open bridges

**Retained words and first commitment.**
[RI-07 §§1–4](../validation/t8-q-first-commit-quotient-2026-09-13/FIRST_COMMIT_QUOTIENT.md)
requires finitely many **full** committing labels, faithful finite-dimensional
output cones, and deliberately unobserved silent paths. Arbitrarily long
actual command words create countably many labels even with one command and
a finite controller: \((A^n,\alpha)\) remains distinct for every n.
Matrix equality does not erase those labels. Each bounded finite policy
is covered separately; that fact is not an infinite first-commit theorem.

An extension needs a declared word-indexed output space and complete norm;
absolute or otherwise appropriate operator convergence of the retained
path/word sums; countable mass and never-commit accounting; and justification
for exchanging those sums with word-dependent continuations. Every claimed
quotient must respect those continuations and retained labels. Finite-horizon
identities, per-label scalar convergence or quotient convergence do not
establish this joint result. Silent paths may be eliminated only when the
question actually excludes them; no terminal state is invented for never
committing. This is a named missing cross-bundle argument, already qualified
in [RI-08g §8](../validation/t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md),
not an implementation launched here.

**From synthetic identification to a measured comparator pilot.** The
[exact identifiability theorem, “Domain and question” and “Theorem and finite witnesses”](../coordination/IDENTIFIABILITY_CONTRACT.md)
tests whether a target row annihilates the nullspace of a known design on
unrestricted real parameters. The [public-RET comparator, “Fixed declarations”
and “Public interface and retained records”](../coordination/COMPARATOR_DEMO.md) adds
synthetic model-conditional arithmetic and retained-record replay, not
instrument calibration or measured policy advantage.

A measured pilot still requires an actual instrument and data; a frozen
target, tolerance and evaluation objective; calibrated noise/budgets and
stability; measured acquisition/reset costs; a strong frozen conventional
baseline; and held-out evaluation with justified size and source accounting.
Those requirements are specified in
[the application plan, RI-12](../coordination/APPLICATION_WORK_PLAN.md).
J's deterministic budgets are not confidence levels, and its cone-specific
constants do not transfer automatically to that different observation model.
No RET or apparatus work is authorized by this synthesis.
