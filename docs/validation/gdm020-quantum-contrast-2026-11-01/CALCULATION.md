# GDM020 — finite quantum expression for the normalized response contrast

**Result:** under the prospectively fixed candidate in MODEL.md, the coefficient of epsilon in Z_R^B-Z_R^A reduces exactly to nineteen adjacent-by-two circular-state matrix elements. Its angular dependence has the same second-harmonic form as the classical contrast. Its two amplitudes have not been numerically evaluated or bounded against the classical values; P1 response correspondence remains undecided. This completes the authorized finite-expression alternative, not a physical or full quantum/classical verification.

MODEL and PREMISES were saved and fully read before the supported16:59:54 UTC checkpoint. No model choice was changed during this derivation. All equalities below concern the defined formal coefficient at fixed parameters and t; no finite-epsilon remainder estimate is supplied.

## 1. Common denominator and the perturbation that survives

Let
\[
 A_j=\tfrac12(q_xp_j+p_jq_x),\qquad
 D=-\frac3M\sum_jP_j A_j.
\]
The supplied Weyl convention gives H_B-H_A=epsilon*g*D. At g=0 the Hamiltonians coincide for every f, and the observable and initial state are the same, so their force responses S_R coincide as formal series. This is an identity of interventions within the candidate, not an independent force calibration.

At leading order the relative Coulomb dynamics decouples from the center. Under the leading controls,
\[
 Q_x(t)=Q_x+\frac tM P_x+\frac{(f+Mg)t^2}{2M}.
\]
Since the leading R observable is Q, both models have
\[
 S_R^{(0)}=s=\frac{t^2}{2M}>0\quad(t>0),\qquad
 T_R^{(0)}=\frac{t^2}{2}.
\]
These formulas hold for the stated finite-width Gaussian; they do not use a sharp central point. Formal division is therefore available at t*. No positive lower bound for an unknown physical denominator is inferred.

Write DeltaT_R=T_R^B-T_R^A=epsilon*DeltaTau_R. The common first-order denominator correction cancels in the contrast:
\[
 [\epsilon](Z_R^B-Z_R^A)=\frac{\Delta\tau_R}{s}.
 \tag{1}
\]
There is no need to compute or assume the classical value of that common correction.

## 2. Linear response and the endpoint identity

Use the interaction picture of H0 at f=g=0. Because D already multiplies epsilon*g, its contribution to this coefficient uses only leading propagation and the leading Q observable. Common order-epsilon Hamiltonian corrections, or the order-epsilon part of R, would enter this model-to-model difference only at higher formal order. The first Duhamel coefficient is
\[
 \Delta\tau_R(t,\varphi)=
 \frac{i}{\hbar}\int_0^t
 \langle[D_I(u),Q_x(t)]\rangle_\varphi\,du.
\]
Under H0, P_j is constant and A_j(u) acts in the relative sector. Hence
\[
 [D_I(u),Q_x+tP_x/M]=\frac{3i\hbar}{M}A_x(u),
\]
and therefore
\[
 \Delta\tau_R=-\frac3M\int_0^t\langle A_x(u)\rangle_\varphi\,du.
 \tag{2}
\]
The central Gaussian width and spectator spin drop out of this contrast coefficient through the commutator. They have not been discarded from the individual responses. In particular, no assertion that all internal response operators vanish for a finite-width center was needed.

For the ordinary Coulomb H_C,
\[
 \frac{d}{du}q_x^2(u)=\frac{2}{\mu}A_x(u),
\]
because the potential commutes with q_x^2. Define
\[
 F_\varphi(t)=\langle\psi_\varphi|
 e^{iH_Ct/\hbar}q_x^2e^{-iH_Ct/\hbar}
 |\psi_\varphi\rangle.
\]
Combining(1)–(2) gives the principal result
\[
 \boxed{\Delta\zeta_R(t,\varphi):=[\epsilon](Z_R^B-Z_R^A)
 =-\frac{3\mu}{t^2}[F_\varphi(t)-F_\varphi(0)].}
 \tag{3}
\]
It has energy units, as required for the coefficient of epsilon in a mass-valued normalized response.

This does not equate raw Q and R responses. A direct leading-order differentiation of the common readout correction gives, within this candidate,
\[
 T_R^j-T_Q^j\doteq-\epsilon\frac tM\langle A_x(t)\rangle_\varphi,
 \qquad
 S_R-S_Q\doteq-\epsilon\frac t{M^2}\langle A_x(t)\rangle_\varphi.
\]
Those common corrections cancel in the B-minus-A numerator and in the order-correct ratio contrast. They are not generally zero individually.

## 3. Exact finite reduction without a projected dynamics

Let X_nm=<n|q_x^2|m> in the complete Coulomb space. The initial packet has finite support, so
\[
 F_\varphi(t)=\sum_{n,m=140}^{160}c_nc_m
 e^{i(n-m)\varphi}e^{i(E_n-E_m)t/\hbar}X_{nm}.
\]
This is a matrix element of the full operator. No projected position/momentum commutator, projected Hamiltonian or closure of the21-state span is assumed.

The azimuthal factors of q_x^2=q^2*sin^2(theta)*cos^2(alpha) have magnetic weights0,+2,-2. For circular states m_z=n-1, this implies n-m=0,+2,-2. The rank0/rank2 angular decomposition and even parity allow the corresponding l differences0,+2,-2; thus these are the complete selection possibilities among the occupied circular states. The diagonal terms cancel in F(t)-F(0).

Define, for n=140,...,158,
\[
 B_n={}_c\langle n|q_x^2|n+2\rangle_c>0,
 \quad \Omega_n=(E_{n+2}-E_n)/\hbar>0,
 \quad W_n=c_nc_{n+2}B_n.
\]
With the prospectively fixed real radial functions and Condon-Shortley phase convention, B_n is real and positive. Pairing conjugate terms gives
\[
 F_\varphi(t)-F_\varphi(0)
 =2\sum_{n=140}^{158}W_n
 [\cos(2\varphi+\Omega_nt)-\cos(2\varphi)],
\]
so
\[
 \boxed{\Delta\zeta_R(t_*,\varphi)=
 \frac{6\mu}{t_*^2}\sum_{n=140}^{158}W_n
 [\cos(2\varphi)-\cos(2\varphi+\theta_n)]},
 \quad
 \theta_n=\frac{\pi150^3}{8}
 \left(\frac1{n^2}-\frac1{(n+2)^2}\right).
 \tag{4}
\]
The theta formula follows from the fixed reference a and clock in MODEL. It does not replace the finite energy gaps by one orbital frequency.

For completeness, the matrix elements in(4) can be specified without an unspecified numerical operator. Put a_C=hbar^2/(mu*C), beta_n=1/(n*a_C), and
\[
 K_n=\frac{2}{n^2a_C^{3/2}\sqrt{(2n-1)!}}
       \left(\frac{2}{n a_C}\right)^{n-1},\qquad
 R_{n,n-1}(r)=K_nr^{n-1}e^{-\beta_nr}.
\]
Then
\[
 B_n=\frac12\sqrt{\frac{n(n+1)}{(2n+1)(2n+3)}}
 K_nK_{n+2}\frac{(2n+4)!}{(\beta_n+\beta_{n+2})^{2n+5}}.
 \tag{5}
\]
To check(5), the radial measure and r^2 insertion give the integral of r^(2n+4) times exp[-(beta_n+beta_(n+2))*r]. The angular factor follows by applying sin(theta)*exp(i alpha) twice to a highest-weight spherical harmonic: each raising step has coefficient minus sqrt[2(l+1)/(2l+3)]. The relevant cos^2(alpha) term supplies1/4. With l=n-1 the product is the positive factor displayed. B_n has length-squared units. Equations(4)–(5) and the fixed c_n specify all nineteen terms exactly; no numerical evaluation was run.

## 4. What comparison is and is not decided

Let K_cl=24C/(pi^2*a)=3mu*a^2/(2t_*^2). Define the two dimensionless numbers
\[
 d_c=\frac4{a^2}\sum_n W_n(1-\cos\theta_n),\qquad
 d_s=\frac4{a^2}\sum_n W_n\sin\theta_n.
\]
The quantum contrast is K_cl[d_c*cos(2varphi)+d_s*sin(2varphi)], while the accepted classical contrast is K_cl[cos(2varphi)+sin(2varphi)]. Exact agreement as functions of the same orientation would require **both d_c=1 and d_s=1**. Equal second-harmonic form alone is insufficient. For this fixed orientation convention the uniform pointwise contrast discrepancy is exactly
\[
 K_{cl}\sqrt{(d_c-1)^2+(d_s-1)^2}.
 \tag{6}
\]
This is a comparison expression, not a new selected threshold or observable.

No value or controlled enclosure for d_c,d_s has been produced here. The smallest remaining evaluation is these two fixed nineteen-term sums, including the already specified normalization and radial factors, with sufficient error control to compare(6) to the existing event scale. There is no need to search a new spectral family, clock or model to pose that evaluation. An unevaluated sum does not establish either agreement or disagreement.

Even equality of this contrast would not determine the separate T/S functions or their unpaired marginal laws. A common phase-dependent shift can cancel from a contrast while changing each individual law. Nor does equality of a contrast clear preparation, physical interventions, a detector map or response completeness. No0-versus2/3 physical event transfer follows.

## 5. Domain, order and disposition

The required first-order difference uses only P_j*A_j and q_x^2 under the conventional H0, not nonperturbative evolution under a negative quartic truncation. The Gaussian has all required central moments. Each occupied circular state behaves as r^(n-1) near the origin and decays exponentially, with n>=140. The finite products and derivatives entering the displayed quadratic forms and endpoint identity are therefore integrable; integration-by-parts boundary terms vanish. The singular common Weyl terms have locally integrable coefficient distributions; the stated high-order vanishing removes contact-boundary contributions from the matrix elements needed here. This does not assert essential self-adjointness of the full truncated H_A/B, convergence of its perturbation expansion or a bound on discarded physical terms.

The result is independent of the stipulated central width and spin only for the isolated contrast coefficient, for the reasons in section2. It does not replace those frozen choices or identify the quantum state with the classical point preparation. All parameters, t*, controls, ordering and packet coefficients remain as prospectively saved.

**Disposition: retain the finite formal expression(4)–(5); leave P1 response agreement undecided pending the two-number comparison.** This completes one necessary comparison at the permitted finite-expression scope. P0 synthesis/repeatability, P2 physical matched controls, P3 readout/calibration, and complete omitted-response/error treatment remain open. No native DET derivation, physical gravity prediction, experiment or successor execution is claimed.

The seven exact inputs were checked before work; new review/disposition and GDM015 were freshly read, and prior complete readings of the other unchanged inputs were retained. All derivation was manual after the saved-model checkpoint. No scientific/numerical runtime, source search, Git, data, descendants or other-chat contact was used. Saved readbacks, final identities and actual completion follow before handoff; independent review and root disposition remain separate.
