# RI184 independent review of the RI182 compound-cleanup repair

## Verdict

**Recommend acceptance of the exact, unexecuted narrow F04-R source repair.** I found no remaining blocker in the assigned repair. This closes the two RI180 source findings concerning retained caller cleanup errors and attempts after successful pipe closure. It does not qualify the supervisor, execute a control or authorize admission.

The reviewed subject is `/Volumes/AI_DATA/development/det-review-evidence/ri182-compound-cleanup-oracle-repair-6835ytb8/HANDOFF.json`, 13,764 bytes, SHA256 `55f33b57bb11d1633b8410c64574cebccfa17846397fb6aacc27fe4a23d6bd26`. Its complete 28-file namespace and 27 payloads were authenticated before review. The exact root assignment is the 1,980-byte RI184_REVIEW_ASSIGNMENT.json with SHA256 `327cc285b708d2b290a7c5c889418854b87360a17ce87b05a2e2da559f270728`.

I am the nonauthor reviewer of RI171 and RI180, and previously authored unrelated WHITE validator/caller/bootstrap material. I did not author RI182, RI176/RI171 qualification source, or RI165/167/169 supervisor source. Prior reviewer involvement is disclosed and is not substituted for fresh scrutiny of the changed logic. Only `/Volumes/AI_DATA/development/det-review-evidence/ri184-compound-independent-review-yju68l4m` was written. Root retains disposition, admission, future assignment and publication. RET remains paused.

## Caller secondary errors and their real order

At `check_saved.py:495–504`, the caller branch now requires the complete first three receipt error triples to be the exact primary read error, unregister failure, and pipe-close failure. Each triple must occur exactly once in the full receipt error list. Canonical comparison preserves the triple field domain and types. The branch also requires exactly one matching `source_error` event for each triple, ordered between its corresponding injection and the next injection.

The stricter consecutive prefix is supported by the unchanged actual call path. RI169's synchronous read handler records the pump failure and calls `stop_pipe`. That function catches and records the injected unregister failure, then independently attempts and records the injected close failure before returning. No observer scan or sibling pump intervenes inside that sequence. The worker logs `source_error` immediately before calling the original error recorder. A resource interruption or other earlier failure preventing this sequence cannot satisfy the ordinary terminal and exact-prefix requirements; it does not become a positive case merely because the recipe was selected.

The old false-pass counterpath is therefore closed: removing or swapping either caller secondary while leaving the injection trace intact now fails the receipt-prefix predicate. Keeping the receipt but omitting or swapping the matching source-error records fails the independent trace predicates. Existing candidate-to-file equality, actual ordinary return, no unrelated exception, durable completed receipt, healthy sibling and subject reap checks remain intact.

At `check_saved.py:608–613`, the observer branch keeps its existing explicit secondary-string checks and adds the exact first-three-string sequence, each once. This is the correct observer error domain; caller triples are not substituted for observer strings. The unchanged observer's synchronous pump/stop_pipe path supports the same prefix ordering. Later observer refusal/tail messages remain allowed after that prefix.

## Both pipes, one selected owned lifetime

The new helper at `check_saved.py:196–224` is invoked only in the caller compound branch at line 505 and observer compound branch at line 613. It selects `caller` for the two whole cases and `ps` for the two observer-only cases. It requires exactly one acquisition of that role, the subject receipt/record's actual owned PID, and a typed handle ordinal. The preserved global acquisition/recovery checks subsequently enforce positive PID and consecutive handle ordinals and reconcile every owned recovery row.

This role/lifetime restriction is justified for these four fixed cases. The unchanged worker wraps each acquired process into exactly one stdout/stderr pair using role-qualified tags. A caller compound case owns one caller but can acquire many separate ps observers; those different-role pipe events must be ignored by the caller lifecycle ledger. An observer-only compound case invokes one process_snapshot and owns one ps process. A second same-role acquisition would make tag-only identity ambiguous, so the helper refuses it. It does not claim general multi-process lifetime tracking from stream tags alone.

For both stdout and stderr of that selected role, the helper requires all lifecycle events to follow acquisition, exactly one installed registration and exactly one successful close. It checks **attempts** after success, not merely success counts. The worker records unregister and pipe-close attempts before the underlying calls; a repeat that throws before another success event is still visible and now rejected at line 218.

The failed pipe must have two unregister attempts and two close attempts. The required order is registration, injected read failure, first unregister attempt and its injected error, first close attempt and its injected error, retry unregister, retry close, successful close. The healthy sibling requires one unregister attempt and one close attempt in order between registration and success.

These counts match the real unchanged RI169 `stop_pipe` implementation at lines 116–136. It removes the failed pump from the active set, independently attempts unregister and close, and leaves the closed set unset when the first close fails. The remaining drain loops service only active pipes. The final ownership tail retries the failed pipe once. A successful close sets the closed marker, so later stop_pipe calls return before any unregister or close attempt. The sibling closes once at actual EOF and is similarly skipped later. Both caller and observer final ownership tails use that same function; the four cases do not require a new cleanup budget or monitor change.

The old second counterpath is therefore closed for both failed and healthy pipes in all four cases: an extra success fails the unique-success predicate, while an extra failed attempt after the sole success fails the attempt predicate. Additional attempts before success fail the exact attempt counts. A correct first injection, correct receipt and eventual close are no longer sufficient on their own.

## Prospective mutation coverage

All 35 plan families were read. O01–O26 are an exact byte-for-byte prefix of the RI176 plan reviewed in RI180. Their role, transient order, observer, terminal, buffer, subject-reap, recovery and hash/size requirements are preserved. The nine additions address the residual repair as follows:

| Families | Independent source assessment |
|---|---|
| O27–O28 | Both caller cases have isolated secondary omissions and swaps; these reach the new receipt-prefix predicate after consistent saved-byte accounting. |
| O29 | Missing or reordered caller source-error events reach the exact-event/order predicates while preserving the receipt prefix. |
| O30 | Duplicate successful close is covered separately for the failed pipe and sibling of all four cases. |
| O31–O33 | Extra close or unregister attempts after success are covered for both pipes, including explicit failed repeats without another success. Distinct later failures preserve the original once-only injected messages, avoiding earlier unrelated injection-count refusal. |
| O34 | Extra pre-success unregister attempts are checked against each pipe's exact attempt count. |
| O35 | A second same-role acquisition with a complete recovery row is rejected as ambiguous selected-role lifetime, rather than incorrectly accepted by stream tag alone. |

Each variant requires its own actually executed, independently matched positive predecessor of the same exact case. Caller stdout cannot substitute for caller stderr or either observer case. The positive caller companions expressly retain unrelated ps lifetimes. Administrative rebinding is confined to a separately admitted synthetic saved-oracle inspection, with original genuine evidence preserved and no fabricated tool origin. Unrelated earlier custody/schema refusal receives no credit for a named semantic predicate.

These are source plans, not generated fixtures or executed counterexamples. There are still **92 subject cases, 34 inherited recipes, 35 prospective mutation families, zero actual case outcomes and zero actual mutation outcomes**. The future number of concrete mutation variants is greater than 35 and is not mislabeled as 35 executed controls.

## Complete delta, inherited coverage and actual checks

The complete 7,363-byte SOURCE_DIFF.patch was read. All three new checker spans and their surrounding branches were read and traced against the real unchanged worker callbacks and RI169 stop_pipe. Whole-source administrative reconciliation independently establishes that removing precisely those three added spans recovers the complete predecessor checker, with no hidden deletions or changes. It also reconstructs the complete new files from every literal declared diff hunk. The protocol change is solely the new fixed source-directory literal.

Six complete files are byte-identical to RI176: driver, worker, inert payload, CASE_MANIFEST.json, CASE_OBLIGATIONS.json and SCHEMAS.md. The complete RI176 source and unchanged RI169 supervisor were read in RI180; their accepted repair boundaries and disclosed source-only limitations are inherited by these exact identities, not freshly reexecuted. The current five modules total 1,619 lines; the sole behavioral delta adds 43 checker lines to the previously completely reviewed source. Fresh review of the actual added logic, complete source correspondence, unchanged interfaces and all 35 plan rows covers this bounded repair without claiming a new independent runtime test.

The exact 92-case inventory, all 34 complete recipe objects, all thirteen groups and the 69 whole/16 observer/7 direct split are unchanged. The literal four compound IDs and their once-closed recipe requirements are preserved. All earlier F01–F05/main-F04 source repairs, the complete ordered 92-row policy map, ordinary/receipt/hard/deadline distinction, full capture and source custody, recovery ledger, original control source and inactive historical failures remain intact.

Independent administrative tool `b8bb7c` exited 0, running only this reservation's checker with `/opt/homebrew/bin/python3 -I -B`. It performed 7,255 predicates over 139 distinct stable file identities: the current 28-file seal, all 110 declared original dependencies and the independent assignment. It verified both exact predecessor namespaces; all seven source-role pins; all 278 author-declared metadata checks; 117 final author references to 116 distinct files; six unchanged files; the three exact added spans; complete reverse projection and whole-patch reconstruction; the 92/34 inventory and all 35 planned family IDs. All 139 identities were reread unchanged at the end.

`ADMIN_CHECK.json` is 607,712 bytes, SHA256 `7d3d5a145fc489738981fe52c941a8f7fd4f04ae424098dc1368f7ded1a6d6e5`. No independent administrative command failed or display was truncated. The author's actual command records and complete administrative-check source were read; those checks remain same-author metadata evidence. Historical failed administrative attempts, including RI180 V1, stay preserved under their exact input pins. The 325 inherited provenance references are retained through their authenticated record, not recursively walked as current runtime/supplier observations.

## Remaining operational boundaries

No target/vendor/helper/control import, compilation, AST, probe or run occurred. No fixture, scientific decoding/evaluation, current runtime observation, operational card, freeze/admission, repository/index/Git write or new agent occurred. Proposed request/operation absence was not probed. No subject or predecessor bytes were changed.

The unchanged supervisor retains 315/310/312-second total/work/kill bounds, observer 0.2-second work plus 0.2 cleanup within the same outer deadline, 8-MiB streams, 64-MiB journal and 262,144-byte observer/receipt caps. The separate 335-second collection wait is not a hard outer primitive or added subject cleanup budget. Sampled process identity and birth strings do not prove complete descendant coverage or atomic PID lifetime; sent signals do not prove absence. Existing independent recovery and genuine root completion obligations remain.

After root source adjudication, operational progression still requires current source/interpreter/stdlib/native/cache/supplier/host preflight, concrete external deadline and genuine tool-origin evidence, separate case admission, complete actual outcomes including real-clock cases, and resolution or retained refusal of every recovery obligation. This review neither creates those premises nor assigns a successor. It recommends acceptance of this exact unexecuted source repair only; it supplies no native, scientific, measurement, calibration or physical acceptance.
