# RI164 — bounded static native supplier closure

## Result and proposed disposition

The declared Mach-O load graph of the 76 selected non-system files closes
without an additional non-system supplier. Both architecture slices were
inspected. This resolves the finite static part of RT02; it does **not**
establish a hermetic runtime or accept the Apple system boundary.

Recommended root disposition: accept this exact static non-system closure
only after explicitly accepting the Apple platform premises below and its
adequacy for the retained operation. If root requires runtime loading or
whole-system closure, RT02 remains open. This author packet does not make
that acceptance, admit execution, or replace RI165 supervision.

## Exact scope and observed graph

The fixed direct interpreter and framework binary are rooted at:

- /Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9
- /Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Python3

All 74 installed regular .so files in the previously selected lib-dynload
namespace are additional roots, including test and optional modules. This is
an installed-extension **overapproximation**, not an observed import profile.
The current root selector is bound in INSPECTION_POLICY.json; no filesystem
search supplied a new root.

| Quantity | Observed |
| --- | ---: |
| Non-system files, whole-pinned before/after inspection | 76 |
| Total distinct non-system bytes | 22,985,616 |
| Architecture slices | 152: x86_64 and arm64 in each file |
| Declared load/dylinker edge occurrences across slices | 200 |
| Non-system edge occurrences | 2 |
| System-candidate edge occurrences | 198 |
| Unique system-candidate install names | 17 |
| Additional non-system suppliers | 0 |
| Weak, lazy, reexport, upward, rpath and DYLD-environment commands | 0 |
| Unknown load-command kinds in these captures | 0 |
| Missing or unresolved non-system edges | 0 |
| Signature verification commands returning zero | 76 |

For each slice the only non-system edge is
`@executable_path/../Python3` from the direct interpreter. Its ordered
candidate list has one entry: the selected framework binary, after normalizing
the literal bin/.. segment. That file was whole-pinned at its canonical
nonsymlink path and contains the matching slice. The longest simple path to
the system boundary is two edges; non-system depth is one.

The framework's `LC_ID_DYLIB` value,
`@rpath/Python3.framework/Versions/3.9/Python3`, is image identity metadata.
It is not a dependency and creates no missing @rpath edge. No actual LC_RPATH
command occurs, so there is no contextual run-path search to resolve here.

The parser checks complete per-slice command indices, ncmds and total cmdsize
against sizeofcmds, then reconciles the -L listing against load plus identity
commands in order. Full captures, arguments, statuses and parser text are
retained. No target/source code is decoded or evaluated by this parser.

## Apple boundary: explicit premises, not path-based trust

The 17 exact names are listed in NATIVE_GRAPH.json, including /usr/lib/dyld,
libSystem, CoreFoundation, SystemConfiguration, Tcl/Tk, TrustEvaluationAgent,
and the named compression, crypto, database, terminal and ffi libraries.
They are system **candidates** because of their absolute install names, not
proven trusted suppliers because their spelling begins with /usr or /System.

Bounded component lstat observations found /usr/lib/dyld regular and the
other 16 exact leaf paths absent. None of these selected paths encountered a
symlink. Absence of an on-disk dylib does not establish absence or presence
in a shared cache. No cache was extracted or inspected and these 17 system
images were not whole-file pinned or recursively closed. dyld's available
disk file was not promoted to a proof of the loader actually used.

Root must explicitly accept:

1. The installed Apple kernel, loader and shared-cache implementation and
   integrity for the observed macOS 26.5.2/build 25F84, including resolution
   and availability of the 17 named system candidates.
2. The selected inspection-tool implementations, signing policy and platform
   trust store as observation infrastructure. Tool executables are pinned;
   their own transitive dependencies, file's magic database and the trust
   store are not recursively mapped here.
3. The adequacy of this installed-extension static overapproximation,
   together with separately stated dynamic import/environment and fresh
   custody assumptions for the actual operation.

All 76 signature display commands reported the Apple signing authority chain
and all verify commands returned zero. These are tool observations, not an
independently established trust anchor or a whole-runtime guarantee.

The host reports arm64. Inspecting both x86_64 and arm64 slices does not prove
which slice a future Python process executes. No Python process was started.

## Bounds and actual tools

The predeclared limits are 256 native objects, depth 32, 64 MiB/file,
1 GiB total supplier/tool hashing, 2 MiB combined output per inspection,
15 seconds/tool and 300 seconds aggregate tool time. There were 76 native
objects, no added non-system suppliers, and no inspection error, signal,
timeout, output overflow or truncated capture among the 307 actual commands:
three tool/host selection calls plus four inspections for each native file.

The native batches' cumulative byte counter is 181,611,268, including repeated
tool and before/after native-file reads. Initial tool discovery and later
administrative identity rechecks are separately accounted in AUTHOR_CHECKS;
historical source-provenance bytes are not native supplier traversal.

The retained aggregate counter is 3,700.782006 ms. The initial three calls
used separate wall-clock Date.now samples: 832 ms in their aggregate counter
and 834 ms summed from their per-call records. Subsequent calls used monotonic
hrtime (2,868.782006 ms). The conservative total is therefore 3,702.782006 ms.
The first author checker incorrectly equated the two initial measurements and
failed; that diagnostic is retained and corrected without rerunning tools.
This is inspection timing, not an external execution supervisor.

The initial selected Xcode otool path is a symlink to llvm-otool. A first
strict nonsymlink metadata reader rejected it (tool chunk 13f3c4, exit 1).
That failure is retained, not relabeled as success. A bounded readlink
observation recorded the relative target; the exact target was declared in
policy, whole-pinned, then invoked directly. No target was executed during
this failure or recovery.

No target interpreter, qualification caller, control, source helper or
scientific fixture was executed. No new launcher was created.

## Snapshot and provenance limits

SOURCE_DEPENDENCIES.json and SOURCE_IDENTITIES.json close 322 historical
source/preparation paths through explicit administrative routing, including
the whole predecessor packet. Their read-window identities and the current
native observations are separate branches. Current signatures/bytes were
stable across the finite inspections; that is not uninterrupted custody or
a filesystem freeze. The current sealed namespace does not rewrite the
historical policy snapshots retained in tool records.

This graph does not prove symbol-binding success, arbitrary dlopen/plugin
targets, actual imports, environmental independence, runtime resource limits,
or complete system-cache contents. No test/optional root was silently removed.
The absence of weak/lazy edges is an observation about these load commands,
not a statement that the runtime cannot load anything lazily.

## Reuse and unchanged research status

For measurement, this packet can support a separate preflight only if it
selects these exact interpreter/framework/native bytes and compatible
platform premises, freshly reconciles them, and explicitly handles its own
sources, imports and dynamic suppliers. It is not a measurement admission.

RI165 owns the separately assigned external supervision work. RT03 fresh
root admission and execution custody, and RT04 actual flag/resource behavior,
remain separate. No request, admission or operational output namespace was
created here. The prepared qualification counts remain prospective: 2,547
records/mode, 5,094 total, zero executed by RI164.

The actual grid and scientific conclusions are unchanged. This packet
contains no new quantum, geometry, mass, gravity or ontology result.
RET remains paused; measurement stays separate. Root owns review,
operational authorization and repository publication.
