# RI169 independent root source review

30 September 2026 UTC. Root did not author RI165, RI167 or RI169. Root previously
adjudicated F01/F02 and discovered F03 in the RI167 source. This is a fresh
manual review and independent literal-byte comparison, not author acceptance
or actual supervisor qualification.

## Decision

Accept the narrow source repair of F03. The silent BlockingIOError handler now
surrounds only os.read. Obtaining the descriptor, writing the returned bytes,
counting, hashing and handling overflow remain outside that inner handler.
All prior RI167 repairs and all fixed bounds survive unchanged. There are no
remaining blocking findings from this bounded source review. This decision
does not accept any actual run, runtime supply or native case outcome.

## Complete failure-path reading

Root read all 588 source lines, the exact diff, repair contract, six new recipes,
the retained thirteen-group protocol, correspondence and command/dependencies.
The two source halves were read in e9b9a1 and 848aa8, both exit 0; earlier
combined output was truncated, so those complete halves govern the reading.

For either stdout or stderr, after a successful nonempty read, write_all can
raise before writing or after a real partial prefix. Both now reach the outer
Exception handler. The original pump error is appended before stop_pipe's
independent unregister/close attempts, the failed pump is disabled, and its
EOF is not invented. Counts/digest advance only after write_all completes.
The healthy sibling remains active and is serviced by the normal or fallback
drain and the separately bounded direct-reap path. Error saturation has an
explicit failure marker; it cannot restore a clean receipt.

In the zero-progress case, empty-file readback can correctly match zero count
and hash, but the recorded error and absent EOF prevent CAPTURED_FOR_ROOT_REVIEW
and force return 2 if ordinary receipt finalization completes. In the 17-byte
prefix case, the original pump error remains first and the unchanged full
readback adds the count/hash mismatch as a secondary error. No chunk retry or
false completeness is introduced. A read-side BlockingIOError consumes no
bytes, leaves the pump active, and permits a later read; that positive local
control does not accept deliberately nonempty stderr at the whole-supervisor
level. Descriptor-access exceptions are outside the silent catch.

Root rechecked the downstream error test, cleanup and final receipt selection,
not only the changed catch. Partial acquisition ownership, independent handle
cleanup, observer-independent direct poll/reap, hard-abort distinctions and
all durability/readback checks remain as reviewed in RI167. The ps pump has
no output write in its read retry block and is byte-identical. Timer, signal,
process identity and complete-fork-coverage limitations remain explicit.

## Actual administrative check

Root-authored check_ri169.py uses only the authenticated administrative metadata
helper and literal text. fc6179 exited 0. It independently authenticates all
20 sealed files and 26 predecessor/source/assignment identities; extracts the
caller drain by literal text; constructs the expected narrow change; and
reverses the change to match the entire 26,254-byte predecessor exactly.
Fourteen of fifteen global function spans are identical. The final 26,321-byte
source has 588 lines. No Python source parser, AST, compile or subject import
was used. The helper was authenticated before its administrative import.

All thirteen groups and twenty-eight recipes are exact predecessor copies.
The six new recipes cover two streams times zero-progress write, after-prefix
write and transient read. All 34 unique recipes remain marked unexecuted. Root
checked the unchanged native argv, five source roles, request proposal, output
paths, environment, limits and command pin. The proposed RI163 request remains
absent and was not treated as an existing authenticated file.

The author retained its failed administrative ENOENT request read and original
script. Root's initial literal-read call 85152b exited 1 after successfully
reading HANDOFF.json because it also requested nonexistent HANDOFF.md. This
was a mistaken display filename, not an evidence check or subject execution;
the actual namespace and contract were then read and independently checked.
Neither diagnostic is erased or converted into qualification credit.

## Next actual work and limits

Prepare executable finite supervisor-only qualification cases from the retained
thirteen groups and 34 recipes, including explicit inert substitutions and
fault doubles. Do not run the native caller to test its supervisor. Source
review and root admission must precede those processes; genuine outer results,
all applicable tails, raw observer evidence and complete saved reconstruction
must follow them. Named predicate reachability is required; an earlier unrelated
refusal is not coverage. Doubles prove only their declared finite branches.

Preserve 315 seconds with 310/312 cutoffs, all caps and the original cleanup
deadline. No shortened clock proves a real deadline and no extra monitor or
cleanup budget is added. Native 2,547 cases per mode and the actual 109-vector
remain unexecuted/unread. RI164's platform assumptions remain external premises.
Measurement106 acceptance is separate. RET alone stays paused.
