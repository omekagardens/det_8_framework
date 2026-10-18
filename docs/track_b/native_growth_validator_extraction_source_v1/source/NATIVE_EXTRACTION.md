# RI134 native four-policy extraction

Source-only implementation of the four policy families selected by the RI132
root adjudication. This is a new caller version, not an edit to RI129 or RI132.
No caller/control was imported, compiled, AST-parsed, probed or executed. No
scientific body, fixture or native coefficient was evaluated. No active copy,
card, freeze, admission, runtime inventory, attempt or repository/Git change
was created by this contribution.

## Scope and interfaces

The complete RI132 root decision and root narrative, complete 111-line
independent review and all 1452 lines of RI129 `supervise.py` were read before
the implementation. The new caller has 1469 lines, 89283 bytes and SHA-256
`e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d`.
Its accepted predecessor is 88890 bytes /
`34707ca1bd6e245ca9ec469adeb4c3da8cf0ed303be945036708554073b39650`.

Exactly four pure, actual production functions are introduced:

| Function | Argument boundary | Return |
| --- | --- | --- |
| `validate_dependency_payload(value)` | Parsed dependency payload | New list containing the validated original entry objects |
| `validate_source_decision_payload(decision, index)` | Parsed source decision and existing observed identity index | `None` |
| `validate_source_review_payload(review, index)` | Parsed independent review and existing observed identity index | `None` |
| `validate_current_target_checks(review)` | Completed review's policy fields | `None` |

These functions perform no I/O, cache installation or accepted-global mutation.
They still consult the caller's fixed path constants. The two source policies
call the original `bind` and `current` functions with the existing production
index in the same order. Nothing eagerly constructs expected identity values
before an earlier key or scope guard. Their production domain is the already
authenticated JSON object supplied by the unchanged metadata reader, not an
arbitrary hostile Python object with overridden methods.

## Complete source correspondence

Literal source reconstruction, not subject execution, verifies that the entire
new caller equals the old caller plus precisely these four moves/call sites,
the opening docstring, fixed `E` directory and the dependency byte/hash pin.
`native_coverage.json` records the exact raw spans, hashes and reconstruction
result. The integrator's `SOURCE_CORRESPONDENCE.json` and
`NATIVE_CALLER_DELTA.patch` provide the separate author-side whole-source
reverse projection; neither author comparison is a nonauthor review.

| Moved body | RI129 lines | RI134 lines | Exact raw-body identity |
| --- | --- | --- | --- |
| Dependency payload | 374–402 | 360–388 | 1934 bytes; `a599831e5efc49bbed7605a2cf94dafd1667f4444d075961a97bd243e7477ecf` |
| Source decision | 779–793 | 767–781 | 1158 bytes; `6ba09d447d54d01928ac0960ef727439701472624d75960e2b068e52a27c209e` |
| Independent source review | 795–802 | 785–792 | 583 bytes; `6bb7f6f365433b62eea8f0907089bb6ba5f54024e9d1e3f587b921318b18003e` |
| Current-target checks | 1019–1027 | 876–884 | Old 677 bytes / `1b99440132ad84fd2f66b56698059ae0f7fa60a9ed73796d780294c176f03feb`; new 641 bytes / `787e2e2280538a3d3a5ed3b2fcdadc4d7db81a7b7aa3e01e2cda852774c8be6a` |

The first three bodies are byte-identical. Only the fourth loses exactly four
leading spaces on each of its nine lines. Its statements, key order, strict
integer test, literal 15/4/71 counts, booleans and exact first messages are
otherwise unchanged. The new dependency function's `return entries` exposes
the existing local list; production tuple conversion remains after the final
file-identity recheck, not inside the policy function.

Production calls are at lines 407, 813, 815 and 1044, respectively. Dependency
authentication remains: fixed identity pin → raw bytes/hash → strict JSON →
actual pure payload validator → final identity equality → tuple cache. Source
cards retain original/copy/runtime/history/dependency checks, authenticated
fixed reads, recursive closed-reference checking, decision policy, review read
and review policy, then the fixed RI128 decision. Current-target policy remains
inside the prior completed-mode review loop after genuine serial custody,
actual outer completion and review-scope checks, before review bindings and
complete output comparison. No earlier/later checks are skipped or reordered.

## Path, dependency and wire-schema changes

`E` is the new exclusive RI134 directory. The original RI128 scientific source
and five original input roles, old immutable history/runtime paths and all
limits remain unchanged. The new `SOURCE_DEPENDENCIES.json` is 624320 bytes /
`80fb2a5a5f5a318208c9c6389bb7b59646ca18002b32bec01c632d33904cea9a`
with 343 authored dependency roles. The temporary predecessor draft pin was
replaced before this source handoff; it is not an execution fallback.

All RI129 wire-schema labels are intentionally retained as compatible protocol
names. This does not inherit RI129 authority: literal new paths and six current
source identities must bind this new caller/contract/dependency packet. Old
cards at the RI129 path cannot act as current cards. Future root source review,
current runtime authentication, execution cards and qualification remain
separate. There is no permissive old/new schema alternative or test mode.

## Callable unexecuted controls

`native_policy_controls.py` supplies `CASES` and
`run_case(authenticated_caller, case_id)`, with no loader or CLI. It constructs
in-memory arguments only, calls the actual extracted function and requires
exact exception class, code, entire message and positive return semantics.
Preparation failures cannot be fabricated into policy outcomes because the
pure tests perform no caller preparation. A later dispatcher must authenticate
the complete exact sources and actual runtime before loading either module.

There are 77 source-defined cases: 25 dependency, 21 source-decision, 15
independent-review and 16 current-target cases. Four are positive, 71 are
isolated negative policy mutations, and two are explicitly combined
early-scope/empty-index order probes. Those two probes verify that a scope
failure remains earlier than any missing expected-identity lookup; they are
not presented as single-fault cases. No case has run.

Dependency cases cover shape/schema/status/scope, closure and entry shape,
role/path order and duplication, identity shape/types, alias/link rejection and
provenance types. Source cases include every one of six source-binding positions
and every one of four additional decision references, plus missing-index and
early-scope ordering. Current-target cases preserve exact keys and strict type
checks: wrong individual counts, booleans, an integer-valued float, missing or
extra fields, completion and inherited-qualification flags. A pure accepted
15/4/71 dictionary proves only a metadata policy, never actual scientific checks.

Positive dependency return must be a new list of the same validated entry
objects; other positive policies must return exactly `None`. A local recursive
typed comparison checks the before/after built-in argument values and dict
order, distinguishing tuple/list and boolean/integer/float representations.
It does not rely on JSON, which would collapse D06's tuple into a list.
Return observations say pure policy only, whole-entry false,
no active record, no complete qualification and no scientific execution.

## All 52 declarations and remaining gaps

`native_coverage.json` preserves each original declaration tuple and order. It
distinguishes the RI132 source classification from RI134's present support:

- Five declarations now have new actual pure-policy control source: dependency
  order/duplicates, dependency aliases/links, source-card scope, source-card
  extra fields and current-target qualification credit.
- Sixteen retain only the applicability question for earlier **unexecuted**
  narrow direct sources, not copied controls or outcomes.
- Ten retain exact engine source reasoning only, not fault qualification.
- One earlier whole-entry specification remains tied to RI129, not silently
  retargeted to this new path or admitted.
- Twenty deeper declaration rows remain blocked by genuine raw-file,
  preparation, serial, filesystem or process prerequisites.

The independent-review payload cases are supplemental; a missing physical
review declaration is not relabeled as review-policy coverage. Applicability,
audit binding, eight-object observations, runtime/history parser extraction,
full-entry faults and actual process/custody verification are not implemented
here. Native/audit policy codes remain independent, not unified by this module.

Five scientific inputs, fourteen certificate sections, eight audit objects,
three candidate copies and witness → normal → optimized → audit remain fixed.
So do pre-Attempt refusal, repeated in-attempt checks, complete failure custody,
120-second active-child/512-MiB sampled-group/8-MiB scientific-body ceilings,
auxiliary metadata and arithmetic limits. Actual C2/C3 signs, simultaneous H30
feasibility and all physical claims remain unresolved. RET alone remains paused.
