# GDM014 — equal baseline centers need not have equal force responses

**Coordinator-adopted formal result after independent review:** the specified circular electromagnetic baseline has \(Q=R\) without forcing, but \(S_Q\ne S_R\) at a finite time through order \(c^{-2}\), under the same stipulated drive. Transferring the force-reference denominator between these two observables requires the correction below.

Here \(\doteq\) means equality of formal coefficients through \(c^{-2}\), at fixed parameters and finite time. It is not a rigorous remainder bound for a full electromagnetic system.

## Source and order check

SB is [Sonnleitner–Barnett, arXiv:1806.00234v3](https://arxiv.org/html/1806.00234v3); SG is [Schwartz–Giulini, arXiv:1908.06929v2](https://arxiv.org/html/1908.06929v2). SB explicitly permits the classical Poisson interpretation before §IV. Use its Eqs.18,24–29, checked against SG Appendix A: corrected 12*,23* have negative quartic kinetic terms; 25b* restores the missing momentum square. SG reproduces 25c,25f and26a–c without correction marks. Its §5.1 and Eqs.5.5–5.6 confirm the relevant zero-gravity terms. Radiation-sector corrections do not enter the selected conservative baseline.

Take \(m_1=m_2=m>0\), \(M=2m\), \(\mu=M/4\), and \(C=e_{\rm charge}^2/(4\pi\epsilon_0)>0\). The Newtonian center is \(\mathbf R=(\mathbf r_1+\mathbf r_2)/2\). Bold symbols are vectors; \(q=|\mathbf q|\), \(P^2=\mathbf P\cdot\mathbf P\). Source formulas specialized to commuting real classical variables give
\[
 A_0=\frac{p^2}{2\mu}-\frac Cq,\qquad
 A=A_0+\frac{A_2}{c^2},\qquad
 A_2=-\frac{p^4}{32\mu^3}
 -\frac{C}{2\mu M}\left(\frac{p^2}{q}
             +\frac{(\mathbf p\cdot\mathbf q)^2}{q^3}\right).
 \tag{1}
\]
An expression plus H.c. becomes twice that expression. The equal-mass canonical transformation is
\[
\begin{aligned}
 \mathbf R&\doteq\mathbf Q-\frac{\mathbf B}{c^2},
 &\mathbf B&=\frac{(\mathbf q\cdot\mathbf P)\mathbf p+
                  (\mathbf P\cdot\mathbf p)\mathbf q}{2M^2},\\
 \mathbf r&\doteq\mathbf q-\frac{(\mathbf q\cdot\mathbf P)\mathbf P}{2M^2c^2},
 &\mathbf p_r&\doteq\mathbf p+\frac{(\mathbf p\cdot\mathbf P)\mathbf P}{2M^2c^2}.
\end{aligned}\tag{2}
\]
Total \(\mathbf P\) is unchanged. SB29 suppresses the central quartic term; retain it from corrected25b*/SG5.5 to check its actual variation. With \(\mathbf n=\hat{\mathbf x}\), our prescribed Hamiltonian is
\[
 H_f\doteq A+\frac{P^2}{2M}
 -\frac{P^2A_0}{2M^2c^2}-\frac{P^4}{8M^3c^2}
 -f Q_x. \tag{3}
\]
The last term is an additional mathematical control hypothesis, not a sourced laboratory force. Equations (1)–(3) define the selected conservative approximation; the following response calculation is our own.

| Term or substitution | Role at first order in \(f\), about \(\mathbf P=0\) |
|---|---|
| \(P^2/(2M)\) | Supplies leading central response. |
| \(-P^2A_0/(2M^2c^2)\) | Nonzero momentum Hessian; retain. |
| \(-P^4/(8M^3c^2)\) | Velocity is cubic in \(P\); zero first variation. |
| \(A_2/c^2\) | Corrects internal orbit; its insertion into another \(c^{-2}\) term affects only higher formal order. |
| \(-\mathbf B/c^2\) | Vanishes at baseline; its momentum derivative survives. |
| Transformed drive correction | Linear in \(f\); cannot discard it using a radiation-coupling hierarchy. |

## Preparation and response

Hold the same canonical initial state for every \(f\):
\[
 \mathbf Q(0)=\mathbf P(0)=0,\quad
 \mathbf q(0)=a\hat{\mathbf x},\quad
 \mathbf p(0)=p_0\hat{\mathbf y},\qquad a>0.
\]
Hamilton's equations from \(A_0\) are
\(\dot{\mathbf q}=\mathbf p/\mu\), \(\dot{\mathbf p}=-C\mathbf q/q^3\).
Consequently the leading circular orbit requires
\[
 \omega=\sqrt{\frac{C}{\mu a^3}},\quad p_0=\mu a\omega,\quad
 \mathbf q_0=a(\cos\omega t,\sin\omega t,0),\quad
 \mathbf p_0=\mu a\omega(-\sin\omega t,\cos\omega t,0),
 \quad E_0=A_0=-\frac{C}{2a}. \tag{4}
\]
Assume \(a\omega/c\ll1\), \(|f|T/(Mc)\ll1\) near zero force, and a compact collision-free interval containing \(0\le t\le T=\pi/(4\omega)\). All parameters and \(T\) are fixed as the expansion is taken. The full truncated internal orbit need not be exactly circular; (4) suffices inside terms already multiplied by \(c^{-2}\).

Write \(\delta=\partial_f|_{f=0}\). Equation (3) gives
\[
 \mathbf P_f=ft\mathbf n,\qquad
 \delta\mathbf P=t\mathbf n,\qquad
 \delta\mathbf q=\delta\mathbf p=0. \tag{5}
\]
The last equalities follow because the internal forcing from \(P^2\) is quadratic in \(f\), with fixed initial data. At baseline \(A_0(t)=E_0\) to leading order. Thus
\[
 S_Q(t)=\delta Q_x(t)\doteq
 \frac{t^2}{2M}\left(1-\frac{E_0}{Mc^2}\right)
 =\frac{t^2}{2M}\left(1+\frac{C}{2aMc^2}\right). \tag{6}
\]
Although \(\mathbf R_0=\mathbf Q_0=0\), differentiate (2) before setting \(P=0\):
\[
 \boxed{S_R(t)-S_Q(t)\doteq
 -\frac{t\,q_{0x}(t)p_{0x}(t)}{M^2c^2}
 =\frac{\mu a^2\omega t}{2M^2c^2}\sin(2\omega t).} \tag{7}
\]
At \(t_*=\pi/(4\omega)\),
\[
 S_R(t_*)-S_Q(t_*)\doteq\frac{\pi\mu a^2}{8M^2c^2}>0
 \quad\text{at the retained order}. \tag{8}
\]
It vanishes at \(t=0\); the oscillatory coefficient also has discrete later zeros where \(\sin(2\omega t)=0\), if those times lie within the chosen validity interval. This is not equality for all times. The dimensions are displacement/force, \( {\rm time}^2/{\rm mass}\).

## Same intervention in the original variables

Inverting (2), the same control is
\[
 -fQ_x\doteq-fR_x-\frac f{c^2}B_x(\mathbf r,\mathbf p_r,\mathbf P). \tag{9}
\]
The unforced Hamiltonian in these variables also retains the source cross term
\[
 \frac{X_2}{c^2}=\frac1{c^2}
 \left[-\frac{(\mathbf P\cdot\mathbf p_r)^2}{2M^2\mu}
       +\frac{C(\mathbf P\cdot\mathbf r)^2}{2M^2r^3}\right]. \tag{10}
\]
Substitution of (2) into the leading internal energy produces
\(+(\mathbf P\cdot\mathbf p)^2/(2M^2\mu c^2)
-C(\mathbf P\cdot\mathbf q)^2/(2M^2q^3c^2)\), cancelling (10).
This explicitly checks the source cancellation in the equal-mass case.

At the common initial \(P=0\), all initial variables agree to this order; the relative-coordinate shifts are quadratic in \(P\), so their first variations also vanish. Equations (9)–(10) independently give
\[
 \dot S_R-\dot S_Q\doteq
 \frac{t}{M^2c^2}
 \left(-\frac{p_{0x}^2}{\mu}+\frac{Cq_{0x}^2}{a^3}\right)
 -\frac{q_{0x}p_{0x}}{M^2c^2},
\]
exactly the derivative of (7), using (4).

Replacing (9) by \(-fR_x\) removes its momentum-dependent term and changes the intervention. In \(Q\) variables that alternative adds \(+fB_x/c^2\) to (3), contributing \(+f q_xp_x/(M^2c^2)\) to \(\dot Q_x\) at first order. It is not a re-expression of the same force. Nor are \(Q_x\) and \(R_x\) the same observable: a coordinate change preserves a consistently transformed observable, not an untransformed coordinate label.

## Decision and limits

The mechanical denominator cannot be transferred merely from baseline equality of centers. Equation (7) is the required correction in this precise conventional model/protocol. It is neither a new force nor an equivalence-principle violation.

The calculation does not realize the drive, preparation, clock or detector physically. Radiation, other omitted physical effects and full-model response remainders have not been bounded; a formal coefficient is not a measurable error margin. No gravity numerator, normalized discrimination, spring-to-atom correspondence or DET derivation follows. Retain the scoped GDM012 theorem and GDM013 adjudication. Stop this completed calculation for distinct review and coordinator disposition.

Both version metadata and the cited formulas with surrounding definitions were read, including SG's relevant correction appendix. Coverage is recorded in SOURCE_PINS; neither full-paper validation nor immutable remote byte custody is claimed. No scientific runtime or experiment was used.
