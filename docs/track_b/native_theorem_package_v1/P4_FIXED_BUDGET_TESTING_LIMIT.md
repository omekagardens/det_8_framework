# The P4 fixed-raw-budget testing limit

21 October 2026. Conditional finite-observation theorem.
No implementation, native probability evaluation or experiment.

**Result.** In the declared iid three-category observation model, no
decision rule with a fixed finite raw-draw budget can uniformly
distinguish the admitted baseline and perturbation families at arbitrarily
small positive scales with both low false-positive probability and high
power. This includes arbitrary randomized rules, stopping by the budget,
and procedures using a known invertible observation channel.

The conclusion is not exact-law nonidentifiability. For each positive
scale, the population laws may remain distinct. Their finite-observation
laws nevertheless become arbitrarily close. Abstention can preserve low
conditional error only by making decision coverage vanish along this
limit; small unconditional wrong-label probabilities alone are trivial.

The retained independent review of [the observation-channel theorem](P4_OBSERVATION_CHANNEL.md) already previewed a finite-budget TV argument. This
packet makes the full proof, quantifiers, randomization/stopping scope
and abstention trade-off explicit; it is not an unexposed independent
rediscovery of that argument.

## 1. Conditional occurrence and the positive-scale source pair

Assume the eligible subclass is nonempty: there is an **actually
admitted** canonical prefix satisfying the inherited held calibration
and its own conditional \(\Xi>1\), regular perturbation construction,
fixed amplitude, positivity neighborhood and full-law requirements.
Fix one such member, one admitted \(\lambda\) in its neighborhood,
and one fixed admissible old-mark distribution.

This is a conditional choice of an actual law, not construction of a
law from freely selected scalar coefficients. The sources do not
resolve an actual numerical \(\Xi\) comparison here. If the occurrence
premise fails, there is no baseline/perturbation instance of this
conditional test problem; this packet does not supply one.

Let \(B_\rho,Q_\rho\) be the corresponding complete baseline and regular
perturbed P4 child-shape laws at admitted positive common scales.
Use the already accepted sequence of scales \(\rho\downarrow0\)
available for this fixed member and parameter. The proof only needs
such a sequence of simultaneous admissible scales; it does not require
new coefficient or capacity calculations.

Retain all child shapes. Aggregate the two selected shapes as
\(0=K_0\) (empty birth) and \(4=K_4\) (C4 birth/T9), and every other
shape as \(O=\mathrm{OTHER}\), including the full-birth shape \(K_f\).
For \(H\in\{B,Q\}\), write the resulting complete probability vector as
\[
 p_{H,\rho}
   =\bigl(\nu_H(1-q_H),\,\nu_Hq_H,\,1-\nu_H\bigr),\qquad
 \nu_H=p_{H,\rho}(0)+p_{H,\rho}(4)>0,\quad 0<q_H<1.        \tag{1}
\]
Here \(\nu_H,q_H\) can depend on \(\rho\); no numerical value is evaluated.

[The prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md)'s calibrated coordinate inequalities and [the diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s conditioning
give
\[
 q_B\le\frac{648}{673}
       <\frac{22617}{23117}<q_Q.                           \tag{2}
\]
In particular the two aggregated population laws are different at each
admitted positive scale. We do not need to enlarge these native laws
to every point of the conservative ratio envelopes.

The accepted fixed-prefix rare-event limit is the load-bearing input:
every proper shape mass is \(O(\rho)\), while the unchanged full-birth
mass tends to one. Consequently
\[
 \nu_B\longrightarrow0,\quad \nu_Q\longrightarrow0,\quad
 p_{B,\rho},p_{Q,\rho}\longrightarrow(0,0,1).              \tag{3}
\]
Only this accepted limit and the positive-scale source validity are
used below. **Scale zero is not an admitted member.** The tests compare
two actual positive-scale laws; the boundary distribution is a device
for proving their finite-observation closeness, not a new null law.

A uniform guarantee over the larger admitted family must in particular
hold on this one fixed-member baseline/perturbation sequence. An
obstruction on the sequence therefore suffices to reject that
uniform guarantee, conditional on its occurrence.

## 2. Observation model and fixed raw budget

Let \(\mathcal X=\{0,4,O\}\). Under either hypothesis, the true categories
\(X_1,\ldots,X_N\) are iid from the same fixed source law for that run.
Use a single fixed row-stochastic matrix \(M\), shared across the two
hypotheses and all scales being compared:
\[
 M=
 \begin{pmatrix}
 a&b&1-a-b\\
 c&d&1-c-d\\
 e&f&1-e-f
 \end{pmatrix}.                                           \tag{4}
\]
Rows are true categories, columns reported categories. Retain [the observation-channel theorem](P4_OBSERVATION_CHANNEL.md)'s
nonnegative rows and positive diagnostic detection probabilities
\(a+b>0,\ c+d>0\). The proof below does not need positive orientation,
leakage, or invertibility; known invertible channels are included.

Conditional on the whole true sequence, reported categories are
independent with transition probabilities \(M_{X_n,y}\).
Summing over the iid true categories gives iid reported categories
with one-draw laws
\[
 P_\rho=p_{B,\rho}M,\qquad Q_\rho=p_{Q,\rho}M.              \tag{5}
\]
The full \(N\)-observation laws are \(P_\rho^{\otimes N}\) and
\(Q_\rho^{\otimes N}\). The same aggregate OTHER row must actually apply
to all source shapes collapsed into OTHER; this is an additional
observation-model premise, not a consequence of the aggregation itself.

Here \(N\) is a fixed nonnegative integer **raw-draw** cap, not a target diagnostic
count. Every reported OTHER outcome counts. Nothing is assumed about
a physical classifier, calibration, repeated preparation or empirical
availability beyond the stated hypothetical model.
A growing trajectory with changing parents is not iid fixed-law repetition.

## 3. Elementary finite-alphabet total variation

For probability vectors \(P,Q\) on a finite alphabet, define
\[
 d_{\rm TV}(P,Q)=\frac12\sum_x|P(x)-Q(x)|.                  \tag{6}
\]
Let \(r(x)=P(x)-Q(x)\). Since \(\sum_xr(x)=0\), the sum of its positive
entries and the absolute sum of its negative entries both equal (6).
It follows that, for every subset \(A\),
\[
 |P(A)-Q(A)|\le d_{\rm TV}(P,Q),
\]
with equality for the positive-entry set. More generally, for every
function \(0\le\phi(x)\le1\),
\[
 \left|\sum_x\phi(x)(P(x)-Q(x))\right|
       \le d_{\rm TV}(P,Q).                               \tag{7}
\]
Indeed its positive contribution is at most the full positive mass and
its negative contribution at least minus the full negative mass.

The pointwise identity
\(\min(P(x),Q(x))=(P(x)+Q(x)-|P(x)-Q(x)|)/2\) also gives
\[
 \sum_x\min(P(x),Q(x))=1-d_{\rm TV}(P,Q).                   \tag{8}
\]
These facts supply every event/test and overlap bound used here.

### A shared observation channel cannot increase TV

For any row-stochastic matrix \(K\), finite sums and the triangle
inequality imply
\[
 \begin{aligned}
 2d_{\rm TV}(PK,QK)
 &=\sum_y\left|\sum_x(P(x)-Q(x))K_{xy}\right|\\
 &\le\sum_x|P(x)-Q(x)|\sum_yK_{xy}
  =2d_{\rm TV}(P,Q).
 \end{aligned}                                           \tag{9}
\]
Nonnegativity and row sums one, not invertibility, give this bound.

### Independent products: proof without a coupling theorem

Let \(d=d_{\rm TV}(P,Q)\) and \(r_*(x)=\min(P(x),Q(x))\).
On every length-\(N\) vector,
\[
 \min\!\left\{\prod_{i=1}^N P(x_i),\prod_{i=1}^N Q(x_i)\right\}
       \ge\prod_{i=1}^N r_*(x_i).
\]
Summing and using (8), the two product laws have common mass at least
\((\sum_xr_*(x))^N=(1-d)^N\). Hence
\[
 d_{\rm TV}(P^{\otimes N},Q^{\otimes N})
       \le1-(1-d)^N\le\min\{1,Nd\}.                       \tag{10}
\]
For \(N\ge1\), the last bound follows directly from
\(1-(1-d)^N=d\sum_{j=0}^{N-1}(1-d)^j\le Nd\).
The zero-observation case has identical empty-vector laws and TV zero.

## 4. Quantitative rare-mass bound for all N-observation laws

Define the larger true diagnostic mass
\[
                      v_\rho=\max\{\nu_B,\nu_Q\}.
\]
Directly from (1),
\[
 \begin{aligned}
 d_{\rm TV}(p_{B,\rho},p_{Q,\rho})
 &=\tfrac12\bigl(
 |\nu_B(1-q_B)-\nu_Q(1-q_Q)|+
 |\nu_Bq_B-\nu_Qq_Q|+|\nu_B-\nu_Q|\bigr)\\
 &\le\tfrac12(\nu_B+\nu_Q+|\nu_B-\nu_Q|)
  =v_\rho.
 \end{aligned}                                           \tag{11}
\]
Equivalently, the shared mass at OTHER alone is at least \(1-v_\rho\).
This sharper bound is sufficient without using the magnitude of the
conditional-label separation.

Apply (9) to \(M\), then (10) to the reported laws:
\[
 \boxed{
 \begin{aligned}
 d_\rho&:=d_{\rm TV}(P_\rho,Q_\rho)\le v_\rho,\\
 D_{N,\rho}
   &:=d_{\rm TV}(P_\rho^{\otimes N},Q_\rho^{\otimes N})\\
   &\le1-(1-d_\rho)^N
    \le \varepsilon_{N,\rho}:=1-(1-v_\rho)^N
    \le\min\{1,Nv_\rho\}.
 \end{aligned}}                                         \tag{12}
\]
The inequality replacing \(d_\rho\) by \(v_\rho\) uses that
\(1-(1-x)^N\) is increasing on \([0,1]\).
Thus \(D_{N,\rho}\to0\) for every fixed finite \(N\) along (3);
indeed the displayed upper bound is \(O(N\rho)\) for this fixed pair.
There is no evaluated coefficient or native numerical effect size here.

The common limit can also be seen at the reported-law level. Let \(R\)
be the OTHER row of \(M\), and let \(V_H\) be the convex mixture of its
0 and 4 rows with weights \(1-q_H,q_H\). Then
\[
 P_\rho=(1-\nu_B)R+\nu_B V_B,\qquad
 Q_\rho=(1-\nu_Q)R+\nu_Q V_Q.
\]
Since TV between probability vectors is at most one,
\(d_{\rm TV}(P_\rho,R)\le\nu_B\) and likewise for \(Q_\rho\).
Equation (10) therefore makes both \(N\)-observation laws tend to
\(R^{\otimes N}\) in TV. No restriction on whether \(e+f\) is zero
or positive is needed. Leakage is not necessary for this
fixed-raw-budget obstruction: the identity channel is already included.

## 5. Arbitrary randomized decisions and stopping by N

An admissible decision uses only the reported observations, the known
fixed channel and declared model information, together with exogenous
randomization. Its output is B, Q, or A=ABSTAIN.

The formal requirement is one **common decision kernel conditional on
the full reported vector**, the same under both hypotheses.
A sufficient implementation is a random seed \(U\) independent of
the hypothesis, true draws and channel randomness, and a measurable
output function of \(U\) and the observed data. Marginal independence
of \(U\) from the hypothesis alone would not exclude a seed correlated
with hidden source information; such an oracle is not allowed.

A stopping time \(T\le N\), based on reported prefixes and this seed,
with a terminal decision at \(T\), fits the same formulation. For the
proof, mathematically complete the iid run to length \(N\) even if the
procedure stops early. Given a full vector \(y\), run the same stopping
and output logic on its prefixes and integrate only over \(U\):
\[
 K_j(y)=P_U(\hbox{the procedure outputs }j\hbox{ on }y),
 \quad j\in\{B,Q,A\}.
\]
These are nonnegative, sum to one, and are the same under either
hypothesis. The completion requires no actual acquisition after stopping.
No source-preparation changes, adaptive interventions, uncounted
observations or hypothesis-dependent side information are admitted.

For each output event \(E\), its conditional probability \(K_E(y)\)
lies in \([0,1]\). Applying (7) yields
\[
 |P_B(\hbox{output}\in E)-P_Q(\hbox{output}\in E)|
       \le D_{N,\rho}\le\varepsilon_{N,\rho}.              \tag{13}
\]
Here \(P_B,P_Q\) denote probabilities over both the reported run and
the independent decision randomization at the fixed scale.
Equivalently (9) contracts the TV of the three-output laws.

This covers arbitrary measurable randomized decision rules on the
finite observed vector, not just threshold statistics or the first
diagnostic labels. Any statistic, known-channel correction, intermediate
estimate or bounded stopping transcript followed by a decision still
induces such a kernel. The bound does not assume computational limits.

## 6. Forced binary decisions: precise testing lower bound

First forbid ABSTAIN. Define
\[
 \alpha_\rho=P_B(Q),\qquad \beta_\rho=P_Q(B).
\]
Apply (13) to output Q:
\[
 \begin{aligned}
 \alpha_\rho+\beta_\rho
 &=1-\bigl(P_Q(Q)-P_B(Q)\bigr)\\
 &\ge1-D_{N,\rho}
 \ge(1-v_\rho)^N.
 \end{aligned}                                          \tag{14}
\]
Therefore
\[
 \max\{\alpha_\rho,\beta_\rho\}
        \ge\frac{1-D_{N,\rho}}2
        \ge\frac{(1-v_\rho)^N}{2}.                        \tag{15}
\]
These bounds hold for every admissible rule at each actual positive
scale. They do not set either individual error to \(1/2\); a rule may
favor one hypothesis at the other's expense.

For every fixed finite \(N\), no common rule can guarantee
\(\alpha_\rho\le\bar\alpha\) and \(\beta_\rho\le\bar\beta\)
uniformly over all admitted small scales if
\(\bar\alpha+\bar\beta<1\).
As \(v_\rho\to0\), the right side of (14) approaches one.

More precisely, on any two-label class containing this paired sequence,
\[
 \inf_{\text{admissible forced rules}}
     \ \sup_{\text{admitted pair scales }\rho}
       \max\{P_B(Q),P_Q(B)\}=\frac12.                     \tag{16}
\]
The lower bound follows from (15). A hypothetical independent fair-coin
decision gives the upper bound \(1/2\) for every source law. This is a
mathematical comparison, not an executed procedure or recommendation.

As a coarse necessary raw-budget condition at one scale, any forced
test with error sum at most \(s<1\) must satisfy
\[
                Nv_\rho\ge1-s,                          \tag{17}
\]
by (12) and (14). This is not sufficient and supplies no numerical
budget without applicable native availability information. It simply
exposes why one finite uniform cap cannot suffice as \(v_\rho\to0\).

## 7. ABSTAIN: false labels, failure to reject, power and coverage

For the three-output rule define, separately under each true hypothesis,
\[
 \begin{gathered}
 a=P_B(Q),\qquad b=P_Q(B),\\
 z_B=P_B(A),\quad z_Q=P_Q(A),\qquad
 c_B=1-z_B,\quad c_Q=1-z_Q,\\
 \pi=P_Q(Q)=1-b-z_Q,\qquad
 \beta_{\rm fail}=P_Q(B\hbox{ or }A)=b+z_Q=1-\pi .
 \end{gathered}                                         \tag{18}
\]
Thus \(a,b\) are unconditional wrong-label probabilities,
\(z_H\) abstention probabilities, \(c_H\) decision coverages,
\(\pi\) power, and \(\beta_{\rm fail}\) all failures to reject B,
**including abstention**.

Equation (13) for output Q gives
\[
 \boxed{\quad a+\beta_{\rm fail}\ge1-D_{N,\rho},
                  \qquad \pi\le a+D_{N,\rho}.\quad}       \tag{19}
\]
In particular, uniform false-positive control \(a\le\bar\alpha\)
forces \(\pi\le\bar\alpha+\varepsilon_{N,\rho}\) along the paired
sequence. It cannot coexist with uniform power at least
\(1-\bar\beta\) when \(\bar\alpha+\bar\beta<1\).

It would be false to replace \(\beta_{\rm fail}\) by \(b\) in (19)
without accounting for abstention. Always returning A gives \(a=b=0\),
but coverage and power zero and \(\beta_{\rm fail}=1\).

There is a useful bound on wrong labels together with coverage.
Applying (13) to output B gives
\[
 P_B(B)-P_Q(B)=c_B-a-b\le D_{N,\rho}.
\]
Applying it to output Q similarly gives \(c_Q-a-b\le D_{N,\rho}\).
Hence
\[
 \boxed{\quad
 a+b\ge\max\{c_B,c_Q\}-D_{N,\rho}
      =1-\min\{z_B,z_Q\}-D_{N,\rho}.
 \quad}                                                  \tag{20}
\]
Negative right sides are harmless lower bounds. This formula says
exactly why small wrong-label probabilities alone do not certify
frequent correct decisions.

### Conditional accuracy forces vanishing coverage

When \(c_B,c_Q>0\), the conditional-on-decision errors are \(a/c_B\)
and \(b/c_Q\). They are not posterior probabilities that a reported
label is true. Suppose a rule promises
\[
 a\le\eta_B c_B,\qquad b\le\eta_Q c_Q,\qquad
 0\le\eta_B,\eta_Q,\qquad \eta_B+\eta_Q<1.              \tag{21}
\]
These inequalities are meaningful even when a coverage is zero, but
the corresponding conditional probability is then **undefined**,
not zero.

Combining (20) with
\(a+b\le(\eta_B+\eta_Q)\max\{c_B,c_Q\}\) proves
\[
 \boxed{\quad
 \max\{c_B,c_Q\}\le
       \frac{D_{N,\rho}}{1-\eta_B-\eta_Q}
       \le\frac{\varepsilon_{N,\rho}}{1-\eta_B-\eta_Q}.
 \quad}                                                  \tag{22}
\]
One may cap the right side at one.
This holds for asymmetric tolerances as well. For two 5% conditional
tolerances it is \( \max(c_B,c_Q)\le D_{N,\rho}/0.9\).

Consequently, fixed-\(N\) conditional accuracy with tolerance sum below
one can persist along the rare-event limit only if both decision
coverages tend to zero. In that situation power also tends to zero
and failure to reject, including abstention, tends to one.
A uniform positive coverage requirement would contradict (22).

This does not say that low conditional error is itself impossible.
Under the identity channel, [the diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s unchanged rule can retain its
conditional guarantees while collection by its fixed cap becomes
arbitrarily unlikely. That is an admitted illustration of compatibility
with (22), not an execution and not a claim that every leaky channel
admits such a conditional procedure.
No bound on conditional-law TV is asserted by simply dividing or
conditioning (12) on a rare data-dependent event.

## 8. Known-channel invertibility does not evade the bound

If \(M\) is known and invertible, equality of population vectors
\(p_BM=p_QM\) would imply \(p_B=p_Q\).
Thus the positive-scale distinction (2) survives such a channel;
at the population level \(p=\widehat pM^{-1}\).

A finite observed sample is not an exact population vector.
An inverse-based estimate followed by any admitted decision is still
a common data-processing kernel covered by (13)–(22).
Neither matrix invertibility nor unlimited computation increases
the information in the fixed \(N\) observations.

This distinction holds even for an invertible leaky channel. [The observation-channel theorem](P4_OBSERVATION_CHANNEL.md)'s
illustration with identity diagnostic rows and OTHER row
\((e,f,1-e-f)\), \(0<e+f<1\), has determinant \(1-e-f>0\).
The present TV bound still applies. Reported diagnostics can remain
abundant because of leakage while the underlying informative masses
vanish; conditioning on reported collection does not manufacture
uniform raw-budget power.

No general inverse-estimation programme, estimator, calibration method
or numerical conditioning analysis is opened here.

## 9. Exact conclusion and exclusions

The failed claim is **uniform fixed-finite-raw-budget testing** over a
class that includes the admitted arbitrarily small positive-scale pair:
one cannot simultaneously promise low false-positive probability and
high unconditional power, or low conditional error with uniformly
positive decision coverage, under this observation model.

The proof does **not** rule out:

- Distinct exact population laws at each positive scale, or pointwise
  identification/consistent testing as the budget increases for a fixed
  pair. It supplies no such operational procedure.
- Scale-dependent or unbounded raw budgets. The convergence in (12)
  is for fixed \(N\), not a claim that \(N(\rho)v_\rho\to0\) for every
  growing budget.
- Restricting the intended class by a separately justified positive
  availability/effect floor or other conditions excluding this limit.
  Such a restriction removes this particular obstruction; a floor
  alone does not prove usable channel separation, source validity,
  calibration or a finite-sample design.
- A genuinely different observation model with additional information,
  interventions or measurements. Those require new authorization and
  justification and are not silently included in this theorem.

The result is stronger than [the observation-channel theorem](P4_OBSERVATION_CHANNEL.md)'s conditional-label threshold
obstruction in one specific respect: it applies to **every** admitted
decision rule with fixed raw cap, not only the count-threshold rule.
It is not stronger in the sense of declaring every positive-scale
pair unidentifiable, or denying the earlier clean-channel conditional
error guarantee.

The application admission blocker is now explicit. A practical guarantee
must state its intended source class and scale/availability restrictions,
fixed preparation and observation model, false-positive/conditional
error targets, raw budget, coverage/power requirement and costs.
Source membership, the conditional occurrence premise, repeated
preparation, classifier/channel calibration and independently authorized
held-out evaluation remain unestablished operational requirements.

Foundational physics additionally requires a justified mapping from
accessible physical records to the native classes and observation
model, with a native prediction tested against appropriate rivals.
This conditional information bound neither falsifies nor validates DET,
its ontology, QM or gravity. Application success would not establish
those foundations, and a mathematical testing obstruction in this
selected optional family is not a physical observation.

[The diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s original numbers and decision rule, WIDTH_DIAGNOSTIC and
APPROXIMATE_WIDTH_DIAGNOSTIC remain unchanged. The width protocols were
not read or run. RET remains paused; historical failures and custody
limitations are unchanged.

## Public premises and evidence scope

The [observation-channel theorem](P4_OBSERVATION_CHANNEL.md) supplies the
declared common three-category channel, its additional observation premises,
rare-event limitations and the distinction between population invertibility
and finite observations. The
[diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md) supplies the prospective
iid repeated-draw model, conservative conditional-label bounds and unchanged
original rule with explicit abstention. The
[prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md) supplies the admitted
actual-law classes, held calibration and positive-scale sequence tending to
the rare-event boundary. Nonempty eligible occurrence remains conditional;
neither envelope inequalities nor freely selected scalar values construct
an admissible native instance.

The source manuscript expressly records prior exposure to a finite-budget
TV argument in the retained review of the observation-channel result. This
provenance is preserved above; the argument is not represented as a blinded
independent rediscovery. For source-manuscript construction, the retained
statement is:

All proofs are self-contained and manual.

This describes the author's construction, not later independent review or
its separate checks. Review and check records are retained privately.
Neither publication nor administrative correspondence checks supply a
machine proof, independent mathematical acceptance, operational admission
or original-custody authentication.

The limitation concerns every fixed finite raw budget in the declared iid
model and the admitted positive-scale pair, including the identity channel,
shared known invertible channels, exogenous randomization and stopping by
the cap. Distinct exact population laws at positive scale remain compatible
with it. Low conditional-on-decision error with tolerance sum below one
forces vanishing coverage along the rare-event limit; unconditional false
labels, failure to reject including ABSTAIN, power and coverage retain their
separate meanings. Scale-dependent budgets, a separately justified restricted
source class or genuinely different information are outside this obstruction.
No physical falsification or validation is supplied. The original numerical
design, frozen width protocols, RET pause and historical failures are unchanged.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. Public dependency links identify mathematical
premises; they do not supply private custody records or original certificate
reproduction. This edition is conditional mathematical exposition, not an
executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## Restricted half-scale availability counterpart

[Half-scale event availability](HALF_SCALE_EVENT_AVAILABILITY.md) states a
conditional positive counterpart on one actual eligible fixed prefix and
its own fixed compact positive-lambda neighborhood, after an optional
whole-domain half-scale law choice. With exact iid access it gives a
finite symbolic prospective raw cap, including abstention and coverage
accounting. It does not give arbitrary-scale or cross-prefix uniformity,
an evaluated numerical cap or physical validation. The fixed-budget
limitation above retains its original domain and quantifiers; the original
40,000 / 400,000 / 38,825 diagnostic design remains unchanged.
