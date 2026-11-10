# Areal radius and spherical mass from three local polar tides

A circular geodesic carries an initially outward torque-free gyroscope. Record the proper period and signed final spin on its first forward return. At one event compare three polar tidal readings, one on the orbit and two on freely falling observers with known, equal and opposite tangential boosts relative to it. The three instruments have a common positive gain and additive zero, both unknown. In a static spherical annulus these observations identify the orbit’s areal radius and Misner–Sharp mass. An external areal ruler is unnecessary; the calibrated proper clock and the supplied constants $c$ and $G$ set the dimensions.

## Metric and observations

Use
$$
 ds^2=-A(r)c^2dt^2+B(r)dr^2+r^2d\Omega^2,\qquad A,B>0
$$
on a smooth annulus, with areal radius $r$. At the circular equatorial orbit $r=R>0$, let
$$
 e_0=(c\sqrt A)^{-1}\partial_t,\quad e_\phi=R^{-1}\partial_\phi,
 \quad n=R^{-1}\partial_\theta.
$$
Unit four-vectors have norm $-1$, with worldline parameter $s=c\tau$. Write
$$
 \omega=2\pi/T,\quad x=\omega R/c>0,\quad
 \gamma=\sqrt{1+x^2},\quad \beta=x/\gamma,
 \quad u=\gamma e_0+x e_\phi,\quad E=x e_0+\gamma e_\phi.
$$
The circular condition is
$$
 \frac{RA'}{2A}=\beta^2.
$$
Indeed the coordinate radial geodesic equation after substituting the static-frame components of u is
$$
 0=\frac{\gamma^2 A'}{2AB}-\frac{x^2}{BR},
$$
which gives that condition. The accepted signed spin record gives
$$
 C^2+D^2=1,\qquad
 q=\frac{\arg(C-iD)}{2\pi},\qquad
 q=\frac1{\gamma\sqrt B},
$$
where the argument is in $[0,2\pi)$. Positive finite radius, nonzero forward orbit and $1\le B<\infty$ imply $0<q<1$ and $\gamma q\le1$. The initial spin is outward and torque-free; the signed forward component is retained at the first forward meridian return. No extra turns or unsigned phase are substituted.

Define the Riemann convention by
$R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}+\Gamma^\rho_{\mu\alpha}\Gamma^\alpha_{\nu\sigma}-\Gamma^\rho_{\nu\alpha}\Gamma^\alpha_{\mu\sigma}$.
Then polar Jacobi acceleration per separation is $-K(W)$, with
$K(W)=c^2R(n,W,n,W)$. The recorded outputs are
$$
 z_0=b+gK(u),\qquad z_\pm=b+gK(W_\pm),\qquad
 W_\pm=\cosh\lambda\,u\pm\sinh\lambda\,E,\quad g>0,\ b\in\mathbb R.
$$
The known finite $\lambda>0$ is a local relative rapidity, not a measured static orbital velocity. Only $u$ must remain circular. The other two tangents are initial conditions for local freely falling test observers.

## 2. General spherical polar curvatures

The relevant coordinate connection entries are
$$
 \Gamma^r_{tt}=\frac{c^2A'}{2B},\quad
 \Gamma^\theta_{r\theta}=\frac1r,\quad
 \Gamma^r_{\theta\theta}=-\frac rB,\quad
 \Gamma^r_{\phi\phi}=-\frac{r\sin^2\theta}{B},\quad
 \Gamma^\theta_{\phi\phi}=-\sin\theta\cos\theta.
$$
They give
$R_{\theta t\theta t}=c^2rA'/(2B)$ and
$R_{\theta\phi\theta\phi}=r^2\sin^2\theta(1-B^{-1})$.
Consequently the static orthonormal components at the equator are
$$
 \alpha:=c^2R(n,e_0,n,e_0)
       =\frac{c^2A'}{2ABR},\qquad
 \chi:=c^2R(n,e_\phi,n,e_\phi)
       =\frac{c^2}{R^2}(1-B^{-1}),\qquad
 R(n,e_0,n,e_\phi)=0.                            \tag{1}
$$
The mixed component vanishes in the static diagonal spherical metric. These formulas require no matter equations. They contain no $A''$ or $B'$, which occur in other curvature sections with radial legs, and no higher radial derivatives. This polar/tangential design does not sample those other sections. The only lapse derivative $A'/A$ is eliminated by the circular condition. The lapse normalization $A(R)$ is unmeasured and cancels.

Using $B^{-1}=\gamma^2q^2$ and the circular condition,
$$
 \alpha=\omega^2q^2,\qquad
 \chi=\frac{c^2}{R^2}(1-\gamma^2q^2).
$$
Introduce the useful dimensionless unknown
$$
 \kappa=\gamma/x=1/\beta>1,\qquad
 x=(\kappa^2-1)^{-1/2},\qquad a_q=1-q^2>0.
$$
Transformation of the two-plane quadratic curvature form gives
$$
 K_0:=K(u)=\gamma^2\alpha+x^2\chi=\boxed{\omega^2},
$$
$$
 L:=c^2R(n,u,n,E)=\gamma x(\alpha+\chi)
                  =\boxed{\omega^2a_q\kappa},
$$
$$
 K_E:=c^2R(n,E,n,E)=x^2\alpha+\gamma^2\chi
                  =\boxed{\omega^2(a_q\kappa^2-q^2)}.       \tag{2}
$$
Thus the orbiting reference by itself measures no new radius datum. As a sign check, rotating the orbital plane produces a polar Jacobi displacement proportional to $\sin(\omega\tau)$; its acceleration is $-\omega^2$ times displacement. This agrees with $K_0>0$ in the stipulated acceleration convention.

The forward choice of $E$, the plus label and $x>0$ make $L>0$. Reversing the polar normal changes neither of its two occurrences in any component. Reversing the forward axis instead swaps the labelled boost channels and must not be hidden by an absolute value.

## 3. Three-channel affine invariant and unique inverse

Set $S=\sinh\lambda>0$, $H=\cosh\lambda>0$. The exact boost formula is
$$
 K_\pm=H^2K_0+S^2K_E\pm2HS L,
$$
or equivalently
$$
 K_\pm-K_0
  =\omega^2a_q\left[S^2(1+\kappa^2)\pm2HS\kappa\right].    \tag{3}
$$
Define from the readings
$$
 \Delta=z_+-z_-,\qquad U=z_++z_--2z_0.
$$
The common offset cancels and
$$
 \Delta=4g\omega^2a_q HS\kappa>0,\qquad
 U=2g\omega^2a_q S^2(1+\kappa^2)>0.
$$
Their ratio cancels the common gain:
$$
 \boxed{J:=2\coth\lambda\,\frac{U}{\Delta}
              =\kappa+\kappa^{-1}.}                       \tag{4}
$$
The map $\kappa\mapsto\kappa+\kappa^{-1}$ is strictly increasing for $\kappa>1$. Its other quadratic root lies below one and is not a second physical orbit. Therefore
$$
 \boxed{\kappa=\frac{J+\sqrt{J^2-4}}2,\qquad
 R=\frac{c}{\omega\sqrt{\kappa^2-1}},}
$$
$$
 \boxed{\mu:=\frac{2GM_{\rm MS}}{c^2R}
       =1-\frac{q^2\kappa^2}{\kappa^2-1},\qquad
 M_{\rm MS}=\frac{c^2R}{2G}\mu.}                           \tag{5}
$$
Also recover the instrumental nuisance parameters:
$$
 \boxed{g=\frac{\Delta}{4\omega^2a_q HS\kappa},\qquad
 b=z_0-g\omega^2.}                                        \tag{6}
$$
All of these are conditional on the same offset and positive gain for the three projections; separately unknown gains or offsets would destroy this cancellation.

## 4. Exact feasibility, compactness endpoints and realization

The complete finite test is:

1. Require finite $T>0,\lambda>0$, finite real signed $C,D$ with $C^2+D^2=1$, and $q=\arg(C-iD)/(2\pi)\in(0,1)$.
2. Require finite real $z_0,z_+,z_-$ and $\Delta>0$. Form $J$ from (4).
3. Put
   $$
    \kappa_{\min}=(1-q^2)^{-1/2}>1,\qquad
    J_{\min}=\kappa_{\min}+\kappa_{\min}^{-1}.
   $$
   Require $\boxed{J\ge J_{\min}}$, then use (5)–(6).
   This includes $J=J_{\min}>2$, so the radical and every denominator are valid. No independent constraint on $z_0$ is needed because $b$ is arbitrary.

Necessity follows from the forward law and
$\gamma^2q^2\le1\iff\kappa\ge\kappa_{\min}$.
These conditions yield $g>0$, $R>0$ finite, $0\le\mu<1$, and $B^{-1}=\gamma^2q^2>0$. A zero or negative labelled $\Delta$ rejects the registered three-channel record; it is not repaired by choosing a negative gain. All three equal outputs are likewise impossible in the stated finite domain.

For fixed spin phase $q$, the sharper exact ranges before observing the tide ratio are
$$
 0<R\le\frac{c}{\omega}\frac{\sqrt{1-q^2}}q,\qquad
 \boxed{0\le\mu<1-q^2.}                                  \tag{7}
$$
The included endpoint $J=J_{\min}$ gives $\mu=0$, $B=1$ and the maximum radius. It remains identifiable and is compatible with a nonzero circular speed: no matter equations tie the nonconstant lapse to $B=1$. The upper compactness value $1-q^2$ is a sharp supremum, approached by finite admissible $\kappa\to\infty$, $R\downarrow0$, but never attained at a positive-radius orbit. The general untrapped endpoint $\mu=1$ is excluded as well. Each allowed finite $\kappa$ has an actual local witness, so these endpoints do not follow merely from a formal inequality.

To prove sufficiency, use the recovered $R,\beta=1/\kappa,\gamma,q$, choose any $A_0>0$, and on $R/2<r<3R/2$ set
$$
 A(r)=A_0\exp[\,2\beta^2(r-R)/R\,],\qquad
 B(r)=\frac1{\gamma^2q^2}\ge1.
$$
The path $r=R,\theta=\pi/2$, with
$dt/ds=\gamma/(c\sqrt{A_0})$, $d\phi/ds=\omega/c$,
is future normalized and satisfies the circular geodesic equations. Its first forward return has proper duration $T$; the transported outward spin gives exactly the observed signed phase $q$. Smooth local geodesic initial-value solutions through the same event with $W_\pm=Hu\pm SE$ realize both freely falling probes. They need not be circular. Formula (1) gives (2)–(3), and (6) fits all three raw outputs, not just their ratio. This realizes every record passing the test.

No radial stability assumption, interior matter distribution, field equation or asymptotic exterior is required by this local exact-preparation contract.

## 5. Missing-channel analysis: generic loss and an exception

Keep $T,C,D,\lambda$ and all their standards; only one $z$ is omitted. For any candidate $\kappa\ge\kappa_{\min}$, two unequal curvature values can be fitted to two unequal outputs by a unique affine response with positive gain precisely when their signed ordering agrees. Thus two channels generally retain only ordering information about $\kappa$, rather than (4).

- **Omit $z_-$; retain $z_0,z_+$.** Equation (3) gives $K_+-K_0>0$ for every admissible $\kappa$. The exact feasibility test is $z_+>z_0$; every $\kappa\ge\kappa_{\min}$ can then be fitted by $g=(z_+-z_0)/(K_+-K_0)>0$, $b=z_0-g\omega^2$. There is no radius identification.
- **Omit $z_0$; retain $z_+,z_-$.** The exact test is $z_+>z_-$. Again every admissible $\kappa$ can fit, using $g=(z_+-z_-)/(K_+-K_-)$ and a corresponding $b$.
- **Omit $z_+$; retain $z_0,z_-$.** Define $\kappa_*=\coth(\lambda/2)>1$. Then $K_--K_0$ has the sign of $\kappa-\kappa_*$, and vanishes only at $\kappa_*$ in the physical branch. For $z_-<z_0$, the feasible set is $[\kappa_{\min},\kappa_*)$, nonempty exactly if $\kappa_{\min}<\kappa_*$. For $z_->z_0$, it is $[\kappa_{\min},\infty)\cap(\kappa_*,\infty)$. Unequal outputs fix $g,b$ for each surviving candidate but leave a continuum of radii.

**Equal-reading exception.** If the retained pair has $z_-=z_0$, positivity of $g$ forces $\kappa=\kappa_*$. This identifies $R,M_{\rm MS}$ when
$$
 \kappa_*\ge\kappa_{\min}
 \quad\Longleftrightarrow\quad q\le\operatorname{sech}(\lambda/2);
$$
otherwise the record is infeasible. At equality the mass is zero. In the feasible equal-reading case only $b+g\omega^2=z_0$ is fixed, so the gain and offset are still not individually identified. The reference/plus and plus/minus pairs cannot be equal in the stipulated domain.

Thus three channels are sufficient and needed for global identification over all admissible records; they are not pointwise necessary for every special record. The known signed ordering, gain positivity and exact equality are essential to the exception.

## 6. Complete matched-data worlds for each omission

Here are realized local metrics, not just assignments of independent curvature numbers. Fix any $\omega>0$, the same calibrated $T=2\pi/\omega$, $c,G$, signed spin $(C,D)=(-1,0)$ so $q=1/2$, and commanded $\lambda=\log2$, so $H=5/4,S=3/4$. Choose:

| Quantity | World A | World B |
| --- | --- | --- |
| $\kappa$ | 4 | 5 |
| $\beta$ | $1/4$ | $1/5$ |
| Radius | $R_A=c/(\omega\sqrt{15})$ | $R_B=c/(\omega\sqrt{24})$ |
| Constant $B$ | $15/4$ | $96/25$ |
| Lapse $A(r)$ | $\exp[(r-R_A)/(8R_A)]$ | $\exp[2(r-R_B)/(25R_B)]$ |
| Compactness $\mu$ | $11/15$ | $71/96$ |
| $M_{\rm MS}/[c^3/(2G\omega)]$ | $11/(15\sqrt{15})$ | $71/(96\sqrt{24})$ |
| $K_0/\omega^2$ | 1 | 1 |
| $K_+/\omega^2$ | $883/64$ | 19 |
| $K_-/\omega^2$ | $163/64$ | $79/16$ |

Each metric is used on its own annulus $R_i/2<r<3R_i/2$. The construction in §4 gives the exact circular geodesic, proper first return, spin, and the two boosted freely falling tangents. Their radii and masses differ, while all retained clock, spin, boost and orientation standards coincide. Both mass bounds are strictly satisfied.

Let $g_A=g_0>0,b_A=0$. For each separate reduced observation, choose World B's shared affine response as follows:

| Omitted channel | $g_B/g_0$ | $b_B/(g_0\omega^2)$ | Identical retained outputs, divided by $g_0\omega^2$ |
| --- | ---: | ---: | --- |
| $z_-$ | $91/128$ | $37/128$ | $(z_0,z_+)=(1,883/64)$ |
| $z_+$ | $11/28$ | $17/28$ | $(z_0,z_-)=(1,163/64)$ |
| $z_0$ | $4/5$ | $-449/320$ | $(z_+,z_-)=(883/64,163/64)$ |

Direct substitution of the curvature table into $z=b+gK$ verifies every entry. The gains are positive; the offset is allowed either sign. Each row is a separate exact collision for that omitted-channel experiment, not one affine response matching all three channels. A fixed output convention and every known physical standard are held unchanged; only the unknown gain/offset may differ between candidate worlds, as stipulated. No hidden matter model or external radius input has been changed into an observed quantity.

These witnesses establish failure of global radius and mass identification for every channel omission. The third labelled output breaks these collisions via (4).

## 7. Standards, limits and claim boundary

The dimensional scale comes from the orbiting proper clock $T$, the local speed standard $c$, and the geometric relation inferred from the known boosts. Once $\kappa=1/\beta$ is identified, $R=(cT/2\pi)/\sqrt{\kappa^2-1}$. The commanded rapidity is dimensionless, but its interpretation as $W_\pm=Hu\pm SE$ presumes normalized physical four-velocities and a common local $c$. Static orbital velocity is inferred, not measured separately. The first-return tag and signed spin fix $q$ without a winding ambiguity. $G$ converts spherical geometric compactness and radius to mass. No absolute gradiometer gain, zero, coordinate-time period or separate length baseline enters.

The reference tide $\omega^2$ is a model prediction in calibrated proper-time units. With an arbitrary affine response it alone supplies no radius; the two extra known velocity projections give the shape information cancelling the nuisance parameters. After that shape is fixed, the proper-clock prediction also permits recovery of the unknown gain and offset. Pair-specific response functions, unregistered boost signs, unequal unknown boost magnitudes or uncontrolled clock normalization would change the inference contract.

For a common unknown rescaling $T\mapsto aT$ with $c$ held fixed and the same dimensionless spin/boost/affine-shape record, $R\mapsto aR$, $M_{\rm MS}\mapsto aM_{\rm MS}$, $K\mapsto K/a^2$. Choosing $g\mapsto a^2g$, with $b$ unchanged, preserves the raw outputs. Thus without the calibrated proper-time standard an absolute radius and mass do not follow. The supplied clock and $c,G$, not event counts or uncalibrated tides, supply the dimensional standards.

The exact excluded limit $\lambda=0$ makes all three observers share $u$ and all readings equal, destroying (4). Near that limit the difference and second difference become small. The boundary $q=0$ or $q=1$ is not an admissible finite orbit/spin record in this mass-bounded class. The quadratic inversion approaches its branch-merger $J=2$ only through a limiting regime outside any fixed $q>0$ domain. The limit $\kappa\to\infty$ has $R\to0$ at fixed $T$, not a positive-radius endpoint. Zero mass at finite $\kappa_{\min}$ is regular. These are exact algebraic identification results; no error tolerance, finite-sample precision, apparatus performance or backreaction control is established.

The inferred $M_{\rm MS}(R)=c^2R(1-B^{-1})/(2G)$ is the local mass of a spherical geometry. Associating it with integrated matter energy or an asymptotic central mass needs extra field/interior/exterior assumptions. None are used. A conventional calculation with the same local projections and standards has the same inverse. There is no demonstrated energetic benefit or new physical validation of DET dynamics.

[One-orbit signed gyroscope](spherical_mass_from_one_orbiting_gyroscope.md) · [Central mass from two radial crossing observers](central_mass_from_crossing_observers.md)
