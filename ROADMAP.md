# DET v8.0 — Roadmap

**Phase history, current state, remaining work.**
**Condensed from AGENTS.md and all phase cards.**

---

## Phase History

| Phase | Focus | Key outcome |
|---|---|---|
| P0.1 | Architecture proposal | Event graph, record, law map, possibility object defined |
| P0.3 | Governance baseline | Adversarial holdings, F8-OPEN, anti-smuggling rules frozen |
| P0.4 | Construction sprint | Formal core + MAM-0 + MAM-Q + F8-OPEN v2 + Bell memo |
| P0.4r1.1 | Adversarial revision | Downgraded openness to M. κ-γ split. Two-axis claim register. |
| P0.5 | Derivations + Track A | 10 active + 5 retired correspondence checks. 1 prediction pre-registered. Track B formalized. |
| P0.6 | Evolution + diffusion | DET-native Schrödinger. κ-diffusion on bonds. Unified simulation. |
| P0.7 | Joint kernel + basis | O4 finite construction and O8 apparatus-controllability account implemented; analytic/global results remain open. |
| P0.8 | Confluence + O7 | Finite confluence and causal-geometry estimators implemented; continuum/manifoldlike emergence remains open. |
| — | Red-team (2 rounds) | All 10 challenges addressed. 4 closed, 3 narrowed, 3 open research frontiers. |
| — | Dataset analysis | Clock, Eötvös, flyby, SPARC, cluster, BAO, and GPS analyses completed; gravity-related interpretations were subsequently retired under Option B. |
| — | Remaining items | All 5 addressed. Mathematical review applied (M0 fix, claim-status revision). |
| — | Continuum limit | Architecture implemented. Finite-model numerical evidence supports convergence pathways. Formal CT remains open. 14 continuum-limit modules. See `docs/CONTINUUM_LIMIT_FRAMEWORK.md`. |

---

## Current State

**Record-Kernel Physics finite/computed program implemented** (T1–T7 + T2a + T6b + T6 residual + why-ℂ), with open assumptions and continuum results tracked explicitly. Key limits: T2a shows grade-2 is empirical rather than forced; T7 is estimator verification rather than manifoldlike emergence; the complex-structure result assumes one phase form and reversible dynamics.

**RET integrated:** general relational inference, Exodus endpoint accounting, neutron-lifetime calibration design, governed mathematical searches, and bounded Navier–Stokes protocols.

**651/651 tests passing.**
**128 model modules / 144 Python files.**

### Two tracks

| Track | Status |
|---|---|
| A — Physical Calculus | Finite/computed theorem-program results plus one active falsifiable prediction (κ-Π clock anomaly), gated on F9 and independent κ. See `FALSIFICATION_LEDGER.md`. |
| B — Ontological Grammar | Governed synthesis addressing four deadlocks; metaphysical claims remain separated from empirical validation. Relational-creation research is active. |

### Classification

DET v8.0 is a disciplined interpretive framework with a record-kernel reconstruction program, correspondence checks, RET research tooling, and one gated pre-registered experimental prediction. It is not yet an empirically validated physical theory.

---

## Remaining Work (Requires External Resources)

### Experimental (needs lab access)
- F9 recovery-rate experiment on raw \(R(t)\) records
- Independent κ preparation and structural-proxy calibration
- Atomic-clock collaboration only after the prerequisite gates pass

### RET validation and replication
- Measured Exodus apparatus/calibration inputs and conventional endpoint closure
- Absolute neutron proton-detection audit with documented covariance
- Independent validation for higher Riemann computations and fresh RET records
- Spatial/temporal Navier–Stokes convergence rectangle plus independent replication

### Mathematical (long-term / speculative)
- why-ℂ residual: why exactly ONE phase Ω and why reversible dynamics (§3.4, speculative)
- Manifoldlike emergence (embedding + uniqueness) — open, inherited from causal set theory (T7)
- Berry-Esseen convergence rates for U(1) emergence (minor)

---

## Key Documents

| Document | Content |
|---|---|
| `MODEL_CARD.md` | **Primary reference.** Primitives, derivations, predictions, code inventory. |
| `ONTOLOGY.md` | Track B: four deadlocks, metaphysics ledger, agency quarantine, fruit-first. |
| `PHYSICS.md` | Track A: predictions, experiments, derivations, anti-smuggling. |
| `GOVERNANCE.md` | F8-OPEN, claim register, decision gates, Bell position, confluence. |
| `ROADMAP.md` | This document. Phase history, current state, remaining work. |

---

## Running Tests

```bash
python3 run_tests.py
# Expected: 651/651 passed, 0 failed, 0 errors
```

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md.**
