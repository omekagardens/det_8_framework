# Calibrating a sector mass from a coincident two-photon cascade

A certified upper endpoint of the two-photon invariant fixes the baseline inertial mass $M_0$ in units of $Rc^2/G$ when both tagged radiation actions are calibrated by gravitating bursts. The initial carrier velocity may differ on every event. For a finite nonempty list of positive invariants, the compatible masses instead form a closed ray from a calculable lower bound to arbitrarily large mass. The lower bound is attained. Both conclusions use the same free two-step dynamics.

## What the two photons record

Let $r_1=M_1/M_0$ and $r_2=M_2/M_0$, with $1<r_1<r_2$ and $M_0>0$. The common-spring calibration supplies these ratios conditional on faithful sector preparation, a common stiffness and tick, and the accepted phase branch. It allows a common rescaling of all masses and stiffness. An additional physical registration identifies those inertias with the rest masses of the same carrier in three specified internal states. The allowed transition is $2\longrightarrow 1+a$ followed by $1\longrightarrow 0+b$ on that carrier, with the same on-shell intermediate in both vertices. Neither sector preparation nor a successful one-photon occupation readout provides this dynamical link or its angular support. [Sector inertial mass ratios](sector_inertial_mass_ratios.md) · [Radiative readout of one occupation](radiative_readout_of_one_occupation.md)

Use energy units for four-momenta with signature $(+,-,-,-)$, so $P_i^2=M_i^2c^4$. For $h=a,b$ put $k_h=J_h\omega_h(1,\mathbf n_h)$, where $\mathbf n_h$ is the unit propagation direction and $J_h>0$ is the energy per angular frequency of that tag. The measured dimensionless invariant, in one registered proper tick $T$, is
$$
 Q=2(\omega_a T)(\omega_b T)(1-\mathbf n_a\cdot\mathbf n_b)
   =\frac{T^2}{J_aJ_b}(k_a+k_b)^2. \tag{1}
$$
The frequencies and directions on the left must belong to the same event and frame, or be transported into that frame. The tick specifies a common duration standard across events. Changes of inertial frame alter both frequencies and their separation angle together while preserving the four-vector product. No parent velocity measurement enters (1).

## Kinematic range from the two mass shells

Write $P_2=P_1+k_a$ and $P_0=P_1-k_b$. Because each photon is null,
$$
 2P_1\cdot k_a=(M_2^2-M_1^2)c^4,\qquad
 2P_1\cdot k_b=(M_1^2-M_0^2)c^4.
$$
In the **intermediate** rest frame these determine both photon energies,
$$
 E_a^*=\frac{(M_2^2-M_1^2)c^2}{2M_1},\qquad
 E_b^*=\frac{(M_1^2-M_0^2)c^2}{2M_1}.
$$
For an explicit boost check, the first photon has energy $(M_2^2-M_1^2)c^2/(2M_2)$ in the parent rest frame. There the intermediate recoils opposite to the first photon with speed $\beta c$, $\beta=(M_2^2-M_1^2)/(M_2^2+M_1^2)$. The photon energy in the intermediate frame increases by $\sqrt{(1+\beta)/(1-\beta)}=M_2/M_1$, giving $E_a^*$ above.

Let $\theta^*$ be the angle between the two photon directions measured in this single intermediate frame and put $x=(1-\cos\theta^*)/2$. Antiparallel photons give $x=1$. With $u_h=J_h/(M_0c^2T)$, equations (1) and $2k_a\cdot k_b=2E_a^*E_b^*(1-\cos\theta^*)$ give
$$
 F=\frac{(r_2^2-r_1^2)(r_1^2-1)}{r_1^2}>0,\qquad
 Q=Q_{\rm kin}\,x,\qquad
 Q_{\rm kin}=\frac{F}{u_a u_b}. \tag{2}
$$
The closed interval $0\le Q\le Q_{\rm kin}$ is exactly attainable kinematically. Fix $P_1=(M_1c^2,\mathbf 0)$, take photons of the stated energies at any chosen $\theta^*\in[0,\pi]$, and form $P_2$ and $P_0$ as above. The masses satisfy both shells, the parent energy is $M_1c^2+E_a^*>0$, and the final carrier energy is $(M_1^2+M_0^2)c^2/(2M_1)>0$. Each cascade may then be independently boosted. Collinear photons give zero even though both have positive energy. The finite record specified here contains only strictly positive $Q$. The adjacent massless-pair endpoint in successive two-body decays has the same mass-gap factors in the published kinematic comparison. [Gjelsten, Miller and Osland, v1, Eq. (4.3)](https://arxiv.org/pdf/hep-ph/0410303v1)

## When a population endpoint calibrates mass

Suppose the upper endpoint $Q_*>0$ of the registered population support is known in tick units. The necessary additional certificate is that allowed and accepted cascades populate arbitrarily close to $x=1$: for every $0<\varepsilon<1$ there is positive population probability at $x>1-\varepsilon$. No event has to hit exactly $x=1$, and the angular law need not be uniform. Under this premise $Q_*=Q_{\rm kin}$, giving
$$
 \frac{J_aJ_b}{M_0^2c^4T^2}=u_a u_b=\frac{F}{Q_*}. \tag{3}
$$
The cascade alone fixes this product. Changing $J_a$ and $J_b$ by reciprocal positive factors preserves it, so the endpoint alone cannot test equality of the two actions. A known upper edge of a population selected away from antiparallel configurations would supply only an inequality.

Now take the accepted full-rank, positive two-band burst solution with absolute populations, $\gamma_h=GJ_h/(c^3R^2)>0$ for $h=a,b$. The tag-to-action law must hold across the bursts and the two cascade vertices at the respective observed frequencies. Register the cascade tick to the burst's **areal** radius through $H=R/(cT)>0$. Writing $\mu=GM_0/(Rc^2)$ gives $u_h=H\gamma_h/\mu$. Therefore
$$
 \boxed{\displaystyle \mu=H\sqrt{\frac{\gamma_a\gamma_b Q_*}{F}},\qquad
 \frac{GM_i}{Rc^2}=r_i\mu\quad(i=1,2).} \tag{4}
$$
Only the geometric mean of the two calibrated actions enters this mass formula. The separate burst values also supply $J_a/J_b=\gamma_a/\gamma_b$ and determine each $J_h/(M_0cR)=\gamma_h/\mu$. Unknown absolute burst population normalization would leave their geometric mean uncalibrated. The result assumes neither equal radiation actions nor a universal action constant. [Gravitational calibration of the two radiation actions](radiation_action_from_two_gravitating_bursts.md)

If the same baseline carrier is independently registered to the accepted fixture, its measured positive compactness slope is $a_f=2G\kappa M_0/(R_fc^2)$. A registered radius ratio $R_f/R$ then gives $\kappa=a_f(R_f/R)/(2\mu)$. This uses the fixture's own tested load law. The opposite-direction recoil calibration supplies a comparison with different preparation requirements; its velocity matching and mass estimate are not inputs here. To express $M_0$ in kilograms requires the dimensional unit $Rc^2/G$ or an equivalent calibration. For example, an absolute tick and $H$ yield $R=cTH$. [Fixture mass response from free recoil](fixture_mass_response_from_two_free_recoils.md)

## What a finite list actually establishes

Let $Q_1,\ldots,Q_n$ be a nonempty finite list of finite positive invariants and put $q=\max_iQ_i$. Without an angular-coverage promise the full condition is $q\le Q_{\rm kin}$. It gives the following sharp sets:
$$
 0<u_a u_b\le F/q\quad\text{from the cascade},\qquad
 \boxed{\displaystyle \mu\in[\mu_{\min},\infty),\qquad
 \mu_{\min}=H\sqrt{\frac{\gamma_a\gamma_b q}{F}}}
 \quad\text{with the calibrated burst}. \tag{5}
$$
For the registered fixture this gives precisely $0<\kappa\le a_f(R_f/R)/(2\mu_{\min})$. A mass below the bound would make at least one event exceed the kinematic endpoint.

For attainability, take any finite $\lambda\ge1$. Keep $R,T,J_a,J_b$ and the entire burst preparation fixed, set $\mu=\lambda\mu_{\min}$, and use $M_i=r_iM_0$. Rescale the spring stiffness with the sector masses so every earlier spring reading and supported native history remains the same. Then $Q_{\rm kin}=\lambda^2q$. For event $i$ choose
$$
 \cos\theta_i^*=1-\frac{2Q_i}{\lambda^2q},
$$
which lies in $[-1,1)$, and construct both on-shell vertices as above. At $\lambda=1$ an event with $Q_i=q$ has antiparallel photons. At every $\lambda>1$ even the largest observed invariant lies strictly inside the allowed range. A population may assign weight to the constructed angles and velocities under the stated unrestricted preparations. If fixture data are retained, choose $\kappa$ from its measured slope at this same $\mu$ so all loaded exterior masses remain fixed.

This construction can reproduce the measured individual frequencies and directions as well as their invariant. For each positive $Q_i$ the sum of the two photon four-momenta is future timelike. In the pair's center-of-momentum frame the photons are opposite and each has energy $\sqrt{(k_a+k_b)^2}/2$. The constructed and recorded pairs have the same value of this squared sum at the fixed actions and tick. A spatial rotation aligns the first tag, thereby aligning the second. Boosting back to the recorded lab then maps the entire constructed event to the observed photon pair. Event-specific parent velocities are allowed, so this operation imposes no condition on another event. Consequently a finite sample maximum can attain the true endpoint in one compatible world and fall short in other worlds with exactly the same record.

## Physical registration and scope

Coincidence must identify both photons from the same carrier and correctly assign their transition tags. The matched ensemble must retain the stipulated sector states, the intact on-shell intermediate, two-body recoil at each vertex, and free propagation without an unaccounted impulse, additional quantum or energy loss. Photon energies here use angular frequencies and the specified channel actions. Detector coverage, frequency and angle registration, boosts or optical transport to a common frame, the clock-to-radius transfer, and absolute burst population calibration are physical inputs. Conditioning on a detected pair supplies neither a branching probability nor evidence that the detected population reaches the angular endpoint.

Preparing sector 2, supplying its rest and kinetic energy, registering coincidences, recovering or replacing the final carrier, and restoring the apparatus require energy and readout resources. The invariant records contain no measurement of that work. This is an identifiability result under supplied transition dynamics and calibrations. No cascade observation or empirical population endpoint is supplied.
