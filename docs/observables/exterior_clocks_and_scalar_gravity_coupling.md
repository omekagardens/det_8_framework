# Testing exterior mass with one blank and three source loads

An empty fixture and three labelled spherical loads give a finite test of the proposed proportional increase in exterior mass. The blank and two loads fix the common clock gain, the fixture compactness $b$, and the compactness slope $a$. The third load must reproduce a definite fourth clock reading. With an independently registered areal-radius ratio $R/\ell$ and an admitted quadratic sector-to-scalar conversion, the inferred gravitational combination is
$$
 \boxed{\displaystyle \kappa\,\frac{G M_0^2}{cJ_s}
   =\frac{a}{2j}\frac{R}{\ell}},\qquad j=\frac{J_s}{M_0c\ell}.
$$
The factor $\kappa$ represents the unknown exterior-mass increase per unit inertial load. Its calibration is a separate requirement.

## Registration and clock convention

Use the compatible three-pair spring and nine-mean scalar record described in [Testing a scalar mass term against three sector inertias](scalar_mass_term_from_three_sector_inertias.md). Retain its labelled inertial mass ratios $1=m_0<m_1<m_2$, spring settings and full independent native histories, supported chain/diamond mixture, common scalar gain, offset and length, and the same visible scalar response channels. The empty fixture is a **fourth** setting of increment zero; sector zero is the positive baseline inertial load $M_0$. Registration must match the complete load, including its attachments and preparation, across the mechanical, scalar and exterior experiments. The scalar result gives $j=\sqrt{(h/k)/2}>0$ only for a compatible quadratic exponent with the positive conversion $k=(M_0c/J_s)^2$ adopted. The clock test itself only needs the independently admitted labelled ratios.

For $t\in\{0,1,m_1,m_2\}$, let the exterior mass be $M_B+\kappa M_0 t$. Define
$$
 X_t=\frac{2GM_{\rm ext}(t)}{Rc^2}=b+at,\qquad
 b=\frac{2GM_B}{Rc^2}\ge0,\qquad a=\frac{2G\kappa M_0}{Rc^2}>0,
 \qquad b+a m_2<1 .
$$
Both clocks lie in a settled spherical vacuum exterior. $R$ and $2R$ are common **areal** radii. In the supplied Schwarzschild line element a static clock advances at a rate proportional to $\sqrt{1-2GM_{\rm ext}/(rc^2)}$. The inner proper rate divided by the outer proper rate is also the frequency ratio received at $2R$ to emitted at $R$ for the same signal. Write $d_t$ for this quotient multiplied by a common positive instrument gain $g$. Squaring gives
$$
 Y_t=d_t^2
 =g^2\,\frac{1-X_t}{1-X_t/2}
 =2g^2\left(1-\frac1{2-b-at}\right).
$$
The lapse normalization cancels; no distant clock epoch enters. A reciprocal frequency or period convention would require conversion before applying the inverse. [Schwarzschild, *On the gravitational field of a mass point*, English translation, v1](https://arxiv.org/abs/physics/9905030v1)

## Exact four-reading decision

Require finite positive $d_t$ and strictly decreasing $Y_0>Y_1>Y_{m_1}>Y_{m_2}>0$. At each positive $t$ form the observed quantity
$$
 Z_t=\frac{t}{Y_0-Y_t}.
$$
The exact clock law gives $Y_0-Y_t=2g^2at/[(2-b)(2-b-at)]$. Consequently $Z_t=u-vt$, where $u=(2-b)^2/(2g^2a)$ and $v=(2-b)/(2g^2)>0$.

1. Use only $t=0,1,m_1$ to set $v=(Z_1-Z_{m_1})/(m_1-1)$, $u=Z_1+v$. Require $v>0$ and $u>0$. The unique candidates are
   $$
   g=\sqrt{(Y_0+1/v)/2},\qquad b=1-vY_0,\qquad
   a=\frac{(2-b)v}{u}.
   $$
   Indeed $Y_0=2g^2-1/v$, $2-b=2g^2v$, and $u/v=(2-b)/a$.
2. Require $b\ge0,\ a>0,\ b+a m_2<1$. This admits a massless blank, excludes a clock on a horizon and keeps every denominator positive.
3. Test the remaining equality **$Z_{m_2}=u-vm_2$**. Equivalently the fourth squared ratio must be $Y_0-m_2/(u-vm_2)$. Require all four positive square roots in the original convention. Failure of any condition rejects the proposed joint clock model for these settings.

These tests suffice on the supplied apparatus premises. The reconstructed gain and compactnesses reproduce the blank exactly; the three differences $Y_0-Y_t=t/(u-vt)$ reproduce each load, including the fourth value. For any positive $G,c,R,M_0$ allowed by the registration, set $M_B=bRc^2/(2G)$ and $\kappa=aRc^2/(2GM_0)$. Each proposed exterior then has the required mass parameter, with the clocks outside its mass radius. This constructs the exterior observations; a stable physical source realizing them is a preparation premise. Because $Y_{m_2}$ can vary with the first three readings fixed, the last equality is a genuine further test.

Agreement establishes compatibility with affine exterior response at these four settings. If that source hypothesis is withdrawn while the gain is unknown, a trial squared gain $S>\max_t Y_t$ gives compactnesses $X_t=2(S-Y_t)/(2S-Y_t)$ reproducing the same data. They are exterior and nonnegative; for $S\ne g^2$ they cannot form another admissible common affine response, by the uniqueness just proved. The readings alone therefore do not certify how fixture energy or binding changes with loading. A nonspherical source class would require a separate exterior law.

## Why two readings and a linearized clock law lose information

Take one feasible spring/scalar preparation with $m_1=2,m_2=3$. It can be the accepted common-spring example $M_i=M_0(1,2,3)_i,\ K=M_0/T^2$, with the quadratic scalar model at any allowed common $h,k,g_{\rm scalar}>0,\ d_{\rm offset}\ge0,\ 0\le\pi\le1$. Keep those preparations and the complete spring/scalar law fixed in both worlds. If only the blank and $t=1$ clock readings are kept, the following gravitational choices agree:

| $b$ | $a$ | $g^2$ | $Y_0$ | $Y_1$ | Largest compactness $b+3a$ |
|---:|---:|---:|---:|---:|---:|
| $0$ | $1/8$ | $1$ | $1$ | $14/15$ | $3/8$ |
| $1/2$ | $3/62$ | $3/2$ | $1$ | $14/15$ | $20/31$ |

The corresponding positive raw clock readings coincide exactly and all four possible configurations are exterior. The table establishes nonidentification on the retained record without altering any load label.

For $X_{\max}=b+a m_2\ll1$, $d_t=g[1-(b+at)/4+O(X_{\max}^2)]$, and $1-d_t/d_0=at/4+O(X_{\max}^2)$. The blank-relative shift thus estimates $a$ to leading order. Treating only the truncated straight line as an exact fit would determine its intercept $g(1-b/4)$ and slope $-ga/4$; those do not split the three parameters. The exact separation uses nonlinear response that can be small in a weak field. No force, timing or clock-gain error tolerance for that separation is supplied.

## Coupling, units and remaining freedom

The clocks determine $\kappa GM_0/(Rc^2)=a/2$ and $M_B/(\kappa M_0)=b/a$. Define the dimensionless gravitational coupling in scalar action units by $\alpha_s=G M_0^2/(cJ_s)$. When the scalar conversion is admitted, the clocks and scalar data alone fix $\kappa\alpha_s\,\ell/R=a/(2j)$. A separate **areal** $R/\ell$ gives the boxed $\kappa\alpha_s$. If using instead the dimensionless squared gravitational length $GJ_s/(c^3\ell^2)=j^2\alpha_s$, the identified product with the same registration is $\kappa GJ_s/(c^3\ell^2)=(aj/2)(R/\ell)$.

Two freedoms explain the qualifications. Without $R/\ell$, keep the geometry and mechanics fixed and send $\ell\mapsto\lambda\ell,\ J_s\mapsto\lambda J_s$ for $\lambda>0$. The scalar apparatus's $k,h,d_{\rm offset},g_{\rm scalar}$ all scale by $\lambda^{-2}$; the full scalar responses and $j$ are preserved. The clock responses are unchanged. Even with $R/\ell$ fixed, keep $G,c,R,\ell,M_B$ and the spring tick fixed, and rescale
$$
 M_i\mapsto\mu M_i,\qquad K\mapsto\mu K,\qquad
 J_s\mapsto\mu J_s,\qquad \kappa\mapsto\kappa/\mu,\qquad \mu>0.
$$
All mechanical readings and native histories, scalar increments and responses, exterior masses and clock readings persist, while $\alpha_s\mapsto\mu\alpha_s$. Independent calibration of $\kappa$ would remove this freedom; choosing $\kappa=1$ reports the coupling in that normalization. Evidence that a physical source actually has unit response requires an independent comparison.

The use of a common exterior radius pair, a reproducible blank, a stable clock gain, settled states, and identical carrier and fixture boundaries must be established by the apparatus. Switching sources can require work and change binding or stored energy. The measurement contains no independent work ledger, signal from the interior, absolute action standard, or test of the field equations themselves. These are conditional inferences from exact symbolic records.
