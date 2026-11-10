# Gaussian field transport on the registered histories

**Decision.** A fixed centered Gaussian state on three dimensionless canonical pairs realizes the registered causal commutator and preserves the exact old-field state at both births, branch by branch. It extends the accepted two-event covariance $W_2$. The construction changes fresh spectral state selection and keeps the instantaneous commutator zero modes as observables with fluctuations. The stagewise kernel-as-zero quotient obstructs the specified old-operator inclusion on a supported branch, independently of state choice.

## Inputs and convention

The prepared order is $a\prec b$, with marks $(i,0)$ and counters $(1,0)$, for $i=0,1$. Use the original 15 ideal sequences $I_x,I_y$, with four fair suffix-mark pairs for each sequence. Let $P_i(H)$ be the given probability of one of the 60 marked histories conditional on that preparation. The ideal of each birth gives its full strict past. The construction uses only that current order and the fixed inherited roles of $a,b,x,y$. [Exact interval and continuation table](finite_interval_action_and_source_preparation.md) · [Prepared source ledger](native_source_readout_response.md)

Write $c_{rs}=\mathbf 1_{\{s\prec r\}}$. With target row and source column, $K_R=\beta C$ for a single supplied $\beta>0$, $D=\beta(C-C^T)$, and the prescribed commutator is $[\phi_r,\phi_s]=iD_{rs}\mathbf 1$. In particular $D_{ab}=-\beta$. Use the accepted prefix second moment in the order $a,b$,
$$
  W_2=\frac{\beta}{2}\begin{pmatrix}1&-i\\i&1\end{pmatrix}.
$$
The accepted field-prefix result excludes fresh positive spectral assignment at every birth under this identification. Here the covariance comes from a single supplied state and explicit field operators. [Accepted field-prefix report](spectral_covariance_under_native_growth.md)

Johnston v2 uses the difference of retarded and advanced kernels in Eq. (18), the field commutator in Eq. (22), and imposes the additional operator identity for all commutator zero modes in Eq. (23). The accepted field-prefix report converts the source-first paper indexing to the target-first convention above. A transpose changes the sign of the skew matrix and preserves its kernel. The following inclusion test uses that kernel with the registered target-first signs. [Johnston, arXiv:0909.0944v2, §II Eqs. (18)–(23)](https://arxiv.org/pdf/0909.0944v2)

## A single state and a causal field map

Reserve the three canonical pairs $(Q_0,P_0),(Q_x,P_x),(Q_y,P_y)$ on one Hilbert space $L^2(\mathbb R^3)$. The dimensionless convention is $[Q_j,P_k]=i\delta_{jk}\mathbf 1$, and the position-position and momentum-momentum commutators vanish. Use the Schrödinger position and momentum operators with the common Schwartz domain for the linear fields. The state $\omega$ is the vector state of the normalized real Gaussian
$$
 \psi(q_0,q_x,q_y)=\pi^{-3/4}
      \exp[-(q_0^2+q_x^2+q_y^2)/2].
$$
It has zero means, symmetrized covariance $I_6/2$, and a Gaussian characteristic function for all real linear combinations. For the ordered quadrature column $R=(Q_0,P_0,Q_x,P_x,Q_y,P_y)^T$, put $J=\bigoplus_{j=0,x,y}\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$. Then $\omega(R_jR_k)=(I_6+iJ)_{jk}/2$. This state is fixed before either suffix birth and is common to both prepared bits and all continuations. The pairs and Gaussian are supplied mathematical resources.

At the two-event preparation and the third birth define
$$
 \phi_a=\sqrt{\beta}\,Q_0,\qquad
 \phi_b=-\sqrt{\beta}\,P_0,\qquad
 \phi_x=\sqrt{\beta}\,(Q_x-c_{xb}Q_0-c_{xa}P_0).
$$
The definition of $\phi_x$ uses $I_x$ only. At the fourth birth set
$$
 \rho=c_{yx}-c_{yb}c_{xa}+c_{ya}c_{xb},\qquad
 \phi_y=\sqrt{\beta}\,(Q_y-c_{yb}Q_0-c_{ya}P_0-\rho P_x).
$$
The coefficients here use only $I_x,I_y$ at the time $y$ is born. The earlier operators are the same operators on the same Hilbert space. Three pairs suffice simultaneously as a resource bound, one for $a,b$ and one reserved for each suffix birth. The factors of one on the two new position quadratures and the variance $1/2$ in each dimensionless quadrature are explicit choices. The $-\rho P_x$ term compensates the contribution of the shared first pair to the last commutator.

## Signs and positivity on the complete support

For $r=x,y$, the terms on pair $0$ give
$$
 [\phi_r,\phi_a]=i\beta c_{ra}\mathbf 1,\qquad
 [\phi_r,\phi_b]=i\beta c_{rb}\mathbf 1.
$$
The first pair gives $[\phi_a,\phi_b]=-i\beta\mathbf 1$. For the two suffix fields, the first pair contributes $i\beta(c_{yb}c_{xa}-c_{ya}c_{xb})\mathbf 1$, and $-\rho P_x$ against $Q_x$ contributes $i\beta\rho\mathbf 1$. Hence $[\phi_y,\phi_x]=i\beta c_{yx}\mathbf 1$. These calculations use strict precedence bits of the actual order, so they give all matrix entries with the registered sign, including zero on unrelated pairs. Earlier comparabilities are inherited at each birth.

At any stage write the column of fields as $\sqrt\beta\,L R$, with $L$ the corresponding real matrix of the displayed coefficients. In the two-point convention $W_{rs}=\omega(\phi_r\phi_s)$, the second-moment matrix $W$ and real symmetrized covariance $V$ are
$$
 W=\frac{\beta}{2} L(I_6+iJ)L^T,\qquad
 V=\frac{\beta}{2}LL^T,\qquad
 W-W^T=i\beta LJL^T=iD .
$$
Each $2\times 2$ block of $I_6+iJ$ has eigenvalues $0,2$. Thus $W$ is positive semidefinite. Equivalently, $u^\dagger W u=\omega(\Phi(u)^\dagger\Phi(u))\ge 0$ for $\Phi(u)=\sum_r u_r\phi_r$. The first two rows give the prescribed $W_2$ exactly. The real symmetric covariance is positive definite on the displayed field labels: the unique $Q_y$ coefficient forces the coefficient of $\phi_y$ to vanish in a zero combination, the $Q_x$ coefficient then forces the coefficient of $\phi_x$ to vanish, and the $Q_0,P_0$ coefficients force those of $\phi_a,\phi_b$ to vanish. The same argument applies to the truncated row lists.

For any real $g\in\ker D$ of the current stage, $\Phi(g)$ commutes with all fields of that stage and its variance is $\frac{\beta}{2}\|L^Tg\|^2$, strictly positive for $g\ne0$. These are retained central fluctuations in the current field algebra. The ancillary quadratures allow a central observable at one stage to acquire a commutator with a later field.

## Branchwise and unread preservation

In a continuation, adding a row to $L$ keeps every earlier row fixed. Hence every old principal block of both $W$ and $V$ equals the corresponding earlier covariance. The restriction of the full state on old observables also agrees. A real smearing $u$ at an old stage has Weyl characteristic function
$$
  \omega(e^{i\Phi(u)})=\exp(-u^TVu/2),
$$
and the corresponding Weyl operators and their products are identical before and after the extension on that branch. The preparation of $\omega$ is independent of the native records. Choosing the newly appended observable according to the realized ideal leaves the old operator and its state intact.

At the prepared pair, each terminal history therefore has restriction $W_4(H)[a,b;a,b]=W_2$. Summing against the original marked probabilities gives
$$
 \sum_{H=1}^{60} P_i(H) W_4(H)[a,b;a,b]
   =W_2\sum_{H=1}^{60}P_i(H)=W_2,\qquad i=0,1 .
$$
A particular marked three-event prefix has the same restriction identity for the old $a,b,x$ covariance under each allowed fourth birth. Averaging it uses the original normalized conditional law given that prefix. The same linear averaging applies to the expectation of any bounded old observable in the represented field algebra. All fair marks and structural rows keep their original probability, with no field feedback to the native law.

## Why changing the state alone is insufficient with the quotient

With a stagewise kernel-as-zero rule, the label inclusion from a prefix to a continuation must send every old commutator zero mode to a new zero mode. In fact an old linear combination set to the zero operator must still commute with the newly appended field. For the coefficient-vector inclusion $\iota$ by a final zero entry, this requires $\iota(\ker D_{\rm old})\subseteq\ker D_{\rm new}$.

Use the registered row $I_x=\varnothing,\ I_y=\{x\}$. The three-event order has $a\prec b$ and isolated $x$. The fourth event satisfies $x\prec y$ with no predecessors among $a,b$. The original structural probability is $(1/5)(1/44)=1/220$ for each prepared bit, or $1/880$ for each of its four marked histories. The old $e_x$ belongs to $\ker D_3$, so the old quotient would impose $\phi_x=0$. But $(D_4\iota e_x)_y=\beta$ and $[\phi_y,\phi_x]=i\beta\mathbf 1$ on this very extension. The old zero operator cannot realize that commutator. The obstruction is to inclusion of the quotiented algebras and is independent of covariance or Gaussianity. [Registered structural row and weights](native_source_readout_response.md)

With the retained center, this same row gives $\phi_x=\sqrt\beta Q_x$ and $\phi_y=\sqrt\beta(Q_y-P_x)$. The old central field has variance $\beta/2$ and becomes noncentral in the enlarged field algebra with precisely the required commutator. The accepted spectral rule fails at the covariance level. Replacing its state alone while keeping Eq. (23) at each prefix encounters the operator obstruction above. The given Gaussian extension changes both premises and realizes the stipulated inclusion.

## Scope and custody

The native law supplies the conditional orders and weights. The retarded benchmark, $\beta$, fixed label identification, ancillary canonical pairs, Gaussian state and field coefficients are declared premises or choices. The derived quantities are commutators, second moments and old-state restrictions in this normalization. For example the variance of $x$ in the displayed row is $\beta/2$, with dimensionless ratio $1/2$ to $\beta$. Central fields are mathematical observables in the represented algebra. An operational instrument, a calibrated field scale, carrier inertia, an energy generator and its dynamics, an action unit and a physical clock would require separate physical premises. This finite construction supplies a positive kinematic interface on the registered support.


The construction uses three canonical pairs on an infinite-dimensional Hilbert space. This is a finite mode-count bound, not an energy, physical cost or finite-dimensional state-space certificate.
