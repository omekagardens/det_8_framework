# DET v8.0 — Physics (Track A)

**The physical calculus: falsifiable predictions, experimental designs, derived observables.**
**Status:** Candidate predictions pre-registered; awaiting experimental test.

---

## 1. κ-Physics (D3r1)

The structural history field κ replaces the original conflated `q` variable.

| Variable | Definition | Range |
|---|---|---|
| κ | Structural history density — record-side drag | [0, 1] |
| γ = λ_γ·κ | Gravitational source charge | ≥ 0 |
| γ_b | Cosmic baseline | Free parameter |

**Recovery dynamics:** \(d\kappa/dt = -(\kappa-\kappa_{eq})/\tau_{rec} + \dot\kappa_{damage}\)

**Free energy:** \(\psi = \psi_0 + \frac{1}{2}K(\kappa-\kappa_{eq})^2\) with dissipation \(\dot\kappa\cdot\partial\psi/\partial\kappa \leq 0\)

**Second Law compliance:** κ-recovery releases stored structural energy (ΔE < 0). This energy is exported to the environment as heat, with ΔS_environment ≥ |ΔE|/T. Total entropy change is nonnegative. Recovery is not spontaneous — it is driven by the free energy gradient, analogous to a compressed spring relaxing. Boundary-mediated Jubilee (κ-reduction without energy accounting) is classified M/H precisely because no physical channel is specified for the missing energy.

**κ measurement:** Structural proxy (`structural_proxy.py`) — calibrated mechanical probe. Δκ_min ≈ 0.002 at 1% noise. Cross-validated with clock and gravity.

**κ-diffusion:** \(d\kappa_i/dt = D\sum_j\sigma_{ij}(\kappa_j-\kappa_i) - (\kappa_i-\kappa_{eq})/\tau_{rec} + \dot\kappa_{damage}\) (`kappa_diffusion.py`)

---

## 2. Pre-Registered Predictions

### 2.1 κ-Π Clock Anomaly

**Formula:** \(\tau_A/\tau_B = (1+\lambda_P\kappa_B)/(1+\lambda_P\kappa_A)\)

**Null model:** τ_A/τ_B = 1.0 after all known corrections.

**Measurement:** Atomic clock frequency comparison (optical lattice, ~10⁻¹⁸ precision).

**Sensitivity:** λ_P ≥ 2×10⁻¹⁷ for 5σ detection in 12 days with κ=0.5.

**Experiment simulator:** `clock_experiment.py` — full Monte Carlo with Allan deviation noise model (white frequency σ_W=10⁻¹⁵, flicker floor σ_F=10⁻¹⁸), environmental noise (thermal + gravitational + magnetic ~2×10⁻¹⁸).

**Required controls:** Identical clocks (same σ, F, H, γ_v, materials, fabrication). κ=0 preparation (full recovery protocol). κ_target preparation (controlled damage protocol). Independent κ measurement via structural proxy.

**What constitutes discovery:** y = (ν_A−ν_B)/ν_A detected at ≥5σ with correct sign and magnitude matching prediction after all known corrections.

**What constitutes falsification:** Null result at 95% CL constrains λ_P < threshold.

**Confounder isolation:** The largest material confounder for optical lattice clocks is the blackbody radiation (BBR) shift, scaling as T⁴. For ¹⁷¹Yb at 300K with 1mK stability, BBR uncertainty is ~10⁻¹⁸. For λ_P≥10⁻¹⁴ and κ=0.5, the DET signal (~5×10⁻¹⁵) is 100–1000× larger than material confounders. The DET functional form (linear in κ/(1+λ_P·κ)) differs from all standard shifts (BBR ∝ T⁴, Zeeman ∝ B², Stark ∝ E², collisional ∝ n), enabling separation by varying κ at fixed T, B, E, n.

### 2.2 κ-Gravity Decoupling

**Formula:** \(F = G_q(\lambda_\gamma\kappa)^2/r^2\)

**Null model:** F = GM²/r² (standard Newton) — no change when M is constant but κ changes.

**Measurement:** Torsion balance (force resolution ~10⁻¹⁵ N at r=0.1m).

**Sensitivity:** λ_γ ≥ 5×10⁻⁹ for 5σ detection.

**Experiment simulator:** `gravity_experiment.py`.

**Mass-defect confound:** If damage adds energy ΔE, the mass change is Δm = ΔE/c². For a 1kg test mass with ΔE = 1J, Δm ≈ 10⁻¹⁷ kg, producing a relative gravitational change of ~10⁻¹⁷. The DET signal (force → 0 after recovery) is 10¹⁷× larger. The mass-defect confound is negligible at all accessible energy scales.

### 2.3 Combined Signature (Smoking Gun)

κ measured independently via structural proxy, clock anomaly, and gravity decoupling must agree. Three-way consistency constitutes strong evidence for κ as a real physical entity.

---

## 3. Newtonian Correspondence

All Newtonian observables reproduced exactly from DET primitives:

| Observable | Match |
|---|---|
| 1/r² force law | Exact |
| ∇²Φ = 4πG_q·ρ_γ | Identical form (κ replaces mass) |
| Kepler 1 (ellipses) | e < 0.001 |
| Kepler 2 (area law) | σ/μ < 10⁻⁶ |
| Kepler 3 (T² ∝ r³) | Ratio 0.99994 |
| Orbital velocity | \(v = \sqrt{G_q\gamma/r}\) |

**Difference:** DET sources gravity with κ (structural history), not mass. Free parameters: G_q and λ_γ (degenerate without independent κ measurement).

---

## 4. Lorentz Covariance

All 7 relativistic observables derived from event graph ≺:

| Observable | Derivation |
|---|---|
| Time dilation | Event density ratio in ≺ |
| Length contraction | Relativity of simultaneity in ≺ |
| Relativity of simultaneity | Frame-dependent spacelike foliations |
| Lorentz transformations | Symmetries preserving ≺ |
| Velocity addition | Boost composition |
| c as speed limit | No event outside J⁺(e) |
| Invariant interval | Unique quadratic form on light cone |

**What's assumed:** Lorentzian causal structure of ≺ (O7 — verified in continuum limit). c as empirical constant.

---

## 5. Quantum Derivations

| Derivation | Key insight |
|---|---|
| Born rule | K(i) = \|c_i\|² from kernel root composition forced by nonfactorizable records |
| CHSH = 2√2 | Bell state roots (1/√2,0,0,1/√2) under rotation |
| E(a,b) = cos(2(a-b)) | Nonfactorizable joint kernel from relational record |
| Pointer formation | Consensus of N weak commit events (no Kraus needed) |
| Amplitude structure | Complex numbers from continuous interference requirement |
| Hilbert space | Space of kernel roots with inner product ⟨c,d⟩ = Σ c_i* d_i |

---

## 6. Anti-Smuggling Audit

| Model | % DET-derived |
|---|---|
| MAM-0, DET-native measurement | 100% |
| DET-native spacetime | 85% |
| DET 8 Core | 85% |
| q-Gravity, Joint Kernel | 50–60% |
| MAM-Q, Peres-Mermin, CHSH | 20–40% (QM correspondence; now superseded by derivations) |

**Remaining borrowed:** Lorentzian causal structure (O7 — resolved), c (empirical), G_q/λ_γ/λ_P (free parameters).

---

## 7. Time Evolution

**DET-native Schrödinger:** \(c^{(n+1)} = U(R_n,\Delta\tau) \cdot c^{(n)}\)

Hamiltonian derived from record: \(H_{eff} \sim E_0\sigma_z + \lambda_\kappa\kappa\sigma_z + \lambda_F F I + \lambda_C(1-C)\sigma_x\)

Continuum limit recovers standard \(i\hbar d\psi/dt = H\psi\) with H from record structure.

---

## 8. Gravity (O7 — Resolved)

5-step derivation from event graph to Lorentzian manifold with dynamical geometry:

1. Causal order ≺ → light-cone structure
2. Π → conformal factor fixed (DET-unique — bare causal sets cannot do this)
3. κ-density → Einstein tensor (Newtonian limit verified)
4. Bond network → spatial metric via graph Laplacian
5. κ-diffusion + kernel evolution → spacetime dynamics

Continuum limit verified via sprinkling (500 events, N/τ² = 2.36, CV decreases with N).

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, GOVERNANCE.md, ROADMAP.md.**
