# RI1408 — Law and service adjudication

This documentary checkpoint consolidates the newly root-accepted RI1407 conditional summable-allocation theorem and E-C014 exact robust service-rectangle test, together with the previously locally accepted fixed 17-window rank interpretation now eligible for publication after distinct checkpoint review. The independent reviews accept these results only under their stated premises. They provide no scientific execution, physical validation, observed significance, energy advantage or universal DET prediction. NE's physical-input hold, CE's strict resident-memory hold and measurement's binding/safe-composition hold remain active.

## 1. QR: an optional summable law and eventual finite deficit

A state consists of a finite order P, immutable binary marks r, and an arbitrary complex positive-semidefinite payload. A birth adds a maximal vertex with ideal past S and fair newborn bit b; its complete branch map multiplies the payload by q(P,r,S)/2. All ideals, empty and full included, remain eligible. Proper probabilities may depend on the whole unmarked parent and precursor marks; full probabilities may use all parent marks. Marked equivariance and complete incomparable-birth diamonds are required. The positive prefix through parent size five and the sufficient full-marked ratio-potential characterization are admitted premises, not newly proved or derived from bare DET.

For n>=6 choose in advance a deterministic dimensionless schedule 0<epsilon_n<1 with sum_n epsilon_n finite. Preserve transitions from parents of sizes 0 through 5. Rebuild every later layer from the changed prefix. In the fixed potential convention, for a proper ideal S set J=Max(P)\S and

    u_n(P,r,S) = product over nonempty A subset J of
                q(P\A, r restricted to P\A, S)^((-1)^(|A|+1)),
    K_n(P,r) = sum over every proper ideal occurrence S of u_n(P,r,S),
    M_n = max over every marked n-parent (P,r) of K_n(P,r),
    alpha_n = epsilon_n/(1+M_n),
    q(P,r,S) = alpha_n u_n(P,r,S) for S proper,
    q(P,r,P) = 1-alpha_n K_n(P,r).

Every factor uses the newly constructed smaller-size prefix. Finite positivity gives finite positive potentials and M_n. The proper row load is at most epsilon_n M_n/(1+M_n)<epsilon_n<1; every proper branch and the full complement remain strictly positive and each row normalizes. The admitted ratio characterization permits the common positive scale and preserves marked locality, equivariance and every complete marked diamond, including equal precursors and full first precursors. The fair bits contribute the same 1/4 to both complete two-birth maps on arbitrary PSD payloads. Changed full complements enter the next layer's potentials. Reusing old later coefficients or scaling proper branches in an already finished law would not supply this argument.

Let A_n be a non-full birth from parent size n. Summing both newborn bits gives Pr(A_n | complete marked history through n)<=epsilon_n. Hence

    Pr(any A_n with n>=m) <= min(1, sum_{n>=m} epsilon_n),
    E[sum_{n>=6} 1_A_n] <= sum_{n>=6} epsilon_n < infinity.

A tail union bound, or the finite expected count, proves only finitely many non-full births almost surely without independence. Positive finite-branch probabilities cause no contradiction because no uniform later lower bound is imposed. The optional schedule epsilon_n=2^(4-n) has total 1/2 and tail 2^(5-m); these are symbolic bounds, not executed estimates.

For vertex-count height H_n, H_(n+1)=max(H_n,1+H(S)), so each increment is zero or one. A full birth increments height by one; a proper birth can also do so. The deficit D_N=N-H_N is a nondecreasing integer bounded by D_6 plus the finite number of later non-full births. If K is the last proper parent index, with K=5 when none occur after size five, set N_*=max(6,K+1). Then a finite random integer D>=0 satisfies

    H_N=N-D for every N>=N_* almost surely.

N_* is an eventual pathwise index, not asserted to be a stopping time. No exact deficit distribution or deterministic stabilization size follows, and D need not count all proper births. The order is the retained finite order P_(N_*) followed by a chain above it. Width and the number of unordered incomparable pairs therefore become constant, while old incomparabilities can persist forever; the whole order need not be a chain. H_N/N tends to one in this optional family.

This is a changed law in a fixed potential convention, not a gauge change or a DET-selected mechanism. The unchanged half-scale baseline, with its own recursively built potentials, retains its previous accepted half-height statement; this summable argument neither proves nor disproves its eventual constant deficit. Intrinsic event count and height supply no physical clock, readout, metric, dimension, informative quantum dynamics or manifoldlike spacetime.

## 2. E: exact conditional service-rectangle invariance

Fix the positive-width rectangle R=[L_1,U_1] x [L_2,U_2], d_i=U_i-L_i>0, and the separately postulated continuous law, for j!=i,

    C_i T_i' = eta_i P_i - h_i(T_i-Ta) + g(T_j-T_i) + sigma_i b + w_i,
    sigma_1=-1, sigma_2=+1.

Assume C_i,h_i>0, eta_i>=0, finite nonnegative Pbar_i,Gbar,beta,omega_i, and Aminus<=Aplus. The uncertainty class is the full product of measurable essentially bounded paths Ta in [Aminus,Aplus], g in [0,Gbar], |b|<=beta and |w_i|<=omega_i, including endpoints and independent combinations. Realized heaters are independent controls 0<=P_i<=Pbar_i, with perfect current full-state access and no lag. No shared heater budget is assumed.

One fixed regular feedback robustly preserves every initial point in the whole rectangle for every path in this full envelope if and only if, for each i,

    F_i^- = eta_i Pbar_i + h_i(Aminus-L_i)
            + Gbar min(0,L_j-L_i) - beta - omega_i >= 0,
    F_i^+ = h_i(Aplus-U_i)
            + Gbar max(0,U_j-U_i) + beta + omega_i <= 0.

These coupling extrema account for possibly different zone bands. The lower face uses maximum heat and the upper face zero heat. The opposite signs of the shared b do not need to realize both adverse signs simultaneously: each necessity witness concerns one face. Equality allows tangent flow.

For sufficiency use P_i(T)=Pbar_i clip((U_i-T_i)/d_i,0,1). It is bounded and globally Lipschitz and gives the required face actions. For each allowed exogenous path the vector field is measurable in time, globally Lipschitz in state, with linear growth. A valid infinity-norm Lipschitz constant is max_i (h_i+2Gbar+eta_i Pbar_i/d_i)/C_i. Thus the Caratheodory solution exists uniquely. Let V be the sum of coordinate distances outside their intervals. At the clipped state every active face points inward; the Lipschitz estimate and positive-part chain rule give V'<=2KV almost everywhere. Gronwall and V(t0)=0 imply invariance.

If a lower inequality is strictly negative, start on T_i=L_i,T_j=L_j and hold Ta=Aminus, sigma_i b=-beta,w_i=-omega_i, with g=Gbar if L_j<L_i and g=0 otherwise. Even maximum allowed heat points outward. Strictness persists locally and causes immediate exit for every bounded heating choice. For an upper inequality strictly positive, use T_i=U_i,T_j=U_j, Ta=Aplus, sigma_i b=+beta,w_i=+omega_i, and g=Gbar if U_j>U_i, otherwise zero. Even zero heat points outward. These constant admissible witnesses prove necessity for the full product class and every-initial-point claim. A narrower correlated uncertainty family or a selected interior initial set can behave differently.

This test concerns persistence after independently certified entry. It supplies no reachability, sampled-state observation channel, sample/hold or lag guarantee, physical coefficient calibration, pre-entry safety, reset, continuous dwell or cost advantage. The Euler table supplies only sample-boundary algebra, not a physical interpolation. Intersample service still needs sensor/lag uncertainty, a valid rate bound and an upper actual clock-gap bound; uninterrupted dwell needs a lower elapsed-time bound. D=60, horizon 64 and W=20 remain: full nominal dwell inside that horizon requires entry by step 44, while later allowed entry needs proved continuation. The separate +1 K pre-entry overshoot ceiling and terminal physical reset remain unproved. Matched information/resources, the competent persistent-arrival 32-packet MHE baseline, held-out iid evaluation, reliability/quality/time margins, zero-link/capacity controls and complete source-to-reset W/J including failure and reset costs persist.

## 3. Measurement: fixed 17-window conditional rank interpretation

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

## 5. Evidence, process limits and next questions

Present pinned bytes and corrected predecessor inventory checks establish current identity only. The initial generic inventory audit's zero counts were schema-limited failures to cover list-based inventories, subsequently corrected; they are not successful checks and repair no history. Original missing RI1389 evidence, RI1401's late freeze, the legacy helper guard-count limitation, prior measurement active-time uncertainty, NE-C010/011 gaps and CE's failed patch/freeze-repair, mutable-version and unpaired-clock history remain. No historical custody or timing is reconstructed.

RI1407's six stored author guards and declarations are consistent with its budget, but its completion/readback attribution remains limited and an early declaration did not independently certify completion. E-C014 has four separate author guard records and a fifth response embedded in its freeze; usage/write-start is not independent completed-file time. Earlier E timestamp corrections and the combined review's first concurrent-clock limitation persist. The rank review independently possessed the exact author freeze before the author's deadline; exact creation and substantive-completion instants remain attributed. Its first concurrent author clock/usage observation and later brackets do not certify continuously sampled capacity or each read instant. These documentary acceptances do not waive those limits.

The shared supported-capacity stop applies at 10% remaining or below for any applicable window; unavailable or ambiguous applicable capacity stops work, and null secondary is unavailable rather than spare capacity. Supported reset conditions, actual protected-validation/custody, all resource controls, Option B/Status M, operational ABSTAIN, zero production qualification and RET-only pause persist. This checkpoint itself is inert documentation, prepared from captured fronts; present checkout/application verification and distinct publication review remain separate root responsibilities. Historical suffixes are retained verbatim even where earlier status wording has been superseded by this front.

RI1409 asks whether the accepted Bernoulli subset law has unbounded incomparability count and, if so, how that compares with RI1407's eventual finite count, distinguishing infinite-history law separation from finite-history discrimination and physical readout. E-C015 asks for sufficient causal noisy sampled-hold service margins derived from E-C014's continuous-feedback theorem using E-C013's independent global derivative enclosure. Both are assigned author work pending independent review; they remain next questions only. No successor result is accepted or executed here. NE waits for actual physical source/calibration/transfer/resource inputs, CE for a reviewed exact runner input, and measurement for actual binding/safe-composition input and, separately, a justified prospective significance model. No new generic search, simulation, benchmark or protected-validation run follows from this checkpoint.
