# QR-05F results: when observation history matters

6 September 2026. **Bounded two-stage observation investigation completed.**
All 133 tests pass normally and optimized. Ten complete exact analyses agree
between independently implemented observed-order and full-source-indicator
routes; the frozen artifact replays exactly. RET/core and dependencies are
unchanged. Remote publication remains deferred at the user's request.

## Main result

Observation history is useful relative to a declared question, not automatically
indispensable for every calculation. This study separates four guarantees:

1. A two-stage acquisition law composes into a final observation law.
2. A particular estimator can be computed from the retained information.
3. That estimator has the intended mean and variability.
4. A summary preserves a specified history-conditioned continuation prediction.

These guarantees are not interchangeable. A tiny provenance token can preserve
one estimator while losing a repeat-observation prediction. Conversely, losing
the intermediate record does not prevent a different unbiased final-sample
estimator from working. Both are explicit finite examples, not ontological claims.

The conditioning distinction is standard two-phase sampling mathematics;
the bounded chain/access diagnostics are the research contribution here.
[Beaumont--Haziza (2016), section 1](https://www150.statcan.gc.ca/n1/pub/12-001-x/2016002/article/14662/01-eng.htm).

## Mathematical objects and boundaries

Use the supplied Ferrers6, S3 and total-chain orders with six interior vertices
and fixed bottom/top probes; one Ferrers6 case also fixes an interior vertex.
First retain eligible vertices S, then T subset S. The observer receives induced
transitive orders and original retained IDs, with a known ID frame, fixed probes,
density and sampling design. Hidden source relations, source names, coordinates
and full targets are audit information, not estimator inputs.

For q=0,1,2,3, N_q counts internal q-vertex chains. Let a be the eligible
vertices of a particular chain. With P1(S) the first law and K(T|S) the second,
compare three constructions:

```text
Pf(T) = sum_S P1(S) K(T|S).
Hfinal = sum_observed_chains 1/pif(a),        when pif(a)>0.
Hseq   = sum_observed_chains 1/[pi1(a)pi2(a|S)], when both factors>0.
B(T)   = E[Hseq | T],                       only when Pf(T)>0.
```

The first two estimates explicitly omit unsupported terms; those terms and
their full targets remain in the evidence. The associated scalar coefficient
is alpha_q H_q, with alpha_q=(-1)^q/(2^(q+1)rho^q) and supplied rho=12.
These signed coefficients are not quantum channels or Born probabilities.
No new coupling to the earlier quantum payload is introduced.

## Identical final observations can require different sequential estimates

In the adaptive example, first-stage inclusion is independent one-half.
Second-stage inclusion is independent conditional on S, using rate 1/3 when
|S| is even and 2/3 when it is odd. Both stages are completely specified.

The same final observation T={1} occurs through these supported histories:

| Intermediate S | Joint probability of (S,T) | Sequential event-count estimate | Direct final estimate |
|---|---:|---:|---:|
| {1} | 1/96 | 3 | 4 |
| {1,2} | 1/288 | 6 | 4 |

Thus the sequential estimate is not a function of the final record alone.
Nevertheless, the direct final estimator is available and unbiased. Both have
full-source mean N=6 in this Ferrers6 case. This is an unavailable-estimator
witness, not a proof that final-only estimation is impossible.

Conditional averaging gives yet another answer at that same final observation:
B_N({1})=570/119, whereas Hfinal,N({1})=4. Its final-mask probability is
1309/23328. In these mask-only designs, B can be calculated from the final
observed chains and the known design without recovering the actual S.

The covariance identity holds exactly:

```text
Cov(Hseq) = Cov(B) + E[Cov(Hseq | T)].
```

This guarantees reduced covariance for the conditional average relative to the
sequential estimator. It does not compare every other estimator. For adaptive
Ferrers6, sequential and final variances are respectively 21 and 64/3 for N,
but 185 and 3464/25 for related-pair count R. Neither of those two estimators
uniformly dominates across the question vector. All conditional and overall
covariances are checked as exact positive-semidefinite matrices.

## A small record can preserve one task and fail another

For the adaptive case, retain the final record plus the known policy token
r(S). This is enough to compute each sequential chain weight, without retaining
all intermediate IDs. It is not enough to preserve the following conditional
question: what is the probability that vertex 1 appears in an independent repeat
of the second acquisition from the same intermediate S?

For T empty, S={1} and S={2} share token 2/3 and both have positive probability,
but their repeat probabilities are 2/3 and 0. These form the first token-level
repeat-prediction collision in the prescribed scan.

| Available record in the adaptive example | Sequential estimator computable? | Specified S-conditioned repeat probability preserved? |
|---|---|---|
| Final T only | No | No |
| Final T plus policy token | Yes | No |
| Final T plus full intermediate S | Yes | Yes |

The token preserves the sequential estimate in all ten tested cases. Full S
preserves both declared targets. These checks do not establish a minimal summary
or preservation of the full conditional observation law.

Averaging over hidden histories can give a legitimate reduced-information
forecast; it is a different task from retaining each original S-conditioned
prediction. Nor is an independent repeat from S a new order-growth law or a
third quantum process. It is one explicitly defined acquisition question.

## Positive final inclusion does not remove conditional support holes

A second control keeps all of S when |S| is even and discards it when odd.
Every source chain still has positive final inclusion. Direct final weighting
therefore estimates the full targets, but sequential omission does not:

| Source | Full targets / direct final means, q=0..3 | Sequential means |
|---|---|---|
| Ferrers6 | [1,6,6,0] | [1,3,3,0] |
| Chain6 | [1,6,15,20] | [1,3,15/2,10] |

For these nonempty eligible supports, only half the relevant intermediate
probability mass permits a second-stage exposure. Sequential means therefore
sum fractional path-coverage factors, not an integer supported-chain count.
Conditioning the sequential estimate back onto T preserves this bias; it does
not repair missing conditional support.

First-stage support is a separate boundary. When exactly two eligible vertices
are selected first, none of chain6's 20 three-internal-vertex chains can be
observed later. Their full target remains 20 while supported/coverage targets
are zero. Impossible transcript rows remain visible. Conditional moments given
impossible final observations are null; averages of the specified K at zero-P1
first masks are explicitly labeled kernel diagnostics, not conditioning on null
events.

## Positive composition and correlated-loss controls

Two independent half-retentions compose to independent quarter retention.
Sequential, final and naive-quarter estimators agree pointwise. Ferrers6 and S3
both have means(N,R)=(6,6), Var(N)=18 and Cov(N,R)=36, but Var(R)=138 and 126.
This continues QR-05E's separation of endpoint-kernel agreement from sampling
response. The always-retained interior vertex is weighted once, not four times.

If a common second-stage fair coin instead keeps or discards all survivors,
every vertex still has final marginal 1/4. Related vertices are not independent:
correct joint weighting gives mean R=6, while the naive-quarter correction gives
12. Correct sequential/final estimates coincide, with Var(N)=48, Cov(N,R)=60
and Var(R)=104 for Ferrers6. Empty-S keep/discard alternatives coalesce correctly
into one outcome with mass one, not two copies.

## Retained evidence

The [frozen protocol](README.md) and [artifact](results.json) retain all 6,804
transcripts: 3,534 positive and 3,270 zero joint-probability rows. There are 608
first rows and 608 final rows, 40 questions, 217 source-chain terms and 81,648
operational estimator values. Each four-method overall count/coefficient
covariance family has 640 entries; positive final observations additionally
retain 460 conditional covariance matrices. Maximum retained arithmetic
component size is 45 bits against the 4,096-bit guard. No Monte Carlo or data fit.

- **133 tests passed in 12.56 s normally and 12.60 s optimized:** 100 mathematical,
  interface and aggregate tests plus 33 capture lifecycle checks. Optimized pytest
  emitted its expected assertion-rewriting warning; executable validators use
  explicit exceptions. Ruff checks and formatting pass.
- Complete primary/reference outputs and whole-suite native-JSON round trips
  agree. Tests independently reconstruct laws, observed-chain estimates, omissions,
  fractional coverage, conditional defects, exact moments, covariance/PSD and
  the deterministic access-collision scan.
- Six source files and ten prior artifacts are byte-bound. Ten source comparisons,
  forty full-target questions and 416 first-law rows match pinned QR-05E evidence.
  The fixed-interior comparison conditions the old IID law on retaining vertex 3;
  unavailable chain6 first-law comparisons remain explicitly null.
- Create-only capture: 8,967,973 bytes; SHA-256
  `0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917`.
  Suite runtime 4.51910 s; exact read-only replay 4.60875 s. These are local suite
  timings, not application-performance claims. No frozen source correction was
  needed and no prior result was overwritten.
- A separate JSON-only audit imported no project code and independently checked
  every transcript and operational estimate, all support/coverage inventories,
  conditional and overall covariance/PSD, 60 access comparisons, 40 prior targets,
  416 prior observation rows and all seven aggregate control groups. Canonical
  artifact bytes and all six source/ten prior identities match; no discrepancy
  was found.

## Use for the calculus and proposed next gate

The result supports question-specific provenance contracts: record which
operation or prediction must remain computable, what acquisition context it
uses, and what support/uncertainty guarantee is intended. A successful scalar
estimate is not automatically a sufficient state for subsequent interaction.
Equally, a failed summary is not evidence that all history must be retained.

QR-05D's geometric ambiguities and the earlier quantum/record counterexamples
remain intact. These finite observation calculations do not derive geometry,
gravity, a continuum limit, or a new ontology. RET integration still has its own
SDK/calibration gates and is not part of this result.

**Proposed QR-05G: question-relative predictive compression.** Freeze a small
continuation-question family and compare full intermediate records with partial
summaries, seeking a verified sufficient partition or explicit collisions. Keep
estimator computability, conditional means and full predictive laws distinct;
do not claim a universal minimal history. This is a proposal to specify before
execution, not an already completed extension of QR-05F.
