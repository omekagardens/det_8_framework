# RI1418: Critical-sample adjudication

For two separately fixed admitted growth laws, one uniform anonymous sample of the completed order has three proved statistical regimes. Below the square-root scale their reported laws approach one another; above that scale while remaining sublinear a chain/nonchain rule is consistent. At a finite positive multiple of the square-root scale, total variation stays strictly between zero and one in the liminf/limsup sense: discrimination is nontrivial, but every forced rule has an unavoidable asymptotic error sum. The critical conclusion is the root-accepted RI1417 theorem after distinct review. The preceding two regimes retain their accepted finite domains and conditional premises.

This report gives the experiment and proofs together. None of these optional prescriptions is selected by bare DET. No physical readout, empirical finding, exact critical distribution, universal parameter guarantee or operational qualification follows.

## 1. Conditional laws and the observation

Let P_N be the completed retained order after N births, and I_N its number of unordered incomparable pairs. Births append maximal vertices whose strict past is an ideal; old relations persist. The admitted marked model also has immutable fair bits and scalar-passive payloads. These model features and the sufficient marked ratio characterization are conditional inputs, not derived here from bare DET.

Fix p in (0,1), put q=1-p, and retain the Bernoulli law B_p from the empty parent. Its independent forward-edge coordinates E_ij have Bernoulli(p) distributions for i<j, and P_N is their transitive closure. Reuse the admitted expectation bound

    E_B[I_N] <= q N/p^2.

Consecutive birth-label vertices are incomparable exactly when their direct edge is absent: a forward path has no intermediate integer label, and later vertices cannot create a path returning to an old endpoint. These labels and edges are proof auxiliaries, not observations.

Separately fix an admitted summable-allocation law S_epsilon, retaining its own positive prefix through parent size five and rebuilding subsequent transitions from that prefix. Its deterministic schedule satisfies 0<epsilon_n<1 and sum_(n>=6) epsilon_n<infinity. Its conditional admission, strict finite-history support and marked-ratio sufficiency remain premises. The property needed here is

    Pr_S(A_n | F_n) <= epsilon_n,   n>=6,

where A_n is a proper, non-full birth from parent size n and F_n contains its history. A full birth appends above every old vertex and creates no incomparable pair. B_p is not spliced onto the S_epsilon prefix; the laws have separate complete prescriptions and need no coupling.

At each design size N, choose a predetermined integer k=k_N with 2<=k<=N. Select one uniform k-element subset U without replacement, using sampling randomness independent of growth. Report only Q_N=P_N[U], the restriction of the completed order to U, up to unmarked isomorphism. N and k are common fixed design data. No birth labels, vertex/subset identifiers, generating edges, marks or payload are supplied. Restricting the completed relation preserves comparisons mediated by unsampled vertices; deleting vertices from a generating graph and recomputing reachability would be a different experiment.

There is one sample at each fixed N, not an accumulating sequence of observations. The theorem compares the two reported laws on their common finite space at that N; those finite spaces may vary with N.

## 2. Pair counting and the summable tail split

A given unordered pair occurs in binom(N-2,k-2) of the binom(N,k) subsets. Thus, for every integer 2<=k<=N, including k=N,

    c_(N,k) = binom(k,2)/binom(N,2) = k(k-1)/[N(N-1)],
    E[I(Q_N) | P_N] = c_(N,k) I_N.

Linearity requires no independence among sampled pairs or among general incomparable pairs in the source. Write C_k for the unique unmarked chain type. Since an order is a chain exactly when it has no incomparable pair,

    Pr(Q_N != C_k | P_N) <= min(1, c_(N,k) I_N).

For common integers 2<=k<=N and 6<=m<=N, define

    K_m=binom(m,2),
    r_(m,N)=sum_(n=m)^(N-1) epsilon_n,
    R_m=sum_(n=m)^infinity epsilon_n.

The finite sum is empty when N=m. If no proper birth occurs from parent m through parent N-1, all appended vertices are above the old order, so I_N=I(P_m)<=K_m. Taking expectations of the conditional birth bounds and using a union bound gives Pr_S(I_N>K_m)<=r_(m,N). Splitting the sampling estimate on this exceptional event yields

    a_S(N,k):=Pr_S(Q_N != C_k)
      <= s_(N,k,m):=min(1, r_(m,N)+c_(N,k) K_m)
      <= min(1, R_m+c_(N,k) K_m).

The probability cap applies to the total upper bound. Neither independent births nor an integrable eventual incomparable count is assumed. A certified bound on R_m can replace that tail for quantitative use; abstract summability alone is not an effective uniform cutoff procedure.

If k_N=o(N), then c_(N,k_N)K_m tends to zero for every fixed m. First fix m and let N tend to infinity, obtaining limsup a_S<=R_m; only then let m grow. Summability proves a_S(N,k_N)->0 throughout this sublinear regime. This is convergence for each fixed prescription, not a uniform rate over arbitrary schedules.

## 3. Obstruction below the square-root scale

The Bernoulli expectation bound and the same pair-counting identity imply, for 2<=k<=N,

    a_B(N,k):=Pr_B(Q_N != C_k)
      <= b_(N,k):=min(1, k(k-1)q/[p^2(N-1)]).

Write L_B(N,k) and L_S(N,k) for the reported isomorphism-type distributions. Use TV(L,M)=sup_A |L(A)-M(A)|=(1/2)sum_x |L(x)-M(x)|. Distance to the point mass at C_k equals the exact nonchain probability. Thus, on the common finite domain 2<=k<=N and 6<=m<=N,

    TV(L_B(N,k),L_S(N,k)) <= min(1, b_(N,k)+s_(N,k,m)).

When k_N=o(sqrt(N)), b_(N,k_N)->0 and also k_N=o(N), so the summable result applies. Both distances to the moving chain point mass vanish, and TV between the two observed laws tends to zero. This uses same-N comparisons, not a presumed common space or coupling across all sample sizes.

For a common randomized forced rule, let g(x) in [0,1] be the probability of choosing B_p on reported type x. Its errors are e_S=E_S[g] and e_B=E_B[1-g], so e_S+e_B=1-(E_B[g]-E_S[g]). The signed difference of two probability masses has total zero, and its positive part has mass TV. Bounding the g-weighted difference and reversing signs gives

    |e_S+e_B-1| <= TV(L_B,L_S).

Consequently every sequence of such rules, including N-dependent rules, has error sum tending to one in the small-sample regime. Both errors cannot tend to zero. Only under equal priors is their half-sum average error; constant guessing attains average one half, so the optimal equal-prior average tends to one half. There is no separate one-half lower bound on each error. Abstention, rare-report conditioning and selection-conditioned risk are different experiments and are not covered.

## 4. A Bernoulli chain bound from disjoint proof pairs

For the following bound alone assume N>=4 and 2<=k<=N. Set M=floor(N/2) and use the disjoint consecutive-label pairs D_j={2j-1,2j}, j=1,...,M. In the Bernoulli realization define

    X_j=1-E_(2j-1,2j),
    V_j=1{D_j subset U},
    W_j=X_j V_j,   Z=sum_j W_j.

The X_j are independent Bernoulli(q). Choose U uniformly from the deterministic carrier [N], independently of all generating coordinates and bits. Conditional on the completed order this realizes exactly the stipulated sampling kernel. It is an auxiliary realization of one law, not a coupling of the competing laws. A selected pair with X_j=1 is an incomparable pair in the completed induced order, so I(Q_N)>=Z. The rule never accesses these labels or hidden variables.

Direct subset counting gives the pair-inclusion probability

    a = k(k-1)/[N(N-1)].

For distinct i,j their pairs have four different vertices. Their joint inclusion probability is

    d = 0                         when k=2 or 3,
    d = k(k-1)(k-2)(k-3)/[N(N-1)(N-2)(N-3)] when k>=4.

Independence of these inclusion events is not assumed. For k>=4, k<=N implies

    (k-2)/(N-2) <= k/N,
    (k-3)/(N-3) <= (k-1)/(N-1).

Multiplication gives d/a<=a, hence d<=a^2; for k=2,3 this is immediate. The equality at k=N causes no problem. Independence of sampling from edge coordinates, and independence of distinct edge coordinates, therefore give

    E[W_j]=qa,
    E[W_i W_j]=q^2 d,
    Cov(W_i,W_j)=q^2(d-a^2)<=0.

It follows that

    mu:=E[Z]=Mqa>0,
    Var(Z)=Mqa(1-qa)+M(M-1)q^2(d-a^2)<=mu.

Nonpositive pair covariances suffice; the W_j are not asserted independent. On Z=0 the squared deviation from mu equals mu^2, so Var(Z)>=mu^2 Pr(Z=0). A chain sample forces Z=0. Thus the finite Bernoulli bound is

    Pr_B(Q_N=C_k) <= H_(N,k)
      :=min(1, N(N-1)/[q floor(N/2) k(k-1)]),
    N>=4, 2<=k<=N.

This is an elementary second-moment argument, not a binomial approximation, numerical computation or independence assumption about sampled witnesses.

## 5. Recovery above the square-root scale while remaining sublinear

Use the intrinsic single-sample rule: choose B_p exactly when Q_N is not a chain; choose S_epsilon when it is a chain. Its paired finite error bounds have the common domain

    2<=k<=N, 6<=m<=N, all integers:
    e_S(N,k)<=s_(N,k,m),   e_B(N,k)<=H_(N,k).

This explicitly incorporates the binding domain clarification. The H formula alone also applies at N=4,5, where the supplied summable cutoff expression is unavailable and only the trivial e_S<=1 is supplied here. N=m gives an empty finite tail. k=N is allowed in the finite formulas but is outside the sublinear limit below. N<4 is outside the new witness bound.

Now suppose k_N/N->0 and k_N^2/N->infinity. The summable error tends to zero by the fixed-m tail argument. The second assumption implies k_N->infinity and

    mu=floor(N/2) q k_N(k_N-1)/[N(N-1)]
       ~q k_N^2/(2N) -> infinity.

Thus H_(N,k_N)->0 and the Bernoulli error also tends to zero. For example, k_N=floor(N^alpha) with separately fixed 1/2<alpha<1 meets both assumptions for all sufficiently large N. Constants depend on fixed p, and summable quantitative bounds depend on the specified tail.

The observable event “not a chain” gives

    TV(L_B(N,k_N),L_S(N,k_N))
      >=max(0, 1-e_B(N,k_N)-e_S(N,k_N)) -> 1.

This recovers statistical separation using only the anonymous order, not hidden proof witnesses. At every finite N>=k>=2 both errors of this particular rule remain strictly positive: a positive-probability all-empty-precursor history under S_epsilon gives an antichain, and a positive-probability all-full history under B_p gives a chain. Consistency is a limit, not perfect finite discrimination.

At the critical scale, separately fix a constant c in (0,infinity) and a predetermined integer sequence k_N/sqrt(N)->c. Keep p and the entire summable prescription fixed as N grows. Set r=1-p^2 and lambda=qc^2/2. The positive finite constant lambda is the limit of the witness mean mu. The integer spacing parameter h used below is distinct from the Bernoulli bound H_(N,k) above.

## 6. A positive lower bound on Bernoulli non-chain probability

Cauchy–Schwarz applied to \(Z\mathbf1_{\{Z>0\}}\) gives
\[
 \mu^2=(\mathbb E[Z\mathbf1_{\{Z>0\}}])^2
 \le \mathbb E[Z^2]\Pr(Z>0)
 \le(\mu^2+\mu)\Pr(Z>0).
\]
Thus the inherited second moment gives the sharper finite bound
\[
 \boxed{a_B(N,k)\ge\Pr(Z>0)\ge\frac{\mu}{1+\mu},\qquad
        \Pr_B(Q_N=C_k)\le\frac1{1+\mu}.}
\]
This is a direct moment inequality, not a Poisson or binomial approximation. At critical scaling \(\mu\to\lambda=qc^2/2>0\). It proves a positive non-chain probability, but alone does not establish unavoidable error. For that we next prove a positive chain probability.

## 7. A finite pair bound from the admitted product edges

Use birth labels only as proof auxiliaries. For \(i<j\), put \(d=j-i\). If these vertices are incomparable, their direct edge is absent and none of the two-edge paths \(i\to\ell\to j\), \(i<\ell<j\), exists. The direct-edge coordinate and the two-coordinate sets for distinct intermediate \(\ell\) are disjoint. Independence of those edge coordinates in the admitted product realization therefore yields
\[
 \boxed{\Pr_B(i\parallel j)\le q(1-p^2)^{d-1}=qr^{d-1}.}
\]
Longer paths can only reduce the incomparability probability. This derives the needed estimate from the allowed product-edge premise; it does not reconstruct or claim novelty for the law. It asserts no independence between different pair-incomparability events.

## 8. A positive finite chain bound using a spacing event

Fix an integer \(h\ge0\), and suppose
\[
 N'=N-h(k-1)\ge k\ge2.
\]
Order the sampled auxiliary labels \(x_1<\cdots<x_k\). Let \(G_h\) be the event
\(x_{i+1}-x_i\ge h+1\) for every consecutive sampled pair. The map
\[
 y_i=x_i-h(i-1)
\]
is a bijection from such samples to the \(k\)-subsets of \([N']\). Hence
\[
 \rho_{N,k,h}:=\Pr(G_h)=\frac{\binom{N'}k}{\binom Nk},
\]
and, conditional on \(G_h\), \(\{y_i\}\) is a uniform \(k\)-subset of \([N']\).

We may realize the stipulated sample independently of all Bernoulli edges. Conditioning on the sampling-only event \(G_h\) consequently leaves those edge probabilities unchanged. If all consecutive sampled vertices are comparable, forward orientation and transitivity make the entire sample a chain. For a fixed sample the union bound and section 7 give
\[
 \Pr_B(Q_N\ne C_k\mid U)
 \le \sum_{i=1}^{k-1}qr^{x_{i+1}-x_i-1}.
\]
On \(G_h\), each summand is
\(qr^h r^{y_{i+1}-y_i-1}\).
Bound this consecutive-pair sum by the sum over all unordered sampled \(y\)-pairs, whose terms are nonnegative. Each pair in \([N']\) is included with probability \(k(k-1)/[N'(N'-1)]\). Therefore
\[
 \begin{aligned}
 \Pr_B(Q_N\ne C_k\mid G_h)
 &\le qr^h\frac{k(k-1)}{N'(N'-1)}
       \sum_{d=1}^{N'-1}(N'-d)r^{d-1}\\
 &\le A_{N,k,h}:=
       \frac{qr^h k(k-1)}{p^2(N'-1)}.
 \end{aligned}
\]
The last step uses
\(\sum_{d\ge1}r^{d-1}=1/(1-r)=1/p^2\).
No independence between consecutive comparability events was used: this is a union bound and linearity of expectation.

Writing \([t]_+=\max\{t,0\}\), we have the finite bound
\[
 \boxed{
 \Pr_B(Q_N=C_k)\ge
 g_{N,k,h}:=\rho_{N,k,h}[1-A_{N,k,h}]_+.}
\]
The spacing event, compressed coordinates and conditioning are internal proof devices only. The actual experiment still uses every uniform sample, reports no identifiers, and performs no postselection. The result is an unconditional chain-probability bound.

## 9. Critical asymptotics of the auxiliary spacing bound

Keep \(h\) fixed and take \(k=k_N\sim c\sqrt N\). The domain \(N'\ge k\) eventually holds, \(N'/N\to1\), and
\[
 A_{N,k,h}\to Ar^h,\qquad A=qc^2/p^2.
\]
For completeness, the subset ratio has the limit
\[
 \rho_{N,k,h}
 =\prod_{j=0}^{k-1}
   \left(1-\frac{h(k-1)}{N-j}\right)
 \longrightarrow e^{-hc^2}.
\]
To justify it directly, put \(z_j=h(k-1)/(N-j)\). Their maximum tends to zero,
\(\sum_jz_j\to hc^2\), and
\(\sum_jz_j^2=O(k^3/N^2)\to0\).
The elementary bound
\[
 |\log(1-z)+z|\le z^2/(1-z)\quad(0\le z<1)
\]
follows by integrating \(t/(1-t)\) from zero to \(z\). Applying it termwise gives the stated limit. The case \(h=0\) has \(\rho=1\) identically.

Choose a fixed integer \(h\ge0\) so that \(Ar^h<1\). Then
\[
 g_{N,k_N,h}\longrightarrow
 \gamma=e^{-hc^2}(1-Ar^h)>0,
\]
and therefore
\[
 \liminf_{N\to\infty}\Pr_B(Q_N=C_{k_N})\ge\gamma.
\]
This is a limit of an auxiliary combinatorial bound, not an exact critical distribution for \(Q_N\). The constant may be very small; positivity, not optimality, is what rules out consistency.

## 10. TV and forced-decision consequences

At each \(N\), define
\[
 \Delta_N=d_{\rm TV}(L^B_{N,k},L^S_{N,k}),\qquad
 d_{\rm TV}(L,M)=\sup_A|L(A)-M(A)|
               =\tfrac12\sum_x|L(x)-M(x)|.
\]
Since TV to the chain point mass is the non-chain probability, the triangle and reverse triangle inequalities give
\[
 |\Delta_N-a_B(N,k)|\le a_S(N,k).
\]
Combining Sections 2, 6–8 yields the explicit finite sandwich
\[
 \boxed{
 \max\left\{0,\frac{\mu}{1+\mu}-s_{N,k,m}\right\}
 \le\Delta_N
 \le\min\{1,1-g_{N,k,h}+s_{N,k,m}\}.}
\]
Its common domain is
\(6\le m\le N,\ 2\le k\le N,\ N-h(k-1)\ge k\), with fixed integer \(h\ge0\).
The predecessor's Bernoulli-only domain is not silently transferred to the summable bound.

At critical scaling, \(a_S\to0\), \(\mu\to\lambda\), and \(g\to\gamma\). This proves the strict asymptotic bounds stated below.

For any common randomized forced binary rule choosing Bernoulli with probability \(f(x)\), the errors obey
\[
 e_S+e_B=1+\mathbb E_S f-\mathbb E_B f\ge1-\Delta_N.
\]
Indeed, \(0\le f\le1\) bounds the signed difference by the positive mass of \(L^B-L^S\), which equals TV. Thus
\[
 \liminf(e_S+e_B)\ge\gamma>0.
\]
Neither error separately has this lower bound; it is their sum. No rule on this observation can have both errors vanish.

For equal priors, minimizing that sum over finite-alphabet rules gives
\[
 R_N^*=\tfrac12(1-\Delta_N).
\]
The lower bound is attained by choosing Bernoulli on the positive part of \(L^B-L^S\), so this identity requires no external testing theorem. It is a mathematical optimum, not an implemented likelihood calculation. It gives the bounds below without asserting a limit.

The simpler observable chain/non-chain rule also shows nontrivial discrimination: its summable error tends to zero, while its Bernoulli error obeys
\[
 g_{N,k,h}\le e_B(N)=\Pr_B(Q_N=C_k)\le\frac1{1+\mu}.
\]
Consequently its limiting upper average error is below \(1/2\), but its Bernoulli error remains bounded away from zero. Labels, edge bits and spacing events are not inputs to this rule.

## 11. Critical theorem, remaining question and physical limits

Put A=qc^2/p^2 and choose any fixed integer h>=0 with A r^h<1; one exists because 0<r<1. Define

    gamma=exp(-h c^2)(1-A r^h)>0.

For the single-sample reported laws and the optimal equal-prior average error, the preceding proofs establish

    0 < lambda/(1+lambda)
      <= liminf Delta_N <= limsup Delta_N <= 1-gamma < 1,

    0 < gamma/2
      <= liminf R_N^* <= limsup R_N^*
      <= 1/[2(1+lambda)] < 1/2.

Every sequence of common randomized forced rules has liminf(e_S+e_B)>=gamma. This is a bound on the sum, not on each separate error. The chain/nonchain rule has e_S->0 and gamma<=liminf e_B<=limsup e_B<=1/(1+lambda). These are bounds, not exact critical distributions, convergence assertions or optimal constants. The mathematical likelihood optimum does not constitute an implemented classifier.

The finite critical sandwich requires integers 6<=m<=N, 2<=k<=N, h>=0 and N-h(k-1)>=k. The witness inequalities alone allow N>=4. At N=m the finite tail is empty; at k=N spacing permits only h=0. The asymptotics keep m and h fixed before taking their stated limits. Endpoints p=0,1 and c=0,infinity, or size-dependent p, are excluded from this critical theorem. Quantitative summable rates require a certified tail; no terminal-count integrability or uniform schedule rate is assumed.

Positive finite-history support prevents perfect finite forced discrimination. For the chain/nonchain rule both finite errors are strictly positive, as shown above. That support fact alone does not prove the critical asymptotic error floor; the unconditional positive chain-probability bound is essential. The spacing event, birth labels and compressed coordinates are proof devices, not reported data or observational postselection.

The next question is whether an arbitrary admitted positive finite prefix, including a Bernoulli prefix, can be retained and followed by rebuilt summable layers, and what uniform discrimination means for an explicitly declared delayed-summable family. Such an expanded family must be distinguished from the specific admitted schedule family, and a fixed law from horizon-dependent adversarial choices. This remains an OPEN question; no finite-prefix extension or law-uniformity successor theorem is adopted here.

All results concern separately fixed optional prescriptions. No informative quantum dynamics, spacetime/gravity prediction, DET advantage or law-selection principle follows. Repeated, accumulated, adaptive, targeted, labeled, marked or payload-assisted observations and selection-conditioned risk are outside this experiment. No physical sampling, clock, record-reconstruction or readout apparatus is supplied.

## 12. Other lanes and process boundaries

E retains the accepted conditional finite-entry theorem and its accepted exact time-origin correction copy. With absolute entry time tau, controlled start t0, attempt start a and duration bound B, tau-a<=t0-a+B. This does not supply actual plant/initial/input/rate calibration, bounded sensing/update/lag/action or clock certificates. Nominal 60-second updates, step 60, step 44, horizon 64 and dwell W20 do not become interchangeable. Pre-entry ceilings, lower elapsed-time dwell bounds, physical reset/storage, full source-to-reset and failure costs, matched persistent 32-packet MHE resources and held-out reliability/quality/time/energy remain actual prerequisites. No new generic reduction or execution is admitted by this mathematical result.

NE retains its common actual pre-command source and independently justified transfer requirements. Candidate-indexed one-world guarantees do not establish counterfactual common-source equality. The accepted sum of source, calibration and target risks is an unconditional gate-and-error bound, not error conditional on acceptance. Physical source, reset/command transfer, control/readout, target sampling and clock/time/energy inputs remain absent; source costs must supplement 32*n_cal+2*N preparations/readouts.

CE retains the unresolved exact instantaneous resident-memory ceiling of 256 MiB before import for the selected process, together with CPU 10 s, wall 30 s, one process/no children, output 140 KiB, no network and failure/cleanup evidence. A footprint-triggered fatal policy differs from a no-overshoot resident-set guarantee. Installed-version applicability, entitlements and durable post-kill evidence remain unestablished. Bounded search is not universal impossibility and supplies no execution permission.

Measurement retains the missing applicable versioned selected-image/current-cache membership and safe-composition mechanism. No acquisition, replay, native call or nominal-calculation execution is supplied. The fixed 17-window rank interpretation requires justified null exchangeability and fixed-label/selection premises; conditional admission needs corresponding conditional symmetry. Its minimum unrandomized p-value is 1/17, above 5%, and zero comparison contrast still triggers the original abstention rule. Disjointness, stationarity or common filtering do not establish the null. No observed significance, physical calibration or native DET prediction is claimed.

The root accepted RI1417 after distinct manual proof review and current-source checks, retaining the prior paired-domain clarification. The scientific review stopped on a reset discrepancy and reconciled it using a supported same-account advanced corresponding reset within its original deadlines. Its declarations, recorded author observations and source-consumption history retain their attributed scope. Current hashes do not reconstruct historical consumption or custody. Original author/first-review timing failures, the earlier checker-before-guard-inspection sequencing error, RI1401 late-freeze, missing RI1389 evidence and historical helper limitations remain without waiver. Mathematical acceptance does not certify flawless historical process or operational readiness.

This package uses manual reasoning and new inert byte/JSON/archive preparation only. It does not execute scientific code, frozen programs or release operations. Protected-validation/custody requirements, Option B/Status M, operational ABSTAIN, zero production qualification, the shared supported 10% stop/reset conditions, existing schedules and the RET-only pause remain. Distinct publication review, root final acceptance and current repository/remote checks remain separate gates.
