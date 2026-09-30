# RI171 independent supervisor qualification source review

## Verdict and scope

**Require source repairs before qualification admission.** Five concrete qualification/oracle defects are set out below. They arise from the actual sealed call ordering and predicates; no supervisor, control, fixture or saved-case checker was executed to find them. All 92 controls remain unexecuted.

The subject is `/Volumes/AI_DATA/development/det-review-evidence/ri171-supervisor-qualification-source-zksymhs1/HANDOFF.json`, 14,569 bytes, SHA256 `b83a4588d780d552cbf665263a599e514e8c6944d41d3237bce1bd1180b01078`. Its exact 30-file namespace and 29 payloads were authenticated before reading and independently rechecked. In this report, source filenames and line numbers refer to that directory unless explicitly identified as the unchanged RI169 subject.

The reviewer did not author these five modules or the RI165/167/169 supervisor. I previously independently reviewed RI165 and have authored separate WHITE validator/caller/bootstrap material, as disclosed in earlier packets. Those roles confer no acceptance on RI171 or on its author's saved oracle. No source was repaired here. The sole writable reservation is `/Volumes/AI_DATA/development/det-review-evidence/ri171-independent-supervisor-source-review-fw3b83xu`. Root owns disposition, repairs, actual admission and publication. RET remains paused.

## F01 — caller read faults are injected into the observer, including false-positive transient coverage

**Blocking; high priority.** Anchors: `case_worker.py:71–77`, `case_worker.py:332–345`; unchanged RI169 `supervise_native.py:423–447`; `check_saved.py:212–226`.

`Instrument.read` selects any registered input tag ending in `:<target_stream>`. It does not distinguish `caller:stdout` from `ps:stdout`, or their stderr counterparts. In a whole case, the supervisor performs its first `process_snapshot` at line 428 before its first caller `drain` at line 447. Thus the one-shot read injection is consumed by an observer read.

The ordinary `S04.stdout.read`, `S04.stderr.read`, `S10.caller.stdout.unregister_close` and `S10.caller.stderr.unregister_close` cases then receive a ps-pump refusal wrapped as a supervision error. They cannot satisfy the intended caller-pump first error. For the compound unregister/close variants, the same suffix-only selection also consumes the cleanup injections on the wrong process's pipe.

More seriously, `S04.stdout.read_would_block.transient` and `S04.stderr.read_would_block.transient` can match their current saved oracle without exercising the intended caller read race. The first ps read raises the injected `BlockingIOError`; the unchanged observer treats it as transient and completes. The subsequent caller receives two ordinary 64-byte streams and ultimately the expected nonempty-stderr refusal. The saved oracle only counts one `RI169_READ_TRANSIENT` message, then separately looks for a caller 64-byte read. It never requires that the error event have the caller tag, or that the same pipe remain active from that error to the successful read. The recipe explicitly excludes ps substitution.

Required repair: bind each injection to the exact process role and stream declared by that case. The saved oracle must independently require the corresponding error tag and event ordering, and reject a ps-only transient as caller coverage. Preserve the explicitly observer-scoped controls; they should still target `ps:<stream>`. A repair should include prospective negative oracle checks for a correct message on the wrong role, without treating those source checks as executed qualification.

## F02 — late-observer case is shadowed by generic late-file handling

**Blocking.** Anchors: `check_saved.py:234–260`, `check_saved.py:305–308`; `case_worker.py:254–263`; manifest ID `S13.late_observer`.

The condition `f == 'nonzero' or f.startswith('late_')` precedes the dedicated `late_observer` branch. It requires the first error to be `caller/outer failed` and a reaped caller code of 7. But the actual named double refuses on the second observer call with `RI171_OBSERVER_FAILURE`; that is the intended first error and normally precedes the one-second payload exit. The dedicated branch at line 258 is unreachable.

There is a second independent routing problem: the shared late-file tail at line 305 also matches `late_observer`. It then demands a secondary stage named `observer:<stream>`, which the subject's observer/refusal path does not produce. Reordering only the earlier branch would not fix the case.

Required repair: use a closed set of late-file faults, excluding the observer case from both generic conditions. Require the exact second-call observer injection, a preceding successful real observation and the intended primary error. Keep unrelated earlier or later failures from earning this case's credit.

## F03 — ordinary failed cases can match with only a candidate receipt and an unrelated terminal exception

**Blocking; high priority.** Anchors: `check_saved.py:97–130`, `check_saved.py:234–247`; `case_worker.py:453–480`; `qualify_supervisor.py:94–113`; unchanged RI169 `supervise_native.py:570–580`.

The saved oracle initializes `receipt` from the traced serialization candidate. It compares the on-disk completion only if that file exists, and `whole receipt required` checks only that the candidate is non-null. For an ordinary expected-failed case, the generic result check requires only status FAILED and a nonempty error list. It does not require `report.return == 2`, `report.exception is None`, or the expected completed on-disk receipt.

For example, in `S03.nonzero`, the actual caller can exit 7 and produce the intended primary error. The subject then serializes its failed receipt candidate, but an unrelated receipt-creation, write or durability error can escape afterwards. The worker records that exception without marking it as its own worker error. The collector can consequently complete a capture. The saved oracle accepts the candidate as its receipt and the existing nonzero-caller primary/reap fields. A missing completion file skips the disk comparison; a full file with a failed fsync likewise is not rejected by this ordinary-case branch. The case can therefore match despite not completing its required ordinary terminal path.

This is distinct from the intentionally partial S11 receipt cases and S12/S09 hard escapes. Their explicit negative semantics must remain available; they cannot become a generic exemption for every expected-failed case.

Required repair: classify terminal outcomes per case. Ordinary failed whole cases must have their expected actual return, no unrelated escape, and a complete saved receipt equal to the candidate, with the applicable durability/tail evidence. Only specifically declared receipt/hard-escape controls may use the corresponding partial or missing artifact semantics. Missing fields and partials should remain preserved failures, not be deleted or converted into completed evidence.

## F04 — several inherited failure recipes lack their defining saved assertions

**Blocking coverage/oracle gap.** Anchors: `check_saved.py:297–318`, `check_saved.py:342–355`, `check_saved.py:389–394`; `case_worker.py:300–328`, `case_worker.py:370–375`.

The full inherited recipe objects are preserved byte-for-byte in the manifest, but preserving their prose is not implementing their complete oracle:

- The healthy-sibling exact-byte/EOF checks at lines 297–304 apply only to S04, S05.caller and S10.caller. They exclude the fallback and journal-failure families. For `S05.fallback.alive`, `S05.fallback.already_exited`, `S10.journal.alive`, `S10.journal.already_exited` and the two S13 kill-failure cases, the intended already-buffered healthy data can be missing while the current checker still sees the correct initial refusal, a failed receipt and an independently reaped caller. Capture pins authenticate whatever was saved; they do not establish the expected 64-byte streams. A subsequent capture-tail error does not itself make these case predicates fail.
- `S13.observer.kill_failure` and `S13.journal.kill_failure` do not require the named `RI171_KILL_FAILURE` injection or its `direct_handle_kill` secondary error. Their first-refusal/reap checks can match without the defining second fault. The source contains an injection, but the qualification oracle must establish it was reached.
- Negative ps I/O/registration/compound-close cases verify the first failure and sibling bytes/EOF, but do not require the observer's own reap result or the applicable original finish-deadline evidence. Fixture-owner recovery is not a substitute for the subject observer's bounded reap. The separately implemented fixed `ps_nonzero` and `ps_timeout` checks do require reaped=true; that does not cover the six I/O/registration/compound variants.
- Recovery classification merely filters the records that happen to be supplied. It does not reconcile one result for every `popen_acquired` handle, reject missing/duplicate identities, or require the separately created leaf's retained recovery obligation. An omitted recovery row can therefore remove an external obligation from the returned summary. This is a missing saved-record consistency check, not a claim that a sent signal proves absence.

Required repair: implement a finite per-case obligation map tying each defining injection, first/secondary error, expected healthy capture or explicit incomplete-tail state, subject reap and fixture-recovery identity to the corresponding trace/receipt data. Do not demand successful EOF/reap from the deliberately exhausted-budget/nonreap controls; require their specified incomplete evidence instead, without promoting it to successful cleanup. Reconcile recovery entries against acquired handles and leaf evidence. Preserve the root's genuine-origin and actual recovery responsibilities.

These are source-level false-pass paths, not newly fabricated or executed saved cases. Focused prospective oracle mutations can show that removing the defining fault, sibling data, required subject reap or a recovery row is rejected before genuine qualification is attempted.

## F05 — the stderr hash-drift case changes size instead

**Blocking the claimed distinct hash-drift coverage.** Anchors: `inert_payload.py:117–125`; `case_worker.py:137–154`; `check_saved.py:305–307`; manifest IDs `S10.stderr.drift` and `S10.stderr.size`.

The payload emits stderr only for its named S04/S05/S10.caller/S10.journal/S13 families or the plain stderr case. The fault string for `S10.stderr.drift` is `late_drift`, so its initial stderr file is empty. The mutation then writes `Q` at offset zero. This grows the file from zero to one byte. The separate size case also writes one byte to that initially empty stream. The drift case therefore does not isolate unchanged-size content/hash drift; a readback implementation checking size alone could reject both.

The saved oracle checks the common readback-mismatch stage but not that the drift was same-size or that the expected mutation was reached with the intended precondition. The stdout and process-journal drift controls have nonempty data and do not have this particular empty-file problem.

Required repair: arrange a nonempty deterministic stderr prefix for the drift case while preserving the original intended first error, and check the before/after length equality plus exact byte/hash mutation. Keep the size variant's length change distinct. No new supervisor or broader launcher design is needed.

## Full reviewed coverage and retained strengths

All five complete modules were read: protocol 164 lines, controller 122, worker 485, inert payload 129, saved checker 410, totaling 1,310. The entire unchanged RI169 supervisor, 588 lines, was read as source. The full 92-case manifest, thirteen groups, 34 inherited recipe objects, protocol, schemas, invocation, author record, actual administrative-check records, current metadata checker text and declared metadata output were read. An overbroad combined display was truncated; all required manifest ranges were subsequently read in bounded chunks. No truncated display was credited as a complete read.

The remaining coverage was examined as follows:

| Group | Review scope |
|---|---|
| S01–S03 | Healthy ordinary capture, actual separate timer observations, nonzero and stderr rejection; ordinary terminal distinction has F03. |
| S04 | Exact/excess 8-MiB streams, dual excess, read/write/short-write/would-block variants, prefix accounting and sibling servicing; read-role defect has F01. |
| S05 | Whole observer byte framing, malformed/duplicate/non-ASCII/empty/nonzero/stderr/overflow/timeout cases; real versus substituted observer command, partial registration, fallback ownership and independent reap; gaps have F04. |
| S06–S07 | Real separate-session leaf setup and identity capture, observed descendant before caller exit, controlled missing-caller identity, ordinary failure versus real hard deadline, explicit external leaf recovery. |
| S08 | All complete direct operands, distinct discover versus signal identity mismatches, unverified group and independent safe second group. These are explicitly non-signalling finite branch tests. |
| S09 | Original 310/312/315-second subject times, real clock cases, declared stale-table double, hard escape versus ordinary completion; genuine root clock/deadline evidence remains required. |
| S10 | Independent fsync/close, path versus descriptor replacement, size versus hash drift, compound read/unregister/close and journal failures. F01, F04 and F05 identify the missed distinctions. |
| S11–S12 | Receipt preexistence, real 17-byte prefix, fsync/base-sync/post-receipt escapes, ownership/drain/finalization HardStop paths and separately owned recovery. F03 requires these exceptions to stay case-specific. |
| S13 | Journal cap, direct descendant cap, maximum observer input, late observer, compound kill/nonreap/poll/deadline paths; F02 and F04 apply. |

The implementation captures the complete pinned supervisor once and substitutes only the declared invocation/PREFIX and named proxies. It does not execute an extracted monitor replica. The driver and worker authenticate the closed source/request/prerequisite view; source tails attempt all comparable records independently. The full body tree is compared at worker, post-child collection and saved review, with final source/read-set checks. The saved checker uses independent fixed byte/table expectations rather than calling the target. These are useful source properties, but the five defects prevent their promotion to qualification readiness.

Original target constants remain 315 seconds, work cutoff 310, kill cutoff 312, per-stream 8 MiB, journal 64 MiB, ps/receipt 262,144 bytes, observer 0.2-second work plus up-to-0.2-second cleanup within the shared deadline. The controller's 335-second collection wait is separate and is correctly not advertised as a hard outer primitive or an extension of target cleanup. A controller timeout is failed and leaves explicit recovery uncertainty. Ready barriers, scheduler latency, startup time, full clock duration, I/O responsiveness, current vendor/stdlib/native suppliers, process identity races and genuine outer completion remain actual prerequisites, not facts established by this source review.

The fixture owner records real Popen handles before injected acquisition failure and uses its existing deadline rather than inventing an extra ordinary wait budget. Leaf signalling uses a fresh matching observed identity and retains an external recovery requirement; birth strings are not atomic PID-lifetime authentication. These boundaries should be preserved in repairs. An entry/capture failure that prevents complete records must remain failed and retained; no root approval may be inferred from a schema-shaped prerequisite record.

## Independent administrative checks and failures

Own administrative check `59ddad`, exit 0, executed only `/opt/homebrew/bin/python3 -I -B` with this reservation's `check_admin.py`. It made 3,525 metadata/literal-inventory checks over 55 distinct file identities: the exact current 30-file seal, all 24 declared original files, and the independent assignment. It checked the exact predecessor namespace, unchanged subject pin, seven source roles, all 92 unique unexecuted cases, all thirteen groups, the 69 whole/16 observer/7 direct split, 58 base cases, and all 34 inherited recipe objects in their original order with type-sensitive JSON equality. All observed identities were reread at the end of that bounded check.

`ADMIN_CHECK.json` is 269,609 bytes, SHA256 `14ef68bdea792a4b5a17161c381d632d49cbbcf9d73e2807a03e887fa9281da5`. This is evidence of source identity and inventory consistency, not control or runtime success. The inherited 325-reference provenance is retained by its exact dependency record; it was not recursively re-observed as current runtime/supplier state. The historically absent proposed native request was not probed. No massive operational-provenance recopy was undertaken.

No own administrative command failed. Combined display `4256b5` exited zero but was truncated; bounded recoveries are recorded in `COMMAND_OUTCOMES.json`. The author's original `72a8b8` administrative FilePin property-order failure and its exact diagnostic remain sealed in the subject, along with the corrected `880ec6` outcome. Its 84-case intermediate stage and before-observer-oracle source/metadata remain explicitly inactive provenance; the final packet has 92 cases. The disclosed original RI165 system-Python startup deviation receives no qualification credit, and was not repeated by this reviewer.

No subject/vendor/helper/control import, compilation, AST, probe or run occurred. No fixture, saved scientific body decode, runtime inventory, operational card, freeze/admission, repository/index/Git edit or new agent occurred. Repair and then fresh independent source review are the next root-owned actions; actual per-case admission, genuine timing and recovery, complete source/runtime custody and all 92 real outcomes remain pending.
