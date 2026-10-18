# RI135 bounded F01/F02 repair and control contract

**Source only; zero executions.** Root's `REQUIRE_F01_F02_REPAIR_BEFORE_PREPARATION_ADMISSION` is the predecessor disposition. This packet does not reverse that disposition or self-adjudicate the repair. Both prepared modules are copied into a fresh reservation; RI133 and its independent review remain untouched.

## F01 — ownership and earliest failure

`prepare.run` now obtains and authenticates a genuine initial admission reference before ownership. It initializes time, artifact/check maps, first-error/tail state and helper closures before `mkdir`. Any failure through unsuccessful creation is a preownership refusal, with no owned receipt and genuine outer failure evidence. After successful creation the very next protected block contains the fresh admission read, current source read and ATTEMPT construction/write. Any of those failures therefore reaches the original independent POST/source-admission/checks/namespace/completion tails.

The original first error remains distinct from all secondary tail errors. Every tail group is attempted independently, even when ATTEMPT is absent or partial. The initial reference remains the actual preownership reference; no successful pin is synthesized after a failed read. Partial ATTEMPT and COMPLETE files are never overwritten, deleted or retried. A failure to write the final receipt still escapes to genuine outer evidence, as required. Monitor logic, stage order, limits, source loading, 65 caller controls and all existing tail semantics are otherwise unchanged.

The 14 F01 control IDs, in order, are:

1. `F01_positive`: isolated positive real-run path with explicit non-runtime doubles.
2. `F01_pre_admission_read`: fail the genuine initial fixture metadata reference before ownership; no owned output/tails.
3. `F01_occupied`: preserve an unrelated occupied output and refuse before ownership.
4. `F01_mkdir`: fail creation; no owned output/tails.
5. `F01_post_admission_read`: fail only the newly protected post-ownership reference; exact first refusal and all tails.
6. `F01_initial_source_read`: fail only the source read used to construct ATTEMPT; later source tail still attempted.
7. `F01_attempt_open`: fail initial receipt before writing; no manufactured ATTEMPT.
8. `F01_attempt_partial`: write a literal partial receipt, then fail; retain it and write no retry.
9. `F01_secondary_post`: partial first receipt plus independent POST failure.
10. `F01_secondary_source`: partial first receipt plus independent source-observation failure.
11. `F01_secondary_namespace`: partial first receipt plus independent namespace failure.
12. `F01_secondary_checks`: partial first receipt plus independent CHECKS failure.
13. `F01_three_secondary`: partial first receipt plus all POST/source/namespace failures in exact order.
14. `F01_final_partial`: partial first receipt plus partial final receipt; first error remains in the attempted final object and the final write error must escape.

For owned cases, POST, source tail, checks, namespace and completion each have exact-one counters. For early failures PRE has exact zero, showing the intended failure occurred before later work. Case controls match the first exception class and literal message rather than accepting any refusal. Preownership cases require all owned counters zero. The source-control harness supplies its own fixture-metadata bytes and explicitly substituted authority/runtime, so none of its internal completion-shaped objects can serve as actual preparation evidence.

## F02 — complete authentic interpreter selection

`runtime_metadata.require_historical_interpreter` first requires the interpreter FilePin and its historical handoff FilePin in the opaque dependency closure. It authenticates the handoff, requires its exact historical scope/status and exactly one matching interpreter role, authenticates the complete binding JSON, then requires type-sensitive complete-object equality with the current observation. Named and resolved paths, every literal link and its order, and both target length/hash are included. `snapshot` calls it immediately after its initial interpreter observation and before runtime member enumeration. The original fresh end-of-snapshot interpreter check remains unchanged.

The historical binding is 1,057 bytes, SHA256 `622bc49403bfda7ce3cb090af44a9a698d8927dea73d733b9191f04869c6c158`; provenance is the authentic 4,302-byte RI121 handoff, SHA256 `5438ae6344a895e018f519b0f62a595a884aa516cd0dcfefabb12dba5077a9e8`. Their actual metadata identity and handoff membership were checked while authoring. No current interpreter was observed or launched.

The 11 F02 control IDs, in order, are `F02_positive`, `F02_named_path`, `F02_resolved_path`, `F02_link_literal`, `F02_link_order`, `F02_link_omitted`, `F02_target_bytes`, `F02_target_sha`, `F02_provenance_missing`, `F02_snapshot_alias`, `F02_snapshot_target`.

All altered-binding cases reach the exact new historical comparison and must refuse with `candidate interpreter differs from authentic historical binding`. Genuine saved provenance and binding read counters prove the earlier authentication steps were reached successfully. The provenance-row control is explicitly an in-memory mutation after true metadata authentication and must fail at `historical interpreter handoff identity`, before the binding read. The two snapshot controls additionally require precisely one host/source/absence/namespace/route observation, eight native-binding observations, one interpreter observation, and zero later tree walks; an earlier hash/runtime refusal or a later-walk error cannot count as success.

## Retained boundaries

The old 18 prospective preparation obligations and all 65 unchanged caller controls remain dependencies, not executed evidence. The focused25 are also unexecuted until fresh independent source review and separate root admission. Neither current runtime applicability nor resource feasibility is inferred from historical success. The genuine capture → accepted normal → optimized → separately admitted65 order remains unchanged.

No scientific target/helper import, compilation, AST/probe/run, fixture generation, scientific numerical decode, active inventory/card/freeze, repository mutation or Git operation was performed. The author wrote RI133/RI130 and the separate RI125 validator; this is author repair evidence, not independent review. RET remains paused. Parent-PID/child-ownership and sampled-not-hard-resource limitations remain actual-run review premises, without adding a third repair threshold.
