# RI140 F01: recoverable launcher sink acquisition

Status: **source repair proposed for independent review; not execution admission**.
This note describes source paths, not observed signal delivery, file creation,
closure, custody success, or policy outcomes. No launcher, helper, control, fixture,
interpreter bootstrap, runtime inventory, or scientific target was executed.
No active operational cards or attempts were created. RI138 remains unchanged.

## Scope and selecting decisions

The selecting sealed review is
`ri138-launch-independent-review-6xGu5oak/INDEPENDENT_SOURCE_REVIEW.md`, its JSON
companion, and `HANDOFF.json`. The root disposition is
`ri139-root-bootstrap-adjudication-goau3dIc/RI138_ROOT_ADJUDICATION.json`, supported
by `RI138_ROOT_SOURCE_REVIEW.md`. All were read completely. The additional
`ROOT_SOURCE_REVIEW.md` in the same root directory was also read; its distinct
bootstrap subject is not promoted into launcher acceptance.

F01 identified a real source-level ownership gap: the former sink constructor
opened the marker before completing initialization, returning the object to its
caller, or invoking the phase-owned callback. An ordinary signal or initializer
failure in that interval could leave a real marker and descriptor while the
caller still held `sink=None` and `Phase.owned=False`. That route could omit both
independent sink close and the owned phase's complete after-custody attempt.

This author's exclusive outputs are this note and the new
`ri140-native-failure-repair-source-l_a4mna0/launch_policy_case.py`. F02 process-pump
failure ordering, packet manifests, full correspondence, and prospective
qualification design belong to their assigned authors. This note neither edits
nor independently accepts those artifacts.

## Complete-source identities

The copied predecessor is
`ri138-native-external-launch-source-92pbd52w/launch_policy_case.py`:
982 lines, 57,622 bytes,
SHA256 `670232ab5da7b2efa63d703c6fbd38fa088ff758d9d4dea129ac62845aab6ab9`.

The proposed new complete launcher is 1,040 lines, 60,009 bytes,
SHA256 `a0526720e530caa529499ff4d6e9e9794462fb50a1975232eb229e37d683828d`.
It was initially copied verbatim using `apply_patch`, then changed by explicit
patches. The full text diff was read; no target-source parsing, import,
compilation, instrumentation, probe, or execution supplied this identity.

The RI140 subject-manifest pin was independently checked as opaque metadata:
26,029 bytes,
SHA256 `25a694353f782aa3d6c50f925981b5403a5da28308676930256b420c110f192c`.
The RI140 dependency manifest is 699,052 bytes,
SHA256 `bd04d9013a543e63eb3db2488156c9c1c22333c48b68bdbce2ffcb9e33461544`;
the declared current closure has 423 entries. None of those statements claims
that current runtime or history objects have been observed.

## Narrow acquisition mechanism

`DurableSink.__init__` now acquires no resource. It initializes its path,
deadline, `fd=None`, byte count, SHA256 accumulator, and closed flag before
checking time and the parent path. A failure anywhere in this constructor cannot
create a new evidence file. Its caller receives the initialized object and stores
it in the local `sink` variable before invoking `sink.acquire(...)`.

`DurableSink.acquire(owner=None)` checks time and single-acquisition state, then
enters `AcquisitionSignals`. Only the exclusive `os.open`, descriptor assignment,
and direct phase ownership assignment are inside this short transition. Its
`finally` assigns `owner.owned=True` exactly when a descriptor has been registered
and an owner was supplied. The only marker caller passes the existing `Phase`
object directly. The former arbitrary callable parameter is removed; there is
no fallible callback moved outside protection and no delayed ownership recovery
that depends on returning a receipt to `Phase.claim`.

The constructor/open split is applied to both acquisition call sites:

- `write_new` stores the initialized sink, then calls `acquire(owner)` before
  appending bytes. Its ordinary exception receipt and independent close remain.
- `Phase.observe` stores the initialized sink, then calls `acquire()`. Any
  constructor/acquisition failure selects the failing journal callback, but the
  complete frozen observation inventory is still passed to `observe_all`.
  A known acquired descriptor is independently closed even when acquisition
  ended by an ordinary deferred interruption.

The `Phase.observe` acquisition try also has its own `finally` hard-unwinding
guard. A hard abort there, before entry into the later observation try/finally,
best-effort closes its already known fd and immediately propagates the same
BaseException. That guard also covers a hard abort during acquisition-error
handling. It performs no fsync, receipt persistence, observation, or completed
tail claim.

All close routes now require both an available sink and a registered descriptor.
Thus a genuinely failed exclusive open has no owned resource, no fabricated
close identity, and no new phase ownership. An acquired zero-byte marker has a
real original writer identity through the unchanged close logic; it is not
misrepresented as a successful marker write.

## Signals and first failure

The new `ACQUISITION_SIGNALS` global names only the current nonnested acquisition
context. The context holds `deferring=True` and a single pending `Refused`
exception object. Every delivered signal is still appended to `SIGNALS`.
`SIGALRM` is checked first and raises `HardDeadline` immediately, before any
ordinary-signal deferral or primary-preservation logic.

During acquisition, TERM/INT/HUP record the first pending exception but do not
raise while `deferring` is true. The same exception object is retained for later
repeated ordinary signals. After fd and owner registration, `__exit__` changes
`deferring` to false inside its own `try/finally`. With no original exception it
raises that exact pending object via `interrupt()`. Its `finally` clears the
active context. If a signal lands after the flag is cleared but before the
context is cleared, the handler uses the same pending object, not a newly
invented later primary.

An original exception leaving the protected body takes precedence over pending
ordinary signals. `ACQUISITION_PRIMARY` identifies exactly that object, or the
pending interruption object raised by `interrupt()`. While the context is active,
ordinary signals do not replace an already active body exception. After context
clear, the handler suppresses an additional ordinary raise only when
`sys.exc_info()[1] is ACQUISITION_PRIMARY`. The sentinel can retain a reference,
but has no suppressing effect when no exception is active or when a different
exception is active. Unrelated exception handlers keep the predecessor's
immediate ordinary-signal refusal; there is no blanket exception-unwinding
exemption. This narrow exact-object rule protects acquisition error handling
across context clear. All recorded signals still prevent success at the existing
phase checks.

Relevant interleavings, as source deductions rather than executed controls:

| Point of interruption or ordinary failure | Source route |
| --- | --- |
| Before or during nonacquiring constructor | No new file/fd; marker phase remains unowned. |
| Truly failed exclusive open | `fd` stays `None`; no owner assignment or fabricated close receipt. Original open failure remains primary even if an ordinary signal was pending. |
| Successful open before fd assignment completes | Ordinary handler records and returns; assignment proceeds before scope exit can raise. |
| Known fd before direct owner assignment | Ordinary handler records and returns; protected `finally` assigns the phase owner. |
| Ordinary failure after fd registration within the protected body | Local sink already exists; owner recovery runs before exit preserves the original error. |
| Pending signal at context exit or another signal during exit | The same first pending exception object is raised only after fd/owner recovery. |
| Another ordinary signal while handling that acquisition primary after context clear | The additional signal is recorded; exact-object preservation does not replace the primary. |
| First marker append/fsync failure | Phase is already owned; original writer close is attempted, failure propagates through `Phase.claim`, and the unchanged owned-phase route attempts full after custody. |
| First marker close/readback failure | Independent close stages and receipt errors remain; phase is already owned and cannot become a successful run. |
| Journal acquisition failure in an already owned phase | The failing sink callback does not suppress the frozen inventory; any known acquired fd is closed independently. |
| SIGALRM at any point | Immediate `HardDeadline`; no budget extension, fabricated completed after-tail, or conversion to an ordinary failure. |

No claim is made that arbitrary repeated signals, process termination, memory
exhaustion, or an uninterruptible kernel operation permit all cleanup to finish.
In particular, a hard alarm between kernel fd creation and Python fd registration
can leave an unregistered resource until process exit. The hard-abort route can
only best-effort close a descriptor it actually knows. That is the preserved
immediate-hard-watchdog boundary, not an ordinary acquisition loophole or a claim
of complete evidence. Genuine outer tool completion and independent review remain
required.

## Exhaustive changed source regions

Line spans below refer to the complete identities above, inclusive. Full-file
delta/correspondence artifacts are coordinator-owned; these span descriptions are
not substitutes for their complete byte comparison.

| Region | RI138 span | RI140 span | Change |
| --- | --- | --- | --- |
| Opening docstring and packet constants | 2; 22; 25–26 | 2; 22; 25–26 | RI140 description/reservation and new immutable manifest bytes/hash. |
| New globals | absent | 50–51 | `ACQUISITION_SIGNALS`, `ACQUISITION_PRIMARY`. |
| `close_on_abort` | 75–81 | 77–83 | Excludes unacquired `fd=None` sinks. |
| `signal_received` | 126–130 | 128–144 | Recorded acquisition-only deferral and exact acquisition-primary preservation; immediate SIGALRM unchanged. |
| `AcquisitionSignals` | absent | 218–245 | New nonnested acquisition scope, stable pending exception, exact-primary sentinel, protected exit/clear. |
| `DurableSink.__init__` | 206–211 | 250–255 | Preinitialization only; open moved out. |
| `DurableSink.acquire` | absent | 257–267 | Exclusive open, fd registration and direct owner registration in protected transition. |
| `DurableSink.append_bytes` | 213–227 | 269–283 | Existing unavailable/closed-write guard also requires a registered fd; existing message retained. |
| `write_new` | 252–268 | 308–323 | Owner reference replaces private callback; local sink before acquire; close only known fd. |
| `authenticate` | 304–422 | 359–478 | Current HANDOFF schema, repaired predecessor lineage, current closure count/message only. |
| `Phase.claim` | 456–465 | 512–519 | Passes `self`; deletes former ownership callback. |
| `Phase.observe` | 468–496 | 522–554 | Explicit acquire, acquisition-boundary hard close/rethrow guard, failing callback on any acquisition error, fd-aware independent close. |

No import changed. `DurableSink.__call__` and `close`, `Phase.finish`, card
creation, preparation reconciliation, exact child envelope checks, process
artifact collection, `run_phase`, `main`, and the terminal wrapper are unchanged
text. The retained terminal label `RI138 LAUNCH REFUSAL` and retained RI138 wire
schemas are compatible protocol labels, not current-source identity claims.

## Minimal lineage adaptation and unchanged limits

The current packet HANDOFF schema is
`ri140-native-failure-repair-source-handoff-v1` with the existing eight-field
shape and source-only status/scope. Its `predecessor` is compared to
`manifest['repair_ancestry']['predecessor_source_handoff']`, the immutable RI138
source HANDOFF (5,173 bytes,
SHA256 `6ee043592352d35048bb31a34aa8b550bb830a9af2afc99170db14b3806510e0`).
The scientific policy dispatcher's source HANDOFF remains the distinct RI136
object. No current self hash is embedded in the subject manifest or source;
genuine external root authentication continues to pin the complete current
HANDOFF and launcher before dispatch. No new cyclic ROOT_DISPATCH digest argument
is introduced.

RI138 root-plan, prepare/run, observation, marker, result and custody schemas are
retained. The accepted 77 native/62 audit RI134 pure-policy subjects and their
exact RI136 dispatcher remain unchanged. No old narrow controls, whole-entry
cases, production/scientific entry, or broader qualification are admitted.
The 423 closure replaces only the old declared 396 closure count and refusal
message; runtime/history expectations are not rebaselined.

The final one-entry addition is the separately root-authorized collector startup
scope in `ri142-portable-focused25-net0j999/RI140_STARTUP_SCOPE_ADDENDUM.md`,
1,715 bytes,
SHA256 `8a6259d9fb2bc0597de215fd8f51a77ab228a6dc1e053fda3ba96643310d9008`.
It is bound by `repair_ancestry.startup_scope_addendum`. The process-helper author
implements that related F01 handler-order change; this launcher author changed
only the final manifest pin/count for that addition and makes no independent
acceptance claim about the helper.

The fixed limits are unchanged: child 120 seconds, 512 MiB RSS, 8 MiB output,
64 MiB auxiliary metadata, 50 ms sampling and 250 ms ps timeout. Metadata,
before, after and final phase budgets remain 60/300/300/60 seconds with an
840-second launcher watchdog. This launcher component adds no retry, timer reset,
signal masking, sleeping, process launch, new trust root, or cleanup budget.
Root separately authorized narrowly scoped TERM/INT/HUP masking in the process
helper's startup/handler-restoration transition. That distinct author-owned
mechanism must never mask SIGALRM; it is not implemented by this launcher.

## Remaining obligations

Independent source review must decide whether this bounded repair resolves F01;
the author makes no acceptance determination. Coordinator-owned prospective
qualification must distinguish genuine preownership failure from a created
marker, exercise the acquisition and first-failure interleavings, retain actual
tool history and incomplete failures, and stop under its separately authorized
attempt cap; the coordinator-owned focused prospective qualification design is
authoritative for that cap. This note implements no test controller or fault injector and
records zero executed cases. Only later explicit root admission can authorize
any operational preparation or run. Even a later successful pure-policy case is
not complete caller qualification or a quantum, geometry, gravity, or empirical
result.
