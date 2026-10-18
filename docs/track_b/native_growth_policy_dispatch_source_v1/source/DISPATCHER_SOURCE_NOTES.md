# RI136 one-case pure-policy dispatcher — author source notes

Status: SOURCE ONLY, UNEXECUTED, FOR NONAUTHOR REVIEW. This note is an author
description, not source acceptance, execution authorization, successful
qualification, or historical evidence. No subject import, compilation, AST
inspection, probe, case execution, runtime inventory, scientific decoding,
active card, attempt, or fixture was performed in this assignment. The only
author checks were complete text reads, a literal old/new source diff, and
opaque byte counts/hashes. Predecessor source and evidence remain unchanged.

## Closed subject and case scope

The new file is
`/Volumes/AI_DATA/development/det-review-evidence/ri136-native-policy-dispatch-source-g_z472z7/qualify_policies.py`.
It is 23,248 bytes, SHA256
`1ac5514c37f27478fe3991c6f80773e688a0bc13a154029ab47af0e4d9c5eb37`.

It dispatches exactly one member of the fixed 77-native / 62-audit RI134 pure
policy inventories in a fresh process. The four families are dependency
payload, current source-decision payload, independent source-review payload,
and exact current-target 15/4/71 policy. Native has four positive cases, 71
isolated negatives, and two explicitly multi-fault scope-before-missing-index
order probes. Audit has four positives and 58 isolated negatives. These are
139 source-defined cases, not 139 executed or inherited passes.

RI132's old 17/16 narrow controls and entry cases are not included. No caller
production `main`, `run`, preflight, fixture, scientific helper, target check,
or current acceptance-record creation is dispatched. The fixed control's
`run_case(authenticated_caller, case_id)` is called only after authentication;
its fabricated in-memory arguments are not records or file evidence. New
policy observations cannot qualify the complete caller or inherited engine.

The subject directory is
`/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde`.
The dispatcher and independently authored static manifest both bind:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| supervise.py | 89283 | e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d |
| native_policy_controls.py | 22580 | 8c50cb0ac29385265b89fa9d5b77ee766a74e84d49b0a354f9e7d7c0603e7f25 |
| launch_audit.py | 103969 | 74f3ef59520a7d8d360a280bcf5d5389d0e3f6c456e8f02178fbc773c4e5d60b |
| audit_policy_controls.py | 19923 | e04a1014d91a49061ec8bde6a2b318209e12328d82d7633f076fcd77a2952548 |

The fixed subject-only `SOURCE_IDENTITIES.json` is 23,216 bytes, SHA256
`edb77d0f7edd2e79fd55d3f55b781286aceaf876e98fd1850e58a14281476a37`.
Its exact ordered `(id, family, mutation)` inventories, output contracts,
RI134 authority identities, RI132 runner ancestry identities, and new opaque
dependency-manifest identity are authenticated before use. It contains no
current dispatcher or current HANDOFF identity; its hardpin is not circular.

## Exact source ancestry and deltas

The source ancestor is
`/Volumes/AI_DATA/development/det-review-evidence/ri132-native-caller-qualification-source-0ZmB3R5I/qualify_callers.py`,
14,025 bytes, SHA256
`758c82dc6e07026e4fb5bcb4f7368b0d04a0d5203710420d26237fdd3e54b996`.
The complete 270-line ancestor and complete 400-line new file were read and
compared as text. This is a new dispatcher, not a claim that every old
statement survived unchanged or that RI132 observations cover RI136.

Line spans below refer to those exact bytes. Only source text was compared.

| Component | RI132 lines | RI136 lines | Exact correspondence |
| --- | --- | --- | --- |
| Standard-library imports | 10–19 | 9–18 | Unchanged import statements. |
| Refused, require, canonical, exact, digest_text | 40–59 | 54–73 | Unchanged definitions and bodies. |
| read_stable | 61–86 | 88–113 | Unchanged complete definition: non-symlink ancestry, regular positive bounded file, descriptor/path signatures and opaque hash. |
| Strict JSON parser tail | 94–104 | 121–131 | Unchanged duplicate-key, noninteger-number and object-root checks. New read_json requires a positive typed identity and matching literal path before reading, and authenticated raw bytes before parsing; old optional identity support is removed. |
| load_exact_module executable body | 114–121 | 144–151 | Unchanged statements: exact whole bytes, fresh non-main module, normal optimize=0 compile and complete exec. Only its explanatory docstring differs. This future load was not performed by the author. |
| postchecks | 124–134 | 154–164 | Unchanged complete definition; independently attempts each registered file even after another file check fails. |
| interrupted | 137–138 | 167–170 | Revised to retain signal observations; raises before finalization, records without interrupting independent postchecks during finalization. |
| execute_one | 141–249 | 229–379 | Rewritten for the closed RI134 policy scope and separate operational evidence directory, as detailed below. Not an unchanged inherited executor. |
| main | 252–260 | 382–390 | One extra CLI argument; the same four signal registrations, 120-second local alarm, dispatch and alarm cancellation structure. |
| Terminal wrapper | 263–270 | 393–400 | Same failure/SystemExit structure, with RI136 refusal label. |

Other explicit additions are `literal_path`, `validate_identity`, `register`,
`validate_manifest`, `validate_observation`, fixed current source pins, and
signal/finalization state. Constants move source ancestry to RI134 and add
the subject manifest and current handoff paths. Limits retain 120 seconds,
512 MiB self RSS, 8 MiB output and 64 MiB per metadata read; the exact external
envelope additionally declares 50 ms group-monitor sampling and 250 ms `ps`
timeout. Those last two limits are external obligations, not a monitor hidden
inside this dispatcher.

## Authentication and one-case loading sequence

The future CLI is the literal vector:

`/opt/homebrew/bin/python3 -I -S -B /Volumes/AI_DATA/development/det-review-evidence/ri136-native-policy-dispatch-source-g_z472z7/qualify_policies.py native|audit CASE_ID EVIDENCE_DIR AUTH_SHA`

`EVIDENCE_DIR` must already be an immediate, canonical child of
`/Volumes/AI_DATA/development/det-review-evidence`, with nonempty name suffix
after `ri136-policy-run-`; it must be the process cwd. The dispatcher creates
no directory, card, capture, result file, copy, or attempt. The exact environment
is `PATH=/usr/bin:/bin`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`, and
`__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0`, with no additional variables.
Darwin, isolated/no-site/no-bytecode flags, optimize=0, literal dispatcher
argv path and fixed interpreter realpath are checked.

The ordered sequence is:

1. Read `EVIDENCE_DIR/AUTHORIZATION.json` as stable opaque bytes; compare its
   digest to the externally supplied nonzero literal AUTH_SHA before strict
   JSON parsing. Check exact schema, case binding, scope, command prefix,
   cwd, environment and limits. Positive identity byte counts reject booleans.
2. Authenticate the referenced `EVIDENCE_DIR/PREFLIGHT.json` before parsing.
   Check exact bindings, complete external-preflight assertions and expected
   interpreter identity shape/realpath. This checks assertions, not their
   independent origin or the actual complete runtime bytes.
3. Authenticate the externally pinned current source HANDOFF before parsing.
   Its schema is `ri136-native-policy-dispatch-source-handoff-v1`, status is
   `SOURCE_ONLY_SEALED_FOR_NONAUTHOR_REVIEW`, and `execution_authorized` and
   `scientific_execution` are false. Its sorted unique immediate-source-file
   identities exclude itself and include dispatcher plus subject manifest.
   Dispatcher and manifest identities must match the root authorization.
4. Match the literal hardpin of `SOURCE_IDENTITIES.json`, authenticate its
   bytes, and parse the static inventory. Register all four exact subject
   modules, current handoff payloads, direct authority/ancestry identities
   and the opaque dependency manifest. Reject a case outside the exact
   static inventory and a mismatched case triple before any subject loading.
5. Re-read and compare every registered file before loading. Then load the
   entire authenticated control module under a non-main name. Save canonical
   full CASES text, require tuple type, compare every ordered case triple,
   and take an independent JSON-safe selected-case metadata snapshot.
6. Load the entire authenticated caller module under a non-main name and
   call the real `run_case` exactly once. No snippets, source rewriting,
   accepted global mutation, monkeypatch, replacement guard or production
   entry is used. Check the exact selected expected outcome and exact
   native/audit output contract, including each scope boolean.
7. Retain the first error separately. Independently attempt the final
   catalogue tuple-type/text check and every registered opaque file check,
   regardless of primary success or failure. Final signals, elapsed time,
   catalogue stability and all file postchecks affect the verdict.

The selected-case snapshot cannot be changed merely by mutating the original
helper CASES dictionary. Final catalogue checking also rejects replacing the
tuple with a list even when their canonical JSON would otherwise coincide.
This does not purport to prove an arbitrary hostile module noninterfering;
complete source identity and independent review remain load-bearing.

The authorization stores only `outer_argv_prefix`, excluding its own AUTH_SHA.
Root must separately record and authenticate the complete actual dispatch
after hashing the card. The current HANDOFF does not pin its own bytes; the
externally issued authorization pins it. Neither the dispatcher nor static
subject manifest embeds that HANDOFF hash. Source-only declarations in the
manifest/HANDOFF cannot issue operational authorization.

## Results, refusals and finalization limits

Native observations have their fixed nine keys and
`DIRECT_ACTUAL_PURE_POLICY_ONLY` scope. Audit observations have their fixed
eleven keys and `DIRECT_EXTRACTED_POLICY_ONLY` scope. The dispatcher checks
exact outcome, exception type, code and message; native additionally checks
the exact return-kind description. Audit expected metadata and
`arguments_unchanged: true` are checked. Every required false scope field is
checked with `is False`, not truthiness.

Normal output is one bounded canonical JSON envelope containing `result`,
`first_error`, `postchecks`, `catalogue_postcheck`, `received_signals`,
`elapsed_ns`, and `qualified_as_complete: false`. A successful local verdict
uses stdout and exit 0. An ordinary primary failure, failed postcheck, elapsed
limit violation or recorded signal invalidates the verdict and uses stderr
and exit 2. A primary-error-free result can still be invalidated by a
postcheck; `first_error: null` alone is not acceptance. The result explicitly
says external-preflight assertions were only checked, independent outer
origin/custody review is required, and whole-entry/complete-caller/scientific
qualification is false.

Argument-count failure occurs before `execute_one` and uses terminal refusal
text rather than its JSON envelope. Serialization, output-cap, write or flush
failures may also prevent a complete envelope and fall through to terminal
refusal handling; a broken output transport cannot guarantee preservation of
all in-memory error records. Such a run is invalid, not an alternative pass.
The external evidence contract owns raw bounded capture, actual completion
and first-error adjudication. No truncated/partial output can qualify.

During finalization signals are recorded instead of aborting the remaining
postchecks. The local alarm therefore does not kill a stalled finalization.
The external owned-group wall/RSS/output monitor must bound the entire
process, including module loading, finalization, serialization, output and
cleanup. A late signal can make the exit nonzero even if stdout was already
chosen. The external actual return code and process-group completion remain
mandatory. Local elapsed time ends before output serialization/transport;
only the external observation can cover that complete boundary.

## Unresolved external orchestration obligations

No active launcher, monitor, preflight or authorization was created here.
Before any future one-case execution, root must independently supply all of:

- Authorization to execute this separately accepted immutable source version,
  one real externally issued case admission, literal full command custody,
  and a separately owned operational evidence reservation.
- Complete before-load bootstrap authentication of the interpreter, linked
  runtime, namespace, host and source suppliers before this script imports
  even standard-library modules. Self-observation cannot prove this origin.
- Complete current source, historical dependency and runtime closure, with
  independent before/after observations. Internally the new 373-entry
  dependency manifest is authenticated as one opaque file; its 373 listed
  bodies are not traversed or postchecked by this dispatcher. Directly
  registered identity checks do not substitute for that complete closure.
- A real independent owned-process-group monitor under the unchanged normal
  isolated envelope, bounded raw stdout/stderr capture, actual tool/process
  completion, and owned-group cleanup evidence. A synthetic or parent-only
  monitoring record is not the missing observation.
- Review of all primary, catalogue, signal, file, monitor and completion
  evidence without crediting an earlier admission/source refusal as a deeper
  loading, policy, output or custody test.

The stopping point of this assignment is source handoff for independent
review. No full-caller admission, scientific work, successor gate, runtime
qualification claim, old-control inheritance claim, or operational retry is
authorized by this note.
