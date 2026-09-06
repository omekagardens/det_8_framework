# QR-05K results: recursive observation-summary closure

6 September 2026. **Completed bounded investigative gate.**
Isolated mathematical research after the committed/pushed QR-05J checkpoint.

## Outcome

The pair-overlap summary B supports an exact stochastic update kernel on this
finite observed-state family. The mean summary D does not. Both still have
simple exact expected-feature updates. Knowing how a summary updates on
average is therefore weaker than knowing the distribution of its next value.

The independent observed-chain/binomial and source-count-law/interpolation
routes agree on their complete native outputs. The successful quotient kernels
compose under fresh independent two-color thinning at every pair of rates,
not merely the selected audit rates.

| Present summary | Classes | Expected feature updates | Full next-summary law |
|---|---:|:---:|:---:|
| Color-graded chains D | 88 | Yes | No |
| Eligible-union chain pairs B | 91 | Yes | Yes, on this domain |
| Fixed-anchored color-marked order | 118 | — | Yes |
| Complete labeled observed record | 188 | — | Yes |

Actual memberships give a strict refinement chain from full record through
color-marked order and B to D. Class counts are not storage costs: the dense
pair tensor is not claimed to be a smaller or faster implementation.

## What changed from J

This is a new, subset-closed domain for an observation-update question:
four source orders, two public fixed/eligible frames, 224 source/mask aliases
and 188 unique labeled observations. Every induced successor is included.
Source aliases identify provenance in the evidence, not a sampling prior.

Compressed summary keys retain the public frame but omit the hidden source, old acquisition
design/token, intermediate labeled mask and earlier final record. A summary-only
observer predicts its next summary's law, not the exact successor associated
with a specified labeled mask.

All 224 aliases and all 608 J state occurrences match their previous observed
orders, colors, counts, D/B tensors and color-order codes. This includes 98
zero-first-mass occurrences. J's supported-history partitions remain untouched;
their class counts must not be compared as though they used this new domain.

## Mathematical contract

For an observed S with O eligible odd and E eligible even vertices, an induced
successor U with o/e such vertices has probability

```text
P_(x,y)(S,U) = x^o (1-x)^(O-o) y^e (1-y)^(E-e).
```

All fixed vertices remain. Transition polynomials have bidegree at most(3,3).
Every structurally attainable atom is retained, including selected-rate zeros.
Each row sums coefficientwise to one.

Indicator survival gives the two diagonal expected updates

```text
E[D_qoe(U) | S] = x^o y^e D_qoe(S)
E[B_qroe(U) | S] = x^o y^e B_qroe(S).
```

But stochastic closure requires the stronger identity: every S,S' in a
current summary class must have the same complete polynomial row after
successors are grouped by their next summary. Failed partitions receive a
collision witness and no quotient kernel.

This is a finite Markov-chain aggregation question, not a novel physical law.
For standard background on exact aggregation see
[Buchholz, Journal of Applied Probability 31(1), 1994](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/exact-and-ordinary-lumpability-in-finite-markov-chains/2DC748F09D80BEEB03CCF18036E149D7).
The gate's specific premises and proof arguments are in the [protocol](README.md).

Fresh independent stages satisfy

```text
P_(x,y) P_(a,b) = P_(xa,yb).
```

Each vertex survives both decisions with the product rate. A closed summary
inherits composition by lifting class functions to fine observations.
Executors additionally check all 256 four-variable coefficient cells per
reachable source/target pair. The independent runner checks the equivalent
matrix identities A_ij A_kl = 0 for unequal exponent pairs, and A_ij otherwise.

Thus the passing finite quotients can be iterated for any finite sequence of
declared fresh independent stages. The computational certificate is finite;
the extension to repeated composition is the elementary induction argument.
No adaptive policy, correlated-stage law, event birth or physical-time dynamics
is asserted. Repeating the same parameter pair can produce degree-six
expressions; a two-variable four-node grid alone would not certify that case.

## Retained failures and controls

The selected Ferrers star mask57 and path mask27 have identical D. Their
probabilities of reaching the D class of mask41 are respectively

```text
star: x(1-x)y²
path: 0
```

At half rates this is 1/16 versus0. This realized next-summary failure is kept
separately from the automatically first collision: states39/54, current D
class21, successor class5, with x²y(1-y) versus0. Equal expected D updates
do not repair either failure.

B, color-marked order and full record pass all fiber comparisons. Every
frame has one fixed-only absorbing state (IDs0 and156). All four corners
are deterministic; boundary edges need not be. At(1,1) the fine kernel
is identity, while(0,0) gives the frame's fixed-only record.

A reused Bernoulli-half coin gives two-stage singleton retention1/2,
whereas two fresh independent half coins give1/4. The reused-coin diagnostic
violates the independence premise; it is not a failure of the declared theorem.

## Uncertainty through another observation

Every one of188 states is checked at four ordered stage-rate pairs, retaining
752 complete covariance-tower rows:

```text
Cov(final counts | S)
  = E[ Cov(final counts | U) | S ]
  + Cov( E[final counts | U] | S ).
```

The first term is within-intermediate-record uncertainty; the second is
between-record variation. Their sum equals direct product-rate covariance,
and the conditional means agree as well. For an odd singleton under two
half-rate stages:

```text
final variance 3/16 = within 1/8 + between 1/16.
```

All rows preserve the zero N0 covariance direction and deterministic fixed
contributions. No positive-definiteness requirement, inversion, regularization,
Gaussian model or empirical noise calibration is introduced.

## Evidence and verification

| Quantity | Total |
|---|---:|
| Frames / profiles / aliases / unique states | 2 / 4 / 224 / 188 |
| Fine transition atoms | 2,300 |
| State/summary transition atoms | 7,059 |
| Fine plus pushed coefficient cells | 149,744 |
| D / B feature cells | 12,032 / 48,128 |
| Expected-update coefficient cells | 962,560 |
| Closed quotient atoms | 4,400 |
| Quotient two-hop structural paths | 23,949 |
| Four-variable composition cells | 1,126,400 |
| Rational audit points per row | 22 |
| Evaluated fine/pushed atoms | 205,898 |
| Evaluated quotient atoms | 96,800 |
| Deterministic state/corner rows | 752 |
| Covariance tower rows | 752 |
| Prior aliases / state occurrences matched | 224 / 608 |
| Largest retained exact component | 59 bits |

Validation passed:

- 96 tests normally (36.46s) and 96 with `-O` (36.62s).
  Optimized pytest emits its standard warning about non-test assertions;
  executor/runner checks are explicit, and optimized subprocess tests
  verify valid output equality and invalid-input rejection without assertions.
- Ruff check and format verification passed.
- Create-only capture: 1,900,466 bytes; suite time 8.957642374996794s.
- Exact unchanged replay: normal 9.191843583015725s,
  optimized 9.218982791993767s.
- Independent JSON-only postflight: 2,546,155 explicit checks in 4.67s,
  with no executor, runner or test imports. It rechecked the state/alias
  domain, observed D/B/color codes, all fine/pushed rows, every closure
  fiber and first failure, 962,560 expected-update cells, all 1,126,400
  four-variable composition cells, all 752 tower rows and all 608 J
  correspondences. Source/prior ledgers and artifact bytes were unchanged.

Artifact SHA-256:
`46d93f643c443b75ef425349cff11d7f3c437a79921e7e1ee94610998bd1a501`.

The test route independently reconstructs the finite states, induced-subset
outcomes, features, polynomial pushforwards, closure witnesses, composition
and tower rows. Mutation controls reject fabricated quotients for failed D,
altered coefficients/certificates, a consistent but noncanonical state-ID
permutation, boolean-for-integer substitutions and changed source identity.
The runner retains 19 malformed-input fixtures rejected by both executors;
additional subclass and optimized assertion-free guards are tested.

All six source identities and all 15 prior artifact identities are frozen.
Lifecycle mutation tests use temporary stub evidence only. The canonical
[results.json](results.json) was created once by exclusive creation and never
overwritten. Replays are read-only; reports and this roadmap update are outside
the source ledger. Runtime measurements are descriptive, not benchmarks.

## Applicable value and next gate

This supplies a concrete criterion for deciding when a summary can be reused
after another observation without silently losing predictive distinctions.
It links exact count uncertainty to recursive stochastic state reduction.
The useful structure is the declared observation kernel and its compatible
summary partition; no DET ontology is needed.

For Track B, this is a prerequisite-style consistency test for a proposed
coarse description, not evidence that its classes are geometry or that thinning
is gravitational evolution. Physical observables, apparatus noise, units,
calibration and a dynamical correspondence still need separate definitions.
No RET integration, quantum channel, metric, continuum limit or gravity is
claimed. RET/core and unrelated checkout files were untouched.

**Proposed next: QR-05L, adversarial closure and stable refinement.**
Challenge the finite-family B success without changing its observation law:
append two height-two orders on the same six eligible IDs, plus all their
induced observations.

```text
P6 internal relations:
  1<2, 1<4, 3<4, 3<6, 5<6
C4 + K2 internal relations:
  1<4, 1<6, 3<4, 3<6, 2<5
```

A design-review calculation predicts equal B: both have three vertices of
each color, five mixed edges and color-wise degree multiset[2,2,1].
Only the second can yield the four-cycle successor on{1,3,4,6}, with probability
x²(1-x)y²(1-y): at half rates, C4+K2 gives 1/64 and P6 gives 0. This is a prespecified
adversarial extension, **not part of the K captured domain or certificate**.

Freeze and verify that extension separately, preserve K as an exact restriction,
then iteratively refine B classes by their complete polynomial transition rows
until stable. The intended repair is the coarsest strongly closed refinement
of B on the declared expanded finite domain, if independently verified—not
another moment tensor, a universal minimal-memory theorem or a physical law.
Lean and the apparatus/RET interface remain separate gates.
