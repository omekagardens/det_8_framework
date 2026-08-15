# DET v8.0 — Next Steps

**Date:** August 14, 2026
**Test suite:** 400/400 passing
**Status:** Framework architecture complete. Theory, derivations, dataset analyses, and continuum-limit modules implemented. Formal continuum proofs remain long-term mathematical work.

---

## What's Been Done (Complete)

### Theory
- 10 active + 5 retired correspondence checks
- 6 open problems addressed (CI/AT, see MODEL_CARD §6)
- 1 Track A prediction pre-registered (κ-Π clock anomaly)
- Track B ontological grammar formalized (4 deadlocks)
- 2-round adversarial red-team review
- U(1) emergence formalized
- r_SFR predicted from scaling relations

### Dataset Analysis (9 analyses, all public data)
| Dataset | Key result |
|---|---|
| Atomic clocks | λ_P < 2×10⁻¹⁷ (refined Δκ) |
| Eötvös (MICROSCOPE) | κ ∝ Z excluded |
| Flyby anomalies | ppm-level κ differences |
| SPARC galaxies (135) | Physics-based κ(r): RMS 31.5%, no DM |
| Galaxy clusters (10) | 98% mass reduction, no DM |
| Solar system | All 4 GR tests passed |
| Cluster mass profiles | β-model fits, 94–98% reduction |
| BAO constraint | \|Δκ\|/κ < 0.02 |
| r_SFR prediction | From scaling relations, not fitted |

### Code
- 97 modules, 400/400 tests
- Full simulation stack + experimental simulators + dataset analysis

### Applied-Physics Real Data
- Full-year 2023 IGS GNSS clock products downloaded (365 daily `IGS0OPSFIN_*_30S_CLK.CLK.gz`, CDDIS)
- κ-recovery vs IEEE log-aging adversarial on 12 GPS satellites → **null**
  (κ wins 0/12; IEEE 7/12; quadratic 5/12 — the lone apparent κ win, G11, was
  a quadratic-trough false positive). See `docs/applied_physics.md` §5.
- IBM Quantum calibration ingest live (ibm_fez, 156 qubits) + daily launchd poll
  (`com.det.ibm-poll`)

---

## What's Next (theorem program + data)

### Theorem program (`docs/record_kernel_physics.md`)
- ✅ T1 predictive-history sufficiency — implemented
- ✅ T2b quadratic commit — implemented
- ✅ T2a grade-2 justification — implemented (negative result: grade-2 is NOT forced a priori — an explicit normalized positive grade-3 measure with I_3≠0 exists; the discriminator is empirical §7.2)
- ✅ T3 record formation — implemented
- ✅ T4 kernel irreversibility (`⟨e^{−Σ}⟩=1−λ`, `⟨Σ⟩≥0`) — implemented
- ✅ T5 local-kernel continuum (graph Laplacian → diffusion; coefficients from moments) — implemented
- ✅ T6 correlation class — implemented (local 2 / quantum & almost-quantum 2√2 / no-signalling 4; SOS certificate; Q ⊆ almost-quantum, Q⊊Q̃ cited)
- ✅ T6b correlation-class frontier — implemented (TLM/Masanes exact Q for (2,2,2), verified on the vector model; B inequality separates Q̃ from Q; NPA convergence makes "global record extendability ⇒ Q" a theorem)
- ✅ T6 residual (record extendability) — resolved (bare 𝔇-marginal extendability is trivial; the Q̃→Q collapse holds iff "record extendability" is read as the operator-algebra / NPA-moment-matrix consistency, settling the residual)
- ✅ T7 order-and-count geometry — implemented (kinematic only: order ⇒ null structure, count ⇒ conformal factor, order+count ⇒ dimension; estimator verification on known sprinklings, manifoldlike emergence left open)
- ✅ why-ℂ (complex field selection) — addressed (ℝ ruled out empirically — real QM falsified; ℂ forced by reversible dynamics O∩Sp=U(m) → J=G⁻¹Ω with J²=−I; ℍ excluded by the single phase Ω)

Residual (speculative, not implementation):
- why-ℂ assumptions — why exactly ONE phase Ω (single arrow of time) and why reversible dynamics; the §3.4 speculative targets.

### Track B (relational creation)
- ✅ RC1.2 formalized (`det8/models/relational_creation.py`) — σ_ij / A_ij / L_i / M_iG code-auditable; surfaced two new Track-A falsification levers: **FL-4 κ-reversibility** (latent capacity persists) and **FL-5 κ-transfer** (externalization relocates, not annihilates). See `FALSIFICATION_LEDGER.md`.
- ✅ FL-4/FL-5 physical realization (`det8/models/relational_realization.py`) — σ/A map onto materials observables (σ↔cohesion, A↔recoverable capacity); FL-4 = the EXTENT test (full vs partial recovery), complementing F9's RATE test. Remaining gap: a calibrated structural proxy.

### Falsification (the traction infrastructure)
- `FALSIFICATION_LEDGER.md` — the register: FL-1 clock (Class I, gated), FL-2/FL-3 almost-quantum + grade-3 discriminators (Class II, **pre-registered**, low-traction one-directional), FL-4 κ-reversibility (**physically realized** — extent test), FL-5 κ-transfer (downstream), FL-6/FL-7 candidates.

### Data (§7, matched to DET primitives)
- Matched-state / different-history ensembles (H₀: K_a = K_b + held-out transport)
- Alternative-combination counts (I_2, I_3)
- Forward/reverse trajectory datasets (Σ[ω] path irreversibility)

### Clock (late-stage, weakly identified)
- Common-mode universality test (`y = Bκ + u·1 + ε`); gated on F9 + independent κ.

---

## Documentation

| Document | Content |
|---|---|
| `MODEL_CARD.md` | **Primary reference.** Complete. |
| `PHYSICS.md` | Track A. Complete. |
| `ONTOLOGY.md` | Track B. Complete. |
| `GOVERNANCE.md` | Constraints. Complete. |
| `ROADMAP.md` | Phase history. Updated. |
| `FALSIFICATION_LEDGER.md` | **The register of every falsifiable prediction + falsifier + status.** |
| `docs/falsification_protocol.md` | Lab-executable protocol for the three probes. |
| `docs/applied_physics.md` | Applied-physics program (5 tests + adversary + findings). |
| `NEXT_STEPS.md` | This document. |

```bash
python3 run_tests.py   # 400/400 passing
```
