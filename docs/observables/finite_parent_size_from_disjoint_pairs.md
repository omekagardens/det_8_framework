# Finite parent geometry under uniform sampling without replacement

**Decision.** The accepted native pair moments allow at most eight exchangeable disjoint pair flags for every source mixture. A uniformly sampled fixed-size parent must therefore have $N\le17$. This bound is sharp for the abstract pair-flag diagnostic; existence of a transitive 17-event parent order is not established. The accepted native four-event ensemble supplies a genuine $N=4$ order reference.

Reuse exactly the accepted empty-prepared, original-fair-mark, four-birth moments for the actual source $\rho(x)=(x,1-x)$, $0\le x\le1$. Define
$$
 k=\frac{8449-2x}{8448},\qquad
 \frac{8447}{8448}\le k\le\frac{8449}{8448},\qquad
 P=\frac{5839}{7920},\quad D=\frac{205}{396}.
$$
Then the donor probabilities are
$$
 p=\Pr(Y_1=1)=\Pr(Y_2=1)=kP,\qquad
 d=\Pr(Y_1=Y_2=1)=kD,                         \tag{1}
$$
with $d-p^2<0$ throughout this interval. These moments already include every native history and original mark. No new growth coefficient, prepared prefix, cardinality case of the native law or four-event enumeration is introduced.

## Why a finite parent requires an exchangeable block

Put $b=\lfloor N/2\rfloor$. On a hypothetical parent order, choose one uniform random permutation of all $N$ vertices and pair its first $2b$ vertices consecutively. Let $Y_1,\ldots,Y_b$ be the corresponding binary comparability flags.

Permuting the pair blocks is a permutation of the vertex permutation, so these flags are exchangeable conditional on each fixed parent. Any mixture of parent orders preserves exchangeability. Their first pair is a uniform unordered pair. Their first two pairs involve a uniform four-element subset: among its 24 internal permutations, each of the three unordered perfect matchings has eight permutations, and the two pair orders are fair. Thus their first two flags have exactly the registered four-sample matching law. Symmetry of the pair reader removes within-pair orientation, and the independent identical pair-noise contract preserves the argument.

Consequently any proposed parent model at fixed $N$, even with an arbitrary trial-random order, must admit an exchangeable binary block of length $b$ whose distinct one- and two-flag moments are $p,d$ in (1). These are hypothetical consistency marginals of the registered parent model, not additional measured events or physical operations.

Let the integer total be
$$
 K=\sum_{j=1}^bY_j\in\{0,1,\ldots,b\}.
$$
Exchangeability gives
$$
 \mu:=\mathbb E K=bp,\qquad
 F:=\mathbb E[K(K-1)]=b(b-1)d,                 \tag{2}
$$
and
$$
 \operatorname{Var}(K)=bp(1-p)+b(b-1)(d-p^2).  \tag{3}
$$
The accepted negative covariance can be compatible with a finite block; it cannot remain fixed in magnitude as its exchangeable length grows without limit.

## Finite moment bounds, including integer support

Nonnegative variance alone requires
$$
 d-p^2\ge-\frac{p(1-p)}{b-1},
 \qquad
 b\le\frac{p-d}{p^2-d}\quad(d<p^2,\ b\ge2).    \tag{4}
$$
The right side of the size bound lies strictly between 8 and 9 throughout the donor source interval. Indeed it is
$$
 \frac{P-D}{kP^2-D}
$$
and decreases with $k$; its endpoint range is
$$
 \frac{116353290240}{13736082529}
 \ \le\ \frac{p-d}{p^2-d}\
 \le\ \frac{116353290240}{13667894687},
$$
whose lower endpoint exceeds 8 and whose upper endpoint is below 9. This already excludes length nine, but does not alone certify feasibility at length eight.

Integer support supplies the sharper lower bound. For $j=\lfloor\mu\rfloor$, every integer $K$ satisfies
$$
 (K-j)(K-j-1)\ge0.
$$
Taking expectations yields
$$
 F\ge2j\mu-j(j+1).                            \tag{5}
$$
Writing $r=\mu-j$, the equivalent variance form is
$$
 \operatorname{Var}(K)\ge r(1-r),
$$
or
$$
 d-p^2\ge-\frac{p(1-p)}{b-1}
              +\frac{r(1-r)}{b(b-1)}.         \tag{6}
$$
The upper bound follows from $K(K-1)\le(b-1)K$:
$$
 F\le(b-1)\mu,\quad\text{equivalently }d\le p. \tag{7}
$$

Together with $0\le\mu\le b$, bounds (5) and (7) are also sufficient for the two moments of an abstract integer total. The adjacent-integer distribution on $j,j+1$ with mean $\mu$ attains (5), with degenerate endpoints treated directly. The distribution on $0,b$ with that same mean attains (7). Convexly mixing them preserves the mean and reaches every intervening $F$. Given any such total, choosing a uniform subset of $K$ ones among $b$ positions produces an exchangeable binary block with (2). This is a bit-level result, without a transitive-order representation.

## Exact exclusion of nine flags on the full source interval

For $b=9$, $\mu_9=9kP=5839k/880$ lies strictly between 6 and 7 over the entire source interval, so $j=6$. The required nonnegative integer-support gap is
$$
 G_9:=F_9-12\mu_9+42
     =72kD-108kP+42
     =42-\frac{9317}{220}k.                   \tag{8}
$$
Here $F_9=72kD$. Equivalently,
$$
 G_9=72kD-12(9kP)+42
       =\mathbb E[(K-6)(K-7)]
$$
would have to be nonnegative for an integer total in $\{0,\ldots,9\}$.

In fact, since $k\ge8447/8448$,
$$
 \boxed{G_9\le42-\frac{9317}{220}\frac{8447}{8448}
               =-\frac{5299}{15360}<0.}       \tag{9}
$$
At the equal mixture $k=1$, the gap is $-7/20$; at the other source endpoint it is $-5453/15360$. Thus every admitted mixture violates the integer-support requirement by a uniform positive amount. A length-nine exchangeable flag distribution does not exist.

Every longer exchangeable block would have a length-nine marginal with these same one- and two-flag moments. Therefore all $b\ge9$ are excluded as well. Arbitrary randomness of the parent order at fixed $N$ cannot evade the pointwise nonnegativity of the integer polynomial whose expectation is contradicted in (9).

## Eight flags are feasible as abstract exchangeable bits

For $b=8$,
$$
 \mu_8=8kP=5839k/990\in(5,6),\qquad
 F_8=56kD.
$$
Its integer-support gap is
$$
 G_8=F_8-10\mu_8+30=\frac{2970-2969k}{99},
$$
which satisfies
$$
 \frac{5479}{836352}\le G_8
          \le\frac{11417}{836352}.
$$
It is strictly positive. The upper bound (7) also holds since $D<P$.

An explicit construction avoids relying solely on a bound. Put
$\varepsilon=k-1$, so $|\varepsilon|\le1/8448$, and give the integer total the following law:

| Total $K$ | Probability |
|---|---:|
| 5 | $q_5=(53-10342\varepsilon)/495$ |
| 6 | $q_6=(293+11843\varepsilon)/330$ |
| 7 | $q_7=(1-2969\varepsilon)/198$ |
| all other values in $0,\ldots,8$ | $0$ |

Each probability is strictly positive throughout the interval: $53\cdot8448>10342$, $293\cdot8448>11843$, and $8448>2969$. Their sum is one. Direct substitution gives
$$
 5q_5+6q_6+7q_7=8kP,\qquad
 20q_5+30q_6+42q_7=56kD.                      \tag{10}
$$
For example, at the equal mixture the probabilities are $53/495,\ 293/330,\ 1/198$.

After drawing $K$, choose uniformly which $K$ of the eight flag positions are one. This produces an exchangeable vector satisfying
$$
 \Pr(Y_i=1)=\mathbb E K/8=p,\qquad
 \Pr(Y_i=Y_j=1)=\mathbb E[K(K-1)]/56=d
 \quad(i\ne j).
$$
Thus its entire two-bit marginal is the donor's matched law: masses $d,p-d,p-d,1-2p+d$. Taking smaller flag marginals preserves those moments. This establishes bit-level feasibility for every $2\le b\le8$, not only one favourable source.

Combining (9) and (10), the largest exchangeable block size allowed by this diagnostic is
$$
 \boxed{b_{\max}=8\quad\text{for every }x\in[0,1].} \tag{11}
$$

## Parent size, random orders and the genuine small reference

Since $b=\lfloor N/2\rfloor$, a parent passing the pair-flag diagnostic must satisfy
$$
 \boxed{\lfloor N/2\rfloor\le8,\qquad N\le17.}  \tag{12}
$$
Every fixed-size parent with $N\ge18$ is excluded, including any distribution of transitive orders on that cardinality and any source-conditioned such distribution. The argument applies to its unconditional flag moments; it does not require fixing one order across trials.

The abstract length-eight construction means that this particular diagnostic cannot lower the bound below $N=17$. It does not assign pair relations on the complete vertex set of a 16- or 17-event order, enforce their transitivity, or reproduce all induced four-event order probabilities. An exchangeable binary sequence is less constrained than the comparability matrix of a causal order. No actual $N=17$ parent is constructed or certified, and no largest realizable order cardinality inside $[4,17]$ is decided.

There is a genuine small-order reference at $N=4$: draw the four-event parent order from the accepted native terminal-order ensemble for the declared source, sample its four distinct vertices uniformly, and apply the same matching. Sampling all four vertices leaves the parent order unchanged, so this reproduces the donor's whole four-event law and its two pair bits. This uses the already supplied four-birth ensemble, with parent orders allowed to vary across trials; it neither invents native growth beyond four events nor proves a single fixed four-order suffices.

The resulting distinction is precise: an arbitrarily large fixed-cardinality parent is ruled out under the uniform registration; eight abstract disjoint pair flags are attainable; a genuine order ensemble is supplied at four vertices; larger-order representability remains unproved within the permitted size range.

## Observation-scale meaning and limits

Uniform sampling without replacement can cause negative disjoint-pair covariance. The accepted negative covariance is too large in magnitude to arise from an arbitrarily large parent under this registration. If the record is a uniform four-event observation of any fixed-size parent meeting these assumptions, it samples at least $4/17$ of that parent's vertex inventory. This is an event-count fraction, not proper volume, physical length, curvature, dimension, mass or a continuum limit.

The size exclusion depends on uniform selection of four distinct vertices from one parent, unchanged induced relations, the same source-conditioned population moments, symmetric pair readout and its independent-noise contract, and consistency of those observations with the hypothetical disjoint-pair construction on the whole parent. Nonuniform or order-selected acceptance, altered/missing relations, nonshared or correlated readout errors, or loss of that parent-sampling registration changes the question. The fixed-$N$ hypothesis is essential; a population with unregistered varying parent cardinalities is outside this certificate. No alternative instrument or mechanism is selected or calibrated here.

The hypothetical permutation is a consistency argument, not an instruction to measure more events. Access to the full parent and unbiased selection from its entire vertex inventory remain registration premises. This report supplies no physical reader, calibrated source, empirical variance estimate, repetition law, cost advantage or gravitational interpretation.


The [four-event disjoint-pair result](disjoint_pairs_in_four_native_events.md) supplies the native population probabilities used here.
