# RI1414: Sampled-readout adjudication

This checkpoint concerns a conditional mathematical observation channel for two separately stipulated growth laws. A single uniform sample of a fixed number of vertices loses their complete-order distinction asymptotically: both observed order distributions approach the same chain. Explicit finite bounds quantify the resulting forced-testing limitation. This does not identify a physically correct law or supply a physical readout.

## 1. Laws, retained objects and the exact experiment

At size N, P_N is the completed retained finite order, and I_N counts its unordered incomparable pairs. A birth adds a new maximal vertex whose strict past is an ideal of the existing order; old relations persist. Immutable marks and scalar-passive payloads belong to the admitted construction but are not reported by this experiment.

The Bernoulli law B_p is fixed from the empty parent, with p in (0,1) and q=1-p. Its forward-edge realization has independent Bernoulli(p) coordinates E_ij for i<j; P_N is their transitive closure. The accepted bound used here is E_B[I_N] <= q N/p^2. Consecutive-label absent edges also witness I_N >= sum_(i=1)^(N-1)(1-E_(i,i+1)), but those labels and edges are proof auxiliaries, not observations. Complete marked admission and the expectation bound remain inherited premises.

Separately fix one admitted summable-allocation law S_epsilon. It preserves its own positive prefix through parent size five and rebuilds all subsequent transitions using a fixed deterministic schedule 0<epsilon_n<1 with sum_(n>=6) epsilon_n finite. Its permitted common proper-ideal scale at size n is epsilon_n/(1+M_n), where M_n is the maximum complete proper deletion-potential load over all marked n-parents. The underlying marked ratio-potential sufficiency theorem and the admitted seed remain conditional premises. This is an optional law choice, not a coordinate change or a law forced by DET. In particular B_p is not spliced onto this seed.

The specific inherited property needed below is Pr_S(A_n | F_n) <= epsilon_n, where A_n is a proper birth from parent size n and F_n contains its history. A full birth lies above every old vertex and creates no new incomparable pair. The two measures need not share a probability space or a coupling.

Fix integer k>=2 and known design size N>=k. Independently of growth, choose one uniform k-element subset U of the N vertices, without replacement. Report only Q=P_N[U], the restriction of the completed order to U, up to unmarked order isomorphism. Do not report vertex or subset identities, birth labels, marks, generating edges or payload. Restricting the completed relation differs from deleting vertices of a generating graph and then recomputing reachability. N and k are common fixed design data under both hypotheses.

Let L_B and L_S be the resulting distributions on the finite set of unmarked k-order types, and C_k its unique chain type. This is a stipulated mathematical observation kernel. No device, sampling implementation, physical clock or measurement cost is established.

## 2. Exact pair inclusion and finite chain bounds

For any fixed completed order, each unordered vertex pair occurs in exactly binom(N-2,k-2) of its binom(N,k) uniform subsets. Thus its inclusion probability is

    c_(N,k) = binom(k,2)/binom(N,2) = k(k-1)/(N(N-1)).

Linearity gives the exact identity

    E[I(Q) | P_N] = c_(N,k) I_N.

Neither sampled-pair indicators nor general source incomparable-pair indicators must be independent. The identity includes k=N. An order is a chain exactly when it has zero incomparable pairs; hence

    Pr(Q != C_k | P_N) <= min(1, c_(N,k) I_N).

Use total variation TV(L,M)=sup_A |L(A)-M(A)|=(1/2)sum_x |L(x)-M(x)|. Its distance to the chain point mass is exactly Pr(Q != C_k). Denote these distances by a_B and a_S. Averaging and using the inherited Bernoulli expectation bound yields

    a_B <= b_(N,k) := min(1, k(k-1)q/[p^2(N-1)]).

For the summable law choose an integer m with 6<=m<=N, still N>=k, and write

    K_m = binom(m,2),
    r_(m,N) = sum_(n=m)^(N-1) epsilon_n,
    R_m = sum_(n=m)^infinity epsilon_n.

If no proper birth occurs from parent m through parent N-1, every appended vertex lies above the old order and I_N=I(P_m)<=K_m. Taking expectations of the conditional proper-birth bounds and using a union bound gives Pr_S(I_N>K_m)<=r_(m,N). Splitting the sampling bound on this event gives

    a_S <= s_(N,k,m) := min(1, r_(m,N) + c_(N,k) K_m)
        <= min(1, R_m + c_(N,k) K_m).

The finite sum is empty at N=m. The cutoff bound is asserted only on its stated integer domain; a_S<=1 remains available otherwise. The quantities b and s are sufficient upper bounds, not exact probabilities. No independence of births or integrability of the eventual incomparable count is assumed.

For the already stipulated geometric schedule epsilon_n=2^(4-n), the symbolic sums are R_m=2^(5-m) and r_(m,N)=2^(5-m)(1-2^(m-N)). A quantitative cutoff for another schedule requires its own known or certified tail bound; abstract summability does not provide an effective numerical procedure.

## 3. Loss of distinction and forced testing

Fix p, k and the entire summable prescription separately. The Bernoulli bound tends to zero as N grows. For each fixed m the factor c_(N,k)K_m tends to zero, so limsup_N a_S<=R_m. Only then let m tend to infinity; summability makes R_m vanish. Both observed distributions therefore approach the same chain point mass in total variation. This order of limits avoids assuming a finite expected terminal incomparable count.

The triangle inequality gives, on the finite cutoff domain,

    TV(L_B,L_S) <= eta_(N,k,m) := min(1, b_(N,k)+s_(N,k,m)),
    TV(L_B,L_S) -> 0 as N -> infinity for fixed k and fixed laws.

A common randomized forced rule chooses Bernoulli with probability g(x) in [0,1] after the reported type x. Its two conditional errors are e_S=E_S[g] and e_B=E_B[1-g]. Thus e_S+e_B=1-(E_B[g]-E_S[g]). For d_x=L_B(x)-L_S(x), sum_x d_x=0; maximizing sum_x g(x)d_x over 0<=g<=1 selects its positive masses, whose sum is TV. Reversing signs bounds the negative difference. Consequently

    |e_S+e_B-1| <= TV(L_B,L_S),
    e_S+e_B >= 1-eta_(N,k,m).

The error sum approaches one even for N-dependent rules in this fixed-k experiment. Under equal prior probabilities, average error is half this sum, so it is at least (1-eta)/2. A constant guess achieves average error 1/2; the optimal equal-prior average therefore tends to 1/2. This is not a lower bound of 1/2 on each error: always choosing S gives e_S=0 and e_B=1.

No abstention, selected-outcome conditional risk, different-prior benchmark or conditional-on-report guarantee is inferred. Conditioning on a rare selection event changes the observed law and requires its own premises.

## 4. What the obstruction leaves open

The accepted complete-order result RI1411 uses I_N at a deliberately chosen finite horizon and can make each error positive but at most a prescribed tolerance. The accepted infinite-history result RI1409 separates eventual finite count under S_epsilon from divergent count under B_p. Losing those distinctions after this specified information reduction is compatible with both results: vanishing quadratic incomparable density does not imply a finite total count.

The present theorem addresses one fixed-k sample at each design size. It does not assert identical finite-N distributions, equality of the full laws, an exact or optimal rate, a parameter-uniform rate, or an almost-sure result for a coupled sequence of samples. It does not analyze an accumulating observation history, repeated, adaptive or targeted samples, growing k, or supplied identifiers, marks and payloads.

The next bounded question is whether a single growing but sublinear anonymous uniform sample can recover consistent discrimination, and what justified sample-size regimes permit or obstruct it. This is a question, not an accepted answer, optimality assertion or permission to implement a physical readout. Birth-label witnesses may support a proof but cannot become undeclared data for the rule.

## 5. Coordinator disposition, provenance and the other lanes

The coordinator accepts the conditional theorem above after its own manual proof assessment, actual source checks and a fresh distinct independent review completed within its original prospective budget. The original RI1413 author recorded a check-summary observation after its fixed substantive cutoff and reported its completed freeze readback after its deadline. Its first distinct reviewer also recorded a late substantive completion observation. Those historical failures remain unchanged. The fresh review supports present mathematical acceptance without certifying prior timeliness, reconstructing missing custody or extending an expired budget. It also records an inert checker dispatched before inspection of a discrepant usage-reset field; work stopped, a new supported response restored the assigned observation, and checks were rerun after inspection within the unchanged budget. That sequencing failure remains recorded; no usage-threshold reset or capacity exception was inferred.

Earlier RI1401 late-freeze, missing original RI1389 evidence and inherited helper/timing limitations persist. Current hashes establish current identities only. Manual proof and inert byte/JSON/archive checks are distinct from scientific execution. No numerical growth experiment or new coefficient audit supports this theorem.

The thermal-control lane's E-C016 theorem with the binding absolute-time correction and exact E-C016-C1 clean copy were accepted in RI1412. If tau is absolute entry time, t0 the controlled initial time, a the actual attempt start and B the conditional duration bound, tau-a<=t0-a+B. This correction supplies no calibrated physical plant, sensing/update/lag/action/clock certificate, full source-to-reset costs or held-out benchmark. This bounded theorem and repair remain closed pending those actual inputs.

The energy lane retains its actual common physical source, transfer, control/readout and time/energy/resource prerequisites. Computing retains the unresolved exact pre-import strict resident-memory bound of 256 MiB together with its other fixed execution limits; termination after crossing a memory threshold does not prove no overshoot. Measurement retains the missing applicable versioned selected-image/current-cache membership and safe-composition input. Its fixed 17-window rank interpretation requires its null and selection assumptions, has minimum p-value 1/17 above 5%, and supplies no observed significance or native DET prediction.

All protected-validation and custody requirements, Option B/Status M, operational ABSTAIN, zero production qualification, the RET-only pause and shared supported 10% usage stop/reset conditions remain. Existing schedules and notification preferences remain unchanged. No result in one lane validates another lane's assumptions or the physical theory.
