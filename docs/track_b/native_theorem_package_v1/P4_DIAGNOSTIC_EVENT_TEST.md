# A prospective P4 diagnostic-event test with abstention

21 October 2026. Conditional probability theorem and prospective
observation design; no implementation or experiment.

**Result.** Under an explicitly additional iid repeated-draw model,
the accepted common relative separation gives a uniform finite
**diagnostic-event** error guarantee. It does not give uniform finite
**raw-draw** power. A predeclared capped test can make few wrong decisions
while almost always returning ABSTAIN when diagnostic events are rare.

A closed conservative example below fixes \(m=40{,}000\) diagnostic
events, \(N=400{,}000\) raw draws, a rational label threshold and
conditional error tolerances \(1/20\) in advance.
It proves those error bounds if enough events arrive, but makes no
promise that they will. These are prospective mathematical choices,
not measured native event rates, application readiness or authority to
run a protocol.

## 1. Admitted law classes and the new observation assumption

Let \(\mathcal P_B\) and \(\mathcal P_Q\) be [the prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md)'s baseline and regular
perturbed P4 child-shape classes, respectively, including its justified
within-label probability mixtures when their coordinate kernels are
measurable. Each constituent is a complete positive normalized law on
the same seven possible unmarked child shapes.

All inherited restrictions remain: actual valid canonical prefixes with
the specified common held identities, the same P4 parent and perturbation
support, admitted common scales, and each perturbed member's own regular
construction, fixed amplitude, neighborhood and conditional \(\Xi>1\).
The underlying prefix family may be a singleton. No freely chosen
coefficient tuple or actual \(\Xi\) value is supplied.

Write \(p_0=p(K_0)>0\), \(p_4=p(K_4)>0\), and
\[
 D=\{K_0,K_4\},\qquad
 \nu=p(D)=p_0+p_4>0,\qquad
 q=p(K_4\mid D)=\frac{p_4}{p_0+p_4}.                         \tag{1}
\]
Here \(\nu\) denotes event availability and \(q\) a conditional
Bernoulli probability, not a new native growth kernel.
Every other shape is classified as OTHER and remains in the complete
law and raw-draw count.

**Prospective iid assumption.** There is one fixed complete law \(p\)
in the declared null or perturbation class, and repeated observations
\(X_1,X_2,\ldots\) are iid from that law. Each draw is classified exactly
as \(K_0\), \(K_4\), or OTHER.

This assumption is additional. It is not implied by a single native
growth transition, fair newborn bits, a mixture formula, or a trajectory
whose parent changes after each birth.
Exact shape access and repeatable draws from the same conditional
experiment require separate implementation/observation justification.

The fixed law \(p\) may itself be a marginal mixture of admitted laws.
Assuming iid draws from that marginal is legitimate as a prospective
model, but is not a consequence of defining the mixture.
A law drawn once and held latent throughout a run is treated separately
in §7; its observations are generally not iid unconditionally.

## 2. Common diagnostic-label bounds

The accepted calibration is
\[
 C=\frac{648}{25},\qquad R_{\min}=\frac{3231}{125}
            =\frac{359}{360}C.
\]
Every baseline obeys \(p_4\le Cp_0\).
Every admitted perturbed law has multiplier \(h_9>7/4\), hence
\[
 p_4>\frac74 R_{\min}p_0
          =L p_0,\qquad L=\frac{22617}{500}>C.              \tag{2}
\]
These are inequalities on unnormalized shape coordinates, not on a
law conditioned by dropping OTHER.

They also hold for arbitrary hidden-mark and admitted-prefix/law
mixtures within each hypothesis. Integrate
\(p_4-Cp_0\le0\) or \(p_4-Lp_0>0\) over a probability measure
concentrated on the respective admitted laws.
Strict positivity survives because a bounded positive measurable
integrand has a positive integral; no uniform absolute margin is needed.
The mixture has positive \(p_0\). Averaging component ratios with the
original mixture weights would not be valid and is not used.

Since \(r\mapsto r/(1+r)\) is increasing for \(r>0\), (1)–(2) give
\[
 \boxed{\quad
 q\le u:=\frac{648}{673}\quad(p\in\mathcal P_B),\qquad
 q>\ell:=\frac{22617}{23117}\quad(p\in\mathcal P_Q).
 \quad}                                                       \tag{3}
\]
The strictly separated conservative endpoints have gap
\[
 \delta:=\ell-u
       =\frac{241425}{15557741}>\frac3{200}>0.               \tag{4}
\]
For the last comparison,
\(200(241425)=48285000>46673223=3(15557741)\).
No native probability or event availability has been evaluated.
Equation (3) is a conditional-label bound; \(\nu\) can still be
arbitrarily small.

## 3. A closed, predeclared capped rule

More generally fix, before observing the test data,
integers \(1\le m\le N\), a threshold \(u<\tau<\ell\),
and desired conditional error tolerances
\(0<\alpha_{\rm I},\alpha_{\rm II}<1\).
Set \(k=\lceil m\tau\rceil\). Before claiming the tolerances,
certify that the two binomial-tail bounds in §5 are at most those values;
predeclaring arbitrary counts and tolerances does not itself certify them.

Process raw draws until the earlier of the \(m\)-th diagnostic event
and draw \(N\). Count every OTHER draw toward the cap.

- If fewer than \(m\) diagnostics have arrived by the cap, output ABSTAIN.
- Otherwise let \(S_m\) count \(K_4\) among the **first** \(m\)
  diagnostic labels. Output PERTURBED if \(S_m\ge k\), and BASELINE
  if \(S_m<k\).

The labels are decisions within the two declared model families,
not proof of the null or certification of an arbitrary outside-family
input. Do not extend the cap, alter the threshold, replace unfavorable
labels or reclassify outcomes after seeing the run.

One fully specified conservative design is:

| Item | Prospective choice |
| --- | --- |
| Raw-draw cap | \(N=400{,}000\) |
| Target diagnostic count | \(m=40{,}000\) |
| Label threshold | \(\tau=(u+\ell)/2\) |
| Integer decision boundary | \(k=38{,}825=\lceil40{,}000(u+\ell)/2\rceil\) |
| Conditional type-I tolerance | \(\alpha_{\rm I}=1/20\) |
| Conditional type-II tolerance | \(\alpha_{\rm II}=1/20\) |
| Insufficient diagnostics | ABSTAIN, explicitly reported |

All quantities in this table are fixed exact numbers.
The cap is a declared mathematical budget, not a native cost estimate
or an availability-calibrated choice.
The count is conservative, not claimed minimal; exact binomial tails
can certify other predeclared designs without changing the diagnostic.

## 4. Why selection and stopping do not bias the diagnostic labels

Let \(D_n=\mathbf1_{\{X_n\in D\}}\), and let \(T_m\) be the raw index
of the \(m\)-th diagnostic event.
For the fixed iid law, \(D_n\) are iid Bernoulli(\(\nu\)).
Define the availability event
\[
 A=\{T_m\le N\}
    =\left\{\sum_{n=1}^N D_n\ge m\right\}.                  \tag{5}
\]
The full first \(N\) draws may be considered mathematically even when
the procedure stops earlier.

For any fixed indicator pattern \(d_1,\ldots,d_N\) with \(j\)
diagnostics, the conditional labels at those \(j\) selected positions
are independent Bernoulli(\(q\)). Indeed the joint categorical
probability factors into
\[
 \nu^j(1-\nu)^{N-j}
       \prod_{\text{diagnostic positions }s}
                         q^{z_s}(1-q)^{1-z_s}.              \tag{6}
\]
Conditioning on the pattern cancels its first factor.
For every pattern with \(j\ge m\), its first \(m\) label distribution
is therefore the same product law. Averaging over the patterns in \(A\)
gives exactly
\[
                         S_m\mid A\sim\operatorname{Bin}(m,q).
                                                               \tag{7}
\]
For \(N\ge m\) and \(\nu>0\), \(P(A)>0\).
Equivalently the diagnostic label sequence can be coupled independently
of the diagnostic-arrival indicators.

The stopping rule uses membership in \(D\), which is outcome-dependent,
but not the relative \(K_0/K_4\) label within \(D\).
Equation (6), rather than an unsupported assertion about censoring,
justifies the selection. A rule that stopped according to the accumulated
\(K_4\) labels, or a classifier with label-dependent missed events,
would require a different proof.

## 5. Exact tails and a self-contained conservative bound

Binomial counts increase with their success probability: couple them
as \(\sum_{j=1}^m\mathbf1_{\{U_j\le q\}}\) using independent uniform
\(U_j\). Thus (3) and (7) yield the finite-event bounds
\[
 \begin{split}
 e_{\rm I}
 &:=\sup_{\mathcal P_B}P(\mathrm{PERTURBED}\mid A)
 \le\sum_{j=k}^m {m\choose j}u^j(1-u)^{m-j},\\
 e_{\rm II}
 &:=\sup_{\mathcal P_Q}P(\mathrm{BASELINE}\mid A)
 \le\sum_{j=0}^{k-1}{m\choose j}\ell^j(1-\ell)^{m-j}.
 \end{split}                                                \tag{8}
\]
The alternative endpoint is conservative because its actual \(q>\ell\).
No evaluation of these tails or statistical test is performed here.

For an explicit analytic bound, let \(Y\) be Bernoulli(\(q\)) and
\(f(t)=\log E e^{t(Y-q)}\). Then \(f(0)=f'(0)=0\).
The second derivative is the variance of a Bernoulli variable under
exponential tilting, so \(0\le f''(t)\le1/4\).
Taylor's integral identity
\(f(t)=t^2\int_0^1(1-s)f''(st)\,ds\le t^2/8\)
holds for real \(t\), including negative \(t\).
For \(m\) independent labels, Markov's inequality and \(t=4\varepsilon\)
give
\[
 P\left(\frac1m\sum Y_j-q\ge\varepsilon\right)
 \le \exp(-2m\varepsilon^2).
\]
Using negative \(t\) gives the same bound for the lower tail.
This proves the concentration estimate here without an external
statistical reference.

The integer threshold introduces no hidden rounding error:
\(S_m\ge\lceil m\tau\rceil\) implies \(S_m/m\ge\tau\);
\(S_m<\lceil m\tau\rceil\) implies \(S_m/m<\tau\).
Consequently
\[
 e_{\rm I}\le e^{-2m(\tau-u)^2},\qquad
 e_{\rm II}\le e^{-2m(\ell-\tau)^2}.                         \tag{9}
\]
At the midpoint, both are at most \(e^{-m\delta^2/2}\).
A general sufficient event-count prescription is
\[
 m\ge\left\lceil\frac{2}{\delta^2}
      \max\{\log(1/\alpha_{\rm I}),\log(1/\alpha_{\rm II})\}
      \right\rceil.                                       \tag{10}
\]

For the fixed example in §3, (4) gives
\[
 e_{\rm I},e_{\rm II}
 \le e^{-40000\delta^2/2}
 <e^{-9/2}<\frac1{20}.                                     \tag{11}
\]
The last inequality follows already from the positive exponential series:
\[
 e^{9/2}>
 1+\frac92+\frac{(9/2)^2}{2}+\frac{(9/2)^3}{6}
          =\frac{493}{16}>20.
\]
These are hand-derived bounds for a prospective design, not numerical
native effect estimates, synthetic execution or observed error rates.

## 6. Availability, unconditional decisions and raw-draw power

For a fixed iid law define its exact abstention probability
\[
 b_N(\nu)=P(A^c)
       =\sum_{j=0}^{m-1}{N\choose j}\nu^j(1-\nu)^{N-j},
 \qquad a_N(\nu)=1-b_N(\nu).                                \tag{12}
\]
For any design whose bounds (8) or (9) have been certified below its
declared tolerances, the following guarantees apply. The selection proof
gives conditional error control, not an assurance that \(A\) occurs.

| Quantity | Guaranteed bound |
| --- | --- |
| Wrong PERTURBED decision under baseline, conditional on \(A\) | \(\le\alpha_{\rm I}\) |
| Wrong BASELINE decision under perturbation, conditional on \(A\) | \(\le\alpha_{\rm II}\) |
| Unconditional wrong PERTURBED decision under baseline | \(\le\alpha_{\rm I}a_N(\nu)\le\alpha_{\rm I}\) |
| Unconditional wrong BASELINE decision under perturbation | \(\le\alpha_{\rm II}a_N(\nu)\le\alpha_{\rm II}\) |
| Power \(P(\mathrm{PERTURBED})\) under perturbation | \(\ge(1-\alpha_{\rm II})a_N(\nu)\), and \(\le a_N(\nu)\) |
| ABSTAIN under either family | exactly \(b_N(\nu)\) |

Here the two declared tolerances concern wrong labels among runs that
reach \(m\) diagnostic events. If “type-II error” instead means
**all failures to reject the null**, including ABSTAIN, its bound is
\[
 P_{\mathcal P_Q}(\hbox{not PERTURBED})
 \le b_N(\nu)+\alpha_{\rm II}(1-b_N(\nu)),                   \tag{13}
\]
not merely \(\alpha_{\rm II}\).
ABSTAIN must not be omitted from reporting or silently counted as success.

Without a positive availability lower bound, the raw cap cannot give
uniform positive power. Since
\(E\sum_{n=1}^N D_n=N\nu\), Markov's inequality gives
\[
                     a_N(\nu)\le \frac{N\nu}{m}.            \tag{14}
\]
The admitted common-scale construction allows \(\rho\downarrow0\)
at a fixed eligible prefix and fixed \(\lambda\).
Every proper shape probability, including \(p_0,p_4\), is then
\(O(\rho)\), so \(\nu\to0\). For any finite fixed \(N,m\),
(14) implies \(a_N(\nu)\to0\), ABSTAIN approaches one and power
approaches zero. Uniform finite-event accuracy and vanishing
unconditional power are therefore compatible.

### What a certified availability bound would add

If an additional justified bound \(\nu\ge\nu_{\min}>0\) is available
for the tested iid law or uniformly for the intended class, then
binomial monotonicity gives
\[
 b_N(\nu)\le b_N(\nu_{\min}).
\]
For \(N\nu_{\min}>m-1\), the same concentration proof also gives
\[
 b_N(\nu)\le
 \exp\left[-2N\left(\nu_{\min}-\frac{m-1}{N}\right)^2\right].
                                                               \tag{15}
\]
A prospective cap chosen so that this expression, or the exact
binomial tail, is at most \(\zeta\) yields
\[
 P_{\mathcal P_Q}(\mathrm{PERTURBED})
      \ge(1-\alpha_{\rm II})(1-\zeta),\qquad
 P(\hbox{ABSTAIN})\le\zeta.                                 \tag{16}
\]
The example cap in §3 has **no** such guarantee without a supplied
\(\nu_{\min}\). The cap must not be enlarged after inspecting the run
and still be described as the original design.

A model-certified bound would require applicable native probability
information, not just the relative ratio gap.
An empirically estimated lower bound would require its own declared
measurement/classification model and uncertainty coverage.
If an independent, pre-test calibration justifies the bound with
failure probability at most \(\gamma\), a subsequent design may
budget that failure as well: total failure to make the correct
perturbation decision is at most
\(\gamma+\zeta+\alpha_{\rm II}\), conservatively.
This statement requires the promised calibration coverage and iid
test validity conditional on the calibration; a data-dependent plug-in
value alone gives no such guarantee.
No calibration study is carried out or authorized here.

[The baseline-scale theorem](BASELINE_SCALE_THEOREM.md)'s optional half-scale results do not give a numerical
\(\nu_{\min}\) for the arbitrary-scale family used here.
No actual scale, coefficient table, \(\Xi\), native event rate or
physical acquisition cost is selected.

## 7. A fixed latent law is a separate model

Suppose instead that a latent index \(Z\) is selected once for a run,
and conditional on \(Z=z\) the observations are iid from \(p_z\).
Its index distribution is concentrated on admissible laws of one
declared hypothesis, not a mixture of hypothesis labels.

In general the unconditional draws are dependent, and neither the raw
diagnostic count nor the selected-label count is binomial at the
marginal mean parameter. Conditional on \(Z=z\), however, §§4–6 apply
with \(q_z,\nu_z\).

After conditioning on \(A\), the index distribution is reweighted by
\[
                         P(A\mid Z=z)=a_N(\nu_z).
\]
Thus \(S_m\mid A\) is generally a mixture of
\(\operatorname{Bin}(m,q_z)\) under these reweighted indices, not one
binomial law. Because (8)–(11) bound every component uniformly,
\[
 P(\mathrm{wrong}\mid A)\le\alpha,\qquad
 P(\mathrm{wrong})\le\alpha P(A),                            \tag{17}
\]
using the appropriate \(\alpha_{\rm I}\) or \(\alpha_{\rm II}\).
The denominator \(P(A)>0\) follows from \(\nu_z>0\) almost surely
and \(N\ge m\).
The abstention probability is
\[
                       E[b_N(\nu_Z)],                       \tag{18}
\]
not \(b_N(E\nu_Z)\).

A uniform almost-sure lower bound \(\nu_Z\ge\nu_{\min}\) gives (15)–(16).
A lower bound on \(E\nu_Z\) alone does not supply that same guarantee:
a positive fraction of runs may have arbitrarily small \(\nu_Z\),
balanced by higher-availability runs. This does not mean that a mean
bound gives no weaker information: the event that the first \(m\) raw
draws are all diagnostic implies \(A\), so
\(P(A)\ge E[\nu_Z^m]\ge(E\nu_Z)^m\) by convexity.
It is not the componentwise binomial-tail guarantee in (15).
No assertion of iid marginal observations, arbitrary dependent sampling,
adaptive preparation or validity along a native growing trajectory is made.

## 8. Event complexity, raw cost and implementation admission

The event-count requirement (10) is of order
\(\delta^{-2}\log(1/\alpha)\) for equal tolerances under this conservative
bound. It counts diagnostic labels, not raw observations.

For a fixed iid law, waiting gaps between diagnostics are independent
geometric variables with mean \(1/\nu\); the tail sum
\(\sum_{t\ge0}(1-\nu)^t=1/\nu\) gives
\[
 E[T_m]=m/\nu,\qquad
 E[\min(T_m,N)]
   =\sum_{t=0}^{N-1}P(\operatorname{Bin}(t,\nu)<m)
   \le\min\{N,m/\nu\}.                                     \tag{19}
\]
These are mathematical raw-draw costs.
Under a fixed latent law, conditional expectation is \(m/\nu_Z\);
its unconditional mean may be infinite if \(E[1/\nu_Z]=\infty\),
despite every component having positive availability.

The rule needs at most \(N\) exact classifications and linear-in-\(N\)
counter updates, with \(O(\log N+\log m)\) bits for the counters.
These operation counts are not a total bit-complexity or classification
runtime bound. They do not price acquiring a complete child order, resetting or
preparing the same parent experiment, resolving noisy relations, computing
native probabilities, or validating a classifier.
No runtime, sample-collection system or benchmark has been implemented.

Before any implementation could be admitted, a separate prospective
record would need to establish:

- The fixed diagnostic \(D=\{K_0,K_4\}\), exact category definitions,
  tested P4 parent/support and the null/perturbation families.
- The sampling model: iid fixed-law repetition, or the explicitly
  justified conditional-iid latent model; no unproved trajectory
  substitution.
- A predeclared \(N,m,k,\alpha_{\rm I},\alpha_{\rm II}\), any availability
  target \(\zeta\), and immutable handling/reporting of ABSTAIN,
  failures and all OTHER draws.
- Exact-classifier assumptions or a separately justified error model;
  known physical/data access to the relevant complete order.
- Source-law admissibility and native numerical availability evidence
  appropriate to any raw-cost/power claim, including the conditional
  occurrence and regular-construction premises.
- Measurement, preparation, classification and computational cost
  accounting, distinct from diagnostic-event count.
- Independent held-out evaluation under separately authorized rules,
  with no retuning of the fixed diagnostic on evaluation outcomes.

This is an admission checklist, not a plan authorizing those actions.
The existing WIDTH_DIAGNOSTIC and APPROXIMATE_WIDTH_DIAGNOSTIC protocols
remain frozen and unaffected. Neither was read or executed.
RET remains paused. No new sampler, benchmark or frozen diagnostic
change is supplied.

Foundational physics would still require an explicit native physical
prediction and an observation channel.
Application success would not establish DET or its ontology.
The present yield is a closed prospective mathematical test with honest
abstention and observation assumptions.

## Public premises and evidence scope

The [prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md) supplies the admitted
actual-law classes, held calibration, common separator and measurable
within-label mixture premises. The family may be a singleton; no second
distinct qualifying prefix is established. The
[marking-mixture theorem](P4_MARKING_MIXTURES.md) supplies the hidden-mark
comparison on the inherited neighborhood. The
[nuisance-identifiability theorem](P4_NUISANCE_IDENTIFIABILITY.md) distinguishes
exact model-label separation from parameter recovery and finite-sample
stability. The [child-shape theorem](P4_CHILD_SHAPE_OBSERVATION.md) supplies
intrinsic recognition of the diagnostic shapes under complete exact order
access.

The [baseline-scale theorem](BASELINE_SCALE_THEOREM.md) states the admitted
common-scale construction and its distinct optional half-scale prescription.
The [regular-family theorem](REGULAR_OBSERVABLE_FAMILY.md) supplies the
established regular construction for its admitted fixed instance. Each
additional perturbed prefix must justify its own construction, neighborhood,
fixed amplitude and conditional premises as required by the prefix-family
theorem. None of these sources supplies a numerical event availability for
the arbitrary-scale family used here.

The probability proofs and rational comparisons in the source manuscript
were manual and self-contained. That manuscript used no external technical
source, scientific executor, synthetic arithmetic program, native sampler
or statistical test. Independent review and its separate checks are recorded
in the retained private evidence.

The repeated iid draws and exact classification are additional prospective
observation assumptions. The fixed latent-law model has its separate
conditional-iid argument. Conditional label-error bounds concern runs that
reach the declared diagnostic count; they do not give a uniform probability
of reaching it before the raw-draw cap. ABSTAIN and all OTHER draws retain
their stated accounting. The exact illustrative choices are prospective
mathematical design values, not native effect estimates, implemented tests,
application readiness or a physical observation channel. The existing frozen
protocols and RET pause remain unchanged.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. Public dependency links identify mathematical
premises; they do not supply private custody records or original certificate
reproduction. This edition is conditional mathematical exposition, not an
executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## Transfer through a declared observation channel

The [observation-channel manuscript](P4_OBSERVATION_CHANNEL.md) adds one
fixed common memoryless three-category channel. Without OTHER leakage,
positive determinant preserves a same-oriented conditional gap, while the
original numerical design needs its own error certificate. Fixed positive
leakage removes the uniform gap in the admitted rare-event limit; frequent
reported events do not establish genuine diagnostic availability. A separate
restricted contamination premise can restore a bounded guarantee. The
original design and ABSTAIN remain unchanged; no physical calibration is
supplied.
