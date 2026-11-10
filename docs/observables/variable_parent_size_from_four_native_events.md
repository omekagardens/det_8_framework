# What a four-event record implies about the size of its parent order

**Decision.** The prescribed native four-event population cannot be a uniform induced observation from any population supported entirely on finite parents with $N\ge9$, even with arbitrary trial-to-trial variation of parent size, order and edge density. A valid all-source lower bound is
$$
 \Pr(4\le N\le8)\ge
 \frac{1492565-62122x}{40144896}
 \ge\frac{1430443}{40144896}>0.
$$
This is a trial-fraction bound, not a bound on every parent's size or a spacetime-volume inference. The nearest smaller eight-vertex total-edge moment test passes, without certifying an order extension.

## 1. Observation contract

Retain the original complete empty-prepared four-birth population, fair reference marks, every history and the actual two-state source $\rho(x)=(x,1-x)$, $0\le x\le1$. The readout is the exact unlabelled induced order, with its six comparable/incomparable pair relations read consistently. Birth ranks and marks are not retained features. Both comparisons have the same complete-order information, sampling access, registration and cost contract.

A hypothetical trial draws one finite partial order with $N\ge4$ vertices under an arbitrary trial law. The law may vary in cardinality and edge density, including conditional on source. Conditional on that parent, four distinct vertices are selected uniformly and independently of relations, and their unmodified induced order is returned. Trial weights are not reweighted by $N$, by the number of four-subsets, or by their observed order. Hypothetical extra subsampling below is a mathematical coupling, not a request to measure more events.

This assignment uses the complete order and its overlap information. The earlier two matched disjoint flags alone supplied $p,d$, not the new shared-edge moment. No detector implementation, repetition independence, empirical uncertainty or physical correspondence is inferred from the exact population law.

## 2. Edge, overlapping-edge and disjoint-edge moments

Temporarily give the four sampled vertices uniform random names $1,2,3,4$, solely for an invariant calculation. Let $X_{ij}$ be one when vertices $i,j$ are comparable, including transitive relations, and zero otherwise. Define
$$
 p=\mathbb E X_{12},\qquad
 a=\mathbb E[X_{12}X_{13}],\qquad
 d=\mathbb E[X_{12}X_{34}].                    \tag{1}
$$
The shared edge $X_{12}$ denotes the same relation in each subrecord; it is not resampled.

For a realized four-order, let $m$ be its comparable-edge count and $t$ its count of perfect matchings with both constituent edges comparable. Among the $\binom m2$ unordered pairs of successful edges, exactly $t$ are disjoint. Therefore
$$
 w=\binom m2-t
$$
counts successful unordered overlapping edge pairs. There are 6 possible edges, 12 possible overlapping edge pairs, and 3 possible disjoint edge pairs. Hence
$$
       p=\mathbb E[m]/6,\quad
       a=\mathbb E[w]/12,\quad
       d=\mathbb E[t]/3.                       \tag{2}
$$
This adds no birth labels or rooted observation and requires no order-isomorphism enumeration.

The accepted ten reference blocks can be written with one denominator, 2640:

| $(m,t)$ | $w=\binom m2-t$ | Reference probability numerator |
|---|---:|---:|
| $(0,0)$ | 0 | 10 |
| $(1,0)$ | 0 | 24 |
| $(2,0)$ | 1 | 108 |
| $(2,1)$ | 0 | 12 |
| $(3,0)$ | 3 | 401 |
| $(3,1)$ | 2 | 110 |
| $(4,1)$ | 5 | 423 |
| $(4,2)$ | 4 | 22 |
| $(5,2)$ | 8 | 1079 |
| $(6,3)$ | 12 | 451 |

The numerator sum is 2640. The weighted sums of $m,t,w$ have numerators respectively $11678,4100,17778$ over 2640. In particular
$$
 \mathbb E_{\rm ref}w
 =\frac{108+1203+220+2115+88+8632+5412}{2640}
 =\frac{2963}{440}.
$$
The complete active law multiplies every non-antichain block by
$$
               k(x)=\frac{8449-2x}{8448},
 \qquad 8447/8448\le k\le8449/8448.
$$
The antichain has its own retained positive probability, and $m=t=w=0$ there. Thus all three moments, with full original multiplicities, are
$$
 \boxed{p=k\,\frac{5839}{7920},\qquad
        a=k\,\frac{2963}{5280},\qquad
        d=k\,\frac{205}{396}.}                 \tag{3}
$$
There is no conditioning away of the antichain or any other trial.

## 3. A coupling valid for arbitrary parent sizes above a threshold

Suppose initially that every trial has $N\ge n$, for one fixed $n$. Conditional on its parent, choose a uniform $n$-vertex subset and then a uniform four-subset of that subset. The resulting four-subset is uniform in the original parent: every four-subset is contained in the same number of $n$-subsets. This holds separately at each $N$ and preserves the original arbitrary trial weights.

Randomly label the induced $n$-order. Its one-edge, overlapping-edge and disjoint-edge population moments therefore equal (1), unconditionally over all parents and sizes. No assumption that conditional edge probabilities are constant across parents is made.

Let $K_n$ be the integer number of comparable edges in that induced order. It lies in $\{0,\ldots,\binom n2\}$. Counting ordered distinct pairs of edges gives
$$
 \mathbb E K_n=\binom n2p,
$$
$$
 \mathbb E[K_n(K_n-1)]
   =n(n-1)(n-2)\,a+6\binom n4d.               \tag{4}
$$
The first coefficient counts ordered overlapping pairs, the second ordered disjoint pairs. These sum to $\binom n2(\binom n2-1)$. Vertex-exchangeable edge indicators need not be exchangeable as an arbitrary list of edges: the two types in (4) are kept distinct.

For every integer $K$ and every integer $j$,
$$
                     (K-j)(K-j-1)\ge0.        \tag{5}
$$
Writing $\mu=\mathbb E K$ and $F=\mathbb E[K(K-1)]$, this requires
$$
              F-2j\mu+j(j+1)\ge0.
$$
At $j=\lfloor\mu\rfloor$ it is the adjacent-integer lower moment bound. It also holds with one fixed $j$ for mixtures having different conditional means. This last point prevents variable cardinality or edge-density fluctuations from avoiding the test.

## 4. Nine vertices exclude an all-large-parent population

For $n=9$, there are 36 edges, 504 ordered overlapping edge pairs and 756 ordered disjoint edge pairs. Substituting (3) into (4) gives
$$
 \mu_9=36p=\frac{5839k}{220},\qquad
 F_9=504a+756d=\frac{148323k}{220}.
$$
The mean is strictly between 26 and 27 for every admitted source. The necessary integer gap is therefore
$$
 \begin{aligned}
 G_9&:=F_9-52\mu_9+26\cdot27\\
    &=702-\frac{31061}{44}k\\
    &=-\frac{1492565-62122x}{371712}.
 \end{aligned}                                \tag{6}
$$
It is strictly negative throughout the source interval. Explicitly,
$$
 \boxed{G_9\le-\frac{1430443}{371712}<0.}        \tag{7}
$$
At $x=0$ it is $-1492565/371712$, and at the equal source mixture it is $-173/44$.

But (5) would make this same expression
$\mathbb E[(K_9-26)(K_9-27)]\ge0$. This contradiction rules out every trial population supported entirely on $N\ge9$, including arbitrarily varying finite $N$, orders and edge densities. It does not merely rule out one fixed parent cardinality.

The proof uses only a consistent simple comparability graph on each sampled set; transitivity supplies no escape from the integer obstruction. It uses no hypothetical native growth beyond four events and no empirical nine-event acquisition.

## 5. Nearest smaller size: a diagnostic, not representability

For an eight-vertex induced order, there are 28 edges, 336 ordered overlapping pairs and 420 ordered disjoint pairs. The same candidate moments give
$$
 \mu_8=\frac{40873k}{1980}\in(20,21),\qquad
 F_8=\frac{133973k}{330}.
$$
Its adjacent-integer gap is
$$
 G_8=F_8-40\mu_8+20\cdot21
       =420-\frac{415541}{990}k,
$$
and on the full source interval
$$
       G_8\ge\frac{1772491}{8363520}>0.         \tag{8}
$$
The upper support bound also passes:
$$
                 27\mu_8-F_8
                    =\frac{99911}{660}k>0.
$$
With $0<\mu_8<28$, these lower and upper bounds permit an abstract integer edge total on $0,\ldots,28$ with these first two total-count moments. For example, interpolate between a mean-matched adjacent-integer law and a law supported on $0,28$.

This count-level feasibility is not a construction of a graph with the required separate $a,d$, much less a transitive order reproducing the full native four-order law. Thus the eight-vertex diagnostic does not justify claiming an attainable largest parent size. If a parent cardinality were fixed across all trials, (7) now gives the necessary bound $N\le8$ under this complete-order observation. The earlier $N\le17$ result used the weaker disjoint-flag diagnostic; its abstract eight-flag construction did not provide an order extension.

A genuine parent model remains available at $N=4$: draw the accepted native terminal four-order itself and sample all its vertices. This exactly reproduces the entire stipulated record. No larger-order realization is asserted.

## 6. A valid lower bound on the small-parent trial fraction

To include populations having some parents below nine, define a witness on each observed four-order:
$$
 \begin{aligned}
 H(m,t)
  &=702-312m+42w+252t\\
  &=21m^2-333m+210t+702.
 \end{aligned}                                \tag{9}
$$
Equations (2) and (6) give
$$
       \mathbb E H=702-1872p+504a+756d=G_9.
$$
For every particular parent with $N\ge9$, the coupling of section 3 gives
$$
       \mathbb E[H\mid\text{parent}]
          =\mathbb E[(K_9-26)(K_9-27)\mid\text{parent}]
          \ge0.                              \tag{10}
$$
No native moment identity is assumed conditional on that parent.

There is also a uniform lower bound for every possible four-order:
$$
                         H(m,t)\ge-108.       \tag{11}
$$
Here is a proof without enumerating orders or graphs. The six possible edges split into their three disjoint perfect matchings. If $t$ matchings have both edges present, the remaining matchings each have at most one edge, so
$$
                      t\ge\max(0,m-3).
$$
For $0\le m\le3$, use $t\ge0$ in (9); the resulting decreasing quadratic has minimum $-108$ at $m=3$. For $3\le m\le6$, use $t\ge m-3$; the lower quadratic is $21m^2-123m+72$, increasing on this interval, again with minimum $-108$ at $m=3$. A four-order with a root below three incomparable leaves has $m=3,t=0$, so this witness minimum is a genuine small-order value. Its existence does not certify attainability of the full mixture bound.

Let
$$
                         \eta=\Pr(4\le N\le8)
$$
under the same original trial weighting. Splitting by parent size, (10) applies to the large-parent subpopulation and (11) to the small-parent subpopulation. Hence
$$
                         G_9=\mathbb E H\ge-108\eta,
$$
which forces
$$
 \boxed{\eta\ge-\frac{G_9}{108}
     =\frac{1492565-62122x}{40144896}
     \ge\frac{1430443}{40144896}>0.}            \tag{12}
$$
In particular the uniform lower bound is greater than $7/200=3.5\%$. At least that fraction of trials must have parents with at most eight vertices under this registration. On those trials, the four-vertex sample covers at least half the parent's vertex inventory.

This is one valid necessary fraction bound. No optimality or attaining parent population for (12) is claimed. It does not imply that every parent has $N\le8$, bound the largest parent or mean parent size, or establish a compatible arbitrarily large tail. Those extension questions are unresolved by this witness. The trial fraction is neither an event-weighted fraction nor a proper-volume fraction.

## 7. Native units and physical registration

The new decision closes the previously untested all-large variable-size population under the prescribed complete induced-order reader. It allows arbitrary mixing across parent sizes and geometries while requiring uniform four-vertex selection within each parent and consistency of shared edges. A population reweighted by its number of vertices or four-subsets would be a different trial law and would require the fraction statement to be registered anew.

Nonuniform/order-selected sampling, omitted or altered relations, independently regenerated shared-edge reports, a changed preparation or an unqualified readout-error model changes the stipulated observation. No such alternative is fitted here. All native histories, marks, zero-comparability cases and original source weights remain in the calculation; the source coefficient $x$ is not a prior over uncertain preparations.

The coupling and the bound are dimensionless cardinality statements at the declared event scale. They supply no proper area or volume, spacetime dimension, density, curvature, physical clock, gravity coupling, mass calibration, continuum limit or efficiency advantage. The same complete records, processing and costs are available to both comparisons. Exact population statements are not empirical frequency estimates or finite-sample confidence bounds.

[Four-event order law](disjoint_pairs_in_four_native_events.md) · [Fixed-size parent test](finite_parent_size_from_disjoint_pairs.md) · [Comparability and curvature](order_comparability_and_curvature.md)
