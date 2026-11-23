# DET v8.0 — Physics (Track A)

**The physical calculus: falsifiable predictions, experimental designs, and correspondence checks.**
**Status:** Candidate predictions pre-registered; awaiting experimental test. Concurrent κ-gravity revival evaluation on branch `revival/kappa-gravity-pathways` (`det8/models/kappa_gravity_revival.py`) operates under relaxed Gate 4 (`PROVISIONAL_INTEGRATED_MODEL` constructive exploration): **Pathway 1** (`kappa_t1_contraction.py`) = **`PARTIAL_LIMITATION`**, **Pathway 2** (`pi_conformal_bridge.py`) = **`REFUTED`**.

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

**κ measurement candidate:** Structural proxy (`structural_proxy.py`) — a simulated mechanical protocol, not yet an independently calibrated κ measurement. Its use is gated on F9 and operational plateau anchors; under `revival/kappa-gravity-pathways` (`kappa_t1_contraction.py::evaluate_screening_constraints`), scalar conflation of lab `FL-1` (`Δκ_dev = 0.002–0.5`) with gravitational `G_eff` violates MICROSCOPE (`1.5e-15`) by `1.242e12×` / `5.794e14×`, requiring rank `r > 1` separation (`κ_env` screened in lab vs. isolated `κ_dev` in clocks/proxies; `docs/record_kernel_physics.md` §2.1 & §2.4).

> **⚠ κ vs. defect density (Round 3 red-team, open).** The structural proxy currently models κ as "fraction of locked structural degrees of freedom" with standard materials-science proxies (dislocation density, residual stress, hardness, resistivity). No discriminator yet distinguishes "κ is a new field" from "κ = defect density". Until a discriminator is pre-registered (e.g., a τ_rec temporal signature decoupled from thermal annealing), the clock anomaly cannot claim novelty over standard materials science.

**Standard variable completeness audit:** To isolate a κ residual, all known material parameters affecting the probe response must be measured and corrected for. The audit lists: density, temperature, elastic moduli, thermal history, known defect density, and any other standard material parameter contributing >0.1× the κ signal. Any residual beyond the combined uncertainty of all listed parameters is the κ candidate. If residual is zero, κ is falsified as independent. Nonzero residual may still be κ or an unmeasured standard variable — the test can falsify but not conclusively confirm κ without exhaustive parameter coverage.

**κ-diffusion:** \(d\kappa_i/dt = D\sum_j\sigma_{ij}(\kappa_j-\kappa_i) - (\kappa_i-\kappa_{eq})/\tau_{rec} + \dot\kappa_{damage}\) (`kappa_diffusion.py`)

---

## 2. Pre-Registered Prediction (clock anomaly — an optional probe)

> **Ontology first (Round 6, Team A rebuttal):** DET's primary content is the relational record-kernel ontology (Track B) — the clock anomaly is an **optional empirical probe** of one physical realization (κ as an independent field), not the point. A null probe result costs the ontology nothing.
>
> **Scope decision (Option B & Revival Track Distinction):** Option B's core claim register treats DET as a participation/measurement theory, keeping the 28 legacy gravity modules (`gravity_v2.py`, `sparc_analysis.py`, `cluster_dynamics.py`, `post_newtonian.py`, `kappa_derivation.py`, `det_gravity.py`) permanently retired in `legacy_gravity_quarantine.FULLY_RETIRED` (PHYSICS §8–§10). On branch `revival/kappa-gravity-pathways`, `det8/models/kappa_gravity_revival.py` evaluates two new exploratory pathways outside `FULLY_RETIRED` under relaxed Gate 4 (`GOVERNANCE.md` §1) with explicit `TH-DET`/`P`/`CORR`/`FIT`/`EXTERNAL_ANCHOR` accounting:
> - **Pathway 1 (`kappa_t1_contraction.py` — T1 Kernel-Contraction + Reciprocal Aperture):** `κ(r) = exp(-(Σ_*+Σ_gas)/Σ_crit - w_SFR Σ_SFR)`, `G_eff(r) = G/(1 - βκ(r))` — status **`PARTIAL_LIMITATION`** (`4/4` core gates pass: `8/8` F6 monotonic, SPARC 43-galaxy `14.70%` `1d` / `14.83%` `freeman_2d` mean error with `30/43` within 20%, `14.2857×` `R6-B` ceiling at `β=0.93`, exponential `R6-A` `8.025e-25` at 1 AU solar wind; `5/6` limitations open: Keplerian `r^(-1/2)` outer turnover `-0.4928` / `-0.5000`, `41.19%` `KNOWN_GALAXIES` error from `11.54×` `M_star` discrepancy, power-law `729×` local 1 AU Cassini failure, unclosed covariant lensing/action).
> - **Pathway 2 (`pi_conformal_bridge.py` — Π-Conformal Clock-Metric Bridge):** `Δτ = Π ΔN`, `a = -c² ∇ ln Π`, `Φ_κ = c² ln(1 + λ_P κ)`, `g_μν = Π² η_μν` — status **`REFUTED`** across all 4 criteria (`C1_sign`: `8/8` repulsive under T1; `C2_lensing`: `γ_PPN = -1.0`, `86,956.52×` Cassini violation / `100%` VLBI miss; `C3_sparc_btfr`: `43.44×` `v²/c²` dynamic range, `38/43` unbound literal, `36.30%` sign-flipped error; `C4_clock_gap`: `5.0e10×` NIST / `57.14×` GPS / `0.01798 m/s²` lab acceleration; `any_det_native_survivor = False`).

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

### 2.2–2.3 Legacy κ-Gravity Decoupling & Combined Signature — RETIRED (Historical)

> **RETIRED (Round 6, Option B).** The legacy κ-gravity decoupling prediction (two-source law, α channel) and the combined "smoking gun" signature remain withdrawn (`archive/retired_kappa_gravity.md`). Current exploratory revival work (`kappa_t1_contraction.py` `PARTIAL_LIMITATION`; `pi_conformal_bridge.py` `REFUTED`) lives in new, quarantine-isolated modules documented in §2 above.

### 2.4 Falsification Ladder & Data Guardrail

The clock anomaly is tested in three ordered, DET-native steps (`det_falsification.py`):

| Step | Experiment | Falsifies DET if | Confirms DET if |
|---|---|---|---|
| 1 | κ-vs-defect discriminator (`kappa_discriminator.py`) | recovery time tracks thermal annealing (κ = defect density) | recovery is T-independent |
| 2 | Structural-proxy calibration (`structural_proxy.py`) | zero residual after known-physics regression | nonzero, reproducible residual |
| 3 | Clock comparison (`clock_experiment.py`) | null at precision σ ⇒ λ_P·κ < σ | Δν/ν = λ_P·κ/(1+λ_P·κ) at ≥5σ, correct sign |

**Data guardrail:** external datasets were built under other theories (GR, ΛCDM, materials science). Only their theory-independent **observed** quantity is admissible; the theory-dependent interpretation is quarantined. E.g., atomic-clock data contributes the frequency ratio (safe), not the GR redshift (quarantined); SPARC contributes v(r) (safe) but no DET gravity claim uses it under Option B.

**Gravity emergence:** under Option B's core register, gravity is not a promoted DET claim, and "does κ source or modify gravity?" remains an **OPEN frontier**. Under relaxed Gate 4 / lifted `T7` administrative pre-blocking (`docs/CONTINUUM_LIMIT_FRAMEWORK.md`, `GOVERNANCE.md` §1) with strict Gates 1–3, 5–6 and `FL-1` rank `r > 1` separation, `det8/models/kappa_gravity_revival.py` records **Pathway 1** (`PARTIAL_LIMITATION`, `FIT`/`CORR` closure on `TH-DET` T1 contraction) and **Pathway 2** (`REFUTED`). Full promotion still requires a DET-native derivation and covariant screening/lensing closure.

**Lab-executable protocol:** the full, step-by-step experimental protocol (materials, procedure, decision thresholds, SI units, power) is in `docs/falsification_protocol.md`. The supporting analyses are `det_falsification.sweep_probes` (where each probe bites) and `kappa_discriminator.power_curve` (power vs sample count).

---

## 3. Newtonian Correspondence — RETIRED (historical)

> **Retired (Round 6, Option B).** The legacy κ-only Newtonian correspondence (`a = −G_q·γ/r²`, Kepler recovered via `m → κ`) remains retired in `archive/retired_kappa_gravity.md`. Current revival checks (`galaxy_observables.py`, `kappa_t1_contraction.py`, `pi_conformal_bridge.py`) evaluate Pathway 1 (`PARTIAL_LIMITATION`) and Pathway 2 (`REFUTED`) against Level-2/3 Freeman-Newtonian baselines without reinstating legacy `G_q` or `λ_γ`.

---

## 4. Lorentz Covariance

Seven relativistic correspondence observables are reproduced after mapping the event graph ≺ to the standard spacetime role:

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

**Activity/record semantics (13 September 2026).** Distinguish present residual
transformation, committed-record formation and subsequent access. The
[semantic contract](docs/track_b/RECORD_PROCESS_CONTRACT.md) implements these as
separate experimental operations without choosing a Hamiltonian or growth law.
The conditional QR-MAP completion uses `X=(C,D_C)`, not a record-only state.
Its prior mathematical results remain conditional; the authorized
[mass/geometry/gravity research plan](docs/track_b/QR_MAP_RELATIVITY_GEOMETRY_PLAN.md)
does not revive retired κ-gravity. That isolated owner-authorized research
is distinct from release hardening and supersedes earlier blanket research
deferrals for this lane. The legacy formula `Δτ=ΠΔN` is a declared
count-based quantity, not proof that no commit implies no physical evolution.
Legacy claims below of a uniquely forced quantum theory or complete measurement
derivation are not the current QR-MAP result: noisy copying stabilizes an assumed
classical target; full QM remains conditional on additional operational premises.

> **Honest reclassification.** These are **correspondence checks**: each recovers a standard quantum result. They are now supplemented — not replaced — by the theorem program (T2b quadratic commit, T2a grade-2, T6/T6b correlation class, why-ℂ). The honest bottom line: DET derives the *almost-quantum* framework, with grade-2 an empirical choice and ℂ forced by (empirical Ω≠0) + reversibility.

| Correspondence | Key insight |
|---|---|
| Born rule | Grade-2 (quadratic) form is EMPIRICAL (T2a negative result); given grade-2, μ(A)=‖v_A‖² follows (T2b) |
| CHSH = 2√2 | SOS certificate (T6): B² = 4I − [A₀,A₁][B₀,B₁] ⇒ ‖B‖ ≤ 2√2, verified |
| E(a,b) = cos(2(a-b)) | Standard Bell state + rotation in the joint-kernel language |
| Pointer formation | Consensus of N weak commit events (no Kraus needed) |
| Amplitude structure | why-ℂ: ℝ falsified empirically; ℂ forced by reversible dynamics O∩Sp=U(m) (why_complex.py) |
| Hilbert space | Space of kernel roots with inner product ⟨c,d⟩ = Σ c_i* d_i (Gram, T2b) |

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

**Remaining borrowed & Revival Native-vs-Fitted Accounting:** Lorentzian causal structure (O7 — kinematic, T7), c (empirical), λ_P (free; G_q/λ_γ retired). In the κ-gravity revival (`closure_manifest()`), **Pathway 1** combines `TH-DET` T1 contraction `κ_n <= exp(-N_int/N_rec)` with `CORR` Freeman surface-density/`h = 0.3 kpc`/Keplerian kinematics and `FIT` closures (`Σ_crit = 0.008`, `w_SFR`, `β = 0.93`, `(1 - βκ)^(-1) = Σ_{m=0}^∞ (βκ)^m` geometric series; `Σ_crit` lies `17.13×` below MOND `a_0/(2πG) = 0.13701`); **Pathway 2** combines `TH-DET` M0 monotonicity and `P` `Π(κ)` with `CORR` `g_00 = -Π²`/`g_μν = Π² η_μν` (`REFUTED`) and `FIT` galactic `λ_P`.

---

## 7. Time Evolution

**DET-native Schrödinger:** \(c^{(n+1)} = U(R_n,\Delta\tau) \cdot c^{(n)}\)

Hamiltonian derived from record: \(H_{eff} \sim E_0\sigma_z + \lambda_\kappa\kappa\sigma_z + \lambda_F F I + \lambda_C(1-C)\sigma_x\)

Continuum limit recovers standard \(i\hbar d\psi/dt = H\psi\) with H from record structure.

---

## 8. Gravity — RETIRED (historical)

> **Retired (Round 6, Option B).** The legacy "O7 gravity" derivation (κ → Einstein tensor) and retired `post_newtonian.py` solar-system analysis remain quarantined in `archive/retired_kappa_gravity.md`. (L1–L3 order-and-count reconstruction remains active as kinematic T7.) Under the revival track, Pathway 1 passes exponential 1 AU screening (`8.025e-25 < 2.3e-5`) but fails power-law 1 AU screening (`729×`) and lacks a covariant lensing action (`PARTIAL_LIMITATION`), while Pathway 2's conformal metric yields `γ_PPN = -1.0` (`86,956.52×` Cassini violation; `REFUTED`).

---

## 9–12. Galaxy/Cluster/Dataset Analyses — RETIRED (historical) & Revival Dataset Audit

> **Retired (Round 6, Option B) vs. Revival Datasets:** The legacy `sparc_analysis.py`, `cluster_dynamics.py`, `remaining_items.py`, and `kappa_derivation.py` modules remain retired (`archive/retired_kappa_gravity.md`). Neutral galaxy fixtures are now isolated in `det8/models/galaxy_observables.py` (`KNOWN_GALAXIES`: 8; `SAMPLE_GALAXIES`: 43; `sparc_subset.json`: 56 records with `#` comments, `56/56` `M_gas == M_star`, `12/56` `V_flat == 0.0`, and up to `39.1×` / `11.54×` `M_star` discrepancies). Pathway 1 achieves `14.70%` (`1d`) / `14.83%` (`freeman_2d`) mean error on `SAMPLE_GALAXIES` with `8/8` F6 monotonic (`PARTIAL_LIMITATION`, turning over to `r^(-1/2)` outer slope `-0.4928`), while Pathway 2 is `REFUTED` (`38/43` unbound literal, `36.30%` sign-flipped error). The atomic-clock bound remains a product bound λ_P·Δκ < σ (§14).

---

## 13. U(1) Emergence from Z₂

Complex amplitudes emerge from discrete sign statistics (the full constructive
derivation is **open**; the items below are shape arguments, not proven — see
`u1_emergence.py`, which explicitly disclaims derivation status):

1. **Shape argument:** CLT → Gaussian effective amplitudes
2. **Shape argument:** Circular symmetry → U(1) phase invariance
3. **Shape argument:** Continuous interference from relative phases
4. **Conjectured:** Convergence rates (Berry-Esseen), uniqueness (quantum reconstruction)

---

## 14. GPS Satellite Clock Analysis

> **⚠ Vacuous bound (Round 3 red-team).** The λ_P bounds quoted below are constraints on the *product* λ_P·Δκ, where Δκ between two clocks is **assumed, not measured**. λ_P is unconstrained by existing clock data until κ is independently measured. The model-independent statement is λ_P·Δκ < σ.

GPS clock data bounds the product λ_P·Δκ (orbital clocks): λ_P·Δκ ≲ 3.5×10⁻⁹ (≈10⁹× weaker than lab clocks). **Finding:** this confirms the clock bound is a product, not a standalone λ_P bound, and in Pathway 2 (`pi_conformal_bridge.py::audit_clock_scale_gap`) galactic `λ_P = 2.0e-7` exceeds the conditional GPS bound (`3.5e-9` at `Δκ = 10⁻⁶`) by **`57.14×`** (`C4_clock_gap` refutation alongside `5.0e10×` NIST). Lab experiments with controlled κ preparation remain the right approach.

Module: `gps_analysis.py`.

---

## 15. Continuum Limit Status (L1-L4)

> **⚠ Dimensional caveat (Round 3 red-team).** The empirical convergence rates quoted below (α ≈ 0.50, 0.75, 0.85) are all measured in **1+1 Minkowski**. The physically relevant 3+1 case is the slowest (N^(−1/4)) and is not yet computed. The "α=0.50" headline should be read with this caveat.

| Lemma | Statement | Status |
|---|---|---|
| L1 | Causal structure → (M, g) causal structure | **Proven** (causal set theory) |
| L2 | Coarse-grained count → conformal factor Ω(x) | Numerical evidence (α=0.50 convergence). Formal proof open. |
| L3 | Reconstructed metric g_N → g | Statistical convergence verified (CV 0.56→0.25). LGH proof open. |
| L4 | κ-density → G_μν = 8πG_q·T^κ_μν | **RETIRED** (κ-gravity, Option B) — see `archive/retired_kappa_gravity.md` |

DET's active contribution: the **counting measure** fixes the conformal factor (order alone cannot), a **kinematic** reconstruction (order + count → geometry) — the T7 program, implemented in `det8/models/order_count_geometry.py`. The Π conformal factor (Ω = Π/c) is **RETIRED** (count supersedes it, and Pathway 2 `pi_conformal_bridge.py` quantitatively **refutes** `g_μν = Π² η_μν` with `γ_PPN = -1.0` and `86,956.52×` Cassini violation). The L4 gravity step is retired — the discrete-action → Einstein–Hilbert route is now standard gravity, not a DET gravity claim.

Module: `continuum_limit_proof.py`, `continuum_limit_l234.py`.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, GOVERNANCE.md, ROADMAP.md.**
