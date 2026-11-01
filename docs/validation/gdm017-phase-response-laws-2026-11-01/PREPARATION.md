# GDM016 — initial phase controls the signed ensemble response

**Accepted scoped formal result after distinct review and coordinator disposition.** In the accepted two-truncation comparison, uniform classical initial phase cancels the signed mean response difference through order c^-2. Retaining a nonzero signed mean requires an independently specified phase-distribution moment. No physical phase preparation or response-error bound is supplied.

Prior familiarity with the earlier GDM calculations is disclosed in PREMISES. The accepted GDM015-v2 result is a dependency; rejected v1 remains unadmitted. This is not blind reproduction.

## Same model, changed initial phase only

Use exactly the Hamiltonians, -fQ_x control, canonical map and Q/R readouts in the accepted [GDM015 calculation](../gdm015-gradient-response-2026-10-31/CALCULATION.md). In particular,
\[
H_B-H_A\doteq-\frac{3\epsilon g}{M}q_x(\mathbf P\cdot\mathbf p),
\qquad \epsilon=c^{-2},\quad M=2m,\quad\mu=M/4,
\]
and omega^2=C/(mu*a^3). The source potential remains -gR_x, with no offset, beta_PPN=gamma_PPN=1 and no radiation interaction. All equalities marked doteq concern formal coefficients through epsilon at fixed finite time, not bounded full-model remainders.

Let varphi be a classical orbital initial phase, not a quantum phase. Keep Q(0)=P(0)=0, and set
\[
\mathbf q(0)=a(\cos\varphi,\sin\varphi,0),\quad
\mathbf p(0)=\mu a\omega(-\sin\varphi,\cos\varphi,0).
\]
For each varphi these initial data are held fixed across f,g and both models. The laboratory x direction, orbital plane, radius and angular speed are unchanged. The leading unforced orbit has angle varphi+omega*t; its E_0=W_0=-C/(2a) remains phase-independent. Its use inside epsilon-multiplied terms has the same formal-order justification as the accepted calculation. Keep the same collision-free, low-speed, weak-local-field scope and t_*=pi/(4omega).

## Phasewise first response

Write T_X^j=partial_g X_x^j at f=g=0, X=Q or R, j=A or B, and Delta=B-minus-A. The same vector-field difference gives
\[
\Delta\dot T_Q(t,\varphi)\doteq
-\frac{3\epsilon}{M}q_{0x}p_{0x}
=\frac{3\epsilon\mu a^2\omega}{2M}
\sin(2\varphi+2\omega t).
\]
The added term changes neither the first momentum variation nor the internal first variations at baseline P=Q=0. The Q-to-R correction therefore cancels between the two models. Directly in old variables, the added Hamiltonian gives the same -3epsilon*r_x*p_rx/M velocity-response difference. Zero response initial data require integration from zero:
\[
\boxed{\Delta T_Q(t,\varphi)\doteq\Delta T_R(t,\varphi)
\doteq\frac{3\mu a^2}{4Mc^2}
\{\cos(2\varphi)-\cos(2\varphi+2\omega t)\}.}\tag{1}
\]
Equivalently this is 3mu*a^2/(2Mc^2) times [sin^2(varphi+omega*t)-sin^2(varphi)]. Omitting the initial-phase subtraction would violate DeltaT(0,varphi)=0 and give an incorrect ensemble mean.

At the stipulated time,
\[
\Delta T_Q(t_*,\varphi)\doteq\Delta T_R(t_*,\varphi)
\doteq K[\cos(2\varphi)+\sin(2\varphi)],\qquad
K=\frac{3\mu a^2}{4Mc^2}=\frac{3a^2}{16c^2}>0.\tag{2}
\]
Varphi=0 recovers the accepted endpoint. T and K have units time squared. This equality of model-to-model changes does not identify the individual Q and R responses.

## Exact ensemble criterion

Let nu be any fixed probability distribution on phase modulo 2pi, specified independently of f,g, the model label and the response being tested. It is the same preparation distribution for force and gravity responses. No density, iid sampling or physical phase-control device is assumed. Define its bounded moments
\[
m_c=\int\cos(2\varphi)\,d\nu,\qquad
m_s=\int\sin(2\varphi)\,d\nu,\qquad \eta=m_c+m_s.
\]
Averages here are coefficientwise integrals of bounded continuous phase functions at fixed time. They are not an interchange claim about unknown full-model remainders. Equation (2) gives
\[
\boxed{\langle\Delta T_Q(t_*)\rangle_\nu
\doteq\langle\Delta T_R(t_*)\rangle_\nu\doteq K\eta.}\tag{3}
\]
Thus the retained coefficient is positive exactly when eta>0, negative exactly when eta<0, and zero exactly when eta=0. A nonzero second-harmonic moment in some other direction is insufficient; its particular projection eta is decisive here. Eta is dimensionless and distinct from the constituent mass m.

For uniform phase on [0,2pi), both sine and cosine integrals vanish, so eta=0 and the signed mean difference vanishes through the retained order. This does not assert exact equality beyond that order. Without any phase certificate, the allowed distributions include this cancellation; there is no guaranteed signed nonzero mean.

One sufficient phase-interval certificate is support, on a chosen circular lift, in
\[
[\pi/8-h,\pi/8+h],\qquad 0\le h<\pi/4.
\]
On this interval,
\[
\cos(2\varphi)+\sin(2\varphi)
=\sqrt2\cos(2\varphi-\pi/4)\ge\sqrt2\cos(2h)>0.
\]
Hence every probability distribution with that certified support satisfies eta>=sqrt(2)*cos(2h), and (3) has the corresponding positive retained floor. This is a mathematical sufficient condition, not an available preparation procedure; no second interval family is needed.

## Force normalization and ensemble order

The same [GDM014 force identities](../gdm014-force-response-2026-10-31/CALCULATION.md), evaluated on this shifted leading orbit, give
\[
S_Q\doteq s\left(1-\frac{\epsilon E_0}{M}\right),\qquad
S_R(t,\varphi)-S_Q(t)\doteq
-\frac{\epsilon t}{M^2}q_{0x}p_{0x},\qquad s=\frac{t^2}{2M}.\tag{4}
\]
Both models have these same force denominators because they coincide at g=0. At t_*>0, s>0 is independent of phase. The corrections are bounded on the phase circle, so the formal inverses exist uniformly in phase; this is not a rigorous lower bound for a full physical response. Normalization at t=0 is excluded.

For clarity, the individual gravity numerators may be written
\[
J(t,\varphi)=\frac{\mu a^2}{2M}
[\sin^2(\varphi+\omega t)-\sin^2\varphi],
\]
\[
T_Q^A\doteq t^2/2-\epsilon J,\quad
T_Q^B\doteq t^2/2+2\epsilon J,\quad
T_R^j-T_Q^j\doteq-\frac{\epsilon t}{M}q_{0x}p_{0x}.\tag{5}
\]
In particular the leading numerator t_0=t^2/2=M*s is also independent of phase. Distinguish, for each model and readout,
\[
\mathcal Z_{X,\mathrm{ratio}}^j
=\frac{\langle T_X^j\rangle}{\langle S_X\rangle},\qquad
\mathcal Z_{X,\mathrm{mean}}^j
=\left\langle\frac{T_X^j}{S_X}\right\rangle.
\]
Writing T_X^j=t_0+epsilon*tau_X^j and S_X=s+epsilon*sigma_X shows directly that both have the same retained expansion
\[
\frac{t_0}{s}+\epsilon\left(
\frac{\langle\tau_X^j\rangle}{s}
-\frac{t_0\langle\sigma_X\rangle}{s^2}\right).\tag{6}
\]
They are different definitions; their agreement here follows from the phase-independent leading numerator and denominator. No exact or higher-order identity is claimed, particularly for the phase-dependent R denominator.

Since DeltaT already starts at epsilon, each model-to-model normalized difference at t_* is therefore
\[
\boxed{\Delta\mathcal Z_{Q,\mathrm{ratio}}
\doteq\Delta\mathcal Z_{R,\mathrm{ratio}}
\doteq\Delta\mathcal Z_{Q,\mathrm{mean}}
\doteq\Delta\mathcal Z_{R,\mathrm{mean}}
\doteq\frac{24C}{\pi^2ac^2}\,\eta.}\tag{7}
\]
The units are mass. Uniform phase cancels this retained difference too. For the single interval certificate above, replace eta by its stated lower bound to obtain the corresponding positive retained normalized floor.

## Preparation decision and remaining boundary

Reject the unconditional claim that this signed ensemble-mean readout remains nonzero without phase information. Retain only its conditional version with an independently specified distribution whose projected moment eta has a certified nonzero sign. A quantitative preparation margin would require |eta|>=eta_min>0; exact nonzero alone gives no margin against unbounded physical or measurement errors. This is a condition on an ensemble, not a demand for perfectly sharp individual phases.

The [GDM013 applicability boundary](../gdm013-physical-applicability-2026-10-31/APPLICABILITY.md) remains: neither Hamiltonian is a complete physical response model. Omitted electromagnetic-gradient effects and response-level errors, physical preparation/control/time/readout and calibration, and any native DET correspondence remain unresolved. The phase certificate cannot be manufactured by fitting the target response or selecting observed outcomes. No sampling guarantee, empirical discriminator, physical gravity prediction or broader phase-blind impossibility follows. This preparation screen is closed at its proved scope. The distinct distributional question is addressed in [GDM017](CALCULATION.md); it does not revise this signed-mean conclusion.


GDM016 distinct review completed November 1, 2026 at 09:10:14 UTC; coordinator disposition followed at 09:12:42 UTC. See [review](REVIEW.md), [adoption](ADOPTION.md) and [source manifest](SOURCE_MANIFEST.json).
