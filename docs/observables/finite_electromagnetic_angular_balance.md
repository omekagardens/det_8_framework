# A finite electromagnetic angular-momentum balance

Conditional result under supplied Maxwell–Lorentz dynamics

The registered finite ledger closes exactly. Define the positive angular-impulse scale

$$
\mathcal J=\frac{\mu _0Qm_0}{12\pi R}
           =\frac{\mu _0QK_0R^2}{72},
\qquad m_0=\frac{4\pi}{3}K_0b^3,\quad b=R/2.
$$

For the one ball of radius $L=2R$, between $0$ and $t_f=4R/c$,

| Registered record | Exact value |
|---|---:|
| Initial field angular momentum $L_{\rm EM,z}(0)$ | $\mathcal J$ |
| Final field angular momentum $L_{\rm EM,z}(t_f)$ | $0$ |
| Field change $\Delta L_{\rm EM,z}$ | $-\mathcal J$ |
| Electromagnetic impulse on charged receiver $I_{\rm rec}$ | $2\mathcal J$ |
| Electromagnetic impulse on inner sheet $I_{\rm inner}$ | $0$ |
| Signed outward field angular flux $F_{\rm out,z}$ | $-\mathcal J$ |
| Support impulse on receiver | $-2\mathcal J$ |
| Impulse received by support | $2\mathcal J$ |

Thus $-\mathcal J+2\mathcal J+0-\mathcal J=0$. The negative outward flux is a net inward signed transfer of positive z angular momentum across the observation sphere. It is not set to zero by an assertion that radiation is negligible. No sign is asserted for the instantaneous flux throughout the switching transient. Negative signed angular flux implies neither an incoming free field nor inward signal propagation, and gives no sign of electromagnetic energy flux. The receiver remains clamped and its net mechanical angular change is zero; the support receives the angular impulse.

## 1. Fixed preparation and source roles

Supply Euclidean space, inertial time and positive $R,Q,K_0,\epsilon _0,\mu _0$, $c^{-2}=\epsilon _0\mu _0$, vacuum Maxwell–Lorentz dynamics in SI, and no added free or incoming field. The mathematical sources are

$$
\rho_Q=\frac{Q}{4\pi R^2}\delta(r-R),\quad \mathbf j_Q=0,
\qquad
\rho_b=0,\quad
\mathbf j_b=K_0f(t)\sin\theta\,\delta(r-b)\mathbf e_\phi,\quad b=R/2.
$$

The receiver is nonconducting, spherical and fixed. The current sheet is neutral and externally prescribed; this does not supply a mechanical model for its moving constituents or driver. Ideal sheets and average-self-field surface force are supplied continuum assumptions. This is a synthetic analytic construction, with no empirical observations.

The one switching interval is $T=R/c$:

$$
f(t)=
\begin{cases}
1&t\leq0,\\
1-10s^3+15s^4-6s^5,\quad s=t/T&0<t<T,\\
0&t\geq T.
\end{cases}
$$

Inside the interval $f'=-30s^2(1-s)^2/T$. Both $f'$ and $f''$ vanish at its endpoints, so $f$ is $C^2$. No slow-switching limit is used. The fixed observation sphere is not a material wall, and observation ends at the prescribed finite cut $t_f$.

Both charge distributions are time independent. The current has only an axisymmetric azimuthal component, so its distributional divergence is zero: the spherical divergence differentiates this component only with respect to $\phi$, and no radial current crosses the sheet. Equivalently, integration by parts around each closed azimuthal loop gives zero against every smooth scalar test function. The factor $\sin\theta\,\mathbf e_\phi=\hat{\mathbf z}\times\mathbf n$ is regular at the poles. Thus $\partial_t\rho+\nabla\cdot\mathbf j=0$ exactly.

Two accepted results provide scope comparisons only. CL023 uses supplied rigid-body impulse fixtures in which reduced translational recoil omits angular, application-site and reservoir information; its reservoir update is imposed, not a Maxwell-force theorem or a physical actuator. This calculation does not automatically realize that reservoir: matching source/driver mechanics, preparations and readouts would still be needed, and angular closure alone does not certify isolation. CL081 supplies a particular capacitor/resistor response and calibrated heat readout under additional physical-state assumptions. No such circuit, thermal store, heat formula or native-history probability is supplied or transferred here. No expanding-region GR pressure-work coefficient, scalar-family observable, mass relation or calibration enters this electromagnetic calculation.

Public context is Johns, [*A Spherical Version of Feynman’s Static Field Momentum Example*, arXiv:1911.05893v3](https://arxiv.org/html/1911.05893v3), version 3, 20 October 2023. The original derivation consulted the abstract and §§1–3, including Eqs. (2.1)–(3.4) and the stated approximation/backreaction assumptions. Those sections use a small-source dipole approximation, slow switching and a large-inertia free receiver. The present model specifies a finite current sheet and a clamped receiver instead; the proof below is derived from that supplied model. This assembly reuses the scoped source consultation and accepted proof, with no new or full-paper read or literature-novelty claim. Johns §6’s mass-flow interpretation is excluded, and no mass, gravity or ontology conclusion is imported.

## 2. Exact retarded field representation

The scalar potential is time independent:

$$
\Phi_Q(r)=
\begin{cases}
Q/(4\pi\epsilon _0R),&r<R,\\
Q/(4\pi\epsilon _0r),&r>R.
\end{cases}
$$

Consequently $\mathbf E_Q=E_Q(r)\mathbf e_r$, with $E_Q=0$ inside and $Q/(4\pi\epsilon _0r^2)$ outside the receiver. The ideal sheet has the prescribed radial jump and no tangential electric discontinuity.

For $\mathbf x=r\mathbf n$, the retarded vector potential is

$$
\mathbf A(\mathbf x,t)=
\frac{\mu _0K_0b^2}{4\pi}
\int_{S^2}
\frac{f(t-d/c)}{d}\,
(\hat{\mathbf z}\times\mathbf n')\,d\Omega',
\quad d=|\mathbf x-b\mathbf n'|.
\tag{1}
$$

This is the finite source integral, not a point-dipole expression. Its scalar kernel depends on $\mathbf n'$ only through $u=\mathbf n\cdot\mathbf n'$. Rotations fixing $\mathbf n$ therefore imply

$$
\int\mathbf n' h(\mathbf n\cdot\mathbf n')d\Omega'
=2\pi\mathbf n\int_{-1}^{1}u h(u)\,du.
$$

It follows exactly that

$$
\mathbf A=a(r,t)\sin\theta\,\mathbf e_\phi,\qquad
a(r,t)=\frac{\mu _0K_0b^2}{2}
\int_{-1}^{1}
\frac{u f(t-\sqrt{r^2+b^2-2rbu}/c)}
{\sqrt{r^2+b^2-2rbu}}\,du.
\tag{2}
$$

At the origin the original vector integral is zero; expansion of its smooth kernel for $r<b$ gives $a=O(r)$. Thus the apparent polar-coordinate factors do not produce a central singularity. The toroidal angular form has $\nabla\cdot\mathbf A=0$. Together with the time-independent scalar potential it obeys Lorenz gauge, so the conserved-source retarded potential solves the supplied Maxwell system.

Writing a dot for $\partial_t$ and a subscript r for $\partial_r$, the exact fields away from the sheets are

$$
\begin{aligned}
E_r&=E_Q(r),& E_\theta&=0,& E_\phi&=-\dot a\sin\theta,\\
B_r&=\frac{2a}{r}\cos\theta,&
B_\theta&=-\frac{a+ra_r}{r}\sin\theta,& B_\phi&=0.
\end{aligned}
\tag{3}
$$

Equation (3) includes the complete retarded switching field. Terms often described as induction and radiation are retained through (2), rather than discarded.

The single-layer kernel $1/d$ in (1) is locally integrable on the two-dimensional source sphere. The potential and its time derivatives through the needed orders are continuous across it: the local integral is bounded by a constant times $\int_0^\eta ds$, while $f,f',f''$ are bounded. Spatial derivatives have the standard finite one-sided jump associated with a surface current. This jump also follows from distributional Maxwell equations: $B_r$ is continuous and

$$
B_\theta(b^+)-B_\theta(b^-)=\mu _0K_0 f(t)\sin\theta.
$$

There is no delta-function electric field or magnetic field; the delta sources enter their derivatives. The tangential electric field is continuous at both sheets, and the magnetic field is smooth through $r=R$, where there is no current. Average self fields thus define the stipulated surface forces, without multiplying two delta functions. The fields and field-angular density are locally integrable throughout the finite ball.

## 3. Exact static source moment and initial fields

The moment is derived directly from the finite current:

$$
\begin{aligned}
\mathbf m_0
&=\frac12\int\mathbf x'\times\mathbf j_b(\mathbf x',0)\,d^3x'\\
&=\frac{K_0b^3}{2}\int
[\hat{\mathbf z}-\mathbf n'(\mathbf n'\cdot\hat{\mathbf z})]\,d\Omega'
=\frac{4\pi K_0b^3}{3}\hat{\mathbf z}.
\end{aligned}
\tag{4}
$$

Introduce $\alpha=\mu _0m_0/(4\pi)=\mu _0K_0b^3/3$, only as a supplied-parameter abbreviation.

At $t=0$, all retarded arguments are nonpositive, so $f=1$, $f'=0$. For $r>b$, the convergent expansion $1/d=r^{-1}\sum_{\ell\geq0}(b/r)^\ell P_\ell(u)$ gives $\int_{-1}^1u/d\,du=2b/(3r^2)$, because only $\ell=1$ survives. For $r<b$, the analogous expansion gives $2r/(3b^2)$. Continuity gives the value at $r=b$. Hence

$$
a_0(r)=
\begin{cases}
\alpha r/b^3,&r\leq b,\\
\alpha/r^2,&r\geq b.
\end{cases}
\tag{5}
$$

This is an exact angular-$\ell=1$ result for this sheet, although its exterior static formula has dipolar form. There has been no expansion in small $b/R$, and $b/R$ remains $1/2$.

The interior static magnetic field is $2\alpha\hat{\mathbf z}/b^3$. The exterior is

$$
\mathbf B_0=\frac{\alpha}{r^3}
(2\cos\theta\,\mathbf e_r+\sin\theta\,\mathbf e_\theta).
\tag{6}
$$

At $b$, $B_r=2\alpha\cos\theta/b^3$ on each side, while $B_\theta^-=-2\alpha\sin\theta/b^3$ and $B_\theta^+=\alpha\sin\theta/b^3$. Their difference is $\mu _0K_0\sin\theta$, the correct surface-current jump. The field at the receiver and observation sphere is finite and continuous in its magnetic components.

## 4. Finite terminal clearing

For any point with $r\leq2R$ and any source point on $b=R/2$,

$$
0\leq d\leq r+b\leq5R/2.
$$

At the final cut,

$$
t_f-d/c\geq4R/c-5R/(2c)=3R/(2c)>T.
$$

Every factor $f$, $f'$, and $f''$ needed in (1) and its field derivatives is therefore zero with a uniform positive slack of $R/(2c)$ past the switching endpoint. It follows that $\mathbf A,\mathbf B,\mathbf E_{\rm induced}$ vanish everywhere in the whole observation ball, including both source sheets and its boundary. Only $\mathbf E_Q$ remains. The statement is local to this finite ball at the prescribed finite cut; fields may still exist elsewhere. No infinite-time decay, quasistatic propagation or added homogeneous solution is used.

## 5. Direct endpoint field angular integrals

Use $\mathbf g_{\rm EM}=\epsilon _0\mathbf E\times\mathbf B$ and $l_z=(\mathbf x\times\mathbf g_{\rm EM})_z$. At the initial cut the electric field vanishes for $r<R$, and for $R<r<2R$,

$$
l_z(0)=r\sin\theta\,\epsilon _0E_Q B_{\theta,0}
=\frac{Q\alpha}{4\pi r^4}\sin^2\theta .
$$

Since $\int_{S^2}\sin^2\theta\,d\Omega=8\pi/3$,

$$
\begin{aligned}
L_{\rm EM,z}(0)
&=\frac{2Q\alpha}{3}\int_R^{2R}\frac{dr}{r^2}
=\frac{Q\alpha}{3R}=\mathcal J,\\
L_{\rm EM,z}(t_f)&=0.
\end{aligned}
\tag{7}
$$

There is no missing sheet angular density: the fields have finite jumps, so the ordinary locally integrable density has no surface delta contribution. Its values on measure-zero sheets do not affect (7). There is no central contribution or singularity; $E_Q$ vanishes in a neighborhood containing the entire inner sheet. At the final cut the magnetic field is zero, so the full field momentum is zero.

As a check within the same finite region at an intermediate time, the induced electric field crossed with the poloidal magnetic field has only meridional components, and therefore contributes no z angular density. Equation (3) gives the exact identity

$$
L_{\rm EM,z}(t)
=-\frac{2Q}{3}\int_R^{2R}(a+ra_r)\,dr
=\frac{2Q}{3}\,[R a(R,t)-2R\,a(2R,t)].
\tag{8}
$$

This is an algebraic check on the fixed-domain computation, not an additional observation case. It confirms that the angular contribution of the upper boundary cannot be dropped.

## 6. Direct receiver and source impulses

The receiver surface charge is $\sigma_Q=Q/(4\pi R^2)$. Its radial self-electric force has no z torque. The induced tangential electric field is continuous at $R$, so averaging self fields does not change it. There is no receiver magnetic force because its current is exactly zero. Thus

$$
\begin{aligned}
N_{\rm rec,z}(t)
&=\int_{S^2}R\sin\theta\,
\sigma_Q[-\dot a(R,t)\sin\theta]\,R^2d\Omega\\
&=-\frac{2QR}{3}\dot a(R,t),\\
I_{\rm rec}
&=-\frac{2QR}{3}[a(R,t_f)-a(R,0)]
=\frac{2Q\alpha}{3R}=2\mathcal J.
\end{aligned}
\tag{9}
$$

The endpoint theorem in (9) integrates the exact retarded field; it does not replace its intermediate-time potential with an instantaneous static potential.

For the inner sheet, $\rho_b=0$. Its force is $\mathbf K\times\mathbf B_{\rm av}$, where $\mathbf K=K_0f\sin\theta\,\mathbf e_\phi$ and the averaged magnetic field is poloidal. The cross product has only r and $\theta$ components, so its azimuthal component and its z torque vanish pointwise. In particular,

$$
N_{\rm inner,z}(t)=0,\qquad I_{\rm inner}=0.
\tag{10}
$$

This checks, rather than presumes, the zero electromagnetic torque. It does not assert zero mechanical angular momentum in the current carriers or zero impulse exchanged with their external driver. Those unmodeled mechanical quantities cannot be inferred from (10).

The clamp supplies the equal and opposite instantaneous z torque to keep the receiver at rest. Its impulse on the receiver is $-I_{\rm rec}$; the impulse delivered to the support by the receiver is $+I_{\rm rec}$. No rotor angular velocity, large moment of inertia or negligible rotational backreaction is assumed. The absence of a receiver current is exact for the supplied stationary charge preparation. The support-received impulse routes the already counted receiver electromagnetic impulse; it must not be added again to the electromagnetic ledger as another independent transfer. This is the impulse delivered to the support, not a complete support-body angular change, which would require its own other forces and mechanical model. Releasing the clamp would change receiver motion/current and the coupled source/field problem; the present result supplies no free-rotor final spin.

## 7. Direct finite outer flux from complete Maxwell stress

Use the stated Cauchy stress

$$
\sigma_{ij}=\epsilon _0(E_iE_j-\delta_{ij}E^2/2)
+\frac1{\mu _0}(B_iB_j-\delta_{ij}B^2/2).
$$

On the radial observation surface,
$(\mathbf x\times(\boldsymbol\sigma\cdot\mathbf n))_z
=L\sin\theta\,\sigma_{\phi r}$, where $L=2R$. The complete off-diagonal component is

$$
\sigma_{\phi r}=\epsilon _0E_\phi E_r+\mu _0^{-1}B_\phi B_r
=-\epsilon _0E_Q(L)\dot a(L,t)\sin\theta.
\tag{11}
$$

The diagonal isotropic terms give radial traction and zero cross product. The magnetic shear term vanishes because $B_\phi=0$, even during the full transient. The pure induced electric term has no radial component, and pure Coulomb stress has no azimuthal component. The Coulomb–induced cross term in (11) survives. Thus all field terms relevant to this angular readout have been either retained or shown identically zero by the exact symmetry.

With the outward unit normal $\mathbf n=\mathbf e_r$ and the minus sign defining outward angular flux,

$$
\begin{aligned}
\dot F_{\rm out,z}(t)
&=-L^3\int_{S^2}\sin\theta\,\sigma_{\phi r}\,d\Omega
=\frac{2QL}{3}\dot a(L,t),\\
F_{\rm out,z}
&=\frac{2QL}{3}[a(L,t_f)-a(L,0)]
=-\frac{2Q\alpha}{3L}
=-\mathcal J.
\end{aligned}
\tag{12}
$$

The side integral was computed directly from Maxwell stress, independently of defining a residual by conservation. No energy-flux calculation or claim about radiation energy is needed. The sign of a z-angular flux is a signed momentum-stress statement, not a statement that electromagnetic signals propagate inward.

## 8. Conservation sign, sheets, units and decision

From the supplied local momentum law

$$
\partial_tg_i-\partial_j\sigma_{ij}=-f_i,
$$

multiply by $\epsilon_{k\ell i}x_\ell$. Differentiation of $x_\ell$ produces $\epsilon_{kji}\sigma_{ij}=0$, because Maxwell stress is symmetric. Therefore

$$
\partial_t(\mathbf x\times\mathbf g)_k
-\partial_j(\epsilon_{k\ell i}x_\ell\sigma_{ij})
=-(\mathbf x\times\mathbf f)_k.
$$

Integrating over the fixed ball and time interval gives exactly

$$
\Delta L_{\rm EM,z}+I_{\rm rec}+I_{\rm inner}+F_{\rm out,z}=0.
\tag{13}
$$

The sheet interpretation is consistent with this distributional law. At $R$, the jump in $\sigma_{\phi r}$ is
$\epsilon _0 E_\phi(E_r^+-E_r^-)=\sigma_QE_\phi$, which is precisely the tangential force used in (9). At $b$, $E_r=0$ and $B_\phi=0$, so $\sigma_{\phi r}=0$ on both sides, consistent with zero source z torque. No extra angular delta term is left unaccounted for. Equation (8) differentiated also makes (13) hold at each intermediate time with the directly computed torque and side rate.

Units provide an independent check. $K_0$ has A/m; $m_0$ has A m²; $a$ has tesla metre; $\dot a$ has V/m. $QRa$, $\mu _0Qm_0/R$ and $\mu _0QK_0R^2$ all have kg m²/s, the unit of angular momentum and integrated torque. Maxwell stress has N/m², and its moment integrated over area and time has the same unit. Positivity of $Q,K_0,R$ makes $\mathcal J>0$, fixing every endpoint sign in the table.

This exact conditional finite electromagnetic angular ledger has been accepted after distinct scientific review. The registered receiver impulse is twice the field angular momentum initially within the observation ball because the outer stress term imports the remaining signed amount. There is no defect or missing field term in the fixed mathematical model. The factor two compares the receiver impulse with the initial field angular momentum inside this chosen finite ball; it carries no energy-gain or efficiency interpretation.

The result provides a finite classical reference for explicit field, boundary and support accounting. It derives no Maxwell law from native DET records: source equations, spatial geometry, physical time, units, receiver constraint and force readout are added structure. It proves no isolated-apparatus closure, microscopic current-driver behavior, free-rotor final spin, physical source/receiver realization, electromagnetic energy balance, work, heat, efficiency, native unit/action/mass calibration, gravitational law, ontology or empirical validation. Retired kappa-gravity remains retired. No additional source, radius, switching profile, observation cut, feedback or radiation-energy case is included; a change to receiver or driver would require a separately specified model.

## 9. Review provenance

This article assembles the accepted CL109/v1 result. A sole Classical author produced the derivation; a distinct Classical reviewer checked the stable result, including the exact retarded source and the separately computed field, force and side integrals. The reviewer had prospective protocol-design and candidate-outcome exposure, so the scientific review was nonblind, not design-independent. The Classical lane admitted the finite result. DET Energy Research then assessed recipient assumptions, signs, normalization, support routing and scope while reusing that completed proof review, and the coordinator admitted the result with these limits. This publication assembly adds no scientific model, theorem, empirical observation or execution.
