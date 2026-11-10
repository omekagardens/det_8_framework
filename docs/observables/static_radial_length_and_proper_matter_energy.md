# One radial rod and the matter energy of two static sources

At areal radius $R=6GM/c^2$, the shell gives a centre-to-surface rod length of $R$. The uniform fluid gives $\sqrt3\,R\arcsin(1/\sqrt3)>R$. Either length selects its source and its integrated local matter energy within the stipulated pair. Their entire vacuum exteriors and their central accelerometer readings agree.

## What the record fixes

Write $m=GM/c^2$ for the length associated with the measured ADM mass $M>0$, and use $G=c=1$ in the calculation. Write $e=GE_{\rm mat}/c^4$ for the integrated local matter energy in length units. Define the compactness $b=2m/R$, $s=\sqrt{1-b}$, and $x=r/R$. Here $b=1/3$. The areal label $r$ assigns area $4\pi r^2$ and great-circle circumference $2\pi r$. The common vacuum exterior has
$$
 ds^2=-N^2dt^2+B^{-2}dr^2+r^2d\Omega^2,\qquad N=B=\sqrt{1-2m/r},\quad r>R .
$$
The coordinate time uses the Killing field normalized at infinity. All exterior matter densities and pressures vanish. Surface values below refer to the corresponding interior limit or the explicitly specified material layer.

On the hypersurface orthogonal to the static observers, $d\ell=dr/B$ along a radial line, and $dV=r^2d\Omega\,d\ell$. The extra measurement is $L=\int_0^R d\ell$ on that slice with the endpoint tagged by its area. The coordinate interval in $r$ is $R$ in both preparations. A radial round-trip signal instead accumulates coordinate time $2\int_0^R d\ell/N$, and a central clock multiplies this by $N(0)$. The rod compares spatial distances and requires no clock synchronization by light exchange.

## Regular uniform fluid F

For constant local energy density $\epsilon$, the enclosed mass function is $m(r)=4\pi\epsilon r^3/3=m x^3$, fixing $\epsilon=3m/(4\pi R^3)$. The regular Schwarzschild interior solution with $p(R)=0$ gives
$$
 B_F=\sqrt{1-bx^2},\qquad
 N_F=(3s-B_F)/2,\qquad p_F=\epsilon\,\frac{B_F-s}{3s-B_F}.
$$
Here $s=\sqrt{2/3}$, so $3s-1>0$. The pressure is positive inside, has finite central value $\epsilon(1-s)/(3s-1)$, and vanishes at $R$. Both $N_F(R)$ and $B_F(R)$ equal $s$. The normal lapse derivative $B_FN_F'=br/(2R^2)$ equals the exterior value $m/R^2$ at the surface, where prime denotes $d/dr$. Together with matched areal radius and $B$, this gives matching extrinsic curvature and hence zero surface stress despite the jump in bulk density. The static observer's outward acceleration component in its orthonormal frame is $d\ln N/d\ell=B N'/N$. It is zero at the centre. [Martin and Visser, section 5, equations 30–35 and 39](https://arxiv.org/pdf/gr-qc/0306038v1)

The proper length and matter-energy integrals are
$$
 \frac{L_F}{R}=\int_0^1\frac{dx}{\sqrt{1-bx^2}}
 =\frac{\arcsin\sqrt b}{\sqrt b},\qquad
 \frac{e_F}{m}=3\int_0^1\frac{x^2\,dx}{\sqrt{1-bx^2}}
 =\frac{3}{2b^{3/2}}\left(\arcsin\sqrt b-\sqrt b\,s\right).
$$
The energy counts each fluid element with its proper volume. Both antiderivatives follow by setting $\sqrt b\,x=\sin\chi$. Schwarzschild used the same angle for the interior ruler length, circumference radius, and local density times proper volume. [Schwarzschild, equations 37–43, Antoci translation](https://arxiv.org/pdf/physics/9912033v1)

## Self-supported material shell S

The flat interior has $B_S=1,\ N_S=s$ throughout. This constant lapse matches the exterior at the shell. The central static acceleration vanishes, and the radial rod reaches the material surface at $L_S=R$. The shell has zero proper thickness.

Take the normal to point from interior to exterior, toward increasing radius on both sides, and use the jump $[K]=K_+-K_-$ for each extrinsic-curvature component. With $K^a{}_b$ defined by the tangential projection of $\nabla n$, the mixed components for a static surface are $K^\tau{}_\tau=B N'/N$ and $K^\theta{}_\theta=K^\phi{}_\phi=B/R$. Their jumps are $m/(R^2s)$ and $(s-1)/R$, respectively. The junction condition $8\pi S^a{}_b=-([K^a{}_b]-\delta^a{}_b[K^d{}_d])$ yields $S^a{}_b=\mathrm{diag}(-\Sigma,P,P)$ in the surface rest frame, with
$$
 \Sigma=\frac{1-s}{4\pi R},\qquad
 P=\frac{1}{8\pi R}\left(\frac{1-m/R}{s}-1\right)
  =\frac{(1-s)^2}{16\pi R s},\qquad
 e_S=4\pi R^2\Sigma=R(1-s)=\frac{2m}{1+s}.
$$
Both the surface energy density and the *tangential pressure* are positive. There is zero radial surface stress and vacuum on each side. The jumps determine the pressure that supports the static shell under its own gravity. The local shell energy obeys $m=e_S-e_S^2/(2R)$. Martínez denotes our exterior $m$ by $m$, and our local $e_S$ by $M$ when $G=c=1$. [Martínez, section II, equations 2.4–2.6](https://arxiv.org/pdf/gr-qc/9601037v2)

## Exact inverse at the stipulated radius

Let $\theta=\arcsin(1/\sqrt3)$, and let $q_F,q_S$ be the dimensionless entries in the final column. The baseline record contains the calibrated common exterior, tagged radius, and zero central static acceleration.

| Preparation | Rod reading $L/R$ | Local matter energy $q=E_{\rm mat}/(Mc^2)=e/m$ |
| --- | --- | --- |
| F · uniform fluid | $\sqrt3\,\theta$ | $q_F=\frac{9\sqrt3}{2}(\theta-\frac{\sqrt2}{3})$ |
| S · material shell | $1$ | $q_S=\frac{2}{1+\sqrt{2/3}}$ |

The fluid rod integrand exceeds unity for every $0<x\leq1$ and is bounded by $1/s$. This proves the lengths are finite and strictly ordered. For the energies substitute $u=x^3$ in the fluid integral and integrate the shell expression in the following form,
$$
 q_F=\int_0^1(1-bu^{2/3})^{-1/2}du,\qquad
 q_S=\int_0^1(1-bu)^{-1/2}du.
$$
Since $u^{2/3}>u$ for $0<u<1$, these integrals prove $q_F>q_S>1$ at $b=1/3$.

| Exact retained record | Compatible sources | Compatible local matter energies |
| --- | --- | --- |
| Baseline alone | $\{F,S\}$ | $\{Mc^2q_F,Mc^2q_S\}$ |
| Baseline and $L=R$ | $\{S\}$ | $\{Mc^2q_S\}$ |
| Baseline and $L=R\sqrt3\,\theta$ | $\{F\}$ | $\{Mc^2q_F\}$ |
| Baseline and any other length | $\varnothing$ | $\varnothing$ |

Failure of an earlier condition, such as nonzero central acceleration, a different exterior from the supplied one, or an inconsistent surface tag, also makes both sets empty, whatever length is appended. Each length selects only the energy in its own row.

## Why both sources have the measured active mass

Let $p_r,p_\theta,p_\phi$ be local principal stresses. For the infinity-normalized static Killing field and a slice with regular centre, the Komar mass in length units is
$$
 m_K=\int N(\epsilon+p_r+p_\theta+p_\phi)\,dV .
$$
Equivalently its exterior flux on a sphere is $r^2BN'=m$. In the fluid $N_F(\epsilon+3p_F)=\epsilon B_F$ by substitution, so the volume factor $B_F^{-1}$ cancels. Thus $m_K=4\pi\epsilon\int_0^R r^2dr=m$. [Mazur and Mottola, section III, equations 3.15–3.18](https://arxiv.org/pdf/1501.03806v1)

For the shell choose a radial proper-distance coordinate $\lambda$ through the surface, increasing outward with $\lambda=0$ there. Then $dV=r(\lambda)^2d\Omega\,d\lambda$. The distributional entries in the static frame are $\epsilon=\Sigma\delta(\lambda),\ p_r=0,\ p_\theta=p_\phi=P\delta(\lambda)$. Pairing the proper-distance delta with a continuous test function samples its surface value with area $R^2d\Omega$. In particular $N=s$ on the layer. This avoids multiplying a coordinate delta by a discontinuous areal-coordinate radial metric coefficient. There is one whole shell contribution to the all-space integral,
$$
 m_K=4\pi R^2s(\Sigma+2P)
 =R\left[s(1-s)+\frac{(1-s)^2}{2}\right]
 =\frac R2(1-s^2)=m .
$$
The factor of two counts the two tangential stresses. The vacuum on either side of this layer contributes zero to the matter integral. For both sources the integrated local energy exceeds the common active mass in geometrized units.

## Units and weak-field check

Lengths $R,L,r,\ell,m,e$ above have units of length. A length-valued mass converts to kilograms by $c^2/G$, and a length-valued energy converts to joules by $c^4/G$. Thus the absolute rod readings multiply $R=6GM/c^2$ and the absolute energy readings multiply $Mc^2$ by their respective tabulated ratios. The ratios alone carry no independent calibration of $M$ or $R$. Multiply geometric $\epsilon,p_F$, of units $\mathrm{length}^{-2}$, by $c^4/G$ to obtain bulk energy density or pressure in $\mathrm{J/m^3}$. Multiply geometric $\Sigma,P$, of units $\mathrm{length}^{-1}$, by $c^4/G$ for surface energy or tangential force per length in $\mathrm{J/m^2}=\mathrm{N/m}$. The proper-distance delta has inverse-length units.

For a check within the same two families, let $b=2GM/(Rc^2)\to0^+$. Taylor expansion of the integrated expressions gives
$$
 L_F/R=1+b/6+O(b^2),\quad L_S/R=1,\qquad
 e_F/m=1+3b/10+O(b^2),\quad e_S/m=1+b/4+O(b^2).
$$
The leading excesses $E_{\rm mat}-Mc^2$ are $3GM^2/(5R)$ for the fluid and $GM^2/(2R)$ for the shell. Their signs and ordering agree with the exact integrals. The decision table uses the exact compactness $1/3$.

The inference assumes the two specified static GR equilibria, calibrated units, and ideal test rods. The matter integral counts energy measured in the local matter frame. Identifying it with baryonic rest energy requires additional matter data. Stability, a physical release process, and an inverse for arbitrary density profiles lie outside this two-source calculation.
