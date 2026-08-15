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
| P0.7 | Joint kernel + basis | O4 resolved. O8 resolved. |
| P0.8 | Confluence + O7 | O3 resolved. O7 resolved (5-step, later retired: Π conformal factor → count, T7 order-and-count). |
| — | Red-team (2 rounds) | All 10 challenges addressed. 4 closed, 3 narrowed, 3 open research frontiers. |
| — | Dataset analysis | Clock bounds, Eötvös, flyby, SPARC 135 galaxies (31% RMS), post-Newtonian, clusters, κ(r) derivation, BAO, r_SFR prediction, GPS, continuum limit L2-L4. |
| — | Remaining items | All 5 addressed. Mathematical review applied (M0 fix, claim-status revision). |
| — | Continuum limit | Architecture implemented. Finite-model numerical evidence supports convergence pathways. Formal CT remains open. 14 continuum-limit modules. See `docs/CONTINUUM_LIMIT_FRAMEWORK.md`. |

---

## Current State

**Record-Kernel Physics theorem program complete** (T1–T7 + T2a + T6b + T6 residual + why-ℂ). Honest landmarks: T6 lands on **almost-quantum not quantum**; T2a is a negative result (grade-2 empirical, not a-priori forced); T6 residual resolved (bare 𝔇-extendability trivial; collapse = NPA under a sharpened reading); T7 is estimator verification (manifoldlike emergence open); why-ℂ addressed (ℝ falsified empirically; ℂ forced by reversible dynamics O∩Sp=U(m)).

**384/384 tests passing.**
**95 code modules** (MODEL_CARD §7 documents a selected subset).
**5 primary documents replacing 24.**

### Two tracks

| Track | Status |
|---|---|
| A — Physical Calculus | Theorem program complete and honest; ONE active falsifiable prediction (κ-Π clock anomaly, gated on F9 + independent κ, currently null). See `FALSIFICATION_LEDGER.md`. |
| B — Ontological Grammar | 4 deadlocks resolved. Mature. Relational-creation research (RC1/RC2) active. |

### Classification

DET v8.0 is a disciplined interpretive framework with a fully derived physical calculus and pre-registered experimental predictions. Candidate physical theory pending experimental validation.

---

## Remaining Work (Requires External Resources)

### Experimental (needs lab access)
- Atomic clock collaboration for κ-Π anomaly test
- Torsion balance for κ-gravity decoupling
- Physical κ structural proxy apparatus

### Observational (needs telescope data)
- Full SPARC rotation curve data points (individual radii)
- DESI/Euclid BAO data for κ(z) constraint
- Galaxy cluster mass profile data (Chandra/XMM archives)

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
# Expected: 384/384 passed, 0 failed, 0 errors
```

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md.**
