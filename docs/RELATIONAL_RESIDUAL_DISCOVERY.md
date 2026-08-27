# Relational Residual Discovery

**Status:** Implemented synthetic discovery protocol. The reported relations
are computational findings inside declared finite workloads, not resolutions
of the Riemann hypothesis or Collatz conjecture.

**Governance rule:**

\[
\boxed{\text{RG2: Model generation follows replicated predictive failure.}}
\]

Run the combined experiment with:

```bash
python3 -m det8.models.relational_residual_discovery
python3 run_tests.py
```

## 1. What was added

`det8/models/relational_evidence.py` complements the Gaussian parameter-state
RET core with likelihood-agnostic predictive evidence. It implements:

- Gaussian and Student-t continuous evidence;
- binomial, beta-binomial, Poisson, and negative-binomial count evidence;
- multinomial and Dirichlet-multinomial histogram evidence;
- recursively immutable evidence records with verified canonical payload
  digests and overlap-protected ledgers;
- a required broad `M_bottom` model-inadequacy branch;
- prequential log scores and question-conditioned action ranking; and
- common-random-number scheduling with order-independent random streams and
  Monte Carlo uncertainty estimates.

A joint likelihood occupies one ledger record listing each atomic source
once. A `joint` flag cannot waive source-overlap protection or cause an
already-assimilated likelihood to be multiplied in again. Exact-zero model
weights also remain zero on later updates.

An evidence posterior is conditional support among declared predictive
families. It is not a probability that a theorem or ontology is true.

`det8/models/relational_discovery_governance.py` turns that boundary into an
ordered decision ladder. Exact independently checked certificates are handled
separately. Statistical candidates must otherwise pass source-disjointness,
historical-freshness, open-model, replication, untouched-prediction, and
diagnostic gates before they can enter `DISCOVERY_CANDIDATE`. Proof language
is blocked for every statistical state.

## 2. Riemann multiscale spectroscopy

The adapter reuses the previously admitted first 512 nontrivial zeta-zero
ordinates. It divides them into eight disjoint 64-root blocks. Blocks 1–6 are
used for sequential training; blocks 7–8 are withheld from this fit until
scoring. The seven gaps crossing block boundaries are excluded so no spacing
observation belongs to two blocks.

This is a within-run validation split, not a historically fresh holdout. The
earlier validated-extension experiment summarized a 24-zero window beginning
at zero 489, which overlaps block 8. Its posterior is not consumed by this
multiscale fit, so there is no direct parameter leakage, but confirmation must
use newly admitted zeros beyond 512.

Each block records adjacent-gap ratios, unfolded spacing variance, small-gap
frequency, number variance at four scales, an approximate spectral-rigidity
statistic, pair-correlation summaries, and the maximum-gap tail. A
Dirichlet-multinomial spacing histogram compares deterministic synthetic
references: Poisson, beta-2 GUE, beta-3 finite-height, beta-5 over-rigid,
deleted-root, and jittered-root families. These are calibration references,
not rival mathematical theories.

### Result

| Check | Result |
|---|---:|
| Training winner | beta-3 finite-height reference |
| Training posterior for beta-3 | 0.9320 |
| Training `M_bottom` | \(1.04\times10^{-6}\) |
| Within-run validation winner | beta-2 GUE reference |
| Beta-3 validation gain over best alternative | -0.2404 log units |
| Mean adjacent-gap ratio | \(0.61731\pm0.00319\) between blocks |
| Mean unfolded-spacing variance | \(0.14062\pm0.00452\) between blocks |
| Clean synthetic-family recovery | 92.7% |
| Synthetic attack detection | 62.5% |

The finite-height training preference does not improve prediction on the two
withheld blocks. Four training-block increment wins are reported only as
exploratory prequential stability; because the reference was selected from
that sequence, they are not four independent confirmations. The scanner also
misses too many sparse deleted-root attacks to clear its declared 75%
diagnostic gate. The negative validation gain is decisive, so RG2 returns
`NO_HELDOUT_GAIN`; the run does not support a new Riemann-zero relation.

This negative result is useful: the spacing histogram is reasonably good at
recovering clean reference families but is not a sufficient anomaly detector
for sparse local omissions. A next Riemann run should freeze the family panel,
add local count-increment and independent root-quality diagnostics, calibrate
those diagnostics without the real holdout, and then score fresh disjoint
zero blocks.

## 3. Accelerated Collatz valuation tree

The Collatz adapter performs two deliberately separate tasks.

First, it constructs an exact arithmetic frontier for every positive start
through \(2^{20}=1{,}048{,}576\). Ascending dynamic-programming certificates,
four hash-chained \(2^{18}\) checkpoints, ordinary/accelerated toll identities,
and independent record-start audits guard the bounded computation.

Second, it asks a predictive workload question: after controlling for height
and the first accelerated odd jump, does a deeper residue/valuation prefix
improve prediction of total stopping time? Odd starts in
\([2^{18},2^{19})\) form the fitting band and odd starts in
\([2^{19},2^{20})\) form the locked model-selection band. The predeclared
panel contains height-only, first-jump, residue-tree, and valuation-tree
models at depths 3–10, scored with a robust Student-t likelihood.

### Exact bounded computation

| Check | Result |
|---|---:|
| Starts exactly computed to reach 1 | 1,048,576 of 1,048,576 |
| Longest total stopping time | 524 at 837,799 |
| Largest trajectory peak | 90,239,155,648 at 1,042,431 |
| Independent record/exception audits | 63 of 63 matched |
| Resume digest | `d2a2e67d66f947d742ea07084a587fefdea77ba24dcaf5e0f505577a61d8cfe7` |

RG2 reports this as `BOUNDED_EXACT_COMPUTATION` only for **positive integer
starts 1 through \(2^{20}\)**. The arithmetic census is reproducible and is
cross-checked by accelerated toll identities for all odd starts plus 63 direct
record/exception audits. Those checks are not a second full implementation or
an independently replayable per-start witness manifest, so the stricter
`EXACT_CERTIFICATE` label and proof language remain blocked. The result says
nothing about untested starts and is not a proof of the global Collatz
conjecture.

### Predictive relation result

| Model-selection-band check | Result |
|---|---:|
| Selected model | residue tree, depth 10 |
| Selected RMSE | 55.333 |
| First-jump-control RMSE | 57.580 |
| Height-only RMSE | 58.241 |
| Selected mean Student-t log score | -5.47762 |
| First-jump-control mean log score | -5.51141 |
| Height-only mean log score | -5.52191 |
| Raw mod-8 stopping-time contrast, 7 minus 5 | 24.773 train; 24.573 validation |
| Contrast after first-jump control | 6.104 train; 5.904 validation |
| Depth-10 gain over first-jump control | 0.03379 mean log-score units |
| \(2^{14}\)-start blocks favoring depth 10 over first-jump | 32 of 32 |

The controlled contrast has the same positive sign in all six exploratory
dyadic bands from \(2^{14}\) through \(2^{20}\), and every one of the 32
descriptive validation subblocks favors depth 10 over first-jump control.
This is real finite-workload stability, but the subblocks all participate in
the same model-selection exercise and therefore contribute zero
post-selection replications.

Three further issues prevent promotion. First, depth 10 is the ceiling of the
declared panel, so the run did not identify an optimal depth. Second, residue
modulo \(2^k\) deterministically encodes several future parity/valuation
decisions, making a model that controls only the first accelerated jump too
weak a scientific null. Third, the broad Student-t `M_bottom` is a sensitivity
reference whose scale was not calibrated into an inadequacy probability;
actual residual coverage, tail, height-drift, and block-heterogeneity checks
are also absent. RG2 therefore returns `MODEL_REVISION`, not
`NEEDS_REPLICATION` or `DISCOVERY_CANDIDATE`.

The next cycle must use only the already-consumed range through \(2^{20}\) to
choose and freeze a stronger multistep parity/valuation null, a non-boundary
depth panel, block-level scoring, robust-open sensitivity analysis, and
residual diagnostic gates. It must then evaluate the frozen comparison without
reselection on two predeclared fresh bands, for example
\([2^{20},2^{21})\) and \([2^{21},2^{22})\). A future band cannot be used both
to revise the model and to confirm it.

## 4. Ten-step shortcut follow-up through \(2^{22}\)

The next run implements the requested stronger mechanistic comparison in
`det8/models/examples/collatz_multistep_replication.py`. Define the shortcut
map

\[
S(x)=\begin{cases}
x/2,&x\text{ even},\\
(3x+1)/2,&x\text{ odd},
\end{cases}
\qquad
C_k=k+\sum_{j=0}^{k-1}\mathbf 1[S^j(n)\text{ is odd}].
\]

On every modeled prefix, which is audited not to encounter 1 early,

\[
\tau(n)=C_k+\tau(S^k(n)).
\]

The first \(k\) shortcut parities are in one-to-one correspondence with
\(n\bmod 2^k\). Their binary encodings are generally **not numerically equal**;
the code exhaustively verifies the 1,024-element bijection at \(k=10\) and
keys the saturated control by the actual residue.

The models answer a deliberately narrow workload question:

- the mechanistic baseline is the exact prefix toll plus an affine function of
  \(\log_2 S^{10}(n)\);
- the compressed candidate adds position-specific parity terms and adjacent
  parity interactions; and
- a shrunken lookup over \(n\bmod 2^{10}\) is retained as a saturated control,
  never as a discovery candidate.

This is a ten-shortcut-step start-residue prediction test. It is not yet a
fixed-number-of-accelerated-odd-jumps valuation model, and its baseline does
not match endpoint residue/valuation at the same resolution. Consequently, a
positive result could not be interpreted as dynamical “memory.” The observed
negative result does not need that stronger interpretation: the candidate
already loses to the simpler exact-toll/terminal-height baseline.

### Frozen geometry and consumed-data result

| Role | Half-open start range | Odd observations | Use |
|---|---:|---:|---|
| Revision fit | \([2^{18},2^{19})\) | 131,072 | Fit candidate families |
| Consumed selection | \([2^{19},2^{20})\) | 262,144 | Historical gate only |
| Locked transport 1 | \([2^{20},2^{21})\) | 524,288 | Score without refit |
| Locked transport 2 | \([2^{21},2^{22})\) | 1,048,576 | Score without refit |

Depth 10 is design-fixed to revisit the earlier depth-10 residue claim. Depths
4, 6, 8, 10, 12, 14, and 16 are sensitivity checks, not a new selection
panel. Residual scales use two-direction blocked cross-fitting over the two
consumed ranges, followed by one final coefficient fit over
\([2^{18},2^{20})\). The immutable protocol binds the model parameters,
cross-fit scales, \(2^{14}\)-start block width, scoring gates, source-data
digest, and module hash.

| Consumed selection-band model | Mean Student-t log score | RMSE |
|---|---:|---:|
| Exact-toll/terminal-height baseline | -5.47559730 | 55.24367 |
| Compressed parity candidate | -5.47610924 | 55.24777 |
| Saturated residue control | -5.47733785 | 55.31046 |

The compressed candidate loses by \(-0.000511944\) mean log-score units and
the saturated control loses by \(-0.001740549\). The saturated control also
loses at every sensitivity depth from 4 through 16. The candidate therefore
fails before either higher-band score is considered; the state is
`NO_HISTORICAL_GAIN`.

### Higher-band transport checks

The bands are evaluated in 64 and 128 fixed score blocks. A whole band could
count at most once, and only after clearing a 0.02 mean-gain floor, a positive
two-HAC-standard-error lower bound, at least 75% positive blocks, positive
leave-one-block-out means, a 20% block-dominance cap, calibrated residual
diagnostics, historical freshness, and a calibrated open-model gate.

| Check | \([2^{20},2^{21})\) | \([2^{21},2^{22})\) |
|---|---:|---:|
| Candidate mean gain over baseline | 0.000053179 | 0.000073926 |
| Mean minus 2 HAC SE | 0.000042340 | 0.000056426 |
| Positive score blocks | 49/64 | 97/128 |
| Central 50% coverage | 35.63% | 35.39% |
| Central 80% coverage | 72.09% | 70.66% |
| Clears 0.02 gain floor | No | No |
| Residual diagnostics pass | No | No |
| Formal replication | No | No |

The positive directions are about 376 and 271 times smaller than the practical
gain floor. Both fail central-coverage calibration. No development-calibrated
\(M_\bot\) probability exists, so the open-model gate is explicitly false.
Also, although the ranges were predeclared and excluded from fitting, an
integration run accessed them before the final manifest was persisted. The
artifact therefore records them as locked transport evaluations rather than
historically fresh replications. The 192 internal blocks are stability units,
not 192 confirmations.

### Extended bounded arithmetic

| Check | Result |
|---|---:|
| Positive starts computed | 4,194,304 of 4,194,304 |
| Resource-limited or cycle cases | 0 |
| Longest total stopping time | 596 at 3,732,423 |
| Largest trajectory peak | 858,555,169,576 at 3,873,535 |
| Hash-chained checkpoints | 16 |
| Shortcut recurrence unresolved cases | 0 |
| Record/exception direct audits | 78 of 78 matched |
| Resume digest | `aa813caba5f6dc41918b1060448ab8bdca9c4066a92a780528fe0485f15b99e2` |

This is exact integer computation for starts 1 through \(2^{22}\), inclusive.
It is not an independently replayable formal certificate, says nothing about
untested starts, and is not a proof of the Collatz conjecture.

## 5. Consumed-only accelerated endpoint prequalification

The next, deliberately unlaunched cycle is implemented in
`det8/models/examples/collatz_accelerated_endpoint.py`. It replaces shortcut
parities with a fixed number of accelerated odd jumps. On a nonterminal
depth-\(d\) prefix,

\[
A(x)=\frac{3x+1}{2^{v_2(3x+1)}},
\qquad
\tau(n)=C_d+\tau(A^d(n)),
\]

with deterministic early-terminal prefixes separated from statistical rows.
The fixed design uses depth \(d=4\), endpoint-residue resolution \(K=8\), and
valuation cap \(L=8\). H0 removes the exact origin toll and models continuation
from endpoint height, a shrunken endpoint-residue effect, and a same-depth
endpoint valuation basis. H1 adds only the matched origin valuation basis as
new terms, while jointly refitting the shared endpoint coefficients and
residue effects. Thus the comparison asks whether origin valuations add
compressed predictive information beyond a strong endpoint control; it does
not test nonlocal memory or the Collatz conjecture.

### Consumed rolling result

All fitting, scoring, and sensitivity work remained within the already-consumed
frontier through \(2^{22}\). The fixed comparison produced:

| Consumed score range | Equal-block-weighted H1 minus H0 mean log-score gain | Diagnostics | Score gates |
|---|---:|---:|---:|
| \([2^{19},2^{20})\) | \(-0.0002973846\) | Pass | Fail |
| \([2^{20},2^{21})\) | \(-0.0000409709\) | Pass | Fail |
| \([2^{21},2^{22})\) | \(-0.00000415615\) | Pass | Fail |

Every diagnostic inequality passed, although these diagnostic gates were not
simulation-calibrated. Every rolling score gate failed regardless because the
fixed H1 did not improve H0. The paired sensitivity designs
\((d,K)=(2,6),(4,8),(6,10)\) were also all negative. Consequently
`candidate_prequalified` is false. This is a useful negative result for this
particular frozen feature family and finite scope; it is not evidence that all
accelerated-valuation relations are absent.

The accompanying odd-only exact census resolved every positive start from 1
through \(2^{22}\), inclusive:

| Exact consumed-frontier check | Result |
|---|---:|
| Starts reaching 1 | 4,194,304 of 4,194,304 |
| Resource-limited or verified-cycle cases | 0 |
| Maximum total stopping time | 596 at 3,732,423 |
| Direct stopping-time audits | All passed |
| Accelerated affine audits | All passed |

This exact result remains bounded arithmetic, not an independently replayable
formal certificate or a proof of universal convergence.

### Preserved future evidence and open-model limit

The planned bands \([2^{22},2^{23})\) and \([2^{23},2^{24})\) were not opened.
Because consumed prequalification failed, no launch manifest was persisted and
no start above \(2^{22}\) was accessed. Those bands therefore remain available
for a genuinely new protocol rather than being spent on a candidate that
already failed its historical gate.

The reported broad-tail Student-t sensitivity is **not** a calibrated robust
open model. It yields no \(M_\bot\) probability, does not satisfy the RG2 open-
model gate, and cannot authorize a formal replication or discovery state. No
post-\(2^{22}\) numerical result exists in this experiment.

## 6. Current conclusion

The new calculus succeeded mainly as a claim-control mechanism:

- the Riemann training preference failed within-run validation and was
  rejected;
- the Collatz residue-resolution pattern is descriptively stable, but its
  apparent gain disappears on consumed data once ten exact shortcut steps are
  included in the baseline; the later positive transport directions are tiny,
  miscalibrated, and contribute zero formal replications;
- the endpoint-matched accelerated successor also has negative gain on all
  three consumed rolling ranges, so it does not prequalify and its two planned
  future bands remain untouched; and
- the Collatz arithmetic census is an exact computation only over its
  explicitly bounded range through \(2^{22}\), not an independently replayable
  certificate.

That separation is the result. The simulator can now generate and rank novel
relations without silently converting an exploratory fit into a discovery or
a finite computation into a universal proof.
