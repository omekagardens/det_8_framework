# QR-05E results: observation-aware chain and propagation estimates

6 September 2026. **Bounded sampling-aware investigation completed.**
All 175 tests pass normally and under optimized Python. Two independent exact
implementations agree on every retained output, and the frozen capture replays
exactly without changing its bytes. RET/core sources and dependencies are unchanged.

## Main result

The order/propagation questions from QR-05D can be estimated from an induced
retained order using a declared sampling law. Correct weighting needs the joint
probability of retaining each chain's random vertices, not merely an average
retention rate. Exact mean correction does not imply single-sample reconstruction,
geometric identification, or predictive sufficiency for the quantum payload.

This is an application of established inverse-inclusion sampling mathematics,
not a new physical postulate. The contribution here is the exact finite evidence,
access contract, fixed-probe treatment, and retained counterexamples linking the
questions to QR-05D. See [Horvitz--Thompson (1952)](https://doi.org/10.1080/01621459.1952.10483446)
and [Klusowski--Wu, section 2.1](https://proceedings.mlr.press/v75/klusowski18a/klusowski18a.pdf).

For a fixed interval (a,b), let N_q count its q-internal-vertex chains. Let T be
the eligible, randomly retained vertices of one chain; fixed probes do not
receive a random-vertex factor. The operational estimator is

```text
H_q = sum over observed chains with pi(T)>0 of 1/pi(T),
pi(T) = probability that every vertex of T is retained.

E[H_q] = number of full-source chains with positive inclusion.
coefficient of z^q = (-1)^q H_q / (2^(q+1) rho^q),  z = mass².
```

The observer has retained IDs, their induced transitive order, the ID frame,
fixed probes, supplied density, and sampling law. Hidden relations, coordinates,
full targets and source/fixture names are not available to the estimator. The
primary implementation enumerates observed chains; the separate reference uses
full-source chain indicators as an audit oracle. These are scalar coefficients,
not CP maps or Born probabilities.

## Equal complete endpoint kernels, unequal sampling variability

The QR-05D Ferrers6 and standard-example S3 orders both have whole-interval
targets N=6 internal events and R=6 related pairs. Their entire complete
endpoint polynomials agree. Independent half-retention of their interiors gives:

| Quantity | Ferrers6 | S3 |
|---|---:|---:|
| Corrected mean N | 6 | 6 |
| Corrected mean R | 6 | 6 |
| Variance of corrected N | 6 | 6 |
| Covariance of corrected N and R | 12 | 12 |
| Variance of corrected R | 34 | 30 |
| Probability corrected R equals its target 6 in one sample | 0 | 0 |

The variance difference has a short explanation. There are eight unordered
pairs of relations sharing a vertex in Ferrers6, versus six in S3. With half
retention, the corrected R variance is 18 plus twice that overlap count.
Thus the response to observation can distinguish structure that the complete
endpoint polynomial misses. This is not a new geometric-embedding certificate.

The zero exact-hit probability is equally important: corrected R is four times
an integer and can never be six. Unbiasedness is an ensemble property, not a
promise that an individual retained sample gives the original answer.

## Knowing the mean retention rate is insufficient

Under alternating independent inclusion probabilities 1/3 and 2/3, multiplying
the actual vertex marginals is valid. Replacing them with the average rate 1/2
gives corrected mean R of 52/9 in Ferrers6 and 56/9 in S3, instead of six. Mean
N is still corrected to six, so a successful event-count check misses the error.

Under all-or-none loss, every nonempty vertex-set has joint inclusion 1/2.
The correct chain weight is two, irrespective of its number of random vertices.
Multiplying vertex marginals instead assigns weight four to a related pair:
mean R becomes 12 instead of six, and mean z² coefficient becomes 1/96 instead
of 1/192. One density rescaling cannot simultaneously repair all degrees.

The fixed mesh center illustrates another boundary. It survives by design and
must not be treated as randomly thinned. Under half-retention, incorrectly
doubling the entire observed count, including the fixed center, gives mean ten
rather than nine. This separate analytical wrong-all-vertices control is not
the implemented `uniform_rate` estimator: all implemented eligible-support
corrections keep the center unweighted and recover mean nine in this case.

## Missing support and nonidentifiability are different failures

Selecting exactly two eligible vertices supports every actual chain question in
the two-level Ferrers6/S3 orders. Their corrected N is constantly six. The exact
covariance includes negative contributions from pairs of chains that cannot be
jointly observed; these cancel to give Var(N)=Cov(N,R)=0, while Var(R)=54.

On the fixed-center mesh, the full whole-interval chain targets through degree
three are [1,9,27,37], but the supported targets are [1,9,27,13]. Exactly 24
three-eligible-vertex chains have zero inclusion. The other 13 degree-three
chains contain the fixed center: two with both eligible vertices before it,
nine straddling it, and two with both eligible vertices after it. Their supported
estimate has mean 13 and variance
195. All local-probe targets remain supported.

Those 24 terms are retained explicitly, not replaced, divided by zero, or
discarded from the evidence. This limits the chainwise estimator; it does not
prove that no other inference can recover the source. Repeated labeled pair
observations can in principle expose all its relations.

A separate control establishes a genuine identification obstruction. Under
singleton sampling, Ferrers6 and a six-interior-event total chain have exactly
the same observation law: bottom < chosen labeled vertex < top, each choice
with probability 1/6. Yet their full targets are [1,6,6,0] and [1,6,15,20].
Because source names are not observer information, no estimator of these
observations can be unbiased for both different full targets. Equality of the
observation laws persists for any fixed number of independent repetitions.

## The observation channel itself must be specified

Keeping the induced transitive order is not the same as retaining only original
Hasse links and then taking reachability. Removing intermediate link vertices
can erase a probe comparison that survives in the correct induced order.
For singleton observations of the total-chain control, the Hasse-only channel
loses the endpoint connection with probability one. The evidence retains every
sample's comparison flags and the first positive-probability failure.

This is a declared channel mismatch, not experimental noise. Similarly, the
QR-05D deterministic mesh bias, local-volume ambiguity and particular S3
embedding obstruction remain intact. Correcting sampling counts repairs none
of them. Prior record-location and delayed quantum-map counterexamples also
remain separate, pinned witnesses; no new quantum coupling was introduced.

## Evidence and verification

The [protocol](README.md) fixes all 17 cases before capture. The [artifact](results.json)
retains 2,048 mask rows, including 1,201 probability-zero rows; 847 rows have
positive probability. There are 108 questions, 615 source-chain terms, 73,728
estimator values, and 3,648 entries in each of the count- and coefficient-
covariance families. All arithmetic is rational; maximum retained component
size is 42 bits against a 4,096-bit guard. No Monte Carlo or experimental data.

- 142 mathematical/interface/aggregate tests plus 33 capture lifecycle tests:
  **175 passed in 11.36 s normally and 11.38 s optimized**. Optimized pytest emits
  its expected assertion-rewriting warning; executable validation uses exceptions.
- Ruff checks and formatting pass. Strict native-JSON and canonical-byte
  comparisons distinguish Booleans from integers and reject tuple coercion.
- All complete primary/reference analyses agree. Tests independently reconstruct
  sampling laws, chains, estimates, means, biases, centered covariance matrices,
  covariance identities, coefficient transforms and positive semidefiniteness.
- The complete aggregate round trip passed before create-only capture. Six
  source files and nine prior artifacts are byte-bound, including both QR-05D
  versions. Twelve endpoint questions and six local coefficients reproduce
  QR-05D's pinned targets without importing prior executors.
- Capture: 6,400,976 bytes; SHA-256
  `362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41`.
  Suite runtime 3.32335 s; exact read-only replay 3.34805 s. These are local
  suite timings, not application performance claims.
- A separate JSON-only audit, importing no executors, passed 98,415 checks:
  it recomputed every observed sample and all 68 method-specific moment/covariance
  families, verified all source/support inventories and the independent covariance
  identity, and checked the six source/nine prior hashes, target bridges and totals.
  All 91,001 rational-string occurrences are canonical, with maximum 42-bit
  components. Audit check counts are execution evidence, not additional test cases.

Before freeze, tests corrected a test-only mesh hand count from nine to 13 and
required the native-type guard to run before serialization. Both corrections
preceded capture; no frozen source or result required replacement.

## Value for the calculus and the next gate

The useful additional object is an explicit observation law attached to an
order-based question. A summary now needs its target, access contract, inclusion
support and covariance—not just a corrected scalar value. This supports future
calibration contracts, loss-model stress tests and formal verification of the
finite expectation/covariance identities. It does not establish unknown geometry,
quantum-field dynamics, a continuum limit or gravity.

**Proposed next gate: QR-05F, two-stage observation consistency.** Compare direct
final observation with sequential thinning of the same supplied finite orders.
Specify the joint and conditional observation laws and whether intermediate
records are retained. Test conditional expectation/composition and support
boundaries, preserving failures when the intermediate record or conditional
inclusion information is discarded. This is a new finite protocol to be frozen
before execution, not a result of QR-05E. Keep the QR-06 RET quantum adapter
under its separate SDK/calibration gates; no adapter or apparatus integration
is needed to begin this mathematical question.

In that next protocol, distinguish observation-law composition from direct
final-sample weighting and intermediate-record-aware sequential weighting.
Conditional support may fail even when final inclusion is positive. Conversely,
losing an intermediate record does not automatically prevent unbiased estimation
from the final sample; it can instead make only a particular sequential estimate
unavailable. QR-05F must test these distinctions, not presume their equivalence.
