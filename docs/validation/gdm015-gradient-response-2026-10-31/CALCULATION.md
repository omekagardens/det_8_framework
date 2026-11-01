# GDM015-v2 — particle-gradient sensitivity of a gravity response

**Accepted scoped formal result after distinct review and coordinator disposition.** The declared particle-gradient restoration changes both first gravity responses at formal order c^-2, including after the accepted force normalization. This is a comparison of specified truncated Hamiltonians, not a complete gravitational atom, empirical prediction, or DET derivation.

The saved premises were read before explicit stage-two release. Prior v1 exposure remains disclosed: v1 is rejected for adoption, unadmitted, and not a scientific dependency. This prospective calculation makes no claim of blind or independent reproduction.

## Models and preparation

Write epsilon=c^-2; doteq denotes equality through that formal order at fixed finite time, not a full-model error bound. Use M=2m, mu=M/4, C>0, beta=gamma=1, no radiation interaction. In old variables define
\[
K_r=\frac{p_r^2}{2\mu},\quad V_r=-\frac Cr,\quad E_r=K_r+V_r,\quad W_r=3K_r+2V_r,
\]
\[
A_{2r}=-\frac{p_r^4}{32\mu^3}
-\frac{C}{2\mu M}\left(\frac{p_r^2}{r}
+\frac{(\mathbf p_r\cdot\mathbf r)^2}{r^3}\right),\quad
X_{2r}=-\frac{(\mathbf P\cdot\mathbf p_r)^2}{2M^2\mu}
+\frac{C(\mathbf P\cdot\mathbf r)^2}{2M^2r^3}.
\]
Bold symbols are vectors; unbold r and q denote lengths. The physical spatial metric h=(1-2epsilon*phi)I and its inverse make the internal kinetic-plus-Coulomb term E_r+epsilon*phi*(2K_r+V_r). Combining this with the central coupling gives W_r, not just E_r.

Model A, with phi=-g*R_x, is the classical conservative specialization of [SG 5.5–5.6](https://arxiv.org/html/1908.06929v2), retaining its flat X before transformation:
\[
\begin{split}
H_A\doteq{}&E_r+\frac{P^2}{2M}+M\phi-fQ_x\\
&+\epsilon\left[A_{2r}+X_{2r}-\frac{P^2E_r}{2M^2}
-\frac{P^4}{8M^3}+\phi W_r+\frac{3\phi P^2}{2M}
+\frac{M\phi^2}{2}\right]. \tag{1}
\end{split}
\]
Here -fQ_x means the same transformed control below, not -fR_x. SG 3.14 has coefficient (2gamma+1)/(2Mc^2) multiplying an expression plus H.c.; commuting real classical variables double it. Consequently Model B is exactly
\[
H_B-H_A\doteq\frac{3\epsilon}{M}
(\mathbf r\cdot\nabla\phi)(\mathbf P\cdot\mathbf p_r)
=-\frac{3\epsilon g}{M}r_x(\mathbf P\cdot\mathbf p_r). \tag{2}
\]
Nothing else is restored.

Use the accepted GDM014/[SB 26](https://arxiv.org/html/1806.00234v3) canonical map:
\[
\mathbf R\doteq\mathbf Q-\epsilon\mathbf B,\quad
\mathbf B=\frac{(\mathbf q\cdot\mathbf P)\mathbf p+
(\mathbf P\cdot\mathbf p)\mathbf q}{2M^2},
\]
\[
\mathbf r\doteq\mathbf q-\epsilon\frac{(\mathbf q\cdot\mathbf P)\mathbf P}{2M^2},\qquad
\mathbf p_r\doteq\mathbf p+\epsilon\frac{(\mathbf p\cdot\mathbf P)\mathbf P}{2M^2}. \tag{3}
\]
P is unchanged. The same old-variable control is -fR_x-epsilon*f*B_x. The common canonical preparation, fixed across f,g, is Q=P=0, q=a*xhat, p=mu*a*omega*yhat. Let omega^2=C/(mu*a^3), theta=omega*t. The leading orbit is
\[
\mathbf q_0=a(\cos\theta,\sin\theta,0),\quad
\mathbf p_0=\mu a\omega(-\sin\theta,\cos\theta,0),\quad
E_0=W_0=-\frac C{2a}. \tag{4}
\]
Retain 0<=t<=t_*=pi/(4omega), collision-free and low-speed, with weak local field near g=0. These assumptions do not bound a discarded response remainder.
The A_2 term perturbs the internal orbit; inserting that perturbation into epsilon-multiplied response coefficients affects only higher formal order.

## Prospective first-variation calculation

In (1), the leading internal-energy substitution cancels X_2. Crucially, M*phi(R)=-MgQ_x+epsilon*MgB_x. Writing E,K,V,W,A_2 for the same functions of q,p gives
\[
\begin{split}
H_A\doteq{}&E+\frac{P^2}{2M}-(f+Mg)Q_x\\
&+\epsilon\left[A_2-\frac{P^2E}{2M^2}-\frac{P^4}{8M^3}
-gQ_x\left(W+\frac{3P^2}{2M}\right)
+MgB_x+\frac{Mg^2Q_x^2}{2}\right].
\end{split}\tag{5}
\]
\[
H_B-H_A\doteq-\frac{3\epsilon g}{M}q_x(\mathbf P\cdot\mathbf p).\tag{6}
\]
The following is our manual calculation. Put delta_g=partial_g at f=g=0. Both models give
\[
\delta_g\mathbf P\doteq t(M+\epsilon W_0)\hat{\mathbf x},
\qquad\delta_g\mathbf q=\delta_g\mathbf p\doteq0.
\]
Indeed internal forcing contains Q or P, both zero on the baseline. The central P^4, gQ_xP^2, and g^2Q_x^2 terms have zero relevant first variation there. The momentum derivative of gB_x survives. Since W_0=E_0 on (4),
\[
\dot T_Q^A\doteq t+\frac{\epsilon}{M}q_{0x}p_{0x},\qquad
\dot T_Q^B-\dot T_Q^A\doteq-\frac{3\epsilon}{M}q_{0x}p_{0x},
\quad T_X=\delta_g X_x.\tag{7}
\]
The second contribution must not be discarded because (6) itself vanishes at P=0. Integrating with zero response initial data yields
\[
T_Q^A\doteq\frac{t^2}{2}-\frac{\epsilon\mu a^2}{2M}\sin^2\theta,
\qquad T_Q^B\doteq\frac{t^2}{2}+\frac{\epsilon\mu a^2}{M}\sin^2\theta.\tag{8}
\]
For each model separately, the readout transformation gives
\[
T_R^j-T_Q^j\doteq-\frac{\epsilon t}{M}q_{0x}p_{0x}
=\frac{\epsilon\mu a^2\omega t}{2M}\sin(2\theta),\quad j=A,B.\tag{9}
\]
Thus the two readouts are not identified, but their B-minus-A changes coincide:
\[
\boxed{\Delta T_Q(t)\doteq\Delta T_R(t)
\doteq\frac{3\mu a^2}{2Mc^2}\sin^2(\omega t).}\tag{10}
\]

For a direct old-variable check, (1) gives
\[
\dot T_R^A\doteq t+\frac{\epsilon t}{M}
\left(-\frac{p_{0x}^2}{\mu}+\frac{Cq_{0x}^2}{a^3}\right).
\]
Equation (2) changes neither delta_g P nor the internal first variations, but adds -3epsilon*r_x*p_rx/M to dot T_R. Integration reproduces (9)–(10). This checks the generator, preparation and readout consistently without replacing the control.

## Force normalization and decision

At g=0 both Hamiltonians coincide for every f, so their force responses are the same accepted GDM014 responses:
\[
S_Q\doteq\frac{t^2}{2M}\left(1+\frac{C}{2aMc^2}\right),\qquad
S_R-S_Q\doteq\frac{\mu a^2\omega t}{2M^2c^2}\sin(2\omega t).
\]
For fixed 0<t<=t_* the leading denominator is positive; both displayed retained expressions are positive. Formal division is therefore permitted there, but not at t=0. With Z_X^j=T_X^j/S_X,
\[
\Delta Z_Q\doteq\Delta Z_R\doteq
\frac{3\mu a^2}{c^2t^2}\sin^2(\omega t).\tag{11}
\]
This equality is through c^-2 only; denominator corrections multiply an already c^-2 numerator difference. At t_*:
\[
\Delta T_Q\doteq\Delta T_R\doteq\frac{3a^2}{16c^2},\qquad
\Delta Z_Q\doteq\Delta Z_R\doteq\frac{24C}{\pi^2ac^2}>0.\tag{12}
\]
T has units time squared; S has units time squared/mass; Z has units mass.

**Decision:** the known omitted term changes the chosen normalized response at the retained order. Model A's particle-gradient neglect is not response-neutral for this protocol. Model B remains a partial restoration: SG assumes a constant metric across the pair before 4.8 and in the integration by parts at 4.20; section 5.1 discards separation-gradient terms. No complete electromagnetic-gradient theory, physical detector/control mapping, response-error bound, equivalence-principle violation, or native DET result is established. The fixed omission question is closed at this scope. Further physical or native work requires a separately justified question and review.


Accepted dependencies: [GDM014 force response](../gdm014-force-response-2026-10-31/CALCULATION.md) and [GDM013 applicability boundary](../gdm013-physical-applicability-2026-10-31/APPLICABILITY.md). See [review](REVIEW.md), [adoption](ADOPTION.md) and [source manifest](SOURCE_MANIFEST.json).
