# Exact retained-register dynamics for the continuum packets

**Accepted conditional result, with distinct Energy scientific review and coordinator admission.**
The accepted continuum evolution induces an exact trace-preserving channel on
the supplied vacuum-plus-two-packet register. This family cannot be a
time-homogeneous semigroup on that register: the one-particle input in its
original packet \(h_1\) gives strictly different survival probabilities under actual
evolution and under composition of the one-tick channel. On the original finite
window, however, an explicit time-dependent generator and completely positive
intermediate maps reproduce every stipulated reduced state exactly.

This decides a restricted integration interface. A homogeneous
update cannot simply be assigned to this reduced continuum component. A
time-dependent update is available for the fixed vacuum-environment preparation.
It is not a certificate for arbitrary interventions, physical memorylessness,
native time calibration or a complete replacement of the continuum field.

## 1. Public prerequisites, scope and review

The [continuum packet construction](continuum_packet_covariance_and_spread.md)
supplies the exact normalized cosine-annulus packets, full Hamiltonian and
operator domains, phase convention, characteristic factor and unchanged native
conditioning. Its sections 2–5 give the packet and overlap premises used below.
This article supplies the retained qutrit channel, strict overlap inequality,
intermediate maps and generator needed by the
[repeated-readout result](repeated_retained_register_readout.md).

The comparison with a homogeneous update is defined within this article. A
separate birth/field semigroup and a separate clock/Kerr interface are context,
not mathematical prerequisites for the proof. No theorem from either is used to
identify native time with the supplied continuum parameter or to provide a
calibration.

Provisional Integrated Model research authored the result. A distinct Energy
scientific review accepted the exact channel, composition obstruction and
finite-window propagation with scope and no substantive correction; coordinator
admission followed. Author assistance was separate from that review. The reviewed
record places the registered channel contract before its selected proof. This
scientific acceptance establishes conditional mathematics, not empirical or
apparatus validation. Private source identities and review records are retained
under the [publication policy](../coordination/REDACTED_PUBLICATION.md).

## 2. Supplied reduction and unchanged continuum

Keep the accepted one-particle space, vacuum-zero Hamiltonian and time convention:

\[
\mathcal K=L^2(\mathbb R^3,d^3k),\quad b(k)=c|k|,
\quad H=A_*d\Gamma(b),\quad U_t=e^{-itH/A_*}=\Gamma(e^{-itb}).
\tag{1}
\]

The inner product is anti-linear in its first argument. The positive quantities
\(c,\tau,A_*\) are supplied, not derived native scales. Retain exactly the two
normalized cosine-annulus packets \(h_1,h_2\) in the accepted source, with

\[
\omega_1=5\pi/(4\tau),\qquad \omega_2=7\pi/(4\tau),\qquad
0<\delta<\pi/(8\tau).
\tag{2}
\]

Their supports are disjoint shells, and their common frequency-offset density is
\(w(y)=\cos^2(\pi y/2)\) on \([-1,1]\), with integral one. No packet profile,
frequency, bandwidth range or native history weight is changed. The continuum
component remains conditional on its original supported-chain fixture; the
native chain probabilities are not replaced by one. Other histories receive
no new continuum attachment here.

The following reduction is a **new supplied interface**. Set
\(S=\operatorname{span}\{h_1,h_2\}\) and use the canonical Fock factorization

\[
\mathcal F_s(\mathcal K)
\cong\mathcal F_s(S)\otimes\mathcal F_s(S^\perp).
\]

Within the first factor retain the qutrit

\[
\mathcal H_R=\operatorname{span}\{|0\rangle,|1\rangle,|2\rangle\},
\qquad |j\rangle=a^\dagger(h_j)|0\rangle\ (j=1,2),
\tag{3}
\]

where \(|0\rangle\) is the retained vacuum. Allow any density matrix \(\rho\)
on this qutrit, and at \(t=0\) supply the discarded factor in its exact vacuum
\(|0_E\rangle\), uncorrelated with \(\rho\). This is an input-domain and
preparation premise, not a consequence of the accepted vacuum covariance.
Then define, only on the registered window \(0\le t\le3\tau\),

\[
\Lambda_t(\rho)=\operatorname{Tr}_E
 \big[U_t(\rho\otimes|0_E\rangle\langle0_E|)U_t^\dagger\big].
\tag{4}
\]

Total excitation number is at most one and is conserved by (1), so the reduced
state stays in (3). When an excitation moves into an orthogonal discarded mode,
the retained factor is vacuum. That probability is kept; this is not a survival
projection followed by renormalization.

The information object is the complete reduced density matrix for the fixed
initial preparation at a chosen final time. Ideal final retained-register POVM
access is supplied if an operational interpretation is desired. The only
nontrivial composition witness below uses the original \(|1\rangle\) input and
the final projector \(|1\rangle\langle1|\) at \(2\tau\). No classical joint
record for noncommuting multi-time fields is asserted. Nor does this qutrit
claim to reproduce the continuum's full field algebra or ordered covariance.

A time-homogeneous CPTP semigroup on this retained register is the comparison
assumption here; its required composition identity appears in (12). No equality
between a native parameter and the continuum's \(t\) is introduced, and no native
growth rule or rate is modified.

## 3. Exact reduced channel, including every coherence

Use the accepted characteristic factor

\[
F(z)=\int_{-1}^1w(y)e^{-izy}\,dy
 =\frac{\pi^2\sin z}{z(\pi^2-z^2)},\qquad F(0)=1.
\tag{5}
\]

The integral fixes the removable values. On this window put

\[
f(t)=F(\delta t),\qquad
\eta_j(t)=\langle h_j,e^{-itb}h_j\rangle=e^{-i\omega_jt}f(t).
\tag{6}
\]

The phase follows from Schrödinger evolution in (1), consistently with the
accepted Heisenberg convention. Disjoint supports give
\(\langle h_i,e^{-itb}h_j\rangle=0\) for \(i\ne j\). Decompose

\[
e^{-itb}h_j=\eta_j(t)h_j+r_j(t),\qquad r_j(t)\in S^\perp.
\tag{7}
\]

Here \(\|r_j(t)\|^2=1-|\eta_j(t)|^2\). The two residuals remain supported
in disjoint shells and are orthogonal. The encoded evolution therefore has

\[
|0\rangle|0_E\rangle\mapsto|0\rangle|0_E\rangle,
\]
\[
|j\rangle|0_E\rangle\mapsto
 \eta_j(t)|j\rangle|0_E\rangle+|0\rangle|r_j(t)\rangle_E,
\tag{8}
\]

where the last vector is the unnormalized one-particle residual in the discarded
factor. It is orthogonal to its vacuum. Taking the partial trace in (8) gives
the three finite Kraus operators

\[
R_0(t)=|0\rangle\langle0|+
             \sum_{j=1}^2\eta_j(t)|j\rangle\langle j|,
\qquad R_j(t)=\sqrt{1-f(t)^2}\,|0\rangle\langle j|\quad(j=1,2),
\tag{9}
\]
\[
\boxed{\Lambda_t(\rho)=\sum_{a=0}^2R_a(t)\rho R_a(t)^\dagger.}
\tag{10}
\]

The accepted window gives \(0<f(t)\le1\); the overlap modulus bound also
follows from unitarity and normalized packets. Thus (9) is well defined,
and \(\sum_aR_a^\dagger R_a=I_R\). Equation (10) is completely positive and
trace preserving, including when the register is entangled with a spectator
ancilla. No actual ancillary preparation is added to the proposed readout.

For completeness, its action on every matrix entry is

\[
\begin{aligned}
(\Lambda_t\rho)_{00}&=\rho_{00}+(1-f(t)^2)(\rho_{11}+\rho_{22}),\\
(\Lambda_t\rho)_{jj}&=f(t)^2\rho_{jj} &&(j=1,2),\\
(\Lambda_t\rho)_{j0}&=\eta_j(t)\rho_{j0} &&(j=1,2),\\
(\Lambda_t\rho)_{12}&=\eta_1(t)\overline{\eta_2(t)}\rho_{12}.
\end{aligned}
\tag{11}
\]

The other entries are conjugates for density matrices; these formulas extend
linearly to all register operators. They show that this is a complete channel
description, not merely a fit to one prepared state's population. At \(t=0\)
the map is identity. On this finite-dimensional register no unbounded-generator
domain is needed; the upstream unitary and packet domains were already accepted.

## 4. One exact contradiction to homogeneous composition

A time-homogeneous CPTP semigroup matching (4) on all register states throughout
the same window would require

\[
\Lambda_{2\tau}=\Lambda_\tau\circ\Lambda_\tau.
\tag{12}
\]

Take just the registered input \(\rho=|1\rangle\langle1|\), and set
\(d=\delta\tau\in(0,\pi/8)\). By (11), the final \(|1\rangle\) probabilities
in (12) would have to agree:

\[
P_{\rm actual}=F(2d)^2,\qquad P_{\rm composed}=F(d)^4.
\tag{13}
\]

They are strictly different. To prove the sign without sampling bandwidths,
use the real even form \(F(z)=\int w(y)\cos(zy)\,dy\). Differentiation under
the integral is valid because the domain is compact and the integrands and
their derivatives are bounded. For \(0\le z\le3d<3\pi/8<\pi/2\),
\(\cos(zy)>0\) on \([-1,1]\), and hence

\[
F(z)>0,\qquad
F''(z)=-\int_{-1}^1y^2w(y)\cos(zy)\,dy<0.
\]

Strictness follows because the integrand is positive on a set of nonzero
measure away from \(y=0\). Therefore

\[
(\log F)''(z)=\frac{F''(z)}{F(z)}-
                       \left(\frac{F'(z)}{F(z)}\right)^2<0.
\]

Strict midpoint concavity on \([0,2d]\), together with \(F(0)=1\), gives

\[
2\log F(d)>\log F(2d),\qquad
\boxed{F(2d)^2<F(d)^4.}
\tag{14}
\]

Thus the complete channels cannot obey (12). In particular, **no
time-homogeneous CPTP semigroup on this qutrit can reproduce the specified
family throughout the window**. This conclusion uses one input, one final
projector and the original tick times; it requires no extra fixture, numerical
bandwidth or large-time revival. The allowed bandwidth is strictly positive.

The composed channel is a mathematical comparator. Applying a second copy of
the initial-environment channel would correspond to supplying its vacuum
assignment again, but no physical environment-reset operation is executed or
claimed free. The full continuum in (1) remains autonomous. The failure is of
homogeneous closure on the stipulated reduced register, not of unitarity or of
the accepted full source dynamics.

## 5. Exact time-dependent completely positive propagation

The accepted integral also gives \(F'(z)<0\) for \(0<z\le3d\). For example,
its even form gives

\[
F'(z)=-2\int_0^1 y w(y)\sin(zy)\,dy<0
\]

on this range. Consequently for \(0\le s\le t\le3\tau\),

\[
q(t,s)=\frac{f(t)}{f(s)}\in(0,1],\qquad
\eta_j(t,s)=e^{-i\omega_j(t-s)}q(t,s).
\tag{15}
\]

Define \(\mathcal V_{t,s}\) by the same Kraus form (9)–(10), replacing
\(\eta_j(t)\) by \(\eta_j(t,s)\) and \(f(t)\) by \(q(t,s)\). Every such
map is CPTP by the same explicit sum-to-identity calculation. Directly from
(11), amplitudes multiply and the lost populations add to the complement of
the product survival. Thus

\[
\mathcal V_{t,s}\Lambda_s=\Lambda_t,\qquad
\mathcal V_{t,s}\mathcal V_{s,r}=\mathcal V_{t,r},\qquad
\mathcal V_{s,s}=I
\quad(0\le r\le s\le t\le3\tau).
\tag{16}
\]

For example, the vacuum contribution after two maps with survival factors
\(q_1^2,q_2^2\) is
\((1-q_1^2)+q_1^2(1-q_2^2)=1-q_1^2q_2^2\) per initial excited population.
Coherences multiply by the corresponding complex amplitudes. This verifies
(16) on every matrix unit. Hence the family is CP-divisible on the stated
window despite not being a time-homogeneous semigroup.

An exact time-local generator is also available. Put

\[
D_\omega=\omega_1|1\rangle\langle1|+\omega_2|2\rangle\langle2|,
\quad L_j=|0\rangle\langle j|,
\quad \gamma(t)=-2\frac{\dot f(t)}{f(t)}
              =-2\delta\frac{F'(\delta t)}{F(\delta t)}.
\tag{17}
\]

The rate is finite and continuous on this closed window, with \(\gamma(0)=0\)
and \(\gamma(t)>0\) for \(t>0\). Differentiating (11) yields

\[
\boxed{\frac{d\rho_t}{dt}=-i[D_\omega,\rho_t]
 +\gamma(t)\sum_{j=1}^2\left(
 L_j\rho_t L_j^\dagger-\tfrac12\{L_j^\dagger L_j,\rho_t\}\right).}
\tag{18}
\]

Indeed, the excited populations decay at rate \(\gamma\), vacuum gains their
sum, the coefficients multiplying \(\rho_{j0}\) have logarithmic derivative
\(-i\omega_j-\gamma/2\), and the coefficient multiplying \(\rho_{12}\) has
logarithmic derivative \(-i(\omega_1-\omega_2)-\gamma\). The conjugate
coherences carry the conjugate phase signs. These give exactly the derivatives of
(11). Continuous finite-dimensional coefficients ensure the unique solution
for each initial density matrix; (11) supplies it explicitly. The rates depend
on elapsed time from the specified vacuum-environment preparation. In general
\(\mathcal V_{t,s}\) is not \(\Lambda_{t-s}\), as (14) already witnesses.

No additional dynamical-reservoir hypothesis is needed to prove this
one-time-state representation. Conversely, these intermediate maps are not
asserted to be the actual reduced operation after arbitrary interventions on a
register correlated with its continuum environment. CP-divisibility of this
fixed-preparation family establishes neither a multi-time process law nor
quantum regression, physical memorylessness, environment-reset capability or
an independent costed clock. No claim outside \([0,3\tau]\) is made.

## 6. Integration decision and limits

For the specified restricted input/readout interface, the exact finite retained
state is the qutrit density matrix (11). Its homogeneous-semigroup replacement
is excluded by (14), while (15)–(18) provide an exact time-dependent alternative.
A subsequent integrated model would have to retain the elapsed-time dependence
or additional state sufficient for its own intended dynamics; this packet does
not analyze such an enlarged model or prove it impossible.

This does not alter a separately accepted birth/field semigroup, identify a native
parameter with \(t\), or derive a shared physical clock from a separate
clock/Kerr interface. It does not replace the whole continuum source by three
levels or preserve all its field products. The one-particle restriction,
environment vacuum, lack of initial correlations, reduction and readout are
explicitly supplied. The original continuum model, scales and native-chain
conditioning remain supplied as before.

Retained-register leakage is motion out of the chosen packet subspace under
free dispersion. It is not disappearance of an excitation from the full field.
The original number-conserving unitary and full energy conservation remain
unchanged. A reduced occupation or the finite frequency matrix in (18) is not
a derivation of emitted energy, heating, work, source stress, gravitational
mass or a conserving apparatus. No physical packet preparation, detector,
calibration, repeated-run resource budget or empirical test is provided.

The value here is an explicit conditional component interface and composition
decision, not a new fundamental law or a claim of mathematical novelty.
**Agreement with observations: NOT TESTED.** Known covariance/pointer failures,
Option B, Status M and the retirement of kappa-gravity remain unchanged.

## 7. Evidence and physical-resource boundary

There are two original packet modes, one retained qutrit, total input excitation
at most one, one symbolic admitted bandwidth family and one nontrivial
composition witness. There were **zero scientific code executions, numerical
sweeps, simulations, empirical trials or upstream reruns**. File, hash, JSON and
readback checks establish document custody, not physical resource or
algorithm-performance measurements. No finite environment, reset-work or
finite-sample guarantee is claimed. A finite Kraus list for each time does not
supply a fixed finite physical environment or an autonomous finite dilation for
the whole family.

The exact channel, all coherences, strict two-tick inequality, intermediate-map
composition and generator were checked analytically in the distinct scientific
review. Publication preserves that scope; it does not create a new dynamical,
physical-resource or empirical acceptance.
