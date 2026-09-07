# QR-05Y results: fallback completes a policy without repairing supported errors

7 September 2026. Exact finite classical forecast-policy gate.
Completed with frozen-source tests, exclusive capture, exact replays and
independent raw-history audit. No physical or empirical claim is added.

## Outcome

The explicit N-conditional fallback supplies a forecast on every previously
unsupported report in the declared experiment. The original supported
forecasts are unchanged, and X's incomplete scores remain null in a separate
`x_scores` record. Completing the policy does not retroactively complete X.

All 96 fallback-used pair cells have zero regret in these six W cases.
This was predicted in the protocol: a clean-model-impossible report produced
by positive uniform replacement has constant likelihood within its current
N fiber. Its complete current posterior and future law equal the N-conditional
ones. It is a consequence of this particular replacement model, not evidence
that arbitrary fallbacks are correct.

Completion does not repair wrong forecasts on supported reports. In the
mixture cases, even actual replacement 1/2 with assumed replacement zero
makes the completed policy strictly worse than N-only in case-average risk.
All its excess regret comes from supported forecasts, not the fallback.

Across the six cases, each positive-actual/assumed-clean comparison completes
22 previously incomplete histories and uses fallback on 32 report cells.
The three actual levels give 66 history-pair and 96 report-pair occurrences,
not additional histories, raw states or independent experimental repetitions.
All 482 histories now have defined scores for all 16 pairs, within the
declared report union. Nothing is promised for an unseen apparatus output.

## Quantitative comparison with coarse-only prediction

Define gain as N-only risk minus completed-policy risk. Positive means the
completed policy is better; negative means it is worse. Actual report and
future probabilities supply the scoring weights.

For right_balanced, let G=49/5971968 be W's clean added NMT gain.
The following table gives gain/G:

| Actual t \\ Assumed s | 0 | 1/2 | 3/4 | 1 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 1 | 3/4 | 7/16 | 0 |
| 1/2 | 0 | 1/4 | 3/16 | 0 |
| 3/4 | -1/2 | 0 | 1/16 | 0 |
| 1 | -1 | -1/4 | -1/16 | 0 |

The same normalized table holds for right_biased with G=888832/31381059609.
This is not a universal mismatch threshold, nor a percentage change in total
prediction error. The already-small added-information gain is the denominator.

The mixture cases preserve negative results that an unsupported-report
repair alone cannot remove:

| Case | Gain at actual 1/2, assumed 0 | Gain at actual 3/4, assumed 1/2 |
| --- | ---: | ---: |
| mixture_balanced | -377/191102976 | -463/7166361600 |
| mixture_biased | -637952/94143178827 | -4566016/21182215236075 |

At each of these two settings, counts across the six cases are 2 histories
better than N-only, 4 worse, and 476 equal. These are unweighted inventory
counts; each case's risk uses its own original history likelihoods. The six
experiments are not pooled into a probability distribution.

At actual full replacement with any smaller assumed level, all 10
informative histories across the cases are worse than N-only. The label
carries no additional information under that actual model, while the
misspecified forecast still relies on it. Assuming full replacement is
N-only and has zero gain for every actual level. Both left cases have zero
gain throughout. Every correctly specified diagonal remains Bayes-correct.

## Contract and mathematical checks

For supplied actual future law p and forecast f, the unscaled Brier risk is

    L(f;p) = 1 - 2<p,f> + ||f||² = R(p) + ||p-f||²,
    R(p) = 1 - ||p||².

For each history, one prefix-indexed fallback table is shared across all
actual/assumed settings. The chosen policy depends on the received report
and assumed support, not on the actual noise level or future outcome:

    f_j(z) = p_j(.|z)  when assumed mass is strictly positive,
             g_N(z)   when assumed mass is exactly zero.

A tiny positive assumed mass remains supported; no numerical threshold or
posterior repair is introduced. A fallback can put probability on a future
symbol absent from every actual/assumed sparse law, and that coordinate must
still be scored. Both the completed policy and coarse-only comparator are
evaluated on every actual-positive report, including when they coincide.

Supported and fallback contributions retain their ORIGINAL actual weights.
No division by coverage or fallback mass is allowed. Likewise, history
aggregation retains original positive likelihoods. The complete identities are

    completed risk = supported risk + fallback risk,
    completed regret = supported regret + fallback regret,
    completed risk = full Bayes risk + completed regret,
    gain = coarse risk - completed risk
         = coarse regret - completed regret.

On fallback-used cells the chosen and coarse forecasts coincide, so local
gain is zero; all gain comes from supported cells and its absolute value is
bounded by twice the supported mass. Gain is signed, not an improvement
certificate. Zero regret requires equality of complete future laws, not just
equal scalar risk.

For W specifically, fallback regret is zero, completed regret equals X's
supported regret, and completed risk equals X's supported forecast risk plus
full-minus-supported Bayes risk. Coarse-only risk equals W's N risk at every
actual level. The independent raw audit must authenticate these premises,
not merely check the resulting scores.

The generic API has a weaker contract: a supplied prefix-grouped forecast
need not be a true N-conditional law. Countercontrols allow positive fallback
regret, varying coarse risk with actual level, and gains reaching both -2
and +2. Shared unconditional future marginals do not certify the W noise
mechanism or apparatus provenance.

## Retained evidence and work accounting

| Object | Count |
| --- | ---: |
| Cases / positive histories | 6 / 482 |
| Actual/assumed pairs per history / history-pair results | 16 / 7,712 |
| Input report cells / channel future-law atoms | 2,064 / 9,272 |
| Explicit fallback entries / fallback future-law atoms | 482 / 1,936 |
| Retained pair cells | 8,256 |
| Supported / fallback-used pair cells | 8,160 / 96 |
| Completed-policy / coarse-comparator support visits | 74,176 / 74,312 |
| Total support visits | 148,488 |
| Public analyze calls / malformed calls rejected by runner | 12 / 14 |

Work counts reflect both actual-plus-forecast support traversals for each
comparison, even where the forecasts coincide. They are bounded work
accounting, not wall-clock performance claims. All complete laws, X nulls,
scores, original-weight aggregates, counts and first witnesses are retained.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 16,474,309 bytes,
SHA256 `c4189b0f1bb0df4bb3e5f14c1969ede0ee754f59b4bc99e89aeac8d6b065891f`.
The canonical suite is 16,468,704 bytes,
SHA256 `64510d40654f579e21bb1f617a713f5674adfc36ed1106571bca57017b8ad61a`.
The canonical JSON list of six complete analyses is 15,713,927 bytes,
SHA256 `b6d2def3728f4aeaf152e305c87bccc7ad75155a3cff2e4b25d00f95cd52a180`.

| Check | Outcome |
| --- | --- |
| Full normal tests | 176 passed in 187.13s |
| Full optimized tests | 176 passed in 186.76s |
| Exclusive final capture | 40.384568375000526s |
| Fresh normal exact read-only replay | 45.521857208000256s, exact |
| Fresh optimized exact read-only replay | 45.57421175000036s, exact |
| Final JSON-only raw-history audit | 13,808,177 checks in 23.846739999999954s, passed |

Optimized pytest emits its expected assertion warning. Each dedicated
normal/optimized guard subprocess performs 265 explicit rejections, including
54 pre-serialization cycle/depth/expanded-DAG rejections across both cores
and runner. These guard checks do not rely on Python assertions. There are
94 malformed public-input fixtures and 22 nonvacuous complete-output
corruptions, plus pinned-producer corruption controls. Both actual/comparator
score traversals are counted even when forecasts coincide. Pre-score caps,
4096-bit input/retained bounds with valid intermediate cancellation, benign
shared containers and detached output ownership are checked.

The stdlib JSON-only audit authenticates 4,447 raw states and rebuilds
168,388 induced-subset relations with 9,201,100 subset-Mobius subtractions.
It checks 8,894 raw K3 member rows and 32,768 categorical vertex-lifetime
assignments, reconstructing all 482 current beliefs and 2,064 noisy cells.
Both complete current posteriors and future laws are compared against the
raw N conditional on all 96 unsupported pair cells.

The complete original X input, scores, nulls and reporting are independently
rebuilt; Y's explicit fallback table is derived from raw N cells, and the
full Y input, output, witnesses, counts, controls and native/canonical
envelope agree. Across X/Y scoring, the audit evaluates 763,054 explicit
actual-outcome/forecast-coordinate squared-error terms. Its 195,598
disagreement summands are scalar terms, not enumeration of every replica
outcome pair. Neither metric is the cores' linear support-visit count.

The auditor imports no executor, runner or test; it reads their sources only
as bytes for identity. It also verifies seven X and six W producer source
hashes. Prior public APIs, broad operator/minimality certificates and source
aliases are not replayed. The inherited fine-polynomial digest remains
pinned producer identity, not an independently rederived polynomial.
Historical API/runtime counters are validated metadata, not reproduced
performance measurements.

The protocol was recorded before any Y case outcomes. The first complete
primary/reference/independent-runner comparison passed in 33.11987054200017s.
After that comparison, before source freeze, the runner was strengthened
with an explicit comparison of W's retained current posterior against the
N posterior on fallback-used reports. Future-law equality was already checked,
and independent raw posterior equality was already preregistered. This is
additional verification coverage, not a change to policy, scores, inputs,
expected outcomes or acceptance criteria. Initial Ruff cleanup did not alter
mathematics; no mathematical or test correction was needed, and no scientific
setting was tuned.

A temporary create-only capture outside the checkout exercised the audit
before final freeze; its 13,808,177 checks passed in 20.23019108399967s.
That preflight was not overwritten or substituted for the published artifact.
Both final full test suites passed on their first runs.

Seven frozen source/protocol files and all 29 producer artifacts stayed
unchanged through final tests, capture, replays and audit. Artifact bytes
stayed unchanged after creation. The audit additionally verified seven X
and six W source hashes before/after. All final runs use isolated Python
and fresh explicit external bytecode caches. RESULTS.md and the roadmap
are outside the frozen ledger. No frozen source or artifact was edited.

The staged publication whitespace check flagged one trailing blank line at
the end of the frozen README.md. Its audited bytes were preserved. The staged
check passes with only the blank-at-EOF warning disabled; this is a formatting
disclosure, not a mathematical or verification change.

## Application value and boundaries

The useful structure is explicit separation of forecast availability,
fallback behavior, and error on supported reports. A consumer can issue a
declared coarse forecast where a detailed model is silent, retain the missing
support evidence, and measure whether the resulting whole policy is actually
better than staying coarse. Availability alone is not forecast hardening.

This is mathematical forecast accounting on supplied finite laws. It is not
an integrated RET capability, a calibrated sensor policy, an empirically
validated robustness claim or a deployment recommendation. No observation is
dismissed as noise or setup error. No Lean verification, ontology, new physical
law, metric reconstruction or gravity correspondence follows from this gate.

## Proposed next gate: QR-05Z, fixed attenuation of supported forecasts

Keep the same actual/assumed experiments and declared fallback g. Compare a
prespecified menu of retained detailed-forecast weights a in {0,1/2,1}:

    h_a = g + a(f-g),

where f is Y's completed policy. Apply each fixed rule without access to the
actual noise index or future outcome; report all rules, not an oracle-selected
winner. Fallback-used reports are unchanged because f=g there. Keep original
weights, complete future laws, Y identities and negative gains visible.

The prospective quadratic control is

    gain(a) = a*gain(1) + a*(1-a)*E_actual ||f-g||².

At full replacement the actual future law is g, so this reduces to
-a²*E_actual ||f-g||². Nonzero retention can therefore remain harmful; uniform
dominance over coarse-only across the full menu is not a plausible acceptance
criterion. The gate would quantify an explicit attenuation tradeoff, not
optimize noise, fit a policy, establish robustness to arbitrary mechanisms or
recommend deployment. Record its full protocol before any Z case run.
No Z outcomes have been computed.
