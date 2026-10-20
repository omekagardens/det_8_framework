# DET v8.0 — Deep Existence Theory

DET is a research framework for records, causal order and possible physical
laws. This repository contains software models, conditional
mathematics, finite simulations and experimental-analysis tools. Their evidence
and success criteria are distinct: a passing software check or a conventional
data replay does not establish the physical theory.

**Published research snapshot: 20 October 2026.** The current native result is a
[consolidated conditional theorem package](docs/track_b/native_theorem_package_v1/THEOREM_PACKAGE.md),
with the initial [law-dependence result](docs/track_b/native_theorem_package_v1/LAW_DEPENDENCE.md)
and a [fixed/moving seed family theorem](docs/track_b/native_theorem_package_v1/LAW_FAMILY_SUPPLEMENT.md).
Start there for the mathematical statements and their dependencies. Later local
work is not part of this published snapshot merely because it appears in a
coordination discussion.

## What is established

| Area | Published result | Boundary |
| --- | --- | --- |
| Native record-marked growth | An explicit positive extension through one additional birth layer at sufficiently small amplitude, under the admitted law and harmonic-support premises. | No uniform all-size harmonic continuation or physical spacetime map. |
| Fixed-law kernel and exclusions | Complete signed-kernel classification on the stated 30-, 33- and 38-class supports; the prescribed positive affine endpoint at amplitude `1/4` fails on each. The kernel has dimension one or two depending on an unresolved canonical-coefficient equality. | These are fixed-law, fixed-support results. They do not exclude arbitrary supports, seeds or amplitudes. |
| Law dependence | The old normalized seed fails under a declared law change. An explicit moving seed is unique across the stated family except at most one parameter, with an exact compatibility alternative there. | The exceptional branch remains symbolic; later h8 and fixed 30/33/38 results do not transfer. |
| Observation identifiability | Under the admitted finite law, a shared external readout can rescale or erase contrast while preserving native outcome and payload marginals. | Conditional non-feedback extensions demonstrate missing physical channel premises; no apparatus, universal no-go or empirical result is claimed. |
| Software and finite studies | Research models, explicit witness suites and conventional data-analysis artifacts with stated contracts. | Check results are specific to their sources, inputs and environments; there is no blanket whole-tree or physical-validation claim. |
| Measurement | Five prospective synthetic fixtures passed independent residual arithmetic checking. | Observed GWOSC replay has not run: H1 acquisition stopped on a missing approved header before body consumption. A narrow new-attempt decision is pending; historical custody failures remain failures. |
| Application diagnostic | A fixed one-birth width statistic has declared baselines, costs and conditional finite-sample error bounds. | ABSTAIN / NOT RUN: a certified numerical effect bound and validated sampler are missing. No measured advantage or physical channel is claimed. |

The theorem package prints the natural coordinates, complete reduced systems,
recovery formulas and inherited coefficient assumptions. The historical
coordinate dictionary, reproduction of the admitted finite certificates and the
actual canonical branch remain open. Its arbitrary complex positive-semidefinite
payload is scalar-passive; retaining it does not derive informative quantum
dynamics.

The native physical forward map—from DET's records and growth law to a selected
observable—has not been established. The metric-as-record proposal remains
Status M. **Unchanged general relativity remains the gravitational baseline
(Option B); the retired gravity modification is not restored by these results.**
The separate RET research lane remains paused.

## Where to start

| Document | Use |
| --- | --- |
| [Theorem package](docs/track_b/native_theorem_package_v1/THEOREM_PACKAGE.md) | Exact admitted law, support, positive theorem, kernel, exclusions and unresolved premises. |
| [Law dependence](docs/track_b/native_theorem_package_v1/LAW_DEPENDENCE.md) | Structural identities, coordinate changes, optional prescriptions and the explicit alternative prefix. |
| [Law-family supplement](docs/track_b/native_theorem_package_v1/LAW_FAMILY_SUPPLEMENT.md) | Fixed-seed obstruction, explicit replacement seed and exceptional compatibility. |
| [Width diagnostic](docs/track_b/native_theorem_package_v1/WIDTH_DIAGNOSTIC.md) | Simulation channel, held-out rule, error bounds, costs and actual blockers. |
| [Observation identifiability](docs/track_b/native_theorem_package_v1/OBSERVATION_IDENTIFIABILITY.md) | Exact readout counterexamples, retained custody failure and the missing operational channel contract. |
| [Publication scope](docs/track_b/native_theorem_package_v1/PUBLICATION_NOTE.md) | Independent reviews, synthetic evidence, acquisition failure and withheld provenance. |
| [Next steps](NEXT_STEPS.md) | Bounded deliverables, acceptance criteria and current pauses. |
| [Implementation plan](REVIEW_IMPLEMENTATION_PLAN.md) | Current summary first, followed by the preserved chronological implementation record. |
| [Original independent review](<indep ndent_review.md>) | The September 2026 assessment that motivated the implementation programme; preserved with its original scope and evidence limits. |
| [Model card](MODEL_CARD.md) | Framework primitives, supported claims and historical model inventory. |
| [Governance](GOVERNANCE.md) and [falsification ledger](FALSIFICATION_LEDGER.md) | Claim boundaries, decision gates, active and retired falsifiers. |
| [Branch workflow](docs/BRANCH_WORKFLOW.md) | Reviewed integration from `ret` to `main`, maintenance checks and publication boundaries. |

The implementation plan and coordination records are additive histories. Earlier
status statements remain useful provenance; the current summary and the scoped
result document govern the claim being read. Integration into `main` does not
upgrade an experiment, conditional theorem or historical execution record.

## Programme and architecture

The record-kernel calculus separates causal structure, committed records, the
law that generates possibilities and the kernel that assigns outcomes. The
[core model implementation](det8/models/det8_core.py) is one software entry
point. Importable research modules are not automatically supported APIs.

**Track A** concerns falsifiable physical claims. The documented κ-Π clock
proposal remains gated on F9 and an independent κ measurement; its presence in
the model inventory is not experimental validation. See [PHYSICS.md](PHYSICS.md)
and the [falsification ledger](FALSIFICATION_LEDGER.md).

**Track B** develops the ontological and mathematical programme. Its conditional
reconstruction and growth results must keep additional assumptions visible.
See [ONTOLOGY.md](ONTOLOGY.md), [record-kernel physics](docs/record_kernel_physics.md),
[QR-MAP](docs/track_b/QR_MAP.md) and [gravity](docs/track_b/gravity.md).

Current priorities are independently complete theorem and law-dependence
deliverables, one prospective conventional GWOSC replay, and separately scoped
physical-prediction and application-benchmark projects. An application benchmark
must declare baselines, costs, failure rates and held-out evaluation; success
does not establish DET physics. [NEXT_STEPS.md](NEXT_STEPS.md) gives the roadmap.

## Running and checking

Run commands from the repository root. Consult the selected component's
documentation for dependencies and its execution contract. The standalone
research-check registry supports Python 3.11 or later and uses the standard
library; this does not imply that every research adapter has the same
requirements.

For ordinary repository integration, use the scoped checks in the
[branch workflow](docs/BRANCH_WORKFLOW.md). Research execution is a separate
choice and must respect the current pauses, protected inputs and run approvals.
No new scientific execution or whole-repository pass count is asserted by this
documentation update; the branch workflow records the scoped maintenance run.

The explicit research registry can list and validate its fixed manifest without
executing a witness suite:

```sh
.venv/bin/python -B scripts/run_research_checks.py --list
.venv/bin/python -B scripts/run_research_checks.py --check
```

Create/select an appropriate Python environment before using those paths. See
[Research checks](docs/RESEARCH_CHECKS.md) for selected-suite execution, source
identity checks and the meaning of a successful finite witness. Its registry
does not discover or execute every research directory.

The historical broad runner is still available:

```sh
python3 run_tests.py
```

It runs research and numerical work, including RET-related studies. It is **not
a routine merge gate** and should not be run while that research is paused.
Individual study entry points and their prerequisites are documented below;
listing them here does not authorize another experiment or consume a holdout.

## Earlier studies and tools

| Area | Documentation |
| --- | --- |
| Experimental inference | [Relational Experimental Calculus](docs/RELATIONAL_EXPERIMENTAL_CALCULUS.md), [Novelty Ledger](NOVELTY_LEDGER.md) |
| Exodus apparatus and endpoint models | [Equation audit](docs/EXODUS_DET_TRANSLATION.md), [next runs](docs/EXODUS_NEXT_RUNS.md), [2-D field model](docs/EXODUS_FIELD_RUN.md), [floating supply](docs/EXODUS_FLOATING_SUPPLY_RUN.md), [3-D apparatus](docs/EXODUS_3D_APPARATUS_RUN.md), [tomography](docs/EXODUS_RELATIONAL_TOMOGRAPHY.md), [scheduler](docs/EXODUS_ADAPTIVE_SCHEDULER.md) |
| Neutron lifetime | [Published-aggregate analysis and calibration prerequisites](docs/NEUTRON_LIFETIME_RET.md) |
| Riemann and Collatz | [Bounded searches](docs/MATHEMATICAL_SEARCHES.md), [next-run protocols](docs/MATHEMATICAL_NEXT_RUNS.md), [residual discovery and preserved higher-band gates](docs/RELATIONAL_RESIDUAL_DISCOVERY.md) |
| Navier–Stokes | [Numerical protocol, finite results and convergence limits](docs/NAVIER_STOKES_NEAR_SINGULARITY.md) |
| Conventional GWOSC processing | [Input qualification](docs/experiments/gwosc_input_qualification_v1/), [nominal processing](docs/experiments/gwosc_nominal_processing_v1/), [nominal result](docs/experiments/gwosc_nominal_result_v1/) |
| Historical phases | [Roadmap](ROADMAP.md) |

These studies retain their original evidence and restrictions. Bounded Collatz
checks are not a universal proof; the locked higher bands remain protected.
Navier–Stokes results remain numerical evidence with their stated spatial and
temporal limits, not singularity or regularity proofs. Existing RET tools remain
available as source while new RET research is paused.
