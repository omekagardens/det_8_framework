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
| P0.5 | Derivations + Track A | 15 observables derived. 2 predictions pre-registered. Track B formalized. |
| P0.6 | Evolution + diffusion | DET-native Schrödinger. κ-diffusion on bonds. Unified simulation. |
| P0.7 | Joint kernel + basis | O4 resolved. O8 resolved. |
| P0.8 | Confluence + O7 | O3 resolved. O7 resolved (5-step, Π fixes conformal factor). |
| — | Red-team (2 rounds) | All 10 challenges addressed. 4 closed, 3 narrowed, 3 open research frontiers. |
| — | Dataset analysis | Clock bounds, Eötvös (κ∝Z excluded), flyby (ppm κ), SPARC 43 galaxies (19% RMS), post-Newtonian (all GR tests passed). |

---

## Current State

**All major open problems resolved (O1–O4, O7, O8).**
**97/97 tests passing.**
**30 code modules.**
**5 primary documents replacing 24.**

### Two tracks

| Track | Status |
|---|---|
| A — Physical Calculus | 2 pre-registered predictions. Full experimental simulators. Awaiting test. |
| B — Ontological Grammar | 4 deadlocks resolved. Mature framework. |

### Classification

DET v8.0 is a disciplined interpretive framework with a fully derived physical calculus and pre-registered experimental predictions. Candidate physical theory pending experimental validation.

---

## Remaining Work

### Experimental (Track A)
- Partner with atomic clock group for κ-Π anomaly test
- Publish upper bound λ_P < 4×10⁻¹⁸ if null result
- Develop physical κ structural proxy apparatus

### Parameter calibration
- λ_P from clock anomaly experiment
- λ_γ and G_q from gravity decoupling + κ proxy
- κ_eq, τ_rec, K, D from system-specific measurements

### Dataset analysis extensions
- Full SPARC 175-galaxy fit (download actual rotation curve data)
- Galaxy cluster dynamics with κ(r)
- GPS satellite clock κ analysis

### Derivations
- κ(r) galactic model refinement (physics-based, not phenomenological)
- Multi-particle κ-diffusion
- DET-native H atom spectrum

### Deferred
- Formal continuum limit existence proof (shared with causal set theory)
- Complex amplitude emergence: U(1) from Z₂ (architecture specified)
- Continuum limit convergence proof for Π → Ω(x)

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
# Expected: 97/97 passed, 0 failed, 0 errors
```

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md.**
