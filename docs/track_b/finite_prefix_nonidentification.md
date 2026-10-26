# QR-LD032 — Exact finite-prefix agreement with different limiting density

Status: independently reviewed and accepted by the coordinator as conditional mathematics on 2026-10-26. This is a scoped public derivative of the frozen QR-LD032 report; no scientific execution or physical validation is claimed.

The underlying unrestricted admission conditions, fixed-p construction and density results are collected in [the native law package](native_symmetric_law_nonuniqueness_v1.md). This construction does not preserve the separately prescribed finite seed in general. The statement compares two laws after fixing p and m; it does not use one alternative law for every horizon, retune a law with N, or rule out learning from longer records or additional assumptions.

**Theorem.** For every fixed \(p\in(0,1)\) and integer \(m\ge1\), the candidate below defines one admitted all-size law \(L_{p,m}\). It agrees with the fixed-p law \(L_p\) on every complete canonical marked history through \(m+1\) births, including its unnormalized payload map. Nevertheless, under \(L_{p,m}\),
\[
\mathbb E R_N\longrightarrow0,\qquad R_N\longrightarrow0
\quad\text{in probability},
\]
whereas accepted QR-LD030 gives \(R_N\to1\) almost surely under \(L_p\). No almost-sure density-zero conclusion is made.

## 1. Fixed candidate and direct admission

Fix p and m throughout, put \(\lambda=p/(1-p)>0\), and define
\[
t_k=
\begin{cases}
\lambda^k,&0\le k\le m,\\
\lambda^m2^{-2^{k-m}},&k\ge m+1.
\end{cases}
\qquad
Z_n=\sum_{k=0}^n\binom nk t_k.
\tag{1}
\]
At an n-vertex parent P, each actual subset A receives probability \(t_{|A|}/Z_n\). Its downward closure is the newborn's strict past. The new immutable bit is independently fair, and the payload branch is \(q(P,r,S)X/2\).

For an actual ideal S write \(s=|S|\) and \(a=|\operatorname{Max}(S)|\); a is distinct from the fixed cutoff m. The closure equals S exactly when
\[
\operatorname{Max}(S)\subseteq A\subseteq S.
\]
Consequently the structural kernel is
\[
G(s,a)=\sum_{k=a}^s\binom{s-a}{k-a}t_k,\qquad
q(P,r,S)=G(s,a)/Z_n.
\tag{2}
\]
Every weight is strictly positive and each normalizer is finite. Every ideal has a generating subset, and the closure events partition all actual subsets. Thus all ideal occurrences have positive mass and each complete row sums to one. Empty/full ideals are retained; the empty ideal has mass \(1/Z_n\), and the empty-parent row is one.

The formula ignores marks, satisfying proper selected-mark locality and permitted full-slot dependence. Its counts are invariant under transported relabeling, giving equivariance.

For any n-vertex base C and ideals S,T, the second old precursor in either incomparable-birth route excludes the other newborn. Its induced order, size and maximal count remain unchanged. Both structural products therefore equal
\[
\frac{G(|S|,|\operatorname{Max}(S)|)\,
      G(|T|,|\operatorname{Max}(T)|)}
     {Z_nZ_{n+1}}.
\tag{3}
\]
This covers empty, full-base and equal precursors, every inherited marking and both arbitrary newborn bits. Both complete marked routes multiply the same transported arbitrary complex positive-semidefinite payload by (3)/4. The sum of all one-step ideal/bit maps is the identity. Admission has been checked directly before using the candidate.

To realize one all-size law, independently sample A_j on the deterministic old carrier \([j-1]\) with probabilities (1), and independent fair bits. Draw \(i\to j\) iff \(i\in A_j\), then take transitive closure. New subsets are independent of the entire old history, and closure gives exactly (2) conditionally at every history. This realizes the consistent finite canonical marked histories and their infinite extension. Inclusions within one A_j are generally dependent; only different target births are independent.

## 2. Exact agreement through the prescribed horizon

For every parent size \(n\le m\), only the geometric prefix of (1) occurs:
\[
Z_n=(1+\lambda)^n,\qquad
G(s,a)=\lambda^a(1+\lambda)^{s-a}.
\]
Hence on every actual ideal, with all inherited marks,
\[
q(P,r,S)
=\frac{\lambda^a(1+\lambda)^{s-a}}{(1+\lambda)^n}
=p^a(1-p)^{n-s}
=q_p(P,r,S).
\tag{4}
\]
This includes the empty parent and all empty/full slots.

A complete N-birth marked canonical history has probability
\[
2^{-N}\prod_{n=0}^{N-1}q(P_n,r_n,S_n).
\tag{5}
\]
If \(N\le m+1\), every parent in (5) has size at most m, so (4) proves exact equality to \(L_p\). The complete composed payload map has the same scalar coefficient on every common initial payload X, hence also agrees without normalization or trace division. This is equality of full histories, not only terminal order summaries.

Manual check: take \(p=1/2,m=1\). Then \(t_0=t_1=1,t_2=1/4\). The singleton empty/full row is \((1/2,1/2)\), exactly the fixed-p row; each particular two-birth order/bit history has probability \(1/8\). At parent size two, \(Z_2=13/4\). The two-antichain ideal row is \((4,4,4,1)/13\), with sum one, whereas the fixed-p row is \((1,1,1,1)/4\). This example agrees through two births and can already differ at the next birth.

## 3. Cardinality bound, including the exceptional ratios

Let \(K_n=|A_{n+1}|\), \(w_{n,k}=\binom nk t_k\), and \(\mu_n=\mathbb E K_n\). For \(0\le k<n\), the exact adjacent ratios are
\[
\frac{w_{n,k+1}}{w_{n,k}}
=\frac{n-k}{k+1}
\begin{cases}
\lambda,&0\le k<m,\\
1/4,&k=m,\\
2^{-2^{k-m}},&k\ge m+1.
\end{cases}
\tag{6}
\]
Only applicable indices are used. In particular, the junction \(k=m\) does not obey the displayed tail formula.

For \(n\ge1\), define
\[
d_n=\max\{1,\lceil\log_2\log_2(2n)\rceil\},\quad
c_n=m+d_n,\quad B_n=c_n+2.
\tag{7}
\]
If \(k\ge c_n\), then \(k\ge m+1\) and \(2^{k-m}\ge\log_2(2n)\), so the corresponding ratio is at most \(1/2\). If \(c_n\le n\), the tail satisfies
\(w_{n,c_n+r}\le2^{-r}w_{n,c_n}\) on its allowed indices. Therefore
\[
\mu_n
\le c_n+\sum_{r\ge1}r\,\Pr(K_n=c_n+r)
\le c_n+\sum_{r\ge1}r2^{-r}
=B_n.
\tag{8}
\]
Terms outside the support are zero. If \(c_n>n\), the bound follows from \(\mu_n\le n<c_n\). No bound on the exceptional finite prefix ratios is needed.

The sequence B_n is nondecreasing and
\[
B_n\le m+3+\log_2\log_2(2n).
\tag{9}
\]
Thus the required explicit \(O(m+\log\log n)\) bound holds. The threshold depends on n only for analysis; the weights and cutoff of the law never change.

All subsets of a given cardinality have equal probability. Exchangeability and the sum of inclusion indicators give the exact single-vertex marginal
\[
\Pr(i\in A_{n+1})=\mu_n/n,\qquad i\le n.
\tag{10}
\]
This is not an assertion of within-birth edge independence.

## 4. Reachability and limiting density

Fix \(\delta\in(0,1)\), with p and m still fixed, and let \(N\ge2\). For labels \(i\ge\lceil\delta N\rceil\) and \(j>i\), each forward path
\(i=v_0<\cdots<v_\ell=j\) requires one inclusion at each of distinct target births. Its exact probability factors across those births:
\[
\prod_{r=1}^{\ell}
 \frac{\mu_{v_r-1}}{v_r-1}
\le \left(\frac{B_N}{\delta N}\right)^\ell.
\tag{11}
\]
There are \(\binom{j-i-1}{\ell-1}\) such length-\(\ell\) paths. A union bound over all forward paths, with no independence between paths assumed, yields
\[
\Pr(i\prec j)\le
\beta_N(1+\beta_N)^{j-i-1}
\le\rho_N(\delta):=\frac{B_N}{\delta N}e^{B_N/\delta},
\quad \beta_N=\frac{B_N}{\delta N}.
\tag{12}
\]
Comparability is exactly forward reachability in this representation. Bound (9) gives
\[
e^{B_N/\delta}\le
e^{(m+3)/\delta}
[\log_2(2N)]^{1/(\delta\ln2)}.
\]
For fixed m and delta, a fixed logarithmic power times \(O(m+\log\log N)\), divided by N, tends to zero. Hence \(\rho_N(\delta)\to0\).

Let R_N be the number of unordered comparable pairs divided by \(\binom N2\). Pairs whose earlier label is below \(\lceil\delta N\rceil\) number at most \(\delta N^2\); bound their probabilities by one. All other pairs obey (12). Thus
\[
0\le\mathbb E R_N\le
\min\left\{1,\frac{2\delta N}{N-1}+\rho_N(\delta)\right\}.
\tag{13}
\]
First take \(N\to\infty\) with delta fixed, giving \(\limsup\mathbb E R_N\le2\delta\); then let delta decrease to zero. This proves convergence in mean to zero. Markov's inequality proves convergence in probability:
\[
\Pr(R_N>\varepsilon)\le\min\{1,\mathbb E R_N/\varepsilon\}\longrightarrow0
\quad(\varepsilon>0).
\]
No within-birth or pair-indicator independence has been smuggled into the argument.

## 5. Exact finite-prefix limitation

For each fixed p,m, the restrictions of \(L_p\) and \(L_{p,m}\) to the complete history sigma-algebra through \(m+1\) births are equal. Every statistic measurable from that horizon therefore has the same distribution under these two laws, although their established asymptotic density statements differ.

The quantifiers are \(\forall p\,\forall m\,\exists L_{p,m}\). Different prescribed cutoffs may select different alternatives; each selected alternative is one fixed law for all N. This is not a law with a horizon-varying cutoff. Nor does one alternative agree with \(L_p\) at every finite horizon simultaneously: agreement on all finite cylinders would give the same infinite history law, incompatible with these different limits.

This result concerns this asymptotic distinction in the unrestricted model at a fixed finite horizon. It does not prohibit all inference, additional restrictions, or distinctions from longer records. It does not extend the separately prescribed mark-dependent seed or assert a coordinate change.

There is no almost-sure density-zero proof, preferred law, physical readout/time/dimension/metric/gravity, quantum reconstruction, computational advantage or novelty claim. Auxiliary labels/subsets remain proof devices. Supplied conventional attribution is unchanged without new source acquisition.

All inherited custody/failure limits and LD023's 65-second NONCOMPLIANCE remain unwaived. Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. The frozen source retains its original handoff language. This derivative records completed distinct review and coordinator acceptance; subsequent proposals require their own disposition.

## Review identity and limits

Frozen author REPORT: 9474 bytes, SHA256 `0910872c97717449aa9b5dd47caf4ad09e2bd2e14bc99361fee1818d8317d867`; PREMISES: 6498 bytes, SHA256 `2715ab663577af10542bdf99a97b32ea5f501b98c3528c92f4f39b862bbd213e`. Distinct REVIEW: 8856 bytes, SHA256 `9a4b7493435a9c8f3477b371bbdd246c1844afe0c2e96a0fc6520eab0a4c93fa`. Coordinator disposition QR-LD032: 17522 bytes, SHA256 `acfbfeaab8de74c7d633f00cd248048cccdae37757a5edb62b82ca5783b55a3b`.

The coordinator checked the direct admission proof, finite-prefix indexing, geometric-to-thin-tail junction, cardinality bound, independence across target births, path bound and order of limits against the accepted model and dependency scopes. Retained input identities and available raw records were checked. One reviewer usage observation is retained only as a summary; historical final sessions were not reopened. Current byte equality does not repair historical custody or waive inherited failures. No novelty, implementation efficiency, selected physical law, dimensionality, clock or detector map follows.
