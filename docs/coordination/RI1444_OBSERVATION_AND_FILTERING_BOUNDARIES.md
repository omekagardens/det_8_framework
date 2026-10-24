# RI1444: Observation and finite-filtering boundaries

Two separately reviewed, root-accepted results are consolidated here: a joint-selector counterexample and an exact-real finite filtering bound. Both remain conditional mathematics. Neither derives physical readout, calibrates an instrument, authorizes execution or validates the other track.

## 1. A fixed finite observation family

Let \(P_t\), \(t\in I=(-1/18,2/3)\), be the accepted completed anonymous four-order family. Its fixed-seed, mark-independent, scalar-passive admission assumes positive complete birth rows, proper-precursor mark locality with whole-unmarked-parent access, equivariance, fair immutable bits and complete marked incomparable-birth diamonds. These constrain the supplied growth maps. They do not prescribe an observer's subset choices.

Finite admission is inherited from the fixed family in [RI1442](RI1442_REPEATED_TRIPLE_OBSERVATION.md), not extended beyond four births or classified anew. The following accepted probability premises completely specify the inputs needed for this audit.

With \(C_j\) a \(j\)-chain and \(\sqcup\) disjoint union without cross-comparisons, exactly three world weights vary:
\[
\begin{aligned}
X=C_2\sqcup C_2 &: P_t(X)=19/81+t/6,\\
Y=C_3\sqcup C_1 &: P_t(Y)=4/27-2t/9,\\
Z=C_4 &: P_t(Z)=1/324+t/18.
\end{aligned}
\]
These weights are positive on \(I\), sum to \(125/324\), and all other weights are individually fixed with total \(199/324\). Hence
\[
P_t-P_s=\frac{t-s}{18}(3\delta_X-4\delta_Y+\delta_Z).
\]

For a fixed world \(Q\), let \(K_Q\) be the law of the anonymous induced completed order on one uniform three-vertex subset. There are four such subsets. Let \(A,E,V,W,C\) denote respectively the antichain, one edge plus an isolate, one bottom below two tops, two bottoms below one top, and three-chain. The accepted one-triple marginal is
\[
\sum_QP_t(Q)K_Q=m,\qquad
m(A,E,V,W,C)=(1,6,2,1,2)/12
\]
for every \(t\). Put \(e=\delta_E,c=\delta_C\). Then
\[
K_X=e,\qquad K_Y=(3e+c)/4,\qquad K_Z=c.
\]
These kernels follow by deleting each vertex: all X triples are E; three Y triples are E and one C; all Z triples are C. Restriction retains completed comparisons even when a chain's middle vertex is omitted.

## 2. Uniform marginals leave the coupling unspecified

Passive access returns selected content and induced completed order without changing committed history or residual state. A view need not be past-closed. Residual transformation and new receipt/commitment are separate operations; a returned view is no physical interaction certificate.

Commitment validates an already selected positive branch, not sampling or a normalized instrument. Growth constraints and fair bits prescribe neither the bit-to-subset map nor successive-choice coupling. Birth precursors are ideals; views need not be. Scalar passivity is not physical nondisturbance.

For \(\mathcal S_3(Q)\), the four three-subsets of \(Q\), consider two mathematical extensions:
\[
S_Q^{\rm ind}(U,V)=1/16,\qquad
S_Q^{\rm reuse}(U,V)=\tfrac14\mathbf1_{\{U=V\}}.
\]
The first selects independently twice with replacement. The second selects one uniform subset and accesses it twice. Each law normalizes: sixteen terms of \(1/16\), or four diagonal terms of \(1/4\). Each row and column sums to \(1/4\), so both individual subset marginals are uniform. Relabeling permutes subsets and preserves equality, making both selectors equivariant. Growth positivity does not require positive probability for every observation pair.

For each protocol, first draw one \(Q\sim P_t\) and keep that same mathematical state throughout both accesses, without intervening residual transformation or commitment. Selector randomness is stipulated independent of growth. Report only ordered anonymous triple types, without identities, marks, payloads or overlap metadata. Both preserve history, order and residual state under passive-access semantics; neither supplies physical randomness or nondisturbance.

Replacement permits a repeated subset; it does not itself establish independence or require reuse.

## 3. Full normalized laws and the distinguishing calculation

The two output laws are
\[
J_t(u,v)=\sum_QP_t(Q)K_Q(u)K_Q(v),
\qquad
D_t(u,v)=\sum_QP_t(Q)K_Q(u)\mathbf1_{\{u=v\}}
=m(u)\mathbf1_{\{u=v\}}.
\]
The product in \(J_t\) occurs before averaging over the shared world. Each conditional kernel and \(P_t\) normalize, so both full output laws have mass one. \(D_t\) is the parameter-blind diagonal lift of \(m\): its entries on \(AA,EE,VV,WW,CC\) are \(1/12,1/2,1/6,1/12,1/6\), with all other cells zero.

In \(J_t\), the unchanged worlds contribute a common nonnegative measure \(B\) of mass \(199/324\), including possible mass on cells affected by the changing worlds. The latter contribute mass \(125/324\). Neither component is discarded or renormalized.

Subtracting full laws and expanding the four ordered cells gives
\[
\begin{aligned}
J_t-J_s
&=\frac{t-s}{18}\left[3e\otimes e
-4((3e+c)/4)^{\otimes2}+c\otimes c\right]\\
&=\frac{t-s}{24}(e-c)\otimes(e-c),\\
D_t-D_s&=0.
\end{aligned}
\]
The bracket coefficients on EE, EC, CE, CC are 3/4, -3/4, -3/4, 3/4. All other differences vanish; zero row/column sums preserve the marginal.

Use total variation as half the sum of absolute cell differences. For two fixed known hypotheses \(s,t\), equal priors, zero-one loss and a forced decision from one reported pair:

| Protocol | Total variation | Optimal equal-prior error |
| --- | ---: | ---: |
| Independent replacement from one fixed world | \(|t-s|/12\) | \(1/2-|t-s|/24\) |
| Reuse one subset of that world | \(0\) | \(1/2\) |

Indeed four absolute changes are \(|t-s|/24\), and the Bayes error is \(\frac12\sum\min(p,q)=(1-\mathrm{TV})/2\) for the full normalized laws. For distinct interior parameters, \(0<\mathrm{TV}<13/216\) and \(203/432<R^*<1/2\). Opposite excluded endpoints approach but do not attain those limits. Equal hypotheses give TV zero and error \(1/2\). These are average forced binary errors, not equal conditional errors, minimax/abstention guarantees or exact parameter recovery.

The two protocols differ at every admitted \(t\), not only between selected parameter pairs. On \(Y\), independent selection gives conditional \(EC\) probability \(3/16\), whereas reuse gives zero. Since \(P_t(Y)>0\),
\[
J_t(E,C)\ge (3/16)P_t(Y)>0=D_t(E,C).
\]
Nonnegative contributions from other worlds cannot cancel this witness.

A third experiment draws two independent new worlds, with independent selectors and growth draws under a fixed hypothesis \(t\). Its law is \(m\otimes m\), also parameter-blind. It differs from reuse: \((m\otimes m)(E,C)=1/12\), while \(D_t(E,C)=0\). Independent new-world preparation/reset is an additional premise. Conditional independence within one shared world does not justify multiplying averaged marginals.

Thus uniform marginals, equivariance and passive access do not derive the independent joint contract. Its conditional validity remains; neither universal information loss nor physical implementability follows.

## 4. The sufficient observation interface and physical gap

At the reported-output level, it suffices to supply
\[
O_Q(u,v)=K_Q(u)K_Q(v)
\]
for the same fixed \(Q\), with exact completed-order projection and ordered anonymous reporting. Averaging against \(P_t\) recovers \(J_t\). A stronger sufficient selection contract is probability \(1/16\) for every ordered subset pair, retaining the same sampled object without feedback altering it.

This sufficient interface is not a unique necessary or smallest-axiom theorem. Other selectors may share its anonymous pushforward. Reducing residual/controller/access-history dependence to this Q-kernel needs justification. Necessity for every distinguishing observer is not claimed.

Missing inputs remain: preparation mapped to P_t; actual source/control and joint selection; source-to-record readout, losses and receipts; relevant nondisturbance; calibration/inference to completed order; and full action/storage/latency/reset/resource costs. Software projection is no physical observation certificate. Option B/Status M persists.

## 5. The exact finite filtering operator

The second accepted result concerns a different mathematical object. Fix a record length \(N\ge2\). For each of the 17 ordered stages \(s=0,\ldots,16\), fix integer padding \(0\le p_s<N-1\) and finite section coefficients \((b_0,b_1,b_2,a_0,a_1,a_2)\), with \(a_0=1\) and exact \(d=a_0+a_1+a_2\ne0\). Define the exact DC gain
\[
g=(b_0+b_1+b_2)/d.
\]
A zero numerator/gain is allowed. The admitted recipe has four sections and padding 27 at stage 0, then one section and padding 9 at each remaining stage: 20 sections in total, requiring \(N>28\). The nominal H1 record has \(N=131072\).

Fixed binary64 coefficient values are treated as exact reals, without decoding or redesign here. Nonzero exact DC denominators remain premises: the prior exact audit is attributed, and rounded checks alone do not prove it. Finite bounds need no pole-stability assumption.

For \(v\in\mathbb R^N\), form the odd extension
\[
E_p(v)=(2v_0-v_p,\ldots,2v_0-v_1,\ v_0,\ldots,v_{N-1},
2v_{N-1}-v_{N-2},\ldots,2v_{N-1}-v_{N-p-1}).
\]
Its length is \(L=N+2p\); \(E_0\) is identity. Let \(R_L\) reverse coordinates and \(C_p\) select the half-open range \([p,L-p)\), with \(C_0\) identity.

Define one ordered cascade \(F_{s,L}\) on input \(z\in\mathbb R^L\). Suppress the stage index on section coefficients. Let \(G_0=1\) and \(G_j=\prod_{i=1}^jg_i\). For section \(j\), use \(x_t=z_t\) at the first section and the preceding section's output otherwise. Initialize
\[
x_{-2}=x_{-1}=G_{j-1}z_0,\qquad
y_{-2}=y_{-1}=G_jz_0.
\]
For \(t=0,\ldots,L-1\), compute in order
\[
y_t=\frac{b_0x_t+b_1x_{t-1}+b_2x_{t-2}
-a_1y_{t-1}-a_2y_{t-2}}{a_0}.
\]
After the last section return its \(L\) outputs. Propagated constant prehistory is not replaced by the preceding section's first computed output.

Composition is right to left:
\[
A_s=C_{p_s}R_LF_{s,L}R_LF_{s,L}E_{p_s},
\quad L=N+2p_s,\qquad T_N=A_{16}\cdots A_0.
\]
Both passes retain the same section order. The second pass starts from the reversed complete forward output and reinitializes from its first coordinate, using the same gain rule. Padding is removed after each stage. At \(p=0\), the explicit crop is \([0,L)\), not an empty \([0,-0)\). Later display/window selection is separate.

Extension, reversal and crop are linear. Initial states are fixed multiples of the first input coordinate; section/time induction makes each recurrence output linear, dividing only by fixed nonzero a0. Composition proves T_N linear, including initialization, zero input and superposition.

Neither executable is certified exactly linear. Decimal.from_float preserves binary64 values, but Decimal80 gain/state/recurrence operations and production binary64 operations round and can fail. SciPy internals were not inspected here. Fixture/tolerance agreement is not a uniform ideal-error enclosure.

## 6. A complete finite majorant

For stage \(s\), with \(m_s\) sections and pass length \(L\), retain its gains \(G_j\), and start \(U_0=1\). Define
\[
\begin{aligned}
P_j&=\max(U_{j-1},|G_{j-1}|),\\
\beta_j&=(|b_0|+|b_1|+|b_2|)/|a_0|,\qquad
\alpha_{j1}=|a_1|/|a_0|,\quad\alpha_{j2}=|a_2|/|a_0|,\\
q_{j,-2}&=q_{j,-1}=|G_j|,\\
q_{j,t}&=\beta_jP_j+\alpha_{j1}q_{j,t-1}+\alpha_{j2}q_{j,t-2},
\quad t=0,\ldots,L-1,\\
U_j&=\max_{0\le t<L}q_{j,t},\qquad H_s(L)=U_{m_s}.
\end{aligned}
\]
For \(\|z\|_\infty\le u\), \(u\ge0\), the preceding section's actual outputs are bounded by \(U_{j-1}u\), negative-time inputs by \(|G_{j-1}|u\), and initial output states by \(|G_j|u\). The maximum \(P_j\) covers every feedforward argument. Triangle inequality and time induction bound \(|y_t|\le q_{j,t}u\); section induction yields
\[
\|F_{s,L}z\|_\infty\le H_s(L)\|z\|_\infty.
\]
This includes zero gains and \(u=0\), and accounts for prehistory even when it exceeds actual preceding-section outputs.

Odd extension has sup-norm bound \(e_0=1\) and \(e_p=3\) for \(p>0\); reversal/crop have bound at most one. Apply the same pass estimate to the newly initialized backward input. Thus
\[
B_N=\prod_{s=0}^{16}\bigl[e_{p_s}H_s(N+2p_s)^2\bigr],
\qquad \|T_Nv\|_\infty\le B_N\|v\|_\infty.
\]
Every term is finite by finite recursion and the fixed nonzero denominators. No numerical value, tightness, useful magnitude, coefficient-uniform bound or infinite-horizon stability is asserted.

For a nonempty window of \(n_W\) coordinates, with selector \(P_W\),
\[
\|P_WT_Nv\|_2\le\sqrt{n_W}B_N\|v\|_\infty
\le\kappa_W\|v\|_2,\qquad \kappa_W=\sqrt{n_W}B_N.
\]
This is a conservative finite induced-norm bound, not a measured sensitivity.

## 7. Conditional transfer to the fixed nominal contrast

Let \(x\) be a nominal full record and \(x+v\) the target. Supply a justified finite \(\rho\ge0\) with \(\|v\|_2\le\rho\). For finite stored \(\widehat y\), also supply finite nonnegative \(\eta_W\) satisfying simultaneously
\[
\|P_W(\widehat y-T_Nx)\|_2\le\eta_W.
\]
The envelopes cover initialization, arithmetic, conversion and storage discrepancy; neither Decimal precision nor residual tolerances supplies them. Subtracting T_N x and using linearity and triangle inequality gives, for ideal target y'=T_N(x+v):
\[
\frac{\|P_W(y'-\widehat y)\|_2}{\sqrt{n_W}}
\le\epsilon_W=\frac{\kappa_W\rho+\eta_W}{\sqrt{n_W}}.
\]
Comparing two rounded outputs additionally requires the target implementation's discrepancy envelope. The displayed one-envelope result compares a stored baseline with an ideal target.

For the unchanged H1 statistic, each window has \(n=4096\). The event is \([65536,69632)\); comparisons are \([4096j,4096(j+1))\) for \(j=4,\ldots,11,20,\ldots,27\). Define \(a_W=\|P_W\widehat y\|_2/\sqrt n\) and
\[
\ell_W=\max(0,a_W-\epsilon_W),\quad u_W=a_W+\epsilon_W,\quad
E'_W=\|P_Wy'\|_2^2/n.
\]
Triangle and reverse-triangle inequalities give \(\ell_W^2\le E'_W\le u_W^2\). Therefore
\[
\max_j\ell_j^2>0,\qquad
\ell_{\rm event}^2>\max_j u_j^2
\]
suffice for valid strict contrast throughout this uncertainty set. Equality does not establish strict contrast. The fixed nominal rule keeps all 17 energies, the first maximizing comparison in ascending \(j\), and the ratio only for positive comparison maximum. A zero baseline or another failed mandatory gate requires ABSTAIN.

One full-record perturbation couples windows; product-ball sharpness or necessity does not transfer. Outside-window errors may affect the filtered window. No finite-support/independent-noise premise, actual rho/eta, observed energy or joint coverage is supplied. Physical calibration and a native detector map remain missing. No calibration prerequisite is added to the admitted nominal-only calculation.

## 8. Acceptance and remaining gates

RI1443 and M-F008 were independently reviewed and root-accepted only at these scopes. No unreviewed successor result is included.

E still requires an actual actuator/operator failure-state certificate and complete cost, latency and source-to-reset closure. NE still requires actual source/reset/control/readout transfer and history-wise certificates in both candidate worlds, with full costs. CE retains diagnostic-interface ownership, runtime/allocator/enforcer and hard-resource admission, with M1 held. Measurement retains the flat-record packing failure and unresolved general serialization contract, source/build/ABI/binding, resource/control/qualification and observed-execution prerequisites. No result here repairs another lane's operational gap or changes caps or targets.

Current hashes establish present identity, not historical custody/completion. Missing evidence, late freezes/readbacks and cap/display/schema/wrapper/patch/TextEncoder failures remain qualified. Final author completions remain attributed; write starts, declarations and current rereads do not repair history.

No all-horizon or physical/empirical claim follows. Protected validation/custody, Option B/Status M, ABSTAIN, zero qualification, the 10% guard and RET-only pause remain. Publication is not execution; no release receipt is supplied.
