# Two clock conventions for a supported light cavity

A pulse pushes the upper mirror upward and the lower mirror downward. Both contacts repeat with the same base-clock period, while the upper clock advances faster. For a short cavity, the magnitude of the downward force divided by the base acceleration tends to $2E/c^2$ when each rate uses its local clock, and to $E/c^2$ when both rates use the base clock. At finite height even the latter ratio differs from $E/c^2$.

## One round trip

Let $N(z)=1+gz/c^2$, $h=N(L)>1$, and $s=\ln h$. The instant immediately after the initial bottom reflection sets the initial pulse and $t=0$. From $ds^2=0$, the travel time on each leg is $\int_0^L dz/[cN(z)]=(c/g)s$. The top reflects at $t_1=(c/g)s$, and the bottom reflects at $t_2=2(c/g)s$. The impulse window $(0,t_2]$ includes the top and final bottom reflections. The outgoing pulse defines the endpoint on both cuts.

Stationary clocks have $d\tau=N\,dt$. Comparing both clocks on the same slices $0,t_2$ gives $\Delta\tau_b=2cs/g$ and $\Delta\tau_t=h\Delta\tau_b$. The top duration is the advance of its clock between those slices. It requires only the one sampled top impact.

Write $u=N^{-1}\partial_t$ for a stationary observer's four-velocity and $p$ for the ray four-momentum. The conserved energy $-p\cdot\partial_t$ on a free null leg equals $N(-p\cdot u)=N E_{\rm loc}$. Reversal at a stationary mirror preserves $E_{\rm loc}$ and hence this conserved energy across the impact. Its value throughout is the supplied bottom launch energy $E>0$. The top measures $E/h$ on both sides of reflection, and the bottom measures $E$ on return and relaunch. The signed local momenta of a null ray are $\pm E_{\rm loc}/c$. Taking minus the change of pulse momentum, with $+z$ upward, gives
$$
J_t=+2E/(hc),\qquad J_b=-2E/c .
$$
There is zero local energy transfer in each mirror's instantaneous rest frame.

## What the two clock displays measure

Substitution in the two specified signed rates gives
$$
-\frac{F_{\rm local}}{g}=-\frac{1}{g}\left(\frac{J_b}{\Delta\tau_b}+\frac{J_t}{\Delta\tau_t}\right)
=\frac{E}{c^2}\frac{1-h^{-2}}{\ln h},\qquad
-\frac{F_{\rm base}}{g}=-\frac{J_b+J_t}{g\Delta\tau_b}
=\frac{E}{c^2}\frac{1-h^{-1}}{\ln h}.
$$
Both pulse-on-mirror displays point downward. Their positive mass-dimension ratios differ by the factor $1+h^{-1}$ (local divided by base). The top term in the local rate carries one factor $h^{-1}$ from energy and one from its clock.

For $s>0$, $(1-e^{-ks})/s=\int_0^k e^{-sv}\,dv$. With $k=1$, the dimensionless base ratio lies strictly between zero and one. With $k=2$, the local ratio in units of $E/c^2$ decreases strictly and continuously from two to zero as $s$ increases. There is a unique $s_*>0$ satisfying $1-e^{-2s_*}=s_*$. Thus $-F_{\rm local}/g$ exceeds $E/c^2$ below $s_*$, equals it at $s_*$, and falls below it above $s_*$, with $s=\ln h$. For $gL/c^2\to0^+$ with $E$ fixed, the integrals tend to $2$ and $1$ for the local and base conventions respectively. Division by $g$ is defined here for $g>0$.

## Fixed inertial ledger at $h=5/4$

Use the inertial coordinates initially at rest with the bottom mirror, with rapidity $\eta=gt/c$ and $\rho=c^2/g+z$. The transformation $cT=\rho\sinh\eta,\ Z+c^2/g=\rho\cosh\eta$ recovers the prescribed metric and gives the mirror velocity $dZ/dT=c\tanh\eta$. The local-to-lab boost on $(E_{\rm ray}/c,p_z)$ has diagonal entries $\cosh\eta$ and off-diagonal entries $\sinh\eta$. Thus a rightward null energy gains a lab factor $e^\eta$, and a leftward one a factor $e^{-\eta}$.

At the top impact $\eta=s$, giving $(\cosh\eta,\sinh\eta)=(41,9)/40$. At the final bottom impact $\eta=2s$, giving $(881,369)/800$. The final bottom rest frame therefore moves with rapidity $s$ relative to the top impact frame, or relative speed $9c/41$ toward $+z$. Relative to the initial lab the final bottom speed is $369c/881$. The two-clock impulse records are $J_t=8E/(5c)$, $J_b=-2E/c$. The base duration $2c\ln(5/4)/g$ equals $8L\ln(5/4)/c$, and the top duration is $5/4$ times that. In units of $E/c^2$ the local and base mass comparisons are $9/[25\ln(5/4)]$ and $1/[5\ln(5/4)]$, respectively.

The following entries are lab components $(E_{\rm ray}/c,p_z)$ in units of $E/c$. Propagation keeps the entries constant between impacts.

| Included impact | Incoming pulse | Outgoing pulse | Mirror acting on pulse, outgoing minus incoming |
|---|---|---|---|
| Top | $(1,1)$ | $(16/25,-16/25)$ | $(-9/25,-41/25)$ |
| Final bottom | $(16/25,-16/25)$ | $(25/16,25/16)$ | $(369/400,881/400)$ |

In particular the local mirror-on-pulse four-impulses are $(0,-8/5)$ at the top and $(0,2)$ at the bottom in the same units. Applying their respective boosts yields exactly the two jumps in the last column. The pulse loses $9E/25$ at the top and gains $369E/400$ at the bottom. Adding the jumps gives $(225,225)/400=(9/16,9/16)$, which is also the difference between the final outgoing $(25/16,25/16)$ and initial outgoing $(1,1)$. The pulse returns with the same locally measured bottom energy $E$, while the outgoing ray at the final cut carries the Doppler factor $e^{2s}=25/16$ in the initial lab. The lab therefore records net work $+9E/16$ and upward impulse $+9E/(16c)$ on the pulse.

The pulse-on-mirror four-impulses have the opposite signs in this same lab. For example, the sum of their local spatial readings is $-2E/(5c)$, while the sum of their lab spatial components is $-9E/(16c)$. The spatial basis of each instantaneous rest frame has a different boost to the lab. Using one denominator on a display still leaves its two impulse readings in those event frames.

## Support, calibration and scope

Relative to the empty prescribed trajectories, if the mirrors retain the same mechanical four-momenta through their impacts and the supports provide the balancing reaction, the additional support-on-mirror impulse at each hit equals minus the pulse-on-mirror four-impulse. On this ideal accounting the supports supply a net $+9E/16$ of lab work and $+9E/(16c)$ of lab momentum to the mirror-plus-pulse subsystem over the cuts. Continuous empty-trajectory support is subtracted. External actuators, mirror material and any stress or energy stored in a connecting structure would require their own records for a total apparatus weight or a closed-system inertia measurement.

The input ruler fixes the proper length $L$ on a stationary slice. The supplied clocks measure proper time in common units, the calibrated base accelerometer scale gives $g$, $c$ relates length and time, and the calibrated local launch energy fixes $E$. The supplied observations include orientation, event order and local energy/impulse readings. $h$ and $s$ are dimensionless, $E/c$ has momentum units, $J/\Delta\tau$ has force units, and $F/g$ has mass units. This one-cycle result uses conventional flat-spacetime propagation, prescribed worldlines and ideal reflection. Claims about active gravity, curvature inferred from measurements, a DET-native mechanism or unit, and empirical realization lie outside those inputs.

CL026 supplies the flat lapse fixture and base radar duration. CL063 and its two-body radiation note use freely recoiling bodies and complete local balances. The radiation-shell note obtains a boost coefficient from a complete stationary conserved source including wall stress. Those accepted targets delimit the present open pulse calculation. Rätzel et al. discuss the physical distinction between prescribed rigidity and a material resonator. [Public background, arXiv:1711.11320v1](https://arxiv.org/abs/1711.11320v1)

## Comparing the readout with system inertia

The shared base-clock denominator registers the impacts per unit base time. Each impulse still belongs to the instantaneous rest frame of its mirror. The common-inertial-frame calculation above transforms the impulses themselves. Inferring the inertia of a complete apparatus would also require the energy, momentum and stress of its load-bearing parts on registered slices. [Inertia of a complete radiation shell](closed_radiation_shell_inertia.md) · [Two-body radiation exchange](two_body_radiation_mass_ledger.md)
