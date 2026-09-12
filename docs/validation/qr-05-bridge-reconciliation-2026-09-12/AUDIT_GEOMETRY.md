# Selective geometry and operator audit of the concurrent QR-05 branch

12 September 2026. Reviewed source: `qr-05-bridge` commit
`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`. All GitHub citations below are pinned
to that commit, not to the moving branch. The authoritative working checkout
remains `ret`.

## Decision and scope

There is useful work to retain: finite causal-order counterexamples, the
longest-chain premetric, a corrected max-plus construction, supplied-geometry
estimator fixtures, observational factorization, and the directed-distance
correction. The branch's stronger statements about closure of the mixed
reconstruction program, uniform convergence, and completed operator compatibility
must not be inherited from passing gate labels.

This was a **selective audit**, not an execution or line-by-line certification of
all gates CF–DD. It combined substantial static review of CY–DD, selective
operator/geometry review across CF–CR, primary-source checks for the imported
LGH/LIS mathematics, three bounded suite reruns, and small explicit diagnostic
calculations. The branch was inspected in an isolated archive. The original
branch sources, captures and freezes were not edited or overwritten.

| Execution in the audit archive | Result | Elapsed suite time |
|---|---|---|
| QR-05DC `test_qr05dc.py` | 13 tests passed | 3.042 s |
| QR-05CR `test_qr05cr.py` | 8 tests passed | 0.024 s |
| QR-05CY `test_qr05cy.py` | 11 tests passed | 0.136 s |

These runs used `python3 -B` and process alarms below 60 seconds. They include
the suites' stored-report comparison checks, but are not substitutes for the
separate whole-branch source-identity inventory. DD's full large study was **not**
rerun. Its normalization checks below use the existing committed report plus
small helper probes. No empirical data, new physical operator or gravity claim
is established by this audit.

Severity below concerns whether a result can safely be adopted: **P1** blocks the
stated mathematical promotion; **P2** requires correction or sharper scope before
reuse. A passing suite can coexist with either kind of error when the assertions
repeat the same mistaken claim as the implementation.

## 1. DC: link closure does not characterize every superadditive reconstruction

**P1.** DC states that every A2-compliant reconstruction equals the max-plus
closure of its own link weights, then uses this characterization to constrain the
mixed order/count program. The claim is false. See the
[characterization in DC README, lines 39–46](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dc-max-plus-closure-2026-09-11/README.md#L39-L46).

Take a three-event chain `0 ≺ 1 ≺ 2` with distances

```text
D(0,1) = 1,  D(1,2) = 1,  D(0,2) = 3,
```

and zero on all other pairs. It has exactly the required causal support and
satisfies the reverse triangle because `3 ≥ 1+1`. Its link-only closure assigns
`2` to `(0,2)`, not `3`. Both DC implementations reproduced zero reverse-triangle
violations for D, link-only closure `2`, and all-pair closure `3`.

The corrected useful statement is:

> For a finite strict partial order and nonnegative weights on all causal pairs,
> the maximum chain-weight sum is the least superadditive majorant of those
> weights. Positive causal-pair weights give exact positive causal support.

The proof is elementary. Concatenating maximizing chains proves
superadditivity. Any superadditive majorant bounds each chain's total weight, so
it bounds their maximum. In particular, a superadditive D is the closure of its
**full causal-pair weight matrix**. Restricting that matrix to links loses
information in general. The corrected all-pair statement does not assert
uniqueness of a physically preferred weight rule or convergence to a continuum.

### DC's uniform-bound conclusion also exceeds its data

**P1.** The report hardcodes
`mixed_uniform_bound_reduces_to_order_only = True`; the surrounding verdict says
the closure distortion equals the chain distortion for every tested weight.
See [DC primary, lines 326–367](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dc-max-plus-closure-2026-09-11/primary.py#L326-L367).

Its own census contradicts equality. For `n=64, seed=1`, the chain distortion is
`0.6903`, whereas closure at weight `a=0.75` is `0.6027` and at `a=0` is `0.5551`.
The last case fails link positivity, but the positive-weight example already
disproves the equality claim. See [DC table, lines 65–72](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dc-max-plus-closure-2026-09-11/README.md#L65-L72).

What survives is much narrower: on six selected sprinkled objects, none of the
five tested weight choices beats the particular plain count estimator. That
finite sweep neither eliminates other mixed constructions nor reduces their
uniform-convergence question to the longest-chain estimator. Pointwise
domination alone does not order minimax approximation errors; DC's own later
discussion acknowledges this, while the opening module commentary still makes
the invalid transfer.

**Prospective repair:** retain the all-pair closure construction, add the
three-chain regression, distinguish measured comparisons from universal claims,
and leave the mixed reconstruction family open. Recompute any proposed new
comparison under a prospectively fixed weight family and error definition.

## 2. DD: distinguish the theorem's quantity, the reported statistic and convergence

### 2.1 Different normalizations are treated as the same measurement

**P1.** DD defines

```text
U = inf over c>0 of max over causal pairs |L - c tau|,
delta = ell U,
ell = sqrt(AREA/n).
```

The factorization `delta=ell U` is correct for the stated infimum. However, the
implementation computes `ell` and then reports and fits `U/mean_L` instead.
See [DD primary, lines 179–200](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dd-order-only-uniform-bound-2026-09-11/primary.py#L179-L200).

From its committed capture at `n=128, seed=0`:

| Quantity | Value |
|---|---|
| `ell * ceiling_links`, the declared delta | `0.3179130556875` |
| `ceiling_norm`, the reported normalized statistic | `0.892557983` |
| `ell * mean_L`, the factor relating the two | `0.356181964375` |

The reduction test checks only
`ceiling_links = ceiling_norm * mean_L`, which follows from the normalization
definition. It does not test the theorem's `delta=ell U`. See
[DD test, lines 145–149](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dd-order-only-uniform-bound-2026-09-11/test_qr05dd.py#L145-L149).

The distinction matters to the negative control. The declared layered family has
`L≤2`, hence its unnormalized quantity satisfies `delta≤2ell→0` by letting the
relative scale tend to zero. DD instead labels the control nonvanishing using
`U/mean_L>0.5` at one size, `n=300`. A normalized noncollapse diagnostic and the
stated unnormalized infimum are not interchangeable. The discrepancy is not
evidence that the normalized diagnostic is useless; it is evidence that the
object being tested must be named and its relation to the theorem justified.

**Prospective repair:** report `U`, `ell`, `mean_L`, `ell U` and `U/mean_L`
separately. Decide which normalized comparison is intended. Any asymptotic bridge
between them requires an explicit condition on `ell*mean_L`. State a
noncollapse/normalization convention before making control or convergence claims.

### 2.2 The numerical fit does not establish a uniform vanishing theorem

**P1.** The flag `order_only_uniform_bound_vanishes` is set from a positive fitted
exponent and `R²>0.9`. Other flags declare a power law, consistency with the LPP
exponent and no plateau using finite thresholds. See
[DD primary, lines 206–212](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dd-order-only-uniform-bound-2026-09-11/primary.py#L206-L212).
The decision record then supersedes DA's “convergence not established” on the
basis of five sizes and three seeds. See
[DD RESULTS, lines 49–63](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dd-order-only-uniform-bound-2026-09-11/RESULTS.md#L49-L63).

A decreasing finite sequence and a good log–log fit do not exclude a later
plateau or establish an asymptotic law. The study does retain a false
`unconditional_proof_established` flag and some bounded-numerics caveats; those
caveats should govern the verdict too, rather than coexist with a “vanishes”
promotion.

The imported result also needs a separate uniformity argument. Baik, Deift and
Johansson establish a centered/scaled longest-increasing-subsequence distribution
for random permutations. That is not, by itself, DD's maximum over all sampled
intervals after scale optimization. Tail control, simultaneous coverage across
intervals and treatment of small/near-null intervals are additional obligations.
See the [BDJ original paper](https://arxiv.org/abs/math/9810105).

As a diagnostic calculated from the already stored rows, fitting the seed means
of the **declared** `ell U` gives exponent approximately `0.26617`, rather than
the published `0.274` for `U/mean_L`. This is a change of statistic, not a repaired
convergence result. Neither fit is an asymptotic proof.

**Prospective repair:** keep the result as a selected finite-range trend; replace
asymptotic success flags with descriptive statistics; predeclare uncertainty and
competing-trend checks; and state the uniform concentration theorem actually
needed. A numerical trend need not be discarded just because it is not a proof.

### 2.3 Strict light-cone ties need a boundary regression

**P2 for generalized reuse.** The fast pair enumerators sort by `u=t-x` without
excluding equal-u groups. The small probe `[(0,0),(0.5,0.5)]` returned
`lengths=[1], taus=[0.0]`, although the points are null related, not strictly
chronologically ordered. See
[DD primary pair enumeration](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05dd-order-only-uniform-bound-2026-09-11/primary.py#L66-L104).
This does not establish contamination of the fixed random capture. It does block
using the helper as a general exact implementation of strict two-coordinate
dominance without a tie policy.

The Fenwick and segment-tree implementations are useful independent chain
mechanics. They do not independently validate their shared quantity definition,
control interpretation or statistical promotion logic.

## 3. CU–CZ: an LGH comparison is not a trimmed mean or a bijection problem

### 3.1 A trimmed mean is not a supremum upper bound

**P1 for the upper-bound claim.** CU defines its error as the maximum of two mean
errors restricted to selected timelike pairs, then calls it a correspondence/LGH
upper bound. Large errors at excluded or rare pairs can be invisible to that
statistic. See [CU README, lines 15–27](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cu-lgh-distance-2026-09-10/README.md#L15-L27).

It can be retained as a trimmed average reconstruction error. It cannot be
relabeled a bound on a full supremum without an additional argument covering
every omitted pair and the continuum coverage defect.

### 3.2 General correspondences can beat every bijection

**P1 for promotion to the full LGH infimum.** CW/CX and CZ use bijections between
two finite event sets. CZ's corrected scale-free formula still has this
restriction. See [CZ README, lines 50–57](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cz-scale-free-lgh-2026-09-10/README.md#L50-L57).

Minguzzi–Suhr define distortion using a supremum over a relation that is onto
both spaces, not necessarily the graph of a bijection. Their bounded Lorentzian
metric spaces also require distinction of points, in addition to the conditional
reverse-triangle and topological conditions. See definitions 1.1, 4.1 and 4.3 in
the [primary publication](https://link.springer.com/article/10.1007/s11005-024-01813-z).

An explicit distinguishing finite-space counterexample shows why the restriction
matters. Let all unlisted distances be zero:

```text
X: d(0,2)=1, d(1,2)=1.1.
Y: d(0,1)=1, d(0,2)=1.1.
R={(0,0),(1,0),(2,1),(2,2)}.
```

Both spaces distinguish their three points. With the discrete topology the
continuity/compactness requirements hold, and there are no two-step positive
chains on which the conditional reverse triangle could fail. R is onto both
spaces and has distortion `0.1`. Exhaustion of the six bijections gave best
distortion `1`. Thus even equal finite cardinalities do not justify replacing
general correspondences by bijections.

A lower bound proved only for the bijection problem is not automatically a lower
bound for the broader correspondence infimum. The discrete-to-continuum problem
also needs coverage beyond a comparison of two matrices on the same finite
sample. Prospective work should either keep the finite bijection diagnostic
explicitly named, or implement the appropriate correspondence and coverage
problem with its hypotheses.

### 3.3 CZ's directed-distance correction is useful

The correction from symmetric `sqrt(dt²-dx²)` to the future-directed separation
is a real improvement. Comparing a directed chain matrix with a symmetric
continuum matrix adds reverse-direction errors by construction. CZ explicitly
withdraws that contaminated obstruction. Retain the support-mismatch regression
and the corrected convention; do not inherit the withdrawn CW/CX floor. See
[CZ convention analysis](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cz-scale-free-lgh-2026-09-10/README.md#L13-L48).

## 4. CR: the selected conservative operator has a different moment coefficient

**P2.** CR usefully distinguishes the pointwise form from the divergence form,
then selects the latter as conservative. However, its exact coefficient audit
uses only the pointwise kernel. See
[CR primary, lines 48–69](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cr-no-double-counting-2026-09-10/primary.py#L48-L69)
and the [combined success predicate, lines 81–104](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cr-no-double-counting-2026-09-10/primary.py#L81-L104).

For the pointwise operator `d_k(f_{k+1}-2f_k+f_{k-1})`, the second moment divided
by two in unit-link coordinates is exactly `d_k`. For the divergence operator
the neighbor weights are `(d_k+d_{k+1})/2` and `(d_k+d_{k-1})/2`, so that coefficient
is instead

```text
(2*d_k+d_{k+1}+d_{k-1})/4.
```

The executed probe `d=[1,2,1], k=0` gives `1.25` for the actual divergence moment,
while the audit reports `1`. The same conceptual mismatch occurs in the reference
route. The selected form therefore does not have the claimed exact finite-grid
coefficient identity. See its [selection and conclusion](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cr-no-double-counting-2026-09-10/RESULTS.md#L3-L28).

What survives: both forms annihilate constants; the divergence form telescopes
to zero when summed around the periodic grid; the pointwise form generally does
not conserve that unweighted sum. These are useful operator properties, not
proofs of physical source absence or a unique geometry-to-dynamics coupling.

**Prospective repair:** compute the first and second moments of the actual
selected divergence kernel; distinguish finite-grid identity from a smooth-limit
approximation; state the measure with respect to which conservation is intended.
No repaired divergence-operator study has been executed in this reconciliation.

## 5. DB: preserve the obstruction under explicit fixed-function assumptions

DB's elementary finite witnesses are useful. On a three-chain, `sqrt(1+m)` gives
link distances `1,1` and endpoint distance `sqrt(2)`, violating the reverse
triangle. Raw `sqrt(m)` assigns zero to links. Longest-chain length, by contrast,
has exact positive causal support and obeys the reverse triangle because chains
concatenate. See [DB witnesses and proof setup](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05db-count-reconstruction-obstruction-2026-09-11/RESULTS.md#L29-L52).

The broader count-only proof needs tightening. Its Claim B establishes a lower
bound along a subsequence and then asserts a full liminf bound without the
needed additional step. Claim C uses informal count scaling as though it were
already a global asymptotic theorem for g. See
[DB RESULTS, lines 54–72](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05db-count-reconstruction-obstruction-2026-09-11/RESULTS.md#L54-L72).

A simpler corrected argument preserves a useful conditional impossibility:

1. Fix one density-independent function `g:N_0→[0,infinity)` with `g(0)>0`.
   Use `d_rho(i,j)=rho^(-1/d)*g(m_ij)`, with spacetime dimension `d≥2`.
2. Require the reverse triangle on all finite pure chains, of arbitrarily large
   size. This implies `g(x+y+1)≥g(x)+g(y)` for nonnegative integers x,y.
3. Taking `y=0` and iterating gives `g(m)≥(m+1)g(0)` for **every** m.
4. For a fixed positive-volume timelike interval, suppose its count satisfies
   `m_rho/rho→V>0` in probability, as in the stated homogeneous sampling model.
   Then
   `rho^(-1/d)*g(m_rho) ≥ g(0)*rho^(1-1/d)*(m_rho/rho+1/rho)`,
   which diverges in probability. It cannot converge to a finite nonzero
   Lorentzian separation.

This argument does not need to infer an asymptotic formula for g. Its scope is
essential: a fixed count-only g, positive link weight, the specified density
normalization, and axioms on all pure chains. It does not rule out arbitrary
density-dependent rules, general all-pair order/count functionals, approximate
axioms or different admissible classes. The corrected proof is analytical audit
work, not a claim that all DB code or mathematical generalizations were repaired.

## 6. CY and the earlier chord: useful structures with narrow interpretations

### Observational quotient and anchor

CY's elementary factorization criterion is sound: a target can be recovered from
a deterministic channel exactly when it is constant on that channel's fibers.
A deterministic postprocessing of the same channel cannot distinguish an
equal-observation/different-target witness pair.

Its positive examples distinguish a small **fixed-seed catalog**. Dimension
worlds use one sample per dimension; conformal-count worlds use one sample per
parameter. That is not a statistical identification or error guarantee over all
sampling outcomes. The added scale anchor is literally the target c appended
to the observation. It is a transparent perfect-information example, not
calibration evidence. See [CY world construction, lines 127–170](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cy-observational-quotient-2026-09-10/primary.py#L127-L170).

The no-go applies relative to the declared channel and world class; it does not
establish that every conceivable internally generated observable or every BW
reference has the same information restriction. CY's broader wording should not
be promoted. See [CY report propositions and verdict](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cy-observational-quotient-2026-09-10/primary.py#L293-L315).
The local [common-world calculus](CALCULUS.md) retains the scoped finite-set
principle and explicitly marks injected anchor information.

### Supplied geometry and chosen operators

- **CF/CJ/CK:** retain supplied-geometry dimension, order and normalized count
  profile fixtures as estimator checks. They do not establish manifold emergence
  or eliminate sampling-density versus metric-factor ambiguity outside the
  generating assumptions. [CF scope](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cf-t7-supplied-geometry-2026-09-10/README.md#L13-L43).
- **CL/CM:** retain finite-difference and kernel-moment checks. In CM the compared
  coefficients are `2hV` and `h²D`; they depend on h and vanish at different rates.
  A nontrivial fixed drift-diffusion generator needs a scaling prescription, not
  just agreement with that h-dependent Taylor expression.
  [CM defining expressions](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cm-t5-drift-diffusion-2026-09-10/README.md#L13-L31).
- **CN–CP:** the shared-input density/KDE/coefficient constructions are useful
  compatibility examples. They use supplied coordinates, chosen bandwidths and
  chosen operator forms. A high correlation of two profile estimates is not a
  derivation of a unique kernel from causal order/count, nor a proof that the
  profiles are exactly proportional. [CN witness](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cn-t7-t5-bridge-2026-09-10/README.md#L51-L67).
- **CQ:** retain the lesson that a non-manifoldlike order can fool an
  ordering-fraction-only screen. Adding a link-fraction check rejects the selected
  bipartite control, but passing two summaries is not a manifoldlikeness theorem.
  [CQ diagnostic boundaries](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05cq-adversarial-control-2026-09-10/README.md#L46-L61).

These are candidates for selective future verification, not declarations that
the unexecuted gates have all passed this audit.

## 7. Integration boundary and next work

The reconciliation adopts a corrected finite common-world measurement-channel
calculus and named regression lessons. It does not transplant the concurrent
branch's geometry engines, promote its gate-completion labels, or claim to have
fixed all issues above. The local exact tests are separate evidence from the
three archived suites rerun here.

Useful next geometry work can proceed under supplied geometry, but should first
fix its mathematical contract: directed separation and strict ties; all-pair
versus link weights; the exact normalized error; general correspondence versus
finite bijection scope; and the actual operator whose moments are being checked.
Convergence, calibration and empirical applicability remain distinct obligations.

The recommended stance is neither wholesale rejection nor wholesale adoption:
reuse the explicit constructions and counterexamples, repair their premises and
claims prospectively, and require independent verification of the particular
result being advanced.
