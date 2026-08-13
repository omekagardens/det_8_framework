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

### 2.2 κ-Gravity Decoupling (v2 — two-source)

> **RETIRED (Round 6, Option B).** This prediction is withdrawn. DET does not modify gravity; gravity is standard GR and dark matter is standard. The two-source law below is retained for historical audit only. **Revisit condition** (not "given up"): gravity may be revisited only if a DET-native mechanism is derived from primitives and survives the equivalence-principle/Eötvös/rotation-curve discipline — see `det_falsification.gravity_emergence_note()`.

> **Resolved (Round 3 red-team, Team A decision).** The mass-independent law `F = G_q·λ_γ²·κ₁κ₂/r²` is **DEPRECATED** (empirically falsified by the equivalence principle: a 1 g and a 1000 kg mass with equal κ do not gravitate identically). It is retained only as a historical audit (`gravity_v2.compare_force_laws`). The active law is the **two-source field equation** (`gravity_v2.py`):

\[
\nabla^2\Phi = 4\pi G(\rho_m + \rho_\kappa),
\qquad
\rho_\kappa = \rho_m\,\chi(\kappa),
\qquad
\chi(\kappa) = \frac{\kappa-\kappa_{eq}}{\kappa_{earth}}
\]

with effective coupling \(G_{eff} = G(1+\alpha\chi)\) — **linear in κ**. The point-source force \(F = G_{eff}\,m_1m_2/r^2\) scales ∝ m₁m₂, preserving the equivalence principle. κ remains dimensionless in [0,1]; it **modifies the gravitational response**, it does not replace mass, and it is not a hidden mass variable.

**Null model:** F = GM²/r² (standard Newton) — no change when M is constant but κ changes.

**Rewritten prediction (v2):** recovering κ (κ → κ_eq ⇒ χ → 0) removes only the anomalous component \(F_\kappa = G\alpha\chi\,m_1m_2/r^2\), leaving standard Newtonian \(F_N\). The signature is \(\Delta F = F_\kappa \neq 0\), **not** F → 0.

**Measurement:** Torsion balance (force resolution ~10⁻¹⁵ N at r=0.1m).

**Sensitivity:** α·χ must be resolved above the mass-defect floor (the λ_γ ≥ 5×10⁻⁹ sensitivity is superseded pending recalibration).

**Experiment simulator:** `gravity_v2.py` (`decoupling_prediction_v2`); legacy `gravity_experiment.py` retained for the deprecated law.

**Mass-defect confound:** If damage adds energy ΔE, the mass change is Δm = ΔE/c². For a 1kg test mass with ΔE = 1J, Δm ≈ 10⁻¹⁷ kg, producing a relative gravitational change of ~10⁻¹⁷. The DET signal (ΔF = F_κ) must exceed this; the fractional \(F_\kappa/F_N = \alpha\chi\) must be resolved above ~10⁻¹⁷.

### 2.3 Combined Signature (Smoking Gun)

> **RETIRED (Round 6, Option B).** Withdraws with §2.2 — there is no gravity decoupling to cross-check. κ is measured via the structural proxy alone.

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

## 3. Newtonian Correspondence (legacy κ-only; superseded by gravity_v2)

> **Deprecated (Round 3).** This section records the κ-only correspondence (`newton_correspondence.py`, `a = −G_q·γ/r²`). It is a *correspondence check* (Kepler recovered because the law is Newtonian with `m → κ`), and its source law is superseded by the two-source field equation in §2.2 / `gravity_v2.py`. Retained for historical audit.

| Observable | Match |
|---|---|
| 1/r² force law | Exact |
| ∇²Φ = 4πG_q·ρ_γ | Identical form (κ replaces mass) |
| Kepler 1 (ellipses) | e < 0.001 |
| Kepler 2 (area law) | σ/μ < 10⁻⁶ |
| Kepler 3 (T² ∝ r³) | Ratio 0.99994 |
| Orbital velocity | \(v = \sqrt{G_q\gamma/r}\) |

**Difference (legacy):** this section sources gravity with κ alone (now deprecated). The active law (§2.2) keeps mass as the conserved source with κ as a modifier.

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

## 8. Post-Newtonian κ-Gravity (Solar System Tests)

> **RETIRED (Round 6, Option B).** This and the following §§9–11 belong to the withdrawn gravity-modification program. DET does not modify gravity; the solar-system/galaxy/cluster analyses are retained for historical audit only.

DET κ-gravity extends naturally to the relativistic regime through \(G_{eff}(r) = G \cdot \kappa(r)/\kappa_{earth}\).

**All four classical GR tests passed:**

| Test | DET prediction | Bound | Status |
|---|---|---|---|
| Mercury perihelion | 9.9×10⁻⁴ arcsec/century excess | ±0.04 | ✅ |
| Cassini Shapiro delay | γ−1 ≈ 2.0×10⁻⁵ | <2.3×10⁻⁵ | ✅ |
| Light deflection | Δκ/κ ≈ 1.5×10⁻⁵ | <10⁻⁴ | ✅ |
| Binary pulsar | Δκ < 6.7×10⁻⁴ | | ✅ |

**Natural scale separation:** The galactic κ(r) profile (r_core ≈ 1 kpc, δκ ≈ 2.0) extrapolated to solar-system scales gives δκ(1 AU) ≈ 10⁻⁸ — 2000× below the Cassini bound. DET reproduces GR exactly at solar-system scales while producing MOND-like effects at galactic scales. No fine-tuning.

Module: `post_newtonian.py`.

---

## 9. Galaxy Rotation Curves (SPARC Analysis)

DET κ-gravity explains flat galaxy rotation curves without dark matter.

> **Linear re-derivation (Round 3, `gravity_v2`):** the rotation curve now uses the two-source law \(v^2 = G(1+\alpha\chi)\,M/r\) with \(\chi = (\kappa-\kappa_{eq})/\kappa_{earth}\) — **linear** in κ, replacing the deprecated quadratic \((\kappa/\kappa_{earth})^2\), which with κ ∈ [0,1] is **≤ Newtonian** (it cannot enhance gravity at all — its old "success" came entirely from κ exceeding 1). With κ clamped to [0,1], a single coupling \(\alpha \approx 16\) (broad minimum 14–18) reproduces flat curves in 42/43 of the sample (mean RMS ~19%). **Ceiling (R6-B):** with κ ∈ [0,1] and a single α, the maximum enhancement is \(1+\alpha(1-\kappa_{eq})/\kappa_{earth} \approx 9\times\), so the law covers at most the mildest disk-galaxy discrepancies — NOT dwarf (~50×) or cluster (~100×) scales. See `sparc_analysis.scan_alpha` and `det_units.coupling_implications`.

### Phenomenological fit (135 galaxies)
- κ(r) = 0.7 + 4.0·(1−e^(−r/20kpc))
- Mean RMS: 31%, within ±20%: 37%, within ±50%: 83%

> **⚠ Reproducibility (Round 3 red-team, open).** The "135 galaxies" figure and the quoted RMS/20%/50% statistics are **not reproducible from the committed tree**: `sparc_analysis.py` hardcodes 43 galaxies and `det8/data/sparc_subset.json` is empty. The "RMS" is a single outermost-point fractional error, not a curve-level RMS. The numbers above are from an uncommitted analysis.

### κ(r) parameterization with r_SFR scale

> **F6 status (Round 3):** the `Σ_*/Σ_SFR/age` derivation is now **implemented** (`kappa_derivation.kappa_from_galaxy_properties` uses `M_star`, `SFR`, `age`, `r_d`, `r_SFR` — no fitted constants). **But the derivation fails the sign test:** for inside-out growth (r_SFR > r_d, all 8 known galaxies), it gives κ **decreasing** with radius (Δκ < 0), the opposite of what flat rotation curves require. The "reset ∝ recent SFR" mechanism has the wrong radial profile; a correct derivation needs a reset driver more concentrated than the stars (r_reset < r_d) or an accumulation term more extended than the SFR. See `radial_gradient_check`.

\[
\kappa(r) = \kappa_0 + \kappa_{\text{scale}} \cdot (1 - e^{-r/r_{\text{SFR}}})
\]

**DET mechanism:** In the core, rapid star formation → frequent supernova events → κ reset → low κ (~0.5). In the outskirts, low SFR → rare resets → κ accumulates over billions of years → high κ (~3.5). The transition scale r_SFR is a galaxy-specific observable (SFR scale length), replacing the averaged 20 kpc from the phenomenological fit.

**Universal parameters:** κ₀ = 0.5, κ_scale = 3.0. Galaxy-specific: r_SFR (1–8 kpc, from observations).

**Results on 8 test galaxies:** κ_core 0.5–0.8, κ_outskirts 3.4–3.5, ratio 5–6×, (κ/κ_earth)² ≈ 12× enhancement at large radii. Matches phenomenological fit with fewer free parameters and no galaxy-by-galaxy tuning.

Module: `sparc_analysis.py`, `kappa_derivation.py`.

---

## 10. Galaxy Cluster Dynamics

DET κ-gravity extends naturally to cluster scales (100–3000 kpc).

**Universal κ(r): galaxy → cluster (continuous):**

| Scale | r (kpc) | κ | Enhancement |
|---|---|---|---|
| Galaxy core | 0.1 | 0.7 | 1× |
| Galaxy disk | 1–10 | 1.8–3.5 | 3–12× |
| Galaxy outskirts | 30 | 3.5 | 12× |
| Cluster transition | 100 | 4.3 | 19× |
| Cluster virial | 300 | 5.9 | 35× |
| Cluster outskirts | 1000–3000 | 7.3–7.5 | 54–56× |

**Results on 10 clusters (A133 through Coma):**
- Avg κ at r_virial: 7.4
- κ reduction factor: (κ/κ_earth)² = 0.018
- Required mass reduced by 98.2% at cluster scales

**Comparison:**
| Theory | Galaxy DM | Cluster DM |
|---|---|---|
| ΛCDM | 85% | 85% |
| MOND | 0% | ~50% |
| **DET κ-gravity** | **0%** | **~0%** |

DET uniquely eliminates dark matter at BOTH galaxy and cluster scales.
MOND still requires ~2× dark matter in clusters.

Module: `cluster_dynamics.py`.

---

## 11. Dataset Constraints

| Dataset | Module | Result |
|---|---|---|
| Atomic clocks (NIST, Tokyo, PTB) | `experimental_constraints.py` | λ_P < 4×10⁻¹⁸ (Δκ=0.5) |
| Eötvös (MICROSCOPE) | `experimental_constraints.py` | Terrestrial materials must have nearly equal κ (a *consistency requirement*, not a test passed) |
| Flyby anomalies | `flyby_anomaly.py` | κ_sc/κ_earth ≈ 1 ± 10⁻⁶ |
| Galaxy rotation curves (135) | `sparc_analysis.py` | κ(r) physics-based: RMS 31.5%, no dark matter |
| Galaxy clusters (10) | `cluster_dynamics.py` | Universal κ 0.7→7.5. 98% mass reduction. No DM at any scale. |
| Solar system GR tests | `post_newtonian.py` | All 4 tests passed |

---

## 12. r_SFR Prediction from Scaling Relations

Eliminates the last fitted parameter in κ(r). r_SFR is now predicted from galaxy observables:

\[
r_{\text{SFR}} = r_d \cdot (1.5 + 0.3\log_{10} M_* - 0.1\log_{10} \text{sSFR})
\]

Clamped to observed range [1.2, 2.5]. Larger r_SFR/r_d → stronger inside-out growth → steeper κ(r) → flatter rotation curves.

---

## 13. U(1) Emergence from Z₂

Complex amplitudes emerge from discrete sign statistics:
1. **Proven:** CLT → Gaussian effective amplitudes
2. **Proven:** Circular symmetry → U(1) phase invariance
3. **Proven:** Continuous interference from relative phases
4. **Conjectured:** Convergence rates (Berry-Esseen), uniqueness (quantum reconstruction)

---

## 14. GPS Satellite Clock Analysis

> **⚠ Vacuous bound (Round 3 red-team).** The λ_P bounds quoted below (and in `MODEL_CARD.md` §8) are constraints on the *product* λ_P·Δκ, where Δκ between two clocks is **assumed, not measured**. λ_P is therefore unconstrained by existing clock data until the structural proxy produces an actual κ value. The model-independent statement is λ_P·Δκ < σ.

GPS constrains κ differences in the orbital environment:
- Standard GR correction: +38.5 μs/day (verified to 0.3 ns/day)
- Orbital Δκ ≈ 10⁻⁸ to 10⁻⁶ (fabrication + orbital environment)
- λ_P < 3.5×10⁻⁹ — 10⁹× weaker than lab clocks
- **Finding:** κ is dominated by material processing history, not gravitational environment. Lab experiments with controlled κ preparation are the right approach.

Module: `gps_analysis.py`.

---

## 15. Continuum Limit Status (L1-L4)

> **⚠ Dimensional caveat (Round 3 red-team).** The empirical convergence rates quoted below (α ≈ 0.50, 0.75, 0.85) are all measured in **1+1 Minkowski**. The physically relevant 3+1 case is the slowest (N^(−1/4)) and is not yet computed. The "α=0.50" headline should be read with this caveat.

| Lemma | Statement | Status |
|---|---|---|
| L1 | Causal structure → (M, g) causal structure | **Proven** (causal set theory) |
| L2 | Coarse-grained Π → conformal factor Ω(x) | Numerical evidence (α=0.50 convergence). Formal proof open. |
| L3 | Reconstructed metric g_N → g | Statistical convergence verified (CV 0.56→0.25). LGH proof open. |
| L4 | κ-density → G_μν = 8πG_q·T^κ_μν | Newtonian verified. Discrete action sketch. GR limit open. |

DET's unique contribution: Π fixes the conformal factor (bare causal sets cannot). κ provides native matter content. **Complete mathematical framework — see `docs/CONTINUUM_LIMIT_FRAMEWORK.md`.**

Module: `continuum_limit_proof.py`, `continuum_limit_l234.py`.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, GOVERNANCE.md, ROADMAP.md.**
