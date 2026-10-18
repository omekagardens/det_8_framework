# QR-05X results: forecasting under the wrong noise model

7 September 2026. Exact finite classical forecast-scoring gate.

## Outcome

Across all six fixed experiments, the two implementations and the runner's
independent scorer agree on the complete 4x4 actual/assumed-noise comparison.

A clean assumed model fails to define a forecast on some reports produced by
every positive actual-noise level. This affects 22 of the 482 histories:
3 in each left case and 4 in each right/mixture case. Each affected
actual/assumed pair retains 32 unsupported report cells across the six cases.
Those are report cells, not 32 new raw states or physical events.

Full case forecast risk and regret are therefore null for all six cases whenever
actual noise is positive but assumed noise is zero. A small missing
probability is still missing; supported scores cannot be silently reported
as an unconditional score.

| Case | Incomplete histories | Unsupported actual mass at t=1/2, assumed s=0 |
| --- | ---: | ---: |
| left_balanced | 3 | 31/46656 |
| left_biased | 3 | 248/531441 |
| right_balanced | 4 | 23/46656 |
| right_biased | 4 | 220/531441 |
| mixture_balanced | 4 | 1/3888 |
| mixture_biased | 4 | 38/177147 |

At actual level 3/4 these masses are 3/2 times the table; at level 1 they
are twice the table. At level 1/2 they are about 0.021–0.066% of each
case's own probability mass. The six experiments are not pooled.

The left cases illustrate why two questions must stay separate: their
supported forecast regret is zero even under mismatch, but their clean
assumed models still have incomplete support under positive actual noise.
Zero error where a forecast exists does not establish a complete forecaster.

All positive assumed-noise levels have full coverage on these W cases.
Every diagonal comparison has zero regret and exactly reproduces W's risk.
These are preregistered consequences/controls of the fixed family, not
empirical calibration or new robustness evidence.

## Quantitative mismatch cost

Risk is evaluated under the ACTUAL report and future laws. The assumed
model supplies only the forecast; it does not supply the scoring weights.

For right_balanced let G=49/5971968, the clean added NMT gain from W.
The following entries are full regret divided by G:

| Actual t \\ Assumed s | 0 | 1/2 | 3/4 | 1 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0 | 1/4 | 9/16 | 1 |
| 1/2 | undefined | 0 | 1/16 | 1/4 |
| 3/4 | undefined | 1/16 | 0 | 1/16 |
| 1 | undefined | 1/4 | 1/16 | 0 |

This scaling table concerns one case and its already-small added gain,
not a percentage reduction in total prediction error. It is not a general
symmetry theorem for misspecification.

For mixture_balanced, actual 1/2 with assumed 3/4 has full regret
193/537477120; reversing the levels gives 697/1791590400. The asymmetry is
real: changing which experiment is actual changes both conditional laws
and their scoring weights.

Assuming full replacement supplies the N-conditional forecast. Its actual-law
expected risk equals W's N risk for every actual noise level. Conversely,
when actual replacement is full, assuming a smaller positive level produces
strict excess risk in the four informative cases: the forecast attributes
information to a label that now carries none beyond N. No cost-optimal or
uniformly best assumed setting is selected.

Every off-diagonal pair has positive SUPPORTED regret in the same 10
histories that had useful NMT information in W. In the three positive-actual/
assumed-clean pairs, only 8 of these histories have complete forecasts;
the other 2 retain a supported contribution, not a full regret value.
Missing forecasts are not counted as zero-error histories.

## What is verified mathematically

For actual future law p and a defined forecast f, the unscaled Brier risk is

    Brier(f;p) = 1 - 2 sum_q p(q)f(q) + sum_q f(q)^2
               = R(p) + ||p-f||^2,
    R(p) = 1 - sum_q p(q)^2.

Both complete sparse supports are used. Missing future atoms within an
existing forecast mean exact zero; an entirely missing report is different.
Conditional Bayes risk is at most 1. Misspecified forecast risk and regret
can reach 2, as verified by opposed deterministic hand controls.

For actual report mass w(z), coverage is the sum of w over reports with a
defined assumed forecast. Supported Bayes risk, forecast risk and regret
are sums with ORIGINAL actual weights, without division by coverage.
Supported forecast risk equals supported Bayes risk plus supported regret.
The full Bayes risk is always known. Full forecast risk and full regret are
retained only when coverage is exactly one.

History aggregation uses the original positive likelihoods. A case with
one incomplete positive-weight history remains incomplete; neither report
nor history weights are renormalized. No replacement-coin observation,
fallback policy, changed K3, changed Q3 or fitted parameter is introduced.

## Scoring interface and evidence boundary

The generic API takes four exact conditional report/future experiments
per history. It checks native reduced fractions, sorted positive laws,
normalization and shared future marginals, then computes all 16 pairs.
It does not receive raw orders, history paths, artifact filenames or
current class-local transition rules.

Normalization alone does NOT certify N-preserving replacement,
non-disturbance, physical provenance or calibration. Those claims are
specific to the pinned W experiment and its independent raw audit.
This deliberately narrower interface reuses W's established laws; it is
not a claim to rederive the thinning calculus in another implementation.

The runner authenticates W plus its 27 immutable prior artifacts, projects
the complete input laws and compares all outputs with an independent
coordinate-wise expected squared-error calculation. The primary uses direct
quadratic scoring; the reference uses expected loss at each actual outcome.
The separate JSON-only audit authenticates the raw-history connection.

| Checked/retained object | Count |
| --- | ---: |
| Cases / positive histories | 6 / 482 |
| Actual/assumed pairs per history | 16 |
| History-pair results | 7,712 |
| Input report cells / future-law atoms | 2,064 / 9,272 |
| Retained pair cells | 8,256 |
| Supported / unsupported pair cells | 8,160 / 96 |
| Declared scoring support visits | 72,076 |
| Public analyze calls / malformed calls rejected by runner | 12 / 14 |

The 96 unsupported cells count 32 cells at each of three distinct actual
noise levels; they are not pooled probabilities or independent repetitions.
Scoring visits count actual plus assumed support lengths for each supported
comparison. They are a bounded work metric, not wall-clock performance.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 8,842,933 bytes,
SHA256 `1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4`.
The canonical suite is 8,837,477 bytes,
SHA256 `04de08cdc02c6a5a6f1739482b6c2a9d795806cf7667dfa109a5b1a086844247`.
The canonical JSON list of six complete analyses is 8,198,676 bytes,
SHA256 `ce50e95bdd7b82807210a333e6accf411d0186b34f0307fd84741cdceb3d110d`.

| Check | Outcome |
| --- | --- |
| Full normal tests | 142 passed in 90.17s |
| Full optimized tests | 142 passed in 90.09s |
| Exclusive final capture | 17.56920820799951s |
| Fresh normal exact read-only replay | 18.264874542000143s, exact |
| Fresh optimized exact read-only replay | 18.71511908299999s, exact |
| Final JSON-only raw-history audit | 8,502,326 checks in 12.825305000000299s, passed |

Optimized pytest emits its expected assertion warning. Each dedicated
normal/optimized guard subprocess performs 186 explicit rejections, including
39 pre-serialization cycle/depth/expanded-DAG checks across cores and runner.
Its checks do not rely on Python assertions. Work caps reject before score
loops; valid shared containers and output ownership are tested. There are
65 malformed public-input fixtures and 18 complete-output corruptions.

The independent JSON-only audit checks 4,447 supplied raw states and rebuilds
168,388 induced-subset relations, using 9,201,100 subset-Mobius subtractions to authenticate
features/H fibers. It checks 8,894 raw K3 member rows and uses 32,768
categorical vertex-lifetime assignments to recover current histories and
future joints. All 2,064 W noisy cells, their complete current/future laws
and the complete X projection agree.

X risks are independently rebuilt through 245,820 explicit
actual-outcome/forecast-coordinate squared-error terms, distinct from the
cores' linear support-visit metric. Disagreement controls use 84,334 scalar
summands; that number is not an enumeration of all replica outcome pairs.
The complete X native/canonical suite, counts, witnesses, controls and
envelope are checked—not only scalar totals.

The audit imports no executor, runner or test; their source contents are
read only as bytes for identity checks. It also authenticates W's six source
hashes. Its scope is the raw law/projection/scoring bridge: prior public
APIs, broader operator/minimality certificates and source aliases are not
replayed. The inherited fine-polynomial digest is pinned producer identity,
not a new polynomial derivation. Historical public-call and runtime fields
are checked as metadata, not replayed API/performance measurements.

The protocol was fixed before case outcomes. Before the first case run,
native resource-accounting conventions were clarified and a reference
implementation guard was corrected: it had incorrectly limited every
intermediate rational to 4,096 bits instead of inputs and retained results.
Intermediate denominators can cancel into valid retained values. Regression
controls now accept those cases while rejecting genuinely oversized results.
Per-route input-immutability checks were also separated before that run.

After the first successful case comparison but before the full suites, one
test's producer-corruption value was changed from a potentially unchanged
[1,1] to an actually invalid [0,1], with explicit non-no-op checks. No
scientific formula, noise setting, expected outcome or acceptance threshold
changed. Initial formatting/lint cleanup did not change the mathematics.

A temporary create-only capture outside the checkout exercised the audit
before final source freeze: its 8,502,326 checks passed in 12.498789041999771s.
This was a preflight, not the published artifact, and it was not overwritten.
Both final full test suites passed on their first runs.

Seven frozen source/protocol files and all 28 producer artifacts remained
unchanged through the final tests, capture, replays and audit. Final artifact
bytes remained unchanged after creation; the audit additionally checked six
W producer source hashes before/after. All final runs use isolated Python
and explicit fresh external bytecode caches. RESULTS.md and the roadmap
remain outside the frozen ledger. No frozen source or artifact was edited.

## Application value and limits

This adds a useful safeguard for forecast consumers: distinguish a
quantitatively wrong forecast from a model that cannot issue one, retain
coverage alongside scores, and avoid optimistic results created by dropping
unsupported observations. The result is applicable as finite mathematical
forecast-accounting structure; it is not yet an integrated RET application.

The noise family and all priors are hypothetical and supplied. No empirical
sensor calibration, explanation of conflicting observations, apparatus
authentication, fallback decision, robust optimization, cost model,
Lean verification, ontology, new physics or gravity correspondence is claimed.

## Proposed next gate: QR-05Y, explicit N-forecast fallback

Keep X's four actual/assumed experiments unchanged. On an assumed-supported
report, retain the assumed forecast exactly. On an unsupported report, apply
a separately declared N-conditional fallback from W. Preserve fallback mass
and supported/fallback score contributions; do not retroactively turn X's
null full scores into estimates. Compare the resulting complete rule with
the N-only forecast under the actual law, allowing it to perform worse.

A prospective family-specific theorem makes the expected boundary clear.
An unsupported W report under a clean assumed model has zero clean-label
probability within its N fiber. Under positive actual replacement, that
report's likelihood is constant across current states in the fiber.
Its actual posterior/future law is therefore the N-conditional law.
The proposed fallback would be Bayes-correct on precisely these missing
reports: fallback regret zero, completed regret equal to X's supported
regret, and completed risk equal to X's supported forecast risk plus its
full-minus-supported Bayes risk.

Those are predicted consequences of this family, not a new robustness
discovery. The gate would verify an explicit total forecasting rule and its
access/coverage contract. It would not repair wrong forecasts on already
supported reports or establish a generally optimal fallback.
Include a generic non-W countercontrol with positive fallback regret to
prevent treating this family-specific theorem as an unconditional guarantee.
No Y outcomes have been computed.
