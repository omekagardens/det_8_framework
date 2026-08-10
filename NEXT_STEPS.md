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

### Dataset Analysis
- **Atomic clocks:** λ_P < 4×10⁻¹⁸ (NIST Yb/Sr 2021, assuming Δκ=0.5)
- **Eötvös:** κ ∝ Z excluded by MICROSCOPE (η < 1.5×10⁻¹⁵). Terrestrial materials must have nearly equal κ.
- **Flyby anomalies:** κ_sc/κ_earth ≈ 1 ± 10⁻⁶. Galileo I vs II opposite signs → anomaly not simply κ-gravity.
- **SPARC galaxies (43):** κ(r) = 1.0 + 2.0·(1−e^(−r/1kpc)). Mean RMS 19%. 56% within ±20%. No dark matter needed.
- **Solar system:** All GR tests passed. δκ(1AU) ≈ 10⁻⁸ from galactic profile → 2000× below Cassini bound.

### Code
- 30 modules, 97/97 tests
- Full simulation stack: records, bonds, events, κ-diffusion, time evolution, gravity, unified simulation
- Experimental simulators: clock anomaly, gravity decoupling
- Dataset analysis: experimental constraints, flyby, SPARC, post-Newtonian

---

## What's Next (Priority Order)

### 1. Full SPARC 175-galaxy fit
- Download actual SPARC rotation curve data from literature
- Fit universal κ(r) to all 175 galaxies
- Compare with ΛCDM dark matter halo fits
- **Impact:** Could establish DET as a viable dark matter alternative

### 2. Galaxy cluster dynamics
- Extend κ(r) model to cluster scales (r ~ 100–1000 kpc)
- Test whether κ-gravity explains cluster velocity dispersions and lensing masses
- **Impact:** Closes the loop from solar system → galaxy → cluster scales

### 3. κ(r) model refinement
- Derive κ(r) from physical principles (star formation rate, mass accretion history) rather than phenomenological fit
- Predict κ(r) from galaxy formation simulations
- **Impact:** Makes κ(r) a derived quantity, not a fitted one

### 4. GPS satellite clock analysis
- GPS clocks apply relativistic corrections. Any residual could be a κ signal.
- IGS (International GNSS Service) data is public.
- **Impact:** Laboratory-scale test of κ-gravity in Earth's vicinity

### 5. Multi-particle κ-diffusion
- Extend single-particle κ-diffusion to N-particle systems
- Derive effective viscosity, thermal conductivity from κ-dynamics
- **Impact:** Condensed matter predictions

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

## Quick Reference

```bash
python3 run_tests.py   # 97/97 passing
```

**Primary entry point:** `MODEL_CARD.md`
