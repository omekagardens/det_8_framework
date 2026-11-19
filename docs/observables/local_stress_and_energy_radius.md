# Local stress and energy radius of the fixed continuum packet

**Accepted conditional result: the supplied source dictionary succeeds for the registered one-particle packet.** Its vacuum-subtracted local expectation tensor is smooth, real, symmetric and conserved. Its nonnegative energy density integrates to the accepted excitation energy \(A_*\omega_1\). The initial energy-density radius is finite at every admitted positive bandwidth and strictly exceeds the accepted Fourier-profile radius:
\[
\boxed{
R_E^2(\delta)=\frac{\pi^2c^2}{4\delta^2}
+\frac{5c^2}{4\omega_1^2}
\int_{-1}^{1}\frac{\cos^2(\pi y/2)}{1-(\delta/\omega_1)^2y^2}\,dy,
\qquad 0<\delta<\frac{\pi}{8\tau},\quad
\omega_1=\frac{5\pi}{4\tau}.
}                                                        \tag{1}
\]
In particular \(R_E>R_{\mathrm{profile}}=\pi c/(2\delta)\), while
\(R_E\sim\pi c/(2\delta)\) as \(\delta\to0^+\). The additional positive term requires both frequency-weight derivatives and angular derivatives; it cannot be obtained by substituting the accepted profile radius.

This is a conditional theorem in the supplied continuum Fock model, flat metric and minimal vacuum-subtracted scalar prescription. The accepted covariance belongs to the vacuum, while this nonzero source belongs to its specified one-particle excitation. They remain different states. No DET-native metric, mass, gravity coupling, absolute vacuum-energy rule, preparation or empirical claim is derived. The result passed its reserved distinct scientific review and coordinator admission.

## 1. Supplied inputs and fixed question

Use the accepted [continuum packet construction](continuum_packet_covariance_and_spread.md) with its stated domains, normalization, energy convention and finite-window covariance limits.

The one-particle space is \(\mathcal K=L^2(\mathbb R^3,d^3k)\), with inner product anti-linear in the first argument. The carrier is \(\mathcal F_s(\mathcal K)\), with vacuum \(\Omega\), anti-linear annihilation \(a(f)\), and
\[
[a(f),a^\dagger(g)]=\langle f,g\rangle I,
\qquad \omega(k)=c|k|,
\qquad H=A_*d\Gamma(\omega),\qquad H\Omega=0.               \tag{2}
\]
The positive constants \(c,\tau,A_*\) are supplied. Only the existing \(j=1\) packet is excited. Write
\[
r=|k|,\quad r_\pm=\frac{\omega_1\pm\delta}{c},\quad
N_\delta=\sqrt{\frac{c}{4\pi\delta}},\quad
g(r)=\cos\frac{\pi(cr-\omega_1)}{2\delta},
\]
\[
h_\delta(k)=\frac{N_\delta g(r)}r\,1_{(r_-,r_+)}(r),
\qquad |h_\delta\rangle=a^\dagger(h_\delta)\Omega.           \tag{3}
\]
The accepted proof establishes normalization, \(H^1\) regularity, compact spectral support away from zero,
\(\langle h_\delta|H|h_\delta\rangle=A_*\omega_1\), and
\(R_{\mathrm{profile}}^2=\pi^2c^2/(4\delta^2)\). The first radial derivative can jump at the shell edges. No smoothing, profile substitution, extra excitation or frequency alias is used.

Supply \(X=(x^0,x)\), \(x^0=ct\), \(\eta=\operatorname{diag}(-1,1,1,1)\) and \(\kappa>0\), exactly as in the control. The scalar \(\kappa\) is a kinetic normalization, not the retired κ-gravity proposal. The given field distribution is
\[
\widehat\Psi(t,x)=\frac{C}{(2\pi)^{3/2}}
\int\frac{d^3k}{\sqrt{\omega(k)}}
\left[a(k)e^{-i\omega(k)t+ik\cdot x}
+a^\dagger(k)e^{i\omega(k)t-ik\cdot x}\right],
\qquad C=\sqrt{\frac{A_*c^2}{2\kappa}}.                     \tag{4}
\]
Its kinetic density is \(\kappa[c^{-2}\dot\Psi^2-|\nabla\Psi|^2]/2\). The minimal tensor and Minkowski-vacuum subtraction are fixed; no improvement, constant source offset or independent finite subtraction is added.

## 2. Smeared fields and an actual invariant domain

The bounded-momentum core used for the earlier packet fields is not asserted invariant under arbitrary local-field smearing. Instead define
\[
\mathscr E_\infty=\bigcap_{m=0}^{\infty}D(\omega^m)\subset\mathcal K,
\qquad
\mathscr D=\operatorname{span}\{\Omega,
f_1\otimes_s\cdots\otimes_s f_n:
n<\infty,\ f_i\in\mathscr E_\infty\}.                      \tag{5}
\]
This algebraic domain is dense: square-integrable functions with bounded momentum support are dense in \(\mathcal K\), and finite algebraic symmetric tensors are dense sectorwise. It contains \(|h_\delta\rangle\). Multiplication by \(\omega\) and \(e^{it\omega}\) preserves \(\mathscr E_\infty\); \(H\) acts on each tensor by a finite sum of single-factor multiplications. Thus \(H\) and its time group preserve \(\mathscr D\). For any \(f\in\mathscr E_\infty\), creation adds a factor and annihilation contracts a factor, so both preserve \(\mathscr D\). All these operations and their finite products are defined there.

For a real test function \(F\in C_c^\infty(\mathbb R^4)\), use the measure \(d^4X=dx^0d^3x\) and set
\[
f_F(k)=\frac{C}{(2\pi)^{3/2}\sqrt{\omega(k)}}
\int F(X)e^{i|k|x^0-ik\cdot x}\,d^4X.
\]
Then \(\Psi(F)=a(f_F)+a^\dagger(f_F)\). The Fourier transform of \(F\) decreases faster than every inverse power along the mass shell at large \(|k|\). At zero the multiplier is at worst \(|k|^{-1/2}\), whose squared radial integral in three dimensions is proportional to \(\int_0^1r\,dr<\infty\). Multiplication by any nonnegative power of \(\omega\) preserves square integrability. Therefore \(f_F\in\mathscr E_\infty\).

Real Schwartz spatial smearings at a fixed time have the same property. Differentiated fields smeared against these tests introduce only additional polynomial momentum/frequency factors or test-function derivatives, and remain in the same class. Complex tests are defined by linear extension. Consequently the finite products of smeared fields required for the two-point expectation act on (5). Their kernels need not have bounded momentum support. This supplies the required domain without asserting a state-independent point-stress operator or its self-adjointness.

The accepted second-quantized time group acts on (5) by
\[
e^{itH/A_*}a(f)e^{-itH/A_*}=a(e^{it\omega}f),
\]
and likewise on creation. The anti-linearity of annihilation gives the negative phase in its integral in (4); the adjoint gives the positive phase. Thus the new local dictionary has the stipulated free-time dependence after smearing. Its mass-shell kernel also satisfies the massless wave equation distributionally.

## 3. Subtraction before coincidence

Use the prescribed unitary inverse Fourier transform \(\mathscr F\), and define the one-particle wave amplitude
\[
v_\delta(t,x)=\frac{C}{(2\pi)^{3/2}}
\int\frac{h_\delta(k)}{\sqrt{\omega(k)}}
e^{-i\omega(k)t+ik\cdot x}\,d^3k
=C\mathscr F\!\left[\omega^{-1/2}h_\delta e^{-it\omega}\right](x).
                                                               \tag{6}
\]
This is \(\langle\Omega|\widehat\Psi(X)|h_\delta\rangle\) as a distributional matrix element. Every momentum-weighted integrand in any spacetime derivative of (6) is in \(L^1\), because its support is compact and avoids zero. Differentiation under the integral is justified, so \(v_\delta\in C^\infty\), all its derivatives are bounded, and
\[
\Box v_\delta=0,
\qquad \Box=-c^{-2}\partial_t^2+\Delta_x.                  \tag{7}
\]
The jumps of the momentum derivative at the shell edges do not obstruct spacetime smoothness: these derivatives multiply the integrand by momentum, rather than differentiating it with respect to momentum.

Apply the CCR to smeared products on (5), with the normalized one-particle state (3). They give
\[
\begin{aligned}
&\langle h_\delta|\widehat\Psi(X)\widehat\Psi(Y)|h_\delta\rangle
-\langle\Omega|\widehat\Psi(X)\widehat\Psi(Y)|\Omega\rangle\\
&\hspace{1cm}=
v_\delta(X)\overline{v_\delta(Y)}
+\overline{v_\delta(X)}v_\delta(Y).                         \tag{8}
\end{aligned}
\]
Equation (8) is initially a distributional equality. Its right side is a smooth function, symmetric in \(X,Y\); it is therefore also exactly the registered symmetric difference \(S_\delta(X,Y)\). It can be differentiated and restricted to the diagonal without ambiguity. Neither unrenormalized vacuum expectation is separately evaluated at coincidence.

## 4. Complete tensor, positivity and conservation

In this section write \(v=v_\delta\). The prescribed tensor is
\[
t^{\mu\nu}_\delta(X)=\kappa\lim_{Y\to X}
\left[\tfrac12(\partial_X^\mu\partial_Y^\nu+
\partial_X^\nu\partial_Y^\mu)
-\tfrac12\eta^{\mu\nu}\eta^{\alpha\gamma}
\partial_{X^\alpha}\partial_{Y^\gamma}\right]S_\delta(X,Y),
\]
with upper derivatives raised by \(\eta\). Applying this operator to (8) gives
\[
\boxed{
t^{\mu\nu}_\delta
=2\kappa\operatorname{Re}(\partial^\mu\overline v\,\partial^\nu v)
-\kappa\eta^{\mu\nu}\partial_\alpha\overline v\,\partial^\alpha v.
}                                                        \tag{9}
\]
The contracted term is real. All components, including flux and stress, are
\[
\boxed{\begin{aligned}
\rho_\delta=t^{00}_\delta
 &=\kappa\left(c^{-2}|\dot v|^2+|\nabla v|^2\right),\\
t^{0a}_\delta=t^{a0}_\delta
 &=-\frac{2\kappa}{c}\operatorname{Re}(\dot{\overline v}\,\partial_av),\\
t^{ab}_\delta
 &=2\kappa\operatorname{Re}(\partial_a\overline v\,\partial_bv)
+\kappa\delta^{ab}\left(c^{-2}|\dot v|^2-|\nabla v|^2\right).
\end{aligned}}                                            \tag{10}
\]
Equations (6) and (10) specify the tensor everywhere by convergent exact integrals for the one fixed packet. It is real, symmetric and smooth. In particular \(\rho_\delta\ge0\). This positivity is for the registered one-particle expectation, not for every normal-ordered state or for a pointwise stress operator.

Differentiate (9). Smooth mixed derivatives commute; the terms quadratic in first/second derivatives cancel against the derivative of the contracted term. The remainder is
\[
\partial_\mu t^{\mu\nu}_\delta
=2\kappa\operatorname{Re}\bigl[(\Box\overline v)\partial^\nu v\bigr]
=0.                                                       \tag{11}
\]
This proves local conservation on the supplied flat spacetime without a boundary source or an asymptotic approximation.

## 5. Integrated energy and boundary control

The first derivatives of (6) are in \(L^2(\mathbb R^3)\) for every real \(t\). Plancherel and \(\omega=c|k|\) yield
\[
\|c^{-1}\dot v\|_2^2
=\frac{A_*}{2\kappa}\int\omega|h_\delta|^2d^3k,
\qquad
\|\nabla v\|_2^2
=\frac{A_*}{2\kappa}\int\omega|h_\delta|^2d^3k.              \tag{12}
\]
The phases have modulus one. Hence
\[
\boxed{\int\rho_\delta(t,x)d^3x
=A_*\langle h_\delta,\omega h_\delta\rangle
=\langle h_\delta|H|h_\delta\rangle
=A_*\omega_1>0.}                                         \tag{13}
\]
The last value is the accepted packet energy. The local-to-global equality has been checked directly from the new dictionary, not assumed from a formal identity between an unsmeared local Hamiltonian and \(H\).

Every tensor component is in \(L^1\) by Cauchy–Schwarz applied to (10) and (12). For an integrated conservation check, let \(\chi_R(x)=\chi(x/R)\) be smooth, equal to one on a ball and zero outside a larger ball, with \(|\nabla\chi_R|\le C_\chi/R\). The energy current is \(j^a=c\,t^{a0}\); (10) gives \(|j|\le c\rho_\delta\). Integrating \(\partial_t\rho_\delta+\nabla\cdot j=0\) against \(\chi_R\), its boundary contribution has magnitude at most
\[
\frac{C_\chi}{R}\int|j|d^3x
\le\frac{C_\chi c A_*\omega_1}{R}\longrightarrow0.          \tag{14}
\]
This bound is uniform on finite time intervals. The same argument for the other components uses their uniform \(L^1\) bounds. No unproved pointwise decay, surface limit on an exact sphere or compact spatial support is needed.

## 6. Initial energy moment, with the spectral and angular terms

Set \(n_i=k_i/|k|\) on the spectral shell and
\[
f(k)=\sqrt{\omega(k)}\,h_\delta(k).
\]
At \(t=0\), substituting (6) in the first line of (10) gives
\[
\rho_\delta(0,x)=\frac{A_*}{2}
\left(|\mathscr Ff(x)|^2+
\sum_{i=1}^3|\mathscr F(n_if)(x)|^2\right).                 \tag{15}
\]
The functions \(f,n_if\) vanish at both shell edges and are smooth inside the shell. The shell avoids the origin. Their interior first derivatives are square integrable, and their zero traces remove the surface delta from zero extension. Thus all four functions lie in \(H^1(\mathbb R^3)\). Their derivative jumps are allowed; no second weak derivative is required.

The weighted Plancherel theorem now proves finiteness and gives
\[
M_{2,E}=\int|x|^2\rho_\delta(0,x)d^3x
=\frac{A_*}{2}\left(\|\nabla_k f\|_2^2+
\sum_i\|\nabla_k(n_if)\|_2^2\right).                        \tag{16}
\]
For radial real \(f\), \(\nabla f=f'(r)n\), and
\(\partial_{k_a}n_i=(\delta_{ai}-n_an_i)/r\). Consequently
\[
\sum_i|\nabla(n_if)|^2=(f')^2+\frac{2f^2}{r^2}.
\]
The cross term vanishes because \(\sum_i n_i\nabla n_i=0\); the sum of the angular derivative squares is \(2/r^2\). Inserting this in (16) yields
\[
M_{2,E}=4\pi A_*\int_{r_-}^{r_+}\left[r^2(f')^2+f^2\right]dr.
                                                               \tag{17}
\]
On the shell, \(f(r)=N_\delta\sqrt c\,r^{-1/2}g(r)\), so the full integrand is
\[
r^2(f')^2+f^2
=cN_\delta^2\left[rg'^2-gg'+\frac{5g^2}{4r}\right].         \tag{18}
\]
The \(1/4\) part comes from the radial derivative of \(r^{-1/2}g\); the additional \(1\) comes from the angular contribution in (17). The mixed term has the exact boundary value
\[
-\int_{r_-}^{r_+}gg'\,dr=-\frac12[g^2]_{r_-}^{r_+}=0.       \tag{19}
\]
No shell-edge term has been dropped by an unsupported smoothness assumption.

With \(s=cr-\omega_1\), direct parity and trigonometric integration give
\[
\int_{r_-}^{r_+}rg'^2\,dr
=\frac{\pi^2}{4\delta^2}
\int_{-\delta}^{\delta}(\omega_1+s)
\sin^2\frac{\pi s}{2\delta}\,ds
=\frac{\pi^2\omega_1}{4\delta},
\]
\[
\int_{r_-}^{r_+}\frac{g^2}{r}\,dr
=\int_{-\delta}^{\delta}
\frac{\cos^2(\pi s/(2\delta))}{\omega_1+s}\,ds.              \tag{20}
\]
Since \(4\pi cN_\delta^2=c^2/\delta\), divide (17) by the energy (13) to obtain the exact initial radius
\[
\boxed{R_E^2(\delta)=\frac{\pi^2c^2}{4\delta^2}
+\frac{5c^2}{4\delta\omega_1}
\int_{-\delta}^{\delta}
\frac{\cos^2(\pi s/(2\delta))}{\omega_1+s}\,ds.}             \tag{21}
\]
The denominator is strictly positive, since \(\delta/\omega_1<1/10\); the integral is finite and positive. Symmetrizing after \(s=\delta y\) gives (1). This is the allowed specified convergent one-dimensional integral, not a numerical evaluation or an omitted moment calculation.

The preparation and (6) are rotation invariant, so \(\rho_\delta(0,x)\) is radial. Its first moment is absolutely integrable because
\(\int|x|\rho_\delta\le\sqrt{M_{2,E}\int\rho_\delta}\). Parity therefore gives \(\int x\rho_\delta(0,x)d^3x=0\). The fixed origin used in (16) is its energy centroid; no translation or radius convention was optimized after the result.

## 7. Narrow-band behavior and the permitted covariance comparison

Write \(\epsilon=\delta/\omega_1\) and \(w(y)=\cos^2(\pi y/2)\). On \([-1,1]\), \(\int w\,dy=1\), and
\[
I(\epsilon)=\int_{-1}^1\frac{w(y)}{1-\epsilon^2y^2}\,dy,
\qquad
1<I(\epsilon)<\frac1{1-\epsilon^2}\quad(0<\epsilon<1/10).
\]
In particular the correction in (1) is positive and bounded for the entire admitted family. Uniform geometric expansion under the integral gives
\[
I(\epsilon)=1+\mu_2\epsilon^2+O(\epsilon^4),
\qquad \mu_2=\int_{-1}^1y^2w(y)dy=\frac13-\frac2{\pi^2}.
\]
For example, after the first two terms the absolute remainder is at most
\(\epsilon^4\int y^4w(y)dy/(1-\epsilon^2)\), which justifies the expansion without a numerical limit. Thus
\[
\boxed{R_E^2(\delta)=\frac{\pi^2c^2}{4\delta^2}
+\frac{5c^2}{4\omega_1^2}
\left[1+\left(\frac13-\frac2{\pi^2}\right)
\frac{\delta^2}{\omega_1^2}
+O\!\left(\frac{\delta^4}{\omega_1^4}\right)\right].}        \tag{22}
\]
The finite constant correction is \(5c^2/(4\omega_1^2)=4c^2\tau^2/(5\pi^2)\). It follows that
\[
R_E>R_{\mathrm{profile}},\qquad
\frac{R_E}{R_{\mathrm{profile}}}\longrightarrow1,
\qquad
\lim_{\delta\to0^+}\frac{\delta R_E}{c}=\frac\pi2.           \tag{23}
\]
As bandwidth tends to zero, the accepted finite-window vacuum covariance error tends to zero while this specified one-particle energy radius diverges, without changing its mean excitation energy. The two radii are not identical even though their leading divergence agrees.

For precision about that last statement, the already accepted error is
\[
\mathcal E_\delta=\sqrt{3/8}\,[1-F(3\delta\tau)],\qquad
F(z)=\frac{\pi^2\sin z}{z(\pi^2-z^2)},
\]
with its accepted removable values, and
\(\mathcal E_\delta=(9/2)\sqrt{3/8}\,\mu_2(\delta\tau)^2
+O((\delta\tau)^4)\). Combining this accepted formula with (22) gives only the family-parameter relation
\[
\mathcal E_\delta
=\frac{9\pi^2}{8}\sqrt{3/8}\,\mu_2
\left(\frac{c\tau}{R_E(\delta)}\right)^2
+O\!\left(\left(\frac{c\tau}{R_E(\delta)}\right)^4\right).
                                                               \tag{24}
\]
Here \(\omega_1\tau=5\pi/4\) stays fixed. Equation (24) relates the **vacuum** covariance of the original distributed two-direction probe to the radius of the separately specified **one-particle** state as functions of the common parameter \(\delta\). It is not a covariance measured in that excited state, a single preparation realizing both properties or a bound over other profiles. No new excited-state covariance calculation is performed.

## 8. Result, limitations and stop

The finite source branch is positive: differentiated coincidence is well-defined in the one-state expectation, conservation holds, nonnegative energy weighting is justified and the integrated excitation energy matches. The finite-bandwidth moment exists. The equality-of-radii shortcut is rejected by the positive term in (1), while the energy-radius divergence is proved. These statements complete exactly the admitted obligations.

The source dictionary, full Fock representation, metric and coordinates, dispersion, field kernel, \(c,\tau,A_*,\kappa\) and subtraction convention remain supplied. Cancellation of \(A_*\) and \(\kappa\) from the radius is not a calibration or native unit derivation. The metric/Hilbert/amplitude inputs fail the primitive-input test for a DET-native quantum–geometry map; this result is not \(F\) or \(L\) derived from DET.

Reference-vacuum stress is zero by the stipulated subtraction. No gravitational absolute source, cosmological vacuum-energy cancellation, mass identification, self-gravitating state, clock/force response, physical detector or preparation/work budget follows. The initial radius is a fixed-frame energy-distribution moment, not an invariant particle-position observable or universal localization bound.

The original structural chain probabilities \(779/1320\) and \(574/1320\), with fair marked-quarter weights \(779/5280\) and \(574/5280\), remain unchanged. The field is still a conditional attachment, not an all-history model or feedback into the native growth law. The excluded original prefix, exact stationary isolated-source obstruction and absence of a normalized monochromatic packet remain unchanged. No torus initial data or tidal proof was repeated; no cavity/feedback draft was adopted.

Exact private controls, source identities, author and review records are retained under the [publication policy](../coordination/REDACTED_PUBLICATION.md). This public derivation does not supply a physical preparation or empirical custody package.
