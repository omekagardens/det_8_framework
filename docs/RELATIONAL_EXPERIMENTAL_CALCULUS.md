# Relational Experimental Calculus

**Status:** General synthetic methodology core with Exodus and thermal-drift
fixtures. It is not yet a live-data controller.

**Implementation:**

- `det8/models/relational_tomography.py`
- `det8/models/relational_scheduler.py`
- `det8/models/relational_closure.py`
- `det8/models/relational_experimental_calculus.py`
- `det8/models/relational_evidence.py`
- `det8/models/relational_discovery_governance.py`
- `det8/models/relational_residual_discovery.py`
- `det8/models/examples/exodus_tomography.py`
- `det8/models/examples/neutron_lifetime.py`
- `det8/models/examples/thermal_drift_tomography.py`
- `det8/models/examples/riemann_multiscale_discovery.py`
- `det8/models/examples/collatz_valuation_discovery.py`
- `det8/models/examples/collatz_accelerated_endpoint.py`
- `det8/models/examples/navier_stokes_near_singularity.py`
- `det8/models/examples/drift_change_point.py`

Run the full demonstration with:

```bash
python3 -m det8.models.relational_experimental_calculus
python3 -m det8.models.relational_residual_discovery
python3 run_tests.py
```

## 1. What was generalized

The adaptive scheduler is no longer extended as an Exodus-specific optimizer.
Exodus is now one experiment adapter for a general sequential experimental-
design engine:

\[
D_n \longrightarrow p(M,\theta,\psi\mid D_n)
\longrightarrow x^*_{n+1}\longrightarrow D_{n+1},
\]

where (M) is a declared model, \(\theta\) contains effect parameters,
\(\psi\) contains nuisance parameters, and (x) may be either a science or a
calibration action.

The implementation separates:

1. relational-family identification;
2. optional-endpoint existence;
3. endpoint-parameter characterization;
4. conserved-transfer closure.

## 2. RG1: identification before extension

\[
\boxed{\text{RG1: Relational identification precedes ontological extension.}}
\]

Stage A establishes predictive support for a broad relational family:

\[
p(\mathcal F\mid D)>\theta_F.
\]

Stage B tests whether an optional endpoint is required:

\[
p(z_j=1\mid D)>\theta_N,
\qquad \theta_N\geq\theta_F.
\]

Stage C characterizes its continuous parameters:

\[
p(a_j,\theta_j\mid z_j=1,D).
\]

The code rejects a novelty threshold below the family threshold. This makes
the stronger novelty standard an executable governance constraint.

## 3. Hierarchical amplitudes and spike-and-slab endpoints

The old Exodus hypotheses used fixed amplitudes. The general core instead
represents an optional endpoint through two declared models:

\[
a_j=0 \quad\text{(spike)},
\qquad
a_j\sim\mathcal N(\mu_j,\sigma_j^2) \quad\text{(slab)}.
\]

The endpoint-inclusion probability is the posterior weight summed over all
models containing \(a_j\). Within each slab model, the amplitude posterior is
updated exactly for linear responses or by Gaussian cubature for nonlinear
responses. This avoids an artificial
choice between, for example, exactly 0 and exactly 50 µN.

Model priors are unequal by default:

\[
p(M)\propto\exp[-\lambda C(M)],
\]

where \(C(M)\) is declared model complexity. Explicit priors may be supplied
instead.

## 4. Observation and uncertainty model

For action \(x\), the general declared observation model is

\[
Y_x=b_x+H_x\beta_M+h_x(\beta_M)+\epsilon_x,
\qquad
\epsilon_x\sim\mathcal N(0,R_x).
\]

The parameter vector \(\beta_M\) includes both effect and nuisance terms.
\(R_x\) may be a scalar standard deviation, which retains the old
\(\sigma_x^2I\) behavior, or a complete positive-definite covariance matrix.
Different actions may declare different noise models.

For a linear response, the predictive distribution remains exact:

\[
p(Y_x\mid M,D)=
\mathcal N\!\left(b_x+H_x\mu_M,
H_x\Sigma_MH_x^\mathsf T+R_x\right).
\]

For a nonlinear response, the core propagates \(2n\) spherical-radial
cubature points through \(h_x\). Their moments approximate the observation
mean, signal covariance, and parameter-observation cross covariance. The
posterior update is then

\[
K=C_{\beta Y}S_Y^{-1},\qquad
\mu^+=\mu+K(y-\bar y),\qquad
\Sigma^+=\Sigma-KS_YK^\mathsf T.
\]

This retains curvature that a plug-in prediction \(h(E[\beta])\) would miss,
while preserving the existing Gaussian posterior interface. Linear feature
terms and nonlinear increments may be composed in the same action.

Example:

```python
action = RelationalAction(
    "paired_response",
    "science",
    (0.0, 0.0),
    {"bias": (1.0, 1.0)},
    nonlinear_increment=lambda p: (p.get("rate", 0.0) ** 2,
                                    0.5 * p.get("rate", 0.0) ** 2),
)
covariance = ((0.04, 0.02), (0.02, 0.09))
posterior = update_ret_posterior(posterior, action, observation, covariance)
```

Thus both parameter uncertainty and correlated measurement geometry change
action ranking even when marginal sensor noise is small.

## 5. Question-conditioned, calibration-aware scheduling

A scientific question is a mapping (q(M)), not necessarily a request to
identify every model. Expected information gain targets the answers:

\[
I(q(M);Y_x\mid D).
\]

The scheduler also values nuisance reduction and subtracts practical burden:

\[
U(x)=I(q(M);Y_x\mid D)
+\lambda_\psi I(\psi;Y_x\mid D)
-\lambda_tT(x)-\lambda_mM(x)-\lambda_rR(x)-\lambda_wW(x).
\]

Actions declare their type as `science` or `calibration`. A science action can
still rank first during calibration if it simultaneously constrains nuisance
terms and answers the scientific question more efficiently. The governance
state describes what uncertainty must be resolved; it does not impose an
action label.

## 6. Open-model branch

Every posterior includes an explicit broad predictive model (M_\bot), named
`M_bottom` in code. It means only:

> The declared model set is inadequate for the observation.

It does not mean new physics. When its posterior exceeds the declared gate,
the state machine enters `MODEL_FAILURE` and requests model revision rather
than selecting the least-bad named endpoint.

## 7. State machine

The implemented states are:

```text
CALIBRATE
  → DISCOVER_FAMILY
  → TEST_EXTENSIONS
  → CHARACTERIZE
  → CLOSE
  → CLOSED

Branches: MODEL_FAILURE, INCONCLUSIVE
```

The transition order is evidence-based rather than automatic. Nuisance
uncertainty can keep the system in `CALIBRATE`; ambiguous family support keeps
it in `DISCOVER_FAMILY`; ambiguous spike-and-slab inclusion enters
`TEST_EXTENSIONS`; and imprecise supported amplitudes enter `CHARACTERIZE`.
Conservation closure is evaluated only after the inferential gates clear.

## 8. Current synthetic findings

### Exodus fixture

The initial posterior is calibration-gated because the cross-axis coefficient
has standard deviation 0.08. Under the joint scientific-plus-nuisance
objective, the top action is a science configuration that also contains high
cross-axis information. After it:

- the external-relational-family probability is 0.99990;
- the cross-axis standard deviation falls below the 0.05 gate;
- Earth and history inclusion remain unresolved;
- the state advances to `TEST_EXTENSIONS` rather than claiming novelty.

The extension run declares an Earth-correlated truth of 17 µN, which was not a
point hypothesis. After 12 adaptively selected actions:

\[
\hat a_E=16.62\pm1.86\ \mu\mathrm N
\quad(1\sigma),
\]

with an approximately 95% interval of 12.98–20.26 µN and endpoint inclusion
effectively 1.0. History inclusion remains low at approximately 0.11.

A deliberately incompatible 5 mN vector observation drives `M_bottom` to
1.0 and enters `MODEL_FAILURE`.

### Thermal-drift fixture

The unrelated two-axis thermal model demonstrates reuse:

- the first selected action is sensor calibration;
- asking about ambient coupling selects an airflow-on science action;
- asking about preparation history selects a different airflow-off action;
- `M_bottom` remains low after the calibration record.

This is the key generality check: one posterior and action set produce
different schedules for different scientific questions.

### Neutron-lifetime adapter

Three published aggregate records distinguish confinement method from decay
readout. Within the declared reduced model set, a proton-specific pipeline
relationship leads at approximately 0.80, while the correctly-signed
dark-decay endpoint (beam lengthened, bottle shortened) remains below 0.02.
The scheduler chooses an absolute proton flux/readout audit before another
lifetime measurement. See
[`NEUTRON_LIFETIME_RET.md`](NEUTRON_LIFETIME_RET.md) for the assumptions,
results, and interpretation boundary.

The adapter also verifies the new core with a three-record joint covariance
likelihood and a nonlinear paired survival-fraction response. A zero-
correlation joint update reproduces independent sequential assimilation to
floating-point precision. A companion
`det8/models/examples/neutron_counting_evidence.py` exercises the evidence
layer's Binomial and Poisson families on synthetic raw counts and reproduces
the same proton-pipeline direction.

### Navier–Stokes numerical adapter

The phase-1 periodic three-dimensional Navier–Stokes scout records bounded
floating-point trajectories as immutable numerical evidence and applies a
separate admission layer to scalar diagnostics: energy and enstrophy balance,
stepwise energy behavior, divergence, spectral-tail occupancy, vorticity
amplification, spectrum transport, and resolution/timestep refinement. Failed
admission produces `UNDERRESOLVED` or the suite-
level `NUMERICAL_MODEL_REVISION`; it is not evidence for singularity.

The default calibration suite still contains underresolved $N=16/24$
actions. A consumed adaptive branch using the same continuum low-mode field
at $N=16,24,32,40,48$ finds admitted, spatially and temporally transported
transient amplification at $N=40/48$, but no near-singular scaling. That
branch also has no frozen competing growth likelihood, locked holdout,
historically fresh replication, or calibrated open-model probability. It
therefore reports
`NOT_EVALUATED_NO_FROZEN_PREDICTIVE_RELATION`, not an RG2 state. Its finite
records cannot enter either RG2 exact branch and authorize neither blow-up nor
global-regularity language. See
[`NAVIER_STOKES_NEAR_SINGULARITY.md`](NAVIER_STOKES_NEAR_SINGULARITY.md).

## 9. Conservation closure

`relational_closure.py` represents a conserved transfer by equal and opposite
endpoint vectors. A closure ladder evaluates increasingly broad regime cuts.
An instrument-only cut exposes the uncaptured transfer; including both the
instrument and environment closes it. Failure of every declared cut is
reported as model failure rather than silently assigning an endpoint.

## 10. Interpretation boundary

The runtime emits this warning with every governance state:

> Posterior model probability is conditional predictive support within the
> declared model set; it is not an ontological existence probability.

For example, a posterior of 0.999 for an Earth-correlated response means that
the corresponding declared predictive structure fits the accumulated record.
It does not establish a novel Earth coupling or any Track-B ontology.

## 11. Non-Gaussian evidence and residual discovery

The companion `relational_evidence.py` layer now represents eight fixed
predictive families: Gaussian, Student-t, binomial, beta-binomial, Poisson,
negative-binomial, multinomial, and Dirichlet-multinomial. It preserves an
explicit robust `M_bottom`, immutable source provenance, prequential scores,
and question-conditioned action selection. This layer compares declared
predictive distributions; the original RET core remains the parameter-state
engine for Gaussian linear and cubature-propagated nonlinear observations.

RG2 adds a discovery boundary: a residual relation must replicate on disjoint
records, improve untouched prediction, pass diagnostics, and keep the open
model below threshold. Statistical support cannot authorize proof language.
The Riemann/Collatz pressure tests and their current findings are documented
in [`RELATIONAL_RESIDUAL_DISCOVERY.md`](RELATIONAL_RESIDUAL_DISCOVERY.md). The
frozen ten-shortcut Collatz follow-up extends exact arithmetic through
\(2^{22}\) and finds that the earlier residue-tree gain disappears against the
stronger consumed-data baseline; tiny positive higher-band transport scores do
not clear the historical, practical-gain, calibration, or open-model gates.
The consumed-only accelerated endpoint successor then matches four origin
valuation jumps against endpoint height, residue, and same-depth valuations,
jointly refitting the shared controls under H1. Its equal-block-weighted H1
gain is negative on all three rolling ranges through \(2^{22}\), so it
does not prequalify: no manifest was persisted, no higher start was accessed,
and the two planned future bands remain preserved. Its broad-tail sensitivity
is not a calibrated open model and supplies neither a probability nor an RG2 or
formal-replication claim.

## 12. Longitudinal evolution, change points, and mixture inference

The Gaussian core treats every record as generated by a fixed latent parameter.
Three additions in `relational_tomography.py` close that gap without replacing
the closed-form linear/cubature machinery.

**Longitudinal evolution.** A model may declare per-parameter process noise via
`RelationalModel.drift_standard_deviations`. `evolve_ret_posterior` advances
each model's Gaussian state by adding the declared process variance between
separately committed actions (a symmetric random walk: means are unchanged,
only predictive uncertainty grows). A zero-drift model is untouched. This is
the missing "longitudinal stochastic process across separately committed
actions": the scheduler automatically assigns a larger expected information
gain to re-measuring a stale state.

**Mixture parameter inference.** `MixtureParameterState` represents a
non-Gaussian parameter posterior as a weighted Gaussian mixture, so multimodal
or strongly skewed posteriors survive assimilation instead of collapsing into
a single Gaussian. `update_mixture_state` Kalman-updates each component
independently and reweights components by predictive likelihood, pruning
negligible components. `collapse_mixture` returns the moment-matched single
Gaussian for reporting or scheduling. A one-component mixture update agrees
exactly with the existing single-Gaussian core.

**Change-point detection.** `change_point_mixture` builds a two-component
stable-vs-drifted mixture (the spike-and-slab idiom reused from optional
endpoints), and `change_probability` reads the posterior weight of the drifted
component after an observation. A matched-generator fixture
(`det8/models/examples/drift_change_point.py`) tracks a rate that shifts from
0 to 3 midway through a sequence: the change posterior stays below ~0.04 on the
stationary prefix and jumps to ~1 at the first shifted record.

These are Gaussian-mixture and random-walk extensions. A full particle or
arbitrary nonconjugate parameter filter remains outside the core.

## 13. Limits and next pressure tests

This implementation is deliberately synthetic. Nonlinear parameter
propagation in the original RET core is still a Gaussian moment
approximation, though mixture states now preserve multimodality per
component. The evidence layer accepts non-Gaussian predictive families but
does not itself learn arbitrary nonconjugate parameter states. Correlation
across records is exact when records are supplied as one joint vector, and a
declared random-walk drift now carries a longitudinal process across
separately committed actions; an unobserved change point of unknown magnitude
is not inferred without a declared drift scale. Remaining pressure tests
include uncertain action execution, geometry fields, destructive apparatus
constraints, richer posterior-predictive diagnostics, and only then live-data
ingestion.
