# DET v8.0 — Next Steps

**Date:** August 13, 2026
**Test suite:** 314/314 passing
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
- 89 modules, 314/314 tests
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
- ✅ T3 record formation — implemented
- ✅ T4 kernel irreversibility (`⟨e^{−Σ}⟩=1−λ`, `⟨Σ⟩≥0`) — implemented
- ✅ T5 local-kernel continuum (graph Laplacian → diffusion; coefficients from moments) — implemented
- T6 correlation class (the long pole: pair-kernel 𝔇 + why-ℂ)
- T7 order-and-count geometry (kinematic only; gravity stays out of scope)

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
python3 run_tests.py   # 314/314 passing
```
