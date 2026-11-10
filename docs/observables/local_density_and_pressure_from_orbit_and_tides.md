# What one signed orbit and four tidal readings determine

At one event on a nontrivial circular geodesic in a smooth static spherical annulus, the orbit predicts the true polar tidal acceleration in each of two velocity frames. The predictions differ strictly on the entire admitted orbit domain. They calibrate the common positive gain and zero of the instrument. Its two radial readings then give the two remaining curvature components. With Einstein's equations and zero cosmological constant this fixes the local energy density, radial pressure and tangential pressure. All statements below concern exact records in the stated model.

## The orbit and its domain

Write the metric in areal radius as
$$
 ds^2=-e^{2\Phi(r)}c^2dt^2+dr^2/F(r)+r^2d\Omega^2,\qquad F(r)=1-2m(r)/r.
$$
The Misner–Sharp mass in length units is $m=GM_{\rm MS}/c^2$. Use a calibrated radius $R>0$, finite positive proper period $T$ to the **first forward meridian return**, and the outward and forward components $(C,D)$ of an initially outward parallel-transported unit spin. Define
$$
 x=2\pi R/(cT),\quad \gamma=\sqrt{1+x^2},\quad \beta=x/\gamma,\quad
 q=\operatorname{Arg}_{[0,2\pi)}(C-iD)/(2\pi).
$$
Require real $C,D$ with $C^2+D^2=1$ and $0<q\le1/\gamma$. Use the outward radial and forward orbital directions of the signed record. In the local static tetrad the orbit has unit timelike tangent $U_o=\gamma(e_0+\beta e_\phi)$. Its angular proper rate gives $\gamma\beta=x$. The radial geodesic equation gives $R\Phi'_R=\beta^2$. The accepted spin transport gives $(C,D)=(\cos(2\pi\sqrt{F_R}/\gamma),-\sin(2\pi\sqrt{F_R}/\gamma))$. The untrapped, pointwise nonnegative mass domain $0<F_R\le1$ puts the phase on the admitted arc, yielding $F_R=\gamma^2q^2$. This uses an exactly prepared circular orbit. Stability under radial perturbations is a separate question.

## From the metric to the four displays

Take signature $(-+++)$, $R^a{}_{bcd}=\partial_c\Gamma^a_{db}-\partial_d\Gamma^a_{cb}+\Gamma^a_{ce}\Gamma^e_{db}-\Gamma^a_{de}\Gamma^e_{cb}$, and $R_{bd}=R^a{}_{bad}$. For a unit separation direction $n$ normal to the unit timelike tangent $U$, the signed instantaneous relative acceleration per unit proper separation is $K=-c^2 R_{nUnU}$. Stretch is positive. Proper time is that of the freely falling central body.

Let $d\ell=dr/\sqrt F$, $N=e^\Phi$. The static orthonormal connection for the time and sphere factors has logarithmic radial derivatives $N_{,\ell}/N$ and $r_{,\ell}/r$. Differentiation in the radial plane gives $R_{0r0r}=N_{,\ell\ell}/N$ and $R_{r\theta r\theta}=-r_{,\ell\ell}/r$. The products of the two connection coefficients give $R_{0\theta0\theta}=N_{,\ell}r_{,\ell}/(Nr)$, and the unit sphere curvature gives $R_{\theta\phi\theta\phi}=(1-r_{,\ell}^2)/r^2$. Here the indices denote unit tetrad vectors. Substituting $r_{,\ell}=\sqrt F$ gives these four independent components in radius units, all at $R$:
$$
\begin{aligned}
 a &=R^2 R_{0r0r} =R^2[F(\Phi''+\Phi'^2)+F'\Phi'/2],\\
 b &=R^2 R_{0\theta0\theta}=R^2 R_{0\phi0\phi}=F_R R\Phi'_R,\\
 h &=R^2 R_{r\theta r\theta}=R^2 R_{r\phi r\phi}=-RF'_R/2,\\
 d &=R^2 R_{\theta\phi\theta\phi}=1-F_R.
\end{aligned}
$$
Compare a central geodesic instantaneously at rest in the static frame ($U_s=e_0$) with the orbit tangent $U_o$. Radial and polar unit vectors are perpendicular to the azimuthal boost and can be used in both frames at the tagged event. The terms $R_{n0n\phi}$ vanish by static time reversal. Thus $H=R^2R_{nUnU}$ takes the following values.

| Frame | Radial $H$ | Polar $H$ |
|---|---:|---:|
| Instantaneously at rest | $a$ | $b$ |
| Orbiting | $\gamma^2a+x^2h$ | $\gamma^2b+x^2d$ |

**Two polar calibration points.** Since $b=F_R\beta^2$ and $d=1-F_R$, the two polar curvatures reduce to $H_{s\theta}=x^2q^2$ and $H_{o\theta}=x^2$. In physical units the corresponding accelerations per length are $-q^2(2\pi/T)^2$ and $-(2\pi/T)^2$. Their curvature difference in radius units is
$$
 \Delta=x^2(1-q^2)\ \ge\ x^4/(1+x^2)>0.
$$
This includes $m(R)=0$. The anchors become poorly separated in the joint slow-orbit, $q\to1$ limit. At exactly zero speed there is no second frame.

## Exact recovery and consistency

Let $Z_{sr},Z_{s\theta},Z_{or},Z_{o\theta}$ denote the four raw signed displays. Their common response is $Z=z_0+\alpha K=z_0-gH$ with $g=\alpha c^2/R^2>0$. A necessary sign check is **$Z_{s\theta}>Z_{o\theta}$**. For finite real readings satisfying this check and an admissible signed orbit, the unique inverse is
$$
\begin{aligned}
 g&=(Z_{s\theta}-Z_{o\theta})/\Delta, & z_0&=Z_{s\theta}+g\,b,\\
 a&=(z_0-Z_{sr})/g, & h&=\{(z_0-Z_{or})/g-\gamma^2a\}/x^2 .
\end{aligned}
$$
The physical gain is $\alpha=gR^2/c^2$. Independent channel gains or zeros would invalidate this use of the polar readings for the radial channels.

The stated checks are also sufficient for the local geometric problem with $m(R)\ge0$. To see this, put $y=(r-R)/R$ and choose
$$
 F(r)=F_R-2hy,\qquad
 \Phi(r)=\Phi_0+\beta^2y+
 \tfrac12[(a+h\beta^2)/F_R-\beta^4]y^2 .
$$
These functions reproduce $a,b,h,d$, the orbit and all four displays. A small open interval about $R$ has $F>0$. The arbitrary constant $\Phi_0$ sets the time coordinate normalization. Higher derivatives and a global continuation remain free.

## Local density and principal pressures

The diagonal Ricci components multiplied by $R^2$ are $a+2b,\ -a+2h,\ -b+h+d,\ -b+h+d$ in time, radial, polar and azimuthal order. Trace reversal and $G_{\mu\nu}=8\pi G T_{\mu\nu}/c^4$ with $\Lambda=0$ therefore give, in the static orthonormal frame,
$$
 \boxed{\ (\epsilon,p_r,p_t)=K_R(2h+d,\ 2b-d,\ a+b-h),\qquad
 K_R=\frac{c^4}{8\pi G R^2}\ }.
$$
Both tangential pressures equal $p_t$. In particular $p_r/K_R=(1+3x^2)q^2-1$, recovering the pressure measured by the orbit alone, while $\epsilon/K_R=2m'(R)$ explains why the single mass value was insufficient. As a sign check the Schwarzschild vacuum components $(a,b,h,d)=(-2,1,-1,2)m/R$ give positive radial stretching, polar compression and zero in all three stress entries.

The curvature inference uses geometry alone. With the stated field equation the inferred stresses may, as an additional pointwise test, be required to satisfy the dominant energy condition. Its exact checks are $2h+d\ge|2b-d|$ and $2h+d\ge|a+b-h|$. They test the stress at the tagged radius. A neighborhood energy condition would impose a requirement on an extension.

At $m(R)=0$, $F_R=1$, $d=0$, $b=\beta^2$ and $\Delta=x^2\beta^2>0$. If nonnegative $m$ is imposed on both sides of $R$, differentiability at its interior minimum requires $m'(R)=(d+2h)/2=0$. Thus $h=0$, a realizable geometric endpoint with $F\equiv1$. It has $\epsilon=0$, $p_r=2K_R\beta^2>0$, which rules it out under the additional pointwise dominant energy condition. With only $m(R)\ge0$ the inverse includes the endpoint and imposes no such restriction on $h$.

## Two local metrics with the same static record

Choose $x=1,\ q=1/2$, so $T=2\pi R/c,\ (C,D)=(-1,0),\ F_R=\beta^2=1/2,\ b=1/4,\ d=1/2$. Take $a=0$ in both metrics and use the displayed polynomial construction with the same $\Phi_0$. The table gives two distinct sets of derivatives and their outputs.

| $h$ | $RF'_R$ | $R^2\Phi''_R$ | Static $H_r,H_\theta$ | Orbiting $H_r,H_\theta$ | $(\epsilon,p_r,p_t)/K_R$ |
|---:|---:|---:|---|---|---|
| $0$ | $0$ | $-1/4$ | $0,1/4$ | $0,1$ | $(1/2,0,1/4)$ |
| $1/4$ | $-1/2$ | $0$ | $0,1/4$ | $1/4,1$ | $(1,0,0)$ |

The same gain and zero give identical static displays. Both local metrics have positive mass and strictly satisfy the pointwise dominant energy inequalities at the orbit. Even with perfect calibration the static pair loses the information in $h$. The moving radial channel distinguishes the two densities and tangential pressures.

## What the measurement assumes

The period and spin are finite-orbit records. The four tidal readings are local Jacobi-field limits with initially comoving, freely falling test bodies. They require registered radial and polar separations, projection in a locally nonrotating frame at the measurement instant, common sign and response across channels, and a common event or fully registered repeats. A supported static apparatus and a finite-time radial epicyclic measurement have different acceleration terms. A finite arm or sampling interval would require an error law to justify the limit.

The components $a,b,h,d$ and the three ratios to $K_R$ are dimensionless. Scaling $R,T$ together preserves $x,q$ and these radius-unit results, while physical curvatures and stresses scale as $R^{-2}$ for the scaled metric. The calibrated $R$ supplies the physical curvature scale and $c^4/(8\pi G)$ converts it to energy per proper volume or pressure in pascals. Mass-equivalent density is $\epsilon/c^2$. An equation of state, a radial survey and an interior integral enter none of the local reconstruction. No empirical data enter this calculation.

The general geodesic-deviation measurement principle is described by Puetzfeld and Obukhov. The two polar anchors and the restricted spherical inverse above follow from the stated orbital data and the local calculation. [Published article, Physical Review D 93, 044073 (2016)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.93.044073)

The original [signed orbital mass result](spherical_mass_from_one_orbiting_gyroscope.md) and [orbit-only radial pressure and possible densities](radial_pressure_from_a_signed_gyroscope_orbit.md) specify the starting record.
