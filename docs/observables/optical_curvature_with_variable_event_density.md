# Separating centre curvature from spatial variation in event density

Five nested count means and two four-ray optical exposures at the same half-side diamond separate the geometry from the sampling density in the family below. Without the optical measurement, the entire spatial point-process law can agree at different centre curvatures. The centre density in clock units already follows from the counts and the registered clock.

## Geometry and spatial sampling

Let
$$
 z=(u-v)^2,\quad ds^2=-2L^2f(z)\,du\,dv,\quad
 f(z)=1-Az-Bz^2-Cz^3,\quad 0<f(z)\le1\ (0\le z\le1),
$$
$$
 \rho(z)=\rho_0(1+\eta z),\quad \rho_0>0,\quad\eta>-1.
$$
The density variation is quadratic in $u-v$; symmetry makes its first derivative at the centre vanish. The coefficient $\eta$ is the variation parameter at issue, not a measured first derivative at the centre.

Write $\sigma=\rho_0L^2$ and
$$
 w(z)=(1+\eta z)f(z)=1+w_1z+w_2z^2+w_3z^3+w_4z^4.
$$
The spatial Poisson intensity with respect to coordinate measure is exactly
$$
 \boxed{\Lambda(du\,dv)=\sigma w((u-v)^2)\,du\,dv.}        \tag{1}
$$
No independently uniform proper-area draw can be substituted for this sampled population.

The curvature convention gives
$$
 R_c=4A/L^2.
$$
Because $0<f\le1$ and $f(0)=1$, the central image $u=v$ uniquely maximizes tip-to-tip proper time: its proper length is $\sqrt2L$, while every causal curve is bounded by that value using the factor $f\le1$ and Cauchy–Schwarz on its two null-coordinate rates. Therefore
$$
 T=\sqrt2L/c,\qquad L=cT/\sqrt2.
$$
Fractional proper-time tags along that central clock locate centred causal squares of the stipulated fractional sides, also when only a stable unknown-duration tick is given.

## 2. Five nested means identify the spatial product

Set
$$
 h_i=1,1/2,1/3,1/4,1/5,\qquad x_i=h_i^2,\quad y_i=m_{h_i}/h_i^2.
$$
Rescaling a centred side-$h$ square to the unit square gives $z=h^2(U-V)^2$. Since
$\int(U-V)^{2j}\,dU\,dV=2/[(2j+1)(2j+2)]$, its mean is
$$
 \boxed{\frac{m_h}{h^2}
 =P(h^2)=\sigma\left[
  1+\frac{w_1h^2}{6}+\frac{w_2h^4}{15}
       +\frac{w_3h^6}{28}+\frac{w_4h^8}{45}\right].}       \tag{2}
$$
There is one unknown common $\sigma$; no independent density normalization is inserted.

The five distinct $x_i$ give a unique polynomial of degree at most four:
$$
 P(x)=\sum_{i=1}^5y_i\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}
      =\sum_{j=0}^4p_jx^j.
$$
Recover
$$
 \boxed{\sigma=p_0>0,\qquad
 (w_1,w_2,w_3,w_4)=(6p_1,15p_2,28p_3,45p_4)/p_0.}       \tag{3}
$$
This is finite interpolation in the supplied family, not an observed sixth zero-side window, a claim of minimality, or a generic local derivative limit. Independence of nested counts is unnecessary; exact means suffice.

The intercept identifies $\rho_0L^2$, since the stipulated $f(0)=1$ and density factor $1+\eta z$ both have unit constant term. Their normalizations matter. The whole count mean is
$$
 m_1=\sigma I(w),\qquad
 I(w)=1+w_1/6+w_2/15+w_3/28+w_4/45,
$$
and is generally not $\sigma$. The actual whole proper area is instead
$L^2I(f)=L^2(1-A/6-B/15-C/28)$.

## 3. Full spatial-law ambiguity without optics

Choose the same arbitrary $L>0,\rho_0>0,c$, the same calibrated central clock, and these two admissible worlds:

| Quantity | World A | World B |
| --- | --- | --- |
| Metric $f(z)$ | $1-z/4$ | $1-z/2$ |
| $A,B,C$ | $(1/4,0,0)$ | $(1/2,0,0)$ |
| Density coefficient $\eta$ | $-1/2$ | $-1/4$ |
| Proper-area density | $\rho_0(1-z/2)$ | $\rho_0(1-z/4)$ |
| Centre curvature | $1/L^2$ | $2/L^2$ |
| Centre density | $\rho_0$ | $\rho_0$ |

Both metric factors are smooth, positive and at most one on the entire interval; both density factors are strictly positive with $\eta>-1$. Their product is identical pointwise:
$$
 w(z)=(1-z/4)(1-z/2)=1-\frac34z+\frac18z^2.
$$
Thus their **entire spatial Poisson process law** is the same intensity measure (1). Every spatial count law, conditional position distribution, nested count, empty event and joint spatial statistic agrees. The whole count is Poisson with common mean
$$
 \sigma I(w)=\sigma(1-1/8+1/120)=(53/60)\sigma.
$$
Conformal positivity gives the same causal order relation on positions. Consequently every order formed from the observed sampled process, including joint order/position/count statistics, has the same law. A denser or complete observation of this process cannot factor its intensity measure.

The maximizing clock is identical, with $T=\sqrt2L/c$; use the same tick duration and endpoint phases if its record is $N=T/\Delta$. The causally registered nested boundaries also agree. The scales and known standards are held fixed, not rescaled. Centre curvature differs even though centre density is the same. Geometric proper areas need not agree, but no independent proper-area or uniform-sampler observation is supplied to distinguish them.

This demonstrates a stronger ambiguity than equality of a few integrals. It does not rely on missed detections, unknown masks, retuned native marks, or an independently biased order detector. It is a factorization ambiguity in the actual sampled intensity.

For completeness, the counts-only candidate factorizations can be described finitely. For any proposed $\eta$, set
$$
 A=\eta-w_1,\qquad B=-w_2-\eta A,\qquad C=-w_3-\eta B.
$$
The remaining coefficient requires
$$
 \eta^4-w_1\eta^3+w_2\eta^2-w_3\eta+w_4=0.               \tag{4}
$$
Keep only real roots with $\eta>-1$ and admissible $f$. These equations include $\eta=0$ and lower-degree products. Some individual products may have a unique admissible factorization; the displayed pair proves the absence of universal count-only identification.

## 4. One optical exposure does not universally suffice

At the registered half-side diamond, its tips have $z=0,f=1$, and its side corners have $z_*=1/4$. Put $F_*=f(1/4)$. In the accepted optical convention,
$$
 {\cal I}_*=\int_{\text{half-side}}R\,d{\cal A}
     =2\log\frac{f_Pf_F}{f_Af_B}
     =\boxed{-4\log F_*}.                               \tag{5}
$$
For one four-ray exposure let
$$
 Q=\frac{r_{PA}r_{PB}}{r_{AF}r_{BF}},\qquad
 \Gamma=\frac{a_Aa_B}{a_Pa_F}.
$$
The positive received/emitted ratios obey
$$
 \log Q={\cal I}_*/2+2\log\Gamma.
$$
The reviewed nuisance theorem states that the other three log-ratio directions can be fitted by freely chosen unit-velocity rapidities at the corners. Hence retaining all four positive ratios does not itself calibrate $\Gamma$.

The two full-spatial-law worlds above provide an explicit complete single-exposure collision. They have
$$
 F_{*,A}=15/16,\qquad F_{*,B}=7/8,
$$
with respective integrals $4\log(16/15)$ and $4\log(8/7)$. In each world choose zero optical rapidities, tip gains one and each side-device gain $\sqrt{F_*}$. These are positive, common to both local readings of the corresponding device. Substitution in every link law gives
$$
 (r_{PA},r_{PB},r_{AF},r_{BF})=(1,1,1,1)
$$
in both worlds. The point-process and clock records still match. The unknown device gains may differ between compatible worlds, while the frequency readout convention and every known standard remain fixed. No frequency-gain calibration follows merely from the independently calibrated elapsed clock.

Thus a single uncalibrated optical exposure does not guarantee separation. This is a universal-design statement; it does not deny unique count-only special cases.

## 5. Exchanged exposures at one anchor determine $F_*$

Now use the stipulated two repeated four-ray exposures at the same half-side geometry. Let $q_r=\log Q_r$, and let $x_i=\log a_i$ be the gains of the same four portable devices. With role signs $d_i=+1$ on side corners, $-1$ on tips, the complete tip/side exchange gives the second sign vector $-d$. Stable transported gains and identical integrated curvature give
$$
 q_1={\cal I}_*/2+2d\cdot x,\qquad
 q_2={\cal I}_*/2-2d\cdot x.
$$
Therefore
$$
 \boxed{{\cal I}_*=q_1+q_2,\qquad
 F_*=\exp[-(q_1+q_2)/4].}                               \tag{6}
$$
Either ordering within each destination pair is allowed. This is one spatial anchor but two registered optical exposures. Both tip devices must move to side roles and both side devices to tips. A partial exchange, unregistered station gains, gain drift or an unknown mismatch of the two integrals would not obey this exact cancellation.

The full eight-ratio record imposes no hidden additional shape condition after (6). Indeed $d\cdot x=(q_1-q_2)/4$; choose, for example, $x=d(q_1-q_2)/16$, using $d\cdot d=4$. In each exposure subtract that geometry/gain zero-rapidity prediction from the four observed log ratios, obtaining residuals $z_1,z_2,z_3,z_4$. Their contrast vanishes by (6). The corner rapidities
$$
 (\xi_P,\xi_A,\xi_B,\xi_F)=(0,-z_1,z_2,z_3-z_1)
$$
give boost contributions $(z_1,z_2,z_3,z_4)$. Thus every given positive eight-ratio record with the recovered integral can be realized on that fixed admissible metric by the common positive device gains and future unit velocities. Individual gains and velocities are not uniquely determined.

## 6. Combined inverse, feasibility and reduced degrees

From (3) the product polynomial $w$ is known. Since $F_*>0$,
$$
 w(1/4)=(1+\eta/4)F_*
$$
gives the unique density coefficient
$$
 \boxed{\eta=4\left[\frac{w(1/4)}{F_*}-1\right].}         \tag{7}
$$
Then use
$$
 \boxed{A=\eta-w_1,\qquad B=-w_2-\eta A,\qquad
 C=-w_3-\eta B.}                                        \tag{8}
$$
These formulas divide by neither $\eta$ nor the highest polynomial coefficient. They cover a constant density ($\eta=0$), quadratic/linear/constant metric factors, and lower-degree product polynomials.

A finite necessary-and-sufficient data test in this family is:

1. Require finite five mean counts. Interpolate $P$ at the specified distinct nodes; require $p_0=\sigma>0$ and form $w$ by (3).
2. Require all eight optical ratios finite and positive with the stipulated complete role exchange, stable portable gains and reproducible geometry. Compute (6); require ${\cal I}_*\ge0$, hence $0<F_*\le1$.
3. Form (7)–(8), require finite coefficients and $\eta>-1$. Check the exact polynomial identity
   $w(z)=(1+\eta z)(1-Az-Bz^2-Cz^3)$, including $w_4=-\eta C$, and check $f(1/4)=F_*$.
4. Check $0<f(z)\le1$ on $[0,1]$: evaluate $f$ at $0,1$ and at all real interior roots of $f'(z)=-A-2Bz-3Cz^2$. Handle an identically zero derivative as the constant $f=1$ case. Endpoint/critical-point checks are sufficient for this polynomial.
5. Require a positive finite calibrated maximizing $T$, or positive finite exact $N$ with a common stable duration $\Delta>0$, and the supplied central clock/boundary registration.

Passing these tests yields a real admissible metric, a strictly positive density and a common Poisson process whose nested means are the offered means. Its central clock realizes the time record. The gain/rapidity construction in §5 realizes all eight optical ratios. Thus the tests are sufficient as well as necessary. No independent uniform-area pair law is an additional test or input.

Uniqueness follows directly: the five distinct nodes fix $\sigma,w$; (6) fixes $F_*$; (7) fixes $\eta$; coefficient comparison fixes $A,B,C$. The clock fixes $L$ absolutely if calibrated, or in tick units otherwise. No alternative admissible factorization can retain the same product and same positive anchor value.

Zero integrated anchor curvature is not by itself a flatness claim. It says $f(1/4)=1$, and a nonconstant admissible cubic can attain that value. The inverse remains regular at ${\cal I}_*=0$ and at $\eta=0$; the product and full polynomial checks still distinguish the cases. This anchor cannot generically separate an arbitrary unknown density function from an arbitrary metric: success depends on the stipulated single linear density factor and cubic shape family.

## 7. Centre area per event and dimensional standards

For calibrated $T$, the inverse yields
$$
 L=cT/\sqrt2,\qquad
 \boxed{R_c=\frac{8A}{(cT)^2},\qquad
 \rho_0=\frac{2\sigma}{(cT)^2},\qquad
 \rho(z)=\rho_0(1+\eta z).}                             \tag{9}
$$
The centre mean area per sampled event is $\rho_0^{-1}$, with length convention $\ell_0=\rho_0^{-1/2}=L/\sqrt{\sigma}$. Centre density is already identified from the five count means and clock normalization, even without optics. The anchor separates the variation and curvature, not a previously missing centre count normalization.

For unknown stable tick duration $\Delta$ and exact $N=T/\Delta$,
$$
 \boxed{R_c(c\Delta)^2=\frac{8A}{N^2},\qquad
 \rho_0(c\Delta)^2=\frac{2\sigma}{N^2},\qquad
 \frac{\ell_0}{c\Delta}=\frac{N}{\sqrt{2\sigma}},\qquad
 \frac{R_c}{\rho_0}=\frac{4A}{\sigma}.}                  \tag{10}
$$
The density-shape coefficients are dimensionless. Dilation of $L,\Delta$ by the same $\lambda>0$, with $\rho_0\mapsto\rho_0/\lambda^2$, leaves all count and optical ratios and $N$ unchanged. Optical integrated curvature is dimensionless and cannot remove this clock scale freedom. A calibrated $\Delta$ supplies the dimensional standard.

The actual whole-area-per-mean-count quantity is
$$
 \frac{L^2I(f)}{\sigma I(w)}
   =\rho_0^{-1}\frac{I(f)}{I(w)},
$$
generally different from the centre value $\rho_0^{-1}$. Neither is a realized cell area or a reciprocal random count. A Poisson count may vanish. The fixed shape normalization, density length convention and elapsed proper-time standard are distinct assumptions.

The sampling model stipulates a Poisson process with a specified intensity per unit proper area. The optical measurements require stable portable gains, registered null rays and a repeatable metric. Applying these results to physical or native events requires independent registration. [Nested-diamond geometry](centre_curvature_from_nested_diamonds.md) · [Exchanged optical receivers](integrated_curvature_with_exchanged_receivers.md) · [Four-link frequency law](integrated_curvature_from_four_frequency_ratios.md)
