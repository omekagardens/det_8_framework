# P4 diagnostic separation through a declared observation channel

21 October 2026. Conditional probability theorem and rare-event
obstruction; no implementation, calibration or experiment.

**Result.** With no OTHER-to-diagnostic leakage, missed/confused labels
preserve a positive same-oriented conditional gap exactly when the
diagnostic channel has positive determinant. The gap and decision
threshold change in general; the original numerical design is not
automatically certified. With any fixed positive OTHER leakage, the
admitted rare-native-event limit sends both observed conditional label
probabilities to the same value. A uniform positive gap then fails.
A separately justified bound on relative contamination can restore a
bounded conditional guarantee on a restricted class.

These statements concern the explicitly declared three-category channel.
They do not establish that a physical channel exists or is calibrated,
select an actual native occurrence, or validate DET.

## 1. Accepted source laws and conservative envelopes

Retain [the prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md)'s complete positive P4 child-shape laws and [the diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s two
hypotheses, BASELINE and PERTURBED. The parent is
\(P_4=C_4\oplus A_2\); \(K_0\) is the empty-birth shape and \(K_4\)
the C4-birth/T9 shape. Every remaining shape, including the full-birth
shape \(K_f\), is in OTHER. No shape is deleted from the source law.

All original membership conditions remain: actual valid canonical
prefixes and common held calibration, the specified parent and support,
admitted scales, and each perturbed member's own regular construction,
fixed amplitude, neighborhood and conditional \(\Xi>1\). Scalar bounds
alone do not establish membership or an actual \(\Xi\) comparison.
The qualifying prefix class may be a singleton. This is not a theorem
about arbitrary DET laws.

For the aggregated complete law write
\[
 (p_0,p_4,p_O)=(\nu(1-q),\nu q,1-\nu),\qquad
 p_0,p_4>0,\quad 0<q<1,\quad \nu>0.
\]
Here \(\nu\) is true diagnostic availability, not an observed event rate.
The accepted linear bounds, including admitted measurable within-label
mixtures, are
\[
 p_4\le Cp_0\quad(B),\qquad p_4>Lp_0\quad(Q),\qquad
 C=\frac{648}{25},\quad L=\frac{22617}{500}.
\]
They imply the conservative envelopes
\[
 q\in(0,u]\quad(B),\qquad q\in(\ell,1)\quad(Q),\qquad
 u=\frac{648}{673}<\ell=\frac{22617}{23117},
\]
\[
 \delta=\ell-u=\frac{241425}{15557741}>\frac3{200}.       \tag{1}
\]
Equivalently the ratio \(r=p_4/p_0\) obeys \(0<r\le C\) or \(r>L\).
[The prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md) also bounds the baseline ratio below by \(3231/125\);
using that tighter lower endpoint would not change the upper-baseline/
lower-perturbation separation derived below.

Whenever an endpoint condition is called necessary and sufficient
**over the envelopes**, the quantifier includes every mathematical
\(q\) in these declared intervals. It does not assert that every such
\(q\), or a sequence approaching \(\ell\), is realized by the smaller
native construction. Inherited source-law inequalities and mathematical
envelopes are not existence proofs for additional laws.

## 2. Additional observation model

Let \(X_n\in\{0,4,O\}\) be iid true categories from one fixed complete law.
Let \(Y_n\in\{0,4,O\}\) be the reported categories, through one fixed
row-stochastic matrix
\[
 M=
 \begin{pmatrix}
 a&b&1-a-b\\
 c&d&1-c-d\\
 e&f&1-e-f
 \end{pmatrix}.                                           \tag{2}
\]
Rows are true \(0,4,O\); columns are observed \(0,4,O\).
All entries are nonnegative, and
\[
 s_0=a+b>0,\quad s_4=c+d>0,\quad t=e+f,\qquad
 s_0,s_4,t\le1.
\]
Thus true diagnostic categories have positive detection probabilities,
but may be missed or confused.

Precisely, conditional on the entire true sequence, channel outputs
are independent and
\[
 P(Y_1=y_1,\ldots,Y_N=y_N\mid X_1,\ldots,X_N)
       =\prod_{n=1}^N M_{X_n,y_n}.                          \tag{3}
\]
The same matrix applies across the two hypotheses and every included
scale/source law. The aggregate OTHER row is a substantive assumption:
different OTHER shapes, hidden markings, nuisance parameters or
preparation histories must not silently change it. Neither false-positive
rates nor conditional independence follow from row stochasticity.

Equation (3) and iid true draws imply iid reported categories with law
\(\widehat p=pM\): summing the product over all true sequences factors
into \(\prod_n\sum_x p_xM_{x,y_n}\).
Repeated fixed-law preparation and a category-only memoryless channel
are additional premises, not consequences of fair newborn bits, a single
growth transition, or a trajectory whose parent changes.
No channel is measured, calibrated or physically constructed here.

## 3. Clean case: OTHER never produces a diagnostic event

First set \(e=f=0\). Define
\[
 s(q)=s_0(1-q)+s_4q>0,\qquad \Delta_M=ad-bc.
\]
Then the reported diagnostic availability and conditional label are
\[
 \widehat\nu=\nu s(q)>0,\qquad
 \widehat q=P(Y=4\mid Y\in\{0,4\})
    =\phi_M(q):=\frac{b(1-q)+dq}{s(q)}.                    \tag{4}
\]
In ratio form the same fractional-linear map is
\[
 \psi_M(r)=\frac{b+dr}{s_0+s_4r},\qquad
 \phi_M(q)=\psi_M\!\left(\frac q{1-q}\right).              \tag{5}
\]
Unequal detection rates alter the selected mixture; they cannot simply
be omitted when conditioning on detection.

Subtracting two fractions gives the exact identity
\[
 \phi_M(q_2)-\phi_M(q_1)
   =\frac{\Delta_M(q_2-q_1)}{s(q_1)s(q_2)}.               \tag{6}
\]
The numerator determinant follows from
\(d(a+b)-b(c+d)=ad-bc\).
Equivalently,
\(\phi'_M(q)=\Delta_M/s(q)^2\).
The sign is also that of \(d/s_4-b/s_0\): a detected true 4 must be
more likely to be called 4 than a detected true 0.

Put
\[
 U=\phi_M(u)=\frac{b+dC}{s_0+s_4C},\qquad
 V=\phi_M(\ell)=\frac{b+dL}{s_0+s_4L}.                     \tag{7}
\]
When \(\Delta_M>0\),
\[
 \widehat q_B\le U<V<\widehat q_Q,\qquad
 G:=V-U
   =\frac{\Delta_M\delta}{s(u)s(\ell)}
   =\frac{\Delta_M(L-C)}
          {(s_0+s_4C)(s_0+s_4L)}>0.                     \tag{8}
\]

**Clean-channel endpoint theorem.** For one fixed channel with
\(s_0,s_4>0\), there is a uniform positive same-oriented conditional
gap over the declared envelopes if and only if
\[
                    U<V\quad\Longleftrightarrow\quad\Delta_M>0.
\]
Necessity follows from (6): zero determinant makes every conditional
label probability equal; negative determinant reverses every ordered
pair. Sufficiency and the exact conservative infimum gap \(G\) follow
from (8), continuity at \(\ell\), and the closed baseline endpoint \(u\).
The perturbed endpoint itself need not belong to the envelope.

For a specified real threshold \(\tau_M\), distinguish:

- The noiseless-probability separator
  \(\widehat q_B\le\tau_M<\widehat q_Q\) for all envelope laws
  holds exactly when \(U\le\tau_M\le V\), given \(\Delta_M>0\).
  Equality at \(V\) is allowed because the perturbed endpoint is open.
- Uniform positive distances from the threshold on **both** sides
  hold exactly when \(U<\tau_M<V\).
- A finite-count error certificate is a statement about binomial tails,
  not merely either endpoint ordering. Section 4 supplies its exact test.

If \(\Delta_M<0\), the gap is reversed:
\(\widehat q_B\ge U>V>\widehat q_Q\). A reversed decision convention
would require a separately declared design; the existing one is unchanged.
If \(\Delta_M=0\), then
\(\phi_M(q)=b/s_0=d/s_4\), possibly 0 or 1.
This rejects conditional-label discrimination by this statistic, not
every use of the observation: availability may still depend on \(q\).
For \(\Delta_M>0\), both observed diagnostic categories have positive
probability for \(0<q<1\), so no conditional denominator singularity
is hidden in (7)–(8).

The conclusion is for a fixed matrix. Positive determinants across a
variable family of channels alone do not provide a common positive
gap or a common threshold; their gaps may shrink and their endpoints
may shift.

## 4. What happens to the original fixed design?

[The diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s design remains exactly
\[
 m_0=40{,}000,\quad N_0=400{,}000,\quad
 \tau_0=\frac{u+\ell}{2}=\frac{30201057}{31115482},\quad
 k_0=38{,}825,\quad \alpha_{\rm I}=\alpha_{\rm II}=1/20.
                                                               \tag{9}
\]
It counts the first \(m_0\) diagnostic labels if available by \(N_0\);
otherwise it reports ABSTAIN. No number, category, reporting rule or
frozen protocol is changed here.

For a clean channel with positive determinant, applying that same
numerical rule to reported categories is conditionally certified over
the full envelopes **if and only if** both endpoint tails satisfy
\[
 \sum_{j=k_0}^{m_0}{m_0\choose j}U^j(1-U)^{m_0-j}\le1/20,
 \qquad
 \sum_{j=0}^{k_0-1}{m_0\choose j}V^j(1-V)^{m_0-j}\le1/20.
                                                               \tag{10}
\]
Binomial monotonicity gives sufficiency; the closed baseline endpoint
and continuous approach to the open perturbed endpoint give the
envelope suprema and necessity. For the actual smaller native class,
(10) is sufficient, but necessity is not established without
endpoint attainability/approach. Equation (10) has not been numerically
evaluated for a measured channel.

When \(U<\tau_0<V\), a convenient sufficient check is
\[
 e^{-2m_0(\tau_0-U)^2}\le1/20,\qquad
 e^{-2m_0(V-\tau_0)^2}\le1/20.                              \tag{11}
\]
Integer rounding is already accounted for by \(k_0=\lceil m_0\tau_0\rceil\).
These conservative checks are not necessary replacements for (10).

Two explicitly invented, hand-calculated channels clarify the boundary.
They are neither native probability estimates nor empirical calibration.

**Equal misses, no confusion.** If \(a=d=s>0\), \(b=c=e=f=0\),
then \(\phi_M(q)=q\) and \(\widehat\nu=s\nu\).
The original conditional error certificate survives exactly; collecting
the events becomes harder when \(s<1\).

**Confusion with positive orientation.** For
\[
 M=
 \begin{pmatrix}
 3/4&1/4&0\\
 1/4&3/4&0\\
 0&0&1
 \end{pmatrix},
 \qquad \Delta_M=1/2,\quad \phi_M(q)=1/4+q/2<3/4,
\]
there is still a positive gap \(G=\delta/2\) and unchanged availability.
But Markov's inequality for the selected count yields
\[
 P_Q(S_{m_0}\ge k_0\mid A)<\frac{30000}{38825},
 \qquad
 P_Q(\mathrm{BASELINE}\mid A)>
                 \frac{8825}{38825}>\frac1{20}.
\]
The last comparison follows from \(20(8825)=176500>38825\).
Thus positive orientation does not preserve the original error
certificate, even for every actual alternative law under this
hypothetical channel.

A separately declared **hypothetical** design can instead use
\[
 \tau_M=(U+V)/2,\quad k'=\lceil m'\tau_M\rceil,\quad
 m'\ge\left\lceil\frac2{G^2}
       \max\{\log(1/\alpha_{\rm I}),\log(1/\alpha_{\rm II})\}
       \right\rceil,\qquad N'\ge m'.                       \tag{12}
\]
The centered Bernoulli exponential bound proved in [the diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md) gives
each conditional error at most \(e^{-m'G^2/2}\).
For the invented confusion matrix, \(m'=160000\) with its new midpoint
would reproduce the original conservative exponent; that is only
arithmetic illustrating (12), not an adopted protocol.
The raw cap needs its own prospective choice and availability analysis.
Neither (12) nor this example authorizes retuning or executing (9).

## 5. Selection and abstention at the observed categories

The structure of [the diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s selection proof survives, but its parameters
are now \(\widehat\nu,\widehat q\), not \(\nu,q\).
This applies to both clean and leaky fixed channels.

Let \(\widehat D_n=\mathbf1_{\{Y_n\in\{0,4\}\}}\) and
\(A=\{\sum_{n=1}^N\widehat D_n\ge m\}\), for fixed \(N\ge m\ge1\).
For any indicator pattern with \(j\) reported diagnostics, its joint
probability with relative diagnostic labels \(z_s\in\{0,1\}\) is
\[
 \widehat\nu^j(1-\widehat\nu)^{N-j}
       \prod_{\text{diagnostic }s}
            \widehat q^{z_s}(1-\widehat q)^{1-z_s}.        \tag{13}
\]
Condition on any positive-probability pattern and cancel the first
factor. Every pattern with \(j\ge m\) gives the same product law for
its first \(m\) labels. Hence
\[
                S_m\mid A\sim\operatorname{Bin}(m,\widehat q).
                                                               \tag{14}
\]
The usual degenerate-category cases are interpreted by their
probabilities, not by dividing by a zero-probability pattern.
Here \(\widehat\nu>0\), so \(P(A)>0\).

Unequal true-category misses do not invalidate (13) under the declared
memoryless model; they change \(\widehat q\). Using the original \(q\)
after such selection would be wrong. Collection must use observed
diagnostic membership only, the first fixed \(m\) labels, and the fixed
raw cap. Label-based early stopping, correlated errors, adaptive
classification or discarding unfavorable outcomes is not covered.

For any design with certified common conditional wrong-label bounds
\(\alpha_{\rm I},\alpha_{\rm II}\), define
\[
 b_N(v)=P(\operatorname{Bin}(N,v)<m),\qquad a_N(v)=1-b_N(v).
\]
Then ABSTAIN has probability \(b_N(\widehat\nu)\); wrong decisions
unconditionally are bounded by \(\alpha a_N(\widehat\nu)\).
Under the alternative,
\[
 P(\mathrm{PERTURBED})\ge(1-\alpha_{\rm II})a_N(\widehat\nu),\qquad
 P(\hbox{not PERTURBED})\le
 b_N(\widehat\nu)+\alpha_{\rm II}a_N(\widehat\nu).           \tag{15}
\]
The latter includes ABSTAIN; it is not merely \(\alpha_{\rm II}\).
These error probabilities are not posterior probabilities of a label.
No raw-power guarantee follows just from the conditional gap in (8).

For fixed iid draws the expected uncapped raw cost is
\(m/\widehat\nu\), and
\[
 E\min(T_m,N)
   =\sum_{n=0}^{N-1}P(\operatorname{Bin}(n,\widehat\nu)<m)
   \le\min\{N,m/\widehat\nu\}.                              \tag{16}
\]
Counter updates do not price preparation, classification or channel
calibration. In the clean case \(\widehat\nu\to0\) when native
\(\nu\to0\), so the original rarity/abstention problem remains.

## 6. Fixed positive leakage destroys the uniform conditional gap

Now allow \(t=e+f>0\), keeping the same fixed matrix and positive
\(s_0,s_4\). Write
\[
 z=f/t\in[0,1].
\]
The complete observed probabilities give
\[
 \widehat\nu=\nu s(q)+(1-\nu)t,\qquad
 \widehat q
 =\frac{\nu s(q)\phi_M(q)+(1-\nu)t z}
        {\nu s(q)+(1-\nu)t}.                              \tag{17}
\]
Thus the observed conditional label is a mixture of detected true
diagnostics and false diagnostics. It depends on availability as well
as the true conditional label. The clean determinant does not, by
itself, control its orientation across laws with different availability.

[The prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md) §7 permits fixing an eligible perturbable prefix and an admitted
\(\lambda\), then sending the positive common scale \(\rho\) to zero.
Every proper shape has mass \(O(\rho)\); the full-birth mass tends to one.
For both baseline and its admitted perturbation, therefore,
\[
 \nu\longrightarrow0,\qquad
 (p_0,p_4,p_O)\longrightarrow(0,0,1).
\]
These are limits of positive-scale laws, conditional on the same
occurrence/construction premises; scale zero is not a member.
The already justified limit, not a new coefficient calculation, gives
\[
 \widehat p\longrightarrow(e,f,1-t),\qquad
 \widehat\nu\longrightarrow t,\qquad
 \widehat q\longrightarrow z                              \tag{18}
\]
under both hypotheses. For example the weight on \(\phi_M(q)\) in
(17) is at most \(\nu/((1-\nu)t)\) for \(\nu<1\), which tends to zero
regardless of the bounded conditional label.

**Rare-event obstruction.** No uniform positive same-oriented
conditional-label gap survives over the full admitted arbitrary-scale
family for any fixed \(t>0\). If such a gap \(g>0\) held for every
baseline/perturbation pair, applying it along the two sequences in (18)
would give \(0\ge g\), a contradiction.

There is also a narrow fixed-rule consequence. For fixed finite \(m,k\)
and the two-label decision rule on collection, let
\(H(q)=P(\operatorname{Bin}(m,q)\ge k)\), a continuous polynomial.
Along the two rare-event sequences, (14) implies
\[
 e_B\longrightarrow H(z),\qquad
 e_Q\longrightarrow1-H(z),\qquad e_B+e_Q\longrightarrow1.  \tag{19}
\]
Thus this fixed-count rule cannot keep both conditional errors uniformly
below \(1/20\), or any tolerances whose sum is below one, over all scales.
This is a statement about that rule, not all statistical procedures.

Observed collection can remain frequent while the native signal
vanishes: \(\widehat\nu\to t>0\), and indeed
\(\widehat\nu\ge\min\{s_0,s_4,t\}>0\) for this fixed channel.
Reaching the event-count target is therefore not evidence that the
reported diagnostics predominantly came from true \(K_0/K_4\) events.
In the limit, collection probability is \(a_N(t)\), not necessarily
close to one but not forced to zero by native rarity.

Neither (18) nor (19) proves exact overlap at every positive scale,
impossibility of every statistic, or invalidity of a known-channel
correction. For example, identity diagnostic rows and OTHER row
\((e,f,1-t)\) with \(0<t<1\) give an invertible matrix of determinant
\(1-t\), despite sharing the limit (18).
Exact positive-scale law distinctions can survive such a matrix.
No inverse problem, correction estimator or error-rate analysis for it
is developed here.

## 7. One bounded sufficient premise for a restricted leaky class

Suppose the diagnostic subchannel has \(\Delta_M>0\), with clean
endpoints \(U<V\) and gap \(G\).
For each tested complete law define the false-to-true detected ratio
and contamination fraction
\[
 h(p)=\frac{(1-\nu)t}{\nu s(q)},\qquad
 w(p)=\frac{h(p)}{1+h(p)}.
\]
Assume, as an **additional uniform premise** on the intended restricted
law class, that
\[
 h(p)\le h_{\max}<\infty,\qquad
 \varepsilon=\frac{h_{\max}}{1+h_{\max}},\qquad
                       2\varepsilon<G.                  \tag{20}
\]
Equation (17) becomes
\(\widehat q=(1-w)\phi_M(q)+wz\).
Since both labels are probabilities,
\[
 |\widehat q-\phi_M(q)|=w|z-\phi_M(q)|\le\varepsilon.
\]
Consequently
\[
 \widehat q_B\le U+\varepsilon
       <V-\varepsilon<\widehat q_Q,\qquad
                 G_{\rm eff}=G-2\varepsilon>0.            \tag{21}
\]
One may use these conservative endpoints in (10) or in the hypothetical
midpoint/count prescription (12), replacing \(G\) by \(G_{\rm eff}\).
If needed the endpoints can be clipped to \([0,1]\); (20) already places
\(U+\varepsilon<V-\varepsilon\) strictly inside that interval.
This is sufficient, not necessary or optimized for the known value of
\(z\). It does not reopen a broad channel uncertainty-set problem.

A concrete way to justify a bound of the form (20), if independently
established, is a true availability floor \(\nu\ge\nu_{\min}>0\).
With \(s_{\min}=\min(s_0,s_4)>0\), it gives
\[
 h_{\max}=\frac{(1-\nu_{\min})t}{\nu_{\min}s_{\min}},\qquad
 \widehat\nu\ge\nu_{\min}s_{\min},\qquad
 \frac{2h_{\max}}{1+h_{\max}}<G                            \tag{22}
\]
as one explicit sufficient inequality for separation.
A positive floor alone does not imply the last inequality: leakage
must also be small enough relative to genuine detected availability.
Conversely, a large observed event rate alone does not prove a true
availability floor.

For a certified observed floor \(\widehat\nu\ge v_{\min}>0\), a declared
cap with \(Nv_{\min}>m-1\) satisfies the [diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md) bound
\[
 b_N(\widehat\nu)\le
 \exp\!\left[-2N\left(v_{\min}-\frac{m-1}{N}\right)^2\right].
                                                               \tag{23}
\]
Making this at most a declared \(\zeta\), together with a certified
conditional decision design, gives power at least
\((1-\alpha_{\rm II})(1-\zeta)\).
The probability guarantee requires both valid label endpoints and
collection control; neither can replace the other.

For fixed positive \(t\), the extra bound (20) excludes the unrestricted
\(\rho\to0\) regime, because \(h(p)\to\infty\).
It is not an inherited fact about the full family.
[The baseline-scale theorem](BASELINE_SCALE_THEOREM.md)'s optional half-scale construction does not supply a numerical
availability floor for that arbitrary-scale class or calibrate a
channel. No native \(\nu_{\min}\), \(M\), false-positive rate, cost,
calibration dataset or actual \(\Xi\) is supplied here.
If calibration estimates rather than exact premises are used later,
their justified uncertainty/failure probability must be budgeted as
well; plugging an estimate into (20) is not a certificate.
No such estimation is performed or authorized.

## 8. A fixed run-latent law or channel is a separate model

If a latent index \(Z\) is drawn once per run and conditional on \(Z=z\)
the true draws and channel satisfy §2 with \((p_z,M_z)\), then observed
draws are conditionally iid with law \(p_zM_z\).
They are generally dependent unconditionally.
Their raw diagnostic count is not generally binomial at
\(E\widehat\nu_Z\), nor is the selected count binomial at a marginal
conditional-label mean.

Conditional on \(z\), all the preceding formulas apply. After successful
collection the index distribution is reweighted by
\(a_N(\widehat\nu_z)\). Thus the selected count is a mixture of
\(\operatorname{Bin}(m,\widehat q_z)\) under those weights.

A single fixed decision design retains conditional error control if
**every** included component has the same hypothesis label and satisfies
common endpoint bounds that certify that design. Then
\[
 P(\mathrm{wrong},A)\le\alpha E[a_N(\widehat\nu_Z)]
                         =\alpha P(A),
 \qquad P(\mathrm{wrong}\mid A)\le\alpha.
\]
Abstention is \(E[b_N(\widehat\nu_Z)]\), not
\(b_N(E\widehat\nu_Z)\). An almost-sure observed availability floor gives
the common cap bound (23). Expected uncapped cost is
\(E[m/\widehat\nu_Z]\), possibly infinite.

For variable channels, positivity of each \(\Delta_{M_z}\) is
insufficient for common endpoint separation. Any claim using (20)–(23)
must likewise hold uniformly over the admitted components, not merely
at averaged channel entries or average native availability.
No optimization over channel families is undertaken.

If instead the latent component is redrawn iid per raw observation,
the reported draws can be iid from the fixed marginal
\(E[p_ZM_Z]\), given the corresponding independent preparation/channel
model. This is generally not \((Ep_Z)(EM_Z)\).
Coordinate inequalities uniform across components integrate, whereas
component conditional ratios do not average with the original mixing
weights. These are distinct observation models, not interchangeable
consequences of a mixture definition.

## 9. Observation assumptions now isolated

The mathematical yield is a channel-transfer theorem, a rare-event
obstruction and one bounded sufficient contamination condition.
Operational admission would still have to establish:

1. **True source/class validity.** The complete parent/shape definitions,
   canonical-prefix and common-calibration conditions, admissible
   scales, and each perturbed member's own construction and conditional
   \(\Xi>1\). Successful classification cannot establish those premises.
2. **Repeated preparation.** A justified fixed-law iid experiment, or
   the separately stated conditional-iid latent model. A changing-parent
   trajectory is not substituted for repeated draws.
3. **Classifier/channel calibration.** The intended aggregate matrix,
   row definitions, category-only action, cross-draw independence and
   applicability across the tested law class; uncertainty and drift
   must be accounted for. No exact three-category channel is derived
   merely from a generic noisy-order classifier.
4. **Availability and false-positive control.** Evidence for any native
   or observed floor and, with leakage, a separation-preserving
   contamination bound. Frequent reported events alone are insufficient.
5. **Error, abstention and cost accounting.** Predeclared counts, cap,
   threshold, conditional tolerances, calibration-failure budget and
   reporting of every OTHER draw, failure and ABSTAIN; raw preparation
   and calibration costs remain distinct from event counts.
6. **Independent held-out evaluation.** Separately authorized evaluation
   and immutable reporting, without choosing channels, diagnostics or
   thresholds on held-out outcomes.

A **conditional native prediction theorem** relates probabilities of
specified admissible mathematical laws under an added observation model.
A **diagnostic benchmark** would measure a specified implemented system
under its own controlled data/label conditions; none is executed here.
A **physical detector** additionally requires a justified correspondence
from accessible physical records to these true classes, sources and
channel assumptions. Neither of the first two supplies the third.
Application success cannot validate DET or its ontology.

[The diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md)'s original design, WIDTH_DIAGNOSTIC and
APPROXIMATE_WIDTH_DIAGNOSTIC remain unchanged. The width protocols were
not read, retuned or executed. RET remains paused; historical failures
are not repaired by this calculation.

## Public premises and evidence scope

The [diagnostic-event theorem](P4_DIAGNOSTIC_EVENT_TEST.md) supplies the
prospective iid repeated-draw model, conservative conditional-label
envelopes, selection argument, fixed original design, abstention accounting
and separate fixed run-latent model. The
[prefix-family theorem](P4_PREFIX_FAMILY_SEPARATOR.md) supplies the admitted
actual-law classes, held calibration, measurable within-label mixtures and
the common-scale rare-event limit. Its qualifying prefix family may be a
singleton; mathematical envelope endpoints do not establish additional
native laws or endpoint attainability. The
[baseline-scale theorem](BASELINE_SCALE_THEOREM.md) distinguishes the admitted
common-scale construction from its optional half-scale prescription. That
prescription does not supply numerical availability for the arbitrary-scale
class or calibrate an observation channel.

For construction of the source manuscript, the retained statement is:

All mathematics and illustrative channel arithmetic are hand-derived.

This statement describes source-manuscript construction, not later
independent review or its separate checks. Review and check records are
retained privately. Public preparation alone supplies no independent
mathematical acceptance, operational admission or historical-custody repair.

The fixed common category-only memoryless channel and repeated preparation
are additional assumptions. Clean-channel positive orientation does not
automatically certify the original numerical design. Fixed positive OTHER
leakage destroys the uniform conditional-label gap in the admitted rare-event
limit; this does not prove exact overlap at positive scale or failure of
every statistic or known-channel correction. The restricted contamination
bound is an additional sufficient premise, not an inherited availability
fact. The original thresholds, operational ABSTAIN and OTHER accounting,
frozen diagnostic protocols and RET pause remain unchanged. No channel
calibration, implemented benchmark, physical detector or validation of DET
is supplied.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. Public dependency links identify mathematical
premises; they do not supply private custody records or original certificate
reproduction. This edition is conditional mathematical exposition, not an
executable installation or an independently replayable custody package.
See the [publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).

## Every decision rule under a fixed raw budget

The [fixed-budget testing theorem](P4_FIXED_BUDGET_TESTING_LIMIT.md) extends
the conditional rare-event limitation to every admitted randomized decision
rule and stopping procedure with a fixed finite raw cap, including the
identity channel and known invertible channels. Exact positive-scale laws
can remain distinct. With ABSTAIN allowed, conditional error tolerances whose
sum is below one force decision coverage to vanish along the admitted limit.
The result assumes an actually eligible source pair and the stated iid model;
it supplies no physical falsification or validation.
