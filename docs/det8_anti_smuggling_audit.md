# DET v8.0 — Anti-Smuggling Audit: Derived vs Borrowed (Revised)

**Date:** August 9, 2026 (revised after observable derivations)
**Purpose:** Full audit of every DET 8 model — what is derived from DET primitives, what is borrowed from standard physics, and what is assumed/inherited. Updated to reflect Born rule, CHSH, gravity, and Lorentz derivations.

---

## Global Derivation Status

### Now Derived from DET Primitives (was borrowed)

| Observable | Was | Now | Derivation module |
|---|---|---|---|
| Born rule \(K(i)=|c_i|^2\) | Borrowed (QM) | **Derived** | `born_derivation.py` |
| CHSH \(S=2\sqrt{2}\) | Borrowed (QM) | **Derived** | `chsh_derivation.py` |
| E(a,b) = cos(2(a-b)) | Borrowed (QM) | **Derived** | `chsh_derivation.py` |
| 1/r² force law | Newtonian placeholder | **Derived** | `det_gravity.py` |
| Field equation ∇²Φ = 4πG_q·ρ | Newtonian placeholder | **Derived** | `det_gravity.py` |
| Kepler's laws (all 3) | Assumed | **Derived** | `newton_correspondence.py` |
| Time dilation | Lorentz factor inserted | **Derived** | `lorentz_derivation.py`, `det_native_spacetime.py` |
| Length contraction | Not addressed | **Derived** | `lorentz_derivation.py` |
| Relativity of simultaneity | Not addressed | **Derived** | `lorentz_derivation.py` |
| Lorentz transformations | Assumed from SR | **Derived** | `lorentz_derivation.py` |
| Velocity addition | Assumed from SR | **Derived** | `lorentz_derivation.py` |
| c as speed limit | Assumed | **Derived** | `lorentz_derivation.py` |
| Pointer-record formation | Kraus/POVM (MAM-Q) | **Derived** | `det_native_measurement.py` |
| Amplitude structure (ℂ) | Borrowed (QM) | **Derived** | `chsh_derivation.py` |
| Hilbert space | Borrowed (QM) | **Derived** | `born_derivation.py`, `chsh_derivation.py` |

### Still Borrowed / Assumed

| Item | Status | Why |
|---|---|---|
| Lorentzian causal structure of ≺ | **Assumed** | Causal set theory (O7). Not derived, but same assumption as all causal set approaches. |
| c as finite constant | **Empirical** | Measured, not derived. |
| Continuum limit of event graph | **Assumed** | Open problem (causal set theory). |
| Embedding dimension 3+1 | **Assumed** | Open problem (causal set theory). |
| κ-gravity coupling G_q | **Free parameter** | Must be calibrated. Degenerate with λ_γ. |
| λ_γ (κ→mass conversion) | **Free parameter** | Degenerate with G_q. Broken by Π clock anomaly. |

---

## Audit by Model

### MAM-0 (`mam0.py`)

| Element | Status | Notes |
|---|---|---|
| Record with integer value | DET-derived | Record = committed fact. DET primitive. |
| Law map generates Ω from record | DET-derived | L: R⁻ → (Ω, K). DET primitive. |
| Conservation in Ω construction | DET-derived | All ω ∈ Ω satisfy sum conservation. |
| Commit kernel (uniform) | DET-derived | K(ω) = 1/|Ω|. Simplest DET kernel. |
| Commit map writes successor | DET-derived | Commit: (R⁻, X) → R⁺. DET primitive. |
| Actualizer (pseudorandom) | DET-derived | Seed for reproducibility. Not ontology. |
| Scheduler independence | DET-derived | Different schedules, same invariants. |
| **Verdict: 100% DET-derived.** | | |

---

### MAM-Q (`mamq.py`)

| Element | Status | Notes |
|---|---|---|
| Qubit state (α, β) | **BORROWED** | Complex amplitudes from standard QM. Not derived from DET record structure. |
| Born rule P(0)=|α|² | **BORROWED** | Born rule is provisional calibration (H/O). Not DET-derived. |
| Kraus operators (POVM) | **BORROWED** | Standard quantum measurement theory. |
| Pointer record | DET-derived | Classical committed outcome. DET primitive. |
| Measurement commit | DET-derived | Outcome → pointer record write. DET primitive. |
| No-signalling test | DET-derived | Checked from DET kernel marginals. |
| Bell state | **BORROWED** | Standard QM state. DET needs relational record model. |
| **Verdict: ~40% DET-derived.** | Heavy QM borrowing. | |

---

### Peres-Mermin (`peres_mermin.py`)

| Element | Status | Notes |
|---|---|---|
| Pauli matrices | **BORROWED** | Standard QM operators. |
| Tensor products | **BORROWED** | Standard QM composition. |
| Matrix multiplication | **BORROWED** | Linear algebra (unavoidable). |
| Row/column product verification | DET-derived | Checking constraints on observables. |
| Noncontextual assignment proof | DET-derived | Combinatorial contradiction. DET interpretation. |
| **Verdict: ~30% DET-derived.** | QM correspondence model. | |

---

### CHSH (`chsh.py`)

| Element | Status | Notes |
|---|---|---|
| Bell state | **BORROWED** | Standard QM. |
| Correlation function E(a,b)=cos(2(a-b)) | **BORROWED** | Standard QM result. DET needs joint kernel derivation. |
| CHSH inequality bound | **BORROWED** | Standard Bell theorem mathematics. |
| Monte Carlo simulation | DET-derived | Numerical verification. |
| **Verdict: ~20% DET-derived.** | Pure QM correspondence harness. | |

---

### DET 8 Core (`det8_core.py`)

| Element | Status | Notes |
|---|---|---|
| NodeRecord (κ, σ, F, H, C, r, θ, η) | DET-derived | DET record variables. |
| Participation aperture Π | DET-derived | Π = f(κ, σ, F, H). DET primitive. |
| κ-drag on Π | DET-derived | Π ∝ 1/(1+λ_P·κ). Pure DET. |
| Proper time as event accumulation | DET-derived | τ = Σ Π_e. DET primitive. |
| κ-damage / κ-recovery | DET-derived | Record-side dynamics. |
| κ-Jubilee | **M/H** | Boundary operator. Not in minimal core. |
| Clock ratio | DET-derived | τ_A/τ_B from Π ratio. |
| Lorentz factor (original) | **BORROWED** | γ inserted by hand in original det8_core. |
| **Verdict: ~80% DET-derived.** | Lorentz factor is the main borrowed element. | |

---

### DET-Native Spacetime (`det_native_spacetime.py`) — NEW

| Element | Status | Notes |
|---|---|---|
| φ(v) from causal graph geometry | DET-derived | Event density ratio from ≺. Replaces inserted Lorentz factor. |
| Lorentzian causal structure | **ASSUMED** | ≺ approximates Minkowski in continuum limit. Same assumption as causal set theory. |
| c as maximum signal speed | **ASSUMED** | Empirical fact; not derived. |
| DET-native Π (no γ insertion) | DET-derived | Π = (record factors) × φ(v). Pure DET. |
| Clock comparison | DET-derived | κ and velocity effects from Π. |
| **Verdict: ~85% DET-derived.** | Causality structure assumed, not derived. | |

---

### DET-Native Measurement (`det_native_measurement.py`) — NEW

| Element | Status | Notes |
|---|---|---|
| Apparatus bits as records | DET-derived | ApparatusBit is a Record element. |
| Measurement as commit events | DET-derived | Each event: L → Ω → actualize → Commit. |
| Commit kernel (fidelity-weighted) | DET-derived | K(outcome \| target) = fidelity if correct. |
| Pointer record from consensus | DET-derived | r = majority vote of apparatus bits. |
| Pointer strength r | DET-derived | Fraction agreeing with consensus. |
| Redundancy | DET-derived | N × pointer_strength. |
| No Hilbert space | DET-derived | No amplitudes, no operators. |
| No Born rule | DET-derived | Kernel specified directly, not from |ψ|². |
| No collapse | DET-derived | Information transfer, not state reduction. |
| **Verdict: 100% DET-derived.** | Pure DET-native measurement model. | |

---

### Joint Kernel (`joint_kernel.py`)

| Element | Status | Notes |
|---|---|---|
| RelationalRecord | DET-derived | Record spanning two nodes. |
| Nonfactorizable joint kernel API | DET-derived | K(A,B \| R, a, b) — DET primitive. |
| Specific K form (cos correlation) | **BORROWED** | Standard QM result. |
| No-signalling verification | DET-derived | Marginal independence check. |
| CHSH from joint kernel | DET-derived | Computing S from K. |
| **Verdict: ~50% DET-derived.** | Architecture is DET; correlation function is borrowed. | |

---

### q-Gravity (`q_gravity.py`)

| Element | Status | Notes |
|---|---|---|
| γ = λ_γ·κ (gravitational charge) | DET-derived | From D3r1 ontology fork. |
| ρ = γ - γ_b (source contrast) | DET-derived | DET gravity source. |
| Newtonian force law F ∝ γ_i·γ_j/r² | **BORROWED** | Newtonian form. DET field equation not derived. |
| Euler integration | DET-derived | Numerical method. |
| Decoupling test | DET-derived | κ-recovery → gravity change without F change. |
| **Verdict: ~60% DET-derived.** | Gravity source is DET; force law is Newtonian placeholder. | |

---

## Summary

| Model | % DET-derived | Main borrowed elements |
|---|---|---|
| MAM-0 | 100% | — |
| DET-native measurement | 100% | — |
| DET-native spacetime | 85% | Lorentzian causal structure (assumed) |
| DET 8 Core | 80% | Lorentz factor (now fixed in native version) |
| q-Gravity | 60% | Newtonian force law |
| Joint Kernel | 50% | QM correlation function |
| MAM-Q | 40% | Born rule, Kraus operators, Hilbert space |
| Peres-Mermin | 30% | Pauli operators, QM formalism |
| CHSH | 20% | Bell state, correlation function |

### What's Fully DET-Derived (No Borrowing)
1. Record structure and commit cycle (MAM-0, core)
2. Participation aperture and proper time (core, native spacetime)
3. κ-drag on clock rates (core)
4. Pointer-record formation from consensus (native measurement)
5. Conservation in Ω construction (MAM-0, bonds)
6. Causal event graph and spacelike detection
7. Confluence analysis
8. Nonfactorizable joint kernel architecture (form, not function)

### What's Still Borrowed (Needs DET-Native Derivation)
1. **Born rule** — P(i) = |⟨i|ψ⟩|². Critical. Without it, quantum sector is borrowed.
2. **Amplitude structure** — Complex numbers, Hilbert space. Where do they come from in DET?
3. **CHSH correlation function** — E(a,b) = cos(2(a-b)). Needs DET joint kernel derivation.
4. **Gravitational field equation** — Newtonian ∇²Φ = 4πGρ is a placeholder.
5. **Lorentzian causal structure** — Assumed from relativity. Derivation from ≺ is causal set theory (O7).

### Honest Assessment
DET has a **fully native classical/stochastic sector** (records, kernels, commit, measurement, proper time). The quantum sector and gravitational sector still borrow from standard physics. The next phase should target the Born rule and the gravitational field equation as the two highest-priority DET-native derivations.
