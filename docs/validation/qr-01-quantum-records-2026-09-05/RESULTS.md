# QR-01 first result: records are part of quantum equivalence

Completed September 5, 2026 in the primary checkout. **Exact finite research,
not an empirical test.** [Protocol and implementation guide](README.md) ·
[Full exact artifact](results.json) ·
[Research charter](../../QUANTUM_RECORD_STRUCTURE_RESEARCH.md).

## Outcome

The first bounded implementation works: a DET-described network of quantum
events can retain ordinary quantum-instrument mathematics, outcome records,
complex phases, mixed states and entangled correlations. For five selected
nontrivial fixtures, all permitted schedules have exactly the same complete
quantum-plus-record map. A deliberately invalid independence claim is detected.

This is more than matching predictions for a few prepared states: equality is
checked on every matrix unit, so it extends by linearity to every input density
matrix for these **fixed instruments**. It is not an exhaustive check of all
instruments, graphs, Hilbert spaces or physical experiments.

The demonstrated usefulness is a correctness diagnostic: specifying which
records survive can expose an invalid equivalence that disappears when only
outcome-discarded dynamics, or even joint outcome probabilities, are compared.
No claim of a unique DET method, computational speedup or improved experiment
selection is established by this study.

## The revealing counterexample

Consider projective Z and X measurements on the same qubit. With no precedence
edge, the proposed graph allows both schedules. The verifier rejects their
full recorded-map equivalence. These operations must be ordered or explicitly
treated as conflicting in this model.

For input `|0>`, writing records in the fixed order **(Z, X)**:

| Record | Z then X | X then Z |
|---|---:|---:|
| `(0,+)` | 1/2 | 1/4 |
| `(0,-)` | 1/2 | 1/4 |
| `(1,+)` | 0 | 1/4 |
| `(1,-)` | 0 | 1/4 |

For input `I/2`, all four joint records instead have probability `1/4` in both
schedules, **but their quantum output states still differ**. In record `(0,+)`:

- Z then X leaves unnormalized state `|+><+| / 4`.
- X then Z leaves unnormalized state `|0><0| / 4`.

A subsequent quantum measurement can distinguish those branch states. In
contrast, discarding all records gives exactly the same composite map in both
orders: `rho -> trace(rho) I/2`. Thus neither commuting discarded channels nor
matching joint probabilities guarantees equality of the retained process.

This is ordinary QM expressed through an explicit record contract, not a new
physical effect. Artifact records are sorted by ID (therefore X before Z);
the explanatory table above deliberately displays Z before X. The
`branch_state_difference` witness compares entries of the output state itself;
its generic matrix-helper index fields are not another input-basis experiment.

## Positive cases and accounting

| Fixture | Main schedules | Incomparable pairs | Result |
|---|---:|---:|---|
| Local Z on A and B | 2 | 1 | Exact full-map equality; Bell correlations preserved |
| Local Y on A and Z on B | 2 | 1 | Exact equality with complex entries |
| Damping on A and X on B | 2 | 1 | Exact equality, including a multi-Kraus outcome |
| Four-event diamond | 2 | 1 | Exact equality through CNOT and parity boundaries |
| Four-event commuting antichain | 24 | 6 | Exact equality across every schedule |
| Ordered same-qubit Z/X | 1 | 0 | Valid control; no independence comparison |
| Unordered same-qubit Z/X | 2 | 1 | Expected counterexample retained |
| Explicit zero outcome | 1 | 0 | Both record blocks retained; no independence comparison |

Totals: **8 fixtures, 36 main schedules, 528 main matrix-unit executions**.
The 11 incomparable pairs add 22 two-event schedules and 328 matrix-unit
executions. Explanatory checks add three map schedules / 12 matrix units and
five direct-state executions. Remote-marginal checks add two map schedules /
32 matrix units. In total, 63 map computations (900 matrix-unit executions)
were compared against independently constructed reference superoperators.
The optimized replay repeated that work; those repetitions are not additional
distinct scientific cases.

For remote Z measurement and damping on B, summing all remote outcomes and
tracing out B leaves A unchanged on the complete two-qubit operator basis.
Bell-state conditional steering is also covered by the focused tests. This
separates conditional correlation from unconditional signalling under the
adopted local tensor-product model; it does not test laboratory separation.

## Verification and evidence integrity

- **81 focused tests passed** in ordinary Python (0.55 s), including complex
  arithmetic, multi-Kraus sums, zero branches, entanglement, label semantics,
  false support declarations, incomplete instruments and bounded schema errors.
- **81 passed under optimized Python** (0.54 s). Pytest emitted its expected
  warning about assertions outside rewritten test modules; executor, reference
  and study validation use explicit exceptions. A separate subprocess control
  checks invalid-instrument rejection under optimization without assertions.
- Ruff checks and formatting checks passed on the five-file research set.
- Two independent source reviews found no remaining mathematical/capture
  blocker. Pre-capture review corrected rational exponent parsing, aligned
  identifier grammars, and closed a replay-byte identity gap. Five artifact
  regressions cover replacement, source drift, suite mismatch, create-only
  refusal and the hash of the exact verified bytes.
- Exact capture completed in **4.874 s**. A fresh isolated, optimized process
  replayed it in **5.443 s**, with identical results and source identities.
- An independent retained-artifact audit verified all five source hashes,
  re-enumerated the schedules, inspected 125 stored superoperator blocks and
  checked every equality flag and mismatch witness against its actual entries.
  It also independently recovered the Bell probabilities, discarded Z/X
  channel equality, zero map and both remote-marginal identities from the
  retained maps, without calling the executor again.

Capture used CPython 3.11.6 on macOS arm64 and standard-library-only research
code. Process high-water RSS was 43,712,512 bytes. The largest retained main-map
rational numerator/denominator required 7 bits; this is not a measurement of
peak intermediate arithmetic. These timings and RSS describe this run, not a
benchmark or an application resource guarantee.

The exact artifact is 2,915,928 bytes. SHA-256:

```text
e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b
```

The artifact binds `README.md`, `exact.py`, `reference.py`, `study.py`, and
`test_qr01.py`. This results note is a subsequent interpretation, outside that
five-file source ledger. The artifact is create-only and replay checks source
and result-byte stability. It is local integrity evidence, not authenticated
experimental provenance or external preregistration. The fixtures were selected
and reviewed before capture, not randomly sampled from all quantum instruments.

## What this opens next

**QR-02: controlled forgetting of records.** Define a fixed classical mapping
from fine outcomes to coarse labels and sum the corresponding quantum maps.
Ask exactly which future questions this preserves. Two initial controls should
be a record-independent future instrument and a future operation conditioned
on a fine outcome that has been forgotten. Coarse record probabilities alone
must not silently replace the remaining quantum state; forgetting recorded
alternatives sums their maps, not their Kraus amplitudes.

**QR-03: useful history summaries.** Test whether two different histories can
be compressed to one retained description without changing a specified family
of future predictions. This may eventually inform RET, materials monitoring
and anomaly triage, but no storage saving or decision benefit is demonstrated
here. A stable, reviewed RET API and separate quantum/application validation
remain prerequisites for integration.

**Track-B:** schedule independence supplies one consistency check for an
event-and-record representation. It does not construct the event order, select
a geometry or derive gravity. The next bridge still needs an explicit
quantum-to-record-to-order mapping and refinement/coarse-graining tests, followed
by separately justified geometric and dynamical claims.

No new physical laws, measurements, noise explanations, Lorentz-covariance
claims, gate advancement or ontology proof follow from QR-01. No RET files,
dependencies, application gates, shared roadmap/charter files or legacy physics
modules were changed in this milestone. All additions remain in this isolated
research directory; RET's timing-sensitive work was coordinated separately.
