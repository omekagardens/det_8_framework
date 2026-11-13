# An all-branch compact cavity and collar source for four-birth fields

Conditional analytic source construction

Yes. One history-independent 12-mode homogeneous-Neumann scalar field inside a centered compact cubic cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ ($L=8c\tau$, $V=L^3=512c^3\tau^3$), prepared once prior to suffix births in its unique stationary Gaussian ground state $\Omega_0\in\mathcal S(\mathbb R^{12})\subset L^2(\mathbb R^{12})$ and completed outside $\Omega$ by one history-independent smooth compactly supported Beltrami stress collar in $\overline{B_{3L}(0)}\subset\mathbb R^3$, simultaneously upgrades all 15 four-birth structural rows (all 60 marked histories per prepared source, conditional probability weight $1320/1320$) to `"available"` in the $3+1$D static linearized gravitational source ledger. Along an explicit adapted interior worldline-segment embedding in $[-\frac38L,-\frac{1}{24}L]\times\{0\}\times\{0\}\subset\operatorname{int}(\Omega)$, boundary-reflected image waves remain strictly spacelike separated from every sampled event pair across all 15 structural rows ($3\le 12+\nu_-(z_u)-\nu_+(z_v)\le 22\le 23$), cancelling identically in the discrete odd-harmonic square wave $S_{24}$ while an eight-node modulo-24 Vandermonde theorem guarantees strictly positive-definite complex and real branch covariances $W(H)\succ 0$ and $V(H)\succ 0$, positive-variance stagewise commutator zero modes, and exact stage $2\to 3$, $2\to 4$, and $3\to 4$ Weyl-algebra marginal preservation with zero feedback into the native growth law. Throughout $\Omega$, the unshifted action-derived Hamiltonian equals $H_{\rm sc}=(A_*/\tau)K$ with ground energy $E_0=27\pi A_*/\tau$, and the smooth composite source $T^{\mu\nu}_{\rm tot}\in C_c^\infty(\mathbb R^3)$ matches the ground-state cavity stress $\omega_{\rm vac}(T^{\mu\nu}_{\rm sc})$ pointwise on $\Omega$, satisfies exact whole-space conservation $\partial_\mu T^{\mu\nu}_{\rm tot}=0$ and the full Lorentzian dominant energy condition $\|T^{ab}_{\rm tot}(x)\|\le T^{00}_{\rm tot}(x)$ at every $x\in\mathbb R^3$, admits a unique decaying harmonic-gauge gravitational potential $\bar h_{\mu\nu}$ obeying $\partial^\mu\bar h_{\mu\nu}=0$, yields history-independent whole-carrier boost inertia and active monopole mass $M_{\rm in}=M_{\rm active}=(E_0+E_{\rm support})/c^2$ across all 60 marked histories without history-dependent re-preparation, and produces an axisymmetric prolate active stress quadrupole $Q_{11}=-2Q_{22}=-2Q_{33}>0$ with strictly nonzero gauge-invariant exterior tidal curvature contrast both asymptotically and at $p_*=(80L,0,0)$.

This is a conditional $3+1$D spacetime, positive-generator, and static first-order linearized gravitational source attachment on a prescribed flat Minkowski background. It is not a derivation of native spatial geometry or general relativity, a constitutive equation of state or mechanical realization of a material cavity wall, a nonlinear self-gravitating equilibrium, an ultraviolet renormalization of the untruncated continuum scalar vacuum, or an operational preparation, sequential readout, and reset budget.

In the [compact four-chain cavity source](compact_cavity_source_for_four_chain_field.md) (lifting the [periodic scalar source lift](local_scalar_source_for_four_chain_field.md) and [stationary four-chain dynamics](stationary_dynamics_for_four_chain_fields.md)), whole-space $3+1$D static gravitational sourcing was established exclusively on the total-chain structural row $a\prec b\prec x\prec y$ ($779/1320$ under $P_0$ and $574/1320$ under $P_1$), leaving the remaining 14 non-chain structural rows tagged `"unavailable"` because single-point spatial sampling cannot realize incomparable pairs. Conversely, the [all-branch $1+1$D wavefield extension](spacelike_branch_extension_for_four_birth_fields.md) realized all 15 structural rows ($1320/1320$) on an anti-periodic $1+1$D cylinder $\mathbb R\times S_L^1$—resolving the stagewise spectral obstruction in the [spectral covariance obstruction](spectral_covariance_under_native_growth.md) and upgrading the abstract three-pair [kinematic Gaussian field-transport construction](gaussian_field_transport_on_native_histories.md) to a positive stationary generator—without supplying a $3+1$D compact cavity, stress-energy tensor, or whole-space gravitational field. The native continuation weights and mark rules are retained unchanged from the [finite interval and source specification](finite_interval_action_and_source_preparation.md) and [prepared source ledger](native_source_readout_response.md), and the whole-space harmonic-gauge gravitational, simultaneous-slice boost-inertia, and Beltrami stress conventions follow the [closed-source active-mass note](closed_radiation_shell_mass.md), its [same-source boost companion](closed_radiation_shell_inertia.md), and the [static stress-quadrupole construction](stress_quadrupole_at_equal_energy.md).

---

## 1. Twelve-mode cubic homogeneous-Neumann cavity field and readout calibration

Retain the target-first Johnston causal commutator convention of the [kinematic Gaussian field-transport construction](gaussian_field_transport_on_native_histories.md) and [all-branch $1+1$D wavefield extension](spacelike_branch_extension_for_four_birth_fields.md) (transposing the source-first indexing of Johnston, arXiv:0909.0944v2, §II Eqs. (18)–(23)). On any realized four-element strict partial order $(\{a,b,x,y\},\prec)$ of a marked history $H$, set $c_{rs}(H):=\mathbf 1_{\{s\prec r\}}$ and $D_{rs}(H):=\beta\bigl(c_{rs}(H)-c_{sr}(H)\bigr)$ for a single supplied $\beta>0$, writing $r\parallel s$ when $r\ne s$, $r\not\prec s$, and $s\not\prec r$. The required operator commutator is
$$
[\phi_r(H),\phi_s(H)]=iD_{rs}(H)I=i\beta\bigl(c_{rs}(H)-c_{sr}(H)\bigr)I=
\begin{cases}
+i\beta I,& s\prec r,\\
-i\beta I,& r\prec s,\\
0,& r\parallel s\ \text{or}\ r=s.
\end{cases}
\tag{1}
$$

To accommodate both direct lightcone separations and cavity-wall reflections within a single odd-harmonic square-wave window, fix $N=24$ and $M=12$ ($N=2M$) and define for $m=0,1,\ldots,11$ the discrete angles, positive cotangent weights, reflected frequencies, and odd-harmonic sine sum
$$
\varphi_m:=\frac{(2m+1)\pi}{24},\qquad
c_m:=\frac{1}{12}\cot\!\left(\frac{\varphi_m}{2}\right)=\frac{1}{12}\cot\!\left(\frac{(2m+1)\pi}{48}\right)>0,
$$
$$
\tilde\varphi_m:=2\pi-\varphi_m=\frac{(47-2m)\pi}{24}\in(\pi,2\pi),\qquad
\theta_m:=3\tilde\varphi_m=\frac{(47-2m)\pi}{8}>0,
$$
$$
S_{24}(\nu):=\sum_{m=0}^{11}c_m\sin(\nu\varphi_m)=
\begin{cases}
+1,& \nu\in\{1,2,\ldots,23\},\\
0,& \nu\in\{0,24\},\\
-1,& \nu\in\{-23,\ldots,-2,-1\},
\end{cases}
\tag{2}
$$
extended $48$-periodically by $S_{24}(\nu+48)=S_{24}(\nu)$. Because $1\le 2m+1\le 23$, every half-angle satisfies $\frac{\varphi_m}{2}\in[\frac{\pi}{48},\frac{23\pi}{48}]\subset(0,\frac\pi2)$, where $\sin$ and $\cos$ are strictly positive; hence $c_m>0$ for all $m=0,\ldots,11$, with reciprocal pairing $12^2c_m c_{11-m}=\cot\bigl(\frac{(2m+1)\pi}{48}\bigr)\cot\bigl(\frac{\pi}{2}-\frac{(2m+1)\pi}{48}\bigr)=1$. To verify the exact square-wave values in (2) from first principles, note first that $(\nu+48)\varphi_m=\nu\varphi_m+2(2m+1)\pi$ gives $S_{24}(\nu+48)=S_{24}(\nu)$, oddness of $\sin$ gives $S_{24}(-\nu)=-S_{24}(\nu)$, and $\sin(0)=\sin((2m+1)\pi)=0$ gives $S_{24}(0)=S_{24}(24)=0$. For $\nu\in\{1,\ldots,23\}$ and any $\varphi\in(0,2\pi)$, telescoping $2\sin(\varphi/2)\cos(k\varphi)=\sin\bigl((k+\tfrac12)\varphi\bigr)-\sin\bigl((k-\tfrac12)\varphi\bigr)$ over $k=1,\ldots,\nu-1$ yields
$$
\sin\!\left(\frac{\varphi}{2}\right)\left[1+2\sum_{k=1}^{\nu-1}\cos(k\varphi)+\cos(\nu\varphi)\right]
=\sin\!\left(\Bigl(\nu-\frac12\Bigr)\varphi\right)+\sin\!\left(\frac{\varphi}{2}\right)\cos(\nu\varphi)
=\sin(\nu\varphi)\cos\!\left(\frac{\varphi}{2}\right),
$$
so $\cot(\varphi/2)\sin(\nu\varphi)=1+2\sum_{k=1}^{\nu-1}\cos(k\varphi)+\cos(\nu\varphi)$. For each $k\in\{1,\ldots,23\}$, $0<\frac{k\pi}{24}<\pi$ gives $\sin(k\pi/24)>0$, and telescoping in $m$ yields
$$
2\sin\!\left(\frac{k\pi}{24}\right)\sum_{m=0}^{11}\cos(k\varphi_m)
=\sum_{m=0}^{11}\left[\sin\!\left(\frac{k(2m+2)\pi}{24}\right)-\sin\!\left(\frac{k(2m)\pi}{24}\right)\right]
=\sin(k\pi)-\sin(0)=0,
$$
whence $\sum_{m=0}^{11}\cos(k\varphi_m)=0$ for all $k\in\{1,\ldots,23\}$. Summing the cotangent identity over $m=0,\ldots,11$ therefore gives $S_{24}(\nu)=\frac{1}{12}\sum_{m=0}^{11}1=1$ for every $\nu\in\{1,\ldots,23\}$, and oddness gives $S_{24}(\nu)=-1$ for $\nu\in\{-23,\ldots,-1\}$.

Supply flat Cartesian coordinates $(x^0,x_1,x_2,x_3)$ on $\mathbb R^{1,3}$ with $x^0=ct$, metric $\eta=\operatorname{diag}(-1,1,1,1)$, orthonormal spatial basis $e_1,e_2,e_3$, and physical constants $c,\tau,A_*,\kappa>0$ denoting propagation speed, tick duration, action reference, and $3+1$D scalar kinetic normalization. Define the centered compact cubic cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ of side length $L$ and volume $V=L^3$, together with the 12 smooth axial profiles ($m=0,1,\ldots,11$)
$$
\boxed{L:=8c\tau,\qquad V:=L^3=512c^3\tau^3,}
$$
$$
k_m:=\frac{(47-2m)\pi}{L},\qquad
\omega_m:=ck_m=\frac{(47-2m)\pi}{8\tau}=\frac{\theta_m}{\tau},\qquad
\alpha_m(x_1):=k_m\!\left(x_1+\frac{L}{2}\right),\qquad
u_m(x):=\cos\alpha_m(x_1),
$$
$$
\int_\Omega u_m(x)u_{m'}(x)\,d^3x=\frac{V}{2}\delta_{mm'},\qquad
\int_\Omega\nabla u_m(x)\cdot\nabla u_{m'}(x)\,d^3x=\frac{V}{2}k_m^2\delta_{mm'}.
\tag{3}
$$
Every odd integer $n_m:=47-2m\in\{25,27,\ldots,47\}$ satisfies $\omega_m=ck_m=\theta_m/\tau$ under the single compatibility relation $L=8c\tau$ in (3). Because $\nabla u_m(x)=-k_m\sin\alpha_m(x_1)\,e_1$ and $\nabla^2 u_m(x)=-k_m^2u_m(x)$, checking all six faces of $\partial\Omega$ directly gives: on $x_1=-L/2$ ($n=-e_1$), $\alpha_m(-L/2)=0$ so $n\cdot\nabla u_m=k_m\sin 0=0$; on $x_1=+L/2$ ($n=+e_1$), $\alpha_m(L/2)=n_m\pi$ so $n\cdot\nabla u_m=-k_m\sin(n_m\pi)=0$; and on $x_2=\pm L/2$ ($n=\pm e_2$) and $x_3=\pm L/2$ ($n=\pm e_3$), $\partial_2u_m=\partial_3u_m=0$ identically. Thus every $u_m$ satisfies $-\nabla^2 u_m=k_m^2u_m$ on $\Omega$ and the homogeneous Neumann condition $n\cdot\nabla u_m=0$ on all six faces of $\partial\Omega$. Setting $s=\frac{\pi}{L}(x_1+L/2)\in[0,\pi]$ ($dx_1=\frac{L}{\pi}\,ds$, $\alpha_m=n_ms$), each mode has zero spatial mean $\int_\Omega u_m\,d^3x=\frac{V}{\pi n_m}[\sin(n_ms)]_0^\pi=0$ (equivalently $u_m(-x)=-u_m(x)$ since $\alpha_m(-x_1)=n_m\pi-\alpha_m(x_1)$ with $n_m$ odd). Moreover, because $n_m+n_{m'}\ge 50$ is a positive integer and $n_m-n_{m'}=2(m'-m)$ vanishes if and only if $m=m'$, integrating $2\cos(n_ms)\cos(n_{m'}s)=\cos((n_m-n_{m'})s)+\cos((n_m+n_{m'})s)$ and $2\sin(n_ms)\sin(n_{m'}s)=\cos((n_m-n_{m'})s)-\cos((n_m+n_{m'})s)$ over $s\in[0,\pi]$ establishes both orthogonality relations in (3).

Take the minimally coupled scalar action on $[t_1,t_2]\times\Omega$,
$$
\mathcal S_{\rm cav}[\Phi_{\rm sc}]=\frac{\kappa}{2}\int_{t_1}^{t_2}dt\int_\Omega d^3x
\left[\frac{\dot\Phi_{\rm sc}^2}{c^2}-|\nabla\Phi_{\rm sc}|^2\right],
$$
$$
\delta\mathcal S_{\rm cav}
=\kappa\int_{t_1}^{t_2}dt\int_\Omega d^3x\,\bigl(-c^{-2}\ddot\Phi_{\rm sc}+\nabla^2\Phi_{\rm sc}\bigr)\delta\Phi_{\rm sc}
-\kappa\int_{t_1}^{t_2}dt\int_{\partial\Omega}(n\cdot\nabla\Phi_{\rm sc})\,\delta\Phi_{\rm sc}\,dS,
\tag{4}
$$
for smooth variations $\delta\Phi_{\rm sc}$ on $[t_1,t_2]\times\overline\Omega$ vanishing at $t=t_1,t_2$ (the twelve edges and eight corners of $\partial\Omega$ having zero two-dimensional surface area). Under $n\cdot\nabla\Phi_{\rm sc}=0$ on $\partial\Omega$, the boundary integral vanishes without Dirichlet restriction on $\delta\Phi_{\rm sc}|_{\partial\Omega}$, yielding $(c^{-2}\partial_t^2-\nabla^2)\Phi_{\rm sc}=0$ on $\Omega$. Restricting $\mathcal S_{\rm cav}$ to the 12-mode subspace $\Phi_{\rm sc}(t,x)=\sum_{m=0}^{11}q_m(t)u_m(x)$ via (3) produces the decoupled oscillator Lagrangian $\mathcal L_{\rm red}=\sum_{m=0}^{11}\frac{\mu}{2}(\dot q_m^2-\omega_m^2q_m^2)$ with generalized mode inertia $\mu:=\frac{\kappa V}{2c^2}$ and canonical momenta $p_m:=\mu\dot q_m$.

On the Hilbert space $\mathcal H=L^2(\mathbb R^{12})$ in Schrödinger coordinates $\mathsf q=(\mathsf q_0,\ldots,\mathsf q_{11})\in\mathbb R^{12}$ with common dense invariant Schwartz domain $\mathcal S(\mathbb R^{12})$, let $(Q_m\psi)(\mathsf q)=\mathsf q_m\psi(\mathsf q)$ and $(P_m\psi)(\mathsf q)=-i\partial_{\mathsf q_m}\psi(\mathsf q)$ ($m=0,\ldots,11$), satisfying $[Q_m,P_{m'}]=i\delta_{mm'}I$ and $[Q_m,Q_{m'}]=[P_m,P_{m'}]=0$ on $\mathcal S(\mathbb R^{12})$. Define on $\mathcal S(\mathbb R^{12})$
$$
B_m:=\sqrt{\frac{2A_*c^2}{\kappa V\omega_m}}>0,\qquad
X_m(t):=Q_m\cos(\omega_mt)+P_m\sin(\omega_mt),\qquad
Y_m(t):=P_m\cos(\omega_mt)-Q_m\sin(\omega_mt),
$$
$$
q_m(t):=B_mX_m(t),\qquad
p_m(t):=\mu B_m\omega_mY_m(t),\qquad
\Phi_{\rm sc}(t,x):=\sum_{m=0}^{11}B_mu_m(x)X_m(t),
$$
$$
[\Phi_{\rm sc}(t,x),\Pi_{\rm sc}(t,y)]=iA_*\frac{2}{V}\sum_{m=0}^{11}u_m(x)u_m(y)\,I
\qquad\left(\Pi_{\rm sc}:=\frac{\kappa}{c^2}\dot\Phi_{\rm sc},\ x,y\in\Omega\right).
\tag{5}
$$
Because $[X_m(t),Y_{m'}(t)]=i\delta_{mm'}I$ and $\mu B_m^2\omega_m=A_*$, the mode pairs satisfy $[q_m(t),p_{m'}(t)]=iA_*\delta_{mm'}I$ and $[q_m(t),q_{m'}(t)]=[p_m(t),p_{m'}(t)]=0$ on $\mathcal S(\mathbb R^{12})$, while $[\Phi_{\rm sc}(t,x),\Pi_{\rm sc}(t,y)]$ is $iA_*$ times the $L^2(\Omega)$-orthogonal projection kernel onto $\operatorname{span}\{u_0,\ldots,u_{11}\}$. Integrating the Hamiltonian density $\mathcal H_{\rm sc}(t,x):=\frac{\kappa}{2}\bigl[c^{-2}\dot\Phi_{\rm sc}(t,x)^2+|\nabla\Phi_{\rm sc}(t,x)|^2\bigr]$ over $\Omega$ via (3) and applying the exact operator-ordering identity $X_m(t)^2+Y_m(t)^2=Q_m^2+P_m^2+\cos(\omega_mt)\sin(\omega_mt)(Q_mP_m+P_mQ_m-P_mQ_m-Q_mP_m)=Q_m^2+P_m^2$ on $\mathcal S(\mathbb R^{12})$ yields
$$
K:=\frac{1}{2}\sum_{m=0}^{11}\theta_m\bigl(Q_m^2+P_m^2\bigr),\qquad
H_{\rm sc}:=\int_\Omega\mathcal H_{\rm sc}(t,x)\,d^3x
=\sum_{m=0}^{11}\frac{\kappa VB_m^2\omega_m^2}{4c^2}\bigl(X_m(t)^2+Y_m(t)^2\bigr)
=\frac{1}{2}\sum_{m=0}^{11}A_*\omega_m\bigl(Q_m^2+P_m^2\bigr)
=\boxed{\frac{A_*}{\tau}K,}
$$
$$
\Omega_0(\mathsf q):=\pi^{-3}\exp\!\left(-\frac{1}{2}\sum_{m=0}^{11}\mathsf q_m^2\right),\qquad
K\Omega_0=27\pi\,\Omega_0,\qquad
E_0:=\omega_{\rm vac}(H_{\rm sc})=\frac{27\pi A_*}{\tau}>0,
\tag{6}
$$
where $\omega_{\rm vac}(A):=\langle\Omega_0,A\Omega_0\rangle$ denotes expectation in the unique normalized ground state $\Omega_0\in\mathcal S(\mathbb R^{12})$ of $K$ (so $\omega_0=\theta_0/\tau=47\pi/(8\tau)$ always denotes the $m=0$ mode angular frequency). Because $\theta_m>0$ for each $m$, $K$ is symmetric, strictly positive, and essentially self-adjoint on $\mathcal S(\mathbb R^{12})$, diagonalized by the 12-fold Hermite basis with eigenvalues $\sum_{m=0}^{11}\theta_m(\ell_m+\tfrac12)$ ($\ell_m\in\mathbb Z_{\ge 0}$), ground eigenvalue $\frac12\sum_{m=0}^{11}\frac{(47-2m)\pi}{8}=\frac{432\pi}{16}=27\pi$, and lowest excitation gap $\theta_{11}=\frac{25\pi}{8}>0$. No normal-ordering subtraction or identity offset $CI$ enters (6). On $\mathcal S(\mathbb R^{12})$, $[iK,Q_m]=\theta_mP_m$ and $[iK,P_m]=-\theta_mQ_m$ integrate to $e^{itH_{\rm sc}/A_*}\Phi_{\rm sc}(0,x)e^{-itH_{\rm sc}/A_*}=e^{i(t/\tau)K}\Phi_{\rm sc}(0,x)e^{-i(t/\tau)K}=\Phi_{\rm sc}(t,x)$, while $e^{-itH_{\rm sc}/A_*}\Omega_0=e^{-iE_0t/A_*}\Omega_0$ makes $\omega_{\rm vac}$ stationary with $\omega_{\rm vac}(Q_m^2)=\omega_{\rm vac}(P_m^2)=\frac12$, $\omega_{\rm vac}(Q_mP_m)=+\frac{i}{2}$, $\omega_{\rm vac}(P_mQ_m)=-\frac{i}{2}$, $\omega_{\rm vac}(\{Q_m,P_m\})=0$, and zero cross-mode contractions.

As in the [all-branch $1+1$D wavefield extension](spacelike_branch_extension_for_four_birth_fields.md), across spatially separated sampling points the action-normalized amplitudes $B_m\propto\omega_m^{-1/2}$ are not proportional by a single scalar to the commutator-calibrated weights $\sqrt{2\beta c_m}$ because $c_m\theta_m$ varies with $m$. Define on $\mathcal S(\mathbb R^{12})$ the dimensionless 12-mode cavity field $\Psi(t,x)$, the calibrated physical field $\Psi_{\rm cal}(t,x)$ with field unit $F_*>0$ normalized to unit gain at $m=0$, the dimensionless mode-gain ratios $\eta_m>0$, and the symmetric Neumann-cosine readout kernel $\Gamma_{\rm read}(x,y)$ on $\Omega\times\Omega$:
$$
\Psi(t,x):=\sum_{m=0}^{11}\sqrt{2\beta c_m}\,u_m(x)X_m(t),\qquad
\Psi_{\rm cal}(t,x):=F_*\Psi(t,x)=F_*\sum_{m=0}^{11}\sqrt{2\beta c_m}\,u_m(x)X_m(t),
$$
$$
F_*:=\frac{B_0}{\sqrt{2\beta c_0}}=\sqrt{\frac{A_*c^2}{\kappa V\omega_0\beta c_0}}>0,\qquad
\eta_m:=\frac{F_*\sqrt{2\beta c_m}}{B_m}=\sqrt{\frac{c_m\theta_m}{c_0\theta_0}}>0\quad(m=0,\ldots,11),
$$
$$
\Gamma_{\rm read}(x,y):=\frac{2}{V}\sum_{m=0}^{11}\eta_m u_m(x)u_m(y),\qquad
\int_\Omega\Gamma_{\rm read}(x,y)\,\Phi_{\rm sc}(t,y)\,d^3y=\Psi_{\rm cal}(t,x).
\tag{7}
$$
Integrating $\Gamma_{\rm read}(x,y)\Phi_{\rm sc}(t,y)$ over $y\in\Omega$ via $\int_\Omega u_m(y)u_{m'}(y)\,d^3y=\frac{V}{2}\delta_{mm'}$ in (3) cancels $\frac{2}{V}\cdot\frac{V}{2}=1$ mode by mode, giving $\sum_{m=0}^{11}\eta_mB_mu_m(x)X_m(t)=F_*\sum_{m=0}^{11}\sqrt{2\beta c_m}\,u_m(x)X_m(t)=\Psi_{\rm cal}(t,x)$ identically, while the inverse kernel $\Gamma_{\rm read}^{-1}(x,y):=\frac{2}{V}\sum_{m=0}^{11}\eta_m^{-1}u_m(x)u_m(y)$ recovers $\Phi_{\rm sc}(t,\cdot)$ from $\Psi_{\rm cal}(t,\cdot)$ on $\operatorname{span}\{u_0,\ldots,u_{11}\}$. Both $\Phi_{\rm sc}$ and $\Psi_{\rm cal}$ satisfy $(c^{-2}\partial_t^2-\nabla^2)(\cdot)=0$ in $\Omega$, $n\cdot\nabla(\cdot)=0$ on $\partial\Omega$, and Heisenberg evolution under the single unshifted Hamiltonian $H_{\rm sc}=(A_*/\tau)K$.

---

## 2. Offset interior causal embedding and method-of-images wall cancellation

Retain the minimal-denominator ($q=3$) online adapted causal embedding $z_r=(\tau_r,\xi_r)\in\frac13\mathbb Z^2$ ($r\in\{a,b,x,y\}$) established in Section 2 of the [all-branch $1+1$D wavefield extension](spacelike_branch_extension_for_four_birth_fields.md), with fixed prepared prefix $z_a=(0,0)$, $z_b=(1,0)$, stage-3 map $z_x(\varnothing)=(1/3,4/3)$, $z_x(\{a\})=(1,2/3)$, $z_x(\{a,b\})=(2,0)$, and stage-4 map $z_y(I_x,I_y)$ tabulated in Table 1 below. For any $z=(\tau_*,\xi_*)\in\frac13\mathbb Z^2$, in integer lightcone coordinates
$$
\nu_+(z):=3(\tau_*-\xi_*)\in\mathbb Z,\qquad
\nu_-(z):=3(\tau_*+\xi_*)\in\mathbb Z,\qquad
1\le\bigl|\nu_\pm(z_r-z_s)\bigr|\le 9\quad(r\ne s),
$$
$$
s\prec r\iff\nu_\pm(z_r-z_s)\ge 1,\qquad
r\prec s\iff\nu_\pm(z_r-z_s)\le -1,\qquad
r\parallel s\iff\nu_+(z_r-z_s)\nu_-(z_r-z_s)<0
\tag{8}
$$
hold across all 15 structural rows and all 90 unordered vertex pairs $r\ne s$.

Embed $z_r=(\tau_r,\xi_r)$ into the open $3+1$D cavity spacetime $\mathbb R\times\operatorname{int}(\Omega)$ along the offset axial worldline segment centered at $x_{\rm ref}=(-L/4,0,0)$:
$$
t_r:=\tau_r\tau,\qquad
x_r:=\left(-\frac{L}{4}+\xi_rc\tau,\,0,\,0\right)=\left(\frac{\xi_r-2}{8}L,\,0,\,0\right)\in\left[-\frac{3}{8}L,\,-\frac{1}{24}L\right]\times\{0\}\times\{0\}\subset\operatorname{int}(\Omega),
$$
$$
\phi_a:=\Psi(t_a,x_a),\qquad
\phi_b:=\Psi(t_b,x_b),\qquad
\phi_x(H):=\Psi(t_x,x_x),\qquad
\phi_y(H):=\Psi(t_y,x_y),\qquad
\Psi_{\rm cal}(t_r,x_r)=F_*\phi_r(H).
\tag{9}
$$
Across all 15 structural rows in Table 1, $\xi_r$ ranges between $\min\xi_r=-1$ (attained by $y$ on Rows 1 and 7, giving $x_{y,1}=-\frac38L>-\frac12L$, at strict distance $\frac18L=c\tau$ from the left wall $x_1=-L/2$) and $\max\xi_r=+\frac53$ (attained by $y$ on Row 12, giving $x_{y,1}=-\frac{1}{24}L<0<\frac12L$, at strict distance $\frac{13}{24}L=\frac{13}{3}c\tau$ from the right wall $x_1=+L/2$), while $x_{r,2}=x_{r,3}=0\in(-L/2,L/2)$. Every sampled event therefore lies strictly inside the left half of $\operatorname{int}(\Omega)$, and $\phi_x(H)$ depends only on $I_x$ while $\phi_y(H)$ depends only on $(I_x,I_y)$.

| Row | $I_x$ | $I_y$ | $z_x(I_x)$ | $z_y(I_x,I_y)$ | $(\nu_+(z_x),\nu_-(z_x))$ | $(\nu_+(z_y),\nu_-(z_y))$ | $[\min\mu_-,\max\mu_-]$ | $(a_a,a_b,a_x,a_y;\,b_a,b_b,b_x,b_y)\bmod 24$ |
|---:|---|---|---|---|---|---|---|---|
| 1 | $\varnothing$ | $\varnothing$ | $(1/3,4/3)$ | $(1/3,-1)$ | $(-3,+5)$ | $(+4,-2)$ | $[6,\,20]$ | $(6,3,9,2;\,18,15,13,20)$ |
| 2 | $\varnothing$ | $x$ | $(1/3,4/3)$ | $(2/3,4/3)$ | $(-3,+5)$ | $(-2,+6)$ | $[9,\,21]$ | $(6,3,9,8;\,18,15,13,12)$ |
| 3 | $\varnothing$ | $a$ | $(1/3,4/3)$ | $(1,-1/3)$ | $(-3,+5)$ | $(+4,+2)$ | $[8,\,20]$ | $(6,3,9,2;\,18,15,13,16)$ |
| 4 | $\varnothing$ | $ab$ | $(1/3,4/3)$ | $(4/3,0)$ | $(-3,+5)$ | $(+4,+4)$ | $[8,\,20]$ | $(6,3,9,2;\,18,15,13,14)$ |
| 5 | $\varnothing$ | $ax$ | $(1/3,4/3)$ | $(4/3,1)$ | $(-3,+5)$ | $(+1,+7)$ | $[9,\,22]$ | $(6,3,9,5;\,18,15,13,11)$ |
| 6 | $\varnothing$ | $abx$ | $(1/3,4/3)$ | $(2,1/3)$ | $(-3,+5)$ | $(+5,+7)$ | $[7,\,22]$ | $(6,3,9,1;\,18,15,13,11)$ |
| 7 | $a$ | $\varnothing$ | $(1,2/3)$ | $(1/3,-1)$ | $(+1,+5)$ | $(+4,-2)$ | $[6,\,17]$ | $(6,3,5,2;\,18,15,13,20)$ |
| 8 | $a$ | $a$ | $(1,2/3)$ | $(1,-2/3)$ | $(+1,+5)$ | $(+5,+1)$ | $[7,\,17]$ | $(6,3,5,1;\,18,15,13,17)$ |
| 9 | $a$ | $ab$ | $(1,2/3)$ | $(4/3,0)$ | $(+1,+5)$ | $(+4,+4)$ | $[8,\,17]$ | $(6,3,5,2;\,18,15,13,14)$ |
| 10 | $a$ | $ax$ | $(1,2/3)$ | $(5/3,1)$ | $(+1,+5)$ | $(+2,+8)$ | $[9,\,20]$ | $(6,3,5,4;\,18,15,13,10)$ |
| 11 | $a$ | $abx$ | $(1,2/3)$ | $(2,0)$ | $(+1,+5)$ | $(+6,+6)$ | $[6,\,18]$ | $(6,3,5,0;\,18,15,13,12)$ |
| 12 | $ab$ | $\varnothing$ | $(2,0)$ | $(1,5/3)$ | $(+6,+6)$ | $(-2,+8)$ | $[6,\,22]$ | $(6,3,0,8;\,18,15,12,10)$ |
| 13 | $ab$ | $a$ | $(2,0)$ | $(4/3,1)$ | $(+6,+6)$ | $(+1,+7)$ | $[6,\,19]$ | $(6,3,0,5;\,18,15,12,11)$ |
| 14 | $ab$ | $ab$ | $(2,0)$ | $(2,1/3)$ | $(+6,+6)$ | $(+5,+7)$ | $[6,\,19]$ | $(6,3,0,1;\,18,15,12,11)$ |
| 15 | $ab$ | $abx$ | $(2,0)$ | $(3,0)$ | $(+6,+6)$ | $(+9,+9)$ | $[3,\,21]$ | $(6,3,0,21;\,18,15,12,9)$ |

**Table 1.** Adapted $\frac13\mathbb Z^2$ coordinates (with $(\nu_+(z_a),\nu_-(z_a))=(0,0)$ and $(\nu_+(z_b),\nu_-(z_b))=(+3,+3)$ on every row), exact row-wise extremal intervals $[\min_{u,v}\mu_-(u,v),\max_{u,v}\mu_-(u,v)]$ for $\mu_-(u,v)=12+\nu_-(z_u)-\nu_+(z_v)$ over $(u,v)\in\{a,b,x,y\}^2$, and the eight modulo-24 Vandermonde exponents of Section 3.

**Theorem 1 (Method-of-images causal wall cancellation across all 15 rows).** *Along the interior cavity embedding (9), every pair $(r,s)\in\{a,b,x,y\}^2$ on every one of the 15 structural rows (all 60 marked histories $H$) satisfies (1) identically, $[\phi_r(H),\phi_s(H)]=+i\beta\bigl(c_{rs}(H)-c_{sr}(H)\bigr)I$, with exact unit normalization $\beta$.*

*Proof.* On $\mathcal S(\mathbb R^{12})$, direct canonical commutation of $X_m(t)=Q_m\cos(\omega_mt)+P_m\sin(\omega_mt)$ gives $[X_m(t_r),X_{m'}(t_s)]=i\delta_{mm'}\bigl(\cos(\omega_mt_r)\sin(\omega_mt_s)-\sin(\omega_mt_r)\cos(\omega_mt_s)\bigr)I=-i\delta_{mm'}\sin\bigl(\omega_m(t_r-t_s)\bigr)I$. Substituting $\Psi(t,x)=\sum_{m=0}^{11}\sqrt{2\beta c_m}\,u_m(x)X_m(t)$ from (7) yields
$$
[\phi_r(H),\phi_s(H)]=i\beta\sum_{m=0}^{11}c_m\Bigl[-2u_m(x_r)u_m(x_s)\sin\bigl(\omega_m(t_r-t_s)\bigr)\Bigr]I.
$$
Write $\Delta_m:=\omega_m(t_r-t_s)=3\tilde\varphi_m(\tau_r-\tau_s)$ and $\alpha_{m,r}:=\alpha_m(x_{r,1})$. Because $x_{r,1}+\frac{L}{2}=\frac{L}{4}+\xi_rc\tau=(2+\xi_r)c\tau$ and $k_mc\tau=\omega_m\tau=\theta_m=3\tilde\varphi_m$, we have $\alpha_{m,r}=3\tilde\varphi_m(2+\xi_r)=(6+3\xi_r)\tilde\varphi_m$. Applying $2\cos\alpha_{m,r}\cos\alpha_{m,s}=\cos(\alpha_{m,r}-\alpha_{m,s})+\cos(\alpha_{m,r}+\alpha_{m,s})$ followed by $2\sin\Delta_m\cos B=\sin(\Delta_m-B)+\sin(\Delta_m+B)$ gives
$$
\begin{aligned}
4u_m(x_r)u_m(x_s)\sin\Delta_m
&=\sin\bigl(\Delta_m-(\alpha_{m,r}-\alpha_{m,s})\bigr)+\sin\bigl(\Delta_m+(\alpha_{m,r}-\alpha_{m,s})\bigr)\\
&\quad+\sin\bigl(\Delta_m-(\alpha_{m,r}+\alpha_{m,s})\bigr)+\sin\bigl(\Delta_m+(\alpha_{m,r}+\alpha_{m,s})\bigr).
\end{aligned}
$$
In terms of $\nu_\pm(z)=3(\tau_*\mp\xi_*)\in\mathbb Z$, the four phase arguments equal $\tilde\varphi_m\nu_+(z_r-z_s)$, $\tilde\varphi_m\nu_-(z_r-z_s)$, $\tilde\varphi_m\mu_+(r,s)$, and $\tilde\varphi_m\mu_-(r,s)$, where
$$
\mu_-(r,s):=12+\nu_-(z_r)-\nu_+(z_s)\in\mathbb Z,\qquad
\mu_+(r,s):=-12+\nu_+(z_r)-\nu_-(z_s)=-\bigl(12+\nu_-(z_s)-\nu_+(z_r)\bigr)=-\mu_-(s,r)\in\mathbb Z,
$$
$$
-2u_m(x_r)u_m(x_s)\sin\bigl(\omega_m(t_r-t_s)\bigr)
=\frac{1}{2}\Bigl[\sin\bigl(\nu_+(z_r-z_s)\varphi_m\bigr)+\sin\bigl(\nu_-(z_r-z_s)\varphi_m\bigr)
+\sin\bigl(\mu_+(r,s)\varphi_m\bigr)+\sin\bigl(\mu_-(r,s)\varphi_m\bigr)\Bigr],
\tag{10}
$$
using $-\sin(\tilde\varphi_m k)=-\sin(2\pi k-k\varphi_m)=+\sin(k\varphi_m)$ for every integer $k\in\mathbb Z$. Summing (10) against $i\beta c_m$ over $m=0,\ldots,11$ splits $[\phi_r(H),\phi_s(H)]$ into the direct wave commutator plus the boundary-reflection image commutator:
$$
[\phi_r(H),\phi_s(H)]=i\beta\left\{\frac{1}{2}\Bigl[S_{24}\bigl(\nu_+(z_r-z_s)\bigr)+S_{24}\bigl(\nu_-(z_r-z_s)\bigr)\Bigr]
+\frac{1}{2}\Bigl[S_{24}\bigl(\mu_+(r,s)\bigr)+S_{24}\bigl(\mu_-(r,s)\bigr)\Bigr]\right\}I.
$$
On any fixed structural row $H$, as $(u,v)$ ranges independently over $\{a,b,x,y\}^2$, $\min_{u,v}\mu_-(u,v)=12+\min_u\nu_-(z_u)-\max_v\nu_+(z_v)$ and $\max_{u,v}\mu_-(u,v)=12+\max_u\nu_-(z_u)-\min_v\nu_+(z_v)$. Direct inspection of Table 1 across all 15 rows establishes the global integer bounds (attained at $(a,y)$ on Row 15 for the lower bound $3$, and at $(y,x)$ on Rows 5–6 and $(y,y)$ on Row 12 for the upper bound $22$)
$$
3\le 12+\nu_-(z_u)-\nu_+(z_v)\le 22\le 23=N-1\qquad\forall\,(u,v)\in\{a,b,x,y\}^2,
$$
$$
S_{24}\bigl(\mu_+(r,s)\bigr)+S_{24}\bigl(\mu_-(r,s)\bigr)=(-1)+(+1)=0,\qquad
\boxed{[\phi_r(H),\phi_s(H)]=i\beta\bigl(c_{rs}(H)-c_{sr}(H)\bigr)I.}
\tag{11}
$$
Indeed, for every $(r,s)\in\{a,b,x,y\}^2$, $\mu_-(r,s)\in\{3,\ldots,22\}\subset\{1,\ldots,23\}$ gives $S_{24}(\mu_-(r,s))=+1$ by (2), while $\mu_+(r,s)=-\mu_-(s,r)\in\{-22,\ldots,-3\}\subset\{-23,\ldots,-1\}$ gives $S_{24}(\mu_+(r,s))=-1$, so the boundary-image sum vanishes identically. For the remaining direct sum, $1\le|\nu_\pm(z_r-z_s)|\le 9\le 23$ in (8) gives $\frac12[S_{24}(\nu_+)+S_{24}(\nu_-)]=\frac12(1+1)=+1$ when $s\prec r$, $\frac12(-1-1)=-1$ when $r\prec s$, $\frac12(1-1)=0$ when $r\parallel s$, and $0$ when $r=s$, proving (11). $\square$

Notice that $N=24$ ($M=12$ modes) is the minimal even harmonic order for which $S_N(\mu_-) = +1$ holds across all 15 rows under (9): at $N=22$ ($M=11$), $N-1=21<22$ fails at $\mu_-=22$ on Rows 5, 6, and 12 where $S_{22}(22)=0$.

---

## 3. Modulo-24 Vandermonde positivity, covariance structure, and Weyl marginal preservation

Using the ground-state contraction $\omega_{\rm vac}\bigl(X_m(t_r)X_{m'}(t_s)\bigr)=\frac12\delta_{mm'}e^{-i\omega_m(t_r-t_s)}$, the unsymmetrized two-point function $W_{rs}(H):=\omega_{\rm vac}\bigl(\phi_r(H)\phi_s(H)\bigr)$ on $\mathcal S(\mathbb R^{12})$ equals $\beta\sum_{m=0}^{11}c_m\bigl[\cos\alpha_{m,r}\,e^{-i\omega_mt_r}\bigr]\overline{\bigl[\cos\alpha_{m,s}\,e^{-i\omega_mt_s}\bigr]}$. Writing $\cos\alpha_{m,r}=\frac12(e^{i\alpha_{m,r}}+e^{-i\alpha_{m,r}})$ with $\alpha_{m,r}=(6+3\xi_r)\tilde\varphi_m$ and $\omega_mt_r=3\tau_r\tilde\varphi_m$, define for each $r\in\{a,b,x,y\}$ the two integer exponents
$$
a_r:=6-\nu_+(z_r)\in\mathbb Z,\qquad
b_r:=-\bigl(6+\nu_-(z_r)\bigr)\in\mathbb Z,
$$
$$
\cos\alpha_{m,r}\,e^{-i\omega_mt_r}
=\frac{1}{2}\Bigl(e^{i\tilde\varphi_m a_r}+e^{i\tilde\varphi_m b_r}\Bigr)
=\frac{1}{2}\Bigl(e^{-ia_r\varphi_m}+e^{-ib_r\varphi_m}\Bigr),
$$
$$
W_{rs}(H)=W^{\rm dir}_{rs}(H)+W^{\rm img}_{rs}(H),\qquad
\begin{cases}
W^{\rm dir}_{rs}(H):=\dfrac{\beta}{4}\displaystyle\sum_{m=0}^{11}c_m\Bigl(e^{i\nu_+(z_r-z_s)\varphi_m}+e^{i\nu_-(z_r-z_s)\varphi_m}\Bigr),\\[10pt]
W^{\rm img}_{rs}(H):=\dfrac{\beta}{4}\displaystyle\sum_{m=0}^{11}c_m\Bigl(e^{i\mu_+(r,s)\varphi_m}+e^{i\mu_-(r,s)\varphi_m}\Bigr),
\end{cases}
\tag{12}
$$
since $a_s-a_r=\nu_+(z_r-z_s)$, $b_s-b_r=\nu_-(z_r-z_s)$, $a_s-b_r=12+\nu_-(z_r)-\nu_+(z_s)=\mu_-(r,s)$, and $b_s-a_r=\mu_+(r,s)$. Subtracting $W_{sr}(H)$ from $W_{rs}(H)$ independently reproduces (10)–(11).

**Theorem 2 (Strict positive definiteness via modulo-24 Vandermonde invertibility).** *On every one of the 15 structural rows (all 60 marked histories $H$), the $4\times 4$ Hermitian matrix $W(H)$ is strictly positive definite on $\mathbb C^4$, and the real symmetrized covariance $V(H):=\operatorname{Re}W(H)$ is strictly positive definite on $\mathbb R^4$ (and $\mathbb C^4$). Consequently, at every growth stage $k\in\{2,3,4\}$, every nonzero commutator zero mode $g\in\ker D_k(H)\setminus\{0\}$ defines a central observable $\Phi_H(g)=\sum_r g_r\phi_r(H)$ with strictly positive ground-state fluctuation variance $\omega_{\rm vac}\bigl(\Phi_H(g)^2\bigr)=g^{\mathsf T}V_k(H)g>0$.*

*Proof.* For any $u=(u_a,u_b,u_x,u_y)^{\mathsf T}\in\mathbb C^4$, substituting the factorized form in (12) gives
$$
u^\dagger W(H)u=\frac{\beta}{4}\sum_{m=0}^{11}c_m\left|\sum_{r\in\{a,b,x,y\}}u_r\bigl(e^{ia_r\varphi_m}+e^{ib_r\varphi_m}\bigr)\right|^2\ge 0,
$$
$$
\sum_{r\in\{a,b,x,y\}}\Bigl[\bigl(u_r\zeta(a_r)\bigr)\lambda(a_r)^m+\bigl(u_r\zeta(b_r)\bigr)\lambda(b_r)^m\Bigr]=0\qquad(m=0,1,\ldots,7),
\tag{13}
$$
whenever $u^\dagger W(H)u=0$ (since $\beta>0$ and $c_m>0$ for all $m=0,\ldots,11$), where for $k\in\mathbb Z$ we set $\zeta(k):=e^{i\pi k/24}$ and $\lambda(k):=e^{i\pi k/12}=\zeta(k)^2$, so $e^{ik\varphi_m}=e^{ik\pi/24}(e^{ik\pi/12})^m=\zeta(k)\lambda(k)^m$. Two integers $k,k'\in\mathbb Z$ satisfy $\lambda(k)=\lambda(k')$ if and only if $e^{i\pi(k-k')/12}=1$, i.e., $\frac{\pi(k-k')}{12}\in 2\pi\mathbb Z\iff k\equiv k'\pmod{24}$; thus $k\mapsto\lambda(k)$ is injective on $\mathbb Z/24\mathbb Z$. On any row $H$, check all pairwise differences among the eight integers $(a_a,a_b,a_x,a_y,b_a,b_b,b_x,b_y)$:
1. For $r\ne s$, $a_s-a_r=\nu_+(z_r-z_s)$ satisfies $1\le|a_s-a_r|\le 9<24$ by (8), so $a_r\not\equiv a_s\pmod{24}$.
2. For $r\ne s$, $b_s-b_r=\nu_-(z_r-z_s)$ satisfies $1\le|b_s-b_r|\le 9<24$ by (8), so $b_r\not\equiv b_s\pmod{24}$.
3. For all $(r,s)\in\{a,b,x,y\}^2$ (including $r=s$), $a_s-b_r=12+\nu_-(z_r)-\nu_+(z_s)=\mu_-(r,s)$ satisfies $3\le a_s-b_r\le 22<24$ by (11), so $a_s\not\equiv b_r\pmod{24}$.

Hence all eight residues modulo $24$—displayed explicitly in the rightmost column of Table 1—are pairwise distinct on every row, making the eight unit-circle nodes $\bigl(\lambda(a_a),\lambda(a_b),\lambda(a_x),\lambda(a_y),\lambda(b_a),\lambda(b_b),\lambda(b_x),\lambda(b_y)\bigr)$ pairwise distinct. The $8\times 8$ Vandermonde matrix in (13) on modes $m=0,1,\ldots,7$ therefore has nonzero determinant, forcing $u_r\zeta(a_r)=0$ and (since $|\zeta(a_r)|=1$) $u_r=0$ for all $r\in\{a,b,x,y\}$. Thus $W(H)\succ 0$ on $\mathbb C^4$. Writing $W(H)=V(H)+\frac{i}{2}D(H)$ with $V(H)=\operatorname{Re}W(H)$ real symmetric and $D(H)$ real skew-symmetric, every $g\in\mathbb R^4\setminus\{0\}$ satisfies $g^{\mathsf T}D(H)g=0$ and hence $g^{\mathsf T}V(H)g=g^\dagger W(H)g>0$, so $V(H)\succ 0$ on $\mathbb R^4$ (and $\mathbb C^4$). Every stage-$k$ covariance $V_k(H)$ ($k=2,3$) is a principal submatrix of $V(H)$ and is therefore strictly positive definite as well. $\square$

Let us examine explicitly how spatial boundary reflections enter $W(H)$, why the four-chain row and stage-2 prefix remain Toeplitz at $x_{\rm ref}=-L/4$, and how Row 2 resolves Johnston's stagewise zero-mode obstruction:

1. **Direct lag vs. static boundary-image reflection, Row 15 covariance, and $\det W_2^{\rm ext}>0$.** Because $\mu_\mp(r,s)=3(\tau_r-\tau_s)\mp\bigl(12+3(\xi_r+\xi_s)\bigr)$ and $12\varphi_m=\frac{(2m+1)\pi}{2}=m\pi+\frac{\pi}{2}$, we have $\cos\bigl((12+3(\xi_r+\xi_s))\varphi_m\bigr)=-(-1)^m\sin\bigl(3(\xi_r+\xi_s)\varphi_m\bigr)$, so the image piece in (12) takes the explicit form
   $$
   W^{\rm img}_{rs}(H)=\frac{\beta}{2}\sum_{m=0}^{11}c_m\cos\Bigl(\bigl(12+3(\xi_r+\xi_s)\bigr)\varphi_m\Bigr)e^{i3(\tau_r-\tau_s)\varphi_m}
   =-\frac{\beta}{2}\sum_{m=0}^{11}(-1)^mc_m\sin\bigl(3(\xi_r+\xi_s)\varphi_m\bigr)e^{i3(\tau_r-\tau_s)\varphi_m}.
   $$
   Time-stationarity of $\omega_{\rm vac}$ makes both $W^{\rm dir}_{rs}(H)$ and $W^{\rm img}_{rs}(H)$ depend on time solely through $\tau_r-\tau_s$, whereas the cavity walls break spatial translation invariance through $\xi_r+\xi_s$: for general spatially displaced events ($\xi_r+\xi_s\ne 0$), $W_{rs}(H)$ is not a function of $z_r-z_s$ alone (and at a generic reference point $x_{\rm ref}\ne -L/4$, even $\xi_r=\xi_s=0$ carries a nonzero static reflection shift $\frac{\beta}{2}\sum_m c_m\cos(2\alpha_m(x_{\rm ref}))e^{i3(\tau_r-\tau_s)\varphi_m}$). At our quarter-cavity reference point $x_{\rm ref}=-L/4$, however, $\xi_n=0$ gives $2\alpha_m(-L/4)=\frac{(47-2m)\pi}{2}$ ($u_m(-L/4)^2=\frac12$ and $\sin(3(\xi_n+\xi_{n'})\varphi_m)=\sin 0=0$ for every $m=0,\ldots,11$), so $W^{\rm img}_{n,n'}(\text{Row 15})=0$ vanishes identically! Using $\cot\theta+\tan\theta=2\csc(2\theta)$ and $\cot\theta-\tan\theta=2\cot(2\theta)$ at $\theta=\frac{(2m+1)\pi}{48}$ to pair $m$ with $11-m$ ($\psi_m:=3\varphi_m=\frac{(2m+1)\pi}{8}$, $\psi_{11-m}=3\pi-\psi_m$), Row 15 ($z_n=(n,0)$, $n\in\{0,1,2,3\}$) is Toeplitz with positive-lag entries $\ell=n-n'\in\{0,1,2,3\}$ and common stage-2 prefix $W_2^{\rm ext}=W_4(H)[a,b;a,b]$ across all 15 rows:
   $$
   W_{n,n'}(\text{Row 15})=W_{n-n'},\qquad
   W_\ell=\frac{\beta}{2}\sum_{m=0}^{11}c_me^{i\ell\psi_m}\quad(W_{-\ell}=\overline{W_\ell}),\qquad
   W_0=\frac{\beta}{12}\sum_{m=0}^{5}\csc\!\left(\frac{(2m+1)\pi}{24}\right)>0,
   $$
   $$
   W_1=\frac{\beta}{12}\sum_{m=0}^{5}\cot\!\left(\frac{(2m+1)\pi}{24}\right)\cos\!\left(\frac{(2m+1)\pi}{8}\right)+\frac{i\beta}{2},\qquad
   W_2^{\rm lag}=\frac{\beta}{12}\sum_{m=0}^{5}\csc\!\left(\frac{(2m+1)\pi}{24}\right)\cos\!\left(\frac{(2m+1)\pi}{4}\right)+\frac{i\beta}{2},
   $$
   $$
   W_3=\frac{\beta}{12}\sum_{m=0}^{5}\cot\!\left(\frac{(2m+1)\pi}{24}\right)\cos\!\left(\frac{3(2m+1)\pi}{8}\right)+\frac{i\beta}{2},\qquad
   W_2^{\rm ext}:=\begin{pmatrix}W_0&\overline{W_1}\\ W_1&W_0\end{pmatrix},\qquad
   \det W_2^{\rm ext}=W_0^2-|W_1|^2>0,
   $$
   $$
   \omega_{\rm vac}\bigl(\phi_x(\varnothing)^2\bigr)
   =\beta\sum_{m=0}^{11}c_m\cos^2\!\left(\frac{5(2m+1)\pi}{12}\right)
   =W_0-\frac{\beta}{2}\sum_{m=0}^{11}(-1)^mc_m\sin(8\varphi_m)
   \ge\beta c_0\frac{2-\sqrt3}{4}>0.
   \tag{14}
   $$
   Strict positivity $\det W_2^{\rm ext}>0$ follows immediately from Theorem 2 because $W_2^{\rm ext}$ is the leading $2\times 2$ principal submatrix of $W(H)\succ 0$ (and directly by the strict triangle inequality $|W_1|=\frac{\beta}{2}\bigl|\sum_{m=0}^{11}c_me^{i\psi_m}\bigr|<\frac{\beta}{2}\sum_{m=0}^{11}c_m=W_0$, since $c_0,c_1>0$ and $e^{i\pi/8}\ne e^{i3\pi/8}$). As proved in the [stationary four-chain dynamics](stationary_dynamics_for_four_chain_fields.md), releasing the singular prefix $W_2=\frac\beta2\left(\begin{smallmatrix}1&-i\\ i&1\end{smallmatrix}\right)$ ($\det W_2=0$) to $W_2^{\rm ext}$ is mandatory for any positive-Hamiltonian oscillator realization.

2. **Row 2 stagewise commutator zero mode ($I_x=\varnothing,\ I_y=\{x\}$).** On Row 2 (native probability $6/1320=1/220$ under both $P_0$ and $P_1$, or $6/5280=1/880$ per marked history), at stage 3 ($I_x=\varnothing$) vertex $x$ is incomparable with both $a$ and $b$, so $e_x=(0,0,1)^{\mathsf T}\in\ker D_3(\varnothing)$. Imposing Johnston's kernel-as-zero quotient $\phi_x=0$ at stage 3 would forbid the stage-4 continuation $I_y=\{x\}$ ($x\prec y$) from realizing $[\phi_y,\phi_x]=+i\beta I\ne 0$. In this cavity, $\phi_x(\varnothing)=\Psi(\tau/3,(-L/4+\frac43c\tau,0,0))$ commutes with $\phi_a$ and $\phi_b$ while carrying the strictly positive variance displayed in (14) (where $\alpha_m(x_{x,1})=(6+4)\tilde\varphi_m\implies\cos^2\alpha_m(x_{x,1})=\cos^2(10\varphi_m)$, and at $m=0$, $\cos^2(5\pi/12)=\frac{2-\sqrt3}{4}>0$), and at $z_y=(2/3,4/3)$ ($\nu_\pm(z_y-z_x)=(+1,+1)$) the unchanged operator $\phi_x(\varnothing)$ satisfies $[\phi_y,\phi_x(\varnothing)]=+i\beta I$ and $[\phi_y,\phi_a]=[\phi_y,\phi_b]=0$. Note also on Row 2 that although $z_y-z_x=(1/3,0)$ is purely timelike, $\xi_x+\xi_y=8/3\ne 0$ produces a nonzero boundary-image shift $W^{\rm img}_{yx}(\text{Row 2})=-\frac{\beta}{2}\sum_{m=0}^{11}(-1)^mc_m\sin(8\varphi_m)e^{i\varphi_m}$ in $W_{yx}(\text{Row 2})$, illustrating why image correlations enter whenever $\xi_r+\xi_s\ne 0$.

In the [prepared source ledger](native_source_readout_response.md), under each prepared root bit $i\in\{0,1\}$ let $p_3(I_x\mid i)>0$ denote the normalized stage-3 structural continuation law on $I_x\in\{\varnothing,\{a\},\{a,b\}\}$—specifically $\bigl(p_3(\varnothing\mid 0),p_3(\{a\}\mid 0),p_3(\{a,b\}\mid 0)\bigr)=(\tfrac15,\tfrac16,\tfrac{19}{30})$ and $\bigl(p_3(\varnothing\mid 1),p_3(\{a\}\mid 1),p_3(\{a,b\}\mid 1)\bigr)=(\tfrac15,\tfrac13,\tfrac{7}{15})$, satisfying $\sum_{I_x}p_3(I_x\mid i)=1$—and let $q_4(I_y\mid I_x,i)>0$ denote the normalized conditional stage-4 structural continuation law over the actual ideals $I_y$ of $(\{a,b,x\},\prec)$, satisfying $\sum_{I_y}q_4(I_y\mid I_x,i)=1$ for each $(I_x,i)$ and independent of $b_3$. Because the newborn binary marks $b_3,b_4\in\{0,1\}$ are independent and fair (probability $\frac12$ each), the stage-3 marked law is $P_i(I_x,b_3)=\frac12p_3(I_x\mid i)$ ($\sum_{I_x}\sum_{b_3\in\{0,1\}}\frac12p_3(I_x\mid i)=1$), the conditional stage-4 marked law given a realized stage-3 prefix $(I_x,b_3)$ is $P_i(I_y,b_4\mid I_x,b_3)=\frac12q_4(I_y\mid I_x,i)$ ($\sum_{I_y}\sum_{b_4\in\{0,1\}}\frac12q_4(I_y\mid I_x,i)=1$), and their product is the 60-history marked law $P_i(H)=P_i(I_x,I_y,b_3,b_4)=\frac14p_3(I_x\mid i)q_4(I_y\mid I_x,i)$ tabulated in Section 6. Writing $W_3(I_x)$ for the $3\times 3$ two-point matrix of $(\phi_a,\phi_b,\phi_x(I_x))$ and $W_4(H)=W_4(I_x,I_y):=W(H)$ for the $4\times 4$ matrix in (12), on $\mathcal S(\mathbb R^{12})$ every real linear combination $\Phi_H(u)=\sum_{r\in\{a,b,x,y\}}u_r\phi_r(H)$ ($u\in\mathbb R^4$) is symmetric and essentially self-adjoint by Nelson's analytic-vector theorem on the Hermite basis of $K$, generating bounded Weyl unitaries $\mathcal W_H(u):=\exp\bigl(i\overline{\Phi_H(u)}\bigr)$ on $L^2(\mathbb R^{12})$ that satisfy for $i\in\{0,1\}$:
$$
\mathcal W_H(u)\mathcal W_H(u')=e^{-\frac{i}{2}u^{\mathsf T}D(H)u'}\mathcal W_H(u+u'),\qquad
\omega_{\rm vac}\bigl(\mathcal W_H(u)\bigr)=\exp\!\left(-\frac{1}{2}u^{\mathsf T}V(H)u\right),
$$
$$
\sum_{I_x}\sum_{b_3\in\{0,1\}}\frac{1}{2}p_3(I_x\mid i)\,W_3(I_x)[a,b;a,b]=W_2^{\rm ext},\qquad
\sum_{I_x}\sum_{b_3\in\{0,1\}}\frac{1}{2}p_3(I_x\mid i)\,\omega_{\rm vac}(A)=\omega_{\rm vac}(A),
$$
$$
\sum_{H=1}^{60}P_i(H)\,W_4(H)[a,b;a,b]=W_2^{\rm ext},\qquad
\sum_{H=1}^{60}P_i(H)\,\omega_{\rm vac}(A)=\omega_{\rm vac}(A),
$$
$$
\sum_{I_y}\sum_{b_4\in\{0,1\}}\frac{1}{2}q_4(I_y\mid I_x,i)\,W_4(I_x,I_y)[a,b,x;a,b,x]=W_3(I_x),\qquad
\sum_{I_y}\sum_{b_4\in\{0,1\}}\frac{1}{2}q_4(I_y\mid I_x,i)\,\omega_{\rm vac}(B)=\omega_{\rm vac}(B),
\tag{15}
$$
for every bounded observable $A$ in the stage-2 Weyl $C^*$-algebra (or von Neumann algebra) generated by $\{\exp\bigl(i\overline{u_a\phi_a+u_b\phi_b}\bigr):u_a,u_b\in\mathbb R\}$ (which coincides with $\{\mathcal W_H(u_a,u_b,0,0):u_a,u_b\in\mathbb R\}$ on every branch) and every bounded observable $B$ in the stage-3 Weyl algebra generated by $\{\exp\bigl(i\overline{u_a\phi_a+u_b\phi_b+u_x\phi_x(I_x)}\bigr):u_a,u_b,u_x\in\mathbb R\}$ (which coincides with $\{\mathcal W_H(u_a,u_b,u_x,0):u_a,u_b,u_x\in\mathbb R\}$ across all stage-4 continuations of $(I_x,b_3)$). Because $\mathcal H$, $K$, $\Phi_{\rm sc}$, $\Psi$, and $\Omega_0$ are prepared once before the suffix births and are completely independent of $(i,I_x,I_y,b_3,b_4)$, stage $2\to 3$, $2\to 4$, and $3\to 4$ inclusions hold at the operator level on every branch and hence in unread conditional expectation under both $P_0$ and $P_1$.

---

## 4. History-independent $3+1$D cavity stress, axial Beltrami collar, and dominant-energy bound

Inside $\Omega$, adopt the Weyl-ordered minimally coupled kinetic stress-energy tensor associated with (4) on $\mathcal S(\mathbb R^{12})$,
$$
T^{\mu\nu}_{\rm sc}:=\kappa\left[\frac{1}{2}\bigl\{\partial^\mu\Phi_{\rm sc},\partial^\nu\Phi_{\rm sc}\bigr\}-\frac{1}{2}\eta^{\mu\nu}Z\right],\qquad
Z:=\frac{1}{2}\eta^{\alpha\gamma}\bigl\{\partial_\alpha\Phi_{\rm sc},\partial_\gamma\Phi_{\rm sc}\bigr\}
=-\frac{\dot\Phi_{\rm sc}^2}{c^2}+|\nabla\Phi_{\rm sc}|^2,
$$
$$
E_m:=\frac{A_*\omega_m}{2}=\frac{(47-2m)\pi A_*}{16\tau}>0,\qquad
\rho_m:=\frac{E_m}{V}>0,\qquad
\rho_0^{\rm tot}:=\sum_{m=0}^{11}\rho_m=\frac{E_0}{V}=\frac{27\pi A_*}{512c^3\tau^4}>0,
$$
$$
\boxed{\omega_{\rm vac}\bigl(T^{00}_{\rm sc}(x)\bigr)=\rho_0^{\rm tot},\quad
\omega_{\rm vac}\bigl(T^{0a}_{\rm sc}(x)\bigr)=0,\quad
\omega_{\rm vac}\bigl(T^{ab}_{\rm sc}(x)\bigr)
=\operatorname{diag}\!\left(\rho_0^{\rm tot},\,\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1),\,\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)\right)}
\tag{16}
$$
for all $x\in\Omega$. Every quadratic derivative polynomial in $T^{\mu\nu}_{\rm sc}$ maps $\mathcal S(\mathbb R^{12})$ into itself, with $T^{00}_{\rm sc}=\mathcal H_{\rm sc}$ a nonnegative quadratic form, $n_aT^{a0}_{\rm sc}=-\frac{\kappa}{2c}\{\dot\Phi_{\rm sc},n\cdot\nabla\Phi_{\rm sc}\}=0$ on $\partial\Omega$, and $\partial_\mu T^{\mu\nu}_{\rm sc}=\frac{\kappa}{2}\{\Box\Phi_{\rm sc},\partial^\nu\Phi_{\rm sc}\}=0$ on $\operatorname{int}(\Omega)$ ($\Box:=-c^{-2}\partial_t^2+\nabla^2$). To verify (16) directly, observe that $\frac{\kappa}{4}B_m^2k_m^2=\frac{\kappa}{4}\frac{2A_*c^2}{\kappa V\omega_m}\frac{\omega_m^2}{c^2}=\rho_m$; hence ground-state contraction on $\Omega$ gives $\omega_{\rm vac}(c^{-2}\dot\Phi_{\rm sc}^2)=\frac{2}{\kappa}\sum_{m=0}^{11}\rho_m\cos^2\alpha_m(x_1)$, $\omega_{\rm vac}(\frac12\{\partial_a\Phi_{\rm sc},\partial_b\Phi_{\rm sc}\})=\delta_{a1}\delta_{b1}\frac{2}{\kappa}\sum_{m=0}^{11}\rho_m\sin^2\alpha_m(x_1)$, $\omega_{\rm vac}(\{\dot\Phi_{\rm sc},\partial_a\Phi_{\rm sc}\})=0$, and $\omega_{\rm vac}(Z)=-\frac{2}{\kappa}\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)$. Thus $\omega_{\rm vac}(T^{00}_{\rm sc}(x))=\sum_{m=0}^{11}\rho_m(\cos^2\alpha_m+\sin^2\alpha_m)=\rho_0^{\rm tot}$ and $\omega_{\rm vac}(T^{11}_{\rm sc}(x))=\sum_{m=0}^{11}\rho_m(2\sin^2\alpha_m+\cos 2\alpha_m)=\rho_0^{\rm tot}$ are both spatially uniform and static on $\Omega$, while $\omega_{\rm vac}(T^{22}_{\rm sc}(x))=\omega_{\rm vac}(T^{33}_{\rm sc}(x))=-\frac{\kappa}{2}\omega_{\rm vac}(Z)=\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)$ depends only on $x_1$, so $\partial_a\omega_{\rm vac}(T^{ab}_{\rm sc}(x))=0$ inside $\operatorname{int}(\Omega)$.

Because $2\alpha_m(x_1)$ traverses $[0,2(47-2m)\pi]$ on $[-L/2,L/2]$, $\int_{-L/2}^{L/2}\cos 2\alpha_m(x_1)\,dx_1=0$ for each $m=0,\ldots,11$. Integrating (16) over $\Omega$ yields $\int_\Omega\omega_{\rm vac}(T^{00}_{\rm sc})\,d^3x=E_0$ and nonzero longitudinal bulk stress; if one truncates (16) by zero outside $\Omega$ as $T^{\mu\nu}_{\rm trunc}(x):=\mathbf 1_\Omega(x)\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x))$, then for every $f\in C_c^\infty(\mathbb R^3;\mathbb R^3)$ the divergence theorem on $\Omega$ gives $\langle\partial_aT^{ab}_{\rm trunc},f_b\rangle=-\int_\Omega\omega_{\rm vac}(T^{ab}_{\rm sc})\partial_af_b\,d^3x=-\int_{\partial\Omega}n_a\omega_{\rm vac}(T^{ab}_{\rm sc})f_b\,dS$, i.e.,
$$
\int_\Omega\omega_{\rm vac}\bigl(T^{ab}_{\rm sc}(x)\bigr)\,d^3x=\operatorname{diag}(E_0,0,0),\qquad
\boxed{\partial_a\bigl(\mathbf 1_\Omega\,\omega_{\rm vac}(T^{ab}_{\rm sc})\bigr)=-n_a\omega_{\rm vac}(T^{ab}_{\rm sc})\,\delta_{\partial\Omega}\ne 0,}
\tag{17}
$$
where $\delta_{\partial\Omega}$ is the surface area measure on $\partial\Omega$ (evaluating to $\langle\partial_aT^{ab}_{\rm trunc},f_b\rangle=-E_0\ne 0$ for $f(x)=(x_1,0,0)$ near $\overline\Omega$). An isolated conserved whole-space gravitational source must therefore supply a confining stress collar outside $\Omega$.

Because $\alpha_m(x_1)=k_m(x_1+L/2)$ is affine on all of $\mathbb R$, define on all of $\mathbb R^3$ the smooth diagonal interior Beltrami stress potential $\Phi^{\rm int}(x)=\operatorname{diag}\bigl(\Phi_1^{\rm int}(x),\Phi_2^{\rm int}(x),\Phi_3^{\rm int}(x)\bigr)$ by
$$
g(x_1):=\sum_{m=0}^{11}\frac{\rho_m}{4k_m^2}\bigl(1-\cos 2\alpha_m(x_1)\bigr)
=\sum_{m=0}^{11}\frac{\rho_m}{2k_m^2}\sin^2\alpha_m(x_1)\ge 0,
$$
$$
\Phi_1^{\rm int}(x)\equiv 0,\qquad
\Phi_2^{\rm int}(x_1,x_3):=\frac{1}{4}\rho_0^{\rm tot}x_3^2+g(x_1)\ge 0,\qquad
\Phi_3^{\rm int}(x_1,x_2):=\frac{1}{4}\rho_0^{\rm tot}x_2^2+g(x_1)\ge 0.
\tag{18}
$$
For any smooth diagonal tensor $\Phi_{mn}=\Phi_m\delta_{mn}$ with $\epsilon_{123}=+1$, expanding $T^{ab}(\Phi):=\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}$ gives $T^{11}(\Phi)=\partial_3^2\Phi_2+\partial_2^2\Phi_3$, $T^{22}(\Phi)=\partial_3^2\Phi_1+\partial_1^2\Phi_3$, $T^{33}(\Phi)=\partial_2^2\Phi_1+\partial_1^2\Phi_2$, $T^{12}(\Phi)=-\partial_1\partial_2\Phi_3$, $T^{13}(\Phi)=-\partial_1\partial_3\Phi_2$, and $T^{23}(\Phi)=-\partial_2\partial_3\Phi_1$. Differentiating (18) yields $g'(x_1)=\sum_{m=0}^{11}\frac{\rho_m}{2k_m}\sin 2\alpha_m(x_1)$ and $g''(x_1)=\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)$, while $\partial_3^2\Phi_2^{\rm int}=\partial_2^2\Phi_3^{\rm int}=\frac12\rho_0^{\rm tot}$ and all mixed second partial derivatives vanish by additive variable separation. Consequently $T^{ab}(\Phi^{\rm int})(x)=\operatorname{diag}\bigl(\rho_0^{\rm tot},g''(x_1),g''(x_1)\bigr)$ on all $\mathbb R^3$, and in particular $T^{ab}(\Phi^{\rm int})(x)=\omega_{\rm vac}(T^{ab}_{\rm sc}(x))$ at every $x\in\Omega$. Furthermore, because $2\alpha_m(x_1)=2k_mx_1+(47-2m)\pi$ with $47-2m$ odd gives $\cos 2\alpha_m(x_1)=-\cos(2k_mx_1)=\cos 2\alpha_m(-x_1)$, we have $g(-x_1)=g(x_1)$, $\Phi^{\rm int}(-x)=\Phi^{\rm int}(x)$, and exact transverse swap symmetry $\Phi_2^{\rm int}(x_1,x_2)=\Phi_3^{\rm int}(x_1,x_2)$.

Write $B_R(0):=\{x\in\mathbb R^3:|x|<R\}$ for the open ball of radius $R>0$. Every $x\in\overline\Omega=[-L/2,L/2]^3$ satisfies $|x|\le\sqrt{3(L/2)^2}=\frac{\sqrt3}{2}L<L$ (with equality at the eight cube corners $(\pm L/2,\pm L/2,\pm L/2)$), giving the strict radial nesting $\overline\Omega\subset\overline{B_{\frac{\sqrt3}{2}L}(0)}\subset B_L(0)\subset B_{3L/2}(0)\subset B_{2L}(0)\subset B_{3L}(0)$. Retain the smooth radial cutoff family of the [compact four-chain cavity source](compact_cavity_source_for_four_chain_field.md):
$$
b(t):=\begin{cases}e^{-1/t},& t>0,\\ 0,& t\le 0,\end{cases}\qquad
s:=\frac{|x|}{L},\qquad \sigma:=s^2=\frac{|x|^2}{L^2},
$$
$$
\chi_{\rm st}(s):=\frac{b(4-s^2)}{b(4-s^2)+b(s^2-9/4)},\qquad
\chi_{\rm rise}(s):=\frac{b(s^2-1)}{b(s^2-1)+b(9/4-s^2)},\qquad
\chi_{\rm out}(s):=\frac{b(9-s^2)}{b(9-s^2)+b(s^2-4)},
$$
$$
\Phi_{mn}(x):=\chi_{\rm st}\!\left(\frac{|x|}{L}\right)\Phi^{\rm int}_{mn}(x),\qquad
\varepsilon_{\rm tot}(|x|):=\left[\rho_0^{\rm tot}+U_{\rm col}\,\chi_{\rm rise}\!\left(\frac{|x|}{L}\right)\right]\chi_{\rm out}\!\left(\frac{|x|}{L}\right),
$$
$$
T^{00}_{\rm tot}(x):=\varepsilon_{\rm tot}(|x|),\qquad
T^{0a}_{\rm tot}(x)=T^{a0}_{\rm tot}(x):=0,\qquad
T^{ab}_{\rm tot}(x):=\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}(x).
\tag{19}
$$
For every integer $k\ge 1$ and $t>0$, putting $u=1/t>0$ gives $\frac{d}{du}(k\ln u-u)=\frac{k}{u}-1$ and $\frac{d^2}{du^2}(k\ln u-u)=-\frac{k}{u^2}<0$, so $t^{-k}e^{-1/t}=u^ke^{-u}\le k^ke^{-k}$ on $(0,\infty)$ and $b\in C^\infty(\mathbb R)$ is nonnegative and strictly increasing on $(0,\infty)$. Because the two arguments of $b$ in each denominator of (19) sum to $7/4$, $5/4$, and $5$, at least one argument is at least half that sum, bounding the denominators below on $\mathbb R$ by $e^{-8/7}$, $e^{-8/5}$, and $e^{-2/5}$. Since $\sigma=|x|^2/L^2$ is a smooth polynomial on $\mathbb R^3$, every component of $\Phi_{mn}$ and $T^{\mu\nu}_{\rm tot}$ belongs to $C_c^\infty(\mathbb R^3)$ with $\operatorname{supp}\Phi_{mn}\subseteq\overline{B_{2L}(0)}$ and $\operatorname{supp}T^{\mu\nu}_{\rm tot}\subseteq\overline{B_{3L}(0)}$. On $|x|\le L$ (containing $\overline\Omega$), $\chi_{\rm rise}=0$ and $\chi_{\rm st}=\chi_{\rm out}=1$, so $T^{\mu\nu}_{\rm tot}(x)=\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x))$ pointwise throughout $\Omega$. Crucially, $T^{\mu\nu}_{\rm tot}$ depends only on $\Omega_0$ and the fixed collar parameters, and is therefore completely history-independent across all 60 marked histories.

We now derive an explicit elementary closed-form bound on the spatial operator norm $\|T^{ab}_{\rm tot}(x)\|=\sup_{|v|=1}|v_aT^{ab}_{\rm tot}(x)v_b|$ at every $x\in\mathbb R^3$:

1. **Interior and ramp shells ($0\le s\le 3/2$).** Here $\chi_{\rm st}(s)=1$, so $T^{ab}_{\rm tot}(x)=T^{ab}(\Phi^{\rm int})(x)=\operatorname{diag}\bigl(\rho_0^{\rm tot},g''(x_1),g''(x_1)\bigr)$. Because $|g''(x_1)|\le\sum_{m=0}^{11}\rho_m|\cos 2\alpha_m(x_1)|\le\rho_0^{\rm tot}$, we have $\|T^{ab}_{\rm tot}(x)\|=\rho_0^{\rm tot}\le\rho_0^{\rm tot}+U_{\rm col}\chi_{\rm rise}(s)=T^{00}_{\rm tot}(x)$ for any $U_{\rm col}>0$.
2. **Outer taper and exterior ($s\ge 2$).** Here $\chi_{\rm st}(s)=0$, so $T^{ab}_{\rm tot}(x)=0\le(\rho_0^{\rm tot}+U_{\rm col})\chi_{\rm out}(s)=T^{00}_{\rm tot}(x)$.
3. **Stress-cutoff transition shell ($3/2\le s\le 2$).** Here $\chi_{\rm rise}(s)=\chi_{\rm out}(s)=1$, so $T^{00}_{\rm tot}(x)=\rho_0^{\rm tot}+U_{\rm col}$ is constant across the shell. On $|x|\le 2L$, nonnegativity of $\Phi_2^{\rm int},\Phi_3^{\rm int}$, $x_2^2+x_3^2\le|x|^2\le 4L^2$, $1-\cos 2\alpha_m\le 2$, and $k_m\ge k_{11}=\frac{25\pi}{L}$ give
   $$
   \sum_{m=1}^{3}\bigl|\Phi_m^{\rm int}(x)\bigr|
   =\Phi_2^{\rm int}(x)+\Phi_3^{\rm int}(x)
   =\frac{1}{4}\rho_0^{\rm tot}(x_2^2+x_3^2)+2g(x_1)
   \le\left(1+\frac{1}{625\pi^2}\right)\rho_0^{\rm tot}L^2
   <\frac{9}{8}\rho_0^{\rm tot}L^2,
   $$
   using $\pi>3\implies\frac{1}{625\pi^2}<\frac{1}{5625}<\frac18$. For the gradients on $|x|\le 2L$, notice that $\frac{\rho_m}{2k_m}=\frac{(47-2m)\rho_0^{\rm tot}/432}{2(47-2m)\pi/L}=\frac{\rho_0^{\rm tot}L}{864\pi}$ is independent of $m$, so $|g'(x_1)|\le 12\cdot\frac{\rho_0^{\rm tot}L}{864\pi}=\frac{\rho_0^{\rm tot}L}{72\pi}$. Together with $|\nabla\Phi_2^{\rm int}|+|\nabla\Phi_3^{\rm int}|\le 2|g'(x_1)|+\frac12\rho_0^{\rm tot}(|x_2|+|x_3|)$ and $|x_2|+|x_3|\le\sqrt{2(x_2^2+x_3^2)}\le 2\sqrt2 L$, using $17^2=289>288=2\cdot 12^2\implies\sqrt2<\frac{17}{12}$ and $\frac{1}{36\pi}<\frac{1}{108}$ gives $\sqrt2+\frac{1}{36\pi}<\frac{17}{12}+\frac{1}{108}=\frac{77}{54}<\frac{3}{2}$, whence
   $$
   \sum_{m=1}^{3}\bigl|\Phi_m^{\rm int}(x)\bigr|<\frac{9}{8}\rho_0^{\rm tot}L^2,\qquad
   \sum_{m=1}^{3}\bigl|\nabla\Phi_m^{\rm int}(x)\bigr|\le\left(\sqrt2+\frac{1}{36\pi}\right)\rho_0^{\rm tot}L<\frac{3}{2}\rho_0^{\rm tot}L\qquad(|x|\le 2L),
   $$
   $$
   |\nabla\eta(x)|\le\frac{4F_1}{L},\qquad
   \|\operatorname{Hess}\eta(x)\|\le\frac{16F_2+2F_1}{L^2}\qquad\left(\frac{3}{2}L\le|x|\le 2L\right),
   \tag{20}
   $$
   where $\eta(x):=\chi_{\rm st}(|x|/L)=F(\sigma)$ for $\sigma=|x|^2/L^2\in[9/4,4]$ with $F_1:=4e^{-6/7}$ and $F_2:=32e^{-12/7}+54e^{-13/7}+256e^{-20/7}$. To verify (20) on $\sigma\in[9/4,4]$ from scratch, write $F(\sigma)=b_1(\sigma)/D(\sigma)$ with $b_1(\sigma)=b(4-\sigma)$, $b_2(\sigma)=b(\sigma-9/4)$, and $D(\sigma)=b_1(\sigma)+b_2(\sigma)\ge e^{-8/7}$. Because $b'(t)=t^{-2}e^{-1/t}\in(0,4e^{-2}]$ and $|b''(t)|=|(t^{-4}-2t^{-3})e^{-1/t}|\le 256e^{-4}+54e^{-3}$ for $t>0$, we have $-4e^{-2}\le b_1'(\sigma)\le 0\le b_2'(\sigma)\le 4e^{-2}$, $|b_1'(\sigma)+b_2'(\sigma)|\le 4e^{-2}$, and $|b_1''(\sigma)|,|b_2''(\sigma)|\le 256e^{-4}+54e^{-3}$. Setting $p=b_1/D\in[0,1]$ and $q=b_2/D=1-p\in[0,1]$, the quotient identities $F'(\sigma)=(b_1'b_2-b_1b_2')/D^2=q(b_1'/D)-p(b_2'/D)$ and $F''(\sigma)=q(b_1''/D)-p(b_2''/D)-2F'(\sigma)(b_1'+b_2')/D$ give $|F'(\sigma)|\le 4e^{-2}/e^{-8/7}=F_1$ and $|F''(\sigma)|\le(256e^{-4}+54e^{-3})e^{8/7}+8F_1e^{-6/7}=F_2$. Since $\partial_k\eta(x)=\frac{2x_k}{L^2}F'(\sigma)$, $\partial_k\partial_l\eta(x)=\frac{4x_kx_l}{L^4}F''(\sigma)+\frac{2\delta_{kl}}{L^2}F'(\sigma)$, and $|x|\le 2L$, (20) follows.

   For any unit vector $v\in\mathbb R^3$, $w^{(m)}_k:=\sum_{a=1}^3v_a\epsilon_{akm}$ satisfies $|w^{(m)}|^2=1-v_m^2\le 1$, and expanding $\partial_k\partial_l(\eta\Phi_m^{\rm int})$ gives $v_aT^{ab}_{\rm tot}(x)v_b=\eta(x)v_aT^{ab}(\Phi^{\rm int})(x)v_b+2\sum_{m=2}^3(w^{(m)}\cdot\nabla\eta)(w^{(m)}\cdot\nabla\Phi_m^{\rm int})+\sum_{m=2}^3\Phi_m^{\rm int}{w^{(m)}}^{\mathsf T}[\operatorname{Hess}\eta]w^{(m)}$. Applying Cauchy–Schwarz, $0\le\eta\le 1$, $\|T^{ab}(\Phi^{\rm int})\|=\rho_0^{\rm tot}$, and (20) yields across $\frac32L\le|x|\le 2L$:
   $$
   \|T^{ab}_{\rm tot}(x)\|
   <\left[1+2(4F_1)\frac{3}{2}+(16F_2+2F_1)\frac{9}{8}\right]\rho_0^{\rm tot}
   =\left(1+\frac{57}{4}F_1+18F_2\right)\rho_0^{\rm tot}=:M_{\rm st}^{(12)}\rho_0^{\rm tot},
   $$
   $$
   M_{\rm st}^{(12)}:=1+57e^{-6/7}+576e^{-12/7}+972e^{-13/7}+4608e^{-20/7}>1,\qquad
   U_{\rm col}:=M_{\rm st}^{(12)}\rho_0^{\rm tot}>0,
   $$
   $$
   \boxed{\|T^{ab}_{\rm tot}(x)\|\le T^{00}_{\rm tot}(x)\qquad\forall\,x\in\mathbb R^3.}
   \tag{21}
   $$
   On $\frac32L\le|x|\le 2L$, $\|T^{ab}_{\rm tot}(x)\|<U_{\rm col}<\rho_0^{\rm tot}+U_{\rm col}=T^{00}_{\rm tot}(x)$ holds with strict margin greater than $\rho_0^{\rm tot}$. Hence for every future-directed causal four-vector $u^\mu=(u^0,u)$ ($u^0\ge|u|\ge 0$), $J^\mu:=-T^{\mu\nu}_{\rm tot}u_\nu=(T^{00}_{\rm tot}u^0,-T^{ab}_{\rm tot}u_b)$ satisfies $|J(x)|\le\|T^{ab}_{\rm tot}(x)\||u|\le T^{00}_{\rm tot}(x)u^0=J^0(x)$, proving the full Lorentzian dominant (and therefore weak and null) energy condition everywhere on $\mathbb R^3$.

Static $T^{00}_{\rm tot}$ and vanishing $T^{0a}_{\rm tot}$ give $\partial_\mu T^{\mu 0}_{\rm tot}=0$, while $\Phi_{mn}\in C_c^\infty(\mathbb R^3)$ and antisymmetry of $\epsilon_{akm}$ in $(a,k)$ give $\partial_aT^{ab}_{\rm tot}=\epsilon_{akm}\epsilon_{bln}\partial_a\partial_k\partial_l\Phi_{mn}=0$ classically and distributionally on all $\mathbb R^3$. Integrating $\partial_k(\epsilon_{akm}\epsilon_{bln}\partial_l\Phi_{mn})$ over $B_{3L}(0)$ (where $\Phi_{mn}=0$ near $\partial B_{3L}(0)$) gives zero total spatial stress, and splitting $\mathbb R^3=\Omega\sqcup(\mathbb R^3\setminus\Omega)$ with (17) proves exact collar stress compensation:
$$
\partial_\mu T^{\mu\nu}_{\rm tot}=0,\qquad
\Sigma_{ab}:=\int_{\mathbb R^3}T^{ab}_{\rm tot}(x)\,d^3x=0,\qquad
\boxed{\int_{\mathbb R^3\setminus\Omega}T^{ab}_{\rm tot}(x)\,d^3x=-\operatorname{diag}(E_0,0,0).}
\tag{22}
$$

---

## 5. Whole-space linearized gravity, all-branch inertia, and exterior tidal curvature contrast

Adopt the whole-space static linearized Einstein equations in harmonic (de Donder) gauge from the [closed-source active-mass note](closed_radiation_shell_mass.md), [static stress-quadrupole construction](stress_quadrupole_at_equal_energy.md), and [compact four-chain cavity source](compact_cavity_source_for_four_chain_field.md):
$$
\nabla^2\bar h_{\mu\nu}=-\frac{16\pi G}{c^4}T^{\rm tot}_{\mu\nu},\qquad
\bar h_{\mu\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}\frac{T^{\rm tot}_{\mu\nu}(y)}{|x-y|}\,d^3y,\qquad
\lim_{|x|\to\infty}\bar h_{\mu\nu}(x)=0,
$$
$$
h_{\mu\nu}=\bar h_{\mu\nu}-\frac{1}{2}\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta},\qquad
\Phi_{\rm tot}(x)=-\frac{1}{2}c^2h_{00}(x)
=-\frac{G}{c^2}\int_{\mathbb R^3}\frac{\varepsilon_{\rm tot}(|y|)+\operatorname{tr}T_{\rm tot}(y)}{|x-y|}\,d^3y,
\tag{23}
$$
where $T^{\rm tot}_{00}=T^{00}_{\rm tot}$, $T^{\rm tot}_{0a}=0$, and $T^{\rm tot}_{ab}=T^{ab}_{\rm tot}$. Changing variables by $z=x-y$ ($d^3z=d^3y$) writes $\bar h_{\mu\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|z|^{-1}T^{\rm tot}_{\mu\nu}(x-z)\,d^3z$. Because $T^{\rm tot}_{\mu\nu}\in C_c^\infty(\mathbb R^3)$ is supported in $\overline{B_{3L}(0)}$ and $|z|^{-1}\in L^1_{\rm loc}(\mathbb R^3)$, differentiating any number of times with respect to $x$ under the $z$-integral shows $\bar h_{\mu\nu}\in C^\infty(\mathbb R^3)$, while $|\bar h_{\mu\nu}(x)|\le\frac{4G}{c^4(|x|-3L)}\|T^{\rm tot}_{\mu\nu}\|_{L^1}\to 0$ as $|x|\to\infty$. Any difference $w_{\mu\nu}$ of two distributional solutions of $\nabla^2\bar h_{\mu\nu}=-(16\pi G/c^4)T^{\rm tot}_{\mu\nu}$ decaying at infinity satisfies $\nabla^2w_{\mu\nu}=0$ on $\mathbb R^3$, is smooth and harmonic by Weyl's lemma, and vanishes identically by the maximum principle. Differentiating under the $z$-integral gives $\partial^a\bar h_{a\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|z|^{-1}(\partial_aT^{\rm tot}_{a\nu})(x-z)\,d^3z$, and changing variables back via $y=x-z$ yields $\partial^a\bar h_{a\nu}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|x-y|^{-1}\partial_aT^{\rm tot}_{a\nu}(y)\,d^3y=0$ by (22); together with $\partial_0\bar h_{0\nu}=0$, this proves $\partial^\mu\bar h_{\mu\nu}=0$ on all $\mathbb R^3$.

The total rest energy decomposes into the 12-mode cavity ground energy $E_0$ and the strictly positive support-collar energy $E_{\rm support}:=\int_{\mathbb R^3\setminus\Omega}\varepsilon_{\rm tot}(|x|)\,d^3x>0$:
$$
E_{\rm tot}:=\int_{\mathbb R^3}\varepsilon_{\rm tot}(|x|)\,d^3x=E_0+E_{\rm support}
=4\pi L^3\left[\rho_0^{\rm tot}\int_0^3s^2\chi_{\rm out}(s)\,ds+U_{\rm col}\int_1^3s^2\chi_{\rm rise}(s)\chi_{\rm out}(s)\,ds\right],
$$
which is strictly finite and bounded between $4\pi L^3(\frac83\rho_0^{\rm tot}+\frac{37}{24}U_{\rm col})$ and $4\pi L^3(9\rho_0^{\rm tot}+\frac{26}{3}U_{\rm col})$. Under a supplied active Lorentz boost with velocity $v$ ($\beta_v=v/c$, $|\beta_v|<1$, $\gamma=(1-\beta_v^2)^{-1/2}$) along any unit axis $n\in\mathbb R^3$, $x'^0=\gamma(x^0+\beta_vn\cdot x)$ and $x'=x+(\gamma-1)(n\cdot x)n+\gamma\beta_vx^0n$ induce the simultaneous-slice measure $d^3x'=d^3x/\gamma$ on $x'^0=0$ as in the [same-source boost companion](closed_radiation_shell_inertia.md). Because $T^{\mu\nu}_{\rm tot}$ is static with $T^{0a}_{\rm tot}=0$, $T'^{00}(0,x')=\gamma^2(T^{00}_{\rm tot}+\beta_v^2n_an_bT^{ab}_{\rm tot})$ and $T'^{0i}(0,x')=\gamma\beta_v\bigl[\gamma T^{00}_{\rm tot}n_i+T^{ia}_{\rm tot}n_a+(\gamma-1)(n_an_bT^{ab}_{\rm tot})n_i\bigr]$, so integrating against $d^3x'=d^3x/\gamma$ and applying $\Sigma_{ab}=0$ from (22) yields $E':=\int_{x'^0=0}T'^{00}\,d^3x'=\gamma(E_{\rm tot}+\beta_v^2n_an_b\Sigma_{ab})=\gamma E_{\rm tot}$ and $P'_i:=c^{-1}\int_{x'^0=0}T'^{0i}\,d^3x'=\frac{\gamma v}{c^2}E_{\rm tot}n_i$. Likewise $\int_{\mathbb R^3}\operatorname{tr}T_{\rm tot}\,d^3y=\delta_{ab}\Sigma_{ab}=0$ fixes the $O(1/|x|)$ coefficient of $\Phi_{\rm tot}(x)$ in (23), proving across **all 60 marked histories ($1320/1320$) without history-dependent re-preparation**:
$$
M_{\rm in}:=\lim_{v\to 0}\frac{n\cdot P'}{v}=\frac{E_{\rm tot}}{c^2},\qquad
M_{\rm active}:=\frac{1}{c^2}\int_{\mathbb R^3}\bigl(\varepsilon_{\rm tot}(|y|)+\operatorname{tr}T_{\rm tot}(y)\bigr)\,d^3y,\qquad
\boxed{M_{\rm in}=M_{\rm active}=\frac{E_{\rm tot}}{c^2}=\frac{E_0+E_{\rm support}}{c^2}.}
\tag{24}
$$
Table 2 records the complete monopole and boost-stress compensation between the 12-mode quantum cavity interior and the classical Beltrami collar:

| Region of this single source | Energy integral | Spatial-stress integral | Spatial-trace integral | Contribution to $c^2M_{\rm active}$ |
|---|---:|---:|---:|---:|
| Cavity interior ($\Omega$) | $E_0$ | $\operatorname{diag}(E_0,0,0)$ | $+E_0$ | $2E_0$ |
| Support collar ($\mathbb R^3\setminus\Omega$) | $E_{\rm support}$ | $-\operatorname{diag}(E_0,0,0)$ | $-E_0$ | $E_{\rm support}-E_0$ |
| Complete source ($\mathbb R^3$) | $E_0+E_{\rm support}$ | $0$ | $0$ | $E_0+E_{\rm support}$ |

**Table 2.** History-independent monopole energy and spatial-stress balance of $T^{\mu\nu}_{\rm tot}$.

Because $\Phi_{mn}(-x)=\Phi_{mn}(x)$, $T^{ab}_{\rm tot}(-x)=T^{ab}_{\rm tot}(x)$, and $\varepsilon_{\rm tot}(|-x|)=\varepsilon_{\rm tot}(|x|)$, every odd spatial multipole—including the active mass dipole $c^{-2}\int_{\mathbb R^3}x_a(\varepsilon_{\rm tot}+\operatorname{tr}T_{\rm tot})\,d^3x=0$—vanishes identically. Using $\epsilon_{akm}\epsilon_{aln}=\delta_{kl}\delta_{mn}-\delta_{kn}\delta_{ml}$, we have $\operatorname{tr}T_{\rm tot}=\nabla^2(\operatorname{tr}\Phi)-\partial_k\partial_l\Phi_{kl}$. For the tracefree active quadrupole $Q_{ab}:=c^{-2}\int_{\mathbb R^3}P_{ab}(x)(\varepsilon_{\rm tot}(|x|)+\operatorname{tr}T_{\rm tot}(x))\,d^3x$ with $P_{ab}(x)=3x_ax_b-|x|^2\delta_{ab}$, spherical symmetry of $\varepsilon_{\rm tot}(|x|)$ gives $\int_{\mathbb R^3}P_{ab}\varepsilon_{\rm tot}\,d^3x=0$, while $\nabla^2P_{ab}=0$, $\partial_k\partial_lP_{ab}=3(\delta_{ak}\delta_{bl}+\delta_{bk}\delta_{al})-2\delta_{kl}\delta_{ab}$, and two integrations by parts over $B_{3L}(0)$ (with zero boundary terms since $\operatorname{supp}\Phi_{kl}\subseteq\overline{B_{2L}(0)}$) yield
$$
Q_{ab}=-\frac{2}{c^2}\int_{\mathbb R^3}\bigl(3\Phi_{ab}(x)-\delta_{ab}\operatorname{tr}\Phi(x)\bigr)\,d^3x,\qquad
Q_{ab}=0\quad(a\ne b),\qquad
Q_{11}=-2Q_{22}=-2Q_{33}=\frac{2}{c^2}\int_{\mathbb R^3}\bigl(\Phi_2(x)+\Phi_3(x)\bigr)\,d^3x,
$$
$$
Q_{11}>\frac{2}{c^2}\int_{B_{3L/2}(0)}\frac{1}{4}\rho_0^{\rm tot}(x_2^2+x_3^2)\,d^3x
=\frac{81\pi}{40}\frac{\rho_0^{\rm tot}L^5}{c^2},\qquad
\boxed{Q_{11}=-2Q_{22}=-2Q_{33}>\frac{17496\pi^2}{5}A_*\tau>0.}
\tag{25}
$$
Here diagonality of $\Phi=\operatorname{diag}(0,\Phi_2,\Phi_3)$ gives $Q_{ab}=0$ for $a\ne b$ and $3\Phi_{11}-\operatorname{tr}\Phi=-(\Phi_2+\Phi_3)$; exchanging $(x_1,x_2,x_3)\mapsto(x_1,x_3,x_2)$ preserves $|x|$ and $d^3x$ while sending $\Phi_2^{\rm int}(x_1,x_3)\mapsto\Phi_2^{\rm int}(x_1,x_2)=\Phi_3^{\rm int}(x_1,x_2)$, so $\int_{\mathbb R^3}\Phi_2\,d^3x=\int_{\mathbb R^3}\Phi_3\,d^3x$ and hence $Q_{22}=Q_{33}=-\frac12Q_{11}$. Because $\chi_{\rm st}(|x|/L)\ge 0$ everywhere, $\chi_{\rm st}(|x|/L)=1$ on $B_{3L/2}(0)$, and $g(x_1)>0$ almost everywhere on $B_{3L/2}(0)$, restricting the integral to $B_{3L/2}(0)$ and using $\int_{B_R(0)}(x_2^2+x_3^2)\,d^3x=\frac23\cdot 4\pi\int_0^Rr^4\,dr=\frac{8\pi}{15}R^5$ at $R=\frac32L$ ($R^5=\frac{243}{32}L^5$, so $\frac12\cdot\frac{8\pi}{15}\cdot\frac{243}{32}=\frac{81\pi}{40}$) together with $\rho_0^{\rm tot}L^5=E_0L^2=\bigl(\frac{27\pi A_*}{\tau}\bigr)(64c^2\tau^2)=1728\pi A_*c^2\tau$ ($\frac{81}{40}\times 1728=\frac{81\times 216}{5}=\frac{17496}{5}$) establishes (25).

Compare $T^{\mu\nu}_{\rm tot}$ against the smooth compactly supported pressureless dust reference tensor $T^{00}_{\rm ref}(x):=\varepsilon_{\rm tot}(|x|)$, $T^{0a}_{\rm ref}=T^{a0}_{\rm ref}:=0$, $T^{ab}_{\rm ref}:=0$, which obeys $\partial_\mu T^{\mu\nu}_{\rm ref}=0$ and the dominant energy condition, shares the exact pointwise energy density $T^{00}_{\rm ref}=T^{00}_{\rm tot}$ on all $\mathbb R^3$, and has identical boost inertia and active monopole mass $M_{\rm in}^{\rm ref}=M_{\rm active}^{\rm ref}=E_{\rm tot}/c^2$, while $Q^{\rm ref}_{ab}=0$. In the Riemann curvature convention $R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}+\Gamma^\rho_{\mu\alpha}\Gamma^\alpha_{\nu\sigma}-\Gamma^\rho_{\nu\alpha}\Gamma^\alpha_{\mu\sigma}$ of the [static stress-quadrupole construction](stress_quadrupole_at_equal_energy.md), the linearized electric tidal tensor $R^{(1)}_{0i0j}=-\frac12\partial_i\partial_jh_{00}=\frac{1}{c^2}\partial_i\partial_j\Phi$ is gauge-invariant under infinitesimal coordinate transformations on flat spacetime. For $|x|>2L$, $|x-y|^{-1}$ is smooth and harmonic in $y$ on a neighborhood of $\overline{B_{2L}(0)}\supseteq\operatorname{supp}\Phi$, so subtracting $\Phi_{\rm ref}$ from $\Phi_{\rm tot}$ cancels $\varepsilon_{\rm tot}(|y|)$ (and $U_{\rm col}$) identically, and integrating $\operatorname{tr}T_{\rm tot}(y)=\nabla_y^2\operatorname{tr}\Phi(y)-\sum_{m=2}^3\partial_{y_m}^2\Phi_m(y)$ twice by parts in $y$ (using $\Phi_1\equiv 0$ and $\partial_{y_m}^2(|x-y|^{-1})=\partial_{x_m}^2(|x-y|^{-1})$) yields
$$
\Delta\Phi(x):=\Phi_{\rm tot}(x)-\Phi_{\rm ref}(x)
=\frac{G}{c^2}\sum_{m=2}^{3}\int_{B_{2L}(0)}\Phi_m(y)\,\partial_{x_m}^2\!\left(\frac{1}{|x-y|}\right)d^3y\qquad(|x|>2L),
$$
$$
K_m^{(1)}(x,y):=\partial_{x_1}^2\partial_{x_m}^2\!\left(\frac{1}{|x-y|}\right)\quad(x\ne y,\ m=2,3),
$$
$$
\Delta R^{(1)}_{0101}(x):=R^{(1),{\rm tot}}_{0101}(x)-R^{(1),{\rm ref}}_{0101}(x)
=\frac{G}{c^4}\sum_{m=2}^{3}\int_{B_{2L}(0)}\Phi_m(y)\,K_m^{(1)}(x,y)\,d^3y\qquad(|x|>3L),
$$
$$
K_m^{(1)}((r,0,0),y)
=3R^{-5}-15(z_1^2+y_m^2)R^{-7}+105y_m^2z_1^2R^{-9}
=-\frac{12}{R^5}+\frac{15\rho_\perp^2+90y_m^2}{R^7}-\frac{105y_m^2\rho_\perp^2}{R^9}\quad(m=2,3),
\tag{26}
$$
where for $x=(r,0,0)$ ($r>3L$, strictly outside both sources) we set $z=x-y=(r-y_1,-y_2,-y_3)$, $R=|z|$, and $\rho_\perp^2=y_2^2+y_3^2=R^2-z_1^2$; the final equality in (26) substitutes $z_1^2=R^2-\rho_\perp^2$ after four direct differentiations of $R^{-1}$. At $y=0$, $K_2^{(1)}((r,0,0),0)=K_3^{(1)}((r,0,0),0)=-12r^{-5}<0$, whose integral against $\frac{G}{c^4}(\Phi_2(y)+\Phi_3(y))$ in (26) equals $-\frac{12G}{c^4r^5}\int_{B_{2L}(0)}(\Phi_2+\Phi_3)\,d^3y=-\frac{6GQ_{11}}{c^2r^5}<0$ by (25)—agreeing in exact sign and normalization with $\frac{1}{c^2}\partial_{x_1}^2\bigl(-\frac{GQ_{ab}n_an_b}{2|x|^3}\bigr)\big|_{x=(r,0,0)}=-\frac{GQ_{11}}{2c^2}\frac{d^2}{dr^2}(r^{-3})=-\frac{6GQ_{11}}{c^2r^5}$.

To bound the multipole remainder rigorously for every $r>3L$, put $\theta:=2L/r\in(0,2/3)$ and use $\Phi_m(-y)=\Phi_m(y)$ to replace $K_m^{(1)}((r,0,0),y)$ by $\frac12\bigl[K_m^{(1)}((r,0,0),y)+K_m^{(1)}((r,0,0),-y)\bigr]$. For $|y|\le 2L$, $R_\pm:=|(r,0,0)\mp y|\ge r-|y|\ge r(1-\theta)>0$ satisfies $R_\pm^2=r^2(1+u_\pm)$ with $u_\pm=\mp\frac{2y_1}{r}+\frac{|y|^2}{r^2}$ and $1+u_\pm\ge(1-\theta)^2$. By Taylor's theorem at $u=0$ on $h(u)=(1+u)^{-5/2}$ ($h'(0)=-5/2$, $h''(u)=\frac{35}{4}(1+u)^{-9/2}$), for each sign there is $\xi_\pm$ between $0$ and $u_\pm$ (so $1+\xi_\pm\ge(1-\theta)^2$) with $h(u_\pm)=1-\frac52u_\pm+\frac{35}{8}(1+\xi_\pm)^{-9/2}u_\pm^2$. Because $\frac12(u_++u_-)=|y|^2/r^2\le\theta^2$ cancels the odd $y_1$ term and $\frac12(u_+^2+u_-^2)=\frac{4y_1^2}{r^2}+\frac{|y|^4}{r^4}\le(4+\theta^2)\theta^2$, multiplying by $|-12|=12$ bounds the $R^{-5}$ difference by $r^{-5}\theta^2\bigl[30+\frac{105}{2}(1-\theta)^{-9}(4+\theta^2)\bigr]$. For the remaining terms of (26), $0\le y_m^2\le\rho_\perp^2\le R_\pm^2$ implies that both $\frac{15\rho_\perp^2+90y_m^2}{R_\pm^7}$ and $\frac{105y_m^2\rho_\perp^2}{R_\pm^9}$ lie in $\bigl[0,\frac{105\rho_\perp^2}{R_\pm^7}\bigr]$, so their difference has magnitude at most $\frac{105\rho_\perp^2}{R_\pm^7}\le 105r^{-5}\theta^2(1-\theta)^{-7}$. Integrating against $\Phi_2(y)+\Phi_3(y)\le\Phi_2^{\rm int}(y)+\Phi_3^{\rm int}(y)<\frac98\rho_0^{\rm tot}L^2$ from (20) over $B_{2L}(0)$ (volume $\frac{32\pi}{3}L^3$, with $\frac98\cdot\frac{32\pi}{3}=12\pi$) gives for every $r>3L$:
$$
\left|\Delta R^{(1)}_{0101}(r,0,0)-\left(-\frac{6GQ_{11}}{c^2r^5}\right)\right|
\le 12\pi\theta^2C_1(\theta)\,\frac{G\rho_0^{\rm tot}L^5}{c^4r^5},\qquad
C_1(\theta):=30+\frac{105}{2}(1-\theta)^{-9}(4+\theta^2)+105(1-\theta)^{-7}.
\tag{27}
$$
As $r\to\infty$, $\theta=2L/r\to 0$ and $C_1(\theta)\to 345$, so the remainder is $O(r^{-7})$, establishing the exact asymptotic contrast. At the explicit finite exterior point $p_*:=(80L,0,0)=(640c\tau,0,0)$ ($r_*=80L>3L$, $\theta_*=2L/r_*=1/40$), $\frac{40}{39}<\frac{10}{9}$ and $(10/9)^3=\frac{1000}{729}<\frac75$ give $(1-\theta_*)^{-7}<(1-\theta_*)^{-9}<(7/5)^3=\frac{343}{125}<3$; together with $4+\theta_*^2=4+\frac{1}{1600}<\frac{41}{10}$, this yields $C_1(1/40)<30+\frac{315\cdot 41}{20}+315=990.75<1000$ and $12\theta_*^2C_1(1/40)<\frac{12\cdot 1000}{1600}=\frac{15}{2}$. Combining (27) with $-\frac{6GQ_{11}}{c^2r_*^5}<-\frac{243\pi}{20}\frac{G\rho_0^{\rm tot}L^5}{c^4r_*^5}$ from (25) and $\frac{243}{20}-\frac{15}{2}=\frac{93}{20}$ proves
$$
\boxed{\lim_{r\to\infty}r^5\Delta R^{(1)}_{0101}(r,0,0)
=-\frac{6GQ_{11}}{c^2}<-\frac{104976\pi^2}{5}\frac{GA_*\tau}{c^2}<0,}
$$
$$
\boxed{\Delta R^{(1)}_{0101}(80L,0,0)
<-\frac{93\pi}{20}\frac{G\rho_0^{\rm tot}}{80^5c^4}
=-\frac{2511\pi^2}{10240\cdot 80^5}\frac{GA_*}{c^7\tau^4}<0.}
\tag{28}
$$
For nearby freely falling test bodies initially at rest near $p_*=(80L,0,0)$ separated longitudinally by $\xi^1e_1$, the leading geodesic-deviation relative-acceleration coefficient $\mathcal K_1=-c^2R^{(1)}_{0101}$ satisfies $\Delta\mathcal K_1(p_*)=-c^2\Delta R^{(1)}_{0101}(p_*)>0$, reflecting enhanced radial tidal stretching along the prolate $e_1$-quadrupole axis relative to the matched-density spherical dust reference.

---

## 6. Complete 60-history source ledger, dimensional audit, and scope boundaries

Conditional on the fixed prepared prefix $a\prec b$ with marks $(i,0)$ and descendant counters $(1,0)$ for $i\in\{0,1\}$, the native four-birth probability law from the [finite interval and source specification](finite_interval_action_and_source_preparation.md) and [prepared source ledger](native_source_readout_response.md) is retained without modification. Each of the 15 structural predecessor-ideal rows $(I_x,I_y)$ splits into four fair ordered suffix-mark pairs $(b_3,b_4)\in\{0,1\}^2$, each carrying exact conditional probability $P_i(I_x,I_y,b_3,b_4)=\frac14P_i(I_x,I_y)$ over denominator $5280=4\times 1320$:

| Row | $I_x$ | $I_y$ | $1320P_0(I_x,I_y)$ | $1320P_1(I_x,I_y)$ | $5280P_0(I_x,I_y,b_3,b_4)$ | $5280P_1(I_x,I_y,b_3,b_4)$ | $3+1$D cavity–collar status |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | $\varnothing$ | $\varnothing$ | 6 | 6 | 6 | 6 | available (4 marked histories) |
| 2 | $\varnothing$ | $x$ | 6 | 6 | 6 | 6 | available (4 marked histories) |
| 3 | $\varnothing$ | $a$ | 5 | 10 | 5 | 10 | available (4 marked histories) |
| 4 | $\varnothing$ | $ab$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 5 | $\varnothing$ | $ax$ | 33 | 33 | 33 | 33 | available (4 marked histories) |
| 6 | $\varnothing$ | $abx$ | 195 | 195 | 195 | 195 | available (4 marked histories) |
| 7 | $a$ | $\varnothing$ | 5 | 10 | 5 | 10 | available (4 marked histories) |
| 8 | $a$ | $a$ | 5 | 10 | 5 | 10 | available (4 marked histories) |
| 9 | $a$ | $ab$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 10 | $a$ | $ax$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 11 | $a$ | $abx$ | 172 | 392 | 172 | 392 | available (4 marked histories) |
| 12 | $ab$ | $\varnothing$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 13 | $ab$ | $a$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 14 | $ab$ | $ab$ | 19 | 14 | 19 | 14 | available (4 marked histories) |
| 15 | $ab$ | $abx$ | 779 | 574 | 779 | 574 | available (4 marked histories) |
| **Total** | **15 rows** | **60 marked** | **1320** | **1320** | **5280** ($\sum_{b_3,b_4}$) | **5280** ($\sum_{b_3,b_4}$) | **available: 1320/1320 (60/60)** |

**Table 3.** Complete 15-row / 60-marked-history native probability ledger (concatenation denotes a set; columns 6–7 give the numerator over $5280$ of each individual suffix-mark continuation $(b_3,b_4)\in\{0,1\}^2$, summing across the four fair mark pairs per row to $4\times 1320=5280$) and upgraded $3+1$D static cavity–collar availability status.

All 15 structural rows ($264+220+836=1320$ for $P_0$ and $264+440+616=1320$ for $P_1$) are now `"available"` inside one $3+1$D compact cavity–collar source. Note the exact physical role of branch labels in this ledger: $\Omega_0$, $H_{\rm sc}$, $T^{\mu\nu}_{\rm tot}$, $\bar h_{\mu\nu}$, $M_{\rm in}=M_{\rm active}$, $Q_{ab}$, and $\Delta R^{(1)}_{0101}$ are fixed once and for all prior to suffix births and do **not** vary across branches or respond to $(i,I_x,I_y,b_3,b_4)$; the realized native ideals $(I_x,I_y)$ select which interior spacetime points $(t_r,x_r)\in\mathbb R\times\operatorname{int}(\Omega)$ are sampled in (9) without back-reacting on $T^{\mu\nu}_{\rm tot}$ or reweighting $P_0,P_1$.

The normalization, dimensional, and weak-field relations are explicit:
$$
\frac{L}{c\tau}=8,\qquad
\frac{V}{c^3\tau^3}=512,\qquad
\frac{E_0\tau}{A_*}=27\pi,\qquad
F_*^2=\frac{A_*c^2}{\kappa V\omega_0\beta c_0}
=\frac{3\tan(\pi/48)\,A_*}{752\pi\kappa c\tau^2\beta},
$$
$$
\rho_0^{\rm tot}=\frac{27\pi A_*}{512c^3\tau^4},\qquad
g:=\frac{G\rho_0^{\rm tot}L^2}{c^4}=\frac{27\pi GA_*}{8c^5\tau^2}\ll 1.
\tag{29}
$$
If $\Phi_{\rm sc}$ carries field units $\mathcal F$, then $\Psi_{\rm cal},B_m,q_m,F_*$ carry units $\mathcal F$, $\Psi,\phi_r,\beta,\theta_m,c_m,\eta_m$ are dimensionless, $\Gamma_{\rm read}$ carries units $\text{length}^{-3}$, $\kappa$ carries units $\text{energy}/(\mathcal F^2\cdot\text{length})$, $\mu$ carries units $\text{energy}\cdot\text{time}^2/\mathcal F^2$, $p_m$ carries units $\text{action}/\mathcal F$, every component of $T^{\mu\nu}_{\rm sc},T^{\mu\nu}_{\rm tot},T^{\mu\nu}_{\rm ref}$ and $\rho_0^{\rm tot},U_{\rm col}$ carries energy-density units $\text{energy}/\text{length}^3$, and $\Phi^{\rm int}_{mn},\Phi_{mn},g(x_1)$ carry force units $\text{energy}/\text{length}$. Rescaling $\Phi_{\rm sc}\mapsto s\Phi_{\rm sc}$ and $\kappa\mapsto\kappa/s^2$ ($s>0$) rescales $B_m,F_*,\Psi_{\rm cal}$ by $s$ while leaving $H_{\rm sc}$, $\eta_m$, $\Gamma_{\rm read}$, $T^{\mu\nu}_{\rm tot}$, $M_{\rm in}$, $M_{\rm active}$, $Q_{ab}$, and $\Delta R^{(1)}_{0101}$ invariant. In the gravitational sector, $M_{\rm in}$ and $M_{\rm active}$ have mass units, $Q_{ab}$ and $A_*\tau$ have units $\text{mass}\cdot\text{length}^2$, $\bar h_{\mu\nu}$ and $h_{\mu\nu}$ are dimensionless, $\Phi_{\rm tot}$ has velocity-squared units, $R^{(1)}_{0101}$ and $GA_*/(c^7\tau^4)$ have curvature units $\text{length}^{-2}$, and $\Delta\mathcal K_1$ has units $\text{time}^{-2}$. Because $M_{\rm st}^{(12)}$ in (21) and the radial bump integrals are fixed $O(1)$ dimensionless constants independent of $g$, the single supplied weak-field condition $g\ll 1$ in (29) keeps $|\bar h_{\mu\nu}|=O(g)\ll 1$ everywhere on $\mathbb R^3$, with matter held at zeroth order.

**Strict separation of native vs. externally supplied ingredients:**
- **Supplied by the native growth law:** Only the 15 four-birth predecessor-ideal pairs $(I_x,I_y)$ above $a\prec b$, the fair newborn-mark factor $1/4$ per structural row, and the exact conditional probability laws $P_0,P_1$ over the 60 marked histories ($1320$ structural denominator, $5280$ marked denominator).
- **Externally supplied mathematical and physical choices:** The continuum background $\mathbb R^{1,3}$ and metric signature $(-+++)$, physical constants $c,\tau,A_*,\kappa,G>0$, the target-first Johnston normalization $\beta>0$ and released prefix $W_2^{\rm ext}$, the centered cubic domain $\Omega=[-L/2,L/2]^3$ ($L=8c\tau$) with homogeneous Neumann boundary conditions, the 12 odd-harmonic standing modes ($N=24,M=12$, $\tilde\varphi_m=2\pi-\varphi_m$) and Gaussian ground state $\Omega_0\in L^2(\mathbb R^{12})$, the Neumann-cosine readout kernel $\Gamma_{\rm read}$, the offset interior worldline segment (9) at $x_{\rm ref}=-L/4$, the unshifted Weyl-ordered kinetic stress tensor (16), the smooth classical Beltrami collar potential $\Phi_{mn}$ and radial plateau $U_{\rm col}$, the weak-field regime $g\ll 1$, and the ideal exterior tidal readout channel.

**Explicit non-claims and scope limits:**
1. *No native derivation of geometry, gravity, or calibration, and non-uniqueness of attachment choices.* Neither $3+1$D Minkowski geometry, linearized Einstein gravity, nor the numerical physical values of $c,\tau,A_*,\kappa,G$ are derived from native order or counting. The reference offset $x_{\rm ref}=-L/4$, harmonic order $N=24$, and unaliased advances $\theta_m$ are sufficient rather than unique: larger even harmonic counts $N=2M\ge 24$, positive frequency aliases, or shifted interior intervals keeping reflected image cones outside $[-(N-1),N-1]$ also preserve (11) while changing off-cone covariances, $E_0$, and $Q_{11}$.
2. *Finite-mode projector vs. continuum quantum field theory.* Retaining 12 oscillator pairs on $L^2(\mathbb R^{12})$ (infinite-dimensional Hilbert space, finite mode count) yields the rank-12 Neumann projection kernel in (5) rather than a three-dimensional Dirac delta, and realizes exact causal commutators on the $\frac13\mathbb Z^2$ interior lattice up to $|\nu_\pm|\le 23$ rather than continuum microcausality across $\Omega$. The unshifted ground energy $E_0=27\pi A_*/\tau$ is a finite-mode oscillator integral, not a renormalized continuum Casimir energy.
3. *Classical collar admissibility, unassigned operational costs, and Status-M quarantine.* Satisfying $\partial_\mu T^{\mu\nu}_{\rm tot}=0$ and $\|T^{ab}_{\rm tot}\|\le T^{00}_{\rm tot}$ establishes mathematical conservation and dominant-energy admissibility of the composite source; it does not supply a constitutive equation of state, elastic stability of a physical casing, or nonlinear self-gravitating equilibrium, nor does an oscillator gap $\theta_m$ define particle rest mass. Ground-state preparation, maintaining Neumann walls and collar stresses, applying $\Gamma_{\rm read}$, sequentially accessing noncommuting branch operators, measuring weak tidal curvature, and resetting the apparatus carry unassigned physical work and thermodynamic costs. Software execution remains paused, and all Track-B / Status-M ontological commitments (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined and enter no equation, variable, or inference of this calculation.

The scoped decision is therefore **compatible across all 15 structural rows ($1320/1320$, all 60 marked histories per prepared source) as a single history-independent $3+1$D compact cubic homogeneous-Neumann cavity and conserved Beltrami collar source, satisfying $\partial_\mu T^{\mu\nu}_{\rm tot}=0$, $\|T^{ab}_{\rm tot}\|\le T^{00}_{\rm tot}$, $M_{\rm in}=M_{\rm active}=(E_0+E_{\rm support})/c^2$, and strictly nonzero exterior stress-quadrupole tidal curvature contrast**.

## Scientific review

All-Branch 3+1D Cavity Gravity Author derived the 12-mode cubic homogeneous-Neumann cavity attachment, method-of-images boundary-reflection cancellation, modulo-24 Vandermonde covariance positivity, stagewise Weyl-algebra preservation across all 60 marked histories, axisymmetric smooth Beltrami collar and dominant-energy bound, whole-space linearized gravitational potential, inertia–active-mass identity, and exterior stress-quadrupole tidal contrast. Independent All-Branch 3+1D Gravity Reviewer independently verified all 15 embedding rows, square-wave and commutator identities, Vandermonde invertibility, paired cotangent/cosecant lags, collar bump bounds, active quadrupole lower bound, fourth-derivative Newtonian kernel, finite-distance remainder at $p_*=(80L,0,0)$, native probability sums, dimensional relations, and scope boundaries. Prospective protocol SHA-256 f05ef791a62c5c59d697bffac7d28c1bc454e4fce2fac161d79dadce97dba258; accepted author report SHA-256 839b05ad6fb5127bc78de06352da4d12ac6f8993a8d10e4932172f4f59229093; independent scientific review SHA-256 c9706ec16cc3e0f941d5f0103a722ba718ed8b77a78675c6c3653310eb8887eb.
