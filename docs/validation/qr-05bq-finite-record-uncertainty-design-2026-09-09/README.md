# QR-05BQ: finite-record uncertainty contract

9 September 2026 (Pacific/Honolulu). **Analytical/design gate.** This sheet
derives a model-relative confidence construction and fixes a bounded successor
scope. No numerical study, engine, test suite, confidence-table computation,
source/capture freeze or physical acquisition is executed here. Displayed
fractions are analytical identities, not measured or simulated results.

## 1. Question and standalone model

Can finite paired causal records justify simultaneous population bounds,
then a set of relative-volume targets with a stated coverage guarantee?
The new ingredient is the uncertainty construction. Previously supplied
population boxes are not silently reinterpreted as confidence regions.

Use auxiliary null coordinates u,v, signature (+,−), marked regions
Q=(0,1)², I₁=(0,1/2)² and I₂=(0,3/4)×(0,1/2), with I₁⊂I₂⊂Q.
They correspond to supplied probes o=(0,0), m₁=(1/2,1/2),
m₂=(3/4,1/2), t=(1,1). For η∈{0,1}, s∈{1,4}, δ∈[0,2], let

```text
ds²=s(1+ηuv)du dv,        dμ=s(1+ηuv)du dv/2,
ρδ=1+δuv,                ν(R)=∫R ρδdμ / ∫Q ρδdμ,
τ=μ(I₁)/μ(Q)=(16+η)/[16(4+η)].
```

Density is scalar relative to proper volume. The targets are 1/4 (flat,
η=0) and 17/80 (conformal, η=1). The density premise is selected in advance
from [0,0], [0,1/2], [0,1], [0,2], named uniform, half, one, two. It must
contain the true δ for the target-coverage theorem below. This is not an
estimate of δ, a confidence assertion about a supplied bound, or an inferred
clock/coordinate system. Scale s cancels from normalized sampling.

For a rectangle (0,a)×(0,b), write z=ab. Integration gives

```text
M_R(δ)=∫Rρδdμ
      =(s/2)[z + (η+δ)z²/4 + ηδz³/9].
q_i(η,δ)=M_Ii(δ)/M_Q(δ),    z_Q=1, z_I1=1/4, z_I2=3/8.
```

The denominator is positive. Positive density and proper-volume measure on
the three nonempty category regions give 0<q₁<q₂<1. Since z²,z³≤z on
[0,1] and all coefficients are nonnegative, q₁≤1/4 and q₂≤3/8 throughout
this family. These upper bounds will give exact finite-record controls.

Fix n≥1 before acquisition. Each of n fresh iid points yields one paired
symbol Y_j=(1{X_j∈I₁},1{X_j∈I₂}). The same-point law is

```text
P(00)=1−q₂,   P(01)=q₂−q₁,   P(10)=0,   P(11)=q₁.
```

Different attempts are independent; questions within an attempt are not.
One hidden world is fixed for the entire batch. Fixed marks, causal-query
access, fresh iid sampling, no loss and correct pair/attempt association
are explicit acquisition premises. No ontology, alternative physical law,
quantum advantage or apparatus validation follows from adopting them.

## 2. Records, counts and the complete count law

Validate every paired attempt before summarizing. A 10 symbol cannot be
made legal by another 01 symbol: their aggregate counts can satisfy K₁≤K₂
while one input violates the stipulated channel. Refuse such a batch; do
not delete, relabel, resample or convert a missing attempt into a zero.

For a valid batch, K_i=Σ_jY_{ji} and 0≤K₁≤K₂≤n. The category counts are

```text
c00=n−K₂,   c01=K₂−K₁,   c11=K₁.
```

For any integers 0≤k₁≤k₂≤n, the count-pair probability is

```text
P(K₁=k₁,K₂=k₂)
 = n! / [(n−k₂)!(k₂−k₁)!k₁!]
   × (1−q₂)^(n−k₂) (q₂−q₁)^(k₂−k₁) q₁^k₁.
```

The multiplicity belongs to a count state, not an individual ordered word.
The multinomial expansion makes the complete count law sum to one. Given
a positive-probability count state, all its ordered words have equal
conditional probability independently of q. Thus the count pair is
sufficient for this fixed iid likelihood, but discarding attempt metadata
before checking the acquisition contract would discard audit information.

Each marginal K_i is Binomial(n,q_i). Their joint law is NOT the product
of those two binomial laws. In particular Cov(K₁,K₂)=n q₁(1−q₂)>0 in the
declared family. The coverage proof will not assume independence of counts.

## 3. Prespecified error budget and rational construction

Fix before seeing records a rational α with 0<α<1, four positive rational
allocations ε_i,L and ε_i,U with total at most α, and one finite rational
grid G={0=g₀<g₁<⋯<g_m=1}. The grid is computational rounding, not a claim
that the unknown population probabilities lie on it.

Define inclusive binomial tails for 0≤k≤n and p∈[0,1]:

```text
T⁺(k;p)=Σ_(r=k)^n C(n,r) p^r(1−p)^(n−r),
T⁻(k;p)=Σ_(r=0)^k C(n,r) p^r(1−p)^(n−r).
```

At p=0 or 1, use the degenerate binomial law explicitly. For observed k,
define the closed, outward-grid endpoints

```text
L_i(k)=max({0} ∪ {g∈G : T⁺(k;g)≤ε_i,L}),
U_i(k)=min({1} ∪ {g∈G : T⁻(k;g)≤ε_i,U}).
C(K)=[L₁(K₁),U₁(K₁)] × [L₂(K₂),U₂(K₂)].
```

Tail comparisons use ≤, tails include the observed count, and coverage
includes equality at an interval endpoint. Failure is q_i<L_i or q_i>U_i.
The defaults imply L_i(0)=0 and U_i(n)=1 because the corresponding tail
is identically one. Every grid evaluation and comparison is rational;
numerical root finding, floating tolerance and approximate quantiles are
unnecessary.

For 1≤k≤n, T⁺(k;p) is strictly increasing in p on (0,1); its derivative is
n C(n−1,k−1)p^(k−1)(1−p)^(n−k)>0. The lower exact root ℓ_i(k) of
T⁺(k;ℓ)=ε_i,L lies in (0,1). Similarly, for k<n the strictly decreasing
T⁻ has an exact root u_i(k). With ℓ_i(0)=0 and u_i(n)=1,

```text
L_i(k)=floor_G ℓ_i(k),    U_i(k)=ceil_G u_i(k).
```

Roots explain the construction but need not be computed. Rounding widens
the unrounded interval. The intervals do not reverse: if ℓ>u, a p strictly
between them would have both T⁺(k;p)<ε_i,L and T⁻(k;p)<ε_i,U, contradicting
T⁺(k;p)+T⁻(k;p)=1+P_p(K=k)≥1 and ε_i,L+ε_i,U<1. Boundary-count cases
already have lower zero or upper one. Refining a nested grid can only raise
L and lower U toward their exact roots; it cannot create additional data.

## 4. Continuous-parameter coverage proof

Fix an arbitrary true p∈[0,1], not necessarily a grid point. If p<L_i(K),
then K≥1 and the selected grid endpoint g=L_i(K)>p satisfies

```text
T⁺(K;p)<T⁺(K;g)≤ε_i,L.
```

For fixed p, counts with T⁺(k;p)<ε_i,L form either an empty set or an
upper tail {k*,…,n}. The probability of that set is T⁺(k*;p)<ε_i,L.
Consequently P_p(p<L_i(K))≤ε_i,L. At degenerate p=0 or 1, the only
positive-probability count respects the corresponding endpoint directly.

The symmetric argument uses p>U_i(K) and the decreasing lower-tail
function. Counts with T⁻(k;p)<ε_i,U form a lower tail; its probability
is less than ε_i,U. Hence P_p(p>U_i(K))≤ε_i,U.

Apply the union bound to these four failure events:

```text
P_(q₁,q₂)((q₁,q₂)∈C(K))
 ≥ 1−Σ_i(ε_i,L+ε_i,U) ≥ 1−α.
```

This is simultaneous coverage for every continuous nested pair
0≤q₁≤q₂≤1 under the fixed-n iid paired law. No independence between the
two questions and no penalty for the number of grid points is required.
The guarantee can be conservative; “exact arithmetic” does not mean actual
coverage is exactly 1−α or that the box is smallest possible. Intersecting
C with the known nested cone preserves the true pair on the same event.

## 5. Transfer from population coverage to geometric target sets

For the externally selected bound B, define feasible parameters and targets

```text
F_B(K)={(η,s,δ): η∈{0,1}, s∈{1,4}, δ∈B,
                   (q₁(η,δ),q₂(η,δ))∈C(K)},
T_B(K)={τ(η):(η,s,δ)∈F_B(K)}.
```

Use the SAME δ in both constraints. Since each M_R=A_R+B_Rδ and M_Q>0,
the four constraints are M_Ii−L_iM_Q≥0 and U_iM_Q−M_Ii≥0. Their exact
intersection with B is empty or a closed interval per labeled geometry.
Retain all nuisance intervals and their coupled forward laws. Targets are
the discrete subset of {17/80,1/4}, not the interval between them.

For every true θ=(η,s,δ) with δ∈B and the stipulated observation law,

```text
q(θ)∈C(K) ⇒ θ∈F_B(K) ⇒ τ(θ)∈T_B(K),
P_θ(τ(θ)∈T_B(K)) ≥ 1−α.
```

This is uniform model-relative frequentist coverage over the continuous
density domain. It is not a posterior probability that a realized answer
is correct. A false density bound or geometric/acquisition model invalidates
this target guarantee even if the interval routine is arithmetically correct.

For the mathematical probability statement, assign T=∅ on an impossible-10
refusal, while keeping that refusal operationally distinct from an ordinary
empty inverse. Such a symbol has probability zero under every admitted world.
Ordinary empty target sets are possible noncoverage events and must be counted,
not discarded. With only two possible target values,

```text
P_θ(T_B=∅) + P_θ(T_B is a wrong singleton) ≤ α.
```

If S is the event of reporting a singleton and P_θ(S)>0, only
P_θ(wrong | S)≤min(1,α/P_θ(S)) follows. It is not generally bounded by α.
Postselecting successful-looking outputs or repeating until a singleton
appears does not inherit the fixed-batch coverage theorem.

If a density-bound construction itself has a proved failure budget β,
a separate joint argument can give total failure at most α+β; independence
is not needed for that union bound. BQ does not supply such a construction.
Outcome-dependent bounds, marks, tail allocations, quotas or stopping rules
are outside the fixed-premise contract, unless separately justified.

## 6. Persistent indistinguishability

Flat δ=1 and conformal δ=0 have identical normalized point density
(4/5)(1+uv), hence the same paired law q=(17/80,21/64) for every quota.
Their geometric targets differ by 3/80. When B contains both density values
(the one/two premises), the single event q∈C includes BOTH parameter
witnesses. This particular common-box projection therefore satisfies

```text
P_common(T_B={17/80,1/4}) ≥ 1−α.
```

For an arbitrary uniformly covering target-set procedure, equal record
laws alone give the weaker bound 1−2α by a union bound on its two target
noncoverage events. The stronger bound here uses the shared population box,
not a general theorem about all confidence procedures. Neither statement
applies to this pair under a density premise excluding δ=1. Scale copies
remain identical in normalized law for every n; more records do not repair
these information obstructions.

## 7. Fixed four-record analytical controls

Select the minimal successor baseline n=4, α=1/20, all four ε=1/80 and
G={j/256:0≤j≤256}. This keeps the existing quota and asks about correctness,
not useful precision or experimental sample-size adequacy. The displayed
proof applies before any table or outcome census is evaluated.

**All 00.** For every world, the single ordered word (00,00,00,00) has
probability (1−q₂)^4≥(5/8)^4=625/4096>1/20. Any deterministic target-set
procedure with uniform 19/20 coverage must include both targets on that
word: excluding either would already exceed the failure allowance for a
world with that target. This force-on-one-word argument does not directly
extend to randomized reporting rules.

For the proposed interval construction K₁=K₂=0, so both lower endpoints
are zero. Since T⁻(0;3/8)=625/4096>1/80, both upper endpoints exceed 3/8.
Every declared geometry and every δ in its supplied bound survives. The
result is necessarily ambiguous, not a software failure or faulty sensor.

**All 11.** The grid contains 5/16=80/256 and
T⁺(4;5/16)=625/65536<1/80. Therefore the first lower endpoint is at least
5/16>q₁,max=1/4. The proposed inverse is empty for the allowed word
(11,11,11,11), under every density bound. Its probability is q₁^4>0 and
at most 1/256. This is a permissible rare noncoverage outcome, not a
logical contradiction or a diagnosis of which premise failed.

**Why selective confidence fails.** Consider a deliberately DIFFERENT rule:
report {17/80} only on all11, and both targets on every other allowed word.
For every conformal world its coverage is one. For every flat world its
coverage is 1−q₁^4≥255/256>19/20. Nevertheless, conditional on a singleton
under any flat world, the answer is wrong with probability one. This is
a counterexample within the same model family, not an output of the proposed
interval rule, which instead returns empty on all11.

## 8. Proposed executable successor: QR-05BR

BR is NOT implemented or executed by BQ. Before its first numerical work,
freeze its complete schemas, inputs, source/evidence inventory and resource
bounds. The selected prospective domain is:

- n=4, α=1/20, four ε=1/80; G={j/256}; inclusive tails, ≤ comparisons,
  closed intervals and outward rounding exactly as above. Do not tune these
  settings to produce a desired number of singleton answers.
- Five count-to-interval rows k=0,…,4. Retain both tails at all 257 grid
  points: 2,570 rational entries, shared by the two queries. Retain the
  selected and adjacent-grid inequalities certifying each nontrivial endpoint.
- All 15 nested count states, their multinomial exponents/multiplicities and
  simultaneous boxes. Four density bounds give 60 inverse cases and 240
  labeled geometry hypotheses, including both scale labels in each case.
- Six unit-scale validation fixtures: flat δ=0,1,16/11; conformal δ=0,1,45/158.
  They include the whole-point compensated pair and the distinct-law pair
  with common q₁=1/5. Keep all 90 fixture/count probabilities and 24
  fixture/bound summaries. Scale cancellation is an explicit algebraic
  comparison, not a doubled count-law table.
- Summaries retain population-box noncoverage, target noncoverage, empty,
  singleton and ambiguous probabilities with original count-law weights.
  Mark whether the true δ satisfies each supplied bound. Enforce target
  coverage only for in-premise combinations; retain out-of-premise results
  without calling them theorem failures or validated bounds.

These are planned inventories, not executed outcomes. Finite fixture checks
cannot prove uniform coverage; Section 4 supplies its continuous-domain
argument. The n=4 grid-tail comparisons can use integer numerators over
256⁴, comparing 80 times the numerator with 256⁴. An independent reference
can use Bernoulli convolution and cumulative sums. Tests can use the direct
n=4 tail polynomials, endpoint identities and the complete count law.
The population-to-target inverses should remain independently derived and
retain the shared-δ, zero-slope, closed-bound and scale checks.

The dyadic main-grid tail values cannot equal 1/80. Prespecify two separate
private-helper tie controls using ε=1/16: T⁺(4;1/2)=1/16 and
T⁻(0;1/2)=1/16. The respective grid endpoints must equal 1/2, not step
past an equality. These are helper tests, not a changed main error budget,
an extra main fixture family or an executed result in BQ.

The future record interface should own a new schema, not pretend to be BP's
external-population-box caller. Proposed entry point `infer_records` accepts
only protocol/schema/data-kind identifiers, four ordered attempt rows,
the density-bound name and its external-assumption basis. Each row carries
the fixed positional attempt ID and two native bits. Repeated bit patterns
are valid; duplicate/missing IDs or attempts and coercive types are not.
Validate every row before counting, and distinguish a well-shaped impossible
10 refusal from malformed input. IDs do not authenticate physical freshness,
independence, record integrity or correct acquisition.

Return counts, constructed intervals, the fixed quota/grid/tail-budget
certificate and the model-relative target/nuisance sets, or an explicit
refusal. Do not accept actual-world labels, coordinates, fitted confidence
levels, arbitrary frequency fields or generator seeds. Do not pass these
data-derived intervals to the old API under an `external_population_bounds`
tag. A new wrapper may use the same mathematical inverse with honest
confidence-construction provenance and its own source/evidence checks.

Negative controls include forbidden10 hidden by otherwise ordered aggregate
counts; quota/ID/type/schema defects; endpoint and equality conventions;
inward-rounding or marginal-independence substitutions; both analytical
four-record words above; and false density premises. Comparisons of paired
laws must retain their structural zero, not replace them with independent
Bernoulli questions. No particular singleton rate or smallest-interval claim
is an acceptance condition.

Retain the 262,144-byte source and 16,777,216-byte artifact caps, 30-second
analysis and 120-second suite limits, one cached analysis per suite, normal
and optimized suites/full replays and exactly one alternate-reference audit.
Use create-only frozen evidence and preserve failed attempts; no adaptive
scan, old engine/test rerun, exponential paired-word bank, dependency install,
timing-sensitive RET overlap, instrument access or external-data collection.

## 9. Claim boundary and lineage

This adds a mathematical finite-record uncertainty bridge under stated
premises. It does not establish that an instrument samples iid points, has
no loss, knows its marks, or satisfies a density bound. A declared confidence
level is a property of the procedure under its model, not an empirical
certification. More general density/metric families can have different
identification sets and need separate treatment.

The geometric forward family and continuous inverse continue the recorded
[BP specification](../qr-05bp-population-intervals-2026-09-09/README.md) and
[BP result](../qr-05bp-population-intervals-2026-09-09/RESULTS.md). The proof
and failure examples are provided above without requiring a DET ontology
or external statistical software. The [decision record](RESULTS.md) separates
analytical review from future execution. RET/applications, QM adapters,
apparatus calibration, Lean, clocks, general geometry and gravity dynamics
remain separately gated; book work stays archival. See the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
