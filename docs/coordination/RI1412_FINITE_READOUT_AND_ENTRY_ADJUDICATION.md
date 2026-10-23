# RI1412 — Finite readout and entry adjudication

This checkpoint consolidates the root-accepted RI1411 finite intrinsic classifier and E-C016 conditional finite-entry theorem following distinct scientific review. The E result is accepted together with the binding time-origin correction stated below; the original frozen source remains preserved. The previously accepted rank interpretation and NE, CE and measurement blockers are carried unchanged. All results are conditional mathematical or documentary claims. No physical law selection, readout device, actual controller/deadline admission, observed significance, measured advantage or scientific execution is supplied. This publication package remains subject to distinct review and root acceptance.

## 1. QR: a finite intrinsic classifier for two fixed optional laws

### Models and observation premise

A retained order P_N records the vertices and order relations after N births. A birth adds a maximal vertex whose strict past S is an ideal, meaning a downward-closed subset of its parent P. Newborn immutable binary marks are fair; the complete branch map multiplies an arbitrary complex positive-semidefinite payload by Q(P,r,S)/2, with r the existing marks. All ideals remain eligible. Marked equivariance, proper-precursor mark locality and complete incomparable-birth diamonds are admitted conditional model premises, not derived here from bare DET.

For a fixed p in (0,1), the admitted Bernoulli law B_p begins from empty with independent forward edges E_ij distributed as Bernoulli(p), 1<=i<j, and independent fair newborn bits. P_N is the transitive closure of those forward edges on labels 1,...,N. The individual-ideal probability is

    Q_p(P,r,S)=p^(|Max(S)|) (1-p)^(|P|-|S|).

Separately fix one summable law S_epsilon with its own positive admitted prefix through parent size five. Choose deterministic 0<epsilon_n<1 with sum_(n>=6) epsilon_n finite. Its later layers are rebuilt from the changed smaller-size prefix in a fixed deletion-potential convention. For each proper S, put J=Max(P)\S and

    u_n(P,r,S)=product over nonempty A subset J of
              Q(P\A,r restricted to P\A,S)^((-1)^(|A|+1)),
    K_n(P,r)=sum over all proper ideal occurrences S of u_n(P,r,S),
    M_n=max over all marked n-parents of K_n(P,r),
    alpha_n=epsilon_n/(1+M_n),
    Q(P,r,S)=alpha_n u_n(P,r,S) for S proper,
    Q(P,r,P)=1-alpha_n K_n(P,r).

Conditional on the admitted positive prefix and sufficient full-marked ratio characterization, these complete rows remain positive and normalized and preserve the marked constraints. No old later coefficient is reused. Summing both newborn bits gives the inherited conditional bound Pr(A_n | history through n)<=epsilon_n, where A_n is a non-full birth from parent size n to size n+1. Full births append above every older vertex and add no incomparable pair. The Bernoulli seed and transitions are not spliced into the summable prefix; the laws keep separate complete prescriptions and may have different source probability spaces. No coupling is needed.

Let I_N count unordered incomparable pairs in P_N. In the Bernoulli realization, consecutive labels i and i+1 can be joined only by their direct edge: increasing paths have no intermediate integer label, and later vertices cannot create a path returning to the older endpoint. Thus Y_i=1-E_(i,i+1) are iid Bernoulli(q), where q=1-p, and

    T_N=sum_(i=1)^(N-1) Y_i <= I_N.

Only these witnesses are assumed independent. The full incomparable-pair indicators need not be independent. Both laws give positive probability to every admissible fixed finite marked history. These support and witness facts are admitted prior results. Their infinite-history count distinction does not give a zero-error finite decision.

The new decision assumes complete exact access to the retained unmarked order at the predetermined size N. Vertex count and incomparable count are intrinsic under relabeling. Hidden generating edges, birth labels, marks and payload are not decision inputs; edges and adjacent labels serve only the proof. No physical device, relation-reconstruction procedure or tolerance to missing, delayed or misclassified relations is provided.

### Fixed design, exact rounding and two error bounds

Before observing the order, separately fix p, the summable schedule and a tolerance delta in (0,1). Choose an integer m>=6 with a known or certified tail bound sum_(n=m)^infinity epsilon_n<=delta. Set

    q=1-p,
    K=binomial(m,2),
    N_0=1+ceil(max{m, 2K/q, 4p/(q delta)}).

At any predetermined integer horizon N>=N_0, choose B_p if I_N>K, and choose S_epsilon if I_N<=K. This is a forced binary rule; equality belongs to the summable decision. Its two separate conditional errors satisfy

    0 < Pr_(S_epsilon)(choose B_p) <= delta,
    0 < Pr_(B_p)(choose S_epsilon) <= delta.

Each error is bounded by delta. The statement does not bound their sum by delta or assign a posterior probability that either law is physically correct.

For the summable side, if no A_n occurs for parent sizes n=m,...,N-1, every birth after the size-m state is full, so I_N=I(P_m)<=K. An error requires at least one such A_n. Taking expectations of the conditional probability bounds and a finite union bound gives

    e_S=Pr_(S_epsilon)(I_N>K)
       <=sum_(n=m)^(N-1) Pr(A_n)
       <=sum_(n=m)^(N-1) epsilon_n <= delta.

No independence, integrable terminal count or stopping-time stabilization index is needed. Parent m generates vertex m+1, so the size-m threshold and union indices are deliberate.

For the Bernoulli side, write r=N-1. The witness has mean rq and variance rpq: independence makes only the witness covariance terms vanish. The whole count need not have this binomial law. Since T_N<=I_N, an error I_N<=K implies T_N<=K. For rq>K the latter event forces (T_N-rq)^2>=(rq-K)^2, so its contribution to the second moment gives

    e_B<=min{1, rpq/(rq-K)^2}.

The rounded horizon ensures r>=m, rq>=2K and rq>=4p/delta. Because m>=6 gives K>0, rq-K>=rq/2>0, and therefore e_B<=4p/(rq)<=delta. The ceiling and extra one account exactly for the N-1 witnesses, including noninteger bounds and equality. No binomial tail computation or simulation is used.

Abstract summability guarantees existence of a finite m, but does not itself furnish an effective tail-cutoff algorithm for an arbitrary sequence presentation. The specified schedule needs its own justified tail bound. For the admitted geometric example epsilon_n=2^(4-n), the tail is 2^(5-m), so

    m=max{6, 5+ceil(log_2(1/delta))}

is an explicit symbolic choice. Substitute it into K and N_0. The design is fixed before observing data; no unknown-p estimation, data-dependent tuning, parameter-uniform guarantee or optimum horizon is claimed.

Both errors are strictly positive. Since N>=N_0>m, an all-empty-precursor history under S_epsilon gives an N-antichain with binomial(N,2)>K and has positive probability. An all-full-precursor history under B_p gives a chain with I_N=0<=K and also has positive probability. Small positive errors thus coexist with overlapping finite support. A new horizon is chosen for each tolerance; no single fixed horizon delivers arbitrary accuracy. No exact full-count distribution, sequential stopping result, universal law-selection principle, physical readout, informative quantum dynamics or spacetime implication follows.

## 2. E: finite entry under strict causal sampled surplus

### Continuous law, broad enclosure and causal action

For i=1,2, j!=i and sigma_1=-1, sigma_2=+1, stipulate the continuous plant

    C_i T_i'=eta_i P_i-h_i(T_i-Ta)+g(T_j-T_i)+sigma_i b+w_i.

Assume C_i,h_i>0, eta_i>=0, finite nonnegative Pbar_i,Gbar,beta,omega_i, finite Aminus<=Aplus, and independent realized heater bounds 0<=P_i<=Pbar_i. The exogenous paths are measurable and essentially bounded in the full product envelope Ta in [Aminus,Aplus], g in [0,Gbar], |b|<=beta and |w_i|<=omega_i, including endpoints and cross-combinations. Shared ambient, coupling and bias remain shared. No total shared heater budget is added.

The desired positive-width service rectangle is S=[L_1,U_1] x [L_2,U_2], d_i=U_i-L_i>0. Independently establish a common broad invariant box R_B=[ell,u]^2 containing both S and the initial state, valid under every admissible realized bounded heater signal. Its finite derivative bounds |T_i'|<=B_i almost everywhere must follow from initial/input premises rather than assumed service safety. They remain valid outside S during entry or a hypothetical exit.

Actual updates t_0<t_1<... tend to infinity without finite accumulation and have 0<t_(k+1)-t_k<=Delta for a certified finite actual Delta>0. A current reading obeys |Y_i^k-T_i(t_k)|<=e_i, e_i>=0. The same causal clipped policy as in the accepted persistence theorem realizes

    P_i(t)=Pbar_i clip((U_i-Y_i^k)/d_i,0,1)
                  for t in [t_k,t_(k+1)).

The policy uses neither future readings nor latent true state. It assumes immediate exact realization of the held action and no unmodeled sensor, timestamp, computation, communication or actuator lag. Such effects need separately justified bounds before applying the theorem. Conditional on the realized admissible schedule and reading/error sequence, bounded held input and measurable affine thermal forcing yield unique interval solutions. State continuity and nonaccumulating updates concatenate them on finite horizons. Different allowed reading errors need not produce the same trajectory.

The input-universal broad bound first applies because clipped action stays within heater limits. Absolute continuity yields |Y_i^k-T_i(t)|<=e_i+B_i Delta throughout each hold. The globally 1/d_i-Lipschitz clip map therefore bounds the thermal-power discrepancy from ideal current-state clipped feedback by

    rho_i=(eta_i Pbar_i/d_i)(e_i+B_i Delta).

This holds before entry, after entry and outside service within the broad box; it assumes no service conclusion.

### Strict surplus and the maximum-distance comparison

Define ideal lower and upper inward power margins

    m_i^- = eta_i Pbar_i+h_i(Aminus-L_i)
            +Gbar min(0,L_j-L_i)-beta-omega_i,
    m_i^+ = h_i(U_i-Aplus)
            -Gbar max(0,U_j-U_i)-beta-omega_i.

Let s_i^-=m_i^- -rho_i and s_i^+=m_i^+ -rho_i. Require all four surpluses strictly positive and set

    r(t)=max_i{(T_i(t)-U_i)^+, (L_i-T_i(t))^+},
    c=min over i and signs of s_i^sign/C_i >0,
    lambda=min_i h_i/C_i >0.

Here r is maximum distance to service in kelvin, c has K/s, and lambda has 1/s. For an active upper violation T_i=U_i+r, every other coordinate satisfies T_j<=U_j+r. Because g>=0, the common r cancels:

    g(T_j-T_i)<=g(U_j-U_i)<=Gbar max(0,U_j-U_i).

The ideal upper action is zero, so the mismatch bound gives eta_i P_i<=rho_i. Worst admissible ambient/bias/disturbance values then imply

    C_i T_i'<=-s_i^+-h_i r.

For an active lower violation T_i=L_i-r, the other coordinate satisfies T_j>=L_j-r, giving

    g(T_j-T_i)>=g(L_j-L_i)>=Gbar min(0,L_j-L_i),
    C_i T_i'>=s_i^-+h_i r.

The ideal lower action is maximum heat, and actual thermal power can fall short by at most rho_i. Neither argument assumes the other zone is already in service; negative coupling would invalidate the cancellation inequality and is excluded.

Every active positive violation thus has outward derivative at most -c-lambda r. Each positive-part violation and their finite maximum are absolutely continuous. Almost everywhere while r>0, the derivative of that maximum is governed by active violations, including ties; all tied active terms obey the same bound. Hence

    r'(t)<=-c-lambda r(t) almost everywhere with r(t)>0.

Command jumps leave the state and r continuous. No derivative assertion is needed at update instants, and no finite accumulation lets the comparison cover every finite horizon.

### Entry duration, corrected time origin and persistence

Let r0=r(t_0), and define the absolute first-entry time

    tau=inf{t>=t_0:r(t)=0}.

If r0=0, entry is immediate. Otherwise integration up to the first zero gives

    r(t)<=(r0+c/lambda) exp[-lambda(t-t_0)]-c/lambda,
    tau-t_0<=B,   B=log(1+lambda r0/c)/lambda.

If the zero time of the comparison passed while r stayed positive, the bound would force a negative nonnegative distance. Thus finite entry follows. Dropping the nonnegative leak term gives the conservative duration r0/c. The actual model has lambda>0; no zero-leak assumption is substituted.

The binding adopted correction fixes the time convention throughout this checkpoint: tau is an absolute endpoint and B is a duration. Its certified upper endpoint is t_0+B. For an actual recorded attempt start a,

    tau-a<=t_0-a+B.

When a=t_0, this becomes tau-t_0<=B. An entry-by-D certificate must compare the appropriate elapsed bound to the actual deadline duration using an independently valid clock mapping. The original source's deadline prose is accepted only with this correction; its central comparison equation and proof are unchanged. No completed or reviewed clean-copy packet is implied.

An exact initial point gives r0. If only T(t_0) in [ell,u]^2 is certified, use

    r0<=r_B=max_i{(u-U_i)^+, (L_i-ell)^+}.

A valid initial reading alternatively gives r0<=r(Y^0)+max_i e_i, by the distance function's infinity-norm Lipschitz bound. Substituting either independently certified upper bound into B is conservative. These certification quantities do not become latent-state operational inputs to the policy.

Strict surplus implies the accepted non-strict sampled invariance margins. That persistence proof compares the held field to the ideal globally Lipschitz clipped field, projects onto S and uses the sum V of coordinate outside distances. Its Lipschitz constant can be taken as max_i(h_i+2Gbar+eta_i Pbar_i/d_i)/C_i, and the mismatch plus inward-face estimates give V'<=2KV. Gronwall preserves V=0. This argument can restart when entry occurs mid-hold because the original held sample-to-current-state mismatch remains bounded by rho_i; no immediate resample is required. Service therefore persists under the same premises after finite entry. This is a continuous true-state statement, not automatically a measured request-success event.

### Zero surplus and actual certification limits

Nonnegative surpluses with minimum zero give only r'<=-lambda r while positive, allowing exponential approach without finite entry. A symbolic admissible witness sets Pbar_i=0, g=b=w_i=0, constant ambient A, service [A-d,A]^2, broad box [A-d,A+a]^2 and initial state (A+a,A), with a,d>0 and C_i,h_i>0. The realized policy is zero heat regardless of readings and rho_i=0; lower margins are h_i d>0 and upper margins zero. Yet

    T_1(t)=A+a exp[-h_1(t-t_0)/C_1]>A at every finite time,
    T_2(t)=A.

The broad box is invariant and has a finite input-universal rate bound. This proves that non-strict invariance alone does not guarantee finite entry. It is not a numerical apparatus result, and failure of strict sufficient conditions is not universal sampled-control impossibility.

Actual independently reviewable plant/input/rate and initial-condition calibration, physical sensing, update-gap, lag, actuator and clock certificates remain absent. Nominal 60-second updates cannot replace a certified actual Delta. The Euler table does not supply continuous physical interpolation. No actual step-60 or step-44 admission follows. D=60, horizon 64 and nominal W=20 remain distinct: the full-window route inside that horizon needs entry by step 44, and later entry needs proved continuation.

Before entry, the distance estimate bounds T_i(t)<=U_i+r0. A separate pre-entry ceiling S_i is certified only if U_i+r0<=S_i is independently proved for each zone, or another safety proof applies. Finite entry alone does not clear the +1 K overshoot requirement. Dwell credit requires a lower actual elapsed-time bound and continuous qualification; the separate two-endpoint intersample certificate uses an upper actual gap with valid readout/rate margins. Physical terminal reset, chamber/storage accounting, complete source-to-reset W/J including failed attempts and independent evaluator custody remain separate.

Matched causal information and resources for every arm, a competent persistent-arrival 32-packet MHE baseline, independent held-out iid evaluation, reliability/quality/time and useful-energy gates, zero-link/capacity controls, protected validation/custody and the executable-design gate persist. The robust disturbance quantifier is not an iid plant assumption. No scientific execution, physical service certificate or DET advantage is granted.

## 3. Carried measurement interpretation: no observed significance

The inherited finite nonnegative energies are X_0 for event second 16, indices [65536,69632), and X_1,...,X_16 for comparison seconds (4,5,6,7,8,9,10,11,20,21,22,23,24,25,26,27), each using the existing 4096-sample half-open window. Write C=max(X_1,...,X_16). Under all existing gates and C>0, X_0>C means CONTRAST_PRESENT and X_0<=C means CONTRAST_NOT_PRESENT. C=0 or another invalidating gate requires ABSTAIN_INVALID. This checkpoint changes none of those nominal rules.

Add a separately justified null law under which the complete fixed vector is jointly exchangeable across all seventeen labels. The event label and procedure must be fixed before inspecting candidate energies, or the actual selection must independently preserve that symmetry. Neither has been established for the current record. Under this premise, for 0<=alpha<=1,

    Pr(X_0>C) = Pr(a unique maximum exists)/17 <= 1/17,
    p = (1 + number of comparisons X_i>=X_0)/17,
    Pr(p<=alpha) <= floor(17 alpha)/17 <= alpha.

The seventeen strict-maximum events are disjoint and equiprobable. For the rank bound, define r_i as the number of coordinates at least X_i. At most k labels have r_i<=k: tied value groups take their full cumulative rank. Exchangeability then bounds the event-label probability by k/17. Independence is unnecessary; distinct coordinates give equality on the rank grid. Using >= preserves conservatism with ties; all-equal energies give p=1.

The unrandomized minimum is 1/17, greater than 5%, so this design cannot produce a 5% rejection even at a strict event maximum. No randomized rule is added. A formal p at C=0 does not rescue the nominal diagnostic: a positive event against sixteen zeros has formal rank 1/17 while the diagnostic still abstains.

Conditional-on-admission calibration requires the corresponding conditional exchangeability for the exact positive-probability admission event, or a justified jointly permutation-invariant vector/metadata law and invariant gate. An unconditional bound on gate-and-maximum does not bound error conditional on accepted records. Conditioning a uniform permutation of 1,...,17 on label zero being largest makes p=1/17 certain. Likewise inspecting those exchangeable candidates and relabeling the largest as the event destroys exchangeability and makes that rank certain. These counterexamples expose logical failures; they do not allege that actual H1 selection followed those exact rules.

Disjointness, ordinary stationarity, common filtering, and deterministic gain or perturbation bounds do not establish the null symmetry. Prior access to the complete record and crop persists; the fixed windows are not a blind holdout. No actual H1 rank, p-value, false-alarm probability, astrophysical-origin probability, physical calibration or DET observation/readout is provided. A prospective justified null and selection law is needed for significance. This optional interpretation is not a new prerequisite for the unchanged nominal-only calculation.

## 4. Retained NE, CE and actual measurement blockers

NE's accepted conditional source-transfer design requires a common actual pre-command source for every candidate, command, trial and reset plus independently justified transfer. Exact block unitaries preserve its trace-distance bound eta_P, with complete-POVM contraction and effect error eta_Q only at their admitted scope. A stable candidate-indexed source can support a one-world risk statement with candidate-blind admission, but does not certify counterfactual equality. The certified-ideal-then-maximally-mixed source counterexample has distance q/4=1/16 and eight outcome probabilities 1/8 at every setting. For source admission B and effect admission A, separately justified risks on the actual joint selected process yield Pr_j(B and A and wrong)<=delta_src+delta_cal+delta_tgt without independence. This is neither conditional error among accepted trials nor an acceptance-rate guarantee. The physical source certificate, reset/command transfer, control/readout, target sampling and clock/time/energy inputs remain absent. Source costs must supplement 32*n_cal+2*N preparations/readouts. No physical generator, clock, action scale, work store or energy measurement is supplied. Await actual independently reviewable physical inputs.

CE retains a documented footprint-triggered fatal-memory policy and launchd/posix_spawn setup candidate. Footprint differs from resident-set size; a post-crossing callback proves no no-overshoot bound. No exact instantaneous resident-memory ceiling <=256 MiB before import for the selected CPython process, installed-system applicability, entitlement sufficiency or durable post-kill receipt is established. Mutable main-branch source locations do not pin installed versions, and the bounded search is not universal impossibility. CPU 10 s, wall 30 s, one process/no children, output 140 KiB, no network and cleanup/failure evidence remain. No trusted-controller process-count amendment is adopted. Await an exact admitted runner contract or an explicitly adopted reviewed alternative; benchmark, native, hardware, GPU, AI and distributed execution remain unadmitted.

Actual measurement execution remains blocked by the absent applicable versioned selected-image/current-cache membership and safe-composition mechanism for the same invocation. Conditional relation mathematics supplies no such binding. Source/build, record/image/process/resource, failure-before-contrast, protected-validation and custody controls persist. No acquisition, repeated replay, native call, source integration, observed calculation or new nominal-calculation gate is authorized. Physical observation maps and calibration remain necessary for physical claims, without being newly imposed on nominal arithmetic.

## 5. Evidence, retained limitations and next actions

Current pinned bytes and inventory checks establish current identity only; they do not reconstruct custody, verify attributed source revisions or prove earlier completion instants. The corrected earlier list-inventory audit did not make its initial schema-limited zero counts successful checks. RI1401's late freeze, missing original RI1389 evidence, historical helper-count limitations, NE-C010/011 gaps, prior measurement active-time uncertainty and CE's failed patch/freeze-repair, mutable-version and unpaired-clock history remain.

RI1411 retains five author guard observations with post-usage clocks; its freeze declaration preceded creation and is not independent completed-file evidence. E-C016 retains six guard-file responses and a separate final freeze response; its final observation is write-start, with completion claims still author-attributed. Root observed current author identities after those declarations, which does not reconstruct the historical completion instant. Earlier RI1407/RI1409 declarations, E-C014/E-C015 write-start qualifications, the earlier E review timestamp correction and concurrent-clock limitations persist. Distinct reviewers' initial post-usage clocks are not invented pre/post brackets. The earlier rank review independently held exact author-freeze bytes before the deadline, while exact creation and substantive-completion times remain attributed. These boundaries survive scientific acceptance.

The shared supported-capacity stop applies at 10% remaining or below for every applicable reported window. Missing or ambiguous required account/window/reset evidence or failed supported tools stops work; null secondary is unavailable, not spare capacity. Supported reset conditions, existing schedules and all resource controls remain unchanged. Option B/Status M, operational ABSTAIN, zero production qualification, protected-validation/custody and RET-only pause persist. This checkpoint uses captured coordinator fronts, preserves all historical suffix bytes and grants no present-checkout application authority. Distinct publication review and root acceptance/release checks remain separate.

RI1413 asks whether a uniform independent fixed-k induced unmarked suborder loses the distinction as N grows, even though exact complete-order counts permit finite-error discrimination. It is an open whether-question: no answer, convergence statement or total-variation bound is presumed. E-C016-C1 is only a requested exact clean-copy correction to the accepted source; its completion or review is not claimed, and it is not a new theorem. After this bounded entry result and correction, E needs actual physical calibration and resource inputs rather than an assumed generic successor. NE awaits actual source/calibration/transfer/resource inputs, CE an exact admitted runner contract or reviewed alternative, and measurement its actual binding/safe-composition input and, separately, a justified prospective null/selection model for significance. No successor finding, generic search, simulation, benchmark or protected-validation run is authorized by this checkpoint.
