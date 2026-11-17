# Complete pointer laws on native histories

**The complete pointer probability measures are unequal.** For the unchanged quadratic, Gaussian field state and unit-strength pointer instrument, both pointer means are 2, but the bounded statistic \(\cos(2\pi X_{\rm p})\) has strictly different expectations. The same common marked endpoint therefore does not determine this proposed classical source-record law under the specified attachment.

An exact characteristic function for every real argument, a normalized probability representation, and the operator-domain construction are given below. No diagnostic, field, state, coupling or native probability was retuned.

## 1. Fixed histories, field and readout

The [prepared continuation ledger](native_source_readout_response.md) fixes the
original growth probabilities and complete support. The
[three-pair Gaussian attachment](gaussian_field_transport_on_native_histories.md)
and [accepted field-state comparison](native_field_state_across_a_causal_diamond.md)
supply the unchanged field and endpoint transport. The calculation below appends
one fixed terminal instrument to these supplied mathematical resources.

Use the accepted original-law prefix \(a\prec b\), marks \((0,0)\), counters \((1,0)\). Named incomparable births satisfy
\[
 \operatorname{Past}(u)=\{a\},\qquad
 \operatorname{Past}(v)=\{a,b\},\qquad
 \operatorname{Cov}(C)=\{(a,b),(a,u),(b,v)\}.
\]
History \(H_+\) births \(u\) then \(v\); \(H_-\) births \(v\) then \(u\). Each original structural probability is \(19/1320\). For each named pair \((m_u,m_v)\in\{0,1\}^2\), chronological bits are \((m_u,m_v)\) and \((m_v,m_u)\), respectively, with probability \(19/5280\) for each marked history. Transported terminal counters are \((3,1,0,0)\) in endpoint order \((a,b,u,v)\). All 60 original marked continuations remain.

The [Gaussian attachment](gaussian_field_transport_on_native_histories.md) fixes the three canonical pairs and the centered product Gaussian \(\psi\), with quadrature column
\[
 R=(Q_0,P_0,Q_x,P_x,Q_y,P_y)^T,\quad
 [R_j,R_k]=iJ_{jk},\quad
 J=\bigoplus_3\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]
and symmetric covariance \(I_6/2\). The roles \(x,y\) remain actual first/later births before endpoint transport. The [accepted diamond proof](native_field_state_across_a_causal_diamond.md) supplies the exact transported fields and their unequal full states.

For the supplied normalization \(\beta>0\), define the three dimensionless cover differences in the fixed cover order:
\[
 d_1=(\phi_b-\phi_a)/\sqrt\beta,\quad
 d_2=(\phi_u-\phi_a)/\sqrt\beta,\quad
 d_3=(\phi_v-\phi_b)/\sqrt\beta.
\]
Then \(d^\pm=A_\pm R\), with
\[
 A_+=\begin{pmatrix}
 -1&-1&0&0&0&0\\
 -1&-1&1&0&0&0\\
 -1&0&0&1&1&0
 \end{pmatrix},\qquad
 A_-=\begin{pmatrix}
 -1&-1&0&0&0&0\\
 -1&-1&0&-1&1&0\\
 -1&0&1&0&0&0
 \end{pmatrix}.
\]
The unchanged diagnostic is
\[
 Q_\pm=\mathcal Q_C^\pm
       =\frac12\big((d_1^\pm)^2+(d_2^\pm)^2+(d_3^\pm)^2\big).
 \tag{1}
\]
Its \(\beta\) cancels because the accepted field rows each carry \(\sqrt\beta\). This is the stipulated dimensionless normalization, not a derived physical unit.

## 2. Closed form, Friedrichs realization and the pointer interaction

Initially take (1) on \(\mathscr S(\mathbb R^3)\). Let
\[
 T_0 f=2^{-1/2}(d_1f,d_2f,d_3f),\qquad
 q_0[f]=\|T_0f\|^2.
\]
Every \(d_j\) is a real linear position/momentum operator, symmetric on Schwartz space and preserving it. If \(f_n\to0\) while \(T_0f_n\to v\), then for every Schwartz test vector \(h\),
\[
 \langle v_j,h\rangle
 =2^{-1/2}\lim_n\langle f_n,d_jh\rangle=0.
\]
Density gives \(v=0\), so \(T_0\) is closable. Its graph closure gives the closed nonnegative form
\[
 \bar q[f]=\|\bar T_0 f\|^2,\qquad D(\bar q)=D(\bar T_0).
\]
The associated self-adjoint operator is
\[
 Q_F=\bar T_0^{\,*}\bar T_0\ge0.
 \tag{2}
\]
For example, Riesz representation in the graph inner product
\(\langle u,v\rangle+\langle\bar T_0u,\bar T_0v\rangle\)
constructs the positive symmetric resolvent \((I+Q_F)^{-1}\). This is the Friedrichs realization of the original sum of squares. It requires no assumption about the domain of a separately closed algebraic sum. On Schwartz space it agrees with (1), preserves Schwartz space, and the Gaussian belongs to \(D(Q_F^n)\) for every finite \(n\). Hereafter \(Q_\pm\) denotes this specified realization.

Add exactly the supplied independent pointer, with the fixed unit-strength interaction formally written \(U=e^{-iQ\otimes P_{\rm p}}\) and defined spectrally below:
\[
 \mathcal H_{\rm p}=L^2(\mathbb R),\quad
 [X_{\rm p},P_{\rm p}]=i,\quad
 g(x)=\pi^{-1/4}e^{-x^2/2}.
\]
Define the tensor generator through the joint spectral measure of operators on separate factors:
\[
 A_{\rm int}=\int \lambda p\,d(E_Q\otimes E_P)(\lambda,p),
 \qquad
 U=\int e^{-i\lambda p}\,d(E_Q\otimes E_P)(\lambda,p).
 \tag{3}
\]
The real spectral multiplier is self-adjoint on its natural square-integrability domain, and \(U\) is unitary on the whole tensor Hilbert space. Thus the stated exponential is defined without a formal unbounded-operator multiplication argument.

Let
\(\nu_\pm(B)=\langle\psi,E_{Q_\pm}(B)\psi\rangle\).
It is a normalized measure on \([0,\infty)\). Translation has the sign
\(e^{-i\lambda P_{\rm p}}g(x)=g(x-\lambda)\).
The complete measured-position law is consequently
\[
 \boxed{\quad
 \mu_\pm(dx)=
 \left[\int_{[0,\infty)}
       \frac{e^{-(x-\lambda)^2}}{\sqrt\pi}\,
       \nu_\pm(d\lambda)\right]dx .
 \quad}                                                   \tag{4}
\]
This follows by applying the orthogonal spectral resolution in (3), rather than assigning simultaneous classical values to the cover operators. It proves positivity, countable additivity and normalization. All real outcomes, including negative pointer readings, are retained.

Use the characteristic-function convention
\[
 \widehat\mu_\pm(t)=\int_{\mathbb R}e^{itx}\mu_\pm(dx).
\]
Equation (4) gives
\[
 \widehat\mu_\pm(t)
 =e^{-t^2/4}\langle\psi,e^{itQ_\pm}\psi\rangle .
 \tag{5}
\]

## 3. Quantum normal form and the exact full laws

Direct CCR and ordinary row products give
\[
 [d_1,d_3]=-i,\qquad [d_1,d_2]=[d_2,d_3]=0,
\]
\[
 G_+:=A_+A_+^T=
 \begin{pmatrix}2&2&1\\2&3&1\\1&1&3\end{pmatrix},\qquad
 G_-:=A_-A_-^T=
 \begin{pmatrix}2&2&1\\2&4&1\\1&1&2\end{pmatrix}.
 \tag{6}
\]
The symmetric covariances of \(d\) are \(G_\pm/2\). Both Gram matrices are positive definite: their leading principal minors are \((2,2,5)\) and \((2,4,6)\).

Put
\[
 X=d_1,\qquad P=-d_3,\qquad Z=d_2 .
\]
Then \([X,P]=i\), while \(Z\) strongly commutes with \(X,P\): the corresponding linear-field Weyl groups commute exactly. Symplectic completion of these independent real linear forms makes \(X,P\) one canonical pair and \(Z\) another position coordinate, with an unused final pair. This change of analysis coordinates is implemented by a finite linear canonical transformation preserving Schwartz space. It neither changes the field map nor introduces a new carrier or dynamics.

In these coordinates the closed form (2) is the strongly commuting sum
\[
 Q=H_{\rm osc}+Z^2/2,\qquad
 H_{\rm osc}=(X^2+P^2)/2.
 \tag{7}
\]
Tensor products of oscillator Schwartz functions and smooth compactly supported functions in the remaining coordinates form a core; transporting back identifies this sum with the same Friedrichs realization. The Gaussian may correlate \(Z\) with \(X,P\). No product-state assumption in these transformed coordinates is made. The symbol \(H_{\rm osc}\) is a spectral normal form of the fixed readout operator, not the deferred proposal for a physical or native evolution generator.

For completeness, derive a global characteristic formula. For \(z>0\), the oscillator heat operator has Weyl symbol
\[
 \big(e^{-zH_{\rm osc}}\big)_W
 =\operatorname{sech}(z/2)
   \exp[-\tanh(z/2)(X^2+P^2)] .                         \tag{8}
\]
The factor of one half follows from the normalization of \(H_{\rm osc}\). The primary-source normalization check is §1.1, page 1 of Karel Pravda-Starov, *Generalized Mehler formula for time-dependent non-selfadjoint quadratic operators and propagation of singularities*, [arXiv:1703.02797v2](https://arxiv.org/pdf/1703.02797v2), dated 28 May 2017. Its oscillator is \(-\Delta+x^2\), so its semigroup parameter is \(z/2\) here. Only this opening oscillator normalization is used; the source’s general time-dependent theorem is not imported.

A direct check of (8) also fixes the signs. For a radial symbol \(a=A(z)e^{-B(z)(X^2+P^2)}\), the quadratic Weyl product gives
\[
 \partial_z a=-\tfrac12(X^2+P^2)a+\tfrac18\Delta a.
\]
The equations \(B'=(1-B^2)/2\), \(A'/A=-B/2\), with \(B(0)=0,A(0)=1\), give (8). Multiplication by \(e^{-zZ^2/2}\) introduces no star-product correction because \(Z\) commutes with the pair.

The Weyl expectation in the original Gaussian is the phase-space Gaussian integral with covariance \(G_\pm/2\). This is an integral of a Weyl symbol, not a joint measurement law for \(d_1,d_2,d_3\). With \(\alpha=\tanh(z/2)\), that integral yields
\[
 \langle e^{-zQ_\pm}\rangle
 =\frac{\operatorname{sech}(z/2)}
 {\sqrt{\det\!\left(I+G_\pm
                    \operatorname{diag}(\alpha,z/2,\alpha)\right)}}.
 \tag{9}
\]
The square root is positive for positive real \(z\). The formula extends analytically to \(\operatorname{Re}z>0\): both \(\operatorname{Re}z\) and \(\operatorname{Re}\tanh(z/2)\) are positive there, so the Gaussian integral remains convergent. The spectral Laplace transform has the same analytic continuation.

For real \(t\), set
\[
 c=\cos(t/2),\quad s=\sin(t/2),\quad
 D_t=\operatorname{diag}(c,1,c),\quad
 E_t=\operatorname{diag}(s,t/2,s),
\]
\[
 F_\pm(t)=\det(D_t-iG_\pm E_t).
 \tag{10}
\]
Multiplying out the two determinants gives
\[
 \begin{aligned}
 F_+(t)&=c^2-5s^2-5t sc
   +i\left[-5sc-\tfrac32tc^2+\tfrac52ts^2\right],\\
 F_-(t)&=c^2-3s^2-\tfrac{11}{2}t sc
   +i\left[-4sc-2tc^2+3ts^2\right].
 \end{aligned}                                             \tag{11}
\]

There is no real zero of either determinant. If
\((D_t-iG_\pm E_t)v=0\), put \(w=E_tv\). Then
\[
 w^\dagger D_tv=v^\dagger E_tD_tv
               =i\,w^\dagger G_\pm w.
\]
The left side is real and the right side is purely imaginary. Positivity of \(G_\pm\) forces \(w=0\), then \(D_tv=0\). No coordinate of \(D_t\) and \(E_t\) vanishes simultaneously, hence \(v=0\).

Let \(r_\pm(t)\) be the unique continuous square root of \(F_\pm(t)\) along the real line with \(r_\pm(0)=1\). Taking the spectral boundary value \(z\to0^+-it\) in (9) therefore gives the complete answer
\[
 \boxed{\qquad
 \widehat\mu_\pm(t)=\frac{e^{-t^2/4}}{r_\pm(t)},
 \qquad r_\pm(t)^2=F_\pm(t),\quad r_\pm(0)=1,
 \qquad t\in\mathbb R .
 \qquad}                                                  \tag{12}
\]
The right-half-plane construction fixes the same continuous branch across all apparent oscillator caustics. A pointwise principal square root of (11) would be wrong. Equations (4) and (12) together supply normalized probability measures and explicit characteristic functions on the entire real line; they uniquely specify the full laws. In particular, the density is the absolutely convergent inverse Fourier integral of (12), since the spectral factor has modulus at most one and the pointer factor is Gaussian.

## 4. A bounded real statistic separates the laws

An exact witness avoids any branch ambiguity in evaluating (12). In the regular canonical representation, \(H_{\rm osc}\) has levels \(n+1/2\), so
\[
 e^{i2\pi H_{\rm osc}}=-I,\qquad
 e^{i2\pi Q_\pm}=-e^{i\pi Z_\pm^2}.
 \tag{13}
\]
The spectral marginal of the single linear field \(Z\) is a centered Gaussian. From (6),
\[
 \operatorname{Var}_+(Z)=3/2,\qquad
 \operatorname{Var}_-(Z)=2.
\]
Correlations with \(X,P\) do not enter (13). The elementary one-variable Gaussian integral and the independent pointer factor give
\[
 \widehat\mu_+(2\pi)
 =-e^{-\pi^2}(1-3i\pi)^{-1/2},\qquad
 \widehat\mu_-(2\pi)
 =-e^{-\pi^2}(1-4i\pi)^{-1/2}.                         \tag{14}
\]
The square roots in (14) are principal roots after extracting the oscillator minus sign. Equivalently, the continuously continued roots in (12) at this argument are minus those principal roots.

For \(a>0\), define
\[
 f(a)=\operatorname{Re}(1-ia)^{-1/2}
     =\sqrt{\frac{\sqrt{1+a^2}+1}{2(1+a^2)}}.
\]
It is strictly decreasing: writing \(r=\sqrt{1+a^2}\), the derivative of \(f^2=(r+1)/(2r^2)\) with respect to \(r\) is \(-(r+2)/(2r^3)<0\). Thus the fixed bounded real statistic of the same recorded position satisfies
\[
 \boxed{\quad
 \mathbb E_+\cos(2\pi X_{\rm p})
   =-e^{-\pi^2}f(3\pi)
   <-e^{-\pi^2}f(4\pi)
   =\mathbb E_-\cos(2\pi X_{\rm p}).
 \quad}                                                    \tag{15}
\]
This proves \(\mu_+\ne\mu_-\). The statistic is classical postprocessing of the fixed complete position record; no pointer setting, threshold or coupling was changed.

The means remain 2. In (6), both traces are 8, so \(\langle Q_\pm\rangle=\operatorname{tr}G_\pm/4=2\); the independent pointer starts at zero mean. The accepted unequal field states, the agreeing diagnostic and pointer means, and the newly unequal complete pointer laws are three separate statements.

## 5. Native marginal and scope

The field rule does not depend on the suffix marks, so (12)–(15) hold separately for all four matched named mark assignments. Their original \(19/5280\) probabilities are retained. Comparing conditional laws does not equate the distinct native history labels in the joint audit record.

To make the complete appended law explicit, use the same terminal finite-cover sum and form construction for every one of the original 60 histories. Each has finitely many real linear cover fields, so the closability argument of §2 supplies its nonnegative Friedrichs realization and normalized pointer kernel. Formula (4) then defines that kernel without evaluating its density. For every history \(H\),
\[
 \Pr(H,B)=P_0(H)\mu_H(B),\qquad
 \Pr(H,\mathbb R)=P_0(H),\qquad
 \sum_H\Pr(H,\mathbb R)=1.
\]
This proves preservation of the native marginal on the other 52 histories as well as the compared eight, without extra diamond calculations. There is no postselection, history reweighting or feedback. Post-interaction field-state preservation is not asserted.

**Registration verdict.** Under this fixed supplied terminal instrument, the common marked endpoint and agreeing diagnostic mean do not determine the complete classical pointer law. The tested source record retains sensitivity to the birth ordering. This is a finite conditional counterexample, not a statement that every possible source readout must depend on a schedule, nor a minimal-register classification.

The proof uses the declared canonical field and independent pointer resources. It does not derive their availability from DET or identify the readout as physical energy, stress, mass, time, gravitational coupling or a calibrated detector. No empirical discrimination or sampling-cost claim follows from the exact nonzero contrast. The [PIM001 known-answer implementation](../../research/provisional_integrated_model/PIM001/README.md) remains a separate reproduction result; the present proof is analytic. The accepted full-field covariance failure remains intact.

## Scientific provenance

DET Quantum Relativity authored this result. DET Energy Research completed the
distinct nonblind scientific result review, and the coordinator accepted it with
scope on 16 November 2026. The prior Relational State design review and the
author's two mathematical helpers were separate from that scientific verdict.
Energy checked the form and spectral construction, complete laws, global branch,
bounded witness and preservation of the original native marginal, reusing the
accepted field and growth results. No author correction was required.

This article presents the accepted fixed-instrument result. It does not add a
new detector, diamond, field repair, dynamics or empirical claim. Option B and
Status M remain unchanged.
