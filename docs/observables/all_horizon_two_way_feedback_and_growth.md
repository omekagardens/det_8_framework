# All-horizon sequential growth, five-birth causal focusing, and projective two-way quantum-order feedback

**Decision.** Extending the admitted four-birth structural prefix of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix) directly by elementary induction on parent cardinality $n=|P|\ge 4$, the maximal-deletion ansatz $q(P,r,S)=a_n u(P,r,S)$ ($S\subsetneq P$) and $q(P,r,P)=1-a_n\sum_{S\subsetneq P}u(P,r,S)$ defines a self-contained, strictly positive, relabeling-equivariant, proper-slot mark-local, scalar diamond-commuting, and Kolmogorov cylinder-set projective sequential growth law across all finite and countably infinite horizons (`NG-02` of the [native geometry, gravity and measurement plan](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md)) for every positive scale schedule $0<a_n<1/M_n$, without external numerical certificates. At parent size $n=4$, an exact audit across all $16$ unmarked four-poset classes $\mathcal U_4$ proves $M_4<4$ (attained on $A_4$ with $\frac{16}{5}+\frac{3}{110}+\frac{4}{3993}+\frac{256}{1185921}<4$), so $a_4=\frac{1}{10}$ yields $q(P,r,P)>\frac{3}{5}$ everywhere. Generalizing the co-rotating Clifford five-Kraus qubit instrument of [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md) (`NW1-A`) to an arbitrary retention schedule $(\lambda_n)_{n\ge 0}\subset(0,1]$ ($\Lambda_n=\prod_{j=0}^{n-1}\lambda_j$), we prove strict complete positivity if and only if $|r_P(S)|<1-\lambda_n$ and construct an exact nonnegative six-class five-birth harmonic continuation $H_{\rm foc}^{(5)}:\mathcal U_5\to\bigl[0,\frac{13640}{11699}\bigr]$ across all $63$ unmarked five-posets that cancels root-mark contrasts on both $E_{\text{asym-fork}}$ and $E_{\text{diamond}}$, satisfies $|r_P(S)|\le\frac{1}{2}<\frac{3}{4}=1-\lambda_4$ at $\lambda_4=\frac{1}{4}$, recovers `NW1-A` identically upon marginalizing the fifth birth (in sharp contrast to the stopping-horizon failure of terminal exponential interval-action weighting in [interval action and stopping horizon](interval_action_and_stopping_horizon.md)), and produces exact rational step-5 Pauli contrasts in chain continuation ($+\frac{1}{20}\operatorname{Tr}[Z\rho]$ on $C_4$) and Benincasa–Dowker interval action ($-\frac{2{,}785{,}889}{77{,}213{,}400}\operatorname{Tr}[Z\rho]$ on $E_{\text{diamond}}$ at $r_{v_0}=0$). Conversely, as $N\to\infty$, we prove an **infinite-horizon obstruction**: for any nonzero coupling $\theta>0$ and any retention schedule $(\lambda_n)\subset(0,1)$ over full ideal support, strict complete positivity forces $\sum_{n=0}^\infty\Delta_n(H)\le\frac{1}{\theta}<\infty$ and $\liminf_{n\to\infty}n\,\Delta_n(H)=0$, which combined with a $4(n-1)\Delta_n(H)$ up-down bridge diameter bound on $\mathcal U_n$ collapses every all-horizon forward harmonic potential to a constant ($r_P(S)\equiv 0$). We resolve this obstruction constructively via an explicit all-horizon ($0\le n<\infty$ and $N\to\infty$) Kolmogorov-projective coherent quantum-order instrument built from operator-valued superpositions of distinct admitted structural kernels $(q^{(+)},q^{(-)})$ (with optional non-abelian Clifford synthesis on $\mathbb C^2_{\rm Cliff}\otimes\mathbb C^2_{\rm hor}$), prove an exact `NG-02` asymptotic width dichotomy between summable maximal-deletion schedules ($\sum_{n=4}^\infty a_n M_n<\infty$, which freeze almost surely into bounded-width ordinal chain tails $P_{N_*}\oplus C_{N-N_*}$) and the [Bernoulli transitive-percolation sector](../track_b/native_theorem_package_v1/BERNOULLI_ORDER_LIKELIHOOD.md) ($0<p_-<p_+<1$, whose width diverges almost surely at every $k\ge 2$ with persistent quantum coherence steering), and establish uniform imperfect-detector $L^1$ lower bounds. Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## Context and architecture

Under the [foundational research scope](../coordination/FOUNDATIONAL_RESEARCH_SCOPE.md), the [native geometry, gravity and measurement plan](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md) (`NG-01` and `NG-02`), and the [native mass/gravity mapping](../coordination/NATIVE_MASS_MAPPING.md), advancing discrete quantum-and-order feedback beyond the four-birth prefix confronts three structural mathematical questions:

1. **Horizon-independent sequential consistency beyond four births (`NG-02`):** In [interval action and stopping horizon](interval_action_and_stopping_horizon.md), reweighting fixed-size histories by terminal Benincasa–Dowker action $Q_n(H_n)\propto P_n(H_n)e^{-\lambda S_n(H_n)}$ was proved to violate prefix marginal consistency between $n=3$ and $n=4$ for every $\lambda\ne 0$: the marginal distribution on recorded three-birth prefixes depends on the chosen future stopping horizon. By contrast, [native two-way quantum-and-order feedback](native_two_way_quantum_order_feedback.md) (`NW1-A`) achieved exact sequential trace preservation and non-abelian diamond commutation, but strictly within the fixed four-birth seed domain $|P|\in\{0,1,2,3\}$ of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix). Extending sequential growth to five births and to arbitrary finite or countably infinite horizons requires a self-contained all-horizon proof of the maximal-deletion extension and its Kolmogorov prefix marginalization without relying on external computational certificates.
2. **Five-birth continuation vs. infinite-horizon harmonic telescoping:** `NW1-A` coupled qubit expectations $\operatorname{Tr}(\Sigma_{|P|}\rho)$ into causal-order growth through linear telescoping of a mark-independent harmonic potential $H_{\rm foc}$ inside a constant-retention ($\lambda=\frac{1}{2}$) five-Kraus reset channel. Whether `NW1-A` extends intact to five births ($|P|=4\to 5$, $|\mathcal U_5|=63$ unmarked classes) with exact `5 -> 4` prefix consistency—and whether *any* retention schedule $(\lambda_n)_{n\ge 0}\subset(0,1)$ can sustain global linear harmonic telescoping to $N\to\infty$ over full ideal support—must be settled by exact analysis rather than extrapolation.
3. **All-horizon projective two-way feedback and asymptotic poset width (`NG-02`):** If global linear harmonic telescoping encounters an asymptotic complete-positivity barrier as $N\to\infty$, can an exact CPTP quantum-and-order instrument nevertheless sustain genuine bidirectional (`Quantum -> Order` and `Order/Mark -> Quantum`) feedback, full entangled diamond commutation, and Kolmogorov projective consistency across all horizons $N\ge 1$ to $\infty$? And under `NG-02`'s chain/port-width audit, which all-horizon structural kernels freeze into finite-width ordinal chains versus sustaining unbounded antichain width as $N\to\infty$?

Sections 1–5 resolve all three questions completely from first principles.

---

## 1. Self-contained all-horizon structural extension and explicit parent-four bound

### 1.1 Recursive maximal-deletion extension and first-principles diamond proof

Retain verbatim on parent sizes $|P|\in\{0,1,2,3\}$ the binary-marked finite strict partial order domain $(P,\prec,r)$ ($r:P\to\{0,1\}$) and strictly positive structural seed kernel $q(P,r,S)>0$ of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), with seed parameters
$$
a_{\rm seed}=\frac{2}{3},\quad c_{\rm seed}=\frac{1}{5},\quad d_{\rm seed}=\frac{1}{4},\quad (f_0,h_0)=\left(\frac{1}{6},\frac{19}{30}\right),\quad (f_1,h_1)=\left(\frac{1}{3},\frac{7}{15}\right),
$$
$$
g_{\rm seed}=\frac{1}{10},\quad k_{\rm seed}=\frac{11}{20},\quad e=\frac{1}{44}.
\tag{1}
$$
Recall that for any downward-closed subset (ideal) $S\subseteq P$, $P+S$ (or $P+x_S$ when naming the newborn vertex $x$) denotes the $(|P|+1)$-element strict partial order obtained by adjoining one maximal vertex $x$ with strict past $\{u\in P:u\prec x\}=S$, while $r+b_x$ extends $r$ by $r(x)=b\in\{0,1\}$. On $|P|\in\{0,1,2,3\}$, $q(P,r,S)>0$, $\sum_{S\subseteq P}q(P,r,S)=1$, $q(P,r,S)$ reads $r$ solely through $r|_S$ whenever $S\subsetneq P$, $q$ is equivariant under order-and-mark isomorphisms, and for every base $(C,r)$ of size $|C|\in\{0,1,2\}$, all ideals $S,T\subseteq C$, and all newborn bits $b,c\in\{0,1\}$, Part A establishes the exact scalar diamond identity
$$
q(C,r,S)\,q(C+x_S,r+b_x,T)=q(C,r,T)\,q(C+y_T,r+c_y,S).
\tag{2}
$$
For $|P|=n\ge 4$ and any proper ideal $S\subsetneq P$, let $\operatorname{Max}(P):=\{m\in P:\nexists z\in P\text{ with }m\prec z\}$ and put $M:=\operatorname{Max}(P)\setminus S$. Following Eq. (3) of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), define recursively the maximal-deletion potential
$$
u(P,r,S):=\prod_{\varnothing\ne A\subseteq M}q\bigl(P\setminus A,\,r|_{P\setminus A},\,S\bigr)^{(-1)^{|A|+1}}.
\tag{3}
$$

**Theorem 1 (First-principles maximal-deletion all-horizon extension and Kolmogorov consistency).** *Proceeding recursively on parent cardinality $n=|P|\ge 4$, suppose $q$ is already defined on all marked orders of sizes $0,1,\dots,n-1$ satisfying strict positivity, complete-row normalization, proper-slot mark locality, relabeling equivariance, and the scalar diamond identity (2) on all bases of sizes $\le n-2$. Then:*

1. *(Well-definedness, strict positivity, and proper-slot mark locality of $u$.)* *For every marked order $(P,r)$ of size $|P|=n\ge 4$ and every proper ideal $S\subsetneq P$, the set $M=\operatorname{Max}(P)\setminus S$ is nonempty, every factor in (3) is evaluated at an admissible ideal $S\subseteq P\setminus A$ of a parent of size $n-|A|\le n-1$, $u(P,r,S)>0$ is well-defined and relabeling-equivariant, and $u(P,r,S)$ depends on $r$ solely through $r|_S$.*
2. *(Exact ratio-diamond symmetry.)* *For every marked base $(C,r)$ of size $|C|=n-1\ge 3$, every pair of ideals $S,T\subseteq C$ (including $S=T$, empty ideals, and $S=C$ or $T=C$), and all newborn bits $b,c\in\{0,1\}$, $T$ is a proper ideal of $C+x_S$, $S$ is a proper ideal of $C+y_T$, and*
   $$
   q(C,r,S)\,u(C+x_S,r+b_x,T)=q(C,r,T)\,u(C+y_T,r+c_y,S).
   \tag{4}
   $$
3. *(All-horizon admitted family and Kolmogorov projectivity `NG-02`.)* *Let $M_n:=\max_{|P|=n,\,r\in\{0,1\}^n}\sum_{S\subsetneq P}u(P,r,S)\in(0,\infty)$ (finite because $\mathcal U_n$ and $\{0,1\}^n$ are finite). For **any** sequence of scale parameters $(a_n)_{n\ge 4}$ satisfying $0<a_n<1/M_n$, defining*
   $$
   q(P,r,S):=a_n\,u(P,r,S)\quad (S\subsetneq P),\qquad
   q(P,r,P):=1-a_n\sum_{S\subsetneq P}u(P,r,S)
   \tag{5}
   $$
   *yields an all-horizon ($n\ge 0$) structural kernel satisfying strict positivity, complete-row normalization $\sum_{S\subseteq P}q(P,r,S)=1$, proper-slot mark locality, relabeling equivariance, and exact scalar diamond commutation (2) for all base sizes $|C|\ge 0$. Under independent fair newborn marks ($\frac{1}{2}q(P,r,S)$ per branch $(S,b)$), the resulting finite-horizon laws $(\mathbb P_N)_{N\ge 1}$ satisfy exact Kolmogorov cylinder-set prefix marginalization—marginalizing step $N+1$ over $(S_N,b_N)$ recovers $\mathbb P_N$ identically for every $N\ge 1$—and extend uniquely to a countably additive probability measure $\mathbb P_\infty$ on infinite marked growth histories.*

**Proof.** We establish Claims 1–3 simultaneously by induction on $n\ge 4$; for $n=4$, the inductive hypotheses on sizes $0,1,2,3$ and diamond bases $|C|\le 2$ hold verbatim from Part A.

1. Fix $|P|=n\ge 4$ and $S\subsetneq P$. Because $P\setminus S$ is finite and nonempty, it contains at least one element $m$ maximal in $P\setminus S$. No $z\in S$ can satisfy $m\prec z$, since downward closure of $S$ would force $m\in S$; hence $m\in\operatorname{Max}(P)\setminus S=M$, proving $M\ne\varnothing$. For every nonempty $A\subseteq M$, $A\cap S=\varnothing$ gives $S\subseteq P\setminus A$. If $u\in P\setminus A$ and $v\in S$ satisfy $u\prec v$, downward closure of $S$ in $P$ implies $u\in S\subseteq P\setminus A$, so $S$ is an ideal of $P\setminus A$. Since $|P\setminus A|=n-|A|\le n-1$, the inductive positivity hypothesis gives $q(P\setminus A,r|_{P\setminus A},S)>0$, whence $u(P,r,S)>0$. Equivariance under any order-and-mark isomorphism $\pi:(P,r)\xrightarrow{\sim}(P',r')$ follows immediately from $\operatorname{Max}(P')\setminus\pi(S)=\pi(M)$ and inductive equivariance of each factor. For mark locality on $S\subsetneq P$, examine each nonempty $A\subseteq M$:
   - If $S\subsetneq P\setminus A$ (which holds whenever $A\subsetneq M$, and also when $A=M$ if $P\setminus M\supsetneq S$), then $S$ is a *proper* ideal of $P\setminus A$, so by inductive proper-slot locality on size $n-|A|\le n-1$, $q(P\setminus A,r|_{P\setminus A},S)$ depends on $r|_{P\setminus A}$ solely through $(r|_{P\setminus A})|_S=r|_S$.
   - If $S=P\setminus A$, then since $A\subseteq M\subseteq P\setminus S$ we necessarily have $A=M$ and $P\setminus M=S$; in this full-slot factor on $P\setminus M$, the full induced marking $r|_{P\setminus M}$ is literally $r|_S$.
   Thus every factor in (3), and hence $u(P,r,S)$, reads $r$ solely through $r|_S$.

2. Fix $(C,r)$ with $|C|=n-1\ge 3$, ideals $S,T\subseteq C$, and bits $b,c\in\{0,1\}$. In $C+y_T$, the newborn vertex $y$ is maximal with strict past $T$ and $y\notin S$, so $S\subsetneq C+y_T$ is always proper (even when $S=C$). Likewise $T\subsetneq C+x_S$ is always proper. A vertex $v\in C$ remains maximal in $C+y_T$ if and only if $v\in\operatorname{Max}(C)\setminus T$ (since $v\prec y\iff v\in T$, and $y\not\prec v$). Hence $\operatorname{Max}(C+y_T)=\bigl(\operatorname{Max}(C)\setminus T\bigr)\sqcup\{y\}$, and removing $S\subseteq C$ yields the disjoint decomposition
   $$
   M_{T,S}:=\operatorname{Max}(C+y_T)\setminus S=W\sqcup\{y\},\qquad W:=\operatorname{Max}(C)\setminus(S\cup T),
   $$
   where $W$ is manifestly symmetric in $S$ and $T$. Partition the nonempty subsets $\varnothing\ne A\subseteq W\sqcup\{y\}$ into three disjoint classes:
   - **Singleton $A=\{y\}$ ($|A|=1$, $(-1)^{|A|+1}=+1$):** $(C+y_T)\setminus\{y\}=C$ with induced mark $r$, contributing $q(C,r,S)^{+1}$.
   - **Subsets $A=B\sqcup\{y\}$ with $\varnothing\ne B\subseteq W$ ($|A|=|B|+1$, $(-1)^{|A|+1}=(-1)^{|B|}$):** $(C+y_T)\setminus(B\sqcup\{y\})=C\setminus B$ with induced mark $r|_{C\setminus B}$, contributing $q(C\setminus B,r|_{C\setminus B},S)^{(-1)^{|B|}}$.
   - **Subsets $A=B$ with $\varnothing\ne B\subseteq W$ ($|A|=|B|$, $(-1)^{|A|+1}=(-1)^{|B|+1}$):** Since $B\subseteq\operatorname{Max}(C)$ and $B\cap T=\varnothing$, deleting $B$ from $C+y_T$ leaves $y$ maximal with unchanged strict past $T\subseteq C\setminus B$; thus $(C+y_T)\setminus B=(C\setminus B)+y_T$ with induced mark $r|_{C\setminus B}+c_y$, contributing $q\bigl((C\setminus B)+y_T,r|_{C\setminus B}+c_y,S\bigr)^{(-1)^{|B|+1}}$.

   Multiplying $u(C+y_T,r+c_y,S)$ by $q(C,r,T)>0$ and taking logarithms (all factors are strictly positive) gives
   $$
   \log\bigl[q(C,r,T)\,u(C+y_T,r+c_y,S)\bigr]
   =\log q(C,r,T)+\log q(C,r,S)+\sum_{\varnothing\ne B\subseteq W}(-1)^{|B|+1}\log\frac{q\bigl((C\setminus B)+y_T,\,r|_{C\setminus B}+c_y,\,S\bigr)}{q(C\setminus B,\,r|_{C\setminus B},\,S)}.
   $$
   For every $\varnothing\ne B\subseteq W$, set $C_B:=C\setminus B$ and $r_B:=r|_{C\setminus B}$. Because $B\subseteq\operatorname{Max}(C)$, both $S\subseteq C_B$ and $T\subseteq C_B$ remain downward-closed ideals of $C_B$, and $|C_B|=(n-1)-|B|\le n-2$. Multiplying numerator and denominator inside the logarithm by $q(C_B,r_B,T)>0$ yields
   $$
   \frac{q(C_B+y_T,\,r_B+c_y,\,S)}{q(C_B,\,r_B,\,S)}
   =\frac{q(C_B,r_B,T)\,q(C_B+y_T,r_B+c_y,S)}{q(C_B,r_B,S)\,q(C_B,r_B,T)}.
   \tag{6}
   $$
   By the inductive scalar diamond hypothesis on the smaller base $C_B$ ($|C_B|\le n-2$), the numerator of (6) satisfies $q(C_B,r_B,T)q(C_B+y_T,r_B+c_y,S)=q(C_B,r_B,S)q(C_B+x_S,r_B+b_x,T)$, while the denominator $q(C_B,r_B,S)q(C_B,r_B,T)$, the index set $W=\operatorname{Max}(C)\setminus(S\cup T)$, and the leading sum $\log q(C,r,T)+\log q(C,r,S)$ are all invariant under $(S,b_x)\leftrightarrow(T,c_y)$. Hence $\log[q(C,r,T)u(C+y_T,r+c_y,S)]=\log[q(C,r,S)u(C+x_S,r+b_x,T)]$; exponentiating proves (4).

3. Since $u(P,r,S)>0$ and every nonempty poset $P$ ($|P|=n\ge 4$) has at least the proper empty ideal $\varnothing\subsetneq P$, $0<M_n<\infty$. Choosing $0<a_n<1/M_n$ ensures $q(P,r,S)=a_n u(P,r,S)>0$ for all $S\subsetneq P$ and $q(P,r,P)=1-a_n\sum_{S\subsetneq P}u(P,r,S)\ge 1-a_n M_n>0$, with $\sum_{S\subseteq P}q(P,r,S)=1$. Proper-slot locality and equivariance inherit directly from Claim 1 (as $a_n$ depends only on $n=|P|$). Multiplying (4) by $a_n$ gives $q(C,r,S)q(C+x_S,r+b_x,T)=q(C,r,T)q(C+y_T,r+c_y,S)$ for all $|C|=n-1$, closing the induction for all $n\ge 4$. Finally, for any $N$-birth marked prefix history $h_N=((S_0,b_0),\dots,(S_{N-1},b_{N-1}))$ ending at $(P_N,r_N)$, summing the $(N+1)$-step law over all continuations $(S_N,b_N)\in\mathcal I(P_N)\times\{0,1\}$ gives
   $$
   \sum_{S_N\subseteq P_N}\sum_{b_N\in\{0,1\}}\mathbb P_{N+1}\bigl(h_N,(S_N,b_N)\bigr)
   =\mathbb P_N(h_N)\sum_{S_N\subseteq P_N}q(P_N,r_N,S_N)\sum_{b_N=0}^1\frac{1}{2}=\mathbb P_N(h_N),
   $$
   establishing exact prefix marginalization for all $N\ge 1$. Because at each step $N$ the pair $(S_N,b_N)$ takes values in the finite discrete space $2^{\{1,\dots,N\}}\times\{0,1\}$, the projective family $(\mathbb P_N)_{N\ge 1}$ on the compact product of finite discrete spaces extends uniquely by Kolmogorov's extension theorem to $\mathbb P_\infty$. $\blacksquare$

### 1.2 Unique-top identity and explicit parent-four bound $M_4<4$

To obtain concrete five-birth rational laws without computer search, we evaluate or bound $\Sigma_u(P,r):=\sum_{S\subsetneq P}u(P,r,S)$ analytically across all $|\mathcal U_4|=16$ unmarked four-element poset classes (using the class notation of `NW1-A` §1.2).

**Lemma 1 (Unique-top identity and explicit parent-four bound $M_4<4$).**
1. *(Unique-top identity.)* *For every marked poset $(P,r)$ of size $|P|\ge 4$ having a unique maximal vertex $\operatorname{Max}(P)=\{v_{\max}\}$ (equivalently, $P=Q\oplus A_1$ where $Q:=P\setminus\{v_{\max}\}$), the proper ideals of $P$ are precisely the ideals $S\subseteq Q$, and*
   $$
   u(P,r,S)=q(Q,r|_Q,S)\quad (\forall S\subsetneq P),\qquad \Sigma_u(P,r)=\sum_{S\subsetneq P}u(P,r,S)=1
   \tag{7}
   $$
   *identically for every marking $r$.*
2. *(Explicit parent-four maximum $M_4$.)* *Across all $16$ unmarked four-poset classes $P\in\mathcal U_4$ and all markings $r\in\{0,1\}^4$, the maximum $M_4=\max_{|P|=4,r}\Sigma_u(P,r)$ is attained uniquely on the four-antichain $A_4$, with exact rational value*
   $$
   M_4=\Sigma_u(A_4)=\frac{16}{5}+\frac{3}{110}+\frac{4}{3993}+\frac{256}{1185921}<4.
   \tag{8}
   $$
   *In particular, setting $a_4:=\frac{1}{10}<\frac{1}{2(1+M_4)}<\frac{1}{M_4}$ guarantees $q(P,r,S)>0$ for all $S\subseteq P$ and $q(P,r,P)=1-\frac{1}{10}\Sigma_u(P,r)>1-\frac{2}{5}=\frac{3}{5}$ on every marked four-poset.*

**Proof.**
1. If $P=Q\oplus A_1$ with top $v_{\max}$ ($q\prec v_{\max}$ for all $q\in Q$), any ideal $S\subseteq P$ containing $v_{\max}$ must contain all of $Q$ by downward closure, giving $S=P$. Conversely, every ideal $S\subseteq Q$ (including $S=Q$) excludes $v_{\max}$ and is downward-closed in $P$. Thus $\{S:S\subsetneq P\}=\{S:S\subseteq Q\}$. For every such $S$, $M=\operatorname{Max}(P)\setminus S=\{v_{\max}\}$ has $|M|=1$, so the product (3) reduces to its single nonempty subset $A=\{v_{\max}\}$, giving $u(P,r,S)=q(P\setminus\{v_{\max}\},r|_Q,S)^{+1}=q(Q,r|_Q,S)$ and $\sum_{S\subsetneq P}u(P,r,S)=\sum_{S\subseteq Q}q(Q,r|_Q,S)=1$.
2. Group the $16$ classes of $\mathcal U_4$ by $|\operatorname{Max}(P)|\in\{1,2,3,4\}$ and evaluate (3) from Part A's size-$0,1,2,3$ table (`NW1-A` §1.1):
   - **$|\operatorname{Max}(P)|=1$ ($5$ classes: $E_{\text{3-join}}$, $E_{\text{asym-join}}$, $E_{\text{lower-join}}$, $E_{\text{diamond}}$, $C_4$):** By Part 1, $\Sigma_u(P,r)=1$.
   - **$|\operatorname{Max}(P)|=2$ ($7$ classes, $\operatorname{Max}(P)=\{m_1,m_2\}$):** Ideals with $m_1\in S,m_2\notin S$ have $M=\{m_2\}$ and $u(P,r,S)=q(P\setminus\{m_2\},r|_{P\setminus\{m_2\}},S)$; symmetrically $m_2\in S,m_1\notin S$ gives $q(P\setminus\{m_1\},r|_{P\setminus\{m_1\}},S)$; ideals $S\subseteq P\setminus\{m_1,m_2\}$ have $M=\{m_1,m_2\}$ and $u(P,r,S)=\frac{q(P\setminus\{m_1\},r,S)\,q(P\setminus\{m_2\},r,S)}{q(P\setminus\{m_1,m_2\},r,S)}$. Explicitly:
     - $E_{\text{upper-fork}}$ ($r_*\prec u\prec m_1,m_2$, $i=r_{r_*}$): $5$ proper ideals give $2\cdot\frac{41}{44}+\frac{5}{1936}+\frac{1}{1936f_i}+\frac{1}{1936h_i}$, equal to $\frac{68{,}791}{36{,}784}$ ($i=0$) and $\frac{25{,}327}{13{,}552}$ ($i=1$), both $<2$.
     - $E_{\text{asym-fork}}=A_1\oplus(C_2\sqcup A_1)$ ($v_0\prec u\prec m_1,\ v_0\prec m_2$, $i=r_{v_0}$): Because $C_2\sqcup A_1$ has $3\times 2=6$ ideals, $E_{\text{asym-fork}}$ has **$6$ proper ideals**: $S_1=\varnothing$ ($u=\frac{5}{1936}$), $S_2=\{v_0\}$ ($u=\frac{1}{1936f_i}$), $S_3=\{v_0,u\}$ ($u=\frac{(h_i/(44f_i))(1/44)}{h_i}=\frac{1}{1936f_i}$), $S_4=\{v_0,m_2\}$ ($M=\{m_1\}$, $u=q(\text{fork},\{v_0,m_2\})=\frac{h_i}{44f_i}$), $S_5=\{v_0,u,m_1\}$ ($M=\{m_2\}$, $u=q(C_3,C_3)=\frac{41}{44}$), and $S_6=\{v_0,u,m_2\}$ ($M=\{m_1\}$, $u=q(\text{fork},\text{full})=\frac{21}{22}-\frac{h_i}{22f_i}$). Summing all six yields $\Sigma_u=\frac{17{,}509}{9{,}680}$ ($i=0$) and $\frac{18{,}007}{9{,}680}$ ($i=1$), both $<2$.
     - $E_{\text{3chain+iso}}$ ($u\prec v\prec m_1$, iso $m_2$): $7$ proper ideals give $\frac{41}{44}+\bigl(\frac{1}{44}+\frac{1}{8}+\frac{65}{88}\bigr)+3\cdot\frac{5}{1936}=\frac{20}{11}+\frac{15}{1936}=\frac{3{,}535}{1{,}936}<2$ (mark-independent, as $f_i$ and $h_i$ cancel in $\frac{(1/44)(5f_i/44)}{f_i}=\frac{(1/44)(5h_i/44)}{h_i}=\frac{5}{1936}$).
     - $E_{\text{crown}}=A_2\oplus A_2$: $6$ proper ideals give $2\cdot\frac{10}{11}+\frac{1}{484}+2\cdot\frac{5}{968}+\frac{5}{5{,}324}=\frac{9{,}751}{5{,}324}<2$.
     - $E_{\text{join+iso}}$ ($u_1,u_2\prec m_1$, iso $m_2$): $9$ proper ideals give $\frac{10}{11}+\bigl(\frac{1}{110}+\frac{2}{20}+\frac{4}{5}\bigr)+4\cdot\frac{1}{484}=\frac{20}{11}+\frac{1}{121}=\frac{221}{121}<2$.
     - $E_{\text{N-poset}}$ ($u_1\prec m_1,m_2,\ u_2\prec m_2$, $i=r_{u_1}$): $7$ proper ideals give $\frac{10}{11}+\bigl(\frac{5h_i}{44}+\frac{65}{88}\bigr)+\bigl(\frac{1}{484}+\frac{25f_i}{968}+\frac{5}{968}+\frac{5}{968}\bigr)$, equal to $\frac{10{,}085}{5{,}808}$ ($i=0$) and $\frac{625}{363}$ ($i=1$), both $<2$.
     - $E_{\text{2-edges}}=C_2\sqcup C_2$ (root marks $i_1,i_2$): $8$ proper ideals give $2\cdot\frac{65}{88}+\frac{5(h_{i_1}+h_{i_2})}{44}+\frac{1}{484}+\frac{25(f_{i_1}+f_{i_2})}{968}+\frac{5}{176}\le\frac{9{,}643}{5{,}808}<2$ (maximized at $i_1=i_2=0$).
   - **$|\operatorname{Max}(P)|=3$ ($3$ classes, $\operatorname{Max}(P)=\{m_1,m_2,m_3\}$):**
     - $E_{\text{edge+2iso}}=C_2\sqcup A_2$ ($u_1\prec m_1$, isos $m_2,m_3$, $i=r_{u_1}$): $|M|=1$ ideals sum to $\bigl(\frac{1}{20}+\frac{4}{5}\bigr)+2\cdot\frac{65}{88}=\frac{128}{55}$; $|M|=2$ ideals sum to $\frac{25h_i}{1936}+2\bigl(\frac{1}{484}+\frac{1}{88}\bigr)=\frac{25h_i}{1936}+\frac{13}{484}<\frac{1}{100}+\frac{13}{484}$; $|M|=3$ ideals ($\varnothing,\{u_1\}$) equal $\frac{(1/44)^3(2/3)}{(1/4)^2(1/5)}=\frac{5}{7986}$ and $\frac{(1/110)(5f_i/44)^2(1/3)}{(1/10)^2 f_i}=\frac{125f_i}{31{,}944}<\frac{1}{500}$; hence $\Sigma_u<\frac{128}{55}+\frac{1}{25}<3$.
     - $E_{\text{fork+iso}}$ ($v_0\prec m_1,m_2$, iso $m_3$, $i=r_{v_0}$): $|M|=1$ ideals sum to $q(\text{fork},\text{full})+2\cdot\frac{65}{88}\le\frac{49}{55}+\frac{65}{44}=\frac{521}{220}$; $|M|=2$ ideals sum to $2\cdot\frac{5h_i}{1936f_i}+\frac{5}{968}+\frac{5}{176}\le\frac{19}{968}+\frac{65}{1936}=\frac{103}{1936}<\frac{1}{10}$; $|M|=3$ ideals ($\varnothing,\{v_0\}$) equal $\frac{25}{31{,}944}$ and $\frac{125}{127{,}776}$; hence $\Sigma_u<\frac{521}{220}+\frac{1}{9}<3$.
     - $E_{\text{3-claw}}=A_1\oplus A_3$ ($v_0\prec m_1,m_2,m_3$, $i=r_{v_0}$): $|M|=1$ ideals sum to $3\,q(\text{fork},\text{full})\le\frac{147}{55}$; $|M|=2$ ideals sum to $3\cdot\frac{h_i}{1936f_i^2}\le\frac{171}{4840}$; $|M|=3$ ideals ($\varnothing,\{v_0\}$) equal $\frac{(1/44)^3(2/3)}{(1/5)^3}=\frac{125}{127{,}776}$ and $\frac{(1/44)^3(1/3)}{f_i^3}\le\frac{9}{10{,}648}$; hence $\Sigma_u<\frac{147}{55}+\frac{1}{25}<3$.
   - **$|\operatorname{Max}(P)|=4$ ($1$ class: $A_4$):** Grouping the $2^4-1=15$ proper subsets $S\subsetneq A_4$ by $|S|\in\{3,2,1,0\}$ ($|M|=4-|S|$) gives:
     - $\binom{4}{3}=4$ subsets of size $3$ ($|M|=1$): $u(S)=q(A_3,A_3)=\frac{4}{5}$ each, contributing $4\cdot\frac{4}{5}=\frac{16}{5}$;
     - $\binom{4}{2}=6$ subsets of size $2$ ($|M|=2$): $u(S)=\frac{(1/20)^2}{11/20}=\frac{1}{220}$ each, contributing $6\cdot\frac{1}{220}=\frac{3}{110}$;
     - $\binom{4}{1}=4$ subsets of size $1$ ($|M|=3$): $u(S)=\frac{(1/110)^3(1/3)}{(1/10)^3}=\frac{1}{3993}$ each, contributing $\frac{4}{3993}$;
     - $\binom{4}{0}=1$ empty subset ($|M|=4$): $u(\varnothing)=\frac{q(A_3,\varnothing)^4 q(A_1,\varnothing)^4}{q(A_2,\varnothing)^6 q(\varnothing,\varnothing)}=\frac{(1/44)^4(2/3)^4}{(1/4)^6}=\frac{16\cdot 4096}{256\cdot 14{,}641\cdot 81}=\frac{256}{1{,}185{,}921}$.

   Since $\Sigma_u(A_4)>\frac{16}{5}>3>\Sigma_u(P,r)$ for all other $15$ classes, $M_4=\Sigma_u(A_4)=\frac{16}{5}+\frac{3}{110}+\frac{4}{3993}+\frac{256}{1{,}185{,}921}<\frac{16}{5}+\frac{1}{30}+\frac{1}{900}+\frac{1}{4000}<\frac{17}{5}<4$, proving (8). With $a_4=\frac{1}{10}$, $2(1+M_4)<2(1+4)=10$ gives $a_4<\frac{1}{2(1+M_4)}$ and $q(P,r,P)\ge 1-\frac{M_4}{10}>1-\frac{2}{5}=\frac{3}{5}$. $\blacksquare$

| $\lvert\operatorname{Max}(P)\rvert$ | Classes $P\in\mathcal U_4$ | Proper ideals | Exact or sharp $\Sigma_u(P,r)=\sum_{S\subsetneq P}u(P,r,S)$ | Upper bound |
| :---: | --- | :---: | :---: | :---: |
| $1$ | $E_{\text{3-join}},\,E_{\text{asym-join}},\,E_{\text{lower-join}},\,E_{\text{diamond}},\,C_4$ | $8,6,5,5,4$ | $1$ (identically for all $r$) | $1$ |
| $2$ | $E_{\text{upper-fork}},\,E_{\text{asym-fork}},\,E_{\text{3chain+iso}},\,E_{\text{crown}},\,E_{\text{join+iso}},\,E_{\text{N-poset}},\,E_{\text{2-edges}}$ | $5,6,7,6,9,7,8$ | $\le\frac{68{,}791}{36{,}784},\,\frac{18{,}007}{9{,}680},\,\frac{3{,}535}{1{,}936},\,\frac{9{,}751}{5{,}324},\,\frac{221}{121},\,\frac{10{,}085}{5{,}808},\,\frac{9{,}643}{5{,}808}$ | $<2$ |
| $3$ | $E_{\text{edge+2iso}},\,E_{\text{fork+iso}},\,E_{\text{3-claw}}$ | $11,9,8$ | $<\frac{128}{55}+\frac{1}{25},\ <\frac{521}{220}+\frac{1}{9},\ <\frac{147}{55}+\frac{1}{25}$ | $<3$ |
| $4$ | $A_4$ (`4-antichain`) | $15$ | $\frac{16}{5}+\frac{3}{110}+\frac{4}{3993}+\frac{256}{1{,}185{,}921}=M_4$ | $<\frac{17}{5}<4$ |

---

## 2. Generalized retention-schedule five-Kraus instrument and exact five-birth causal-focusing continuation

### 2.1 Variable-retention Clifford five-Kraus instrument and exact Choi spectrum

Retain from `NW1-A` §2.1–2.2 the qubit Hilbert space $\mathcal H_Q=\mathbb C^2$, standard Pauli matrices $(X,Y,Z)$, Clifford axis-cycling unitary $U_*=e^{-i\frac{\pi}{4}Z}e^{-i\frac{\pi}{4}X}$ satisfying $U_*XU_*^\dagger=Y$, $U_*YU_*^\dagger=Z$, $U_*ZU_*^\dagger=X$, and $U_*^3=-I_Q$, stage-indexed Pauli axes $\Sigma_0:=Y$ and $\Sigma_n:=U_*^n\Sigma_0(U_*^\dagger)^n$ ($(\Sigma_0,\Sigma_1,\Sigma_2,\Sigma_3,\Sigma_4,\Sigma_5,\dots)=(Y,Z,X,Y,Z,X,\dots)$), precursor-local phase schedule $\{\varphi_{K,b}\}\subseteq(-\pi,\pi]$ indexed by the isomorphism class $K(S,r|_S)$ of $(S,\prec|_S,r|_S)$ and newborn bit $b\in\{0,1\}$, and step unitaries $U_{n,K,b}:=U_*\exp\bigl(-i\frac{\varphi_{K,b}}{2}\Sigma_n\bigr)$.

To test horizon extensions beyond `NW1-A`'s fixed $\lambda=\frac{1}{2}$, introduce an arbitrary stage-dependent coherent retention schedule $(\lambda_n)_{n\ge 0}\subset(0,1]$ with cumulative products
$$
\Lambda_0:=1,\qquad \Lambda_n:=\prod_{j=0}^{n-1}\lambda_j\quad (n\ge 1),
\tag{9}
$$
and define for any real drift parameter $r\in\mathbb R$ and unitary $U=U_{n,K,b}$ the generalized core map and branch superoperator
$$
\mathcal M_{\lambda_n}(r,\Sigma_n,U)(A):=\lambda_n\,UAU^\dagger+\frac{1}{2}\operatorname{Tr}\!\Bigl[\bigl((1-\lambda_n)I_Q+r\Sigma_n\bigr)A\Bigr]I_Q,
\tag{10}
$$
$$
\mathcal B^{P,r}_{S,b}(A):=\frac{1}{2}q(P,r,S)\,\mathcal M_{\lambda_{|P|}}\!\bigl(r_P(S),\,\Sigma_{|P|},\,U_{|P|,K(S,r|_S),b}\bigr)(A).
\tag{11}
$$
Note that $\lambda_n=\frac{1}{2}$ recovers `NW1-A` Eq. (11) identically ($\frac{1}{2}UAU^\dagger+\frac{1}{4}\operatorname{Tr}[(I_Q+2r\Sigma_n)A]I_Q$), while $\lambda_n=1$ with $r=0$ is the pure unitary channel $UAU^\dagger$.

**Theorem 2 (Generalized retention-$\lambda_n$ five-Kraus CPTP instrument, exact Choi spectrum, history composition, and martingale).** *Fix any stage $n\ge 0$, retention $\lambda_n\in(0,1)$, Pauli axis $\Sigma_n$ with orthonormal eigenbasis $\{|\psi_{n,+}\rangle,|\psi_{n,-}\rangle\}$, unitary $U=U_{n,K,b}$, and real drift $r\in\mathbb R$.*

1. *(Five-Kraus decomposition and necessary-and-sufficient Choi spectrum condition.)* *With $|\Omega\rangle:=|0\rangle\otimes|0\rangle+|1\rangle\otimes|1\rangle\in\mathbb C^2\otimes\mathbb C^2$, the $4\times 4$ Choi matrix $J(\mathcal M_{\lambda_n}):=(\mathcal M_{\lambda_n}(r,\Sigma_n,U)\otimes\operatorname{id}_{\mathbb C^2})(|\Omega\rangle\langle\Omega|)$ has exact eigenvalue spectrum*
   $$
   \operatorname{Spec}\bigl(J(\mathcal M_{\lambda_n})\bigr)=\left\{\frac{1-\lambda_n-r}{2},\ \frac{1-\lambda_n+r}{2},\ \frac{1+\lambda_n-\sqrt{4\lambda_n^2+r^2}}{2},\ \frac{1+\lambda_n+\sqrt{4\lambda_n^2+r^2}}{2}\right\}.
   \tag{12}
   $$
   *Consequently, $\mathcal M_{\lambda_n}$ is completely positive ($J(\mathcal M_{\lambda_n})\succeq 0$) if and only if $|r|\le 1-\lambda_n$, and **strictly** completely positive ($J(\mathcal M_{\lambda_n})\succ 0$) **if and only if** $|r|<1-\lambda_n$. Whenever $|r|\le 1-\lambda_n$, the five operators*
   $$
   L_0:=\sqrt{\lambda_n}\,U,\qquad L_{\alpha,\beta}:=\sqrt{\frac{1-\lambda_n+\alpha r}{2}}\,|\beta\rangle\langle\psi_{n,\alpha}|\qquad (\alpha\in\{+,-\},\ \beta\in\{0,1\})
   \tag{13}
   $$
   *satisfy $L_0AL_0^\dagger+\sum_{\alpha,\beta}L_{\alpha,\beta}AL_{\alpha,\beta}^\dagger=\mathcal M_{\lambda_n}(r,\Sigma_n,U)(A)$ and $L_0^\dagger L_0+\sum_{\alpha,\beta}L_{\alpha,\beta}^\dagger L_{\alpha,\beta}=I_Q+r\Sigma_n$.*
2. *(Closed-form $m$-step composition, entangled diamond commutation, and Heisenberg martingale.)* *Suppose on horizon $|P|\le N-1$ ($N\ge 1$) that $H:\bigcup_{k=0}^N\mathcal U_k\to\mathbb R$ is a mark-independent forward harmonic potential ($\sum_{S\subseteq P}q(P,r,S)H(P+S)=H(P)$ for all marked $(P,r)$ with $|P|\le N-1$), and set*
   $$
   r_P(S):=\frac{\theta}{\Lambda_{|P|}}\bigl[H(P+S)-H(P)\bigr]\qquad (|P|\le N-1)
   \tag{14}
   $$
   *with $|r_P(S)|<1-\lambda_{|P|}$. Then every $\mathcal B^{P,r}_{S,b}$ is strictly completely positive, complete-row trace-preserving ($\sum_{S,b}\operatorname{Tr}[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})]=1$), proper-slot mark-local, and relabeling-equivariant. For any $m$-birth history $h=((S_0,b_0),\dots,(S_{m-1},b_{m-1}))$ ($m\ge 1$, $n+m\le N$) from $(C,r)$ ($|C|=n$) to unmarked endpoint $E=P_m$, writing $W_{\rm str}(h):=\prod_{j=0}^{m-1}q(P_j,r_j,S_j)$, $\Phi_h:=\sum_{j=0}^{m-1}\varphi_{K(S_j,r_j|_{S_j}),b_j}$, and $\lambda_{n,m}:=\prod_{j=0}^{m-1}\lambda_{n+j}=\Lambda_{n+m}/\Lambda_n$, the composed superoperator $\mathcal B_h=\mathcal B^{P_{m-1},r_{m-1}}_{S_{m-1},b_{m-1}}\circ\cdots\circ\mathcal B^{P_0,r_0}_{S_0,b_0}$ obeys*
   $$
   (\mathcal B_h\otimes\operatorname{id}_{\rm ref})(X)=2^{-m}W_{\rm str}(h)\left\{\lambda_{n,m}\bigl(U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}\otimes I_{\rm ref}\bigr)X\bigl(e^{+i\frac{\Phi_h}{2}\Sigma_n}(U_*^\dagger)^m\otimes I_{\rm ref}\bigr)+\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q\!\left[\Bigl(\bigl((1-\lambda_{n,m})I_Q+\frac{\theta}{\Lambda_n}\bigl(H(E)-H(C)\bigr)\Sigma_n\bigr)\otimes I_{\rm ref}\Bigr)X\right]\right\}.
   \tag{15}
   $$
   *Hence exact entangled diamond commutation $(\mathcal B^{C+x_S,r+b_x}_{T,c}\circ\mathcal B^{C,r}_{S,b})\otimes\operatorname{id}_{\rm ref}=(\mathcal B^{C+y_T,r+c_y}_{S,b}\circ\mathcal B^{C,r}_{T,c})\otimes\operatorname{id}_{\rm ref}$ and transported-suffix commutation hold across all bases $|C|\le N-2$, and $\mathcal Q_n:=\Lambda_n^{-1}\Sigma_n$ ($0\le n\le N$) is an exact nonselective Heisenberg operator martingale: $\sum_{S\subseteq P}\sum_{b=0}^1(\mathcal B^{P,r}_{S,b})^\dagger(\mathcal Q_{|P|+1})=\mathcal Q_{|P|}$.*

**Proof.**
1. Expanding $|\Omega\rangle\langle\Omega|=\sum_{j,k=0}^1|j\rangle\langle k|\otimes|j\rangle\langle k|$ gives
   $$
   J(\mathcal M_{\lambda_n})=2\lambda_n|\Phi_U\rangle\langle\Phi_U|+\frac{1}{2}I_2\otimes\bigl((1-\lambda_n)I_2+r\Sigma_n^T\bigr),
   $$
   where $|\Phi_U\rangle:=\frac{1}{\sqrt 2}(U\otimes I_2)|\Omega\rangle=\frac{1}{\sqrt 2}(|u_+\rangle\otimes|\chi_+\rangle+|u_-\rangle\otimes|\chi_-\rangle)$ is a unit vector in the orthonormal basis $|f_1\rangle=|u_+\rangle\otimes|\chi_+\rangle$, $|f_2\rangle=|u_-\rangle\otimes|\chi_-\rangle$, $|f_3\rangle=|u_+\rangle\otimes|\chi_-\rangle$, $|f_4\rangle=|u_-\rangle\otimes|\chi_+\rangle$ of `NW1-A` Theorem 2 ($|u_\alpha\rangle=U|\psi_{n,\alpha}\rangle$, $|\chi_\alpha\rangle=\overline{|\psi_{n,\alpha}\rangle}$). In this basis, $J(\mathcal M_{\lambda_n})$ block-diagonalizes as
   $$
   J(\mathcal M_{\lambda_n})\cong
   \begin{pmatrix}
   \frac{1+\lambda_n+r}{2} & \lambda_n & 0 & 0\\
   \lambda_n & \frac{1+\lambda_n-r}{2} & 0 & 0\\
   0 & 0 & \frac{1-\lambda_n-r}{2} & 0\\
   0 & 0 & 0 & \frac{1-\lambda_n+r}{2}
   \end{pmatrix}.
   $$
   The two $1\times 1$ blocks give eigenvalues $\frac{1-\lambda_n\mp r}{2}$. The $2\times 2$ block has trace $1+\lambda_n$ and determinant $\frac{(1+\lambda_n)^2-r^2}{4}-\lambda_n^2=\frac{1+2\lambda_n-3\lambda_n^2-r^2}{4}$, with discriminant $(1+\lambda_n)^2-(1+2\lambda_n-3\lambda_n^2-r^2)=4\lambda_n^2+r^2>0$, giving eigenvalues $\frac{1+\lambda_n\pm\sqrt{4\lambda_n^2+r^2}}{2}$ and proving (12). Because $(2\lambda_n+|r|)^2-(4\lambda_n^2+r^2)=4\lambda_n|r|\ge 0$, we have $\sqrt{4\lambda_n^2+r^2}\le 2\lambda_n+|r|$, whence
   $$
   \frac{1+\lambda_n-\sqrt{4\lambda_n^2+r^2}}{2}\ge\frac{1+\lambda_n-(2\lambda_n+|r|)}{2}=\frac{1-\lambda_n-|r|}{2}=\min_{\pm}\frac{1-\lambda_n\pm r}{2}.
   $$
   Therefore $\lambda_{\min}(J(\mathcal M_{\lambda_n}))=\frac{1-\lambda_n-|r|}{2}$, which is $\ge 0$ if and only if $|r|\le 1-\lambda_n$ and $>0$ if and only if $|r|<1-\lambda_n$. When $|r|\le 1-\lambda_n$, $1-\lambda_n+\alpha r\ge 0$, so $L_0,L_{\alpha,\beta}$ in (13) are well-defined and direct summation over $\beta\in\{0,1\}$ ($\sum_\beta|\beta\rangle\langle\beta|=I_Q$) and $\alpha\in\{+,-\}$ ($\sum_\alpha(1-\lambda_n+\alpha r)|\psi_{n,\alpha}\rangle\langle\psi_{n,\alpha}|=(1-\lambda_n)I_Q+r\Sigma_n$) verifies both identities.

2. Note first that $\mathcal M_{\lambda_n}(r,\Sigma_n,U)(I_Q/2)=\frac{\lambda_n}{2}I_Q+\frac{1-\lambda_n}{2}I_Q=I_Q/2$ (since $\operatorname{Tr}\Sigma_n=0$) and $\mathcal M_{\lambda_n}^\dagger(B)=\lambda_n U^\dagger BU+\frac{\operatorname{Tr}B}{2}((1-\lambda_n)I_Q+r\Sigma_n)$, so $\mathcal M_{\lambda_n}^\dagger(I_Q)=I_Q+r\Sigma_n$. Harmonicity of $H$ gives $\sum_{S\subseteq P}q(P,r,S)r_P(S)=0$, proving complete-row trace preservation $\sum_{S,b}(\mathcal B^{P,r}_{S,b})^\dagger(I_Q)=I_Q$. Proper-slot locality and equivariance follow from Theorem 1 because $r_P(S)$ reads only $(P,S)$ and $U_{|P|,K(S,r|_S),b}$ reads $r$ only via $K(S,r|_S)$.

   We prove (15) by induction on $m\ge 1$. For $m=1$, $\lambda_{n,1}=\lambda_n$, $\frac{\theta}{\Lambda_n}(H(E)-H(C))=r_C(S_0)$, and (15) matches (10)–(11). Assuming (15) at step $m$ ending at $(P_m,r_m)$ ($|P_m|=n+m\le N-1$) and appending $(S_m,b_m)$ with retention $\lambda_{n+m}$, unitary $U_m=U_{n+m,K_m,b_m}$, and drift $r_m=\frac{\theta}{\Lambda_{n+m}}(H(P_{m+1})-H(P_m))$:
   - Applying $\mathcal M_{\lambda_{n+m}}\otimes\operatorname{id}_{\rm ref}$ to the $\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q[\cdots]$ reset block leaves it invariant by $\mathcal M_{\lambda_{n+m}}(I_Q/2)=I_Q/2$.
   - On the coherent block $\lambda_{n,m}(V_m\otimes I_{\rm ref})X(V_m^\dagger\otimes I_{\rm ref})$ ($V_m:=U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}$), the unitary part produces $\lambda_{n+m}\lambda_{n,m}=\lambda_{n,m+1}$ times conjugation by $U_m V_m=U_*^{m+1}e^{-i\frac{\Phi_h+\varphi_{K_m,b_m}}{2}\Sigma_n}$ (`NW1-A` Eq. (20)), while the reset part contributes $\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q[\lambda_{n,m}(V_m^\dagger((1-\lambda_{n+m})I_Q+r_m\Sigma_{n+m})V_m\otimes I_{\rm ref})X]$. Using $V_m^\dagger\Sigma_{n+m}V_m=\Sigma_n$, $\lambda_{n,m}(1-\lambda_{n+m})=\lambda_{n,m}-\lambda_{n,m+1}$ (which adds to $1-\lambda_{n,m}$ to give $1-\lambda_{n,m+1}$), and
     $$
     \lambda_{n,m}\,r_m=\frac{\Lambda_{n+m}}{\Lambda_n}\cdot\frac{\theta}{\Lambda_{n+m}}\bigl[H(P_{m+1})-H(P_m)\bigr]=\frac{\theta}{\Lambda_n}\bigl[H(P_{m+1})-H(P_m)\bigr],
     $$
     the potential increments telescope to $\frac{\theta}{\Lambda_n}[H(P_{m+1})-H(C)]$, closing the induction.

   Setting $m=2$ in (15) for incomparable births $(S,b)$ and $(T,c)$ on $(C,r)$ ($|C|\le N-2$) shows that $W_{\rm str}$ agrees by Theorem 1's scalar diamond identity (2), $\Phi_h=\varphi_{K(S,r|_S),b}+\varphi_{K(T,r|_T),c}$ agrees because $x\notin T$ and $y\notin S$, and $H(E)-H(C)$ agrees because both paths yield the same unmarked poset $E$; equivariance preserves equality under any transported suffix. Finally, since $\operatorname{Tr}\Sigma_{n+1}=0$ and $U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=\Sigma_n$,
   $$
   \bigl(\mathcal B^{P,r}_{S,b}\bigr)^\dagger(\Lambda_{n+1}^{-1}\Sigma_{n+1})=\frac{1}{2}q(P,r,S)\,\lambda_n\Lambda_{n+1}^{-1}U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=\frac{1}{2}q(P,r,S)\,\Lambda_n^{-1}\Sigma_n,
   $$
   which sums over $(S,b)$ to $\mathcal Q_n$. $\blacksquare$

### 2.2 Explicit six-class five-birth continuation $H_{\rm foc}^{(5)}$ and exact `5 -> 4` prefix consistency

Recall from `NW1-A` §1.3 the canonical four-birth causal-focusing indicator $H_{\rm foc}:\mathcal U_4\to\{0,1\}$, which equals $1$ on the three single-rooted causal classes $\{E_{\text{asym-fork}},E_{\text{diamond}},C_4\}$ and $0$ on the remaining $13$ classes of $\mathcal U_4$ (with backward values $H_{\rm foc}(\text{fork})=H_{\rm foc}(C_3)=\frac{21}{22}$, $H_{\rm foc}(C_2)=\frac{42}{55}$, $H_{\rm foc}(A_1)=H_{\rm foc}(\varnothing)=\frac{14}{55}$, and $0$ elsewhere). Extending `NW1-A` intact through a fifth birth ($|P|=4\to 5$, $|\mathcal U_5|=63$ unmarked isomorphism classes) under Theorem 1's kernel $q(P,r,S)$ ($a_4\in(0,1/M_4)$) requires an unmarked function $H_{\rm foc}^{(5)}:\mathcal U_5\to\mathbb R$ satisfying the mark-independent harmonic continuation equation
$$
\sum_{S\subseteq P}q(P,r,S)\,H_{\rm foc}^{(5)}(P+S)=H_{\rm foc}(P)\qquad \forall P\in\mathcal U_4,\ \forall r\in\{0,1\}^4.
\tag{16}
$$

To solve (16) transparently across all $16$ marked four-poset families without solving a $63$-variable linear system by machine, we isolate the exact parent-reconstruction sets of five targeted five-element posets. For any $Q\in\mathcal U_5$, a four-poset $P\in\mathcal U_4$ can transition to $Q$ ($P+x_S\cong Q$ for some ideal $S\subseteq P$) if and only if $Q\setminus\{x\}\cong P$ for some maximal element $x\in\operatorname{Max}(Q)$ (in which case $S=\operatorname{Pred}_Q(x):=\{u\in Q\setminus\{x\}:u\prec_Q x\}$). Define in $\mathcal U_5$:
- $C_5:=C_4\oplus A_1$ (`5-chain`), $E_{\text{diamond}}\oplus A_1$, and $E_{\text{asym-fork}}\oplus A_1$, each having $|\operatorname{Max}(Q)|=1$;
- $Q_d:=A_1\oplus(C_2\sqcup C_2)$ ($v_0\prec u_1\prec m_1$ and $v_0\prec u_2\prec m_2$, two disjoint two-chains above a single root);
- $Q_p:=E_{\text{asym-fork}}+\{v_0,u,m_2\}$ ($v_0\prec u\prec m_1$ together with $v_0\prec u\prec x_{\rm new}$ and $v_0\prec m_2\prec x_{\rm new}$, i.e., a four-diamond $\{v_0,u,m_2,x_{\rm new}\}$ sharing $v_0\prec u$ with a pendant leaf $m_1$ above $u$);
- $Q_{\rm bipy}:=A_1\oplus A_2\oplus A_2$ ($v_0\prec u,w\prec m_{\max},x_{\rm new}$, single-rooted two-by-two crown above $v_0$).

**Lemma 2 (Parent-exclusivity reconstruction in $\mathcal U_5$).**
1. *(Unique-top reconstruction.)* *If $Q\in\mathcal U_5$ satisfies $|\operatorname{Max}(Q)|=1$ with $\operatorname{Max}(Q)=\{v_{\max}\}$, then $Q=P_0\oplus A_1$ where $P_0:=Q\setminus\{v_{\max}\}\in\mathcal U_4$, and $P+S\cong Q$ holds if and only if $P\cong P_0$ and $S=P$. In particular, $C_5$, $E_{\text{diamond}}\oplus A_1$, and $E_{\text{asym-fork}}\oplus A_1$ arise solely from $C_4$, $E_{\text{diamond}}$, and $E_{\text{asym-fork}}$ respectively, each exclusively at its full ideal $S=P$.*
2. *(Exclusive parents of $Q_d$, $Q_p$, and $Q_{\rm bipy}$.)* *In $\mathcal U_4$:*
   - *$Q_d=A_1\oplus(C_2\sqcup C_2)$ has $E_{\text{asym-fork}}$ as its **unique** parent (exclusively via $S_4=\{v_0,m_2\}$);*
   - *$Q_{\rm bipy}=A_1\oplus A_2\oplus A_2$ has $E_{\text{diamond}}$ as its **unique** parent (exclusively via $S=\{v_0,u,w\}$);*
   - *$Q_p$ has **only** $\{E_{\text{asym-fork}},E_{\text{diamond}}\}$ as parents (via $S_6=\{v_0,u,m_2\}$ on $E_{\text{asym-fork}}$ and via the two symmetric ideals $\{v_0,u\},\{v_0,w\}$ on $E_{\text{diamond}}$).*

**Proof.**
1. Any birth $P+x_S$ places $x$ in $\operatorname{Max}(P+x_S)$. If $\operatorname{Max}(Q)=\{v_{\max}\}$, then necessarily $x=v_{\max}$, $P\cong Q\setminus\{v_{\max}\}=P_0$, and every $u\in P_0$ satisfies $u\prec_Q v_{\max}$ (for if $\operatorname{Max}(P_0)\setminus S$ were nonempty, its elements would remain maximal in $P_0+S$, giving $|\operatorname{Max}(Q)|\ge 2$), whence $S=P$.
2. Inspect $\operatorname{Max}(Q)$ for each class:
   - $\operatorname{Max}(Q_d)=\{m_1,m_2\}$. Deleting $m_1$ leaves $v_0\prec u_1$ and $v_0\prec u_2\prec m_2$, isomorphic to $E_{\text{asym-fork}}$ with strict past $\operatorname{Pred}_{Q_d}(m_1)=\{v_0,u_1\}$ (the $S_4$ slot under $u_1\leftrightarrow m_2$); by symmetry, deleting $m_2$ also leaves $E_{\text{asym-fork}}$ at $S_4$.
   - $\operatorname{Max}(Q_{\rm bipy})=\{m_{\max},x_{\rm new}\}$. Deleting either leaves $v_0\prec u,w\prec m_{\text{other}}$, which is $E_{\text{diamond}}$ with strict past $\{v_0,u,w\}$.
   - $\operatorname{Max}(Q_p)=\{m_1,x_{\rm new}\}$ (since $v_0\prec u\prec m_1$ and $v_0\prec u,m_2\prec x_{\rm new}$ leave only $m_1$ and $x_{\rm new}$ maximal). Deleting $x_{\rm new}$ leaves $E_{\text{asym-fork}}$ with $\operatorname{Pred}_{Q_p}(x_{\rm new})=\{v_0,u,m_2\}=S_6$; deleting $m_1$ leaves $\{v_0\prec u,m_2\prec x_{\rm new}\}=E_{\text{diamond}}$ with $\operatorname{Pred}_{Q_p}(m_1)=\{v_0,u\}$ (symmetric to $\{v_0,m_2\}$ in $E_{\text{diamond}}$). $\blacksquare$

**Theorem 3 (Explicit nonnegative six-class continuation $H_{\rm foc}^{(5)}$, `5 -> 4` prefix recovery, and five-birth rational contrasts).**
1. *(Exact mark-independent continuation across $\mathcal U_4\to\mathcal U_5$.)* *For every scale parameter $a_4\in(0,1/M_4)$ satisfying $a_4<\frac{22}{43}$ (in particular for $a_4=\frac{1}{10}$), define $H_{\rm foc}^{(5)}:\mathcal U_5\to[0,\infty)$ on the six classes of Lemma 2 by*
   $$
   H_{\rm foc}^{(5)}(C_5):=\frac{1}{1-a_4},\qquad
   H_{\rm foc}^{(5)}(E_{\text{asym-fork}}\oplus A_1)=H_{\rm foc}^{(5)}(Q_p)=H_{\rm foc}^{(5)}(Q_{\rm bipy}):=\frac{1}{1-\frac{3623}{3872}a_4}=:H_1,
   \tag{17a}
   $$
   $$
   H_{\rm foc}^{(5)}(Q_d):=\frac{1023}{968}H_1=\frac{1023}{968\bigl(1-\frac{3623}{3872}a_4\bigr)},\qquad
   H_{\rm foc}^{(5)}(E_{\text{diamond}}\oplus A_1):=\frac{1-\frac{21}{22}a_4 H_1}{1-a_4},
   \tag{17b}
   $$
   *and set $H_{\rm foc}^{(5)}(Q):=0$ on all other $57$ classes $Q\in\mathcal U_5$. Then $H_{\rm foc}^{(5)}(Q)\ge 0$ everywhere on $\mathcal U_5$, and (16) holds identically across all $16$ unmarked four-posets $P\in\mathcal U_4$ and all $16$ vertex markings $r\in\{0,1\}^4$.*
2. *(Five-birth CPTP realization and exact `5 -> 4` prefix consistency.)* *Fix $a_4=\frac{1}{10}$, $\theta=\frac{1}{32}$, and the five-step retention schedule $(\lambda_0,\lambda_1,\lambda_2,\lambda_3,\lambda_4)=(\frac{1}{2},\frac{1}{2},\frac{1}{2},\frac{1}{2},\frac{1}{4})$ ($\Lambda_n=2^{-n}$ for $0\le n\le 4$, $\Lambda_5=\frac{1}{64}$). Then (17a)–(17b) take the exact rational values*
   $$
   H_{\rm foc}^{(5)}(C_5)=\frac{10}{9},\quad
   H_1=\frac{38{,}720}{35{,}097},\quad
   H_{\rm foc}^{(5)}(Q_d)=\frac{13{,}640}{11{,}699},\quad
   H_{\rm foc}^{(5)}(E_{\text{diamond}}\oplus A_1)=\frac{11{,}630}{11{,}699},
   \tag{18}
   $$
   *every step-5 drift coefficient $r_P(S)=\frac{1}{2}[H_{\rm foc}^{(5)}(P+S)-H_{\rm foc}(P)]$ ($|P|=4$) satisfies*
   $$
   |r_P(S)|\le\frac{1}{2}<\frac{3}{4}=1-\lambda_4\qquad \bigl(J(\mathcal M_{\lambda_4})\succeq\tfrac{1}{8}I_4\succ 0\bigr),
   \tag{19}
   $$
   *and marginalizing step $5$ over $(S_4,b_4)\in\mathcal I(P_4)\times\{0,1\}$ recovers the complete four-birth unnormalized superoperator and 60-history probability ledger of `NW1-A` identically for every input state $\rho_{Q,\rm ref}$.*
3. *(Exact five-birth rational Pauli, height, and Benincasa–Dowker interval-action contrasts.)* *Define the dimensionless five-element Benincasa–Dowker interval action $S_{\rm BD}^{(5)}(Q):=5-2n_0(Q)+4n_1(Q)-2n_2(Q)$, where $n_k(Q)$ counts comparable pairs $x\prec_Q y$ with $|\{z\in Q:x\prec_Q z\prec_Q y\}|=k$. At step $5$ ($\Sigma_4=Z$):*
   - *Conditional on $(C_4,r)$ (for every $r\in\{0,1\}^4$) and state $\rho\in\mathcal D(\mathbb C^2)$,*
     $$
     \mathbb P_\rho(C_5\mid C_4,r)=\frac{9}{10}+\frac{1}{20}\operatorname{Tr}[Z\rho],\qquad
     \mathbb E_\rho\bigl[h(Q)\mid C_4,r\bigr]=\frac{49}{10}+\frac{1}{20}\operatorname{Tr}[Z\rho].
     \tag{20}
     $$
   - *Conditional on $(E_{\text{diamond}},r)$ with root mark $i=r_{v_0}\in\{0,1\}$ and state $\rho\in\mathcal D(\mathbb C^2)$,*
     $$
     \mathbb E_\rho\bigl[S_{\rm BD}^{(5)}(Q)\mid E_{\text{diamond}},r_{v_0}=0\bigr]=-\frac{43}{1100}-\frac{2{,}785{,}889}{77{,}213{,}400}\operatorname{Tr}[Z\rho],
     \tag{21a}
     $$
     $$
     \mathbb E_\rho\bigl[S_{\rm BD}^{(5)}(Q)\mid E_{\text{diamond}},r_{v_0}=1\bigr]=-\frac{139}{1100}-\frac{3{,}133{,}697}{77{,}213{,}400}\operatorname{Tr}[Z\rho],
     \tag{21b}
     $$
     *with nonzero step-5 mark–coherence interaction contrast $-\frac{14{,}492}{3{,}217{,}225}\Delta\langle Z\rangle\ne 0$.*

**Proof.**
1. By Lemma 2, every parent in $\mathcal U_4$ of the six-class support $\mathcal S_6:=\{C_5,E_{\text{diamond}}\oplus A_1,E_{\text{asym-fork}}\oplus A_1,Q_d,Q_p,Q_{\rm bipy}\}$ belongs to $\{C_4,E_{\text{diamond}},E_{\text{asym-fork}}\}$. Hence for each of the $13$ classes $P\in\mathcal U_4$ with $H_{\rm foc}(P)=0$, $P+S\notin\mathcal S_6$ for every $S\subseteq P$, so $\sum_{S\subseteq P}q(P,r,S)H_{\rm foc}^{(5)}(P+S)=0=H_{\rm foc}(P)$ holds identically for all $r\in\{0,1\}^4$. It remains to verify the three unit classes:
   - **Parent $C_4$ ($H_{\rm foc}(C_4)=1$):** $|\operatorname{Max}(C_4)|=1$ gives $q(C_4,r,C_4)=1-a_4$ by Lemma 1(1) with $C_4+C_4=C_5$, while none of the four proper ideals of $C_4$ ($C_4\sqcup A_1$, $A_1\oplus(C_3\sqcup A_1)$, $C_2\oplus(C_2\sqcup A_1)$, $C_3\oplus A_2$) lies in $\mathcal S_6$ by Lemma 2. Thus $\sum_{S\subseteq C_4}q(C_4,r,S)H_{\rm foc}^{(5)}(C_4+S)=(1-a_4)\frac{1}{1-a_4}=1$.
   - **Parent $E_{\text{asym-fork}}$ ($v_0\prec u\prec m_1,\ v_0\prec m_2$, root mark $i=r_{v_0}\in\{0,1\}$, $H_{\rm foc}=1$):** By Lemma 1(2) and Lemma 2, among all $7$ ideals of $E_{\text{asym-fork}}$, those landing in $\mathcal S_6$ are precisely the full ideal $S=P$ ($P\oplus A_1$, value $H_1$), the sixth proper ideal $S_6=\{v_0,u,m_2\}$ ($Q_p$, value $H_1$), and the fourth proper ideal $S_4=\{v_0,m_2\}$ ($Q_d$, value $\frac{1023}{968}H_1$, $u(S_4)=\frac{h_i}{44f_i}$). Because $P\oplus A_1$ and $Q_p$ carry the **same** value $H_1$, $q(P,r,P)+q(P,r,S_6)=1-a_4[\Sigma_u(P,r)-u(S_6)]=1-a_4\sum_{k=1}^5 u(S_k)$ cancels $u(S_6)$ identically! Substituting $u(S_1)=\frac{5}{1936}$, $u(S_2)=u(S_3)=\frac{1}{1936f_i}$, $u(S_4)=\frac{h_i}{44f_i}$, and $u(S_5)=\frac{41}{44}$ gives
     $$
     \sum_{S\subseteq E_{\text{asym-fork}}}q(P,r,S)\,H_{\rm foc}^{(5)}(P+S)=H_1\left\{1-a_4\left[\frac{5}{1936}+\frac{41}{44}+\frac{2}{1936f_i}+\left(1-\frac{1023}{968}\right)\frac{h_i}{44f_i}\right]\right\}.
     $$
     Since $1-\frac{1023}{968}=-\frac{55}{968}$ and $\frac{55}{968\cdot 44}=\frac{5\cdot 11}{968\cdot 4\cdot 11}=\frac{5}{3872}$, the $i$-dependent terms combine into
     $$
     \frac{2}{1936f_i}-\frac{5h_i}{3872f_i}=-\frac{5h_i-4}{3872f_i}=-\frac{1}{1936}\left(\frac{5h_i-4}{2f_i}\right).
     \tag{22}
     $$
     Using Part A's seed values $(f_0,h_0)=(\frac{1}{6},\frac{19}{30})$ and $(f_1,h_1)=(\frac{1}{3},\frac{7}{15})$, both satisfy $f_i+h_i=\frac{4}{5}$, i.e., $5h_i-4=-5f_i$, so the root-mark ratio satisfies the exact identity
     $$
     \frac{5h_i-4}{2f_i}=-\frac{5}{2}\qquad \text{for both }i=0\text{ and }i=1.
     \tag{23}
     $$
     Inserting (23) into (22) yields $+\frac{5}{3872}$ independently of $i$, and adding $\frac{5}{1936}+\frac{41}{44}=\frac{10+3608}{3872}=\frac{3618}{3872}$ gives $\frac{3618+5}{3872}=\frac{3623}{3872}$. Multiplying $1-\frac{3623}{3872}a_4$ by $H_1=(1-\frac{3623}{3872}a_4)^{-1}$ equals $1$ for every marking $r\in\{0,1\}^4$.
   - **Parent $E_{\text{diamond}}$ ($v_0\prec u,w\prec m_{\max}$, root mark $i=r_{v_0}\in\{0,1\}$, $H_{\rm foc}=1$):** By Lemma 1(1), $q(P,r,P)=1-a_4$ ($P\oplus A_1$) and $u(P,r,S)=q(\text{fork},r|_Q,S)$ on the five proper ideals. By Lemma 2, $S\in\{\varnothing,\{v_0\}\}$ exit $\mathcal S_6$, while $\{v_0,u\},\{v_0,w\}$ map to $Q_p$ (value $H_1$, combined weight $2a_4\frac{h_i}{44f_i}$) and $\{v_0,u,w\}$ maps to $Q_{\rm bipy}$ (value $H_1$, weight $a_4(\frac{21}{22}-\frac{2h_i}{44f_i})$). Summing cancels $h_i/f_i$ identically:
     $$
     (1-a_4)H_{\rm foc}^{(5)}(E_{\text{diamond}}\oplus A_1)+a_4\left(\frac{2h_i}{44f_i}+\frac{21}{22}-\frac{2h_i}{44f_i}\right)H_1=(1-a_4)\frac{1-\frac{21}{22}a_4H_1}{1-a_4}+\frac{21}{22}a_4H_1=1.
     $$
     Finally, $1-\frac{21}{22}a_4 H_1=\frac{1-(\frac{3623}{3872}+\frac{21}{22})a_4}{1-\frac{3623}{3872}a_4}=\frac{1-\frac{7319}{3872}a_4}{1-\frac{3623}{3872}a_4}>0$ whenever $a_4<\frac{3872}{7319}$ (in particular for all $a_4<\frac{22}{43}$, since $\frac{7319}{3872}<\frac{7568}{3872}=\frac{43}{22}$), ensuring $H_{\rm foc}^{(5)}\ge 0$ everywhere.

2. At $a_4=\frac{1}{10}$: $H_{\rm foc}^{(5)}(C_5)=\frac{10}{9}$; $H_1=(1-\frac{3623}{38{,}720})^{-1}=\frac{38{,}720}{35{,}097}$; $H_{\rm foc}^{(5)}(Q_d)=\frac{1023}{968}\cdot\frac{38{,}720}{35{,}097}=\frac{1023\cdot 40}{35{,}097}=\frac{341\cdot 40}{11{,}699}=\frac{13{,}640}{11{,}699}$; and since $\frac{21}{220}\cdot\frac{38{,}720}{35{,}097}=\frac{21\cdot 176}{35{,}097}=\frac{1232}{11{,}699}$, $H_{\rm foc}^{(5)}(E_{\text{diamond}}\oplus A_1)=\frac{10}{9}(1-\frac{1232}{11{,}699})=\frac{10\cdot 10{,}467}{9\cdot 11{,}699}=\frac{11{,}630}{11{,}699}$, verifying (18). On $|P|\le 3$, $\lambda_n=\frac{1}{2}$ leaves all drift coefficients $|r_P(S)|\le\frac{21}{88}<\frac{1}{2}=1-\lambda_n$ identical to `NW1-A`. At $|P|=4$, $\frac{\theta}{\Lambda_4}=\frac{1/32}{1/16}=\frac{1}{2}$: on the $13$ zero-classes $r_P(S)=0$, while on the $3$ unit-classes every child satisfies $0\le H_{\rm foc}^{(5)}(P+S)\le\frac{13{,}640}{11{,}699}<2$, so $|H_{\rm foc}^{(5)}(P+S)-1|\le\max\{1,\frac{1941}{11{,}699}\}=1$ and $|r_P(S)|\le\frac{1}{2}<\frac{3}{4}=1-\lambda_4$, proving (19) and $J(\mathcal M_{\lambda_4})\succeq\frac{3/4-1/2}{2}I_4=\frac{1}{8}I_4\succ 0$ by Theorem 2(1).

   For any four-birth marked history $h_4$ ending at $(P_4,r_4)$, complete-row trace preservation at step $5$ gives
   $$
   \sum_{S_4\subseteq P_4}\sum_{b_4\in\{0,1\}}\operatorname{Tr}_{Q,\rm ref}\!\Bigl[\bigl(\mathcal B^{P_4,r_4}_{S_4,b_4}\otimes\operatorname{id}_{\rm ref}\bigr)\bigl((\mathcal B_{h_4}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr)\Bigr]=\operatorname{Tr}_{Q,\rm ref}\!\bigl[(\mathcal B_{h_4}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr]=\mathbb P_4(h_4;\rho_{Q,\rm ref}).
   $$
   Thus the `5 -> 4` marginal equals `NW1-A`'s four-birth law identically on every prefix—eliminating the stopping-horizon pathology proved in [interval action and stopping horizon](interval_action_and_stopping_horizon.md), where terminal $e^{-\lambda S_n}$ weighting distorted recorded three-birth $E:C$ log-odds by $\frac{29}{66}\lambda+O(\lambda^2)\ne 0$.

3. At step $5$ on $C_4$ ($\Sigma_4=Z$), $q(C_4,r,C_4)=\frac{9}{10}$ and $r_{C_4}(C_4)=\frac{1}{2}(\frac{10}{9}-1)=\frac{1}{18}$ give $\mathbb P_\rho(C_5\mid C_4,r)=\frac{9}{10}(1+\frac{1}{18}\operatorname{Tr}[Z\rho])=\frac{9}{10}+\frac{1}{20}\operatorname{Tr}[Z\rho]$; since $h(C_5)=5$ and $h(C_4+S)=4$ for all four proper ideals $S\subsetneq C_4$, $\mathbb E_\rho[h(Q)\mid C_4,r]=4+\mathbb P_\rho(C_5\mid C_4,r)=\frac{49}{10}+\frac{1}{20}\operatorname{Tr}[Z\rho]$, proving (20).

   On $E_{\text{diamond}}$ ($v_0\prec u,w\prec m_{\max}$, $r_{v_0}=i\in\{0,1\}$), evaluate $(n_0,n_1,n_2)$ and $S_{\rm BD}^{(5)}=5-2n_0+4n_1-2n_2$ across all $6$ ideals:
   - $S=\varnothing$ ($q=\frac{1}{440}$, $E_{\text{diamond}}\sqcup A_1$): $(4,0,1)\implies S_{\rm BD}^{(5)}=-5$, $r=-\frac{1}{2}$;
   - $S=\{v_0\}$ ($q=\frac{1}{440}$): $(5,0,1)\implies S_{\rm BD}^{(5)}=-7$, $r=-\frac{1}{2}$;
   - $S=\{v_0,u\},\{v_0,w\}$ ($q_{\rm sum}=\frac{h_i}{220f_i}$, $Q_p$): covers $(v_0,u),(v_0,w),(u,m_{\max}),(w,m_{\max}),(u,x_{\rm new})$ give $n_0=5$; $(v_0,x_{\rm new})$ via $u$ gives $n_1=1$; $(v_0,m_{\max})$ via $\{u,w\}$ gives $n_2=1$, so $S_{\rm BD}^{(5)}=5-10+4-2=-3$, with $r=\frac{1}{2}(H_1-1)=+\frac{3623}{70{,}194}$;
   - $S=\{v_0,u,w\}$ ($q=\frac{21}{220}-\frac{h_i}{220f_i}$, $Q_{\rm bipy}$): $(6,0,2)\implies S_{\rm BD}^{(5)}=5-12+0-4=-11$, with $r=+\frac{3623}{70{,}194}$;
   - $S=P$ ($q=\frac{9}{10}$, $E_{\text{diamond}}\oplus A_1$): covers $5$, $1$-intervening $(u,x_{\rm new}),(w,x_{\rm new})$ ($n_1=2$), $2$-intervening $(v_0,m_{\max})$ ($n_2=1$), and $3$-intervening $(v_0,x_{\rm new})$ (weight $0$ in $S_{\rm BD}^{(5)}$), giving $S_{\rm BD}^{(5)}=5-10+8-2=+1$, with $r=\frac{1}{2}(\frac{11{,}630}{11{,}699}-1)=-\frac{69}{23{,}398}$ (check: $\sum_S q(S)r(S)=-\frac{1}{440}+\frac{3623}{70{,}194}\cdot\frac{21}{220}-\frac{69}{23{,}398}\cdot\frac{9}{10}=\frac{-11{,}699+25{,}361-13{,}662}{5{,}147{,}560}=0$).

   Combining the $Q_p$ and $Q_{\rm bipy}$ rows gives $q(Q_p)(-3)+q(Q_{\rm bipy})(-11)=-\frac{21}{20}+\frac{2h_i}{55f_i}$, equal to $-\frac{1003}{1100}$ at $i=0$ ($\frac{h_0}{f_0}=\frac{19}{5}$) and $-\frac{1099}{1100}$ at $i=1$ ($\frac{h_1}{f_1}=\frac{7}{5}$). Hence the passive conditional means are $-\frac{12}{440}-\frac{1003}{1100}+\frac{9}{10}=-\frac{43}{1100}$ ($i=0$) and $-\frac{12}{440}-\frac{1099}{1100}+\frac{9}{10}=-\frac{139}{1100}$ ($i=1$). Multiplying each branch by $r(S)\operatorname{Tr}[Z\rho]$ over common denominator $70{,}194\times 1100=77{,}213{,}400$ ($233{,}980\times 330=77{,}213{,}400$) yields slopes $\frac{15\cdot 70{,}194-3623\cdot 1003-621\cdot 330}{77{,}213{,}400}=\frac{1{,}052{,}910-3{,}633{,}869-204{,}930}{77{,}213{,}400}=-\frac{2{,}785{,}889}{77{,}213{,}400}$ ($i=0$) and $\frac{1{,}052{,}910-3{,}981{,}677-204{,}930}{77{,}213{,}400}=-\frac{3{,}133{,}697}{77{,}213{,}400}$ ($i=1$), whose difference is $-\frac{347{,}808}{77{,}213{,}400}=-\frac{14{,}492}{3{,}217{,}225}$ (in lowest terms, as $11{,}699$ is prime). $\blacksquare$

---

## 3. Infinite-horizon obstruction for global harmonic telescoping over full ideal support

Theorem 3 shows that decreasing $\lambda_4$ from $\frac{1}{2}$ to $\frac{1}{4}$ accommodates the step-5 growth of $H_{\rm foc}^{(5)}$ ($\max_{\mathcal U_5}H_{\rm foc}^{(5)}=\frac{13{,}640}{11{,}699}>1$) while maintaining strict complete positivity. A natural question is whether an appropriately chosen infinite retention schedule $(\lambda_n)_{n\ge 0}\subset(0,1)$ can sustain Theorem 2's linear harmonic-telescoping ansatz $r_P(S)=\frac{\theta}{\Lambda_{|P|}}[H(P+S)-H(P)]$ across **all** horizons $n=0,1,2,\dots$ over any strictly positive full-ideal-support growth law $q(P,r,S)>0$. We prove that the answer is **no**: a universal complete-positivity summability identity collides with the $\le 4(n-1)$ up-down diameter of $\mathcal U_n$ to force $H$ to be globally constant.

**Theorem 4 (Infinite-horizon obstruction for global harmonic telescoping over full ideal support).** *Let $q(P,r,S)>0$ be **any** all-horizon structural growth kernel with full downward-ideal support ($\sum_{S\subseteq P}q(P,r,S)=1$ for all marked finite partial orders $(P,r)$, $n=|P|\ge 0$), let $(\lambda_n)_{n\ge 0}\subset(0,1)$ be **any** stage retention sequence with $\Lambda_0=1$ and $\Lambda_n=\prod_{j=0}^{n-1}\lambda_j$, let $\theta>0$, and let $H:\bigcup_{n=0}^\infty\mathcal U_n\to\mathbb R$ be an unmarked function with stage step-oscillation*
$$
\Delta_n(H):=\max_{P\in\mathcal U_n,\,S\subseteq P}\bigl|H(P+S)-H(P)\bigr|\qquad (n\ge 0).
\tag{24}
$$
*Suppose $r_P(S):=\frac{\theta}{\Lambda_{|P|}}[H(P+S)-H(P)]$ satisfies Theorem 2's strict complete-positivity condition $|r_P(S)|<1-\lambda_{|P|}$ for every $n\ge 0$, $P\in\mathcal U_n$, and ideal $S\subseteq P$. Then:*

1. *(Universal CP summability identity and sub-harmonic decay.)* *At every stage $n\ge 0$, strict complete positivity is equivalent to*
   $$
   \theta\,\Delta_n(H)<\Lambda_n-\Lambda_{n+1},
   \tag{25}
   $$
   *which forces global summability $\sum_{n=0}^\infty\Delta_n(H)\le\frac{1-\Lambda_\infty}{\theta}\le\frac{1}{\theta}<\infty$ (where $\Lambda_\infty:=\lim_{n\to\infty}\Lambda_n\in[0,1)$) and*
   $$
   \liminf_{n\to\infty}n\,\Delta_n(H)=0.
   \tag{26}
   $$
2. *(Combinatorial up-down bridge diameter of $\mathcal U_n$.)* *For every integer $n\ge 1$ and every $P\in\mathcal U_n$, peeling non-minimal maximal elements connects $P$ to the $n$-antichain $A_n$ through at most $n-|\operatorname{Min}(P)|\le n-1$ two-birth bridges through $\mathcal U_{n+1}$, yielding*
   $$
   \bigl|H(P)-H(A_n)\bigr|\le 2\bigl(n-|\operatorname{Min}(P)|\bigr)\Delta_n(H)\le 2(n-1)\Delta_n(H),
   \tag{27a}
   $$
   $$
   \bigl|H(C_n)-H(A_n)\bigr|\le 2(n-1)\Delta_n(H),\qquad
   \max_{P_1,P_2\in\mathcal U_n}\bigl|H(P_1)-H(P_2)\bigr|\le 4(n-1)\Delta_n(H).
   \tag{27b}
   $$
3. *(Global harmonic collapse.)* *If $H$ is forward harmonic at all stages ($\sum_{S\subseteq P}q(P,r,S)H(P+S)=H(P)$ for all marked $(P,r)$, $n\ge 0$), then $H(P)=H(\varnothing)$ for **every** finite partial order $P\in\bigcup_{m=0}^\infty\mathcal U_m$, and hence $r_P(S)=0$ identically for all $(P,S)$.*

**Proof.**
1. Because $\Lambda_{n+1}=\lambda_n\Lambda_n$ and $\Lambda_n>0$, we have $1-\lambda_n=\frac{\Lambda_n-\Lambda_{n+1}}{\Lambda_n}$. Taking the maximum of $|r_P(S)|=\frac{\theta}{\Lambda_n}|H(P+S)-H(P)|$ over the finite set $\{(P,S):P\in\mathcal U_n,S\subseteq P\}$ shows that $\max_{P\in\mathcal U_n,S\subseteq P}|r_P(S)|<1-\lambda_n$ holds if and only if $\frac{\theta}{\Lambda_n}\Delta_n(H)<\frac{\Lambda_n-\Lambda_{n+1}}{\Lambda_n}$, proving (25). Since $(\Lambda_n)_{n\ge 0}$ is strictly decreasing in $(0,1]$, $\Lambda_\infty=\lim_{N\to\infty}\Lambda_N\in[0,1)$ exists, and telescoping (25) from $n=0$ to $N-1$ gives
   $$
   \theta\sum_{n=0}^{N-1}\Delta_n(H)<\sum_{n=0}^{N-1}(\Lambda_n-\Lambda_{n+1})=1-\Lambda_N\le 1\qquad (\forall N\ge 1).
   $$
   Letting $N\to\infty$ yields $\sum_{n=0}^\infty\Delta_n(H)\le\frac{1-\Lambda_\infty}{\theta}\le\frac{1}{\theta}<\infty$. If $\liminf_{n\to\infty}n\,\Delta_n(H)>0$, there would exist $c>0$ and $n_0\ge 1$ such that $\Delta_n(H)\ge\frac{c}{n}$ for all $n\ge n_0$; since the harmonic series diverges ($\sum_{k=1}^{2^m}\frac{1}{k}\ge 1+\frac{m}{2}\to\infty$), this contradicts $\sum_{n=0}^\infty\Delta_n(H)<\infty$, proving (26).

2. Fix $n\ge 1$ and $P\in\mathcal U_n$. Note $1\le|\operatorname{Min}(P)|\le n$, with $|\operatorname{Min}(P)|=n$ if and only if $P\cong A_n$ (for if $P$ contains any comparison $u\prec v$, then $v\notin\operatorname{Min}(P)$, so $|\operatorname{Min}(P)|\le n-1$). Suppose $P\not\cong A_n$. Then the non-minimal subset $P\setminus\operatorname{Min}(P)$ is finite and nonempty, so it contains an element $x$ maximal in $P\setminus\operatorname{Min}(P)$, which is automatically maximal in $P$ ($x\in\operatorname{Max}(P)\setminus\operatorname{Min}(P)$). Put $P':=P\setminus\{x\}$ ($|P'|=n-1$) and $I_x:=\operatorname{Pred}_P(x)=\{u\in P':u\prec_P x\}$, a nonempty downward-closed ideal of $P'$ such that $P=P'+x_{I_x}$. Because $x\in\operatorname{Max}(P)$ lies above no element of $P'$, $\operatorname{Pred}_{P'}(y)=\operatorname{Pred}_P(y)$ for every $y\in P'$, so $\operatorname{Min}(P')=\operatorname{Min}(P)$. Now define $Q_1:=P'+\varnothing=P'\sqcup A_1\in\mathcal U_n$ (adjoining an isolated vertex $z$ to $P'$), which satisfies
   $$
   \bigl|\operatorname{Min}(Q_1)\bigr|=\bigl|\operatorname{Min}(P')\bigr|+1=\bigl|\operatorname{Min}(P)\bigr|+1.
   $$
   In $P'$, both $I_x\subseteq P'$ and $\varnothing\subseteq P'$ are ideals; adjoining $x$ over $I_x$ and $z$ over $\varnothing$ in either order yields the **same** unmarked $(n+1)$-element partial order:
   $$
   P+\varnothing=(P'+x_{I_x})+z_\varnothing\cong (P'+z_\varnothing)+x_{I_x}=Q_1+I_x\in\mathcal U_{n+1}.
   \tag{28}
   $$
   Applying the triangle inequality across the two-edge bridge $P\to(P+\varnothing)\cong(Q_1+I_x)\leftarrow Q_1$ gives
   $$
   \bigl|H(P)-H(Q_1)\bigr|\le\bigl|H(P+\varnothing)-H(P)\bigr|+\bigl|H(Q_1+I_x)-H(Q_1)\bigr|\le 2\,\Delta_n(H).
   $$
   Repeating this step $k:=n-|\operatorname{Min}(P)|\le n-1$ times produces $P=Q_0,Q_1,\dots,Q_k\in\mathcal U_n$ with $|\operatorname{Min}(Q_j)|=|\operatorname{Min}(P)|+j$, ending at $|\operatorname{Min}(Q_k)|=n$, i.e., $Q_k\cong A_n$, and summing the $k$ bridge bounds yields (27a). Specializing to $P=C_n$ ($|\operatorname{Min}(C_n)|=1$) gives $|H(C_n)-H(A_n)|\le 2(n-1)\Delta_n(H)$, and for any $P_1,P_2\in\mathcal U_n$, $|H(P_1)-H(P_2)|\le|H(P_1)-H(A_n)|+|H(A_n)-H(P_2)|\le 4(n-1)\Delta_n(H)$, proving (27b).

3. Suppose $H$ is forward harmonic at every stage, and fix any $m\ge 0$, any $P_1,P_2\in\mathcal U_m$, and arbitrary markings $r^{(1)},r^{(2)}\in\{0,1\}^m$. Iterating $\sum_{S\subseteq Q}q(Q,r,S)H(Q+S)=H(Q)$ forward $n-m$ steps (for any integer $n>\max(m,1)$) expresses each $H(P_i)$ as a convex combination $H(P_i)=\sum_{Q\in\mathcal U_n}\mu_i^{(n)}(Q)H(Q)$ with $\mu_i^{(n)}(Q)\ge 0$ and $\sum_{Q\in\mathcal U_n}\mu_i^{(n)}(Q)=1$. Hence for all $n>\max(m,1)$,
   $$
   \min_{Q\in\mathcal U_n}H(Q)\le H(P_i)\le\max_{Q\in\mathcal U_n}H(Q)\implies\bigl|H(P_1)-H(P_2)\bigr|\le\max_{Q_1,Q_2\in\mathcal U_n}\bigl|H(Q_1)-H(Q_2)\bigr|\le 4(n-1)\Delta_n(H)
   $$
   by (27b). Taking $\liminf_{n\to\infty}$ of the right-hand side and invoking (26) ($\liminf_{n\to\infty}4(n-1)\Delta_n(H)=4\liminf_{n\to\infty}n\,\Delta_n(H)=0$) forces $|H(P_1)-H(P_2)|=0$, so $H$ is constant on every layer $\mathcal U_m$. Finally, for $P\in\mathcal U_m$, $H(P)=\sum_{S\subseteq P}q(P,r,S)H(P+S)=H_{\text{const}}(\mathcal U_{m+1})$ equates consecutive layers, so $H(P)=H(\varnothing)$ everywhere and $r_P(S)=0$ identically. $\blacksquare$

*Structural significance of Theorem 4.* Notice that Theorem 4 makes **no** assumption on the specific choice of positive growth weights $q(P,r,S)>0$, **no** restriction on how rapidly $\lambda_n\downarrow 0$, and **no** bound on how large $H$ might grow with $n$: the mere coexistence of (i) additive linear drift $r_P(S)=\frac{\theta}{\Lambda_n}[H(P+S)-H(P)]$, (ii) trace-preserving CPTP positivity $|r_P(S)|<1-\lambda_n=(\Lambda_n-\Lambda_{n+1})/\Lambda_n$, and (iii) eligibility of the empty ideal $S=\varnothing$ alongside arbitrary ideals $S=I_x$ (which bridges $\mathcal U_n$ to $A_n$ in $\le n-1$ steps) forces $\theta\Delta_n(H)$ to be summable, which is incompatible with a non-constant harmonic martingale as $n\to\infty$. Achieving genuine all-horizon ($N\to\infty$) two-way feedback over full ideal support therefore requires replacing **additive** reset-channel telescoping by **multiplicative** coherent Kraus amplitude superposition.

---

## 4. Constructive all-horizon projective two-way quantum-order instrument and asymptotic width dichotomy

### 4.1 All-horizon coherent structural superposition and non-abelian Clifford synthesis

To overcome Theorem 4's additive reset-channel obstruction across infinite growth horizons $N\to\infty$ without sacrificing complete-ideal support, proper-slot mark locality, entangled diamond commutation, or Kolmogorov prefix consistency, we replace additive potential telescoping by a coherent Kraus superposition of two distinct all-horizon admitted structural kernels.

Supply a qubit horizon carrier $\mathcal H_{\rm hor}=\mathbb C^2$ with standard basis $\{|0\rangle,|1\rangle\}$ and $X$-eigenbasis $|\pm\rangle:=\frac{1}{\sqrt 2}(|0\rangle\pm|1\rangle)$ ($X|\pm\rangle=\pm|\pm\rangle$, $Z|\pm\rangle=|\mp\rangle$, $Y|\pm\rangle=\mp i|\mp\rangle$). Let $q^{(+)}(P,r,S)>0$ and $q^{(-)}(P,r,S)>0$ be any two all-horizon ($n=|P|\ge 0$) structural kernels satisfying strict positivity, complete-row normalization $\sum_{S\subseteq P}q^{(\alpha)}(P,r,S)=1$, proper-slot mark locality, relabeling equivariance, and the scalar diamond identity (2) across all base sizes $|C|\ge 0$ (for instance, two distinct Theorem 1 scale sequences $(a_n^{(+)})$ and $(a_n^{(-)})$ extending Part A's seed, or two distinct Bernoulli transitive-percolation kernels below). Let $\{\varphi^{(+)}_{K,b}\}$ and $\{\varphi^{(-)}_{K,b}\}$ be real phase schedules indexed solely by the isomorphism class $K(S,r|_S)$ of the induced marked precursor $(S,\prec|_S,r|_S)$ and newborn bit $b\in\{0,1\}$.

For every marked finite partial order $(P,r)$ ($|P|=n\ge 0$), every downward-closed ideal $S\subseteq P$, and every newborn bit $b\in\{0,1\}$, define on $\mathcal H_{\rm hor}=\mathbb C^2$ the coherent Kraus operator and branch superoperator
$$
K^{P,r}_{S,b}:=\frac{1}{\sqrt 2}\Bigl(\sqrt{q^{(+)}(P,r,S)}\,e^{-i\varphi^{(+)}_{K(S,r|_S),b}/2}|+\rangle\langle +|+\sqrt{q^{(-)}(P,r,S)}\,e^{-i\varphi^{(-)}_{K(S,r|_S),b}/2}|-\rangle\langle -|\Bigr),
\tag{29}
$$
$$
\mathcal B^{P,r}_{S,b}(A):=K^{P,r}_{S,b}\,A\,\bigl(K^{P,r}_{S,b}\bigr)^\dagger,
\tag{30}
$$
together with:
- the **full-Choi-rank strictly completely positive one-step convex-damped variant** (for any stage retention $\eta_n\in(0,1)$) and the **diamond-commuting Choi-rank-$2$ dephased variant** ($\mathcal D_\eta(B):=\eta B+(1-\eta)\sum_{\alpha\in\{\pm\}}|\alpha\rangle\langle\alpha|B|\alpha\rangle\langle\alpha|$):
  $$
  \mathcal B^{P,r;(\eta)}_{S,b}(A):=\eta_{|P|}K^{P,r}_{S,b}A\bigl(K^{P,r}_{S,b}\bigr)^\dagger+(1-\eta_{|P|})\operatorname{Tr}\!\Bigl[\bigl(K^{P,r}_{S,b}\bigr)^\dagger K^{P,r}_{S,b}A\Bigr]\frac{I_{\rm hor}}{2},\qquad
  \widetilde{\mathcal B}^{P,r;(\eta)}_{S,b}:=\mathcal D_{\eta_{|P|}}\circ\mathcal B^{P,r}_{S,b};
  \tag{31}
  $$
- and the **non-abelian Clifford tensor synthesis** on $\mathcal H_Q:=\mathbb C^2_{\rm Cliff}\otimes\mathcal H_{\rm hor}$, pairing $K^{P,r}_{S,b}$ with the co-rotating three-axis Clifford unitary $U_{|P|,K(S,r|_S),b}=U_*\exp\bigl(-i\frac{\varphi_{K(S,r|_S),b}}{2}\Sigma_{|P|}\bigr)$ (`NW1-A` Eq. (11)) across all stages $n\ge 0$:
  $$
  \widehat K^{P,r}_{S,b}:=U_{|P|,K(S,r|_S),b}\otimes K^{P,r}_{S,b},\qquad
  \widehat{\mathcal B}^{P,r}_{S,b}(\widetilde A):=\widehat K^{P,r}_{S,b}\,\widetilde A\,\bigl(\widehat K^{P,r}_{S,b}\bigr)^\dagger.
  \tag{32}
  $$
*(Remark on finite-horizon vs. all-horizon Clifford coupling.)* If one alternatively runs Theorem 3's five-Kraus reset channel $\mathcal M_{\lambda_n}(r_P(S),\Sigma_n,U_{n,K,b})$ on $\mathbb C^2_{\rm Cliff}$ for $n\le 4$ ($q^{(+)}=q^{(-)}=q$ on $n\le 4$) and switches to unitary $\operatorname{Ad}_{U_{n,K,b}}$ ($r_P(S)=0$) for $n\ge 5$, trace preservation and Kolmogorov projectivity still hold across all $N\ge 1$, while diamond commutation holds up to $|C|\le 3$ (stopping at $|C|=4$ whenever $H_{\rm foc}^{(5)}(C+S)$ is not extended to $n=6$). By contrast, (32) achieves **unbroken all-horizon** ($|C|\ge 0$) entangled diamond commutation while retaining non-abelian three-axis $(Y,Z,X)$ Clifford phase dynamics at every stage $n\ge 0$.

**Theorem 5 (All-horizon Kolmogorov-projective two-way quantum-order instrument).** *Put $\bar q(P,r,S):=\frac{1}{2}[q^{(+)}(P,r,S)+q^{(-)}(P,r,S)]$ and $\Delta q(P,r,S):=q^{(+)}(P,r,S)-q^{(-)}(P,r,S)$. For **every** parent cardinality $n=|P|\ge 0$:*

1. *(Complete positivity, trace preservation, locality, and equivariance.)* *Each $\mathcal B^{P,r}_{S,b}$ (and $\widehat{\mathcal B}^{P,r}_{S,b}$) is a nonzero rank-$1$ completely positive map with single nonzero Choi eigenvalue $\bar q(P,r,S)>0$, while each $\mathcal B^{P,r;(\eta)}_{S,b}$ ($\eta_n\in(0,1)$) has strictly positive-definite full-rank Choi matrix $J(\mathcal B^{P,r;(\eta)}_{S,b})\succeq\frac{1-\eta_n}{4}\min\{q^{(+)}(P,r,S),q^{(-)}(P,r,S)\}I_4\succ 0$. All maps in (30)–(32) satisfy exact complete-row trace preservation*
   $$
   \sum_{S\subseteq P}\sum_{b\in\{0,1\}}\bigl(K^{P,r}_{S,b}\bigr)^\dagger K^{P,r}_{S,b}=I_{\rm hor},\qquad
   \sum_{S\subseteq P}\sum_{b\in\{0,1\}}\bigl(\widehat K^{P,r}_{S,b}\bigr)^\dagger\widehat K^{P,r}_{S,b}=I_{\rm Cliff}\otimes I_{\rm hor},
   \tag{33}
   $$
   *proper-slot mark locality, and relabeling equivariance.*
2. *(Exact $m$-step multiplication, all-horizon entangled diamond commutation, and Kolmogorov extension.)* *For any $m$-birth history $h=((S_0,b_0),\dots,(S_{m-1},b_{m-1}))$ ($m\ge 1$) from any marked base $(C,r)$ ($|C|=n\ge 0$), writing $W_{\rm str}^{(\alpha)}(h):=\prod_{j=0}^{m-1}q^{(\alpha)}(P_j,r_j,S_j)$ and $\Phi_h^{(\alpha)}:=\sum_{j=0}^{m-1}\varphi^{(\alpha)}_{K(S_j,r_j|_{S_j}),b_j}$ ($\alpha\in\{+,-\}$), the composed Kraus operators equal*
   $$
   K_h=2^{-m/2}\Bigl(\sqrt{W_{\rm str}^{(+)}(h)}\,e^{-i\Phi_h^{(+)}/2}|+\rangle\langle +|+\sqrt{W_{\rm str}^{(-)}(h)}\,e^{-i\Phi_h^{(-)}/2}|-\rangle\langle -|\Bigr),\qquad
   \widehat K_h=\Bigl(U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}\Bigr)\otimes K_h.
   \tag{34}
   $$
   *Consequently, for **every** base size $|C|=n\ge 0$, all ideals $S,T\subseteq C$, all bits $b,c\in\{0,1\}$, and any passive reference space $\mathcal H_{\rm ref}$, exact operator diamond commutation $K^{C+x_S,r+b_x}_{T,c}K^{C,r}_{S,b}=K^{C+y_T,r+c_y}_{S,b}K^{C,r}_{T,c}$ and $\widehat K^{C+x_S,r+b_x}_{T,c}\widehat K^{C,r}_{S,b}=\widehat K^{C+y_T,r+c_y}_{S,b}\widehat K^{C,r}_{T,c}$ (and exact entangled superoperator commutation for $\mathcal B$, $\widetilde{\mathcal B}^{(\eta)}$, and $\widehat{\mathcal B}$, together with all transported suffixes) hold without horizon restriction. For every initial state $\rho$, the $N$-step history distributions $\mathbb P_{N,\rho}(h_N)=\operatorname{Tr}[\mathcal B_{h_N}(\rho)]$ ($N\ge 1$) satisfy exact Kolmogorov prefix consistency and extend uniquely to $\mathbb P_{\infty,\rho}=\frac{1+\operatorname{Tr}[X\rho]}{2}\mathbb P_\infty^{(+)}+\frac{1-\operatorname{Tr}[X\rho]}{2}\mathbb P_\infty^{(-)}$.*
3. *(Simultaneous all-horizon `Quantum -> Order` coherence steering and `Order/Mark -> Quantum` phase and decoherence back-action.)* *At every stage $n\ge 0$ and input $\rho\in\mathcal D(\mathcal H_{\rm hor})$:*
   - *Summing $\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]$ over $b\in\{0,1\}$ gives the exact structural transition law*
     $$
     \mathbb P_\rho(S\mid P,r)=\bar q(P,r,S)+\frac{1}{2}\Delta q(P,r,S)\operatorname{Tr}[X\rho]=\bar q(P,r,S)+\Delta q(P,r,S)\operatorname{Re}\langle 0|\rho|1\rangle,
     \tag{35}
     $$
     *so off-diagonal computational-basis coherence $\langle 0|\rho|1\rangle$ steers order growth at every $n\ge 0$ where $q^{(+)}(P,r,\cdot)\ne q^{(-)}(P,r,\cdot)$, while $Z$-basis states $|0\rangle,|1\rangle$ yield the identical passive average $\bar q$.*
   - *Writing $\rho=\sum_{\alpha,\beta\in\{\pm\}}\rho_{\alpha\beta}|\alpha\rangle\langle\beta|$ ($\rho_{+-}=\frac{1}{2}\operatorname{Tr}[(Z-iY)\rho]$), the unselected one-step quantum channel $\mathcal E^{P,r}(\rho):=\sum_{S\subseteq P,b\in\{0,1\}}\mathcal B^{P,r}_{S,b}(\rho)$ preserves $X$-populations ($\langle\pm|\mathcal E^{P,r}(\rho)|\pm\rangle=\rho_{\pm\pm}$) and multiplies $\rho_{+-}$ by the complex Bhattacharyya–phase factor*
     $$
     \gamma(P,r):=\sum_{S\subseteq P}\sqrt{q^{(+)}(P,r,S)\,q^{(-)}(P,r,S)}\left(\frac{1}{2}\sum_{b=0}^1\exp\!\left[-\frac{i}{2}\Bigl(\varphi^{(+)}_{K(S,r|_S),b}-\varphi^{(-)}_{K(S,r|_S),b}\Bigr)\right]\right),
     \tag{36}
     $$
     *which imparts mark-dependent $(Z,Y)$-plane phase rotation whenever $\varphi^{(+)}_{K,b}-\varphi^{(-)}_{K,b}$ varies with $K(S,r|_S)$ (plus three-axis $(Y,Z,X)$ non-abelian rotation on $\mathbb C^2_{\rm Cliff}$ under $\widehat{\mathcal B}^{P,r}_{S,b}$) and satisfies strict Cauchy–Schwarz measurement back-action $|\gamma(P,r)|\le\sum_{S\subseteq P}\sqrt{q^{(+)}(P,r,S)q^{(-)}(P,r,S)}<1$ at every parent $(P,r)$ where $q^{(+)}(P,r,\cdot)\ne q^{(-)}(P,r,\cdot)$.*

**Proof.**
1. By orthogonality $\langle +|-\rangle=0$, $(K^{P,r}_{S,b})^\dagger K^{P,r}_{S,b}=\frac{1}{2}q^{(+)}(P,r,S)|+\rangle\langle +|+\frac{1}{2}q^{(-)}(P,r,S)|-\rangle\langle -|$. Thus $J(\mathcal B^{P,r}_{S,b})=(K^{P,r}_{S,b}\otimes I_2)|\Omega\rangle\langle\Omega|((K^{P,r}_{S,b})^\dagger\otimes I_2)$ is rank-$1$ positive semidefinite with single nonzero eigenvalue $\operatorname{Tr}[(K^{P,r}_{S,b})^\dagger K^{P,r}_{S,b}]=\bar q(P,r,S)>0$. For $\mathcal B^{P,r;(\eta)}_{S,b}$, $J(\mathcal B^{P,r;(\eta)}_{S,b})=\eta_n J(\mathcal B^{P,r}_{S,b})+\frac{1-\eta_n}{2}I_2\otimes((K^{P,r}_{S,b})^\dagger K^{P,r}_{S,b})^T\succeq\frac{1-\eta_n}{4}\min\{q^{(+)},q^{(-)}\}I_4\succ 0$, while both $(\mathcal B^{P,r;(\eta)}_{S,b})^\dagger(I_{\rm hor})$ and $(\widetilde{\mathcal B}^{P,r;(\eta)}_{S,b})^\dagger(I_{\rm hor})$ equal $(K^{P,r}_{S,b})^\dagger K^{P,r}_{S,b}$. Summing over $b\in\{0,1\}$ (factor $2$) and $S\subseteq P$ ($\sum_S q^{(\pm)}(P,r,S)=1$) yields $|+\rangle\langle +|+|-\rangle\langle -|=I_{\rm hor}$, and unitarity $U_{n,K,b}^\dagger U_{n,K,b}=I_{\rm Cliff}$ gives (33). Locality and equivariance hold because $q^{(\pm)}(P,r,S)$ are admitted kernels and $K(S,r|_S)$ reads $r$ solely on $S$.

2. Orthogonality of $|+\rangle\langle +|$ and $|-\rangle\langle -|$ makes multiplication of (29) across $j=0,\dots,m-1$ diagonal in $\{|+\rangle,|-\rangle\}$, yielding $K_h$ in (34) immediately, while `NW1-A` Eq. (20) yields $U_{n+m-1,K_{m-1},b_{m-1}}\cdots U_{n,K_0,b_0}=U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}$, proving $\widehat K_h$ in (34). On any diamond $(S,b),(T,c)$ over $(C,r)$ ($|C|=n\ge 0$), both $q^{(+)}$ and $q^{(-)}$ satisfy the scalar diamond identity $q^{(\alpha)}(C,r,S)q^{(\alpha)}(C+x_S,r+b_x,T)=q^{(\alpha)}(C,r,T)q^{(\alpha)}(C+y_T,r+c_y,S)$, and since $x\notin T$ and $y\notin S$, $(S,(r+c_y)|_S)=(S,r|_S)$ and $(T,(r+b_x)|_T)=(T,r|_T)$, equating $\Phi_h^{(+)}$, $\Phi_h^{(-)}$, and $\Phi_h$ on both paths. Thus $K_h$ and $\widehat K_h$ commute identically as operators for all $n\ge 0$, which immediately implies entangled superoperator commutation for $\mathcal B$ and $\widehat{\mathcal B}$, and also for $\widetilde{\mathcal B}^{(\eta)}$ because $\mathcal D_{\eta}$ commutes with every operator diagonal in $\{|+\rangle,|-\rangle\}$ ($\widetilde{\mathcal B}_h^{(\eta)}=\mathcal D_{\eta_{n,m}}\circ\mathcal B_h$ with $\eta_{n,m}=\prod_{j=0}^{m-1}\eta_{n+j}$). Equivariance preserves equality under any transported suffix. Taking traces in (34) gives $\mathbb P_{N,\rho}(h_N)=\langle +|\rho|+\rangle 2^{-N}W_{\rm str}^{(+)}(h_N)+\langle -|\rho|-\rangle 2^{-N}W_{\rm str}^{(-)}(h_N)=\frac{1+\operatorname{Tr}[X\rho]}{2}\mathbb P_N^{(+)}(h_N)+\frac{1-\operatorname{Tr}[X\rho]}{2}\mathbb P_N^{(-)}(h_N)$, which inherits Kolmogorov prefix marginalization and unique $\mathbb P_{\infty,\rho}$ extension directly from $\mathbb P_N^{(\pm)}$.

3. Using $|\pm\rangle\langle\pm|=\frac{1}{2}(I_{\rm hor}\pm X)$ and $X=|0\rangle\langle 1|+|1\rangle\langle 0|$ gives $\langle\pm|\rho|\pm\rangle=\frac{1}{2}(1\pm\operatorname{Tr}[X\rho])=\frac{1}{2}\pm\operatorname{Re}\langle 0|\rho|1\rangle$, so $\sum_{b=0}^1\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]=q^{(+)}(P,r,S)\langle +|\rho|+\rangle+q^{(-)}(P,r,S)\langle -|\rho|-\rangle$ equals (35). Similarly, $\langle +|\mathcal E^{P,r}(\rho)|-\rangle=\sum_{S,b}\langle +|K^{P,r}_{S,b}|+\rangle\rho_{+-}\langle -|(K^{P,r}_{S,b})^\dagger|-\rangle=\gamma(P,r)\rho_{+-}$ yields (36). By the triangle inequality and Cauchy–Schwarz on strictly positive probability vectors,
   $$
   |\gamma(P,r)|\le\sum_{S\subseteq P}\sqrt{q^{(+)}(P,r,S)\,q^{(-)}(P,r,S)}\le\left(\sum_{S\subseteq P}q^{(+)}(P,r,S)\right)^{1/2}\left(\sum_{S\subseteq P}q^{(-)}(P,r,S)\right)^{1/2}=1,
   $$
   with equality in Cauchy–Schwarz if and only if $q^{(+)}(P,r,\cdot)$ and $q^{(-)}(P,r,\cdot)$ are proportional (hence equal, as both sum to $1$). $\blacksquare$

### 4.2 Asymptotic poset-width dichotomy (`NG-02`)

Under `NG-02` of the [native geometry, gravity and measurement plan](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md), a sequential growth candidate whose antichain width $\operatorname{width}(P_N):=\max\{|A|:A\subseteq P_N\text{ is an antichain}\}$ remains bounded as $N\to\infty$ freezes into a quasi-one-dimensional chain structure and cannot serve a volume-filling spatial role. Theorem 5 allows us to compare two explicit all-horizon realizations of $(q^{(+)},q^{(-)})$ with sharply opposite asymptotic width regimes.

Recall from [Intrinsic finite-order likelihood for the Bernoulli-subset law](../track_b/native_theorem_package_v1/BERNOULLI_ORDER_LIKELIHOOD.md) §1 the parameter-$p$ ($p\in(0,1)$) Bernoulli-subset sequential rule: at the birth of vertex $n+1$ onto an $n$-element order $P$, select $R\subseteq P$ by including each $u\in P$ independently with probability $p$, and set $S=\operatorname{Down}_P(R):=\{v\in P:\exists u\in R\text{ with }v\preceq_P u\}$.

**Theorem 6 (`NG-02` asymptotic width-freezing vs. unbounded-width dichotomy).**
1. *(Summable maximal-deletion tails freeze into 1D ordinal chain tails.)* *Let $q^{(+)}$ and $q^{(-)}$ be two Theorem 1 maximal-deletion extensions ($0<a_n^{(-)}<a_n^{(+)}<1/M_n$ for $n\ge 4$) satisfying $\sum_{n=4}^\infty a_n^{(+)}M_n<\infty$ (for instance $a_n^{(\pm)}=\frac{c_\pm}{n^2 M_n}$ with $0<c_-<c_+<16$). Then for every initial state $\rho\in\mathcal D(\mathcal H_{\rm hor})$ and every $n_0\ge 4$, the probability under $\mathbb P_{\infty,\rho}$ that **every** birth $n\ge n_0$ chooses the full ideal $S_n=P_n$ satisfies*
   $$
   \mathbb P_{\infty,\rho}\!\left(\bigcap_{n=n_0}^\infty\{S_n=P_n\}\,\Big|\,P_{n_0},r_{n_0}\right)\ge\prod_{n=n_0}^\infty\bigl(1-a_n^{(+)}M_n\bigr)>0.
   \tag{37}
   $$
   *Moreover, $\mathbb P_{\infty,\rho}$-almost surely there exists a finite random index $N_*<\infty$ after which $P_N=P_{N_*}\oplus C_{N-N_*}$ for all $N\ge N_*$, so the asymptotic poset width freezes almost surely:*
   $$
   \mathbb P_{\infty,\rho}\!\left(\sup_{N\ge 1}\operatorname{width}(P_N)=\operatorname{width}(P_{N_*})<\infty\right)=1,
   \tag{38}
   $$
   *while finite-horizon chain-tail probabilities retain nonzero quantum coherence contrast (e.g., $\mathbb P_\rho(S_4=A_4\mid A_4)=1-\bar a_4 M_4-\frac{1}{2}(a_4^{(+)}-a_4^{(-)})M_4\operatorname{Tr}[X\rho]$).*
2. *(Bernoulli transitive-percolation sector has unbounded width with persistent quantum steering.)* *For each $p\in(0,1)$ and downward-closed ideal $S\subseteq P$ ($|P|=n\ge 0$), the Bernoulli-subset kernel has the exact closed form*
   $$
   q_p(P,S)=p^{|\operatorname{Max}(S)|}(1-p)^{|P|-|S|}>0,
   \tag{39}
   $$
   *which satisfies $\sum_{S\subseteq P}q_p(P,S)=1$, mark independence, relabeling equivariance, and exact scalar diamond commutation (2) for all $|C|\ge 0$. Fix $0<p_-<p_+<1$ and set $(q^{(+)},q^{(-)}):=(q_{p_+},q_{p_-})$ in Theorem 5. Then for every $\rho\in\mathcal D(\mathcal H_{\rm hor})$, every integer $k\ge 2$, and every horizon $N\ge k$:*
   - *(Uniform tail-antichain lower bound and pure-antichain exclusion.)* *The final $k$ vertices $V_{\rm tail}:=\{N-k+1,\dots,N\}$ form an antichain in $P_N$ with probability*
     $$
     \Pr_\rho\bigl(\operatorname{width}(P_N)\ge k\bigr)\ge\Pr_\rho(V_{\rm tail}\text{ is an antichain})=\frac{1+\operatorname{Tr}[X\rho]}{2}(1-p_+)^{\binom{k}{2}}+\frac{1-\operatorname{Tr}[X\rho]}{2}(1-p_-)^{\binom{k}{2}}\ge(1-p_+)^{\binom{k}{2}}>0,
     \tag{40}
     $$
     *while pure antichain collapse vanishes super-exponentially:*
     $$
     \Pr_\rho(P_N=A_N)=\frac{1+\operatorname{Tr}[X\rho]}{2}(1-p_+)^{\binom{N}{2}}+\frac{1-\operatorname{Tr}[X\rho]}{2}(1-p_-)^{\binom{N}{2}}\le(1-p_-)^{\binom{N}{2}}\xrightarrow{N\to\infty}0.
     \tag{41}
     $$
   - *(Exponentially fast width divergence across disjoint blocks.)* *Monotonicity $\operatorname{width}(P_n)\le\operatorname{width}(P_N)$ ($n\le N$) and $\lfloor N/k\rfloor$ disjoint size-$k$ birth blocks yield*
     $$
     \Pr_\rho\bigl(\operatorname{width}(P_N)\le k-1\bigr)=\Pr_\rho\!\left(\max_{1\le n\le N}\operatorname{width}(P_n)\le k-1\right)\le\Bigl(1-(1-p_+)^{\binom{k}{2}}\Bigr)^{\lfloor N/k\rfloor}\xrightarrow{N\to\infty}0,
     \tag{42}
     $$
     *whence $\mathbb P_{\infty,\rho}\bigl(\lim_{N\to\infty}\operatorname{width}(P_N)=+\infty\bigr)=1$.*
   - *(All-horizon quantum coherence contrast in width and comparable-pair density.)* *Between $|+\rangle$ and $|-\rangle$, $\Pr_{|+\rangle}(V_{\rm tail}\text{ antichain})-\Pr_{|-\rangle}(V_{\rm tail}\text{ antichain})=-\bigl[(1-p_-)^{\binom{k}{2}}-(1-p_+)^{\binom{k}{2}}\bigr]<0$ at every $N\ge k$, and the expected comparable-pair density $\rho_{\rm comp}(P_N):=\binom{N}{2}^{-1}|\{\prec_{P_N}\}|$ satisfies*
     $$
     \mathbb E_{|+\rangle}\bigl[\rho_{\rm comp}(P_N)\bigr]-\mathbb E_{|-\rangle}\bigl[\rho_{\rm comp}(P_N)\bigr]\ge\binom{N}{2}^{-1}\sum_{1\le i<j\le N}(p_+-p_-)(1-p_+)^{j-i-1}\ge\frac{2}{N}(p_+-p_-)>0
     \tag{43}
     $$
     *(with adjacent-cover density $\frac{1}{N-1}\sum_{j=1}^{N-1}\mathbf 1_{\{j\prec_{P_N}j+1\}}$ having exact horizon-uniform contrast $p_+-p_->0$ for all $N\ge 2$).*

**Proof.**
1. Under $q^{(\alpha)}$ ($\alpha\in\{+,-\}$), at every parent $(P_n,r_n)$ of size $n\ge 4$, $\mathbb P^{(\alpha)}(S_n\subsetneq P_n\mid P_n,r_n)=a_n^{(\alpha)}\Sigma_u(P_n,r_n)\le a_n^{(+)}M_n$, so $\mathbb P^{(\alpha)}(S_n=P_n\mid P_n,r_n)\ge 1-a_n^{(+)}M_n>0$. Multiplying conditional probabilities from $n_0$ to $N-1$ gives $\mathbb P^{(\alpha)}(\bigcap_{n=n_0}^{N-1}\{S_n=P_n\}\mid P_{n_0},r_{n_0})\ge\prod_{n=n_0}^{N-1}(1-a_n^{(+)}M_n)$. By elementary induction on finite products, $\prod_{j=1}^m(1-x_j)\ge 1-\sum_{j=1}^m x_j$ for $x_j\in[0,1]$ (since $(1-X)(1-x_{m+1})=1-X-x_{m+1}+Xx_{m+1}\ge 1-X-x_{m+1}$). Choosing $m_0\ge n_0$ such that $\sum_{n=m_0}^\infty a_n^{(+)}M_n\le\frac{1}{2}$ yields, for every $N>m_0$,
   $$
   \prod_{n=n_0}^{N-1}\bigl(1-a_n^{(+)}M_n\bigr)\ge\left(\prod_{n=n_0}^{m_0-1}\bigl(1-a_n^{(+)}M_n\bigr)\right)\left(1-\sum_{n=m_0}^{N-1}a_n^{(+)}M_n\right)\ge\frac{1}{2}\prod_{n=n_0}^{m_0-1}\bigl(1-a_n^{(+)}M_n\bigr)>0.
   $$
   Letting $N\to\infty$ by continuity from above of $\mathbb P_{\infty,\rho}=\frac{1+\langle X\rangle_\rho}{2}\mathbb P_\infty^{(+)}+\frac{1-\langle X\rangle_\rho}{2}\mathbb P_\infty^{(-)}$ proves (37). Furthermore, $\sum_{n=4}^\infty\mathbb P_{\infty,\rho}(S_n\subsetneq P_n)\le\sum_{n=4}^\infty a_n^{(+)}M_n<\infty$; hence by the first Borel–Cantelli lemma (if $E_{\rm io}:=\bigcap_{m=4}^\infty\bigcup_{n=m}^\infty\{S_n\subsetneq P_n\}$, then $\mathbb P_{\infty,\rho}(E_{\rm io})\le\sum_{n=m}^\infty a_n^{(+)}M_n\to 0$ as $m\to\infty$), almost surely only finitely many proper births occur. Letting $N_*\ge 1$ be the size immediately after the last proper birth ($N_*=1$ if none occur for $n\ge 1$), every subsequent step $n\ge N_*$ adjoins a universal top $P_{n+1}=P_n\oplus A_1$, giving $P_N=P_{N_*}\oplus C_{N-N_*}$. Since every element of $C_{N-N_*}$ is comparable to every element of $P_{N_*}$ and $\operatorname{width}(C_{N-N_*})=1\le\operatorname{width}(P_{N_*})$, $\operatorname{width}(P_N)=\operatorname{width}(P_{N_*})$ for all $N\ge N_*$, proving (38).

2. For any finite poset $P$ and downward ideal $S\subseteq P$, every $v\in S$ satisfies $v\preceq_P m$ for some $m\in\operatorname{Max}(S)$. Thus $\operatorname{Down}_P(R)=S$ holds if and only if $R\cap(P\setminus S)=\varnothing$ (probability $(1-p)^{|P|-|S|}$) and $\operatorname{Max}(S)\subseteq R$ (probability $p^{|\operatorname{Max}(S)|}$, with all elements of $S\setminus\operatorname{Max}(S)$ unconstrained), proving (39). Since $\bigcup_{S\subseteq P}\{R:\operatorname{Down}_P(R)=S\}=2^P$ is a partition, $\sum_{S\subseteq P}q_p(P,S)=1$. For any base $C$ ($|C|=n$) and ideals $S,T\subseteq C$, $|C+x_S|=n+1$ gives
   $$
   q_p(C,S)\,q_p(C+x_S,T)=p^{|\operatorname{Max}(S)|}(1-p)^{n-|S|}\,p^{|\operatorname{Max}(T)|}(1-p)^{(n+1)-|T|}=p^{|\operatorname{Max}(S)|+|\operatorname{Max}(T)|}(1-p)^{2n+1-|S|-|T|},
   $$
   which is manifestly symmetric in $S\leftrightarrow T$, proving (2) for all $|C|\ge 0$.

   As shown in [Bernoulli order likelihood](../track_b/native_theorem_package_v1/BERNOULLI_ORDER_LIKELIHOOD.md) §1, $P_N$ under $q_p$ is the transitive closure of independent forward $\operatorname{Bernoulli}(p)$ edges $\{E_{ij}:1\le i<j\le N\}$. In any forward DAG ($u\to v\implies u<v$), a directed path between two vertices $i<j$ in an interval $V=[a,b]\subseteq\{1,\dots,N\}$ can visit only intermediate vertices $i<v_1<\dots<v_s<j$, all of which lie inside $V$. Hence $V=[a,b]$ is an antichain in $P_N$ if and only if $E_{ij}=0$ for all $a\le i<j\le b$. Applying this to $V_{\rm tail}=[N-k+1,N]$ ($\binom{k}{2}$ independent edges) gives $\Pr_p(V_{\rm tail}\text{ is an antichain in }P_N)=(1-p)^{\binom{k}{2}}$, proving (40); applying it to $V=[1,N]$ ($\binom{N}{2}$ edges) proves (41).

   Because adjoining maximal births never creates comparisons between existing vertices, every antichain of $P_n$ ($n\le N$) remains an antichain of $P_N$, so $\operatorname{width}(P_n)$ is nondecreasing in $n$ and $\max_{1\le n\le N}\operatorname{width}(P_n)=\operatorname{width}(P_N)$. Partitioning $\{1,\dots,k\lfloor N/k\rfloor\}$ into $B:=\lfloor N/k\rfloor$ disjoint intervals $V_r=[(r-1)k+1,rk]$ ($1\le r\le B$), the edge sets $\mathcal E_r:=\{(i,j)\in V_r\times V_r:i<j\}$ are pairwise disjoint, hence independent under $\mathbb P_N^{(\pm)}$. If $\operatorname{width}(P_N)\le k-1$, none of $V_1,\dots,V_B$ can have all $\binom{k}{2}$ edges zero, so $\Pr_{p_\alpha}(\operatorname{width}(P_N)\le k-1)\le\bigl(1-(1-p_\alpha)^{\binom{k}{2}}\bigr)^B\le\bigl(1-(1-p_+)^{\binom{k}{2}}\bigr)^{\lfloor N/k\rfloor}$, proving (42). Since $\sum_{N=1}^\infty\bigl(1-(1-p_+)^{\binom{k}{2}}\bigr)^{\lfloor N/k\rfloor}\le k\sum_{B=0}^\infty\bigl(1-(1-p_+)^{\binom{k}{2}}\bigr)^B=k(1-p_+)^{-\binom{k}{2}}<\infty$, Borel–Cantelli implies $\liminf_{N\to\infty}\operatorname{width}(P_N)\ge k$ almost surely for every integer $k\ge 2$.

   Finally, couple $P_N^{(+)}$ and $P_N^{(-)}$ via independent $U_{ij}\sim\operatorname{Unif}[0,1]$ ($E_{ij}^{(\pm)}:=\mathbf 1_{\{U_{ij}\le p_\pm\}}$). For any $1\le i<j\le N$, $E_{ab}^{(-)}\le E_{ab}^{(+)}$ implies $\mathbf 1_{\{i\prec^{(-)}j\}}\le\mathbf 1_{\{i\prec^{(+)}j\}}$ everywhere, and on the event $\{p_-<U_{ij}\le p_+\}\cap\bigcap_{u=i+1}^{j-1}\{U_{iu}>p_+\}$ (probability $(p_+-p_-)(1-p_+)^{j-i-1}$), $E_{ij}^{(+)}=1$ forces $i\prec^{(+)}j$ while $E_{iw}^{(-)}=0$ for all $w\in\{i+1,\dots,j\}$ leaves vertex $i$ with no outgoing edge into $\{i+1,\dots,j\}$ in $E^{(-)}$, forcing $i\not\prec^{(-)}j$. Summing over $1\le i<j\le N$ (and isolating the $N-1$ adjacent pairs $j=i+1$ where $(1-p_+)^0=1$ and $i\prec i+1\iff E_{i,i+1}=1$) proves (43). $\blacksquare$

---

## 5. Imperfect-detector readout bounds, scope, and Status-M quarantine

### 5.1 Imperfect-detector $L^1$ lower bounds at five births and arbitrary horizons

Retain from `NW1-A` §4.3 (Proposition 1) the shared three-outcome erasure-and-confusion readout channel $\xi=(f,n,e_{\rm det})\in\mathcal C:=[f_-,f_+]\times[n_-,n_+]\times[e_-,e_+]\subseteq[0,1]^3$ ($e_+<1$, $f_++n_+<1$), which maps any binary native indicator $B\in\{0,1\}$ with setting probabilities $p_\pm=\mathbb P_\pm(B=1)$ and native contrast $\Delta:=p_+-p_-$ to reported distributions $\mu_\pm(\xi)$ on $\{0,1,\perp\}$ satisfying
$$
\inf_{\xi\in\mathcal C}\bigl\|\mu_+(\xi)-\mu_-(\xi)\bigr\|_1=2|\Delta|(1-e_+)(1-f_+-n_+)>0\qquad (\Delta\ne 0).
\tag{44}
$$

**Corollary 1 (Uniform faulty-detector $L^1$ lower bounds at five births and all horizons $N\ge 2$).** *Across the entire detector uncertainty box $\mathcal C$:*
1. *(Five-birth chain continuation and diamond-top readouts, Theorem 3.)* *Comparing $|0\rangle\langle 0|$ against $|1\rangle\langle 1|$ ($\Delta\langle Z\rangle=+2$) at step $5$:*
   - *For $B=\mathbf 1_{\{Q=C_5\}}$ conditional on $(C_4,r)$, $\Delta=+\frac{1}{10}$ by (20), giving $\inf_{\xi\in\mathcal C}\|\mu_{|0\rangle}(\xi)-\mu_{|1\rangle}(\xi)\|_1=\frac{1}{5}(1-e_+)(1-f_+-n_+)>0$.*
   - *For $B=\mathbf 1_{\{Q=E_{\text{diamond}}\oplus A_1\}}$ conditional on $(E_{\text{diamond}},r)$, $\Delta=2\cdot\frac{9}{10}(-\frac{69}{23{,}398})=-\frac{621}{116{,}990}$, giving $\inf_{\xi\in\mathcal C}\|\mu_{|0\rangle}(\xi)-\mu_{|1\rangle}(\xi)\|_1=\frac{621}{58{,}495}(1-e_+)(1-f_+-n_+)>0$.*
2. *(Horizon-uniform all-$N$ width and link readouts, Theorems 5 and 6.)* *Under the coherent Bernoulli instrument ($0<p_-<p_+<1$), comparing $|+\rangle\langle +|$ against $|-\rangle\langle -|$ ($\Delta\langle X\rangle=+2$):*
   - *For the tail-$k$ antichain indicator $B_{N,k}=\mathbf 1_{\{V_{\rm tail}\text{ is an antichain in }P_N\}}$ at **every** horizon $N\ge k\ge 2$, $|\Delta|=(1-p_-)^{\binom{k}{2}}-(1-p_+)^{\binom{k}{2}}>0$, giving the $N$-independent lower bound*
     $$
     \inf_{\xi\in\mathcal C}\bigl\|\mu_{|+\rangle}^{(N)}(\xi)-\mu_{|-\rangle}^{(N)}(\xi)\bigr\|_1=2\Bigl[(1-p_-)^{\binom{k}{2}}-(1-p_+)^{\binom{k}{2}}\Bigr](1-e_+)(1-f_+-n_+)>0.
     \tag{45}
     $$
   - *For the adjacent-birth causal cover indicator $B_N^{\rm cov}=\mathbf 1_{\{N-1\prec_{P_N}N\}}$ at **every** horizon $N\ge 2$, $\Delta=p_+-p_->0$, giving $\inf_{\xi\in\mathcal C}\|\mu_{|+\rangle}^{(N)}(\xi)-\mu_{|-\rangle}^{(N)}(\xi)\|_1=2(p_+-p_-)(1-e_+)(1-f_+-n_+)>0$.*

**Proof.** Substitute each exact native contrast $\Delta$ from Theorem 3(3) and Theorem 6(2) directly into (44). $\blacksquare$

### 5.2 Null controls and strict separation of ingredients

1. **Explicit null controls:**
   - *Equal-kernel passive-order control ($q^{(+)}=q^{(-)}$ in Theorem 5, or $\theta=0$ in Theorem 3):* $\Delta q\equiv 0$ eliminates all `Quantum -> Order` contrasts in (20)–(21) and (40)–(45) while leaving precursor-mark phase rotations $\varphi^{(+)}_{K,b}-\varphi^{(-)}_{K,b}$ (and Clifford $\varphi_{K,b}$) active.
   - *Equal-phase control ($\varphi^{(+)}_{K,b}=\varphi^{(-)}_{K,b}$ and $\varphi_{K,b}=0$):* Eliminates mark-dependent phase rotation in (36) while leaving Cauchy–Schwarz measurement decoherence $\sum_S\sqrt{q^{(+)}(S)q^{(-)}(S)}<1$ and all `Quantum -> Order` steering intact.
   - *Incoherent computational-basis control ($\rho\in\{|0\rangle\langle 0|,|1\rangle\langle 1|,I_{\rm hor}/2\}$ in Theorem 5):* Since $\operatorname{Tr}[X\rho]=2\operatorname{Re}\langle 0|\rho|1\rangle=0$, every structural transition collapses to the passive average $\bar q(P,r,S)$.
   - *Degenerate detector boundary ($e_{\rm det}=1$ or $f+n=1$):* Collapses $\|\mu_+(\xi)-\mu_-(\xi)\|_1$ to $0$, confirming sharpness of $e_+<1$ and $f_++n_+<1$.

2. **Native vs. externally supplied ingredients:**
   - *Supplied by the admitted sequential growth framework ([Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix) and [Bernoulli order likelihood](../track_b/native_theorem_package_v1/BERNOULLI_ORDER_LIKELIHOOD.md)):* Binary-marked finite strict partial orders, downward-closed precursor ideals, append-only maximal births, fair newborn bits, the four-birth seed kernel $q(P,r,S)$, the maximal-deletion recursion $u(P,r,S)$, and the forward Bernoulli-subset order family $q_p(P,S)$.
   - *Externally supplied mathematical structures and law choices:* The complex Hilbert spaces $\mathcal H_{\rm hor}=\mathbb C^2$ and $\mathbb C^2_{\rm Cliff}$, Pauli and Clifford operators $(X,Y,Z,U_*)$, scale schedules $(a_n)_{n\ge 4}$ (and $a_4=\frac{1}{10}$), retention schedule $(\lambda_n)$ ($\lambda_4=\frac{1}{4}$) and coupling $\theta=\frac{1}{32}$, the six-class five-birth harmonic continuation $H_{\rm foc}^{(5)}$, Bernoulli parameters $(p_+,p_-)$, precursor-local phase schedules $\{\varphi^{(\pm)}_{K,b},\varphi_{K,b}\}$, Kraus superposition operators $K^{P,r}_{S,b}$, Benincasa–Dowker action coefficients $5-2n_0+4n_1-2n_2$, trace probability functional, and erasure-and-confusion readout model $\mathcal C$.

### 5.3 Scope limits and Status-M quarantine

1. **Strict quarantine of Status-M ontology:** All Status-M commitments in `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, and `FALSIFICATION_LEDGER.md` remain strictly outside every definition, theorem, equation, and inference of this package.
2. **No derivation of continuum manifold dimension or Lorentzian geometry:** Theorem 6 resolves the discrete `NG-02` width-freezing vs. unbounded-width dichotomy, proving that summable maximal-deletion schedules freeze into finite-width ordinal chains whereas fixed-$p$ Bernoulli transitive percolation sustains $\operatorname{width}(P_N)\to\infty$. Unbounded discrete antichain width is only a necessary anti-freezing condition—**not** a derivation of a $3+1$-dimensional continuum Lorentzian manifold, metric tensor, causal cone structure, or Myrheim–Meyer manifold dimension (indeed, fixed-$p$ transitive percolation is well known to exhibit post-percolation layer/transitivity saturation rather than faithful $3+1$D manifold geometry).
3. **No derivation of Born's rule, General Relativity, clocks, or physical constants:** Complex Hilbert-space carriers, CPTP trace rules, Benincasa–Dowker interval-action weights, and step indices $n$ are conditional discrete mathematical constructs; step $n$ is a combinatorial birth count rather than proper time, and neither $\hbar$, $c$, $G$, Einstein's field equations, nor Born's rule is derived.

## Scientific review

All-Horizon Two-Way Feedback Author derived the self-contained inductive maximal-deletion sequential growth extension and Kolmogorov cylinder-set projectivity across all finite and countably infinite horizons, the unique-top sum identity and explicit parent-four bound $M_4<4$ across all 16 unmarked four-poset classes, the generalized retention-$\lambda_n$ five-Kraus co-rotating CPTP instrument and $4\times 4$ Choi spectrum, the nonnegative six-class five-birth harmonic continuation $H_{\rm foc}^{(5)}$ across all 63 five-posets with exact `5 -> 4` prefix consistency and step-5 chain and Benincasa–Dowker action contrasts, the infinite-horizon harmonic collapse obstruction ($\sum_{n=0}^\infty\Delta_n(H)\le\frac{1}{\theta}<\infty$), the all-horizon Kolmogorov-projective coherent superposition instrument and optional Clifford tensor synthesis, the `NG-02` asymptotic poset-width dichotomy between summable maximal-deletion freezing and Bernoulli transitive percolation, imperfect-detector $L^1$ lower bounds, and null controls. Independent All-Horizon Feedback Reviewer independently verified the all-horizon induction and ratio-diamond proof, all 16 $\mathcal U_4$ rational sums and upper bounds, $4\times 4$ Choi eigenvalues and superoperator compositions, maximal-deletion parent reconstruction on $\mathcal S_6$ and root-mark cancellations on $E_{\text{asym-fork}}$ and $E_{\text{diamond}}$, five-birth chain and Benincasa–Dowker action contrasts, the $4(n-1)\Delta_n(H)$ peeling bridge and infinite-horizon collapse proof, coherent Kraus and dephasing diamond commutation, Borel–Cantelli chain-tail freezing and Bernoulli width-divergence bounds, detector bounds, relative links, and Status-M quarantine boundaries. Prospective protocol SHA-256 ee4b2f455cbcd4079578b7bd6182d19f11fa2ce4b242c5d674510650ec68b317; accepted author report SHA-256 81e9abcd9c4e6946b522353c98271b36964eba943636a9e3588a7c2765c34254; independent scientific review SHA-256 271b4eaae8239d9a85ca69487f475807d576c60f63991691e67d2ea16a3beaa0.
