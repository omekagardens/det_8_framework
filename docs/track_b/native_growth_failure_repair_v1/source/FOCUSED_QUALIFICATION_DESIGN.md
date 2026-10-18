# RI140 prospective focused qualification

This is a bounded design for the two rejected failure paths, not a harness,
runtime record, operational card, admission or claim of passing behavior. No
subject/helper import, compile, AST, probe, fixture or control is performed in
this sitting. The 77 native and 62 audit policy cases are unchanged; the
scenarios below do not extend that catalogue or count as policy outcomes.

## Preconditions and evidence boundary

Fresh complete nonauthor review and root adjudication of the sealed RI140
packet come first. Any later qualification requires its own reviewed boundary
controller and bounded evidence contract, a fresh root reservation, genuine
bootstrap and tool-history evidence, and explicit execution admission. Use the
unchanged source bytes: no test-only source patch, module-global replacement,
synthetic successful receipt, retry or selective rebaselining.

The controller must independently demonstrate the named boundary and the
scenario-specific disposition (an actual fault for failure cases): for example
the precise acquisition point or the actual failing system
operation. Mere intended signal timing or an error label produced by the
subject is insufficient. Exact deterministic boundary control has not been
implemented or qualified here. If a reviewed external controller cannot reach
a boundary without changing the sealed subject or bypassing startup custody,
that scenario remains unresolved, not passed. Fault-injection suppliers, if
later proposed, are explicit bootstrap dependencies, never silent exemptions.

Each admitted attempt is single-shot. No bound exceeds the existing parent
840-second ceiling, child 120 seconds including two-second cleanup reserve,
250-ms census allowance, 512-MiB sampled group RSS, 8-MiB per child stream or
64-MiB auxiliary/journal limits. There are at most 31 executions in this design:
the parameter expansions stated below and no automatic retries. A blocked,
missed boundary or incomplete attempt remains a retained failure or unresolved
case. Hard stops do not grant extra time for evidence completion.

## F01: acquisition and ordinary interruption (23 executions maximum)

| Scenario | Required independently located fault | Required disposition |
| --- | --- | --- |
| F01-1 (three signals) | TERM, INT, HUP, each after successful exclusive open but before descriptor assignment | Signal retained; descriptor/local sink and phase ownership recoverable before ordinary refusal; independent close and full after inventory attempted |
| F01-2 (three signals) | Each ordinary signal after descriptor assignment but before owner assignment | Same owned refusal; no acquired marker misclassified as preownership |
| F01-3 (one attempt) | Repeated ordinary signals spanning acquisition and deferral exit | No lost pending interruption or skipped cleanup; bounded existing signal handling; ordinary failure, not a new budget |
| F01-4 (one attempt) | Exclusive marker open genuinely fails while an ordinary signal is recorded during that failed operation | Original open failure retained, no descriptor or phase ownership fabricated; no false owned completion |
| F01-5 (one attempt) | Safe initialization fails before any open | No acquired descriptor, marker or phase ownership; explicit preownership failure |
| F01-6 (one attempt) | First marker append fails after successful acquisition; independent close operation also fails | Owned failure retained; distinct close error retained; full after observations still attempted |
| F01-7 (one attempt) | Observation journal cannot open during an already-owned phase | Every frozen observation still attempted through failing sink path; no fabricated journal ranges or skipped after objects |
| F01-8 (one attempt) | Existing exclusive phase marker | Genuine preownership refusal; no overwrite, retry or fresh authority |
| F01-9 (one attempt) | Hard SIGALRM during acquisition | Immediate hard abort, only recoverable resources best-effort closed; incomplete custody explicit; no success/extended deadline |
| F01-10 (three signals) | TERM, INT, HUP, each after the collector's first Sink open but before owner.sinks registration | Record-only handling prevents ordinary unwinding; sink becomes known to cleanup; recorded signal refuses dispatcher launch; changed handlers restored |
| F01-11 (one attempt) | Ordinary handler setup fails after one handler was changed | No startup sink acquired; changed handler restored independently; original setup failure retained |
| F01-12 (one attempt) | Directory sync fails after all startup sinks were acquired | Every known sink receives independent close attempt; all changed handlers restored; original setup failure retained |
| F01-13 (one attempt) | An ordinary finalization error escapes before the former restoration location | Outer protected tail still attempts each changed-handler restoration; no fabricated successful receipt or tool completion |
| F01-14 (three signals) | Each ordinary signal becomes pending after the first raising handler has been restored but before all restoration attempts finish | Remaining attempts are not interrupted; original mask restored afterwards; pending observation/delivery retains its actual kind and prevents success |
| F01-15 (one attempt) | Hard SIGALRM while ordinary handler-state transitions are masked | Watchdog is not masked; immediate incomplete hard abort, no durable tail or additional deadline |

Both marker acquisition and ordinary observation writes must be covered by
source review. These targeted signal scenarios qualify the marker's ownership
transition and the specifically authorized collector startup path; they do not
claim exhaustive asynchronous scheduling coverage. The startup addition follows
the owner's RI140_STARTUP_SCOPE_ADDENDUM.md, not a new policy inventory.
Review must also cover masking and unmasking failures, pre-resource refusal of
unsupported original blocked/noncallable handler states, the actual pinned
launcher's raising-handler premise, and honest refusal rather than successful-cleanup claims when
host signal operations fail. Those source obligations receive no executed credit
from this finite design; no unseen signal delivery is fabricated.
Where an earlier error exists, first-error priority must remain that earlier
error; deferring a new signal must not rewrite it.

## F02: primary stream failure before cleanup (eight executions maximum)

| Scenario | Fault combination | Required disposition |
| --- | --- | --- |
| F02-1 (two attempts) | Child-pipe read fails; unregister fails in one attempt, stream close in the other | Original read error first, cleanup error later; same primary through outer handler, no extra owned-body relabel |
| F02-2 (one attempt) | Child sink write fails after a real partial prefix; unregister and close both fail | Write error first, both cleanup attempts evidenced, partial raw bytes retained; no duplication on propagation |
| F02-3 (one attempt) | Child capture reaches exact bound then one additional byte; close fails | Original overflow first; exact bounded prefix and first overflow byte retained; close error later |
| F02-4 (one attempt) | Census capture reaches exact bound then one additional byte; unregister and close fail | Original census overflow first; existing census prefix/overflow semantics unchanged; later cleanup separate; census propagation references original error |
| F02-5 (one attempt) | Read fails during census tail drain; cleanup fails | Original read error once; tail-drain reference points to it, not a new census-tail primary |
| F02-6 (one attempt) | Clean EOF followed only by close failure | Close failure is the primary; no fabricated read/overflow error or propagation token |
| F02-7 (one attempt) | Clean EOF and successful unregister/close | Existing successful EOF behavior retained; no fabricated primary/propagation reference |

Inspect the actual raw prefix and durable error journal/receipt, not only a
terminal error string. For failure cases, verify chronological order and identity
of the primary error; an unrelated earlier failure must remain first. For clean
EOF with successful cleanup (F02-7), verify that no primary or propagation error
is fabricated. A cleanup error
is never evidence that the targeted read/write/overflow fault occurred. Omitted
bounded detail, failed persistence, missing outer completion or failed custody
invalidates a passing result even if a local exception looks correct.

## Stop and meaning

All scenarios require authentic evidence of the boundary, specified disposition,
independent cleanup and applicable after-custody attempts. Root must
reconcile genuine tool history. Any failed or unresolved scenario blocks an
unqualified repair acceptance; it does not create a new policy/science result.
This document ends at design. The next action is independent source review,
not creation or execution of the controller described as a prerequisite.
