# Parameter identification after fixed-size uniform thinning

Historical author status: manual theorem candidate; independent review and coordinator adjudication pending.
Subsequent independent manual review and coordinator adjudication accepted the exact conditional theorem below. Publication preparation and editorial acceptance are separate gates.
Public edition: 22 October 2026.
Execution remains HOLD. This finite distribution theorem does not supply an estimator, calibration, acquisition mechanism or execution permission.

## Public source crosswalk

The source's historical label RI1377 denotes [the finite thinning likelihood](THINNED_ORDER_LIKELIHOOD.md), including the exact survivor-selection channel and three-vertex example. The accepted full-order family and likelihood are in [the Bernoulli-order theorem](BERNOULLI_ORDER_LIKELIHOOD.md). “The accepted auxiliary-seed result” denotes [auxiliary-seed identifiability](AUXILIARY_SEED_IDENTIFIABILITY.md); the height-erasure observation convention is in [the vertex-erasure diagnostic](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md). These are public dependencies, not private custody references. The [package index](THEOREM_PACKAGE.md) and [law-dependence note](LAW_DEPENDENCE.md) retain the wider conditional scope.

The scientific sections below reproduce the source literally. Their historical labels do not require access to private evidence.

## 1. Contract and theorem

Fix known deterministic integers \(N\ge2\) and \(2\le m\le N\).
For each separately fixed \(p\in(0,1)\), generate the accepted from-empty
Bernoulli native order on birth labels \([N]\). Its independent forward-edge
representation has \(E_{ij}\sim\operatorname{Bernoulli}(p)\), mutually
independent for \(i<j\); \(P_N\) is the completed transitive closure.
This optional native family is the premise, not a law selected here by DET.

Conditional on the completed birth-labeled order, choose each actual
\(m\)-subset \(T\subseteq[N]\) with probability \(1/\binom Nm\).
Report the isomorphism class of the faithful completed restriction
\(Q=P_N[T]\), together with \(N,m\). Birth labels, deleted identities,
marks and scalar-passive payload are not observed. Marks and payload remain
underlying model components. This is the accepted RI1377 channel.

For any \(k\)-vertex order \(R\), let \(K(R)\) count unordered comparable
pairs, including comparisons implied by transitivity. It is not the cover
count \(c(R)\) of the likelihood theorem. For \(k\ge2\), define
\[
                         D(R)=\frac{K(R)}{\binom k2}\in[0,1].          \tag{1}
\]
This is intrinsic: relabeling leaves it unchanged. The observer needs only
the reported completed order, not any generating edge or birth label.

Theorem. For every fixed known \(N\ge2\) and every \(2\le m\le N\), the
distribution of the reported order is identifiable in \(p\). More strongly,
the distribution of its intrinsic statistic \(D(Q)\) is identifiable.
Writing \(\mu_N(p)=\mathbb E_p D(P_N)\), one has
\[
                           \mathbb E_p D(Q)=\mu_N(p),                 \tag{2}
\]
and, for \(0<p_1<p_2<1\),
\[
\boxed{
\mathbb E_{p_2}D(Q)-\mathbb E_{p_1}D(Q)
=\mu_N(p_2)-\mu_N(p_1)
\ \ge\ \frac{2}{N}(p_2-p_1)\ >0 .
}                                                                     \tag{3}
\]
All expectations refer to the fixed-size generative law and its declared
channel, not conditioning on a favorable observation. The proof is finite
and manual.

## 2. Uniform subset sampling preserves expected pair density

Fix any completed order \(P\) on \([N]\). For every unordered pair
\(\{i,j\}\), let \(I_{ij}(P)\) indicate that its vertices are comparable.
For a uniform actual \(m\)-subset, the number containing this pair is
\(\binom{N-2}{m-2}\), hence
\[
\Pr(\{i,j\}\subseteq T\mid P)
 =\frac{\binom{N-2}{m-2}}{\binom Nm}
 =\frac{\binom m2}{\binom N2}.                                         \tag{4}
\]
This holds also at \(m=N\), and at \(N=m=2\). The equality is elementary
factorial cancellation. It does not require exchangeability of the
birth-labeled order law.

Faithful completed restriction gives the pointwise identity
\[
K(P[T])=\sum_{1\le i<j\le N} I_{ij}(P)\,\mathbf1_{\{i,j\}\subseteq T}.
\]
Taking conditional expectations term by term and dividing by \(\binom m2\)
gives
\[
                       \mathbb E[D(Q)\mid P_N=P]
                          =\frac{K(P)}{\binom N2}=D(P).               \tag{5}
\]
Taking the expectation over \(P_N\) proves (2). Pair inclusion indicators
need not be mutually independent; only their individual inclusion
probabilities and finite linearity are used. In particular, this is not
an independent-pair or binomial sampling model for the observed statistic.

The expectation in (2) is independent of the chosen survivor size within
the stated range. That does not make the full distributions identical
across sizes, imply equal statistical precision, or restore the naive
substitution of \(m\) for \(N\) in the original full-order likelihood.

## 3. Common monotone coupling and strict separation

Fix \(p_1<p_2\). On one finite product probability space take independent
\(U_{ij}\) uniform on \([0,1]\), for \(i<j\le N\), and set
\[
                       E^{(a)}_{ij}=\mathbf1_{\{U_{ij}\le p_a\}},
                       \qquad a=1,2.                                \tag{6}
\]
Each marginal is exactly the accepted independent forward-edge
representation at its own parameter. Coordinatewise,
\(E^{(1)}_{ij}\le E^{(2)}_{ij}\). Every directed path at \(p_1\) is still
present at \(p_2\), so their completed orders satisfy
\[
                    I_{ij}(P_N^{(1)})\le I_{ij}(P_N^{(2)})
                    \quad\text{for every pair}.                     \tag{7}
\]
This yields weak monotonicity for every term. It does not by itself prove
strictness, which is supplied by the following exact finite witness.

For each adjacent pair of birth labels \(i,i+1\), a forward path from
\(i\) to \(i+1\) has no possible intermediate label. A later vertex cannot
return to the earlier endpoint, and an earlier vertex cannot be visited
after \(i\). Thus
\[
                       I_{i,i+1}(P_N^{(a)})=E^{(a)}_{i,i+1}.          \tag{8}
\]
There are \(N-1\) such pairs. On the common coupling,
\[
\begin{aligned}
\mathbb E[K(P_N^{(2)})-K(P_N^{(1)})]
&=\sum_{i<j}\mathbb E[I_{ij}(P_N^{(2)})-I_{ij}(P_N^{(1)})]\\
&\ge\sum_{i=1}^{N-1}\Pr(p_1<U_{i,i+1}\le p_2)\\
&=(N-1)(p_2-p_1).
\end{aligned}                                                          \tag{9}
\]
The other summands are nonnegative by (7); no independence between
completed comparisons is asserted. Divide by \(\binom N2=N(N-1)/2\),
then use (2), to obtain (3).

One may also attach the same independent uniform subset \(T\) to both
orders in (6). Each marginal then has the required thinning channel,
and completed survivor comparisons remain coupled monotonically.
This is a proof construction, not an additional observation premise.
The hidden labels and the uniforms in (6)–(9) are never observer inputs.
In particular an observer is not asked to identify which surviving
pairs were adjacent in the original birth sequence.

If two parameters gave equal distributions of the reported class, they
would give equal distributions and expectations of the bounded intrinsic
function \(D\). Equation (3) rules that out. The same argument proves the
stronger statistic-level identification. No explicit inversion of
\(\mu_N\), enumeration of order classes, numerical probability evaluation,
or likelihood optimizer is needed.

At \(N=2,m=2\), (3) is exact, since the chain probability is \(p\).
At \(m=N\), the argument applies to the unthinned order as well.
These checks do not add a parameter estimation procedure.

## 4. Boundary cases and why the contract matters

For \(m=0\), the only reported order is empty; for \(m=1\), it is a singleton.
Their distributions are independent of \(p\), so parameter identification
fails for both. Formula (1) is not used at those sizes: its denominator
would be zero. This distinguishes the theorem's entire domain from its
nonidentifying endpoints.

Known true \(N\) is a premise. In fact the accepted RI1377 example already
shows an alias when it is unknown: at \(N=3,m=2\) and parameter \(p\), the
chain probability is
\[
                              f(p)=p+p^2(1-p)/3.
\]
At \(N=2,m=2\) and parameter \(p'=f(p)\), the binary output distribution
is identical. Here \(p'>p\), \(p'>0\), and
\(1-p'=(1-p)(1-p^2/3)>0\), so both parameters are admitted and different.
Thus a claim of identification over all unknown-\(N\) possibilities
would already fail at observed size two. No classification of other
unknown-size cases is supplied.

Order-dependent survivor selection need not satisfy (4): conditional
pair-inclusion probabilities could depend on which pairs are comparable.
Consequently (5) and this proof do not extend to that channel. The
accepted predecessor's phrase “order-dependent observation kernel” means
only that the output restriction depends on its input order; it does not
permit order-dependent selection of the survivor subset.

Nonfaithful restriction also invalidates the pointwise pair-count identity.
Unknown/altered comparisons or deletion from a generating DAG followed by
recomputed reachability are not the specified completed-order channel.
In particular a comparison mediated by an erased vertex must be retained.

These exclusions are statements of this theorem's scope, not a universal
impossibility theorem about every alternative observation mechanism.
The alias above is only the explicit already-supported unknown-size case.

## 5. What is and is not identified

This closes the small-case-only parameter-identification limitation of
RI1377 for every fixed known \(N\) and \(2\le m\le N\). It does not replace
the accepted finite pushforward likelihood or change its survivor and
automorphism multiplicities. The height-erasure theorem remains an
existing dependency for observation conventions, not a newly proved
calibration or error-transfer result.

The accepted auxiliary-seed result gives two different seed descriptions
with the same native law at each \(p\). Applying the same thinning channel
preserves their equality. Identifying the parameter within their common
family cannot identify seed independence, auxiliary mechanics, or the
uniqueness of a physical model. The coupling (6) uses an available
independent representation for proof; it does not infer that representation
from observations.

Distribution identifiability is not exact recovery from one order.
Every \(m\)-vertex order class has positive mass for every \(p\in(0,1)\):
extend it by \(N-m\) isolated vertices to a full order, which has positive
mass under the accepted full-order law, and retain its original \(m\)
vertices, an allowed subset with positive channel probability.
Thus an individual reported order does not exclude all other parameters.

The expectation bound (3) is not a confidence radius, finite-sample error
rate, estimator guarantee or numerical conditioning certificate. No
sampling design, repeated-experiment independence, minimax guarantee,
optimal statistic or efficient general likelihood computation is claimed.

Known true size, genuinely uniform independent survivor selection, and
faithful acquisition of every completed comparison remain stipulated,
not measured or physically implemented. No physical readout, quantum
reconstruction, geometry, mass/gravity law, clock, RET work, application
advantage or ontology promotion follows. Execution remains HOLD.

## Publication and verification note

The source was constructed as a manual finite proof. Independent manual review and coordinator adjudication subsequently accepted its fixed-known-size scope. This public edition preserves scientific sections 1–5 literally; the private administrative evidence section is withheld. The historical candidate status above records the author stage rather than the later adjudication.

Public correspondence checks compare literal text, mathematical spans, dependencies and current byte identities. They are administrative checks, not machine proof, empirical confirmation or reconstruction of historical custody. Reused source consumption, historical display failures and recoveries, partial metadata exposure and worker-reported control observations remain distinguished in private evidence. No raw command receipts, machine identifiers, source-capture maps or private paths are published here.

The accepted result identifies a parameter within the stipulated optional family and faithful uniform-thinning channel. It supplies no exact recovery from one order, finite-sample estimator, physical readout, uniquely inferred hidden mechanism or execution admission. The separately assigned law-dependence continuation remains pending independent admission and is excluded.
