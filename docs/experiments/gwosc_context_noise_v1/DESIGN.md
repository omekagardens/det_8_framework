# RI-67 — a conditional noise model for the fixed context comparison

24 September 2026 UTC. **Independently accepted prospective design and mathematical
argument.** This packet writes this document only. No sampler,
implementation, new coefficient calculation, observed statistic or new data
acquisition has run. The successor described below requires its own source
review and execution authorization.

The purpose is to move from the accepted finite processing-window comparison
to a precisely conditional uncertainty calculation. RI-64 established that
short, specified-context and published full-record processing can differ on the
same central samples. It did not establish a noise distribution, physical error
or calibrated agreement. The [RI-31 programme](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md)
requires synthetic signal/noise checks before a conventional public-data analysis
(ME-02); a native comparison still requires a quantitative observable map
(ME-03). Neither requirement is replaced by the theorem below.

## 1. Retained measurement and first implementation boundary

Retain the [RI-62/64 window and observation contract](../gwosc_observed_context_v1/DESIGN.md):

```text
N=2769, L=4096, T=10961
I=(0,1,27,805,1384,2741,2767,2768)
x=X[65536:68305]
w=X[61440:72401]=(z[:L],x,z[L:])
z=concat(X[61440:65536],X[68305:72401])
central clock = GPS 1126259462 + j/4096, 0 <= j < N.
```

F_m is the exact rational finite filter with the admitted binary64 coefficients,
17 stages, section order, DC initialization, odd extension, reversals and
unpadding. It is distinct from rounded production and Decimal calculations.
Let E insert N central values into an otherwise zero T-vector, C=E^T select
that center, and J select I, in the stated order. Put

```text
P = J F_N C                  (8 by T)
Q = J C F_T                  (8 by T)
A = Q-P                     (8 by T).
```

Thus A w is the exact eight-row context-minus-short result. Its rows are
`(b_left,a,b_right)` in RI-64's coefficient notation. A and the clock are
unchanged by introducing a noise model. The 32-second rounded baseline is
still a descriptive comparison; this packet neither reconstructs exact
F_131072 nor includes that baseline in a likelihood.

The first implementation successor is **synthetic only**: the exact small
operator fixtures in section 4, eight-output rational surrogate models in
section 5, and their fixed sampling checks. The surrogate maps are named
explicitly and must never be reported as the admitted A. No observed HDF5,
CROP, REFERENCE or OBSERVED_CONTEXT file belongs in that executable closure.
It does not regenerate the sixteen admitted adjoints. Section 8 states the
separate integration gate for numerical covariance of the admitted A.

The existing actual-specific numerical thresholds remain unchanged:
whole-vector production/Decimal discrepancy at most `1e-9` times its own input
peak; direct context-interval width at most `1e-12` times the extended input
peak; selected output endpoint distances at most the original `1e-9` peak
limits, and difference distance at most `1e-9*(A_x+A_w)`. There is no unit floor.
The statistical checks below do not replace or loosen any of those gates.

## 2. Shared-noise covariance

Assume a fixed finite raw-window model `w=m+n`, with known deterministic mean
m, E[n]=0 and known deterministic symmetric positive-semidefinite covariance
Sigma. Finite second moments suffice for this section. No Gaussianity,
stationarity, white noise or detector independence is required. Then

```text
mu = A m
Omega = Cov(A n) = A Sigma A^T
      = Q Sigma Q^T + P Sigma P^T
        - Q Sigma P^T - P Sigma Q^T.                         (1)
```

Proof: `A n=(Q-P)n`; distribute the outer product and take its expectation.
Positive semidefiniteness follows from
`v^T Omega v=(A^T v)^T Sigma (A^T v)>=0`. Short and context outputs reuse the
same raw noise. Dropping their cross terms is generally wrong, even if raw
samples are independent. Neither a smaller numerical interval nor a larger
context window proves smaller statistical variance.

An optional two-detector statement uses
`A_stack=diag(A_H,A_L)` and the **joint** covariance
`Sigma_stack=[[Sigma_HH,Sigma_HL],[Sigma_LH,Sigma_LL]]`.
Its cross block is `A_H Sigma_HL A_L^T`. Setting Sigma_HL to zero is an explicit
model assumption, selected only in a named toy if used. No detector independence
is inferred from separate processing or different filenames. Means have strain
units and covariances have squared strain units; the unit-noise toy coordinates
below are dimensionless mathematical fixtures, not calibrated detector noise.

## 3. Conditional Gaussian theorem, support and alternatives

**Theorem.** Fix A, m and Sigma before the random draw. If
`n ~ N(0,Sigma)`, let r=rank(Omega), let Omega^+ be its Moore-Penrose inverse,
and let S=range(Omega). For `Y=A(m+n)` under this fully specified model:

1. `Y-mu` belongs to S almost surely.
2. For r>0, `q=(Y-mu)^T Omega^+ (Y-mu)` has the central chi-square law with
   r degrees of freedom.
3. For r=0, Y=mu almost surely and q=0 deterministically. A nonzero residual
   fails the support condition; it is not admitted merely because Omega^+=0.

**Proof.** Diagonalize Omega on its positive eigenspace as
`U_r diag(lambda_1,...,lambda_r) U_r^T`, with orthonormal U_r and positive
lambda_i. A centered Gaussian with this covariance has the same law as
`U_r diag(sqrt(lambda_i)) Z`, where Z has r independent standard normal
coordinates. Its orthogonal complement is zero almost surely. Substitution
in the quadratic gives `Z^T Z`. The zero-rank case has zero variance in every
coordinate and hence a constant vector. This also proves the support claim.

For a fixed alternative mean shift h, still scored against the frozen null
mean mu, if h is in S then q has noncentral chi-square law with the same rank
and noncentrality `lambda=h^T Omega^+ h`. If h is outside S, the alternative
is outside the null support almost surely. Projection onto S and reporting only
q would discard this incompatibility. These statements concern a specified
mathematical model; an observed departure can instead indicate a wrong noise,
response, calibration or numerical model.

The mean and covariance are known in this theorem, not estimated from the
scored observations. Replacing Omega by an estimated PSD/covariance invalidates
the naive fixed chi-square reference law. An independent off-source estimate
also has estimation uncertainty; independence alone does not make it the true
known covariance. Fitting mean parameters, choosing a lag or selecting rows
from the data likewise requires a new distributional derivation and selection
accounting. Subtracting an informal number of fitted parameters is not allowed.

The implementation must validate a claimed exact rational covariance as
symmetric PSD, its rank exactly, and all four Moore-Penrose identities. It must
check support before assigning a null score. A generic floating eigentolerance
is not a rank or support oracle. Singular fixtures use rational factors and
exact elimination, with expected ranks and null vectors given below.

## 4. Exact small-operator and covariance fixtures

All entries in this section are exact Fractions. Expected answers below are
independent of the implementation to be written. Check every matrix entry,
all covariance routes, all ranks and the stated quadratic values.

**FIR boundary fixture.** Use one explicitly synthetic SOS
`(b0,b1,b2,a0,a1,a2)=(1,1/2,0,1,0,0)`, one stage, padlen=0,
short length 2 and extended length 4, with center indices (1,2). This is a toy,
not a change to the admitted 17-stage filter. Constant-prehistory forward and
backward passes give

```text
F2 = [[7/4,1/2], [3/4,3/2]]
F4 = [[7/4,1/2,0,0], [1/2,5/4,1/2,0],
      [0,1/2,5/4,1/2], [0,0,3/4,3/2]]
P  = [[0,7/4,1/2,0], [0,3/4,3/2,0]]
Q  = [[1/2,5/4,1/2,0], [0,1/2,5/4,1/2]]
A  = [[1/2,-1/2,0,0], [0,-1/4,-1/4,1/2]].
```

With Sigma=I4, expected covariance and cross covariance are

```text
QQ^T = [[33/16,5/4], [5/4,33/16]]
PP^T = [[53/16,33/16], [33/16,45/16]]
QP^T = [[39/16,27/16], [3/2,9/4]]
Omega = [[1/2,1/8], [1/8,3/8]]
det(Omega)=11/64, rank=2
Omega^-1 = [[24/11,-8/11],[-8/11,32/11]].
```

The wrong independent-output formula gives
`[[43/8,53/16],[53/16,39/8]]`; require its rejection as the covariance of
this named shared-input fixture. This is not a ban on independence in an
otherwise explicitly specified model. For residual (1,0), q=24/11. For a raw
unit impulse at coordinate 0, A e0=(1/2,0), giving q=6/11.
Reconstruct F2/F4 from every basis vector using the published independent
[exact DFI oracle](../gwosc_context_operator_v1/oracle.py), and separately use
the displayed matrices to derive P,Q,A and (1). The oracle remains reused
published source, not a newly authored independent implementation.

**Exact cancellation.** For the identity filter at the same lengths, Q=P=C,
A=0 and Omega=0 for Sigma=I4, despite nonzero short/context marginal
covariances. Every raw vector maps to zero difference. A scored residual
(0,1) must fail support, not pass with q=0.

**Rank one.** For Omega=`[[1,1],[1,1]]`, expected rank=1,
Omega^+=Omega/4, support `{(u,u)}`, and q((2,2))=4. Residual (1,-1) is
outside support although its pseudoinverse quadratic is zero.

**Two-detector cross block.** For two scalar outputs U and `(3U+4V)/5`
from independent unit-variance U,V, the joint covariance is
`[[1,3/5],[3/5,1]]`, determinant 16/25, with inverse
`[[25/16,-15/16],[-15/16,25/16]]`. Replacing its off-diagonal entries by zero
must fail this fixture. This supplies no empirical claim about H1/L1.

Also refuse malformed dimensions, asymmetric covariance, negative covariance
(e.g. diag(1,-1)), incorrect rank, incorrect pseudoinverse, nonfinite values,
and a caller attempting to use an estimated covariance under the known-covariance
contract. Do not add a diagonal ridge or project a bad matrix onto PSD silently.

## 5. Frozen eight-output simulation models

Here s and t denote synthetic short/context output surrogates, not P w and Q w
for the admitted filter. All models score `y=t-s` against null mean zero.
Let U8,V8 be independent eight-dimensional standard normals, U2 a
two-dimensional standard normal, and D be the 8 by 2 matrix with rows
`(1,0),(0,1),(1,0),(0,1),(1,0),(0,1),(1,0),(0,1)`.
D^T D=4 I2. In G4, e0 is the first basis vector in R^2; the later
support-alternative e0 and e2 are basis vectors in R^8. Every factor, mean
and covariance in this table is exact rational.

| ID | s; t | Omega; rank; inverse/pseudoinverse | Trials; latent columns; seed |
|---|---|---|---|
| G0 | U8; U8 | 0; 0; 0 | 256; 8; 2026092400 |
| G1 | U8; V8 | 2 I8; 8; I8/2 | 32768; 16; 2026092401 |
| G2 | U8; (3U8+4V8)/5 | (4/5) I8; 8; (5/4) I8 | 32768; 16; 2026092402 |
| G3 | D U2; 2 D U2 | D D^T; 2; D D^T/16 | 32768; 2; 2026092403 |
| G4 | D U2; 2 D U2 + 8 D e0 | same as G3; shifted alternative lambda=64 | 32768; 2; 2026092404 |

G2 has cross covariance `(3/5) I8`; pretending its outputs independent gives
2 I8 instead of (4/5) I8. G3 has cross covariance `2 D D^T`; dropping it gives
`5 D D^T` instead of D D^T. Check these exact failures before sampling.
Support for G3/G4 consists of vectors whose even coordinates agree and whose
odd coordinates agree. G4's shift lies in that support and is deliberately
not subtracted when scoring the null. With retained latent coordinates u,v,
G3's exact score is u^2+v^2 and G4's is (u+8)^2+v^2.

Add two deterministic alternatives: G0 with mean shift e0 must fail support;
G3 with shift e0-e2 must fail support for every latent draw. For the latter,
`(e0-e2)^T y=2`, whereas it is zero throughout the null support. These
alternatives have no probability or finite-tolerance support test.

For each model independently, instantiate
`Generator(PCG64DXSM(SeedSequence(seed)))`, then make exactly one
`standard_normal(size=(trials,latent_columns),dtype=np.float64)` call, in C
row order. For G1/G2 the first eight columns are U8 and the last eight V8.
No warmup, shuffle, reroll, chunk-size substitution, implicit default generator
or process-parallel draw is allowed. Reject nonfinite draws. Convert each
returned binary64 coordinate exactly once with Fraction.from_float and perform
all surrogate linear maps, support tests, pseudoinverse quadratics and threshold
comparisons exactly as Fractions. Do not sample a fitted covariance via a
floating Cholesky/eigendecomposition or use `multivariate_normal`.

NumPy's [standard-normal API](https://numpy.org/doc/2.1/reference/random/generated/numpy.random.Generator.standard_normal.html)
specifies the shape and binary64 option. The
[PCG64DXSM documentation](https://numpy.org/doc/2.1/reference/random/bit_generators/pcg64dxsm.html)
describes seeded bit generation; the
[compatibility policy](https://numpy.org/doc/2.1/reference/random/compatibility.html)
requires the same call sequence, arguments, build and environment for matching
streams. A fixed integer stream does not establish that finite pseudorandom
floating values are mathematically independent exact Gaussians. The theorem
and probability budget below apply to the ideal Gaussian model. These finite
seeded runs are reproducible distributional diagnostics, not a proof of that
model or of its applicability to detector noise.

## 6. Sampling gates and prospective error budget

There are exactly four stochastic acceptance gates: three null tail-frequency
checks (G1,G2,G3), and the shifted-alternative power check G4. G0 and both
support alternatives are exact algebraic checks. Do not count individual draws
as independent theorem proofs or add post-hoc distribution tests.

For a null model with rank r in {2,8}, use threshold `q>2r`. Let K count
exceedances in B=32768 trials. The known ideal exceedance probability is

```text
p_r = exp(-r) * sum(k=0,...,r/2-1) r^k/k!
p_2 = exp(-2)
p_8 = (379/3) exp(-8).
```

This follows by integrating the chi-square density for even rank, or repeated
integration by parts of its integer-shape gamma density. There is no empirical
quantile fitting and no library distribution/quantile oracle.

Enclose these probabilities with exact rational arithmetic: for x in {2,8},
set `S=sum(k=0,...,128) x^k/k!` and
`R=(x^129/129!)/(1-x/130)`. Successive terms of the remaining positive
exponential series have ratio at most x/130, so
`S <= exp(x) <= S+R` and `1/(S+R) <= exp(-x) <= 1/S`.
Multiply by the stated positive rational tail polynomial. Require probability
interval width at most `2^-100`; otherwise refuse this oracle. Compare K/B
to **both** rational endpoints and require its maximum endpoint distance to
be at most `1/64`. Do not round the probability to binary64 or accept merely
because two intervals overlap.

For G4 use the same rank-two threshold q>4 and require K/B>=15/16.
Under the ideal alternative, failure q<=4 implies u<=-6. The one-sided
variance inequality gives P(u<=-6)<=1/37: on that event
`(u-1/6)^2 >= (37/6)^2`, while its expectation is 37/36.
Thus true power is at least 36/37 and exceeds the fixed gate by 21/592.
No noncentral-chi-square numerical oracle is needed.

The family error budget for mistakenly failing these four **correct ideal
models** is less than `1e-5`. For a Bernoulli mean, the exponential-moment
bound gives two-sided deviation probability at most `2 exp(-2 B d^2)`;
its one-sided form omits 2. One derivation bounds the second derivative of
the centered Bernoulli log moment-generating function by 1/4, integrates twice
from zero to obtain `log E exp(t(X-E X))<=t^2/8`, and optimizes the exponential
Markov bound. With probability-oracle width at most 2^-100, the union bound is

```text
6 exp(-2*32768*(1/64-2^-100)^2)
 + exp(-2*32768*(21/592)^2) < 1e-5.                         (2)
```

Independence between the four model runs is unnecessary for this union bound;
independent trials within each ideal model are required. The implementation
must verify the displayed inequality using outward rational exponential-series
bounds, not an unstated floating rounding assumption. It may use the sufficient
bound `1/64-2^-100 > 1/66`: evaluate an upper bound for
`6 exp(-65536/4356)+exp(-65536*(21/592)^2)` by the same positive-series/reciprocal
method through degree 128 (129 terms), with the same term-129 remainder, and
require it below 1/100000. All arguments remain positive and below 130, so the
geometric remainder denominator stays positive.

Equation (2) budgets false failures under the ideal simulation assumptions,
not false discovery in GW150914 and not a rigorous total-variation guarantee
for the NumPy sampler. No numerical sampler-to-Gaussian discrepancy bound is
claimed. A failed fixed-seed run remains a failed attempt; it does not authorize
new seeds, more trials, changed thresholds, a covariance correction or exclusion.

## 7. Numerical enclosures are not a noise model

A deterministic coefficient/output enclosure answers where the exact finite
arithmetic result lies. Sigma instead specifies variability across hypothetical
repeated raw-noise draws. Neither an enclosure width nor production/Decimal
agreement is a noise standard deviation, calibration posterior or confidence
interval. The exact Fraction synthetic maps introduce no additional rounding
in their algebra; the binary64 pseudorandom draw remains the sampled input.

For a later fixed-input calculation, let a verified error set E contain the
difference between the exact output and its rounded representation. Propagate
the residual set `(rounded_output-mu)+E` through the specified statistic.
If it misses range(Omega), support incompatibility is certified; if it meets
that range, bound the statistic on that intersection. A small floating
component outside a singular support is not automatically physical evidence.
A deterministic error tolerance is not permission to change the model's rank.

For a fixed PSD Omega with fixed rank, the elementary inequality

```text
| (z+e)^T Omega^+ (z+e) - z^T Omega^+ z |
 <= ||Omega^+||_2 * (2 ||z||_2 ||e||_2 + ||e||_2^2)
```

follows by expanding the quadratic and applying Cauchy-Schwarz. A future
application needs a proved bound on the inverse over its positive eigenspace,
a verified error set and separate support handling. Covariance uncertainty
requires an additional treatment; inserting an interval midpoint is not one.
RI-64's bounds are actual-input-specific and cannot be silently reused as a
uniform error guarantee for random synthetic draws or all possible data.

## 8. Implementation scope, replay and the next integration gate

After independent acceptance, reserve one small implementation/checker and one
combined deterministic result for sections 4–6, with an independently authored
exact expected-answer audit. Avoid separate report families for each model.
The implementation accepts no observational file path and no user-replacement
model, seed or threshold. Its source, this design and reused oracle bytes must
be pinned before execution. The reused oracle is 9484 bytes, SHA-256
`37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651`;
only its tiny exact operations are invoked.

Use the existing admitted CPython 3.11.6 / NumPy 2.1.3 environment and preserve
its full recorded platform/build/byte-order/NumPy configuration. SciPy 1.14.1,
h5py 3.12.1 and HDF5 1.12.2 may be recorded as inherited environment metadata;
no signal, distribution or HDF5 operation from them is needed. Install nothing.
Source checks and pure rational oracles use stdlib; sampling uses the explicitly
named NumPy API. Run copied sources normally and with `-O`, `-I -B`, serially,
outside the checkout. Require complete deterministic report and random-input
hash equality. Record launch mode, elapsed time and any stderr separately.

Retain exact model matrices/factors, rank/nullspace/pseudoinverse checks,
wrong-covariance refusals, probability intervals, every gate's count/denominator,
exact thresholds, error-budget bound, seeds and call shapes, complete initial
and final generator states, and SHA-256 of all latent binary64 values in fixed
little-endian C order. Also retain a canonical hash of all exact q values and
support decisions in model/trial order, with each value serialized as a
canonical Fraction string. Full latent or q arrays need not become repository
artifacts: independent replay must reproduce their full hashes. Report all
failed gates; never replace failure with an aggregate PASS.

Resource limits are fixed prospectively: 131328 generated trial rows total;
maximum latent dimension 16; maximum exact matrix dimension 16; numerator and
denominator limits of 32768 bits per intermediate Fraction; one worker;
1800 seconds and a sampled 2 GiB resident-memory watchdog per execution.
A watchdog is not a hard allocator cap. Resource failure is unresolved evidence,
not permission to simplify the model or adjust arithmetic. All validations must
remain active under `-O` and use explicit exceptions, not assertions.

The next admitted-operator integration is conditional and **not included in the
first implementation**. It would choose a fully specified finite synthetic
Sigma (a white-noise Sigma=I_T would be an assumption, not an estimate), reuse
the same sixteen certified adjoints, and enclose A Sigma A^T and all cross terms.
It must prove PSD/rank or positive pivots, control inversion and output-statistic
error, and distinguish a sampler using an approximate covariance from the exact
law. If a rank or accuracy condition is unresolved, it stops. No dense
131072-square covariance, full-filter basis enumeration, changed row/window,
new precision or assumption that interval midpoints are exact is authorized.
This gate prevents a toy sampling success from being reported as qualification
of the actual GWOSC operator's noise distribution.

## 9. Public-data and native prerequisites

Before scoring observations, freeze one conventional estimand, its mean/template,
timing, analysis band and support, conditioning, calibration convention,
noise/PSD estimation intervals, gaps/flags, nuisance treatment and selection
history. Qualify a version-compatible official detector response/waveform and
its time reference; do not infer those from the illustrative scalar NR overlay.
A suitable official longer/off-source product and quality metadata must be
located and qualified if the chosen noise estimator needs them. Their availability
has not been established by this design, and no new acquisition is authorized.

The [RI-40 calibration summaries](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
are pointwise statistical summaries, not a joint frequency/time/detector
covariance or simultaneous deterministic envelope. A calibrated inference needs
a defensible joint nuisance model or a clearly labeled conditional fixed-calibration
baseline. Respect the documented response-ratio orientation and frequency limits;
do not invent interpolation, Gaussian independence or waveform error bars.
Retain L1's NO_CW_HW_INJ-clear annotation and its qualification limits.

The [RI-53 reference comparison](../gwosc_nr_comparison_v1/COMPARISON.md)
uses a data-informed supplied scalar waveform, retained printed coordinates,
limited physical support and historical illustrative placement. A chosen interior
or a matching filter length resolves none of its timing, continuation, source
response or calibration obligations. A residual score requires an explicitly
reviewed comparison operator on compatible domains. Previously inspected
GW150914 samples are development data, not a blind holdout.

This document supplies no detector-noise validation, calibrated confidence
region, detection significance, gravity proof or DET-versus-GR result. The
native programme still needs a fixed law with a quantitative source/observer
forward map to this recorded observable and an identifiable discriminator that
survives conventional nuisance freedom. RET remains paused. No repository file
other than this new DESIGN.md is part of this author's reservation.
