# Can order comparability distinguish curvature from missed events?

**Decision.** An unknown fixed acceptance mask can reproduce the complete pair record of a different curvature, even when the mean acceptance and all failure flags are known. In the supplied continuum family, independently assigning a fair complementary mask to **each candidate** recovers the centre curvature times the diamond’s proper area from the pooled population law.

## What the native register measures

For a consistently empty-prepared four-vertex register let $d_v$ be the terminal strict-descendant count of vertex $v$. The accepted incidence identity gives the exact fraction
$$
\widehat p=\frac{\sum_v d_v}{\binom42}=\frac{\sum_v d_v}{6}.
$$
Each comparable unordered pair contributes once at its earlier endpoint. No counter wraps at four vertices. The admitted terminal multiset of count values suffices for the sum, without naming handles or conditioning on an order class. Access to that multiset is an additional observation premise. For example, an antichain and an order with a single relation both return zero on the original “some count equals two” bit, but their fractions are 0 and $1/6$.

On a realized order, $\widehat p$ is the probability of comparability if one of its six unordered pairs is drawn uniformly. Its distribution across native trials depends on their preparation and growth law. A *separate* four-point iid continuum sample has the same counting formula and, by linearity, ensemble mean equal to its two-point comparability probability. Its six indicators share vertices. Neither one realization nor agreement of one mean establishes equality of the two order laws. Chain counts as ensemble observables have a precedent in causal-set geometry. [Roy, Sinha & Surya](https://arxiv.org/abs/1212.0631v1)

## Continuum calculation

On $0<u,v<1$ let $X=(2u-1)(2v-1)$ and $f_\theta=1+\theta X$, $|\theta|\le1/2$. The metric $ds^2=-2L^2 f_\theta\,du\,dv$ has positive proper-area element $L^2 f_\theta\,du\,dv$. Since $\int X\,du\,dv=0$, the diamond has area $\mathcal A=L^2$, and each candidate has normalized position density $f_\theta$. Future order increases in both coordinates. The probability mass in the past of $(u,v)$ is $uv+\theta u(1-u)v(1-v)$. Thus two independent candidates have comparability probability
$$
p_\theta=2\int_{(0,1)^2} f_\theta
 [uv+\theta u(1-u)v(1-v)]\,du\,dv=\tfrac12+\theta/9 .
$$
Indeed the two linear contributions inside the integral are each $\theta/36$, and the quadratic term integrates to zero by reflection in one coordinate.

Use $R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}+\cdots$, with $R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}$. Here $R_{uv}=-\partial_u\partial_v\log f_\theta$, so $R=2(L^2 f_\theta)^{-1}\partial_u\partial_v\log f_\theta$. At $u=v=1/2$ this gives
$$
R_c\mathcal A=8\theta=72(p_\theta-\tfrac12).
$$
The order relation is the same throughout the family. The change in comparability comes from where the proper-area sampling puts the events.

## Complete labelled pair record

Take independent candidate positions and conditionally independent acceptance coins. For mask setting $s=\pm1$, an event at $(u,v)$ passes with probability $a f_{s\eta}$, where $0<a\le1/2,\ |\eta|\le1/2$. Its unnormalized accepted position density and pass probability are
$$
g_s=a f_\theta f_{s\eta}=a(1+B_s X+C_s X^2),\qquad
B_s=\theta+s\eta,\quad C_s=s\theta\eta,\quad q_s=a(1+C_s/9).
$$
Conditional on the settings $s,t$ of the two labelled candidates, define
$$
J_{st}=\frac{q_s q_t}{2}
       +\frac{a^2(B_s+B_t)}{18}
       +\frac{a^2(B_s C_t+C_s B_t)}{450}.
$$

| Acceptance flags | Retained order bit | Probability given $s,t$ |
| --- | --- | --- |
| 11 | comparable | $J_{st}$ |
| 11 | incomparable | $q_s q_t-J_{st}$ |
| 10 | missing | $q_s(1-q_t)$ |
| 01 | missing | $(1-q_s)q_t$ |
| 00 | missing | $(1-q_s)(1-q_t)$ |

To evaluate $J_{st}$, use the comparability indicator $[1+\operatorname{sgn}(u'-u)\operatorname{sgn}(v'-v)]/2$, ignoring ties of zero measure. For independent uniform $x,y$ on $(-1,1)$ let $H_{ij}=\mathbb E[x^i y^j\operatorname{sgn}(y-x)]$. Among degrees $0,1,2$ the only nonzero entries are $H_{01}=1/3,\ H_{12}=-1/15$ and their negatives on exchange. These follow by integrating first over $x$. The two coordinates give $H_{ij}^2$ in the integral against $g_s g_t$, yielding the displayed polynomial. If the earlier candidate is also tagged for comparable pairs, reflection of both coordinates about their midpoints preserves both densities and splits $J_{st}$ equally between the two directions.

**Fixed mask.** Set $s=t=+1$. Exchanging $\theta$ and $\eta$ preserves $g_+$ pointwise and therefore every row of the table, including the missing bit. For example $(\theta,\eta)=(0,1/2)$ and $(1/2,0)$ have the same known $a$, marginal pass rate $a$ and comparable-pair mass $5a^2/9$. Their values of $R_c\mathcal A$ are 0 and 4. The fixed-mask population law cannot decide even whether the centre is flat.

**Complementary masks.** Independently assign a fair sign to each candidate before detection, independently also of positions. Retain both signs and flags; each conditional row above has joint weight $1/4$ times its displayed probability for its particular sign pair. Pool these joint masses by summing over all four sign pairs. Since $(g_++g_-)/2=a f_\theta$, the pooled both-pass position density is $a^2 f_\theta(u,v) f_\theta(u',v')$. Consequently
$$
p_{\rm pool}
=\frac{\Pr(11,\ {\rm comparable})}{\Pr(11)}
=\frac{\sum_{s,t}J_{st}}{\sum_{s,t}q_s q_t}
=p_\theta,\qquad \Pr(11)=a^2>0 .
$$
This ratio uses the observed population weights of the sign groups. Individual sign-conditioned comparability probabilities need not have equal weight among double acceptances. A *shared* fair sign per pair would leave the multiplier $1+\eta^2XX'$ in the pooled density, so cancellation of the single-event mask would not justify the same pair calculation.

Under the registered complementary protocol, the population law identifies $\theta=9(p_{\rm pool}-1/2)$ and $R_c\mathcal A=72(p_{\rm pool}-1/2)$. Finite samples carry sampling uncertainty and can contain no double acceptance. Obtaining $R_c$ in inverse-length-squared units additionally requires a physical calibration of $L$ or $\mathcal A$. Connecting this comparator to DET would require independent evidence for the correspondence, candidate preparation, order readout and detection efficiencies. The native counter identity alone supplies the dimensionless pair fraction.

## Scientific review

DET Quantum Relativity supplied the proof. A distinct scientific reviewer checked the curvature sign, normalized pair law, conditioning, native count and dimensional limitations. Coordinator acceptance was recorded on 9 November 2026 HST.

- Control SHA-256: `5715e061310a2d4cdf35fe1effb6691384220cb5f4c6bafa58b15294b15bdb2e`.
- Author report SHA-256: `d6694214d54c83f36f7269eafdd8dacc97d30b24d8213aca6253e902a42f49f2`.
- Freeze SHA-256: `da83e7faca9fc8f811bc195137720c41159491c047992d80cfbcbc6ab8192af3`.
- Independent scientific review SHA-256: `a7e028f4aa444c3d892778950d0deecf87cfaf23aa2b71adc0e2c42be930bf5f`.
