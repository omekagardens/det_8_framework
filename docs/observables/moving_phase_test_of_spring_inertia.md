# A common-momentum phase test of spring inertia

Under the supplied relativistic dispersion law, three matched moving and stationary phase advances determine the internal offset $z$, the momentum magnitude $P/(M_0c)$ and the moving-to-stationary dwell ratio $\lambda$ whenever the data pass the strict tests below. The offset has an operational meaning within the supplied dispersion law. At $z=0$ its low-momentum inertias agree with the independently measured spring inertias. A feasible nonzero $z$ rejects that additional identification. An additive energy constant *outside* the dispersion remains free.

## Stationary registration and what the phase measures

Take a feasible stationary population record. The registered springs give $m_q=M_q/M_0$ with $1=m_0<m_1<m_2$. For the first-lobe spring readings $y_{ij}$, write $t_{ij}=(\arccos y_{ij})^2$. The three $u_i=(t_{ij}+t_{ik}-t_{jk})/2=KT^2/M_i$ must be positive, with $m_q=u_0/u_q$. This uses the same stiffness $K$, stationary tick $T$, and carrier identities at the three settings. The full signed lift, blank, stroke, echo and work-store feasibility conditions remain those of the accepted stationary experiment. [Sector spring inverse](sector_inertial_mass_ratios.md) · [Stationary phase and action record, §§2–4](action_per_occupation_from_sector_masses.md)

On the supplied occupation tori $J=I_r+I_e=qJ_0$. There is no additional action for the reference-memory bit. The supported native transitions preserve $q$; the sector-one swap commutes with a common rotation of both angles. Retain the phase source preparations $00,10,11$ for $q=0,1,2$, reference-memory label zero, equal initially zero angles, and the same angle convention for states and effects. Both sector-one labels carry the same coefficients. Retain the original tagged mechanical histories and their weights, including support zeros, independently of the phase preparations. A phase dwell is a separate physical operation. The native birth index supplies no elapsed time. [Native phase/action interface](native_phase_action_interface.md)

Let $\phi_q=T E'(qJ_0)>0$ be the stationary common-angle advance. Use a smooth increasing convex stationary profile on the sampled action interval, with level differences $E((q+1)J_0)-E(qJ_0)=M_0c^2(m_{q+1}-m_q)$. Write $\eta=J_0/(M_0c^2T)$ and $\delta_i=m_{i+1}-m_i$. The stationary action set is the intersection of the two segment sets
$$
 \mathcal I_i=\begin{cases}
 (\delta_i/\phi_{i+1},\,\delta_i/\phi_i), & \phi_i<\phi_{i+1},\\
 \{\delta_i/\phi_i\}, & \phi_i=\phi_{i+1}.
 \end{cases}
$$
A decreasing adjacent rate or empty intersection fails the stationary model. Each $\eta\in\mathcal I_0\cap\mathcal I_1$ has an admitted smooth interpolation. Adding a constant to that profile preserves its derivatives, convexity and level differences.

## Moving phase equation

For the moving dwell assume the physical canonical momentum has common constant magnitude $P>0$ in the three preparations, with the actions conserved. The duration is $\lambda T$ for one common finite $\lambda>0$. The proposed Hamiltonian is
$$
 H(J,p)=C_{\rm out}+\sqrt{E(J)^2+c^2p^2},\qquad
 E(qJ_0)=M_0c^2(m_q+z)>0 .
$$
Thus $z>-1$. Use the canonical angle equation at **fixed momentum**. Each component angle has rate $\partial_JH=E E'/\sqrt{E^2+c^2p^2}$, since $\partial J/\partial I_r=\partial J/\partial I_e=1$. Let $\psi_q$ be the unwrapped moving advance over the registered dwell and write $\pi_P=P/(M_0c)$. The observable is
$$
 r_q=\frac{\psi_q}{\phi_q}
     =\lambda\,\frac{m_q+z}{\sqrt{(m_q+z)^2+\pi_P^2}}. \tag{1}
$$
The stationary derivative cancels separately in each sector. The moving dwell may be shorter or longer than $T$. Each $r_q$ is strictly below $\lambda$ and can exceed one if the moving dwell is sufficiently long. No source-dependent boost phase incurred before the dwell may enter its measured advance.

## Complete inverse on the strict physical domain

First verify the stationary record and the phase readout in both arms. For each tagged quadrature, including detector failures, require $\Pr({\rm fail})=1/2$ and $\Pr(\pm)=(1\pm Z)/4$. The independently referenced cosine and sine quadratures reconstruct a point on the unit circle. Require known turns or a band fixing its branch, with both advances finite and positive. The stationary source uses its assured band $0<\phi_q<\pi$. A phase known only modulo $2\pi$ gives a branch-dependent test unless separate registration resolves the turns.

Define $Y_q=r_q^{-2}$, $s=1+z>0$, $h=m_1-1>0$, $\ell=m_2-m_1>0$, and $D=h+\ell$. Equation (1) is equivalent to
$$
 Y_q=A+\frac{B}{(s+m_q-1)^2},\qquad
 A=\lambda^{-2}>0,\quad B=A\pi_P^2>0. \tag{2}
$$

1. Require $Y_0>Y_1>Y_2>0$. Form the ratio of the two adjacent drops, normalized by the mass intervals,
   $$
   R=\frac{\ell(Y_0-Y_1)}{h(Y_1-Y_2)} .
   $$
   Require $R>1$. Find the unique positive $s$ solving
   $$
   R=f(s):=\frac{(2s+h)(s+D)^2}{(2s+h+D)s^2}. \tag{3}
   $$
2. Recover $B=(Y_0-Y_1)/[s^{-2}-(s+h)^{-2}]$ and $A=Y_0-B/s^2$. Require $A>0$. The denominator defining $B$ is positive and step 1 already ensures $B>0$.
3. The unique answer is
   $$
   \boxed{z=s-1,\qquad P/(M_0c)=\sqrt{B/A},\qquad \lambda=1/\sqrt A.}
   $$
   On a feasible record the dimensionless zero-offset test is **$R=f(1)$**. If $R>f(1)$ then $z<0$; if $1<R<f(1)$ then $z>0$.

To prove (3), subtract successive rows of (2); the two differences cancel $A$ and their ratio cancels $B$. The function $f$ falls from infinity to 1 on $s>0$, since
$$
 \frac{d}{ds}\log f(s)=2D\left[\frac{1}{(2s+h)(2s+h+D)}
                                -\frac{1}{s(s+D)}\right]<0 .
$$
The root can equivalently be specified by multiplying out (3) and selecting its positive root. At $R=1$ there is no finite shift. Equal $Y$ entries cannot arise with finite nonzero common momentum and the strictly ordered masses; $A=0$ cannot give a finite positive dwell ratio. The fitted $A,B$ reproduce the first two rows, and (3) reproduces the remaining difference. Positivity then recovers each original signed-positive ratio from its reciprocal square.

For sufficiency with the *full* stationary law, take any of its feasible mechanical realizations and any allowed $\eta$. Choose the stationary interpolation for its level differences and endpoint slopes, then shift its internal origin to $E(0)=M_0c^2s$. It is positive throughout the sampled interval since it is increasing. Set $P=M_0c\sqrt{B/A}$ and the moving dwell to $\lambda T$. This reproduces every sector's moving angle, hence both quadrature outcome laws including failures. The inherited stationary action interval, and its common displayed work-scale constraint, are unchanged by the construction. Direction of the momentum is invisible to this even dispersion. $C_{\rm out}$ is independent of $J,p$ and drops out of all these derivatives and differences.

## A complete feasible record and the momentum-registration check

Use the stationary record of the accepted action experiment, §5. Take masses $M_*(1,2,4)$, $K=M_*/T^2$, stroke length $L=cT$ and work display scale $W=g_w M_*c^2$. The three spring readings are $\cos\sqrt{3/2},\cos\sqrt{5/4},\cos\sqrt{3/4}$. Use its two weak lift fields with displayed clock gaps $g_c j\varepsilon$ and loaded outward/return readings $(j\varepsilon W,-j\varepsilon W)$, with zero blanks. The blank strokes are zero, the engaged strokes are $(j^2W/2,-j^2W/2)$, and echo delays are $(3,5)$ ticks. The donor's store with initial level $(3+2\varepsilon)W$ covers these reversible mechanical trials.

Keep every native history $H=(a,b_1,b_2)$ with the original $p_i(H)=q_a(1+\epsilon_a{\bf1}_{i=1}/2)/4$, $(q_E,q_F)=(2/3,1/3)$ and $(\epsilon_E,\epsilon_F)=(1/8448,-1/4224)$. The two spring histories have their independent product law. Retain the tagged stationary-arm randomizations, blanks, quadrature outcomes, failures and zero cells as given in the cited complete record. Add separate labelled moving preparations with the same sector and quadrature sampling and conditional detector law; no mechanical history is assigned to a phase detection. [Full stationary example and probabilities](action_per_occupation_from_sector_masses.md)

The stationary phases are $(1/2,1,2)$ radians and $\mathcal I_0\cap\mathcal I_1=(1,2)$. Choose $J_0=2\log(2)M_*c^2T$ and $E(J)=M_*c^2(1+2^{J/J_0})$. This gives $z=1$ and the required slopes. With $\pi_P=2$ and $\lambda=1$, the observed moving advances are
$$
 (\psi_0,\psi_1,\psi_2)=\left(\frac1{2\sqrt2},\ \frac3{\sqrt{13}},\
                       \frac{10}{\sqrt{29}}\right).
$$
All six angles are on the specified positive branch. The measured $Y$ values are $(2,13/9,29/25)$, and (3) returns $R=125/32=f(2)$, with $A=1,B=4$. Since $f(1)=8$, this feasible record excludes the zero-offset identification.

Now relax only the equality of the boost magnitudes. For **any** $z'>-1$ and $\lambda'>\max_q r_q$, choose
$$
 \frac{P_q'}{M_0c}=(m_q+z')\sqrt{(\lambda'/r_q)^2-1}>0 .
$$
Every ratio (1) persists. In the example, simply shift the internal energy down by $M_*c^2$, so $z'=0$, and use $\lambda'=1$ with momenta in units of $M_*c$ equal to $(1,4/3,8/5)$. This reproduces all three moving advances and keeps the complete stationary data fixed. The two explanations are separated by independent registration of a common physical momentum. Equal velocities or equal control settings do not by themselves establish that registration.

## What the fit tests, and what still needs calibration

For a given sector the expansion at $p=0$ gives
$$
 H=C_{\rm out}+E_q+\frac{c^2p^2}{2E_q}+O(p^4),\qquad
 M_{{\rm kin},q}=[\partial_p^2H(qJ_0,0)]^{-1}
              =E_q/c^2=M_0(m_q+z).
$$
The spring gives $M_q=M_0m_q$ by a distinct experiment. Matching all three masses, or just their ratios with the stipulated common level differences, requires $z=0$ because the $m_q$ are distinct. This comparison depends on registering the sectors and momentum convention to the same carriers, as well as on the stationary level differences, the proposed dispersion and the common dwell ratio. If equality of the free kinetic Hessian masses with the spring masses is **imposed**, a feasible $z\ne0$ makes that combined model inconsistent. If equality is being **tested**, the same record measures a nonzero internal offset within the supplied dispersion. A fit with $z=0$ establishes consistency on these records. The earlier local boost-coefficient theorem uses its own generator and energy normalization and does not supply the all-momentum square root or fix the external energy origin here. [Conditional boost relation](conditional_boost_mass_relation.md)

All records here are exact conditional population laws. For bounded input errors, retain jointly feasible spring readings, phase probabilities, turn counts and shared calibration parameters; apply (1)–(3) to each common realization and project the resulting set. Zero offset is excluded only if that set is nonempty and contains no zero-offset realization. An empty set rejects the joint model. No error bands, drift law or finite-sample guarantee were supplied. Separate unknown sector gains, omitted failures, unknown phase zeros, or unregistered phase advances during acceleration would alter the inverse.

A physical use requires unchanged carrier preparation, stable phase references at both ends of each dwell, calibrated outcome gains and failure response, a fixed lab-time convention, and matched translational momentum without internal excitation. Failed preparations or unreadable events must be retained and accounted for by their registered channel. The ideal translational energy supplied per carrier at fixed sector is $M_0c^2[\sqrt{(m_q+z)^2+\pi_P^2}-(m_q+z)]$. Producing the boost, timing the dwell, restoring the momentum and phase references, operating the detectors and replenishing the store have additional unmeasured costs. The stationary work record does not measure those costs. The inverse supplies reference-unit ratios only. Dimensional momentum needs $M_0c$, dimensional dwell needs $T$, and dimensional action needs $M_0c^2T$ or the equivalent work and clock calibration. No absolute action, gravity calibration or DET derivation of Lorentz dispersion follows.
