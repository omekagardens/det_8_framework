# Finite records and rare reachable contexts

RI1482 — Conditional finite-access theorem

This extension of [What complete records identify](native_record_identifiability_v1.md) retains that note's fixed finite growth law, strict positivity, all-ideal support, locality, equivariance and complete marked diamonds. The [intrinsic-kernel family](../coordination/RI1478_INTRINSIC_KERNEL_FAMILY.md) is unchanged. The original fair law remains a member; this result selects no preferred kernel.

## Contract and result

Fix the same finite positive growth law q, all-ideal eligibility, from-empty support and horizon N>=2 as in the complete-record theorem linked above. Keep the intrinsic binary scalar-kernel family
\[
 \mathcal B_{S,b}^{P,r}(X)=q(P,r,S)p_b(K(S,r|S))X,
 \quad 0<p_0(K)<1,\quad p_1=1-p_0.
\]
No q coefficients, optimizer, support or horizon are changed. The linked intrinsic-family result supplies admissibility; the complete-record theorem supplies exact-law identification on reachable contexts.

**New hypothetical sampling premise:** the analyst receives m independent complete naturally labelled marked histories, each distributed as the same length-N law restarted from empty. Here m>=1 is fixed. Histories include every precursor choice and mark. Independent repetitions, resets and complete access are mathematical assumptions, not a physical preparation or observation protocol.

For any fixed nonzero kernel separation delta in (0,1), there are strictly positive admitted kernel pairs differing by delta on a reachable context whose m-history laws are arbitrarily close. Thus strict positivity and exact-law identification do not yield a uniform finite-m discrimination or per-context accuracy guarantee. A quantitative lower bound on encountering the context is missing.

## 1. A rare but reachable context

Let K* be the singleton order marked zero. Fix
\[
 \theta_0=(1-\delta)/2,\qquad \theta_1=(1+\delta)/2,
 \qquad 0<\epsilon<1,
\]
and define two intrinsic kernels
\[
 p^{(i)}_0(K)=
 \begin{cases}\theta_i,&K=K^*,\\ \epsilon,&K\ne K^*,\end{cases}
 \qquad p^{(i)}_1=1-p^{(i)}_0,\quad i=0,1.
 \tag{1}
\]
They agree everywhere except K*, with difference delta there. Every probability is strictly positive; epsilon=0 is never admitted.

Write gamma for the supplied singleton empty-slot probability. Proper-mark locality and normalization give 0<gamma<1 and full-slot probability 1-gamma, under these same premises. The first mark is zero with probability epsilon. Selecting its full singleton precursor at birth two encounters K* with probability
\[
 \epsilon(1-\gamma)>0. \tag{2}
\]
Thus K* is reachable within the unchanged horizon. The construction does not insert a new growth coefficient.

Let P_i be the complete length-N history law. The prefix event “first mark zero, second precursor full, second mark zero” has probability epsilon(1-gamma)theta_i. Hence, defining total variation by
\[
 \operatorname{TV}(P,Q)=\tfrac12\sum_h|P(h)-Q(h)|,
\]
we already have
\[
 \operatorname{TV}(P_0,P_1)\ge\epsilon(1-\gamma)\delta>0.
 \tag{3}
\]
Exact-law identification remains intact.

## 2. Common histories and a distance bound

Let A be the event that the first N-1 marks are all one. Every selected precursor in such a history, including at the final birth, contains only ones or is empty, so K* is never selected. Both laws have exactly the same probability on every complete history in A, including either final mark.

Before the first zero, each selected context assigns probability epsilon to mark zero. Summing its complete q row gives conditional probability 1-epsilon of another one. Therefore
\[
 P_0(A)=P_1(A)=(1-\epsilon)^{N-1}. \tag{4}
\]
The equal subprobability on A is common mass. Summing absolute differences only over its complement gives
\[
 \operatorname{TV}(P_0,P_1)
 \le1-(1-\epsilon)^{N-1}\le(N-1)\epsilon. \tag{5}
\]
This argument allows q to read retained marks; q is the same function in both hypotheses and the histories being compared agree.

Under the declared independent sampling premise, the product laws coincide pointwise on A^m, with common mass (1-epsilon)^{m(N-1)}. Thus
\[
 \operatorname{TV}(P_0^{\otimes m},P_1^{\otimes m})
 \le1-(1-\epsilon)^{m(N-1)}
 \le m(N-1)\epsilon. \tag{6}
\]
No product-law approximation or simulation is used.

## 3. Testing and per-context recovery obstruction

Allow any randomized binary decision rule phi with values in [0,1], interpreted as the probability of choosing hypothesis one. Its errors are
\[
 \alpha=\mathbb E_0\phi,\qquad
 \beta=\mathbb E_1(1-\phi).
\]
For any two finite laws, the expectation difference of a [0,1]-valued function is at most total variation: the positive probability differences sum to TV. Consequently
\[
 \alpha+\beta
 =1-(\mathbb E_1\phi-\mathbb E_0\phi)
 \ge(1-\epsilon)^{m(N-1)},\qquad
 \max\{\alpha,\beta\}\ge\tfrac12(1-\epsilon)^{m(N-1)}.
 \tag{7}
\]
These inequalities hold even for a rule told both candidate laws. For any fixed m,N,delta, taking positive epsilon arbitrarily small makes the lower bound approach one half. No uniform worst-case error strictly below one half is guaranteed by positivity alone across this family.

For a target tolerance 0<r<delta/2, let an arbitrary estimator output an estimate of p_0(K*). Classifying that estimate by the midpoint of theta_0 and theta_1 makes a wrong label impossible whenever the estimation error is less than r. Thus its two estimation-failure probabilities e_i satisfy
\[
 e_0+e_1\ge(1-\epsilon)^{m(N-1)}. \tag{8}
\]
This is already an obstruction for one declared reachable context, before attempting global kernel or mechanism recovery.

The result is uniform over the strictly positive family. It does not rule out increasingly accurate inference for a fixed pair as m grows. It also applies to any fixed further data reduction, since a rule using reduced records is a rule on the complete histories. A single observed record is the case m=1, not an exact probability law.

## 4. A minimal quantitative remedy, with its assumptions

For one predeclared context K*, suppose additionally that:

- Its probability nu of being selected at least once among the N births is at least a known 0<lambda<=1 under each hypothesis.
- The two target probabilities theta_0<theta_1 are known for testing and separated by at least delta>0.
- The hypothetical independent complete-history access contract holds, with no selection on later outcomes.

In each history retain only the newborn mark at the **first** selected K*, if any. Whether that selection occurs is determined before its newborn mark; summing the disjoint first-selection prefixes gives a zero-mark probability theta_i conditional on a hit. Independent histories therefore give independent hit indicators. Conditional on which histories hit, their selected marks are independent Bernoulli(theta_i). This uses one mark per history and does not assert independence of multiple marks inside one history.

Let J be the number of hits. Under either hypothesis J is binomial(m,nu). Its variance is at most m nu. The variance inequality gives
\[
 \Pr(J<m\lambda/2)\le \min\{1,4/(m\lambda)\}. \tag{9}
\]
Indeed m lambda/2<=m nu/2, so a low count deviates from its mean by at least m nu/2.

On J>=m lambda/2, use the selected zero-mark fraction and the midpoint threshold. Its conditional variance is at most 1/(4J). A wrong label requires deviation at least delta/2, giving
\[
 \Pr(\text{wrong label and high count})
 \le \min\{1,2/(m\lambda\delta^2)\}. \tag{10}
\]
One may abstain at low count; (9) bounds that probability. If forced to label there by any rule, each hypothesis has error at most
\[
 \min\{1,(4+2/\delta^2)/(m\lambda)\}. \tag{11}
\]
These conservative symbolic bounds are a single-context consequence of the extra assumptions, not a general learning theorem, optimized sample recommendation or executed estimator. The rare-context construction has no uniform positive lambda as epsilon tends to zero. No preparation method, physical repetitions or calibrated record channel is supplied.

## Claim boundary

The obstruction concerns uniform recovery over the declared positive family. The positive bound is for one predeclared context, under explicitly hypothetical independent complete-history access and a known encounter lower bound. It does not supply physical resets, independent experimental repeats, a calibrated observation channel, a native detector, a hidden-mechanism identification theorem or a sample-size recommendation. No inference about geometry, gravity, agency or theology follows. The original fixed law and horizon, protected validation, custody, ABSTAIN, Status M, zero qualification and RET-only pause remain unchanged.
