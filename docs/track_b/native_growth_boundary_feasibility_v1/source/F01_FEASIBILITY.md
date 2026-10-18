# RI143 F01 boundary feasibility: 23 unresolved variants

Disposition: **BLOCKED_DESIGN_SOURCE_ANALYSIS_ONLY**. All 23 expanded F01
variants from the accepted RI140 focused design are retained. This means no
justified available unchanged-subject mechanism under the present premises;
it is not a theorem that these observations are impossible on every platform.
There are no executed cases, controller, fixture, operational card, runtime
capture, source repair, changed subject globals, or new execution admission.

The exact per-variant inventory is [F01_BOUNDARIES.json](F01_BOUNDARIES.json).
Each row separates source location/state, independent boundary/fault/consequence
evidence, first/later cause, a concrete conditional mechanism, current blocker,
minimum extra premise, and an invalid shortcut. Candidate mechanism is not
available mechanism. Every row has `available_mechanism_established=false`,
`executed=false`, and `passed=false`.
Every row also specifies `entry_preconditions` for the whole unchanged prepare
or run entry and `first_reachable_refusal`, distinguishing the actual first
raise/record from earlier nonqualifying guards. No ordinary refusal is presumed
to occur naturally merely because a candidate fault is described.

## Authority and reading boundary

The complete selecting root decision and root review were read:

- `/Volumes/AI_DATA/development/det-review-evidence/ri140-root-source-adjudication-8796wh9l/RI140_ROOT_ADJUDICATION.json`:
  5,028 bytes, SHA256 `c6611c3e7ae4d915dbef12d37cafcbd9ec714eb76a66fb84815a9ed2968b0481`.
- The adjacent `ROOT_SOURCE_REVIEW.md`, whose declared identity is 3,887 bytes,
  SHA256 `2ec34c80d5853bc9cdf9b6e1c1e3c707c8a7b70fc7cb2171aabb5acf8a1c0e08`.

The complete HANDOFF, Markdown review and structured review in
`/Volumes/AI_DATA/development/det-review-evidence/ri140-independent-source-review-i57s4u4b`
were also read. Their review is source acceptance with prerequisites, not a
passed fault campaign. Root explicitly assigned RI143 boundary feasibility and
retained `execution_admitted=false`, zero focused/policy executions and no
qualified controller.

The unchanged accepted sources were reviewed previously in full during authoring
and author-peer review. This sitting reread the exact relevant source paths with
line numbers and rechecked these complete opaque identities:

| Artifact under the immutable RI140 source directory | Bytes | SHA256 |
| --- | ---: | --- |
| `launch_policy_case.py` | 60,009 | `a0526720e530caa529499ff4d6e9e9794462fb50a1975232eb229e37d683828d` |
| `owned_process.py` | 43,838 | `4b2bd7b5bc62ac9de021ee1b85e07a97cccb63a560916b518371ea1fdf2126da` |
| `FOCUSED_QUALIFICATION_DESIGN.md` | 8,969 | `d7be9dec61b3588af4e271afe4bfaea60060a4b6486f7cf229c60e3f33401107` |

The source directory is
`/Volumes/AI_DATA/development/det-review-evidence/ri140-native-failure-repair-source-l_a4mna0`.
The complete focused design was read in this sitting. No fresh full reread of
unchanged custody is claimed, and no host/runtime inventory or source import,
compilation, AST pass, probe, execution or scientific decoding occurred.
Authorship of the launcher and prior peer review of the collector are disclosed;
this is not independent acceptance of either source.

## What an actual boundary witness must distinguish

An open has several different milestones: kernel success and returned fd,
Python assignment into `sink.fd`, assignment into `Phase.owned`, and, in the
collector, insertion into `owner.sinks`. A successful open trace or a new
directory entry proves none of the later Python-state predicates by itself.

Signal send, OS pending state, low-level delivery and execution of the Python
handler are also distinct events. The source only describes its Python handler's
actions. A source line spans multiple operations; a source-line breakpoint is
not evidence of an exact inter-operation interval. Even a nonpatching hardware
instruction stop and a successful OS send do not establish that this pinned
interpreter has a legal evaluation/signal-checkpoint opportunity to run the
Python handler before the next store. That additional runtime premise is
explicitly missing for F01-1 and F01-2. Artificially calling the handler would
test a different mechanism.

Any future qualifying witness must bind its actual process/thread, pinned runtime
and instruction map, relevant object/fd identity, named operation and event order.
It must show when actual handler execution occurred, rather than deduce timing
from a planned sleep or the subject's error text. No debugger, tracing facility,
permission, attach entitlement, checkpoint behavior or operating-system fault
API is asserted to be installed, available or qualified here. Nonpatching
observation is a requested capability, not an implementation.

Observer time, suspension and evidence volume stay inside the existing limits.
Pausing the subject does not pause its wall deadline. A software breakpoint that
rewrites subject/runtime code, injected callback, global replacement, fabricated
successful receipt, interpreter replacement, interposed Python function, or
changed accepted argument is not an unchanged-source qualification route.
Any proposed external supplier requires explicit root admissibility and genuine
bootstrap/custody; a label such as "debugger" creates no exemption.

## Exact design expansion and conditional mechanisms

The following table groups only identical parameter expansions. The JSON retains
23 independent rows, not 15 combined passes. Each row remains unresolved.

| Design group | Variants | Exact target and minimum additional capability |
| --- | ---: | --- |
| F01-1 | TERM, INT, HUP: 3 | Launcher line264: successful open before `sink.fd` store. Need actual open/fd evidence, read-only instruction/object mapping and proof of an actual Python callback at a legal checkpoint before that store. |
| F01-2 | TERM, INT, HUP: 3 | Launcher lines264–267: fd stored, owner not yet stored. Need the same actual callback proof between the two distinct state writes. |
| F01-3 | 1 | Two actual ordinary callbacks spanning deferral/exit, with one exact pending exception object preserved. Conditional representative is TERM during acquisition and INT while that acquisition primary is active across context clear; later admission must fix and observe it. |
| F01-4 | 1 | Marker open genuinely fails while an ordinary callback is recorded in that failed acquisition. Need real operation/error provenance, no-fd evidence and callback chronology, not a fake OSError. |
| F01-5 | 1 | Safe nonacquiring constructor initialization fails before open. Representative is actual accumulator initialization failure at launcher line253. Need a selective genuine allocation/library fault and absence-of-open evidence; no such supplier is established. |
| F01-6 | 1 | First marker write at line276 fails, then actual independent close at line293 fails. Need selective paired operation faults and fd/order evidence; one persistence error cannot establish both. |
| F01-7 | 1 | BEFORE journal open fails after phase ownership. Conditional real collision after initial namespace validation requires a timed operational filesystem action; independent per-row observation evidence is also needed because the journal itself is unavailable. |
| F01-8 | 1 | Current phase marker exists at O_EXCL open but not at earlier namespace observation. Need independently proved post-namespace insertion and unchanged original marker evidence. |
| F01-9 | 1 | Actual SIGALRM handler during acquisition. Representative is after known-fd registration but before owner assignment. Need actual handler state and alarm provenance; only incomplete best-effort hard cleanup is expected. |
| F01-10 | TERM, INT, HUP: 3 | Collector's first Sink is `process-errors.jsonl`: successful open before dictionary registration at line693. Need actual record-only callback in that interval and subsequent same-object registration; a callback while still startup-masked is another case. |
| F01-11 | 1 | SIGTERM installation succeeds, actual SIGINT installation fails at line688 before resources. Need a selective actual installation fault; blocked/noncallable parent guards occur earlier and cannot replace it. |
| F01-12 | 1 | All four startup sinks registered; directory fsync at collector helper line121 fails through line697, and the directory's own close succeeds. Need exact fsync-failure and successful-close evidence, not a file fsync or earlier open failure. |
| F01-13 | 1 | Ordinary finalization error actually escapes before restoration. Conditional representative is unguarded receipt-allocation failure at entry to `Sink.close` from `Owner.save` line623 during report finalization. Need a genuine selective runtime failure and an escaped-exception trace; caught I/O receipt errors do not establish escape. |
| F01-14 | TERM, INT, HUP: 3 | Signal becomes OS-pending after first saved handler restoration but before all attempts finish, while ordinary signals remain masked. Need actual mask/pending/handler observations, followed by original-mask restoration and actual late outcome. |
| F01-15 | 1 | Actual SIGALRM callback during ordinary-mask transition. Representative is startup after saved mask registration and before all handlers install. Need independently observed eligible SIGALRM, actual callback and unchanged watchdog state. |
| Total | 23 | No available mechanism or executed case is established. |

The representative choices locate previously generic one-attempt design slots;
they do not broaden coverage or claim all possible initializer, finalization or
hard-abort boundaries. Root must select any later operational representative,
and missed/unreachable variants stay unresolved without automatic retries.
This sitting does not replace any of the eight separate F02 variants or add a
32nd case to the 31-attempt design.

## The existing-marker trap is an earlier guard, not a passed open test

`run_phase` calls `namespace` at launcher line961 before `state.claim` at line965.
The former requires the exact initial name set at line347. A PREPARE_STARTED
marker seeded before a prepare invocation, or RUN_STARTED seeded before its run,
therefore produces `Refused: operational namespace has absent/unexpected
artifacts`, not the intended marker `os.open` failure. During run, the earlier
PREPARE marker is expected but is not the current RUN marker being tested.

The only concrete unchanged-source filesystem candidate identified here inserts
the current phase marker after a proved successful initial namespace observation
and before the genuine exclusive open. The external creation is an explicit
operational mutation needing later root authorization, not an action taken now.
A deterministic post-check boundary witness and independent before/after marker
identity are absent. A naive preseeded-marker experiment would test a different
guard and must not be counted as F01-8.

The same earlier-guard issue applies to a preseeded observation journal and to
permissions/path changes made before authentication. The design cannot silently
skip namespace or bootstrap to make its intended failure reachable.

## Fault provenance, original error and missing journals

Natural failed operations, faults caused through a real external host action,
and substituted operation results are different provenance classes. A supplied
errno cannot be called an observed natural host failure. Permission changes
are not presumed effective for the actual execution identity. Global disk or
memory exhaustion is not a selective fault: it can fail earlier authentication,
evidence persistence or unrelated operations and does not establish the intended
boundary. No selective host-fault or allocation-fault supplier has been admitted.

F01-12's chosen isolated fsync representative additionally requires the directory's
own `os.close` to return normally. Collector `directory_sync` uses an unguarded
`try: os.fsync(fd)` / `finally: os.close(fd)` at lines119–123. If that close also
raises, its exception replaces the propagated fsync exception and may be the
one recorded as `owned-body`; the source does not independently record it later
while preserving fsync first. Such a compound failure must be retained with its
actual external chronology, not credited as the selected isolated fsync-first
case. This feasibility correction changes no accepted source or design count.

For F01-4, `write_new` captures the original open exception in its local receipt;
`Phase.claim` then raises `Refused` containing the receipt errors because no phase
was owned. There is no owned `first_error` artifact or complete after journal
promised on that route. The terminal wrapper can truncate text. Independent
external evidence must preserve the actual failing operation and original
exception details; absence of a journal is not permission to invent one.

For F01-3, at least two actual Python handler entries and the exact pending/active
exception identities must be witnessed. Multiple signal sends may coalesce or
be handled outside the target state. A second ordinary signal received after
the acquisition primary stops being active does not prove the protected
exact-identity case. An unrelated earlier error always remains first.

For F01-6, the originating append error and later close error need separate
actual operation witnesses. For F01-7, the failure of the journal leaves no
durable per-object ranges; the unchanged source summary alone is not independent
evidence that every original frozen object was attempted. A bounded external
per-row observation/operation witness would be needed without changing or
reloading the original expectation set. No performance feasibility within the
existing 300-second phase and evidence caps is established.

## Masked pending state and hard alarms

F01-14 requires pending membership during the interval between restoration
attempts, not merely a signal sent around that time. The code's first pending
snapshot precedes the loop; the second at collector line819 follows it while
still masked. A qualifying witness must independently locate the intervening
pending arrival and subsequent actual observation/delivery. Pending records are
not `received_signals` callback records. A restored-parent exception can occur
at unmasking, after all handler attempts, and that is a distinct later event.
The earlier PROCESS_REPORT/PROCESS_CLOSE files remain provisional; actual
post-restoration return or exception plus genuine outer completion are required.
For the selected late-pending trace, the source constructs the pending-observation
CollectionFailure before unmasking without raising it immediately. A restored
parent Refused may first be thrown at unmasking. The later recording loop stores
the pending observation before that handler exception unless an earlier first
error already exists. First constructed, first raised and first recorded are
therefore explicitly distinguished in the per-row refusal fields.

Only the pinned raising parent and initially unblocked ordinary signals are
supported. An initially blocked or noncallable parent fails before the intended
startup resource acquisition; that refusal is not F01-11 or F01-14. Host mask or
handler failures remain refused/incomplete best effort, not a guarantee that all
tails finish. These source obligations do not acquire new executed coverage from
this finite map.

A genuinely delivered external SIGALRM can exercise the existing hard handler
for F01-9 or F01-15, but it does not prove the 840-second timer naturally expired.
The signal source must be named and admitted. Neither timer reset nor extra time
is authorized. The hard path preserves only recoverable best-effort actions and
honest missing evidence; it cannot be graded against fabricated full after
custody. A process killed by an outer deadline is not automatically evidence of
the Python HardDeadline branch.

## Minimum decision now

Keep all 23 variants blocked under the present premises. Root may evaluate a
specific nonpatching observation supplier, exact pinned-interpreter checkpoint
semantics, a narrowly authorized operational filesystem race, or selective real
fault supplier. Such evaluation must first establish the capability actually
needed for a row, with unchanged subjects and genuine original bootstrap/custody.
It must not treat a capability wish list as an implemented controller.

If a required checkpoint or fault cannot be reached under those constraints,
the row stays unresolved. No source/global rewrites, generic launcher, made-up
errno, invented callback, timing-based pass, relaxed bound, retry, substituted
scientific target or policy acceptance follows. The 31 focused cases, unchanged
139 policy outcomes, deeper native/audit work and scientific obligations remain
separate. RET stays paused.
