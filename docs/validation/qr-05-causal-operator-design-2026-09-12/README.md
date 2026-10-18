# QR-05: finite causal-operator and signed-path contract

12 September 2026. **Analytical design only.** No new mathematical executor,
fixture enumeration, unit-test suite, simulation or acquisition runs in this
gate. The prospective verification below is not yet implemented or executed.

This standalone finite calculus requires no DET ontology or physical law.
It follows the [joint geometric-channel verification](../qr-05-joint-geometry-verification-2026-09-12/RESULTS.md)
and repairs the [branch audit's support/inverse implications](../qr-05-bridge-reconciliation-2026-09-12/README.md).
The distinction is between a supplied order, a chosen response operator, and
what a specified observed matrix could actually identify.

## 1. Objects, indexing and what is supplied

Let E={0,...,n−1}, n≥1, be a finite labelled set with a strict partial order ≺.
Labels need NOT be in topological order. Define the complete relation matrix
and cover matrix by

```text
C_ij = 1 iff j ≺ i; otherwise 0.
L_ij = 1 iff j ≺ i and no k satisfies j ≺ k ≺ i; otherwise 0.
```

Rows receive, columns send: a nonzero entry at (i,j) acts from j to i.
C is irreflexive and transitive; L generally is not transitive. Supplying an
acyclic adjacency matrix in place of C is not the same input. In particular,
the three-chain has C_20=1 but L_20=0.

A world is (C,A,d), where A is a rational matrix satisfying A_ij=0 whenever
C_ij=0, and d is a positive rational. A may have signed entries and may assign
zero weight to an allowed relation. Define

```text
M = d I − A,
G = M^(-1),
Δ = G − G^T.
```

All quantities in this finite contract are dimensionless. M is a *chosen*
matrix, G its algebraic response, and Δ its antisymmetric part. None is yet
a physical wave operator, propagator, measured response or quantum channel.
An input C is not a causal relation inferred by this construction.

Ordinary transpose uses the counting-coordinate inner product. If a later
model supplies a positive measure matrix W, its adjoint is W^(-1)G^T W,
not automatically G^T. No physical advanced operator, conservation measure,
boundary condition or source normalization is inferred from this transpose.

## 2. Exact inverse and all-path expansion

A topological permutation makes A strictly triangular; equivalently any
nonzero matrix-product term follows a strict chain. No such chain has n
edges, so A^n=0. Consequently

```text
G = sum(k=0,...,n−1) A^k / d^(k+1).
M G = G M = I,          G_ii = 1/d.
```

Multiplying the finite sum by dI−A telescopes, leaving I−A^n/d^n=I.
This is a finite polynomial identity: no small-weight, norm, convergence or
infinite-series assumption is needed.

For i≠j, each entry is the sum over ALL strict chains
j=x_0 ≺ x_1 ≺ ... ≺ x_k=i, k≥1, of

`A_(x_k,x_(k−1)) ... A_(x_1,x_0) / d^(k+1)`.

An edge may be any comparable pair, not only a cover. Paths with a zero
weight contribute zero. A path sum restricted to L would be a different
operator unless A itself were supported only on L.

**Unconditional containment:** G_ij≠0 for i≠j implies C_ij=1.
The converse is false with zero weights or signed cancellation. Support of
Δ is contained in C ∪ C^T, but containment is not equality or a sign rule.

## 3. Constructive result: reachability survives signed cancellation

For any matrix X define S(X)_ij=1 iff i≠j and X_ij≠0. Let TC be the strict
transitive closure of this directed support. All closures below are acyclic.
Then, for every world in section 1,

`TC(S(G)) = TC(S(A)) ⊆ C`.

Proof: the path expansion puts each nonzero off-diagonal G entry in the
reachability of A. Conversely set N=G−I/d. It is strict-order-supported and
nilpotent, and the inverse finite series gives

`A = d² N − d³ N² + ... + (−1)^n d^n N^(n−1)`.

Thus every nonzero A entry also has a path through nonzero N entries.
Taking transitive closures in both directions gives the equality. For n=1
the sums are empty and both supports are empty.

At a cover j≺i, no path of length≥2 can connect j to i. Hence

`G_ij = A_ij / d²` on every cover.

This yields a precise recovery theorem, including signed weights:

```text
TC(S(G)) = C
    iff every cover of C has nonzero A weight.
```

If all covers are nonzero, they survive in G and a saturated cover chain
connects every comparable pair. Conversely, a missing cover cannot be
replaced by a longer path inside C: such a path would contradict coverhood.

The premise concerns the admitted world class. It cannot be certified as a
statement about an unknown latent C merely by observing G. The theorem also
does not create new information: A's directed support has the same closure.
What it shows is that conversion to G preserves this reachability even when
individual noncover responses cancel.

## 4. Stronger pointwise support and sign recovery need positivity

Restrict now to A≥0 entrywise, including all noncover weights. Then

```text
[G_ij > 0 iff C_ij=1, for all i≠j]
    iff every cover weight is strictly positive.
```

Necessity is the cover identity. Sufficiency follows from a positive saturated
cover path and the absence of negative terms. Under BOTH A≥0 and strictly
positive weights on every cover,

`Δ_ij > 0 iff j≺i`, and `Δ_ij < 0 iff i≺j`.

Both Δ entries vanish for incomparable pairs. These signs follow the receiving-
row convention. Positive covers ALONE do not ensure pointwise equality if
negative noncover edges remain allowed, as the audited toy below demonstrates.

| Available assumptions and matrix | Guaranteed order information |
|---|---|
| Arbitrary supported signed A, full G | Same directed reachability as A; containment in C |
| Every cover nonzero, full G | C from TC(S(G)), despite noncover cancellation |
| A≥0 and every cover positive, Δ | C directly from the sign of Δ |
| Every cover nonzero, signed A, Δ alone | No general orientation or order identification |

These are exact information statements, not noise-robust decision rules.
An arbitrarily small nonzero cover has no uniform detection margin merely
because it is nonzero; no stable threshold or calibrated inverse is supplied.

## 5. Exact witnesses and information limits

### 5.1 Preserve the audited toy without changing its name or sign

On 0≺1≺2 take A_10=A_21=3, A_20=−3, d=a>0. The earlier binomial-layer toy
used H=−aI+A. Our convention gives M=−H, therefore G=−H^(-1), not H^(-1).

```text
G_10 = G_21 = 3/a²,
G_20 = −3/a² + 9/a³ = 3(3−a)/a³.
```

At a=3, G_20=0 exactly. At a=5, G_10=G_21=3/25 but G_20=−6/125.
For receiving-oriented pairs these are also the corresponding Δ entries.
The old convention has the opposite whole G and Δ; its upper entries were
Δ_old,01=3/25 and Δ_old,02=−6/125. These are consistent, not conflicting
calculations. In both cases the nonzero adjacent responses still recover
the entire chain by reachability.

These are the actual finite toy coefficients, not a Benincasa–Dowker or
Klein–Gordon identification. Exact cancellation is not relabeled noise.

### 5.2 Cancellation can occur using covers only

For the diamond 0≺1≺3 and 0≺2≺3, include 0≺3 in C and set
A_10=A_20=A_31=1, A_32=−1, with all other A entries zero. The two cover paths
give G_30=(1−1)/d³=0. Every cover remains nonzero; TC(S(G)) is the full
diamond. By contrast unit positive weights on these four covers give
G_30=2/d³. The absent direct A_30 does not prevent a nonzero inverse entry.

### 5.3 Full G recovers its matrix, but may not recover invisible relations

Within this class full G, including its diagonal and specified basis and
normalization, determines d=1/G_ii and A=dI−G^(-1). It determines TC(S(A)),
but need not determine additional latent relations outside that closure
without an extra world-class premise. A zero-weight noncover can still be
forced by a nonzero path and transitivity; zero weight alone does not imply
that a relation is invisible.

For d=1, the three-chain 0≺1≺2 and the order containing only 0≺1, with event
2 isolated, both permit A_10=1 and all other entries zero. They have identical
G=I+A and identical nonzero Δ but nonisomorphic orders. The chain's cover
1≺2 was assigned zero weight. This is why the nonzero-cover premise matters.

### 5.4 Δ can lose orientation even when every cover is nonzero

With d=1, a two-event forward order with A_10=1 gives
G=[[1,0],[1,1]]. The reversed order with A_01=−1 gives
G'=[[1,−1],[0,1]]. Both have
Δ=[[0,−1],[1,0]], although their labelled orientations differ.

There is also a nonisomorphic-order example, not just a reversal of labels:

```text
V order: 0≺1 and 0≺2          Chain order: 1≺0≺2

A_V = [0  0  0]              A_C = [0 −1  0]
      [1  0  0]                    [0  0  0]
      [1  0  0]                    [1  1  0]

G_V = [1  0  0]              G_C = [1 −1  0]
      [1  1  0]                    [0  1  0]
      [1  0  1]                    [1  0  1]

Both: Δ = [0 −1 −1]
          [1  0  0]
          [1  0  0].
```

For the chain, (A_C²)_21=−1 cancels (A_C)_21=1. All respective cover weights
are nonzero, so full G recovers each order by reachability, but Δ cannot
distinguish them. Any common deterministic function of Δ retains this
collision; taking a spectral function is not a source of missing information.

A *supplied compatible linear extension* changes the interface. It tells us
which triangular side receives. Δ then determines G's off-diagonal entries;
if d is also supplied, diag(G)=1/d completes G. With nonzero covers the
off-diagonal support already recovers C. None of these counterexamples says
Δ must remain ambiguous after that extra information is supplied. Nor does
Δ alone determine the scalar diagonal: on a two-event chain A_10=d² gives
the same Δ for every d>0.

## 6. Relabeling, reversal and normalization

For a permutation matrix P, relabel the whole world by
C'=PCP^T, A'=PAP^T, d'=d. Then M',G',Δ' are the same conjugates of M,G,Δ;
the cover and reachability relations transform identically. Do not silently
sort labels and leave output coordinates in a different basis.

Fixed-label order reversal is C'=C^T and A'=A^T, with d'=d. It gives
G'=G^T and Δ'=−Δ. Reversing C while retaining a generally unsupported A is
not this operation. Relabeling and active order reversal are distinct controls.

For a positive rational c, set d'=cd and A'=cA, keeping C fixed. Then
M'=cM, G'=G/c and Δ'=Δ/c. Support and reachability do not change. Thus
support-only observations do not fix the absolute response normalization;
a specified amplitude basis/scale would be extra information. This does not
identify d with the metric scale or sampling reference in the previous model.

## 7. Connection to the joint geometric-channel calculus

If a chosen operator is K(w)=F(Y(w)) for an observed channel Y on a common
world class, equal Y values give equal K values. An injective F preserves
fibers; otherwise it can only merge them. Common randomized or quantum
postprocessing likewise preserves equal input laws.

Therefore choosing an operator only from O,P,T cannot split the previous
four-world geometry collision. Using hidden conformal/scale coordinates or
proper-volume weights introduces additional inputs, not a recovery from
those observations. O there contains two marked comparisons, not an arbitrary
full relation C. A finite supplied C here must not be silently substituted
for an available experimental channel there.

The useful bridge is methodological: exact response/path identities can
separate absent paths, zero couplings and cancellation, and can state when
an ideal directed response preserves order. Physical response measurement,
stable noisy inversion, density/scale metrology and operator selection still
need their own contracts. An antisymmetric real matrix is not by itself a
quantum instrument, state or complete physical dynamics.

## 8. Prospective bounded verification: one fixed study

The next gate will implement this finite calculus, not a physical operator.
Use these THIRTEEN base cases. All unspecified A entries are zero, d=1 unless
specified, and every listed order is its full transitive closure. Unit covers
means A=L. In the edge notation j→i means j≺i.

| ID | n; order | A; d |
|---|---|---|
| singleton | 1; no pairs | A=0 |
| antichain | 3; no pairs | A=0 |
| chain | 3; 0→1→2 | Unit covers |
| fork | 3; 0→1,0→2 | Unit covers |
| diamond | 4; 0→1→3,0→2→3 | Unit covers |
| missing_cover | 3; 0→1→2 | A_10=1 only |
| single_edge | 3; 0→1, with 2 isolated | A_10=1 only |
| signed_diamond | 4; same diamond | A_10=A_20=A_31=1,A_32=−1 |
| toy_cancel | 3; 0→1→2 | A_10=A_21=3,A_20=−3; d=3 |
| toy_sign | 3; 0→1→2 | Same A; d=5 |
| forward_pair | 2; 0→1 | A_10=1 |
| reversed_signed_pair | 2; 1→0 | A_01=−1 |
| signed_relabelled_chain | 3; 1→0→2 | A_01=−1,A_20=A_21=1 |

Apply four separate variants to EACH base, in this order: identity; cyclic
relabeling old i→(i+1) mod n; order reversal; positive rescaling c=3/2.
Do not compose them, fit parameters, deduplicate symmetric cases or sweep
further fixtures. This specifies 52 labelled rows, not 52 independent trials.

The analytically specified census is 148 event occurrences and 452 cells per
reported matrix across the 52 rows. C has 120 strict pairs and 92 covers;
A and off-diagonal G each have 100 nonzero entries in total. Reachability
equals C in 48 rows, while direct support equals C in 36. Only missing_cover
fails reachability; direct equality also fails in signed_diamond, toy_cancel
and signed_relabelled_chain. These expected counts are not executed results.

### Inputs and full report obligations

Freeze a machine-readable protocol and complete API/report schema BEFORE
execution. The pure evaluator should accept a plain dict {C,A,d}: plain square
list matrices with 1≤n≤4, C entries plain int0/1 and A,d plain Fractions with
absolute-numerator/denominator bit lengths≤128, d>0. Reject bool/float/coercion, subclasses,
shape mismatch, diagonal/reflexive/cyclic/nontransitive C and A outside C.
Accept non-topological labellings; do not repair invalid inputs by closure.
No mutation, aliased mutable inputs, I/O or random state belongs in the engine.
The fixed theorem and n bound suffice without an arbitrary output-rational
cutoff; source/report byte and time bounds still apply to the study artifacts.

Preserve for every row: the complete world; C and L; A powers through A^n;
M; G; Δ; BOTH inverse products; and every strict causal chain with its ordered
label sequence, edge weights and exact weighted contribution. Include all
one-event paths (k=0, empty edge list, contribution 1/d) and paths with zero
contribution. There are 304 path records: 148 trivial, 120 one-edge and 36
two-edge paths; 24 records have zero contribution. Retain S(A), S(G), both transitive
closures, all cover-entry identities and complete support-difference witnesses.
Report direct-support equality, nonzero-cover status, entrywise nonnegativity
and reachability equality separately, never as one success flag. Keep the
same-G and same-Δ witness pairs with their distinct target relation matrices.

One route should build the finite power sum; the independent route should
invert M by exact elimination and separately enumerate paths. Compare every
native rational matrix and witness before serialization. Tests must check
the analytical entries above, both inverse products, all three transformation
laws and arbitrary labels. Derive support channels only from their matrix
entries; case IDs and target C cannot be smuggled into a channel encoding.

### Evidence and scope boundary

Bind this design and its decision record, the exact protocol, both independent
implementations, tests, driver and any literal-hash-pinned evidence helpers
before the first new mathematical run. The executor must use authenticated
source bytes, preserve native Fraction/int/bool distinctions, bind freeze
identities to the capture, recheck inputs after execution and publish
exclusively with readback. Do not import the rejected branch engines.

Use 30 seconds per full study, 60 seconds per suite, 262,144 bytes per source,
16,777,216 bytes per artifact, and one alternate-runtime full replay. The
planned sequence is freeze, first capture, normal/optimized suites and full
replays, then one Python 3.11 full replay. Retain any failure and use a named
repair revision rather than tuning frozen sources after the first execution.

Later physical coefficients, measure/boundary choices, actual divergence-
operator moments, correspondence distortion/noncollapse, uniform bounds,
stochastic growth and empirical calibration remain separate. No RET readiness,
materials/anomaly deployment, new gravitational law, book revival or deferred
clock coupling is established. See the [decision record](RESULTS.md).
