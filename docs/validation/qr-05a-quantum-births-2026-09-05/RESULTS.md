# QR-05A results: consistent quantum births, insufficient payload-only geometry

5 September 2026. **Bounded investigative gate completed.** The positive
constructions meet the declared finite consistency checks; the negative
constructions fail in the prespecified, distinct ways. QR-05 as a whole is
not closed. No metric, gravitational dynamics, physical locality, or empirical
agreement has been established by this study.

## Main result

A growing classical event order can carry outcome-recorded quantum operations
with exact birth-label independence in this fixed-qubit construction. However,
even its complete quantum payload map need not determine the retained order.

Take the three-event fork, with one minimal event preceding two others, and
the join, with two minimal events preceding one other. They are not isomorphic:
their numbers of minimal elements are one and two. For the weak-phase fixture
at p=2/5 with all three outcomes zero, both histories have the same map

`J(rho) = (12/125) D_0^3 rho D_0^3`, where `D_0 = diag(3/5,4/5)`.

Both orders have two links and one incomparable pair, and all past parities
are zero. Thus the equality follows analytically and is checked on all four
operator units by both implementations. It holds for every quantum input,
not just one chosen state. The branch probabilities are consequently identical
as well. The retained order records still distinguish the histories.

This is a concrete non-reconstruction result for a **payload-map-only** summary,
not a general impossibility theorem about geometry or quantum gravity. It makes
the next question precise: which additional order/record information must a
summary retain to answer a declared family of future questions?

## Prespecified fixture results

All eight fixtures pass growth normalization, instrument completeness, and
trace preservation of the summed birth map at every enumerated parent,
including source-impossible parent records. All eight complete analyses agree
exactly between the direct and independent reference implementations.

| Fixture | Unweighted diamonds | Weighted diamonds | Complete terminal birth relabeling | Zero terminal maps |
|---|---|---|---|---:|
| Weak phase, p=2/5 | Pass | Pass | Pass | 0 |
| Grouped dephasing, p=2/5 | Pass | Pass | Pass | 0 |
| Weak phase, p=0 | Pass | Pass | Pass | 48 |
| Weak phase, p=1 | Pass | Pass | Pass | 48 |
| Past-parity Z/X, p=2/5 | Fail | Fail | Fail | 34 |
| Past-parity Z/X, p=0 | Fail | Pass | Pass | 54 |
| Ambient-stage Z/X, p=2/5 | Fail | Fail | Fail | 0 |
| Weak phase, uniform-over-ideals growth | Pass | Fail | Fail | 0 |

Each terminal inventory contains 56 natural order/outcome histories. Settings
are retained too. Equality requires matching the transported setting record
as well as the complete quantum submap, including on zero branches. A setting
mismatch on an identically zero map is a failure of this stronger structural
record contract, not by itself an observable channel discrepancy.

The positive cases are examples within ordinary finite-dimensional quantum
instrument mathematics. They do not establish consistency for every growth
law or every adaptive quantum operation.

## What the failures teach us

**Past-local classical reads do not ensure quantum commutation.** With a
record-dependent Z/X setting, two incomparable births can act incompatibly on
the same qubit. For the one-edge order plus an isolated event, transport the
outcome record (1,0,0) between natural orders `[[],[0],[]]` and `[[],[],[0]]`.
Applied to `P_1`, the recorded branch outputs are `(9/250) P_0` and zero.
This is a nonzero submap and branch-probability discrepancy. There is no claim
that the shared qubit describes physically spacelike-separated operations.

**Zero growth weights can hide a universal intermediate conflict.** At p=0,
the same past-parity family passes weighted diamonds and complete terminal
comparisons, while failing unweighted diamonds on the full declared parent
domain. This separates source-reachable agreement from the stronger universal
contract; it does not make the restricted p=0 source dynamics inconsistent.

**Ambient birth count can become an artificial observable.** In the stage-based
Z/X fixture, swap the first two births of an antichain and transport the record
(0,1,0) to (1,0,0). Input `P_0` yields `(27/500) P_0` versus zero. Separately,
the all-zero antichain has an automorphism with the same map but a different
transported setting record: expected `[X,Z,Z]`, actual `[Z,X,Z]`. Comparing
maps alone, or grouping by the resulting decorated key before transporting
settings, would miss this second defect.

**Normalized classical growth need not be birth-label independent.** Uniform
choice among currently available ideals sums to one at each step, but the
two compared natural histories of the one-edge-plus-isolated order have weights 1/6
and 1/8. With weak measurements and all-zero outcomes, input `P_0` gives
`(243/31250) P_0` versus `(729/125000) P_0`. The quantum operations commute;
the defect is in the growth weights.

These are model-level counterexamples, not attributed to experimental noise,
setup faults, or unknown physics.

## Evidence and checks

- 117 tests passed normally (4.61 s) and under optimized Python (4.66 s).
  Optimized pytest emitted its expected warning about assertions outside
  rewritten test modules; executable validation uses explicit exceptions.
- Ruff formatting and checks passed before capture.
- Two independently enumerated and composed routes agree on eight full
  analyses: direct Kraus action on matrix units versus exact superoperators
  using separate complex arithmetic representations.
- 536 retained history maps across levels 0–3, including 448 terminal maps;
  all 184 zero terminal maps remain visible.
- 335 additional closed-form map checks across **all levels** of five
  diagonal-instrument fixtures. This includes the uniform-growth negative;
  it is not a count of positive terminal examples.
- 88 parent normalization rows, 72 diamond contexts, 288 outcome-pair
  comparisons, and 1,280 terminal relabelings, including 832 nonidentity ones.
- 32 terminal order/setting/outcome classes in each intrinsic-parity fixture;
  54 in the stage fixture. Each distinct labeled history contributes once.
  Grouping preserves the total map but does not certify future summary adequacy.
- 16 malformed fixture inputs are retained as rejected by both implementations;
  the test suite exercises additional validation and optimized-execution cases.
- Five analytical controls are retained, including the setting-only
  automorphism and the nonisomorphic fork/join collision.

The model is bounded to three births, one fixed qubit, two recorded outcomes,
and at most two Kraus operators per outcome. Inputs have a 64-bit rational
component limit; arithmetic has a 4,096-bit guard. The largest component found
by the retained rational-string scan was 35 bits. No random sampling or
floating-point tolerance was used for mathematical equality.

## Retained artifact and replay

[results.json](results.json) is a create-only 4,917,037-byte capture with SHA-256:

```text
e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479
```

It records eight source identities, four unchanged prior artifact identities,
complete fixture analyses, rejection cases, analytical controls, and runtime.
The source checkpoint is QR-04 commit
`1fac1352ffe14dbbd6227dd1806bd8f6432ba0e4`.

Capture used isolated Python 3.11.6 on macOS arm64 with a fresh external
bytecode cache. The exact suite took 4.076 s; its recorded process RSS high-water
mark was 55,296,000 bytes. These measurements exclude artifact serialization
and are not application-performance estimates. Fresh-cache optimized replay
took 4.028 s, matched the complete suite exactly, and left artifact bytes
unchanged. Capture/replay commands and source-ledger rules are in the
[protocol](README.md#running-and-replaying).

An independent JSON-only audit, importing neither implementation, verified the
artifact size/hash, all source and prior hashes, counts, growth-weight formulas,
rational map sums, transport flags, and the five analytical controls. The
interpretation above was also checked against the retained artifact.

## Consequence for Track-B and the next gate

The useful bridge is a testable relationship among quantum maps, classical
records, and event order. A description motivated by relational ontology can
be expressed in this calculus without requiring an ontological commitment.
The calculations constrain candidate descriptions; they do not choose an
ontology.

QR-05B should now define future question families before proposing a summary.
Start with payload-only questions, then add order/count questions and
order-sensitive continuations. Keep the fork/join collision as a negative
control. A summary acceptable for the first family may fail the others.
Retain class multiplicities and test direct versus repeated grouping explicitly.

The next gate remains independent of RET integration. Record-dependent growth,
new quantum subsystems, scale limits, manifold correspondence, metric recovery,
Lorentz symmetry, and gravitational dynamics remain later questions under the
[research plan](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
