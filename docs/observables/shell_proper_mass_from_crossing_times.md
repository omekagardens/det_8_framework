# CL066/v1 · Recovering a collapsing shell’s proper mass from two crossings

At fixed exterior mass $M$, the radius tags $8GM/c^2$ and $6GM/c^2$ are shared by a continuous interval of positive shell proper masses. Adding the elapsed time on the shell identifies exactly one mass for every compatible time. Both ends of the compatible time interval are open, including its finite upper end.

## Model and acquisition

Use the classical spherical, neutral, timelike dust shell with a flat interior, a Schwarzschild exterior of mass $M>0$, and radii increasing in both outward normal directions. The shell’s material proper mass is $\mu>0$ and stays constant during the traverse. In Berezin’s notation $m$ is our $M$, and his bare mass $M$ is our $\mu$. Equation (21) gives that bare mass as the integral of the proper surface mass density. Setting charge to zero and both signs positive in (22) gives the signed junction condition below. The author of that paper defines the dot using shell proper time. The two crossings and acquisition rule are supplied by the present control. [V. Berezin, arXiv:gr-qc/9602020v1, pp. 7–8, Eqs. (21)–(23)](https://arxiv.org/pdf/gr-qc/9602020v1)

Write $L=GM/c^2$, $x=R/L$, $s=c\tau/L$, $\eta=\mu/M$, $v=dx/ds$. Thus $v=(dR/d\tau)/c$. The first tag requires finite $v<0$ at $x=8$. Motion stays inward until the first $x=6$ tag. The observer records either the ordered radius tags alone or those tags plus the elapsed proper time on the same shell clock. Its arbitrary additive offset cancels. There is no prescribed release speed before the first crossing.

## Physical branch and reachable masses

Put $A=\sqrt{1+v^2}$ and $B=\sqrt{1+v^2-2/x}$. The physical equation is $A-B=\eta/x$ with $A,B>0$. Since $A^2-B^2=2/x$, this gives $A+B=2/\eta$, hence
$$
 A(x,\eta)=\eta^{-1}+\frac{\eta}{2x},\qquad
 B(x,\eta)=\eta^{-1}-\frac{\eta}{2x}.
$$
In particular, at $x=8$ strict inward speed requires $A>1$ and $B>\sqrt{3}/2$. Therefore
$$
 0<\eta<b,\qquad b=\frac{4}{2+\sqrt3}=8-4\sqrt3.
$$
The value $b$ corresponds to the two roots $1,\sqrt3/2$ at the first tag with zero speed. Strict entry excludes it.

Conversely, $1<b<2$. For $0<\eta\le b$ and $6\le x\le8$, one has $\eta^2<4<2x$, so $B>0$ and $\partial_\eta A=-1/\eta^2+1/(2x)<0$. As $A(8,b)=1$, every $0<\eta<b$ has $A(x,\eta)\ge A(8,\eta)>1$ throughout. The inward rate is uniquely $v=-\sqrt{A^2-1}$. Substitution gives the required second positive root because $A^2-2/x=B^2$ and $B>0$. This recovers the signed equation at every radius.

For each such fixed mass, the speed magnitude has a positive minimum and finite maximum on the closed segment. The function
$$
 s(x)-s(8)=\int_x^8 \frac{dy}{\sqrt{A(y,\eta)^2-1}}
$$
has a strictly decreasing differentiable inverse $x(s)$ with the specified inward rate and finite arrival time. The strict inequalities also hold just outside each tag, allowing transverse crossings. This constructs a history for every mass in the interval. Restricted to the recorded segment it has a single passage through each tag in the stipulated order.

## Compatible elapsed times

Set
$$
 S(\eta)=\int_6^8 \frac{dx}{\sqrt{(\eta^{-1}+\eta/(2x))^2-1}},
 \qquad \Delta\tau=\frac{GM}{c^3}S(\eta).
$$
As $\eta$ increases on the admissible interval, $A$ decreases strictly at every radius and remains greater than one. The integrand and $S$ therefore increase strictly. Continuity follows from joint continuity on the compact radius interval times any closed mass subinterval of $(0,b)$. For $0<\eta<1$, $0<S(\eta)\le 2/\sqrt{\eta^{-2}-1}$, which gives the lower limit zero.

Define $S_*$ by the same integral with $\eta=b$, interpreted at its upper radius as an improper integral. For $6\le x<8$,
$$
 A(x,b)-1=\frac{b(8-x)}{16x},\qquad
 A(x,b)^2-1\ge\frac{b(8-x)}{64}.
$$
The endpoint integrand is positive and bounded above by $8/\sqrt{b(8-x)}$, an integrable function. It bounds each admitted integrand for $x<8$. Dominated convergence gives $S(\eta)\to S_*$ as $\eta\uparrow b$, with $0<S_*<\infty$. At every interior mass the integrand is strictly smaller over $6\le x<8$, so $S_*$ is never attained.

Continuity and strict increase now give a bijection from $0<\mu<Mb$ onto
$$
 0<\Delta\tau<\frac{GM}{c^3}S_*.
$$
For a clock reading inside this interval, the unique solution of $S(\eta)=c^3\Delta\tau/(GM)$ gives $\mu=M\eta$. All readings outside it, including both endpoints, are incompatible with the stated preparation.

## Reduced record and scope

For example, $\mu=M/2$ and $\mu=M$ both lie in the proved mass interval and produce the same ordered tags $(8L,6L)$. The clock distinguishes this pair and every other pair of admissible distinct masses. Radius tags alone give only the compatibility interval. The inverse uses the supplied GR dynamics, fixed orientation, known $M,G,c$, exact areal radii and calibrated shell clock. Its mass and time units come from $M$ and $GM/c^3$. The calculation concerns this ideal observation contract and supplies no empirical acquisition or native DET mass or clock calibration.

## DET recipient scope

The accepted comparison uses one calibrated clock carried by the shell between its two radius crossings. The three-sector spring experiment measures a loaded package's inertial response. Held clocks around a static source measure frequency differences. Applying the shell inverse to either record would require an independent physical correspondence for the masses, trajectory and clock.

Classical accepted CL066/v1 after distinct proof review on 9 November 2026. The coordinator adopted the conventional benchmark after independent recipient review. The frozen proof and reviews have SHA-256 digests `1cf3f4da0e67e3efaa94b73660b75c12d43a40fd23e2691e9e38ea8f0212380c` (author), `7b41874dbb283cea58c3f95ad82ada0a1b1d1ec0d44940091e2d6a01255dc8ed` (proof review) and `ce70500158ec015739a154f8d6d600a6591e763bd21f6b5e557ad3d5a07ed442` (recipient review).
