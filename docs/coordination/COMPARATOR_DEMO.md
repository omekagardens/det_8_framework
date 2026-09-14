# Single-channel comparator: structural and Bayesian arithmetic

RI-12 bounded synthetic public-API fixture, 13 September 2026. The implementation
is [comparator_demo.py](../../det8/applied_physics/comparator_demo.py), alongside
the [exact identifiability contract](IDENTIFIABILITY_CONTRACT.md). This fixture
demonstrates declared computations. It is not apparatus calibration, a sampled
performance study, a policy comparison, a closure decision or G2 completion.
No RET implementation or protected calibration material is changed.

## Fixed declarations

The single observed response has mean `y = g x + b` in volts, with explicit
parameter order `(gain, offset)`. Reference levels are exact dyadic values
`x = -1, 0, +1`; their exact feature rows are `(x,1)`. SDK actions have one
response axis, known response zero and covariance `((1/4,),)`. The named
`gain_offset` model has independent proper priors `g ~ N(1,1)` and `b ~ N(0,1)`;
these arguments denote variances. The public `Parameter` constructor receives
standard deviations one. The offset is labeled a nuisance parameter.

The required SDK open alternative remains present, with prior probability
`0.02` and scale `8`. All parameter and prediction comparisons below are
**conditional on the named model**, not averages across that model and the
open alternative. The fixture does not turn a single declared model into
evidence of model-family selection. The declared time cost one is synthetic
metadata; it is neither a measured cost nor used for ranking.

This is a different observation contract from the existing RET apparatus
adapter, which has two axes at `x` and `x+0.25`. Both observed axes there can
already identify gain and offset in one action. Its design is not diagnosed
as rank deficient by this single-channel example.

## Public interface and retained records

```python
from det8.applied_physics.comparator_demo import run_comparator_demo

demo = run_comparator_demo()
first = demo.snapshots["first"]
assert not first.structural.identified
assert demo.snapshots["distinct"].structural.identified
```

The function takes no arguments and writes no output files. To suppress Python
interpreter bytecode caches as well, use `PYTHONDONTWRITEBYTECODE=1 python -B`.
It uses only public `det8.ret` data contracts and calls: `start`, `ingest`,
`summarize`, `predict`, `manifest_from_state` and `replay_manifest`.
No private posterior field or RET adapter is accessed. There is no Objective,
action ranking, workflow decision or closure evaluation in this fixture.

The result is a frozen `ComparatorDemo`, containing the public experiment,
`model_id`, exact `parameter_order`, target `(-1,1)`, immutable `reference_rows`,
known noise variance `Fraction(1,4)`, snapshots, raw bytes and verified replays.
The target is the mean response at the initially unobserved level `x=-1`.

Each frozen `ComparatorSnapshot` contains public `state` and `summary`, an
immutable tuple `training_rows`, the exact `structural` certificate, public
`predictions` and `mean_variances`, indexed by action ID `minus`, `zero`, `plus`.
`mean_variances` concerns the named model only. It is the public future-response
variance minus the explicitly known observation variance `1/4`. The public
summary exposes parameter means and marginal standard deviations; the demo
does not claim that it exposes full parameter covariance. The exact matrices
below are independent analytic test oracles, not extracted SDK internals.

Every `TrainingRowBinding` retains `record_id`, `record_digest`, `action_id`,
`axis_index`, `source_hashes`, exact `reference` and exact `coefficients`.
Rows are assembled from actually assimilated non-validation records and their
`observed_indices`, preserving record order. The exact declaration is checked
against the SDK action coefficients in the named parameter order. Proposed
candidate rows are never mistaken for observed information. The experiment
rejects missing observations; a single response cannot be entirely missing.

The snapshot schedule is:

| Snapshot | Records used for inference |
|---|---|
| `prior` | None |
| `first` | `training_plus`: `(x,y)=(1,3/2)` |
| `repeated` | Branch from `first`, adding `training_plus_repeat`: `(1,3/2)` |
| `distinct` | Separate branch from `first`, adding `training_minus`: `(-1,-1/2)` |
| `held_out` | Same inference as `distinct`; four terminal validation records retained separately |

The four validation records have levels `(-1,0,+1,0)` and fixed values
`(-1/2,1/2,3/2,1/2)`. They never enter the structural design or update parameter
or model probabilities. They do increase the retained record/work counts.
Each record has its own timestamp and raw capture bytes. The two computational
branches are a fixed arithmetic comparison, not evidence of experimental
counterfactual replay or of an adaptive policy's performance.

## Independent Gaussian oracle

For training design `H`, response vector `y`, prior mean `m0=(1,0)` and prior
covariance `I`, the named-model posterior is

`P = (I + 4 H^T H)^(-1)`, `m = P (m0 + 4 H^T y)`.

This two-by-two inverse gives the following exact values independently of RET:

| Snapshot | Mean `(g,b)` | Posterior covariance `P` | Structural rank |
|---|---|---|---:|
| `prior` | `(1,0)` | `I` | 0 |
| `first` | `(11/9,2/9)` | `[[5,-4],[-4,5]] / 9` | 1 |
| `repeated` | `(21/17,4/17)` | `[[9,-8],[-8,9]] / 17` | 1 |
| `distinct`, `held_out` | `(1,4/9)` | `I / 9` | 2 |

For each row `h=(x,1)`, the mean-response variance is `h P h^T`. A future noisy
observation has variance `h P h^T + 1/4`; these quantities must not be relabeled.

| Snapshot | Mean variances at `x=(-1,0,+1)` | Future-observation variances at `x=(-1,0,+1)` |
|---|---|---|
| `prior` | `(2,1,2)` | `(9/4,5/4,9/4)` |
| `first` | `(2,5/9,2/9)` | `(9/4,29/36,17/36)` |
| `repeated` | `(2,9/17,2/17)` | `(9/4,53/68,25/68)` |
| `distinct`, `held_out` | `(2/9,1/9,2/9)` | `(17/36,13/36,17/36)` |

After the first reading, the null direction `(-1/2,1/2)` leaves the observed
mean fixed and changes the target mean by one. Repeating the same row retains
this ambiguity, even though the same-level mean variance decreases from
`2/9` to `2/17`. Adding either available distinct level resolves the two-parameter
structural ambiguity. The chosen `minus` row identifies the target with row
weights `(0,1)` after the `distinct` branch. Gain and offset still have positive
posterior variance `1/9`; structural identification is not finite-sample
certainty. All candidate results separately report displayed-pair separation
and identification after appending that row alone, without an action score.

## Byte-bound provenance and replay

Each retained raw JSON capture declares synthetic origin, the fixed dyadic
arithmetic generator, synthetic device/session/calibration identity, timestamp,
action and purpose, exact reference/response/row, parameter order, observation
payload and declared noise. No random Gaussian draws or physical captures are
claimed. SHA-256 and byte length are computed from the actual retained bytes
and bound into public `SourceRef` and `EvidenceRecord` objects.

`demo.raw_sources` is the immutable union of seven distinct byte strings across
the branches. `demo.replays["repeated"]` and `demo.replays["held_out"]` are public
verified `ReplayResult` objects, with manifests for two and six records
respectively. Both use their actual source-byte subsets. To replay one branch:

```python
from det8.ret import replay_manifest

manifest = demo.replays["held_out"].manifest
used = {source.sha256 for record in manifest.records for source in record.sources}
raw = {key: demo.raw_sources[key] for key in used}
verified = replay_manifest(manifest, raw_sources=raw)
```

The unused branch's bytes must not be passed as if they belonged to the chosen
manifest. Retained validation captures have distinct hashes; identity alone
does not establish physical statistical independence. Replaying checks the
declared computation and supplied bytes, not physical authenticity. There are
zero workflow decisions to verify. Manifests identify the local runtime and
implementation, so this is not a promise of one permanent manifest hash across
different source versions or environments.

This fixture leaves actual reference uncertainty, apparatus stability,
cross-record noise validation, missing-data acquisition, prior selection,
physical costs, target-specific planning and measured benefit outside scope.
