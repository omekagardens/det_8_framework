# Obstruction to an isolated stationary scalar source

The accepted two-mode stationary field has no nonzero free realization on all of flat $\mathbb R^3$ in the stipulated smooth $H^1$ profile class while preserving its exact all-time generator, local operator samples and unshifted scalar energy. The generator and wave equation alone force every profile to vanish. That zero field then contradicts both the required sample and positive Hamiltonian.

This is an obstruction for one exact conditional realization class. The accepted [periodic scalar source](local_scalar_source_for_four_chain_field.md) remains valid within its separate scope. No physical rest mass, gravitational field, native unit calibration or general exclusion of DET follows.

## The retained state and realization problem

The [stationary construction](stationary_dynamics_for_four_chain_fields.md) supplies two canonical pairs on $\mathcal H=L^2(\mathbb R^2)$, the common invariant Schwartz core $\mathcal S(\mathbb R^2)$, and the normalized centered product Gaussian with symmetrized quadrature covariance $I_4/2$. Oscillator coordinates are distinct from the spatial coordinate $x\in\mathbb R^3$. Retain
$$
[Q_j,P_k]=i\delta_{jk}I,\qquad
\theta_1=\frac{5\pi}{4},\quad\theta_2=\frac{7\pi}{4},\quad
\omega_j=\frac{\theta_j}{\tau},
$$
$$
K=\frac12\sum_{j=1}^2\theta_j(Q_j^2+P_j^2),\qquad
H_0=\frac{A_*}{\tau}K
=\frac{A_*}{2}\sum_j\omega_j(Q_j^2+P_j^2).
$$
No frequency alias or additive energy shift is permitted. This is the accepted changed-prefix attachment on the supported four-chain, with original source-conditioned structural weights $779/1320$ and $574/1320$, and one quarter of the respective weight for each marked instance. Selection does not renormalize the chain to probability one or provide an all-history scalar realization. The separate three-pair Weyl attachment is not a premise.

Supply $c,\tau,A_*,\kappa,\beta>0$: propagation speed, duration per tick, action reference, kinetic-density normalization and commutator normalization. Supply flat spacetime with spatial domain $\mathbb R^3$, without periodic identification, wall, potential, material support or forcing. The retained free massless action is
$$
\mathcal S_{\rm sc}=\frac{\kappa}{2}\int dt\,d^3x
\left[c^{-2}(\partial_t\Psi)^2-|\nabla\Psi|^2\right].
$$
The candidate profiles are arbitrary real
$$
u_j,v_j\in C^\infty(\mathbb R^3)\cap H^1(\mathbb R^3),\qquad
\Psi(0,x)=\sum_{j=1}^2[u_j(x)Q_j+v_j(x)P_j].
$$
Here $H^1$ is inhomogeneous: the profiles themselves and their weak first derivatives are square-integrable. No compact support, radial symmetry, spatial orthogonality or standing-wave phase restriction is imposed.

For every real $t$, require
$$
\Psi(t,x)=e^{itH_0/A_*}\Psi(0,x)e^{-itH_0/A_*},\qquad
(c^{-2}\partial_t^2-\Delta_x)\Psi=0,
$$
with a coefficientwise distributional wave equation, and the full positive energy-form identity on the common core
$$
H_{\rm sc}(t)=\frac{\kappa}{2}\int_{\mathbb R^3}
\left[c^{-2}(\partial_t\Psi)^2+
\sum_{\ell=1}^3(\partial_\ell\Psi)^2\right]d^3x=H_0.
$$
This requires equality of forms, not just expectations, with all cross terms retained and no vacuum subtraction.

At the one local probe require
$$
\Psi(n\tau,0)=F_*\sum_j a_j
[Q_j\cos(n\theta_j)+P_j\sin(n\theta_j)],\qquad n=0,1,2,3,
$$
where
$$
a_1^2=\frac{\beta}{2}(\sqrt2-1),\qquad
a_2^2=\frac{\beta}{2}(\sqrt2+1),\qquad a_j>0,
$$
$$
F_*=\frac{B_2}{a_2},\qquad
B_2^2=\frac{2A_*c^2}{\kappa V_{\rm ref}\omega_2},\qquad
V_{\rm ref}=(8c\tau)^3.
$$
The reference volume fixes the inherited field normalization; it does not change the integration domain to a torus. All geometry, action and time standards remain supplied.

## From all-time evolution to Helmholtz equations

On finite Hermite vectors, $(Q_j+iP_j)/\sqrt2$ acquires the phase $e^{-i\omega_jt}$ under the stipulated Heisenberg evolution. Its adjoint acquires the conjugate phase. The oscillator group preserves the Schwartz core, giving there
$$
Q_j(t)=Q_j\cos\omega_jt+P_j\sin\omega_jt,\qquad
P_j(t)=P_j\cos\omega_jt-Q_j\sin\omega_jt.
$$
Consequently $\Psi(t,x)=\sum_j[f_j(t,x)Q_j+g_j(t,x)P_j]$, with
$$
f_j=u_j\cos\omega_jt-v_j\sin\omega_jt,\qquad
g_j=u_j\sin\omega_jt+v_j\cos\omega_jt.
$$
Both second time derivatives equal $-\omega_j^2$ times the corresponding coefficient. These coefficients are smooth in time as spatial distributions. Evaluating the coefficientwise wave equation at $t=0$ therefore gives
$$
(\Delta_x+k_j^2)u_j=(\Delta_x+k_j^2)v_j=0,\qquad k_j=\omega_j/c>0.
$$

No intermode cancellation is available. For a vanishing linear combination $L=\sum_j(\alpha_jQ_j+\gamma_jP_j)$ on the invariant core,
$$
[L,P_k]=i\alpha_kI,\qquad [L,Q_k]=-i\gamma_kI,
$$
so all coefficients vanish. Distribution-valued coefficients are first smeared against an arbitrary compactly supported smooth spatial test function. This argument needs neither spatial orthogonality nor a time fit separating the two frequencies.

## The Fourier obstruction

Take any one profile $h$ satisfying $(\Delta+k_j^2)h=0$. Because $h\in L^2$, Plancherel gives an $L^2$ Fourier transform. Distributional Fourier transformation yields
$$
(|\xi|^2-k_j^2)\widehat h(\xi)=0.
$$
For any $\varphi\in C_c^\infty$ supported away from the sphere $\Sigma_j=\{\xi:|\xi|=k_j\}$, the quotient
$$
\chi(\xi)=\frac{\varphi(\xi)}{|\xi|^2-k_j^2}
$$
is a smooth compactly supported test function, extended by zero. Testing with $\chi$ shows $\langle\widehat h,\varphi\rangle=0$. Thus $\widehat h$ vanishes distributionally, hence almost everywhere, off $\Sigma_j$.

The sphere has zero three-dimensional Lebesgue measure. An $L^2$ function supported there must vanish almost everywhere. Plancherel gives $h=0$ in $L^2$; smoothness then gives pointwise vanishing. Applying this to all four profiles proves
$$
\boxed{u_1=v_1=u_2=v_2=0,\qquad\Psi(t,x)=0.}
$$
A nonzero Fourier distribution concentrated on a sphere is not an $L^2$ function. The proof excludes that possibility using the declared profile class, without adding a decay assumption.

## Two contradictions and the full energy audit

Already the $n=0$ operator sample requires $u_j(0)=F_*a_j>0$ and $v_j(0)=0$, contradicting zero profiles. In the fixed Gaussian its required variance is
$$
\left\langle\left(F_*\sum_j a_jQ_j\right)^2\right\rangle
=\frac{F_*^2}{2}(a_1^2+a_2^2)
=\frac{F_*^2\beta}{\sqrt2}>0.
$$
Independently, zero profiles give zero scalar energy, whereas the unshifted Hamiltonian has
$$
\langle H_0\rangle=\frac{A_*}{2}(\omega_1+\omega_2)
=\frac{3\pi A_*}{2\tau}>0.
$$
The Gaussian belongs to the common core, so this vector alone disproves equality of the forms.

The conclusion does not discard energy cross terms. With $R=(Q_1,P_1,Q_2,P_2)^T$ and $a=(f_1,g_1,f_2,g_2)^T$, define
$$
C(t)=\kappa\int_{\mathbb R^3}
\left[c^{-2}\dot a\dot a^T+
\sum_\ell(\partial_\ell a)(\partial_\ell a)^T\right]d^3x.
$$
This real symmetric Gram matrix is positive semidefinite, and its entries are finite by $H^1$, fixed frequencies and Cauchy–Schwarz. For every Schwartz vector $\chi$,
$$
h_{{\rm sc},t}[\chi]=\frac{\kappa}{2}\int
\left[c^{-2}\|\dot a^TR\chi\|^2+
\sum_\ell\|(\partial_\ell a)^TR\chi\|^2\right]d^3x\ge0.
$$
Equivalently, on the core,
$$
H_{\rm sc}=\frac12\sum_{\alpha,\gamma}C_{\alpha\gamma}R_\alpha R_\gamma
=\frac14\sum_{\alpha,\gamma}C_{\alpha\gamma}\{R_\alpha,R_\gamma\}.
$$
Symmetry removes only the antisymmetric commutator contraction. The Gaussian expectation is
$$
\langle H_{\rm sc}\rangle=\frac{\kappa}{4}\sum_j
\left[\frac{\omega_j^2}{c^2}(\|u_j\|_2^2+\|v_j\|_2^2)
+\|\nabla u_j\|_2^2+\|\nabla v_j\|_2^2\right].
$$
The coefficient rotations preserve these paired norms. This audits the original form without replacing its required operator identity. Zero profiles make every entry of $C$ zero; no assumed profile orthogonality or zero-point cancellation is involved.

## Scope and scientific provenance

The decisive premises are exact all-time fixed-frequency dynamics, the free whole-space equation and $L^2$ profiles. Smoothness licenses the point probe. The energy identity, later three samples and particular amplitude magnitudes are unnecessary to force zero and cannot repair that obstruction. Four sampled operators or covariances alone do not imply the all-time evolution used here.

The periodic source has a different spatial spectral problem on a compact domain. Its finite periodic energy is not an isolated whole-carrier mass. Finite-energy wave packets, approximate record matching, nonstationary realizations and confinement or material degrees of freedom are outside this theorem and were not constructed or tested. No boost relation, self-gravitating solution, physical calibration or primitive-only quantum/geometry map follows.

DET Quantum Relativity authored the result; DET Relational State Research supplied the distinct scientific **PASS** review on 17 November 2026 at 01:30:43 UTC. The accepted disposition at 01:37:38.485857 UTC is `ACCEPT_OBSTRUCTION_REJECT_EXACT_SOURCE_CLASS`. This article assembles that accepted proof without extending it. The scientific evidence versions are the 13,221-byte author report, SHA-256 `8507751f8046a5fa2d9ef7775beb9980e4de2ad307cdf769f8c24a2c9dfe4db3`, and the 7,750-byte review, SHA-256 `e3fa2a608db137c77c40ad97eaae38a111a383a92ed082f84e95048609164e29`.

The two linked mathematical inputs retain their exact accepted versions: the 11,034-byte stationary article, SHA-256 `26fe52f17ceba12e7a3dae0eda6a751c931f657c0651ac2b901c56c1574e08f0`, and the 17,746-byte periodic-source article, SHA-256 `9ba0b188035835f22257a7ad842ea6675aeb642a15282d3b09dbd491de325bfb`. The conditional boost, CL112 equilibrium and separate Weyl results supply context only, with no mathematical premise added to this obstruction.
