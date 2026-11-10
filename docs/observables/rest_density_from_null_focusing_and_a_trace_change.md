# Rest-mass bounds from null Ricci focusing and a change in scalar curvature

In the homogeneous isotropic Einstein model with a conserved collisionless massive gas and a constant nonnegative vacuum energy density, let $U$ be the conserved gas rest energy per unit **first-epoch** proper volume, $b>1$ the registered expansion factor, and $C=1-b^{-3}$. For the measured trace difference $D$ and first-epoch normalized null contraction $B$, the exact data domain is
$$
                       B>0,\qquad 0<D\le CB
$$
with both readings finite. At $D=CB$, the gas is cold and $U=B$. In the interior the exact interval is
$$
              \boxed{\quad D/C<U\le B/H_* \quad}
$$
where the dimensionless $H_*>1$ is the unique one-speed solution defined below. The maximum is attained by a gas of one speed. The lower endpoint is an infimum approached by a cold shell and a progressively faster massive shell. Each construction reproduces the **same** $D,B$ using one population transported between epochs.

## What the two readings measure

Use signature $(-+++)$, a unit comoving four-velocity $u$, and Einstein’s equation $G_{ab}=(8\pi G/c^4)T_{ab}$ with the constant vacuum included on the matter side. For energy density $E$ and isotropic pressure $p$, $T_{ab}=(E+p)u_a u_b+p g_{ab}$. The trace gives $c^4\mathcal R/(8\pi G)=E-3p$. For any nonzero future null tangent $\ell$, the trace term in the Einstein tensor vanishes on contraction. Thus
$$
 D=\frac{c^4}{8\pi G}(\mathcal R_1-\mathcal R_b),\qquad
 B=\frac{c^4}{8\pi G}\frac{R_{ab}\ell^a\ell^b}{(-u\cdot\ell)^2}
   =E_g(1)+p_g(1).
$$
The vacuum contributes $4u_\Lambda$ to each absolute trace and zero to $B$. Every fixed $u_\Lambda\ge0$ is consistent with every admitted construction. Neither absolute scalar level occurs in the inverse. Rescaling an affine tangent multiplies the numerator and denominator of $B$ by the same squared factor. Isotropy makes the normalized result independent of the ray direction. [Two-epoch trace convention](rest_density_from_two_expansion_epoch_curvatures.md) · [Curvature and stress convention](local_density_and_pressure_from_orbit_and_tides.md)

Let $d\mu$ be the nonnegative measure of particle rest energy per initial proper volume, $U=\int d\mu>0$, and $s=|\mathbf p_1|/(mc)$ the initial momentum magnitude for particles of mass $m>0$. At scale factor $a$, the same shell has $\gamma_a=\sqrt{1+s^2/a^2}$. Proper number density dilutes by $a^{-3}$. The shell kernels for $E_g$ and $3p_g$ are $a^{-3}\gamma_a$ and $a^{-3}(\gamma_a-1/\gamma_a)$, respectively. Finite first-epoch energy makes these moments finite through $a=b$. [Ma and Bertschinger, v1, Eq. (52)](https://arxiv.org/pdf/astro-ph/9506072v1#page=19) · [Local rest-density moments](constituent_rest_density_from_local_stress.md)

Write $z=1/\gamma_1$, so $0<z\le1$, and set $c_b=b^{-2}$, $t_b=b^2-1$. The two shell contributions per unit of rest energy are
$$
 H(z)=\frac{4/z-z}{3},\qquad
 d_b(z)=z\left(1-\frac{c_b}{\sqrt{1+t_b z^2}}\right),\qquad
 B=\int H(z)\,d\mu,\qquad D=\int d_b(z)\,d\mu.
$$
In particular, at the second epoch the trace kernel is $b^{-3}/\gamma_b=b^{-2}z/\sqrt{1+t_bz^2}$. The speed variable in both terms of $D$ labels the same conserved shell.

## Sharp domain and upper endpoint

Use $H$ as the dimensionless shell coordinate. It ranges from $1$ (cold) to arbitrarily large finite values. Define
$$
 z(H)=\frac{\sqrt{9H^2+16}-3H}{2},\qquad f(H)=d_b(z(H)),\qquad H\ge1 .
$$
Here $f(1)=C$, $f>0$, and $f(H)\to0$ as $H\to\infty$. Two shape properties control the inverse. The function $z(H)$ is strictly decreasing and strictly convex, with $z''=72/(9H^2+16)^{3/2}$. Also
$$
 d_b'(z)=1-c_b(1+t_bz^2)^{-3/2}>0,\qquad
 d_b''(z)=3c_bt_bz(1+t_bz^2)^{-5/2}>0 .
$$
Consequently $f$ is strictly decreasing and strictly convex. In particular, $f(H)/H$ decreases continuously from $C$ to zero. For every finite $B>0$ and $0<D/B\le C$, the equation
$$
                         \frac{f(H_*)}{H_*}=\frac{D}{B}
$$
has exactly one finite solution $H_*\ge1$. A single isotropic shell there with rest weight $B/H_*$ produces the prescribed observations. Conversely, $D/B$ is an average of $f(H)/H$ with normalized positive weights $H\,d\mu/B$. This proves the claimed necessary and sufficient data domain. Zero $D$ cannot be attained by a nonempty gas of massive particles with finite energy.

For any distribution, normalize by **rest** weight $d\mu/U$. Its mean shell coordinate is $\bar H=B/U$. Jensen’s inequality gives
$$
                  D/U\ge f(\bar H),\qquad
                  D/B\ge f(\bar H)/\bar H.
$$
Monotonicity implies $\bar H\ge H_*$, or $U\le B/H_*$. Strict convexity makes equality possible exactly when the occupied shells share one $H$, hence one speed magnitude. This is compatible with an isotropic distribution of directions and requires no thermal assumption. Independently, $d_b(z)\le C$ gives $U\ge D/C$. Equality in this last inequality requires only cold particles. Then $H=1$ and $D=CB,\ U=B$. At every interior reading both a pure-speed population and mixed-speed populations exist. The two readings alone do not decide which is present.

## A common two-epoch realization for every interior inventory

Fix $0<D<CB$, and choose any $D/C<U<B/H_*$. Put $X=B/U>1$ and $Y=D/U$. The strict inequalities give $f(X)<Y<C$. Choose a cold shell $H=1$ and a second shell $h\ge X$. Allocate to the second shell the **rest fraction** $w=(X-1)/(h-1)$; give the cold shell the remaining $1-w$. Their mean $H$ is exactly $X$, and their mean trace-difference kernel is
$$
             Y(h)=C+(X-1)\frac{f(h)-C}{h-1}.
$$
At $h=X$ this gives $f(X)$. Strict convexity makes the secant slope, and thus $Y(h)$, strictly increasing with $h$; boundedness of $f$ gives $Y(h)\to C$. There is exactly one finite $h>X$ realizing the prescribed $Y$ in this construction. Rest weights $Uw$ and $U(1-w)$ then reproduce $B,D$ exactly. At $U=B/H_*$ take the single shell directly. As $U\downarrow D/C$ with the readings fixed, $X\to BC/D>1$, $Y\to C$, hence $h\to\infty$ and $w\to0$. No limiting particle with $z=0$ is included.

Choose one fixed positive species mass and isotropic directions on each occupied shell. For each constructed history use the same rest weights at $a=1$ and transport them to $a=b$ by the redshift and dilution above. A nonnegative constant vacuum may even be held identical throughout the family. Expanding Einstein histories exist for these shells: as one existence choice take spatially flat slices and the positive solution of $(\dot a/a)^2=8\pi G(E_g(a)+u_\Lambda)/(3c^2)$ in proper time. The shell moments give $aE_g'(a)=-3(E_g+p_g)$, as follows by differentiating $a^{-3}\gamma_a$. Thus the continuity equation and the second Friedmann equation agree. The positive continuous expansion rate reaches any specified finite $b>1$ from $1$ in finite time. Neither spatial flatness nor an observed expansion rate is needed to obtain the bounds.

## Why the hot-inventory ambiguity changes

At high initial Lorentz factor, the decline kernel goes to zero while $H$ grows without bound. With only $D>0$, a single shell can keep $D$ fixed by increasing its rest weight to $D/f(H)$; its predicted $B=D H/f(H)$ then diverges. An independently calibrated **finite** null reading rules out this sequence. Already $U\le E_g(1)\le B$; the simultaneous decline tightens the upper bound to $B/H_*$. Very fast particles remain possible in a sufficiently small rest fraction. Thus a bound on total inventory does not impose a maximum constituent speed below $c$.

The exact endpoints refer to specified $b,D,B$. At fixed $b>1$ the upper bound varies continuously with $D/B$ in the interior. Near the hot end $f(H)\sim4(1-b^{-2})/(3H)$, so $U_{\max}/B\sim\sqrt{3(D/B)/[4(1-b^{-2})]}$. A small noisy decline is ill-conditioned for a *relative* rest-density inference. As $b\to1$, $C\to0$, and the subtraction of two nearby curvatures also requires adequate absolute precision. Exact cold equality cannot be certified from an error interval that includes interior ratios. No precision or sampling model is supplied.

## What a null readout requires

The input is a local curvature projection at the first epoch in the registered comoving frame. For example, in geometric optics consider a twist-free, affinely parameterized infinitesimal bundle away from a caustic, with positive area radius $J\propto\sqrt{\mathcal A_{\rm beam}}$. In the stated curvature sign convention, writing $|\sigma|^2=\sigma_{ab}\sigma^{ab}/2$ for the screen shear term, the optical equation gives
$$
               R_{ab}\ell^a\ell^b=-2\bigl(J''/J+|\sigma|^2\bigr).
$$
Primes are local affine derivatives for that same tangent. A readout through this route needs the affine derivatives, the comoving normalization $-u\cdot\ell$, and either a justified zero shear or a calibrated shear correction. The squared optical terms scale consistently under constant affine rescaling. A finite beam, finite baseline, lensing distortion or distance versus redshift alone cannot be substituted for the local contraction without a supported conversion and error bound. No distance approximation or fit enters this inverse. [Demiański et al., optical scalar equations, A&A 411 (2003)](https://www.aanda.org/articles/aa/pdf/2003/45/aa4018.pdf#page=2)

$D,B,U$ have energy per proper volume units. $U/c^2$ is the first-epoch rest-mass density and $U/(b^3c^2)$ the second-epoch density. Total conserved rest mass in a comoving cell additionally requires its initial proper volume. Readings in reference-length curvature units yield densities in $c^4/(8\pi G L^2)$ until $L$ is calibrated. The sources, the expansion ratio and the common curvature scale must be registered across epochs; a constant common scalar offset cancels in $D$, while a drifting offset does not. The measurements give neither individual particle mass nor number, vacuum level, full speed distribution, elapsed expansion time or a native DET mass scale. No empirical observations enter the result.
