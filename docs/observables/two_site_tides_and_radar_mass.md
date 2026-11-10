# Can two local tides and a radar echo determine central mass?

In a Schwarzschild–de Sitter static region, tidal readings at two registered sites determine the ratio of their areal radii. The rate ratio of stationary clocks normally fixes both radii and the central mass. When the clocks run at the same rate, a continuous range of masses can survive. In the family below, two different masses give identical tides, clock rates relative to each other, and round-trip light times measured by the inner clock. A calibrated measurement of radial proper length along a static spatial slice distinguishes them.

## The inverse from two tidal pairs and a clock-rate ratio

Assume one metric with known $G,c>0$, unknown $M>0$ and $\Lambda\geq0$, and two stationary sites at unknown radii $0<r_1<r_2$. Write $f(r)=1-2GM/(c^2r)-\Lambda r^2/3$. The static metric is

$$
ds^2=-f(r)c^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2.
$$

Each radial and tangential tide $(R_i,H_i)$ is relative acceleration per unit infinitesimal separation, in the proper frame of freely falling probes released momentarily at rest with respect to site $i$. The endpoint clock-rate ratio for equal static coordinate-time intervals is $Z=d\tau_2/d\tau_1=\sqrt{f(r_2)/f(r_1)}$. Its orientation and the inner/outer labels are part of the record. The single-site tidal equations and their calibration conditions are established in [Local mass inference from tides and signed support](local_mass_from_tides_and_support.md).

For finite readings put $\sigma_i=(R_i-H_i)/3$ and $\lambda_i=(R_i+2H_i)/3$. Require $\sigma_1>\sigma_2>0$, $\lambda_1=\lambda_2=\lambda\geq0$ and $Z>0$. Here $\sigma_i=GM/r_i^3$ and $\lambda=\Lambda c^2/3$ have units of inverse proper time squared. The radius ratio $q=(\sigma_1/\sigma_2)^{1/3}>1$ follows from the data. Taking $\ell=r_1$, the entire family consistent with the tides is

$$
r_2=q\ell,\qquad M=\frac{\sigma_1\ell^3}{G},\qquad
\Lambda=\frac{3\lambda}{c^2},\qquad
0<\ell^2<\frac{1}{\max(a,b)},
$$

where $a=(2\sigma_1+\lambda)/c^2$ and $b=q^2(2\sigma_2+\lambda)/c^2$. The endpoint lapse functions are $f_1=1-a\ell^2$ and $f_2=1-b\ell^2$. Positive endpoints suffice for a static path between them because $f''(r)=-4GM/(c^2r^3)-2\Lambda/3<0$ within each fixed metric.

Write $z=Z^2$. The clock equation is $z=(1-b\ell^2)/(1-a\ell^2)$.

- When $a\ne b$, require $b-za\ne0$ and take $\ell^2=(1-z)/(b-za)$. It gives the unique solution precisely when it lies in the open interval above. Substitution recovers both endpoint lapses and the positive measured $Z$. The clock ranges are $Z>1$ for $a>b$ and $0<Z<1$ for $b>a$. Each finite value in the applicable range occurs.
- When $a=b$, the clock reading is compatible exactly at $Z=1$, and every radius in the tidal interval survives. For $q>1$ the equal-lapse condition is $\lambda=2\sigma_1/[q(q+1)]$.

Rescaling both radii by $s>0$ and $M$ by $s^3$ at fixed $\Lambda$ preserves the timed tides. The clock ratio is invariant under that rescaling on the equal-lapse branch for every allowed scale. This compares physically different masses and locations at fixed calibrated clock units. The usual metric rescaling $r\mapsto sr$, $M\mapsto sM$, $\Lambda\mapsto\Lambda/s^2$ would scale the tidal readings by $1/s^2$ at fixed physical time units. The upper boundary of the family is excluded because at least one stationary worldline would cease to be timelike.

## One round trip with equal endpoint clock rates

Fix $q=2$, $\sigma=\sigma_1>0$, and $\lambda=\sigma/3$. Define the dimensionless scale $t=\sigma\ell^2/c^2$ and radial coordinate $x=r/\ell$, with $1\leq x\leq2$. Then

$$
V(x)=\frac{2}{x}+\frac{x^2}{3},\qquad f_t(x)=1-tV(x),
\qquad \delta=f_t(1)=f_t(2)=1-\frac{7t}{3}.
$$

The strictly convex $V$ takes its maximum $7/3$ at both endpoints. The allowed scales are $0<t<3/7$ and the mass is $M(t)=c^3t^{3/2}/(G\sqrt{\sigma})$. All these scales have the same baseline record,

$$
(R_1,H_1,R_2,H_2,Z)
=\left(\frac{7\sigma}{3},-\frac{2\sigma}{3},
        \frac{7\sigma}{12},\frac{5\sigma}{24},1\right).
$$

Both tangential tides here are nonzero. Equal endpoint clock rates are a different condition from zero support at a single balance point.

Let a radial null pulse leave the stationary inner site, reflect instantaneously at the outer site, and return to the inner clock. The null condition gives $|dt_{\rm coord}|=dr/(cf(r))$. The inner clock converts that entire outward-and-return coordinate interval to its own proper time. Thus

$$
I(t)=\int_1^2\frac{dx}{1-tV(x)},\qquad
\tau_{\rm echo}(t)=\frac{2\ell}{c}\sqrt{\delta}\,I(t),\qquad
E(t)=\frac{\sqrt{\sigma}}2\tau_{\rm echo}(t)=\sqrt{t\delta}\,I(t).
$$

At every interior scale $E$ is finite, continuous and positive. At the lower boundary $I(t)\to1$ and $E(t)\to0$. To check the upper boundary, factor the limiting lapse,

$$
F(x)=f_{3/7}(x)=\frac{(x-1)(2-x)(x+3)}{7x},
\qquad f_t(x)=\delta+(1-\delta)F(x).
$$

For $u=\min(x-1,2-x)$, $F(x)\geq(5/14)(x-1)(2-x)\geq5u/28$. When $0<\delta\leq1/2$ this gives

$$
I(t)\leq 2\int_0^{1/2}\frac{du}{\delta+5u/56}
=\frac{112}{5}\log\left(1+\frac{5}{112\delta}\right).
$$

Consequently $E(t)\to0$ also at the upper boundary. The inner clock's factor $\sqrt{\delta}$ suppresses the logarithmic growth of the coordinate travel time.

At $t_0=3/14$ one has $\delta=1/2$ and $I(t_0)>1$, so $E(t_0)>\sqrt{3/28}>1/4$. By continuity there are two interior scales $t_-<t_0<t_+$ with $E(t_-)=E(t_+)=1/4$. They give the **same strictly positive echo** $\tau_{\rm echo}=1/(2\sqrt{\sigma})$ and the same five baseline readings. Their masses differ because $M(t)$ is strictly increasing. Both are regular static worlds. The limiting configurations at zero mass and at the static boundary were used only to prove existence. The argument establishes at least two solutions for this record.

For any finite reported echo $\tau$, the exact compatible masses in this family are
$$
\left\{\,M(t):0<t<3/7,\quad E(t)=\sqrt{\sigma}\,\tau/2\,\right\}.
$$
The continuous extension of $E$ vanishes at both boundaries and is positive inside, so it attains a finite positive maximum $E_{\max}$ at an interior scale. Its achievable proper-echo range is exactly $0<\tau\leq2E_{\max}/\sqrt{\sigma}$, including the upper endpoint. Nonfinite reports also fail this ideal model. This characterization requires no count of all the extrema or roots.

## What a separately measured proper length would add

A calibrated radial proper separation on a static spatial slice would instead be

$$
L_{\rm prop}(t)=\frac{c}{\sqrt{\sigma}}
\int_1^2\frac{\sqrt{t}}{\sqrt{1-tV(x)}}\,dx.
$$

The derivative of the integrand with respect to $t$ is $1/[2\sqrt{t}(1-tV(x))^{3/2}]>0$. This length increases continuously from zero to the finite, excluded upper limit

$$
L_*=\frac{c}{\sqrt{\sigma}}\sqrt{\frac37}\int_1^2\frac{dx}{\sqrt{F(x)}} .
$$

The limiting integrand has only integrable inverse-square-root singularities at the endpoints. Each measured $0<L_{\rm prop}<L_*$ therefore selects exactly one scale and one mass. If both length and echo are measured, that scale must also reproduce the echo. The two worlds above have the same radar range $c\tau_{\rm echo}/2$ and different proper lengths.

## Measurement and calibration scope

The complete ideal record retains the site and setting labels, deterministic readings and success on every trial; any fixed setting weights are common to both worlds. All readings refer to the same two sites, mass and cosmological constant within each world. The comparison assumes calibrated clocks and tidal response, registered axes and sources, stationary supports, radial null propagation, instantaneous reflection and negligible or bounded backreaction. Measuring proper length requires its own static-slice length calibration. A physical protocol would also need to account for signal losses, readout errors, preparation, support work and reset costs.

These results concern central mass in a supplied static metric. The DET birth law supplies no conversion to physical proper time, calibrated reflector, mass per birth or empirical source measurement. The earlier CL026 comparison used different prescribed static lapse profiles. Relational State Research derived this two-site inverse and echo counterexample. DET Energy Research independently reviewed the result.
