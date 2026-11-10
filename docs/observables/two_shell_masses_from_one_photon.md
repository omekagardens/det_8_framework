# Two shell masses from one centre-traversing light ray

For every fixed exit-to-entry areal-radius ratio $0<\xi<1$, a sufficiently small exterior redshift uniquely selects both shell masses in entry-radius units on the strictly collapsing, weak-self-gravity branch specified below. The data are $\xi$ and one outgoing-to-incoming **exterior** photon-energy ratio $\mathcal W$. The second constraint comes from the time required for that photon to reach the regular centre and exit the moving shell. Both individual cross-interface energy ratios can remain unobserved.

## Shell dynamics and interior flight

Let $R_1$ be the entry radius and $R_2=\xi R_1$ the exit radius. For the conserved positive material proper mass $\mu$ and exterior Schwarzschild mass $M$, put
$$
 x=r/R_1,\qquad e=\frac{G\mu}{2c^2R_1},\qquad E=M/\mu,\qquad
 u=\frac{dr}{c\,d\tau},\qquad f(x)=1-\frac{4eE}{x}.
$$
Here $\tau$ is shell proper time and $E$ is a mass ratio. Write $A=\sqrt{1+u^2}$, $B=\sqrt{f+u^2}$. On the ordinary-normal neutral dust branch the signed junction gives $A-B=2e/x$. Since $A^2-B^2=4eE/x$, for positive $e$
$$
 A(x)=E+e/x,\quad B(x)=E-e/x,\quad w(x)=\sqrt{A(x)^2-1},\quad u(x)=-w(x).
 \tag{1}
$$
This uses the inward root on the whole traverse. The equality of the conserved masses at entry and exit is essential. The local proof below checks $A>1,\ B>0,\ f>0$ on the interval. [Berezin, Eqs. (21)–(23), neutral ordinary sides](https://arxiv.org/pdf/gr-qc/9602020v1)

Let $T$ be inertial time in the flat interior. Along the shell, $dT/d\tau=A$, so the magnitude of its inward speed in this frame is $c\,w/A<c$. The same interval of interior time can be computed along two paths:
$$
 \frac{c(T_2-T_1)}{R_1}
  =\int_\xi^1\frac{A(x)}{w(x)}\,dx
  =1+\xi .
 \tag{2}
$$
The integral follows from (1). The photon travels $R_1$ to the centre and then $\xi R_1$ outward on the opposite side. The centre is regular in flat space and the radial photon crosses it with unchanged interior Killing energy. There is no reflecting surface, centre delay or shell-clock reading in (2).

## The single exterior frequency ratio

Use $P(x)$ for the outward and $Q(x)$ for the inward exterior-over-interior Killing-energy factors of CL092. Matching the photon frequency in the transparent shell frame gives $P=(B+u)/(A+u)$ and $Q=(B-u)/(A-u)$. Since $(A+w)(A-w)=1$, equation (1) gives
$$
 P(x)=1-\frac{2e}{x}(A+w),\qquad
 Q(x)=1-\frac{2e}{x}(A-w).
$$
At entry the ray travels exterior to interior, multiplying its energy by $1/Q(1)$; at exit it travels interior to exterior, multiplying by $P(\xi)$. Thus
$$
 \boxed{\quad \mathcal W=\frac{\mathcal E_{\rm out}^{\rm ext}}{\mathcal E_{\rm in}^{\rm ext}}
      =\frac{P(\xi)}{Q(1)} .\quad}
 \tag{3}
$$
The intermediate energy cancels. Each local factor uses the state at its own event; multiplying two factors evaluated at one event would instead give its exterior lapse squared. The accepted transfer law uses the local null-coordinate derivatives for transmission. [Harada, Cardoso and Miyata, §III, Eq. (3.5) and Appendix A](https://arxiv.org/pdf/1811.05179v3)

## Limiting speed and rank of the inverse

Define $F(E,e;\xi)=\int_\xi^1 A/w\,dx-(1+\xi)$. The algebraic continuation to $e=0$ is regular near $E>1$. In that limit (2) gives
$$
 \frac{w_0}{E_0}=\frac{1-\xi}{1+\xi},\qquad
 E_0=\frac{1+\xi}{2\sqrt{\xi}},\qquad
 w_0=\frac{1-\xi}{2\sqrt{\xi}} .
$$
The first ratio is the limiting magnitude of the interior-frame speed in units of $c$; the proper-time radius rate is $-c w_0$. The reference point is a limit of the dimensionless equations, with no positive shell mass asserted at $e=0$.

Since $d[A/\sqrt{A^2-1}]/dA=-1/w^3$, at that point
$$
 F_E=-\frac{1-\xi}{w_0^3}\ne0,\qquad F_e=-\frac{\log(1/\xi)}{w_0^3}.
$$
For fixed interior $\xi$, the compact integration interval keeps $w$ uniformly positive near $(E_0,0)$. The implicit function theorem therefore gives a unique smooth timing solution $E=E(e;\xi)$ locally, with $E'(0)=-\log(1/\xi)/(1-\xi)$.

At $e=0$ both transfer factors are one for every nearby $E$. Their $E$-derivatives vanish there, so the variation of $E$ required by (2) contributes nothing at first order to (3). Using $E_0+w_0=\xi^{-1/2}$ and $E_0-w_0=\sqrt{\xi}$ gives
$$
 \left.\frac{d\mathcal W}{de}\right|_{F=0,e=0}
   =-\frac{2}{\xi}(E_0+w_0)+2(E_0-w_0)
   =-\frac{2(1-\xi^2)}{\xi^{3/2}}<0.
 \tag{4}
$$
Equations (2) and (3) thus have independent parameter derivatives at the limiting point. Smoothness also permits small changes of the measured $\xi$ around any chosen interior value. For each fixed such $\xi$ there is an $\varepsilon_\xi>0$ on which the exact frequency ratio is strictly decreasing for $0<e<\varepsilon_\xi$. Its image is an open interval immediately below 1. Each ratio in that interval selects one **positive** $e$ and one $E$ on this branch. The exact inverse solves the two displayed equations. Its leading behavior,
$$
 e=\frac{\xi^{3/2}}{2(1-\xi^2)}(1-\mathcal W)+O_\xi((1-\mathcal W)^2),
$$
fixes the sign and sensitivity. Local uniqueness follows from (4) and continuity independently of truncating this expansion. The neighborhood may shrink as $\xi$ approaches either endpoint.

## Realization, units and scope

At the limiting solution $A=E_0>1,\ B=E_0>0,\ f=1$. These strict margins persist uniformly for $x\in[\xi,1]$ and sufficiently small positive $e$. For any such solution choose $R_1>0$ and integrate $dr/d\tau=-c w(r/R_1)$ from $R_1$ to $\xi R_1$. Its speed is finite and nonzero; both sides of the signed junction have the required orientations throughout. The incoming light overtakes the subluminal shell at entry and stays inside until the centre. On the outward leg the photon radius increases while the shell radius decreases. They intersect exactly once, and (2) puts that intersection at $\xi R_1>0$ outside the Schwarzschild radius. Spherical symmetry permits the exit on the opposite side. This constructs physical-branch trajectories of the supplied model for the whole one-sided local data interval.

The dimensionless masses and the optional dimensional conversion are
$$
 \frac{G\mu}{R_1c^2}=2e,\qquad \frac{GM}{R_1c^2}=2eE,\qquad
 \mu=\frac{2eR_1c^2}{G},\qquad M=E\mu .
$$
Without an absolute radius, the rescaling $(R_1,R_2,\mu,M)\mapsto\alpha(R_1,R_2,\mu,M)$ leaves the two measurements invariant for every $\alpha>0$. With a calibrated entry or exit radius, $G$ and $c$, both masses follow in physical units.

This experiment needs a registered pair of areal-radius tags and one conserved test photon with no recoil, absorption or frequency-changing centre interaction. The exterior Killing normalization and gain must agree for both energy measurements; raw local frequencies from different observers require their redshift and motion corrections. It uses a fixed vacuum exterior of conserved mass and the signed, pressureless shell dynamics. CL066 supplies a known exterior mass and a comoving traverse time in its own protocol. The optical-volume protocol registers event-count means between wavefronts. Neither supplies the same centre-traversing photon, its paired radius tags and its exterior frequency ratio. The theorem proves an exact local inverse under a branch prior. It establishes neither a global inverse nor an empirical shell, physical apparatus or native DET frequency or mass standard.

[Two rays at one shell event](dust_shell_masses_from_opposite_rays.md) · [Known-mass shell traverse](shell_proper_mass_from_crossing_times.md) · [Split optical volume](radially_split_reflected_light_counts.md)
