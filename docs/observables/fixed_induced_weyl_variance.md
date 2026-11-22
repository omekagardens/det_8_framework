# Fixed induced electric-Weyl mean and ordinary variance

**Accepted conditional mathematical result.** The fixed curvature-projected state action has the prescribed iterated full-Fock norm limit, and its selected equation residual vanishes in that same order. Its mean is exactly zero and its ordinary connected variance is finite and strictly positive:
\[
\boxed{\mu_Q=0,\qquad
0<\mathcal V_Q\le\gamma^2\left[
\frac{9\pi^3\alpha}{\lambda^6}
\left(b+\frac{2\sqrt{2/\pi}}{\lambda}\right)
+\frac{81\pi^2}{140}\right],}
\]
\[
\alpha=\frac{5\pi}{4},\quad b=\frac{21\pi}{16},\quad
\lambda=\frac{\ell}{c\tau},\quad
\gamma=\frac{GA_*\lambda^2}{\pi^2c^5\tau^2}.               \tag{1}
\]
An exact convergent integral for this variance is given below. The upper bound is deliberately finite rather than sharp; no numerical value, negligibility or gravity-adequacy threshold is inferred.

The result is conditional on the supplied field, flat geometry and leading induced gravitational response defined below. Finite frequency and Abel regulators first give a well-defined action between the needed finite-particle sectors. The proved infinite-regulator statement is only the strictly ordered state-vector limit: remove the frequency cutoff at each fixed positive Abel regulator, then remove the Abel regulator. No finite test, joint limiting path, operator self-adjointness or empirical measurement claim is substituted for that statement.

Original distinct scientific review returned **PASS_SCOPED**, and the coordinator admitted the result **ACCEPT_WITH_SCOPE** on 20 November 2026. This article assembles that accepted result and its existing proof; it introduces no new theorem or scientific review.

## 1. Supplied model and fixed functional

The supplied carrier is the full symmetric Fock space over \(L^2(\mathbb R^3,d^3k)\), with vacuum \(\Omega\), annihilation anti-linear in its test function, and \([a(u),a^\dagger(v)]=\langle u,v\rangle\), where the inner product is anti-linear in its first argument. The dispersion and energy are supplied as \(\omega_k=c|k|\) and \(H=A_*d\Gamma(\omega)\). All \(c,\tau,A_*,\kappa,G\) are positive supplied constants.

The fixed input is the normalized real radial cosine-shell state \(|h_*\rangle=a^\dagger(h_*)\Omega\). Its center is \(\omega_1=5\pi/(4\tau)\), and its half-bandwidth is \(\delta_*=\pi/(16\tau)\). Explicitly, \(h_*(k)=(c\tau)^{3/2}g(c\tau k)\), with the complete dimensionless packet \(g\) given in (13). The same packet, including its shell edges, is used throughout.

With \(X^0=ct\), \(\eta=\operatorname{diag}(-1,1,1,1)\), the field normalization is
\[
\Psi(X)=\frac{C}{(2\pi)^{3/2}}\int
\frac{a(k)e^{-i\omega_kt+ik\cdot x}
+a^\dagger(k)e^{i\omega_kt-ik\cdot x}}{\sqrt{\omega_k}}\,d^3k,
\qquad C=\sqrt{\frac{A_*c^2}{2\kappa}}.
\]
Insert the same \(\chi_\Lambda(k)=1_{\{\omega_k\le\Lambda\}}\) into every field factor. The lower-index minimal source is exactly
\[
\mathsf T_{\mu\nu,\Lambda}
=\kappa:\left[
\partial_{(\mu}\Psi_\Lambda\partial_{\nu)}\Psi_\Lambda
-\tfrac12\eta_{\mu\nu}\partial_\alpha\Psi_\Lambda
\partial^\alpha\Psi_\Lambda\right]:_\Omega .
                                                               \tag{2}
\]
Parentheses include the factor \(1/2\). There is no improvement or further subtraction. Its trace reversal simplifies, as a finite-cutoff Wick identity, to
\[
S_{\mu\nu,\Lambda}
=\mathsf T_{\mu\nu,\Lambda}
-\tfrac12\eta_{\mu\nu}\operatorname{tr}\mathsf T_\Lambda
=\kappa:\partial_{(\mu}\Psi_\Lambda\partial_{\nu)}\Psi_\Lambda: .
                                                               \tag{3}
\]

The fixed energy-radius input \(\ell=c\tau\lambda\) is specified by
\[
\lambda^2=64+\frac4{5\pi^2}
\int_{-1}^1\frac{\cos^2(\pi y/2)}{1-y^2/400}\,dy.
                                                               \tag{4}
\]
Retain \(g_\tau(t)=e^{-t^2/(2\tau^2)}/(\sqrt{2\pi}\tau)\) and the **normalized** spatial test
\(W_\ell(x)=e^{-|x|^2/(2\ell^2)}/[(2\pi)^{3/2}\ell^3]\), both centered at zero. With \(e^{ij}=\operatorname{diag}(1,-1,0)/\sqrt2\), set
\[
\mathcal W[h]=e^{ij}C^{(1)}_{0i0j}[h],\qquad
f(X)=\ell^2g_\tau(X^0/c)W_\ell(x)/c .
\]
The registered Riemann sign is
\[
R^{(1)}_{\alpha\beta\gamma\delta}[h]=\tfrac12(
\partial_\gamma\partial_\beta h_{\alpha\delta}
+\partial_\delta\partial_\alpha h_{\beta\gamma}
-\partial_\delta\partial_\beta h_{\alpha\gamma}
-\partial_\gamma\partial_\alpha h_{\beta\delta}),
                                                               \tag{5}
\]
with \(R^{(1)}_{\beta\delta}=\eta^{\alpha\gamma}R^{(1)}_{\alpha\beta\gamma\delta}\). For this tracefree spatial \(e\), the four-dimensional Weyl subtraction gives the explicit projection
\[
\mathcal W[h]=e^{ij}R^{(1)}_{0i0j}[h]+\tfrac12e^{ij}R^{(1)}_{ij}[h].
\]
This formula fixes the curvature functional without requiring any unlisted Weyl convention.

The response uses \(\Box=-\partial_0^2+\Delta\), \(\Box D_{\rm ret}=\delta^{(4)}\), retarded support and no homogeneous addition:
\[
D_{{\rm ret},\varepsilon}(X)
=e^{-\varepsilon X^0/(c\tau)}D_{\rm ret}(X),\qquad
h_{\mu\nu,\Lambda,\varepsilon}
=-\frac{16\pi G}{c^4}D_{{\rm ret},\varepsilon}*S_{\mu\nu,\Lambda}.
                                                               \tag{6}
\]
Convolution is in \(d^4Y\). Equation (6) is precisely the trace reversal of the registered response to \(\mathsf T\). At finite \(\varepsilon>0\) the damped distribution is not the original \(\Box\) inverse.

The only moment target and internal equation check are
\[
Q_{\Lambda,\varepsilon}=\int d^4X\,f\,\mathcal W[h_{\Lambda,\varepsilon}],
\]
\[
B_{\Lambda,\varepsilon}=\int d^4X\left[
(\Box f)\mathcal W[h_{\Lambda,\varepsilon}]
+\frac{16\pi G}{c^4}f\,\mathcal W[S_\Lambda]\right].        \tag{7}
\]
Here \(Q\) is dimensionless. The auxiliary \(B\) tests the selected projected equation; it is not another statistic.

## 2. Finite-regulator construction, conservation and gauge identity

For finite \(\Lambda\), every field derivative has an \(L^2\) one-particle kernel with all required momentum moments. The undifferentiated squared radial weight at zero is proportional to \(\omega\,d\omega\); derivatives add powers rather than an infrared singularity. Momentum support is bounded above. Creation/annihilation estimates therefore make each Wick tensor and its required derivatives bounded between the relevant fixed particle sectors, uniformly in spacetime, on the algebraic finite-particle domain with arbitrary \(L^2\) symmetric sector wavefunctions.

For \(a_\varepsilon=\varepsilon/(c\tau)>0\), the response distribution is the signed cone measure
\[
D_{{\rm ret},\varepsilon}(X)
=-\frac{e^{-a_\varepsilon X^0}\delta(X^0-|x|)}{4\pi|x|},
\qquad
\|D_{{\rm ret},\varepsilon}\|_{\rm TV}
=\int_0^\infty R e^{-a_\varepsilon R}\,dR=a_\varepsilon^{-2}.
                                                               \tag{8}
\]
Thus (6) is a Bochner state-action integral at finite regulators. Derivatives can act on the cutoff source; their uniform sector bounds and (8) justify differentiation under the integral. The Gaussian tests \(f,\Box f\) and all their required derivatives are integrable. This constructs (7) on the finite-particle domain.

The cutoff field still satisfies the massless wave equation. Differentiating the symmetrized Wick products in (2), the product-rule terms cancel, leaving a symmetrized term proportional to \(\Box\Psi_\Lambda\). Therefore
\(\partial^\mu\mathsf T_{\mu\nu,\Lambda}=0\) there. Normal ordering commutes with these finite-cutoff derivatives. This is conservation of the full tensor, not an inference from its mean or only \(T^{00}\).

For \(h_{\mu\nu}=\partial_\mu\xi_\nu+\partial_\nu\xi_\mu\), commuting derivatives in (5) cancels its terms. Ricci and Weyl contractions then also vanish, giving the registered flat-background linear gauge identity. These statements concern the finite construction and the specified curvature functional. No complete limiting metric is needed.

At finite regulators, bounded source/response derivatives and Schwartz decay of \(f\) justify the integrations by parts in (7). In particular, moving \(\Box\) onto \(f\) has no omitted boundary term. Subsequent removal of regulators is justified below by state-vector estimates, not by formal pointwise limiting fields.

## 3. Exact tensor cancellation at the massless light cone

Use dimensionless momenta \(q=c\tau k,\ p=c\tau k'\), write
\[
r=|q|,\quad s=|p|,\quad
d=rs-q\cdot p,\quad v=sq-rp,\quad
a=(-r,q),\quad b_4=(-s,p),
\]
where \(a,b_4\) are lower-index null covectors. Let
\(J_{\mu\nu}=a_\mu b_{4,\nu}+b_{4,\mu}a_\nu\).
The channel sign \(\sigma=+1\) denotes a pair and \(-1\) a number exchange, with wave covector \(K=a+\sigma b_4\) up to its overall sign. Its wave eigenvalue is
\[
D_0=-K^\mu K_\mu=2\sigma d .
\]

For the plane tensor \(J\), direct substitution in (5) gives
\[
R^{(1)}_{0i0j}[J]=-\sigma v_iv_j,\qquad
R^{(1)}_{ij}[J]=\tfrac12 K^\mu K_\mu J_{ij}
=-\sigma d J_{ij}.                                      \tag{9}
\]
For the Ricci identity, \(K^\alpha J_{\alpha\nu}=-dK_\nu\) and \(\operatorname{tr}J=-2d\) cancel the two longitudinal contributions. Tracefreeness of \(e\) gives
\(\mathcal W[J]=e^{ij}R_{0i0j}^{(1)}+\tfrac12e^{ij}R_{ij}^{(1)}\). Hence
\[
\boxed{\mathcal W[J]=-D_0\,T_e(q,p),\qquad
T_e(q,p)=\frac{e^{ij}v_iv_j}{2d}+\frac{e^{ij}q_ip_j}{2}.} \tag{10}
\]
For \(d>0\),
\[
|v|^2=2rsd,\qquad \|e\|_{\rm op}=1/\sqrt2,\qquad
|T_e(q,p)|\le\frac{3rs}{2\sqrt2}.                         \tag{11}
\]
Define \(T_e=0\) on the exceptional set \(d=0\), including zero momenta. For nonzero momenta this means parallel spatial directions, equivalently collinear future null covectors; it does not include the antiparallel witness used below, where \(d=2\). This is a measure-zero set, so the representative changes no Lebesgue kernel or state action. This wording incorporates the original review’s accepted terminology clarification. The cancellation is a tensor identity for this projected response, not a finite-part subtraction at a pole.

For actual dimensionless temporal frequency \(\nu\) and spatial wavevector \(K_{\rm sp}\), the Abel multiplier is
\[
D_\varepsilon=(\nu+i\varepsilon)^2-|K_{\rm sp}|^2,\qquad
\rho_\varepsilon=\frac{D_0}{D_\varepsilon},
\quad D_0=\nu^2-|K_{\rm sp}|^2 .
\]
It is nonsingular for real \(\nu,K_{\rm sp}\) when \(\varepsilon>0\), and
\[
|D_\varepsilon|^2-D_0^2
=\varepsilon^4+2\varepsilon^2(\nu^2+|K_{\rm sp}|^2)\ge0.
\]
Consequently
\[
|\rho_\varepsilon|\le1,\qquad
\rho_\varepsilon\longrightarrow1\quad(d>0).              \tag{12}
\]
This bounded factor is the reason the curvature action can converge without positing convergence of the complete metric response.

## 4. Normalization, full-Fock action and the ordered limits

The unitary rescaling \(Uf(q)=(c\tau)^{-3/2}f(q/(c\tau))\) takes the packet to
\[
g(q)=\frac{\cos[\pi(|q|-\alpha)/(2\delta_0)]}
{\sqrt{4\pi\delta_0}\,|q|}
1_{\{||q|-\alpha|<\delta_0\}},\qquad
\delta_0=\pi/16,\quad \alpha=5\pi/4.                     \tag{13}
\]
It is real, radial and normalized, with
\(\int r|g(q)|^2dq=\alpha\) and support below \(b=21\pi/16\).
The following Fock formulas use the induced unitary rescaling on every particle sector.

For physical future null covectors \(\widetilde a=(-\omega_k/c,k)\) and \(\widetilde b=(-\omega_{k'}/c,k')\), the number coefficient of \(S\) is
\[
\frac{A_*c^2}{2(2\pi)^3\sqrt{\omega_k\omega_{k'}}}
(\widetilde a_\mu\widetilde b_\nu+
\widetilde b_\mu\widetilde a_\nu).
\]
In the half-pair convention the pair-creation coefficient is its negative. The full \(T\) coefficient has the additional term
\(-\eta_{\mu\nu}\widetilde a\cdot\widetilde b\), removed by trace reversal. This follows directly from both mixed derivative products in the number term and both equal-orientation derivatives in a pair.

The normalized test contributes
\(\exp[-(\nu^2+\lambda^2|K_{\rm sp}|^2)/2]\), with **no spatial volume factor**. Combining this, the coupling, \(\ell^2\), (10), and the unitary rescaling gives the dimensionless prefactor \(\gamma\) in (1). The limiting unscaled kernels are
\[
n(q,p)=\frac{T_e(q,p)}{\sqrt{rs}}
e^{-[(r-s)^2+\lambda^2|q-p|^2]/2},
\qquad
p_2(q,p)=-\frac{T_e(q,p)}{\sqrt{rs}}
e^{-[(r+s)^2+\lambda^2|q+p|^2]/2}.                        \tag{14}
\]
The subscript distinguishes the pair kernel from a momentum variable.

At finite \(\varepsilon\), multiply \(\gamma n\) by \(\rho_{-,\varepsilon}\), using
\(\nu=s-r,\ K_{\rm sp}=p-q,\ D_0=-2d\), and multiply \(\gamma p_2\) by \(\rho_{+,\varepsilon}\), using
\(\nu=-(r+s),\ K_{\rm sp}=-(q+p),\ D_0=2d\).
Call these kernels \(N_\varepsilon,P_\varepsilon\). Their cutoff versions have a factor \(1_{\{r\le\Lambda\tau\}}1_{\{s\le\Lambda\tau\}}\).
The number kernel is Hermitian; the pair-creation kernel is complex symmetric, with its complex conjugate in pair annihilation:
\[
Q_{\Lambda,\varepsilon}
=\iint N_{\Lambda,\varepsilon}a^\dagger a
+\tfrac12\iint\left(P_{\Lambda,\varepsilon}a^\dagger a^\dagger+
\overline{P_{\Lambda,\varepsilon}}aa\right).              \tag{15}
\]
Taking a real part of \(\rho_\varepsilon\) before forming the action would change the registered response; it is not done.

With orthogonal symmetrization and normalized symmetric-sector wavefunctions,
\[
Q_{\Lambda,\varepsilon}|g\rangle
=(N_{\Lambda,\varepsilon}g)\ \oplus\
\sqrt{\tfrac32}\operatorname{Sym}(P_{\Lambda,\varepsilon}\otimes g).
                                                               \tag{16}
\]
Only sectors one and three occur. The spectator \(g\) is uncut; pair annihilation kills the one-particle input.

Equations (11)–(12) dominate these kernels by \(3\gamma\sqrt{rs}/(2\sqrt2)\) times their respective Gaussians. The pair squared majorant, after dropping spatial damping, has radial integral proportional to
\[
\int_0^\infty\!\!\int_0^\infty r^3s^3e^{-(r+s)^2}\,dr\,ds<\infty.
\]
The number kernel restricted to the input shell is Hilbert–Schmidt: \(s\) stays in a compact interval away from zero, while its remaining squared radial tail is bounded by a constant times
\(r^3e^{-(r-b)_+^2}\). Both origin and infinity are integrable.

For fixed \(\varepsilon>0\), dominated convergence therefore removes \(\Lambda\) in the pair Hilbert–Schmidt norm and the shell-restricted number norm. Then (12) and the same majorants remove \(\varepsilon\). Symmetrization is a contraction, so these two steps give exactly the prescribed **iterated full-Fock norm limit**
\[
\boxed{\zeta=\gamma(ng)\ \oplus\
\gamma\sqrt{\tfrac32}\operatorname{Sym}(p_2\otimes g).}    \tag{17}
\]
No joint path, interchange of limits or input-sector projection is used.

## 5. Exact projected equation residual

Restore physical inverse-length-squared eigenvalues
\(\widehat D_0=D_0/(c\tau)^2\) and
\(\widehat D_\varepsilon=D_\varepsilon/(c\tau)^2\).
For one plane tensor source coefficient, write \(g_E=16\pi G/c^4\). Its response is \(-g_E\mathcal W(S)/\widehat D_\varepsilon\). Since \(\Box\) has eigenvalue \(\widehat D_0\), the corresponding term in (7) is
\[
\widehat D_0Q+g_E\mathcal W(S)
=g_E\mathcal W(S)(1-\rho_\varepsilon).
                                                               \tag{18}
\]
Equivalently, multiply each unregulated response kernel \(N_0=\gamma n\) or \(P_0=\gamma p_2\) by
\(-D_0(1-\rho_\varepsilon)/(c\tau)^2\), using its own channel frequency and cutoff factors. This multiplier tends to zero almost everywhere and is bounded by
\[
\frac{2|D_0|}{(c\tau)^2},\qquad |D_0|\le(r+s)^2 .
\]
It only adds polynomial powers to the integrable majorants of Section 4. The transform of \(\Box f\) is precisely \(\widehat D_0\) times that of \(f\); the finite-regulator integrations by parts were justified in Section 2. The same number/pair norm estimates first remove \(\Lambda\), and then dominated convergence in \(\varepsilon\) gives
\[
\boxed{\lim_{\varepsilon\downarrow0}
\lim_{\Lambda\to\infty}B_{\Lambda,\varepsilon}|h_*\rangle=0
\quad\hbox{in full-Fock norm}.}                          \tag{19}
\]
This establishes the registered curvature-projected equation check, source conservation and gauge interpretation on the declared test. It does not establish every Einstein constraint, arbitrary-test Lorenz-gauge limits or a complete global metric.

The following moment formula uses these established action and projected-equation prerequisites. A finite variance alone would not establish them.

## 6. Mean, exact variance and strict positivity

The proper rotation \((q_1,q_2,q_3)\mapsto(q_2,q_1,-q_3)\), applied simultaneously to \(q,p\), preserves \(g\), radial cutoffs, both Gaussians and each Abel ratio, while reversing the fixed tensor \(e\). It therefore reverses \(T_e\). The integrable number-channel expectation equals its negative:
\[
\langle g,N_{\Lambda,\varepsilon}g\rangle=0,
\qquad \boxed{\mu_Q=\langle h_*|\zeta\rangle=0}.           \tag{20}
\]
Reality also follows from the Hermitian number kernel.

For \(\Lambda\ge\omega_1+\delta_*\), the finite-cutoff mean stress is exactly the accepted tensor because the cutoff leaves the packet unchanged. Its mean response convolution at fixed \(\varepsilon>0\) and Gaussian pairing are justified by Section 2, so its value equals the same zero in (20). Its prescribed paired limit is zero. Thus the mean agrees with the selected response of the accepted mean source, without asserting that the entire limiting mean metric exists.

The three diagonal and six cross terms in the symmetric three-particle norm give
\[
\left\|\sqrt{\tfrac32}\operatorname{Sym}(p_2\otimes g)\right\|^2
=\tfrac12\|p_2\|_{\rm HS}^2+\|p_2\overline g\|^2.
\]
The packet is real. Define explicit convergent dimensionless integrals
\[
I_N=\int d^3q\left|\int d^3p\,n(q,p)g(p)\right|^2,\quad
I_P=\iint d^3q\,d^3p\,|p_2(q,p)|^2,
\]
\[
I_C=\int d^3q\left|\int d^3p\,p_2(q,p)g(p)\right|^2 .
\]
The one selected connected variance is exactly
\[
\boxed{\mathcal V_Q=\|\zeta\|^2-|\mu_Q|^2
=\gamma^2\left(I_N+\tfrac12 I_P+I_C\right).}               \tag{21}
\]
Every term converges by the already established domain bounds. This is an ordinary norm/second-moment diagnostic of already normal-ordered stress; the vacuum pair term \(I_P/2\) and occupied-state pair term \(I_C\) remain.

For a strict positivity witness inside the momentum integration domain, take \(q=e_1,\ p=-e_1\). Then
\[
d=2,\quad v=2e_1,\quad T_e=\frac1{2\sqrt2},\quad
p_2(q,p)=-\frac{e^{-2}}{2\sqrt2}\ne0.
\]
Here \(d>0\), so continuity gives a nonzero open set of positive six-dimensional measure. Hence \(I_P>0\) and \(\mathcal V_Q>0\). This is a witness in the unrestricted created-pair integration domain, not a change of the input packet or an additional source case.

## 7. Explicit finite analytic bound

Let \(K=3/(2\sqrt2)\), \(C_\lambda=(2\pi)^{3/2}/\lambda^3\), and
\[
G_\lambda(z)=\frac{\lambda^3}{(2\pi)^{3/2}}e^{-\lambda^2|z|^2/2},
\qquad m_\lambda=\frac{2\sqrt{2/\pi}}{\lambda}.
\]
Dropping temporal damping in the number bound, (11) and Cauchy–Schwarz with this normalized Gaussian yield
\[
|ng(q)|^2\le K^2C_\lambda^2\,r
\int G_\lambda(q-p)s|g(p)|^2\,dp .
\]
The Gaussian first radial moment and the triangle inequality give
\(\int |q|G_\lambda(q-p)dq\le s+m_\lambda\). Since \(s\le b\) on the packet and \(\int s|g|^2=\alpha\),
\[
I_N\le\frac{9\pi^3\alpha}{\lambda^6}(b+m_\lambda).         \tag{22}
\]

For pairs, drop only the spatial damping and use (11):
\[
I_P\le16\pi^2\frac98
\int_0^\infty\!\!\int_0^\infty r^3s^3e^{-(r+s)^2}\,dr\,ds.
\]
The substitution \(R=r+s,\ u=r/R\) gives the radial integral
\[
\left(\int_0^1u^3(1-u)^3du\right)
\left(\int_0^\infty R^7e^{-R^2}dR\right)
=\frac1{140}\,3.
\]
Therefore
\[
I_P\le\frac{27\pi^2}{70},\qquad I_C\le I_P,\qquad
\tfrac12I_P+I_C\le\frac{81\pi^2}{140}.                   \tag{23}
\]
The contraction bound uses \(\|g\|=1\). Equations (21)–(23) prove (1). These are analytic inequalities and elementary Gaussian/Beta integrals, not numerical quadrature. No threshold, scan or second statistic was introduced.

## 8. Interpretation and limits of the result

The selected induced curvature average has zero mean but nonzero finite ordinary fluctuations. Replacing its quantum source by the deterministic mean therefore omits this positive connected moment within the supplied leading response model. The earlier energy relative-variance bound is not propagated or reused as a gravitational adequacy criterion.

Only the specified projected action and equation test have been established. No complete metric limit, full Einstein constraints/evolution, limiting self-adjoint observable, \(D(Q^2)\), spectral measurement law, intrinsic gravitational noise, matter response, gravitational counterterms or nonlinear backreaction is constructed. The supplied Gaussian is noncompact in past/future/space, frame-fixed and samples matter as well as vacuum. No detector, preparation, calibration or empirical claim follows.

The flat metric, Fock/Hilbert carrier, amplitudes, dispersion, coupling and dimensional constants remain inputs. Their cancellation or appearance in \(\gamma\) does not produce DET-native \(F\) or \(L\), native mass/action units, a new physical law, Status-M promotion or revival of retired gravity proposals. Original conditional structural/marked-quarter weights are unchanged, and unattached histories are not assigned zero energy or noise.

The finite-regulator constructions, cancellation, ordered norm convergence, residual, zero mean, positivity and bound are proved statements within this supplied model. The mathematical review found no unresolved premise for this fixed registered result. The existence and physical suitability of the supplied continuum field, geometry, response law and constants remain assumptions; no detector or empirical applicability has been established. In particular, the symbol \(Q\) labels the regulated functional and its limiting action on the one selected state. It does not designate a constructed limiting self-adjoint observable or establish \(h_*\in D(Q^2)\).

## 9. Provenance and exact source identities

This article uses the frozen QR author result, the original distinct Relational State scientific review and the coordinator’s scoped admission. The prior continuum packet, local mean stress/energy radius and full-Fock source-energy proofs are reused only within the dependency scope already checked by that review; the concrete model and kernels needed for this result are stated above. No PIM or other-lane result supplies a new premise. The registered order remains fixed: construct the action and prove its ordered limit and projected residual before using the moment formula. The existing review supports the saved artifact and documented phase order, rather than claiming knowledge of every internal reasoning step.

Source identifiers below are relative to the DET review-evidence archive. SHA-256 hashes identify the exact reviewed versions; hashes do not establish mathematical truth.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `qr-continuum-induced-weyl-20261119/CONTROL.json` | 27175 | `32d878941ab8ce355756f22004db79189c9f6f3dbffb13d71565c6730906b0ed` |
| `qr-continuum-induced-weyl-20261119/REPORT.md` | 21612 | `97dfcfd18cd52277ce86429ff7cef34b5c85990835d47266b1af9983a3f87a05` |
| `qr-continuum-induced-weyl-20261119/MANIFEST.json` | 16190 | `29d8b1c97e4d39c5399c7091ba01959867ea47243d0323b5f699a362e214d16d` |
| `qr-continuum-induced-weyl-review-20261119/REVIEW.md` | 13893 | `348006d9094fe892df8680870773af4432a6b92159f6550521c80fa351e2da6d` |
| `qr-continuum-induced-weyl-review-20261119/MANIFEST.json` | 27104 | `974833128a398b508f9e8c2101f22ed4f2e65b5498a81b736fd38662e576019a` |
| `followthrough-0054-20261120/QR_WEYL_RESULT_DISPOSITION.json` | 10569 | `92981fdb18af61bc97fd76ab937a1d3964a88800ddaca538f67223e9fd300cae` |

Authorship: DET Quantum Relativity. Original distinct scientific review: DET Relational State Research. Scientific admission: coordinator, 20 November 2026. This public article is a faithful assembly of that admission; publication assembly review is separate from the reused scientific review.
