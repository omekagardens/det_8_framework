# A terminal velocity distinguishes two matched tidal histories

Under either template the unbound pair gives exactly $(L,0,\pi\varepsilon^2L^2\omega)$. In units of $\varepsilon L\omega$, the noisy signed spring-pair reading is within $0.488$ of $\pi$ for template 1 and within $0.488$ of zero for template 2. The prescribed threshold 1 therefore distinguishes the two histories even at the endpoints of the allowed readout error.

## Dynamics and the free record

Write $x=X_2-X_1$ for signed axial separation, initially $L>0$. From $\Phi=-K_n(t)(X^2-Y^2)/2$, the gravitational acceleration is $(K_n X,-K_n Y,0)$. The spatial Laplacian of the potential is $-K_n+K_n=0$ throughout the prescribed patch, including the zero-field exterior times. Equal passive and inertial masses make the axial gravitational acceleration independent of body mass. The two masses have equal and opposite internal spring forces when linked. In either preparation the axial centre of mass $C$ obeys $\ddot C=K_n C$ and stays at its initial resting origin. Transverse positions and velocities remain zero by symmetry and uniqueness. Hence for positive separation the free and linked relative equations are
$$
\ddot x_f=K_n x_f,\qquad
\ddot x_b=K_n x_b-\omega^2(x_b-L).
$$
Indeed the spring's relative acceleration is $-k(1/m_1+1/m_2)(x_b-L)$, with $k=\mu\omega^2$ and $1/\mu=1/m_1+1/m_2$. Positivity for both solutions is checked below. Each pair starts with zero relative speed at the same clock origin, faces the same direction, and experiences the same unknown template without affecting the field or the other pair.

Use $u=\omega t,\ U=2\pi,\ \varepsilon=1/1000$. On the driven interval set $a=1+\varepsilon f_n,\ f_n=(1-\cos(nu))/n$. Thus $a\ge1$ and $q=K_n/\omega^2=a''/a$ is bounded. Primes denote differentiation in $u$. Switching $K_n$ between zero and its interior endpoint limits at $0,T=U/\omega$ gives finite acceleration steps, so integration through either switch leaves positions and velocities continuous. Values of $K_n$ at the individual instants do not affect the evolution. The terminal readout uses this common endpoint limit at $T$, before any subsequent spring evolution.

The exact free trajectory $x_f=L a$ satisfies the equation and both initial data since $a(0)=1,\ a'(0)=0$. It remains positive. Its signed relative velocity is $\dot x_f=\varepsilon L\omega\sin(nu)$, which vanishes at $U$, and $a(U)=1$ for either $n$. The accumulator retains
$$
 I=\varepsilon^2L^2\omega\int_0^{2\pi}\sin^2(nu)\,du
   =\pi\varepsilon^2 L^2\omega,\qquad n=1,2 .
$$
This tag has units of length squared per time. It is an integral of squared relative speed, with no force–displacement or dissipation measurement. Its value has no identification here with deposited heat or gravitational field energy. The two other free tags have units of length and length per time.

## Finite-amplitude bound

Write $z=x_b/L-1$. Its exact initial value problem and causal solution are
$$
 z''+z=q(1+z),\quad z(0)=z'(0)=0,\qquad
 z(u)=\int_0^u\sin(u-s)q(s)(1+z(s))\,ds .
$$
The derivative uses $\cos(u-s)$ in place of $\sin(u-s)$. The continuous solution on the closed driven interval exists uniquely for this bounded linear equation using its one-sided endpoint coefficients.

Uniformly for both templates $0\le f_n\le2,\ |f_n''|=|n\cos(nu)|\le2$, giving $|q|\le2\varepsilon$. With $Z=\max_{[0,U]}|z|$, the integral implies
$$
 Z\le 2\varepsilon U(1+Z),\qquad
 Z\le\frac{2\varepsilon U}{1-2\varepsilon U}
 <\frac{14\varepsilon}{1-14\varepsilon}<15\varepsilon .
$$
Here $U<7$ and $\varepsilon=1/1000$. Consequently $x_b>L(1-15\varepsilon)>0$ throughout. The positive-branch spring equation is self-consistent, with no crossing.

The identity $q(1+\varepsilon f_n)=\varepsilon f_n''$ keeps the multiplicative field term in the error exactly. At any $u\in[0,U]$ subtract the leading velocity integral from the exact velocity integral to get
$$
 R_n(u)=z'(u)-\varepsilon\int_0^u\cos(u-s) f_n''(s)\,ds
       =\int_0^u\cos(u-s)q(s)\,[z(s)-\varepsilon f_n(s)]\,ds .
$$
Thus $|R_n(u)|<7(2\varepsilon)(17\varepsilon)=238\varepsilon^2=0.238\varepsilon$. This numerical constant follows from uniform inequalities at the specified amplitude. The signed leading integral at $U$, divided by $\varepsilon$, is $\int_0^{2\pi}\cos(s)n\cos(ns)\,ds$. For $n=1$ the integral of $\cos^2 s$ is $+\pi$. For $n=2$ the integrand is $\cos s+\cos 3s$, whose integral vanishes.

## Readout and its interpretation

Converting back to dimensional velocity gives $v_b=L\omega z'(U)$. Normalize the terminal reading $Y=v_b+\eta$ by the positive velocity scale $S=\varepsilon L\omega$. The final column uses the given deterministic bound $|\eta|/S\le1/4$, including both endpoint errors. Closed enclosures suffice.

| Template | True $v_b/S$ | Measured $Y/S$ |
| --- | --- | --- |
| $n=1$ | $[\pi-0.238,\ \pi+0.238]$ | $[\pi-0.488,\ \pi+0.488]$ |
| $n=2$ | $[-0.238,\ 0.238]$ | $[-0.488,\ 0.488]$ |

The high case exceeds the prescribed threshold $S$ by at least $(\pi-1.488)S>0$. The low case lies below it by at least $0.512S>0$. These enclosures concern terminal velocity, with units of length per time, and $K_n$ has inverse-time-squared units. No tie can occur. For free data alone the two templates give the same entire ordered record, although their interior speed histories differ. The accumulator discards when each contribution arrived. The spring retains a phase-sensitive response to the same drive. Over this period the first template projects onto the oscillator's velocity kernel and the leading projection of the second cancels. The finite-amplitude bound covers the exact remainder in both cases.

## Transfer to gravity measurements

The test requires a calibrated time-dependent tidal field, matched relative rest at the same separation, a known spring frequency, a common clock and a signed velocity measurement. The two-site mass study supplies static tidal readings in a specified metric. The constituent free-fall study compares field-on and field-off motion in a uniform field. A physical implementation of this two-template test needs its own calibration of the field, spring and readout. The templates and their leading-order distinction were specified during design. [Two-site tides and radar mass](two_site_tides_and_radar_mass.md) · [Constituent free fall](constituent_free_fall_from_casing_motion.md)
