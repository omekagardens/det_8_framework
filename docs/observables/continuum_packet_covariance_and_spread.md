# Continuum cosine-annulus covariance, energy and spatial spread

**Accepted conditional result: the registered family gives a controlled approximate embedding of the accepted four-time ordered vacuum covariance.** At every positive allowed bandwidth the full covariance and its commutator differ from the benchmark. Their covariance error tends to zero quadratically as bandwidth narrows. Each normalized one-particle packet has constant mean excitation energy, while its fixed-frame spatial RMS diverges inversely with bandwidth.

This is a conditional theorem in the explicitly supplied continuum model. The carrier, Hamiltonian, dispersion, clock, action scale and distributed probe are inputs. No DET-native continuum, local stress source, mass, gravity, calibrated units or physical preparation/measurement procedure is derived. The accepted exact isolated-source obstruction is unchanged.

## 1. Supplied inputs and fixed question

Supply \(c,\tau,A_*,\beta>0\), and retain
\[
 \theta_1=\frac{5\pi}{4},\quad\theta_2=\frac{7\pi}{4},\quad
 \omega_j=\frac{\theta_j}{\tau},\qquad
 a_1^2=\frac{\beta}{2}(\sqrt2-1),\quad
 a_2^2=\frac{\beta}{2}(\sqrt2+1),\quad a_j>0.
\]
The benchmark is
\[
 W_\star[n,m]=\frac12\sum_{j=1}^2a_j^2e^{-i(n-m)\theta_j},
 \qquad n,m=0,1,2,3.                                      \tag{1}
\]
This is the accepted changed-prefix covariance from the pinned stationary source, not its excluded original saturated prefix.

The supported structural chain retains probabilities \(779/1320\) and \(574/1320\) in its two native preparations; each fair marked instance has one quarter of the corresponding probability, \(779/5280\) and \(574/5280\). All other native histories and weights remain as supplied. This covariance comparison is conditional on that fixture; it supplies no continuum attachment on other histories and never assigns the selected chain probability one. The native weights are not inferred from the continuum calculation.

Write \(b(k)=c|k|\) for the one-particle frequency operator, avoiding confusion with the packet notation. The supplied Hilbert space is \(\mathcal K=L^2(\mathbb R^3,d^3k)\), with inner product anti-linear in its first argument, and the quantum carrier is the symmetric bosonic Fock space \(\mathcal F_s(\mathcal K)\). The vacuum is \(\Omega\); annihilation is anti-linear and
\[
 [a(f),a^\dagger(g)]=\langle f,g\rangle I,\qquad
 H=A_*d\Gamma(b),\qquad H\Omega=0.                          \tag{2}
\]
The energy convention in (2) is positive excitation energy with vacuum zero. It replaces the old finite unshifted oscillator/source identity. No old point calibration, scalar action density or stress prescription is carried over.

## 2. Normalized packets and their regularity

Use exactly the registered family
\[
 0<\delta<\frac{\omega_2-\omega_1}{4}
             =\frac{\pi}{8\tau},\qquad
 h_{j,\delta}(k)=
 \begin{cases}
 N_{j,\delta}\dfrac{\cos[\pi(c|k|-\omega_j)/(2\delta)]}{|k|},
       & |c|k|-\omega_j|<\delta,\\
 0,&\text{otherwise}.
 \end{cases}                                               \tag{3}
\]
Set \(r=|k|\), \(r_{j,\pm}=(\omega_j\pm\delta)/c\), and
\(g_j(r)=\cos[\pi(cr-\omega_j)/(2\delta)]\) on that interval.
The two shells are disjoint and bounded away from zero. Radial integration gives
\[
 \|h_{j,\delta}\|^2
   =4\pi N_{j,\delta}^2\int_{r_{j,-}}^{r_{j,+}}g_j(r)^2\,dr
   =4\pi N_{j,\delta}^2\frac{\delta}{c}.
\]
Consequently the unique positive normalizations are
\[
 \boxed{N_{1,\delta}=N_{2,\delta}
       =\sqrt{\frac{c}{4\pi\delta}},\qquad
       \langle h_{i,\delta},h_{j,\delta}\rangle=\delta_{ij}.} \tag{4}
\]
The shell values vanish at both edges. Zero extension therefore introduces no surface delta in the first weak derivative. The classical derivative inside each shell is square integrable, as the shell stays away from \(r=0\). Thus \(h_{j,\delta}\in H^1(\mathbb R^3)\). Its radial derivative jumps at the shell edges; it is not globally smooth. Compact momentum support also places the packets in the domain of every power of \(b\).

## 3. Operator domain and autonomous evolution

In the \(N\)-particle sector, \(H\) is multiplication by
\(A_*\sum_{\ell=1}^N c|k_\ell|\), with zero on the vacuum. Its positive self-adjoint domain is
\[
 D(H)=\left\{\psi\in\mathcal F_s(\mathcal K):
 \sum_{N=0}^\infty A_*^2
 \int\left(\sum_{\ell=1}^N c|k_\ell|\right)^2
       |\psi_N(k_1,\ldots,k_N)|^2\,d^{3N}k<\infty\right\}.   \tag{5}
\]
A common domain \(\mathcal D\) consists of finite-particle vectors whose nonzero sectors are supported where every \(|k_\ell|\le M\), for some finite \(M\) depending on the vector. It includes arbitrary symmetric square-integrable wavefunctions with that support. It is dense. Particle-number and momentum cutoffs approximate (5) in graph norm, so \(\mathcal D\) is an \(H\)-core.

The domain is invariant under \(H\), \(e^{itH/A_*}\), all creation/annihilation operators used below, and their finite products. A packet field can enlarge the support bound to the maximum of the vector's bound and the packet's bound, and can change particle number by one; both remain finite.

For \(\Phi(f)=(a(f)+a^\dagger(f))/\sqrt2\) and a vector with at most \(N\) particles,
\[
 \|\Phi(f)^q\psi\|
 \le(\sqrt2\|f\|)^q\sqrt{\frac{(N+q)!}{N!}}\,\|\psi\|.
                                                               \tag{6}
\]
This follows by iterating the creation and annihilation number bounds. Dividing by \(q!\) shows convergence of the analytic-vector series for every finite parameter. Thus the symmetric packet fields are essentially self-adjoint on \(\mathcal D\) by the analytic-vector criterion. All products, commutators and vacuum contractions below are already defined on this common invariant domain.

Let \(G_\delta=\sum_j a_jh_{j,\delta}\). The fixed initial distributed probe and its actual Heisenberg evolution are
\[
 \Phi_\delta(0)=\Phi(G_\delta),\qquad
 \Phi_\delta(t)=e^{itH/A_*}\Phi_\delta(0)e^{-itH/A_*}.
\]
Since \(e^{itH/A_*}=\Gamma(e^{itb})\), anti-linearity of annihilation gives
\[
 e^{itH/A_*}a(f)e^{-itH/A_*}=a(e^{itb}f),\qquad
 \boxed{\Phi_\delta(t)=\Phi(e^{itb}G_\delta).}                \tag{7}
\]
Creation transforms with the same argument. For example, the phase inside the annihilation integral is \(e^{-itb}\), consistently with (7). This fixes the sign without changing the initial probe as a function of sampling time. The closure version of (7) follows from the common core.

The two initial packet directions do not form an invariant two-mode subsystem: at nonzero time, \(e^{itc|k|}\) is not constant on either nonempty shell. Full continuum evolution, rather than a fitted evolution of two coefficients, provides autonomy here.

## 4. Exact ordered covariance and commutator

The vacuum has zero field mean. Disjoint shell supports eliminate cross terms, and the CCR with the above conventions gives
\[
 \begin{aligned}
 W_\delta(t,s)
 &=\langle\Omega,\Phi_\delta(t)\Phi_\delta(s)\Omega\rangle\\
 &=\frac12\sum_j a_j^2
     \langle e^{itb}h_{j,\delta},e^{isb}h_{j,\delta}\rangle\\
 &=\frac12\sum_j a_j^2
     \int |h_{j,\delta}(k)|^2e^{-i(t-s)c|k|}\,d^3k .
 \end{aligned}                                             \tag{8}
\]
For each normalized shell, \(y=(c|k|-\omega_j)/\delta\) has the common probability density \(\cos^2(\pi y/2)\) on \([-1,1]\). Define its characteristic factor
\[
 \begin{aligned}
 F(z)&=\int_{-1}^{1}\cos^2(\pi y/2)e^{-izy}\,dy\\
 &=\frac{\sin z}{z}
   +\frac12\left[\frac{\sin(z-\pi)}{z-\pi}
                 +\frac{\sin(z+\pi)}{z+\pi}\right]\\
 &=\frac{\pi^2\sin z}{z(\pi^2-z^2)}. 
 \end{aligned}                                             \tag{9}
\]
The integral defines the removable values \(F(0)=1\) and \(F(\pm\pi)=1/2\). It is real and even. At the four registered times,
\[
 \boxed{W_\delta[n,m]
       =F((n-m)\delta\tau)\,W_\star[n,m].}                  \tag{10}
\]
For an explicit complete matrix, put \(d=\delta\tau\) and \(F_\ell=F(\ell d)\):
\[
 W_\delta=\frac{\beta}{2}
 \begin{pmatrix}
 \sqrt2 &(1/\sqrt2-i)F_1&-iF_2&(-1/\sqrt2-i)F_3\\
 (1/\sqrt2+i)F_1&\sqrt2&(1/\sqrt2-i)F_1&-iF_2\\
 iF_2&(1/\sqrt2+i)F_1&\sqrt2&(1/\sqrt2-i)F_1\\
 (-1/\sqrt2+i)F_3&iF_2&(1/\sqrt2+i)F_1&\sqrt2
 \end{pmatrix}.                                            \tag{11}
\]
Hermiticity and stationarity are explicit. Positivity is not an assumption about an entrywise attenuation: (8) is the Gram matrix of the four vectors \(e^{in\tau b}G_\delta/\sqrt2\), so \(z^\dagger W_\delta z\ge0\) for every \(z\in\mathbb C^4\).

The field commutators are scalar operators on \(\mathcal D\):
\[
 [\Phi_\delta(t),\Phi_\delta(s)]
  =\tfrac12\bigl(\langle e^{itb}G_\delta,e^{isb}G_\delta\rangle
        -\langle e^{isb}G_\delta,e^{itb}G_\delta\rangle\bigr)I .
\]
Using the benchmark's sampled sign,
\[
 \boxed{[\Phi_\delta(n\tau),\Phi_\delta(m\tau)]
 =i\beta\,\operatorname{sign}(n-m)
        F((n-m)\delta\tau)I,\qquad n\ne m.}                 \tag{12}
\]
Thus the finite-bandwidth commutator is also only approximate. No exact native algebra preservation at positive bandwidth is inferred. Equations (8)–(12) are ordered quantum covariances and operator relations, not a joint classical readout distribution for noncommuting observations.

## 5. Exact finite-window error and analytic bound

On \(0<z\le3d<3\pi/8\), the integral in (9) is positive and strictly below one, and
\[
 F'(z)=-2\int_0^1 y\cos^2(\pi y/2)\sin(zy)\,dy<0.            \tag{13}
\]
The benchmark positive-lag entries, divided by \(\beta\), are
\[
 \frac1{2\sqrt2}+\frac i2,\qquad \frac i2,\qquad
 -\frac1{2\sqrt2}+\frac i2 .
\]
Their magnitudes are respectively \(\sqrt{3/8},1/2,\sqrt{3/8}\).
The diagonal error is zero; monotonicity in (13) makes lag three the maximum. Hence the specified error is exactly
\[
 \boxed{\mathcal E_\delta
 :=\max_{0\le n,m\le3}\frac{|W_\delta[n,m]-W_\star[n,m]|}{\beta}
 =\sqrt{\frac38}\,[1-F(3\delta\tau)]>0.}                    \tag{14}
\]
Here \(\mathcal E_\delta\) is the control's covariance error \(E_\delta\), distinguished typographically from excitation energy.

The second moment of the normalized offset density is
\[
 \mu_2=\int_{-1}^1y^2\cos^2(\pi y/2)\,dy
       =\frac13-\frac2{\pi^2}>0.
\]
Using \(1-\cos x\le x^2/2\) directly inside (9) yields
\[
 \boxed{0<\mathcal E_\delta
 \le\frac92\sqrt{\frac38}\,\mu_2(\delta\tau)^2,}
 \qquad
 \mathcal E_\delta=
 \frac92\sqrt{\frac38}\,\mu_2(\delta\tau)^2
       +O((\delta\tau)^4).                                 \tag{15}
\]
The remainder follows from the cosine Taylor remainder and \(|y|\le1\). These are analytic statements for the one registered family, not a numerical bandwidth sweep or an assertion of uniform approximation over arbitrary long times.

## 6. One-particle excitation energy

The states \(|j,\delta\rangle=a^\dagger(h_{j,\delta})\Omega\) are normalized. Compact spectral support places them in \(D(H^q)\) for every positive integer \(q\). Their energies in the convention (2) are
\[
 \begin{aligned}
 \mathsf E_{j,\delta}
 &=\langle j,\delta|H|j,\delta\rangle
   =A_*\langle h_{j,\delta},b h_{j,\delta}\rangle\\
 &=\frac{A_*}{\delta}\int_{-\delta}^{\delta}
       (\omega_j+s)\cos^2\!\frac{\pi s}{2\delta}\,ds\\
 &=\boxed{A_*\omega_j}.
 \end{aligned}                                             \tag{16}
\]
The odd term vanishes. In particular,
\[
 \mathsf E_{1,\delta}=\frac{5\pi A_*}{4\tau},\qquad
 \mathsf E_{2,\delta}=\frac{7\pi A_*}{4\tau}.
\]
These are mean excitation energies equal to the supplied benchmark oscillator gap scales. The packets at positive bandwidth are not energy eigenvectors; the full continuum Hamiltonian has no positive spectral gap. Equation (16) is not the old ground-source energy \(3\pi A_*/(2\tau)\), a rest-mass identification, an absolute vacuum-energy statement or a preparation/work budget.

## 7. Fourier spatial spread and its boundary terms

Use exactly the registered unitary inverse Fourier transform
\[
 u_{j,\delta}(x)=(2\pi)^{-3/2}
       \int e^{ik\cdot x}h_{j,\delta}(k)\,d^3k .
\]
It is normalized. For \(\rho=|x|>0\) its radial integral is, equivalently,
\[
 u_{j,\delta}(\rho)=
 \frac{4\pi N_{j,\delta}}{(2\pi)^{3/2}\rho}
 \int_{r_{j,-}}^{r_{j,+}}g_j(r)\sin(r\rho)\,dr ,
\]
with the continuous limiting value at zero. No compact spatial support is asserted.

Plancherel and the proved \(H^1\) regularity give the finite second moment
\[
 R_{j,\delta}^2
 =\int |x|^2|u_{j,\delta}(x)|^2\,d^3x
 =\|\nabla_k h_{j,\delta}\|_2^2 .
\]
All radial derivative terms must be retained:
\[
 \begin{aligned}
 R_{j,\delta}^2
 &=4\pi N_{j,\delta}^2
   \int_{r_{j,-}}^{r_{j,+}}
       \left[(g_j')^2-\frac{2g_j'g_j}{r}
                         +\frac{g_j^2}{r^2}\right]\,dr\\
 &=4\pi N_{j,\delta}^2
   \left\{\int_{r_{j,-}}^{r_{j,+}}(g_j')^2\,dr
                   -\left[\frac{g_j^2}{r}\right]_{r_{j,-}}^{r_{j,+}}\right\}\\
 &=4\pi\frac{c}{4\pi\delta}
           \left(\frac{\pi c}{2\delta}\right)^2\frac{\delta}{c}
   =\boxed{\frac{\pi^2c^2}{4\delta^2}} .
 \end{aligned}                                             \tag{17}
\]
The boundary term vanishes because \(g_j\) vanishes at both edges. This cancellation removes any apparent center-frequency contribution from differentiating \(1/r\). Both packets therefore have
\[
 \boxed{R_{j,\delta}=\frac{\pi c}{2\delta}.}                 \tag{18}
\]
Spherical symmetry centers this squared profile at the origin. The quantity is the specified fixed-frame \(L^2\) profile RMS, not a physical particle-position measurement, Lorentz-invariant localization measure or energy-density radius.

## 8. Combined conclusion and singular limit

Let \(R=R_{1,\delta}=R_{2,\delta}\). The admitted bandwidth range is equivalent to \(R>4c\tau\). Combining the exact formulas gives
\[
 \boxed{\mathcal E_\delta
 =\sqrt{\frac38}\left[1-F\!\left(\frac{3\pi c\tau}{2R}\right)\right],
 \qquad \mathsf E_{j,\delta}=A_*\omega_j.}                   \tag{19}
\]
In particular
\[
 \mathcal E_\delta\le
 \frac{9\pi^2}{8}\sqrt{\frac38}\,\mu_2
       \left(\frac{c\tau}{R}\right)^2,\qquad
 \mathcal E_\delta=
 \frac{9\pi^2}{8}\sqrt{\frac38}\,\mu_2
       \left(\frac{c\tau}{R}\right)^2
       +O((c\tau/R)^4).                                    \tag{20}
\]
Within this family, approaching the benchmark requires arbitrarily large profile RMS, with no increase of the mean one-particle excitation energies. This is a tradeoff for this exact supplied family, not a universal localization-energy bound or a bound over other probes.

There is no normalized monochromatic packet at the limit. If \(S_{j,\delta}\) is the shell in (3), then for every fixed \(f\in L^2\),
\[
 |\langle f,h_{j,\delta}\rangle|
 \le\|f\,1_{S_{j,\delta}}\|_2\longrightarrow0.
\]
The shells shrink to a measure-zero sphere, which justifies the last step by dominated convergence. Thus \(h_{j,\delta}\rightharpoonup0\) weakly while \(\|h_{j,\delta}\|=1\); there is no strong \(L^2\) limit to a normalized state. Fourier unitarity transfers this conclusion to \(u_{j,\delta}\). A limiting covariance for these bandwidth-dependent probes does not provide a limiting normalized monochromatic source or restore the excluded all-time two-pair source.

The finite decision is therefore positive for the stated approximate covariance embedding and negative for exact matching at every admitted positive bandwidth. The borrowed continuum carrier and full dynamics, distributed probe and vacuum-zero convention are essential disclosed changes. The quantum covariance result leaves physical preparation, detector realization, disturbance, native-unit calibration and any stress/gravity interpretation unestablished.

This fixed-family result passed distinct scientific review and coordinator admission. Exact private controls, source identities and review manifests are retained under the [publication policy](../coordination/REDACTED_PUBLICATION.md). The supplied benchmark and previous exclusion remain available in [the local scalar-source comparison](local_scalar_source_for_four_chain_field.md) and [the isolated-source obstruction](isolated_stationary_scalar_source_obstruction.md).
