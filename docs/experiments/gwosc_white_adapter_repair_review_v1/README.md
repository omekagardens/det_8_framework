# RI156 independent source review and required repairs

30 September 2026. Root independently confirms two source-level custody defects
in the sealed RI156 measurement adapter and requires repair before source
acceptance, qualification or operational admission.

F01: the source observation taken after authentication is not compared with the
already authenticated adapter/module/manifest pins; changed bytes can become
the tail baseline. F02: final owned-output observations are not reconciled with
captured ordinary/action-specific output pins, and the saved-mode final root
observation is not compared with its verified expected post observation.
Both are observable missing comparisons, not claims about an executed attack.

Read review/INDEPENDENT_SOURCE_REVIEW.md, review/VERDICT.json and
root/MEASUREMENT_ROOT_REVIEW.md. The independent reviewer read all eleven
modules and all 55 control definitions. Root traced both findings through the
actual callers and I/O helper. Root replayed the inspected V2 administrative
checker: 4621 predicates, 481 dependencies, 508 fresh whole identities. That
check validates bookkeeping, not source correctness or scientific results.
The five unchanged modules are inherited accepted premises; prior reviewer
WHITE/RI130 authorship is disclosed. No controls or subject code were executed.

This compact archive contains the twelve-file public review subset and seven
root records. The sealed 26-file implementation stays at its pinned external
location and is not published as accepted source. The complete V1/V2/root
metadata diagnostics remain externally pinned. Original handoff names and
references remain unchanged; this compact archive does not pretend to be the
complete original namespace or a self-contained runtime archive. The dependency
map locates the selected 508 observations plus helper and three diagnostics in
fixed-parent Git, this archive or external originals.

RI158 is assigned under root/MEASUREMENT_REPAIR_ASSIGNMENT.json in a fresh
external reservation. It must add source-pin and output-byte reconciliation plus
focused inert integration controls while retaining all existing 55 controls,
first-error/independent-tail/partial-output semantics and original thresholds.
Its active source is excluded. The native RI157 proof is separately under
review, as recorded in root/NATIVE_REVIEW_ASSIGNMENT.json; no acceptance of its
new claims is made by this measurement disposition.

After repaired source review, current-source control qualification, explicit R01
path applicability, actual new-environment capture and profiles, genuine WHITE
modes, complete independent custody and separate saved arithmetic are still
required. Full32, periodic/mean/join, conventional public GWOSC reproduction,
calibration and a native forward map remain separate. RET remains paused.
