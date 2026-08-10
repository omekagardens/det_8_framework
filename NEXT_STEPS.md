# DET v8.0 — Current Status & Next Steps

**Date:** August 10, 2026
**Test suite:** 97/97 passing

---

## What's Been Done

### Theory (all phases complete)
- 15 observables derived from DET primitives (Born rule, CHSH, gravity, Lorentz, pointer formation, amplitudes)
- 6/6 open problems resolved (O1–O4, O7, O8)
- 2 Track A predictions pre-registered (κ-Π clock anomaly, κ-gravity decoupling)
- Track B ontological grammar formalized (4 deadlocks resolved)
- 2-round adversarial red-team review (all challenges addressed)

### Dataset Analysis (5 datasets, all published results)
| Dataset | Key result |
|---|---|
| Atomic clocks (NIST, Tokyo, PTB) | λ_P < 4×10⁻¹⁸ (Δκ=0.5) |
| Eötvös (MICROSCOPE) | κ ∝ Z EXCLUDED |
| Flyby anomalies | κ_sc/κ_earth ≈ 1 ± 10⁻⁶; Galileo inconsistency |
| **SPARC galaxies (135)** | **κ(r)=0.7+4.0·(1−e^(−r/20kpc)), RMS 31%, 37% ±20%, 83% ±50%** |
| Solar system (post-Newtonian) | All 4 GR tests passed; δκ(1AU) ≈ 10⁻⁸ |

### Code
- 30 modules, 97/97 tests
- Full simulation stack + experimental simulators + dataset analysis modules

---

## What's Next (Priority Order)

### 1. κ(r) model refinement (HIGH)
- Replace phenomenological fit with physics-based κ(r) from star formation rate + mass accretion history
- **Impact:** Makes κ(r) a derived quantity, not a fitted one. Could explain the 31% RMS scatter.

### 2. Galaxy cluster dynamics (HIGH)
- Extend κ(r) to cluster scales (100–1000 kpc)
- Test whether κ-gravity explains cluster velocity dispersions and lensing masses
- **Impact:** Closes the loop solar system → galaxy → cluster

### 3. Multi-particle κ-diffusion (MEDIUM)
- Extend to N-particle systems; derive effective viscosity, thermal conductivity
- **Impact:** Condensed matter predictions

### 4. GPS satellite clock analysis (MEDIUM)
- IGS data is public; any residual relativistic correction could be κ signal
- **Impact:** Laboratory-scale test of κ-gravity

### 5. Full SPARC rotation curve data (LOW — catalog done)
- Download individual galaxy rotation curve data points (not just V_flat)
- Fit κ(r) to full velocity profiles, not just flat velocity
- **Impact:** More precise κ(r) constraints; could reduce RMS

### Deferred
- Formal continuum limit proof (shared with causal set theory)
- Complex amplitude emergence: U(1) from Z₂ (architecture specified)
- DET-native H atom spectrum

---

## Documentation

| Document | Content |
|---|---|
| `MODEL_CARD.md` | **Primary reference.** Primitives, derivations, dataset results, code inventory. |
| `PHYSICS.md` | Track A: predictions, experiments, Newton/Lorentz/SPARC/post-Newtonian. |
| `ONTOLOGY.md` | Track B: deadlocks, metaphysics, agency, relativistic growing block. |
| `GOVERNANCE.md` | F8-OPEN, claim register, decision gates, Bell position. |
| `ROADMAP.md` | Phase history, current state, remaining work. |
| `NEXT_STEPS.md` | This document. |

---

```bash
python3 run_tests.py   # 97/97 passing
```
