# Fixed passive TT stress fluctuation and filtered response

**The registered output has strictly positive variance under the supplied Gaussian closure.** The fixed spatial projection gives one quadratic oscillator source; its symmetrized covariance admits an explicit smooth real Gaussian realization. The registered zero-data response and time filter retain that fluctuation. No polarization, phase, frequency, window, filter or source was retuned.

Let
\[
 \mathcal C=
 \frac{A_*(\omega_1\omega_2)^{3/2}}
      {\sqrt2\,V(\omega_1^2+\omega_2^2)}>0,\qquad
 \zeta=\frac{\pi\sqrt{74}}4.
\]
The exact result is
\[
 \boxed{\operatorname{Var}(Y)=
 \left(\frac{256G\mathcal C\tau^2}{175c^2}\right)^2
 \left[74\sin^2\zeta+9(3-4\cos\zeta)^2\right]>0.}            \tag{1}
\]
The deterministic centered expectation-only counterpart has \(Y=0\). Equation (1) distinguishes these two stipulated prescriptions for this one projected output. It is not a result about a self-consistent metric, a physical detector, empirical semiclassical adequacy, native gravitational coupling or mass.

## 1. Accepted source and scope

This result was independently reviewed by DET Relational State Research and accepted within scope by the coordinator. It uses the original published [local scalar source for the four-chain field](local_scalar_source_for_four_chain_field.md) and [stationary dynamics for four-chain fields](stationary_dynamics_for_four_chain_fields.md). These linked articles match the exact frozen source versions used in the calculation. The supplied model, fixed projection, response and filter are retained below.

The model is the original two-pair torus construction, not the later continuum-packet family. Supply \(c,\tau,A_*,\kappa,\beta,G>0\), fixed orthonormal axes, and
\[
 L=8c\tau,\quad V=L^3,\qquad
 k_1=\frac{2\pi}{L}5e_1,\quad k_2=\frac{2\pi}{L}7e_2,\qquad
 \omega_1=\frac{5\pi}{4\tau},\quad\omega_2=\frac{7\pi}{4\tau}.
\]
On \(L^2(\mathbb R^2)\) retain \([Q_j,P_k]=i\delta_{jk}I\), the centered product oscillator ground state \(\Omega\), and the unshifted Hamiltonian
\[
 H_0=\frac12\sum_{j=1}^2 A_*\omega_j(Q_j^2+P_j^2).
\]
The original field and phases are
\[
 \begin{aligned}
 X_j(t)&=Q_j\cos\omega_jt+P_j\sin\omega_jt,\\
 B_j&=\sqrt{\frac{2A_*c^2}{\kappa V\omega_j}},\\
 \varphi_1&=\arccos[(\sqrt2-1)\sqrt{5/7}],\qquad\varphi_2=0,\\
 \alpha_j(x)&=k_j\cdot x+\varphi_j,\qquad
 \Psi(t,x)=\sum_j B_j\cos\alpha_j(x)\,X_j(t).
 \end{aligned}                                             \tag{2}
\]
The symbols \(\varphi_j\) are the original fixed spatial phases; there is no packet bandwidth here.

With \(x^0=ct\) and \(\eta=\operatorname{diag}(-1,1,1,1)\), retain precisely the original Weyl-ordered kinetic tensor
\[
 \mathcal Z=\tfrac12\eta^{\alpha\gamma}
       \{\partial_\alpha\Psi,\partial_\gamma\Psi\},\qquad
 T^{\mu\nu}=\kappa\left[
 \tfrac12\{\partial^\mu\Psi,\partial^\nu\Psi\}
             -\tfrac12\eta^{\mu\nu}\mathcal Z\right].         \tag{3}
\]
There is no normal-order subtraction or alternate stress improvement.

The common Schwartz domain in \(L^2(\mathbb R^2)\) is invariant under the oscillator dynamics and polynomial canonical operators. The fields and stresses, including the degree-four products used in their covariance, act there. The Gaussian vacuum lies in this domain and all required moments are finite. At each fixed time \(X_1\) and \(X_2\) act on separate tensor factors and have strongly commuting self-adjoint closures. The following polynomial identities and contractions therefore have a common specified domain.

The attachment remains conditional on the supported four-chain. Its two native structural probabilities stay \(779/1320\) and \(574/1320\); each of the four fair marked instances has one quarter of the corresponding weight. All other histories and probabilities remain unchanged. Equation (1) is conditional on this supplied attachment, not an all-history variance; histories without that attachment are not silently assigned zero response.

## 2. Fixed projection and its normalization

Put
\[
 p=|k_1|,\quad q=|k_2|,\quad d^2=p^2+q^2,\qquad
 K=k_1+k_2,\quad
 e=(qe_1-pe_2)/d,\quad b=e_3,
\]
\[
 \epsilon_{ij}=(e_ie_j-b_ib_j)/\sqrt2,\qquad
 \chi(x)=\cos(\alpha_1+\alpha_2).
\]
Then \(e,b\) are orthogonal transverse unit vectors, so \(\epsilon\) is symmetric, transverse, trace-free and satisfies \(\epsilon^{ij}\epsilon_{ij}=1\). In particular
\[
 \epsilon_{11}=\frac{q^2}{\sqrt2\,d^2},\quad
 \epsilon_{22}=\frac{p^2}{\sqrt2\,d^2},\quad
 \epsilon_{12}=-\frac{pq}{\sqrt2\,d^2},\quad
 \epsilon_{33}=-\frac1{\sqrt2}.                             \tag{4}
\]
The registered connected projection is
\[
 S(t)=\frac1V\int_{\mathbb T_L^3}
 \chi(x)\epsilon^{ij}
 [T_{ij}(t,x)-\langle T_{ij}(t,x)\rangle_\Omega I]\,d^3x.
                                                               \tag{5}
\]
Because \(K\ne0\) is a reciprocal-lattice vector,
\(V^{-1}\int\chi^2\,d^3x=1/2\). The factor \(1/V\) is thus the stipulated cosine projection, not the extraction of its full cosine-series amplitude. The response \(h\) below uses that same normalization. A hypothetical tensor \(q_{\rm amp}(t)\chi\epsilon_{ij}\) would have projection \(q_{\rm amp}/2\). No such reconstructed metric is required or asserted.

## 3. Exact projected source

At equal time the spatial derivatives are combinations of the commuting \(X_j(t)\). The trace part of (3) drops under \(\epsilon\), leaving
\[
 \epsilon^{ij}T_{ij}
 =\kappa\epsilon^{ij}\partial_i\Psi\,\partial_j\Psi .
\]
Here \(\partial_1\Psi=-B_1p\sin\alpha_1X_1\),
\(\partial_2\Psi=-B_2q\sin\alpha_2X_2\), and
\(\partial_3\Psi=0\). The two pure-mode terms have zero projection against \(\chi\): their spatial Fourier frequencies are zero or \(\pm2k_j\), never \(\pm K\).

For the cross term,
\[
 \sin\alpha_1\sin\alpha_2
  =\tfrac12[\cos(\alpha_1-\alpha_2)-\cos(\alpha_1+\alpha_2)],
 \qquad
 \frac1V\int\chi\sin\alpha_1\sin\alpha_2\,d^3x=-\frac14 .
\]
Combining that factor with both cross indices in the stress gives
\[
 \begin{aligned}
 \frac1V\int\chi\epsilon^{ij}T_{ij}\,d^3x
 &=2\kappa\epsilon_{12}B_1B_2pq(-\tfrac14)\,X_1X_2\\
 &=\mathcal C X_1X_2,
 \end{aligned}
\]
where
\[
 \boxed{
 \mathcal C=\frac{\kappa B_1B_2p^2q^2}{2\sqrt2(p^2+q^2)}
 =\frac{A_*(\omega_1\omega_2)^{3/2}}
       {\sqrt2\,V(\omega_1^2+\omega_2^2)}>0 .}               \tag{6}
\]
The product ground state has \(\langle X_1X_2\rangle_\Omega=0\). Thus the projected mean already vanishes and the registered centered source is exactly
\[
 \boxed{S(t)=\mathcal C X_1(t)X_2(t).}                      \tag{7}
\]
This vanishing projection of the mean does not make the complete stress mean zero. In particular, the original full ground-source energy remains the positive unshifted \(3\pi A_*/(2\tau)\). Centering (5) has not altered it or repaired the torus mean-source obstruction.

## 4. Kernel, positivity and regular Gaussian realization

The ordered oscillator contraction, with the original Heisenberg sign, is
\[
 \langle X_j(t)X_j(s)\rangle_\Omega
       =\tfrac12e^{-i\omega_j(t-s)}.
\]
Cross-mode commutation allows the degree-four product to be grouped by mode, and the product state factorizes. Consequently
\[
 \langle S(t)S(s)\rangle_\Omega
       =\frac{\mathcal C^2}{4}e^{-i\nu(t-s)},\qquad
 \nu=\omega_1+\omega_2=\frac{3\pi}{\tau}.
\]
The specified symmetrized kernel is
\[
 \boxed{N(t,s)=\tfrac12\langle\{S(t),S(s)\}\rangle_\Omega
             =\frac{\mathcal C^2}{4}\cos[\nu(t-s)].}        \tag{8}
\]
It is real and symmetric. For any finite real coefficients \(r_a\) and times \(t_a\),
\[
 \sum_{a,b}r_ar_bN(t_a,t_b)
 =\frac{\mathcal C^2}{4}
 \left[\left(\sum_a r_a\cos\nu t_a\right)^2
       +\left(\sum_a r_a\sin\nu t_a\right)^2\right]\ge0 .
\]
This proves positive semidefiniteness without a numerical kernel check.

Take two independent standard real Gaussian variables \(Z_c,Z_s\) and define
\[
 \boxed{\xi(t)=\frac{\mathcal C}{2}
       [Z_c\cos\nu t+Z_s\sin\nu t].}                       \tag{9}
\]
It has exactly covariance (8) and zero mean. Every sample path is real analytic, so it supplies more than the regularity required for the response and its second-derivative time functional. It has finite moments of every order.

Gaussianity in (9) remains the supplied classical closure. It reproduces the chosen symmetrized second moments; it does not identify the quadratic quantum source with a Gaussian random process, match its higher quantum moments or establish a classical measurement law.

## 5. Unique zero-data causal response

Define
\[
 \gamma=\frac{16\pi G}{c^2},\qquad
 \Omega_K=c|K|=\frac{\pi\sqrt{74}}{4\tau},\qquad
 D=\Omega_K^2-\nu^2=-\frac{35\pi^2}{8\tau^2}<0.
\]
The fixed equation is
\[
 \ddot h+\Omega_K^2 h=\gamma\xi,\qquad h(0)=\dot h(0)=0.
                                                               \tag{10}
\]
For each sample path its unique solution is the causal integral
\[
 h(t)=\frac{\gamma}{\Omega_K}\int_0^t
       \sin[\Omega_K(t-s)]\,\xi(s)\,ds.
\]
Evaluating this integral for (9) gives
\[
 \boxed{
 h(t)=\frac{\gamma\mathcal C}{2D}
 \left[
 Z_c(\cos\nu t-\cos\Omega_Kt)
 +Z_s\left(\sin\nu t-\frac{\nu}{\Omega_K}\sin\Omega_Kt\right)
 \right].}                                                 \tag{11}
\]
The two homogeneous terms enforce both initial conditions. Dropping either would change the requested output. There is no resonance because \(D\ne0\). Direct differentiation checks (10); the difference of any two zero-data solutions solves the homogeneous equation with zero data and hence vanishes.

Let \(r_c(t)=\cos\nu t-\cos\Omega_Kt\) and
\(r_s(t)=\sin\nu t-(\nu/\Omega_K)\sin\Omega_Kt\).
The response has zero mean and covariance
\[
 \mathbb E[h(t)h(s)]
 =\left(\frac{\gamma\mathcal C}{2D}\right)^2
       [r_c(t)r_c(s)+r_s(t)r_s(s)].                         \tag{12}
\]
It need not be stationary despite the stationary forcing covariance. Its sample paths and second derivatives are analytic on the required interval.

## 6. Actual second-derivative filter

Retain exactly
\[
 Y=-\frac{\tau^2}{2}\int_0^\tau
       \frac2\tau\sin^2(\pi t/\tau)\,\ddot h(t)\,dt .        \tag{13}
\]
No integration endpoint or time window has been changed. On writing \(x=t/\tau\), the normalized time weight becomes \(1-\cos(2\pi x)\). Define
\[
 \begin{aligned}
 J_c(z)&=\int_0^1[1-\cos(2\pi x)]\cos(zx)\,dx
       =\frac{4\pi^2\sin z}{z(4\pi^2-z^2)},\\
 J_s(z)&=\int_0^1[1-\cos(2\pi x)]\sin(zx)\,dx
       =\frac{4\pi^2(1-\cos z)}{z(4\pi^2-z^2)} .
 \end{aligned}                                             \tag{14}
\]
These expressions follow from the elementary product-to-sum integrals. Only the following nonsingular arguments are needed:
\[
 a=\nu\tau=3\pi,\qquad
 \zeta=\Omega_K\tau=\frac{\pi\sqrt{74}}4,\qquad
 \zeta^2-a^2=-\frac{35\pi^2}{8},
\]
\[
 J_c(a)=0,\quad J_s(a)=-\frac8{15\pi},\qquad
 J_c(\zeta)=-\frac{32\sin\zeta}{5\zeta},\quad
 J_s(\zeta)=-\frac{32(1-\cos\zeta)}{5\zeta}.                 \tag{15}
\]
In particular (13) acts on the actual second derivative of (11), not on its driving force alone. Substitution gives
\[
 \begin{aligned}
 Y=\frac{\gamma\mathcal C\tau^2}{4(\zeta^2-a^2)}
 \bigl\{&
 [a^2J_c(a)-\zeta^2J_c(\zeta)]Z_c\\
 &+[a^2J_s(a)-a\zeta J_s(\zeta)]Z_s\bigr\}.
 \end{aligned}                                             \tag{16}
\]
Using the fixed values in (15), this simplifies to
\[
 \boxed{
 Y=-\frac{256G\mathcal C\tau^2}{175c^2}
       [\sqrt{74}\sin\zeta\,Z_c+3(3-4\cos\zeta)\,Z_s].}     \tag{17}
\]
The signs in this expression retain both the negative second-derivative prefactor in (13) and the zero-data transients.

## 7. Exact variance and sign

Independence and unit variances of \(Z_c,Z_s\) give
\[
 \mathbb E[Y]=0,\qquad
 \boxed{\operatorname{Var}(Y)=
 \left(\frac{256G\mathcal C\tau^2}{175c^2}\right)^2
       [74\sin^2\zeta+9(3-4\cos\zeta)^2].}                 \tag{18}
\]
The sign requires no numerical approximation. From \(64<74<100\),
\[
 2\pi<\zeta<\frac{5\pi}{2},
\]
so \(\sin\zeta>0\). The first square in (18) is strictly positive, and \(G,\mathcal C,\tau,c\) have the stipulated positive values. Hence the variance is strictly positive for the entire stated positive-parameter family with its fixed frequency ratios. This is an analytic statement for that single registered model, not a parameter sweep.

The centered expectation-only comparator replaces \(S\) by its zero expectation. Under the same equation, initial conditions, projection coordinate and filter, it gives \(\xi=0\), \(h=0\) and \(Y=0\). Both prescriptions have the same output mean, but their output variances differ. This is the finite decision requested by the control.

## 8. Units and interpretation

The coefficient \(\mathcal C\), source \(S\) and classical forcing \(\xi\) have energy-density units. The kernel \(N\) has energy-density squared units. The combination \(\gamma\xi\) has units of inverse time squared, while \(h\) and \(Y\) are dimensionless.

Using only the supplied relations \(V=(8c\tau)^3\) and \(\omega_j=(5,7)\pi/(4\tau)\), the common amplitude in (17) can also be written
\[
 \frac{256G\mathcal C\tau^2}{175c^2}
       =\frac{\pi\sqrt{70}}{5920}\frac{GA_*}{c^5\tau^2}.
                                                               \tag{19}
\]
This makes dimensional consistency explicit. Cancellation of \(\kappa\) follows from the supplied field normalization \(B_j\); the absence of the native sample normalization \(\beta\) does not calibrate the remaining scales or identify native records with physical energy.

The output is a filtered, projection-normalized passive response coordinate. It is not a pointwise metric amplitude or a measured tidal observable. The original flat positive-source reference remains a supplied background, and the mean source has not been removed. No finite-coupling self-consistent geometry, backreaction, full Einstein–Langevin equation or coefficient in a coupled metric-correlation expansion has been established.

The Gaussian closure and the response law are additional premises. The positive variance therefore distinguishes these stipulated models only. It gives no quantum measurement protocol, preparation or resource budget, empirical test, physical calibration, native gravitational coupling or rest-mass derivation. The earlier exact isolated-source obstruction and the accepted continuum-packet theorem remain unchanged. CL114, CL115, PIM and Comp-Sci supply no new premise here.

## 9. Verification and provenance

The source, kernel, Gaussian realization, causal response and variance were derived analytically. Separate author-side checks recalculated the source projection/factors/domain and the response/filter/sign; their formulas agree. These are author-support checks; the completed distinct State scientific result review is separate. No numerical sign inspection, solver, simulation, experiment, additional profile or retuned case was used.

DET Relational State Research accepted this exact result within its stated scope, and the coordinator admitted that result. The review was distinct from authorship and nonblind because the reviewer had previously reviewed the design. The article assembly reuses that completed scientific review and does not add a calculation or case. The mathematical result and all limitations above remain those of the accepted source.

The following byte counts and SHA-256 values identify the accepted archived records. They establish identity, not scientific truth, and are provenance identifiers rather than public reproduction links. The calculation is reproduced above; its original published source dependencies are linked in section 1.

| Archived artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Coordinator scope disposition | 2959 | `104a7a5e3db76dbc33407b8eeb821b04ac8545e6268b64fdc41c48c9102613ed` |
| QR author report | 15411 | `61ca5b50c346f483a46cdc7e3eb636e494010f678906c9d4d77a47882f7cd22b` |
| QR author manifest | 11390 | `d2cb20e639dcd95ee2b61d51d88e091ffa34befe5c3b4da163fa2def4609cf99` |
| Distinct State scientific review | 6795 | `d7d475b377a7478e86b80eab0dab9a2c0ba68e1221b1158d7245687d5d712674` |
| State review manifest | 9594 | `a7dc60de682239d4fd086885e5569a726522b9c08dce1e5c1f34940574446abf` |
