# QR-05V results: predictive value of richer current readouts

6 September 2026. Finite, fixed-law classical value-of-information gate.

## Outcome

Richer current readouts can improve prediction without changing the future
question or its transition law. The improvement is selective, not universal.
Across the six fixed U experiments and their 482 positive histories, current
NMT has strict Brier-risk gain in 10 histories and oracle H in 34.
N has zero gain in all 482 because the latest received record already fixes N.

Here N=[frame,N0,N1,N2,N3] is the current chain-count record, NMT adds
the current motif counts M,T, and H identifies the certified current class.

The conditional-posterior implementation, independent joint-mass
implementation and raw nested-subset audit agree on the complete outputs.
Separate raw two-replica disagreement checks verify the risk calculation.
All comparisons retain the same complete future Q3 alphabet and fresh K3.

| Case | Histories | Strict NMT gain | Strict H gain | Positive H residual |
| --- | ---: | ---: | ---: | ---: |
| left_balanced | 77 | 0 | 3 | 64 |
| left_biased | 77 | 0 | 3 | 64 |
| right_balanced | 78 | 2 | 5 | 65 |
| right_biased | 78 | 2 | 5 | 65 |
| mixture_balanced | 86 | 3 | 9 | 72 |
| mixture_biased | 86 | 3 | 9 | 72 |

Strict counts refer to TOTAL gain from each history's baseline, not the
adjacent NMT→H increment. Counts are not history probabilities or empirical
success frequencies. Each case has its own declared prior and schedule;
the six are not pooled into a common probability experiment.

| Case | Likelihood-weighted NMT gain | Likelihood-weighted H gain |
| --- | ---: | ---: |
| left_balanced | 0 | 73/762048 |
| left_biased | 0 | 38428672/208819643571 |
| right_balanced | 49/5971968 | 578003/7733698560 |
| right_biased | 888832/31381059609 | 924076544/5805496027665 |
| mixture_balanced | 103/15925248 | 67169/684785664 |
| mixture_biased | 2114560/94143178827 | 15749896192/76914977101659 |

These are unscaled categorical Brier-risk reductions. They show exact
mathematical information value under the stated premises, not large,
cost-effective or calibrated real-world performance.

## Concrete useful and insufficient readouts

For right_balanced history 64, both received records are
[0,1,5,3,0]. The current posterior puts masses 1/3,1/3,1/6,1/6
on H classes 95, 100, 102, 104, respectively. Current NMT distinguishes
[0,1,5,3,0,0,0] and [0,1,5,3,0,0,1], each with probability 1/2.

The baseline future Brier risk is 1767/2048.
The two conditional risks are 217/256 and 223/256; their weighted mean
is 55/64. Thus the exact expected gain is 7/2048. The current readout
reveals T, not the future T or the future outcome. This positive history
has likelihood 1/648 under the declared experiment.

Under mixture_balanced, history 71 has the same two records but different
prior conditioning: the readout cell probabilities are 3/4 and 1/4.
The baseline risk 7013/8192 falls to 437/512, a gain 21/8192.
Uniform averaging of those cells would be incorrect.

Conversely, every history in the left cases has zero NMT gain, yet some
have positive H gain. At left_balanced history 42, both received records
are [0,1,4,2,0]; H reduces risk 7703/9408 to 1093/1344, a gain 13/2352.
NMT is therefore insufficient for all the predictive distinctions used by H
in this fixed case, even though NMT is useful elsewhere.

## What is established mathematically

For current belief b, fixed future class law k_h(q), and deterministic
current readout z=r(h), define

    p(q) = sum_h b_h k_h(q)
    w_z = sum_{r(h)=z} b_h
    p_z(q) = sum_{r(h)=z} b_h k_h(q) / w_z, for w_z>0
    R(p) = 1 - sum_q p(q)^2
    G_r = R(p) - sum_z w_z R(p_z)
        = sum_z w_z sum_q (p_z(q)-p(q))^2 >= 0.

No factor 1/2 is included. Absent sparse atoms are exact zero on the SAME
complete alphabet. Zero-mass cells are omitted before division.

Every positive parent in baseline→N→NMT→H retains its child masses,
current-posterior mixture and full future-law mixture. Conditional risk
drops equal their weighted squared-law differences. Zero gain holds iff
all positive child future laws equal their parent law; differing current
beliefs or class IDs alone do not establish predictive usefulness.
Adjacent gains telescope. All-class nesting includes zero-posterior classes.

Full H has residual risk sum_h b_h R(k_h). This remains positive in 402
histories, because knowing the current class does not reveal fresh K3
randomness. H is an information oracle within this menu and model, not an
assumed available physical sensor or a bound on arbitrary interventions.

Case aggregation averages already-conditioned history risks by their
likelihoods. It does not compute the risk of the averaged prediction, which
would discard which history was received. U's complete unconditional
future law and unconditional current posterior remain unchanged.

## Access, authentication and inventory

The public API receives only class-local deletion rows, the supplied label
table, one fixed rational K3 pair, current H posteriors and case history
weights. It receives no raw orders, feature keys, full profiles, U history
paths, K1/K2, initial prior or artifact paths. Structural acceptance does not
authenticate a physical record source.

U's raw/model/history outputs are declared producer dependencies. The raw
audit independently rebuilds all 4,447 observations' H memberships, local
rows and labels, and recomputes complete U filtering evidence before
accepting any of the 482 V beliefs. All 8,894 raw-member K3 rows across the
two distinct rates agree with the reconstructed class laws.

| Retained/checked object | Count |
| --- | ---: |
| Raw observations / H classes | 4,447 / 416 |
| Local deletion entries / reconstructed class-profile atoms | 1,576 / 8,231 |
| Input current-posterior atoms | 1,026 |
| Positive readout cells N / NMT / H | 482 / 492 / 1,026 |
| Readout future-law atoms N / NMT / H | 1,936 / 2,030 / 4,608 |
| Raw positive K3 subset atoms checked | 336,776 |
| Public analyze calls / malformed calls rejected by runner | 12 / 14 |

The broader U public API controls and prior T/P/R/Q gates are not replayed.
No source/alias universe or mutable RET/core code is imported. The identical
counts of 34 H-strict histories here and 34 MAP prediction differences in U
do not establish a general equivalence between oracle value and MAP error.

## Verification and immutable evidence

The create-only [results.json](results.json) artifact is 3,493,736 bytes,
SHA256 `eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7`.
Its canonical suite is 3,488,673 bytes,
SHA256 `b888a2276f5d104e559417dd145e71c420fcab04e4f2e4761243e676a2821842`.
The canonical JSON list of the six complete analyses is 2,176,667 bytes,
SHA256 `96b8bed3e44454e498f7d7dbb85a9178d8d2ce6aba90a9b26d98933d219d5513`.

| Check | Outcome |
| --- | --- |
| Full normal tests | 140 passed in 56.89s |
| Full optimized tests | 140 passed in 56.62s |
| Exclusive capture | 21.465094415994827s |
| Fresh normal exact read-only replay | 22.1526063340134s, exact |
| Fresh optimized exact read-only replay | 22.24661691702204s, exact |
| Separate JSON-only postflight | 13,952,547 checks in 10.708941624994623s, passed |

The optimized suite has only pytest's expected assertion warning.
Each dedicated bounded normal/optimized subprocess performs 172 explicit
rejections without relying on Python assertions, including 33 checks that
cyclic, too-deep or explosively shared objects fail before serialization.
Benign aliases remain accepted. Tests also retain all-container ownership,
native/canonical rational guards, separate rate/belief bit limits, live
output/resource caps and constructor integrality/commuting-color controls.

The independent tests authenticate all 482 beliefs from raw paths and use
raw two-replica future-disagreement risks. Analytical controls distinguish
Bayes risk from misuse of the formula for a MAP forecast, unequal readout
weights, nonzero future randomness after full H, current versus future
readouts, and equal future laws despite different current classes.
Thirty-one output corruptions plus a same-cardinality wrong-parent map
permutation are rejected by the complete raw checker.

The separate stdlib JSON-only postflight imports no executor, runner or test.
It reads source files only for byte identities. Raw feature checks reconstruct
pair-union grades from complete count moments and Boolean-lattice inversion.
Per-vertex survival/deletion lifetimes across K1/K2/K3 authenticate U's
complete producer evidence through 32,768 assignments. Every V readout risk
is additionally checked using explicit replica-question disagreements:
54,360 question pairs across the six cases. All 8,894 raw-member K3 rows,
global maps, full per-parent posterior/future mixtures, aggregate laws,
risk identities, witnesses and counts agree exactly.

The public-call counts are checked as retained metadata, not claimed to
have been re-executed by this artifact-only audit. There are no source/alias,
T minimality or broader U API replays hidden inside that description.

Six source/protocol files and all 26 pinned prior artifacts matched the
pre-test ledger after tests, capture, both replays and postflight. Artifact
bytes remained unchanged after exclusive creation. All final Python runs
used isolation and explicit fresh external bytecode-cache prefixes.
No frozen source or artifact was modified after capture.
RESULTS.md and the roadmap remain outside the frozen ledger.

The protocol, menu, priors, transitions, target, caps and acceptance criteria
were fixed before V outcomes. Before outcomes, clarifications made the
weighted-scalar bound and history-weighted aggregate risk explicit.
Pre-capture runner lint/readability cleanup made an already-correct
variance multiplication grouping explicit; it changed no arithmetic.
Full tests, capture, replays and JSON-only postflight passed on their first
runs without outcome-driven source or criterion corrections.

## Boundary and proposed next gate

This is exact prior-, law-, readout- and loss-relative predictive information
on a supplied finite calculus. It adds no ontology commitment, physical
gravity/quantum/metric law, empirical calibration, sensor cost, adaptive
policy, RET integration or Lean verification.

Proposed QR-05W: imperfect classical readouts under fixed, explicit noise.
Keep current H2, the U beliefs, K3 and Q3 unchanged. On each full-model N
fiber, let A_N contain all distinct NMT labels, including labels absent
from a particular posterior. Use an unflagged N-preserving random-replacement
channel C_t(z|a)=(1-t)1[z=a]+t/|A_N| for z in A_N, with fixed levels
t=0,1/2,3/4,1. Two half-replacements compose to the 3/4 channel.

Retain the stochastic coupling and full conditional mixtures: noisy
channels overlap, unlike V's disjoint deterministic cells. Check expected
risk data processing, not pointwise monotonicity for every realized record.
Complete replacement is equivalent to N in predictive information, not
identical as a record distribution. Do not expose the replacement coin.

Noise must be fresh, non-disturbing and independent of K3 conditional on
current H2. Future-correlated randomness would be additional predictive
access, not harmless readout noise. This is a hypothetical channel study,
not fitted apparatus error or a license to discount conflicting observations.
No W outcomes have been computed.
