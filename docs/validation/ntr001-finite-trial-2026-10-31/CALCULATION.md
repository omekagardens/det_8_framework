# NTR001 — conditional finite-trial native source comparison

**Accepted conditional mathematical result after completed distinct review and coordinator disposition.** The accepted NM006 population law admits a conservative finite-count test once a positive contrast floor and independent repeated preparation/readout are explicitly supplied. This conditional result supplies neither premise physically.

## Fixed laws and quantifiers

Use the adopted [complete-trial source law](../../observables/native_complete_trial_readout.md), including its mixed-source extension, without rederiving native histories. Retain exactly four births, the complete antichain event, every mark/continuation, and outcomes Y in {0,1,perp}. Set
\[
b=\frac{8185}{2230272},\qquad \beta=\frac{263}{1115136},\qquad
r_i=(1-e)\{f+(1-f-n_d)(b+\beta x_i)\},
\]
so the complete reported law is mu_i=(1-e-r_i,r_i,e). Here n_d is the detector false-negative rate; N denotes the per-setting trial count called n in the assignment.

Fix independently certified closed source intervals I_i=[l_i,u_i] and the entire admitted shared detector box. The unknown x_0,x_1,f,n_d,e are fixed throughout the run, with every combination in that full product allowed. No prior, correlated subset or fitted calibration is assumed. The detector bounds obey e_+<1 and f_++n_d,+<1.

For strictly separated source intervals, let h be the setting whose interval is higher and l the other. Define the known floor
\[
g=l_h-u_l>0,\qquad
d=\beta g(1-e_+)(1-f_+-n_{d,+})=\Gamma_{\rm mix}/2>0.\tag{1}
\]
The accepted paired law gives r_h-r_l>=d uniformly over the full certified product. This is a floor on the **raw reported-one probability difference**, not a success-conditioned contrast.

**New hypothetical repetition premise:** assign N attempts to each setting; all 2N reported outcomes are independent, with the same corresponding mu_i on every attempt. The source pair and common detector do not drift. A one-trial law or one continuously growing trajectory does not imply this iid/reset/channel contract.

The null H0 contains every common fixed probability vector nu on {0,1,perp}, sampled independently N times at each setting. The alternative H1 is the exact active NM006 family above, sampled under that same repetition contract. The bounds below hold for every null nu and every fixed alternative tuple in the full certified product. The accepted passive and forward-only controls are included in H0. No residual or other hidden decision feature is available.

## One rule and its finite budget

Record all complete counts C_i(0), C_i(1), C_i(perp), whose sum is N at each setting. Use
\[
\widehat D=\frac{C_h(1)-C_l(1)}{N},\qquad
\boxed{N=\left\lceil\frac{40}{d^2}\right\rceil.}\tag{2}
\]
After the fixed 2N attempts, output **DETECT** if Dhat>=d/2; otherwise output **NO DETECTION**. The latter is not a proof of the null. There is no data-dependent stopping, retry, fitted threshold or calibration step. Reports 0 and perp both contribute zero to the indicator for report 1, but remain in the denominator. The complete three-outcome data are retained; no success-only conditioning is performed.

Within the stated model the rule always decides, so decision coverage is exactly one under both hypotheses and ABSTAIN probability is zero. If an application introduces abstention, it must count toward failure to detect; the theorem does not promise power after such a change.

### Self-contained risk proof

For an indicator X with mean p, X^2=X, hence Var(X)=p(1-p)=1/4-(p-1/2)^2<=1/4. Independence makes distinct centered cross products have expectation zero. Therefore, writing m=E(Dhat),
\[
\operatorname{Var}(\widehat D)
=\frac{r_h(1-r_h)+r_l(1-r_l)}{N}
\le\frac1{2N},\tag{3}
\]
with the same bound under H0 by replacing both r_i with nu(1).

For any nonnegative finite-valued W and a>0, summing over W>=a gives E(W)>=a*P(W>=a). Apply this to W=(Dhat-m)^2 and a=t^2:
\[
P(|\widehat D-m|\ge t)\le\frac{\operatorname{Var}(\widehat D)}{t^2}.
\]
Under H0, m=0, so DETECT implies |Dhat-m|>=d/2. Under H1, m>=d, so NO DETECTION implies m-Dhat>d/2. Consequently
\[
\sup_{H0}P(\mathrm{DETECT})\le\frac{2}{Nd^2}\le\frac1{20},
\qquad
\sup_{H1}P(\mathrm{NO\ DETECTION})\le\frac{2}{Nd^2}\le\frac1{20}.\tag{4}
\]
Thus power is at least 19/20 over each fixed certified alternative class. Ties at the threshold are included in DETECT and satisfy the same bounds. These are unconditional sampling risks at each fixed nuisance tuple, not posterior probabilities or confidence in the physical premises. The bound is deliberately conservative; no optimality or efficiency is claimed.

## Symbolic and negative checks

For pure ideal sources I_h={1}, I_l={0} and f=n_d=e=0, d=beta. Equation (2) becomes
\[
N_{\rm ideal}=\left\lceil40\left(\frac{1115136}{263}\right)^2\right\rceil,\tag{5}
\]
with the accepted pure complete laws and zero erasures. An ideal point inside a larger uncertainty box does not improve that box's guaranteed floor.

If the closed source intervals overlap or touch, an equal-source pair is admitted. Its two laws are identical and belong to H0, so no rule can have size<=1/20 and power>=19/20 over that entire alternative class. Formula (2) is unavailable at d=0. Likewise e=1 or f+n_d=1 gives a common report law; these detector controls lie outside the informative promise. The passive and forward-only laws are source-independent throughout the admitted informative box, so the size bound applies to them. Zero uniform floor does not mean every particular unequal-source pair has zero contrast.

Mere positivity without a certified uniform floor cannot support one fixed cap across arbitrarily close source pairs. For a short scope check, use only the accepted [P4 TV/product lemmas](../../track_b/native_theorem_package_v1/P4_FIXED_BUDGET_TESTING_LIMIT.md): at the ideal detector compare active sources x_h=eta>0, x_l=0 with the null having x=0 at both settings. Their single changed-setting laws have TV=beta*eta. The N-fold product has TV<=N*beta*eta. Adding the unchanged independent setting leaves TV unchanged, since its probabilities sum to one. Therefore any common decision rule has
\[
P_{H1}(\mathrm{DETECT})\le P_{H0}(\mathrm{DETECT})+N\beta\eta.\tag{6}
\]
For fixed N and sufficiently small positive eta, size 1/20 cannot coexist with power 19/20. This instantiates only the elementary lemmas on the existing NM006 law; it imports none of P4's different native scale or occurrence premises. Each separately certified positive eta still permits its own finite bound (2).

Repetition evidence is independently necessary for (3): copying one draw at each setting N times preserves the individual one-trial marginals but gives no 1/N variance reduction. Correct population laws alone cannot justify the stated sampling guarantee.

## Cost and physical admission

The mathematical workload is exactly **2N raw assigned trials and 8N native births**, including every erased report. These counts do not supply physical duration, energy, reset cost, calibration cost or an apparatus. Physical accounting must also retain preparation failures, completion monitoring, acquisition, relation recovery, storage and analysis. Failed physical attempts are not assigned imaginary native births or a fabricated state/history. A fixed raw budget is not a target number of successful detections.

Actual physical use remains blocked by the unsupplied native source/effect/law/reset correspondence, independently valid source intervals, complete four-event order readout, common conditional detector and erasure calibration, stability, and independent repetition. Certificates must cover all compatible possibilities and the assigned-attempt population; the desired terminal contrast cannot certify its own source or detector. Preparation/completion/acquisition failures enter perp under the theorem only where the common-erasure model is independently justified. Otherwise retain all attempts and mark the physical application inapplicable; do not drop failures or claim the power bound. Missing relations do not prove an antichain.

A rejection distinguishes source-independent reported laws under this contract. It does not uniquely identify the active mechanism, exclude conventional or larger static-seed realizations, or establish quantum, energy, time, mass or gravity correspondence. The same-information conventional baseline retains source-label access and all justified records/calibration. No empirical campaign or execution is authorized.

**Decision:** a finite symbolic guarantee exists for this fixed population family under a certified positive floor and the new hypothetical iid contract. The physical correspondence and repetition/calibration evidence remain open. The finite question is closed at this conditional scope. See the [review](REVIEW.md) and [adoption](ADOPTION.md); physical application requires the stated independent evidence.
