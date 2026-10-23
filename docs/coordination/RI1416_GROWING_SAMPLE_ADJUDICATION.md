# RI1416: Growing-sample adjudication

This checkpoint consolidates the root-accepted RI1415 conditional theorem with its binding finite-domain clarification. For two separately fixed admitted growth laws, one anonymous uniform sample smaller than the square-root scale loses their distinction asymptotically, while an appropriate growing sublinear sample larger than that scale recovers consistent discrimination. These are sufficient regimes. The comparable-square-root regime remains open. No physical sampling implementation, unique DET law, empirical result or operational qualification follows.

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

    Pr_B(Q_N=C_k) <= h_(N,k)
      :=min(1, N(N-1)/[q floor(N/2) k(k-1)]),
    N>=4, 2<=k<=N.

This is an elementary second-moment argument, not a binomial approximation, numerical computation or independence assumption about sampled witnesses.

## 5. Recovery above the square-root scale while remaining sublinear

Use the intrinsic single-sample rule: choose B_p exactly when Q_N is not a chain; choose S_epsilon when it is a chain. Its paired finite error bounds have the common domain

    2<=k<=N, 6<=m<=N, all integers:
    e_S(N,k)<=s_(N,k,m),   e_B(N,k)<=h_(N,k).

This explicitly incorporates the binding domain clarification. The h formula alone also applies at N=4,5, where the supplied summable cutoff expression is unavailable and only the trivial e_S<=1 is supplied here. N=m gives an empty finite tail. k=N is allowed in the finite formulas but is outside the sublinear limit below. N<4 is outside the new witness bound.

Now suppose k_N/N->0 and k_N^2/N->infinity. The summable error tends to zero by the fixed-m tail argument. The second assumption implies k_N->infinity and

    mu=floor(N/2) q k_N(k_N-1)/[N(N-1)]
       ~q k_N^2/(2N) -> infinity.

Thus h_(N,k_N)->0 and the Bernoulli error also tends to zero. For example, k_N=floor(N^alpha) with separately fixed 1/2<alpha<1 meets both assumptions for all sufficiently large N. Constants depend on fixed p, and summable quantitative bounds depend on the specified tail.

The observable event “not a chain” gives

    TV(L_B(N,k_N),L_S(N,k_N))
      >=max(0, 1-e_B(N,k_N)-e_S(N,k_N)) -> 1.

This recovers statistical separation using only the anonymous order, not hidden proof witnesses. At every finite N>=k>=2 both errors of this particular rule remain strictly positive: a positive-probability all-empty-precursor history under S_epsilon gives an antichain, and a positive-probability all-full history under B_p gives a chain. Consistency is a limit, not perfect finite discrimination.

## 6. Open regime and unchanged physical limits

The conclusions bracket, but do not settle, k_N comparable to sqrt(N). No critical distribution, exact limiting error, exhaustive transition theorem, optimal classifier or optimal rate is established. A bound that does not vanish does not by itself prove impossibility. The next bounded question is what can be proved when k_N/sqrt(N)->c in (0,infinity), including whether nonzero distinguishability or unavoidable error can be established. No answer to that question is adopted here.

All results concern separately fixed optional laws. No endpoint or size-dependent p guarantee, uniform tail rate, universal DET law selection, informative quantum dynamics, spacetime/gravity prediction or empirical advantage follows. The fixed-k result remains a special small-sample case; complete-order finite discrimination and infinite-history separation retain their different observation scopes. Repeated, accumulated, adaptive, targeted, labeled, marked or payload-assisted observations are not analyzed. No physical sampling, clock, record-reconstruction or readout apparatus is provided.

## 7. Other lanes and process boundaries

E retains the accepted conditional finite-entry theorem and its accepted exact time-origin correction copy. With absolute entry time tau, controlled start t0, attempt start a and duration bound B, tau-a<=t0-a+B. This does not supply actual plant/initial/input/rate calibration, bounded sensing/update/lag/action or clock certificates. Nominal 60-second updates, step 60, step 44, horizon 64 and dwell W20 do not become interchangeable. Pre-entry ceilings, lower elapsed-time dwell bounds, physical reset/storage, full source-to-reset and failure costs, matched persistent 32-packet MHE resources and held-out reliability/quality/time/energy remain actual prerequisites. No new generic reduction or execution is admitted by this mathematical result.

NE retains its common actual pre-command source and independently justified transfer requirements. Candidate-indexed one-world guarantees do not establish counterfactual common-source equality. The accepted sum of source, calibration and target risks is an unconditional gate-and-error bound, not error conditional on acceptance. Physical source, reset/command transfer, control/readout, target sampling and clock/time/energy inputs remain absent; source costs must supplement 32*n_cal+2*N preparations/readouts.

CE retains the unresolved exact instantaneous resident-memory ceiling of 256 MiB before import for the selected process, together with CPU 10 s, wall 30 s, one process/no children, output 140 KiB, no network and failure/cleanup evidence. A footprint-triggered fatal policy differs from a no-overshoot resident-set guarantee. Installed-version applicability, entitlements and durable post-kill evidence remain unestablished. Bounded search is not universal impossibility and supplies no execution permission.

Measurement retains the missing applicable versioned selected-image/current-cache membership and safe-composition mechanism. No acquisition, replay, native call or nominal-calculation execution is supplied. The fixed 17-window rank interpretation requires justified null exchangeability and fixed-label/selection premises; conditional admission needs corresponding conditional symmetry. Its minimum unrandomized p-value is 1/17, above 5%, and zero comparison contrast still triggers the original abstention rule. Disjointness, stationarity or common filtering do not establish the null. No observed significance, physical calibration or native DET prediction is claimed.

The root accepted RI1415 after distinct manual review and actual current-source checks, with the paired-domain clarification stated above. Current author/reviewer completed-operation times are retained at their actual attributed scope; current hashes cannot reconstruct historical consumption or custody. Original author/first-review timing failures, the earlier checker-before-guard-inspection sequencing error and discrepant reset observation, RI1401 late-freeze, missing RI1389 evidence and historical helper limitations remain without waiver. Mathematical acceptance does not certify flawless historical process or operational readiness.

This package uses manual reasoning and new inert byte/JSON/archive preparation only. It does not execute scientific code, frozen programs or release operations. Protected-validation/custody requirements, Option B/Status M, operational ABSTAIN, zero production qualification, the shared supported 10% stop/reset conditions, existing schedules and the RET-only pause remain. Distinct publication review, root final acceptance and current repository/remote checks remain separate gates.
