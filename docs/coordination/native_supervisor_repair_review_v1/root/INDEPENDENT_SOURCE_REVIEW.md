# Independent RI167 supervisor repair review

30 September 2026. Root is not the RI165/RI167 source author. The complete
586-line source, repair contract, command proposal, all thirteen retained
groups and all twenty-eight added recipes were read. This is source review
only: no subject/vendor/ps/helper/fixture invocation, import, compilation,
AST parsing or operational request was performed.

## Improvements verified

The two acquired Popen pipes are retained before either registration attempt.
Registration errors are isolated; the sibling receives its own setup attempt.
`stop_pipe` removes only the failed pump from the active set, attempts unregister
and close independently, retains failed-close ownership and avoids repeating a
successful close. A selector failure records its error and uses bounded attempts
on the remaining nonblocking descriptors. Generic read/write errors now retain
their first error and continue the healthy sibling. The ps observer uses the
same independent ownership/drain rules within its original observer deadline.

The ordinary caller tail independently polls/reaps the direct Popen child even
when a prior observer/journal failure prevented table-based cleanup. Kill failure
does not suppress polling. An unavailable poll records uncertainty; a successful
poll alone never sets observed descendant cleanup. The direct loop uses only the
original deadline and continues healthy capture. Hard abort retains its separate,
weaker no-wait behavior. Thus the originally reported F02 omission is repaired
at source level. None of these observations is an executed qualification result.

The inherited command, five native source roles, request hash, constants, eleven
unchanged functions and complete final data/receipt tail are unchanged. A literal
reverse projection restores the entire RI165 source exactly. Native sources and
all deadline/output/CPU/address-space/core limits remain fixed.

## F03: a write-side would-block exception is silently treated as empty input

Blocking before source acceptance/qualification. Exact location: `supervise`'s
nested `drain`, lines 375-394, especially 383 and 390-391. The one try block
contains both `os.read` and `write_all`. Its first handler catches
`BlockingIOError` and simply continues. That exception is appropriate as a
nonblocking read readiness race. Raised by an output write, it instead occurs
**after the input chunk has been consumed**, and silently discards that chunk.
The generic error-and-disable handler is bypassed.

A finite source-path counterexample within the declared ordinary-I/O fault
model is:

1. The caller supplies one nonempty stdout chunk. The read consumes it.
2. The capture write raises BlockingIOError before writing any bytes. Counts
   and digest remain zero; no pump error is recorded, and the pump stays active.
3. The next read returns EOF. The caller returns zero, stderr is empty, both
   EOF flags become true and the fresh process check reports no survivors.
4. All actual capture-file bytes, count and digest are consistently empty, so
   the unchanged final readback cannot detect the lost chunk. With all other
   observations successful, the receipt can be CAPTURED_FOR_ROOT_REVIEW and
   the outer return can be zero despite discarded output.

For a write that first accepts a prefix and then raises BlockingIOError, final
readback can detect a mismatch, but the original write error is still swallowed.
The zero-progress case above demonstrates why relying on that later mismatch
is insufficient. The existing generic OSError recipes do not specifically
exercise this earlier exception-handler subtype.

This is a control-flow counterexample under an explicit write-fault double,
not a claim that this error actually occurred on the selected local filesystem.
No claim is made that a normal blocking regular-file write commonly produces
would-block. The source contract nevertheless promises recording ordinary write
errors and the declared qualification already substitutes such I/O failures.
The repair should remove the ambiguity, not assume all BlockingIOError values
originated from the read.

Required narrow correction: scope the silent BlockingIOError retry to os.read
alone. Any output-write BlockingIOError must follow the ordinary failed-pump
path, retain the original exception, close/disable only that pump and continue
its sibling. Do not retry an already-consumed chunk without an explicit owned
buffer; the simplest correction needs no buffer, launcher or new deadline.

Add focused recipes for stdout/stderr write BlockingIOError both before any
write and after a real short prefix. Require the actual first pump exception,
healthy sibling bytes/EOF (or its own explicit failure), preserved partial file
and failed outer status. Also retain a read-only transient BlockingIOError
control showing that a later complete read is not lost or falsely rejected.
These remain recipes pending separate admission; existing thirteen groups and
28 variants remain intact.

## Disposition and evidence

F01 ownership and generic exception isolation improved as intended; F02's explicit
bounded direct reap is repaired. F03 blocks overall source acceptance. Keep the
sealed RI167 packet immutable and external, and produce only a narrow successor.
No native qualification, actual fixed-vector decoding or physical claim follows.

SUBJECT_AUTHENTICATION.json authenticates the exact 18-file namespace and all
17 payloads. INDEPENDENT_METADATA_CHECK.json records the independent fresh
identity and literal correspondence check (5ba0ee, exit 0), including all 33
original bindings and the inherited finite reference manifest. Whole-object
hash checks are not behavioral tests, dynamic closure or current runtime admission.

The first root span comparison used untrimmed function slices against the
author's trimEnd-plus-newline pins and failed (e6c333). The preserved correction
matches that framing for span pins while retaining untrimmed whole-source reverse
projection. A read of a guessed nonexistent SOURCE_DEPENDENCIES.json failed;
the actual DEPENDENCY_BINDINGS.json supplied the correct manifest. These are
root administrative diagnostics, not subject failures. No evidence was overwritten.

QR remains on RI168's native row-coupling proof. Measurement's independently
accepted 106 inert controls and current-E preflight are separate. RET remains
paused; protected evidence, native premises and all acceptance gates remain.
