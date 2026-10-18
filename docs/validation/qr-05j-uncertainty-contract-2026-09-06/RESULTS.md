# QR-05J results: constructive uncertainty summary

6 September 2026. **Completed bounded investigative gate.**
The prior QR-05I checkpoint and six earlier pending commits were pushed to
origin/ret before this work began. This gate is isolated mathematical research.

## Outcome

Eligible-support overlap between chains provides a direct, exact summary for
all means and covariances in the declared two-color IID sampling family.
The primary route counts ordered chain pairs and never constructs the full
count distribution. The independent reference derives the same results from
full-law polynomials. Their complete native outputs agree.

This answers what additional structure is needed beyond mean predictions:
which chains share sampled vertices, including self-pairs and multiplicity.
It does not strengthen QR-05I's full-distribution prediction claim, because
a complete law already determines its moments.

The color-graded single-chain tensor preserves all mean polynomials but
loses uncertainty information. The new pair-union tensor preserves both.
Its 2,634 supported classes coincide with I's 2,634 full-law classes by
actual memberships, not just equal class counts. Means retain 2,596 classes.
A separate valid abstract-law counterexample preserves first and second
moments while changing the distribution, so the finite coincidence must
not be promoted to a general theorem.

| Candidate | Classes | All-rate means | All-rate means and covariance |
|---|---:|:---:|:---:|
| Final record | 407 | No | No |
| Policy token | 521 | No | No |
| Tagged policy | 703 | No | No |
| Counts + token | 1,688 | No | No |
| Support grading + token | 1,706 | No | No |
| Tagged support grading | 2,041 | No | No |
| Boundary-anchored unmarked order | 2,023 | No | No |
| Fixed-marked order | 2,040 | No | No |
| Full intermediate record | 3,379 | Yes | Yes |
| Color-graded chains | 2,596 | Yes | No |
| Anonymous block-marked order | 2,720 | No | No |
| Named color-marked order | 2,966 | Yes | Yes |
| Eligible-union-graded ordered chain pairs | 2,634 | Yes | Yes |

Each candidate also retains public current design, density, fixed/eligible
frame and final observed order. Hidden source-profile labels stay out of
keys. These are supported prediction partitions, not bit costs or recursive
state representations. No performance advantage or strict compression
relative to the full-law partition was demonstrated.

## Constructive contract

Let N_q be the number of q-internal-vertex chains between fixed probes,
q=0..3, with N_0=1. Only eligible vertices are independently sampled.
An eligible odd vertex survives with rate x and an even vertex with rate y.
For each ordered pair of chains A,B, count the eligible odd/even vertices
in the union of their supports. Let B[q,r,o,e] be that pair count and
D[q,o,e] the single-chain grading. Then

```text
M_q(x,y)  = E N_q       = Σ D[q,o,e] x^o y^e
R_qr(x,y) = E[N_q N_r]  = Σ B[q,r,o,e] x^o y^e
K_qr(x,y) = Cov(N_q,N_r) = R_qr(x,y) - M_q(x,y) M_r(x,y).
```

The product of two chain-survival indicators is the survival indicator of
their eligible union. Shared random vertices are therefore counted once,
while both orientations of a distinct ordered pair remain present.
Chains with identical eligible supports must retain their multiplicity.
Shared fixed vertices introduce no random factor.

B[0,r]=D[r], so the complete pair tensor already includes the means. Equality
of B is equivalent to equality of all raw-second-moment polynomials and
therefore of means together with covariances. This is a coefficient identity,
not a grid approximation; the [protocol](README.md) gives its proof arguments.

Raw second moments have bidegree at most (3,3) here, but covariance subtraction
requires the complete mean-product convolution. A single three-vertex odd
chain gives R_33=x³ and K_33=x³−x⁶. The 7×7 covariance tables retain those
degree-six terms; total degree never exceeds q+r.

Evaluated covariance is positive semidefinite because every quadratic form
is the variance of a linear combination. It need not be positive definite:
the N0 row/column is always zero. This is the standard covariance identity;
see the [University of Iowa STAT7400 notes](https://homepage.stat.uiowa.edu/~luke/classes/STAT7400-2021/_book/numerical-linear-algebra.html#cholesky-factorization).
Signed polynomial coefficient matrices themselves need not be positive
semidefinite. No fitting, regularization, matrix inverse or Gaussian premise
is used.

## Retained controls and failures

- A singleton has raw second moment x and variance x−x². Treating a self-pair
  as independent would erase the variance.
- Two odd incomparable eligible vertices give R_11=2x+2x². Omitting one
  off-diagonal orientation gives the wrong deterministic raw moment 3 instead
  of 4 at x=1.
- The star and path have identical means but different covariances. Their
  N2 variance difference is exactly 2x(1−x)y², including 1/8 at half rates
  and 16/81 at the colored setting. The previously retained variances
  15/16 versus 13/16 and 68/81 versus 52/81 are recovered.
- A shared-root star gives R_22=2xy+2xy² and
  K_22=2xy+2xy²−4x²y². Its two distinct cross-pairs share their odd root;
  a product that samples the root twice is incorrect.
- The fixed interior vertex 3 contributes deterministically. With only it
  retained, N1=1 and variance is zero; with eligible 6 present, the N1/N2
  raw cross-moment is 2y and covariance is y−y².
- Odd and even triple-chain controls realize the x⁶ and y⁶ covariance terms.
- An edge need not be deterministic: at x=0,y=1/2 the shared-root example
  still has Var(N1)=1/2, while N2 is zero.
- Abstract laws A(n=0,2)=(1/2,1/2) and
  B(n=0,1,3)=(1/3,1/2,1/6), on vectors (1,n,0,0), share every first/second
  moment but have third moments 4 versus 5. They are explicitly not claimed
  to be realizable induced-order IID laws in this gate.

All realized controls carry positive current-history IDs in the artifact.
The abstract moment alias is kept separate from those histories.

## Correlated sampling: center after mixing

The shared-block policy is the equal mixture of four deterministic corner
laws. Its covariance includes variation between their count vectors:

```text
m = average_c z_c
R = average_c z_c z_c^T
K = R - m m^T = average_c (z_c-m)(z_c-m)^T.
```

Each corner has zero conditional covariance. Averaging those zero matrices
alone is wrong. Two odd incomparable vertices have block Var(N1)=1, compared
with independent-half Var(N1)=1/2. For the shared-root example:

| Law | Var(N1) | Cov(N1,N2) | Var(N2) |
|---|---:|---:|---:|
| Independent half rates | 3/4 | 1/2 | 1/2 |
| Shared parity blocks | 5/4 | 3/4 | 3/4 |

The single-chain tensor D already determines each corner's deterministic
count vector and hence this block law. The pair tensor supplies an independently
constructive IID uncertainty description; it is not stronger block prediction.
No arbitrary correlation structure or unknown acquisition law is inferred.

## Evidence and verification

| Quantity | Total |
|---|---:|
| Cases / intermediate states | 10 / 608 |
| First-stage-positive states | 510 |
| Current histories | 6,804 |
| Positive / zero joint histories | 3,534 / 3,270 |
| Potential repeat observations | 6,804 |
| Ordered chain-pair instances | 47,828 |
| Pair coefficient cells | 155,648 |
| Covariance coefficient cells | 476,672 |
| Mean coefficient cells | 38,912 |
| Evaluated policy predictions | 1,824 |
| State/point checks | 13,376 |
| Covariance matrices checked for semidefiniteness | 13,984 |
| Exact principal minors checked | 97,888 |
| Deterministic corner checks | 2,432 |
| Candidate/target assessments | 26 |
| I/J target pairs compared in both directions | 4 |
| Maximum pair / absolute covariance coefficient | 108 / 144 |
| Largest retained exact component | 59 bits |

All 12 original I candidate partitions and complete current-history identities
match. Every raw-moment coefficient matches the corresponding moment of the
pinned I full-law coefficients. All 14 preceding artifact hashes remain fixed.
Ten per-case probability models are retained, so pooled mass is 10, not a source
or acquisition-policy prior.

Validation passed:

- 142 tests normally (89.86s) and 142 with `-O` (89.96s).
  Optimized pytest emits its standard non-test-assertion warning; executors
  and runner use explicit checks, and subprocess tests verify optimized
  invalid-input rejection without relying on assertions.
- Ruff check and format verification passed.
- Create-only capture: 16,334,160 bytes; suite time 33.760235542s.
- Exact unchanged replay: normal 35.055461375s, optimized 34.925798916s.
- Independent JSON-only postflight rechecked all 155,648 raw-moment cells
  against I, all 476,672 covariance convolution cells, all 1,824 policy
  covariance matrices and scalings, all 15 partitions, all eight prior-target
  refinement directions, and all source/prior hashes.

Artifact SHA-256:
`dc8f80f40861107dd7a5ee378c9813a90c1981a3c2e7e14ee343163e9d88c333`.

The 19 malformed runner fixtures are rejected by both routes. Tests include
strict native/subclass rejection, early tensor and prior-identity tampering,
and invalid covariance matrices that pass diagonal or two-by-two checks but
fail the three-by-three principal determinant. Valid singular matrices remain
accepted. Lifecycle mutations use temporary stub evidence only.
Runtime measurements are descriptive, not application benchmarks.

Evidence: [results.json](results.json), with six frozen source identities
and 14 prior identities. The entry point is [study.py](study.py).
No artifact was overwritten or normalized after capture. Human reports and
the roadmap are outside the frozen source ledger.

## Applicable value and next gate

This gives a direct mathematical uncertainty contract for finite record/order
counts under a declared acquisition law. It identifies sampling-induced
covariance that equal averages miss, including shared-selection effects.
It is a useful compact formalization target without requiring DET ontology.
The current dense tensor is not claimed to be a storage or runtime improvement.

Measured applications still require apparatus noise, model mismatch, units,
observables and calibration to be specified independently. No empirical error
bar, RET integration, quantum fluctuation, metric or gravity dynamics follows
from this gate. RET/core sources and unrelated checkout changes were untouched.

**Proposed next: QR-05K, recursive observation-summary closure.** Define a
subset-closed observed-state universe with public fixed/eligible marks and
fresh independent two-color thinning at each step. Separate three claims:
fine-record rate composition; closed expected D/B updates; and the stronger
existence of a well-defined transition law for the next realized summary,
given only the current summary. Compare complete polynomial transition
pushforwards across summary fibers before claiming a Markov quotient.

If a quotient exists in the declared finite family, check its inherited
composition law. Preserve mean-summary failures, between-record covariance,
boundary support and the distinction from a deterministic update using a
labeled retained mask. The new state domain must include valid successor states,
not just the prior positive-history subset, and must not smuggle hidden source
labels into keys. No result for pair-summary closure is prescribed here.
This would be observation-update consistency, not event-growth or spacetime
dynamics. It is proposed only; Lean and the physical interface remain separate.
