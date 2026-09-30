# Root RI140 integration review

This note records root's own source deductions and literal checks. It is not an
execution admission or an assertion that the proposed fault controls ran. Final
disposition also requires the separate complete nonauthor review.

The sealed handoff is 6,044 bytes, SHA256
`8726a3d8be2d62b2326a6ad45d5e1f497fda521d4a1e4a9c92e04101c16f2141`.
Root read the entire Python delta, the process collector, launcher acquisition,
authentication, phase/observation and terminal integration paths, both component
notes, the root interface and complete prospective qualification design. The
unchanged custody implementation is delegated to fresh complete nonauthor review;
root does not claim another independent manual read of all 2,507 module lines.

F01 now makes the launcher sink recoverable before open. Ordinary interruption
is recorded through descriptor and phase-owner registration. Real failed open
leaves no descriptor and no phase ownership. The exact acquisition-primary
sentinel prevents a later ordinary interruption from replacing that exception
while it is active; it is not a blanket suppression of later exceptions. The
observation path selects a failing journal callback after acquisition failure
while retaining the full frozen observation attempt and known-descriptor close.
An immediate hard alarm remains an incomplete best-effort path. Arbitrary repeated
signals after the protected acquisition do not acquire a guarantee of complete
cleanup; the component note expressly retains that boundary.

The collector establishes record-only ordinary handlers before startup sinks.
Only TERM/INT/HUP are temporarily masked during handler installation/restoration;
the exact old mask is restored. The supported caller premise is the pinned
raising-handler launcher with initially unblocked ordinary signals. A callable
test alone does not establish behavior. Pending-set observations are distinct
from delivered-signal records. Provisional saved receipts precede restoration:
the final return and actual outer outcome remain necessary. Host mask/handler
failures and hard aborts are refused or incomplete, never inferred successful
from an earlier receipt. SIGALRM is not added to the ordinary mask.

F02 records the original read, write or overflow failure before independent
unregister/close attempts. Its owner-scoped propagation token preserves that
record through census, tail and body catches without adding a relabelled primary.
Unrelated earlier failures remain first. EOF-only cleanup keeps its separate
meaning. Prefix, output/RSS/time bounds, finite sample semantics and original
custody/outer-origin premises are unchanged.

Root check `4714f0`, exit 0, independently rehashed all 423 selected dependencies
(169,620,097 bytes), compared every one of the 396 inherited entries except its
sorted role number, and checked the 27 additions. Both full diffs reconstruct all
nine shared source/metadata targets exactly; all 96 unchanged definition slices
match their recorded bytes, with overlapping class/method slices explicitly not
treated as disjoint coverage or semantic proof. The source packet has exactly
17 files, all 16 payload identities verified. The four declared external-only
historical diagnostic bodies were not opened or promoted into execution inputs.

No source import, compile, AST pass, runtime inventory, fault injection, operational
card or scientific run occurred. The at-most-31 focused attempts remain a design:
23 F01 and eight F02. Exact boundary-controller feasibility is still unimplemented
and must be decided without silently changing subjects, substituting successful
receipts or counting intended timing as an observed fault. All 139 policy outcomes,
20/42 deeper obligations, actual C2/C3 strict signs and simultaneous H30 feasibility
remain separate. Measurement proceeds independently and RET remains paused.
