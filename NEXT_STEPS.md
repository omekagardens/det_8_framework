# DET v8.0 — Next Steps

**Date:** August 14, 2026
**Test suite:** 376/376 passing
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
- 94 modules, 376/376 tests
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

Remaining open item (research, not implementation):
- why-ℂ (complex field selection) — open, feeds T6's full resolution (sketch: 𝔇=G+iΩ → complex structure J²=−I).

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
| `docs/falsification_protocol.md` | Lab-executable protocol for the three probes. |
| `docs/applied_physics.md` | Applied-physics program (5 tests + adversary + findings). |
| `NEXT_STEPS.md` | This document. |

```bash
python3 run_tests.py   # 376/376 passing
```
