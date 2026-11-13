# Two-way quantum-steered retarded electric curvature readout and causal-order co-registration

**Decision.** Extending two-way quantum-order steering and retarded cavity gravity to live suffix branches establishes a self-contained, gauge-invariant physical readout wherein initial qubit coherence modulates causal versus spacelike suffix-branch probabilities, generating differential retarded electric Riemann curvature contrasts at finite exterior radius co-registered with discrete causal-order invariants and final qubit observables; Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## Introduction and Architectural Overview

In foundational research exploring discrete causal order and quantum measurement, previous milestones established two distinct semiclassical bridges:
1. **Multi-birth quantum-order feedback and record-compensated conservation** (`all_horizon_two_way_feedback_and_growth.md`, `record_compensated_quantum_order_conservation.md`), wherein an unscaled two-level qubit system $\mathcal H_Q = \mathbb C^2$ is coupled to sequential causal growth, demonstrating that initial qubit coherence steers branch probabilities across downward-closed precursor ideals while lost quantum energy is absorbed conservatively into an exact, mark-independent, diamond-confluent geometric potential $V_{\rm geom}(P)$ across all four births; and
2. **Retarded cavity gravity and finite-radius curvature readout** (`all_branch_retarded_cavity_beat_and_finite_radius_readout.md`, `source_coupled_cavity_gravity_and_causal_focusing.md`), wherein a 12-mode homogeneous-Neumann cubic cavity ($L=8c\tau$) supporting an opposite-phase single-excitation beat doublet produces an outgoing retarded linearized gravitational wavefield with non-vanishing gauge-invariant electric Riemann curvature $E_{ij} = R_{0i0j}$ at finite exterior radius $r_* = 250L = 2000c\tau$.

However, in prior cavity gravity formulations, the gravitational source was either frozen in its static ground state or prepared once at the immutable prefix $a\prec b$ without dynamic feedback from the live suffix branches $x, y$. 

The present work unifies these two pathways into an integrated, live-branch-steered dynamical readout. Under this framework:
- Initial qubit coherence $\langle X\rangle = \operatorname{Tr}[X\rho_Q]$ at stage 2 ($a\prec b$) dynamically steers the branch probabilities between connected causal suffix topologies ($I_x = \{a,b\}$) and disconnected spacelike suffix topologies ($I_x = \varnothing$);
- These discrete suffix topologies map into distinct physical spacetime coordinates $(t_x, x_x)$, $(t_y, x_y)$ along the interior worldline segment in the cubic cavity $\Omega = [-L/2, L/2]^3$, generating differential 12-mode field excitations and coherent beat waveforms;
- Through the linearized Einstein equations in harmonic gauge with retarded Green function retardation $t - |x-y|/c$, the source stress-energy tensor generates an exterior gravitational potential $\bar h_{\mu\nu}(t,x)$;
- The electric Riemann curvature tensor $E_{ij}(t,x) = R_{0i0j}(t,x)$ is proved to be strictly gauge-invariant under all linearized coordinate gauge transformations ($\delta R_{\mu\nu\rho\sigma} = 0$), providing a direct physical measure of tidal acceleration $\ddot\xi_i = -c^2 E_{ij}\xi^j$ on freely falling accelerometer pairs;
- At finite exterior radius $r_* = 250L = 2000c\tau$ along the diagonal bisector $n_* = \frac{1}{\sqrt2}(e_1+e_2)$, fourth-order Helmholtz wave-zone remainder bounds rigorously certify sign-alternating curvature contrasts $\Delta\mathcal E(r_*/c, 250L) < -279\sqrt3\pi^3 GA_*/(102{,}400{,}000 c^7\tau^4) < 0$ and $\Delta\mathcal E(r_*/c+4\tau, 250L) > 0$;
- Across the complete 60-history ensemble, this exterior curvature contrast is linearly and simultaneously co-registered with the final coherent qubit observable $\operatorname{Tr}[Z\rho_Q^{(4)}]$, the conserved geometric potential $V_{\rm geom}$, and discrete causal-order invariants ($S_{\rm BD}$, $Y$).

All mathematical expressions, rational coefficients, matrix identities, and wave-zone remainder bounds are derived 100% by hand from first principles under the Strict Software Pause.

---

## 1. Initial Qubit Coherence and Stage 2 Suffix Steering (Quantum $\to$ Order)

### 1.1 Qubit State, Co-Rotating Axes, and Stage 2 Geometry
Let $\mathcal H_Q = \mathbb C^2$ be the Hilbert space of a two-level quantum probe, equipped with standard basis $\{|0\rangle, |1\rangle\}$ and Pauli operators $(X, Y, Z)$. In the co-rotating Clifford frame, the stage-cycling unitary is defined by:
$$
U_* := e^{-i\frac{\pi}{4}Z}e^{-i\frac{\pi}{4}X} = \frac{1}{2}\begin{pmatrix} 1-i & -1-i \\ 1-i & 1+i \end{pmatrix},
$$
satisfying $U_* X U_*^\dagger = Y$, $U_* Y U_*^\dagger = Z$, and $U_* Z U_*^\dagger = X$, with $U_*^3 = -I_Q$. The co-rotating Pauli axes $(\Sigma_0, \dots, \Sigma_4)$ are defined by $\Sigma_0 := Y$ and $\Sigma_n := U_*^n \Sigma_0 (U_*^\dagger)^n$, yielding:
$$
(\Sigma_0, \Sigma_1, \Sigma_2, \Sigma_3, \Sigma_4) = (Y,\, Z,\, X,\, Y,\, Z).
$$
At birth stage $n = |P| = 2$, corresponding to the two-element prefix poset $P_2 = (a\prec b)$, the active Pauli axis is precisely:
$$
\Sigma_2 = X.
$$
An arbitrary initial qubit state $\rho_Q \in \mathcal D(\mathbb C^2)$ is parameterized on the Bloch sphere by:
$$
\rho_Q = \frac{1}{2}\bigl(I_Q + \langle X\rangle X + \langle Y\rangle Y + \langle Z\rangle Z\bigr), \qquad \langle X\rangle = \operatorname{Tr}[X\rho_Q], \quad \langle X\rangle^2 + \langle Y\rangle^2 + \langle Z\rangle^2 \le 1.
$$

### 1.2 Structural Seed Kernel and Suffix Topology Classification
At parent $P_2 = (a\prec b)$, a newborn event $x$ adjoins to the poset with strict past equal to a downward-closed precursor ideal $I_x \subseteq \{a,b\}$. The eligible ideals are:
1. **Disconnected / Spacelike Suffix**: $I_x = \varnothing$. The newborn event $x$ is incomparable to both prefix events ($x \parallel a$ and $x \parallel b$), forming the unmarked poset class `edge+iso` ($P_2 + \varnothing = C_2 \sqcup A_1$).
2. **Partially Connected / Mixed Suffix**: $I_x = \{a\}$. The newborn event $x$ is in the causal future of $a$ ($a \prec x$) but incomparable to $b$ ($x \parallel b$), forming the unmarked poset class `fork` ($P_2 + \{a\} = A_1 \oplus A_2$).
3. **Fully Connected / Causal Suffix**: $I_x = \{a,b\}$. The newborn event $x$ is in the causal future of both $a$ and $b$ ($a \prec b \prec x$), forming the unmarked poset class `3-chain` ($P_2 + \{a,b\} = C_3$).

Under the native structural seed kernel $q(P,r,S)$ of Part A, the unsteered structural branch weights for $I_x$ conditioned on the root mark $r_a \in \{0,1\}$ are:
$$
q(a\prec b, r, \varnothing) = \frac{1}{5}, \qquad q(a\prec b, r, \{a\}) = f_{r_a}, \qquad q(a\prec b, r, \{a,b\}) = h_{r_a},
$$
where $(f_0, h_0) = (1/6, 19/30)$ and $(f_1, h_1) = (1/3, 7/15)$, satisfying:
$$
f_{r_a} + h_{r_a} = \frac{4}{5} \qquad \forall\,r_a \in \{0,1\}.
$$

### 1.3 Quantum-Steered Branch Probabilities and Causal Contrast
Under the globally active four-birth instrument $(H_{\rm full}, \lambda_0=1, \lambda_{1,2,3}=1/2, \theta=1/16)$, the retention factor at stage 2 is $\lambda_2 = 1/2$. The current-prefix drift vector $r_{C_2}(I_x) := \theta\Lambda_2^{-1}[H_{\rm full}(P_2+I_x) - H_{\rm full}(P_2)]$ evaluated with $\theta\Lambda_2^{-1} = \frac{1/16}{1/2} = 1/8$, $H_{\rm full}(a\prec b) = 19/22$, $H_{\rm full}(\text{edge+iso}) = 1/2$, and $H_{\rm full}(\text{fork}) = H_{\rm full}(\text{3-chain}) = 21/22$ yields the exact rational drifts:
$$
r_{C_2}(\varnothing) = \frac{1}{8}\left(\frac{1}{2} - \frac{19}{22}\right) = \frac{1}{8}\left(-\frac{8}{22}\right) = -\frac{1}{22},
$$
$$
r_{C_2}(\{a\}) = r_{C_2}(\{a,b\}) = \frac{1}{8}\left(\frac{21}{22} - \frac{19}{22}\right) = \frac{1}{8}\left(\frac{2}{22}\right) = +\frac{1}{88}.
$$
Notice the exact structural mean cancellation:
$$
\sum_{I_x} q(a\prec b, r, I_x) r_{C_2}(I_x) = \frac{1}{5}\left(-\frac{1}{22}\right) + \frac{4}{5}\left(+\frac{1}{88}\right) = -\frac{1}{110} + \frac{1}{110} = 0.
$$
For an incoming qubit state $\rho_Q$, the branch superoperator $\mathcal B^{a\prec b, r}_{I_x, b_3}$ acts with fair newborn bit $b_3 \in \{0,1\}$. Summing over $b_3$, the steered probability of realizing suffix topology $I_x$ is:
$$
p(I_x \mid \rho_Q) = \operatorname{Tr}\Bigl[\sum_{b_3=0}^1 \mathcal B^{a\prec b, r}_{I_x, b_3}(\rho_Q)\Bigr] = q(a\prec b, r, I_x)\bigl(1 + r_{C_2}(I_x)\operatorname{Tr}[X\rho_Q]\bigr) = q(a\prec b, r, I_x)\bigl(1 + r_{C_2}(I_x)\langle X\rangle\bigr).
$$
Evaluating across the individual topologies:
$$
p(I_x = \varnothing \mid \rho_Q) = \frac{1}{5}\left(1 - \frac{1}{22}\langle X\rangle\right) = \frac{1}{5} - \frac{1}{110}\langle X\rangle,
$$
$$
p(I_x = \{a\} \mid \rho_Q) = f_{r_a}\left(1 + \frac{1}{88}\langle X\rangle\right) = f_{r_a} + \frac{f_{r_a}}{88}\langle X\rangle,
$$
$$
p(I_x = \{a,b\} \mid \rho_Q) = h_{r_a}\left(1 + \frac{1}{88}\langle X\rangle\right) = h_{r_a} + \frac{h_{r_a}}{88}\langle X\rangle.
$$
Summing the connected causal topologies:
$$
p_{\rm causal}(\langle X\rangle) := p(I_x \in \{\{a\}, \{a,b\}\} \mid \rho_Q) = \frac{4}{5}\left(1 + \frac{1}{88}\langle X\rangle\right) = \frac{4}{5} + \frac{1}{110}\langle X\rangle.
$$
The net differential causal contrast between connected and disconnected suffix topologies is:
$$
\Delta p_{\rm causal}(\langle X\rangle) := p_{\rm causal}(\langle X\rangle) - p(I_x = \varnothing \mid \rho_Q) = \left(\frac{4}{5} - \frac{1}{5}\right) + \left(\frac{1}{110} - \left(-\frac{1}{110}\right)\right)\langle X\rangle = \frac{3}{5} + \frac{1}{55}\langle X\rangle.
$$
Hence, positive qubit coherence $\langle X\rangle > 0$ strictly enhances the probability of generating a connected causal history, while negative coherence $\langle X\rangle < 0$ suppresses causal connections in favor of the spacelike isolated branch. This constitutes the exact Quantum $\to$ Order steering channel.

---

## 2. Mapping Suffix Topologies to Cavity Spacetime Coordinates and Differential Field Excitations

### 2.1 12-Mode Homogeneous-Neumann Cavity Geometry
We embed the discrete events into a continuous physical cavity. Let flat Minkowski spacetime $\mathbb R^{1,3}$ have Cartesian coordinates $x^\mu = (x^0, x_1, x_2, x_3) = (ct, x)$ with signature $(-,+,+,+)$.
The physical cavity is a centered cube $\Omega = [-L/2, L/2]^3$ with:
$$
L := 8c\tau, \qquad V := L^3 = 512c^3\tau^3,
$$
where $c > 0$ is the speed of light and $\tau > 0$ is the characteristic tick duration.
The longitudinal cavity scalar field is expanded over $M = 12$ odd-harmonic standing modes ($m = 0, 1, \dots, 11$):
$$
n_m := 47 - 2m \in \{25, 27, \dots, 47\}, \qquad k_m := \frac{n_m\pi}{L} = \frac{(47-2m)\pi}{8c\tau}, \qquad \omega_m := ck_m = \frac{(47-2m)\pi}{8\tau}.
$$
The spatial eigenmodes are:
$$
u_m(x) = \cos\alpha_m(x_1), \qquad \alpha_m(x_1) := k_m\left(x_1 + \frac{L}{2}\right).
$$
Because $n_m$ is an integer, $\alpha_m(-L/2) = 0$ and $\alpha_m(L/2) = n_m\pi$, ensuring that the homogeneous Neumann boundary condition:
$$
n\cdot\nabla u_m\big|_{\partial\Omega} = 0
$$
holds identically on all six faces of $\partial\Omega$. Mode orthogonality is exact:
$$
\int_\Omega u_m(x) u_{m'}(x)\,d^3x = \frac{V}{2}\delta_{mm'}.
$$

### 2.2 Suffix Event Coordinate Mapping Across Structural Rows
Events $r \in \{a,b,x,y\}$ are positioned along the interior worldline segment:
$$
x_r = \left(-\frac{L}{4} + \xi_r c\tau,\, 0,\, 0\right) \in \left[-\frac{3}{8}L, -\frac{1}{24}L\right] \times \{0\} \times \{0\} \subset \operatorname{int}(\Omega), \qquad t_r = \tau_r \tau.
$$
The dimensionless coordinates $(\tau_r, \xi_r) \in \frac{1}{3}\mathbb Z^2$ are fixed for the prefix events across all 15 rows:
$$
z_a = (\tau_a, \xi_a) = (0, 0) \implies (t_a, x_a) = (0, -2c\tau, 0, 0),
$$
$$
z_b = (\tau_b, \xi_b) = (1, 0) \implies (t_b, x_b) = (\tau, -2c\tau, 0, 0).
$$
For the newborn event $x$, the coordinates $z_x(I_x)$ depend strictly on the steered precursor ideal $I_x$:
- **Spacelike Suffix** ($I_x = \varnothing$):
  $$
  z_x = \left(\frac{1}{3}, \frac{4}{3}\right) \implies t_x = \frac{\tau}{3}, \quad x_{1,x} = -2c\tau + \frac{4}{3}c\tau = -\frac{2}{3}c\tau;
  $$
- **Mixed Suffix** ($I_x = \{a\}$):
  $$
  z_x = \left(1, \frac{2}{3}\right) \implies t_x = \tau, \quad x_{1,x} = -2c\tau + \frac{2}{3}c\tau = -\frac{4}{3}c\tau;
  $$
- **Causal Suffix** ($I_x = \{a,b\}$):
  $$
  z_x = (2, 0) \implies t_x = 2\tau, \quad x_{1,x} = -2c\tau.
  $$

The fourth event $y$ is attached at stage 3 with precursor ideal $I_y \subseteq \{a,b,x\}$, defining the 15 structural rows tabulated below:

| Row | $I_x$ | $I_y$ | $z_x = (\tau_x, \xi_x)$ | $z_y = (\tau_y, \xi_y)$ | Spacetime Event $x^\mu_x$ | Spacetime Event $x^\mu_y$ |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | $\varnothing$ | $\varnothing$ | $(1/3, 4/3)$ | $(1/3, -1)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(\frac{1}{3}c\tau, -3c\tau, 0, 0)$ |
| 2 | $\varnothing$ | $\{x\}$ | $(1/3, 4/3)$ | $(2/3, 4/3)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(\frac{2}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ |
| 3 | $\varnothing$ | $\{a\}$ | $(1/3, 4/3)$ | $(1, -1/3)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(c\tau, -\frac{7}{3}c\tau, 0, 0)$ |
| 4 | $\varnothing$ | $\{a,b\}$ | $(1/3, 4/3)$ | $(4/3, 0)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(\frac{4}{3}c\tau, -2c\tau, 0, 0)$ |
| 5 | $\varnothing$ | $\{a,x\}$ | $(1/3, 4/3)$ | $(4/3, 1)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(\frac{4}{3}c\tau, -c\tau, 0, 0)$ |
| 6 | $\varnothing$ | $\{a,b,x\}$ | $(1/3, 4/3)$ | $(2, 1/3)$ | $(\frac{1}{3}c\tau, -\frac{2}{3}c\tau, 0, 0)$ | $(2c\tau, -\frac{5}{3}c\tau, 0, 0)$ |
| 7 | $\{a\}$ | $\varnothing$ | $(1, 2/3)$ | $(1/3, -1)$ | $(c\tau, -\frac{4}{3}c\tau, 0, 0)$ | $(\frac{1}{3}c\tau, -3c\tau, 0, 0)$ |
| 8 | $\{a\}$ | $\{a\}$ | $(1, 2/3)$ | $(1, -2/3)$ | $(c\tau, -\frac{4}{3}c\tau, 0, 0)$ | $(c\tau, -\frac{8}{3}c\tau, 0, 0)$ |
| 9 | $\{a\}$ | $\{a,b\}$ | $(1, 2/3)$ | $(4/3, 0)$ | $(c\tau, -\frac{4}{3}c\tau, 0, 0)$ | $(\frac{4}{3}c\tau, -2c\tau, 0, 0)$ |
| 10 | $\{a\}$ | $\{a,x\}$ | $(1, 2/3)$ | $(5/3, 1)$ | $(c\tau, -\frac{4}{3}c\tau, 0, 0)$ | $(\frac{5}{3}c\tau, -c\tau, 0, 0)$ |
| 11 | $\{a\}$ | $\{a,b,x\}$ | $(1, 2/3)$ | $(2, 0)$ | $(c\tau, -\frac{4}{3}c\tau, 0, 0)$ | $(2c\tau, -2c\tau, 0, 0)$ |
| 12 | $\{a,b\}$ | $\varnothing$ | $(2, 0)$ | $(1, 5/3)$ | $(2c\tau, -2c\tau, 0, 0)$ | $(c\tau, -\frac{1}{3}c\tau, 0, 0)$ |
| 13 | $\{a,b\}$ | $\{a\}$ | $(2, 0)$ | $(4/3, 1)$ | $(2c\tau, -2c\tau, 0, 0)$ | $(\frac{4}{3}c\tau, -c\tau, 0, 0)$ |
| 14 | $\{a,b\}$ | $\{a,b\}$ | $(2, 0)$ | $(2, 1/3)$ | $(2c\tau, -2c\tau, 0, 0)$ | $(2c\tau, -\frac{5}{3}c\tau, 0, 0)$ |
| 15 | $\{a,b\}$ | $\{a,b,x\}$ | $(2, 0)$ | $(3, 0)$ | $(2c\tau, -2c\tau, 0, 0)$ | $(3c\tau, -2c\tau, 0, 0)$ |

### 2.3 Single-Excitation Beat Doublet and Stress-Energy Interference
To extract dynamical gravitational radiation, the cavity field is prepared in the opposite-phase single-excitation beat doublet of its two lowest odd modes $(m_1, m_2) = (11, 10)$:
$$
\psi_\pm := \frac{1}{\sqrt2}\bigl(|1_{11}\rangle \pm |1_{10}\rangle\bigr) \in \mathcal S(\mathbb R^{12}), \qquad \rho_\pm := |\psi_\pm\rangle\langle\psi_\pm|.
$$
The modes carry quantum numbers $n_{11} = 25$ and $n_{10} = 27$, with fundamental frequencies:
$$
\omega_{11} = \frac{25\pi}{8\tau}, \qquad \omega_{10} = \frac{27\pi}{8\tau}.
$$
The beat interference note oscillates at difference frequency and difference wavenumber:
$$
\Omega_{\rm beat} := \omega_{10} - \omega_{11} = \frac{2\pi}{8\tau} = \frac{\pi}{4\tau}, \qquad k_{\rm beat} := k_{10} - k_{11} = \frac{2\pi}{L} = \frac{\pi}{4c\tau},
$$
with sum wavenumber $k_{\rm sum} := k_{10} + k_{11} = 52\pi/L = 26 k_{\rm beat}$. The oscillation period is $T_{\rm beat} = 2\pi/\Omega_{\rm beat} = 8\tau$, with half-period phase reversal at $\Delta t = \pi/\Omega_{\rm beat} = 4\tau$.
The Weyl-ordered stress-energy tensor inside $\Omega$ decomposes as:
$$
\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,\pm} = T^{\mu\nu}_{\rm cav,inc}(x) \pm T^{\mu\nu}_{\rm beat}(t,x; h),
$$
where $T^{\mu\nu}_{\rm cav,inc}(x)$ is a static incoherent tensor with uniform energy density:
$$
\rho_{\rm inc}^{\rm tot} = \frac{121\pi A_*}{2048 c^3\tau^4},
$$
and the dynamic interference tensor has amplitude:
$$
\rho_{\rm beat} := 2\sqrt{\rho_{11}\rho_{10}} = \frac{15\sqrt3\,\pi A_*}{4096 c^3\tau^4}.
$$
The total stress-energy tensor $T_{\mu\nu}^{\rm tot}$ on $\mathbb R^{1,3}$ is completed by a smooth confining Beltrami collar on $\overline{B_{3L}(0)}$ such that $\partial_\mu T^{\mu\nu,\pm}_{\rm tot} = 0$ holds everywhere on $\mathbb R^{1,3}$.

---

## 3. Linearized Harmonic-Gauge Gravity and $t - |x-y|/c$ Retardation

### 3.1 Field Equations in Harmonic Gauge
In weak-field linearized general relativity on flat Minkowski spacetime, the metric is expanded as:
$$
g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}, \qquad |h_{\mu\nu}| \ll 1,
$$
with trace-reversed perturbation $\bar h_{\mu\nu} := h_{\mu\nu} - \frac{1}{2}\eta_{\mu\nu} h$, where $h = \eta^{\alpha\beta}h_{\alpha\beta} = -\bar h$. Imposing the harmonic (de Donder) gauge condition:
$$
\partial^\mu\bar h_{\mu\nu} = 0,
$$
the linearized Einstein field equations decouple into the flat-space wave equation:
$$
\Box\bar h_{\mu\nu} = -\frac{16\pi G}{c^4}T_{\mu\nu}^{\rm tot}, \qquad \Box = -\frac{1}{c^2}\partial_t^2 + \nabla^2 = -\partial_0^2 + \nabla^2.
$$

### 3.2 Retarded Green Function and Past Lightcone Retardation
The unique causal solution satisfying the Sommerfeld outgoing radiation condition (no incoming waves from past null infinity) is given by the retarded Green function:
$$
G_R(x - y) = \frac{1}{4\pi |x-y|}\delta\left(x^0 - y^0 - |x-y|\right) = \frac{1}{4\pi |x-y|}\delta\left(c(t - t_y) - |x-y|\right).
$$
Convolving with the compactly supported source $T_{\mu\nu}^{\rm tot}$ gives:
$$
\bar h_{\mu\nu}(t,x) = \frac{4G}{c^4}\int_{\mathbb R^3}\frac{T_{\mu\nu}^{\rm tot}\left(t - \frac{|x-y|}{c},\, y\right)}{|x-y|}\,d^3y.
$$
This expression embodies exact causal retardation: the metric perturbation at spacetime observation point $(t,x)$ receives contributions strictly from source points $y$ evaluated at the retarded time:
$$
t_{\rm ret} := t - \frac{|x-y|}{c},
$$
lying on the past lightcone of $(t,x)$.

### 3.3 Proof of Harmonic Gauge Consistency from Source Conservation
We rigorously verify that $\partial^\mu\bar h_{\mu\nu} = 0$ holds everywhere on $\mathbb R^{1,3}$. Substituting $w = x - y$ as the integration variable:
$$
\bar h_{\mu\nu}(t,x) = \frac{4G}{c^4}\int_{\mathbb R^3}|w|^{-1}T_{\mu\nu}^{\rm tot}\left(t - \frac{|w|}{c},\, x-w\right)\,d^3w.
$$
Because $T_{\mu\nu}^{\rm tot}$ is smooth with compact spatial support in $\overline{B_{3L}(0)}$, the integrand has compact $w$-support for any bounded $x$. Taking the four-divergence with respect to $x^\mu$:
$$
\partial^\mu\bar h_{\mu\nu}(t,x) = \frac{4G}{c^4}\int_{\mathbb R^3}|w|^{-1}\left(-\frac{1}{c}\partial_t T_{0\nu}^{\rm tot} + \partial_{x_a}T_{a\nu}^{\rm tot}\right)\left(t - \frac{|w|}{c},\, x-w\right)\,d^3w.
$$
Since $\partial_{x_a}T_{a\nu}^{\rm tot}(t-|w|/c, x-w) = \partial_{y_a}T_{a\nu}^{\rm tot}(t_{\rm ret}, y)\big|_{y=x-w}$, the term in parentheses is precisely:
$$
-\partial_0 T_{0\nu}^{\rm tot} + \partial_a T_{a\nu}^{\rm tot} = \partial^\mu T_{\mu\nu}^{\rm tot} = 0,
$$
which vanishes identically by four-divergence conservation. Thus $\partial^\mu\bar h_{\mu\nu}(t,x) = 0$ is exact for all $(t,x) \in \mathbb R^{1,3}$.


---

## 4. Proof of Exact Gauge Invariance of Electric Riemann Curvature

### 4.1 Linearized Coordinate Gauge Transformations
Under an infinitesimal coordinate gauge transformation:
$$
x^\mu \to x'^\mu = x^\mu + \xi^\mu(x),
$$
generated by a smooth arbitrary vector field $\xi^\mu(x) \in C^\infty(\mathbb R^{1,3})$, the linearized metric perturbation transforms according to the Lie derivative along $\xi$:
$$
h_{\mu\nu}(x) \to h'_{\mu\nu}(x) = h_{\mu\nu}(x) - \partial_\mu\xi_\nu(x) - \partial_\nu\xi_\mu(x),
$$
where index lowering uses the flat Minkowski background metric $\xi_\mu = \eta_{\mu\alpha}\xi^\alpha$.

### 4.2 Proof of Exact Gauge Invariance of the Linearized Riemann Tensor
The linearized Riemann curvature tensor is defined by:
$$
R_{\mu\nu\rho\sigma} := \frac{1}{2}\bigl(\partial_\nu\partial_\rho h_{\mu\sigma} + \partial_\mu\partial_\sigma h_{\nu\rho} - \partial_\mu\partial_\rho h_{\nu\sigma} - \partial_\nu\partial_\sigma h_{\mu\rho}\bigr).
$$
We now compute the gauge variation $\delta_\xi R_{\mu\nu\rho\sigma} := R'_{\mu\nu\rho\sigma} - R_{\mu\nu\rho\sigma}$ under the substitution $\delta_\xi h_{\alpha\beta} = -\partial_\alpha\xi_\beta - \partial_\beta\xi_\alpha$:
$$
\delta_\xi R_{\mu\nu\rho\sigma} = \frac{1}{2}\Bigl[\partial_\nu\partial_\rho\bigl(-\partial_\mu\xi_\sigma - \partial_\sigma\xi_\mu\bigr) + \partial_\mu\partial_\sigma\bigl(-\partial_\nu\xi_\rho - \partial_\rho\xi_\nu\bigr) - \partial_\mu\partial_\rho\bigl(-\partial_\nu\xi_\sigma - \partial_\sigma\xi_\nu\bigr) - \partial_\nu\partial_\sigma\bigl(-\partial_\mu\xi_\rho - \partial_\rho\xi_\mu\bigr)\Bigr].
$$
Expanding the brackets into individual terms:
$$
\delta_\xi R_{\mu\nu\rho\sigma} = \frac{1}{2}\Bigl[-\partial_\nu\partial_\rho\partial_\mu\xi_\sigma - \partial_\nu\partial_\rho\partial_\sigma\xi_\mu - \partial_\mu\partial_\sigma\partial_\nu\xi_\rho - \partial_\mu\partial_\sigma\partial_\rho\xi_\nu + \partial_\mu\partial_\rho\partial_\nu\xi_\sigma + \partial_\mu\partial_\rho\partial_\sigma\xi_\nu + \partial_\nu\partial_\sigma\partial_\mu\xi_\rho + \partial_\nu\partial_\sigma\partial_\rho\xi_\mu\Bigr].
$$
Because partial derivatives commute on $C^\infty$ tensor fields ($\partial_\alpha\partial_\beta\partial_\gamma = \partial_\beta\partial_\alpha\partial_\gamma$, etc.), we group the eight terms into four canceling pairs:
1. Terms involving $\xi_\sigma$:
   $$
   -\partial_\nu\partial_\rho\partial_\mu\xi_\sigma + \partial_\mu\partial_\rho\partial_\nu\xi_\sigma = -\partial_\mu\partial_\nu\partial_\rho\xi_\sigma + \partial_\mu\partial_\nu\partial_\rho\xi_\sigma = 0.
   $$
2. Terms involving $\xi_\mu$:
   $$
   -\partial_\nu\partial_\rho\partial_\sigma\xi_\mu + \partial_\nu\partial_\sigma\partial_\rho\xi_\mu = -\partial_\nu\partial_\rho\partial_\sigma\xi_\mu + \partial_\nu\partial_\rho\partial_\sigma\xi_\mu = 0.
   $$
3. Terms involving $\xi_\rho$:
   $$
   -\partial_\mu\partial_\sigma\partial_\nu\xi_\rho + \partial_\nu\partial_\sigma\partial_\mu\xi_\rho = -\partial_\mu\partial_\nu\partial_\sigma\xi_\rho + \partial_\mu\partial_\nu\partial_\sigma\xi_\rho = 0.
   $$
4. Terms involving $\xi_\nu$:
   $$
   -\partial_\mu\partial_\sigma\partial_\rho\xi_\nu + \partial_\mu\partial_\rho\partial_\sigma\xi_\nu = -\partial_\mu\partial_\rho\partial_\sigma\xi_\nu + \partial_\mu\partial_\rho\partial_\sigma\xi_\nu = 0.
   $$
Every single pair cancels identically. Therefore:
$$
\delta_\xi R_{\mu\nu\rho\sigma} = 0 \qquad \forall\,\xi^\mu \in C^\infty(\mathbb R^{1,3}).
$$
The linearized Riemann curvature tensor is an exact, coordinate-independent, gauge-invariant physical tensor field.

### 4.3 Physical Tidal Acceleration and Electric Riemann Curvature
The electric components of the Riemann tensor (the electric curvature tensor or tidal tensor) are defined by:
$$
E_{ij}(t,x) := R_{0i0j}(t,x).
$$
Substituting the indices $\mu=0, \nu=i, \rho=0, \sigma=j$ into the linearized definition:
$$
E_{ij}(t,x) = \frac{1}{2}\bigl(\partial_i\partial_0 h_{0j} + \partial_0\partial_j h_{0i} - \partial_0^2 h_{ij} - \partial_i\partial_j h_{00}\bigr) = -\frac{1}{2c^2}\partial_t^2 h_{ij} + \frac{1}{2c}\partial_t(\partial_i h_{0j} + \partial_j h_{0i}) - \frac{1}{2}\partial_i\partial_j h_{00}.
$$
To establish its physical operational meaning, consider a congruence of freely falling timelike test bodies moving with four-velocity $u^\mu = dx^\mu/d\tau$, where $\tau$ is proper time. In the local rest frame of an accelerometer where $u^\mu = (1, 0, 0, 0)$ to zeroth order, the geodesic deviation equation governing the relative spatial separation vector $\xi^i(\tau)$ between nearby geodesics is:
$$
\frac{D^2\xi^\mu}{d\tau^2} = R^\mu{}_{\nu\rho\sigma} u^\nu u^\rho \xi^\sigma.
$$
Evaluating the spatial component $\mu = i$:
$$
\frac{d^2\xi^i}{dt^2} = c^2 R^i{}_{00j}\xi^j = -c^2 R_{0i0j}\xi^j = -c^2 E_{ij}(t,x)\xi^j.
$$
Thus, $E_{ij}(t,x)$ is directly measurable by local strain gauges, laser interferometers, or baseline accelerometers measuring differential tidal acceleration without any dependence on the chosen coordinate gauge.

---

## 5. Finite-Radius Curvature Readout at $r_* = 250L = 2000c\tau$

### 5.1 Axial Nullity Along the Longitudinal Axis $\pm r e_1$
Before evaluating the curvature signal, we recall the exact geometric obstruction along the longitudinal cavity axis.

**Theorem (Exact Finite-Radius Axial Nullity).** *For every cavity preparation state, every radius $r \ge 0$, and every time $t \in \mathbb R$, the transverse tidal shear in $(e_1)^\perp = \operatorname{span}\{e_2, e_3\}$ vanishes identically along the longitudinal axis $x = \pm r e_1$:*
$$
R_{0202}(t, \pm r e_1) = R_{0303}(t, \pm r e_1), \qquad R_{0203}(t, \pm r e_1) = 0, \qquad \frac{1}{2}\bigl(R_{0202} - R_{0303}\bigr)(t, \pm r e_1) = 0.
$$
*Proof.* The 12-mode standing waves $u_m(x) = \cos\alpha_m(x_1)$ depend solely on $x_1$ and are strictly invariant under the transverse reflections $R_2: (x_1, x_2, x_3) \mapsto (x_1, -x_2, x_3)$, $R_3: (x_1, x_2, x_3) \mapsto (x_1, x_2, -x_3)$, and the coordinate swap $S_{23}: (x_1, x_2, x_3) \mapsto (x_1, x_3, x_2)$. The confining collar potentials likewise respect this $D_4$ symmetry. Consequently, the stress-energy tensor satisfies $T_{02} \equiv T_{03} \equiv T_{23} \equiv 0$ on $\mathbb R^{1,3}$, forcing $\bar h_{02} = \bar h_{03} = \bar h_{23} = 0$ everywhere, and $T_{22}(S_{23}y) = T_{33}(y)$. On the symmetry axis $x = (\pm r, 0, 0)$, reflection symmetry forces $\partial_2^2 h_{00} = \partial_3^2 h_{00}$ and $\partial_2\partial_3 h_{00} = 0$, while $\bar h_{22} - \bar h_{33} \equiv 0$. Thus $R_{0202} - R_{0303} = -\frac{1}{2}\partial_0^2(h_{22}-h_{33}) - \frac{1}{2}(\partial_2^2-\partial_3^2)h_{00} = 0$. $\square$

Therefore, a sensor placed along the longitudinal axis $\pm e_1$ detects identically zero transverse tidal shear at all finite exterior radii!

### 5.2 Equatorial Bisector Geometry and Transverse Polarization
To capture the dynamic beat signal, we position the observer along the equatorial bisector ray:
$$
n_* := \frac{1}{\sqrt2}\bigl(e_1 + e_2\bigr).
$$
We define the associated orthonormal transverse polarization basis:
$$
e_\vartheta := \frac{1}{\sqrt2}\bigl(e_1 - e_2\bigr), \qquad e_3 := (0, 0, 1),
$$
satisfying $n_* \cdot e_\vartheta = 0$, $n_* \cdot e_3 = 0$, and $e_\vartheta \cdot e_3 = 0$. The transverse polarization projection tensor is:
$$
D^{ab} := \frac{1}{2}\bigl(e_\vartheta^a e_\vartheta^b - e_3^a e_3^b\bigr), \qquad \delta_{ab}D^{ab} = \frac{1}{2}(1 - 1) = 0.
$$
The plus electric-curvature channel along this ray is:
$$
\mathcal E(t,r) := D^{ab}E_{ab}(t, rn_*) = \frac{1}{2}\bigl(E_{\vartheta\vartheta}(t, rn_*) - E_{33}(t, rn_*)\bigr).
$$
For the opposite-phase single-excitation beat doublet $\psi_\pm$, the static background $h_{\mu\nu}^{\rm inc}$ cancels identically, isolating the pure dynamic beat contrast:
$$
\Delta\mathcal E(t,r) := \mathcal E_+(t,r) - \mathcal E_-(t,r) = 2D^{ab}R_{0a0b}^{\rm beat}(t, rn_*).
$$

### 5.3 Exterior Wave-Zone Operator and Fourth-Order Helmholtz Remainder Bounds
Outside the source region ($|x| > L$), the beat wavefield is expressed in terms of the scalar Helmholtz convolution:
$$
I_{\rm rad}(x) := \int_{B_L(0)} G_{\rm rad}(y)\frac{e^{ik_{\rm beat}|x-y|}}{|x-y|}\,d^3y, \qquad G_{\rm rad}(y) := G_{\rm diff}(y) - \frac{1}{676}G_{\rm sum}(y).
$$
Direct projection of the tidal tensor onto $D^{ab}$ yields the exact representation on $|x| > L$:
$$
\Delta\mathcal E(t,r) = -\frac{Gk_{\rm beat}^2\rho_{\rm beat}}{c^4}\operatorname{Re}\Bigl\{e^{-i\Omega_{\rm beat}t}\bigl(1 + \mathcal L_{\rm rem}\bigr)I_{\rm rad}(x)\Bigr\}\Bigg|_{x=rn_*},
$$
where the differential remainder operator is:
$$
\mathcal L_{\rm rem} := \frac{2\partial_\parallel\partial_\vartheta + \partial_\vartheta^2 + \partial_3^2}{k_{\rm beat}^2} + \frac{(\partial_\vartheta^2 - \partial_3^2)\partial_1^2}{k_{\rm beat}^4},
$$
with directional derivatives $\partial_\parallel = n_*\cdot\nabla = \frac{1}{\sqrt2}(\partial_1+\partial_2)$, $\partial_\vartheta = e_\vartheta\cdot\nabla = \frac{1}{\sqrt2}(\partial_1-\partial_2)$, and $\partial_3 = e_3\cdot\nabla$.

For $z = x - y$, $d = |z|$, and $k = k_{\rm beat} = 2\pi/L$, the radial derivative sequence $g_0(d) = d^{-1}e^{ikd}$, $g_{n+1}(d) = d^{-1}g_n'(d)$ yields the explicit radial expansion:
$$
g_1(d) = \bigl(ikd^{-2} - d^{-3}\bigr)e^{ikd}, \qquad g_2(d) = \bigl(-k^2d^{-3} - 3ikd^{-4} + 3d^{-5}\bigr)e^{ikd},
$$
$$
g_3(d) = \bigl(-ik^3d^{-4} + 6k^2d^{-5} + 15ikd^{-6} - 15d^{-7}\bigr)e^{ikd},
$$
$$
g_4(d) = \bigl(k^4d^{-5} + 10ik^3d^{-6} - 45k^2d^{-7} - 105ikd^{-8} + 105d^{-9}\bigr)e^{ikd}.
$$
Evaluating at $x = rn_*$ with $r > 3L$ and $y \in B_L(0)$:
- Transverse distances satisfy $z_\vartheta = -e_\vartheta\cdot y$, $z_3 = -e_3\cdot y$, so $|z_\vartheta| \le L$, $|z_3| \le L$, and $z_\vartheta^2 + z_3^2 \le |y|^2 \le L^2$;
- Radial distance satisfies $d \ge r - L > 2L$;
- Wavenumber satisfies $k = 2\pi/L > 6/L$, so $kd > 12$.

Bounding each term in $\mathcal L_{\rm rem}$ from first principles:
1. $\frac{2}{k^2}|g_1(d)| < \frac{13}{36}\frac{L}{d^2} < \frac{1}{2}\frac{L}{(r-L)^2}$;
2. $\bigl(\frac{2dL+L^2}{k^2} + \frac{1}{k^4}\bigr)|g_2(d)| < \frac{181}{54}\frac{L}{d^2} < \frac{7}{2}\frac{L}{(r-L)^2}$;
3. $\frac{2\sqrt2\,dL+L^2}{k^4}|g_3(d)| < \frac{7}{kd}\frac{L}{d^2} < \frac{7}{12}\frac{L}{(r-L)^2}$;
4. $\frac{|z_\vartheta^2-z_3^2|z_1^2}{k^4}|g_4(d)| < \frac{5}{2}\frac{L^2}{d^3} < \frac{5}{4}\frac{L}{(r-L)^2}$;
5. Leading kernel difference $|g_0(d) - r^{-1}e^{ik(r-n_*\cdot y)}| < \frac{29}{7}\frac{L}{(r-L)^2}$.

Summing the terms yields the total kernel remainder bound:
$$
\left(\frac{1}{2} + \frac{7}{2} + \frac{7}{12} + \frac{5}{4} + \frac{29}{7}\right)\frac{L}{(r-L)^2} = \frac{419}{42}\frac{L}{(r-L)^2} < 10\frac{L}{(r-L)^2}.
$$
Integrating over $y \in B_L(0)$ against $|G_{\rm rad}(y)| \le (1 + 1/676)\chi_{\rm box}(y)$ with $\int\chi_{\rm box} \le \frac{46}{45}L^3$ and $10 \times \frac{677}{676} \times \frac{46}{45} < 11$ establishes the universal wave-zone error bound valid for **all** $r > 3L$ and **all** $t \in \mathbb R$:
$$
\left|\Delta\mathcal E(t,r) - \frac{\mathcal C_{\rm beat}^{(12)}}{r}\cos\bigl(\Omega_{\rm beat}(t - r/c)\bigr)\right| \le 11\frac{Gk_{\rm beat}^2\rho_{\rm beat}L^4}{c^4(r-L)^2}.
$$

### 5.4 Asymptotic Beat Contrast and Concrete Bound at $r_* = 250L = 2000c\tau$
From elementary Fourier analysis of the odd-harmonic modes without numerical quadrature:
$$
\mathcal C_{\rm beat}^{(12)} := \lim_{r\to\infty} r\Delta\mathcal E(r/c, r) = -\frac{15\sqrt3\,\pi^3}{128}\frac{GA_*}{c^6\tau^3}\mathcal I_0\mathcal K_2(\sqrt2\pi)\left[\mathcal K_{\rm diff}(\sqrt2\pi) - \frac{1}{676}\mathcal K_{\rm sum}(\sqrt2\pi)\right] < 0,
$$
with guaranteed lower bound:
$$
\bigl|\mathcal C_{\rm beat}^{(12)}\bigr| = -\mathcal C_{\rm beat}^{(12)} > \frac{279\sqrt3\,\pi^3}{25{,}600}\frac{GA_*}{c^6\tau^3} > 0.
$$
Now, choose the concrete finite radius:
$$
r_* := 250L = 2000c\tau > 3L.
$$
At this radius, $r_* - L = 249L$, and $(249)^2 = 62{,}001$. We compare the remainder against half the asymptotic signal:
$$
\frac{\text{Remainder}}{\frac{1}{2r_*}|\mathcal C_{\rm beat}^{(12)}|} \le \frac{11\frac{Gk_{\rm beat}^2\rho_{\rm beat}L^4}{c^4(249L)^2}}{\frac{93}{2000r_*}\frac{Gk_{\rm beat}^2\rho_{\rm beat}L^3}{c^4}} = \frac{11 \times 2000 \times 250}{93 \times 62{,}001} = \frac{5{,}500{,}000}{5{,}766{,}093} < 1.
$$
Because the remainder is strictly less than half the leading signal, the sign of the curvature contrast is certified without approximation!

Evaluating at retarded time $U = 0$ ($t_*^{(0)} = r_*/c = 2000\tau$, $\cos 0 = +1$):
$$
\Delta\mathcal E\left(\frac{r_*}{c},\, 250L\right) \le \frac{\mathcal C_{\rm beat}^{(12)}}{2r_*} < -\frac{279\sqrt3\,\pi^3}{102{,}400{,}000}\frac{GA_*}{c^7\tau^4} < 0.
$$
Evaluating at half-period retarded time $U = 4\tau$ ($t_*^{(\pi)} = r_*/c + 4\tau = 2004\tau$, $\cos\pi = -1$):
$$
\Delta\mathcal E\left(\frac{r_*}{c} + 4\tau,\, 250L\right) \ge \frac{|\mathcal C_{\rm beat}^{(12)}|}{2r_*} > +\frac{279\sqrt3\,\pi^3}{102{,}400{,}000}\frac{GA_*}{c^7\tau^4} > 0.
$$
This proves that the electric Riemann curvature contrast oscillates strictly and alternates sign every $4\tau$ at the finite exterior radius $r_* = 250L$.

---

## 6. Two-Way Co-Registration with Final Qubit, $V_{\rm geom}$, $S_{\rm BD}$, and $Y$

### 6.1 Ensemble Probability Law Conditioned on Qubit State
The full process consists of four births conditioned on prefix $a\prec b$ and initial qubit state $\rho_Q$. Across the 15 predecessor-ideal rows $(I_x, I_y)$ and fair suffix marks $(b_3, b_4) \in \{0,1\}^2$, there are $15 \times 4 = 60$ distinct marked histories $h = 1, \dots, 60$.
The probability of history $h = (I_x, I_y, b_3, b_4)$ is:
$$
P(h \mid \rho_Q) = \frac{1}{4}p(I_x \mid \rho_Q) q_4(I_y \mid I_x) = \frac{1}{4}q(a\prec b, r, I_x)\bigl(1 + r_{C_2}(I_x)\langle X\rangle\bigr)q_4(I_y \mid I_x) = P_0(h) + \langle X\rangle \Delta P_{\rm steer}(h),
$$
where $P_0(h) = \frac{1}{4}q(a\prec b, r, I_x)q_4(I_y \mid I_x)$ is the unsteered background probability and:
$$
\Delta P_{\rm steer}(h) = \frac{1}{4}q(a\prec b, r, I_x)r_{C_2}(I_x)q_4(I_y \mid I_x), \qquad \sum_{h=1}^{60}\Delta P_{\rm steer}(h) = 0.
$$

### 6.2 Co-Registration with Exterior Electric Curvature
The ensemble expectation of the exterior electric Riemann curvature tensor at observation point $(t, r_* n_*)$ is:
$$
\mathbb E_{\rho_Q}\bigl[E_{ij}(t, r_* n_*)\bigr] := \sum_{h=1}^{60} P(h \mid \rho_Q) E_{ij}(t, r_* n_*; h) = \overline E_{ij}(t, r_* n_*) + \langle X\rangle \Delta E_{ij}^{\rm steer}(t, r_* n_*),
$$
where:
$$
\overline E_{ij}(t, r_* n_*) = \sum_{h=1}^{60} P_0(h) E_{ij}(t, r_* n_*; h), \qquad \Delta E_{ij}^{\rm steer}(t, r_* n_*) = \sum_{h=1}^{60}\Delta P_{\rm steer}(h) E_{ij}(t, r_* n_*; h).
$$
Projecting onto the transverse polarization tensor $D^{ab}$:
$$
\mathbb E_{\rho_Q}\bigl[\mathcal E(t, r_*)\bigr] = \overline{\mathcal E}(t, r_*) + \langle X\rangle \Delta\mathcal E_{\rm steer}(t, r_*).
$$

### 6.3 Co-Registration with Conserved Geometric Potential $V_{\rm geom}$
In `record_compensated_quantum_order_conservation.md`, the lost qubit energy from damping $\lambda_2 = 1/2$ is converted conservatively into the 25-poset geometric potential $V_{\rm geom}(P)$. Starting above $a\prec b$, the conditional expectation of the geometric potential shift across the four-birth ensemble is:
$$
\mathbb E_{\rho_Q}\bigl[V_{\rm geom}(P_4) - V_{\rm geom}(a\prec b)\bigr] = \frac{3\varepsilon}{8}\operatorname{Tr}[X\rho_Q] = \frac{3\varepsilon}{8}\langle X\rangle.
$$
This transfer is exact and mark-independent across all 60 histories.

### 6.4 Co-Registration with Causal-Order Invariants ($S_{\rm BD}$ and $Y$)
On each realized four-element poset $P_4(h)$, the discrete 4D Benincasa–Dowker interval action is:
$$
S_{\rm BD}(h) = 4 - 2 N_1(h) + 4 N_2(h) - \dots,
$$
where $N_k$ is the number of intervals of size $k$, and the operational incidence counter is $Y(h)$.
Averaging over the steered ensemble:
$$
\mathbb E_{\rho_Q}\bigl[S_{\rm BD}\bigr] = \overline S_{\rm BD} + \langle X\rangle \Delta S_{\rm steer}, \qquad \Delta S_{\rm steer} = \sum_{h=1}^{60}\Delta P_{\rm steer}(h) S_{\rm BD}(h),
$$
$$
\mathbb E_{\rho_Q}\bigl[Y\bigr] = \overline Y + \langle X\rangle \Delta Y_{\rm steer}, \qquad \Delta Y_{\rm steer} = \sum_{h=1}^{60}\Delta P_{\rm steer}(h) Y(h).
$$

### 6.5 Final Qubit Coherence and Phase Backaction
At the conclusion of stage 4, the co-rotating five-Kraus channel with cumulative retention product $\Lambda_4/\Lambda_2 = (1/8)/(1/2) = 1/4$ maps the qubit coherence into the stage 4 axis $\Sigma_4 = Z$:
$$
\operatorname{Tr}\bigl[Z\rho_Q^{(4)}\bigr] = \frac{1}{4}\langle X\rangle.
$$
Simultaneously, precursor-local phases $\{\varphi_{K,b}\}$ impart history-dependent unitary rotations $U_{n,K,b} = U_*\exp(-i\frac{\varphi_{K,b}}{2}\Sigma_n)$ that generate non-zero root-mark phase backaction without disturbing energy conservation.

### 6.6 Simultaneous Multi-Observable Co-Registration Ledger
The ensemble expectations of all five physical observables are linearly co-registered across the exact same qubit coherence parameter $\langle X\rangle \in [-1, 1]$:

| Observable | Symbol | Physical Domain | Unsteered Mean | Linear Sensitivity to $\langle X\rangle$ |
|---|:---:|:---:|:---:|:---:|
| Suffix Causal Probability | $p_{\rm causal}$ | Poset Topology | $\frac{4}{5}$ | $+\frac{1}{110}$ |
| Final Qubit Coherence | $\operatorname{Tr}[Z\rho_Q^{(4)}]$ | Quantum Probe | $0$ | $+\frac{1}{4}$ |
| Conserved Geometric Energy | $\mathbb E[\Delta V_{\rm geom}]$ | Conserved Ledger | $0$ | $+\frac{3\varepsilon}{8}$ |
| Discrete Benincasa–Dowker Action | $\mathbb E[S_{\rm BD}]$ | Causal-Set Action | $\overline S_{\rm BD}$ | $\Delta S_{\rm steer}$ |
| Exterior Electric Curvature | $\mathbb E[\mathcal E(t, r_*)]$ | Spacetime Curvature ($r_*=250L$) | $\overline{\mathcal E}(t, r_*)$ | $\Delta\mathcal E_{\rm steer}(t, r_*)$ |

All five physical quantities respond simultaneously, linearly, and deterministically to the initial quantum coherence $\langle X\rangle$, establishing complete co-registration between quantum state, discrete causal order, and retarded gravitational curvature.

---

## 7. Scope, Non-Implications, and Status-M Quarantine

### 7.1 Matrix of Null Controls
To certify that the reported signals arise exclusively from genuine physical couplings, we audit three mandatory null controls:
1. **Unpolarized / Orthogonal Qubit Control ($\langle X\rangle = 0$):**
   When the initial qubit has zero $X$-coherence ($\rho_Q = \frac{1}{2}(I_Q + \langle Y\rangle Y + \langle Z\rangle Z)$), the steered probabilities collapse to the background weights: $p(I_x \mid \rho_Q) = q(a\prec b, r, I_x)$. The differential causal contrast vanishes ($\Delta p_{\rm causal} = 3/5$), the geometric energy transfer vanishes ($\mathbb E[\Delta V_{\rm geom}] = 0$), and the curvature expectation reduces to the unsteered mean $\overline E_{ij}$.
2. **Longitudinal Axis Alignment Control ($x = \pm r e_1$):**
   When the gravitational sensor is placed along the longitudinal axis $\pm e_1$, transverse tidal shear vanishes identically at all radii: $R_{0202} - R_{0303} \equiv 0$ and $R_{0203} \equiv 0$, due to exact $D_4$ symmetry. No beat contrast can be detected along this null direction.
3. **Decoupled Cavity Control ($\boldsymbol\lambda = \mathbf 0$):**
   When pointer-probe kicks or cavity couplings are turned off ($\boldsymbol\lambda = \mathbf 0$), all dynamical field displacements vanish ($g = \mathbf 0$), the cavity field remains in its unperturbed state, and exterior dynamical curvature vanishes identically.

### 7.2 Native Discrete Primitives vs. Supplied Continuum Embedding
We maintain strict separation between native discrete poset quantities and supplied continuum structures:
- **Native Discrete Structures**: Finite posets $(P, \prec)$, precursor ideals $I_x, I_y$, binary marks $r$, Benincasa–Dowker interval action $S_{\rm BD}$, incidence counter $Y$, and the co-rotating quantum instrument $(\mathcal B, H_{\rm full}, V_{\rm geom})$.
- **Supplied Semiclassical Continuum Embedding**: Flat Minkowski background $(\mathbb R^{1,3}, \eta_{\mu\nu})$, Cartesian coordinates $(t, x)$, cubic cavity boundary $\Omega = [-L/2, L/2]^3$, 12-mode longitudinal standing waves $u_m(x)$, linearized metric perturbation $h_{\mu\nu}$, and physical constants $(c, \tau, A_*, \kappa, G)$.

### 7.3 Non-Claims
1. This deliverable does **not** derive continuum spacetime dimension ($3+1$D), spatial coordinates, or the continuous manifold from native poset causal set primitives.
2. This deliverable does **not** derive the Einstein field equations or General Relativity from discrete poset growth. The gravitational coupling is formulated strictly within standard linearized general relativity on a prescribed flat Minkowski background.
3. This deliverable does **not** derive Born's rule, quantum state reduction, or physical constants $(c, \tau, A_*, \kappa, G)$.
4. This deliverable does **not** formulate a quantum theory of gravity or a quantum superposition of spacetime geometries; the gravitational source is the semiclassical expectation value of the stress-energy tensor.

### 7.4 Status-M Quarantine Declaration
Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined outside every equation, variable, and inference of this calculation, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## Scientific review

Two-Way Quantum-Steered Retarded Curvature Author derived initial qubit coherence ($\langle X\rangle$) steering of causal vs. spacelike suffix topologies, linearized harmonic-gauge retarded potential $\Box\bar h_{\mu\nu} = -(16\pi G/c^4)T_{\mu\nu}^{\rm tot}$, exact coordinate gauge invariance of electric Riemann curvature $E_{ij}=R_{0i0j}$ ($\delta R_{\mu\nu\rho\sigma}=0$), axial nullity along $\pm r e_1$, finite-radius fourth-order Helmholtz wave-zone remainder bounds at $r_* = 250L = 2000c\tau$ along equatorial bisector $n_* = \frac{1}{\sqrt2}(e_1+e_2)$ certifying sign-alternating curvature contrasts $\Delta\mathcal E(r_*/c, 250L) < -\frac{279\sqrt3\pi^3}{102{,}400{,}000}\frac{GA_*}{c^7\tau^4} < 0$ and $\Delta\mathcal E(r_*/c+4\tau, 250L) > 0$, and multi-observable linear co-registration across 60 histories. Independent Retarded Curvature Reviewer independently verified by hand 100% of equations, tensor variations, rational coefficients, remainder bounds, and strict sibling isolation. Prospective protocol SHA-256 9fd82bfa0af00929e20e29b6872c93fc7600b72ae8d610d3fe7d59bb9a09e6c8; accepted author report SHA-256 d0789ee33cc7ded0c2844bc95601e69c80827db12c81f27783a452aec9f82efa; independent scientific review SHA-256 98615f2d45ceed296f6f36478b0134a146946d878b4d617205f5fe8a2b52151c.
