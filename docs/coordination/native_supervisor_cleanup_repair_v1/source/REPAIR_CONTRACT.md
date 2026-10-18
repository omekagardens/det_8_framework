# RI182 narrow compound-cleanup oracle repair

This packet is **unexecuted source for renewed nonauthor review**. It addresses only RI180 F04-R. The exact original RI176 sources and RI180 review/root rejection remain immutable and externally bound. Nothing here accepts the supervisor, admits a case, supplies a current runtime observation, or replaces root's genuine command/outer/recovery evidence.

## Subject-owned secondary errors

The two caller compound cases retain the existing exact primary read error and exact injected read/unregister/close event checks. The added check requires the complete subject receipt's first three error triples, in order, to be:

1. `pump:<stream> / OSError / RI167_F01_READ`;
2. `unregister:<stream> / OSError / RI171_UNREGISTER`;
3. `pipe_close:<stream> / OSError / RI171_PIPE_CLOSE`.

Each must occur exactly once. These are consecutive because the unchanged synchronous read-error handler records the primary, calls stop_pipe, records its unregister exception, then records the close exception. No other observation is interleaved on this path. The checker additionally finds the three exact source_error trace entries and requires read injection < primary record < unregister injection < unregister record < close injection < close record. The earlier candidate-to-file equality, complete ordinary terminal return/receipt/durability and healthy-sibling requirements remain mandatory. Injection events alone cannot stand in for subject-owned retained errors.

The observer compound branch preserves both explicit error-string membership checks and its existing injection/order/bounded-reap requirements. It adds the equivalent exact first-three-error sequence (ps pump, ps unregister, ps pipe_close), with each string once. Its errors remain observer strings, not caller triples; no type/domain is silently interchanged.

## Selected owned pipe lifetime

The shared function is called only from the two caller and two observer compound cases. It selects caller for whole cases or ps for observer-only cases, and requires exactly one actual popen_acquired event for that selected role, with the subject receipt/record's owned PID and typed existing handle ordinal. Each of these four unchanged recipes creates exactly one selected-role process. Caller cases may create many ps observers; those are different roles and are ignored by this pipe lifecycle check. The observer-only cases create one ps process. Ambiguous multiple same-role lifetimes are rejected rather than pretending that tag-only stream events distinguish them.

For both stdout and stderr of the selected owned process, all registration/unregister/close events must follow that acquisition. The role-qualified tag, single selected-role lifetime and already retained whole-source evidence together identify the owned pipe. There is one installed registration and one successful pipe_closed event. **After that success, no unregister_attempt or pipe_close_attempt is allowed.** The predicate reads attempts, not merely successes; a later operation that throws before another pipe_closed event is still rejected.

For the failed pipe, the original first close attempt fails. There must be exactly two unregister attempts and two close attempts, ordered as:

```text
registration < primary read injection
  < first unregister attempt < injected unregister error
  < first close attempt < injected close error
  < retry unregister attempt < retry close attempt < successful close
```

For the sibling there is exactly one unregister attempt and one close attempt, ordered after its registration and before its successful close. Its complete healthy bytes/EOF are still checked by the unchanged prior oracle. The new lifetime check neither promotes injected failures to genuine runtime events nor infers recovery from a close.

This is a qualification completeness correction. No observed RI169 runtime regression is claimed. The existing subject already guards the closed set and retries a failed close; the source-only saved oracle must verify those defining requirements when actual outcomes eventually exist.

## Preserved source and contracts

The exact five modules remain present. Only check_saved.py changes behavior. protocol.py changes only its fixed source directory to this reservation. qualify_supervisor.py, case_worker.py, inert_payload.py, CASE_MANIFEST.json and CASE_OBLIGATIONS.json are byte-identical to RI176. The old schema strings, seven source roles, three genuine pinned prerequisites, request/operation/reviewer prefixes, envelopes, independent tails, exclusive/no-retry output and complete source/runtime custody requirements are retained. RI176's SCHEMAS.md is included byte-for-byte as the inherited schema contract; this repair adds no trace, receipt or recovery field.

All 92 cases, 34 inherited recipes and 13 groups remain exact and unexecuted. The whole/observer/direct counts remain 69/16/7. The exact external RI169 supervisor is unchanged. Its original 315/310/312 seconds, 0.2 + 0.2 second observer bound, 8-MiB streams, 64-MiB journal and 256-KiB observer/receipt caps are unchanged. The 335-second collection wait remains separate from subject cleanup and is not a hard external deadline proof. All earlier F01–F05 repairs and intentionally incomplete receipt/hard/deadline branches remain.

O01–O26 are preserved as an exact plan prefix; O27–O35 add nine prospective semantic mutation families. Every concrete variant requires its own genuine independently matched positive predecessor. Consistent synthetic administrative rebinding is explicit, and unrelated early custody refusal receives no semantic credit. No positive or negative fixture is generated or run. These plans do not change the 92-case subject inventory.

## Remaining prerequisites

Fresh nonauthor review and root adjudication precede qualification. Root must authenticate current vendor/stdlib/native/cache/host suppliers, concrete external command/deadline, actual tool origin, complete source/input/card/operation custody, all 92 actual cases, the real-clock cases and every recovery obligation. No supplied JSON self-authenticates those facts. Prior RI171/RI176 and independent-review administrative failures remain retained; no historical failure is relabeled successful.

Only administrative text/JSON/opaque file comparisons ran in this reservation. No Python source import, compilation, AST, probe or execution, scientific decode, fixture creation, runtime inventory, operational card/admission, repository/index/Git action or new agent occurred. The author wrote the predecessor qualification source and therefore is not its independent acceptor. RET remains paused.
