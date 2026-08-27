# Navier–Stokes Near-Singularity Search: Phase 1 and DET/RET Phase 2

## Status

The implemented phase-1 adapter is
[`det8/models/examples/navier_stokes_near_singularity.py`](../det8/models/examples/navier_stokes_near_singularity.py).
The observational discovery layer is
[`det8/models/examples/navier_stokes_relational_discovery.py`](../det8/models/examples/navier_stokes_relational_discovery.py).
It performs small, governed numerical calibrations of the unforced
three-dimensional incompressible Navier–Stokes equations on the periodic cube.
The default seven-action suite may still return `NUMERICAL_MODEL_REVISION`
because it contains underresolved actions. The checked adaptive
random-low-mode branch instead ends in
`RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING`.

Both labels are governed numerical interpretations, not physical or
mathematical findings about singularity formation. All present \(N=16\)
through \(N=48\)
runs are calibration only. They are not discovery-grade direct numerical
simulations (DNS), independent replications, evidence of finite-time blow-up,
or evidence of global regularity.

The adapter fixes both of the following flags to false:

- `formal_singularity_claim`
- `proof_language_allowed`

It also reports
`rg2_state = NOT_EVALUATED_NO_FROZEN_PREDICTIVE_RELATION`.
Phase 2 retains the stronger state
`NOT_EVALUATED_NO_SOURCE_DISJOINT_REPLICATION`: its within-trajectory
development holdout is frozen, but it is temporally correlated and is not an
independent confirmation.

## Implemented equation and discretization

On \([0,2\pi)^3\), the adapter evolves the rotational form

\[
  \partial_t u = \mathcal P(u\times\omega)+\nu\Delta u,
  \qquad \omega=\nabla\times u,
  \qquad \nabla\cdot u=0,
\]

where \(\mathcal P\) is the Fourier-space Leray projection. There is no
forcing. The implementation uses:

- NumPy `complex128`/`float64` Fourier coefficients;
- a Fourier pseudo-spectral spatial discretization;
- strict component-wise retention of modes satisfying
  \(|k_i|<N/3\), the standard two-thirds truncation for the quadratic term;
- classical RK4 with an adaptive advective/diffusive timestep cap;
- projection and truncation after every right-hand-side evaluation and step;
- projection and two-thirds truncation of each initial field before its
  retained RMS is normalized to the requested `amplitude`.

This is a finite-dimensional, floating-point approximation. The adapter does
not implement interval arithmetic, an a posteriori PDE theorem, exact
three-halves padding, an independent solver, or an adaptive spatial mesh.

## Public API

The main immutable action is `SpectralRunConfig`. Its initial-condition names
are `abc`, `taylor_green`, `kida_pelz`, `vortex_tubes`, and
`random_low_mode`.

The principal entry points are:

- `prepare_navier_stokes_protocol(actions=None)`: returns the in-memory
  manifest and digests without evolving the PDE;
- `SpectralNavierStokes3D(config).run()`: runs one bounded trajectory;
- `run_development_suite(actions=None)`: runs the fixed phase-1 suite, builds
  the evidence ledger, compares matched resolution/timestep actions, and
  ranks follow-ups;
- `compact_suite_summary(suite)`: returns the CLI-sized summary;
- `classify_numerical_run(result)`: applies the single-run admission gates;
- `compare_resolution_pair(lower, higher)`: evaluates limited numerical
  transport between two otherwise matched actions;
- `compare_timestep_pair(coarser, finer)`: audits maximum-timestep refinement
  for the same spatial and physical action;
- `build_numerical_evidence_ledger(results)`: records immutable configuration
  and result provenance;
- `rank_followup_actions(results)`: applies a deterministic information/cost
  proxy. It is not a Bayesian posterior;
- `phase_one_resolution_ladder_actions()`: returns the consumed
  random-low-mode ladder at \(N=(16,24,32,40,48)\);
- `phase_one_timestep_actions()`: returns the consumed \(N=40\) pair with
  `maximum_dt` equal to 0.0075 and 0.00375;
- `PHASE_ONE_REFERENCE_FINDINGS`: stores the checked ladder, transport, and
  interpretation record without rerunning it.

The phase-two module adds:

- `prepare_discovery_protocol(actions=None)`: freezes actions, LPS
  diagnostics, feature-graph rules, growth families, and implementation
  provenance before a run;
- `run_relational_discovery(config)`: observes one numerical trajectory
  without changing its base result or run digest;
- `run_phase_two_discovery_suite(include_refinements=False)`: runs the two
  one-axis scouts and, when requested, their outcome-selected numerical
  checks;
- `phase_two_refinement_actions(results)`: gives the admitted branch a matched
  spatial and timestep check and gives a tail-underresolved branch only a
  higher-resolution recovery;
- `build_discovery_evidence_ledger(results)`: commits one RET record only for
  a complete physical-action bundle whose spatial and timestep checks pass;
- `compact_phase_two_summary(suite)`: returns the checked run-sized summary.

A single custom run can be constructed as follows:

```python
from det8.models.examples.navier_stokes_near_singularity import (
    SpectralNavierStokes3D,
    SpectralRunConfig,
)

config = SpectralRunConfig(
    initial_condition="taylor_green",
    resolution=24,
    viscosity=0.01,
    final_time=1.0,
)
result = SpectralNavierStokes3D(config).run()
```

The fixed suite is run with:

```bash
python3 -m det8.models.examples.navier_stokes_near_singularity
```

NumPy is a lazy optional dependency. If the selected Python environment does
not provide NumPy, the CLI returns a JSON `REFUSED` response rather than
running a substitute model. Use a NumPy-enabled Python environment, including
the configured Codex workspace Python where available.

## Fixed phase-1 actions

`development_actions()` returns seven actions fixed before the suite call:

| Family | \(N\) | \(\nu\) | Final time | Role |
|---|---:|---:|---:|---|
| ABC | 16 | 0.02 | 0.50 | calibration |
| Taylor–Green | 16 | 0.01 | 1.00 | development |
| Taylor–Green | 24 | 0.01 | 1.00 | development |
| Kida–Pelz | 16 | 0.01 | 0.75 | development |
| Kida–Pelz | 24 | 0.01 | 0.75 | development |
| periodic vortex tubes | 16 | 0.01 | 0.50 | development |
| seeded low modes | 16 | 0.01 | 0.75 | development |

The random low-mode action fixes `seed=20260826`. It now constructs an ordered,
seed-defined, divergence-free Fourier polynomial using modes with
\(1\le |k|^2\le9\). The coefficients are independent of grid resolution. Each
grid samples that same continuum polynomial; the code then projects, applies
the retained-mode mask, and normalizes the post-projection RMS. The checked
\(N=40\) and \(N=48\) initial spectra agree to machine precision.

The adapter's
`vortex_tubes` field is its own periodic Gaussian streamfunction construction;
it is not an exact reproduction of the Kerr or Hou–Li antiparallel-tube data.
Taylor–Green and Kida–Pelz are the two resolution pairs inside the default
seven-action suite. The consumed adaptive branch adds the five-grid
random-low-mode ladder documented below.

## Recorded diagnostics

For kinetic energy \(K\), enstrophy \(\Omega\), palinstrophy \(P\), rate of
vortex stretching \(\Sigma\), and strain tensor \(S\), the implementation uses

\[
  K=\frac12\langle |u|^2\rangle,
  \qquad
  \Omega=\frac12\langle |\omega|^2\rangle,
  \qquad
  P=\frac12\langle |\nabla\omega|^2\rangle,
\]

\[
  \Sigma=\langle\omega\cdot S\omega\rangle,
  \qquad
  \frac{dK}{dt}=-2\nu\Omega,
  \qquad
  \frac{d\Omega}{dt}=\Sigma-2\nu P.
\]

The run records the corresponding numerical balance defects, divergence,
helicity, \(\|u\|_3\), maximum velocity, strain magnitude, shell energy
spectrum, high-wavenumber energy fraction, and grid maximum vorticity. It also
evaluates maximum vorticity on a fixed two-times zero-padded grid.

The approximate BKM-style quantity is the sampled trapezoidal integral

\[
  I_{\omega}(t)=\int_0^t\|\omega(s)\|_\infty\,ds.
\]

"BKM-style" is deliberately qualified: the original Beale–Kato–Majda theorem
is a theorem for the three-dimensional Euler equations. A finite sampled
integral in this Navier–Stokes adapter is only a diagnostic.

For the spectral tail, the adapter fits

\[
  E(k,t)\approx C(t)k^{-p(t)}e^{-2\delta(t)k}
\]

and reports \(\delta\) as an analyticity-strip proxy. The fitted tail uses the
few shells available between roughly half of the retained axis cutoff and that
cutoff. Even at \(N=40\) and \(N=48\), this remains a calibration-scale proxy,
not a research-grade analyticity inference.

## Admission gates and state meanings

The default numerical gates require:

| Gate | Threshold |
|---|---:|
| relative kinetic-energy balance defect | \(\le 5\times10^{-3}\) |
| sampled enstrophy-balance defect | \(\le 5\times10^{-2}\) |
| relative unforced energy increase | \(\le 5\times10^{-3}\) |
| relative one-step energy increase | \(\le 5\times10^{-5}\) |
| positive one-step energy-balance residual | \(\le 5\times10^{-3}\) |
| divergence \(L^2\) norm | \(\le 10^{-10}\) |
| high-wavenumber energy fraction | \(\le 2\times10^{-3}\) |

A single-run scaling trigger would additionally require at least fourfold
maximum-vorticity amplification, twofold enstrophy amplification, an eligible
analyticity fit with \(\delta k_{\mathrm{cut}}\ge2\), two stable late-window
power-law fits with exponent at least one and \(R^2\ge0.98\), and a locked
growth-model holdout.

Phase 1 intentionally fixes
`LOCKED_GROWTH_MODEL_HOLDOUT_AVAILABLE = False`. Consequently, the full
single-run scaling gate cannot pass in the present adapter. The 30% and 40%
late-window fits are exploratory within-run diagnostics and have no fresh
holdout status.

The emitted interpretations are conservative:

- `UNDERRESOLVED`: at least one numerical-admission gate failed;
- `NO_NEAR_SINGULAR_SCALING`: the bounded admitted run did not clear the
  scaling gates;
- `RESOLVED_TRANSIENT_AMPLIFICATION`: admitted vorticity amplification of at
  least 1.20 did not clear the scaling gates;
- `SINGLE_RUN_SCALING_TRIGGER`: reserved for a run that clears all numerical
  and scaling gates; it is unreachable while the locked holdout is absent and
  would still not be a singularity claim.

`compare_resolution_pair()` checks joint admission; initial and final spectrum
transport; vorticity, enstrophy, and palinstrophy amplification transport; and
peak-time transport. `compare_timestep_pair()` checks the same three
amplifications, the final spectrum, admission, and peak time under timestep
refinement. Both outputs explicitly say that transport is numerical and does
not count as replication.

## Current phase-1 result

`PHASE_ONE_REFERENCE_FINDINGS` is the machine-readable record of the consumed
random-low-mode adaptive branch. Its checked digest is
`df280ae1e3f43569acba45b31c967197f964a1398d386d8ed9297dd7e13ada8a`.
The physical action fixes the resolution-invariant Fourier initial condition,
seed 20260826, \(\nu=0.01\), final time 0.75, amplitude 1.0,
`maximum_dt=0.00375`, and `sample_interval=0.05`.

| \(N\) | Run state | Vorticity amplification | Enstrophy amplification | Palinstrophy amplification | Peak high-\(k\) fraction | \(\delta k_{\mathrm{cut}}\) |
|---:|---|---:|---:|---:|---:|---:|
| 16 | `UNDERRESOLVED` | 1.382364 | 1.248320 | 2.588995 | \(8.76\times10^{-2}\) | 3.3621 |
| 24 | `UNDERRESOLVED` | 1.638031 | 1.274727 | 3.035263 | \(1.19\times10^{-2}\) | 2.4070 |
| 32 | `UNDERRESOLVED` | 1.763186 | 1.281836 | 3.275241 | \(2.19\times10^{-3}\) | 0.7197 |
| 40 | `RESOLVED_TRANSIENT_AMPLIFICATION` | 1.7481109697 | 1.282847 | 3.344409 | \(2.52\times10^{-4}\) | 1.7790 |
| 48 | `RESOLVED_TRANSIENT_AMPLIFICATION` | 1.7333735273 | 1.282988 | 3.360812 | \(1.31\times10^{-4}\) | 1.8815 |

The \(N=16,24,32\) actions fail numerical admission. The \(N=40\) and
\(N=48\) actions are admitted as resolved transients, and their spatial
transport comparison passes every configured gate:

| Transport observable, \(40\rightarrow48\) | Relative gap |
|---|---:|
| initial spectrum | \(9.26\times10^{-16}\) |
| maximum-vorticity amplification | 0.8502% |
| enstrophy amplification | 0.01096% |
| palinstrophy amplification | 0.4881% |
| final spectrum | 0.003748% |
| maximum-vorticity peak time | 0 absolute gap |

The \(N=40\) maximum-timestep comparison also passes. Halving
`maximum_dt` from 0.0075 to 0.00375 gives relative gaps of
\(5.81\times10^{-10}\) in vorticity amplification,
\(8.93\times10^{-10}\) in enstrophy amplification,
\(1.72\times10^{-8}\) in palinstrophy amplification, and
\(4.98\times10^{-10}\) in the final spectrum.

These transients transport across the tested calibration-scale spatial and
timestep pairs, but they do not meet the near-singular scaling gates:

- maximum-vorticity amplification is about 1.75, below the required 4;
- enstrophy amplification is about 1.28, below the required 2;
- the admitted analyticity margins are 1.779 and 1.882, below the required 2;
- fitted-time instability is 25.4%, above the allowed 10%;
- no locked growth-model holdout exists.

The adaptive branch state is therefore
`RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING`. The separate
default seven-action suite may still report `NUMERICAL_MODEL_REVISION` because
that aggregate includes underresolved actions. Neither state is a continuum
regularity result.

## Phase-two prospective question

Phase two asks whether the transported phase-one transient strengthens along
two separate axes, while adding diagnostics derived from the
Ladyzhenskaya–Prodi–Serrin (LPS) conditions. The two scouts were fixed before
either was evolved:

| Scout | N | viscosity | final time | `maximum_dt` | sample interval |
|---|---:|---:|---:|---:|---:|
| lower viscosity | 40 | 0.007 | 0.75 | 0.00375 | 0.025 |
| longer horizon | 40 | 0.010 | 1.25 | 0.00375 | 0.025 |

Both use the same resolution-invariant random-low-mode polynomial and seed
20260826. Viscosity and horizon were not changed in the same scout. The
observer receives a copied read-only Fourier state and a deep copy of the
stored diagnostic record; a regression test verifies that attaching it does
not change the base trajectory digest.

## Latest 2026 LPS reference and scale bridge

Ramírez and Protas study q = (3, 4, 5, 9) on the unit torus with viscosity 1.
For q = 9, p = 3, their published constraint levels are
B = (500, 800, 1200), and the displayed B = 800 example uses
T = 2 × 10⁻⁴. Their normal production resolution is 256³. The paper states
that its data are available upon request; no public Fourier coefficient file
or repository was found as of 2026-08-26. No optimized field was imported
here, and these runs do not reproduce the paper's optimization.

For scalar comparison only, the exact PDE change of units from the paper's
unit torus to this code's [0, 2π)³ torus is:

```text
u_code = viscosity_code / (2π viscosity_paper) × u_paper
t_code = (2π)² viscosity_paper / viscosity_code × t_paper
```

It gives the following derived scale-equivalent values for the normalized-mean
L9 norm used by the code:

| code viscosity | mapped B=500 | mapped B=800 | mapped B=1200 | mapped example T |
|---:|---:|---:|---:|---:|
| 0.007 | 0.5570 | 0.8913 | 1.3369 | 1.1280 |
| 0.010 | 0.7958 | 1.2732 | 1.9099 | 0.7896 |

This bridge makes scalar magnitudes and time windows commensurable. The
random-low-mode actions were not initialized by matching a published B, and
matching a scalar value would not reproduce a field, optimization branch, or
trajectory.

## DET/RET discovery diagnostics

The LPS layer stores both the standard integral norm and the normalized-mean
norm. It computes the sampled supremum L3 and the time-average objectives
Phi(q) = (1/T) integral ||u||q^p dt for (q,p) = (4,8), (5,5), and (9,3),
using actual sample times and trapezoidal integration. It also records the
paper's terminal-L3 optimization proxy, enstrophy rebound, and descriptive
phase-plane log–log slopes. These slopes are comparisons, not proof tests.

The DET spatial layer selects exactly the top 1% and 0.1% of grid cells by
vorticity magnitude with a deterministic index tie-break. It records
enstrophy and velocity-L3 concentration, signed and normalized stretching,
strain-eigendirection alignment, neighboring vorticity-direction coherence,
and all periodic six-neighbor components. Adjacent-sample component bonds use
overlap, one-cell-dilated overlap, periodic displacement, and size. They are
feature continuations—not material-vortex identities, reconnections, or
physical causal edges. A separate DET event graph stores only chronological
committed diagnostic events.

The RET development scorer fits the first 70% of a trajectory and scores the
fixed final 30% under exponential, saturating-exponential,
double-exponential, finite-time-power, and robust open `M_bottom` models. It
uses Student-t point scores, but their sum is explicitly a composite score
because samples from one trajectory are correlated. It produces no posterior
model probabilities and counts as no independent replication.

## Checked phase-two runs

The complete machine-readable record is
[`det8/data/navier_stokes_phase_two_findings_2026-08-26.json`](../det8/data/navier_stokes_phase_two_findings_2026-08-26.json).
Its checked findings digest is
`a233a6bae2df47212aacb62290304c1cc01981e83b9ff8b427170ccd81f2f095`.

| Role | N | viscosity | T | vorticity amp. | enstrophy amp. | palinstrophy amp. | peak high-k | final/initial L9 | held-out model | State |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| viscosity scout | 40 | .007 | .75 | 1.82489 | 1.35573 | 3.75080 | 3.40e-4 | .94441 | exponential | admitted transient |
| spatial check | 48 | .007 | .75 | 1.80395 | 1.35599 | 3.77862 | 1.83e-4 | .94441 | exponential | admitted transient |
| timestep check | 40 | .007 | .75 | 1.82489 | 1.35573 | 3.75080 | 3.40e-4 | .94441 | exponential | admitted transient |
| horizon scout | 40 | .010 | 1.25 | 2.54650 | 1.56933 | 8.03839 | 2.31e-3 | .87756 | saturating | underresolved |
| spatial recovery | 48 | .010 | 1.25 | 2.58581 | 1.57007 | 8.25573 | 1.38e-3 | .87748 | saturating | admitted transient |

The low-viscosity N=40→48 pair, matched at `maximum_dt=0.00375`, passes
every configured spatial gate:

| Observable | Relative gap |
|---|---:|
| maximum-vorticity amplification | 1.1609% |
| enstrophy amplification | 0.01916% |
| palinstrophy amplification | 0.7363% |
| initial spectrum | 9.26e-16 |
| final spectrum | 0.005463% |
| peak time | 0 absolute gap |

Its N=40 timestep halving from 0.00375 to 0.001875 also passes; all four
relative diagnostic gaps are below 1.6e-9. The lower viscosity therefore
raises the transported N=48 phase-one vorticity amplification by about 4.1%,
but still yields only a bounded transient.

The long-horizon N=40 action crosses the spectral-tail admission threshold
2.0e-3. Its N=48 recovery is admitted, and all non-admission spatial gaps are
small, but the pair cannot pass the governed transport rule because both
members must be admitted. It also has no timestep-halving run. That branch
remains provisional.

Across all five runs, the normalized-mean L9 norm is maximal at the initial
sample. It falls by about 5.56% on the low-viscosity branch and 12.25% on the
long-horizon N=48 branch, so no positive L9 phase-plane growth slope exists.
The vorticity and palinstrophy amplification therefore reflects development
of gradients and smaller scales, not growth of the LPS L9 velocity norm. On
the held-out segment, the low-viscosity branch favors exponential vorticity
growth, while the longer branch favors saturation; both beat the broad open
model on this dependent development score. Neither is a finite-time
singularity result.

Component birth/death counts are qualitatively similar across each grid pair,
but candidate merge/split counts change substantially with resolution. That
is useful evidence that threshold topology is grid-sensitive, and it blocks
any reconnection interpretation of the feature graph.

## Phase-two RET record and consumed handoff

Exactly one RET record is committed:
`ns-det-ret-d4c7f5d8a416e15c`. It is one joint development bundle containing
the three low-viscosity source trajectories. Its observation is the N=48 log
peak-vorticity amplification 0.5899769, with a numerical log-scale uncertainty
0.0115425. Resolution and timestep variants are stability checks inside that
record; they are not three replications.

The suite state is
`TRANSPORTED_DEVELOPMENT_RELATION_REQUIRES_INDEPENDENT_REPLICATION`, and its
digest is
`cfbd68d3488afc7c41ab743a078325ef1e89138d3c59d0ab4f03937dbaecced0`.
It is not a near-singular candidate label.

That handoff selected the long-horizon N=56 extension followed conditionally
by the N=48 timestep halving. Both actions are now consumed below.

## Phase-three long-horizon completion

The governed runner is
[`det8/models/examples/navier_stokes_long_horizon_completion.py`](../det8/models/examples/navier_stokes_long_horizon_completion.py).
It froze the exact phase-two N=48 anchor, the N=56 extension, and the
conditional fine N=48 action before executing any of them. The conditional
action was authorized only by exact anchor reproduction and a complete pass
of the standard numerical and 48→56 spatial-transport gates. DET topology,
LPS shape, and growth scores were excluded from that predicate.

The anchor reproduced its numerical run digest
`b717450dddc08b4971f69ae9e9ec8411798d1877fb8577b803ee7f209b98af0d`
exactly. The three completed actions are:

| Role | N | `maximum_dt` | Steps | Vorticity amp. | Enstrophy amp. | Palinstrophy amp. | peak high-k | final/initial L9 | Model |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| reproduced anchor | 48 | .00375 | 350 | 2.58581 | 1.57007 | 8.25573 | 1.384e-3 | .87748 | saturating |
| spatial extension | 56 | .00375 | 350 | 2.55088 | 1.57030 | 8.41698 | 3.444e-4 | .87745 | saturating |
| timestep check | 48 | .001875 | 700 | 2.58581 | 1.57007 | 8.25573 | 1.384e-3 | .87748 | saturating |

Every N=48→56 spatial gate passes:

| Observable | Relative gap |
|---|---:|
| maximum-vorticity amplification | 1.3695% |
| enstrophy amplification | 0.01445% |
| palinstrophy amplification | 1.9157% |
| initial spectrum | 2.16e-17 |
| final spectrum | 0.02264% |
| peak time | 0 absolute gap |

The exact 2:1 N=48 timestep intervention doubled the actual RK4 step count
from 350 to 700. Its vorticity, enstrophy, palinstrophy, and final-spectrum
gaps are all below 2.5e-9, and its peak-time gap is zero. Thus the timestep cap
was genuinely exercised rather than remaining inactive.

The N=56 spectral tail is 3.44e-4, about four times smaller than at N=48. Its
L9 norm nevertheless falls to 87.745% of its initial value, its LPS q=9
time-average is stable across the grid pair, and the held-out vorticity model
remains saturating exponential, including against the open model. This
strengthens the interpretation of a resolved transient with small-scale
gradient amplification and depletion, not LPS norm growth or near-singular
scaling.

DET candidate event counts still change with resolution—for example, merge
and split candidates rise from 39/34 at N=48 to 65/62 at N=56. They remain
grid-dependent segmentation diagnostics and are not transported reconnection
observables.

The completed long-horizon RET record is
`ns-det-ret-long-horizon-750e3ed7791e`. It contains four unique source run
digests: the consumed underresolved N=40 scout, the reproduced N=48 anchor,
the N=56 extension, and the N=48 fine run. Its selected N=56 log-amplification
observation is 0.9364384 with numerical log-scale uncertainty 0.0136017.

The phase-three state is
`TRANSPORTED_LONG_HORIZON_DEVELOPMENT_BUNDLE_REQUIRES_INDEPENDENT_REPLICATION`.
The suite digest is
`24f562e9dbb2c3d9f26e42107c64a94474045a7250d8a5bafb81075be5c80129`.
The checked machine record is
[`det8/data/navier_stokes_long_horizon_completion_2026-08-26.json`](../det8/data/navier_stokes_long_horizon_completion_2026-08-26.json),
with findings digest
`0e2dd962900c15a44f3006aed9ee4e3a060e83252c3795599701a008dcd74faa`.

This completion has N=56 spatial transport and temporal stability checked at
N=48. It does not establish timestep convergence at N=56, so the full
spatiotemporal convergence rectangle remains incomplete. The most disciplined
next numerical action is the N=56 run at `maximum_dt=0.001875`. Only after
that passes should the search choose between a source-disjoint initial field,
an independent solver/dealiasing audit, or a new physical stress axis.

## Proof and discovery boundary

The periodic, positive-viscosity, unforced equation is within the official
Navier–Stokes existence-and-smoothness problem. The finite computations here
do not resolve that problem:

1. Every retained Fourier system is a finite-dimensional numerical model;
   apparent smoothness or growth of that model does not decide the continuum
   PDE.
2. Floating-point trajectories and fitted power laws cannot establish an
   infinite norm or convergence of a continuation integral.
3. An analyticity width approaching the grid scale is loss of numerical
   resolution, not evidence that the continuum width vanishes.
4. The present grids, \(16^3\) through \(56^3\), are calibration only.
   Published near-singularity studies use orders of magnitude more modes and
   still make cautious, non-proof claims.
5. Two development branches have transported resolution/timestep checks,
   but neither has a complete highest-grid timestep rectangle, an independent
   solver, alternate-dealiasing confirmation, or historically fresh
   source-disjoint replication.
6. The evidence ledger marks the trajectories as bounded floating-point PDE
   computations and `historically_unique_evidence = False`.
7. `rg2_evaluation_authorized`, `finite_time_singularity_claim_authorized`,
   and `global_regularity_claim_authorized` are all false in the protocol.

A future credible numerical candidate would require much higher resolved
grids, stability under resolution and timestep refinement, a locked competing
growth-model holdout, independent solver transport, resolved spectral tails,
and predeclared initial-condition coefficients. Even that would remain
numerical evidence rather than proof.

## Primary references

- E. Ramírez and B. Protas, [*The Ladyzhenskaya-Prodi-Serrin Conditions and
  the Search for Extreme Behavior in 3D Navier-Stokes
  Flows*](https://arxiv.org/abs/2604.13338), arXiv:2604.13338v1 (2026).
- Charles L. Fefferman, [*Existence and Smoothness of the Navier–Stokes
  Equation*](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf),
  official Clay Mathematics Institute problem description.
- J. T. Beale, T. Kato, and A. Majda, [*Remarks on the Breakdown of Smooth
  Solutions for the 3-D Euler Equations*](https://doi.org/10.1007/BF01212349),
  *Communications in Mathematical Physics* 94 (1984), 61–66.
- C. Sulem, P.-L. Sulem, and H. Frisch, [*Tracing Complex Singularities with
  Spectral Methods*](https://doi.org/10.1016/0021-9991(83)90045-1),
  *Journal of Computational Physics* 50 (1983), 138–161.
- C. Foias and R. Temam, [*Gevrey Class Regularity for the Solutions of the
  Navier–Stokes Equations*](https://doi.org/10.1016/0022-1236(89)90015-3),
  *Journal of Functional Analysis* 87 (1989), 359–369.
- G. S. Patterson and S. A. Orszag, [*Spectral Calculations of Isotropic
  Turbulence: Efficient Removal of Aliasing
  Interactions*](https://doi.org/10.1063/1.1693365), *Physics of Fluids* 14
  (1971), 2538–2541.
- M. E. Brachet et al., [*Small-Scale Structure of the Taylor–Green
  Vortex*](https://doi.org/10.1017/S0022112083001159), *Journal of Fluid
  Mechanics* 130 (1983), 411–452.
- S. Kida, [*Three-Dimensional Periodic Flows with
  High-Symmetry*](https://doi.org/10.1143/JPSJ.54.2132), *Journal of the
  Physical Society of Japan* 54 (1985), 2132–2136.
- P. Constantin and C. Fefferman, [*Direction of Vorticity and the Problem of
  Global Regularity for the Navier–Stokes
  Equations*](https://doi.org/10.1512/iumj.1993.42.42034), *Indiana University
  Mathematics Journal* 42 (1993), 775–789.
- T. Y. Hou and R. Li, [*Computing Nearly Singular Solutions Using
  Pseudo-Spectral Methods*](https://doi.org/10.1016/j.jcp.2007.04.014),
  *Journal of Computational Physics* 226 (2007), 379–397.
- D. Kang, D. Yun, and B. Protas, [*Maximum Amplification of Enstrophy in 3D
  Navier–Stokes Flows*](https://doi.org/10.1017/jfm.2020.204), *Journal of
  Fluid Mechanics* 893 (2020), A22.
- M. D. Bustamante and M. Brachet, [*Interplay Between the Beale–Kato–Majda
  Theorem and the Analyticity-Strip Method to Investigate Numerically the
  Incompressible Euler Singularity
  Problem*](https://doi.org/10.1103/PhysRevE.86.066302), *Physical Review E*
  86 (2012), 066302.
