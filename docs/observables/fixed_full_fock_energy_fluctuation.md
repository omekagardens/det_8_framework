# Fixed continuum stress fluctuation: full-Fock limit and analytic bound

**Accepted conditional result, following distinct scientific review and coordinator admission.** For the registered cosine-shell one-particle state and fixed Gaussian spacetime sampling, the common-cutoff normal-ordered energy action converges in full-Fock norm. Its mean is positive, and its ordinary state-level relative variance satisfies
\[
\boxed{0<\mathcal R_*<\frac{4691}{5184}<1.}                 \tag{1}
\]
This is a proved upper bound, not an evaluated value of the ratio. Exact convergent integrals below define its value. No numerical quadrature, sampling, parameter adjustment or Gaussian closure is used.

The result quantifies fluctuations omitted by replacing this one supplied source functional by its deterministic mean. It is not a metric response, a gravitational-validity criterion, a detector model or a DET-native reconstruction. The positive variance explicitly retains the vacuum and stimulated pair contributions of the already normal-ordered stress.

## 1. Public inputs, registration limits and scope

The fixed scientific inputs are the accepted [continuum packet](continuum_packet_covariance_and_spread.md) and [local stress and energy radius](local_stress_and_energy_radius.md). These public prerequisites provide the full Fock/CCR convention, packet normalization and shell regularity, local field and tensor, integrated energy and exact initial energy-radius proofs used below. Their [publication manifest](../publications/continuum-packet-local-stress/PUBLICATION_MANIFEST.json) and this article's [source and publication identities](../publications/fixed-full-fock-fluctuation/PUBLICATION_MANIFEST.json) identify the adopted versions. Those accepted source proofs are reused.

The result implements its separately accepted prospective design without changing the state, sampling, cutoff or statistic. The recorded order constructs the finite-cutoff action and establishes its full-Fock norm limit before comparing the moments. Distinct scientific review supports the registered artifact and documented phase order. It does not certify invisible private reasoning, every helper's internal chronology or every historical file state; some original chat-output previews were truncated. The complete saved result and the exposed registration/order evidence were reviewed. No unconditional all-reasoning or empirical prospectivity claim is made.

Use \(\mathcal F_s(L^2(\mathbb R^3,d^3k))\), normalized vacuum \(\Omega\), anti-linear annihilation, inner products anti-linear in their first argument, and the accepted CCR. The supplied positive constants are \(c,\tau,A_*,\kappa\), with
\[
\omega_k=c|k|,\quad H=A_*d\Gamma(\omega),\quad
C=\sqrt{\frac{A_*c^2}{2\kappa}}.
\]
The exact original state is \(a^\dagger(h)\Omega\), where
\[
\omega_1=\frac{5\pi}{4\tau},\quad \delta_*=\frac{\pi}{16\tau},
\qquad
h(k)=\sqrt{\frac{c}{4\pi\delta_*}}\,
\frac{\cos[\pi(c|k|-\omega_1)/(2\delta_*)]}{|k|}
1_{\{|c|k|-\omega_1|<\delta_*\}}.                         \tag{2}
\]
It is real, normalized, compactly supported away from zero, and has the accepted \(H^1\) regularity. Its derivative jumps at the shell edges are retained. There is no smoothing or state substitution.

Set \(\ell=R_E(\delta_*)\), the accepted initial **energy** radius, and retain the supplied flat metric and field
\[
\Psi(t,x)=\frac{C}{(2\pi)^{3/2}}
\int\frac{a(k)e^{-i\omega_kt+ik\cdot x}
+a^\dagger(k)e^{i\omega_kt-ik\cdot x}}{\sqrt{\omega_k}}\,d^3k.
\]
The common cutoff is \(\chi_\Lambda(k)=1_{\{\omega_k\le\Lambda\}}\) in each field factor. The registered functional is
\[
E_\Lambda=\int dt\,d^3x\,F(t,x):T^{00}_\Lambda(t,x):_\Omega,
\quad
T^{00}_\Lambda=\frac{\kappa}{2}
\left(c^{-2}\dot\Psi_\Lambda^2+\sum_i(\partial_i\Psi_\Lambda)^2\right),
\]
\[
F(t,x)=\frac{e^{-t^2/(2\tau^2)}}{\sqrt{2\pi}\tau}
e^{-|x|^2/(2\ell^2)}.                                    \tag{3}
\]
The spatial Gaussian is unnormalized, with center value one. Thus \(E_\Lambda\) has energy units. With \(d^4X=c\,dt\,d^3x\), the same test is \(F/c\). The Gaussian's infinite past/future and spatial tails are part of a mathematical sampling convention, not a causal detector. Positive weights do not assert positivity of the full Wick energy on arbitrary states.

## 2. Finite-cutoff action and its norm limit

This section establishes the limiting vector before comparing moments.

For finite \(\Lambda\), the field and first-derivative kernels are in \(L^2\). At zero momentum the field has squared radial weight proportional to \(\omega\,d\omega\), and the derivatives to \(\omega^3d\omega\); the upper endpoint is finite. Their norms are independent of \(t,x\). Creation/annihilation bounds on each fixed particle sector therefore define the normal-ordered quadratic on the algebraic finite-particle domain with arbitrary square-integrable symmetric sector wavefunctions. Its action is uniformly bounded between each relevant pair of sectors. Since \(F\in L^1(dt\,d^3x)\), integrating this action is a Bochner integral on each finite-particle vector. This constructs the registered finite-cutoff product rather than postulating a formal unsmeared limiting operator.

The exact transform of the test is
\[
\int F(t,x)e^{-i\nu t+iz\cdot x}\,dt\,d^3x
=(2\pi)^{3/2}\ell^3e^{-\tau^2\nu^2/2-\ell^2|z|^2/2}.
\]
Write \(d=A_*\ell^3/[2(2\pi)^{3/2}]\) and \(u=\widehat k\cdot\widehat p\). Directions at zero have no effect on the integrals. Define the real symmetric kernels
\[
N(k,p)=d\sqrt{\omega_k\omega_p}(1+u)
e^{-\tau^2(\omega_k-\omega_p)^2/2-\ell^2|k-p|^2/2},
\]
\[
P(k,p)=-d\sqrt{\omega_k\omega_p}(1+u)
e^{-\tau^2(\omega_k+\omega_p)^2/2-\ell^2|k+p|^2/2}.          \tag{4}
\]
Both derivatives have negative equal-orientation products and positive mixed products. Normal ordering gives two mixed number terms, so the exact convention is
\[
E_\Lambda=\iint N_\Lambda(k,p)a^\dagger(k)a(p)\,dk\,dp
+\frac12\iint P_\Lambda(k,p)
[a^\dagger(k)a^\dagger(p)+a(k)a(p)]\,dk\,dp,               \tag{5}
\]
where each kernel is multiplied by \(\chi_\Lambda(k)\chi_\Lambda(p)\). The factor \(1/2\) in the pair term and its minus sign are retained. The kinetic normalization \(\kappa\) cancels using \(C\).

Let \(\operatorname{Sym}\) denote the orthogonal symmetrization projection with normalized symmetric-sector wavefunctions. Only sectors one and three occur:
\[
E_\Lambda|h\rangle
=(N_\Lambda h)\ \oplus\
\sqrt{\frac32}\operatorname{Sym}(P_\Lambda\otimes h).       \tag{6}
\]
The three-particle wavefunction is explicitly
\[
\frac1{\sqrt6}
\left[P_\Lambda(k_1,k_2)h(k_3)
+P_\Lambda(k_1,k_3)h(k_2)
+P_\Lambda(k_2,k_3)h(k_1)\right].
\]
The spectator \(h\) is not truncated. Pair annihilation kills the one-particle input.

Put \(b_\omega=\omega_1+\delta_*\) and
\(C_h=2d\int\sqrt{\omega_p}|h(p)|\,dp<\infty\). Dropping the spatial Gaussian and using the shell support gives
\[
|(Nh)(k)|\le C_h\sqrt{\omega_k}\,
e^{-\tau^2(\omega_k-b_\omega)_+^2/2}.                      \tag{7}
\]
The squared radial majorant is proportional to
\(\omega_k^3e^{-\tau^2(\omega_k-b_\omega)_+^2}\), integrable at zero and infinity. Therefore \(Nh\in L^2\). For \(\Lambda\ge b_\omega\),
\(N_\Lambda h=\chi_\Lambda Nh\to Nh\) in \(L^2\).

For the pair kernel,
\[
|P(k,p)|^2\le4d^2\omega_k\omega_p
e^{-\tau^2(\omega_k+\omega_p)^2}.
\]
Using \((\omega_k+\omega_p)^2\ge\omega_k^2+\omega_p^2\) and the radial measure gives
\[
\|P\|_{\rm HS}^2
\le4d^2\left(\frac{4\pi}{c^3}\right)^2
\left(\int_0^\infty s^3e^{-\tau^2s^2}\,ds\right)^2
=\frac{16\pi^2d^2}{c^6\tau^8}<\infty.                    \tag{8}
\]
Dominated convergence yields \(P_\Lambda\to P\) in Hilbert–Schmidt norm. Since symmetrization is a contraction,
\[
\|E_\Lambda|h\rangle-\zeta_*\|^2
\le\|(\chi_\Lambda-1)Nh\|^2
+\frac32\|P_\Lambda-P\|_{\rm HS}^2\longrightarrow0,
\]
\[
\boxed{\zeta_*=(Nh)\oplus\sqrt{\frac32}
\operatorname{Sym}(P\otimes h).}                          \tag{9}
\]
The number kernel is not claimed Hilbert–Schmidt or bounded without a cutoff. No invariant domain, essential self-adjointness or \(D(E^2)\) claim is made for a limiting operator. The result is the requested state-action norm limit.

## 3. Mean and the ordinary connected second moment

Now define \(\mu_*=\langle h,\zeta_*\rangle=\langle h,Nh\rangle\).
For every \(\Lambda\ge b_\omega\), the one-particle mean uses exactly the accepted wave amplitude
\[
v(t,x)=C\mathscr F[\omega^{-1/2}h\,e^{-it\omega}](x),
\]
since the cutoff leaves its shell unchanged. Normal ordering subtracts the same vacuum as the accepted local tensor. Consequently
\[
\mu_*=\int F(t,x)\rho(t,x)\,dt\,d^3x,\qquad
\rho=\kappa(c^{-2}|\dot v|^2+|\nabla v|^2)\ge0,
\quad \int\rho(t,x)\,d^3x=E:=A_*\omega_1.                 \tag{10}
\]
The finite-cutoff mean agrees exactly with this expression, and (9) identifies its limit. Reality and finiteness follow; \(F>0\) and \(E>0\) already imply \(\mu_*>0\).

The three diagonal and six cross contractions of (6) give
\[
\left\|\sqrt{\frac32}\operatorname{Sym}(P\otimes h)\right\|^2
=\frac12\|P\|_{\rm HS}^2+\|P\overline h\|^2.              \tag{11}
\]
Here \(h\) is real, but the conjugation specifies the convention. Hence
\[
\boxed{V_*=\|\zeta_*\|^2-\mu_*^2
=\|Nh\|^2-\mu_*^2+\frac12\|P\|_{\rm HS}^2
+\|P\overline h\|^2.}                                    \tag{12}
\]
The first term minus \(\mu_*^2\) is nonnegative by Cauchy–Schwarz. The pair kernel is nonzero on an open set of nonzero momenta, so \(V_*>0\). All terms are finite by Section 2. The half-Hilbert–Schmidt term is the ordinary vacuum contribution; the contraction with \(h\) is the additional pair contribution in the occupied state. Normal ordering the square, removing vacuum variance or projecting onto one particle would change (12).

For each finite cutoff the finite-particle domain also supports the square, so the ordinary second moment is the squared action norm. The limiting diagnostic uses that norm limit; no limiting squared-operator domain or spectral measurement law is inferred.

## 4. Exact dimensionless integrals for the single diagnostic

Let
\[
q=c\tau k,\quad \alpha=\frac{5\pi}{4},\quad
\epsilon=\frac{\pi}{16}=\frac{\alpha}{20},\quad
\lambda=\frac{\ell}{c\tau},\quad E_0=\frac{A_*}{\tau}.
\]
The accepted radius fixes, without numerical evaluation,
\[
\lambda^2=64+\frac4{5\pi^2}
\int_{-1}^1\frac{\cos^2(\pi y/2)}{1-y^2/400}\,dy>64.       \tag{13}
\]
The unitary map \(Uf(q)=(c\tau)^{-3/2}f(q/(c\tau))\) takes \(h\) to the normalized real function
\[
g(q)=\frac{\cos[\pi(|q|-\alpha)/(2\epsilon)]}
{\sqrt{4\pi\epsilon}\,|q|}
1_{\{||q|-\alpha|<\epsilon\}}.                            \tag{14}
\]
For \(r=|q|,\ s=|p|\), define \(\gamma=\lambda^3/[2(2\pi)^{3/2}]\) and
\[
n(q,p)=\gamma\sqrt{rs}(1+\widehat q\cdot\widehat p)
e^{-[(r-s)^2+\lambda^2|q-p|^2]/2},
\]
\[
p_2(q,p)=-\gamma\sqrt{rs}(1+\widehat q\cdot\widehat p)
e^{-[(r+s)^2+\lambda^2|q+p|^2]/2}.                        \tag{15}
\]
The subscript on \(p_2\) distinguishes the pair kernel from a momentum variable. The number operator kernel transforms to \(E_0n\), and the pair tensor under \(U\otimes U\) to \(E_0p_2\).

The following are explicit Lebesgue integrals, with every momentum measure \(d^3q\) or \(d^3p\):
\[
\begin{aligned}
m&=\iint g(q)n(q,p)g(p)\,dq\,dp,\\
I_N&=\int\left|\int n(q,p)g(p)\,dp\right|^2dq,\\
I_P&=\iint|p_2(q,p)|^2\,dq\,dp,\\
I_C&=\int\left|\int p_2(q,p)g(p)\,dp\right|^2dq.
\end{aligned}                                           \tag{16}
\]
Section 2 proves convergence; all inner integrals are well-defined and the norm integrals finite. The mean integrand is nonnegative. Their relation to the sole registered diagnostic is
\[
\mu_*=E_0m,\qquad V_*=E_0^2(I_N-m^2+\tfrac12I_P+I_C),
\qquad
\boxed{\mathcal R_*=\frac{I_N-m^2+\tfrac12I_P+I_C}{m^2}.}  \tag{17}
\]
These intermediate terms are the decomposition of one statistic, not additional selected observables. No fitted constants enter. Cancellation of supplied unit scales from the ratio does not derive those scales or the continuum dictionary from DET.

## 5. Analytic mean and number-channel bounds

First strengthen positivity of the mean. Put \(f=\sqrt\omega\,h\), with real \(H^1\) functions \(f,n_if\), where \(n_i=k_i/|k|\). The accepted density has the representation
\[
\rho(t,x)=\frac{A_*}{2}
\left(|\mathscr F(e^{-it\omega}f)|^2+
\sum_i|\mathscr F(e^{-it\omega}n_if)|^2\right).
\]
For each real initial function \(a\) in this list, the weak product rule yields
\[
|\nabla(e^{-it\omega}a)|^2
=|\nabla a|^2+t^2a^2|\nabla\omega|^2.
\]
The cross term vanishes because the two factors have relative phase \(i\), and \(|\nabla\omega|=c\) on the shell. Weighted Plancherel, the accepted initial radius and \(\sum_i n_i^2=1\) imply
\[
\int|x|^2\rho(t,x)\,dx=E(\ell^2+c^2t^2).                 \tag{18}
\]
This uses the exact evolving packet, including its allowed shell-edge regularity. Apply Jensen's inequality to \(e^{-u}\) and the probability density \(\rho(t,\cdot)/E\), then perform the elementary Gaussian time integral:
\[
\frac{\mu_*}{E}\ge
\frac{e^{-1/2}}{\sqrt{1+c^2\tau^2/\ell^2}},
\qquad
\frac m\alpha\ge\frac{e^{-1/2}}{\sqrt{1+\lambda^{-2}}}>
\frac35.                                                \tag{19}
\]
For the last strict inequality, \(\lambda^2>64\) and \(e<49/18\) give
\(64/(65e)>1152/3185>9/25\).
The elementary exponential bound follows, for example, by summing its series through \(1/4!\) and bounding the tail from \(1/5!\) by the geometric sum \(1/100\).
Also \(m\le\alpha\) because the spatial weight is at most one.

For the number-channel norm, define the normalized Gaussian kernel
\[
G_\lambda(z)=\frac{\lambda^3}{(2\pi)^{3/2}}e^{-\lambda^2|z|^2/2},
\quad
J(q,p)=\frac{1+\widehat q\cdot\widehat p}{2}
e^{-(r-s)^2/2}G_\lambda(q-p).
\]
Then \(n=\sqrt r\,J\sqrt r\). The operator \(J\) is a positive contraction. To see this without confusing kernel order with operator order, convolution \(T\) by \(G_\lambda\) has Fourier multiplier \(e^{-|x|^2/(2\lambda^2)}\), so \(0\le T\le I\). Its normalized Gaussian-time average under the multiplication group \(e^{itr}\) is a positive contraction \(B\) with kernel \(e^{-(r-s)^2/2}G_\lambda(q-p)\). With real bounded direction multipliers \(M_i(q)=q_i/r\),
\[
J=\tfrac12(B+\sum_iM_iBM_i),\qquad
\sum_iM_i^2=I,\qquad 0\le J\le I.                         \tag{20}
\]
Separately, the pointwise kernel inequality \(0\le J(q,p)\le G_\lambda(q-p)\) and Cauchy–Schwarz give
\[
|JF(q)|^2\le\int G_\lambda(q-p)|F(p)|^2\,dp
\]
for \(F=\sqrt r\,g\). This \(F\) is a momentum function, not the spacetime test (3). It obeys \(\|F\|^2=\alpha\) and is supported at \(r\le b:=21\alpha/20\). Since \(J^2\le J\),
\[
\begin{aligned}
I_N&=\int r|JF(q)|^2\,dq\\
&\le b\|JF\|^2+
\iint(r-b)_+G_\lambda(q-p)|F(p)|^2\,dp\,dq\\
&\le bm+\alpha\,\frac{2\sqrt{2/\pi}}{\lambda}.             \tag{21}
\end{aligned}
\]
The last line uses \((|q|-b)_+\le|q-p|\) on the support of \(F(p)\) and the exact first radial moment of the three-dimensional normalized Gaussian. It controls output outside the input shell; no projection of the number kernel onto that shell was made.

## 6. Pair bound and resolved comparison

The angular factor in the full minimal tensor is essential for a stronger pair estimate. Radial/angular integration in (16) gives
\[
I_P=\frac{\lambda^6}{4\pi}\,\mathcal I,\qquad
\mathcal I=\int_0^\infty dr\int_0^\infty ds\,r^3s^3
\int_{-1}^1du\,(1+u)^2
e^{-(r+s)^2-\lambda^2(r^2+s^2+2rsu)}.
\]
Use \(S=r+s,\ D=r-s,\ Q^2=D^2+2rs(1+u)\). The domain becomes
\(0\le Q\le S,\ -Q\le D\le Q\), and the full measure with polynomial factor is
\(Q(Q^2-D^2)^2\,dS\,dD\,dQ/8\).
Since \(\int_{-Q}^Q(Q^2-D^2)^2dD=16Q^5/15\),
\[
\mathcal I=\frac{\sqrt\pi}{15}
\int_0^\infty Q^6e^{-\lambda^2Q^2}\operatorname{erfc}(Q)\,dQ,
\quad
\operatorname{erfc}(Q)=\frac2{\sqrt\pi}\int_Q^\infty e^{-S^2}dS.
\]
This also gives a one-dimensional exact expression for the vacuum term. Bounding \(\operatorname{erfc}(Q)\le1\) and using the elementary Gaussian moment yields
\[
\boxed{I_P\le\frac1{64\lambda},\qquad
\tfrac12I_P+I_C\le\tfrac32 I_P\le\frac3{128\lambda}.}       \tag{22}
\]
Here \(I_C\le I_P\) follows from the Hilbert–Schmidt bound and \(\|g\|=1\). All substitutions involve nonnegative integrands, so Tonelli justifies the integration order.

Combine (19), (21) and (22):
\[
\mathcal R_*
\le\frac b m-1+
\frac{\alpha\,2\sqrt{2/\pi}}{\lambda m^2}
+\frac3{128\lambda m^2}.                                \tag{23}
\]
Now use only exact inequalities:
\(\lambda>8,\ \alpha>15/4,\ m>3\alpha/5>9/4\), and
\(\sqrt{2/\pi}<5/6\). They imply
\[
\frac b m-1<\frac34,\quad
\frac{\alpha\,2\sqrt{2/\pi}}{\lambda m^2}<\frac{25}{162},
\quad
\frac3{128\lambda m^2}<\frac1{1728}.
\]
Thus
\[
\mathcal R_*<
\frac34+\frac{25}{162}+\frac1{1728}
=\frac{4691}{5184}<1,
\]
while Section 3 proves strict positivity. The comparison is resolved analytically for this fixed sampling. The bound need not be sharp and does not identify the exact ratio or show that fluctuations are negligible.

## 7. Meaning and physical limits

For this stipulated packet and weighted functional, rms fluctuation is strictly smaller than the positive mean, with the bound (1). The nonzero variance remains information lost by a deterministic-mean substitution. It includes the full one- and three-particle action and does not use the previous finite-oscillator Gaussian closure or any metric response.

The supplied Hilbert/Fock carrier, amplitudes, flat metric, dispersion, field kernel, dimensional constants and vacuum prescription remain inputs. This does not satisfy the primitive-input test for a DET-native quantum–geometry map. No empirical discriminator, gravity adequacy, mass calibration, initial-data construction, detector, preparation cost or dynamics follows. Gaussian sampling remains frame-specific and noncompact.

The original conditional four-chain attachment, structural probabilities \(779/1320\) and \(574/1320\), and fair marked-quarter weights are unchanged. Other histories remain unattached rather than assigned zero energy or variance. No action-profile reweighting is used. PIM's gravity/mass questions and Classical's apparatus work remain separate.

## Scientific status and publication scope

The original author checks supported the analytic construction; they did not substitute for the later distinct scientific review by DET Relational State Research. That review passed the exact frozen result without correction, and coordinator admission retained the conditional scope above. Exact rational arithmetic checked the final inequalities. No numerical quadrature, sampling, parameter sweep, empirical run or new scientific executor was used.

The source-energy diagnostic alone is published here. No later geometry-response result, PIM gravity or mass construction, Classical apparatus result or other pending calculation is incorporated as a premise or consequence. Publication does not establish a limiting self-adjoint observable, a limiting squared-operator domain, a spectral measurement law, native quantities or empirical validity. It does not broaden the conditioning or exclusions of the linked accepted inputs.

Exact original controls, author and review custody, and the scoped acceptance are identified in the [publication manifest](../publications/fixed-full-fock-fluctuation/PUBLICATION_MANIFEST.json). Private administration is retained under the [publication policy](../coordination/REDACTED_PUBLICATION.md). This public proof is not a physical preparation, executable installation or independently replayable empirical custody package.
