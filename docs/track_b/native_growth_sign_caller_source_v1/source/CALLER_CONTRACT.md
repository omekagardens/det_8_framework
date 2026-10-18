# RI129 — fixed native strict-sign caller contract

26 September 2026. **Source only; execution is not admitted.** This packet
adapts the accepted RI122 native supervision and custody route to the exact
sealed RI128 producer and independent saved auditor. Actual C2/C3 signs,
resource feasibility and full H30 feasibility remain unknown. Root alone
creates execution evidence, admits runs, adjudicates results and publishes.

## 1. Scope and fixed locations

In this contract the following aliases denote literal absolute paths:

- E = `/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0`.
- C = E/closure.
- B = C/native_growth_connected_strict_sign_v1.
- S = `/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv`.
- A = `/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx`.

Only source and explanatory/identity documents exist in E at handoff. C, B,
their target/input copies, all mode evidence, current source/applicability
cards, candidates, authorizations and freezes are prospective. No source-only
document substitutes for any of them. A and every predecessor remain intact.

The fixed accepted RI128 decision is
`/Volumes/AI_DATA/development/det-review-evidence/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json`,
3230 bytes, SHA256
`324644290d2d8eeb79a2af655bed476f02f7d0cc3ffb5fac1672f975f0a3ede1`.
Its exact source-only boundary is checked, including actual_signs_decided,
full_H30_feasibility, numerical_qualification_accepted, scientific_body_decode,
source_execution, resource_feasibility_demonstrated, physical_claim and
programme_complete all false. RET remains paused; measurement is separate.

The sealed scientific sources remain unmodified. Nine ordered original/copy
pairs are defined by the literal PAIRS tables in both callers:

| Role | Original | Future copy relative to B | Bytes | SHA256 |
| --- | --- | --- | ---: | --- |
| checker | S/check.py | check.py | 27288 | 73bb32320be53c38cf85889ca108229d9c2ea2d79b27814ac258eb4b6f133e38 |
| auditor | S/audit_saved.py | audit_saved.py | 41355 | 5c9494e78df31c726c973d2aa0188ca745a3532a351a5826dcb312fca3892ed7 |
| implementation | S/IMPLEMENTATION.md | IMPLEMENTATION.md | 9005 | e9053c9b8e9f6d113febf4cc4b5597aca5e2238a25e67d14c5a3b743149aad26 |
| audit_notes | S/AUDIT_NOTES.md | AUDIT_NOTES.md | 13789 | 89af7f6f7f4ea17e835770ff24ed71e181f5f6f28751f4f7fc8c57cdca77caf6 |
| ri88 | A/closure/native_growth_connected_sensitivity_v1/inputs/ri88.json | inputs/ri88.json | 1828149 | ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b |
| ri88_root | RI88 root below | inputs/ri88_root.json | 2783 | 15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6 |
| ri122_root | RI122 root below | inputs/ri122_root.json | 15477 | 162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc |
| ri124_root | RI124 root below | inputs/ri124_root.json | 3645 | 85b6d5c84139b05d5a18f89614a415ecde962efc429092b914e6f2da33ccde9c |
| ri127_root | RI127 root below | inputs/ri127_root.json | 4071 | 66d274815c101015256ba506f3e6a125375797b1b7946831159d39692ffebd77 |

The four original root paths are respectively:

- `/Volumes/AI_DATA/development/det-review-evidence/ri87-ri88-results-checkpoint-3_kuqmvi/RI88_ROOT_RESULT_ADJUDICATION.json`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri124-root-proof-review-77jju1y6/ROOT_ADJUDICATION.json`.
- `/Volumes/AI_DATA/development/det-review-evidence/ri127-root-proof-review-tz7oyfkj/ROOT_ADJUDICATION.json`.

The direct RI88 input original is an accepted historical copy, not a new
scientific original. Its actual RI88 original, seed acceptance and complete
copy/custody ancestry remain protected by the retained history plus extension.
Root must copy complete bytes exclusively; no filtered/recreated JSON inputs.

## 2. Commands, runtime and ceilings

PYTHON is `/opt/homebrew/bin/python3`; PS is `/bin/ps`. Outer and child cwd
are C. Outer argv is PYTHON -I -S -B E/supervise.py MODE for witness, normal
or optimized; audit uses PYTHON -I -S -B E/launch_audit.py audit. The outer
interpreter must have optimize=0. Child argv is exactly:

| Mode | Child argv after PYTHON |
| --- | --- |
| witness | -I -S -B B/check.py --witness |
| normal | -I -S -B B/check.py |
| optimized | -I -S -B -O B/check.py |
| audit | -I -S -B B/audit_saved.py |

The auditor takes **no arguments or descriptor**. No AUDIT_INPUT.json is
created for RI129. Retaining an actual outer binding does not make it an
auditor operand. Literal pre-admitted tool invocations, not reconstructed
command strings, remain necessary for genuine outer completion.

The environment is exactly PATH=/usr/bin:/bin, LANG=C, LC_ALL=C, TZ=UTC,
__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0. No inherited environment, target,
path, mode or ceiling override. LIMITS remains wall_seconds=120,
rss_bytes=536870912, sample_interval_ms=50, ps_timeout_ms=250. Every census
also respects the remaining active-child deadline. Memory is sampled owned
process-group RSS, not a hard kernel cap. A live-child sample and terminal
empty owned group are mandatory. Keep raw census attempts, signal/launch
deferral, termination, durable exclusive outputs and actual outer zero exit.

Scientific bodies remain individually bounded at 8 MiB. Target rational
input/working/transient bit limits are 32768/1048576/2097154, guarded operation
ceiling 200000 and rational-text ceiling 20000. Counts cover guarded arithmetic
and routed comparisons, not every equality/zero test or interpreter work.
Auxiliary caller metadata has a separate retained 64-MiB read ceiling.
Eight auditor bodies may total at most 8 times 8 MiB; this does not relax any
individual body, child memory or time limit. No measured-fit claim is made.

Retained runtime metadata stays at A/RUNTIME_CLOSURE.json: 2862854 bytes,
SHA256 `35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920`.
Its original schema/status and 2988 file, 258 directory, 40 absence records
are preserved, not renamed or freshly inventoried here. Both callers check
every fixed runtime file, exact directory membership, required ENOENT absence
and visible host/platform premise before/admission/after execution. Existing
bytecode, interpreter links, native dependencies and OpenSSL configuration
remain included. Python -B does not imply absence of bytecode reads.

The original A/RUNTIME_INTERFACE.md and A/RUNTIME_AND_HISTORY_SCOPE.md remain
normative for the trusted Darwin kernel/loader/Apple shared-cache boundary.
No Homebrew dependency is exempt. Because hashlib is imported before internal
checks, root must authenticate the complete pinned runtime/configuration and
namespace **externally before launching Python**. Internal checks cannot
retroactively authenticate bootstrap. Drift requires renewed review, never an
automatic recapture or an exception. No runtime inventory is created here.

## 3. Historical and current source closure

A/HISTORY_RECONCILIATION.json remains 2170307 bytes, SHA256
`b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c`.
Its original 699 ordered roles, six older role arrays, known failures,
superseded-reference explanations and original/copy identities remain intact.
Those 699 records alone are not a claim to cover later completed RI122 work.

E/SOURCE_DEPENDENCIES.json supplies the static extension: 583262 bytes,
SHA256 `a2ef77a9827ceafaf8e94296ec01389d686f3ce2f68064b23d7a1626343c3d1c`.
It has schema ri129-source-dependencies-v1, status SOURCE_ONLY_CLOSED_DEPENDENCIES
and exactly schema,status,protected_files,scope. The 299 sorted dep_0001 onward
entries have exactly role,path,identity,classification,access_policy,
reference_provenance. Each five-field full identity names an existing regular
nonsymlink path. Zero-byte genuine historical evidence remains allowed.
scope is exactly scientific_execution:false, runtime_inventory_created:false,
active_execution_artifacts_created:false, old_history_and_runtime_preserved:true.
No new caller, current contract, dependency manifest or future artifact is
self-referentially inserted into its own dependency entries.

The extension protects completed RI122 source/copies/native/audit custody and
the accepted RI124/127/128 proof/source/review ancestry. Scientific certificates,
stdout, reports and their copies remain opaque bytes. Incidental measurement
pins in the shared RI128 metadata check are preserved only as opaque referenced
evidence; they confer no measurement authority or qualification. The separate
DEPENDENCY_NOTES.md explains the closure boundary and metadata collection.

Authenticate each whole manifest before reading its closed arrays. No caller
discovers new dependencies. Every role enters ordered before/after snapshots
and actual freezes; equal paths/bytes do not silently erase distinct roles.
Exact stage input order is defined by input_paths/native_paths in the sources,
not an inherited count. Complete snapshots add interpreter, supervisor,
freeze and authorization. Current root admission is intentionally not an
input to its own freeze: no hash cycle. Later stages require its genuine
accepted content and every completed prerequisite.

## 4. Source-only acceptance interfaces

Six exact current source roles bind full identities:
native_supervisor=E/supervise.py, audit_caller=E/launch_audit.py,
history_manifest=A/HISTORY_RECONCILIATION.json,
runtime_manifest=A/RUNTIME_CLOSURE.json, caller_contract=this file,
dependency_manifest=E/SOURCE_DEPENDENCIES.json.

Future E/ROOT_SOURCE_ADJUDICATION.json has exactly:
schema,status,accepted_sources,independent_review,ri128_source_adjudication,
history_manifest,dependency_manifest,execution_authorized,
qualification_transferred_to_changed_targets.
schema=ri129-root-caller-source-adjudication-v1;
status=ACCEPT_EXACT_NATIVE_CALLER_SOURCE_ONLY. Both booleans are false.
accepted_sources has exactly the six roles above. The remaining references
are full identities for the corresponding fixed paths and the actual current
E/INDEPENDENT_SOURCE_REVIEW.json. Root creates neither card during preparation.

The latter review requires schema=ri129-independent-complete-caller-source-review-v1,
status=PASS_COMPLETE_SOURCE_REVIEW_ONLY, blocking_findings=[], sources with
exactly those six identities, scientific_execution:false and
execution_authorized:false. Additional narrative is allowed, but every typed
path/bytes/hash reference in decoded metadata must match the closed snapshot.
Source commentary or an author review cannot manufacture nonauthor acceptance.

Future E/MODE_APPLICABILITY.json has exactly:
schema,status,mode,source_adjudication,independent_review,
ri128_source_adjudication,history_manifest,dependency_manifest,supervisor,
target,interpreter,monitor,argv,cwd,environment,limits,retained_engine_only,
changed_target_qualification_inherited,changed_validators_reviewed,
execution_authorized.
schema=ri129-stage-applicability-v1;
status=ACCEPT_PRECISE_FIXED_STAGE_APPLICABILITY_ONLY. The mode, full references,
argv, cwd, environment and limits must be exact. retained_engine_only and
changed_validators_reviewed are true; inherited qualification and execution
authorization are false. Retained-engine applicability is not a statement
that new validators, preflight or target have already been qualified.

## 5. Prerequisite timing and genuine serial custody

The sequence is witness, then normal, then optimized, then independent audit.
Each stage has its own root freeze and authorization. Missing/unaccepted inputs,
current cards, runtime, current freeze/authorization or genuine prior completion
must refuse in a complete **read-only preflight before Attempt allocation**.
Preflight validates current identities, configuration, runtime namespace,
source/applicability and serial custody, then rechecks stability. It creates
no attempt/output/card and launches no child. This is a deliberate changed
guard: old RI122 performed much of this only after allocating the attempt.
Here current cards means the frozen source/review/applicability cards and
freeze/authorization, not the mode's own external ROOT_ADMISSION. Root must
issue that genuine admission before dispatch; later stages validate it.
Preflight stops at its first refusal: its tail resnapshots are not a finally
block, and no preflight receipt/snapshot file is emitted. Do not attribute the
in-attempt engine's complete failure postchecks to an early preflight refusal.

After successful preflight, retain the complete in-attempt validation and
fresh before/admission/final observations; preflight is not cached permission
to skip later checks. A refusal before allocation is not a completed stage.
Root must retain the genuine failed outer invocation and externally reconcile
custody; no fake receipt, consumed-success label or automatic retry. After
allocation, every failure/partial output and all independent final postchecks
remain governed by the retained engine. Source-only preparation runs neither
preflight nor any caller/target/refusal helper.

For each completed native mode NAME, later stages require the six exclusive
files E/name-01/{receipt.json,stdout.log,stderr.log,samples.jsonl,prepared.json,
admission.json}, and E/NAME_EXECUTION_FREEZE.json, NAME_AUTHORIZATION.json,
NAME_ROOT_ADMISSION.json, NAME_OUTER_TOOL_RESULT.json, NAME_ROOT_COMPLETE_REVIEW.json,
NAME_INDEPENDENT_COMPLETE_REVIEW.json, NAME_ROOT_CUSTODY.json,
NAME_APPLICABILITY.json. Every reference is current and frozen for the later
stage. Root/source status alone, a successful receipt flag or an unfinished
outer tool session is insufficient.

The inherited RI84/95 engine freeze, authorization, receipt and saved-addendum
schemas are unchanged. The root pre-admitted literal tool invocation must
match the genuine four-key outer record record_type,source,invocation,result.
Require actual integer exit_code=0, no session_id, exact nonempty chunk_id,
and output parsing to the exact successful launcher mode/receipt/hash message.
Never synthesize a completion from child stdout or a saved receipt.

Root stage admission has exactly schema,status,mode,source_adjudication,
applicability,freeze,authorization,outer_argv,outer_cwd,outer_environment,
outer_invocation,retry_or_limit_relaxation_authorized,history_manifest,
dependency_manifest. schema=ri129-root-stage-admission-v1;
status=ADMITTED_ONE_FROZEN_NAME_INVOCATION. No retry/relaxation is authorized.
The actual source/closure, configuration and literal invocation are bound.

Completed root custody has exactly schema,status,mode,source_adjudication,
applicability,receipt,stdout,genuine_outer,root_complete_review,
independent_complete_review,root_admission,before_after_current_identities_match,
terminal_owned_group_absent,actual_outer_exit,actual_outer_chunk_id,
scientific_math_accepted,programme_complete,root_witness_acceptance,
root_normal_acceptance,candidate_custody,saved_summary_whole_bytes_equal.
schema=ri129-root-completed-producer-custody-v1;
status=ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY. Stability/terminal flags are true,
actual_outer_exit is integer zero; scientific_math_accepted/programme_complete
are false. Witness has null prior/candidate/summary fields; normal binds witness
and candidate custody, with null normal and summary fields; optimized binds
both prior custodies and candidate custody, with complete summary equality true.

Both completed reviews bind exact source/applicability/outer/admission/freeze/
authorization/receipt identities and all six outputs keyed by filename. Their
schemas are ri129-root-completed-mode-review-v1 and
ri129-independent-completed-mode-review-v1; statuses respectively
PASS_COMPLETED_NAME_CUSTODY_PENDING_INDEPENDENT_REVIEW and
PASS_COMPLETED_NAME_CUSTODY_ONLY. mode is exact and blocking_findings=[];
before_after_current_identities_match and terminal_owned_group_absent are true;
native_arithmetic_recomputed, native_mathematics_accepted and programme_complete
are false. Additional narrative cannot add unclosed identity references.

NEW required fields in each of those actual completed native reviews are
current_target_checks exactly {sign_fixtures:15, internal_decision_cases:4,
intended_first_refusals:71}, with strictly integer counts;
current_target_checks_completed:true and changed_target_qualification_inherited:false.
These are obligations on an independent review of the **actual current run**,
not numbers copied from old qualification. Source identity, full outputs and
genuine completion bind them. The four decision cases execute internally;
there is no invented four-item report array. Witness is not circularly required
to have completed itself before admission: its embedded checks are adjudicated
after the separately authorized witness and before normal is admitted.

## 6. Candidate and independent-audit binding

Before and throughout witness, E/CERTIFICATE.json, B/CERTIFICATE.json and
E/AUDIT_CANDIDATE.json must all be absent. Only root later creates their
exclusive complete copies from accepted genuine witness stdout. All three
must be whole-byte identical. Both replay and auditor read B/CERTIFICATE.json;
E/AUDIT_CANDIDATE.json is a retained custody/equality copy only, not an auditor
input. No caller or target writes a candidate.

E/CANDIDATE_CUSTODY.json has exactly schema,whole_bytes_equal,
scientific_math_accepted,replays_admitted,original,copy,audit_copy,source_stdout,
saved_addendum,root_witness_acceptance. schema=ri129-exact-candidate-custody-v1;
whole_bytes_equal=true; scientific_math_accepted/replays_admitted=false.
The false replay field describes creation before later separate admission.
All six references bind actual complete identities; saved addendum retains
the RI84 schema and never replaces witness/normal serial custody.

After all three producers are genuinely completed/accepted, root may create
E/AUDIT_BINDING.json, exactly schema,status,audit_admitted,candidates,custodies,
outer_completions,candidate_custody,source_adjudication,ri128_source_adjudication,
history_manifest,dependency_manifest. No descriptor member.
schema=ri129-actual-three-mode-audit-binding-v1;
status=ACCEPT_COMPLETED_THREE_MODE_CUSTODY_FOR_SOURCE_BINDING_ONLY;
audit_admitted=false. candidates has exactly original,native,audit identities;
custodies and outer_completions have witness,normal,optimized identities.
The remaining references bind their exact fixed actual artifacts. This card
does not itself authorize the audit; separate audit applicability/freeze/
authorization and root admission remain necessary.

The auditor's protected physical domain is exactly eight ordered objects:
auditor,producer,ri88,ri88_root,ri122_root,ri124_root,ri127_root,certificate.
All are distinct regular nonsymlink files including path components and distinct
device/inode pairs. Root original/audit custody copies do not enlarge that
target-domain count; outer protection includes them separately. Finally-path
checks of all eight remain independent, including uncaptured paths on failure.
The audit caller may preserve REPORT.json only as an exclusive exact raw stdout
copy after admitted success; root owns its scientific interpretation.

## 7. Actual output checks reserved to later root review

Opaque caller custody is necessary but not scientific output acceptance.
The future owner and independent reviewer must establish all of the following
from the exact authorized outputs, under the unchanged numerical/read bounds:

1. Witness schema ri128-connected-strict-sign-v1 has exactly the 14 sections
   schema,checker_sha256,input_identities,held_rows,seed,profiles,scalars,domain,
   targets,decision,fixtures,refusal_controls,limits,limitations. Complete typed
   content and canonical ASCII bytes with one newline are required.
2. Each replay's nine fields are status,schema,checker_sha256,certificate_sha256,
   reconstructed_sha256,decision,fixture_count,refusal_count,independent_audit.
   Require PASS, correct schema/pins, 15,71,false, correct complete decision and
   full saved/reconstructed equality. Normal/optimized summary bytes must agree.
3. Every producer executes all 15 exact sign fixtures, four internal decision
   cases and 71 intended-first-refusal checks. The auditor independently rebuilds
   15 fixtures and executes 16 of its own refusal checks. Its 71 producer
   declarations are explicitly **not executed by that consumer**. Old RI122
   166 controls/32 fixtures/nineteen sections are not current qualifications.
4. Audit schema ri128-independent-saved-sign-audit-v1 has exactly 17 fields:
   schema,status,producer_identity,auditor_identity,input_identities,
   reconstructed_certificate_identity,complete_top_level_sections,
   reconstructed_certificate,protected_files,postchecks,
   independent_counted_operations,independently_rebuilt_fixture_count,
   declared_producer_controls,auditor_first_refusal_checks,
   custody_semantics_self_adjudicated,arithmetic_route,scope.
   Require all_saved_fields_independently_match, all 14 independently rebuilt
   sections and complete saved-byte equality, exact eight protected identities
   and eight successful ordered postchecks, and correct actual fixture/refusal
   outcomes. custody_semantics_self_adjudicated remains false.
5. Authenticated five inputs and explicit original RI88 seed acceptance precede
   scientific decoding. Only the fixed eight rows/44 slots and seed positions
   1,2, zero-based (z2/z3), may become operands; forty-row keys and eleven-support-class
   transport acceptance remain binding. Do not reconstruct H/z or evaluate new
   q6/q7 laws, actual scales/maxima or K4/K5.
6. A single uniform-nonpositive target rejects only fixed H30; two strictly
   positive uniform targets yield only two local intervals; unresolved is not
   feasibility. The seven-field decision always has full_H30_feasibility:false
   and actual_scales_selected:false. Shared T1 recovery, other connected
   constraints, all five Di and strict positivity remain obligatory.
   For the accepted native seed, the negative-seed/small-x argument rules out
   both targets being uniformly strictly positive on this containing rectangle.
   The generic LOCAL_INTERVALS_ONLY branch remains exercised by fixtures; its
   appearance as a native result would require discrepancy review, not promotion.
7. Outer source/runtime/candidate/custody validity must be independently accepted
   even when mathematical bodies match. A late mismatch, timeout, failed census,
   signal, nonzero outer exit or incomplete cleanup invalidates apparent success.

RI128 contains embedded qualification, not a separate fabricated-only mode.
Fresh changed-caller/refusal qualification and precise applicability are root
admission obligations. Current source declarations are not an executed suite.
No stub success, permissive fallback or invented accepted field can fill a gap.

## 8. Review boundary and stop

The unchanged low-level identity, I/O, freeze/authorization, monitor, owned-group
cleanup and signal mechanics retain their RI122 framing; target/premise maps,
source/dependency guards, no-argument audit, current qualification assertions
and complete pre-attempt preflight are changed source requiring fresh review.
The predecessor contract at
`/Volumes/AI_DATA/development/det-review-evidence/ri115-native-caller-source-fViRkoKT/CALLER_CONTRACT.md`
remains normative for the retained RI84/95 engine's detailed hash-cycle and
durable-custody semantics. Its old source roles, descriptor, paths, cardinalities
and scientific target are expressly superseded by this contract, not inherited.

This sitting stops at sealed source/contract/dependencies for a fresh nonauthor
review. No new active cards, target copies, descriptors, candidates, runtime
inventory, freezes, admission, source/helper import/compile/AST/probe/run or
scientific evaluation. No repository/index/Git, RET, clocks/book, support change,
new quantum-law search or physical promotion. Publication and a later concrete
execution assignment belong to root after review, not to this source packet.
