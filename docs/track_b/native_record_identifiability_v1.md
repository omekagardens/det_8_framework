# What complete records identify

RI1480 — Conditional finite theorem

Within the intrinsic scalar mark-kernel family defined below, the exact law of complete marked histories identifies the kernel on every reachable decision context, and only there. The exact distribution of complete unlabelled marked endpoints also suffices under the stated covariance premises. Erasing marks has a different effect: a mark-blind growth law removes all kernel information from structural histories, whereas the supplied mark-dependent seed gives an explicit contrast of \(1/54\).

This standalone extension uses the stipulated order-growth model and seed rows in the [conditional theorem package, §1](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) and the independently reviewed [intrinsic-kernel family](../coordination/RI1478_INTRINSIC_KERNEL_FAMILY.md). It does not amend the original independently fair law or select a unique law.

## Fixed model and exact observation contract

Fix a finite integer horizon \(N\ge1\), starting from the empty order. A state has a finite order \(P\), immutable binary marks \(r\), and a passive positive-semidefinite payload \(X\). A birth appends one maximal vertex whose strict past is an ideal \(S\) of \(P\). Every ideal is eligible, including the empty and full ideals. On every admitted row through this horizon, fix the same actual coefficients
\[
q(P,r,S)>0,\qquad \sum_{S\text{ ideal of }P}q(P,r,S)=1.
\]
The coefficients are equivariant under simultaneous relabelling. A proper-slot coefficient may depend on the whole unmarked parent but only on the marks inside its precursor; full slots may read all old marks.

Assume complete marked diamonds: whenever two incomparable births fit inside the horizon, their two orders give equal unnormalized branch maps, with all marks transported. In particular, for old ideals \(S,T\) of a base \(C\), neither new vertex entering the other's precursor,
\[
q(C,r,S)q(C+S,r+b,T)
=q(C,r,T)q(C+T,r+c,S).
\]
This includes equal precursors and both newborn bits. Hold this actual \(q\), eligibility and horizon fixed when comparing kernels; do not rerun an optimizer or extend the law.

Let \(K(S,r|_S)\) denote the isomorphism class of the marked induced precursor. The declared family is
\[
0<p_0(K)<1,\quad p_1(K)=1-p_0(K),\qquad
\mathcal B_{S,b}^{P,r}(X)=q(P,r,S)p_b(K)X.
\]
The fair choice remains a member. Summing over bits and ideals normalizes each row. Intrinsic dependence on \(K\) preserves proper-mark locality and equivariance. In an incomparable swap, each precursor and its induced marks are unchanged, so the two scalar \(p\) factors commute; the \(q\) diamond gives the complete map diamond. Later precursor classes agree under the induced terminal isomorphism. These are sufficient family premises, not a classification of all contextual dynamics.

For normalized nonzero payload, a complete naturally labelled history
\(h=((S_1,b_1),\ldots,(S_n,b_n))\), \(n\le N\), has probability
\[
L_p(h)=\prod_{j=1}^n q(P_{j-1},r_{j-1},S_j)p_{b_j}(K_j).
\]
Label \(j\) means birth step \(j\), not physical time. The observer is supplied the exact probability law of all complete length-\(N\) histories, including precursor choices and marks. Summing normalized continuation rows recovers every prefix marginal without going beyond \(N\).

## Reachable-kernel identification

Define \(\mathcal R_N\) to contain the classes \(K(S,r_h|_S)\) at positive-probability prefixes \(|h|<N\), with eligible positive \(q(P_h,r_h,S)\). Strict positivity and common support make this set independent of the candidate kernel. Under the all-ideal premise, every marked order class of size at most \(N-1\) occurs: build it along a linear extension and use it as the full precursor. A size-\(N\) endpoint does not add another decision.

For two kernels with this same \(q\) and horizon,
\[
L_p|_{\mathcal H_N}=L_{p'}|_{\mathcal H_N}
\quad\Longleftrightarrow\quad
p_b(K)=p'_b(K)\quad(K\in\mathcal R_N,\ b=0,1).
\]

To prove the forward direction, for any reachable prefix and precursor use
\[
p_b(K(S,r_h|_S))
=\frac{L_p(h\cdot(S,b))}
       {\sum_{c=0}^1L_p(h\cdot(S,c))}.
\]
The denominator is the positive common factor \(L_p(h)q(P_h,r_h,S)\). Equal terminal history laws give equal prefix and extension probabilities, hence the same ratio. Conversely, agreement on reachable classes makes every factor of every admitted history equal. Differences outside \(\mathcal R_N\) cannot affect this finite law.

This identifies the declared transition kernel, not an underlying mechanism or arbitrary payload dynamics. One finite realized history has positive probability under every strictly positive family member. It is not the exact law used in the ratio, and no finite-sample estimator, precision, stability or efficiency guarantee is asserted.

## Complete endpoints with and without birth labels

A complete marked endpoint on natural birth labels \(1,\ldots,N\) determines its history: restrict to earlier labels to recover each parent, and take vertex \(j\)'s strict past to recover \(S_j\). Maximal births do not alter old comparisons. Arbitrary names, missing comparisons and summaries do not provide this encoding.

Now erase birth labels but retain the entire marked order. For an endpoint isomorphism class \(E\), let \(t_E\) be the number of distinct naturally labelled history encodings ending in \(E\). It is finite and independent of \(p\). All histories in this fibre have equal probability. Indeed, linear extensions of a fixed finite order connect by adjacent incomparable swaps: move the next desired vertex left past only vertices incomparable with it, then iterate. Each swap preserves the complete map by the marked diamond. Subsequent contexts are transported identically, and equivariance removes arbitrary representative names. Therefore
\[
Q_p(E)=t_E L_p(h)\qquad(h\text{ in the fibre of }E).
\]
Dividing by the same \(t_E\) recovers every history probability from the exact quotient law. Count distinct encodings, not repeated automorphic descriptions of linear extensions.

Thus equality of complete unlabelled marked endpoint distributions has the same kernel-identification consequence. A single endpoint still need not reveal its birth sequence. No efficient fibre-counting method or sufficiency of an arbitrary quotient is claimed.

## Mark erasure and a bounded contrast

If every relevant row is mark-blind, \(q(P,r,S)=q(P,S)\), then for a structural history \(g=(S_1,\ldots,S_N)\),
\[
\Pr_p(g)=
\left[\prod_j q(P_{j-1},S_j)\right]
\sum_{b_1,\ldots,b_N}\prod_j p_{b_j}(K_j)
=\prod_j q(P_{j-1},S_j).
\]
Sum the last bit first: its context uses only earlier marks and its two probabilities sum to one. Repeat backwards. Every kernel then gives the same complete structural-history law, and hence the same law of any fixed deterministic structural summary, including the unmarked terminal order. Proper-slot locality alone is weaker than mark-blindness of every relevant row.

For contrast, use exactly the supplied seed: the singleton full-slot probability is \(1-2/3=1/3\). In the two-chain parent with root mark \(i\), the proper probabilities are \(1/5\) and \(f(i)\), where \(f(0)=1/6\), \(f(1)=1/3\). The full-slot probabilities are consequently
\[
h(0)=19/30,\qquad h(1)=7/15.
\]
They depend on the root mark, not the second mark. These are the displayed seed rows, not a reconstruction of unprinted higher-layer certificates.

Choose the intrinsic constant kernel \(p_0(K)=t\), \(0<t<1\). If three births are already admitted, the first three vertices form a chain precisely when the second and third births select full precursors. The root is marked zero with probability \(t\); summing the other newborn marks contributes one each. Thus
\[
\Pr_t(C_3)=\frac13\left[t\frac{19}{30}+(1-t)\frac7{15}\right]
=\frac7{45}+\frac{t}{18},
\qquad
\Pr_{2/3}(C_3)-\Pr_{1/3}(C_3)=\frac1{54}.
\]
At \(N=3\), this is also the unlabelled unmarked terminal-chain event. At larger \(N\), it is a prefix-history event; an unmarked terminal shape need not reveal that prefix. At \(N=2\), these singleton rows are mark-blind and no three-birth contrast is available. Nothing enlarges the admitted horizon.

This disproves universal structural blindness without proving general structural identification. Mark dependence in an unvisited row is insufficient, and any broader identification claim needs its own observation channel and injectivity proof.

## Claim boundary

The result concerns exact finite mathematical record laws. It supplies no instrument, physical preparation, calibration, repeated-world sampling contract, clock, empirical discriminator or native detector. No all-horizon law, necessity classification, quantum reconstruction, geometry, gravity, agency or theological conclusion follows. The stipulated law and seed dependencies remain conditional; historical source, custody and completion limitations are not repaired by this exposition. Protected validation, independent review, ABSTAIN, Option B/Status M, zero qualification, physical/operational holds and RET-only pause remain.
