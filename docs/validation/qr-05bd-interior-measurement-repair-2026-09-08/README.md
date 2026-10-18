# QR-05BD: interior-measurement repair for a specified model expansion

8 September 2026 (Pacific/Honolulu). Protocol written before implementation
or fixed evaluation. Exact finite synthetic verification; no apparatus data,
ontology premise, new physical law or RET integration is introduced.

## Model, admission and target

Supply Q = [0,1]² in flat null coordinates u = t+x, v = t−x with c = 1,
signature (+,−), dμ = du dv/2, V = μ(Q), F = V²f and σ = V⁴.
Use R_Q(u,v) = (1−u)(1−v)/2 and the same target as
[BC](../qr-05bc-local-record-estimator-2026-09-08/RESULTS.md):

\[
T(F)=\frac1\sigma\int_Q F R_Q\,d\mu.
\]

Geometry and the future-volume kernel are supplied, not inferred from shot
counts. R_Q is not a quantum instrument or a polarization–gravity coupling.
The local response map specifies possible preparations, not a continuum
quantum-field state. All coordinate positions and local Z axes are stipulated.

Let the corner order be (00,10,01,11), with the usual bilinear basis
φ = ((1−u)(1−v),u(1−v),(1−u)v,uv), and let b = u(1−u)v(1−v).
The expanded profile family is

\[
f=\sum_a c_a\phi_a+\theta b,\qquad
\max_a|c_a|+\frac{|\theta|}{16}\le1.
\]

The inequality is a sufficient admission rule: φ is a nonnegative partition
of unity and 0 ≤ b ≤ 1/16, so the rule guarantees |f| ≤ 1 everywhere.
It is not a necessary condition for physical state validity. The two
prespecified global controls distinguish an actually invalid profile from a
globally valid profile outside this conservative admitted class.

At each station prepare a fresh qubit ρ = (I₂+fZ)/2 and measure the fixed
projectors Πₓ = (I₂+xZ)/2, x ∈ {−1,+1}, Z = diag(1,−1). Retain
the unnormalized branch ΠₓρΠₓ. All copies are independent, including repeat
shots at one station; unreset measurements are not permitted. Nominal
positions repeated across trials are not multiple independent measurements
at an identical spacetime event. A later apparatus model would need actual
localization, axis, drift, readout and loss calibration.

## New access and a population-level repair

Add the center station cc at z* = (1/2,1/2). Compile from geometry alone the
evaluation matrix A of the five functions (φ₀₀,φ₁₀,φ₀₁,φ₁₁,b) at the
five sites. Its inverse must recover (c,θ) from the five population means.
Retain both inverse identities; this is a finite linear-map certificate, not
only interpolation of a few chosen profiles.

Writing J_b = T(V²b), the repaired target is

\[
T(F)=\sum_a w_ac_a+
\frac{J_b}{b(z_*)}\left(f(z_*)-\sum_a\phi_a(z_*)c_a\right),
\qquad w_a=T(V^2\phi_a).
\]

The associated five weights must be derived before selecting any profile
responses. Neither θ nor the true target is supplied to the observer.
Population identification does not imply exact finite-shot reconstruction
or that noisy reconstructed coefficients define a physical state.

All prescribed records remain required even if a computed target weight
vanishes. Target-specific plan pruning would be a separate question, not an
unannounced change in this complete five-site acquisition contract.

## Frozen plans and fixtures

The [machine-readable protocol](protocol.json) specifies ten admitted
profiles. The first six have θ = 0 and reproduce BC's corner fixtures.
Additional cases include a small bubble, a center-saturating bubble, a
mixed asymmetric response and a negative boundary case. Their choices
precede evaluation; no allocation is fitted to their results.

| Plan | Fresh event slots, in bit order | Cost and question |
|---|---|---|
| corner4 | 00#1,10#1,01#1,11#1 | Four shots; original corner-interpolant target estimator |
| repair5 | 00#1,10#1,01#1,11#1,cc#1 | Five shots; new geometry-compiled target estimator |
| corner5 | 00#1,00#2,10#1,01#1,11#1 | Five shots; average the two 00 outcomes, then use the original corner weights |

Retain every one of the 16 or 32 outcome vectors for each plan/profile,
including probability-zero rows and full unnormalized state diagonals.
Computational basis bits run lexicographically with bit 0 meaning Z = +1;
the first listed event is the most significant factor. Compare full Kraus
operators across all permutations of four and five tensor factors
(Hilbert-space dimensions 16 and 32).
The two 00 shots in corner5 are distinct tensor factors and distinct record
identities, not duplicated files or a reused unreset qubit.

Score every plan against the same full true target T(V²f), retaining mean,
bias, variance and MSE = variance+bias². The corner plans may remain biased
when θ ≠ 0. Compare repair5 with corner5 at equal five-shot count, and show
corner4 separately at its smaller cost. Counted shots are not a calibrated
hardware time/energy expense or evidence of optimal allocation.

An additional decomposition control writes the repaired estimator as the
corner estimator plus J_b times an estimate of θ. Both terms reuse the
corner outcomes, so their covariance must be retained. The falsely
independent variance sum is a negative control, not an alternate valid
uncertainty model. All likelihoods remain classical Bernoulli-equivalent
for these diagonal product states; no quantum advantage is claimed.

## Further-off-model and global-validity controls

The broader continuous-profile witness is

\[
h(u,v)=b(u,v)\left[(u-\tfrac12)^2+(v-\tfrac12)^2\right].
\]

It vanishes at all five sampled sites, is nonnegative and bounded above by
1/32 on Q, and is positive on an interior region. Retain its complete
five-site quantum record law versus the zero profile and independently
integrate its true target. This tests the limit of the repaired family,
not a failure of the conditional five-parameter inverse.

The overshoot control uses c = (1,1,−1,−1), θ = 16 and witness point
(1/2,1/4). Check all five sampled means, then the interior value and formal
minimum eigenvalue. A negative eigenvalue diagnoses an inadmissible
preparation map; it must not be passed to the positive-state simulator as a
physical state. The other control, c = (1,1,1,1), θ = −16, is globally
bounded in [0,1] but lies outside the chosen sufficient admission rule.
Its rejection is a model-domain refusal, not proof of nonphysical behavior.

## Independent computation and observer contract

- Primary: adapt only the preceding primary's sparse tensor/projector and
  monomial-polynomial helpers into new local source; derive A, its inverse,
  target integrals, full branch states and enumerated estimator moments.
- Reference: independent Bernoulli products, beta-moment integration and
  direct coefficient-recovery formula. It does not import the primary or
  any old engine or target table.
- Tests: a distinct tensor-Boole integration oracle. Verify its one-variable
  moments through degree five before applying it to the prescribed product
  integrands. BC's degree-three Simpson guarantee is not reused. These
  oracle evaluations are private synthetic checks, not observer readouts.

The public estimator takes only complete records, compiled station weights
and a fixed public plan ID. It averages each station's declared fresh shots,
then applies the weights. Each record retains the 15 exact fields in the
protocol, including acquisition-plan, station and shot identity. Opaque
registration references bind those slots; they do not encode a profile,
likelihood, state, θ, target or seed. Aggregation occurs only when every
record is available at the declared collector.

Missing, duplicate, mismatched, unavailable, unattempted, private-field,
quota or type-invalid inputs are refused in normal and optimized Python.
Repeated station labels with distinct permitted shot IDs are valid only in
corner5. Missing records are not outcome zero or physical nondetection;
loss would require an expanded POVM/selection model. Forward/reverse list
order checks apply to every admitted profile/plan branch.

## Evidence and execution boundary

No fixed calculation runs until the protocol, both engines, driver and tests
are held and their first source identity is frozen. Reuse of reviewed
mechanical helpers is documented; it does not transfer old certificates.
The driver binds six current files plus five preceding BC documents/artifacts
by exact bytes. It never imports or executes BC's numerical engines.
The first six corner4 reports are compared with the retained BC restriction.

Capture is create-only. Fresh execution uses inspected source bytes, native
report comparison preserves Fraction/int/string distinctions, and inputs
must remain unchanged. Strict bounded JSON, complete replay and final
source/freeze/artifact identity checks remain active under optimization.
Preserve any failed first capture and document any post-first correction.
No runtime benchmark, RET/core mutation, dependency change, apparatus action,
clock experiment or gravity-dynamics claim belongs to this gate. Small runs
must not overlap a timing-sensitive RET rehearsal.

Acceptance requires complete independent reports, matrix inverse identities,
all plan laws/moments, the intended blind spot and global-admission controls,
record-only decoder checks and adversarial tests to agree. MSE differences
must be reported with their sign, not selected for favorable outcomes.
This is a conditional observation/estimation result on supplied geometry;
calibration, unrestricted profiles, unknown geometry and RET integration
remain separate questions. See [RESULTS.md](RESULTS.md) after execution.

## Reproduction

From this directory after publication:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bd.py
python3 -I -O -B test_qr05bd.py
```

Original creation uses `study.py --freeze source-freeze.json` followed by
`study.py --capture results.json`. These must not overwrite retained files.
Replay permits a different optimization mode while requiring the same
frozen sources and mathematical evidence. Local hashes are integrity checks,
not authentication of physical observations or a hostile host.
