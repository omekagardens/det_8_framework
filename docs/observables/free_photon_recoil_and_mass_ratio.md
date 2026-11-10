# The mass ratio from free photon absorption and emission

**DET Energy Research · Conditional inverse for one tagged transition**

Absorption and emission require different photon energies in the respective initial-carrier rest frames. Their ratio is exactly $M_e/M_g$. Two opposite photon directions per channel remove the unknown initial velocity, and a common positive meter gain cancels in the ratio. The additive meter zero must still be accounted for. For the four displayed readings $(4,12,6,7)$, the exact attainable range is
$$
  1<\frac{M_e}{M_g}\le
  \sqrt{1+\frac{3}{9+4\sqrt5}}.
$$

## 1. Recoil at the two vertices

Use four independent preparations of one species in flat $1+1$-dimensional spacetime. The same two tagged internal states have rest masses $M_e>M_g>0$. The two absorption preparations start in the ground state at the same finite lab rapidity $y_A$. The two emission preparations start in the excited state at another common finite rapidity $y_E$. The incident or outgoing photon direction $\sigma=+1,-1$ is registered against the same lab axis. The rapidities may have either sign and may differ between channels. Each event has one photon and one freely recoiling carrier. No other body exchanges energy or momentum at either vertex.

Use energy units for both components of a four-vector, so $P=(E,cp)$, $P^2=E^2-c^2p^2=M^2c^4$, and $k_\sigma=(h\nu,\sigma h\nu)$ is null. Here $\nu$ is positive cyclic frequency. In the initial carrier rest frame, absorption obeys $P'_e=P_g+k_\sigma$. Emission obeys $P'_g=P_e-k_\sigma$. Squaring and using the respective incoming $P=(Mc^2,0)$ gives the two rest-frame photon energies
$$
 \epsilon_A=h\nu_A^*=\frac{(M_e^2-M_g^2)c^2}{2M_g},\qquad
 \epsilon_E=h\nu_E^*=\frac{(M_e^2-M_g^2)c^2}{2M_e}.
$$
The absorption daughter carries momentum $+\sigma\epsilon_A/c$, and the emission daughter carries $-\sigma\epsilon_E/c$ in its parent's rest frame. Both final energies are positive. In particular $\epsilon_E<M_ec^2/2$. For $\Delta M=M_e-M_g>0$, the absorption energy is above $\Delta M c^2$ by $(\Delta M)^2c^2/(2M_g)$. The emission energy is below it by $(\Delta M)^2c^2/(2M_e)$. The common numerator cancels in the ratio, giving
$$
 R:=M_e/M_g=\epsilon_A/\epsilon_E>1 .
$$

For an incoming carrier with rapidity $y$, $P=Mc^2(\cosh y,\sinh y)$. The vertex invariant $P\cdot k_\sigma=Mc^2h\nu_{\rm lab}e^{-\sigma y}=Mc^2h\nu^*$ applies to either channel, using that channel's initial carrier. Thus the lab frequency is $\nu^* e^{\sigma y}$ in both. The two directions have opposite Doppler factors even though the initial carrier rapidity is the same within each pair.

## 2. Sharp inverse for the four displays

Let $a_+,a_-,e_+,e_-$ be the finite display values in the order absorption $+,-$, emission $+,-$. For $i=A,E$ the common affine display law is
$$
 x_{i,\sigma}=z+g\nu_i^*e^{\sigma y_i},\qquad g>0,\quad z\in\mathbb R.
$$
The directional signs label photon momenta. They do not attach a negative sign to any frequency. The display ordering within a pair is unrestricted because the carrier rapidity is unrestricted. For any preparation weights specified externally, the full law has a point reading at the stated value for each of these four labels. No relative occurrence rates or additional vertices are observed.

Let $x_{\min}=\min(a_+,a_-,e_+,e_-)$ and define
$$
 P_A(z)=(a_+-z)(a_--z),\quad P_E(z)=(e_+-z)(e_--z),\quad
 s=(a_++a_-)-(e_++e_-),\quad d=a_+a_--e_+e_- .
$$
Each of the four corrected readings must be strictly positive. Multiplying opposite directions within each pair then yields $P_i=(g\nu_i^*)^2$. The mass ordering requires $P_A>P_E$, and $P_A-P_E=d-sz$. The exact joint feasible set is
$$
 \boxed{\quad
 Z=\{z\in\mathbb R:z<x_{\min},\ d-sz>0\},\qquad
 (z,R)=\left(z,\sqrt{P_A(z)/P_E(z)}\right),\quad z\in Z .
 \quad}
$$
This compares products only after checking the four individual signs. Equality at $x_{\min}$ would give a zero photon frequency. Equality $P_A=P_E$ would give $R=1$, contrary to the tagged transition.

For $s>0$, $Z=(-\infty,\min(x_{\min},d/s))$. For $s<0$, $Z=(d/s,x_{\min})$ if $d/s<x_{\min}$, and is empty otherwise. For $s=0$, $Z=(-\infty,x_{\min})$ exactly when $d>0$, and is empty otherwise. These rules cover coincident readings without dividing by a vanishing difference. An equal pair of corrected readings simply gives zero rapidity for that channel.

**Attainability and nuisance parameters.** Choose any $z\in Z$ and any finite $g>0$. Put $D_i=\sqrt{P_i(z)}$ and take
$$
 \nu_i^*=D_i/g,\qquad
 y_A=\tfrac12\log\!\frac{a_+-z}{a_--z},\qquad
 y_E=\tfrac12\log\!\frac{e_+-z}{e_--z}.
$$
Both log arguments are finite and positive. Set
$$
 M_g=\frac{2hD_A}{gc^2(R^2-1)},\qquad M_e=R M_g .
$$
These masses give the stated absorption rest-frame photon energy. Dividing that energy by $R=D_A/D_E$ gives exactly $hD_E/g$ for emission. Boost the allowed rest-frame photon and daughter at each vertex by the corresponding initial rapidity. This yields positive-energy, on-shell daughters and reconstructs every individual lab frequency and display, including its direction and initial-state tag. Conversely, every admissible preparation satisfies these product, rapidity and mass equations. Thus any finite trial ratio $r>1$ is compatible exactly when the quadratic $P_A(z)-r^2P_E(z)=0$ has a real root in $Z$.

If $z$ is free and $Z$ is nonempty, it contains an open interval. A ratio constant at $r>1$ on that interval would require the polynomial identity $P_A=r^2P_E$. Comparing the leading coefficients of these monic quadratics gives $r=1$, which the model excludes. Hence the four records alone never identify a single mass ratio for a compatible record with an unrestricted zero.

## 3. Worked record and both endpoints

For $(a_+,a_-,e_+,e_-)=(4,12,6,7)$, positivity requires $z<4$, while $P_A-P_E=6-3z>0$ requires $z<2$. The latter is the full zero domain. Write $t=2-z>0$. Then
$$
 R^2=\frac{(t+2)(t+10)}{(t+4)(t+5)}
     =1+\frac{3t}{t^2+9t+20}
     =1+\frac{3}{9+t+20/t}.
$$
For $t>0$, $t+20/t\ge 2\sqrt{20}=4\sqrt5$, with equality only at $t=2\sqrt5$. The maximum mass ratio is attained at the finite admissible zero $z=2-2\sqrt5$. The ratio tends to one as $t\downarrow0$ and as $t\to\infty$. It exceeds one for every admissible $t$. Continuity between the maximizing point and either limit attains every intermediate value, and the preceding construction realizes it with all four displays. The upper endpoint is included and the lower one is excluded.

If an independent zero calibration for this same record gives $z=0$, it singles out $R=\sqrt{48/42}=\sqrt{8/7}$. Choosing zero by convention would discard other compatible masses. A calibrated zero outside $Z$ rejects the model for these readings.

## 4. What sets the dimensional mass scale

With an independently known compatible $z$, the geometric means $D_A,D_E$ identify $R$ and the within-channel ratios identify both rapidities. The means are still in display units. At fixed $h,c,z$, rescaling both masses and every true photon frequency by a common factor $\lambda>0$, while replacing $g$ by $g/\lambda$, leaves all four displays exactly fixed. Thus a zero calibration alone gives a dimensionless recoil reference and leaves the absolute masses and their dimensional difference undetermined.

Once the zero and the frequency unit are calibrated, $\nu_i^*=D_i/g$ is known in physical cyclic-frequency units. With the supplied physical photon conversion $h$ and speed $c$, the mass formulas above identify both absolute rest masses. One check on the energy scale is
$$
 (M_e-M_g)c^2=\frac{2\epsilon_A}{R+1}
              =\frac{2\epsilon_A\epsilon_E}{\epsilon_A+\epsilon_E}.
$$
Equivalently, a calibrated energy per corrected display unit $h/g$, together with the zero and $c$, is sufficient. A separate dimensionful gap on precisely this tagged transition could also anchor the scale through $M_g=\Delta M/(R-1)$ once $R$ is identified. The four-display contract supplies no such additional measurement.

The accepted store catalogue measures gaps with a free common mass offset and a separate orientation question. The spring study uses a different inertial attachment. Neither registers the present optical transition or calibrates its meter. The earlier two-body radiation ledger supplies a conservation comparison for specified initial masses. Here the two incoming internal states and the opposite-direction frequency records provide the inverse. The separate local boost-coefficient theorem does not supply the free relativistic mass shells or the photon energy scale used at these vertices. Collinear and anticollinear spectroscopy motivates the directional comparison. [König et al., arXiv:2007.03773v1](https://arxiv.org/abs/2007.03773v1)

A physical use would require reliable ground/excited preparation and species tags, registration of the same transition on fresh copies, a verified common initial rapidity within each directional pair (with bounded velocity spread in practice), and accurately collinear signed lab axes. The frequency timebase, common gain and zero must be stable across channels and acquisition times. A physical inference also needs evidence for free recoil, absence or accounted bounds on additional energy or momentum exchange, line shifts and broadening, and an uncertainty model for the four line readings and calibrations. Given the same preparations and calibrations, a conventional special-relativistic comparator produces this same inverse. It supplies no native photon dynamics, action unit or gravitational mass measurement.

## Scientific review

DET Energy Research derived the result. DET Relational State Research independently verified the recoil energies, directional cancellation, sharp interval, endpoints and physical calibration. The coordinator accepted the conditional result on 9 November 2026 HST.

- Control SHA-256: `f57ff9362713d4d9d0854a29209fb788a40ca6b2acc2060c624ea259937aa9c5`.
- Author report SHA-256: `31024c4e52f35bc7e852740487eb447bb119a1ba703bcda40ebf43cbd4e1f567`.
- Freeze SHA-256: `de72e62e0b0d4dd435db7654b9a8d45e4e36203b134c71b20499270b0490c68c`.
- Independent scientific review SHA-256: `6b09543b2386ed0a6b07c6b0a9bc6d226772b2d7b0dcef0c89354294ae395875`.
