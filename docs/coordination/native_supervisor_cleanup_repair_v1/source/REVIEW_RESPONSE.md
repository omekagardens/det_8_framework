# RI182 response to RI180 F04-R

Status: unexecuted source repair for fresh independent review; no qualification readiness is self-declared.

| Requirement | Concrete implementation | Exact anchor |
|---|---|---|
| Caller secondary retention and order | Require exact primary/unregister/pipe-close triples as the first three receipt errors, each exactly once; reconcile the matching source_error events and injection order. | `check_saved.py:498` |
| Four-case owned-lifetime identity | Require one actual selected-role acquisition with the subject-owned PID and existing handle ordinal. Different-role ps lifetimes in caller cases remain outside this pipe ledger. | `check_saved.py:196` |
| Once closed means no later attempt | For both failed and sibling pipes, require one successful close and prohibit all later unregister_attempt and pipe_close_attempt events, even without another success. | `check_saved.py:218` |
| Failed-close/retry order | Require two exact failed-pipe unregister/close attempts in the source-derived order around the read/unregister/close fault and final success. Require the sibling single unregister/close sequence. | `check_saved.py:221` |
| Preserve observer semantics | Retain the original explicit observer secondary strings/order tests and add exact ordered first three errors plus the same lifecycle function. | `check_saved.py:612` |

O01–O26 remain an exact prefix of ORACLE_REJECTION_PLAN.md; O27–O35 add isolated caller omission/order, source-event omission/order, duplicate-success, failed-repeat and owned-lifetime variants. Every variant requires its own genuinely executed, independently matched positive predecessor. No mutation, fixture or subject run occurred.

Only check_saved.py and protocol.py change among executable sources. Protocol differs solely in its fixed successor-directory literal. Worker, payload, driver, complete manifest and complete policy rendering are byte-identical to RI176. No source extraction, new monitor, new launcher, altered limit or runtime claim is introduced. All prior seals, errors, accepted repairs and genuine-origin/recovery prerequisites remain.
