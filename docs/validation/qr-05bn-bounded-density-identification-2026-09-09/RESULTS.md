# QR-05BN results: bounded sampling-density partial identification

9 September 2026 (Pacific/Honolulu). **Bounded gate complete.** Two independent
exact implementations and a third test oracle agree on all 36 bound/data
cases and 144 labeled hypothesis rows. All 25 tests pass in normal and
optimized Python; both complete replays and the single alternate-runtime
reference analysis match. The first capture passed without any subsequent
source, protocol, fixture or test correction.

The result is conditional partial identification of relative geometric
volume under an externally stipulated sampling-density bound. It separates
ambiguity caused by a limited observation channel from ambiguity that
survives the entire point law. It is not measured density calibration,
finite-shot certainty, reconstruction of arbitrary geometry or gravity.

## Exact compatible target sets

The [prospective specification](README.md) and [fixed protocol](protocol.json)
declare four geometry/scale labels, one continuous nuisance coefficient
δ∈[0,2], four closed external bounds and nine exact population probabilities.
The proper-volume target is τ=1/4 for flat geometry and τ=17/80 for the
conformal alternative. Each geometry has scale-one and scale-four labels;
both labels remain in every applicable compatibility set.

Here F means the exact singleton target set {1/4}, C means {17/80},
and F,C means the discrete set {17/80,1/4}, not its interval hull.
∅ means that no declared geometry/density combination fits the stipulated
population probability under that bound.

| Exact population q | δ∈[0,0] | δ∈[0,1/2] | δ∈[0,1] | δ∈[0,2] |
|---|---|---|---|---|
| 0 | ∅ | ∅ | ∅ | ∅ |
| 5/104 | ∅ | ∅ | ∅ | ∅ |
| 1/16 | ∅ | ∅ | ∅ | ∅ |
| 173/1136 | ∅ | ∅ | ∅ | C |
| 3/16 | ∅ | ∅ | C | F,C |
| 1/5 | ∅ | C | C | F,C |
| 17/80 | C | C | F,C | F,C |
| 1/4 | F | F | F | F |
| 1 | ∅ | ∅ | ∅ | ∅ |

Thus 10 cases identify one target, four are target-ambiguous, and 22 are
model-infeasible. Across the 144 hypothesis rows, 36 are feasible and 108
are rejected. Identification of one target does not identify the metric
scale: the two scale labels always remain paired.

Both routes certify the exact affine-mass ratio

```text
qη(δ) = [144+9η+(9+η)δ] / [576+144η+(144+64η)δ]
       = (a+bδ)/(c+dδ),
bc−ad = −432(η²+20η+36) < 0,
δ = (a−cq)/(dq−b), when dq−b ≠ 0.
```

The denominator of q is positive on the entire domain. Strict decrease
makes the endpoint range a necessary and sufficient feasibility certificate
for each closed bound, including the singleton uniform bound. Every
feasible inverse is substituted back into its own integrated mass ratio.
No search grid or optimization tolerance approximates the continuous δ set.

The two inverse poles are explicitly guarded: q=1/16 for flat geometry
and q=5/104 for conformal geometry give a zero inverse divisor and a nonzero
right-hand side. They do not produce a division or an all-δ solution.
Other rejected candidates remain visible as algebraic values, but no
admitted mass or normalized point law is assigned to them. The δ=2
endpoints are included under the widest bound and excluded by narrower
bounds. All 27 adjacent-bound checks preserve subset inclusion for labels
and targets and preserve the exact δ of each surviving hypothesis.

For example, q=1/5 admits conformal δ=45/158 under the half bound, but
admits flat δ=16/11 as well under the two bound. Tightening the bound can
therefore identify the target **if the tighter bound is independently
justified**. It does not learn that acquisition premise from the same
ambiguous observations. An empty set diagnoses inconsistency among the
declared data and assumptions, not which apparatus component is at fault
or that physical geometry itself has been refuted.

## Two different information obstructions

The normalized sampling polynomial is proportional to
1+(η+δ)uv+ηδu²v². Its full point law is equal precisely when both η+δ and
ηδ are equal; the metric scale cancels. Full point-law classes are retained
separately inside every feasible case.

| Prespecified pair under δ∈[0,2] | Flat δ | Conformal δ | Same membership law? | Same whole point law? |
|---|---|---|---|---|
| q=17/80 | 1 | 0 | Yes | Yes |
| q=1/5 | 16/11 | 45/158 | Yes | No |

Each pair has geometric-target difference 3/80. The first retains BM's
geometry/density factorization obstruction: even observing complete points,
or applying any common observation channel to those points, cannot
distinguish the pair under these sampling premises. More iid records do
not change equality of population laws.

The second pair is different. The current membership question discards
information that exists in the point law: only the conformal member has
a nonzero u²v² coefficient. A specified richer channel might recover that
distinction. BN does not assume that an arbitrary added question will do
so; the next gate must test its particular channel.

Both scale controls preserve all nuisance sets, targets and normalized
point laws while multiplying absolute proper volumes by four. Neither
density bounds nor fixed-quota normalized observations reveal absolute
volume in this family.

### Population data are not a finite record

All 144 ordered rows of the nine stipulated four-bit laws are retained,
including the 15 zero-probability words at each of q=0 and q=1. Those two
data laws are valid Bernoulli laws but are outside the geometric model.
They are not extra admitted worlds or acquired observations.

Separately, all 64 finite-word support rows retain both geometric targets
under every bound. Every admitted q range lies strictly inside (0,1), so
every four-bit word has positive probability for every admissible geometry
and δ. In particular, observing 0000 does not imply the exact population
q=0. The table above must not be queried with a four-shot frequency merely
because it has the same rational form as a registered population input.
This support statement does not preclude future statistical inference; no
confidence procedure is constructed here.

## Verification and access boundaries

The primary route integrates monomials and intersects the exact algebraic
inverse with the closed density bound. The independent reference integrates
direct functions by tensor Simpson, derives endpoint ranges first and
reconstructs the point polynomial by interpolation. The test oracle uses
endpoint mass formulas and forward substitution. Complete native reports
are compared with exact types before canonical encoding, not only by
their counts or digests.

The public population-query solver is checked against every registered
case. It accepts only the prescribed plain-type schema, exact rational
menu and external-bound declaration. Record/count/frequency-specific schemas
or extra fields, hidden world/state/coordinate fields and coercive bool/
float/subclass inputs are refused. Rational-menu admission precedes arithmetic
on supplied integers. Inputs and outputs are detached, and the solver neither reads
files nor invokes an engine, previous result or BM estimator. Valid inputs
with no compatible hypothesis return an empty result, not a syntax error.
Neither syntax nor a provenance tag can authenticate a caller's claim to
know a population probability or acquisition bound.

BN authenticates fresh bytes of BM's evidence utility driver before local
execution, reusing only exact codecs/comparison, bounded I/O, exclusive
writes and deadline utilities. Those aliases retain their isolated module
globals; BN owns its protocol, schemas, source inventory and publication
wrappers. No BM analysis, estimator, freeze, capture or replay wrapper was
called. No previous mathematical capture was used as an answer table.

Focused tests cover utility identity-before-execution, fresh isolated
loading, source and protocol pins, separate immutable engine inputs,
full-report type/content corruption, canonical tagged fractions,
duplicate-key JSON, regular-file caps, create-only preservation, final
source/freeze/capture readback and deadline restoration. Fault injections
use mocks and temporary files, not mutations to retained evidence.
These controls do not certify a hostile operating environment.

No new quantum-state or passive-chart enumeration was performed. The
independent quantum resource in BM supplies no new information under this
unchanged membership channel. BN neither revalidates all earlier quantum
calculations nor claims a quantum sensing advantage.

## Execution and provenance

The gate began from pushed BM commit
`91dc16c59eaca8eee810bba680d7f48656ea38e5`. The prospective specification
and fixed protocol preceded implementation and mathematical evaluation.
Static review by the implementation/test authors and cross-review preceded
the source freeze. Prefreeze hardening admitted the finite rational menu
before gcd arithmetic; test authoring also corrected a representative
mutation to select a feasible hypothesis rather than make a no-op change.
These were static authoring corrections, not responses to an observed
numerical failure. A late driver-hash difference was traced to formatting
of one condition; in-memory restoration reproduced the prior reviewed
bytes and both versions had the same AST, all before freezing.

The create-only freeze was produced at approximately **20:38:00 UTC on
9 September 2026**, before the first mathematical capture. Its nine
identities bind six BN specification/code/test files and BM's driver,
README and RESULTS. Prior documents authenticate context and utility reuse,
not automatic validation of BN's enlarged model.

| Check | Observed outcome |
|---|---|
| Python 3.14.0 first capture | Complete native primary/reference agreement; 0.099642 s |
| Normal test suite | 25 passed; 0.395 s |
| Optimized test suite | 25 passed; 0.395 s |
| Normal complete replay | Exact match; 0.063490 s |
| Optimized complete replay | Exact match; 0.063883 s |
| Python 3.11.6 reference-only audit | Exactly one analysis; full native and canonical agreement; 0.055818 s |

Each suite cached one complete BN analysis. Boundary/lifecycle tests used
small synthetic reports or mutations of retained reports, not extra
fixture scans. All runs stayed within the fixed 30-second analysis and
120-second suite deadlines. The suite deadline raises an interrupt rather
than a recoverable test error. No adaptive budget increase, numerical
retry or post-first-evaluation correction was needed. No timing-sensitive
RET rehearsal was observed at the preflight process check. No dependencies,
physical devices, external datasets or separate application code changed.

Retained byte identities:

- [Source freeze](source-freeze.json): 1,223 bytes; SHA-256
  `1362df4abcdc0b7436e4a033e79cbb751c426f569d413d63d07964030fab85c8`.
- [Complete capture](results.json): 79,142 bytes; SHA-256
  `22a59809c76c58d146becf5717ccec0d69b72abbaaa9f1751e216604b786f1ee`.
- Canonical mathematical report: 77,908 bytes; SHA-256
  `1095bee998f31ef3bcfaa1824fde0d71570936bfbb58e958baa555bf27e2ea6f`.

Full native and canonical data were compared before their hashes. Final
byte checks preserve all nine frozen source identities and both evidence
artifacts. Independent stored-evidence and interpretation reviews agree;
one post-run prose clarification makes explicit that the API cannot detect
a finite frequency disguised as a valid population input. This changes no
frozen source or mathematical result. Documentation QA covers three scoped
Markdown files: all 84 local-link occurrences resolve, heading/fence/math
delimiters pass, and no trailing whitespace or conflict markers occur.
Ruff passes for all four Python files. These are static/document checks,
not additional numerical runs.

The publication is scoped to the nine BN artifacts and the owned roadmap.
The 231 pre-existing dirty status entries, including separate core/RET/
application work and the temporary model file, remain outside this change.

## Next bounded question

Propose **QR-05BO: richer marked-causal queries under density uncertainty**.
Keep the BN geometry/density family and examine a second supplied mark
m₂=(3/4,1/2), giving I₂=(0,3/4)×(0,1/2) with I₁⊂I₂. Both membership
bits must concern the same sampled point; independent fresh points remain
iid across attempts, not across the two questions within an attempt.
For population q₁=ν(I₁), q₂=ν(I₂), the joint one-point law must be

```text
P(0,0)=1−q₂,  P(0,1)=q₂−q₁,  P(1,0)=0,  P(1,1)=q₁.
```

Freeze the exact channel, marks, finite data domain and comparison targets
before execution. Test whether the added question splits BN's q₁=1/5
membership-only collision while retaining the q₁=17/80 whole-point
collision and both scale obstructions. A possible algebraic certificate
is the rank of normalization plus the two interval integrals on
span{1,uv,u²v²}: recovering that point-law polynomial would still not
identify its geometry/density factorization. This is a proposed question,
not a BO calculation already performed or a claimed rank result.

Retain the structurally impossible 10 outcome and the old membership
marginal, distinguish exact population pairs from finite packets, and
preserve common attempt labels. Added marks and causal-comparator access
are new supplied premises, not inferred coordinates or clock readings.
No detector correction follows automatically from an impossible packet.
BO has not started.

BN does not close QR-05, validate DET ontology, derive QM or gravitational
dynamics, or release RET applications. Physical acquisition calibration,
general metrics and dynamical correspondence remain open. Book work stays
archival; Lean installation, clocks and later gravity couplings remain
separate. See the [roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
