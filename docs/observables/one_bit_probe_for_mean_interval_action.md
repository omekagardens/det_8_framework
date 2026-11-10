# Reading the mean four-birth interval action with one bit per trial

Each preparation yields one bit after a randomly assigned omission setting. Three settings are necessary and sufficient to identify the population mean of the specified dimensionless action across all mixtures on the E63 support. A single shared omission coin invalidates this conclusion, even with every setting available.

## What is prepared and what is recorded

Use either E63 four-birth law $P_i$. Its registered prefix is $a\prec b$ with marks $(i,0)$ and descendant counters $(1,0)$. Keep all 15 structural sequences and their four fair newborn-mark continuations. For each realized order let $n_k$ count strict comparable endpoint pairs with exactly $k$ interior vertices. The stipulated dimensionless action is $S=4-2n_0+4n_1-2n_2$. The preparation supplies the order probabilities, while the action coefficients come from the specified convention. [Accepted E63 table](./finite_interval_action_and_source_preparation.md) · [Benincasa, Dowker & Schmitzer, Eq. (1.1)](https://arxiv.org/pdf/1011.5191v2)

After each independent preparation, choose one of the six unordered endpoint pairs uniformly. Keep those two vertices. Independently assign a setting $t$ and omit each of the two other vertices independently with probability $t$. A stipulated detector returns $B=1$ exactly when the retained endpoints form a link in the induced strict order. Keep the tagged record $(t,B)$ on every trial, including every zero. The observer receives only this record. Uniform pair selection, faithful pair addressing, preservation of induced comparabilities, selective omission, calibrated detection, and reset are supplied operations. All omissions occur in the readout after growth.

Incomparable endpoints always return zero. For comparable endpoints with $k$ strict intermediates the bit is one precisely when all $k$ are omitted. Omission of other vertices is irrelevant. Conditional on the order, the three terms below count disjoint possible pairs, each sampled with probability $1/6$.

$$
p_n(t)=\Pr(B=1\mid n,t)=\frac{n_0+t n_1+t^2n_2}{6}.
$$

At zero omission the detector counts original links, and at full omission it counts all comparable pairs. For a preparation ensemble write $p(t)=\mathbb E[p_n(t)]$. If the assigned settings have probabilities $\pi_t>0$, the complete tagged law gives probabilities $\pi_t p(t)$ and $\pi_t[1-p(t)]$ to the two records at $t$.

## Recovering the ensemble mean

Take the settings $0,\tfrac12,1$. Applying the following linear combination to the basis functions $1,t,t^2$ gives coefficients $-2,4,-2$ after the factor of six in the response.

$$
\mathbb E[S]=4-108p(0)+144p(\tfrac12)-48p(1).
$$

Let $w_0=-108,\ w_{1/2}=144,\ w_1=-48$. A single-trial signed score is $4+w_t B/\pi_t$. Averaging first over the bit and then over the assigned setting gives exactly $S$ conditional on each supported order. Averaging scores from independent preparations therefore estimates the ensemble mean without observing an order. A finite sample still has sampling error. For example, the supported profiles $(1,0,0)$ and $(2,0,0)$ yield actions 2 and 0 respectively, yet both bit values occur at every setting for both profiles. E63's obstruction to determining an individual trial's action remains.

Multiplying each profile by the corresponding structural numerator in the accepted table and summing gives the following check. Each structural row already includes its four newborn-mark continuations.

| Preparation | $1320\,\mathbb E[(n_0,n_1,n_2)]$ | $7920\,p(t)$ | Recovered $\mathbb E[S]$ |
| --- | --- | --- | ---: |
| $P_0$ | $(4066,1886,951)$ | $4066+1886t+951t^2$ | $93/44$ |
| $P_1$ | $(4286,1441,966)$ | $4286+1441t+966t^2$ | $9/22$ |

The source-one minus source-zero contrast is $-75/44$, in the E63 dimensionless convention.

## Why two settings cannot work on this support

Arbitrary mixtures enter only to test the readout on supported orders. The four actual profiles $(1,0,0),(2,0,0),(2,1,0),(4,0,1)$ form a tetrahedron with nonzero volume. Subtracting the first point from the other three gives a matrix of determinant 1. Consequently its centroid $m$ can move a sufficiently small distance in either direction along any vector while remaining a realizable mixture mean.

Take any two allowed settings $s,u$. The vector $v=(su,-(s+u),1)$ gives $(1,x,x^2)\cdot v=(x-s)(x-u)$. Thus two supported mixture means $m\pm\epsilon v$ have exactly the same click probabilities at both settings. Their full tagged population laws agree. Their action means differ because
$$
(-2,4,-2)\cdot v=-2su-4(s+u)-2<0 \qquad (0\le s,u\le1).
$$
This collision also rules out nonlinear decoding and any smaller menu. Three distinct settings determine the quadratic by interpolation, which proves sufficiency as well as the claimed minimum.

There is a narrower inference when the source law is guaranteed to be $P_\lambda=(1-\lambda)P_0+\lambda P_1$. At $t=0$, the click probability changes from $4066/7920$ to $4286/7920$, a difference of $1/36$. Hence $\lambda=36[p_\lambda(0)-4066/7920]$ and $\mathbb E_\lambda[S]=93/44-(75/44)\lambda$. One population rate suffices under this two-source assumption. Individual trials still return just a bit.

## Failure with perfectly correlated omissions

Suppose a shared Bernoulli coin omits both nonendpoints together with probability $t$, and otherwise keeps both. One or two intermediates now clear with the same probability, giving $6p^{\mathrm{shared}}_n(t)=n_0+t(n_1+n_2)$. Take a supported order with profile $(3,1,0)$ and compare it with an equal mixture of the supported profiles $(2,1,0)$ and $(4,0,1)$. Both yield $(3+t)/6$ at every setting. The first has action 2 and the second has mean action $(4-6)/2=-1$. Even the entire shared-coin response curve loses the arbitrary-mixture action mean. The trusted two-source calculation at $t=0$ still holds since neither protocol omits any vertex there.

**Physical scope.** This establishes an observation design conditional on the specified detector. Implementing it would require a physical way to register each trial and realize the stated pair and omission operations. A spacetime interpretation and a dimensional action scale require independent correspondence and calibration. The finite calculation supplies neither a measurement on an apparatus nor a gravitational field equation.
