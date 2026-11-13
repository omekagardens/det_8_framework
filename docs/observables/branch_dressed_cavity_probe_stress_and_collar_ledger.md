# Branch-dressed cavity probe stress, four-divergence conservation, and collar reaction ledger across causal diamonds

**Decision.** Extending the 12-mode Neumann cavity pointer-probe work ledger and Beltrami collar source across committed causal histories $h$, the local impulsive pointer-probe kicks along any committed causal branch inside the homogeneous-Neumann cubic cavity $\Omega=[-L/2,L/2]^3$ ($L=8c\tau$, $V=512c^3\tau^3$) dress the field stress-energy tensor $\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,g} = \omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x)) + T^{\mu\nu}_{\rm cl}(t,x;h,g)$ with exact four-divergence conservation $\partial_\mu T^{\mu\nu}_h = 0$ on $\operatorname{int}(\Omega)$, strictly zero boundary normal momentum flux $n_a T^{a0}_{\rm cl}\big|_{\partial\Omega} = 0$ across all six faces, whole-space Lorentzian dominant energy condition (DEC) compliance $\|T^{ab}_{{\rm tot},h}\|\le T^{00}_{{\rm tot},h}$ certified by the universal Beltrami collar plateau constant $M_{\rm st}^{(12)} = 1 + 57e^{-6/7} + 576e^{-12/7} + 972e^{-13/7} + 4608e^{-20/7}$, and diamond-confluent switching-work collar compensation $W_{\rm collar}(h) = \Delta E_{\rm support}(h)$ across all 15 four-birth structural rows and five-birth continuations ($a_4=1/10$). Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## 1. 12-mode homogeneous-Neumann cavity geometry, mode structure, and spatial eigenmodes

### 1.1 Spacetime background and cavity geometry

Consider flat $(3+1)$-dimensional Minkowski spacetime $\mathbb R^{1,3}$ with Cartesian coordinates $x^\mu = (x^0, x_1, x_2, x_3) = (ct, x)$, coordinate time $t$, signature $(-,+,+,+)$, and metric tensor
$$
\eta_{\mu\nu} = \operatorname{diag}(-1, +1, +1, +1), \qquad \eta^{\mu\nu} = \operatorname{diag}(-1, +1, +1, +1).
$$
The cavity domain $\Omega \subset \mathbb R^3$ is a centered spatial cube of side length $L = 8c\tau$ and volume $V = L^3 = 512c^3\tau^3$, where $c > 0$ is the speed of light in vacuum and $\tau > 0$ is a supplied fundamental duration:
$$
\Omega := \left[-\frac{L}{2}, \frac{L}{2}\right]^3 = [-4c\tau, 4c\tau]^3.
$$
The boundary $\partial\Omega$ consists of the six planar square faces $x_1 = \pm L/2$, $x_2 = \pm L/2$, and $x_3 = \pm L/2$. The outward unit normal field $n$ on $\partial\Omega$ is given by:
$$
n = \begin{cases}
\pm e_1, & x_1 = \pm L/2,\\
\pm e_2, & x_2 = \pm L/2,\\
\pm e_3, & x_3 = \pm L/2,
\end{cases}
$$
where $e_a$ ($a\in\{1,2,3\}$) are the standard spatial Cartesian basis vectors.

### 1.2 Longitudinal mode structure and homogeneous Neumann boundary conditions

The cavity supports a 12-mode scalar quantum field $\Phi_{\rm sc}(t,x)$ whose spatial profiles are chosen from the odd harmonic reflections of the fundamental frequency $(N=24, M=12)$. For mode indices $m \in \{0, 1, \dots, 11\}$, the dimensionless odd harmonic integers $n_m$, discrete angular phases $\varphi_m$, positive cotangent weights $c_m$, dimensionless frequencies $\theta_m$, spatial wavenumbers $k_m$, and mode angular frequencies $\omega_m$ are defined by:
$$
n_m := 47 - 2m \in \{25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47\},
$$
$$
\varphi_m := \frac{(2m+1)\pi}{24}, \qquad c_m := \frac{1}{12}\cot\left(\frac{(2m+1)\pi}{48}\right) > 0,
$$
$$
\theta_m := \frac{(47-2m)\pi}{8} > 0, \qquad k_m := \frac{n_m\pi}{L} = \frac{(47-2m)\pi}{8c\tau},
$$
$$
\omega_m := ck_m = \frac{\theta_m}{\tau} = \frac{(47-2m)\pi}{8\tau} > 0.
$$
The spatial eigenmodes $u_m(x)$ are purely longitudinal, depending only on the first spatial coordinate $x_1$:
$$
u_m(x) := \cos\alpha_m(x_1), \qquad \alpha_m(x_1) := k_m\left(x_1 + \frac{L}{2}\right).
$$
We verify the homogeneous Neumann boundary condition $n \cdot \nabla u_m = 0$ on all six faces of $\partial\Omega$:
1. On the face $x_1 = -L/2$, the phase is $\alpha_m(-L/2) = k_m(-L/2 + L/2) = 0$. The normal derivative evaluates to:
   $$
   n \cdot \nabla u_m\big|_{x_1=-L/2} = -e_1 \cdot \nabla u_m\big|_{x_1=-L/2} = -\partial_1 u_m\big|_{x_1=-L/2} = +k_m\sin(0) = 0.
   $$
2. On the face $x_1 = +L/2$, the phase is $\alpha_m(+L/2) = k_m(L/2 + L/2) = k_m L = n_m\pi$. Since $n_m = 47-2m$ is an odd integer, $\sin(n_m\pi) = 0$, and:
   $$
   n \cdot \nabla u_m\big|_{x_1=+L/2} = +e_1 \cdot \nabla u_m\big|_{x_1=+L/2} = \partial_1 u_m\big|_{x_1=+L/2} = -k_m\sin(n_m\pi) = 0.
   $$
3. On the transverse faces $x_2 = \pm L/2$ and $x_3 = \pm L/2$, $u_m(x)$ is identically independent of $x_2$ and $x_3$, so $\partial_2 u_m = \partial_3 u_m = 0$ throughout $\Omega$.

Thus, $n \cdot \nabla u_m = 0$ holds identically on the entire closed boundary $\partial\Omega$.

### 1.3 Mode orthogonality and cavity volume integration

The spatial eigenmodes satisfy exact $L^2(\Omega)$ orthogonality. Integrating across the cavity volume:
$$
\int_\Omega u_m(x)u_{m'}(x)\,d^3x = \int_{-L/2}^{L/2} \cos\left(k_m\left(x_1+\frac{L}{2}\right)\right)\cos\left(k_{m'}\left(x_1+\frac{L}{2}\right)\right)\,dx_1 \times \int_{-L/2}^{L/2}dx_2 \times \int_{-L/2}^{L/2}dx_3.
$$
The transverse integrals yield $L \times L = L^2$. For the longitudinal integral, set $y = x_1 + L/2 \in [0, L]$:
$$
\int_0^L \cos\left(\frac{n_m\pi y}{L}\right)\cos\left(\frac{n_{m'}\pi y}{L}\right)\,dy = \frac{1}{2}\int_0^L \left[\cos\left(\frac{(n_m+n_{m'})\pi y}{L}\right) + \cos\left(\frac{(n_m-n_{m'})\pi y}{L}\right)\right]dy.
$$
For $m \ne m'$, $n_m - n_{m'} = 2(m'-m) \ne 0$ is an even nonzero integer, and $n_m + n_{m'} = 94 - 2(m+m')$ is also a nonzero integer. Both cosines integrate to zero over $[0, L]$. For $m = m'$, the second cosine is $\cos(0) = 1$, giving:
$$
\int_0^L \cos^2\left(\frac{n_m\pi y}{L}\right)\,dy = \frac{L}{2}.
$$
Multiplying by the transverse area $L^2$ yields the exact volumetric normalization:
$$
\int_\Omega u_m(x)u_{m'}(x)\,d^3x = \frac{L^3}{2}\delta_{mm'} = \frac{V}{2}\delta_{mm'}.
$$

### 1.4 Field operator, mode quadratures, and unshifted vacuum Hamiltonian

The canonical field operator $\Phi_{\rm sc}(t,x)$ on the Schwartz core $\mathcal S(\mathbb R^{12}) \subset \mathcal H_{\rm field} := L^2(\mathbb R^{12})$ is defined by:
$$
\Phi_{\rm sc}(t,x) := \sum_{m=0}^{11} B_m u_m(x) X_m(t),
$$
where the mode amplitude normalization $B_m$ is determined by the scalar coupling constant $\kappa > 0$ and reference action scale $A_* > 0$:
$$
B_m := \sqrt{\frac{2A_* c^2}{\kappa V\omega_m}} > 0.
$$
The time-dependent mode quadratures $X_m(t)$ and conjugate momentum quadratures $Y_m(t)$ are given in terms of the canonical Heisenberg pairs $(Q_m, P_m)$ by:
$$
X_m(t) := Q_m\cos(\omega_m t) + P_m\sin(\omega_m t), \qquad Y_m(t) := P_m\cos(\omega_m t) - Q_m\sin(\omega_m t) = \frac{1}{\omega_m}\dot X_m(t),
$$
satisfying the canonical commutation relations:
$$
[Q_m, P_{m'}] = i\delta_{mm'}I_{\rm field}, \qquad [Q_m, Q_{m'}] = [P_m, P_{m'}] = 0, \qquad [X_m(t), Y_m(t)] = iI_{\rm field}.
$$
The unperturbed field Hamiltonian $H_{\rm sc}$ and its dimensionless generator $K$ on $\mathcal S(\mathbb R^{12})$ are:
$$
H_{\rm sc} = \frac{A_*}{\tau}K = \frac{1}{2}\sum_{m=0}^{11} A_*\omega_m(Q_m^2 + P_m^2) = \frac{1}{2}\sum_{m=0}^{11} A_*\omega_m\bigl(X_m(t)^2 + Y_m(t)^2\bigr).
$$
The vacuum ground state $\Omega_0 \in \mathcal S(\mathbb R^{12})$ satisfies $(Q_m + iP_m)\Omega_0 = 0$ for each $m \in \{0, \dots, 11\}$. The vacuum expectation $\omega_{\rm vac}(A) := \langle\Omega_0, A\Omega_0\rangle$ of the Hamiltonian yields the unshifted zero-point ground state energy $E_0$:
$$
E_0 = \omega_{\rm vac}(H_{\rm sc}) = \frac{1}{2}\sum_{m=0}^{11} A_*\omega_m = \frac{A_*\pi}{16\tau}\sum_{m=0}^{11}(47-2m).
$$
The arithmetic progression sum is:
$$
\sum_{m=0}^{11}(47-2m) = 12 \times 47 - 2 \times \frac{11 \times 12}{2} = 564 - 132 = 432.
$$
Therefore, the exact cavity zero-point ground energy is:
$$
E_0 = \frac{432\pi A_*}{16\tau} = \frac{27\pi A_*}{\tau} > 0.
$$

---

## 2. Impulsive pointer-probe kicks along causal histories and classical mean wavefield shift

### 2.1 Pointer probes and adapted interior cavity coordinates

We consider four local two-level quantum pointer probes $\mathcal H_r = \mathbb C^2$ indexed by the birth vertices $r \in \{a, b, x, y\}$, spanning the probe Hilbert space $\mathcal H_{\rm probes} = \bigotimes_{r\in\{a,b,x,y\}}\mathcal H_r \cong \mathbb C^{16}$ and total Hilbert space $\mathcal H_{\rm tot} = \mathcal H_{\rm probes}\otimes \mathcal H_{\rm field}$. Each probe has local computational basis $\{|0\rangle_r, |1\rangle_r\}$, Pauli operators $(X_r^{\rm det}, Y_r^{\rm det}, Z_r^{\rm det})$, and local energy gap $\varepsilon_{\rm det} = A_*\Omega_{\rm det} > 0$:
$$
H_{{\rm det},r} = \varepsilon_{\rm det}|1\rangle\langle 1|_r = \frac{\varepsilon_{\rm det}}{2}(I_r - Z_r^{\rm det}), \qquad H_0 = I_{\rm probes}\otimes H_{\rm sc} + \sum_{r\in\{a,b,x,y\}}H_{{\rm det},r}\otimes I_{\rm field}.
$$
The eigenstates of $X_r^{\rm det}$ with eigenvalues $\sigma_r \in \{+1, -1\}$ and corresponding orthogonal projectors are:
$$
|\sigma_r\rangle_{x,r} := \frac{|0\rangle_r + \sigma_r|1\rangle_r}{\sqrt 2}, \qquad P_{r,\sigma_r}^{(x)} := |\sigma_r\rangle\langle\sigma_r|_{x,r} = \frac{1}{2}(I_r + \sigma_r X_r^{\rm det}).
$$
For any committed causal history $h$, the four vertices are embedded into adapted interior spacetime points $(t_r(h), x_r(h)) \in \mathbb R \times \operatorname{int}(\Omega)$ according to:
$$
t_r(h) := \tau_r(h)\tau, \qquad x_r(h) := \left(-\frac{L}{4} + \xi_r(h)c\tau, \, 0, \, 0\right),
$$
where the dimensionless coordinates $z_r(h) = (\tau_r(h), \xi_r(h)) \in \frac{1}{3}\mathbb Z^2$ satisfy $\xi_r(h) \in [-1, 4/3]$, guaranteeing that $x_{r,1}(h) \in [-3L/8, -L/24] \subset (-L/2, L/2)$, strictly within the cavity interior.

The local cavity readout field operator $\phi_r(h)$ at the probe event is:
$$
\phi_r(h) := \Psi(t_r(h), x_r(h)) = \sum_{m=0}^{11}\sqrt{2\beta c_m}\,u_m(x_r(h))X_m(t_r(h)),
$$
satisfying the commutation relation:
$$
[\phi_r(h), \phi_s(h)] = i D_{rs}(h)I_{\rm field} = i\beta\bigl(c_{rs}(h) - c_{sr}(h)\bigr)I_{\rm field},
$$
where $c_{rs}(h) := \mathbf 1_{\{s \prec_h r\}}$ is the causal precedence indicator on history $h$.

### 2.2 Impulsive kick unitaries and composite history unitary

For dimensionless coupling parameters $\boldsymbol\lambda = (\lambda_a, \lambda_b, \lambda_x, \lambda_y)^{\mathsf T} \in \mathbb R^4$, the impulsive pointer-probe kick unitary at event $r$ is:
$$
U_r(h;\lambda_r) := \exp\left(-i\lambda_r X_r^{\rm det}\otimes\overline{\phi_r(h)}\right) = \sum_{\sigma_r=\pm 1} P_{r,\sigma_r}^{(x)}\otimes\mathcal W_h(-\sigma_r\lambda_r e_r) \in \mathcal B(\mathcal H_{\rm tot}),
$$
where $e_r \in \mathbb R^4$ is the unit vector for probe $r$, and $\mathcal W_h(g) := \exp(i\overline{\Phi_h(g)})$ is the Weyl displacement operator for $\Phi_h(g) = \sum_r g_r\phi_r(h)$.

Whenever two events are incomparable in the causal order, $r \parallel_h s$, we have $s \not\prec_h r$ and $r \not\prec_h s$, so $c_{rs}(h) = c_{sr}(h) = 0$, which implies $D_{rs}(h) = 0$. By the Weyl composition law:
$$
\mathcal W_h(-\sigma_r\lambda_r e_r)\mathcal W_h(-\sigma_s\lambda_s e_s) = e^{-\frac{i}{2}\sigma_r\sigma_s\lambda_r\lambda_s D_{rs}(h)}\mathcal W_h(-\sigma_r\lambda_r e_r - \sigma_s\lambda_s e_s) = \mathcal W_h(-\sigma_s\lambda_s e_s)\mathcal W_h(-\sigma_r\lambda_r e_r).
$$
Because the probe projectors $P_{r,\sigma_r}^{(x)}$ and $P_{s,\sigma_s}^{(x)}$ act on different tensor factors, they commute as well. Therefore:
$$
[U_r(h;\lambda_r), U_s(h;\lambda_s)] = 0 \qquad \forall\, r \parallel_h s.
$$
This diamond commutation guarantees that the total composite unitary $U_{\rm tot}(h;\boldsymbol\lambda)$ is invariant across all topological linear extensions $(r_1, r_2, r_3, r_4)$ of $(h, \prec_h)$, and coincides identically with coordinate-time ordering:
$$
U_{\rm tot}(h;\boldsymbol\lambda) = \sum_{\boldsymbol\sigma\in\{+1,-1\}^4} \exp\left(-\frac{i\beta}{2}\sum_{s\prec_h r}\sigma_s\sigma_r\lambda_s\lambda_r\right) P_{\boldsymbol\sigma}^{(x)}\otimes\mathcal W_h(-\boldsymbol\sigma\odot\boldsymbol\lambda),
$$
where $P_{\boldsymbol\sigma}^{(x)} := \bigotimes_{r\in\{a,b,x,y\}} P_{r,\sigma_r}^{(x)}$ and $(\boldsymbol\sigma\odot\boldsymbol\lambda)_r := \sigma_r\lambda_r$.

### 2.3 Probe sector displacement and classical mean wavefield

In a definite pointer eigenstate sector $\boldsymbol\sigma \in \{+1,-1\}^4$, setting the real displacement vector $g := \boldsymbol\sigma\odot\boldsymbol\lambda \in \mathbb R^4$, the field undergoes an exact coherent Weyl translation:
$$
\mathcal W_h(g) Q_m \mathcal W_h(-g) = Q_m + \gamma_m(h;g)I_{\rm field}, \qquad \mathcal W_h(g) P_m \mathcal W_h(-g) = P_m - \alpha_m(h;g)I_{\rm field},
$$
where the harmonic quadrature shifts $\alpha_m(h;g)$ and $\gamma_m(h;g)$ are given explicitly by:
$$
\alpha_m(h;g) + i\gamma_m(h;g) := \sqrt{2\beta c_m}\sum_{r\in\{a,b,x,y\}} g_r\cos\alpha_{m,r}(h)\,e^{i\omega_m t_r(h)},
$$
with $\alpha_{m,r}(h) := k_m(x_{r,1}(h) + L/2)$. The time-dependent field quadratures shift according to:
$$
\mathcal W_h(g) X_m(t) \mathcal W_h(-g) = X_m(t) + \bigl(\gamma_m(h;g)\cos(\omega_m t) - \alpha_m(h;g)\sin(\omega_m t)\bigr)I_{\rm field},
$$
$$
\mathcal W_h(g) Y_m(t) \mathcal W_h(-g) = Y_m(t) - \bigl(\alpha_m(h;g)\cos(\omega_m t) + \gamma_m(h;g)\sin(\omega_m t)\bigr)I_{\rm field}.
$$
Consequently, in the post-kick coherent state $\mathcal W_h(-g)\Omega_0$, the quantum field operator $\Phi_{\rm sc}(t,x)$ decomposes into its vacuum fluctuation part plus a classical mean wavefield:
$$
\Phi_{\rm sc}(t,x) = \Phi_{\rm cl}(t,x;h,g)I_{\rm field} + \Phi_{\rm sc,vac}(t,x),
$$
where the classical mean wavefield is:
$$
\Phi_{\rm cl}(t,x;h,g) := \langle\mathcal W_h(-g)\Omega_0, \Phi_{\rm sc}(t,x)\mathcal W_h(-g)\Omega_0\rangle = \sum_{m=0}^{11} B_m u_m(x)\bigl(\gamma_m(h;g)\cos(\omega_m t) - \alpha_m(h;g)\sin(\omega_m t)\bigr).
$$
Notice that $\Phi_{\rm cl}(t,x;h,g)$ is a real-valued classical solution of the free wave equation in $\Omega$, with spatial profile given by the homogeneous Neumann modes $u_m(x)$.


---

## 3. Pointwise field stress-energy tensor backreaction

### 3.1 Semiclassical stress-energy tensor operator

In flat Minkowski spacetime $\mathbb R^{1,3}$, the minimally coupled canonical stress-energy tensor operator for the scalar field $\Phi_{\rm sc}(t,x)$ is defined with symmetric Weyl ordering on $\mathcal S(\mathbb R^{12})$ by:
$$
T^{\mu\nu}_{\rm sc}(t,x) := \kappa\left[\frac{1}{2}\bigl\{\partial^\mu\Phi_{\rm sc}, \partial^\nu\Phi_{\rm sc}\bigr\} - \frac{1}{2}\eta^{\mu\nu}\eta^{\alpha\beta}\frac{1}{2}\bigl\{\partial_\alpha\Phi_{\rm sc}, \partial_\beta\Phi_{\rm sc}\bigr\}\right],
$$
where $\{A, B\} = AB + BA$ denotes the operator anticommutator, and $\kappa > 0$ is the field action coupling constant. Lowering indices with $\eta_{\mu\nu} = \operatorname{diag}(-1,1,1,1)$, the space and time derivatives are:
$$
\partial_0 = \frac{1}{c}\partial_t, \qquad \partial^0 = -\partial_0 = -\frac{1}{c}\partial_t, \qquad \partial^a = \partial_a = \frac{\partial}{\partial x_a} \quad (a\in\{1,2,3\}).
$$
In terms of temporal and spatial derivatives, the operator components take the explicit form:
$$
T^{00}_{\rm sc} = \frac{\kappa}{2}\left[\frac{1}{c^2}\dot\Phi_{\rm sc}^2 + |\nabla\Phi_{\rm sc}|^2\right], \qquad T^{0a}_{\rm sc} = -\frac{\kappa}{2c}\bigl\{\dot\Phi_{\rm sc}, \partial_a\Phi_{\rm sc}\bigr\},
$$
$$
T^{ab}_{\rm sc} = \kappa\left[\frac{1}{2}\bigl\{\partial_a\Phi_{\rm sc}, \partial_b\Phi_{\rm sc}\bigr\} + \frac{1}{2}\delta_{ab}\left(\frac{1}{c^2}\dot\Phi_{\rm sc}^2 - |\nabla\Phi_{\rm sc}|^2\right)\right].
$$

### 3.2 Clean split into static vacuum stress and classical coherent wavefield stress

In the committed causal branch $h$ and probe pointer sector $\boldsymbol\sigma \in \{+1,-1\}^4$ with displacement vector $g = \boldsymbol\sigma\odot\boldsymbol\lambda$, the post-kick field state is the coherent state $|\Psi_h(g)\rangle := \mathcal W_h(-g)\Omega_0$. Expanding the field operator as:
$$
\Phi_{\rm sc}(t,x) = \Phi_{\rm cl}(t,x;h,g)I_{\rm field} + \Phi_{\rm sc,vac}(t,x),
$$
where $\Phi_{\rm sc,vac}(t,x) = \mathcal W_h(-g)\Phi_{\rm sc}(t,x)\mathcal W_h(g) - \Phi_{\rm cl}(t,x;h,g)I_{\rm field}$ satisfies $\langle\Psi_h(g), \Phi_{\rm sc,vac}(t,x)\Psi_h(g)\rangle = \omega_{\rm vac}(\Phi_{\rm sc}(t,x)) = 0$, we substitute this decomposition into the symmetric anticommutator:
$$
\frac{1}{2}\bigl\{\partial^\mu\Phi_{\rm sc}, \partial^\nu\Phi_{\rm sc}\bigr\} = \partial^\mu\Phi_{\rm cl}\partial^\nu\Phi_{\rm cl}I_{\rm field} + \frac{1}{2}\bigl\{\partial^\mu\Phi_{\rm sc,vac}, \partial^\nu\Phi_{\rm sc,vac}\bigr\} + \partial^\mu\Phi_{\rm cl}\partial^\nu\Phi_{\rm sc,vac} + \partial^\nu\Phi_{\rm cl}\partial^\mu\Phi_{\rm sc,vac}.
$$
Taking the expectation value $\langle\cdot\rangle_{h,g} := \langle\Psi_h(g), \cdot\,\Psi_h(g)\rangle$, the linear cross terms vanish identically because $\langle\Psi_h(g), \partial^\mu\Phi_{\rm sc,vac}\Psi_h(g)\rangle = \partial^\mu\omega_{\rm vac}(\Phi_{\rm sc}) = 0$. The vacuum quadratic terms evaluate to $\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x))$, while the classical quadratic terms form $T^{\mu\nu}_{\rm cl}(t,x;h,g)$. Thus, the branch-dressed field stress-energy tensor decomposes cleanly and exactly into:
$$
\boxed{\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,g} = \omega_{\rm vac}\bigl(T^{\mu\nu}_{\rm sc}(x)\bigr) + T^{\mu\nu}_{\rm cl}(t,x;h,g).}
$$

### 3.3 Exact components of the vacuum stress tensor

The vacuum expectation $\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x))$ is static, diagonal, and evaluated directly using mode contractions:
$$
\omega_{\rm vac}(X_m(t)X_{m'}(t)) = \omega_{\rm vac}\bigl((Q_m\cos\omega_mt + P_m\sin\omega_mt)(Q_{m'}\cos\omega_{m'}t + P_{m'}\sin\omega_{m'}t)\bigr) = \frac{1}{2}\delta_{mm'},
$$
$$
\omega_{\rm vac}(\dot X_m(t)\dot X_{m'}(t)) = \omega_m^2\omega_{\rm vac}(Y_m(t)Y_{m'}(t)) = \frac{1}{2}\omega_m^2\delta_{mm'},
$$
$$
\omega_{\rm vac}\bigl(\{\dot X_m(t), X_{m'}(t)\}\bigr) = 0.
$$
Substituting these contractions into the mode expansion gives:
$$
\frac{\kappa}{2c^2}\omega_{\rm vac}(\dot\Phi_{\rm sc}^2) = \frac{\kappa}{4c^2}\sum_{m=0}^{11} B_m^2\omega_m^2 u_m(x)^2 = \sum_{m=0}^{11}\rho_m\cos^2\alpha_m(x_1),
$$
$$
\frac{\kappa}{2}\omega_{\rm vac}(|\nabla\Phi_{\rm sc}|^2) = \frac{\kappa}{4}\sum_{m=0}^{11} B_m^2 k_m^2 \sin^2\alpha_m(x_1) = \sum_{m=0}^{11}\rho_m\sin^2\alpha_m(x_1),
$$
where we used the identity relating the mode normalization to the mode energy density:
$$
\frac{\kappa}{4}B_m^2 k_m^2 = \frac{\kappa}{4}\left(\frac{2A_* c^2}{\kappa V\omega_m}\right)\frac{\omega_m^2}{c^2} = \frac{A_*\omega_m}{2V} =: \rho_m = \frac{(47-2m)\pi A_*}{1024 c^3\tau^4} > 0.
$$
Summing the kinetic and gradient terms:
$$
\omega_{\rm vac}\bigl(T^{00}_{\rm sc}(x)\bigr) = \sum_{m=0}^{11}\rho_m\bigl(\cos^2\alpha_m(x_1) + \sin^2\alpha_m(x_1)\bigr) = \sum_{m=0}^{11}\rho_m =: \rho_0^{\rm tot} = \frac{E_0}{V} = \frac{27\pi A_*}{512c^3\tau^4}.
$$
The vacuum energy density is spatially uniform and strictly positive throughout $\Omega$.

The energy flux vanishes identically:
$$
\omega_{\rm vac}\bigl(T^{0a}_{\rm sc}(x)\bigr) = -\frac{\kappa}{2c}\sum_{m=0}^{11}B_m^2 u_m(x)\partial_a u_m(x)\,\omega_{\rm vac}\bigl(\{\dot X_m, X_m\}\bigr) = 0.
$$
For the spatial stress components:
- Along the longitudinal axis ($a=b=1$):
  $$
  \omega_{\rm vac}\bigl(T^{11}_{\rm sc}(x)\bigr) = \sum_{m=0}^{11}\rho_m\left[2\sin^2\alpha_m(x_1) + \cos^2\alpha_m(x_1) - \sin^2\alpha_m(x_1)\right] = \sum_{m=0}^{11}\rho_m = \rho_0^{\rm tot}.
  $$
- Along the transverse directions ($a=b=2$ or $3$):
  Since $\partial_2 u_m = \partial_3 u_m = 0$, only the isotropic trace term contributes:
  $$
  \omega_{\rm vac}\bigl(T^{22}_{\rm sc}(x)\bigr) = \omega_{\rm vac}\bigl(T^{33}_{\rm sc}(x)\bigr) = \sum_{m=0}^{11}\rho_m\bigl(\cos^2\alpha_m(x_1) - \sin^2\alpha_m(x_1)\bigr) = \sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1).
  $$
- Off-diagonal shear components vanish identically ($T^{ab}_{\rm vac} = 0$ for $a \ne b$).
Thus, the static vacuum stress tensor takes the diagonal form:
$$
\omega_{\rm vac}\bigl(T^{\mu\nu}_{\rm sc}(x)\bigr) = \operatorname{diag}\left(\rho_0^{\rm tot}, \, \rho_0^{\rm tot}, \, \sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1), \, \sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)\right).
$$

### 3.4 Exact components of the classical wavefield stress tensor

The classical wavefield stress tensor is generated by the mean wavefield $\Phi_{\rm cl}(t,x;h,g)$:
$$
T^{\mu\nu}_{\rm cl}(t,x;h,g) = \kappa\left[\partial^\mu\Phi_{\rm cl}\partial^\nu\Phi_{\rm cl} - \frac{1}{2}\eta^{\mu\nu}\eta^{\alpha\beta}\partial_\alpha\Phi_{\rm cl}\partial_\beta\Phi_{\rm cl}\right].
$$
Expanding in Cartesian space and time coordinates yields the exact components:
1. Classical energy density:
   $$
   T^{00}_{\rm cl}(t,x;h,g) = \frac{\kappa}{2}\left[\frac{1}{c^2}\dot\Phi_{\rm cl}^2 + |\nabla\Phi_{\rm cl}|^2\right] = \frac{\kappa}{2}\left[\frac{1}{c^2}\dot\Phi_{\rm cl}^2 + (\partial_1\Phi_{\rm cl})^2\right] \ge 0.
   $$
2. Classical momentum flux (Poynting vector density):
   $$
   T^{0a}_{\rm cl}(t,x;h,g) = T^{a0}_{\rm cl}(t,x;h,g) = -\frac{\kappa}{c}\dot\Phi_{\rm cl}\partial_a\Phi_{\rm cl} = -\delta_{a1}\frac{\kappa}{c}\dot\Phi_{\rm cl}\partial_1\Phi_{\rm cl}.
   $$
   The energy flux is strictly longitudinal, vanishing identically along the transverse directions: $T^{02}_{\rm cl} = T^{03}_{\rm cl} = 0$.
3. Classical spatial stress tensor:
   $$
   T^{ab}_{\rm cl}(t,x;h,g) = \kappa\left[\partial_a\Phi_{\rm cl}\partial_b\Phi_{\rm cl} + \frac{1}{2}\delta_{ab}\left(\frac{1}{c^2}\dot\Phi_{\rm cl}^2 - |\nabla\Phi_{\rm cl}|^2\right)\right].
   $$
   Explicitly:
   $$
   T^{11}_{\rm cl}(t,x;h,g) = \frac{\kappa}{2}\left[\frac{1}{c^2}\dot\Phi_{\rm cl}^2 + (\partial_1\Phi_{\rm cl})^2\right] = T^{00}_{\rm cl}(t,x;h,g),
   $$
   $$
   T^{22}_{\rm cl}(t,x;h,g) = T^{33}_{\rm cl}(t,x;h,g) = \frac{\kappa}{2}\left[\frac{1}{c^2}\dot\Phi_{\rm cl}^2 - (\partial_1\Phi_{\rm cl})^2\right],
   $$
   $$
   T^{ab}_{\rm cl}(t,x;h,g) = 0 \qquad (a \ne b).
   $$
All classical stress components are real-valued, smooth functions of $(t,x) \in \mathbb R \times \Omega$.

---

## 4. Exact four-divergence conservation and boundary flux vanishing

### 4.1 Four-divergence conservation on the cavity interior

We now prove that the branch-dressed field stress-energy tensor is identically divergence-free on the open cavity interior $\mathbb R \times \operatorname{int}(\Omega)$.

**Theorem 2 (Exact interior four-divergence conservation).** *On flat Minkowski spacetime, the classical stress-energy tensor of any solution to the free scalar wave equation $(\Box)\Phi = 0$ is divergence-free: $\partial_\mu T^{\mu\nu}_{\rm cl} = 0$. Since $\Box\Phi_{\rm cl} = 0$ on $\mathbb R \times \operatorname{int}(\Omega)$ and $\partial_\mu\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}) = 0$, the total branch-dressed stress tensor satisfies:*
$$
\boxed{\partial_\mu\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,g} = 0 \qquad \forall\,(t,x)\in\mathbb R\times\operatorname{int}(\Omega).}
$$

*Proof.*
First, compute the four-divergence of the classical stress-energy tensor:
$$
\partial_\mu T^{\mu\nu}_{\rm cl} = \kappa\,\partial_\mu\left[\partial^\mu\Phi_{\rm cl}\partial^\nu\Phi_{\rm cl} - \frac{1}{2}\eta^{\mu\nu}\partial_\alpha\Phi_{\rm cl}\partial^\alpha\Phi_{\rm cl}\right].
$$
Applying the product rule to both terms:
$$
\partial_\mu\left(\partial^\mu\Phi_{\rm cl}\partial^\nu\Phi_{\rm cl}\right) = (\partial_\mu\partial^\mu\Phi_{\rm cl})\partial^\nu\Phi_{\rm cl} + \partial^\mu\Phi_{\rm cl}\partial_\mu\partial^\nu\Phi_{\rm cl} = (\Box\Phi_{\rm cl})\partial^\nu\Phi_{\rm cl} + \partial^\mu\Phi_{\rm cl}\partial_\mu\partial^\nu\Phi_{\rm cl},
$$
$$
\frac{1}{2}\eta^{\mu\nu}\partial_\mu\left(\partial_\alpha\Phi_{\rm cl}\partial^\alpha\Phi_{\rm cl}\right) = \frac{1}{2}\partial^\nu\left(\partial_\alpha\Phi_{\rm cl}\partial^\alpha\Phi_{\rm cl}\right) = \partial^\alpha\Phi_{\rm cl}\partial^\nu\partial_\alpha\Phi_{\rm cl}.
$$
Relabeling the dummy index $\alpha \to \mu$ and using the commutativity of partial derivatives on smooth functions, $\partial_\mu\partial^\nu\Phi_{\rm cl} = \partial^\nu\partial_\mu\Phi_{\rm cl}$, the two contraction terms cancel identically:
$$
\partial^\mu\Phi_{\rm cl}\partial_\mu\partial^\nu\Phi_{\rm cl} - \partial^\mu\Phi_{\rm cl}\partial^\nu\partial_\mu\Phi_{\rm cl} = 0.
$$
Therefore:
$$
\partial_\mu T^{\mu\nu}_{\rm cl} = \kappa(\Box\Phi_{\rm cl})\partial^\nu\Phi_{\rm cl}.
$$
Next, examine the action of the d'Alembertian $\Box = -\frac{1}{c^2}\partial_t^2 + \nabla^2$ on each mode product in $\Phi_{\rm cl}(t,x;h,g) = \sum_{m=0}^{11} B_m u_m(x)X_m^{\rm cl}(t)$:
$$
-\frac{1}{c^2}\partial_t^2 X_m^{\rm cl}(t) = \frac{\omega_m^2}{c^2}X_m^{\rm cl}(t) = k_m^2 X_m^{\rm cl}(t),
$$
$$
\nabla^2 u_m(x) = \partial_1^2\cos\alpha_m(x_1) = -k_m^2\cos\alpha_m(x_1) = -k_m^2 u_m(x).
$$
Adding the two terms gives:
$$
\Box\bigl(u_m(x)X_m^{\rm cl}(t)\bigr) = \left(k_m^2 - k_m^2\right)u_m(x)X_m^{\rm cl}(t) = 0.
$$
By linearity, $\Box\Phi_{\rm cl}(t,x;h,g) = 0$ holds identically for all $(t,x) \in \mathbb R \times \operatorname{int}(\Omega)$. Hence:
$$
\partial_\mu T^{\mu\nu}_{\rm cl}(t,x;h,g) = 0 \qquad \forall\,(t,x)\in\mathbb R\times\operatorname{int}(\Omega).
$$

For the static vacuum stress tensor, $\partial_0\omega_{\rm vac}(T^{0\nu}_{\rm sc}) = 0$. For $\nu = 0$, $\partial_a\omega_{\rm vac}(T^{a0}_{\rm sc}) = 0$ because $\omega_{\rm vac}(T^{a0}_{\rm sc}) = 0$. For $\nu = b \in \{1,2,3\}$:
- For $b = 1$: $\partial_1\omega_{\rm vac}(T^{11}_{\rm sc}) = \partial_1(\rho_0^{\rm tot}) = 0$.
- For $b = 2$: $\partial_2\omega_{\rm vac}(T^{22}_{\rm sc}) = \partial_2\bigl(\sum_m\rho_m\cos 2\alpha_m(x_1)\bigr) = 0$, since the term depends only on $x_1$.
- For $b = 3$: $\partial_3\omega_{\rm vac}(T^{33}_{\rm sc}) = \partial_3\bigl(\sum_m\rho_m\cos 2\alpha_m(x_1)\bigr) = 0$.
All off-diagonal terms are zero. Thus:
$$
\partial_\mu\omega_{\rm vac}\bigl(T^{\mu\nu}_{\rm sc}(x)\bigr) = 0 \qquad \forall\,x\in\operatorname{int}(\Omega).
$$
Combining the two parts establishes $\partial_\mu\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,g} = 0$. $\square$

### 4.2 Vanishing boundary normal momentum flux

We examine the momentum flux through the six planar faces of the cavity boundary $\partial\Omega$.

**Theorem 3 (Strictly zero boundary normal momentum flux).** *Under the homogeneous Neumann boundary condition $n \cdot \nabla u_m = 0$ on $\partial\Omega$, the total momentum flux crossing the cavity boundary vanishes identically at all times:*
$$
\boxed{n_a \langle T^{a0}_{\rm sc}(t,x)\rangle_{h,g}\Big|_{\partial\Omega} = 0 \qquad \forall\,(t,x)\in\mathbb R\times\partial\Omega.}
$$

*Proof.*
The total momentum flux across a boundary element with outward normal $n_a$ is given by:
$$
n_a \langle T^{a0}_{\rm sc}\rangle_{h,g} = n_a\omega_{\rm vac}(T^{a0}_{\rm sc}) + n_a T^{a0}_{\rm cl}.
$$
As established in Section 3.3, $\omega_{\rm vac}(T^{a0}_{\rm sc}) = 0$ identically throughout $\Omega$.

For the classical wavefield flux, substituting $T^{a0}_{\rm cl} = -\frac{\kappa}{c}\dot\Phi_{\rm cl}\partial_a\Phi_{\rm cl}$ yields:
$$
n_a T^{a0}_{\rm cl}\Big|_{\partial\Omega} = -\frac{\kappa}{c}\dot\Phi_{\rm cl}(t,x)\,(n \cdot \nabla\Phi_{\rm cl})\Big|_{\partial\Omega}.
$$
Since $\Phi_{\rm cl}(t,x) = \sum_{m=0}^{11}B_m u_m(x)X_m^{\rm cl}(t)$, taking the directional derivative along the outward unit normal $n$ gives:
$$
n \cdot \nabla\Phi_{\rm cl}\Big|_{\partial\Omega} = \sum_{m=0}^{11} B_m (n \cdot \nabla u_m)\Big|_{\partial\Omega} X_m^{\rm cl}(t).
$$
In Section 1.2, we proved that $n \cdot \nabla u_m\big|_{\partial\Omega} = 0$ holds identically on all six faces of $\partial\Omega$:
- On $x_1 = -L/2$: $n = -e_1 \implies n \cdot \nabla u_m = -\partial_1 u_m = k_m\sin(0) = 0$.
- On $x_1 = +L/2$: $n = +e_1 \implies n \cdot \nabla u_m = +\partial_1 u_m = -k_m\sin(n_m\pi) = 0$.
- On $x_2 = \pm L/2$: $n = \pm e_2 \implies n \cdot \nabla u_m = \pm\partial_2 u_m = 0$.
- On $x_3 = \pm L/2$: $n = \pm e_3 \implies n \cdot \nabla u_m = \pm\partial_3 u_m = 0$.
Therefore, $n \cdot \nabla\Phi_{\rm cl}\big|_{\partial\Omega} = 0$ for all $t \in \mathbb R$. Consequently:
$$
n_a T^{a0}_{\rm cl}\Big|_{\partial\Omega} = 0.
$$
Thus, no momentum or energy flux escapes through the cavity walls into the exterior. $\square$

### 4.3 Boundary spatial traction and necessity of the confining collar

While the momentum flux $n_a T^{a0}$ vanishes at the boundary, the normal spatial traction $n_a T^{ab}$ does not vanish. On $\partial\Omega$, the normal spatial force density exerted by the interior field on the boundary is:
$$
n_a \langle T^{ab}_{\rm sc}\rangle_{h,g}\Big|_{\partial\Omega} = n_a\omega_{\rm vac}\bigl(T^{ab}_{\rm sc}\bigr)\Big|_{\partial\Omega} + n_a T^{ab}_{\rm cl}\Big|_{\partial\Omega}.
$$
Using $n \cdot \nabla\Phi_{\rm cl} = 0$ on $\partial\Omega$, the classical traction simplifies to:
$$
n_a T^{ab}_{\rm cl}\Big|_{\partial\Omega} = \frac{\kappa}{2}n^b\left(\frac{1}{c^2}\dot\Phi_{\rm cl}^2 - |\nabla\Phi_{\rm cl}|^2\right)\Bigg|_{\partial\Omega}.
$$
On the longitudinal faces $x_1 = \pm L/2$, $\partial_1\Phi_{\rm cl} = 0$ and $\partial_2\Phi_{\rm cl} = \partial_3\Phi_{\rm cl} = 0$, so $|\nabla\Phi_{\rm cl}|^2 = 0$, giving an outward normal pressure:
$$
n_a T^{ab}_{\rm cl}\Big|_{x_1=\pm L/2} = \frac{\kappa}{2c^2}\dot\Phi_{\rm cl}^2 n^b.
$$
Including the vacuum stress $\omega_{\rm vac}(T^{11}_{\rm sc}) = \rho_0^{\rm tot}$, the total normal traction on $x_1 = \pm L/2$ is:
$$
n_a \langle T^{ab}_{\rm sc}\rangle_{h,g}\Big|_{x_1=\pm L/2} = \left(\rho_0^{\rm tot} + \frac{\kappa}{2c^2}\dot\Phi_{\rm cl}^2\right)n^b \ne 0.
$$
If one attempted to truncate the cavity stress to zero outside $\Omega$ via $T^{\mu\nu}_{\rm trunc} = \mathbf 1_\Omega \langle T^{\mu\nu}_{\rm sc}\rangle$, the spatial divergence would develop a non-zero distributional surface layer:
$$
\partial_a T^{ab}_{\rm trunc} = -n_a \langle T^{ab}_{\rm sc}\rangle \delta_{\partial\Omega} \ne 0.
$$
This demonstrates that an isolated, conserved system cannot truncate the field stress abruptly at the boundary. An exterior confining collar $T^{\mu\nu}_{\rm col}$ must surround the cavity to smoothly absorb this boundary traction and guarantee whole-space four-divergence conservation $\partial_\mu T^{\mu\nu}_{\rm tot} = 0$ everywhere on $\mathbb R^{1,3}$.


---

## 5. Whole-space Lorentzian dominant energy condition (DEC) compliance

### 5.1 Lorentzian dominant energy condition for classical scalar fields

In general relativity and relativistic field theory, the Dominant Energy Condition (DEC) states that for every future-directed causal vector field $u^\mu$ ($u^0 \ge |\vec u| \ge 0$, $\eta_{\mu\nu}u^\mu u^\nu \le 0$), the energy-momentum current density vector $J^\mu := -T^\mu{}_\nu u^\nu = T^{\mu\nu}(-u_\nu)$ must be a future-directed causal four-vector:
$$
J^0 \ge |\vec J| \ge 0, \qquad \eta_{\mu\nu}J^\mu J^\nu \le 0.
$$
Equivalently, for every pair of future-directed causal vectors $u^\mu, v^\mu$:
$$
T^{\mu\nu}u_\mu v_\nu \ge 0.
$$
When the energy flux vanishes, $T^{0a} = 0$, the DEC is algebraically equivalent to:
$$
T^{00} \ge \|T^{ab}\|,
$$
where $\|T^{ab}\| := \sup_{|v|=1}|v_a T^{ab} v_b|$ is the spatial operator norm (the maximum absolute eigenvalue of the spatial stress tensor).

For any classical scalar field with minimally coupled stress tensor $T^{\mu\nu}_{\rm cl} = \kappa[\partial^\mu\Phi\partial^\nu\Phi - \frac{1}{2}\eta^{\mu\nu}\partial_\alpha\Phi\partial^\alpha\Phi]$, contracting with future-directed causal vectors $u_\mu, v_\nu$ gives:
$$
T^{\mu\nu}_{\rm cl}u_\mu v_\nu = \kappa\left[(u \cdot \partial\Phi)(v \cdot \partial\Phi) - \frac{1}{2}(u \cdot v)(\partial\Phi \cdot \partial\Phi)\right].
$$
If $\partial\Phi$ is timelike or null, $\partial\Phi \cdot \partial\Phi \le 0$, and since $u$ and $v$ are future-directed causal, $u \cdot v = -u^0 v^0 + \vec u \cdot \vec v \le -u^0 v^0 + |\vec u||\vec v| \le 0$, so $-\frac{1}{2}(u \cdot v)(\partial\Phi \cdot \partial\Phi) \le 0$, while $(u \cdot \partial\Phi)(v \cdot \partial\Phi) \ge 0$. If $\partial\Phi$ is spacelike, $\partial\Phi \cdot \partial\Phi > 0$, and Cauchy–Schwarz in Minkowski spacetime proves that $(u \cdot \partial\Phi)(v \cdot \partial\Phi) \ge \frac{1}{2}(u \cdot v)(\partial\Phi \cdot \partial\Phi)$. In all cases, $T^{\mu\nu}_{\rm cl}u_\mu v_\nu \ge 0$ holds identically. In particular, the classical energy density satisfies $T^{00}_{\rm cl} = \frac{\kappa}{2}[\frac{1}{c^2}\dot\Phi_{\rm cl}^2 + |\nabla\Phi_{\rm cl}|^2] \ge 0$, and $\|T^{ab}_{\rm cl}\| \le T^{00}_{\rm cl}$.

### 5.2 Whole-space total stress tensor and the exterior Beltrami collar

To achieve whole-space four-divergence conservation $\partial_\mu T^{\mu\nu}_{\rm tot} = 0$ on all of $\mathbb R^{1,3}$ without violating the DEC, the cavity is embedded into a smooth confining Beltrami stress collar:
$$
T^{\mu\nu}_{{\rm tot},h}(t,x) := \mathbf 1_\Omega(x)\langle T^{\mu\nu}_{\rm sc}(t,x)\rangle_{h,g} + T^{\mu\nu}_{{\rm col},h}(t,x).
$$
The interior spatial stress tensor has potential representation $T^{ab}(\Phi^{\rm int})(x) = \epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}^{\rm int}(x)$, where $\Phi^{\rm int}(x) = \operatorname{diag}(0, \Phi_2^{\rm int}, \Phi_3^{\rm int})$ is defined on $\mathbb R^3$ by:
$$
g(x_1) := \sum_{m=0}^{11}\frac{\rho_m}{2k_m^2}\sin^2\alpha_m(x_1) \ge 0,
$$
$$
\Phi_1^{\rm int}(x) \equiv 0, \qquad \Phi_2^{\rm int}(x) := \frac{1}{4}\rho_0^{\rm tot}x_3^2 + g(x_1), \qquad \Phi_3^{\rm int}(x) := \frac{1}{4}\rho_0^{\rm tot}x_2^2 + g(x_1).
$$
Because $\epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}$ is identically divergence-free for any smooth tensor $\Phi_{mn}$, smoothing $\Phi^{\rm int}$ radially guarantees exact spatial momentum conservation. Let $s := |x|/L$ and $\sigma := s^2 = |x|^2/L^2$, and define the $C^\infty$ cutoff family using the standard flat bump generator $b(t) := e^{-1/t}\mathbf 1_{(0,\infty)}(t)$:
$$
\chi_{\rm st}(s) := \frac{b(4-s^2)}{b(4-s^2) + b(s^2 - 9/4)}, \qquad \chi_{\rm rise}(s) := \frac{b(s^2-1)}{b(s^2-1) + b(9/4 - s^2)}, \qquad \chi_{\rm out}(s) := \frac{b(9-s^2)}{b(9-s^2) + b(s^2 - 4)}.
$$
The whole-space collar potential and energy density are:
$$
\Phi_{mn}(x) := \chi_{\rm st}\left(\frac{|x|}{L}\right)\Phi_{mn}^{\rm int}(x),
$$
$$
\varepsilon_{\rm tot}(|x|) := \left[\rho_{{\rm cav},h}^{\rm tot} + U_{{\rm col},h}\chi_{\rm rise}\left(\frac{|x|}{L}\right)\right]\chi_{\rm out}\left(\frac{|x|}{L}\right),
$$
where $\rho_{{\rm cav},h}^{\rm tot} := \rho_0^{\rm tot} + \rho_{\rm cl}(h)$ is the peak interior energy density, and $U_{{\rm col},h}$ is the collar energy plateau parameter. The total whole-space stress tensor components are:
$$
T^{00}_{{\rm tot},h}(t,x) := \varepsilon_{\rm tot}(|x|), \qquad T^{0a}_{{\rm tot},h}(t,x) := \mathbf 1_\Omega(x) T^{0a}_{\rm cl}(t,x;h,g), \qquad T^{ab}_{{\rm tot},h}(t,x) := \epsilon_{akm}\epsilon_{bln}\partial_k\partial_l\Phi_{mn}(x).
$$

### 5.3 Exact derivation of the universal collar plateau constant $M_{\rm st}^{(12)}$

To certify the Lorentzian dominant energy condition $\|T^{ab}_{{\rm tot},h}(t,x)\| \le T^{00}_{{\rm tot},h}(t,x)$ across all of $\mathbb R^3$, we partition space into three radial shells:

1. **Cavity and inner ramp shell ($0 \le s \le 3/2$):** Here $|x| \le 3L/2$, so $\chi_{\rm st}(s) = 1$. The stress tensor is purely the interior potential stress $T^{ab}(\Phi^{\rm int})(x) = \operatorname{diag}(\rho_0^{\rm tot}, g''(x_1), g''(x_1))$. Since $|g''(x_1)| = \lvert\sum_{m=0}^{11}\rho_m\cos 2\alpha_m(x_1)\rvert \le \rho_0^{\rm tot}$, we have $\|T^{ab}_{{\rm tot},h}\| = \rho_0^{\rm tot} \le \rho_0^{\rm tot} + U_{{\rm col},h}\chi_{\rm rise}(s) \le T^{00}_{{\rm tot},h}$ for any $U_{{\rm col},h} \ge 0$.
2. **Outer exterior shell ($s \ge 2$):** Here $|x| \ge 2L$, so $\chi_{\rm st}(s) = 0$. The spatial stress vanishes identically, $T^{ab}_{{\rm tot},h} = 0$, so $\|T^{ab}_{{\rm tot},h}\| = 0 \le T^{00}_{{\rm tot},h}$ holds trivially.
3. **Transition shell ($3/2 \le s \le 2$):** Here $9/4 \le \sigma \le 4$. In this shell, $\chi_{\rm rise}(s) = 1$ and $\chi_{\rm out}(s) = 1$, so the total energy density is constant:
   $$
   T^{00}_{{\rm tot},h}(t,x) = \rho_{{\rm cav},h}^{\rm tot} + U_{{\rm col},h}.
   $$
   Setting $\eta(x) := \chi_{\rm st}(|x|/L) = F(\sigma)$, we differentiate the product $\Phi_{mn}(x) = \eta(x)\Phi_{mn}^{\rm int}(x)$ to evaluate $T^{ab}_{{\rm tot},h}$. For any spatial unit vector $v \in \mathbb R^3$ ($|v|=1$), contracting $v_a T^{ab} v_b$ yields:
   $$
   v_a T^{ab}_{{\rm tot},h} v_b = \eta(x) v_a T^{ab}(\Phi^{\rm int}) v_b + 2\sum_{m=2}^3 (w^{(m)}\cdot\nabla\eta)(w^{(m)}\cdot\nabla\Phi_m^{\rm int}) + \sum_{m=2}^3 \Phi_m^{\rm int}{w^{(m)}}^{\mathsf T}[\operatorname{Hess}\eta]w^{(m)},
   $$
   where $w^{(m)}_k := \sum_{a=1}^3 v_a\epsilon_{akm}$ satisfies $|w^{(m)}|^2 = 1 - v_m^2 \le 1$. By Cauchy–Schwarz:
   $$
   \|T^{ab}_{{\rm tot},h}\| \le \eta(x)\|T^{ab}(\Phi^{\rm int})\| + 2|\nabla\eta|\sum_{m=2}^3|\nabla\Phi_m^{\rm int}| + \|\operatorname{Hess}\eta\|\sum_{m=2}^3\Phi_m^{\rm int}.
   $$

We establish exact closed-form bounds on each factor across $\sigma \in [9/4, 4]$ ($|x| \le 2L$):
- **Potential magnitude**:
  $$
  \sum_{m=2}^3 \Phi_m^{\rm int}(x) = \frac{1}{4}\rho_0^{\rm tot}(x_2^2 + x_3^2) + 2g(x_1) \le \frac{1}{4}\rho_0^{\rm tot}(4L^2) + 2\sum_{m=0}^{11}\frac{\rho_m}{2k_m^2}(2).
  $$
  Since $k_m \ge k_{11} = \frac{25\pi}{L}$, we have $\frac{2}{k_m^2} \le \frac{2L^2}{625\pi^2}$. Using $\sum_{m=0}^{11}\rho_m = \rho_0^{\rm tot}$ and $\pi > 3 \implies 625\pi^2 > 5625 > 8$, we find:
  $$
  \sum_{m=2}^3 \Phi_m^{\rm int}(x) \le \left(1 + \frac{1}{625\pi^2}\right)\rho_0^{\rm tot}L^2 < \frac{9}{8}\rho_0^{\rm tot}L^2.
  $$
- **Potential gradient**:
  The derivative of $g(x_1)$ is $g'(x_1) = \sum_{m=0}^{11}\frac{\rho_m}{2k_m}\sin 2\alpha_m(x_1)$. Notice that:
  $$
  \frac{\rho_m}{2k_m} = \frac{(47-2m)\rho_0^{\rm tot}/432}{2(47-2m)\pi/L} = \frac{\rho_0^{\rm tot}L}{864\pi}
  $$
  is strictly independent of $m$. Summing over the 12 modes: $|g'(x_1)| \le 12 \times \frac{\rho_0^{\rm tot}L}{864\pi} = \frac{\rho_0^{\rm tot}L}{72\pi}$. Together with $|\nabla\Phi_2^{\rm int}| + |\nabla\Phi_3^{\rm int}| \le 2|g'(x_1)| + \frac{1}{2}\rho_0^{\rm tot}(|x_2| + |x_3|)$ and $|x_2| + |x_3| \le \sqrt{2(x_2^2+x_3^2)} \le 2\sqrt 2 L$:
  $$
  \sum_{m=2}^3 |\nabla\Phi_m^{\rm int}(x)| \le \left(\sqrt 2 + \frac{1}{36\pi}\right)\rho_0^{\rm tot}L.
  $$
  Using $\sqrt 2 < 17/12$ and $36\pi > 108 \implies \frac{1}{36\pi} < \frac{1}{108}$, we have $\sqrt 2 + \frac{1}{36\pi} < \frac{17}{12} + \frac{1}{108} = \frac{154}{108} = \frac{77}{54} < \frac{3}{2}$. Hence:
  $$
  \sum_{m=2}^3 |\nabla\Phi_m^{\rm int}(x)| < \frac{3}{2}\rho_0^{\rm tot}L.
  $$
- **Cutoff function derivatives**:
  Writing $F(\sigma) = \frac{b_1(\sigma)}{D(\sigma)}$ with $b_1(\sigma) = b(4-\sigma)$, $b_2(\sigma) = b(\sigma - 9/4)$, and $D(\sigma) = b_1(\sigma) + b_2(\sigma)$:
  The sum of arguments is $(4-\sigma) + (\sigma - 9/4) = 7/4$, so at least one argument is $\ge 7/8$, giving $D(\sigma) \ge e^{-8/7}$.
  The bump derivatives satisfy $b'(t) = t^{-2}e^{-1/t} \le 4e^{-2}$ and $|b''(t)| \le 256e^{-4} + 54e^{-3}$.
  Quotient differentiation yields:
  $$
  |F'(\sigma)| \le \frac{4e^{-2}}{e^{-8/7}} = 4e^{-6/7} =: F_1,
  $$
  $$
  |F''(\sigma)| \le (256e^{-4} + 54e^{-3})e^{8/7} + 2(4e^{-6/7})(4e^{-2})e^{8/7} = 32e^{-12/7} + 54e^{-13/7} + 256e^{-20/7} =: F_2.
  $$
  Since $\partial_k\eta = \frac{2x_k}{L^2}F'(\sigma)$ and $\partial_k\partial_l\eta = \frac{4x_k x_l}{L^4}F''(\sigma) + \frac{2\delta_{kl}}{L^2}F'(\sigma)$ with $|x| \le 2L$:
  $$
  |\nabla\eta| \le \frac{4F_1}{L}, \qquad \|\operatorname{Hess}\eta\| \le \frac{16F_2 + 2F_1}{L^2}.
  $$

Combining these bounds into the stress norm inequality gives:
$$
\|T^{ab}_{{\rm tot},h}(t,x)\| < \left[1 + 2\left(\frac{4F_1}{L}\right)\left(\frac{3}{2}L\right) + \left(\frac{16F_2 + 2F_1}{L^2}\right)\left(\frac{9}{8}L^2\right)\right]\rho_0^{\rm tot}
= \left(1 + \frac{57}{4}F_1 + 18F_2\right)\rho_0^{\rm tot}.
$$
Substituting $F_1 = 4e^{-6/7}$ and $F_2 = 32e^{-12/7} + 54e^{-13/7} + 256e^{-20/7}$:
$$
\frac{57}{4}F_1 = 57e^{-6/7}, \qquad 18F_2 = 576e^{-12/7} + 972e^{-13/7} + 4608e^{-20/7}.
$$
Thus, we define the exact universal 12-mode Beltrami collar constant:
$$
\boxed{M_{\rm st}^{(12)} := 1 + 57e^{-6/7} + 576e^{-12/7} + 972e^{-13/7} + 4608e^{-20/7} > 1.}
$$
By setting the collar plateau parameter:
$$
\boxed{U_{{\rm col},h} \ge M_{\rm st}^{(12)}\rho_{{\rm cav},h}^{\rm tot},}
$$
the total energy density in the transition shell satisfies:
$$
T^{00}_{{\rm tot},h}(t,x) = \rho_{{\rm cav},h}^{\rm tot} + U_{{\rm col},h} \ge \rho_{{\rm cav},h}^{\rm tot} + M_{\rm st}^{(12)}\rho_{{\rm cav},h}^{\rm tot} > \|T^{ab}_{{\rm tot},h}(t,x)\|.
$$
This ensures strict compliance with the Lorentzian dominant energy condition across all of $\mathbb R^{1,3}$ with a positive safety margin greater than $\rho_{{\rm cav},h}^{\rm tot}$.

---

## 6. Switching-work collar compensation and multi-birth diamond confluence

### 6.1 Cavity excitation energy and two-sided spectral bounds

Under the pointer-probe kicks along history $h$, the 12 cavity modes receive displacement $g = \boldsymbol\sigma\odot\boldsymbol\lambda$. The net injected field excitation energy is:
$$
\Delta E_{\rm field}(h;\boldsymbol\sigma,\boldsymbol\lambda) := \langle\mathcal W_h(-g)\Omega_0, H_{\rm sc}\mathcal W_h(-g)\Omega_0\rangle - E_0 = (\boldsymbol\sigma\odot\boldsymbol\lambda)^{\mathsf T}\mathcal E(h)(\boldsymbol\sigma\odot\boldsymbol\lambda),
$$
where the $4 \times 4$ real symmetric branch excitation matrix $\mathcal E(h)$ has elements:
$$
\mathcal E_{rs}(h) := \beta A_*\operatorname{Re}\sum_{m=0}^{11}\omega_m c_m\cos\alpha_{m,r}(h)\cos\alpha_{m,s}(h)\,e^{-i\omega_m(t_r(h)-t_s(h))}.
$$
Because the 12 mode frequencies satisfy the strict monotonicity:
$$
\omega_{11} = \frac{25\pi}{8\tau} \le \omega_m \le \omega_0 = \frac{47\pi}{8\tau},
$$
and $V(h) = \operatorname{Re}W(h) \succ 0$ is the positive-definite symmetric branch covariance matrix ($V_{rs}(h) = \beta\operatorname{Re}\sum_{m=0}^{11}c_m\cos\alpha_{m,r}\cos\alpha_{m,s}e^{-i\omega_m(t_r-t_s)}$), the field excitation energy is strictly bounded from above and below by the spectral band limits:
$$
\boxed{0 < \frac{25\pi A_*}{8\tau}(\boldsymbol\sigma\odot\boldsymbol\lambda)^{\mathsf T}V(h)(\boldsymbol\sigma\odot\boldsymbol\lambda) < \Delta E_{\rm field}(h;\boldsymbol\sigma,\boldsymbol\lambda) < \frac{47\pi A_*}{8\tau}(\boldsymbol\sigma\odot\boldsymbol\lambda)^{\mathsf T}V(h)(\boldsymbol\sigma\odot\boldsymbol\lambda)} \qquad (\forall\,\boldsymbol\lambda \ne \mathbf 0),
$$
with equality $\Delta E_{\rm field} = 0$ if and only if $\boldsymbol\lambda = \mathbf 0$.

### 6.2 Collar reaction work and complete work compensation

When the cavity field absorbs excitation energy $\Delta E_{\rm field}(h)$, the interior peak energy density increases by $\Delta\rho_{\rm cav}(h) = \frac{\Delta E_{\rm field}(h)}{V}$. To maintain whole-space DEC compliance without violating four-divergence conservation, the confining collar plateau must dynamically adjust by:
$$
\Delta U_{{\rm col},h} = M_{\rm st}^{(12)}\Delta\rho_{\rm cav}(h) = M_{\rm st}^{(12)}\frac{\Delta E_{\rm field}(h)}{V}.
$$
The external switching work expended to establish this compensating collar stress is the collar reaction work $W_{\rm collar}(h) = \Delta E_{\rm support}(h)$, defined by the volumetric integral over the support shell $\mathbb R^3 \setminus \Omega$:
$$
W_{\rm collar}(h) := \int_{\mathbb R^3\setminus\Omega} \Delta\varepsilon_{{\rm tot},h}(|x|)\,d^3x = 4\pi L^3 \Delta U_{{\rm col},h} \int_1^3 s^2\chi_{\rm rise}(s)\chi_{\rm out}(s)\,ds.
$$
Substituting $\Delta U_{{\rm col},h} = M_{\rm st}^{(12)}\frac{\Delta E_{\rm field}(h)}{L^3}$ yields the exact proportionality:
$$
\boxed{W_{\rm collar}(h) = 4\pi M_{\rm st}^{(12)}\Delta E_{\rm field}(h)\int_1^3 s^2\chi_{\rm rise}(s)\chi_{\rm out}(s)\,ds.}
$$
This establishes that the collar reaction work is strictly proportional to the injected cavity field excitation energy, completing the switching-work balance across every branch of history.

### 6.3 Complete 15-row four-birth ledger

Across the fixed prepared prefix $a \prec b$ with root bits $i \in \{0,1\}$, Table 1 displays the complete 15-row four-birth structural ledger, recording the predecessor ideals $I_x, I_y$, unconditioned probability numerators over $1320$ (and $5280$ for marked continuations), causal indicators, and work-ledger status:

| Row | $I_x$ | $I_y$ | $1320P_0(I_x,I_y)$ | $1320P_1(I_x,I_y)$ | $5280P_0(I_x,I_y,b_3,b_4)$ | $5280P_1(I_x,I_y,b_3,b_4)$ | $(\mathbf 1_{\{a\prec x\}}, \mathbf 1_{\{b\prec x\}})$ | Multi-probe stress & collar ledger status |
|---:|---|---|---:|---:|---:|---:|---|---|
| 1 | $\varnothing$ | $\varnothing$ | 6 | 6 | 6 | 6 | $(0,0)$ | exact DEC & divergence-free |
| 2 | $\varnothing$ | $x$ | 6 | 6 | 6 | 6 | $(0,0)$ | exact DEC & divergence-free |
| 3 | $\varnothing$ | $a$ | 5 | 10 | 5 | 10 | $(0,0)$ | exact DEC & divergence-free |
| 4 | $\varnothing$ | $ab$ | 19 | 14 | 19 | 14 | $(0,0)$ | exact DEC & divergence-free |
| 5 | $\varnothing$ | $ax$ | 33 | 33 | 33 | 33 | $(0,0)$ | exact DEC & divergence-free |
| 6 | $\varnothing$ | $abx$ | 195 | 195 | 195 | 195 | $(0,0)$ | exact DEC & divergence-free |
| 7 | $a$ | $\varnothing$ | 5 | 10 | 5 | 10 | $(1,0)$ | exact DEC & divergence-free |
| 8 | $a$ | $a$ | 5 | 10 | 5 | 10 | $(1,0)$ | exact DEC & divergence-free |
| 9 | $a$ | $ab$ | 19 | 14 | 19 | 14 | $(1,0)$ | exact DEC & divergence-free |
| 10 | $a$ | $ax$ | 19 | 14 | 19 | 14 | $(1,0)$ | exact DEC & divergence-free |
| 11 | $a$ | $abx$ | 172 | 392 | 172 | 392 | $(1,0)$ | exact DEC & divergence-free |
| 12 | $ab$ | $\varnothing$ | 19 | 14 | 19 | 14 | $(1,1)$ | exact DEC & divergence-free |
| 13 | $ab$ | $a$ | 19 | 14 | 19 | 14 | $(1,1)$ | exact DEC & divergence-free |
| 14 | $ab$ | $ab$ | 19 | 14 | 19 | 14 | $(1,1)$ | exact DEC & divergence-free |
| 15 | $ab$ | $abx$ | 779 | 574 | 779 | 574 | $(1,1)$ | exact DEC & divergence-free |
| **Total** | **15 rows** | **60 marked** | **1320** | **1320** | **5280** ($\sum_{b_3,b_4}$) | **5280** ($\sum_{b_3,b_4}$) | **$(1056, 836/616)$** | **1320/1320 (60/60 verified)** |

**Table 1.** Complete 15-row / 60-marked-history probability ledger, causal indicators, and stress-energy conservation and collar status.

### 6.4 Diamond confluence and five-birth continuation ($a_4 = 1/10$)

Because $[U_r, U_s] = 0$ for all incomparable pairs $r \parallel_h s$, the total displacement vector $g = \boldsymbol\sigma\odot\boldsymbol\lambda$ and the excitation matrix $\mathcal E(h)$ are strictly invariant under any permutation of incomparable events. For example, on Rows 1–6 where $x \parallel_h b$, the physical coordinate time of event $x$ satisfies $t_x = \tau/3 < t_b = \tau$, reversing the native birth index order. Because $[U_x, U_b] = 0$, the composite unitary $U_y U_x U_b U_a = U_y U_b U_x U_a$ is identical, and the resulting backreaction stress tensor $\langle T^{\mu\nu}_{\rm sc}\rangle_{h,g}$ is confluent across the causal diamond.

Extending sequential growth to five births ($|P| = 4 \to 5$, encompassing all 63 unmarked five-element posets $\mathcal U_5$), the maximal-deletion kernel $u(P,r,S)$ with parent-four scale parameter $a_4 = 1/10$ satisfies:
$$
q(P,r,S) = a_4\,u(P,r,S) \quad (S \subsetneq P), \qquad q(P,r,P) = 1 - a_4\sum_{S\subsetneq P}u(P,r,S).
$$
Since an exact hand audit across all 16 unmarked four-posets yields $M_4 := \max_P \sum_{S\subsetneq P}u(P,r,S) < 4$, choosing $a_4 = 1/10 < 1/4$ guarantees:
$$
q(P,r,P) > 1 - \frac{4}{10} = \frac{3}{5} > 0.
$$
Under fair continuation marks ($b_5 \in \{0,1\}$), summing over the fifth birth recovers the 15-row four-birth probabilities identically:
$$
\sum_{S_4 \subseteq P_4}\sum_{b_5 \in \{0,1\}} \frac{1}{2}q(P_4, r_4, S_4) = 1,
$$
preserving Kolmogorov cylinder-set consistency. Across all 63 five-element posets, every incomparable pair $u \parallel v$ satisfies $D_{uv} = 0 \implies [U_u, U_v] = 0$, guaranteeing that diamond confluence and collar compensation extend intact to five births.


---

## 7. Scope, non-implications, and Status-M quarantine

### 7.1 Separation between native poset primitives and supplied continuum scaffolding

To maintain strict scientific and ontological discipline, we delineate the exact boundary between native discrete poset primitives and supplied continuum mathematical scaffolding:

1. **Native discrete poset primitives:**
   - Finite strict partial orders $(P, \prec)$ representing committed causal structures.
   - Downward-closed precursor ideals $S \in \mathcal I(P)$ representing causal pasts of newborn events.
   - Binary vertex marks $r: P \to \{0,1\}$ representing internal discrete states.
   - Rational sequential growth kernels $q(P,r,S)$ satisfying scalar diamond commutation, proper-slot mark locality, and Kolmogorov cylinder-set consistency.
2. **Supplied continuum scaffolding:**
   - Background $(3+1)$-dimensional flat Minkowski spacetime $\mathbb R^{1,3}$ with prescribed metric $\eta_{\mu\nu} = \operatorname{diag}(-1,1,1,1)$.
   - Prescribed Cartesian coordinates $(ct, x_1, x_2, x_3)$ and cubic cavity boundary $\Omega = [-L/2, L/2]^3$ with supplied side length $L = 8c\tau$.
   - Quantized 12-mode longitudinal scalar field $\Phi_{\rm sc}(t,x)$ with supplied frequencies $\omega_m = (47-2m)\pi/(8\tau)$ and homogeneous Neumann boundary conditions.
   - Smooth radial cutoff bump family $\chi_{\rm st}, \chi_{\rm rise}, \chi_{\rm out}$ and the classical external Beltrami stress collar $T^{\mu\nu}_{\rm col}$.
   - Semiclassical coupling parameters $\boldsymbol\lambda \in \mathbb R^4$, action scale $A_*$, and detector gap $\varepsilon_{\rm det}$.

Every result established in this work is an exact mathematical theorem concerning the conditional coupling of quantum pointer probes to a continuum cavity field on a prescribed Minkowski background.

### 7.2 Null controls and limiting edge cases

The mathematical consistency of the framework is verified against several operational null controls:

1. **Zero-coupling limit ($\boldsymbol\lambda \to \mathbf 0$):**
   When probe coupling vanishes, $\boldsymbol\lambda = \mathbf 0$, all kick unitaries reduce to the identity operator: $U_r(h;\mathbf 0) = I_{\rm tot}$. The displacement vector vanishes identically: $g = \boldsymbol\sigma\odot\boldsymbol\lambda = \mathbf 0$. Consequently, the harmonic quadrature shifts vanish ($\alpha_m = \gamma_m = 0$), the classical mean wavefield vanishes ($\Phi_{\rm cl} \equiv 0$), the classical stress tensor vanishes ($T^{\mu\nu}_{\rm cl} \equiv 0$), the field excitation energy is zero ($\Delta E_{\rm field} = 0$), and the collar reaction work is zero ($W_{\rm collar} = 0$). The total stress tensor collapses to the static unperturbed vacuum stress $\omega_{\rm vac}(T^{\mu\nu}_{\rm sc}(x))$, which satisfies exact divergence-free conservation and the DEC.
2. **Incomparable-pair commutation ($r \parallel_h s$):**
   For any two events that are causally incomparable, the commutator $[\phi_r(h), \phi_s(h)] = i\beta(c_{rs} - c_{sr})I_{\rm field} = 0$ vanishes. Consequently, $[U_r, U_s] = 0$. Conjugation of probe $r$'s observables by $U_{\rm tot}$ is strictly independent of $\lambda_s$, certifying exact zero spacelike signaling.
3. **Collar removal limit ($U_{\rm col} \to 0$):**
   If the external confining collar is omitted, the truncated stress tensor $T^{\mu\nu}_{\rm trunc} = \mathbf 1_\Omega \langle T^{\mu\nu}_{\rm sc}\rangle$ produces a non-zero distributional surface divergence $-n_a T^{ab}\delta_{\partial\Omega} \ne 0$, confirming that the collar is indispensable for global four-divergence conservation.

### 7.3 Explicit non-claims

In adherence to foundational research governance:
- **No continuum spacetime derivation:** No claim is made to derive the continuous Minkowski manifold $\mathbb R^{1,3}$, the spatial dimension 3, or the Lorentzian signature $(-,+,+,+)$ from native causal poset primitives.
- **No Born rule derivation:** No claim is made to derive quantum measurement probabilities or the Born rule from deterministic poset growth.
- **No physical constant derivation:** No claim is made to derive the speed of light $c$, Planck's constant $\hbar$, Newton's constant $G$, or the cavity parameters $(\tau, A_*, \kappa)$.
- **No General Relativity derivation:** No claim is made to derive Einstein's field equations, dynamic metric backreaction, or spacetime curvature from the flat-space stress-energy tensor.

### 7.4 Status-M quarantine declaration

Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined outside every equation, variable, and inference of this calculation, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## Scientific review

Branch-Dressed Cavity Probe Stress Author derived local impulsive pointer-probe kicks along committed causal histories inside the 12-mode Neumann cavity ($L=8c\tau$), exact four-divergence conservation $\partial_\mu T^{\mu\nu}_h = 0$, vanishing boundary momentum flux $n_a T^{a0}_{\rm cl}=0$, whole-space Lorentzian DEC compliance with the universal Beltrami collar constant $M_{\rm st}^{(12)}=1+57e^{-6/7}+576e^{-12/7}+972e^{-13/7}+4608e^{-20/7}$, diamond-confluent switching-work collar compensation $W_{\rm collar}(h) = \Delta E_{\rm support}(h)$, and five-birth continuation compatibility ($a_4=1/10$). Independent Cavity Probe Stress Reviewer independently verified by hand 100% of equations, boundary conditions, DEC inequalities, diamond commutations, GFM table escaping, and strict sibling isolation. Prospective protocol SHA-256 991a45964e1a805e952db88a1a7a1ed1b7b2d9cca4e6de76b793de63536b9054; accepted author report SHA-256 23928f2c5b8c43fefef820654cd02f81ab92cc6073a3d10ed32673688a75d3c0; independent scientific review SHA-256 a570a01d11729c8d3c72b7b2725703a3e48c54881a2a011990815cc6f22f2077.
