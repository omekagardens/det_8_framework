# QR-MAP: conditional finite-QM reconstruction and an explicit L/F

Begun 12 September; reviewed 13 September 2026. Status: **PROPOSED_AXIOM_EXTENSION;
CONDITIONAL_FINITE_QM; CANDIDATE_L_AND_F_SPECIFIED.**

The owner asked to determine F and L and reconstruct QM, then explicitly
authorized exploring additional, unproved axioms. This note exercises that
authorization without adopting new global DET primitives. It provides:

1. A sufficient operational axiom package, with a published reconstruction
   theorem as an explicit dependency, not a purported new proof of that theorem.
2. A faithful pair-kernel calculus for the resulting **entire finite-dimensional
   quantum framework**, not just one measurement example.
3. A fully specified candidate law L_XYZ and its licensed commit transition F_L.

This is not a derivation of those additional axioms from existing DET, a unique
physical L, infinite-dimensional QM, QFT, spacetime or a physical Hamiltonian.
The [strict kernel derivation and countermodels](../t8-q-strict-derivation-2026-09-12/DERIVATION.md)
remain valid. Hilbert space is a conclusion of the proposed operational package;
the particular quantum protocol below is subsequently **chosen**, not forced.

## 1. Assumption ledger and operational meaning

The distinction between a mathematical representation and a physical law is
load-bearing. All entries marked proposed or chosen remain unproved additions.

| Ingredient | Status here | What it supplies |
| --- | --- | --- |
| Committed C=(V,≺,R), fresh maximal append, unchanged past | Existing QR-MAP architecture | Record-growth meaning |
| Admitted complex strongly positive pair-kernel D | Existing conditional kernel premise | Gram representation, not all QM |
| Finite operational-probabilistic framework | **Proposed** additional structure | Systems, tests, composition, equivalence |
| Six operational postulates below | **Proposed**, not DET theorems | Sufficient reconstruction hypotheses |
| Complete finite complex QM representation | Imported conditional theorem | State/effect/process calculus |
| Compatible history encoding J_n | Explicit construction below | Faithful D coordinates for that calculus |
| Two ports, three axes, action weights, modulo-three context, selective update | **Chosen law**, not reconstructed uniqueness | Concrete L_XYZ |
| Unique physical law, unrestricted original-D interpretation, geometry | **Not established** | No promotion |

A residual system is an interface admitting preparations and subsequent tests.
Two preparations are equivalent when every allowed continuation gives the same
record probabilities; transformation equivalence must also allow ancillary
systems. Parallel/serial wiring, identities, refinement, coarse-graining,
randomization and closure under operational limits are additional structure,
not consequences of an event order. We assume finite-dimensional operational
state spaces and the **full** reconstruction framework, not only these informal
descriptions. The authors' [operational review](https://arxiv.org/html/1506.00398v1)
explains the framework and standing assumptions.

Operational purity means absence of a nontrivial refinement. Discarding a
residual subsystem means ceasing to interrogate it; it does **not** delete a
committed record. Reversible processes act on residual systems, not backward
on the already committed poset. Operational subsystem types are an assumption;
their complex Hilbert tensor representation is a reconstruction conclusion.

We adopt the **2011 CDP formulation**, including its precise definitions:

- **Causality:** preparation probabilities do not depend on later test choices.
- **Perfect distinguishability:** every non-completely-mixed state has a
  perfectly distinguishable alternative.
- **Ideal compression:** preparations admit lossless, efficient encodings.
- **Local distinguishability:** product tests distinguish different joint states.
- **Pure conditioning:** atomic local readout of a pure joint preparation
  leaves a pure nonzero conditional state.
- **Purification:** every state has a pure extension, unique up to reversible
  action on a fixed purifying system.

These are the hypotheses of [Chiribella, D'Ariano and Perinotti, sections II–III](https://arxiv.org/html/1011.6451v3#S3).
The list is a reading aid; the full definitions and standing framework are
incorporated by reference. The 2015 review uses a differently presented
purity principle; we do not silently substitute it for the 2011 formulation.

In QR-MAP language, poset acyclicity alone does not establish operational
causality. “Completely mixed” concerns refinement support, not a preferred
uniform distribution. Ideal compression is not a selective measurement
formula. Purification includes uniqueness, not just an enlarged description.
None of these terminological similarities is a DET proof.

## 2. Conditional reconstruction: precisely what follows

**Imported theorem.** Under the complete framework and postulates just
specified, finite systems admit the full complex quantum representation:
all density matrices, quantum effects and completely positive
trace-nonincreasing transformations. Composite systems have tensor-product
representations; reversible transformations are unitary conjugations.
The endpoint is not merely an embedding of some allowed states into matrices:
CDP's Theorem 20 and Corollary 52 establish the complete state and transformation
sets. See [section XIII.5](https://arxiv.org/html/1011.6451v3#S13.SS5).

The reconstruction theorem is credited prior mathematics. This note applies
it conditionally to the proposed residual-system interpretation; it does not
independently reprove its lengthy operational reconstruction or verify the
postulates experimentally.

In reconstructed coordinates the resulting calculus is:

\[
\rho\succeq0,\quad \operatorname{Tr}\rho=1,\qquad
0\preceq E\preceq I,\qquad p(E|\rho)=\operatorname{Tr}(\rho E),
\]

\[
\Phi_x(\rho)=\sum_\alpha K_{x\alpha}\rho K_{x\alpha}^\dagger,
\qquad \sum_{x,\alpha}K_{x\alpha}^\dagger K_{x\alpha}=I.
\]

Thus p_x=Tr Φ_x(ρ), and ρ_x=Φ_x(ρ)/p_x only for p_x>0. A positive
zero-trace output is the zero matrix. Sequential processes compose as maps;
parallel processes use tensor products. Mixed preparations, entanglement,
interference, general instruments and unitary evolution all have their usual
finite-dimensional meanings. These displayed rules are the working
representation, not extra hidden primitive inputs to the reconstruction.

An effect does not fix its instrument: both ρ↦PρP and
ρ↦Tr(Pρ)σ have effect P for any normalized σ, but different residuals.
Consequently reconstruction cannot select the measurement-update part of L.
Nor does knowing all allowed unitaries select which one occurs: identity and
Z act differently on a subsequently X-tested |+⟩ preparation. Specifying a
particular generator, clock parameter or physical coupling remains separate.

The original D premises do not imply this operational package. For example,
diagonal positive kernels with classical simplex states, stochastic processes
and ordinary classical composites form a consistent operational countermodel
to such an implication: a mixed classical state has no pure joint classical
extension, since a pure joint point mass has a pure marginal. This argument
uses only the currently admitted kernel conditions, not a hypothetical stronger
postulate that every positive matrix must be physically preparable. Such a
richness postulate would itself require an explicit new assumption.

## 3. Full quantum calculus in faithful pair-kernel coordinates

Here is a constructive correspondence for **any** finite dimension n. It is
downstream of section 2, not a claim that an arbitrary original D already
selects its physical system, algebra or operations.

Choose an orthonormal flat frame |f_r⟩ with U_ir=⟨i|f_r⟩,
|U_ir|=1/√n and U_i0=1/√n. Fourier frames suffice. Use product frames
for composites, with a fixed relabeling, to make parallel composition coherent.
Let z_i=|i⟩⟨i|, q_r=|f_r⟩⟨f_r| and h_(r,i)=q_r z_i. Then

\[
\sum_{r,i}h_{r,i}=I,\qquad
\sum_{r,i}h_{r,i}^\dagger h_{r,i}=I,
\]

and these n² histories span M_n. Their indices are formal residual possibility
labels, not preallocated future events or a growth schedule. Define

\[
J_n(\rho)_{(r,i),(s,j)}
 =\operatorname{Tr}(\rho h_{r,i}^\dagger h_{s,j})
 =\delta_{rs}U_{ir}\overline{U_{jr}}\rho_{ji}.
\tag{1}
\]

For every coefficient vector c, its quadratic form is
Tr(ρ A†A)≥0 with A=Σ c_(r,i)h_(r,i). Therefore J_n(ρ) is strongly
positive. It is linear, and its total-entry mass m(D)=Σ_ab D_ab satisfies

\[
m(J_n\rho)=\operatorname{Tr}\rho,
\qquad \sum_a(J_n\rho)_{aa}=\operatorname{Tr}\rho,
\qquad \rho_{ji}=n(J_n\rho)_{(0,i),(0,j)}.
\tag{2}
\]

The first equality follows from Σh=I, the second from Σh†h=I, and the
third uses the uniform frame column. This proves an explicit inverse:
no residual quantum information is replaced by scalar outcome probabilities.
The two normalizations coincide on this specified image, not on every D.

**Compatible-cone theorem.** Write C_n=J_n(PSD_n). For any finite quantum
instrument Φ_x:M_n→M_m, define on C_n

\[
\mathcal B_x=J_m\circ\Phi_x\circ J_n^{-1}.
\tag{3}
\]

This transports the entire finite-dimensional instrument calculus into
pair-kernel coordinates. Positivity, linearity, mixtures, branch weights and
instrument normalization follow from (1)–(2). Sequential composition follows
by cancellation of J_m^{-1}J_m. With product frames,
J_(nm)(ρ⊗σ)=J_n(ρ)⊗J_m(σ) up to the declared index reordering; linear
extension gives compatible parallel maps, including their action on correlated
inputs. Positive branches have D_x=𝓑_x(D)/m(𝓑_x(D)); zero-weight outputs
are exactly zero on this cone and are never normalized.

This is a representation theorem for the **image cones**, not a proof that
every strongly positive history kernel lies in one such compatible cone with
the intended physical meaning. General original-D operation selection remains
unresolved. The frame and the choice to represent residual systems this way
are explicit correspondence choices.

The history Gram space must not be confused with the physical system space.
Each of the n diagonal r-blocks in (1) has rank rank ρ; hence

\[
\dim H_{J_n(\rho)}=\operatorname{rank}J_n(\rho)
                    =n\operatorname{rank}\rho.
\tag{4}
\]

For a physical four-level system it is 4 for a pure state and 16 for a
full-rank state. Thus the earlier null-quotient construction alone does not
identify a fixed four-dimensional physical Hilbert space.

A recorded test can be represented before commitment by the direct sum
⊕_x 𝓑_x(D) with explicit classical outcome tags. Its total mass is one
and cross-record blocks vanish. This prepares a record-decoherent description;
it does not derive a physical decoherence mechanism or justify discarding
the residual blocks. This is a new branch-tagged carrier, not passive restriction
of the input D. Committing x stores the tag in C and retains its full normalized
block on the residual carrier.

## 4. General F once a complete law L is supplied

First state the transition without Hilbert coordinates. Let ω be a residual
operational state and u its deterministic effect. A fixed L assigns to C a
complete family of transformations τ^L_(C,β), where β contains an allowed
precursor ideal S, action/setting tags and an outcome. Set

\[
p_\beta=u(\tau^L_{C,\beta}\omega),\quad
\sum_\beta p_\beta=1,\quad
\omega^+_\beta=\tau^L_{C,\beta}\omega/p_\beta\quad(p_\beta>0).
\tag{5}
\]

F_L samples this **joint** label, appends a fresh maximal event with past S,
records its tags, and retains ω⁺. L is unchanged. A zero branch remains in
the branch description but is neither normalized nor committed. Existing
events, relations and records are untouched. The residual D is conditional
predictive data, not a claim that every old unconditioned kernel entry remains
unchanged after observing an outcome. This is a stochastic transition,
not a hidden deterministic selector or a choice of precursor by an external
scheduler.

After reconstruction, τ is represented by Φ, u by trace and ω by ρ;
equations (3) and (5) give exactly the D-coordinate version. Birth-label
invariance further requires the **full unnormalized transformations**, precursor
sets and tags to transport consistently under swaps of incomparable births.
Matching scalar probabilities alone is insufficient. These conditions define
what a lawful candidate must supply; they do not choose that candidate.

## 5. A specified candidate: L_XYZ

This is a **new**, separately scoped law, not a modification of a previously
captured source. It selects one record-growth protocol inside section 2's
ambient theory. It is not a universal controller or the whole reconstructed
theory by itself.

Choose two residual operational systems of informational dimension two,
with ports a,b. Only after reconstruction write their space as C²⊗C².
The ports are declared interfaces, not spatial coordinates or future vertices.
Allow every normalized four-level density matrix as an initial residual state.
An initial preparation is an input; L does not claim to select the universe's
initial condition.

For a committed marked poset C, let H_p be the latest committed event touching
port p, if it exists. Define the following fixed rules:

\[
\begin{split}
&A\in\{a,b,ab\},\quad w_A=1/3,\\
&S_A=\bigcup_{p\in A}\downarrow H_p,\\
&r_A=\left(\sum_{v\in S_A}x_v\right)\bmod3,\\
&\sigma_0=X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
\sigma_1=Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
\sigma_2=Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\\
&T_{A,r}=\prod_{p\in A}\sigma_r^{(p)},\qquad
P_{A,x,r}=\frac{I+(-1)^xT_{A,r}}2,\quad x\in\{0,1\},\\
&\Phi^L_{C;A,x}(\rho)=\frac13P_{A,x,r_A}\rho P_{A,x,r_A},\\
&K_L(C,\rho;A,x)=\frac13\operatorname{Tr}(\rho P_{A,x,r_A}).
\end{split}
\tag{6}
\]

Downsets are inclusive, absent heads contribute nothing and their union
counts each ancestor **once**. The context is fixed before the new outcome.
Each action also has a formal outcome ⊥ with the identically zero map and
weight zero. This is bookkeeping, not a physical third result.

F_L samples (A,x) from (6), normalizes its positive residual output, appends
one event with past exactly S_A and records (A,r_A,x). The touched heads
advance to that event. There are no uncommitted future slots, ambient birth
counter in L, independent action chooser or agency variable. Determining the
heads uses declared structural metadata; “local” here means this interface
support plus R restricted to S_A, not a stronger claim of independence from
all changing structural context.

Since T=T† and T²=I, each P is an orthogonal projector, P_0+P_1=I and
P_0P_1=0. Equation (6) is completely positive by its one Kraus operator
P/√3. Its binary action weights sum to 1/3, so all actions sum to one.
The discarded-outcome channel is generally dephasing, **not** the identity.
For ab, this is a coherent two-outcome parity readout of σ_r⊗σ_r;
it is not two separate local readouts with their results subsequently hidden.
The choice of PρP is part of L, not a theorem that an effect forces this update.

For incomparable a-only and b-only births, adding either leaves the other's
head, precursor and context unchanged. Their local projectors commute for
all nine context pairs. Hence the full unnormalized branch maps commute
on every input, including entangled states; the record tags and pasts also
transport. All births sharing a port are comparable. Adjacent incomparable
swaps therefore prove linear-extension/birth-label covariance of this law
on its generated histories. This is not Lorentz covariance.

Quantum readout changes future contexts. Nevertheless each action has marginal
1/3 independently of ρ, and the two-port order grammar has width at most two.
The model does not establish quantum-dependent precursor probabilities,
manifoldlike growth, geometrical emergence or universality of its control menu.
Axes, action weights, the modulo-three rule and interface inventory are visible
law choices, not hidden derivations from the six postulates.

## 6. A reachable imaginary-coherence witness

The preceding real X/Z-only protocol could not distinguish complex-conjugate
initial states by any recorded history: its real history operators give real
symmetric effects. L_XYZ removes that particular blindness, without claiming
that this proves its menu operationally complete.

Start at empty C with

\[
\rho^\pm=\rho_a^\pm\otimes I_b/2,\qquad
\rho_a^\pm=\begin{pmatrix}1/2&\mp i/4\\\pm i/4&1/2\end{pmatrix}.
\tag{7}
\]

These are positive, complex-conjugate states with the same computational
diagonal. Their J_4 images in a product flat frame also have identical
atomic diagonals. Compare the same recorded prefix in both runs:

1. Commit b with context X and outcome 1. Its joint weight is 1/6;
   the residual is ρ_a^±⊗P_(X−),b.
2. Commit ab with context Y⊗Y and outcome 0. Its joint conditional weight
   is 1/6, because the b-state has zero Y expectation. The prefix weight
   is therefore 1/36 in both runs.
3. Test the next a action. Both distinct residuals now share the same
   **reachable** C and context Y. The conditional Y-positive probabilities
   are 3/4 and 1/4; including the action choice, the next branch weights are
   1/4 and 1/12.

The second projector commutes with Y_a; direct expansion gives conditional
⟨Y_a⟩=±1/2 after that prefix. This proves the stated third-step values.
The full three-record history weights are 1/144 and 1/432. The residuals
at the common prefix are the actual projected states, not the unprojected
product matrices (7) artificially attached to an incompatible history.
Both prefix maps are real (X and Y⊗Y), so those conditional residuals also
remain complex conjugates with identical computational and atomic J_4
diagonals at the same reachable C. Thus diagonal-only summaries fail for
this next-record question, not only for the whole history from the initial state.

## 7. Verification and completion boundary

The small standalone [exact checker](check_law.py) verifies the newly chosen
law and displayed witnesses; it does not test whether DET implies the six
postulates or replace the general proofs above. It imports no earlier
research executor or RET implementation. All **9/9** tests pass in normal and
optimized Python; Ruff passes. The reviewed source has SHA-256
`7681bc3e36861a55176384704fb7e85a50652873aa026e8a3be115f7415a15e0`.

The exact Gaussian-rational checks compare all 18 action/context/outcome maps
on all 16 matrix units: **288 full map comparisons**, using dense projectors
and an independently written bit/phase formula. They also compare **576 full
disjoint basis compositions**, plus projector identities, normalization versus
disturbance, actual/formal zeros, probability-weighted mixtures, marked-order
swaps, same-port noncommutation and the reachable witness in section 6.
Linearity makes the matrix-unit comparisons complete map checks for these
specified finite operators; they are not an empirical test or a reconstruction
axiom proof. No growth census, sampling or new frozen capture was introduced.
The general reconstruction/encoding argument and the reachable example also
received independent read-only mathematical review; that is not formal proof
assistant verification.

From the repository root, reproduce with:

```sh
.venv/bin/python docs/validation/t8-q-operational-completion-2026-09-12/check_law.py
.venv/bin/python -O docs/validation/t8-q-operational-completion-2026-09-12/check_law.py
.venv/bin/ruff check docs/validation/t8-q-operational-completion-2026-09-12/check_law.py
```

The outcome is a **conditional reconstruction plus a specified candidate**:
the ambient finite-QM calculus has a faithful D representation and L_XYZ has
a complete joint growth/readout F. Original DET does not yet force the
operational postulates, select this L or interpret every admitted D as a
physical quantum system. Those are explicit logical boundaries, not results
that a larger finite enumeration could close.

No original axiom list, shared API, RET, clocks, book or retired κ-gravity
work changes. No geometry, coverage/noncollapse/identifiability sequel or
new QR-05 letter is opened. Option B, Status M and zero new gravity Novelty
Ledger rows remain unchanged. This note neither supplies nor claims an
empirical discriminator. No automatic successor is authorized by it.
