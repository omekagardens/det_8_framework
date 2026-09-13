# QR-05: directed correspondence, scale and noncollapse

12 September 2026 (Pacific/Honolulu). **Analytical design only.** No new
mathematical executor, fixture enumeration, test suite, simulation or data
acquisition runs in this gate. The census in section 8 is prospective, not
measured. See the [decision record](RESULTS.md).

This standalone calculus requires no DET ontology. It follows the
[measure/divergence verification](../qr-05-measure-divergence-verification-2026-09-12/RESULTS.md)
and repairs the correspondence, closure and normalization problems identified
in the [concurrent-branch geometry audit](../qr-05-bridge-reconciliation-2026-09-12/AUDIT_GEOMETRY.md).
It defines a comparison layer, not gravitational field equations or an
empirical reconstruction of spacetime.

## 1. Objects, conventions and mathematical source

An input is a nonempty finite set X with a supplied kernel
d_X:X×X→[0,∞), with d_X(x,x)=0. The comparison construction works on this
whole class. Separately record whether the kernel is an admissible directed
separation: its positive support is a strict order and it obeys the
conditional reverse triangle inequality

`d(x,z) ≥ d(x,y)+d(y,z) whenever d(x,y)>0 and d(y,z)>0`.

Record point distinction separately: distinct points must have different
complete outgoing OR incoming distance profiles. Zero separation does not
mean equality of events; spacelike and null pairs can both have zero directed
separation. A symmetric positive two-point kernel is allowed only as an
explicitly invalid-causal comparison control, not a Lorentzian model.

The argument order is source then target: d(x,y) means x→y. Matrices here
have source rows and target columns. This is the transpose of the receiving-row
convention used in the earlier causal-operator gate. A comparison kernel is
not |Q|, |G|, a graph Laplacian, or a distance inferred merely from an order.
Its values and units are additional inputs.

The onto-correspondence and supremum-distortion conventions follow
[Minguzzi and Suhr, *Lorentzian metric spaces and their Gromov–Hausdorff convergence*,
Definitions 4.1, 4.3 and 4.6](https://link.springer.com/article/10.1007/s11005-024-01813-z).
In particular, their distance is the infimum of distortion **without a factor
of 1/2**. The finite proofs below are given explicitly; no continuum theorem
is needed for them. The paper's additional topological hypotheses must not be
discarded when making claims about its continuum category. Its
[published correction](https://link.springer.com/article/10.1007/s11005-024-01837-5)
concerns a reference and acknowledgements, not these definitions.

## 2. Full correspondences, not only bijections

A correspondence R⊆X×Y has both coordinate projections onto. Define

```text
dis(R) = max over (x,y),(x',y') in R of |d_X(x,x')−d_Y(y,y')|,
D_C(X,Y) = min over onto-both R of dis(R).
```

Both maxima and minima exist for finite nonempty inputs. Every ordered pair
of relation members is included: diagonals, reverse directions, zeros and
rare large discrepancies. For equal cardinalities, D_B denotes the minimum
over graphs of bijections only. Otherwise D_B is unavailable, not infinity
silently substituted into an exact rational report.

Always D_C≤D_B when D_B is defined. Any exhibited correspondence gives an
upper bound on D_C; a lower bound on every bijection does NOT give a lower
bound on every correspondence. Simultaneously reversing both kernels leaves
D_C unchanged; reversing just one need not do so. Relabelling invariance is
distinct from either operation.

The transpose relation proves symmetry. If R relates X to Y and S relates
Y to Z, their relational composition is onto both sides. For any two of
its members choose the corresponding intermediate y,y'; the ordinary
triangle inequality bounds their discrepancy by dis(R)+dis(S). Thus D_C
obeys the triangle inequality. Also, with a=max d_X and b=max d_Y,

`|a−b| ≤ D_C(X,Y) ≤ max(a,b)`.

For the lower bound use onto-ness to lift a pair attaining either diameter;
the full relation X×Y proves the upper bound. An identity correspondence on
a common labelled set gives D_C≤||d_X−d_Y||∞. A mean or trimmed discrepancy
is not a substitute for this supremum.

### 2.1 Zero distance and lost multiplicity

Write x∼x' if their full outgoing AND incoming profiles agree. This is an
equivalence relation and the kernel descends to its quotient. The graph of
the quotient map has zero distortion, so quotienting these twins leaves
D_C unchanged.

Conversely, in a zero-distortion correspondence, two points paired with the
same point are twins: lift every test point using onto-ness and compare both
directions. The correspondence therefore induces a distance-preserving
bijection between the twin quotients. Hence D_C=0 iff these quotients are
isomorphic. When both spaces distinguish points, zero distance means an
actual distance-preserving bijection. A zero singleton and two all-zero
points have D_C=0 despite different cardinalities.

Multiplicity, probability weights, physical volume and named event marks are
not retained by this unmarked distance. A future marked or measure-aware
comparison needs its own contract; the preceding supplied-measure gate does
not silently add one here.

### 2.2 Exact obstruction to replacing correspondences by bijections

Take X=Y={0,1,2}. List only nonzero values:

```text
X: d(0,2)=1, d(1,2)=11/10;
Y: d(0,1)=1, d(0,2)=11/10.
R = {(0,0),(1,0),(2,1),(2,2)}.
```

Both are point-distinguishing admissible directed separations. R has
distortion 1/10. Distortion strictly below 1/10 would force exact equality
of all paired kernel entries, because the smallest nonzero discrepancy
between possible values {0,1,11/10} is 1/10. A zero-distortion isomorphism
is impossible: X has two points with a nonzero outgoing profile, Y only one.
Thus D_C=1/10.

A bijection with distortion below 1 would preserve positive support, which
has the same obstruction. The bijection 0↦1, 1↦0, 2↦2 attains distortion
1, so D_B=1. This is an exact analytical counterexample, not an optimization
result obtained by running a new search.

## 3. Distinction gaps and a conditional finite-to-space bridge

Define the profile distance (the paper's distinction metric, when points
are distinguished)

`γ_X(x,x') = max_z max(|d_X(x,z)−d_X(x',z)|, |d_X(z,x)−d_X(z,x')|)`.

It is a pseudometric, and a metric exactly when points are distinguished.
For at least two points set σ_X=min_{x≠x'}γ_X(x,x'). Include zero values;
do not omit twins when taking this minimum. For a singleton the mathematical
convention is σ_X=+∞; an exact finite-data schema must represent this as an
explicit singleton case, not a nonfinite JSON number.

If (x,y),(x',y)∈R, onto-ness supplies (z,w) for every z∈X. Comparing the
two outgoing values through d_Y(y,w), and incoming values through d_Y(w,y),
gives γ_X(x,x')≤2 dis(R). The analogous bound holds for fibers over X.
Consequently,

`2 D_C(X,Y) < min(σ_X,σ_Y)  ⇒  every optimal R is a bijection and D_B=D_C`.

This is a sufficient condition, not a necessary one. Strictness matters:
the three-point fork with source-to-sink weights 1 and 3 versus a two-point
chain of weight 2 has σ_X=σ_Y=2 and D_C=1. Merging the fork's sources
attains 1; a smaller error would force an impossible bijection. Finite point
distinction alone supplies no uniform positive gap along a sequence.

### 3.1 What a genuine coverage certificate would permit

For a possibly infinite space M with bounded nonnegative kernel, replace
maxima by suprema in γ and distortion, and the correspondence minimum by
an infimum. The same symmetry and triangle arguments hold in this ambient
bounded-kernel class. This extension alone asserts no Lorentzian topology.

Suppose a finite S⊆M and a supplied retraction p:M→S obey
sup_u γ_M(u,p(u))≤ε. Changing the two arguments in turn gives

`|d_M(u,v)−d_M(p(u),p(v))| ≤ γ_M(u,p(u))+γ_M(v,p(v)) ≤ 2ε`.

The graph of p is onto both sides. If an estimated kernel on S additionally
satisfies ||d̂_S−d_M|_(S×S)||∞≤η, then D_C(M,Ŝ)≤2ε+η. Applying triangle
inequalities in both directions to two such approximations gives

`|D_C(M,N)−D_C(Ŝ,T̂)| ≤ 2ε_M+η_M+2ε_N+η_N`.

This is a useful conditional bridge from a finite exact comparison to a
larger geometry. Its premises are not obtained here. In particular γ_M uses
profiles over ALL of M; γ_S is only a lower bound on that restricted-point
profile distance and cannot certify ambient coverage. A singleton sample
can omit a second event at arbitrarily large separation without changing
any sampled value. A sup-error estimate also does not prove the estimated
kernel's causal/reverse-triangle admissibility; check that separately.

## 4. Scale, shape and two distinct kinds of noncollapse

For a common c>0, D_C(cX,cY)=c D_C(X,Y), where cX multiplies the kernel,
not a metric tensor or sampling density. Thus allowing both inputs to shrink
toward zero makes an absolute error tend to zero without improving shape.
Calibrated scale and shape must be recorded separately.

For positive a=diam X and b=diam Y define X̂=(X,d_X/a), Ŷ=(Y,d_Y/b),
and S_C(X,Y)=D_C(X̂,Ŷ). This is invariant under independent positive
rescaling and is a pseudometric on normalized kernel spaces. It intentionally
forgets absolute scale. Zero-diameter kernels are not normalized: return an
explicit unavailable result, never divide by an arbitrary epsilon.

The diameter bound and the same correspondence give

```text
S_C(X,Y) ≤ 2 D_C(X,Y)/max(a,b),
D_C(X,Y) ≤ min(a,b) S_C(X,Y)+|a−b|.
```

For the first, divide both kernels by a and account for changing d_Y/a to
d_Y/b: error ≤(dis(R)+|a−b|)/a≤2 dis(R)/a. Interchange X,Y and minimize.
For the second, use an optimal normalized correspondence and compare first
at scale a, then at scale b. Shape convergence plus convergence to a finite
common diameter implies raw convergence. Raw convergence implies shape
convergence when the common maximum diameter is bounded away from zero.
Neither statement alone certifies physical units.

Diameter normalization prevents global vanishing but not local merging.
For 0<ε≤1/2 take a three-point fork with weights 1,1+ε and a two-point
chain of weight 1. Both distinguish points. The natural source-merging
correspondence and diameter bound give D_C=ε. After normalization,
S_C=ε/(1+ε): the same relation gives the upper bound. Onto-ness must pair
the fork's value 1/(1+ε) with either 0 or 1 in the chain, with discrepancy
at least ε/(1+ε). The fork's normalized distinction gap is ε/(1+ε), tending
to zero even though both normalized diameters equal 1.

Therefore keep three separate records: raw dimensional error, diameter-
normalized shape error, and local distinction/coverage information. A lower
bound on diameter is not a bound on local gaps, sampling density or measure.

### 4.1 One-sided scale fits are not a symmetric distance

For positive diameters let F(X,Y)=inf_{c>0}D_C(X,cY). With t=cb/a,

`F(X,Y)/a = inf_{t>0} D_C(X̂,tŶ),     S_C/2 ≤ F(X,Y)/a ≤ S_C`.

The upper bound uses t=1. If e=D_C(X̂,tŶ), the diameter bound gives
|1−t|≤e and the identity correspondence gives D_C(tŶ,Ŷ)≤|1−t|;
triangle then gives S_C≤2e. An individual fit with error e in raw units
must satisfy |a−cb|≤e. The fit parameter and this scale residual must not
be concealed behind a fitted percentage.

F is generally asymmetric. A directed two-point unit chain A and symmetric
two-point unit kernel B have S_C=1, F(A,B)=1/2 (at c=1/2), and F(B,A)=1.
Every correspondence must compare B's positive forward/reverse pair with
either a diagonal or a zero direction in A; bijections attain the stated
bounds. B is an invalid-causal control in the larger kernel class, not a
physical counterexample. No general continuous scale optimizer is authorized
by the prospective finite comparison gate.

### 4.2 The audited DD statistic and its missing scale factor

For a declared paired list (not automatically an onto correspondence), write

```text
U = inf_(c>0) max_k |L_k−c τ_k|,    meanL = mean_k L_k > 0,
declared error = ℓ U,               fitted surrogate = U/meanL,
ℓ U = (ℓ meanL)(U/meanL).
```

For positive ℓ, vanishing of these two quantities is equivalent under
uniform bounds 0<m≤ℓ meanL≤M<∞. Without these bounds either implication
can fail, even with all τ_k=1:

- L=(n,2n), ℓ=n⁻²: U=n/2, so ℓU=1/(2n)→0 but U/meanL=1/3.
- L=(n²,n²+2n), ℓ=n⁻¹: U=n, so U/meanL=1/(n+1)→0 but ℓU=1.

A finite exact control is L=(1,1,2), τ=(1,1,3), ℓ=1/2. The optimal c=3/4
gives U=1/4: |1−c|≤u requires c≥1−u, while |2−3c|≤u requires
c≤(2+u)/3, hence u≥1/4; equality is attained. Thus ℓU=1/8,
U/meanL=3/16 and ℓ meanL=2/3. None of these is interchangeable with D_C
without a separately justified pairing and objective. A finite trend or
fitted power law is not a uniform convergence proof.

## 5. Supremum versus trimmed diagnostics

Compare two three-point chains on the same labels. Both have adjacent
separations 1; their endpoint separations are respectively 3 and 2. All
other values are zero. Both kernels are admissible and distinguish points.
Their identity correspondence has nine ordered discrepancy cells: one 1
and eight zeros. The full mean is 1/9, the mean over the three positive-
separation pairs is 1/3 (not the mean over positive-error cells),
and a diagnostic omitting the endpoint pair is 0, while the supremum and
D_C are 1 (the diameter bound is sharp).

On a complete finite list of N nonnegative discrepancies, max≤N mean is
valid but not a size-independent guarantee. A trimmed list supplies no
upper bound on omitted pairs without an additional certificate. Future
reports must retain the full ordered discrepancy cells, maxima and their
attaining pairs; averages may appear only as labelled diagnostics.

## 6. All-pair max-plus closure: the precise repair

Supply a strict order ≺ on X and nonnegative weights w(x,y) on ALL its
comparable pairs. Off-order and diagonal values are displayed as zero, but
are not traversable edges. Define

`T_≺w(x,y) = max_(x=x₀≺...≺xᵣ=y) sum_(j=0,...,r−1) w(xⱼ,xⱼ₊₁)`

on comparable pairs and zero elsewhere. A direct comparable edge is one
of the allowed paths. This requires an explicit order mask; a dense numeric
zero must never create an off-order path.

T_≺ is extensive, monotone and idempotent. It is the least majorant h≥w
supported on ≺ satisfying **order-superadditivity**

`h(x,z)≥h(x,y)+h(y,z) for EVERY x≺y≺z, including zero-valued legs`.

Concatenating maximizing paths proves superadditivity (strictness prevents
cycles or repeated vertices). Induction along a path shows every such
majorant dominates its sum; hence it dominates T_≺w. This proves leastness
and idempotence. Every path has at most n−1 edges, so, on a fixed order,

`||T_≺w−T_≺v||∞ ≤ (n−1)||w−v||∞`.

The constant is sharp on a full n-chain: compare all-zero weights with
weight ε on every comparable pair; the endpoint closure is (n−1)ε.
This is neither uniform in growing n nor a bound for changing orders.

Positive support of T_≺w equals the supplied order iff every cover weight
is positive. A cover has no alternative path; conversely a saturated chain
of positive covers gives a positive sum for any comparable pair. With zero
weights, conditional reverse triangle is weaker than order-superadditivity.
For a three-chain w(0,1)=0, w(1,2)=1, w(0,2)=0, the conditional inequality
is vacuous but order-superadditivity fails. Closure makes the endpoint 1
while the first cover remains zero.

In particular, additive closure can gain positive support along a path with
a zero leg. Its support need not equal the transitive closure of the positive
support of w. Do not transplant the earlier multiplicative inverse/path
support theorem into this max-plus construction.

### 6.1 Why cover-only recovery is not the same theorem

On the three-chain w(0,1)=w(1,2)=1, w(0,2)=3, the input already satisfies
order-superadditivity. Its all-pair closure has endpoint 3; a cover-only
longest-path calculation returns 2. Thus superadditivity does not imply
recovery from cover weights.

The all-pair closure pointwise dominates the cover-only closure for
nonnegative supplied weights, but that does not order approximation errors.
Reference endpoint 2 favors the cover-only output; reference endpoint 3
favors the all-pair output. Both references can have the same unit adjacent
weights. A mixed-family or uniform continuum claim requires its own proof;
none follows from pointwise domination or this finite closure theorem.

## 7. What this contributes, and what it leaves open

This is a defensible language for comparing proposed directed geometries:
it states the information retained, distinguishes absolute scale from shape,
and gives a conditional coverage/error bridge. It also identifies when a
cheaper bijection search is mathematically justified. These are useful
structures even without an ontological commitment.

No agreement with a new quantum/gravitational observable is tested here.
A null pair is not assigned positive proper separation by a chain-count
convention. Acquisition noise, missing events and setup/model artifacts need
explicit bounds or controls; they cannot be used to discard inconvenient
supremum errors. The preceding Q and causal G constructions do not determine
this new supplied separation kernel. Metric/measure calibration, stochastic
growth, uniform coverage, continuum rates, physical dynamics, RET integration
and empirical application validation remain separate obligations.

## 8. Prospective bounded exact verification

The next gate may implement only the following fixed finite contract.
Inputs and arithmetic are exact rationals; no coordinate simulation, random
sampling, parameter sweep, continuous fitting solver or acquisition is included.
Expected values below are analytical predictions, NOT executed results.

### 8.1 Seven comparison bases

Unlisted entries are zero; labels start at 0. “Chain t” means two points
with only d(0,1)=t. Each row has the stated original label order.

| Base | X | Y | D_C | D_B | S_C |
| --- | --- | --- | --- | --- | --- |
| zero_multiplicity | zero singleton | two all-zero points | 0 | unavailable | unavailable |
| scale_pair | chain 1 | chain 3/2 | 1/2 | 1/2 | 0 |
| fork_correspondence | d02=1,d12=11/10 | d01=1,d02=11/10 | 1/10 | 1 | 1/11 |
| duplicate_fork | chain 1 | d02=d12=1 | 0 | unavailable | 0 |
| near_twins | d02=1,d12=11/10 | chain 1 | 1/10 | unavailable | 1/11 |
| endpoint_excess | d01=d12=1,d02=3 | d01=d12=1,d02=2 | 1 | 1 | 1/6 |
| orientation_mismatch | chain 1 | d01=d10=1 | 1 | 1 | 1 |

Normalized bijection distances, where available, are respectively 0,10/11,
1/6,1 for scale_pair, fork_correspondence, endpoint_excess and
orientation_mismatch. Only the last base contains an invalid-causal kernel.
zero_multiplicity's two-point kernel and duplicate_fork's three-point kernel
fail point distinction; all other inputs distinguish points.

Each base has four SEPARATE variants: identity; cyclic relabelling i↦i+1
mod n independently in each input; simultaneous transpose of both kernels;
common multiplication of both kernels by 3/2. Do not compose, deduplicate
or add variants. Raw errors and gaps scale by 3/2 in the last variant;
normalized errors are invariant. Labels, inverse relabellings and unavailable
cases must be explicit.

The predicted census is 28 rows, 132 input-node occurrences and 332 full
input square-matrix cells. Across these rows, enumerate all 4,752 relation
bitmasks, including the empty candidates rejected for non-surjectivity;
retain every one of the predicted 2,380 onto relations, their 12,576 member
occurrences and all 69,976 ordered raw discrepancy cells. Normalization is
available for 69,960 corresponding cells. There are 64 bijection records.
Counts retain repeated kernels across different named variants.

These counts can be derived without enumeration. For m×n define

`P_mn(z)=sum_(i=0..m,j=0..n) (−1)^(i+j) C(m,i)C(n,j)(1+z)^((m−i)(n−j))`.

Its coefficient of z^k counts onto relations of size k. For 3×3 the
nonzero coefficients, k=3,...,9, are (6,45,90,78,36,9,1); for 2×3,
k=3,...,6, they are (6,12,6,1); for 2×2, k=2,...,4, they are (2,4,1).
For 1×2 only the full size-two relation is onto. Summing k and k² times
these coefficients yields the stated member and ordered-cell census.

The primary route enumerates bitmasks and checks both projections. The
independent reference route chooses nonempty row neighborhoods and checks
coverage of all columns. They may share declared fixture data and exact
serialization, not enumeration, distortion, normalization, quotient or
closure helpers. Compare the complete canonical relation lists, full ordered
error matrices, maxima/all attaining pairs, all minimizing relations and
all bijection records—not just the two optimum scalars. Retain raw inputs,
admissibility, twin classes, profile distances, gaps, diameters and all
available normalized fields. Use supplied analytical correspondences and
the diameter/value-gap arguments as independent expected-value oracles.

### 8.2 Four closure bases and fixed analytical controls

Closure bases are: the singleton empty order; the three-chain with weights
(w01,w12,w02)=(1,1,3); that chain with (0,1,0); and that chain with
(1,1,1). Their four separate variants are identity, cyclic relabelling,
simultaneous order/weight reversal, and weight multiplication by 3/2.
Predicted totals: 16 rows, 40 nodes, 112 full square cells and 36 comparable
weight slots. The primary route uses explicit all-pair path enumeration;
the reference uses a topologically ordered max-plus recurrence. Keep paths,
weights, sums, attaining paths, full closure and cover-only matrices, both
support relations, and every order-superadditivity residual.

Fixed named unit controls may check symmetry, triangle by explicit relation
composition on the three two-point chains of weights 1,3/2,2; the strict
gap boundary fork (1,3) versus chain 2; the F(A,B) asymmetry witness; the
paired-list optimum (L,τ,ℓ)=((1,1,2),(1,1,3),1/2); the endpoint mean/trim
example; and the three-chain Lipschitz equality between all-zero and all-unit
comparable weights. These controls are not additional study rows or sweeps;
their exact input/output evidence must be retained with tests. The infinite
families and ambient coverage theorem remain analytical, not finitely proved
by this executor. Include malformed-input and off-order-zero negative tests.

### 8.3 Evidence and stopping rules

Before first mathematical execution, freeze this two-file design and seven
new prospective sources: verification README, fixtures, primary route,
reference route, study driver, mathematical/API tests and evidence tests.
That is nine source bindings. Freeze exact bytes/hashes, entry points,
test inventory, named controls, census, report schema and resource checks.
No old branch implementation is imported as a trusted oracle. Executable
local evidence helpers must reside in these bound sources; no unbound
local helper imports are allowed. Standard-library infrastructure is allowed.

Default caps: 30 seconds per study run, 60 seconds per suite, 262,144 bytes
per source file and 16 MiB per serialized evidence artifact. A pre-execution
code/schema size estimate may tighten the report, but must not drop any
contracted relation or discrepancy cells. If the full protocol cannot fit,
stop and redesign BEFORE execution. After the first mathematical execution,
do not repair sources or retune fixtures in this gate: retain the failure
and propose a separately versioned repair. No silent partial run passes.

Require both normal and optimized-mode tests, and three complete replays
against the first canonical capture, including exactly one Python 3.11
replay. Retain independent-route agreement, census, all named controls,
source freeze, full native report, canonical report/capture hashes and a
final decision. Existing immutable captures are checked as metadata only;
unrelated core/RET/application changes stay outside scope. Passing this
bounded verification would verify these finite implementations, not prove
uniform convergence, sample coverage or gravitational dynamics.
