# Mass balance in a finite expanding region

Conditional result under supplied general relativity

For the one registered radiation FLRW solution, the geometrically defined Misner–Sharp energy and independently integrated Kodama slice charge coincide. Over the prescribed comoving ball they decrease from
$$
 E_0=\frac{c^5t_0}{64G}\quad\hbox{to}\quad E_1=\frac{E_0}{2}.
$$
The full four-dimensional Kodama current is divergence-free, but its outward flux through the comoving worldtube is $F_K=E_0/2$. The finite pressure-work integral also equals $E_0/2$, while the outward energy flux measured in the fluid frame is zero. Thus
$$
 Q_K(4t_0)-Q_K(t_0)+F_K=0,
 \qquad E_1-E_0=-\int_{t_0}^{4t_0}p\,\dot V\,dt.
$$
Current conservation does not assert zero flux through this boundary. This is a finite conventional GR balance with a specified region, current and normalization, not a changing total invariant mass of an isolated system.

## 1. Premises, units and observation

Supply positive conventional G,c,t0, signature (−+++), x⁰=ct, a dimensionless scale factor a, and a length coordinate χ. The complete prescribed spacetime history on the slab is
$$
 ds^2=-(dx^0)^2+a(t)^2(d\chi^2+\chi^2d\Omega^2),
 \qquad a(t)=\sqrt{t/t_0},\qquad t\in[t_0,4t_0].
$$
The region is exactly $0\leq\chi\leq\chi_0=ct_0/2$. Its side is the mathematical worldtube χ=χ0 in a homogeneous fluid that continues on both sides. There is no wall, vacuum matching, reflector, material shell, particle-number prescription or additional reservoir. Cosmic t is proper time along comoving observers. No empirical records are supplied.

Einstein's equation is $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, with Λ=0. The stress takes the supplied ideal-fluid form once its coefficients have been obtained from the metric:
$$
 T^{\mu\nu}=(u+p)U^\mu U^\nu+p g^{\mu\nu},
 \qquad U^\mu=(1,0,0,0),\qquad U\cdot U=-1.
$$
Here u is energy per proper volume, p has the same units, and U is dimensionless in x⁰ coordinates. Dots below mean d/dt and primes in the curvature calculation mean ∂/∂x⁰. Set H=$\dot a/a$=1/(2t).

The finite observation consists of two exact mathematical slice records at t0 and 4t0, together with the integrated oriented side flux and the integrated pressure-work term over that same slab. The calculation must distinguish these records from a global mass, rest-particle inventory or an experimental acquisition protocol. All dimensional scales are supplied; $c^3t_0/G$ is not a derived native mass standard.

## 2. Metric source and local conservation

The source can be derived in nonsingular comoving Cartesian spatial coordinates $X^i$, where χ²=δijXiXj and $g_{ij}=a^2\delta_{ij}$. This also avoids treating the polar coordinate singularity at χ=0 as physical. Use the curvature convention
$$
 R_{\mu\nu}=\partial_\lambda\Gamma^\lambda_{\mu\nu}
 -\partial_\nu\Gamma^\lambda_{\mu\lambda}
 +\Gamma^\lambda_{\lambda\rho}\Gamma^\rho_{\mu\nu}
 -\Gamma^\lambda_{\nu\rho}\Gamma^\rho_{\mu\lambda}.
$$
The only nonzero Cartesian Christoffel classes are
$$
 \Gamma^0_{ij}=a a'\delta_{ij},\qquad
 \Gamma^i_{0j}=\Gamma^i_{j0}=\frac{a'}a\delta^i_j.
$$
Their contractions give
$$
 R_{00}=-3\frac{a''}a,\quad
 R_{ij}=(a a''+2a'^2)\delta_{ij},\quad
 \mathcal R=6\left(\frac{a''}a+\frac{a'^2}{a^2}\right),
$$
with off-diagonal entries zero. In this fixture
$$
 \frac{a'}a=\frac1{2ct},\qquad
 \frac{a''}a=-\frac1{4c^2t^2},\qquad \mathcal R=0,
$$
so
$$
 G_{00}=\frac3{4c^2t^2},\qquad
 G_{ij}=\frac{a^2}{4c^2t^2}\delta_{ij}.
$$
In polar coordinates the spatial diagonal is the same coefficient times $(1,\chi^2,\chi^2\sin^2\theta)$. Einstein's equation therefore yields exactly
$$
 u(t)=\frac{3c^2}{32\pi Gt^2},\qquad
 p(t)=\frac{c^2}{32\pi Gt^2}=\frac{u(t)}3,\qquad
 T^\mu{}_{\nu}=\operatorname{diag}(-u,p,p,p).\tag{1}
$$
Thus radiation form and normalization have been checked from the metric, rather than inserted as an unchecked Friedmann density. There is no new microscopic radiation model. Positive u and p=u/3 imply u≥|p| and u+p>0; the ideal-fluid stress satisfies the dominant and null energy conditions on the complete slab.

The time component of covariant stress conservation reduces to
$$
 \dot u+3H(u+p)=0.\tag{2}
$$
Directly, $\dot u=-2u/t=-4Hu$, while $3H(u+p)=4Hu$. Spatial conservation follows from homogeneous p and the zero comoving acceleration: $\Gamma^\mu_{00}=0$. Equivalently the Cartesian mixed time divergence is $-[\dot u+3H(u+p)]/c$, with spatial divergences zero. No arbitrary-vector current conservation has been inferred from (2).

Since t≥t0>0, a, its derivatives, the metric and inverse metric are smooth and finite in Cartesian coordinates throughout the ball. The centre is regular. The curvature is not claimed to vanish: $\mathcal R=0$ is the radiation trace condition, while the Ricci tensor above is nonzero. The t=0 singular regime is outside the declared domain.

## 3. Region, areal geometry and time registration

The areal radius is R=aχ. On the orbit space $(x^0,\chi)$, $h_{ab}=\operatorname{diag}(-1,a^2)$, and
$$
 \partial_0R=\frac{HR}{c},\quad \partial_\chi R=a,
 \quad D:=h^{ab}\partial_aR\partial_bR
 =1-\left(\frac{HR}{c}\right)^2.\tag{3}
$$
Let z=t/t0∈[1,4]. At the side,
$$
 R_b(t)=\frac{ct_0}{2}\sqrt z,\qquad
 \frac{HR_b}{c}=\frac1{4\sqrt z}.
$$
Every interior sphere has a smaller value of HR/c, hence D≥15/16>0 on all nonzero symmetry spheres in the slab. The regular central limit is D→1. The region is untrapped; there is no horizon crossing or marginal endpoint.

The induced side metric is
$$
 ds^2_{\rm side}=-(dx^0)^2+R_b^2d\Omega^2,
$$
so the side is timelike. A comoving worldline at fixed χ,θ,φ has dτ=dt, making the endpoint time registration explicit. The future unit slice normal is
$$
 n^\mu=U^\mu=(1,0,0,0),\qquad n_\mu=(-1,0,0,0).
$$
The proper spatial volume element is
$$
 dV_{\rm proper}=a^3\chi^2\sin\theta\,d\chi\,d\theta\,d\phi.
$$
Consequently the volume of each ball equals $V=4\pi a^3\chi_0^3/3=4\pi R_b^3/3$. Equality between areal and proper-slice volume is a property of this spatially flat fixture, not a statement about every spherical spacetime.

## 4. Geometric energy and the explicitly normalized current

First compute the geometric energy independently of any current integral. Substituting (3) into its supplied definition gives
$$
 E_{\rm MS}(t,\chi)
 =\frac{c^4R}{2G}(1-D)
 =\frac{c^2H^2R^3}{2G}
 =\frac{c^2R^3}{8Gt^2}.\tag{4}
$$
Its small-sphere behavior is E=O(R³), with a regular radial limit at the centre. This is not an additional claim that the sphere-assigned energy is a smooth Cartesian scalar at the origin. The defined mass is $M_{\rm MS}=E_{\rm MS}/c^2$, with mass units.

Next apply the fixed orbit-space orientation $\epsilon^{0\chi}=1/a$. The Kodama field is
$$
 K^a=\epsilon^{ab}\partial_bR,
 \qquad K^\mu=\left(1,-\frac{H\chi}{c},0,0\right).\tag{5}
$$
It satisfies K·∂R=0 and $K\cdot K=-D<0$, with positive K⁰ throughout the slab. In particular K is future timelike, agrees with U at the centre, and has not been renormalized to unit length away from the centre. Its spherical formula extends smoothly as $K^i=-HX^i/c$ in Cartesian coordinates.

K is not a Killing field of this history. An explicit component is
$$
 (\mathcal L_Kg)_{0\chi}
 =a^2\partial_0K^\chi
 =-\frac{a^2\chi\dot H}{c^2}
 =\frac{a^2\chi}{2c^2t^2},\tag{6}
$$
which is nonzero for χ>0. Its time-time and spatial diagonal Lie derivatives vanish, but that does not eliminate the nonzero mixed component. No stationary Killing-charge argument is being imported.

Using the mixed stress in (1), the separately defined current is
$$
 J^\mu=-T^\mu{}_{\nu}K^\nu
 =\left(u,\frac{pH\chi}{c},0,0\right).\tag{7}
$$
In x⁰ and χ coordinates its nonzero components have energy-density units. The full four-dimensional determinant is $\sqrt{-g}=a^3\chi^2\sin\theta$. For χ>0 its divergence is therefore
$$
 \begin{aligned}
 \nabla_\mu J^\mu
 &=\frac{1}{a^3\chi^2}
   \left[\partial_0(a^3\chi^2u)
   +\partial_\chi\left(a^3\chi^2\frac{pH\chi}{c}\right)\right]\\
 &=\frac1c\,[\dot u+3Hu+3Hp]=0.\tag{8}
 \end{aligned}
$$
The smooth Cartesian extension gives the same result at the centre. In particular the radial pressure contribution has been retained. A two-dimensional divergence without the spherical area factor would be an incorrect check. This explicit conservation uses the fixture and its selected current; stress conservation alone does not make the current built from every vector divergence-free.

On the registered slice, $-n_\mu J^\mu=u$, so direct integration gives
$$
 Q_K(t)=\frac{4\pi}3u(t)a(t)^3\chi_0^3
 =u(t)V(t)=\frac{c^2R_b(t)^3}{8Gt^2}
 =E_{\rm MS}(t,\chi_0).\tag{9}
$$
This independently agrees with (4). The integration uses the dimensionless K normalization in (5); an extra factor c or a pointwise unit-normalization of K would change the stipulated charge. The slice charge has energy units because its integrand is energy/volume and its measure is volume.

For this same vector, changing coordinates from $x^0=ct$ to t gives $K^t=1/c$ and $K^\chi=-H\chi/c$. Using $K^t=1$ and $K^\chi=-H\chi$ instead rescales the vector and its current by c; the charge formula would require the corresponding compensation. It is not the normalization used here. Likewise $K\mapsto K/\sqrt D$ is a pointwise change of current, not a coordinate conversion; neither this charge nor its proved conservation is exported under that replacement.

## 5. Complete finite endpoint record

Define the reference constants, without treating any of them as new physical standards,
$$
 R_0=\frac{ct_0}{2},\quad
 V_0=\frac{\pi c^3t_0^3}{6},\quad
 u_0=\frac{3c^2}{32\pi Gt_0^2},\quad p_0=u_0/3,
 \quad E_0=u_0V_0=\frac{c^5t_0}{64G},\quad M_0=E_0/c^2.
$$
The exact history on this ball is
$$
 R_b=R_0\sqrt z,\quad V=V_0z^{3/2},\quad
 u=u_0z^{-2},\quad p=p_0z^{-2},\quad
 E_{\rm MS}=Q_K=E_0z^{-1/2},\quad
 M_{\rm MS}=M_0z^{-1/2}.\tag{10}
$$
In particular:

| Quantity | t=t0 | t=4t0 |
| --- | --- | --- |
| Areal radius | ct0/2 | ct0 |
| Proper and areal volume | V0 | 8V0 |
| Energy density | u0 | u0/16 |
| Pressure | p0 | p0/16 |
| Geometric energy and slice charge | c⁵t0/(64G) | c⁵t0/(128G) |
| Defined quasi-local mass | c³t0/(64G) | c³t0/(128G) |
| HR_b/c | 1/4 | 1/8 |
| Boundary D | 15/16 | 63/64 |

These endpoint values come from the full registered history, not an assumed endpoint rescaling independent of the field/source check.

## 6. Oriented side flux and finite Gauss balance

On χ=χ0 the outward unit spacelike normal is
$$
 s_\mu=(0,a,0,0),\qquad
 s^\mu=(0,1/a,0,0),\qquad s\cdot s=1,\quad U\cdot s=0.
$$
Its contraction with the current and the proper side measure are
$$
 J^\mu s_\mu=\frac{pHR_b}{c},\qquad
 d\Sigma=R_b^2\sin\theta\,dx^0d\theta d\phi
 =cR_b^2\sin\theta\,dt d\theta d\phi.
$$
Thus the exact outward current flux is
$$
 F_K=\int_{t_0}^{4t_0}4\pi pHR_b^3\,dt
 =\int_{t_0}^{4t_0}p\dot V\,dt.\tag{11}
$$
The second equality uses $\dot V=3HV=4\pi HR_b^3$, not a zero-flux boundary condition. J·s has energy-density units; dΣ has length³ units. The c in dx⁰=c dt cancels the 1/c in J·s. Equivalently the instantaneous physical energy rate through the side is c times J·s times its area.

For clarity about Lorentzian orientation, the final spacelike cap's directed covector measure is $-n_\mu dV$, and the initial cap's is $+n_\mu dV$, with n future unit timelike. These include the timelike-normal sign in the Lorentzian Gauss formula. The outward side measure is $s_\mu d\Sigma$. The cap contributions are therefore +Q_K(4t0) and −Q_K(t0), giving
$$
 0=\int_{\rm slab}\nabla_\mu J^\mu d\mathcal V
 =Q_K(4t_0)-Q_K(t_0)+F_K.\tag{12}
$$
One may verify the same signs directly by integrating the coordinate divergence in (8). The χ=0 term vanishes as χ³, so the regular centre supplies no hidden boundary flux.

The finite integral can be evaluated without using (12). From (10),
$$
 F_K=\frac{3}{2}p_0V_0\int_1^4z^{-3/2}\,dz
 =\frac{3}{2}p_0V_0
 =\frac{E_0}{2}=\frac{c^5t_0}{128G}>0.\tag{13}
$$
Here $\int_1^4z^{-3/2}dz=1$. Substitution of the two separately computed cap charges then gives $E_0/2-E_0+E_0/2=0$. This is a complete finite charge ledger on the one prescribed slab.

## 7. Fluid-frame flux and independent pressure-work check

Define the fluid-frame outward energy flux scalar as
$$
 q_{\rm fluid}:=-T_{\mu\nu}U^\mu s^\nu=0,\tag{14}
$$
because T0χ=0 and U·s=0. Its physical energy rate per area would be c q_fluid, also zero. This is a zero net flux of fluid-frame energy; the perfect-fluid model does not describe individual photon paths or license a claim that no photons ever cross the geometrical boundary.

Equation (14) does not set J·s to zero. For this source $-T^\mu{}_{\nu}U^\nu=uU^\mu$, whereas J includes the spatial part of K. Pressure acting on that part gives exactly the nonzero radial component in (7). Even the fluid-frame energy vector has divergence
$$
 \nabla_\mu(uU^\mu)=\frac1c(\dot u+3Hu)=-\frac{3Hp}{c},
$$
which expresses the work term rather than a violation of stress conservation. It is not the conserved current J.

An independent local conservation calculation gives, for the same comoving volume,
$$
 \frac{d(uV)}{dt}=V\dot u+u\dot V
 =-3HV(u+p)+3HuV=-p\dot V.\tag{15}
$$
Using p=p0z⁻² and V=V0z³ᐟ², the finite pressure-work term is
$$
 W:=\int_{t_0}^{4t_0}p\dot V\,dt
 =\frac32p_0V_0\int_1^4z^{-3/2}\,dz
 =\frac{E_0}{2}=F_K,\qquad \Delta E=-W.\tag{16}
$$
This work balance follows from the checked fluid conservation law and the actual volume change; the independent side-flux and geometric computations explain its relation to the selected charge. In this fixture equality of Q_K and uV makes the two ledgers coincide. The equality F_K=W describes the same finite energy decrease in two ways. These are not two separate losses or two independent outputs.

W is a hydrodynamic pressure-work term for this geometrical region. It is not asserted to be heat, an externally supplied photon flux, energy harvested by an apparatus, or the energy acquired by a named wall or reservoir. No such wall or reservoir has been supplied. One need not invent a destination within an isolated Minkowski ledger to reconcile (14) and (16): the region is embedded in the expanding fluid and the conserved geometric-current balance contains its nonzero side flux.

## 8. Scientific scope, source roles and limits

The accepted conditional statement is that this exact finite worldtube has a divergence-free selected current and a varying enclosed charge, with the computed boundary flux and pressure-work term closing the same finite ledger. The fact that K is non-Killing is checked explicitly; it does not obstruct the independently verified conservation of this J. Conversely current conservation does not by itself remove a boundary term.

The equality of geometric E_MS, slice charge Q_K and integrated comoving matter energy uV was proved for this spatially flat homogeneous fixture. It is not a general identification of all quasi-local masses with proper matter-energy integrals. M_MS is defined by E_MS/c²; it is neither a conserved rest-particle count nor a newly measured inertial mass. No asymptotically flat exterior or ADM construction exists in the supplied contract, and no universe-total-energy conclusion is made.

Three existing results delimit the scope; none supplies a dynamical coefficient for this calculation:

- [Boost-defined inertia of the complete radiation-shell source](closed_radiation_shell_inertia.md) concerns a stationary complete-source tensor, supplied Minkowski boost and simultaneous-slice integration. Its defined small-velocity momentum coefficient is $E_{\rm total}/c^2$, with a rest-active-mass comparison only at shared leading-field scope. The present region has no such stationary complete isolated source or boost registration; its changing quasi-local mass neither changes that coefficient nor contradicts it.
- [One radial rod and the matter energy of two static sources](static_radial_length_and_proper_matter_energy.md) compares specified static sources with the same exterior but different integrated proper matter energies, with declared static-length and infinity-normalized Komar conventions. The equality E_MS=Q_K=uV here neither identifies proper matter energy with exterior/Komar mass generally nor removes that source ambiguity.
- [Spherical mass from one orbiting gyroscope](spherical_mass_from_one_orbiting_gyroscope.md) uses a registered circular orbit, moving clock and signed spin components in a smooth static spherical annulus. Untrapped spheres and nonnegative geometric mass here do not supply a static annulus or its orbital readout. That inverse is not applied to this expanding region.

The [Einstein–four-scalar torus family](local_einstein_four_scalar_development.md) is also distinct: it has its own scalar data, inhomogeneous spatial stress, torus geometry, coupling parameter and registered observer/variance. No stress averaging, geometry or parameter identification, slice map or observable bridge is supplied. This homogeneous ideal-radiation-fluid calculation provides no scalar-family energy formula, lifespan, variance correction or native mass calibration. It may inform the boundary accounting in a future question, but no result from that scalar calculation is imported.

The conventional primary framework is Sean A. Hayward, [*Unified first law of black-hole dynamics and relativistic thermodynamics*, arXiv:gr-qc/9710089v2](https://arxiv.org/html/gr-qc/9710089v2), version 2, 27 August 1998. The original derivation consulted Section II through Eq. (2.10), Section V through Eq. (5.11), and Section VIII through Eq. (8.20), with surrounding retrieved context, for spherical energy, current and balance conventions. That scoped consultation is reused here; no new or full-paper read is claimed. The source's additional conserved material-current assumptions in its thermodynamic discussion are not imported: no conserved material current, particle inventory or thermal preparation has been supplied. The exact metric source, factors of c and G, region, normals, charge, divergence and finite integrals above were derived manually rather than adopted from a general theorem. No literature-novelty claim is made.

All geometry, gravitational equation, clock and dimensional scales are supplied conventional structure. No native G, c, time, energy or mass unit, empirical validation, physical boundary/source realization, new inertia or heat law, work extraction, global conserved invariant mass or ontology validation follows. The retired kappa-gravity programme remains retired. No further dust, curvature, alternative boundary, horizon or cosmological case is selected here.

## 9. Review provenance

This article assembles the accepted CL108/v1 result. The sole Classical author and the distinct Classical scientific reviewer were separate; the reviewer had prospective design and candidate-outcome exposure, so the review was nonblind. The completed review admitted the finite expanding-region mass balance. DET Energy Research then assessed recipient assumptions, normalization and scope, reusing that proof review, and the coordinator admitted the result with those limits. This publication assembly preserves the proof and incorporates those scope clarifications; it adds no scientific model, theorem, observation or execution.
