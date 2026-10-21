# A rational proxy certificate from a complete probability envelope

20 October 2026. Prospective mathematical/API design.

**Implementation update:** the separately reviewed [exact constructor](ENVELOPE_IMPLEMENTATION.md)
now implements this contract. The original design and proof below are retained;
references to a future implementation describe that design stage. Actual-law
intervals and operational benchmark admission remain absent.

**Operational status: ABSTAIN / NOT RUN.** No interval producer, native probability row, sampler, random-source or channel certificate, numerical effect bound, or held-out result is supplied. This design can discharge the *proxy-error* premise of the [deterministic categorical map](CATEGORICAL_MAP.md) only when its external premises are independently established. [Frozen D4-A](WIDTH_DIAGNOSTIC.md) and the separate [optional approximate protocol](APPROXIMATE_WIDTH_DIAGNOSTIC.md) are unchanged.

## 1. Inputs and the claim to be certified

Fix a complete ordered finite outcome list with m entries. A true target row P may have real probabilities, but it must be normalized on this exact list. Externally supplied exact rational endpoints must satisfy

    0 <= l_i <= u_i <= 1,
    E = {P: sum_i P_i = 1 and l_i <= P_i <= u_i for every i}.

The endpoint certificate must cover every coordinate simultaneously for the same target law, marking, baseline and outcome dictionary. The algebra below neither authenticates that certificate nor proves that the list is complete. In the optional width application the list contains all eleven individual ideals and both newborn bits, without outcome aggregation, thinning, supported-child selection or conditioning on favorable births.

The deliverable is one deterministic normalized rational q on the same ordered list and an exact rational eta such that

    TV(q,P) <= eta for EVERY P in E.                         (E1)

All outcomes remain in q, including coordinates forced to zero. A possible zero proxy mass is not an assertion of positivity or admissibility of a new exact growth law.

## 2. Feasibility and normalization tightening

Let L0 = sum_i l_i and U0 = sum_i u_i. Subject to the endpoint inequalities, the necessary and sufficient feasibility condition is

    L0 <= 1 <= U0.                                         (E2)

Necessity follows by summing the coordinate bounds. For sufficiency, put S0 = U0-L0. If S0=0, (E2) forces L0=U0=1 and the unique point is q=l=u. If S0>0, t0=(1-L0)/S0 lies in [0,1], and l_i+t0(u_i-l_i) lies in its interval and sums to one. This is an existence proof, not an assumption that either endpoint vector is already normalized.

Before constructing the chosen proxy, tighten every coordinate using the ORIGINAL totals and endpoints:

    a_i = max(l_i, 1-(U0-u_i)),
    b_i = min(u_i, 1-(L0-l_i)).                            (E3)

Every original feasible P satisfies these inequalities, since P_i=1-sum_(j!=i)P_j. Conversely [a_i,b_i] is contained in [l_i,u_i]. Thus replacing all intervals by (E3) preserves E exactly. In particular the tightened envelope is nonempty whenever (E2) holds. This is a simultaneous single pass, with no order-dependent iterative rule. There is no clipping of invalid original endpoints or renormalization of an infeasible envelope.

Write

    L = sum_i a_i,  U = sum_i b_i,
    A = 1-L,       B = U-1,       S = U-L = A+B,
    s_i = b_i-a_i.                                        (E4)

These quantities are nonnegative except that L,U are totals; L<=1<=U and sum s_i=S. If S=0, set q_i=a_i and eta=0. This handles exact rows and normalization-forced singleton envelopes without division by zero.

## 3. Deterministic construction and a useful TV bound

For S>0 define

    t = A/S,
    q_i = a_i + t s_i,
    eta = A B / S = t(1-t) S.                             (E5)

Then 0<=t<=1, a_i<=q_i<=b_i, and sum q_i=L+tS=1. The construction is exact rational and deterministic in the supplied order. Zero-width coordinates keep their exact values. If a_i=b_i=0 then q_i=0 and the outcome is retained. There is no tie choice, endpoint search or estimated normalization.

To prove (E1), take any real P in E and put x_i=P_i-a_i. Then 0<=x_i<=s_i and sum x_i=A=tS. For s_i>0, the chord bound for the convex absolute-value function gives

    |x_i-t s_i| <= (1-x_i/s_i)t s_i
                    +(x_i/s_i)(1-t)s_i
                 = t s_i + (1-2t)x_i.                    (E6)

For s_i=0 both sides are zero. Summing (E6) gives

    sum_i |P_i-q_i| <= tS + (1-2t)tS = 2t(1-t)S.

Half this sum is TV on a complete finite probability space, proving (E1) with (E5). The proof includes t=0 and t=1; those cases have zero error. Also eta<=min(A,B)<=1, since A<=1. No floating-point estimate or numerical optimization is used.

This bound uses normalization beyond the naive sum of coordinate errors. It is no larger than either total one-sided slack A or B and no larger than the independent-coordinate bound (1/2)sum_i max(q_i-a_i,b_i-q_i)=max(A,B)/2. Indeed AB/(A+B)<=min(A,B) and AB/(A+B)<=max(A,B)/2. Tightening (E3) can improve the bound further, though no monotonic comparison between different chosen proxies is asserted.

Neither minimax optimality of q nor sharpness of eta for every envelope is claimed. For example, intervals [0,1/5], [0,9/10], [0,9/10] give q=(1/10,9/20,9/20) and eta=1/2. For that q the exact worst TV is only 9/20: in three outcomes each event is a singleton or its complement, and the maximum singleton deviations are 1/10, 9/20, 9/20. The point (1/10,9/10,0) attains 9/20. A failed budget test with this bound therefore does not prove that no smaller valid bound or different proxy exists. No extra optimization/search procedure is required by this design.

## 4. Exact integer recipe and proposed API contract

This section specifies a possible future implementation; no such implementation is provided here. A conceptual call is

    proxy_envelope(ordered_outcomes, lower, upper, proxy_budget, resource_limits).

Inputs are exact rationals (plain integers or reduced Fraction-style numerator/denominator pairs), not floats, rounded decimals, strings interpreted as approximations, booleans or implicit numeric adapters. The ordered outcome identifiers must be distinct; their completeness and scientific meaning are external premises. The finite lists must have matching lengths. The optional budget tau=proxy_budget is a predeclared exact rational in [0,1]; it is an allowance to check, not an inferred scientific threshold.

One explicit construction uses a common denominator D, the least common multiple of all original endpoint denominators. Set ell_i=D*l_i and v_i=D*u_i. These are integers. Check (E2) in integer form. Calculate the tightened integer endpoints

    alpha_i = max(ell_i, D-(sum_j v_j-v_i)),
    beta_i  = min(v_i, D-(sum_j ell_j-ell_i)).

Let M=sum alpha_i, V=sum beta_i, a=D-M, b=V-D, s=V-M and sigma_i=beta_i-alpha_i. If s=0, return q_i=alpha_i/D and eta=0. Otherwise reduce the following exact rational values:

    q_i = (alpha_i*s + a*sigma_i)/(D*s),
    eta = a*b/(D*s).                                      (E7)

The output record should retain the ordered outcome list, original and tightened endpoints, q, eta, totals or integer witnesses needed to recompute (E7), exact budget comparison, endpoint-provenance reference and resource disposition. Exact rationals are serialized as integer numerator/positive denominator pairs, never silently rounded down for a comparison. A producer must label the claim as conditional on endpoint validity and completeness.

The proposed bounded profile accepts 1..256 outcomes and endpoints/budget with reduced numerator and denominator sizes at most 256 bits. These are resource limits, not mathematical assumptions of (E1). Reject invalid types, empty/mismatched/duplicate lists, negative/inverted/out-of-[0,1] endpoints, or an invalid budget. If (E2) fails, report INFEASIBLE_ENVELOPE; do not rescale endpoints, drop coordinates, or construct a purported normalized target.

A future consumer may use q in the existing categorical-map module only if its reduced weights also meet that module's 256-bit numerator/denominator limits. Input endpoints meeting 256-bit limits do not guarantee this output property. If the exact proxy exceeds the consumer's bounds, report ABSTAIN_RESOURCE, preserving the conditional mathematical result when available. No uncharged truncation or substitute proxy is licensed.

If eta>tau, report ABSTAIN_BUDGET for this certificate, not a statistical FAIL or proof of intrinsic impossibility. If eta<=tau and the exact arithmetic/consumer limits pass, the arithmetic output is a CONDITIONAL_PROXY_CERTIFICATE, not a benchmark PASS. Missing or invalid external endpoint provenance still makes operational admission ABSTAIN. Implementation failure, exhausted resources or incomplete arithmetic likewise cause ABSTAIN without a partial certificate being treated as complete.

## 5. Cost, precision and tiny allowances

The construction requires O(m) exact gcd/lcm, arithmetic and comparison operations and O(m) stored numbers. This is not an O(m) bit-time claim. If each endpoint denominator has at most K bits, D has at most the sum of their bit lengths, at most 2mK. All cumulative integer sums are at most mD; the unreduced numerators and denominators in (E7) are at most mD^2. A conservative preflight bound of

    2 * (sum of original denominator bit lengths)
        + ceil(log2(max(m,1))) + 4

bits covers the envelope-construction intermediates only, including gcd/lcm multiplication before reduction. Call this bound C. With m,K<=256, C is at most 262,156 bits. Exact output storage can require O(m^2 K) bits. These finite bounds do not supply measured preparation cost, certify a particular runtime, or price endpoint generation as free.

A separately supplied budget tau can require larger operands even when the envelope has small denominators. Write tau=n_tau/d_tau in reduced form and let K_tau=max(bit_length(n_tau),bit_length(d_tau))<=256. To compare reduced eta=n_eta/d_eta with tau, form n_eta*d_tau and n_tau*d_eta. The conservative bound C_compare=C+K_tau+1 covers the budget operands and these comparison products; its stated-profile maximum is 262,413 bits. A future implementation must admit both the envelope-construction and budget-comparison precision/memory bounds, or report ABSTAIN_RESOURCE before exceeding either. The construction bound C alone does not cover an arbitrary budget comparison. Later categorical-map or protocol arithmetic remains subject to its own separate resource limits.

The zero budget tau=0 is legitimate: it passes only when the computed eta is zero. A tiny positive budget is compared exactly; it is never treated as zero or given a numerical tolerance. More held-out draws do not repair an excessive proxy bias.

For a prospective total complete-row allowance E and independently certified bit error epsilon, the remaining map-rounding allowance would be delta=E-eta-epsilon. If delta<0, this composition does not certify E. If delta=0, the map must have exact gamma=0. If delta>0, the map's general bound gamma<m/2^(k+1) supplies a sufficient prospective bit width satisfying m/2^(k+1)<=delta; the exact computed gamma may allow a smaller width. Any chosen k must still meet the existing map's 0..256 limit and the frozen resource budget. No width search, actual draw, or automatic increase in sampling is authorized here.

## 6. Composition and the external conditional premises

Fix the envelope and q before held-out outcomes. Let T be the reviewed total k-bit categorical map, p its law under a uniform k-bit word, and gamma=TV(p,q) its exact rounding certificate. Suppose a separately certified consumed bit-block law R satisfies

    TV(R, Uniform_k) <= epsilon

conditional on the full relevant history and valid return, on the optional protocol's preflight good-certificate event. Deterministic mapping contracts TV; for every target P in the certified envelope,

    TV(T_*R,P) <= min(1, epsilon + gamma + eta).            (E8)

Thus one may choose e_a=min(1,epsilon_a+gamma_a+eta_a) in the optional protocol, given the constituent certificates. A channel discrepancy c_a remains separate, so its bias allowance is b_a=min(1,e_a+c_a). The required B=b_Q+b_B<d/2, certificate/availability budgets, alpha=beta=1/20, fixed sample count, threshold and held-out failure rules are unchanged. There is no numerical d or feasible sample count here.

Endpoint validity is required simultaneously on the declared good-certificate event. If interval producers instead provide probabilistic coverage bounds, their failure risks must be justified for the full frozen selection and combined with other certification risks. A union bound can sum valid coordinate/arm failure allowances without independence; it does not manufacture valid individual allowances, conditional validity or simultaneous coverage from uncalibrated intervals. Certification-failure probability belongs in the protocol's explicit risk budget, not silently in eta. Deterministic exact endpoints alone do not imply that their scientific provenance has zero failure risk.

For a fixed target row, a simultaneous preflight envelope is enough for the algebraic q-versus-P claim; the bit-source/channel certificates still must hold conditional on the complete history across both arms and on valid return. If the target or envelope is history-dependent, an applicable certificate must cover every reachable relevant history with the required uniform bounds and frozen algorithm. This design does not authorize changing the target, choosing intervals from held-out successes, favorable retries or post-selection. Marginally accurate bits and a PRNG name do not meet the conditional premise. The alternative whole-attempt TV route still requires its own joint certificate; (E8) alone is not one.

No operational failure-rate bound is supplied. The optional design's distinction between wrong-terminal-decision guarantees and power counting ABSTAIN remains: a full non-PASS bound requires its declared availability/failure allowance. Frozen exact D4-A is not satisfied or retroactively amended by any approximate certificate.

## 7. Recomputable rational examples

These are invented finite arithmetic examples, not native coefficients, interval data, sampled outcomes or held-out benchmarks. Bounded exact-arithmetic checks verify the displayed values directly, without importing the categorical-map implementation or implementing this proposed API.

**A. Feasibility, tightening, proxy and map composition.** Take l=(1/5,1/10,0), u=(3/5,1/2,1/5). The original totals are 3/10 and 13/10. With D=10, tightened endpoints are alpha=(3,2,0), beta=(6,5,2). Thus M=5, V=13, a=5, b=3, s=8 and sigma=(3,3,2). Equation (E7) gives

    q = (39,31,10)/80,
    eta = 15/80 = 3/16.

The feasible point P=(3/5,1/5,1/5) differs from q by (9,-15,6)/80, so its TV is 15/80: this example attains the bound. At three map bits, N=8, the scaled proxy counts before rounding are (39/10,31/10,1). Largest remainders give counts (4,3,1), so p-q=(1,-1,0)/80 and gamma=1/80. If, hypothetically, a separately valid conditional bit certificate gave epsilon=1/100, (E8) would give e<=3/16+1/80+1/100=21/100. No such bit-source certificate is asserted to exist.

**B. Zero-width and zero-probability entries.** For intervals [0,0], [2/5,2/5], [3/5,3/5], S=0 and q=(0,2/5,3/5), eta=0. All three outcomes remain. For [0,4/5], [1,1], normalization tightening collapses the first interval to [0,0]; the only feasible row is q=(0,1), again eta=0.

**C. Tiny budgets.** Let z=1/1,000,000 and use two intervals [1/2-z,1/2+z]. They remain unchanged by (E3). L=1-2z, U=1+2z, A=B=2z, S=4z; hence q=(1/2,1/2) and eta=z. Budget tau=z passes exactly; tau=z/2 does not certify this proxy uniformly. The feasible endpoint row (1/2+z,1/2-z) has TV=z, whereas the center itself has TV zero. At z=0 use the S=0 branch. No finite-precision tolerance is needed.

**D. Impossible envelopes.** Lower endpoints (3/5,3/5) have total 6/5>1, even with upper endpoints (4/5,4/5). Conversely upper endpoints (2/5,2/5) have total 4/5<1, even with zero lower endpoints. Both are infeasible; neither is repaired by endpoint normalization.

The non-sharp envelope example in section 3 is checked separately. These arithmetic checks substantiate the examples only; the all-P statement rests on the proof, and applicability to a scientific row rests on the missing external certificate.

## 8. Completion and remaining premises

This design closes a finite mathematical question: feasibility, a deterministic rational proxy construction, and a universal-in-the-envelope TV allowance can be obtained without acquiring target coefficients or running a sampler. An implementation, independently established complete native probability intervals and their provenance, a valid conditional bit source/channel, a certified numerical effect, feasible costs/failure treatment and held-out freeze remain separate missing inputs. No native-row acquisition, scientific sampling, observed-data result, measured failure rate, application advantage, physical observation, production qualification, or new DET claim follows.

The dependencies are the [categorical-map note](CATEGORICAL_MAP.md), [optional approximate protocol](APPROXIMATE_WIDTH_DIAGNOSTIC.md) and [exact width diagnostic](WIDTH_DIAGNOSTIC.md). Exact private source correspondence and arithmetic receipts remain withheld under the [publication evidence boundary](PUBLICATION_NOTE.md). Existing scientific inputs, diagnostic conditions, historical custody failures and the RET-only pause are preserved. This prospective contract supplies no authorization or result for a sampling run.


## Complete-row admission boundary

The [prospective admission design](ENVELOPE_ADMISSION.md) binds endpoints and
simultaneous coverage to the declared law, parent, sector, old marking and
complete ordered row. The frozen diagnostic uses eleven ideals and twenty-two
marked outcomes; the distinct eight-ideal P4 theorem cannot substitute for it.
Structural checks do not establish mathematical validity or authenticity.
No adapter, native interval certificate or operational admission is supplied.
