# Comparing the passive gravitational response of a solid and its fluid

Two signed support loads at distinct, independently registered fluid densities determine the ratio of the solid and fluid passive responses per unit inertial mass in an inertial laboratory. The force gain, impulse gains and field strength can all be unknown. In a uniformly accelerating laboratory the same two loads still decide equality and ordering. The decisive observable is the inferred support at the density for which the displaced fluid and solid have equal inertial mass.

## The inertial masses entering the buoyancy measurement

Let $m>0$ and $V>0$ be the material inertial mass and external volume of one rigid 2:1 prolate spheroid. In fill $j=1,2$, let $\rho_j$ be the inertial fluid density and $d_j=\rho_j V/m$. The accepted CL093 benchmark uses a separate fresh, quiescent ideal-fluid preparation for each axial impulse. The effective inertias are $m+p\rho_j V$ longitudinally and $m+q\rho_j V$ transversely, with known shape factors $0<p<q$. These coefficients describe the kinetic energy of induced flow. [Two-axis material mass benchmark](material_mass_from_two_immersed_impulses.md) · [Tuckerman, NACA Report 210, §4](https://ntrs.nasa.gov/api/citations/19930091277/downloads/19930091277.pdf)

For each fill form $x_j$ and $y_j$ from the displayed signed longitudinal and transverse impulses divided by their respective calibrated velocity changes. Each impulse and velocity change must be finite, nonzero and of matching sign within its trial. The strict donor domain is $0<x_j<y_j<(q/p)x_j$. Since a single positive impulse gain applies within that fill, $r_j=y_j/x_j$ gives
$$
 d_j=\frac{r_j-1}{q-pr_j}>0 .
$$
The two fills can have different impulse gains. Indeed, with physical impulse equal to $g_j$ times displayed impulse, any chosen common $m>0$ gives $g_j=m(q-p)/(q x_j-p y_j)>0$ and $\rho_j V=m d_j$, reproducing both impulse responses per fill. Require $d_1\ne d_2$. Transfer each $\rho_j$ and the same solid volume and material state to the finite hydrostatic bath. The two directional effective inertias have served their purpose once $d_j$ is known.

## Hydrostatic pressure and signed support

Let $\alpha_s,\alpha_f>0$ denote passive gravitational mass divided by inertial mass for the solid and fluid, respectively. One $\alpha_f$ applies to both homogeneous fills of the same composition. Let $z$ increase upward and write the uniform prescribed field as $-g\hat{\mathbf z}$ with $g>0$. In the inertial lab, static force balance on a fluid element gives $\partial_z P_j=-\rho_j\alpha_f g$. On the submerged solid the pressure traction is $-P_j\mathbf n$ for outward solid normal $\mathbf n$. Extending the surrounding hydrostatic pressure field across the excluded volume gives
$$
 \mathbf F_{{\rm pressure},j}
 =-\int_{\partial V}P_j\mathbf n\,dA
 =-\int_V \nabla P_j\,dV
 =\rho_j V\alpha_f g\,\hat{\mathbf z}.
$$
A constant pressure contributes zero net force. Balancing this upward pressure force and the downward solid weight gives the required signed **upward** force of the support on the body,
$$
 S_j=mg(\alpha_s-d_j\alpha_f).
$$
A negative $S_j$ requires a downward hold. At $S_j=0$ the solid is neutrally supported. There is no relative fluid motion in this equilibrium.

Take two physical orientations of the signed cell, holding the body, fill, field, depth and physical load fixed. Choose the positive orientation to display an upward support with positive signed response. For four finite real displays the model is
$$
 W_{j,+}=z_j^{\,0}+k S_j,\qquad W_{j,-}=z_j^{\,0}-k S_j,\qquad k>0.
$$
The same display-per-force gain $k$ applies across both fills and both orientations. The zero is stable within each reversal pair. Its midpoint $z_j^{\,0}=(W_{j,+}+W_{j,-})/2$ is determined separately for each fill. The half-difference $Q_j=(W_{j,+}-W_{j,-})/2=k S_j$ preserves support direction. Equal displays within a pair are admissible and give a genuine zero support on these premises.

## Sharp inverse in the inertial lab

Fit the two points to $Q(d)=A-Bd$. Distinct $d_1,d_2$ give
$$
 B=\frac{Q_1-Q_2}{d_2-d_1},\qquad
 A=\frac{d_2Q_1-d_1Q_2}{d_2-d_1}. \tag{1}
$$
The inertial model requires $A=kmg\,\alpha_s>0$ and $B=kmg\,\alpha_f>0$. These two strict checks, the donor checks and the stated registrations suffice. Given any compatible $m>0$ and finite $k,g>0$, choose $\alpha_s=A/(kmg)$ and $\alpha_f=B/(kmg)$. Use the midpoint zeros, choose the registered fill densities and choose an additive pressure constant compatible with a filled finite bath. The pressure balances then reproduce **all four** raw support readings. A zero or negative fitted coefficient excludes the assumed positive inertial-lab model even though an individual support can have either sign.

The solid-to-fluid coefficient ratio is $\eta=\alpha_s/\alpha_f=A/B$. The passive mass of the solid divided by that of the displaced fluid in fill $j$ is $\eta/d_j$. Support changes sign at $d=\eta$. On the admissible domain the two materials share a coefficient exactly when
$$
 Q(1)=A-B=\frac{(d_2-1)Q_1+(1-d_1)Q_2}{d_2-d_1}=0. \tag{2}
$$
The sign of $Q(1)$ gives the ordering. Neither fill has to attain $d=1$. In the exact model the two-point interpolation or extrapolation evaluates the same force law there.

With **one inertial-lab fill** at $d>0$, write $Q=B(\eta-d)$ with unknown $B>0$. The exact feasible sets for $\eta$ are $(d,\infty)$ when $Q>0$, $(0,d)$ when $Q<0$, and $\{d\}$ when $Q=0$. For a nonzero reading take $B=Q/(\eta-d)$ for any ratio on the indicated side. For a zero reading any $B>0$ works. Thus one signed reading can exclude equality if its feasible set omits 1. A neutral reading fixes the ratio and establishes equality exactly when $d=1$.

## Unknown common acceleration of the bath

Let $a$ denote the signed component of lab acceleration in the downward field direction. The lab translates without rotation and each bath has re-equilibrated. The inertial force per unit inertial mass is now upward $a\hat{\mathbf z}$. Hydrostatic balance gives $\partial_z P_j=-\rho_j(g\alpha_f-a)$. Integrating the traction yields the signed upward pressure force $\rho_j V(g\alpha_f-a)$. Balancing the solid in the lab gives
$$
 S_j=m\big[(g\alpha_s-a)-d_j(g\alpha_f-a)\big].
$$
The coefficients returned by (1) now obey
$$
 A=C\alpha_s-t,\qquad B=C\alpha_f-t,\qquad C=kmg>0,\quad t=kma . \tag{3}
$$
For any finite fitted $A,B$ the complete equivalence class consists of
$$
 C>0,\qquad t>\max(-A,-B),\qquad
 \alpha_s=(A+t)/C,\quad \alpha_f=(B+t)/C,\quad a/g=t/C . \tag{4}
$$
If the acceleration is restricted to point downward, impose that sign on $t$ as well. Necessity follows from positivity of both passive coefficients. Conversely, take any allowed $C,t$, choose $m,g,k>0$ realizing $C$, and set $a=gt/C$. The signed hydrostatic pressure gradient, support and both reversal midpoints reconstruct every reading. A finite bath admits a positive reference pressure throughout the occupied region for either sign of the gradient under the stipulated containment and immersion. Thus the inertial-lab checks $A,B>0$ cannot be imposed on the *effective* coefficients in (3).

The common acceleration cancels from $A-B=C(\alpha_s-\alpha_f)$. Equation (2) still gives an exact equality and ordering test, including when $A=B=0$. The true ratio is $(A+t)/(B+t)$. Its magnitude for unequal coefficients depends on the unknown translation $t$ in display units. For unrestricted signed $a$ the sharp ratio sets are $(1,\infty)$ if $A>B$, $(0,1)$ if $A<B$, and $\{1\}$ if $A=B$, by varying $t$ in (4). An independent value of $kma$ would restore the ratio. Neutral support in a single accelerated fill equates the two *effective* weights; at $d=1$ it still tests equality of the intrinsic coefficients directly.

**One record, two physical interpretations.** In consistent units set $m=V=g=k=1$, $d_1=1/2$, $d_2=2$. For the accepted shape factors take unit impulse gains, unit positive velocity changes, and displayed axial impulses $(1+p d_j,1+q d_j)$ in each fill. These are in the strict CL093 domain. In an inertial lab choose $(\alpha_s,\alpha_f)=(3,2)$. Signed supports are $S_1=2$, $S_2=-1$. With cell zeros $5,7$ the four displays in $(+,-)$ order are $(7,3)$ and $(6,8)$. They give $A=3,B=2$ and $Q(1)=1$. In a second lab let $a=1$ downward and $(\alpha_s,\alpha_f)=(4,3)$ with all inertial preparations and calibrations fixed. Both effective weights per unit inertial mass and both pressure gradients are unchanged across the two worlds. All recorded impulses, velocities and support readings agree. The intrinsic ratios are $3/2$ and $4/3$, while the solid has the larger coefficient in both. A bidirectional support supplies the downward force in the denser fill.

## Calibration and physical limits

The unknown impulse scale leaves $m$ and each displaced inertial mass $m d_j$ undetermined in kilograms. One absolute impulse-to-velocity calibration or an independent mass anchor fixes them; dimensional fluid density also requires a volume scale or equivalent calibration. In the inertial lab the solid passive mass is $A/(kg)$ and the displaced passive masses are $d_j B/(kg)$. The product of the force gain and field strength therefore suffices to set their scale. The individual passive-to-inertial coefficients require $kmg$ or an equivalent normalization. In the accelerating lab the corresponding numerators are $A+t$ and $d_j(B+t)$. A known field strength alone does not register that acceleration correction.

This comparison requires independent transfer of the material state, solid volume and both fill densities from the ideal, effectively unbounded impulse experiments to fully submerged static equilibria in the finite baths. The displaced fluid must remain homogeneous, the support must transmit both signs without an unaccounted mount buoyancy, and gravity gradients, self-gravity, interface crossings and pressure-induced solid deformation are outside the model. The sensor must actually reverse its response at fixed load with a stable pair zero and common gain. A sign change applied afterward to the same display cannot remove its physical zero.

A stationary support has zero displacement relative to the bath. Its force samples give no integrated work for filling, accelerating, settling, mounting, reversing, reading or restoring the apparatus. Absolute work would require a force–displacement or energy-store record with the relevant boundaries and calibrations. The benchmark and pressure balance test passive gravitational response only for these two registered materials and the supplied Newtonian laws. They supply neither an active source mass nor empirical evidence for universal equality. [Signed lifting work and passive mass](signed_lift_work_and_passive_mass.md)
