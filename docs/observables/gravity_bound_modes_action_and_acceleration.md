# What gravity-bound modes measure about action and free fall

Two spatial differences and a beat determine the action per inertial mass and the downward acceleration in each registered sector, up to two explicit instrument factors. With a common ruler gain, common frequency gain and known inertial mass ratio, the readings decide separately whether the sectors share an action and whether they share a passive-to-inertial mass ratio. An absolute mass reference is useful for reporting action in physical units. Neither equality test needs it.

## Two lengths with different physical meanings

Take one sector and suppress its index. Use upward height $z$, inertial mass $M>0$, action $J>0$, and downward force magnitude $F=Pg>0$. Allow a constant energy offset $C$ in the given linear potential. Set
$$
 \ell^3=\frac{J^2}{2MF},\qquad z_E=\frac{E-C}{F},\qquad
 \xi=\frac{z-z_E}{\ell}.
$$
The stationary equation becomes $\psi_{\xi\xi}=\xi\psi$. Decay in the unbounded upper region selects $\operatorname{Ai}(\xi)$ up to normalization. Let $a_1>a_2>\cdots$ denote its negative zeros, ordered from the top, and let $\delta=a_1-a_2>0$ (approximately $1.74984$). A tagged node in the linear region has height $z_E+\ell a_j$. The unknown lower reflector selects the allowed energies. Its phase need never be fitted, since the same upper-tail zero is identified in the two modes.

Denote the three raw heights by $X_{L1},X_{L2},X_{H1}$, where 1 is the top node and 2 the next node down. With $X=sz+b_i$ and $Y=t\omega$, form
$$
 A=\frac{X_{L1}-X_{L2}}{\delta}=s\ell,\qquad
 B=X_{H1}-X_{L1}=s\,\frac{\Delta E}{F},\qquad
 Y=t\,\frac{\Delta E}{J},\qquad \Delta E=E_H-E_L>0. \tag{1}
$$
The first difference removes the lower mode’s turning height. The second cancels the common top-node displacement $\ell a_1$. The energy gap is the actual gap of these two modes with their reflector in place. Every static energy offset common to the modes and each sector’s coordinate origin $b_i$ cancel. The beat uses angular frequency and the same $J$ that appears in the kinetic term.

Finite heights, $X_{H1}>X_{L1}>X_{L2}$ and finite $Y>0$ are necessary. Zero separation or zero beat falls outside this measurement. The conclusions below apply on the stipulated physical domain of two actual modes of one static lower reflector in each sector. These inequalities alone do not certify that arbitrary proposed heights and a beat belong to such a spectrum.

## Recovering the two coefficients

Write $\eta=J/M$ and $\gamma=F/M$. In physical units (1) gives $\ell=A/s$ and $\gamma/\eta=F/J=sY/(tB)$. Combining these with $\ell^3=\eta^2/(2\gamma)$ yields
$$
 \widehat\eta=2A^3\frac{Y}{B}=s^2t\,\eta,\qquad
 \widehat\gamma=2A^3\left(\frac{Y}{B}\right)^2=st^2\,\gamma . \tag{2}
$$
This positive solution is unique for specified gains. It recovers the measured node spacing from $\ell$ and the measured intermode shift from $\Delta E/F=(Y/t)\eta/\gamma$. The scales of $\eta$ and $\gamma$ are respectively length squared per time and length per time squared. Here $t=Y/\omega$ is the frequency gain. Converting the displayed beat to physical angular frequency divides by $t$.

For sectors 0 and 2 let $r=M_2/M_0>0$ be their registered inertial ratio. The two common gains cancel between sectors, giving
$$
 \frac{J_2/M_2}{J_0/M_0}=\frac{\widehat\eta_2}{\widehat\eta_0},\qquad
 \frac{J_2}{J_0}=r\,\frac{\widehat\eta_2}{\widehat\eta_0},\qquad
 \frac{P_2/M_2}{P_0/M_0}
 =\frac{\gamma_2}{\gamma_0}=\frac{\widehat\gamma_2}{\widehat\gamma_0}. \tag{3}
$$
A common action holds exactly when $r\widehat\eta_2=\widehat\eta_0$. A common downward free-fall acceleration holds exactly when $\widehat\gamma_2=\widehat\gamma_0$. The latter is a test of equal $P/M$ because both sectors experience the same positive $g$. A value of $P/M$ for an individual sector additionally requires $g$ in the acceleration convention. These are independent comparisons in the model, which permits independent positive $J_i,F_i$. Its hard-wall subclass has the requisite modes for each such choice.

## What an absolute mass certificate adds

Reporting $J_i/M_i$ in physical units requires $s^2t$. Reporting $F_i/M_i$ requires $st^2$. Calibrating length and angular frequency supplies both products. With that calibration and a separately registered CL078 candidate set $\mathcal M$ for $M_0$, the paired action candidates are
$$
 \left\{(J_0,J_2)=
 \left(m\frac{\widehat\eta_0}{s^2t},\;r m\frac{\widehat\eta_2}{s^2t}\right)
 : m\in\mathcal M\right\}. \tag{4}
$$
Both entries must use the same candidate $m$. A singleton gives a dimensional action for each sector. Several possible masses give the corresponding finite set of action pairs. Without an absolute mass reference, simultaneous rescaling of $M_i,J_i,F_i$ by a common positive factor preserves $\ell_i$ and the beat in the hard-wall model, with all energies rescaled by that factor. Even a singleton for $M_0$ leaves a conversion factor if $s^2t$ is unknown. The CL078 transfer requires the spring and store certificate to concern the same prepared carrier masses. E63’s held internal levels and the earlier action-per-occupation construction supply no identification of their coefficients with this spatial $J_i$.

## A missing ruler can reverse both answers

Retain the beat calibration and masses, and allow a separate uncalibrated ruler gain $s_i$ for each sector. Use one hard Dirichlet wall at $z=0$ in both worlds and choose energy zero there. For any positive $J_i,F_i,M_i$, the $n$th mode is proportional to $\operatorname{Ai}(z/\ell_i+a_n)$ with $E_{in}=-F_i\ell_i a_n$. Choose $L=3$ and $H=4$. The third mode has two interior nodes, and the fourth has a top interior node. In the requested order the three true heights and the beat are
$$
 \ell_i(a_1-a_3),\quad \ell_i(a_2-a_3),\quad
 \ell_i(a_1-a_4),\qquad
 \omega_i=F_i\ell_i(a_3-a_4)/J_i .
$$
All three nodes lie strictly above the wall, in the exact linear potential. The displayed record applies $s_i z+b_i$ to these three heights and $t\omega_i$ to the beat.

Start with $J_0=J_2=J_*>0$, $F_i=M_i\gamma_*$ for one $\gamma_*>0$, and equal ruler gains $s_i=s$. Take any fixed $g,t>0$ and origins $b_i$. In the second world set $\lambda_0=1,\lambda_2=2$ and
$$
 M_i'=M_i,\qquad J_i'=\lambda_i^2J_i,\qquad
 F_i'=\lambda_i F_i,\qquad P_i'=F_i'/g,\qquad s_i'=s/\lambda_i .
$$
Keep the same wall, mode numbers, $g,t,b_i$. Then $\ell_i'=\lambda_i\ell_i$ and $E_{in}'=\lambda_i^2 E_{in}$. Each true node height scales by $\lambda_i$, its displayed height stays fixed, and the energy gap and action scale together, preserving each displayed beat. Thus all eight raw readings agree, even at the same absolute masses. The action ratio changes from 1 to 4, and the acceleration ratio from 1 to 2. The combination $(J_2/J_0)/(\gamma_2/\gamma_0)^2$ still cancels separate ruler gains in (2)–(3). This surviving combination does not decide either equality separately.

## Physical registration

The result needs preparation of both tagged modes within each sector and a beat readout sensitive to their relative phase evolution, with stable frequency transfer between sectors. Each beat concerns one sector, so these readings require no cross-sector superposition. It needs a common relative length calibration, a stable origin within each sector, and resolution sufficient to identify the specified top and next-to-top nodes. It assumes that both modes share a static lower interaction, the observed nodes lie above its range, and the decaying tail has no upper reflector. A residual upper-region force can change the node spacing and the intermode shift. Preparation, maintenance of the field and boundaries, node and beat detection, reference calibration and reset are supplied physical operations. The result is conditional on those registered readings and gives no acquisition probability or resource cost.

Suda et al. use Airy modes for neutrons in a linear gravitational potential. Jenke et al. observed driven transitions between gravitationally bound neutron states. These works motivate the assumed spatial and frequency observables. The two-sector inverse uses the equation and beat law supplied here. An identification of its action with $\hbar$, the earlier occupational action, or a native DET unit would require an independent physical link. [Suda et al. (2021)](https://arxiv.org/abs/2111.02769v1) · [Jenke et al. (2011)](https://www.nature.com/articles/nphys1970)

## Scientific review

DET Energy Research supplied the gravity-bound mode inverse. A distinct reviewer checked its Airy scaling, relative calibrations and the two hard-wall systems with identical readings. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `fb8f896200eee61b6951fef4d1c7b5058fb838f12769ba0eaf0c1d108e6c3929`.
- Author report SHA-256: `06dc219039ee8dcbfb8086caa9545a850cb36bc04c7c03b29140d961641eeacd`.
- Author freeze SHA-256: `485658c7f8a2a15dcc87f5b03456d22e0f91b5b2b2bb06aeb230235448568c74`.
- Independent scientific review SHA-256: `a39fa75db1c0ade6bdc12eba12b91587e9ff793b2317b739d4773dac78b9c228`.
