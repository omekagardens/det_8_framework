# RI1422: Sampling-consistency adjudication

Uniform anonymous sampling of a completed order is an additional optional constraint on a growth law. It is different from retaining the first births or changing vertex names. The root-accepted RI1421 audit proves that it excludes the admitted Bernoulli law at three completed births and excludes every fixed strictly positive delayed-summable law. This does not invalidate either family's admitted temporal consistency, establish a universal impossibility, select a replacement law or adopt a new DET axiom.

The proofs below state the observation, compose its subset kernels, identify the smallest Bernoulli discrepancy and derive the fixed-law delayed-family obstruction. All law-admission and positive-prefix assumptions remain conditional; there is no physical sampling or empirical validation claim.

## 1. Exact object and observation

Let \(\mathcal P_N\) be the finite set of unmarked \(N\)-element order isomorphism types. For one fixed growth law, let \(\mu_N\) be the law of its completed retained order after exactly \(N\) births, projected to \(\mathcal P_N\). A transition from parent size \(n\) produces size \(n+1\); growth stopped at size \(k\) has used parent rows \(0,\ldots,k-1\).

For \(1\le k\le N\), define \(T_{N,k}\) as the Markov kernel that chooses one uniform \(k\)-subset of the \(N\) vertices, using fresh randomness independent of growth, and reports only the isomorphism type of the restricted **completed order relation**. This is not deletion of generating edges followed by a new transitive closure. It reports no birth labels, subset identifiers, marks, payload or auxiliary edges. A representative of an isomorphism type can be used to sample; relabeling bijects its subsets and leaves the reported kernel unchanged.

The optional requirement is
\[
 \boxed{\mu_N T_{N,k}=\mu_k
        \quad\text{for every }1\le k\le N.}\tag{SC}
\]
Thus an anonymous subsample of a later order would have the same law as growth stopped at the smaller size. It is an equality of probability distributions, not a claim that actual suborders in a single realization coincide with the first-born vertices. Sizes \(N,k\) are fixed design data.

## 2. One-vertex deletion is enough, if required at every size

The kernels themselves satisfy
\[
 T_{N,m}T_{m,k}=T_{N,k}\qquad(1\le k\le m\le N).
\]
Indeed, for a particular \(k\)-subset \(U\) of a fixed \(N\)-vertex representative, there are \(\binom{N-k}{m-k}\) intermediate \(m\)-subsets containing it. Its probability under the two-stage procedure is
\[
 \frac{\binom{N-k}{m-k}}{\binom Nm\binom mk}
 =\frac1{\binom Nk}.
\]
Restriction of a completed relation is associative. Forgetting names between stages changes neither these probabilities nor the final isomorphism type. This argument does not require independent inclusions of vertices or an exchangeable growth law.

Consequently, if
\[
 \mu_nT_{n,n-1}=\mu_{n-1}\qquad\text{for every }n\ge2,
\]
iteration and the kernel composition identity give (SC) for every \(N,k\). Conversely (SC) includes those one-deletion identities. This equivalence concerns a consistent family across all sizes. A check at just one size or on just one realized order is insufficient.

## 3. Smallest Bernoulli witness: three births, two sampled vertices

Use the admitted from-empty product-edge realization at a separately fixed \(p\in(0,1)\). On the first three birth labels, the independent forward edges \(E_{12},E_{23},E_{13}\) each have probability \(p\); the retained relation is their transitive closure. Labels here are proof auxiliaries, not reports.

At size two there is one possible forward edge and no intermediate vertex. Hence, writing \(C_2\) for the two-chain and \(A_2\) for the two-antichain,
\[
 \mu_2(C_2)=p,\qquad \mu_2(A_2)=1-p.
\]
In the completed size-three order, pairs \(\{1,2\}\) and \(\{2,3\}\) are comparable precisely when their respective direct edges are present. Each therefore has comparability probability \(p\).

For pair \(\{1,3\}\), comparability occurs either through its direct edge or through the two-step path via vertex 2. Splitting on the direct edge gives the disjoint-event identity
\[
 \Pr(1\prec3)=p+(1-p)p^2.
\]
There are no other possible paths on these three forward-labeled vertices. The three possible sampled pairs are equally likely, independently of the edges. Therefore
\[
 \boxed{(\mu_3T_{3,2})(C_2)
       =p+\frac{(1-p)p^2}{3}>p=\mu_2(C_2).}
\]
Equivalently, the antichain probability is
\[
 (\mu_3T_{3,2})(A_2)=(1-p)\left(1-\frac{p^2}{3}\right).
\]
Since the output alphabet consists of these two types, their total variation distance, with convention \(d_{\rm TV}(P,Q)=\sup_A|P(A)-Q(A)|\), is exactly
\[
 \boxed{d_{\rm TV}(\mu_3T_{3,2},\mu_2)
       =\frac{(1-p)p^2}{3}>0.}
\]

This is a symbolic three-edge proof, not a coefficient enumeration or numerical calculation. The causal reason for the extra term is precise: sampling \(\{1,3\}\) retains their completed comparability even when vertex 2, which supplied a path, is discarded. Removing 2 from a generating DAG and then recomputing reachability would erase this particular mechanism, but would be a different kernel and not this audit's observation.

No smaller \(N\) can witness failure: \(k=N\) is the identity kernel, and every nonempty one-vertex order has the same type. Thus all cases with \(N\le2\) are automatic. The witness uses completed births 1, 2 and 3, hence parent rows 0, 1 and 2; it involves no later continuation or parent-five seed.

## 4. Delayed-summable laws fail by their fixed-size chain limit

Fix one admitted law \(D(F,L,\epsilon)\), with its admitted strictly positive finite prefix F through parent \(L\ge5\) and positive summable tail bounds from parent \(L+1\). Its rebuilt later transitions satisfy conditional proper-birth probabilities at most \(\epsilon_n\), where \(0<\epsilon_n<1\) and \(\sum_{n\ge L+1}\epsilon_n<\infty\); a full birth appends above every old vertex and creates no incomparable pair. The admitted prefix and full marked layerwise extension premise remain assumptions. All statements in this section are for that one fixed law.

For any m>=L+1, a union bound makes the probability of any proper birth from parent m onward at most the summable tail from m, which tends to zero. Thus only finitely many proper births occur almost surely, without independence. Write I(P_N) for the number of unordered incomparable pairs and C_k for the k-element chain type. After the last proper birth the finite incomparable count is unchanged by all remaining full births. This eventual finiteness and the sampling argument below give
\[
 \mu_N^D T_{N,k}\longrightarrow\delta_{C_k}
 \quad\text{in TV for each fixed }k\ge2.
\]
For completeness, this consequence needs no integrability of the eventual incomparable count: conditional on a completed order, a fixed incomparable pair enters the sample with probability \(\binom k2/\binom N2\). Thus
\[
 \Pr(Q\ne C_k\mid P_N)
 \le \min\left\{1,\frac{\binom k2}{\binom N2}I(P_N)\right\}.
\]
For almost every history, the count eventually stabilizes at a finite value; the right side tends to zero and is bounded by one. Bounded convergence proves the displayed chain limit. This is a manual restatement of the accepted fixed-\(k\) argument, not a new rate or a uniform family estimate.

If (SC) held, its left side would be the constant distribution \(\mu_k^D\) for every \(N\ge k\). Its limit would then force
\[
 \mu_k^D=\delta_{C_k}\quad\text{for every fixed }k\ge2.
\]
But strict positive finite-history support already contradicts this at \(k=2\). After the unique first vertex, the empty precursor in the singleton parent is a legal proper ideal with positive probability for every admitted mark. Choosing it at birth 2 yields \(A_2\); both newborn marks have positive probability. Hence
\[
 a_D:=\mu_2^D(A_2)>0.
\]
Here strict support means positivity of every admissible finite history, not a finite support for the infinite-history measure.

The contradiction also supplies a finite, though not numerically located, witness: by convergence there is a finite \(N_D\) such that for all \(N\ge N_D\),
\[
 (\mu_N^DT_{N,2})(A_2)<a_D/2,
 \qquad
 d_{\rm TV}(\mu_N^DT_{N,2},\mu_2^D)>a_D/2.
\]
No common \(N_D\), quantitative rate, or smallest witness is claimed across arbitrary prefixes and tails. By section 2, failure of the full identity also entails failure of at least one one-vertex deletion identity for this fixed law, without locating that size. This does not assert failure at every adjacent size.

The conclusion covers the original fixed parent-five family as a subfamily, and the enlarged delayed family separately. It does not conflate their prefixes. No extension construction or layerwise ratio sufficiency is rederived here.

## 5. Why temporal consistency and equivariance do not imply (SC)

Retained-prefix temporal consistency restricts the history to its first \(k\) births. It selects the distinguished oldest \(k\) vertices, not a uniform subset of all \(N\). In an admitted retained growth history, that restriction has precisely the earlier completed order \(P_k\). This history projection generally cannot even be recovered from a single anonymous terminal-order type, which omits ages and birth identities.

Anonymous uniform deletion can discard an old vertex and retain a newer vertex. It also preserves every relation in the completed order, including a relation whose generating path used a discarded vertex. The Bernoulli witness shows that replacing the distinguished prefix with this random subset changes the distribution.

Equivariance says that changing vertex names transports the same mathematical construction and observation. It does not say that replacing old vertices by arbitrary later vertices leaves the stopped-growth distribution unchanged. Randomly renaming a terminal order also leaves its unmarked distribution and its sampling kernel unchanged; that coordinate operation cannot repair the strict discrepancy in section 3.

The admitted Bernoulli law therefore directly witnesses the logical separation: temporal retained-prefix consistency and coordinate equivariance coexist with failure of (SC). For the delayed laws, the fixed-size limit gives an additional obstruction. Neither failure invalidates their previously admitted temporal growth consistency.

## 6. Scope and the next finite question

This audit establishes an optional definition, a kernel-composition theorem with an all-sizes adjacent-deletion equivalence, the smallest Bernoulli counterexample, and failure of the optional property for every fixed strictly positive delayed-summable law. The Bernoulli claim has fixed parameter p in (0,1), and the delayed claim has its own law-dependent positive antichain mass and finite witness horizon. Neither claim supplies a uniform horizon across arbitrary delayed laws, a rate, or a numerical cutoff.

Exclusion of these two classes does not exclude every admissible growth law. No replacement candidate is supplied, no optional identity is adopted as a physical or DET principle, and no general incompatibility between strict positivity, native diamonds and sampling consistency is established. The original parent-five fixed-prefix family and its enlarged delayed family remain distinct; the result applies to each fixed member at the stated scope. Prior finite-prefix matching and critical-sample results are neither rederived nor changed by this marginal audit.

The next RI1423 question remains OPEN: are strict positivity, complete marked native diamonds and optional sampling consistency already incompatible through three completed births, or is there a complete positive prefix through parent size two satisfying both? No answer or prospective successor result is adopted. Even a future finite compatibility result would leave all-size sampling consistency unproved unless a separate extension argument establishes it.

The observation concerns only unmarked completed-order marginals. It does not replace native records or quantum payload, provide physical readout or clock certificates, or establish informative quantum dynamics, geometry, gravity, mass, native empirical predictions or application advantage. Conditional mathematical admission and operational qualification remain different gates.

## 7. Other lanes and retained process limits

E retains the accepted conditional finite-entry theorem and its accepted exact time-origin correction copy. With absolute entry time tau, controlled start t0, attempt start a and duration bound B, tau-a<=t0-a+B. This does not supply actual plant/initial/input/rate calibration, bounded sensing/update/lag/action or clock certificates. Nominal 60-second updates, step 60, step 44, horizon 64 and dwell W20 do not become interchangeable. Pre-entry ceilings, lower elapsed-time dwell bounds, physical reset/storage, full source-to-reset and failure costs, matched persistent 32-packet MHE resources and held-out reliability/quality/time/energy remain actual prerequisites. No new generic reduction or execution is admitted by this mathematical result.

NE retains its common actual pre-command source and independently justified transfer requirements. Candidate-indexed one-world guarantees do not establish counterfactual common-source equality. The accepted sum of source, calibration and target risks is an unconditional gate-and-error bound, not error conditional on acceptance. Physical source, reset/command transfer, control/readout, target sampling and clock/time/energy inputs remain absent; source costs must supplement 32*n_cal+2*N preparations/readouts.

CE retains the unresolved exact instantaneous resident-memory ceiling of 256 MiB before import for the selected process, together with CPU 10 s, wall 30 s, one process/no children, output 140 KiB, no network and failure/cleanup evidence. A footprint-triggered fatal policy differs from a no-overshoot resident-set guarantee. Installed-version applicability, entitlements and durable post-kill evidence remain unestablished. Bounded search is not universal impossibility and supplies no execution permission.

Measurement retains the missing applicable versioned selected-image/current-cache membership and safe-composition mechanism. No acquisition, replay, native call or nominal-calculation execution is supplied. The fixed 17-window rank interpretation requires justified null exchangeability and fixed-label/selection premises; conditional admission needs corresponding conditional symmetry. Its minimum unrandomized p-value is 1/17, above 5%, and zero comparison contrast still triggers the original abstention rule. Disjointness, stationarity or common filtering do not establish the null. No observed significance, physical calibration or native DET prediction is claimed.

The root accepted RI1421 after full manual reasoning and a distinct independent review. Its current process disposition establishes no new author or reviewer timing violation; recorded author/reviewer observations and externally attributed completion times retain their actual scope. Current file identities cannot reconstruct historical inspection or custody. RI1419's original complete manuscript readback was late relative to its substantive cutoff and remains a failure; current mathematics does not waive or backdate it. Older timing, custody, guard/reset-sequencing and helper-count failures, missing RI1389 evidence and RI1401 late-freeze remain recorded.

An earlier publication-preparation attempt remained unfrozen after usage-guard holds and its original deadline expired; its initial administrative dispatch syntax failure and incomplete packaging remain historical failures. This replacement uses a separately authorized new bounded preparation. It does not backdate completion, repair the earlier process, or change the accepted mathematics or operational gates.

This publication preparation uses manual reasoning and new inert byte/text/JSON/archive checks only. No scientific code, numerical simulation, coefficient enumeration, frozen-program import/execution, release operation, network access, probe or repository/index mutation is performed. Protected validation and custody, Option B/Status M, operational ABSTAIN, zero qualification, shared supported 10% stop/reset conditions, existing schedules and the RET-only pause remain. Distinct publication review, exact root acceptance and current repository/remote verification remain pending gates.
