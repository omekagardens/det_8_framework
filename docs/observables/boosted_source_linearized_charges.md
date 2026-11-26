# Linearized initial data and charges of one boosted source

**Accepted conditional mathematics.** Distinct Energy review and coordinator admission establish this result for one fixed prepared source in a supplied linearized initial-data model. The construction below establishes regular fields before evaluating their boundary charges. PIM remains provisional; empirical status: **NOT TESTED**.

## 1. Fixed source and conventions

Use the [continuum cosine-annulus packet](continuum_packet_covariance_and_spread.md) and [minimal local expected stress](local_stress_and_energy_radius.md), with supplied \(c,\tau,A_*,\kappa,G>0\), \(X^0=ct\), metric \(\eta=\operatorname{diag}(-1,1,1,1)\), and
\[
\mathcal K=L^2(\mathbb R^3,d^3k),\qquad
\omega_k=c|k|,\qquad C=\sqrt{\frac{A_*c^2}{2\kappa}}.
\]
The original real normalized seed is
\[
h_*(k)=\sqrt{\frac{c}{4\pi\delta_*}}\,
\frac{\cos[\pi(c|k|-\omega_1)/(2\delta_*)]}{|k|}
\,\mathbf1_{\{|c|k|-\omega_1|<\delta_*\}},
\quad
\omega_1=\frac{5\pi}{4\tau},\quad
\delta_*=\frac{\pi}{16\tau}.
\]
Its zero edge trace and first-derivative jumps are retained.

Fix only \(\theta_0=\log 2\). For the supplied active plus-\(x^1\) scalar boost, let
\[
\phi_\theta(q)=
(\cosh\theta\,q_1+\sinh\theta\,|q|,q_2,q_3),\qquad
f(k)=(U_{\theta_0}h_*)(k)
=\sqrt{\frac{|\phi_{-\theta_0}(k)|}{|k|}}\,
h_*(\phi_{-\theta_0}(k)).
\]
The value at \(k=0\) is immaterial. The sole surface is
\(\Sigma_0:\ X^0=0\). No phase, origin, profile or rapidity is adjusted.

With the unchanged Fourier convention and vacuum subtraction, define
\[
v_f(X)=\frac{C}{(2\pi)^{3/2}}\int
\frac{f(k)}{\sqrt{\omega_k}}e^{-i|k|X^0+ik\cdot x}\,d^3k,
\]
\[
t_f^{\mu\nu}
=2\kappa\operatorname{Re}(\partial^\mu\overline v_f\,\partial^\nu v_f)
-\kappa\eta^{\mu\nu}\partial_\alpha\overline v_f\,\partial^\alpha v_f .
\]
This is the one-particle expected tensor, not a point-stress operator. At \(X^0=0\), write \(w_\mu=\partial_\mu v_f\) and
\[
\rho=t_f^{00}=\kappa\!\left(|w_0|^2+\sum_i|w_i|^2\right),
\qquad
J_i=t_f^{0i}=-2\kappa\operatorname{Re}(\overline w_0w_i).
\]
All momentum components are retained. This source differs from the earlier [radial construction at \(t=\tau\)](linearized_gravity_initial_data.md); the geometry below is not asserted to be a boost of that older solution.

## 2. Source regularity

The fixed boosted packet has compact momentum support separated from zero. For every spatial multi-index \(\alpha\), the Fourier amplitude of \(\partial_x^\alpha w_\mu\) is
\[
C(ik)^\alpha b_\mu(k)\frac{f(k)}{\sqrt{\omega_k}},
\qquad b_0=-i|k|,\quad b_i=ik_i.
\]
The multiplier is bounded on that annulus. It is therefore \(L^2\), and finite support measure also makes it \(L^1\). Fourier differentiation and Plancherel give smooth bounded \(L^2\) derivatives. Their transforms tend to zero: approximate each amplitude in \(L^1\) by smooth compact functions, use integration by parts for those functions, and bound the uniform transform error by the \(L^1\) error.

Thus every \(\partial^\alpha w_\mu\) lies in \(C_0\cap L^\infty\cap L^2\), where \(C_0\) denotes continuous functions vanishing at infinity. Leibniz's rule and Cauchy–Schwarz then establish
\[
\boxed{\partial^\alpha\rho,\ \partial^\alpha J_i
\in L^1\cap C_0\cap L^\infty\quad\text{for every }\alpha.}
\]
No momentum derivative is taken through a packet edge. Neither spatial compact support nor radial tail estimates are assumed.

## 3. Normalized inverse and actual initial data

Supply the formal coefficient ansatz
\[
\gamma_{ij}=\delta_{ij}+\epsilon h_{ij}+\text{formal higher order},
\quad K_{ij}=\epsilon k_{ij}+\text{formal higher order},
\]
\[
h_{ij}=4u\delta_{ij},\qquad
k_{ij}=(LW)_{ij}
=\partial_iW_j+\partial_jW_i-\frac23\delta_{ij}\partial_\ell W_\ell.
\]
Use the supplied sign \(K=-\mathcal L_n\gamma/2\) and fixed-\(G\) equations
\[
\Delta u=-\frac{2\pi G}{c^4}\rho,\qquad
PW:=\Delta W+\frac13\nabla\operatorname{div}W
=\frac{8\pi G}{c^4}J.
\]
The longitudinal restriction is an explicit modelling premise. Seek real smooth fields on all \(\mathbb R^3\), with \(u,W,k\to0\), and no puncture or added homogeneous, transverse-traceless or radiative field.

For \(r=|x|\), set
\[
g=-\frac1{4\pi r},\qquad b=-\frac r{8\pi}.
\]
Small-sphere integration by parts gives \(\Delta g=\delta_0\) and \(\Delta b=g\) in distributions. There is no extra point delta in \(\Delta r=2/r\) or its Hessian. Define
\[
T_{ij}=g\delta_{ij}-\frac14\partial_i\partial_jb
=-\frac1{32\pi}\left(\frac{7\delta_{ij}}r+\frac{x_ix_j}{r^3}\right).
\]
Its normalization follows on all of \(\mathbb R^3\):
\[
\partial_aT_{aj}=\frac34\partial_jg,\qquad
\Delta T_{ij}=\delta_{ij}\delta_0-\frac14\partial_i\partial_jg,
\qquad PT=I\delta_0.
\]
The Hessian terms cancel. The growing auxiliary distribution \(b\) is never convolved with the source.

Construct the ordinary integrals
\[
\boxed{
u(x)=\frac{G}{2c^4}\int\frac{\rho(y)}{|x-y|}\,d^3y,\qquad
W_i(x)=\frac{8\pi G}{c^4}\sum_j\int T_{ij}(x-y)J_j(y)\,d^3y.}
\]
They are absolutely finite: use bounded source and local integrability of the \(r^{-1}\) kernels near the singularity, and bounded kernels against the \(L^1\) source elsewhere.

For regularity, split either kernel with a smooth compact cutoff equal to one near zero. The near kernel is \(L^1\); arbitrary derivatives transfer to the smooth bounded source derivatives, and each convolution is \(C_0\). Every derivative of the far kernel is bounded \(C_0\); differentiation under its \(L^1\) source integral is justified, and compact-source approximation proves decay. Hence \(u,W\) are real smooth functions with all derivatives tending to zero. In particular, \(k=LW\) is smooth, tracefree and tends to zero.

First kernel derivatives have locally integrable order \(r^{-2}\), with no delta term because their small-sphere boundary contribution vanishes. Second derivatives are handled distributionally, not treated as absolutely integrable kernels. Against compact smooth tests, Fubini is justified by the uniformly finite local \(r^{-1}\) integral and the \(L^1\) source. The normalized fundamental identities therefore give the two PDEs distributionally and, by smoothness, pointwise everywhere. Since \(\partial_j(LW)_{ij}=(PW)_i\), both constraints hold, including at the origin.

This establishes actual admissible initial coefficient fields before a boundary functional is evaluated. No pointwise power-law falloff or unrestricted uniqueness theorem is asserted.

## 4. Four boundary charges and their limits

For Euclidean spheres \(S_R=\partial B_R\) with outward normal \(n\), use the fixed-\(G\) coefficient functionals
\[
E_{\rm grav}(R)=\frac{c^4}{16\pi G}
\int_{S_R}(\partial_jh_{ij}-\partial_ih_{jj})n_i\,dS,
\]
\[
P_{{\rm grav},i}(R)=\frac{c^3}{8\pi G}
\int_{S_R}(k_{ij}-\delta_{ij}\operatorname{tr}k)n_j\,dS,
\quad i=1,2,3.
\]
The constructed fields are smooth on each closed ball. Since
\(\partial_jh_{ij}-\partial_ih_{jj}=-8\partial_i u\) and
\(\operatorname{tr}k=0\), the ordinary divergence theorem and the established constraints give
\[
\boxed{
E_{\rm grav}(R)=\int_{B_R}\rho\,d^3x,\qquad
P_{{\rm grav},i}(R)=\frac1c\int_{B_R}J_i\,d^3x,\quad i=1,2,3.}
\]
These are proved identities of the constructed fields, not definitions of their charges. Absolute integrability supplies all four limits:
\[
|E_{\rm grav}-E_{\rm grav}(R)|
\le\int_{|x|>R}\rho\,d^3x\longrightarrow0,
\]
\[
|P_{{\rm grav},i}-P_{{\rm grav},i}(R)|
\le\frac1c\int_{|x|>R}|J_i|\,d^3x\longrightarrow0.
\]
No compact-source substitution, assumed field expansion or discarded lateral spacetime flux is used.

For completeness, the admitted matter comparator uses \(K(k)=(|k|,k)\). The fixed-slice Plancherel identity is
\[
\mathcal P^\mu_{\rm matter}[f]
=\frac1c\int t_f^{\mu0}(0,x)\,d^3x
=A_*\int K^\mu(k)|f(k)|^2\,d^3k.
\]
Under \(k=\phi_{\theta_0}(q)\), the boost Jacobian
\(|\phi_{\theta_0}(q)|/|q|\) cancels the half-density square in \(f\), while \(K(k)=B_{\theta_0}K(q)\). The original radial seed has charge \((E_*/c,0,0,0)\), with \(E_*=A_*\omega_1\). Reusing that accepted comparator yields
\[
\boxed{
(E_{\rm grav}/c,\mathbf P_{\rm grav})
=\mathcal P_{\rm matter}[f]
=\frac{E_*}{c}\left(\frac54,\frac34,0,0\right).}
\]
Thus \(E_{\rm grav}=5E_*/4\), \(P_{{\rm grav},1}=3E_*/(4c)\), and both transverse integrated charges vanish. Local momentum density has not been set to zero. Only the fixed \(\theta_0=\log2\), slice and registered sphere limits are claimed.

## 5. Scope and process qualifications

This is conditional formal linearized initial data, not a nonlinear constraint solution, nonzero-\(\epsilon\) remainder or error estimate, evolution, stability, full spacetime, curved matter conservation or gravitational Lorentz-covariance theorem. The surface functionals are coefficient charges, not a physical ADM measurement or finite-coupling identification. No uniqueness outside the stated claim follows.

Field/Fock structure, dispersion, boost, source identification, longitudinal prescription, geometry, frame, clock and \(c,\tau,A_*,\kappa,G\) remain supplied. Kappa is kinetic normalization. No native units, calibrated mass, physical preparation/detector, coupling calibration, work/heat/funding, memory/reset/reuse or finite apparatus budget is derived. The [spectral-versus-mean mass distinction](spectral_and_mean_four_momentum_mass.md) remains: \(E_{\rm grav}/c^2\) in one frame is not automatically invariant rest mass or particle spectral mass.

The actual post-readout sharp-projection state's \(H^{1/2}\)-form membership and prior band-sign problem remain unresolved. This prepared-source construction assigns neither energy, stress nor geometry to that state. Zero-weight available blocks have no normalized conditional state; unavailable donor records have no target state or energy and are never filled with vacuum or zero. No new donor-to-boost map or pending peer result is adopted.

The distinct review accepted the visible order: saved construction and readback preceded the boundary release, and boundary calculations followed it. The full input-identity audit was recorded after author-adviser dispatch; it is not represented as an earlier audit. A later custody-sentence correction changed no mathematics. Historical timing **ALL_SELECTED_ALGEBRA_AFTER_SAVED_CONTROL_NOT_MET**, interface selection **NOT MET**, repeated-readout control-before-proof failure, gravity documented-process limitations, mass scope adjudication/prior exposure, the later targeted-operator supplement and limited-history qualifications remain unrepaired. The contextual QR guard-inspection incident also remains recorded. No blind-first-exposure, all-private-reasoning or retrospective clean-process certificate is claimed.

The result passed its original distinct Energy review and coordinator admission. This article condenses that accepted proof without a new scientific run, source, parameter or claim; publication does not add empirical acceptance.
