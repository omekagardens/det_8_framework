# QR-05I — analytic portability contract

Status: protocol frozen before implementation, 2026-09-06.
Research base: `0f8d3ec4023cea5aac840cf19be692f0f2bbf5e8`.
This directory is isolated mathematical research. No RET/core imports, API
changes, dependency installation, remote synchronization, empirical claims,
new physical laws, or ontological commitments. Earlier evidence stays frozen.

## Question and acceptance

Replace QR-05H's two selected independent sampling settings with the complete
two-color independent sampling family on the closed square `[0,1]^2`.
Determine which existing summaries preserve the polynomial joint law of the
four chain counts, which preserve only their means, and whether H's finite
menu partitions happen to agree with the analytic partitions in this bounded
universe. Agreement or a retained counterexample can complete this gate.
No outcome for full-law partition counts is prescribed in advance.

Acceptance requires two independent exact executors with complete identical
native output: observed-order binomial expansion, and original-source
chain-set evaluation followed by degree-bounded tensor interpolation.
The runner independently audits coefficients, held-out evaluations, partitions
and pinned H identities. Independent tests, normal and optimized execution,
create-only capture, immutable replay and source/prior hashes are required.
Passing finite checks is not machine-checked proof of the general statements
below. The proof arguments are explicit mathematics, not inferred from testing.

## Standalone mathematical contract

An input order is a finite partially ordered set with fixed bottom 0 and top 7.
A supplied observation S contains every fixed vertex and some eligible vertices.
A continuation U retains every fixed vertex and independently keeps each
eligible odd-ID vertex with probability x and each eligible even-ID vertex
with probability y. Color is public apparatus metadata, not geometry. It
applies only to eligible vertices. A fixed interior vertex is never randomized.

Let O,E be the numbers of eligible odd/even vertices in S. For U contained in
S, let o,e be their retained numbers. For q=0,1,2,3, N_q(U) is the number of
q-internal-vertex chains between the probes, counted once per vertex set.
Thus N_0=1. Chains may contain fixed interiors. Write z=N(U).

For every attainable count vector z, define

```text
P_z(x,y) = sum_{U : N(U)=z}
           x^o (1-x)^(O-o) y^e (1-y)^(E-e).
```

This is a finite probability-generating family for the joint count vector,
not a quantum amplitude, a generating function in z, or a new physical law.
All subsets U, including zero-probability outcomes at selected boundaries,
enter its definition. Attainable atoms are sorted lexicographically and never
dropped merely because one evaluation vanishes.

### Contract 1: degree, normalization and positivity

Every P_z has integer monomial coefficients and bidegree at most (O,E),
hence at most (3,3) in this gate. Expand each factor with the binomial theorem.
Summing over all subsets gives
`(x+(1-x))^O (y+(1-y))^E = 1`, coefficientwise.
Every subset term is nonnegative on the closed square. Signed monomial
coefficients do not signify negative probabilities. Every attainable atom is
strictly positive in the open square; some disappear at its boundary.
A coefficient table is padded to 4 by 4 even for smaller O or E.

### Contract 2: means and color-graded chains

Let D[q,o,e] count chains in S having exactly o eligible odd and e eligible
even internal vertices. Fixed interiors contribute to q but not to o or e.
A chain survives iff all its eligible members survive, so linearity gives

```text
M_q(x,y) = E[N_q(U)] = sum_{o,e} D[q,o,e] x^o y^e
         = sum_z z_q P_z(x,y).
```

Consequently equality of all mean polynomials on a square with interior is
equivalent to equality of D: a polynomial vanishing on an open rectangle has
all coefficients zero (apply the one-variable root bound successively).
Equal complete laws imply equal means, not conversely. Any fixed linear
functional of these four counts has the corresponding linear combination of
M_q as its expectation; no normalization or estimator access is implied.

### Contract 3: exact polynomial equality and interpolation

For this declared degree bound, equality of every coefficient, equality
throughout [0,1]^2, and equality at every point in
`{0,1/3,2/3,1} x {0,1/3,2/3,1}` are equivalent. At each fixed y node the
difference has four x roots and degree at most three; its x coefficients
then have four y roots and degree at most three. Therefore all are zero.
This justifies the independent exact rational interpolation route. It is
not an empirical grid-coverage assumption. The one-variable interpolation
identity is standard; see [NIST DLMF, Lagrange interpolation](https://dlmf.nist.gov/3.3.i).
Tensorization and this gate's degree bound are the explicit arguments above.

The higher-degree diagnostic
`g(x)=x(x-1/3)(x-2/3)(x-1)` vanishes at every grid point but is 1/144 at
x=1/2. It is deliberately outside the degree contract, not a poset law.
It prevents treating an arbitrary finite grid as a universal certificate.

### Contract 4: correlated law as a corner mixture

The H block_coin policy flips one fair shared coin for the entire eligible
odd block and another independent fair coin for the even block. Its count
law is exactly

```text
P_block(z) = (P_z(0,0)+P_z(1,0)+P_z(0,1)+P_z(1,1))/4.
```

Each corner is a deterministic observation. D determines its deterministic
count vector by evaluating M at that corner; therefore D also determines
this particular correlated law. Duplicate corner atoms coalesce when a
color is absent. This is a mixture of laws, not evaluation at (1/2,1/2),
and not a theorem for arbitrary dependence or arbitrary observation laws.

### Contract 5: selected-rate agreement is insufficient in general

In addition to realizable order counterexamples below, retain a clearly
separated algebraic diagnostic on two abstract atoms. Compare the constant
law (1/2,1/2) with `(1/2+h/4,1/2-h/4)`, where

```text
h(x,y)=x(1-x)(2y-1)(3y-2).
```

It has bidegree (2,2); |h|<=1/2 on the square, so both components lie in
[3/8,5/8] and sum to one. The laws agree at H's IID points (1/2,1/2),
(1/3,2/3), and at all four corners, but differ by 1/48 in the first atom at
(1/2,1/3). These rational-coefficient abstract laws are NOT claimed to be
realizable induced-order count laws in this gate. They demonstrate why any
observed H/I partition coincidence must retain its bounded-domain qualifier.

## Frozen finite universe

IDs 0..7, density metadata 12. Fixed probes 0,7 bound every interior.
Write a_i=i+1 and b_j=j+4, i,j=0..2. ferrers6 has a_i<b_j iff i<=j;
standard_example3 has a_i<b_j iff i!=j; chain6 is the total order.
ferrers6_fixed uses the Ferrers order but fixed vertices [0,3,7].
All other cases fix [0,7]. Eligible vertices are increasing IDs 1..6
excluding fixed interiors. Every supplied relation is its transitive past.

Cases in exact order:

1. ferrers6 / independent
2. ferrers6 / parity_adaptive
3. ferrers6 / common_coin
4. ferrers6 / parity_hole
5. ferrers6 / first_pair
6. standard_example3 / independent
7. chain6 / parity_adaptive
8. chain6 / parity_hole
9. chain6 / first_pair
10. ferrers6_fixed / independent

A mask bit j denotes eligible[j]. Intermediate mask S runs in increasing
order. Its first-stage probability is 2^-M except first_pair, uniform over
size-two masks with mass 1/binom(M,2), zero otherwise. Current final mask T
runs through all subsets of S in increasing numeric order. Its conditional
law is independent thinning at 1/2 for independent/first_pair, rate 1/3
for even |S| and 2/3 for odd |S| under parity_adaptive, rate 1 for even |S|
and 0 for odd |S| under parity_hole, or fair all/none under common_coin.
At empty S the two common-coin outcomes coalesce to mass one.
The current policy token is that rate, or 1/2 for common_coin.

This reproduces H's 608 intermediate states (510 first-stage-positive),
6,804 histories (3,534 joint-positive, 3,270 zero), and 6,804 possible
repeat observations (case,S,U). History IDs follow case,S,T increasing
order, including zeros. Never expand triples (S,T,U).
Positive history classes alone are used for sufficiency. Zero states remain
diagnostics with declared conditional laws, not source-supported evidence.

The public base is `[context,T kept,T local past]`, where
`context=[current design,"12",fixed IDs,eligible IDs]`. Hidden source/profile
names are audit metadata, never partition-key fields. Per-case masses
normalize to one. Pooled class masses sum to ten: no source or policy prior.

## Summaries and partitions

Retain H's 12 candidate keys and memberships exactly. Append to the public
base: final_only nothing; policy_token [r]; tagged_policy [r,tag];
counts_policy [r,N(S)]; graded_policy [r,C]; tagged_graded [r,C,tag];
unmarked_order [r,unmarked code]; marked_order [r,marked code];
full_record [S kept,S local past]; color_graded [r,D];
block_order [r,anonymous block code]; color_order [r,color code].
Here tag is whether eligible[0] belongs to S and C[q,k]=sum_{o+e=k}D[q,o,e].

Canonical codes anchor fixed vertices individually in increasing order then
permute all remaining vertices. Relation code is
sum_{v_i precedes v_j} 2^(i*n+j). Unmarked order deliberately anchors only
0,7, forgetting a fixed interior mark. Plain code is [n,min relation].
Colored code minimizes lexicographically (relation,color bits), with
color bits sum_i 2^i over eligible odd vertices; output [n,relation,color].
Anonymous block code replaces color bits by sum_{i<j, same eligible parity}
2^(i*n+j), allowing exchange of block names. Fixed vertices never receive
a color/block decoration.

Two new targets: analytic_means uses the four padded mean coefficient
tables; analytic_counts uses the sorted list of count atoms and padded
integer polynomial coefficients. Target key is [base,signature].
Class IDs follow first positive occurrence. Store exact member IDs and mass,
the 12x12 and 2x2 refinement matrices, and all 24 candidate/target assessments.
A refinement row A, column B means A finer than B. A failed assessment retains
the first collision in increasing history order against the first class
representative, plus the common-refinement class count.

Equality of analytic_means and the color_graded candidate is expected here:
D's q=1 row recovers |S| and hence the current token from the public design.
The runner must nevertheless verify actual memberships. Full-law outcomes
are measured, not prescribed. Compare both analytic target memberships with
all eight pinned H targets, in both directions, recording first collisions
and common-refinement sizes. Do not infer equality merely from class counts.

## Exact executor interface and wire schema

Input must be exactly the native dict
`{"schema_version":"det8-qr05i-problem-v1","family":"qr05h_two_color"}`.
Unknown keys, wrong values, subclasses, bool/int substitutions, or coercions
are rejected normally and under -O. Entry point: analyze(problem).
Executors perform no filesystem I/O, import no previous executors, and do not
read retained artifacts or one another. Python standard library only.

Output uses H's analysis schema, with targets replaced by the two above.
Case fields unchanged, including stage1_inclusions. State fields unchanged
EXCEPT predictions and transports are removed and these are added:

```text
color_sizes: [O,E]
count_polynomials: [{"counts":[N0,N1,N2,N3],
                     "coefficients":[[integer c00,...,c03],...,[c30,...,c33]]}, ...]
mean_polynomials: [4x4 integer table for each q=0..3]
```

Observations keep mask, kept, local past, chain_counts. All attainable atoms
occur once sorted lexicographically; no identically zero polynomial entries.
Array indices are powers x first, y second. All 16 cells retained.
Signatures directly use mean_polynomials or count_polynomials.
History and partition/assessment fields are unchanged except the target names.
Analysis counts have exactly: cases,states,positive_states,observations,
histories,positive_histories,zero_histories,candidates,targets,polynomial_atoms,
polynomial_coefficient_cells,mean_coefficient_cells.
Last two totals equal atoms*16 and states*4*16.
Fractions are reduced strings including "0" and "1"; counts, IDs and
coefficients are native ints; flags native bool; zeros have null class IDs.
Native dict/list only, string keys, no floats, tuple or Fraction coercions
in retained evidence. Maximum exact component size 4096 bits.

## Runner, controls and pinned bridge

The runner audits all coefficient normalization and weighted-count mean
identities, color degree bounds, D=C grading, atom enumeration, and direct
subset-law agreement at all 16 interpolation points plus the two H IID
points and held-out (2/5,3/7), (1/5,4/5), (1/2,1/3), (0,2/5), (3/7,1).
These are 22 distinct points: H's (1/3,2/3) is already a grid node.
Reconstruct all H IID and block-coin predictions
from the polynomials, including coefficient means with H's fixed factors
(-1)^q/(2^(q+1)12^q). Independently reconstruct H's labeled probability
vectors from the supplied policies, not from coarse count polynomials.
Match H's source/frame/state/observation/history and
candidate identities; H transports remain pinned prior evidence, not rerun.
All 13 earlier artifact hashes are verified before and after computation.

Retain controls from case0 with final mask0 and positive history mass:
singleton masks1 vs2 (color distinguishes equal marked orders);
antichain masks5 vs3 (equal IID-half law but different block law);
star mask57 vs path27 (equal D/mean polynomials, unequal count polynomials,
same block law). Retain the fixed-interior case9 and an absent-color state.
Boundary control uses case0 mask5: its two odd vertices give an interior
N1=1 atom that disappears at x=0,1 and under block_coin.
Retain the two algebraic diagnostics above with explicit non-poset labels.

## Evidence lifecycle and limits

Before capture, finish tests, review and formatting; freeze README, the two
executors, runner and two test files in a byte/hash ledger. results.json is
created once using exclusive creation, canonical exact JSON and readback.
Replay checks the complete suite and never writes the artifact. Run isolated
Python with a fresh external bytecode cache, normally and with -O.
Lifecycle tests mutate only temporary stub evidence. RESULTS.md and the
roadmap are human-readable reports outside the frozen source ledger.

This gate concerns classical finite conditional observation laws on supplied
orders. It constructs no quantum channel, metric, gravity dynamics, continuum
limit, empirical apparatus model, RET integration or universal minimal summary.
Its practical value is a precise rate-portable prediction contract and a small
candidate for later formalization. Neither Lean nor a physical bridge begins
here. Next-gate selection is made only after this result is known.
