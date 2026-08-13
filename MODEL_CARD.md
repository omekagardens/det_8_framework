# DET v8.0 — Model Card

**Primary reference for the Deep Existence Theory framework.**
**Date:** August 10, 2026 (revised per mathematical review)
**Test suite:** 208/208 passing

**Status:** DET8 implements a finite record-kernel framework that is the measurable shadow of a deeper relational ontology. It reproduces selected quantum, Newtonian, and Lorentzian formulas in constructed finite models and proposes **one** parameterized experimental anomaly (the κ-Π clock anomaly). **Gravity is standard GR — DET does not modify gravity** (Option B, Round 6); dark matter is not explained by DET. General Born-rule uniqueness, quantum-correlation characterization, scheduler-independent probability, continuum spacetime reconstruction, and global κ-identifiability remain open theorem programs. Track B supplies the relational substance — present participation, faith, healing, reciprocity — of which Track A's mathematical patterns are the measurable trace.

---

## 1. What DET Is

DET (Deep Existence Theory) is a two-track framework:

**Track A (Physical Calculus):** The measurable SHADOW. A record-kernel grammar for constructing falsifiable physical models. Its mathematical structures (L, Ω, K, κ, Π) approximately capture the relational dynamics of presence navigating possibility. Its fruit tests itself — the recursion IS the evidence that the underlying relational reality exists.

**Track B (Ontological Grammar):** The relational SUBSTANCE. Describes the ontological reality (present participation, relational continuity, faith, healing, reciprocity) of which Track A's patterns are the measurable trace. Track B does not merely "interpret" Track A — Track A is the shadow; Track B is the substance.

---

## 2. Primitives

| Primitive | Definition | Module |
|---|---|---|
| Event graph | \(\mathcal G = (V, \prec)\) — locally finite partial order | `event_graph.py` |
| Record | \(\mathcal R\) — committed facts at each node (κ, F, σ, H, C, r, θ, η) | `det8_core.py` |
| Law map | \(\mathcal L: \mathcal R^- \rightarrow (\Omega, \Sigma, K, \mathcal C)\) — generates possibility object | `mam0.py`, `det8_core.py` |
| Commit kernel | \(K: \Omega \rightarrow [0,1]\) — proper transition kernel | `markov_kernel.py` |
| Participation aperture | \(\Pi = \sigma \eta (1+F)^{-1}(1+H)^{-1}\phi(v)(1+\lambda_P\kappa)^{-1}\) — proper-time rate | `det8_core.py` |
| Structural history | κ ∈ [0,1] — record-side drag on Π | `det8_core.py` |
| Gravitational charge | \(\gamma = \lambda_\gamma \kappa\) — **DEPRECATED (Option B, no κ-gravity)** | `det8_core.py` |
| Kernel roots | \(c_i\) with \(K(i) = |c_i|^2\) — Born rule from composition | `born_derivation.py` |
| Bonds | σ_ij, C_ij, π_ij — spatial connectivity between nodes | `bonds.py` |

---

## 3. Observable Correspondence Checks (10 active + 5 retired)

These are **correspondence checks**, not derivations: each module shows that a standard result (Born rule, CHSH, Lorentz covariance) is recovered when DET's primitive `κ` (or a kernel root) is mapped onto the standard source/amplitude role. The step from DET primitives to the standard result is *assumed*, not derived — the genuine derivation program (O1–O4) remains open at status CI/AT per §6. This is a necessary consistency step, but it is not the same as a derivation.

**Option B (Round 6):** the 5 gravity/Kepler rows below are **RETIRED** — κ no longer sources gravity, so there is no κ-gravity to "correspond" to. They are retained for audit only. The 10 active rows are the quantum + Lorentz + measurement checks, tied to the participation/proper-time structure.

| # | Observable | Correspondence | Module |
|---|---|---|---|
| 1 | Born rule \(K(i)=\|c_i\|^2\) | Kernel roots + linear composition | `born_derivation.py` |
| 2 | CHSH \(S=2\sqrt{2}\) | Bell state roots under rotation | `chsh_derivation.py` |
| 3 | \(E(a,b)=\cos(2(a-b))\) | Nonfactorizable joint kernel | `o4_joint_kernel.py` |
| 4 | 1/r² force law | **RETIRED** — κ-charge superposition (no κ-gravity) | `det_gravity.py` |
| 5 | \(\nabla^2\Phi = 4\pi G_q\rho_\gamma\) | **RETIRED** — discrete Laplacian limit (no κ-gravity) | `det_gravity.py` |
| 6–8 | Kepler's laws 1–3 | **RETIRED** — DET orbits (no κ-gravity) | `newton_correspondence.py` |
| 9 | Time dilation | Event density ratio from ≺ | `lorentz_derivation.py` |
| 10 | Length contraction | Relativity of simultaneity in ≺ | `lorentz_derivation.py` |
| 11 | Relativity of simultaneity | Frame-dependent spacelike foliations | `lorentz_derivation.py` |
| 12 | Lorentz transformations | Symmetries preserving ≺ | `lorentz_derivation.py` |
| 13 | Velocity addition | Boost composition | `lorentz_derivation.py` |
| 14 | Pointer-record formation | Consensus of N weak commit events | `det_native_measurement.py` |
| 15 | Amplitude structure (ℂ) | Continuous interference from kernel roots | `chsh_derivation.py` |

---

## 4. Track A — Physical Predictions

> **Scope decision (Round 6, Option B):** DET is a participation/measurement theory, not a gravity-modification theory. The **sole** falsifiable prediction is the κ-Π clock anomaly (the λ_P channel). The gravity-decoupling prediction and the two-source law (α channel) are **RETIRED** — gravity is standard GR, and dark matter is not explained by DET.

| Prediction | Formula | Measurement | Sensitivity |
|---|---|---|---|
| κ-Π Clock Anomaly | \(\tau_A/\tau_B = \frac{1+\lambda_P\kappa_B}{1+\lambda_P\kappa_A}\) | Atomic clock comparison | λ_P ≥ 2×10⁻¹⁷ (5σ, 12 days) |

Pre-registered in `track_a.py`. Monte Carlo simulator: `clock_experiment.py`. κ measured independently via structural proxy (`structural_proxy.py`); the κ-vs-defect-density discriminator (`kappa_discriminator.py`) is the gating experiment.

---

## 5. Track B — Ontological Grammar

Four deadlocks resolved (see `ONTOLOGY.md`):
1. **Time:** Block universe → record-growth time
2. **Quantum:** Many-worlds/hidden variables → open relational constraints
3. **Agency:** Epiphenomenalism/dualism → present-enactment agency
4. **History:** Retrocausality → mutable structural carrying (κ)

---

## 6. Open Problem Status (Revised per Mathematical Review, Aug 2026)

Mathematical-evidence axis: D=Definition, I=Implemented, CI=Computed Instance, FT=Finite Theorem, AT=Analytic Theorem, CT=Continuum Theorem, PR=Pre-Registered, M=Metaphysical.

| # | Problem | Previous | Revised Status | What would constitute resolution |
|---|---|---|---|---|
| O1 | Born rule | ✅ Resolved | **CI** — Root representation + quantum correspondence | AT: Uniqueness theorem forcing quadratic form from DET axioms |
| O2 | CHSH 2√2 | ✅ Resolved | **CI** — Correct calculation for Bell construction | AT: Characterize DET correlation class, prove CHSH supremum |
| O3 | Confluence | ✅ Resolved | **CI/FT** — Support confluence in finite cases | AT: Distributional scheduler independence over all linear extensions |
| O4 | Joint kernel | ✅ Resolved | **CI** — Nonfactorizable finite construction | AT: Global consistency, analytic no-signalling, covariance |
| O7 | Event graph → Lorentzian | ✅ Resolved | **I/CI** — Architecture + numerical evidence | CT: Manifoldlikeness, metric convergence, curvature convergence |
| O8 | Preferred basis | ✅ Resolved | **I** — Apparatus-controllability account | FT: Redundant record formation stability theorem |
| M0 | Proper-time consistency | — | **FT** — Fixed: Δτ = Π·ΔN, N ≠ κ | — |
| **O9-RID** | **Resurrection identity bridge** | — | **Open** — PID-C/PID-M split. Track B. | Numerical identity across embodied interruption. See `docs/track_b/resurrection.md`. |
| **F9** | **Fact Genesis Protocol** | — | **Open** — Are facts discovered or created? Track B. 5-level ladder. | Distinguish unknown vs not-yet-existent facts. See `docs/track_b/fact_genesis.md`. |
| **F10** | **Law Genesis** | — | **Proposed** — Why is L stable? Track B. | Stability of the law map. See `docs/track_b/law_genesis.md`. |
| **F11** | **Cosmic Record** | — | **Proposed** — κ-field across cosmic time. Track B. | Not yet developed. |
| **F12** | **Anthropic Principle** | — | **FT/CI** — WAP selection confirmed; SAP necessity rejected; fine-tuning reduced to one combination. Track B. | Gravitational binding + inhomogeneous κ. See `docs/track_b/anthropic_principle.md`. |
| — | Complex amplitudes | Mostly derived | **I** — Architecture specified; U(1) emergence sketch | AT: Field-selection theorem (ℂ vs ℝ vs ℍ) |
| — | κ dynamics | Physical field | **I** — Phenomenological reaction-diffusion | AT: Well-posedness, invariant domain, energy balance |
| — | Clock prediction | Pre-registered | **PR** — Testable parameterized hypothesis | EV: Identifiable parameters + reproducible experiment |

---

## 7. Code Module Inventory (selected subset)

> **Honest scoping (Round 3 red-team):** this is a **selected subset** — `det8/models/` contains 82 `.py` files. The list below omits the Track B simulation suite (`resurrection_simulation`, `atonement_simulation`, `afterlife_simulation`, `salvation_history`, `unified_death_sin`, `track_b_simulations`), the `rc1_*` research modules, the 14 `continuum_limit_*` modules, and several dataset-analysis modules.

```
det8/models/
├── mam0.py, mamq.py                    # Toy models (M2-M3)
├── peres_mermin.py, chsh.py            # Quantum correspondence (D5, D8)
├── bounded_adversary.py                # Model-complexity (D9)
├── det8_core.py                        # Π, κ-dynamics, NodeRecord
├── bonds.py                            # BondRecord, BondNetwork
├── event_graph.py                      # CausalGraph, ≺, spacelike detection
├── confluence.py, confluence_resolution.py  # Confluence (O3)
├── markov_kernel.py                    # MeasurableSpace, TransitionKernel
├── det_simulation.py                   # Multi-node DetUniverse
├── q_gravity.py                        # κ-gravity toy (retired)
├── joint_kernel.py                     # Joint kernel sketch
├── det_native_spacetime.py             # Time dilation (derived)
├── det_native_measurement.py           # Pointer formation (derived)
├── born_derivation.py                  # Born rule (O1)
├── chsh_derivation.py                  # CHSH + amplitudes (O2)
├── det_gravity.py                      # Field equation (retired)
├── lorentz_derivation.py               # Lorentz covariance (derived)
├── newton_correspondence.py            # Newton verification
├── structural_proxy.py                 # κ measurement protocol
├── clock_anomaly.py, clock_experiment.py  # Track A clock
├── gravity_experiment.py               # Track A gravity (retired)
├── track_a.py                          # Track A pre-registrations
├── time_evolution.py                   # Schrödinger (derived)
├── kappa_diffusion.py                  # κ-diffusion on bonds
├── unified_simulation.py               # All layers unified
├── o4_joint_kernel.py                  # O4 resolution
├── o7_causal_spacetime.py, o7_derivation.py, o7_continuum_limit.py  # O7
├── preferred_basis.py                  # O8 resolution
├── anthropic_principle.py              # Anthropic Principle (F12)
├── gravity_v2.py                       # Two-source gravity (F2 resolution)
├── kappa_discriminator.py              # κ vs defect density (F9)
├── det_units.py                        # SI ↔ DET units conversion
└── det_falsification.py                # Falsification ladder + data guardrail
```

---

## 8. Dataset Analysis Results

> **Deprecated (Round 6, Option B):** the astrophysics rows below (galaxy rotation, clusters, solar-system κ-gravity, λ_P-from-clock "constraints" on gravity) belong to the **retired** gravity-modification program. DET no longer claims any gravitational anomaly; gravity is GR and dark matter is standard. These rows are retained for historical audit only.

> **⚠ Reproducibility & vacuity caveats (Round 3 red-team).** Several rows below are not reproducible from the committed tree or overstate what was established: (1) the SPARC "135 galaxies" fit uses 43 hardcoded galaxies with an empty data file; (2) all λ_P bounds are constraints on the *product* λ_P·Δκ with Δκ **assumed**, so λ_P is unconstrained until κ is independently measured; (3) "κ ∝ Z EXCLUDED" was a straw-man (no one proposed κ ∝ Z) — the legitimate statement is only that terrestrial materials have nearly equal κ; (4) "κ(r) from galaxy formation physics" is now **implemented** from Σ_*/Σ_SFR/age, but it gives the wrong radial direction (κ *decreases* with radius for the observed inside-out growth r_SFR > r_d) — the reset-by-SFR mechanism needs revision. See `PHYSICS.md` and `kappa_derivation.radial_gradient_check`.

| Dataset | Module | Key result |
|---|---|---|
| Atomic clock comparisons (NIST, Tokyo, PTB) | `experimental_constraints.py` | λ_P < 4×10⁻¹⁸ (Δκ=0.5); weakens to <2×10⁻¹² (Δκ=10⁻⁶) |
| Eötvös (MICROSCOPE, Eöt-Wash) | `experimental_constraints.py` | κ ∝ Z EXCLUDED. Terrestrial materials must have nearly equal κ. |
| Flyby anomalies (Galileo, NEAR, Rosetta) | `flyby_anomaly.py` | κ_sc/κ_earth ≈ 1 ± 10⁻⁶. Galileo I vs II opposite signs → inconsistent with single κ_sc. |
| SPARC galaxy rotation curves (135 galaxies) | `sparc_analysis.py` | κ(r)=0.7+4.0·(1−e^(−r/20kpc)) phenomenological. RMS 31%. 37% ±20%, 83% ±50%. |
| **κ(r) from galaxy formation physics** | `kappa_derivation.py` | **κ(r)=κ₀+κ_scale·(1−e^(−r/r_SFR)). Derived from SFR + inside-out growth. 2 universal params + 1 observable.** |
| Galaxy cluster dynamics (10 clusters) | `cluster_dynamics.py` | Universal κ 0.7→7.5. 98% mass reduction. No DM at any scale. |
| Solar system (Mercury, Cassini, binary pulsar) | `post_newtonian.py` | All GR tests passed. δκ(1AU) ≈ 10⁻⁸. |
| **r_SFR prediction from scaling relations** | `remaining_items.py` | r_SFR = r_d·(1.5+0.3·logM−0.1·log(sSFR)). Predicted, not fitted. |
| **Cluster mass profiles (β-model)** | `remaining_items.py` | M_DET(<r) reduction 94→98% over 50–1200 kpc. |
| **BAO constraint** | `remaining_items.py` | \|Δκ\|/κ < 0.02 (z=1100 to z=0). DESI/Euclid testable. |
| **Track A refined sensitivity** | `remaining_items.py` | λ_P < 2×10⁻¹⁷ (Δκ=0.1); up to λ_P < 2×10⁻¹⁶ (Δκ=0.01). |
| GPS satellite clocks (IGS) | `gps_analysis.py` | λ_P < 3.5×10⁻⁹ (Δκ≈10⁻⁶). Weaker than lab clocks. κ dominated by material history, not orbital environment. |
| **Continuum limit (CL1-CL11)** | `continuum_limit_*.py` (14 modules) | Candidate continuum-limit program: measure, metric, κ-field, curvature, LGH, BD action, stress-energy, Bianchi. Formal CT remains open. See `docs/CONTINUUM_LIMIT_FRAMEWORK.md`. |

---

## 9. Constants and Free Parameters
|---|---|---|
| λ_P | κ-drag coupling on Π | Free (constrained by clock experiment) |
| λ_γ | κ → gravitational charge conversion | **Deprecated** (legacy κ-only law) |
| G_q | κ-gravity coupling | **Deprecated** (legacy κ-only law) |
| α | κ-response coupling (gravity v2) | **Deprecated** (Option B — no fifth force) |
| κ_earth | κ normalization reference (gravity v2) | **Deprecated** (Option B — no fifth force) |
| κ_eq | Equilibrium structural history | Free (system-dependent) |
| τ_rec | Recovery time scale | Free (system-dependent) |
| K | Structural stiffness | Free (system-dependent) |
| D | κ-diffusion coefficient | Free (system-dependent) |
| c | Maximum signal speed | Empirical |

---

## 10. Key Formulas

**Participation aperture:** \(\Pi_i = \sigma_i\eta_i \frac{1}{1+F_i}\frac{1}{1+H_i}\phi(v_i)\frac{1}{1+\lambda_P\kappa_i}\)

**Proper time:** \(\Delta\tau_i = \Pi_i \Delta N_i\) with \(N\) the monotone event-count variable (\(N \neq \kappa\); M0 fix).

**Gravity (Option B):** standard GR — DET does not source or modify gravity. (The retired two-source law \(G_{eff} = G(1+\alpha\chi)\) is historical; see `gravity_v2.py`.)

**Born rule:** \(K(i) = |c_i|^2\) where \(c_i' = \sum_j U_{ij} c_j\)

**Clock anomaly:** \(\frac{\tau_A}{\tau_B} = \frac{1+\lambda_P\kappa_B}{1+\lambda_P\kappa_A}\)

**κ-diffusion:** \(\frac{d\kappa_i}{dt} = D\sum_j\sigma_{ij}(\kappa_j-\kappa_i) - \frac{\kappa_i-\kappa_{eq}}{\tau_{rec}} + \dot\kappa_{damage}\)

**Kernel evolution:** \(c^{(n+1)} = U(R_n,\Delta\tau) \cdot c^{(n)}\)

---

## 11. Test Suite

**208/208 tests passing** over **22 of 82 `.py` files** in `det8/models/`. Run: `python3 run_tests.py`

The test suite verifies **internal consistency**, not empirical validity:
- ✅ Code correctly implements mathematical axioms.
- ✅ Axioms are internally consistent (no contradictions).
- ✅ Derived observables match their expected values.

The test suite does **NOT** verify:
- ❌ That DET axioms map to physical reality.
- ❌ That DET makes correct empirical predictions.
- ❌ That κ, Π, or λ_P exist in nature.

**Coverage caveat (Round 3 red-team):** the 208 tests exercise only the toy models (`mam0`, `mamq`), the core primitives (`det8_core`, `bonds`, `event_graph`, `confluence`, `markov_kernel`, `det_simulation`), the quantum-correspondence toys (`peres_mermin`, `chsh`), `bounded_adversary`, `anthropic_principle`, the Track A clock/proxy code (`clock_experiment`, `clock_anomaly`, `track_a`, `structural_proxy`), and the Round 3/6 resolution modules (`gravity_v2`, `kappa_discriminator`, `sparc_analysis`, `det_units`, `kappa_derivation`, `det_falsification`). The physics-correspondence modules (`born_derivation`, `chsh_derivation`, `o4_joint_kernel`, `det_gravity`, `newton_correspondence`, `lorentz_derivation`, `time_evolution`, `preferred_basis`, …) and much of the astrophysics suite (`cluster_dynamics`, `post_newtonian`, `experimental_constraints`, `continuum_limit_*`, …) are currently **untested** by this runner.

Test count is a software engineering metric, not a physics validation metric. Empirical validation requires the Track A experiments.

---

**Primary reference. See also: ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md, ROADMAP.md, docs/CONTINUUM_LIMIT_FRAMEWORK.md, docs/track_b/resurrection.md.**
