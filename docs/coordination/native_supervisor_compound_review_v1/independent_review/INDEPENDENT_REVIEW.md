# RI180 independent review of RI176 qualification repairs

## Decision

**Require the narrow F04-R oracle repair before qualification admission.** The main F01, F02, F03 and F05 defects are repaired in the sealed source. The main F04 buffer, kill-failure, observer-reap and recovery-membership predicates are also implemented, but the complete retained compound-cleanup recipe is not yet asserted. This is a source-only verdict: all 92 subject controls and all 26 prospective oracle mutation families remain unexecuted.

Subject: `/Volumes/AI_DATA/development/det-review-evidence/ri176-supervisor-qualification-repair-3ausb2jo/HANDOFF.json`, 14,679 bytes, SHA256 `572fe0bfc79489dc3b9c4a6df9bc4d7bbb0ff455de1c68eb2fbb00e6d870421e`. Exact 33 files and 32 payloads were authenticated before review. The sole write reservation is `/Volumes/AI_DATA/development/det-review-evidence/ri180-supervisor-independent-review-4xwmvctt`.

I did not author RI176, its five modules, or RI165/167/169 supervisor source. I authored the independent RI171 review and earlier separate WHITE validator/caller/bootstrap work. The latter is outside this subject; neither prior role confers source acceptance here. The RI171 review, RI171 rejected source and unchanged RI169 supervisor remain immutable. Root alone adjudicates, assigns repairs, admits execution and publishes. RET remains paused.

All source locations below are in the RI176 directory unless explicitly marked RI169.

## F04-R: compound cleanup evidence is not completely checked

**Blocking, narrowly scoped to the retained compound-cleanup recipes.** Relevant source: `check_saved.py:358–360`, `461–465`, `568–570`, and `272–276`; worker `case_worker.py:201–203`, `350–358`, `399–403`; unchanged RI169 `supervise_native.py:116–136` and `519`.

The four unchanged inherited `S10.{caller,ps}.{stdout,stderr}.unregister_close` recipes explicitly require both cleanup failures to be retained, the failed close to be retried independently, and successful closes not to be repeated. This was re-read in the complete original recipe objects, not inferred from the author's response labels.

For the two **caller** cases, the checker requires the primary read error, exact-tag injected unregister/close events and a later successful close. It does not require the actual subject receipt to retain either of these secondary triples:

- `unregister:<stream> / OSError / RI171_UNREGISTER`;
- `pipe_close:<stream> / OSError / RI171_PIPE_CLOSE`.

The two observer cases do explicitly require their corresponding `record.errors` entries at line 568. No equivalent caller check or complete reconciliation of `source_error` events with `receipt.errors` exists. The full candidate-to-file equality and custody checks authenticate the supplied receipt; they do not establish that it includes these independently observed errors.

Consequently, a prospective synthetic saved-oracle mutation can remove either or both caller cleanup errors from the candidate and completion, preserving the first read error, exact injected events, healthy buffer, reap and terminal evidence. With the affected administrative identities and completion-byte accounting consistently rebound as required by the existing mutation protocol, the semantic oracle has no predicate that rejects the lost subject-owned cleanup errors. This is a manual counterpath through the code, not an executed or generated fixture. It does not claim that the unchanged RI169 subject actually loses these errors.

For **all four compound cases**, the only successful-close requirement is that some `pipe_closed` event occur after the injected close failure. Neither branch rejects further unregister/close attempts after that success. The exact inherited requirement is stronger than the presence of one successful retry. A regression that attempts to close a successfully closed pipe again can add a `pipe_close_attempt` and a subsequent secondary error without changing the already verified primary, healthy bytes or terminal return. These added attempts are not rejected. Merely counting successful `pipe_closed` events is insufficient: the second attempt can fail before emitting another success event.

Required narrow repair:

1. Require the two exact caller secondary error triples in the subject receipt, after the exact primary and in the source-derived unregister-then-close order. Preserve the observer checks.
2. Reconcile the compound failed-pipe lifecycle: injected first close failure, the later successful retry, and no subsequent unregister/close attempt after success. Apply the corresponding once-closed rule to the successfully closed sibling as required by the retained recipe, with process-role/stream identity preserved.
3. Extend the prospective mutation plan with isolated missing-caller-secondary and post-success repeat-attempt mutations. Each must start from its own actually matched positive predecessor, consistently rebind only a separately admitted synthetic inspection, and reach the named semantic predicate rather than fail at an earlier unrelated custody check. No such mutations are executed by this review.

These changes can remain in the existing saved oracle and finite source plan. A new monitor, launcher, recovery budget, lowered threshold or supervisor edit is unnecessary. This finding does not reopen the repaired role selection or ordinary receipt requirements.

## Findings reconciled against actual source

| RI171 finding | Independent source assessment |
|---|---|
| F01 | Worker line 50 creates an exact `caller:<stream>` or `ps:<stream>` tag; read, registration, unregister and close routes compare that exact tag. An initial real observer therefore cannot consume a caller fault. Checker lines 188–195 require exact message/type/tag and prior registration. Lines 371–376 require the same caller pipe's later 64-byte read, no intervening unregister/close/re-registration, and a subsequent EOF. Output-write cases separately verify the consumed read and real zero/17-byte write prefix. The original wrong-role false-pass is repaired. |
| F02 | Both former broad `late_` conditions are replaced by the closed six-file-fault set. The payload uses that same set for exit 7 and stderr emission. `late_observer` reaches its dedicated lines 408–413, requiring ordinals starting at 2, prior actual observer acquisition and discovery, one retained journal record, correct first refusal, caller buffers and reap, and unverified group cleanup. The source no longer requires its nonexistent file-mutation tail or nonzero exit. |
| F03 | Lines 237–270 distinguish ordinary, receipt, hard and declared branch-deadline outcomes. Ordinary cases now require actual integer return 0/2, no exception, complete canonical on-disk receipt equal to the candidate, and ordered successful receipt write/fsync/close/base-sync events with complete byte accounting. Success events are emitted after real operations return. Candidate-only or unrelated terminal-escape evidence cannot match an ordinary case. Specific incomplete cases retain separate semantics. |
| F04 | Finite 92-row obligations add exact healthy buffers/EOF/durability, defining direct-kill failure and its secondary receipt entry, subsequent owned poll, subject observer reap within its original finish bound, and a complete ordered handle/leaf recovery ledger. These principal repairs are present. F04-R above retains the remaining compound-cleanup ledger/lifecycle requirement. |
| F05 | Late-file payloads now supply nonempty R64 stderr while preserving nonzero caller exit as the earlier failure. Worker lines 138–158 preserve actual before/after pins. Checker lines 478–491 distinguishes same-size first-byte replacement from appended-byte size change, reconstructs the corresponding preimage, checks both hashes/lengths, requires the expected first byte, and fixes stdout/stderr preimages to R64. The former empty-to-one-byte drift test is repaired. |

The F03 incomplete classes were traced independently. `receipt_preexists` preserves the original file and exclusive-creation exception. Partial receipt writes retain the exact 17-byte prefix; fsync/base-sync/post-receipt cases require their designated exceptions. Hard ownership/drain/finalization and real expiry retain null returns and no invented receipt. The nonreap/deadline doubles require the precise completion-deadline refusal, failed complete candidate bytes, incomplete caller/cleanup state and actual consumed-prefix/EOF consistency. They provide branch coverage only; they do not prove an actual 315-second nonreap. `fast_reparent` retains the ordinary failed-completion or genuine hard-deadline alternatives. These exemptions are not applied to ordinary cases.

F04 observer-reap evidence is drawn from the subject observer's own wrapped poll, after the selected injection and inside `min(recorded_call_deadline, observer_start + 400,000,000 ns)`. This equals the unchanged work-plus-cleanup bound, including the earlier outer argument. Fixture-owner recovery uses raw owned handles and cannot supply those subject poll events. Recovery rows must match every acquired handle ID/kind/PID in order; complete success/failure schemas preserve unresolved outcomes. The two descendant cases require a separate final leaf row, and signalled-leaf records retain `absence_proven=false` and a mandatory root recovery obligation. Signalling does not prove absence or atomic PID lifetime.

## Complete source and case coverage

I read all five modules completely: protocol 164 lines, driver 122, worker 499, payload 130, saved checker 661, total 1,576 lines. I also re-read the entire unchanged 588-line RI169 supervisor. The complete repair contract, response, invocation, schema correspondence, author record, all O01–O26 plan rows, full actual administrative command records and complete author administrative checker source were read. Every literal case policy was read; all 92 IDs/faults/expected outcomes were reconciled, and all 34 retained inherited recipe objects were re-read. The full manifest is byte-identical to the previously completely read RI171 manifest.

- S01–S03: complete ordinary capture, timer separation, nonzero/stderr failures and repaired terminal requirements.
- S04: exact/excess stream caps, dual overflow, read/write/partial/short-write and both would-block directions. Process-role isolation and complete write-prefix/healthy-sibling predicates were traced.
- S05: all complete observer raw framing/parser/cap/timeout branches; caller and observer partial registration, first read failures, fallback alive/already-exited routes and independent subject versus fixture reap.
- S06–S08: observed descendant versus deliberately missed initial caller identity, retained leaf uncertainty, all seven literal direct-operand tests and their non-signalling doubles. Direct cases do not receive whole-supervisor credit.
- S09: unchanged actual 310/312/315-second boundaries, real timer versus stale-table/branch doubles, outer completion and recovery uncertainty.
- S10: all late fsync/close/path/descriptor/hash/size predicates, first-error order, journal partials and compound cleanup. F04-R is the residual assertion gap.
- S11–S12: all five receipt outcomes, three hard phases, source/capture tails and separately owned recovery without invented completed subject evidence.
- S13: journal and descendant caps, full observer maximum, repaired late observer, kill-failure, nonreap, poll failure and exhausted deadline; real evidence remains distinct from explicit branch doubles.

The 26 mutation families are **plans**, not executable qualification evidence. Their corrected role, terminal, healthy-buffer, reap, recovery and hash/size predicates are reachable in the reviewed source after the prescribed administrative rebinding. O01–O04 address wrong-role and transient order; O05–O06 late observer; O07–O10 ordinary receipt and successful durability; O11–O16 kill/buffer/subject-reap evidence; O17–O20 recovery identity and uncertainty; O21–O24 hash versus size; O25–O26 registration and observer compound role. They do not include F04-R's two residual distinctions. The plan correctly requires an actually matched positive predecessor, preserves genuine records, forbids inventing tool origin, and withholds named-predicate credit for an unrelated earlier refusal. No mutation was generated or evaluated.

## Identity, correspondence and actual administrative evidence

Independent `check_metadata_v2.py` ran using `/opt/homebrew/bin/python3 -I -B`; genuine tool `70e5da` exited 0. It made 6,972 administrative/literal predicates over 98 distinct stable whole-file identities: the current 33-file subject, all 64 declared originals and this independent assignment. It checked exact predecessor namespaces, all role pins, 92 unique unexecuted cases, 34 recipes, the 69 whole/16 observer/7 direct split, complete ordered policy rendering, 26 planned mutation families and all 47 declared byte-identical function text spans. It reconstructed every changed file from the complete declared unified-diff hunks, verifying the whole old and new text. It confirmed unchanged driver/manifest and the protocol's sole directory-literal change. All 98 input identities were reread unchanged at the end.

`ADMIN_CHECK.json`: 534,125 bytes, SHA256 `0f7a30d60bd2776c9ae7341b289a060a6802f51313957096949760f51450ef2c`. This corroborates identities and inventories, not syntax, branch reachability, runtime behavior or qualification. The author's 266 administrative checks, 64 external identities and 47 spans are corroborated as metadata; their same-author result is not independent acceptance. The inherited 325-reference provenance is authenticated by its retained dependency record, not recursively reobserved or promoted to current runtime custody.

One own administrative attempt failed: `ff585f`, exit 1. V1 regenerated patch text with Python difflib and compared it with system-diff text; equivalent edits can use different valid hunk alignment. V1 source and its traceback are preserved. V2 leaves the subject unchanged and instead reconstructs complete before/after source text from every declared hunk. That stricter semantic text correspondence passed. No failed result was overwritten or described as passed. `FAILED_ADMIN_V1.json` and `COMMAND_OUTCOMES.json` record the distinction. The subject's pre-final metadata and earlier historical failures remain immutable and receive no qualification credit.

## Preserved boundaries and next root action

No subject/vendor/helper/control import, compilation, AST, probe or run occurred. No fixture, scientific decoding or evaluation, current runtime observation, operational card, freeze/admission, repository/index/Git change or new agent occurred. No old card or absent proposed request was probed.

The unchanged subject retains 315-second total, 310 work and 312 kill cutoffs; observer 0.2-second work plus 0.2 cleanup within the existing outer bound; 8-MiB streams, 64-MiB journal and 262,144-byte observer/receipt limits. The controller's separate 335-second collection wait is not a hard outer primitive or an extension of subject cleanup. Source text preserves exact direct-vendor invocation and environment, complete source binding and independent comparable custody tails. Actual interpreter/stdlib/native/cache/supplier/host authenticity, scheduler and I/O response, genuine tool origin and external deadline, actual clock cases and every recovery obligation still require root preflight and adjudication.

Root should adjudicate this one bounded residual finding and have the original author repair the existing oracle/plan, followed by fresh independent review. All 92 genuine case outcomes and the separate mutation campaign remain future, separately admitted work. This review assigns no successor and grants no native, scientific, measurement, calibration or physical acceptance.
