# A sharp mass interval from boundary impulse and two energy certificates



Let $P=M_{\rm port}>0$ be the known sum of the two terminal masses, $v=\Delta V=aT>0$ their common velocity change, and $M=P+\mu$ the total mass, with interior mass $\mu\ge0$. The instrument displays $J_{\rm disp}$ with absolute error at most $\epsilon_J$ on the true summed boundary impulse. Independently certified interior kinetic energy relative to the terminals is at most $E_*$ at each endpoint. The **exact feasible set** is
$$
\boxed{\quad M=P+\mu,\qquad \mu\ge0,\qquad
 |J_{\rm disp}-(P+\mu)v|\le \epsilon_J+2\sqrt{2\mu E_*}.\quad} \tag{1}
$$
It is a finite closed interval whenever nonempty. Every included mass, even at a saturated boundary, has a finite connected spring realization.

## What the impulse measures

In the registered inertial frame let the common terminal velocity be $V(t)$, and denote each interior mass and its velocity relative to the terminals by $m_i,w_i(t)$. The network momentum is $M V(t)+p(t)$, where $p(t)=\sum_i m_i w_i(t)$. Pairwise spring forces cancel from the total momentum balance. With only the two actuators supplying external longitudinal impulse, the true reading is
$$
J=\int_0^T (F_L+F_R)\,dt=Mv+p(T)-p(0).
$$
No frequency or equilibrium opening is needed. At $t=0,T$, Cauchy–Schwarz and the separate certificates give
$$
 |p(t)|^2\le\left(\sum_i m_i\right)\left(\sum_i m_iw_i(t)^2\right)
 \le 2\mu E_* .
$$
The momenta may have opposite signs. Their difference therefore has magnitude at most $2\sqrt{2\mu E_*}$. Intersecting the allowed true-impulse interval about $Mv$ with the closed meter interval $[J_{\rm disp}-\epsilon_J,J_{\rm disp}+\epsilon_J]$ gives (1). This uses the mass of the unknown interior in the momentum bound; the known ports move exactly at $V(t)$. Impulse has units $\mathrm{N\,s}=\mathrm{kg\,m/s}$, $E_*$ has units of joules, and $\sqrt{\mu E_*}$ has impulse units.

## Computing the interval, including incompatible displays

Set $x=\sqrt{\mu}$, $b=2\sqrt{2E_*}$, and subtract the known port impulse to form
$$
 L=J_{\rm disp}-Pv-\epsilon_J,\qquad U=J_{\rm disp}-Pv+\epsilon_J.
$$
Equation (1) is equivalent to $x\ge0,\ vx^2-bx\le U,\ vx^2+bx\ge L$. The first parabola has minimum $-b^2/(4v)=-2E_*/v$. Thus the record is incompatible precisely when
$$
 J_{\rm disp}+\epsilon_J<Pv-2E_*/v .
$$
For every other record define
$$
 s=\sqrt{b^2+4vU},\quad
 x_{\max}=\frac{b+s}{2v},\qquad
 x_{\min}=\max\left\{0,\frac{b-s}{2v},
 \frac{\sqrt{b^2+4v\max(L,0)}-b}{2v}\right\}.
$$
The answer is $[P+x_{\min}^2,\,P+x_{\max}^2]$. The first quadratic confines $x$ between its roots. The second is increasing on the nonnegative axis and adds only a lower cutoff. At $x_{\max}$, $vx^2+bx=U+2bx\ge L$, proving the claimed nonemptiness. The limiting compatible display with $U=-2E_*/v$ gives a singleton. A signed impulse can be negative despite $v>0$ if the interior loses enough forward relative momentum.

* **Zero interior mass.** $M=P$ is included exactly when $|J_{\rm disp}-Pv|\le\epsilon_J$. A positive spring between the two translating terminals gives a connected realization with no interior masses.
* **Zero energy budget.** Both endpoint relative momenta vanish. The set is $[P,\infty)\cap[(J_{\rm disp}-\epsilon_J)/v,(J_{\rm disp}+\epsilon_J)/v]$, including a singleton for an exact compatible meter.
* **Exact impulse with positive budget.** Taking $\epsilon_J=0$ in (1) leaves the full allowed momentum change. Perfect integration alone need not give a unique mass.

## Attaining every mass with one interior particle

For any candidate $\mu>0$ satisfying (1), choose a true impulse $J$ in the intersection of the two closed intervals used above. Write $s_p=J-(P+\mu)v$. Make a three-particle chain with the known positive terminal masses and a central mass $\mu$. Connect it to each terminal with an identical positive spring of stiffness $k=\mu\omega^2/2$, taking $\omega=\pi/T$. This frequency is a choice for a physical witness; computing (1) requires no frequency measurement.

Relative to a common translation $X''=a$, the centre's displacement $y$ from its translated equilibrium obeys $y''+\omega^2 y=-a$. Choose
$$
 w_0=-\frac{s_p}{2\mu},\qquad
 y(t)=-\frac{a}{\omega^2}+\frac{w_0}{\omega}\sin(\omega t).
$$
The actual interior relative velocities are $w_0$ initially and $-w_0$ finally. The momentum change is exactly $-2\mu w_0=s_p$, and each endpoint has relative kinetic energy $s_p^2/(8\mu)\le E_*$. With the same force sign convention at both terminals, the applied forces are $m_La-ky$ and $m_Ra-ky$, which integrate in sum to the selected $J$. The allowed meter error then reproduces the given display, including equality at either bound.

The positions, velocities, forces and spring energy are finite for each candidate. Equilibrium spacings can exceed $a/\omega^2+|w_0|/\omega$ to keep the particles ordered. If an existing positive spacing is to be respected, an arbitrarily large odd multiple of $\pi/T$ gives the same endpoint reversal with a smaller excursion and finite positive stiffness. This construction also works when $s_p=0$: the static relative offset transmits the required acceleration with zero relative motion. No assumption of zero initial spring energy was made.

## What the certificates add

Without the endpoint energy constraints, for **every** $\mu>0$ one may set $J=J_{\rm disp}$ and use the same finite construction with $w_0=-(J_{\rm disp}-(P+\mu)v)/(2\mu)$. Every finite display then admits all $M>P$. The zero-interior case still requires $|J_{\rm disp}-Pv|\le\epsilon_J$. The impulse measures the system’s net momentum change, but yields no further upper mass bound when the interior relative momentum change is free.

The relative kinetic-energy caps must cover every hidden moving mass, in the common terminal velocity frame and at both specified instants. Establishing them requires independent knowledge of the preparation or a calibrated kinetic-energy bound. A spring-energy budget, a single pre-stroke reading, or the impulse display by itself supplies no such pair of certificates. Their use here places no upper bound on spring potential or on whole-trajectory energy across candidate networks. The calibrated impulse meter must register both signed actuator impulses over the same interval, with a certified absolute error on their sum. Finite instantaneous force samples alone do not certify that integral without independent integration-error information. The common velocity change, terminal mass, frame, timing and impulse standard are supplied physical calibrations.

For inertial displacements $u_i$ from equilibrium the mechanical energy contains all particle kinetic energies and one elastic term per edge,
$$
 H=\tfrac12\sum_i m_i\dot u_i^2+
 \tfrac12\sum_{\{i,j\}} k_{ij}(u_i-u_j)^2,\qquad
 H(T)-H(0)=\int_0^T(F_L+F_R)V(t)\,dt .
$$
This is signed actuator work in joules; the impulse integral weights the force by time alone. The displayed impulse and the endpoint kinetic caps do not determine this work or the cost of preparing, reading and resetting the apparatus. The accepted timing and recoil studies used different observations and energy restrictions. Equation (1) is a conditional result in the stated Newtonian network.

[Force timing and finite precision](total_mass_with_two_sampling_intervals.md) · [Nine-force mass measurement](total_mass_from_nine_boundary_forces.md)
