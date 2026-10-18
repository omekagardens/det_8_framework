# RI-24 — accepted-file integrity inventory

14 September 2026 UTC. **Independently accepted integrity checker.** This is a read-only
reproducibility companion to the [implementation plan](../../REVIEW_IMPLEMENTATION_PLAN.md).
It records the 71 accepted file identities held through RI-22 and RI-23 in a
[durable manifest](review_snapshot.json). The
[checker](../../scripts/check_review_snapshot.py) compares current file bytes
with that supplied inventory without importing or executing any listed source.

The existing [research registry](../RESEARCH_CHECKS.md) covers nineteen
executable suites; it does not cover all the later proof/design notes and
coordination companions. The held collection had previously been assembled
from the registry, acceptance records and temporary coordinator inventories.
This checkpoint makes that collection directly inspectable and checkable from
a checkout or copied archive, without those temporary files.

## Run the check

From the repository root, with Python 3.11 or later:

```sh
.venv/bin/python -I -S -B scripts/check_review_snapshot.py
```

The checker uses only the standard library. `-I -S -B` isolates Python's
startup search path and site packages and prevents bytecode cache writes.
There are no research imports, subprocesses, git commands or network requests.
The checker writes one JSON report to stdout and creates no evidence files.
A caller can explicitly redirect stdout elsewhere if a retained report is wanted.

A different source directory or manifest can be supplied:

```sh
.venv/bin/python -I -S -B scripts/check_review_snapshot.py --root /path/to/copied/project
.venv/bin/python -I -S -B scripts/check_review_snapshot.py --manifest docs/coordination/review_snapshot.json
```

The default root is the checker's parent project directory, independent of the
shell's current directory. An explicit root is resolved to an existing directory;
a root symlink alias is allowed. Manifest and artifact paths beneath that root
must be canonical relative POSIX paths with no symlink components, including
symlinks whose targets remain inside the root. A copied archive needs no `.git`
directory, installed DET package, core/RET baseline or development dependencies.

## Exact coverage and publication anchor

The manifest is anchored to the already published checkpoint
[5ec58e5f6961a01ce37d0442dfcf80cbac8725df](https://github.com/omekagardens/det_8_framework/commit/5ec58e5f6961a01ce37d0442dfcf80cbac8725df),
tree `7df594315dd1c6f67c67b099dd7f844c5718671b`. Its SHA256 is
`635e85203dac1d15d5d9e0a2116ce37b3002c6c62626afdfce1baa488858bc45`.
Before writing it, the coordinator checked each of its 71 digests against
both the held acceptance inventory and that commit's actual file blobs.
This records a performed construction check, not a capability of the runtime
checker or a cryptographic signature.

| Included collection | Distinct files |
|---|---:|
| Nineteen registry suites' statement and executable files | 53 |
| Finite-record synthesis, RI-15 note/adapter/check, local-joint launcher, general research runner and RI-17 design | 7 |
| RI-18 note/adapter/check and separate launcher/regressions | 5 |
| RI-19 note, connected synthesis and RI-20/21/22/23 notes | 6 |
| Total | 71 |

The complete path list and expected SHA256 digests are in the manifest. This
is the held accepted-artifact collection, **not every accepted project file**
and not a complete package, import closure, release or working-tree inventory.
The original review, current coordination summaries, registry JSON itself,
application plan, core/RET work and unrelated user edits are outside its scope.
The registry and separate launchers retain their own source/import/execution
contracts. Their historical 411 registered witnesses and separate RI-18
31-witness execution are unchanged; this command runs none of them.

The new checker, tests and guide are also outside this historical 71-file
inventory. After acceptance, their separate RI-24 publication commit will be recorded
in [review progress](REVIEW_PROGRESS.md). The manifest does not attempt
to hash itself or certify the program that reads it.

## Report and refusal semantics

| Exit | Report status | Meaning |
|---|---|---|
| 0 | `match` | Every declared artifact was read and its captured bytes matched the supplied digest. |
| 1 | `mismatch` | The manifest is valid, but at least one artifact differs or cannot be read under the path/size contract. |
| 2 | `invalid` | The root or manifest cannot be read, or the manifest schema/path declarations are invalid. Command-line syntax errors instead use argparse's stderr/exit-2 behavior. |

For valid manifests the report carries the captured manifest SHA256, its
**declared** checkpoint, total declared files, successfully hashed files,
matched files and a per-file result. A digest mismatch still counts as a
successfully hashed file; an unreadable artifact does not. Every per-file
result gives the path, expected digest, actual digest or null, and status
`match`, `mismatch` or `unreadable`. Unreadable results include a reason.
`executed_files` is always zero. Invalid manifests produce no artifact checks.

Manifest and individual artifact reads are bounded at **1,000,000 bytes each**.
An oversized or inaccessible manifest is invalid; an oversized, missing,
nonregular, inaccessible or symlinked artifact is an unreadable file in a
valid inventory. Malformed declarations are invalid rather than ordinary
file drift. These distinct outcomes avoid turning a schema failure into an
apparent verification of the remaining list.

## Manifest contract

Schema version 1 has exactly three top-level fields:

- `schema_version`: the integer 1, excluding booleans.
- `checkpoint`: exactly `commit` and `tree`, each a lowercase 40-digit hex string.
- `artifacts`: a nonempty list of objects with exactly `path` and `sha256`;
  digests are lowercase 64-digit hex strings and paths are unique.

Duplicate JSON keys, duplicate artifact paths, extra/missing fields, invalid
hashes and noncanonical/escaping paths are refused. Paths cannot be absolute,
contain dot or parent components, backslashes or NUL characters, or use
alternate spellings such as doubled separators. The complete lexical schema
is validated before any artifact is opened. No automatic discovery, digest
refresh, normalization of bad paths or repair of listed files is provided.

A different well-formed manifest can describe a different collection. A
successful check against it does not make its contents coordinator-accepted.
The caller must obtain the manifest and checker from a trusted publication
or independently compare their identities. Editing both a file and its
expected digest can produce a match; this checker is not an authentication
system and does not query git or the remote to validate checkpoint metadata.

## What the result establishes

A match establishes byte agreement for the files as individually read. It is
not an atomic filesystem snapshot: concurrent changes may occur between reads
or after a read. Source quiet remains necessary when binding a later execution
to a coherent candidate. Symlink/path refusal is an input boundary, not a
hostile-filesystem sandbox or race-proof custody mechanism.

No theorem is reproved, witness replayed, numerical tolerance calibrated,
measurement made, publication authenticated or release approved by this
command. Hash identity also does not prove that a listed collection is an
execution closure. The supplied composition, domain and acquisition premises
in the accepted notes retain their original limits.

Changing a held source or adding a new accepted result requires its own
review and an explicitly reviewed successor inventory. Do not refresh these
historical digests merely to obtain a green report. An intentional source
change can correctly report drift from this dated checkpoint.


## Acceptance evidence

Independent inventory review matched all 71 entries to their accepted hashes
and anchored commit blobs. Independent full-source review accepted the
checker's refusal/report contract and zero research-execution boundary.
The separate regression implementer passed 94 synthetic-fixture tests in
normal and optimized Python, plus scoped lint/format checks.

The coordinator then passed all 94 regressions in a minimal isolated candidate
without git or the uncommitted project baseline. Its CLI tests include normal
and optimized startup. Separately, both normal and optimized direct runs in
that copied candidate matched the actual 71-entry manifest, reported zero
executed files, and left every candidate byte unchanged. These are integrity
and regression checks, not additional registered research witnesses.
