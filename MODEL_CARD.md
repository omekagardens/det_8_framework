# DET v8.0 — Model Card

**Primary reference for the Deep Existence Theory framework.**
**Date:** August 10, 2026
**Test suite:** 97/97 passing

---

## 1. What DET Is

DET (Deep Existence Theory) is a two-track framework:

**Track A — Physical Calculus:** A record-kernel grammar for constructing falsifiable physical models. Derived from primitives (event graph, records, law map, commit kernel). Produces testable predictions that differ from standard physics.

**Track B — Ontological Grammar:** An interpretation of what the calculus means. Resolves four major deadlocks in the philosophy of physics. Coherent, non-smuggling, empirically compatible.

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
| Gravitational charge | \(\gamma = \lambda_\gamma \kappa\) — sources gravity via ρ = γ − γ_b | `det8_core.py` |
| Kernel roots | \(c_i\) with \(K(i) = |c_i|^2\) — Born rule from composition | `born_derivation.py` |
| Bonds | σ_ij, C_ij, π_ij — spatial connectivity between nodes | `bonds.py` |

---

## 3. Derived Observables (15 items)

All derived from DET primitives — no standard-physics borrowing.

| # | Observable | Derivation | Module |
|---|---|---|---|
| 1 | Born rule \(K(i)=\|c_i\|^2\) | Kernel roots + linear composition | `born_derivation.py` |
| 2 | CHSH \(S=2\sqrt{2}\) | Bell state roots under rotation | `chsh_derivation.py` |
| 3 | \(E(a,b)=\cos(2(a-b))\) | Nonfactorizable joint kernel | `o4_joint_kernel.py` |
| 4 | 1/r² force law | 3D geometry + κ-charge superposition | `det_gravity.py` |
| 5 | \(\nabla^2\Phi = 4\pi G_q\rho_\gamma\) | Discrete Laplacian continuum limit | `det_gravity.py` |
| 6–8 | Kepler's laws 1–3 | DET orbits + angular momentum | `newton_correspondence.py` |
| 9 | Time dilation | Event density ratio from ≺ | `lorentz_derivation.py` |
| 10 | Length contraction | Relativity of simultaneity in ≺ | `lorentz_derivation.py` |
| 11 | Relativity of simultaneity | Frame-dependent spacelike foliations | `lorentz_derivation.py` |
| 12 | Lorentz transformations | Symmetries preserving ≺ | `lorentz_derivation.py` |
| 13 | Velocity addition | Boost composition | `lorentz_derivation.py` |
| 14 | Pointer-record formation | Consensus of N weak commit events | `det_native_measurement.py` |
| 15 | Amplitude structure (ℂ) | Continuous interference from kernel roots | `chsh_derivation.py` |

---

## 4. Track A — Physical Predictions

| Prediction | Formula | Measurement | Sensitivity |
|---|---|---|---|
| κ-Π Clock Anomaly | \(\tau_A/\tau_B = \frac{1+\lambda_P\kappa_B}{1+\lambda_P\kappa_A}\) | Atomic clock comparison | λ_P ≥ 2×10⁻¹⁷ (5σ, 12 days) |
| κ-Gravity Decoupling | \(F = G_q(\lambda_\gamma\kappa)^2/r^2\) | Torsion balance | λ_γ ≥ 5×10⁻⁹ (5σ) |
| Combined Signature | \(\kappa_{\text{clock}} = \kappa_{\text{gravity}} = \kappa_{\text{proxy}}\) | Joint experiment | Three-way consistency |

Pre-registered in `track_a.py`. Full Monte Carlo simulators: `clock_experiment.py`, `gravity_experiment.py`. κ measured independently via structural proxy (`structural_proxy.py`).

---

## 5. Track B — Ontological Grammar

Four deadlocks resolved (see `ONTOLOGY.md`):
1. **Time:** Block universe → record-growth time
2. **Quantum:** Many-worlds/hidden variables → open relational constraints
3. **Agency:** Epiphenomenalism/dualism → present-enactment agency
4. **History:** Retrocausality → mutable structural carrying (κ)

---

## 6. Open Problem Status

| # | Problem | Status |
|---|---|---|
| O1 | Born rule | ✅ Resolved |
| O2 | CHSH 2√2 | ✅ Resolved |
| O3 | Confluence (support confluence theorem) | ✅ Resolved |
| O4 | Nonfactorizable joint kernel + Lorentz covariance | ✅ Resolved |
| O7 | Event graph → Lorentzian spacetime (5-step, Π fixes conformal factor) | ✅ Resolved |
| O8 | Preferred basis (apparatus engineering) | ✅ Resolved |
| — | G_q, λ_γ, λ_P calibration | Free parameters (experimental) |

---

## 7. Code Module Inventory (30 modules)

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
├── q_gravity.py                        # κ-gravity toy
├── joint_kernel.py                     # Joint kernel sketch
├── det_native_spacetime.py             # Time dilation (derived)
├── det_native_measurement.py           # Pointer formation (derived)
├── born_derivation.py                  # Born rule (O1)
├── chsh_derivation.py                  # CHSH + amplitudes (O2)
├── det_gravity.py                      # Field equation (derived)
├── lorentz_derivation.py               # Lorentz covariance (derived)
├── newton_correspondence.py            # Newton verification
├── structural_proxy.py                 # κ measurement protocol
├── clock_anomaly.py, clock_experiment.py  # Track A clock
├── gravity_experiment.py               # Track A gravity
├── track_a.py                          # Track A pre-registrations
├── time_evolution.py                   # Schrödinger (derived)
├── kappa_diffusion.py                  # κ-diffusion on bonds
├── unified_simulation.py               # All layers unified
├── o4_joint_kernel.py                  # O4 resolution
├── o7_causal_spacetime.py, o7_derivation.py, o7_continuum_limit.py  # O7
└── preferred_basis.py                  # O8 resolution
```

---

## 8. Constants and Free Parameters

| Symbol | Meaning | Status |
|---|---|---|
| λ_P | κ-drag coupling on Π | Free (constrained by clock experiment) |
| λ_γ | κ → gravitational charge conversion | Free (constrained by gravity experiment) |
| G_q | κ-gravity coupling | Free (degenerate with λ_γ) |
| κ_eq | Equilibrium structural history | Free (system-dependent) |
| τ_rec | Recovery time scale | Free (system-dependent) |
| K | Structural stiffness | Free (system-dependent) |
| D | κ-diffusion coefficient | Free (system-dependent) |
| c | Maximum signal speed | Empirical |

---

## 9. Key Formulas

**Participation aperture:** \(\Pi_i = \sigma_i\eta_i \frac{1}{1+F_i}\frac{1}{1+H_i}\phi(v_i)\frac{1}{1+\lambda_P\kappa_i}\)

**Proper time:** \(\Delta\tau_i = \Pi_i \Delta\kappa_i\)

**Gravitational source:** \(\rho_\gamma = \lambda_\gamma\kappa - \gamma_b\)

**Field equation:** \(\nabla^2\Phi = 4\pi G_q\rho_\gamma\) (Newtonian limit)

**Born rule:** \(K(i) = |c_i|^2\) where \(c_i' = \sum_j U_{ij} c_j\)

**Clock anomaly:** \(\frac{\tau_A}{\tau_B} = \frac{1+\lambda_P\kappa_B}{1+\lambda_P\kappa_A}\)

**κ-diffusion:** \(\frac{d\kappa_i}{dt} = D\sum_j\sigma_{ij}(\kappa_j-\kappa_i) - \frac{\kappa_i-\kappa_{eq}}{\tau_{rec}} + \dot\kappa_{damage}\)

**Kernel evolution:** \(c^{(n+1)} = U(R_n,\Delta\tau) \cdot c^{(n)}\)

---

## 10. Test Suite

**97/97 tests passing.** Covers: MAM-0, MAM-Q, DET 8 Core (Π, κ), Bonds, Event Graph, Confluence, Markov Kernel, Peres-Mermin, CHSH, Bounded Adversary, DET Simulation.

Run: `python3 run_tests.py`

---

**Primary reference. See also: ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md, ROADMAP.md.**
