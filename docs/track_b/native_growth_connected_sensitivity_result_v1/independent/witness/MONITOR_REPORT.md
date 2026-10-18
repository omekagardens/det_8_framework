# RI122 independent raw witness-monitor and outer-chain review

**PASS within the raw-monitor and trusted-transcript scope.** Every raw census was independently parsed; its owned rows, RSS, leader presence, terminal state and receipt summaries reconcile. The exact root-admitted outer invocation and its successful receipt binding match the recorded genuine tool chain. Scientific stdout remained opaque.

## Independent reconstruction

The checker read every one of the **14** samples.jsonl events: one launch, **12** monitor attempts and one terminal poll. Across the twelve raw `/bin/ps -axo pid=,pgid=,rss=` outputs it parsed **9,995 rows**, validating each three-decimal-field row and PID uniqueness. For each row it independently selected PGID equal to the launched PID **71318**, checked that any leader row had that same PGID, summed owned RSS in KiB and multiplied by 1024. It then compared these derived values to the event fields; receipt counts and peak were used only afterward as comparisons.

| Attempt | All raw rows | Owned rows | Derived RSS bytes | Start elapsed s | End elapsed s | Recorded child poll |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 833 | 1 | 4456448 | 0.002540709 | 0.022330750 | None |
| 2 | 833 | 1 | 35504128 | 0.077931292 | 0.098631375 | None |
| 3 | 833 | 1 | 42876928 | 0.151868084 | 0.171981792 | None |
| 4 | 833 | 1 | 44974080 | 0.227256167 | 0.247008209 | None |
| 5 | 833 | 1 | 48381952 | 0.302589125 | 0.322072834 | None |
| 6 | 833 | 1 | 55803904 | 0.377262125 | 0.396088792 | None |
| 7 | 833 | 1 | 61440000 | 0.451265709 | 0.470085500 | None |
| 8 | 833 | 1 | 62308352 | 0.523788209 | 0.542783000 | None |
| 9 | 833 | 1 | 62341120 | 0.598396917 | 0.616823375 | None |
| 10 | 833 | 1 | 62357504 | 0.671922542 | 0.690715500 | None |
| 11 | 833 | 1 | 62357504 | 0.745923292 | 0.765553709 | None |
| 12 | 832 | 0 | 0 | 0.820579125 | 0.842217834 | 0 |

This derives **11 live-leader samples** and a **62,357,504-byte (60,896-KiB; 59.46875-MiB) sampled peak**, agreeing with the receipt. Each live census contains only the owned leader; the final census contains no member of its process group. All ps attempts returned zero with empty stderr. The final poll records exit zero, and terminal absence is true. No cleanup/error event is hidden among the log events.

Monitor source was reviewed as text: supervise.py lines 1080–1131 define full-system census parsing and owned-group selection, including the pre/post-poll race handling; lines 1221–1260 define launch and terminal-loop behavior; lines 1261–1330 define finalization and receipt/outer message. This is the native owned-group policy, not the synthetic lane's sole-child policy. The reconstructed final empty group satisfies the native rule when the leader is already terminal before sampling; each earlier sample has its leader present and both polls live.

## Timing and limits

All events are ordered, finite and within the unchanged **120-second** active-child deadline. Each effective ps timeout equals `min(0.250, 120-elapsed_before)` and is positive. All observed census durations are below 250 ms; the maximum is **21.638709000 ms**. The maximum observed interval between census starts is **75.390582999 ms**. The 50-ms value is the source's sleep target between live iterations, alongside census and durable-log work; it is not a promised 50-ms start-to-start ceiling. No synthetic-lane maximum-gap rule was substituted.

The final raw census ends at **0.8422178340006212 s** and the raw terminal event is **0.8427583340017009 s** after the launch origin. The receipt separately records child end at **0.8429490000016813 s**, 0.190666000 ms after that event. Source line 1254 assigns a new monotonic reading after the event has been durably written. That exact assignment has no separate raw event, so this review does **not** claim to independently reconstruct the receipt's exact child-end number. It verifies source-consistent ordering and the unchanged deadline. The receipt's total/preflight/cleanup time and outer tool-call wait durations are different measurements, not alternate child runtime estimates.

RSS is a sampled observation, not a hard allocation bound or proof of an unobserved continuous maximum. Every observed owned-group sum stays below 536,870,912 bytes.

## Literal outer chain and receipt/output custody

The root admission, genuine outer record and chain have identical invocation objects: isolated `/usr/bin/env -i` with exactly the declared five environment settings, `/opt/homebrew/bin/python3 -I -S -B`, the exact supervise.py path and `witness`, closure cwd, login=false, 1,000-ms initial yield and 2,000-token output cap. The child receipt has the fixed `check.py --witness` command and unchanged environment/limits.

The recorded chain starts with chunk **68b05f**, session **54903**, empty initial output and no completed exit; it ends with chunk **ee3610**, exit **0**, no outstanding session ID. The completion exactly equals the outer record and its JSON success message binds the current 3,716,750-byte receipt SHA-256 **2789a16a1b835d603a0cc2b255c2efaf43bfb500202478f90fb155e369ba7e03**. This is **trusted root tool-history transcription**. This reviewer did not personally observe the original tool calls and does not manufacture a stronger provenance claim.

The receipt's complete samples, stdout and stderr identities match fresh opaque hashes and literal-link resolution. Native stdout is **233,035 bytes** and was not decoded; stderr is empty. Each reviewed evidence file was read with stable before/open/after descriptor/path stat checks, literal-link checks, and a second matching full hash pass. Complete 3,724-input/namespace/issued-card custody is reviewed separately by the parent; this result does not substitute for it.

| Evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| WITNESS_OUTER_TOOL_RESULT.json | 1036 | 33b23154e3709c4e761114fbfefcefc7a64f3e70906b0adb97a60c5542b044a4 |
| WITNESS_ROOT_ADMISSION.json | 3181 | ee0ef5ede9d9d615545f990de6492eeab360047e9e88649957ee3eec09b47890 |
| receipt.json | 3716750 | 2789a16a1b835d603a0cc2b255c2efaf43bfb500202478f90fb155e369ba7e03 |
| samples.jsonl | 205281 | f97ee3fc5366cedfee4188b5b4f95e1d7df291fcc0c73bb0959d8b3f7ab99f1d |
| stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| stdout.log | 233035 | 0bb05cd98706ff6b5a8284a14019899ab1b92e76e18591a3c94ea4632e88855d |
| WITNESS_GENUINE_TOOL_CHAIN.json | 1031 | a39bbf93f7e3c7352af7f5290fe7798797eaee2d874ef7b00579f468a173aba2 |

## New independent evidence and limits

The independent administrative checker ran as `/usr/bin/python3 -I -B` and completed with exit 0 (tool `74ab7c`). All parsed rows and per-attempt derivations are retained in its result.

| New file | Bytes | SHA-256 |
| --- | ---: | --- |
| MONITOR_CHECK.py | 14616 | 79b887e68824d1caa5aab0028611f0c01e63de9152c93681b31beadf4412e46b |
| MONITOR_RESULT.json | 964879 | dce52758c761f42943967db911f9fbcc7606a05e0ba03a6c2dea5c4fbae5e962 |

No target/caller/helper was executed, imported, compiled or parsed as Python. No scientific stdout was decoded and no native arithmetic or physical claim was adjudicated. No card, admission, freeze, sealed packet or repository/index change was made; only new MONITOR_* files in this independent reservation were authored.
