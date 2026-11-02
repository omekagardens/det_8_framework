# Conditional internal-clock Ramsey readout

**Independently reviewed and coordinator-adopted mathematical scope:** retain this finite conventional clock construction; revise a mean-trajectory-only interface to include the momentum second moment. Reject the claim that the two chosen variances distinguish the matched gravity-minus-zero-field readout at order c^-2. GDM022's different, fixed center-motion exclusion remains unchanged.

**Model and source-reduction card.** Work on L2(R) tensor C2 with [X,P]=i hbar, M>0, DeltaE>0, omega=DeltaE/hbar, finite T>0, and fixed real field parameter g. Positive g means force -Mg and potential phi(X)=gX, with the same declared origin and time reference in both controls. Define

\[
H_0^g=P^2/(2M)+MgX,\quad V_g=gX-P^2/(2M^2),\quad
H_A=\Delta E|e\rangle\langle e|,
\]
\[
H^{(2)}=H_0^g+H_A+c^{-2}(H_A V_g+H_{\rm common}^g).
\]
The common operator acts on COM identically in both internal levels; it may depend on g and need not commute with H0 or V. Assume a self-adjoint realization admitting the stated finite-time perturbative matrix elements on the preparations. An arbitrary unspecified common operator is not automatically guaranteed these domain properties.

The two-level truncation with constant gap, fixed internal basis and no transitions/leakage is an added model assumption. Ground internal energy is set to zero; M is the declared baseline mass in this convention, not a derived physical constituent or bound-state mass. Canonical coordinates/time, Hilbert structure, external field and ideal pulses are borrowed inputs.

Schwartz–Giulini §5.2 relates the composite central Hamiltonian to a point-particle expression with internal-energy mass correction, retaining other post-Newtonian terms; its internal-energy identification depends on physical spatial geometry. Section6 warns against universal conclusions based only on classical trajectories or mass labels. Neither section supplies this constant two-level reduction or pulse implementation. Our calculation is a conditional response-level construction, not a derivation of that reduction. [Primary source, §§5.2 and6](https://arxiv.org/html/1908.06929v2).

**Prospective preparations and measurement.** Fix symbolic s>0 and eta>0, independent of c, once for all controls. Choose normalized Gaussian COM density operators rho_A,rho_B with means x0,p0 and covariance matrices

\[
\Sigma_A=\operatorname{diag}(s^2,\hbar^2/(4s^2)),\qquad
\Sigma_B=\operatorname{diag}(s^2,\hbar^2/(4s^2)+\eta).
\]
The symmetrized XP covariance is zero. Both satisfy det Sigma >= hbar²/4. A is pure and B can be obtained by Gaussian random momentum displacement of A with variance eta, hence is mixed. Requiring both to be pure would contradict the stipulated equal position variance and unequal momentum variance. Write their momentum variances as sigmaP_j². The initial joint state is rho_j tensor |+><+|, with |+>=(|g>+|e>)/sqrt2, identical in the g and0 settings.

Use one free evolution T, no intermediate measurement, then either projector onto

\[
|+_\theta\rangle=(|g\rangle+e^{-i\theta}|e\rangle)/\sqrt2,
\qquad \theta=0,\pi/2,
\]
on separately prepared trials. The outcome complement is I minus that projector. These phases are fixed relative to the initial internal basis and the same canonical-time pulse reference across fields and preparations; no setting-dependent phase fit removes a signal. The carrier phase omega T is retained, not assumed small.

Let Ug=exp[-i(H0^g+c^-2 Hcommon^g)T/hbar] and
Ue=exp[-i(H0^g+DeltaE+c^-2(Hcommon^g+DeltaE Vg))T/hbar]. Within a well-defined truncated-model realization the intended exact functional is

\[
C_j^g(T)=\operatorname{Tr}_{\rm COM}(U_e\rho_jU_g^\dagger),\quad
\rho_{{\rm int},eg}=C_j^g/2,\quad
p_{j,\theta}^g=\tfrac12[1+\operatorname{Re}(e^{i\theta}C_j^g)]. \tag{1}
\]
The populations remain1/2 and |C|<=1, so the exact two-outcome law is normalized. The two quadratures reconstruct C=(2p_0-1)-i(2p_pi/2-1). No COM trajectory is an input to (1).

**Retained-order derivation.** Here O_form(c^-4) denotes discarded formal second-order terms in this specified model, not a certified physical error bound. Keep all parameters, states and T fixed in this expansion. In the H0 interaction picture define

\[
K_g=\int_0^T(H_{\rm common}^g)_I(t)dt,\qquad
A_g=\int_0^T(V_g)_I(t)dt.
\]
Factoring off the internal carrier, the two COM propagators have factors I-iK_g/(hbar c²) and I-i(K_g+DeltaE A_g)/(hbar c²). Thus

\[
U_g^\dagger U_e=e^{-i\omega T}
 [I-i\omega A_g/c^2]+O_{\rm form}(c^{-4}). \tag{2}
\]
The common term cancels between the two first-order factors. Its noncommutation and the changes it causes to the trajectory enter products at the discarded order. This is cancellation at the retained order, not exact cancellation of arbitrary common dynamics. It applies separately at g and0 even when their common terms differ. Internal-dependent omitted terms would not enjoy this argument.

The zeroth-order Heisenberg operators are

\[
P_t=P-Mgt,\qquad X_t=X+Pt/M-gt^2/2.
\]
Consequently, by direct integration,

\[
(V_g)_I(t)=gX-P^2/(2M^2)+2gtP/M-g^2t^2,
\]
\[
A_g=gTX-TP^2/(2M^2)+gT^2P/M-g^2T^3/3. \tag{3}
\]
There is no XP ordering ambiguity in (3). Define alpha_j^g=<A_g>_j. Then

\[
\alpha_j^g=gTx_0-\frac{T(p_0^2+\sigma_{P,j}^2)}{2M^2}
 +\frac{gp_0T^2}{M}-\frac{g^2T^3}{3},
\]
\[
C_j^g=e^{-i\omega T}(1-i\omega\alpha_j^g/c^2)
 +O_{\rm form}(c^{-4}), \tag{4}
\]
\[
p_{j,\theta}^g=\frac{1+\cos(\omega T-\theta)}2
 -\frac{\omega\alpha_j^g}{2c^2}\sin(\omega T-\theta)
 +O_{\rm form}(c^{-4}). \tag{5}
\]
These are coefficients of (1), not globally valid truncated probabilities for arbitrary parameter magnitudes. At this order only x0,p0 and <P²> enter; the common position variance does not. Gaussianity supplies lawful chosen states and finite polynomial moments, rather than being necessary for this first-order identity.

**Mean trajectory and both comparisons.** The mean Newtonian trajectory is xbar(t)=x0+p0 t/M-gt²/2, pbar(t)=p0-Mgt. Substituting it in Vg gives

\[
a_g=\int_0^T[g\bar x(t)-\bar p(t)^2/(2M^2)]dt,
\qquad \alpha_j^g=a_g-T\sigma_{P,j}^2/(2M^2).
\]
Thus the mean substitution misses the same variance phase in each field channel:

\[
p_{j,\theta}^g-p_{{\rm mean},\theta}^g
 =\frac{\omega T\sigma_{P,j}^2}{4M^2c^2}
   \sin(\omega T-\theta)+O_{\rm form}(c^{-4}), \tag{6}
\]
\[
p_{B,\theta}^g-p_{A,\theta}^g
 =\frac{\omega T\eta}{4M^2c^2}\sin(\omega T-\theta)
 +O_{\rm form}(c^{-4}). \tag{7}
\]
Equation7 also holds at g=0. A single projector may be phase-blind; the two fixed quadratures cannot both be blind because sin(omega T) and cos(omega T) cannot both vanish. No coefficients or phase settings were tuned after the calculation.

For the matched field contrast, however,

\[
D_g:=\alpha_j^g-\alpha_j^0
 =gTx_0+gp_0T^2/M-g^2T^3/3=a_g-a_0, \tag{8}
\]
\[
p_{j,\theta}^g-p_{j,\theta}^0
 =-\frac{\omega D_g}{2c^2}\sin(\omega T-\theta)
 +O_{\rm form}(c^{-4}). \tag{9}
\]
It is the same for A, B and the mean-trajectory substitution through the retained order. The preparation difference of these matched contrasts has zero c^-2 coefficient. Dg itself can vanish for particular fixed parameters; no universal nonzero field signal is claimed. Differences obtained by retaining a full nonlinear cosine of the truncated phase would introduce uncontrolled higher-order terms.

This identifies the missing second moment in each channel, not a uniquely quantum signature: a classical phase-space ensemble with these same moments reproduces the first-order coefficients. Momentum spread affects the kinetic contribution even without gravity. Position/reference shifts alter coordinate phase assignments; a physical frame change must transport the state, Hamiltonian and pulse reference together. Equation9 is a declared-coordinate comparison, not an equivalence-principle violation.

**Order and application ledger.**

| Layer | Established here or still required |
| --- | --- |
| Truncated model | Equations1–9 give the intended trace functional and its formal c^-2 coefficients, conditional on evolution/domain regularity. No scientific runtime was used. |
| Common corrections | Internal-common c^-2 contributions cancel only at first order in this internal readout. They are not absent from COM dynamics or other observables. |
| Higher orders | No c^-4 visibility/decoherence prediction or physical remainder bound. In particular, squaring the first-order coherence to infer its modulus is invalid at the omitted order. |
| Source reduction | Physical two-level selection, constant gap/basis, omitted internal/gradient/field couplings, leakage, and any mapping of ground energy into M need independent justification. |
| Regime and tails | Physical use requires small internal-energy/rest-energy, weak-field and slow-motion parameters, accumulated-phase/error control and moment/domain bounds. Gaussian support is unbounded: no uniform weak-field/velocity bound is asserted. Tail budgets and response-level errors remain unsupplied. |
| Controls/readout | Real pulses may impart recoil or entangle COM; their geometry, phase, duration, field switch, clock, preparation and detector calibration are not supplied by ideal projectors. |
| Public evidence | A later named realization needs compatible public preparation/covariance, field/reference, level and acquisition evidence, complete attempts/failures, uncertainty and full preparation-to-reset costs. No experiment or empirical success follows. |

**Finite disposition.** Retain the conditional clock observable as a concrete readout design; revise a means-only per-channel description to a second-moment-aware one. At c^-2 retain the mean substitution for this matched contrast alone. Reject a variance-based gravity discriminator at this order. GDM008's restricted no-go and GDM009/011/012/013's conditional/correspondence boundaries remain intact; neither GDM022 nor CL008 is repaired or reopened. This implements the programme's permitted conditional-coupling route, not DET-native emergence, a new mass law or a gravity novelty claim. Independent scientific review is complete. This reference supplies no higher-order or apparatus qualification.

Source identity: GDM023 report SHA256 `c39f466e70cf387644cec658b8684bb143fd265b457ef01abc6920c35e5b09ad`; distinct review SHA256 `f713f9118b341dab47444490c7194e52fd13da273c1bfd3b95b273174f35183a`. Coordinator adoption followed completed independent review on November 2, 2026. These identities establish the source versions; the derivation and assumptions above establish the stated mathematical scope.
