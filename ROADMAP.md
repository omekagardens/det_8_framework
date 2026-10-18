# DET v8.0 — Roadmap

**Published programme overview, updated October 18, 2026.**
The phase table preserves the earlier project history. Current priorities are
defined below and in [Next Steps](NEXT_STEPS.md).

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

**Conditional native mathematics is consolidated:** the [theorem package](docs/track_b/native_theorem_package_v1/THEOREM_PACKAGE.md) collects the exact admitted finite law, support, small-amplitude positive result, kernel alternatives and 30/33/38 exclusions. Its [law-dependence companion](docs/track_b/native_theorem_package_v1/LAW_DEPENDENCE.md) identifies which choices change the law. The stated premises and unresolved historical-coordinate/actual-branch questions remain.

**RET tooling is retained; RET development is paused.** Earlier Exodus, neutron-lifetime, mathematical-search and Navier–Stokes results remain historical bounded studies with their original caveats.

**Validation is scoped to individual checks and recorded runs.** Earlier aggregate counts and module totals are not current release guarantees. Software integration, finite scientific checks, production qualification and physical validation are separate outcomes.

### Deliverables ahead

| Deliverable | Completion criterion |
|---|---|
| Public theorem package | A reader can identify each established claim, exact law/support and remaining premise without reading chronological coordination logs. |
| Law dependence | State what is forced, optional, construction-specific or proved over a declared family; close a bounded result before extending the coefficient audit. |
| Prospective portable replay | Reproduce one fixed public GWOSC calculation in a newly documented environment and independently check its arithmetic; preserve historical custody failures. |
| Foundational physics | Supply an explicit native prediction and observation channel before claiming empirical evidence for the theory. |
| Application value | Evaluate a fixed diagnostic or signal-processing benchmark against declared baselines, costs, failure rates and held-out data. |

Full production qualification remains separate from the portable replay. A
successful conventional benchmark does not establish a native gravity law.

### Two tracks

| Track | Status |
|---|---|
| A — Physical Calculus | Finite/computed theorem-program results plus one active falsifiable prediction (κ-Π clock anomaly), gated on F9 and independent κ. See `FALSIFICATION_LEDGER.md`. |
| B — Ontological Grammar | Governed synthesis and conditional native-growth research; metaphysical claims remain separated from mathematical and empirical evidence. |

### Classification

DET v8.0 is a disciplined interpretive framework with a record-kernel reconstruction program, correspondence checks, RET research tooling, and one gated pre-registered experimental prediction. It is not yet an empirically validated physical theory.

---

## Remaining Work and Prerequisites

The [current work plan](NEXT_STEPS.md) is authoritative for sequencing. The
items below retain earlier programme goals; they do not authorize work in the
paused RET lane or bypass experimental and protected-validation gates.

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

## Integration and validation

Follow [Branch Workflow](docs/BRANCH_WORKFLOW.md) for regular reviewed
`ret` → `main` integration. Its maintenance checks are separate from the
numerical/research aggregator `run_tests.py` and the explicitly selected
[research check registry](docs/RESEARCH_CHECKS.md). Report actual outcomes
and limitations for the exact revision tested; do not reuse an old passing count.

---

**See also: MODEL_CARD.md (primary), ONTOLOGY.md, PHYSICS.md, GOVERNANCE.md.**
