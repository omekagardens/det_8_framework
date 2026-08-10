# DET v8.0-P0.5-D3r1 — q-Physics Ledger (Revised)

**Status:** P0.5 deliverable (revised per reviewer critique)
**Date:** August 9, 2026
**Revision:** r1 — addresses three-role conflation, missing thermodynamics, scale definition, and identifiability
**Supersedes:** `det8_p0.5_q_physics_ledger.md` (D3 original)

---

## 0. Revision Summary

### 0.1 Problem Identified

The inherited DET \(q\) field conflates three distinct physical roles:

1. **Mutable material history** — record-side drag on participation.
2. **Universal clock drag** — proper-time rate suppression.
3. **Gravitational source** — contrast \(\rho = q - b\) sourcing gravity.

This conflation makes \(q\) operationally unidentifiable (circular: measure q via clocks, then use q to predict clocks), and prevents independent determination of which role is doing physical work.

### 0.2 Resolution: Ontology Fork (Option C — Explicit Coupling)

\(q\) is split into two coupled variables with a common physical origin:

\[
\boxed{
\begin{aligned}
\kappa_i &\in [0,1] \quad\text{— Structural history density (record-side)}\\
\gamma_i &= \lambda_\gamma \cdot \kappa_i \quad\text{— Gravitational source charge}\\
b &\quad\text{— Cosmic baseline (background structural history)}
\end{aligned}
}
\]

Both \(\kappa\) and \(\gamma\) derive from the same underlying process — the accumulation of structural imprints from past actualization — but serve distinct physical roles with independent operational definitions.

### 0.3 Mandatory Tasks Addressed

| # | Task | Section |
|---|---|---|
| 1 | Ontology fork | §1 |
| 2 | Neutral q-recovery equation | §2 |
| 3 | Free energy and dissipation law | §3 |
| 4 | q=0 and q=1 scale definition | §4 |
| 5 | Independent structural proxy | §5 |
| 6 | Baseline response operator chain | §6 |
| 7 | Zero-mode, coarse-graining, mass ledger, total energy | §7–10 |

---

## 1. Ontology Fork: The κ-γ Split

### 1.1 Structural History Density (κ)

\[
\kappa_i \in [0,1]
\]

**What it is:** The per-node record-side density of accumulated structural imprints from past actualization events. κ = 0 means the node carries no residual structural constraint from its history (fully recovered, pristine). κ = 1 means the node is maximally constrained by its history.

**Operational definition:** κ is the fraction of the node's available structural degrees of freedom that are currently locked into historical constraint patterns. A fully recovered node (κ = 0) has all degrees of freedom available for new participation. A maximally constrained node (κ = 1) has no free structural degrees of freedom.

**Physical preparation of κ = 0:** A node that has undergone complete structural recovery — all historical constraints released. This may require Boundary-mediated Jubilee (M/H) or a natural limit of recovery dynamics.

**Physical preparation of κ = 1:** A node that has accumulated structural constraints until no free degrees of freedom remain. This is a saturation limit, not an equilibrium.

### 1.2 Gravitational Source Charge (γ)

\[
\gamma_i = \lambda_\gamma \cdot \kappa_i
\]

where \(\lambda_\gamma\) is the gravitational coupling constant (dimensions of mass or gravitational charge per unit κ).

**What it is:** The effective gravitational source strength of node i. γ enters the gravitational source equation, not κ directly. This separation allows κ to be measured independently of gravity (via Π or structural proxies) and then tested against gravitational predictions.

**Why proportional:** The gravitational charge of a structure is proportional to the amount of structural history it carries. More history → more gravitational source. This maintains the DET intuition that ρ = q - b sources gravity, but makes the relationship explicit and parametrized.

### 1.3 Cosmic Baseline (b)

The baseline b is the average structural history density of the universe at the relevant scale. It replaces the "vacuum" against which local gravitational sources are measured.

\[
\rho_i = \gamma_i - \gamma_b
\]

where \(\gamma_b = \lambda_\gamma \cdot b\) is the baseline gravitational charge density. b may vary cosmologically; for local physics, b is approximately constant.

---

## 2. Neutral Physical κ-Recovery Equation

### 2.1 Removing Boundary Dependence

The original D3 ledger had three mechanisms for q-reduction: natural recovery, Boundary Healing, and Boundary Jubilee. The latter two are M/H and have no specified physical channel.

**Revised:** κ-recovery has a single physical mechanism — structural relaxation — with a well-defined rate equation. Boundary operators (if they exist) modify the rate or the equilibrium, but the baseline dynamics are record-side.

### 2.2 Recovery Dynamics

\[
\frac{d\kappa_i}{dt} = -\frac{\kappa_i - \kappa_{\text{eq}}}{\tau_{\text{rec}}} + \dot{\kappa}_{\text{damage}}
\]

where:
- \(\kappa_{\text{eq}} \in [0,1]\) is the equilibrium structural history (the value κ relaxes toward).
- \(\tau_{\text{rec}}\) is the recovery time scale (may depend on σ, F, C).
- \(\dot{\kappa}_{\text{damage}}\) is the damage rate from ongoing event actualization.

### 2.3 Damage Rate

\[
\dot{\kappa}_{\text{damage}} = \alpha \cdot (\text{event rate}) \cdot (1 - \kappa_i)
\]

where α is the damage coefficient per event. The factor (1 - κ_i) enforces the saturation limit κ ≤ 1.

### 2.4 Boundary Modification (M/H)

If Boundary operators exist, they may:
- Shift \(\kappa_{\text{eq}}\) downward (Jubilee: lower equilibrium).
- Decrease \(\tau_{\text{rec}}\) (Healing: faster recovery).
- Directly reduce κ by Δκ (Jubilee: instantaneous release).

These are M/H and do not enter the minimal physical core. The neutral equation above is the physical baseline.

---

## 3. Free Energy and Dissipation Law

### 3.1 Free Energy Functional

The structural history κ carries free energy. A node with κ > κ_eq stores excess structural energy that can be released through recovery.

\[
\psi(\kappa, F, C) = \psi_0(F, C) + \frac{1}{2} K (\kappa - \kappa_{\text{eq}})^2
\]

where:
- \(\psi_0(F, C)\) is the baseline free energy from resources and coherence.
- \(K\) is the structural stiffness (energy cost per unit κ² deviation from equilibrium).
- The quadratic form is the simplest model; higher-order terms may be needed near κ = 0 or κ = 1.

### 3.2 Dissipation Law

κ-recovery must satisfy nonnegative dissipation:

\[
\dot{\kappa} \cdot \frac{\partial\psi}{\partial\kappa} \leq 0
\]

For the quadratic free energy:

\[
\frac{\partial\psi}{\partial\kappa} = K(\kappa - \kappa_{\text{eq}})
\]

The recovery dynamics \(\dot{\kappa} = -(\kappa - \kappa_{\text{eq}})/\tau_{\text{rec}}\) satisfies:

\[
\dot{\kappa} \cdot \frac{\partial\psi}{\partial\kappa} = -\frac{K}{\tau_{\text{rec}}}(\kappa - \kappa_{\text{eq}})^2 \leq 0
\]

Dissipation is nonnegative for any τ_rec > 0.

### 3.3 Energy Ledger

| Process | Δκ | ΔE_structural | ΔS |
|---|---|---|---|
| Damage (event) | +Δκ | +½K[(κ+Δκ-κ_eq)² - (κ-κ_eq)²] | ΔS_export ≥ ΔE/T |
| Recovery (natural) | -Δκ | -½K[(κ-κ_eq)² - (κ-Δκ-κ_eq)²] | ΔS_local ≥ 0 |
| Jubilee (Boundary, M/H) | -Δκ | Same as recovery | May bypass entropy export |

---

## 4. κ Scale Definition

### 4.1 Physical κ = 0

**Definition:** Zero residual structural constraint. All structural degrees of freedom are available for new participation. The node's Π is at its maximum possible value for given σ, F, H, γ_v.

**Preparation protocol:**
1. Isolate the node from event-generating interactions.
2. Allow natural recovery to κ_eq (may require τ_rec ≪ observation time).
3. If κ_eq > 0, apply calibrated Jubilee or extended recovery.
4. Verify: Π has reached its asymptotic maximum under fixed σ, F, H, γ_v.

### 4.2 Physical κ = 1

**Definition:** All structural degrees of freedom are locked into historical constraint patterns. The node cannot participate in further actualization (Π → 0 in the q-drag channel).

**Preparation protocol:**
1. Subject the node to a high rate of actualization events until saturation.
2. Verify: κ no longer increases with further events (saturation).
3. Verify: Π has reached its asymptotic minimum (1/(1+λ_P) of the κ=0 value).

**Note:** κ = 1 may be unattainable in practice if the node disintegrates or transforms before saturation. The scale is defined by extrapolation.

### 4.3 Calibration of λ_P

Given κ = 0 and κ = 1 preparations:

\[
\lambda_P = \frac{\Pi(0)}{\Pi(1)} - 1
\]

This calibrates λ_P directly from Π measurements at the two endpoints, without requiring independent knowledge of σ, F, H, or γ_v (which are held constant).

---

## 5. Independent Structural Proxy

### 5.1 The Circularity Problem

Measuring κ via Π and then using κ to predict Π is circular. An independent proxy is required.

### 5.2 Proposed Proxy: Structural Response Function

Apply a calibrated probe (small energy impulse, brief bond stress) and measure the structural response:

\[
R(\kappa) = \frac{\text{response amplitude}}{\text{probe amplitude}}
\]

A node with κ = 0 (fully free) responds maximally. A node with κ = 1 (fully constrained) shows minimal or zero response.

### 5.3 Calibration Protocol

1. Prepare nodes at known κ values (using the preparation protocols of §4).
2. Apply a standardized probe to each.
3. Measure the response amplitude.
4. Construct the calibration curve R(κ).
5. For an unknown node, measure R and invert to obtain κ.

### 5.4 Requirements

- The probe must not significantly alter κ (non-destructive).
- The response must be monotonic in κ.
- The probe must not depend on σ, F, H, or γ_v in a way that confounds κ.

### 5.5 Alternative: Bond Network Analysis

If the node is part of a bond network, the collective vibrational spectrum of the network is sensitive to κ. Changes in κ shift the normal-mode frequencies. This provides an independent measurement channel.

---

## 6. Baseline Response Operator Chain

### 6.1 The Full Chain

A change in structural history propagates through the following causal chain:

\[
\Delta\kappa \xrightarrow{\lambda_\gamma} \Delta\gamma \xrightarrow{\text{baseline}} \Delta\rho \xrightarrow{\text{field eq.}} \Delta\Phi \xrightarrow{\text{geodesic}} \Delta(\text{acceleration})
\]

### 6.2 Step-by-Step

1. **κ → γ:** \(\Delta\gamma = \lambda_\gamma \cdot \Delta\kappa\). Linear coupling.
2. **γ → ρ:** \(\Delta\rho = \Delta\gamma - \Delta\gamma_b\). If baseline is fixed, \(\Delta\rho = \Delta\gamma\).
3. **ρ → Φ:** The gravitational potential Φ satisfies a field equation. Simplest model (Newtonian):
   \[
   \nabla^2\Phi = 4\pi G_q \cdot \rho(\mathbf{x})
   \]
   where \(G_q\) is the q-gravity coupling. For a point source at distance r:
   \[
   \Phi(r) = -\frac{G_q \cdot M_\gamma}{r}, \quad M_\gamma = \int \gamma(\mathbf{x}) d^3x
   \]
4. **Φ → acceleration:** Test particle acceleration: \(\mathbf{a} = -\nabla\Phi\).

### 6.3 For the Decoupling Test

Starting from two nodes with κ_A, κ_B:

- Before recovery: \(\gamma_A = \lambda_\gamma\kappa_A\), \(\gamma_B = \lambda_\gamma\kappa_B\).
  Force ∝ γ_A · γ_B (at fixed separation).
- After B recovers: κ_B → 0, γ_B → 0.
  Force → 0 while F (resource/energy) unchanged.
- Prediction: gravitational force drops by factor γ_B/γ_B = 1 → 0.

### 6.4 Distinguishability from Mass Loss

Standard mass loss (ΔF) changes the energy-momentum tensor but does not change κ unless the loss process generates structural damage. The κ-proxy (§5) provides an independent check: if κ decreases without F changing, the gravitational change is κ-mediated, not mass-mediated.

---

## 7. Zero-Mode and Boundary Conditions

### 7.1 The Zero-Mode Problem

The gravitational field equation \(\nabla^2\Phi = 4\pi G_q\rho\) determines Φ only up to a harmonic function (the zero mode). Boundary conditions at infinity must be specified.

### 7.2 Isolated Mass Construction

For an isolated mass in asymptotically flat space:

\[
\Phi(r) \to 0 \quad \text{as} \quad r \to \infty
\]

This fixes the zero mode. The total gravitational charge of an isolated system is:

\[
M_\gamma^{\text{tot}} = \int_{\text{system}} \gamma(\mathbf{x}) d^3x
\]

### 7.3 Cosmological Baseline

In a cosmological context, b may be nonzero and vary with cosmic time. The field equation then uses ρ = γ - γ_b as the source, and the zero mode is set by the cosmological boundary conditions (e.g., Friedmann-Robertson-Walker asymptotic).

---

## 8. Coarse-Graining Covariance

### 8.1 The Problem

If κ is defined per-node on a lattice, the total gravitational charge of a region should be invariant under lattice refinement:

\[
M_\gamma(\text{region}) = \sum_{i \in \text{region}} \gamma_i
\]

should approach a continuum limit independent of the lattice spacing.

### 8.2 Resolution

Define the continuum density:

\[
\gamma(\mathbf{x}) = \lim_{\text{refinement}} \frac{\sum_{i \in \Delta V} \gamma_i}{\Delta V}
\]

The coupling \(\lambda_\gamma\) must be defined so that \(\gamma_i\) scales correctly with the node's spatial volume. If nodes represent fixed physical volumes, \(\gamma_i\) is already a density. If nodes are abstract graph vertices, a volume element must be assigned.

### 8.3 Invariance Condition

The field equation \(\nabla^2\Phi = 4\pi G_q\rho\) in the continuum limit must produce the same Φ for a given mass distribution regardless of how the lattice discretizes it. This requires \(\gamma_i\) to be an extensive quantity (∝ node volume) and \(\lambda_\gamma\) to be calibrated accordingly.

---

## 9. Mass-Equivalence Ledger

DET distinguishes at least four mass concepts:

| Mass concept | Symbol | Definition | Depends on |
|---|---|---|---|
| **Energy mass** | \(M_E\) | \(E/c^2\) from total energy content | F, π (momentum), κ-field energy |
| **Inertial mass** | \(M_I\) | Resistance to acceleration: F = M_I·a | Unknown — may equal M_E |
| **Gravitational mass (κ)** | \(M_\gamma\) | \(\int \gamma d^3x = \lambda_\gamma \int \kappa d^3x\) | κ only |
| **Gravitational mass (standard)** | \(M_G\) | Source in Einstein equations | \(T_{\mu\nu}\) (energy-momentum) |
| **Participation mass** | \(M_\Pi\) | \(\Pi^{-1}\) (inverse participation aperture) | σ, F, H, κ, γ_v |

### 9.1 Required Equivalences

For DET to reduce to known physics in appropriate limits:

1. **Weak-field, low-κ:** \(M_\gamma \approx M_G\) (q-gravity matches standard gravity when κ is small). This requires \(\lambda_\gamma\) to be calibrated against G.
2. **Inertial-gravitational:** \(M_I = M_\gamma + M_G\) (total gravitational charge determines inertia). Or \(M_I = M_E\) (standard equivalence). P0.5 does not decide this.
3. **Participation-mass:** \(M_\Pi\) is a separate observable (clock rate), not a gravitational or inertial mass.

### 9.2 Open Question

Does \(M_\gamma = M_G\) in the Newtonian limit? If q-gravity is ADDITIONAL to standard gravity, the total gravitational field is \(\Phi_{\text{tot}} = \Phi_{\text{GR}} + \Phi_q\). If q-gravity REPLACES standard gravity, then \(\Phi_q\) must reproduce all observed gravitational phenomena. This is unresolved and deferred to P0.6.

---

## 10. Total Energy Ledger

### 10.1 Energy Contributions

The total energy of a DET system includes:

\[
E_{\text{tot}} = E_{\text{resource}} + E_{\text{kinetic}} + E_{\text{structural}} + E_{\text{field}} + E_{\text{interaction}}
\]

| Term | Definition |
|---|---|
| \(E_{\text{resource}}\) | \(\sum_i F_i\) — local resource/field energy |
| \(E_{\text{kinetic}}\) | \(\sum_i \frac{1}{2} m_i v_i^2\) or relativistic equivalent |
| \(E_{\text{structural}}\) | \(\sum_i \frac{1}{2} K (\kappa_i - \kappa_{\text{eq}})^2\) — stored structural energy |
| \(E_{\text{field}}\) | \(\frac{1}{8\pi G_q} \int |\nabla\Phi|^2 d^3x\) — gravitational field energy |
| \(E_{\text{interaction}}\) | \(\sum_i \gamma_i \Phi(\mathbf{x}_i)\) — node-field coupling |

### 10.2 Conservation

In the absence of Boundary operators, \(E_{\text{tot}}\) is conserved. κ-damage converts kinetic/resource energy into structural energy. κ-recovery converts structural energy into heat (entropy export) or kinetic/resource energy.

### 10.3 Boundary Operators (M/H)

If Boundary operators inject or extract energy, this must be accounted for in the energy ledger. Until a physical channel is specified, Boundary operators are outside the conservation accounting (this is acceptable for M/H status, but must be stated).

---

## 11. Universal-Clock vs Damaged-Clock Distinction

### 11.1 The Problem

A clock that runs slow due to κ could be:
- A fundamentally altered clock (different proper-time physics).
- A locally damaged clock in an otherwise standard spacetime.

DET claims the former, but the observable is the same (slower tick rate). The distinction requires a reference.

### 11.2 Resolution: Multi-Clock Comparison

Compare three clocks:

1. **Clock A:** κ = 0 (pristine). Ticks at rate Π(0).
2. **Clock B:** κ > 0 (damaged). Ticks at rate Π(κ) < Π(0).
3. **Clock C:** Standard GR clock at same gravitational potential, velocity, etc.

If DET's Π is the correct proper-time law:
- Clocks A and C agree (Π(0) matches GR prediction).
- Clock B runs slow by factor 1/(1+λ_P·κ).

If κ is merely local damage:
- Clocks A, B, C all agree after correcting for material changes (σ, geometry).
- The residual difference after material correction is zero.

The DET prediction is a nonzero residual after material correction. This is the q-Π clock anomaly, now reformulated in terms of κ.

---

## 12. Revised Risky Predictions

### 12.1 P1: κ-Gravity Decoupling (Reformulated)

**Claim:** κ-recovery reduces γ = λ_γ·κ and therefore reduces gravitational attraction, independently of changes in F (resource energy).

**Operational chain:** \(\Delta\kappa \xrightarrow{\lambda_\gamma} \Delta\gamma \xrightarrow{\text{field eq}} \Delta\Phi \xrightarrow{\text{geodesic}} \Delta a\).

**Null model:** No gravitational change when F is constant.

**Preregistration requirements:**
1. Calibrate λ_γ from independent κ and gravity measurements.
2. Prepare two systems with identical F but different κ.
3. Measure gravitational force difference.
4. Compare against prediction ΔF_grav ∝ Δγ.

### 12.2 P2: κ-Π Clock Anomaly (Reformulated)

**Claim:** Two clocks with identical σ, F, H, γ_v but different κ tick at different rates. The ratio is 1+λ_P·Δκ.

**Operational chain:** \(\Delta\kappa \xrightarrow{\lambda_P} \Delta\Pi \xrightarrow{\text{accumulation}} \Delta\tau\).

**Null model:** Clock rate depends only on σ, F, H, γ_v (material properties and kinematics).

**Preregistration requirements:**
1. Calibrate λ_P from κ=0 and κ=1 preparations.
2. Measure κ independently via structural proxy (§5).
3. Compare predicted Π ratio against measured clock ratio.
4. Verify the residual after material correction is nonzero and matches prediction.

---

## 13. Summary of Revisions

| Original (D3) | Revised (D3r1) |
|---|---|
| q as single three-role variable | κ (structural history) + γ = λ_γ·κ (gravitational charge) |
| Recovery via Boundary operators | Neutral physical recovery equation: dκ/dt = -(κ-κ_eq)/τ_rec + damage |
| No thermodynamics | Free energy ψ = ψ_0 + ½K(κ-κ_eq)², dissipation law \(\dot\kappa\cdot\partial\psi/\partial\kappa \leq 0\) |
| No scale definition | κ=0: fully recovered. κ=1: fully constrained. Calibration protocols. |
| Circular measurement (Π → q → Π) | Independent structural proxy via calibrated probe response |
| Vague baseline b | Explicit baseline operator chain: Δκ → Δγ → Δρ → ΔΦ → Δa |
| No zero-mode handling | Asymptotic flatness for isolated masses; cosmological boundary conditions |
| No coarse-graining | Continuum density limit; extensive γ_i |
| Single "mass" concept | Four-mass ledger: M_E, M_I, M_γ, M_Π |
| No energy ledger | Total energy: E_resource + E_kinetic + E_structural + E_field + E_interaction |
| No clock-type distinction | Multi-clock comparison protocol distinguishing universal from local damage |

---

**End of D3r1 — q-Physics Ledger (Revised)**
