# QR-05BP results: interval-valued population-pair identification

9 September 2026 (Pacific/Honolulu). **Bounded gate complete.** The added
causal question, under δ∈[0,2], retains target identification for the two
prespecified narrow population boxes, but wider boxes restore target ambiguity. Exact
continuous nuisance intervals—not independently chosen query endpoints—are
retained throughout. Two independent implementations and a third test oracle
agree on the entire report. All 25 tests pass normally and optimized; both
full replays and the single alternate-runtime reference audit match.
The first capture passed without any post-first source correction.

This is robustness to stipulated population bounds within a supplied model.
It is not calibrated error bars, finite-record confidence, metric recovery,
experimental validation, quantum advantage or gravitational dynamics.

## What survives population uncertainty

The [prospective specification](README.md) and [fixed protocol](protocol.json)
keep the two geometries η=0,1, two scale labels s=1,4 and scalar sampling
density ρδ=1+δuv relative to proper volume, with δ∈[0,2]. The relative-volume
target is τ=1/4 for flat geometry and 17/80 for conformal geometry. The
same fresh point answers two nested causal-membership questions. Marks,
access, sampling, loss-free acquisition and iid premises remain supplied.

For each geometry and region, integration yields an affine mass
M_R(δ)=A_R+B_Rδ. The normalization M_Q is positive on the entire declared
domain. For a population box [L₁,U₁]×[L₂,U₂], compatibility is exactly

```text
M_I1 − L₁ M_Q ≥ 0,    U₁ M_Q − M_I1 ≥ 0,
M_I2 − L₂ M_Q ≥ 0,    U₂ M_Q − M_I2 ≥ 0,
δ within the independently supplied density bound.
```

These are four affine inequalities in one parameter. Their intersection
is empty or a closed interval, including a singleton. This is a continuous
set calculation, not a scan over selected δ values. The reference instead
clips each requested probability interval to its attainable range, then
inverts only reachable endpoints. Zero slopes and inverse poles are handled
explicitly. The independent oracle partitions at exact box-face roots and
checks the original ratios on endpoints and open cells.

The key controls below use the widest density premise, δ∈[0,2]. A box
half-width applies to both probabilities. F,C denotes the discrete target
set {17/80,1/4}; it does not include intermediate targets.

| Prespecified population constraint | Target answer | What it checks |
|---|---|---|
| Around (1/5,5/16), half-width 1/65536 | {1/4} | Flat target survives a nonzero tolerance |
| Around (1/5,2275/7296), half-width 1/65536 | {17/80} | Conformal target survives a nonzero tolerance |
| Either center above, half-width 1/1024 | F,C | Wider uncertainty loses the distinction |
| Around (17/80,21/64), half-width 1/65536 | F,C | The whole-point compensation remains |
| [0,1]² | F,C | Every nuisance value is retained |
| [1/4,1/4]×[19/64,21/64] | ∅ | Individually feasible queries can have no common δ |
| [3/16,17/80]×[21/64,3/8] | F,C | Closed singleton contact must not be discarded |
| [1/5,2/5]×[3/10,1/2] | F,C | A partly nonnested box can contain valid coupled laws |
| [3/4,1]×[0,1/4] | ∅ | A wholly nonnested box is valid syntax but infeasible |
| [1/16,1/16]×[0,1] | ∅ | Unreachable inverse-pole face is rejected safely |

For the narrow flat-centered box, the flat nuisance set is exactly
[1092/751,16388/11263]. For the narrow conformal-centered box, the conformal
set is [547839/1925473,2744325/9625883]. Each retains its scale copy. These
nonpoint sets identify a target without uniquely identifying density or
scale. The wider flat-centered box admits both flat
[84/59,52/35] and conformal [2655/10177,9/31]. The fixed radii demonstrate
survival and loss; they do not estimate a sharp robustness threshold or
establish the precision achievable by an instrument.

The inconsistent control makes the coupling issue explicit: its first
flat-query constraint admits only δ=0, while its second admits [1,2]. Both
individual sets are nonempty but their intersection is empty. Choosing a
different δ for each question would invent a compatible model. Conversely,
the touch control admits exactly flat δ=1 and conformal δ=0. The stored
intervals duplicate each singleton endpoint, and both endpoint-law rows
are retained.

## Complete inventory and preserved ambiguities

Twelve zero-width BO inputs and eleven new boxes, each under four external
density bounds, give 92 cases. All 48 zero-width projections exactly recover
the authenticated stored BO answers: same worlds, targets and statuses;
old nuisance singletons become [δ,δ]. This comparison does not rerun BO's
record enumeration or automatically recertify every historical source.

| Density premise | Target-identified | Target-ambiguous | Infeasible | Feasible labeled hypotheses |
|---|---:|---:|---:|---:|
| [0,0] | 5 | 2 | 16 | 18 |
| [0,1/2] | 9 | 2 | 12 | 26 |
| [0,1] | 6 | 6 | 11 | 36 |
| [0,2] | 8 | 8 | 7 | 48 |
| Total | 28 | 18 | 46 | 128 |

The 368 labeled hypotheses contain 240 empty sets, 70 singleton intervals
and 58 nonpoint intervals. All 69 adjacent-density-bound and 48 declared
box-inclusion checks preserve every labeled nuisance subset, world subset
and target subset, including empty cases. These counts are an inventory,
not an identification success rate or a comparison score against BO's
different input domain. Data IDs name constraints, not a supplied true
generator. A target answer remains conditional on the density premise.

Each retained feasible curve expresses both probabilities and the entire
same-point law using one shared δ:

```text
(p00,p01,p10,p11) = (1−q₂(δ), q₂(δ)−q₁(δ), 0, q₁(δ)).
```

Its two coordinate ranges are descriptive projections; their Cartesian
product is not generally an attainable paired-law set. Both scale comparisons retain
identical nuisance sets and normalized laws in every case while the actual
mass and volume coefficients scale by four. Scale remains unidentified.

The whole-point collision, flat δ=1 versus conformal δ=0, still has the
same normalized point density and q=(17/80,21/64), but target gap 3/80.
Both parameters are admitted in twelve case rows; all twelve are ambiguous.
The other six ambiguous rows do not admit this particular pair: full and
crossing under the two narrower density bounds, and the two wide centered
boxes under [0,2]. Thus admission of the collision implies ambiguity, but
ambiguity does not imply admission of that collision. Duplicate point IDs
and alternative bounds do not represent twelve distinct physical laws.

Strict positivity of the three allowed affine category masses over the
whole density domain gives an analytic support certificate: 81 possible
four-attempt words and 175 containing the impossible 10 symbol. No new
record enumeration was needed. Every allowed finite packet has support
throughout the family; population-set identification does not make four
records identify a geometry with certainty.

## Boundary and verification record

BP began from pushed BO commit
`766d3a80d44099635d2d7ac13cc1e4de5635c3be`. Specification and fixed inputs
preceded numerical execution. The mathematical implementations, third oracle,
public query and evidence-handling tests received independent static review.
Existing Ruff and normal/optimized syntax checks passed before freezing.

The public `study.identify` interface accepts exactly six fields declaring
population intervals and external density/uncertainty premises. All four
endpoints' native integer types and 31-bit caps are checked before any
gcd/Fraction arithmetic. Reduced, ordered rational intervals beyond the
fixture list are supported. Inputs/outputs are detached; the solver reads
no files, engines or old captures. It returns an empty result for a legal
box outside the model, rather than conflating model failure with malformed
input. The two prespecified non-fixture δ=1/3 queries pass. These finite
tests are not exhaustive verification of every machine input, and metadata
cannot authenticate uncertainty bounds or expose a disguised sample frequency.

The create-only source freeze was produced at approximately **22:05:32 UTC
on 9 September 2026**, before the first mathematical capture. Ten identities
bind six BP source/specification/test files, BO README/RESULTS/capture and
the BM utility driver. BO capture bytes are authenticated before parsing;
they are used only for the 48 historical point projections after the two
new native reports agree. BP reuses fresh authenticated BM codecs, bounded
I/O, comparison, exclusive-write and deadline helpers with isolated globals;
it owns its mathematical and publication wrappers. No historical executor,
estimator, publication wrapper or old test tree ran.

| Check | Observed outcome |
|---|---|
| Python 3.14.0 first capture | Complete primary/reference native agreement; 0.264894 s |
| Normal suite | 25 passed; 0.934 s |
| Optimized suite | 25 passed; 0.935 s |
| Normal complete replay | Exact match; 0.300481 s |
| Optimized complete replay | Exact match; 0.298898 s |
| Python 3.11.6 reference-only audit | Exactly one analysis; full native/canonical and 48 point-projection match; 0.259621 s |

Each suite caches one full analysis; focused mocks and temporary files test
lifecycle failures. Coverage includes source/protocol/prior-capture pinning,
ten-source caps, native type and complete-report mutations, fresh separate
engine inputs, immutable inputs, owned defaults, canonical JSON, exclusive
publication and final source/freeze/capture readbacks. The prior-deadline
test checks forwarding and restoration; the 120-second suite alarm raises
KeyboardInterrupt. All work stayed inside the fixed 30/120-second limits.
There was no numerical retry, post-first correction or adaptive cap increase.
No timing-sensitive RET rehearsal was observed at preflight.

- [Source freeze](source-freeze.json): 1,362 bytes; SHA-256
  `d90db2b07c0287922de242864771f380958f99ddec0af9a95988d752be6dd346`.
- [Complete capture](results.json): 412,301 bytes; SHA-256
  `1824c536c26127ab5e3b852cff73b54345a0b1441a199f0e54ed781e6d02a1c9`.
- Canonical mathematical report: 410,928 bytes; SHA-256
  `2a148820ddd78e74eefa993f94b9e2f609f0ddf6b115785a81ce2dd672520ecf`.

Publication is confined to nine BP artifacts and the owned roadmap. The
stored-evidence and scientific-prose reviews found no outstanding issue
after qualifying the widest-bound result and the singleton projection case.
Static documentation QA resolves all 86 local-link occurrences across the
three scoped Markdown files and checks heading/fence structure, whitespace
and conflict markers. All ten frozen identities and both retained artifacts
remain unchanged; these checks do not add numerical runs. The
231 pre-existing dirty status entries, including separate core/RET/application
work and the temporary model file, remain outside this change. No dependency,
physical device, external dataset, quantum-state or chart enumeration was
added. Reproduction commands and resource bounds are in the prospective
specification. These controls are not a hostile-environment certification.

## Next bounded question

Propose **QR-05BQ: finite-record uncertainty contract**, initially an
analytical/design-only gate. Prespecify a fixed iid paired-record quota,
failure budget, four tail allocations and outward rational rounding. Define
simultaneous population bounds from marginal binomial-tail inversion, then
feed one box into the shared-δ inverse. Dependence between questions within
a point must not be replaced with independence; a simultaneous bound needs
a joint coverage argument. Coverage must hold over the continuous probability
domain, not only the rounding grid or selected fixtures.

The next gate should state precisely when true-target set coverage transfers
from population coverage under the model and an independently justified
density bound. It must separate that unconditional guarantee from certainty
conditional on reporting only singleton answers. Selection, optional stopping,
loss, impossible-symbol handling and false model/density premises need
explicit boundaries. BQ is not started; no such confidence construction or
coverage guarantee is claimed by BP.

Calibrating apparatus and iid/density assumptions, general-density/metric
identification, dynamics and RET integration remain separate. BP does not
close QR-05, prove an ontology, derive QM/gravity or release applications.
Book work remains archival; Lean, clocks and later gravity couplings stay
deferred. See the [roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
