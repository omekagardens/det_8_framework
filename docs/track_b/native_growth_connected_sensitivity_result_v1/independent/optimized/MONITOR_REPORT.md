# RI122 independent optimized raw-monitor review

**PASS for raw monitor reconstruction and literal trusted outer-chain consistency.** A review-only parser assumption was corrected to match the retained monitor's explicit exit-race behavior. The initial failure is preserved; no scientific target was rerun and no limit or custody requirement was relaxed.

## Source adaptation and preserved review failure

The normal metadata checker was pinned at 14,631 bytes, SHA-256 `f7e5c852011144a673aae8c61ce88c287130ea6b7bb4dacff1920910d7ae9c58`. Initial adaptation changed only normal→optimized mode/paths/status, actual tool-chain IDs and the child-only `-O` flag. The outer supervisor remains unoptimized under `-I -S -B`.

The first metadata run (tool `5ed6bc`, exit 1) refused an intermediate terminal_poll because the prior normal evidence had only one terminal event. The optimized stream instead exercises the explicitly permitted native sequence: census 11's pre-exit ps snapshot contains the leader, its subsequent poll returns zero, terminal absence remains false, and the loop takes census 12 to verify the now-empty group. Native source lines 1113–1119 and 1249–1256 expressly describe and enforce this path. These sections were reread and the full source repinned at 82,578 bytes, SHA-256 `3a953ee908ca7d5db9694e5bdff6efa955d65b11447cd0f2bf6aa9eeca3de3e4` (tool `fedbd4`).

The initial checker, initial exact diff and failure record are preserved. The correction enforces the full native event grammar: every census whose post-poll is terminal must be followed by exactly its matching terminal_poll; absence=false requires a confirmation census; a cached terminal return code cannot change; absence=true must close the stream with an empty owned group. All original raw-row, identity, RSS, wall, timeout, command and outer-binding checks remain. The complete final diff and separate grammar-correction diff are retained and reviewed. This corrects an overly narrow evidence-parser assumption; it does not change the retained caller or accept a leaked group.

## Independent reconstruction

The corrected administrative checker read all **15 events**: one launch, **12 censuses** and **2 terminal polls. It parsed all **9,995 raw ps rows**, requiring three decimal fields and unique PIDs within each census. It derived the owned rows from PGID **73675**, checked leader PGID, summed KiB and converted to bytes before comparing any saved row/RSS summary.

| Census | Raw rows | Owned rows | Derived RSS bytes | Pre-poll | Post-poll | End elapsed s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 833 | 1 | 4423680 | None | None | 0.021823583 |
| 2 | 833 | 1 | 35553280 | None | None | 0.096575792 |
| 3 | 833 | 1 | 44843008 | None | None | 0.172375167 |
| 4 | 833 | 1 | 46940160 | None | None | 0.246211917 |
| 5 | 833 | 1 | 49381376 | None | None | 0.320584542 |
| 6 | 833 | 1 | 56688640 | None | None | 0.395528083 |
| 7 | 833 | 1 | 62013440 | None | None | 0.470399667 |
| 8 | 833 | 1 | 62636032 | None | None | 0.544212417 |
| 9 | 833 | 1 | 62652416 | None | None | 0.618609333 |
| 10 | 833 | 1 | 62652416 | None | None | 0.693310208 |
| 11 | 833 | 1 | 62799872 | None | 0 | 0.768154167 |
| 12 | 832 | 0 | 0 | 0 | 0 | 0.787566792 |

Derived totals are **11 live-leader samples** and a **62,799,872-byte sampled peak** (**61,328 KiB**), including the valid pre-exit leader snapshot. The final census has poll-before zero, poll-after zero and no owned-group rows; its terminal event records exit zero and terminal absence. Every ps attempt returns zero with empty stderr. No unrelated or cleanup event is silently discarded. These independently derived totals match the receipt.

All event times are finite, ordered and below the unchanged **120-second** active-child deadline. All effective timeouts equal min(250 ms, remaining deadline), and the maximum observed census duration is **20.184417001 ms**. The 50-ms live-loop sleep target is not a promised start-to-start interval; the race-confirmation loop correctly performs another census without that live sleep. Every observed owned-group RSS is below **536,870,912 bytes**. Sampled RSS is not an unobserved continuous peak or hard allocator bound.

The final raw terminal event is **0.7880856670017238 s** after the launch origin. Receipt child end is **0.7882866670006479 s**, 0.200999999 ms later. Source line 1254 assigns a fresh monotonic reading after the durable terminal event; that precise assignment is not separately logged. This review reconstructs the raw terminal time and verifies source-consistent ordering/deadline of the receipt value, and does **not** claim independent regeneration of the exact receipt-end number.

## Outer invocation and opaque output binding

The optimized root admission, genuine outer record and chain have identical literal invocation objects, including the exact **LANG, LC_ALL, PATH, TZ, __CF_USER_TEXT_ENCODING** assignment order and fixed environment values. Outer interpreter flags remain `-I -S -B`; child flags are exactly `-I -S -B -O` before the fixed check.py path, with no witness argument. Cwd, login=false, initial 1,000-ms yield, 2,000-token cap and unchanged resource envelope match the admission and receipt.

The chain records initial chunk **7e854f**, session **12358**, empty initial output and no completed exit, then final chunk **aa3053**, exit **0**, with no pending session. The final result equals OPTIMIZED_OUTER_TOOL_RESULT.json and binds the current receipt SHA-256 **9870e9f4b2d810e3065a8e36300ed93e811e4841ee26544b3f6b5951b417a815**. This is explicitly **trusted root tool-history transcription**, not a claim that this reviewer personally witnessed the original tool calls.

The receipt's samples, stdout and stderr full identities match fresh opaque hashes/link resolution; stderr is empty. Scientific stdout was never decoded. All eight source/evidence files received stable pre/open/post stat/link observations and a second matching hash pass. The parent separately checks complete input/predecessor/card/namespace custody and normal/optimized output equality; this raw-monitor review does not replace those checks.

| Reviewed evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| OPTIMIZED_OUTER_TOOL_RESULT.json | 1043 | 0851f7d3adc1170c5a31e34ba569e93e4139b3f3094304c747272e181cd0b70b |
| OPTIMIZED_ROOT_ADMISSION.json | 3201 | f69d54038602493a55ddc30d635405a71fad997b1ebd6b9fde9d46e78477d562 |
| receipt.json | 3743222 | 9870e9f4b2d810e3065a8e36300ed93e811e4841ee26544b3f6b5951b417a815 |
| samples.jsonl | 205380 | 87c8855d9db69a8c59146ece7391fdebe5af17b9a46ecf005cb8031f03d36b98 |
| stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| stdout.log | 996 | 277d2ec09a597146aeb14d7c1997cda5900945cc2c85cd5c1e9ba2ee3ac94e40 |
| OPTIMIZED_GENUINE_TOOL_CHAIN.json | 1038 | 1734f42a7bfa6ab89f5abb8b107883d9e2f5fa2318ce474aa59580a587a6b929 |

## Independent artifacts

The corrected checker ran with `/usr/bin/python3 -I -B`, actual exit zero (tool `93c4e7`). Its result retains every parsed census row, both terminal events and all derived quantities. No target/caller was imported, compiled, parsed as Python or executed; no admission/card/freeze, sealed input or repository/index change occurred. Only new MONITOR_* evidence in this reservation was authored.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| MONITOR_CHECK.py | 16439 | aaab9053bf87f5e266c249691d5e695607fd13edabca39a7e6e2bea48625b655 |
| MONITOR_ADAPTATION.diff | 15133 | dc5b9675fca9ec4dade600f43383ec390d35c66087b8b40dc70e9dfaec3f01e6 |
| MONITOR_RESULT.json | 965392 | deb9c129ff2b0da9dea7c01c6d09517fe32147aacca7adfc10d1813d93a555b4 |
| MONITOR_INITIAL_CHECK.py | 14699 | 9b8447364197fb02e843f20ea969b3c43d307cf47664217fca9371604ffa38ea |
| MONITOR_INITIAL_ADAPTATION.diff | 9194 | 51be2810b2e6c77a0639c1c289bc373389438f5a0ae197f388ec667e3227d365 |
| MONITOR_PREPARATION_FAILURE.json | 948 | c3291394ff3d698eda7c5a2ec3bf33fef5331106f00c15ea5bfe08bc3ab88d22 |
| MONITOR_EVENT_GRAMMAR_CORRECTION.diff | 8769 | 94a13c105c3855654a67fac649be80d52bebc9d2f4f0025998e6b4ebe0995b80 |
