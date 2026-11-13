# A compact cavity and smooth conserved collar lift of the four-chain field

Conditional analytic source construction

Yes. Replacing the periodic three-torus by a centered compact cubic homogeneous-Neumann cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ together with an explicitly constructed smooth compactly supported conserved support collar on $\mathbb R^3$ resolves the global periodic-source obstruction within the supplied static linearized gravitational model. Two axial Neumann standing modes in $\Omega$ with $L=4c\tau$ and $V=64c^3\tau^3$ reproduce the positive oscillator generator $H_{\rm sc}=(A_*/\tau)K$ without zero-point subtraction or offset and match the changed-prefix four-tick field operators $\Psi(n\tau,x_*)=F_*\phi_n$ ($n=0,1,2,3$) at a single explicit interior probe $x_*\in\operatorname{int}(\Omega)$ without mode-dependent detector gains or added standing-wave phase shifts. Extending the ground-state cavity stress tensor across $\partial\Omega$ via a staggered smooth Beltrami stress potential and a radial collar energy plateau gives a $C_c^\infty(\mathbb R^3)$ source tensor $T^{\mu\nu}_{\rm tot}$ that agrees pointwise with $\langle T^{\mu\nu}_{\rm sc}\rangle$ throughout $\Omega$, satisfies $\partial_\mu T^{\mu\nu}_{\rm tot}=0$ and $\|T^{ab}_{\rm tot}(x)\|\le T^{00}_{\rm tot}(x)$ everywhere on $\mathbb R^3$, cancels the anisotropic cavity bulk stress $\operatorname{diag}(E_1,E_2,0)$, admits a unique decaying harmonic-gauge gravitational potential $\bar h_{\mu\nu}$ obeying $\partial^\mu\bar h_{\mu\nu}=0$, satisfies $M_{\rm in}=M_{\rm active}=E_{\rm tot}/c^2$ for the complete cavity-plus-collar energy $E_{\rm tot}=E_0+E_{\rm support}$, and produces a strictly nonzero gauge-invariant exterior stress-quadrupole curvature contrast both asymptotically and at an explicit finite exterior point.

This is a conditional source construction on a prescribed flat Minkowski background within static first-order linearized gravity. It is not a native spatial or gravitational derivation, an equation of state or mechanical realization of a physical cavity wall, a nonlinear self-gravitating equilibrium, a full continuum quantum-field Casimir calculation, or an operational preparation, readout and reset protocol.

The [periodic scalar source lift](local_scalar_source_for_four_chain_field.md) established the local two-mode probe and generator match on $\mathbb T_L^3$ while diagnosing its periodic Poisson obstruction. The [stationary two-mode construction](stationary_dynamics_for_four_chain_fields.md) supplies the dimensionless canonical operators and changed-prefix Gaussian state, and the [Gaussian field-transport construction](gaussian_field_transport_on_native_histories.md) supplies the underlying kinematic history context with the saturated prefix $W_2$ released. The [closed-source active-mass note](closed_radiation_shell_mass.md), its [same-source boost companion](closed_radiation_shell_inertia.md), and the [static stress-quadrupole example](stress_quadrupole_at_equal_energy.md) supply the whole-space linearized gravitational, simultaneous-slice inertia, and Beltrami stress conventions retained below.

## 1. Cubic Neumann cavity and four-tick interior probe match

Retain the two dimensionless canonical pairs $(Q_1,P_1),(Q_2,P_2)$ on $L^2(\mathbb R^2)$ satisfying $[Q_j,P_k]=i\delta_{jk}I$ and $[Q_j,Q_k]=[P_j,P_k]=0$ on the common invariant Schwartz domain ${\cal S}(\mathbb R^2)$, together with the normalized centered product Gaussian ground state $\psi_0(q_1,q_2)=\pi^{-1/2}\exp[-(q_1^2+q_2^2)/2]$ whose quadrature variances are $\langle Q_j^2\rangle=\langle P_j^2\rangle=1/2$ with $\langle\{Q_j,P_j\}\rangle=0$. As in the [stationary two-mode construction](stationary_dynamics_for_four_chain_fields.md), set
$$
 \theta_1=\frac{5\pi}{4},\quad\theta_2=\frac{7\pi}{4},\qquad
 a_1=\sqrt{\frac{\beta}{2}(\sqrt2-1)},\quad
 a_2=\sqrt{\frac{\beta}{2}(\sqrt2+1)},\quad \beta>0,
$$
$$
 K=\frac12\sum_{j=1}^2\theta_j(Q_j^2+P_j^2),\qquad
 \phi_n=e^{inK}\phi_0e^{-inK}
 =\sum_{j=1}^2a_j\bigl(Q_j\cos n\theta_j+P_j\sin n\theta_j\bigr).
 \tag{1}
$$
The unaliased phase advances in (1) are stipulated, and the four ticks $n=0,1,2,3$ index the supported chain $a\prec b\prec x\prec y$.

Supply flat Cartesian coordinates $(x^0,x_1,x_2,x_3)$ on $\mathbb R^{1,3}$ with $x^0=ct$, metric $\eta=\operatorname{diag}(-1,1,1,1)$, orthonormal spatial basis $e_1,e_2,e_3$, and constants $c,\tau,A_*,\kappa>0$ denoting propagation speed, physical tick duration, action reference, and scalar kinetic-density normalization. Define the centered compact cubic cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ of volume $V=L^3$ and the two smooth axial profiles
$$
 \alpha_1(x_1)=\frac{5\pi}{L}\left(x_1+\frac L2\right),\qquad
 \alpha_2(x_2)=\frac{7\pi}{L}\left(x_2+\frac L2\right),\qquad
 u_1(x)=\cos\alpha_1(x_1),\qquad u_2(x)=\cos\alpha_2(x_2),
$$
with wavevectors $k_1=(5\pi/L)e_1$, $k_2=(7\pi/L)e_2$ and $|k_1|=5\pi/L$, $|k_2|=7\pi/L$. Because $\nabla u_1=-|k_1|\sin\alpha_1(x_1)\,e_1$ and $\nabla u_2=-|k_2|\sin\alpha_2(x_2)\,e_2$, checking the six faces of $\partial\Omega$ directly gives: on $x_1=\pm L/2$ ($n=\pm e_1$), $\alpha_1(-L/2)=0$ and $\alpha_1(L/2)=5\pi$ give $\sin\alpha_1(\pm L/2)=0$ while $e_1\cdot\nabla u_2=0$; on $x_2=\pm L/2$ ($n=\pm e_2$), $\alpha_2(-L/2)=0$ and $\alpha_2(L/2)=7\pi$ give $\sin\alpha_2(\pm L/2)=0$ while $e_2\cdot\nabla u_1=0$; on $x_3=\pm L/2$ ($n=\pm e_3$), $\partial_3u_1=\partial_3u_2=0$. Hence both modes satisfy $-\nabla^2u_j=|k_j|^2u_j$ on $\Omega$ and the homogeneous Neumann condition $n\cdot\nabla u_j=0$ on all six faces of $\partial\Omega$. Matching the wave-equation mode frequencies $\omega_j=c|k_j|$ to $\theta_j/\tau$ for $j=1,2$ gives $(5\pi c)/L=5\pi/(4\tau)$ and $(7\pi c)/L=7\pi/(4\tau)$, both equivalent to the single compatibility relation
$$
 \boxed{L=4c\tau,\qquad V=L^3=64c^3\tau^3.} \tag{2}
$$
Relative to the periodic torus side $8c\tau$ in the [periodic scalar source lift](local_scalar_source_for_four_chain_field.md), the half-wavelength Neumann boundary condition halves $L$ and reduces $V$ by a factor of eight. Equation (2) is a compatibility condition among the chosen mode integers $(5,7)$, the supplied wave operator, and the stipulated unaliased phases; it does not derive $c,\tau$ or $L$ from native order.

Take the minimally coupled scalar action on $\Omega$,
$$
 {\cal S}_{\rm cav}=\frac{\kappa}{2}\int_{t_1}^{t_2}dt\int_\Omega d^3x
 \left[\frac{\dot\Psi^2}{c^2}-|\nabla\Psi|^2\right].
 \tag{3}
$$
For any smooth variation $\delta\Psi$ on $[t_1,t_2]\times\overline\Omega$ vanishing at $t=t_1,t_2$, integration by parts over $\Omega$ (whose twelve edges and eight corners have zero two-dimensional surface area) yields
$$
 \delta{\cal S}_{\rm cav}
 =\kappa\int_{t_1}^{t_2}dt\int_\Omega d^3x\,
 \bigl(-c^{-2}\ddot\Psi+\nabla^2\Psi\bigr)\delta\Psi
 -\kappa\int_{t_1}^{t_2}dt\int_{\partial\Omega}(n\cdot\nabla\Psi)\,\delta\Psi\,dS.
$$
Under $n\cdot\nabla\Psi=0$ on $\partial\Omega$, the boundary variation vanishes without restricting $\delta\Psi|_{\partial\Omega}$, giving $c^{-2}\ddot\Psi-\nabla^2\Psi=0$ in $\Omega$. Likewise the outward normal energy flux across $\partial\Omega$ vanishes identically because $n\cdot\nabla u_j=0$ on every face.

On $[-L/2,L/2]$, $\alpha_1$ runs from $0$ to $5\pi$ and $\alpha_2$ runs from $0$ to $7\pi$, so $\int_{-L/2}^{L/2}\cos\alpha_1(x_1)\,dx_1=(L/5\pi)[\sin\alpha]_0^{5\pi}=0$ and $\int_{-L/2}^{L/2}\cos\alpha_2(x_2)\,dx_2=(L/7\pi)[\sin\alpha]_0^{7\pi}=0$. Consequently each mode has zero spatial mean on $\Omega$, $\int_\Omega u_1u_2\,d^3x=L(\int u_1\,dx_1)(\int u_2\,dx_2)=0$, and $\nabla u_1\cdot\nabla u_2=0$ pointwise because $e_1\cdot e_2=0$. Since $\int_0^{m\pi}\cos^2\alpha\,d\alpha=\int_0^{m\pi}\sin^2\alpha\,d\alpha=m\pi/2$ for every positive integer $m$, exact integration over $\Omega$ gives
$$
 \int_\Omega u_ju_k\,d^3x=\frac V2\delta_{jk},\qquad
 \int_\Omega\nabla u_j\cdot\nabla u_k\,d^3x=\frac V2|k_j|^2\delta_{jk}.
 \tag{4}
$$
Restricting ${\cal S}_{\rm cav}$ to the two-mode subspace $\Psi(t,x)=\sum_{j=1}^2q_j(t)u_j(x)$ yields the reduced oscillator Lagrangian ${\cal L}_{\rm red}=\sum_{j=1}^2\frac{\mu}{2}(\dot q_j^2-\omega_j^2q_j^2)$ with generalized mode inertia $\mu=\kappa V/(2c^2)$ and conjugate momenta $p_j=\mu\dot q_j$. Quantizing with the supplied action scale $A_*$, define on ${\cal S}(\mathbb R^2)$
$$
 B_j=\sqrt{\frac{2A_*c^2}{\kappa V\omega_j}},\qquad
 X_j(t)=Q_j\cos\omega_jt+P_j\sin\omega_jt,\qquad
 Y_j(t)=P_j\cos\omega_jt-Q_j\sin\omega_jt,
$$
$$
 q_j(t)=B_jX_j(t),\qquad
 p_j(t)=\mu B_j\omega_jY_j(t),\qquad
 \Psi(t,x)=\sum_{j=1}^2B_ju_j(x)X_j(t),
$$
$$
 [\Psi(t,x),\Pi(t,y)]=iA_*\frac2V\sum_{j=1}^2u_j(x)u_j(y)\qquad
 \left(\Pi:=\frac{\kappa}{c^2}\dot\Psi,\ x,y\in\Omega\right).
 \tag{5}
$$
Because $[X_j(t),Y_k(t)]=i\delta_{jk}I$ and $\mu B_j^2\omega_j=A_*$, the mode coordinates satisfy $[q_j(t),p_k(t)]=iA_*\delta_{jk}I$ and $[q_j(t),q_k(t)]=[p_j(t),p_k(t)]=0$ on ${\cal S}(\mathbb R^2)$, while (5) gives the orthogonal-projection kernel onto $\operatorname{span}\{u_1,u_2\}\subset L^2(\Omega)$ rather than a three-dimensional Dirac delta. Integrating the action-derived Hamiltonian density ${\cal H}(t,x)=\frac{\kappa}{2}[c^{-2}\dot\Psi^2+|\nabla\Psi|^2]$ over $\Omega$ via (4) and using the exact operator-ordering identity $X_j(t)^2+Y_j(t)^2=Q_j^2+P_j^2+\cos\omega_jt\sin\omega_jt\,(Q_jP_j+P_jQ_j-P_jQ_j-Q_jP_j)=Q_j^2+P_j^2$ on ${\cal S}(\mathbb R^2)$ gives
$$
 H_{\rm sc}=\int_\Omega{\cal H}(t,x)\,d^3x
 =\sum_{j=1}^2\frac{\kappa VB_j^2\omega_j^2}{4c^2}\bigl(X_j(t)^2+Y_j(t)^2\bigr)
 =\frac12\sum_{j=1}^2A_*\omega_j(Q_j^2+P_j^2)
 =\boxed{\frac{A_*}{\tau}K}. \tag{6}
$$
Thus $e^{itH_{\rm sc}/A_*}$ generates the Heisenberg evolution (5) with no normal-ordering subtraction and no identity offset $CI$.

Unlike the torus construction, the homogeneous Neumann boundary conditions fix the standing profiles $u_1,u_2$ without free spatial phase parameters. Instead, observe that $1<\sqrt2<2$ and $0<5/7<1$ imply $0<(\sqrt2-1)\sqrt{5/7}<1$, so $\delta_*:=\arccos[(\sqrt2-1)\sqrt{5/7}]$ lies strictly in $(0,\pi/2)$. Define the single probe location and common field unit
$$
 x_*=\left(-\frac{L}{10}+\frac{L}{5\pi}
 \arccos\!\left[(\sqrt2-1)\sqrt{\frac57}\right],\,\frac{L}{14},\,0\right),\qquad
 F_*=\frac{B_2}{a_2}>0. \tag{7}
$$
Because $0<\frac{L}{5\pi}\delta_*<\frac{L}{10}$, the first coordinate satisfies $-L/2<-L/10<x_{*,1}<0<L/2$, while $x_{*,2}=L/14\in(-L/2,L/2)$ and $x_{*,3}=0\in(-L/2,L/2)$; hence $x_*\in\operatorname{int}(\Omega)$ strictly away from $\partial\Omega$. Direct evaluation gives $\alpha_1(x_{*,1})=\frac{5\pi}{L}(\frac{2L}{5}+\frac{L}{5\pi}\delta_*)=2\pi+\delta_*$ and $\alpha_2(x_{*,2})=\frac{7\pi}{L}(\frac{4L}{7})=4\pi$, so $u_1(x_*)=\cos\delta_*=(\sqrt2-1)\sqrt{5/7}$ and $u_2(x_*)=\cos 4\pi=1$. Since $B_1/B_2=\sqrt{\omega_2/\omega_1}=\sqrt{7/5}$ and $a_1/a_2=\sqrt{(\sqrt2-1)/(\sqrt2+1)}=\sqrt2-1$, it follows that $B_1u_1(x_*)=B_2(a_1/a_2)=F_*a_1$ and $B_2u_2(x_*)=B_2=F_*a_2$. Because $\omega_jn\tau=n\theta_j$, evaluating (5) at $x_*$ proves the exact operator and ground-state identities
$$
 \boxed{\Psi(n\tau,x_*)=F_*\phi_n,\qquad n=0,1,2,3,}
$$
$$
 \langle\Psi(n\tau,x_*)\Psi(m\tau,x_*)\rangle
 =\frac{F_*^2}{2}\sum_{j=1}^2a_j^2e^{-i(n-m)\theta_j},\qquad
 [\Psi(n\tau,x_*),\Psi(m\tau,x_*)]
 =iF_*^2\beta\,\operatorname{sign}(n-m)I\quad(n\ne m). \tag{8}
$$
Dividing $\langle\Psi(n\tau,x_*)\Psi(m\tau,x_*)\rangle$ by $F_*^2$ reproduces the exact changed-prefix Toeplitz lags $\beta/\sqrt2$, $\beta/(2\sqrt2)+i\beta/2$, $i\beta/2$, and $-\beta/(2\sqrt2)+i\beta/2$ at $n-m=0,1,2,3$. Only one local point sample and one scalar conversion factor $F_*$ are used, with no mode-dependent gains or external phase shifts; selecting $x_*\in\operatorname{int}(\Omega)$ is disclosed spatial-attachment data rather than a native prediction.

## 2. Cavity ground stress and the boundary-traction obstruction

On $\Omega$, adopt the Weyl-ordered minimally coupled kinetic stress tensor associated with (3),
$$
 T^{\mu\nu}_{\rm sc}=\kappa\left[
 \frac12\{\partial^\mu\Psi,\partial^\nu\Psi\}-\frac12\eta^{\mu\nu}Z\right],\qquad
 Z=\frac12\eta^{\alpha\gamma}\{\partial_\alpha\Psi,\partial_\gamma\Psi\}
 =-\frac{\dot\Psi^2}{c^2}+|\nabla\Psi|^2. \tag{9}
$$
All quadratic products of field derivatives in (9) map ${\cal S}(\mathbb R^2)$ into itself, with $T^{00}_{\rm sc}={\cal H}$ a nonnegative quadratic form and $n_aT^{a0}_{\rm sc}=-\frac{\kappa}{2c}\{\dot\Psi,n\cdot\nabla\Psi\}=0$ on $\partial\Omega$. Differentiating (9) inside $\operatorname{int}(\Omega)$ cancels $\frac12\partial^\nu Z$ against $\frac12\{\partial^\mu\Psi,\partial_\mu\partial^\nu\Psi\}$, giving the operator identity $\partial_\mu T^{\mu\nu}_{\rm sc}=\frac{\kappa}{2}\{\Box\Psi,\partial^\nu\Psi\}=0$ for $\Box=-c^{-2}\partial_t^2+\nabla^2$.

Define the mode ground energies and bulk energy densities
$$
 E_1=\frac{A_*\omega_1}{2}=\frac{5\pi A_*}{8\tau},\qquad
 E_2=\frac{A_*\omega_2}{2}=\frac{7\pi A_*}{8\tau},\qquad
 E_0=E_1+E_2=\frac{3\pi A_*}{2\tau}>0,
$$
$$
 \rho_j=\frac{E_j}{V}\quad(j=1,2),\qquad
 \rho_0=\rho_1+\rho_2=\frac{E_0}{V}=\frac{3\pi A_*}{128c^3\tau^4}>0,
$$
so $\rho_1=\frac{5}{12}\rho_0$, $\rho_2=\frac{7}{12}\rho_0$, and $\frac{\kappa}{4}B_j^2|k_j|^2=\frac{\kappa}{4}\frac{2A_*c^2}{\kappa V\omega_j}\frac{\omega_j^2}{c^2}=\rho_j$. With $d_1=e_1$ and $d_2=e_2$, ground-state contraction on $\Omega$ gives $\langle c^{-2}\dot\Psi^2\rangle=\frac{2}{\kappa}\sum_{j=1}^2\rho_j\cos^2\alpha_j$, $\langle\frac12\{\partial_a\Psi,\partial_b\Psi\}\rangle=\frac{2}{\kappa}\sum_{j=1}^2\rho_j\sin^2\alpha_j\,d_j^ad_j^b$, and $\langle\{\dot\Psi,\partial_a\Psi\}\rangle=0$. Substituting $2\sin^2\alpha_j=1-\cos 2\alpha_j$ and $\sin^2\alpha_j-\cos^2\alpha_j=-\cos 2\alpha_j$ into (9) yields for all $x\in\Omega$
$$
 \boxed{\langle T^{00}_{\rm sc}(x)\rangle=\rho_0>0,\qquad
 \langle T^{0a}_{\rm sc}(x)\rangle=0,\qquad
 \langle T^{ab}_{\rm sc}(x)\rangle
 =\sum_{j=1}^2\rho_j\bigl[d_j^ad_j^b+(\delta^{ab}-d_j^ad_j^b)\cos 2\alpha_j\bigr].}
 \tag{10}
$$
Explicitly, $\langle T^{ab}_{\rm sc}\rangle$ is static and diagonal on $\Omega$,
$$
 \langle T^{11}_{\rm sc}(x)\rangle=\rho_1+\rho_2\cos 2\alpha_2(x_2),\qquad
 \langle T^{22}_{\rm sc}(x)\rangle=\rho_2+\rho_1\cos 2\alpha_1(x_1),\qquad
 \langle T^{33}_{\rm sc}(x)\rangle=\rho_1\cos 2\alpha_1(x_1)+\rho_2\cos 2\alpha_2(x_2),
$$
with $\partial_a\langle T^{ab}_{\rm sc}\rangle=0$ in $\operatorname{int}(\Omega)$ because each diagonal entry is independent of its own differentiation coordinate. Since $\int_{-L/2}^{L/2}\cos 2\alpha_1(x_1)\,dx_1=\int_{-L/2}^{L/2}\cos 2\alpha_2(x_2)\,dx_2=0$, integrating (10) over $\Omega$ gives $\int_\Omega\langle T^{00}_{\rm sc}\rangle\,d^3x=E_0$ and nonzero anisotropic bulk stress $\int_\Omega\langle T^{ab}_{\rm sc}\rangle\,d^3x=\operatorname{diag}(E_1,E_2,0)$.

Extending (10) by zero outside $\Omega$ does not produce an isolated conserved source on $\mathbb R^3$. Define $T^{\mu\nu}_{\rm trunc}(x):=\mathbf 1_\Omega(x)\langle T^{\mu\nu}_{\rm sc}(x)\rangle$. Although $n\cdot\nabla\Psi=0$ eliminates the gradient traction $n_a\{\partial_a\Psi,\partial_b\Psi\}$ on $\partial\Omega$, the isotropic pressure term $-\frac{\kappa}{2}n_bZ$ does not vanish on the cavity walls. For any test vector field $f\in C_c^\infty(\mathbb R^3;\mathbb R^3)$, the definition of distributional derivative and the Gauss–Green theorem on $\Omega$ give
$$
 \langle\partial_aT^{ab}_{\rm trunc},f_b\rangle
 =-\int_\Omega\langle T^{ab}_{\rm sc}(x)\rangle\,\partial_af_b(x)\,d^3x
 =-\int_{\partial\Omega}n_a\langle T^{ab}_{\rm sc}(x)\rangle f_b(x)\,dS,
$$
because $\partial_a\langle T^{ab}_{\rm sc}\rangle=0$ inside $\Omega$. Consequently, as a distribution on $\mathbb R^3$,
$$
 \int_\Omega\langle T^{ab}_{\rm sc}(x)\rangle\,d^3x=\operatorname{diag}(E_1,E_2,0),\qquad
 \boxed{\partial_a\bigl(\mathbf 1_\Omega\langle T^{ab}_{\rm sc}\rangle\bigr)
 =-n_a\langle T^{ab}_{\rm sc}\rangle\,\delta_{\partial\Omega}\ne 0,} \tag{11}
$$
where $\delta_{\partial\Omega}$ is the surface area measure on $\partial\Omega$. Specifically, the outward normal traction $n_a\langle T^{ab}_{\rm sc}\rangle$ equals $\pm(\rho_1+\rho_2\cos 2\alpha_2)e_1^b$ on $x_1=\pm L/2$, $\pm(\rho_2+\rho_1\cos 2\alpha_1)e_2^b$ on $x_2=\pm L/2$, and $\pm(\rho_1\cos 2\alpha_1+\rho_2\cos 2\alpha_2)e_3^b$ on $x_3=\pm L/2$; choosing $f(x)=(x_1,0,0)$ on a neighborhood of $\overline\Omega$ already yields $\langle\partial_aT^{ab}_{\rm trunc},f_b\rangle=-E_1\ne 0$. Inserting $T^{\mu\nu}_{\rm trunc}$ alone into $\nabla^2\bar h_{\mu\nu}=-(16\pi G/c^4)T_{\mu\nu}$ leaves $\partial^a\bar h_{ab}(x)=-(4G/c^4)\int_{\partial\Omega}|x-y|^{-1}n_a\langle T^{ab}_{\rm sc}(y)\rangle\,dS_y\ne 0$, violating the de Donder gauge condition required for linearized Einstein compatibility. A compatible whole-space gravitational source must therefore supply a confining stress structure outside $\Omega$.

## 3. Smooth Beltrami collar and dominant-energy admissibility

Write $B_R(0):=\{x\in\mathbb R^3:|x|<R\}$ for the open ball of radius $R>0$. For every $x\in\overline\Omega=[-L/2,L/2]^3$, $|x|\le\sqrt{3(L/2)^2}=\frac{\sqrt3}{2}L<L$ (with equality at the eight corners $(\pm L/2,\pm L/2,\pm L/2)$), giving the strict radial nesting
$$
 \overline\Omega\subset\overline{B_{\frac{\sqrt3}{2}L}(0)}\subset B_L(0)
 \subset B_{3L/2}(0)\subset B_{2L}(0)\subset B_{3L}(0).
$$
Because $\alpha_1,\alpha_2$ are affine functions on all of $\mathbb R$, define on $\mathbb R^3$ the smooth diagonal interior Beltrami potential $\Phi^{\rm int}(x)=\operatorname{diag}\bigl(\Phi_1^{\rm int}(x),\Phi_2^{\rm int}(x),\Phi_3^{\rm int}(x)\bigr)$ by
$$
 \Phi_1^{\rm int}(x_2)=-\frac{\rho_2}{4|k_2|^2}\cos 2\alpha_2(x_2),\qquad
 \Phi_2^{\rm int}(x_1)=-\frac{\rho_1}{4|k_1|^2}\cos 2\alpha_1(x_1),
$$
$$
 \Phi_3^{\rm int}(x_1,x_2)
 =\frac{\rho_1}{8|k_1|^2}+\frac{\rho_2}{8|k_2|^2}
 +\frac12\rho_2x_1^2+\frac12\rho_1x_2^2
 +\Phi_1^{\rm int}(x_2)+\Phi_2^{\rm int}(x_1). \tag{12}
$$
For any smooth diagonal tensor $\Phi_{mn}=\Phi_m\delta_{mn}$ with $\epsilon_{123}=+1$, expanding $T^{ab}(\Phi):=\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}$ directly gives $T^{11}=\partial_3^2\Phi_2+\partial_2^2\Phi_3$, $T^{22}=\partial_3^2\Phi_1+\partial_1^2\Phi_3$, $T^{33}=\partial_2^2\Phi_1+\partial_1^2\Phi_2$, $T^{12}=-\partial_1\partial_2\Phi_3$, $T^{13}=-\partial_1\partial_3\Phi_2$, and $T^{23}=-\partial_2\partial_3\Phi_1$. Since $\partial_2^2\Phi_1^{\rm int}=\rho_2\cos 2\alpha_2$, $\partial_1^2\Phi_2^{\rm int}=\rho_1\cos 2\alpha_1$, $\partial_1^2\Phi_3^{\rm int}=\rho_2+\rho_1\cos 2\alpha_1$, $\partial_2^2\Phi_3^{\rm int}=\rho_1+\rho_2\cos 2\alpha_2$, and all remaining second derivatives of $\Phi_m^{\rm int}$ vanish, $\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi^{\rm int}_{mn}(x)$ equals the smooth continuation of (10) identically at every $x\in\mathbb R^3$. Moreover, (12) satisfies the pointwise nonnegativity identity
$$
 2\Phi_3^{\rm int}(x)-\Phi_1^{\rm int}(x)-\Phi_2^{\rm int}(x)
 =\rho_2x_1^2+\rho_1x_2^2
 +\frac{\rho_1}{4|k_1|^2}\bigl(1-\cos 2\alpha_1(x_1)\bigr)
 +\frac{\rho_2}{4|k_2|^2}\bigl(1-\cos 2\alpha_2(x_2)\bigr)
 \ge \rho_2x_1^2+\rho_1x_2^2\ge 0 \qquad (x\in\mathbb R^3).
$$

To cut off $\Phi^{\rm int}$ and the total energy density smoothly on staggered spherical shells without surface layers, set
$$
 b(t)=\begin{cases}e^{-1/t},&t>0,\\0,&t\le 0,\end{cases}
 \qquad s=\frac{|x|}{L},\qquad \sigma=s^2=\frac{|x|^2}{L^2},
$$
$$
 \chi_{\rm st}(s)=\frac{b(4-s^2)}{b(4-s^2)+b(s^2-9/4)},\qquad
 \chi_{\rm rise}(s)=\frac{b(s^2-1)}{b(s^2-1)+b(9/4-s^2)},\qquad
 \chi_{\rm out}(s)=\frac{b(9-s^2)}{b(9-s^2)+b(s^2-4)}. \tag{13}
$$
For every integer $k\ge 1$ and $t>0$, writing $u=1/t>0$ gives $\frac{d}{du}(k\ln u-u)=k/u-1$ and $\frac{d^2}{du^2}(k\ln u-u)=-k/u^2<0$, so $t^{-k}e^{-1/t}=u^ke^{-u}\le k^ke^{-k}$ on all $(0,\infty)$ and $t^{-k}e^{-1/t}\to 0$ as $t\to 0^+$. Thus $b\in C^\infty(\mathbb R)$ is nonnegative and strictly increasing on $(0,\infty)$. In each ratio in (13), the two arguments of $b$ in the denominator sum to a positive constant ($7/4$, $5/4$, and $5$, respectively), so at least one argument is at least half that sum; hence the three denominators are bounded below on all $\mathbb R$ by $b(7/8)=e^{-8/7}>0$, $b(5/8)=e^{-8/5}>0$, and $b(5/2)=e^{-2/5}>0$. Because $\sigma=|x|^2/L^2$ is a smooth polynomial on $\mathbb R^3$, the radial profiles $x\mapsto\chi_{\rm st}(|x|/L)$, $\chi_{\rm rise}(|x|/L)$, $\chi_{\rm out}(|x|/L)$ belong to $C^\infty(\mathbb R^3)$ with values in $[0,1]$. Specifically: $\chi_{\rm st}(s)=1$ for $s\le 3/2$ and $0$ for $s\ge 2$; $\chi_{\rm rise}(s)=0$ for $s\le 1$ and $1$ for $s\ge 3/2$; $\chi_{\rm out}(s)=1$ for $s\le 2$ and $0$ for $s\ge 3$.

For a constant plateau $U_{\rm col}>0$ fixed explicitly below, define on all $\mathbb R^3$
$$
 \Phi_{mn}(x)=\chi_{\rm st}\!\left(\frac{|x|}{L}\right)\Phi^{\rm int}_{mn}(x),\qquad
 \varepsilon_{\rm tot}(|x|)=\Bigl[\rho_0+U_{\rm col}\,\chi_{\rm rise}\!\left(\frac{|x|}{L}\right)\Bigr]
 \chi_{\rm out}\!\left(\frac{|x|}{L}\right),
$$
$$
 T^{00}_{\rm tot}(x)=\varepsilon_{\rm tot}(|x|),\qquad
 T^{0a}_{\rm tot}(x)=T^{a0}_{\rm tot}(x)=0,\qquad
 T^{ab}_{\rm tot}(x)=\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}(x). \tag{14}
$$
Every component of $T^{\mu\nu}_{\rm tot}$ belongs to $C_c^\infty(\mathbb R^3)$ with $\operatorname{supp}\Phi_{mn}\subseteq\overline{B_{2L}(0)}$ and $\operatorname{supp}T^{\mu\nu}_{\rm tot}\subseteq\overline{B_{3L}(0)}$. On $|x|\le L$ (which strictly contains $\overline\Omega$), $\chi_{\rm rise}=0$ and $\chi_{\rm st}=\chi_{\rm out}=1$, so $T^{\mu\nu}_{\rm tot}(x)=\langle T^{\mu\nu}_{\rm sc}(x)\rangle$ pointwise throughout $\overline\Omega$.

Now derive an explicit elementary upper bound on the spatial operator norm $\|T^{ab}_{\rm tot}(x)\|=\sup_{|v|=1}|v_aT^{ab}_{\rm tot}(x)v_b|$ across every shell:

1. **Interior and energy-ramp region ($0\le s\le 3/2$).** Here $\chi_{\rm st}(s)=1$, so $T^{ab}_{\rm tot}(x)$ equals the diagonal matrix (10), whose diagonal entries satisfy $|\rho_1+\rho_2\cos 2\alpha_2|\le\rho_0$, $|\rho_2+\rho_1\cos 2\alpha_1|\le\rho_0$, and $|\rho_1\cos 2\alpha_1+\rho_2\cos 2\alpha_2|\le\rho_0$. Hence $\|T^{ab}_{\rm tot}(x)\|\le\rho_0$ for all $|x|\le\frac32L$, while $T^{00}_{\rm tot}(x)=\rho_0$ on $0\le s\le 1$ and $T^{00}_{\rm tot}(x)=\rho_0+U_{\rm col}\chi_{\rm rise}(s)\ge\rho_0$ on $1\le s\le 3/2$.

2. **Outer energy-taper and exterior region ($s\ge 2$).** Here $\chi_{\rm st}(s)=0$ identically, so $T^{ab}_{\rm tot}(x)=0$, while $T^{00}_{\rm tot}(x)=(\rho_0+U_{\rm col})\chi_{\rm out}(s)\ge 0$ on $2\le s\le 3$ and $T^{00}_{\rm tot}(x)=0$ for $s\ge 3$.

3. **Stress-cutoff transition shell ($3/2\le s\le 2$).** Here $\chi_{\rm rise}(s)=\chi_{\rm out}(s)=1$, so $T^{00}_{\rm tot}(x)=\rho_0+U_{\rm col}$ is constant across the entire transition shell with no boundary-layer vanishing at $s=3/2$ or $s=2$. Write $\eta(x):=\chi_{\rm st}(|x|/L)=F(\sigma)$ with $\sigma=|x|^2/L^2\in[9/4,4]$. First bound $\Phi_m^{\rm int}$ and its derivatives for $|x|\le 2L$ using $|k_1|=5\pi/L$, $|k_2|=7\pi/L$, $\rho_1=\frac{5}{12}\rho_0$, $\rho_2=\frac{7}{12}\rho_0$, and $x_1^2+x_2^2\le|x|^2\le 4L^2$:
   - Potential magnitudes: $|\Phi_1^{\rm int}|\le\frac{\rho_2}{4|k_2|^2}=\frac{\rho_0L^2}{336\pi^2}$, $|\Phi_2^{\rm int}|\le\frac{\rho_1}{4|k_1|^2}=\frac{\rho_0L^2}{240\pi^2}$, and since $\frac12\rho_2x_1^2+\frac12\rho_1x_2^2\le\frac12\rho_2(4L^2)=\frac76\rho_0L^2$ while $|1-2\cos 2\alpha_j|\le 3$, $|\Phi_3^{\rm int}|\le\bigl(\frac76+\frac{3}{480\pi^2}+\frac{3}{672\pi^2}\bigr)\rho_0L^2=\bigl(\frac76+\frac{3}{280\pi^2}\bigr)\rho_0L^2$. Using $\frac{1}{336}+\frac{1}{240}+\frac{3}{280}=\frac{5+7+18}{1680}=\frac{1}{56}$ and $\pi>3$ ($\frac{1}{56\pi^2}<\frac{1}{504}<\frac16$) gives
     $$
     \sum_{m=1}^3|\Phi_m^{\rm int}(x)|
     \le\left(\frac76+\frac{1}{56\pi^2}\right)\rho_0L^2
     <\frac43\rho_0L^2 \qquad (|x|\le 2L).
     $$
   - Gradients: $|\nabla\Phi_1^{\rm int}|\le\frac{\rho_2}{2|k_2|}=\frac{\rho_0L}{24\pi}$, $|\nabla\Phi_2^{\rm int}|\le\frac{\rho_1}{2|k_1|}=\frac{\rho_0L}{24\pi}$, and $|\nabla\Phi_3^{\rm int}|\le\sqrt{(\rho_2x_1)^2+(\rho_1x_2)^2}+|\nabla\Phi_1^{\rm int}|+|\nabla\Phi_2^{\rm int}|\le\bigl(\frac76+\frac{1}{12\pi}\bigr)\rho_0L$. Using $\pi>3$ ($\frac{1}{6\pi}<\frac{1}{18}<\frac{1}{12}$) gives
     $$
     \sum_{m=1}^3|\nabla\Phi_m^{\rm int}(x)|
     \le\left(\frac76+\frac{1}{6\pi}\right)\rho_0L
     <\frac54\rho_0L \qquad (|x|\le 2L).
     $$
   - Hessians and Laplacians: $\|\operatorname{Hess}\Phi_1^{\rm int}\|,|\nabla^2\Phi_1^{\rm int}|\le\rho_2=\frac{7}{12}\rho_0$, $\|\operatorname{Hess}\Phi_2^{\rm int}\|,|\nabla^2\Phi_2^{\rm int}|\le\rho_1=\frac{5}{12}\rho_0$, $\|\operatorname{Hess}\Phi_3^{\rm int}\|\le\rho_0$, $|\nabla^2\Phi_3^{\rm int}|\le 2\rho_0$, and $\|\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi^{\rm int}_{mn}\|\le\rho_0$:
     $$
     \sum_{m=1}^3|\Phi_m^{\rm int}|<\frac43\rho_0L^2,\qquad
     \sum_{m=1}^3|\nabla\Phi_m^{\rm int}|<\frac54\rho_0L,\qquad
     \bigl\|\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi^{\rm int}_{mn}\bigr\|\le\rho_0
     \qquad (|x|\le 2L). \tag{15}
     $$

   Next bound the derivatives of $F(\sigma)=b_1(\sigma)/D(\sigma)$ for $\sigma\in[9/4,4]$, where $b_1(\sigma)=b(4-\sigma)$, $b_2(\sigma)=b(\sigma-9/4)$, and $D(\sigma)=b_1(\sigma)+b_2(\sigma)\ge e^{-8/7}$. For $t>0$, $b'(t)=t^{-2}e^{-1/t}\in(0,4e^{-2}]$ and $b''(t)=(t^{-4}-2t^{-3})e^{-1/t}$, so $|b''(t)|\le t^{-4}e^{-1/t}+2t^{-3}e^{-1/t}\le 256e^{-4}+54e^{-3}$. Hence on $[9/4,4]$, $-4e^{-2}\le b_1'(\sigma)\le 0\le b_2'(\sigma)\le 4e^{-2}$ (which directly implies $|b_1'(\sigma)+b_2'(\sigma)|\le 4e^{-2}$) and $|b_1''(\sigma)|,|b_2''(\sigma)|\le 256e^{-4}+54e^{-3}$. Putting $p(\sigma)=b_1(\sigma)/D(\sigma)\in[0,1]$ and $q(\sigma)=b_2(\sigma)/D(\sigma)=1-p(\sigma)\in[0,1]$, the quotient rule gives
   $$
   F'(\sigma)=\frac{b_1'D-b_1D'}{D^2}
   =\frac{b_1'b_2-b_1b_2'}{D^2}
   =q(\sigma)\frac{b_1'(\sigma)}{D(\sigma)}-p(\sigma)\frac{b_2'(\sigma)}{D(\sigma)},
   $$
   and differentiating $N(\sigma)/D(\sigma)^2$ with $N=b_1'b_2-b_1b_2'$ (so $N'=b_1''b_2-b_1b_2''$) gives
   $$
   F''(\sigma)=\frac{N'D^2-2NDD'}{D^4}
   =\left(q(\sigma)\frac{b_1''(\sigma)}{D(\sigma)}-p(\sigma)\frac{b_2''(\sigma)}{D(\sigma)}\right)
   -2F'(\sigma)\frac{b_1'(\sigma)+b_2'(\sigma)}{D(\sigma)}.
   $$
   Because $p,q\ge 0$ satisfy $p+q=1$, convex-combination bounds with $D(\sigma)\ge e^{-8/7}$ yield on $[9/4,4]$
   $$
   |F'(\sigma)|\le\frac{4e^{-2}}{e^{-8/7}}=4e^{-6/7}=:F_1,
   $$
   $$
   |F''(\sigma)|\le\frac{256e^{-4}+54e^{-3}}{e^{-8/7}}+2F_1\frac{4e^{-2}}{e^{-8/7}}
   =256e^{-20/7}+54e^{-13/7}+32e^{-12/7}=:F_2.
   $$
   In radial variable $s=|x|/L\in[3/2,2]$, $\chi_{\rm st}(s)=F(s^2)$ satisfies $0\le\chi_{\rm st}(s)\le 1$, $|\chi_{\rm st}'(s)|=2s|F'(s^2)|\le 4F_1$, and $|\chi_{\rm st}''(s)|=|4s^2F''(s^2)+2F'(s^2)|\le 16F_2+2F_1$. In Cartesian coordinates, $\partial_k\eta(x)=\frac{2x_k}{L^2}F'(\sigma)$ and $\partial_k\partial_l\eta(x)=\frac{4x_kx_l}{L^4}F''(\sigma)+\frac{2\delta_{kl}}{L^2}F'(\sigma)$. Since $\|xx^{\mathsf T}\|=|x|^2=s^2L^2\le 4L^2$ for $3/2\le s\le 2$,
   $$
   |\nabla\eta(x)|\le\frac{4F_1}{L},\qquad
   \|\operatorname{Hess}\eta(x)\|\le\frac{16F_2+2F_1}{L^2},\qquad
   |\nabla^2\eta(x)|\le\frac{16F_2+6F_1}{L^2}
   \qquad\left(\frac32L\le|x|\le 2L\right). \tag{16}
   $$

   Now expand $\partial_k\partial_l(\eta\Phi_m^{\rm int})=\eta\partial_k\partial_l\Phi_m^{\rm int}+(\partial_k\eta)(\partial_l\Phi_m^{\rm int})+(\partial_l\eta)(\partial_k\Phi_m^{\rm int})+(\partial_k\partial_l\eta)\Phi_m^{\rm int}$. For any unit vector $v\in\mathbb R^3$, define $w^{(m)}_k:=\sum_{a=1}^3v_a\epsilon_{akm}$, which satisfies $|w^{(m)}|^2=\sum_{a,b=1}^3(\delta_{ab}-\delta_{am}\delta_{bm})v_av_b=1-v_m^2\le 1$. Then
   $$
   v_aT^{ab}_{\rm tot}(x)v_b
   =\eta(x)\,v_aT^{ab}(\Phi^{\rm int})(x)v_b
   +2\sum_{m=1}^3\bigl(w^{(m)}\cdot\nabla\eta(x)\bigr)\bigl(w^{(m)}\cdot\nabla\Phi_m^{\rm int}(x)\bigr)
   +\sum_{m=1}^3\Phi_m^{\rm int}(x)\,{w^{(m)}}^{\mathsf T}[\operatorname{Hess}\eta(x)]w^{(m)}.
   $$
   Applying Cauchy–Schwarz, $|w^{(m)}|\le 1$, $0\le\eta(x)\le 1$, (15), and (16) cancels $L$ and $L^2$ identically, giving across $\frac32L\le|x|\le 2L$:
   $$
   \|T^{ab}_{\rm tot}(x)\|
   \le\rho_0+2|\nabla\eta(x)|\sum_{m=1}^3|\nabla\Phi_m^{\rm int}(x)|
   +\|\operatorname{Hess}\eta(x)\|\sum_{m=1}^3|\Phi_m^{\rm int}(x)|
   \le\left(1+\frac{38}{3}F_1+\frac{64}{3}F_2\right)\rho_0=:M_{\rm st}\rho_0.
   $$
   Fix the explicit closed-form dimensionless bound $M_{\rm st}$ and collar plateau $U_{\rm col}$ by
   $$
   M_{\rm st}=1+\frac{152}{3}e^{-6/7}+\frac{2048}{3}e^{-12/7}
   +1152e^{-13/7}+\frac{16384}{3}e^{-20/7}>1,\qquad
   U_{\rm col}:=M_{\rm st}\rho_0>0,
   $$
   $$
   \boxed{\|T^{ab}_{\rm tot}(x)\|\le T^{00}_{\rm tot}(x)\qquad\forall\,x\in\mathbb R^3.} \tag{17}
   $$
   On $\frac32L\le|x|\le 2L$, (17) holds with strict positive margin $\rho_0$ because $\|T^{ab}_{\rm tot}(x)\|\le M_{\rm st}\rho_0=U_{\rm col}<\rho_0+U_{\rm col}=T^{00}_{\rm tot}(x)$. Consequently, for every future-directed causal four-vector $u^\mu=(u^0,u)$ ($u^0\ge|u|\ge 0$), the four-momentum flux $J^\mu=-T^{\mu\nu}_{\rm tot}u_\nu=(T^{00}_{\rm tot}u^0,-T^{ab}_{\rm tot}u_b)$ satisfies $|J(x)|\le\|T^{ab}_{\rm tot}(x)\||u|\le T^{00}_{\rm tot}(x)u^0=J^0(x)$, proving the full Lorentzian dominant (and hence weak and null) energy condition at every point of $\mathbb R^3$.

Static $T^{00}_{\rm tot}$ and vanishing $T^{0a}_{\rm tot}$ give $\partial_\mu T^{\mu 0}_{\rm tot}=0$, while smoothness of $\Phi_{mn}\in C_c^\infty(\mathbb R^3)$ gives $\partial_aT^{ab}_{\rm tot}=\epsilon_{akm}\epsilon_{bln}\partial_a\partial_k\partial_l\Phi_{mn}=0$ classically and distributionally on all $\mathbb R^3$, with no omitted surface delta or external force density. Integrating $\partial_k(\epsilon_{akm}\epsilon_{bln}\partial_l\Phi_{mn})$ over $B_{3L}(0)$ (where $\Phi_{mn}=0$ near $\partial B_{3L}(0)$) gives zero total spatial stress, and splitting $\mathbb R^3=\Omega\sqcup(\mathbb R^3\setminus\Omega)$ proves exact collar stress compensation:
$$
 \partial_\mu T^{\mu\nu}_{\rm tot}=0,\qquad
 \Sigma_{ab}:=\int_{\mathbb R^3}T^{ab}_{\rm tot}(x)\,d^3x=0,\qquad
 \boxed{\int_{\mathbb R^3\setminus\Omega}T^{ab}_{\rm tot}(x)\,d^3x
 =-\operatorname{diag}(E_1,E_2,0).} \tag{18}
$$

## 4. Whole-space linearized gravity, inertia and exterior stress quadrupole

Adopt the whole-space static linearized Einstein equations in harmonic (de Donder) gauge from the [closed-source active-mass note](closed_radiation_shell_mass.md) and [static stress-quadrupole example](stress_quadrupole_at_equal_energy.md),
$$
 \nabla^2\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T^{\rm tot}_{\mu\nu},\qquad
 \bar h_{\mu\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}\frac{T^{\rm tot}_{\mu\nu}(y)}{|x-y|}\,d^3y,\qquad
 \lim_{|x|\to\infty}\bar h_{\mu\nu}(x)=0,
$$
$$
 h_{\mu\nu}=\bar h_{\mu\nu}-\frac12\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta},\qquad
 \Phi_{\rm tot}(x)=-\frac12c^2h_{00}(x)
 =-\frac{G}{c^2}\int_{\mathbb R^3}\frac{\varepsilon_{\rm tot}(|y|)+\operatorname{tr}T_{\rm tot}(y)}{|x-y|}\,d^3y, \tag{19}
$$
where $T^{\rm tot}_{00}=T^{00}_{\rm tot}$, $T^{\rm tot}_{0a}=0$, and $T^{\rm tot}_{ab}=T^{ab}_{\rm tot}$. Because $T^{\rm tot}_{\mu\nu}\in C_c^\infty(\mathbb R^3)$ has support in $\overline{B_{3L}(0)}$ and $|z|^{-1}\in L^1_{\rm loc}(\mathbb R^3)$, writing $\bar h_{\mu\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|z|^{-1}T^{\rm tot}_{\mu\nu}(x-z)\,d^3z$ shows $\bar h_{\mu\nu}\in C^\infty(\mathbb R^3)$ with $|\bar h_{\mu\nu}(x)|\le\frac{4G}{c^4(|x|-3L)}\|T^{\rm tot}_{\mu\nu}\|_{L^1}\to 0$ as $|x|\to\infty$. Any difference $w_{\mu\nu}$ of two distributional solutions decaying at infinity satisfies $\nabla^2w_{\mu\nu}=0$ on $\mathbb R^3$, is smooth and harmonic by Weyl's lemma, and vanishes identically by the maximum principle. Differentiating under the $z$-integral and changing variables $y=x-z$ gives $\partial^a\bar h_{a\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|x-y|^{-1}\partial_aT^{\rm tot}_{a\nu}(y)\,d^3y=0$, while $\partial_0\bar h_{0\nu}=0$, proving $\partial^\mu\bar h_{\mu\nu}=0$ on all $\mathbb R^3$.

The total rest energy splits into the cavity two-mode ground energy $E_0$ and the strictly positive support-collar energy $E_{\rm support}$:
$$
 E_{\rm tot}:=\int_{\mathbb R^3}\varepsilon_{\rm tot}(|x|)\,d^3x
 =E_0+E_{\rm support}>E_0,\qquad
 E_{\rm support}:=\int_{\mathbb R^3\setminus\Omega}\varepsilon_{\rm tot}(|x|)\,d^3x>0.
$$
Explicitly, $E_{\rm tot}=4\pi L^3\bigl[\rho_0\int_0^3s^2\chi_{\rm out}(s)\,ds+U_{\rm col}\int_1^3s^2\chi_{\rm rise}(s)\chi_{\rm out}(s)\,ds\bigr]$, which is strictly finite and bounded between $4\pi L^3(\frac83\rho_0+\frac{37}{24}U_{\rm col})$ and $4\pi L^3(9\rho_0+\frac{26}{3}U_{\rm col})$. Under a supplied active Lorentz boost with velocity $v$ ($\beta_v=v/c$, $|\beta_v|<1$, $\gamma=(1-\beta_v^2)^{-1/2}$) along any unit axis $n$, evaluating the simultaneous-slice integrals $E'=\int_{x'^0=0}T'^{00}\,d^3x'$ and $P'_i=c^{-1}\int_{x'^0=0}T'^{0i}\,d^3x'$ via the tilted-slice measure $d^3x'=d^3x/\gamma$ from the [same-source boost companion](closed_radiation_shell_inertia.md) yields $E'=\gamma(E_{\rm tot}+\beta_v^2n_an_b\Sigma_{ab})=\gamma E_{\rm tot}$ and $P'_i=\frac{\gamma v}{c^2}E_{\rm tot}n_i$ by $\Sigma_{ab}=0$ in (18). Likewise, the $O(1/|x|)$ coefficient of $\Phi_{\rm tot}(x)$ in (19) uses $\int_{\mathbb R^3}\operatorname{tr}T_{\rm tot}\,d^3y=\delta_{ab}\Sigma_{ab}=0$, proving
$$
 M_{\rm in}:=\lim_{v\to 0}\frac{n\cdot P'}{v}=\frac{E_{\rm tot}}{c^2},\qquad
 M_{\rm active}:=\frac{1}{c^2}\int_{\mathbb R^3}\bigl(\varepsilon_{\rm tot}(|y|)+\operatorname{tr}T_{\rm tot}(y)\bigr)\,d^3y,\qquad
 \boxed{M_{\rm in}=M_{\rm active}=\frac{E_{\rm tot}}{c^2}=\frac{E_0+E_{\rm support}}{c^2}.} \tag{20}
$$
The complete monopole and boost-stress ledger separates the quantum cavity interior from the supplied classical support collar:

| Region of this one source | Energy integral | Spatial-stress integral | Spatial-trace integral | Contribution to $c^2M_{\rm active}$ |
|---|---:|---:|---:|---:|
| Cavity interior ($\Omega$) | $E_0$ | $\operatorname{diag}(E_1,E_2,0)$ | $+E_0$ | $2E_0$ |
| Support collar ($\mathbb R^3\setminus\Omega$) | $E_{\rm support}$ | $-\operatorname{diag}(E_1,E_2,0)$ | $-E_0$ | $E_{\rm support}-E_0$ |
| Complete source ($\mathbb R^3$) | $E_0+E_{\rm support}$ | $0$ | $0$ | $E_0+E_{\rm support}$ |

Thus the inertial and active gravitational monopole masses agree for the complete conserved system, and both equal $(E_0+E_{\rm support})/c^2$ rather than $E_0/c^2$ alone because the collar energy $E_{\rm support}$ gravitates and carries inertia alongside $E_0$.

Next examine parity and higher exterior multipoles. Because $2\alpha_1(x_1)=\frac{10\pi x_1}{L}+5\pi$ and $2\alpha_2(x_2)=\frac{14\pi x_2}{L}+7\pi$ differ from even multiples of $\pi$ by odd multiples of $\pi$, $\cos 2\alpha_1(x_1)=-\cos(10\pi x_1/L)=\cos 2\alpha_1(-x_1)$ and $\cos 2\alpha_2(x_2)=-\cos(14\pi x_2/L)=\cos 2\alpha_2(-x_2)$. Although the mode amplitudes $u_1,u_2$ are odd across $x_1=0$ and $x_2=0$, their quadratic stress potentials satisfy $\Phi_m^{\rm int}(-x)=\Phi_m^{\rm int}(x)$ and in fact are invariant under flipping each coordinate $x_a\mapsto -x_a$ individually. Since $|-x|=|x|$, $\Phi_{mn}(-x)=\Phi_{mn}(x)$, $T^{ab}_{\rm tot}(-x)=T^{ab}_{\rm tot}(x)$, and $\varepsilon_{\rm tot}(|-x|)=\varepsilon_{\rm tot}(|x|)$ for all $x\in\mathbb R^3$. Consequently every odd spatial moment—including the active mass dipole $c^{-2}\int_{\mathbb R^3}x_a(\varepsilon_{\rm tot}+\operatorname{tr}T_{\rm tot})\,d^3x=0$ and all odd-$2\ell+1$ exterior multipoles—vanishes identically.

Using $\epsilon_{akm}\epsilon_{aln}=\delta_{kl}\delta_{mn}-\delta_{kn}\delta_{ml}$, the spatial stress trace is $\operatorname{tr}T_{\rm tot}=\nabla^2(\operatorname{tr}\Phi)-\partial_k\partial_l\Phi_{kl}$. Evaluate the tracefree active quadrupole $Q_{ab}:=c^{-2}\int_{\mathbb R^3}P_{ab}(x)\bigl(\varepsilon_{\rm tot}(|x|)+\operatorname{tr}T_{\rm tot}(x)\bigr)\,d^3x$ with $P_{ab}(x)=3x_ax_b-|x|^2\delta_{ab}$. Spherical symmetry of $\varepsilon_{\rm tot}(|x|)$ gives $\int_{\mathbb R^3}P_{ab}(x)\varepsilon_{\rm tot}(|x|)\,d^3x=0$. Since $\partial_k\partial_lP_{ab}=3(\delta_{ak}\delta_{bl}+\delta_{bk}\delta_{al})-2\delta_{kl}\delta_{ab}$ and $\nabla^2P_{ab}=0$, integrating $\operatorname{tr}T_{\rm tot}$ twice by parts on $\mathbb R^3$ (with zero boundary terms as $\operatorname{supp}\Phi_{kl}\subseteq\overline{B_{2L}(0)}$) yields for any symmetric compactly supported Beltrami potential
$$
 Q_{ab}
 =\frac{1}{c^2}\int_{\mathbb R^3}\bigl[(\nabla^2P_{ab})\operatorname{tr}\Phi(x)-(\partial_k\partial_lP_{ab})\Phi_{kl}(x)\bigr]\,d^3x
 =\boxed{-\frac{2}{c^2}\int_{\mathbb R^3}\bigl(3\Phi_{ab}(x)-\delta_{ab}\operatorname{tr}\Phi(x)\bigr)\,d^3x.}
$$
Because $\Phi=\operatorname{diag}(\Phi_1,\Phi_2,\Phi_3)$ is diagonal, the off-diagonal active quadrupoles vanish identically, $Q_{12}=Q_{13}=Q_{23}=0$. Along the third axis, $3\Phi_{33}-\operatorname{tr}\Phi=2\Phi_3-\Phi_1-\Phi_2=\chi_{\rm st}(|x|/L)(2\Phi_3^{\rm int}-\Phi_1^{\rm int}-\Phi_2^{\rm int})\ge 0$ pointwise on all $\mathbb R^3$ by (12). Since $\chi_{\rm st}(|x|/L)=1$ on $B_{3L/2}(0)$ and $1-\cos 2\alpha_j>0$ almost everywhere there, restricting the integral to $B_{3L/2}(0)$ and using $\int_{B_R(0)}x_1^2\,d^3x=\int_{B_R(0)}x_2^2\,d^3x=\frac13\cdot 4\pi\int_0^Rr^4\,dr=\frac{4\pi}{15}R^5$ at $R=\frac32L$ ($R^5=\frac{243}{32}L^5$) together with $\rho_0L^5=(\rho_0L^3)L^2=E_0(16c^2\tau^2)=24\pi A_*c^2\tau$ gives the strict closed-form bound
$$
 -Q_{33}=\frac{2}{c^2}\int_{\mathbb R^3}\bigl(2\Phi_3(x)-\Phi_1(x)-\Phi_2(x)\bigr)\,d^3x
 >\frac{2}{c^2}\int_{B_{3L/2}(0)}(\rho_2x_1^2+\rho_1x_2^2)\,d^3x
 =\frac{81\pi}{20}\frac{\rho_0L^5}{c^2},\qquad
 \boxed{Q_{33}<-\frac{486\pi^2}{5}A_*\tau<0.} \tag{21}
$$

To isolate the gauge-invariant exterior gravitational effect of the cavity-and-collar spatial stress at fixed pointwise energy density and equal inertia, compare $T^{\mu\nu}_{\rm tot}$ against the smooth compactly supported isotropic pressureless reference tensor
$$
 T^{00}_{\rm ref}(x)=\varepsilon_{\rm tot}(|x|),\qquad
 T^{0a}_{\rm ref}(x)=T^{a0}_{\rm ref}(x)=0,\qquad
 T^{ab}_{\rm ref}(x)=0.
$$
Then $T^{\mu\nu}_{\rm ref}\in C_c^\infty(\mathbb R^3)$ obeys $\partial_\mu T^{\mu\nu}_{\rm ref}=0$, satisfies the dominant energy condition, shares the exact pointwise energy density $T^{00}_{\rm ref}=T^{00}_{\rm tot}$ on all $\mathbb R^3$, and has identical boost inertia and active monopole mass $M_{\rm in}^{\rm ref}=M_{\rm active}^{\rm ref}=E_{\rm tot}/c^2$, while $Q^{\rm ref}_{ab}=0$. In the curvature convention of the [static stress-quadrupole example](stress_quadrupole_at_equal_energy.md), $R^{(1)}_{0i0j}=-\frac12\partial_i\partial_jh_{00}=\frac{1}{c^2}\partial_i\partial_j\Phi$ is invariant under infinitesimal coordinate gauge transformations on flat spacetime. Subtracting the two potentials cancels $\varepsilon_{\rm tot}(|y|)$ (and hence $U_{\rm col}$) identically: for every $|x|>2L$, $|x-y|^{-1}$ is smooth and harmonic in $y$ on a neighborhood of $\overline{B_{2L}(0)}\supseteq\operatorname{supp}\Phi$, so integrating $\operatorname{tr}T_{\rm tot}(y)=\nabla_y^2\operatorname{tr}\Phi(y)-\sum_{m=1}^3\partial_{y_m}^2\Phi_m(y)$ twice by parts in $y$ and using $\partial_{y_m}^2(|x-y|^{-1})=\partial_{x_m}^2(|x-y|^{-1})$ gives
$$
 \Delta\Phi(x):=\Phi_{\rm tot}(x)-\Phi_{\rm ref}(x)
 =\frac{G}{c^2}\sum_{m=1}^3\int_{B_{2L}(0)}\Phi_m(y)\,
 \partial_{x_m}^2\!\left(\frac{1}{|x-y|}\right)d^3y \qquad (|x|>2L).
$$
Differentiating twice with respect to $x_3$ under the integral yields, for all $|x|>3L$ (strictly outside the support of both complete sources),
$$
 \Delta R^{(1)}_{0303}(x)
 :=R^{(1),{\rm tot}}_{0303}(x)-R^{(1),{\rm ref}}_{0303}(x)
 =\frac{G}{c^4}\sum_{m=1}^3\int_{B_{2L}(0)}\Phi_m(y)\,K_m(x,y)\,d^3y,\qquad
 K_m(x,y):=\partial_{x_3}^2\partial_{x_m}^2\!\left(\frac{1}{|x-y|}\right),
$$
where along the positive third axis $x=(0,0,r)$ ($r>3L$), writing $z=x-y=(-y_1,-y_2,r-y_3)$, $R=|z|$, and $\rho_\perp^2=y_1^2+y_2^2=R^2-z_3^2$, four direct differentiations of $R^{-1}$ give
$$
 K_m((0,0,r),y)
 =3R^{-5}-15(z_3^2+y_m^2)R^{-7}+105y_m^2z_3^2R^{-9}
 =-\frac{12}{R^5}+\frac{15\rho_\perp^2+90y_m^2}{R^7}-\frac{105y_m^2\rho_\perp^2}{R^9}
 \quad(m=1,2),
$$
$$
 K_3((0,0,r),y)=-K_1((0,0,r),y)-K_2((0,0,r),y)
 =\frac{24}{R^5}-\frac{120\rho_\perp^2}{R^7}+\frac{105\rho_\perp^4}{R^9}. \tag{22}
$$
At $y=0$, $K_1((0,0,r),0)=K_2((0,0,r),0)=-12r^{-5}$ and $K_3((0,0,r),0)=24r^{-5}$, whose contribution to $\Delta R^{(1)}_{0303}(0,0,r)$ is exactly $\frac{12G}{c^4r^5}\int_{B_{2L}(0)}(2\Phi_3-\Phi_1-\Phi_2)\,d^3y=-\frac{6GQ_{33}}{c^2r^5}$.

To bound the multipole remainder elementarily for every $r>3L$, set $\theta:=2L/r\in(0,2/3)$ and use $\Phi_m(-y)=\Phi_m(y)$ to replace $K_m((0,0,r),y)$ by $\frac12[K_m((0,0,r),y)+K_m((0,0,r),-y)]$. For $|y|\le 2L$, let $R_\pm:=|(0,0,r)\mp y|\ge r-|y|\ge r(1-\theta)>0$, so $R_\pm^2=r^2(1+u_\pm)$ with $u_\pm=\mp\frac{2y_3}{r}+\frac{|y|^2}{r^2}$ satisfying $1+u_\pm\ge(1-\theta)^2$. By Taylor's theorem at $u=0$ on $h(u)=(1+u)^{-5/2}$ ($h'(0)=-5/2$, $h''(u)=\frac{35}{4}(1+u)^{-9/2}$), for each sign there is $\xi_\pm$ between $0$ and $u_\pm$ (hence $1+\xi_\pm\ge\min(1,1+u_\pm)\ge(1-\theta)^2$) with $h(u_\pm)=1-\frac52u_\pm+\frac{35}{8}(1+\xi_\pm)^{-9/2}u_\pm^2$. Since $\frac12(u_++u_-)=|y|^2/r^2\le\theta^2$ cancels the odd $y_3$ term and $\frac12(u_+^2+u_-^2)=\frac{4y_3^2}{r^2}+\frac{|y|^4}{r^4}\le(4+\theta^2)\theta^2$,
$$
 \left|\frac{R_+^{-5}+R_-^{-5}}{2}-r^{-5}\right|
 \le r^{-5}\theta^2\left[\frac52+\frac{35}{8}(1-\theta)^{-9}(4+\theta^2)\right].
$$
In the remaining terms of (22), $0\le y_m^2\le\rho_\perp^2\le R_\pm^2$ implies $0\le\frac{15\rho_\perp^2+90y_m^2}{R_\pm^7}\le\frac{105\rho_\perp^2}{R_\pm^7}$, $0\le\frac{105y_m^2\rho_\perp^2}{R_\pm^9}\le\frac{105\rho_\perp^2}{R_\pm^7}$, and $0\le\frac{105\rho_\perp^4}{R_\pm^9}\le\frac{120\rho_\perp^2}{R_\pm^7}$; since the difference of two numbers in $[0,M]$ has absolute value at most $M$ and $\rho_\perp^2/R_\pm^7\le\theta^2r^2/[r^7(1-\theta)^7]$, the non-$R^{-5}$ part of $K_m((0,0,r),\pm y)$ is bounded in magnitude by $120r^{-5}\theta^2(1-\theta)^{-7}$ for all $m=1,2,3$. Because the $R^{-5}$ coefficients satisfy $|-12|\le 24$, every $m\in\{1,2,3\}$, $r>3L$, and $|y|\le 2L$ obeys
$$
 \left|\frac{K_m((0,0,r),y)+K_m((0,0,r),-y)}{2}-K_m((0,0,r),0)\right|
 \le r^{-5}\theta^2C(\theta),\qquad
 C(\theta):=60+105(1-\theta)^{-9}(4+\theta^2)+120(1-\theta)^{-7}.
$$
Integrating against $\sum_{m=1}^3|\Phi_m(y)|\le\sum_{m=1}^3|\Phi_m^{\rm int}(y)|<\frac43\rho_0L^2$ from (15) over $|y|\le 2L$ (volume $\frac{32\pi}{3}L^3$) gives
$$
 \left|\Delta R^{(1)}_{0303}(0,0,r)-\left(-\frac{6GQ_{33}}{c^2r^5}\right)\right|
 \le\frac{128\pi}{9}\theta^2C(\theta)\,\frac{G\rho_0L^5}{c^4r^5}\qquad(r>3L).
$$
As $r\to\infty$, $\theta=2L/r\to 0$ and $C(\theta)\to 600$, so the remainder is $O(r^{-7})$, establishing the exact asymptotic curvature contrast. Moreover, at the explicit finite exterior receiver point $p_*=(0,0,r_*)$ with $r_*=80L=320c\tau>3L$ ($\theta_*=2L/r_*=1/40$), $\frac{40}{39}<\frac{10}{9}$ and $(10/9)^3=\frac{1000}{729}<\frac75$ (since $5000<5103$) give $(1-\theta_*)^{-7}<(1-\theta_*)^{-9}<(7/5)^3=\frac{343}{125}<3$; together with $4+\theta_*^2=4+\frac{1}{1600}<\frac{41}{10}$, this gives $C(1/40)<60+315\cdot\frac{41}{10}+360=1711.5<1712$ and $\frac{128}{9}\theta_*^2C(1/40)<\frac{128\cdot 1712}{9\cdot 1600}=\frac{3424}{225}<16$. Subtracting this bound from the strict leading-term bound $-\frac{6GQ_{33}}{c^2r_*^5}>\frac{243\pi}{10}\frac{G\rho_0L^5}{c^4r_*^5}$ from (21) yields
$$
 \boxed{\lim_{r\to\infty}r^5\Delta R^{(1)}_{0303}(0,0,r)
 =-\frac{6GQ_{33}}{c^2}>\frac{2916\pi^2}{5}\frac{GA_*\tau}{c^2}>0,}
$$
$$
 \boxed{\Delta R^{(1)}_{0303}(0,0,80L)
 >\frac{83\pi}{10}\frac{G\rho_0}{80^5c^4}
 =\frac{249\pi^2}{1280\cdot 80^5}\frac{GA_*}{c^7\tau^4}>0.} \tag{23}
$$
For nearby freely falling test bodies initially at rest near $p_*=(0,0,80L)$ separated radially by $\xi^3e_3$, the corresponding leading geodesic-deviation relative-acceleration coefficient ${\cal K}=-c^2R^{(1)}_{0303}$ satisfies $\Delta{\cal K}(p_*)=-c^2\Delta R^{(1)}_{0303}(p_*)<0$ at retained linear order.

## 5. Native history bookkeeping, unit ledger and scope boundaries

The full native four-birth probability law is retained unchanged from the [finite source table](finite_interval_action_and_source_preparation.md). Conditional on the fixed prepared prefix $a\prec b$ with marks $(i,0)$ and descendant counters $(1,0)$ for $i=0,1$, the 15 predecessor-ideal pairs $(I_x,I_y)$ carry the following exact structural probability numerators over $1320$ (concatenation denotes a set):

| $I_x$ | $I_y$ | $1320P_0$ | $1320P_1$ |
|---|---|---:|---:|
| $\varnothing$ | $\varnothing$ | 6 | 6 |
| $\varnothing$ | $x$ | 6 | 6 |
| $\varnothing$ | $a$ | 5 | 10 |
| $\varnothing$ | $ab$ | 19 | 14 |
| $\varnothing$ | $ax$ | 33 | 33 |
| $\varnothing$ | $abx$ | 195 | 195 |
| $a$ | $\varnothing$ | 5 | 10 |
| $a$ | $a$ | 5 | 10 |
| $a$ | $ab$ | 19 | 14 |
| $a$ | $ax$ | 19 | 14 |
| $a$ | $abx$ | 172 | 392 |
| $ab$ | $\varnothing$ | 19 | 14 |
| $ab$ | $a$ | 19 | 14 |
| $ab$ | $ab$ | 19 | 14 |
| $ab$ | $abx$ | 779 | 574 |
| **Total** | | **1320** | **1320** |

Each structural row splits into four fair ordered suffix-mark pairs of equal conditional weight, giving 60 marked histories per preparation with denominator $5280$. Only the fifteenth row $(I_x,I_y)=(ab,abx)$ is the four-chain $a\prec b\prec x\prec y$: its structural probabilities are $779/1320$ and $574/1320$, and each of its four marked instances carries exact weight $779/5280$ and $574/5280$. The compact cavity, collar lift, and linearized gravitational source attachment in this note apply strictly to those four marked instances of the chain row without modifying or reweighting the native process. In this 3+1D gravitational source ledger, the remaining 14 non-chain structural rows retain their tabulated probabilities and carry attachment status `"unavailable"`, leaving any all-branch kinematic or positive-generator extension to separate investigation outside this note.

The normalization, unit, and weak-field relations are explicit:
$$
 F_*^2=\frac{4A_*c^2}{\kappa V\omega_2\,\beta(\sqrt2+1)}
 =\frac{A_*}{28\pi\kappa c\tau^2\,\beta(\sqrt2+1)},\qquad
 \frac{L}{c\tau}=4,\qquad
 \frac{E_0\tau}{A_*}=\frac{3\pi}{2},\qquad
 \frac{E_2}{E_1}=\frac75,
$$
$$
 \rho_0=\frac{3\pi A_*}{128c^3\tau^4},\qquad
 g:=\frac{G\rho_0L^2}{c^4}=\frac{3\pi GA_*}{8c^5\tau^2}\ll 1. \tag{24}
$$
If $\Psi$ has field units ${\cal F}$, then $B_j,q_j,F_*$ have units ${\cal F}$, $\kappa$ has units $\text{energy}/({\cal F}^2\cdot\text{length})$, $p_j$ has units $\text{action}/{\cal F}$, $\mu$ has units $\text{energy}\cdot\text{time}^2/{\cal F}^2$, every component of $T^{\mu\nu}_{\rm sc},T^{\mu\nu}_{\rm tot},T^{\mu\nu}_{\rm ref}$ and $\rho_0,U_{\rm col}$ has energy-density units $\text{energy}/\text{length}^3$, and $\Phi^{\rm int}_{mn},\Phi_{mn}$ have units $\text{energy}/\text{length}$ (force). Rescaling $\Psi\mapsto s\Psi$ and $\kappa\mapsto\kappa/s^2$ ($s>0$) rescales $B_j,F_*$ by $s$ while leaving $H_{\rm sc}$, $T^{\mu\nu}_{\rm tot}$, $M_{\rm in}$, $M_{\rm active}$, $Q_{ab}$, and $\Delta R^{(1)}_{0303}$ invariant. In the gravitational sector, $M_{\rm in}$ and $M_{\rm active}$ have mass units, $Q_{ab}$ and $A_*\tau$ have units $\text{mass}\cdot\text{length}^2$, $\bar h_{\mu\nu}$ and $h_{\mu\nu}$ are dimensionless, $\Phi_{\rm tot}$ has velocity-squared units, $R^{(1)}_{0303}$ and $GA_*/(c^7\tau^4)$ have curvature units $\text{length}^{-2}$, and $\Delta{\cal K}$ has units $\text{time}^{-2}$. Because $M_{\rm st}$ in (17) and the radial integrals of $\chi_{\rm st},\chi_{\rm rise},\chi_{\rm out}$ are fixed $O(1)$ dimensionless constants independent of $g$, the single supplied weak-field condition $g\ll 1$ in (24) keeps both the cavity interior and support-collar metric perturbations at first weak-field order, $|\bar h_{\mu\nu}|=O(g)\ll 1$, with matter held at zeroth order.

The boundary between native and externally supplied premises is strict:

- **Supplied by the native growth law:** the 15 four-birth predecessor-ideal pairs, their exact rational continuation probabilities over $1320$ and $5280$, and the chain order $a\prec b\prec x\prec y$ on the selected row.
- **Externally supplied in this conditional construction:** the continuum background $\mathbb R^{1,3}$ and signature $(-+++)$, physical parameters $c,\tau,A_*,\kappa,G$, the released two-event prefix $W_2$ and unaliased oscillator phases $(\theta_1,\theta_2)=(5\pi/4,7\pi/4)$, the centered cubic domain $\Omega$ with homogeneous Neumann boundary conditions and mode integers $(5,7)$, the zero-offset Weyl-ordered stress prescription (9), the interior probe location $x_*$, the smooth classical Beltrami support collar $\Phi_{mn}$ and radial plateau $U_{\rm col}$, the weak-field regime $g\ll 1$, and the ideal exterior tidal readout channel.

No native derivation of spacetime dimensionality, Lorentzian geometry, general relativity, physical calibration of $c,\tau,A_*,G$, or excitation rest mass is claimed. Satisfying $\partial_\mu T^{\mu\nu}_{\rm tot}=0$ and $\|T^{ab}_{\rm tot}\|\le T^{00}_{\rm tot}$ proves mathematical conservation and dominant-energy admissibility of the composite stress tensor; it does not establish a constitutive equation of state, elastic stability of a material cavity casing, nonlinear self-gravitating equilibrium, or ultraviolet renormalization of the untruncated continuum scalar vacuum. Preparing the two-mode Gaussian ground state, maintaining the Neumann boundary and collar stresses, resolving a point probe at $x_*$, sequentially accessing noncommuting samples, measuring weak exterior tidal curvature, and resetting the apparatus carry unassigned physical work and thermodynamic costs. Track-B ontology and Status-M commitments (`ONTOLOGY.md`, `GOVERNANCE.md`) remain strictly quarantined and enter no equation, variable, or inference of this calculation.

The scoped decision is therefore **compatible as an isolated whole-space linearized gravitational source on the selected four-chain row once the cubic Neumann cavity is completed by an explicit conserved support collar, with $M_{\rm in}=M_{\rm active}=(E_0+E_{\rm support})/c^2$ and strictly nonzero exterior stress-quadrupole curvature contrast**. Any downstream claim of whole-carrier cavity mass or exterior tidal response must retain the collar energy and confining stress in its complete source ledger.

## Scientific review

Compact Cavity Stress & Gravity Author derived the conditional cubic homogeneous-Neumann cavity attachment, smooth Beltrami support collar, dominant-energy bound, whole-space linearized gravitational potential, inertia–active-mass identity, and exterior stress-quadrupole tidal contrast. Independent Gravity & Cavity Reviewer independently verified every operator identity, boundary condition, radial bump bound, multipole integration by parts, fourth-derivative Newtonian kernel, finite-distance remainder, native 60-history probability table, dimensional relation, and scope boundary. Prospective protocol SHA-256 5eeb403391cb1de4968177a093c32f8eb2f499f49fa08e4be2d3575bb7c3c570; accepted author report SHA-256 55206e1d4bf2aae6c4de096ba2497d1f41d9c825462bfa832974a3e75e6d797b; independent scientific review SHA-256 60323567dbf087b43d195e3856bc86b8af80f97609c7d0090cea6961908aa0ef.
