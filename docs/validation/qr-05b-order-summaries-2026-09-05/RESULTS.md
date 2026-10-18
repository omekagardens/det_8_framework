# QR-05B results: future predictions require order–record correlations

5 September 2026. **Bounded investigative gate completed.** Four complete
analyses agree between direct Kraus propagation and a separately implemented
diagonal-coefficient reference. Seventy tests pass normally and under optimized
Python; the retained capture replays exactly. This is a finite mathematical
summary contract, not evidence of a spacetime metric or gravitational dynamics.

Scope clarification: QR-05A checked at most three births; QR-05B adds one
specified continuation, not an exhaustive four-birth covariance certificate.
See the [protocol wording erratum](ERRATA.md), recorded after capture.

## Main finding

The same quantum payload map and the same basic order counts can conceal
different future predictions. Even the separate future marginals can agree
while their joint distribution differs. The missing information can be an
order–record correlation: **which record belongs at which place in the order**.

This sharpens QR-05A's fork/join result. A geometric or relational summary cannot
be judged only by whether it preserves a present total or a quantum map. We
must specify the future questions it must answer and test those questions.
The finding constrains this supplied model; it does not prove that a physical
spacetime is made of these orders or that these variables source gravity.

## The question hierarchy

For each retained three-event history h, J_h is its complete unnormalized
quantum map. We tested three cumulative question families:

- F0: retain J_h, including its history probability and residual payload.
- F1: also retain a nondisturbing probe of event count, link count,
  incomparable-pair count, and minimal/maximal-element counts.
- F2: also retain one genuine next birth under the existing percolation law,
  reporting precursor size m, selected past parity b, quantum outcome x,
  and residual quantum payload. Distinct ideals producing the same output
  are summed as CP maps.

Equality means equality of every outcome-resolved map for every initial qubit
state. It is stronger than QR-03's conditional-probability equivalence; these
are not claimed to be its coarsest conditional classes. A later common
payload measurement preserves the guarantee. Arbitrary hidden-history
interventions and many-step futures are not covered.

| Source fixture | F0 classes | F1 classes | F2 classes | Never-possible histories |
|---|---:|---:|---:|---:|
| Weak phase, p=2/5 | 26 | 29 | 32 | 0 |
| Grouped dephasing, p=2/5 | 26 | 29 | 32 | 0 |
| Weak phase, p=0 | 5 | 5 | 5 | 48 |
| Weak phase, p=1 | 8 | 8 | 8 | 48 |

Each fixture has 56 natural histories and 32 marked-order isomorphism classes.
Boundary operational class counts include **one class of all 48 zero maps**.
Those histories have no conditional predictions; their formal records are
still retained. The p=0 case has four live classes; p=1 has seven.

For both nonboundary fixtures, keeping only the source probability functional
fails F0 because it loses quantum coherence information. Keeping J_h suffices
for F0 but fails F1. Keeping J_h plus order counts suffices for F1 but fails
F2. Keeping the marked order up to isomorphism suffices for all three.

At this tiny nonboundary bound, the F2 partition is exactly the 32 marked-order
classes: it removes natural birth labels but provides no further compression
of marked orders. This is not a general reconstruction theorem. At p=0 and
p=1, the restricted source and continuation hide distinctions that matter at
p=2/5; the payload map suffices for their declared F2 source kernels.

## Two exact controls

### Same payload, different future growth

For the all-zero fork and join, the shared source map remains
`J(rho) = (12/125) D_0^3 rho D_0^3`, with D_0=diag(3/5,4/5).
After marginalizing the next quantum outcome, the precursor-size probabilities
for m=0,1,2,3 are:

- Fork: (27,18,60,20)/125.
- Join: (27,36,12,50)/125.

Thus a newborn whose past includes the entire parent has conditional
probability 4/25 for the fork and 2/5 for the join. These are consequences of
the previously adopted q(C,S), not an added physical law. They hold for every
initial state on which the histories occur.

### Same payload, counts, and separate marginals; different correlation

Use the same one-edge-plus-isolated order `[[],[],[0]]`, with outcome records
(0,0,1) and (0,1,0). Both histories have all settings weak0, classical weight
18/125, identical J_h, and counts (3,1,2,2,2). In the grouped-dephasing fixture,
the corresponding settings are dephase0 and the same equality holds within
that fixture.

The two histories have the same distribution of precursor size and the same
distribution of selected parity, with P(b=1)=2/5. Nevertheless,

`P(m=1,b=1 | first history) = 0`,

`P(m=1,b=1 | second history) = 18/125`.

Moving the recorded one from the descendant to the isolated event changes
which ideals read it. Tests check these probabilities against the actual
continuation maps, not just a separate scalar table. Even adding these two
matching marginal distributions to the shared current summary would not
resolve this pair's joint prediction.

The retained physical witnesses use full-rank input states and valid qubit
measurement effects. For example, input I/2 and the F2 output (m=1,b=0,x=0),
followed by effect P0, give joint probabilities 3779136/6103515625 versus
1889568/6103515625 for this pair. Each source history has probability
1296/78125. The all-state decision uses exact map equality; the witness bank
only makes a detected discrepancy operationally explicit within the model.

## Aggregation is not predictive sufficiency

Direct grouping by order counts agrees exactly with grouping first by marked
order and then by counts. Direct total summation also agrees with both staged
routes, for the entire F2 signature. Every distinct natural history contributes
once; no amplitudes are combined and no zero branches are dropped.

In contrast, averaging within each marked-order class and summing those class
averages gives total source probability on I/2 of:

- 44393/78125 for either p=2/5 fixture, instead of one.
- 337/625 at p=0, instead of one.
- One at p=1, where live class multiplicities are one and this mistake is hidden.

Correct pushforward uses the known fine-grained mixture. It does not show that
the aggregate payload alone determines a future transition law. The equal-
payload controls above are explicit obstructions to such a universal rule on
this declared domain. Likewise, finite associativity of grouping is not the
scale-consistency result required by QR-05C.

## Verification and development record

- 70 tests passed normally (4.41 s) and under optimized Python (4.39 s).
  The optimized run emitted pytest's expected warning about assertions
  outside rewritten test modules. Executable validators use exceptions.
- Complete direct/reference agreement for four fixtures; 224 source histories,
  3,584 outcome-resolved continuation blocks, and 96 zero source histories.
- 60 candidate/family checks: 33 valid and 27 invalid, with a physical first
  witness for every invalid check. The 11,954 retained conflict-pair entries
  include repetitions across candidates and families, not 11,954 unique pairs.
- 4,956 exact Choi-positivity checks on retained source, continuation, and
  aggregation maps. These include repeated map occurrences and exploit the
  special diagonal-superoperator form; no numerical positivity solver.
- 14 malformed input fixtures rejected by both implementations, including
  optimized-process boundary tests; lifecycle tests cover create-only capture,
  schema/canonical-envelope rejection, source/prior changes, symlinks, and
  byte-preserving replay. Ruff checks passed before capture.
- Maximum retained rational component size: 52 bits, below the 4,096-bit guard.
  No sampling, floating-point equality tolerance, RET imports, or new dependencies.

The initial development check mistakenly required the summed next-birth map
to equal J_h. Its first execution failed because ignoring a measurement's
outcome generally changes the quantum state. The corrected protocol checks
preservation of the trace functional, while retaining the changed quantum
map. A regression test requires nontrivial state change in every fixture.
This correction was recorded before capture; there is no overwritten result.

Independent design calculations supplied the nonboundary class ladder and
both analytical controls before the direct executor was run. The two executable
routes are independently implemented algorithms, but share the verified QR-05A
source artifact; agreement is not a fresh derivation of the prior source data
or a machine-checked proof in Lean.

## Artifact and next gate

[results.json](results.json) is a create-only 3,675,197-byte artifact with SHA-256:

```text
2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b
```

It binds seven source identities and five unchanged prior artifacts. Capture
used isolated Python 3.11.6 on macOS arm64 with a fresh external bytecode cache:
3.953 s for the suite and a 62,488,576-byte process RSS high-water mark.
These exclude serialization and are not application-performance claims.
Fresh optimized replay matched the complete suite in 3.962 s and left the
artifact bytes unchanged. See the [protocol](README.md#reproduction) to replay.

A subsequent JSON-only audit imported neither executor. It checked the artifact
size/hash, all seven source and five prior identities, every family partition
and candidate conflict list, all 4,956 retained Choi checks, and the next-birth
trace identities directly from the saved data. All checks passed.

QR-05C is next: define a bounded refinement/coarsening family and compare
growing then coarsening against predicting from the coarse description, with
measurement access and retained correlations specified on both routes.
Preserve the present collisions as negative controls. A summary that works
for one source layer and one-step question family must not be assumed closed
under growth or repeated coarse descriptions.

No physical metric, manifold correspondence, Lorentz symmetry, new clock
coupling, or Einstein dynamics is established here. The useful Track-B result
is a sharper criterion for which relational information a candidate description
must retain. See the [research plan](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
