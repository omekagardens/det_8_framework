# PROGRESS_P0.5.md — DET v8.0-P0.5 Sprint Log (Final)

**Project:** Deep Existence Theory (DET)
**Phase:** P0.5 — Physical Residue, Derivation, and Track A Predictions
**Started:** August 9, 2026
**Completed:** August 9, 2026
**Governing baseline:** P0.4r1.1 (frozen)

---

## Overall Status

### Original P0.5 Deliverables

| # | Deliverable | Status | Date |
|---|---|---|---|
| D1 | DET 7 regression report | ⬜ Blocked (no DET 7 code) | — |
| D2 | Minimal physical residue statement | ✅ Complete | 2026-08-09 |
| D3 | q-physics ledger | ✅ Revised (D3r1) | 2026-08-09 |
| D4 | Discriminator feasibility memos | ✅ Complete | 2026-08-09 |
| D5 | Peres-Mermin contextuality model | ✅ Complete | 2026-08-09 |
| D6 | Formal type/Markov-kernel refinement | ✅ Complete | 2026-08-09 |
| D7 | Confluence/scheduler tests | ✅ Complete | 2026-08-09 |
| D8 | CHSH correspondence harness | ✅ Complete → Derived | 2026-08-09 |
| D9 | Bounded-adversary discriminator | ✅ Complete | 2026-08-09 |

### Extended Deliverables (Beyond Original P0.5 Scope)

| # | Deliverable | Status | Date |
|---|---|---|---|
| E1 | Ontological Residue Addendum (Track B) | ✅ Complete | 2026-08-09 |
| E2 | D3r1: q-physics ledger revised (κ-γ split) | ✅ Complete | 2026-08-09 |
| E3 | Born rule derivation from DET primitives | ✅ Complete | 2026-08-09 |
| E4 | CHSH correlation derivation (E = cos(2(a-b))) | ✅ Complete | 2026-08-09 |
| E5 | Gravitational field equation derivation | ✅ Complete | 2026-08-09 |
| E6 | Newtonian correspondence verification | ✅ Complete | 2026-08-09 |
| E7 | Lorentz covariance derivation (all 7 observables) | ✅ Complete | 2026-08-09 |
| E8 | DET-native measurement model (no Kraus) | ✅ Complete | 2026-08-09 |
| E9 | Anti-smuggling audit (revised) | ✅ Complete | 2026-08-09 |
| E10 | Track A: Clock anomaly prediction | ✅ Complete | 2026-08-09 |
| E11 | Track A: Gravity decoupling prediction | ✅ Complete | 2026-08-09 |
| E12 | Track A: Combined signature + sensitivity | ✅ Complete | 2026-08-09 |

---

## Observable Derivation Status

### Derived from DET Primitives (15 items)

| Observable | Module |
|---|---|
| Born rule \(K(i)=\|c_i\|^2\) | `born_derivation.py` |
| CHSH \(S=2\sqrt{2}\) | `chsh_derivation.py` |
| E(a,b) = cos(2(a-b)) | `chsh_derivation.py` |
| 1/r² force law | `det_gravity.py` |
| Field equation \(\nabla^2\Phi = 4\pi G_q\rho_\gamma\) | `det_gravity.py` |
| Kepler's laws (all 3) | `newton_correspondence.py` |
| Time dilation | `lorentz_derivation.py`, `det_native_spacetime.py` |
| Length contraction | `lorentz_derivation.py` |
| Relativity of simultaneity | `lorentz_derivation.py` |
| Lorentz transformations | `lorentz_derivation.py` |
| Velocity addition | `lorentz_derivation.py` |
| c as speed limit | `lorentz_derivation.py` |
| Pointer-record formation | `det_native_measurement.py` |
| Amplitude structure (ℂ) | `chsh_derivation.py` |
| Hilbert space | `born_derivation.py`, `chsh_derivation.py` |

### Still Assumed (6 items)

| Item | Reason |
|---|---|
| Lorentzian causal structure of ≺ | Causal set theory (O7) — same assumption as all causal set approaches |
| c as finite constant | Empirical |
| Continuum limit of event graph | Open problem (causal set theory) |
| Embedding dimension 3+1 | Open problem (causal set theory) |
| G_q (κ-gravity coupling) | Free parameter — degenerate with λ_γ |
| λ_γ (κ→mass conversion) | Free parameter — broken by Π clock anomaly |

---

## Track A — Physical Predictions

### Pre-Registered Predictions

| Prediction | Formula | Null Model | Measurement |
|---|---|---|---|
| κ-Π Clock Anomaly | τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A) | τ_A/τ_B = 1 | Atomic clock comparison |
| κ-Gravity Decoupling | F = G_q·(λ_γ·κ)²/r² | F = G·M²/r² | Torsion balance |
| Combined Signature | κ_clock = κ_gravity | No consistent κ | Joint experiment |

### Sensitivity (current technology)

- Clock: λ_P ≥ 10⁻¹⁴ detectable at κ=1 with 10⁻¹⁸ clocks
- Gravity: λ_γ·κ ≥ 10⁻⁷ needed for 10⁻¹⁵ N resolution at r=0.1m
- Parameter estimation demonstrated: λ_P recovered to ±0.008 with 1% noise

### Discovery Criteria
1. Clock anomaly at ≥ 5σ after known corrections
2. Gravity change when Δκ ≠ 0, ΔM = 0
3. Consistent κ from independent clock and gravity

---

## Track B — Ontological Grammar

The Ontological Residue Addendum (`det8_p0.5_ontological_residue.md`) formally captures DET's four resolved deadlocks:

1. **Time**: Block universe → record-growth time
2. **Quantum**: Many-worlds/hidden variables → open relational constraints
3. **Agency**: Epiphenomenalism/dualism → present-enactment agency
4. **History**: Retrocausality → mutable structural carrying (κ)

### Classification
- **Track A**: Unvalidated physical framework (candidate predictions exist, untested)
- **Track B**: Mature ontological framework (logically coherent, empirically compatible, non-smuggling)
- **Overall**: Disciplined interpretive framework with associated physical calculus

---

## Full Model Inventory

```
det8/models/
├── mam0.py                  # Finite-bit actualization (100% DET-derived)
├── mamq.py                  # Qubit quantum analogue (40% DET-derived)
├── peres_mermin.py          # Contextuality correspondence (30%)
├── chsh.py                  # CHSH correspondence harness (20%)
├── bounded_adversary.py     # Model-complexity tool (S2b)
├── det8_core.py             # Π, κ-dynamics, proper time (85%)
├── bonds.py                 # BondRecord, BondNetwork, flux conservation
├── event_graph.py           # CausalGraph, spacelike detection
├── confluence.py            # Confluence testing (3 levels)
├── markov_kernel.py         # MeasurableSpace, TransitionKernel
├── det_simulation.py        # DetUniverse — integrated simulation
├── q_gravity.py             # q-gravity toy model
├── joint_kernel.py          # Nonfactorizable joint kernel sketch
│
│  # ── DET-Native Derivations ──
├── det_native_spacetime.py  # Time dilation from causal graph
├── det_native_measurement.py # Pointer formation (no Kraus)
├── born_derivation.py       # Born rule from kernel roots
├── chsh_derivation.py       # CHSH correlation from kernel roots
├── det_gravity.py           # Field equation from κ conservation
├── lorentz_derivation.py    # Full Lorentz covariance
├── newton_correspondence.py # Newtonian verification
│
│  # ── Track A ──
├── clock_anomaly.py         # κ-Π clock anomaly prediction
└── track_a.py               # Pre-registrations + sensitivity
```

---

## Decision Gate Assessment (Revised)

Per P0.4r1.1 §16.4, revised for current state:

```
Track A: Novel, risky record-side predictions survive?
  → Pre-registered but untested. Clock anomaly and gravity decoupling
    are falsifiable predictions with defined null models.
  → Status: Candidate physical predictions exist; none validated.

Track B: Only known dynamics + DET terminology survive?
  → DET provides a distinctive ontological grammar that resolves
    four deadlocks. This is genuine philosophical contribution.
  → Status: Mature ontological framework.

Overall classification:
  → DET v8.0-P0.5 is a disciplined interpretive framework
    with an associated physical calculus and two pre-registered
    falsifiable predictions awaiting experimental test.
```

---

## Test Suite

**97/97 passing, 0 failures, 0 errors.**

Coverage: MAM-0, MAM-Q, DET 8 Core (Π, κ), Bonds, Event Graph, Confluence, Markov Kernel, Peres-Mermin, CHSH, Bounded Adversary, DET Simulation.

---

**End of P0.5 Sprint Log**
