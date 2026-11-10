# Do matched hydrostatic spheres cross the same radius?

The material surface first reaches $3R_0/5$ at $4/(5\Omega)$ for $\gamma=4/3$. For $\gamma=5/3$ it stays at or above $2R_0/3$ throughout the observation. The two spheres share the same gravitational law, initial pressure support and imposed velocity.

## Local balance and the free surface

Let $x$ label the initial radius of a shell, let $r=bx$ be its current radius, and take outward acceleration as positive. Write $\Omega^2=GM/R_0^3=4\pi G\rho_0/3$. With $m(x)=M(x/R_0)^3$, integration of $P'_0(x)=-\rho_0\Omega^2 x$ from the zero-pressure surface gives

$$
 P_0(x)=\tfrac12\rho_0\Omega^2(R_0^2-x^2).
$$

The pressure is positive inside and has zero gradient at the center. The volume map has Jacobian $b^3$ for $b>0$. Thus $dm=4\pi\rho_0 x^2dx$ remains fixed, $\rho=\rho_0 b^{-3}$ inside, and $u=\dot b x$. The shell retains $K_\gamma(x)=P_0(x)/\rho_0^\gamma$, giving $P=P_0(x)b^{-3\gamma}$. Taking $\partial_r=b^{-1}\partial_x$ at fixed time yields the outward pressure and inward gravitational accelerations at each interior shell,

$$
 a_P=-\rho^{-1}\partial_r P=\Omega^2 x b^{2-3\gamma},
 \qquad a_g=-Gm(x)/(bx)^2=-\Omega^2 x b^{-2}.
$$

The shell acceleration is $\ddot b x$, so all $x>0$ obey the same scale equation

$$
 \ddot b=\Omega^2(b^{2-3\gamma}-b^{-2}).
$$

Both accelerations and the velocity vanish linearly at the center. In Cartesian coordinates their vectors are scalar multiples of the position vector, and pressure is quadratic in radius. The force and symmetry extend regularly to $x=0$. At $R(t)=bR_0$, the boundary velocity is $\dot R=u(R^-,t)$ and $P(R^-,t)=P(R^+,t)=0$. The moving surface therefore has zero relative mass flux and zero pressure traction despite the jump from $\rho_0/b^3$ to vacuum. Its material acceleration is the interior limit $R_0\ddot b$. The interior field $-\Omega^2r/b^3$ has spherical divergence $-4\pi G\rho$ and joins the exterior field $-GM/r^2$ continuously at $R$. There is no surface mass sheet or central point source.

With $b=1,\dot b=0$, the scale equation gives the stationary solution in each world. Its right-hand side is smooth for $b>0$, so these initial data select this solution within the supplied family. Immediately after the ideal kick, both have $R=R_0,\rho=\rho_0,P=P_0(x),u=-\Omega x/2$, and $g_{\rm ext}=-GM/r^2$. The right-hand material acceleration is zero throughout, including the surface. In particular, inward surface velocity at release coexists with zero initial surface acceleration. The listed instantaneous observations coincide.

## Dimensional energy balance

Use $I=\int x^2\,dm=3MR_0^2/5$, the radial second moment of the initial mass, and $A=I\Omega^2=3GM^2/(5R_0)>0$. The kinetic and gravitational energies at scale $b$ are

$$
 K=\tfrac12 I\dot b^2,\qquad
 W=-\int_0^{R_0}\frac{Gm(x)}{bx}\,dm=-\frac{A}{b}.
$$

The gravitational integral counts the interaction of each added shell with its enclosed mass once and tends to zero at infinite dispersal. Integrating the common hydrostatic pressure gives $\int P_0\,dV_0=4\pi\rho_0\Omega^2 R_0^5/15=A/3$. With the specified internal energy density, set $q=3(\gamma-1)$. Then

$$
 U=\frac{\int P_0\,dV_0}{\gamma-1}b^{3-3\gamma}
   =\frac{A}{q b^q},\qquad
 E=\tfrac12 I\dot b^2+\frac{A}{q b^q}-\frac{A}{b}.
$$

Here $b,q$ are dimensionless, $\dot b$ has units of inverse time, and both $I\dot b^2$ and $A$ have units of mass times length squared per time squared. The initial pressure has units $\rho_0\Omega^2R_0^2$, and $P\,dV$ has units of energy. Differentiating gives $\dot E=I\dot b[\ddot b-\Omega^2(b^{-q-1}-b^{-2})]=0$ by the pointwise equation, including at a turning point by continuity. Each isolated postkick flow conserves its own energy. The impulse adds the same kinetic energy $A/8$ to each initially stationary sphere.

| Material law | $U(b)$ | $W(b)$ | $E$ before kick | $E$ after kick |
|---|---:|---:|---:|---:|
| $\gamma=4/3$ | $A/b$ | $-A/b$ | $0$ | $A/8$ |
| $\gamma=5/3$ | $A/(2b^2)$ | $-A/b$ | $-A/2$ | $-3A/8$ |

Thus the same $P_0$ corresponds initially to energy densities $3P_0$ and $3P_0/2$ respectively. The initial matched observations omit internal energy. The impulse acts only on velocity, and its apparatus is outside the balance.

## Finite crossing record

Set $\tau=\Omega t$ and denote $db/d\tau$ by $b'$. Both solutions start at $b=1,\ b'=-1/2$. The observation ends at $\tau=1$.

For $\gamma=4/3$, the two forces cancel for every $b>0$. Thus $b''=0$ and $b=1-\tau/2$. Monotonicity makes $\tau=4/5$ the first time $b=3/5$. The bit is **1**. Throughout the full horizon $b\ge 1/2$, so the material map stays regular and ordered.

For $\gamma=5/3$, $b''=b^{-3}-b^{-2}=(1-b)/b^3$, positive under compression. Its energy integral in units of $A$ reads

$$
 \tfrac12(b')^2+\tfrac{1}{2b^2}-\tfrac1b=-\tfrac38,
 \qquad (b')^2+(1/b-1)^2=\tfrac14.
$$

Consequently $2/3\le b\le2$ and $|b'|\le1/2$ on every interval of existence. These compact bounds lie strictly inside the smooth phase domain $b>0$, so continuation of the ordinary differential equation covers the whole horizon. Since $\partial r/\partial x=b>0$, shells remain ordered. The lower bound exceeds $3/5$, giving bit **0**.

The finite event identifies the exponent under the stated two-candidate choice, with known $M,R_0,G$, the specified adiabatic pressure response, exact impulse and calibrated readout. An unrestricted material law or flow would require additional constitutive assumptions or observations. The construction concerns this homologous domain and finite time. General fluid stability, empirical stellar identification, and derivations of the supplied mass and gravitational calibration lie outside the result.

The selected input dispositions CL018, CL024 and CL068 concern local gravitational density inference, radial force response, and gravitational binding respectively. The equilibrium, shell balance and finite records here follow directly from the specified model. The published background gives the inviscid mass, momentum and Poisson equations and transports a shell-dependent pressure coefficient. Its stellar solutions and mode calculations were unnecessary for this calculation. [Cao and Lou (2009), §2, equations (1)–(4), arXiv:0908.3225v1](https://arxiv.org/pdf/0908.3225v1).

## What a DET source record must retain

If both preparations map to the same summary $S$, a predictor using only $S$ and the registered kick must assign one crossing probability to that input. Agreement with the two complete, preparation-conditional predictions would require that probability to equal both 1 and 0. Averaging over preparations would answer a different question. A correspondence covering both must retain a distinction in the live source state or in its transition law that carries the material response through compression. A model restricted in advance to one material can state that restriction explicitly. The two-world result does not select any particular DET variable as the carrier of this distinction.

To apply the benchmark to DET, QR would need to register the two preparations, map native source quantities to shell mass, radius, pressure and velocity, and justify the common kick and subsequent material response. The source uses Newtonian inviscid Euler–Poisson dynamics in vacuum, homologous spherical flow, a shell-advected adiabatic law with the stated energy convention, and isolated evolution after the impulse. The observation map must follow the same material surface, calibrate the radius threshold, identify release and supply a clock covering the whole interval through $1/\Omega$. The mass, length, time and gravitational coupling that set this scale are physical inputs. The native mapping note sets out correspondence obligations, and the exterior-clock result concerns a different static observable. Neither establishes these material or observation maps.

The Classical lane supplied the two-fluid calculation and its independent scientific review. QR accepted the source-record test for the two specified preparations. [Native mapping requirements](../coordination/NATIVE_MASS_MAPPING.md)

## Scientific provenance

- Classical CL074/v1 author SHA-256 bf02690934818c73388a09dd91c492fe206b01df85a48d3871b77334b45f1750.
- Independent Classical review SHA-256 02b19ac531d00887e37989ba7fad3d6fff125185649b21de457097a37fca71f9.
- Independent QR recipient review SHA-256 4dcd61969207c96d080441cd6530c6ab5c6446aa47b12dd87fbc6be9dbc8dcba.
