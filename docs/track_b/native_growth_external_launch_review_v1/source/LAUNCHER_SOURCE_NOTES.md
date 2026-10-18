# RI138 two-phase launcher source notes

`launch_policy_case.py` implements the external orchestration selected by the
accepted RI136 review. This is new, unexecuted source, not a completed control,
runtime observation or admission. The three metadata files remain unchanged.
Only a later genuinely admitted exact RI136 case may run through this code.

## Fixed subject and source authentication

The source directory is
`/Volumes/AI_DATA/development/det-review-evidence/ri138-native-external-launch-source-92pbd52w`.
The launcher hard-pins SOURCE_IDENTITIES.json at 23755 bytes, SHA-256
`ea8dec463c6827bd10ebb15df1bb52932cd03552baee869c933acae4f74c5465`.
That manifest fixes the unchanged RI136 dispatcher, complete 77/62 inventories,
distinct observation contracts, predecessor acceptance and expected runtime and
history metadata. It binds the 396-file source dependency manifest but excludes
current code and the current handoff, avoiding a source hash cycle.

The externally pinned root plan separately binds the complete current handoff.
Its exact fields are schema, status, source_directory, files, predecessor,
author_checks, scope, remaining_obligations. Schema is
`ri138-native-external-launch-source-handoff-v1`; status is
`SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW`. Every payload is a sorted, unique,
ordinary path/bytes/sha256 identity immediately under the source directory;
the handoff does not list itself. Exact actual namespace and every payload
identity are checked before either helper is loaded. The author-check identity
must be the payload AUTHOR_STATIC_CHECKS.json; the predecessor must be the
accepted RI136 handoff. Source-only scope is checked exactly.

Both helpers load from their complete authenticated bytes under fresh non-main
module names. There is no snippet extraction, global replacement, alternate
module, extra policy evaluator or production caller entry. The whole-module
loading and finite stable-read patterns follow the reviewed RI136 mechanism;
this note does not claim byte-identical launcher ancestry. The helper-specific
RI134 correspondence is documented by their respective authors.

## Exact root inputs and separate phases

The only CLI forms are `prepare PLAN_SHA` and `run PLAN_SHA`, after the fixed
`/opt/homebrew/bin/python3 -I -S -B` and absolute launcher path. The cwd must be
a canonical nonsymlink immediate child of the evidence root with a nonempty
`ri136-policy-run-` suffix. The environment is exactly PATH=/usr/bin:/bin,
LANG=C, LC_ALL=C, TZ=UTC, __CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0. Normal
optimization, Darwin host, literal source path and interpreter resolution
are checked. The initial bootstrap remains genuine root's external premise.

ROOT_PLAN.json has exactly schema, status, caller, case, operational_directory,
source_manifest, source_handoff, launcher, independent_review,
root_adjudication, external_bootstrap, outer_environment, limits,
phase_budgets, acceptance_assertions, prepare_authorized, one_run_authorized,
scientific_execution_authorized, production_entry_authorized,
retry_or_limit_relaxation_authorized. Its schema is
`ri138-root-one-case-plan-v1`; status is
`ADMIT_PREPARE_AND_ONE_CONDITIONAL_POLICY_RUN`. The two phase permissions are
true and the three scope/relaxation permissions false. Case is one exact
accepted id/family/mutation triple. All ordinary identities have exactly path,
bytes and sha256, with canonical absolute path, bounded integer byte count and
nonzero lowercase digest. Root authority identities must be outside the writable
operational reservation. Administrative JSON rejects duplicate keys, decimals,
nonfinite values and non-object roots; whole bytes are checked before decoding.

The exact root-owned acceptance_assertions are source_handoff equal to the
current handoff identity, source_accepted true, blocking_findings an empty list,
complete_caller_qualification false and scientific_result_claimed false.
These are mechanically checked root assertions, not proof of their genuine
origin. The launcher does not guess an independent review's future schema or
manufacture acceptance. Genuine root must inspect the actual pinned review,
adjudication and bootstrap evidence before issuing the plan and each invocation.

After hashing the plan, root writes ROOT_PREPARE_DISPATCH.json with exactly
schema, root_plan, prepare_argv, outer_cwd, outer_environment, limits,
phase_budgets, literal_tool_invocation. Its schema is
`ri138-root-prepare-dispatch-v1`. `invocation` in the source constructs the
deterministic literal tool dictionary with cmd, workdir, login=false,
yield_time_ms=1000, max_output_tokens=2000. cmd is formed by individually
`shlex.quote`-quoting these tokens in this order:

```text
exec /usr/bin/env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC
__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0
/opt/homebrew/bin/python3 -I -S -B ABSOLUTE_LAUNCHER prepare PLAN_SHA
```

The displayed line breaks are explanatory only; the actual command joins tokens
with single spaces. The run dictionary uses `run` in that same position. Code
never evaluates a shell string; only root's real tool executes the prebound
literal command. No command contains its own enclosing record's hash.

Before preparation the reservation contains exactly ROOT_PLAN.json and
ROOT_PREPARE_DISPATCH.json. Before run it additionally contains all nine complete
prepare artifacts, PREPARE_TOOL_RESULT.json and ROOT_DISPATCH.json. Extra,
missing, directory, symlink and stale-phase entries refuse; there is no overwrite
or automatic retry. Exclusive PREPARE_STARTED.json and RUN_STARTED.json claim
each phase only after authority, source and frozen-spec authentication. A
pre-ownership refusal emits raw refusal text, not invented phase postchecks.

## Implemented preparation and intervening genuine tool evidence

The custody helper loads authenticated fixed expectations: original 373 source
dependencies, RI122 history/runtime files, runtime namespaces/absences and host
premises. The launcher adds all 396 current dependency identities, the complete
current packet and root inputs. Expectations are immutable canonical bytes and
are retained exactly, without a terminal newline, in PREPARE_EXPECTATIONS.json.
Start marker and spec identities are included in the before observation.

PREPARE_BEFORE.jsonl receives every full observation as canonical ASCII JSON
plus one newline. Its synchronous sink returns exact path/offset/bytes/sha256
references only after writing the entire record and fsync. Each file/journal is
capped at 64 MiB. A failed sink open supplies a failing callback to observe_all;
it does not skip independent object observations. Close fsync, descriptor close,
independent readback and directory fsync errors remain separately recorded.

Only complete, matching, durable before evidence permits exclusive creation
of the exact unchanged RI136 PREFLIGHT.json and AUTHORIZATION.json. Their
preflight evidence binds the actual before summary/log, frozen spec, root plan,
external bootstrap identity and current launcher handoff. This is mechanical
card construction under explicit root delegation, not self-issued acceptance.
The authorization binds its complete preflight and a hash-free child argv prefix.
The final authorization digest is never inserted into its own content.

PREPARE_AFTER uses the original frozen spec extended purely with newly created
artifact identities. It never reloads changed expected manifests as new truth.
Extension failure is preserved and the original complete spec is still observed.
All ordinary after/final failures survive alongside the first cause. Final
source and operational namespace checks are independent. The bounded
PREPARE_RESULT.json contains provisional success before its own close; the
compact terminal line separately carries its complete identity and actual
result-close errors. Only zero exit, terminal success and genuine root review
may permit the next phase. Cards remaining after a failed prepare confer no
permission to run.

Root then preserves PREPARE_TOOL_RESULT.json with exactly record_type, source,
invocation, result. record_type is
`transcription_of_genuine_exec_command_result`; source is
`Coordinator task tool history; actual invocation, not replay or reconstructed success`.
Its invocation must equal ROOT_PREPARE_DISPATCH's exact dictionary. Result must
have integer exit_code zero, actual nonempty chunk_id, no session_id, exact
compact terminal output and nonnegative finite wall_time_seconds; optional
original_token_count is a nonnegative integer. Only this genuine tool
transcription parser permits finite JSON floats. These consistency checks do
not establish tool origin; root must preserve real initial/session/final history.

ROOT_DISPATCH.json retains the RI136 schema
`ri136-literal-policy-dispatch-v1` and fields schema, caller, case, authorization,
outer_argv, outer_cwd, outer_environment, limits, literal_tool_invocation, plus
root_plan, prepared_result and prepare_tool_result. outer_argv is the full
unchanged RI136 child argv with the actual authorization digest. Its tool
dictionary invokes the future parent `run PLAN_SHA`, not a fabricated child
tool call. Prepared result/card/tool identities and every complete prepare
artifact are authenticated again before run ownership.

PLAN_SHA does **not** transitively authenticate this later ROOT_DISPATCH file.
Genuine root must preserve and verify its complete identity externally before
the actual run tool call, then reconcile exactly that identity with the
RUN_EXPECTATIONS inventory and RUN_RESULT.root_dispatch. The launcher checks
command consistency and records the observed identity; it cannot manufacture
this external binding or genuine tool origin. Adding that digest inside the
record's own literal command would create a hash cycle and is not done.

## Implemented run and independent output checks

Run builds and saves its own frozen expected inventory, adding all authenticated
prepare artifacts and later root inputs. Fresh complete RUN_BEFORE observations
and both namespace checks precede the single run_child call. ROOT_DISPATCH's
original observed identity is reread immediately before launch. There is no
loop, warm module reuse, child hold handshake, silently substituted attempt or
scientific entry. A missing real live-leader sample remains failure.

The collector's first error, later errors, signal state, omitted-error count
and unavailable-journal flag are preserved. The launcher independently checks
the originally returned PROCESS_REPORT and PROCESS_CLOSE identities. The
authenticated CLOSE supplies the final identities of all four logs, including
the error journal absent from the provisional report. Saved report content must
equal the returned report. An original pin remains the expectation even when
a reread fails; changed actual bytes never become a new successful baseline.
All six known process paths receive independent read/error attempts after an
ordinary launch failure, even when run_child raised instead of returning.
Unpinned or missing partial files retain explicit failure and actual observation
where available. They cannot yield success.

The child must have a genuine zero exit, successful independent collector,
empty stderr and one complete canonical stdout JSON line. The launcher checks
the exact seven-field RI136 envelope and eighteen-field result, all source and
card bindings, strict scope booleans and native/audit observation contract. It
reconstructs the entire ordered dispatcher postcheck identity set from the
unchanged RI136 handoff, subject manifest and cards; nonempty/all-true alone is
insufficient. Boundary equals the fixed family-to-policy-function mapping.
The unchanged authenticated dispatcher/control pair supplies the exact selected
exception/message/return expectation; no new copied policy evaluator is added.

Full RUN_AFTER is attempted after every ordinary body failure, from the same
original frozen expectations plus original created-file pins. Independent file,
source namespace, operational namespace and final durability failures cannot be
erased by an internally successful child envelope. RUN_RESULT and its compact
terminal line remain collected evidence, explicitly not external root acceptance
or complete caller qualification.

## Measured budgets, hard abort and last-close boundary

Fixed metadata preparation is 60 seconds. Before custody has 300 seconds,
including journal close/summary and prepare-card writes. After custody has
300 seconds, including its close/summary. The unchanged child limit remains
120 seconds with the collector's two-second internal cleanup reserve.

There is one shared 60-second finalization budget, not a fresh allowance per
operation. For run, the first portion starts at the collector's actual
collection_end_ns and includes its final receipt persistence, child-envelope
validation and process-artifact checks. The elapsed portion is recorded as
final_budget_spent_before_after_ns. After custody reserves only the remaining
portion, which pays for final rereads, namespace checks and result durability.
Before/after phase summaries never receive an extra 60-second grant. Final
write/close and terminal flush deadlines are rechecked; a late flush may leave
earlier stdout success text followed by a genuine nonzero exit, which root must
reject. The overall ceiling is 840 seconds, not an exemption from phase limits.

HardDeadline is a dedicated BaseException; ordinary custody and collector
handlers catch Exception. On a hard watchdog abort, guarded finalizers skip
further persistence; known process ownership receives only best-effort kill and
descriptor cleanup from the collector. No complete after observation, result
or successful close is invented. The last durable journal rows and frozen
inventory expose incomplete work. Arbitrarily blocked host/kernel/fsync calls
remain the explicitly trusted host and real root/tool hard-stop boundary,
not a guarantee established by a receipt or Python alarm.

All source preparation here was text/administrative metadata only. No new
source/helper import, compilation, AST, probe, run, case or fixture execution;
no runtime inventory, scientific JSON decoding, operational record, repository
or Git operation occurred. This implementation requires fresh full nonauthor
review and root adjudication before any real launch. No new scientific gate,
measurement work or RET work is selected.
