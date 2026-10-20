# Optional approximate-sampler robustness protocol for the one-birth width diagnostic

20 October 2026. Source-based design and manual probability derivation only.

**Optional prospective design; ABSTAIN / NOT RUN operationally.**
This is a separate optional protocol. It does not amend, satisfy, relabel or relax [frozen D4-A](WIDTH_DIAGNOSTIC.md), whose exact-sampler/channel acceptance remains unchanged. It supplies sufficient prospective error certificates for a different, explicitly approximate implementation. No numerical effect bound, sampler, random-source certificate, channel-error certificate or measured performance is supplied.

## 1. Fixed scientific target

Retain D4-A's original admitted baseline B at lambda=1, original normalized harmonic z with z1=1, and epsilon=1/4. Each call starts afresh at the same six-element parent P*=C3 ordinal-sum A3 with all old marks zero. Use the complete ideal row and both newborn bits, with target probabilities

    P_B(S,b) = q_B(P*,0,S)/2,
    P_Q(S,b) = q_B(P*,0,S) h7([P*+S])/2.

The outcome space has 22 entries: eleven individual ideals and two newborn bits. Its ideal list is empty, the first one and first two chain elements, and C3 union any subset of the three caps. No supported-child, proper-birth, width, bit or trajectory selection is allowed. Approximation error is charged against these complete target laws; an approximate implementation is not thereby an admitted exact growth law.

The fixed ideal observation is Y=width(P*+S)-3, in {0,1}. Equivalently, Y=1 exactly when the newborn is incomparable with all three caps. The mathematical channel and parent embedding are fixed. An approximate reported bit is denoted X; a malformed order, missing record or nonbinary channel output is a failure, not a silently repaired value.

Write mu_a=E_Pa[Y] and Delta=mu_Q-mu_B. The inherited identity is Delta=rho U0/4>0. Freeze a separately certified numerical 0<d<=Delta. The statistical regions remain H0: Delta<=0 and H1: Delta>=d. H0 is the no-gain comparator, not another theoretical prediction for the declared B/Q pair. The gap 0<Delta<d has no guarantee.

## 2. Sufficient certificate A: conditional error plus a failure budget

Freeze the two arms, approximation/channel versions, exact score rule, draw order, n and all bounds before viewing any held-out outcome. Use n calls per arm in a fixed schedule. Let F0 contain all selection/calibration information, but no unrevealed held-out randomness; Ft contains the complete past revealed history across BOTH arms. Required bounds must hold for every reachable history, not just on average over histories. Shared RNG state, common random numbers, adaptive numerical errors and cross-arm dependence are not assumed harmless.

A good-certificate event G, determined before the held-out attempt, must have probability at least 1-kappa. On G, uniformly conditional on F0 and past history:

1. Whenever a scheduled step returns a valid, nonaborted result, its complete ideal/bit distribution K_at satisfies total variation TV(K_at,P_a)<=e_a. Here TV is sup_A |K(A)-P_a(A)|. This conditioning includes that step's return/failure decision; a failure correlated with the generated value cannot be ignored when certifying the returned distribution.
2. Given that valid return and history, the reported binary X differs from the exact Y of its emitted order with probability at most c_a. The ideal order/channel error is therefore represented explicitly rather than attributed to sampling variation.
3. The probability of any incomplete batch, detected invalid output, timeout or other operational ABSTAIN during this single attempt is at most nu, conditional on F0 and G. No independence of failures from scores is required. If only wrong-terminal-decision guarantees are wanted, this availability bound can be omitted, as explained below; it cannot be omitted from a claim of 95% power.

Use deterministic analytic certificates where possible, giving kappa=0. A probabilistic certificate must have a justified failure bound covering the chosen d, law approximation, random source, channel and availability claims together; held-out outcomes cannot create that certificate. Independence of certification/calibration from held-out selection is required, or the displayed conditional guarantees must explicitly cover that selection. No confidence level is supplied merely by calling a check independent.

Define

    b_a = min(1, e_a+c_a),   B=b_Q+b_B,
    g=d-2B,                r=kappa+nu.

Require g>0 and r<1/20. This means total worst-case arm bias must be strictly less than half the certified ideal effect. A valid-return score has conditional mean in [mu_a-b_a,mu_a+b_a]: the binary score event changes by at most TV, and channel disagreement changes its expectation by at most c_a. Adding these errors does not require independence between sampler and channel errors.

For a fixed k_a-bit TOTAL sampling map to the 22 outcomes, given independently valid constituent certificates, one may take e_a=min(1,e_map,a+e_bits,a): under ideal uniform bits, the map approximates P_a within e_map,a; the actual consumed bit BLOCK, conditional on the relevant history/valid return, is within e_bits,a of that ideal uniform block. Deterministic mapping cannot increase TV. A variable-length implementation needs a certificate covering its complete consumed transcript and stopping rule, or a direct conditional K_at bound; the fixed-block shortcut does not automatically apply. Marginal bit balance, a pseudorandom-generator name or a computational-security claim alone is not a statistical TV or independence certificate.

## 3. Frozen decision and finite cost

Choose prospectively

    n = ceil(4 log(1/(1/20-r)) / (d-2B)^2),
    Dhat = (sum_i X_Qi - sum_i X_Bi)/n.

The logarithm is natural. More draws can be fixed beforehand; none can be added after seeing results. Verify that the declared computational/storage budget admits this n. A zero-error, total-interface model with kappa=nu=B=0 recovers D4-A's sample-size formula algebraically; it does not retroactively qualify an approximate run as D4-A.

The sole terminal rule is:

- ABSTAIN before running if d, the distribution/dependence/channel certificates, necessary availability guarantee, feasible n or frozen protocol are missing or invalid.
- ABSTAIN on an incomplete batch or detected premise violation; retain all records and the actual failure reason. No favorable retry, dropped draw, replacement sample or optional stopping is covered.
- With all 2n scheduled valid outputs and premises satisfied: PASS iff Dhat>=d/2, otherwise FAIL.

There is one declared comparison and one held-out attempt. Unknown dependence or a retrospectively estimated error allowance cannot be repaired by increasing n.

Under certificate A, the false-PASS risk under H0 is at most 1/20. Under H1, the probability of FAIL OR operational ABSTAIN is at most 1/20: beta here includes failure to deliver a PASS. These are unconditional probabilities for this predeclared attempt within the certified model, not probabilities conditioned on the favorable event of completion. A preflight ABSTAIN because the design is uninstantiated is not an experiment with established power.

If no nu is certified, a weaker, explicitly labelled result is available with r=kappa and the same conditional bias premises: both wrong terminal decisions, P_H0(PASS) and P_H1(FAIL), are at most 1/20. There is then NO 95% power/availability claim, since ABSTAIN might be frequent. This weaker label must not be substituted for the full-power protocol above. Failure rates and abstentions must always be reported separately.

## 4. Manual finite-sample proof, including dependence and aborts

On G first consider the complete scheduled score sequence. If an abort occurs, complete it only mathematically with independent ideal target scores for that step and the remaining scheduled steps. These virtual values are never executed or reported. The conditional law on a valid return obeys the stated bias bound; an abort filled by an ideal score has zero bias. Their mixture still has bias at most b_a. Thus the proof does not condition on eventual completion and does not discard an informative abort.

Give each score weight s_t/n, where s_t=+1 for Q and -1 for B. Let m_t=E[X_t|F_(t-1)] for this virtual completion and set

    M = sum_t (s_t/n)(X_t-m_t),
    A = sum_t (s_t/n)m_t.

The signed conditional-mean sum obeys |A-Delta|<=B pathwise, and Dhat=A+M on every completed actual run. Each centered signed increment has conditional mean zero and interval length 1/n. The conditional bounded-variable exponential bound is

    E[exp(u (s_t/n)(X_t-m_t)) | F_(t-1)]
        <= exp(u^2/(8n^2)).

For completeness, for a binary variable the second derivative of its centered log moment-generating function is its exponentially tilted variance, at most 1/4. Integrating twice from value and derivative zero gives u^2/8; scaling gives the displayed bound. Iterated conditional expectation over 2n steps gives E exp(uM)<=exp(u^2/(4n)). No factorization into independent actual trials is assumed.

Markov's inequality optimized at u=2nt therefore gives either tail bound exp(-nt^2). Under H0, PASS implies M>=d/2-B=g/2. Under H1, FAIL implies M<-(d/2-B). On G, each wrong-terminal probability is at most exp(-ng^2/4). The actual PASS/FAIL events are subsets of their virtual-completion events, so the same bounds hold with outcome-dependent aborts. Add kappa for a bad certificate; for H1 non-PASS add nu for operational ABSTAIN. Hence

    P_H0(PASS) <= kappa + exp(-ng^2/4) <= 1/20,
    P_H1(FAIL or ABSTAIN) <= kappa+nu+exp(-ng^2/4) <= 1/20.

The sample-size rule proves the last inequalities. FAIL is still not proof of Delta<=0 or a refutation of DET. Certification errors, algorithm failures and statistical fluctuations remain distinct.

## 5. Alternative certificate B: one whole-attempt distribution bound

A second sufficient route may be selected BEFORE observation instead of A. Let R_n be the actual law of the complete ordered 2n reported bits, with one extra outcome ABORT for any incomplete/invalid attempt. Let P_n be the product of n ideal Q-score Bernoulli laws and n ideal B-score laws, with zero mass on ABORT. Require an independently justified bound

    TV(R_n,P_n)<=zeta,   kappa+zeta<1/20,

uniformly conditional on frozen preflight information on G; kappa bounds certificate failure as above. This certificate covers arbitrary internal dependencies, approximate bits, channel errors and all aborts together. It is a bound on the WHOLE output law, not on individual marginals. Use the unchanged d/2 threshold and a prospectively chosen n satisfying

    exp(-n d^2/4) <= 1/20-kappa-zeta.

If the available bound is zeta(n), verify this inequality at the chosen n BEFORE running; do not treat it as a constant or assume larger n improves it. For either decision event, TV adds at most zeta to its independent ideal probability. Under H1 the event is non-PASS, including ABORT. Thus both full error budgets hold. No sampling is needed to derive this argument, but no such joint certificate is supplied here.

As a counterexample to using marginal accuracy alone, duplicate one fair bit for every Q output and an independent fair bit for every B output. Every marginal has its ideal no-gain distribution, but Dhat is 1 with probability 1/4 for every n. A fixed positive threshold below 1 therefore has false-PASS probability 1/4, not a vanishing tail. Neither A's conditional-history premise nor B's small whole-attempt TV follows from those perfect marginals. Without a suitable certificate, ABSTAIN.

## 6. Computational accounting and remaining inputs

A complete run uses exactly 2n one-birth returns and O(n) counting operations. If the ideal specialized decoder is used, at most 6n cap-comparability checks suffice and c_a=0 under that decoder's correctness assumptions. An approximate channel instead has its declared cost C_channel and certified c_a. Working counters need O(log n) bits; complete auditable records require O(n) storage. A fixed k_a-bit sampler uses n(k_Q+k_B) bits; variable consumption requires its own prospective finite resource bound and failure accounting.

Write C_prepare for obtaining and independently checking d, the exact target-law descriptions, algorithm and error/resource certificates. The run cost is

    C_prepare + n(C_draw,Q+C_draw,B+C_channel,Q+C_channel,B)
              + O(n) accounting, plus audit storage.

Neither unknown normalization nor exact target coefficients are priced as free local inputs. The effective separation d-2B, certificate risk and availability budget can make the finite cost prohibitive. Quantization/bit/channel allowances must be adequate for the chosen n, rather than inferred from one favorable observed statistic. Record actual failures, costs and held-out outcomes if a future authorized implementation instantiates this design; no rates or advantages are measured here.

A total finite sampling/channel implementation can establish nu=0 within a declared mathematical execution model; external interruption or unmodelled failure remains an actual ABSTAIN and cannot be advertised as covered reliability. This design demands only the guarantees used by this bounded decision, not full production qualification.

Missing now: a numerical d; an approximate implementation; independently established conditional error/availability certificates A or whole-attempt certificate B; and a feasible frozen n/resource budget. The optional protocol is operationally ABSTAIN / NOT RUN. The current D4-A disposition is unchanged. No scientific simulation, coefficient acquisition, observed-data work, empirical width advantage, physical observation channel, h8/30/33/38 transfer or DET validation follows. PASS does not certify its own error bounds or independently establish faithful realization of the declared law. No successor or execution is authorized by this manuscript.

## Deterministic implementation component

The separate [categorical-map component](CATEGORICAL_MAP.md) now implements
a fixed-bit partition for supplied exact rational proxy probabilities and
reports its exact map-to-proxy total-variation error. It obtains no random
bits and supplies neither the declared-law row nor its proxy-error certificate.
The true-law/proxy, bit-source, channel, effect-size, resource and failure
premises above remain required; the diagnostic remains **ABSTAIN / NOT RUN**.
This component and its synthetic tests do not alter the protocol's normative
conditions or supply a whole-attempt certificate.
