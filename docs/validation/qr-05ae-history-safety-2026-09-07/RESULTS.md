# QR-05AE: history-level safety under retained witnesses

7 September 2026. Exact finite-model diagnostic; not empirical safety or
geometry reconstruction. The [prospective protocol](README.md) precedes
every AE fixed coefficient, decomposition and outcome. Base: pushed AD
commit `070f4795ddf48513839a1e85f3121681c943c645`.

## Result

No hidden positive conditional-history excess was found under AD's retained
common mechanisms and unchanged policies. All 240 decision/world
certificates have nonpositive expected Brier excess for every included
history and every weight in the supplied policy set. There are 96
decisions over six experiments and 482 original case-history occurrences.
Every original-weight aggregate recovers its AD certificate exactly.

The fixed examples therefore show no positive harm contribution cancelled
by negative benefit. The generic tests explicitly exhibit and detect such
cancellation, so its absence in the fixed cases is not assumed by the API.
The two engines, root oracle and independent raw-auditor helper agree on
the entire six-case suite. Final publication verification is recorded below.

| Frozen experiment | Histories | Point-policy worlds | Interval-policy worlds | Worlds with possible history harm | Strata |
| --- | ---: | ---: | ---: | ---: | ---: |
| left_balanced | 77 | 0 | 40 | 0 | 120 |
| left_biased | 77 | 0 | 40 | 0 | 120 |
| right_balanced | 78 | 30 | 10 | 0 | 60 |
| right_biased | 78 | 30 | 10 | 0 | 60 |
| mixture_balanced | 86 | 30 | 10 | 0 | 60 |
| mixture_biased | 86 | 30 | 10 | 0 | 60 |
| Total | 482 | 120 | 120 | 0 | 480 |

World counts include repeated actual levels under different declared bounds
and policies; these are not independent physical trials. The 480 strata
comprise 360 singleton points and 120 open intervals, with 38,160 complete
history/sign memberships. No interval-used profile has an interior history
sign root in these fixed cases. Generic tests exercise distinct, duplicate
and near roots and all nontrivial boundary cases.

Of the 240 worlds, 72 have some strictly benefited histories at the retained
policy; the other 168 have only zero excess throughout that policy set.
There are 180 negative and 37,980 zero stratum memberships, with no positive
memberships. Both left cases are entirely zero. Each right case contributes
36 negative memberships and each mixture case 54. These are repeated
history/stratum occurrences, not distinct histories or independent trials.

## What this closes—and what it does not

This closes the proposed witness-limited diagnostic without finding a
new failure. It strengthens our description of these fixed witnesses:
AD's case-average benefit is not masking a harmed history here.
It does NOT establish history-level robustness over AC's whole replacement
simplex. A mechanism maximizing aggregate risk need not maximize the risk
of a particular history; another tied aggregate-maximizing mechanism can
also redistribute local risk. No new mechanism was optimized or tested.

History risk is an expectation over that history's report/future law,
not a promise that every realized outcome incurs a smaller loss. A group's
likelihood mass is the original probability of histories with that sign
of conditional expected excess, not the probability of an adverse realized
score. No empirical calibration or deployment decision follows.

All AD policies, complete interval families, forecasts, witness laws and
case-average guarantees remain unchanged. The full AD case is retained as
the exact baseline, including all earlier AC/AA failures and harmful
unselected candidates. No risk was clipped, reweighted or hidden by
selecting a different policy per history, bound realization or mechanism.

## Mathematical construction

For each original history H, assumed model s and actual level t under the
same common witness, derive the conditional-history polynomial

    Q_H,s,t(a) = A_H,s,t a^2 - 2 B_H,s,t a.

History weight w_H is outside A_H and B_H. The root producer uses
conditional-report vector squared distances/cross products. The auditor
independently expands literal Brier-loss coordinates against conditional-H
unnormalized joint masses, which sum to one. Neither fits coefficients to
alpha samples. All 7,712 history-profile rows are retained in the input;
all 96 weighted actual-world polynomials recover AD exactly.

A supplied point policy is diagnosed at its unchanged weight. A supplied
whole-interval policy retains the sorted distinct knots 0,1 and all eligible
history roots 2B_H/A_H in (0,1). Every knot singleton and every intervening
open interval is included. The sign proof uses

    Q_H(a) = a(A_H a - 2B_H),

not a sampled midpoint or an optimizer ratio B_H/A_H. Duplicate roots retain
every owning history; the knot list alone is deduplicated. Aggregate zeros
do not create extra history sign-change knots. Different worlds retain
their own partitions of the SAME symbolic alpha, without selecting it
separately for each world or history.

Each stratum has complete positive, negative and zero history groups with
their original-weight masses and coefficient subtotals:

    P(a) = sum_positive w_H Q_H(a),
    N(a) = sum_negative w_H Q_H(a),
    Z(a) = sum_zero w_H Q_H(a),
    aggregate polynomial = P + N + Z.

N is signed negative contribution; benefit magnitude is -N. On a singleton,
the zero group may have a nonzero polynomial whose value vanishes only at
that weight. Omitting Z would make a coefficientwise P+N identity false.
On an open stratum Z is identically zero. At every singleton, literal
weighted history scores and evaluated group polynomials agree, with
P>=0, N<=0, Z=0 and aggregate=P+N.

The independent auditor literally rescores 206 case-local unique shared-alpha
(s,t,a) boundaries, covering 16,596 conditional history scores. These include
all interval knots as proof boundaries, not chosen interval policies.
All 360 retained point strata are checked against those scores; open strata
use complete sign-factor proofs. The entire baseline and output wire are
compared, not only aggregate numbers or boolean flags.

## Nonvacuous controls and resource boundaries

For two equally weighted generic histories,

    Q1(a) = 2a^2 - a/2,
    Q2(a) = 2a^2 - 3a/2,

the shared point a=1/2 gives conditional excesses +1/4 and -1/4.
Aggregate excess is zero, but harm is 1/8, signed negative contribution is
-1/8, and positive/negative history masses are each 1/2. The full interval
partition has knots 0,1/4,3/4,1 and all seven point/open strata. The aggregate
zero at 1/2 is not an individual-history sign knot. This is an abstract
admitted-polynomial control, not a claimed frozen Brier producer.

The API also handles signed linear/flat histories, roots at endpoints,
double zeros, coincident crossings and nonzero singleton-zero-group
polynomials. It does not reject positive risks. It receives supplied
polynomials, original weights and a supplied policy—not raw laws or prior
artifacts—and authenticates neither their origin nor policy optimality.

Before any root division or scoring, conservative reservations use eligible
root multiplicity, not the later number of distinct roots. Duplicate-root
deduplication can reduce execution but cannot retroactively admit a request
whose reservation failed. Native/DAG/depth/byte checks precede whole
serialization; all retained rational components are bounded to 4,096 bits.
Oversized internal weighted products may cancel, but separately retained
group coefficients or harm/benefit values cannot evade their bit limits
just because aggregate net risk cancels.

The fixed suite executes 89,968 declared work visits, equal to its reservation;
these are specified logical visits, not CPU operations or physical time.

## Verification and provenance

External preflight, frozen tests, exclusive final capture, both fresh
read-only replays and the final-capture raw-history audit all pass.

The complete frozen suite passes 289 tests in each mode: normal in 105.53s
and optimized in 105.44s. This comprises 254 mathematical/adversarial tests
and 35 capture-lifecycle tests. The dedicated non-assertion guard subprocess
records 511 explicit rejections in each mode, including 45 pre-serialization
graph checks; there are 203 malformed fixtures. The full-output, full-case
and producer corruption controls reject 16, 5 and 6 nonvacuous mutations,
respectively. Bounded corruption tests bypass only the prior AD verifier,
which is independently covered by the complete six-case runner test.
Optimized pytest emits its expected warning about non-test assertions;
production guards and the explicit subprocess checks do not rely on assert.
Scoped Ruff checking and formatting checks pass.

The first fixed comparison passed in 42.861439000000246s with all four
protocol/implementation sources and 35 prior artifacts unchanged. The
complete suite is 6,321,432 bytes, SHA256
`9273c48f22dc997d1653293690eb13298e8cf1e3b79592982a4388efb73cd433`.
An independent fixed auditor-helper run passed 1,545,379 checks in
10.150310s and matched that complete suite. Its 797,248-byte analysis list
has SHA256
`11f57e53aa6b94b24bd670ba85b21c7ac58d8b34023a0c78b65737c7ff4ba581`.
The helper is not a substitute for the full raw-history audit.

The exclusive external preflight took 45.70965054100088s and retained
6,327,928 bytes, SHA256
`db8e31c3ad752ce833fb2c0d477246211de02f3e3b90a3f6c1b0558016d9713d`.
Its full raw-history audit passed 47,793,220 checks in 66.76605633400322s,
authenticating all 97 source/prior identity targets before and after.

The exclusive final [results.json](results.json) capture took
46.353178375000425s and retained 6,327,929 bytes, SHA256
`5b7946512ea77e076387a25d5cf46c30d25a42d37fdd66ae39a4edadb179bbde`.
Its complete mathematical suite is byte-identical to the preflight and
first fixed comparison; only capture runtime metadata differs. Suite-end
process high-water RSS was 661,700,608 bytes, not an incremental allocation
or application performance claim. Every retained suite rational component
remains within 4,096 bits.

Fresh normal and optimized read-only replays pass in 48.384894125003484s
and 48.47529483299877s, respectively. The final raw-history audit passes
47,793,220 checks in 69.52399166700343s, matching the independent analysis
digest above. It rebuilds 4,447 raw states, 168,388 raw subset atoms and
482 raw-history beliefs, then authenticates the complete X/Y/Z/AA/AB/AC/AD/AE
mathematical reporting chain without importing the engines, runner or tests.
All 97 source/prior identities and final capture bytes are unchanged before
and after. No numerical or scientific-rule correction was required after
the first fixed comparison.

Seven source files are frozen for publication: README.md, safety.py,
reference_qr05ae.py, study.py, test_qr05ae.py, test_capture.py and audit_json.py.
The full audit authenticates 35 prior artifacts, seven sources each for
AE/AD/AC/AB/AA/Z/Y/X and six W sources: 97 distinct source/prior targets,
plus the capture itself, checked before and after. Prior polynomial identity
is not reported as a fresh derivation; historical public API/runtime and
broader operator/minimality obligations are not replayed. RESULTS.md and
the roadmap remain outside the frozen source ledger.

## Next: QR-05AF, supplied-geometry interface and resolved diagnostic

Return to geometry with the interface protocol inside the next gate, not
another forecasting optimization prerequisite. Freeze a small supplied
geometry family, marked probe intervals, local order/count or scalar-kernel
questions, observation access and density/sampling assumptions before new
computations. Check which retained information supports those questions;
do not assume a predictive summary is geometrically sufficient.

Keep geometric truth on the generator/auditor side. Carry D/E's local
density ambiguity, endpoint collisions, finite-mesh bias, missing support
and nonuniform/correlated-sampling controls. Passing a local correspondence
test would not establish metric identification, continuum emergence,
quantum-channel coupling or gravitational dynamics. RET integration and
Lean remain separate. No AF outcomes are computed by this gate.
