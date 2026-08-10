# DET Continuum Limit — Formal Proof Roadmap

**Date:** August 10, 2026
**Status:** L1 proven. L2-L3 numerical evidence. L4 sketch.
**Target:** CT (Continuum Theorem) — manifoldlikeness + metric convergence + curvature convergence.

---

## 1. What Must Be Proved

**Theorem (DET Continuum Limit):** Let (M, g) be a smooth (d+1)-dimensional Lorentzian manifold with bounded geometry. Let G_N be a DET event graph obtained by faithful sprinkling of N events into (M, g) with density ρ, where each event carries Π and κ values. Then as N → ∞, with probability approaching 1:

1. The causal structure of G_N converges to that of (M, g).
2. The coarse-grained Π field converges uniformly to the conformal factor Ω(x).
3. The reconstructed metric g_N converges to g in the Lorentzian Gromov-Hausdorff topology.
4. The discrete field equations converge to G_μν = 8π G_q · T^κ_μν.

---

## 2. Current Status

| Lemma | Status | Next step |
|---|---|---|
| L1 | **Proven** (causal set theory, Bombelli+1987) | — |
| L2 | Numerical evidence (α=0.37–0.50) | Uniform convergence proof |
| L3 | Statistical convergence (CV 0.56→0.25) | LGH embedding + distance proof |
| L4 | Newtonian verified | Discrete action definition + convergence |

---

## 3. Process for Formal Proof

### 3.1 What DET Can Do (with DET's unique resources)

**a) Π-volume measure theorem (DET-specific)**

Define the Π-weighted counting measure on the event graph:

\[
\mu_N(A) = \sum_{e \in A} \Pi_e
\]

Prove: as N → ∞, μ_N(A) / N → (1/vol(M)) ∫_A Ω(x) √|det g| d^{d+1}x.

This uses DET's unique Π field. Bare causal sets cannot do this — they have only event counts, not Π-weighted counts.

**b) κ-source convergence (DET-specific)**

Prove: the coarse-grained κ field converges to the continuum matter density:

\[
\kappa_N(x) \to \kappa(x) \quad \text{in } L^1_{loc}(M)
\]

This uses DET's unique κ field. Bare causal sets have no native matter content.

**c) Bond Laplacian → spatial ∇² (DET-specific)**

Prove: the graph Laplacian on the bond network converges to the spatial Laplacian:

\[
\Delta_{\text{disc}} \to \nabla^2 \quad \text{as } N \to \infty
\]

This uses DET's bond network. Bare causal sets have only the causal order, no spatial connectivity.

### 3.2 What Requires External Mathematics

**d) Lorentzian Gromov-Hausdorff convergence (shared with causal set theory)**

Use the Minguzzi-Suhr (2019+) framework for LGH distance. Prove that the reconstructed metric spaces converge in LGH topology. This is the hardest part and is shared with the causal set theory program.

**e) Benincasa-Dowker action convergence (shared with causal set theory)**

If using the BD action: prove that its expectation converges to the Einstein-Hilbert action under sprinkling. Numerical evidence exists (Benincasa+Dowker 2010+). Rigorous proof is open.

**f) Measure concentration (probability theory)**

Prove that the probability of large deviations from the continuum limit decays exponentially with N. Requires concentration inequalities for dependent random variables (sprinkled events are Poisson, not i.i.d.).

---

## 4. Concrete Next Steps (Priority Order)

### Step 1: Π-volume measure theorem (DET-specific, doable)

- Define μ_N precisely on the event graph
- Prove μ_N(A)/N → (1/vol)∫_A Π(x) √|g| for nice sets A
- Use Poisson process properties (sprinkling → spatial Poisson process)
- Estimate convergence rate via concentration inequalities
- **Effort:** 3-6 months for a skilled probabilist
- **DET advantage:** Π provides the weight; bare causal sets have only counts

### Step 2: Bond Laplacian convergence (DET-specific, doable)

- Define the graph Laplacian on the bond network
- Prove Δ_disc f → ∇² f for smooth test functions f
- Use the known convergence of graph Laplacians on random geometric graphs
- **Effort:** 2-4 months
- **DET advantage:** Bond network provides the spatial structure

### Step 3: κ-source convergence (DET-specific, doable)

- Define coarse-graining of κ over causal diamonds
- Prove L¹_loc convergence to continuum κ(x)
- Use the regularity of κ from the recovery-diffusion equation
- **Effort:** 2-4 months
- **DET advantage:** κ is a native field with known dynamics

### Step 4: LGH metric convergence (shared, hard)

- Implement the Minguzzi-Suhr LGH distance for DET graphs
- Prove that the LGH distance between (M, g) and G_N → 0 as N → ∞
- Requires Steps 1-3 as prerequisites
- **Effort:** 1-2 years, likely requires collaboration with causal set theorists
- **DET advantage:** Steps 1-3 provide the conformal factor and matter that bare causal sets lack

### Step 5: Discrete action → Einstein-Hilbert (shared, very hard)

- Define S_DET on the event graph (candidate: κ-weighted BD action)
- Prove convergence to S_EH + S_κ under sprinkling
- Derive discrete equations of motion
- Prove discrete Bianchi identity
- **Effort:** 2-5 years, major research program
- **DET advantage:** κ provides the matter action natively

---

## 5. What Can Be Done Now (Without External Collaboration)

1. **Complete Π-volume measure numerical verification** — already done (L2, α=0.50 convergence).
2. **Complete bond Laplacian numerical verification** — already done (graph Laplacian = ∇² exactly for polynomials).
3. **Complete κ-source numerical verification** — already done (SPARC 135 galaxies, solar system, clusters).
4. **Write the theorem statements precisely** — already done (continuum_limit_proof.py).
5. **Publish the numerical evidence as a pre-registered theorem program** — the four lemmas with their current status form a complete research proposal.

---

## 6. What Requires External Collaboration

1. **LGH convergence proof** — needs a differential geometer familiar with Minguzzi-Suhr framework.
2. **Benincasa-Dowker action convergence** — needs a causal set theorist.
3. **Measure concentration bounds** — needs a probabilist.
4. **Formal proof assistant verification** — once the proofs exist, formalizing them in Lean/Coq.

---

## 7. Realistic Timeline

| Timeframe | Milestone |
|---|---|
| 0-6 months | Π-volume theorem (DET-specific, doable with current team) |
| 6-12 months | Bond Laplacian + κ-source convergence (DET-specific) |
| 1-2 years | LGH metric convergence (requires collaboration) |
| 2-5 years | Discrete action → Einstein-Hilbert (major program) |

---

## 8. What DET Uniquely Contributes

Bare causal set theory cannot complete the continuum limit because:
- No conformal factor (Π provides this)
- No matter content (κ provides this)
- No spatial metric (bonds provide this)

DET turns the causal set continuum limit from an underdetermined problem into a determined one. The missing pieces are mathematical technique (LGH, concentration, BD action), not physical content.

---

**End of Formal Proof Roadmap**
