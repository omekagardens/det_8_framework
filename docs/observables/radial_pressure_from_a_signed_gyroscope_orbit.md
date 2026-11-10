# Radial pressure and the density allowed by one signed gyroscope orbit

Measure the areal radius $R$, the orbiting clock’s proper period $T$ to its first forward meridian return, and the outward and forward components $(C,D)$ of the initially outward, parallel-transported unit spin. Define
$$
x=\frac{2\pi R}{cT},\qquad \gamma=\sqrt{1+x^2},\qquad
q=\frac{\arg(C-iD)}{2\pi}\ \text{on }[0,1),\qquad
K_R=\frac{c^4}{8\pi G R^2}.
$$
For a compatible signed gyroscope record, Einstein gravity with zero cosmological constant fixes the local radial pressure in the static orthonormal frame:
$$
\boxed{P:=p_r(R)=K_R\big[(1+3x^2)q^2-1\big]}.
$$
With the dominant energy condition (DEC) on an open annulus and nonnegative Misner–Sharp mass required only at $R$, the **entire feasible set** of local proper energy densities is $\boxed{\epsilon(R)\in[|P|,\infty)}$. Each finite value is attained with exactly the same signed orbit. Positive $P$ means radial pressure and negative $P$ means radial tension. The dividing spin phase is $q=1/\sqrt{1+3x^2}$.

## Which field-equation data the orbit supplies

In static areal coordinates use
$$
ds^2=-e^{2\Phi(r)}c^2dt^2+\frac{dr^2}{F(r)}+r^2d\Omega^2,
\quad F(r)=1-\frac{2m(r)}r,\quad m(r)=\frac{G M_{\rm MS}(r)}{c^2}.
$$
Here $m$ is a length. The gyroscope measurement admits finite $R,T>0$, real unit spin components $C^2+D^2=1$, and $0<q\le1/\gamma$. On that arc, circular free fall and the signed spin measurement give
$$
R\Phi'(R)=\beta^2=\frac{x^2}{1+x^2},\qquad
F_R:=F(R)=\gamma^2 q^2,\qquad m_R=\frac R2(1-F_R).
$$
Only the value and the indicated lapse derivative at the orbit matter. The normalization of the static time coordinate is free. The measurement requires an exactly prepared circular geodesic; robustness to radial perturbations was not measured. An inadmissible orbit record has no solution under the added premises.

For a static diagonal stress tensor with orthonormal energy density $\epsilon$, radial pressure $p_r$ and equal tangential pressures $p_t$, set $\kappa=8\pi G/c^4$. The temporal and radial Einstein equations in this convention are
$$
\kappa\epsilon=\frac{1-F}{r^2}-\frac{F'}r=\frac{2m'}{r^2},\qquad
\kappa p_r=F\left(\frac{2\Phi'}r+\frac1{r^2}\right)-\frac1{r^2}.
$$
The angular equation is equivalently imposed, once these two hold, by stationary conservation,
$$
p_t=p_r+\frac r2\big[p_r'+(\epsilon+p_r)\Phi'\big].
$$
Indeed the radial divergence of a diagonal spherical tensor is $p_r'+(\epsilon+p_r)\Phi'+2(p_r-p_t)/r$. The contracted Bianchi identity gives this same relation for the Einstein tensor, fixing its angular components when its temporal and radial components match. The equations use proper energy per volume, with pressure and energy density both in $\mathrm{J/m^3}=\mathrm{Pa}$. [Herrera, Ospino and Di Prisco, v3, §2, Eqs. (1)–(4)](https://arxiv.org/pdf/0712.0713v3)

Substitution in the radial equation gives $P/K_R=F_R(1+2\beta^2)-1=(1+3x^2)q^2-1$. Neither $F'_R$ nor $m'(R)$ was measured. For example, finding $\epsilon(R)$ separately through the mass profile would require $dM_{\rm MS}/dr$ at $R$, since $M'_{\rm MS}=4\pi r^2\epsilon/c^2$. A single mass value gives no such derivative.

## Sharpness on an open annulus

DEC requires $\epsilon\ge|p_r|,|p_t|$ throughout the annulus, so $\epsilon(R)\ge|P|$ is necessary. To realize any finite $E\ge|P|$, choose the following smooth profiles near $R>0$:
$$
\epsilon(r)=E(R/r)^2,\qquad p_r(r)=P(R/r)^2,\qquad
m(r)=m_R+\frac{\kappa}{2}ER^2(r-R).
$$
The mass derivative satisfies the temporal equation. Fix any finite $\Phi(R)$ and integrate
$$
\Phi'(r)=\frac{m(r)+\tfrac{\kappa}{2}r^3p_r(r)}
                    {r^2[1-2m(r)/r]} .
$$
This enforces the radial equation. Since $F_R>0$ and $R\Phi'(R)=\beta^2\in(0,1)$ by the orbit’s pressure formula, a two-sided open neighborhood exists with $F>0$ and $0<r\Phi'(r)<1$. The integral defines a smooth positive lapse there. Finally $p_r'=-2p_r/r$, so the angular equation reduces to
$$
p_t(r)=\tfrac12\,r\Phi'(r)\,[\epsilon(r)+p_r(r)].
$$
The chosen profiles obey $\epsilon\ge|p_r|$ everywhere. Thus $0\le\epsilon+p_r\le2\epsilon$, which gives $0\le p_t\le\epsilon$ throughout this neighborhood. This proof covers both signs of radial saturation $E=|P|$, with $p_t=0$ when $P=-E$; it also covers $E=P=0$ with vacuum on the annulus. Every constructed metric has the same $F_R$, the same $\Phi'(R)$, and can share the same $\Phi(R)$. Spin transport then reproduces the same proper period and both spin components. No regular centre, equation of state, exterior matching or matter stability is used.

## What the forward component distinguishes

With only $C$ retained, take the distinct candidates $\{\arccos(C)/(2\pi),\,1-\arccos(C)/(2\pi)\}$ that lie in the admissible arc. Apply the boxed pressure and density formulas to each survivor. In the supplied example $x=3/4,\ C=-1/2$, the factor $1+3x^2$ is $43/16$, and both candidates survive:

| Forward component $D$ | Phase $q$ | $p_r(R)/K_R$ | Local interpretation |
|---|---:|---:|---|
| $-\sqrt3/2$ | $1/3$ | $-101/144$ | Radial tension |
| $+\sqrt3/2$ | $2/3$ | $7/36$ | Positive radial pressure |

Both branches satisfy local Einstein gravity and DEC by the construction above. They can even share the same density $E=K_R$. Thus discarding the forward sign loses the pressure sign on this reduced record.

## Zero mass at the observed sphere

At the allowed endpoint $q=1/\gamma$, one has $m_R=0,\ F_R=1$, and $P=2K_R\beta^2>0$. DEC forces $\epsilon(R)>0$ and hence $m'(R)>0$. Smoothness then gives negative $m(r)$ just inside $R$. This is consistent with the original pointwise premise $m_R\ge0$; the open-annulus family above realizes the endpoint and its exact density bound.

If $m(r)\ge0$ is additionally required throughout a **two-sided neighborhood**, a zero at $R$ is an interior minimum, so $m'(R)=0$. The temporal equation now forces $\epsilon(R)=0$, and DEC forces $P=0$, contradicting the nonzero orbital speed. Thus adding neighborhood nonnegativity to Einstein gravity and local DEC eliminates the zero-mass record entirely. For $m_R>0$, continuity preserves positive mass on a sufficiently narrow annulus, so the feasible density sets there are unchanged. As a purely geometric condition, neighborhood nonnegativity would still permit $F\equiv1$ and $R\Phi'(R)=\beta^2$; its exclusion of this endpoint relies on the added matter equations and energy condition.

The orbit supplies a local geometric mass, a speed and a signed phase using the calibrated areal radius, proper clock and physical $G,c$. The pressure scale $K_R$ changes as $R^{-2}$ under a common dilation of $R,T$ that preserves the dimensionless record. The conditional pressure inference supplies neither a global stellar model nor an integrated proper matter energy, which needs the interior density and proper-volume element.

[Geometric mass from the signed gyroscope orbit](spherical_mass_from_one_orbiting_gyroscope.md) · [Interior proper matter energy](static_radial_length_and_proper_matter_energy.md)
