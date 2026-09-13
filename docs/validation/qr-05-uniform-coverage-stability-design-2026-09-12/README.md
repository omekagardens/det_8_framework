# QR-05: uniform coverage, stable closure and calibrated noncollapse

12 September 2026 (Pacific/Honolulu). **Analytical design only.** No new
mathematical executor, fixture enumeration, test suite, simulation or
acquisition runs in this gate. Section 9 is a prospective finite verification
contract, not an executed result. See the [decision record](RESULTS.md).

This standalone calculus requires no DET ontology. It follows the
[exact correspondence/noncollapse verification](../qr-05-correspondence-noncollapse-verification-2026-09-12/RESULTS.md)
and addresses the uniformity and normalization gaps retained in the
[concurrent-branch audit](../qr-05-bridge-reconciliation-2026-09-12/AUDIT_GEOMETRY.md).
Its constructive result is a conditional route from coverage and calibrated
pairwise intervals to a stable directed-kernel approximation. It does not
derive the supplied geometry, certify an apparatus, or select gravity laws.

## 1. Domain and comparison conventions

Let M be nonempty, with a bounded nonnegative kernel d_M, zero on the
diagonal. Write a_M=sup d_M. Argument order is source then target. Define

```text
γ_M(x,x') = sup_z max(|d_M(x,z)−d_M(x',z)|,
                     |d_M(z,x)−d_M(z,x')|),
dis(R) = sup_((x,y),(x',y')∈R) |d_M(x,x')−d_N(y,y')|,
D_C(M,N) = inf_(R onto both M,N) dis(R).
```

For finite inputs, these extrema are attained. For general bounded spaces
keep suprema and infima; no minimizer or compactness is presumed. γ is a
pseudometric and separates points exactly when incoming/outgoing profiles
do. D_C is symmetric and obeys the triangle inequality by composition of
onto relations. It is a comparison of unmarked kernels, not a comparison
of measures, event multiplicities or coordinate labels.

The no-half correspondence convention and profile metric are those of
[Minguzzi and Suhr, *Lorentzian metric spaces and their Gromov–Hausdorff
convergence*, sections 4.1 and 4.3](https://link.springer.com/article/10.1007/s11005-024-01813-z).
The proofs here use the ambient bounded-kernel class. Applying the paper's
Lorentzian-space theorems additionally requires its point-distinction and
topological hypotheses; a supplied auxiliary mesh metric below does not
replace them. No new literature novelty claim is made for these estimates.

When a kernel is called causally admissible, separately require strict
positive support and conditional reverse triangle on two positive legs.
When an operator T_C is used, require the stronger **C-superadditivity**
on the declared order C, including any zero-valued legs. These are not
interchangeable conditions. All dimensional comparisons below use a common
declared separation unit; rescaling a kernel is not a coordinate or metric-
tensor transformation silently applied afterward.

## 2. A coverage certificate with an explicit error budget

Supply a metric q on M and a nondecreasing modulus ω with ω(0)=0,
ω(r)→0 as r↓0, and the GLOBAL bound

`γ_M(x,x') ≤ ω(q(x,x')) for every x,x'∈M`.

This bound must cover all profiles over M, not only profiles evaluated on
the observed sample. For a finite nonempty S⊆M define its q-fill radius
h=sup_(x∈M) min_(s∈S) q(x,s), and require h<∞. Without that condition the
modulus-based certificate is unavailable. A nearest-point assignment p:M→S is a
retraction; resolve ties in a fixed label order. More generally, any supplied
retraction with q(x,p(x))≤h is enough.

Let d_S be the restriction of d_M to S×S. Changing the two arguments gives

```text
|d_M(x,x')−d_S(p(x),p(x'))|
 ≤ γ_M(x,p(x))+γ_M(x',p(x')) ≤ 2ω(h).
```

Thus the graph of p, onto both sides, has distortion at most 2ω(h).
If an estimated nonnegative zero-diagonal sample kernel d̂_S has the
SIMULTANEOUS bound ||d̂_S−d_S||∞≤η, then

`D_C(M,Ŝ) ≤ E := 2ω(h)+η`.

If a sharper graph-distortion certificate Δ_p is available, substitute
E=Δ_p+η. The matrix error is over all ordered sample pairs, including
null, reverse and omitted-by-diagnostic pairs. It includes separately
justified numerical and measurement errors; a fit residual is not itself
a calibration bound. Kernel admissibility is checked separately from this
ambient comparison inequality.

For two independently described approximations, triangle inequalities yield

`|D_C(M,N)−D_C(Ŝ,T̂)| ≤ E_M+E_N`.

Independence of the errors is not needed. The bound is useful precisely
because it names what a finite matrix comparison lacks: ambient coverage,
a global continuity modulus and simultaneous error control.

### 2.1 Why a point cloud cannot certify its own coverage

Compare two possible ambient models for the same observed pair S={a,b}:

```text
Model A: M=S,              d(a,b)=1.
Model B: M={a,u,b},        d(a,u)=d(u,b)=1/2, d(a,b)=1.
All other directed values are zero.
```

Both are point-distinguishing, causally admissible, and have diameter exactly
1. Their entire observed S×S kernel is identical. Nevertheless the ambient
γ-fill radius of S is 0 in A and 1/2 in B. Even an exact diameter reference
does not remove the ambiguity. No function of just that observed matrix
can distinguish these ambient-coverage targets over this model class.

In B, give u mass 0<ε<1 and each endpoint mass (1−ε)/2. This measure has
full support, yet n independent draws miss u with probability (1−ε)^n.
Without a lower mass bound this probability can be arbitrarily close to
1 for any fixed n. This uniform counterexample varies ε across the permitted
measure class; it does not deny eventual density for one fixed measure.
Conditional on missing u, the observed endpoint law
matches A's equal-endpoint law. More repetitions do not supply a uniform
finite-sample guarantee over arbitrarily small hidden masses.

## 3. Fixed-order closure: identify the accumulating error

On a finite strict order C, supply nonnegative C-supported weights w, with
diagonal/off-order zeros. All comparable pairs are edges, not only covers.
T_Cw is the maximum sum over all strict C-paths, zero outside C. The
[preceding calculus](../qr-05-correspondence-noncollapse-design-2026-09-12/README.md)
proves that it is the least C-superadditive majorant of w.

Let d be a nonnegative, zero-diagonal, C-supported and C-superadditive
target on the same labelled set. Then T_Cd=d.
Write H(C) for the maximum number of edges in a strict path, and define

```text
β = max_paths sum_e |w_e−d_e|,
η_minus = max_pairs (d_e−w_e)_+,
β_plus = max_paths sum_e (w_e−d_e)_+.
```

Use zero for an empty path/pair menu. The same path menu bounds differences
between maxima, giving

`||T_Cw−d||∞ ≤ β ≤ H(C)||w−d||∞`.

A sharper one-sided statement is

`d−η_minus ≤ T_Cw ≤ d+β_plus`.

The lower bound uses the available direct edge T_Cw≥w. For the upper bound,
each w-path sum is at most its d-path sum plus β_plus, and C-superadditivity
bounds the d-path sum by its endpoint d. Negative perturbations therefore
need not accumulate, but positive perturbations can.

If d is nonnegative, zero-diagonal and C-supported but not C-superadditive,
write b_C=||T_Cd−d||∞. Only
`||T_Cw−d||∞≤β+b_C` follows. An unreported order/model bias cannot be
relabelled measurement noise.

### 3.1 A sharp growing-size obstruction

For n≥2 take the full chain with t_i=i/(n−1), d_ij=t_j−t_i for i<j,
and w_ij=d_ij+η on every comparable pair. A path with k edges has sum
d_ij+kη. Hence

`(T_Cw)_ij=d_ij+(j−i)η`, and endpoint error is `(n−1)η`.

Choosing η_n=1/(n−1) makes entrywise noise vanish while closure error stays
1. Here T_Cw=2d exactly: diameter-normalized shape error is zero even though
raw calibrated error is 1. Keeping diameters merely bounded away from zero
does not repair that scale mistake; an absolute reference must also agree.
For a generic two-sided error route one therefore needs H(C_n)η_n→0,
or a genuinely sharper path-budget argument.

### 3.2 A certified path budget can replace the height factor

If |w_e−d_e|≤η a_e for nonnegative supplied a_e and every strict path
has sum_e a_e≤B, then ||T_Cw−d||∞≤ηB. For example, supplied monotone
marks t∈[0,1] and a_ij=t_j−t_i telescope along paths, giving B≤1.
The weighted error envelope and the marks/order must be justified; assigning
these marks after seeing the desired result is not a certificate. B must
remain uniform along a sequence before it supports a uniform rate.

### 3.3 A changing order is a different problem

Let C0 contain only 1≺2, with d12=1 and all other entries zero. Let C1 be
the full three-chain, and put w01=ε,w12=1,w02=0, 0≤ε≤1. Although
||w−d||∞=ε, T_C1w has endpoint 1+ε, while T_C0d has endpoint 0.
At ε=0 the numeric input arrays are identical and changing the order alone
creates endpoint 1. The missing C1-superadditivity of d has bias b_C1=1.

For 0<ε≤1, even the unmarked correspondence distance between the two
closed kernels is 1. The isolated input point must be paired with a target
point having some incoming or outgoing separation at least 1; onto-ness
supplies the other member and proves the lower bound. The bijection
0↦1,1↦0,2↦2 attains it. This is not an impossibility theorem for separately
certified order recovery; it shows why the fixed-order premise matters.
An edge list missing a required transitive pair must be refused as an order,
not silently repaired and then described as unchanged input.

## 4. Constructive interval closure without size-amplified overshoot

Supply simultaneous bounds 0≤l≤d≤u on a known C, and assume the true d is
C-superadditive and zero off C. Leastness and extensivity give

`l ≤ T_Cl ≤ d ≤ u`.

Consequently

`0 ≤ d−T_Cl ≤ u−l`, so `||T_Cl−d||∞ ≤ v := ||u−l||∞`.

There is NO H(C) factor. This route intentionally builds a conservative
lower estimate. It is not asserted to be unbiased, optimal, or physically
preferred. If w already satisfies d−η≤w≤d, the sharper bound is η,
again independently of graph size.

For a nonnegative centered estimate w with justified simultaneous error η,
take l=max(0,w−η), u=w+η on comparable pairs, and keep off-order/diagonal
entries zero. Then v≤2η and the lower closure has error at most 2η.
Missing measurements cannot be assigned tight zero intervals. Unknown order
cannot be treated as known merely to invoke this theorem.

### 4.1 A complete finite feasibility criterion

There exists a C-superadditive h with l≤h≤u **if and only if** T_Cl≤u.
Necessity follows because every such h dominates the least majorant T_Cl;
sufficiency uses h=T_Cl. Equivalently, every lower-weight path sum must
not exceed its endpoint upper bound.

On the three-chain let l=(l01,l12,l02)=(1,1,0). For u=(1,1,3/2),
the entrywise intervals are nonempty but T_Cl02=2>3/2, so they are jointly
infeasible. Replacing only u02 by 2 makes them feasible, with h=(1,1,2).

This criterion does not force point distinction or positive separation on
every C-pair; impose those additional requirements separately if needed.
Feasibility establishes the existence of a model inside the intervals,
not that the actual world is that model or that the intervals cover truth.
Failure is an anomaly-triage signal: measurement error, order error, an
invalid model class or bad calibration are possible causes, not uniquely
identified diagnoses. This gives a possible future RET interface only IF
RET supplies calibrated simultaneous intervals; no such integration or
coverage claim is made here.

## 5. A combined approximation theorem and scale contract

For each finite S_n⊆M supply:

- A retraction with q-fill bound h_n and the same global modulus ω.
- A strict C_n for which d_n=d_M|_(S_n×S_n) is C_n-superadditive and
  supported on C_n.
- Simultaneously valid full-pair intervals 0≤l_n≤d_n≤u_n, zero off C_n
  and on the diagonal as in section 4, of maximum width v_n.

Let K_n be the kernel T_Cn l_n on S_n. Sections 2 and 4 give

`D_C(M,K_n) ≤ E_n := 2ω(h_n)+v_n`.

Thus h_n→0 and v_n→0 suffice for this conditional convergence theorem;
no shrinking pair-error rate multiplied by graph height is required on
this conservative route. For two such approximations, comparison error is
at most E_n+E'_n. A sharper supplied Δ_p may replace 2ω(h_n). These are
theorems with premises, not evidence that the premises hold in DET records.

For a=a_M>0 and â_n=diam K_n, the diameter inequality gives
|â_n−a|≤E_n. If E_n<a, normalization is defined, and

`D_C(M/a,K_n/â_n) ≤ 2E_n/a`.

A known a≥a0>0 can replace a in the denominator. Conversely, normalized
shape convergence transfers to raw error only with suitable converging
calibrated scales, using D_C≤min(a,b)S_C+|a−b|. An arbitrary fitted scale
or a supplied measure normalization is not automatically such a reference.

The audited DD identity remains

`lattice_scale*U = (lattice_scale*meanL)*(U/meanL)`.

Uniform positive lower and finite upper bounds on lattice_scale*meanL
guarantee transfer of vanishing in both directions. Without them neither
transfer is guaranteed in general; particular sequences can still have both
quantities vanish. The earlier exact
counterexample families remain in force. Neither this interval theorem nor
a successful finite power-law fit resolves that missing normalization.

## 6. A concrete supplied-geometry bridge, including null boundaries

Take the rectangle M=[0,T]×[−L,L], T>0,L≥0, with common time/space units
(c=1), and q the coordinate sup metric. Define the directed kernel

`d(u,v)=sqrt(max((t_v−t_u)_+²−(x_v−x_u)²,0))`.

This is the usual supplied flat-spacetime proper-separation expression with
past directions set to zero. It is a test background, not a geometry derived
from records. q is an analytical coverage aid, not a new fundamental field.
Null and spacelike separations are exactly zero; reverse directions are
not symmetrized.

Positive support is future-timelike and transitive. For two future-timelike
increments a,b, their Minkowski inner product is nonnegative and

`(a0*b0−a1*b1)² − (a0²−a1²)(b0²−b1²) = (a0*b1−a1*b0)² ≥ 0`.

Taking square roots and expanding the squared length of a+b proves reverse
triangle. The same nonnegative-limit argument includes null legs for the
known strict future-causal order. A rectangle-restricted kernel is therefore
compatible with the order-superadditivity needed above when that order is
supplied correctly; no physical law is changed by the comparison machinery.

### 6.1 Explicit global modulus and grid certificate

Set C=2T+4L. Moving one endpoint by q-distance δ changes its positive-part
time square by at most 2Tδ and its spatial square by at most 4Lδ.
Positive-part clipping is 1-Lipschitz, and for A,B≥0,
|sqrt(A)−sqrt(B)|≤sqrt(|A−B|). Hence

`γ_M(u,u') ≤ sqrt(C q(u,u'))`.

The generic certificate gives 2sqrt(Ch). Directly changing both endpoints
improves the true sample graph distortion to

`Δ_p ≤ min(T,sqrt(2Ch))`.

The minimum uses that both exact kernels lie between 0 and T. Thus a
calibrated estimated sample kernel adds η, or the lower-interval closure
adds v, to this geometric bound. A product grid with positive integers n_t
time intervals and n_x spatial intervals, including boundaries, has

`h ≤ max(T/(2 n_t), L/n_x)`.

For L=0, a single spatial node suffices and the spatial term is zero.
This is a deterministic coordinate-mesh certificate, not a reconstruction
of those coordinates from a distance matrix. Rational coordinates generally
produce irrational square roots; a generic grid cannot be fed silently
into the existing Fraction-only API. A future implementation must retain
symbolic squared bounds, algebraic values or preregistered outward-rounded
error intervals. No generic radical evaluator or grid simulation runs here.

### 6.2 Exact rational null-boundary witnesses

In T=L=1 use a=(0,0), b=(1/2,1/2), and for k≥2

`b_k=((k²+1)/(2(k²−1)),1/2)`.

Then q(b_k,b)=1/(k²−1), d(a,b)=0,
d(a,b_k)=k/(k²−1), and d(b,b_k)=1/(k²−1). All these values are rational.
The profile-change/coordinate-change ratio is at least k and diverges.
More generally the ratio to q^α grows as k^(2α−1) for α>1/2.
Thus one cannot replace the uniform square-root modulus near null boundaries
by a Lipschitz or stronger-than-1/2 Hölder assertion.

For k=3, the three-point kernel has only d02=3/8,d12=1/8 positive;
for k=5, only d02=5/24,d12=1/24. These are prospective finite regressions
of exact arithmetic, not finite proofs of the infinite-family result.
For L=0 the kernel instead reduces to (t_v−t_u)_+ and γ=q; the spatial
null-boundary obstruction is absent.

### 6.3 A supplied geometric scale anchor

The rectangle has diameter T, attained by a vertical boundary-to-boundary
pair. If S includes that pair, its exact diameter is T. For a general
h-net with h<T/4, approximate both endpoints on the same vertical line: their time
separation is at least T−2h and spatial difference at most 2h. This gives

`diam S ≥ sqrt(max(T²−4Th,0))`.

For h≥T/4 the displayed lower bound is simply zero and is trivial.
For h<T/4 it is positive; h≤θT with θ<1/4 gives a uniform relative
lower bound. An estimated kernel with sup error η has diameter at least
this lower bound minus η (or minus v for the interval route). These are
supplied-coordinate consequences, not empirical clock/length calibration.

## 7. Conditional sampling guarantees, not fitted convergence

Let (M,q) be compact, with a probability measure μ on measurable q-balls.
Fix a deterministic cover by K radius-r balls, each of μ-mass at least
m(r)>0. For N IID draws let S_N be the set of sampled points; repeated
draws need not give distinct points. If every cover ball is hit, triangle
inequality gives fill_q(S_N)≤2r. Union bound therefore gives

`P(fill_q(S_N)>2r) ≤ min(1,K(1−m(r))^N) ≤ min(1,K exp(−N m(r)))`.

If simultaneous sample-kernel error ≤η fails with probability at most α,
the error certificate with h=2r fails with probability at most δ+α,
where δ is the coverage bound above. No independence between measurement
and sampling errors is required. The interval route similarly uses its
already justified simultaneous-coverage event and width v. Per-pair error
probabilities do not by themselves control the growing collection of all
pairs: if each of at most N² ordered pairs fails with probability ≤p_N,
only a bound such as N²p_N follows without stronger joint information.

Suppose, on the relevant small-radius range, K(r)≤A r^(−d) and
m(r)≥b r^d, for fixed supplied A,b,d>0. With
r_N=(c log N/N)^(1/d), N≥2, substitution gives

`δ_N ≤ (A/c) N^(1−bc)/log N`.

For bc≥1 this tends to zero. For bc>2 it is summable; the boundary bc=2
only gives a nonsummable 1/(N log N) bound. Almost-sure total-error
convergence by the first Borel–Cantelli implication additionally requires
summable measurement-failure bounds and η_N→0 (or v_N→0). Independence
across N is not needed for that implication. All bounds must be valid at
r_N; the symbols are not parameters estimated retrospectively from one
successful point cloud.

With a Hölder modulus ω(r)=K0 r^α, the coverage term is conditionally
O((log N/N)^(α/d)). The supplied Minkowski square-root modulus has α=1/2.
This is not a longest-increasing-subsequence fluctuation exponent, a rate
for a particular DET growth process, or a transfer from a single-interval
distribution to a maximum over intervals. Those growth/calibration premises
remain separate. Fixed-space full support does give eventual IID density
almost surely: each fixed finite 1/j-scale cover has positive ball masses
and a summable miss bound, and one intersects these countably many events.
It alone gives no quantitative uniform rate across this permitted
measure/domain class.

## 8. Noncollapse must be defined at the intended resolution

Three different conditions now have distinct roles:

- A calibrated positive diameter prevents global vanishing of the unit scale.
- Lower sampling mass on small balls and a covering bound control holes.
- Profile separation of a finite set of targets controls whether a low-error
  correspondence can merge those targets.

These control different failure modes and cannot simply replace one another.
In the same units γ≤diam, so a positive gap between at least two targets
does imply a diameter lower bound; neither condition certifies sampling
mass or coverage. In particular, a fixed minimum profile gap
cannot be demanded for arbitrarily fine samples of an infinite compact
distinguishing geometry. A compact γ-space has only finitely many points
in any σ0-separated subset, for each σ0>0. Arbitrarily fine nets in an
infinite distinguishing quotient require unbounded cardinality: choose
any fixed number of distinct points and balls smaller than half their
minimum separation. Eventually separate sample points must cover them.
Thus the minimum sample gap tends to zero.

Furthermore γ computed using only sample probes is no larger than the
ambient γ on sample points, so a uniform positive gap cannot be recovered
by restricting the profiles. If the quotient is finite, this packing
obstruction does not apply. The appropriate future object is a declared
resolution-dependent set of distinguishable targets or cells, not a blanket
ban on all local merging as sampling gets finer. No clustering/identity
algorithm is selected here.

## 9. Prospective bounded certificate verification

The next gate should verify the finite implementation of these certificate
calculations, not simulate a continuum or draw random samples. All study
objects have at most three ambient nodes and rational entries. Five coverage
bases and six interval bases each receive four SEPARATE variants: identity,
cyclic relabelling, simultaneous kernel/order reversal and common separation-
value multiplication by 3/2. No composition, deduplication or parameter sweep.

### 9.1 Five finite coverage bases

Unlisted kernel entries are zero. S is ordered increasingly in original
labels; p lists the image in S of each ambient node. Under cyclic ambient
relabeling P, preserve the transported sample-list order S'=[P(s) for s∈S]
without re-sorting: sample-matrix indices keep their positions, and
p'=P∘p∘P⁻¹. Retain both label maps and inverses. Reversal transposes the
ambient and sample kernels without changing labels, S or p; rescaling
multiplies both kernels and all separation-valued bounds by 3/2. In the table, the
sample estimate equals the true restriction unless explicitly changed.

| Base | Ambient kernel M | S; p | Sample estimate | Ambient γ-radius ε | True graph distortion Δ | η | Estimated graph distortion |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| singleton | one zero node | {0}; (0) | zero | 0 | 0 | 0 | 0 |
| observed_chain | d01=1 | {0,1}; (0,1) | exact | 0 | 0 | 0 | 0 |
| unseen_midpoint | d01=d12=1/2,d02=1 | {0,2}; (0,0,2) | exact | 1/2 | 1/2 | 0 | 1/2 |
| biased_midpoint | d01=d12=1/2,d02=1 | {0,2}; (0,0,2) | sample edge=5/4 | 1/2 | 1/2 | 1/4 | 3/4 |
| near_twins | d02=1,d12=11/10 | {0,2}; (0,0,2) | exact | 1/10 | 1/10 | 0 | 1/10 |

Retain every ambient/sample kernel and profile cell, S, p, relabelling and
its inverse, full true/estimated graph discrepancy matrices, ε,Δ,η and both
upper bounds Δ+η and 2ε+η. Also retain diameters and the observed-chain/
unseen-midpoint identical-observation/different-coverage witness. A graph
distortion is an exhibited correspondence upper bound, not a newly solved
unrestricted optimum. The primary may loop over ordered ambient pairs;
the independent reference should use explicit rectangular relation incidence
to pull back the sample kernel. Neither borrows the prior mathematical engine.

Prospective census: 20 rows, 48 ambient-node occurrences, 36 sample-node
occurrences, 128 ambient square cells and 128 ordered discrepancy cells
on the retraction graphs, 68 sample square cells and 48 retraction entries.
The rectangular ambient-by-sample incidence masks instead contain 92 cells.
These are hand-derived expected counts, not measured results.

### 9.2 Six interval bases

All non-singleton orders are full three-chains. Triples list (01,12,02).
A missing target means no supplied truth witness; infeasibility must not
manufacture one. The extra centered w belongs only to positive_center.

| Base | Target d | Lower l | Upper u | T_Cl | Feasible? |
| --- | --- | --- | --- | --- | --- |
| singleton | zero | zero | zero | zero | yes |
| conservative_chain | (1/2,1/2,1) | (3/8,3/8,7/8) | (5/8,5/8,9/8) | (3/8,3/8,7/8) | yes |
| positive_center | (1/2,1/2,1) | (1/2,1/2,1) | (3/4,3/4,5/4) | (1/2,1/2,1) | yes |
| inconsistent_endpoint | unavailable | (1,1,0) | (1,1,3/2) | (1,1,2) | no |
| feasible_endpoint | (1,1,2) | (1,1,0) | (1,1,2) | (1,1,2) | yes |
| zero_cover | (0,1,1) | (0,1,0) | (0,1,1) | (0,1,1) | yes |

For positive_center supply w=(5/8,5/8,9/8) and centered radius 1/8.
T_Cw=(5/8,5/8,5/4) has raw error 1/4; T_Cl=d has error zero. For
conservative_chain the one-sided lower-closure error is 1/8 and interval
width is 1/4. Retain full arrays, all lower-weight paths and sums, maximizing
paths, every T_Cl≤u residual, feasibility witnesses/violations, target
membership and superadditivity where supplied, and exact error/budget fields.
Use independent explicit-path and topological recurrence implementations.

Prospective census: 24 rows, 64 nodes, 184 cells per full matrix, 60 comparable
slots, 80 strict-path records and 100 path-weight occurrences. Truth is
supplied in 20 rows over 52 nodes and 148 square cells. Feasibility is expected
in 20 rows and failure in 4. No target error is reported for the latter.

### 9.3 Fixed controls, resource and evidence boundaries

Four additional control families are authorized, separate from the 44 study
rows: the three-point telescoping budget t=(0,1/2,1),w=(5/4)d,B=1; the
changed-order witness at ε=1/8 with its displayed correspondence; the two
three-point null-boundary controls k=3,5; and arithmetic of the exact union
bound K=4,m=1/4,N=8, namely 6561/16384. The four families contain five
parameter instances because the null family uses two k values. The
probability control draws no
samples and does not certify its supplied covering/mass assumptions.
Include malformed-order/interval, missing-target, zero-diameter, native-
rational and unavailable-field tests. Generic radicals remain out of scope.

Before first mathematical execution, freeze the two files of this design
and seven new sources: executable README, fixtures, primary, reference,
study driver, mathematical/API tests and evidence tests. Freeze exact source
bytes, schemas, all controls, resource estimates and test inventory. Keep
all local executable helpers within these nine bindings; use only standard-
library infrastructure otherwise. Preserve type-strict native rational
reports, authenticated source snapshots and write-once captures.

Default caps remain 30 seconds per study, 60 seconds per combined suite,
262,144 bytes per source and 16 MiB per artifact. Stop and redesign BEFORE
execution if the full evidence cannot fit; after first execution, retain
any failure without modifying the frozen sources in that gate. Require
normal/optimized tests and three dedicated full replays including exactly
one Python 3.11 replay. Prior evidence checks are metadata-only.

A passing bounded certificate gate would verify finite arithmetic and
refusals. The ambient modulus/coverage theorems, infinite families, uniform
rates and probability premises are not proved by those finite cases. No
new geometry simulation, causal-growth experiment, empirical acquisition,
RET change or gravity/clock coupling is authorized by this design.
