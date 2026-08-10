# DET v8.0-P0.5-D3 — q-Physics Ledger

**Status:** P0.5 deliverable
**Date:** August 9, 2026
**Purpose:** Operationalize mutable structural history \(q\) as DET's potentially most distinctive surviving physical object. Address all 7 requirements from P0.4r1.1 §16.2.

---

## 1. Operational Definition of \(q\)

### 1.1 What \(q\) IS

\(q \in [0,1]\) is a per-node scalar in the committed record \(\mathcal R\). It represents:

> The present structural imprint of past events — the degree to which prior actualization continues to constrain current structural expression.

\(q\) is:
- **Record-side** — part of \(\mathcal R\), not a metaphysical primitive.
- **Mutable** — can decrease (recovery) or increase (damage/constraint accumulation).
- **Cumulative** — represents retained structural drag from all past events.
- **Local** — per-node; different nodes can have different \(q\) values.

\(q\) is NOT:
- Agency, choice, will, or intention.
- A measure of "how much the past still matters" in any metaphysical sense.
- Retroactive editing of history (the past event is fixed; only its present structural expression changes).

### 1.2 Physical Interpretation

\(q\) acts as a **drag coefficient** on participation:

\[
\Pi_i = \sigma_i \frac{1}{1+F_i} \frac{1}{1+H_i} \frac{1}{\gamma_{v,i}} \frac{1}{1+\lambda_P q_i}
\]

Higher \(q\) → lower \(\Pi\) → slower proper time → less physical participation.

In the gravity sector:

\[
\rho = q - b
\]

where \(b\) is a baseline. The contrast \(\rho\) sources gravitational effects.

### 1.3 Dynamics (Provisional, from DET 7)

\(q\) increases through:
- Event actualization that produces structural constraint.
- Damage, wear, entropy production, record formation.
- Bond formation that creates new relational constraints.

\(q\) decreases through:
- Recovery: natural relaxation of structural constraint.
- Healing: Boundary-mediated restoration of relational integrity.
- Jubilee: Boundary-mediated release of retained constraint.

The DET 7 update equation (provisional, pending regression):

\[
q_i^+ = q_i + \Delta q_{\text{event}} - \Delta q_{\text{recovery}} - \Delta q_{\text{Boundary}}
\]

---

## 2. Independent Measurement Protocol

### 2.1 The Measurement Problem

\(q\) is not directly observable. It must be inferred from its effects on measurable quantities:

1. **Clock rate:** \(\Pi \propto 1/(1+\lambda_P q)\). If \(\Pi\) is measurable via proper-time accumulation, \(q\) can be inferred.
2. **Gravity:** \(\rho = q - b\) sources gravitational effects. If the gravitational field is measurable, \(q\) can be inferred from \(\rho\).
3. **Participation rate:** Any process whose rate depends on \(\Pi\) is sensitive to \(q\).

### 2.2 Proposed Protocol

For a system with known (or calibrated) \(\sigma, F, H, \gamma_v\):

1. **Measure \(\Pi\):** Track proper-time accumulation \(\Delta\tau\) over known coordinate interval \(\Delta\kappa\).
2. **Invert the \(\Pi\) equation:**
   \[
   q_i = \frac{1}{\lambda_P}\left(\frac{\sigma_i}{\Pi_i} \frac{1}{1+F_i} \frac{1}{1+H_i} \frac{1}{\gamma_{v,i}} - 1\right)
   \]
3. **Cross-validate** with gravitational measurement of \(\rho = q - b\).

### 2.3 Calibration Requirements

To use this protocol:
- \(\sigma_i\) must be independently measurable or calibratable.
- \(F_i\) and \(H_i\) must be independently measurable.
- \(\gamma_{v,i}\) must be known from kinematics.
- \(\lambda_P\) must be calibrated (a single global or regime-level constant).
- \(b\) (gravity baseline) must be calibrated.

### 2.4 Identifiability Challenge

If \(\sigma, F, H\) are not independently measurable, \(q\) is not identifiable — changes in \(q\) can be absorbed into changes in \(\sigma, F,\) or \(H\). This is the central identifiability problem (see §6).

---

## 3. Energy and Entropy Ledger for \(q\)

### 3.1 \(q\)-Increase: Constraint Accumulation

When \(q\) increases, the system becomes more constrained. This should:

1. **Cost energy:** Forming new structural constraints requires work. The energy cost should appear in the local resource field \(F\).
2. **Export entropy:** The formation of ordered constraint (lower local entropy) must export entropy to the environment. This is standard thermodynamics.

Provisional ledger entry:

\[
\Delta E_{q\uparrow} = \kappa_q \cdot \Delta q \cdot (\text{local energy scale})
\]

\[
\Delta S_{\text{export}} \geq \frac{\Delta E_{q\uparrow}}{T}
\]

### 3.2 \(q\)-Decrease: Constraint Release

When \(q\) decreases (recovery), the system becomes less constrained:

1. **May release energy:** Breaking constraints can release stored energy.
2. **May absorb entropy:** The system becomes less ordered; entropy increases locally unless exported.
3. **Boundary-mediated reduction (Jubilee):** If a Boundary operator reduces \(q\) without the usual energy/entropy cost, this is a physical anomaly that requires accounting — where does the constraint go?

Provisional ledger entry:

\[
\Delta E_{q\downarrow} = -\kappa_q' \cdot \Delta q \cdot (\text{local energy scale})
\]

\[
\Delta S_{\text{local}} \geq 0 \quad \text{(constraint release increases local disorder)}
\]

### 3.3 Unresolved Questions

1. Is \(q\)-increase always energy-costly? Can constraint accumulate "for free" in some regimes?
2. Is \(q\)-decrease always energy-releasing? Can constraint dissipate without energy transfer?
3. What is the entropic signature of Jubilee-mediated \(q\)-reduction? If it violates the second law locally, what compensates?

---

## 4. Effect of \(q\)-Recovery on \(\Pi\)

From the participation aperture formula:

\[
\Pi_i(q) = \frac{\Pi_i(0)}{1 + \lambda_P q_i}
\]

where \(\Pi_i(0) = \sigma_i \frac{1}{1+F_i} \frac{1}{1+H_i} \frac{1}{\gamma_{v,i}}\) is the baseline participation at \(q=0\).

### 4.1 Recovery Effect

A reduction \(\Delta q < 0\) produces:

\[
\frac{\Delta\Pi}{\Pi} \approx \frac{\lambda_P |\Delta q|}{1 + \lambda_P q}
\]

For small \(q\):
\[
\frac{\Delta\Pi}{\Pi} \approx \lambda_P |\Delta q|
\]

### 4.2 Observable Consequences

1. **Clock speedup:** Recovery increases proper-time accumulation rate.
2. **Gravity reduction:** \(\rho = q - b\) decreases; gravitational effects weaken.
3. **Participation increase:** All \(\Pi\)-dependent processes accelerate.

### 4.3 Testable Prediction

A system undergoing \(q\)-recovery should exhibit a measurable increase in \(\Pi\) that:
- Is proportional to \(\Delta q\).
- Cannot be explained by changes in \(\sigma, F, H,\) or \(\gamma_v\).
- Has a specific time signature (recovery rate) predicted by the \(q\)-dynamics equation.

---

## 5. Effect of \(q\)-Recovery on Gravity

### 5.1 Gravity Sourcing

In DET 7/8, gravity is sourced through the contrast:

\[
\rho_i = q_i - b
\]

where \(b\) is a baseline (possibly zero, possibly a cosmic average).

### 5.2 Recovery Effect on Gravity

If \(q_i\) decreases through recovery:
- \(\rho_i\) decreases.
- The local gravitational source weakens.
- Nearby gravitational effects (curvature, attraction) diminish.

### 5.3 Testable Prediction

A massive object undergoing \(q\)-recovery (e.g., through Jubilee or natural relaxation) should exhibit:
- A measurable decrease in its gravitational field.
- This decrease should be distinguishable from mass loss (which would affect \(F\) and the energy-momentum tensor, not \(q\)).
- The time scale of gravity reduction should match the \(q\)-recovery time scale.

### 5.4 Challenge

Standard gravity is sourced by energy-momentum, not by a separate \(q\) field. For DET to be viable:
- \(q\) must either couple to the metric in addition to \(T_{\mu\nu}\), or
- \(q\) must modify the effective energy-momentum tensor, or
- \(q\) must be reinterpretable as a standard gravitational source term.

This mapping is unresolved.

---

## 6. Identifiability of \(q\)-Drag

### 6.1 The Problem

The participation aperture depends on five variables:

\[
\Pi = f(\sigma, F, H, \gamma_v, q)
\]

If only \(\Pi\) is measured, the five variables cannot be separately identified without additional measurements or constraints.

### 6.2 Identifiability Analysis

| Variable | Independent measurement? | Confounded with? |
|---|---|---|
| \(\sigma\) | Conductivity: measure transport rates | \(q\) — both suppress \(\Pi\) |
| \(F\) | Resource/field: measure local energy density | \(q\) — both suppress \(\Pi\) |
| \(H\) | Coordination load: measure computational/structural complexity | \(q\) — both suppress \(\Pi\) |
| \(\gamma_v\) | Kinematic: measure velocity | Identifiable if velocity is known |
| \(q\) | Structural history: **target of inference** | \(\sigma, F, H\) — degenerate |

### 6.3 Resolution Strategies

1. **Multiple regimes:** Measure \(\Pi\) under different conditions where \(\sigma, F, H\) vary but \(q\) is fixed (or vice versa).
2. **Gravitational cross-check:** Measure \(\rho = q - b\) independently via gravity. This breaks the degeneracy if gravity is measurable.
3. **Temporal signature:** \(q\) changes slowly (accumulation/recovery time scales), while \(\sigma, F, H\) may change rapidly. Temporal filtering can separate them.
4. **\(q\)-specific interventions:** If a Boundary operator (Jubilee) reduces \(q\) without affecting \(\sigma, F, H\), the effect on \(\Pi\) is a clean \(q\) signature.
5. **Baseline calibration:** For a system at \(q=0\) (fully recovered), measure \(\Pi(0)\) to calibrate \(\sigma, F, H, \gamma_v\). Then \(q\) is identifiable from \(\Pi(q) / \Pi(0)\).

### 6.4 Remaining Risk

Even with these strategies, \(q\) may remain entangled with other record variables in practice. This is an empirical question, not a theoretical one.

---

## 7. Risky Prediction

### 7.1 The Requirement

From P0.4r1.1: "A risky prediction that cannot be reproduced by simply redefining an ordinary damage or memory variable."

### 7.2 Candidate Prediction: \(q\)-Gravity Decoupling

**Claim:** \(q\) and the standard energy-momentum tensor \(T_{\mu\nu}\) can be varied independently in certain regimes, producing a gravitational signature that no standard theory predicts.

**Specific prediction:**
1. A system undergoes \(q\)-recovery (e.g., via Jubilee) without changing its energy-momentum content (\(F, \pi\) unchanged).
2. Its gravitational field weakens measurably.
3. Standard GR predicts no change (energy-momentum unchanged).
4. DET predicts change \(\propto \Delta q\).

**Why this is risky:**
- If no such decoupling is observed, DET's gravity sector is falsified (or \(q\) is not independently measurable).
- If decoupling is observed, it would be a major discovery — a gravitational source beyond energy-momentum.

**Why this is not just "damage":**
- An ordinary damage variable (e.g., crack density, dislocation count) affects energy-momentum (stored strain energy, mass deficit). \(q\)-recovery without energy-momentum change is not reproducible by redefining damage.
- A memory variable stores information; it does not source gravity unless it has energy content. \(q\) is claimed to source gravity without proportional energy content.

### 7.3 Fallback Prediction: \(q\)-\(\Pi\) Clock Anomaly

If gravity decoupling is too ambitious:

**Claim:** Systems with different \(q\) but identical \(\sigma, F, H, \gamma_v\) exhibit different proper-time accumulation rates.

**Test:** Compare two identical clocks where one has accumulated structural history (\(q > 0\)) and the other is freshly calibrated (\(q = 0\)). The \(q>0\) clock should run slower by factor \(1/(1+\lambda_P q)\).

**Why this is risky:** Clocks are among the most precise instruments. A deviation from standard time dilation predictions would be detectable.

**Why this is not just "wear":** Standard wear changes material properties (\(\sigma\), geometry), which can be independently measured and controlled for. \(q\) is an additional drag beyond material changes.

---

## 8. Summary

| Requirement | Status |
|---|---|
| 1. Operational definition of \(q\) | ✅ Defined as record-side structural drag scalar. |
| 2. Independent measurement protocol | ✅ Proposed: invert \(\Pi\) equation, cross-validate with gravity. |
| 3. Energy and entropy ledger | ✅ Provisional ledger entries; unresolved questions listed. |
| 4. Effect of \(q\)-recovery on \(\Pi\) | ✅ Derived: \(\Delta\Pi/\Pi \approx \lambda_P|\Delta q|\) for small \(q\). |
| 5. Effect of \(q\)-recovery on gravity | ✅ Traced through \(\rho = q - b\); mapping to metric unresolved. |
| 6. Identifiability | ✅ Analyzed; 5 resolution strategies; empirical question. |
| 7. Risky prediction | ✅ Two candidates: \(q\)-gravity decoupling (high-risk) and \(q\)-\(\Pi\) clock anomaly (medium-risk). |

### Open Issues

1. **Mapping \(q\) to the metric:** How does \(\rho = q - b\) couple to \(g_{\mu\nu}\)? Is it additive to \(T_{\mu\nu}\)? Does it modify the Einstein equation?
2. **\(q\)-dynamics equation:** The update rule for \(q\) is inherited from DET 7 and unvalidated.
3. **\(\lambda_P\) calibration:** The coupling constant needs empirical determination.
4. **Boundary-mediated \(q\)-reduction:** If Jubilee reduces \(q\) without energy/entropy cost, where does the constraint go? This is a potential conservation violation.
5. **Cosmic \(q\) background:** Is there a universal \(q\) field? Does \(b\) vary cosmologically?

---

**End of q-Physics Ledger**
