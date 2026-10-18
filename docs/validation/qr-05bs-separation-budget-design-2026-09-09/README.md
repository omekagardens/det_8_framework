# QR-05BS: separation and acquisition-budget contract

9 September 2026 (Pacific/Honolulu). **Analytical/design gate.** This document
derives sufficient conditions for useful finite-record target identification
and fixes a bounded verification successor. No new confidence table, larger-
quota count law, engine, test suite, simulation or physical acquisition is
executed here. Displayed fractions and integer budgets are analytical
calculations, not numerical-study outcomes or minimum sample estimates.

## 1. Question and standalone model

When does a covering population box actually separate geometric targets?
Three distinct limitations must remain visible:

- Sampling uncertainty depends on the number and law of acquired records.
- Outward-grid rounding adds a computational enclosure, not information.
- Identical observation laws can leave different targets indistinguishable
  regardless of quota or numerical precision.

Keep auxiliary null coordinates u,v, signature (+,−), marked regions
Q=(0,1)², I₁=(0,1/2)² and I₂=(0,3/4)×(0,1/2). The supplied model is

```text
ds² = s(1+ηuv) du dv,       dμ = s(1+ηuv) du dv/2,
ρδ = 1+δuv,                η∈{0,1}, s∈{1,4}, δ∈[0,2].
```

The target is the relative proper volume
τ=μ(I₁)/μ(Q)=(16+η)/[16(4+η)], namely 1/4 or 17/80.
For z=ab and R=(0,a)×(0,b), integration gives

```text
M_R(δ) = (s/2)[z + (η+δ)z²/4 + ηδz³/9],
q_i(η,δ) = M_Ii(δ)/M_Q(δ),       z_Q=1, z_I1=1/4, z_I2=3/8.
```

The same point answers both nested questions. Its symbol probabilities in
order 00,01,10,11 are (1−q₂,q₂−q₁,0,q₁). All three allowed categories are
positive. Fix n fresh iid points before acquisition; counts satisfy
0≤K₁≤K₂≤n. Each marginal is binomial, but the two counts are dependent.

The external density premise B=[0,b] is one of uniform, half, one, two,
with b=0,1/2,1,2. It must contain the true δ. Marks, access, association,
iid/no-loss acquisition, the geometric family and this bound remain
supplied premises. This is not an ontology, a changed physical law,
a recovered metric or a calibrated acquisition procedure.

## 2. The continuous families are exact line segments

Cancel the common scale s. For either region product z,

```text
q_0,z(δ) = (1−t₀)z + t₀z²,                  t₀=δ/(4+δ),
q_1,z(δ) = (1−t₁)(4z+z²)/5
                      + t₁(9z²+4z³)/13,     t₁=13δ/(45+13δ).
```

Both t functions increase strictly with δ. Thus each set
C_η(B)={q(η,δ):δ∈B} is the WHOLE closed line segment between q(η,0)
and q(η,b), not a sampled approximation. For b=0 it is a single point.
The same mixing parameter applies to both coordinates.

The two supporting lines are

```text
flat:       16q₂ − 20q₁ = 1,
conformal:  7296q₂ − 9520q₁ = 371.
```

Their unique intersection is P=(17/80,21/64), attained by flat δ=1 and
conformal δ=0. At that pair the normalized whole-point densities are
also identical, (4/5)(1+uv); this is stronger than membership-pair equality.
Scale copies add no distinct normalized curve and are not opposite-target
competitors.

For a point p and an opposite-target segment, define

```text
d_η,B(p) = min_(δ'∈B) ||p − q(1−η,δ')||∞,
||(x₁,x₂)||∞ = max(|x₁|,|x₂|).
```

Compactness gives an attained minimum. For an in-premise true point
p=q(η,δ), the distance is zero precisely at an admitted compensated
intersection. A zero raw distance can also be computed for an out-of-premise
fixture; it must not be mistaken for a valid two-world inference premise.
For example flat δ=1 has distance zero to the conformal segment even when
a narrower B excludes the true flat density.

A distance between two selected fixtures generally exceeds the distance to
the entire competing segment. Using that larger gap as a certified lower
bound would overstate the available information.

## 3. Exact pointwise separation certificate

Write the opposite segment as a+t v, with a=q(1−η,0),
v=q(1−η,b)−a and 0≤t≤1. For b>0 both components of v are strictly negative.
Put r_i(t)=p_i−a_i−t v_i. The unique minimizing parameter is

```text
t* = clip_[0,1]((p₁+p₂−a₁−a₂)/(v₁+v₂)),
d  = max(|r₁(t*)|,|r₂(t*)|).
```

To see this, the two residuals increase strictly with t. Below their
opposite-sign balancing point, the negative residual of greatest magnitude
determines a decreasing maximum; above it, the positive residual of
greatest magnitude determines an increasing maximum. At the balance
r₁=−r₂. If it lies outside [0,1], the nearest endpoint is selected.
For b=0 do not divide by v₁+v₂: use the single endpoint and t*=0.

Retain the actual contact point, both signed residuals, d and whether the
unclipped balance lies before, at, inside or after the segment. Equality
at t=0 or 1 remains a closed contact, not a refusal. Recover the competing
density from endpoint-segment t by

```text
flat competitor:       δ' = 4bt/[4+b(1−t)],
conformal competitor:  δ' = 45bt/[45+13b(1−t)].
```

Both denominators are positive on the prescribed domain. All these values
are rational for rational p,b. Retaining δ' verifies that the nearest point
belongs to the allowed continuous family, rather than merely its
supporting line.

An independent finite construction evaluates t=0,1 and all in-range roots
of r₁=0, r₂=0, r₁−r₂=0 and r₁+r₂=0. Handle constant/identically-zero
equations separately. These roots partition the maximum of four affine
functions into linear pieces, so an endpoint of one of those pieces
attains the minimum. Deduplicate equal candidates but preserve equality
and endpoint classifications.

For an interior balance, a lower certificate is

```text
d = |v₂(p₁−a₁) − v₁(p₂−a₂)| / (|v₁|+|v₂|).
```

The numerator is constant along the supporting line, and the triangle
inequality bounds it by (|v₁|+|v₂|) times any residual sup norm. The retained
contact attains this bound. At a clipped endpoint, a signed coordinate
residual that is monotone away from that endpoint supplies the lower
certificate. Thus a contact witness proves attainability and a matching
lower certificate proves minimality.

A closed square centered at the TRUE point with radius r excludes the
opposite family exactly when r<d. At r=d it contains the contact witness.
This statement concerns a known center; it is not yet a finite-record
confidence guarantee.

For the two interior fixtures under B=[0,2], this distinction is concrete:

| True population point | Nearest opposite density | Exact distance to the whole opposite segment |
|---|---:|---:|
| Flat (1/5,5/16) | Conformal δ'=270/973 | 5/16816 |
| Conformal (1/5,2275/7296) | Flat δ'=16516/11261 | 5/16416 |

Both density witnesses lie strictly inside [0,2]. The contact residuals
have opposite signs and equal absolute value. For the first point, the
conformal-line residual is 5, divided by 9520+7296. For the second, the
flat-line residual is −5/456, divided by 20+16. Both directed distances are
smaller than the selected fixtures' vertical gap 5/7296. These are symbolic
derivations, not a new numerical fixture evaluation.

## 4. Whole-class separation and its failure

An operational quota cannot depend on an unknown true density. Define the
two-class margin under the externally justified common bound:

```text
D(B) = min_(δ,δ'∈B) ||q(0,δ)−q(1,δ')||∞.
```

For 0≤b<1, every flat point lies componentwise above P, while every conformal
point lies at or below P. The nearest pair is flat δ=b and conformal δ'=0.
Their first-coordinate gap is 3(1−b)/[20(4+b)] and their second-coordinate
gap is larger, 3(1−b)/[16(4+b)]. Therefore

```text
D([0,b]) = 3(1−b)/[16(4+b)]       for 0≤b<1,
D([0,b]) = 0                     for 1≤b≤2.
```

In particular D(uniform)=3/64 and D(half)=1/48. For one and two the
compensated pair is admitted, so no uniform positive margin exists.
Individual nonintersection points may still have positive margins.
A sequence approaching the intersection has margins tending to zero;
pointwise positive separation does not provide a common positive margin
on such a class.

For fixed n the paired count probabilities are continuous functions of q.
At the admitted intersection the common-box rule returns both targets with
probability at least 1−α. Consequently a uniform high correct-singleton
probability cannot hold on a class containing that pair, or uniformly on
a class with admissible points arbitrarily approaching it. Merely failing
a conservative sufficient budget elsewhere is NOT such an impossibility proof.

One may instead prespecify a restricted true-parameter class with a proved
positive infimum d₀ of its pointwise distances. The competing family must
remain the ENTIRE family allowed by the inference premise; restricting the
truth set for planning must not silently delete possible competitors.
No such additional class is selected or fitted to observed records here.

## 5. Confidence width without a count-table sweep

Keep total α=1/20 and all four one-sided allocations ε=1/80.
Fix positive integers n,m before acquisition. For a marginal count k and
uniform grid G={j/m:0≤j≤m}, h=1/m, define

```text
T⁺(k;p)=P_p(K≥k),          T⁻(k;p)=P_p(K≤k),
L(k)=max({0}∪{g∈G:T⁺(k;g)≤ε}),
U(k)=min({1}∪{g∈G:T⁻(k;g)≤ε}).
```

Use inclusive tails, closed intervals, outward rounding and explicit
degenerate p=0,1 laws. The defaults are L(0)=0 and U(n)=1.
Let ℓ(k),u(k) be the unrounded exact roots with the same defaults, and
let p̂=k/n. A standard independent bounded-sum inequality gives

```text
P_p(p̂−p≥a) ≤ exp(−2na²),
P_p(p−p̂≥a) ≤ exp(−2na²),       a≥0.
```

This is the Bernoulli specialization of Hoeffding's Theorem 1, inequality
(2.3), checked in the original paper's printed page 15. The theorem concerns
independence across attempts; it does not assume independence of the two
queries within an attempt. [Original paper](https://doi.org/10.1080/01621459.1963.10500830),
[readable primary-paper copy](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).

For completeness, a Bernoulli-specific derivation is short. The centered
log moment-generating function ψ has ψ(0)=ψ'(0)=0 and
ψ''(λ)=p_λ(1−p_λ)≤1/4, where p_λ is the tilted Bernoulli probability.
Integration yields ψ(λ)≤λ²/8. Independence and exponential Markov give
exp(−nλa+nλ²/8); λ=4a gives the bound. Apply the same argument to −λ
for the other tail. Degenerate Bernoulli variables satisfy the result directly.

Put r_n=sqrt(ln(80)/(2n)). If p̂−r_n>0, the inclusive upper tail at
p=p̂−r_n is at most ε, so monotonicity yields ℓ(k)≥p̂−r_n.
If the candidate is nonpositive, the bound follows from ℓ≥0.
The upper endpoint is symmetric, including defaults:

```text
ℓ(k) ≥ p̂−r_n,                 u(k) ≤ p̂+r_n,
L(k) ≥ p̂−r_n−h,              U(k) ≤ p̂+r_n+h,
U(k)−L(k) ≤ min(1, 2r_n+2h).
```

This is deterministic for EVERY count, not a second probabilistic event.
Each outward endpoint adds less than one grid step; 2h is a conservative
combined allowance. Inclusive root/grid ties are retained. The proof does
not require evaluating an n-dependent tail table or enumerating count pairs.

## 6. A sufficient correct-singleton theorem

Let C(K) be the product of the two count intervals. The
[BQ coverage proof](../qr-05bq-finite-record-uncertainty-design-2026-09-09/README.md)
gives P(E)≥1−α for E={q_true∈C(K)}, without query independence.
Assume the model/acquisition and true-density premises, and a certified
lower bound d≤d_η,B(q_true). If

```text
2 sqrt(ln(80)/(2n)) + 2h < d,
```

then on E every point in C is at sup-norm distance less than d from the
true point. The entire opposite-target segment is excluded, while the
true parameter and target are retained. Hence

```text
E ⇒ T_B(K)={τ_true},
P(correct singleton) ≥ 1−α.
```

The controlling quantity is the box's full maximum side width, not its
half-width. For a box centered at an estimated point, center error plus
radius matters; omitting the resulting factor of two is invalid.
Closed-boundary equality must not be treated as strict exclusion.
The deterministic width step consumes no additional failure budget.

This stronger premise also changes what may be said after selecting
singletons. Let a=P(correct singleton), w=P(wrong singleton). Then a≥1−α
and a+w≤1, so

```text
P(wrong | singleton) = 1−a/(a+w) ≤ 1−a ≤ α.
```

The conditioning event has probability at least 1−α>0. This stronger
conditional bound follows because the SAME coverage event forces a
CORRECT singleton. Ordinary target coverage alone gives only
min(1,α/P(singleton)); a separately established P(singleton)≥1−α gives
the weaker α/(1−α). Neither substitutes for the strict
separation/width premise.

BR's four-record counterexample remains intact: its baseline has no such
width certificate and its rare conformal singletons are all wrong.
Do not advertise the new theorem for that baseline, false bounds, a
misspecified acquisition law or a realized packet merely because it has
a singleton answer.

## 7. Exact conservative budget certificates

For d>2h, a sufficient real-valued condition is

```text
n > 2 ln(80) / (d−2h)².
```

This is a sufficient bound, not a necessary or minimum sample requirement.
There is no useful conclusion from this certificate when d≤2h; that
failure alone does not prove that the rounded procedure can never identify.

An entirely rational, slightly more conservative certificate avoids
floating logarithms. Positive terms in the exponential series give

```text
e⁵ > Σ_(j=0)^5 5ʲ/j! = 1097/12 > 80,       hence ln(80) < 5.
```

Therefore d>2h and n(d−2h)²≥10 imply the STRICT required width inequality.
Equality in this rational check is safe because ln(80)<5 is strict.
An equivalent sufficient witness form uses a nonnegative rational R:

```text
2nR²≥5,        2R+2h≤d        ⇒        r_n<R and width<d.
```

As one concrete prospective design, keep m=256 and select n=65,536 before
acquisition. Under the entire uniform and half classes, respectively,

```text
d=3/64:       d−2h=5/128,      n(d−2h)²=100,
d=1/48:       d−2h=5/384,      n(d−2h)²=100/9.
```

Both pass the sufficient threshold 10. Thus under either independently
justified narrow density premise the mathematical procedure has at least
95% correct-singleton probability throughout the supplied two-geometry
family, and the conditional singleton error bound above applies.
The quota is selected using a whole-class margin, not the hidden actual δ.

This does NOT say 65,536 records are necessary, that an instrument can
supply the required records, or that the density bound has been calibrated.
It is not an instruction to acquire or simulate that many records now.
No such count law or confidence table is executed by this design gate.
For one/two the uniform margin is zero; the same design cannot acquire
information absent from the normalized observation law.

A finer grid reduces a computational enclosure but cannot resolve an
exact zero distance. Conversely, increasing n with fixed h only removes
the sampling contribution from this particular width bound. It need not
meet a separation condition smaller than the remaining grid allowance.
Nested-grid refinement and quota increase are different operations.

## 8. Proposed bounded successor: QR-05BT

BT is NOT implemented or executed here. It should verify separation and
planning certificates, not run a 65,536-record experiment or a quadratic
count-state census. Fix complete schemas, sources and work limits before
its first mathematical evaluation.

Use BR's unchanged six unit-scale fixtures—flat δ=0,1,16/11 and conformal
δ=0,1,45/158—and the four existing bounds. The prospective domain is:

- 24 fixture/bound distance rows, retaining actual true-bound membership,
  the full opposite segment, exact minimizer/contact/density witness,
  signed residuals, distance and matching lower certificate. Retain
  out-of-premise and zero-distance rows; do not coerce them into successes.
- Four whole-class margin rows for uniform, half, one, two, with attaining
  pairs and the analytical global lower argument. Distinguish these
  margins from fixture-specific distances.
- One fixed planning pair n=65,536,m=256, α=1/20, ε=1/80. Retain the rational
  sufficient-condition result for each whole-class margin and each of the 24
  pointwise distances, with premise/certificate eligibility distinguished.
  A false sufficient condition means “not certified,” not “impossible.”
- Both scale-pair algebraic comparisons: normalized endpoints, distances
  and target sets are unchanged despite actual volume scaling. Do not
  expand the fixture likelihood bank.
- Read-authenticated stored BR intervals as a coarse baseline only.
  Retain their exact maximum side width and compare with each distance;
  do not rerun BR's engines, API, tests or original confidence table.

The primary route should use the clipped opposite-face balance. The
reference should build and compare the exact breakpoint candidates
independently. A third test route should certify forward contacts and
matching global lower bounds, not merely compare two reported decimals.
Every report value should use native exact rationals and complete
source-bound comparison before encoding.

Prespecified analytical controls must include the b=0 point segment;
closed contact at the admitted intersection; clipped versus interior
nearest points; the two directed margins smaller than the selected-fixture
gap above; full-width versus half-width; and a radius exactly equal to
distance admitting its contact. For each of those two interior/B=two rows,
use exactly three derived box controls: the square centered at p with
radius d/2 (excludes the opponent), the radius-d square (admits its contact),
and the coordinatewise bounding rectangle of p and its nearest contact.
The last has maximum side width d and half-width d/2<d, yet contains both
points. It refutes both a half-width substitution and non-strict width≤d
as sufficient exclusion rules. These six controls use fixed rows, not a
new world or probability scan.
The rational planning threshold may be tested at equality via the
symbolic witness form; its strict logarithmic slack must remain explicit.

Retain bounded sources≤262,144 bytes, artifacts≤16,777,216 bytes,
30-second analysis and 120-second suites; one cached analysis per suite,
normal/optimized suites and full replays, and exactly one alternate-
reference audit. Freeze new source identities before execution, authenticate
the stored BR baseline, use create-only evidence and preserve failures.
No adaptive budget/grid tuning, unbounded δ/grid sweep, paired-word bank,
large-quota tail/count computation, old engine/test rerun, dependency
installation, timing-sensitive RET overlap or physical acquisition.

The successor's planning result must not masquerade as a record-observer
output: actual fixture parameters are analytical design inputs, never
evidence about an unknown observed world. BR's public interface and frozen
results remain unchanged. No RET integration is implied.

## 9. Provenance and claim boundary

This gate continues the frozen
[BR result](../qr-05br-finite-record-confidence-2026-09-09/RESULTS.md)
and BQ's continuous-parameter coverage theorem. Its line-segment,
separation, width-transfer and budget arguments are analytical derivations
with independent review, not formal Lean proofs or new experimental tests.
The original concentration theorem was checked as primary literature;
the Bernoulli derivation above keeps the statistical premise explicit.

The [decision record](RESULTS.md) separates this completed design from
future execution. Useful target identification under a narrow model and
a justified density bound is not unique factorization of general geometry
and density, scale recovery, physical gravity or an ontological proof.
Acquisition calibration, general densities/metrics, dynamics, RET and
quantum adapters remain separately gated. Book work stays archival;
clocks, later gravity couplings and Lean installation remain deferred.
See the [research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
