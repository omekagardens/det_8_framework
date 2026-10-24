# RI1440: One anonymous four-order observation

Distinct laws in an accepted finite growth family agree on one uniformly sampled pair or triple but disagree on the complete anonymous four-order. For two known parameters in the interval below, the exact total variation and optimal equal-prior forced-classification error are
\[
\operatorname{TV}(P_s,P_t)=2|t-s|/9,\qquad R^*(s,t)=1/2-|t-s|/9.
\]
These are one-observation statements about a specified mathematical experiment. Distinct laws do not make the parameter exactly recoverable from one outcome.

## 1. Declared model and complete finite family

A state has a finite completed partial order, immutable binary marks and an arbitrary complex positive-semidefinite payload \(D\). A birth selects any ideal \(S\), appends a maximal vertex with strict past exactly \(S\), and appends an independently fair bit. The whole unnormalized branch map is \((q(P,S)/2)D\), with stipulated transport to the terminal carrier. This family is fully mark-independent and scalar-passive.

Admission requires strictly positive complete rows, proper-precursor mark locality with whole-unmarked-parent access, transported equivariance and every complete marked incomparable-birth diamond, including full first precursors and arbitrary PSD payloads. One birth is a bookkeeping step, not a physical clock. Fair bits, scalar passivity and the carrier are premises. The accepted finite admission and sampling proof is in [RI1438](RI1438_FOUR_BIRTH_ADJUDICATION.md); no unrestricted marked-family or physical claim is imported.

The earlier rows are: empty parent, probability one; singleton, empty/full probabilities \(1/2,1/2\); two-chain, empty/bottom/full probabilities \(1/3,1/3,1/3\); two-antichain, empty/two separate singletons/full probabilities \(1/6,1/3,1/3,1/6\). Pair-chain probability is \(1/2\).

Use \(A\) for the three-antichain, \(E\) for \(x<y\) with isolated \(z\), \(V\) for \(x<y,x<z\), \(W\) for \(x<z,y<z\), and \(C\) for \(x<y<z\). Their actual history-weighted probabilities are
\[
\mu_3(A,E,V,W,C)=(1,6,2,1,2)/12.
\]
For example, \(E\) receives \((1/2)(1/3)\) from a chain's empty ideal and \(2(1/2)(1/3)\) from the two antichain singletons. Parent types are not weighted uniformly.

Here is the complete proper-ideal table for the fourth birth. “Each” counts distinct ideals separately. Each parent also has its single full ideal with probability \(F_P\).

| Parent | Proper ideal and probability per occurrence |
| --- | --- |
| \(A\) | empty: \(a_1/27\); each of three singletons: \(2a_2/9\); each of three pairs: \(a_3/6\) |
| \(E\) | empty: \(a_2/9\); \(x\): \(2a_4/9\); \(z\): \(a_5/3\); \(xy\): \(a_6/3\); \(xz\): \(a_7/6\) |
| \(V\) | empty: \(2a_4/9\); \(x\): \(2a_8/9\); each of \(xy,xz\): \(a_9/3\) |
| \(W\) | empty: \(a_3/6\); each of \(x,y\): \(a_7/3\); \(xy\): \(a_{10}/6\) |
| \(C\) | empty: \(a_6/3\); \(x\): \(a_9/3\); \(xy\): \(a_{11}/3\) |

With \(F_P=1-K_P\), the complete proper loads are
\[
\begin{aligned}
K_A&=a_1/27+2a_2/3+a_3/2,\\
K_E&=a_2/9+2a_4/9+(a_5+a_6)/3+a_7/6,\\
K_V&=2a_4/9+2a_8/9+2a_9/3,\\
K_W&=a_3/6+2a_7/3+a_{10}/6,\\
K_C&=(a_6+a_9+a_{11})/3.
\end{aligned}
\]
The positive finite domain requires every \(a_i>0\) and every \(F_P>0\). RI1437's exact witness is
\[
a^*=(2/3,2/3,2/3,2/3,38/27,2/3,2/9,2/3,2/3,2/3,29/18),
\]
with full probabilities \((16/81,4/81,7/27,17/27,1/54)\).

Keep all other coordinates and earlier rows fixed, and set
\[
a_5=38/27+t,\quad a_6=2/3-t,\qquad t\in I=(-1/18,2/3).
\]
Only \(F_C\) changes, to \(1/54+t/3\). The lower endpoint makes \(F_C=0\), and the upper makes \(a_6=0\); both are excluded. Finite admission and equality of uniform pair/triple marginals throughout \(I\) are accepted premises. This interval is not asserted to be the entire feasible set. Let \(P_t\) be the law of the completed four-order with labels and marks forgotten.

## 2. Four changing occurrences, three terminal types

Let \(C_j\) denote a \(j\)-chain and \(\sqcup\) disjoint union with no cross-comparisons. Put
\[
X=C_2\sqcup C_2,\qquad Y=C_3\sqcup C_1,\qquad Z=C_4.
\]
The proper table contains \(a_5\) once and \(a_6\) twice. The \(E\) load depends on their fixed sum; the \(C\) full complement changes. The exhaustive changing occurrences are:

| Parent/ideal | Conditional probability | Terminal type | Slope after parent weighting |
| --- | --- | --- | ---: |
| \(E,\{z\}\) | \(38/81+t/3\) | \(X\) | \(1/6\) |
| \(E,\{x,y\}\) | \(2/9-t/3\) | \(Y\) | \(-1/6\) |
| \(C,\varnothing\) | \(2/9-t/3\) | \(Y\) | \(-1/18\) |
| \(C,\text{full}\) | \(1/54+t/3\) | \(Z\) | \(1/18\) |

Each listed ideal has occurrence multiplicity one. The two marked branches have probabilities \(q/2\) and sum to \(q\) when the bit is forgotten. There is no extra automorphism or terminal-maximal-vertex factor in these already history-weighted probabilities.

There are no additional constant incoming contributions to \(X,Y,Z\). The last-born vertex must be maximal. Either maximal deletion from \(X\) leaves \(E\), whose unique isolated vertex is the required precursor. Those symmetric terminal roles do not double a given \(E\)-history transition. For \(Y\), deleting its isolated vertex leaves \(C\) with empty precursor; deleting its chain top leaves \(E\) with the two-chain precursor. For \(Z\), its sole maximal deletion leaves \(C\) with full precursor. This exhausts the maximal-vertex roles.

Thus the absolute probabilities are
\[
\begin{aligned}
P_t(X)&=\tfrac12(38/81+t/3)=19/81+t/6,\\
P_t(Y)&=(\tfrac12+\tfrac16)(2/9-t/3)=4/27-2t/9,\\
P_t(Z)&=\tfrac16(1/54+t/3)=1/324+t/18.
\end{aligned}
\]
They are positive on \(I\) and sum to \(125/324\). Every other terminal probability is fixed, with total mass \(199/324\): neither its incoming occurrences nor earlier history weights change. Hence
\[
P_t=P_0+\frac{t}{18}(3\delta_X-4\delta_Y+\delta_Z).
\]
The signed coefficients sum to zero. Strictly increasing \(P_t(X)\) proves injectivity of the parameter-to-law map on this interval.

## 3. Exact distance and forced decision risk

Use \(\operatorname{TV}(P,Q)=\frac12\sum_H|P(H)-Q(H)|\). Only three types contribute:
\[
\operatorname{TV}(P_s,P_t)=\frac{|t-s|}{36}(3+4+1)=\frac{2|t-s|}{9}.
\]
The decision problem has two fixed known hypotheses \(s,t\in I\), prior probability \(1/2\) each, zero-one loss and a forced choice from one complete anonymous four-order. There is no rejection option. Choosing the more likely hypothesis at each observed type gives
\[
R^*=\frac12\sum_H\min(P_s(H),P_t(H))
=\frac12(1-\operatorname{TV})=\frac12-\frac{|t-s|}{9},
\]
using \(\min(u,v)=(u+v-|u-v|)/2\). For \(s<t\), choose \(t\) on \(X,Z\), \(s\) on \(Y\), and decide or randomize arbitrarily on every other type, where likelihoods tie. Reverse for \(s>t\). This is equal-prior average error, not equal conditional errors or a minimax guarantee.

The open interval has width \(13/18\), so distinct admitted parameters satisfy
\[
0<\operatorname{TV}<13/81,\qquad 34/81<R^*<1/2.
\]
Opposite excluded endpoints approach the distance supremum and error infimum; neither is attained. At \(s=t\), TV is zero and \(R^*=1/2\). Law-level distinguishability retains strictly positive one-observation error.

## 4. What one uniform subset reveals

The kernel \(T_{4,k}\) chooses one \(k\)-subset uniformly using randomness independent of growth and reports only its anonymous induced completed order. No labels, marks or newborn identity are reported. Restrict existing comparisons: removing a chain's middle vertex retains its endpoint comparison. Deleting generating edges and recomputing reachability is a different experiment.

| \(k\) | Observation law | TV between \(s,t\) | Equal-prior forced error |
| --- | --- | --- | --- |
| 1 | singleton with probability one | \(0\) | \(1/2\) |
| 2 | chain and antichain each \(1/2\) | \(0\) | \(1/2\) |
| 3 | \((A,E,V,W,C)\) weights \((1,6,2,1,2)/12\) | \(0\) | \(1/2\) |
| 4 | complete law \(P_t\) | \(2|t-s|/9\) | \(1/2-|t-s|/9\) |

The first three laws use accepted RI1437 consistency. Their parameter blindness is also direct. Every triple of \(X\) is \(E\); three triples of \(Y\) are \(E\) and one is \(C\); every triple of \(Z\) is \(C\). Thus
\[
T_{4,3}(X)=\delta_E,\quad T_{4,3}(Y)=\tfrac34\delta_E+\tfrac14\delta_C,\quad T_{4,3}(Z)=\delta_C.
\]
The signed-difference coefficients become \(3-4(3/4)=0\) for \(E\) and \(-4(1/4)+1=0\) for \(C\). Pair-chain fractions of \(X,Y,Z\) are \(2/6,3/6,6/6\), giving \(3(1/3)-4(1/2)+1=0\). Antichain and singleton cancellations follow from total mass. At \(k=4\), the identity kernel retains the difference.

These are one-uniform-subset statements, not the joint law of repeated draws from one world, an exhaustive triple deck or a labeled table of every pair. An exhaustive labeled pair table determines the order. Repeated subsets share a latent four-order; equal individual marginals do not imply equal joint laws or unconditional independence. Independently regenerating a world before each sample is another experiment. No repeated-sampling performance is adopted here. RI1441's two-draw same-world question is pending, with no result included.

## 5. Scientific and evidence boundaries

This consolidates root-accepted RI1439 following distinct independent review, on the accepted RI1435/RI1437 family. It supplies no fifth-birth continuation, all-horizon sampling law, full feasible-set classification, unrestricted marked-component H classification, physical observation map, informative quantum dynamics, metric, mass, gravity or empirical qualification. Fixed stochastic laws already explain the calculation; no law genesis, parameter-update dynamics or ontological conclusion follows.

Measurement, E, NE and CE retain their actual source, calibration, cost, resource, qualification and execution requirements. Mathematical acceptance approves no experiment in another lane. Protected validation and custody, Option B/Status M, ABSTAIN, zero qualification, the shared 10% usage guard and RET-only pause remain.

The source report is 10,629 bytes, SHA256 72d03ec92e1f50daa2ccec4de4dbf0e81d4750ea411ff5e8d64c36114060b00b; its independent review is 10,136 bytes, SHA256 343d326a80f1229346efd0f245dcab08c45d6414436c4459c46af2a6352f1340. The formulas expose the argument. Administrative checks establish present byte identity, not original provider custody or historical completion. Missing original evidence, late freezes/readbacks and recorded processing failures remain qualified. This documentation grants no execution authority or evidence of a commit, push or publication.
