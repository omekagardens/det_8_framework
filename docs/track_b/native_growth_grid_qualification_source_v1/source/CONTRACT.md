# RI161 synthetic grid qualification source contract

This packet prepares executable source for QP01–QP03 after acceptance of the
unchanged RI159 checker and independent auditor. It supplies neither runtime
admission nor a qualification result. No source, control, caller or certificate
has been executed by this assignment. QP04, the actual fixed-certificate run,
remains separate. The actual 109-component grid result is unknown.

The recipient is the root research owner and a fresh source/control reviewer.
They must decide whether this exact source can be admitted for synthetic
qualification. Source review cannot substitute for that qualification or its
independent outcomes review. RET remains paused; measurement remains separate.

## Source and oracle boundaries

The eleven-file namespace comprises three Python sources, three task documents,
the dependency note, two provenance manifests, author checks and a final handoff.
HANDOFF.json binds every other file. SOURCE_DEPENDENCIES.json selects 280 prior
files; only its 98 administrative bodies are decoded for provenance checks.
Scientific bodies, including the original certificate, stay opaque. See
DEPENDENCY_NOTES.md for the exact selection and inherited exclusions.

| Source | Responsibility |
| --- | --- |
| qualify_grid.py | Explicit Q01–Q35 and R01–R16 recipes, independent full expected objects and exact per-implementation refusal expectations |
| fault_cases.py | In-memory operational controls for P01–P09 and P12, including compound failures |
| caller.py | Exact future request and source bindings, bounded normal/optimized processes, genuine P10/P11 observations and retained captures |

The future subjects are unchanged grid_check.py and grid_audit.py in the
accepted RI159 source directory. Their complete identities are respectively
16091 bytes / cf9e50b061d2fcb6a040e2b1a4ce367dc802f003b0307333d561295782d87982
and 22760 bytes / aa0571ec5d7705367732a8579165429a9abf99c17dbf38798f8ac8d742b70277.
The caller hard-pins these subjects. No original input or production pin is
changed, and no existing scientific executor is extended.

Positive synthetic expectations are assembled from independently specified
literal rational answers and the complete 109-entry shape, not from the
producer, auditor or agreement between them. Full recursive type-sensitive
objects are compared before a PASS is possible. Output hashes summarize those
comparisons; hash agreement alone is not an oracle. Direct synthetic results
remain unauthenticated even if an envelope repeats the original input pins.
No synthetic root list establishes a growth law or actual canonical roots.

Each negative Q/R case specifies the first expected exception class identity,
code and message separately for each implementation. Unexpected exceptions,
wrong classes with the same name, unexpected returns and setup defects fail.
Decoder-only depth/integer/string cases are explicitly distinct from later
semantic reconstruction; parser acceptance is not witness acceptance.

## Isolated operational substitutions

Fault controls replace attributes on the individual subject module and restore
them in finally blocks. They do not replace shared os or sys module members.
MemoryOS and MemoryStream have no host-file adapter. P01's target keeps the
original bounded reader and identity comparison; earlier unrelated auditor
roles use declared identity doubles to reach that target. The hash variant has
the correct length and different bytes; the length variant is one byte larger.
This tests rejection branches, not authentication of the real fixed files.

P03 checks before-open and in-read state changes, close-only failures and a
primary failure followed by a close failure. P04 substitutes lower parsing and
read boundaries to isolate wrapper composition: every eligible final fixed-role
attempt is required even after an earlier failure. Auditor controls also
require the final saved-result attempt. P07 distinguishes initial capture
failure with no baseline from later saved-result drift. P09 inspects exact
return code 2, partial stdout, stderr and write/flush chronology for short
writes, failed flushes and failed diagnostic persistence. These are subject
operational controls, not fault injection into the caller's own capture code.

Bounded operational observations retain first and secondary errors, attempted
calls and stream bytes in the record message, as well as their digest. A
FaultFailure or other unexpected exception is a harness failure, not a passing
subject refusal. A catastrophic suite failure can retain a validated completed
prefix; absent cases are never manufactured. Production pin snapshots are
compared after each operational case. Source and interpreter pins are rechecked
outside the guarded control region, with later rechecks still attempted after
an ordinary failure.

## Future request and bootstrap contract

No request, interpreter identity, runtime inventory or admission is created
here. A later root admission must authenticate the exact request, caller,
interpreter executable and its standard-library/bootstrap provenance before
starting Python. In-source rereads cannot prove which bytes were already
executed during bootstrap. Historical execution admission is not inherited.

The request is a strict JSON object with exactly these fields:

| Field | Contract |
| --- | --- |
| schema | ri161-qualification-request-v1 |
| nonce | 32 lowercase hexadecimal characters, fresh for the admitted attempt |
| interpreter | Exact path, bytes and sha256; nonsymlink normalized absolute path; at most 256 MiB; must equal sys.executable |
| sources | Exactly caller, qualify, fault, checker and auditor, each with path, bytes and sha256; fixed source paths; at most 2 MiB each |
| output_directory | New exclusive absolute normalized directory under an existing nonsymlink parent; never overwrite or remove an earlier attempt |
| trust_basis | Exactly admission_reference, stdlib_basis, external_bootstrap_required:true and qualification_only:true; first two are nonempty strings of at most 2048 characters |

The trust references are documentary, not automatically verified credentials.
Request bytes are bounded by 65536, strict JSON depth by 16 and integer tokens
by 20 digits. Duplicate keys, floats and nonfinite tokens are rejected. The
request SHA-256 is separately supplied on the command line; no circular pin
between caller and request is required. Root must ensure the request's three
new source identities are precisely the accepted handoff identities.

The intended future parent command, shown as a template and NOT executed, is:

```text
INTERPRETER -I -S -B /Volumes/AI_DATA/development/det-review-evidence/ri161-grid-qualification-source-679wwadg/caller.py --request ABSOLUTE_REQUEST_PATH --request-sha256 REQUEST_SHA256
```

INTERPRETER and the request placeholders require a new admission. The parent
launches exactly two children with that same interpreter, -I -S -B and an
additional -O for the optimized child. The internal suffix is --child normal
or --child optimized followed by the same request arguments. Direct child
invocation does not replace parent ownership and capture evidence.

The Python dependencies are the pinned five sources and the interpreter's
standard library, including copy, contextlib, fractions, hashlib,
importlib.util, io, json, os, posixpath, re, resource, selectors, signal, stat,
subprocess, sys, time and types, plus their transitive runtime dependencies.
There is no third-party package dependency. A future admission must resolve
that runtime provenance; a list of module names is not a runtime inventory.

Authenticated subject/control bytes are loaded through a captured-byte loader,
not a disk or bytecode-cache loader. Required standard-library modules are
preloaded. A Python audit hook rejects real file opens and specified filesystem,
process and network operations during imports and controls; any recorded
attempt fails the suite even if a subject catches the exception. This reviewed
code guard is not a hostile-code sandbox or proof against every possible I/O
mechanism. P10 observes import stdout/stderr, guarded events and actual main
entry calls. Literal source review supplies the complementary check that no
scientific reconstruction is initiated at import. P11 records actual flags.

## Resource and completion contract

| Boundary | Limit or required evidence |
| --- | --- |
| Parent | 300 seconds, monotonic deadline plus ITIMER_REAL |
| Each owned child | 120 seconds total, including 2 seconds reserved cleanup; 118-second work cutoff |
| Child CPU | RLIMIT_CPU 110 seconds with installed-limit readback |
| Child memory | RLIMIT_AS 512 MiB with readback; address-space limit, not an RSS monitor |
| Core dumps | RLIMIT_CORE 0 with readback |
| Each captured stream and child report | 8 MiB; cap prefix and overflow byte retained on overflow |
| Each receipt | 256 KiB |
| Catalogue | At most 10000 cases |
| Path | At most 4096 characters and 128 nonempty components; normalized absolute nonsymlink path |
| Import output | At most 8192 characters per stream |
| Case observation strings | At most 8192 characters; operational diagnostics must fit or fail |
| Error list | 32 bounded entries plus an overflow indication; omitted later detail cannot turn failure into success |

Unsupported POSIX facilities or failed limit installation refuse the run.
Each child has its own session/process group. The parent drains both streams
with selectors, terminates its owned group on failure/deadline, and requires
actual waitpid-backed reaping, exit zero, both EOFs, no overflow, empty stderr,
durable captures and a terminal group-empty observation. All cleanup uses the
original deadline. No printed PASS substitutes for those observations.

Exclusive output consists of caller.start.json, caller.finish.json and, for
each mode normal and optimized, mode.start.json, mode.stdout.bin,
mode.stderr.bin and mode.finish.json. Files use O_EXCL/O_NOFOLLOW and mode 0600;
the new directory uses 0700. Completed writes are synchronized and closed;
captured files are reread, whole-hashed and compared with drained bytes.
Start and finish receipts are separate; failed or partial artifacts are kept.

Hard aborts permit known-handle kill/close attempts only, not invented reaping,
fresh cleanup budgets or success tails. Kernel stalls, uninterruptible calls,
bootstrap custody and genuine external-tool completion still require root's
external supervision. Missing/failed receipt persistence or a nonzero outer
process means no accepted completion, even if an earlier file says PASS.
Finite snapshots do not establish continuous custody or future immutability.

## Result and disposition contract

Each case descriptor has exactly id, family, implementation and boundary.
Each record adds status, expected, observed and full_output_compared.
Expected and observed have exactly outcome, exception_type, code, message and
output_sha256. PASS requires their equality, and all non-native-refusal PASS
records require full_output_compared:true. Native REFUSED records require the
actual subject exception class, code and message, not a result-object digest.

The child report has exactly schema, status, nonce, mode, request_sha256,
source_pins, interpreter, flags, catalogue, records, summary and errors.
Its schema is ri161-qualification-child-v1. Summary contains total, passed and
failed. Parent acceptance requires the exact 63-family set, complete record
coverage, all explicit Q05/R07/R08 sweep IDs, no FAIL or error and matching
normal/optimized records except P11's expected optimize flag. Valid completed
prefixes may be retained for failed suites but cannot qualify the suite.

The source-defined prospective total is 2547 records per mode, 5094 across two
modes: 474 Q, 1994 R, 75 operational and four caller observations per mode.
These are manual source counts, not constructed or executed cases. Runtime
admission and independent outcomes review must verify complete evidence.

Even successful future qualification would not determine the actual grid.
Only a separate QP04 admission may run the authenticated fixed-certificate
producer and saved auditor. GRID_PASS could support the retained sufficient-
envelope rejection only together with the unchanged accepted premises.
GRID_FAIL removes that shortcut; refusal proves neither alternative. No W,
C2/C3/H30, global M6/rho, adequate joint q/v budget or physical QM, geometry,
mass or gravity result is supplied by this packet.
