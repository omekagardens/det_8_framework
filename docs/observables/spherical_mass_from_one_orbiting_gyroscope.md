# Spherical mass from one orbiting gyroscope

Use an exactly circular equatorial geodesic in a smooth static spherical annulus with metric $ds^2=-A(r)c^2dt^2+B(r)dr^2+r^2d\Omega^2$, where $A,B>0$ and $r$ is areal radius. The sphere at the observed radius $R$ is untrapped and has nonnegative Misner–Sharp mass. Prepare a torque-free outward unit spin and retain its signed outward and forward components $C,D$ at the first forward return to the stationary meridian. Let $T$ be the period on the orbiting proper clock.

For an admissible signed record, define $x=2\pi R/(cT)$, $\gamma=\sqrt{1+x^2}$, and take $2\pi q=\arg(C-iD)$ in $[0,2\pi)$. The orbit identifies the mass of the observed sphere:
$$
 M_{\rm MS}(R)=\frac{c^2R}{2G}\bigl[1-(1+x^2)q^2\bigr].
$$
The complete compatibility test is finite $R,T>0$, real $C,D$ with $C^2+D^2=1$, and $0<q\le 1/\gamma$. The signed direction picks a single phase on this arc. A radial projection alone can leave two different masses.

## The orbit and its moving axes

Use proper length $s=c\tau$ and unit timelike tangent $u=dx^\mu/ds\,\partial_\mu$ with $u\cdot u=-1$. On the equator, use the static orthonormal vectors $e_0=(c\sqrt A)^{-1}\partial_t$, $e_r=B^{-1/2}\partial_r$, and $e_\phi=r^{-1}\partial_\phi$. All metric coefficients and first derivatives below are evaluated at $R$ unless an argument is shown. Time and azimuth are Killing coordinates, so their velocities are constant on the circular geodesic. The first forward return gives $d\phi/ds=2\pi/(cT)=x/R$. Normalization and future orientation then give
$$
 u=\gamma e_0+x e_\phi,\qquad \beta=x/\gamma,\qquad
 E=x e_0+\gamma e_\phi .
$$
Here $c\beta$ is the speed seen by a static observer, inferred from the supplied period and radius. Projecting $e_\phi$ into $u^\perp$ gives $e_\phi+xu=\gamma E$. Thus $E$ is precisely the designated forward unit axis and $e_r$ is the outward rest axis.

Put $h=A'/(2A\sqrt B)$ and $k=1/(R\sqrt B)$. The metric connection on the equator gives $\nabla_{e_0}e_0=h e_r$, $\nabla_{e_\phi}e_\phi=-k e_r$, $\nabla_{e_0}e_r=h e_0$, and $\nabla_{e_\phi}e_r=k e_\phi$. The two mixed time-azimuth derivatives vanish. Equatorial reflection preserves the orbital plane. The radial geodesic equation is $\gamma^2h-x^2k=0$, hence
$$
 \frac{RA'}{2A}=\beta^2=\frac{x^2}{1+x^2}\in(0,1).
$$
In particular, the proper period fixes the logarithmic derivative of the lapse coefficient. Its value $A(R)>0$ is freely normalized.

The derivative $\nabla_u e_r=\gamma h e_0+x k e_\phi$ reduces to $\beta k E$ using the geodesic equation. Metric compatibility, $\nabla_u u=0$, and equatorial symmetry give $\nabla_u E=-\beta k e_r$. For a parallel unit spin $S=P e_r+Q E$, the normal component stays zero and
$$
 \frac{dP}{d\phi}=qQ,\qquad \frac{dQ}{d\phi}=-qP,\qquad
 q=\frac{\beta k}{d\phi/ds}=\frac1{\gamma\sqrt B}.
$$
Starting with $(P,Q)=(1,0)$ gives $(C,D)=(\cos 2\pi q,-\sin 2\pi q)$ at the first return. The initial drift is toward the backward axis. $P,Q$ are components in the comoving orthonormal screen. Launch and return have distinct times on the same stationary meridian, whose registered axes supply the comparison.

## Why the arc is both necessary and sufficient

The supplied Misner–Sharp definition gives $\mu=2GM_{\rm MS}(R)/(c^2R)=1-B^{-1}$, since the squared norm of the areal-radius covector is $g^{-1}(dr,dr)=1/B$. The declared $0\le\mu<1$ yields $1\le B<\infty$. For each positive finite $x$, $0<q\le1/\gamma<1$. The included endpoint $q=1/\gamma$ has zero mass. The excluded limit $q\downarrow0$ has $\mu\uparrow1$. The pair $(1,0)$ would require an integer $q$ and is impossible. The only possible $D=0$ has $C=-1$ and $q=1/2$, allowed exactly when $x\le\sqrt3$. Any two phases with the same signed pair differ by an integer in $q$, so at most one fits. Inverting $B^{-1}=\gamma^2q^2$ now gives the displayed singleton mass. Records failing the test have an empty mass set. [Hayward, §II, Eq. (4)](https://arxiv.org/pdf/gr-qc/9408002v2)

To realize every allowed record, choose any $A_0>0$, take an annulus $R/2<r<3R/2$, and use
$$
 A(r)=A_0\exp\!\bigl[2\beta^2(r-R)/R\bigr],\qquad
 B(r)=\frac1{\gamma^2q^2}.
$$
Both coefficients are smooth and positive. At $R$, $A'(R)=2A_0\beta^2/R$. The equatorial path with $r=R$, $dt/ds=\gamma/(c\sqrt{A_0})$, and $d\phi/ds=x/R$ has the normalized tangent above and satisfies every geodesic equation. It returns after $T$, and the transported outward spin gives exactly the stipulated pair. This also realizes zero geometric mass with nonzero orbital speed when $q=1/\gamma$. The construction requires only a local metric and an exactly prepared geodesic.

## Keeping only the radial projection

For finite $R,T>0$ and $C\in[-1,1]$, let $a=\arccos(C)/(2\pi)$. Intersect the set $\{a,1-a\}$ with $(0,1/\gamma]$ and evaluate the mass formula on each distinct survivor. All reduced records outside these input ranges are impossible. At $C=-1$ the two phases coincide. At $C=1$ both fail. For $-1<C<1$ two surviving phases give distinct masses because $1-\gamma^2q^2$ strictly decreases for $q>0$. An empty intersection rules out the record. Each survivor is realized by the same annulus construction.

For the synthetic fixture $x=3/4$ and $C=-1/2$, one has $T=8\pi R/(3c)$, $\gamma=5/4$, $\beta=3/5$, and $q_{\max}=4/5$. The two possibilities are

| Missing forward component $D$ | $q$ | Constant $B$ | $M_{\rm MS}(R)/(c^2R/(2G))$ |
|---|---:|---:|---:|
| $-\sqrt3/2$ | $1/3$ | $144/25$ | $119/144$ |
| $+\sqrt3/2$ | $2/3$ | $36/25$ | $11/36$ |

Take $A(r)=\exp[18(r-R)/(25R)]$ for both and use the corresponding table entry for $B(r)$ throughout the annulus. These are two realized local metrics with identical $R,T,C$. The larger mass gives the negative forward component.

## Vacuum check and calibration

For the Schwarzschild check only, take $m=GM_0/c^2>0$, $y=m/R$, and $R>6m$. With $A(r)=1-2m/r,\ B(r)=1/A(r)$, the orbit constraint gives $\beta^2=y/(1-2y)$, $x^2=y/(1-3y)$, and $\gamma^2=(1-2y)/(1-3y)$. Thus $T=(2\pi R/c)\sqrt{(1-3y)/y}$ and $q=\sqrt{1-3y}$, the circular-geodesic transport frequency per radian of azimuth in Rothman, Ellis and Murugan. The signed readout is $C=\cos(2\pi\sqrt{1-3y})$, $D=-\sin(2\pi\sqrt{1-3y})>0$ on this interval. Substitution in the inverse gives $1-\gamma^2q^2=2y$ and $M_{\rm MS}=M_0$. [Rothman, Ellis and Murugan, §3.3, Eqs. (3.15)–(3.16)](https://arxiv.org/pdf/gr-qc/0008070v4)

Under a constant future-oriented time change $t'=\lambda t$, $A$ becomes $A/\lambda^2$. The ratio $A'/A$ (radial derivative over value), the static unit axis $e_0$, $B$, and the proper record are invariant. The length $R$ is the calibrated areal radius, $T$ the moving clock's proper time, and $x,\gamma,\beta,q,\mu,C,D$ are dimensionless. The supplied $c^2R/G$ has units of mass. A common physical dilation of $R$ and $T$ keeps the dimensionless data fixed and scales the mass in proportion to $R$.

The inference describes the geometry of one sphere. Recovering integrated local material energy would require a matter model and an interior slice. An asymptotic mass requires an exterior and appropriate behavior at infinity. A fluid globe and a thin shell can share a vacuum exterior while containing different integrated local matter energies. [Proper matter energy from an interior baseline](static_radial_length_and_proper_matter_energy.md) Physical calibration of a DET record or mass unit would require separate evidence.

In the Kottler exterior $B^{-1}=1-2GM/(c^2R)-\Lambda R^2/3$. Substitution gives $M_{\rm MS}(R)=M+\Lambda c^2R^3/(6G)$. The central parameter $M$ inferred from falling clocks agrees with this sphere mass in the Schwarzschild case. [Central mass from crossing observers](central_mass_from_crossing_observers.md)
