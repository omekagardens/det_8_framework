# QR-05Z results: fixed attenuation helps selected mismatches

7 September 2026. Exact finite classical forecast-policy comparison.
Completed: both implementations, independent runner, normal/optimized tests,
exact read-only replays and raw-history audit pass.

## Outcome

The two implementations and independent runner agree on every complete Y
baseline and all three fixed blends for the six experiments. The half blend
improves selected mismatches but is not uniformly better than coarse-only
prediction, and it sacrifices accuracy when the detailed model is correct.

The rule is h_a=(1-a)g+a f, where f is the completed Y forecast, g the same
coarse forecast, and a is fixed at 0, 1/2 or 1. Each rule is evaluated under all
four actual and four assumed noise settings. Actual noise and future outcomes
never choose a weight; all results, including negative gains, are retained.

At actual replacement 1/2 with assumed replacement 0, and at actual 3/4 with
assumed 1/2, the half blend beats BOTH Y and coarse-only in all 10 informative
histories across the cases. The remaining 472 histories are unchanged.
Y alone had 2 histories better than coarse, 4 worse and 476 equal at each of
those settings. These are inventory counts; each case's expected risk keeps
its own original history likelihoods. The six cases are not pooled.

For the mixture cases, the case-average gains over coarse reverse sign:

| Case and actual/assumed setting | Y gain (a=1) | Half-blend gain (a=1/2) |
| --- | ---: | ---: |
| mixture_balanced, 1/2 versus 0 | -377/191102976 | 859/764411904 |
| mixture_biased, 1/2 versus 0 | -637952/94143178827 | 369152/94143178827 |
| mixture_balanced, 3/4 versus 1/2 | -463/7166361600 | 9107/28665446400 |
| mixture_biased, 3/4 versus 1/2 | -4566016/21182215236075 | 23507456/21182215236075 |

Positive gain means lower Brier risk than coarse-only. These are small absolute
improvements in supplied hypothetical experiments, not measured application
performance or a large reduction in total error.

The midpoint is Bayes-correct at these two settings in both right cases,
but not in the mixture cases. In mixture_balanced its regrets are respectively
809/3822059520 and 193/28665446400. Thus forecast blending is not generally
equivalent to substituting a halfway noise parameter or recovering the true
conditional law.

## Where the half blend still fails

At actual 3/4, assumed 0, the midpoint improves on Y in all 10 informative
histories, yet remains worse than coarse in 4, better in 2 and equal in 476.
Its case-average gain is -377/509607936 for mixture_balanced and
-79744/31381059609 for mixture_biased; both right cases have zero gain.
Improvement over a harmful forecast is not sufficient to beat the baseline.

At actual full replacement and any assumed level below 1, all 10 informative
histories still lose to coarse-only. Their midpoint excess risk is exactly
one quarter of Y's excess risk, as predicted by the quadratic identity.
The penalty is reduced, not eliminated.

When actual and assumed settings match below full replacement, the midpoint
is worse than the Bayes-correct Y forecast in the 10 informative histories.
It retains three quarters of Y's gain over coarse, losing the remaining
quarter to shrinkage. Assuming full replacement makes all three policies
identical; both left cases are identical throughout.

For right_balanced let G=49/5971968, W's clean added NMT gain.
The table gives the HALF-BLEND gain over coarse divided by G:

| Actual t \\ Assumed s | 0 | 1/2 | 3/4 | 1 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 3/4 | 7/16 | 15/64 | 0 |
| 1/2 | 1/4 | 3/16 | 7/64 | 0 |
| 3/4 | 0 | 1/16 | 3/64 | 0 |
| 1 | -1/4 | -1/16 | -1/64 | 0 |

The same normalized table holds for right_biased with G=888832/31381059609.
This does not establish a universal noise threshold or a percentage reduction
in total prediction error.

## What is verified mathematically

For actual future law p, coarse forecast g and completed Y forecast f, let
D=||f-g||². Exact Brier scoring gives

    L(h_a;p) = (1-a)L(g;p)+aL(f;p)-a(1-a)D,
    gain_coarse(a) = a gain_coarse(1)+a(1-a)D,
    gain_base(a) = L(f;p)-L(h_a;p)
                 = gain_coarse(a)-gain_coarse(1).

The same identities hold after weighting by original actual report masses
and history likelihoods. D is in [0,2], as are risk and regret; gains are signed
in [-2,2]. No report or history renormalization is introduced.

The midpoint's advantage over the AVERAGE endpoint risk is the predetermined
D/4 convexity term. It does not guarantee an advantage over either endpoint.
An independent generic control has equal endpoint risks 1, midpoint risk 1/2
and D=2, demonstrating why equal scalar risks do not imply equal laws.

When f=p, mixed regret is (1-a)²D. For W full replacement p=g, gain is -a²D.
These prospective controls explain the correct-model cost and full-noise
penalty. They are consequences of the supplied laws, not robustness discoveries
or empirical estimates.

Every blend retains its complete positive sparse forecast. Exactly-zero
endpoint atoms are omitted; positive midpoint atoms cannot be pruned.
The full Y baseline remains unchanged, including every nested X null score,
support flag, fallback contribution, forecast and witness. All 96 fallback-used
pair cells satisfy f=g, so all their blends are unchanged. Generic countertests
retain positive fallback regret: a wrong fallback is not repaired by mixing
it with itself.

The mixtures are classical forecast decision rules, not actual observation
channels, coherent amplitude sums or new quantum dynamics. Their actual-weight
future marginal need not equal the true future marginal. Generic normalized
input does not authenticate W replacement, a true N-conditional fallback,
apparatus origin or calibration.

## Evidence and bounded work

| Object | Count |
| --- | ---: |
| Cases / positive histories | 6 / 482 |
| Actual/assumed pairs per history | 16 |
| Fixed weights / history-pair-weight results | 3 / 23,136 |
| Retained base pair cells / scored blend cells | 8,256 / 24,768 |
| Positive mixed-forecast atoms | 111,536 |
| Carried Y scoring support visits | 148,488 |
| Mixture construction / endpoint-distance visits | 222,936 / 74,312 |
| Blend scoring support visits | 222,800 |
| Total declared work terms | 668,536 |
| Public analyze calls / malformed wrappers rejected by runner | 12 / 16 |

Each blend is constructed from both endpoint supports and rescored, even at
a=0 or 1 and even when fallback makes the endpoints identical. Distance is
computed once per pair cell. All structural/work caps are planned before
either Y or Z forecast scoring; executed counts must agree. These counters
are bounded arithmetic work metrics, not runtime or application throughput.

## Verification and immutable evidence

The seven source/protocol files were frozen after the successful second
external preflight. All final verification runs passed on their first attempt.

| Final check | Result | Time |
| --- | --- | ---: |
| Normal Python test suite | 189 passed | 298.24s |
| Optimized Python test suite | 189 passed; expected assertion warning | 298.09s |
| Exclusive final capture | Created once | 94.610s |
| Normal exact read-only replay | Passed | 98.281s |
| Optimized exact read-only replay | Passed | 98.422s |
| Independent JSON-only audit | 34,970,735 checks passed | 36.653s |
| Ruff lint / format checks | Passed / unchanged | — |

Times are rounded local run measurements, not reproducible performance claims.
The exact numerical suite matches the first comparison and both preflights.

| Canonical object | Bytes | SHA256 |
| --- | ---: | --- |
| Final results.json | 31,075,315 | `7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc` |
| Numerical suite | 31,069,562 | `1d790ab0c8c467b4fe38b989093b952aeafcff758e946f4f5d3242ca0e73c909` |
| Complete analysis list | 30,313,670 | `d46c8e1bb136b38a948aeebb3971796a7cfe4691d8a80a67ecd3357c9f898020` |

The outer envelope includes runtime metadata; it is deliberately distinguished
from the exact numerical suite. Canonical hashes use sorted ASCII JSON with
compact separators and one trailing newline.

Optimized pytest emits its expected assertion warning. Each dedicated
normal/optimized guard subprocess performs 314 explicit rejections, including
69 pre-serialization cycle/depth/expanded-DAG checks across the two cores and
runner. Those guard checks do not rely on Python assertions. There are 108
malformed public-input fixtures (94 inherited inner experiments and 14 outer
wrappers), 10 nonvacuous complete-output corruptions and pinned-producer
corruption controls.

The tests check full Y-baseline preservation, all three complete sparse laws,
signed scores, original weights, exact endpoints, wrong generic fallbacks,
distinct laws with equal scalar risks, actual-index-independent forecasts,
live caps before any Y/Z forecast scoring, honest construction/distance/score
counts, detached ownership and depth 128/129 scalar/empty/shared-subtree
boundaries.

A specific new bit-boundary control has valid Y input and retained Y scores,
but its midpoint law contains a 4097-bit denominator. Z correctly rejects that
new retained value. Separate controls accept oversized intermediates that
cancel into valid 4096-bit retained values; the guard is not an indiscriminate
restriction on every arithmetic intermediate.

The JSON-only auditor reconstructs 4,447 raw states, 168,388 induced-subset
relations, 9,201,100 subset-Mobius subtractions, 8,894 raw K3 member rows and
32,768 categorical vertex-lifetime assignments. It authenticates all 482
current histories and 2,064 noisy cells, including both complete posterior
and future-law equality with N on 96 unsupported pair cells.

Across X/Y/Z scoring the audit evaluates 1,539,096 literal
actual-outcome/forecast-coordinate squared-error terms and 306,862 scalar
disagreement summands, not every possible replica pair. Its Z-only work
includes 24,768 scored blends, 37,224 endpoint-distance coordinates and
111,672 mixture coordinates. These counts are separate from the cores'
linear source-support traversal metric.

It then independently rebuilds every X/Y score, original null, complete
baseline and all Z forecasts/scores. Full native/canonical X/Y/Z reporting,
counts, witnesses, producer controls and envelope identities agree. It imports
no executor, runner or test; source contents are read only as bytes for identity.
The inherited polynomial digest is pinned producer identity, not a fresh
polynomial derivation. Prior public APIs, source aliases and broader
operator/minimality certificates are not replayed. Historical API/runtime
fields are validated metadata, not reproduced performance measurements.

The protocol was recorded before fixed Z case outcomes. Before the first case
comparison, the carried runner's depth guard was corrected to count scalar
leaves at their actual depth, use zero edge-height for empty containers, and
check memoized subtree depth without an off-by-one allowance. This strengthens
native validation under the existing contract; no scientific setting, forecast
rule, output schema or acceptance criterion changed. The two cores required
no mathematical corrections during initial hand checks.

After the first case comparison and successful hand tests, before final freeze,
the midpoint-overflow test was strengthened to explicitly require each locally
carried Y analyzer to accept the underlying experiment. This ensures the
rejection is genuinely due to the new Z midpoint, not a pre-existing Y
failure. Its targeted rerun passed. Initial Ruff formatting did not change
mathematics. No outcome, threshold or weight was tuned.

The first complete comparison passed in 80.73590237499957s with four
protocol/implementation files and 30 prior artifacts unchanged.

The first external create-only preflight audit failed at exact reporting
closure: the auditor constructed `equal_than_base/coarse_beliefs` and
`first_equal_than_base/coarse` instead of the protocol's `equal_to_*`
names. Both implementations, runner and independent test oracle already
agreed. All first-case numerical fields matched; the mismatch was confined
to four auditor field names. A one-expression auditor-only fix corrected
the join. All six complete analyses and producer controls then matched the
preserved capture (5,317,161 checks). A new generic complete-wire auditor
regression verifies the keys alongside midpoint and wrong-fallback controls.

The first preflight remains unchanged outside the checkout: 31,075,317 bytes,
SHA256 `0b3d29cd383ce0ea73b7815124137fa7c4c044065129b5869bb484aae837b625`.
A second exclusive preflight with the corrected source ledger passed the
full 34,970,735-check audit in 35.43325216700032s before final freeze.
Neither temporary capture was overwritten or substituted for the final
artifact. Both share the same exact numerical suite as the first comparison.
The correction changed no forecast, score, schema or acceptance criterion.

Seven frozen Z source/protocol files and 30 producer artifacts remain
unchanged through final tests, capture, replays and audit. Artifact bytes are
unchanged after exclusive creation. The audit additionally checks seven Y,
seven X and six W producer source hashes before/after. Final runs use isolated
Python and fresh explicit external bytecode caches. RESULTS.md and the roadmap
are outside the frozen ledger; no frozen source or artifact is edited.

## Application value and boundaries

This provides a transparent, bounded way to compare partial reliance on a
detailed model against its complete and coarse alternatives. It preserves
coverage evidence, full forecast laws, signed losses and costs of conservatism.
It does not select a deployable policy: useful gains depend on the actual
noise mechanism, which is unknown to the rule and hypothetical in these cases.

No calibration data, empirical robustness claim, RET integration, sensor
recommendation, Lean proof, ontology, physical law, metric reconstruction or
gravity correspondence is added. No observation is dismissed as noise or a
setup artifact.

## Proposed next gate: QR-05AA, declared uncertainty-bound decisions

Use declared upper bounds u from the four existing noise levels, with
finite uncertainty sets S_u={existing t<=u}. For each case, assumed model
and bound, compare the same three weights using worst-case SIGNED excess
risk over coarse. Choose one weight for the whole experiment, shared across
all histories and reports. Actual noise is fixed but unknown, not selected
separately for each history or report.

Retain every candidate/world risk, worst-case value and all exact minimizing
weights. Do not clip negative excess to zero or select a tie retrospectively.
The certificate would concern only the declared three-rule menu.

Prospective checks should verify that actual-law expected risk of a fixed
report-dependent forecast is affine in replacement level, even though its
actual conditional laws need not be affine. For this W family, the planned
monotonicity control would reduce worst-case excess to the declared upper
endpoint. Full replacement remains a coarse-only boundary except where
forecasts coincide.

Bounds are assumptions, not inferred calibration. No cross-case pooling,
report-wise selector, outside-family robustness or deployable policy is
implied. Record the full AA protocol before computing any policy values.
No AA outcomes have been computed.
