# Radial energy of a radiation-loaded membrane

Conditional energy estimate under supplied fluid and membrane laws

The specified coupled linear model has a strictly positive conserved quadratic energy. Let $q=\delta u$, let $v$ be the physical radial fluid velocity, and let $\xi,V=\dot\xi$ be the wall displacement and velocity. Put

$$
w_0=u_0+p_0=\frac{4u_0}{3},\qquad
\rho_a=\frac{w_0}{c^2},\qquad
\mu_s=\frac{3\tau_0}{c^2},\qquad
k_s=\frac{2\tau_0}{R_0^2},\qquad A_0=4\pi R_0^2 .
$$

Here $\rho_a$ and $\mu_s$ are, respectively, the supplied model's bulk inertial coefficient and surface mass/area coefficient; no native mass scale is derived. On the fixed background ball,

$$
\boxed{\mathcal Q=
\int_{B_{R_0}}\left[\frac{q^2}{8u_0}+
\frac{2u_0}{3c^2}v^2\right]d^3x
+\frac{6\pi\tau_0R_0^2}{c^2}V^2
+4\pi\tau_0\xi^2,\qquad
\mathcal Q(t)=\mathcal Q(0).}
\tag{1}
$$

This holds for every smooth compatible radial solution of the registered linear problem on $0\leq t\leq 2\sqrt3R_0/c$, in the fixed-material and fixed-radiation-content tangent class specified below. All four terms are strictly positive in their physical variables. The result is an a-priori energy statement, not a nonlinear existence, global stability, spectral, microscopic-reflection or self-gravity theorem.

## 1. Model and source boundaries

Supply Minkowski geometry, $x^0=ct$, signature $(-+++)$, positive $c,R_0,u_0,n_0$, $p_0=u_0/3$, and $\tau_0=u_0R_0/6$. The Cartesian tensor equation $\partial_\mu T^{\mu\nu}=0$ is expressed below in spherical components using the equivalent covariant divergence, including the radial geometric factors. Bare spherical-coordinate partial derivatives of tensor components are not used.

The accepted [surface material assignment](surface_material_for_static_radiation_shell.md) has the fixed law

$$
e(n)=an+Kn^2+b,\quad
an_0=\tau_0,\quad Kn_0^2=\tau_0/2,\quad b=3\tau_0/2,
\qquad p_s=ne'(n)-e(n)=Kn^2-b.
\tag{2}
$$

The constants are held fixed. The surface material amount is fixed exactly,
$N=4\pi R^2n=4\pi R_0^2n_0$.
The wall has perfect surface stress
$S^{ab}=(e+p_s)U_s^aU_s^b+p_s h^{ab}$.
At the reference $e_0=3\tau_0$ and $p_{s0}=-\tau_0$.
There is no tangential motion, shear rigidity, bending rigidity, viscosity or extra heat variable.

Inside the moving sphere, the added radiation model is

$$
T^{\mu\nu}=(u+p)U^\mu U^\nu+p\eta^{\mu\nu},\qquad
p=u/3,\qquad U_\mu U^\mu=-1,\qquad \nabla_\mu T^{\mu\nu}=0.
\tag{3}
$$

Outside is vacuum. This is a stipulated smooth, local-equilibrium perfect-fluid closure. It is not collisionless ray transport or a conclusion about a real photon mean free path. The moving interface is impermeable in its own rest frame and the complete interior-plus-surface stress is distributionally conserved, with no support or external drive.

The [surface material assignment](surface_material_for_static_radiation_shell.md) supplies its law and static source specialization, not loaded dynamics. The [complete static radiation-shell source](closed_radiation_shell_mass.md) supplies the reference traction $2\tau_0/R_0=p_0$. Its mass and gravitational conclusions retain their original scope and are not recomputed here. The [Newtonian homologous free-boundary comparison](matched_self_gravitating_fluid_crossing.md) and [discrete packet/free-mirror comparison](packet_preparation_and_boundary_response.md) are scope comparisons only. No gravitational, FLRW, Maxwell or QR scalar coefficient is imported.

The original derivation consulted the conventional worldvolume framework of [Mourão, Natário and Vicente, arXiv:2409.10602v1](https://arxiv.org/html/2409.10602v1), version 1, §§2.1–2.3 and §2.5 through Eq. (62). This assembly reuses that scoped consultation; it claims no new or full-paper read. Those sections provide context for surface stress and normal/tangential equations; they do not supply the radiation-loaded result derived here. No Dyson-sphere theorem or literature-novelty claim is made.

The result is a synthetic analytic construction under supplied laws and units, without empirical observations.

## 2. Moving-interface normal equation and exact work balance

This section derives the nonlinear geometric relations needed only to linearize and form the energy Hessian. It does not assert a nonlinear solution-existence theorem.

Write $W=\dot R$, $\beta_s=W/c$ and
$\gamma_s=(1-\beta_s^2)^{-1/2}$.
In the time/radial orthonormal frame, the wall velocity and outward spacelike unit normal are

$$
U_s^\mu=\gamma_s(1,\beta_s\mathbf e_r),\qquad
\nu^\mu=\gamma_s(\beta_s,\mathbf e_r).
$$

Impermeability $U\cdot\nu=0$, spherical radial motion and future normalization give fluid velocity $v_b=W$ at the boundary. The interior traction is consequently
$T^{\mu\nu}\nu_\mu=p_b\nu^\nu$,
where $p_b$ is the actual boundary pressure in the common rest frame. There is no tangential force or energy flux through the wall in that frame.

Use
$K_{ab}=e_a\cdot\nabla_b\nu=-\nu\cdot\nabla_a e_b$.
Distributional differentiation of the interior indicator contributes $-p_b\nu\,\delta_\Sigma$; the normal part of the surface-stress divergence is $-S^{ab}K_{ab}\nu\,\delta_\Sigma$. Thus total conservation gives

$$
D_aS^{ab}=0,\qquad S^{ab}K_{ab}=-p_b .
\tag{4}
$$

The tangential energy equation is consistent with the fixed material amount, rather than an extra restriction on the pressure field. In the wall proper-length derivative $D_{U_s}$, number conservation gives $D_{U_s}n=-2n\gamma_sW/(cR)$. The identity $ne'=e+p_s$ then gives $D_{U_s}e+(e+p_s)2\gamma_sW/(cR)=0$, exactly the temporal projection of $D_aS^{ab}=0$. Its angular projections vanish by spherical uniformity.

In a wall-orthonormal frame the relevant curvatures are
$$
K_{UU}=-\frac{\gamma_s^3\ddot R}{c^2},\qquad
K_{\hat\theta\hat\theta}=K_{\hat\phi\hat\phi}=\frac{\gamma_s}{R}.
$$
The first identity follows by differentiating $U_s$ along its proper-length parameter and contracting its acceleration with $\nu$; the angular identities follow from the outward curvature of a sphere. Since $S^{\hat a\hat b}=\mathrm{diag}(e,p_s,p_s)$, (4) yields

$$
\boxed{\frac{e\gamma_s^3}{c^2}\ddot R
=p_b+\frac{2p_s\gamma_s}{R}.}
\tag{5}
$$

In particular, the normal inertial coefficient is $e/c^2$, not $(e+p_s)/c^2$. The static equation gives $p_0+2p_{s0}/R_0=0$, precisely the accepted reference traction. Reversing the normal flips both signed curvature and force and leaves (5) unchanged.

Let $E_s(R)=4\pi R^2e(N/(4\pi R^2))$ denote the wall rest energy at fixed $N$. Area work gives
$$
E_s'(R)=-8\pi R\,p_s.
\tag{6}
$$
The wall inertial-frame energy is $E_{\rm wall}=\gamma_s E_s$. To check this directly, the invariant surface delta is
$\delta_\Sigma=\delta(r-R)/\gamma_s$; the pushed-forward time-time surface stress is $e\gamma_s^2$, so its fixed-time integral is $4\pi R^2e\gamma_s$. Tangential pressure does not add a spurious radial kinetic coefficient.

Using (5)–(6),
$$
\frac{d}{dt}(\gamma_s E_s)
=4\pi R^2W\left[-\frac{2p_s\gamma_s}{R}
+\frac{e\gamma_s^3\ddot R}{c^2}\right]
=4\pi R^2p_bW .
\tag{7}
$$

The moving-volume radiation balance is independently obtained from the temporal equation in (3):
$$
\frac{d}{dt}\int_{r<R(t)}T^{00}d^3x
=4\pi R^2[W T^{00}-cT^{0r}]_b.
$$
At the wall $v_b=W$, hence
$T^{00}=(u+p)\gamma_s^2-p$ and
$cT^{0r}=(u+p)\gamma_s^2W$.
The bracket is exactly $-p_bW$. The two sides of (7) therefore exchange equal and opposite power:

$$
\frac{dE_{\rm rad}}{dt}=-4\pi R^2p_bW,\qquad
\frac{dE_{\rm wall}}{dt}=+4\pi R^2p_bW,\qquad
\frac{dE_{\rm total}}{dt}=0.
\tag{8}
$$

This derives the complete total-energy formula and its interface-work cancellation. It retains moving-volume and actual boundary-pressure terms. No uniform-pressure approximation was used.

## 3. Radiation content and linear acoustic equations

Contract (3) with $U_\nu$. Normalization gives
$$
U^\mu\nabla_\mu u+(u+p)\nabla_\mu U^\mu=0.
$$
For $p=u/3$, set
$s(u)=(u/u_0)^{3/4}$.
Then
$$
U\cdot\nabla s=-s\,\nabla\cdot U,\qquad
\nabla_\mu(sU^\mu)=0.
\tag{9}
$$
Impermeability makes this current's normal wall flux zero, so
$$
C=\int_{r<R(t)}s(u)\gamma\,d^3x,\qquad
C_0=\frac{4\pi R_0^3}{3}
\tag{10}
$$
is conserved for smooth solutions of the supplied model. Here $\gamma=U^0$, with $x^0=ct$. This normalization gives $C$ volume units. The name “adiabatic content” identifies a mathematical current of this equation of state; it asserts neither measured entropy nor physical photon count.

Linearize about $u_0,v=0,R_0$, with $q=\delta u$, $\xi=R-R_0$, $V=\dot\xi$. At first order
$$
\delta T^{00}=q,\qquad
\delta T^{0r}=w_0v/c,\qquad
\delta T^{ij}=(q/3)\delta^{ij}
$$
in Cartesian spatial components. Transforming their divergence to the radial form gives

$$
\boxed{q_t+w_0\frac1{r^2}\partial_r(r^2v)=0,\qquad
\rho_a v_t+\frac13 q_r=0,\qquad 0<r<R_0.}
\tag{11}
$$

Thus $q_{tt}=(c^2/3)r^{-2}\partial_r(r^2q_r)$, and the sound speed is $c_s=c/\sqrt3$. The specified finite interval $T=2\sqrt3R_0/c$ is therefore two reference acoustic crossing times. The full radial field is retained; neither homogeneous pressure nor homologous flow is imposed.

For a smooth scalar and radial vector at the center, $q$ has an even smooth radial expansion and $v=r\,a(r^2,t)$ near zero. In particular $q_r(0,t)=0$, $v(0,t)=0$, and there is no flux or singular point source at the center.

Fixed $N$ and the constitutive law give
$$
\delta n=-\frac{2n_0}{R_0}\xi,\qquad
\delta p_s=p_s'(n_0)\delta n=-\frac{2\tau_0}{R_0}\xi .
\tag{12}
$$
Because the background bulk pressure is uniform, evaluating its perturbation at $R_0+\xi$ changes its linear trace only at second order. Expanding (5) and impermeability therefore gives the dynamic boundary system

$$
\boxed{\dot\xi=V,\qquad v(R_0,t)=V,\qquad
\mu_s\dot V=\frac{q(R_0,t)}3-k_s\xi .}
\tag{13}
$$

Indeed the perturbation of $2p_s/R$ is
$2\delta p_s/R_0-2p_{s0}\xi/R_0^2=-2\tau_0\xi/R_0^2$.
This contains both material-pressure variation and sphere-curvature variation. A term $2\delta p_s/R_0$ alone would give the wrong wall stiffness.

The first variation of (10) is

$$
\boxed{\delta C=\frac1{w_0}\int_{B_{R_0}}q\,d^3x+A_0\xi=0 .}
\tag{14}
$$

The factor $\gamma$ contributes only at second order at rest. Integrating (11) and using (13) gives
$\partial_t\delta C=-A_0v(R_0)+A_0V=0$.
Thus the declared linear content constraint is preserved, not an extra time-dependent condition imposed independently of the PDE.

## 4. Compatible preparation class is nonempty

Smooth initial data satisfy center regularity, (14), $v_0(R_0)=V_0$, and compatibility between the time derivative of that relation and the two dynamical equations:

$$
-\frac{q_{0,r}(R_0)}{3\rho_a}
=\frac{q_0(R_0)/3-k_s\xi_0}{\mu_s}.
\tag{15}
$$

Higher compatibility conditions are obtained by further differentiation using (11)–(13). They are required to the order of smoothness assumed; no arbitrary boundary trace is independently prescribed. Equations (11)–(13) form the bulk evolution plus a moving-wall degree of freedom and its kinematic coupling, rather than two unrelated conditions on a rigid wall.

For an explicit nonzero class witness, take any nonzero smooth dimensionless $f(s)$ supported strictly within $1/4<s<1/2$, put $s=r/R_0$, and choose the tangent data

$$
q_0(r)=\varepsilon u_0\,s^{-2}\frac{d}{ds}\big(s^2 f(s)\big),
\quad v_0=0,\quad \xi_0=0,\quad V_0=0 .
\tag{16}
$$

The expression is defined as zero in the neighborhoods of $s=0$ and $s=1$, where $f$ vanishes. It is smooth and nonzero, and
$$
\int_{B_{R_0}}q_0\,d^3x
=4\pi\varepsilon u_0R_0^3[s^2f(s)]_0^1=0.
$$
All initial fields and spatial jets vanish near the interface and the center. The evolution equations recursively give zero boundary time jets at the initial instant, so (15) and every initial compatibility condition hold. This is a nonempty-data check for the registered class, not a second observational case or a separately solved trajectory.

At sufficiently small amplitude $u>0$ and $n>0$ in kinematic paths used for variations. If an exactly fixed-$C$ kinematic path through tangent data is needed, an $O(\varepsilon^2)$ smooth interior density correction can enforce it because the derivative of $C$ with respect to such a density correction with nonzero volume integral is nonzero. This does not prove the nonlinear dynamical evolution exists. The finite-window result below is explicitly conditional on smooth linear solutions.

## 5. Fixed-content Hessian of the complete energy

Keep $N$ fixed and use the constrained energy
$$
\mathcal F=E_{\rm total}-\lambda C,\qquad \lambda=w_0=4u_0/3.
\tag{17}
$$

The value of $\lambda$ is determined by stationarity, not chosen to conceal a negative term. Direct first variation at equilibrium gives
$$
\delta E_{\rm total}
=\int q\,d^3x+(u_0A_0+E_s'(R_0))\xi
=\int q\,d^3x+w_0A_0\xi=w_0\delta C,
\tag{18}
$$
where $E_s'(R_0)=p_0A_0$. Thus $\delta\mathcal F=0$ for all fixed-$N$ first variations, including ones not restricted by $\delta C=0$.

For clarity, define $\mathcal Q$ as the coefficient of $\varepsilon^2$ in $\mathcal F(\varepsilon)-\mathcal F(0)$, so the corresponding Hessian is $2\mathcal Q$. Along exactly fixed-$N,C$ paths it is also the second-order coefficient of $E_{\rm total}-E_0$. Since (18) vanishes for $\mathcal F$, unspecified second-order corrections to the path make no contribution to this coefficient. This removes a possible ambiguity between tangent data and exact constraint-preserving paths.

In the bulk,
$$
T^{00}=(u+p)\gamma^2-p
=u+w_0v^2/c^2+O(\varepsilon^3)
$$
when $q,v=O(\varepsilon)$, and
$$
s(u)\gamma
=1+\frac{3q}{4u_0}-\frac{3q^2}{32u_0^2}
+\frac{v^2}{2c^2}+O(\varepsilon^3).
$$
Consequently the integrand in $\mathcal F$ is

$$
T^{00}-w_0s\gamma
=-p_0+\frac{q^2}{8u_0}+\frac{w_0v^2}{2c^2}
+O(\varepsilon^3).
\tag{19}
$$

In particular, its first derivative with respect to $u$ is zero at $u_0$. Therefore moving the domain does not leave an omitted $q(R_0)\xi$ cross term at second order. The only geometric volume term at this order is the expansion of $-p_0\operatorname{Vol}(B_R)$. The same statement holds under a smooth pullback to the background ball because terms multiplying the vanishing first variation cancel.

At fixed $N$,
$$
E_s'(R_0)=8\pi R_0\tau_0,\qquad
E_s''(R_0)=24\pi\tau_0,\qquad
p_0\operatorname{Vol}''(R_0)=16\pi\tau_0.
\tag{20}
$$
The second identity follows by differentiating (6), with
$d p_s/dR|_0=-2\tau_0/R_0$.
Thus the combined wall/geometric restoring coefficient is
$$
\frac12[E_s''(R_0)-p_0\operatorname{Vol}''(R_0)]\xi^2
=4\pi\tau_0\xi^2.
\tag{21}
$$
It is neither the bare second derivative of $E_s$ nor the energy of a wall at fixed external pressure without the fluid terms.

The wall kinetic term is $E_s(R_0)V^2/(2c^2)=6\pi\tau_0R_0^2 V^2/c^2$. Combining (19)–(21) gives exactly (1). This construction keeps the fluid velocity contribution to the conserved content and the wall moving-volume correction; omitting either would change the Hessian.

The constraint (14) selects the preparation class. Positivity of (1) in fact holds on the larger radial physical-variable space as well. No restriction was invoked merely to discard a negative direction, and no relabeling displacement has been counted as an additional physical mode.

## 6. Independent linear energy ledger and finite-window bound

The same quadratic form follows directly from the linear equations, without invoking nonlinear second-order dynamics. Set
$$
\epsilon_2=\frac{q^2}{6w_0}+\frac{\rho_a}{2}v^2
=\frac{q^2}{8u_0}+\frac{2u_0}{3c^2}v^2.
$$
Multiply the first equation in (11) by $q/(3w_0)$, and the second by $v$. Their sum is
$$
\partial_t\epsilon_2+
\frac1{r^2}\partial_r\left(r^2\frac q3\,v\right)=0.
\tag{22}
$$
Center regularity eliminates its inner boundary term. Hence
$$
\frac{d\mathcal Q_{\rm bulk}}{dt}
=-A_0\,\frac{q(R_0,t)}3\,V.
\tag{23}
$$

From (13), the wall quadratic energy obeys
$$
\begin{aligned}
\mathcal Q_{\rm wall}
&=\frac{A_0}{2}(\mu_sV^2+k_s\xi^2),\\
\frac{d\mathcal Q_{\rm wall}}{dt}
&=A_0V(\mu_s\dot V+k_s\xi)
=+A_0\,\frac{q(R_0,t)}3\,V .
\end{aligned}
\tag{24}
$$
This is the exact opposite of (23), using the actual acoustic trace. Adding them proves (1) for the smooth linear solution. The interface-work terms are one internal exchange, not two energy losses or outputs. No external wall support was inserted.

Let $\|\cdot\|_2$ denote the volume $L^2(B_{R_0},d^3x)$ norm, including the $4\pi r^2dr$ measure. Every term in (1) is positive because $u_0,\tau_0,R_0,c>0$, and $\mathcal Q=0$ implies $q=v=0$ almost everywhere and $\xi=V=0$. For smooth fields this is the zero physical state. No null physical radial direction is left within the specified variables.

A fully explicit dimensionless comparison norm is
$$
\|X\|_*^2=
\frac1{R_0^3}\int_{B_{R_0}}
\left[\left(\frac q{u_0}\right)^2+
\left(\frac v c\right)^2\right]d^3x
+\left(\frac{\xi}{R_0}\right)^2+
\left(\frac Vc\right)^2 .
\tag{25}
$$
Using $\tau_0=u_0R_0/6$,
$$
\frac{\mathcal Q}{u_0R_0^3}
=\frac1{R_0^3}\int_{B_{R_0}}
\left[\frac18\left(\frac q{u_0}\right)^2+
\frac23\left(\frac vc\right)^2\right]d^3x
+\frac{2\pi}{3}\left(\frac{\xi}{R_0}\right)^2
+\pi\left(\frac Vc\right)^2 .
\tag{26}
$$
It follows, without a claimed optimal unweighted constant, that
$$
\frac18\|X\|_*^2
\leq\frac{\mathcal Q}{u_0R_0^3}
\leq\pi\|X\|_*^2,\qquad
\boxed{\|X(t)\|_*^2\leq8\pi\,\|X(0)\|_*^2
\quad(0\leq t\leq2\sqrt3R_0/c).}
\tag{27}
$$
The exact weighted energy norm itself is constant; (27) merely converts it to the specified common-weight norm. The factor 8π compares squared norms, not the norms themselves. Component bounds, if desired, are
$$
\|q(t)\|_2^2\leq8u_0\mathcal Q(0),\quad
\|v(t)\|_2^2\leq\frac{3c^2}{2u_0}\mathcal Q(0),\quad
V(t)^2\leq\frac{c^2\mathcal Q(0)}{\pi u_0R_0^3},\quad
\xi(t)^2\leq\frac{3\mathcal Q(0)}{2\pi u_0R_0}.
\tag{28}
$$

These bounds control volume density and velocity norms and the wall position/velocity. They do not control gradients, pointwise density, the instantaneous pressure trace, higher derivatives, or regularity from arbitrary energy data. Smooth solution existence over the registered interval is a hypothesis of the a-priori statement, not a consequence asserted from this energy identity. Compatibility and a nonzero class were checked; no spectrum, exponential-mode theorem, nonlinear uniqueness or global evolution claim is made.

## 7. Units, decision and unresolved physical premises

The bulk kinetic coefficient $w_0/c^2$ has mass/volume units; $e_0/c^2$ has mass/area units. The wall stiffness $k_s=2\tau_0/R_0^2$ has pressure/length units, so $\mu_s\dot V$, $q/3$, and $k_s\xi$ are all pressures. Each volume integrand in (1) has energy/volume units. Its wall kinetic and restoring terms have energy units, as does $u_0R_0^3$. The power exchanged in (23)–(24) is area times pressure times velocity. The charge $C$ has volume units and $\lambda=w_0$ has energy/volume units, so $\lambda C$ is an energy.

The accepted result is a finite radial energy estimate for this one coupled model: the complete stress/interface equations yield (11)–(14); (1) is the constrained complete-energy second-order coefficient $\mathcal Q$, with Hessian $2\mathcal Q$; and direct boundary-work accounting conserves $\mathcal Q$ with the norm control (27). This supplies the stated loaded dynamics beyond the static/local material assignment. It is not another bare-material characteristic speed, a homogeneous-pressure oscillator or a change to a gravitational mass coefficient.

Remaining premises include the supplied Minkowski geometry and physical clock/unit mapping, ideal thin perfect membrane, continuum radiation equation of state/local equilibrium, exact impermeability and total stress conservation, and smooth compatible linear solutions. The equations are not derived from DET records. The result does not identify this hydrodynamic radiation with collisionless packets, demonstrate a physical reflecting material, or supply microscopic constitutive/scattering physics. It does not establish nonlinear or nonspherical stability, finite-amplitude persistence inside the CL107 density patch, self-gravitating/GR consistency, an actual heat/work device, work extraction or efficiency gain, a new mass/boost coefficient, a native scale, a scalar-family correspondence, an empirical result or ontology validation. Retired kappa-gravity remains retired.

No further shell mode, parameter law, spectrum or nonlinear extension is included.

## 8. Review provenance

This article assembles the accepted CL110/v1 result. A sole Classical author produced the proof; a distinct Classical reviewer checked the stable result, including the moving-interface traction, fixed-content expansion and independent pressure-work identity. The reviewer had prospective model and energy-method exposure, so the scientific review was nonblind, not design-independent. The Classical lane admitted the finite energy result. DET Relational State Research then assessed recipient premises, normalization and claim limits while reusing the completed proof review, and the coordinator admitted it with those limits. This publication assembly adds no model, theorem, empirical observation or scientific execution.
