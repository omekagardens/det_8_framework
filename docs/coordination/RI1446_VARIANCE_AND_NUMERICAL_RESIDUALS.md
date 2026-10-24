# RI1446: Variance and numerical residuals

Two independently reviewed, root-accepted conditional results are presented here. A scalar variance test excludes no admitted parameter. Separately, certified local residuals would bound a finite reference filter's error against its ideal output. Neither supplies a physical observer, validates the other track or authorizes execution.

## 1. The finite family and the hypothetical extension

Let P_t be the admitted completed anonymous four-order law, with fixed parameter t in the open interval I=(-1/18,2/3). Admission concerns the fixed-seed, mark-independent, scalar-passive family with positive complete birth rows, proper-precursor mark locality with whole-unmarked-parent access, equivariance, fair immutable bits and complete marked incomparable-birth diamonds. These are finite growth premises, not an all-horizon construction or an observation apparatus.

The pair-chain probability is p=1/2. The triple law on antichain A, one edge plus isolate E, fork V, join W and chain C is

    m(A,E,V,W,C) = (1,6,2,1,2)/12.

For X=C2 disjoint-union C2, Y=C3 disjoint-union C1 and Z=C4, the only changing terminal probabilities are

    P_t(X)=19/81+t/6,
    P_t(Y)=4/27-2t/9,
    P_t(Z)=1/324+t/18.

Here Cj denotes a j-chain, with no comparisons between disjoint components. Every other terminal weight is fixed. The three displayed weights have total 125/324; unchanged worlds have total 199/324. Their signed change is (t-s)(3 delta_X-4 delta_Y+delta_Z)/18. The accepted finite family and observation boundary are also described in [RI1444](RI1444_OBSERVATION_AND_FILTERING_BOUNDARIES.md); the moment inputs and proof needed here are given below.

Fix t. For an integer N>=4, suppose a random completed N-order exists whose uniform induced four-order has law P_t. This is the hypothesis being tested, not a claim of existence. Successive uniform restriction gives the stated pair and triple laws. Independently give each realized order a conditional uniform random bijective labeling by 1,...,N; these auxiliary labels are not birth times. Set

    X_ij = 1{ i and j are comparable in the completed relation },
    S_N = sum_(i<j) X_ij,
    eta = E[X_12 X_13],   theta = E[X_12 X_34].

Deleting vertices retains existing completed comparisons. Relabeling gives common moments within overlap classes; it does not make indicators independent. Formal restriction and labeling assert no physical selection or readout.

## 2. Exact scalar variance and the complete disjoint moment

Expanding variance over unordered pairs of vertices gives

    Var(S_N) = C(N,2)p(1-p)
             + 6 C(N,3)(eta-p^2) + 6 C(N,4)(theta-p^2).

There are C(N,2) diagonal terms, 3 C(N,3) unordered pairs of distinct edges sharing a vertex, and 3 C(N,4) unordered disjoint edge pairs. Off-diagonal covariance contributes a separate factor two. These classes exhaust the expansion, and X_ij squared equals X_ij.

The triple types have j=0,1,2,2,3 comparable pairs. Of their three overlapping edge pairs, C(j,2) have both edges comparable. Thus

    eta = [(2/12)+(1/12)+3(2/12)]/3 = 1/4 = p^2.

This zero overlap covariance does not imply joint independence. Also E[S_N]=C(N,2)/2.

For a four-order Q, let M(Q) count perfect matchings whose two pairs are comparable. Uniform labeling makes 12|34 uniform among the three matchings, so theta=E[M]/3. The actual three-parent weights are

    mu_3(A,E,V,W,C)=(1/12,1/2,1/6,1/12,1/6).

Take E as x<y with isolate z; V as x<y,x<z; W as x<z,y<z; and C as x<y<z. A fourth maximal birth v above ideal S has matching count

    d(P,S)=M(P+v_S)
          =sum_(u in S) 1{the two old vertices other than u are comparable}.

Every matching pairs v with exactly one old vertex u. The displayed condition is therefore necessary and sufficient for that matching, and counts it once. For A every count is zero; for E only u=z contributes; for V either leaf contributes; for W either bottom contributes; for C each old vertex contributes.

The full ideal-class list, with the full ideal last, is:

| Parent | Ideal classes | Matching counts per occurrence | Conditional mean of M |
| --- | --- | --- | ---: |
| A | empty; singleton x3; pair x3; full | 0,0,0,0 | 0 |
| E | empty; x; z; xy; xz; full | 0,0,1,0,1,1 | 5/9+t/3 |
| V | empty; root; root-plus-leaf x2; full | 0,0,1,2 | 26/27 |
| W | empty; bottom singleton x2; bottom pair; full | 0,1,2,2 | 44/27 |
| C | empty; x; xy; full | 0,1,2,3 | 73/54+t |

These are 22 classes representing 28 actual occurrences (8,6,5,5,4). Each repeated occurrence has the displayed count. The admitted per-occurrence probabilities give the complete nonzero contributions:

    E: (38/81+t/3) + 1/27 + 4/81 = 5/9+t/3,
    V: 2(2/9) + 2(7/27) = 26/27,
    W: 2(2/27) + 2(1/9) + 2(17/27) = 44/27,
    C: 2/9 + 2(29/54) + 3(1/54+t/3) = 73/54+t.

Zero-count branches stay in the normalized rows and contribute zero to this moment. Full-ideal branches are included. The two fair newborn-bit probabilities sum q/2+q/2=q, with no extra mark or automorphism factor. Actual parent weighting yields

    E[M] = (1/2)(5/9+t/3)+(1/6)(26/27)
         + (1/12)(44/27)+(1/6)(73/54+t)
         = 259/324+t/3,
    theta(t) = 259/972+t/9.

This includes every incoming transition. Independently, X,Y,Z have M=1,0,3 and theta kernels 1/3,0,1, giving slope t/9. Their absolute contribution is 79/972+t/9; unchanged worlds contribute the essential remaining 180/972=5/27. Dropping that constant tests the wrong law.

## 3. Necessary inequalities, with no excluded parameter

Substitution gives the required variance of any hypothesized extension:

    Var(S_N)=C(N,2)/4+6 C(N,4)(theta(t)-1/4).

For integer N>=4, nonnegativity and C(N,4)>0 imply

    theta(t) >= 1/4 - C(N,2)/(24 C(N,4))
             = 1/4 - 1/[2(N-2)(N-3)].

For this fixed t, existence of extensions at unbounded sizes forces theta(t)>=1/4 by taking the limit of these necessary inequalities. No coupling of the proposed sizes or infinite exchangeability representation is needed for that implication. The denominator formula is not used at N<4.

For the admitted open interval,

    253/972 < theta(t) < 331/972,
    5/486 < theta(t)-1/4 = 4/243+t/9 < 22/243.

Every admitted t passes both the finite-size and limiting inequalities strictly. This scalar total-count variance test excludes none. At N=4 it gives Var(S_4)=259/162+2t/3. The changing X,Y,Z have comparable-pair counts 2,3,6, so their second-moment change is t(3*4-4*9+36)/18=2t/3, agreeing with that slope while the mean stays fixed. The candidate variance is positive for N>=2 and zero for N=1, using the admitted lower marginals at small sizes.

Passing this test proves no larger extension. It certifies neither all covariance or distribution constraints nor a fifth-birth law, all-horizon sampling consistency or native continuation. Incomparable-birth diamonds govern alternative growth routes; uniform induced-subset laws are a different requirement. The accepted missing joint-selector and physical-readout premises remain missing.

## 4. The separate reference-filter target

Fix a finite record length N>=2, fixed finite section coefficients (b0,b1,b2,a0,a1,a2), a0=1, and exact d=a0+a1+a2!=0. Let g=(b0+b1+b2)/d. Fix section/stage order and integer padding 0<=p_s<N-1. The admitted recipe has 17 stages: four sections with padding 27, then sixteen single-section stages with padding 9; thus N>28. Coefficient identity and nonzero exact denominators are premises, not newly evaluated facts. Zero gains are allowed.

Define T_N by exact arithmetic using the source's finite prescription. At each stage extend w by the left coordinates 2w_0-w_r for r=p,...,1, then w, then right coordinates 2w_(N-1)-w_r for r=N-2,...,N-p-1. The length is L=N+2p. In a pass starting from z, set h_0=z_0 and h_j=g_j h_(j-1). Section j starts with x_-2=x_-1=h_(j-1) and y_-2=y_-1=h_j, then computes

    y_t=(b0 x_t+b1 x_(t-1)+b2 x_(t-2)
         -a1 y_(t-1)-a2 y_(t-2))/a0,   0<=t<L.

The first section uses the pass input; later sections use the preceding section's outputs. Propagated constant prehistory is not its first computed output. Apply this ordered cascade, reverse its complete output, apply a newly initialized cascade in the same section order, reverse again and crop [p,L-p). Repeat stages. At p=0 extension and crop are identities. This exact finite operator is linear by section/time induction; rounded executables are not certified exactly linear.

Hats below mean exact real values of finite stored numbers in a hypothetical successful source-bound rounded run. A signed local residual is stored result minus the exact operation on its actual stored operands. Supply certified finite nonnegative bounds on these residuals and any input/state/output discrepancies. Copies, indices, reversal and crop must be exact selections or have their discrepancies charged. All required nodes and operands must be finite and present. No relative-error model is assumed.

## 5. Gains, padding and propagated histories

For n=b0+b1+b2 and d=a0+a1+a2, the source forms each sum left-associatively with two additions. Let r_n and r_d be the respective sums of signed addition residuals, and r_q=hat g-hat n/hat d. Then

    hat n=n+r_n,   hat d=d+r_d,
    hat g-g=r_q+(r_n-g r_d)/hat d,
    Gamma=Q+(Nerr+|g| Derr)/|hat d|

bounds |hat g-g| when Q,Nerr,Derr bound |r_q|,|r_n|,|r_d|. The identity uses n=g d. The rounded denominator must be nonzero; its actual magnitude or a certified positive lower bound is required. Nonzero exact d alone is insufficient. Reuse of the prepared gains needs no independence assumption.

If e_i bounds the current stage-input discrepancy, each padded coordinate has bound 2e_endpoint+e_r+pi_r, where pi_r bounds the sum of the product-by-2 and subtraction residual magnitudes for that occurrence. Central coordinates retain e_i. No multiplication is presumed exact just because its multiplier is an integer; at p=0 there are no padding residuals.

For pass input bounds f_t, put H_0=f_0. Let mu_j=hat h_j-hat g_j hat h_(j-1) be the actual prehistory-product residual. If |mu_j|<=M_j, then

    H_j=|g_j|H_(j-1)+Gamma_j|hat h_(j-1)|+M_j

bounds |hat h_j-h_j|. This follows by subtracting the ideal product and adding/subtracting g_j hat h_(j-1). Actual rounded prehistory magnitudes, or certified upper bounds, are needed. Literal copies give initial error bounds H_(j-1),H_j. If actual initial states differ, add supplied A^x_-k and A^y_-k bounding their discrepancies from those rounded histories, k=1,2. These A terms are zero only when the source-copy premise holds.

## 6. Local recurrence residuals and finite composition

At time t let m0,...,m4 be the stored products of b0,b1,b2,a1,a2 with hat x_t,hat x_(t-1),hat x_(t-2),hat y_(t-1),hat y_(t-2), respectively. Let u0,...,u4 be their signed residuals. The source association is

    s1=round(m0+m1),  s2=round(s1+m2),
    s3=round(s2-m3),  s4=round(s3-m4),
    hat y_t=round(s4/a0).

Let v1,...,v4 be these addition/subtraction residuals and q the division residual. Naming products does not change evaluation order or assert fused arithmetic. Substitution gives the rounded-operand recurrence plus aggregate defect

    r_t=(u0+u1+u2-u3-u4+v1+v2+v3+v4)/a0+q.

The feedback multiplication defects carry minus signs; subtraction-operation defects enter positively. If U_i,V_i,Q_t bound the corresponding absolute residuals, a sufficient bound is

    Lambda_t=(sum_(i=0..4)U_i+sum_(i=1..4)V_i)/|a0|+Q_t.

A directly certified aggregate bound is also sufficient. Division by a0=1 remains charged unless its exactness is justified.

Within a section, let X_t bound the input error, using f_t for the first section and preceding-section output bounds thereafter. Initialize

    X_-k=H_(j-1)+A^x_-k,   Y_-k=H_j+A^y_-k,   k=1,2,

and define for 0<=t<L

    Y_t=(|b0|X_t+|b1|X_(t-1)+|b2|X_(t-2)
         +|a1|Y_(t-1)+|a2|Y_(t-2))/|a0|+Lambda_t.

Subtracting the exact recurrence from the rounded-operand identity and applying triangle inequalities proves the bound by time induction, then section induction. This is additive-error propagation, not an assumption that the rounded program is linear.

Start with c_i>=|hat x_i-x_i|. Exact conversion of the same admitted finite nominal binary64 inputs to Decimal gives c_i=0; it does not certify physical quantization. Propagate padding and forward-pass bounds, reverse the complete error vector, and perform a new backward-pass construction using the reversed actual forward output's first sample. Recompute prehistory-product and recurrence residuals; use the same prepared gain bounds and section order. Reverse, crop and repeat all stages. No interstage Decimal-to-binary64 conversion occurs in this reference prescription.

If E_i are the final component envelopes, supply sigma_i>=|hat y_i^store-hat y_i^ref| for final conversion/storage. Then

    |hat y_i^store-(T_N x)_i|<=E_i+sigma_i,
    eta_W=sqrt(sum_(i in W)(E_i+sigma_i)^2)

is a sufficient window 2-norm discrepancy bound. Sigma is zero only if returned numeric values are retained exactly. All input, state, arithmetic and output discrepancies zero imply zero error. Finite recursion with finite bounds and the stated nonzero denominators gives a finite exact-real envelope, without stability, tightness or useful-magnitude claims.

## 7. Evidence still needed and preserved gates

No trace, residual values, operand envelopes or numerical certificate is supplied. A valid application needs complete source/runtime/context, coefficient/order/length binding, finite successful operations and justified bounds at every required occurrence, plus validated exact or outward arithmetic for computing the certificate. Decimal precision 80 and final finiteness do not establish these premises. Finite exponent limits, InvalidOperation/DivisionByZero/Overflow traps, underflow and cancellation cannot be ignored. Absolute residuals allow rounding to zero; trapped, nonfinite, missing or incomplete nodes invalidate a certificate.

This proof concerns the reference's direct-form-I graph. Production SciPy sosfiltfilt need not use that graph; its internals are not certified here. It needs its own source/trace error argument or an independently certified same-input discrepancy D_W from the same reference-output representation, after which eta_W^prod<=D_W+eta_W^ref. Pairwise fixture agreement alone supplies no ideal-reference error bound.

With separately justified full-record input error rho, ideal operator bound kappa_W and numerical envelope eta_W, the earlier conditional transfer is epsilon_W=(kappa_W rho+eta_W)/sqrt(n_W). No actual values or coverage are asserted. The fixed 17-window nominal contrast, strict comparison, first maximum and zero-baseline ABSTAIN remain unchanged. No new calibration or trace prerequisite is added to that nominal-only statistic.

E still needs the actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE needs actual source/reset/control/readout transfer and history-wise certificates in both candidate worlds, including full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains packing/general serialization, source/build/ABI/binding, resource/control/qualification and observed-execution holds. The native joint observation kernel, physical preparation/readout, nondisturbance, calibration and action/reset costs remain separate missing inputs.

RI1445 and M-F009 are accepted only at the scopes proved above. No unreviewed successor is included. Root separately reports checking all 27 nonself members of the four author/reviewer packets; this publication preparation verifies only its literal granted inputs and does not recheck ungranted nested members. Current hashes establish present identity, not historical custody or completion. Missing evidence, late readbacks/freezes, draft-cap and display/schema/wrapper/patch/TextEncoder failures remain qualified; attributed final completion times are not reconstructed from current bytes.

Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% usage guard and RET-only pause persist. Publication is not execution. No physical validation, all-horizon existence, empirical significance or release receipt is supplied.
