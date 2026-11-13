# Coherent two-mode cavity beat superpotential and retarded tidal curvature contrast

Conditional analytic dynamical source and retarded curvature construction

Yes. Preparing the unchanged two-mode homogeneous-Neumann cubic cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ ($L=4c\tau$, $V=64c^3\tau^3$) in the opposite-phase single-excitation quantum states $\psi_\pm=\frac{1}{\sqrt2}(|1,0\rangle\pm|0,1\rangle)$ and comparing them against each other and against their equal-weight incoherent mixture $\rho_{\rm inc}=\frac12|1,0\rangle\langle 1,0|+\frac12|0,1\rangle\langle 0,1|$ yields an exact smooth spatially compact four-dimensional conserved stress-energy completion on $\mathbb R^{1,3}$ that satisfies the full Lorentzian dominant energy condition everywhere and produces a strictly nonzero outgoing $1/r$ retarded electric-curvature contrast along the equatorial bisector $n_*=\frac{1}{\sqrt2}(e_1+e_2)$. Inside $\Omega$, the Weyl-ordered expectation $T^{\mu\nu}_{{\rm cav},\pm}(t,x)=\langle\psi_\pm,T^{\mu\nu}_{\rm sc}(t,x)\psi_\pm\rangle$ splits into the static doubled ground stress $2T^{\mu\nu}_{\rm cav,vac}(x)=\operatorname{Tr}(\rho_{\rm inc}T^{\mu\nu}_{\rm sc}(t,x))$ plus an oscillating interference tensor $\pm T^{\mu\nu}_{\rm beat}(t,x)$ at beat frequency $\Omega_{\rm beat}=\omega_2-\omega_1=\frac{\pi}{2\tau}$ and wavenumber $k_{\rm beat}=\frac{\Omega_{\rm beat}}{c}=\frac{2\pi}{L}$, conserving four-momentum in $\operatorname{int}(\Omega)$ with constant bulk energy $2E_0=\frac{3\pi A_*}{\tau}$, zero bulk momentum, zero normal energy flux across $\partial\Omega$, and zero-offset interior dominant-energy positivity. Because $\partial_aT^{ab}_{\rm beat}=-\partial_0T^{0b}_{\rm beat}\ne 0$, no purely spatial Beltrami stress collar can extend $T^{ab}_{\rm beat}$ outside $\Omega$. Lifting $T^{\mu\nu}_{\rm beat}$ instead through a Riemann-symmetric four-dimensional superpotential $(\Sigma^{\rm beat},\Phi^{\rm beat})$ cut off on a thin product cube inside $B_L(0)$ and supported by an explicit static collar plateau $U_{\rm col}^{\rm dyn}$ preserves pointwise interior agreement on $\mathbb R\times\overline\Omega$, identical constant total energy $E_{\rm tot}$, zero total momentum, and vanishing beat mass monopole, dipole, quadrupole, and octupole moments ($\ell=0,1,2,3$) at every time $t\in\mathbb R$. Although leading mass-quadrupole and mass-octupole radiation formulas therefore predict zero contrast, retaining the exact spatial retardation phase $e^{-ik_{\rm beat}n\cdot y}$ in the harmonic-gauge retarded integral yields a strictly positive gauge-invariant asymptotic curvature contrast ${\cal C}_{\rm beat}=\lim_{r\to\infty}r[\mathcal E_+(r/c,r)-\mathcal E_-(r/c,r)]>0$ along $n_*$, while all $1/r$ beat radiation vanishes identically along the six coordinate axes $\pm e_1,\pm e_2,\pm e_3$.

This is a conditional semiclassical source-and-readout calculation on a prescribed flat Minkowski background within first-order linearized general relativity under an eternal harmonic steady-state ansatz. It is not a native spatial or gravitational derivation, a quantized gravitational field or superposition of geometries, a microscopic elastodynamic model of cavity walls, a nonlinear self-gravitating or $O(G^2)$ radiation-reaction closure, or an operational state-preparation, sustaining, detection, and reset protocol.

The [compact cavity source](compact_cavity_source_for_four_chain_field.md) supplies the centered homogeneous-Neumann cubic domain $\Omega$, the two axial standing modes, the interior four-tick probe match, and the static ground-state Beltrami collar $T^{\mu\nu}_{\rm tot,vac}$. The [stationary two-mode construction](stationary_dynamics_for_four_chain_fields.md) and [periodic scalar source lift](local_scalar_source_for_four_chain_field.md) supply the canonical oscillator algebra, unaliased phases $(\theta_1,\theta_2)=(5\pi/4,7\pi/4)$, and Weyl-ordered scalar stress tensor. The [coherent inertia analysis](coherent_inertia_from_opposite_kicks.md) motivates testing opposite-phase superpositions within the single-excitation doublet $\operatorname{span}\{|1,0\rangle,|0,1\rangle\}$, while the [static stress-quadrupole example](stress_quadrupole_at_equal_energy.md) and [retarded stress calculation](retarded_stress_at_fixed_density.md) supply the linearized harmonic-gauge, outgoing convolution, and electric-curvature conventions retained below. The [finite source table](finite_interval_action_and_source_preparation.md) supplies the unchanged 60-history native probability law.

## 1. Opposite-phase single-excitation states and interior beat stress-energy

Retain the two dimensionless canonical quadrature pairs $(Q_1,P_1),(Q_2,P_2)$ on $L^2(\mathbb R^2,dq_1\,dq_2)$ acting on the common invariant Schwartz domain ${\cal S}(\mathbb R^2)$ via $(Q_j\psi)(q)=q_j\psi(q)$ and $(P_j\psi)(q)=-i\partial_{q_j}\psi(q)$, with $[Q_j,P_k]=i\delta_{jk}I$ and $[Q_j,Q_k]=[P_j,P_k]=0$ on ${\cal S}(\mathbb R^2)$. Define the ladder operators $\mathfrak a_j:=\frac{1}{\sqrt2}(Q_j+iP_j)$ and $\mathfrak a_j^\dagger:=\frac{1}{\sqrt2}(Q_j-iP_j)$ on ${\cal S}(\mathbb R^2)$, which satisfy $[\mathfrak a_j,\mathfrak a_k^\dagger]=\delta_{jk}I$, $[\mathfrak a_j,\mathfrak a_k]=0$, and $\mathfrak a_j^\dagger\mathfrak a_j+\frac12I=\frac12(Q_j^2+P_j^2)$. Retain from the [stationary two-mode construction](stationary_dynamics_for_four_chain_fields.md) the unaliased phase advances, dimensionless generator, and four-tick chain observables
$$
 \theta_1=\frac{5\pi}{4},\quad \theta_2=\frac{7\pi}{4},\qquad
 a_1=\sqrt{\frac{\beta}{2}(\sqrt2-1)},\quad
 a_2=\sqrt{\frac{\beta}{2}(\sqrt2+1)}\quad(\beta>0),
$$
$$
 K=\frac12\sum_{j=1}^2\theta_j(Q_j^2+P_j^2)
  =\sum_{j=1}^2\theta_j\left(\mathfrak a_j^\dagger\mathfrak a_j+\frac12I\right),\qquad
 \phi_n=e^{inK}\phi_0e^{-inK}
  =\sum_{j=1}^2a_j\bigl(Q_j\cos n\theta_j+P_j\sin n\theta_j\bigr)
 \quad(n=0,1,2,3). \tag{1}
$$
In terms of the normalized product Gaussian ground state $\psi_0(q_1,q_2)=|0,0\rangle(q_1,q_2)=\pi^{-1/2}\exp[-(q_1^2+q_2^2)/2]\in{\cal S}(\mathbb R^2)$ satisfying $\mathfrak a_1\psi_0=\mathfrak a_2\psi_0=0$, define the orthonormal single-excitation basis states $|1,0\rangle:=\mathfrak a_1^\dagger|0,0\rangle$ and $|0,1\rangle:=\mathfrak a_2^\dagger|0,0\rangle$, with explicit Schwartz wavefunctions $|1,0\rangle(q_1,q_2)=\sqrt2\,q_1\psi_0(q_1,q_2)$ and $|0,1\rangle(q_1,q_2)=\sqrt2\,q_2\psi_0(q_1,q_2)$, together with the opposite-phase coherent superpositions and equal-weight incoherent mixture
$$
 \psi_\pm:=\frac{1}{\sqrt2}\bigl(|1,0\rangle\pm|0,1\rangle\bigr)\in{\cal S}(\mathbb R^2),\qquad
 \rho_{\rm inc}:=\frac12|1,0\rangle\langle 1,0|+\frac12|0,1\rangle\langle 0,1|
 =\frac12|\psi_+\rangle\langle\psi_+|+\frac12|\psi_-\rangle\langle\psi_-|.
$$
Direct $L^2(\mathbb R^2)$ integration gives $\|\psi_\pm\|^2=1$, $\langle\psi_+,\psi_-\rangle=0$, $\operatorname{Tr}\rho_{\rm inc}=1$, and $\rho_{\rm inc}\succeq 0$.

Supply flat Cartesian coordinates $(x^0,x_1,x_2,x_3)$ on $\mathbb R^{1,3}$ with $x^0=ct$, metric $\eta=\operatorname{diag}(-1,1,1,1)$, orthonormal spatial triad $e_1,e_2,e_3$, and positive constants $c,\tau,A_*,\kappa>0$. Retain verbatim from the [compact cavity source](compact_cavity_source_for_four_chain_field.md) the centered cubic cavity $\Omega=[-L/2,L/2]^3\subset\mathbb R^3$ of side $L=4c\tau$ and volume $V=L^3=64c^3\tau^3$, mode frequencies $\omega_1=\frac{\theta_1}{\tau}=\frac{5\pi}{4\tau}$ and $\omega_2=\frac{\theta_2}{\tau}=\frac{7\pi}{4\tau}$, wavevectors $k_1=\frac{5\pi}{L}e_1$ and $k_2=\frac{7\pi}{L}e_2$ ($\omega_j=c|k_j|$), and homogeneous-Neumann standing profiles
$$
 \alpha_1(x_1)=\frac{5\pi}{L}\left(x_1+\frac L2\right),\qquad
 \alpha_2(x_2)=\frac{7\pi}{L}\left(x_2+\frac L2\right),
$$
$$
 u_1(x_1)=\cos\alpha_1(x_1)=-\sin\!\left(\frac{5\pi}{L}x_1\right),\qquad
 u_2(x_2)=\cos\alpha_2(x_2)=+\sin\!\left(\frac{7\pi}{L}x_2\right),
$$
$$
 B_j=\sqrt{\frac{2A_*c^2}{\kappa V\omega_j}},\qquad
 X_j(t)=Q_j\cos\omega_jt+P_j\sin\omega_jt
  =\frac{1}{\sqrt2}\bigl(\mathfrak a_je^{-i\omega_jt}+\mathfrak a_j^\dagger e^{i\omega_jt}\bigr),
$$
$$
 Y_j(t)=P_j\cos\omega_jt-Q_j\sin\omega_jt
  =-\frac{i}{\sqrt2}\bigl(\mathfrak a_je^{-i\omega_jt}-\mathfrak a_j^\dagger e^{i\omega_jt}\bigr),\qquad
 \Psi(t,x)=\sum_{j=1}^2B_ju_j(x_j)X_j(t)\quad(x\in\overline\Omega). \tag{2}
$$
Here $\cos(\varphi+5\pi/2)=-\sin\varphi$ and $\cos(\varphi+7\pi/2)=+\sin\varphi$ verify both trigonometric forms in (2), with $\partial_1u_1(x_1)=-|k_1|\sin\alpha_1(x_1)=-\frac{5\pi}{L}\cos(\frac{5\pi}{L}x_1)$ and $\partial_2u_2(x_2)=-|k_2|\sin\alpha_2(x_2)=+\frac{7\pi}{L}\cos(\frac{7\pi}{L}x_2)$ vanishing at $x_1=\pm L/2$ and $x_2=\pm L/2$, respectively, so $n\cdot\nabla u_j=0$ on all six faces of $\partial\Omega$. On ${\cal S}(\mathbb R^2)$, the cavity Hamiltonian $H_{\rm sc}=\int_\Omega\frac{\kappa}{2}[c^{-2}\dot\Psi^2+|\nabla\Psi|^2]\,d^3x=\frac{A_*}{\tau}K$ generates (2) without normal-ordering subtraction or identity offset, and evaluating $\Psi(t,x)$ at the interior point $x_*=(-\frac{L}{10}+\frac{L}{5\pi}\arccos[(\sqrt2-1)\sqrt{5/7}],\frac{L}{14},0)\in\operatorname{int}(\Omega)$ with $F_*=B_2/a_2$ preserves the state-independent operator identity $\Psi(n\tau,x_*)=F_*\phi_n$ ($n=0,1,2,3$) on ${\cal S}(\mathbb R^2)$. On the single-excitation eigenstates, $H_{\rm sc}|1,0\rangle=\frac{11\pi A_*}{4\tau}|1,0\rangle$ and $H_{\rm sc}|0,1\rangle=\frac{13\pi A_*}{4\tau}|0,1\rangle$, so $\langle\psi_\pm,H_{\rm sc}\psi_\pm\rangle=\operatorname{Tr}(\rho_{\rm inc}H_{\rm sc})=\frac{3\pi A_*}{\tau}=2E_0$.

On $\mathbb R\times\overline\Omega$ (and never outside $\overline\Omega$), retain the Weyl-ordered minimally coupled scalar stress tensor
$$
 T^{\mu\nu}_{\rm sc}(t,x)=\kappa\left[
 \frac12\{\partial^\mu\Psi,\partial^\nu\Psi\}-\frac12\eta^{\mu\nu}Z\right],\qquad
 Z=\frac12\eta^{\alpha\gamma}\{\partial_\alpha\Psi,\partial_\gamma\Psi\}
  =-\frac{\dot\Psi^2}{c^2}+|\nabla\Psi|^2\qquad(x\in\overline\Omega), \tag{3}
$$
so $T^{00}_{\rm sc}=\frac{\kappa}{2}[c^{-2}\dot\Psi^2+|\nabla\Psi|^2]$, $T^{0a}_{\rm sc}=T^{a0}_{\rm sc}=-\frac{\kappa}{2c}\{\dot\Psi,\partial_a\Psi\}$ (since $\partial^0\Psi=-\partial_0\Psi=-c^{-1}\dot\Psi$ and $\partial^a\Psi=+\partial_a\Psi$), and $T^{ab}_{\rm sc}=\frac{\kappa}{2}\{\partial_a\Psi,\partial_b\Psi\}+\frac{\kappa}{2}\delta^{ab}[c^{-2}\dot\Psi^2-|\nabla\Psi|^2]$. Set $E_1=\frac{A_*\omega_1}{2}=\frac{5\pi A_*}{8\tau}$, $E_2=\frac{A_*\omega_2}{2}=\frac{7\pi A_*}{8\tau}$, $E_0=E_1+E_2=\frac{3\pi A_*}{2\tau}$, $\rho_j=\frac{E_j}{V}=\frac{\kappa}{4}B_j^2|k_j|^2$ ($j=1,2$), and $\rho_0=\rho_1+\rho_2=\frac{3\pi A_*}{128c^3\tau^4}$. From the [compact cavity source](compact_cavity_source_for_four_chain_field.md), the ground-state expectation $T^{\mu\nu}_{\rm cav,vac}(x):=\langle\psi_0,T^{\mu\nu}_{\rm sc}(t,x)\psi_0\rangle$ on $\overline\Omega$ is static with $T^{00}_{\rm cav,vac}=\rho_0$, $T^{0a}_{\rm cav,vac}=0$, and $T^{ab}_{\rm cav,vac}=\sum_{j=1}^2\rho_j[d_j^ad_j^b+(\delta^{ab}-d_j^ad_j^b)\cos 2\alpha_j]$ ($d_1=e_1$, $d_2=e_2$).

Now evaluate the expectations of $T^{\mu\nu}_{\rm sc}(t,x)$ in $\psi_\pm$ and $\rho_{\rm inc}$ on $\mathbb R\times\overline\Omega$. In any Fock state $|n_1,n_2\rangle$ ($n_j\in\{0,1\}$), expanding (2) gives $\langle n_1,n_2|X_j(t)^2|n_1,n_2\rangle=\langle n_1,n_2|Y_j(t)^2|n_1,n_2\rangle=\frac12\langle n_1,n_2|(\mathfrak a_j\mathfrak a_j^\dagger+\mathfrak a_j^\dagger\mathfrak a_j)|n_1,n_2\rangle=n_j+\frac12$, $\langle n_1,n_2|\{X_j(t),Y_j(t)\}|n_1,n_2\rangle=0$, and zero for every cross-mode product ($j\ne k$). Averaging $(n_1,n_2)=(1,0)$ and $(0,1)$ with equal weights $\frac12,\frac12$ yields $\frac12(\frac32+\frac12)=1=2\langle\psi_0,X_j(t)^2\psi_0\rangle=2\langle\psi_0,Y_j(t)^2\psi_0\rangle$ for both $j=1,2$, proving $\operatorname{Tr}\bigl(\rho_{\rm inc}T^{\mu\nu}_{\rm sc}(t,x)\bigr)=2T^{\mu\nu}_{\rm cav,vac}(x)$ pointwise on $\mathbb R\times\overline\Omega$. For the off-diagonal interference term $\operatorname{Re}\langle 1,0|T^{\mu\nu}_{\rm sc}(t,x)|0,1\rangle$, single-mode quadratic operators vanish between $|1,0\rangle$ and $|0,1\rangle$ by orthogonality in the unacted factor, while mode-1 and mode-2 operators commute on ${\cal S}(\mathbb R^2)$. From (2), $\langle 1|X_1(t)|0\rangle=\frac{1}{\sqrt2}e^{i\omega_1t}$, $\langle 0|X_2(t)|1\rangle=\frac{1}{\sqrt2}e^{-i\omega_2t}$, $\langle 1|Y_1(t)|0\rangle=+\frac{i}{\sqrt2}e^{i\omega_1t}$, and $\langle 0|Y_2(t)|1\rangle=-\frac{i}{\sqrt2}e^{-i\omega_2t}$. With $\Omega_{\rm beat}:=\omega_2-\omega_1=\frac{\pi}{2\tau}>0$, the four cross-mode matrix elements and their real parts are
$$
 \langle 1,0|X_1(t)X_2(t)|0,1\rangle=\frac12e^{-i\Omega_{\rm beat}t},\qquad
 \langle 1,0|Y_1(t)Y_2(t)|0,1\rangle=+\frac12e^{-i\Omega_{\rm beat}t},
$$
$$
 \langle 1,0|Y_1(t)X_2(t)|0,1\rangle=+\frac{i}{2}e^{-i\Omega_{\rm beat}t},\qquad
 \langle 1,0|X_1(t)Y_2(t)|0,1\rangle=-\frac{i}{2}e^{-i\Omega_{\rm beat}t},
$$
$$
 T^{\mu\nu}_{{\rm cav},\pm}(t,x):=\langle\psi_\pm,T^{\mu\nu}_{\rm sc}(t,x)\psi_\pm\rangle
  =2T^{\mu\nu}_{\rm cav,vac}(x)\pm T^{\mu\nu}_{\rm beat}(t,x),\qquad
 \operatorname{Tr}\bigl(\rho_{\rm inc}T^{\mu\nu}_{\rm sc}(t,x)\bigr)=2T^{\mu\nu}_{\rm cav,vac}(x)\quad(x\in\overline\Omega), \tag{4}
$$
where $T^{\mu\nu}_{\rm beat}(t,x):=\operatorname{Re}\langle 1,0|T^{\mu\nu}_{\rm sc}(t,x)|0,1\rangle$. Using $i e^{-i\Omega_{\rm beat}t}=\sin(\Omega_{\rm beat}t)+i\cos(\Omega_{\rm beat}t)$, we have $\operatorname{Re}\langle 1,0|X_1X_2|0,1\rangle=\operatorname{Re}\langle 1,0|Y_1Y_2|0,1\rangle=\frac12\cos(\Omega_{\rm beat}t)$, $\operatorname{Re}\langle 1,0|Y_1X_2|0,1\rangle=+\frac12\sin(\Omega_{\rm beat}t)$, and $\operatorname{Re}\langle 1,0|X_1Y_2|0,1\rangle=-\frac12\sin(\Omega_{\rm beat}t)$.

Define the beat wavenumber, beat energy-density amplitude, and smooth mode-product profile on $\mathbb R^3$:
$$
 \Omega_{\rm beat}=\omega_2-\omega_1=\frac{\pi}{2\tau},\qquad
 k_{\rm beat}=\frac{\Omega_{\rm beat}}{c}=|k_2|-|k_1|=\frac{2\pi}{L}=\frac{\pi}{2c\tau},
$$
$$
 \rho_{\rm beat}:=2\sqrt{\rho_1\rho_2}=\frac{\sqrt{35}\,\pi A_*}{256c^3\tau^4}>0,\qquad
 G_{\rm int}(x):=u_1(x_1)u_2(x_2)=\cos\alpha_1(x_1)\cos\alpha_2(x_2)
  =-\sin\!\left(\frac{5\pi}{L}x_1\right)\sin\!\left(\frac{7\pi}{L}x_2\right).
$$
Since $\frac{\kappa}{4}B_j^2|k_j|^2=\rho_j$, we have $\frac{\kappa}{2}B_1B_2|k_1||k_2|=2\sqrt{\rho_1\rho_2}=\rho_{\rm beat}$, i.e., $\kappa B_1B_2=\frac{2\rho_{\rm beat}}{|k_1||k_2|}$. Substituting $\dot\Psi/c=\sum_{j=1}^2B_j|k_j|u_jY_j$, $\partial_1\Psi=B_1(\partial_1u_1)X_1$, $\partial_2\Psi=B_2(\partial_2u_2)X_2$, and $\partial_3\Psi=0$ into (3) yields every component of $T^{\mu\nu}_{\rm beat}$:
- In $c^{-2}\dot\Psi^2$, the cross term $2B_1B_2|k_1||k_2|u_1u_2Y_1Y_2$ has real matrix element $B_1B_2|k_1||k_2|G_{\rm int}(x)\cos(\Omega_{\rm beat}t)=\frac{2\rho_{\rm beat}}{\kappa}G_{\rm int}(x)\cos(\Omega_{\rm beat}t)$.
- In $|\nabla\Psi|^2=(\partial_1\Psi)^2+(\partial_2\Psi)^2$, orthogonality $e_1\cdot e_2=0$ leaves no cross-mode term, so $\langle 1,0||\nabla\Psi|^2|0,1\rangle=0$ and $\langle 1,0|(\partial_a\Psi)^2|0,1\rangle=0$ for each $a\in\{1,2,3\}$. Hence $T^{00}_{\rm beat}$ and all three diagonal stresses $T^{11}_{\rm beat}=T^{22}_{\rm beat}=T^{33}_{\rm beat}$ equal $\frac{\kappa}{2}\operatorname{Re}\langle 1,0|c^{-2}\dot\Psi^2|0,1\rangle=+\rho_{\rm beat}G_{\rm int}(x)\cos(\Omega_{\rm beat}t)$.
- In $T^{01}_{\rm sc}=-\frac{\kappa}{2c}\{\dot\Psi,\partial_1\Psi\}$, only the $(j_{\rm time},j_{\rm grad})=(2,1)$ product $-\kappa B_1B_2|k_2|(\partial_1u_1)u_2\,X_1(t)Y_2(t)$ connects $|1,0\rangle$ to $|0,1\rangle$; combining $-\kappa B_1B_2|k_2|=-\frac{2\rho_{\rm beat}}{|k_1|}$, $(\partial_1u_1)u_2=\partial_1G_{\rm int}$, and $\operatorname{Re}\langle 1,0|X_1Y_2|0,1\rangle=-\frac12\sin(\Omega_{\rm beat}t)$ gives $T^{01}_{\rm beat}=+\frac{\rho_{\rm beat}}{|k_1|}(\partial_1G_{\rm int})\sin(\Omega_{\rm beat}t)$.
- In $T^{02}_{\rm sc}=-\frac{\kappa}{2c}\{\dot\Psi,\partial_2\Psi\}$, only the $(1,2)$ product $-\kappa B_1B_2|k_1|u_1(\partial_2u_2)\,Y_1(t)X_2(t)$ contributes; combining $-\kappa B_1B_2|k_1|=-\frac{2\rho_{\rm beat}}{|k_2|}$, $u_1(\partial_2u_2)=\partial_2G_{\rm int}$, and $\operatorname{Re}\langle 1,0|Y_1X_2|0,1\rangle=+\frac12\sin(\Omega_{\rm beat}t)$ gives $T^{02}_{\rm beat}=-\frac{\rho_{\rm beat}}{|k_2|}(\partial_2G_{\rm int})\sin(\Omega_{\rm beat}t)$, while $T^{03}_{\rm beat}=0$.
- In $T^{12}_{\rm sc}=\frac{\kappa}{2}\{\partial_1\Psi,\partial_2\Psi\}$, the product $\kappa B_1B_2(\partial_1u_1)(\partial_2u_2)X_1(t)X_2(t)$ gives $T^{12}_{\rm beat}=+\frac{\rho_{\rm beat}}{|k_1||k_2|}(\partial_1\partial_2G_{\rm int})\cos(\Omega_{\rm beat}t)$, while $T^{13}_{\rm beat}=T^{23}_{\rm beat}=0$.

Collecting all ten independent components gives on $\mathbb R\times\overline\Omega$ (and as smooth trigonometric formulas on $\mathbb R^{1,3}$):
$$
 T^{00}_{\rm beat}(t,x)=T^{11}_{\rm beat}(t,x)=T^{22}_{\rm beat}(t,x)=T^{33}_{\rm beat}(t,x)
  =\rho_{\rm beat}G_{\rm int}(x)\cos(\Omega_{\rm beat}t)
  =-\rho_{\rm beat}\sin\!\left(\frac{5\pi}{L}x_1\right)\sin\!\left(\frac{7\pi}{L}x_2\right)\cos(\Omega_{\rm beat}t),
$$
$$
 T^{01}_{\rm beat}(t,x)=+\frac{\rho_{\rm beat}}{|k_1|}\bigl(\partial_1G_{\rm int}(x)\bigr)\sin(\Omega_{\rm beat}t)
  =-\rho_{\rm beat}\cos\!\left(\frac{5\pi}{L}x_1\right)\sin\!\left(\frac{7\pi}{L}x_2\right)\sin(\Omega_{\rm beat}t),
$$
$$
 T^{02}_{\rm beat}(t,x)=-\frac{\rho_{\rm beat}}{|k_2|}\bigl(\partial_2G_{\rm int}(x)\bigr)\sin(\Omega_{\rm beat}t)
  =+\rho_{\rm beat}\sin\!\left(\frac{5\pi}{L}x_1\right)\cos\!\left(\frac{7\pi}{L}x_2\right)\sin(\Omega_{\rm beat}t),
$$
$$
 T^{12}_{\rm beat}(t,x)=+\frac{\rho_{\rm beat}}{|k_1||k_2|}\bigl(\partial_1\partial_2G_{\rm int}(x)\bigr)\cos(\Omega_{\rm beat}t)
  =-\rho_{\rm beat}\cos\!\left(\frac{5\pi}{L}x_1\right)\cos\!\left(\frac{7\pi}{L}x_2\right)\cos(\Omega_{\rm beat}t),
$$
$$
 T^{03}_{\rm beat}(t,x)=T^{13}_{\rm beat}(t,x)=T^{23}_{\rm beat}(t,x)=0. \tag{5}
$$

Using $\partial_0=c^{-1}\partial_t$, $\partial_1^2G_{\rm int}=-|k_1|^2G_{\rm int}$, $\partial_2^2G_{\rm int}=-|k_2|^2G_{\rm int}$, $\partial_3G_{\rm int}=0$, and $|k_2|-|k_1|=k_{\rm beat}$, direct differentiation of (5) checks every component of local spacetime conservation:
- $\nu=0$: $\partial_0T^{00}_{\rm beat}+\partial_aT^{a0}_{\rm beat}=[-k_{\rm beat}+(-|k_1|+|k_2|)]\rho_{\rm beat}G_{\rm int}\sin(\Omega_{\rm beat}t)=0$;
- $\nu=1$: $\partial_0T^{01}_{\rm beat}+\partial_aT^{a1}_{\rm beat}=[\frac{k_{\rm beat}}{|k_1|}+(1-\frac{|k_2|}{|k_1|})]\rho_{\rm beat}(\partial_1G_{\rm int})\cos(\Omega_{\rm beat}t)=0$;
- $\nu=2$: $\partial_0T^{02}_{\rm beat}+\partial_aT^{a2}_{\rm beat}=[-\frac{k_{\rm beat}}{|k_2|}+(-\frac{|k_1|}{|k_2|}+1)]\rho_{\rm beat}(\partial_2G_{\rm int})\cos(\Omega_{\rm beat}t)=0$;
- $\nu=3$: $\partial_0T^{03}_{\rm beat}+\partial_aT^{a3}_{\rm beat}=\rho_{\rm beat}(\partial_3G_{\rm int})\cos(\Omega_{\rm beat}t)=0$.

Because $\int_{-L/2}^{L/2}\sin(\frac{5\pi}{L}x_1)\,dx_1=\int_{-L/2}^{L/2}\sin(\frac{7\pi}{L}x_2)\,dx_2=0$, the spatial integrals of $T^{00}_{\rm beat}$, $T^{01}_{\rm beat}$ (odd in $x_2$), and $T^{02}_{\rm beat}$ (odd in $x_1$) over $\Omega$ vanish at every $t\in\mathbb R$, while on $\partial\Omega$, $\cos(\frac{5\pi}{L}(\pm\frac L2))=\cos(\pm\frac{5\pi}{2})=0$ kills $T^{10}_{\rm beat}|_{x_1=\pm L/2}$, $\cos(\frac{7\pi}{L}(\pm\frac L2))=\cos(\pm\frac{7\pi}{2})=0$ kills $T^{20}_{\rm beat}|_{x_2=\pm L/2}$, and $T^{30}_{\rm beat}=0$. Combined with $\partial_\mu T^{\mu\nu}_{\rm cav,vac}=0$, this establishes for all $t\in\mathbb R$:
$$
 \partial_0T^{0\nu}_{{\rm cav},\pm}+\partial_aT^{a\nu}_{{\rm cav},\pm}=0\quad\text{in }\operatorname{int}(\Omega),\qquad
 \int_\Omega T^{00}_{{\rm cav},\pm}(t,x)\,d^3x=2E_0=\frac{3\pi A_*}{\tau},
$$
$$
 \int_\Omega T^{0a}_{{\rm cav},\pm}(t,x)\,d^3x=0\quad(a=1,2,3),\qquad
 n_aT^{a0}_{{\rm cav},\pm}(t,x)=0\quad\text{on }\partial\Omega. \tag{6}
$$

Next prove that $T^{\mu\nu}_{{\rm cav},\pm}(t,x)$ on $\mathbb R\times\overline\Omega$—and more generally the Weyl-ordered expectation $T^{\mu\nu}_{{\rm ext},\pm}(t,x):=2T^{\mu\nu}_{\rm ext,vac}(x)\pm T^{\mu\nu}_{\rm beat}(t,x)$ of the smooth trigonometric continuation $\Psi_{\rm ext}(t,x):=\sum_{j=1}^2B_j\cos\alpha_j(x_j)X_j(t)$ on all $\mathbb R^{1,3}$, where $T^{\mu\nu}_{\rm ext,vac}(x)$ denotes the ground-state ($\psi=\psi_0$) Weyl-ordered stress expectation of $\Psi_{\rm ext}$ on $\mathbb R^3$ ($T^{00}_{\rm ext,vac}=\rho_0$, $T^{0a}_{\rm ext,vac}=0$, $T^{ab}_{\rm ext,vac}=\sum_{j=1}^2\rho_j[d_j^ad_j^b+(\delta^{ab}-d_j^ad_j^b)\cos 2\alpha_j(x_j)]$ for all $x\in\mathbb R^3$, agreeing with $T^{\mu\nu}_{\rm cav,vac}(x)$ on $\overline\Omega$)—satisfies the full Lorentzian dominant energy condition with zero energy offset. Fix any normalized state $\psi\in{\cal S}(\mathbb R^2)$ (in particular $\psi=\psi_0$, $\psi=\psi_+$, or $\psi=\psi_-$) and any $(t,x)\in\mathbb R^{1,3}$, and define the real symmetric $4\times 4$ derivative-covariance matrix
$$
 C_{\mu\nu}(t,x):=\left\langle\psi,\,\frac12\{\partial_\mu\Psi_{\rm ext}(t,x),\partial_\nu\Psi_{\rm ext}(t,x)\}\psi\right\rangle,\qquad
 T^{\rm ext}_{\mu\nu}(t,x)=\kappa\left[C_{\mu\nu}(t,x)-\frac12\eta_{\mu\nu}\eta^{\alpha\beta}C_{\alpha\beta}(t,x)\right].
$$
For every $\xi=(\xi^0,\xi^1,\xi^2,\xi^3)\in\mathbb R^4$, the operator $D_\xi:=\xi^\mu\partial_\mu\Psi_{\rm ext}(t,x)$ is a real linear combination of $Q_1,P_1,Q_2,P_2$, hence symmetric on ${\cal S}(\mathbb R^2)$, giving $\xi^\mu\xi^\nu C_{\mu\nu}(t,x)=\|D_\xi\psi\|_{L^2(\mathbb R^2)}^2\ge 0$; thus $C(t,x)\succeq 0$. Take any two future-directed null vectors $\ell_1=(1,\hat e_1)$ and $\ell_2=(1,\hat e_2)$ with $|\hat e_1|=|\hat e_2|=1$, let $\theta\in[0,\pi]$ satisfy $\hat e_1\cdot\hat e_2=\cos\theta$, and choose an orthonormal spatial triad $(f_1,f_2,f_3)$ such that $\hat e_1=\cos\frac{\theta}{2}\,f_1+\sin\frac{\theta}{2}\,f_2$ and $\hat e_2=\cos\frac{\theta}{2}\,f_1-\sin\frac{\theta}{2}\,f_2$. In the Lorentz-orthonormal basis $(e_0,f_1,f_2,f_3)$, let $\widetilde C_{\alpha\beta}$ be the congruent positive-semidefinite components of $C_{\mu\nu}$, whose $3\times 3$ principal submatrix on $\{0,1,3\}$ is the real part of the $L^2(\mathbb R^2)$ Gram matrix of $\partial_0\Psi_{\rm ext}\psi$, $(f_1\cdot\nabla\Psi_{\rm ext})\psi$, and $(f_3\cdot\nabla\Psi_{\rm ext})\psi$ (i.e., their Gram matrix under $\operatorname{Re}\langle\cdot,\cdot\rangle_{L^2(\mathbb R^2)}$). Because $\eta_{\mu\nu}\ell_1^\mu\ell_2^\nu=-1+\cos\theta=-2\sin^2\frac{\theta}{2}$ and the $(0,2)$ and $(1,2)$ cross terms of $\ell_1^\mu\ell_2^\nu$ cancel by opposite signs of $\pm\sin\frac{\theta}{2}$, direct expansion gives
$$
 \frac{1}{\kappa}T^{\rm ext}_{\mu\nu}(t,x)\ell_1^\mu\ell_2^\nu
  =\bigl(\widetilde C_{00}+2\cos\tfrac{\theta}{2}\,\widetilde C_{01}+\cos^2\tfrac{\theta}{2}\,\widetilde C_{11}-\sin^2\tfrac{\theta}{2}\,\widetilde C_{22}\bigr)
   +\sin^2\tfrac{\theta}{2}\bigl(-\widetilde C_{00}+\widetilde C_{11}+\widetilde C_{22}+\widetilde C_{33}\bigr)
$$
$$
  =\bigl(\cos^2\tfrac{\theta}{2}\,\widetilde C_{00}+2\cos\tfrac{\theta}{2}\,\widetilde C_{01}+\widetilde C_{11}\bigr)+\sin^2\tfrac{\theta}{2}\,\widetilde C_{33}
  =\bigl\|\bigl(\cos\tfrac{\theta}{2}\,\partial_0\Psi_{\rm ext}+f_1\cdot\nabla\Psi_{\rm ext}\bigr)\psi\bigr\|^2
   +\sin^2\tfrac{\theta}{2}\,\bigl\|(f_3\cdot\nabla\Psi_{\rm ext})\psi\bigr\|^2\ge 0. \tag{7}
$$
Every future-directed causal vector $u^\mu=(u^0,\vec u)$ ($u^0\ge|\vec u|\ge 0$) is a nonnegative combination of two future-directed null vectors, $u=\frac{u^0+|\vec u|}{2}(1,\hat e)+\frac{u^0-|\vec u|}{2}(1,-\hat e)$ ($\hat e=\vec u/|\vec u|$ for $\vec u\ne 0$, $\hat e=e_1$ for $\vec u=0$). Bilinearity and (7) therefore give $T^{\rm ext}_{\mu\nu}(t,x)u^\mu w^\nu\ge 0$ for all future-directed causal $u^\mu,w^\mu$ at every $(t,x)\in\mathbb R^{1,3}$ (and by convexity for $\rho_{\rm inc}$ as well). Equivalently, for every future-directed causal $w^\nu$, the energy-momentum flux $J^\mu:=-T_{\rm ext}{}^\mu{}_\nu w^\nu$ obeys $-\eta_{\mu\nu}u^\mu J^\nu=T^{\rm ext}_{\mu\nu}u^\mu w^\nu\ge 0$ for all future-directed causal $u^\mu$, so $J^0\ge|\vec J|\ge 0$. Restricting to $\mathbb R\times\overline\Omega$ establishes exact interior dominant-energy positivity of $T^{\mu\nu}_{{\rm cav},\pm}(t,x)$ with zero offset.

Despite vanishing normal energy flux $n_aT^{a0}_{{\rm cav},\pm}=0$ on $\partial\Omega$, extending $T^{\mu\nu}_{{\rm cav},\pm}$ by zero outside $\Omega$ fails conservation on $\mathbb R^{1,3}$, and no spatial-only Beltrami collar can cure the dynamical beat stress. First, on $\partial\Omega$, the normal beat pressures do not vanish: on $x_1=\pm L/2$ ($n=\pm e_1$), $T^{11}_{\rm beat}=\mp\rho_{\rm beat}\sin(\frac{7\pi}{L}x_2)\cos(\Omega_{\rm beat}t)$; on $x_2=\pm L/2$ ($n=\pm e_2$), $T^{22}_{\rm beat}=\pm\rho_{\rm beat}\sin(\frac{5\pi}{L}x_1)\cos(\Omega_{\rm beat}t)$; and on $x_3=\pm L/2$ ($n=\pm e_3$), $T^{33}_{\rm beat}=-\rho_{\rm beat}\sin(\frac{5\pi}{L}x_1)\sin(\frac{7\pi}{L}x_2)\cos(\Omega_{\rm beat}t)$. For any smooth spacetime test field $f_b\in C_c^\infty(\mathbb R^{1,3};\mathbb R^3)$, integrating $\mathbf 1_\Omega T^{\mu b}_{\rm beat}$ against $\partial_\mu f_b$ using $\partial_\mu T^{\mu b}_{\rm beat}=0$ in $\operatorname{int}(\Omega)$ yields the nonzero surface layer $\partial_\mu(\mathbf 1_\Omega T^{\mu b}_{\rm beat})=-n_aT^{ab}_{\rm beat}\,\delta_{\partial\Omega}\ne 0$. Second, for any smooth spatial Beltrami potential $\Phi_{mn}(t,x)$, antisymmetry of $\epsilon_{akm}$ against symmetric $\partial_a\partial_k$ forces $\partial_a(\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn})\equiv 0$ everywhere, whereas inside $\Omega$ (5) has nonzero spatial divergence whenever $\cos(\Omega_{\rm beat}t)\ne 0$:
$$
 \partial_\mu\bigl(\mathbf 1_\Omega T^{\mu b}_{\rm beat}\bigr)=-n_aT^{ab}_{\rm beat}\,\delta_{\partial\Omega}\ne 0,\qquad
 \partial_aT^{a1}_{\rm beat}(t,x)=-\partial_0T^{01}_{\rm beat}(t,x)
  =k_{\rm beat}\rho_{\rm beat}\cos\!\left(\frac{5\pi}{L}x_1\right)\sin\!\left(\frac{7\pi}{L}x_2\right)\cos(\Omega_{\rm beat}t)\not\equiv 0,
$$
$$
 \partial_aT^{a2}_{\rm beat}(t,x)=-\partial_0T^{02}_{\rm beat}(t,x)
  =-k_{\rm beat}\rho_{\rm beat}\sin\!\left(\frac{5\pi}{L}x_1\right)\cos\!\left(\frac{7\pi}{L}x_2\right)\cos(\Omega_{\rm beat}t)\not\equiv 0. \tag{8}
$$
Hence no purely spatial Beltrami tensor $\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}$ can equal $T^{ab}_{\rm beat}$ on $\Omega$ or complete it across $\partial\Omega$.

## 2. Four-dimensional Lorentzian superpotential, staggered collar and whole-space DEC

For any smooth symmetric spatial tensor fields $\Sigma^{ab}(t,x)=\Sigma^{ba}(t,x)$ and $\Phi_{mn}(t,x)=\Phi_{nm}(t,x)$ on $\mathbb R^{1,3}$ (with $\partial_0=c^{-1}\partial_t$ and $\epsilon_{123}=+1$), define the symmetric spacetime tensor $T^{\mu\nu}(\Sigma,\Phi)$ by
$$
 T^{00}(\Sigma,\Phi):=\partial_k\partial_l\Sigma^{kl},\qquad
 T^{0b}(\Sigma,\Phi)=T^{b0}(\Sigma,\Phi):=-\partial_0\partial_k\Sigma^{kb},\qquad
 T^{ab}(\Sigma,\Phi):=\partial_0^2\Sigma^{ab}+\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}. \tag{9}
$$
Equation (9) is the $3+1$ form of $T^{\mu\nu}=\partial_\alpha\partial_\beta H^{\mu\alpha\nu\beta}$ for the Riemann-symmetric four-tensor with $H^{0k0l}=\Sigma^{kl}$, $H^{akbl}=\epsilon_{akm}\epsilon_{bln}\Phi_{mn}$, and $H^{0kbl}=0$. Commuting smooth partial derivatives verifies exact four-divergence vanishing on all $\mathbb R^{1,3}$:
- For $\nu=0$: $\partial_0T^{00}(\Sigma,\Phi)+\partial_bT^{b0}(\Sigma,\Phi)=\partial_0\partial_k\partial_l\Sigma^{kl}-\partial_0\partial_k\partial_b\Sigma^{kb}=0$;
- For $\nu=b$: $\partial_0T^{0b}(\Sigma,\Phi)+\partial_aT^{ab}(\Sigma,\Phi)=-\partial_0^2\partial_k\Sigma^{kb}+\partial_0^2\partial_a\Sigma^{ab}+\epsilon_{akm}\epsilon_{bln}(\partial_a\partial_k)\partial_l\Phi_{mn}=0$.

Using $|k_1|=\frac{5}{2}k_{\rm beat}$ and $|k_2|=\frac{7}{2}k_{\rm beat}$, introduce the constant dimensionless rational diagonal matrices $S_\Sigma$ and $S_\Phi$ and smooth interior superpotentials on $\mathbb R^{1,3}$:
$$
 S_\Sigma:=\operatorname{diag}\!\left(\frac25,\,-\frac27,\,0\right),\qquad
 S_\Phi:=-\operatorname{diag}\!\left(\frac{2}{49},\,\frac{2}{25},\,\frac{4}{35}\right),
$$
$$
 \Sigma^{\rm beat,int}(t,x):=G_{\rm int}(x)\cos(\Omega_{\rm beat}t)
  \operatorname{diag}\!\left(\frac{\rho_{\rm beat}}{k_{\rm beat}|k_1|},\,-\frac{\rho_{\rm beat}}{k_{\rm beat}|k_2|},\,0\right)
  =\frac{\rho_{\rm beat}}{k_{\rm beat}^2}\,G_{\rm int}(x)\cos(\Omega_{\rm beat}t)\,S_\Sigma,
$$
$$
 \Phi^{\rm beat,int}(t,x):=-G_{\rm int}(x)\cos(\Omega_{\rm beat}t)
  \operatorname{diag}\!\left(\frac{\rho_{\rm beat}}{2|k_2|^2},\,\frac{\rho_{\rm beat}}{2|k_1|^2},\,\frac{\rho_{\rm beat}}{|k_1||k_2|}\right)
  =\frac{\rho_{\rm beat}}{k_{\rm beat}^2}\,G_{\rm int}(x)\cos(\Omega_{\rm beat}t)\,S_\Phi. \tag{10}
$$
Check every component of $T^{\mu\nu}(\Sigma^{\rm beat,int},\Phi^{\rm beat,int})$ against (5) on $\mathbb R^{1,3}$:
- $T^{00}=\bigl(\frac{\rho_{\rm beat}}{k_{\rm beat}|k_1|}(-|k_1|^2)-\frac{\rho_{\rm beat}}{k_{\rm beat}|k_2|}(-|k_2|^2)\bigr)G_{\rm int}\cos(\Omega_{\rm beat}t)=\frac{|k_2|-|k_1|}{k_{\rm beat}}\rho_{\rm beat}G_{\rm int}\cos(\Omega_{\rm beat}t)=\rho_{\rm beat}G_{\rm int}\cos(\Omega_{\rm beat}t)=T^{00}_{\rm beat}$;
- $T^{01}=-\frac{\rho_{\rm beat}}{k_{\rm beat}|k_1|}(\partial_1G_{\rm int})(-k_{\rm beat}\sin\Omega_{\rm beat}t)=+\frac{\rho_{\rm beat}}{|k_1|}(\partial_1G_{\rm int})\sin(\Omega_{\rm beat}t)=T^{01}_{\rm beat}$, $T^{02}=+\frac{\rho_{\rm beat}}{k_{\rm beat}|k_2|}(\partial_2G_{\rm int})(-k_{\rm beat}\sin\Omega_{\rm beat}t)=-\frac{\rho_{\rm beat}}{|k_2|}(\partial_2G_{\rm int})\sin(\Omega_{\rm beat}t)=T^{02}_{\rm beat}$, and $T^{03}=0$;
- Using $\epsilon_{1km}\epsilon_{1ln}\partial_k\partial_l\Phi_{mn}=\partial_3^2\Phi_2+\partial_2^2\Phi_3$, $\epsilon_{2km}\epsilon_{2ln}\partial_k\partial_l\Phi_{mn}=\partial_3^2\Phi_1+\partial_1^2\Phi_3$, $\epsilon_{3km}\epsilon_{3ln}\partial_k\partial_l\Phi_{mn}=\partial_2^2\Phi_1+\partial_1^2\Phi_2$, and $\epsilon_{1km}\epsilon_{2ln}\partial_k\partial_l\Phi_{mn}=-\partial_1\partial_2\Phi_3$ for diagonal $\Phi=\operatorname{diag}(\Phi_1,\Phi_2,\Phi_3)$ together with $\partial_3G_{\rm int}=0$:
  $T^{11}=\rho_{\rm beat}\bigl(-\frac{k_{\rm beat}}{|k_1|}+\frac{|k_2|}{|k_1|}\bigr)G_{\rm int}\cos(\Omega_{\rm beat}t)=\rho_{\rm beat}G_{\rm int}\cos(\Omega_{\rm beat}t)$,
  $T^{22}=\rho_{\rm beat}\bigl(+\frac{k_{\rm beat}}{|k_2|}+\frac{|k_1|}{|k_2|}\bigr)G_{\rm int}\cos(\Omega_{\rm beat}t)=\rho_{\rm beat}G_{\rm int}\cos(\Omega_{\rm beat}t)$,
  $T^{33}=\rho_{\rm beat}\bigl(\frac12+\frac12\bigr)G_{\rm int}\cos(\Omega_{\rm beat}t)=\rho_{\rm beat}G_{\rm int}\cos(\Omega_{\rm beat}t)$,
  $T^{12}=+\frac{\rho_{\rm beat}}{|k_1||k_2|}(\partial_1\partial_2G_{\rm int})\cos(\Omega_{\rm beat}t)=T^{12}_{\rm beat}$, and $T^{13}=T^{23}=0$.

Thus $T^{\mu\nu}(\Sigma^{\rm beat,int},\Phi^{\rm beat,int})\equiv T^{\mu\nu}_{\rm beat}$ identically on all $\mathbb R^{1,3}$.

Write $B_R(0):=\{x\in\mathbb R^3:|x|<R\}$ for the open Euclidean ball of radius $R>0$. Fix the dimensionless collar-shell width $\delta_1:=\frac{1}{600}$ ($2\delta_1=\frac{1}{300}$), set $s_0:=\frac12$, $s_1:=\frac12+\delta_1=\frac{301}{600}$, $s_2:=\frac12+2\delta_1=\frac{151}{300}$, and define the open nested cubes $\Omega_1:=(-s_1L,s_1L)^3$ and $\Omega_2:=(-s_2L,s_2L)^3$. Because $3s_2^2=3\cdot\frac{22801}{90000}=\frac{22801}{30000}<1$, every $x\in\overline{\Omega_2}$ satisfies $|x|\le\sqrt3\,s_2L<L$, giving the strict inclusion chain
$$
 \overline\Omega\subset\Omega_1\subset\overline{\Omega_1}\subset\Omega_2\subset\overline{\Omega_2}
  \subset B_L(0)\subset B_{3L/2}(0)\subset B_{2L}(0)\subset B_{3L}(0).
$$
With $b(z):=e^{-1/z}\mathbf 1_{z>0}\in C^\infty(\mathbb R)$, define the smooth transition $S(w):=\frac{b(1-w)}{b(1-w)+b(w)}$ ($w\in\mathbb R$), whose denominator satisfies $D_S(w)=b(1-w)+b(w)\ge b(\max(1-w,w))\ge b(1/2)=e^{-2}>0$ on $\mathbb R$, with $S(w)=1$ for $w\le 0$ and $S(w)=0$ for $w\ge 1$. Define the manifestly even smooth compactly supported one-dimensional profiles $\vartheta_0,\vartheta\in C_c^\infty(\mathbb R;[0,1])$ and three-dimensional product cutoffs $\chi_{\rm in},\chi_{\rm box}\in C_c^\infty(\mathbb R^3;[0,1])$ by
$$
 \vartheta_0(u):=S\!\left(\frac{u^2-s_0^2}{s_1^2-s_0^2}\right),\qquad
 \vartheta(u):=S\!\left(\frac{u^2-s_1^2}{s_2^2-s_1^2}\right)\qquad(u\in\mathbb R),
$$
$$
 \chi_{\rm in}(x):=\vartheta_0\!\left(\frac{x_1}{L}\right)\vartheta_0\!\left(\frac{x_2}{L}\right)\vartheta_0\!\left(\frac{x_3}{L}\right),\qquad
 \chi_{\rm box}(x):=\vartheta\!\left(\frac{x_1}{L}\right)\vartheta\!\left(\frac{x_2}{L}\right)\vartheta\!\left(\frac{x_3}{L}\right). \tag{11}
$$
Because $u\mapsto u^2$ is a smooth even polynomial on $\mathbb R$, $\vartheta_0$ and $\vartheta$ belong to $C_c^\infty(\mathbb R)$ everywhere including $u=0$, with $\vartheta_0(u)=1$ for $|u|\le s_0$ and $0$ for $|u|\ge s_1$, and $\vartheta(u)=1$ for $|u|\le s_1$ and $0$ for $|u|\ge s_2$. Consequently $\chi_{\rm in}(x)=1$ on $\overline\Omega$ and $\chi_{\rm in}(x)=0$ on $\mathbb R^3\setminus\Omega_1$, while $\chi_{\rm box}(x)=1$ on $\overline{\Omega_1}$ and $\chi_{\rm box}(x)=0$ on $\mathbb R^3\setminus\Omega_2$.

Retain from Eq. (13)–(17) of the [compact cavity source](compact_cavity_source_for_four_chain_field.md) the radial cutoff $\chi_{\rm out}(|x|/L)=\frac{b(9-|x|^2/L^2)}{b(9-|x|^2/L^2)+b(|x|^2/L^2-4)}\in C_c^\infty(\mathbb R^3;[0,1])$ (equal to $1$ on $|x|\le 2L$ and $0$ on $|x|\ge 3L$) and the complete static ground-state cavity-plus-collar source tensor $T^{\mu\nu}_{\rm tot,vac}\in C_c^\infty(\mathbb R^3)$ (which satisfies $\partial_\mu T^{\mu\nu}_{\rm tot,vac}=0$, $T^{0a}_{\rm tot,vac}=0$, $\|T^{ab}_{\rm tot,vac}(x)\|\le T^{00}_{\rm tot,vac}(x)$ everywhere on $\mathbb R^3$, $\operatorname{supp}T^{\mu\nu}_{\rm tot,vac}\subseteq\overline{B_{3L}(0)}$, and $T^{\mu\nu}_{\rm tot,vac}(x)=T^{\mu\nu}_{\rm ext,vac}(x)$ for all $|x|\le L$, hence $T^{\mu\nu}_{\rm tot,vac}(x)=T^{\mu\nu}_{\rm cav,vac}(x)$ on $\overline\Omega$). For a constant plateau $U_{\rm col}^{\rm dyn}>0$ fixed explicitly in (14) below, define on $\mathbb R^{1,3}$:
$$
 G(x):=\chi_{\rm box}(x)G_{\rm int}(x),\qquad
 \Sigma^{\rm beat}(t,x):=\chi_{\rm box}(x)\Sigma^{\rm beat,int}(t,x)
  =\frac{\rho_{\rm beat}}{k_{\rm beat}^2}\,G(x)\cos(\Omega_{\rm beat}t)\,S_\Sigma,
$$
$$
 \Phi^{\rm beat}(t,x):=\chi_{\rm box}(x)\Phi^{\rm beat,int}(t,x)
  =\frac{\rho_{\rm beat}}{k_{\rm beat}^2}\,G(x)\cos(\Omega_{\rm beat}t)\,S_\Phi,\qquad
 T^{\mu\nu}_{\rm beat,tot}(t,x):=T^{\mu\nu}(\Sigma^{\rm beat},\Phi^{\rm beat})(t,x),
$$
$$
 T^{\mu\nu}_{\rm tot,inc}(x):=2T^{\mu\nu}_{\rm tot,vac}(x)
  +U_{\rm col}^{\rm dyn}\bigl(1-\chi_{\rm in}(x)\bigr)\chi_{\rm out}\!\left(\frac{|x|}{L}\right)\delta^\mu_0\delta^\nu_0,\qquad
 T^{\mu\nu}_{{\rm tot},\pm}(t,x):=T^{\mu\nu}_{\rm tot,inc}(x)\pm T^{\mu\nu}_{\rm beat,tot}(t,x). \tag{12}
$$
Every component of $T^{\mu\nu}_{\rm tot,inc}$ and $T^{\mu\nu}_{{\rm tot},\pm}$ belongs to $C^\infty(\mathbb R;C_c^\infty(\mathbb R^3))$ with $\operatorname{supp}T^{\mu\nu}_{\rm beat,tot}(t,\cdot)\subseteq\overline{\Omega_2}\subset B_L(0)$ and $\operatorname{supp}T^{\mu\nu}_{{\rm tot},\pm}(t,\cdot)\subseteq\overline{B_{3L}(0)}$. On $\overline\Omega$, $\chi_{\rm in}=\chi_{\rm box}=\chi_{\rm out}=1$ and $|x|<L$, so $T^{\mu\nu}_{\rm tot,inc}(x)=2T^{\mu\nu}_{\rm cav,vac}(x)=\operatorname{Tr}(\rho_{\rm inc}T^{\mu\nu}_{\rm sc}(t,x))$ and $T^{\mu\nu}_{{\rm tot},\pm}(t,x)=T^{\mu\nu}_{{\rm cav},\pm}(t,x)$ pointwise on $\mathbb R\times\overline\Omega$. Because $T^{\mu\nu}_{\rm tot,inc}$ is static with $\partial_aT^{a\nu}_{\rm tot,inc}=2\partial_aT^{a\nu}_{\rm tot,vac}=0$ and $T^{\mu\nu}_{\rm beat,tot}$ has the superpotential form (9), $\partial_\mu T^{\mu\nu}_{{\rm tot},\pm}=0$ and $\partial_\mu T^{\mu\nu}_{\rm tot,inc}=0$ hold classically and distributionally on all $\mathbb R^{1,3}$ without surface layers.

To bound $T^{\mu\nu}_{\rm beat,tot}$ across $\overline{\Omega_2}\setminus\Omega_1$ in elementary closed form, use $z^{-k}e^{-1/z}\le k^ke^{-k}$ ($z>0$, $k\ge 1$) and $e=\sum_{n=0}^\infty\frac{1}{n!}>1+1+\frac12=\frac52$ ($e^{-1}<\frac25$, $e^{-2}<\frac{4}{25}$). For $S(w)=\frac{b_1(w)}{D_S(w)}$ with $b_1(w)=b(1-w)$, $b_2(w)=b(w)$, and $D_S(w)=b_1(w)+b_2(w)\ge e^{-2}$, we have $-4e^{-2}\le b_1'(w)\le 0\le b_2'(w)\le 4e^{-2}$, $|b_1'(w)+b_2'(w)|\le 4e^{-2}$, and $|b_j''(w)|\le 256e^{-4}+54e^{-3}$. By $S'(w)=\frac{b_2b_1'-b_1b_2'}{D_S^2}$ and $S''(w)=\frac{b_2b_1''-b_1b_2''}{D_S^2}-2S'(w)\frac{b_1'+b_2'}{D_S}$ with $\frac{b_1+b_2}{D_S}=1$,
$$
 |S'(w)|\le\frac{4e^{-2}}{e^{-2}}=4,\qquad
 |S''(w)|\le\frac{256e^{-4}+54e^{-3}}{e^{-2}}+2\cdot 4\cdot\frac{4e^{-2}}{e^{-2}}
  =256e^{-2}+54e^{-1}+32<\frac{1564}{25}+32<95.
$$
With $\Delta_2:=s_2^2-s_1^2=(s_2-s_1)(s_2+s_1)=\frac{1}{600}\cdot\frac{603}{600}=\frac{67}{40000}$, on $|u|\le s_2=\frac{302}{600}$ (outside which $\vartheta'= \vartheta''=0$) we have $\frac{2|u|}{\Delta_2}\le\frac{2s_2}{\Delta_2}=\frac{120800}{201}<601$ and $\frac{2}{\Delta_2}=\frac{80000}{67}<1195$. Thus $|\vartheta'(u)|\le\frac{2|u|}{\Delta_2}|S'|<601\cdot 4=2404<2500=:M_1$ and $|\vartheta''(u)|\le(\frac{2|u|}{\Delta_2})^2|S''|+\frac{2}{\Delta_2}|S'|<601^2\cdot 95+1195\cdot 4=34{,}318{,}875<3.5\times 10^7=:M_2$. For $\chi_{\rm box}(x)=\prod_{m=1}^3\vartheta(x_m/L)$, $|\partial_k\chi_{\rm box}|\le M_1/L$ gives $|\nabla\chi_{\rm box}|\le\frac{\sqrt3\,M_1}{L}<\frac{5000}{L}$, while $|\partial_k^2\chi_{\rm box}|\le M_2/L^2$ and $|\partial_k\partial_l\chi_{\rm box}|\le M_1^2/L^2$ ($k\ne l$). Since any symmetric $3\times 3$ matrix $H$ satisfies $|v^{\mathsf T}Hv|\le\sum_{k,l}|H_{kl}|\frac{v_k^2+v_l^2}{2}\le|v|^2\max_k\sum_l|H_{kl}|$,
$$
 |\nabla\chi_{\rm box}(x)|<\frac{5000}{L},\qquad
 \|\operatorname{Hess}\chi_{\rm box}(x)\|\le\frac{M_2+2M_1^2}{L^2}=\frac{4.75\times 10^7}{L^2},\qquad
 \|\operatorname{Hess}G(x)\|<\frac{4.8\times 10^7}{L^2}. \tag{13}
$$
To check the last inequality in (13), use $3<\pi<4$ ($\frac{\pi}{6}=\int_0^{1/2}(1-x^2)^{-1/2}dx>\frac12$ and inscribed/circumscribed unit-circle polygons): $|G_{\rm int}|\le 1$, $|\partial_1G_{\rm int}|\le\frac{5\pi}{L}<\frac{20}{L}$, $|\partial_2G_{\rm int}|\le\frac{7\pi}{L}<\frac{28}{L}$, $|\nabla G_{\rm int}|\le\frac{\sqrt{74}\,\pi}{L}<\frac{9\pi}{L}<\frac{36}{L}$, and $\|\operatorname{Hess}G_{\rm int}\|\le\frac{(35+49)\pi^2}{L^2}=\frac{84\pi^2}{L^2}<\frac{1344}{L^2}$, so $\|\operatorname{Hess}(\chi_{\rm box}G_{\rm int})\|\le\|\operatorname{Hess}\chi_{\rm box}\|+2|\nabla\chi_{\rm box}||\nabla G_{\rm int}|+\|\operatorname{Hess}G_{\rm int}\|<\frac{(4.75\times 10^7+3.6\times 10^5+1344)}{L^2}<\frac{4.8\times 10^7}{L^2}$, while $|\partial_1G|<\frac{2520}{L}$ and $|\partial_2G|<\frac{2528}{L}$.

Using $k_{\rm beat}=\frac{2\pi}{L}>\frac{6}{L}$ and $k_{\rm beat}^2=\frac{4\pi^2}{L^2}>\frac{36}{L^2}$, bound each piece of $T^{\mu\nu}_{\rm beat,tot}$ from (9)–(10) and (12)–(13):
- $|T^{00}_{\rm beat,tot}(t,x)|\le\frac{\rho_{\rm beat}}{k_{\rm beat}^2}\bigl(\frac25|\partial_1^2G|+\frac27|\partial_2^2G|\bigr)<\frac{\rho_{\rm beat}}{36}\cdot\frac{24}{35}\cdot 4.8\times 10^7<9.2\times 10^5\,\rho_{\rm beat}$;
- $2|\vec T^{0\bullet}_{\rm beat,tot}(t,x)|\le\frac{2\rho_{\rm beat}}{k_{\rm beat}}\bigl(\frac25|\partial_1G|+\frac27|\partial_2G|\bigr)<\frac{\rho_{\rm beat}}{3}\bigl(1008+\frac{5056}{7}\bigr)<578\,\rho_{\rm beat}$;
- Writing $w^{(m)}_k=\sum_{a=1}^3v_a\epsilon_{akm}$ ($|w^{(m)}|\le 1$ for $|v|=1$), $|v_aT^{ab}_{\rm beat,tot}v_b|\le\rho_{\rm beat}\bigl[\|S_\Sigma\|+\frac{1}{k_{\rm beat}^2}\sum_{m=1}^3|S_{\Phi,mm}|\|\operatorname{Hess}G\|\bigr]<\rho_{\rm beat}\bigl[\frac25+\frac{1}{36}\cdot\frac{288}{1225}\cdot 4.8\times 10^7\bigr]<(1+3.4\times 10^5)\rho_{\rm beat}$ (since $\frac{2}{49}+\frac{2}{25}+\frac{4}{35}=\frac{288}{1225}<\frac14$ and $\frac{4.8\times 10^7}{144}=\frac{10^6}{3}<3.4\times 10^5$).

Summing gives $|T^{00}_{\rm beat,tot}|+2|\vec T^{0\bullet}_{\rm beat,tot}|+\|T^{\rm sp}_{\rm beat,tot}\|<1{,}260{,}579\,\rho_{\rm beat}<2\times 10^6\,\rho_{\rm beat}$ everywhere on $\mathbb R^{1,3}$. Fix the explicit closed-form collar constant
$$
 U_{\rm col}^{\rm dyn}:=2\times 10^6\,\rho_{\rm beat}
  =\frac{10^6\sqrt{35}\,\pi A_*}{128c^3\tau^4}>0,\qquad
 T^{\rm tot,\pm}_{\mu\nu}(t,x)u^\mu w^\nu\ge 0\qquad\forall\,(t,x)\in\mathbb R^{1,3}, \tag{14}
$$
for all future-directed causal $u^\mu,w^\mu$, verified exhaustively across three regions covering $\mathbb R^3$:
1. **Inner cube $x\in\overline{\Omega_1}$.** Here $\chi_{\rm box}(x)=1$ and $|x|<L$, so $2T^{\mu\nu}_{\rm tot,vac}(x)\pm T^{\mu\nu}_{\rm beat,tot}(t,x)=T^{\mu\nu}_{{\rm ext},\pm}(t,x)$, which satisfies $T^{\rm ext,\pm}_{\mu\nu}u^\mu w^\nu\ge 0$ by (7), while $U_{\rm col}^{\rm dyn}(1-\chi_{\rm in}(x))\chi_{\rm out}(|x|/L)\delta^\mu_0\delta^\nu_0$ has nonnegative energy density and zero flux/stress, hence also satisfies DEC (with no boundary-layer deficit where $1-\chi_{\rm in}\to 0$ on $\partial\Omega$).
2. **Beat cutoff shell $x\in\overline{\Omega_2}\setminus\Omega_1$.** Here $\chi_{\rm in}(x)=0$ and $|x|<L<2L$, so $\chi_{\rm out}(|x|/L)=1$ and $T^{00}_{\rm plateau}(x)=U_{\rm col}^{\rm dyn}$ is strictly constant. For $S^{\mu\nu}:=U_{\rm col}^{\rm dyn}\delta^\mu_0\delta^\nu_0\pm T^{\mu\nu}_{\rm beat,tot}$ and $u^0\ge|\vec u|$, $w^0\ge|\vec w|$, Cauchy–Schwarz gives $S_{\mu\nu}u^\mu w^\nu=S^{00}u^0w^0-u^0(\vec S^{0\bullet}\cdot\vec w)-w^0(\vec S^{0\bullet}\cdot\vec u)+\vec u^{\mathsf T}S^{\rm sp}\vec w\ge\bigl(U_{\rm col}^{\rm dyn}-|T^{00}_{\rm beat,tot}|-2|\vec T^{0\bullet}_{\rm beat,tot}|-\|T^{\rm sp}_{\rm beat,tot}\|\bigr)u^0w^0\ge 0$, while $2T^{\mu\nu}_{\rm tot,vac}(x)$ independently satisfies DEC.
3. **Exterior $x\in\mathbb R^3\setminus\overline{\Omega_2}$.** Here $T^{\mu\nu}_{\rm beat,tot}(t,x)=0$ identically, leaving $2T^{\mu\nu}_{\rm tot,vac}(x)+U_{\rm col}^{\rm dyn}\chi_{\rm out}(|x|/L)\delta^\mu_0\delta^\nu_0$, which satisfies $\|T^{\rm sp}\|\le T^{00}$ and $T^{0a}=0$ everywhere.

Integrating $\partial_k\partial_l\Sigma^{kl}_{\rm beat}$ and $-\partial_k(\partial_0\Sigma^{kb}_{\rm beat})$ over $B_L(0)\supset\operatorname{supp}\Sigma^{\rm beat}$ gives zero beat energy and zero beat momentum at all $t\in\mathbb R$. Hence $\psi_+$, $\psi_-$, and $\rho_{\rm inc}$ share the exact constant total energy $E_{\rm tot}:=2(E_0+E_{\rm support})+E_{\rm plateau}>2E_0$ (where $E_{\rm support}:=\int_{\mathbb R^3\setminus\Omega}T^{00}_{\rm tot,vac}(y)\,d^3y>0$ is the static ground-collar energy from the [compact cavity source](compact_cavity_source_for_four_chain_field.md), so $\int_{\mathbb R^3}T^{00}_{\rm tot,vac}(y)\,d^3y=E_0+E_{\rm support}$, and $E_{\rm plateau}:=U_{\rm col}^{\rm dyn}\int_{\mathbb R^3}(1-\chi_{\rm in}(y))\chi_{\rm out}(|y|/L)\,d^3y>0$) and zero total linear momentum $P^a_{\rm tot}=0$ for all $t\in\mathbb R$.

## 3. Vanishing mass multipoles through octupole order

Because $\vartheta(-u)=\vartheta(u)$ is even and $\sin(-z)=-\sin z$ is odd, the cut-off scalar profile $G(y)=-\vartheta(y_1/L)\vartheta(y_2/L)\vartheta(y_3/L)\sin(\frac{5\pi}{L}y_1)\sin(\frac{7\pi}{L}y_2)$ satisfies exact coordinate-reflection parities on $\mathbb R^3$:
$$
 G(-y_1,y_2,y_3)=-G(y_1,y_2,y_3),\qquad
 G(y_1,-y_2,y_3)=-G(y_1,y_2,y_3),\qquad
 G(y_1,y_2,-y_3)=+G(y_1,y_2,y_3).
$$
In particular, $\int_{\mathbb R^3}G(y)\,d^3y=0$, and for every $d\in\{1,2,3\}$ the first moment $\int_{\mathbb R^3}y_dG(y)\,d^3y=0$ vanishes as well ($y_1G$ is odd in $y_2$, $y_2G$ is odd in $y_1$, and $y_3G$ is odd in $y_1,y_2,y_3$). Since $\Sigma^{kl}_{\rm beat}(t,\cdot)\in C_c^\infty(B_L(0))$ is proportional to $G(y)S_\Sigma^{kl}$, integrating $T^{00}_{\rm beat,tot}(t,y)=\partial_k\partial_l\Sigma^{kl}_{\rm beat}(t,y)$ twice by parts on $\mathbb R^3$ with zero boundary terms proves at every $t\in\mathbb R$:
$$
 \int_{\mathbb R^3}T^{00}_{\rm beat,tot}(t,y)\,d^3y=0,\qquad
 \int_{\mathbb R^3}y_aT^{00}_{\rm beat,tot}(t,y)\,d^3y
  =-\int_{\mathbb R^3}\partial_l\Sigma^{al}_{\rm beat}(t,y)\,d^3y=0,
$$
$$
 \int_{\mathbb R^3}y_ay_bT^{00}_{\rm beat,tot}(t,y)\,d^3y
  =2\int_{\mathbb R^3}\Sigma^{ab}_{\rm beat}(t,y)\,d^3y=0,
$$
$$
 \int_{\mathbb R^3}y_ay_by_cT^{00}_{\rm beat,tot}(t,y)\,d^3y
  =2\int_{\mathbb R^3}\bigl(y_a\Sigma^{bc}_{\rm beat}+y_b\Sigma^{ca}_{\rm beat}+y_c\Sigma^{ab}_{\rm beat}\bigr)(t,y)\,d^3y=0
 \qquad\forall\,a,b,c\in\{1,2,3\}. \tag{15}
$$
Note that even for $(a,b)=(1,2)$—where $y_1y_2T^{00}_{\rm beat,tot}$ is even in all three coordinates—the second moment in (15) vanishes identically because $\Sigma^{12}_{\rm beat}=0$ ($\partial_1^2(y_1y_2)=\partial_2^2(y_1y_2)=0$). Similarly, integrating $T^{0b}_{\rm beat,tot}=-\partial_0\partial_k\Sigma^{kb}_{\rm beat}$ and $T^{ab}_{\rm beat,tot}=\partial_0^2\Sigma^{ab}_{\rm beat}+\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi^{\rm beat}_{mn}$ by parts on $\mathbb R^3$ gives at every $t\in\mathbb R$:
$$
 \int_{\mathbb R^3}y_aT^{0b}_{\rm beat,tot}(t,y)\,d^3y
  =\int_{\mathbb R^3}\partial_0\Sigma^{ab}_{\rm beat}(t,y)\,d^3y=0,\qquad
 \int_{\mathbb R^3}y_ay_cT^{0b}_{\rm beat,tot}(t,y)\,d^3y
  =\int_{\mathbb R^3}\bigl(y_c\partial_0\Sigma^{ab}_{\rm beat}+y_a\partial_0\Sigma^{cb}_{\rm beat}\bigr)(t,y)\,d^3y=0,
$$
$$
 \int_{\mathbb R^3}T^{ab}_{\rm beat,tot}(t,y)\,d^3y=0,\qquad
 \int_{\mathbb R^3}y_cT^{ab}_{\rm beat,tot}(t,y)\,d^3y=0
 \qquad\forall\,a,b,c\in\{1,2,3\}. \tag{16}
$$
Consequently $\psi_+$, $\psi_-$, and $\rho_{\rm inc}$ share identical mass monopole, dipole, quadrupole, and octupole moments, zero angular momentum, identical current-quadrupole moments, and zero unweighted and first-moment spatial stress integrals at every time $t\in\mathbb R$. Applying the textbook long-wavelength mass-quadrupole gravitational-wave truncation ([Carroll, *Lecture Notes on General Relativity*, gr-qc/9712019v1, §6, Eqs. (6.78)–(6.85)](https://arxiv.org/pdf/gr-qc/9712019v1))—or even the next-order mass-octupole and current-quadrupole truncations—therefore returns identically zero radiative contrast among $\psi_+$, $\psi_-$, and $\rho_{\rm inc}$.

## 4. Retarded harmonic-gauge potential and outgoing tidal curvature contrast

Supply the whole-space linearized Einstein equations in harmonic (de Donder) gauge with the no-incoming-wave retarded integral from Eq. (9) of the [retarded stress calculation](retarded_stress_at_fixed_density.md), for each preparation label $z\in\{+,-,\mathrm{inc}\}$:
$$
 \Box\bar h_{\mu\nu}^z=-\frac{16\pi G}{c^4}T^{\mathrm{tot},z}_{\mu\nu},\qquad
 \Box=-\partial_0^2+\nabla^2,\qquad
 \bar h_{\mu\nu}^z(t,x)=\frac{4G}{c^4}\int_{\mathbb R^3}
  \frac{T^{\mathrm{tot},z}_{\mu\nu}(t-|x-y|/c,\,y)}{|x-y|}\,d^3y,
$$
$$
 h_{\mu\nu}^z=\bar h_{\mu\nu}^z-\frac12\eta_{\mu\nu}\eta^{\alpha\beta}\bar h_{\alpha\beta}^z,\qquad
 \partial^\mu\bar h_{\mu\nu}^z=0, \tag{17}
$$
where $T^{\mathrm{tot},z}_{00}=T^{00}_{\mathrm{tot},z}$, $T^{\mathrm{tot},z}_{0b}=-T^{0b}_{\mathrm{tot},z}$, and $T^{\mathrm{tot},z}_{ab}=T^{ab}_{\mathrm{tot},z}$. Changing variables to $w=x-y$ gives $\bar h_{\mu\nu}^z(t,x)=\frac{4G}{c^4}\int_{\mathbb R^3}|w|^{-1}T^{\mathrm{tot},z}_{\mu\nu}(t-|w|/c,x-w)\,d^3w$. For $|x|<R_0$, the integrand vanishes outside $|w|\le R_0+3L$, is smooth in $(t,x)$ for every $w\ne 0$ without differentiating $|w|$, and is dominated together with all $(t,x)$-derivatives by integrable multiples of $|w|^{-1}\in L^1(B_{R_0+3L}(0))$. Thus $\bar h_{\mu\nu}^z\in C^\infty(\mathbb R^{1,3})$, and differentiating under the $w$-integral yields
$$
 \partial^\mu\bar h_{\mu\nu}^z(t,x)
  =-\partial_0\bar h_{0\nu}^z(t,x)+\partial_{x_a}\bar h_{a\nu}^z(t,x)
  =\frac{4G}{c^4}\int_{\mathbb R^3}\frac{\bigl(-\partial_0T^{\mathrm{tot},z}_{0\nu}+\partial_{y_a}T^{\mathrm{tot},z}_{a\nu}\bigr)(t-|w|/c,\,x-w)}{|w|}\,d^3w=0,
$$
because $-\partial_0T^{\mathrm{tot},z}_{0\nu}+\partial_{y_a}T^{\mathrm{tot},z}_{a\nu}=\eta_{\nu\beta}\partial_\mu T^{\mu\beta}_{\mathrm{tot},z}=0$ pointwise on $\mathbb R^{1,3}$. Likewise, $\Box_x\bar h_{\mu\nu}^z(t,x)=\frac{4G}{c^4}\int_{\mathbb R^3}r_w^{-1}(\Box T^{\mathrm{tot},z}_{\mu\nu})(t-r_w/c,x-w)\,d^3w$ ($r_w=|w|$, $\hat w=w/r_w$); on $w\ne 0$, the vector field $V_a(w):=-\frac{\hat w_a}{r_w^2}T^{\mathrm{tot},z}_{\mu\nu}+\frac{1}{r_w}\partial_{y_a}T^{\mathrm{tot},z}_{\mu\nu}-\frac{\hat w_a}{cr_w}\partial_tT^{\mathrm{tot},z}_{\mu\nu}$ (evaluated at $(t-r_w/c,x-w)$) satisfies $\nabla_w\cdot V(w)=-r_w^{-1}(\Box T^{\mathrm{tot},z}_{\mu\nu})(t-r_w/c,x-w)$ identically, so applying the Gauss–Green theorem on $\epsilon<|w|<R_0+3L$ and sending $\epsilon\to 0^+$ yields $\Box_x\bar h_{\mu\nu}^z(t,x)=\frac{4G}{c^4}(-4\pi T^{\mathrm{tot},z}_{\mu\nu}(t,x))=-\frac{16\pi G}{c^4}T^{\mathrm{tot},z}_{\mu\nu}(t,x)$.

By linearity, $\bar h_{\mu\nu}^\pm(t,x)=\bar h_{\mu\nu}^{\rm inc}(x)\pm\bar h_{\mu\nu}^{\rm beat}(t,x)$, where $\bar h_{\mu\nu}^{\rm inc}(x)=\frac{4G}{c^4}\int_{\mathbb R^3}|x-y|^{-1}T^{\rm tot,inc}_{\mu\nu}(y)\,d^3y$ is purely static. Write $T^{ab}_{\rm beat,tot}(t,y)={\cal T}^{ab}_{\rm beat}(y)\cos(\Omega_{\rm beat}t)$ with ${\cal T}^{ab}_{\rm beat}(y)=\rho_{\rm beat}[-G(y)S_\Sigma^{ab}+k_{\rm beat}^{-2}\epsilon_{akm}\epsilon_{bln}S_{\Phi,mn}\partial_k\partial_lG(y)]$. For $|x|>L$ (strictly outside $\operatorname{supp}G\subset B_L(0)$), define the outgoing scalar convolution $I_{\rm beat}(x):=\int_{B_L(0)}G(y)|x-y|^{-1}e^{ik_{\rm beat}|x-y|}\,d^3y$. Integrating $\partial_{y_k}$ and $\partial_{y_k}\partial_{y_l}$ by parts on $B_L(0)$ using $\partial_{y_k}(|x-y|^{-1}e^{ik_{\rm beat}|x-y|})=-\partial_{x_k}(|x-y|^{-1}e^{ik_{\rm beat}|x-y|})$ and $T^{\rm beat,tot}_{0b}=-T^{0b}_{\rm beat,tot}=+\partial_0\partial_k\Sigma^{kb}_{\rm beat}$ yields the exact exterior identities for all $|x|>L$:
$$
 \bar h_{00}^{\rm beat}(t,x)=\frac{4G\rho_{\rm beat}}{c^4k_{\rm beat}^2}\,
  \operatorname{Re}\bigl[e^{-i\Omega_{\rm beat}t}S_\Sigma^{kl}\partial_k\partial_lI_{\rm beat}(x)\bigr],\qquad
 \bar h_{0b}^{\rm beat}(t,x)=\frac{4G\rho_{\rm beat}}{c^4k_{\rm beat}^2}\,
  \partial_0\operatorname{Re}\bigl[e^{-i\Omega_{\rm beat}t}S_\Sigma^{kb}\partial_kI_{\rm beat}(x)\bigr],
$$
$$
 \bar h_{ab}^{\rm beat}(t,x)=\frac{4G\rho_{\rm beat}}{c^4k_{\rm beat}^2}\,
  \operatorname{Re}\Bigl[e^{-i\Omega_{\rm beat}t}\bigl(-k_{\rm beat}^2S_\Sigma^{ab}I_{\rm beat}(x)
  +\epsilon_{akm}\epsilon_{bln}S_{\Phi,mn}\partial_k\partial_lI_{\rm beat}(x)\bigr)\Bigr]\qquad(|x|>L). \tag{18}
$$

For $x=rn$ ($r>2L$, $n\in S^2$) and $y\in B_L(0)$, put $d=|rn-y|\in(r-L,r+L)$ and $\hat z=(rn-y)/d$. For each derivative order $m\in\{0,1,2,3,4\}$, differentiating $d^{-1}e^{ik_{\rm beat}d}$ gives $(ik_{\rm beat})^m\hat z_{a_1}\cdots\hat z_{a_m}d^{-1}e^{ik_{\rm beat}d}+O(d^{-2})$ because every derivative hitting $d^{-1}$ or $\hat z$ lowers the power of $d$ by at least one; since $|\hat z_a-n_a|\le 4L/r$, $|d^{-1}-r^{-1}|\le 2L/r^2$, and $|e^{ik_{\rm beat}d}-e^{ik_{\rm beat}(r-n\cdot y)}|\le k_{\rm beat}|d-(r-n\cdot y)|\le k_{\rm beat}L^2/r$, integrating against $G\in C_c^\infty(B_L(0))$ yields uniformly in $n\in S^2$:
$$
 \partial_{a_1}\cdots\partial_{a_m}I_{\rm beat}(rn)
  =(ik_{\rm beat})^mn_{a_1}\cdots n_{a_m}\,\frac{e^{ik_{\rm beat}r}}{r}\,\widehat G(k_{\rm beat}n)+O(r^{-2})\qquad(0\le m\le 4),
$$
$$
 \widehat G(q):=\int_{\mathbb R^3}G(y)e^{-iq\cdot y}\,d^3y
  =-\int_{\mathbb R^3}G(y)\sin(q_1y_1)\sin(q_2y_2)\cos(q_3y_3)\,d^3y\in\mathbb R,
$$
$$
 \widehat G(\pm k_{\rm beat}e_a)=0\quad(a=1,2,3). \tag{19}
$$
In (19), reality and factorization of $\widehat G(q)$ follow from the coordinate parities of $G(y)$ because only $(-i\sin q_1y_1)(-i\sin q_2y_2)(\cos q_3y_3)=-\sin(q_1y_1)\sin(q_2y_2)\cos(q_3y_3)$ survives integration. Whenever $q_1=0$ or $q_2=0$, $\widehat G(q)=0$; hence along all six coordinate rays $n\in\{\pm e_1,\pm e_2,\pm e_3\}$, every $1/r$ radiative component of $\bar h_{\mu\nu}^{\rm beat}(t,rn)$ and of its linearized Riemann curvature vanishes identically.

Now fix the equatorial bisector ray and orthonormal transverse polarization basis
$$
 n_*:=\frac{1}{\sqrt2}(e_1+e_2),\qquad
 e_\vartheta:=\frac{1}{\sqrt2}(e_1-e_2),\qquad
 e_3=(0,0,1),
$$
which satisfy $|n_*|=|e_\vartheta|=|e_3|=1$ and $n_*\cdot e_\vartheta=n_*\cdot e_3=e_\vartheta\cdot e_3=0$. At fixed retarded time $U:=t-r/c$ (so $\operatorname{Re}[e^{-i\Omega_{\rm beat}t}e^{ik_{\rm beat}r}]=\cos(\Omega_{\rm beat}U)$ since $\widehat G(k_{\rm beat}n_*)\in\mathbb R$), substituting (19) ($m=0,2$) into (18) gives $\bar h_{ab}^{\rm beat}(t,rn_*)=\frac{4G}{c^4r}\widehat{\cal T}^{ab}_{\rm beat}(k_{\rm beat}n_*)\cos(\Omega_{\rm beat}U)+O(r^{-2})$, where double integration by parts cancels $k_{\rm beat}^{-2}$ against $-k_{\rm beat}^2$:
$$
 \widehat{\cal T}^{ab}_{\rm beat}(k_{\rm beat}n_*)
  :=\int_{\mathbb R^3}{\cal T}^{ab}_{\rm beat}(y)e^{-ik_{\rm beat}n_*\cdot y}\,d^3y
  =\rho_{\rm beat}\widehat G(k_{\rm beat}n_*)\bigl[-S_\Sigma^{ab}-\epsilon_{akm}\epsilon_{bln}n_{*,k}n_{*,l}S_{\Phi,mn}\bigr].
$$
For any $v\in\mathbb R^3$, $-v_av_b\epsilon_{akm}\epsilon_{bln}n_{*,k}n_{*,l}S_{\Phi,mn}=\sum_{m=1}^3(-S_{\Phi,mm})[(v\times n_*)_m]^2$. Using $e_\vartheta\times n_*=+e_3$ and $e_3\times n_*=\frac{1}{\sqrt2}(-e_1+e_2)$ together with $S_\Sigma=\operatorname{diag}(\frac25,-\frac27,0)$ and $-S_\Phi=\operatorname{diag}(\frac{2}{49},\frac{2}{25},\frac{4}{35})$,
- Along $e_\vartheta$: $-e_\vartheta^ae_\vartheta^bS_\Sigma^{ab}=\frac12(-\frac25+\frac27)=-\frac{2}{35}$, and $\sum_m(-S_{\Phi,mm})[(e_\vartheta\times n_*)_m]^2=+\frac{4}{35}$, summing to $-\frac{2}{35}+\frac{4}{35}=+\frac{2}{35}=+\frac{70}{1225}$;
- Along $e_3$: $-e_3^ae_3^bS_\Sigma^{ab}=0$, and $\sum_m(-S_{\Phi,mm})[(e_3\times n_*)_m]^2=\frac12(\frac{2}{49}+\frac{2}{25})=\frac{1}{49}+\frac{1}{25}=+\frac{74}{1225}$.

Subtracting the two transverse projections yields the exact rational coefficient
$$
 \bigl(e_\vartheta^ae_\vartheta^b-e_3^ae_3^b\bigr)\widehat{\cal T}^{ab}_{\rm beat}(k_{\rm beat}n_*)
  =\left(-\frac{2}{35}+\frac{4}{35}-\frac{74}{1225}\right)\rho_{\rm beat}\widehat G(k_{\rm beat}n_*)
  =-\frac{4}{1225}\,\rho_{\rm beat}\widehat G(k_{\rm beat}n_*). \tag{20}
$$

Adopt the linearized Riemann curvature convention of the [static stress-quadrupole example](stress_quadrupole_at_equal_energy.md) and [retarded stress calculation](retarded_stress_at_fixed_density.md), $R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}+\Gamma^\rho_{\mu\alpha}\Gamma^\alpha_{\nu\sigma}-\Gamma^\rho_{\nu\alpha}\Gamma^\alpha_{\mu\sigma}$, which gives the gauge-invariant electric curvature $R^{(1)}_{0a0b}=-\frac12\partial_0^2h_{ab}+\frac12\partial_0(\partial_ah_{0b}+\partial_bh_{0a})-\frac12\partial_a\partial_bh_{00}$. Along $n_*$, define the plus electric-curvature channel for $z\in\{+,-,\mathrm{inc}\}$:
$$
 \mathcal E_z(t,r):=\frac12\bigl(R^{(1),z}_{0\vartheta 0\vartheta}-R^{(1),z}_{0303}\bigr)(t,rn_*),\qquad
 R^{(1),z}_{0\vartheta 0\vartheta}:=e_\vartheta^ae_\vartheta^bR^{(1),z}_{0a0b}.
$$
In the source-to-source difference $\Delta\mathcal E(t,r):=\mathcal E_+(t,r)-\mathcal E_-(t,r)=2[\mathcal E_\pm(t,r)-\mathcal E_{\rm inc}(r)]$ (with sign $\pm$), the static field $h_{\mu\nu}^{\rm inc}(x)$ cancels identically at all radii. For the beat perturbation $\Delta h_{\mu\nu}=2h_{\mu\nu}^{\rm beat}$, (18)–(19) show that at order $1/r$ every spatial derivative $\partial_a\Delta h_{\mu\nu}(t,rn_*)$ is proportional to $n_{*,a}$, so $e_\perp^ae_\perp^b\partial_0\partial_a\Delta h_{0b}(t,rn_*)=O(r^{-2})$ and $e_\perp^ae_\perp^b\partial_a\partial_b\Delta h_{00}(t,rn_*)=O(r^{-2})$ for both $e_\perp\in\{e_\vartheta,e_3\}$ by $e_\perp\cdot n_*=0$. Moreover, $|e_\vartheta|^2=|e_3|^2=1$ cancels the trace-reversal term $-\frac12\delta_{ab}\eta^{\alpha\beta}\Delta\bar h_{\alpha\beta}$ between $e_\vartheta$ and $e_3$. Using $-\frac14\partial_0^2[2\cos(\Omega_{\rm beat}U)]=+\frac12k_{\rm beat}^2\cos(\Omega_{\rm beat}U)$ and $\frac12\cdot 4\cdot(-\frac{4}{1225})=-\frac{8}{1225}$ from (18) and (20) gives
$$
 \Delta\mathcal E(t,r):=\mathcal E_+(t,r)-\mathcal E_-(t,r)
  =-\frac{8\,G\,k_{\rm beat}^2\,\rho_{\rm beat}\,\widehat G(k_{\rm beat}n_*)}{1225\,c^4r}\cos(\Omega_{\rm beat}U)+O(r^{-2})\qquad(U=t-r/c). \tag{21}
$$

To determine the sign and strict nonvanishing of (21) without numerical quadrature, substitute $y_a=Lu_a$ and $k_{\rm beat}n_*L=\frac{2\pi}{L}\cdot\frac{1}{\sqrt2}(e_1+e_2)L=(\sqrt2\pi,\sqrt2\pi,0)$ into (19):
$$
 \widehat G(k_{\rm beat}n_*)=L^3\,{\cal J}_1(\sqrt2\pi)\,{\cal J}_2(\sqrt2\pi)\,{\cal J}_0,
$$
$$
 {\cal J}_1(\xi):=\int_{\mathbb R}\vartheta(u)\sin(5\pi u)\sin(\xi u)\,du,\quad
 {\cal J}_2(\xi):=\int_{\mathbb R}\vartheta(u)\sin(7\pi u)\sin(\xi u)\,du,\quad
 {\cal J}_0:=\int_{\mathbb R}\vartheta(u)\,du. \tag{22}
$$
Split ${\cal J}_j(\sqrt2\pi)={\cal J}_j^{\rm core}(\sqrt2\pi)+{\cal J}_j^{\rm tail}(\sqrt2\pi)$ into the cavity-interior integral over $[-1/2,1/2]$ (where $\vartheta(u)=1$) and the cutoff tail over $[-s_2,-1/2]\cup[1/2,s_2]$. On $[-1/2,1/2]$, using $2\sin(m\pi u)\sin(\xi u)=\cos((m\pi-\xi)u)-\cos((m\pi+\xi)u)$, $\sin(\frac{5\pi}{2}\mp\frac{\xi}{2})=+\cos(\frac{\xi}{2})$, and $\sin(\frac{7\pi}{2}\mp\frac{\xi}{2})=-\cos(\frac{\xi}{2})$ gives at $\xi=\sqrt2\pi$:
$$
 {\cal J}_1^{\rm core}(\sqrt2\pi)
  =\frac{2\sqrt2\,\cos(\pi/\sqrt2)}{23\pi},\qquad
 {\cal J}_2^{\rm core}(\sqrt2\pi)
  =-\frac{2\sqrt2\,\cos(\pi/\sqrt2)}{47\pi}.
$$
Establish the required rational bounds from first principles:
1. **$3<\pi<\frac{22}{7}$.** For $x\in(0,1)$, $0<\frac{x^4(1-x)^4}{1+x^2}=x^6-4x^5+5x^4-4x^2+4-\frac{4}{1+x^2}$; integrating over $[0,1]$ yields $0<\frac17-\frac23+1-\frac43+4-\pi=\frac{22}{7}-\pi$.
2. **$\cos(\pi/\sqrt2)<-\frac12$.** Since $1^2<2<(\frac32)^2$, $1<\sqrt2<\frac32$, so $\frac{2\pi}{3}<\frac{\pi}{\sqrt2}<\pi$. Because $\frac{d}{d\theta}\cos\theta=-\sin\theta<0$ on $(0,\pi)$, $\cos(\pi/\sqrt2)<\cos(2\pi/3)=-\frac12$, i.e., $-\cos(\pi/\sqrt2)>\frac12$.
3. **$\frac75<\sqrt2$ and tail bound $|{\cal J}_j^{\rm tail}(\sqrt2\pi)|\le\frac{1}{150}$.** Since $7^2=49<50=2\cdot 5^2$, $\sqrt2>\frac75$. Because $0\le\vartheta(u)\le 1$ and $\operatorname{supp}(\vartheta-\mathbf 1_{[-1/2,1/2]})\subseteq[-s_2,-1/2]\cup[1/2,s_2]$ has total measure $2(s_2-\frac12)=4\delta_1=\frac{4}{600}=\frac{1}{150}$, we have $|{\cal J}_j^{\rm tail}(\sqrt2\pi)|\le\frac{1}{150}$ ($j=1,2$).

Combining (1)–(3) proves strict opposite signs of ${\cal J}_1(\sqrt2\pi)$ and ${\cal J}_2(\sqrt2\pi)$:
$$
 -{\cal J}_1(\sqrt2\pi)\ge -{\cal J}_1^{\rm core}(\sqrt2\pi)-\frac{1}{150}
  >\frac{\sqrt2}{23\pi}-\frac{1}{150}
  >\frac{7/5}{23\cdot(22/7)}-\frac{1}{150}
  =\frac{49}{2530}-\frac{1}{150}=\frac{241}{18{,}975}>\frac{1}{80}>0,
$$
$$
 {\cal J}_2(\sqrt2\pi)\ge{\cal J}_2^{\rm core}(\sqrt2\pi)-\frac{1}{150}
  >\frac{\sqrt2}{47\pi}-\frac{1}{150}
  >\frac{7/5}{47\cdot(22/7)}-\frac{1}{150}
  =\frac{49}{5170}-\frac{1}{150}=\frac{109}{38{,}775}>\frac{1}{360}>0,
$$
while ${\cal J}_0\ge\int_{-1/2}^{1/2}1\,du=1>0$. Therefore $\widehat G(k_{\rm beat}n_*)=L^3{\cal J}_1(\sqrt2\pi){\cal J}_2(\sqrt2\pi){\cal J}_0<-\frac{L^3}{28{,}800}<0$ strictly. Substituting $k_{\rm beat}^2\rho_{\rm beat}L^3=\bigl(\frac{\pi^2}{4c^2\tau^2}\bigr)\bigl(\frac{\sqrt{35}\,\pi A_*}{256c^3\tau^4}\bigr)(64c^3\tau^3)=\frac{\sqrt{35}\,\pi^3A_*}{16c^2\tau^3}$ into (21) at phase origin $U=0$ ($t=r/c$) yields the exact asymptotic radiative contrast and closed-form lower bound:
$$
 \boxed{
 {\cal C}_{\rm beat}:=\lim_{r\to\infty}r\,\bigl[\mathcal E_+(r/c,r)-\mathcal E_-(r/c,r)\bigr]
  =\frac{\sqrt{35}\,\pi^3}{2450}\,\frac{GA_*}{c^6\tau^3}\,
   \bigl(-{\cal J}_1(\sqrt2\pi)\bigr){\cal J}_2(\sqrt2\pi){\cal J}_0
  >\frac{\sqrt{35}\,\pi^3}{70{,}560{,}000}\,\frac{GA_*}{c^6\tau^3}
  >\frac{\pi^3}{14{,}112{,}000}\,\frac{GA_*}{c^6\tau^3}>0.} \tag{23}
$$
Relative to the static incoherent mixture $\rho_{\rm inc}$ (for which $\lim_{r\to\infty}r\mathcal E_{\rm inc}(r)=0$), each coherent state satisfies $\lim_{r\to\infty}r[\mathcal E_\pm(r/c,r)-\mathcal E_{\rm inc}(r)]=\pm\frac12{\cal C}_{\rm beat}\ne 0$. For nearby freely falling test bodies initially at rest near $(t,rn_*)$ separated along $e_\vartheta$ vs. $e_3$, the leading geodesic-deviation relative-acceleration contrast is $-c^2\Delta\mathcal E(t,r)$.

## 5. Native history bookkeeping, dimensional ledger and scope boundaries

The complete native four-birth probability law is retained unchanged from the [finite source table](finite_interval_action_and_source_preparation.md). Conditional on the fixed prepared prefix $a\prec b$ with marks $(i,0)$ and descendant counters $(1,0)$ for $i\in\{0,1\}$, the 15 predecessor-ideal pairs $(I_x,I_y)$ carry the following exact structural probability numerators over $1320$ (concatenation denotes a set):

| $I_x$ | $I_y$ | $1320P_0$ | $1320P_1$ | Dynamical cavity-collar status |
|---|---|---:|---:|---|
| $\varnothing$ | $\varnothing$ | 6 | 6 | `"unavailable"` |
| $\varnothing$ | $x$ | 6 | 6 | `"unavailable"` |
| $\varnothing$ | $a$ | 5 | 10 | `"unavailable"` |
| $\varnothing$ | $ab$ | 19 | 14 | `"unavailable"` |
| $\varnothing$ | $ax$ | 33 | 33 | `"unavailable"` |
| $\varnothing$ | $abx$ | 195 | 195 | `"unavailable"` |
| $a$ | $\varnothing$ | 5 | 10 | `"unavailable"` |
| $a$ | $a$ | 5 | 10 | `"unavailable"` |
| $a$ | $ab$ | 19 | 14 | `"unavailable"` |
| $a$ | $ax$ | 19 | 14 | `"unavailable"` |
| $a$ | $abx$ | 172 | 392 | `"unavailable"` |
| $ab$ | $\varnothing$ | 19 | 14 | `"unavailable"` |
| $ab$ | $a$ | 19 | 14 | `"unavailable"` |
| $ab$ | $ab$ | 19 | 14 | `"unavailable"` |
| $ab$ | $abx$ | 779 | 574 | `"available"` |
| **Total** | | **1320** | **1320** | |

Each structural row splits into four fair ordered suffix-mark pairs of equal conditional weight $\frac14$, accounting for all $60$ marked histories $H$ per preparation $i\in\{0,1\}$ with denominator $5280$. Let $\mathcal C$ denote the four marked instances of the fifteenth row $(I_x,I_y)=(ab,abx)$ ($a\prec b\prec x\prec y$), which has structural probabilities $779/1320$ ($i=0$) and $574/1320$ ($i=1$) and per-marked-history probabilities $779/5280$ and $574/5280$. Following the tag-registration discipline of the [coherent inertia analysis](coherent_inertia_from_opposite_kicks.md) and [compact cavity source](compact_cavity_source_for_four_chain_field.md), draw the cavity-state preparation tag $z\in\{+,-,\mathrm{inc}\}$ independently of $H$ with uniform conditional weight $\frac13$ on every history:
$$
 {\Pr}_i(H,z,\mathrm{available},\mathcal E=\mathcal E_z)=\frac{P_i(H)}{3}\quad(H\in\mathcal C),\qquad
 {\Pr}_i(H,z,\mathrm{unavailable},\mathcal E=\bot)=\frac{P_i(H)}{3}\quad(H\notin\mathcal C). \tag{24}
$$
Summing (24) over $z\in\{+,-,\mathrm{inc}\}$ and all $60$ marked histories recovers $\sum_{H,z}=1$ and preserves every native history probability without reweighting, post-selection, or feedback into the growth law. In this two-mode four-chain dynamical source ledger, the 14 non-chain structural rows ($56$ marked histories) remain `"unavailable"`.

The normalization, weak-field, and dimensional relations are explicit:
$$
 F_*^2=\frac{A_*}{28\pi\kappa c\tau^2\,\beta(\sqrt2+1)},\qquad
 \frac{L}{c\tau}=4,\qquad
 \Omega_{\rm beat}\tau=\frac{\pi}{2},\qquad
 k_{\rm beat}L=2\pi,\qquad
 \frac{\rho_{\rm beat}}{\rho_0}=\frac{\sqrt{35}}{6},
$$
$$
 g:=\frac{G\rho_0L^2}{c^4}=\frac{3\pi GA_*}{8c^5\tau^2}\ll 1,\qquad
 {\cal C}_{\rm beat}L=O(g)\ll 1. \tag{25}
$$
If $\Psi$ has field units ${\cal F}$, then $B_j,F_*$ have units ${\cal F}$, $\kappa$ has units $\text{energy}/({\cal F}^2\cdot\text{length})$, every component of $T^{\mu\nu}_{\rm sc},T^{\mu\nu}_{\mathrm{tot},z},{\cal T}^{ab}_{\rm beat}$ and $\rho_0,\rho_{\rm beat},U_{\rm col}^{\rm dyn}$ has energy-density units $\text{energy}/\text{length}^3$, $\Sigma^{\rm beat}_{ab},\Phi^{\rm beat}_{mn}$ have force units $\text{energy}/\text{length}$, $G_{\rm int},G,\chi_{\rm in},\chi_{\rm box},S_\Sigma,S_\Phi,{\cal J}_1,{\cal J}_2,{\cal J}_0,\bar h_{\mu\nu}^z,h_{\mu\nu}^z$ are dimensionless, $\widehat G(q)$ has units $\text{length}^3$, $\widehat{\cal T}^{ab}_{\rm beat}(q)$ has units $\text{energy}$, $I_{\rm beat}(x)$ has units $\text{length}^2$, $\mathcal E_z$ and $\Delta\mathcal E$ have curvature units $\text{length}^{-2}$, ${\cal C}_{\rm beat}$ and $\frac{GA_*}{c^6\tau^3}$ have units $\text{length}^{-1}$, and $-c^2\Delta\mathcal E$ has units $\text{time}^{-2}$. Rescaling $\Psi\mapsto s\Psi$ and $\kappa\mapsto\kappa/s^2$ ($s>0$) leaves $H_{\rm sc}$, $T^{\mu\nu}_{\mathrm{tot},z}$, $\bar h_{\mu\nu}^z$, $\mathcal E_z$, and ${\cal C}_{\rm beat}$ invariant. Because $\frac{\rho_{\rm beat}}{\rho_0}=\frac{\sqrt{35}}{6}$ and $\frac{U_{\rm col}^{\rm dyn}}{\rho_0}=\frac{10^6\sqrt{35}}{3}$ are fixed $O(1)$ dimensionless constants independent of $g$, the supplied condition $g\ll 1$ keeps $|\bar h_{\mu\nu}^z|=O(g)\ll 1$ throughout $\mathbb R^{1,3}$.

The boundary between native and externally supplied premises and the methodological limits of this construction are strict:

- **Supplied by the native growth law:** the 15 four-birth predecessor-ideal pairs, their exact rational continuation probabilities over $1320$ and $5280$, and the chain order $a\prec b\prec x\prec y$ on the fifteenth row.
- **Externally supplied in this conditional construction:** the continuum background $\mathbb R^{1,3}$ and signature $(-+++)$, physical parameters $c,\tau,A_*,\kappa,G$, the released prefix $W_2$ and unaliased phases $(5\pi/4,7\pi/4)$, the cubic Neumann domain $\Omega$ and mode integers $(5,7)$, the single-excitation preparations $\psi_\pm,\rho_{\rm inc}$ with a common phase origin, the zero-offset Weyl-ordered stress prescription (3), the classical four-dimensional collar superpotential $(\Sigma^{\rm beat},\Phi^{\rm beat})$ and static plateau $U_{\rm col}^{\rm dyn}$, the semiclassical retarded field equation (17) in the weak-field regime $g\ll 1$, and the asymptotic ray $n_*$ and transverse polarization axes $(e_\vartheta,e_3)$.
- **Semiclassical expectation sourcing, steady-state scope, and collar non-uniqueness:** Equation (17) couples a classical metric perturbation to the expectation value $\operatorname{Tr}(\rho_z T^{\rm tot}_{\mu\nu})$; no quantized graviton state or quantum superposition of spacetime geometries is claimed. Under autonomous evolution $e^{-itH_{\rm sc}/A_*}$, $T^{\mu\nu}_{{\rm tot},\pm}(t,x)$ is spatially compact at every $t$ and bounded for all $t\in\mathbb R$, making the retarded integral over $\overline{B_{3L}(0)}$ exact at $O(G)$, whereas quadratic gravitational-wave energy flux and radiative damping of the two-mode coherence enter at $O(G^2)$ beyond the retained linear approximation (matching the [retarded stress calculation](retarded_stress_at_fixed_density.md)). Exteriority $r>3L$ gives exact outgoing representation (18), while interpreting the $1/r$ coefficient as dominant requires the far-field wave zone $r\gg L$ (where $k_{\rm beat}r=2\pi r/L\gg 1$); no finite-radius remainder bound or detector noise budget is claimed. The synchronous classical collar $(\Sigma^{\rm beat},\Phi^{\rm beat})$ is a non-unique mathematical completion proving admissibility rather than a constitutive material wall model, though the small shell parameter $\delta_1=\frac{1}{600}$ ensures that the sign and nonvanishing of ${\cal C}_{\rm beat}$ in (23) are dominated by the cavity interior $\Omega$.
- **Unassigned operational costs and Status-M quarantine:** Preparing $\psi_\pm$ or $\rho_{\rm inc}$, maintaining a common phase and clock reference, confining the cavity and collar stresses, resolving asymptotic tidal curvature, and resetting the apparatus carry unassigned work and thermodynamic costs (`docs/coordination/FOUNDATIONAL_RESEARCH_SCOPE.md`). Software remains paused. Track-B ontology and Status-M commitments (`ONTOLOGY.md`, `PHYSICS.md`, `GOVERNANCE.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined and enter no equation, variable, or inference.

The scoped decision is therefore **compatible on the selected four-chain row as an isolated whole-space conserved, dominant-energy-compliant dynamical semiclassical source whose opposite-phase two-mode quantum coherence generates a strictly nonzero outgoing $1/r$ retarded electric-curvature contrast ${\cal C}_{\rm beat}>0$ along $n_*=\frac{1}{\sqrt2}(e_1+e_2)$ while all mass multipoles through octupole order and all coordinate-axis $1/r$ radiation vanish**.

## Scientific review

Dynamical Cavity-Beat & Retarded Gravity Author derived the single-excitation two-mode cavity beat stress tensor, zero-offset interior dominant-energy proof, spatial-Beltrami obstruction, four-dimensional Riemann-symmetric collar superpotential and staggered cutoff bounds, multipole vanishing through octupole order, retarded harmonic-gauge field, and quadrature-free outgoing $1/r$ electric-curvature contrast along $n_*=\frac{1}{\sqrt2}(e_1+e_2)$. Independent Retarded Cavity-Beat Reviewer independently verified every matrix element, conservation law, null-cone Gram decomposition, superpotential component, bump derivative bound, whole-space dominant-energy inequality, Gauss–Green wave-equation proof, transverse polarization projection, rational Fourier lower bound, native 60-history probability table, dimensional relation, and scope boundary. Prospective protocol SHA-256 e14d7f487770a91fb38fce6bd7a2f7fbd65a04d97d5143304383bf29e89ab8a1; accepted author report SHA-256 2d438609ce58ac92997c09b5551f55df32d5ce25a9d2176633a37f617b511e8d; independent scientific review SHA-256 6f9ff02d7908c5e3fc2df7b7b2bb8fe3b6573790b88e58730cf64ef757759adf.
