# Integrated curvature from four null-link frequency ratios

For each future link $X\to Y$, retain the positive frequency ratio $r_{XY}$, receiver reading divided by emitter reading for that same ray. Write $a_X>0$ for the multiplicative frequency gain at corner $X$. The four-link record gives the signed integrated scalar curvature $\mathcal I$ if one relative calibration $\Gamma$ is known:
$$
Q=\frac{r_{PA}r_{PB}}{r_{AF}r_{BF}},\qquad
\Gamma=\frac{a_Aa_B}{a_Pa_F},\qquad
\boxed{\ \mathcal I=\int_{\mathcal D}R\,d\mathcal A
       =2\log Q-4\log\Gamma\ } .
$$
A common unknown gain gives $\Gamma=1$. With arbitrary independent unknown gains, even all four labelled ratios together can be identical in a flat and a curved diamond.

## What each receiver measures

Use the supplied $1+1$-dimensional metric $ds^2=-2L^2 f\,du\,dv$, with $f>0$ smooth on the closed unit square and both null coordinates increasing to the future. The coordinate order of the four corners is $P=(0,0), A=(1,0), B=(0,1), F=(1,1)$. Set $f_X=f(X)$ and $c=1$ in the local velocity normalization. Any allowed future unit velocity at a corner can be written
$$
U_X^u=\frac{e^{\xi_X}}{\sqrt{2}L\sqrt{f_X}},\qquad
U_X^v=\frac{e^{-\xi_X}}{\sqrt{2}L\sqrt{f_X}},
$$
with independent real rapidities $\xi_X$. The two readings at any one corner use the same $U_X$ and $a_X$.

For a ray with $v$ constant, the affine geodesic equation uses $\Gamma^u_{uu}=\partial_u\log f$, so $K=L^2 f k^u>0$ is constant along that ray. Its observer frequency is $-g(U,k)=K U^v$. For a ray with $u$ constant, $\Gamma^v_{vv}=\partial_v\log f$ gives constant $K=L^2f k^v>0$ and observer frequency $K U^u$. Thus the normalization of each individual photon cancels between its own emission and reception. The readout law multiplies the observer frequency by the local gain. It gives

| Future link | Received / emitted frequency reading |
|---|---|
| $P\to A$, increasing $u$ | $(a_A/a_P)\sqrt{f_P/f_A}\exp(\xi_P-\xi_A)$ |
| $P\to B$, increasing $v$ | $(a_B/a_P)\sqrt{f_P/f_B}\exp(\xi_B-\xi_P)$ |
| $A\to F$, increasing $v$ | $(a_F/a_A)\sqrt{f_A/f_F}\exp(\xi_F-\xi_A)$ |
| $B\to F$, increasing $u$ | $(a_F/a_B)\sqrt{f_B/f_F}\exp(\xi_B-\xi_F)$ |

## Velocity cancellation and the curvature sign

The two links leaving $P$ have combined rapidity exponent $\xi_B-\xi_A$. The two entering $F$ have exactly the same exponent. Dividing the products therefore gives
$$
Q=\Gamma^2\,\frac{f_P f_F}{f_A f_B}.
$$
With the adopted convention $R_{uv}=-\partial_u\partial_v\log f$ and inverse metric component $g^{uv}=-1/(L^2 f)$, the scalar is $R=2(L^2 f)^{-1}\partial_u\partial_v\log f$. The positive proper area element is $d\mathcal A=L^2 f\,du\,dv$. Integrating the mixed derivative on the square gives
$$
\mathcal I=2[\log f_F-\log f_A-\log f_B+\log f_P]
          =2\log\frac{f_P f_F}{f_A f_B}.
$$
This establishes the stated sign for the registered received-over-emitted convention. A zero integral is compatible with cancellation of positive and negative curvature in a general diamond.

**Why just one gain combination is necessary and sufficient.** In the table order, the four boost terms in log space are $(p-a,b-p,t-a,b-t)$, where $p,a,b,t$ here stand for the four rapidities. The kernel consists of common shifts of all four rapidities. The image therefore fills the three-dimensional hyperplane $z_1+z_2-z_3-z_4=0$. At fixed geometry and gains, arbitrary local velocities realize every positive four-ratio record with the stated $Q$. Consequently the remaining three log-ratio directions cannot provide an independent gain measurement. Holding a record fixed determines only $\mathcal I+4\log\Gamma=2\log Q$. In the allowed smooth metric class, the corner factor can be any positive number (take $f=\exp(\lambda uv)$). Any residual freedom in $\Gamma$ can thus be offset by a change of geometry and the three available boost directions. Knowledge of $\Gamma$, or equivalent information fixing it, suffices. Four pairwise clock calibrations are unnecessary.

## Family check and a matched four-reading record

For the adopted $f_\theta=1+\theta(2u-1)(2v-1)$, $|\theta|\le1/2$, the tips have value $1+\theta$ and the side corners $1-\theta$. Hence
$$
\frac{Q}{\Gamma^2}=\left(\frac{1+\theta}{1-\theta}\right)^2,\qquad
\mathcal I=4\log\frac{1+\theta}{1-\theta}=8\,\operatorname{artanh}\theta.
$$
It has the sign of $\theta$, vanishes at the flat member and inverts to $\theta=\tanh(\mathcal I/8)$. The accepted centre value times area is $R_c\mathcal A=8\theta$. The integral and that centre-based quantity agree to first order around flat space and differ at nonzero $\theta$.

To exhibit the full ambiguity, choose identical $L$ and $\xi_X=0$ at every corner in both of these preparations.

| Preparation | Tips $a_P=a_F$ | Side corners $a_A=a_B$ | $(r_{PA},r_{PB},r_{AF},r_{BF})$ | $\mathcal I$ |
|---|---:|---:|---|---:|
| Flat, $\theta=0$ | $1$ | $1$ | $(1,1,1,1)$ | $0$ |
| Curved, $\theta=1/2$ | $\sqrt{3/2}$ | $\sqrt{1/2}$ | $(1,1,1,1)$ | $4\log 3$ |

In the curved case $a_X=\sqrt{f_X}$ exactly cancels the geometric factor on each individual link. The four local velocities in each case obey unit normalization. This ambiguity uses only the four retained ratios.

## Calibration, registration and dimensional scale

Under this family assumption, the calibrated optical result can supply the shape $\theta$ in the earlier tip-to-tip clock inverse, or be compared with the independent proper-area population law $p=1/2+\theta/9$. The ratios are unchanged by $L\mapsto\lambda L$ at fixed $f,\xi,a$. The integral is dimensionless. For the family $\mathcal A=L^2$ and $R_c=8\theta/L^2$, so dimensional centre curvature at nonzero $\theta$ still requires a length or area measurement. For example, register the unique maximizing image $u=v$ and read a calibrated elapsed proper time $\tau$ from $P$ to $F$. Then the earlier result gives $L=c\tau/[\sqrt2\,J(\theta)]$, where $J(\theta)=\int_0^1\sqrt{1+\theta z^2}\,dz$. An unknown tick duration retains the joint length/tick rescaling. Even a common clock gain known in absolute units supplies no elapsed time or wavelength through these four ratios alone. For general $f$ one integrated measurement gives no local curvature profile.

A physical implementation requires four identified future-propagating rays and eight matched endpoint frequency tags, with both local tags probing the same observer velocity and gain at each corner. Register the corner coincidences, the two null directions, local receiver/emitter assignments and the direction of each frequency quotient. Prepare or verify geometric-optics propagation in the stipulated effectively two-dimensional metric and the local contraction readout; independently establish the gain product and characterize instrumental uncertainty. Each emission may use its own frequency. The method requires neither phase-coherent relays nor comparisons of remote clock phases. A separate clock exchange could support relative calibration only after its device-transport and path-delay conditions were established. Relating these tags to a DET event record requires a physical correspondence for rays, geometry, observers and clocks. This result is an exact conditional optical calculation.

[Order comparability and the curvature convention](order_comparability_and_curvature.md) · [Proper time and dimensional curvature](proper_time_and_curvature_of_a_diamond.md) · [Conditions for clock exchange](device_exchange_clock_ratio.md)
