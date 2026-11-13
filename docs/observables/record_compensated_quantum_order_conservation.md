# Record-compensated quantum-and-order conservation across multi-birth causal diamonds

**Decision.** Over the unchanged four-birth structural domain and seed kernel of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), an unscaled, bounded-spectrum co-rotating two-level qubit observable $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ ($\operatorname{Spec}(H_n)=\{E_0-\frac{\varepsilon}{2},E_0+\frac{\varepsilon}{2}\}$, $\varepsilon>0$) coupled to causal-order growth on $\mathcal H_Q=\mathbb C^2$ (extended by $\otimes\,\operatorname{id}_{\rm ref}$ to any finite-dimensional passive reference space $\mathcal H_{\rm ref}$) admits an **exact, mark-independent, diamond-confluent joint conservation law** $\mathcal C(P,\rho_{Q,\rm ref})=V_{\rm geom}(P)+\operatorname{Tr}[(H_{|P|}\otimes I_{\rm ref})\rho_{Q,\rm ref}]$ across all four births, all $25$ unmarked posets of sizes $0\le|P|\le 4$, all vertex markings, and every initial state $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$. First, we derive the exact master linear compensation system for any retention-$\lambda_n$ co-rotating quantum instrument, proving that single-parent conditional-mean conservation holds across $\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$ if and only if either $\lambda_n=1$ (unitary step) or $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ (rank-2 POVM effects), whereas state-independent *branchwise* conservation on individual outcomes is algebraically obstructed on $\mathcal D(\mathbb C^2)$ unless $r_P(S)=0$ and $\lambda_n=1$. Second, we prove a multi-birth reachability obstruction showing that the sparse causal-focusing potential $H_{\rm foc}$ of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md) admits exact single-step compensation at $a\prec b$ ($|P|=2\to 3$) yet fails two-step global compensation ($2\to 3\to 4$) at constant $\lambda_n=\frac{1}{2}$ because `2-chain` reaches `edge+iso` with probability $\frac{1}{5}>0$ where $r_{\text{edge+iso}}\equiv 0$. Third, inside the 13-dimensional mark-independent harmonic subspace through four births, we construct a globally active harmonic potential $H_{\rm full}:\mathcal U_4\to[0,1]$ paired with retention schedule $(\lambda_0,\lambda_1,\lambda_2,\lambda_3)=(1,\frac{1}{2},\frac{1}{2},\frac{1}{2})$ and coupling $\theta=\frac{1}{16}$ satisfying complete positivity (unitary at $n=0$, strictly completely positive five-Kraus at $n=1,2,3$), locality, equivariance, entangled diamond commutation from empty start $|P|=0$, and $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ on every nonempty parent. Fourth, we construct in exact rational arithmetic a **purely geometric** unmarked potential $V_{\rm geom}:\bigsqcup_{n=0}^4\mathcal U_n\to\mathbb Q\,\varepsilon$ ($V_{\rm geom}(\varnothing)=0$) whose root-mark dependencies cancel identically across all marked parents and whose endpoint invariance guarantees automatic confluence across every incomparable-birth diamond. Consequently, damped qubit coherence converts conservatively into committed causal-order potential—transferring $\mathbb E_{\rho_0}[V_{\rm geom}(P_4)]=\frac{7\varepsilon}{16}\operatorname{Tr}[Y\rho_0]$ from empty start and $\mathbb E_{\rho_2,r_a}[V_{\rm geom}(P_4)-V_{\rm geom}(a\prec b)]=\frac{3\varepsilon}{8}\operatorname{Tr}[X\rho_2]$ above $a\prec b$ independently of $r_a\in\{0,1\}$—while precursor-local phase back-action simultaneously generates a nonzero root-mark contrast $\Delta_{r_a}\mathbb E[\operatorname{Tr}(Y\rho_4)]\ne 0$ without disturbing conserved energy, with strictly positive $L^1$ lower bounds through a shared faulty erasure-and-confusion detector. All Status-M ontological commitments (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined, and no derivation of Born's rule, physical energy units, clocks, continuum geometry, or General Relativity is claimed.

---

## Context and architecture

Under the [foundational research scope](../coordination/FOUNDATIONAL_RESEARCH_SCOPE.md), the [native geometry, gravity and measurement plan](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md), and the [native mass/gravity mapping](../coordination/NATIVE_MASS_MAPPING.md), prior native compensation and quantum-order feedback packages left three sharp mathematical boundaries open:

1. **First-birth rank-1 obstruction for classical constant-damping dynamics:** The [first-birth additive-balance obstruction](../track_b/native_additive_balance_obstruction.md) proved that under the [active classical residual law](../track_b/native_active_residual_v1.md) (`NM004`), empty start $|P|=0\to 1$ has a single downward ideal $S=\varnothing$ with zero drift $r_\varnothing(\varnothing)=0$ (rank-1 state-independent branch effects) while the classical transition matrix $K\ne I_2$ damps every nonconstant linear functional $\ell\rho$, making $C(E,\rho)=V(E)+\ell\rho$ impossible across admitted initial states.
2. **Single-parent local classification vs. global multi-birth and diamond-merged potentials:** The [local record-compensation theorem](../track_b/local_record_compensation.md) proved that at a single parent, a finite two-state classical instrument compensates a nonconstant linear functional $\ell\rho$ in conditional mean if and only if its effect matrix has rank $2$ or its total map satisfies $K=I_2$. By contrast, [homogeneous two-state compensation](../track_b/homogeneous_native_compensation.md) and [finite-dimensional homogeneous compensation](../track_b/finite_homogeneous_compensation.md) proved that parent-independent commuting classical branch matrices force stationary effects and therefore cannot compensate any nonzero drift $h=\ell(I-K)\ne 0$—while explicitly leaving open whether context-dependent instruments admit a **single global record potential across multiple births, shared child posets, and diamond-merged histories**, and whether conditional-mean balance can ever hold branchwise along individual outcomes.
3. **Exponentially rescaled Heisenberg martingale vs. bounded-spectrum joint conservation:** In [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md), a non-abelian co-rotating five-Kraus instrument on $\mathcal H_Q=\mathbb C^2$ achieved simultaneous `Quantum -> Order` and `Order/Mark -> Quantum` coupling across four births while preserving the exponentially rescaled Heisenberg operator martingale $\mathcal Q_n=2^n\Sigma_n$ ($\|\mathcal Q_n\|_{\rm op}=2^n$). Because each step damps the unscaled Pauli expectation by $\frac{1}{2}$ ($\sum_{S,b}(\mathcal B^{P,r}_{S,b})^\dagger(\Sigma_{n+1})=\frac{1}{2}\Sigma_n$), an **unscaled, bounded-spectrum two-level stage Hamiltonian**
   $$
   H_n:=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n,\qquad \operatorname{Spec}(H_n)=\left\{E_0-\frac{\varepsilon}{2},\,E_0+\frac{\varepsilon}{2}\right\}\qquad (E_0\in\mathbb R,\ \varepsilon>0)
   $$
   loses quantum expectation $\frac{\varepsilon}{2}(1-\lambda_n)\operatorname{Tr}[\Sigma_n\rho]$ whenever the coherent retention factor satisfies $\lambda_n<1$. Whether that lost quantum expectation can be absorbed conservatively into a state-independent, path-independent potential $V(P,r)$—or even a purely geometric unmarked poset functional $V_{\rm geom}(P)$—across all four births and all incomparable-birth diamonds is resolved completely below.

---

## 1. Master quantum compensation equations, single-parent rank criterion, and branchwise nonlinearity obstruction

### 1.1 Retention-parametrized co-rotating five-Kraus instrument and bounded stage Hamiltonian

Retain verbatim the four-birth domain of binary-marked finite strict partial orders $(P,\prec,r)$ ($|P|\in\{0,1,2,3\}$, $r:P\to\{0,1\}$), downward-closed precursor ideals $S\subseteq P$ (forming the set $\mathcal I(P)$ of eligible ideals), append-only maximal births $P+S$, fair newborn bits $b\in\{0,1\}$, and strictly positive structural seed kernel $q(P,r,S)>0$ ($\sum_{S\in\mathcal I(P)}q(P,r,S)=1$) from [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), as summarized in Section 1.1 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#11-unchanged-structural-kernel-through-four-births).

On the fixed two-dimensional Hilbert space $\mathcal H_Q=\mathbb C^2$ with standard basis $\{|0\rangle,|1\rangle\}$ and Pauli operators $(X,Y,Z)$, retain from Section 2.1 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#21-co-rotating-clifford-unitary-and-stage-pauli-axes) the Clifford axis-cycling unitary
$$
U_*:=e^{-i\frac{\pi}{4}Z}e^{-i\frac{\pi}{4}X}=\frac{1}{2}\begin{pmatrix}1-i & -1-i\\ 1-i & 1+i\end{pmatrix},
\qquad
U_*XU_*^\dagger=Y,\quad U_*YU_*^\dagger=Z,\quad U_*ZU_*^\dagger=X,
\tag{1}
$$
with $U_*^2=-U_*^\dagger$, $U_*^3=-I_Q$, and co-rotating stage Pauli axes $\Sigma_0:=Y$ and $\Sigma_n:=U_*^n\Sigma_0(U_*^\dagger)^n$:
$$
(\Sigma_0,\Sigma_1,\Sigma_2,\Sigma_3,\Sigma_4)=(Y,\,Z,\,X,\,Y,\,Z).
\tag{2}
$$
For any fixed reference energy $E_0\in\mathbb R$ and level splitting $\varepsilon>0$, define the bounded co-rotating stage Hamiltonian
$$
H_n:=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n\qquad (n\ge 0).
\tag{3}
$$
Because $\Sigma_n$ is Hermitian and unitary with $\Sigma_n^2=I_Q$ and $\operatorname{Tr}(\Sigma_n)=0$, every $H_n$ has stage-independent spectrum $\{E_0-\frac{\varepsilon}{2},E_0+\frac{\varepsilon}{2}\}$ and constant gap $\varepsilon$ across all births.

Let $\{\varphi_{K,b}\}\subseteq(-\pi,\pi]$ be any real phase family indexed solely by the isomorphism class $K=K(S,r|_S)$ of the induced marked strict precursor $(S,\prec|_S,r|_S)$ and the newborn bit $b\in\{0,1\}$, and set $U_{n,K,b}:=U_*\exp(-i\frac{\varphi_{K,b}}{2}\Sigma_n)$. Fix stage retention parameters $\lambda_n\in(0,1]$ ($n\in\{0,1,2,3\}$). For any real drift parameter $r\in\mathbb R$ satisfying $|r|\le 1-\lambda_n$ and any unitary $U$ on $\mathcal H_Q$, define the retention-$\lambda_n$ core superoperator on $M_2(\mathbb C)$ by
$$
\mathcal M_{\lambda_n}(r,\Sigma_n,U)(A):=\lambda_n\,UAU^\dagger+\frac{1}{2}\operatorname{Tr}\!\Bigl[\bigl((1-\lambda_n)I_Q+r\Sigma_n\bigr)A\Bigr]I_Q,
\tag{4}
$$
and for any current-prefix drift rule $r_P:\mathcal I(P)\to[-(1-\lambda_{|P|}),\,1-\lambda_{|P|}]$ satisfying $\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)=0$, define the branch superoperator
$$
\mathcal B^{P,r}_{S,b}(A):=\frac{1}{2}q(P,r,S)\,\mathcal M_{\lambda_{|P|}}\!\bigl(r_P(S),\,\Sigma_{|P|},\,U_{|P|,K(S,r|_S),b}\bigr)(A)\qquad (|P|\le 3).
\tag{5}
$$
At $\lambda_n=\frac{1}{2}$, $\frac{1}{2}((1-\frac{1}{2})I_Q+r\Sigma_n)=\frac{1}{4}(I_Q+2r\Sigma_n)$, so (4)–(5) recover equations (11)–(12) of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#22-precursor-local-phases-and-branch-superoperator-definition) verbatim; at $\lambda_n=1$, $|r|\le 1-1=0$ forces $r=0$ and reduces $\mathcal M_1(0,\Sigma_n,U)(A)=UAU^\dagger$ to pure unitary conjugation.

**Lemma 1 (Kraus decomposition, exact $4\times 4$ Choi spectrum, and Heisenberg action of $\mathcal M_\lambda$).** *Fix stage $n\ge 0$, $\lambda\in(0,1]$, $|r|\le 1-\lambda$, unitary $U=U_{n,K,b}$, and orthonormal $\Sigma_n$-eigenbasis $\{|\psi_{n,+}\rangle,|\psi_{n,-}\rangle\}$ ($\Sigma_n|\psi_{n,\pm}\rangle=\pm|\psi_{n,\pm}\rangle$).*
1. *(Kraus decomposition and Hilbert–Schmidt adjoint.)* *The operators*
   $$
   L_0:=\sqrt{\lambda}\,U,\qquad L_{\alpha,\beta}:=\sqrt{\frac{1-\lambda+\alpha r}{2}}\,|\beta\rangle\langle\psi_{n,\alpha}|\qquad (\alpha\in\{+,-\},\ \beta\in\{0,1\})
   \tag{6}
   $$
   *satisfy $L_0AL_0^\dagger+\sum_{\alpha=\pm}\sum_{\beta=0}^1 L_{\alpha,\beta}AL_{\alpha,\beta}^\dagger=\mathcal M_\lambda(r,\Sigma_n,U)(A)$, and the Hilbert–Schmidt adjoint $\mathcal M_\lambda(r,\Sigma_n,U)^\dagger$ is*
   $$
   \mathcal M_\lambda(r,\Sigma_n,U)^\dagger(B)=\lambda\,U^\dagger BU+\frac{\operatorname{Tr}(B)}{2}\bigl((1-\lambda)I_Q+r\Sigma_n\bigr).
   \tag{7}
   $$
   *In particular, $\mathcal M_\lambda(r,\Sigma_n,U_{n,K,b})^\dagger(I_Q)=I_Q+r\Sigma_n$, $\mathcal M_\lambda(r,\Sigma_n,U_{n,K,b})^\dagger(\Sigma_{n+1})=\lambda\Sigma_n$, and*
   $$
   \mathcal M_\lambda(r,\Sigma_n,U_{n,K,b})^\dagger(H_{n+1})=E_0(I_Q+r\Sigma_n)+\lambda\frac{\varepsilon}{2}\Sigma_n.
   \tag{8}
   $$
2. *(Exact $4\times 4$ Choi eigenvalues and complete positivity.)* *With $|\Omega\rangle:=|0\rangle\otimes|0\rangle+|1\rangle\otimes|1\rangle$, the Choi matrix $J(\mathcal M_\lambda):=(\mathcal M_\lambda(r,\Sigma_n,U)\otimes\operatorname{id}_{\mathbb C^2})(|\Omega\rangle\langle\Omega|)$ has exact spectrum*
   $$
   \operatorname{Spec}\bigl(J(\mathcal M_\lambda)\bigr)=\left\{\frac{1-\lambda-r}{2},\ \frac{1-\lambda+r}{2},\ \frac{1+\lambda-\sqrt{4\lambda^2+r^2}}{2},\ \frac{1+\lambda+\sqrt{4\lambda^2+r^2}}{2}\right\}.
   \tag{9}
   $$
   *Hence $\mathcal M_\lambda(r,\Sigma_n,U)$ is completely positive whenever $|r|\le 1-\lambda$, strictly completely positive ($\lambda_{\min}(J(\mathcal M_\lambda))=\frac{1-\lambda-|r|}{2}>0$) whenever $\lambda\in(0,1)$ and $|r|<1-\lambda$, and rank-1 unitary ($J(\mathcal M_1)=(U\otimes I_2)|\Omega\rangle\langle\Omega|(U^\dagger\otimes I_2)\succeq 0$ with spectrum $\{0,0,0,2\}$) when $\lambda=1$ and $r=0$.*

**Proof.**
1. Because $|r|\le 1-\lambda$, $1-\lambda+\alpha r\ge 0$ for both $\alpha\in\{+,-\}$. Using $\sum_{\beta=0}^1|\beta\rangle\langle\beta|=I_Q$ and $\sum_{\alpha=\pm}(1-\lambda+\alpha r)|\psi_{n,\alpha}\rangle\langle\psi_{n,\alpha}|=(1-\lambda)I_Q+r\Sigma_n$, we obtain for every $A\in M_2(\mathbb C)$:
   $$
   L_0AL_0^\dagger+\sum_{\alpha=\pm}\sum_{\beta=0}^1L_{\alpha,\beta}AL_{\alpha,\beta}^\dagger
   =\lambda UAU^\dagger+\sum_{\alpha=\pm}\frac{1-\lambda+\alpha r}{2}\langle\psi_{n,\alpha}|A|\psi_{n,\alpha}\rangle I_Q
   =\lambda UAU^\dagger+\frac{1}{2}\operatorname{Tr}\!\Bigl[\bigl((1-\lambda)I_Q+r\Sigma_n\bigr)A\Bigr]I_Q.
   $$
   For any $A,B\in M_2(\mathbb C)$, $\operatorname{Tr}[B\,\mathcal M_\lambda(r,\Sigma_n,U)(A)]=\lambda\operatorname{Tr}[U^\dagger BUA]+\frac{\operatorname{Tr}(B)}{2}\operatorname{Tr}[((1-\lambda)I_Q+r\Sigma_n)A]$, establishing (7). Evaluating (7) on $B=I_Q$ ($\operatorname{Tr}(I_Q)=2$, $U^\dagger U=I_Q$) yields $\lambda I_Q+(1-\lambda)I_Q+r\Sigma_n=I_Q+r\Sigma_n$. Since $\Sigma_{n+1}=U_*\Sigma_nU_*^\dagger$ has $\operatorname{Tr}(\Sigma_{n+1})=0$ and $e^{+i\frac{\varphi_{K,b}}{2}\Sigma_n}$ commutes with $\Sigma_n$, $U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=e^{+i\frac{\varphi_{K,b}}{2}\Sigma_n}(U_*^\dagger\Sigma_{n+1}U_*)e^{-i\frac{\varphi_{K,b}}{2}\Sigma_n}=\Sigma_n$, so (7) gives $\mathcal M_\lambda^\dagger(\Sigma_{n+1})=\lambda\Sigma_n$, and linearity on $H_{n+1}=E_0I_Q+\frac{\varepsilon}{2}\Sigma_{n+1}$ gives (8).
2. Expanding $|\Omega\rangle\langle\Omega|=\sum_{j,k=0}^1|j\rangle\langle k|\otimes|j\rangle\langle k|$ yields
   $$
   J(\mathcal M_\lambda)=\lambda(U\otimes I_2)|\Omega\rangle\langle\Omega|(U^\dagger\otimes I_2)+\frac{1}{2}I_2\otimes\bigl((1-\lambda)I_2+r\Sigma_n^T\bigr).
   $$
   Set $|\chi_\alpha\rangle:=\overline{|\psi_{n,\alpha}\rangle}$ ($\Sigma_n^T|\chi_\pm\rangle=\pm|\chi_\pm\rangle$) and $|u_\alpha\rangle:=U|\psi_{n,\alpha}\rangle$. Since $|\Omega\rangle=|\psi_{n,+}\rangle\otimes|\chi_+\rangle+|\psi_{n,-}\rangle\otimes|\chi_-\rangle$, $(U\otimes I_2)|\Omega\rangle=|u_+\rangle\otimes|\chi_+\rangle+|u_-\rangle\otimes|\chi_-\rangle$. In the orthonormal basis $|f_1\rangle:=|u_+\rangle\otimes|\chi_+\rangle$, $|f_2\rangle:=|u_-\rangle\otimes|\chi_-\rangle$, $|f_3\rangle:=|u_+\rangle\otimes|\chi_-\rangle$, $|f_4\rangle:=|u_-\rangle\otimes|\chi_+\rangle$ of $\mathbb C^2\otimes\mathbb C^2$, $J(\mathcal M_\lambda)$ is block-diagonal with $1\times 1$ entries $\frac{1-\lambda-r}{2}$ on $|f_3\rangle$ and $\frac{1-\lambda+r}{2}$ on $|f_4\rangle$, and $2\times 2$ block on $\operatorname{span}\{|f_1\rangle,|f_2\rangle\}$ equal to
   $$
   \begin{pmatrix}\lambda+\frac{1-\lambda+r}{2} & \lambda\\[4pt] \lambda & \lambda+\frac{1-\lambda-r}{2}\end{pmatrix}
   =\begin{pmatrix}\frac{1+\lambda+r}{2} & \lambda\\[4pt] \lambda & \frac{1+\lambda-r}{2}\end{pmatrix}.
   $$
   This $2\times 2$ block has trace $1+\lambda$ and determinant $\frac{(1+\lambda)^2-r^2}{4}-\lambda^2$, so its characteristic polynomial $\mu^2-(1+\lambda)\mu+\frac{(1+\lambda)^2-r^2}{4}-\lambda^2=0$ has discriminant $(1+\lambda)^2-(1+\lambda)^2+r^2+4\lambda^2=4\lambda^2+r^2$ and roots $\frac{1+\lambda\pm\sqrt{4\lambda^2+r^2}}{2}$, proving (9). Because $\sqrt{4\lambda^2+r^2}\le 2\lambda+|r|$, $\frac{1+\lambda-\sqrt{4\lambda^2+r^2}}{2}\ge\frac{1-\lambda-|r|}{2}$, confirming nonnegativity for $|r|\le 1-\lambda$, strict positivity when $\lambda\in(0,1)$ and $|r|<1-\lambda$, and spectrum $\{0,0,0,2\}$ at $(\lambda,r)=(1,0)$. $\blacksquare$

---

### 1.2 Master linear system and exact single-parent quantum record-compensation criterion

Fix any marked parent $(P,r)$ of cardinality $|P|=n\in\{0,1,2,3\}$ and parent record value $V(P,r)\in\mathbb R$. Let $E^{P,r}_{S,b}:=(\mathcal B^{P,r}_{S,b})^\dagger(I_Q)=\frac{1}{2}q(P,r,S)(I_Q+r_P(S)\Sigma_n)$ denote the POVM branch effects in the real four-dimensional space $\mathcal H_{\rm Herm}(\mathbb C^2)$ of $2\times 2$ Hermitian matrices ($\sum_{S\in\mathcal I(P)}\sum_{b\in\{0,1\}}E^{P,r}_{S,b}=I_Q$). For any candidate assignment of real child record potentials $\{V(P+S,r+b)\}_{S\in\mathcal I(P),\,b\in\{0,1\}}$, decompose each ideal's pair of bit values into its bit-symmetric mean and bit-antisymmetric half-difference:
$$
\overline V(P+S,r):=\frac{V(P+S,r+0)+V(P+S,r+1)}{2},
\qquad
w(P+S,r):=\frac{V(P+S,r+0)-V(P+S,r+1)}{2},
\tag{10}
$$
so that $V(P+S,r+0)=\overline V(P+S,r)+w(P+S,r)$ and $V(P+S,r+1)=\overline V(P+S,r)-w(P+S,r)$ bijectively. Define the $q$-weighted drift variance
$$
\operatorname{Var}_{q(P,r,\cdot)}(r_P):=\sum_{S\in\mathcal I(P)}q(P,r,S)\,r_P(S)^2\ge 0
\tag{11}
$$
(using $\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)=0$).

**Theorem 1 (Master linear system and exact single-parent quantum record-compensation criterion).** *Fix a marked parent $(P,r)$ ($|P|=n\le 3$), retention factor $\lambda_n\in(0,1]$, drift vector $r_P:\mathcal I(P)\to[-(1-\lambda_n),1-\lambda_n]$ satisfying $\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)=0$, bounded stage Hamiltonians $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ and $H_{n+1}=E_0I_Q+\frac{\varepsilon}{2}\Sigma_{n+1}$ ($\varepsilon>0$), and parent value $V(P,r)\in\mathbb R$.*

1. *(Equivalence to the master linear pair.)* *A child-record assignment $\{V(P+S,r+b)\}_{S\in\mathcal I(P),\,b\in\{0,1\}}\subseteq\mathbb R$ satisfies exact conditional-mean conservation*
   $$
   \sum_{S\in\mathcal I(P)}\sum_{b\in\{0,1\}}\Bigl(V(P+S,r+b)\operatorname{Tr}\!\bigl[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr]+\operatorname{Tr}\!\bigl[(H_{n+1}\otimes I_{\rm ref})(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr]\Bigr)
   =V(P,r)+\operatorname{Tr}\!\bigl[(H_n\otimes I_{\rm ref})\rho_{Q,\rm ref}\bigr]
   \tag{12}
   $$
   *for all finite-dimensional reference spaces $\mathcal H_{\rm ref}$ and all joint density operators $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$ (and already for $\dim\mathcal H_{\rm ref}=1$ on the two pure eigenstates $\frac{1}{2}(I_Q\pm\Sigma_n)\in\mathcal D(\mathbb C^2)$) **if and only if** the bit-averaged child values $\overline V(P+S,r)$ satisfy the two linear equations*
   $$
   \text{\rm (I)}\quad \sum_{S\in\mathcal I(P)}q(P,r,S)\,\overline V(P+S,r)=V(P,r),
   \qquad
   \text{\rm (II)}\quad \sum_{S\in\mathcal I(P)}q(P,r,S)\,r_P(S)\,\overline V(P+S,r)=\frac{\varepsilon}{2}(1-\lambda_n),
   \tag{13}
   $$
   *with the bit-antisymmetric coordinates $\{w(P+S,r)\}_{S\in\mathcal I(P)}\in\mathbb R^{|\mathcal I(P)|}$ completely unconstrained.*
2. *(Exact feasibility and POVM effect-rank criterion.)* *Because $q(P,r,S)>0$ on all $S\in\mathcal I(P)$, $\dim\operatorname{span}_{\mathbb R}\{E^{P,r}_{S,b}:S\in\mathcal I(P),\,b\in\{0,1\}\}\in\{1,2\}$ inside $\mathcal H_{\rm Herm}(\mathbb C^2)$, with dimension $2$ if and only if $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ (equivalently $r_P\not\equiv 0$). System (13) admits a solution $\{V(P+S,r+b)\}$ **if and only if** either:*
   - *$\lambda_n=1$ (unitary non-damping step, which forces $r_P\equiv 0$), or*
   - *$\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ (equivalently $\dim\operatorname{span}_{\mathbb R}\{E^{P,r}_{S,b}\}=2$).*
3. *(Exact affine solution dimensions and minimum-variance canonical solution.)*
   - *When $\lambda_n=1$ (so $r_P\equiv 0$), equation (II) holds identically ($0=0$) and the solution space of $\{V(P+S,r+b)\}$ in $\mathbb R^{2|\mathcal I(P)|}$ is an affine subspace of exact dimension $2|\mathcal I(P)|-1$ ($|\mathcal I(P)|$ free antisymmetric parameters $w(P+S,r)$ plus $|\mathcal I(P)|-1$ zero-$q$-mean parameters for $\overline V$), with canonical constant solution $\overline V(P+S,r)=V(P,r)$.*
   - *When $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$, the linear map $L_P:\mathbb R^{|\mathcal I(P)|}\to\mathbb R^2$ defined by $L_P(\overline V):=\bigl(\sum_S q(P,r,S)\overline V_S,\,\sum_S q(P,r,S)r_P(S)\overline V_S\bigr)$ is surjective of rank $2$, so the solution space of $\{V(P+S,r+b)\}$ in $\mathbb R^{2|\mathcal I(P)|}$ is an affine subspace of exact dimension $2|\mathcal I(P)|-2$ ($|\mathcal I(P)|$ free antisymmetric parameters $w(P+S,r)$ plus $|\mathcal I(P)|-2$ parameters in $\ker L_P$). Across all solutions of (13), the unique bit-averaged vector minimizing the $q$-weighted child variance $\operatorname{Var}_{q(P,r,\cdot)}(\overline V):=\sum_{S\in\mathcal I(P)}q(P,r,S)(\overline V(P+S,r)-V(P,r))^2$ is*
     $$
     \overline V_{\min}(P+S,r)=V(P,r)+\frac{\varepsilon(1-\lambda_n)}{2\operatorname{Var}_{q(P,r,\cdot)}(r_P)}\,r_P(S)\qquad (S\in\mathcal I(P)),
     \tag{14}
     $$
     *attaining minimum variance $\operatorname{Var}_{q(P,r,\cdot)}(\overline V_{\min})=\dfrac{\varepsilon^2(1-\lambda_n)^2}{4\operatorname{Var}_{q(P,r,\cdot)}(r_P)}$.*

**Proof.**
1. For any $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, let $\rho_Q:=\operatorname{Tr}_{\rm ref}(\rho_{Q,\rm ref})\in\mathcal D(\mathbb C^2)$ denote its reduced qubit density operator ($\operatorname{Tr}(\rho_Q)=1$). Because $(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})^\dagger(A\otimes I_{\rm ref})=(\mathcal B^{P,r}_{S,b})^\dagger(A)\otimes I_{\rm ref}$ for every $A\in M_2(\mathbb C)$, the left-hand side of (12) equals $\operatorname{Tr}_Q[O_{\rm LHS}\,\rho_Q]$ and the right-hand side equals $\operatorname{Tr}_Q[O_{\rm RHS}\,\rho_Q]$, where in $\mathcal H_{\rm Herm}(\mathbb C^2)$:
   $$
   O_{\rm LHS}:=\sum_{S\in\mathcal I(P)}\sum_{b\in\{0,1\}}\Bigl(V(P+S,r+b)\,E^{P,r}_{S,b}+\bigl(\mathcal B^{P,r}_{S,b}\bigr)^\dagger(H_{n+1})\Bigr),
   \qquad
   O_{\rm RHS}:=V(P,r)I_Q+H_n=(V(P,r)+E_0)I_Q+\frac{\varepsilon}{2}\Sigma_n.
   $$
   Observe that $E^{P,r}_{S,b}=\frac{1}{2}q(P,r,S)(I_Q+r_P(S)\Sigma_n)$ is independent of $b\in\{0,1\}$. Hence for each ideal $S\in\mathcal I(P)$, summing over $b\in\{0,1\}$ cancels $w(P+S,r)$ identically:
   $$
   \sum_{b\in\{0,1\}}V(P+S,r+b)\,E^{P,r}_{S,b}=\bigl(V(P+S,r+0)+V(P+S,r+1)\bigr)\frac{1}{2}q(P,r,S)(I_Q+r_P(S)\Sigma_n)=q(P,r,S)\overline V(P+S,r)(I_Q+r_P(S)\Sigma_n).
   $$
   Likewise, by (5) and Lemma 1's identity (8) (which is also independent of $b$ and $\varphi_{K,b}$),
   $$
   \sum_{b\in\{0,1\}}\bigl(\mathcal B^{P,r}_{S,b}\bigr)^\dagger(H_{n+1})=q(P,r,S)\left(E_0(I_Q+r_P(S)\Sigma_n)+\lambda_n\frac{\varepsilon}{2}\Sigma_n\right).
   $$
   Summing over $S\in\mathcal I(P)$ and applying $\sum_{S\in\mathcal I(P)}q(P,r,S)=1$ and $\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)=0$ gives
   $$
   O_{\rm LHS}=\left(\sum_{S\in\mathcal I(P)}q(P,r,S)\overline V(P+S,r)+E_0\right)I_Q+\left(\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)\overline V(P+S,r)+\lambda_n\frac{\varepsilon}{2}\right)\Sigma_n.
   $$
   Subtracting $O_{\rm RHS}$ cancels $E_0I_Q$ and yields the Hermitian defect operator
   $$
   \Delta O:=O_{\rm LHS}-O_{\rm RHS}=\alpha\,I_Q+\beta\,\Sigma_n,
   $$
   where $\alpha:=\sum_{S\in\mathcal I(P)}q(P,r,S)\overline V(P+S,r)-V(P,r)$ and $\beta:=\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)\overline V(P+S,r)-\frac{\varepsilon}{2}(1-\lambda_n)$. If (13) holds, then $\alpha=\beta=0$, so $\Delta O=0$ and $\operatorname{Tr}_Q[\Delta O\,\rho_Q]=0$ for every $\mathcal H_{\rm ref}$ and every $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$. Conversely, suppose (12) holds on the two eigenstates $\rho_\pm:=\frac{1}{2}(I_Q\pm\Sigma_n)\in\mathcal D(\mathbb C^2)$ (with $\dim\mathcal H_{\rm ref}=1$). Using $\operatorname{Tr}(I_Q)=2$, $\operatorname{Tr}(\Sigma_n)=0$, and $\operatorname{Tr}(\Sigma_n^2)=2$, we obtain $0=\operatorname{Tr}[\Delta O\,\rho_\pm]=\alpha\pm\beta$, forcing $\alpha=\beta=0$ and hence (13), with $w(P+S,r)$ completely free.
2. Since $q(P,r,S)>0$ for all $S\in\mathcal I(P)$ and $E^{P,r}_{S,b}=\frac{1}{2}q(P,r,S)(I_Q+r_P(S)\Sigma_n)$, $\operatorname{span}_{\mathbb R}\{E^{P,r}_{S,b}\}=\operatorname{span}_{\mathbb R}\{I_Q+r_P(S)\Sigma_n:S\in\mathcal I(P)\}\subseteq\operatorname{span}_{\mathbb R}\{I_Q,\Sigma_n\}$. Because $I_Q$ and $\Sigma_n$ are linearly independent, this span has dimension $1$ if $r_P(S)$ is constant across $S\in\mathcal I(P)$—which by $\sum_S q(P,r,S)r_P(S)=0$ and $q>0$ holds if and only if $r_P\equiv 0$, i.e., $\operatorname{Var}_{q(P,r,\cdot)}(r_P)=0$—and dimension $2$ if and only if $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$.
   - If $r_P\equiv 0$, equation (II) in (13) reads $0=\frac{\varepsilon}{2}(1-\lambda_n)$. Since $\varepsilon>0$, this is solvable if and only if $\lambda_n=1$; when $\lambda_n=1$, equation (I) has a solution because $\sum_S q(P,r,S)=1\ne 0$.
   - If $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$, let $\mathbf 1\in\mathbb R^{|\mathcal I(P)|}$ be the all-ones vector and $r_P\in\mathbb R^{|\mathcal I(P)|}$ the drift vector, equipped with the strictly positive-definite inner product $\langle u,v\rangle_q:=\sum_{S\in\mathcal I(P)}q(P,r,S)u_Sv_S$. Here $\langle\mathbf 1,\mathbf 1\rangle_q=1$, $\langle\mathbf 1,r_P\rangle_q=0$, and $\langle r_P,r_P\rangle_q=\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$, so $\{\mathbf 1,r_P\}$ is $\langle\cdot,\cdot\rangle_q$-orthogonal of rank $2$, and $L_P(\overline V)=(\langle\mathbf 1,\overline V\rangle_q,\langle r_P,\overline V\rangle_q)$ maps $\mathbb R^{|\mathcal I(P)|}$ onto $\mathbb R^2$. In particular, (14) satisfies $\langle\mathbf 1,\overline V_{\min}\rangle_q=V(P,r)\langle\mathbf 1,\mathbf 1\rangle_q+0=V(P,r)$ and $\langle r_P,\overline V_{\min}\rangle_q=0+\frac{\varepsilon(1-\lambda_n)}{2\operatorname{Var}_q(r_P)}\langle r_P,r_P\rangle_q=\frac{\varepsilon}{2}(1-\lambda_n)$, proving existence.
3. By the bijection (10), $\mathbb R^{2|\mathcal I(P)|}\cong\mathbb R^{|\mathcal I(P)|}_{\overline V}\oplus\mathbb R^{|\mathcal I(P)|}_w$. When $\lambda_n=1$ ($r_P\equiv 0$), $\overline V$ lies in the hyperplane $\{\overline V:\langle\mathbf 1,\overline V\rangle_q=V(P,r)\}$ of dimension $|\mathcal I(P)|-1$, giving total affine dimension $(|\mathcal I(P)|-1)+|\mathcal I(P)|=2|\mathcal I(P)|-1$. When $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$, $\operatorname{rank}(L_P)=2$ gives $\dim\ker L_P=|\mathcal I(P)|-2$ and total affine dimension $(|\mathcal I(P)|-2)+|\mathcal I(P)|=2|\mathcal I(P)|-2$. Finally, any solution $\overline V$ of (13) writes uniquely as $\overline V=\overline V_{\min}+z$ with $z\in\ker L_P$, i.e., $\langle\mathbf 1,z\rangle_q=\langle r_P,z\rangle_q=0$. Since $\overline V_{\min}-V(P,r)\mathbf 1=c\,r_P$ ($c:=\frac{\varepsilon(1-\lambda_n)}{2\operatorname{Var}_q(r_P)}$) is $\langle\cdot,\cdot\rangle_q$-orthogonal to $z$, the Pythagorean identity in $(\mathbb R^{|\mathcal I(P)|},\langle\cdot,\cdot\rangle_q)$ gives
   $$
   \operatorname{Var}_{q(P,r,\cdot)}(\overline V)=\|\overline V_{\min}-V(P,r)\mathbf 1+z\|_q^2=c^2\|r_P\|_q^2+\|z\|_q^2=\frac{\varepsilon^2(1-\lambda_n)^2}{4\operatorname{Var}_{q(P,r,\cdot)}(r_P)}+\|z\|_q^2,
   $$
   which is uniquely minimized at $z=0$ ($\|z\|_q^2=0\iff z=0$ because $q>0$). $\blacksquare$

*Remark (Quantum unification of the Track-B classical criteria).* Theorem 1 generalizes the [local record-compensation criterion](../track_b/local_record_compensation.md) ($\operatorname{rank}(E)=2$ or $K=I_2$) and its affine solution dimensions ($2|\mathcal I(P)|-2$ vs. $2|\mathcal I(P)|-1$, matching [homogeneous native compensation](../track_b/homogeneous_native_compensation.md) and [finite homogeneous compensation](../track_b/finite_homogeneous_compensation.md)) from commuting classical simplex maps to non-abelian co-rotating five-Kraus quantum instruments on $\mathcal H_Q\otimes\mathcal H_{\rm ref}$, where the active Pauli measurement axis $\Sigma_{|P|}$ rotates through $(Y,Z,X,Y,Z)$ across stages. Crucially, notice that the reference offset $E_0$ cancels identically out of (13), and arbitrary precursor-local phases $\varphi_{K,b}$ do not enter (13) at all because $U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=\Sigma_n$ intertwines the co-rotating Hamiltonian axis exactly.

---

### 1.3 State-independent branchwise conservation and the rational nonlinearity obstruction

Conditional-mean conservation (12) weights each child record by its unnormalized trace probability $p^{P,r}_{S,b}(\rho)=\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]$, canceling the state-dependent denominator of the normalized post-measurement state
$$
\rho'_{S,b}:=\frac{\mathcal B^{P,r}_{S,b}(\rho)}{\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]}\in\mathcal D(\mathbb C^2)
\qquad\bigl(\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]>0\bigr).
\tag{15}
$$
A natural question left open in [local record compensation](../track_b/local_record_compensation.md) and [finite homogeneous compensation](../track_b/finite_homogeneous_compensation.md) is whether state-independent record potentials can ever conserve $V+\operatorname{Tr}[H_{|P|}\rho]$ **branchwise** on individual outcomes $(S,b)$ across $\mathcal D(\mathbb C^2)$.

**Theorem 2 (Branchwise nonlinearity obstruction on $\mathcal D(\mathbb C^2)$).** *Fix a marked parent $(P,r)$ ($|P|=n\le 3$), retention $\lambda_n\in(0,1]$, a branch $(S,b)\in\mathcal I(P)\times\{0,1\}$ with $|r_P(S)|<1$ (which holds automatically whenever $\lambda_n\in(0,1]$ and $|r_P(S)|\le 1-\lambda_n$), and finite constants $V(P,r),V(P+S,r+b)\in\mathbb R$. Then state-independent branchwise conservation*
$$
V(P+S,r+b)+\operatorname{Tr}[H_{n+1}\rho'_{S,b}]=V(P,r)+\operatorname{Tr}[H_n\rho]
\tag{16}
$$
*holds for every initial density matrix $\rho\in\mathcal D(\mathbb C^2)$ (and already on the three states $\{\frac{1}{2}I_Q,\,\frac{1}{2}(I_Q+\Sigma_n),\,\frac{1}{2}(I_Q-\Sigma_n)\}\subseteq\mathcal D(\mathbb C^2)$) **if and only if***
$$
r_P(S)=0,\qquad \lambda_n=1,\qquad\text{and}\qquad V(P+S,r+b)=V(P,r).
\tag{17}
$$
*In particular, no strictly damping step ($\lambda_n<1$) and no order-steering branch ($r_P(S)\ne 0$) can satisfy state-independent branchwise conservation on $\mathcal D(\mathbb C^2)$.*

**Proof.** For any $\rho\in\mathcal D(\mathbb C^2)$, set $s:=\operatorname{Tr}[\Sigma_n\rho]\in[-1,1]$. Because $q(P,r,S)>0$ and $|r_P(S)|<1$, Lemma 1 gives
$$
\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]=\frac{1}{2}q(P,r,S)\bigl(1+r_P(S)s\bigr)>0
$$
for every $s\in[-1,1]$, so $\rho'_{S,b}$ in (15) is well-defined across the entire state space $\mathcal D(\mathbb C^2)$. By (8),
$$
\operatorname{Tr}[H_{n+1}\mathcal B^{P,r}_{S,b}(\rho)]=\frac{1}{2}q(P,r,S)\left(E_0\bigl(1+r_P(S)s\bigr)+\lambda_n\frac{\varepsilon}{2}s\right).
$$
Dividing by $\frac{1}{2}q(P,r,S)(1+r_P(S)s)>0$ cancels the $\frac{1}{2}q(P,r,S)$ prefactor and the $E_0$ offset:
$$
\operatorname{Tr}[H_{n+1}\rho'_{S,b}]=E_0+\frac{\varepsilon}{2}\,\frac{\lambda_n s}{1+r_P(S)s},
\qquad
\operatorname{Tr}[H_n\rho]=E_0+\frac{\varepsilon}{2}\,s.
\tag{18}
$$
Substituting (18) into (16) and noting that $s=\operatorname{Tr}[\Sigma_n\rho]$ ranges over the entire interval $[-1,1]$ as $\rho=\frac{1}{2}(I_Q+s\Sigma_n)$ ranges over $\mathcal D(\mathbb C^2)$ shows that (16) holds for all $\rho\in\mathcal D(\mathbb C^2)$ if and only if the rational function of $s\in[-1,1]$ satisfies
$$
\frac{\varepsilon}{2}\left(\frac{\lambda_n s}{1+r_P(S)s}-s\right)=V(P,r)-V(P+S,r+b)=:c\qquad\forall s\in[-1,1].
\tag{19}
$$
Evaluating (19) at $s=0$ ($\rho=\frac{1}{2}I_Q\in\mathcal D(\mathbb C^2)$) forces $c=0$, i.e., $V(P+S,r+b)=V(P,r)$. With $c=0$ and $\frac{\varepsilon}{2}>0$, multiplying (19) through by $1+r_P(S)s>0$ yields the quadratic polynomial identity
$$
(\lambda_n-1)s-r_P(S)s^2=0\qquad\forall s\in[-1,1].
\tag{20}
$$
Evaluating (20) at $s=+1$ and $s=-1$ ($\rho=\frac{1}{2}(I_Q\pm\Sigma_n)\in\mathcal D(\mathbb C^2)$) gives $(\lambda_n-1)-r_P(S)=0$ and $-(\lambda_n-1)-r_P(S)=0$. Adding the two equations gives $-2r_P(S)=0\implies r_P(S)=0$; subtracting them gives $2(\lambda_n-1)=0\implies\lambda_n=1$. Conversely, when $r_P(S)=0$, $\lambda_n=1$, and $V(P+S,r+b)=V(P,r)$, (18) gives $\operatorname{Tr}[H_{n+1}\rho'_{S,b}]=E_0+\frac{\varepsilon}{2}s=\operatorname{Tr}[H_n\rho]$ for every $\rho\in\mathcal D(\mathbb C^2)$. $\blacksquare$

Theorem 2 pinpoints why conditional-mean balance (12)—and not branchwise equality (16)—is the exact conservation law of selective quantum-order instruments whenever $\lambda_n<1$: Bayes normalization $\rho\mapsto\rho'_{S,b}$ divides by $1+r_P(S)s$, turning $\operatorname{Tr}[H_{n+1}\rho'_{S,b}]$ into a nonlinear rational function of $s=\operatorname{Tr}[\Sigma_n\rho]$ whenever $r_P(S)\lambda_n\ne 0$, whereas multiplying by the branch probability $\frac{1}{2}q(P,r,S)(1+r_P(S)s)$ restores exact linearity in $\rho$ and couples the state-independent record potential $\overline V(P+S,r)$ directly to $r_P(S)\Sigma_n$ in equation (II) of Theorem 1.

## 2. Multi-birth reachability obstruction for sparse potentials and the globally active four-birth instrument

### 2.1 Single-step success vs. two-step reachability obstruction for the sparse focusing potential $H_{\rm foc}$

In [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#13-canonical-causal-focusing-potential-h_rm-foc-and-current-prefix-coefficient-r_ps), the five-Kraus instrument used constant retention $\lambda_n\equiv\frac{1}{2}$ ($n\in\{0,1,2,3\}$), coupling $\theta=\frac{1}{32}$, and the binary causal-focusing indicator $H_{\rm foc}:\mathcal U_4\to\{0,1\}$ supported on $\{E_{\text{asym-fork}},E_{\text{diamond}},E_{\text{4-chain}}\}$. That law illustrates sharply why single-parent feasibility (Theorem 1) does **not** automatically extend to a multi-birth global conservation law—even when restricted to states actually reached from a prepared causal prefix.

**Theorem 3 (Single-step compensation vs. multi-birth reachability obstruction for $(H_{\rm foc},\lambda_n\equiv\frac{1}{2})$).** *Consider the five-Kraus instrument of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md) ($\lambda_n\equiv\frac{1}{2}$, $\theta=\frac{1}{32}$, $r_P^{\rm foc}(S)=\frac{1}{32}2^{|P|}[H_{\rm foc}(P+S)-H_{\rm foc}(P)]$) paired with the bounded stage Hamiltonian $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ ($\varepsilon>0$).*

1. *(Exact single-step compensation above $a\prec b$ at $|P|=2\to 3$.)* *On the prepared causal prefix $P_2=(a\prec b)$ with any marks $(r_a,r_b)\in\{0,1\}^2$ and parent gauge $V(a\prec b,r)$, single-step conditional-mean conservation (12) holds simultaneously across all $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$ and all $(r_a,r_b)\in\{0,1\}^2$ for the mark-independent size-$3$ geometric assignment*
   $$
   V(\text{edge+iso})=V(a\prec b)-\frac{220}{21}\varepsilon,
   \qquad
   V(\text{fork})=V(\text{3-chain})=V(a\prec b)+\frac{55}{21}\varepsilon.
   \tag{21}
   $$
2. *(Two-step reachability obstruction at $2\to 3\to 4$, including on restricted reachable states.)* *No assignment of marked record potentials $V(P,r)\in\mathbb R$ ($|P|\in\{2,3,4\}$) can satisfy conditional-mean conservation (12) across both steps $2\to 3\to 4$ starting from $(a\prec b,r)$—even if (12) at $|P|=3$ is required solely on post-measurement qubit states $\rho'_3$ actually reached with positive probability from $(a\prec b,r)$ and initial states $\rho_2\in\mathcal D(\mathbb C^2)$.*
3. *(Empty-start $|P|=0\to 1$ obstruction for ideal-only damping vs. unitary and bit-coupled resolutions.)* *At $P_0=\varnothing$, $|\mathcal I(\varnothing)|=1$ ($\mathcal I(\varnothing)=\{\varnothing\}$) forces $r_\varnothing(\varnothing)=0$ for every newborn-bit-independent drift rule; hence any instrument with $\lambda_0<1$ fails (12) at $0\to 1$ across $\rho_0\in\mathcal D(\mathbb C^2)$. Within bit-independent structural steering, conservation at $0\to 1$ holds if and only if $\lambda_0=1$ (unitary first birth); alternatively, admitting newborn-bit-coupled steering $r_{\varnothing,b}=(-1)^b r_0$ ($0<|r_0|\le 1-\lambda_0$) restores rank-$2$ effects $\frac{1}{2}(I_Q+(-1)^b r_0\Sigma_0)$ and unique bit-antisymmetric compensation $V(A_1,b)=V(\varnothing)+(-1)^b\frac{\varepsilon(1-\lambda_0)}{2r_0}$.*

**Proof.**
1. On $P_2=(a\prec b)$, $\lambda_2=\frac{1}{2}$ gives $\frac{\varepsilon}{2}(1-\lambda_2)=\frac{\varepsilon}{4}$, and from Section 1.3 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#13-canonical-causal-focusing-potential-h_rm-foc-and-current-prefix-coefficient-r_ps) the three ideals $S\in\{\varnothing,\{a\},\{a,b\}\}$ send $P_2+S$ to `edge+iso`, `fork`, and `3-chain` with probabilities $(\frac{1}{5},f_{r_a},h_{r_a})$ ($f_{r_a}+h_{r_a}=\frac{4}{5}$) and drifts $(-\frac{21}{220},+\frac{21}{880},+\frac{21}{880})$. Substituting (21) into (13) cancels $r_a\in\{0,1\}$ in both equations:
   $$
   \frac{1}{5}\left(V(a\prec b)-\frac{220}{21}\varepsilon\right)+\frac{4}{5}\left(V(a\prec b)+\frac{55}{21}\varepsilon\right)=V(a\prec b)+\frac{-44+44}{21}\varepsilon=V(a\prec b),
   $$
   $$
   \frac{1}{5}\left(-\frac{21}{220}\right)\left(-\frac{220}{21}\varepsilon\right)+\frac{4}{5}\left(+\frac{21}{880}\right)\left(+\frac{55}{21}\varepsilon\right)=\left(\frac{1}{5}+\frac{4}{80}\right)\varepsilon=\frac{1}{4}\varepsilon,
   $$
   where $V(a\prec b)$ drops out of (II) because $\sum_S q\,r_{C_2}(S)=0$. By Theorem 1, single-step conservation holds across $\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$.
2. Prepare $\rho_{2,\pm}:=|\pm\rangle\langle\pm|=\frac{1}{2}(I_Q\pm X)\in\mathcal D(\mathbb C^2)$ at $(a\prec b,r)$ ($\Sigma_2=X$, $\operatorname{Tr}[X\rho_{2,\pm}]=\pm 1$). On the empty-precursor branch $(S=\varnothing,b_3)$ leading to $(P_3,r_3)=(\text{edge+iso},r+b_3)$, $q(a\prec b,r,\varnothing)=\frac{1}{5}$, $r_{C_2}^{\rm foc}(\varnothing)=-\frac{21}{220}$, and $\varphi_{\varnothing,b_3}=0$, so $U_{2,\varnothing,b_3}=U_*$. Using $U_*XU_*^\dagger=Y=\Sigma_3$, the unnormalized output is
   $$
   \mathcal B^{a\prec b,r}_{\varnothing,b_3}(\rho_{2,\pm})=\frac{1}{10}\left(\frac{1}{2}\,\frac{I_Q\pm Y}{2}+\frac{1}{4}\left(1\mp\frac{21}{110}\right)I_Q\right),
   $$
   with strictly positive trace probability $p_\pm=\frac{1}{10}(1\mp\frac{21}{220})$ ($\frac{199}{2200}>0$ for $+$, $\frac{241}{2200}>0$ for $-$). Because $\operatorname{Tr}(YI_Q)=0$ and $\operatorname{Tr}(Y^2)=2$, $\operatorname{Tr}[Y\,\mathcal B^{a\prec b,r}_{\varnothing,b_3}(\rho_{2,\pm})]=\pm\frac{1}{40}\operatorname{Tr}(Y^2)=\pm\frac{1}{20}$; normalizing by $p_\pm$ produces two reachable post-measurement states $\rho'_{3,\pm}\in\mathcal D(\mathbb C^2)$ on $(\text{edge+iso},r+b_3)$ with
   $$
   \operatorname{Tr}[\Sigma_3\rho'_{3,+}]=\operatorname{Tr}[Y\rho'_{3,+}]=\frac{\frac{1}{20}}{\frac{199}{2200}}=+\frac{110}{199},
   \qquad
   \operatorname{Tr}[\Sigma_3\rho'_{3,-}]=\operatorname{Tr}[Y\rho'_{3,-}]=\frac{-\frac{1}{20}}{\frac{241}{2200}}=-\frac{110}{241}.
   $$
   Now examine step $3\to 4$ at $(\text{edge+iso},r+b_3)$. As recorded in the drift table of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#13-canonical-causal-focusing-potential-h_rm-foc-and-current-prefix-coefficient-r_ps), $H_{\rm foc}(\text{edge+iso})=0$ and $H_{\rm foc}(E)=0$ on every child $E$ of `edge+iso`, so $r_{\text{edge+iso}}^{\rm foc}(S)=0$ for all $S\in\mathcal I(\text{edge+iso})$. With $\lambda_3=\frac{1}{2}$, Theorem 1's defect operator on $(\text{edge+iso},r+b_3)$ is $\Delta O=\alpha I_Q-\frac{\varepsilon}{4}\Sigma_3$ ($\beta=0-\frac{\varepsilon}{4}=-\frac{\varepsilon}{4}$). Requiring $\operatorname{Tr}[\Delta O\,\rho'_{3,\pm}]=0$ on the two reachable states $\rho'_{3,\pm}$ forces $\alpha-\frac{\varepsilon}{4}(\frac{110}{199})=0$ and $\alpha-\frac{\varepsilon}{4}(-\frac{110}{241})=0$; subtracting gives $-\frac{\varepsilon}{4}(\frac{110}{199}+\frac{110}{241})=0$, contradicting $\varepsilon>0$.
3. At $P_0=\varnothing$, $\mathcal I(\varnothing)=\{\varnothing\}$ and $q(\varnothing,\varnothing,\varnothing)=1$, so trace preservation $1\cdot r_\varnothing(\varnothing)=0$ forces $r_\varnothing(\varnothing)=0$ and $\operatorname{Var}_q(r_\varnothing)=0$. By Theorem 1(2), (13) is solvable if and only if $\lambda_0=1$ (giving $\overline V(A_1)=V(\varnothing)$). If instead one modifies (5) at $n=0$ to allow bit-opposite drifts $r_{\varnothing,b}=(-1)^b r_0$ ($0<|r_0|\le 1-\lambda_0$, $\frac{1}{2}r_{\varnothing,0}+\frac{1}{2}r_{\varnothing,1}=0$), then $E^\varnothing_{\varnothing,b}=\frac{1}{2}(I_Q+(-1)^b r_0\Sigma_0)$ spans $\{I_Q,\Sigma_0\}$ (rank $2$), and equating $\sum_{b=0}^1 V(A_1,b)E^\varnothing_{\varnothing,b}+\lambda_0\frac{\varepsilon}{2}\Sigma_0=V(\varnothing)I_Q+\frac{\varepsilon}{2}\Sigma_0$ yields $\frac{V(A_1,0)+V(A_1,1)}{2}=V(\varnothing)$ and $\frac{V(A_1,0)-V(A_1,1)}{2}r_0=\frac{\varepsilon}{2}(1-\lambda_0)$, i.e., $V(A_1,b)=V(\varnothing)+(-1)^b\frac{\varepsilon(1-\lambda_0)}{2r_0}$. $\blacksquare$

Theorem 3(3) directly extends the classical [first-birth additive-balance obstruction](../track_b/native_additive_balance_obstruction.md) to co-rotating quantum instruments, while Theorem 3(2) exposes a genuinely multi-birth obstruction invisible at one parent: global compensation across $n=0,1,2,3$ requires $\lambda_0=1$ at empty start **and** $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ on **every** nonempty parent $P$ reachable along the four-birth poset tree (`singleton`, `2-antichain`, `2-chain`, `3-antichain`, `edge+iso`, `join`, `fork`, and `3-chain`), while still respecting mark-independent harmonicity and all diamond commutation laws.

---

### 2.2 Globally active four-birth harmonic potential $H_{\rm full}$ and exact diamond commutation from empty start

Recall from Theorem 1 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#12-the-16-unmarked-four-element-posets-and-theorem-1) that $H:\mathcal U_4\to\mathbb R$ generates mark-independent backward expectations $H(P)=\sum_{S\in\mathcal I(P)}q(P,r,S)H(P+S)$ across all $|P|\in\{0,1,2,3\}$ and all markings $r\in\{0,1\}^{|P|}$ if and only if
$$
H(E_{\text{fork+iso}})=H(E_{\text{3chain+iso}}),\qquad
H(E_{\text{asym-fork}})=H(E_{\text{diamond}}),\qquad
H(E_{\text{3-claw}})-H(E_{\text{upper-fork}})=41\bigl(H(E_{\text{4-chain}})-H(E_{\text{diamond}})\bigr).
\tag{22}
$$
Inside this 13-dimensional mark-independent harmonic space, define the **globally active harmonic potential** $H_{\rm full}:\mathcal U_4\to[0,1]$ by
$$
H_{\rm full}(E_{\text{4-chain}})=H_{\rm full}(E_{\text{diamond}})=H_{\rm full}(E_{\text{asym-fork}}):=1,
$$
$$
H_{\rm full}(E_{\text{asym-join}}):=\frac{44}{65},\qquad
H_{\rm full}(E_{\text{lower-join}}):=\frac{11}{20},\qquad
H_{\rm full}(E_{\text{3-join}}):=\frac{1}{4},
\tag{23}
$$
and $H_{\rm full}(E):=0$ on all remaining ten isomorphism classes in $\mathcal U_4$ ($E_{\text{4-antichain}}$, $E_{\text{edge+2iso}}$, $E_{\text{fork+iso}}$, $E_{\text{join+iso}}$, $E_{\text{3-claw}}$, $E_{\text{2-edges}}$, $E_{\text{N-poset}}$, $E_{\text{crown}}$, $E_{\text{3chain+iso}}$, and $E_{\text{upper-fork}}$). Pair $H_{\rm full}$ with the retention schedule and cumulative retention products
$$
(\lambda_0,\lambda_1,\lambda_2,\lambda_3):=\left(1,\,\frac{1}{2},\,\frac{1}{2},\,\frac{1}{2}\right),
\qquad
\Lambda_n:=\prod_{j=0}^{n-1}\lambda_j\implies (\Lambda_0,\Lambda_1,\Lambda_2,\Lambda_3,\Lambda_4)=\left(1,\,1,\,\frac{1}{2},\,\frac{1}{4},\,\frac{1}{8}\right),
\tag{24}
$$
coupling constant $\theta:=\frac{1}{16}$, precursor-phase family $\{\varphi_{K,b}\}$ satisfying $\varphi_{\varnothing,0}=\varphi_{\varnothing,1}=0$ (which holds in particular for the chiral singleton-$0$ rule $\varphi_{K_0,0}=\varphi_0$, zero otherwise), and current-prefix drift rule
$$
r_P(S):=\theta\,\Lambda_{|P|}^{-1}\bigl[H_{\rm full}(P+S)-H_{\rm full}(P)\bigr]\qquad (|P|\le 3,\ S\in\mathcal I(P)).
\tag{25}
$$

**Theorem 4 (Globally active four-birth two-way instrument and exact diamond commutation from empty start).** *Under $(H_{\rm full},\lambda_0=1,\lambda_{1,2,3}=\frac{1}{2},\theta=\frac{1}{16})$, the instrument family $\{\mathcal B^{P,r}_{S,b}\}$ in (5) satisfies:*

1. *(Exact mark-independent backward harmonicity, everywhere-active nonempty variance, and strict drift bound.)* *Equation (23) lies in the $[0,1]$-valued mark-independent harmonic subspace (22), with exact backward values and current-prefix drifts across all nine unmarked parents of sizes $0\le|P|\le 3$:*

   | $\lvert P\rvert$ | Unmarked parent $P$ | $\theta\Lambda_{\lvert P\rvert}^{-1}$ | $H_{\rm full}(P)$ | Ideals $S\in\mathcal I(P)$ and exact $r_P(S)$ | $\operatorname{Var}_{q(P,r,\cdot)}(r_P)$ |
   | :---: | --- | :---: | :---: | --- | :---: |
   | $0$ | $\varnothing$ | $\frac{1}{16}$ | $\frac{377}{660}$ | $S=\varnothing$: $0$ | $0$ ($\lambda_0=1$) |
   | $1$ | `singleton` $\{u\}$ | $\frac{1}{16}$ | $\frac{377}{660}$ | $\varnothing$: $-\frac{193}{21{,}120}$; $\{u\}$: $+\frac{193}{10{,}560}$ | $\frac{37{,}249}{223{,}027{,}200}>0$ |
   | $2$ | `2-antichain` $\{u,v\}$ | $\frac{1}{8}$ | $\frac{17}{40}$ | $\varnothing$: $-\frac{9}{320}$; $\{u\},\{v\},\{u,v\}$: $+\frac{3}{320}$ | $\frac{27}{102{,}400}>0$ |
   | $2$ | `2-chain` $a\prec b$ | $\frac{1}{8}$ | $\frac{19}{22}$ | $\varnothing$: $-\frac{1}{22}$; $\{a\},\{a,b\}$: $+\frac{1}{88}$ | $\frac{1}{1{,}936}>0$ |
   | $3$ | `3-antichain` $\{u,v,w\}$ | $\frac{1}{4}$ | $\frac{1}{5}$ | all $7$ proper $S\subsetneq P$: $-\frac{1}{20}$; $S=P$: $+\frac{1}{80}$ | $\frac{1}{1{,}600}>0$ |
   | $3$ | `edge+iso` ($u\prec v$, iso $w$) | $\frac{1}{4}$ | $\frac{1}{2}$ | all $5$ proper $S\subsetneq P$: $-\frac{1}{8}$; $S=P$: $+\frac{23}{520}$ | $\frac{23}{4{,}160}>0$ |
   | $3$ | `join` ($u\prec w,\ v\prec w$) | $\frac{1}{4}$ | $\frac{1}{2}$ | all $4$ proper $S\subsetneq P$: $-\frac{1}{8}$; $S=P$: $+\frac{1}{80}$ | $\frac{1}{640}>0$ |
   | $3$ | `fork` ($u\prec v,\ u\prec w$) | $\frac{1}{4}$ | $\frac{21}{22}$ | $\varnothing,\{u\}$: $-\frac{21}{88}$; $\{u,v\},\{u,w\},P$: $+\frac{1}{88}$ | $\frac{21}{7{,}744}>0$ |
   | $3$ | `3-chain` ($u\prec v\prec w$) | $\frac{1}{4}$ | $\frac{21}{22}$ | $\varnothing,\{u,v\}$: $-\frac{21}{88}$; $\{u\},P$: $+\frac{1}{88}$ | $\frac{21}{7{,}744}>0$ |

   *Every parent satisfies $\sum_{S\in\mathcal I(P)}q(P,r,S)r_P(S)=0$, every nonempty parent ($|P|\in\{1,2,3\}$) satisfies $\operatorname{Var}_{q(P,r,\cdot)}(r_P)>0$ independently of $r$, and $\max_{|P|\le 3,\,S\in\mathcal I(P)}|r_P(S)|=\frac{21}{88}<\frac{1}{2}=1-\lambda_n$ ($n=1,2,3$).*
2. *(Complete positivity, trace preservation, full support, locality, and equivariance.)* *At $n=0$, $\mathcal M_1(0,\Sigma_0,U_{0,\varnothing,b})(A)=U_*AU_*^\dagger$ is unitary CP ($\mathcal B^{\varnothing,\varnothing}_{\varnothing,b}(A)=\frac{1}{2}U_*AU_*^\dagger$). At $n\in\{1,2,3\}$, every $\mathcal B^{P,r}_{S,b}$ is strictly completely positive ($J(\mathcal B^{P,r}_{S,b})\succeq\frac{23}{352}q(P,r,S)I_4\succ 0$), with strictly positive branch traces $\ge\frac{67}{176}q(P,r,S)>0$, exact row trace preservation, maximally-mixed anchor $\mathcal B^{P,r}_{S,b}(I_Q/2)=\frac{1}{2}q(P,r,S)(I_Q/2)$ across all $n\in\{0,1,2,3\}$, proper-slot mark locality, and relabeling equivariance.*
3. *(Closed-form $m$-birth history superoperator and exact diamond + suffix commutation across $|C|\in\{0,1,2\}$.)* *For every marked base $(C,r)$ ($|C|=n\le 3$) and $m$-birth history $h=((S_0,b_0),\dots,(S_{m-1},b_{m-1}))$ ($1\le m\le 4-n$) reaching unmarked order $E=P_m$ with $W_{\rm str}(h)=\prod_{j=0}^{m-1}q(P_j,r_j,S_j)$ and $\Phi_h=\sum_{j=0}^{m-1}\varphi_{K(S_j,r_j|_{S_j}),b_j}$,*
   $$
   (\mathcal B_h\otimes\operatorname{id}_{\rm ref})(X)=2^{-m}W_{\rm str}(h)\left\{\frac{\Lambda_{n+m}}{\Lambda_n}\bigl(U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}\otimes I_{\rm ref}\bigr)X\bigl(e^{+i\frac{\Phi_h}{2}\Sigma_n}(U_*^\dagger)^m\otimes I_{\rm ref}\bigr)+\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q\!\left[\Bigl(\bigl((1-\tfrac{\Lambda_{n+m}}{\Lambda_n})I_Q+\theta\Lambda_n^{-1}\bigl(H_{\rm full}(E)-H_{\rm full}(C)\bigr)\Sigma_n\bigr)\otimes I_{\rm ref}\Bigr)X\right]\right\}.
   \tag{26}
   $$
   *Consequently, for every marked base $(C,r)$ of size $|C|\in\{0,1,2\}$ (including empty start $C=\varnothing$ with $\lambda_0=1$ and $\lambda_1=\frac{1}{2}$), every pair of downward ideals $S,T\in\mathcal I(C)$, and all newborn bits $b,c\in\{0,1\}$,*
   $$
   \bigl(\mathcal B^{C+x_S,r+b_x}_{T,c}\circ\mathcal B^{C,r}_{S,b}\bigr)\otimes\operatorname{id}_{\rm ref}
   =
   \bigl(\mathcal B^{C+y_T,r+c_y}_{S,b}\circ\mathcal B^{C,r}_{T,c}\bigr)\otimes\operatorname{id}_{\rm ref},
   \tag{27}
   $$
   *and this exact unnormalized superoperator equality persists under composition with every transported suffix through four births.*

**Proof.**
1. Clearly $H_{\rm full}\in[0,1]$ satisfies (22): $H_{\rm full}(E_{\text{fork+iso}})=0=H_{\rm full}(E_{\text{3chain+iso}})$, $H_{\rm full}(E_{\text{asym-fork}})=1=H_{\rm full}(E_{\text{diamond}})$, and $0-0=41(1-1)=0$. Evaluating the backward expectations from Section 1.2 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#12-the-16-unmarked-four-element-posets-and-theorem-1):
   - *Size $3$:* Every proper ideal of `3-antichain`, `edge+iso`, and `join` produces a class in $\mathcal U_4$ where $H_{\rm full}=0$, leaving solely their full-ideal terms: $H_{\rm full}(\text{3-antichain})=\frac{4}{5}\cdot\frac{1}{4}=\frac{1}{5}$, $H_{\rm full}(\text{edge+iso})=\frac{65}{88}\cdot\frac{44}{65}=\frac{1}{2}$, and $H_{\rm full}(\text{join})=\frac{10}{11}\cdot\frac{11}{20}=\frac{1}{2}$. On `fork` and `3-chain`, $H_{\rm full}$ coincides with $H_{\rm foc}$, giving $H_{\rm full}(\text{fork})=H_{\rm full}(\text{3-chain})=1-2e=\frac{21}{22}$.
   - *Size $2$:* $H_{\rm full}(\text{2-antichain})=\frac{1}{4}\cdot\frac{1}{5}+\frac{1}{5}\cdot\frac{1}{2}+\frac{11}{20}\cdot\frac{1}{2}=\frac{2+4+11}{40}=\frac{17}{40}$, and $H_{\rm full}(\text{2-chain})=\frac{1}{5}\cdot\frac{1}{2}+\frac{4}{5}\cdot\frac{21}{22}=\frac{11+84}{110}=\frac{95}{110}=\frac{19}{22}$.
   - *Sizes $1$ and $0$:* $H_{\rm full}(\text{singleton})=\frac{2}{3}\cdot\frac{17}{40}+\frac{1}{3}\cdot\frac{19}{22}=\frac{17}{60}+\frac{19}{66}=\frac{187+190}{660}=\frac{377}{660}=H_{\rm full}(\varnothing)$.

   Multiplying $H_{\rm full}(P+S)-H_{\rm full}(P)$ by $\theta\Lambda_{|P|}^{-1}=(\frac{1}{16},\frac{1}{16},\frac{1}{8},\frac{1}{4})$ gives every entry in the table:
   - `singleton`: $\frac{1}{16}(\frac{17}{40}-\frac{377}{660})=\frac{1}{16}(\frac{561-754}{1320})=-\frac{193}{21{,}120}$ and $\frac{1}{16}(\frac{19}{22}-\frac{377}{660})=\frac{1}{16}(\frac{1140-754}{1320})=+\frac{193}{10{,}560}$, with variance $\frac{2}{3}(\frac{193}{21{,}120})^2+\frac{1}{3}(\frac{193}{10{,}560})^2=\frac{193^2(2+4)}{3\cdot 21{,}120^2}=\frac{37{,}249}{223{,}027{,}200}$.
   - `2-antichain`: $\frac{1}{8}(\frac{1}{5}-\frac{17}{40})=-\frac{9}{320}$ ($q=\frac{1}{4}$) and $\frac{1}{8}(\frac{1}{2}-\frac{17}{40})=+\frac{3}{320}$ ($q=\frac{3}{4}$), with variance $\frac{1}{4}\frac{81}{102{,}400}+\frac{3}{4}\frac{9}{102{,}400}=\frac{27}{102{,}400}$.
   - `2-chain`: $\frac{1}{8}(\frac{1}{2}-\frac{19}{22})=-\frac{1}{22}$ ($q=\frac{1}{5}$) and $\frac{1}{8}(\frac{21}{22}-\frac{19}{22})=+\frac{1}{88}$ ($q=\frac{4}{5}$), with variance $\frac{1}{5}\frac{16}{7{,}744}+\frac{4}{5}\frac{1}{7{,}744}=\frac{4}{7{,}744}=\frac{1}{1{,}936}$.
   - `3-antichain`: $\frac{1}{4}(0-\frac{1}{5})=-\frac{1}{20}$ ($q=\frac{1}{5}$) and $\frac{1}{4}(\frac{1}{4}-\frac{1}{5})=+\frac{1}{80}$ ($q=\frac{4}{5}$), with variance $\frac{1}{5}\frac{16}{6{,}400}+\frac{4}{5}\frac{1}{6{,}400}=\frac{1}{1{,}600}$.
   - `edge+iso`: $\frac{1}{4}(0-\frac{1}{2})=-\frac{1}{8}$ ($q=\frac{23}{88}$) and $\frac{1}{4}(\frac{44}{65}-\frac{1}{2})=+\frac{23}{520}$ ($q=\frac{65}{88}$), with variance $\frac{23}{88}\frac{1}{64}+\frac{65}{88}\frac{529}{270{,}400}=\frac{23}{5{,}632}+\frac{529}{371{,}712}=\frac{23(65+23)}{88\cdot 64\cdot 65}=\frac{23}{4{,}160}$.
   - `join`: $\frac{1}{4}(0-\frac{1}{2})=-\frac{1}{8}$ ($q=\frac{1}{11}$) and $\frac{1}{4}(\frac{11}{20}-\frac{1}{2})=+\frac{1}{80}$ ($q=\frac{10}{11}$), with variance $\frac{1}{11}\frac{100}{6{,}400}+\frac{10}{11}\frac{1}{6{,}400}=\frac{1}{640}$.
   - `fork` and `3-chain`: $-\frac{21}{88}$ ($q=\frac{1}{22}$) and $+\frac{1}{88}$ ($q=\frac{21}{22}$), with variance $\frac{1}{22}\frac{441}{7{,}744}+\frac{21}{22}\frac{1}{7{,}744}=\frac{21}{7{,}744}$.
2. At $n=0$, $r_\varnothing(\varnothing)=0$, $\lambda_0=1$, and $\varphi_{\varnothing,b}=0$, so $U_{0,\varnothing,b}=U_*$ and $\mathcal M_1(0,\Sigma_0,U_*)(A)=U_*AU_*^\dagger$. At $n\in\{1,2,3\}$, $\lambda_n=\frac{1}{2}$ and $|r_P(S)|\le\frac{21}{88}<\frac{1}{2}$; by Lemma 1(2), $\lambda_{\min}(J(\mathcal M_{1/2}))=\frac{1/2-|r_P(S)|}{2}\ge\frac{23}{176}$, giving $J(\mathcal B^{P,r}_{S,b})\succeq\frac{23}{352}q(P,r,S)I_4\succ 0$ and $\operatorname{Tr}[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})]\ge\frac{1}{2}(1-\frac{21}{88})q(P,r,S)=\frac{67}{176}q(P,r,S)>0$. Evaluating (4) on $I_Q/2$ uses $\operatorname{Tr}(\Sigma_n)=0$ to give $\mathcal M_{\lambda_n}(r_P(S),\Sigma_n,U)(I_Q/2)=\frac{\lambda_n}{2}I_Q+\frac{1-\lambda_n}{2}I_Q=\frac{1}{2}I_Q$ for all $\lambda_n\in(0,1]$. Locality and equivariance follow because $r_P(S)$ depends solely on unmarked $(P,S)$ and $U_{|P|,K(S,r|_S),b}$ solely on $K(S,r|_S)$ and $b$.
3. Induct on $m\ge 1$ to establish (26). At $m=1$, $\frac{\Lambda_{n+1}}{\Lambda_n}=\lambda_n$ and $\theta\Lambda_n^{-1}(H_{\rm full}(C+S_0)-H_{\rm full}(C))=r_C(S_0)$ (including at $n=0$, where $\lambda_0=1$ and $H_{\rm full}(A_1)-H_{\rm full}(\varnothing)=0=r_\varnothing(\varnothing)$), so (26) matches (4)–(5) identically. Suppose (26) holds for an $m$-birth history $h$ ending at $(P_m,r_m)$ ($k:=n+m\le 3$), and append $(S_m,b_m)$ with weight $q_m:=q(P_m,r_m,S_m)$, retention $\lambda_k$, drift $r_m:=r_{P_m}(S_m)=\theta\Lambda_k^{-1}(H_{\rm full}(P_{m+1})-H_{\rm full}(P_m))$, and unitary $U_m:=U_{k,K_m,b_m}$. By the maximally-mixed anchor $\mathcal M_{\lambda_k}(\frac{1}{2}I_Q)=\frac{1}{2}I_Q$, the reset block in (26) passes through $\mathcal M_{\lambda_k}\otimes\operatorname{id}_{\rm ref}$ unchanged, while the coherent block $\frac{\Lambda_k}{\Lambda_n}(V_m\otimes I_{\rm ref})X(V_m^\dagger\otimes I_{\rm ref})$ ($V_m:=U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}$) maps to:
   - a new coherent block with prefactor $\lambda_k\frac{\Lambda_k}{\Lambda_n}=\frac{\Lambda_{k+1}}{\Lambda_n}$ and unitary $U_mV_m=U_*^{m+1}e^{-i\frac{\Phi_h+\varphi_{K_m,b_m}}{2}\Sigma_n}$ (using $e^{-i\frac{\alpha}{2}\Sigma_k}U_*^m=U_*^m e^{-i\frac{\alpha}{2}\Sigma_n}$); plus
   - an added reset term $\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q[\frac{\Lambda_k}{\Lambda_n}V_m^\dagger((1-\lambda_k)I_Q+r_m\Sigma_k)V_m\otimes I_{\rm ref}\cdot X]$.

   Since $V_m^\dagger\Sigma_kV_m=\Sigma_n$, $(1-\frac{\Lambda_k}{\Lambda_n})+(1-\lambda_k)\frac{\Lambda_k}{\Lambda_n}=1-\frac{\Lambda_{k+1}}{\Lambda_n}$, and $\theta\Lambda_n^{-1}(H_{\rm full}(P_m)-H_{\rm full}(C))+\frac{\Lambda_k}{\Lambda_n}\theta\Lambda_k^{-1}(H_{\rm full}(P_{m+1})-H_{\rm full}(P_m))=\theta\Lambda_n^{-1}(H_{\rm full}(P_{m+1})-H_{\rm full}(C))$, multiplying outside by $\frac{1}{2}q_m$ completes the induction for all $(\lambda_0,\dots,\lambda_3)$. Setting $m=2$ in (26) for any diamond at $(C,r)$ ($|C|\in\{0,1,2\}$) equates both birth orders because $E$, $W_{\rm str}$ (by Part A's scalar diamond identity), and $\Phi_h=\varphi_{K(S,r|_S),b}+\varphi_{K(T,r|_T),c}$ are symmetric under swapping $(x_S,b)\leftrightarrow(y_T,c)$—including at empty start $C=\varnothing$ ($S=T=\varnothing$, $W_{\rm str}=1\cdot\frac{2}{3}=\frac{2}{3}$, $\frac{\Lambda_2}{\Lambda_0}=\frac{1}{2}$, $\Phi_h=0+0=0$ for all $(b,c)\in\{0,1\}^2$, confirmed directly since step $0$ applies $\frac{1}{2}\operatorname{Ad}_{U_*}$ independently of $b$ and step $1$ applies $\frac{1}{2}\cdot\frac{2}{3}\mathcal M_{1/2}(-\frac{193}{21{,}120},Z,U_*)$ independently of $c$). Relabeling equivariance then equates every transported suffix. $\blacksquare$

---

## 3. Constructive diamond-confluent unmarked geometric potential through four births

Theorem 4 guarantees that **local** single-parent compensation (Theorem 1) is solvable at every parent of size $|P|\in\{0,1,2,3\}$. However, as highlighted in [local record compensation](../track_b/local_record_compensation.md) and [homogeneous native compensation](../track_b/homogeneous_native_compensation.md), local solvability at separate parents is far weaker than existence of a **single global potential** across four births:
1. Different parents of size $n$ transition into **shared child posets** of size $n+1$ (for instance, `2-antichain` and `2-chain` both produce `edge+iso`; `3-antichain`, `edge+iso`, `join`, `fork`, and `3-chain` share `edge+2iso`, `join+iso`, `fork+iso`, `3chain+iso`, `N-poset`, and `asym-fork`), coupling the linear systems across parents;
2. The kernel $q(P,r,S)$ depends explicitly on root marks $r_a\in\{0,1\}$ on `2-chain` and $r_u\in\{0,1\}$ on `edge+iso` and `fork`, threatening to overdetermine any mark-independent ansatz; and
3. Every incomparable-birth diamond $C\to C+x_S\to C+x_S+y_T\cong C+y_T+x_S\leftarrow C+y_T\leftarrow C$ merges two distinct birth histories into a single terminal marked order, requiring **exact diamond confluence** of the potential without hidden history tags.

We now prove that all three global constraints admit a simultaneous **purely geometric** solution $V_{\rm geom}(P)$ depending solely on the unmarked poset isomorphism class $P\in\bigsqcup_{n=0}^4\mathcal U_n$ ($1+1+2+5+16=25$ classes total)—completely independent of all vertex marks $r\in\{0,1\}^{|P|}$!

**Theorem 5 (Existence and explicit rational construction of a diamond-confluent unmarked geometric potential $V_{\rm geom}$ through four births).** *Under the globally active four-birth instrument $(H_{\rm full},\lambda_0=1,\lambda_{1,2,3}=\frac{1}{2},\theta=\frac{1}{16})$ of Theorem 4 and bounded stage Hamiltonian $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ ($\varepsilon>0$), define $V_{\rm geom}:\bigsqcup_{n=0}^4\mathcal U_n\to\mathbb Q\,\varepsilon$ across all $25$ unmarked poset classes (normalized by $V_{\rm geom}(\varnothing):=0$) by the exact rational table:*

| $\lvert P\rvert$ | Unmarked poset class $P\in\mathcal U_{\lvert P\rvert}$ | Exact rational ratio $v(P):=V_{\rm geom}(P)/\varepsilon$ |
| :---: | --- | :---: |
| $0$ | $\varnothing$ | $0$ |
| $1$ | `singleton` ($A_1$) | $0$ |
| $2$ | `2-antichain` ($A_2$) | $-\dfrac{2{,}640}{193}$ |
| $2$ | `2-chain` ($C_2$) | $+\dfrac{5{,}280}{193}$ |
| $3$ | `3-antichain` ($A_3$) | $-\dfrac{23{,}360}{579}$ |
| $3$ | `edge+iso` ($C_2\sqcup A_1$) | $+\dfrac{1{,}034}{193}$ |
| $3$ | `join` ($A_2\oplus A_1$) | $-\dfrac{54{,}008}{6{,}369}$ |
| $3$ | `fork` ($A_1\oplus A_2$) | $+\dfrac{12{,}683}{386}$ |
| $3$ | `3-chain` ($C_3$) | $+\dfrac{12{,}683}{386}$ |
| $4$ | $E_{\text{edge+2iso}},\,E_{\text{join+iso}},\,E_{\text{fork+iso}},\,E_{\text{3chain+iso}},\,E_{\text{N-poset}}$ ($5$ shared classes) | $0$ |
| $4$ | $E_{\text{4-antichain}}$ ($A_4$) | $-\dfrac{307{,}472}{579}$ |
| $4$ | $E_{\text{3-join}}$ ($A_3\oplus A_1$) | $-\dfrac{20{,}465}{579}$ |
| $4$ | $E_{\text{crown}}$ ($A_2\oplus A_2$) | $-\dfrac{725{,}552}{6{,}369}$ |
| $4$ | $E_{\text{lower-join}}$ ($A_2\oplus C_2$) | $-\dfrac{41{,}270}{6{,}369}$ |
| $4$ | $E_{\text{2-edges}}$ ($C_2\sqcup C_2$) | $-\dfrac{654}{193}$ |
| $4$ | $E_{\text{asym-join}}$ ($(C_2\sqcup A_1)\oplus A_1$) | $+\dfrac{1{,}420}{193}$ |
| $4$ | $E_{\text{3-claw}}$ ($A_1\oplus A_3$) and $E_{\text{upper-fork}}$ ($C_2\oplus A_2$) | $+\dfrac{4{,}191}{193}$ |
| $4$ | $E_{\text{asym-fork}}$, $E_{\text{diamond}}$ ($A_1\oplus A_2\oplus A_1$), and $E_{\text{4-chain}}$ ($C_4$) | $+\dfrac{274{,}835}{8{,}106}$ |

*Then:*
1. *(Simultaneous all-mark master satisfaction.)* *Setting $V(P,r):=V_{\rm geom}(P)$ satisfies both master equations (I) and (II) of Theorem 1 simultaneously across **every** marked parent $(P,r)$ of sizes $|P|\in\{0,1,2,3\}$ and **every** marking $r\in\{0,1\}^{|P|}$.*
2. *(Automatic diamond confluence.)* *Because $V_{\rm geom}(P)$ is an isomorphism invariant of the unmarked poset $P$ alone, $V_{\rm geom}((C+x_S)+y_T)=V_{\rm geom}((C+y_T)+x_S)$ holds identically across every incomparable-birth diamond and every multi-birth history merging into the same terminal poset, with zero path memory or history tags.*

**Proof.** Write $v(P):=V_{\rm geom}(P)/\varepsilon$. Since $V(P,r)=\varepsilon\,v(P)$ is independent of $r$ and of newborn bits $b\in\{0,1\}$, $\overline V(P+S,r)=\varepsilon\,v(P+S)$, and dividing (13) by $\varepsilon>0$ reduces Theorem 1's master pair at every marked parent $(P,r)$ ($|P|=n\in\{0,1,2,3\}$) to
$$
\text{\rm (I)}\quad \sum_{S\in\mathcal I(P)}q(P,r,S)\,v(P+S)=v(P),
\qquad
\text{\rm (II)}\quad \sum_{S\in\mathcal I(P)}q(P,r,S)\,r_P(S)\,v(P+S)=\frac{1-\lambda_n}{2}=
\begin{cases}
0, & n=0,\\[3pt]
\dfrac{1}{4}, & n\in\{1,2,3\}.
\end{cases}
\tag{28}
$$
First, verify why root-mark dependence cancels identically out of **both** (I) and (II) on all three mark-sensitive unmarked parent shapes (`2-chain`, `edge+iso`, and `fork`) under our tie-conditions:
- On `2-chain` ($a\prec b$), only $S=\{a\}\to\text{fork}$ ($q=f_{r_a}$) and $S=\{a,b\}\to\text{3-chain}$ ($q=h_{r_a}$) depend on $r$, and by Theorem 4(1) they share the **exact same drift** $r_{C_2}(\{a\})=r_{C_2}(\{a,b\})=+\frac{1}{88}$. Hence imposing $v(\text{fork})=v(\text{3-chain})$ combines their weights into $f_{r_a}+h_{r_a}=\frac{4}{5}$ in (I) and $(f_{r_a}+h_{r_a})(+\frac{1}{88})=\frac{1}{110}$ in (II), eliminating $r_a\in\{0,1\}$ from both equations.
- On `edge+iso` ($u\prec v$, isolate $w$), only $S=\{u\}\to E_{\text{fork+iso}}$ ($q=5ef_{r_u}$) and $S=\{u,v\}\to E_{\text{3chain+iso}}$ ($q=5eh_{r_u}$) depend on $r$, and by Theorem 4(1) they share the **exact same drift** $r_{\text{edge+iso}}(\{u\})=r_{\text{edge+iso}}(\{u,v\})=-\frac{1}{8}$. Hence imposing $v(E_{\text{fork+iso}})=v(E_{\text{3chain+iso}})$ combines their weights into $5e(f_{r_u}+h_{r_u})=\frac{1}{11}$ in (I) and $-\frac{1}{88}$ in (II) (both $0$ when $v(E_{\text{fork+iso}})=v(E_{\text{3chain+iso}})=0$), eliminating $r_u\in\{0,1\}$ from both equations.
- On `fork` ($u\prec v,\ u\prec w$), only $S=\{u,v\},\{u,w\}\to E_{\text{asym-fork}}$ (combined weight $2e\frac{h_{r_u}}{f_{r_u}}$) and $S=\{u,v,w\}\to E_{\text{diamond}}$ (weight $1-2e-2e\frac{h_{r_u}}{f_{r_u}}$) depend on $r$, and by Theorem 4(1) all three ideals share the **exact same drift** $r_{\text{fork}}(S)=+\frac{1}{88}$. Hence imposing $v(E_{\text{asym-fork}})=v(E_{\text{diamond}})=:v_{\rm diam}$ combines their weights into $1-2e=\frac{21}{22}$ in (I) and $\frac{21}{22}(+\frac{1}{88})=\frac{21}{1{,}936}$ in (II), eliminating $r_u\in\{0,1\}$ from both equations.

Now solve and verify (28) stage by stage in exact rational arithmetic:

1. **Stage $0\to 1$ ($P=\varnothing$, $\lambda_0=1$, $r_\varnothing(\varnothing)=0$):** With $v(\varnothing)=0$ and $v(\text{singleton})=0$, (I) reads $1\cdot 0=0$ and (II) reads $1\cdot 0\cdot 0=0$.

2. **Stage $1\to 2$ (`singleton` $\{u\}$, $v(A_1)=0$, $\lambda_1=\frac{1}{2}$):** Here $(q(\varnothing),q(\{u\}))=(\frac{2}{3},\frac{1}{3})$ and $(r_{A_1}(\varnothing),r_{A_1}(\{u\}))=(-\frac{193}{21{,}120},+\frac{193}{10{,}560})$.
   - Equation (I): $\frac{2}{3}v(A_2)+\frac{1}{3}v(C_2)=\frac{2}{3}(-\frac{2{,}640}{193})+\frac{1}{3}(+\frac{5{,}280}{193})=\frac{-5{,}280+5{,}280}{579}=0=v(A_1)$.
   - Equation (II): $\frac{2}{3}(-\frac{193}{21{,}120})(-\frac{2{,}640}{193})+\frac{1}{3}(+\frac{193}{10{,}560})(+\frac{5{,}280}{193})=\frac{5{,}280+10{,}560}{63{,}360}=\frac{15{,}840}{63{,}360}=\frac{1}{4}$.

3. **Stage $2\to 3$ (`2-chain` then `2-antichain`, $\lambda_2=\frac{1}{2}$):**
   - *Parent `2-chain` ($v(C_2)=+\frac{5{,}280}{193}$, solving for $v(\text{edge+iso})$ and $v(\text{fork})=v(\text{3-chain})$):* With $q=(\frac{1}{5},\frac{4}{5})$ and $r=(-\frac{1}{22},+\frac{1}{88})$ on (`edge+iso`, `fork`/`3-chain`), (II) reads $\frac{1}{110}(v(\text{fork})-v(\text{edge+iso}))=\frac{1}{4}$, i.e., $v(\text{fork})-v(\text{edge+iso})=\frac{55}{2}$, and (I) reads $\frac{1}{5}v(\text{edge+iso})+\frac{4}{5}v(\text{fork})=\frac{5{,}280}{193}$. Substituting $v(\text{edge+iso})=v(\text{fork})-\frac{55}{2}$ gives $v(\text{fork})=\frac{5{,}280}{193}+\frac{11}{2}=\frac{10{,}560+2{,}123}{386}=+\frac{12{,}683}{386}=v(\text{3-chain})$ and $v(\text{edge+iso})=\frac{12{,}683-10{,}615}{386}=\frac{2{,}068}{386}=+\frac{1{,}034}{193}$.
     *Direct check:* (I) $\frac{1}{5}\cdot\frac{2{,}068}{386}+\frac{4}{5}\cdot\frac{12{,}683}{386}=\frac{2{,}068+50{,}732}{5\cdot 386}=\frac{52{,}800}{1{,}930}=+\frac{5{,}280}{193}$; (II) $\frac{1}{110}\cdot\frac{12{,}683-2{,}068}{386}=\frac{10{,}615}{42{,}460}=\frac{55\cdot 193}{220\cdot 193}=\frac{1}{4}$.
   - *Parent `2-antichain` ($v(A_2)=-\frac{2{,}640}{193}$, substituting $v(\text{edge+iso})=+\frac{1{,}034}{193}$ to solve for $v(A_3)$ and $v(\text{join})$):* Put $W:=\frac{1}{5}v(\text{edge+iso})+\frac{11}{20}v(\text{join})$. Equations (I) and (II) read $\frac{1}{4}v(A_3)+W=-\frac{2{,}640}{193}$ and $-\frac{9}{1{,}280}v(A_3)+\frac{3}{320}W=\frac{1}{4}$ (equivalently $-\frac{3}{4}v(A_3)+W=\frac{80}{3}$). Subtracting yields $v(A_3)=-\frac{2{,}640}{193}-\frac{80}{3}=\frac{-7{,}920-15{,}440}{579}=-\frac{23{,}360}{579}$, whence $W=-\frac{2{,}640}{193}+\frac{5{,}840}{579}=-\frac{2{,}080}{579}$ and $\frac{11}{20}v(\text{join})=-\frac{2{,}080}{579}-\frac{1}{5}\cdot\frac{3{,}102}{579}=-\frac{13{,}502}{5\cdot 579}$, giving $v(\text{join})=-\frac{54{,}008}{6{,}369}$.
     *Direct check:* (I) $-\frac{5{,}840}{579}+\frac{3{,}102-13{,}502}{5\cdot 579}=-\frac{5{,}840+2{,}080}{579}=-\frac{7{,}920}{579}=-\frac{2{,}640}{193}$; (II) $(-\frac{9}{1{,}280})(-\frac{23{,}360}{579})+\frac{3}{320}(-\frac{2{,}080}{579})=\frac{657-78}{4\cdot 579}=\frac{579}{4\cdot 579}=\frac{1}{4}$.

4. **Stage $3\to 4$ (Block-triangular solution across all five size-$3$ parents, $\lambda_3=\frac{1}{2}$):** Fix $v=0$ on the five shared non-private size-$4$ classes $E_{\text{edge+2iso}},E_{\text{join+iso}},E_{\text{fork+iso}},E_{\text{3chain+iso}},E_{\text{N-poset}}$, set $v(E_{\text{asym-fork}})=v(E_{\text{diamond}})=:v_{\rm diam}$, and solve the five $2\times 2$ parent systems in block-triangular order:
   - *(4.1) `3-antichain` ($v(A_3)=-\frac{23{,}360}{579}$) for $(v(E_{\text{4-antichain}}),v(E_{\text{3-join}}))$:* Nonzero-potential ideals are $S=\varnothing\to E_{\text{4-antichain}}$ ($q=\frac{1}{44},r=-\frac{1}{20}$) and $S=P\to E_{\text{3-join}}$ ($q=\frac{4}{5},r=+\frac{1}{80}$):
     $$
     \frac{1}{44}v(E_{\text{4-antichain}})+\frac{4}{5}v(E_{\text{3-join}})=-\frac{23{,}360}{579},
     \qquad
     -\frac{1}{880}v(E_{\text{4-antichain}})+\frac{1}{100}v(E_{\text{3-join}})=\frac{1}{4}.
     $$
     Subtracting $80\times\text{(II)}$ ($-\frac{1}{11}v(E_{\text{4-antichain}})+\frac{4}{5}v(E_{\text{3-join}})=20$) from (I) gives $\frac{5}{44}v(E_{\text{4-antichain}})=-\frac{23{,}360+11{,}580}{579}=-\frac{34{,}940}{579}\implies v(E_{\text{4-antichain}})=-44\cdot\frac{6{,}988}{579}=-\frac{307{,}472}{579}$ and $\frac{4}{5}v(E_{\text{3-join}})=20-\frac{27{,}952}{579}=-\frac{16{,}372}{579}\implies v(E_{\text{3-join}})=-5\cdot\frac{4{,}093}{579}=-\frac{20{,}465}{579}$.
     *Direct check:* (I) $\frac{-6{,}988-16{,}372}{579}=-\frac{23{,}360}{579}$; (II) $\frac{307{,}472/880-20{,}465/100}{579}=\frac{6{,}988-4{,}093}{20\cdot 579}=\frac{2{,}895}{20\cdot 579}=\frac{1}{4}$.
   - *(4.2) `join` ($v(\text{join})=-\frac{54{,}008}{6{,}369}$) for $(v(E_{\text{crown}}),v(E_{\text{lower-join}}))$:* Nonzero-potential ideals are $S=\{u,v\}\to E_{\text{crown}}$ ($q=\frac{1}{44},r=-\frac{1}{8}$) and $S=P\to E_{\text{lower-join}}$ ($q=\frac{10}{11},r=+\frac{1}{80}$):
     $$
     \frac{1}{44}v(E_{\text{crown}})+\frac{10}{11}v(E_{\text{lower-join}})=-\frac{54{,}008}{6{,}369},
     \qquad
     -\frac{1}{352}v(E_{\text{crown}})+\frac{1}{88}v(E_{\text{lower-join}})=\frac{1}{4}.
     $$
     Subtracting $80\times\text{(II)}$ ($-\frac{5}{22}v(E_{\text{crown}})+\frac{10}{11}v(E_{\text{lower-join}})=20$) from (I) gives $\frac{1}{4}v(E_{\text{crown}})=-\frac{54{,}008+127{,}380}{6{,}369}=-\frac{181{,}388}{6{,}369}\implies v(E_{\text{crown}})=-\frac{725{,}552}{6{,}369}$ and $v(E_{\text{lower-join}})=22+\frac{1}{4}v(E_{\text{crown}})=\frac{140{,}118-181{,}388}{6{,}369}=-\frac{41{,}270}{6{,}369}$.
     *Direct check:* (I) $\frac{-181{,}388-412{,}700}{11\cdot 6{,}369}=-\frac{594{,}088}{11\cdot 6{,}369}=-\frac{54{,}008}{6{,}369}$; (II) $\frac{181{,}388-41{,}270}{88\cdot 6{,}369}=\frac{140{,}118}{88\cdot 6{,}369}=\frac{22}{88}=\frac{1}{4}$.
   - *(4.3) `edge+iso` ($v(\text{edge+iso})=+\frac{1{,}034}{193}$) for $(v(E_{\text{2-edges}}),v(E_{\text{asym-join}}))$:* Nonzero-potential ideals are $S=\{w\}\to E_{\text{2-edges}}$ ($q=\frac{1}{44},r=-\frac{1}{8}$) and $S=P\to E_{\text{asym-join}}$ ($q=\frac{65}{88},r=+\frac{23}{520}$):
     $$
     \frac{1}{44}v(E_{\text{2-edges}})+\frac{65}{88}v(E_{\text{asym-join}})=\frac{1{,}034}{193},
     \qquad
     -\frac{2}{704}v(E_{\text{2-edges}})+\frac{23}{704}v(E_{\text{asym-join}})=\frac{1}{4}.
     $$
     Adding $88\times\text{(I)}$ ($2v(E_{\text{2-edges}})+65v(E_{\text{asym-join}})=88\cdot\frac{1{,}034}{193}$) to $704\times\text{(II)}$ ($-2v(E_{\text{2-edges}})+23v(E_{\text{asym-join}})=176$) gives $88\,v(E_{\text{asym-join}})=176+88\cdot\frac{1{,}034}{193}\implies v(E_{\text{asym-join}})=2+\frac{1{,}034}{193}=+\frac{1{,}420}{193}$ and $v(E_{\text{2-edges}})=-65+\frac{23\cdot 517}{193}=\frac{-12{,}545+11{,}891}{193}=-\frac{654}{193}$.
     *Direct check:* (I) $\frac{2(-654)+65(1{,}420)}{88\cdot 193}=\frac{-1{,}308+92{,}300}{88\cdot 193}=\frac{90{,}992}{88\cdot 193}=+\frac{1{,}034}{193}$; (II) $\frac{1{,}308+32{,}660}{704\cdot 193}=\frac{33{,}968}{704\cdot 193}=\frac{176\cdot 193}{704\cdot 193}=\frac{1}{4}$.
   - *(4.4) `fork` FIRST ($v(\text{fork})=+\frac{12{,}683}{386}$) for $(v(E_{\text{3-claw}}),v_{\rm diam})$:* Nonzero-potential ideals are $S=\{u\}\to E_{\text{3-claw}}$ ($q=\frac{1}{44},r=-\frac{21}{88}$) and $S\in\{\{u,v\},\{u,w\},P\}\to E_{\text{asym-fork}}/E_{\text{diamond}}$ (combined $q=\frac{21}{22},r=+\frac{1}{88}$):
     $$
     \frac{1}{44}v(E_{\text{3-claw}})+\frac{21}{22}v_{\rm diam}=\frac{12{,}683}{386},
     \qquad
     -\frac{21}{3{,}872}v(E_{\text{3-claw}})+\frac{21}{1{,}936}v_{\rm diam}=\frac{1}{4}.
     $$
     Multiplying (I) by $44$ ($v(E_{\text{3-claw}})+42v_{\rm diam}=22\cdot\frac{12{,}683}{193}$) and (II) by $\frac{3{,}872}{21}$ ($-v(E_{\text{3-claw}})+2v_{\rm diam}=\frac{968}{21}$) and adding yields $44\,v_{\rm diam}=\frac{968}{21}+22\cdot\frac{12{,}683}{193}\implies v_{\rm diam}=\frac{22}{21}+\frac{12{,}683}{386}=\frac{8{,}492+266{,}343}{8{,}106}=+\frac{274{,}835}{8{,}106}$, and $v(E_{\text{3-claw}})=2v_{\rm diam}-\frac{968}{21}=\frac{44-968}{21}+\frac{12{,}683}{193}=-44+\frac{12{,}683}{193}=\frac{-8{,}492+12{,}683}{193}=+\frac{4{,}191}{193}$.
     *Direct check:* (I) $\frac{4{,}191+274{,}835}{44\cdot 193}=\frac{279{,}026}{44\cdot 193}=\frac{22\cdot 12{,}683}{44\cdot 193}=+\frac{12{,}683}{386}$ (using $\frac{21}{22}\cdot\frac{1}{8{,}106}=\frac{1}{22\cdot 386}=\frac{1}{44\cdot 193}$); (II) $\frac{21}{3{,}872}(2v_{\rm diam}-v(E_{\text{3-claw}}))=\frac{21}{3{,}872}\cdot\frac{968}{21}=\frac{1}{4}$.
   - *(4.5) `3-chain` SECOND ($v(\text{3-chain})=+\frac{12{,}683}{386}$, substituting the already-determined $v(E_{\text{asym-fork}})=v_{\rm diam}=+\frac{274{,}835}{8{,}106}$ on $S=\{u\}$) for its private children $(v(E_{\text{upper-fork}}),v(E_{\text{4-chain}}))$:* Moving the known $S=\{u\}$ term ($q=\frac{1}{44},r=+\frac{1}{88}$) to the right-hand side yields
     $$
     \frac{1}{44}v(E_{\text{upper-fork}})+\frac{41}{44}v(E_{\text{4-chain}})=\frac{12{,}683}{386}-\frac{1}{44}v_{\rm diam},
     \qquad
     -\frac{21}{3{,}872}v(E_{\text{upper-fork}})+\frac{41}{3{,}872}v(E_{\text{4-chain}})=\frac{1}{4}-\frac{1}{3{,}872}v_{\rm diam}.
     $$
     Comparing with System (4.4) ($\frac{1}{44}v(E_{\text{3-claw}})+\frac{41}{44}v_{\rm diam}=\frac{12{,}683}{386}-\frac{1}{44}v_{\rm diam}$ and $-\frac{21}{3{,}872}v(E_{\text{3-claw}})+\frac{41}{3{,}872}v_{\rm diam}=\frac{1}{4}-\frac{1}{3{,}872}v_{\rm diam}$) and noting that the $2\times 2$ coefficient matrix has nonzero determinant $\frac{41(1+21)}{44\cdot 3{,}872}=\frac{41}{7{,}744}\ne 0$, the unique solution is $v(E_{\text{upper-fork}})=v(E_{\text{3-claw}})=+\frac{4{,}191}{193}$ and $v(E_{\text{4-chain}})=v_{\rm diam}=+\frac{274{,}835}{8{,}106}$.
     *Direct check:* (I) $0+\frac{1}{44}\cdot\frac{274{,}835}{8{,}106}+\frac{1}{44}\cdot\frac{4{,}191}{193}+\frac{41}{44}\cdot\frac{274{,}835}{8{,}106}=\frac{4{,}191+274{,}835}{44\cdot 193}=+\frac{12{,}683}{386}$; (II) $0+\frac{1}{3{,}872}\cdot\frac{274{,}835}{8{,}106}-\frac{21}{3{,}872}\cdot\frac{4{,}191}{193}+\frac{41}{3{,}872}\cdot\frac{274{,}835}{8{,}106}=\frac{21}{3{,}872}(2v_{\rm diam}-v(E_{\text{3-claw}}))=\frac{1}{4}$.

Finally, for any incomparable-birth diamond at $(C,r)$ with downward ideals $S,T\in\mathcal I(C)$, the canonical newborn-swap bijection is an order isomorphism $(C+x_S)+y_T\cong (C+y_T)+x_S$ into the exact same unmarked poset class in $\mathcal U_{|C|+2}$, so $V_{\rm geom}((C+x_S)+y_T)=V_{\rm geom}((C+y_T)+x_S)$ holds identically. $\blacksquare$

## 4. Multi-birth quantum-to-geometry energy exchange ledger, coherent phase coexistence, and imperfect-detector bounds

### 4.1 Path-independent joint conservation and exact quantum-to-geometry conversion

Combine the globally active instrument $(H_{\rm full},\lambda_0=1,\lambda_{1,2,3}=\frac{1}{2},\theta=\frac{1}{16})$ of Theorem 4 with the unmarked geometric potential $V_{\rm geom}:\bigsqcup_{n=0}^4\mathcal U_n\to\mathbb Q\,\varepsilon$ of Theorem 5 and the bounded co-rotating stage Hamiltonian $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ ($\varepsilon>0$). For any finite-dimensional passive reference space $\mathcal H_{\rm ref}$, any unmarked poset $P\in\bigsqcup_{n=0}^4\mathcal U_n$ ($|P|=n$), and any joint state $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, define the joint quantum-plus-order functional
$$
\mathcal C(P,\rho_{Q,\rm ref}):=V_{\rm geom}(P)+\operatorname{Tr}\!\bigl[(H_{|P|}\otimes I_{\rm ref})\rho_{Q,\rm ref}\bigr].
\tag{29}
$$
For any marked base $(C,r)$ of size $|C|=n\le 3$, initial state $\rho_{n}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, and horizon step $m\in\{1,\dots,4-n\}$, every $m$-birth history $h=((S_0,b_0),\dots,(S_{m-1},b_{m-1}))$ occurs with active trace probability $p_h(\rho_n):=\operatorname{Tr}[(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(\rho_n)]>0$ ($\sum_h p_h(\rho_n)=1$) and conditional post-measurement state $\rho_{n+m,h}:=(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(\rho_n)/p_h(\rho_n)$, so for any stage-$(n+m)$ observable $A$, $\mathbb E_{\rho_n,r}[\operatorname{Tr}((A\otimes I_{\rm ref})\rho_{n+m})]=\sum_h\operatorname{Tr}[(A\otimes I_{\rm ref})(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(\rho_n)]$.

**Theorem 6 (Multi-birth joint conservation, exact quantum-to-geometry conversion, and phase-backaction coexistence).** *Under $(H_{\rm full},\lambda_0=1,\lambda_{1,2,3}=\frac{1}{2},\theta=\frac{1}{16})$ and $V_{\rm geom}$:*

1. *(Exact multi-step martingale conservation across all markings and reference entanglements.)* *For every marked base $(C,r)$ ($|C|=n\in\{0,1,2,3\}$), every $m\in\{1,\dots,4-n\}$, and every initial joint state $\rho_n\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$,*
   $$
   \mathbb E_{\rho_n,r}\!\bigl[\mathcal C(P_{n+m},\rho_{n+m})\bigr]
   =\sum_h\Bigl(V_{\rm geom}(P_{n+m,h})\operatorname{Tr}\!\bigl[(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(\rho_n)\bigr]+\operatorname{Tr}\!\bigl[(H_{n+m}\otimes I_{\rm ref})(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(\rho_n)\bigr]\Bigr)
   =\mathcal C(C,\rho_n),
   \tag{30}
   $$
   *with exact stage-by-stage quantum expectation decay*
   $$
   \mathbb E_{\rho_n,r}\!\Bigl[\operatorname{Tr}\!\bigl[(H_{n+m}\otimes I_{\rm ref})\rho_{n+m}\bigr]\Bigr]
   =E_0+\frac{\Lambda_{n+m}}{\Lambda_n}\,\frac{\varepsilon}{2}\operatorname{Tr}\!\bigl[(\Sigma_n\otimes I_{\rm ref})\rho_n\bigr].
   \tag{31}
   $$
2. *(Empty-start four-birth conversion law, $P_0=\varnothing$.)* *Starting from $P_0=\varnothing$ ($V_{\rm geom}(\varnothing)=0$, $\Sigma_0=Y$, $\Lambda_0=1$, $\Lambda_4=\frac{1}{8}$), for every initial qubit state $\rho_0\in\mathcal D(\mathbb C^2)$,*
   $$
   \mathbb E_{\rho_0}\!\bigl[V_{\rm geom}(P_4)\bigr]
   =\operatorname{Tr}[H_0\rho_0]-\mathbb E_{\rho_0}\!\bigl[\operatorname{Tr}(H_4\rho_4)\bigr]
   =\frac{7\varepsilon}{16}\operatorname{Tr}[Y\rho_0].
   \tag{32}
   $$
3. *(Prepared causal-prefix conversion law above $a\prec b$, $P_2=C_2$.)* *Starting from $P_2=(a\prec b)$ with any root and leaf marks $(r_a,r_b)\in\{0,1\}^2$ ($V_{\rm geom}(a\prec b)=+\frac{5{,}280}{193}\varepsilon$, $\Sigma_2=X$, $\frac{\Lambda_4}{\Lambda_2}=\frac{1}{4}$), for every initial qubit state $\rho_2\in\mathcal D(\mathbb C^2)$,*
   $$
   \mathbb E_{\rho_2,r}\!\bigl[V_{\rm geom}(P_4)-V_{\rm geom}(a\prec b)\bigr]
   =\operatorname{Tr}[H_2\rho_2]-\mathbb E_{\rho_2,r}\!\bigl[\operatorname{Tr}(H_4\rho_4)\bigr]
   =\frac{3\varepsilon}{8}\operatorname{Tr}[X\rho_2],
   \tag{33}
   $$
   *converting $100\%$ of the damped off-diagonal computational-basis coherence $\frac{3\varepsilon}{8}\cdot 2\operatorname{Re}(\rho_2)_{01}$ into committed causal-order geometric potential **independently** of $(r_a,r_b)\in\{0,1\}^2$ and of the precursor-phase schedule $\{\varphi_{K,b}\}$.*
4. *(Degenerate-subspace phase-backaction coexistence at fixed conserved energy.)* *Under the chiral singleton-$0$ phase schedule ($\varphi_{K_0,0}=\varphi_0$, zero otherwise) on $P_2=(a\prec b)$ with marks $(r_a,0)$ ($r_a\in\{0,1\}$), the unselected two-birth terminal state $\mathcal E_{r_a}(\rho_2):=\sum_h\mathcal B_h(\rho_2)$ satisfies for every $\rho_2\in\mathcal D(\mathbb C^2)$:*
   $$
   \mathbb E_{\rho_2,r_a}\!\bigl[\operatorname{Tr}(Y\rho_4)\bigr]
   =\operatorname{Tr}\!\bigl[Y\,\mathcal E_{r_a}(\rho_2)\bigr]
   =\frac{1}{4}\sum_{k=0}^2\nu_{r_a}(k)\Bigl[\cos(k\varphi_0)\operatorname{Tr}(Z\rho_2)+\sin(k\varphi_0)\operatorname{Tr}(Y\rho_2)\Bigr],
   \tag{34}
   $$
   *where $(\nu_0(0),\nu_0(1),\nu_0(2))=(\frac{4{,}781}{5{,}280},\frac{247}{2{,}640},\frac{1}{1{,}056})$ and $(\nu_1(0),\nu_1(1),\nu_1(2))=(\frac{879}{880},\frac{1}{880},0)$. At $\varphi_0=\frac{\pi}{2}$, the root-mark contrast $\Delta_{r_a}\mathbb E[\operatorname{Tr}(Y\rho_4)]:=\mathbb E_{\rho_2,0}[\operatorname{Tr}(Y\rho_4)]-\mathbb E_{\rho_2,1}[\operatorname{Tr}(Y\rho_4)]$ is*
   $$
   \Delta_{r_a}\mathbb E\bigl[\operatorname{Tr}(Y\rho_4)\bigr]=-\frac{83}{3{,}520}\operatorname{Tr}(Z\rho_2)+\frac{61}{2{,}640}\operatorname{Tr}(Y\rho_2),
   \tag{35}
   $$
   *which is strictly nonzero across generic initial states—for example $-\frac{83}{4{,}400}\ne 0$ on $|\psi_{3,4}\rangle=\frac{2}{\sqrt 5}|+\rangle+\frac{1}{\sqrt 5}|-\rangle$ (where both $r_a\in\{0,1\}$ share identical conserved energy $E_0+\frac{53{,}379}{1{,}930}\varepsilon$ and identical energy conversion $+\frac{9\varepsilon}{40}$) and $+\frac{61}{2{,}640}\ne 0$ on $|+_Y\rangle=\frac{1}{\sqrt 2}(|0\rangle+i|1\rangle)$ (where zero net energy transfers)—without disturbing $\mathcal C$.*

**Proof.**
1. By Theorem 5(1) and Theorem 1(1), for every marked parent $(P,r)$ ($|P|=k\le 3$) and every unnormalized positive operator $M\in\mathcal B_+(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, linearity of (12) on $\rho_{Q,\rm ref}=M/\operatorname{Tr}(M)$ (trivial when $M=0$) gives the exact one-step telescoping identity
   $$
   \sum_{S\in\mathcal I(P)}\sum_{b\in\{0,1\}}\Bigl(V_{\rm geom}(P+S)\operatorname{Tr}\!\bigl[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(M)\bigr]+\operatorname{Tr}\!\bigl[(H_{k+1}\otimes I_{\rm ref})(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(M)\bigr]\Bigr)
   =V_{\rm geom}(P)\operatorname{Tr}(M)+\operatorname{Tr}\!\bigl[(H_k\otimes I_{\rm ref})M\bigr].
   $$
   Applying this identity inductively at $M=(\mathcal B_{h'}\otimes\operatorname{id}_{\rm ref})(\rho_n)$ from $m-1$ down to $0$ proves (30). Similarly, summing Lemma 1's identity (8) over $(S,b)$ gives $\sum_{S,b}(\mathcal B^{P,r}_{S,b})^\dagger(H_{k+1})=E_0I_Q+\lambda_k\frac{\varepsilon}{2}\Sigma_k$ and $\sum_{S,b}(\mathcal B^{P,r}_{S,b})^\dagger(I_Q)=I_Q$; iterating $m$ times multiplies $\Sigma_n$ by $\prod_{j=0}^{m-1}\lambda_{n+j}=\frac{\Lambda_{n+m}}{\Lambda_n}$ and proves (31).
2. Subtracting (31) at $(n,m)=(0,4)$ ($\frac{\Lambda_4}{\Lambda_0}=\frac{1}{8}$, $\Sigma_0=Y$, $V_{\rm geom}(\varnothing)=0$) from (30) yields
   $$
   \mathbb E_{\rho_0}\!\bigl[V_{\rm geom}(P_4)\bigr]
   =\left(E_0+\frac{\varepsilon}{2}\operatorname{Tr}[Y\rho_0]\right)-\left(E_0+\frac{1}{8}\,\frac{\varepsilon}{2}\operatorname{Tr}[Y\rho_0]\right)
   =\left(1-\frac{1}{8}\right)\frac{\varepsilon}{2}\operatorname{Tr}[Y\rho_0]
   =\frac{7\varepsilon}{16}\operatorname{Tr}[Y\rho_0].
   $$
3. Subtracting (31) at $(n,m)=(2,2)$ ($\frac{\Lambda_4}{\Lambda_2}=\frac{1/8}{1/2}=\frac{1}{4}$, $\Sigma_2=X$) from (30) yields
   $$
   \mathbb E_{\rho_2,r}\!\bigl[V_{\rm geom}(P_4)-V_{\rm geom}(a\prec b)\bigr]
   =\left(E_0+\frac{\varepsilon}{2}\operatorname{Tr}[X\rho_2]\right)-\left(E_0+\frac{1}{4}\,\frac{\varepsilon}{2}\operatorname{Tr}[X\rho_2]\right)
   =\frac{3\varepsilon}{8}\operatorname{Tr}[X\rho_2],
   $$
   where $\operatorname{Tr}[X\rho_2]=\langle 0|\rho_2|1\rangle+\langle 1|\rho_2|0\rangle=2\operatorname{Re}(\rho_2)_{01}$.

   *(Independent 15-row active covariance check above $a\prec b$.)* Taking $\operatorname{Tr}$ of (26) at $(n,m)=(2,2)$ ($\theta\Lambda_2^{-1}=\frac{1}{8}$, $H_{\rm full}(a\prec b)=\frac{19}{22}$) gives active history probabilities $\mathbb P_{r_a,\rho_2}(h)=P_{r_a}^{\rm pass}(h)[1+\frac{1}{8}(H_{\rm full}(E_h)-\frac{19}{22})\operatorname{Tr}(X\rho_2)]$. Over the 15 structural rows above $(a\prec b,(r_a,0))$ tabulated in Section 4.1 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#41-complete-15-row--60-marked-history-active-two-way-ledger) (with common passive denominator $1{,}320$ for both $r_a\in\{0,1\}$), the nonzero-$v(E)$ rows are Row 2 ($E_{\text{2-edges}}$, weight $6$, $H_{\rm full}=0$, $v=-\frac{654}{193}$), Row 6 ($E_{\text{asym-join}}$, weight $195$, $H_{\rm full}=\frac{44}{65}$, $v=+\frac{1{,}420}{193}$), Rows 8 & 14 ($E_{\text{3-claw}},E_{\text{upper-fork}}$, combined weight $24$ for both $r_a\in\{0,1\}$, $H_{\rm full}=0$, $v=+\frac{4{,}191}{193}$), and Rows 9, 10, 11, 13, 15 ($E_{\text{asym-fork}},E_{\text{diamond}},E_{\text{4-chain}}$, combined weight $1{,}008$ for both $r_a\in\{0,1\}$, $H_{\rm full}=1$, $v=+\frac{274{,}835}{8{,}106}$, where $\frac{1{,}008}{8{,}106}=\frac{24}{193}$). First, the passive mean equals
   $$
   \mathbb E_{r_a}^{\rm pass}[v(P_4)]=\frac{6(-654)+195(1{,}420)+24(4{,}191+274{,}835)}{1{,}320\cdot 193}=\frac{-3{,}924+276{,}900+6{,}696{,}624}{1{,}320\cdot 193}=\frac{6{,}969{,}600}{1{,}320\cdot 193}=+\frac{5{,}280}{193}=v(a\prec b).
   $$
   Second, using $195(\frac{44}{65}-\frac{19}{22})=-\frac{801}{22}$ and $1{,}008(1-\frac{19}{22})=+\frac{3{,}024}{22}$ (with $\frac{3{,}024}{8{,}106}=\frac{72}{193}$), the active slope in $\operatorname{Tr}[X\rho_2]$ is
   $$
   \frac{1}{8\cdot 1{,}320\cdot 22}\cdot\frac{6(-19)(-654)-801(1{,}420)-456(4{,}191)+72(274{,}835)}{193}
   =\frac{74{,}556-1{,}137{,}420-1{,}911{,}096+19{,}788{,}120}{232{,}320\cdot 193}
   =\frac{16{,}814{,}160}{232{,}320\cdot 193}
   =\frac{87{,}120}{232{,}320}
   =\frac{3}{8},
   $$
   confirming (33) independently directly from the 25-poset ledger.
4. Summing (26) at $(n,m)=(2,2)$ ($\frac{\Lambda_4}{\Lambda_2}=\frac{1}{4}$, $1-\frac{\Lambda_4}{\Lambda_2}=\frac{3}{4}$, $\Sigma_2=X$) over all $60$ marked continuations $h$ from $(a\prec b,(r_a,0))$ cancels $\sum_h P_{r_a}^{\rm pass}(h)(H_{\rm full}(E_h)-H_{\rm full}(a\prec b))=0$ by backward harmonicity of $H_{\rm full}$, leaving the exact unselected channel
   $$
   \mathcal E_{r_a}(\rho_2)=\frac{3}{4}\operatorname{Tr}(\rho_2)\frac{I_Q}{2}+\frac{1}{4}U_*^2\left(\sum_{k=0}^2\nu_{r_a}(k)\,e^{-i\frac{k\varphi_0}{2}X}\rho_2\,e^{+i\frac{k\varphi_0}{2}X}\right)(U_*^\dagger)^2,
   $$
   where $\nu_{r_a}(k)=\sum_{h:\Phi_h=k\varphi_0}P_{r_a}^{\rm pass}(h)$ depends solely on Part A's unchanged passive kernel and therefore takes the exact values established in Section 4.2.B of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#b-backward-ordermark---quantum-response-and-single-state-pythagorean-witness): $(\frac{4{,}781}{5{,}280},\frac{247}{2{,}640},\frac{1}{1{,}056})$ for $r_a=0$ and $(\frac{879}{880},\frac{1}{880},0)$ for $r_a=1$. Because $\operatorname{Tr}(YI_Q)=0$ and $U_*^2=-U_*^\dagger$ gives $(U_*^\dagger)^2YU_*^2=U_*YU_*^\dagger=Z$, while $XZ=-iY$ gives
   $$
   e^{+i\frac{\alpha}{2}X}Ze^{-i\frac{\alpha}{2}X}=(\cos\alpha\,I_Q+i\sin\alpha\,X)Z=\cos\alpha\,Z+\sin\alpha\,Y,
   $$
   taking $\operatorname{Tr}[Y\,\mathcal E_{r_a}(\rho_2)]$ yields (34). Setting $\varphi_0=\frac{\pi}{2}$ gives $\mathbb E_{\rho_2,r_a}[\operatorname{Tr}(Y\rho_4)]=\frac{1}{4}[(\nu_{r_a}(0)-\nu_{r_a}(2))\operatorname{Tr}(Z\rho_2)+\nu_{r_a}(1)\operatorname{Tr}(Y\rho_2)]$. Subtracting $r_a=1$ from $r_a=0$ uses $(\frac{4{,}781-5}{5{,}280})-\frac{5{,}274}{5{,}280}=-\frac{498}{5{,}280}=-\frac{83}{880}$ and $\frac{494-6}{5{,}280}=+\frac{488}{5{,}280}=+\frac{61}{660}$ to yield (35). On $|\psi_{3,4}\rangle$ ($(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)=(\frac{3}{5},0,\frac{4}{5})$), $\mathcal C(a\prec b,|\psi_{3,4}\rangle)=E_0+(\frac{5{,}280}{193}+\frac{3}{10})\varepsilon=E_0+\frac{53{,}379}{1{,}930}\varepsilon$, $\frac{3\varepsilon}{8}\langle X\rangle=+\frac{9\varepsilon}{40}$, and (35) equals $-\frac{83}{3{,}520}\cdot\frac{4}{5}=-\frac{83}{4{,}400}\ne 0$. Notice structurally *why* this phase signal carries zero energy cost: at birth $4$, $H_4=E_0I_Q+\frac{\varepsilon}{2}Z$ depends only on $\operatorname{Tr}[Z\rho_4]$, whereas precursor-local phases rotate the state in the transverse Bloch plane $\operatorname{span}\{X,Y\}$ orthogonal to $Z$. $\blacksquare$

---

### 4.2 Imperfect-detector $L^1$ discrimination bounds and explicit null controls

Adopt verbatim the faulty three-outcome detector model summarized in Section 4.3 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#43-shared-imperfect-detector-lower-bounds-and-empty-start-complete-trial-check): any binary native event $B\in\{0,1\}$ passes through a shared erasure-and-confusion channel $\xi=(f,n,e_{\rm det})\in\mathcal C:=[f_-,f_+]\times[n_-,n_+]\times[e_-,e_+]\subseteq[0,1]^3$ ($e_+<1$, $f_++n_+<1$), outputting $(0,1,\perp)$ with probabilities $((1-e_{\rm det})(1-f),(1-e_{\rm det})f,e_{\rm det})$ when $B=0$ and $((1-e_{\rm det})n,(1-e_{\rm det})(1-n),e_{\rm det})$ when $B=1$. By Proposition 1 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#43-shared-imperfect-detector-lower-bounds-and-empty-start-complete-trial-check), any two preparations inducing native contrast $\Delta=\mathbb P_+(B=1)-\mathbb P_-(B=1)$ satisfy the uniform reported-law $L^1$ lower bound
$$
\inf_{\xi\in\mathcal C}\bigl\|\mu_+(\xi)-\mu_-(\xi)\bigr\|_1=2|\Delta|(1-e_+)(1-f_+-n_+).
\tag{36}
$$

**Proposition 1 (Faulty-detector $L^1$ lower bounds for geometric potential sign and mark-to-qubit phase back-action).** *Fix $(H_{\rm full},\lambda_0=1,\lambda_{1,2,3}=\frac{1}{2},\theta=\frac{1}{16},\varphi_0=\frac{\pi}{2})$ and any informative uncertainty box $\mathcal C$ ($e_+<1$, $f_++n_+<1$).*

1. *(Prepared $a\prec b$ positive-geometric-potential indicator $B_{\rm pos}(E):=\mathbf 1_{\{V_{\rm geom}(E)>0\}}$ on $|+\rangle$ vs. $|-\rangle$.)* *Across $\mathcal U_4$, $B_{\rm pos}(E)=1$ holds on $\{E_{\text{asym-join}},E_{\text{3-claw}},E_{\text{upper-fork}},E_{\text{asym-fork}},E_{\text{diamond}},E_{\text{4-chain}}\}$. Above $(a\prec b,(r_a,0))$ ($r_a\in\{0,1\}$), its native contrast between $\rho_+=|+\rangle\langle+|$ and $\rho_-=|-\rangle\langle-|$ is $\Delta_{\pm}(B_{\rm pos})=+\frac{589}{38{,}720}>0$, yielding*
   $$
   \inf_{\xi\in\mathcal C}\bigl\|\mu_{r_a,|+\rangle}^{B_{\rm pos}}(\xi)-\mu_{r_a,|-\rangle}^{B_{\rm pos}}(\xi)\bigr\|_1
   =\frac{589}{19{,}360}(1-e_+)(1-f_+-n_+)>0\qquad (r_a\in\{0,1\}).
   \tag{37}
   $$
2. *(Empty-start maximum-geometric-potential indicator $B_{\rm top}(E):=\mathbf 1_{\{V_{\rm geom}(E)=\frac{274{,}835}{8{,}106}\varepsilon\}}$ on $|+_Y\rangle$ vs. $|-_Y\rangle$.)* *From $P_0=\varnothing$, comparing $\rho_0=|\pm_Y\rangle\langle\pm_Y|$ ($\Delta\langle Y\rangle=+2$) gives native contrast $\Delta_{\varnothing}(B_{\rm top})=+\frac{1{,}981}{145{,}200}>0$ and*
   $$
   \inf_{\xi\in\mathcal C}\bigl\|\mu_{\varnothing,|+_Y\rangle}^{B_{\rm top}}(\xi)-\mu_{\varnothing,|-_Y\rangle}^{B_{\rm top}}(\xi)\bigr\|_1
   =\frac{1{,}981}{72{,}600}(1-e_+)(1-f_+-n_+)>0.
   \tag{38}
   $$
3. *(Isoenergetic `Order/Mark -> Quantum` terminal $Y$-basis readout $B_Y$ on $r_a=0$ vs. $r_a=1$.)* *Let $B_Y\in\{0,1\}$ be the outcome of a terminal projective measurement in the eigenbasis $\{|-_Y\rangle,|+_Y\rangle\}$ of $Y$ at birth $4$ ($\mathbb P_{\rho_2,r_a}(B_Y=1)=\frac{1}{2}(1+\mathbb E_{\rho_2,r_a}[\operatorname{Tr}(Y\rho_4)])$). On $\rho_2=|\psi_{3,4}\rangle\langle\psi_{3,4}|$ (at identical conserved energy $E_0+\frac{53{,}379}{1{,}930}\varepsilon$), $\Delta_{r_a}\mathbb P(B_Y=1)=-\frac{83}{8{,}800}\ne 0$, and on $\rho_2=|+_Y\rangle\langle+_Y|$ (at identical conserved energy $E_0+\frac{5{,}280}{193}\varepsilon$), $\Delta_{r_a}\mathbb P(B_Y=1)=+\frac{61}{5{,}280}\ne 0$, yielding*
   $$
   \inf_{\xi\in\mathcal C}\bigl\|\mu_{|\psi_{3,4}\rangle,0}^{B_Y}(\xi)-\mu_{|\psi_{3,4}\rangle,1}^{B_Y}(\xi)\bigr\|_1=\frac{83}{4{,}400}(1-e_+)(1-f_+-n_+)>0,
   $$
   $$
   \inf_{\xi\in\mathcal C}\bigl\|\mu_{|+_Y\rangle,0}^{B_Y}(\xi)-\mu_{|+_Y\rangle,1}^{B_Y}(\xi)\bigr\|_1=\frac{61}{2{,}640}(1-e_+)(1-f_+-n_+)>0.
   \tag{39}
   $$

**Proof.**
1. Above $(a\prec b,(r_a,0))$, the complement $\{B_{\rm pos}=0\}$ consists of Rows 1, 2, 3, 4, 5, 7, 12, whose passive weights sum to $6+6+5+19+33+5+19=93$ ($r_a=0$) and $6+6+10+14+33+10+14=93$ ($r_a=1$) over $1{,}320$, all carrying $H_{\rm full}(E)=0$. With $\theta\Lambda_2^{-1}\Delta\langle X\rangle=\frac{1}{8}\cdot 2=\frac{1}{4}$ and $H_{\rm full}(a\prec b)=\frac{19}{22}$, $\Delta_{\pm}(B_{\rm pos}=0)=\frac{93}{1{,}320}\cdot\frac{1}{4}(0-\frac{19}{22})=-\frac{31}{440}\cdot\frac{19}{88}=-\frac{589}{38{,}720}$, so $\Delta_{\pm}(B_{\rm pos}=1)=+\frac{589}{38{,}720}$. Applying (36) multiplies by $2$ and gives (37).
2. From $P_0=\varnothing$, $B_{\rm top}=1$ holds on $\{E_{\text{asym-fork}},E_{\text{diamond}},E_{\text{4-chain}}\}$, which has passive empty-start probability $1\cdot\frac{1}{3}\cdot\frac{4}{5}\cdot\frac{21}{22}=\frac{14}{55}$ and $H_{\rm full}(E)=1$ throughout. Since $H_{\rm full}(\varnothing)=\frac{377}{660}$ and $\theta\Lambda_0^{-1}\Delta\langle Y\rangle=\frac{1}{16}\cdot 2=\frac{1}{8}$, $\Delta_{\varnothing}(B_{\rm top})=\frac{1}{8}\cdot\frac{14}{55}(1-\frac{377}{660})=\frac{1}{8}\cdot\frac{14\cdot 283}{55\cdot 660}=\frac{1{,}981}{145{,}200}>0$, and (36) gives (38).
3. Because $\mathbb P_{\rho_2,r_a}(B_Y=1)=\frac{1}{2}+\frac{1}{2}\mathbb E_{\rho_2,r_a}[\operatorname{Tr}(Y\rho_4)]$, subtracting $r_a=1$ from $r_a=0$ gives $\Delta_{r_a}\mathbb P(B_Y=1)=\frac{1}{2}\Delta_{r_a}\mathbb E[\operatorname{Tr}(Y\rho_4)]$, which equals $-\frac{83}{8{,}800}$ on $|\psi_{3,4}\rangle$ and $+\frac{61}{5{,}280}$ on $|+_Y\rangle$ by (35); multiplying $|\Delta|$ by $2$ in (36) yields (39). $\blacksquare$

*Explicit null controls:*
1. **Maximally mixed state ($\rho_0=\frac{1}{2}I_Q$ or $\rho_2=\frac{1}{2}I_Q$):** Here $\operatorname{Tr}[\Sigma_n\rho_n]=0$, so $\mathbb E_{I_Q/2}[V_{\rm geom}(P_4)]=0$ from $\varnothing$, $\mathbb E_{I_Q/2,r}[V_{\rm geom}(P_4)-V_{\rm geom}(a\prec b)]=0$ above $a\prec b$, and $\Delta_{r_a}\mathbb E[\operatorname{Tr}(Y\rho_4)]=0$, recovering Part A's passive structural law with zero net quantum-to-geometry exchange.
2. **Phase-free active control ($\varphi_0=0$):** Setting $\varphi_0=0$ leaves every value of $H_{\rm full}$, $r_P(S)$, $V_{\rm geom}(P)$, (32)–(33), and (37)–(38) completely unchanged while collapsing $\Delta_{r_a}\mathbb E[\operatorname{Tr}(Y\rho_4)]$ in (34) identically to $0$ ($\sum_{k=0}^2\nu_{r_a}(k)=1$).
3. **Unitary-limit control ($\theta\to 0$ with $\lambda_n\equiv 1$):** At $\lambda_n\equiv 1$ and $r_P\equiv 0$, $1-\lambda_n=0$ gives $V_{\rm geom}\equiv 0$, conserving $\operatorname{Tr}[H_n\rho_n]=\operatorname{Tr}[H_0\rho_0]$ purely inside the qubit sector with zero backreaction on order.
4. **Uninformative detector boundary ($e_{\rm det}=1$ or $f+n=1$):** Every $L^1$ distance in (37)–(39) vanishes identically when $e_+=1$ or $f_++n_+=1$.

---

## 5. Scope, non-implications, and Status-M quarantine

### 5.1 Prefix-dependent similarity gauge vs. operational fixed-interface conservation

Just as in Section 5.2 of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md#52-prefix-dependent-algebraic-similarity--gauge-analysis), setting $\alpha_P:=\theta\Lambda_{|P|}^{-1}(H_{\rm full}(P)-H_{\rm full}(\varnothing))$ ($0\le|P|\le 4$) defines invertible linear maps $\mathcal S_P(A):=A+\frac{1}{2}\alpha_P\operatorname{Tr}(\Sigma_{|P|}A)I_Q$ intertwining the $\theta=0$ retention-$\lambda_{|P|}$ channel with $\mathcal B^{P,r}_{S,b}$ via $\mathcal S_{P+S}\circ\mathcal B^{P,r;\theta=0}_{S,b}\circ\mathcal S_P^{-1}=\mathcal B^{P,r}_{S,b}$ (since $\lambda_n\alpha_{P+S}-\alpha_P=\theta\Lambda_n^{-1}(H_{\rm full}(P+S)-H_{\rm full}(P))=r_P(S)$). As proved there, whenever $\alpha_P\ne 0$ (e.g., $\alpha_{C_2}=\frac{1}{8}(\frac{19}{22}-\frac{377}{660})=+\frac{193}{5{,}280}\ne 0$), $\mathcal S_P$ is prefix-dependent, non-trace-preserving ($\mathcal S_P^\dagger(I_Q)=I_Q+\alpha_P\Sigma_{|P|}\ne I_Q$), and non-positive on $\mathcal D(\mathbb C^2)$. Fixing the operational density-matrix state space $\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, unit trace normalization $I_Q$, and bounded stage observable $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ across prefixes makes the conservation law (30) and exchange laws (32)–(33) operationally well-defined on that fixed interface, without excluding larger-environment Stinespring dilations.

### 5.2 Strict separation of native vs. externally supplied ingredients

- **Supplied by the admitted four-birth native structural law ([Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix)):** Binary-marked finite strict partial orders through four births ($25$ unmarked poset classes across sizes $0\le|P|\le 4$), downward-closed precursor ideals $S\in\mathcal I(P)$, append-only maximal births $P+S$, immutable fair newborn marks, and the positive seed kernel $q(P,r,S)>0$ with its all-mark scalar diamond identities.
- **Externally supplied mathematical structures and model choices:** The qubit Hilbert space $\mathcal H_Q=\mathbb C^2$ and passive reference $\mathcal H_{\rm ref}$, Pauli operators and Clifford co-rotation $U_*$, the bounded Hamiltonian family $H_n=E_0I_Q+\frac{\varepsilon}{2}\Sigma_n$ with external energy scale $\varepsilon>0$ and offset $E_0\in\mathbb R$, the retention schedule $(\lambda_0,\lambda_1,\lambda_2,\lambda_3)=(1,\frac{1}{2},\frac{1}{2},\frac{1}{2})$, the harmonic potential $H_{\rm full}$ and coupling $\theta=\frac{1}{16}$, the precursor-local phase schedule $\varphi_{K,b}$ (and $\varphi_0=\frac{\pi}{2}$), the selected shared-poset zeros fixing the canonical rational representative $V_{\rm geom}$ inside the affine solution space, the trace probability postulate, and the shared three-outcome erasure-and-confusion detector box $\mathcal C$.

### 5.3 Non-implications and Status-M quarantine

1. **Strict Status-M quarantine:** All Status-M ontological commitments in `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, and `FALSIFICATION_LEDGER.md` remain strictly quarantined outside every definition, theorem, equation, and inference in this manuscript.
2. **Finite four-birth scope and affine non-uniqueness of $V_{\rm geom}$:** Theorems 4–6 are proved strictly over the four-birth domain ($0\le|P|\le 4$). Within that domain, $V_{\rm geom}$ is an explicit rational mark-independent member of a higher-dimensional affine solution family (setting the five shared non-private size-$4$ classes to $0$); it is not claimed to be the unique global potential, nor extended here to all-horizon infinite growth.
3. **Conditional-mean vs. pathwise conservation:** By Theorem 2, $\mathcal C(P,\rho)$ is conserved in exact conditional mean (martingale expectation) across histories, and **cannot** be conserved state-independently along single selective branches whenever $\lambda_n<1$ or $r_P(S)\ne 0$.
4. **No derivation of physical energy, mass, Born's rule, clocks, continuum geometry, or General Relativity:** Calling $H_n$ a bounded two-level Hamiltonian and $V_{\rm geom}(P)$ a geometric potential refers solely to their mathematical roles in the exact conserved functional $\mathcal C(P,\rho)=V_{\rm geom}(P)+\operatorname{Tr}[H_{|P|}\rho]$; the scale $\varepsilon>0$ carries no derived physical units (Joules or kilograms), and no correspondence with physical stress-energy tensors, proper-time clocks, Born-rule genesis, continuum Lorentzian manifolds, or Einstein's field equations is claimed.

## Scientific review

Record-Compensated Quantum Conservation Author derived the retention-$\lambda_n$ co-rotating five-Kraus instrument adjoint and $4\times 4$ Choi spectrum, master necessary-and-sufficient linear system and POVM effect-rank criterion for state-independent entangled conditional-mean conservation of $\mathcal C(P,r,\rho)=V(P,r)+\operatorname{Tr}[H_{|P|}\rho]$ across $\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, canonical minimum-variance compensation potential, selective pathwise no-go theorem, multi-birth reachability obstruction for sparse causal focusing $H_{\rm foc}$ at `edge+iso`, globally active four-birth harmonic potential $H_{\rm full}$ with unitary step-$0$ retention ($\lambda_0=1$, $\lambda_1=\lambda_2=\lambda_3=\frac{1}{2}$, $\max|r_P(S)|=\frac{21}{88}<\frac{1}{2}$) and entangled diamond commutation, constructive 25-poset mark-independent diamond-confluent geometric potential $V_{\rm geom}(P)$, path-independent martingale conservation and exact $\frac{7\varepsilon}{16}\operatorname{Tr}[Y\rho_0]$ and $\frac{3\varepsilon}{8}\operatorname{Tr}[X\rho_2]$ quantum-to-geometric conversion laws, isoenergetic transverse phase contrast, imperfect-detector $L^1$ lower bounds, null controls, and prefix-dependent similarity gauge analysis. Independent Quantum Conservation Reviewer independently verified all Clifford and adjoint identities, Kraus sums and Choi eigenvalues, operator-span conservation equations, pathwise no-go and reachability obstructions, all 16 size-four and 9 ancestor values of $H_{\rm full}$ and positive drift variances, all 25 rational values of $V_{\rm geom}(P)$ across every marking, the 15-row active $a\prec b$ conversion ledger, transverse phase contrasts, detector bounds, controls, similarity maps, relative links, and Status-M quarantine boundaries. Prospective protocol SHA-256 06ea263e04785180d9642c2e691fb46be85de712e9e76519a827e6cf6151ce21; accepted author report SHA-256 9344563ed42f0ae86edfb0f064c87e8e22134a24be4a1fca0557d4c21c783414; independent scientific review SHA-256 fbcdf8fb7a1df7c8afa820926fe3c706108261d9d511667b155730ad93be6d9d.
