# RI143 boundary evidence and unchanged subject constraints

This note defines what a concrete controller would have to establish for the
31 RI140 prospective attempts. It is a source and design analysis, not a
controller, fault observation or admission. The accepted RI140 repair remains
immutable. Its source acceptance does not establish that every proposed fault
can be induced and independently located through its actual entry point.

The load-bearing distinction is between a source branch, a reachable branch
under the admitted inputs, and an independently observed occurrence of that
branch. An error label or final failure does not establish all three.

## Actual entry and observable boundary

The subject is the complete pinned RI140 launcher and helpers, using the exact
RI136 dispatcher and one of the unchanged 77 native or 62 audit cases. Calling
DurableSink, Owner or pump directly in a new test process would bypass the
launcher and is not qualification of this entry. A copied implementation or
test-only globals replacement is a different subject.

The launcher authenticates its exact path, interpreter, flags, environment,
root plan, current packet, cases and operational namespace before claiming its
phase. It has no boundary-control argument, extra environment slot or trace
callback in that contract. This is a source fact, not proof that every possible
external observation technology is impossible. No such technology is supplied
or admitted by this packet.

For each attempt, a later controller would need the following evidence chain.
These are requirements, not invented event records.

| Evidence | What it must establish |
| --- | --- |
| Authentic start | Exact subject, suppliers, reservation, command, environment, root admission and frozen before expectations; no late unaccounted runtime supplier |
| Boundary entry | Actual process instance, source-resolved site, relevant object and operation, and the required state before the action; not elapsed-time guessing |
| Action or fault | Independently observed actual signal, pending-set transition, filesystem operation or failing operation; intended injection is not occurrence |
| Language-level consequence | The actual Python handler or exception boundary when the scenario requires it; kernel delivery/errno alone is not interchangeable with it |
| Cause and cleanup order | Original error retained before each secondary failure, or an earlier unrelated error still first; same operation/descriptor generation, no PID/fd-reuse confusion |
| Durable and incomplete evidence | Original raw prefix, correct overflow witness, separate cleanup attempts and full applicable frozen after inventory; missing/failed evidence stays missing/failed |
| Actual final outcome | Post-restoration return or escaping exception and genuine outer completion, reconciled with provisional saved process receipts |

The observer must bind these observations to actual control flow and object
identity. A source line alone can contain multiple operations. A timestamp from
the controller's intended action is not a timestamp for the subject's later
Python handler. Clock proximity is not a substitute for a causally ordered trace.
No hypothetical addresses, runtime object layouts, syscalls, error numbers or
successful receipt bodies are supplied here as if observed.

## Kernel activity and Python activity are distinct

An open can succeed in the kernel before its returned descriptor is stored in
the Python sink. Phase ownership is another store. F01-1 requires evidence of
the interval before descriptor registration; F01-2 requires the subsequent
interval before ownership. A trace of successful open does not itself locate
the Python store or Python handler. Python's documentation distinguishes
low-level signal receipt from later execution of its Python handler. This is
general explanatory context, not verification of the pinned interpreter build.
[Python signal handling](https://docs.python.org/3/library/signal.html#execution-of-python-signal-handlers)

The accepted acquisition context records ordinary interruptions and preserves
its exact primary exception. The collector instead records ordinary signals
without raising during active work. Sending a signal therefore does not, by
itself, supply the ordinary os.read exception required by F02. Python's EINTR
retry policy also distinguishes handlers that return from handlers that raise;
a proposed fault supplier must establish the actual result at the intended
language boundary rather than infer it from signal delivery.
[PEP 475](https://peps.python.org/pep-0475/)

Similarly, selector unregister and stream close are separate calls with separate
state and failure meanings. The public selector contract describes unregister
errors for invalid or unregistered objects; it does not establish that an
arbitrary backend errno will surface as the required exception in the pinned
implementation. That translation must be justified before a paired-fault
controller can claim it reaches the selected F02 branch.
[Python selectors](https://docs.python.org/3/library/selectors.html#selectors.BaseSelector.unregister)

These public documentation references are contextual reading only. They are not
authenticated suppliers in the local dependency closure, proof of installed
versions, permission to inspect current runtime state, or a reason to change the
expected runtime. No current runtime capture occurred.

## Candidate mechanisms and why they are not controllers here

| Proposed shortcut | Specific deficiency under this entry |
| --- | --- |
| Sleep, then send TERM/INT/HUP | No proof of the actual store/handler boundary; an earlier or later interruption can produce a superficially similar refusal |
| Observe file creation, then send a signal | Creation identifies an object, not the remaining Python descriptor/owner-store window or actual handler execution |
| Precreate the phase marker | Initial namespace checking rejects it before Phase.claim; reaching exclusive open instead needs an independently proved post-check operation |
| Add a Python wrapper or replace module globals | Changes the subject or bypasses its authenticated CLI and whole-module load path |
| Insert a loader/interposition environment variable | Violates the exact environment; no permission to add an unaccounted supplier or silently amend bootstrap |
| Supply a verbose child, replacement ps or padded pipe bytes | Replaces the selected producer or its causal output; not the unchanged dispatcher/census scenario |
| Exhaust global memory/disk or flood the process table | Not a selective proven target-boundary mechanism; can fail earlier checks, harm unrelated work or exceed the fixed envelopes |
| Debugger, kernel fault supplier or emulator by name | No exact authenticated mechanism, permissions, operation semantics, object mapping, scheduling effect or bounded witness has been established |

A possible additional premise is an independently authenticated, nonpatching
observer able to bind exact instruction/object/syscall state to the selected
process. A separate selective operation-fault capability is needed for paired
read/write/unregister/close errors. Naming these capabilities is not implementing
them. Hardware instruction observation, a software breakpoint and modification
of a return register have different effects; they cannot be treated as equivalent
merely because the source files on disk retain their hashes.

A forced operation result must be described as such, with the responsible
supplier and mechanism. It cannot be represented as a naturally occurring host
failure or manufactured by printing the subject's expected error message. Root
must decide whether a proposed supplier is admissible under unchanged custody;
this packet neither inserts it nor presumes that decision.

For filesystem candidates, a path mutation must occur at the required boundary
and retain its real identity and effects. It must not be hidden by updating the
frozen expectations to match it. A caught namespace/custody refusal is not the
later exclusive-open, write or close fault it was intended to induce.

## First cause and late outcome remain load bearing

F02's four originating branches record the real exception or overflow before
unregister and close. Its owner-scoped token is propagation, not a new error.
The controller must distinguish the original event from repeated references to
it. In census tail drain, an existing census-body error may already be first;
the later read fault must not displace it. Clean EOF followed by failing close
has a close primary; successful EOF must not fabricate a primary.

Child overflow retains the bounded child prefix and first excess byte. Census
overflow has its own retained-prefix semantics and does not supply a child-style
first-excess-byte field. A controller may require an independent actual-byte
witness without pretending that the unchanged census report already has one.

PROCESS_REPORT.json and PROCESS_CLOSE.json precede handler restoration and can
contain provisional success. A later pending signal, restoration failure or
escaping exception can invalidate that outcome. Genuine post-restoration return
or exception plus actual outer completion is required. Neither equality of old
receipts nor a self-authored tool-shaped JSON object closes that boundary.

## Fixed limits and stop

No proposed observation pauses, resets or extends the clocks: parent ceiling
840 seconds; metadata/before/after/final budgets 60/300/300/60; child 120 seconds
including its two-second cleanup reserve; each census at most 250 ms; sampled
owned-group RSS 536870912 bytes; each child stream 8388608 bytes; each applicable
auxiliary read/journal bound 67108864 bytes. Controller overhead must fit the
unchanged admitted envelope. Stopping a process for inspection does not create
extra time. No timing/performance feasibility has been established here.

All 23 F01 and eight F02 obligations remain in their original inventory, as do
all 139 policy cases and deeper 20 native/42 audit obligations. A blocked design
is not a passed test, a dismissed obligation or a theorem of impossibility.
The source/observability gaps are recorded for root's next decision. No general
launcher, patched subject, controller, fixture, admission or execution is created
by this note. Actual C2/C3 signs and simultaneous H30 remain qualification-blocked;
RET remains paused and measurement remains separate.
