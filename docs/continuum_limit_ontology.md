# DET Continuum Limit — Ontologically-Correct Framing

**Date:** August 10, 2026
**Purpose:** Reframe the continuum limit proof in light of DET's ontological commitments. The proof must be consistent with Track B, not just mathematically correct.

---

## 1. Ontological Commitments That Constrain the Proof

### 1.1 The event graph is fundamental, not the manifold

**DET position:** G = (V, ≺) is the fundamental structure. The Lorentzian manifold (M, g) is an emergent approximation in the continuum limit — a useful description, not the underlying reality.

**Proof implication:** We are NOT proving "spacetime exists." We are proving that the discrete structure has a well-defined continuum approximation. The direction is discrete → continuum, not continuum → discrete.

**Correct framing:** "Under what conditions does a DET event graph admit a Lorentzian manifold approximation, and how good is that approximation?"

### 1.2 Time is record growth, not a coordinate

**DET position:** Proper time τ = Σ Π·ΔN is accumulated through discrete commit events. There is no fundamental continuous time parameter.

**Proof implication:** The continuum time coordinate t emerges from the event count density. The proper time τ along a worldline is the fundamental quantity, not the coordinate time.

**Correct framing:** "The continuum proper time between two events is the limit of Σ Π·ΔN along any chain of events connecting them."

### 1.3 κ is structural history, not a fundamental field

**DET position:** κ is accumulated per-node structural history — discrete, record-side, mutable. It is NOT a smooth field κ(x) in the fundamental theory.

**Proof implication:** The continuum field κ(x) is the coarse-grained limit of the discrete κ values. The convergence must be proven, not assumed.

**Correct framing:** "The discrete κ field, when coarse-grained over causal diamonds, converges to a smooth function κ(x) in the limit of large event count."

### 1.4 No global state — scheduler independence

**DET position:** The scheduler is a numerical gauge. No hidden global state exists. The continuum limit must be independent of scheduling choices.

**Proof implication:** The continuum limit must hold for ANY faithful sprinkling, not just one particular realization. The convergence must be in probability over the random sprinkling.

**Correct framing:** "With probability approaching 1, a randomly sprinkled DET event graph admits a Lorentzian manifold approximation."

### 1.5 Fruit-first — we only measure records

**DET position:** DET measures the fruit of becoming (records), not becoming itself. The continuum geometry is reconstructed from record data, not from any direct access to "spacetime."

**Proof implication:** The metric reconstruction must use only observable record data — causal relations (from ≺), proper time (from Π·ΔN), and matter content (from κ). No unobservable geometric primitives.

**Correct framing:** "From the observable record data (≺, Π, κ) on the event graph, a Lorentzian metric can be reconstructed that approximates the true continuum metric."

---

## 2. Reframed Lemmas

### Lemma 1 (Causal structure) — Unchanged
The causal order ≺ determines the light-cone structure. This is the standard causal set result.

### Lemma 2 (Conformal factor) — Reframed
**Original:** "Π fixes the conformal factor."
**Reframed:** "The Π-weighted event count in a causal diamond converges to the proper-time volume of that diamond. This fixes the conformal factor Ω(x) in the continuum description."

**Key insight:** We don't need Π to "equal" the conformal factor. We need the Π-weighted counting measure to converge to the volume measure. The conformal factor is the Radon-Nikodym derivative of the continuum volume with respect to the coordinate volume.

### Lemma 3 (Metric reconstruction) — Reframed
**Original:** "The reconstructed metric converges to the true metric."
**Reframed:** "From the causal order ≺ and the Π-weighted counting measure, a Lorentzian metric can be constructed that, with probability approaching 1, is close to the true metric in the LGH sense."

**Key insight:** The metric is RECONSTRUCTED from observable data. It is not "discovered" as a pre-existing entity.

### Lemma 4 (Field equations) — Reframed
**Original:** "κ-density sources the Einstein tensor."
**Reframed:** "The coarse-grained κ field satisfies, in the continuum limit, field equations that reduce to ∇²Φ = 4π G_q·ρ_γ in the Newtonian limit and to G_μν = 8π G_q·T^κ_μν in the relativistic limit."

**Key insight:** The field equations are EMERGENT — they describe how the continuum approximation behaves, not what "really exists" at the fundamental level.

---

## 3. What This Reframing Changes

### 3.1 The proof becomes statistical, not deterministic

We prove convergence **in probability** over random sprinklings, not deterministic convergence for every possible event graph. This is the standard causal set approach and is consistent with DET's no-global-state ontology.

### 3.2 The continuum is an approximation, not the truth

The Lorentzian manifold is a **useful effective description** of the discrete event graph at large scales. DET does not claim spacetime "is" a manifold — only that it behaves like one in the appropriate limit.

### 3.3 The proof direction is bottom-up, not top-down

We start from the discrete event graph and show that a continuum description emerges. We do NOT start from a continuum manifold and discretize it. (Though sprinkling into a known manifold is a useful test.)

### 3.4 Scheduler independence becomes a statistical property

The continuum limit must hold for the **ensemble** of all possible sprinklings, not for any particular one. This is stronger than proving convergence for a single sprinkling — it requires concentration inequalities.

---

## 4. What This Means for the Proof Strategy

### 4.1 The Π-volume theorem becomes: "measure convergence"

Instead of proving Π(x) → Ω(x) pointwise, we prove that the Π-weighted empirical measure converges weakly to the volume measure:

\[
\frac{1}{N} \sum_{e} \Pi_e \delta_{x_e} \rightharpoonup \Omega(x) \, d\text{vol}_g(x)
\]

This is a standard problem in empirical process theory and can be attacked with concentration inequalities.

### 4.2 The metric reconstruction becomes: "statistical reconstruction"

Instead of proving that a single reconstructed metric is close to the true metric, we prove that the **expected** reconstructed metric is close, with explicit variance bounds. This is how all statistical inverse problems are framed.

### 4.3 The field equations become: "emergent dynamics"

Instead of proving that κ "sources" gravity, we prove that the coarse-grained κ field satisfies certain PDEs in the continuum limit. The PDEs are properties of the limit, not fundamental laws.

---

## 5. Concrete Revised Proof Plan

### Step 1: Measure convergence (replaces old L2)
Prove: μ_N = (1/N) Σ Π_e δ_{x_e} converges weakly to Ω dvol_g.
- Technique: empirical process theory + concentration for Poisson processes.
- DET advantage: Π provides the weights.

### Step 2: Causal reconstruction (replaces old L3)
Prove: From (≺, μ_N), reconstruct a metric g_N such that E[d_LGH(g_N, g)] → 0.
- Technique: causal set reconstruction + LGH convergence.
- DET advantage: μ_N fixes the conformal factor.

### Step 3: κ-field convergence (replaces old L4)
Prove: The coarse-grained κ field converges to a smooth function satisfying the continuum PDE.
- Technique: discrete-to-continuum for reaction-diffusion equations.
- DET advantage: κ dynamics (recovery + diffusion) provide regularity.

### Step 4: Field equation emergence
Prove: The limit κ field satisfies G_μν = 8π G_q·T^κ_μν.
- Technique: Benincasa-Dowker action + κ coupling.
- DET advantage: κ provides the matter action.

---

## 6. Bottom Line

The ontological reframing doesn't make the proof easier — it makes it **correct**. We're not proving that spacetime exists; we're proving that the discrete event graph has a well-defined continuum approximation. The proof is statistical (convergence in probability), emergent (bottom-up from the event graph), and scheduler-independent (holds for the ensemble).

This is consistent with both Track A (physical calculus) and Track B (ontological grammar).

---

**End of Ontologically-Correct Framing**
