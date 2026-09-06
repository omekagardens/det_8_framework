# QR-05I results: analytic portability

6 September 2026. **Completed bounded investigative gate.**
This is an exact classical observation-law result on supplied finite orders,
not a derivation of gravity or a quantum model.

## Outcome

The calculus now describes the complete two-color independent sampling family,
not only selected rates. The joint four-count law is represented by exact
integer polynomial coefficients on the whole square [0,1]^2. Two independent
routes agree: observed-order binomial expansion and full-source chain-set
evaluation followed by exact rational tensor interpolation.

The color-graded chain tensor D is precisely the coefficient tensor of all
four mean polynomials. It preserves every mean in this family, but it does
not preserve every full distribution. Color-preserving, fixed-marked order
does preserve the full law. Fixed-versus-eligible status and the named color
marks remain necessary acquisition metadata, not inferred geometry.

| Representation | Classes | All-rate means | All-rate joint count law |
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

Every row also retains the same public current design, density, fixed/eligible
frame and final observed order. Each number describes a supported finite
partition, not bytes, a universal statistic, or a recursively closed state.

The exact question partitions have 2,596 mean classes and 2,634 full-law
classes. Their members match H's menu-mean and menu-count partitions,
respectively; the full-law partition also matches H's selected colored-IID
count partition. Both refinement directions and first collisions were checked
against all eight H targets. These are actual membership equalities, not an
inference from equal numbers of classes.

Thus the H menu happened to distinguish every all-rate distinction present
in this fixture universe. It is not a general certificate: the retained
abstract two-atom counterexample agrees at both H IID rates and all four
corners but differs elsewhere, within the same bidegree bound. It is explicitly
not claimed to be an induced-order count law in this universe.

## What is established mathematically

For an observation S containing O odd and E even eligible vertices,

```text
P_z(x,y) = Σ_{U:N(U)=z} x^o(1-x)^(O-o)y^e(1-y)^(E-e).
M_q(x,y) = Σ_z z_q P_z(x,y) = Σ_{o,e} D[q,o,e]x^o y^e.
```

The [protocol](README.md) gives the finite-sum arguments for normalization,
nonnegativity on the square, degree bounds, means, coefficient uniqueness
and the correlated corner mixture. These arguments are general within
their stated finite-observation premises; the execution validates their
implementation on the declared fixtures. They are not Lean-checked proofs.

Each atom has bidegree at most (O,E), at most (3,3) here. Consequently the
16 exact grid values at {0,1/3,2/3,1}² determine its coefficients. The
one-variable interpolation identity is standard, with the tensor extension
proved explicitly in the protocol; see
[NIST DLMF, Lagrange interpolation](https://dlmf.nist.gov/3.3.i).
Signed monomial coefficients are valid: positivity follows from the
nonnegative subset construction, not from the signs of those coefficients.

H's shared-block law is the average of the four deterministic corner laws.
It is not the independent half-rate law. D determines those deterministic
corner count vectors and therefore this particular block mixture, but no
arbitrary correlated law is inferred.

All attainable atoms remain in the coefficient representation. They are
positive throughout the open square; they may disappear on boundary faces.
This does not establish fine-record transport support at a boundary.
The distinct fine/coarse transport contracts remain pinned H evidence.

## Retained failures and controls

- Equal marked singleton orders can have mean N1 equal to x or y. Color
  information cannot be discarded when the rates may differ.
- Two antichains have the same half-rate count law but block probability
  P(N1=1) equal to 0 versus 1/2. Equal marginals do not specify dependence.
- The star and path observations have identical D and all mean polynomials,
  but different count polynomials. Their N2 variances are 15/16 versus 13/16
  at half rates and 68/81 versus 52/81 at the colored setting. Their block
  count laws remain identical.
- Two odd eligible vertices retain the N1=1 atom symbolically even though its
  probability vanishes at x=0, x=1 and under shared-block sampling.
- The fixed interior vertex3 contributes a constant count, never an x factor.
  An absent color introduces no polynomial dependence on its rate.
- The abstract normalized PMFs (1/2,1/2) and
  (1/2+h/4,1/2-h/4), h=x(1-x)(2y-1)(3y-2), agree at all selected H points
  and corners. At (1/2,1/3), they give (1/2,1/2) and (25/48,23/48).
- The out-of-degree diagnostic x(x-1/3)(x-2/3)(x-1) vanishes on the
  interpolation grid but equals 1/144 at x=1/2. The degree premise matters.

Both synthetic diagnostics are marked as algebraic, not additional
realizable poset fixtures or counterexamples found in the supported histories.
All order-based collision controls retain their positive-history IDs.

## Scope and evidence

| Quantity | Retained total |
|---|---:|
| Cases / intermediate states | 10 / 608 |
| First-stage-positive states | 510 |
| Current histories | 6,804 |
| Positive / zero joint histories | 3,534 / 3,270 |
| Potential repeat observations | 6,804 |
| Joint-law polynomial atoms | 2,979 |
| Integer atom-coefficient cells | 47,664 |
| Mean-coefficient cells | 38,912 |
| Distinct driver audit points per state | 22 |
| State/point checks | 13,376 |
| Coefficientwise normalization checks | 9,728 |
| Deterministic corner checks | 2,432 |
| Candidate/target assessments | 24 |
| H/I target pairs checked in both directions | 16 |
| H policy predictions matched | 1,824 |
| Malformed runner fixtures rejected by both routes | 19 |
| Maximum absolute atom coefficient | 54 |
| Largest retained exact component | 59 bits |

All 12 H candidate partitions and all current history identities match.
H's count laws and count/coefficient means are reconstructed from the
polynomials. Its 1,824 labeled probability vectors are independently checked
from the supplied policies, not inferred from coarse count polynomials.
All 13 earlier artifact hashes remain pinned. Pooled masses sum to 10 because
ten per-case probability models are retained; no source prior is invented.

Independent tests also use nonnegative Bernstein multiplicities, an additional
off-grid rational point, all nine interior/edge/corner support strata, strict
native/subclass rejection, exact partition reconstruction and tamper controls.
Capture lifecycle tests use only temporary stub evidence.

Validation passed:

- 134 tests normally (46.17s) and 134 with `-O` (46.29s).
  Optimized pytest reports its standard warning about non-test assertions;
  the executors and runner use explicit checks, and subprocess tests exercise
  optimized rejection paths without relying on assertions.
- Ruff check and format verification passed.
- Create-only capture: 11,671,159 bytes; measured suite time 21.464642333s.
- Exact unchanged replay: normal 23.352126375s, optimized 23.309501125s.
- Independent read-only JSON postflight rechecked all 13,376 state/point
  evaluations, coefficient identities, all 14 candidate/target partitions,
  all 32 H/I refinement directions, and every source/prior hash.

Artifact SHA-256:
`9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798`.

During test development, the pinned-H fixture initially applied the exact-math
type guard to descriptive runtime metadata. That test-only error was corrected
before the final successful runs and source freeze; no prior artifact changed.
Runtime measurements are descriptive, not application-performance evidence.

The evidence bundle is [results.json](results.json); the capture and replay
entry point is [study.py](study.py). The six frozen source identities and
13 prior identities are recorded inside the artifact. The human report and
bridge roadmap are outside that ledger. No retained artifact was overwritten.

## Value and next gate

This supplies a precise reusable contract for rate-dependent count prediction,
summary selection and checks against acquisition-law changes. It provides a
small formalization target without requiring DET ontology. Application runtime
benefit, measured uncertainty calibration and production integration are not
tested. RET/core and the separate QR-06 adapter were not changed.

**Proposed next: QR-05J, constructive uncertainty-summary contract.** Count
ordered pairs of chains by the color composition of their eligible union.
That directly yields all raw second-moment polynomials and, with D, all
covariances. Compare this summary with the full-law oracle from I, retain
the star/path distinction and test correlated-mixture handling. Raw second
moments retain a 4×4 coefficient frame, while covariance subtraction can
require 7×7: the mean product can reach degree six. Pair self-overlap,
ordered-pair multiplicity and shared fixed versus sampled vertices must
remain explicit.

This would explain the information needed for uncertainty questions without
claiming prediction stronger than I's full law or assuming strict compression.
It is proposed, not executed here. Dynamic closure needs a separately declared
update/access contract. Physical interpretation still needs an observable
interface, units, acquisition model and empirical validation protocol.
No quantum channel, metric, gravity dynamics, continuum limit or new physical
law is established. Lean remains uninstalled. Remote publication stays deferred.
