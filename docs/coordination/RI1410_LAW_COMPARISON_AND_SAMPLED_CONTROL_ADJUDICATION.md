# RI1410 — Law comparison and sampled control adjudication

This checkpoint consolidates the newly root-accepted RI1409 comparison of two optional order-growth laws and E-C015 sufficient causal sampled-service theorem, after their distinct scientific reviews. It carries the previously accepted fixed 17-window conditional rank interpretation and the unchanged NE, CE and measurement blockers. These are conditional mathematical and documentary results. They supply no physical law selection, finite classifier error guarantee, actual controller admission, observed significance, energy advantage or scientific execution. The exact publication package itself remains subject to distinct review and root application.

## 1. QR: intrinsic count separation with overlapping finite support

### Two separately specified laws

A retained finite order P_N contains the vertices after N births. Each birth adds a maximal vertex whose strict past S is an ideal (a downward-closed subset) of its parent P. The immutable newborn bit is fair; the accompanying arbitrary complex positive-semidefinite payload is scalar-passive, with the complete branch map multiplying it by q(P,r,S)/2. Marks r, transported equivariance, proper-precursor mark locality and complete marked incomparable-birth diamonds belong to the admitted conditional model. They are not derived here from bare DET.

For a fixed p in (0,1), the admitted Bernoulli law B_p starts from empty. Its realization has mutually independent forward-edge coordinates E_ij with Bernoulli(p) distribution for 1<=i<j, independent fair newborn bits, and P_N the transitive closure of the forward-edge directed acyclic graph on labels 1,...,N. Its individual-ideal probability is

    q_p(P,r,S)=p^(|Max(S)|) (1-p)^(|P|-|S|).

Max(S) denotes the maximal elements of S. This positive normalized marked law, its product-edge realization and its previously proved expectation and quadratic-density bounds are admitted inputs, not a new construction in this checkpoint.

Separately fix one summable-allocation law S_epsilon. It retains its own admitted positive prefix through parent size five, hence through the sixth birth. Choose deterministic 0<epsilon_n<1 with sum_(n>=6) epsilon_n finite. For each later marked n-parent and proper ideal, set J=Max(P)\S and use the fixed deletion potential

    u_n(P,r,S)=product over nonempty A subset J of
              q(P\A,r restricted to P\A,S)^((-1)^(|A|+1)),
    K_n(P,r)=sum over every proper ideal occurrence S of u_n(P,r,S),
    M_n=max over every marked n-parent of K_n(P,r),
    alpha_n=epsilon_n/(1+M_n),
    q(P,r,S)=alpha_n u_n(P,r,S) for S proper,
    q(P,r,P)=1-alpha_n K_n(P,r).

All deletion factors come from this law's newly constructed smaller prefix; no old later coefficients are reused. The sufficient full-marked ratio characterization and positive prefix remain explicit admitted premises. Finite positivity gives a proper row load strictly below epsilon_n and a positive full complement. Conditional on that characterization, all marked constraints and complete diamonds are preserved. Summing both newborn bits bounds each later non-full-birth conditional probability by epsilon_n. A tail union bound gives only finitely many non-full births almost surely, without independence. Subsequently every vertex is above every earlier vertex: for a finite random N_*,

    P_N=P_(N_*) ordinal-sum C_(N-N_*) for all N>=N_*.

Here C_k is a k-vertex chain above the retained prefix. The earlier accepted conclusion also gives eventual H_N=N-D for finite integer D>=0, constant width and constant incomparable-pair count. Proper births need not each increase the height deficit; N_* is an eventual pathwise index, not asserted to be a stopping time.

B_p and S_epsilon keep their own seeds and entire transition prescriptions. B_p is not spliced onto S_epsilon's parent-five prefix. Their source probability spaces may differ. All almost-sure claims below concern each named, separately fixed law; no common coupling or simultaneous parameter-uniform event is assumed.

### Count bounds and the infinite-history event

Let I_N=I(P_N) count unordered incomparable pairs. Under B_p, the only possible increasing path from consecutive labels i to i+1 is their direct edge. No intermediate integer label exists, and later vertices cannot form a path returning to the old endpoint. Thus, permanently after their births,

    1_{i incomparable with i+1}=1-E_(i,i+1)=Y_i.

Only these witnesses are asserted iid Bernoulli(1-p): adjacent pairs may share a vertex but use distinct independent edge coordinates. General incomparable-pair indicators need not be independent. The N-1 witness pairs give I_N>=sum_(i=1)^(N-1) Y_i. Their strong law and linearity of expectation yield, for fixed p,

    liminf_(N->infinity) I_N/N >= 1-p > 0 almost surely,
    (N-1)(1-p) <= E_p I_N <= (1-p)N/p^2 for N>=1.

The upper expectation bound and I_N/N^2->0 almost surely are inherited accepted inputs. The lower bound proves divergence and, together with the upper bound, linear order of expectation at fixed p. It does not prove an exact asymptotic count coefficient, convergence of I_N/N or an almost-sure linear upper bound. I_0=0 separately. Birth labels are proof auxiliaries; I(P_N) itself is invariant under relabeling.

Under S_epsilon no new incomparable pair is created after N_*, so I_N becomes a finite random constant. Hence I_N/N and I_N/N^2 tend to zero. Almost-sure finiteness does not establish integrability of the terminal count or a uniform expectation bound for arbitrary summable schedules. Both laws have vanishing quadratic density, also when normalized by binomial(N,2), while their total count behavior differs.

Push the separate laws onto a common measurable space of compatible retained finite order histories, with the sigma-field generated by finite-history coordinates, optionally retaining marks or using order isomorphism classes. Define the intrinsic event

    E={sup_(N>=1) I(P_N)<infinity}
     =union_(k>=0) intersection_(N>=1) {I(P_N)<=k}.

This countable expression proves measurability. Retention preserves every old comparison and incomparison, so the count is a nondecreasing integer and boundedness is equivalent to eventual constancy. E also means that the union order contains only finitely many incomparable pairs; it requires neither generating edges nor a chosen birth labeling. The S_epsilon pushforward assigns E probability one, and the B_p pushforward assigns it probability zero. The infinite-history pushforwards are therefore mutually singular. The same separator lifts to marked histories by ignoring marks. A finite plateau cannot certify E: this is an infinite observation statement, not a finite stopping rule or physical detector.

### Exact finite-support limit

At any fixed finite horizon N, every admissible naturally presented marked history h from empty has positive probability under both laws: each ideal choice and each newborn bit has positive mass. Write these finite masses as mu_N(h) for S_epsilon and nu_N(h) for B_p. They are generally unequal but mutually absolutely continuous. Common coarsening, randomized postprocessing or common selection cannot remove their overlapping positive support.

For a common randomized forced binary rule, let g(h) be its probability of choosing B_p. Its two errors are

    e_S=sum_h mu_N(h) g(h),
    e_B=sum_h nu_N(h) (1-g(h)).

If e_S=0, positivity forces g=0 everywhere; if e_B=0, it forces g=1 everywhere. Both errors cannot vanish. This does not require each individual error to be positive: a constant decision can be right under one law and wrong under the other. With abstention, let g_B,g_S>=0 and g_B+g_S<=1 be probabilities of the conclusive answers. Zero wrong-answer probability under both laws forces both conclusive functions to vanish everywhere, hence almost-sure abstention under both. There is no error-free conclusive subset of positive probability at that fixed horizon.

This fixed-horizon support result permits statistical evidence and unequal likelihoods. It supplies no numerical nonzero error bound, sequential sample complexity, endpoint-p claim, size-dependent parameter result or guarantee uniform in p and epsilon. Neither optional law is selected as physically correct. No physical readout, clock, metric, dimension, informative quantum dynamics, empirical discriminator or universal DET law follows.

## 2. E: causal noisy sampled control with explicit service margins

### Law, independent rate premise and implemented policy

For zones i=1,2 and j!=i, stipulate the continuous law

    C_i T_i'=eta_i P_i-h_i(T_i-Ta)+g(T_j-T_i)+sigma_i b+w_i,
    sigma_1=-1, sigma_2=+1.

Assume C_i,h_i>0, eta_i>=0, finite nonnegative Pbar_i,Gbar,beta,omega_i, and finite Aminus<=Aplus. Realized independent heater powers satisfy 0<=P_i<=Pbar_i. The uncertainty class is the full product of measurable essentially bounded paths Ta in [Aminus,Aplus], g in [0,Gbar], |b|<=beta and |w_i|<=omega_i, with endpoints and allowed cross-combinations. Shared Ta,g,b remain shared quantities; no common total heater-budget constraint is added.

Fix the desired positive-width service rectangle S=[L_1,U_1] x [L_2,U_2], d_i=U_i-L_i>0. Independently prove a common broad enclosure R_B=[ell,u]^2 containing S, invariant from its admitted initial states under every realized bounded heater input. Establish finite nonnegative B_i in K/s satisfying ess sup |T_i'|<=B_i throughout that broad enclosure and the relevant time domain. These are external input-universal bounds, obtained without assuming service invariance; a rate proved only inside S is insufficient. This independence makes the rate available even during a hypothetical service exit. Begin with T(t_0) in S, hence in R_B.

Actual updates satisfy t_0<t_1<... with t_k tending to infinity and 0<t_(k+1)-t_k<=Delta. Delta is a finite actual-time upper bound, not a nominal sampling interval. At t_k a current reading satisfies |Y_i^k-T_i(t_k)|<=e_i, e_i>=0, and the realized action immediately becomes

    P_i(t)=Pbar_i clip((U_i-Y_i^k)/d_i,0,1)
              for t in [t_k,t_(k+1)).

The command uses only current and past available readings and remains within heater bounds even for readings outside S. No future reading or latent true state is an operational input. There is no unmodeled sensor, computation, communication, timestamp or actuator delay, nor mismatch between held command and realized heater power. Any such effect would need its own proved contribution before applying this theorem. Positive actual update gaps require Delta>0; Delta=0 in algebra is only an ideal continuous-update limit, not a realizable positive-gap schedule.

### Sufficient inequalities and equality-safe proof

Define the ideal full-envelope inward margins in watts:

    m_i^- = eta_i Pbar_i+h_i(Aminus-L_i)
            +Gbar min(0,L_j-L_i)-beta-omega_i,
    m_i^+ = h_i(U_i-Aplus)
            -Gbar max(0,U_j-U_i)-beta-omega_i.

They use maximum heat at a lower face and zero heat at an upper face. Unequal zone bands allow adverse coupling directions; nonnegative coupling is not simply assumed inward. For ideal instantaneous full-state feedback these are the previously accepted face margins. The new sufficient sampled condition is

    rho_i=(eta_i Pbar_i/d_i)(e_i+B_i Delta),
    m_i^- >= rho_i and m_i^+ >= rho_i for each i.

Absolute continuity and the independent broad bound imply |Y_i^k-T_i(t)|<=e_i+B_i(t-t_k)<=e_i+B_i Delta throughout a hold interval. The clipped map is globally 1/d_i-Lipschitz. Consequently the thermal-power discrepancy from the ideal current-state feedback pi_i(x)=Pbar_i clip((U_i-x_i)/d_i,0,1) is at most rho_i, including for actual states outside S but inside R_B. The sensing/hold term is extra margin; it does not replace ambient, bias, disturbance or coupling uncertainty. Failure of these sufficient inequalities alone proves neither sampled-control impossibility nor exit under this policy.

For each fixed allowed update schedule and realized reading sequence, the held thermal field is measurable in time, affine and globally Lipschitz in state on each interval, with bounded forcing. States remain continuous across updates though actions can jump. No finite accumulation of updates allows the unique interval solutions to concatenate over every finite horizon. Uniqueness is conditional on the realized causal readings and schedule; different admissible error realizations need not produce the same trajectory. Clipping keeps powers admissible, so the broad enclosure first applies independently.

The ideal clipped field has a global infinity-norm Lipschitz constant

    K=max_i [h_i+2Gbar+eta_i Pbar_i/d_i]/C_i.

Let z be coordinatewise projection of the actual state x onto S and V(x)=sum_i[(x_i-U_i)^+ +(L_i-x_i)^+]. At an upper projected face the ideal derivative is at most -m_i^+/C_i; the actual held derivative differs by at most rho_i/C_i plus K||x-z||_infinity. Under the sufficient margin it is at most K V(x). The corresponding lower-face outward derivative has the same bound. The positive-part chain rule therefore gives V'<=2K V almost everywhere, including boundary contact. Since V(t_0)=0, Gronwall gives V=0 throughout each hold interval and then across every finite horizon. This establishes robust forward invariance from every initial point of S, for every allowed exogenous path, actual update schedule and bounded-error causal reading sequence under this policy. Non-strict equality in both margin conditions is covered; a bare first-exit assertion is not needed.

If either ideal margin is zero, this certificate forces rho_i=0. With eta_i Pbar_i>0 that means e_i=0 and B_i Delta=0; positive-gap schedules with Delta>0 then require B_i=0. No positive sensing or motion-during-hold tolerance is furnished at that zero-margin face. If eta_i Pbar_i=0, rho_i=0 regardless of readings, but the uncontrolled inward-face conditions still must hold; no heating authority is created.

### Actual service and cost boundary

No plant coefficients, broad-box rates, positive face slack, sensor errors, physical clock-gap bound, lag or actuator response have been calibrated here. Substituting nominal 60 seconds for Delta without a certified actual upper gap and valid coefficients is invalid. The Euler table provides sample-boundary algebra, not continuous physical interpolation or an independently proved derivative bound.

The theorem proves persistence after independently certified entry. It establishes no reachability or entry by D, actual dwell credit, pre-entry +1 K overshoot protection, viable continuation, terminal return/reset or energy advantage. The official entry deadline remains step 60; a horizon of 64 steps and nominal dwell of 20 intervals gives the conservative full-window route only when entry is no later than step 44, and later entry needs proved continuation. The intersample endpoint test requires valid sensor/lag uncertainty and an upper actual interval duration; uninterrupted W needs a lower elapsed-time bound. Those two clock directions are distinct.

Matched causal information/resources for all arms, a competent persistent-arrival 32-packet MHE baseline, independent held-out iid evaluation, reliability/quality/time and useful-energy gates, failure/reset and complete source-to-reset W/J accounting, zero-link/capacity controls and protected-validation/custody obligations remain. The iid evaluation obligation is not an iid premise on the robust thermal disturbance paths. No executable-design or physical controller admission is supplied.

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

## 5. Evidence, retained limitations and open questions

Current pinned bytes and the predecessor inventory check establish current identity only. They do not verify an attributed historical source revision, reconstruct custody or prove earlier completion instants. The prior schema-limited zero-count inventory audit was corrected; the original zeros were not successful coverage. RI1401's late freeze, missing original RI1389 evidence, the legacy helper-count limitation, NE-C010/011 gaps, prior measurement active-time uncertainty and CE's failed patch/freeze-repair, mutable-version and unpaired-clock history remain.

RI1409's five recorded author guards are consistent with its stated account/window and budget, but its freeze declaration preceded creation and is not independently completed-file evidence. E-C015 has five guard-file receipts plus a separate final freeze response; its final observation was write-start, not completed-file time. E-C014's earlier write-start qualification, the prior E review timing correction and inherited concurrent-clock limitations remain. The new distinct review's initial sequential usage call preceded its clock and reads, but is not a strict before/after bracket. The earlier rank review independently possessed the author freeze before its deadline while exact creation and substantive-completion instants remain attributed. Current identity does not repair these evidentiary boundaries.

The shared supported-capacity stop applies at 10% remaining or below for any applicable window, and unavailable or ambiguous required capacity/account/reset stops work. Null secondary is unavailable, not spare capacity; supported reset conditions and all resource controls persist. Option B/Status M, operational ABSTAIN, zero production qualification, actual protected-validation/custody and RET-only pause are unchanged. This is inert documentary preparation from captured fronts. Distinct publication review and present-checkout release checks remain root responsibilities. The complete historical suffixes are preserved, including earlier status wording superseded by the new front.

RI1411 is the open question whether intrinsic incomparable count permits a finite-observation classifier with explicit nonzero error guarantees for fixed p and a fixed summable schedule. No answer, finite error bound or physical readout is presumed. E-C016 is the open question whether strict surplus margins establish finite-time entry under the same causal sampled policy, retaining actual plant/sensing/time, pre-entry safety and reset gaps. No entry theorem is presumed. Both are successor questions only; this checkpoint accepts no successor result and authorizes no execution. NE awaits actual source/calibration/transfer/resource inputs, CE an exact admitted runner contract or reviewed alternative, and measurement actual binding/safe-composition input and, separately, a justified prospective null/selection model for significance. No generic search, simulation, benchmark or protected-validation run follows from this checkpoint.
