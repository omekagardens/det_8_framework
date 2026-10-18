# Activity, commitment and access: implemented semantic contract

13 September 2026. **SEMANTIC_CONTRACT_IMPLEMENTED; EXPERIMENTAL_API.**

Owner-authorized follow-through to the
[DET-wide audit](PRESENT_ACTIVITY_RECORD_FORMATION.md). This adopts a precise
distinction in DET's research descriptions and provides finite software
contracts. It does **not** establish a new physical law, a full QM derivation,
a first-outcome mechanism or an ontological observation. Status M is unchanged.

## 1. Object and three operations

Use the declared-scope state

\[
X=(C,\mathcal Z),\qquad C=(V,\prec,R_{\rm comm}).
\]

In QR-MAP the first candidate for \(\mathcal Z\) is the existing residual
pair-kernel \(\mathfrak D_C\), with its system type, operational interface
and relevant controller context. The software accepts other declared encoded
residual types for counterexamples; it does not assert their physical validity.

| Operation | Committed history | Residual state | Meaning |
| --- | --- | --- | --- |
| `evolve_residual` | Same snapshot object, same count | Supplied same-type transformation | No append in the declared scope |
| `commit_record` | Exactly one fresh maximal event appended | Supplied branch output; type may change | Already-selected positive-probability branch |
| `access_records` | Unchanged | Unchanged | Exact selected view, not a physical measurement interaction |

Record-time counts/orders commitments. It has not been established that
record growth exhausts present relational transformation. Composition order
of function calls is not a universal clock or derived duration. A fixed law
may act on changing sufficient state; “fixed law” does not mean “frozen state.”

Passive access is a mathematical projection. A physical reading interaction
may also disturb a residual system and produce a **new receipt event**. No
human observer is needed for commitment. No new accessible record does not
imply that no record formed elsewhere in the declared scope.

## 2. Implemented interface and invariants

The module is [record_process.py](../../det8/models/record_process.py), under
`det8.models`; it is not exported through the hardened core or RET SDK.

- `CommittedRecord`: integer event ID, full strict predecessor ideal `past`,
  `kind`, label, immutable payload and optional receipt source. IDs are labels,
  not times. Boolean IDs are rejected. Records use `outcome`, `null` or `receipt`.
- `CommittedSnapshot`: immutable record tuple in one valid append order.
  Duplicate IDs, unknown predecessors, self-precedence and non-downward-closed
  pasts are rejected. Prior events and relations cannot be edited by these APIs.
- `ResidualState`: nonempty declared `type_id` plus immutable scalar/tuple
  encoding. This is **not** a positivity, normalization or admissibility check.
- `ProcessState`: distinct committed and residual components.
- `AccessibleRecord` / `RecordView`: selected content and induced transitive
  order, without unselected predecessor metadata. A selected subset need not
  be past-closed. Unknown-ID order queries fail rather than report “unrelated.”

Payloads use exact built-in immutable scalar types, finite floats/complex
numbers, `Fraction`, or nested tuples. Mutable containers and custom subclasses
are rejected. This is public-API immutability, not a security boundary against
reflection or private-field tampering. It does not freeze physical memory
carriers: an immutable historical event and its presently mutable storage
are different objects. Legacy `NodeRecord` remains a mutable current-state
container; no migration or runtime behavior change is implied by its name.

The implementation checks selected branch probabilities in \((0,1]\), with
exact positive fractions supported. It rejects an impossible zero-weight
branch. It does not sample, prove probabilities, validate a complete instrument,
or certify normalization across branches. Callback side effects outside the
provided immutable state are not controlled by this experimental interface.

## 3. Silent, null, missing and delayed are not synonyms

1. A **silent residual operation** leaves the entire declared committed
   snapshot unchanged. Its lawful physical availability remains to be proved
   or explicitly assumed for each candidate process.
2. A **logged null/no-click outcome** is a record and increments the count,
   provided its selected branch has positive probability. It may be informative.
3. A **missing accessible record** may already exist in committed history.
   Projection models omission, not lack of formation or detector inefficiency.
4. A **receipt** is a fresh committed event referencing an earlier source in
   its causal past. Receipt order is not automatically formation order.

For \(a\prec b\prec c\), accessing only \(a,c\) retains \(a\prec c\).
Dropping cover edges with an omitted middle vertex would lose valid order.
The exact projection preserves supplied order; it does not prove that a
physical observer can recover missing order or a metric. A receipt can name
an inaccessible source without adding that source as an accessible vertex.

## 4. Small example: activity without commitment

```python
from det8.models.record_process import (
    CommittedRecord, CommittedSnapshot, ProcessState, ResidualState,
    access_records, commit_record, evolve_residual,
)

x = ProcessState(CommittedSnapshot(), ResidualState("classical-bit", 0))
y = evolve_residual(x, lambda z: ResidualState(z.type_id, 1 - z.value))
assert y.committed is x.committed   # count is still zero
z = commit_record(
    y, CommittedRecord(0, frozenset(), label="readout", payload=y.residual.value),
    y.residual, branch_probability=1,
)
view = access_records(z, [0])
assert view.count == 1 and view.records[0].payload == 1
```

This is a declared classical witness, not a DET-native physical law or evidence
selecting QM. A conditional exact phase/readout example is tested separately;
its supplied quantum representation and operation are not derived by this API.

## 5. Reconciled claims and untouched boundaries

- MODEL_CARD, ONTOLOGY, PHYSICS and record-kernel documentation now distinguish
  residual activity, committed history and access. This is semantic scope,
  not a new axiom selecting dynamics or an empirical conclusion.
- `time_evolution`'s fixed-input sampling is not a proof that all state freezes
  between commits. Its numerical propagator is unchanged.
- Historical T3 `record_formation` is labeled a **conditional classical
  stabilization bound**. It assumes a target, independent copies and reliability.
  Neither first-outcome formation nor pair-kernel decoherence follows from a
  majority-error bound. Its arithmetic is unchanged; its certificate is corrected.
- Historical `det_native_measurement` is labeled **classical record copying**.
  Its copying routines and names are retained. Comparison text no longer claims
  full quantum measurement equivalence or determinate values of every observable.
- Geometry use must separately specify record production, loss and delay.
  Count alone is not a calibrated volume/duration. Exact order projection is
  not a reconstruction of unknown geometry.

No RET, clocks, book or retired κ-gravity implementation is changed. The
owner-authorized mass/geometry/gravity research remains open subject to its
derivation and correspondence obligations. No metric is inserted here. The
countermodels to a full DET-derived quantum theory remain live; no principle
from the [selection report](../validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md)
is adopted by these contracts. No new QR-05 lettered gate is opened.

## 6. Verification and next research obligation

The contract tests cover immutable state, silent activity, same-type checks,
selected-branch validation, logged nulls, delayed receipts, omitted records,
transitive-order retention, exact conditional phase arithmetic and a classical
silent-bit control. Legacy scope tests cover unchanged elementary arithmetic
and the corrected claims. Optimized Python must retain all runtime validation.

Validation at implementation: **42 focused tests pass** normally and under
`-O` (30 interface tests, 12 stabilization/copying scope regressions). Ruff
passes on the three new Python files. The existing strict derivation (8),
chosen-law (9) and hypothesis-countermodel (5) checks also pass. These results
verify the scoped implementation and examples, not the unproved physical laws.
The 42 focused tests also pass in both modes on an export of the exact staged
tree, without the concurrent uncommitted core/RET changes.

After this implementation is committed and pushed, start the QR-MAP plan with
one precise question: **when is committed history sufficient for all declared
future record experiments?** Establish that factorization criterion, then
account for no-append transitions and never-commit probability in a conditional
first-commit law. Physical availability, operational axioms, growth and geometry
remain explicit later obligations—not consequences of passing interface tests.
