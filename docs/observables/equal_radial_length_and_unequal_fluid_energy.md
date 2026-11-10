# One radial rod leaves the proper matter energy undetermined

At the prescribed areal radius $R=6GM/c^2$, there is a continuous family of regular fluid stars with the same Schwarzschild exterior, zero central holding acceleration and exactly the same centre-to-surface proper length. Their densities decrease strictly outward, their pressures are isotropic, and their integrated local matter energies vary. The rod distinguishes the two particular sources in CL082. Extending the allowed interiors to positive, decreasing-density fluids removes that energy inference. [Shell and uniform-fluid comparison](static_radial_length_and_proper_matter_energy.md)

## A neighbourhood of fluid equilibria

Use $G=c=1$ until the final conversion. Write $m=GM/c^2$ for the exterior mass in length units, $u(r)$ for enclosed mass, $q(r)=1-2u(r)/r$, and $N=e^\nu$ for the lapse. In areal radius the static line element is $-N^2dt^2+dr^2/q+r^2d\Omega^2$. Local energy density is $\rho=u'/(4\pi r^2)$. With $x=r/R$, start from
$$
 u_\eta(r)=m[(1+\eta)x^3-\eta x^5],\qquad
 \rho_\eta(r)=\frac{m}{4\pi R^3}[3(1+\eta)-5\eta x^2].
$$
For $0<\eta<1$, the density is positive through the surface and strictly decreasing for $0<r\le R$. The mass is $m$ at $R$. Moreover $u_\eta/r=(m/R)[(1+\eta)x^2-\eta x^4]$ increases strictly from zero to $m/R$, so $q\ge 2/3$.

Choose two nonzero smooth nonnegative functions $h_1,h_2$ of mass dimension, compactly supported respectively in $R/4<r<R/3$ and $2R/3<r<3R/4$. For example each can be $m$ times a smooth bump in the indicated interval of $x$. Vary the mass profile by
$$
                   u_{\alpha,\beta}=u_\eta+\alpha h_1+\beta h_2 .
$$
Each perturbation redistributes density within its own annulus, with zero net change of enclosed mass outside it. Both vanish near the centre and the surface. For fixed $\eta>0$, the baseline density and the magnitude of its negative slope have positive minima on the closed annuli. Bounded first and second derivatives of the bumps therefore preserve positive, outward-decreasing density for sufficiently small coefficients of either sign. The same neighbourhood can be chosen to keep $q$ uniformly positive.

It remains to supply a regular pressure for every profile used. Put $y=r^2$ and $\mu(y)=u(r)/r^3$, extended at the origin by its finite limit. Both $\rho$ and $\mu$ are smooth in $y$ up to the centre since the central profile is the unperturbed polynomial. The perfect-fluid equations have the regular form
$$
 \frac{dp}{dy}=-\frac{(\rho+p)(\mu+4\pi p)}{2(1-2y\mu)},\qquad
 \frac{d\nu}{dy}=\frac{\mu+4\pi p}{2(1-2y\mu)},\qquad
 p(R^2)=0,\quad \nu(R^2)=\tfrac12\log(1-2m/R).
$$
These are the isotropic hydrostatic and lapse equations with exterior time normalized at infinity. [Martin and Visser, §§3–5](https://arxiv.org/pdf/gr-qc/0306038v1)

At $\eta=\alpha=\beta=0$ the constant-density Schwarzschild solution has $\rho_*=3m/(4\pi R^3)$ and maximum pressure $p_c=\rho_*(1-s)/(3s-1)<\rho_*$, where $s=\sqrt{2/3}$. Hence $\rho_*-p$ has a strictly positive uniform margin on the full interval. On a bounded neighbourhood of this pressure solution with $1-2y\mu$ bounded away from zero, the pressure equation is uniformly locally Lipschitz in $p$. Its coefficients converge uniformly to the reference coefficients as the three parameters go to zero. Continuous dependence for the terminal-value ODE on the compact interval gives existence down to $y=0$ and uniform closeness to the reference pressure. Choose $\eta>0$ sufficiently small first, then restrict $(\alpha,\beta)$ further so that $p<\rho$ everywhere. At any zero of $p$ the inward derivative is strictly positive since $\rho,\mu>0$. Thus $p>0$ inside and $p=0$ at the surface.

Integrating the bounded lapse equation gives finite $\nu$ and $N>0$. At the centre $q=1+O(r^2)$ and $\nu'(r)=O(r)$, so the geometry is regular and the static holding acceleration $\sqrt q\,\nu'$ vanishes there. At $R$, $q=s^2$, $N=s$, and the pressure condition gives $\nu'(R)=m/(R^2s^2)$, exactly the exterior value. The induced metric and the extrinsic-curvature components $\sqrt q\,\nu'$ and $\sqrt q/R$ agree across the surface with the same outward normal. The permitted density jump to vacuum introduces no material layer. Each constructed interior thus matches the same exterior at the same areal radius.

## Holding the length exactly fixed

The rod and the local matter energy on the static slice are
$$
 L[u]=\int_0^R w\,dr,\qquad e[u]=\int_0^R u' w\,dr,\qquad
                         w=(1-2u/r)^{-1/2}.
$$
The energy expression uses $dV=4\pi r^2w\,dr$ and the fluid-frame energy density. Both functionals are smooth in $(\alpha,\beta)$ there because the bumps have compact interior support and $q$ is bounded away from zero. For an interior mass perturbation $h$,
$$
 \begin{aligned}
 DL[h]&=\int_0^R \frac{w^3}{r}h\,dr,\\
 De[h]&=\int_0^R \left(wh'+u'\frac{w^3}{r}h\right)dr
       =\int_0^R\frac{w^3}{r}\frac{u}{r}h\,dr .
 \end{aligned}
$$
The boundary term vanishes because $h$ has interior support. Differentiating $w$ gives $w'=w^3(u'/r-u/r^2)$, so the $u'$ terms cancel. The energy response per unit length response therefore samples $u/r$.

Evaluate these derivatives at $u_\eta$. Let $l_i=DL[h_i]>0$ and $k_i=De[h_i]/l_i$. Each $k_i$ is the average of $u_\eta/r$ on its annulus with positive weight $w^3h_i/r$ wherever $h_i>0$. The averaged quantity $u_\eta/r$ increases strictly, and the entire second annulus lies outside the first. Hence $k_1<k_2$.

The common observed rod value is the definite integral
$$
 L_* = L[u_\eta]
     =R\int_0^1\!\left[1-\tfrac13((1+\eta)x^2-\eta x^4)\right]^{-1/2}dx .
$$
Since $\partial_\beta L=l_2>0$, the implicit function theorem gives a smooth $\beta(\alpha)$, with $\beta(0)=0$, such that $L[u_{\alpha,\beta(\alpha)}]=L_*$ **exactly** throughout an open interval about zero. Its slope at zero is $-l_1/l_2$. Along that exact length level,
$$
 \left.\frac{d}{d\alpha}e[u_{\alpha,\beta(\alpha)}]\right|_0
       = l_1(k_1-k_2)<0 .
$$
Consequently the baseline and every sufficiently small positive $\alpha$ on this curve are two attainable equilibria with identical rod readings and unequal energies. The derivative establishes the strict energy change along a curve on which the equality of readings has already been proved.

## Energy and physical meaning

The mass integral $u(R)=\int_0^R4\pi r^2\rho\,dr=m$ is common. The proper-volume integral $e=\int\rho\,dV$ varies, and each $e>m$ since $u'>0$ and $w>1$ inside. As an equilibrium check, the same pressure and lapse equations give $(r^2\sqrt q\,N')'=4\pi r^2N(\rho+3p)/\sqrt q$. The flux vanishes at the regular centre and equals $m$ at the surface. Thus the pressure- and lapse-weighted static mass integral agrees with the common exterior mass even as the local matter energies differ.

The rod gives the proper radial length $L$ in metres. The areal radius $R$ is fixed separately by the surface area $4\pi R^2$. Restoring units gives exterior mass $M=c^2m/G$ in kilograms and proper matter energy $E_{\rm mat}=c^4 e/G$ in joules. Geometric $\rho$ and $p$ multiply by $c^4/G$ to give energy density and pressure. The difference from $Mc^2$ compares two specified energy measures. Baryon rest energy or extractable work would require additional matter or process information.

The proof assumes the static slice, calibrated radial rod and surface area, common exterior time normalization and the existence of the stated perfect-fluid preparations. It uses freedom in the density profile and imposes no shared material equation of state, sound speed or dynamical stability criterion. The conclusion concerns what an exact rod reading can establish in that equilibrium class.
