# RI-33 — observation channel, clock ambiguity and public-data qualification

24 September 2026 UTC. **Cycle-1 design and conditional mathematics.** This
implements the first measurement-design packet in the
[native geometry/gravity programme](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md).
It specifies a small exact timing inference target and qualifies public-data
metadata. There is no new simulator, acquired strain dataset, fitted physical
parameter, native-to-observable map or DET-versus-GR result in this packet.

The two examples below have different input types. Four-timestamp clock transfer
tests an identifiability contract; GWOSC strain tests calibrated-data provenance
and a future conventional analysis. Strain samples must never be relabeled as
the clock messages or native births. Both use the same distinction between
records, channel assumptions, derived quantities and interpretation.

## 1. Observation contract and record roles

Keep these stages separate:

`native candidate/history -> record formation -> acquisition/emission attempt
-> detector output -> retention/transmission -> analyst selection -> inference`.

The native history is a latent model object. A future candidate must supply a
law connecting it to record formation. That connection is absent here. An
observation channel may nevertheless be specified and tested conditionally.

| Input class | Required information | What it licenses |
|---|---|---|
| Attempt/exposure log | Source and attempt IDs, actual/proposed role, channel/settings, exposure duration/unit, local clock and closure rule. | Statements about actual attempts only if the log is available and justified; an expected ID is not proof of emission. |
| Detector record | Immutable acquisition ID, source association evidence, channel/outcome, local timestamp/unit, resolution/error declaration, status and provenance. | A retained registered output; not automatically a fundamental event. |
| Missing/null record | Distinguish a registered null, a receiver cutoff absence, an acquisition gap and an unavailable file. | Only the corresponding finite absence statement. None supplies an infinite horizon. |
| Calibration/channel declaration | Version/validity, units, rate/offset assumptions, latency, efficiency, false detections, dead time, dependence/covariance and systematic bounds. | Conditional conversion or uncertainty set; declarations alone do not authenticate calibration. |
| Selection/evaluation declaration | Included IDs and roles, exclusions, window, development/calibration/evaluation split and prior access. | Reproducible selection; unselected, proposed or withheld rows cannot narrow training compatibility. |

Retain all actual attempts and exclusion reasons. Detector failure, missing
transmission and analyst exclusion are different mechanisms. Append analysis
results without changing committed/acquired records. Preserve the complete
input and premise identity, including excluded rows and settings; a hash binds
bytes under its usual assumptions but does not establish acquisition, calibration
or custody. The future implementation must refuse incomplete required inputs
rather than fill them from simulator truth.

Outputs must distinguish `compatible_given_premises`,
`incompatible_given_premises`, `insufficient_records` and
`unsupported_clock_or_channel_model`. A finite compatible interval is not a
confidence interval, an actuation recommendation or evidence that the premises
describe an instrument. Preserve the actual source-freeze, custody and
protected-validation rules of any later selected evaluation workflow.

## 2. Exact two-way timing target

### Admitted model and data

There are two clocks with **one supplied shared transfer-time parameter** t:
`C_A(t)=t+beta_A`, `C_B(t)=t+beta_B`. Rates are one in common units and offsets
are constant over an exchange. This is a conditional clock model, not a
consequence of each clock having unit rate with respect to its own proper
time. Motion, gravitational rate shifts, drift and uncertain endpoint latency
require a separately justified extension or correction/error model.

One matched exchange contains four exact local timestamps:

| Symbol | Actual event |
|---|---|
| A1 | A sends the identified outbound message. |
| B2 | B receives that message. |
| B3 | B sends the identified reply after receiving it. |
| A4 | A receives that reply. |

The physical transfer delays are p and q, both nonnegative in t units.
The turnaround r is nonnegative. Timestamp events and latency corrections
must be defined consistently; a raw detector edge is not silently an ideal
arrival time. Define

`theta=beta_B-beta_A`, `u=B2-A1`, `v=A4-B3`, `r=B3-B2`.

Then `u=theta+p`, `v=-theta+q`, and
`S=u+v=(A4-A1)-r=p+q`.
Thus a round trip identifies the sum of delays in this model; half the
cross-clock difference gives `(u-v)/2=theta+(p-q)/2`, not theta alone.

### Exact compatibility theorem

For exact readings and nonnegative delays, refuse r<0 and S<0 as
`incompatible_given_premises`. Otherwise every compatible offset is exactly

`I0=[-v,u]`.

Optional, separately justified bounds `p in [pL,pU]`, `q in [qL,qU]`,
and `p-q in [hL,hU]` give the exact interval

`I = I0 intersect [u-pU,u-pL] intersect [qL-v,qU-v]`

`        intersect [(u-v-hU)/2,(u-v-hL)/2]`.

Omit the associated interval when that premise is absent. Directional bounds
are ordered, finite and nonnegative; asymmetry bounds are finite and ordered.
Invalid declarations are input errors, distinct from an empty compatibility
set under well-formed declarations. No directional upper bound or reciprocity
assumption is required for I0. Singleton intervals are admitted.
An empty set supplies no estimate, radius or precision verdict.

**Proof.** Solving the two observation equations gives `p=u-theta` and
`q=v+theta`. Their nonnegativity is equivalent to `-v<=theta<=u`.
Substituting these expressions into each optional bound gives exactly its
displayed interval. Conversely, take any theta in their intersection and
choose `beta_A=0`, `beta_B=theta`, `t1=A1`, `t2=B2-theta`,
`t3=B3-theta`, `t4=A4`. Then `t2-t1=p>=0`, `t3-t2=r>=0`, and
`t4-t3=q>=0`, so all four readings, chronology and bounds are attained.
This proves sufficiency on the whole real domain, not merely selected fixtures.

For nonempty `I=[L,U]`, the midpoint minimizes worst-case absolute offset
error and its radius is `(U-L)/2`: the endpoint errors force any estimate's
worst error to be at least half their separation, and the midpoint attains
that bound. Precision to tolerance T>=0 means this radius is at most T.
It does not mean `abs(theta)<=T`. Reciprocity `p=q` is the optional premise
`hL=hU=0`; it identifies theta only when the remaining premises are compatible.

### Exact fixtures for the future independent test author

All values are rational in one common time unit. These are specified fixtures,
not acquired readings or a report of simulator execution.

| Readings (A1,B2,B3,A4) | Additional premise | Required result |
|---|---|---|
| (0,5,7,8) | None | r=2, S=6, I=[-1,5], minimax center 2 and radius 3. |
| (0,5,7,8) | p=q | I={2}, p=q=3. |
| (0,5,7,8) | p-q in [-1,1] | I=[3/2,5/2], radius 1/2. |
| (0,5,7,8) | p,q both in [2,4] | I=[1,3], radius 1. |
| (0,5,7,8) | p-q=7 | Empty intersection: incompatible. |
| (0,5,4,8) | None | Reject negative turnaround despite nonnegative u+v. |
| (0,1,3,1) | None | Reject S=-1. |

The first row has, for example, two indistinguishable explanations:
`(theta,p,q)=(2,3,3)` and `(1,4,2)`. Both reproduce every timestamp and
the same turnaround. Identifying offset from those readings alone is therefore
impossible, even though round-trip delay is known. The ambiguity is a model
identifiability result, not an assertion about every possible clock experiment.

## 3. Uncertain timestamps: preserve the joint feasible set

The exact theorem does **not** license feeding interval midpoints into it.
For bounded-error records, introduce latent exact readings
`z=(a1,b2,b3,a4)` in a declared simultaneous set E. Preserve correlations,
shared systematic parameters, chronological constraints and all relevant
exchanges. For fixed unit rates the correct general contract is projection
onto theta of

`z in E; b3-b2>=0; b2-a1=theta+p; a4-b3=-theta+q;`

`p>=0; q>=0; and all declared directional/asymmetry constraints`.

When E is a bounded rational polytope, this is a rational linear feasibility
and projection problem. A bounded nonempty feasible set has attained extrema;
convexity makes its theta projection an interval. No general solver or exact
projection formula is implemented in this packet. Nonlinear rate/drift models
need their own admitted set and analysis, not a false linear certificate.
Nonconvex calibration or selection hypotheses can produce a union instead;
do not promise a single interval without the convexity premise.

Separate marginal intervals for `u=b2-a1` and `v=a4-b3` can enlarge E after
dependencies or turnaround information are dropped. Results then describe an
outer relaxation, not exact attainable precision. A shared theta across
exchanges or a shared calibration nuisance must stay shared. Marginal
confidence intervals are not automatically simultaneous deterministic bounds;
neither sampling confidence nor coverage is inferred from interval arithmetic.

Two exact negative controls make the distinction concrete:

- If E consists of `(0,z,z,2*z)` for z in [1,2] and reciprocity is supplied,
  then u=v=z and theta=0. Independent marginals u,v in [1,2] instead allow
  theta in [-1/2,1/2]. Their extra values have no witness in E.
- If A1=0, A4=10, B2 in [4,5], B3 in [0,5], and reciprocity is supplied,
  the retained chronology B3>=B2 gives theta in [-1,0]. Every value is
  attained by B2=B3=theta+5. Independent difference intervals u in [4,5],
  v in [5,10] instead allow [-3,0]; the endpoint -3 requires negative
  turnaround. Even independent timestamp boxes do not justify dropping
  chronology when forming difference intervals.

A relaxation may be a valid conservative enclosure; its endpoints and minimax
radius need not be attainable or sharp for the original joint data model.

The first implementation successor should support an exact four-timestamp exchange
and the optional finite bounds only. An uncertain-clock solver is a separate
reviewed increment. Synthetic negative controls must include drift, unmatched
message IDs, source/receipt confusion, quantization, negative turnaround,
finite absence and an inadmissible correlation relaxation. Their proper result
may be refusal rather than a narrower answer.

## 4. Count/efficiency obstruction

For a supplied finite Poisson formation rate lambda>=0, known finite exposure
T>0 and independent constant retention/detection efficiency eta in [0,1],
the retained count's generating function is

`E[z^Nretained] = exp(lambda*T*((1-eta+eta*z)-1))`

`                 = exp(eta*lambda*T*(z-1))`.

Thus the retained-count law identifies only eta*lambda within this model;
finite observations still require an estimation/error analysis. At T=0 even
the product is unidentified. For example,
`(lambda,eta)=(10,1/5)` and `(5,2/5)` give identical retained-count laws at
every exposure T. More counts do not separately identify the factors. A
separately justified efficiency measurement or formation premise is required.
Unknown exposure or a count-to-volume scale adds ambiguity. Dead time,
history-dependent detection, backgrounds or correlated loss invalidate this
simple thinning model and require their own channel. It supplies no mapping
between instrument detections and native event counts.

## 5. GWOSC metadata qualification card

**Decision:** select the original event release's corrected V2 4096 Hz,
32-second H1/L1 HDF5 pair as a *metadata-qualified acquisition candidate*.
Scientific file bodies have not been downloaded or inspected. They are not
yet admitted analysis inputs; checksums below are publisher declarations.
The separate catalogue/event version number is not the strain product version.

Source: [GW150914 original event release](https://gwosc.org/events/GW150914/),
DOI [10.7935/K5MW2F23](https://doi.org/10.7935/K5MW2F23).
Its 4096 Hz table links the exact files below. The expected GPS interval is
`[1126259446,1126259478)`, giving 131072 samples per detector if the files match
their advertised start, duration and rate. Actual headers/time arrays remain
to be checked. Strain is a calibrated dimensionless product, not raw photodiode
data or a list of native events.

| Candidate file | Published MD5, not locally verified |
|---|---|
| [H-H1_LOSC_4_V2-1126259446-32.hdf5](https://gwosc.org/GW150914data/H-H1_LOSC_4_V2-1126259446-32.hdf5) | `50441a42c13fc1f14e5c4ea5527f1515` |
| [L-L1_LOSC_4_V2-1126259446-32.hdf5](https://gwosc.org/GW150914data/L-L1_LOSC_4_V2-1126259446-32.hdf5) | `361ae6a040a9fef7897b1e0124d5b0a1` |

The values were independently read from the official
[checksum manifest](https://gwosc.org/GW150914data/md5.txt). Upon acquisition,
compare the declared MD5 for transfer-error detection and compute local
SHA-256 plus retrieval/source provenance for the frozen inputs. Neither MD5
nor an unanchored local hash authenticates calibration or custody.

[GWOSC technical notes](https://gwosc.org/techdetails/) distinguish V2/C02
calibration from V1/C01 and document correction of the old approximately
1 ms downsampling offset. They specify frequency-dependent magnitude/phase
calibration uncertainty, 1 Hz quality/injection flags, NaNs when DATA is false,
and uncalibrated content below 10 Hz. Injection bits use one for **no** injection.
Interpret flags for this release; do not import an unrelated run's schema.
The 32-second and longer files were downsampled independently, so overlapping
samples need not be bit-identical. Exact file selection must precede comparison.

The public [O1 calibration-uncertainty archive](https://dcc.ligo.org/T2100313/public)
has a [README](https://dcc.ligo.org/public/0177/T2100313/003/README) connecting
the estimates to final C02 calibration and describing detector/hour/frequency
dependent magnitude and phase estimates. Its one-sigma bands are not
simultaneous deterministic bounds. Exact applicable archive members, numerical
values, interpolation and correlations remain unqualified. The
[historical tutorial](https://gwosc.org/GW150914data/GW150914_tutorial.html)
is unmaintained and names V1 files; it does not override this V2 selection.

### Remaining admission checks and first analysis boundary

| Required before the corresponding claim | Current state / next action |
|---|---|
| File identity and schema | Only metadata checked. Retrieve the exact two files in a later scoped acquisition; verify publisher checksum, local SHA-256, channel/unit, shape, sample grid and GPS bounds. Refuse substitution or mismatch. |
| Data validity | Inspect DATA, quality/injection channels and finite samples. Retain excluded intervals and reasons; never interpolate/filter across missing spans silently. No flags have been evaluated here. |
| Calibration uncertainty | Select the matching detector/epoch/C02 uncertainty artifacts and their interpretation, including relevant correlation assumptions. Numerical envelopes have not been supplied or checked. |
| Processing reproducibility | Freeze filter/edge behavior, sample indexing, comparison intervals, software versions and reference calculation before examining the selected samples. A familiar old tutorial is not authority to fetch V1. |
| Scientific interpretation | No native law currently predicts this readout. This known public event is development/reference material, not a blind holdout or a new detection experiment. |

The first useful execution, after separate scope review, is an input/quality
manifest and conventional calibrated-strain transient reproduction using the
qualified product. Predeclare a central event display and surrounding
comparison intervals, exact conditioning and an independent reference.
Do not claim a detection significance, travel-time precision or native gravity
residual from visual alignment or an unmodeled cross-correlation peak.
If longer context or a noise estimate is needed, qualify that exact companion
product and its processing instead of silently enlarging the dataset.
Follow [GWOSC reuse and acknowledgment guidance](https://gwosc.org/data/).

## 6. Bounded next handoff

This dossier completes a design increment, not the execution of every planned
test or acquisition. After independent review, the next coordinator-owned
packet may implement the exact timing theorem and fixture/refusal contract
in a new standalone standard-library bundle. It must expose explicit premise
identity and reproduce each attaining witness without simulator-truth access.
The uncertain-input generalization and the public-data acquisition/processing
packet require separate bounded scopes. No project-wide import or RET change
is required for the exact timing consumer.

QR independently owns RI-32's native candidate dossier. Neither this contract
nor its public-data card closes QR's missing law, manifold, mass/source or
physical-readout premises. Existing accepted model sources, the RI-31 plan,
historical witnesses, actual calibration/freeze/custody prerequisites and the
RET implementation pause remain unchanged. Root owns review/publication;
no automatic acquisition, protected evaluation or theorem successor follows.
