# QR-05U results: exact inference from coarse received records

6 September 2026. Finite, declared-prior partial-observation gate.

## Outcome

Beliefs over the 416 certified classes preserve exact inference and future
question laws after two coarse received records on the unchanged domain.
Sequential normalized Bayes filtering, independent unnormalized class-path
filtering and a raw induced-subset path oracle agree on all six cases.

Every case has positive histories with the same latest record but different
future question laws. Forgetting the first record and replacing the posterior
by one MAP class both produce retained prediction errors. The menu and
witness ordering were fixed before U outcomes; neither failure was assumed.

| Retained inventory | Count |
| --- | ---: |
| Raw observations / certified classes | 4,447 / 416 |
| Hypothetical priors / schedules / cases | 3 / 2 / 6 |
| Positive first-record histories | 80 |
| Positive two-record histories | 482 |
| Current-history posterior / prediction atoms | 1,026 / 1,936 |
| Same-latest-record history pairs compared | 1,810 |
| Pairs with different future laws | 36 |
| Histories differing from latest-only prediction | 24 |
| Histories differing from MAP prediction | 34 |
| Within-H initial-prior redistribution checks | 12 |
| Raw member/rate rows checked | 26,682 |
| Raw positive rate atoms checked | 1,010,328 |

These counts describe the fixed six-case experiment, not coverage of every
possible prior, rate schedule or observation policy. The all-member bridge
covers both frames; the selected application priors begin in frame0.

## A concrete history effect

Take the declared left prior: initial raw state 612 is known with probability 1.
Its eligible ranks are (3,3). Under the balanced schedule, receive either:

- Y1=[0,1,4,2,0], then Y2=[0,1,4,2,0]; or
- Y1=[0,1,5,2,0], then the same Y2=[0,1,4,2,0].

A record is [frame,N0,N1,N2,N3]. Both histories have positive probability.
After the separately declared predictive thinning step, the question value
[0,1,3,0,0,0,0] has probabilities 13/336 and 1/16, respectively.
This describes three retained interior vertices with no comparable interior
pair, and zero declared motifs. The probability difference is exactly 1/42.

For the first history, forgetting Y1 gives 69/1744 instead of 13/336.
The chosen MAP current class predicts zero for this question, despite its
positive mixture probability. These compare the SAME prior, schedule,
latest record, stage and future question, not different experiments.

Knowing the initial state is not knowing the current state after hidden
thinning. The current posterior tracks uncertainty created by unobserved
deletions. Equal posterior vectors suffice for equal future laws; a mere
difference in posterior vectors was not accepted as a history witness.

## Mathematical contract

The supplied class-local rows reconstruct the exact class thinning law K.
For the explicit record map e and a current belief b:

    bminus(j) = sum_i b(i) K(i,j)
    Z = sum_{e(j)=y} bminus(j)
    bnew(j) = 1[e(j)=y] bminus(j) / Z, provided Z > 0.

The stages are prior → K1 → received Y1 → K2 → received Y2 → K3 → prediction.
No third observation is received. Posterior coordinates identify CURRENT
classes, not hypotheses about the original source; initial-source smoothing
is outside this contract.

All first/joint likelihoods, posterior normalizations and supports, tower
identities, marginalizations and unconditional three-rate composition hold
exactly. Unconditional product-rate composition does not authorize dropping
informative intermediate records. Impossible known records return an explicit
unavailable posterior/prediction; malformed or unknown records are rejected.

The three priors are deltas at states 612 and 625, and their fair mixture. They are
hypothetical inputs, not fitted or calibrated beliefs. For each schedule,
moving a given initial H mass to the first or last raw member of its fiber
leaves every history likelihood, current H posterior and future law unchanged.
This does not assert equality of raw-state posteriors.

## Access, authentication and independence

The received record map is [frame,N0,N1,N2,N3]; the future question adds M,T.
Both maps are separately checked on every member of every H fiber.
The local deletion table alone does not determine these observable labels.

The public filtering core receives only local class rows, their explicit
label table, class prior and three rational rate pairs. It receives no raw
orders, H feature keys, full subset profiles or prior artifacts.
Its structural parser cannot authenticate an empirical apparatus or
raw-order realization; the independently checked producer bridge is necessary.

Original vertex 1 membership is not H-measurable: raw states 1 and 4 share
class 1 but have values 1 and 0 for that predicate. Custom named-ID observations
are not supported by the public contract. This is a retained access limitation,
not something classified as noise.

The raw oracle independently enumerates induced subsets and weighted nested
paths. Raw features, actual H memberships, class-local rows, labels and all
rate laws are reconstructed on the full retained domain. The 1,576 local
entries recover 8,231 class-profile atoms, with T's exact recurrence/operator
certificate unchanged. Neither implementation imports prior executors or
mutable RET/core code. T's raw/local/label tables are explicit dependencies,
not a hidden refinement/minimality replay.

No source/alias universe, P consumer, R helper or Q four-variable certificate
is rerun. No storage or performance benchmark is claimed.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 1,320,664 bytes,
SHA256 `a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee`.
Its canonical suite is 1,315,752 bytes,
SHA256 `78e6f50ba1234d3dfb88ae43503ae35f58a08b2c2614839cc09fdef385e7d1e0`.

| Check | Outcome |
| --- | --- |
| Full normal tests | 157 passed in 69.70s |
| Full optimized tests | 157 passed in 69.92s |
| Exclusive capture | 33.823652582999784s |
| Fresh normal exact read-only replay | 34.36701383299078s, exact |
| Fresh optimized exact read-only replay | 34.323266291001346s, exact |
| Separate JSON-only postflight | 13,955,344 checks in 13.831031166017056s, passed |

The optimized suite has only pytest's expected assertion warning.
Each dedicated bounded normal/optimized subprocess checks 102 explicit
malformed-input rejections without relying on Python assertions.
Tests also retain hand-calculated Bayes, tie/unique-MAP, identity, full-deletion,
nonrealizable local-model, arithmetic-cap and mutable-ownership controls.

The runner makes 12 public analyze calls and 18 separate filter_history calls;
the latter include 4 known-impossible cases. It rejects 14 malformed analysis
inputs. The independent postflight verifies these counts as retained metadata,
not as a claim to have re-executed the public helpers.

The JSON-only audit reconstructs raw features, all local/subset laws and
filtering evidence without importing any executor, runner or test.
It uses per-vertex survival/deletion stages across the three thinnings:
98,304 lifetime assignments cover the six cases and 12 alternative raw lifts.
Its feature audit separately reconstructs pair-union grades through subset
Möbius inversion. Source files are read only for their byte identities.

Six source/protocol files and all 25 prior artifacts matched their pre-test
ledger after tests, capture, replays and postflight. Artifact bytes stayed
unchanged after exclusive creation. All final runs used isolated Python and
explicit fresh external bytecode-cache prefixes. No frozen source or artifact
was changed after capture.

The protocol, priors, schedules, maps, caps and acceptance criteria were
fixed before U outcome computation. Before execution, schema clarification
made the depth bound, hash scopes and complete record validation before
zero-evidence branching explicit. The full tests, capture and JSON-only
postflight passed on their first runs without source corrections.
An auxiliary primary manual-control harness had an undefined local alias;
correcting that harness required no implementation, test, protocol or
mathematical-output change. The corrected controls passed before capture.
RESULTS.md and the roadmap remain outside the frozen ledger.


## Boundary and proposed next gate

This is exact prior/design-relative classical filtering on a supplied finite
observation calculus. It does not identify an actual physical order, validate
an empirical prior, or derive a new physical memory, time, quantum, metric
or gravity law. There is no ontology commitment, RET integration, Lean
installation or apparatus calibration.

Proposed QR-05V: predictive value of richer readouts. Keep U's K2/K3,
hypothetical priors and full Q3 target fixed. At a retained current posterior,
compare nested readouts N, (N,M,T) and H, with H explicitly an oracle upper
bound rather than an assumed physical sensor. Compute exact expected Brier
risk and its reduction, verify the conditional-mixture identity and
nonnegative improvement, and retain strict-gain/no-gain cases as outcomes.
Even full H need not eliminate fresh K3 randomness. No cost model, adaptive
policy, sensor availability or empirical calibration is silently introduced.
This proposal measures added information without altering the target or
thinning schedule to make prediction easier. No V outcome is computed here.
