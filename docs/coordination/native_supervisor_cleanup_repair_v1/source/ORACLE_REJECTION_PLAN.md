# Prospective targeted saved-oracle rejection checks

These are source specifications only: no fixtures, captures, cards, mutated results, checker imports or executions exist. They are separate from the unchanged 92 subject cases and do not add subject qualification credit. Root must review and separately admit any future oracle-vetting harness. Each negative starts from one complete saved case that the repaired oracle has actually matched; if no such predecessor exists, that check remains blocked. Retain an unmodified positive comparison for each selected predecessor.

Use a distinct, explicitly synthetic saved-oracle operation. Never edit the real case or manufacture historical genuine tool origin. Any future metadata envelopes, request/source bindings and file pins must be honestly created for that synthetic inspection and separately admitted by root. Reconcile all affected administrative report/trace/tree/collection identities so the named semantic predicate is reached. Record the complete ordered check prefix and actual failure. A refusal at an earlier unrelated pin, schema or namespace is a custody-control outcome, not coverage of the named oracle predicate. Genuine source/worker execution and historical completion authority must remain absent from these fixtures' interpretation.

| ID | Positive predecessor | One semantic mutation (administrative envelopes rebound consistently) | Required rejecting predicate |
|---|---|---|---|
| O01 | stdout read-transient | Change only the transient event tag to ps:stdout | exact role stream injection RI169_READ_TRANSIENT |
| O02 | stderr read-transient | Change only transient event tag to ps:stderr | exact role stream injection RI169_READ_TRANSIENT |
| O03 | either read-transient | Move same-pipe 64-byte read before transient, preserve monotonic ordering | first read on same pipe is injected RI169_READ_TRANSIENT |
| O04 | either read-transient | Insert same-pipe unregister between transient and successful read | same pipe remains active through retry |
| O05 | late_observer | Change first observer-double ordinal 2 to 1 | dedicated second observer fault |
| O06 | late_observer | Remove prior discover event without altering actual first error | successful first real observer precedes late fault |
| O07 | S03.nonzero | Remove completion file; leave full candidate and ordinary return 2 | ordinary complete durable receipt bytes |
| O08 | S03.nonzero | Keep complete failed bytes but replace return by null and exception by unrelated OSError | ordinary exact return and no escape |
| O09 | S03.nonzero | Delete successful completion fsync event, keep attempt | ordinary receipt ordered complete durability |
| O10 | S03.nonzero | Delete successful completion close or second base-sync event (two variants) | ordinary receipt ordered complete durability |
| O11 | S13.observer.kill_failure | Remove defining direct_kill_error only | defining direct kill failure reached |
| O12 | S13.journal.kill_failure | Remove direct_handle_kill secondary from candidate and completion, preserving first error | defining kill failure is secondary |
| O13 | each of four fallback/journal alive/already-exited cases and two kill-failure cases | Remove/shorten stdout or stderr independently, updating capture pins | complete healthy capture stdout or stderr |
| O14 | same six ordinary cases | Keep bytes but clear corresponding EOF | complete healthy capture stdout or stderr |
| O15 | each of six observer I/O/registration/compound cases | Clear subject record reaped and returncode, leaving fixture-owner recovery intact | observer owns exact bounded reap |
| O16 | same six observer cases | Remove matching subject-owned successful poll or move it past the original finish bound | observer own successful poll inside original finish deadline |
| O17 | S01.healthy | Omit one owned recovery row | every owned handle recovered exactly once in acquisition order |
| O18 | S01.healthy | Duplicate a recovery row replacing another; keep count | recovery exact acquired identity for replaced ordinal |
| O19 | observed_descendant | Omit separate leaf row while retaining original leaf bodies | complete leaf obligation membership |
| O20 | observed_descendant with signalled-leaf row | Change absence_proven from false to true | closed unresolved signalled leaf |
| O21 | stderr drift | Substitute a size-increasing mutation and adjust the after pin, preserve before pin | mutation original length and hash (length mismatch is first) |
| O22 | stderr drift | Pretend empty-to-one-byte mutation by setting before length 0 | nonempty intended mutation operand |
| O23 | stderr drift | Retain unmodified R64 bytes and matching after hash | isolated same-size hash drift |
| O24 | stderr size | Substitute same-length Q + R63 and adjust after pin, preserve before pin | mutation original length and hash |
| O25 | caller registration | Remove unregister attempt after installed registration failure | caller partial registration cleanup reached |
| O26 | observer compound cleanup | Change cleanup error tag to caller:<stream> | exact role stream injection RI171_UNREGISTER or RI171_PIPE_CLOSE |

O13/O14 preserve the source-derived primary failure and full terminal receipt while testing the missing healthy buffer requirement. O15/O16 preserve genuine subject/fixture distinction. O17–O20 test membership and declared uncertainty, not process signalling. O21–O24 must preserve the exact primary nonzero-caller error. If source order yields an earlier *related* predicate (for example fixed complete late-stream preimage), retain and describe that exact result rather than relabeling it as a later predicate.

Positive boundary companions also preserve the specifically declared receipt-partial, hard-stop and branch-deadline/nonreap cases. They must remain matched only with their exact incomplete semantics; no test may transform them into ordinary completion or actual timing credit. These plans are neither an executed mutation campaign nor evidence of root acceptance.


## RI182 F04-R additions: O27–O35, all unexecuted

The entire O01–O26 plan above is retained byte-for-byte as a prefix. These nine new families do not change the 92 subject cases. Each concrete variant requires its **own actually executed, independently matched positive predecessor of the same exact compound case** under the same repaired source identities. A caller stdout positive cannot stand in for caller stderr or either observer positive. If that predecessor does not exist, the variant is blocked. No such positive or negative fixture exists in this source packet.

The four-case set is exactly S10.caller.stdout.unregister_close, S10.caller.stderr.unregister_close, S10.ps.stdout.unregister_close and S10.ps.stderr.unregister_close. For each case, “failed pipe” means its specified role/stream; “sibling” is the other stream of that same acquired role/handle lifetime. Whole caller cases may contain unrelated ps lifetimes: preserve their complete events, and do not relabel those different-role events as caller repeats. Rebinding and genuine-origin restrictions above apply to every variant. Rebind complete saved candidate/file bytes, completion write accounting and administrative report/trace/tree pins when those records change, without claiming a fabricated historical execution. Keep the primary and all unrelated predicates unchanged so the named semantic check is reached. Retain its full successful check prefix and actual first rejection; an earlier unrelated refusal earns no credit.

| ID | Positive predecessor and isolated variants | Semantic mutation | Required rejecting predicate |
|---|---|---|---|
| O27 | Each caller compound case, three variants | Remove only its unregister secondary, only its pipe-close secondary, or both from candidate/completion; leave injection and source_error trace intact | compound caller retained ordered primary and secondary errors |
| O28 | Each caller compound case | Swap the two receipt secondary entries, preserving exact primary and all trace events | compound caller retained ordered primary and secondary errors |
| O29 | Each caller compound case, three variants | Keep receipt prefix unchanged; omit either matching source_error event, or swap only the two matching source_error events and their monotonic positions consistently | compound caller exact source error unregister:<stream> or pipe_close:<stream>; ordering variant: compound caller source error order |
| O30 | Each of all four cases, failed-pipe and sibling variants | Add a second pipe_closed event for that same owned pipe after its successful close, without another attempt | compound one successful close <role>:<stream> |
| O31 | Each of all four cases, one failed-pipe variant | Add pipe_close_attempt after the failed pipe's successful retry, then an explicit failed repeat (no new pipe_closed); preserve original injection events and first three errors, append the distinct later source-owned close failure | compound no attempt after successful close <role>:<failed-stream> |
| O32 | Each of all four cases, one sibling variant | Add pipe_close_attempt after the sibling's successful close, then an explicit failed repeat (no new success); preserve first three errors and append the distinct later source-owned failure | compound no attempt after successful close <role>:<sibling-stream> |
| O33 | Each of all four cases, failed-pipe and sibling variants | Add unregister_attempt after success followed by a distinct failed repeat, without another close success; append the appropriate later caller triple or observer error string | compound no attempt after successful close <role>:<stream> |
| O34 | Each of all four cases, failed-pipe and sibling variants | Add an extra unregister_attempt before that pipe's first successful close but after the first existing attempt; preserve existing read/unregister/close fault sequence and successes | compound failed pipe exact attempt counts <role>:<stream> or compound healthy pipe exact attempt counts <role>:<stream> |
| O35 | Each of all four cases | Add a second selected-role Popen acquisition/complete matching recovery row with a distinct handle identity. Keep unrelated-role observations, original owned PID, stream fault and retained source errors unchanged | compound unique owned role lifetime |

O31–O33 specifically retain just one successful pipe_closed event, demonstrating why success counts alone cannot implement the once-closed rule. The later failure must have a distinct appropriate ValueError/KeyError (or another explicitly declared failed-repeat observation); do not reuse RI171_UNREGISTER or RI171_PIPE_CLOSE as a second injected fault, because the original once-only injection check would reject earlier. Caller repeats are recorded by source_error and receipt triples; observer repeats use the observer record's complete error strings. These prospective fixture records are expressly synthetic semantic inputs, not genuine process-error observations.

Positive companions include the complete unmodified outcome for each of the four actual cases. In particular, caller positives retain actual unrelated ps pipe lifetimes; the new role/lifetime check must continue to ignore those different-role attempts. No ambiguous second same-role acquisition is silently accepted. Runtime origin, subject cleanup, real recovery, ordinary terminal receipt and all preserved earlier checks remain separate and mandatory.
