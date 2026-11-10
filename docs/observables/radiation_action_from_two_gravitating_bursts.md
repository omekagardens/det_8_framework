# Can two gravitating bursts test a common radiation action?

Two bursts determine the positive actions of two tagged radiation channels in gravitational units if the spectral mixtures are linearly independent, the populations are absolutely registered, and the measured local energies admit a positive solution. The test of a common action is whether the two bursts give the same local energy times tick duration per unit of total spectral moment. An independent mixture makes this test decisive within the two-action model. Unknown separate band efficiencies can reverse the equality verdict while preserving every recorded quantity.

## From the four readings to energy at the outer sphere

Use the two preparations separately, at a common registered areal radius $R$ and outer radius $2R$. In each, let $x$ be retarded time in length units, $m(x)=GM_B(x)/c^2$ and $X_{i,f}=2m_{i,f}/R$. The pure outgoing spherical exterior has $ds^2=-f\,dx^2-2\,dx\,dr+r^2d\Omega^2$, $f=1-2m/r$, and geometrized $T_{xx}=-m'(x)/(4\pi r^2)$. The smooth nonincreasing mass is constant before and after the burst. This exterior convention is the only input from the collapsing-shell paper. [Mann, Nagle and Terno, v1](https://arxiv.org/pdf/1801.01981v1)

For each burst require four finite positive E81 readings. With $B=H_R/H_{2R}$ the local energy reading ratio and $C=D_i/D_f$ the ratio of displayed endpoint clock transfers, require $B>1$ and $0<C<1$. The E81 inverse is
$$
h=\operatorname{arccoth}(\sqrt2 B),\qquad
k=\tfrac12\operatorname{arsinh}\left(\sinh(2h)\frac{1-C}{1+C}\right),\qquad
h+k\le\operatorname{arsinh}1.
$$
Passing gives $X_i=1-\sinh^2(h-k)$ and $X_f=1-\sinh^2(h+k)$, with $0\le X_f<X_i<1$. These are the sharp E81 checks, including a zero final mass. Each positive gain is shared within its stipulated pair. The extra radar and occupation records cannot cure a failed four-reading check. [Accepted two-sphere inverse](radiated_mass_from_two_spheres.md)

At fixed $r$, $U=(f^{-1/2},0)$ and $s=(-f^{-1/2},\sqrt f)$ are the local future unit tangent and outward unit spatial normal. The measured outward flux is $-T(U,s)=-m'/(4\pi r^2 f)$ and the proper length of observer time is $c\,d\tau=\sqrt f\,dx$. Integration over the sphere and the full burst gives
$$
 E_r=\frac{c^4}{G}\int\frac{-m'}{\sqrt{1-2m/r}}\,dx
     =\frac{c^4r}{G}\big[\sqrt{1-2m_f/r}-\sqrt{1-2m_i/r}\big].
$$
For burst $b$ define the positive outer-sphere energy in units of $c^4R/G$ by
$$
 e_b=\frac{GE_{2R,b}}{c^4R}
 =2\big[\sqrt{1-X_{fb}/2}-\sqrt{1-X_{ib}/2}\big].
$$
The Bondi energy radiated to infinity is $E_{\infty,b}=c^4R(X_{ib}-X_{fb})/(2G)$. Its ratio to $E_{2R,b}$ is the mean of the initial and final outer lapse roots. The populations and frequencies below belong to the supported observer at $2R$, so the energy in their equation is $E_{2R,b}$. Adding the two local fluences would count the same emission twice.

## From the echo to the registered spectral tick

After the mass settles, an observer at $2R$ sends a radial test signal to $R$, where it is promptly reflected and returns to the original observer. In the final static geometry $c\,|dt|=|dr|/(1-2m_f/r)$ on either null leg. The outer observer's clock runs at $\sqrt{1-X_f/2}$ times the static coordinate rate. With $u=r/R$ the round-trip proper duration is
$$
 \Delta\tau_b=\frac{R}{c}\,D(X_{fb}),\quad
 D(X)=2\sqrt{1-X/2}\int_1^2\frac{u\,du}{u-X}
     =2\sqrt{1-X/2}\left[1+X\ln\frac{2-X}{1-X}\right].
$$
This gives $D(0)=2$ by direct substitution. The measured finite positive number of local ticks is $n_b=\Delta\tau_b/T_b$. Therefore $cT_b/R=D(X_{fb})/n_b$. This fixes the relevant tick ratio for each preparation even if its tick differs from the other preparation's. The echo's radar distance $c\Delta\tau_b/2$ includes the static propagation and outer clock factors. [Schwarzschild exterior, Eq. (14), English translation v1](https://arxiv.org/pdf/physics/9905030v1)

## The positive inverse

For channel $c=1,2$, use the complete moment $K_{bc}=\int_{\rm sphere,burst}\omega_{\rm loc}T_b\,dN_{bc}$. Here $\omega_{\rm loc}$ is the angular frequency of each population element in the outer local frame. Frequency drift and a time-dependent spectrum enter inside the integral. Each moment must be finite and nonnegative. A cycle-frequency record would first require conversion to angular frequency.

The proposed law is $E_{2R,b}=\sum_c J_cK_{bc}/T_b$, with fixed positive $J_c$ across preparations. In dimensionless units it gives
$$
 j_c=\frac{GJ_c}{c^3R^2},\qquad
 Y_b=\frac{GE_{2R,b}T_b}{c^3R^2}
     =e_b\frac{D(X_{fb})}{n_b}>0,\qquad
 K\begin{pmatrix}j_1\\j_2\end{pmatrix}
 =\begin{pmatrix}Y_1\\Y_2\end{pmatrix}.
$$
A zero row cannot supply a positive burst energy. For the remaining cases write $S_b=K_{b1}+K_{b2}>0$ and $\Delta=K_{11}K_{22}-K_{12}K_{21}$.

| Records | Positive two-action solutions | Common-action decision |
|---|---|---|
| $\Delta\ne0$ | The sole candidate is $j_1=(Y_1 K_{22}-K_{12}Y_2)/\Delta$, $j_2=(K_{11}Y_2-Y_1K_{21})/\Delta$. Both must be strictly positive. | For a positive solution, equality is forced exactly when $Y_1/S_1=Y_2/S_2$. Otherwise the records exclude equality and determine both unequal actions. |
| Two nonzero proportional rows, $K_{2c}=\rho K_{1c}$ | Require $Y_2=\rho Y_1$, where $\rho>0$. All positive points on $K_{11}j_1+K_{12}j_2=Y_1$ then fit. | The common choice $j_1=j_2=Y_1/S_1$ and unequal choices all fit. |
| A zero row, inconsistent proportional rows, or a nonpositive unique candidate | No strictly positive pair fits. This includes a rank-zero record. | The fixed positive two-action model itself fails on these inputs. |

In the proportional case with both columns active, $0<j_1<Y_1/K_{11}$ and $j_2=(Y_1-K_{11}j_1)/K_{12}$. With a missing column the observed action is fixed and the other can be any positive value. A single burst gives exactly this same one-row ambiguity. More generally, substituting $(j,j)$ directly proves the common-action test for every pair of nonzero rows. Each $Y_b/S_b$ is an occupation-moment-weighted average, so repeated mixture fractions cannot separate the two actions.

**Admissible independent mixtures.** Choose the same smooth nonincreasing Vaidya profile with $0\le X_f<X_i<1$ twice, the same stations and the same tick. For example, take the mass drop proportional to the cumulative integral of a smooth nonnegative pulse of unit integral. Identical macroscopic readings give $Y_1=Y_2=Y>0$. For $w>0$ set
$$
 K=w\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad j_1=j_2=j_*=\frac{Y}{3w}.
$$
Give the bands distinct positive local angular frequencies in geometric optics. At each time and angle split the spherical outward energy current in fractions $(2/3,1/3)$ in the first preparation and $(1/3,2/3)$ in the second. Divide each band current by its own $J_*\omega_{\rm loc}$ to obtain the matched population current, where $J_*=j_*c^3R^2/G$. The integrated moments are exactly the four displayed entries, the total stress history is unchanged, and $\Delta=3w^2>0$. This construction uses the stipulated continuum or ensemble-mean matching. An unequal-action example follows using the same energy splits with any fixed positive $J_1\ne J_2$ in the two population currents. This rescales the two columns by positive factors and preserves their independence. Thus both equality verdicts can occur for physical records under the stated premises.

## Unknown band efficiencies

Let $L_{bc}$ be the displayed moments. Suppose a fixed $\epsilon_c\in(0,1]$ multiplies the true population measure throughout band $c$ in both preparations, so $L_{bc}=\epsilon_c K_{bc}$. This assumes the factor applies to the frequency-weighted moment. A total count efficiency alone does not specify the weighting for spectrally selective losses. Put $a_c=j_c/\epsilon_c$. Replacing $K$ by $L$ in the positive inverse gives exactly all positive effective pairs $a$ from $La=Y$.

* **Separate unknown efficiencies.** For every such $a$, the true actions occupy $(0,a_1]\times(0,a_2]$, realized by $\epsilon_c=j_c/a_c$. Take the union over effective solutions when the rank is one. Any feasible record admits a common true action in $(0,\min(a_1,a_2)]$ for each effective solution and admits unequal true actions as well. Even a unique unequal effective pair leaves equality undecidable. An empty effective solution set stays empty.
* **One common unknown efficiency.** The possible true pairs are $\epsilon a$ for $0<\epsilon\le1$ over the same effective solution set. At full rank the action ratio $j_1/j_2=a_1/a_2$ is fixed. Equality or inequality is therefore decided as with absolute registration, although the common scale is unknown. In a feasible rank-one record, both common and unequal pairs survive.

For an exact full-rank witness, use the equal-action construction above as world A, with perfect registration so that $L=K$. In world B keep the total flux, both band energy currents, frequencies, geometry, ticks and detector displays fixed. Double the true band-one population at each frequency, time and angle, set $j_1'=j_*/2$, and use $\epsilon'_1=1/2$. Keep $j_2'=j_*$ and $\epsilon'_2=1$. Each true band energy is unchanged. Both displayed population measures, all four moments, the four E81 readings per burst and both radar counts agree exactly. One world has a common radiation action and the other has unequal radiation actions. The comparison covers the entire stipulated record in the continuum or matched-mean model.

## Absolute scale and connection to native actions

The observable $j_c$ is a squared gravitational length $GJ_c/c^3$ in units of $R^2$. Expressing $J_c$ in joule-seconds requires the dimensional action unit $c^3R^2/G$ or an equivalent absolute calibration, as well as the needed population registration. An absolute proper tick and the echo give $R=cT_b n_b/D(X_{fb})$. To see the scale freedom, multiply all radii, geometric masses, retarded lengths and proper times including ticks by $\lambda>0$. Divide local angular frequencies and the fluence display gain by $\lambda$, preserve the populations, and multiply each $J_c$ by $\lambda^2$. Energies acquire the factor $\lambda$. The four original readings, radar tick counts and spectral moments are unchanged. Within the supplied exterior the radiation inverse needs no fixture response factor $\kappa$.

For transfer to a scalar arm, register the burst's **areal** $R$ against the scalar length $\ell$. Then $j_c(R/\ell)^2=GJ_c/(c^3\ell^2)$ is the radiation result in the scalar length convention. Assigning this number to $J_s$ requires an independently supported action identification, or an independent scalar determination in the same units that can test the equality. In particular, with baseline mass $M_0$ and native scalar result $q_s=J_s/(M_0c\ell)$,
$$
 \frac{GJ_s}{c^3 R^2}
 =\frac{GM_0}{Rc^2}\,q_s\,\frac{\ell}{R}.
$$
If the exterior fixture supplies the mass conversion, its slope returns $\kappa GM_0/(R_{\rm fixture}c^2)$. One must register $R_{\rm fixture}/R$ and determine $\kappa$ or supply another independent mass conversion. Conversely, if the scalar and radiation actions are independently identified and $R/\ell$ is known, the radiation determination supplies $GJ_s/(c^3\ell^2)$ directly. [Exterior clocks and scalar gravity coupling](exterior_clocks_and_scalar_gravity_coupling.md)

For the native occupation arm with $q_o=J_{\rm occ}/(M_0c^2T_{\rm occ})$, the corresponding number is $(GM_0/(Rc^2))q_o(cT_{\rm occ}/R)$. Register the baseline mass and native tick against the same radius, or supply a calibrated physical link between channel quanta and native occupation changes. Such a link needs the complete energy and population accounting of the transition, including failed emissions, unobserved channels, recoil and spectator energy when present. A common action for two tagged radiation bands by itself leaves the native sector identification open. Independent admissible action sets in the same units can exclude equality if disjoint. Overlap must also respect any shared calibration or preparation constraints. [Comparing occupation and spatial actions](comparing_occupation_and_spatial_actions.md) · [Radiative readout of one occupation](radiative_readout_of_one_occupation.md)

The inference presupposes supported stations, complete angular and temporal coverage at $2R$, a settled exterior during the prompt echo, and a local tick shared between that echo and its burst's spectra. The two channels must exhaust the outward radiation. Registration must be nondepleting or use qualified reproducible preparations. Preparing and supporting the source, capturing the spectra, reflecting the signal and restoring the apparatus require physical resources. The records specify neither that work nor a universal action or a DET derivation of the assumed exterior. This is an exact identifiability result without empirical data.
