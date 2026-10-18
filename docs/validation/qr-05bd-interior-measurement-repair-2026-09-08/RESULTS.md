# QR-05BD results

8 September 2026 (Pacific/Honolulu). **The bounded investigative gate is
complete.** One added center measurement repairs population identification
for the declared bilinear-plus-bubble family. It does not recover arbitrary
continuous profiles or guarantee better finite-shot precision. These are
exact finite synthetic results on supplied geometry, not apparatus data,
a new physical law, an ontology test or RET integration.

The [standalone model and execution contract](README.md),
[frozen input](protocol.json) and [complete evidence](results.json) retain
the assumptions and all favorable and unfavorable results.

## What the new observation repairs

Under the supplied normalization, V = 1/2, σ = 1/16, J_b = 1/144 and
b(1/2,1/2) = 1/16. With sites ordered (00,10,01,11,cc), the geometry-only
target weights are

\[
v=\left(\frac1{12},\frac1{36},\frac1{36},0,\frac1{9}\right),
\qquad \sum_i v_i=\frac14.
\]

The five-site evaluation matrix A has the identity on its first four
rows and final row (1/4,1/4,1/4,1/4,1/16). Both independently constructed
decoders D satisfy AD = DA = I₅. In particular, population means recover

\[
c_a=f(z_a),\qquad
\theta=16f(z_{cc})-4\sum_a f(z_a).
\]

For integral row q = (1/9,1/18,1/18,1/36,1/144), v = qD and vA = q.
This full linear-map identity covers the stated model family, not merely
the ten fixtures. Physical preparations in the positive study obey the
sufficient bound max|c_a|+|θ|/16 ≤ 1. The public record-only estimator is
unbiased for its full target throughout that admitted family; a single
record vector need not equal the target, and reconstructed noisy
coefficients need not themselves describe physical states.

The primary sparse quantum/monomial route and independent Bernoulli/beta
route agree on every native report value. All 800 admitted profile/plan
branches remain: 478 positive-probability and 322 zero-probability rows,
with complete unnormalized state diagonals. The four- and five-factor
Kraus banks agree across all 24 and 120 factor schedules, respectively.
This is operator-order consistency for separate copies, not physical
Lorentz covariance or a spacetime-dynamics result.

The first six corner4 profiles reproduce the retained BC geometry,
targets, means, variances and all 96 full branch rows. This is the selected
overlapping restriction; BC's other controls are preserved in its own
capture and are not rerun or re-certified here.

## Bias removal is not uniform precision improvement

Every repair5 mean equals the true target, so its MSE equals its variance.
Both corner plans retain mean Σw_ac_a and bias −θ/144. corner5 averages
two fresh 00 shots before applying the original weights. It has the same
five-shot cost as repair5; corner4 has only four shots.

All entries below are exact. Δ4 and Δ5 mean repair5 MSE minus the
corresponding corner-plan MSE: negative is better, positive is worse.

| Profile | True target | corner4 MSE | corner5 MSE | repair5 MSE | Δ4 | Δ5 |
|---|---:|---:|---:|---:|---:|---:|
| zero | 0 | 25/1296 | 17/1296 | 1/48 | 1/648 | 5/648 |
| plus | 1/4 | 0 | 0 | 0 | 0 | 0 |
| minus | −1/4 | 0 | 0 | 0 | 0 | 0 |
| asymmetric | 13/216 | 667/46656 | 451/46656 | 289/15552 | 25/5832 | 13/1458 |
| corner00 | −1/36 | 0 | 0 | 1/108 | 1/108 | 1/108 |
| corner11 | −7/36 | 0 | 0 | 1/108 | 1/108 | 1/108 |
| bubble | 1/144 | 401/20736 | 91/6912 | 431/20736 | 5/3456 | 79/10368 |
| peak_bubble | 1/9 | 41/1296 | 11/432 | 11/1296 | −5/216 | −11/648 |
| asymmetric_bubble | 19/216 | 703/46656 | 487/46656 | 269/15552 | 13/5832 | 5/729 |
| negative_boundary | −1/48 | 379/20736 | 283/20736 | 109/6912 | −13/5184 | 11/5184 |

At matched five-shot count, repair5 is better in one fixture, equal in
two and worse in seven. Against the smaller corner4 plan it is better in
two, equal in two and worse in six. In particular, negative_boundary
improves against four corner shots but loses against five: omitting cost
would change the impression of this result. These fixed fixtures are not
a probability distribution over real applications or an optimized design
search. No uniform risk reduction or quantum advantage is demonstrated.
The diagonal product-state laws have an exact classical Bernoulli counterpart.

### Shared observations require a covariance term

Writing the repair as B + J_b θ̂ does not make B and θ̂ independent: the
same corner outcomes enter both. The complete joint law gives

\[
\operatorname{Var}(B+J_b\hat\theta)
=\operatorname{Var}(B)+J_b^2\operatorname{Var}(\hat\theta)
+2J_b\operatorname{Cov}(B,\hat\theta).
\]

The covariance-corrected expression agrees with the five-weight variance
in every fixture. The false independence sum differs in six fixtures.
For zero, Var(B) = 25/1296, Var(θ̂) = 320 and Cov(B,θ̂) = −1:
the shortcut gives 5/144, while the correct variance is 1/48.
The θ variance and covariance in the capture refer to raw θ̂, before
the displayed J_b factors. Neither formula is a calibrated sensor-error
model; all copies and ideal readouts are stipulated.

## Boundaries that remain visible

The old bubble and zero profiles have identical corner laws, but their
five-site laws now differ. The additional center access genuinely detects
the declared missing mode. It does not solve unrestricted interpolation:

\[
h=b\big[(u-\tfrac12)^2+(v-\tfrac12)^2\big]
\]

is continuous, nonnegative and bounded by 1/32. It has exactly the zero
profile's complete five-site law and branch states: every outcome vector
has probability 1/32. Nevertheless its true target is 1/1440. The repaired
estimator has mean 0, bias −1/1440, variance 1/48 and MSE 43201/2073600.
Any number of fresh repetitions at those same sites preserves this
observation-law collision. It is a real model/access limitation in the
specified mathematics, not noise or a setup error inferred from a mismatch.

The test integration oracle first verifies Boole moments through degree
five in each coordinate, then checks these target integrals independently.
Its synthetic quadrature nodes are not additional observer measurements.

The separate global controls distinguish two different domain failures:

| Control | Admission bound | Sampled means | Global conclusion |
|---|---:|---|---|
| overshoot | 2 | (1,1,−1,−1,1) | At (1/2,1/4), f = 5/4 and the formal minimum eigenvalue is −1/8: invalid local preparation in the interior |
| valid_uncertified | 2 | (1,1,1,1,0) | Analytic enclosure [0,1] certifies global validity despite failing the chosen sufficient admission rule |

Five valid sampled states do not imply global validity. Conversely,
failure of a conservative bound is not proof of a nonphysical model.
These controls are reported separately and are not passed into the
positive-state branch simulator as admitted profiles.

The public decoder reproduces all 800 branch estimates and 1,600
forward/reverse list-order checks. It retains 102 named malformed-record
refusals across the three plans. Every prescribed slot remains required,
including 11 in repair5 despite its zero target weight. Distinct fresh
00 shots are admitted only under the explicit corner5 quota. Missing
records, physical nondetection and a numerical outcome of zero are not
interchangeable. No loss, drift or unknown-readout calibration was added.

## Verification and source history

The protocol was written before implementation or fixed evaluation at
SHA-256 `68a49ef25e379663a04fa7742d06b28fe3490d12d431ed4f3adc2fddcb907d73`.
The starting published BC commit is
`f7322c7d360f37a399959f80ffbd6b82a53ff3ca`.

Before freezing, review tightened the driver's protocol hash/parse to one
byte snapshot, fixed the primary's center admission to the declared point,
clarified tensor factors versus Hilbert-space dimension in the README,
and completed ordinary test closure bindings and formatting. No engine
evaluation or test execution preceded the first source freeze.
The protocol and fixtures did not change during implementation. The first
capture succeeded; there was no post-first source, mathematical, protocol
or test correction and no failed first capture to supersede.

| Verification | Recorded result |
|---|---|
| Python 3.14.0, isolated normal mode | 44 unittest methods passed; 5.875 s reported by unittest |
| Python 3.14.0, isolated optimized mode | The same 44 methods passed; 5.840 s reported by unittest |
| Independent reference-only audit | Exactly one Python 3.11.6 reference evaluation; entire encoded mathematical report matches; no primary, driver, observer or historical numerical execution in that audit |
| Evidence safeguards | Complete-report mutations, native/wire type changes, source/input/cache changes, JSON duplication and byte caps, selected BC corruption and capture/replay byte changes are refused |
| Static checks | All four Python files pass Ruff lint and format checks; the 44 methods contain no optimization-disabled `assert` statements |

Durations are execution observations, not benchmarks. The reference-only
audit is not a full-suite Python 3.11 compatibility claim. Full normal
and optimized driver replays also pass with unchanged source identities,
freeze and artifact bytes. Tests use temporary synthetic corruption
fixtures; they do not alter the retained evidence or historical sources.

The [source freeze](source-freeze.json) is 2,309 bytes, SHA-256
`3ac7ac90513ca74cb2ed87949e3b629cde4cf51951c32b257990fdb00ed3997c`.
Its 11 identities cover six current protocol/implementation/test files
and five preceding BC documents/artifacts. The [full capture](results.json)
is 956,398 bytes, SHA-256
`30872f9a461270aab14c946d03f6c71aeae8958ef6e72b0a2e01bd0d2606ed8e`.
The audited mathematical subreport is 182,890 canonical bytes, SHA-256
`7bb0babfffd4619c2a5e714e7bdd1ccc10360c3c737f05c15db9448ea7f220ff`.
Hashes support local integrity, not physical authentication or protection
against a hostile host. No RET/core source, dependency, apparatus or
clock experiment belongs to this gate.

## Next proposed gate: target-specific measurement reduction

**QR-05BE is prospective, not executed.** The zero 11 coefficient motivates
a separately declared four-site plan (00,10,01,cc), without changing BD's
five-site acceptance contract. Test pathwise estimator equality and full
marginal record-law equality, then compare retained quantum branches
through the appropriate partial trace of the summed five-factor branches.
Reduced output must not be called the original complete five-factor state.

Include globally admitted profile collisions along the omitted observation
direction: same retained means and target, but different full coefficients
and omitted-site states. This would separate target-specific sufficiency
from full-profile recovery. Retain the broader off-model obstruction.

Compare the new four-shot plan with corner4 at equal cost. A separate
prespecified five-shot reallocation can ask whether a saved shot is useful;
its site must be chosen before the next evaluation, not selected from
favorable fixture scores. Freeze its acquisition contract, all controls
and complete bias/variance/MSE report before computation. No automatic
minimality, optimal allocation, apparatus advantage, unknown-geometry
inference or gravity claim follows. RET quantum integration remains QR-06
work under its own SDK and calibration gates.
