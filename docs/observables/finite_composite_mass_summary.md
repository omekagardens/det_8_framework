# Complete one-body means do not determine composite spectral mass

**Accepted conditional mathematics.** This fixed two-preparation counterexample passed its first distinct scientific review by DET State Research and coordinator admission without repair. It concerns a supplied finite quantum model; empirical status is **NOT TESTED**.

The preparations have the same normalized one-body reduction and the same mean of every additive one-body observable, but different complete composite spectral mass laws:
\[
 \gamma_A=\gamma_B=\tfrac12 I_K,\qquad
 S_A(a)=S_B(a)=\operatorname{Tr}_K a,\qquad
 \boxed{\mu_A=\delta_0,\quad \mu_B=\delta_{\,2p_0/c}.}
\]
The constants \(c,p_0>0\), carrier, generators and spectral-observable dictionary are supplied. The conclusion rejects this mean summary as sufficient for this collective observable.

## Fixed model

Let \(K=\mathbb C^2\) have orthonormal basis \(e_+,e_-\). Supply the bosonic two-particle sector
\(\mathcal H_2=\operatorname{Sym}^2K\subset K\otimes K\), with basis
\[
 u_+=e_+\otimes e_+,\qquad
 u_0=\frac{e_+\otimes e_-+e_-\otimes e_+}{\sqrt2},\qquad
 u_-=e_-\otimes e_-.
\]
Tensor-product orthogonality gives unit norms and zero mutual inner products. A symmetric tensor has equal coefficients on \(e_+\otimes e_-\) and \(e_-\otimes e_+\), so these three vectors span \(\mathcal H_2\).

Write \(Q_j=|u_j\rangle\langle u_j|\), and fix
\[
 \rho_A=\tfrac12(Q_++Q_-),\qquad \rho_B=Q_0.
\]
In the ordered basis \((u_+,u_0,u_-)\), these are
\(\operatorname{diag}(1/2,0,1/2)\) and \(\operatorname{diag}(0,1,0)\). Both are positive, self-adjoint, trace one and supported on the sector.

The supplied one-body generators are
\[
 h=cp_0I_K,\qquad
 p_x=p_0(|e_+\rangle\langle e_+|-|e_-\rangle\langle e_-|),
 \qquad p_y=p_z=0.
\]
For Hermitian \(a\) on \(K\), define the additive lift and its mean functional by
\[
 D(a)=\left.(a\otimes I+I\otimes a)\right|_{\mathcal H_2},
 \qquad S_\rho(a)=\operatorname{Tr}_{\mathcal H_2}[\rho D(a)].
\]
The summary \(S_\rho\) includes **every** Hermitian \(2\times2\) input, not only energy and momentum. Total generators are \(H=D(h)\) and \(P_i=D(p_i)\).

## Reduction and the complete mean summary

Embed \(\rho\) in \(K\otimes K\) and use the trace-one reduction
\[
 \gamma_\rho=\operatorname{Tr}_2\rho,\qquad
 \operatorname{Tr}_K\gamma_\rho=1.
\]
The tensor identity
\[
 \operatorname{Tr}_2\!\left(|x\otimes y\rangle\langle x'\otimes y'|\right)
 =\langle y',y\rangle\,|x\rangle\langle x'|
\]
gives \(\gamma_A=I_K/2\). Expanding \(Q_0\), its two diagonal terms give half of each one-body basis projector; its two cross terms vanish because the traced factors are orthogonal. Thus \(\gamma_B=I_K/2\) as well.

The flip \(F(x\otimes y)=y\otimes x\) commutes with \(a\otimes I+I\otimes a\). Its symmetric eigenspace is therefore reducing, and \(D(a)\) is self-adjoint on all of \(\mathcal H_2\). A density operator supported there satisfies \(F\rho F=\rho\), so its two one-factor reductions agree. The partial-trace identity yields
\[
 S_\rho(a)
 =\operatorname{Tr}[\rho(a\otimes I)]
  +\operatorname{Tr}[\rho(I\otimes a)]
 =2\operatorname{Tr}_K(\gamma_\rho a).
\]
The factor two accompanies the trace-one reduction. Consequently
\[
 S_A(a)=S_B(a)=\operatorname{Tr}_K a
 \quad\text{for every Hermitian }a,
\]
including off-diagonal inputs. This establishes equality of the entire declared mean functional, not equality of all probability distributions of the lifted observables or all joint records.

## Positive mass operator and full probability laws

In the fixed sector basis,
\[
 H=2cp_0 I_{\mathcal H_2},\qquad
 P_x=2p_0(Q_+-Q_-),\qquad P_y=P_z=0.
\]
These are bounded self-adjoint operators on all of \(\mathcal H_2\). They are simultaneously diagonal, and their spectral projectors are sums of mutually orthogonal \(Q_j\). Their projections commute, providing the finite joint spectral calculus.

Define the registered contraction
\[
 \begin{aligned}
 \mathsf B
 &=\frac{H^2}{c^4}-\frac{P_x^2+P_y^2+P_z^2}{c^2}\\
 &=\frac{4p_0^2}{c^2}\bigl(I_{\mathcal H_2}-Q_+-Q_-\bigr)
 =\frac{4p_0^2}{c^2}Q_0\ge0.
 \end{aligned}
\]
Indeed, \(\langle v,\mathsf Bv\rangle=(4p_0^2/c^2)|\langle u_0,v\rangle|^2\ge0\) for every sector vector. Its unique nonnegative spectral square root is
\[
 M=\sqrt{\mathsf B}=\frac{2p_0}{c}Q_0.
\]
Every operator, product and spectral projector here has domain \(\mathcal H_2\). The raw polynomial is already bounded and closed and equals the joint-calculus operator; no unbounded-domain cancellation or closure extension is used.

Put \(m_0=2p_0/c>0\). For every Borel set \(U\subset\mathbb R\),
\[
 \mathbf1_U(M)
 =\mathbf1_U(0)(Q_++Q_-)+\mathbf1_U(m_0)Q_0.
\]
Thus the complete spectral probability laws are
\[
 \begin{aligned}
 \mu_A(U)&=\operatorname{Tr}[\rho_A\mathbf1_U(M)]=\mathbf1_U(0),\\
 \mu_B(U)&=\operatorname{Tr}[\rho_B\mathbf1_U(M)]=\mathbf1_U(m_0).
 \end{aligned}
\]
Each law has probability one at its stated support point. The event \(U=\{0\}\) has probabilities one and zero, so the laws differ. A function of the declared summary alone cannot determine both laws from the identical input \(S_A=S_B\). This disproves universal sufficiency of that summary on any state class containing the fixed pair in this model.

The separate scalar formed from mean four-momentum is
\[
 m_{\rm mean}(\rho)=\frac1{c^2}
 \sqrt{\langle H\rangle_\rho^2-c^2|\langle\boldsymbol P\rangle_\rho|^2}.
\]
Both preparations have \(\langle H\rangle=2cp_0\) and \(\langle\boldsymbol P\rangle=0\), giving \(m_{\rm mean}=2p_0/c\) for both. This common scalar does not replace either full spectral law. In particular the spectral expectations are \(0\) and \(2p_0/c\), respectively.

## Meaning and limits

The result constrains a mean-summary interface for a declared collective observable. It does not establish identical complete states, all measurement distributions, or all records. Only occupation probabilities enter the diagonal generator/mass calculation; an exclusively quantum or ontological interpretation is not justified.

The finite carrier is separately supplied. It is not a pair of normalizable continuum plane waves and has no supplied local field embedding or stress/record dictionary. Therefore no equality of local stress fields or gravitational sources, physical indistinguishability, or extension of the original continuum packet's source theorem follows. The related [spectral mass and mass formed from mean four-momentum](spectral_and_mean_four_momentum_mass.md) result supplies definition context; the present proof is self-contained.

Hilbert space, bosonic statistics, preparations, additive generators, dispersion labels, mass contraction and scales are inputs, not DET-derived quantities. The primitive-input test is not passed. No native F/L, geometry or units, physical Lorentz covariance, mass-generation law, gravitational field equation, Einstein solution, quantum anomaly, source preference or empirical discriminator is established. Option B, Status M, GDM022 exclusion and retired kappa-gravity remain unchanged.

Preparation, detection, calibration, measurement cost and efficiency remain unestablished. No apparatus, sampling protocol, scientific code, simulation or empirical experiment was used. A local-source or physical application requires the missing field, measurement and calibration premises.

## Provenance and process qualification

The exact fixed-pair result passed first distinct scientific review and coordinator admission. This note condenses the accepted proof without adding a state, case, observable, premise or claim. Detailed custody records remain separate from this public text.

The review retains a **material earlier guard-inspection error**: a failed usage check was followed by four read-only discovery commands before inspection and stopping. Later eligible work and mathematical correctness do not repair it. The pair and correlation pattern were known during design; no blind prediction, empirical prospectivity or certification of every private reasoning step is claimed. The documented execution sequence was corroborated only within the visible record's scope. Earlier planning, registration and scope-adjudication qualifications remain attached. The earlier repeated-readout packet's control-before-proof failure remains prior provenance; it is neither repaired nor attributed to this finite proof.
