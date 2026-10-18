# QR-04: adaptive quantum events with causal-past record access

September 5, 2026. Bounded exact research following QR-03. This protocol
defines the executable study; executed outcomes are reported in RESULTS.md.
No RET integration, empirical claim, ontology requirement or gate advancement.

## Question and mathematical contract

Can settings selected from declared available past records preserve complete
quantum-plus-record maps across all permitted schedules? Adopt standard finite
quantum instruments, not different physical laws. Each event e reads outcome
labels in a fixed set A_e and chooses s_e = g_e(r restricted to A_e). It writes
one new event-indexed triple (record_id, selected_setting, outcome).

For an admissible classical-quantum input sum_r tau_r tensor |r><r|, the lift is

`sum_(r,x) I[e,g_e(r|A_e),x](tau_r) tensor |r+(r_e,s_e,x)><r+(r_e,s_e,x)|`,

where r_e is event e's record_id (not necessarily its event_id).

Every outcome map is CP; each setting's summed instrument is trace preserving.
The controlled lift is linear on classical-quantum inputs. Do not normalize
or prune branches during composition. Past output settings remain recorded,
but this first policy language can read only past outcomes, not past settings.

For incomparable e,f, neither policy may read the other's output. For each
formal outcome assignment on the union of their read sets, select their two
settings, then compare every outcome-resolved two-event map in both orders on
the full operator basis. Preserve the selected-setting labels too. If every
such context commutes, their controlled lifts commute on arbitrary allowed
classical-quantum input blocks. Any two linear extensions of a finite order
are connected by adjacent incomparable swaps, proving schedule independence
under these premises. This is a conditional commuting-map argument, not a
Lorentz-covariance or spacetime derivation.

Two certificates must be reported separately:

1. **Source-reachable full-schedule equality:** all composite maps from the
   original quantum input agree. Every initial density matrix is covered for
   the fixed network; this is not a selected-input-state check.
2. **Universal pair-context equality:** every incomparable pair commutes on
   arbitrary quantum operators and every formal read context, including
   contexts that the preceding source cannot physically produce. This is a
   stronger sufficient certificate, not a necessary condition for 1.

An impossible past branch can hide a bad setting. A nonzero past operation
can also restrict the reachable quantum states enough to hide noncommutation
on arbitrary inputs. Keep both controls; never present formal impossible
contexts or matrix units as physical preparations.

## Frozen bounded wire schema

```text
{
  schema_version: "det8-qr04-problem-v1",
  qubits: 1 | 2,
  events: [{
    event_id: id,
    record_id: id,
    support: [qubit_index, ...],
    available_records: [record_id, ...],
    read_records: [record_id, ...],
    settings: [{setting: id, outcomes: [{label: id, kraus: [matrix, ...]}]}],
    policy: [{when: [[record_id, outcome_label], ...], setting: id}]
  }],
  precedence: [[earlier_event_id, later_event_id], ...]
}
```

- One/two qubits; one to four events; at most 24 schedules. A zero-event
  problem is excluded here; a single schedule is a valid vacuous control.
- One/two settings per event, one/two outcomes per setting, one/two Kraus
  operators per outcome. Each setting has the same outcome-label set and
  declared support for that event. Setting order and outcome order are not
  semantic; labels are. Unused settings are permitted but still validated.
- Unique event IDs and unique record IDs, separate namespaces. Exactly one
  writer per record; never overwrite an old slot. Supports are entrywise
  checked as local operator tensor spectator identity, not merely trusted.
- available_records is a sorted unique list of at most three known record IDs,
  each written by a strict ancestor in the transitive event order. Availability
  is a declared apparatus premise, not proof of communication in a laboratory.
- read_records is a sorted unique subset of available_records of length at
  most two. An ancestor can be unavailable; causal ancestry alone is not
  permission to read its record. Incomparable, future, self and unknown reads
  are rejected, even when a particular scheduler would already have run them.
- policy has exactly one row for every Cartesian assignment of outcomes to
  read_records (one to four rows), including unreachable/zero contexts.
  when is a sorted canonical list of pairs on exactly that read set. No missing,
  duplicate, extra, wildcard or fallback rows. Referenced settings must exist.
- No callbacks, scheduler index, execution-log access, hidden state, randomness,
  dynamic graph growth or implicit dependencies. Unknown fields are rejected.
  Thus access safety concerns this finite declarative language, not arbitrary
  Python programs, process isolation, or a security sandbox.
- Kraus matrices use QR-01's full-system Gaussian-rational wire format:
  each complex entry is [canonical_real_fraction, canonical_imag_fraction].
  Input components have a 64-bit bound; arithmetic has a 4096-bit guard.
  No floats, tolerances, sampling, dependency or lockfile changes.

## Output contract for independent implementations

`analyze(wire)` returns the same canonical JSON-compatible dictionary in two
independent paths. Record triples and pair-context pairs are lists on output.
Maps use QR-01 row-major superoperators, d^2 by d^2; every zero block survives.

```text
schedules: [{order: [event_id,...], maps: [{record: [[rid,s,x],...], superoperator: matrix}]}]
schedule_comparisons: [{left: order, right: order, equal: bool, difference: witness_or_null}]
schedule_equal: bool
nontrivial_schedule_comparison: bool
pairs: [{events: [e,f], universal_equal: bool, contexts: [{
  read_context: [[rid,x],...], selected_settings: [[event_id,s],...],
  forward: maps, reverse: maps, equal: bool, difference: witness_or_null
}]}]
universal_pair_equal: bool
adaptive_events: [event_id,...]
counts: {schedules, schedule_map_blocks, incomparable_pairs, pair_contexts,
         pair_map_blocks, matrix_unit_executions, zero_schedule_blocks}
```

Events, schedules, pairs, record triples and contexts are lexicographically
ordered by their labels. Context assignments follow sorted record IDs and
sorted outcome labels. schedule_comparisons compares the first order to every
other order. adaptive_events lists events whose policy actually selects more
than one distinct setting across formal contexts, even if some are unreachable.
Record objects in differences use lists, never tuples. A map-entry witness
has kind, record, output_index, input_index, left, right, delta; an inventory
witness has kind, left and right. Witness choice is the first lexicographic
record and row-major mismatch, as in QR-01.

pair maps show only the new e/f records; the specified prior context is held
fixed and unchanged. Their arbitrary input operator is the state immediately
before those operations, not necessarily reachable from the original source.
matrix_unit_executions counts d^2 * (number_of_schedules + 2 * pair_contexts)
for the direct executor; reference superoperator composition is a different
work route, not extra matrix-unit executions. No schedule or pair is sampled.

## Prespecified controls and evidence discipline

| Fixture | Full schedules | Universal pairs | Purpose |
|---|---|---|---|
| ordered_adaptive_reset | Equal, one schedule | Vacuous | Z outcome chooses I/X; both branches finish at zero |
| shared_selector_overlap | Equal | Equal | One coin chooses the same Z/X basis for two incomparable same-qubit measurements |
| independent_selectors_conflict | Different | Different | Separate coin parents choose bases independently; mixed Z/X contexts conflict |
| two_read_xor_policy | Equal | Equal | Two parent outcomes jointly select I/S; source order is immaterial |
| disjoint_adaptive_complex | Equal | Equal | Shared coin selects local Y/X or Z/Z measurements on separate qubits; Bell-state control |
| disjoint_adaptive_multikraus | Equal | Equal | One branch selects a grouped damping/reset channel; independent local Y instrument |
| source_range_restriction | Equal | Different | Measure-and-reset source leaves only P0; recorded Z and adaptive damping fail to commute on unreachable intermediate P1 |
| unreachable_policy_context | Equal | Different | Identity/zero parent hides an I/S setting conflict with X in the impossible context |

Coins use rational Kraus amplitudes 3/5 and 4/5. Damping uses survival/jump
amplitudes (3/5,4/5) or their reversal. Settings are not fitted to data.
The shared-selector fixture gives both same-system measurements a consistent
common control; it does not make arbitrary overlapping operations independent.
The two source-only equalities distinguish impossible classical contexts from
nonzero branches with restricted reachable quantum states. Both are retained.
For the independent-selector conflict, input P0 and the record (A:Z0, B:X0,
C:coin0, D:coin1) give (72/625) P+ in order C,A,D,B but (36/625) P0 in
order C,D,B,A. This physical full-process witness is retained separately from
the explicitly unreachable intermediate P1 pair witnesses.

Twelve retained invalid fixtures cover unavailable/unknown/self/incomparable
records, missing/duplicate policy rows, unknown settings, hidden scheduler
fields, record overwrite, cyclic dependencies, changed setting outcome domains,
and a forbidden read inside an impossible branch. Additional focused tests
exercise the full parser boundaries, including unused invalid settings.

Reuse only SHA-pinned QR-01 exact arithmetic and the separate SHA-pinned
QR-01 reference arithmetic. New policy validation, branching and comparisons
are separately implemented. The runner checks full exact output equality,
retains fixture wires, all schedule/pair maps and mismatch witnesses, source
identities, prior artifact hashes, runtime, counts and retained bit growth.
Capture is create-only; fresh replay is read-only and rechecks source/prior
and result-byte identities. Integrity hashes do not authenticate experiments.

The source ledger names README.md, adaptive.py, reference_qr04.py, study.py,
test_qr04.py and the two QR-01 dependencies. RESULTS.md is a subsequent
interpretation outside the ledger. All additions stay in this directory.
RET sources, shared docs, dependencies and existing QR artifacts are untouched.
Coordinate short runs with RET; use Python -I with an external bytecode cache
and disable pytest's checkout cache. No long numerical work is authorized here.

From the checkout root, use a fresh external cache for each invocation:

```sh
qr04_cache=$(mktemp -d /tmp/det8-qr04-bytecode.XXXXXXXX)
.venv/bin/python -I -X pycache_prefix="$qr04_cache" -m pytest docs/validation/qr-04-adaptive-causal-records-2026-09-05/test_qr04.py -q -p no:cacheprovider
```

Capture runs the directory's study.py instead of pytest; replay adds --verify
after study.py. Use a new cache and Python -O for the independent optimized
test/replay invocation. Validation uses explicit exceptions, not assertions
that disappear under optimization. The input boundary is a bounded in-memory
research fixture, not a hardened streaming service or general quantum SDK.

## Boundaries

This study tests fixed finite models under adopted QM, not all adaptive
processes, a quantum RET adapter, physical spacelike locality, ontology,
geometry, clock effects or gravity. Observable compatibility remains a separate
apparatus-specific comparison. Neither noise nor a missing dependency edge
can be used as an automatic excuse for a disagreement. A useful result is a
precise access/composition diagnostic, not an asserted application benefit.
