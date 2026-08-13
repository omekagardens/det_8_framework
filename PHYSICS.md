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

**κ-energy carrier:** The free energy ψ = ψ₀ + ½K(κ−κ_eq)² is a phenomenological form. The microscopic carrier of κ-energy depends on the physical realization: if κ manifests as lattice defect density, the energy is elastic strain energy stored in dislocation fields (standard materials science). If κ represents structural history beyond standard defect density, the carrier must be identified in the relevant physical realization. At this stage, the energy ledger is a *constraint* that any physical realization of κ must satisfy, without specifying the carrier.

**κ measurement:** Structural proxy (`structural_proxy.py`) — calibrated mechanical probe. Δκ_min ≈ 0.002 at 1% noise. Cross-validated with clock and gravity.

> **⚠ κ vs. defect density (Round 3 red-team, open).** The structural proxy currently models κ as "fraction of locked structural degrees of freedom" with standard materials-science proxies (dislocation density, residual stress, hardness, resistivity). No discriminator yet distinguishes "κ is a new field" from "κ = defect density". Until a discriminator is pre-registered (e.g., a τ_rec temporal signature decoupled from thermal annealing), the clock anomaly cannot claim novelty over standard materials science.

**Standard variable completeness audit:** To isolate a κ residual, all known material parameters affecting the probe response must be measured and corrected for. The audit lists: density, temperature, elastic moduli, thermal history, known defect density, and any other standard material parameter contributing >0.1× the κ signal. Any residual beyond the combined uncertainty of all listed parameters is the κ candidate. If residual is zero, κ is falsified as independent. Nonzero residual may still be κ or an unmeasured standard variable — the test can falsify but not conclusively confirm κ without exhaustive parameter coverage.

**κ-diffusion:** \(d\kappa_i/dt = D\sum_j\sigma_{ij}(\kappa_j-\kappa_i) - (\kappa_i-\kappa_{eq})/\tau_{rec} + \dot\kappa_{damage}\) (`kappa_diffusion.py`)

---

## 2. Pre-Registered Prediction (clock anomaly — an optional probe)

> **Ontology first (Round 6, Team A rebuttal):** DET's primary content is the relational record-kernel ontology (Track B) — the clock anomaly is an **optional empirical probe** of one physical realization (κ as an independent field), not the point. A null probe result costs the ontology nothing.
>
> **Scope decision (Option B):** DET is a participation/measurement theory, not a gravity-modification theory. The κ-gravity decoupling prediction (§2.2 v1/v2) and the combined signature (§2.3) are **RETIRED**: gravity is standard GR, dark matter is standard, and DET no longer claims any gravitational anomaly. The retired gravity program is retained for historical audit (PHYSICS §8–§10, `gravity_v2.py`, `sparc_analysis.py`, `cluster_dynamics.py`, `post_newtonian.py`).

### 2.1 κ-Π Clock Anomaly

> **Precision-materials program (L0/L1/L2).** Track A is reframed as a precision-measurement program for detecting and controlling history-dependent structural effects in materials used by clocks, oscillators, and quantum devices (`det8/models/operational_kappa.py`):
>
> - **L0** — κ as an engineering descriptor of structural history (useful even if DET is false).
> - **L1** — κ as an *independent residual* beyond standard materials variables (the empirical milestone; the scientific discriminator).
> - **L2** — κ coupling to clock rate via λ_P (the risky DET-specific prediction).
>
> κ is made **operational** (metrological): `κ̂_op = Σ w_i s_i (z_i − f_std_i)/Σ w_i s_i²` over a multi-probe vector `z`, with uncertainty per sample. Two guardrails: (i) a **standard-variable completeness audit** — any parameter capable of > 0.05× the expected signal must be measured, bounded, or stabilized; (ii) an **anti-circularity rule** — κ must NOT be inferred from the clock anomaly it is used to test (mechanical/calorimetric/microscopic/transport, a reference sample, or a non-clock oscillator only). The full program and findings are in **`docs/applied_physics.md`** (module: `det8/applied_physics/`).

> **Empirical status — revaluation (Aug 2026):** two facts about the λ_P channel temper how this prediction should be read.
>
> 1. **λ_P is free, not derivable.** It enters only the participation aperture (Π = …(1+λ_P·κ)⁻¹), nowhere in the commit kernel `K`, the law map `L`, or the κ-dynamics (κ* = (κ_eq+β)/(1+β) is independent of λ_P). It is dimensionless, so no dimensional anchor exists. Its only internal constraint is the anthropic inequality λ_P ≤ (1/Π_min − 1)/κ*, and Π_min is a module-level *choice*, not a derived quantity. `det8_core.py` defines λ_P only operationally (`λ_P = Π(0)/Π(1) − 1`). The prediction is therefore a **one-parameter family** Δν/ν = λ_P·κ/(1+λ_P·κ), not a single number; λ_P's value is purely empirical.
>
> 2. **The probe is gated behind two prerequisites that do not yet exist.** Because λ_P and κ only ever enter as the *product* λ_P·κ (the F7 point), the clock test needs (a) a κ *preparation* protocol producing two known κ values, and (b) an independent κ *measurement* (the structural proxy). The proxy has an unsolved **bootstrap**: `calibrate_proxy` requires known-κ anchor samples (κ=0, κ=1) that nothing yet tells us how to prepare, and the single mechanical-response model `R(κ)=R₀(1−κ)^α` is *asserted*, not measured. The whole ladder is gated on the **F9 discriminator** (does κ survive at 900 K, i.e. is it anything beyond defect density?) — unexecuted — which itself needs the preparation protocol.
>
> **Net revaluation:** Option B is ontologically clean but **empirically thin** — it concentrates the entire empirical program into a *single* probe sitting at the top of the L0→L1→L2 ladder, gated behind materials-science prerequisites (preparable κ, measurable κ) that are open experimental problems. This does not weaken the ontology (which never needed λ_P ≠ 0); it means the clock anomaly is a *conditional, future* test — contingent on F9 and the proxy landing — not a near-term prediction. Full dependency chain in `docs/falsification_protocol.md`.

**Formula:** \(\tau_A/\tau_B = (1+\lambda_P\kappa_B)/(1+\lambda_P\kappa_A)\)

**Null model:** τ_A/τ_B = 1.0 after all known corrections.

**Measurement:** Atomic clock frequency comparison (optical lattice, ~10⁻¹⁸ precision).

**Sensitivity:** λ_P ≥ 2×10⁻¹⁷ for 5σ detection in 12 days with κ=0.5.

**Experiment simulator:** `clock_experiment.py` — full Monte Carlo with Allan deviation noise model (white frequency σ_W=10⁻¹⁵, flicker floor σ_F=10⁻¹⁸), environmental noise (thermal + gravitational + magnetic ~2×10⁻¹⁸).

**Required controls:** Identical clocks (same σ, F, H, γ_v, materials, fabrication). κ=0 preparation (full recovery protocol). κ_target preparation (controlled damage protocol). Independent κ measurement via structural proxy.

**What constitutes discovery:** y = (ν_A−ν_B)/ν_A detected at ≥5σ with correct sign and magnitude matching prediction after all known corrections.

**What constitutes falsification:** Null result at 95% CL constrains λ_P < threshold.

**Confounder isolation:** The largest material confounder for optical lattice clocks is the blackbody radiation (BBR) shift, scaling as T⁴. For ¹⁷¹Yb at 300K with 1mK stability, BBR uncertainty is ~10⁻¹⁸. For λ_P≥10⁻¹⁴ and κ=0.5, the DET signal (~5×10⁻¹⁵) is 100–1000× larger than material confounders. The DET functional form (linear in κ/(1+λ_P·κ)) differs from all standard shifts (BBR ∝ T⁴, Zeeman ∝ B², Stark ∝ E², collisional ∝ n), enabling separation by varying κ at fixed T, B, E, n.

**Damage protocol specification:** The κ=0.5 preparation must change κ while holding standard parameters constant to the required precision. Candidate protocol: neutron irradiation with active cryogenic cooling maintains T stability to <1mK. The neutron flux introduces lattice defects (primarily Frenkel pairs in Yb/Sr optical lattices) with negligible electromagnetic side-effects: no net charge injection (ΔE ≈ 0), no magnetic field generation (ΔB < 1nT), and no change in atomic density (Δn/n < 10⁻⁹). The dominant remaining confounder is BBR from any residual temperature increase, held to <10⁻¹⁸ by active cooling. For low-λ_P searches (10⁻¹⁶–10⁻¹⁷), the 12-day integration requires active systematic control of BBR drift to maintain SNR. Below λ_P=10⁻¹⁷, next-generation nuclear clocks (~10⁻¹⁹ precision) are needed.

### 2.2–2.3 κ-Gravity Decoupling & Combined Signature — RETIRED

> **RETIRED (Round 6, Option B).** Gravity is standard GR; dark matter is standard. The κ-gravity decoupling prediction (two-source law, α channel) and the combined "smoking gun" signature are withdrawn. Full historical audit in `archive/retired_kappa_gravity.md`.

### 2.4 Falsification Ladder & Data Guardrail

The clock anomaly is tested in three ordered, DET-native steps (`det_falsification.py`):

| Step | Experiment | Falsifies DET if | Confirms DET if |
|---|---|---|---|
| 1 | κ-vs-defect discriminator (`kappa_discriminator.py`) | recovery time tracks thermal annealing (κ = defect density) | recovery is T-independent |
| 2 | Structural-proxy calibration (`structural_proxy.py`) | zero residual after known-physics regression | nonzero, reproducible residual |
| 3 | Clock comparison (`clock_experiment.py`) | null at precision σ ⇒ λ_P·κ < σ | Δν/ν = λ_P·κ/(1+λ_P·κ) at ≥5σ, correct sign |

**Data guardrail:** external datasets were built under other theories (GR, ΛCDM, materials science). Only their theory-independent **observed** quantity is admissible; the theory-dependent interpretation is quarantined. E.g., atomic-clock data contributes the frequency ratio (safe), not the GR redshift (quarantined); SPARC contributes v(r) (safe) but no DET gravity claim uses it under Option B.

**Gravity emergence:** gravity is not a current DET claim, but "does κ source or modify gravity?" remains an **open frontier**, not a rejected hypothesis. The retired gravity modules are archived; the question can be revisited only if a DET-native mechanism is derived and survives the standard constraints (equivalence principle, Eötvös, rotation curves).

**Lab-executable protocol:** the full, step-by-step experimental protocol (materials, procedure, decision thresholds, SI units, power) is in `docs/falsification_protocol.md`. The supporting analyses are `det_falsification.sweep_probes` (where each probe bites) and `kappa_discriminator.power_curve` (power vs sample count).

---

## 3. Newtonian Correspondence — RETIRED (historical)

> **Retired (Round 6, Option B).** The κ-only Newtonian correspondence (`a = −G_q·γ/r²`, Kepler recovered via `m → κ`) belongs to the retired κ-gravity program. Historical audit in `archive/retired_kappa_gravity.md`. Gravity is standard GR.

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

## 5. Quantum Correspondence

> **Honest reclassification (Round 3 red-team).** These are **correspondence checks**: each recovers a standard quantum result after standard amplitudes/rotations are *assumed*. They are not derivations from DET primitives — the uniqueness/derivation theorems remain open (O1/O2 status CI/AT per `MODEL_CARD.md` §6).

| Correspondence | Key insight |
|---|---|
| Born rule | K(i) = \|c_i\|² is *postulated* in the definition of a kernel root; the uniqueness theorem is open |
| CHSH = 2√2 | Standard Bell state (1/√2,0,0,1/√2) + standard rotation, relabeled |
| E(a,b) = cos(2(a-b)) | Standard Bell state + rotation in the joint-kernel language |
| Pointer formation | Consensus of N weak commit events (no Kraus needed) |
| Amplitude structure | Complex numbers assumed; U(1) emergence from Z₂ is a sketch (open) |
| Hilbert space | Space of kernel roots with inner product ⟨c,d⟩ = Σ c_i* d_i |

---

## 6. Anti-Smuggling Audit

> **Honest note (Round 3 red-team):** the "% DET-derived" figures below are the authors' self-assessments. The quantum/gravity/Lorentz "derivation" modules are standard physics with the symbol `m → κ` substituted (see §5 reclassification); their high percentages reflect DET *terminology*, not DET *derivation*. Genuine anti-smuggling holds only for the modules built purely from DET primitives (`mam0`, `det8_core`, `anthropic_principle`).

| Model | % DET-derived |
|---|---|
| MAM-0, DET-native measurement | 100% |
| DET-native spacetime | 85% |
| DET 8 Core | 85% |
| q-Gravity, Joint Kernel | 50–60% |
| MAM-Q, Peres-Mermin, CHSH | 20–40% (QM correspondence; now superseded by derivations) |

**Remaining borrowed:** Lorentzian causal structure (O7 — kinematic, T7), c (empirical), λ_P (free; G_q/λ_γ retired).

---

## 7. Time Evolution

**DET-native Schrödinger:** \(c^{(n+1)} = U(R_n,\Delta\tau) \cdot c^{(n)}\)

Hamiltonian derived from record: \(H_{eff} \sim E_0\sigma_z + \lambda_\kappa\kappa\sigma_z + \lambda_F F I + \lambda_C(1-C)\sigma_x\)

Continuum limit recovers standard \(i\hbar d\psi/dt = H\psi\) with H from record structure.

---

## 8. Gravity — RETIRED (historical)

> **Retired (Round 6, Option B).** The "O7 gravity" derivation (κ → Einstein tensor) and the post-Newtonian solar-system analysis belong to the retired κ-gravity program. Gravity is standard GR; dark matter is standard. Historical audit in `archive/retired_kappa_gravity.md`. (L1–L3 order-and-count reconstruction remains active as the kinematic program T7; only the L4 gravity step is retired.)

---

## 9–12. Galaxy/Cluster/Dataset Analyses — RETIRED (historical)

> **Retired (Round 6, Option B).** The SPARC rotation-curve, cluster-dynamics, r_SFR, Eötvös/flyby, and solar-system analyses all belong to the withdrawn κ-gravity program. They are **not** active physical results (several were not reproducible from the committed tree, and the `κ(r)` derivation failed its sign test). Historical audit in `archive/retired_kappa_gravity.md`. The only surviving datum is the atomic-clock bound λ_P·Δκ < σ (§14).

---

## 13. U(1) Emergence from Z₂

Complex amplitudes emerge from discrete sign statistics:
1. **Proven:** CLT → Gaussian effective amplitudes
2. **Proven:** Circular symmetry → U(1) phase invariance
3. **Proven:** Continuous interference from relative phases
4. **Conjectured:** Convergence rates (Berry-Esseen), uniqueness (quantum reconstruction)

---

## 14. GPS Satellite Clock Analysis

> **⚠ Vacuous bound (Round 3 red-team).** The λ_P bounds quoted below are constraints on the *product* λ_P·Δκ, where Δκ between two clocks is **assumed, not measured**. λ_P is unconstrained by existing clock data until κ is independently measured. The model-independent statement is λ_P·Δκ < σ.

GPS clock data bounds the product λ_P·Δκ (orbital clocks): λ_P·Δκ ≲ 3.5×10⁻⁹ (≈10⁹× weaker than lab clocks). **Finding:** this says nothing about a gravitational κ channel (retired, Option B) — it only confirms the clock bound is a product, not a λ_P bound. Lab experiments with controlled κ preparation are the right approach.

Module: `gps_analysis.py`.

---

## 15. Continuum Limit Status (L1-L4)

> **⚠ Dimensional caveat (Round 3 red-team).** The empirical convergence rates quoted below (α ≈ 0.50, 0.75, 0.85) are all measured in **1+1 Minkowski**. The physically relevant 3+1 case is the slowest (N^(−1/4)) and is not yet computed. The "α=0.50" headline should be read with this caveat.

| Lemma | Statement | Status |
|---|---|---|
| L1 | Causal structure → (M, g) causal structure | **Proven** (causal set theory) |
| L2 | Coarse-grained Π → conformal factor Ω(x) | Numerical evidence (α=0.50 convergence). Formal proof open. |
| L3 | Reconstructed metric g_N → g | Statistical convergence verified (CV 0.56→0.25). LGH proof open. |
| L4 | κ-density → G_μν = 8πG_q·T^κ_μν | **RETIRED** (κ-gravity, Option B) — see `archive/retired_kappa_gravity.md` |

DET's active contribution: Π fixes the conformal factor (bare causal sets cannot); this is a **kinematic** reconstruction (order + count → geometry), the T7 program. The L4 gravity step is retired — the discrete-action → Einstein–Hilbert route is now standard gravity, not a DET gravity claim.

Module: `continuum_limit_proof.py`, `continuum_limit_l234.py`.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, GOVERNANCE.md, ROADMAP.md.**
