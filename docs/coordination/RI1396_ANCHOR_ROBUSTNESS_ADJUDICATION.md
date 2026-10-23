# RI1396: Native anchors and finite-vector robustness

This checkpoint records five coordinator dispositions after separate author submissions and distinct reviews. It accepts conditional mathematics and identifies concrete design defects; it grants no scientific, operational, benchmark, hardware or protected-validation execution. Newly assigned questions below have no accepted results in this publication. No application success validates the physical theory.

## Native selected-family population anchors

The admitted construction has latent parameter theta supported on [0,1], with density dmu_sigma(theta)=(1+sigma h(theta)/642)dtheta, sigma in {-1,+1}, and h(theta)=70theta^4-140theta^3+90theta^2-20theta+1. For each fresh realization, sample theta from this law, independently sample forward edges with Bernoulli(theta), take transitive closure and forget labels. The exact chain event at size j has probability E_mu[theta^(j-1)]. This is a stipulated common-latent construction and selected pair of laws, not a universal principle forcing the seed, normalization or readout. Fresh preparation, known cardinality and cross-size response transfer are separate premises.

The following six sections reproduce the accepted RI1395 argument literally. The coordinator accepts its selected-family population-anchor proposition, finite-budget bound and no-uniform-slope limitation. Historical RI1389 author-artifact omissions remain unresolved; the present complete frozen RI1395 package does not reconstruct those artifacts or their custody.

## 1. Answer and admitted anchors

The selected admitted pair supplies two distinct known chain-population
means. It can replace RI1393's separately certified true-zero control
population by a size-two population with a known mean, provided a common
readout response transfers across cardinalities. That transfer and fresh
preparations are additional premises, not consequences of native admission.

In the captured RI1389 family, chain probability at size j is
\(\int\theta^{j-1}d\mu_\sigma(\theta)\). A chain needs its consecutive
forward edges; those edges suffice, irrespective of redundant edges.
For the accepted pair
\[
 d\mu_\sigma=(1+\sigma h/642)d\theta,\quad
 h=70\theta^4-140\theta^3+90\theta^2-20\theta+1,
 \qquad \sigma\in\{+1,-1\},
\]
the accepted moment identities give \(\int h=\int\theta h=0\) and
\(\int\theta^4h=1/630\). Therefore
\[
 a_1=1,\qquad a_2=1/2,\qquad a_{5,\sigma}=1/5+\sigma d,\qquad
 d=1/(642\cdot630)>0.                                               \tag{1}
\]
The size-one statement also follows from its unique singleton order.
For size two, \(\int\theta(1+\sigma h/642)d\theta=1/2\).
These are population probabilities under this selected pair, not a
universal DET mean or labels certifying individual size-two outcomes.
No size-minimality claim is made.

## 2. Added observation experiment and joint map

At each known true cardinality j in {1,2,5}, independently prepare fresh
from-empty realizations under one fixed unknown hypothesis. Redraw the
latent variable for every preparation; use independent conditional growth
and response randomness across all trials and batches. The observer
receives the cardinality and one reported bit Y per realization, not
the true chain bit B or latent parameter.

Explicitly assume one stable hypothesis-blind memoryless response
\[
 f=\Pr(Y=1\mid B=0),\quad t=\Pr(Y=1\mid B=1),\quad s=t-f,
 \quad (f,t)\in[0,1]^2,                                            \tag{2}
\]
identical at sizes 1,2,5. This includes conditional independence and
dependence only on B, not hidden order features. Cardinality is not time.
There is no physical reset, control source or readout implementation
asserted by these mathematical promises.

The three Bernoulli means are
\[
 q_1=t,\qquad q_2=(f+t)/2,\qquad q_5=f+s(1/5+\sigma d).              \tag{3}
\]
Thus the joint exact-law map identifies the response:
\[
 t=q_1,\qquad f=2q_2-q_1,\qquad S=2(q_1-q_2)=s.                    \tag{4}
\]
The interpolated size-five baseline and residual are
\[
 f+s/5=(8/5)q_2-(3/5)q_1,\qquad
 D=q_5-(8/5)q_2+(3/5)q_1=\sigma sd.                               \tag{5}
\]
These follow by substitution, including the signs of both coefficients.

If \(s\ne0\), \(D/S=\sigma d\), and \(\operatorname{sign}(DS)=\sigma\).
A negative slope reverses the sign of D but also of S; D alone cannot
orient the hypothesis without slope information. Equal joint triples
under competing responses force equal t and f by (4); with nonzero
slope they cannot arise under opposite hypotheses. Thus joint population
anchors resolve the offset alias that a size-five-only bit allowed.

If \(s=0\), all three means equal f=t, and their entire independent
product observation laws are identical under the two hypotheses.
The response remains identifiable from exact anchor laws, but the
hypothesis is not. Exact-law identification is not exact recovery from
finitely many observations.

## 3. A fully accounted finite-budget rule

Predeclare an integer n>=1 and collect n independent observations at
each size: total 3n trials. Let \(\widehat q_j\) be each sample fraction,
and form \(\widehat D,\widehat S\) by (4)–(5). The forced binary rule is
\[
 \text{choose plus if }\widehat D\,\widehat S\ge0;\quad
 \text{choose minus otherwise}.                                  \tag{6}
\]
It uses no known sign or offset, no division by a noisy slope, no
postselection and no estimated-parameter clipping.

For every fixed response with \(s\ne0\), either hypothesis has error
\[
 \Pr(\text{wrong})\le
 \min\{1,\;6\exp[-n s^2d^2/32]\}.                                 \tag{7}
\]
To prove it, take the analysis radius \(r=|s|d/8\). Each Bernoulli
sample mean has two-sided deviation bound \(2e^{-2nr^2}\). This follows
by centering its log MGF: value and derivative vanish at zero, its
second derivative is a tilted Bernoulli variance <=1/4, so the log MGF
is <=u^2/8. Independence and exponential Markov at u=±4r yield each
one-sided bound \(e^{-2nr^2}\). The union bound over three sample means
gives a simultaneous good event with complement <=\(6e^{-2nr^2}\).

On that good event,
\[
 |\widehat S-s|\le4r=|s|d/2,\qquad
 |\widehat D-\sigma sd|\le(16/5)r=(2/5)|s|d.                        \tag{8}
\]
Since 0<d<1, both estimated signs are strictly correct. Hence their
product has sign sigma, and no tie occurs there. All anchor-estimation
and test errors are included in the one complement event. This proves
(7), including the tie convention; independence between the contrasts
themselves is neither assumed nor needed.

For a predeclared nondegeneracy premise \(0<s_*\le|s|\le1\) and target
\(0<\alpha<1\), choosing
\[
 n\ge\left\lceil\frac{32}{s_*^2d^2}\log(6/\alpha)\right\rceil        \tag{9}
\]
gives a uniform error <=alpha. No numeric evaluation, practical power
claim or efficient sample-budget assertion follows. The lower bound
\(s_*\) is an external response premise, not supplied by the law anchors.
For each fixed nonzero s, (7) tends to zero with n even if its magnitude
was not known to the rule. This pointwise consistency is weaker than
uniform finite-budget separation.

## 4. Why nonzero slope alone gives no uniform budget

Consider the valid common responses
\[
 f_s=1/2-s/2,\quad t_s=1/2+s/2,\qquad 0<s\le1.
\]
Under plus and minus at the same response, the anchor laws coincide,
and the size-five means differ by \(2sd\). Couple each corresponding
size-five Bernoulli pair using the same uniform random variable. The
probability that the two bits differ is exactly \(2sd\); for n such
trials the probability of any difference is at most \(2nsd\).
Couple the anchor data identically. Therefore the total variation
distance of the entire data laws is at most \(2nsd\), capped by one.

For every randomized binary rule, its opposite error probabilities
sum to at least \(1-2nsd\): if its probability of choosing plus is a
function in [0,1], the difference of its expectations is bounded by
that total variation. As s decreases to zero, the sum approaches one.
Thus for each finite n, the supremum of the larger error over all
nonzero slopes is at least 1/2. Arbitrarily small nonzero s precludes
a uniform two-error guarantee below 1/2 with that budget. The same
argument uses the number of size-five observations for unequal
predeclared finite batch sizes. This is not an exact alias at every
nonzero s; it is an arbitrarily close alternative obstruction.

## 5. Optional confidence/abstention accounting

The forced rule above already accounts for all calibration uncertainty;
it has no abstention or calibration-success conditioning. If a different
reporting convention demands sign certificates, predeclare eta in (0,1)
and batch sizes \(n_j\), and let
\[
 r_j=\sqrt{\log(6/\eta)/(2n_j)},\quad
 e_S=2(r_1+r_2),\quad
 e_D=r_5+(8/5)r_2+(3/5)r_1.                                      \tag{10}
\]
Three two-sided bounds give simultaneous mean coverage >=1-eta.
Report the sign of \(\widehat D\widehat S\) only if
\(|\widehat S|>e_S\) and \(|\widehat D|>e_D\); otherwise abstain.
On the simultaneous coverage event every reported sign is correct.
Thus
\[
 \Pr(\text{wrong and report})\le\eta,\qquad
 \Pr(\text{wrong or abstain})\le\eta+\Pr(\text{abstain}),             \tag{11}
\]
with the latter capped by one. This is not an eta bound on error
conditional on reporting, and no lower report frequency is promised.
An interval excluding zero is statistical evidence, not a deterministic
native lower bound on |s|. Any use of it in later testing needs its own
coverage/failure accounting. The finite binary theorem (7)–(9) does
not require this optional reporting convention.

## 6. Exact obstruction when response transfer is dropped

If the response is allowed to vary with cardinality, its map is instead
\(q_j=f_j+(t_j-f_j)a_j\). The anchors identify neither f5 nor t5.
Even nonzero slopes at all sizes do not repair this.

In one plus world, use \((f_j,t_j)=(1/4,3/4)\) for all three sizes.
In a competing minus world, use the same response at sizes 1 and 2,
but use \((f_5,t_5)=(1/4+d,3/4+d)\). Every response is valid and has
slope 1/2. Both worlds give exactly
\[
                 (q_1,q_2,q_5)=(3/4,\;1/2,\;7/20+d/2).            \tag{12}
\]
Thus their entire joint independent observation laws agree at every
finite set of batch counts. All binary tests have opposite errors
summing to one at this pair. This is a cross-world nuisance comparison:
each actual apparatus would have its own fixed response-by-size function,
not a device told which hypothesis is true.

In this example the usual contrast would misleadingly indicate plus
in both worlds if cross-size transfer were assumed without justification.
Consequently the native population anchors do not validate response
transfer merely because the resulting observable triple fits the
common-response model.


## Finite-vector measurement robustness

The coordinator accepts the following deterministic theorem on supplied processed-window error envelopes. The author text is reproduced with the mixed-outcome statement explicitly restricted to C_min>0 and its former pending-review sentence updated to the actual disposition. Exact endpoint necessity holds over the unrestricted product of the disjoint window balls. Physically coupled subsets retain sufficient bounds but need not admit those witnesses. No actual radius, calibration coverage or native detector map is supplied. This result adds no prerequisite to the separately admitted nominal-only calculation.

## Fixed functional and premises

Let n=4096 and N=131072. In the fixed nominal record, event window W_0=[65536,69632) is second16. Comparison windows W_j=[4096j,4096(j+1)) use the fixed ordered list J=(4,5,6,7,8,9,10,11,20,21,22,23,24,25,26,27). These17 windows are disjoint. Every interval is half-open; no selection, delay, detector, filtering or threshold change is proposed.

For finite real window vector y_W in R^n, write E_W=||y_W||_2²/n and a_W=sqrt(E_W). Let C=max_{j in J}E_j, D=E_0-C and R=E_0/C only for C>0. With every existing input/quality/execution gate separately passed, the nominal rules remain CONTRAST_PRESENT for C>0,D>0; CONTRAST_NOT_PRESENT for C>0,D<=0; ABSTAIN_INVALID for C=0 or another failed gate. The first maximizing comparison is the smallest j. This theorem does not certify those non-arithmetic gates or an observed result.

Suppose an alternative processed record has y'_W=y_W+delta_W and simultaneously satisfies

    ||delta_W||_2/sqrt(n) <= epsilon_W,

for each selected W, where every supplied epsilon_W is finite and nonnegative. This is a direct processed-window envelope. It is not inferred from the native law, the file identity, a dimensionless ratio, producer precision, flags, a calibration fit or the observed contrast. No stochastic independence between windows or errors is assumed.

Define l_W=max(0,a_W-epsilon_W), u_W=a_W+epsilon_W and

    C_min=max_j l_j²,       C_max=max_j u_j²,
    d_min=l_0²-C_max,       d_max=u_0²-C_min.

## Theorem 1: exact one-window interval

Every admitted perturbation satisfies l_W² <= E'_W <= u_W². Indeed the triangle inequality gives ||y_W+delta_W||<=||y_W||+||delta_W||; its reverse gives ||y_W+delta_W||>=max(0,||y_W||-||delta_W||). Divide by sqrt(n) and square nonnegative quantities.

These are exact possible energy bounds for the unrestricted norm ball. If a_W>0, choose any b in [l_W,u_W], let y'_W=(b/a_W)y_W and delta_W=y'_W-y_W. Then ||delta_W||/sqrt(n)=|b-a_W|<=epsilon_W and E'_W=b². If a_W=0, choose any unit vector v and y'_W=sqrt(n)b v, b in [0,epsilon_W]. This also realizes every energy in the stated interval, including both endpoints. When epsilon_W=0 the interval is the singleton nominal energy. These witnesses are symbolic vectors, not generated fixtures or observed signals.

## Theorem 2: validity, contrast and sharp boundaries

For simultaneous window bounds, every perturbed comparison maximum lies in [C_min,C_max], and every perturbed excess lies in [d_min,d_max]. Therefore:

1. If C_min>0 and d_min>0, every admitted perturbed vector has a valid positive baseline and strict contrast.
2. If C_min>0 and d_max<=0, every admitted perturbed vector has a valid positive baseline and noncontrast. Equality permits a tie, correctly classified as noncontrast.
3. If C_max=0, every admitted perturbed comparison vector is zero and every outcome has zero-baseline abstention, whatever the event energy.
4. If C_min=0<C_max, the bounds alone do not guarantee baseline validity. In the unrestricted product of the17 balls, both a zero baseline and a positive baseline are attainable. A positive excess bound alone cannot override zero-baseline abstention.

Proof of the bounds: each E'_j lies between l_j² and u_j², so their maximum lies between the corresponding maxima. Subtracting those comparison bounds from the event bounds gives the excess interval. Baseline validity and the declared strict/non-strict decisions then yield1–4.

Sharpness is at the **product-ball** scope: the only constraints are the17 displayed norm balls, with unselected samples unconstrained or kept nominal. Disjoint windows let the one-window witnesses be assembled into a single N-vector. Set the event to its lower energy and every comparison to its upper energy to attain d_min. Reverse those choices to attain d_max. Set each comparison to its lower energy to attain C_min and each to its upper energy to attain C_max. Continuously vary the target root-mean-square values within their intervals to realize intermediate maxima/excesses as well. Consequently, when C_min>0, condition1 is necessary and sufficient for strict contrast for **every** product-ball member; condition2 is necessary and sufficient for noncontrast for every member. If C_min>0 and d_min<=0<d_max, both a noncontrast member and a strict-contrast member exist. d_min=0 allows an exact tie and is insufficient for universal strict contrast; d_max=0 is sufficient for universal noncontrast.

Additional global, calibration, or temporal-coupling constraints can shrink that product set. The bounds stay sufficient on any such subset, but their necessity and the assembled witnesses must not be transferred unless the subset admits them. Overlapping windows likewise preserve sufficient bounds but generally destroy independent endpoint attainability. The actual chosen windows are disjoint; their physical errors need not be independent.

With C_min>0, the ratio obeys

    l_0²/C_max <= R' <= u_0²/C_min.

These endpoints are also attained on the product set. If C_min=0 no division by it is allowed; a finite upper ratio bound need not exist, and a zero baseline remains invalid even if some other members have a valid ratio. This theorem does not stabilize the first maximizing j: comparison ordering can change within the bounds. For a specified k, l_k²>max_{j!=k}u_j² is sufficient for a unique maximizing k; otherwise the original first-index tie rule remains unchanged.

For prospective exact checking, interval predicates need not be decided by rounded square roots. For example d_min>0 is equivalent to a_0>a_j+epsilon_0+epsilon_j for every comparison j. Put t_j=epsilon_0+epsilon_j and h_j=E_0-E_j-t_j². Since t_j,a_j>=0, the latter strict inequality is equivalent to **h_j>0 and h_j²>4t_j²E_j**. The sign test is essential before squaring. C_min>0 is equivalent to at least one E_j>epsilon_j². Thus rational energies and rational supplied radii admit exact rational strict-contrast predicates. No predicate was evaluated on data here; no new implementation is supplied.

## Finite boundary witnesses

Take each window vector to have a constant coordinate value; then its root-mean-square amplitude is the absolute value of that constant. These are hand-specified symbolic examples with n=4096, not generated controls.

- Event constant2, every comparison constant1, all radii1/2: event decrease to3/2 and comparison increase to3/2 attain d_min=0. The nominal contrast is positive, but a permitted tie refutes universal strict contrast.
- Event constant1, every comparison constant2, all radii1/2: event increase to3/2 and every comparison decrease to3/2 attain d_max=0. Every allowed vector is noncontrast, with a tie possible, demonstrating the non-strict boundary.
- Event constant100 with radius0, every comparison constant1 with radius1: the event lower energy exceeds every comparison upper energy, yet choosing delta_j=-y_j makes all comparison energies zero. The result must abstain. This demonstrates why C_min>0 is a separate universal-validity requirement.

## Theorem 3: common gain and its failure boundary

For a fixed finite real g!=0 applied to the entire processed record, every energy becomes g²E_W; C becomes g²C; D becomes g²D. Hence zero/nonzero baseline status, strict contrast/noncontrast, the ratio when defined, and all maximizing comparison indices including first-index tie breaking are preserved. Negative gain is allowed because of the square. This is a mathematical functional invariance, not a claim that altered bytes pass the original input-identity gate or retain all physical metadata. At g=0 all comparison energies vanish and the rule abstains; R cannot be assigned its old value by cancellation of0/0.

A window-dependent gain need not preserve order. With event constant2 and all comparisons constant1, nominal energies are4 and1. Event gain1/4 and comparison gains1 produce event energy1/4 against maximum1, reversing the decision while the baseline stays positive. No arbitrary phase-, frequency- or timing-dependent detector calibration reduces to a common scalar gain by assertion. The finite counterexample concerns unconstrained gains, not an estimate of any actual detector error.

## Linking a processing map, without inventing calibration

If a fixed full-record linear map T:R^N->R^N is independently stipulated with all boundary/padding/state conventions fixed, y=T x and a pre-processing perturbation v produces output perturbation T v. Let P_W select the n coordinates in W. A sufficient input-to-window certificate would be an independently supplied bound

    sup_{v in V} ||P_W T v||_2/sqrt(n) <= epsilon_W

for one stated full-record uncertainty set V. For example, if ||v||_2<=rho and a separately established induced operator bound is ||P_W T||_(2->2)<=kappa_W, then epsilon_W=kappa_W rho/sqrt(n) suffices by the definition of induced norm. A gain/error operator acting before T requires its own V or operator-composition bound. No kappa_W, rho, V or linearity of the actual complete recorded pipeline is established here.

An input perturbation outside W can contribute to P_W T v when the whole-record processing couples samples. One must not replace that full-record expression by T acting only on v_W, assume finite support, or add independent per-window variances without proof. A time-dependent, uncertain or nonlinear processing map requires a separately justified error decomposition/bound. This paper does not calculate any actual operator norm, reopen coefficients, refilter the waveform, or supply detector amplitude/phase/timing uncertainties and their correlations.

## Confidence, physical limits and admission

The conclusions are deterministic on the joint event B that all17 bounds hold and all relevant non-arithmetic premises are true. They require no independence. If an external calibration procedure independently establishes Pr(B)>=1-alpha for the intended population under its own stated assumptions, a fixed certificate's deterministic implication holds on B, and its unconditional failure probability is at most alpha. This is not a posterior probability conditional on an observed contrast, a p-value or a claim that the certificate is likely to pass. Separately certified marginal bounds with failure budgets alpha_W imply joint failure at most sum alpha_W by union bound, without independence; no coverage values are supplied here. Selection after seeing the signal cannot be treated as such an external certificate without a new valid coverage argument.

All actual input admission, source/effects review, control passes, execution/resource/custody gates remain unchanged. Applicable physical calibration, sampling/selection and a native law-to-detector observation map remain missing for physical/DET interpretation. The accepted prospective replay remains completed; nothing is repeated or historically reconstructed. This formal result is a parallel scientific analysis of sensitivity, not additional mandatory qualification for the nominal-only statistic. The coordinator accepts precisely this conditional scope after distinct review.

## Energy: finite joint-calibration gauge obstruction

The accepted NE-C008 result is an internal-identifiability obstruction relative to a fixed external ideal. In one target cell of mass q=1/4, take sigma=(q/2)(I+aX), a=1/2, and Q_±=(I±[(3/5)X+(4/5)Z])/2; three other cells have states qI/2. In the target cell use H_0=0, H_1=(pi/2)Z and U_s=exp[-is pi Z/2]; other cells have zero generators. Conjugate both preparation and effects in the target cell by W=Z, leaving others unchanged. W commutes with U_s and changes X to -X. Thus sigma'=(q/2)(I-aX) and Q'_±=(I±[-(3/5)X+(4/5)Z])/2. Cyclicity of trace and commutation give Tr(Q'_o U_s sigma' U_s†)=Tr(Q_o U_s sigma U_s†) for every setting and hypothesis. All eight labeled row probabilities coincide. This proves row equivalence, not an assertion about arbitrary dependent recording laws or loss of the H_0/H_1 distinction.

Against the held-fixed ideal, sigma'-sigma=-X/8 has trace norm 1/4, so eta_P=1/8; Q'_+-Q_+=-(3/5)X has operator norm 3/5, so eta_Q=3/5. Their sum is 29/40 while the row total-variation discrepancy is zero. The earlier sufficient norm threshold 3/1280 cannot be inferred from internal rows alone; failure of that sufficient criterion does not establish discrimination failure. A known held-fixed coherent reference sigma_ref=q(I+rX)/2, 0<r<1, gives plus probabilities q(1±3r/5)/2, separated by 3qr/5. A diagonal reference cannot break this witness. One such witness-breaking reference is not full tomography. An independently certified complete-row envelope is an alternative premise; fitting the test rows is not that certification. No physical clock, action scale or work store follows.

## Relational state: recovered candidate, typed-design defects

The coordinator accepts recovery of the E-C008 candidate specification and requires repair before an executable comparison. The first-valid E-C003 rule, no-anchor branch and retry semantics remain fixed. Equal available channels do not imply equal closed-loop histories, and the 32-packet moving-horizon estimator retains older information through its persistent arrival prior.

The state x=(T1,T2,Ta,g0,g1,b,w1,w2) has eight coordinates, whereas the ordered innovation (Ta,g0,g1,b,w1,w2) has six. A 6-by-6 innovation covariance cannot be added directly to an 8-by-8 arrival covariance. An explicit transition F and 8-by-6 injection G, or an equivalently consistent model, are required; inventing direct temperature noise would change the proposal. Clipping derivatives, initialization, solver approximation and covariance conventions also need specification.

Pairwise objective tolerance is not an equivalence relation: objective values 0, 0.75 tau and 1.5 tau have adjacent distances below tau but endpoint distance above tau. A fixed-reference admissible set and deterministic attained-choice rule are required. Q, R, priors, MPC details, full source-to-reset costs and independently held-out reliability remain missing. The bounded proposal is neither a competent matched benchmark nor an advantage result.

## Computing: documentary feasibility hold

CE-R001's initial review verified local pins but lacked the captured documentary bodies. That limited review remains intact. A later prospective independent documentary completion read the two admitted primary sources, including the exact XNU blob 5190630bfe4d4b592bf4e9dfd9c60b88bb34591f. It supplies new prospective textual support, not reconstruction of earlier capture custody or installed-host identity.

The archived manual describes preferential resident-memory reclamation, not the required instantaneous hard resident ceiling. The inspected XNU address-space limit concerns virtual maps and does not prove a resident-memory guarantee. CPU time does not bound wall time. No admitted mechanism yet establishes the combined 10-second CPU, 30-second wall, 256-MiB instantaneous resident, pre-import control, 140-KiB total-output and durable post-failure receipt contract. A killed workload cannot subsequently write its own receipt. An external controller would require an explicit process-count amendment; none is adopted here. This is a documentary HOLD, not a universal impossibility theorem or installed-system verification. A one-second discrepancy in a historical reset label is not accepted reset evidence.

## Current dispositions and next reserved questions

| Lane | Current accepted scope | Newly assigned deliverable; uncertainty to close |
|---|---|---|
| QR | Selected-family common-response anchor proposition only | RI1397: common-latent law/readout identifiability beyond the selected pair; investigate the proposed endpoint-atom alias and the separately stipulated no-endpoint-atom case. Neither is a result of this checkpoint. |
| Measurement | Conditional finite-vector robustness theorem above | Nominal H1 minimal-admission dependency matrix: distinguish necessary nominal controls from production/robustness extras and identify the smallest actual missing closure without executing the calculation. |
| Relational state | Candidate recovered; MHE covariance and selection defects found | E-C009: typed eight-state/six-innovation propagation and deterministic tolerance-selection repair, preserving the candidate and full-cycle cost blockers. |
| Energy | Finite joint-gauge obstruction and limited reference witness | NE-C009: conditional binary-effect reconstruction from explicitly trusted held-fixed I/2 and three known-axis references, with error and conditioning bounds; these reference premises are not established experimentally. |
| Computing | Documentary hold retained | CE-T001: finite payload-only DAG incremental correctness and fully charged work accounting against competent conventional baselines; no performance execution or advantage claim. |

Each new reservation is a bounded author assignment awaiting distinct review and coordinator disposition. No successor findings are included here. All five lanes share the account-capacity guard: work stops at 10% remaining or less, with supported same-account reset evidence required after a threshold stop. The preparation exception is closed. Scope, exact inputs, budgets, exclusive outputs and stop conditions remain in the respective assignments. The RET-only pause, actual protected-validation and custody requirements, frozen packages and historical failures remain in force. Publication is a scoped documentation checkpoint; main integration is merge-only with no landing-page change.

## Evidence and review boundary

Root adjudication is separate from authoring and review. The current identity audit checked 148 inventory and direct-join conditions across the five current pairs plus the original limited CE review; hashes establish current bytes and joins, not theorem truth, scientific execution or historical custody. The publication preparer previously authored the measurement and CE reviews and performed identity audits; this editorial preparation is not another independent review. A distinct publication review remains required before application.

Scientific source identity is given below. These pins identify the exact frozen source documents used, not validation of their premises.

| Lane | Author document SHA-256 | Distinct review SHA-256 |
|---|---|---|
| QR | `35ffeae938683943c184d9defbced12c85b8dbda60a016cdbc93c1f0f2b01920` | `97af14c8b45628f8381bfc056d884873d8648983ddcebd1e4809fba1d386d629` |
| E | `813974f8e331b1dad9183e4d4a8a639d9917c1739b60858a49bcc2e7dcd24ae5` | `d2cde855a1994deb417f583797a3441c96af73366cef6817420906ad22e9ff96` |
| NE | `6817ce8fbfdc583832d03ada04696dd5c70b1510a34a5fe2dc8adcd1b4ebc73e` | `58f4365aa2582ca0077f67e49ed4c038235477189e9f513ab8b69750b5e056bd` |
| CE | `37662e13e7162b4b98aa1f091f429185ee806bc5c880614e48e7329f7968ff04` | `f9bcfc0332e3fd6530e6f8b6aedb020ba1a129e9f1f981df6621c7d7af9a78b4` |
| measurement | `f4f722092cba13ec997eb1178ceba6c66b37fe5e454e0b6404def7331822812b` | `c026f6d40307e2f0767034ce0873dc779be0ff1fe47aa3701d9c77b4132d5c26` |
