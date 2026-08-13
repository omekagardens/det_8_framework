# Record-Kernel Physics — Re-foundation Proposal (DET 8.1)

**Status:** Proposal / working direction (Aug 2026). This document re-founds the
Track A physical program around the commit kernel `K` as the operational center,
redefines κ as a *derived* predictive-history coordinate (not a primitive field),
introduces a pair-kernel `𝔇` as the candidate pre-commit quantum object, and
specifies the DET 8.1 theorem program (T1–T7).

It supersedes the earlier "κ-Physics" framing and the "κ-Π clock anomaly as the
sole probe" framing. The ontology (Track B) is unaffected.

---

## 1. The problem with the current κ

### 1.1 The operational estimator does not yet measure a fundamental field

The current estimator

\[
\widehat{\kappa}_{op}
=
\frac{\sum_i w_i s_i\left(z_i-f_i^{std}\right)}
{\sum_i w_i s_i^2},
\]

is a one-factor latent-variable estimator. It assumes: all residual probes
respond to one common scalar; the sensitivities `s_i` are already known; the
probe residuals share a common normalization; the scalar is sufficient to
predict effects in a held-out instrument. Until those assumptions are tested,
`κ̂_op` is not a direct measurement — it is a **fitted coordinate**. The range
`[0,1]` is consequently a calibration convention, not a discovered physical
bound. (This was especially visible in the retired gravity work, where legacy κ
profiles exceeded one.)

### 1.2 The quadratic free energy is not evidence that κ is fundamental

\[
\psi=\psi_0+\frac12 C_\kappa(\kappa-\kappa_{eq})^2
\]

should be retained only as a local constitutive model. Any smooth stable
potential has a leading quadratic term near equilibrium. The quadratic
establishes local stability, but it does not identify what κ is made of, why it
is scalar, how it composes between systems, why every realization uses the same
κ, or why κ should couple to clocks. The stiffness should be renamed `C_κ` (or
`Y_κ`) — using `K` for both the commit kernel and the structural stiffness is
actively confusing.

### 1.3 The clock test currently mixes proper time with device response

The damage protocol alters the clock apparatus or its material environment and
then looks for a frequency change. But a frequency change in a damaged clock can
always initially be interpreted as a change in the clock's effective
Hamiltonian, cavity, fields, lattice environment, transport properties, or other
device-level response. A **universal proper-time effect** is stronger: it
requires the same fractional common-mode shift in physically dissimilar clocks
or processes after their device-specific responses have been removed.

Thus the present clock experiment can test: *"Does controlled structural
history produce an unexplained oscillator shift?"* — but it cannot yet cleanly
test *"Does structural history alter proper time?"*. Gravity once offered a
second, compositionally different κ channel; its retirement leaves no
universality cross-check.

### 1.4 Present status of κ

\[
\boxed{\text{κ is currently an L0 history descriptor and an L1 latent-variable hypothesis, not a fundamental field.}}
\]

That does not make κ useless — it means κ needs a precise predictive definition
before it is placed in a universal equation.

---

## 2. A DET-native definition of κ

DET already contains the right objects to define history carrying without
importing materials physics: a causal record `R⁻`; a current state or local
record `S_e`; a possibility set `Ω_e`; a commit kernel `K_e`.

> **κ is the minimal information about the causal record that must be retained,
> beyond the present state description, to predict the next commit kernel.**

Formally, seek a compressed history coordinate `κ_e = T(R⁻_e)` satisfying

\[
K_e(\,\cdot\mid R^-_e) = K_e(\,\cdot\mid S_e,\kappa_e),
\]

with `κ_e` minimal among sufficient history summaries. Equivalently,

\[
X_{e+1}\;\perp\!\!\!\perp\;R^-_e \mid (S_e,\kappa_e).
\]

Two systems that appear identical in their present measured state nevertheless
have different future possibility/commit distributions because their histories
remain structurally active.

### 2.1 Scalar κ becomes an empirical rank claim

There is no reason to assume in advance that κ has one component. A scalar κ is
justified only when: history-conditioned residuals across independent probes are
approximately rank one; the same inferred coordinate predicts held-out probes;
its ordering is stable under changes of instrument; its evolution is
reproducible; independent systems have a defined composition rule.

Possible outcomes are informative: **rank zero** (present variables are
state-complete; κ is unnecessary); **rank one** (a scalar κ is supported);
**rank r > 1** (structural history is a vector/tensor); **nontransportable
residuals** (each probe has its own nuisance history variable, no universal κ).
**This rank test should precede the clock experiment.**

### 2.2 A canonical operational distance

For two preparations `h_a`, `h_b` matched on all present measured variables `S`,
estimate their future outcome kernels `K_a(x)=K(x|S,h_a)`, `K_b(x)=K(x|S,h_b)`.
The normalized Fisher–Rao history distance is

\[
\boxed{
\kappa(h_a,h_b\mid S)
=
\frac{2}{\pi}
\arccos\left[\sum_{x\in\Omega}\sqrt{K_a(x)K_b(x)}\right]
}
\]

with `0 ≤ κ ≤ 1`. Interpretation: `κ=0` ⇒ identical future kernels; `κ=1` ⇒
disjoint future supports; intermediate values quantify retained predictive
distinction. For nearby kernels the local quadratic form is the Fisher metric,

\[
d\kappa^2 \propto \sum_x \frac{(dK_x)^2}{K_x}.
\]

The Fisher metric is not arbitrary: on classical probability spaces it is, up to
scale, the canonical Riemannian metric monotone under stochastic coarse-graining.

### 2.3 Why this is better than "fraction of locked degrees of freedom"

It is directly estimated from raw outcome counts; independent of the microscopic
material carrier; meaningful for materials, biological regimes, stochastic
devices, clocks, and quantum experiments; zero exactly when history has no
remaining predictive consequence; naturally connected to `K` (DET's actual
operational primitive); compatible with scalar, vector, or higher-rank history
structure. Defect density may generate a nonzero κ — so may residual stress,
hidden chemical configuration, glassy memory, relational network structure, or
an unknown field. κ no longer claims in advance which carrier is responsible.
The physical interpretation comes **after** measuring the predictive history
distance.

### 2.4 Recovery can be derived rather than imposed

Under a common information-losing stochastic channel `T`,
`K_a ↦ TK_a`, `K_b ↦ TK_b`, distinguishability cannot increase:

\[
\kappa(TK_a,TK_b)\le\kappa(K_a,K_b).
\]

Recovery is *contraction of history-conditioned future kernels toward one
another*. If the channel has contraction coefficient `0 < η < 1`, then
`κ_{n+1} ≤ η κ_n`, and exponential relaxation follows, `κ_n ≲ κ_0 e^{−n/n_rec}`.
The recovery time is derived from the channel's contraction/spectral
properties — not postulated as a universal ODE.

---

## 3. The missing quantum object is not another scalar

The commit kernel `K : Ω → [0,1]` contains ordinary probabilities. Once only
`K(i)` is known, relative phases and interference information have already been
discarded. That is why defining arbitrary roots `K(i)=|c_i|^2` cannot derive
quantum mechanics — infinitely many phase choices produce the same `K`. DET
needs a **pre-commit relational object** containing relations between
alternatives.

### 3.1 Proposed pair-kernel

Introduce a local history/possibility pair-kernel

\[
\mathfrak D_e : \mathcal A_e \times \mathcal A_e \to \mathbb C,
\]

where `A_e` is the event algebra generated by `Ω_e`. Require Hermiticity
`𝔇(A,B) = conj(𝔇(B,A))`, biadditivity `𝔇(A⊔B,C)=𝔇(A,C)+𝔇(B,C)` for disjoint
`A,B`, `𝔇(Ω,Ω)=1`, and strong positivity `[𝔇(A_i,A_j)]_{ij} ⪰ 0`. Define the
quadratic possibility weight `μ(A)=𝔇(A,A)`. A partition `𝒫={A_i}` becomes
commit-ready when its alternatives are record-distinguishable
(`𝔇(A_i,A_j)≈0` for `i≠j`). Only then does an ordinary commit kernel emerge:

\[
\boxed{K_{\mathcal P}(i)=\mathfrak D(A_i,A_i)},\qquad \sum_i K_{\mathcal P}(i)=1.
\]

Clean distinction: `𝔇` = relational possibility structure before commit;
`K_𝒫` = ordinary probabilities for a recordable partition; `X_e` = the
committed outcome; `R⁺` = the resulting record.

### 3.2 What this quadratic derives

Biadditivity immediately yields the absence of irreducible third-order
interference, `I_3 = μ(A∪B∪C) − μ(A∪B) − μ(A∪C) − μ(B∪C) + μ(A) + μ(B) + μ(C) = 0`.
Pairwise interference remains (`2 Re 𝔇(A,B)` need not vanish). Strong positivity
gives a Gram representation `𝔇(A,B)=⟨v_A,v_B⟩`, so `μ(A)=‖v_A‖²`; the
norm-squared form appears as a representation theorem rather than being inserted
as `K=|c|²`. This structure is closely related to **quantum measure theory and
decoherence functionals** (Sorkin et al.); DET must credit that prior framework
explicitly rather than present the mathematics as unprecedented.

### 3.3 Why this can still be DET-native

Using known mathematics is not smuggling; smuggling is inserting a known
physical result and relabeling it. The DET-native question is: *can the axioms
of 𝔇 be forced by record growth, alternative composition, positive
commitability, and the absence of irreducible higher-order relational
constraints?* The target theorem:

\[
\text{record relationality} + \text{composition} + \text{positive commitability}
\Longrightarrow \text{strongly positive grade-2 pair-kernel}.
\]

### 3.4 What it does not yet derive

Three problems remain open. **(i) Complex field selection** — why `ℂ` and not
`ℝ`, quaternions, or another algebra (a possible program: decompose
`𝔇=G+iΩ` with `G` symmetric and `Ω` antisymmetric, then prove reversible
relational dynamics generate a complex structure `J²=−I`). **(ii) Exact Born
rule** — the Gram representation gives a norm-squared commit theorem, but the
full Born rule additionally requires the event/projector structure, allowable
measurements, state transformations, and cross-context consistency.
**(iii) Exact quantum correlation set** — strong positivity + composition do not
automatically isolate the standard quantum set; "almost quantum" structures can
arise. Hence CHSH `2√2` cannot be claimed merely by choosing a Bell vector and
standard rotations. A candidate DET-specific condition is *global record
extendability* (`𝔇_n = Marginal(𝔇_{n+1})` for every lawful future refinement).

---

## 4. Revised minimal Track A architecture

**Primitives:** `(V,≺)` causal event order; counting measure `#`; local
committed record `R`; law map `L` (generates lawful alternatives and relational
constraints); pair-kernel `𝔇` (candidate); local composition and commit
operation.

**Derived:** `K_𝒫` (diagonal of `𝔇` on a decoherent/recordable partition);
kernel roots/amplitudes (Gram coordinates of `𝔇`, not primitives); κ (minimal
predictive history coordinate); scalar κ (norm along a rank-one history mode);
`Π_a` (tick/commit intensity of process `a` relative to causal event count);
proper time (order-and-count geometry in a manifoldlike limit); classical
probability (diagonal/decohered limit); diffusion/relaxation (local limits of
`K`); entropy production (forward/reverse path-kernel ratio).

The revised generative chain:

\[
\boxed{
R^-_e \xrightarrow{L} (\Omega_e,\mathcal A_e,\mathfrak D_e,\mathcal C_e)
\xrightarrow{\text{recordable partition}} K_{e,\mathcal P}
\xrightarrow{\text{commit}} X_e \to R^+_e
}
\]

κ is no longer placed between record and reality as an unexplained substance;
it is derived afterward as a measure of how history changes the generated kernel.

---

## 5. Reconstructing known physics without importing the Standard Model

DET should initially target *structural* phenomena (not masses, gauge groups,
gravity, or cosmological parameters): **classical probability as the committed
limit**; **two-path interference and `I_3=0`**; **quadratic commit weights**
(Gram representation, not yet "Born rule derived"); **reversible evolution**
(isometries → one-parameter unitary form `U(τ)=e^{−iHτ}`, with `H` still to be
produced by `L`); **path irreversibility and fluctuation relations**
(`Σ[ω]=log(P_F/P_R)`, `⟨e^{−Σ}⟩=1`, `⟨Σ⟩≥0`); **diffusion/relaxation** (graph
Laplacian from locality + normalization + weak incremental updating);
**pointer records from redundancy** (`P_error(N) ≤ e^{−NC}`); **causal geometry
from order and count** (separating estimator verification on known sprinklings
from genuine emergence); **Bell/Tsirelson** (kept as correspondence, no Bell
state or Pauli rotation inserted).

**What DET cannot yet derive** (and should not claim): Standard Model gauge
group; particle generations; masses/couplings; Maxwell; Einstein; dark matter;
the dimension `3+1`; a specific physical Hamiltonian.

---

## 6. Derivation certificates (replace anti-smuggling percentages)

Every claimed derivation should carry a machine-readable certificate: **Inputs**
(exact primitives, allowed mathematical theorems, empirical constants only for
units, initial/boundary conditions); **Forbidden dependencies** (Hilbert space,
complex amplitudes, Lorentzian metric, standard Hamiltonian, Newtonian/Einstein
field equations, SM symmetries, target observable formula — unless
reconstructed); **Theorem statement** (`A_1,…,A_n ⇒ O`); **Uniqueness statement**
(could alternative lawful structures produce a different result?); **Adversary
models** (classical stochastic, higher-order interference, non-strongly-positive
pair-kernel, non-manifoldlike graph, multidimensional history); **Empirical
interface** (only raw observations: settings/outcomes, timestamps,
adjacency/precedence, counts, oscillator frequencies, measured probe values);
**Classification** — `MATH` (imported mathematics, attributed), `AX-DET`
(DET-specific axiom), `TH-DET` (theorem from DET axioms), `CORR`
(correspondence after importing physical structure), `FIT` (phenomenological
fit), `PR` (pre-registered prediction), `EV` (empirically validated).

Examples: Bell state + rotations = `CORR`; Minkowski sprinkling + recovered
metric = `CORR`; pair-kernel axioms ⇒ `I_3=0` = `TH-DET` (once the axioms are
justified); commit path ratio ⇒ `⟨e^{−Σ}⟩=1` = `TH-DET`; local symmetric kernel
⇒ graph diffusion = `TH-DET`; clock shift fit to `λ_P κ` = `FIT/PR`.
Borrowed mathematics is celebrated and cited; borrowed physical premises are
exposed.

---

## 7. A better data strategy

DET does not need another large astronomy dataset. The new program uses datasets
whose raw structure matches DET primitives: **(7.1) matched-state,
different-history datasets** (test `H₀: K_a = K_b`; then held-out transport —
a κ inferred from probes A,B predicting probe C is the decisive test for a
common history coordinate); **(7.2) alternative-combination datasets** (compute
`I_2`, `I_3` from raw counts with one/pairs/triples of alternatives open);
**(7.3) sequential setting/outcome datasets** (ingest as
`(causal order, setting, outcome, record context)`); **(7.4) forward/reverse
trajectory datasets** (test `Σ[ω]=log(P_F/P_R)`); **(7.5) redundant-record
datasets** (cross-check the commit-channel error exponent).

---

## 8. Rebuild the clock program around common-mode universality

The clock experiment is a late-stage test, not the first operational definition
of κ. Model `y = Bκ + u·1 + ε`, where `Bκ` is device-specific history response,
`u` is a universal common-mode proper-time effect, `ε` is noise/systematics.
The program: infer κ from independent non-clock probes; calibrate
device-specific responses on ordinary oscillators; compare materially and
physically dissimilar clock mechanisms; test for a residual common mode `u`;
interpret only `u` as a candidate Π/proper-time effect. Under this model the
formula `τ_A/τ_B = (1+λ_P κ_B)/(1+λ_P κ_A)` is a special rank-one,
universal-coupling limit that must be **earned empirically**.

Redefine Π as a process-specific tick intensity,

\[
\Pi_a(e) = \lim_{\Delta N\to\infty} \frac{\mathbb E[\Delta N_a \mid R_e]}{\Delta N},
\]

where `N` is causal event/volume count and `N_a` the number of ticks of process
`a`. A universal proper-time rate exists only if calibrated ideal processes
share a common geometric component. This prevents `σ, η, F, H, φ(v)`, and κ
from being multiplied together without derivation.

---

## 9. Immediate corrections (applied Aug 2026)

1. **Governance sync** — GOVERNANCE.md no longer claims Born/CHSH/Lorentz/gravity
   are "derived", no longer lists κ-gravity as active, and no longer promises a
   clock/gravity anomaly validates DET. ✓ applied.
2. **Retire gravity from the active physics surface** — moved to
   `archive/retired_kappa_gravity.md`. ✓ applied.
3. **F12 reconsidered** — reformulated participation-only (κ-gravity retired);
   "gravitational binding" removed from its remaining work. ✓ applied.
4. **κ demoted** — primitive table now lists κ as an L0/L1 fitted coordinate
   (rank-one special case), not a primitive field. ✓ applied.
5. **Kernel roots demoted** — pair-kernel `𝔇` added as the candidate primitive;
   roots become Gram coordinates (CORR). ✓ applied.
6. **Program renamed** — "Record-Kernel Physics" (four sectors). ✓ applied.

---

## 10. DET 8.1 theorem program

- **T1 — Predictive History Sufficiency.** Prove/implement
  `K(·|R⁻) = K(·|S,κ)`. Deliverables: latent-rank test, cross-probe transport
  test, scalar/vector decision gate, Fisher–Rao operational metric.
- **T2 — Quadratic Commit Theorem.** From pair-kernel axioms: grade-two
  additivity, `I_3=0`, Gram representation, nonnegative committed weights,
  classical additivity on decoherent partitions, composition closure. (Not yet
  "Born rule".)
- **T3 — Record Formation Theorem.** Repeated weak commits ⇒
  `P_record_error(N) ≤ e^{−NC}`, connecting redundancy to suppression of
  pair-kernel cross terms.
- **T4 — Kernel Irreversibility Theorem.** `⟨e^{−Σ}⟩=1`, `⟨Σ⟩≥0`, including
  conditions for absolute irreversibility and incomplete reverse support.
- **T5 — Local Kernel Continuum Theorem.** When local conservative graph kernels
  converge to diffusion / drift-diffusion / reversible wave-like evolution; all
  continuum coefficients from discrete-kernel moments.
- **T6 — Correlation-Class Theorem.** Characterize all bipartite distributions
  generated by lawful local pair-kernels (classical / quantum / almost-quantum /
  no-signalling). Only afterward optimize CHSH.
- **T7 — Order-and-Count Geometry.** Separate estimator verification from genuine
  emergence: `(≺, #, L, 𝔇) ⇒ stable manifoldlike Lorentzian geometry`. Gravity
  stays out of scope until this kinematic theorem succeeds.

---

## Final answer to the κ question

**What is κ?** The best definition:

\[
\boxed{
\kappa = \text{the minimal predictive compression of the causal record that remains necessary to determine the present commit kernel}
}
\]

A scalar κ exists only when that retained history is empirically rank one.
Operationally, κ is measured as a distance between history-conditioned future
kernels — not as an assumed fraction of locked degrees of freedom.

**Does DET need another fundamental quantity?** Not another free scalar. DET
needs: the commit kernel `K` as the operational center; an order/count measure
for spacetime reconstruction; a pair-kernel `𝔇(A,B)` for pre-commit relational
interference.

**Does DET need a fundamental quadratic?** Yes — but a structured quadratic: the
Fisher quadratic on changes of `K` (making κ operational), and the pair-kernel
quadratic `μ(A)=𝔇(A,A)` (supporting interference and norm-squared commit
weights). These may be two faces of one geometry: `𝔇` supplies the relational
state structure, and its induced information geometry supplies κ.

The central reorganization:

\[
\boxed{
R^- \to (\Omega,\mathfrak D) \to K_{\mathcal P} \to X \to R^+,
\qquad
\kappa = \text{derived history dependence of } K
}
\]
