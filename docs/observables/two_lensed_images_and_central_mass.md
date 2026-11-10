# What two lensed images measure about a compact mass

**Result.** For the supplied thin lens, the two signed positions and calibrated delay determine the redshifted total mass of the compact component (point plus disk, excluding the uniform sheet). At known disk radius $\rho$, the complete two-image census also gives a sharp lower bound on the fraction $f$ in the central point. The bound is strict because equality produces a third ray. Two distinct extended lenses can give exactly the same complete observation.

## Exterior positions, signed delay and mass

Take one point source at positive offset $\beta$ and a transparent, centered, circular lens in geometric optics. The two measured rays are $+p$ and $-m$, with $p>m>\rho>0$ in radians. The measurement associates both arrivals with the same emission, registers their signs against the same lens centre and uses one calibrated clock. The sheet has $0\le\kappa<1$. There is no shear, obscuration, blending or source structure. Circular symmetry makes the vector lens map a scalar multiple of the image vector. Since the source vector is nonzero, each image lies on its axis. The origin is singular for every allowed $f>0$.

Set $\lambda=1-\kappa$. At either exterior ray the signed equation is $\lambda\theta^2-\beta\theta-A=0$. Its root sum and product give
$$
\beta=\lambda(p-m),\qquad A=\lambda pm.
$$
These are the only exterior solutions. Both are on the same exterior potential branch: the radial potential with derivative $A/r$ is $A\log(r/\theta_*)$ plus a common constant for all $r\ge\rho$. Matching continuously to the interior can change that constant, which cancels between the arrivals.

Write $s=p/m>1$ and $B(s)=(s-s^{-1})/2+\log s>0$. Expanding the supplied Fermat potential at the two roots gives
$$
\begin{aligned}
\phi(-m)-\phi(p)
 &=\tfrac12\lambda(m^2-p^2)+\beta(m+p)+A\log(p/m)\\
 &=\tfrac12\lambda(p^2-m^2)+A\log(p/m)=A B(s).
\end{aligned}
$$
Thus the measured delay $\Delta t=t(-m)-t(p)$ must be finite and strictly positive. Every such delay is feasible. It fixes $TA=\Delta t/B(s)$. All nuisance solutions are obtained by choosing any $0<\lambda\le1$ and setting $\kappa=1-\lambda$, $\beta=\lambda(p-m)$, $A=\lambda pm$, $T=\Delta t/[\lambda pm B(s)]$. The source offset, sheet and time coefficient can vary together even at exact positions and delay. A common arrival epoch and potential zero drop out.

Under the conventional calibration $TA=4G(1+z_L)M/c^3$, the mass observable is
$$
M_z=(1+z_L)M=\frac{c^3\,\Delta t}{4G B(s)} .
$$
The measured time unit and known $c,G$ supply the dimensional scale. An independent lens redshift gives $M=M_z/(1+z_L)$. Without that input only the product is fixed. The angle ratio determines the dimensionless factor; absolute registered angular units also enter the reconstruction of $A,\beta,T$. The sheet is external to this definition of compact mass. The source-to-lens correspondence and time calibration are supplied physical assumptions. The DET occupation, clock, tide and radar studies supply no conversion to this lens mass. Muñoz and colleagues motivate the transient point-lens delay baseline. The disk and exact census below are the comparison specified by E55. [Muñoz et al., 2016, v1](https://arxiv.org/abs/1605.00008v1)

## All rays inside and at the edge of the disk

For the interior calculation define
$$
h=\frac{pm}{\rho^2},\qquad C=h-1,\qquad b=\frac{p-m}{\rho},
\qquad x=\frac{|\theta|}{\rho}.
$$
In particular $C>b>0$, since $C-b=(m-\rho)(p+\rho)/\rho^2$. At a negative ray $-\rho x$, the interior lens equation divided by $\lambda\rho$ is
$$
b=N_f(x)=Cx+hf(x^{-1}-x),\qquad 0<x\le1 .
$$
This follows by inserting $fA/\theta+(1-f)A\theta/\rho^2$ for the compact deflection. On the positive side the right-hand side is $-N_f(x)<0$, so it gives no image. At the edge $N_f(1)=C>b$ for every $f$. The deflection agrees with the exterior there, and neither edge point is an image.

Inside $0<x<1$, a negative ray exists precisely where
$$
 f=F(x)=\frac{x(b-Cx)}{h(1-x^2)}.
$$
Only $0<x<b/C<1$ can yield a positive fraction. The function is positive there and tends to zero at both ends. Its derivative has the sign of $b(1+x^2)-2Cx$. The smaller root
$$
x_*=\frac{b}{C+\sqrt{C^2-b^2}}
$$
lies inside $(0,b/C)$; the other is its reciprocal and lies outside the disk. The derivative changes sign from positive to negative at $x_*$. At that point $2Cx_*=b(1+x_*^2)$, so the maximum is
$$
 f_*=\frac{b x_*}{2h}
     =\frac{C-\sqrt{C^2-b^2}}{2h}.
$$
In particular $0<f_*<C/(2h)<1/2$. Counting distinct rays gives the complete decision.

| Central point fraction | Additional rays | Total images |
| --- | --- | --- |
| $0<f<f_*$ | Two distinct negative rays inside the disk | 4 |
| $f=f_*$ | One negative tangent ray at $-\rho x_*$ | 3 |
| $f_*<f\le1$ | None | 2 |

At equality the derivative of $N_f$ vanishes and $N_f''=2hf/x^3>0$, so the tangent is a double root at one distinct angular location. The ideal census counts it. At $f=1$ the exterior and interior laws are those of the same point lens, and the endpoint is included.

## Sharp feasible set and a matched pair

For data satisfying the stated angle domain, a finite positive signed delay and exactly two images, choose **any**
$$
0<\lambda\le1,\qquad f_*<f\le1 .
$$
The exterior formulas above set $\kappa,\beta,A,T$. Assign fractions $f$ and $1-f$ of $A$ to the point and the uniform disk at the given radius. This realizes every recorded ray and the signed delay. The preceding count excludes every other fraction in the model. Hence the redshifted **point** mass ranges over $(f_*M_z,M_z]$, or the physical point mass over $(f_*M,M]$ at known redshift. If only the two exterior rays and their delay are known, every $0<f\le1$ fits them; the strict positive lower bound comes from complete detection of distinct rays, including central and tangent images.

For example choose $p=5\rho/3,\ m=5\rho/4$. Then $h=25/12,\ C=13/12,\ b=5/12,\ x_*=1/5,\ f_*=1/50$. Hold the sheet, total strength, time coefficient and redshift fixed. Fractions $1/25$ and $1/2$ both give exactly $+5\rho/3,-5\rho/4$ and $\Delta t=TA B(4/3)>0$. Both disks carry positive mass, while their central point masses differ. There are no recorded fluxes or other observables to distinguish this pair. Applying the bound to an actual transient would require the stated centre, geometry, clock, source association and complete image census.

## Scientific provenance

DET Quantum Relativity derived the E55 finite inverse. DET Relational State Research independently checked its sign, mass calibration, radial roots, strict endpoint and matched example. Related spherical observables use different measurement records. [Exterior clocks](finite_exterior_clocks_and_total_mass.md) · [Local tides and support](local_mass_from_tides_and_support.md) · [Two-site tides and radar](two_site_tides_and_radar_mass.md)

Frozen author report SHA-256: 5a5b4e260d625a36f46530179424e53132f82a13d7238ff043deed92e8e9df6b

Independent scientific review SHA-256: ea316801e03490e8900bbb9eec762fa717c3ce4b605a51fe0bef5971f9ece186

