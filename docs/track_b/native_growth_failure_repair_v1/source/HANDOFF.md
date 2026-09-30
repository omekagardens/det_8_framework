# RI140: narrow F01/F02 source repair

This packet proposes repairs to the two findings that caused root to reject
RI138 for operational use. It stops for fresh complete nonauthor review and
root adjudication. It is not execution admission or a passing qualification.

The immutable predecessor is
`ri138-native-external-launch-source-92pbd52w/HANDOFF.json`, 5173 bytes,
SHA-256 `6ee043592352d35048bb31a34aa8b550bb830a9af2afc99170db14b3806510e0`.
The selecting independent review and root decision remain pinned, including
their negative findings. Root separately authorized the related collector
startup acquisition defect within F01. No prior source was overwritten.

## What changed

F01 initializes and locally registers the launcher sink before acquisition,
protects the ordinary-signal transition through descriptor and phase ownership,
and preserves genuine failed-open preownership. Known resources remain available
to independent close and owned-phase after custody. SIGALRM remains immediate;
hard-stop incompleteness is not converted into a successful tail.

The related F01 startup repair establishes record-only ordinary handlers before
collector resource acquisition and protects restoration on ordinary tails.
Only TERM/INT/HUP handler-state transitions use a temporary saved signal mask;
SIGALRM is excluded. Pending observations are not fabricated handler deliveries.
Recorded interruptions and failed restoration cannot yield a successful return.

F02 records the original pipe read, sink-write, child-overflow or census-overflow
cause before unregister/close cleanup. Owner-scoped propagation refers to that
cause without duplicating or relabeling it. EOF-only close failure, raw prefixes,
overflow evidence and all resource limits are preserved.

`custody.py` is byte-for-byte unchanged. The RI136 dispatcher and all 77 native
and 62 audit policy cases remain unchanged. Neither a new general launcher nor
an enlarged scientific/policy inventory is introduced.

## Evidence and review route

- F01_SOURCE_NOTES.md and F02_SOURCE_NOTES.md explain the exact failure-path
  changes; the latter also describes the authorized F01 startup transition.
- ROOT_INTERFACE_CONTRACT.md preserves root/tool provenance, literal dispatch,
  finite custody, resource and evidence boundaries.
- SOURCE_CODE.diff contains the complete old-to-new Python changes.
  METADATA_CONTRACT.diff contains complete changes to shared metadata/contracts.
- SOURCE_CORRESPONDENCE.json gives exact unchanged definition slices, changed
  and added definitions, complete source pins and full-delta reconstruction.
  Text matching is not Python parsing, compilation, execution or a theorem.
- AUTHOR_STATIC_CHECKS.json reports administrative source/metadata checks only.
  Authors and author peers cannot confer independent acceptance on this packet.
- REVIEW_OBLIGATIONS.md identifies the required complete review.
  FOCUSED_QUALIFICATION_DESIGN.md is prospective only: at most 31 separately
  admitted attempts (23 F01, eight F02), without a controller or any executed
  fault. Boundary-control feasibility remains unimplemented and unqualified.

The active dependency selection is 423 files: all 396 inherited entries remain
identical except sorted role numbering, plus 15 complete RI138 source files,
eight compact review records, three native root records and one startup scope
addendum. The four declared V1/V2 external diagnostic bodies are not selected or
newly read. Their pins and failed history remain explicit. The operational
64-MiB read cap is unchanged; there is no retrospective full-history expansion.

The subject manifest binds this ancestry and the unchanged subjects, not its
own hash or the current code. The externally pinned current HANDOFF.json binds
all current payloads without self-reference. Its predecessor is RI138; the
executable dispatcher ancestry remains the distinct RI136 source handoff.

## Disposition and stop

Zero subject/helper imports, compilations, AST passes, probes, fixtures, controls,
scientific executions, current runtime captures, operational cards or admissions
were performed here. There are no repository, index or Git changes. The owner
retains publication, Git and runtime-admission authority.

The actual native scientific question remains the C2/C3 strict signs and shared
H30 feasibility. This repair supplies no answer, QM derivation, geometry bridge
or physical claim. All policy outcomes and deeper caller obligations remain
separate. Measurement remains independent and RET remains paused.

Next disposition: fresh complete nonauthor review and root adjudication of this
exact packet. No execution or successor research starts from author checks.
