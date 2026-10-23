# RI1420: Finite-prefix adjudication

An admitted positive growth law can, conditionally on the full marked layerwise ratio-extension premise, retain any finite admitted prefix and then use rebuilt summable proper-birth layers. This permits delayed laws that exactly match a fixed Bernoulli law at any specified finite horizon while eventually acquiring only finitely many incomparable pairs. The matching rival may change with the horizon. Uniform forced discrimination over this enlarged family therefore fails, although pointwise discrimination against each fixed rival can succeed asymptotically.

The root accepts the RI1419 conditional mathematics after distinct review, with an explicit original author late-readback qualification. Current mathematical acceptance does not certify that author's original process compliance. The construction, finite matching, quantifier distinction and sufficient restricted-family bounds follow below; no physical law selection or operational qualification is implied.

## Notation and admitted model

A parent P is a finite retained order with immutable bit marking r. An eligible precursor S is an order ideal of P. A birth appends a new maximal vertex whose strict past is S, denoted P+S, and gives it an independent fair bit. The nonnegative row q(P,r,S) sums to one over all ideal occurrences; the probability of a specified precursor and newborn bit is q/2. A full birth has S=P; a proper birth has S strictly contained in P. Old relations persist. The common admitted scalar-passive payload transport is denoted by \(\mathfrak D\); it is an assumption about the branch maps, not a new physical dynamics derived here.

The admitted Bernoulli law B_p starts from the empty parent, with separately fixed p in (0,1). It can be realized by independent forward-edge Bernoulli(p) coordinates followed by transitive closure, and belongs to the admitted marked model. Its auxiliary edges are proof coordinates, not part of the marked growth-history observation below. Write I(P) for the number of unordered incomparable pairs. All claims retain the conditional positive-prefix and full marked-ratio sufficiency premises.

## 1. What is admitted, and the enlarged family

An admitted prefix through parent size \(L\) specifies all transition rows \(q(P,r,S)\) for \(|P|=0,\ldots,L\), including every marked parent, every eligible ideal occurrence and every full complement. It is not a single observed trajectory. It is strictly positive, normalized, record-local and equivariant and satisfies every complete marked diamond contained in that prefix. Newborn bits are fair and the branch maps are the admitted scalar-passive maps \(q(P,r,S)\mathfrak D/2\).

We use the inherited layerwise sufficiency premise: for an admitted positive prefix, the maximal-deletion potentials provide the proper-slot ratios at the next layer; assigning positive scales consistently to their components and positive full complements yields a marked-admissible extension. This is the full marked ratio characterization already admitted for the extension construction, not a new theorem or a consequence of DET primitives proved here.

The construction below uses positivity of the existing prefix, the admitted sufficient ratio theorem, finite complete layers and normalization. It uses no numerical seed coefficient or special identity of parent size five. It does not certify arbitrary tables that have not first been admitted or remove the ratio-sufficiency premise.

Explicitly define \(\mathcal D\) to consist of laws
\[
 D(F,L,\epsilon),
\]
where \(L\ge5\), \(F\) is such an admitted prefix through parent \(L\), and
\[
 0<\epsilon_n<1\quad(n\ge L+1),\qquad
 \sum_{n=L+1}^{\infty}\epsilon_n<\infty.
\]
Each law is constructed in section 2. This is an **enlarged delayed-summable family**. RI1407's exact parent-five fixed-prefix family is the subfamily with \(L=5\) and its particular admitted prefix \(F_*\). Other prefixes are not silently identified with \(F_*\).

For a separately fixed \(p\in(0,1)\), let \(\mathcal D_p^B\subseteq\mathcal D\) be the subfamily with \(F\) equal to the from-empty Bernoulli law's complete rows through parent \(L\). That finite restriction is admitted because the supplied Bernoulli law is admitted at all sizes. We do not assert that this Bernoulli-prefix subfamily belongs to RI1407's original fixed-prefix family.

## 2. Construction and first boundary diamond

Retain \(F\) exactly through parent \(L\), including its full probabilities. For every \(n\ge L+1\), recompute, from the smaller rows of this newly constructed law,
\[
 u_n(P,r,S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}},
 \qquad S\subsetneq P,\quad |P|=n.
\]
Define
\[
 K_n(P,r)=\sum_{S\subsetneq P}u_n(P,r,S),\qquad
 M_n=\max_{|P|=n,r}K_n(P,r),\qquad
 \alpha_n=\frac{\epsilon_n}{1+M_n}.
\]
The sums count every ideal occurrence; the maximum covers the entire marked layer. Set
\[
 q(P,r,S)=\alpha_nu_n(P,r,S)\quad(S\subsetneq P),\qquad
 q(P,r,P)=1-\alpha_nK_n(P,r).
\]

At a finite layer, positive smaller probabilities make every product and reciprocal finite and positive. There are finitely many orders, markings and ideals on a fixed finite carrier, so \(0<M_n<\infty\). Hence
\[
 0<\alpha_nK_n(P,r)
 \le\frac{\epsilon_nM_n}{1+M_n}<\epsilon_n<1.
\]
All proper probabilities are positive, the full complement is greater than \(1-\epsilon_n\), and complete rows sum to one. The common scale is allowed on all ratio components. Locality and all inherited marked ratio equations follow from the admitted characterization; label transport preserves the products, complete maximum and full complements.

At the **first new layer**, \(n=L+1\), the new boundary diamonds have a retained base \(C\) of size \(L\). For old ideals \(S,T\subseteq C\), they require
\[
 q_F(C,r,S)\,q_{\rm new}(C+S,r+b,T)
 =
 q_F(C,r,T)\,q_{\rm new}(C+T,r+c,S).
\]
Both second precursors are proper in their intermediate parents because they exclude the other newborn. The retained first factors, including full first births when \(S=C\) or \(T=C\), enter the newly recomputed potentials. The sufficient ratio theorem enforces this equality for all old and newborn marks, including equal precursors. Both routes act on the entire transported PSD payload with the same scalar product divided by four.

New full complements at size \(L+1\) do not occur as second factors in that first boundary diamond. They do occur as first factors at the following boundary; the next layer's potentials must therefore use those new values. Induction repeats this check at every size. No old later coefficient, completed harmonic continuation or independent proper-only scaling of an existing whole law is reused.

This supplies an admitted positive extension at every layer, conditional on the stated ratio sufficiency. The normalized finite-history probabilities \(q/2\) are consistent and define the admitted classical history measure. The construction retains the whole old law prefix, not merely selected finite records.

## 3. Eventual finite proper births and exact indexing

Let \(A_n\) denote a proper birth from size \(n\) to size \(n+1\). Summing over both newborn bits gives
\[
 \Pr_D(A_n\mid\mathcal F_n)
 =\alpha_nK_n(P_n,r_n)\le\epsilon_n,\qquad n\ge L+1.
\]
For every \(m\ge L+1\),
\[
 \Pr_D\!\left(\bigcup_{n=m}^{\infty}A_n\right)
 \le\sum_{n=m}^{\infty}\epsilon_n\longrightarrow0
 \quad(m\to\infty).
\]
Thus only finitely many proper births occur after the retained prefix, almost surely, without independence. The prefix itself has finitely many births, so the total is finite almost surely.

Preserving parent sizes \(0,\ldots,L\) preserves **births \(1,\ldots,L+1\)**. The first potentially different birth has parent size \(L+1\) and produces size \(L+2\). If \(K\) is the last proper parent index at or after \(L+1\), with \(K=L\) if there are none, then \(N_*=\max\{L+1,K+1\}\) has only full transitions afterward. This is a pathwise eventual index, not a claimed stopping time. The retained order thereafter is
\[
 P_N=P_{N_*}\oplus C_{N-N_*}\qquad(N\ge N_*).
\]
In particular the incomparable count is eventually finite and constant. Vertex-count height has the form \(H_N=N-D_0\) eventually for a finite nonnegative integer \(D_0\), because adjoining one maximal vertex changes vertex-count height by zero or one, and each later full birth raises it by one. A proper birth need not increase the deficit.

An explicit schedule available for every chosen \(L\) is
\[
 \epsilon_n^{(L)}=2^{L-1-n}\quad(n\ge L+1),
\]
with first value \(1/4\) and sum \(1/2\). This symbolic example fixes the shape of the post-onset tail; the uniform-discrimination failure below already follows just by allowing its onset \(L\) to vary.

## 4. Exact finite matching

Fix \(p\in(0,1)\) and a completed-birth horizon \(N\ge1\). Choose
\[
 L\ge\max\{5,N-1\}
\]
and take \(D_N=D(B_p|_{\le L},L,\epsilon^{(L)})\).
The subscript labels the choice made for this horizon; it does not assert that these choices form one common infinite law.

For any complete admissible marked growth history \(h\) through size \(N\), each transition has parent size \(0,\ldots,N-1\le L\). Its probability is the product of precisely the same \(q/2\) factors under \(D_N\) and \(B_p\). Therefore
\[
 \boxed{\mathcal L_{D_N}(H_{\le N})
        =\mathcal L_{B_p}(H_{\le N}).}
\]
Here \(H_{\le N}\) denotes the complete ordered growth history of ideals, retained orders and immutable marks, not Bernoulli's auxiliary generating-edge coordinates. For a common initial PSD payload, the associated scalar branch maps also agree through this prefix.

Terminal marked or unmarked orders are deterministic functions of that history, so their laws agree as well. For any common Markov observation kernel \(K_N(dy\mid h)\),
\[
 \int K_N(dy\mid h)\,d\Pr_{D_N}(h)
 =
 \int K_N(dy\mid h)\,d\Pr_{B_p}(h).
\]
This includes complete-order observation, a uniform induced-order sample of any allowed finite size, and common randomized postprocessing. It does not include a model-dependent side channel that reveals the hidden choice of law or future observations beyond the matched horizon.

The equality is exact, not merely overlapping support or a small TV estimate. Yet each fixed \(D_N\), once chosen and continued to infinity, has only finitely many proper births almost surely.

## 5. Uniform forced discrimination fails over the declared family

At each horizon use any one common observation kernel and a common randomized forced classifier. Let \(g_N(y)\in[0,1]\) be its probability of choosing Bernoulli, and define
\[
 e_B(N)=\mathbb E_{B_p}(1-g_N),\qquad
 e_D(N)=\mathbb E_D g_N.
\]
For the horizon-matching \(D_N\in\mathcal D_p^B\), exact observation equality gives
\[
 \boxed{e_B(N)+e_{D_N}(N)=1.}
\]
Consequently, at every finite horizon,
\[
 \boxed{e_B(N)+\sup_{D\in\mathcal D_p^B}e_D(N)\ge1.}
\]
The same obstruction holds for the larger \(\mathcal D\). In particular one cannot have both \(e_B(N)\to0\) and \(\sup_D e_D(N)\to0\); if the Bernoulli error tends to zero, the worst-case delayed-family error tends to one.

For the randomized minimax maximum of the two errors conditional only on the true law, with no selection or acceptance gate,
\[
 \inf_{g_N}\max\left\{e_B(N),\sup_{D\in\mathcal D_p^B}e_D(N)\right\}
 =\frac12.
\]
The lower bound follows from their sum being at least one. A common independent fair guess attains \(1/2\) for every law, proving equality. Equivalently the worst-rival equal-prior average cannot improve on \(1/2\). This is a forced-decision statement, not an abstention or selected-risk claim, and it makes no physical discrimination assertion.

These conclusions quantify over an explicitly enlarged class. They do not show that RI1407's exact parent-five fixed-prefix family can reproduce the Bernoulli prefix, or that the accepted fixed-law comparisons have equal finite distributions.

## 6. Pointwise limits and infinite histories remain different

For every fixed \(D=D(F,L,\epsilon)\), \(L\) is finite and its tail is summable. Its incomparable count is eventually finite almost surely. Bernoulli's incomparable count diverges almost surely: each disjoint consecutive-label pair is incomparable exactly when its own direct edge is absent, since no intermediate label is available. These absences are independent with probability 1-p>0. The probability of no absences among any next t pairs is p^t, tending to zero; taking the countable union over starting pairs shows infinitely many absences almost surely. Each such incomparability persists in the completed order. Hence the intrinsic measurable event
\[
 \left\{\sup_N I(P_N)<\infty\right\}
\]
has probabilities one and zero under \(D\) and \(B_p\). Their infinite retained-order-history laws remain singular. There is no one delayed law asserted to match Bernoulli through every finite horizon.

Here Q_N is one independent uniform k-subset without replacement, with the completed relation restricted to that subset and reported only up to unmarked isomorphism; C_k is the k-element chain type. Common N and k are design data. The same finite-prefix tail proof also gives, for a fixed delayed law, convergence of its sublinear uniform samples to the chain point mass: use any \(m\ge L+1\), then the fixed-\(m\) and tail limits proved explicitly in section 7. For reference, the admitted Bernoulli disjoint-pair estimate is
\[
 \Pr_{B_p}(Q_N=C_k)\le\min\{1,1/\mu_{N,k}\},\qquad
 \mu_{N,k}=(1-p)\lfloor N/2\rfloor\frac{k(k-1)}{N(N-1)},
 \quad N\ge4,\ 2\le k\le N.
\]
It follows from a witness Z with I(Q_N)>=Z, positive mean mu and variance at most mu; its overlapping sampling events are not assumed independent. For the delayed-law paired bounds use the stricter common cutoff N>=m>=L+1 (hence N>=6), 2<=k<=N. Together with this estimate, the chain/non-chain rule in the regime \(\sqrt N\ll k_N\ll N\) is pointwise consistent against each fixed delayed law. This is a direct extension of the tail argument, not reuse of old numerical coefficients.

The quantifiers differ:
\[
 \forall D,\quad e_D(N)\to0
 \quad\not\Rightarrow\quad
 \sup_D e_D(N)\to0.
\]
The matching choice \(D_N\) delays the change past the current horizon. It is not a counterexample in which a single fixed law violates its own asymptotic theorem. The previously accepted fixed-law and critical-scale results retain their original premises and scope.

## 7. One sufficient package for uniform use of the existing bounds

To apply the existing tail estimates uniformly over a restricted subfamily \(\mathcal F\subseteq\mathcal D\), one sufficient set of added controls is:

- A known finite bound \(L\le L_{\max}\) on retained-prefix lengths.
- A certified uniform tail envelope
\[
 R_{\mathcal F}(m):=
 \sup_{D\in\mathcal F}\sum_{n=m}^{\infty}\epsilon_n^D
 \longrightarrow0,\qquad m\ge L_{\max}+1.
\]

Then for common integers \(m\ge L_{\max}+1,\ N\ge m,\ 2\le k\le N\),
\[
 \sup_{D\in\mathcal F}\Pr_D(Q_N\ne C_k)
 \le\min\left\{1,R_{\mathcal F}(m)
             +\frac{\binom k2\binom m2}{\binom N2}\right\}.
\]
To prove this bound, the conditional proper-birth estimates and a union bound give probability at most the displayed tail for any proper birth at parent sizes m through N-1. If none occurs, every later vertex is above the old order and I(P_N)=I(P_m)<=binom(m,2). Each old incomparable pair is included in the uniform sample with probability binom(k,2)/binom(N,2). A union bound over those pairs controls nonchain probability on this event. Adding the exceptional-event bound, taking the supremum and capping the total at one gives the formula, without birth independence or terminal-count integrability.

For uniform convergence when k_N=o(N), first hold m fixed so the pair term vanishes, then let m grow so the certified common tail vanishes. Combining this with the fixed-p Bernoulli witness estimate, whose mean tends to infinity when k_N^2/N tends to infinity, yields uniform consistency when sqrt(N)<<k_N<<N. The same reasoning for a singleton family proves the pointwise claim in section 6. Complete-order cutoff bounds can likewise use this common certified tail.

Individual summability alone does not provide that common cutoff or uniform tail control. Conversely, no theorem is claimed that these two restrictions are necessary for every conceivable uniform method; they are a sufficient way to make the displayed estimates uniform. The unrestricted delayed Bernoulli-prefix family fails the finite-horizon separation requirement by exact matching, regardless of a chosen classifier.

## 8. Relationship to the accepted sample regimes and the next question

The anonymous sample Q_N means a single independent uniform k-subset without replacement, with the completed relation restricted to that subset and reported only up to unmarked isomorphism. Common N and k are design data; birth labels, subset identities, generating edges, marks and payload are not reported. This is neither an accumulating observation nor recomputation of reachability after deleting generating-graph vertices.

For the separately fixed admitted laws at their original scope, the accepted sample regimes remain: total variation tends to zero when k=o(sqrt(N)); the chain/nonchain rule is consistent when sqrt(N)<<k<<N; at k/sqrt(N)->c in (0,infinity), total variation has positive liminf and limsup below one and forced error sums have a positive asymptotic lower bound. Those fixed-law bounds are not uniform assertions over arbitrarily delayed rivals. No exact critical law, optimal constants or uniform parameter rate is asserted here. The complete critical proof is not required for the finite-prefix matching argument.

The new construction addresses an explicitly enlarged family. It does not place every Bernoulli-prefix extension inside the original parent-five fixed-prefix family, identify finite-history equality for every fixed pair, or assert that one delayed law matches Bernoulli at every horizon. The sufficient bounded-onset and common-tail controls above are not claimed necessary for all possible methods.

The next OPEN question is the optional condition that a uniform anonymous completed-order k-subset at size N should have the law of growth stopped at k. That condition must be distinguished from temporal prefix consistency and equivariant relabeling. Compatibility or finite counterexamples for the admitted Bernoulli and delayed-summable laws require their own independent work. No answer, successor theorem or new DET principle is adopted here.

## 9. Other lanes and process boundaries

E retains the accepted conditional finite-entry theorem and its accepted exact time-origin correction copy. With absolute entry time tau, controlled start t0, attempt start a and duration bound B, tau-a<=t0-a+B. This does not supply actual plant/initial/input/rate calibration, bounded sensing/update/lag/action or clock certificates. Nominal 60-second updates, step 60, step 44, horizon 64 and dwell W20 do not become interchangeable. Pre-entry ceilings, lower elapsed-time dwell bounds, physical reset/storage, full source-to-reset and failure costs, matched persistent 32-packet MHE resources and held-out reliability/quality/time/energy remain actual prerequisites. No new generic reduction or execution is admitted by this mathematical result.

NE retains its common actual pre-command source and independently justified transfer requirements. Candidate-indexed one-world guarantees do not establish counterfactual common-source equality. The accepted sum of source, calibration and target risks is an unconditional gate-and-error bound, not error conditional on acceptance. Physical source, reset/command transfer, control/readout, target sampling and clock/time/energy inputs remain absent; source costs must supplement 32*n_cal+2*N preparations/readouts.

CE retains the unresolved exact instantaneous resident-memory ceiling of 256 MiB before import for the selected process, together with CPU 10 s, wall 30 s, one process/no children, output 140 KiB, no network and failure/cleanup evidence. A footprint-triggered fatal policy differs from a no-overshoot resident-set guarantee. Installed-version applicability, entitlements and durable post-kill evidence remain unestablished. Bounded search is not universal impossibility and supplies no execution permission.

Measurement retains the missing applicable versioned selected-image/current-cache membership and safe-composition mechanism. No acquisition, replay, native call or nominal-calculation execution is supplied. The fixed 17-window rank interpretation requires justified null exchangeability and fixed-label/selection premises; conditional admission needs corresponding conditional symmetry. Its minimum unrandomized p-value is 1/17, above 5%, and zero comparison contrast still triggers the original abstention rule. Disjointness, stationarity or common filtering do not establish the null. No observed significance, physical calibration or native DET prediction is claimed.

The original RI1419 author recorded manuscript writing before its substantive cutoff, but its complete own-manuscript readback occurred at least 73 seconds after that cutoff. No complete-check-before-cutoff receipt or original process compliance is certified. A timely distinct review and current root full reading support the present conditional mathematical admission; they do not waive or backdate the author's failure. Declarations and write-start timestamps are not completed readback evidence. Current identities cannot reconstruct historical consumption or custody. Earlier timing/custody/guard-sequencing failures, RI1401 late-freeze, missing RI1389 evidence and helper limitations remain recorded.

This documentation preparation uses manual reasoning and new inert byte/JSON/archive work only. There is no scientific code execution, frozen-program import, release operation or physical experiment. No law selection, informative quantum/gravity result, native empirical prediction or DET application advantage follows. Protected validation and custody, Option B/Status M, operational ABSTAIN, zero qualification, shared supported 10% stop/reset conditions, existing schedules and the RET-only pause remain. Distinct publication review, root final acceptance and current repository/remote verification remain separate gates.
