# DET v8.0 — Deep Existence Theory

A disciplined two-track framework: a **record-kernel physical calculus** with correspondence checks and governed falsifiers, and an **ontological grammar** addressing four major deadlocks in the philosophy of physics.

## Quick Reference

| Document | Content |
|---|---|
| [`MODEL_CARD.md`](MODEL_CARD.md) | **Primary reference.** Primitives, 10 active + 5 retired correspondence checks, 1 prediction, RET research, formulas, and test coverage. |
| [`PHYSICS.md`](PHYSICS.md) | Track A — falsifiable predictions, experimental designs, anti-smuggling audit. |
| [`ONTOLOGY.md`](ONTOLOGY.md) | Track B — four deadlocks (time, quantum, agency, history), metaphysics ledger, agency quarantine. |
| [`docs/track_b/gravity.md`](docs/track_b/gravity.md) | Track B — gravity as the geometry of the growing record (Problem of Time, openness unification, present-tense constraints). |
| [`GOVERNANCE.md`](GOVERNANCE.md) | F8-OPEN protocol, adversary classes, claim register, decision gates, Bell position. |
| [`ROADMAP.md`](ROADMAP.md) | Phase history (P0.1→P0.8), current state, remaining work. |
| [`docs/EXODUS_DET_TRANSLATION.md`](docs/EXODUS_DET_TRANSLATION.md) | Governed Exodus equation audit, DET momentum closure, and boundary/history simulations. |
| [`docs/EXODUS_NEXT_RUNS.md`](docs/EXODUS_NEXT_RUNS.md) | Phase-2 boundary, momentum-inventory, history-detectability, and AC discriminator runs. |
| [`docs/EXODUS_FIELD_RUN.md`](docs/EXODUS_FIELD_RUN.md) | Geometry-aware 2-D Maxwell-stress, chamber, reversal, and source-topology run. |
| [`docs/EXODUS_FLOATING_SUPPLY_RUN.md`](docs/EXODUS_FLOATING_SUPPLY_RUN.md) | Charge-constrained floating-source, capacitance, leakage, and stray-capacitance run. |
| [`docs/EXODUS_3D_APPARATUS_RUN.md`](docs/EXODUS_3D_APPARATUS_RUN.md) | Three-dimensional electrode, explicit-lead, terminal-capacitance, and leakage-path run. |
| [`docs/EXODUS_RELATIONAL_TOMOGRAPHY.md`](docs/EXODUS_RELATIONAL_TOMOGRAPHY.md) | DET-native endpoint inference, rotation, nested closure, and matched-state history audit. |
| [`docs/EXODUS_ADAPTIVE_SCHEDULER.md`](docs/EXODUS_ADAPTIVE_SCHEDULER.md) | Bayesian information-gain scheduling, control ablation, and novel-channel stopping gates. |
| [`docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md`](docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md) | General hierarchical RET, question-conditioned scheduling, calibration, costs, model inadequacy, and closure. |
| [`docs/NEUTRON_LIFETIME_RET.md`](docs/NEUTRON_LIFETIME_RET.md) | Published-aggregate neutron-lifetime inference and calibration-first next-action design. |
| [`docs/MATHEMATICAL_SEARCHES.md`](docs/MATHEMATICAL_SEARCHES.md) | Proof-governed Riemann zero-spacing and bounded Collatz adaptive searches. |
| [`docs/MATHEMATICAL_NEXT_RUNS.md`](docs/MATHEMATICAL_NEXT_RUNS.md) | Validated 512-zero Riemann extension and checkpointed Collatz frontier through 262,144. |
| [`docs/RELATIONAL_RESIDUAL_DISCOVERY.md`](docs/RELATIONAL_RESIDUAL_DISCOVERY.md) | Non-Gaussian evidence, RG2 governance, Riemann spectroscopy, the frozen multistep Collatz follow-up, and the consumed-only accelerated endpoint prequalification through \(2^{22}\). |
| [`docs/NAVIER_STOKES_NEAR_SINGULARITY.md`](docs/NAVIER_STOKES_NEAR_SINGULARITY.md) | Periodic 3-D Navier–Stokes calibration plus LPS, DET feature-graph, RET growth-score, phase-two transport, and phase-three long-horizon completion results. |

## Highlights

- **A relational ontology** — the record-kernel unification of existence, participation, and becoming (event graph ≺ → record → law map → commit kernel → participation aperture). The ontology is the point; the clock anomaly is an optional empirical probe.
- **751/752 tests passing** — `python3 run_tests.py`
- **10 active + 5 retired correspondence checks** — Born rule, CHSH, Lorentz covariance, pointer formation, amplitude structure (active); gravity/Kepler (retired, Option B)
- **1 pre-registered prediction** — κ-Π clock anomaly (testable with atomic clocks); gravity is standard GR (Option B)
- **6 major open problems addressed** (O1–O4 as CI/AT correspondence checks, O7/O8 — full uniqueness theorems remain open; see MODEL_CARD §6)
- **128 model modules / 144 Python files** — core framework, applied physics, RET, governed mathematical searches, and bounded numerical studies
- **DET 8 is a clean starting point** — no dependency on prior DET versions

## Two Tracks

**Track A (Physical Calculus):** Must be falsifiable. It currently has one pre-registered prediction, the κ-Π clock anomaly, gated on F9 and an independent κ measurement. The former κ-gravity program is retired; gravity is standard GR.

**Track B (Ontological Grammar):** Must be coherent, non-smuggling, and empirically compatible. It offers a governed synthesis for four deadlocks—time, quantum interpretation, agency, and history—while keeping its metaphysical claims distinct from physical evidence.

## Architecture

DET's physical core uses a **record-kernel calculus**: the event graph (G = (V, ≺)) defines causal structure, node records store committed facts, the law map generates possibility objects, and commit kernels produce outcomes. The implemented quantum and Lorentz modules are correspondence checks; they do not yet constitute uniqueness derivations from DET primitives.

## Running

```bash
python3 run_tests.py   # 751/752 passing
python3 -m det8.models.exodus_simulation  # governed research sandbox
python3 -m det8.models.exodus_next_runs   # phase-2 discriminators
python3 -m det8.models.exodus_field_solver  # 2-D Maxwell-stress run
python3 -m det8.models.exodus_floating_supply  # floating-source charge run
python3 -m det8.models.exodus_apparatus_3d  # 3-D apparatus and lead run
python3 -m det8.models.exodus_relational_tomography  # endpoint tomography
python3 -m det8.models.exodus_adaptive_scheduler  # adaptive interventions
python3 -m det8.models.relational_experimental_calculus  # general RET/REC suite
python3 -m det8.models.examples.neutron_lifetime  # neutron discrepancy adapter
python3 -m det8.models.mathematical_searches  # bounded Riemann/Collatz searches
python3 -m det8.models.mathematical_next_runs  # validated higher/frontier runs
python3 -m det8.models.relational_residual_discovery  # RG2-governed discovery runs
python3 -m det8.models.examples.collatz_multistep_replication  # ten-step transport run
python3 -m det8.models.examples.navier_stokes_near_singularity  # NumPy phase-1 calibration
python3 -m det8.models.examples.navier_stokes_relational_discovery  # NumPy DET/RET phase-2 scouts
python3 -m det8.models.examples.navier_stokes_long_horizon_completion  # NumPy phase-3 conditional completion
```

The accelerated endpoint-matched successor is implemented in
[`det8/models/examples/collatz_accelerated_endpoint.py`](det8/models/examples/collatz_accelerated_endpoint.py).
Its consumed-only rolling tests did not prequalify the fixed valuation
candidate, so no manifest was persisted and no start above \(2^{22}\) was
accessed. The two planned higher bands remain preserved; there is intentionally
no future-run command in this quick-start list.

The default Navier–Stokes suite may still return `NUMERICAL_MODEL_REVISION`,
but its checked adaptive branch now uses one seed-defined,
resolution-invariant Fourier initial condition. The \(N=40/48\) actions are
admitted resolved transients, their spatial transport passes, and the \(N=40\)
timestep-halving audit passes. The branch state is
`RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING`; all grids through
\(N=48\) remain calibration only, with no proof, RG2 evaluation, or
replication claim. See
[`docs/NAVIER_STOKES_NEAR_SINGULARITY.md`](docs/NAVIER_STOKES_NEAR_SINGULARITY.md).

The phase-two discovery layer lowers viscosity and extends the horizon in
separate scouts, records LPS norms and intense-vorticity relations, and freezes
a dependent 70/30 growth-model score. Phase three reproduces the exact
long-horizon (N=48) anchor, transports it spatially to an admitted (N=56)
run, and conditionally completes a 2:1 timestep-cap check at (N=48). All
transport and timestep gates pass, all (L^9) velocity norms decrease from
their initial value, and the frozen growth comparison continues to prefer a
saturating exponential over the open alternatives. This is an (N=56)
spatial result with temporal stability checked at (N=48), not a complete
spatiotemporal convergence rectangle. The development ledger carries no
posterior, RG2, independent-replication, singularity, regularity, or proof
claim.

## Status

The framework, RET tooling, and bounded research adapters are implemented and internally tested. Empirical validation, independent replication, and the open analytic/continuum theorem programs remain future work.
