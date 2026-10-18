# RI138 — concrete owned-process collector, source only

`owned_process.py` supplies the previously missing process mechanism. It does
not supply execution authority, bootstrap truth, scientific evaluation or genuine
tool-origin verification. No launcher, dispatcher, caller, control, census or
fixture was executed while authoring this source. No current runtime inventory,
operational reservation/card or repository change was made by this component.

## Selecting evidence and exact scope

The complete RI136 root decision and root review, complete independent review
and structured verdict, and complete LAUNCH_COLLECTION_CONTRACT.md were read.
RI136_ROOT_ADJUDICATION.json selects an external implementation while retaining
`execution_admitted=false`, `controls_executed=0` and no scientific result.
The exact RI136 dispatcher remains unchanged. This module never imports or
patches it, loads a policy module, writes root cards, retries a case, or creates a
hold/ready handshake for a child that would otherwise finish too quickly.

The sole API is:

```text
run_child(command, cwd, env, outputdir, *, outer_deadline_ns)
```

It may be called once in a fresh authenticated launcher process. `command` must
be a nonempty list of nonempty strings with an absolute executable and no NUL;
Popen explicitly uses `shell=False`. The host must be Darwin. `cwd` and
`outputdir` must already be canonical nonsymlink directories. The environment
must exactly equal the fixed five-variable RI136 environment. No resource
override is exposed. The parent independently verifies the full authorized
command, actual cwd/environment and correct immediate-child reservation; these
minimal local checks do not accept arbitrary commands on root's behalf.

`outer_deadline_ns` is the parent's positive integer monotonic deadline, not an
additional allowance. Invalid preconditions raise before process ownership.
After collection setup begins, body and independent cleanup failures are retained
in the return where possible, even if local evidence storage fails. The parent
must catch a precondition refusal and preserve the real external failure too.

## Real process ownership and deadlines

Exactly one dispatcher Popen is reached. It uses a fresh session, DEVNULL stdin,
two pipes and closed unrelated descriptors. The real returned PID is retained
before the immediate `os.getpgid` observation, so an ownership-check failure
does not erase the known child handle. The observed PGID must equal that PID.
No PID or sample is inferred from the dispatcher's own output.

The process deadline is the smaller of launch-start plus 120 seconds and the
parent's remaining outer deadline. Two seconds are reserved inside that ceiling
for cleanup; ordinary child work therefore receives at most 118 seconds. Early
failure receives at most a two-second cleanup tail, still capped by the original
deadline. This is a stricter work allowance, not 120 seconds followed by an
unbounded grace period. Raw capture close and identity readback must finish by
the original process deadline for success. Receipt construction follows raw
collection and remains under the parent orchestration's overall hard deadline.

SIGTERM, SIGINT and SIGHUP temporarily record rather than raise through
the Popen handle-assignment window. Their original parent handlers are restored.
The parent's SIGALRM watchdog is neither replaced nor consumed, and no timer is
reset or enlarged. Recorded ordinary signals invalidate success and are
checked by active stream, census and work loops. Cleanup observes the original
deadline and performs no blocking wait after it. Up to 1024 individual signal
observations are retained; any additional count is explicit and invalidates
success. Late signals cannot be repaired by an earlier provisional success.

The parent's dedicated HardDeadline is a non-Exception BaseException. Ordinary
handlers catch Exception only. Explicit census/save/run finally guards propagate
any such hard abort; an outer run finally additionally covers an alarm arriving
during an already-entered finalization block. That path performs only one
best-effort immediate SIGKILL of known child/helper groups and leaders, descriptor
closure and ordinary-signal-handler restoration. It does not run a census,
blocking wait, journal/fsync, metadata finalization or receipt-success path.
Already durable partials survive; unresolved ownership/reap and missing tails
must be marked incomplete by the external root. A hard abort is not converted
into a normal returned collection failure or a claimed complete cleanup.

## Census and concurrent stream mechanics

A single selector drains the child stdout/stderr pipes while collecting a real
`/bin/ps -axo pid=,pgid=,rss=` helper's pipes. All pipe descriptors are nonblocking.
No `communicate()`, `subprocess.run()` or unbounded `wait()` is used. Real process
handles are polled with Popen.poll's nonblocking reap operation.

Each census has a deadline no greater than 250 ms and the remaining enclosing
deadline. Up to 50 ms of that same allowance is reserved for census-helper
kill/reap, leaving at most 200 ms ordinary census work. The helper receives its
own freshly owned session and is killed by its exact owned group/leader on
timeout or unfinished pipes. It is never a second dispatcher invocation.
Census preparation and persistence that overrun the census deadline fail too.
Raw stdout/stderr are retained as base64 in the durable event journal, together
with start/end/deadline timing, real helper PID/exit/reap, EOF flags, parsed rows,
child polls and errors. The intended sampling interval remains 50 ms; actual
timestamps are evidence, not a guarantee that scheduling achieved that interval.

The parser requires exactly three decimal fields per nonempty ps line and no
duplicate PID. An observed leader outside its owned PGID fails. Owned-group RSS
is the sum of actual matching rows times 1024 and may not exceed 536870912 bytes.
A live sample requires a pre-census live child poll and an actual leader row
with positive RSS. A fast child with no such sample fails; an empty sample is
not replaced by fabricated timing, a handshake, a retry or output inference.

An accepted terminal-empty census must have begun after the child was actually
reaped and must contain no owned-group rows. A pre-exit snapshot cannot satisfy
that condition merely because a later poll reaped the leader. Descendants left
in the owned group after leader reap fail. Cleanup censuses observe only the
original child/group; there is no case relaunch. They are capped at eight and
spaced by the intended 50 ms, all inside the remaining cleanup deadline. A
faulty cleanup selector/census stops that loop; independent final child poll,
helper reaps, pipe closes and sink closes are still attempted.

Every owned group and leader termination attempt is separately recorded, as are
already-absent outcomes and errors. An unreaped child/helper or missing terminal
empty observation is an explicit failure. A bounded unsuccessful reap is not
described as successful cleanup. Only the exact newly owned PIDs/PGIDs are
signalled; no broad process-name or unrelated group kill is used.

## Exact captures and shared metadata capacity

The six exclusively created files are:

| File | Meaning |
| --- | --- |
| stdout.log | Raw child stdout, independently capped at 8388608 bytes |
| stderr.log | Raw child stderr, independently capped at 8388608 bytes |
| process-events.jsonl | Launch, raw census, termination and reap events |
| process-errors.jsonl | First and subsequent error observations while writable |
| PROCESS_REPORT.json | Provisional process/raw-capture observation |
| PROCESS_CLOSE.json | Independent sink-close/report-write receipt |

Both raw pipes are drained independently. A full-cap-plus-one-byte read detects
overflow: at most the permitted raw prefix is written, the first overflow byte
is explicitly retained in the stream report, and the capture is invalidated.
There is no silent truncation. A partial write retains its actual written count
and digest, marks that stream incomplete and fails collection. Ownership or
registration failure still attempts registration/drain of the original pipes
during cleanup. Missing EOF is a failure, not evidence of a complete capture.

Metadata has a shared 64-MiB ceiling: 63 MiB for events, 512 KiB for errors and
256 KiB for each of the two final receipts. Census raw buffering is restricted
further to a conservative fraction of remaining event quota, reserving space
for base64, parsed rows and framing. Exhaustion refuses rather than silently
discarding evidence or growing storage without bound. These stricter capacity
guards are explicit; no empirical capacity/performance result is claimed.

The sink uses exclusive, no-follow regular-file creation and bounded os.write
loops. Event/error writes attempt fsync immediately; raw captures attempt fsync
on closing. Each independent close receipt records the fsync attempt, complete
bounded readback/digest, descriptor/path stat comparison and close outcome.
Readback verifies the bytes actually present, not only the proposed bytes.
Directory fsync is attempted after initial creation and final receipt writes.
Root must independently observe the final paths, bytes and filesystem custody.

## First error, bounded later errors and finality

The first body/census error is retained before independent termination/reap
errors. Up to 64 later details are retained; omitted_error_count records every
additional error whose detail cannot fit that bounded list. Error text is capped
at 1024 characters with message_truncated and original_message_characters fields.
A failed error journal is attempted once, marked error_journal_unavailable and
not hammered by a repeating cleanup loop. Any omitted detail or unavailable
error journal invalidates success. Failure evidence is never presented as an
exhaustive transcript when a bounded detail budget has been exceeded.

Each final serialized receipt must fit its own 256-KiB reserved capacity. A
serialization/cap/write/fsync/identity/close failure is retained as a failed
receipt, not an accepted truncated JSON document. The first receipt is expressly
provisional: later error-sink close, close-receipt persistence or signal-handler
restoration can still invalidate the returned result. The final receipt cannot
authenticate its own last close. Such a failure remains in the return for the
root to preserve through an independent channel. No finite file scheme can
guarantee its own durable failure receipt on an unwritable or failed filesystem.

The return has schema/status/success, report, report_file, close_receipt, the six
files, first_error, later_errors, omitted_error_count,
error_journal_unavailable, received_signals and signal_overflow, plus
outer_tool_origin_established=false and root_acceptance=false. `report` contains
the genuine returncode, ownership observation, all process timestamps, sample
counts, peak group RSS, terminal-empty result, raw stream states and close
receipts. `report_file` and `close_receipt` retain exact saved identities and
independent errors where available. Paths to files never successfully opened
remain declared expectations whose missing post-observation must be retained.

No local success field confers root acceptance. The parent must preserve the
whole returned failure independently, attempt complete custody postchecks,
reconcile real tool history and actual terminal exit, and reject a nonzero or
unfinished outer invocation. This module never prints a fake tool chunk/exit,
creates RAW_TOOL_RESULT.json or claims that a saved receipt proves tool origin.

## Reviewed ancestry and changed mechanism

The source reuses the *reviewed design obligations*, not an unmodified copied
function. Its concrete ancestry is the accepted RI134 supervise.py, 89283 bytes,
SHA-256 `e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d`:

| RI134 source | Preserved obligation | RI138 adaptation |
| --- | --- | --- |
| Attempt, lines 1126–1159 | Exclusive evidence and independent durable closes | Bounded Sink, raw readback and two-stage final receipts |
| monitor, lines 1162–1213 | Real raw ps, owned rows/RSS, live and terminal observations | Concurrent nonblocking child/helper drains and stricter post-reap terminal sample |
| terminate_owned, lines 1216–1237 | Exact group/leader kill and recorded reap | Poll-only deadline-bounded cleanup with independent helper custody |
| run, lines 1273–1446 | Real session/leader, limits, preserved first error and independent tails | Fixed four-argument API, separate parent authority, capped errors/storage and shared selector |
| stop_signal, lines 1456–1460 | Do not lose the newly spawned handle on ordinary catchable interruption | Temporarily recorded TERM/INT/HUP, preserved parent hard alarm and explicit non-Exception abort guards |

The old monitor's subprocess.run timeout cleanup and direct-to-file child output
do not provide the independently bounded drain/census tails required here.
Consequently the new selector and bounded storage machinery are newly authored
source requiring fresh complete review, not inherited execution qualification.
No RI135 or RI137 measurement launcher is copied, imported or retargeted.

## Explicit host and review limits

The monitor is a sampled process-group observation, not a kernel memory limit,
hostile-process containment or proof that an escaped/reparented descendant never
existed. Ownership/session and PID reuse rely on the same trusted-host boundary
as the accepted supervision, with exact contemporary observations retained.
Blocking kernel/filesystem/Popen operations cannot be made arbitrarily
preemptible by Python bookkeeping. The preserved parent watchdog can interrupt
where the runtime delivers it; the real external tool deadline and root stop
remain the ultimate boundary. In particular a hard abort before a Popen handle
becomes available cannot justify inventing a PID or claiming completed ownership
cleanup. A stuck kernel cannot be repaired by a successful-looking receipt.
Crossed deadlines or failed cleanup must remain failures.

All methods above are prospective source behavior only. This component has not
been imported, compiled, AST-parsed, probed or run. Its metadata/text review does
not establish syntax execution, scheduling, resource feasibility, runtime
applicability, actual policy results or complete caller qualification. Seal with
the complete RI138 packet for independent review and root adjudication before
any separately admitted execution.
