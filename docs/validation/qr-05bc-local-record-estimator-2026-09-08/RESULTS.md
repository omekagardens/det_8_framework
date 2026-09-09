# QR-05BC results

8 September 2026 (Pacific/Honolulu). **Bounded exact gate complete.**
Classification: synthetic finite verification of a stipulated QM/readout model,
not measured-data analysis, apparatus calibration or inferred geometry.

## Main result

The four labeled local records give an unbiased estimator of the chosen
bilinear response functional on the supplied unit rectangle. Independently
integrated weights are

\[
(w_{00},w_{10},w_{01},w_{11})
=\left(\frac19,\frac1{18},\frac1{18},\frac1{36}\right),\qquad
\sum_a w_a=\frac14.
\]

For one fresh shot at each station,

\[
\widehat T=\frac{X_{00}}9+\frac{X_{10}}{18}
          +\frac{X_{01}}{18}+\frac{X_{11}}{36},\qquad
\mathbb E\widehat T=T(V^2If).
\]

These are weights for the specified geometric functional, not probabilities
that should be renormalized to sum to one. V = 1/2 and σ = V⁴ = 1/16.
The independent quantum-instrument and Bernoulli routes agree on the entire
report. A third, tensor-Simpson integration check agrees on every prescribed
geometric integral. See the [frozen protocol and methods](README.md).

| Profile | Corner responses (00,10,01,11) | Target = estimator mean | One-trial variance |
|---|---|---|---|
| zero | (0,0,0,0) | 0 | 25/1296 |
| plus | (1,1,1,1) | 1/4 | 0 |
| minus | (−1,−1,−1,−1) | −1/4 | 0 |
| asymmetric | (1/2,−1/3,2/3,−1/2) | 13/216 | 667/46656 |
| corner00 | (1,−1,−1,−1) | −1/36 | 0 |
| corner11 | (−1,−1,−1,1) | −7/36 | 0 |

All 96 outcome rows remain present: 36 have positive probability and 60 are
structural zero branches. Their postmeasurement states remain unnormalized.
The 16 complete diagonal outcome Kraus operators agree across all 24 station
orders. Because those are complete operators, this comparison is stronger
than a comparison of traces on the six states. It is still a finite fixed-Z
instrument statement, not physical Lorentz covariance or a general QM theorem.

The nonzero variance of the zero-response case explicitly separates equality
of population means from exact reconstruction in a finite trial. The selected
diagonal product preparations and Z measurements are Bernoulli-equivalent;
the passing comparison establishes no quantum advantage.

## The missing interior remains missing

The profiles f⁽⁰⁾ = 0 and f⁽¹⁾ = u(1−u)v(1−v) give the same corner states,
the same 16 probabilities (each 1/16), and the same unnormalized quantum
branches. Their true continuous-profile targets nevertheless differ:

\[
T(V^2 f^{(0)})=0,\qquad T(V^2 f^{(1)})=\frac1{144}.
\]

The four-site estimator has mean zero under both. Its bias for the bubble's
true target is therefore −1/144, even though it remains unbiased for the
bilinear interpolant. This is the intended model-expansion obstruction,
not a failure of the bilinear model or of conventional QM.

The finite capture verifies one complete four-station trial for this pair.
BB's separate product-law argument extends indistinguishability to arbitrary
fresh repetitions at these same sites; no large repeated-trial enumeration
was performed here. More corner shots cannot identify this unseen interior.
Geometry and calibration context are held fixed, with no private fixture IDs
leaking into the public decoder.

## Other controls separate different failure mechanisms

- **Station labels:** the corner00 and corner11 profiles have identical
  complete plus-count histogram laws, but targets −1/36 and −7/36. Their
  labeled laws differ. Wrongly swapping the corner labels exchanges these
  targets; jointly relabeling records and weights preserves each estimate.
- **Wrong geometric quadrature:** the asymmetric true target is 13/216;
  the naive corner-product trapezoid gives 1/8, while a wrong label swap
  gives mean −5/216. These are different arithmetic/information failures,
  not unexplained detector noise. The kernel is bilinear, but its product
  with the response is not integrated exactly by that corner trapezoid.
- **Fresh copies versus no reset:** all four two-shot histories are retained.
  Both modes have zero means and the same one-shot marginals. The sample-mean
  variance is 1/2 for fresh independent copies and 1 for repeated measurement
  of the same unreset qubit. Correct marginals do not certify independence.
- **Known readout calibration:** the biased fixture has true polarization
  1/2, offset 1/8, contrast 5/8 and registered mean 7/16. Inversion of the
  known channel returns 1/2. This is exact synthetic channel algebra, not a
  measured calibration or a finite-shot confidence guarantee.
- **Unknown calibration:** the confound fixtures have different true means,
  0 and 1/2, but the same registered binary law (1/2,1/2) under different
  assignment channels. This is an ambiguity when that calibration is unknown;
  known distinct channels would supply additional information. The blind
  zero-contrast case retains a null corrected mean and explicit refusal.

The public record-only decoder reproduces all 96 estimates and 2,304
record-list permutation checks. The retained report lists 31 named invalid
record refusals and two unknown-calibration refusals. The unit tests add
independent type, container, weight, file-access, source and artifact controls.
These refusal counts are software checks, not detector loss rates.

## Conditional error composition, without a noise claim

For the separately supplied corner-error vector
e = (1/10,−1/20,0,1/8), δF = V²u(1−u)v(1−v), and ε = 1/16:

\[
w\cdot e=\frac{17}{1440},\quad
\widetilde T-T(F)=\frac7{1440},\quad
\epsilon S_R=\frac1{64},\quad
\sum_a|w_ae_a|=\frac5{288},\quad
|\widetilde T-T(F)|\le\frac{19}{576}.
\]

This control checks the stated triangle-bound identity with prescribed
perturbations. Its rational e values are not claimed to be realized by the
one-shot binary records above, or to be a calibrated statistical uncertainty
set. No sharpness, confidence coverage, stochastic independence of error
sources or transfer of BA's 37-receiver certificate follows. Shot variation,
readout bias and interpolation error remain distinct.

## Verification and source history

The input protocol was fixed before implementation/evaluation at SHA-256
`7b07d4961163f4241c2eb0452fc78d992f38995918418b20fd38acdf911cf340`.
This gate starts from pushed BB commit
`8c3bebb32309569fe9bfdd63b111ec2fc5b5e44f`.

Pre-evaluation review corrected harness weaknesses: native rational/string
comparison, input mutation detection, cached-module execution versus frozen
source bytes, and final capture/replay identity brackets. Corresponding tests
were added before the first source freeze. The fixtures and mathematical
protocol did not change. These were pre-run code corrections, not repaired
numerical results or concealed failed captures.

The source freeze was created before the first fixed evaluation. That first
capture succeeded. No implementation, protocol, test, or source-bound README
changed afterward; no failed numerical first capture exists to supersede.

| Verification | Recorded result |
|---|---|
| Python 3.14.0, isolated normal mode | 44 unittest methods passed; 0.824 s reported by unittest |
| Python 3.14.0, isolated optimized mode | The same 44 methods passed; 0.819 s reported by unittest |
| Independent reference-only audit | Exactly one Python 3.11.6 reference evaluation; entire encoded mathematical report agrees; no quantum/observer execution in that audit |
| Evidence safeguards | Non-noop retained-report mutations, strict native/wire types, duplicate JSON keys, size limits, missing/private records, source changes, cached imports and capture/replay byte changes checked |
| Static checks | All four Python files pass Ruff lint and format checks; test guards do not rely on `assert` statements |

The execution durations are observations, not performance benchmarks. The
reference-only audit is not a claim that the full test suite ran on Python
3.11. The final normal and optimized driver replays retained the entire
captured analysis, including the observer report; both succeeded with the
same eight identities and the unchanged 93,015-byte artifact.

The [source freeze](source-freeze.json) contains eight identities: six current
protocol/implementation/test files and both preceding BB documents. It is
1,703 bytes, SHA-256
`c5184de8b4f071f7635b5810ed87e2314247e745e129ce1915e687a48c2d64f0`.
The [complete capture](results.json) is 93,015 bytes, SHA-256
`749d4fae5debaec73e383b52802762e588214c698dab6842d556878c7e98a665`.
The independently audited mathematical subreport has 26,076 canonical bytes,
SHA-256 `b2cb20e6200d15b172d23ea19227fa441eed6509040bbe88634687d6930ed197`.
Hashes give local integrity, not authentication of physical observations.
No old numerical engines, RET/core sources or dependency locks were changed
or reused as new certificates.

## Next useful question: one interior measurement

**QR-05BD is prospective, not executed.** Test genuinely new measurement
access: one fixed interior Z station in addition to the corners. Restrict
the proposed repair to

\[
f(z)=\sum_a c_a\phi_a(z)+\theta b(z),\qquad |f(z)|\le1\text{ on }Q.
\]

At an interior point z* with b(z*) ≠ 0, the population response would give
θ = [f(z*)−∑ₐcₐφₐ(z*)]/b(z*). The corresponding target estimator must use
weights compiled from geometry, not from θ or the answer. Freeze new physical
profile bounds, fixtures, complete record laws, variance and measurement
cost before evaluating them. Five admissible sampled means alone do not
certify |f| ≤ 1 everywhere.

Retain a further-off-model obstruction: a suitably bounded nonnegative
profile proportional to b(z) times squared coordinate distance from z*
vanishes at all five sites but can still change the true integral. Extra
access can repair a specified model family without recovering arbitrary
continuous profiles or guaranteeing better finite-shot precision. The new
integration oracle must cover the higher polynomial degree; BC's Simpson
exactness cannot simply be inherited.

This remains supplied-geometry mathematics. It neither infers a metric nor
supplies a polarization–gravity coupling. Empirical calibration and QR-06
RET integration remain separately gated; main priorities remain RET,
materials monitoring and anomaly triage.
