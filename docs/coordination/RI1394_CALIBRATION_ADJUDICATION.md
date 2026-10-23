# RI1394: Calibration and five-lane adjudication

The coordinator accepts RI1393's conditional calibrated binary-readout proposition after a distinct manual scientific review. The four other accepted packages remain conditional mathematical or inert design results. This checkpoint admits no scientific, apparatus, benchmark, protected-validation or operational execution, and no physical validation. The five successors below are author reservations awaiting independent review and coordinator disposition; their proposed questions are not accepted results.

The following sections reproduce the complete RI1393 setup, proposition, proof, witnesses and calibration accounting literally. The admitted input is the RI1391 true-bit experiment: the optional common-latent law draws a fresh latent parameter independently for each preparation; its two densities on [0,1] are 1±h(t)/642 with h(t)=70t^4−140t^3+90t^2−20t+1. Given t, independent forward Bernoulli(t) edges are transitively closed and birth labels forgotten. A completed size-n chain requires the n−1 adjacent edges, so its conditional probability is t^(n−1). The established fourth-moment difference supplies the size-five probabilities used below. This law and preparation/readout premises are declared construction assumptions, not a selected physical law or observation channel. No chronological account is needed to use the finite readout proposition.

## 1. Fixed experiment and response

The accepted RI1391 independent-preparation experiment supplies iid true
chain bits \(B_i\) with
\[
 a_\sigma=\Pr_\sigma(B_i=1)=a_0+\sigma d,\qquad
 a_0=1/5,\quad d=1/(642\cdot630)>0,\quad \sigma\in\{+,-\}.
 \tag{1}
\]
Each trial independently redraws its latent variable and grows a fresh
completed order to known true size five. The hypothesis is fixed across
trials. These promises are not replaced by successive prefixes of one
history. Size five is specified, not asserted minimal.

The observer now sees only \(Y_i\in\{0,1\}\), through one memoryless response
\(c=(f,t)\in[0,1]^2\):
\[
 \Pr(Y_i=1\mid B_i=0,c)=f,\qquad
 \Pr(Y_i=1\mid B_i=1,c)=t,\qquad s=t-f.
 \tag{2}
\]
Here f is the false-positive probability and t the true-positive
probability. The same fixed c applies throughout the experiment and is
hypothesis blind. Conditional response randomness is independent between
trials and independent of preparations given the true bits; the response
depends on the order only through its true bit. There is no drift,
memory, selective reporting, missingness or unknown size in this model.

Consequently the observed bits are iid Bernoulli with
\[
 q_\sigma(c)=(1-a_\sigma)f+a_\sigma t
            =f+s a_0+\sigma s d.
 \tag{3}
\]
Before test data are taken, declare a nonempty compact convex calibration
set \(C\subseteq[0,1]^2\), independent of the test randomness. Initially
treat membership of the actual c in C as a stated premise. Section 5
separates that premise from a finite probabilistic calibration guarantee.
Convexity is explicit and includes rectangles and the segment examples
below; arbitrary nonconvex sets are not claimed to have the same dichotomy.

## 2. One finite proposition, with distinct nuisance quantifiers

**Known fixed response.** If c is known, \(s\ne0\) is exactly the condition
for distinct observed Bernoulli laws. With \(b=f+s a_0\), choose plus when
\[
             \operatorname{sign}(s)(\overline Y-b)\ge0,
 \tag{4}
\]
and minus otherwise. Each conditional error is at most
\[
                         \exp(-2k s^2d^2).                         \tag{5}
\]
If \(s=0\), the two complete output distributions agree for every k.
A negative known slope reverses the decision orientation; it does not
destroy the distinction.

**Shared but unknown response.** At the same fixed c, the paired gap is
\(q_+(c)-q_-(c)=2sd\). This conditional comparison is not yet a test that
an observer ignorant of c can implement. The centering b in (4) is
unknown. To require one procedure valid for every possible c in C, use
the composite output-mean families
\[
 Q_\sigma=\{q_\sigma(c):c\in C\}=[L_\sigma,U_\sigma],
 \quad L_\sigma=\min_C q_\sigma,\quad U_\sigma=\max_C q_\sigma.
 \tag{6}
\]
These are closed intervals: q is linear, and C is compact and convex.

If \(g=L_+-U_->0\), predeclare threshold
\(\tau=(L_++U_-)/2\) and choose plus when \(\overline Y\ge\tau\).
Uniformly for every admissible actual response and either hypothesis,
\[
                         \Pr(\text{wrong})\le e^{-kg^2/2}.
 \tag{7}
\]
The reverse orientation holds if \(g=L_--U_+>0\): use the midpoint of
those two endpoints and choose plus when \(\overline Y\le\tau\).
For a predeclared \(\alpha\in(0,1)\), an integer
\[
                    k\ge\left\lceil2\log(1/\alpha)/g^2\right\rceil
 \tag{8}
\]
suffices in either case. These threshold and sample-count rules must be
chosen before seeing test data, though they may depend on independent
pre-experiment calibration.

**Separate nuisance choices in competing explanations.** If
\(Q_+\cap Q_-\ne\varnothing\), there exist \(c_+,c_-\in C\) with
\(q_+(c_+)=q_-(c_-)\). Their entire iid Y laws are then identical for
every finite k. For any randomized binary test of those observations,
\[
 \Pr_{+,c_+}(\text{choose }-)+
 \Pr_{-,c_-}(\text{choose }+)=1.                                    \tag{9}
\]
Thus no uniformly valid test on this composite experiment can have both
errors below 1/2 at that pair, regardless of trial count. For compact
convex C, either the intervals are strictly ordered as above or they
overlap; touching endpoints already permit exact alias.

This does not assert that an apparatus changes response when a hypothesis
changes. One actual response is fixed and common. Rather, when c is
unknown, two different possible worlds can explain the same observations
using different responses consistent with the same calibration information.
A guarantee uniform over all c must cover both worlds. If the comparison
is explicitly restricted to one known or externally identified c, the
paired result applies instead. Unknown shared nuisance is not automatically
an experimentally identified nuisance. Likewise (9) concerns test bits
conditional on the stated calibration information C; it is not an alias
claim for a richer joint law of raw calibration records and test records.

## 3. Proof and explicit finite witnesses

Equation (3) follows by conditioning on B. Independence follows from the
fresh preparations and independent memoryless response draws, not merely
from equal one-trial marginals.

For a Bernoulli variable of mean q, the centered log moment-generating
function has value and first derivative zero at zero and second derivative
equal to a tilted Bernoulli variance, at most 1/4. Integrating twice gives
\(\log\mathbb E e^{u(Y-q)}\le u^2/8\) for either sign of u.
For independent trials, exponential Markov at \(u=4r\) or \(-4r\) yields
\[
 \Pr(\overline Y-q\ge r),\quad
 \Pr(\overline Y-q\le-r)\ \le e^{-2kr^2}\quad(r>0).
 \tag{10}
\]
The known-response threshold is distance \(|s|d\) from each mean,
giving (5), with either tie convention bounded by the closed tail.
The composite midpoint is at least g/2 from every mean on the appropriate
side, giving (7) and (8). For alias, both experiments have the same
Bernoulli product law. If a test chooses plus with probability z under
that law, its two errors are 1-z and z, proving (9).

A concrete calibration segment exposes the offset problem without an
unknown sign or vanishing slope. For \(0\le w\le d\), set
\[
 C_w=\{(f,t):f\in[1/4,1/4+w],\quad t=f+1/2\}.                       \tag{11}
\]
All parameters are in [0,1] since \(d<1/4\), and the slope is exactly 1/2
everywhere. Yet
\[
 Q_\sigma=[7/20+\sigma d/2,\;7/20+w+\sigma d/2].
 \tag{12}
\]
The paired gap is d at every fixed response, whereas the robust interval
gap is only \(g=d-w\).

For \(w=d\), choose
\[
 c_+=(1/4,3/4),\qquad c_-=(1/4+d,3/4+d).
\]
Both give \(q=7/20+d/2\) under their respective hypotheses. Thus a strictly
positive slope, even known exactly, does not exclude finite alias when
the offset is uncertain. This is an alias already for one observed bit
and hence for every finite product of independent observed bits.

For \(w=d/2\), the same model instead has gap \(g=d/2\).
The threshold \(7/20+d/4\) separates the families and each error is at
most \(\exp(-kd^2/8)\). These exact witnesses are stipulated calibration
sets, not measured precision claims, numerical searches or apparatus designs.

## 4. What calibration must control

For a rectangular set \(C=[f_L,f_U]\times[t_L,t_U]\subseteq[0,1]^2\),
the nonnegative weights in (3) give explicit endpoints
\[
 L_\sigma=(1-a_\sigma)f_L+a_\sigma t_L,\qquad
 U_\sigma=(1-a_\sigma)f_U+a_\sigma t_U.
 \tag{13}
\]
One must compare the cross-hypothesis endpoints, not just verify that
\(t-f\) is positive throughout C. For example, with center \((f_0,t_0)\)
and both coordinate radii at most rho, each q differs from its center
value by at most rho. If \(s_0=t_0-f_0>0\), then
\[
                       L_+-U_-\ge2s_0d-2\rho.                    \tag{14}
\]
Thus \(\rho<s_0d\) is a sufficient, not necessary, calibration condition
for the positive-orientation test. Clipping a rectangle to [0,1]^2
cannot worsen this bound. No practical feasibility is inferred from it.

## 5. Finite pre-experiment calibration, explicitly conditional

One possible mathematical source of C is the following separate finite
experiment. Assume externally certified controls with true bit zero
and true bit one are available. Take predeclared positive sample counts
\(m_0,m_1\); their readouts are independent Bernoulli(f) and Bernoulli(t),
respectively, under exactly the same stable response as the later test.
All calibration randomness is independent of later preparations and
response randomness, conditional on the fixed c. Access to certified
controls and response transferability are additional premises, not
established by the DET construction.

For \(0<\eta<1\), define
\[
 r_j=\sqrt{\log(4/\eta)/(2m_j)},\qquad
 C=\bigl([\widehat f-r_0,\widehat f+r_0]\cap[0,1]\bigr)
   \times\bigl([\widehat t-r_1,\widehat t+r_1]\cap[0,1]\bigr).
 \tag{15}
\]
The two-sided version of (10) bounds each coordinate's exclusion
probability by \(\eta/2\); the union bound gives
\(\Pr_c(c\notin C)\le\eta\). This is repeated-sampling coverage,
not a posterior probability for c after seeing C.

Conditional on any calibration realization for which the actual c lies
in C and a positive separation gap exists, test randomness remains iid
with its original q. Thus (7) applies to the predeclared calibration-based
threshold, and (8) can set k using that realized gap. To avoid hiding
calibration failures, count nonseparating calibration outcomes as failures.
Then the total failure probability is bounded by
\[
                \eta+\Pr_c(\text{no positive gap})+\alpha,         \tag{16}
\]
capped trivially by one, when positive-gap outcomes use (8).
Equivalently, the probability of a wrong decision on positive-gap outcomes
is at most \(\eta+\alpha\); this is not the error conditioned on obtaining
a positive gap. An overall binary guarantee of \(\eta+\alpha\) requires
the additional premise that all calibration outcomes used by the design
have a positive gap (or a separate bound/accounting for the others).
No such success-frequency or calibration-power claim is supplied here.

The alias in section 3 remains an alias of the test-bit families given
the uncertainty set. Informative raw control observations may distinguish
the nuisance values; this note does not assert equality of their joint
calibration distributions. Merely supplying an interval without a coverage
or hard-membership premise supplies no guaranteed error bound.


## Coordinator dispositions and remaining premises

**QR — accepted conditional proposition.** The distinct review checked the affine response, both slope orientations, compact-convex interval dichotomy, offset witnesses, simultaneous calibration coverage and failure accounting. The coordinator accepts the proposition exactly at those premises. A noisy common channel cannot overcome the earlier one-latent-history information bound. The complete current RI1391 and RI1393 packages do not repair RI1389's missing original author SOURCE_PINS, RESULT and FREEZE artifacts. Historical custody failure remains visible.

**Relational State — E-C007 accepted at scoped coordinate-equivalence and missing-algorithm scope.** Given the packet and retained conductance estimate, m=qhat−ghat_z(y1−y2) is invertible back to qhat; it creates no new information, sufficient statistic or energy store. A competent conventional causal implementation can clone a specified deterministic recurrence, retaining and charging the same state. This establishes neither equality with the proposed moving-horizon estimator (MHE) nor a performance advantage. Both arms receive the same raw-packet entitlement, while 32-packet MHE plus persistent arrival prior/covariance must not be conflated with identical effective memory. Safety/validity precede estimation and shared MPC control, including the accepted first-valid/retry corrections.

The missing-definition finding concerns E-C007's allowed inputs. The coordinator subsequently recovered the existing E-D001 section4 candidate q/g recurrence, residual forecast and parameter domains, together with E-C002's causal boundary contract. Those inputs are explicitly admitted to the successor. The paired MHE objective, arrival-state updates, solver/tie rules and shared MPC implementation still require specification. Full source-to-reset costs, regeneration/reset dynamics, numerical calibration certificates, competent comparison and independently held-out evaluation remain unresolved. No thermal controller, trace or experiment was executed.

**Energy — NE-C007 conditional finite-catalogue budget accepted.** For the admitted two-setting catalogue, the ideal summed row total variation D is at least3/320. Complete normalized candidate/setting row error at most e yields actual D at least3/320−4e, hence e<3/1280 suffices. Equal-setting labelled joint TV is D/2. Under the same exact unitary evolution, positive four-block source states of total trace1 with half summed trace-norm error eta_P, and complete two-sign POVMs with effect operator-norm error eta_Q, give row TV at most eta_P+eta_Q. The signed witness gap is at least3/160−8e. These are sufficient conditional budgets, not measured calibration values.

The fixed-pair midpoint alias threshold e≥max_c d_c/2 is sharp only for the declared abstract row balls. At rho=2,u=v=0 the row distances are0 and3/40, giving e=3/80; this is neither a global sharp threshold nor a demonstrated source/effect realization. Preparation/readout certificates and transfer remain external; common independent record generation must be supplied for full-record alias. No physical clock, action scale, work store or apparatus follows.

**Computing Efficiency — CE-S004 inert repair accepted; execution HOLD.** FatalResourceStop, MemoryError and TimeoutError propagate by bare raise before the ordinary per-case failure handler. The designated class is the actual loaded harness class, not its name. The22 cases remain; C15 supplies33347 while retention is33346, and the full no-exception path has40 assertion/rejection calls, eight in C20. These are source assessments, not observed runs. Catchable exception propagation does not enforce a hard resource ceiling or guarantee a failure receipt after exhaustion. CPU10s, wall30s, strict instantaneous resident256MiB and one workload process/no children require a concrete enforcing boundary before import. JSON64KiB plus temporary64KiB, cleanup4KiB and two4KiB diagnostics totals140KiB. Runtime/source identity, import effects, cleanup and incomplete-outcome custody remain gates; no M1 or benchmark admission follows.

**Measurement — conditional R1 inert component accepted with process limitation.** The source uses MACH_TASK_BASIC_INFO with one task_info call and a fresh native count. Native failure status precedes exact-count validation, which precedes resident_size use; failure never becomes a zero measurement. A valid native zero does not qualify a positive RSS observation. Checked signed-magnitude conversion avoids negating INT_MIN, roundtrips/static widths constrain decimal rendering, and bounded encoding prevents partial-success output. Valid exclusive caller storage and a borrowed own-task right with a valid lifetime are explicit premises. One call is not a time/resource enforcer. Include/ABI/build/compiler/image/cache/B1 identities and execution admission remain unresolved.

The R1 review's initial broad header search occurred before the required fresh header-pin check and was truncated. Later verified readback and31 identity checks support the conditional source assessment, but do not erase that sequencing deviation or reconstruct historical custody. No scientific source was parsed, imported, compiled or executed in this checkpoint. The accepted prospective GWOSC replay is not repeated, and no native forward map is invented.

## Five next author reservations

| Lane and owner | Reserved deliverable and uncertainty | Scope and stop |
|---|---|---|
| QR / DET Quantum Relativity: RI1395 | Determine whether admitted law-family population anchors can reduce RI1393's externally certified control premise. Verify size1/size2 chain anchors and investigate a stable response transferring across sizes1,2,5; resolve orientation, zero slope and finite-budget separation. | Assigned question only: the suggested anchors, contrasts and new error bounds are not proved claims of this checkpoint. Manual proposition or obstruction, then distinct review. Cross-size response transfer is an added premise. |
| Relational State / DET Relational State Research: E-C008 | Versioned parametric candidate/MHE interface and competent MHE proposal, using recovered E-D001 and E-C002 plus accepted later corrections. | Specify arrival state, objective, constraints, timing, termination/ties and unresolved certificates; no favorable invented numbers, trace tuning or execution. Exact paired action distinction remains open. |
| Energy / DET Energy Research: NE-C008 | Test whether non-target probabilities certify individual source/effect norm budgets without a trusted reference; seek a finite gauge-equivalence counterexample or precise obstruction. | Coordinate gauge, actual error, sufficient norm failure and observed row failure must remain separate. Candidate conjugations are questions, not accepted results. No catalogue execution. |
| Computing / DET Comp-Sci Research: CE-R001 | Documentary runner feasibility for the unchanged CPU/wall/resident/output/failure-receipt requirements. | Narrow primary-document allowance only; installed identity is not inferred from manuals or repository main. Flag supervisor/one-process conflicts and unsupported hard caps; no host probing, verifier execution or implicit relaxation. |
| Measurement / delegated measurement author: fixed H1 contrast robustness design | Manual finite-vector perturbation certificate for unchanged nominal4096-sample mean-square contrast, strict contrast/noncontrast, ties, zero comparison and sharp witnesses. | No arrays or observed statistic. Separate deterministic simultaneous bounds from joint coverage; distinguish common scalar gain from window-dependent or frequency/phase/timing errors. This analysis adds no prerequisite to the separately admitted nominal calculation. |

Each reservation is one bounded author packet with exclusive output and separate review. Four chat successors and the separate measurement author have been assigned; publication includes no accepted successor result. Current scientific questions remain parallel. RET remains paused; protected validation and custody requirements remain intact. No application result validates another lane or physical DET. All workers retain the shared supported usage guard, stop/reset conditions and their specific input/output budgets.

## Evidence and publication limits

Scientific decisions are the coordinator's dispositions after distinct subject review, not this editorial preparation's new independent scientific review. The editor previously authored the E and measurement reviews and an identity-only audit, and has prior publication exposure. The current identity audit passed132 checks across ten frozen author/review packages; older recursive references were skipped. The distinct reviews report49 QR,24 E,18 NE,21 CE and31 measurement administrative identity checks. Those counts and current hashes establish named byte relationships, not scientific execution, historical custody or proof by themselves. The mathematical review was manual.

The report's RI1393 sections1–5 are literal source text. The manuscript SHA256 is396003f69d996369c9ce3d1469d9e977d42d9d2392d8b7fedb0b1baf7624d414; its distinct review SHA256 is2f038a3883e33436d6486d65995e72d25e211aaf95e88b7f43314d9f7e08a739. A separate public manifest pins this report and the four public coordinator fronts, excluding itself. The prepared update preserves each old front as an exact suffix. Main remains merge-only, with no landing README change. Publication preparation requires distinct review and root application; hashes do not grant execution.
