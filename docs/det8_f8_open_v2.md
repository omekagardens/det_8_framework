# DET v8.0-P0.4 — F8-OPEN v2: Becoming-Imprint Protocol

**Status:** P/A (proposed core with adversarial constraints)
**Date:** August 9, 2026
**Purpose:** Transform the F8-OPEN falsifier from a philosophical challenge into an executable research protocol with adversary classes, candidate signatures, null models, pre-registration templates, and automatic downgrade rules.

---

## 1. The F8-OPEN Challenge (Restated Precisely)

DET 8 claims that the future is ontologically open: where \(|\Omega_e| > 1\), no fact of the matter exists as to which successor will become actual before the actualization event.

A skeptic proposes a **Hidden Deterministic Emulator (HDE)**: a model that, given the same complete causal-past record \(\mathcal R^-_e\), produces a *unique* successor \(X^\star_e\) via a hidden rule \(f\):

\[
X^\star_e = f(\mathcal R^-_e, \lambda_e)
\]

where \(\lambda_e\) is a local hidden variable inaccessible to measurement but fully determinate.

F8-OPEN demands that DET either:

- **(a) Produce a discriminator**: an operationally testable prediction that differs between DET's open actualization and any HDE with an equivalent predictive kernel, or
- **(b) Honest downgrade**: restrict "open becoming" to metaphysical status (M) and acknowledge that the distinction between openness and hidden determinism is empirically empty.

This protocol formalizes both paths.

---

## 2. Adversary Classes

Each adversary class represents a distinct way to produce the same observable statistics as DET without ontological openness.

### 2.1 D0 — Hidden Deterministic Emulator (HDE)

**Claim:** Every actualization event is strictly deterministic. The appearance of openness arises from ignorance of hidden variables.

**Mechanism:**
\[
X^\star_e = f(\mathcal R^-_e, \lambda_e)
\]
where \(\lambda_e\) is a local hidden variable.

**Constraints:**
- Produces identical predictive kernel \(K_e\) to DET.
- Satisfies all conservation and causal-locality constraints.
- May use hidden variables that are inaccessible by construction.

**What it does NOT explain:**
- Why \(|\Omega_e| > 1\) should ever arise if the dynamics are fundamentally single-valued.
- The origin of the apparent "choice" structure (why Nature bothers to generate a set of alternatives only to deterministically pick one).

**Testability:** By construction, empirically indistinguishable from DET in any local measurement.

---

### 2.1 D1 — Fundamental Stochastic Emulator (FSE)

**Claim:** Actualization is a genuine chance process with ontic probabilities, but there is no "present" or "becoming" — outcomes are randomly sampled from the kernel.

**Mechanism:**
\[
X^\star_e \sim K_e(\cdot \mid \mathcal R^-_e)
\]

**Constraints:**
- Same kernel as DET.
- No hidden variables beyond the kernel.
- Genuine randomness, not determinism + ignorance.

**What it does NOT explain:**
- Why the "collapse" or "commit" is irreversible in a way that pure chance would not require.
- Why the record grows (stochastic models typically are time-symmetric at the micro level).

**Testability:** Also empirically indistinguishable from DET in standard measurement statistics.

---

### 2.3 D2 — Many-Worlds / Branching Emulator (MWE)

**Claim:** All outcomes in \(\Omega_e\) are realized in decohering branches. The appearance of a single outcome is indexical (we only experience one branch).

**Mechanism:**
\[
|\Psi\rangle \rightarrow \sum_{X \in \Omega_e} |X\rangle \otimes |\text{env}_X\rangle
\]
where all branches are physically real.

**Constraints:**
- Reproduces Born rule probabilities (via decision theory, branch counting, or other arguments).
- No collapse; everything is unitary.

**What it does NOT explain:**
- Why the Born rule holds with the specific functional form \(p(X) = |\langle X|\Psi\rangle|^2\).
- Why we experience a single classical outcome rather than a superposition.
- Why the record appears to be determinate and singular.

**Testability:** Empirically indistinguishable without access to other branches.

---

### 2.4 D3 — Superdeterministic Emulator (SDE)

**Claim:** The measurement setting and the system state share common causes in the past, such that all correlations (including Bell violations) arise deterministically.

**Mechanism:**
\[
P(a, b \mid x, y) = \sum_\lambda P(\lambda) P(a \mid x, \lambda) P(b \mid y, \lambda)
\]
where \(\lambda\) is correlated with \(x\) and \(y\) via past common causes.

**Constraints:**
- Violates Measurement Independence (a Bell premise).
- Preserves causal locality (no superluminal signalling).
- Indistinguishable from quantum mechanics in any finite experiment if the common-cause mechanism is sufficiently opaque.

**What it does NOT explain:**
- Why the apparent "free choice" of measurement settings produces exactly the quantum correlations.
- Why Nature conspires to hide the deterministic mechanism so thoroughly.

**Testability:** By construction, indistinguishable unless we can prove Measurement Independence (which may be circular).

---

### 2.5 Summary Table

| Class | Open? | Hidden Vars? | Distinguishable from DET? |
|---|---|---|---|
| D0 (HDE) | No | Yes (local) | By construction: NO |
| D1 (FSE) | No (stochastic) | No | By construction: NO |
| D2 (MWE) | No (all outcomes real) | No | Without branch access: NO |
| D3 (SDE) | No | Yes (global) | Without MI proof: NO |
| **DET** | Yes | No | — |

---

## 3. Candidate Signatures

If DET is to satisfy F8-OPEN path (a), it must identify at least one candidate signature that could distinguish genuine openness from ALL adversary classes. The following are candidates under investigation.

### 3.1 S1 — Record Growth Asymmetry

**Claim:** If actualization genuinely creates new facts, the total amount of committed record should exhibit a fundamental growth asymmetry that is not derivable from any time-symmetric microscopic law plus initial conditions.

**Proposed measure:**
\[
\Gamma(t) = \sum_{e: \tau(e) \leq t} \mathbb{I}[|\Omega_e| > 1]
\]
where \(\Gamma(t)\) counts the cumulative number of open-support events that have been resolved.

**Null model (HDE/D1/D2):** \(\Gamma(t)\) is a function of initial conditions and deterministic/stochastic propagation. It should be possible (in principle) to explain \(\Gamma(t)\) as a consequence of the initial state plus known dynamics.

**DET prediction:** After accounting for all known record-side dynamics, \(\Gamma(t)\) exhibits an irreducible excess that cannot be explained by initial conditions or by any time-symmetric propagation law. The excess represents genuinely new facts.

**Status:** Speculative. No operational measure of "irreducible excess" exists.

---

### 3.2 S2 — Failure of Retroactive Compressibility

**Claim:** A sequence of open-support actualizations cannot be losslessly compressed into an equivalent deterministic initial-condition-plus-propagation description without the compression itself encoding the outcomes (which would be circular).

**Proposed test:** For a system undergoing \(N\) open-support events, attempt to find a set of initial conditions and deterministic rules that reproduce the exact sequence of committed outcomes. If no such compression exists that is substantially smaller than the sequence itself, the sequence carries irreducible new information.

**Null model (HDE):** There exists a compact hidden-variable description that generates the sequence.

**DET prediction:** For sufficiently complex agent-involving systems, no compact HDE exists.

**Status:** Requires formalization of "compact" and "agent-involving." Related to Kolmogorov complexity.

---

### 3.3 S3 — Agent-Involving Unpredictability

**Claim:** In systems where selfhood-bearing regimes (agents) participate, the statistical properties of outcomes differ from what any HDE or FSE can produce, specifically in their temporal correlation structure.

**Proposed test:** Compare the autocorrelation structure of agent-involving time series against the best-fit HDE or FSE. Look for:
- Excess long-range correlations.
- Non-Markovian structure not explainable by hidden-state models.
- "Creative" pattern shifts that resist state-space modeling.

**Null model:** The best HDE/FSE fit to the data is statistically indistinguishable from the data.

**DET prediction:** Agent-involving series exhibit statistically significant excess structure beyond the best HDE/FSE fit.

**Status:** Requires specifying what constitutes "agent-involving" in operational terms. Currently circular: we identify agents by the very unpredictability we're trying to measure.

---

### 3.4 S4 — Violation of Leggett-Garg / Macrorealism

**Claim:** If becoming creates facts, the Leggett-Garg inequality (which assumes macrorealism: a system always has a definite value of a macroscopic observable) may be violated in a way that is not merely quantum but specifically reflects fact-creation.

**Proposed test:** Extend Leggett-Garg tests to systems where "becoming" is claimed to be active. Look for violations that exceed what quantum coherence alone predicts.

**Null model:** Quantum mechanics fully accounts for all Leggett-Garg violations.

**DET prediction:** Systems with genuine becoming exhibit excess Leggett-Garg violation beyond quantum predictions.

**Status:** No quantitative DET prediction exists. QM already violates Leggett-Garg.

---

### 3.5 S5 — Irreducible Commit-Lag Signature

**Claim:** The commit map has a finite causal lag. During the interval between the start of actualization and the completion of commit, the record is in an intermediate state. This "commit window" may produce detectable signatures in finely timed correlation experiments.

**Proposed test:** Ultra-high-precision timing measurements on quantum measurement events, looking for a brief interval where the pointer record is not yet classically stable.

**Null model:** Collapse is instantaneous; any timing spread is due to detector physics, not ontology.

**DET prediction:** A finite, non-zero commit lag exists and produces distinct temporal correlation signatures.

**Status:** Currently beyond experimental resolution for most systems.

---

## 4. Null Models

### 4.1 NM-HDE — Hidden Deterministic Null Model

A fully deterministic emulator that:
- Takes the identical initial record \(\mathcal R^-_e\).
- Uses a hidden rule \(f_\lambda\) (possibly a cryptographic hash seeded by \(\lambda\)).
- Produces a single outcome \(X^\star_e\).
- The rule \(f_\lambda\) is chosen so that the empirical distribution matches DET's kernel \(K_e\) over ensembles.

**How to falsify:** Show a statistical pattern (in a single trajectory or ensemble) that no such \(f_\lambda\) can produce.

**Current status:** No such pattern is known.

---

### 4.2 NM-FSE — Fundamental Stochastic Null Model

Same as NM-HDE but uses genuine randomness instead of hidden determinism.

**How to falsify:** Same difficulty as NM-HDE. Adding "genuine randomness" makes the null model even harder to reject, since it can match any probability distribution.

**Current status:** No discriminator known.

---

### 4.3 NM-MWE — Many-Worlds Null Model

All branches are real. Our experience of a single outcome is indexical.

**How to falsify:** Inter-branch interference effects? If "other branches" are real, they might produce detectable interference that DET (with a single actualized branch) would not. But standard decoherence already suppresses this.

**Current status:** No discriminator known.

---

## 5. Pre-Registration Template

Any proposed F8-OPEN discriminator must be pre-registered with the following structure:

```
F8-OPEN Pre-Registration: [DISCRIMINATOR NAME]
Date: [YYYY-MM-DD]
Proposer: [Name/Institution]

1. HYPOTHESIS
   H_DET: [Specific DET prediction for record-level observables]
   H_0:   [Specific null-model prediction]

2. SYSTEM
   [Description of the physical system or simulation]

3. OBSERVABLE
   [Precise definition of the measurable quantity]

4. STATISTIC
   [The test statistic and its distribution under H_0]

5. THRESHOLD
   [Rejection threshold for H_0, including significance level α]

6. SAMPLE SIZE
   [Required number of trials/events, with power analysis]

7. ADVERSARY CLASSES
   [Which adversary classes this discriminator targets]

8. FAILURE CONDITION
   [What outcome constitutes failure to reject H_0]

9. DOWNGRADE OBLIGATION
   [If H_0 cannot be rejected, what downgrade is triggered]
```

---

## 6. Automatic Downgrade Rule

If no candidate discriminator survives pre-registered testing by the end of the P0.4 cycle:

> **Rule DG-OPEN:** The claim "the future is ontologically open" shall be reclassified from status P (proposed core) to status M (metaphysical/interpretational). The formal machinery of \(\Omega_e\), \(K_e\), and \(\operatorname{Commit}\) shall be retained as a calculational framework, but the ontological commitment to genuine becoming shall be explicitly flagged as empirically unsupported.

This downgrade does NOT:

- Remove \(\Omega_e\), \(K_e\), or \(\operatorname{Commit}\) from the formal core (they remain useful calculational structures).
- Invalidate DET's local, record-determinate, conservation-preserving architecture.
- Remove the No Pre-Existing Future Facts invariant (it remains a regulatory principle even if empirically undiscriminated).
- Affect the agency quarantine (agency is already M).

This downgrade DOES:

- Prevent any claim that DET has empirically established ontological openness.
- Require all P0.4 documents to carry a warning: "Openness is a metaphysical interpretation pending a successful F8-OPEN discriminator."
- Shift research priority away from becoming-imprint discovery and toward formal completeness of the record-side model.

---

## 7. Current Assessment (August 2026)

**Status:** No candidate discriminator has yet been pre-registered.

**Honest assessment:** All adversary classes (D0-D3) are, by construction, empirically indistinguishable from DET in all currently feasible experiments. The candidate signatures (S1-S5) are speculative and none has a concrete, testable formulation.

**Recommendation for P0.4:** Unless a concrete discriminator is formulated before the P0.4 draft, DG-OPEN should be applied preemptively: F8-OPEN should be declared unsatisfied, and "open becoming" should be tagged M in the P0.4 card. This is the epistemically honest position and strengthens DET's credibility for its falsifiable, record-side claims.

**Path forward:** The most promising long-term direction is S2 (failure of retroactive compressibility), coupled with S3 (agent-involving unpredictability). If a rigorous measure of "irreducible sequence complexity" can be defined and linked to agent-involving systems, this could become a viable discriminator. But this is a multi-year research program, not a P0.4 deliverable.

---

**End of F8-OPEN v2 Protocol**

*This document implements the adversary-class structure and downgrade protocol required by AGENTS.md Workstream C. The honest answer for P0.4 is: no discriminator currently exists, and DG-OPEN should be applied.*
