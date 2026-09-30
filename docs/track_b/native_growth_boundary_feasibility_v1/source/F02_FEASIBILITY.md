# RI143 F02 boundary feasibility — eight unchanged variants

Disposition: **BLOCKED_DESIGN for all eight qualification designs; no controller
implementation is justified by the unchanged premises.** This is not a finding
that every branch is intrinsically unreachable. Clean successful EOF (F02-7) is
a source-feasible natural path; its independent boundary witness and complete
unchanged monitoring/custody feasibility remain unestablished. The other rows
have the specific causal/control gaps below, not merely a missing permission to
run. No attempt, fixture, injected fault or observed qualification is reported.

The controlling decision is RI140_ROOT_ADJUDICATION.json in
`ri140-root-source-adjudication-8796wh9l`: exact source accepted with execution
prerequisites, execution_admitted=false, focused_controls_executed=0. The full
root review, independent HANDOFF/Markdown/JSON review, complete 850-line
owned_process.py, complete 400-line RI136 dispatcher, focused design and root
interface contract were read. The launcher integration at lines 780–1040 was
also read; no new whole-launcher/custody semantic review is claimed. Exact input
identities and the eight machine-readable rows are in F02_BOUNDARIES.json.

## Meaning and invariant evidence requirements

The seven original scenario labels expand to eight attempts only because
F02-1 has two cleanup alternatives. IDs here are F02-1-UNREGISTER,
F02-1-CLOSE, F02-2, F02-3, F02-4, F02-5, F02-6 and F02-7. Child stdout and ps
stdout are proposed stream instantiations for a future design, not additions or
amendments to the accepted inventory. No current case is available for dispatch.

Any eventual focused failure qualification must preserve the actual failing
outer result. It cannot make RI140's policy-success validator accept an outer
failure. run_phase records monitor failure; the six original process artifacts,
late returned errors, after-custody attempts and genuine terminal tool history
remain necessary. A source repair can be accepted while this operational
qualification is still blocked. No F02 outcome grants one of the 139 policy
outcomes or resolves the deeper 20 native / 42 audit obligations.

An independently authenticated observer would have to identify the real parent,
child/helper, descriptor generation and pipe/file role; bind the unchanged
source/runtime and exact argv; locate the actual Python and underlying syscall
boundaries; and retain actual returns, exceptions and their causal order. It
must distinguish an attempted operation from an operation that returned or
raised. Kernel timestamps, source error labels and intended controller schedules
are not interchangeable observations. No suitable complete supplier, privilege
model, timing argument and bounded evidence contract have been established here.

In particular, an errno chosen by a proposed controller is not an observed
Python exception. The exact pinned selector/runtime path must establish whether
that errno propagates, is retried, translated or suppressed. selectors.unregister
and stream.close are Python-call boundaries; evidence of a failing kernel
operation is not automatically evidence that either method raised. No current
runtime body or runtime inventory was read to fill this gap. Signals are not
substitutes for the requested read error: the collector's ordinary handler
returns after recording, and a signal can instead cause a different refusal or
a restarted operation. Killing a writer generally provides a candidate EOF, not
proof of an os.read exception.

F02's source ordering is precise. fail_pipe constructs the original error record,
stores it through failure before journal persistence, then calls close_pipe.
close_pipe pops the registered stream, independently tries unregister and close,
and records either failure in that order. The same-owner exact
RecordedPipeFailure token propagates the existing record; it is not a fresh
owned-body, independent-cleanup or census-tail primary. Census references use
the stored phase and monotonic_ns. Unrelated earlier errors remain first.

For runtime-selected I/O errors, no errno, class or message is invented in this
design. E_R, E_W, E_U and E_C denote independently observed read, write,
unregister and close exceptions respectively. A future observation must match
the actual class and the source's exact message projection (first 1024
characters, message_truncated flag and original_message_characters). The
overflow exceptions below instead have fixed literal messages. Actual record
timestamps and reference equality must be retained, not synthesized.

Successful focused evidence needs the real retained prefix and original writer
identity, successful required error persistence, no omitted error detail, and
independent after observations. A close failure cannot prove a prior read/write
failure. A failed journal or missing outer completion is retained as failure,
not treated as a passing targeted result. Additional genuine later errors remain
visible; the listed cleanup errors are an ordered subsequence, not a license to
erase others. If the selected pipe fault is to be first, evidence must also show
that no earlier error was present.

## Exact eight-variant findings

| Variant | Required actual boundary and ordering | Concrete missing premise |
| --- | --- | --- |
| F02-1-UNREGISTER | os.read on the registered child stdout pipe raises E_R; selector.unregister on that same stream then raises E_U; close still attempted. pipe-read-child-stdout precedes pipe-unregister-child-stdout. | A source/runtime-bound external mechanism for both exceptions, with independent Python-boundary evidence; an injected errno, closed fd or selector label alone does not establish the second exception. |
| F02-1-CLOSE | Same real read failure, independent unregister attempt, then stream.close raises E_C. pipe-read-child-stdout precedes pipe-close-child-stdout; any extra unregister error is retained. | Exact read/close targeting and exception propagation, without confusing another process's descriptor number or a sink-file close with the child pipe. |
| F02-2 | Sink.append retains a real positive os.write prefix on stdout.log; a subsequent write raises E_W; unregister and pipe close raise E_U then E_C. pipe-write-child-stdout is first absent an earlier error. | A selectively bounded short-write-then-error mechanism plus both genuine Python cleanup exceptions; no direct edits to bytes/hash/written counters and no filesystem-wide exhaustion that invalidates required journals/custody. |
| F02-3 | Real child stdout supplies 8388608 bytes plus one; capture retains the exact prefix and first excess byte. CollectionFailure / pipe-overflow-child-stdout / stdout exceeded independent 8-MiB capture ceiling precedes E_C at pipe-close-child-stdout. | An admissible unchanged-subject producer of that extra byte and a separately witnessed close failure. The normal RI136 envelope is checked against the cap before it is written. |
| F02-4 | Real ps stdout exceeds the current positive joint stdout/stderr raw quota by one; permitted prefix is retained. CollectionFailure / pipe-overflow-ps-stdout / census raw metadata capacity exceeded; partial bytes retained precedes E_U then E_C. | Genuine ps output and genuine dynamic quota history satisfying this exact boundary inside 250 ms, plus both Python cleanup failures. No supplied ps output or edited quota/journal counters. |
| F02-5 | A real read raises E_R during census's finally-tail pump, followed by the proposed close failure E_C. The earlier census error E_0 remains first; pipe-read-ps-stdout is recorded once later and referenced, not relabeled census-tail-pump. | Independently witnessed earlier census failure, incomplete helper/pipe state and actual tail-call location; selective read/close failures within the original remaining tail. A generic pump failure does not prove this branch. |
| F02-6 | Actual os.read returns b''; stdout eof is set; unregister succeeds and pipe close raises E_C. pipe-close-child-stdout is the primary absent an earlier error; no fail_pipe token or read/overflow error. | Natural EOF plus an exact externally controlled/witnessed close exception, with evidence of the successful unregister and genuine zero-byte read. |
| F02-7 | Actual os.read returns b''; unregister and close return normally. EOF remains true; no F02 primary or propagation reference is generated. | No fault supplier is needed for source reachability. An independent real zero-read and method-return witness, authentic admission, a real live-leader sample and full unchanged monitoring/custody still need a concrete feasible design. |

The JSON records entry_preconditions and first_reachable_refusal separately for
every row. Each proposed target is downstream of actual bootstrap, immutable
inputs and before-custody, original process/descriptor registration, and earlier
ready-key processing. pump first checks recorded interruption and its original
deadline, then calls selector.select; refusal or exception there does not prove
the later os.read/write/EOF boundary. Their exact source messages are retained in
the per-row map rather than pretending the desired injected fault is the first
reachable failure. F02-3 additionally identifies the dispatcher output-cap
refusal before normal oversized output. F02-4 identifies no-time, Q<=0,
preparation-deadline, signal and helper-timeout refusals before raw overflow.
F02-5 identifies its necessary actual earlier E_0 before the tail target.

Selected cleanup faults are not a license to erase additional actual failures.
F02-1-UNREGISTER requires an independent close attempt, not successful close.
F02-1-CLOSE, F02-3 and the proposed close alternative for F02-5 likewise retain
an extra unregister error if it occurs rather than silently demanding success.
The designated faults must still occur. F02-6 explicitly requires only a close
failure after clean EOF and therefore does require successful unregister;
F02-7 requires both normal returns. Unexpected additional errors remain in the
actual history even when they prevent the stipulated isolated case from being
established.

### Child overflow is a producer constraint, not just a timer problem

RI136 execute_one constructs one canonical envelope, checks
len(raw) <= LIMITS['output_bytes'], then writes and flushes it to one stream.
Its normal checked envelope therefore cannot itself cross the collector's
8388608-byte bound. Selecting one of the unchanged 77/62 cases supplies no
padding/repetition interface. This finding does not prove that every possible
compound error path and subsequent stderr diagnostic concatenation is below
the cap; no such universal bound is asserted. A proposed exceptional route would
need its own exact unchanged-source derivation and independent byte provenance,
not an assertion that sufficiently much output might occur.

A substitute chatty child, extra writer, repeated envelope, altered case, forged
read return, lowered output ceiling or changed subject globals would answer a
different question. None is authorized evidence for F02-3. The minimum missing
premise is a demonstrated producer path under the existing subject/stream
contract; if that cannot exist, a changed workload would require new owner
authorization and must not count as this unchanged-subject qualification.

### Census overflow is not a supplied ps fixture

The collector invokes exactly /bin/ps -axo pid=,pgid=,rss= with the fixed
environment and genuine helper identity. Before each census it derives

    Q = max(0, floor((events.limit - events.written - 65536) / 16))

events.limit is 66060288 bytes. The combined genuine ps stdout/stderr must cross
that current positive Q, and the controller must prove the relevant event-writer
history rather than insert Q. At zero remaining journal bytes consumed, the
formula would give 4124672; the actual launch/event bytes reduce it. There is no
claim that a real machine's ps output reaches any particular value.

Q <= 0 instead raises no metadata capacity for census before Popen and never
qualifies this overflow branch. Earlier journal exhaustion, timeout, malformed
rows or stderr failure may likewise stop a proposed route first. A sufficiently
large genuine host process population or sufficiently consumed legitimate
journal is only a candidate condition: no source-bound construction within
the unchanged sample, time, RSS and metadata budgets has been demonstrated.
Spawning unrelated processes or filling journals to force it is not silently
admitted by this note. Altering ps output, counters or the fixed command is not
an independent census witness. Census preserves its allowed raw prefix; unlike
child overflow it has no dedicated first-excess-byte field. That byte would
require independent actual read-boundary evidence, not a newly invented receipt.

### Census tail has an earlier first cause

Normal census loop completion requires the helper already polled complete and
both ps EOF flags true. Such a completion does not enter the tail pump. The
proposed F02-5 instantiation therefore needs a prior census-body failure while
the helper or pipe remains incomplete. The body catch records E_0 before the
finally block kills/drains the helper. For example, an actually observed bounded
helper timeout could be that antecedent; no timeout was induced here.

The tail pump must then reach its actual os.read, not fail earlier on a recorded
ordinary signal, exhausted deadline, selector call or already-closed pipe.
E_R is later than E_0, before its own cleanup error; the event reference identifies
E_R's existing phase/time. Requiring the tail read to replace E_0 as first would
test the wrong behavior. This is a source deduction, not a newly observed fault.

## Minimum continuation boundary

No controller code, host fault provider or generic launcher is supplied. A
future proposal must solve the per-row producer/operation/witness gaps, bind any
new external supplier as an explicit bootstrap dependency, and preserve every
old subject byte, catalogue, environment, privilege/custody premise and bound.
It must also explain its own authenticated bounded evidence and cleanup without
using the subject's claimed error as independent proof. Unsupported kernel or
runtime behavior is a missing premise, not an assumed feature of a debugger.

The fixed bounds remain parent 840 s; child 120 s including the 2 s cleanup
reserve; census at most 250 ms and remaining deadline; 512 MiB sampled group
RSS; intended 50 ms sampling; 8 MiB independently per child stream; and 64 MiB
auxiliary storage with the original narrower subdivisions. No handshake,
hidden hold, retry, synthetic sample, relaxed success test or replacement
workload is authorized. Natural fast EOF can still fail live-leader sampling.

Only plain source, administrative metadata and opaque selected-file identities
were inspected. There was no subject/helper/control import, compile, AST, probe,
runtime capture, fixture/controller construction, card/admission, target/fault
execution, scientific-body decode, repository/index or Git operation. The
additional minimum premises are requests for future decisions, not assertions
that those decisions or facilities already exist. The named blocked boundaries
and the source-feasible clean EOF candidate complete this feasibility sitting.
