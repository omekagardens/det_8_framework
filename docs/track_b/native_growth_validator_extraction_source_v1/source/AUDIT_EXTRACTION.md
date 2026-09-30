# RI134 — audit policy extraction and direct-control source

Author: `/root/ri132_audit_controls`. This is an unexecuted author contribution
for fresh independent review, not qualification, actual custody, admission or a
scientific result. RI129 and RI132 remain immutable.

## Scope implemented

The new `launch_audit.py` changes exactly four policy boundaries from the
accepted RI129 caller. There is no new applicability, binding, object,
filesystem, runtime, history, serial-custody or monitoring extraction.

| Real new function | Arguments and result | Original production position |
| --- | --- | --- |
| `validate_dependency_payload(value)` | Decoded metadata argument; returns the ordered entry list | After literal manifest identity and raw byte authentication and `strict_json`; before final identity recheck and tuple-cache installation. |
| `validate_source_decision_payload(decision, sources, known)` | Current decision and already-constructed expected identities/index; returns `None` | After unchanged runtime, source/copy, RI128, history/dependency checks and authenticated current decision read. |
| `validate_source_review_payload(review, sources)` | Current review and the same expected source set; returns `None` | After the source-decision policy and ordered reference checks, then the authenticated current review read. |
| `validate_current_target_checks(value)` | A completed-review argument; returns `None` | After its existing scope/provenance predicate, before ordered references and all-six-output binding. |

The original audit-specific codes and full messages are unchanged. In
particular dependency scope comparison still raises `identity`, malformed
dependency identities still use the original `configuration` guard, and the
15/4/71 shape and combined policy guards retain their distinct `prerequisite`
messages. A generic shared helper has not replaced these implementations.

The six-source `sources` dictionary is still constructed at the same point in
`verify_source_cards`, before the decision's authenticated metadata read. The
extraction does not precompute expected references before earlier predicates.
The source-decision helper keeps the exact ordered `require_ref` loop and its
lazy per-reference checks. Final `bind_refs` over both decision and review
stays at the original production location, outside both extracted functions.
Neither production nor a direct test may treat supplied argument identities as
physical observations or independent permission.

The dependency helper performs the original statements in their original
order and returns the existing local list. `dependency_prepare` still does:
fixed pin validation; file identity; fixed byte-count/hash comparison; complete
raw read and exact raw hash; `strict_json`; payload policy; final
`file_identity` equality; then `DEPENDENCY_ENTRIES = tuple(entries)`. No cache
is installed before that final physical identity check. The pure helper has
no reads, writes, imports, callback, test-mode switch or cache mutation.

## Exact adaptation and compatibility

The old source is 103287 bytes, SHA-256
`5263099d45d9ed021a80d65029da511ad9019d30892278b1b412cb1794465ae5`, at
`/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0/launch_audit.py`.

The new caller is 103969 bytes, SHA-256
`74f3ef59520a7d8d360a280bcf5d5389d0e3f6c456e8f02178fbc773c4e5d60b`.
Its fixed E directory is
`/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde`.
Besides the four extractions and their four call sites, only the opening
RI134 docstring label, E path and the new dependency byte-count/hash literals
are adapted. The dependency manifest is 624320 bytes, SHA-256
`80fb2a5a5f5a318208c9c6389bb7b59646ca18002b32bec01c632d33904cea9a`,
with 343 source-time administrative entries. It is not a current runtime
inventory, live card or permission.

RI129 wire schema strings, status labels and error messages intentionally
remain compatible protocol identifiers. They do not identify the executable:
the new absolute paths and six complete current-source identities must bind
RI134. An old RI129 source/custody card does not become a current card through
schema compatibility. Actual new cards, fixed copies, freezes, dispatch and
admission remain separately root-owned future work. This source-only packet
creates none of them.

## Literal correspondence evidence

The main author's `SOURCE_CORRESPONDENCE.json` and `AUDIT_CALLER_DELTA.patch`
record the exact full correspondence. No syntax parser or subject execution is
used. Removing the four new function spans, reinlining their old blocks and
undoing only the E/pin/opening-label adaptations recovers **all old bytes**.
The original supervision, full pre-Attempt check and repeated in-attempt
validation are therefore retained; the proof is not merely a few equal guards.

| Policy | Old block lines | New function lines | New call line | Old block SHA-256 |
| --- | --- | --- | ---: | --- |
| Dependency | 565–593 | 550–583 | 599 | `a599831e5efc49bbed7605a2cf94dafd1667f4444d075961a97bd243e7477ecf` |
| Source decision | 900–912 | 879–895 | 933 | `156ca6c4a01252977c14918fdd30c92eb402802a2cc7b74804f7309b3e7163ac` |
| Source review | 914–919 | 896–905 | 935 | `909292849382827349da122e10818293893aa5513a64a69df35040f2e7f730ed` |
| Current target checks | 1245–1253 | 1151–1163 | 1274 | `5a513728cad65a6144de68b1c3b1dbb586f4f3dab60d746a92e6510c666d3486` |

The policy-body comparison excludes each new one-line explanatory docstring,
the necessary dependency `return entries`, and an eight-space common dedent
for the previously nested current-target block. No predicate, operand,
message, local statement order or reference-loop order differs. The complete
function span hashes and full old/new identities are in the correspondence
artifact; the whole-byte reverse projection also rules out unrelated edits.

## Concrete controls, still unexecuted

`audit_policy_controls.py` exposes a closed `CASES` tuple and
`run_case(authenticated_caller, case_id)`. It has no caller loader, CLI,
subprocess dispatch or active evidence writer. A later separately reviewed
dispatcher must authenticate the complete new source and bootstrap runtime
before importing it. Existing RI132 dispatch source is pinned to RI129 and is
not silently reused for this new caller.

The 62 cases consist of four positive baselines and 58 isolated negative
mutations. Every argument is built in memory; no fixture has been instantiated
or executed during this sitting, and nothing is installed at a production
path. Synthetic identities carry inert bytes/hashes and are never described
as actual cards or evidence. Each test calls the **real extracted function**,
not a rewritten equivalent predicate or a sliced/evaluated source fragment.

| Cases | Family | Intended boundaries |
| --- | --- | --- |
| AD01–AD19 | Dependency payload | Positive two-entry list; root keys/schema/status/scope; empty/non-list closure; entry keys; role, duplicate and noncanonical path; identity shape/type; alias/link value; classification/access/provenance type. |
| AS01–AS17 | Current source decision | Positive six-source/four-reference argument; exact keys; scope/schema/status and strict false flags; source-set equality; missing closed reference; zero, null and individually mismatched ordered references. |
| AR01–AR09 | Independent source review | Positive policy; schema/status/blockers; strict false science/execution flags; expected source-set equality. |
| AT01–AT17 | Exact current-target policy | Positive strict integer 15/4/71; missing/null/extra/incomplete counts; boolean/string/float count types; individually wrong counts; missing/false/nonboolean completed or inherited flags. |

Earlier predicates are satisfied by each positive baseline before its one
semantic mutation. For example AD09 gives the second entry a duplicate path
and a matching identity, leaving its role correct; the order guard is therefore
first. AS14 preserves the first independent-review reference and changes only
the next RI128 reference, so the expected mismatch cannot be an earlier
reference error. A nonempty symlink value in AD14 is structurally valid before
the dependency no-alias policy rejects it; no real link is created.

The expected class is exactly the supplied caller's `Stop`, with exact code
and entire message. Positive dependency return must be exactly an ordered
list equal to the supplied entries; the other positive returns must be
`None`. The runner also rejects changes visible to canonical JSON comparison
of its supplied input arguments; this comparison does not claim to preserve
dictionary insertion order or arbitrary Python object identity. An
unexpected early exception or setup error is not a matching control. Returned
observations explicitly deny whole-entry qualification, actual target-check
execution, real-history status of arguments and complete caller qualification.

These tests cover policies over their production metadata domain. They do not
add an outer object-shape guard where the original production had already
established a dictionary, widen its input domain, or promise exhaustive
coverage of every possible Python object or resource failure.

## All 69 declarations and remaining gaps

`audit_coverage.json` preserves the complete original ordered 69 declaration
tuples and records both prior RI132 classification and current support. The
source declaration block itself remains byte-identical in the new caller.

Six prior blocked rows now have concrete extracted-policy controls:
dependency order/duplicates; dependency alias/link values; source extra keys;
source promotion; incomplete source review; and old/current-target
qualification credit. They are **direct policy source**, not observed passes.
The remaining classification is 21 retained narrow source-applicability rows
and 42 blocked deeper rows. All 69 rows have `executed:false` and
`whole_entry_qualified:false`.

The 21 retained rows comprise the prior eight direct-case sources, twelve
retained-engine source arguments and one prospective whole-entry source
specification. Those sources were reviewed but never executed; their unchanged
RI129 driver/absolute entry specification does not automatically target RI134.
This packet neither reimplements nor credits their execution. Their precise
remaining gaps and representative first messages are preserved in the map.

Fixed raw-hash authentication and cache installation, live source-card
provenance, complete reference closure, applicability, actual audit binding,
all eight physical objects, three real candidates, true serial receipts and
outer completions, runtime/history policy and current conformity, and real
monitor/time/RSS/signal/late-output faults remain outside pure-policy tests.
In particular malformed dependency bytes still fail the real fixed hash
before a payload function is called. The extracted tests do not bypass that
ordering. A current-target policy accepting 15/4/71 does not demonstrate that
one producer action executed.

## Preserved scientific and governance boundary

The sealed RI128 producer/auditor, five premises, nine original/copy pairs,
fourteen certificate sections, eight auditor objects and three candidate copies
are unchanged. So are support, epsilon, arithmetic ceilings, fixed environment
and flags, 120-second active-child/536870912-byte sampled-group/8-MiB body
limits, 50-ms intended sampling and 250-ms bounded census, and strict
witness → normal → optimized → audit custody. Early refusal still has no
invented Attempt receipt; root externally preserves actual completion and full
before/after custody. Allocated failures retain the existing guarded finalizer.

Actual C2/C3 signs, simultaneous H30 feasibility, producer 15/4/71 execution,
auditor 15/16 execution and complete independent saved arithmetic remain open.
No scientific body, q6/q7, actual scale or global maximum was decoded or
evaluated. There is no QM/geometry/gravity or physical validation claim. RET
remains paused. Fresh nonauthor review and root adjudication are the stopping
boundary for these new sources.

## Author verification

Complete read scope includes the RI132 root adjudication and root review, full
nonauthor Markdown/machine review, and all 1623 lines of the accepted RI129
audit caller. Source construction used `apply_patch` only. Read-only Node
operations inspected administrative metadata and literal UTF-8 text and
computed opaque hashes. The four moved bodies and complete reverse projection
were checked without importing, compiling, parsing an AST, probing or running
any target/helper. No active cards, copies, fixtures, runtime inventory,
admissions, repository, index or Git changes were made.
