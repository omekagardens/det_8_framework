# A driven scalar ruler for a spherical gravity experiment

In a fixed Schwarzschild annulus, drive a static scalar to a nonzero value at areal radius $R$, clamp it to zero at $3R$, and measure the field at $2R$ relative to the drive. At known compactness $u=2GM/(Rc^2)<1$, this single ratio determines the dimensionless continuum parameter $(\mu R)^2$ uniquely. Three sector measurements then determine $\sqrt{\lambda}\,R/\ell$, where $\lambda$ converts the registered native scalar increments to continuum increments. An independent calibration of $\lambda$ makes this a measurement of $R/\ell$ without a Poisson-density standard.

## The field and the midpoint readout

Use the supplied vacuum exterior with $f(r)=1-uR/r$ and $0\le u<1$. For a static spherical test field of inverse length $\mu$, the minimally coupled equation $(\Box-\mu^2)\phi=0$ becomes
$$
 \frac1{r^2}\frac{d}{dr}\left(r^2 f(r)\frac{d\phi}{dr}\right)-\mu^2\phi=0 .
$$
The radial factor follows from $g^{rr}=f$ and the spherical metric volume density proportional to $r^2\sin\theta$. Only the metric and field equation are imported. A nonzero maintained inner drive and a finite outer clamp supply the boundary conditions for this experiment. [Schwarzschild, v1, Eq. (14)](https://arxiv.org/pdf/physics/9905030v1) · [Hod, v1, §II, Eqs. (1)–(3)](https://arxiv.org/pdf/1807.06225v1)

Let $x=r/R,\ p(x)=x(x-u),\ z=(\mu R)^2\ge0$, and normalize the field by its nonzero value at $R$. Then
$$
 L_z y:=-(p y')'+zx^2 y=0,\qquad y(1)=1,\quad y(3)=0,\qquad A_u(z)=y(2).
$$
The primes now refer to dimensionless $x$. The measured $A_u$ is a ratio of blank-subtracted amplitudes with the same gain within a setting. The sign and magnitude of the inner drive cancel. The label $2R$ refers to areal radius, not halfway in proper radial distance.

## Why one ratio has a unique inverse

The coefficients are smooth and $p>0$ on the closed interval. For homogeneous zero boundary values, integration against $y$ gives $\int_1^3[p(y')^2+zx^2y^2]\,dx=0$, so the only such solution is zero. To obtain the driven solution, start at $x=1$ with value one and vary the initial slope. The value at 3 is affine in that slope with nonzero coefficient, since a vanishing coefficient would give a nonzero homogeneous solution with zero endpoints. Thus a unique slope attains the clamp. Regular initial-value dependence gives continuity of $A_u(z)$ for every finite $z\ge0$.

The maximum principle for $L_z$ gives $0<y(x)<1$ in the interior (also directly from integration for $z=0$). For $z_2>z_1\ge0$, the two solutions obey
$$
 L_{z_2}(y_{z_1}-y_{z_2})=(z_2-z_1)x^2y_{z_1}>0
$$
with zero boundary difference. The difference is strictly positive inside. In particular $A_u(z)$ is strictly decreasing on the entire nonnegative half-line.

At zero mass one has constant $p y'$, hence
$$
 A_u(0)=
 \frac{\int_2^3 dx/[x(x-u)]}{\int_1^3 dx/[x(x-u)]}
 =
 \begin{cases}
 \displaystyle\frac{\log[(1-u/3)/(1-u/2)]}
                        {\log[(1-u/3)/(1-u)]},&0<u<1,\\
 1/4,&u=0 .
 \end{cases}
$$
For large $z$, take $w(x)=\exp[-\sqrt z(x-1)]$. Its endpoint values dominate those of $y$, and
$$
 L_z w=[z(x^2-p)+\sqrt z\,p']w\ge0
$$
because $x^2-p=ux$ and $p'=2x-u>0$. Comparison gives $0<A_u(z)\le e^{-\sqrt z}$. Thus the single-reading range is exactly **$(0,A_u(0)]$**. Zero is approached only in the infinite-mass limit. The upper endpoint is attained at $\mu=0$. For any ratio in this range its inverse is the unique nonnegative root of the displayed boundary-value response. No approximation to a decay length or boundary at infinity enters the decision.

## Three sectors and the transfer calibration

Use the independently compatible, quadratic spring/scalar record, with all original labelled histories, supported scalar preparations and nine scalar means retained. It supplies $v_i=m_i^2$, with $v_0=1<v_1<v_2$, and $H=h/k=2/(k\ell^2)>0$. The continuum settings use the same labels, one fixed geometry and the proposed law
$$
 \mu_i^2=d_{\rm ext}+\lambda k v_i,\qquad d_{\rm ext}\ge0,\quad\lambda>0 .
$$
The continuum offset is independent of the native scalar offset.

For each finite measured ratio $A_i$, require $0<A_i\le A_u(0)$ and form $z_i=A_u^{-1}(A_i)$. Define
$$
 S=\frac{z_1-z_0}{v_1-v_0},\qquad B=z_0-Sv_0.
$$
The complete remaining checks are $S>0,\ B\ge0,\ z_2=B+Sv_2$. They identify $S=\lambda kR^2$ and $B=d_{\rm ext}R^2$. Thus the third sector tests a prediction. With positive $v_i$, even a zero offset gives positive masses and strictly ordered ratios $A_u(0)>A_0>A_1>A_2>0$. An exactly massless single-field response is admissible for the boundary problem but fails the coupled sector test.

These conditions suffice. For example, fix any admissible $R>0$ consistent with the background. For a specified $\lambda>0$ choose $k=S/(\lambda R^2)$, $d_{\rm ext}=B/R^2$, and recover the corresponding native $h=Hk$, offset and gain using the scalar apparatus's freely scalable dimensional parameters. The original spring/scalar record is reproduced. The three constructed driven solutions reproduce the ratios. If $\lambda$ is free, this construction works for each positive choice. Positivity allows the unambiguous square root
$$
 \boxed{\sqrt{\lambda}\,\frac R\ell=\sqrt{\frac{HS}{2}}}.
$$
With independently known $\lambda$, divide by $\sqrt\lambda$ to obtain $R/\ell$. The fitted offset also determines $d_{\rm ext}/(\lambda k)=B/S$.

**A record-preserving freedom.** Keep $R$, background geometry, all continuum masses, $d_{\rm ext}$, mechanics and the optical apparatus fixed. For any $s>0$, send $\ell\mapsto s\ell$, and multiply the native $k,h,$ native mass-term offset and scalar readout gain by $s^{-2}$, as in the accepted native inverse. In the quadratic interpretation take $J_s\mapsto sJ_s$ at fixed $M_0,c$. Send $\lambda\mapsto s^2\lambda$. The native three-setting responses, registered mass ratios and $H$ persist. The continuum products $\lambda k v_i$, all boundary profiles, and all attenuation ratios also persist. The value $R/\ell$ has changed by $1/s$. This demonstrates exactly the remaining ambiguity in that length ratio. The same fixed geometry can retain the earlier count and clock records.

## Returning the length to the gravity experiment

The four-source exterior clock inverse supplies $a=2G\kappa M_0/(Rc^2)$ only on its compatible affine-source record. The scalar inverse supplies $j=J_s/(M_0c\ell)=\sqrt{H/2}$ under the positive quadratic action convention. If the clock experiment uses this same **areal** $R$, and the baseline carrier, native scalar scale and continuum transfer are registered across the experiments, then
$$
 \kappa\frac{GM_0^2}{cJ_s}
 =\frac{a}{2j}\frac R\ell
 =\frac a2\sqrt{\frac{S}{\lambda}} .
$$
A free $\lambda$ leaves only $\sqrt{\lambda}\,\kappa GM_0^2/(cJ_s)=a\sqrt S/2$. Even with $\lambda$ calibrated, removing the distinct source-response factor $\kappa$ requires its own calibration. The optical count comparison measures the radius in density units and the accepted radial projection can preserve readings while losing scalar-order information. This driven comparison uses a continuum-to-native mass-increment standard in place of a density-to-length standard.

The apparatus must establish compactness independently for the settled annulus, position each boundary and the midpoint detector by areal radius, hold the drive and clamp during each read, and verify stable gain and blank subtraction within each setting. The supplied static linear field law, negligible backreaction and reproducible sector transfer require independent justification. Preparing the field, supporting the boundaries, settling to a static profile, reading it and resetting the apparatus have physical costs. The amplitude ratios give no absolute stored energy, power or preparation-work measurement. Finite resolution at strong attenuation would need an error model. Nothing in this boundary-value calculation establishes a physical implementation or a DET-native field equation.

[Sector scalar response](scalar_mass_term_from_three_sector_inertias.md) · [Exterior clock experiment](exterior_clocks_and_scalar_gravity_coupling.md)
