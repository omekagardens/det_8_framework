# QR-05W results: information loss from imperfect current readouts

7 September 2026. Exact finite classical noise-channel gate.

## Outcome

The two summary-only implementations and an independent raw-history audit
agree on complete noisy-readout laws, current posteriors, future predictions,
stochastic couplings and Brier-risk identities for all six experiments.

Under the fixed random-replacement model, the useful added NMT information
falls substantially as noise increases. At replacement level 1/2, the four
informative cases retain about 20.6–25% of their clean added gain; at level
3/4 they retain about 5.0–6.25%. Complete replacement retains none of the
information beyond N. These percentages concern the already-small added
Brier gain, not a percentage reduction in total prediction error.

| Case | Clean added gain over N | Retained at t=1/2 | Retained at t=3/4 | Retained at t=1 |
| --- | ---: | ---: | ---: | ---: |
| left_balanced | 0 | undefined | undefined | undefined |
| left_biased | 0 | undefined | undefined | undefined |
| right_balanced | 49/5971968 | 1/4 | 1/16 | 0 |
| right_biased | 888832/31381059609 | 1/4 | 1/16 | 0 |
| mixture_balanced | 103/15925248 | 319/1545 | 31/618 | 0 |
| mixture_biased | 2114560/94143178827 | 917/4425 | 521/10325 | 0 |

Undefined retention is stored as null when the clean gain is zero. Its
numerator is also zero; inventing a percentage would conceal the 0/0 case.
Case retention is the ratio of likelihood-weighted gains, not a uniform
history average or an average of individual retention fractions.
The six hypothetical priors/schedules are not pooled.

Strict added gain occurs in 10 of 482 histories at each of t=0,1/2,3/4,
and in none at t=1. As recorded BEFORE W outcomes, survival of strict gain
for every t<1 follows from this channel family. It is not independent
evidence of robustness or practical sensor performance. Each adjacent
garbling has strict expected-risk loss in those same 10 histories.

N is the current chain-count record [frame,N0,N1,N2,N3]; NMT adds the
current motif counts M,T. Every actual U history already knows N.
The full-H oracle remains a lower-risk control, with positive residual
future randomness in 402 histories. Neither H nor a physical NMT sensor
is assumed to be experimentally available.

## What noise means here

For the true CURRENT label a in a fixed N fiber, report z according to

    C_t(z|a) = (1-t) 1[z=a] + t / |A_N|, for z in A_N.

A_N is the set of DISTINCT NMT labels in the WHOLE model, not just
currently probable labels and not a class-multiplicity-weighted alphabet.
There are 72 N fibers and 93 distinct NMT labels.

The replacement coin is unobserved. A replacement may draw the original
label again, so t is not the probability of a wrong displayed label.
For a two-label fiber, the misreport probability is t/2.
At complete replacement, the displayed label remains random but carries
only N information. This is information equivalence, not literal equality
with an N-only record.

Noise does not alter current H2, the fresh K3 transition or the complete
future Q3 target. It is independent of K3 conditional on H2. The proof
couplings use intermediate reports, but the forecaster receives only the
one report of the experiment being scored—not those intermediate records
or the replacement coin.

## Two concrete histories

For right_balanced history 64, both received records are [0,1,5,3,0].
The two clean current NMT cells have equal probabilities. Their clean added
gain is 7/2048; it becomes 7/8192 at t=1/2 and 7/32768 at t=3/4.
The retained fractions are exactly 1/4 and 1/16.

For mixture_balanced history 71, the received records are the same but the
clean cell probabilities are 3/4 and 1/4. Its clean gain 21/8192 becomes
21/40960 and 1/8192, retaining 1/5 and 1/21 respectively.
Unequal prior conditioning changes the amount retained even under the same
noise family. Each of these histories has likelihood 1/648 in its own
declared experiment; they are not a comparison under a common prior.

## Mathematical certificate

For current belief b and fixed future class law k_h(q), the joint law is

    J_t(z,h,q) = b_h C_t(z|a_h) k_h(q).

Conditioning each positive report mass gives the full current posterior and
future law. All noisy levels preserve the same marginal b and future Q3
distribution. Zero report masses are omitted before division.

For true prediction p, use unscaled categorical Brier Bayes risk
R(p)=1-sum_q p(q)^2. Each readout gain equals the weighted squared distance
of its conditional future laws from the baseline future law.

Adjacent comparisons use garbling levels 1/2,1/2,1. Matrix multiplication on
every full-model source label verifies C_0 C_1/2=C_1/2,
C_1/2 C_1/2=C_3/4 and C_3/4 C_1=C_1. Their joint report pairs overlap:
a later report can receive mass from several earlier reports.

For every later cell, reverse-Bayes weights are reconstructed from retained
coupling and receiving-cell masses. The complete current-posterior and future-law
mixtures are verified. In particular,

    R_later - R_earlier
      = sum_z,w P(z,w) ||p_earlier(.|z)-p_later(.|w)||^2 >= 0.

Zero loss holds exactly when every positively coupled earlier future law
equals its later law. Changed beliefs or labels alone do not establish loss.
The three expected losses telescope to the clean gain over N.
The full risk order is

    R_H <= R_clean <= R_half <= R_three_quarters <= R_full = R_N <= R_baseline.

Expected-risk ordering does not imply pointwise ordering for every displayed
symbol. A hand binary identity-future control with prior (9/10,1/10)
has rare-symbol conditional risk 3/8 at t=1/2 and 135/512 at t=3/4,
which DECREASES. The overall risks increase from 9/56 to 45/256.
Both statements are compatible because the report probabilities change.

Other analytical controls distinguish hidden from revealed replacement
coins, duplicate classes from distinct labels, zero-prior alphabet entries,
multi-N beliefs, future-correlated noise leakage and fresh future randomness.
They are controls, not additional fixed-case or empirical experiments.

## Retained domain and access boundary

| Retained or checked object | Count |
| --- | ---: |
| Raw observations / certified H classes | 4,447 / 416 |
| Fixed cases / positive current histories | 6 / 482 |
| Current posterior atoms | 1,026 |
| Global channel atoms at t=0,1/2,3/4,1 | 93 / 173 / 173 / 173 |
| Actual composition products across three edges | 1,223 |
| Positive report cells across cases, by level | 492 / 524 / 524 / 524 |
| Future-law atoms across cases, by level | 2,030 / 2,414 / 2,414 / 2,414 |
| Retained report-pair coupling atoms, by edge | 548 / 644 / 644 |
| Receiving-cell checks, by edge | 524 / 524 / 524 |
| Raw-member K3 rows / positive subset atoms checked | 8,894 / 336,776 |
| Public analyze calls / malformed calls rejected by runner | 12 / 14 |

Each positive-noise level has 32 more positive report cells than the clean
level. A declared label can be displayed even when its true current-label
probability is zero. These are additional possible reports, not newly
created raw states or new physical events.

The core receives class-local rows, supplied labels, current H beliefs,
history weights and the one fixed K3 pair. It receives no raw orders,
artifact paths, original prior, K1/K2 or received-history paths.
U/V producer outputs are explicit dependencies: the runner independently
rebuilds raw features, fibers, local/subset laws and complete U/V evidence
before accepting W inputs. All class-local reconstruction certificates and
all-member K3 laws are retained unchanged.

The broader U/V public-helper suites, T minimality, P consumer, R helper,
Q four-variable certificate and original source/alias universe are not
replayed. No mutable RET/core code is imported. Structural parsing is not
apparatus authentication.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 6,756,094 bytes,
SHA256 `05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a`.
The canonical suite is 6,750,889 bytes,
SHA256 `1866bca575b26214bb349d09409704c7dd536fd8d0caebbceb41ab83dd188b58`.
The canonical JSON list of six complete W analyses is 3,261,855 bytes,
SHA256 `468dab20b1ada854b11d78c92297400bdb216b09b7c2686b217f5ff1d8a2d497`.

| Check | Outcome |
| --- | --- |
| Final full normal tests | 149 passed in 77.95s |
| Final full optimized tests | 149 passed in 77.98s |
| Exclusive capture | 28.846842833999972s |
| Fresh normal exact read-only replay | 29.92382095899984s, exact |
| Fresh optimized exact read-only replay | 29.90583349999997s, exact |
| Final independent JSON-only postflight | 7,076,822 checks in 11.833938292s, passed |

The optimized suite emits only pytest's expected assertion warning.
Each dedicated normal/optimized subprocess makes 180 explicit rejections
without relying on Python assertions. These include 33 cycle/depth/explosive
DAG checks before serialization, live workload-minus-one checks for the
four new channel/coupling caps, and nonvacuous derived-arithmetic limits.
Ordinary shared inputs are accepted and outputs remain detached.

Tests reconstruct every noisy posterior/future law from raw histories and
use an independent raw two-replica disagreement oracle. They cover all
fixed-case outputs, analytical counterexamples and 36 output corruptions.
Typed cache entry, global zero-prior labels, class multiplicity, mixed-N
beliefs, weighted aggregation, and complete coupling marginals/mixtures
are checked explicitly.

The separate stdlib JSON-only audit imports no executor, runner or test;
source files are read only as bytes for identity hashes. It reconstructs raw
features and H fibers using 9,201,100 subset-Möbius subtractions, and
authenticates current histories and future joints through 32,768 categorical
vertex-lifetime assignments across K1/K2/K3.

It independently rebuilds complete V and W analyses, including all 2,064
noisy cells, 1,836 coupling atoms and 1,572 receiving checks. Conditional
two-replica disagreement identities use 24,390 scalar summands; that count
is not an enumeration of all pairs of question values. All 8,894 raw K3
member rows, local/full-subset profiles, reconstruction certificates,
risk identities, retention ratios, witnesses and aggregate laws agree.

The final closure also checks strict native/canonical mathematical bytes,
the envelope, exact source/prior inventories and complete suite summaries.
The legacy fine-polynomial digest is checked as pinned V producer identity,
not independently rederived by this postflight. Raw subsets, local rows,
class profiles and fixed K3 laws are independently rebuilt. Public-call
counts and runtime timing/RSS fields are checked as recorded metadata,
not as replayed API behavior or performance evidence.

The protocol and acceptance criteria were fixed before W outcomes.
A draft profile-cap typo was corrected to V's existing 32,768-atom bound
before any outcome computation. The initial full normal/optimized suites
each had 135 passes and 14 setup errors from one test fixture: it wrongly
applied the mathematical wire validator to the prior envelope's floating
runtime metadata. The narrow correction checks canonical envelope bytes
separately and retains strict native validation of the mathematical suite.
No implementation, experiment, risk formula or expected mathematical
outcome changed. All 149 tests then passed under both modes.

The first artifact-only mathematical audit passed. Final review extended
its coverage to canonical typed equality and envelope/suite summary
metadata before the final audit pass. This changed only the outside-repo
verification script; it did not alter frozen sources or results.
Auxiliary pre-run lint cleanup also affected only that script.

Six final source/protocol files and all 27 pinned prior artifacts matched
their refrozen pre-test ledger after the successful tests, capture, replays
and final postflight. Artifact bytes stayed unchanged after exclusive
creation. All final runs use isolated Python and explicit fresh external
bytecode-cache prefixes. RESULTS.md and the roadmap are outside the frozen
ledger. No frozen source or result has been modified after capture.

## Boundary and proposed next gate

These are exact results under supplied finite priors, laws, labels and a
hypothetical, correctly specified noise family. They do not establish actual
apparatus noise, empirical calibration, a sensor cost/utility model, an
adaptive sensing policy, RET integration, Lean verification, ontology,
new physics or gravity correspondence.

Proposed QR-05X: noise-model misspecification. Keep H2 beliefs, K3, Q3 and
the same four declared channels fixed. Compare actual channel t with an
assumed conditioning channel s across the 4×4 menu, scoring the forecast
under the ACTUAL conditional law. Verify actual Brier risk and excess risk
relative to the correctly specified forecast, without changing the target.
Use Risk(f;p)=1-2<p,f>+||f||^2=R(p)+||f-p||^2. Actual forecast risk
and regret can reach 2; they must not inherit the Bayes-risk bound of 1.

If a report has positive actual probability but zero assumed probability,
its assumed posterior is undefined. Retain the report and its actual mass
as unsupported; do not invent a forecast, silently discard it or report an
unconditional risk from the remaining supported reports.
No fallback policy, fitted calibration or robust optimization is supplied.
No X outcomes have been computed.
