# RI1442: Two triple observations of one finite world

Two independently selected uniform triples, with replacement from one fixed latent four-order, distinguish laws that one triple cannot distinguish. For two known parameters in the accepted interval, the ordered pair of reported anonymous triple types has law \(J_t\) satisfying
\[
J_t-J_s=\frac{t-s}{24}(\delta_E-\delta_C)\otimes(\delta_E-\delta_C).
\]
Consequently
\[
\operatorname{TV}(J_s,J_t)=\frac{|t-s|}{12},
\qquad R^*(s,t)=\frac12-\frac{|t-s|}{24}.
\]
Here \(R^*\) is optimal equal-prior, forced binary classification error from one reported pair. This conditional finite theorem assumes the sampling protocol below; it supplies no physical readout or independent-reset certificate.

## 1. Accepted finite family and observation inputs

The underlying fixed-seed family is mark-independent and scalar-passive. A birth adds a maximal vertex above an ideal, with an independently fair immutable bit and whole unnormalized payload map \((q/2)D\). Strictly positive complete rows, proper-precursor mark locality with whole-unmarked-parent access, equivariance and complete marked incomparable-birth diamonds are admitted conditions. The payload, fair bits, scalar passivity and birth bookkeeping are stipulated model premises, not physical conclusions.

The fixed prefix has pair-chain probability \(1/2\). The accepted witness is
\[
a^*=(2/3,2/3,2/3,2/3,38/27,2/3,2/9,2/3,2/3,2/3,29/18).
\]
Only \(a_5=38/27+t\) and \(a_6=2/3-t\) vary, with
\[
t\in I=(-1/18,2/3).
\]
All earlier growth rows and other coordinates remain fixed. The full chain-parent complement is \(1/54+t/3\); it vanishes at the excluded lower endpoint, while \(a_6\) vanishes at the excluded upper endpoint. Finite admission and pair/triple consistency throughout \(I\) are accepted inputs. The interval is not a classification of the entire feasible set. The complete growth rows and one-observation proof are in [RI1440](RI1440_FOUR_ORDER_OBSERVATION.md).

Let \(P_t\) be the completed anonymous four-order law. Write \(C_j\) for a \(j\)-chain and \(\sqcup\) for disjoint union without cross-comparisons. Exactly three world probabilities vary:
\[
\begin{aligned}
X=C_2\sqcup C_2:&\quad P_t(X)=19/81+t/6,\\
Y=C_3\sqcup C_1:&\quad P_t(Y)=4/27-2t/9,\\
Z=C_4:&\quad P_t(Z)=1/324+t/18.
\end{aligned}
\]
They are positive on \(I\), with total mass \(125/324\). Every other world probability is individually fixed, with aggregate mass \(199/324\). Thus
\[
P_t-P_s=\frac{t-s}{18}(3\delta_X-4\delta_Y+\delta_Z).
\]

For a world \(Q\), let \(K_Q\) be the law of one uniformly selected anonymous induced completed triple. Use \(A,E,V,W,C\) for the triple antichain, one edge plus an isolate, one bottom below two tops, two bottoms below one top, and three-chain. The common one-triple law is
\[
m(A,E,V,W,C)=(1,6,2,1,2)/12.
\]
In particular \(m(E)=1/2\) and \(m(C)=1/6\). The three changing worlds have kernels
\[
K_X=\delta_E,\qquad K_Y=\tfrac34\delta_E+\tfrac14\delta_C,\qquad K_Z=\delta_C.
\]
Every triple of \(X\) is \(E\). In \(Y\), deleting any chain vertex leaves \(E\), while deleting the isolated vertex leaves \(C\). Every triple of \(Z\) is \(C\). Existing completed comparisons are restricted: deleting a chain's middle vertex preserves its endpoint comparison. Recomputing reachability from surviving generating edges would define a different observation.

## 2. Two selections from one fixed world

First draw one \(Q\sim P_t\). Conditional on that fixed \(Q\), select two three-vertex subsets \(U_1,U_2\) independently and uniformly, with replacement. Their selection seeds are independent of growth. There are sixteen ordered choices, each with conditional probability \(1/16\), including choosing the same subset twice.

Report only the ordered anonymous triple types \((T_1,T_2)\). Report no vertex or subset identities, overlap metadata, birth labels, marks or newborn identity. A relabeling merely permutes the four subsets and leaves this anonymous kernel unchanged.

The world is held fixed during both selections by definition of this static experiment. This is an additional mathematical observation contract, not demonstrated physical nondisturbance or repeatable native access. Conditional independence gives
\[
\Pr_t(T_1=u,T_2=v\mid Q)=K_Q(u)K_Q(v),
\qquad
J_t=\sum_QP_t(Q)\,K_Q\otimes K_Q.
\]
The product is taken before averaging over the shared world. With replacement concerns the conditional subset choices; it does not make reported outcomes unconditionally independent.

## 3. Retain the unchanged worlds

Define the common subprobability measure
\[
B=\sum_{Q\notin\{X,Y,Z\}}P_0(Q)\,K_Q\otimes K_Q.
\]
It is nonnegative, independent of \(t\), and has mass \(199/324\). It can contribute to the same four cells that change with \(t\). Its entries are neither computed here nor assumed zero.

Put \(e=\delta_E\) and \(c=\delta_C\). Then the complete law is
\[
J_t=B+P_t(X)e\otimes e+
P_t(Y)\left(\tfrac34e+\tfrac14c\right)^{\otimes2}
+P_t(Z)c\otimes c.
\]
This gives the absolute cell probabilities:

| Ordered cell | Probability |
| --- | --- |
| \(EE\) | \(B(EE)+103/324+t/24\) |
| \(EC\) | \(B(EC)+1/36-t/24\) |
| \(CE\) | \(B(CE)+1/36-t/24\) |
| \(CC\) | \(B(CC)+1/81+t/24\) |
| Every other cell | \(B(\text{cell})\) |

The constants follow from
\[
19/81+(9/16)(4/27)=103/324,\quad
(3/16)(4/27)=1/36,\quad
(1/16)(4/27)+1/324=1/81.
\]
Counting both ordered mixed cells gives \((103+9+9+4)/324=125/324\). Together with \(B\), the law has mass one. The changed-world contributions originate from positive world probabilities and probability kernels throughout \(I\).

For \(\Delta=t-s\), the common \(B\) cancels:
\[
\begin{aligned}
J_t-J_s
&=\frac{\Delta}{18}\left[3e\otimes e
-4\left(\tfrac34e+\tfrac14c\right)^{\otimes2}
+c\otimes c\right]\\
&=\frac{\Delta}{18}\left[\tfrac34e\otimes e-\tfrac34e\otimes c
-\tfrac34c\otimes e+\tfrac34c\otimes c\right]\\
&=\frac{\Delta}{24}(e-c)\otimes(e-c).
\end{aligned}
\]
Exactly four ordered cells change when \(\Delta\ne0\): \(EE,CC\) by \(+\Delta/24\), and \(EC,CE\) by \(-\Delta/24\). All other differences vanish. The mixed cells are distinct outcomes. Zero row and column sums leave each marginal equal to \(m\), despite a changing joint law.

## 4. Exact decision limit and restricted minimality

Use total variation as half the sum of absolute cell differences:
\[
\operatorname{TV}(J_s,J_t)=\tfrac12\,4|\Delta|/24=|\Delta|/12.
\]
For two fixed known hypotheses, equal priors, zero-one loss and a forced decision from one realized ordered pair,
\[
R^*=\tfrac12\sum_{u,v}\min(J_s(u,v),J_t(u,v))
=\tfrac12(1-\operatorname{TV})=\tfrac12-|\Delta|/24.
\]
This follows from pointwise likelihood selection and \(\min(a,b)=(a+b-|a-b|)/2\). It uses the full normalized laws. Although the common \(B\) cancels from differences, discarding it and treating the remainder as normalized would invalidate the argument.

For \(s<t\), choose \(t\) on \(EE,CC\) and \(s\) on \(EC,CE\). All other outcomes are likelihood ties; either choice or randomization there has the same equal-prior risk. Reverse the choices for \(s>t\). This is average binary decision error, not equal conditional errors, minimax risk, an abstention rule or unrestricted parameter estimation.

The open interval has width \(13/18\). For distinct admitted parameters,
\[
0<\operatorname{TV}<13/216,\qquad 203/432<R^*<1/2.
\]
Opposite excluded endpoints approach the distance supremum and error infimum without attaining them. At \(s=t\), TV is zero and \(R^*=1/2\). One realized pair does not identify the hypothesis with certainty or recover \(t\) exactly.

One triple has the same law \(m\) for all \(t\); two have distinct laws for every \(s\ne t\). Therefore two is the minimum number of draws for law-level distinction within this specified same-world replacement-triple protocol. This is a one-versus-two comparison, not a minimum over every possible observation, an arbitrary-many-draw theorem or operational sample complexity.

## 5. Dependence and independent new worlds

Let \(g(Q)=K_Q(E)\). Conditional independence implies
\[
\operatorname{Cov}_t(\mathbf1_{\{T_1=E\}},\mathbf1_{\{T_2=E\}})
=\mathbb E_t[g(Q)^2]-(\mathbb E_tg(Q))^2
=\operatorname{Var}_t(g(Q)).
\]
This variance is strictly positive throughout \(I\): \(X,Z\) both have positive mass, with \(g(X)=1\) and \(g(Z)=0\). The reported E indicators are therefore unconditionally dependent despite independent selector seeds. Their covariance changes by \(\Delta/24\), since their individual means remain \(1/2\). This does not assert positive covariance for every pair of different outcome indicators.

Now stipulate another experiment. For each fixed hypothesized \(t\), draw \(Q_1,Q_2\) independently from \(P_t\), with mutually independent uniform selectors independent of both growth draws, and report one triple from each new world. This additional independence is not supplied by native growth, elapsed time, discarded records or a physical reset. Averaging factorizes:
\[
H_t(u,v)=
\left(\sum_QP_t(Q)K_Q(u)\right)
\left(\sum_QP_t(Q)K_Q(v)\right)=m(u)m(v).
\]

| Formal experiment | Law | TV for \(s,t\) | Optimal equal-prior forced error |
| --- | --- | --- | --- |
| One uniform triple | \(m\) | \(0\) | \(1/2\) |
| Two replacement triples from one fixed world | \(J_t\) | \(|t-s|/12\) | \(1/2-|t-s|/24\) |
| One triple from each of two independent new worlds | \(m\otimes m\) | \(0\) | \(1/2\) |

The shared-world experiment averages a product. The independent-new-world experiment multiplies separately averaged laws. Neither certifies actual preparation, uniform selection, access, nondisturbance, reset, timing or cost.

## 6. Acceptance and remaining premises

This report consolidates root-accepted RI1441 after distinct independent review. It preserves the fixed finite family and supplies no fifth birth, full feasible-set classification, unrestricted marked-component H, all-horizon law, informative quantum dynamics, native physical forward map, geometry, gravity or empirical prediction. No philosophical premise is needed. RI1443's native-readout admission audit remains unreviewed; no successor conclusion is included.

The other lanes retain concrete blockers. E requires an independently justified actuator/operator failure-state and complete cost, latency and source-to-reset closure certificate. NE requires actual source/reset/control/readout transfer and history-wise certificates in both candidate worlds, with full costs. CE's documentary cleanup closure still leaves diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission requirements, with M1 held. Measurement still needs a selected finite-domain/event serialization contract and its source/build/ABI, qualification and execution prerequisites; the accepted packing limitation is not impossibility of every lossless encoding. No cross-lane result waives these premises or changes existing caps and targets.

The source report is 11,541 bytes, SHA256 92c32fb4634a110b89cab8d6d65155a5ccb0ebbc3363d89c5b6f8cfed4614a76. The distinct review is 10,078 bytes, SHA256 06960dacc42a83b0034d9c0dd4be91e5de99b89c202330b91efc88c0b56a2637. Current hashes and retained checks establish present identity, not original custody or historical completion. Final author completion remains separately attributed; missing original evidence, late historical freezes/readbacks and recorded display, schema, wrapper, patch and review draft-cap failures remain qualified.

Protected validation and custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% guard and RET-only pause remain. This documentation provides no execution grant or evidence of publication, commit or push.
