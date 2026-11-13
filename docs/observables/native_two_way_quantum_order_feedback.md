# A native two-way quantum-and-order feedback law through four births

**Decision.** Over the unchanged four-birth structural domain and seed kernel of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix), a coordinate-free five-Kraus quantum instrument family on a fixed qubit carrier $\mathcal H_Q=\mathbb C^2$ (extended by $\otimes\,\operatorname{id}_{\rm ref}$ to any finite-dimensional passive reference space $\mathcal H_{\rm ref}$) simultaneously satisfies strict complete positivity, complete-row trace preservation, full ideal and newborn-bit support, proper-slot mark locality, marked-parent relabeling equivariance, and exact unnormalized superoperator commutation across every incomparable-birth diamond and every transported suffix. Across parent sizes $n=1,2,3$, a co-rotating Clifford unitary cycles the active measurement axis through all three pairwise non-commuting Pauli observables $(\Sigma_1,\Sigma_2,\Sigma_3)=(Z,X,Y)$, preserving an exact nonselective Heisenberg operator martingale $\mathcal Q_n=2^n\Sigma_n$ while obstructing classical diagonal reduction in any single parent-independent basis on $\mathbb C^2$. Conditional on the prepared causal prefix $a\prec b$ with marks $(i,0)$ ($i\in\{0,1\}$)—where the [active classical antichain residual law](../track_b/native_active_residual_v1.md) is identically passive and the [precursor-local unitary payload law](../track_b/native_precursor_payloads_v1.md) has zero backreaction on order—the coupled law exhibits simultaneous `Quantum -> Order` and `Order/Mark -> Quantum` feedback across all $15$ structural continuations ($60$ marked histories), including a sign-reversing synergistic interaction contrast $-\frac{497}{5808}\ne 0$ in mean Benincasa–Dowker interval action, a single-run rational witness on the pure state $|\psi_{3,4}\rangle=\frac{2}{\sqrt5}|+\rangle+\frac{1}{\sqrt5}|-\rangle$, and strictly positive $L^1$ lower bounds through a shared imperfect erasure-and-confusion detector. This conditional finite mathematical construction leaves Status-M ontological commitments (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) strictly quarantined and derives neither Born's rule, physical constants, clocks, continuum spacetime geometry, nor General Relativity.

---

## Context and architecture

Under the [foundational research scope](../coordination/FOUNDATIONAL_RESEARCH_SCOPE.md), the [native geometry, gravity and measurement plan](../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md), and the [native mass/gravity mapping](../coordination/NATIVE_MASS_MAPPING.md), previously accepted finite bridge packages over the admitted four-birth prefix of the [native theorem package](../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) separated into two one-way mechanisms:

1. **Pure `Order/Mark -> Quantum` payload transport without structural backreaction:** Both [mark-sensitive payloads](../track_b/native_mark_payloads_v1.md) and [precursor-local payloads](../track_b/native_precursor_payloads_v1.md), together with the optional [finite incidence register](finite_incidence_register.md) and [finite pair-incidence register](finite_pair_incidence_register.md), apply trace-preserving isometric or unitary branch conjugations weighted by the unchanged scalar structural kernel $q(P,r,S)$. Every classical marked-history and unmarked-order probability remains identical to the passive baseline for every normalized quantum input.
2. **Pure classical antichain `Residual -> Order` drift that vanishes above every causal link:** The [active classical residual law](../track_b/native_active_residual_v1.md) (`NM004`) updates a two-state positive vector cone $\mathbb R_+^2$ and shifts structural weights along the terminal four-antichain potential $H_{\rm anti}(P)=a_{|P|}\chi(P)$, audited end-to-end from empty start in [complete-trial source response](native_complete_trial_readout.md). Because $\chi(P)=0$ whenever $P$ contains at least one comparable pair, `NM004` reduces to a forward-only constant-damping channel with zero structural feedback on and above the prepared causal prefix $a\prec b$ used in [prepared source and readout response](native_source_readout_response.md) and [finite interval action and source preparation](finite_interval_action_and_source_preparation.md).

This package resolves whether a single finite-horizon quantum instrument family over the unchanged four-birth domain can close both gaps simultaneously—coupling non-abelian qubit coherence into causal-order growth above $a\prec b$ while encoding precursor-local mark records back into coherent qubit phases, without violating locality, trace normalization, or full entangled diamond commutation.

---

## 1. Classification of mark-independent harmonic potentials and the causal-focusing drift rule

### 1.1 Unchanged structural kernel through four births

Retain verbatim the domain and positive structural kernel $q(P,r,S)>0$ of [Native mark-law geometry, Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix) for all binary-marked finite strict partial orders $(P,\prec,r)$ ($r:P\to\{0,1\}$) of cardinality $|P|\in\{0,1,2,3\}$. A downward-closed subset $S\subseteq P$ ($u\prec v\in S\implies u\in S$, including $S=\varnothing$ and $S=P$) is an eligible precursor ideal; a birth over $S$ adjoins one maximal vertex $x_{\rm new}$ with strict past $\{u\in P:u\prec x_{\rm new}\}=S$, forming $P+S$, and assigns an independently fair newborn bit $b\in\{0,1\}$. The prescribed seed constants are
$$
a_{\rm seed}=\frac{2}{3},\quad c_{\rm seed}=\frac{1}{5},\quad d_{\rm seed}=\frac{1}{4},\quad (f_0,h_0)=\left(\frac{1}{6},\frac{19}{30}\right),\quad (f_1,h_1)=\left(\frac{1}{3},\frac{7}{15}\right),
$$
$$
g_{\rm seed}=\frac{1}{10},\quad k_{\rm seed}=\frac{11}{20},\quad e=\frac{1}{44}.
\tag{1}
$$
At size $0$, $q(\varnothing,\varnothing,\varnothing)=1$. At size $1$ (`singleton` $\{u\}$), $(q(\varnothing),q(\{u\}))=(a_{\rm seed},1-a_{\rm seed})=(\frac{2}{3},\frac{1}{3})$. At size $2$, `2-antichain` $\{u,v\}$ has $(q(\varnothing),q(\{u\}),q(\{v\}),q(\{u,v\}))=(d_{\rm seed},g_{\rm seed},g_{\rm seed},k_{\rm seed})=(\frac{1}{4},\frac{1}{10},\frac{1}{10},\frac{11}{20})$, and `2-chain` $a\prec b$ with root mark $r_a=i\in\{0,1\}$ has $(q(\varnothing),q(\{a\}),q(\{a,b\}))=(c_{\rm seed},f_i,h_i)$. At size $3$, the five unmarked shapes and their complete ideal probability rows are:

| Size-3 parent $P$ | Proper ideals $S\subsetneq P$ and $q(P,r,S)$ | Full ideal $q(P,r,P)$ |
| --- | --- | --- |
| `3-antichain` $\{u,v,w\}$ | $\varnothing$: $\frac{1}{44}$; $\{u\},\{v\},\{w\}$: $\frac{e g_{\rm seed}}{d_{\rm seed}}=\frac{1}{110}$ each; $\{u,v\},\{u,w\},\{v,w\}$: $\frac{e k_{\rm seed}}{d_{\rm seed}}=\frac{1}{20}$ each | $\frac{4}{5}$ |
| `edge+iso` ($u\prec v$, isolate $w$) | $\varnothing,\{w\}$: $\frac{1}{44}$ each; $\{u\}$: $\frac{e f_{r_u}}{c_{\rm seed}}=\frac{5f_{r_u}}{44}$; $\{u,v\}$: $\frac{e h_{r_u}}{c_{\rm seed}}=\frac{5h_{r_u}}{44}$; $\{u,w\}$: $\frac{e k_{\rm seed}}{g_{\rm seed}}=\frac{1}{8}$ | $\frac{65}{88}$ |
| `fork` ($u\prec v,\ u\prec w$) | $\varnothing,\{u\}$: $\frac{1}{44}$ each; $\{u,v\},\{u,w\}$: $\frac{e h_{r_u}}{f_{r_u}}$ ($\frac{19}{220}$ if $r_u=0$; $\frac{7}{220}$ if $r_u=1$) | $\frac{43}{55}$ ($r_u=0$); $\frac{49}{55}$ ($r_u=1$) |
| `join` ($u\prec w,\ v\prec w$) | $\varnothing,\{u\},\{v\},\{u,v\}$: $\frac{1}{44}$ each | $\frac{10}{11}$ |
| `3-chain` ($u\prec v\prec w$) | $\varnothing,\{u\},\{u,v\}$: $\frac{1}{44}$ each | $\frac{41}{44}$ |

Every row is strictly positive and sums to $1$ (for `edge+iso`, $f_0+h_0=\frac{1}{6}+\frac{19}{30}=\frac{4}{5}=f_1+h_1=\frac{1}{3}+\frac{7}{15}$ gives proper sum $\frac{2}{44}+\frac{4}{44}+\frac{1}{8}=\frac{23}{88}$ for both $r_u\in\{0,1\}$).

### 1.2 The 16 unmarked four-element posets and Theorem 1

Let $\mathcal U_n$ denote the set of isomorphism classes of unmarked $n$-element strict partial orders ($|\mathcal U_0|=1$, $|\mathcal U_1|=1$, $|\mathcal U_2|=2$, $|\mathcal U_3|=5$). Every 4-element poset $E$ is classified uniquely by its height $h(E)\in\{1,2,3,4\}$ and its numbers of minimal vertices $|\operatorname{Min}(E)|$, maximal vertices $|\operatorname{Max}(E)|$, and comparable pairs $|\{\prec_E\}|$, yielding $|\mathcal U_4|=16$ non-isomorphic classes:

- **Height $1$ ($1$ class):** $E_{\text{4-antichain}}=A_4$ $(4,4,0)$.
- **Height $2$ ($8$ classes):** $E_{\text{edge+2iso}}=C_2\sqcup A_2$ $(3,3,1)$; $E_{\text{fork+iso}}=(A_1\oplus A_2)\sqcup A_1$ $(2,3,2)$; $E_{\text{join+iso}}=(A_2\oplus A_1)\sqcup A_1$ $(3,2,2)$; $E_{\text{3-claw}}=A_1\oplus A_3$ $(1,3,3)$; $E_{\text{3-join}}=A_3\oplus A_1$ $(3,1,3)$; $E_{\text{2-edges}}=C_2\sqcup C_2$ $(2,2,2)$; $E_{\text{N-poset}}$ ($u_1\prec v_1,v_2,\ u_2\prec v_2$) $(2,2,3)$; $E_{\text{crown}}=A_2\oplus A_2$ $(2,2,4)$.
- **Height $3$ ($6$ classes):** $E_{\text{3chain+iso}}=C_3\sqcup A_1$ $(2,2,3)$; $E_{\text{asym-fork}}=A_1\oplus(C_2\sqcup A_1)$ ($r_*\prec u\prec v,\ r_*\prec w$) $(1,2,4)$; $E_{\text{upper-fork}}=C_2\oplus A_2$ ($r_*\prec u\prec v,w$) $(1,2,5)$; $E_{\text{asym-join}}=(C_2\sqcup A_1)\oplus A_1$ $(2,1,4)$; $E_{\text{lower-join}}=A_2\oplus C_2$ $(2,1,5)$; $E_{\text{diamond}}=A_1\oplus A_2\oplus A_1$ ($r_*\prec u,v\prec w$) $(1,1,5)$.
- **Height $4$ ($1$ class):** $E_{\text{4-chain}}=C_4$ ($r_*\prec u\prec v\prec w$) $(1,1,6)$.

Exactly five classes in $\mathcal U_4$ are single-rooted ($|\operatorname{Min}(E)|=1$): $E_{\text{3-claw}}$ (height $2$), $E_{\text{asym-fork}}$, $E_{\text{upper-fork}}$, $E_{\text{diamond}}$ (height $3$), and $E_{\text{4-chain}}$ (height $4$). The other eleven have $|\operatorname{Min}(E)|\ge 2$.

**Theorem 1 (Classification of mark-independent unmarked harmonic potentials through four births).** *Let $H:\mathcal U_4\to\mathbb R$ be any real-valued function on unmarked 4-element posets. The backward one-step expectations*
$$
\widetilde H(P,r):=\sum_{S\subseteq P}q(P,r,S)\,H(P+S)
\tag{2}
$$
*define mark-independent functions $H(P)=\widetilde H(P,r)$ recursively across all marked parents $(P,r)$ of sizes $|P|=3,2,1,0$ if and only if $H$ satisfies the three linearly independent homogeneous relations*
$$
H(E_{\text{fork+iso}})=H(E_{\text{3chain+iso}}),
\tag{3a}
$$
$$
H(E_{\text{asym-fork}})=H(E_{\text{diamond}}),
\tag{3b}
$$
$$
e\bigl(H(E_{\text{3-claw}})-H(E_{\text{upper-fork}})\bigr)+(1-3e)\bigl(H(E_{\text{diamond}})-H(E_{\text{4-chain}})\bigr)=0,
\tag{3c}
$$
*where (3c) is equivalently $H(E_{\text{3-claw}})-H(E_{\text{upper-fork}})=41\bigl(H(E_{\text{4-chain}})-H(E_{\text{diamond}})\bigr)$ at $e=\frac{1}{44}$. Thus the space of mark-independent unmarked harmonic potentials through four births has exact dimension $16-3=13$.*

**Proof.** Evaluate (2) backwards stage by stage across all unmarked shapes and all markings $r\in\{0,1\}^{|P|}$.

*Stage $|P|=3$:*
1. On `3-antichain`, `join`, and `3-chain`, the kernel $q(P,r,S)$ is independent of $r$ on every ideal $S\subseteq P$. Hence $\widetilde H(P,r)$ is automatically independent of $r$, with
   $$
   H(\text{3-antichain})=\frac{1}{44}H(E_{\text{4-antichain}})+\frac{3}{110}H(E_{\text{edge+2iso}})+\frac{3}{20}H(E_{\text{join+iso}})+\frac{4}{5}H(E_{\text{3-join}}),
   $$
   $$
   H(\text{join})=\frac{1}{44}H(E_{\text{join+iso}})+\frac{1}{22}H(E_{\text{N-poset}})+\frac{1}{44}H(E_{\text{crown}})+\frac{10}{11}H(E_{\text{lower-join}}),
   $$
   $$
   H(\text{3-chain})=e\,H(E_{\text{3chain+iso}})+e\,H(E_{\text{asym-fork}})+e\,H(E_{\text{upper-fork}})+(1-3e)\,H(E_{\text{4-chain}}).
   $$
2. On `edge+iso` ($u\prec v$, isolate $w$), the six ideals send $P+S$ respectively to $E_{\text{edge+2iso}}$ ($S=\varnothing$), $E_{\text{2-edges}}$ ($S=\{w\}$), $E_{\text{fork+iso}}$ ($S=\{u\}$), $E_{\text{3chain+iso}}$ ($S=\{u,v\}$), $E_{\text{N-poset}}$ ($S=\{u,w\}$), and $E_{\text{asym-join}}$ ($S=\{u,v,w\}$). Only $S=\{u\}$ and $S=\{u,v\}$ depend on $r$, solely through $r_u\in\{0,1\}$:
   $$
   \widetilde H(\text{edge+iso},r)=e\,H(E_{\text{edge+2iso}})+e\,H(E_{\text{2-edges}})+\frac{1}{8}H(E_{\text{N-poset}})+\frac{65}{88}H(E_{\text{asym-join}})+5e\bigl(f_{r_u}H(E_{\text{fork+iso}})+h_{r_u}H(E_{\text{3chain+iso}})\bigr).
   $$
   Since $f_1-f_0=\frac{1}{3}-\frac{1}{6}=\frac{1}{6}$ and $h_1-h_0=\frac{7}{15}-\frac{19}{30}=-\frac{1}{6}$, the mark contrast is
   $$
   \widetilde H(\text{edge+iso},r_u=1)-\widetilde H(\text{edge+iso},r_u=0)=\frac{5e}{6}\bigl(H(E_{\text{fork+iso}})-H(E_{\text{3chain+iso}})\bigr)=\frac{5}{264}\bigl(H(E_{\text{fork+iso}})-H(E_{\text{3chain+iso}})\bigr).
   $$
   Hence $\widetilde H(\text{edge+iso},r)$ is mark-independent if and only if (3a) holds; under (3a), $f_{r_u}+h_{r_u}=\frac{4}{5}$ gives $5e(f_{r_u}+h_{r_u})=4e=\frac{1}{11}$ for both $r_u\in\{0,1\}$.
3. On `fork` ($u\prec v,\ u\prec w$), the five ideals send $P+S$ to $E_{\text{fork+iso}}$ ($S=\varnothing$), $E_{\text{3-claw}}$ ($S=\{u\}$), $E_{\text{asym-fork}}$ ($S=\{u,v\}$ and $S=\{u,w\}$), and $E_{\text{diamond}}$ ($S=\{u,v,w\}$). Using $q(\{u,v,w\})=1-2e-2e\frac{h_{r_u}}{f_{r_u}}$,
   $$
   \widetilde H(\text{fork},r)=e\,H(E_{\text{fork+iso}})+e\,H(E_{\text{3-claw}})+(1-2e)\,H(E_{\text{diamond}})+2e\frac{h_{r_u}}{f_{r_u}}\bigl(H(E_{\text{asym-fork}})-H(E_{\text{diamond}})\bigr).
   $$
   Because $\frac{h_1}{f_1}-\frac{h_0}{f_0}=\frac{7}{5}-\frac{19}{5}=-\frac{12}{5}\ne 0$ (contrast coefficient $-\frac{6}{55}\ne 0$), $\widetilde H(\text{fork},r)$ is mark-independent if and only if (3b) holds, in which case
   $$
   H(\text{fork})=e\,H(E_{\text{fork+iso}})+e\,H(E_{\text{3-claw}})+(1-2e)\,H(E_{\text{diamond}}).
   $$

*Stage $|P|=2$:* Assuming (3a)–(3b) so $H:\mathcal U_3\to\mathbb R$ is well-defined:
1. On `2-antichain`, $q$ is independent of $r$, so $\widetilde H(\text{2-antichain},r)=\frac{1}{4}H(\text{3-antichain})+\frac{1}{5}H(\text{edge+iso})+\frac{11}{20}H(\text{join})$ is automatically mark-independent.
2. On `2-chain` ($a\prec b$), the three ideals send $P+S$ to `edge+iso` ($S=\varnothing$, weight $\frac{1}{5}$), `fork` ($S=\{a\}$, weight $f_{r_a}$), and `3-chain` ($S=\{a,b\}$, weight $h_{r_a}$). Taking the root-mark contrast gives
   $$
   \widetilde H(\text{2-chain},r_a=1)-\widetilde H(\text{2-chain},r_a=0)=\frac{1}{6}\bigl(H(\text{fork})-H(\text{3-chain})\bigr).
   $$
   Thus $\widetilde H(\text{2-chain},r)$ is mark-independent if and only if $H(\text{fork})=H(\text{3-chain})$. Subtracting the formulas for $H(\text{3-chain})$ and $H(\text{fork})$ and applying (3a) ($H(E_{\text{fork+iso}})=H(E_{\text{3chain+iso}})$) and (3b) ($H(E_{\text{asym-fork}})=H(E_{\text{diamond}})$, so $(1-2e)H(E_{\text{diamond}})-eH(E_{\text{asym-fork}})=(1-3e)H(E_{\text{diamond}})$) yields
   $$
   H(\text{fork})-H(\text{3-chain})=e\bigl(H(E_{\text{3-claw}})-H(E_{\text{upper-fork}})\bigr)+(1-3e)\bigl(H(E_{\text{diamond}})-H(E_{\text{4-chain}})\bigr),
   $$
   which vanishes if and only if (3c) holds. Since $\frac{1-3e}{e}=\frac{41/44}{1/44}=41$, (3c) is equivalently $H(E_{\text{3-claw}})-H(E_{\text{upper-fork}})=41\bigl(H(E_{\text{4-chain}})-H(E_{\text{diamond}})\bigr)$. Under (3c), $f_{r_a}+h_{r_a}=\frac{4}{5}$ gives $H(\text{2-chain})=\frac{1}{5}H(\text{edge+iso})+\frac{4}{5}H(\text{3-chain})$.

*Stages $|P|=1$ and $|P|=0$:* On `singleton`, $q=(\frac{2}{3},\frac{1}{3})$ is mark-independent, giving $H(\text{singleton})=\frac{2}{3}H(\text{2-antichain})+\frac{1}{3}H(\text{2-chain})$. At $\varnothing$, $q=1$ gives $H(\varnothing)=H(\text{singleton})$. Finally, (3a), (3b), and (3c) act on disjoint pivot variables $H(E_{\text{fork+iso}})$, $H(E_{\text{asym-fork}})$, and $H(E_{\text{3-claw}})$, so they have rank $3$ and kernel dimension $16-3=13$. $\blacksquare$

*Remark (Why `NM004` is passive above $a\prec b$, and stage $3\to 4$ chain-vs-diamond splitting).* The antichain indicator $H_{\rm anti}(E):=\mathbf 1_{\{E=E_{\text{4-antichain}}\}}$ of [active classical residual law](../track_b/native_active_residual_v1.md) vanishes on all seven posets appearing in (3a)–(3c), recovering $(H_{\rm anti}(\varnothing),H_{\rm anti}(A_1),H_{\rm anti}(A_2),H_{\rm anti}(A_3),H_{\rm anti}(A_4))=(\frac{1}{264},\frac{1}{264},\frac{1}{176},\frac{1}{44},1)$ while giving $H_{\rm anti}(P)=0$ on every poset containing a comparable pair—in particular $H_{\rm anti}(a\prec b)=0$ and $H_{\rm anti}(E)=0$ on all continuations above $a\prec b$. Conversely, the 13-dimensional subspace of Theorem 1 contains potentials supported entirely on single-rooted causal orders, including both our canonical $[0,1]$-valued indicator $H_{\rm foc}$ below and the companion $[0,1]$-valued chain-splitting basis vector $H_{\rm ch}$ defined by $H_{\rm ch}(E_{\text{3-claw}})=H_{\rm ch}(E_{\text{4-chain}})=1$, $H_{\rm ch}(E_{\text{diamond}})=H_{\rm ch}(E_{\text{asym-fork}})=\frac{40}{41}$, and $H_{\rm ch}(E)=0$ on all other twelve classes in $\mathcal U_4$ (including $E_{\text{upper-fork}}$), which satisfies $1-0=41(1-\frac{40}{41})$ in (3c) with $H_{\rm ch}(\text{fork})=H_{\rm ch}(\text{3-chain})=\frac{1721}{1804}$ and splits `4-chain` from `diamond` even at the final step $3\to 4$.

### 1.3 Canonical causal-focusing potential $H_{\rm foc}$ and current-prefix coefficient $r_P(S)$

Fix the canonical $[0,1]$-valued binary indicator solution $H_{\rm foc}:\mathcal U_4\to\{0,1\}$ by setting
$$
H_{\rm foc}(E):=
\begin{cases}
1, & E\in\{E_{\text{asym-fork}},\,E_{\text{diamond}},\,E_{\text{4-chain}}\},\\
0, & \text{for all other } 13 \text{ classes } E\in\mathcal U_4
\end{cases}
\tag{4}
$$
(that is, $H_{\rm foc}(E)=1$ on the single-rooted height-$\ge 3$ unmarked size-4 posets excluding $E_{\text{upper-fork}}$, and $0$ on all unrooted posets $|\operatorname{Min}(E)|\ge 2$, $E_{\text{3-claw}}$, and $E_{\text{upper-fork}}$). Equation (4) satisfies (3a) ($0=0$), (3b) ($1=1$), and (3c) ($0-0=41(1-1)=0$). Evaluating Theorem 1's backward formulas yields $H_{\rm foc}(P)$ on every unmarked poset of sizes $0,1,2,3$:

- **Size $3$:** Every child of `3-antichain`, `edge+iso`, and `join` has $|\operatorname{Min}|\ge 2$, so
  $$
  H_{\rm foc}(\text{3-antichain})=H_{\rm foc}(\text{edge+iso})=H_{\rm foc}(\text{join})=0,
  \qquad
  H_{\rm foc}(\text{fork})=H_{\rm foc}(\text{3-chain})=1-2e=\frac{21}{22}.
  $$
- **Size $2$:** $H_{\rm foc}(\text{2-antichain})=0$, and $H_{\rm foc}(\text{2-chain})=\frac{1}{5}\cdot 0+\frac{4}{5}\cdot\frac{21}{22}=\frac{42}{55}$.
- **Sizes $1$ and $0$:** $H_{\rm foc}(\text{singleton})=\frac{2}{3}\cdot 0+\frac{1}{3}\cdot\frac{42}{55}=\frac{14}{55}=H_{\rm foc}(\varnothing)$.

Fix $\theta:=\frac{1}{32}$ and define for every unmarked parent $P$ ($|P|\le 3$) and downward ideal $S\subseteq P$ the current-prefix drift coefficient
$$
r_P(S):=\theta\,2^{|P|}\bigl[H_{\rm foc}(P+S)-H_{\rm foc}(P)\bigr].
\tag{5}
$$
Equation (5) is an explicit finite lookup table on the current unmarked pair $(P,S)$ alone; it reads zero vertex marks and consults no future outcome or terminal oracle:

| $\lvert P\rvert$ | Unmarked parent $P$ | $H_{\rm foc}(P)$ | Ideal $S\subseteq P$ and explicit $r_P(S)$ |
| :---: | --- | :---: | --- |
| $0$ | $\varnothing$ | $\frac{14}{55}$ | $S=\varnothing$: $r_\varnothing(\varnothing)=0$ |
| $1$ | `singleton` $\{u\}$ | $\frac{14}{55}$ | $S=\varnothing$: $-\frac{7}{440}$; $S=\{u\}$: $+\frac{7}{220}$ |
| $2$ | `2-antichain` $\{u,v\}$ | $0$ | all four ideals $S\subseteq P$: $r_P(S)=0$ |
| $2$ | `2-chain` $a\prec b$ | $\frac{42}{55}$ | $S=\varnothing$: $-\frac{21}{220}$; $S=\{a\}$: $+\frac{21}{880}$; $S=\{a,b\}$: $+\frac{21}{880}$ |
| $3$ | `3-antichain`, `edge+iso`, `join` | $0$ | all ideals $S\subseteq P$: $r_P(S)=0$ |
| $3$ | `fork` ($u\prec v,\ u\prec w$) | $\frac{21}{22}$ | $S\in\{\varnothing,\{u\}\}$: $-\frac{21}{88}$; $S\in\{\{u,v\},\{u,w\},\{u,v,w\}\}$: $+\frac{1}{88}$ |
| $3$ | `3-chain` ($u\prec v\prec w$) | $\frac{21}{22}$ | $S\in\{\varnothing,\{u,v\}\}$: $-\frac{21}{88}$; $S\in\{\{u\},\{u,v,w\}\}$: $+\frac{1}{88}$ |

Across the entire domain $|P|\le 3$,
$$
|r_P(S)|\le 8\theta\cdot\frac{21}{22}=\frac{21}{88}<\frac{1}{4}<\frac{1}{2},
\qquad
\sum_{S\subseteq P}q(P,r,S)\,r_P(S)=\theta\,2^{|P|}\Bigl(\sum_{S\subseteq P}q(P,r,S)H_{\rm foc}(P+S)-H_{\rm foc}(P)\Bigr)=0
\tag{6}
$$
for every marked parent $(P,r)$.

---

## 2. Non-abelian co-rotating five-Kraus quantum instrument and complete positivity

### 2.1 Co-rotating Clifford unitary and stage Pauli axes

Supply a fixed two-dimensional complex Hilbert space $\mathcal H_Q=\mathbb C^2$ with standard orthonormal basis $\{|0\rangle,|1\rangle\}$, trivial vertex-relabeling action, and standard Pauli matrices
$$
X=\begin{pmatrix}0&1\\ 1&0\end{pmatrix},\qquad
Y=\begin{pmatrix}0&-i\\ i&0\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\ 0&-1\end{pmatrix}.
$$
Define the Clifford axis-cycling operator
$$
U_*:=e^{-i\frac{\pi}{4}Z}e^{-i\frac{\pi}{4}X}
=\frac{1}{\sqrt 2}\begin{pmatrix}1-i&0\\ 0&1+i\end{pmatrix}
 \frac{1}{\sqrt 2}\begin{pmatrix}1&-i\\ -i&1\end{pmatrix}
=\frac{1}{2}\begin{pmatrix}1-i & -1-i\\ 1-i & 1+i\end{pmatrix}.
\tag{7}
$$

**Lemma 1 (Direct $2\times 2$ verification of $U_*$).** *The matrix $U_*$ in (7) satisfies $U_*U_*^\dagger=U_*^\dagger U_*=I$, $U_*^2=-U_*^\dagger$, $U_*^3=-I$ (hence $\operatorname{Ad}_{U_*}^3=\operatorname{id}$), and*
$$
U_*XU_*^\dagger=Y,\qquad U_*YU_*^\dagger=Z,\qquad U_*ZU_*^\dagger=X.
\tag{8}
$$

**Proof.** With $U_*^\dagger=\frac{1}{2}\bigl(\begin{smallmatrix}1+i&1+i\\ -1+i&1-i\end{smallmatrix}\bigr)$, direct $2\times 2$ multiplication gives
$$
U_*U_*^\dagger=\frac{1}{4}\begin{pmatrix}|1-i|^2+|1+i|^2 & (1-i)(1+i)-(1+i)(1-i)\\ (1-i)(1+i)-(1+i)(1-i) & |1-i|^2+|1+i|^2\end{pmatrix}=\frac{1}{4}\begin{pmatrix}4&0\\ 0&4\end{pmatrix}=I,
$$
and
$$
U_*^2=\frac{1}{4}\begin{pmatrix}(1-i)^2-(1+i)(1-i) & -(1-i)(1+i)-(1+i)^2\\ (1-i)^2+(1+i)(1-i) & -(1-i)(1+i)+(1+i)^2\end{pmatrix}
=\frac{1}{4}\begin{pmatrix}-2i-2 & -2-2i\\ -2i+2 & -2+2i\end{pmatrix}
=\frac{1}{2}\begin{pmatrix}-1-i & -1-i\\ 1-i & -1+i\end{pmatrix}=-U_*^\dagger,
$$
so $U_*^3=U_*^2U_*=-U_*^\dagger U_*=-I$ and $\operatorname{Ad}_{U_*}^3(A)=(-I)A(-I)^\dagger=A$. Next,
$$
U_*XU_*^\dagger=\frac{1}{4}\begin{pmatrix}-1-i & 1-i\\ 1+i & 1-i\end{pmatrix}\begin{pmatrix}1+i & 1+i\\ -1+i & 1-i\end{pmatrix}
=\frac{1}{4}\begin{pmatrix}-2i+2i & -2i-2i\\ 2i+2i & 2i-2i\end{pmatrix}=\begin{pmatrix}0&-i\\ i&0\end{pmatrix}=Y,
$$
$$
U_*ZU_*^\dagger=\frac{1}{4}\begin{pmatrix}1-i & 1+i\\ 1-i & -1-i\end{pmatrix}\begin{pmatrix}1+i & 1+i\\ -1+i & 1-i\end{pmatrix}
=\frac{1}{4}\begin{pmatrix}2-2 & 2+2\\ 2+2 & 2-2\end{pmatrix}=\begin{pmatrix}0&1\\ 1&0\end{pmatrix}=X,
$$
and since $Y=-iZX$, unitarity gives $U_*YU_*^\dagger=-i(U_*ZU_*^\dagger)(U_*XU_*^\dagger)=-iXY=-i(iZ)=Z$. $\blacksquare$

Define the stage-indexed Pauli observables $\Sigma_0:=Y$ and $\Sigma_n:=U_*^n\Sigma_0(U_*^\dagger)^n$ for $n\ge 0$. By Lemma 1,
$$
(\Sigma_0,\Sigma_1,\Sigma_2,\Sigma_3,\Sigma_4)=(Y,\,Z,\,X,\,Y,\,Z).
\tag{9}
$$
In particular, across the three active internal parent sizes $n=1,2,3$ where $r_P(S)$ is non-identically zero (`singleton` at $n=1$, `2-chain` $a\prec b$ at $n=2$, and `fork` / `3-chain` at $n=3$), $(\Sigma_1,\Sigma_2,\Sigma_3)=(Z,X,Y)$ spans all three pairwise non-commuting Pauli axes.

### 2.2 Precursor-local phases and branch superoperator definition

For each downward ideal $S\subseteq P$ and marking $r:P\to\{0,1\}$, let $K(S,r|_S)$ denote the isomorphism class of the induced marked strict precursor $(S,\prec|_S,r|_S)$. Let $\{\varphi_{K,b}\}_{(K,b)}\subseteq(-\pi,\pi]$ be any supplied family of real phase angles indexed solely by intrinsic marked precursor class $K$ and newborn bit $b\in\{0,1\}$. For our explicit rational witnesses in Section 4, let $K_0$ denote the class of a single vertex marked $0$ (matching the local trigger of [precursor-local payloads](../track_b/native_precursor_payloads_v1.md)) and fix
$$
\varphi_{K,b}:=
\begin{cases}
\varphi_0, & K=K_0\text{ and }b=0,\\
0, & \text{otherwise},
\end{cases}
\qquad \varphi_0\in(0,\pi].
\tag{10}
$$
For stage $n\in\{0,1,2,3\}$, precursor class $K$, bit $b\in\{0,1\}$, and real drift $|r|<\frac{1}{2}$, define on $\mathcal B(\mathcal H_Q)=M_2(\mathbb C)$ the step unitary, core map, and branch superoperator:
$$
U_{n,K,b}:=U_*\exp\!\left(-i\frac{\varphi_{K,b}}{2}\Sigma_n\right),
\qquad
\mathcal M(r,\Sigma_n,U_{n,K,b})(A):=\frac{1}{2}U_{n,K,b}AU_{n,K,b}^\dagger+\frac{1}{4}\operatorname{Tr}\bigl[(I_Q+2r\Sigma_n)A\bigr]I_Q,
\tag{11}
$$
$$
\mathcal B^{P,r}_{S,b}(A):=\frac{1}{2}q(P,r,S)\,\mathcal M\bigl(r_P(S),\,\Sigma_{|P|},\,U_{|P|,K(S,r|_S),b}\bigr)(A)
\qquad (|P|\le 3).
\tag{12}
$$

**Theorem 2 (Five-Kraus representation, exact Choi spectrum, trace preservation, locality, and equivariance).** *Fix any stage $n\in\{0,1,2,3\}$, Pauli axis $\Sigma_n$ with orthonormal eigenbasis $\{|\psi_{n,+}\rangle,|\psi_{n,-}\rangle\}$ ($\Sigma_n|\psi_{n,\pm}\rangle=\pm|\psi_{n,\pm}\rangle$), unitary $U=U_{n,K,b}$, and real parameter $|r|<\frac{1}{2}$.*

1. *(Explicit Kraus representation and dual effect.)* *The five operators on $\mathcal H_Q=\mathbb C^2$ given by*
   $$
   L_0:=\frac{1}{\sqrt 2}U,\qquad
   L_{\alpha,\beta}:=\frac{\sqrt{1+2\alpha r}}{2}\,|\beta\rangle\langle\psi_{n,\alpha}|\qquad (\alpha\in\{+,-\},\ \beta\in\{0,1\})
   \tag{13}
   $$
   *satisfy*
   $$
   L_0AL_0^\dagger+\sum_{\alpha\in\{+,-\}}\sum_{\beta\in\{0,1\}}L_{\alpha,\beta}AL_{\alpha,\beta}^\dagger=\mathcal M(r,\Sigma_n,U)(A),
   \qquad
   L_0^\dagger L_0+\sum_{\alpha\in\{+,-\}}\sum_{\beta\in\{0,1\}}L_{\alpha,\beta}^\dagger L_{\alpha,\beta}=I_Q+r\Sigma_n.
   \tag{14}
   $$
2. *(Exact $4\times 4$ Choi matrix eigenvalues and strict complete positivity.)* *Let $|\Omega\rangle:=|0\rangle\otimes|0\rangle+|1\rangle\otimes|1\rangle\in\mathbb C^2\otimes\mathbb C^2$. The $4\times 4$ Choi matrix $J(\mathcal M):=(\mathcal M(r,\Sigma_n,U)\otimes\operatorname{id}_{\mathbb C^2})(|\Omega\rangle\langle\Omega|)$ has exact spectrum*
   $$
   \operatorname{Spec}\bigl(J(\mathcal M)\bigr)=\left\{\frac{1-2r}{4},\ \frac{1+2r}{4},\ \frac{3-2\sqrt{1+r^2}}{4},\ \frac{3+2\sqrt{1+r^2}}{4}\right\},
   \tag{15}
   $$
   *independent of $U$ and $n$, with minimum eigenvalue $\lambda_{\min}(J(\mathcal M))=\frac{1-2|r|}{4}>0$. In particular, since $|r_P(S)|\le\frac{21}{88}<\frac{1}{2}$, every branch superoperator $\mathcal B^{P,r}_{S,b}$ is strictly completely positive ($J(\mathcal B^{P,r}_{S,b})\succeq\frac{23}{352}q(P,r,S)I_4\succ 0$).*
3. *(Trace preservation, strict branch positivity, locality, anchor, and equivariance.)* *For every finite-dimensional reference Hilbert space $\mathcal H_{\rm ref}$, every marked parent $(P,r)$ ($|P|\le 3$), and every $\rho_{Q,\rm ref}\in\mathcal D(\mathcal H_Q\otimes\mathcal H_{\rm ref})$:*
   $$
   \sum_{S\subseteq P}\sum_{b\in\{0,1\}}\operatorname{Tr}\bigl[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr]=\operatorname{Tr}(\rho_{Q,\rm ref})=1,
   \tag{16}
   $$
   $$
   \operatorname{Tr}\bigl[(\mathcal B^{P,r}_{S,b}\otimes\operatorname{id}_{\rm ref})(\rho_{Q,\rm ref})\bigr]
   =\frac{1}{2}q(P,r,S)\Bigl(1+r_P(S)\operatorname{Tr}\bigl[(\Sigma_{|P|}\otimes I_{\rm ref})\rho_{Q,\rm ref}\bigr]\Bigr)
   \ge\frac{67}{176}q(P,r,S)>0.
   \tag{17}
   $$
   *Moreover, $\mathcal B^{P,r}_{S,b}(I_Q/2)=\frac{1}{2}q(P,r,S)(I_Q/2)$; for proper ideals $S\subsetneq P$, $\mathcal B^{P,r}_{S,b}$ depends on $r$ solely through $r|_S$ (and on full ideals $S=P$ through $r$); and $\mathcal B^{P',r'}_{\pi(S),b}=\mathcal B^{P,r}_{S,b}$ for every order-and-mark isomorphism $\pi:(P,r)\xrightarrow{\sim}(P',r')$.*

**Proof.**
1. Because $|r|<\frac{1}{2}$, $1+2\alpha r>0$ for $\alpha\in\{+,-\}$. Using $\sum_{\beta=0}^1|\beta\rangle\langle\beta|=I_Q$ and $\sum_{\alpha=\pm}(1+2\alpha r)|\psi_{n,\alpha}\rangle\langle\psi_{n,\alpha}|=I_Q+2r\Sigma_n$, we compute for any $A\in M_2(\mathbb C)$:
   $$
   L_0AL_0^\dagger+\sum_{\alpha,\beta}L_{\alpha,\beta}AL_{\alpha,\beta}^\dagger
   =\frac{1}{2}UAU^\dagger+\sum_{\alpha=\pm}\frac{1+2\alpha r}{4}\langle\psi_{n,\alpha}|A|\psi_{n,\alpha}\rangle\sum_{\beta=0}^1|\beta\rangle\langle\beta|
   =\frac{1}{2}UAU^\dagger+\frac{1}{4}\operatorname{Tr}\bigl[(I_Q+2r\Sigma_n)A\bigr]I_Q.
   $$
   Similarly, $L_0^\dagger L_0=\frac{1}{2}U^\dagger U=\frac{1}{2}I_Q$ and $\sum_{\alpha,\beta}L_{\alpha,\beta}^\dagger L_{\alpha,\beta}=\sum_{\alpha=\pm}\frac{1+2\alpha r}{2}|\psi_{n,\alpha}\rangle\langle\psi_{n,\alpha}|=\frac{1}{2}I_Q+r\Sigma_n$, summing to $I_Q+r\Sigma_n$. In general, the Hilbert–Schmidt adjoint $\mathcal M^\dagger$ obeys $\operatorname{Tr}[B\,\mathcal M(A)]=\operatorname{Tr}[\mathcal M^\dagger(B)A]$ with
   $$
   \mathcal M(r,\Sigma_n,U)^\dagger(B)=\frac{1}{2}U^\dagger BU+\frac{\operatorname{Tr}(B)}{4}(I_Q+2r\Sigma_n).
   \tag{18}
   $$
2. Expanding $|\Omega\rangle\langle\Omega|=\sum_{j,k=0}^1|j\rangle\langle k|\otimes|j\rangle\langle k|$ gives
   $$
   J(\mathcal M)=\frac{1}{2}(U\otimes I_2)|\Omega\rangle\langle\Omega|(U^\dagger\otimes I_2)+\frac{1}{4}\sum_{j,k=0}^1\langle k|(I_Q+2r\Sigma_n)|j\rangle\,I_2\otimes|j\rangle\langle k|
   =|\Phi_U\rangle\langle\Phi_U|+\frac{1}{4}I_2\otimes\bigl(I_2+2r\Sigma_n^T\bigr),
   $$
   where $|\Phi_U\rangle:=\frac{1}{\sqrt 2}(U\otimes I_2)|\Omega\rangle$ is a unit vector ($\|\Phi_U\|^2=\frac{1}{2}\langle\Omega|\Omega\rangle=1$). Let $|\chi_\alpha\rangle:=\overline{|\psi_{n,\alpha}\rangle}$ ($\alpha\in\{+,-\}$), which forms an orthonormal eigenbasis of $\Sigma_n^T$ ($\Sigma_n^T|\chi_\pm\rangle=\overline{\Sigma_n|\psi_{n,\pm}\rangle}=\pm|\chi_\pm\rangle$), and set $|u_\alpha\rangle:=U|\psi_{n,\alpha}\rangle$, an orthonormal basis of $\mathbb C^2$. Since $|\Omega\rangle=|\psi_{n,+}\rangle\otimes|\chi_+\rangle+|\psi_{n,-}\rangle\otimes|\chi_-\rangle$, we have $|\Phi_U\rangle=\frac{1}{\sqrt 2}(|u_+\rangle\otimes|\chi_+\rangle+|u_-\rangle\otimes|\chi_-\rangle)$. In the orthonormal basis
   $$
   |f_1\rangle:=|u_+\rangle\otimes|\chi_+\rangle,\quad
   |f_2\rangle:=|u_-\rangle\otimes|\chi_-\rangle,\quad
   |f_3\rangle:=|u_+\rangle\otimes|\chi_-\rangle,\quad
   |f_4\rangle:=|u_-\rangle\otimes|\chi_+\rangle
   $$
   of $\mathbb C^2\otimes\mathbb C^2$, $|\Phi_U\rangle$ is orthogonal to $|f_3\rangle$ and $|f_4\rangle$, so $J(\mathcal M)$ decomposes into the $2\oplus 1\oplus 1$ block-diagonal matrix
   $$
   J(\mathcal M)\cong
   \begin{pmatrix}
   \frac{3+2r}{4} & \frac{1}{2} & 0 & 0\\
   \frac{1}{2} & \frac{3-2r}{4} & 0 & 0\\
   0 & 0 & \frac{1-2r}{4} & 0\\
   0 & 0 & 0 & \frac{1+2r}{4}
   \end{pmatrix}.
   $$
   The $1\times 1$ blocks yield eigenvalues $\frac{1-2r}{4}$ and $\frac{1+2r}{4}$; the $2\times 2$ block has trace $\frac{3}{2}$ and determinant $\frac{9-4r^2}{16}-\frac{1}{4}=\frac{5-4r^2}{16}$, giving roots $\frac{1}{2}\bigl(\frac{3}{2}\pm\sqrt{\frac{9}{4}-\frac{5-4r^2}{4}}\bigr)=\frac{3\pm 2\sqrt{1+r^2}}{4}$ and proving (15). Since $\sqrt{1+r^2}\le 1+|r|$ for all $r\in\mathbb R$, $3-2\sqrt{1+r^2}\ge 1-2|r|$, so $\lambda_{\min}(J(\mathcal M))=\frac{1-2|r|}{4}>0$ for all $|r|<\frac{1}{2}$. With $|r_P(S)|\le\frac{21}{88}$, $\lambda_{\min}(J(\mathcal M))\ge\frac{1-42/88}{4}=\frac{23}{176}$, hence $J(\mathcal B^{P,r}_{S,b})=\frac{1}{2}q(P,r,S)J(\mathcal M)\succeq\frac{23}{352}q(P,r,S)I_4\succ 0$.
3. On $\mathcal H_Q\otimes\mathcal H_{\rm ref}$, $(\mathcal M(r,\Sigma_n,U)\otimes\operatorname{id}_{\rm ref})(X)=\frac{1}{2}(U\otimes I_{\rm ref})X(U^\dagger\otimes I_{\rm ref})+\frac{1}{4}I_Q\otimes\operatorname{Tr}_Q[((I_Q+2r\Sigma_n)\otimes I_{\rm ref})X]$. Taking $\operatorname{Tr}_{Q,\rm ref}$ and using $\operatorname{Tr}_Q(I_Q)=2$ gives $\operatorname{Tr}_{Q,\rm ref}[(\mathcal M\otimes\operatorname{id}_{\rm ref})(X)]=\operatorname{Tr}_{Q,\rm ref}[((I_Q+r\Sigma_n)\otimes I_{\rm ref})X]$. Multiplying by $\frac{1}{2}q(P,r,S)$ establishes the equality in (17); because $\|\Sigma_{|P|}\|_{\rm op}=1$ and $|r_P(S)|\le\frac{21}{88}$, $1+r_P(S)\operatorname{Tr}[(\Sigma_{|P|}\otimes I_{\rm ref})\rho_{Q,\rm ref}]\ge 1-\frac{21}{88}=\frac{67}{88}$, giving the lower bound $\frac{67}{176}q(P,r,S)>0$. Summing (17) over $b\in\{0,1\}$ (factor $2$) and $S\subseteq P$ uses $\sum_S q(P,r,S)=1$ and $\sum_S q(P,r,S)r_P(S)=0$ from (6) to yield (16). Evaluating on $I_Q/2$ uses $\operatorname{Tr}(\Sigma_{|P|})=0$ to give $\mathcal M(r,\Sigma_{|P|},U)(I_Q/2)=\frac{1}{4}I_Q+\frac{1}{4}I_Q=I_Q/2$. Finally, $r_P(S)$ and $\Sigma_{|P|}$ depend only on the unmarked pair $(P,S)$, $U_{|P|,K(S,r|_S),b}$ depends on $r$ only through the isomorphism class $K(S,r|_S)$, and $q(P,r,S)$ satisfies Part A locality and marked-parent relabeling equivariance; hence $\mathcal B^{P,r}_{S,b}$ satisfies proper-slot mark locality, full-slot admissibility, and relabeling equivariance. $\blacksquare$

---

## 3. Exact non-abelian diamond commutation, history closed form, martingale law, and classical reduction obstruction

### 3.1 Closed-form $m$-birth history superoperator and diamond commutation

**Theorem 3 (Closed-form $m$-birth history superoperator and exact diamond commutation on $\mathcal H_Q\otimes\mathcal H_{\rm ref}$).**
1. *(Co-rotation intertwining identities.)* *For every stage $n\ge 0$, precursor classes $K,K'$, and bits $b,c\in\{0,1\}$,*
   $$
   U_{n,K,b}^\dagger\,\Sigma_{n+1}\,U_{n,K,b}=\Sigma_n,
   \qquad
   U_{n+1,K',c}\,U_{n,K,b}=U_*^2\exp\!\left(-i\frac{\varphi_{K,b}+\varphi_{K',c}}{2}\Sigma_n\right),
   \tag{19}
   $$
   *and for any $m$-step sequence $(K_0,b_0),\dots,(K_{m-1},b_{m-1})$ with total phase $\Phi:=\sum_{j=0}^{m-1}\varphi_{K_j,b_j}$,*
   $$
   U_{n+m-1,K_{m-1},b_{m-1}}\cdots U_{n,K_0,b_0}=U_*^m\exp\!\left(-i\frac{\Phi}{2}\Sigma_n\right).
   \tag{20}
   $$
2. *(Closed-form $m$-birth history superoperator.)* *Let $h=\bigl((S_0,b_0),\dots,(S_{m-1},b_{m-1})\bigr)$ ($m\ge 1$) be any supported $m$-birth history from marked parent $(C,r)$ ($|C|=n$, $n+m\le 4$) through intermediate marked orders $(P_j,r_j)$ ($|P_j|=n+j$) to unmarked endpoint $E=P_m$, with structural weight product $W_{\rm str}(h):=\prod_{j=0}^{m-1}q(P_j,r_j,S_j)$ and total precursor phase $\Phi_h:=\sum_{j=0}^{m-1}\varphi_{K(S_j,r_j|_{S_j}),b_j}$. Then the composed unnormalized superoperator $\mathcal B_h:=\mathcal B^{P_{m-1},r_{m-1}}_{S_{m-1},b_{m-1}}\circ\cdots\circ\mathcal B^{P_0,r_0}_{S_0,b_0}$ satisfies, for all $X\in\mathcal B(\mathcal H_Q\otimes\mathcal H_{\rm ref})$,*
   $$
   (\mathcal B_h\otimes\operatorname{id}_{\rm ref})(X)=2^{-m}W_{\rm str}(h)\left\{2^{-m}\bigl(U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}\otimes I_{\rm ref}\bigr)X\bigl(e^{+i\frac{\Phi_h}{2}\Sigma_n}(U_*^\dagger)^m\otimes I_{\rm ref}\bigr)+\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q\!\left[\Bigl(\bigl((1-2^{-m})I_Q+\theta\,2^n\bigl(H_{\rm foc}(E)-H_{\rm foc}(C)\bigr)\Sigma_n\bigr)\otimes I_{\rm ref}\Bigr)X\right]\right\}.
   \tag{21}
   $$
3. *(Exact diamond and transported-suffix commutation.)* *For every marked base $(C,r)$ of size $|C|\le 2$, every pair of downward ideals $S,T\subseteq C$ (including $S=T$, empty ideals, and full ideals $S=C$ becoming proper in $C+y_T$), and all newborn bits $b,c\in\{0,1\}$, after the canonical newborn-swap identification of $C+x_S+y_T$ with $C+y_T+x_S$,*
   $$
   \bigl(\mathcal B^{C+x_S,r+b_x}_{T,c}\circ\mathcal B^{C,r}_{S,b}\bigr)\otimes\operatorname{id}_{\rm ref}
   =
   \bigl(\mathcal B^{C+y_T,r+c_y}_{S,b}\circ\mathcal B^{C,r}_{T,c}\bigr)\otimes\operatorname{id}_{\rm ref}
   \tag{22}
   $$
   *as exact unnormalized superoperators on $\mathcal B(\mathcal H_Q\otimes\mathcal H_{\rm ref})$, and this equality persists after composing any transported suffix within the four-birth horizon.*

**Proof.**
1. By definition $\Sigma_{n+1}=U_*\Sigma_nU_*^\dagger$, so $U_*^\dagger\Sigma_{n+1}U_*=\Sigma_n$. Conjugating by $e^{-i\frac{\varphi_{K,b}}{2}\Sigma_n}$ (which commutes with $\Sigma_n$) gives $U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=e^{+i\frac{\varphi_{K,b}}{2}\Sigma_n}\Sigma_n e^{-i\frac{\varphi_{K,b}}{2}\Sigma_n}=\Sigma_n$. Likewise, $e^{-i\frac{\alpha}{2}\Sigma_{n+1}}=U_*e^{-i\frac{\alpha}{2}\Sigma_n}U_*^\dagger$ implies $e^{-i\frac{\alpha}{2}\Sigma_{n+1}}U_*=U_*e^{-i\frac{\alpha}{2}\Sigma_n}$ for all $\alpha\in\mathbb R$, whence
   $$
   U_{n+1,K',c}U_{n,K,b}=U_*e^{-i\frac{\varphi_{K',c}}{2}\Sigma_{n+1}}U_*e^{-i\frac{\varphi_{K,b}}{2}\Sigma_n}
   =U_*^2e^{-i\frac{\varphi_{K',c}}{2}\Sigma_n}e^{-i\frac{\varphi_{K,b}}{2}\Sigma_n}
   =U_*^2\exp\!\left(-i\frac{\varphi_{K,b}+\varphi_{K',c}}{2}\Sigma_n\right).
   $$
   Iterating $e^{-i\frac{\alpha}{2}\Sigma_{n+m}}U_*^m=U_*^me^{-i\frac{\alpha}{2}\Sigma_n}$ proves (20) by immediate induction on $m\ge 1$.
2. Proceed by induction on $m\ge 1$. For $m=1$, $E=C+S_0$, $W_{\rm str}(h)=q(C,r,S_0)$, $\Phi_h=\varphi_{K_0,b_0}$, $U_*e^{-i\frac{\Phi_h}{2}\Sigma_n}=U_{n,K_0,b_0}$, $1-2^{-1}=\frac{1}{2}$, and $\theta 2^n(H_{\rm foc}(E)-H_{\rm foc}(C))=r_C(S_0)$; since $\frac{1}{2}(\frac{1}{2}I_Q+r_C(S_0)\Sigma_n)=\frac{1}{4}(I_Q+2r_C(S_0)\Sigma_n)$, (21) coincides identically with $(\mathcal B^{C,r}_{S_0,b_0}\otimes\operatorname{id}_{\rm ref})(X)$.

   Suppose (21) holds for an $m$-birth history $h$ ending at $(P_m,r_m)$ ($|P_m|=n+m\le 3$), and append one birth $(S_m,b_m)$ with weight $q_m:=q(P_m,r_m,S_m)$, drift $r_m:=r_{P_m}(S_m)=\theta 2^{n+m}(H_{\rm foc}(P_{m+1})-H_{\rm foc}(P_m))$, and unitary $U_m:=U_{n+m,K_m,b_m}$. Put $V_m:=U_*^m e^{-i\frac{\Phi_h}{2}\Sigma_n}$ and write $(\mathcal B_h\otimes\operatorname{id}_{\rm ref})(X)=2^{-m}W_{\rm str}(h)(Y_{\rm coh}+Y_{\rm mix})$, where $Y_{\rm coh}:=2^{-m}(V_m\otimes I_{\rm ref})X(V_m^\dagger\otimes I_{\rm ref})$ and $Y_{\rm mix}:=\frac{1}{2}I_Q\otimes R_m$ with $R_m:=\operatorname{Tr}_Q[\bigl(((1-2^{-m})I_Q+\theta 2^n(H_{\rm foc}(P_m)-H_{\rm foc}(C))\Sigma_n)\otimes I_{\rm ref}\bigr)X]$. Applying $\mathcal M(r_m,\Sigma_{n+m},U_m)\otimes\operatorname{id}_{\rm ref}$ linearly:
   - By the maximally-mixed anchor of Theorem 2, $(\mathcal M\otimes\operatorname{id}_{\rm ref})(Y_{\rm mix})=\frac{1}{2}I_Q\otimes R_m$.
   - On $Y_{\rm coh}$, the unitary term is $2^{-(m+1)}(U_mV_m\otimes I_{\rm ref})X(V_m^\dagger U_m^\dagger\otimes I_{\rm ref})$, where $U_mV_m=U_*^{m+1}e^{-i\frac{\Phi_h+\varphi_{K_m,b_m}}{2}\Sigma_n}$ by (20). The reset term is
     $$
     \frac{1}{4}I_Q\otimes\operatorname{Tr}_Q\!\Bigl[\bigl((I_Q+2r_m\Sigma_{n+m})\otimes I_{\rm ref}\bigr)2^{-m}(V_m\otimes I_{\rm ref})X(V_m^\dagger\otimes I_{\rm ref})\Bigr]
     =\frac{1}{2}I_Q\otimes\operatorname{Tr}_Q\!\Bigl[\bigl(2^{-(m+1)}V_m^\dagger(I_Q+2r_m\Sigma_{n+m})V_m\otimes I_{\rm ref}\bigr)X\Bigr].
     $$
     Since $\Sigma_{n+m}=U_*^m\Sigma_n(U_*^\dagger)^m$, $V_m^\dagger\Sigma_{n+m}V_m=e^{+i\frac{\Phi_h}{2}\Sigma_n}\Sigma_n e^{-i\frac{\Phi_h}{2}\Sigma_n}=\Sigma_n$. Furthermore, $2^{-(m+1)}(2r_m)=2^{-m}\theta 2^{n+m}(H_{\rm foc}(P_{m+1})-H_{\rm foc}(P_m))=\theta 2^n(H_{\rm foc}(P_{m+1})-H_{\rm foc}(P_m))$. Adding this to $\frac{1}{2}I_Q\otimes R_m$ telescopes $(1-2^{-m})+2^{-(m+1)}=1-2^{-(m+1)}$ and $(H_{\rm foc}(P_m)-H_{\rm foc}(C))+(H_{\rm foc}(P_{m+1})-H_{\rm foc}(P_m))=H_{\rm foc}(P_{m+1})-H_{\rm foc}(C)$, while multiplying outside by $\frac{1}{2}q_m\cdot 2^{-m}W_{\rm str}(h)=2^{-(m+1)}W_{\rm str}(h')$ completes the induction.
3. For any two ideals $S,T\subseteq C$ ($|C|=n\le 2$) and bits $b,c\in\{0,1\}$, neither newborn vertex belongs to the other's strict past ($x\notin T$, $y\notin S$). Under the canonical swap identifying $x\leftrightarrow x$, $y\leftrightarrow y$, and $v\leftrightarrow v$ ($v\in C$): (i) both two-step histories reach the same unmarked order $E$, so $H_{\rm foc}(E)-H_{\rm foc}(C)$ is identical; (ii) Part A's complete scalar diamond identity $q(C,r,S)q(C+x_S,r+b_x,T)=q(C,r,T)q(C+y_T,r+c_y,S)$ equates $W_{\rm str}$ on both paths for all old marks $r$, all $(b,c)$, equal ideals $S=T$, and full ideals $S=C$ becoming proper in $C+y_T$; and (iii) the induced marked precursors $(S,(r+c_y)|_S)=(S,r|_S)$ and $(T,(r+b_x)|_T)=(T,r|_T)$ have identical classes $K_S,K_T$ in either birth order, so $\Phi=\varphi_{K_S,b}+\varphi_{K_T,c}=\varphi_{K_T,c}+\varphi_{K_S,b}$ agrees. Substituting $m=2$ into (21) proves (22). Because the swapped marked intermediate posets are canonically isomorphic, Theorem 2's relabeling equivariance makes every subsequent transported branch map (including suffix ideals containing $x$, $y$, or both) identical, preserving exact equality across every suffix within the four-birth horizon. $\blacksquare$

### 3.2 Heisenberg operator martingale, variance-driven causal focusing, and fixed-basis reduction obstruction

For any marked parent $(C,r)$ of size $|C|=n\le 3$, let $P_{(C,r)}^{\rm pass}(h):=2^{-(4-n)}W_{\rm str}(h)$ denote Part A's passive fair-mark continuation probability law to terminal size $4$.

**Theorem 4 (Heisenberg operator martingale, covariance response law, and fixed-basis classical reduction obstruction).**
1. *(Exact nonselective Heisenberg martingale.)* *Define the stage-scaled observables $\mathcal Q_n:=2^n\Sigma_n$ ($0\le n\le 4$). At every marked parent $(P,r)$ ($|P|\le 3$) and on every individual branch $(S,b)$, $(\mathcal B^{P,r}_{S,b})^\dagger(\mathcal Q_{|P|+1})=\frac{1}{2}q(P,r,S)\mathcal Q_{|P|}$, whence*
   $$
   \sum_{S\subseteq P}\sum_{b\in\{0,1\}}\bigl(\mathcal B^{P,r}_{S,b}\bigr)^\dagger(\mathcal Q_{|P|+1})=\mathcal Q_{|P|}.
   \tag{23}
   $$
2. *(Covariance law and variance-driven causal focusing.)* *For every marked parent $(C,r)$ ($|C|=n\le 3$), initial state $\rho\in\mathcal D(\mathcal H_Q)$, and terminal unmarked observable $F:\mathcal U_4\to\mathbb R$,*
   $$
   \mathbb E_{(C,r),\rho}[F(E)]=\mathbb E_{P_{(C,r)}^{\rm pass}}[F(E)]+\theta\,2^n\operatorname{Cov}_{P_{(C,r)}^{\rm pass}}\!\bigl(F(E),H_{\rm foc}(E)\bigr)\operatorname{Tr}(\Sigma_n\rho).
   \tag{24}
   $$
   *In particular, for $F=H_{\rm foc}$,*
   $$
   \mathbb E_{(C,r),\rho}[H_{\rm foc}(E)]-H_{\rm foc}(C)=\theta\,2^n\operatorname{Var}_{P_{(C,r)}^{\rm pass}}\!\bigl(H_{\rm foc}(E)\bigr)\operatorname{Tr}(\Sigma_n\rho).
   \tag{25}
   $$
3. *(Fixed-basis classical reduction obstruction on $\mathbb C^2$.)* *No instrument family $\{\widetilde{\mathcal B}^{P,r}_{S,b}\}$ on the fixed carrier $\mathbb C^2$ whose branch effects $(\widetilde{\mathcal B}^{P,r}_{S,b})^\dagger(I_Q)$ are simultaneously diagonal in a single parent-independent orthonormal basis $\{|e_0\rangle,|e_1\rangle\}$ can reproduce the state-to-branch trace functionals $\rho\mapsto\operatorname{Tr}[\mathcal B^{P,r}_{S,b}(\rho)]$ across parent sizes $n=1,2,3$. Moreover, every state $\rho$ diagonal in $\{|e_0\rangle,|e_1\rangle\}$ obeys $\sum_{n=1}^3|\operatorname{Tr}(\Sigma_n\rho)|^2\le 1<3$, maximizing direct stage-$n$ contrast on at most one stage while giving strictly suboptimal or zero direct contrast across $(\Sigma_1,\Sigma_2,\Sigma_3)=(Z,X,Y)$. Explicitly, every $Z$-diagonal state $\rho=p|0\rangle\langle 0|+(1-p)|1\rangle\langle 1|$ attains optimal $n=1$ singleton full-slot relative multiplier contrast $\Delta^{\rm rel}_{n=1}=2r_{A_1}(\{u\})=\frac{7}{110}$ (raw full-slot probability contrast $\Delta^{\rm prob}_{n=1}=q(A_1,r,\{u\})\Delta^{\rm rel}_{n=1}=\frac{7}{330}$ between $|0\rangle\langle 0|$ and $|1\rangle\langle 1|$), yet yields identically zero direct $n=2$ structural contrast on $a\prec b$ and identically zero direct $n=3$ structural contrast on `3-chain` and `fork`.*

**Proof.**
1. Put $n=|P|$. By (18) and $\operatorname{Tr}(\Sigma_{n+1})=0$, together with $U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}=\Sigma_n$ from (19),
   $$
   \bigl(\mathcal B^{P,r}_{S,b}\bigr)^\dagger(2^{n+1}\Sigma_{n+1})=\frac{1}{2}q(P,r,S)\cdot\frac{1}{2}U_{n,K,b}^\dagger(2^{n+1}\Sigma_{n+1})U_{n,K,b}=\frac{1}{2}q(P,r,S)\,2^n\Sigma_n=\frac{1}{2}q(P,r,S)\mathcal Q_n.
   $$
   Summing over $b\in\{0,1\}$ and $S\subseteq P$ with $\sum_{S\subseteq P}q(P,r,S)=1$ gives (23).
2. Applying $\operatorname{Tr}$ to (21) at $m=4-n$ (with trivial reference and $\operatorname{Tr}\rho=1$) gives the exact active history probability
   $$
   \mathbb P_{(C,r),\rho}(h)=\operatorname{Tr}\bigl[\mathcal B_h(\rho)\bigr]=P_{(C,r)}^{\rm pass}(h)\Bigl[1+\theta\,2^n\bigl(H_{\rm foc}(E_h)-H_{\rm foc}(C)\bigr)\operatorname{Tr}(\Sigma_n\rho)\Bigr],
   \tag{26}
   $$
   since $2^{-m}+(1-2^{-m})=1$. By Theorem 1, $\mathbb E_{P_{(C,r)}^{\rm pass}}[H_{\rm foc}(E)]=H_{\rm foc}(C)$, so $\mathbb E_{P_{(C,r)}^{\rm pass}}[F(E)(H_{\rm foc}(E)-H_{\rm foc}(C))]=\operatorname{Cov}_{P_{(C,r)}^{\rm pass}}(F(E),H_{\rm foc}(E))$. Multiplying (26) by $F(E_h)$ and summing over $h$ proves (24), and setting $F=H_{\rm foc}$ proves (25).
3. Any Hermitian operator diagonal in $\{|e_0\rangle,|e_1\rangle\}$ lies in $\operatorname{span}_{\mathbb R}\{I_Q,\Sigma_{\mathbf u}\}$, where $\Sigma_{\mathbf u}:=|e_0\rangle\langle e_0|-|e_1\rangle\langle e_1|=u_xX+u_yY+u_zZ$ ($u_x^2+u_y^2+u_z^2=1$) is a single unit Bloch observable. By (14), our branch effects are $(\mathcal B^{P,r}_{S,b})^\dagger(I_Q)=\frac{1}{2}q(P,r,S)(I_Q+r_P(S)\Sigma_{|P|})$, whose traceless parts at $(A_1,\{u\})$ ($n=1$, coefficient $\frac{7}{1320}Z$), $(C_2,\varnothing)$ ($n=2$, coefficient $-\frac{21}{2200}X$), and $(C_3,C_3)$ ($n=3$, coefficient $\frac{41}{7744}Y$) are nonzero multiples of $Z$, $X$, and $Y$ respectively. Since $\{I_Q,X,Y,Z\}$ spans $M_2(\mathbb C)$ linearly independently and $\mathcal D(\mathbb C^2)$ spans the Hermitian subspace, no single $\operatorname{span}_{\mathbb R}\{I_Q,\Sigma_{\mathbf u}\}$ can contain all three branch effects. Furthermore, any state diagonal in $\{|e_0\rangle,|e_1\rangle\}$ has the form $\rho=\frac{1}{2}(I_Q+s\Sigma_{\mathbf u})$ ($s\in[-1,1]$), so $(\operatorname{Tr}(Z\rho),\operatorname{Tr}(X\rho),\operatorname{Tr}(Y\rho))=s(u_z,u_x,u_y)$ satisfies $\sum_{n=1}^3|\operatorname{Tr}(\Sigma_n\rho)|^2=s^2(u_z^2+u_x^2+u_y^2)=s^2\le 1<3$. For $Z$-diagonal $\rho=p|0\rangle\langle 0|+(1-p)|1\rangle\langle 1|$, $\operatorname{Tr}(Z\rho)=2p-1$ gives $p_{A_1,\text{full}}(\rho)=\frac{1}{3}(1+\frac{7}{220}(2p-1))$—attaining relative multiplier contrast $2r_{A_1}(\{u\})=\frac{7}{110}$ and raw probability contrast $\frac{1}{3}\cdot\frac{7}{110}=\frac{7}{330}$ between $p=1$ and $p=0$—whereas $\operatorname{Tr}(X\rho)=\operatorname{Tr}(Y\rho)=0$ forces every $n=2$ continuation probability on $a\prec b$ and every $n=3$ step probability on `3-chain` and `fork` to collapse identically to the passive baseline. $\blacksquare$

---

## 4. Bidirectional feedback ledger above $a\prec b$, synergistic action shift, and imperfect-readout bounds

### 4.1 Complete 15-row / 60-marked-history active two-way ledger

Condition on the prepared causal prefix $C=(a\prec b)$ ($|C|=n=2$, $m=2$ remaining births $x$ then $y$ with fair bits $(b_3,b_4)\in\{0,1\}^2$), carrying immutable marks $(r_a,r_b)=(i,0)$ ($i\in\{0,1\}$), consistent ancestor counters $(1,0)$ as in [prepared source and readout response](native_source_readout_response.md), and initial qubit state $\rho\in\mathcal D(\mathbb C^2)$. Here $\Sigma_2=X$, $\theta\,2^2=\frac{1}{8}$, and $H_{\rm foc}(C_2)=\frac{42}{55}$, so by (26) every marked history $h$ ending at unmarked order $E$ acquires the active structural multiplier
$$
M_\rho(E):=1+\frac{1}{8}\left(H_{\rm foc}(E)-\frac{42}{55}\right)\langle X\rangle_\rho
=
\begin{cases}
1+\dfrac{13}{440}\langle X\rangle_\rho, & H_{\rm foc}(E)=1,\\[8pt]
1-\dfrac{21}{220}\langle X\rangle_\rho, & H_{\rm foc}(E)=0,
\end{cases}
\tag{27}
$$
where $\langle X\rangle_\rho:=\operatorname{Tr}(X\rho)$. At $\rho=|+\rangle\langle+|$ ($\langle X\rangle=+1$), $M_{|+\rangle}(1)=\frac{453}{440}$ and $M_{|+\rangle}(0)=\frac{398}{440}=\frac{199}{220}$; at $\rho=|-\rangle\langle-|$ ($\langle X\rangle=-1$), $M_{|-\rangle}(1)=\frac{427}{440}$ and $M_{|-\rangle}(0)=\frac{482}{440}=\frac{241}{220}$. Multiplying the passive structural denominators ($1320$) by $440$ puts all active row probabilities over the exact common integer denominator $1320\times 440=580{,}800$.

Recall from [finite interval action and source preparation](finite_interval_action_and_source_preparation.md) the dimensionless Benincasa–Dowker interval action $S_{\rm BD}(E):=4-2n_0+4n_1-2n_2$ (where $n_k$ counts comparable pairs $u\prec v$ with open-interval cardinality $k\in\{0,1,2\}$), and from [prepared source and readout response](native_source_readout_response.md) the total-chain indicator $D(E)\in\{0,1\}$ and vertex-counter-equals-$2$ indicator $Y(E)\in\{0,1\}$. Under the chiral precursor-phase rule (10) ($\varphi_{K_0,0}=\varphi_0$, zero otherwise), a step triggers $\varphi_0$ precisely when its precursor ideal is a singleton marked $0$ and its newborn bit is $0$:
- At $I_x\subseteq\{a,b\}$, only $I_x=\{a\}$ is a singleton; since $r_a=i$, it triggers $\varphi_0\mathbf 1_{\{i=0,\,b_3=0\}}$.
- At $I_y\subseteq\{a,b,x\}$, $\{b\}$ is never downward-closed ($a\prec b$); $\{a\}$ is a singleton in Rows 3, 8, 13, triggering $\varphi_0\mathbf 1_{\{i=0,\,b_4=0\}}$; and $\{x\}$ is downward-closed solely when $I_x=\varnothing$ (Row 2), where $x$ carries mark $r_x=b_3$, triggering $\varphi_0\mathbf 1_{\{b_3=0,\,b_4=0\}}$ on $(b_3,b_4)=(0,0)$ under *both* $i=0$ and $i=1$.

The complete 15-row structural ledger—retaining all $4$ fair bit pairs $(b_3,b_4)\in\{0,1\}^2$ per row (each carrying exactly $\frac{1}{4}$ of its row's structural probability), hence all $60$ naturally encoded marked histories per preparation—is (writing $\mathbb P_{i,\pm}:=\mathbb P_{i,\lvert\pm\rangle}$):

| Row | $(I_x,I_y)$ | Unmarked $E$ | $H_{\rm foc}$ | $1320P_0^{\rm pass}$ | $1320P_1^{\rm pass}$ | $580{,}800\,\mathbb P_{0,\pm}$ ($+$ / $-$) | $580{,}800\,\mathbb P_{1,\pm}$ ($+$ / $-$) | $S_{\rm BD}$ | $(D,Y)$ | $\Phi_h$ counts $(0,\varphi_0,2\varphi_0)$ ($i=0$ ; $i=1$) |
| ---: | --- | --- | :---: | ---: | ---: | :---: | :---: | ---: | :---: | :---: |
| 1 | $(\varnothing,\varnothing)$ | $E_{\text{edge+2iso}}$ | $0$ | $6$ | $6$ | $2{,}388$ / $2{,}892$ | $2{,}388$ / $2{,}892$ | $2$ | $(0,0)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 2 | $(\varnothing,\{x\})$ | $E_{\text{2-edges}}$ | $0$ | $6$ | $6$ | $2{,}388$ / $2{,}892$ | $2{,}388$ / $2{,}892$ | $0$ | $(0,0)$ | $(3,1,0)$ ; $(3,1,0)$ |
| 3 | $(\varnothing,\{a\})$ | $E_{\text{fork+iso}}$ | $0$ | $5$ | $10$ | $1{,}990$ / $2{,}410$ | $3{,}980$ / $4{,}820$ | $0$ | $(0,1)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 4 | $(\varnothing,\{a,b\})$ | $E_{\text{3chain+iso}}$ | $0$ | $19$ | $14$ | $7{,}562$ / $9{,}158$ | $5{,}572$ / $6{,}748$ | $4$ | $(0,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 5 | $(\varnothing,\{a,x\})$ | $E_{\text{N-poset}}$ | $0$ | $33$ | $33$ | $13{,}134$ / $15{,}906$ | $13{,}134$ / $15{,}906$ | $-2$ | $(0,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 6 | $(\varnothing,\{a,b,x\})$ | $E_{\text{asym-join}}$ | $0$ | $195$ | $195$ | $77{,}610$ / $93{,}990$ | $77{,}610$ / $93{,}990$ | $2$ | $(0,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 7 | $(\{a\},\varnothing)$ | $E_{\text{fork+iso}}$ | $0$ | $5$ | $10$ | $1{,}990$ / $2{,}410$ | $3{,}980$ / $4{,}820$ | $0$ | $(0,1)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 8 | $(\{a\},\{a\})$ | $E_{\text{3-claw}}$ | $0$ | $5$ | $10$ | $1{,}990$ / $2{,}410$ | $3{,}980$ / $4{,}820$ | $-2$ | $(0,0)$ | $(1,2,1)$ ; $(4,0,0)$ |
| 9 | $(\{a\},\{a,b\})$ | $E_{\text{asym-fork}}$ | $1$ | $19$ | $14$ | $8{,}607$ / $8{,}113$ | $6{,}342$ / $5{,}978$ | $2$ | $(0,0)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 10 | $(\{a\},\{a,x\})$ | $E_{\text{asym-fork}}$ | $1$ | $19$ | $14$ | $8{,}607$ / $8{,}113$ | $6{,}342$ / $5{,}978$ | $2$ | $(0,0)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 11 | $(\{a\},\{a,b,x\})$ | $E_{\text{diamond}}$ | $1$ | $172$ | $392$ | $77{,}916$ / $73{,}444$ | $177{,}576$ / $167{,}384$ | $-6$ | $(0,0)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 12 | $(\{a,b\},\varnothing)$ | $E_{\text{3chain+iso}}$ | $0$ | $19$ | $14$ | $7{,}562$ / $9{,}158$ | $5{,}572$ / $6{,}748$ | $4$ | $(0,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 13 | $(\{a,b\},\{a\})$ | $E_{\text{asym-fork}}$ | $1$ | $19$ | $14$ | $8{,}607$ / $8{,}113$ | $6{,}342$ / $5{,}978$ | $2$ | $(0,0)$ | $(2,2,0)$ ; $(4,0,0)$ |
| 14 | $(\{a,b\},\{a,b\})$ | $E_{\text{upper-fork}}$ | $0$ | $19$ | $14$ | $7{,}562$ / $9{,}158$ | $5{,}572$ / $6{,}748$ | $6$ | $(0,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| 15 | $(\{a,b\},\{a,b,x\})$ | $E_{\text{4-chain}}$ | $1$ | $779$ | $574$ | $352{,}887$ / $332{,}633$ | $260{,}022$ / $245{,}098$ | $4$ | $(1,1)$ | $(4,0,0)$ ; $(4,0,0)$ |
| **Total** | | | | **$1{,}320$** | **$1{,}320$** | **$580{,}800$ / $580{,}800$** | **$580{,}800$ / $580{,}800$** | | | **$60$ ; $60$** |

*Column conservation checks:* Under both $i=0$ and $i=1$, the five $H_{\rm foc}=1$ rows (Rows 9, 10, 11, 13, 15) have passive numerator sum $19+19+172+19+779=1008=14+14+392+14+574$ ($\frac{1008}{1320}=\frac{42}{55}$), and the ten $H_{\rm foc}=0$ rows sum to $312$ ($\frac{312}{1320}=\frac{13}{55}$). Thus $1008\times 453+312\times 398=456{,}624+124{,}176=580{,}800$ for $|+\rangle$ and $1008\times 427+312\times 482=430{,}416+150{,}384=580{,}800$ for $|-\rangle$. Note also how incomparable-birth diamond pairs—Rows 3 & 7, Rows 4 & 12, self-paired equal-precursor Rows 1, 8, 14, and full-to-proper Rows 9 & 13—carry identical active numerators and identical $\Phi_h$ trigger distributions.

### 4.2 Exact rational bidirectional contrasts and single-state witness

#### A. Forward (`Quantum -> Order`) contrasts on $|+\rangle$ vs $|-\rangle$

Comparing $\rho=|+\rangle\langle+|$ against $\rho=|-\rangle\langle-|$ ($\Delta\langle X\rangle=+2$, so $\theta\,2^2\Delta\langle X\rangle=\frac{1}{4}$ in (24)):

1. **Causal-focusing shift ($H_{\rm foc}=1$):** Under both $i=0$ and $i=1$, $\operatorname{Var}_{P_i^{\rm pass}}(H_{\rm foc})=\frac{42}{55}\cdot\frac{13}{55}=\frac{546}{3025}$, giving
   $$
   \mathbb P_{i,|+\rangle}(H_{\rm foc}=1)-\mathbb P_{i,|-\rangle}(H_{\rm foc}=1)
   =\frac{456{,}624-430{,}416}{580{,}800}
   =\frac{26{,}208}{580{,}800}
   =\frac{1}{4}\cdot\frac{546}{3025}
   =+\frac{273}{6050}>0.
   \tag{28}
   $$
2. **Total-chain shift ($D=1$, Row 15):** Since $D(E)=\mathbf 1_{\{\text{Row }15\}}$ lies inside $H_{\rm foc}=1$, $\operatorname{Cov}_{P_i^{\rm pass}}(D,H_{\rm foc})=P_i^{\rm pass}(\text{Row }15)\cdot\frac{13}{55}$, giving
   $$
   \mathbb P_{0,|+\rangle}(D=1)-\mathbb P_{0,|-\rangle}(D=1)=\frac{352{,}887-332{,}633}{580{,}800}=\frac{20{,}254}{580{,}800}=+\frac{10{,}127}{290{,}400}>0,
   \tag{29a}
   $$
   $$
   \mathbb P_{1,|+\rangle}(D=1)-\mathbb P_{1,|-\rangle}(D=1)=\frac{260{,}022-245{,}098}{580{,}800}=\frac{14{,}924}{580{,}800}=+\frac{3{,}731}{145{,}200}>0.
   \tag{29b}
   $$
3. **Operational incidence-counter shift ($Y=1$):** In the ledger, $Y=1$ holds on Rows 3, 4, 5, 6, 7, 12, 14 ($H_{\rm foc}=0$, passive sum $295$ for $i=0$ and $290$ for $i=1$) together with Row 15 ($H_{\rm foc}=1$, passive weight $779$ for $i=0$ and $574$ for $i=1$). Using multiplier differences $453-427=+26$ ($H_{\rm foc}=1$) and $398-482=-84$ ($H_{\rm foc}=0$),
   $$
   \mathbb P_{0,|+\rangle}(Y=1)-\mathbb P_{0,|-\rangle}(Y=1)=\frac{779\times 26-295\times 84}{580{,}800}=\frac{20{,}254-24{,}780}{580{,}800}=-\frac{4{,}526}{580{,}800}=-\frac{2{,}263}{290{,}400}<0,
   \tag{30a}
   $$
   $$
   \mathbb P_{1,|+\rangle}(Y=1)-\mathbb P_{1,|-\rangle}(Y=1)=\frac{574\times 26-290\times 84}{580{,}800}=\frac{14{,}924-24{,}360}{580{,}800}=-\frac{9{,}436}{580{,}800}=-\frac{2{,}359}{145{,}200}<0,
   \tag{30b}
   $$
   matching $\frac{1}{4}\operatorname{Cov}_{P_i^{\rm pass}}(Y,H_{\rm foc})$ ($779\times 55-1074\times 42=-2263$ and $574\times 55-864\times 42=-4718$ over $290{,}400$).
4. **Synergistic / non-additive Benincasa–Dowker interval-action shift:** Recall from [finite interval action and source preparation](finite_interval_action_and_source_preparation.md) that $1320\,\mathbb E_0^{\rm pass}[S_{\rm BD}]=2790$ ($\mathbb E_0^{\rm pass}[S_{\rm BD}]=\frac{93}{44}$) and $1320\,\mathbb E_1^{\rm pass}[S_{\rm BD}]=540$ ($\mathbb E_1^{\rm pass}[S_{\rm BD}]=\frac{9}{22}$). Restricting to the five $H_{\rm foc}=1$ rows gives
   $$
   1320\,\mathbb E_0^{\rm pass}[S_{\rm BD}H_{\rm foc}]=3(19)(2)+172(-6)+779(4)=114-1032+3116=2198,
   $$
   $$
   1320\,\mathbb E_1^{\rm pass}[S_{\rm BD}H_{\rm foc}]=3(14)(2)+392(-6)+574(4)=84-2352+2296=28,
   $$
   while the $H_{\rm foc}=0$ sums are $2790-2198=592$ ($i=0$) and $540-28=512$ ($i=1$). Therefore:
   $$
   \mathbb E_{0,|+\rangle}[S_{\rm BD}]-\mathbb E_{0,|-\rangle}[S_{\rm BD}]=\frac{2198\times 26-592\times 84}{580{,}800}=\frac{57{,}148-49{,}728}{580{,}800}=+\frac{7{,}420}{580{,}800}=+\frac{371}{29{,}040}>0,
   \tag{31a}
   $$
   $$
   \mathbb E_{1,|+\rangle}[S_{\rm BD}]-\mathbb E_{1,|-\rangle}[S_{\rm BD}]=\frac{28\times 26-512\times 84}{580{,}800}=\frac{728-43{,}008}{580{,}800}=-\frac{42{,}280}{580{,}800}=-\frac{1{,}057}{14{,}520}<0.
   \tag{31b}
   $$
   Switching initial coherence from $|-\rangle$ to $|+\rangle$ *increases* mean interval action when $i=0$ (where causal focusing predominantly amplifies `4-chain` with $S_{\rm BD}=+4$) and *decreases* mean interval action when $i=1$ (where causal focusing strongly amplifies `diamond` with $S_{\rm BD}=-6$). The exact mark–coherence interaction contrast is nonzero:
   $$
   \Delta_{\rm int}(S_{\rm BD}):=\Bigl(\mathbb E_{1,|+\rangle}[S_{\rm BD}]-\mathbb E_{1,|-\rangle}[S_{\rm BD}]\Bigr)-\Bigl(\mathbb E_{0,|+\rangle}[S_{\rm BD}]-\mathbb E_{0,|-\rangle}[S_{\rm BD}]\Bigr)
   =-\frac{1{,}057}{14{,}520}-\frac{371}{29{,}040}=-\frac{2{,}485}{29{,}040}=-\frac{497}{5{,}808}\ne 0.
   \tag{32}
   $$

#### B. Backward (`Order/Mark -> Quantum`) response and single-state Pythagorean witness

Summing (21) ($n=2$, $m=2$, $\Sigma_2=X$) over all $60$ marked continuations $h$ from $(C_2,(i,0))$ cancels $\sum_h P_i^{\rm pass}(h)(H_{\rm foc}(E_h)-\frac{42}{55})=0$ in the reset block, yielding the exact unselected two-birth quantum channel
$$
\mathcal E_i(\rho):=\sum_h\mathcal B_h(\rho)=\frac{3}{4}\operatorname{Tr}(\rho)\frac{I_Q}{2}+\frac{1}{4}U_*^2\left(\sum_{k=0}^2\nu_i(k)\,e^{-i\frac{k\varphi_0}{2}X}\rho\,e^{+i\frac{k\varphi_0}{2}X}\right)(U_*^\dagger)^2,
\tag{33}
$$
where $\nu_i(k):=\sum_{h:\Phi_h=k\varphi_0}P_i^{\rm pass}(h)$. Summing the last column of the 15-row ledger over $4\times 1320=5280$ gives:
- Under $i=0$: $5280\,\nu_0(2)=5\times 1=5$; $5280\,\nu_0(1)=6(1)+2(5+5+5+19+19+172+19)=6+488=494$; and $5280\,\nu_0(0)=5280-499=4781$, so $(\nu_0(0),\nu_0(1),\nu_0(2))=(\frac{4781}{5280},\frac{247}{2640},\frac{1}{1056})$.
- Under $i=1$: only Row 2's $(b_3,b_4)=(0,0)$ history triggers $k=1$, so $5280\,\nu_1(1)=6$, $5280\,\nu_1(2)=0$, $5280\,\nu_1(0)=5274$, i.e., $(\nu_1(0),\nu_1(1),\nu_1(2))=(\frac{879}{880},\frac{1}{880},0)$.

Because $U_*^2=-U_*^\dagger$ (Lemma 1), $(U_*^\dagger)^2XU_*^2=U_*XU_*^\dagger=Y$, and $e^{+i\frac{\alpha}{2}X}Ye^{-i\frac{\alpha}{2}X}=(\cos\alpha\,I_Q+i\sin\alpha\,X)Y=\cos\alpha\,Y-\sin\alpha\,Z$. Hence for any initial state $\rho\in\mathcal D(\mathbb C^2)$,
$$
\langle X\rangle_{\rm final}(i;\rho):=\operatorname{Tr}\bigl[X\,\mathcal E_i(\rho)\bigr]
=\frac{1}{4}\sum_{k=0}^2\nu_i(k)\bigl[\cos(k\varphi_0)\,\langle Y\rangle_\rho-\sin(k\varphi_0)\,\langle Z\rangle_\rho\bigr].
\tag{34}
$$
Fix the chiral precursor angle $\varphi_0:=\frac{\pi}{2}$, where $(\cos(k\varphi_0),\sin(k\varphi_0))$ equals $(1,0)$, $(0,1)$, $(-1,0)$ at $k=0,1,2$, simplifying (34) to
$$
\langle X\rangle_{\rm final}(i;\rho)=\frac{1}{4}\Bigl[\bigl(\nu_i(0)-\nu_i(2)\bigr)\langle Y\rangle_\rho-\nu_i(1)\,\langle Z\rangle_\rho\Bigr].
\tag{35}
$$
Now prepare the tilted pure Pythagorean qubit state and its $Z$-flipped partner:
$$
|\psi_{3,4}\rangle:=\frac{2}{\sqrt 5}|+\rangle+\frac{1}{\sqrt 5}|-\rangle=\frac{3}{\sqrt{10}}|0\rangle+\frac{1}{\sqrt{10}}|1\rangle,
\qquad
|\psi_{-3,4}\rangle:=Z|\psi_{3,4}\rangle=\frac{1}{\sqrt 5}|+\rangle+\frac{2}{\sqrt 5}|-\rangle=\frac{3}{\sqrt{10}}|0\rangle-\frac{1}{\sqrt{10}}|1\rangle.
\tag{36}
$$
Directly, $|\psi_{3,4}\rangle$ has Bloch expectations $(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)=(\frac{3}{5},0,\frac{4}{5})$, whereas $|\psi_{-3,4}\rangle$ has $(\langle X\rangle,\langle Y\rangle,\langle Z\rangle)=(-\frac{3}{5},0,+\frac{4}{5})$. Substituting $\langle Y\rangle=0$ and $\langle Z\rangle=\frac{4}{5}$ into (35) yields $\langle X\rangle_{\rm final}(i)=-\frac{1}{5}\nu_i(1)$ on *both* states:
$$
\langle X\rangle_{\rm final}\bigl(0;\,|\psi_{\pm 3,4}\rangle\bigr)=-\frac{1}{5}\cdot\frac{247}{2640}=-\frac{247}{13{,}200},
\qquad
\langle X\rangle_{\rm final}\bigl(1;\,|\psi_{\pm 3,4}\rangle\bigr)=-\frac{1}{5}\cdot\frac{1}{880}=-\frac{1}{4{,}400}=-\frac{3}{13{,}200},
\tag{37}
$$
with exact nonzero `Order/Mark -> Quantum` coherence shift
$$
\langle X\rangle_{\rm final}\bigl(0;\,|\psi_{\pm 3,4}\rangle\bigr)-\langle X\rangle_{\rm final}\bigl(1;\,|\psi_{\pm 3,4}\rangle\bigr)
=-\frac{247}{13{,}200}-\left(-\frac{3}{13{,}200}\right)=-\frac{244}{13{,}200}=-\frac{61}{3{,}300}\ne 0.
\tag{38}
$$
*(Arithmetic check: each of the four bit pairs in Row 2 has passive probability $\frac{1}{4}\cdot\frac{6}{1320}=\frac{1}{880}$, so multiplying $\nu_1(1)=\frac{1}{880}$ by $-\frac{1}{4}\langle Z\rangle=-\frac{1}{5}$ gives $-\frac{1}{4400}=-\frac{3}{13200}$, whose difference from $-\frac{247}{13200}$ is $-\frac{244}{13200}=-\frac{61}{3300}$.)* Simultaneously, comparing $|\psi_{3,4}\rangle$ against $|\psi_{-3,4}\rangle$ ($\Delta\langle X\rangle=+\frac{6}{5}=\frac{3}{5}\cdot 2$) scales every `Quantum -> Order` contrast in (28)–(32) by $\frac{3}{5}$—giving $+\frac{819}{30{,}250}$ on $H_{\rm foc}$, $(+\frac{10{,}127}{484{,}000},+\frac{3{,}731}{242{,}000})$ on $D$, $(-\frac{2{,}263}{484{,}000},-\frac{2{,}359}{242{,}000})$ on $Y$, and $(+\frac{371}{48{,}400},-\frac{1{,}057}{24{,}200})$ with interaction $-\frac{497}{9{,}680}$ on $S_{\rm BD}$—while keeping $\langle X\rangle_{\rm final}(i)$ completely invariant.

### 4.3 Shared imperfect detector lower bounds and empty-start complete-trial check

Follow the observation-channel contract of [complete-trial source response](native_complete_trial_readout.md): pass any binary native event $B\in\{0,1\}$ through a shared three-outcome erasure-and-confusion channel $\xi=(f,n,e_{\rm det})\in\mathcal C:=[f_-,f_+]\times[n_-,n_+]\times[e_-,e_+]\subseteq[0,1]^3$ ($e_+<1$, $f_++n_+<1$, writing $e_{\rm det}$ for erasure probability to distinguish it from $e=\frac{1}{44}$), reporting outcome $(0,1,\perp)$ with probabilities $\bigl((1-e_{\rm det})(1-f),\,(1-e_{\rm det})f,\,e_{\rm det}\bigr)$ when $B=0$ and $\bigl((1-e_{\rm det})n,\,(1-e_{\rm det})(1-n),\,e_{\rm det}\bigr)$ when $B=1$.

**Proposition 1 (Uniform $L^1$ lower bound across the detector uncertainty box).** *Let two preparations $+$ and $-$ induce binary event probabilities $p_\pm=\mathbb P_\pm(B=1)$ with native contrast $\Delta:=p_+-p_-$, and let $\mu_\pm(\xi)$ denote the resulting reported laws on $\{0,1,\perp\}$. Then*
$$
\inf_{\xi\in\mathcal C}\bigl\|\mu_+(\xi)-\mu_-(\xi)\bigr\|_1=2|\Delta|(1-e_+)(1-f_+-n_+)>0\qquad\text{whenever }\Delta\ne 0.
\tag{39}
$$

**Proof.** Put $k:=1-f-n>0$ and $z_\pm:=f(1-p_\pm)+(1-n)p_\pm=f+kp_\pm\in[0,1]$, so $\mu_\pm(\xi)=\bigl((1-e_{\rm det})(1-z_\pm),\,(1-e_{\rm det})z_\pm,\,e_{\rm det}\bigr)$. Since $z_+-z_-=k\Delta$, $\mu_+(\xi)-\mu_-(\xi)=\bigl(-(1-e_{\rm det})k\Delta,\,+(1-e_{\rm det})k\Delta,\,0\bigr)$, giving $\|\mu_+(\xi)-\mu_-(\xi)\|_1=2|\Delta|(1-e_{\rm det})(1-f-n)$. Both positive factors $1-e_{\rm det}$ and $1-f-n$ decrease monotonically to their attained minimum at the corner $\xi_*=(f_+,n_+,e_+)\in\mathcal C$, establishing (39). $\blacksquare$

Applying Proposition 1 yields strictly positive uniform $L^1$ guarantees across $\mathcal C$ for:
- **Prepared $a\prec b$ operational counter event $B=Y$ on $|+\rangle$ vs $|-\rangle$:** $\Gamma_{0,Y}=\frac{2{,}263}{145{,}200}(1-e_+)(1-f_+-n_+)>0$ ($i=0$) and $\Gamma_{1,Y}=\frac{2{,}359}{72{,}600}(1-e_+)(1-f_+-n_+)>0$ ($i=1$).
- **Prepared $a\prec b$ causal-focusing event $B=H_{\rm foc}$ on $|+\rangle$ vs $|-\rangle$:** $\Gamma_{i,H_{\rm foc}}=\frac{273}{3{,}025}(1-e_+)(1-f_+-n_+)>0$ ($i\in\{0,1\}$).
- **Complete four-birth empty-start trial ($C=\varnothing$, $n=0$, $\Sigma_0=Y$) on $|\pm_Y\rangle:=\frac{1}{\sqrt2}(|0\rangle\pm i|1\rangle)$:** Because $H_{\rm foc}$ is harmonic at every birth (Theorem 1) and $H_{\rm foc}(E)\in\{0,1\}$ is an indicator at size $4$, $\mathbb E_{P_\varnothing^{\rm pass}}[H_{\rm foc}(E)]=H_{\rm foc}(\varnothing)=\frac{14}{55}$ (verified independently forward: $1\cdot\frac{1}{3}\cdot\frac{4}{5}\cdot\frac{21}{22}=\frac{14}{55}$), so its empty-start passive variance is immediately
  $$
  \operatorname{Var}_{P_\varnothing^{\rm pass}}(H_{\rm foc})=\frac{14}{55}\left(1-\frac{14}{55}\right)=\frac{574}{3025}.
  \tag{40}
  $$
  By (25) at $n=0$ ($\theta=\frac{1}{32}$), $\mathbb P_{\varnothing,\rho}(H_{\rm foc}=1)=\frac{14}{55}+\frac{287}{48{,}400}\operatorname{Tr}(Y\rho)$ ($\frac{12{,}607}{48{,}400}$ on $|+_Y\rangle$ vs $\frac{12{,}033}{48{,}400}$ on $|-_Y\rangle$), giving pure-state contrast $\Delta_\varnothing(H_{\rm foc})=\frac{287}{24{,}200}>0$ and detector bound $\Gamma_{\varnothing,H_{\rm foc}}=\frac{287}{12{,}100}(1-e_+)(1-f_+-n_+)>0$. (For uncertain Bloch-expectation intervals $\operatorname{Tr}(\Sigma_n\rho_\pm)\in[l_\pm,u_\pm]\subseteq[-1,1]$ with gap $g=\max(0,l_+-u_-,l_--u_+)$, linearity scales (39) by $\frac{g}{2}$, matching the mixed-source criterion of [complete-trial source response](native_complete_trial_readout.md).)

---

## 5. Controls, algebraic gauge analysis, strict separation of ingredients, and scope limits

### 5.1 Explicit null controls

Retaining the same four-birth domain, all ideal/bit branches, and complete denominators:

1. **Passive-order control ($\theta=0$):** Setting $\theta=0$ gives $r_P(S)\equiv 0$, so every branch trace equals $\frac{1}{2}q(P,r,S)\operatorname{Tr}(\rho)$ independently of $\rho$. Every `Quantum -> Order` contrast in (28)–(32) and (40) vanishes identically, while the `Order/Mark -> Quantum` contrast (38) remains $-\frac{61}{3300}\ne 0$.
2. **Phase-free active control ($\varphi_{K,b}\equiv 0$):** Setting $\varphi_0=0$ makes (34) equal $\frac{1}{4}\langle Y\rangle_\rho$ for both $i=0$ and $i=1$ ($\sum_{k=0}^2\nu_i(k)=1$), so the `Order/Mark -> Quantum` shift $\langle X\rangle_{\rm final}(0;\rho)-\langle X\rangle_{\rm final}(1;\rho)$ vanishes identically for every $\rho\in\mathcal D(\mathbb C^2)$, while all `Quantum -> Order` contrasts (28)–(32) and (40) remain unchanged.
3. **Maximally mixed and equal-state controls ($\rho=I_Q/2$ or $\rho_+=\rho_-$):** For $\rho=I_Q/2$, $\operatorname{Tr}(\Sigma_n\rho)=0$ and $\mathcal B^{P,r}_{S,b}(I_Q/2)=\frac{1}{2}q(P,r,S)(I_Q/2)$ at every step, recovering Part A's exact passive 60-history distribution $P_i^{\rm pass}$ and terminal state $I_Q/2$ ($\langle X\rangle_{\rm final}=0$). Likewise, any shared preparation $\rho_+=\rho_-$ gives zero setting contrast across $\mathcal C$.
4. **Degenerate detector boundaries ($f+n=1$ or $e_{\rm det}=1$):** At $f+n=1$ ($k=0$) or $e_{\rm det}=1$, the detector columns coincide and $\mu_+(\xi)=\mu_-(\xi)$ for all inputs, confirming necessity of the informative-box conditions $e_+<1$ and $f_++n_+<1$ in (39).

### 5.2 Prefix-dependent algebraic similarity / gauge analysis

Extending Section 6 of [active classical residual law](../track_b/native_active_residual_v1.md) to the non-abelian operator setting, set $\alpha_P:=\theta\,2^{|P|}\bigl(H_{\rm foc}(P)-H_{\rm foc}(\varnothing)\bigr)$ ($0\le|P|\le 4$) and define the invertible linear superoperator $\mathcal S_P:M_2(\mathbb C)\to M_2(\mathbb C)$ by
$$
\mathcal S_P(Y):=Y+\frac{1}{2}\alpha_P\operatorname{Tr}(\Sigma_{|P|}Y)\,I_Q,
\qquad
\mathcal S_P^{-1}(A)=A-\frac{1}{2}\alpha_P\operatorname{Tr}(\Sigma_{|P|}A)\,I_Q
\tag{41}
$$
(verified via $\operatorname{Tr}(\Sigma_{|P|}I_Q)=0$). Let $\mathcal B^{P,r;\text{pass-tr}}_{S,b}(Y):=\frac{1}{2}q(P,r,S)\mathcal M(0,\Sigma_{|P|},U_{|P|,K(S,r|_S),b})(Y)$ denote the trace-preserving $\theta=0$ control. For any $A\in M_2(\mathbb C)$ and $n=|P|\le 3$, applying $\mathcal M_0:=\mathcal M(0,\Sigma_n,U_{n,K,b})$ to $\mathcal S_P^{-1}(A)$ uses $\mathcal M_0(I_Q)=I_Q$ to give $Z':=\mathcal M_0(A)-\frac{1}{2}\alpha_P\operatorname{Tr}(\Sigma_nA)I_Q$; then (19) gives $\operatorname{Tr}(\Sigma_{n+1}Z')=\frac{1}{2}\operatorname{Tr}(U_{n,K,b}^\dagger\Sigma_{n+1}U_{n,K,b}A)=\frac{1}{2}\operatorname{Tr}(\Sigma_nA)$, whence
$$
\bigl(\mathcal S_{P+S}\circ\mathcal B^{P,r;\text{pass-tr}}_{S,b}\circ\mathcal S_P^{-1}\bigr)(A)
=\frac{1}{2}q(P,r,S)\left\{\mathcal M_0(A)+\frac{1}{2}\Bigl(\frac{1}{2}\alpha_{P+S}-\alpha_P\Bigr)\operatorname{Tr}(\Sigma_nA)\,I_Q\right\}
=\mathcal B^{P,r}_{S,b}(A),
\tag{42}
$$
because $\frac{1}{2}\alpha_{P+S}-\alpha_P=\theta\,2^n(H_{\rm foc}(P+S)-H_{\rm foc}(P))=r_P(S)$.

Crucially, for every poset $P$ with $\alpha_P\ne 0$ (such as $P=C_2$, where $\alpha_{C_2}=\frac{7}{110}>0$ and $\Sigma_2=X$), $\mathcal S_P$ is: (i) *prefix-dependent*, rather than a fixed unitary or basis transformation on $\mathcal H_Q$; (ii) *non-trace-preserving*, since $\mathcal S_P^\dagger(I_Q)=I_Q+\alpha_P\Sigma_{|P|}\ne I_Q$; and (iii) *not positive-cone-preserving*, since for $|+\rangle\langle+|$ at $P=C_2$, $\langle-|\mathcal S_{C_2}^{-1}(|+\rangle\langle+|)|-\rangle=-\frac{7}{220}<0$. Holding the physical-interface state space $\mathcal D(\mathbb C^2)$ and unit trace effect $I_Q$ fixed across prefixes makes our CPTP operational contrasts well-defined, while (42) shows transparently that this finite four-birth model neither establishes representation-independent physical backreaction nor excludes Stinespring or larger-environment passive dilations.

### 5.3 Strict separation of native vs. externally supplied ingredients

- **Inherited from the admitted four-birth native structural prefix ([Part A](../track_b/native_mark_law_geometry_v1.md#a-original-model-and-the-fixed-four-birth-structural-prefix)):** Finite strict partial orders through four births, downward-closed precursor ideals $S\subseteq P$, append-only maximal births $P+S$, immutable binary marks with fair newborn bits, and the seed structural probabilities $q(P,r,S)>0$ with their all-mark scalar diamond identities.
- **Newly supplied optional mathematical law choices and external structures:** The qubit Hilbert space $\mathcal H_Q=\mathbb C^2$ and computational basis, the Clifford unitary $U_*$ and initial Pauli axis $\Sigma_0=Y$, the selected harmonic indicator $H_{\rm foc}$ and coupling scale $\theta=\frac{1}{32}$, the precursor-local phase schedule $\varphi_{K,b}$ (and witness value $\varphi_0=\frac{\pi}{2}$), the five-Kraus damping/reset channel form $\mathcal M$, the prepared prefix $a\prec b$ and state preparations, the optional incidence counters, the Benincasa–Dowker interval-action weights $4-2n_0+4n_1-2n_2$, the trace probability rule, and the shared three-outcome erasure-and-confusion detector model $\mathcal C$.

### 5.4 Explicit non-claims and scope limits

1. **Quarantine of Status-M ontology:** All Status-M commitments in `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, and `FALSIFICATION_LEDGER.md` remain strictly outside every definition, equation, and inference in this document.
2. **Finite four-birth horizon only:** Theorem 1, the lookup table $r_P(S)$ with $|r_P(S)|\le\frac{21}{88}<\frac{1}{2}$, and the resulting CPTP instrument are proved solely for parent sizes $|P|\le 3$ (four births); no all-size positive harmonic continuation or asymptotic scaling limit is claimed.
3. **No derivation of quantum mechanics or Born's rule:** Complex Hilbert spaces, Pauli operators, CPTP instruments, and trace probabilities $\operatorname{Tr}[\mathcal B_h(\rho)]$ are postulated mathematical inputs, not derived from order-growth axioms; the classical reduction obstruction in Theorem 4 applies to fixed-basis diagonal instruments on $\mathbb C^2$, not to arbitrary higher-dimensional hidden-variable or Stinespring models.
4. **No derivation of continuum geometry, General Relativity, mass, clocks, or physical constants:** Neither $H_{\rm foc}$, $D$, $Y$, nor $S_{\rm BD}$ is a calibrated metric, curvature scalar, proper-time clock, or gravitational field, and no physical constants ($c,G,\hbar$) or experimental apparatus calibrations are derived.

Within these explicit finite-model and quarantine boundaries, the five-Kraus co-rotating instrument family establishes an exact, diamond-covariant, non-abelian two-way feedback law between quantum state coherence and causal-order growth through four births.

## Scientific review

Native Two-Way Quantum-Order Feedback Author derived the 13-dimensional classification of mark-independent unmarked harmonic potentials through four births, canonical causal-focusing potential $H_{\rm foc}$, non-abelian co-rotating five-Kraus quantum instrument and $4\times 4$ Choi spectrum, closed-form $m$-birth history superoperator and entangled diamond commutation, Heisenberg operator martingale $\mathcal Q_n=2^n\Sigma_n$, fixed-basis classical reduction obstruction, 60-history active bidirectional ledger above $a\prec b$, sign-reversing Benincasa–Dowker interval-action interaction, single-state Pythagorean witness, imperfect-detector $L^1$ lower bounds, null controls, and prefix-dependent similarity gauge analysis. Independent Native Two-Way Feedback Reviewer independently verified all 16 four-element poset classes, backward harmonic constraints, drift coefficients $r_P(S)$, Clifford matrix identities, Kraus sums and Choi eigenvalues, inductive superoperator composition, diamond and suffix commutation, martingale and reduction-obstruction proofs, all 15 structural rows over $580{,}800$, bidirectional and synergistic contrasts, detector bounds, controls, similarity identities, relative links, and Status-M quarantine boundaries. Prospective protocol SHA-256 270104f9ba8e16b6818d708a1e32592beef3d1c964be55f38d57345b8a88cab6; accepted author report SHA-256 b4d889c715f3c807707e9b372d1ac6a5a963f1aea6aef87c75aea2fda4fdbb79; independent scientific review SHA-256 de6f0e20754100296ddaeec10671c2e40c2ee1a2d804e907c6d14efd77d3e0f5.
