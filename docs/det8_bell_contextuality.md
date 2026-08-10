# DET v8.0-P0.4 — Bell/Contextuality Strategy Memo

**Status:** P/O (proposed position; mechanism remains open)
**Date:** August 9, 2026 (revised per adversarial review)
**Purpose:** Specify precisely how DET relates to Bell's theorem, CHSH, and Kochen-Specker contextuality. Eliminate vague "local but not local" language.

---

## 1. Bell's Theorem: The Premises

Bell's theorem (in the CHSH formulation) shows that any theory satisfying the following premises must obey the CHSH inequality \(|S| \leq 2\):

1. **Realism / Hidden Variables:** Measurement outcomes are determined by a complete specification of the state (hidden variables \(\lambda\)).

2. **Locality / Factorizability:**
   \[
   P(a, b \mid x, y, \lambda) = P(a \mid x, \lambda) \cdot P(b \mid y, \lambda)
   \]
   Alice's outcome \(a\) depends only on her setting \(x\) and \(\lambda\), not on Bob's remote setting \(y\).

3. **Measurement Independence (No-Conspiracy):**
   \[
   P(\lambda \mid x, y) = P(\lambda)
   \]
   The hidden variable distribution is independent of the measurement settings.

4. **Outcome Independence:**
   \[
   P(a \mid b, x, y, \lambda) = P(a \mid x, y, \lambda)
   \]
   Given \(\lambda\), Alice's outcome does not depend on Bob's outcome.

Since quantum mechanics violates the CHSH inequality (achieving \(|S| = 2\sqrt{2}\) for maximally entangled states), any theory that reproduces QM must reject at least one premise.

### 1.1 Bell Assumptions: DET Position Summary

| Assumption | Definition | DET Position | Reason | Status |
|---|---|---|---|---|
| Realism (hidden variables) | Outcomes determined by pre-existing \(\lambda\) | **Modified**: record is determinate; outcomes are not pre-existing | No Pre-Existing Future Facts invariant | P (architectural constraint) |
| Locality / Factorizability | \(P(a,b\|x,y,\lambda) = P(a\|x,\lambda) \cdot P(b\|y,\lambda)\) | **Rejected** | Entangled pairs are non-factorizable relational records | **P/O** (mechanism open) |
| Measurement Independence | \(P(\lambda\|x,y) = P(\lambda)\) | **Preserved** | Settings are boundary inputs; no conspiracy | P |
| Outcome Independence | \(P(a\|b,x,y,\lambda) = P(a\|x,y,\lambda)\) | **Rejected** (subsumed by factorizability rejection) | Outcomes are co-created, not independent | **P/O** |
| Causal Locality | No controllable superluminal signalling | **Preserved** (necessary but not sufficient for Bell-causal account) | No-signalling toy-tested; full relativistic locality unresolved | **P/O** |

---

## 2. Which Premises DET Preserves

### 2.1 Measurement Independence — PRESERVED

DET **preserves** Measurement Independence. The measurement settings \(x, y\) are not correlated with any hidden variable that pre-determines outcomes.

**Reason:** DET's No Pre-Existing Future Facts invariant (P0.3 §3.14) prohibits hidden variables that pre-fix unactualized outcomes. Measurement settings are declared by the experimenter (or by the causal history of the apparatus) and enter the law map \(\mathcal L_e\) as boundary inputs \(B_e\). They are not secretly correlated with outcomes via a common past cause.

**DET rejects superdeterminism and global-reconciliation shortcuts** (AGENTS.md §5.8).

---

### 2.2 Causal Locality — PRESERVED

DET **preserves** causal locality: no controllable superluminal signalling is possible.

**Reason:** This was verified in MAM-Q (M3): the marginal probability distribution for B does not depend on whether A measured in Z or X basis. The no-signalling test yielded delta = 0.005 (well within statistical tolerance).

Formally:
\[
P(b \mid y) = \sum_{a} P(a, b \mid x, y) = \sum_{a} P(a, b \mid x', y) \quad \forall x, x'
\]

The reduced density matrix of B is invariant under operations on A alone. DET's event-domain locality ensures that spacelike-separated measurements operate on disjoint event domains with declared causal order or confluence rules.

---

### 2.3 Realism (Record Determinacy) — PRESERVED (in modified form)

DET preserves the principle that the committed record is determinate. However, DET does **not** claim that measurement outcomes pre-exist in the record before measurement.

**Reason:** Before measurement, the entangled pair is an actual relational record (A/P): a non-factorizable phase-bearing relation that constrains future measurement outcomes without containing those outcomes as pre-existing facts. The qubit state (α, β) is a present structural feature. After measurement, the pointer record is a committed actual fact (A).

This is NOT the same as Bell's "Realism" premise, which assumes outcomes are determined by pre-existing \(\lambda\). DET replaces "outcomes are pre-determined by hidden variables" with "the relation is determinate; the outcomes are co-created at measurement in a way that respects the relation."

---

## 3. Which Premise DET Rejects

### Outcome Independence (Bell-Local Factorizability) — REJECTED

DET **rejects** Outcome Independence in the form of Bell-local factorizability:

\[
P(a, b \mid x, y, \lambda) \neq P(a \mid x, \lambda) \cdot P(b \mid y, \lambda)
\]

**Reason:** The entangled pair is a non-factorizable relational record. The two qubits do not have independent local properties; they share a single relational object that cannot be decomposed into \(\lambda_A \otimes \lambda_B\). When measurements occur at spacelike separation:

1. Each measurement event operates on its local event domain \(D_e\).
2. The law map \(\mathcal L_e\) for each event generates its possibility object \(\mathcal W_e\) from the causal-past record \(\mathcal R^-_e\).
3. For spacelike-separated measurements on an entangled pair, the joint outcome distribution is not factorizable because the pre-measurement relational record is not factorizable.

**DET's diagnosis:** Bell-local factorizability assumes that the complete state \(\lambda\) can be partitioned into independent local components. DET's relational records are not always partitionable in this way. The relation itself is a determinate physical object that spans spacelike-separated regions without being a signal channel.

---

## 4. Precise Statement

\[
\boxed{
\begin{aligned}
&\text{DET preserves:} \\
&\quad \bullet\ \text{Causal locality (no controllable superluminal signalling).} \\
&\quad \bullet\ \text{Measurement Independence (no conspiracy between settings and outcomes).} \\
&\quad \bullet\ \text{Record determinacy (committed facts are determinate).} \\
&\text{DET rejects:} \\
&\quad \bullet\ \text{Bell-local factorizability (outcomes are not independent given } \lambda\text{).} \\
&\quad \bullet\ \text{Pre-existing hidden outcomes (No Pre-Existing Future Facts).} \\
&\text{DET replaces pre-existing local properties with:} \\
&\quad \bullet\ \text{Non-factorizable relational records that constrain measurement outcomes} \\
&\quad\ \ \text{without containing them as pre-existing facts.}
\end{aligned}
}
\]

---

## 5. How No-Signalling Is Preserved

Even though DET rejects Bell-local factorizability, causal locality is preserved because:

1. The relational record (e.g., the Bell state) is a **global constraint** on the joint outcome distribution, not a signal channel.
2. The marginal probability for any local measurement depends only on the reduced density matrix, which is invariant under operations on the distant part.
3. The commit events at A and B are spacelike-separated; neither can causally influence the other's outcome (only the joint distribution is constrained).
4. The actualization at each event operates on its declared local domain \(D_e\); no nonlocal "influence" traverses the gap at the moment of measurement.

In DET language:
\[
P(\text{outcome at B} \mid \text{setting at B}, \mathcal R^-_B) = P(\text{outcome at B} \mid \text{setting at B}, \mathcal R^-_B, \text{setting at A})
\]
for spacelike-separated A and B. The possibility object at B does not depend on A's setting because A's setting is not in B's causal past.

---

## 6. Contextuality: Kochen-Specker

The Kochen-Specker theorem shows that non-contextual hidden variable models (where measurement outcomes are pre-assigned independently of which other observables are measured) are impossible for quantum systems of dimension ≥ 3.

### DET's response

DET is **explicitly contextual**. The measurement outcome depends on the complete measurement context — specifically, on which observables are jointly measured.

In DET terms:
- The law map \(\mathcal L_e\) generates the possibility object \(\mathcal W_e\) from the complete local record \(\mathcal R^-_e\), which includes the measurement setting (choice of basis/observable).
- Different measurement contexts produce different possibility objects, even for the "same" pre-measurement state.
- This is natural in DET: the measurement setting is a boundary input \(B_e\) that shapes \(\Omega_e\) and \(K_e\).

### MAM-Q contextuality example

In MAM-Q, measuring \(|+\rangle = (|0\rangle + |1\rangle)/\sqrt{2}\) in the Z basis yields:
- \(\Omega_Z = \{0, 1\}\), \(K_Z = (0.5, 0.5)\)

Measuring the same state in the X basis yields:
- \(\Omega_X = \{0\}\), \(K_X = (1.0)\)

The same pre-measurement relational record produces different possibility objects depending on the measurement context. The outcome "0 in X basis" is not the same physical event as "0 in Z basis" — they are different pointer records produced by different measurement events with different boundary conditions.

**This is contextuality, not a contradiction.** DET does not attempt to assign pre-existing values to observables independently of measurement context.

---

## 7. Minimal Contextuality Demonstration (Code)

For completeness, here is a concrete DET-contextuality demonstration using MAM-Q:

```python
from det8.models.mamq import QubitState, make_z_measurement, make_x_measurement
import math

inv2 = 1.0 / math.sqrt(2)
state = QubitState(alpha=inv2, beta=inv2)  # |+⟩

# Context 1: Z measurement
z_poss = make_z_measurement().compute_possibility(state)
# Ω_Z = [(0, |0⟩), (1, |1⟩)]
# K_Z  = [0.5, 0.5]

# Context 2: X measurement
x_poss = make_x_measurement().compute_possibility(state)
# Ω_X = [(0, |+⟩)]
# K_X  = [1.0]

# The same pre-measurement relational record yields different
# possibility objects in different measurement contexts.
# No pre-existing outcome assignment can be context-independent.
```

---

## 8. Unresolved Blockers

### 8.1 Blocker B1: Derivation of the Born Rule

DET currently uses the Born rule as a provisional calibration (H/O). To be a complete theory, DET must either:
- Derive \(p(X) = |\langle X|\Psi\rangle|^2\) from the commit kernel structure, or
- Accept the Born rule as a primitive and explain why it takes this specific form.

**Status:** O (open problem). This is Blocker #1 from P0.1 and remains unresolved.

---

### 8.2 Blocker B2: CHSH Violation Magnitude

QM predicts \(|S| = 2\sqrt{2}\) for the CHSH inequality. Any DET model must reproduce this precise value.

DET's rejection of Bell-local factorizability allows \(|S| > 2\) in principle, but does not yet fix the value at \(2\sqrt{2}\). The specific magnitude must emerge from the commit kernel structure.

**Status:** O (open problem). This is Blocker #2 from P0.1.

---

### 8.3 Blocker B3: Event-Domain Overlap for Entangled Measurements

When two spacelike-separated measurements occur on an entangled pair, the event domains \(D_A\) and \(D_B\) both reference the same relational record (the qubit pair). This is a special case of the Confluence problem (P0.1 §5.5).

DET requires one of:
1. A causal order between the events (not available for spacelike separation).
2. A declared joint event domain (risks nonlocality).
3. A confluence theorem (not yet established).
4. A local conflict rule (not yet defined).

**Status:** O (open problem). This is the Confluence problem from P0.1 and remains unresolved.

---

### 8.4 Blocker B4: Non-Factorizability Without Nonlocality

DET's core claim — that relational records can be non-factorizable without being nonlocal signal channels — requires a precise formal characterization.

What exactly makes a record "relational" versus "local"? When is non-factorizability a legitimate relational property versus a disguised nonlocal influence? These questions need formal criteria.

**Status:** O (open problem).

---

## 9. Relationship to F8-OPEN

The Bell/contextuality strategy is **orthogonal** to F8-OPEN. Even if DET rejects Bell-local factorizability and embraces contextuality, the question of whether genuine becoming (versus hidden determinism) occurs is a separate issue. All adversary classes (D0-D3) from F8-OPEN v2 can equally well adopt DET's Bell/contextuality stance while remaining deterministic, stochastic, or many-worlds.

This means:
- DET's Bell strategy does not help satisfy F8-OPEN.
- DET's Bell strategy is independently testable (reproduce QM correlations without superdeterminism).
- Success on Bell does not imply success on F8-OPEN.

---

## 10. Summary

| Question | Answer |
|---|---|
| Which Bell premise does DET reject? | Bell-local factorizability (Outcome Independence). |
| Which Bell premises does DET preserve? | Measurement Independence, Causal Locality. |
| Is DET superdeterministic? | No. DET explicitly rejects superdeterminism. |
| Is DET contextual? | Yes. Outcome possibilities depend on measurement context. |
| Does DET allow superluminal signalling? | No. Causal locality is preserved (verified in MAM-Q). |
| Does DET derive the Born rule? | No. It is provisional calibration (H/O, Blocker #1). |
| Does DET derive CHSH = 2√2? | No. It is an open problem (Blocker #2). |

---

**End of Bell/Contextuality Memo**

*This document replaces vague "local but not local" language with precise statements about which premises are retained, which are rejected, and what remains unresolved.*
