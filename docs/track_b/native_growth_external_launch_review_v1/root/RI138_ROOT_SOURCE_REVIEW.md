# Root adjudication of native RI138 failure paths

RI138 requires a new immutable F01/F02 source repair before launch admission.
This is a source rejection for operational use, not a new mathematical or
physical result. No native case, fault injection or scientific target was run.

Root freshly read the complete independent review and its disposition, the
review obligations, and the full relevant acquisition, phase ownership, signal,
pipe collection and first-error paths. The independent nonauthor review covers
all 2,364 lines across the three new modules; root does not relabel that coverage
as its own full manual reread. Current source and all 396 direct dependency
identities are separately reconciled. Inherited runtime expectations are pinned
history, not fresh observations of the candidate runtime.

F01 is independently confirmed in launch_policy_case.py. The ordinary signal
handler immediately raises Refused. DurableSink exclusively creates its file
before subsequent state initialization, before the constructor returns into
write_new's local sink, and before Phase.claim's callback sets owned. An ordinary
interruption in that interval leaves an acquired marker but can leave sink None
and owned False. The ordinary exception path then rethrows as preownership and
does not reach owned-phase finalization/after custody. Even successful constructor
return leaves a gap before the ownership callback. This is distinct from the
explicit hard-watchdog limitation. A failed open with no acquired resource must
continue to refuse as genuinely preownership.

F02 is independently confirmed in owned_process.py. The read, sink-write, child
overflow and census overflow paths call close_pipe before their primary cause is
recorded by the outer handler. close_pipe records unregister/close errors through
failure immediately, so a secondary cleanup error can become first_error. The
primary failure must be preserved before independent cleanup; propagation must
not duplicate or relabel it. A close error after ordinary EOF remains a possible
primary error when no earlier cause exists. Raw prefixes and overflow evidence,
both cleanup attempts and every resource ceiling must remain intact.

RI140 is the narrow successor: safe preinitialized sink/resource registration and
ordinary-signal deferral through acquisition/ownership; original-cause recording
before pipe cleanup; only necessary source correspondence, contracts and bounded
focused qualification design. The original RI138 packet remains immutable.
Fresh complete nonauthor review and root adjudication precede separate genuine
execution admission. No acceptance flag or tool-shaped local receipt creates
authority. Hard-stop incompleteness remains explicit; no deadline is extended.

The reviewer disclosed authorship of thirteen inherited WHITE provenance files;
their identities/references alone were checked. The reviewer did not author the
current native modules or their native ancestors. Two reviewer metadata-tool
failures are retained as failures. The compact V3 actual successful check supports
its stated direct-closure/reference census only; 112,276 external historical
reference occurrences were not dereferenced. Large redundant diagnostics remain
external and pinned rather than silently omitted or represented as passing runs.

All 139 native policy cases, the deeper 20/42 obligations and separate scientific
qualification remain open. Actual C2/C3 signs and shared H30 feasibility retain
their qualification/execution blocker. The next source repair actively serves
that native question; measurement work continues independently. RET alone remains
paused.
