# What a gravitational field step and a clock reveal about a shell encounter

For the specified unequal masses, a compatible field step identifies which shell left the detector sphere. The elapsed time then fixes the radial kinetic energy transferred into the internal register, including zero at perfect restitution. An elapsed time shared by the two updates gives different losses. A field step of one mass unit by itself permits the entire range of contact losses.

## Encounter and energy balance

Write $V=\sqrt{Gm/R}$ and take radial velocities positive outward. In transparent passage $T$, A keeps $+V$ and becomes outer, and B keeps $-2V$ and becomes inner. For contact $C_e$, each solid-angle element contains masses $2m\,d\Omega/(4\pi)$ and $m\,d\Omega/(4\pi)$. Its two radial impulses sum to zero. Thus $2v_A^++v_B^+=0$, while restitution gives $v_B^+-v_A^+=3eV$. It follows that
$$
v_A^+=-eV,\qquad v_B^+=2eV,\qquad 1/2\le e\le1.
$$
B becomes outer. The impulses per unit solid angle are $-2m(1+e)V/(4\pi)$ on A and its positive opposite on B, along the local outward axis. Integrating the radial unit vector over the sphere gives zero. Each complete spherical shell has zero vector momentum even as its scalar radial velocity changes. The per-angle balance is supplied by the local impact rule.

The potential of shell $i$ at radius $r>0$ is $-Gm_i/\max(r,r_i)$, continuous at its surface and through a crossing. The position-dependent gravitational energy with zero at infinite dispersal is
$$
U=-G\left[
 M_0\left(\frac{m_A}{r_A}+\frac{m_B}{r_B}\right)
 +\frac{m_A^2}{2r_A}+\frac{m_B^2}{2r_B}
 +\frac{m_A m_B}{\max(r_A,r_B)}
\right].
$$
The pair contributes once. The self-energy terms follow from assembling each spherical layer. The central point contributes through its interaction with the shells. Both encounter limits give $U=-(15/2)mV^2$. On each separated arc $-\partial U/\partial r_i=m_i\ddot r_i$ and the radial kinetic energy $K$ plus $U$ is constant. Finite gravity at $R$ supplies zero instantaneous impulse.

At the encounter $K^-=3mV^2$, $K_T^+=3mV^2$, and $K_C^+=3e^2mV^2$. With no external work the mechanical loss and internal gain are
$$
L=-\Delta(K+U)=\Delta E_{\rm int}
=\begin{cases}0 & T,\\3(1-e^2)mV^2 & C_e.\end{cases}
$$
The ledger specifies an energy increment. Its microscopic form and the initial internal energy are free.

## Flight to the first gate

Use $x=r/R$, $\tau=tV/R$, $D=d/R=33/32$. A prime denotes differentiation with respect to $\tau$. The departing outer shell has $x(0)=1,\ x'(0)=s>0,\ x''=-q/x^2$. Here $q$ counts the central mass, the inner shell and half the outer shell, in units of $m$. The dimensionless data on the ordered arcs are

| Update | Outer, $s,q$ | Inner, $x'(0),q_{\rm in}$ |
| --- | --- | --- |
| $T$ | A, $1,3$ | B, $-2,3/2$ |
| $C_e$ | B, $2e,7/2$ | A, $-e,2$ |
| Equal masses, $T$ or $C_1$ | A or B respectively, $1,5/2$ | B or A respectively, $-2,3/2$ |

Integration along the outgoing arc gives $x'^2=s^2-2q(1-1/x)$, so its dimensionless gate time is
$$
F(s,q)=\int_1^D \frac{dx}{\sqrt{s^2-2q(1-1/x)}} .
$$
For all rows, $s\ge1,\ 2q\le7$, and $0\le1-1/x\le1/33$ up to the gate. The squared speed is at least $26/33$. Thus the outgoing solution reaches $D$ while strictly increasing by time $\sqrt{33/26}/32<1/16$. For the inner solution, as long as $x_{\rm in}\ge1/2$, $x_{\rm in}''\ge-8$ and $x_{\rm in}'(0)\ge-2$. Before time $1/16$ this gives
$$
x_{\rm in}(\tau)\ge1-2\tau-4\tau^2\ge55/64>1/2.
$$
A first descent to $1/2$ during this interval would violate the bound. The inner shell has strictly negative speed and acceleration throughout. The two independently constructed positive-radius arcs therefore have the asserted strict order at every positive time through the gate, without a turn or intervening encounter. The equations are smooth for these arcs, and the strictly separated outgoing velocities fix their order at launch.

## Inverse for the two unequal masses

Let $j=Jd^2/(Gm)$, $\tau_g=t_g V/R$, $\tau_T=F(1,3)$, and $H(e)=F(2e,7/2)$. Immediately before the crossing the detector encloses $4m$. Immediately after it encloses $2m$ in $T$ and $3m$ in $C_e$. The shell theorem with the one-sided readings gives $j=2$ and $j=1$, respectively. The additive readout offset cancels.

| Exact joint record | Compatible update | Set of losses $L/(mV^2)$ |
| --- | --- | --- |
| $j=2,\ \tau_g=\tau_T$ | $T$ | $\{0\}$ |
| $j=1,\ H(1)\le\tau_g\le H(1/2)$ | $C_e$ with $e=H^{-1}(\tau_g)$ | $\{3(1-e^2)\}$ |
| Every other pair | None | $\varnothing$ |

As $e$ increases, the integrand in $H(e)$ strictly decreases at every radius. Its denominator is uniformly bounded away from zero throughout the closed interval. Continuity and strict decrease give existence on the whole stated time interval and uniqueness there. Taking either endpoint in the contact row is allowed. At $\tau_g=H(1)$ the loss is zero, and at $\tau_g=H(1/2)$ it is $9mV^2/4$. Each selected update realizes its record by the outgoing solutions above. A negative or zero time, an unlisted jump, or a mismatched time and allowed jump has no realization.

## Loss of information under the controls

**Time alone.** At $e=1/2$ the contact outer shell launches at the transparent speed with stronger deceleration, so $H(1/2)>\tau_T$. At $e=1$ the squared outgoing speed for contact exceeds that for transparent passage by $3-(1-1/x)>0$ through the gate, so $H(1)<\tau_T$. Hence $e_*=H^{-1}(\tau_T)$ lies strictly between the endpoints. At this common time the compatible losses are $0$ for $T$ and $3(1-e_*^2)mV^2>0$ for contact. At every other time in the closed contact interval only the contact solution in the table survives. All times outside that interval are impossible.

**Jump alone.** A step $j=2$ identifies transparent passage and zero loss. A step $j=1$ identifies contact and permits every $L$ in $[0,9mV^2/4]$. In particular, $C_1$ and $C_{1/2}$ give the same step and the two endpoint losses. All other steps are impossible.

**Equal-mass control.** With $m_A=m_B=m$ and the prescribed incoming velocities, $T$ sends A outward at $V$ and B inward at $-2V$. For perfect contact, local balance gives $v_A^++v_B^+=-V$ and restitution gives $v_B^+-v_A^+=3V$. B goes outward at $V$ and A inward at $-2V$. Exchanging labels maps one outgoing state and all its ordered equations to the other. The unlabeled mass distribution agrees at every time through the gate. Both records have the same encounter stamp, time $F(1,5/2)R/V$, and inward field $3Gm/d^2$ until its drop to $2Gm/d^2$. Both losses vanish. A material tag read on the outward shell would distinguish A in $T$ from B in $C_1$.

The calculation uses supplied Newtonian shell dynamics, synthetic preparations, infinitesimal shells and calibrated $m,G,R$, clock and field gain. It covers the encounter and first outward detector crossing at exact resolution. DET supplies no physical identification or calibration for these inputs in this packet. For background on intersecting Newtonian shells, see [Barkov, Belinski and Bisnovatyi-Kogan, *Chaotic motion and ballistic ejection of gravitating shells* (v2)](https://arxiv.org/abs/astro-ph/0107051v2).


The gravitational field drop registers a change in the mass enclosed by the detector. The contact loss uses the closed Newtonian energy balance. A material tag has a different role from the field measurement in the equal-mass control. [Separate relativistic shell proper-mass measurement](shell_proper_mass_from_crossing_times.md)
