# DET v8.0 — Model Card

**Primary reference for the Deep Existence Theory framework.**
**Date:** August 14, 2026 (revised per mathematical review + re-foundation + T6/T6b/T7/T2a/T6-residual/why-ℂ/RC1.2/FL-realization)
**Test suite:** 407/407 passing

**Status:** DET8 is a **relational ontology** — the record-kernel unification of existence (event graph `≺`), participation (aperture Π), and becoming (commit kernel K) — with a physical calculus that is its measurable shadow. **The ontology is the primary content** (Track B: the four deadlocks — time, quantum, agency, history — resolved in one framework). Track A's κ-Π clock anomaly is an **optional empirical probe** of one physical realization (κ as an independent field) — not the point; DET's value does not depend on λ_P ≠ 0. Gravity is standard GR (Option B, Round 6); dark matter is standard. **The correlation class lands on almost-quantum (Q¹)** — the leading-order *effective* quantum level, consistent with the effective-field-theory nature of all real quantum theories (full quantum Q^∞ is the idealized UV-complete limit); collapse is the *commit* primitive (record formation), not a patch. General Born-rule uniqueness, scheduler-independent probability, continuum spacetime reconstruction, and global κ-identifiability remain open theorem programs. Track B supplies the relational substance — present participation, faith, healing, reciprocity — of which Track A's patterns are the measurable trace.

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
| Structural history | κ ∈ [0,1] — **L0/L1 fitted coordinate, not a primitive field** (rank-one special case of a predictive-history coordinate) | `det8_core.py` |
| Gravitational charge | \(\gamma = \lambda_\gamma \kappa\) — **RETIRED (Option B, no κ-gravity)** | `det8_core.py` |
| Pair-kernel (candidate) | \(\mathfrak D: \mathcal A \times \mathcal A \to \mathbb C\) — pre-commit relational possibility structure; \(K_\mathcal P(i)=\mathfrak D(A_i,A_i)\) on recordable partitions | *proposed (T2)* |
| Kernel roots | \(c_i\) with \(K(i) = |c_i|^2\) — **correspondence (CORR)**: Gram coordinates of \(\mathfrak D\), not primitives | `born_derivation.py` |
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

> **Revaluation (Aug 2026):** λ_P is a **free, underived** coupling — it enters only the participation aperture and is defined operationally (`λ_P = Π(0)/Π(1) − 1`), so the prediction is a one-parameter *family*, not a number. And because λ_P·κ is a joint product, the test is gated on two prerequisites that do not yet exist: a κ *preparation* protocol and an independent κ *measurement* (the proxy, which itself has an unsolved known-κ bootstrap). Option B is therefore ontologically clean but **empirically thin**: a single probe at the top of the ladder, conditional on F9 and the proxy landing. The ontology never required λ_P ≠ 0. Details: `PHYSICS.md` §2.1, `docs/falsification_protocol.md`.

> **Program name (re-foundation, Aug 2026):** the active physical program is **Record-Kernel Physics** (renamed from "κ-Physics"), with four sectors: (i) kernel geometry and history (T1 — κ as predictive-history compression); (ii) pair-kernel quantum reconstruction (T2/T6 — 𝔇); (iii) path irreversibility and measurement (T3/T4); (iv) causal order-and-count geometry (T7). The theorem program is specified in `docs/record_kernel_physics.md`.

---

## 5. Track B — Ontological Grammar

Four deadlocks addressed (see `ONTOLOGY.md` and `det_falsification.ontology_claim_register()`):

| Deadlock | Resolution | Epistemic status |
|---|---|---|
| **Time** | Block universe → record-growth time (Crystallizing Block) | **ADOPTED** (Ellis 2014) — borrowed, not DET-native |
| **Quantum** | Many-worlds/hidden variables → emergent complex amplitudes | **SKETCH** — U(1) emergence is an open program |
| **Agency** | Epiphenomenalism/dualism → present-enactment agency | **QUARANTINED** — the ontological gloss is Status M |
| **History** | Retrocausality → mutable structural carrying (κ) | **RELABELED** — standard internal-variable free energy |

None of the four is a DET-native derivation; the honest framing is a *coherent synthesis* of existing proposals, not "resolved from primitives" — a contribution in its own right, but stated as such.

---

## 6. Open Problem Status (Revised per Mathematical Review, Aug 2026)

Mathematical-evidence axis: D=Definition, I=Implemented, CI=Computed Instance, FT=Finite Theorem, AT=Analytic Theorem, CT=Continuum Theorem, PR=Pre-Registered, M=Metaphysical.

| # | Problem | Previous | Revised Status | What would constitute resolution |
|---|---|---|---|---|
| O1 | Born rule | ✅ Resolved | **CI** — Root representation + quantum correspondence; T2a: the quadratic (grade-2) form is NOT a-priori forced — an explicit normalized positive grade-3 measure with I₃≠0 exists, so grade-2 is an empirical choice | AT: §7.2 empirical I₃=0, or a genuinely new (non-grade-2) primitive |
| O2 | CHSH 2√2 | ✅ Resolved | **CI/FT** — CHSH supremum 2√2 proven (SOS); correlation classes characterized; Q for (2,2,2) = TLM/Masanes (verified); Q⊊Q̃ via the B inequality; "global record extendability ⇒ Q" is a theorem (NPA convergence), residual settled; why-ℂ addressed (ℝ falsified empirically; ℂ forced by reversible dynamics O∩Sp=U(m) → J=G⁻¹Ω) | AT: why one Ω / why reversible dynamics (speculative §3.4) |
| O3 | Confluence | ✅ Resolved | **CI/FT** — Support confluence in finite cases | AT: Distributional scheduler independence over all linear extensions |
| O4 | Joint kernel | ✅ Resolved | **CI** — Nonfactorizable finite construction | AT: Global consistency, analytic no-signalling, covariance |
| O7 | Event graph → Lorentzian | ✅ Resolved | **I/CI** — T7 order-and-count geometry: dimension/null-structure/conformal-factor estimators verified on known Minkowski sprinklings (Malament/HKM, Myrheim–Meyer cited) | CT: Manifoldlike emergence (embedding + uniqueness) — open, inherited from causal set theory |
| O8 | Preferred basis | ✅ Resolved | **I** — Apparatus-controllability account | FT: Redundant record formation stability theorem |
| M0 | Proper-time consistency | — | **FT** — Fixed: Δτ = Π·ΔN, N ≠ κ | — |
| **O9-RID** | **Resurrection identity bridge** | — | **Open** — PID-C/PID-M split. Track B. | Numerical identity across embodied interruption. See `docs/track_b/resurrection.md`. |
| **F9** | **Fact Genesis Protocol** | — | **Open** — Are facts discovered or created? Track B. 5-level ladder. | Distinguish unknown vs not-yet-existent facts. See `docs/track_b/fact_genesis.md`. |
| **F10** | **Law Genesis** | — | **Proposed** — Why is L stable? Track B. | Stability of the law map. See `docs/track_b/law_genesis.md`. |
| **F11** | **Cosmic Record** | — | **Proposed** — κ-field across cosmic time. Track B. | Not yet developed. |
| **F12** | **Anthropic Principle** | — | **FT/CI** — WAP selection confirmed; SAP necessity rejected; fine-tuning reduced to one scalar (participation-only, Option B — κ-gravity retired). Track B. | Prior-independent naturalness; promote "λ_P is the selection target" from P to PR. See `docs/track_b/anthropic_principle.md`. |
| — | Complex amplitudes | Correspondence (CORR) | **I** — Architecture specified; U(1) emergence sketch | AT: Field-selection theorem (ℂ vs ℝ vs ℍ) |
| — | κ dynamics | Phenomenological descriptor (L0/L1) | **I** — Reaction-diffusion toy | Rank test (scalar/vector) + held-out transport |
| — | Clock prediction | Weakly identified (FIT/PR) | **PR** — Gated parameterized hypothesis | EV: common-mode universality + identifiable parameters |

---

## 7. Code Module Inventory (selected subset)

> **Honest scoping (Round 3 red-team):** this is a **selected subset** — `det8/models/` contains 83 `.py` files. The list below omits the Track B simulation suite (`resurrection_simulation`, `atonement_simulation`, `afterlife_simulation`, `salvation_history`, `unified_death_sin`, `track_b_simulations`), the `rc1_*` research modules, the 14 `continuum_limit_*` modules, and several dataset-analysis modules.

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
├── det_falsification.py                # Falsification ladder + data guardrail
└── operational_kappa.py                # Precision-materials program (L0/L1/L2)
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

**407/407 tests passing** over the exercised module subset. Run: `python3 run_tests.py`

The test suite verifies **internal consistency**, not empirical validity:
- ✅ Code correctly implements mathematical axioms.
- ✅ Axioms are internally consistent (no contradictions).
- ✅ Derived observables match their expected values.

The test suite does **NOT** verify:
- ❌ That DET axioms map to physical reality.
- ❌ That DET makes correct empirical predictions.
- ❌ That κ, Π, or λ_P exist in nature.

**Coverage caveat (Round 3 red-team):** the 251 tests exercise only the toy models (`mam0`, `mamq`), the core primitives (`det8_core`, `bonds`, `event_graph`, `confluence`, `markov_kernel`, `det_simulation`), the quantum-correspondence toys (`peres_mermin`, `chsh`), `bounded_adversary`, `anthropic_principle`, the Track A clock/proxy code (`clock_experiment`, `clock_anomaly`, `track_a`, `structural_proxy`), the Round 3/6 resolution modules (`gravity_v2`, `kappa_discriminator`, `sparc_analysis`, `det_units`, `kappa_derivation`, `det_falsification`, `operational_kappa`), and the applied-physics suite (`adversarial`, `kappa_ingest`, `discriminator`, `applied_tests`, `ingest`). The physics-correspondence modules (`born_derivation`, `chsh_derivation`, `o4_joint_kernel`, `det_gravity`, `newton_correspondence`, `lorentz_derivation`, `time_evolution`, `preferred_basis`, …) and much of the astrophysics suite (`cluster_dynamics`, `post_newtonian`, `experimental_constraints`, `continuum_limit_*`, …) are currently **untested** by this runner.

Test count is a software engineering metric, not a physics validation metric. Empirical validation requires the Track A experiments.

---

**Primary reference. See also: ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md, ROADMAP.md, docs/CONTINUUM_LIMIT_FRAMEWORK.md, docs/track_b/resurrection.md.**
