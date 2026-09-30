# RI140 F02 — preserve the originating pipe failure

This is an unexecuted F02 repair of `owned_process.py`, plus the separately
authorized related F01 startup-handler extension described below. The original
RI138 packet remains immutable. It is not a new launcher admission, fault
observation, policy result or completed qualification. The launcher's F01 repair
is owned separately; this component's F01 extension changes only run_child's
ordinary-signal setup/restoration order, not its child acquisition mechanism.

## Selecting evidence

The complete RI138 independent review Markdown, structured review and handoff in
`ri138-launch-independent-review-6xGu5oak`, and the complete
RI138_ROOT_ADJUDICATION.json and RI138_ROOT_SOURCE_REVIEW.md in
`ri139-root-bootstrap-adjudication-goau3dIc`, were read. The root disposition is
`REQUIRE_F01_F02_IMMUTABLE_SOURCE_REPAIR`; execution_admitted is false and
controls_executed is zero.

The exact predecessor is
`/Volumes/AI_DATA/development/det-review-evidence/ri138-native-external-launch-source-92pbd52w/owned_process.py`:
38953 bytes, SHA-256
`8e749ead931f4a47f83853b1e4bb24c4c752aef79aac7349f0fd5cb7f8de5b62`.
The new file began as that whole source through apply_patch, then received only
the changes listed below. All process wire schemas retain their RI138 labels
because this is the same process evidence protocol, not fresh historical credit.
Only the opening module description is relabeled RI140.

The complete root startup-scope addendum was also read and bound:
`/Volumes/AI_DATA/development/det-review-evidence/ri142-portable-focused25-net0j999/RI140_STARTUP_SCOPE_ADDENDUM.md`,
1715 bytes, SHA-256
`8a6259d9fb2bc0597de215fd8f51a77ab228a6dc1e053fda3ba96643310d9008`.
That narrow authorization does not admit the other RI142 artifacts or any
execution. It identifies a related ordinary-signal acquisition gap, not an
executed counterexample.

## The rejected ordering

Previously four `pump` branches attempted `close_pipe` before recording the
read, sink-write, child-overflow or census-overflow cause. `close_pipe` records
its own unregister and close failures immediately. With paired faults, that
later cleanup error could become first_error; the original cause arrived at an
outer handler too late. A failed result did not make that chronology correct.

The repair records the originating cause at the actual pipe boundary, before
either cleanup operation. The relevant phases are:

- `pipe-read-<kind>-<name>` for an ordinary read failure;
- `pipe-write-<kind>-<name>` for child capture-sink failure;
- `pipe-overflow-<kind>-<name>` for the two existing overflow branches.

Here kind/name remain the existing child-or-ps and stdout-or-stderr values.
The retained type, message and monotonic timestamp describe the original
exception, not a cleanup exception or propagation wrapper. If an unrelated
earlier error already exists, the new pipe cause is correctly later; the repair
does not reset first_error or erase preceding evidence.

## Explicit already-recorded propagation

`Owner.fail_pipe` creates the original error record and passes it to `failure`
first. Only after that recording does it create a `RecordedPipeFailure` token,
perform the unchanged `close_pipe`, and raise the token chained from the
original exception. The token carries its exact owner and original record; it
is internal control flow, not a new observed failure.

`Owner.failure` suppresses only `type(error) is RecordedPipeFailure` with
`error.owner is self`. It neither broadly deduplicates ordinary exceptions nor
accepts another owner's token as already recorded. Therefore unchanged outer
body/cleanup handlers cannot append the same pipe cause again under a new
`owned-body` or `independent-cleanup` label. Unrelated exception handling and
its existing semantics remain unchanged.

The census body and census-tail handlers likewise recognize only the exact
local-owned token. Their event uses `propagated_pipe_failure_refs`, containing
the original record's phase and monotonic_ns, rather than appending a newly
constructed `census` or `census-tail-pump` error. The reference uses the existing
timestamp; it does not fabricate another occurrence or replace the stored
original type/message. Ordinary census exceptions keep their previous event
and error-recording behavior. This is not a claim of system-wide error dedup.

The primary memory record is installed before error-journal writing and before
pipe cleanup. If journal persistence then fails, its existing independent
error-journal failure is later. Both unregister and stream-close attempts remain
independent and in their original order. If both fail, both ordinary cleanup
errors follow the already-recorded I/O/overflow cause, subject to the unchanged
explicit error-cap/omission rules.

## Preserved EOF, bytes, bounds and hard abort

The EOF branch and the complete `close_pipe` body are unchanged. EOF alone is
not converted into a recorded pipe exception. An unregister/close failure after
ordinary EOF can still be the first actual failure when no earlier error exists.
BlockingIOError remains the same no-data-yet path, not a recorded I/O failure.

The child stream's observed-byte count, retained permitted prefix, incomplete
flag and first excess byte are set as before. The census permitted raw prefix
is also retained before its existing overflow refusal. No prefix is enlarged,
output silently truncated into success, or first excess child byte discarded.

All limits and mechanisms outside the specified F02 ordering and F01
startup/restoration changes remain unchanged:
120-second child ceiling with the existing two-second cleanup reserve;
536870912-byte sampled group RSS ceiling; intended 50-ms sampling;
250-ms census ceiling; independent 8388608-byte child stream caps; the shared
67108864-byte metadata budget and narrower existing journal capacities;
bounded later-error and signal storage; genuine live-leader and terminal-empty
requirements; exact owned-group/leader termination; independent close/reap
attempts; and explicit unresolved-cleanup failure.

The parent's SIGALRM remains untouched. The new token is an ordinary Exception,
so the existing bounded failure cleanup runs. Non-Exception hard aborts are not
converted to tokens, swallowed, or given extra deadlines. The existing hard
abort helpers remain unchanged; run_child additionally attempts restoration of
its saved original signal mask on emergency exit. Those exits preserve already
durable partials, attempt only known-handle emergency actions and the saved-mask
restoration, and propagate incomplete outcomes to root.

## Separately authorized F01 startup-handler extension

The inherited raising parent handler previously remained active while the four
startup Sinks and selector were acquired. An ordinary signal could interrupt a
successful Sink open before assignment into owner.sinks. run_child now installs
its record-only TERM/INT/HUP handlers before any Sink or selector acquisition,
inside the already protected ordinary cleanup path. Each Sink still initializes
safe state before opening, and its returned object is registered immediately;
there is no added fallible work between constructor return and registration.

Handler installation itself is a transition: an unchanged parent handler could
otherwise interrupt partial registration. run_child temporarily blocks exactly
TERM, INT and HUP with pthread_sigmask(SIG_BLOCK, ordinary_signals), saving the
returned original mask. Before each signal.signal call it stores that signal's
original handler. The source now fails closed, before any Sink/selector/child
acquisition, if any of those three signals was initially blocked or any original
handler is noncallable. The two exact refusals are `unsupported initially blocked
ordinary signal in parent launcher` and `unsupported noncallable ordinary handler
in parent launcher`. This is a strengthened precondition matching the actual
authenticated launcher's callable raising handlers and unblocked ordinary
signals, not generic support for default/ignored/blocked inherited policies.
Callability alone is not a proof that an arbitrary callback raises; the actual
parent source identity and operational admission still bind that behavior. Even
an unsupported-state refusal follows saved-handler and exact-mask restoration.
It checks the actual sigpending intersection and refuses any
observed pending ordinary signal with the explicit message `pending ordinary
signals during startup registration: [...]`; this is a pending observation, not
a fabricated delivered-handler record. Only complete registration with no such
observation proceeds to restore the exact original mask and acquire resources.
An ordinary registration failure instead reaches cleanup with no Sink/selector
acquired and with any successful handler changes still registered for restoration.

Signals actually delivered to the record-only handler retain the original
received_signals/signal_overflow evidence and invalidate success. The existing
pre-dispatch check refuses recorded startup interruptions. Signals remain
recordable during later finalization; moving the return construction after
restoration ensures a late recorded signal cannot leave an already-computed
successful return. No signal is relabeled as a policy execution result.

Normal restoration now runs in the outer finally, not after the fallible receipt
tail. Thus an escaping ordinary cleanup/finalization exception still runs this
transition and then continues to propagate; it is not converted into a completed
return. While all successfully installed handlers are still record-only (or the
startup registration mask remains in force), run_child blocks only the same
three ordinary signals for restoration. This prevents an already-restored
raising parent handler from interrupting the remaining restoration attempts.
Each saved handler is attempted independently before restoring the original mask.
Mask/pending-check/handler errors are collected in a small fixed-size local list,
then recorded through the existing bounded error machinery, preserving earlier
errors. The original mask is restored in a nested finally even if a handler
restoration fails. No SIGALRM handler or mask membership is changed.

Actual pending-set checks immediately before the handler loop and again after
it, still before restoring the original mask, create explicit
signal-pending-restore / signal-pending-unmask refusals when nonempty. They do not
append to received_signals or assert delivery. Both observations remain evidence
even on an unsupported initial-state refusal. Pending delivery while the original
mask is restored can itself raise through the actual callable parent handler;
that ordinary exception is retained as a signal-mask-restore error after all
saved-handler attempts. Other phases are signal-restore-mask,
signal-restore-pending-check, signal-unmask-pending-check and
signal-handler-restore. The finite snapshots do not count signals or claim
observation of every arrival outside those snapshots. In the supported actual
launcher, arrivals after the final check are delivered to the restored raising
parent handler once unmasked; a later escape is an external refusal, not a
successful process return. Generic ignored/initially blocked policies are not
accepted merely because a pending-set snapshot happened to be empty.

On the complete normal path the added calls are two SIG_BLOCK operations, two
SIG_SETMASK operations and three sigpending observations; early refusals may reach
fewer of them. There are no retries, changed deadlines, added child launches or
new process evidence schemas. Temporary masks add only TERM/INT/HUP and exact
saved-mask restoration leaves the inherited SIGALRM state unchanged. Normal
operation still relies on the authenticated parent keeping its hard watchdog
eligible for delivery.

These are attempted restorations, not a claim that host signal APIs cannot fail.
A failed remask means the ordinary transition cannot promise interruption-free
completion; it is a refusal/incomplete external outcome, never success. A failed
handler/mask restoration is likewise retained as failure, with no retry or
synthetic claim of restoration. Final report/close files may precede these later
errors, so only the post-transition returned error state plus the external root's
actual observation can settle completion; stale receipt success is insufficient.
If ordinary finalization escaped, root must preserve that raw exception and any
already durable evidence, not infer a completed return or all durable tails.

SIGALRM and other non-Exception aborts remain immediate. The outer guards skip
ordinary journals, call unchanged abort_owned for known resources and make a
best-effort saved-mask restoration before propagating. A hard stop before the
initial mask call's return is stored, during handler registration, or during
emergency restoration can leave the mask/handler state incomplete. There is no
claim of cleanup, reaping, receipt completeness or successful restoration in
those cases. The actual external root/tool boundary remains necessary.

## Complete changed-body list

| Definition | Change |
| --- | --- |
| RecordedPipeFailure.__init__ | New owner-scoped internal token holding the already-stored record |
| Owner.failure | Exact local-token guard only; existing ordinary recording remains |
| Owner.fail_pipe | New record-before-close helper and chained propagation |
| Owner.pump | Four ordinary failure branches use the helper; byte/EOF/BlockingIOError work retained |
| Owner.census | Two propagation handlers refer to the prior pipe record instead of duplicating/relabeling it |
| run_child | Separately authorized F01 startup handler installation before resources; narrow ordinary-signal masks/pending refusals; outer-finally restoration; return constructed after restoration; emergency saved-mask best effort |

There are no other changed function bodies. The added class declaration/docstring
and opening module-label edit are the only associated non-body changes.
Owner.close_pipe, Owner.cleanup, Owner.drive, Sink, resource constants,
record-only signal handler, hard-abort helpers and returned process/report/close
field schemas remain unchanged. The coordinator owns the complete saved
delta, correspondence and focused qualification design; this note does not
substitute for that reconciliation or fresh nonauthor review.

## Verification boundary

Author checking is limited to complete literal source differences and opaque
byte identities. No source/helper import, compilation, AST parsing, probing,
fault/fixture construction or execution, control/case run, scientific-body
decoding, runtime inventory, operational card/admission/attempt, or repository/
index/Git operation occurred. No observed pass is claimed for any paired fault.

The independent review's requested focused read-plus-unregister,
write-plus-close, child-overflow-plus-close, census-overflow-plus-close and
EOF-only-close evidence remains prospective. It requires the coordinator's
separate reviewed design and genuine admission. Source review must also verify
both cleanup failures together, original-cause propagation and unchanged hard
abort handling. The related F01 startup/finalization/handler-transition cases
also remain prospective, including partial registration, actual pending signals,
paired finalization/restoration errors and immediate hard-watchdog propagation.
All 139 policy outcomes and deeper native/audit obligations
remain open; no scientific or physical conclusion follows from this repair.
