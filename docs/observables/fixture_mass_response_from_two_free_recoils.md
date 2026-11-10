# Calibrating the exterior fixture response with two free recoils

Two opposite elastic backscatters on fresh copies of the baseline carrier determine its common initial rapidity and the tagged radiation action per unit inertial rest mass. Combining that ratio with the same channel's absolutely calibrated gravitational burst action gives $GM_0/(Rc^2)$. The accepted fixture slope then gives its response $\kappa$ separately. A common unknown burst counting efficiency leaves a continuous ambiguity in both quantities, even with exact recoil frequencies.

## Two directions and one rest mass

Let $R$ be the burst's inner areal radius and $T$ the scattering lab's local tick. The measured frequencies in tick units are $w=\omega T$ for the common incident frequency and $v_s=\omega'_s T$ for the outgoing photon in each preparation. The label $s=+1,-1$ is the **incident** direction on a fixed lab axis. Each outgoing direction is $-s$. Require finite positive $w,v_+,v_-$, a registered positive $H=R/(cT)$, and two initial targets of the same rest mass $M_0>0$ and signed rapidity $y$. The incident and outgoing photon in both events obey $E=J_c\omega$ for the same positive tagged action. The observations use angular frequencies with a calibrated zero.

Use energy units for both components of four-momentum and metric signature $(+,-)$. Write $M=M_0c^2$, $E=J_c\omega$, $E_s'=J_c\omega_s'$ and
$$
 P=M(\cosh y,\sinh y),\qquad k_s=E(1,s),\qquad k'_s=E_s'(1,-s).
$$
Conservation gives $P'_s=P+k_s-k'_s$. Elastic recoil requires $(P'_s)^2=P^2=M^2$. The photon vectors are null and $k_s\cdot k'_s=2EE_s'$. Thus
$$
 ME e^{-sy}-ME_s'e^{sy}=2EE_s',\qquad
 r_s:=\frac{w}{v_s}=e^{2sy}+2A e^{sy},\qquad A:=\frac{J_c\omega}{M_0c^2}>0. \tag{1}
$$
At $y=0$ both ratios are $1+2A$, the backscatter limit for a free target initially at rest. Compton's fixed journal paper gives the historical recoil context. The signed moving-target inverse here follows from (1). [Compton, *Physical Review* 21, 483 (1923)](https://doi.org/10.1103/PhysRev.21.483)

Put $u=e^y$. Equating $2A=r_+/u-u=r_-u-1/u$ gives the unique finite candidate
$$
 y=\tfrac12\ln\frac{1+r_+}{1+r_-},\qquad
 A=\frac{r_+r_--1}{2\sqrt{(1+r_+)(1+r_-)}},\qquad
 \boxed{\delta:=\frac{J_c}{M_0cR}=\frac{A}{wH}}. \tag{2}
$$
For positive frequency records the sharp remaining check is $r_+r_->1$, equivalently $v_+v_-<w^2$. Equality would give $A=0$ and a smaller product of the ratios would give $A<0$. Either fails for a positive action at finite positive mass and frequency. Either single outgoing frequency can exceed the incident frequency. Equal outgoing readings give $y=0$ and pass exactly when each is below the incident frequency.

For sufficiency, insert the positive root $u$ and $A$ into (1) to recover *each* outgoing frequency. For any allowed $R,T$ and $J_c>0$, set $M_0=J_c\omega/(A c^2)$. The constructed target recoil has $(P'_s)^2=M^2>0$ and light-cone component $P_s^{\prime 0}+sP_s^{\prime 1}=Me^{sy}+2E>0$. Its other light-cone component equals $M^2/(Me^{sy}+2E)>0$, so the recoiling target is future-directed in both shots. This proves kinematic attainability on the assumed two-body channel. The event rate is a separate physical input.

A single direction cannot calibrate the mass with unknown rapidity. For a fixed ratio $r_s>0$, choose any $z=e^{sy}$ in $(0,\sqrt{r_s})$ and set $2A=r_s/z-z$. This continuous function decreases from infinity to zero. Every $A>0$ therefore reproduces the same incident and outgoing readings, with a suitable positive $M_0$ even at fixed $J_c$. Allowing the two targets unrelated initial rapidities restores this same ambiguity separately in each shot. The earlier free absorption/emission result uses a change of internal mass and yields a transition mass ratio. Its photon conversion and mass labels do not calibrate the present elastic arm. [Free photon recoil and mass ratio](free_photon_recoil_and_mass_ratio.md)

**Finite example.** Take $e^y=2$ and $A=1/4$. Equation (1) gives $(r_+,r_-)=(5,1/2)$, so for $w=1$ the observed pair is $(v_+,v_-)=(1/5,2)$. Their product is $2/5$. Equation (2) returns $y=\ln2$, $A=1/4$ and $\delta=1/(4H)$. The blueshift in the second shot draws on the initial target motion. For a joint realization, choose an admissible full-rank burst preparation and tagged action $J_c$ from its positive solution. Choose a registered tick with the specified $H$ and set $M_0=4J_c/(c^2T)$. Two copies at rapidity $\ln 2$ realize the events above. The fixture can have any compatible blank and positive slope, with its response set by the conversion below. Independently supplied scalar data must meet their own registration and admissibility checks.

## Joining the recoil, burst and fixture records

The accepted burst inverse supplies $\gamma=GJ_c/(c^3R^2)>0$ from two independent spectral mixtures, local outer-sphere energy, the registered burst tick and absolute populations. Select the channel actually used in both recoil shots. The burst and scattering ticks can differ if time transfer independently supplies $H$ for the scattering tick and the same areal $R$. A tag name or a common frequency unit alone does not establish the same energy per angular frequency in the two arms. [Accepted gravitational radiation-action inverse](radiation_action_from_two_gravitating_bursts.md)

Let $R_f$ be the inner **areal** radius of the exterior fixture and $F=R_f/R$ its known ratio to the burst radius. For compatible blank and three-load clock data the accepted exterior law is $2GM_{\rm ext}(t)/(R_f c^2)=b+at$, where $M_{\rm ext}(t)=M_B+\kappa M_0t$, $b\ge0$, $a>0$, and $t$ is the registered inertial load ratio. With an admitted scalar action $j=J_s/(M_0c\ell)>0$ and registered $L=R/\ell$, the following quantities are determined. [Exterior clocks and scalar gravity coupling](exterior_clocks_and_scalar_gravity_coupling.md)

| Quantity | Value from registered observations |
|---|---|
| Baseline inertial mass in units of $Rc^2/G$ | $\displaystyle\mu=\frac{GM_0}{Rc^2}=\frac{\gamma}{\delta}$ |
| Fixture response per unit baseline load | $\displaystyle\kappa=\frac{aF}{2\mu}$ |
| Exterior blank mass and loaded mass in baseline units | $\displaystyle\frac{M_B}{M_0}=\frac{bF}{2\mu},\qquad\frac{M_{\rm ext}(t)}{M_0}=\frac{(b+at)F}{2\mu}$ |
| Scalar gravity strength | $\displaystyle\alpha_s=\frac{GM_0^2}{cJ_s}=\frac{\mu L}{j}$ |
| Squared scalar gravitational length in scalar units | $\displaystyle\frac{GJ_s}{c^3\ell^2}=j^2\alpha_s=\mu jL$ |
| Radiation-to-scalar action ratio | $\displaystyle\frac{J_c}{J_s}=\frac{\delta L}{j}$ |

The first identity follows by dividing two independently measured quantities with the same $J_c$. The fixture then tests a proposed value of $\kappa$, including unity, against its own accepted slope. The last row permits a separate equality test $J_c/J_s=1$ using recoil, $j$ and length registration alone. The conversion to $\mu$ does not assume that equality. Without $H$, recoil gives $A$ and $J_c/(M_0c^2T)=A/w$ but leaves $\delta$ unresolved. An unregistered recoil-to-burst action ratio or recoil-to-baseline mass ratio likewise multiplies the inferred mass conversion by an unknown factor. An unregistered $F$ leaves the fixture response undetermined, and an unregistered $L$ leaves the scalar transfer undetermined.

The mass and action units here are $Rc^2/G$ and $c^3R^2/G$. An absolute $R$, or an absolute $T$ and $H$ giving $R=cTH$, with physical $c,G$ gives the dimensional mass and actions. With dimensionless registrations alone the common length scale is free. For example, scale lengths and times by $\lambda>0$, geometric and inertial masses by $\lambda$, actions by $\lambda^2$ and frequencies by $1/\lambda$. The dimensionless recoil frequencies, $H$, all the ratios in the table and the burst and fixture records persist with the corresponding dimensional apparatus scales and inverse energy-display gain. This result leaves the universality of $\kappa$ across sources open.

## What a common unknown counting efficiency preserves

Suppose the observed burst population **measure** in each band is $\epsilon$ times its true measure, with the same fixed $0<\epsilon\le1$ at all included angles, frequencies and times in both bursts. Full rank determines the effective channel value $\widehat\gamma=\gamma/\epsilon$ and the ratio of the two radiation actions. Scattering frequencies of correctly identified individual events still give the same $y,A,\delta$. Define $\widehat\mu=\widehat\gamma/\delta$, $\widehat\kappa=aF/(2\widehat\mu)$ and $\widehat\alpha_s=\widehat\mu L/j$. Then the sharp joint ambiguity under these premises is
$$
 (\gamma,\mu,\kappa,\alpha_s)
 =(\epsilon\widehat\gamma,\ \epsilon\widehat\mu,\
   \widehat\kappa/\epsilon,\ \epsilon\widehat\alpha_s),
 \qquad 0<\epsilon\le1. \tag{3}
$$
In particular $\mu\in(0,\widehat\mu]$, $\kappa\in[\widehat\kappa,\infty)$ and $\alpha_s\in(0,\widehat\alpha_s]$, with the same $\epsilon$ in all three. A proposed $\kappa$ below that lower bound can still be excluded. The products $\kappa\mu=aF/2$ and $\kappa\alpha_s=aFL/(2j)$, the recoil ratio $\gamma/\mu=\delta$, and $J_c/J_s=\delta L/j$ all remain fixed. The burst's two-band equality test survives a common efficiency. Separate unknown band efficiencies also remove that two-band equality test. For mass calibration with one tagged band it is that band's absolute normalization that matters.

To realize (3) on the **same record**, begin with the $\epsilon=1$ realization. At fixed $R,R_f,\ell,T,c,G$ and fixed burst geometry, multiply both radiation actions by $\epsilon$ and increase both true burst population measures by $1/\epsilon$. Applying efficiency $\epsilon$ reproduces every displayed moment while preserving the true band energy currents, macroscopic clocks, fluences and radar observations. Multiply all registered inertial masses and $J_s$ by $\epsilon$. Both photons and target four-momenta in each recoil event scale by $\epsilon$ at the original frequencies and rapidity, so all three scattering frequencies and the elastic vertices persist. Scale the common spring stiffness by $\epsilon$ to retain the mechanical periods and mass ratios. The scalar ratio, scalar conversion $M_0c/J_s$, and native histories stay fixed. Replace $\kappa$ by $\kappa/\epsilon$ and keep the blank mass fixed. Every loaded exterior mass, slope and fixture clock reading is then identical. The same baseline is used in every arm within each realization. No absolute mass datum or burst population count in this record distinguishes the realizations.

## Physical scope

The recoil result assumes a locally inertial lab, collinear signed axes, equal incoming lab frequencies, fresh targets with identical initial velocity and rest mass, a freely recoiling unchanged internal state, and one incoming and one outgoing tagged quantum at each vertex. A support impulse, internal excitation, unobserved radiation or a direction-dependent frequency shift changes (1). The baseline registration must cover the complete load, including any attachments or stored energy relevant to its inertial mass. Binding and support can affect the fixture response. The value inferred applies to the tested load law and preparations.

The burst still needs complete matched energy and population accounting, stable ticks and supported radius stations. The scattering arm needs a calibrated local frequency zero and scale in tick units, valid time transfer, a qualified selection of elastic events, and independent evidence that the same tagged action holds across frames, frequency ranges and arms. Preparing equal velocities, supplying the incident photons, collecting outgoing frequencies, restoring targets and readout, and maintaining the fixture and radar stations all require resources. These records do not measure their work or event probabilities. The calculation uses stipulated relativistic four-momenta and conditional burst, scalar and exterior models. It establishes identifiability for exact records without new measurements or a universal action postulate.
