# Material mass from two principal-axis impulses

For the specified 2:1 prolate spheroid, two calibrated signed ratios of impulse to final velocity determine both the material mass $m$ and the displaced-fluid mass $D=\rho V$, whenever the records satisfy the strict inequalities below. The inference uses the difference in fluid kinetic energy between two directions of translation. The body’s material mass is the same in the two trials.

## Geometry and coefficient convention

Let $A=2a$ denote the long semiaxis and $a>0$ either transverse semiaxis. The dimensionless aspect ratio is $A/a=2$, the eccentricity is $e=\sqrt{1-a^2/A^2}=\sqrt{3}/2$, and the dimensional volume is $V=4\pi A a^2/3=8\pi a^3/3$. We use the supplied ellipsoid potential-flow law. Tuckerman’s three translational integrals at the surface have values $\alpha_i=2N_i$ in the control’s notation, so $k_i=\alpha_i/(2-\alpha_i)=N_i/(1-N_i)$. [L. B. Tuckerman, NACA Report 210, printed pp. 3–4 and §4 on p. 7](https://ntrs.nasa.gov/api/citations/19930091277/downloads/19930091277.pdf)

For $\Delta(s)=\sqrt{\prod_j(a_j^2+s)}$, differentiation gives $-2(1/\Delta)'=\Delta^{-1}\sum_j(a_j^2+s)^{-1}$. Summing the defining integrals thus gives $\sum_i N_i=Aa^2/\Delta(0)=1$. Every $N_i$ is positive. In the long-axis integral, substituting $t=A/\sqrt{A^2+s}$ gives
$$
 n=N_\parallel=(1-e^2)\int_0^1\frac{t^2\,dt}{1-e^2t^2}
 =\frac{1-e^2}{e^3}(\operatorname{atanh}e-e)
 =\frac{2\log(2+\sqrt3)}{3\sqrt3}-\frac13.
$$
Transverse symmetry gives $N_\perp=(1-n)/2$. The long-axis integrand has the larger denominator $A^2+s>a^2+s$ at every $s$, hence $0<n<N_\perp$. Since $N/(1-N)$ increases on $(0,1)$,
$$
 p=k_\parallel=\frac n{1-n}\simeq0.210,\qquad
 q=k_\perp=\frac{1-n}{1+n}\simeq0.704,\qquad 0<p<q .
$$
A sphere has three equal $N_i=1/3$ and all $k_i=1/2$. The sum rule normalizes the $N_i$.

## Response to each finite pulse

Reset the body and the unbounded homogeneous ideal fluid to rest before each trial. For translation along the registered principal direction $\mathbf e_i$, the exterior velocity is $\nabla\phi$ with $\nabla^2\phi=0$, $\partial_n\phi=U_i\,\mathbf e_i\!\cdot\mathbf n$ at the slip surface, and decaying velocity at infinity. Zero circulation and those boundary data fix the velocity. The unit-speed solution multiplied by $U_i(t)$ in coordinates relative to the translating centre gives the required field at each instant.

For either chosen axis the hull has two perpendicular mirror planes through that axis. For the proposed translation, each reflection preserves the exterior flow problem and its pressure (up to a spatial constant). The pressure force lies in both planes. The pressure torque about the centre, an axial vector, must be normal to each plane and therefore vanishes. The applied force passes through the mass centre. Pure axial motion from rest thus solves both the translational and rotational equations with zero angular velocity throughout. This argument only needs hull symmetry and a centred mass for the proposed motion, even if the body’s internal mass distribution has less symmetry.

In trial $i$ the body and fluid kinetic energies sum to $T_i=(m+Dk_i)U_i^2/2$. Spatial homogeneity makes the centre coordinate cyclic in the unforced kinetic energy. Its generalized momentum is $P_i=\partial T_i/\partial U_i=(m+Dk_i)U_i$, and the axial actuator force gives $\dot P_i=F_i(t)$. For a pulse of signed impulse $J_i=\int F_i\,dt$ starting from rest,
$$
         J_i=(m+Dk_i)\Delta U_i .
$$
The partition of generalized impulse is $m\Delta U_i+Dk_i\Delta U_i$. The second term is the fluid contribution from the spatially varying potential field. Its coefficient expresses how much fluid kinetic energy the translation induces. It does not identify a parcel of fluid moving rigidly with the spheroid.

## Exact data domain and inverse

Require finite, nonzero $J_i,\Delta U_i$ and matching signs within each trial ($J_i\Delta U_i>0$). The choices of positive axis may be reversed independently. Set $X=J_\parallel/\Delta U_\parallel$, $Y=J_\perp/\Delta U_\perp$. In addition to the signed checks the full compatibility condition is
$$
                    0<X<Y<(q/p)X .
$$
Indeed $X=m+pD$, $Y=m+qD$. Their difference is $(q-p)D$, and $qX-pY=(q-p)m$. Conversely these strict inequalities give the unique positive values
$$
 m=\frac{qX-pY}{q-p},\qquad D=\frac{Y-X}{q-p},\qquad
 \rho=\frac{Y-X}{V(q-p)} .
$$
Substitution returns both registered ratios. For any prescribed positive trial duration $\tau_i$, for example, apply the central pulse $F_i(t)=(2J_i/\tau_i)\sin^2(\pi t/\tau_i)$ on $0\le t\le\tau_i$ and zero outside. The integrated equation gives each prescribed signed end velocity, starting from the independent quiescent states. This constructs a realization on the entire stated domain.

At $Y=X>0$ the solution would have $D=0$. At $Y=(q/p)X>0$ it would have $m=0$. The common origin of the closed cone sets both to zero. These boundaries are excluded. Data beyond either ray with $X>0$ force a negative parameter. A nonzero impulse with zero end velocity or reversed sign cannot be realized, and any zero impulse, including a zero-impulse/zero-velocity pair, violates the pulse preparation.

## Reduced records and scales

With just a valid long-axis ratio $X$, the full positive family is $0<m<X,\ \rho=(X-m)/(pV)$. For example the pairs $(m,\rho)=(X/2,X/(2pV))$ and $(X/4,3X/(4pV))$ give the same signed speed under the same impulse. For a separate equal-volume sphere with its own unknown parameters, require the same nonzero signed checks and equality of all observed directional ratios to one $S>0$. Its full family is $0<m<S,\ \rho=2(S-m)/V$. Each member realizes every such reading since the sphere has effective inertia $S$ in all directions.

For an unknown positive common impulse gain, define the physical impulses by $J_i=g\,j_i$ for recorded values $j_i$. Write $x=j_\parallel/\Delta U_\parallel$ and $y=j_\perp/\Delta U_\perp$. The same signed and strict cone tests apply to $j_i,x,y$ because $X=gx,\ Y=gy$. With $r=y/x$ the dimensionless material-to-displaced-fluid mass ratio is
$$
    h=\frac{m}{\rho V}=\frac{q-pr}{r-1},\qquad 1<r<q/p .
$$
For instance the material fraction of either measured effective inertia is $m/(m+Dk_i)=h/(h+k_i)$. Absolute $m$ and $\rho$ still scale with $g$. Every solution is obtained by varying $g>0$ in the two-ratio inverse, equivalently $(m,\rho,g)\mapsto(\lambda m,\lambda\rho,\lambda g)$ for $\lambda>0$ at fixed known $V$. Conversely, when impulses and velocities are absolutely calibrated but only the aspect ratio is known, $p,q,m,D$ are determined. Any chosen length scale $a\mapsto c a$ gives $V\mapsto c^3 V,\ \rho\mapsto\rho/c^3$ for the same two readings. Recovering dimensional density requires a volume scale.

## Work and scope

Over either pulse, $\int F_i U_i\,dt=\int(m+Dk_i)U_i\dot U_i\,dt$. The work supplied from rest is
$$
 W_i=\tfrac12 J_i\Delta U_i
    =\tfrac12 m(\Delta U_i)^2+\tfrac12 Dk_i(\Delta U_i)^2>0 .
$$
Both terms are reversible kinetic energy in the specified dynamics. Deceleration along the same line to rest would return this work and restore the quiescent field. The ideal slip flow dissipates no energy, and the material mass is constant. This calculation uses only the two finite pulse endpoints for inference.

Each $J_i/\Delta U_i$ has units of mass, $D/V$ has units of density and $k_i,h,r$ are dimensionless. These are conditional classical results under supplied geometry, continuum dynamics and calibrations. CL083/v1 treated total inertial mass through internal motion and CL089/v1 treated driven boundary inertance. Both serve as scope comparators. The present independent directional response is induced by external fluid motion. No empirical measurement, gravitational correspondence or native DET unit is asserted.

## Transfer to free recoil and gravity

The calibrated two-axis inverse supplies the material mass within the ideal fluid experiment. Using it as the rest mass of a free recoil carrier requires the same body and internal state, an independently registered mass scale, and evidence that removal from the fluid preserves the relevant material system. The directional added mass counts kinetic energy carried by the external fluid. Measuring a response to gravity requires a separate gravitational record and a law connecting that response to the body or fixture. The [driven boundary inertance](signed_boundary_inertance_from_seven_forces.md) describes a frequency-dependent response of an internally moving network.
