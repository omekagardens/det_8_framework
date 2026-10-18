# RI142 independent portable-checker review

**PASS for the stated narrow read-only archive utility. No blocking finding.** I read the complete223-line checker and its complete README, then ran17 authorized administrative tests: three positive and14 negative, all passing. This approves neither archived code execution nor a new control, runtime or scientific result.

Reviewer: `/root/ri116_complete_caller_review`, nonauthor of this new root-authored checker. My earlier independent RI139 source/actual review is a declared predecessor; I did not author the RI139 launcher/control implementation. Earlier RI125 primary/qualifier and RI131 authorship is outside this utility review.

Reviewed source: `verify_archive.py`,11568 bytes, SHA256 `660e41bb8615b86145b12f7a161ac532886fb6405949b4197e7f164d48ef798d`, in `/Volumes/AI_DATA/development/det-review-evidence/ri142-portable-focused25-net0j999`.
Sole write reservation: its `review/` subdirectory. The original public archive is `docs/experiments/gwosc_focused25_result_v1`. No repository or Git operation was performed.

## Complete source assessment

The entry accepts an explicit archive path or derives the documented sibling archive from the checker location. No working-directory-dependent historical path is required. The code walks only that selected tree, rejects a symlink/non-directory root, nonregular members and symlink directories, and restricts files/directories to the exact manifest-implied namespace. Its relative-name guard rejects absolute POSIX paths, traversal/dot/redundant separators, backslashes and NUL. Names are interpreted as archive-relative paths, not evaluated shell commands.

The exact25566-byte manifest and SHA256 `da4ccad5e3f06e313ad0ba2a0b00b23c4a6aa7b5faaa6b28043c6259998024ee` are checked before decoding. Every134 payload row is bounded, has a unique normalized relative path and exact identity fields, and its complete file bytes are authenticated. Including the manifest gives135 files. Each file is bounded to8MiB, the total to32MiB and the namespace to512 names. The current payload is5,040,112 bytes plus the25,566-byte manifest. No unexpected file or empty directory is accepted.

`read_regular` checks regular-file type/size, opened-descriptor identity, before/after seven-field state and exact byte count. Its use of ordinary open and a final namespace reread is correctly limited by the README's stable-local-checkout premise: this is not adversarial filesystem containment, an atomic whole-tree snapshot, or a defense against coordinated mutation after an earlier read. The utility neither claims those guarantees nor substitutes for original custody. Parent-path or race-resistant sandboxing is outside this utility's stated purpose.

The132 copied-file mappings are reconciled against the same payload identities. Original absolute paths are keys in an in-memory dictionary only. The checker never passes an original dependency path, external-map operand or Git reference to an opener, subprocess, importer or evaluator. `saved_ref` returns an authenticated relative archive name. The utility imports only its own standard-library dependencies and has no archived-source import/exec/run path. Its outputs are JSON on stdout or a refusal on stderr; no archive writer is present.

All89 operation files are reconciled with the saved full namespace. Saved directories, including `environment/tmp`, remain historical records; they are not required as empty physical Git directories. The code separately requires all saved ancestor-directory records. On-disk directories must be precisely those implied by actual payload files, so unexpected empty directories refuse. This is consistent with a fresh Git checkout and the archive README.

The helper `same` first requires identical Python types, then recursively compares complete dict/list structures. It correctly distinguishes false/zero, integer/float and nested type changes in the fields where it is used. Other selected scalar checks use direct comparisons after complete fixed-byte authentication. This is deliberately not a generic exhaustive typed-schema validator for arbitrary newly supplied reports; the fixed authenticated snapshot closes that input scope. A mutated report cannot reach those later comparisons without failing its fixed identity first.

The selected semantic checks reconcile root status/counts/boundaries, all25 ordered outcome assertions, the complete child-completion object, all30 raw numeric RSS/time records and their bounds, final gap/elapsed/maximum RSS, and byte-identical saved bootstrap PRE/POST. The1e-12 arithmetic comparison is only a saved subtraction-consistency check; actual gap/RSS/wall bounds remain literal. The utility does not independently reconstruct all F01/F02 events, fault semantics or fixture objects. That broader accepted review remains archived evidence, as the README explicitly says.

The published commit string identifies the intended publication; the utility does not query Git, authenticate the publisher or verify historical tool origin. Success means fixed published bytes plus the stated saved agreements. Its explicit false flags for archived-code execution, external-path reads, current-runtime qualification, independent historical-tool-origin authentication and scientific claims are appropriate within the stable-filesystem and reader-environment scope.

## Actual tests

The reviewer-owned driver `test_archive.py` invokes the unchanged checker through `/usr/bin/python3 -I -B`, with a30-second administrative subprocess timeout and unrelated working directory. It invokes no archived subject/helper/caller. Original and relocated source identities are checked before/after. Every command vector, cwd, actual exit, stdout, stderr, elapsed observation and expected refusal is preserved in `TEST_RESULTS.json` and the17 individual records.

The actual reviewer-driver tool was **c0fe42**, exit0. There were no failed reviewer attempts. Negative cases deliberately return exit1 and are successful rejection tests.

| Test | Exit | Actual expected result |
| --- | --- | --- |
| Original archive, explicit path, different cwd |0 |135 files,132 copies,89 operation files,25 saved outcomes,30 samples |
| Relocated checker and archive, explicit path |0 |Same complete result |
| Relocated checkout-like default sibling layout |0 |Same result; historical empty directories absent on disk |
| Missing payload |1 |Complete file inventory differs |
| Same-size payload tampering |1 |Payload bytes differ |
| Extra file |1 |Complete file inventory differs |
| Extra empty directory |1 |Unexpected directory |
| Symlink file |1 |Nonregular member, before payload open |
| Symlink directory |1 |Nonregular archive directory |
| Symlink archive root |1 |Root must be a real directory |
| Same-size manifest count mutation |1 |Pinned publication manifest differs |
| Same-size absolute manifest-path mutation |1 |Pinned publication manifest differs |
| Added byte to a zero-byte stream |1 |Changed-size file |
| Replacing partial JSON with completed JSON |1 |Changed-size file |
| Same-size saved outcome-count tampering |1 |Payload bytes differ |
| Missing manifest |1 |Missing file |
| Regular file as archive root |1 |Root must be a real directory |

The three successful checks authenticate both zero-byte streams and all eight deliberately partial JSON receipts. They do not attempt to parse those partial files as completed JSON. The altered partial receipt is correctly treated as tampering even when the replacement is syntactically valid JSON.

**Coverage limit:** unsafe-path and count mutations in the manifest fail at its immutable hash before `relative()` or later count checks. Outcome mutations fail at the payload hash before semantic comparison. Those actual first refusals are recorded accurately; they do not qualify deeper parser, type or outcome mutation branches. Those branches were source-reviewed here. I did not bypass or rewrite the fixed manifest pin to manufacture deeper dynamic coverage.

Original public archive bytes/names, the source, README and unmutated portable copy are unchanged. No cache file was created by the checker invocation. All symlink targets are reviewer-owned inert fixtures. The copied mutation trees are retained only in this external review directory, not in the proposed publication subset.

## Handoff and scope

`TEST_RESULTS.json` is63393 bytes, SHA256 `f00c08af271fecfd8263b4f7537811e7fab2dc91273098ced6090eb261b050b6`; it preserves all17 complete commands/results and the before/after archive identity inventory. `PUBLICATION_SUBSET.json` binds a compact set consisting of this review, verdict, actual test driver/result records, and exact source/README identities. Root can publish that subset without repeating the135-file archive for every test. Fixture/cwd/portable-copy trees stay external.

No requirement to rerun historical controls, observe current runtime, expand the external dependency closure, or add an operational wrapper follows. Original RI137 rejection, bounded RI139 acceptance, the separate production-entry prerequisite and all scientific/measurement limits remain unchanged. Root owns publication/adjudication and Git.
