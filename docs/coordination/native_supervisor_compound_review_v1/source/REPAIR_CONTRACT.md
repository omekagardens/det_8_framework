# RI176 focused qualification-source repair

Status: **source only, unexecuted, requires fresh nonauthor review and root adjudication**. All 92 supervisor cases and 34 inherited recipe objects remain byte-identical in CASE_MANIFEST.json. There is no qualification/admission credit. The separately implemented saved interpretation has the same author as the worker and is not an independent reviewer. The author previously wrote RI165/167/169/171, RI125 primary/qualifier and RI131; none of those roles confers acceptance here.

The sole new write reservation is this directory. The original RI171 seal, independent review, rejected root decision and RI169 supervisor are external immutable dependencies. The source directory selection alone is relocated in protocol.py; the driver remains byte-identical. The existing request/output prefixes and RI171 envelope schema strings are intentionally retained. A request must bind the new exact source roles; old RI171 cards or qualification evidence cannot select or qualify this packet. Root must freshly authenticate the command, sources, runtime and prerequisites. No actual request, fixture, card or operation is created here.

## F01: exact pipe identity and reached-fault evidence

The worker derives `target_input_tag` as `ps:<stream>` only for observer cases, otherwise `caller:<stream>`. Read, registration, unregister and close injections compare exact tags. An earlier real ps call therefore cannot consume a caller fault. Output injections remain tied to the exact caller output descriptor tag; observer/journal/receipt descriptors are not substituted by those recipes.

The saved oracle independently selects the literal tag from its 92-row CASE_OBLIGATIONS map, checks the exact error type/message/tag, and requires registration before the injected first read. A transient must be followed by the same pipe's exact 64-byte read and later EOF, with no intervening unregister/close/re-registration. Wrong-role messages cannot qualify it. Ordinary write and would-block cases require the exact output error, full consumed caller read before it, and zero bytes or a real 17-byte prefix as appropriate. Registration and compound cleanup cases require the actual same-pipe installed/error/unregister/close sequence; the failed pump remains disabled. These are prospective trace predicates, not evidence that any fault has occurred.

## F02: separate observer and file faults

The closed late-file set is exactly late_fsync, late_close, late_replacement, late_descriptor, late_drift and late_size. Both generic saved branches exclude late_observer. The payload uses the same closed set for exit 7. The late-observer payload exits 0 absent the earlier injected observation failure. The dedicated saved branch requires first failure RI171_OBSERVER_FAILURE, a successful first real ps/discover before the second-call injection, consecutive injected observer ordinals beginning at 2, exactly one retained real journal record, complete expected caller buffers, actual caller reap, and unverified group cleanup. It cannot pass as a nonzero-caller or late-file case.

## F03: complete case-specific terminal outcomes

The pinned checker contains the complete finite terminal policy. CASE_OBLIGATIONS.json is an exact administrative rendering, not a second operational input. For ordinary whole cases, require actual return 0 for captured cases or 2 for failed cases, no exception, the complete canonical on-disk receipt equal to the traced candidate, and ordered receipt acquisition/write/fsync-complete/close-complete/base-sync-complete evidence. Completion bytes must account for every successful write. Candidate-only or full-bytes-plus-unrelated-escape evidence cannot pass. All comparable ordinary capture files retain their applicable durability and readback obligations.

The worker adds success events only after the real fsync/close/base-and-fixture sync calls return. Attempt events alone are not durability. The explicit receipt_post_receipt double occurs after completed sync and still must have its exact expected exception. The ordinary collector continues to collect, not to accept; its byte-identical status never substitutes the saved oracle or genuine root outer completion.

The following intentionally incomplete terminal families remain distinct:

- receipt_preexists, receipt_partial, receipt_fsync, receipt_base_sync, receipt_post_receipt: the existing exact partial/preexisting/full-written-then-escape semantics, actual null return and their exact designated exceptions; never ordinary completion credit.
- hard_ownership, hard_drain, hard_finalization, real_expiry: exact designated HardStop, null return and no invented completion or candidate. Full real-clock duration is still required where originally specified.
- S13.observer.nonreap, S13.journal.nonreap and S13.deadline_exhausted: the declared branch clock causes the original completion-durability deadline refusal; require null return, that exact exception, the complete failed saved candidate bytes if it reaches that branch, unverified reap/cleanup, and explicit final-deadline evidence. Buffered data must be a bounded actual consumed prefix with truthful EOF. This proves no actual 315-second timing or actual process nonreap. Earlier unrelated failures do not satisfy these recipe predicates.
- fast_reparent: retain the existing genuine ordinary failed completion or genuine hard-timer alternative. A saved ordinary outcome must satisfy the complete ordinary terminal policy. A hard outcome has no invented receipt. Unknown ancestry and recovery remain external obligations.

Source failure or startup/resource conditions that prevent those exact outcomes remain failed/incomplete, not silently converted into a matched case.

## F04: retained buffers, subject reap and complete fixture recovery

Each literal case row specifies its entry/fault, terminal family, exact input tag, complete healthy stream lengths and subject-reap class. The checker continues the original per-case first-error, cap, table and late-file branches. The added policy requires both 64-byte healthy buffers through actual EOF and successful durable readback for ordinary fallback/journal and both kill-failure cases, and the appropriate sibling for pump failures. Deliberately exhausted/nonreap cases keep bounded consumed-prefix semantics instead of an invented successful EOF/reap. Poll-unavailable remains an explicit failed subject-reap condition despite independently recovered fixture handles.

Fallback and journal cases require the exact owned caller kill attempt unless already reaped; already-exited cases require their retained exit observation and no caller kill. Actual post-kill polling must establish the recorded caller return code in the ordinary reaped cases. Both kill-failure recipes additionally require the named RI171_KILL_FAILURE, its direct_handle_kill secondary error, and a later genuine owned poll. A failed kill cannot be inferred merely from its recipe name.

The six observer I/O/registration/compound-cleanup recipes require the subject observer's own reaped result and matching successful poll within its original finish deadline. The worker records the exact 400-ms outer argument passed to the unchanged process_snapshot. The oracle computes finish as min(that argument, actual observer start + 200-ms work + 200-ms cleanup); it does not infer a new deadline from report duration. Later fixture recovery never substitutes the subject observer's bounded reap. Actual finalization or host scheduling that misses the prescribed bounded evidence is a failed qualification outcome.

Every wrapped Popen acquisition receives a monotonically assigned handle_id, captured before any injected ownership failure. Recovery uses those same actual owned handles and returns exactly one row per acquisition, in order. The oracle reconciles the entire ordered identity list, closed success/error row forms and return/reap relation. Missing, duplicate, shifted or foreign recovery identities are rejected. A successful owned recovery is still not subject cleanup credit.

A separate leaf row is required exactly for the two descendant cases. Its original LEAF and RECOVERY_IDENTITY bodies are read and pinned. Missing identity must remain explicitly unavailable. A successful signal row must match the freshly recorded whole observation and actual signal trace, retain absence_proven=false and require root external recovery review. A failure row retains the original complete identity/error and the same root obligation. No signal proves absence; no group or PID race is eliminated.

## F05: unchanged-size content mutation

All six late-file payload variants now provide deterministic nonempty 64-byte stdout and stderr, then exit 7. The supervisor checks nonzero caller status before its separate nonempty-stderr predicate, preserving the intended first error. The stderr drift control therefore has a nonempty operand.

Before/after actual mutation pins and the original first byte are recorded by the worker for each late replacement/descriptor/drift/size injection. The saved oracle checks complete pin schemas/pathnames and, for drift/size, reconstructs the exact single-byte transformation. Drift preserves length, replaces byte zero with Q and changes the hash; size appends Q and increases length by one. Both stdout/stderr preimages must be exactly R repeated 64 times. The process-journal preimage begins with the pinned canonical first byte; recovering its pre-mutation hash for this local mutation comparison does not restore durable journal custody or grant a complete monitor result.

## Unchanged bounds and prerequisites

The subject remains the exact external RI169 supervisor, SHA256 566c5bc4ae52b775a50ea465999b6e50a99067ea6312df38c38d1ba4c8018bc6. Its source is not edited, loaded, imported, compiled, AST-parsed or run during preparation. Original 315/310/312 seconds, observer 0.2 + 0.2 seconds, 8-MiB streams, 64-MiB journal, 256-KiB ps and receipt caps remain unchanged. The controller's 335-second collection wait is separate and is neither a new subject cleanup budget nor a hard external deadline proof. Administrative caps, exclusive paths, whole-source authentication, independent comparable tails and retained partials are unchanged.

No new runtime or supplier observation occurred. Fixed direct vendor, environment, complete transitive startup/native/stdlib/cache/host trust, real external timer and genuine root tool origin remain root-owned preflight requirements. The original proposed native request is not probed or created. A source-level positive prediction is not an actual feasibility result. All 92 genuine outcomes and the prospective oracle mutation checks remain unexecuted. RET is paused.
