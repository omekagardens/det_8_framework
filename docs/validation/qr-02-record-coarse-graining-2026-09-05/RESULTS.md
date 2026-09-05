# QR-02 result: safe forgetting depends on the future question

Completed September 5, 2026. **Exact finite research within standard quantum
instrument mathematics.** [Protocol](README.md) · [Exact evidence](results.json)
· [Previous QR-01 result](../qr-01-quantum-records-2026-09-05/RESULTS.md).

## Main finding

We now have an executable distinction between **a bad replacement**, **useful
record compression**, and **genuinely unrecoverable information**. They are not
the same failure mode.

QR-01 showed that records and remaining quantum states must be considered
together when comparing processes. QR-02 asks when a fine record can be merged
into a coarser record while preserving a specified later process. The answer
depends on the source instrument, the remaining quantum state, the permitted
replacement operation and the future outputs that must be preserved.

All ten selected fixtures agreed exactly with the independent reference.
Seven proposed replacements preserve the complete required future map for
their specified source; three do not. The seven include a no-merge control
and an unreachable-branch control, so **five are substantive successful
grouping/replacement examples**, not seven general compression demonstrations.

## What the examples distinguish

| Situation | Exact finding | Consequence |
|---|---|---|
| Future operation does not need the forgotten distinction | Grouping and future evolution agree on every input block | Safe for that declared future contract |
| Quantum state or fixed source probabilities allow an alternative future | Reset and averaged-channel replacements preserve the required map | Fine-record dependence alone does not prove loss |
| Identity is substituted for a controlled operation | It can fail although a different physical replacement succeeds | A failed candidate is not an impossibility proof |
| Same complete coarse state requires two different futures | No coarse-only operation can reproduce both | Genuine loss of information needed by that future |
| A unique inverse is linear but not positive | No physical quantum channel can implement that inverse | Algebraic invertibility is not physical recoverability |

These are useful distinctions for a DET event-and-record description. The
underlying mathematics is adopted QM and linear algebra; the demonstrated
contribution is the explicit, tested record/future contract and its diagnostic
examples, not a new physical effect or a uniquely DET theorem.

### A failed replacement that can be repaired

Measure Z, retain outcome 0 or 1, then apply identity for 0 and X for 1. This
fine-record-controlled process resets the state to `|0><0|`.

If we forget the outcome and simply do nothing, initial `|1>` ends at `|1>`,
which is wrong for the required process. But a complete reset-to-zero channel
can act on the remaining quantum state and reproduce the fine process for
**every initial density matrix**. That candidate was verified on the full
operator basis. Therefore the first failed candidate was not proof that the
record was indispensable.

A second source-dependent positive example uses a fixed quantum-independent
coin with weights 9/25 and 16/25 and future controls I and `S=diag(1,i)`.
Their corresponding channel mixture reproduces the grouped future exactly.
The fine branch contributions need not match individually: the retained
object is their sum, together with the remaining quantum state.

### A record that really is indispensable for the declared future

Now the source measures Z **and resets the quantum system to zero** before
the fine record is forgotten. Initial `|0>` and `|1>` both leave exactly the
same available coarse state, `|0><0|`, with the same coarse record probability.

Nevertheless, the original fine-record-controlled I/X future requires `|0>`
for the first input and `|1>` for the second. An operation given the same
available input cannot produce both different required outputs. This is an
explicit no-replacement witness, not merely rejection of identity. It assumes
the forgotten record and any other side information are genuinely unavailable.

### A mathematical inverse that is not a physical recovery

A random recorded phase error has coarse channel

`K(rho) = (9/25) rho + (16/25) Z rho Z`.

With its fine label, the phase error can be undone exactly. Without the label,
K is still linearly invertible: it preserves diagonal entries and multiplies
off-diagonal entries by `-7/25`. The unique inverse multiplies them by `-25/7`.

The study verifies both `K^-1 K = identity` and `K K^-1 = identity`. But
`K^-1(|+><+|)` has diagonal entries `1/2` and off-diagonal entries `-25/14`.
Its expectation in `|+>` is **`-9/7`**, so it is not positive.

Because K is invertible on the full operator space, a linear physical recovery
matching all source inputs would have to be this same inverse everywhere.
There is no different completely positive extension that can fix the problem.
This rules out physical coarse-only recovery for the stated task. The invalid
inverse is a documented algebraic negative control, not an accepted instrument.

### Forgetting a recorded alternative is not coherent recombination

Forgetting a Z outcome sums its two **maps**, producing dephasing. On `|+>`,
a later X+ probability is `1/2`. Incorrectly adding the two Kraus projectors
first produces identity and predicts probability `1` instead.

Likewise, a coarse record probability alone is not the quantum state: after
forgotten Z measurement, `|0>` and `|1>` give the same sole coarse-label
probability but different later Z probabilities. Both controls passed exactly.

## Scope and verification

The implemented model has one or two qubits, one source stage and one fixed
future stage. It is not the general adaptive graph program deferred to QR-04.
Each supplied instrument has at most two outcomes and two Kraus operators per
outcome; merging can retain four Kraus contributions as a sum of maps.

Two comparisons are reported separately: equality for arbitrary independently
variable classical-quantum input blocks, and equality only for outputs reachable
from the specified source. Four fixtures pass the first, seven the second.
Of the three that pass only the reachable test, two are substantive physical
replacements; the third is the deliberately unreachable zero-branch control.

Evidence and accounting:

- **70 tests passed** in ordinary Python (0.65 s), and **70 passed under
  optimized Python** (0.65 s). The optimized run emits Pytest's expected warning
  about assertions outside rewritten tests; implementation checks use explicit
  exceptions, including a separate assertion-free optimized subprocess control.
- **60 reference-bundle comparisons; 111 retained exact superoperator blocks.**
  The executor evaluated 52 initial matrix units through all reachable routes
  and 160 additional matrix units for individual unrestricted future maps.
  These are workload counts, not independent experiments.
- Eight direct-state route checks supplement the full-map comparisons, including
  a Bell-state case. Separate exact inverse/expectation calculations check the
  nonphysical recovery control. No random sampling or numerical tolerance is used.
- Both independent source reviews cleared the mathematics and runner. Review
  also tightened pinned-source loading so a cached module cannot impersonate
  the verified source merely by claiming the same file path.
- Source/prior drift, result replacement, suite disagreement and create-only
  refusal have focused artifact tests. Ruff and formatting checks passed.
- Capture completed in **0.424 s** and a fresh isolated, optimized replay in
  **0.414 s**, with identical retained results and source identities.
- An independent retained-artifact audit checked all seven source hashes,
  the unchanged QR-01 identity, 111 stored maps, nine mismatch witnesses and
  all 48 retained state blocks against their maps and traces. It independently
  verified the collision, two-sided inverse and `-9/7` expectation directly
  from the saved data, without importing or rerunning the executor.

Capture used CPython 3.11.6 on macOS arm64. RSS high-water sampled at suite end
was 41,779,200 bytes. The largest rational numerator/denominator in retained
case maps needed 5 bits; that excludes the separate inverse control and is not
peak intermediate growth. Runtime/RSS exclude later serialization/comparison
overhead and are not performance or deployment claims.

The artifact is 685,156 bytes. SHA-256:

```text
b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c
```

Seven protocol/source/test files are bound in its ledger, including the two
read-only QR-01 dependencies. The original QR-01 artifact hash is checked
before and after execution and remains unchanged. This subsequent results
note is outside the source ledger. Local hashes establish integrity, not
experimental provenance or external preregistration.

## Applicable value and next step

**For DET descriptions:** records become explicit mathematical resources.
Their relevance can be tested against future questions rather than assumed
from an ontology or reduced automatically to a scalar summary.

**For later RET or monitoring applications:** this suggests a disciplined
summary contract: specify the source model, retained state/evidence, available
side information and future prediction/decision family before deleting history.
A convenient summary can be adequate for one task and inadequate for another.
QR-02 demonstrates that distinction, not an application accuracy, storage or
decision-quality improvement. Integration still waits for RET's own hardening
and separate application calibration.

**For Track-B:** a record-to-order construction must explain which distinctions
survive grouping and which downstream relations they support. These finite
examples supply checks for such a future construction; they do not construct
a spacetime metric, establish Lorentz covariance or derive gravitational laws.

The next bounded milestone is **QR-03: predictive history summaries for an
explicit family of future questions**, with positive compression examples and
histories that a proposed summary incorrectly treats as equivalent. No universal
minimal state, universal scalar kappa, ontology proof or empirical compatibility
claim follows from this result.

All additions are confined to this research directory. RET, dependency locks,
shared roadmap/charter documents, QR-01 evidence and legacy physics modules
were not modified. RET timing coordination was maintained throughout.
