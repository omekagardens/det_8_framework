# RI122 independent raw normal-monitor review

**PASS for raw monitor reconstruction and literal outer-chain consistency.** No raw-event or invocation discrepancy was found. Scientific stdout was hashed opaquely and never decoded; this is not native mathematical adjudication or a new admission.

## Reviewed adaptation

The prior independently authored witness administrative checker was pinned at 14,616 bytes, SHA-256 `79b887e68824d1caa5aab0028611f0c01e63de9152c93681b31beadf4412e46b`. The complete saved `MONITOR_ADAPTATION.diff` was read before execution. Its changes are confined to normal-mode filenames/mode/status, omission of the witness-only child argument, actual initial/session/final tool IDs, exact admitted environment-assignment order, and an additional explicit receipt-mode check. Hash/stat/link, complete raw-row parsing, owned-group, timing, output-binding and trusted-transcription checks are unchanged.

The unchanged native supervise.py was freshly pinned at 82,578 bytes and SHA-256 `3a953ee908ca7d5db9694e5bdff6efa955d65b11447cd0f2bf6aa9eeca3de3e4`, binding the previously fully read native monitor/launch/finalization sections. All raw outputs are evaluated using its owned-group policy, not a sole-child policy.

## Raw reconstruction

The checker independently parsed **14 events** and **10068 raw ps rows** across **12 censuses**. Every row has three decimal fields and a unique PID within its census. Owned rows were freshly selected by PGID equal to the launched PID **72718**, with any leader row required to have that PGID. Derived rows, byte sums, leader presence and terminal absence were then compared to the saved per-event fields, followed by receipt summary comparisons.

| Census | Raw rows | Owned rows | Derived RSS bytes | Start elapsed s | End elapsed s | Child poll |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 840 | 1 | 4423680 | 0.002975166 | 0.022553250 | None |
| 2 | 839 | 1 | 35766272 | 0.073737375 | 0.094685000 | None |
| 3 | 839 | 1 | 44417024 | 0.148867791 | 0.167555666 | None |
| 4 | 839 | 1 | 46727168 | 0.223066625 | 0.242210958 | None |
| 5 | 839 | 1 | 47382528 | 0.297734416 | 0.317026416 | None |
| 6 | 839 | 1 | 54640640 | 0.372394375 | 0.391693375 | None |
| 7 | 839 | 1 | 60817408 | 0.447079750 | 0.466155083 | None |
| 8 | 839 | 1 | 62406656 | 0.521659041 | 0.540626833 | None |
| 9 | 839 | 1 | 62439424 | 0.592641083 | 0.612297208 | None |
| 10 | 839 | 1 | 62455808 | 0.667824375 | 0.686673833 | None |
| 11 | 839 | 1 | 62455808 | 0.739387333 | 0.758811791 | None |
| 12 | 838 | 0 | 0 | 0.814206166 | 0.834325666 | 0 |

This independently derives **11 live-leader samples** and **62,455,808 bytes** sampled peak (**60,992 KiB**). The final census has no owned-group member and records leader exit zero before and after sampling; the terminal event records exit zero and terminal absence. The successful event sequence contains only launch, its ordered censuses and the terminal poll. Every ps invocation returned zero with empty stderr. All these derived results match the receipt.

All durations are finite, nonnegative, ordered and below the unchanged 120-second active-child deadline. Every timeout is exactly min(250 ms, remaining deadline); the longest observed census was **20.947625002 ms**. The largest observed start-to-start census interval was **75.183292000 ms**. The 50-ms sleep target is not a hard start-to-start ceiling; no unrelated maximum-gap policy is imposed. Every observed group RSS is below 536,870,912 bytes. Sampled RSS is not an unsampled continuous peak or hard allocator bound.

The raw terminal event is **0.8348774580008467 s** after the launch origin. The receipt records its later child-end assignment at **0.8350324159982847 s**, 0.154957997 ms afterward. Source line 1254 takes that additional monotonic reading after durable terminal-event output; no separate raw event logs the exact assignment. Thus this review independently reconstructs the raw terminal time and verifies source-consistent ordering/deadline of the receipt value, but **does not claim to regenerate the exact receipt child-end number**.

## Literal invocation and trusted outer provenance

The actual normal admission, outer record and tool chain contain exactly the same invocation. Its `/usr/bin/env -i` assignments appear in the admitted order **LANG, LC_ALL, PATH, TZ, __CF_USER_TEXT_ENCODING**, while the semantic dictionary retains the fixed five values. The outer command is the fixed interpreter with `-I -S -B`, exact supervise.py and mode `normal`, in closure cwd, login=false, initial yield 1,000 ms and output cap 2,000 tokens. The child command is fixed check.py with **no --witness argument**. No alternate target, environment, threshold or retry is admitted.

The trusted root transcription records initial chunk **6f73b4**, session **73787**, no exit and empty output; completion **bc77ab** has exit zero and no pending session. Its completion exactly matches NORMAL_OUTER_TOOL_RESULT.json, and the JSON success message binds the current receipt SHA-256 **530f951110b10fe6c6b3682fc065efbe77d810749e297229a7f65a6f595ea4b9**. This reviewer did not personally observe the original tool history; the provenance premise remains explicit trusted root transcription.

Samples, opaque stdout and empty stderr match the receipt's full output identities. All eight reviewed source/evidence files received stable pre/open/post stat/link checks and a second matching hash pass. The parent's separate review covers all 3,743 input roles, candidate and witness prerequisites, namespace, issued cards and broader output closure. This monitor review does not replace those checks.

| Reviewed evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| NORMAL_OUTER_TOOL_RESULT.json | 1034 | 4bd65a63bec8b75eb9dba9f98d60497cef6d01907948d6a1d5872408d47fdbf5 |
| NORMAL_ROOT_ADMISSION.json | 3171 | c7a23c8c33b9df67a2544d8951fb12fd22336743173114809d5af63748d10fac |
| receipt.json | 3731974 | 530f951110b10fe6c6b3682fc065efbe77d810749e297229a7f65a6f595ea4b9 |
| samples.jsonl | 206740 | c97f810682ebac6b11b31b9b03d7b66664e9600066ef1e062043a748100d1c99 |
| stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| stdout.log | 996 | 277d2ec09a597146aeb14d7c1997cda5900945cc2c85cd5c1e9ba2ee3ac94e40 |
| NORMAL_GENUINE_TOOL_CHAIN.json | 1029 | e25f14e4c614e1783694c74a19ab452625595172f6333026f14535c365e6b599 |

## Independent evidence

The administrative checker ran under `/usr/bin/python3 -I -B` with actual exit zero (tool `16a4c5`). Its result retains all parsed rows and derivations. No reviewed helper, caller, candidate interpreter or scientific target was imported, executed, compiled or parsed as Python. No scientific stdout was decoded; no cards, admissions, sealed inputs or repository/index state were changed.

| New artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| MONITOR_CHECK.py | 14631 | f7e5c852011144a673aae8c61ce88c287130ea6b7bb4dacff1920910d7ae9c58 |
| MONITOR_ADAPTATION.diff | 9237 | 5493340a5056567a46d172bc6b3e506c089d82c1a984a05627f954e082d51a9c |
| MONITOR_RESULT.json | 972022 | c05ea5402932722ceb08ab1cda431e97a500f087c312a3da0e4de22a24c75ad0 |
