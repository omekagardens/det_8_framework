# Intrinsic causal resolvent propagators, Pauli–Jordan commutator algebra, and microcausality across discrete causal horizons

**Decision.** Replacing supplied continuum cavity backgrounds with native, background-free causal poset geometry establishes an exact operator-algebraic causal propagator theory directly on finite causal orders $P = (V, \prec)$ across arbitrary discrete horizons $N \ge 1$. The unipotent operator $D_\mu(P) = I - \mu C_P$ is unconditionally invertible with $\det(D_\mu(P)) = 1$, and generates the retarded Green operator resolvent $G_R(P) = D_\mu(P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k$, which is strictly nilpotent with $\det(G_R(P)) = 0$ ($G_R(P)^N = 0$), strictly positive on timelike-separated pairs, and supported exclusively on causal relations, while the discrete Pauli–Jordan commutator $\Delta(P) = G_R(P) - G_A(P)$ satisfies exact discrete microcausality across all spacelike-incomparable events ($[\phi(u), \phi(v)] = i\Delta(P)_{uv}\mathbf 1$), order-convex restriction invariance, and positive-semidefinite Sorkin–Johnston bosonic state attachment ($W_{\rm SJ} = \frac{1}{2}(\lvert M\rvert + M)$ with $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(P)$). Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## 1. Finite Poset Causal Incidence Matrix, Acyclicity, and Polynomial Nilpotency

Let $P = (V, \prec)$ denote a finite strict partial order (causal poset) where $V$ is a finite set of $N = \lvert V\rvert \ge 1$ discrete spacetime events and $\prec$ is a strict partial order relation satisfying:
1. **Irreflexivity**: For every $u \in V$, $u \not\prec u$.
2. **Transitivity**: For all $u, v, w \in V$, if $u \prec v$ and $v \prec w$, then $u \prec w$.
3. **Acyclicity**: There exist no directed cycles; for all $k \ge 1$, $u_0 \prec u_1 \prec \dots \prec u_k \implies u_k \not\prec u_0$.

Two distinct events $u, v \in V$ are:
- **Causally related (timelike)** if either $v \prec u$ ($v$ is in the causal past of $u$) or $u \prec v$ ($u$ is in the causal past of $v$).
- **Incomparable (spacelike)**, denoted $u \parallel v$, if neither $v \prec u$ nor $u \prec v$ holds.

### 1.1 Natural Enumeration and Strict Topological Triangularity

By the topological sorting theorem for finite directed acyclic graphs, every finite poset admits at least one linear extension (topological sort) labeling the vertices $V = \{0, 1, \dots, N-1\}$ such that:
$$
v \prec u \implies v < u \quad (\text{in the natural order of integers}).
$$
In any such topological labeling, we define the causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$ by:
$$
(C_P)_{uv} := \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise.} \end{cases}
$$
Under this convention, row index $u$ corresponds to the target (future) event, while column index $v$ corresponds to the source (past) event.

**Proposition 1.1 (Strict Lower Triangularity).** *In any topological sort of $P$, $C_P$ is strictly lower triangular:*
$$
(C_P)_{uv} = 0 \quad \text{for all } u \le v.
$$
*In particular, the main diagonal vanishes identically: $(C_P)_{uu} = 0$ for all $u \in \{0, \dots, N-1\}$.*

*Proof.* If $(C_P)_{uv} = 1$, then by definition $v \prec u$. By the topological sorting property, $v \prec u \implies v < u$. Thus $(C_P)_{uv}$ can only be non-zero when $u > v$, which proves that all diagonal entries ($u = v$) and all upper-triangular entries ($u < v$) are identically zero. $\blacksquare$

### 1.2 Powers of $C_P$ as $k$-Chain Counting Operators

For an integer $k \ge 1$, a strict $k$-chain from $v$ to $u$ in $P$ is an ordered sequence of $k+1$ events:
$$
v = x_0 \prec x_1 \prec x_2 \prec \dots \prec x_k = u.
$$
The length of this chain is $k$ (the number of strict causal relations / links traversed).

**Theorem 1.2 (Incidence Power Chain Representation).** *For every integer $k \ge 1$ and any pair of events $u, v \in V$, the matrix entry $(C_P^k)_{uv}$ equals the exact number of distinct strict $k$-chains connecting past event $v$ to future event $u$:*
$$
(C_P^k)_{uv} = \lvert \{ (x_0, x_1, \dots, x_k) \in V^{k+1} : v = x_0 \prec x_1 \prec \dots \prec x_k = u \} \rvert.
$$

*Proof.* We proceed by induction on $k \ge 1$.
- *Base case ($k = 1$)*: By definition, $(C_P)_{uv} = 1$ if $v \prec u$ and $0$ otherwise. This is exactly the count of 1-chains $v = x_0 \prec x_1 = u$.
- *Inductive step*: Assume the theorem holds for $k \ge 1$. By matrix multiplication:
  $$
  (C_P^{k+1})_{uv} = \sum_{w=0}^{N-1} (C_P)_{uw} (C_P^k)_{wv}.
  $$
  Each term in the sum is non-zero if and only if both $(C_P^k)_{wv} > 0$ and $(C_P)_{uw} = 1$. The factor $(C_P^k)_{wv}$ counts the number of $k$-chains $v = x_0 \prec \dots \prec x_k = w$, and $(C_P)_{uw} = 1$ requires $w \prec u$. Appending $x_{k+1} = u$ to each $k$-chain terminating at $w$ produces a unique $(k+1)$-chain terminating at $u$. Summing over all possible penultimate vertices $w$ enumerates every strict $(k+1)$-chain from $v$ to $u$ without omission or duplication. Hence the identity holds for $k+1$. $\blacksquare$

### 1.3 Polynomial Nilpotency and Poset Height

Let $h(P)$ denote the height of the poset $P$, defined as the maximum length $k$ of any strict chain in $P$:
$$
h(P) := \max \{ k \in \mathbb{N} : \exists x_0 \prec x_1 \prec \dots \prec x_k \text{ in } P \}.
$$
Since $P$ has $N$ distinct elements and all elements in a strict chain are distinct, the maximum possible chain length is at most $N - 1$. Therefore:
$$
0 \le h(P) \le N - 1.
$$

**Corollary 1.3 (Exact Polynomial Nilpotency).** *The causal incidence matrix $C_P$ is strictly nilpotent with nilpotency degree at most $h(P) + 1 \le N$:*
$$
C_P^k = 0 \quad \text{for all } k \ge h(P) + 1.
$$
*In particular, $C_P^N = 0$ holds unconditionally for every finite poset of cardinality $N$.*

*Proof.* If $k \ge h(P) + 1$, there exist no strict $k$-chains in $P$. By Theorem 1.2, $(C_P^k)_{uv} = 0$ for all $u, v \in V$. Hence $C_P^k$ is the zero matrix. Since $h(P) \le N - 1$, $h(P) + 1 \le N$, which ensures $C_P^N = 0$. $\blacksquare$

---

## 2. Background-Free Retarded Green Operator Resolvent

In continuum field theory, retarded Green functions $G_R(x, y)$ satisfy the wave equation $(\Box_x - m^2)G_R(x, y) = \delta^4(x - y)$ with support restricted to the causal future light cone of $y$. In native poset geometry, there is no smooth differential operator $\Box_x$ and no background metric. Instead, causal propagation is defined directly through the incidence algebra of the discrete order.

### 2.1 Resolvent Definition and Unconditional Invertibility

For a propagation coupling parameter $\mu > 0$ (or arbitrary $\mu \in \mathbb{C}$), consider the unipotent linear operator:
$$
D_\mu(P) := I - \mu C_P.
$$

**Theorem 2.1 (Unconditional Invertibility of $I - \mu C_P$).** *For any finite poset $P$ of cardinality $N$ and any coupling $\mu \in \mathbb{C}$, the operator $I - \mu C_P$ is unconditionally invertible with determinant:*
$$
\det(I - \mu C_P) = 1.
$$
*Its exact algebraic inverse is given by the finite, terminating Neumann polynomial series:*
$$
(I - \mu C_P)^{-1} = \sum_{k=0}^{N-1} \mu^k C_P^k = I + \mu C_P + \mu^2 C_P^2 + \dots + \mu^{N-1} C_P^{N-1}.
$$

*Proof.* In any topological sort of $P$, $C_P$ is strictly lower triangular with all diagonal entries $(C_P)_{uu} = 0$. Consequently, the matrix $I - \mu C_P$ is lower triangular with diagonal entries all identically equal to $1$:
$$
(I - \mu C_P)_{uu} = 1 - \mu \cdot 0 = 1.
$$
The determinant of a triangular matrix is the product of its diagonal entries:
$$
\det(I - \mu C_P) = \prod_{u=0}^{N-1} 1 = 1 \ne 0.
$$
Because the determinant is identically 1, $I - \mu C_P$ is invertible for all $\mu \in \mathbb{C}$.

To confirm the explicit formula for the inverse, multiply $I - \mu C_P$ by the finite sum $\sum_{k=0}^{N-1} \mu^k C_P^k$:
$$
(I - \mu C_P) \left( \sum_{k=0}^{N-1} \mu^k C_P^k \right) = \sum_{k=0}^{N-1} \mu^k C_P^k - \sum_{k=0}^{N-1} \mu^{k+1} C_P^{k+1} = I - \mu^N C_P^N.
$$
By Corollary 1.3, $C_P^N = 0$. Therefore:
$$
(I - \mu C_P) \left( \sum_{k=0}^{N-1} \mu^k C_P^k \right) = I - 0 = I.
$$
By uniqueness of the matrix inverse, $(I - \mu C_P)^{-1} = \sum_{k=0}^{N-1} \mu^k C_P^k$. $\blacksquare$

### 2.2 Retarded Green Operator Definition and Entrywise Representation

**Definition 2.2 (Background-Free Retarded Green Operator).** *The background-free retarded Green operator $G_R(P)$ associated with poset $P$ and coupling $\mu > 0$ is defined as the strictly off-diagonal resolvent:*
$$
G_R(P) := (I - \mu C_P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k = \mu C_P + \mu^2 C_P^2 + \dots + \mu^{N-1} C_P^{N-1}.
$$

Combining Definition 2.2 with Theorem 1.2 yields the explicit combinatorial formula:
$$
(G_R(P))_{uv} = \sum_{k=1}^{N-1} \mu^k \, \lvert \{ (x_0, \dots, x_k) \in V^{k+1} : v = x_0 \prec x_1 \prec \dots \prec x_k = u \} \rvert.
$$

### 2.3 Exact Positivity and Causal Support

**Theorem 2.3 (Causal Support and Strict Positivity of $G_R$).** *For every finite poset $P = (V, \prec)$ and any coupling $\mu > 0$:*
1. **Diagonal Vanishing**: $(G_R(P))_{uu} = 0$ for all $u \in V$.
2. **Causal Vanishing**: If $v \not\prec u$, then $(G_R(P))_{uv} = 0$.
3. **Strict Positivity on Timelike Past-to-Future Pairs**:
   $$
   (G_R(P))_{uv} > 0 \iff v \prec u.
   $$

*Proof.*
1. For each $k \ge 1$, $(C_P^k)_{uu}$ counts strict $k$-chains from $u$ to $u$. By irreflexivity and acyclicity, no such chain can exist. Hence $(C_P^k)_{uu} = 0$ for all $k \ge 1$, which implies $(G_R(P))_{uu} = \sum_{k=1}^{N-1} \mu^k \cdot 0 = 0$.
2. Suppose $v \not\prec u$. If there existed a strict $k$-chain $v = x_0 \prec x_1 \prec \dots \prec x_k = u$ for some $k \ge 1$, then by transitivity of $\prec$ we would have $v \prec u$, contradicting the hypothesis. Therefore, no $k$-chain connects $v$ to $u$, so $(C_P^k)_{uv} = 0$ for all $k \ge 1$. Thus $(G_R(P))_{uv} = 0$.
3. For the forward implication: If $(G_R(P))_{uv} > 0$, then at least one term in the sum must be strictly positive, so $(C_P^k)_{uv} \ge 1$ for some $k \ge 1$. Hence there exists a $k$-chain from $v$ to $u$, which by transitivity proves $v \prec u$.
For the reverse implication: If $v \prec u$, then the 1-chain $v \prec u$ exists, so $(C_P)_{uv} = 1$. Since $\mu > 0$, the first-order term contributes $\mu (C_P)_{uv} = \mu > 0$. Every higher-order term $\mu^k (C_P^k)_{uv} \ge 0$ because all entries of $C_P^k$ are nonnegative integers. Therefore:
$$
(G_R(P))_{uv} = \mu (C_P)_{uv} + \sum_{k=2}^{N-1} \mu^k (C_P^k)_{uv} \ge \mu > 0.
$$
This establishes $(G_R(P))_{uv} > 0 \iff v \prec u$. $\blacksquare$

**Remark 2.4 (Resolution of the QR-05 Sign Cancellation Defect).** *In earlier heuristic causal operator designs (such as binomial-layer d'Alembertians with alternating negative coefficients), higher-layer subtractions caused accidental zero-crossings inside the causal cone (for instance, vanishing propagation between endpoints of a 3-chain). In the resolvent Green operator $G_R(P)$, all coefficients $\mu^k$ are strictly positive for $\mu > 0$. Because each term $\mu^k C_P^k$ has strictly nonnegative entries, destructive interference or accidental cancellations within the causal cone are mathematically impossible.*

---

## 3. Advanced Green Operator

In complete duality to the retarded Green operator, the advanced Green operator propagates influence backward along the causal order (from future to past).

**Definition 3.1 (Advanced Green Operator).** *The discrete advanced Green operator $G_A(P)$ is defined as the matrix transpose of the retarded Green operator:*
$$
G_A(P) := G_R(P)^T = \sum_{k=1}^{N-1} \mu^k (C_P^T)^k.
$$

**Proposition 3.2 (Properties of the Advanced Green Operator).** *For every finite poset $P = (V, \prec)$ and any $\mu > 0$:*
1. **Entrywise Identity**: $(G_A(P))_{uv} = (G_R(P))_{vu}$.
2. **Diagonal Vanishing**: $(G_A(P))_{uu} = (G_R(P))_{uu} = 0$ for all $u \in V$.
3. **Past Causal Support**:
   $$
   (G_A(P))_{uv} > 0 \iff u \prec v.
   $$
4. **Vanishing on Non-Predecessor Pairs**: If $u \not\prec v$, then $(G_A(P))_{uv} = 0$.

*Proof.*
1. By matrix transposition, the $(u, v)$ entry of $G_R(P)^T$ is $(G_R(P))_{vu}$.
2. Vanishing on the diagonal follows immediately from $(G_R(P))_{uu} = 0$.
3. By Theorem 2.3, $(G_R(P))_{vu} > 0 \iff u \prec v$. Since $(G_A(P))_{uv} = (G_R(P))_{vu}$, this translates to $(G_A(P))_{uv} > 0 \iff u \prec v$.
4. If $u \not\prec v$, then $(G_R(P))_{vu} = 0$, so $(G_A(P))_{uv} = 0$. $\blacksquare$

---

## 4. Discrete Pauli–Jordan Commutator Algebra and Exact Discrete Microcausality

In relativistic quantum field theory, the Pauli–Jordan distribution $\Delta(x, y)$ is defined by the difference between retarded and advanced Green functions:
$$
\Delta(x, y) = G_R(x, y) - G_A(x, y).
$$
Microcausality requires that the commutator of two spacelike-separated field operators vanishes identically:
$$
[\phi(x), \phi(y)] = i \Delta(x, y) = 0 \quad \text{for all } (x - y)^2 > 0.
$$

### 4.1 Algebraic Definition and Symmetries

**Definition 4.1 (Discrete Pauli–Jordan Commutator Operator).** *The discrete Pauli–Jordan commutator operator $\Delta(P) \in \mathbb{R}^{N \times N}$ is defined by:*
$$
\Delta(P) := G_R(P) - G_A(P) = G_R(P) - G_R(P)^T.
$$
*The corresponding complex Hermitian commutator operator $M(P) \in \mathbb{C}^{N \times N}$ is:*
$$
M(P) := i \Delta(P) = i (G_R(P) - G_A(P)).
$$

**Proposition 4.2 (Algebraic Symmetries).**
1. $\Delta(P)$ is a purely real, skew-symmetric matrix:
   $$
   \Delta(P)^T = \left(G_R - G_R^T\right)^T = G_R^T - G_R = -\Delta(P).
   $$
2. $M(P)$ is a complex Hermitian matrix:
   $$
   M(P)^\dagger = \left(i \Delta(P)\right)^\dagger = -i \Delta(P)^T = -i (-\Delta(P)) = i \Delta(P) = M(P).
   $$

### 4.2 The Theorem of Exact Discrete Microcausality

We now state and prove the central causality theorem on discrete posets.

**Theorem 4.3 (Exact Discrete Microcausality).** *Let $P = (V, \prec)$ be any finite partial order, $\mu > 0$, and let $u, v \in V$ be arbitrary events. Then the discrete Pauli–Jordan commutator $\Delta(P)_{uv}$ satisfies:*
1. **Timelike Past-to-Future Relation ($v \prec u$)**:
   $$
   \Delta(P)_{uv} = (G_R(P))_{uv} > 0, \qquad \Delta(P)_{vu} = -(G_R(P))_{uv} < 0.
   $$
2. **Timelike Future-to-Past Relation ($u \prec v$)**:
   $$
   \Delta(P)_{uv} = -(G_R(P))_{vu} < 0, \qquad \Delta(P)_{vu} = (G_R(P))_{vu} > 0.
   $$
3. **Coincident Events ($u = v$)**:
   $$
   \Delta(P)_{uu} = 0.
   $$
4. **Spacelike / Incomparable Events ($u \parallel v$)**:
   $$
   \Delta(P)_{uv} = 0 \quad \text{and} \quad \Delta(P)_{vu} = 0 \quad \text{identically.}
   $$

*Proof.* By Definition 4.1, the $(u, v)$ entry is:
$$
\Delta(P)_{uv} = (G_R(P))_{uv} - (G_A(P))_{uv} = (G_R(P))_{uv} - (G_R(P))_{vu}.
$$
We analyze each case:
- *Case 1 ($v \prec u$)*: By Theorem 2.3, $(G_R(P))_{uv} > 0$. By acyclicity, $v \prec u \implies u \not\prec v$. Hence by Theorem 2.3(2), $(G_R(P))_{vu} = 0$. Therefore:
  $$
  \Delta(P)_{uv} = (G_R(P))_{uv} - 0 = (G_R(P))_{uv} > 0.
  $$
  By skew-symmetry, $\Delta(P)_{vu} = -\Delta(P)_{uv} < 0$.
- *Case 2 ($u \prec v$)*: Symmetrically, $u \prec v \implies (G_R(P))_{vu} > 0$ and $(G_R(P))_{uv} = 0$. Thus:
  $$
  \Delta(P)_{uv} = 0 - (G_R(P))_{vu} = -(G_R(P))_{vu} < 0.
  $$
- *Case 3 ($u = v$)*: By Theorem 2.3(1), $(G_R(P))_{uu} = 0$, so $\Delta(P)_{uu} = 0 - 0 = 0$.
- *Case 4 ($u \parallel v$)*: By definition of incomparability, neither $v \prec u$ nor $u \prec v$ holds.
  Since $v \not\prec u$, Theorem 2.3(2) asserts that $(G_R(P))_{uv} = 0$.
  Since $u \not\prec v$, Theorem 2.3(2) asserts that $(G_R(P))_{vu} = 0$.
  Substituting these into the commutator definition yields:
  $$
  \Delta(P)_{uv} = 0 - 0 = 0.
  $$
  By skew-symmetry, $\Delta(P)_{vu} = -0 = 0$. $\blacksquare$

Theorem 4.3 guarantees that on any finite poset, no field commutator can penetrate the spacelike barrier. Microcausality is exact, algebraic, and holds without requiring continuum approximations, metric tensors, or asymptotic limits.


---

## 5. Order-Convex Diamond Restriction Invariance

A foundational requirement for any intrinsic causal field theory is that local causal propagation within an isolated region must not depend on events outside that region. In native poset geometry, this property is formulated as restriction invariance across order-convex subposets.

### 5.1 Order-Convex Subposets and Causal Diamonds

**Definition 5.1 (Order-Convex Subposet).** *A subposet $Q \subseteq P$ is said to be order-convex in $P$ if for every pair of events $x, y \in Q$ and any event $z \in P$,*
$$
x \prec z \prec y \implies z \in Q.
$$

Prominent examples of order-convex subposets include:
1. **Alexandrov Intervals (Open Causal Diamonds)**: For any pair $p \prec q$ in $P$,
   $$
   I(p, q) := \{ z \in P : p \prec z \prec q \}.
   $$
2. **Closed Causal Diamonds**:
   $$
   [p, q] := \{ z \in P : p \preceq z \preceq q \}.
   $$
3. **Past Ideals (Lower Sets)**: $J \subseteq P$ such that $y \in J$ and $x \prec y \implies x \in J$.
4. **Future Filters (Upper Sets)**: $F \subseteq P$ such that $x \in F$ and $x \prec y \implies y \in F$.

### 5.2 Preservation of Strict $k$-Chains and Restriction Invariance Theorem

**Theorem 5.2 (Exact Order-Convex Restriction Invariance).** *Let $P = (V, \prec)$ be a finite poset and let $Q \subseteq P$ be an order-convex subposet with induced order $\prec_Q := \prec \cap (Q \times Q)$. Then for all $u, v \in Q$ and every integer $k \ge 1$:*
$$
(C_P^k)_{uv} = (C_Q^k)_{uv}.
$$
*Consequently, the restriction of the global retarded Green operator, advanced Green operator, and discrete Pauli–Jordan commutator of $P$ to the subposet $Q$ coincides identically with the intrinsic operators constructed purely within $Q$:*
$$
(G_R(P))|_Q = G_R(Q), \qquad (G_A(P))|_Q = G_A(Q), \qquad (\Delta(P))|_Q = \Delta(Q).
$$

*Proof.* By Theorem 1.2, $(C_P^k)_{uv}$ is the number of strict $k$-chains:
$$
v = x_0 \prec x_1 \prec x_2 \prec \dots \prec x_k = u \quad \text{in } P.
$$
Because $u, v \in Q$, we have $v \prec x_j \prec u$ for every intermediate index $j \in \{1, 2, \dots, k-1\}$.
By Definition 5.1, the order-convexity of $Q$ implies that $x_j \in Q$ for all $j \in \{1, \dots, k-1\}$.
Therefore, every strict $k$-chain connecting $v$ to $u$ in $P$ is composed entirely of elements belonging to $Q$.
Since the relation $\prec_Q$ on $Q$ is the exact restriction of $\prec$ to $Q$, every such chain in $P$ is a valid strict $k$-chain in $Q$, and vice versa.
Thus the count of strict $k$-chains connecting $v$ to $u$ in $P$ equals the count in $Q$:
$$
(C_P^k)_{uv} = (C_Q^k)_{uv} \quad \text{for all } u, v \in Q, \; k \ge 1.
$$

Now evaluate the retarded Green operator on the pair $u, v \in Q$:
$$
((G_R(P))|_Q)_{uv} = (G_R(P))_{uv} = \sum_{k=1}^{N_P-1} \mu^k (C_P^k)_{uv}.
$$
For $k \ge N_Q$, any chain in $Q$ of length $k$ would require at least $k+1 > N_Q$ distinct elements in $Q$, which is impossible. Hence $(C_Q^k)_{uv} = 0$ for all $k \ge N_Q$.
Using $(C_P^k)_{uv} = (C_Q^k)_{uv}$, we obtain:
$$
((G_R(P))|_Q)_{uv} = \sum_{k=1}^{N_Q-1} \mu^k (C_Q^k)_{uv} = (G_R(Q))_{uv}.
$$
This establishes $(G_R(P))|_Q = G_R(Q)$.

Transposing yields the advanced Green operator identity:
$$
(G_A(P))|_Q = ((G_R(P))|_Q)^T = G_R(Q)^T = G_A(Q).
$$
Subtracting the two relations gives:
$$
(\Delta(P))|_Q = (G_R(P))|_Q - (G_A(P))|_Q = G_R(Q) - G_A(Q) = \Delta(Q).
$$
$\blacksquare$

Theorem 5.2 establishes that causal resolvent propagation is strictly local with respect to order-convex domains: the internal causal commutator algebra inside a causal diamond $[p, q]$ is completely invariant under embedding into larger future or past causal histories.

---

## 6. Background-Free Sorkin–Johnston Bosonic State Attachment

In continuum quantum field theory on curved spacetimes lacking timelike Killing vectors, there is in general no preferred vacuum state. Sorkin and Johnston introduced an intrinsic, coordinate-free formulation of the quantum vacuum state directly from the Pauli–Jordan commutator operator. Here we construct the exact discrete Sorkin–Johnston bosonic state on any finite causal poset without continuum limits or coordinate embeddings.

### 6.1 Discrete Symplectic Field Space and Canonical Commutation Relations

Let $\mathcal{F} := \mathbb{R}^N$ be the real vector space of discrete field configurations (or test functions) on $V$. We define the discrete symplectic form $\sigma: \mathcal{F} \times \mathcal{F} \to \mathbb{R}$ by:
$$
\sigma(f, g) := f^T (G_R(P) - G_A(P)) g = f^T \Delta(P) g.
$$
Since $\Delta(P) = G_R(P) - G_A(P)$ is real and skew-symmetric, $\sigma$ is bilinear and antisymmetric:
$$
\sigma(g, f) = g^T \Delta(P) f = -f^T \Delta(P) g = -\sigma(f, g).
$$

To each test vector $f \in \mathcal{F}$, we associate a self-adjoint bosonic quantum field operator $\phi(f)$ acting on a Hilbert space $\mathcal{H}$. The field operators satisfy the canonical commutation relations (CCR):
$$
[\phi(f), \phi(g)] = i \sigma(f, g) \mathbf{1}_{\mathcal{H}} = i f^T \Delta(P) g \mathbf{1}_{\mathcal{H}} = i f^T (G_R(P) - G_A(P)) g \mathbf{1}_{\mathcal{H}}.
$$
In terms of the localized site operators $\phi(u) := \phi(e_u)$ (where $e_u$ is the standard basis vector for event $u \in V$):
$$
[\phi(u), \phi(v)] = i \Delta(P)_{uv} \mathbf{1}_{\mathcal{H}} = i (G_R(P) - G_A(P))_{uv} \mathbf{1}_{\mathcal{H}}.
$$
By Theorem 4.3, if $u \parallel v$, then $\Delta(P)_{uv} = 0$, guaranteeing:
$$
[\phi(u), \phi(v)] = 0 \quad \text{for all incomparable (spacelike) events } u \parallel v.
$$

### 6.2 Gaussian States and the Physical State Condition

A Gaussian quantum state $\omega$ on the field algebra is fully characterized by its two-point correlation matrix $W \in \mathbb{C}^{N \times N}$:
$$
W_{uv} := \omega(\phi(u) \phi(v)).
$$
The state $\omega$ is physical if and only if $W$ satisfies two fundamental requirements:
1. **Commutator Identity**:
   $$
   W - W^T = i \Delta(P) = i (G_R(P) - G_A(P)) = M.
   $$
2. **Quantum Uncertainty / Positivity**:
   $$
   W \succeq 0 \quad (\text{positive semidefinite as a complex Hermitian matrix}).
   $$
Writing $W = \frac{1}{2} R + \frac{i}{2} \Delta(P)$ with $R = R^T \in \mathbb{R}^{N \times N}$, condition $W \succeq 0$ is equivalent to the generalized Robertson–Schrödinger uncertainty relation:
$$
R \succeq 0 \quad \text{and} \quad R \succeq \pm M = \pm i \Delta(P) = \pm i (G_R(P) - G_A(P)).
$$

### 6.3 Spectral Decomposition of the Hermitian Operator $M$

Consider the complex matrix:
$$
M := i \Delta(P) = i (G_R(P) - G_A(P)).
$$
Since $\Delta = G_R - G_A$ is real and skew-symmetric ($\Delta^T = -\Delta$), $M$ is purely imaginary and Hermitian:
$$
M^\dagger = \left(i \Delta\right)^\dagger = -i \Delta^T = -i (-\Delta) = i \Delta = M.
$$
Therefore, $M$ has purely real eigenvalues. Moreover, because $M$ is purely imaginary ($M^* = -M$), if $v$ is an eigenvector with eigenvalue $\lambda$, then:
$$
M v^* = -(M v)^* = -(\lambda v)^* = -\lambda v^*.
$$
Thus, all non-zero eigenvalues of $M$ occur in symmetric pairs $\pm \lambda_j$ ($\lambda_j > 0$).

Let the spectral decomposition of $M$ be:
$$
M = \sum_{\lambda_j > 0} \lambda_j \left( v_j v_j^\dagger - v_j^* (v_j^*)^\dagger \right) + 0 \cdot P_{\ker(M)},
$$
where $\{v_j\}$ are orthonormal eigenvectors corresponding to positive eigenvalues $\lambda_j > 0$, $\{v_j^*\}$ are orthonormal eigenvectors corresponding to negative eigenvalues $-\lambda_j$, and $P_{\ker(M)}$ is the orthogonal projection onto the null space $\ker(M)$.

The operator absolute value $\lvert M\rvert := \sqrt{M^2}$ is given by:
$$
\lvert M\rvert = \sum_{\lambda_j > 0} \lambda_j \left( v_j v_j^\dagger + v_j^* (v_j^*)^\dagger \right).
$$

### 6.4 The Sorkin–Johnston Two-Point Operator

**Definition 6.1 (Sorkin–Johnston Two-Point Operator).** *The discrete Sorkin–Johnston two-point operator $W_{\rm SJ}$ is defined by:*
$$
W_{\rm SJ} := \frac{1}{2} \left( \lvert M\rvert + M \right).
$$

**Theorem 6.2 (Properties of the Sorkin–Johnston State).**
1. **Explicit Positive-Eigenmode Projector**:
   $$
   W_{\rm SJ} = \sum_{\lambda_j > 0} \lambda_j v_j v_j^\dagger.
   $$
2. **Unconditional Positivity**: $W_{\rm SJ} \succeq 0$.
3. **Commutator Identity**:
   $$
   W_{\rm SJ} - W_{\rm SJ}^T = M = i \Delta(P).
   $$
4. **Clean Decoupling of Spacelike Zero Modes**: For every vector $v_0 \in \ker(M) = \ker(G_R - G_A)$,
   $$
   W_{\rm SJ} v_0 = 0.
   $$
5. **Modal Expansion and Standard Bosonic CCR**: Expanding the localized site field operators in the positive eigenmodes of $M$:
   $$
   \phi(u) = \sum_{\lambda_j > 0} \sqrt{\lambda_j} \left( (v_j)_u \hat a_j + (v_j^*)_u \hat a_j^\dagger \right),
   $$
   the standard bosonic annihilation and creation algebra:
   $$
   [\hat a_j, \hat a_k^\dagger] = +\delta_{jk}\mathbf{1}_{\mathcal{H}}, \qquad [\hat a_j, \hat a_k] = 0, \qquad [\hat a_j^\dagger, \hat a_k^\dagger] = 0,
   $$
   identically reproduces the physical two-point function and commutator:
   $$
   \langle 0_{\rm SJ}\rvert \phi(u) \phi(v) \lvert 0_{\rm SJ}\rangle = (W_{\rm SJ})_{uv},
   $$
   $$
   [\phi(u), \phi(v)] = \sum_{\lambda_j > 0} \lambda_j \left( (v_j)_u (v_j^*)_v - (v_j^*)_u (v_j)_v \right) \mathbf 1_{\mathcal{H}} = (W_{\rm SJ} - W_{\rm SJ}^T)_{uv}\mathbf 1_{\mathcal{H}} = M_{uv}\mathbf 1_{\mathcal{H}} = i\Delta(P)_{uv}\mathbf 1_{\mathcal{H}}.
   $$

*Proof.*
1. Substituting the spectral representations:
   $$
   W_{\rm SJ} = \frac{1}{2} \left( \sum_{\lambda_j > 0} \lambda_j (v_j v_j^\dagger + v_j^* (v_j^*)^\dagger) + \sum_{\lambda_j > 0} \lambda_j (v_j v_j^\dagger - v_j^* (v_j^*)^\dagger) \right) = \sum_{\lambda_j > 0} \lambda_j v_j v_j^\dagger.
   $$
2. Each term $\lambda_j v_j v_j^\dagger$ is a positive semidefinite rank-1 operator because $\lambda_j > 0$. The sum of positive semidefinite operators is positive semidefinite: $W_{\rm SJ} \succeq 0$.
3. Notice that $(v_j v_j^\dagger)^T = (v_j^\dagger)^T v_j^T = v_j^* (v_j^*)^\dagger$. Therefore:
   $$
   W_{\rm SJ}^T = \sum_{\lambda_j > 0} \lambda_j v_j^* (v_j^*)^\dagger.
   $$
   Subtracting gives:
   $$
   W_{\rm SJ} - W_{\rm SJ}^T = \sum_{\lambda_j > 0} \lambda_j \left( v_j v_j^\dagger - v_j^* (v_j^*)^\dagger \right) = M = i \Delta(P).
   $$
4. If $v_0 \in \ker(M)$, then by orthogonality of eigenspaces, $v_j^\dagger v_0 = 0$ for all $\lambda_j > 0$. Therefore:
   $$
   W_{\rm SJ} v_0 = \sum_{\lambda_j > 0} \lambda_j v_j (v_j^\dagger v_0) = 0.
   $$
5. Evaluating the commutator of the modal expansion directly:
   $$
   [\phi(u), \phi(v)] = \sum_{j, k} \sqrt{\lambda_j \lambda_k} \left[ (v_j)_u (v_k^*)_v [\hat a_j, \hat a_k^\dagger] + (v_j^*)_u (v_k)_v [\hat a_j^\dagger, \hat a_k] \right]
   $$
   $$
   = \sum_{\lambda_j > 0} \lambda_j \left( (v_j)_u (v_j^*)_v - (v_j^*)_u (v_j)_v \right) \mathbf 1_{\mathcal{H}} = (W_{\rm SJ} - W_{\rm SJ}^T)_{uv}\mathbf 1_{\mathcal{H}} = M_{uv}\mathbf 1_{\mathcal{H}} = i\Delta(P)_{uv}\mathbf 1_{\mathcal{H}}.
   $$
$\blacksquare$

Theorem 6.2 proves that the Sorkin–Johnston state $W_{\rm SJ}$ provides an exact, coordinate-free vacuum state attachment. Pure spacelike modes (vectors supported on antichains or incomparable events that do not communicate causally) lie strictly in $\ker(M)$ and decouple cleanly from physical field fluctuations.

---

## 7. Explicit Hand-Calculated Canonical Benchmarks

To establish an incontrovertible baseline for verification, all matrices, resolvents, commutators, characteristic polynomials, and eigenspaces are derived strictly by hand across six canonical posets.

### 7.1 Benchmark 1: Singleton Poset ($N = 1$)

Consider the trivial poset $P_1 = \{0\}$ consisting of a single event:
- Vertices: $V = \{0\}$.
- Causal relations: None ($0 \not\prec 0$).
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 \end{pmatrix}.
  $$
- Resolvent Green operators:
  $$
  G_R(P_1) = \begin{pmatrix} 0 \end{pmatrix}, \qquad G_A(P_1) = \begin{pmatrix} 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(P_1) = \begin{pmatrix} 0 \end{pmatrix}, \qquad M = i\Delta(P_1) = \begin{pmatrix} 0 \end{pmatrix}.
  $$
- Sorkin–Johnston state: $W_{\rm SJ} = \begin{pmatrix} 0 \end{pmatrix}$.
- Microcausality holds vacuously.

### 7.2 Benchmark 2: Two-Chain $C_2$ ($N = 2$)

Consider the two-element chain with order relation $0 \prec 1$:
- Vertices: $V = \{0, 1\}$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}.
  $$
- Nilpotency:
  $$
  C_P^2 = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix} = 0.
  $$
- Retarded and advanced Green operators (for parameter $\mu > 0$):
  $$
  G_R(C_2) = \mu C_P = \begin{pmatrix} 0 & 0 \\ \mu & 0 \end{pmatrix}, \qquad G_A(C_2) = G_R^T = \begin{pmatrix} 0 & \mu \\ 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(C_2) = G_R - G_A = \begin{pmatrix} 0 & -\mu \\ \mu & 0 \end{pmatrix}.
  $$
- Hermitian operator $M = i\Delta$:
  $$
  M = \begin{pmatrix} 0 & -i\mu \\ i\mu & 0 \end{pmatrix} = -\mu \sigma_y.
  $$
- Characteristic polynomial of $M$:
  $$
  \det(\lambda I - M) = \det \begin{pmatrix} \lambda & i\mu \\ -i\mu & \lambda \end{pmatrix} = \lambda^2 - (i\mu)(-i\mu) = \lambda^2 - \mu^2 = 0.
  $$
  Eigenvalues: $\lambda_1 = +\mu$, $\lambda_2 = -\mu$.
- Normalized positive eigenvector for $\lambda_1 = +\mu$:
  $$
  \begin{pmatrix} \mu & i\mu \\ -i\mu & \mu \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies x_0 = -i x_1 \implies v_+ = \frac{1}{\sqrt{2}} \begin{pmatrix} -i \\ 1 \end{pmatrix}.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \mu v_+ v_+^\dagger = \mu \frac{1}{2} \begin{pmatrix} -i \\ 1 \end{pmatrix} \begin{pmatrix} i & 1 \end{pmatrix} = \frac{\mu}{2} \begin{pmatrix} 1 & -i \\ i & 1 \end{pmatrix}.
  $$
- Verification:
  $$
  W_{\rm SJ} - W_{\rm SJ}^T = \frac{\mu}{2} \begin{pmatrix} 1 & -i \\ i & 1 \end{pmatrix} - \frac{\mu}{2} \begin{pmatrix} 1 & i \\ -i & 1 \end{pmatrix} = \begin{pmatrix} 0 & -i\mu \\ i\mu & 0 \end{pmatrix} = M = i\Delta.
  $$
  Eigenvalues of $W_{\rm SJ}$ are $\mu \ge 0$ and $0 \ge 0$, confirming $W_{\rm SJ} \succeq 0$ and $\dim\ker(M) = 0$.

### 7.3 Benchmark 3: Two-Antichain $A_2$ ($N = 2$)

Consider two incomparable events $0 \parallel 1$:
- Vertices: $V = \{0, 1\}$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}.
  $$
- Resolvent Green operators:
  $$
  G_R(A_2) = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}, \qquad G_A(A_2) = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(A_2) = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}, \qquad M = i\Delta = 0, \qquad W_{\rm SJ} = 0.
  $$
- Exact microcausality verification: $\Delta_{01} = \Delta_{10} = 0$ identically on $0 \parallel 1$.

### 7.4 Benchmark 4: Three-Chain $C_3$ ($N = 3$)

Consider the total order $0 \prec 1 \prec 2$:
- Vertices: $V = \{0, 1, 2\}$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix}.
  $$
- Matrix powers:
  $$
  C_P^2 = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \qquad C_P^3 = 0.
  $$
- Retarded Green operator:
  $$
  G_R(C_3) = \mu C_P + \mu^2 C_P^2 = \begin{pmatrix} 0 & 0 & 0 \\ \mu & 0 & 0 \\ \mu + \mu^2 & \mu & 0 \end{pmatrix}.
  $$
- Advanced Green operator:
  $$
  G_A(C_3) = G_R^T = \begin{pmatrix} 0 & \mu & \mu + \mu^2 \\ 0 & 0 & \mu \\ 0 & 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(C_3) = G_R - G_A = \begin{pmatrix} 0 & -\mu & -(\mu + \mu^2) \\ \mu & 0 & -\mu \\ \mu + \mu^2 & \mu & 0 \end{pmatrix}.
  $$
- Positivity check: For $\mu > 0$, $(G_R)_{10} = \mu > 0$, $(G_R)_{21} = \mu > 0$, and $(G_R)_{20} = \mu + \mu^2 > 0$. Zero cancellations occur.
- Hermitian operator $M = i\Delta$:
  $$
  M = \begin{pmatrix} 0 & -i\mu & -i(\mu+\mu^2) \\ i\mu & 0 & -i\mu \\ i(\mu+\mu^2) & i\mu & 0 \end{pmatrix}.
  $$
- Characteristic polynomial of $M$:
  $$
  \det(\lambda I - M) = \det \begin{pmatrix} \lambda & i\mu & i(\mu+\mu^2) \\ -i\mu & \lambda & i\mu \\ -i(\mu+\mu^2) & -i\mu & \lambda \end{pmatrix}.
  $$
  Expanding by the first row:
  $$
  \det(\lambda I - M) = \lambda \left[ \lambda^2 - \mu^2 \right] - (i\mu) \left[ -i\mu \lambda + \mu(\mu+\mu^2) \right] + (i(\mu+\mu^2)) \left[ -\mu^2 + i\lambda(\mu+\mu^2) \right]
  $$
  $$
  = \lambda^3 - \mu^2 \lambda - \mu^2 \lambda - i\mu^2(\mu+\mu^2) + i\mu^2(\mu+\mu^2) - \lambda(\mu+\mu^2)^2.
  $$
  The imaginary terms cancel identically, leaving:
  $$
  \det(\lambda I - M) = \lambda^3 - \left[ 2\mu^2 + (\mu+\mu^2)^2 \right] \lambda = \lambda \left( \lambda^2 - \omega_3^2 \right) = 0,
  $$
  where $\omega_3 := \sqrt{2\mu^2 + (\mu+\mu^2)^2} = \mu \sqrt{3 + 2\mu + \mu^2}$.
  For $\mu = 1$, $\omega_3 = \sqrt{2 + 4} = \sqrt{6}$.
  Eigenvalues at $\mu = 1$: $\lambda \in \{+\sqrt{6}, -\sqrt{6}, 0\}$.
- Zero mode of $M$ at $\mu = 1$:
  $$
  M v_0 = 0 \implies \begin{pmatrix} 0 & -1 & -2 \\ 1 & 0 & -1 \\ 2 & 1 & 0 \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} = 0 \implies x_1 = -2x_2, \; x_0 = x_2 \implies v_0 = \frac{1}{\sqrt{6}} \begin{pmatrix} 1 \\ -2 \\ 1 \end{pmatrix}.
  $$
- Normalized positive eigenvector for $\lambda = +\sqrt{6}$:
  $$
  (M - \sqrt{6}I) v_+ = 0 \implies v_+ = \frac{1}{\sqrt{60}} \begin{pmatrix} -1 - 2i\sqrt{6} \\ 2 - i\sqrt{6} \\ 5 \end{pmatrix}, \qquad \lVert v_+\rVert^2 = \frac{1 + 24 + 4 + 6 + 25}{60} = 1.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{6} v_+ v_+^\dagger = \frac{\sqrt{6}}{60} \begin{pmatrix} 25 & 10 - 5i\sqrt{6} & -5 - 10i\sqrt{6} \\ 10 + 5i\sqrt{6} & 10 & 10 - 5i\sqrt{6} \\ -5 + 10i\sqrt{6} & 10 + 5i\sqrt{6} & 25 \end{pmatrix}.
  $$
- Commutator verification:
  $$
  W_{\rm SJ} - W_{\rm SJ}^T = \begin{pmatrix} 0 & -i & -2i \\ i & 0 & -i \\ 2i & i & 0 \end{pmatrix} = M = i\Delta.
  $$
  Decoupling of the longitudinal zero mode: $W_{\rm SJ} v_0 = \sqrt{6} v_+ (v_+^\dagger v_0) = 0$ since $v_+^\dagger v_0 = \frac{1}{60}[(-1+2i\sqrt 6) - 2(2+i\sqrt 6) + 5] = 0$.

### 7.5 Benchmark 5: Three-Element Fork Poset $V$ ($N = 3$)

Consider the fork poset with relations $0 \prec 1$, $0 \prec 2$, and $1 \parallel 2$:
- Vertices: $V = \{0, 1, 2\}$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}.
  $$
- Nilpotency: $C_P^2 = 0$.
- Retarded and advanced Green operators:
  $$
  G_R(V) = \begin{pmatrix} 0 & 0 & 0 \\ \mu & 0 & 0 \\ \mu & 0 & 0 \end{pmatrix}, \qquad G_A(V) = \begin{pmatrix} 0 & \mu & \mu \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(V) = G_R - G_A = \begin{pmatrix} 0 & -\mu & -\mu \\ \mu & 0 & 0 \\ \mu & 0 & 0 \end{pmatrix}.
  $$
- Microcausality check: On the incomparable pair $1 \parallel 2$, $\Delta_{12} = 0$ and $\Delta_{21} = 0$.
- Hermitian operator $M = i\Delta$:
  $$
  M = \begin{pmatrix} 0 & -i\mu & -i\mu \\ i\mu & 0 & 0 \\ i\mu & 0 & 0 \end{pmatrix}.
  $$
- Characteristic polynomial:
  $$
  \det(\lambda I - M) = \lambda (\lambda^2 - 2\mu^2) = 0.
  $$
  Eigenvalues: $\lambda \in \{+\mu\sqrt{2}, -\mu\sqrt{2}, 0\}$.
- Spacelike zero mode of $M$:
  $$
  M v_0 = 0 \implies \begin{pmatrix} 0 & -i\mu & -i\mu \\ i\mu & 0 & 0 \\ i\mu & 0 & 0 \end{pmatrix} \begin{pmatrix} x_0 \\ x_1 \\ x_2 \end{pmatrix} = 0 \implies x_0 = 0, \; x_1 + x_2 = 0.
  $$
  Normalized spacelike zero mode:
  $$
  v_0 = \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ 1 \\ -1 \end{pmatrix}.
  $$
  Notice that $v_0$ is supported exclusively on the incomparable events $\{1, 2\}$, demonstrating that spacelike degrees of freedom decouple into the kernel of $M$ ($\dim\ker(M)=1$).
- Normalized positive eigenvector for $\lambda = +\mu\sqrt{2}$ (at $\mu = 1$):
  $$
  (M - \sqrt{2}I) v_+ = 0 \implies v_+ = \frac{1}{2} \begin{pmatrix} -i\sqrt{2} \\ 1 \\ 1 \end{pmatrix}, \qquad \lVert v_+\rVert^2 = \frac{2 + 1 + 1}{4} = 1.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{2} v_+ v_+^\dagger = \frac{\sqrt{2}}{4} \begin{pmatrix} -i\sqrt{2} \\ 1 \\ 1 \end{pmatrix} \begin{pmatrix} i\sqrt{2} & 1 & 1 \end{pmatrix} = \begin{pmatrix} \frac{\sqrt{2}}{2} & -\frac{i}{2} & -\frac{i}{2} \\ \frac{i}{2} & \frac{\sqrt{2}}{4} & \frac{\sqrt{2}}{4} \\ \frac{i}{2} & \frac{\sqrt{2}}{4} & \frac{\sqrt{2}}{4} \end{pmatrix}.
  $$
- Commutator and decoupling verification:
  $$
  W_{\rm SJ} - W_{\rm SJ}^T = \begin{pmatrix} 0 & -i & -i \\ i & 0 & 0 \\ i & 0 & 0 \end{pmatrix} = M = i\Delta, \qquad W_{\rm SJ} v_0 = 0.
  $$

### 7.6 Benchmark 6: Four-Element Diamond $E_{\text{diamond}}$ ($N = 4$)

Consider the four-element causal diamond poset with order relations:
$$
0 \prec 1, \quad 0 \prec 2, \quad 0 \prec 3 \quad (\text{transitive}), \quad 1 \prec 3, \quad 2 \prec 3, \quad 1 \parallel 2.
$$
- Vertices: $V = \{0, 1, 2, 3\}$.
- Causal incidence matrix $C_P$:
  $$
  C_P = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 1 & 1 & 0
  \end{pmatrix}.
  $$
- Matrix powers:
  $$
  C_P^2 = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 1 & 1 & 0
  \end{pmatrix}
  \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 1 & 1 & 0
  \end{pmatrix}
  = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  2 & 0 & 0 & 0
  \end{pmatrix}.
  $$
  Notice $(C_P^2)_{30} = 2$, enumerating the two distinct 2-chains from $0$ to $3$: $0 \prec 1 \prec 3$ and $0 \prec 2 \prec 3$.
  All other entries of $C_P^2$ are zero.
  $$
  C_P^3 = C_P C_P^2 = 0 \quad (\text{poset height } h(P) = 2).
  $$
- Retarded Green operator:
  $$
  G_R(E_{\text{diamond}}) = \mu C_P + \mu^2 C_P^2 = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  \mu & 0 & 0 & 0 \\
  \mu & 0 & 0 & 0 \\
  \mu + 2\mu^2 & \mu & \mu & 0
  \end{pmatrix}.
  $$
- Advanced Green operator:
  $$
  G_A(E_{\text{diamond}}) = G_R^T = \begin{pmatrix}
  0 & \mu & \mu & \mu + 2\mu^2 \\
  0 & 0 & 0 & \mu \\
  0 & 0 & 0 & \mu \\
  0 & 0 & 0 & 0
  \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta(E_{\text{diamond}}) = G_R - G_A = \begin{pmatrix}
  0 & -\mu & -\mu & -(\mu + 2\mu^2) \\
  \mu & 0 & 0 & -\mu \\
  \mu & 0 & 0 & -\mu \\
  \mu + 2\mu^2 & \mu & \mu & 0
  \end{pmatrix}.
  $$
- Microcausality check: $\Delta_{12} = 0$ and $\Delta_{21} = 0$ on the spacelike pair $1 \parallel 2$.
- Diamond restriction invariance check: Restricting to the order-convex fork $Q = \{0, 1, 2\}$ yields:
  $$
  (G_R(E_{\text{diamond}}))|_Q = \begin{pmatrix} 0 & 0 & 0 \\ \mu & 0 & 0 \\ \mu & 0 & 0 \end{pmatrix} = G_R(V).
  $$
- Explicit evaluation at $\mu = 1$:
  At $\mu = 1$, $\mu + 2\mu^2 = 1 + 2 = 3$.
  $$
  \Delta = \begin{pmatrix}
  0 & -1 & -1 & -3 \\
  1 & 0 & 0 & -1 \\
  1 & 0 & 0 & -1 \\
  3 & 1 & 1 & 0
  \end{pmatrix}, \qquad
  M = i\Delta = \begin{pmatrix}
  0 & -i & -i & -3i \\
  i & 0 & 0 & -i \\
  i & 0 & 0 & -i \\
  3i & i & i & 0
  \end{pmatrix}.
  $$
- Characteristic polynomial of $M$:
  $$
  \det(\lambda I - M) = \det \begin{pmatrix}
  \lambda & i & i & 3i \\
  -i & \lambda & 0 & i \\
  -i & 0 & \lambda & i \\
  -3i & -i & -i & \lambda
  \end{pmatrix}.
  $$
  Subtracting row 2 from row 3 and adding column 2 to column 3 yields:
  $$
  \det(\lambda I - M) = \lambda^2 (\lambda^2 - 13) = 0.
  $$
- Eigenvalues of Hermitian matrix $M$:
  $$
  \lambda(M) \in \{ +\sqrt{13}, \; -\sqrt{13}, \; 0, \; 0 \}, \qquad \dim\ker(M) = 2.
  $$
- Orthonormal basis for $\ker(M)$:
  1. Spacelike zero mode localized on the incomparable pair $1 \parallel 2$:
     $$
     v_{0, 1} := \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ 1 \\ -1 \\ 0 \end{pmatrix}.
     $$
  2. Longitudinal zero mode across the diamond axis:
     $$
     v_{0, 2} := \frac{1}{\sqrt{26}} \begin{pmatrix} 2 \\ -3 \\ -3 \\ 2 \end{pmatrix}.
     $$
- Normalized positive eigenvector for $\lambda = +\sqrt{13}$:
  $$
  (M - \sqrt{13}I) v_+ = 0 \implies v_+ = \frac{1}{\sqrt{286}} \begin{pmatrix} -2 - 3i\sqrt{13} \\ 3 - i\sqrt{13} \\ 3 - i\sqrt{13} \\ 11 \end{pmatrix},
  $$
  with norm squared:
  $$
  \lVert v_+\rVert^2 = \frac{(4 + 117) + 2(9 + 13) + 121}{286} = \frac{121 + 44 + 121}{286} = 1.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{13} v_+ v_+^\dagger.
  $$
- Verification of commutator and clean mode decoupling:
  $$
  W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(E_{\text{diamond}}),
  $$
  $$
  W_{\rm SJ} v_{0, 1} = 0, \qquad W_{\rm SJ} v_{0, 2} = 0.
  $$
  Both unphysical spacelike and longitudinal degrees of freedom decouple identically from the physical field state.

### 7.7 Benchmark 7: Four-Chain $C_4$ ($N = 4$)

Consider the four-element total order with chain relations $0 \prec 1 \prec 2 \prec 3$:
- Vertices: $V = \{0, 1, 2, 3\}$.
- Causal incidence matrix $C_P$:
  $$
  C_P = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  1 & 1 & 0 & 0 \\
  1 & 1 & 1 & 0
  \end{pmatrix}.
  $$
- Incidence powers and nilpotency:
  $$
  C_P^2 = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  2 & 1 & 0 & 0
  \end{pmatrix}, \qquad
  C_P^3 = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0
  \end{pmatrix}, \qquad
  C_P^4 = 0.
  $$
- Retarded Green operator at $\mu = 1$:
  $$
  G_R(C_4) = C_P + C_P^2 + C_P^3 = \begin{pmatrix}
  0 & 0 & 0 & 0 \\
  1 & 0 & 0 & 0 \\
  2 & 1 & 0 & 0 \\
  4 & 2 & 1 & 0
  \end{pmatrix}, \qquad
  G_A(C_4) = G_R^T = \begin{pmatrix}
  0 & 1 & 2 & 4 \\
  0 & 0 & 1 & 2 \\
  0 & 0 & 0 & 1 \\
  0 & 0 & 0 & 0
  \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator $\Delta(C_4) = G_R - G_A$:
  $$
  \Delta(C_4) = \begin{pmatrix}
  0 & -1 & -2 & -4 \\
  1 & 0 & -1 & -2 \\
  2 & 1 & 0 & -1 \\
  4 & 2 & 1 & 0
  \end{pmatrix}.
  $$
- Pfaffian and Determinant of $\Delta(C_4)$:
  $$
  \operatorname{Pf}(\Delta) = \Delta_{01}\Delta_{23} - \Delta_{02}\Delta_{13} + \Delta_{03}\Delta_{12} = (-1)(-1) - (-2)(-2) + (-4)(-1) = 1 - 4 + 4 = 1.
  $$
  $$
  \det(\Delta(C_4)) = \left(\operatorname{Pf}(\Delta)\right)^2 = 1^2 = 1 \ne 0.
  $$
- Hermitian operator $M = i\Delta(C_4)$:
  $$
  M = \begin{pmatrix}
  0 & -i & -2i & -4i \\
  i & 0 & -i & -2i \\
  2i & i & 0 & -i \\
  4i & 2i & i & 0
  \end{pmatrix}.
  $$
- Characteristic polynomial of $M$:
  $$
  \det(\lambda I - M) = \lambda^4 - 27\lambda^2 + 1 = 0.
  $$
  Setting $u = \lambda^2$ yields the quadratic resolvent $u^2 - 27u + 1 = 0$, whose exact positive roots are:
  $$
  u_1 = \frac{27 + 5\sqrt{29}}{2} \approx 26.962912, \qquad u_2 = \frac{27 - 5\sqrt{29}}{2} = \frac{1}{u_1} \approx 0.037088.
  $$
- Exact characteristic spectrum of $M$:
  $$
  \lambda \in \left\{ \pm \sqrt{\frac{27 + 5\sqrt{29}}{2}}, \; \pm \sqrt{\frac{27 - 5\sqrt{29}}{2}} \right\} \approx \{ \pm 5.192582, \; \pm 0.192582 \}.
  $$
- Non-degeneracy and Kernel:
  Since all four eigenvalues are strictly non-zero and $\det(M) = u_1 u_2 = 1 \ne 0$, we have:
  $$
  \dim\ker(M) = 0.
  $$
- Closed-form positive mode eigenvectors: For any positive root $\lambda > 0$ of $\lambda^4 - 27\lambda^2 + 1 = 0$, an exact eigenvector of $M$ is given by:
  $$
  v(\lambda) = \frac{1}{N(\lambda)} \begin{pmatrix}
  5\lambda + 10i\lambda^2 \\
  -10\lambda + 5i\lambda^2 \\
  (\lambda - \lambda^3) + 2i(\lambda^2 - 1) \\
  2\lambda(1 - \lambda^2) + i(1 - \lambda^2)
  \end{pmatrix},
  $$
  where $N(\lambda) = \lVert v(\lambda)\rVert$.
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \lambda_1 v(\lambda_1) v(\lambda_1)^\dagger + \lambda_2 v(\lambda_2) v(\lambda_2)^\dagger \succeq 0,
  $$
  satisfying $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(C_4)$ unconditionally.

### 7.8 Summary Table of Hand-Calculated Canonical Benchmarks

| Poset | $N$ | Poset Height $h(P)$ | Nilpotency Degree | Incomparable Pairs | $\Delta_{uv}$ on $u \parallel v$ | Non-Zero Spectrum of $M$ ($\mu=1$) | $\dim\ker(M)$ |
|---|---|---|---|---|---|---|---|
| Singleton $P_1$ | 1 | 0 | 1 ($C^1 = 0$) | 0 | Vacuous | None | 1 |
| Two-Chain $C_2$ | 2 | 1 | 2 ($C^2 = 0$) | 0 | Vacuous | $\pm 1$ | 0 |
| Two-Antichain $A_2$ | 2 | 0 | 1 ($C^1 = 0$) | 1 ($0 \parallel 1$) | $\Delta_{01} = 0$ | None | 2 |
| Three-Chain $C_3$ | 3 | 2 | 3 ($C^3 = 0$) | 0 | Vacuous | $\pm\sqrt{6}$ | 1 |
| Fork $V$ | 3 | 1 | 2 ($C^2 = 0$) | 1 ($1 \parallel 2$) | $\Delta_{12} = 0$ | $\pm\sqrt{2}$ | 1 |
| Diamond $E_{\text{diamond}}$ | 4 | 2 | 3 ($C^3 = 0$) | 1 ($1 \parallel 2$) | $\Delta_{12} = 0$ | $\pm\sqrt{13}$ | 2 |
| Four-Chain $C_4$ | 4 | 3 | 4 ($C^4 = 0$) | 0 | Vacuous | $\pm\sqrt{\frac{27 \pm 5\sqrt{29}}{2}}$ | 0 |

---

## 8. Scope, Non-Implications, and Status-M Quarantine

### 8.1 Rigorous Mathematical Scope

The results established in this deliverable are exact algebraic and combinatorial theorems on finite partially ordered sets:
1. The unipotent operator $D_\mu(P) = I - \mu C_P$ is unconditionally invertible with $\det(D_\mu(P)) = 1$, and generates the retarded Green operator resolvent $G_R(P) = D_\mu(P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k$, which is strictly nilpotent with $\det(G_R(P)) = 0$ ($G_R(P)^N = 0$) and strictly positive inside the causal cone without continuum approximations.
2. The discrete Pauli–Jordan commutator $\Delta(P) = G_R(P) - G_A(P)$ obeys exact microcausality on all incomparable pairs $u \parallel v$ ($[\phi(u), \phi(v)] = i\Delta(P)_{uv}\mathbf 1 = 0$).
3. Restriction to order-convex subposets (causal diamonds) is strictly invariant: $(G_R(P))|_Q = G_R(Q)$, $(G_A(P))|_Q = G_A(Q)$, and $(\Delta(P))|_Q = \Delta(Q)$.
4. The Sorkin–Johnston two-point operator $W_{\rm SJ} = \frac{1}{2}(\lvert M\rvert + M) \succeq 0$ attaches an exact, positive-semidefinite bosonic state directly to the discrete causal structure ($W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(P)$ and $[\hat a_j, \hat a_k^\dagger] = +\delta_{jk}\mathbf 1$) while cleanly projecting out spacelike zero modes.

### 8.2 Explicit Non-Implications

To maintain strict scientific integrity and avoid unwarranted extrapolations:
1. **No Continuum Limit Claim**: The existence of an exact discrete Green operator on a finite poset does not prove that the poset approximates a smooth $3+1$-dimensional Lorentzian manifold or satisfies the continuum Einstein field equations.
2. **No Physical Units or Constants Derived**: The parameter $\mu > 0$ is a dimensionless mathematical coupling in the incidence algebra. No claim is made to derive the speed of light $c$, Planck's constant $\hbar$, Newton's gravitational constant $G$, or particle masses.
3. **No Derivation of Born's Rule**: Quantum state attachment via the Sorkin–Johnston construction provides a mathematical representation of canonical commutation relations on the discrete order; it does not derive quantum mechanics, measurement collapse, or Born's rule from deterministic poset growth.
4. **No Derivation of General Relativity**: The exactness of discrete microcausality reflects the irreflexive, transitive, and acyclic properties of partial orders, not an emergent dynamic metric theory.

### 8.3 Status-M Quarantine Statement

In full compliance with foundational research governance:
- **`ONTOLOGY.md`**, **`GOVERNANCE.md`**, **`PHYSICS.md`**, and **`FALSIFICATION_LEDGER.md`** remain strictly quarantined.
- No modifications, citations, or ontological claims are made regarding Status-M documents.
- The results presented herein stand purely on mathematical definitions of finite incidence algebras and operator theory.

---

## 9. Scientific review

Intrinsic Causal Propagator Author derived unipotent resolvent generator $D_\mu(P) = I - \mu C_P$ ($\det(D_\mu)=1$), background-free retarded Green operator resolvent $G_R(P) = D_\mu(P)^{-1} - I = \sum_{k=1}^{N-1}\mu^k C_P^k$ (strictly nilpotent with $\det(G_R)=0$, $G_R^N=0$), advanced operator $G_A(P) = G_R(P)^T$, Pauli–Jordan commutator $\Delta(P) = G_R - G_A$, exact discrete microcausality on incomparable pairs ($[\phi(u), \phi(v)] = i\Delta(P)_{uv}\mathbf 1$), order-convex diamond restriction invariance, and background-free Sorkin–Johnston bosonic state attachment $W_{\rm SJ} = \frac{1}{2}(\lvert M\rvert + M) \succeq 0$ with $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(P)$ and $[\hat a_j, \hat a_k^\dagger] = +\delta_{jk}\mathbf 1$. Independent Causal Propagator Reviewer independently verified by hand 100% of equations, nilpotency, invertibility of $D_\mu(P)$, microcausality proofs, and canonical benchmarks. Prospective protocol SHA-256 7109855eac970e6581238ecce78de351c8b0d45354883640d50f478084e1612f; accepted author report SHA-256 ed75a45f04f919411cd0ed7427df46a9abf47d6f1bc4cf7d1bf3e418c3602e05; independent scientific review SHA-256 532fbae93c9e56e29fb9f5e43c9ff49fd74348135675cd41526ab32e5b65c039.
