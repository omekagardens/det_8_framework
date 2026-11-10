# One finite-mass corner measurement on two equal-area diamonds

**Decision.** At $m^2L^2=1/64$, the curved diamond ($\theta=1/2$) has a larger normalized corner response than the flat diamond ($\theta=0$). The gap exceeds $1.5361\times10^{-6}$, including the entire series remainder. An absolute error of at most $7.5\times10^{-7}$ per normalized reading preserves the distinction. This is an external continuum observation design for the two supplied geometries.

## What the corners measure

On $0<u,v<1$ take $ds^2=-2L^2 f_\theta\,du\,dv$, where $f_\theta=1+\theta(2u-1)(2v-1)$. Both candidates have proper area $\mathcal A=L^2$ and the same causal relation: future points increase in both null coordinates. The accepted curvature convention gives $R_{\rm centre}\mathcal A=8\theta$, hence 0 and 4 for this pair. Use the covariantly normalized unit impulse at $P=(0,0)$ and the signed retarded field at $F=(1,1)$, with the stipulated nonreflecting evolution. [Metric, area and curvature convention](order_comparability_and_curvature.md)

Minimal coupling on this single two-dimensional conformal patch gives the massless kernel $G_0=1/2$ for timelike-related points. Values on null boundaries do not affect the integrals below. Let $Q_\theta=G_m(F,P)/G_0(F,P)$. The ratio of the two corner readings gives $Q_\theta$ when the massless and massive impulses and detector share the same nonzero gain and response convention. The mass deformation uses metric-volume convolution in the retarded equation $G_m=G_0-m^2G_0*G_m$. [Nomaan X, Dowker and Surya, equations (3)–(4), (10) and §3.1](https://arxiv.org/pdf/1701.07212v5)

## The first term that separates the candidates

Put $x=m^2\mathcal A/2=1/128$, $d\mu_\theta=f_\theta\,du\,dv$, and $I_0=1$. Define the dimensionless ordered volumes
$$
 I_n(\theta)=\int_{P\prec z_1\prec\cdots\prec z_n\prec F}
                 \prod_{j=1}^{n} d\mu_\theta(z_j).
$$
The term with $n$ interior integrations contains $n+1$ factors of $1/2$ and $n$ factors of $\mathcal A$. Dividing by the massless response gives
$$
 Q_\theta=\sum_{n=0}^\infty(-x)^n I_n(\theta).
$$
The massless term is one, and $I_1=1$ in both diamonds because the areas agree. At the next order the volume with a specified ordering of two points is half of their comparability probability. Explicitly, the normalized past area of $(u,v)$ is $uv+\theta u(1-u)v(1-v)$. Integrating it against $f_\theta\,du\,dv$ gives
$$
 I_2(\theta)=\tfrac14+\tfrac{\theta}{18}.
$$
Each linear contribution is $\theta/36$, and the quadratic contribution vanishes by reflection in one coordinate. Thus $I_2(0)=1/4$ and $I_2(1/2)=5/18$, consistent with the earlier comparability probabilities $1/2$ and $5/9$. The first difference is **positive at order $m^4$**: its contribution to $Q_{1/2}-Q_0$ is $x^2/36=1/589824$. The two-point probability is a way to compute a volume integral. The proposed detector reads only the corners.

## Bound at the actual mass

View $I_n$ as the measure of one specified ordering of $n$ labelled points under the product of the normalized area measures. An ordered chain requires their $u$ coordinates to occur in that specified increasing order. Exchangeability and zero tie probability give $0\le I_n(\theta)\le1/n!$, uniformly in both metrics. This also bounds the integrals over every subdiamond with the same full-area normalization, so iteration of the retarded equation gives an absolutely convergent series there.

Define $P_\theta=1-x+x^2 I_2(\theta)$. The ratio of successive terms in the factorial majorant is at most $x/4$ from $n=3$ onward. Thus, separately for each geometry,
$$
 |Q_\theta-P_\theta|
 \le B=\frac{x^3}{6(1-x/4)}
 =\frac{1}{12558336}<7.963\times10^{-8}.
$$
At $x=1/128$ the finite responses therefore satisfy
$$
 Q_{1/2}-Q_0\ \ge\ \frac{1}{589824}-2B
 \ >\ 1.5361\times10^{-6}.
$$
In particular, no cancellation by the higher mass terms can erase or reverse the difference.

| Candidate | Quadratic prediction $P_\theta$, rounded | Bound on all omitted terms |
| --- | ---: | ---: |
| Flat | 0.992202758789 | $B$ |
| Curved | 0.992204454210 | $B$ |

An explicit decision threshold is the midpoint $(P_0+P_{1/2})/2\simeq0.992203606500$. Under the two-candidate assumption, an observed normalized response lies below this threshold for the flat candidate and above it for the curved candidate whenever its absolute measurement error is at most $7.5\times10^{-7}$. Indeed this allowance plus $B$ is strictly smaller than half the quadratic gap. It applies to each **final ratio**, including uncertainty from its massless reference. It is a design tolerance, without an associated instrument precision claim.

## Conditions on the inference

The mass setting and common proper area must establish the product $m^2\mathcal A=1/64$ in consistent units. Any uncertainty in that product, the impulse normalization, relative gain, boundary conditions or corner registration must fit the total response error allowance or be independently accounted for before applying the threshold. The two alternatives have identical massless causal reach and equal volume. Their massive corner responses differ because the internal proper-area weighting of causally ordered pairs differs. The protocol does not determine arbitrary curvature profiles from one signal.

The previous masked-point result observes acceptance flags and pair comparability for sampled interior events. Here no interior event is sampled or read. The four-vertex native-order result concerns exact equality of a discrete inverse to an external massless kernel. The present computation uses a supplied continuum wave law and two supplied metrics; it establishes no native-to-continuum convergence, mass calibration or gravity dynamics. [Interior pair observation](order_comparability_and_curvature.md) · [Accepted four-vertex obstruction](point_source_propagation_on_finite_orders.md)
