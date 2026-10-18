# RI136 — version-bound subjects and predecessor dependencies

Source preparation only. These files bind a prospective one-case dispatcher to
the accepted RI134 source version and its exact 139 declared pure-policy cases.
They do not authorize execution, certify a current runtime, establish completed
caller qualification, or produce a scientific result.

## Fixed files and scope

The files are under
`/Volumes/AI_DATA/development/det-review-evidence/ri136-native-policy-dispatch-source-g_z472z7`:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| SOURCE_IDENTITIES.json | 23216 | `edb77d0f7edd2e79fd55d3f55b781286aceaf876e98fd1850e58a14281476a37` |
| SOURCE_DEPENDENCIES.json | 652822 | `da5708eb15abbb4da7a8c17b5a6c737b2fce9e8663c2177e4dbb1b9e2107d42c` |

The subject manifest has schema `ri136-policy-subject-identities-v1` and status
`SOURCE_ONLY_VERSION_BOUND_POLICY_CASES`. Its exact top-level fields are schema,
status, subjects, acceptance, runner_ancestry, dependency_manifest and scope.
Scope has exactly four false fields: execution_authorized,
scientific_execution, old_cases_included and production_entry_authorized.

Each subject has a caller identity, a control-module identity, case_count,
ordered_cases and result_contract. An identity has exactly path, bytes and
sha256. A case row has exactly id, family and mutation. The two subject modules
and two caller modules are unchanged RI134 files:

| Role | Bytes | SHA-256 |
| --- | ---: | --- |
| native caller: supervise.py | 89283 | `e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d` |
| audit caller: launch_audit.py | 103969 | `74f3ef59520a7d8d360a280bcf5d5389d0e3f6c456e8f02178fbc773c4e5d60b` |
| native_policy_controls.py | 22580 | `8c50cb0ac29385265b89fa9d5b77ee766a74e84d49b0a354f9e7d7c0603e7f25` |
| audit_policy_controls.py | 19923 | `e04a1014d91a49061ec8bde6a2b318209e12328d82d7633f076fcd77a2952548` |

All four paths remain under
`/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde`.
The manifest binds their actual opaque identities, not copies, aliases, edited
globals, derived functions or a renamed older runner. Their identities agree
with the accepted RI134 source handoff.

## Closed case inventory and distinct result contracts

The manifest contains all 77 native and all 62 audit triples, in source order.
Each inventory was compared both with its reviewed RI134 coverage JSON and with
literal `_case` lines in the complete CASES block. That check used text matching,
not an import, AST, evaluation of `_case`, or execution of any control.

| Subject | Dependency | Source decision | Source review | Current-target policy | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Native | 25 | 21 | 15 | 16 | 77 |
| Audit | 19 | 17 | 9 | 17 | 62 |

Native has four positive baselines, 71 isolated negative cases and two explicit
multi-fault ordering probes. Audit has four positive baselines and 58 isolated
negative cases. None has been executed in this preparation. No RI132 legacy
17-native/16-audit case or whole-entry case is admitted by this inventory.

The complete, pinned control source carries the exact expected exception type,
code, message and positive return semantics. The manifest deliberately does not
reimplement the case builder. Before any later subject load, the dispatcher must
authenticate the manifest and select one literal case from these closed triples;
after authenticated load it must reconcile the actual module's complete ordered
triples and enforce that module's exact expected result. A count alone is not
the inventory.

The native result has exactly nine keys: id, boundary, outcome, observed,
coverage_scope, whole_entry, active_acceptance_record_created,
complete_caller_qualification and scientific_execution. Its observed object
has exception_type, code, message and return_kind. Its scope is
`DIRECT_ACTUAL_PURE_POLICY_ONLY`; the four scope booleans are false.
The native expected object additionally has outcome. A dependency positive
requires a new list containing the same validated entry objects; the other
three family positives return None. The pinned controls check recursive exact
types and values, dictionary order, sequence shape and float representation.

The audit result has exactly eleven keys: id, boundary, outcome, observed,
expected, arguments_unchanged, coverage_scope, whole_entry,
actual_target_checks_executed, complete_caller_qualification and
fabricated_arguments_are_history. Its observed object has exception_type,
code and message; its expected object additionally has outcome. Its scope is
`DIRECT_EXTRACTED_POLICY_ONLY`; arguments_unchanged is true and the four scope
booleans are false. Its argument-preservation check is canonical JSON value
equality, not native-style dictionary-order or arbitrary-object identity
preservation. These two contracts are intentionally not collapsed into a more
generous common result schema.

Direct testing of the typed 15/4/71 acceptance predicate is not the actual
15/4/71 qualification. Fabricated policy arguments are never cards, historical
records, acceptance decisions, runtime observations or scientific evidence.

## Acceptance and runner ancestry

The acceptance object directly binds five roles:

- source_handoff: RI134 source HANDOFF.json;
- independent_review: RI134 INDEPENDENT_SOURCE_REVIEW.json;
- independent_review_note: the complete accompanying review Markdown;
- independent_review_handoff: the RI134 review HANDOFF.json;
- root_adjudication: RI134_ROOT_ADJUDICATION.json.

The accepted review verdict is `PASS_BOUNDED_UNEXECUTED_SOURCE_ONLY`. The root
decision is `ACCEPT_BOUNDED_UNEXECUTED_EXTRACTION_AND_SELECT_DISPATCHER`:
source_accepted is true, while execution_admitted, current_caller_qualification,
current_runtime_observed and scientific_result_claimed are false, and
controls_executed is zero. Exact authority identities bind those facts; the
subject manifest does not promote them.

The runner_ancestry object binds caller_qualifier, source_identities,
evidence_contract and source_handoff to the immutable RI132 qualify_callers.py,
SOURCE_IDENTITIES.json, EVIDENCE_CONTRACT.md and HANDOFF.json. They are ancestry,
not authorized alternate launchers or compatible current subject sources. The
RI132 runner's original pins are not retargeted or patched.

## Dependency extension: 343 retained plus 30 selected

The dependency file retains the protocol schema
`ri129-source-dependencies-v1`, status `SOURCE_ONLY_CLOSED_DEPENDENCIES`,
top-level fields and scope from the accepted RI134 manifest. Its 373 entries
are sorted by absolute literal path and numbered dep_0001 through dep_0373.
Each has role, path, identity, classification, access_policy and
reference_provenance. Full identities have path, resolved_path, bytes, sha256
and symlinks. All observed files are regular, canonical, nonsymlink files with
resolved_path equal to path and an empty symlink list.

The inherited RI134 manifest is 624320 bytes, SHA-256
`80fb2a5a5f5a318208c9c6389bb7b59646ca18002b32bec01c632d33904cea9a`.
All its 343 entries retain their identity, classification, access policy and
provenance unchanged. Only role numbers are rebased to preserve sorted order.
Earlier roles still mean roles in their earlier manifest; no old artifact is
rewritten. The inherited manifest itself is included among the new dependencies.

Exactly 30 files are added:

| Selected namespace | Files |
| --- | ---: |
| Entire sealed RI134 source namespace, including HANDOFF.json | 17 |
| Entire sealed RI134 independent-review namespace, including HANDOFF.json | 8 |
| Selected RI134 root acceptance/support records | 5 |

The first two namespaces are
`ri134-native-validator-extraction-source-y8kwkcde` and
`ri134-native-extraction-independent-review-mcwy0ya3` under the external evidence
root. Their exact directory membership and source/review handoff payload pins
were checked. The five selected root files under
`ri134-root-source-adjudication-e9zhmh62` are RI134_ROOT_ADJUDICATION.json,
ROOT_SOURCE_REVIEW.md, ROOT_REVIEW_RECONCILIATION.json, check_review.py and
SUCCESSOR_RESERVATIONS.json. The root directory is not a complete claimed
namespace. Publication checkpoints, REPO_ENTRY.json, parallel measurement
records and other unselected root artifacts are not silently added.

There were no duplicate literal paths among the 30 additions and inherited
343 entries. Equal content at different paths remains distinct provenance.
Preserved review-method script revisions remain opaque source evidence; no
review helper was invoked.

This new 373-entry file is a dispatcher preparation dependency boundary. It is
not installed as the RI134 callers' production dependency manifest. The unchanged
callers retain their original RI134 path, 343 entries and whole-file pin.

## Observed metadata checks and deliberate closure boundaries

All 373 selected dependency files were opaquely hashed and compared with their
expected identities. Path components were checked for symlinks. Device, inode,
mode, size, mtime and ctime were compared across the initial path, open-file,
post-read descriptor and final path observations. This establishes finite
observed stability, not a continuous lock or future runtime custody.

There are 156 metadata-readable dependency entries: 145 inherited and eleven
new administrative JSON bodies. The predecessor's accepted 145-body recursive
reference review is retained as predecessor evidence; that historical traversal
was not rerun or described as new execution. The eleven new metadata-readable
bodies were traversed for typed path/bytes/sha256 references. Their 785 reference
occurrences all matched the selected 373-file dependency boundary, including
every additional identity field present. There were zero unclosed or mismatched
occurrences in this explicitly limited traversal.

The inherited history and runtime manifests were whole-file authenticated
before reading their expected identity arrays as potential terminal boundaries:
699 retained history roles and 2988 expected runtime files. None of the 785 new
reference occurrences needed either boundary. No current runtime file,
namespace, absence, host state or installed environment was inventoried. Old
expected runtime metadata is not evidence about a future process environment.

ROOT_REVIEW_RECONCILIATION.json and SUCCESSOR_RESERVATIONS.json are deliberately
opaque-only supporting records in this extension. The latter contains a
cross-lane RI135 measurement handoff pointer: its presence has been disclosed,
but its referent is not interpreted, accepted or pulled into native dependency
closure. The former is retained as whole supporting evidence without treating
its internal references as new dependencies. Accordingly, this note makes no
claim that every typed reference in every added JSON body was traversed or
closes within the native packet. That restriction is explicit access policy,
not an overlooked reference or an inferred measurement authorization.

## No self-hash cycle; external authority remains necessary

The subject manifest excludes the current dispatcher, itself, this note and the
current RI136 HANDOFF. It binds only the unchanged predecessor subjects and
authority/ancestry records plus the new dependency manifest. The dependency
manifest excludes every current RI136 file. The dispatcher may therefore pin
the complete subject manifest without a self-hash cycle.

A separately root-pinned final RI136 HANDOFF must bind the complete current
packet, including dispatcher, subject manifest, dependency manifest, contract
and this note. External authorization must pin that handoff and the subject
manifest consistently. A manifest's self-description is not root approval,
and child-produced observations cannot substitute for outside pre/post custody.
The external root must separately admit the exact runtime, resources, selected
case, launch, actual completion and custody evidence before any execution.

The work here used only literal text, administrative metadata and opaque bytes.
No research source/helper import, compile, AST, probe, control or fixture run;
no scientific JSON decoding; no current runtime inventory, active card, copy,
freeze, admission, attempt or candidate; and no repository/index/Git operation
was performed. The three new files require complete source review and root
adjudication with the rest of RI136. All 139 outcomes remain unobserved.
